"""F213 füstpróba: a szó-lap töredéke néhány szóra a natív pardes.db-vel (WSL); a HTML a megadott könyvtárba kerül.

Futtatás (WSL): PARDES_DB=~/pardes/pardes.db <venv>/bin/python naplok/F213_fustproba.py <kimeneti könyvtár>
"""
import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eszkozok', 'olvaso_szerver')
sys.path.insert(0, D)
import adatbazis  # noqa: E402
import hozzaferes  # noqa: E402
import oldalak  # noqa: E402

ki = sys.argv[1]
os.makedirs(ki, exist_ok=True)
db = os.environ.get('PARDES_DB') or os.path.expanduser('~/pardes/pardes.db')
h = hozzaferes.Hozzaferes.betolt(os.path.join(D, 'konfig'))
gyar = oldalak.OldalGyar(adatbazis.Adatbazis(db, 'belso'), h)
szint = h.rang[h.alap_szint]
for strong, ig in (('H0216', '1Móz 1:3'), ('H0127', None), ('H1242', '1Móz 1:5'), ('H7843', None), ('H6440', None), ('G1941', None),
                   ('H7121', None), ('H1961', None), ('H0776', None), ('H7451', None)):
    t0 = time.time()
    html = gyar.szo_fragment(strong, szint, ig)
    with open(os.path.join(ki, '%s.html' % strong), 'w', encoding='utf-8') as f:
        f.write(html)
    print(strong, ig or '-', len(html), '%.2fs' % (time.time() - t0))
