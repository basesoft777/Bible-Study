#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teljesseg_meres.py -- egy motívum előfordulás-listájának teljesség-mérése három független
hálóval (DT548, F123_MIGRACIO2_BRIEF.md U1). Csak olvas; adattáblát nem ír.

A három háló:
    1. Strong:  a motívum Strongjainak (az `elofordulasok.tsv` `strong` mezője) minden
                előfordulása a TAHOT/TAGNT-ben;
    2. Károli:  a megadott szótári alakok (a motívum Károli-szavai) minden előfordulása a
                Károli 1908-ban, az `adat/szoto/karoli_szotari_alak.tsv` szótövező táblán át;
    3. szótár:  a BDB (`adat/bdb_vers_jelentes.tsv`) és a Thayer (`adat/thayer_vers_jelentes.tsv`)
                által a motívum Strongjainál idézett igehelyek (Károli-vers).

Minden találat állapota: `E` (előfordulás-sor), `J:<döntés>` (jelöltsor) vagy `ELTÉRÉS`
(a háló talál, az adat nem ismeri). A találat mellett áll, hogy a versben ott van-e a
motívum valamelyik Strongja (`gerinc_a_versben`): a 2. és a 3. háló eltérése ennek
hiányában a lexikai negatív kritériumon akad meg, és ez a döntés előkészítése, nem döntés.

A Károli-szavak listája paraméter (`--karoli-szavak`), mert a motívum Károli-szavainak
kijelölése (melyik szó fordítja a motívum szavát, és melyik csak a környezete) kutatói
döntés. Paraméter nélkül az eszköz csak a jelölt szótári alakokat listázza
(`karoli_szo`-mezők → szótári alak, soronkénti darabszámmal), scant nem futtat.

Szópár-mód (`--kollokacio`, az ANTROP-001-nél készült, F123.ANTROP2.2): ha a motívum azonossága
két szó együttállása (a `gerinc_elem` `A+B` alakú), az 1. háló nem a Strongok egyenkénti
előfordulása, hanem azok a versek, amelyekben a pár minden tagja áll (a `--rokon A=A2,B=B2`
leképezéssel a tag rokon alakja is számít, pl. a főnév melléknévi alakja). A 2. és a 3. háló
`gerinc_a_versben` mezője ekkor azt mondja meg, hogy a pár áll-e a versben, a `reszlet` mező
végén pedig a versben álló egyes Strongok szerepelnek (`[a versben: …]`): a más lexémás és a
csak egyik tagot hordozó találat így lexémánként csoportosítható (`sablonok/9_…` v1, 2. szabály).

Használat:
    python eszkozok/teljesseg_meres.py ID [--karoli-szavak sír,pokol,...] [--ki naplok/F123_teljesseg_ID]
    python eszkozok/teljesseg_meres.py ID --kollokacio [--rokon G4151=G4152,G5590=G5591] [...]
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import lekerdez as L  # noqa: E402

SZO = re.compile(r'[^\W\d_]+', re.UNICODE)
TARTOMANY = re.compile(r'^(.+?) (\d+):(\d+)-(\d+)$')


def ts():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')


def olvas(ut):
    """TSV olvasása split('\\t')-vel (CLAUDE.md: a csv modul ezeken a táblákon adatot ront);
    a '#' kezdetű sorok kimaradnak, az első nem-megjegyzés sor a fejléc."""
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:] if s.strip()]


def versekre(igehely):
    """'Jel 20:13-14' → ['Jel 20:13', 'Jel 20:14']; egyes vers változatlan."""
    m = TARTOMANY.match(igehely.strip())
    if not m:
        return [igehely.strip()]
    konyv, fej, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
    return ['%s %s:%d' % (konyv, fej, v) for v in range(a, b + 1)]


