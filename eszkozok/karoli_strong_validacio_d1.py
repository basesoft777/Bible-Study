#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V21 — az online validációs felület D1-betöltője (DT-F175vp).

A letétből (`~/Bible-Study-letet/`, a repón kívül) elkészíti a D1 adatbázis betöltő SQL-jét: a sémát
(`eszkozok/karoli_strong_validacio_worker/schema.sql`), a tételeket az ellenőrző oldal formájában, az ellenőröket
(a token SHA-256-jával, a token nélkül) és a kiosztást. A kimenet is a letétbe kerül, mert a tételeket tartalmazza:

  * `tokenek.tsv`      — ellenőrönként a 128 bites véletlen token és a link (csak itt és a felhasználónál; a D1-ben
                         csak az SHA-256-ja áll). A név–token megfeleltetést a felhasználó írja a `megjegyzes`
                         oszlopba; a rendszerben név nincs;
  * `admin_kulcs.txt`  — az admin-végpontok kulcsa (Cloudflare secretként kell beállítani: ADMIN_KULCS);
  * `d1_betoltes.sql`  — a betöltő SQL (`npx wrangler d1 execute … --remote --file …`).

Ellenőrök: E1 = a külső ellenőr (a teljes minta a csalikkal), E2 = a második ítélő (`kozos` = 1), P1, P2 = a
kétfős próba (a mintán kívüli `proba.tsv`, 10 pár). Betöltés előtt a letétfájlok SHA-256-ját és a tételek
kanonikus JSON-jának SHA-256-ját a repóbeli LEKOTES.md-vel veti össze; eltérésnél nem ír semmit.

Használat (a repó gyökeréből):
    python eszkozok/karoli_strong_validacio_d1.py --uj-tokenek          # első futás: tokenek és admin-kulcs
    python eszkozok/karoli_strong_validacio_d1.py                       # a meglévő tokenekkel újra
    python eszkozok/karoli_strong_validacio_d1.py --alap-url https://karoli-strong-validacio.<fiók>.workers.dev
