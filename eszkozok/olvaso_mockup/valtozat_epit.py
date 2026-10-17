"""Az alap olvasófelület-mockup és a nyolc változat építése: közös, tömörített Ez 37-adat + változatonként CSS/JS és fejléc-sáv."""
import sys, os, json, re, gzip, base64, html
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
d = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(d, 'valt')
E = json.load(open(os.path.join(d, 'ez37.json'), encoding='utf-8'))
N = json.load(open(os.path.join(d, 'nav.json'), encoding='utf-8'))
VA = json.load(open(os.path.join(d, 'vadat.json'), encoding='utf-8'))
LINK = json.load(open(os.path.join(V, 'linkek.json'), encoding='utf-8')) if os.path.exists(os.path.join(V, 'linkek.json')) else {}
f = E['fejezet']

def kivag(minta):
    m = re.search(minta, f, re.S)
    if not m:
        raise SystemExit('nincs meg: ' + minta)
    return m.group(0)
def szoveg(x):
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x))).strip()

versszoveg = {}
for v, hh in E['versek'].items():
    m = re.search(r'<p class="karoli-szoveg"[^>]*>(.*?)</p>', hh, re.S)
    versszoveg[v] = szoveg(m.group(1)) if m else ''
szoindex = {}
for s, hh in E['szavak'].items():
    c = re.search(r'<h2 class="szocim">(.*?)</h2>', hh, re.S)
    a = re.search(r'<p class="alapjel"[^>]*>(.*?)</p>', hh, re.S)
    szoindex[s] = [szoveg(c.group(1)) if c else s, szoveg(a.group(1)).replace('Alapjelentés', '').strip() if a else '']
adat = {'folyo': kivag(r'<p class="folyo" id="szoveg">.*?</p>\s*(?=</section>)'), 'cimkek': kivag(r'<div class="cimkek" id="cimkek">.*?</div>'),
        'utmutato': kivag(r'<details class="utmutato" id="utmutato".*?</details>'), 'jegy': kivag(r'<div class="szoveg-jegy">.*?</div>'),
        'cim': szoveg(kivag(r'<h1>.*?</h1>')), 'versek': E['versek'], 'szavak': E['szavak'], 'versszoveg': versszoveg,
        'szoindex': szoindex, 'olvaso_css': E['olvaso_css']}
B64 = base64.b64encode(gzip.compress(json.dumps(adat, ensure_ascii=False).encode('utf-8'), 9)).decode('ascii')
ARCULAT = E['arculat_css'].replace('data-tema=', 'data-theme=')
KICSI = json.dumps({'konyvek': N['konyvek'], 'motivumok': N['motivumok'], 'konyv': 'Ez', 'fej': 37, 'szint': E['szint']}, ensure_ascii=False).replace('</', '<\\/')
SABLON = open(os.path.join(d, 'nav2_sablon.html'), encoding='utf-8').read()

VALT = [
    ('v1', 'Előfordulások kiemelése', 'Egy szóra kattintva a fejezet összes azonos Strong-számú szava kiemelődik; egy sáv mutatja a számot és a versek számát, előző/következő gombokkal; a jobb szélen a fejezet-sáv jelzi, hol állnak.', 'Accordance, STEPBible', 'Kattints az 1. versben a „lélek” szóra.', {}),
    ('v2', 'Kereszthivatkozás-előnézet', 'A hivatkozott vers szövege rámutatásra megjelenik, kattintásra rögzül; a Kereszthiv. fülön egy gombbal minden célvers szövege kibontható a lista alatt (272 célvers beágyazva).', 'Logos, Olive Tree', 'Jelölj ki egy verset, nyisd a Kereszthiv. fület, és vidd az egeret egy hivatkozásra.', {'kh': VA['kh']}),
    ('v3', 'Interlineáris sor', 'A Károli-szavak alatt a héber szó és a magyar BDB-alapjelentés első tagja, külön nézet nélkül; a jelölő-sávban kapcsolható.', 'Logos reverse interlinear', 'Görgess a szövegben; a jelölő-sávban az „interlineáris sor” kapcsoló.', {}),
    ('v4', 'Szövegbeállítások', 'Új „Aa” gomb a fejlécben: betűméret, sorköz, betűcsalád, sorszélesség, versszámok, folyó szöveg vagy versenként új sor; a választás a böngészőben megmarad.', 'YouVersion, Olive Tree', 'Kattints a fejlécben az „Aa” gombra.', {}),
    ('v5', 'Fejezet-kalauz', 'A szöveg fölött egy kinyitható kalauz: kulcsszavak, személyek és helyek, témák, motívumok, a kereszthivatkozások célkönyvei, a szerver mostani blokkjaiból összesítve.', 'Logos Passage Guide', 'A kalauz a cím alatt van; a sorok kattinthatók.', {}),
    ('v6', 'Vers-elemző táblázat', 'Új „Elemzés” fül: a vers minden szava egy sorban (Károli, héber és kiejtés, Strong, magyar BDB-alapjelentés, igealak, pár-bizonyosság); ez a nyitó fül.', 'Logos Exegetical Guide', 'Kattints egy versre; a panel az Elemzés fület mutatja.', {}),
    ('v7', 'Személy- és helykártya', 'A tulajdonnevek a szövegben jelölve (◆); rájuk kattintva névkártya: TIPNR-névalak, versek száma a Bibliában, első említés, leggyakoribb könyvek, és hol áll a fejezetben.', 'Logos Factbook, TIPNR', 'Kattints a 16. versben az „Izráel” vagy „József” szóra.', {'tipnr': VA['tipnr']}),
    ('v8', 'Párhuzamos oszlopok', 'A szövegoszlop helyén táblázat: versenként Károli, héber, LXX, BSB és KJV egymás mellett; az oszlopok és a jobb panel ki-be kapcsolhatók.', 'Bible Gateway, Accordance', 'A „jobb panel” kapcsolóval szélesebb a táblázat.', {}),
]

