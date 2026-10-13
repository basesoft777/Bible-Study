"""F94.3 (FELADATOK #94): M2 — keresési találati arány a minta lemmáin, a pooled definícióval (az előmérés
újradefiniált M2-je, napló 2.3; a #94-ben emMorph nélkül).

Tokenek: a repó Károli–Strong párosítása (`adat/karoli_strong/szavak_<könyv>.tsv`, `oldal=hu`; a `betoldas` token Strong
nélküli). A minta minden sorának lemmája L = {szotari_alak, szotari_alak_mai} (kisbetűsen; a sorok szótári alak szerint
összevonva).
- **Pooled célhalmaz:** azok a tokenek, amelyek alakját **bármelyik** elemző (a hibrid A, C, CK változata és a
  simplemma) L-re vezeti, ÉS a token a lemma fő Strong-jához párosított, vagy Strong nélküli. A **fő Strong**: a
  pooled-jelölt tokenek leggyakoribb nem grammatikai Strongja ([HG]9xxx kizárva); ha nincs, a célhalmaz a Strong
  nélküli jelölt tokenek.
- Elemzőnként (A, C, CK): **(a)** a célhalmaz tokenjeinek hány %-át vezeti az elemző L-re; **(b)** … vagy az alak
  maga L; **(c)** … vagy a token a fő Strong-hoz párosított.
Kiírás: token-súlyozva és lemmánkénti átlagként, a minta minden lemmáján, és a K tábla alakjai nélküli lemmákon
(a DT-F94c döntő halmaza, l. napló 13.3).

Használat: python eszkozok/szoto/meres_m2.py --minta adat/szoto/szoto_minta_4_fuggetlen.tsv [--csak-felhasznalo]"""
import argparse
import collections
import datetime
import glob
import hashlib
import os
import platform
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

try:
    import simplemma
except ImportError:
    simplemma = None

GRAM = re.compile(r'^[HG]9\d\d\d$')
TISZT = re.compile(r'[^\wÁÉÍÓÖŐÚÜŰáéíóöőúüű-]')
VALTOZATOK = ('A', 'C', 'CK')


def sha(p, n=12):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:n]


def tokenek():
    """(alak, Strong-halmaz) tokenenként; a Strong-halmaz üres a Strong nélküli (betoldás) tokennél."""
    ki, h = [], hashlib.sha256()
    for p in sorted(glob.glob(os.path.join(REPO, 'adat', 'karoli_strong', 'szavak_*.tsv'))):
        b = open(p, 'rb').read()
        h.update(b)
        for s in b.decode('utf-8').split('\n'):
            if not s or s.startswith('#') or s.startswith('vers\t'):
                continue
            m = s.split('\t')
            if m[1] != 'hu':
                continue
            w = TISZT.sub('', m[3])
            if w and not w[:1].isdigit():
                ki.append((w, frozenset(x for x in m[6].split('+') if x)))
    return ki, h.hexdigest()[:12]


