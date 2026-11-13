# -*- coding: utf-8 -*-
"""F194.32 — két ISTENTISZT-001 kapcsolat-sor indoklása saját szavakkal (a független ellenőr 2. eltérése, az orkesztrátor
döntése: „a 2Kir 5:11 kapcsolat-indoklása legyen saját szavas, ne Károli-idézetnek álcázott szöveg”).

(1) 1Móz 4:26 → 2Kir 5:11: a TAHOT szerint a versben a formula három szava áll (H7121, H8034, H3068), a név mellett az
„ő Istene” megnevezésével; a kapcsolat a közös formulán áll, idézés nélkül (közepes). (2) 1Móz 4:26 → Sof 3:9 és (3) 1Móz 12:8 → 13:4: az
indoklás idézőjeles, de nem Károli-szövege saját szavakra. Kulcs: (forras_igehely, cel_igehely, id).
Futtatás a repó gyökeréből: python naplok/F194_kapcsolat_szoveg2.py"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
P = 'adat/kapcsolatok.tsv'
UJ = {
    ('1Móz 4:26', '2Kir 5:11'): {
        'funkcio': 'azonos szereposztás: a formula egy idegen szájában, a név mellett az ő Istene megnevezésével',
        'indoklas': 'A versben a formula mindhárom szava áll (a hívás igéje, a név és utána az Úr neve), a név mellett '
                    'Naámán az Urat a próféta Istenének is nevezi; a hely a korábbi helyet nem idézi, a kapcsolat a közös '
                    'formulán áll, idézés nélkül, innen a közepes bizonyosság.'},
    ('1Móz 12:8', '1Móz 13:4'): {
        'indoklas': 'A 13:4 maga mondja ki, hogy Ábrám annak az oltárnak a helyére megy, „melyet ott elsőben készített '
                    'vala”: azonos helyszín, azonos szereplő, közvetlen szövegi utalás, nem rekonstrukció.'},
    ('1Móz 4:26', 'Sof 3:9'): {
        'indoklas': 'Mindkét hely a formulát hozza: az 1Móz 4:26 a segítségül hívás kezdetét mondja ki, a Sof 3:9 azt '
                    'ígéri, hogy a népek mind segítségül hívják az Úr nevét; a közös szókapcsolat hitvallási nyelv, nem '
                    'csak tematikus rokonság.'},
}
raw = open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
sorok = raw.split(nl)
fej = [s for s in sorok if s and not s.startswith('#')][0].split('\t')
ix = {k: i for i, k in enumerate(fej)}
n = 0
for i, s in enumerate(sorok):
    c = s.split('\t')
    if len(c) == len(fej) and c[ix['id']] == 'ISTENTISZT-001' and (c[0], c[1]) in UJ:
        for k, v in UJ[(c[0], c[1])].items():
            c[ix[k]] = v
        sorok[i] = '\t'.join(c); n += 1
assert n == 3, n
open(P, 'w', encoding='utf-8', newline='').write(nl.join(sorok))
print('%s: %d sor' % (P, n))