def motivum_adat(mid, elof_ut, jelolt_ut):
    """(strongok, E-versek, J-versek {vers: döntés}, karoli_szo-lista)"""
    strongok, e_versek, karoli = set(), set(), []
    for r in olvas(elof_ut):
        if r.get('id') != mid:
            continue
        for s in (r.get('strong') or '').split('+'):
            if s.strip():
                strongok.add(s.strip())
        e_versek.update(versekre(r['igehely']))
        if r.get('karoli_szo'):
            karoli.append(r['karoli_szo'])
    j_versek = {}
    for r in olvas(jelolt_ut):
        if r.get('id') != mid or r.get('jelolt_tipus', 'elofordulas') not in ('', 'elofordulas'):
            continue
        for v in versekre(r['igehely']):
            j_versek.setdefault(v, r.get('dontes', ''))
    return strongok, e_versek, j_versek, karoli


def parok(mid, elof_ut):
    """A `gerinc_elem` mező `A+B` alakú elemei, tagonként: [('G4151', 'G5590'), ...]."""
    ki = set()
    for r in olvas(elof_ut):
        if r.get('id') == mid and '+' in (r.get('gerinc_elem') or ''):
            ki.add(tuple(s.strip() for s in r['gerinc_elem'].split('+') if s.strip()))
    return sorted(ki)


def rokon_terkep(szoveg):
    """'G4151=G4152,G5590=G5591' → {'G4151': {'G4151', 'G4152'}, 'G5590': {'G5590', 'G5591'}}"""
    t = {}
    for tag in (x.strip() for x in szoveg.split(',') if x.strip()):
        a, _, b = tag.partition('=')
        t.setdefault(a.strip(), {a.strip()}).add(b.strip())
    return t


def vers_strongjai(strongok, tahot, tagnt):
    """{vers: {Strong, ...}} a megadott Strongokra (a 2. és 3. háló `reszlet`-kiegészítéséhez)."""
    v = defaultdict(set)
    for r in list(tahot) + list(tagnt):
        if r['Strong-szám'] in strongok:
            v[r['Igehely']].add(r['Strong-szám'])
    return v


def halo_par(par_lista, rokon, vs):
    """{vers: [Strong, ...]} azokra a versekre, amelyekben egy pár minden tagja (vagy rokon alakja) áll."""
    talalat = {}
    for vers, jelen in vs.items():
        for par in par_lista:
            if all(jelen & rokon.get(tag, {tag}) for tag in par):
                talalat[vers] = sorted(jelen)
                break
    return talalat


def allapot(vers, e_versek, j_versek):
    if vers in e_versek:
        return 'E'
    if vers in j_versek:
        return 'J:' + j_versek[vers]
    return 'ELTÉRÉS'


def szotari_tabla(ut):
    tabla = {}
    for r in olvas(ut):
        tabla.setdefault(r['alak'], r['szotari_alak'])
    return tabla


def szotari_alak(szo, tabla):
    if szo in tabla:
        return tabla[szo]
    return tabla.get(szo.lower(), '')


def karoli_jeloltek(karoli_szavak, tabla):
    """A `karoli_szo`-mezők szavainak szótári alakja → hány sorban áll (soronként egyszer)."""
    db = Counter()
    for k in karoli_szavak:
        db.update({szotari_alak(sz, tabla) or sz.lower() for sz in SZO.findall(k)})
    return db


def halo_strong(strongok, tahot, tagnt):
    """{vers: [Strong, ...]} a motívum Strongjaira."""
    talalat = defaultdict(set)
    for r in list(tahot) + list(tagnt):
        if r['Strong-szám'] in strongok:
            talalat[r['Igehely']].add(r['Strong-szám'])
    return talalat


def halo_karoli(lemmak, karoli_1908, tabla):
    """{vers: [szóalak, ...]} azokra a versekre, amelyekben a lemmák valamelyike áll."""
    talalat = defaultdict(list)
    kis = {lm.lower() for lm in lemmak}
    for vers, szoveg in karoli_1908.items():
        for sz in SZO.findall(szoveg):
            if karoli_egyezik(sz, lemmak, kis, tabla):
                talalat[vers].append(sz)
    return talalat