"""

import argparse
import hashlib
import json
import os
import re
import secrets
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_strong_validacio_kiertekel as ki  # noqa: E402
import karoli_strong_validacio_minta as m  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

LETET = os.path.dirname(m.LETET_ALAP)
SEMA = os.path.join(m.GYOKER, 'eszkozok', 'karoli_strong_validacio_worker', 'schema.sql')
ELLENOROK = [('E1', 'kulso'), ('E2', 'masodik'), ('P1', 'proba'), ('P2', 'proba')]
TOKEN_FEJ = ['ellenor', 'szerep', 'token', 'link', 'megjegyzes']
MAX_UTASITAS = 100000   # a D1 egy SQL-utasításának felső mérete (bájt)


def lekotes_online(lekotes=None):
    """A LEKOTES.md online-táblájának sorai: [(címke, SHA-256)]."""
    ki_ = []
    with open(lekotes or m.LEKOTES, encoding='utf-8') as f:
        for sor in f:
            x = re.match(r'^\| (.+?) \| `([0-9a-f]{64})` \|$', sor.rstrip('\n'))
            if x:
                ki_.append((x.group(1), x.group(2)))
    return ki_


def lekotott(cimke_eleje, lekotes=None):
    t = [h for c, h in lekotes_online(lekotes) if c.startswith(cimke_eleje)]
    if len(t) != 1:
        raise SystemExit('a LEKOTES.md-ben nincs (vagy nem egyértelmű) a(z) „%s” sor' % cimke_eleje)
    return t[0]


def sql_szoveg(s):
    return "'" + s.replace("'", "''") + "'"


def tetelek(letet=LETET):
    """(a külső ellenőr tételei, a második ítélőé, a próbatételek) — a lekötéssel ellenőrizve."""
    for fn in ('minta.tsv', 'F175V_csalik.tsv', 'proba.tsv'):
        ut = os.path.join(letet, fn)
        if not os.path.exists(ut):
            raise SystemExit('hiányzik a letétből: %s (előállítás: python eszkozok/karoli_strong_validacio_minta.py)' % ut)
        if letet == LETET and m.lekotes_sha(fn) != m.fajl_sha256(ut):
            raise SystemExit('a letétfájl SHA-256-ja nem egyezik a LEKOTES.md-vel: %s' % fn)
    valodi = m.minta_olvas(os.path.join(letet, 'minta.tsv'))
    _, csalis = m.letet_olvas(os.path.join(letet, 'F175V_csalik.tsv'))
    osszes = sorted(valodi + csalis, key=lambda r: r['tetel_id'])
    masodik = m.masodik_resz(osszes)
    proba = sorted(m.minta_olvas(os.path.join(letet, 'proba.tsv')), key=lambda r: r['tetel_id'])
    if letet == LETET:
        for cimke, sorok in (('a külső ellenőr tételei', osszes), ('a második ítélő tételei', masodik),
                             ('a próbatételek', proba)):
            if m.tetelek_sha256(sorok) != lekotott(cimke):
                raise SystemExit('a tételek SHA-256-ja nem egyezik a LEKOTES.md-vel: %s' % cimke)
    return osszes, masodik, proba


def tokenek_olvas(ut):
    sorok = []
    with open(ut, encoding='utf-8') as f:
        fej = f.readline().rstrip('\n').split('\t')
        if fej != TOKEN_FEJ:
            raise SystemExit('a tokenfájl fejléce nem a várt: %s' % ut)
        for sor in f:
            sor = sor.rstrip('\n')
            if sor:
                sorok.append(dict(zip(fej, sor.split('\t'))))
    if [(r['ellenor'], r['szerep']) for r in sorok] != ELLENOROK:
        raise SystemExit('a tokenfájl ellenőrei nem a vártak: %s' % ut)
    if any(not re.fullmatch(r'[0-9a-f]{32}', r['token']) for r in sorok):
        raise SystemExit('hibás token a tokenfájlban: %s' % ut)
    return sorok


def tokenek_ir(ut, sorok):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(TOKEN_FEJ) + '\n')
        for r in sorok:
            f.write('\t'.join(r[k] for k in TOKEN_FEJ) + '\n')


def sql_epit(osszes, masodik, proba, tokenek):
    """A betöltő SQL szövege (séma + adat)."""
    with open(SEMA, encoding='utf-8') as f:
        sema = f.read()
    halmaz = {'kulso': osszes, 'masodik': masodik, 'proba': proba}
    ut = ['-- GENERÁLT: eszkozok/karoli_strong_validacio_d1.py (F175.V21) — a letétben marad, a repóba nem kerül.',
          '-- Üres D1 adatbázisba töltendő; a sima INSERT miatt kétszeri betöltés hibával áll meg, nem ír felül.', '',
          sema.strip(), '']
    adat = {}
    for r in osszes + proba:
        adat[r['tetel_id']] = m.oldal_adat([r])[0]
    for tid in sorted(adat):
        js = json.dumps(adat[tid], ensure_ascii=False, separators=(',', ':'))
        ut.append('INSERT INTO tetel (id, adat) VALUES (%s, %s);' % (sql_szoveg(tid), sql_szoveg(js)))
    for r in tokenek:
        sorok = halmaz[r['szerep']]
        ut.append('INSERT INTO ellenor (id, szerep, token_sha256, minta_hash, tetelszam) VALUES (%s, %s, %s, %s, %d);'
                  % (sql_szoveg(r['ellenor']), sql_szoveg(r['szerep']),
                     sql_szoveg(hashlib.sha256(r['token'].encode('ascii')).hexdigest()),
                     sql_szoveg(ki.minta_hash(sorok)), len(sorok)))
    for r in tokenek:
        for s in halmaz[r['szerep']]:
            ut.append('INSERT INTO kiosztas (ellenor, tetel) VALUES (%s, %s);'
                      % (sql_szoveg(r['ellenor']), sql_szoveg(s['tetel_id'])))
    for u in ut:
        if len(u.encode('utf-8')) > MAX_UTASITAS:
            raise SystemExit('túl hosszú SQL-utasítás (%d bájt): %s' % (len(u.encode('utf-8')), u[:80]))
    return '\n'.join(ut) + '\n'


def tetel_frissites_sql(osszes, proba):
    """A már betöltött D1 tételeinek frissítése (UPDATE tetel SET adat = …): a tokeneket, az ellenőröket és a kiosztást
    nem érinti (a konvenció-egységesítés után a kártyák a vers többi párját az 1.1 szerint mutatják; DT-F175vr)."""
    ut = ['-- GENERÁLT: eszkozok/karoli_strong_validacio_d1.py --tetel-frissites — a letétben marad, a repóba nem kerül.',
          '-- Csak a tetel tábla adat mezőjét írja; a tokent, az ellenőrt, a kiosztást és a válaszokat nem.', '']
    for r in sorted(osszes + proba, key=lambda r: r['tetel_id']):
        js = json.dumps(m.oldal_adat([r])[0], ensure_ascii=False, separators=(',', ':'))
        ut.append('UPDATE tetel SET adat = %s WHERE id = %s;' % (sql_szoveg(js), sql_szoveg(r['tetel_id'])))
    for u in ut:
        if len(u.encode('utf-8')) > MAX_UTASITAS:
            raise SystemExit('túl hosszú SQL-utasítás (%d bájt): %s' % (len(u.encode('utf-8')), u[:80]))
    return '\n'.join(ut) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--uj-tokenek', action='store_true', help='új tokenek és admin-kulcs (csak ha még nincsenek)')
    ap.add_argument('--alap-url', help='a Worker címe (pl. https://karoli-strong-validacio.<fiók>.workers.dev); '
                                       'a linkek a tokenfájlba kerülnek')
    ap.add_argument('--letet', default=LETET)
    ap.add_argument('--tetel-frissites', metavar='FAJLNEV',
                    help='csak a betöltött D1 tételeinek frissítő SQL-je a letétbe (új fájl; a tokeneket nem érinti)')
    a = ap.parse_args()
    tok_ut = os.path.join(a.letet, 'tokenek.tsv')
    admin_ut = os.path.join(a.letet, 'admin_kulcs.txt')
    osszes, masodik, proba = tetelek(a.letet)
    if a.tetel_frissites:
        ut = os.path.join(a.letet, os.path.basename(a.tetel_frissites))
        if os.path.exists(ut):
            raise SystemExit('a fájl már létezik, nem írom felül: %s' % ut)
        sql = tetel_frissites_sql(osszes, proba)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(sql)
        print('tétel-frissítő SQL: %s (%d tétel, SHA-256 %s)' % (ut, len(osszes) + len(proba),
                                                                hashlib.sha256(sql.encode('utf-8')).hexdigest()))
        return
    if os.path.exists(tok_ut):
        if a.uj_tokenek:
            raise SystemExit('a tokenfájl már létezik (%s); új tokenekhez előbb kézzel kell félretenni' % tok_ut)
        tok = tokenek_olvas(tok_ut)
    elif a.uj_tokenek:
        tok = [{'ellenor': e, 'szerep': sz, 'token': secrets.token_hex(16), 'link': '', 'megjegyzes': ''}
               for e, sz in ELLENOROK]
        with open(admin_ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(secrets.token_hex(32) + '\n')
    else:
        raise SystemExit('nincs tokenfájl (%s). Első előállításhoz: --uj-tokenek' % tok_ut)
    if a.alap_url:
        alap = a.alap_url.rstrip('/')
        if not re.fullmatch(r'https://[A-Za-z0-9.-]+', alap):
            raise SystemExit('az --alap-url alakja: https://<host>')
        for r in tok:
            r['link'] = '%s/?t=%s' % (alap, r['token'])
    # a tokenfájl a letét védett fájlja: csak új tokeneknél íródik; a meglévő nem íródik felül (DT-F175vl)
    if not os.path.exists(tok_ut):
        tokenek_ir(tok_ut, tok)
    elif tokenek_olvas(tok_ut) != tok:
        raise SystemExit('a tokenfájl tartalma változna (pl. --alap-url): a meglévő tokenfájl nem íródik felül')
    sql = sql_epit(osszes, masodik, proba, tok)
    sql_ut = os.path.join(a.letet, 'd1_betoltes.sql')
    with open(sql_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(sql)
    print('D1-betöltő: %s (%d bájt, SHA-256 %s)' % (sql_ut, len(sql.encode('utf-8')),
                                                     hashlib.sha256(sql.encode('utf-8')).hexdigest()))
    print('  tételek: %d (külső ellenőr %d, második ítélő %d, próba %d)'
          % (len(osszes) + len(proba), len(osszes), len(masodik), len(proba)))
    print('  tokenek: %s; admin-kulcs: %s (mindkettő csak a letétben)' % (tok_ut, admin_ut))
    print('  minta_hash: E1 %s, E2 %s, próba %s' % (ki.minta_hash(osszes), ki.minta_hash(masodik), ki.minta_hash(proba)))


if __name__ == '__main__':
    main()