CIMEK = {'v1': 'Előfordulás-kiemelő olvasó', 'v2': 'Hivatkozás-előnézetes olvasó', 'v3': 'Interlineáris olvasó', 'v4': 'Állítható szövegű olvasó',
         'v5': 'Fejezet-kalauzos olvasó', 'v6': 'Vers-elemző olvasó', 'v7': 'Névkártyás olvasó', 'v8': 'Párhuzamos olvasó'}

def fajl(n, ut):
    p = os.path.join(V, n + ut)
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''

def linksor(akt):
    r = ['<a href="%s">Alap mockup</a>' % LINK['alap'] if 'alap' in LINK and akt != 'alap' else '<b>Alap mockup</b>' if akt == 'alap' else 'Alap mockup']
    for i, (k, c, *_) in enumerate(VALT, 1):
        t = '%d. %s' % (i, c)
        r.append('<b>%s</b>' % t if k == akt else ('<a href="%s">%s</a>' % (LINK[k], t) if k in LINK else t))
    return '<div class="vlinkek"><span>Változatok:</span> ' + ' · '.join(r) + '</div>'

def epit(kulcs, cim, sav, vcss, vjs, vshadow, vadat, kimenet):
    t = SABLON
    for k, v in (('__ARCULAT__', ARCULAT), ('__KICSI__', KICSI), ('__GZ__', B64), ('__VCSS__', vcss), ('__VSAV__', sav), ('__VHTML__', ''),
                 ('__VADAT__', json.dumps(vadat, ensure_ascii=False).replace('</', '<\\/')), ('__VSHADOW__', json.dumps(vshadow, ensure_ascii=False).replace('</', '<\\/')),
                 ('__VJS__', vjs)):
        assert t.count(k) == 1, k
        t = t.replace(k, v)
    if cim:
        t = t.replace('<title>Olvasófelület-mockup</title>', '<title>%s</title>' % cim, 1)
    open(os.path.join(d, kimenet), 'w', encoding='utf-8').write(t)
    return len(t.encode('utf-8'))

# a szövegbeállítások (a 4. változatból) minden lap alapjának része
V4 = ('const V4_ALAP = true;\n' + fajl('v4', '.js'), fajl('v4', '.css'), fajl('v4', '.shadow.css'))
alap_sav = ('<div class="vsav"><div class="in gut"><div><b>Alap mockup</b> · az olvasófelület új alapja az Ez 37 mostani teljes tartalmával, '
            'a szövegbeállításokkal (Aa) és a szélesebb jobb panellel. A változatok mindegyike ehhez képest egy-egy újdonságot mutat.</div>%s</div></div>' % linksor('alap'))
print('alap', epit('alap', None, alap_sav, V4[1], V4[0], V4[2], None, 'olvasofelulet_mockup.html'))
for i, (k, c, uj, ihlet, probald, vadat) in enumerate(VALT, 1):
    megj = (' A szövegbeállítások azóta minden mockupban benne vannak; ez a változat mutatta be őket.' if k == 'v4' else '')
    sav = ('<div class="vsav"><div class="in gut"><div><span class="uj">%d/8</span> <b>%s</b> · <b>Az alap mockuphoz képest új:</b> %s%s '
           '<span style="color:var(--muted)">Ihlet: %s. Próbáld ki: %s Az új elemeket <span class="uj">ÚJ</span> jelzi.</span></div>%s</div></div>'
           % (i, html.escape(c), html.escape(uj), html.escape(megj), html.escape(ihlet), html.escape(probald), linksor(k)))
    if k == 'v4':
        css, js, sh = fajl(k, '.css'), fajl(k, '.js'), fajl(k, '.shadow.css')
    else:
        css, js, sh = V4[1] + '\n' + fajl(k, '.css'), V4[0] + '\n' + fajl(k, '.js'), V4[2] + '\n' + fajl(k, '.shadow.css')
    n = epit(k, CIMEK[k], sav, css, js, sh, vadat or None, 'olvaso_v%d_mockup.html' % i)
    print(k, n)
