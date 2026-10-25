#!/usr/bin/env python
"""A Thayer szakaszonkénti fordításának bemenete: Thayer-betöltő a közös lánchoz (F132; DT-F132d (1), DT-F132b (3)).

A #128 szótárfüggetlen elemeit **importálja, nem másolja és nem módosítja** (`eszkozok/bdb_jelolt/szakasz_bemenet.py`: a
`⟪n⟫` határtoken, a `sz<sorszam>` kulcs, a SHA-1, a csoportosítás, a tokenes alak, a közös összefűző `strong_magyar`); csak
a betöltő Thayer-specifikus: a szakaszok az `adat/thayer_szakaszok.tsv`-ből (SEMA 2.34) jönnek.

  - `szakaszok(strong)`: [{sorszam, jel, utvonal, szoveg, hash, illesztes}] vagy None (a Strong nincs a táblában); a
    `szoveg` a `jel` + `szoveg` egy szóközzel (a BDB-nézet alakja), a `hash` ennek SHA-1-e (a `forditasok.tsv` `sz<n>`
    sorának `forras_hash`-e, DT286 (1)). **Javított nézet (DT-F132i (2)):** a `javitassal` illesztésű Strong sorába az
    `adat/thayer_forras_javitas.tsv` (SEMA 2.38) `javitva` sora a `sor_poz` helyén beszúrja a `javitott_alak`-ot (a tábla
    `elotte` mezőjével igazolva; eltérésnél ValueError). A `thayer_szakaszok.tsv` maga nyers marad.
  - `tokenes`, `csoportok`, `nezet`, `jelentes_szam`, `sorszam_jelentesbol`, `strong_magyar`, `strong_magyar_sorok`, `TOKEN`:
    a #128 függvényei változatlanul.

CLI:
  python eszkozok/thayer_jelolt/thayer_bemenet.py G1941 [--ki PATH]   a tokenes bemenet (csoportokkal)
  python eszkozok/thayer_jelolt/thayer_bemenet.py --ellenoriz        determinizmus, a tokenes alak és a csoportok épsége
TSV: split('\\t'), csv modul nélkül. Fájlt nem ír (csak a --ki útvonalra).
"""
import argparse
import collections
import importlib.util
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
if ITT not in sys.path:
    sys.path.insert(0, ITT)
import kulcs  # noqa: E402

GYOKER = os.path.dirname(os.path.dirname(ITT))
TABLA = os.path.join(GYOKER, 'adat', 'thayer_szakaszok.tsv')
JAV_TABLA = os.path.join(GYOKER, 'adat', 'thayer_forras_javitas.tsv')
SZOTAR = 'Thayer'


def _kozos():
    """A #128 modulja saját néven betöltve (a `szakasz_bemenet` név ne ütközzön)."""
    if 'bdb_szakasz_bemenet_kozos' not in sys.modules:
        ut = os.path.join(GYOKER, 'eszkozok', 'bdb_jelolt', 'szakasz_bemenet.py')
        spec = importlib.util.spec_from_file_location('bdb_szakasz_bemenet_kozos', ut)
        mod = importlib.util.module_from_spec(spec)
        sys.modules['bdb_szakasz_bemenet_kozos'] = mod
        spec.loader.exec_module(mod)
    return sys.modules['bdb_szakasz_bemenet_kozos']


K = _kozos()
TOKEN = K.TOKEN
token = K.token
jelentes_szam = K.jelentes_szam
sorszam_jelentesbol = K.sorszam_jelentesbol
sha1 = K.sha1
tokenes = K.tokenes
csoportok = K.csoportok
nezet = K.nezet
strong_magyar = K.strong_magyar
strong_magyar_sorok = K.strong_magyar_sorok
_hossz = K._hossz
CSOPORT_CEL = K.CSOPORT_CEL

_CACHE = {}


def tabla_olvas(ut=None):
    """-> OrderedDict: Strong_padded -> [sor-dict] (a tábla sorrendjében)."""
    ut = os.path.abspath(ut or TABLA)
    if ut not in _CACHE:
        with open(ut, encoding='utf-8', newline='') as f:
            sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
        fej = sorok[0].split('\t')
        d = collections.OrderedDict()
        for s in sorok[1:]:
            r = dict(zip(fej, s.split('\t')))
            d.setdefault(r['strong'], []).append(r)
        _CACHE[ut] = d
    return _CACHE[ut]


