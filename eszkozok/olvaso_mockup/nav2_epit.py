"""Az olvasófelület-mockup feltöltött változata: a szerver lapelőállítójának Ez 37-kimenete (ez37.json) tömörítve beágyazva."""
import sys, os, json, re, gzip, base64, html
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
d = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(d, 'ez37.json'), encoding='utf-8'))
N = json.load(open(os.path.join(d, 'nav.json'), encoding='utf-8'))
f = E['fejezet']

def kivag(minta):
    m = re.search(minta, f, re.S)
    if not m:
        raise SystemExit('nincs meg: ' + minta)
    return m.group(0)

folyo = kivag(r'<p class="folyo" id="szoveg">.*?</p>\s*(?=</section>)')
cimkek = kivag(r'<div class="cimkek" id="cimkek">.*?</div>')
utmutato = kivag(r'<details class="utmutato" id="utmutato".*?</details>')
jegy = kivag(r'<div class="szoveg-jegy">.*?</div>')
cim = re.sub(r'<[^>]+>', '', kivag(r'<h1>.*?</h1>')).strip()

def szoveg(x):
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x))).strip()

versszoveg = {}
for v, h in E['versek'].items():
    m = re.search(r'<p class="karoli-szoveg"[^>]*>(.*?)</p>', h, re.S)
    versszoveg[v] = szoveg(m.group(1)) if m else ''

szoindex = {}
for s, h in E['szavak'].items():
    c = re.search(r'<h2 class="szocim">(.*?)</h2>', h, re.S)
    a = re.search(r'<p class="alapjel"[^>]*>(.*?)</p>', h, re.S)
    szoindex[s] = [szoveg(c.group(1)) if c else s, szoveg(a.group(1)).replace('Alapjelentés', '').strip() if a else '']

# a token-fájl sötét témája a mockup attribútumára (data-theme) hangolva
arculat = E['arculat_css'].replace('data-tema=', 'data-theme=')
adat = {'folyo': folyo, 'cimkek': cimkek, 'utmutato': utmutato, 'jegy': jegy, 'cim': cim, 'versek': E['versek'],
        'szavak': E['szavak'], 'versszoveg': versszoveg, 'szoindex': szoindex, 'olvaso_css': E['olvaso_css']}
nyers = json.dumps(adat, ensure_ascii=False).encode('utf-8')
gz = gzip.compress(nyers, 9)
b64 = base64.b64encode(gz).decode('ascii')
kicsi = {'konyvek': N['konyvek'], 'motivumok': N['motivumok'], 'konyv': 'Ez', 'fej': 37, 'szint': E['szint']}
t = open(os.path.join(d, 'nav2_sablon.html'), encoding='utf-8').read()
for k, v in (('__ARCULAT__', arculat), ('__KICSI__', json.dumps(kicsi, ensure_ascii=False).replace('</', '<\\/')), ('__GZ__', b64)):
    assert t.count(k) == 1, k
    t = t.replace(k, v)
open(os.path.join(d, 'olvasofelulet_mockup.html'), 'w', encoding='utf-8').write(t)
print('nyers', len(nyers), 'gz', len(gz), 'b64', len(b64), 'lap', len(t.encode('utf-8')))
print('cím', cim, '| versek', len(E['versek']), '| szavak', len(E['szavak']))
