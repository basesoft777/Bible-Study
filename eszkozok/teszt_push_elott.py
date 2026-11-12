#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_push_elott.py -- F216: a `eszkozok/push_elott.py` tesztje.

Fut: python eszkozok/teszt_push_elott.py (a CI szabály-teszt lépésében is). Kilépési kód: 0 = zöld.
"""

import io
import os
import subprocess
import sys
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import push_elott as P

HIBAK = []


def ellenoriz(feltetel, nev):
    if feltetel:
        print('RENDBEN  ' + nev)
    else:
        print('BUKOTT   ' + nev)
        HIBAK.append(nev)


def valos_workflow():
    with open(P.WORKFLOW, encoding='utf-8') as f:
        return f.read()


def main():
    wf = valos_workflow()

    # 1. a valódi workflow egyezik a lépéslistával
    ellenoriz(P.ci_egyezes() == [], 'a valódi workflow egyezik a lépéslistával')

    # 2. egy hiányzó tesztlépés a workflow-ból -> HIBA
    csonka = wf.replace('python eszkozok/teszt_gyokerok_kapuk.py', 'echo kihagyva')
    hibak = P.ci_egyezes(csonka)
    ellenoriz(any('teszt_gyokerok_kapuk.py' in h for h in hibak), 'hiányzó teszt a workflow-ból: HIBA')

    # 3. megváltozott állandó argumentum (--szigoru kiesik) -> HIBA
    gyenge = wf.replace('allitas_adat.py --minden --szigoru', 'allitas_adat.py --minden')
    ellenoriz(any('allitas_adat.py' in h for h in P.ci_egyezes(gyenge)), 'kiesett --szigoru: HIBA')

    # 4. a workflow-ban van egy új, a listán kívüli szkript -> HIBA
    uj = wf.replace('python eszkozok/teszt_proza_allitas.py', 'python eszkozok/teszt_proza_allitas.py\n          python eszkozok/teszt_uj_kapu.py')
    ellenoriz(any('teszt_uj_kapu.py' in h for h in P.ci_egyezes(uj)), 'új szkript a workflow-ban, a listán kívül: HIBA')

    # 5. az egyezés-lépés hiánya -> HIBA
    ellenoriz(any('egyezés-lépés' in h for h in P.ci_egyezes(wf.replace('--ci-egyezes', ''))), 'az egyezés-lépés hiánya: HIBA')

    # 6. a megjegyzéssor nem számít hívásnak
    ellenoriz(P.python_hivasok('# python eszkozok/x.py\n  run: python eszkozok/y.py a b\n') == [('eszkozok/y.py', ' a b')],
              'a megjegyzéssor nem hívás')

    # 7. a sorvégi folytatás egy hívássá áll össze
    folyt = P.python_hivasok('python eszkozok/z.py \\\n  --a 1 \\\n  --b 2\n')
    ellenoriz(folyt and '--a 1' in folyt[0][1] and '--b 2' in folyt[0][1], 'a sorvégi folytatás összevonva')

    # 8. a lépés-futtató: bukó lépés HIBA-sorral és nyilvántartással, rendben lévő lépés nem
    fut = P.Futas()
    puf = io.StringIO()
    with redirect_stdout(puf):
        rc_jo, _ = fut.lepes('jó', [sys.executable, '-c', 'print("rendben")'])
        rc_rossz, _ = fut.lepes('rossz', [sys.executable, '-c', 'print("- `HIBA` x.md:1 -- baj"); raise SystemExit(1)'])
    ki = puf.getvalue()
    ellenoriz(rc_jo == 0 and rc_rossz == 1 and len(fut.hibas) == 1 and fut.hibas[0][0] == 'rossz', 'a futtató csak a bukó lépést jegyzi')
    ellenoriz('HIBA     rossz' in ki and '`HIBA` x.md:1' in ki, 'a bukó lépés HIBA-sora kiíródik')

    # 9. a parancssori --ci-egyezes a valódi fájlon 0
    r = subprocess.run([sys.executable, os.path.join(P.ROOT, 'eszkozok', 'push_elott.py'), '--ci-egyezes'],
                       capture_output=True, encoding='utf-8', cwd=P.ROOT)
    ellenoriz(r.returncode == 0, '--ci-egyezes kilépési kódja 0')

    print()
    if HIBAK:
        print('BUKOTT: %d teszt: %s' % (len(HIBAK), '; '.join(HIBAK)))
        return 1
    print('Minden teszt zöld.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