def javitas_olvas(ut=None):
    """-> {(Strong, sorszam): (sor_poz, javitott_alak, elotte)} a javítótábla `javitva` soraiból; {} ha nincs fájl."""
    ut = os.path.abspath(ut or JAV_TABLA)
    kulcs_ = ('jav', ut)
    if kulcs_ not in _CACHE:
        d = {}
        if os.path.exists(ut):
            with open(ut, encoding='utf-8', newline='') as f:
                sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
            fej = sorok[0].split('\t')
            for s in sorok[1:]:
                r = dict(zip(fej, s.split('\t')))
                if r['allapot'] == 'javitva':
                    d[(r['strong'], r['sorszam'])] = (int(r['sor_poz']), r['javitott_alak'], r['elotte'])
        _CACHE[kulcs_] = d
    return _CACHE[kulcs_]


def javitott_szoveg(r, jav):
    """A sor `szoveg`-e a javítótábla beszúrásával (DT-F132i (2)); a nem `javitassal` sor változatlan."""
    sz = r['szoveg']
    if r['illesztes'] != 'javitassal':
        return sz
    j = jav.get((r['strong'], r['sorszam']))
    if j is None:
        return sz
    p, alak, elotte = j
    if p > len(sz) or sz[max(0, p - len(elotte)):p] != elotte:
        raise ValueError('%s#%s: a javítótábla `elotte` mezője nem illeszkedik a sorra' % (r['strong'], r['sorszam']))
    return sz[:p] + alak + sz[p:]


def szakaszok(strong, tabla=None, javitas=None):
    sp = kulcs.strong_pad(strong)
    sorok = tabla_olvas(tabla).get(sp) if sp else None
    if sorok is None:
        return None
    jav = javitas_olvas(javitas)
    if sorok[0]['illesztes'] == 'javitassal' and not any((sp, r['sorszam']) in jav for r in sorok):
        raise ValueError('%s: `javitassal` illesztés, de nincs `javitva` sora a javítótáblában' % sp)
    ki = []
    for r in sorok:
        t = ' '.join(x for x in (r['jel'], javitott_szoveg(r, jav)) if x)
        ki.append({'sorszam': int(r['sorszam']), 'jel': r['jel'], 'utvonal': r['utvonal'], 'szoveg': t, 'hash': sha1(t),
                   'illesztes': r['illesztes']})
    return ki


def ellenoriz(tabla=None):
    hibak, stat, nagy = [], collections.Counter(), []
    for st in tabla_olvas(tabla):
        a, b = szakaszok(st, tabla), szakaszok(st, tabla)
        if a != b:
            hibak.append('%s: nem determinisztikus' % st)
        if [int(n) for n in TOKEN.findall(tokenes(a))] != [x['sorszam'] for x in a]:
            hibak.append('%s: a tokenek sorrendje hibás' % st)
        if [x['sorszam'] for x in a] != list(range(1, len(a) + 1)):
            hibak.append('%s: a sorszámok nem folytonosak' % st)
        cs = csoportok(a)
        if [x for c in cs for x in c] != a:
            hibak.append('%s: a csoportok nem fedik le a szakaszokat' % st)
        if any('⟪' in x['szoveg'] or '⟫' in x['szoveg'] for x in a):
            hibak.append('%s: a szövegben határtoken-jel áll' % st)
        stat['strong'] += 1
        stat['szakasz'] += len(a)
        if len(cs) > 1:
            nagy.append((st, len(nezet(a)), [sum(_hossz(x) for x in c) for c in cs]))
    stat['tobbcsoportos'] = len(nagy)
    return hibak, stat, nagy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('strong', nargs='?')
    ap.add_argument('--ki')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    if a.ellenoriz:
        hibak, stat, nagy = ellenoriz()
        print('Strong %d, szakasz %d; több csoportos Strong: %d' % (stat['strong'], stat['szakasz'], stat['tobbcsoportos']))
        for h in hibak[:50]:
            print('HIBA', h)
        print('RENDBEN' if not hibak else 'HIBA: %d' % len(hibak))
        return 1 if hibak else 0
    if not a.strong:
        ap.error('Strong-szám vagy --ellenoriz kell')
    szak = szakaszok(a.strong)
    if szak is None:
        print('%s: nincs a thayer_szakaszok.tsv-ben' % a.strong)
        return 2
    cs = csoportok(szak)
    ki = []
    for i, c in enumerate(cs):
        if len(cs) > 1:
            ki.append('# csoport %d/%d (%d karakter)' % (i + 1, len(cs), sum(_hossz(x) for x in c)))
        ki.append(tokenes(c))
    szoveg = '\n'.join(ki) + '\n'
    if a.ki:
        with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('irva: %s (%d szakasz, %d csoport)' % (a.ki, len(szak), len(cs)))
    else:
        sys.stdout.write(szoveg)
    return 0


if __name__ == '__main__':
    sys.exit(main())
