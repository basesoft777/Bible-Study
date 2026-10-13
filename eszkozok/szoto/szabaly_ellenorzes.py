"""F94.1 (FELADATOK #94): a hibrid helyesírási és tőváltó szabályainak korpusz-ellenőrzése a repó Károli–Strong
párosításából (`adat/karoli_strong/szavak_<könyv>.tsv`, `oldal=hu`, SEMA 2.20; modell-kimenet, javaslat). Az előmérés
ugyanezt a `pardes.db` `token_karoli`-jából (csak ÓSZ) számolta; a módszer és a küszöbök változatlanok.
Csak olvas. Kimenet: `adat/szoto/szabaly_ellenorzes.tsv` (generált; szabályonként egy sor) és a jelentés a
standard kimenetre (markdown).
Használat: python eszkozok/szoto/szabaly_ellenorzes.py [--ts …]

Mit mér, szabályonként:
- HELYESÍRÁSI szabály (minta -> csere, pl. setét -> sötét): a Károli minden alakjára, amelyre a szabály illik,
  képezi a cserélt alakot. „Pár” = a régi és a cserélt alak is előfordul a Károliban.
- TŐVÁLTÓ szabály (pl. lelk- -> lélek): a régi család = a tőváltozat + rag/birtokos jel (a hibrid RAG/BIRT listái
  és ezek kombinációi) alakjai; az új család = a szótári alak + ugyanezek. Mindkét család alakjai a Károliból.
- Strong-támasz: a régi alak(család) Strong-hoz párosított tokenjeinek hány %-a hordozza az új alak(család) fő
  Strong-számainak valamelyikét (fő Strong = a család tokenjeinek legalább 10%-át adó, nem grammatikai
  [HG]9xxx Strong). Helyesírási szabálynál párokon, a régi tokenekkel súlyozva.
- Könyv-eloszlás: hány könyvben áll csak a régi, csak az új, és mindkét alak (helyesírási szabálynál a párok
  összesítve). Ha a két alak könyvenként elkülönül, az írásmód-változatra utal; ha egy könyvben együtt áll, az
  sem cáfolja (a Károli 1908 helyesírása nem egységes).

Minősítés (a futtatás ELŐTT rögzítve, 2026-10-13):
- „nincs adat”: nincs Strong-hoz párosított régi token, vagy (helyesírásinál) nincs pár;
- „alátámasztva”: Strong-támasz >= 70%;
- „gyenge”: 30–70%;
- „ellentmond”: < 30%.
Korlát: a közös Strong támasz, nem bizonyíték (ugyanazt a héber/görög szót két külön magyar szó is fordíthatja);
az „alátámasztva” azt jelenti, hogy az adat nem mond ellent, és ugyanazt a forrásszót fordítja."""
import argparse
import collections
import datetime
import glob
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(ITT))
sys.path.insert(0, ITT)
import hibrid  # noqa: E402