def karoli_egyezik(szo, lemmak, kis, tabla):
    """A szó szótári alakja a lemmák egyike; ha a szótövező nem töveli (nincs sora, vagy a
    szótári alak maga a szóalak), a szóalak egy lemmával kezdődik (pl. „koporsóba”, „Seolban”;
    a szótövező ismert korlátja, naplok/SZOTOVEZES_meres.md)."""
    sa = szotari_alak(szo, tabla)
    if sa in lemmak:
        return True
    if sa == '' or sa.lower() == szo.lower():
        return any(szo.lower().startswith(lm) for lm in kis)
    return False


def halo_szotar(strongok, bdb_sorok, thayer_sorok):
    """{vers: [forrás-címke, ...]} a BDB és a Thayer által idézett Károli-versekre."""
    talalat = defaultdict(list)
    for r in bdb_sorok:
        if r.get('strong') in strongok and r.get('karoli_vers'):
            talalat[r['karoli_vers']].append('BDB %s sorszam %s (%s)' % (
                r['strong'], r.get('sorszam', ''), r.get('utvonal') or r.get('szakasz') or 'fej'))
    for r in thayer_sorok:
        if r.get('strong') in strongok and r.get('karoli_vers'):
            talalat[r['karoli_vers']].append('Thayer %s sorszam %s (%s)' % (
                r['strong'], r.get('sorszam', ''), r.get('utvonal') or r.get('szakasz') or ''))
    return talalat


