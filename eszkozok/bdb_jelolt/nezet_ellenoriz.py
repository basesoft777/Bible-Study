#!/usr/bin/env python
"""A szakasztáblából generált sima szöveg (nézet) összevetése a BDB_teljes_unabridged.tsv-vel (F107, 3. lépés).

A nézet Strongonként: a sorok `jel` + ' ' + `szoveg` mezője, egy szóközzel összefűzve, whitespace-normalizálva (a
javítótábla javításai NEM alkalmazódnak: a nyers szöveg nézete, SEMA 2.30). Mindhárom szöveg whitespace-normalizálva.

Osztályok (Strongonként, az első illeszkedő):
  azonos        nézet == TSV
  sub           a TSV a JSON változatlan konverziója, és a nézet a JSON <sub> nélküli tisztításával pontosan egyezik: az
                eltérés csak a <sub> (a _convert_bdb.py `_N`-je; a táblában a `gyakorisag` oszlop) — szoveg_konverzio
  tsv_utolagos  a TSV eltér a JSON _convert_bdb.py-újrakonvertált alakjától (a TSV utólag javított sora, F34/F46), és a
                nézet a JSON-nal egyezik (`+szokoz`: csak szóközben tér el)
  szokoz        csak szóközben tér el (a JSON <sub> nélküli tisztításához mérve): a táblában a `jel` és a `szoveg`
                közötti forrás-szóköz nincs rögzítve, a nézet mindig egy szóközzel fűz (tapadt fej: „a.-1”, „Pi`el3masculine”;
                vagy hamis fej a bekezdéshatár után: „below 3);”) — tabla_hiba-jelölt a 4. lépés osztályozásához
  forras_html   a nézetben nyers jelölés-töredék áll (a JSON hibás HTML-je, l. a kódot) — forras_hiba / tabla_hiba
  egyeb         ismeretlen okú eltérés (az első eltérő pozícióval)

A TSV-ben JSON-kulcs nélküli 9 sor (F57/F72) `nincs_a_tablaban`.
Csak olvas. Kimenet: összefoglaló a stdout-ra, `--lista N`: az első N nem `azonos` Strong.
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import forras_osszevetes  # noqa: E402  (a _convert_bdb.py strip_html()-jének másolata)
import bont  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(ITT))
TSV = os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')
TABLA = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')


JELOLES_TOREDEK = re.compile(r'href=|class=|<a |<font|<e |</|<p')


def ws(t):
    return re.sub(r'\s+', ' ', t).strip()


def nezetek():
    with open(TABLA, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    fej = sorok[2].split('\t')
    ki = collections.OrderedDict()
    for s in sorok[3:]:
        if not s:
            continue
        d = dict(zip(fej, s.split('\t')))
        ki.setdefault(d['strong'], []).append(' '.join(x for x in (d['jel'], d['szoveg']) if x))
    return {k: ws(' '.join(v)) for k, v in ki.items()}


def elso_elteres(a, b):
    n = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    return n, a[max(0, n - 30):n + 40], b[max(0, n - 30):n + 40]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lista', type=int, default=0)
    a = ap.parse_args()
    nez = nezetek()
    with open(bont.JSON_UT, encoding='utf-8') as f:
        ujra, sima = {}, {}
        for item in json.load(f):
            m = re.match(r'^H(\d+)', item.get('top', ''))
            if m:
                pad = 'H%04d' % int(m.group(1)) + item['top'][len(m.group(0)):]
                ujra[pad] = ws(forras_osszevetes.strip_html_142ad625(item.get('def', '')))
                # a tábla tisztítása az egész szócikkre: mint a _convert_bdb.py, de a <sub> kimarad
                sima[pad] = ws(bont.sima(item.get('def', '')))
    with open(TSV, encoding='utf-8', newline='') as f:
        tsv = [s.split('\t') for s in f.read().split('\n')[1:] if s]
    stat, reszlet = collections.Counter(), []
    for s in tsv:
        k, t = s[0], ws(s[2])
        if k not in nez:
            stat['nincs_a_tablaban'] += 1
            reszlet.append((k, 'nincs_a_tablaban', ''))
            continue
        v = nez[k]
        if v == t:
            stat['azonos'] += 1
            continue
        r, s0 = ujra[k], sima[k]
        # a nézet és a nyers JSON (a <sub> nélkül) viszonya
        if v == s0:
            alap = 'pontos'
        elif re.sub(r'\s', '', v) == re.sub(r'\s', '', s0):
            alap = 'szokoz'
        else:
            alap = 'egyeb'
        if alap == 'egyeb' and JELOLES_TOREDEK.search(v):
            # a JSON hibás HTML-je (töredékes <a href=…>, <e …> tag, benne <p>): a bekezdés-bontás a töredéket nyers
            # jelölésként a szövegbe engedi, az egész szócikkre futó tisztítás nem (H1980, H3117, H4639, H4714, H8104)
            oszt = 'forras_html'
        elif alap == 'egyeb':
            oszt = 'egyeb'
        elif t != r:
            oszt = 'tsv_utolagos' + ('' if alap == 'pontos' else '+szokoz')
        elif alap == 'szokoz':
            oszt = 'szokoz'
        else:
            oszt = 'sub'
        stat[oszt] += 1
        if oszt == 'sub':
            reszlet.append((k, oszt, '%d <sub>' % (len(r) - len(s0))))
        elif oszt.startswith('tsv_utolagos'):
            n, x, y = elso_elteres(t, r)
            reszlet.append((k, oszt, 'TSV «%s» | JSON «%s»' % (x, y)))
        else:
            n, x, y = elso_elteres(v, s0)
            reszlet.append((k, oszt, 'poz %d: nézet «%s» | JSON «%s»' % (n, x, y)))
    print('TSV-sor: %d; %s' % (len(tsv), dict(stat)))
    for k, o, r in reszlet[:a.lista]:
        print('  %s\t%s\t%s' % (k, o, r))
    print('proveniencia: scope=F107 3. lépés, nézet ↔ BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_jelolt/nezet_ellenoriz.py | ts=%s'
          % datetime.date.today().isoformat())
    return 0


if __name__ == '__main__':
    sys.exit(main())
