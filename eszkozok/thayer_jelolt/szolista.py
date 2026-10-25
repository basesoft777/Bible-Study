#!/usr/bin/env python
"""Az újrafuttatható M3 szólistája (F132; DT-F132h (1), felhasználó, 2026-10-25).

A futás pillanatában előállítja, mely görög Strongok szakaszonkénti Thayer-fordítása következik:
  - a halmaz: az `adat/elofordulasok.tsv` `strong` mezőjének görög tokenjei (a `+` mentén bontva), `Strong_padded`-re
    normalizálva (`kulcs.strong_pad`) — a motívumok aktuális görög gerincszavai;
  - **kihagyva**, ha a Strongnak minden szakaszához van érvényes szakaszos fordítás: a `forditasok.tsv`-ben `szotar = Thayer`,
    `jelentes_szam = sz<sorszam>`, `mezo = forditas_hu`, nem üres, `allapot ≠ elavult`, és a `forras_hash` egyezik a szakasz
    mai SHA-1-ével (`thayer_bemenet.szakaszok`) — ok: `kesz`; vagy ha a Strong nincs a `thayer_szakaszok.tsv`-ben — ok:
    `nincs_szakasz` (explicit, nem pótolt);
  - **fordítandó** minden más: ok `nincs_szakaszos` (csak `teljes` sor vagy semmi), `hianyos` (szakaszsor hiányzik),
    `elavult_hash` (van szakaszsor, de a `forras_hash` már nem a mai szakaszé).
A DT-F132c (ii) szerinti `kezi` régi sort a lista nem kezeli (az a beírás dolga); a `megjegyzes` jelzi.

Kimenet: TSV (stdout vagy --ki), soronként proveniencia-sorral; a bemenetek hash-e a `# forras:` fejlécsorban.
Fájlt a repóban nem ír (a --ki a hívó útvonala; a lista futásonkénti napló, nem adattábla).

  python eszkozok/thayer_jelolt/szolista.py [--ki PATH] [--ts NAP] [--csak-forditando]
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import datetime
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
if ITT not in sys.path:
    sys.path.insert(0, ITT)
import kulcs  # noqa: E402
import thayer_bemenet as TB  # noqa: E402

GYOKER = TB.GYOKER
ELOFORDULASOK_UT = os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')
FORDITASOK_UT = os.path.join(GYOKER, 'adat', 'forditasok.tsv')

FEJLEC = ['strong', 'statusz', 'ok', 'szakasz', 'karakter', 'csoport', 'illesztes', 'motivumhely', 'megjegyzes', 'proveniencia']


def tsv_dict(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s.rstrip('\r') for s in f.read().split('\n')]
    sorok = [s for s in sorok if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def sha12(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()[:12]


def gerinc_strongok(ut=ELOFORDULASOK_UT):
    """-> OrderedDict: Strong_padded -> a motívumhelyek (különböző `igehely`) száma; a görög tokenek, sorrendben."""
    helyek = collections.OrderedDict()
    for r in tsv_dict(ut):
        for tok in re.split(r'[+\s,;]+', r.get('strong', '')):
            p = kulcs.strong_pad(tok)
            if p:
                helyek.setdefault(p, set()).add(r.get('igehely', ''))
    return collections.OrderedDict((k, len(v)) for k, v in helyek.items())


def thayer_sorok(ut=FORDITASOK_UT):
    d = collections.defaultdict(list)
    for r in tsv_dict(ut):
        if r.get('szotar') == TB.SZOTAR:
            d[kulcs.strong_pad(r.get('strong', '')) or r.get('strong', '')].append(r)
    return d


def allapot(sp, szak, sorok):
    """-> (statusz, ok, megjegyzes)."""
    if szak is None:
        return 'kihagyva', 'nincs_szakasz', 'a Strong nincs a thayer_szakaszok.tsv-ben'
    ervenyes = {}
    van_szakaszsor = False
    for r in sorok:
        n = TB.sorszam_jelentesbol(r.get('jelentes_szam'))
        if n is None or r.get('mezo', 'forditas_hu') != 'forditas_hu':
            continue
        van_szakaszsor = True
        if r.get('allapot') != 'elavult' and (r.get('forditas_hu') or '').strip():
            ervenyes.setdefault(n, set()).add(r.get('forras_hash', ''))
    kezi_teljes = any(r.get('jelentes_szam') == 'teljes' and r.get('allapot') == 'kezi' for r in sorok)
    megj = 'régi kezi teljes sor (DT-F132c (ii))' if kezi_teljes else ''
    hianyzo = [x['sorszam'] for x in szak if x['sorszam'] not in ervenyes]
    regi_hash = [x['sorszam'] for x in szak if x['sorszam'] in ervenyes and x['hash'] not in ervenyes[x['sorszam']]]
    if not hianyzo and not regi_hash:
        return 'kihagyva', 'kesz', megj
    if not van_szakaszsor:
        return 'forditando', 'nincs_szakaszos', megj
    if regi_hash:
        return 'forditando', 'elavult_hash', '; '.join(x for x in (megj, 'eltérő forras_hash: sz%s' % ','.join(map(str, regi_hash[:10]))) if x)
    return 'forditando', 'hianyos', '; '.join(x for x in (megj, 'hiányzó szakasz: sz%s' % ','.join(map(str, hianyzo[:10]))) if x)


def lista(ts, elof_ut=ELOFORDULASOK_UT, ford_ut=FORDITASOK_UT, tabla=None):
    g = gerinc_strongok(elof_ut)
    fs = thayer_sorok(ford_ut)
    forras = 'thayer_jelolt/szolista.py (fejléc)'
    ki = []
    for sp in sorted(g):
        szak = TB.szakaszok(sp, tabla)
        st, ok, megj = allapot(sp, szak, fs.get(sp, []))
        ki.append({'strong': sp, 'statusz': st, 'ok': ok,
                   'szakasz': str(len(szak)) if szak else '0',
                   'karakter': str(len(TB.nezet(szak))) if szak else '0',
                   'csoport': str(len(TB.csoportok(szak))) if szak else '0',
                   'illesztes': szak[0]['illesztes'] if szak else '',
                   'motivumhely': str(g[sp]), 'megjegyzes': megj,
                   'proveniencia': 'scope=%s | forras=%s | ts=%s' % (sp, forras, ts)})
    return ki


def fajl_szoveg(sorok, ts, tabla=None):
    fej = ['# GENERÁLT: eszkozok/thayer_jelolt/szolista.py --ts %s — az M3 futási listája (DT-F132h); kézzel nem szerkesztendő.' % ts,
           '# forras: adat/elofordulasok.tsv@%s + adat/forditasok.tsv@%s + adat/thayer_szakaszok.tsv@%s'
           % (sha12(ELOFORDULASOK_UT), sha12(FORDITASOK_UT), sha12(tabla or TB.TABLA)),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(r[m] for m in FEJLEC) for r in sorok]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ki')
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    ap.add_argument('--csak-forditando', action='store_true')
    a = ap.parse_args()
    sorok = lista(a.ts)
    c = collections.Counter((r['statusz'], r['ok']) for r in sorok)
    if a.csak_forditando:
        sorok = [r for r in sorok if r['statusz'] == 'forditando']
    szoveg = fajl_szoveg(sorok, a.ts)
    if a.ki:
        with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('irva: %s' % a.ki)
    else:
        sys.stdout.write(szoveg)
    print('# összesítő: %s' % ', '.join('%s/%s %d' % (s, o, n) for (s, o), n in sorted(c.items())), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
