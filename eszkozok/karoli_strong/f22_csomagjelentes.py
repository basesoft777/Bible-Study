#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 22.9 — a csomag-összesítő táblák (könyvenként költség, kapuhiba, `[nem TR]`, régi arany) és az újravetítés.

Olvas: f22/api_termeles/futasnaplo.tsv, naplok/F22_<könyv>_jelentes.md (a f22_konyvjelentes.py kimenete),
adat/karoli_strong/nem_tr_parositott.tsv, f22/minta_<könyv>.tsv; api_koteg.PLAFON_USD. Nem hív hálózatot.

Használat:
    python eszkozok/karoli_strong/f22_csomagjelentes.py --csomag D --konyv Mt --konyv Mk [--hatralevo 3123]
"""

import argparse
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

_ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ITT)
import api_koteg  # noqa: E402
import f22_konyvjelentes as kj  # noqa: E402
import sonnet_koteg  # noqa: E402
import tokenek  # noqa: E402

ROOT = tokenek.ROOT


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--csomag', required=True)
    ap.add_argument('--konyv', action='append', required=True)
    ap.add_argument('--hatralevo', type=int, default=0, help='a hátralevő versek száma az újravetítéshez')
    a = ap.parse_args()
    log_all = kj.tsv(os.path.join(ROOT, 'f22', 'api_termeles', 'futasnaplo.tsv'))
    sor = []
    tot = dict(vers=0, hivas=0, ko=0.0, kapu=0, javito=0, jsonh=0, nemtr=0, nemtrp=0)
    print('| könyv | Károli-vers | hívás | költség (USD) | USD/vers | kapuhiba 1. próba | javító körös köteg | ebből egész köteg formátumhiba | `[nem TR]` | ebből párosított | régi arany |')
    print('|---|---|---|---|---|---|---|---|---|---|---|')
    for k in a.konyv:
        n = sonnet_koteg.ascii_nev(k)
        vers = len(kj.tsv(os.path.join(ROOT, 'f22', 'minta_%s.tsv' % n)))
        log = [r for r in log_all if r['futas'] == 'api_termeles/high/%s' % n]
        ko = sum(float(r['koltseg_usd'] or 0) for r in log)
        javito = len({int(r['koteg']) for r in log if r['probalkozas'] == '2'})
        jel = open(os.path.join(ROOT, 'naplok', 'F22_%s_jelentes.md' % n), encoding='utf-8').read()
        kapu = int(re.search(r'kapuhiba első próbára [\d.]+% \((\d+)/', jel).group(1))
        jh = int(re.search(r'formátumhiba \(érvénytelen JSON[^|]*\| (\d+)', jel).group(1))
        nt = int(re.search(r'`\[nem TR\]` tokenek: (\d+), ebből (\d+)', jel).group(1))
        ntp = int(re.search(r'`\[nem TR\]` tokenek: (\d+), ebből (\d+)', jel).group(2))
        arany = re.search(r'Mért érték \(kizárás nélkül, minden link\):\*\* ((?:[\d.]+%|n\.é\.) \(\d+/\d+\))', jel).group(1)
        print('| %s | %d | %d | %.4f | %.5f | %d/%d | %d | %d | %d | %d | %s |' % (k, vers, len(log), ko, ko / vers, kapu, vers, javito, jh, nt, ntp, arany))
        tot['vers'] += vers; tot['hivas'] += len(log); tot['ko'] += ko; tot['kapu'] += kapu; tot['javito'] += javito; tot['jsonh'] += jh; tot['nemtr'] += nt; tot['nemtrp'] += ntp
    print('| **össz** | **%d** | **%d** | **%.4f** | **%.5f** | **%d/%d** | **%d** | **%d** | **%d** | **%d** | |' % (
        tot['vers'], tot['hivas'], tot['ko'], tot['ko'] / tot['vers'], tot['kapu'], tot['vers'], tot['javito'], tot['jsonh'], tot['nemtr'], tot['nemtrp']))
    futo = float(log_all[-1]['futo_osszeg_usd'])
    print('\nCSOMAG %s: költség %.4f USD; futó összeg %.4f USD; plafon %.2f USD; maradék %.4f USD' % (a.csomag, tot['ko'], futo, api_koteg.PLAFON_USD, api_koteg.PLAFON_USD - futo))
    if a.hatralevo:
        egyseg = tot['ko'] / tot['vers']
        v = a.hatralevo * egyseg
        print('újravetítés: %d vers × %.5f = %.2f USD; ×1,2 = %.2f USD; belefér a maradékba: %s' % (
            a.hatralevo, egyseg, v, v * 1.2, 'igen' if v * 1.2 <= api_koteg.PLAFON_USD - futo else 'NEM'))


if __name__ == '__main__':
    main()
