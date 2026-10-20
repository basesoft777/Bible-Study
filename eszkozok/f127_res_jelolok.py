"""F127 A2 (DT-F127a): az `alkalmazas` és a `tanitoi` rés jelölőinek beszúrása
az ISTENTISZT-001 forrásába és tanítói fájljába, bájt-összevetéssel.

A szöveg nem változik: a szkript csak a `<!-- RÉS-KEZDET: … -->` és a
`<!-- RÉS-VÉGE: … -->` sort (egy üres sorral) szúrja be, majd ellenőrzi, hogy a
beszúrt karakterláncok eltávolítása után a fájl bájtra azonos az eredetivel.
Eltérésnél nem ír (kilépési kód 1).

Használat:
    python eszkozok/f127_res_jelolok.py            # szárazfutás: csak ellenőriz
    python eszkozok/f127_res_jelolok.py --ir       # beszúrás + ellenőrzés
"""
import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (fájl, rés, a jelölt szöveg első sorának eleje, a záró jelölő utáni sor eleje)
FELADATOK = (
    ('motivumok/ISTENTISZT-001.md', 'alkalmazas',
     '**Alkalmazási kérdések**', '## 6. Napló-frissítés'),
    ('motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md', 'tanitoi',
     'A vizsgált 13 tanítóból', None),  # None: a fájl végéig
)


def egy_fajl(rel, res, kezdo, zaro, ir):
    path = os.path.join(ROOT, rel)
    with open(path, 'rb') as f:
        eredeti = f.read()
    szoveg = eredeti.decode('utf-8')
    nl = '\r\n' if '\r\n' in szoveg else '\n'
    kezd_jel = '<!-- RÉS-KEZDET: %s -->' % res
    veg_jel = '<!-- RÉS-VÉGE: %s -->' % res
    if kezd_jel in szoveg or veg_jel in szoveg:
        print('%s: a %s jelölő már a fájlban van -- nincs teendő' % (rel, res))
        return 0
    i = szoveg.find(nl + kezdo)
    if i < 0 or szoveg.count(nl + kezdo) != 1:
        print('HIBA: %s: a kezdősor nem egyértelmű: %r' % (rel, kezdo))
        return 1
    i += len(nl)
    if zaro is not None:
        j = szoveg.find(nl + zaro, i)
        if j < 0:
            print('HIBA: %s: a záró sor nem található: %r' % (rel, zaro))
            return 1
        j += len(nl)
        betet_v = veg_jel + nl + nl
    else:
        j = len(szoveg)
        # a fájl végi sorvég után
        betet_v = nl + veg_jel + nl
    betet_k = kezd_jel + nl + nl
    uj = szoveg[:i] + betet_k + szoveg[i:j] + betet_v + szoveg[j:]
    # bájt-összevetés: a betétek eltávolítása után az eredeti
    vissza = uj[:i] + uj[i + len(betet_k):]
    j2 = j  # a második betét helye a visszaállított szövegben
    vissza = vissza[:j2] + vissza[j2 + len(betet_v):]
    if vissza.encode('utf-8') != eredeti:
        print('HIBA: %s: a jelölők nélküli szöveg nem azonos az eredetivel' % rel)
        return 1
    torzs = szoveg[i:j]
    print('%s: %s -- jelölt törzs %d bájt, %d sor; jelölők nélkül bájtra azonos: igen'
          % (rel, res, len(torzs.encode('utf-8')), torzs.count(nl)))
    if ir:
        with open(path, 'wb') as f:
            f.write(uj.encode('utf-8'))
        print('  írva')
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ir', action='store_true')
    a = p.parse_args()
    kod = 0
    for rel, res, kezdo, zaro in FELADATOK:
        kod = max(kod, egy_fajl(rel, res, kezdo, zaro, a.ir))
    return kod


if __name__ == '__main__':
    sys.exit(main())
