#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/f93_tipnr_token_hiany.py -- F93: a TIPNR token nélküli alapszámainak osztályozása.

Bemenet: a kész pardes.db (CSAK OLVASÁS; argumentum, vagy PARDES_DB, vagy ./pardes.db).
A `tipnr` táblának azok az utótag nélküli sorai, amelyek `strong` értéke a `token_strong`-ban
nem szerepel (a #88 levágott utótagos sora nem tartozik ide). Kimenet: naplok/F93_alapszamok.tsv
(alapszámonként egy sor). Jelölés, nem javítás: a TIPNR/TAGNT/TAHOT és a pardes.db nem változik.

Osztályok (DT-F93a, 2026-10-15, felhasználói döntés):
  szövegváltozat      kiadás-jelölés a Névváltozatban + a versen azonos nevű más Strong-token
                      (görögnél másik nevű is, ha) a token `Kritikai kiadás` mezője a jelölt
                      kiadást nem tartalmazza
  alak-/névhasítás    nincs kiadás-jelölés, de a versen ugyanazon név (nev) más Strong-száma tokenként megvan
  számozási eltérés   a versen nincs token, de a szomszédos versben az azonos nevű token megvan
  nincs Károli-vers   a TIPNR-sor igehelye üres (LXX.* hely)
  adathiány           nincs jelölés, a versen nincs azonos nevű token
  nem eldönthető      minden más; explicit jelölve, nem kitöltve (CLAUDE.md 3. szabály)

Két futás kimenete bájtazonos: a ts a pardes.db meta.epites_ts értéke, a rendezés kulcsos.
TSV-írás '\\t'.join()-nal (a csv modul tilos).
"""
import collections
import os
import re
import sqlite3
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIMENET = os.path.join(GYOKER, 'naplok', 'F93_alapszamok.tsv')
OSZLOPOK = ['strong', 'nev', 'nevvaltozat', 'igehely', 'osztaly', 'tagnt_strong_a_versen',
            'tagnt_kiadas', 'indoklas', 'proveniencia', 'nyelv', 'tipnr_sorok']
KIADAS_RE = re.compile(r'=([A-Za-z]+(?:,[A-Za-z]+)*)')
# a TAGNT `Kritikai kiadás` mező alapkiadásai (a ritka kéziratjelölések, KJV/NIV maradványok nélkül)
TAGNT_KIADASOK = {'NA28', 'NA27', 'Tyn', 'SBL', 'WH', 'Treg', 'TR', 'Byz'}
NINCS_KIADAS_MEZO = 'n/a (a TAHOT-kivonat nem hordoz kiadás-mezőt)'


def kiadasok(nevvaltozat):
    t = set()
    for m in KIADAS_RE.finditer(nevvaltozat or ''):
        t.update(m.group(1).split(','))
    return t


def vers_parse(ig):
    m = re.match(r'^(.+) (\d+):(\d+)$', ig or '')
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def kiadas_halmaz(szoveg):
    return set(szoveg.replace('/', '+').replace(' ', '').split('+'))


def main(argv):
    db = argv[1] if len(argv) > 1 else os.environ.get('PARDES_DB') or os.path.join(GYOKER, 'pardes.db')
    kim = argv[2] if len(argv) > 2 else KIMENET
    c = sqlite3.connect('file:%s?mode=ro' % db.replace('\\', '/'), uri=True)
    r = c.execute("select ertek from meta where kulcs='epites_ts'").fetchone()
    ts = r[0] if r else 'ismeretlen'
    prov = ('scope=tipnr(utótag nélkül) ∖ token_strong; token_eredeti (TAGNT/TAHOT) | '
            'forras=pardes.db (epites_ts=%s), konkordancia/TIPNR_kivonat.tsv, TAGNT_kivonat.tsv, '
            'TAHOT_kivonat.tsv | ts=%s' % (ts, ts))

    rows = c.execute("select nev,nevvaltozat,strong,nyelv,igehely,step_nyers from tipnr "
                     "where utotag='' and strong not in (select strong from token_strong) "
                     "order by strong, igehely, step_nyers, nev, nevvaltozat").fetchall()

    def van_token(ig):
        return c.execute("select 1 from token_eredeti where igehely=? limit 1", (ig,)).fetchone() is not None

    def vers_nevei(ig, ny, s):
        """A versen tokenként megvan: a TIPNR más (utótag nélküli) Strong-számai ugyanazon a versen."""
        van = []
        for (st, n) in c.execute("select distinct strong, nev from tipnr where igehely=? and nyelv=? "
                                 "and strong<>?", (ig, ny, s)).fetchall():
            if c.execute("select 1 from token_strong where igehely=? and strong=? limit 1",
                         (ig, st)).fetchone():
                van.append((st, n))
        return sorted(set(van))

    def kiadas_mezo(ig, st, ny):
        if ny != 'görög':
            return NINCS_KIADAS_MEZO
        v = set()
        for (k,) in c.execute("select kritikai_kiadas from token_eredeti where igehely=? and "
                              "(strong_lanc=? or strong_lanc like ? or strong_lanc like ? or strong_lanc like ?)",
                              (ig, st, st + '+%', '%+' + st, '%+' + st + '+%')):
            v.add(k)
        return ' / '.join(sorted(v)) if v else 'n/a'

    def szomszedok(ig):
        p = vers_parse(ig)
        if not p:
            return []
        k, f, v = p
        lista = []
        if v > 1:
            lista.append('%s %d:%d' % (k, f, v - 1))
        lista.append('%s %d:%d' % (k, f, v + 1))
        lista.append('%s %d:1' % (k, f + 1))
        return lista

    alap = {}
    for (nev, nv, s, ny, ig, step) in rows:
        alap.setdefault(s, []).append((nev, nv, ny, ig, step))

    kim_sorok = []
    for s in sorted(alap):
        sorok = alap[s]
        osztalyok, strongok, kiadasok_l, indok, igek = [], [], [], [], []
        for (nev, nv, ny, ig, step) in sorok:
            hely = ig if ig else step
            igek.append(hely)
            tag = kiadasok(nv)
            tagszoveg = ','.join(sorted(tag))
            if ig is None:
                osztalyok.append('nincs Károli-vers')
                indok.append('%s: a TIPNR-sor igehelye üres, nincs Károli-vers, tehát TAGNT/TAHOT-vers sem' % hely)
                continue
            cand = vers_nevei(ig, ny, s)
            azonos = [x for x in cand if x[1] == nev]
            if not van_token(ig):
                megvan = None
                for z in szomszedok(ig):
                    for (st, n) in c.execute("select distinct strong, nev from tipnr where igehely=? and nyelv=? "
                                             "and nev=? and strong<>?", (z, ny, nev, s)).fetchall():
                        if c.execute("select 1 from token_strong where igehely=? and strong=? limit 1",
                                     (z, st)).fetchone():
                            megvan = (z, st)
                            break
                    if megvan:
                        break
                if megvan:
                    osztalyok.append('számozási eltérés')
                    strongok.append('%s:%s' % megvan)
                    kiadasok_l.append(kiadas_mezo(megvan[0], megvan[1], ny))
                    indok.append('%s: a versen nincs token; a szomszédos %s versben az azonos nevű (%s) %s token megvan'
                                 % (hely, megvan[0], nev, megvan[1]))
                else:
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: a versen nincs token, és a szomszédos versben sincs azonos nevű (%s) token'
                                 % (hely, nev))
                continue
            if tag:
                if ny == 'görög':
                    osszeh = sorted(tag & TAGNT_KIADASOK)
                    if not osszeh:
                        osztalyok.append('nem eldönthető')
                        indok.append('%s: kiadás-jelölés (%s), de egyik jelölt kiadás sincs a TAGNT Kritikai kiadás mezőjének kiadásai között (%s)'
                                     % (hely, tagszoveg, '+'.join(sorted(TAGNT_KIADASOK))))
                        continue
                    talalt = None
                    for (st, n) in azonos + [x for x in cand if x not in azonos]:
                        kk = kiadas_mezo(ig, st, ny)
                        if not (set(osszeh) & kiadas_halmaz(kk)):
                            talalt = (st, n, kk)
                            break
                    if talalt:
                        osztalyok.append('szövegváltozat')
                        strongok.append('%s:%s' % (hely, talalt[0]))
                        kiadasok_l.append(talalt[2])
                        indok.append('%s: kiadás-jelölés (%s); a versen %s (%s) %s token, Kritikai kiadás: %s (a %s kiadást nem tartalmazza)'
                                     % (hely, tagszoveg, 'azonos nevű' if (talalt[0], talalt[1]) in azonos else 'más nevű',
                                        talalt[1], talalt[0], talalt[2], '+'.join(osszeh)))
                    else:
                        osztalyok.append('nem eldönthető')
                        indok.append('%s: kiadás-jelölés (%s), de a versen nincs olyan token, amelynek Kritikai kiadás mezője a %s kiadást nem tartalmazza'
                                     % (hely, tagszoveg, '+'.join(osszeh)))
                elif azonos:
                    st = azonos[0][0]
                    strongok.append('%s:%s' % (hely, st))
                    kiadasok_l.append(NINCS_KIADAS_MEZO)
                    osztalyok.append('szövegváltozat')
                    indok.append('%s: kiadás-jelölés (%s); a versen azonos nevű (%s) %s token; a TAHOT nem hordoz kiadás-mezőt'
                                 % (hely, tagszoveg, nev, st))
                elif cand:
                    strongok.append('%s:%s' % (hely, cand[0][0]))
                    kiadasok_l.append(NINCS_KIADAS_MEZO)
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: kiadás-jelölés (%s), a versen csak más nevű token (%s %s); a TAHOT nem hordoz kiadás-mezőt, azonos nevű token nincs'
                                 % (hely, tagszoveg, cand[0][1], cand[0][0]))
                else:
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: kiadás-jelölés (%s), de a versen nincs a névhez köthető token' % (hely, tagszoveg))
            else:
                if azonos:
                    st = azonos[0][0]
                    osztalyok.append('alak-/névhasítás')
                    strongok.append('%s:%s' % (hely, st))
                    kiadasok_l.append(kiadas_mezo(ig, st, ny))
                    indok.append('%s: nincs kiadás-jelölés (Névváltozat: %s); a versen azonos nevű (%s) %s token van, a TIPNR a névalaknak külön Strong-számot ad'
                                 % (hely, nv, nev, st))
                elif cand:
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: nincs kiadás-jelölés, a versen csak más nevű token (%s) van' % (hely, cand[0][1]))
                else:
                    osztalyok.append('adathiány')
                    indok.append('%s: nincs kiadás-jelölés, a versen nincs a névhez köthető token' % hely)
        egyedi = sorted(set(osztalyok))
        if len(egyedi) == 1:
            osz = egyedi[0]
        else:
            osz = 'nem eldönthető'
            indok.append('az alapszám sorai több osztályba esnek (%s)' % ', '.join(egyedi))
        kim_sorok.append([s, sorok[0][0], ' || '.join(sorted({x[1] for x in sorok})), ' ; '.join(igek),
                          osz, ' ; '.join(strongok) or '-', ' ; '.join(kiadasok_l) or '-',
                          ' | '.join(indok), prov, sorok[0][2], str(len(sorok))])

    for sor in kim_sorok:
        for m in sor:
            assert '\t' not in m and '\n' not in m
    szoveg = '\t'.join(OSZLOPOK) + '\n' + ''.join('\t'.join(x) + '\n' for x in kim_sorok)
    with open(kim, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    ossz = collections.Counter()
    sor_ossz = collections.Counter()
    for x in kim_sorok:
        ossz[(x[9], x[4])] += 1
        sor_ossz[(x[9], x[4])] += int(x[10])
    print('alapszám: %d, sor: %d' % (len(kim_sorok), sum(int(x[10]) for x in kim_sorok)))
    for k in sorted(ossz):
        print(k, 'alapszám', ossz[k], 'sor', sor_ossz[k])


if __name__ == '__main__':
    main(sys.argv)
