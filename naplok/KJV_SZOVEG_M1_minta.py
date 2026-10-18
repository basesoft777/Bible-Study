#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KJV_SZOVEG_M1_minta.py -- #118 M1: a kis minta (brief 4. pont, M1) az eszkozok/kjv_szoveg_import.py fuggvenyeivel,
a vers nyers USFM-szovegevel egyutt; plusz epseg-ellenorzesek a teljes (memoriabeli) kimeneten. Csak olvas.

Futtatas:  python -I naplok/KJV_SZOVEG_M1_minta.py --munka C:/Users/bases/Desktop/kjv_munka --ki <scratch>/minta.md
"""

import argparse
import collections
import datetime
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import kjv_szoveg_import as K  # noqa: E402
import f19_ebible_import as f19  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BS = chr(92)
MINTA = [('Gen', 1, 1), ('Gen', 1, 2), ('Gen', 1, 3), ('Psa', 3, 0), ('Psa', 3, 1), ('Psa', 3, 2),
         ('Psa', 119, 1), ('Psa', 119, 8), ('Psa', 119, 9), ('Mat', 1, 1), ('Rev', 22, 21),
         ('Mrk', 9, 43), ('Luk', 6, 41), ('Luk', 17, 36), ('Rom', 16, 27), ('1Jn', 2, 23)]


def nyers_vers(t, f, v):
    """A vers nyers USFM-sorai a forrasbol (labjegyzettel): v=0 -> a \\d sor; kulonben a \\v-tol a kovetkezo \\v / \\c-ig,
    a kozbeeso \\s1 / \\q1 / \\p sorokkal."""
    sorok = t.split('\n')
    i = next(k for k, s in enumerate(sorok) if re.match(re.escape(BS) + r'c %d\s*$' % f, s))
    ki = []
    if v == 0:
        for s in sorok[i + 1:]:
            if s.startswith(BS + 'd'):
                return [s.rstrip()]
        return []
    bent = False
    for s in sorok[i + 1:]:
        if re.match(re.escape(BS) + r'c ', s):
            break
        mv = re.search(re.escape(BS) + r'v ([0-9]+)', s)
        if mv and int(mv.group(1)) == v:
            bent = True
            ki.append(s.rstrip())
            continue
        if bent:
            if mv:
                break
            ki.append(s.rstrip())
    return ki


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--munka', required=True)
    ap.add_argument('--ki', required=True)
    a = ap.parse_args()
    zp = os.path.join(a.munka, 'kjv.zip')
    zsha = K.sha256(zp)
    assert zsha == K.VART_SHA256, zsha
    konyvek = f19.lista_konyvek()
    sz = collections.Counter()
    adat, anom, nyers = K.olvas(zp, konyvek, sz)
    rs = K.sorok(adat, konyvek, sz)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    idx = {r[0]: r for r in rs}
    out = ['<!-- proveniencia: scope=KJV_SZOVEG M1 minta (16 vers) + épség a teljes, memóriabeli kimeneten | forras=kjv.zip sha256=%s | ts=%s -->' % (zsha, ts), '']
    for (b, f, v) in MINTA:
        ih = '%s.%d.%d' % (b, f, v)
        r = idx[ih]
        out.append('#### `%s`' % ih)
        out.append('')
        out.append('| mező | érték |')
        out.append('|---|---|')
        for nev, ert in zip(('Szöveg', 'Szöveg_jelolt', 'Elotte', 'Utoirat'), r[1:]):
            out.append('| `%s` | %s |' % (nev, ert.replace('|', '&#124;') if ert else '*(üres)*'))
        out.append('')
        out.append('Nyers USFM:')
        out.append('')
        out.append('```')
        out += nyers_vers(nyers[b], f, v)
        out.append('```')
        out.append('')
    # epseg
    sajat = {(b, f, v) for b, _ in konyvek for (f, v) in adat[b]}
    f19v = set()
    for b, _ in konyvek:
        vv, _a, _h = f19.parse_usfm(nyers[b])
        f19v |= {(b, f, v) for (f, v) in vv}
    hibak = collections.Counter()
    for r in rs:
        for i, ert in enumerate(r[1:], 1):
            if BS in ert:
                hibak['backslash_mezo%d' % i] += 1
            if re.search(r' [,.;:?!)]', ert):
                hibak['szokoz_irasjel_elott_mezo%d' % i] += 1
            if '  ' in ert:
                hibak['dupla_szokoz_mezo%d' % i] += 1
        if r[2].count('[') != r[2].count(']'):
            hibak['zarojel_paratlan'] += 1
        if '[]' in r[2] or re.search(r'\[\s|\s\]', r[2]):
            hibak['zarojel_ures_vagy_szokoz'] += 1
        if K.PILCROW in r[1]:
            hibak['pilcrow_a_Szovegben'] += 1
        if re.sub(r'[\[\]' + K.PILCROW + r']', '', r[2]).split() != r[1].split():
            hibak['Szoveg_es_jelolt_szavai_elternek'] += 1
    out.append('**Épség a teljes, memóriabeli kimeneten** (a tábla nem íródott a `konkordancia/`-ba):')
    out.append('')
    out.append('- sorok: %d; üres `Szöveg`: %d; `Elotte`: %d; `Utoirat`: %d; vershíd: %d; folytatás-sor: %d; parse-anomália: %d' % (
        len(rs), sum(1 for r in rs if not r[1]), sum(1 for r in rs if r[3]), sum(1 for r in rs if r[4]), sz['vershid'], sz['vers_folytatas_sor'], len(anom)))
    out.append('- a versek halmaza azonos a `f19.parse_usfm`-éval: %s (saját %d, F19 %d)' % (sajat == f19v, len(sajat), len(f19v)))
    out.append('- formai hibák (backslash, szóköz írásjel előtt, dupla szóköz, páratlan/üres `[ ]`, ¶ a `Szöveg`-ben, a két szövegmező szavai eltérnek): %s' % (dict(hibak) or 0))
    out.append('- veszteség-számlálók: ' + ', '.join('%s=%d' % (k, sz[k]) for k in ('w', 'labjegyzet', 'p', 'q1', 'b', 'nd', 'wj', 'tl', 'pilcrow', 'add', 'kiser_add', 'fejlec_sor')))
    with open(a.ki, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(out) + '\n')
    print('\n'.join(out[-6:]))


if __name__ == '__main__':
    main()
