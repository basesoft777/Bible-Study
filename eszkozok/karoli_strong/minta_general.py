#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 P0.2 — a 200 verses pilotminta előállítása rögzített véletlenmaggal.

Kimenet: f21p/minta.tsv (generált; kézzel nem szerkesztendő).

Rétegek (F21 brief P0.2):
  R1 ÓSZ próza + bölcsesség : 1Móz 40, 2Móz 30, Péld 30  (100 vers, KJV-támponttal)
  R2 ÓSZ költészet          : Zsolt 13, Jób 12           (25)
  R3 ÓSZ próféták           : Ézs 9, Jer 8, Ez 8         (25)
  R4 ÚSZ                    : evangéliumok 25 (Mt 7, Mk 6, Luk 6, Ján 6),
                              levelek 25 (Róm–Júd, egyenletes húzás)  (50)

A briefben megadott darabszámokon túli felosztás (Zsolt/Jób, Ézs/Jer/Ez,
evangéliumonként) a szkript rögzített döntése; a levelek köre Róm–Júd
(ApCsel és Jel nem része a F21-mintának, a brief szerint csak "evangéliumok"
és "levelek").

Kizárások (a jelöltkészletből):
  * a 61 + 30 versmegfeleltetési maradék (tokenek.maradek);
  * a sorrend-ellenőrzésen elbukott versek (f21p/sorrend_eltero_versek.tsv:
    a kivonat sorrendje nem a szórend, ezért a sorszám nem származtatható);
  * 0 Károli-tokenes vers;
  * R1-ben az a vers, amelyhez nincs KJV-támpont (tokenek.kjv_tamapont).

1Móz: a 40 versből legalább 20 olyan, amelyhez van sor a régi aranyban
(Karoli_Strong_kivonat.tsv); a szkript 24-et húz ezekből.

A maggal és a bemeneti adatokkal a kimenet bájtra azonos (a jelöltlisták
kanonikus sorrendben, a húzás random.Random(MAG).sample).

Futtatás a repó gyökeréből:
    python eszkozok/karoli_strong/minta_general.py
"""

import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

MAG = 20260930
KIMENET = os.path.join(tokenek.ROOT, 'f21p', 'minta.tsv')
ELTERO = os.path.join(tokenek.ROOT, 'f21p', 'sorrend_eltero_versek.tsv')

# (réteg, alréteg, [könyvek], darab)
TERV = [
    ('R1', 'proza_bolcsesseg', ['1Móz'], 40),
    ('R1', 'proza_bolcsesseg', ['2Móz'], 30),
    ('R1', 'proza_bolcsesseg', ['Péld'], 30),
    ('R2', 'kolteszet', ['Zsolt'], 13),
    ('R2', 'kolteszet', ['Jób'], 12),
    ('R3', 'profetak', ['Ézs'], 9),
    ('R3', 'profetak', ['Jer'], 8),
    ('R3', 'profetak', ['Ez'], 8),
    ('R4', 'evangelium', ['Mt'], 7),
    ('R4', 'evangelium', ['Mk'], 6),
    ('R4', 'evangelium', ['Luk'], 6),
    ('R4', 'evangelium', ['Ján'], 6),
    ('R4', 'level', ['Róm', '1Kor', '2Kor', 'Gal', 'Ef', 'Fil', 'Kol', '1Thessz', '2Thessz',
                     '1Tim', '2Tim', 'Tit', 'Filem', 'Zsid', 'Jak', '1Pét', '2Pét',
                     '1Ján', '2Ján', '3Ján', 'Júd'], 25),
]
ARANY_MIN_1MOZ = 20
ARANY_HUZAS_1MOZ = 24
KOTEGMERET = 10


def eltero_versek():
    if not os.path.exists(ELTERO):
        raise SystemExit('hiányzik: %s (előbb a sorrend_ellenoriz.py)' % ELTERO)
    return {r[0] for r in tokenek._sorok(ELTERO)}


def general():
    karoli = tokenek.betolt_karoli()
    ered = tokenek.betolt_eredeti()
    a, b = tokenek.maradek(karoli, ered)
    kizart = set(a) | set(b) | eltero_versek()
    arany_versek = {ig for ig, _, _ in tokenek.regi_arany()}
    arany_sorok = {}
    for ig, _, _ in tokenek.regi_arany():
        arany_sorok[ig] = arany_sorok.get(ig, 0) + 1
    rnd = random.Random(MAG)
    sorok = []
    hasznalt = set()
    for reteg, alreteg, konyvek, n in TERV:
        halmaz = set(konyvek)
        jeloltek = []
        for ig, szoveg in karoli.items():
            if tokenek.konyv_rovid(ig) not in halmaz or ig in kizart or ig in hasznalt:
                continue
            if not tokenek.tokenizal(szoveg) or ig not in ered:
                continue
            if reteg == 'R1' and tokenek.kjv_tamapont(ig) is None:
                continue
            jeloltek.append(ig)
        if konyvek == ['1Móz']:
            arany_j = [ig for ig in jeloltek if ig in arany_versek]
            egyeb_j = [ig for ig in jeloltek if ig not in arany_versek]
            if len(arany_j) < ARANY_HUZAS_1MOZ:
                raise SystemExit('1Móz: kevés régi-arany vers (%d)' % len(arany_j))
            valasztas = rnd.sample(arany_j, ARANY_HUZAS_1MOZ) + rnd.sample(egyeb_j, n - ARANY_HUZAS_1MOZ)
        else:
            if len(jeloltek) < n:
                raise SystemExit('kevés jelölt: %s (%d < %d)' % (konyvek, len(jeloltek), n))
            valasztas = rnd.sample(jeloltek, n)
        for ig in valasztas:
            hasznalt.add(ig)
            sorok.append((reteg, alreteg, ig))
    # kanonikus sorrend rétegen belül (R1..R4), azon belül Károli-fájlsorrend
    sorrend = {ig: i for i, ig in enumerate(karoli)}
    sorok.sort(key=lambda x: (x[0], sorrend[x[2]]))
    fejlec = ['sorsz', 'igehely', 'reteg', 'alreteg', 'kotegsz', 'kjv_tamapont',
              'eredeti_szo', 'karoli_szo', 'regi_arany_sor']
    ki = ['\t'.join(fejlec)]
    for i, (reteg, alreteg, ig) in enumerate(sorok):
        ki.append('\t'.join([
            str(i + 1), ig, reteg, alreteg, str(i // KOTEGMERET + 1),
            'van' if reteg == 'R1' else 'nincs',
            str(len(ered[ig])), str(len(tokenek.tokenizal(karoli[ig]))),
            str(arany_sorok.get(ig, 0)),
        ]))
    return ki, sorok


def main():
    ki, sorok = general()
    os.makedirs(os.path.dirname(KIMENET), exist_ok=True)
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')
    print('mag: %d, vers: %d -> %s' % (MAG, len(sorok), KIMENET))
    szam = {}
    for reteg, _, _ in sorok:
        szam[reteg] = szam.get(reteg, 0) + 1
    print('rétegek: %s' % ', '.join('%s=%d' % kv for kv in sorted(szam.items())))


if __name__ == '__main__':
    main()