def kulcs(vers):
    try:
        return L.parse_igehely(vers)
    except Exception:  # noqa: BLE001 — ismeretlen alak a végére
        return ('~', 0, 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('id')
    ap.add_argument('--karoli-szavak', default='',
                    help='vesszővel elválasztott szótári alakok (a 2. háló); nélküle csak a jelölt alakok listája')
    ap.add_argument('--ki', default='', help='kimeneti előtag (.tsv és .md); nélküle csak összegzés a konzolra')
    ap.add_argument('--kollokacio', action='store_true',
                    help='szópár-mód: az 1. háló a gerinc_elem A+B párjának együttállása egy versben')
    ap.add_argument('--rokon', default='', help='a pár tagjainak rokon alakjai, pl. G4151=G4152,G5590=G5591')
    a = ap.parse_args()

    mid = a.id
    elof = os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')
    jel = os.path.join(GYOKER, 'adat', 'jeloltek.tsv')
    strongok, e_versek, j_versek, karoli = motivum_adat(mid, elof, jel)
    if not strongok:
        sys.exit('%s: nincs Strong az elofordulasok.tsv-ben' % mid)
    tabla = szotari_tabla(os.path.join(GYOKER, 'adat', 'szoto', 'karoli_szotari_alak.tsv'))
    most = ts()

    jelolt_alakok = karoli_jeloltek(karoli, tabla)
    print('# %s — Strongok: %s; E-vers: %d; J-vers: %d' % (mid, ', '.join(sorted(strongok)),
                                                          len(e_versek), len(j_versek)))
    print('# a karoli_szo-mezők szótári alakjai (sor/alak): ' + ', '.join(
        '%s %d' % (k, v) for k, v in jelolt_alakok.most_common()))
    lemmak = {x.strip() for x in a.karoli_szavak.split(',') if x.strip()}

    halok = {}
    vs = {}
    if a.kollokacio:
        par_lista = parok(mid, elof)
        if not par_lista:
            sys.exit('%s: --kollokacio, de nincs A+B alakú gerinc_elem' % mid)
        rokon = rokon_terkep(a.rokon)
        strongok = set().union(*[set(p) for p in par_lista], *[rokon.get(x, set()) for p in par_lista for x in p])
        vs = vers_strongjai(strongok, L.load_tahot(), L.load_tagnt())
        halok['strong'] = halo_par(par_lista, rokon, vs)
        leiras = ' | '.join('+'.join('(%s)' % '|'.join(sorted(rokon.get(x, {x}))) for x in p) for p in par_lista)
        prov_strong = ('scope=TAHOT-teljes+TAGNT-teljes: egy versben %s | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv '
                       '| n=%d | ts=%s' % (leiras, len(halok['strong']), most))
        print('# szópár-mód: %s; a szótár-háló Strongjai: %s' % (leiras, ', '.join(sorted(strongok))))
    else:
        halok['strong'] = halo_strong(strongok, L.load_tahot(), L.load_tagnt())
        prov_strong = ('scope=TAHOT-teljes+TAGNT-teljes | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv '
                       '| strong=%s | n=%d | ts=%s' % ('+'.join(sorted(strongok)), len(halok['strong']), most))
    prov_karoli = ''
    if lemmak:
        halok['karoli'] = halo_karoli(lemmak, L.load_karoli_1908(), tabla)
        prov_karoli = ('scope=Karoli_1908-teljes | forras=Karoli_1908.tsv+adat/szoto/karoli_szotari_alak.tsv '
                       '| szotari_alak=%s | n=%d | ts=%s' % ('+'.join(sorted(lemmak)), len(halok['karoli']), most))
    halok['szotar'] = halo_szotar(strongok, olvas(os.path.join(GYOKER, 'adat', 'bdb_vers_jelentes.tsv')),
                                  olvas(os.path.join(GYOKER, 'adat', 'thayer_vers_jelentes.tsv')))
    prov_szotar = ('scope=%s | forras=adat/bdb_vers_jelentes.tsv+adat/thayer_vers_jelentes.tsv (karoli_vers) '
                   '| n=%d | ts=%s' % ('+'.join(sorted(strongok)), len(halok['szotar']), most))
    provok = {'strong': prov_strong, 'karoli': prov_karoli, 'szotar': prov_szotar}

    sorok = []
    osszeg = {}
    for nev, t in halok.items():
        db = Counter()
        for vers in sorted(t, key=kulcs):
            all_ = allapot(vers, e_versek, j_versek)
            gerinc = 'igen' if vers in halok['strong'] else 'nem'
            db[all_.split(':')[0]] += 1
            if all_ == 'ELTÉRÉS':
                db['ELTÉRÉS, gerinc ' + gerinc] += 1
            reszlet = ', '.join(sorted(t[vers])) if nev == 'strong' else '; '.join(t[vers])
            if a.kollokacio and nev != 'strong':
                reszlet += ' [a versben: %s]' % (', '.join(sorted(vs.get(vers, ()))) or '—')
            sorok.append((nev, vers, all_, gerinc, reszlet, provok[nev]))
        osszeg[nev] = db
    # a fordított irány: E-vers, amelyet egyik háló sem ad
    lefedett = set().union(*[set(t) for t in halok.values()])
    nem_fedett = sorted(e_versek - lefedett, key=kulcs)

    for nev, db in osszeg.items():
        print('%-7s találat %4d | E %3d | J %3d | ELTÉRÉS %3d (gerinc a versben: %d, nincs: %d)' % (
            nev, sum(db[k] for k in ('E', 'J', 'ELTÉRÉS')), db['E'], db['J'], db['ELTÉRÉS'],
            db['ELTÉRÉS, gerinc igen'], db['ELTÉRÉS, gerinc nem']))
    print('E-vers, amelyet egyik háló sem ad: %d %s' % (len(nem_fedett), ', '.join(nem_fedett)))
    for nev, p in provok.items():
        if p:
            print('proveniencia (%s): %s' % (nev, p))

    if a.ki:
        ki = os.path.join(GYOKER, a.ki) if not os.path.isabs(a.ki) else a.ki
        with open(ki + '.tsv', 'w', encoding='utf-8', newline='\n') as f:
            f.write('# GENERÁLT: eszkozok/teljesseg_meres.py %s — kézzel nem szerkesztendő (DT548)\n' % mid)
            f.write('\t'.join(['halo', 'igehely', 'allapot', 'gerinc_a_versben', 'reszlet', 'proveniencia']) + '\n')
            for s in sorok:
                f.write('\t'.join(s) + '\n')
        print('írva: %s.tsv (%d sor)' % (a.ki, len(sorok)))


if __name__ == '__main__':
    main()
