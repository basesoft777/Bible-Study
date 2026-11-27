#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V — a Macula-alaktani kódok rövid, olvasható magyar alakja (az ellenőrző oldal szókártyáihoz).

Héber/arámi: a Macula (OSHB-jellegű) kódja nyelvi előtag nélkül, pl. `Ncmsa`, `Vqp3ms`, `Sp3ms`, `Td`.
A törzs (binján) betűje héberben és arámiban mást jelent (pl. `P` = pual / itpaal), ezért a nyelvet
a vers dönti el (`arami_vers`); a vegyes versben (1Móz 31:47, Dán 2:4) a kétértelmű törzsbetűt nem
nevezzük meg, csak a betűt adjuk. Görög: Robinson-kód, pl. `V-PAP-NSM`, `N-GSF`, `T-NSM`.

`heber(kod, arami)` és `gorog(kod)`: a magyar alak, vagy None, ha a kód nem fejthető meg
(ilyenkor az oldal a nyers kódot mutatja).
"""

import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------- héber / arámi

TORZS_HEBER = {
    'q': 'qal', 'N': 'nifal', 'p': 'piél', 'P': 'pual', 'h': 'hifil', 'H': 'hofal', 't': 'hitpaél',
    'o': 'polél', 'O': 'polal', 'r': 'hitpolél', 'm': 'poél', 'M': 'poal', 'k': 'palél', 'K': 'pulal',
    'Q': 'qal passivum', 'l': 'pilpél', 'L': 'polpal', 'f': 'hitpalpél', 'D': 'nitpaél', 'j': 'pealal',
    'i': 'pilél', 'u': 'hotpaal', 'c': 'tifil', 'v': 'histafél', 'w': 'nitpalél', 'y': 'nitpoél', 'z': 'hitpoél',
}
TORZS_ARAMI = {
    'q': 'peal', 'Q': 'peíl', 'u': 'hitpeél', 'p': 'pael', 'P': 'itpaal', 'M': 'hitpaal', 'a': 'afél',
    'h': 'hafél', 's': 'safél', 'e': 'safél', 'H': 'hofal', 'i': 'itpeél', 't': 'histafal', 'v': 'istafal',
    'w': 'hitafal', 'o': 'polél', 'z': 'itpoél', 'r': 'hitpolél', 'f': 'hitpalpél', 'b': 'hefal', 'c': 'tifél',
    'm': 'poél', 'l': 'palpél', 'L': 'itpalpal', 'O': 'itpolal', 'G': 'ittafal',
}
IGEALAK = {
    'p': 'perfectum', 'q': 'w-perfectum (weqatal)', 'i': 'imperfectum', 'w': 'wayyiqtol', 'h': 'cohortativus',
    'j': 'iussivus', 'v': 'imperativus', 'r': 'part. act.', 's': 'part. pass.', 'a': 'inf. abs.', 'c': 'inf. cstr.',
}
NEM = {'m': 'hn.', 'f': 'nn.', 'c': 'közös nem', 'b': 'hn./nn.', 'x': ''}
SZAM = {'s': 'e.sz.', 'p': 't.sz.', 'd': 'kettes sz.', 'x': ''}
ALLAPOT = {'a': 'abszolút', 'c': 'status constr.', 'd': 'determinált'}
SZOFAJ_T = {'d': 'névelő', 'o': 'tárgyjelölő (ʾet)', 'n': 'tagadószó', 'r': 'vonatkozó szó', 'i': 'kérdőszó',
            'm': 'mutató partikula', 'a': 'megerősítő partikula', 'e': 'buzdító partikula', 'j': 'indulatszó'}
SZOFAJ_P = {'p': 'személyes névmás', 'd': 'mutató névmás', 'i': 'kérdő névmás', 'r': 'vonatkozó névmás',
            'f': 'határozatlan névmás'}
SZOFAJ_N = {'c': 'főnév', 'g': 'népnév', 'p': 'tulajdonnév', 'x': 'főnév'}
SZOFAJ_A = {'a': 'melléknév', 'c': 'tőszámnév', 'o': 'sorszámnév', 'g': 'népnévi melléknév'}

# arámi szakaszok (Károli-kulcs); a vegyes versben a nyelv nem dönthető el
_ARAMI = [('Ezsd', 4, 8, 6, 18), ('Ezsd', 7, 12, 7, 26), ('Dán', 2, 5, 7, 28), ('Jer', 10, 11, 10, 11)]
_VEGYES = {'1Móz 31:47', 'Dán 2:4'}
_IGEHELY = re.compile(r'^(.+) (\d+):(\d+)$')


def arami_vers(vers):
    """True: arámi; False: héber; None: vegyes vers (a törzsbetű kétértelmű)."""
    if vers in _VEGYES:
        return None
    m = _IGEHELY.match(vers)
    if not m:
        return False
    k, f, v = m.group(1), int(m.group(2)), int(m.group(3))
    for kk, f1, v1, f2, v2 in _ARAMI:
        if k == kk and (f1, v1) <= (f, v) <= (f2, v2):
            return True
    return False


def _szgsz(sz, n, s):
    """személy + nem + szám -> 'E/3 hn.' alak."""
    if sz not in '123' or n not in NEM or s not in SZAM:
        return None
    jel = {'s': 'E', 'p': 'T'}.get(s)
    alap = ('%s/%s' % (jel, sz)) if jel else ('%s. sz. %s' % (sz, SZAM[s]))
    return (alap + (' ' + NEM[n] if NEM[n] else '')).strip()


def _ngsz(n, s, a=None):
    if n not in NEM or s not in SZAM or (a is not None and a not in ALLAPOT):
        return None
    reszek = [NEM[n], SZAM[s]] + ([ALLAPOT[a]] if a else [])
    return ' '.join(x for x in reszek if x)


def heber(kod, arami=False):
    if not kod:
        return None
    f, r = kod[0], kod[1:]
    if f == 'N':
        if not r or r[0] not in SZOFAJ_N:
            return None
        if r == 'p':
            return 'tulajdonnév'
        if len(r) == 4:
            t = _ngsz(r[1], r[2], r[3])
            return t and '%s, %s' % (SZOFAJ_N[r[0]], t)
        return None
    if f == 'A':
        if len(r) == 4 and r[0] in SZOFAJ_A:
            t = _ngsz(r[1], r[2], r[3])
            return t and '%s, %s' % (SZOFAJ_A[r[0]], t)
        return None
    if f == 'V':
        if len(r) < 2:
            return None
        if arami is None and r[0] in TORZS_HEBER and r[0] in TORZS_ARAMI and TORZS_HEBER[r[0]] != TORZS_ARAMI[r[0]]:
            torzs = 'törzs: %s' % r[0]
        else:
            torzs = (TORZS_ARAMI if arami else TORZS_HEBER).get(r[0])
        alak = IGEALAK.get(r[1])
        if not torzs or not alak:
            return None
        rest = r[2:]
        if r[1] in 'rs':
            if len(rest) == 3:
                t = _ngsz(rest[0], rest[1], rest[2])
            elif len(rest) == 2:
                t = _ngsz(rest[0], rest[1])
            else:
                t = None
            return t and 'ige, %s %s, %s' % (torzs, alak, t)
        if r[1] in 'ac':
            return 'ige, %s %s' % (torzs, alak) if not rest else None
        if len(rest) == 3:
            t = _szgsz(rest[0], rest[1], rest[2])
            return t and 'ige, %s %s, %s' % (torzs, alak, t)
        return None
    if f == 'S':
        if r == 'd':
            return 'irányjelölő -āh'
        if r == 'h':
            return 'nyomatékos -āh'
        if r == 'n':
            return 'paragogikus nun'
        if len(r) == 4 and r[0] == 'p':
            t = _szgsz(r[1], r[2], r[3])
            return t and 'névmási rag, %s' % t
        return None
    if f == 'P':
        if not r or r[0] not in SZOFAJ_P:
            return None
        if len(r) == 1:
            return SZOFAJ_P[r[0]]
        if len(r) == 4:
            t = _ngsz(r[2], r[3]) if r[1] == 'x' else _szgsz(r[1], r[2], r[3])
            return t and '%s, %s' % (SZOFAJ_P[r[0]], t)
        if len(r) == 3:
            t = _ngsz(r[1], r[2])
            return t and '%s, %s' % (SZOFAJ_P[r[0]], t)
        return None
    if f == 'T':
        if r == '':
            return 'partikula'
        return SZOFAJ_T.get(r)
    if kod == 'R':
        return 'elöljárószó'
    if kod == 'Rd':
        return 'elöljárószó + névelő'
    if kod == 'C':
        return 'kötőszó'
    if kod == 'D':
        return 'határozószó'
    return None


# ---------------------------------------------------------------- görög (Robinson)

ESET = {'N': 'nom.', 'G': 'gen.', 'D': 'dat.', 'A': 'acc.', 'V': 'voc.'}
GSZAM = {'S': 'e.sz.', 'P': 't.sz.'}
GNEM = {'M': 'hn.', 'F': 'nn.', 'N': 'semlegesnem'}
IDO = {'P': 'praesens', 'I': 'imperfectum', 'F': 'futurum', 'A': 'aoristus', 'R': 'perfectum',
       'L': 'plusquamperf.', '2A': 'aoristus (2.)', '2F': 'futurum (2.)', '2R': 'perfectum (2.)',
       '2L': 'plusquamperf. (2.)'}
IGENEM = {'A': 'act.', 'M': 'med.', 'P': 'pass.', 'E': 'med./pass.', 'D': 'med. (dep.)', 'O': 'pass. (dep.)',
          'N': 'med./pass. (dep.)', 'Q': 'impers. act.', 'X': ''}
MOD = {'I': 'ind.', 'S': 'coni.', 'O': 'opt.', 'M': 'imper.', 'N': 'inf.', 'P': 'part.'}
GSZOFAJ = {'N': 'főnév', 'A': 'melléknév', 'T': 'névelő', 'R': 'vonatkozó névmás', 'C': 'kölcsönös névmás',
           'D': 'mutató névmás', 'K': 'korrelatív névmás', 'I': 'kérdő névmás', 'X': 'határozatlan névmás',
           'Q': 'korrelatív/kérdő névmás', 'F': 'visszaható névmás', 'S': 'birtokos névmás', 'P': 'személyes névmás'}
EGYSZERU = {'ADV': 'határozószó', 'CONJ': 'kötőszó', 'PREP': 'elöljárószó', 'PRT': 'partikula',
            'INJ': 'indulatszó', 'COND': 'feltételes kötőszó', 'ARAM': 'arámi szó (nem ragozott)',
            'HEB': 'héber szó (nem ragozott)'}
UTOTAG = {'C': 'középfok', 'S': 'felsőfok', 'I': 'kérdő', 'N': 'tagadó', 'K': 'korrelatív'}


def _eszn(x):
    """'GSF' -> 'gen. e.sz. nn.'; 'NP' (nem nélkül) is."""
    if len(x) == 3 and x[0] in ESET and x[1] in GSZAM and x[2] in GNEM:
        return '%s %s %s' % (ESET[x[0]], GSZAM[x[1]], GNEM[x[2]])
    if len(x) == 2 and x[0] in ESET and x[1] in GSZAM:
        return '%s %s' % (ESET[x[0]], GSZAM[x[1]])
    return None


def gorog(kod):
    if not kod:
        return None
    r = kod.split('-')
    f = r[0]
    if f in EGYSZERU:
        alap = EGYSZERU[f]
        u = [UTOTAG[x] for x in r[1:] if x in UTOTAG]
        return alap + (' (%s)' % ', '.join(u) if u else '')
    if f == 'V':
        if len(r) < 2:
            return None
        m = re.match(r'^(2?[PIFARL])([AMPEDONQX])([ISOMNP])$', r[1])
        if not m:
            return None
        ido, nem, mod = IDO.get(m.group(1)), IGENEM.get(m.group(2)), MOD.get(m.group(3))
        if ido is None or nem is None or mod is None:
            return None
        alap = 'ige, %s %s %s' % (ido, nem, mod)
        alap = ' '.join(alap.split())
        if m.group(3) == 'N':
            return alap if all(x == 'ATT' for x in r[2:]) else None
        if len(r) == 2:
            return None
        x = r[2]
        if m.group(3) == 'P':
            t = _eszn(x)
            return t and '%s, %s' % (alap, t)
        mm = re.match(r'^([123])([SP])$', x)
        if mm:
            return '%s, %s/%s' % (alap, 'E' if mm.group(2) == 'S' else 'T', mm.group(1))
        return None
    if f in GSZOFAJ:
        if len(r) < 2:
            return None
        x = r[1]
        nev = GSZOFAJ[f]
        if f == 'N' and x == 'PRI':
            return 'tulajdonnév (nem ragozott)'
        if f == 'N' and x in ('LI', 'OI'):
            return 'főnév (nem ragozott)'
        if f == 'A' and x == 'NUI':
            return 'számnév (nem ragozott)'
        u = [UTOTAG[y] for y in r[2:] if y in UTOTAG]
        uto = (' (%s)' % ', '.join(u)) if u else ''
        m = re.match(r'^([123])([A-Z]+)$', x)
        if f in ('P', 'F', 'S') and m:
            szem = m.group(1)
            rest = m.group(2)
            if f == 'S' and len(rest) == 4 and rest[0] in GSZAM:
                t = _eszn(rest[1:])
                return t and '%s (%s/%s), %s%s' % (nev, 'E' if rest[0] == 'S' else 'T', szem, t, uto)
            t = _eszn(rest)
            return t and '%s, %d. sz., %s%s' % (nev, int(szem), t, uto)
        t = _eszn(x)
        return t and '%s, %s%s' % (nev, t, uto)
    return None


if __name__ == '__main__':
    for k in sys.argv[1:]:
        print(k, '->', heber(k) if not '-' in k and k not in EGYSZERU else gorog(k))
