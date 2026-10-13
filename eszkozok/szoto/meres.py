"""F94.1 (FELADATOK #94): a szótövezés mérője a mintákon (adat/szoto/szoto_minta_*.tsv, SEMA 2.27).

M1 — szótárialak-pontosság: helyes, ha az elemző kimenete (kisbetűsen) a `szotari_alak`, a `szotari_alak_mai` vagy a
`tovabbi_elfogadhato` (|-vel elválasztva) értékek egyike (kisbetűsen). Alakonként és a `gyakorisag` szerint súlyozva,
rétegenként (`kategoria`). Elemzők: a hibrid A/B/C változata (eszkozok/szoto/hibrid.py) és a simplemma önmagában
(ha telepítve van). Az emMorph nem része (CC BY-NC-SA, DT130 (12)).
Az M2 (keresési találati arány, pooled definíció) a negyedik mintához készül (F94.3).

Használat:
    python eszkozok/szoto/meres.py [--minta <tsv> ...] [--csak-felhasznalo] [--hibak A] [--lexikon <tsv>]
Alapértelmezés: a három átvett minta (és a negyedik, ha létezik)."""
import argparse
import collections
import datetime
import hashlib
import os
import platform
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

SZ = os.path.join(REPO, 'adat', 'szoto')
ALAP = ['szoto_minta_1_fejlesztes.tsv', 'szoto_minta_2_fejlesztes.tsv', 'szoto_minta_3_ellenorzott.tsv',
        'szoto_minta_4_fuggetlen.tsv']
KAT = ['ossz', 'gyakori', 'ragos_nevszo', 'regies_ige', 'regies_helyesiras', 'ige_mai_alak', 'tulajdonnev']


def sha(p, n=12):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:n]


def beolvas(p, csak_felhasznalo):
    sorok = [s for s in open(p, encoding='utf-8').read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    ki = []
    for s in sorok[1:]:
        r = dict(zip(fej, s.split('\t')))
        if not r.get('ellenorzes'):
            sys.exit(f'HIBA: üres ellenorzes: {os.path.basename(p)} {r["alak"]}')
        if csak_felhasznalo and r['ellenorzes'] != 'felhasznalo':
            continue
        jo = {r['szotari_alak'].lower(), r['szotari_alak_mai'].lower()} | \
             {x.lower() for x in r.get('tovabbi_elfogadhato', '').split('|') if x}
        ki.append(dict(alak=r['alak'], gy=int(r['gyakorisag']), kat=r['kategoria'], jo=jo))
    return ki


def elemzok(valtozatok, v2, simp):
    """név -> (modul, változat); a változat None: a simplemma önmagában."""
    e = {}
    for v in valtozatok:
        if v == 'A' and simplemma is None:
            continue
        e[f'hibrid {v}'] = (hibrid, v)
    if v2:
        import hibrid_v2
        for v in v2:
            if v == 'A' and simplemma is None:
                continue
            e[f'v2 {v}'] = (hibrid_v2, v)
    if simp and simplemma is not None:
        e['simplemma'] = (None, None)
    return e


def elemez(modul, v, alak):
    if modul is None:
        return simplemma.lemmatize(alak, lang='hu').lower()
    modul.valtozat(v)
    return modul.to(alak).lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--minta', nargs='*')
    ap.add_argument('--csak-felhasznalo', action='store_true')
    ap.add_argument('--hibak', nargs='*', default=['hibrid A', 'hibrid CK'], help='melyik elemző hibáit listázza')
    ap.add_argument('--valtozatok', nargs='*', default=['A', 'C', 'CK'], help='a hibrid (v3) változatai')
    ap.add_argument('--v2', nargs='*', default=[], help='összevetésül a v2 (hibrid_v2.py) változatai')
    ap.add_argument('--simplemma', action='store_true', help='a simplemma önmagában is')
    ap.add_argument('--lexikon', help='más korpusz-lexikon (csak összevetéshez)')
    a = ap.parse_args()
    if a.lexikon:
        hibrid.lexikon_betolt(a.lexikon)
    mintak = a.minta or [os.path.join(SZ, f) for f in ALAP if os.path.exists(os.path.join(SZ, f))]
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    el = elemzok(a.valtozatok, a.v2, a.simplemma)
    for p in mintak:
        sorok = beolvas(p, a.csak_felhasznalo)
        c = collections.defaultdict(collections.Counter)
        hibak = collections.defaultdict(list)
        for r in sorok:
            for n, (mod, v) in el.items():
                t = elemez(mod, v, r['alak'])
                ok = t in r['jo']
                for k in ('ossz', r['kat']):
                    c[n][(k, ok, 'a')] += 1
                    c[n][(k, ok, 's')] += r['gy']
                if not ok:
                    hibak[n].append((r['gy'], r['alak'], t, '/'.join(sorted(r['jo']))))
        print(f'#### {os.path.basename(p)} ({len(sorok)} alak{", csak felhasznalo" if a.csak_felhasznalo else ""})\n')
        print('| elemző | ' + ' | '.join(KAT) + ' |')
        print('|---|' + '---|' * len(KAT))
        for n in el:
            cel = []
            for k in KAT:
                ja, ha = c[n][(k, True, 'a')], c[n][(k, False, 'a')]
                js, hs = c[n][(k, True, 's')], c[n][(k, False, 's')]
                cel.append(f'{100 * ja / (ja + ha):.0f}% / {100 * js / (js + hs):.1f}% ({ja}/{ja + ha})' if ja + ha else '—')
            print(f'| {n} | ' + ' | '.join(cel) + ' |')
        for n in a.hibak:
            if n in hibak:
                print(f'\n*A {n} hibái (alak → kimenet | helyes; gyakoriság):* ' +
                      '; '.join(f'{al} → {t} | {jo} ({g})' for g, al, t, jo in sorted(hibak[n], key=lambda x: (-x[0], x[1]))))
        print(f'\nscope={os.path.basename(p)} (sha256:{sha(p)}) | forras=eszkozok/szoto/meres.py + hibrid.py (v3, sha256:{sha(os.path.join(ITT, "hibrid.py"))}) + gyakori_alakok.tsv (sha256:{sha(hibrid._KTAB)})' + (f' + hibrid_v2.py (sha256:{sha(os.path.join(ITT, "hibrid_v2.py"))})' if a.v2 else '') + ' '
              f'+ {"a megadott lexikon" if a.lexikon else "adat/szoto/karoli_lexikon.tsv"} (sha256:{sha(a.lexikon or hibrid._LEX)})'
              + (f' + simplemma {simplemma.__version__} (hu.plzma sha256:{sha(os.path.join(os.path.dirname(simplemma.__file__), "strategies", "dictionaries", "data", "hu.plzma"))})'
                 if simplemma else ' (simplemma nélkül)')
              + f' | futtatókörnyezet: Python {platform.python_version()} ({platform.system()}) | ts={ts}\n')


if __name__ == '__main__':
    main()
