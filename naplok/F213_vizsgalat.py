"""F213 vizsgálat: a H0068 BDB-alapjelentése és a H0216 6. jelentésének LXX-párja a szerver útján (WSL, natív pardes.db)."""
import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eszkozok', 'olvaso_szerver')
sys.path.insert(0, D)
import adatbazis  # noqa: E402
import blokkok  # noqa: E402
import bdb_szokartya  # noqa: E402
import oldalak  # noqa: E402
con = adatbazis.Adatbazis(os.environ.get('PARDES_DB') or os.path.expanduser('~/pardes/pardes.db'), 'belso').kapcsolat()
kozos = oldalak.Kozos(con)
K = oldalak.Kontekst(con, kozos, strong='H0068')
b = blokkok._bdb_bontas(K)
print('H0068 appar alap:', repr((b['appar'].get('alap') or '')[:200]))
print('nemi tanú nélkül:', repr(bdb_szokartya.alap_nemi_tanu(b['appar'].get('alap'))[:200]))
print('_alap_jelentes:', blokkok._alap_jelentes(bdb_szokartya.alap_nemi_tanu(b['appar'].get('alap'))))
K = oldalak.Kontekst(con, kozos, strong='H0216')
d = blokkok._f_bdb_apparatus(K)
vj = blokkok.VersJelolo(d['appar'], d['vj_sorok'], None, kozos.slug, {})
sorok = vj.csomopont_sorok.get('bdb-0-6', [])
print('H0216 6. sorai:', [(r['karoli_vers'], r['vers_feloldas'], r['okkod'], r['szurt'], blokkok._vj_feloldott(r)) for r in sorok])
for r in sorok:
    print('  ', r['karoli_vers'], d['lxx'].get(r['karoli_vers']))
print('Jób 41 kulcsok:', [k for k in d['lxx'] if k.startswith('Jób 41')])
