"""Az Ez 37 mostani tartalma a szerver saját lapelőállítójával (oldalak.OldalGyar), szerver nélkül, csak olvasva.
WSL-venvben fut: a kimenet egy JSON a scratchpadban."""
import sys, os, json, re, inspect

SZ = '/mnt/c/Users/bases/Desktop/Bible-Study/eszkozok/olvaso_szerver'
sys.path.insert(0, SZ)
os.chdir(SZ)
import adatbazis, hozzaferes, oldalak  # noqa: E402

DB = os.path.expanduser('~/pardes/pardes.db')
KI = sys.argv[1]
SLUG, FEJ = 'Ez', 37

hozz = hozzaferes.Hozzaferes.betolt()
gyar = oldalak.OldalGyar(adatbazis.Adatbazis(DB, 'belso'), hozz)
print('szint-alap', hozz.szint(), '| szintek', getattr(hozz, 'szintek', None))
print('vers_fragment', inspect.signature(gyar.vers_fragment), '| szo_fragment', inspect.signature(gyar.szo_fragment))
szintek = getattr(hozz, 'szintek', None) or []
szint = len(szintek) - 1 if szintek else hozz.szint()   # a legmagasabb (kutató) szint sorszáma
print('használt szint', szint)

fej_html = gyar.fejezet_lap(SLUG, FEJ, None, oldalak.ALAP_NEZET, szint, '', '', '/%s/%d' % (SLUG, FEJ))
kk = gyar.kozos.slug_kk[SLUG]
nv = dict(gyar.kozos.fejezet_szam[kk])[FEJ] if isinstance(gyar.kozos.fejezet_szam[kk], list) else None
versek = {}
v = 1
while True:
    try:
        versek[v] = gyar.vers_fragment(SLUG, FEJ, v, szint)
    except oldalak.NemTalalhato:
        break
    v += 1
strongok = sorted(set(re.findall(r'/szo/([HG]\d{4,5}[a-zA-Z]?)', fej_html + ''.join(versek.values()))))
szavak = {}
for s in strongok:
    try:
        szavak[s] = gyar.szo_fragment(s, szint)
    except oldalak.NemTalalhato:
        pass
css = open(os.path.join(SZ, 'statikus', 'olvaso.css'), encoding='utf-8').read()
json.dump({'fejezet': fej_html, 'versek': versek, 'szavak': szavak, 'arculat_css': gyar.arculat.css, 'olvaso_css': css,
           'szint': str(szint)}, open(KI, 'w', encoding='utf-8'), ensure_ascii=False)
print('versek', len(versek), 'szavak', len(szavak), 'fejezet', len(fej_html),
      'vers össz', sum(map(len, versek.values())), 'szó össz', sum(map(len, szavak.values())))
