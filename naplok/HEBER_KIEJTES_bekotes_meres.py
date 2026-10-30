"""A gépi héber kiejtés bekötésének mérése a két migrált lapon (DT-F131y, N-F131w; 2026-10-30).

Összeveti a lap commitolt (HEAD) változatát a munkafa változatával: hány „…, gépi” jelölés és hány különböző héber szó
kapott gépi kiejtést, hány „(szótári alak: …)” jelölés maradt, és mely héber szavak állnak kiejtés nélkül a generált
részen (`kiejtes_szoveg.elemez`). Csak kiír (stdout); adatot nem ír.
"""
import collections
import os
import re
import subprocess
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import kiejtes_szoveg as KSZ  # noqa: E402

LAPOK = ['lexikon/ISTENTISZT-001_TUDOMANYOS.md', 'lexikon/ALVIL-001_TUDOMANYOS.md']
GEPI_ZAROJEL = re.compile(r'(%s)(?:\*\*)?(?:\s*\*\([^)]*\)\*)?\s*\(([^()]*?), gépi\)' % KSZ.HEBER)
GEPI_CELLA = re.compile(r'\|\s*(?:\*\*)?(%s)(?:\*\*)?[^|]*\|\s*([^|]*?), gépi\s*\|' % KSZ.HEBER)


def meres(szoveg):
    szavak = collections.Counter()
    for m in GEPI_ZAROJEL.finditer(szoveg):
        szavak[KSZ.heber_kulcs(m.group(1))] += 1
    for m in GEPI_CELLA.finditer(szoveg):
        szavak[KSZ.heber_kulcs(m.group(1))] += 1
    hiany = [h for h in KSZ.elemez(szoveg) if h[2] == 'generált' and re.match(KSZ.HEBER, h[3])]
    return {
        'gepi_jeloles': szoveg.count(', gépi'),
        'gepi_szo': len(szavak),
        'szotari_alak': szoveg.count('szótári alak:'),
        'heber_hiany_generalt': len(hiany),
        'hiany_szavak': sorted({h[3] for h in hiany}),
    }


def main():
    for lap in LAPOK:
        regi = subprocess.run(['git', 'show', 'HEAD:' + lap], cwd=ROOT, capture_output=True).stdout.decode('utf-8')
        with open(os.path.join(ROOT, lap), encoding='utf-8') as f:
            uj = f.read()
        a, b = meres(regi), meres(uj)
        print('== %s' % lap)
        for k in ('gepi_jeloles', 'gepi_szo', 'szotari_alak', 'heber_hiany_generalt'):
            print('  %-22s előtte %4d  utána %4d' % (k, a[k], b[k]))
        print('  maradt (generált, héber):', ' '.join(b['hiany_szavak']))


if __name__ == '__main__':
    main()
