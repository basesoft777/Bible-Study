"""F213 füstpróba a bekötési audithoz: a fordítást kapott blokkok néhány lapon (WSL, natív pardes.db); a HTML a megadott könyvtárba."""
import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eszkozok', 'olvaso_szerver')
sys.path.insert(0, D)
import adatbazis  # noqa: E402
import hozzaferes  # noqa: E402
import oldalak  # noqa: E402
ki = sys.argv[1]
os.makedirs(ki, exist_ok=True)
h = hozzaferes.Hozzaferes.betolt(os.path.join(D, 'konfig'))
gyar = oldalak.OldalGyar(adatbazis.Adatbazis(os.environ.get('PARDES_DB') or os.path.expanduser('~/pardes/pardes.db'), 'belso'), h)
szint = h.rang[h.alap_szint]
for s in ('G0086', 'G1941', 'G1311', 'H7585', 'H0127', 'H0056'):
    open(os.path.join(ki, 'a_%s.html' % s), 'w', encoding='utf-8').write(gyar.szo_fragment(s, szint))
for nev, args in (('Zak_8_21', ('Zak', 8, 21)), ('Mt_4_1', ('Mt', 4, 1))):
    open(os.path.join(ki, 'v_%s.html' % nev), 'w', encoding='utf-8').write(gyar.vers_fragment(args[0], args[1], args[2], szint, 'temak'))
print('ok')
