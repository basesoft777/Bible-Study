"""Az olvasói bevezetők („Mit mutat ez a rész?”) teljességi mérése egy lexikonlapon (DT-F131t; ISTENTISZT-001 arany
lap, 2026-10-29). Csak olvas.

A lap minden blokkját és alblokkját (`##`–`#####` cím) listázza: van-e olvasói bevezető (a cím utáni első tartalmi sor
`**Mit mutat ez a rész?**`), és ha nincs, miért nem kell:
- igehely-alcím (a 4. Kereszthivatkozások listája): a szakasz bevezetője fedi;
- szótári alcím (`#####`, a Rokon szavak szava): a fölérendelt blokk bevezetője fedi;
- a kézi próza alcíme: eleve olvasói szöveg, a rés bevezetője fedi;
- egyéb: hiány (javítandó).
A proveniencia-sorokat (dőlt `scope=… | forras=… | ts=…`) a Jelmagyarázat „Proveniencia-sor” bejegyzése oldja fel.

  python naplok/OLVASOI_blokk_teljesseg_meres.py lexikon/ISTENTISZT-001_TUDOMANYOS.md [--minden]
"""
import argparse
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eszkozok'))
import kiejtes_szoveg as KSZ  # noqa: E402

IGEHELY = re.compile(r'^#### [1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][A-Za-záéíóöőúüű]{0,7} \d+:\d+')


def meres(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = f.read().split('\n')
    reszek = KSZ._sor_reszek(sorok)
    ki = []
    for i, s in enumerate(sorok):
        if not re.match(r'#{2,5} ', s) or s.startswith('# '):
            continue
        kov = next((x for x in sorok[i + 1:i + 10] if x.strip() and not x.startswith('<!--')), '')
        if kov.startswith('**Mit mutat ez a rész?**'):
            ki.append((i + 1, s, 'van', ''))
            continue
        gen = reszek[i][0] or (i + 2 < len(sorok) and 'GENERÁLT' in ''.join(sorok[i + 1:i + 3]))
        if IGEHELY.match(s):
            ok = 'igehely-alcím: a 4. Kereszthivatkozások bevezetője fedi'
        elif gen and (s.startswith('##### ') or re.match(r'#### [GH]\d{4} — ', s)):
            ok = 'szótári alcím: a fölérendelt blokk (Rokon szavak / szerep) bevezetője fedi'
        elif s.startswith('## ') and not gen:
            ok = 'szakaszcím: a rései (### …) bevezetője fedi'
        elif not gen:
            ok = 'a kézi próza alcíme: eleve olvasói szöveg, a rés bevezetője fedi'
        else:
            ok = 'HIÁNY'
        ki.append((i + 1, s, 'nincs', ok))
    prov = sum(1 for s in sorok if re.match(r'\*\(?[Pp]roveniencia', s.strip()))
    return ki, prov


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lap')
    ap.add_argument('--minden', action='store_true')
    a = ap.parse_args()
    ki, prov = meres(a.lap)
    c = collections.Counter(x[3] if x[2] == 'nincs' else 'van' for x in ki)
    print('blokk / alblokk: %d · olvasói bevezetővel: %d · proveniencia-sor: %d (a Jelmagyarázat oldja fel)'
          % (len(ki), c['van'], prov))
    for k, n in c.most_common():
        if k != 'van':
            print('  bevezető nélkül — %s: %d' % (k, n))
    for i, s, van, ok in ki:
        if a.minden or ok == 'HIÁNY' or (van == 'nincs' and not ok.startswith('igehely')):
            print('%5d  %-5s  %-70.70s  %s' % (i, van, s, ok))


if __name__ == '__main__':
    main()