def minta_lemmak(p, csak_felhasznalo):
    sorok = [s for s in open(p, encoding='utf-8').read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    lem = collections.OrderedDict()
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        if csak_felhasznalo and r['ellenorzes'] != 'felhasznalo':
            continue
        kulcs = r['szotari_alak'].lower()
        e = lem.setdefault(kulcs, dict(L={r['szotari_alak'].lower(), r['szotari_alak_mai'].lower()}, k=False, alakok=[]))
        e['L'] |= {r['szotari_alak'].lower(), r['szotari_alak_mai'].lower()}
        e['alakok'].append(r['alak'])
        e['k'] = e['k'] or r['alak'].lower() in hibrid.K
    return lem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--minta', required=True)
    ap.add_argument('--csak-felhasznalo', action='store_true')
    a = ap.parse_args()
    if simplemma is None:
        sys.exit('HIBA: a pooled célhalmazhoz a simplemma is kell (A változat és a simplemma önmagában)')
    tok, htok = tokenek()
    formak = sorted({w for w, _ in tok})
    kimenet = {v: {} for v in VALTOZATOK}
    for v in VALTOZATOK:
        hibrid.valtozat(v)
        for w in formak:
            kimenet[v][w] = hibrid.to(w).lower()
    kimenet['simplemma'] = {w: simplemma.lemmatize(w, lang='hu').lower() for w in formak}
    lemmak = minta_lemmak(a.minta, a.csak_felhasznalo)
    # index: alak -> Strong-halmazok előfordulásszámmal; elemzői kimenet -> alakok
    alak_st = collections.defaultdict(collections.Counter)
    for w, st in tok:
        alak_st[w][st] += 1
    kimenet_alak = collections.defaultdict(set)
    for x in kimenet:
        for w, t in kimenet[x].items():
            kimenet_alak[t].add(w)
    eredm = {}
    for kulcs, e in lemmak.items():
        L = e['L']
        jelolt_alak = set().union(*(kimenet_alak.get(l, set()) for l in L))
        st_szam = collections.Counter()
        for w in jelolt_alak:
            for st, n in alak_st[w].items():
                for s in st:
                    if not GRAM.match(s):
                        st_szam[s] += n
        fo = st_szam.most_common(1)[0][0] if st_szam else None
        r = {'cel': 0, 'fo': fo or '—', 'k': e['k'], 'alakok': e['alakok']}
        for v in VALTOZATOK:
            for m in 'abc':
                r[(v, m)] = 0
        for w in jelolt_alak:
            for st, n in alak_st[w].items():
                if not ((fo in st) if fo else False) and st:
                    continue
                r['cel'] += n
                for v in VALTOZATOK:
                    ok = kimenet[v][w] in L
                    r[(v, 'a')] += n if ok else 0
                    r[(v, 'b')] += n if ok or w.lower() in L else 0
                    r[(v, 'c')] += n if ok or (fo and fo in st) else 0
        eredm[kulcs] = r
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    for cim, kell in (('a minta minden lemmája', lambda r: True),
                      ('a K tábla alakjai nélküli lemmák (a DT-F94c döntő halmaza)', lambda r: not r['k'])):
        sor = {k: r for k, r in eredm.items() if kell(r) and r['cel']}
        ures = [k for k, r in eredm.items() if kell(r) and not r['cel']]
        ossz = sum(r['cel'] for r in sor.values())
        print(f'#### M2 — {cim}: {len(sor)} lemma, célhalmaz {ossz} token' + (f' (célhalmaz nélküli lemma: {len(ures)}: {", ".join(ures)})' if ures else '') + '\n')
        print('| változat | (a) token-súlyozva | (b) | (c) | (a) lemmánkénti átlag | (c) lemmánkénti átlag |')
        print('|---|---|---|---|---|---|')
        for v in VALTOZATOK:
            fa = sum(r[(v, 'a')] for r in sor.values())
            fb = sum(r[(v, 'b')] for r in sor.values())
            fc = sum(r[(v, 'c')] for r in sor.values())
            la = sum(r[(v, 'a')] / r['cel'] for r in sor.values()) / max(len(sor), 1)
            lc = sum(r[(v, 'c')] / r['cel'] for r in sor.values()) / max(len(sor), 1)
            print(f'| hibrid {v} | {100 * fa / ossz:.2f}% | {100 * fb / ossz:.2f}% | {100 * fc / ossz:.2f}% ({fc}/{ossz}) | {100 * la:.1f}% | {100 * lc:.1f}% |')
        gyenge = sorted(((100 * r[('A', 'a')] / r['cel'], 100 * r[('C', 'a')] / r['cel'], k, r['cel'], r['fo'])
                         for k, r in sor.items()), key=lambda x: (min(x[0], x[1]), -x[3]))[:12]
        print('\n*A 12 leggyengébb lemma ((a), A / C; célhalmaz, fő Strong):* ' +
              '; '.join(f'{k} {pa:.0f}% / {pc:.0f}% ({n}, {fo})' for pa, pc, k, n, fo in gyenge) + '\n')
    print(f'scope={os.path.basename(a.minta)} (sha256:{sha(a.minta)}) lemmái; a párosított Károli-könyvek ({len(tok)} hu token, {len(formak)} alak) | '
          f'forras=eszkozok/szoto/meres_m2.py + adat/karoli_strong/szavak_*.tsv (együttes sha256:{htok}; modell-kimenet, javaslat) + '
          f'hibrid.py (v3, sha256:{sha(os.path.join(ITT, "hibrid.py"))}) + gyakori_alakok.tsv (sha256:{sha(hibrid._KTAB)}) + '
          f'karoli_lexikon.tsv (sha256:{sha(hibrid._LEX)}) + simplemma {simplemma.__version__} (hu.plzma sha256:'
          f'{sha(os.path.join(os.path.dirname(simplemma.__file__), "strategies", "dictionaries", "data", "hu.plzma"))}) | '
          f'futtatókörnyezet: Python {platform.python_version()} ({platform.system()}) | ts={ts}')


if __name__ == '__main__':
    main()
