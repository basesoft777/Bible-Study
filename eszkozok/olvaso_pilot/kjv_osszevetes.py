"""kjv_osszevetes.py -- F60 (#60, értékelő jelentés 8.6): a KJV-szavak kötése Strong-számhoz
az 1Móz 1–25-ben és a Zsolt 22-ben, a Károli-szavak mérésével (meres.py 1. pont) összevethető bontásban.

Kategóriák: tartalmas Strong (nem nyelvtani), nyelvtani Strong (adat/grammatikai_strongok.tsv),
címke nélkül (köztük a dőlt, \\add jelölésű fordítói betoldások). A lábjegyzet (\\f) és a
kereszthivatkozás (\\x) nem számít; a költői sorokra tört verseket a \\v-től a következő \\v-ig gyűjti.

A teljes KJV-szöveg nincs a repóban (a KJV_Strongs_teljes.tsv csak a címkézett szavakat tartja),
ezért a bemenet az eBible USFM-csomagja, a repón kívül kibontva:
    https://ebible.org/Scriptures/eng-kjv_usfm.zip
Futtatás:
    python eszkozok/olvaso_pilot/kjv_osszevetes.py <kibontott usfm-mappa> <eng-kjv_usfm.zip>
Csak olvas; a kimenet a konzol (proveniencia-sorral).
"""
import os
import sys, re, datetime, hashlib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

USFM = sys.argv[1]          # a kibontott usfm-mappa
ZIP = sys.argv[2]
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/') + '/'

gramm = set()
for l in open(R + 'adat/grammatikai_strongok.tsv', encoding='utf-8'):
    if l.startswith('#'):
        continue
    m = re.match(r'^([HG])0*(\d+)', l.split('\t')[0])
    if m:
        gramm.add(m.group(1) + m.group(2).zfill(4))

SZO = re.compile(r"[A-Za-z][A-Za-z'’]*")
W = re.compile(r'\\w\s+([^|\\]*?)\|strong="([^"]+)"\s*\\w\*')
MARKER = re.compile(r'\\[a-z0-9]+\*?')


DOLT = {'n': 0}   # a KJV dőlt (\add, a fordító által hozzáadott) szavai; a „címke nélkül” részei


def norm(s):
    m = re.match(r'^([HG])0*(\d+)', s)
    return m.group(1) + m.group(2).zfill(4) if m else ''


def szamol(szoveg, st):
    """Egy vers (vagy felirat) szövegének tokenjei kategóriánként."""
    for a in re.findall(r'\\add\s(.*?)\\add\*', szoveg):
        DOLT['n'] += len(SZO.findall(MARKER.sub(' ', a)))
    poz = 0
    for m in W.finditer(szoveg):
        elotte = MARKER.sub(' ', szoveg[poz:m.start()])
        st['nincs'] += len(SZO.findall(elotte))
        n = len(SZO.findall(m.group(1)))
        strongok = [norm(x) for x in re.split(r'[\s,]+', m.group(2)) if norm(x)]
        if strongok and all(s in gramm for s in strongok):
            st['gramm'] += n
        else:
            st['tartalmas'] += n
        poz = m.end()
    st['nincs'] += len(SZO.findall(MARKER.sub(' ', szoveg[poz:])))


JEGYZET = re.compile(r'\\(f|x)\s.*?\\\1\*')   # lábjegyzet és kereszthivatkozás: nem a bibliaszöveg része


def feldolgoz(fajl, fejezetek, felirattal):
    """A verseket a \\v-től a következő \\v/\\c-ig gyűjti (a költői sorok több sorba törnek)."""
    st = {'tartalmas': 0, 'gramm': 0, 'nincs': 0}
    felirat = {'tartalmas': 0, 'gramm': 0, 'nincs': 0}
    fej = None
    versek = 0
    puffer = []

    def zar():
        if puffer:
            szamol(JEGYZET.sub(' ', ' '.join(puffer)), st)
            puffer.clear()

    for sor in open(fajl, encoding='utf-8'):
        sor = sor.rstrip('\n')
        m = re.match(r'\\c\s+(\d+)', sor)
        if m:
            zar()
            fej = int(m.group(1))
            continue
        if fej not in fejezetek:
            continue
        if sor.startswith('\\d'):
            zar()
            if felirattal:
                szamol(JEGYZET.sub(' ', sor[2:]), felirat)
            continue
        m = re.match(r'\\v\s+\d+\s?(.*)', sor)
        if m:
            zar()
            versek += 1
            puffer.append(m.group(1))
            continue
        if puffer:
            puffer.append(re.sub(r'^\\(q\d?|p|m|b|nb|pi\d?)\s*', ' ', sor))
    zar()
    return st, felirat, versek


def kiir(nev, st, versek):
    ossz = sum(st.values())
    print(f"{nev}: {versek} vers, {ossz} szó | tartalmas Strong {st['tartalmas']} ({100*st['tartalmas']/ossz:.1f}%) | "
          f"nyelvtani Strong {st['gramm']} ({100*st['gramm']/ossz:.1f}%) | címke nélkül {st['nincs']} ({100*st['nincs']/ossz:.1f}%)")


sha = hashlib.sha256(open(ZIP, 'rb').read()).hexdigest()
ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
g, _, gv = feldolgoz(USFM + '/02-GENeng-kjv.usfm', set(range(1, 26)), False)
kiir('1Móz 1–25 (KJV)', g, gv)
print(f"  ebből dőlt (\\add) szó: {DOLT['n']}")
DOLT['n'] = 0
z, zf, zv = feldolgoz(USFM + '/20-PSAeng-kjv.usfm', {22}, True)
kiir('Zsolt 22 (KJV, felirat nélkül)', z, zv)
print(f"  ebből dőlt (\\add) szó (a felirattal): {DOLT['n']}")
osszes = {k: z[k] + zf[k] for k in z}
kiir('Zsolt 22 (KJV, a felirattal együtt)', osszes, zv)
print(f'nyelvtani Strong-halmaz: {len(gramm)} elem (adat/grammatikai_strongok.tsv)')
print(f'scope=1Móz 1–25 + Zsolt 22, KJV-szavak (betűtoken) | forras=eBible eng-kjv_usfm.zip sha256={sha} + adat/grammatikai_strongok.tsv | ts={ts}')