_ap = argparse.ArgumentParser()
_ap.add_argument('--ts', default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'))
_ap.add_argument('--kimenet', default=os.path.join(REPO, 'adat', 'szoto', 'szabaly_ellenorzes.tsv'))
ARG = _ap.parse_args()

GRAM = re.compile(r'[HG]9\d\d\d$')
TISZT = re.compile(r'[^\wÁÉÍÓÖŐÚÜŰáéíóöőúüű-]')
SZAVAK = sorted(glob.glob(os.path.join(REPO, 'adat', 'karoli_strong', 'szavak_*.tsv')))


def tokenek():
    for p in SZAVAK:
        for s in open(p, encoding='utf-8').read().split('\n'):
            if not s or s.startswith('#') or s.startswith('vers\t'):
                continue
            m = s.split('\t')
            if m[1] == 'hu':
                yield m[0], m[3], m[6]


# alak (kisbetűs) -> Strong-számláló, könyv-számláló, tokenszám
strong = collections.defaultdict(collections.Counter)
konyv = collections.defaultdict(collections.Counter)
tokn = collections.Counter()
for ig, szo, st in tokenek():
    w = TISZT.sub('', szo or '').lower()
    if not w:
        continue
    tokn[w] += 1
    konyv[w][ig.rsplit(' ', 1)[0]] += 1
    for s in (st or '').split('+'):
        if s and not GRAM.match(s):
            strong[w][s] += 1
formak = set(tokn)


def fo_strongok(alakok):
    o = collections.Counter()
    for a in alakok:
        o.update(strong[a])
    n = sum(o.values())
    return {s for s, k in o.items() if n and k >= 0.1 * n}, o


def tamasz(regi_alakok, uj_fo):
    """A régi alakok Strong-hoz párosított tokenjei közül hány hordoz új-fő Strong-ot (token szinten közelítve:
    alakonként a Strong-számláló alapján)."""
    jo = ossz = 0
    for a in regi_alakok:
        for s, k in strong[a].items():
            ossz += k
            if s in uj_fo:
                jo += k
    return jo, ossz


def konyvek(alakok):
    o = collections.Counter()
    for a in alakok:
        o.update(konyv[a])
    return set(o)


def minosit(jo, ossz, van_par=True):
    if not van_par or ossz == 0:
        return 'nincs adat'
    p = jo / ossz
    return 'alátámasztva' if p >= 0.7 else 'gyenge' if p >= 0.3 else 'ellentmond'


sorok = []
# --- helyesírási szabályok ---
for minta, csere in hibrid.HELYESIRAS:
    parok = []
    for w in formak:
        u = re.sub(minta, csere, w)
        if u != w:
            parok.append((w, u))
    att = [(w, u) for w, u in parok if u in formak]
    jo = ossz = 0
    for w, u in att:
        fo, _ = fo_strongok([u])
        j, o = tamasz([w], fo)
        jo += j
        ossz += o
    kr, ku = konyvek([w for w, _ in att]), konyvek([u for _, u in att])
    pelda = sorted(att, key=lambda p: -tokn[p[0]])[:4]
    sorok.append(dict(
        tipus='helyesírás', szabaly=f'{minta} → {csere}', regi_alak=len(parok), regi_token=sum(tokn[w] for w, _ in parok),
        par=len(att), par_token=sum(tokn[w] for w, _ in att), tamasz=f'{100 * jo / ossz:.0f}% ({jo}/{ossz})' if ossz else '—',
        konyv=f'csak régi {len(kr - ku)}, csak új {len(ku - kr)}, mindkettő {len(kr & ku)}',
        minosites=minosit(jo, ossz, bool(att)),
        pelda='; '.join(f'{w}({tokn[w]})~{u}({tokn[u]})' for w, u in pelda)))

# --- tőváltó szabályok ---
SUF = {''} | set(hibrid.BIRT) | set(hibrid.RAG)
for b in hibrid.BIRT:
    for r in hibrid.RAG:
        SUF.add(b + r)
        SUF.add(hibrid._hosszitas_vissza(b)[:-1] + {'a': 'á', 'e': 'é'}.get(b[-1], b[-1]) + r if b[-1] in 'ae' else b + r)


def csalad(t, kizar=''):
    return {f for f in formak if f.startswith(t) and f[len(t):] in SUF and not (kizar and f.startswith(kizar))}


for tv, lemma in hibrid.TOVALTO.items():
    if tv == lemma:
        continue
    regi = {f for f in csalad(tv) if f[len(tv):] != ''} - csalad(lemma)
    uj = csalad(lemma)
    fo, oszl = fo_strongok(uj)
    jo, ossz = tamasz(regi, fo)
    kr, ku = konyvek(regi), konyvek(uj)
    fo_regi, _ = fo_strongok(regi)
    pelda = sorted(regi, key=lambda a: -tokn[a])[:4]
    sorok.append(dict(
        tipus='tőváltó', szabaly=f'{tv}- → {lemma}', regi_alak=len(regi), regi_token=sum(tokn[a] for a in regi),
        par=len(uj), par_token=sum(tokn[a] for a in uj), tamasz=f'{100 * jo / ossz:.0f}% ({jo}/{ossz})' if ossz else '—',
        konyv=f'csak régi {len(kr - ku)}, csak új {len(ku - kr)}, mindkettő {len(kr & ku)}',
        minosites=minosit(jo, ossz, bool(uj)),
        pelda='; '.join(f'{a}({tokn[a]})' for a in pelda) + f' | fő Strong régi: {",".join(sorted(fo_regi)) or "—"}, új: {",".join(sorted(fo)) or "—"}'))

ts = ARG.ts
_h = hashlib.sha256()
for _p in SZAVAK:
    _h.update(open(_p, 'rb').read())
prov = (f'scope=hibrid.py (sha256:{hashlib.sha256(open(os.path.join(ITT, "hibrid.py"), "rb").read()).hexdigest()[:12]}) '
        f'HELYESIRAS ({len(hibrid.HELYESIRAS)}) + TOVALTO ({sum(1 for k, v in hibrid.TOVALTO.items() if k != v)}) szabályai; '
        f'a párosított Károli-könyvek ({len(SZAVAK)} szavak-fájl, oldal=hu, {sum(tokn.values())} token) | '
        f'forras=adat/karoli_strong/szavak_*.tsv (együttes sha256:{_h.hexdigest()[:12]}; modell-kimenet, javaslat) | ts={ts}')
mezok = ['tipus', 'szabaly', 'regi_alak', 'regi_token', 'par', 'par_token', 'tamasz', 'konyv', 'minosites', 'pelda']
with open(ARG.kimenet, 'w', encoding='utf-8', newline='\n') as f:
    f.write('# GENERÁLT: eszkozok/szoto/szabaly_ellenorzes.py (F94.1) — kézzel nem szerkeszthető | ' + prov + '\n')
    f.write('\t'.join(mezok) + '\n')
    for s in sorok:
        f.write('\t'.join(str(s[m]) for m in mezok) + '\n')

print('# A hibrid szabályainak korpusz-ellenőrzése\n')
print('Helyesírásinál a „pár” oszlop: hány régi alaknak van cserélt párja a Károliban; tőváltónál: az új család alakszáma.\n')
print('| típus | szabály | régi alak / token | pár (alak / token) | Strong-támasz | könyvek | minősítés | példák |')
print('|---|---|---|---|---|---|---|---|')
for s in sorok:
    print(f"| {s['tipus']} | {s['szabaly']} | {s['regi_alak']} / {s['regi_token']} | {s['par']} / {s['par_token']} | {s['tamasz']} | "
          f"{s['konyv']} | {s['minosites']} | {s['pelda']} |")
db = collections.Counter(s['minosites'] for s in sorok)
print('\nÖsszesen: ' + ', '.join(f'{k}: {v}' for k, v in db.most_common()))
print('\n' + prov)
