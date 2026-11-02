"""F12 8. lépés: a TEREMT-002 próbalapjának mérése az ISTENTISZT-001 arany lapja mellett. Csak olvas.

(a) a 21. szabály (lap-tisztaság) gépi része a próbalapon (`ellenoriz.lap_hibak`); a „fordításra vár” jelölések;
(c) arany-összevetés: a lap `##`/`###` címsorai és a mércének nevezett blokkok (szótári gerinc, a „Jelentés
    (a szó)” / „Funkció (a motívumban)” oszlopok, ⓘ-lábjegyzetek, LXX-sor, kolofon, 12–14. szerep) mindkét lapon.

    python naplok/F12_proba_meres.py <TEREMT-002 próbalap> [arany lap, alap: lexikon/ISTENTISZT-001_TUDOMANYOS.md]
"""
import os
import re
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import ellenoriz as E  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BLOKKOK = [
    ('szótári gerinc (DT272)', r'Szótári gerinc \(DT272\)'),
    ('„Jelentés (a szó)” oszlop', r'Jelentés \(a szó\)'),
    ('„Funkció (a motívumban)” oszlop', r'Funkció \(a motívumban\)'),
    ('ⓘ-lábjegyzet', r'ⓘ'),
    ('Mit mutat ez a rész?', r'\*\*Mit mutat ez a rész\?\*\*'),
    ('Következtetés', r'\*\*Következtetés:\*\*'),
    ('LXX-fordítói döntések szakasz', r'^## 3\. LXX-fordítói döntések'),
    ('LXX-döntés sor (adat/lxx_dontesek.tsv)', r'\| adat/lxx_dontesek\.tsv \|'),
    ('12. Tematikus index', r'^#### 12\. '),
    ('13. Károli-megfelelők', r'^#### 13\. '),
    ('14. Rejtett / hamis párhuzam', r'^#### 14\. '),
    ('Kolofon', r'^## Kolofon'),
    ('Irodalom és idézés', r'^## 8\. Irodalom és idézés'),
    ('Tanítói egyezés rés', r'^### Tanítói egyezés'),
    ('Alkalmazás rés', r'^### Alkalmazás és tanítványság'),
    ('Miért fontos rés', r'^### Miért fontos ez a lelet'),
    ('Kizárt és vizsgált helyek', r'^## 1/b\. Kizárt és vizsgált helyek'),
    ('Kapcsolódó motívumok', r'^## 5/b\. Kapcsolódó motívumok'),
    ('ÜRES-BLOKK jelölő', r'ÜRES-BLOKK'),
    ('„fordításra vár”', r'fordításra vár'),
]


def olvas(ut):
    with open(ut, encoding='utf-8') as f:
        return f.read()


def cimek(szoveg):
    return [re.sub(r'\s*\*\((kézi|generált)\)\*', '', s).strip()
            for s in szoveg.split('\n') if re.match(r'^#{2,3} ', s)]


def main():
    proba = sys.argv[1]
    arany = sys.argv[2] if len(sys.argv) > 2 else os.path.join(GYOKER, 'lexikon', 'ISTENTISZT-001_TUDOMANYOS.md')
    p, a = olvas(proba), olvas(arany)
    print('# (a) 21. szabály, gépi rész (próbalap)')
    h = E.lap_hibak(p, E._letezo_tetelek(GYOKER)[0], E._letezo_tetelek(GYOKER)[1])
    for k, v in sorted(h.items()):
        print('  (%s): %s' % (k, v if v else 'nincs'))
    print('\n# (c) blokkok: arany | próba')
    for nev, minta in BLOKKOK:
        na, np_ = len(re.findall(minta, a, re.M)), len(re.findall(minta, p, re.M))
        print('  %-42s %4d | %4d' % (nev, na, np_))
    print('\n# (c) ##/### címsorok: csak az arany lapon / csak a próbán')
    ca, cp = cimek(a), cimek(p)
    norm = lambda c: re.sub(r':.*$', '', c)  # noqa: E731
    na_, np2 = {norm(c) for c in ca}, {norm(c) for c in cp}
    print('  csak arany:', sorted(na_ - np2))
    print('  csak próba:', sorted(np2 - na_))


if __name__ == '__main__':
    main()
