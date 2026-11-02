"""F12.6: a TEREMT-002 lexikonoldal-rétegének bekötése — a res_forras.tsv kilenc sora (az ISTENTISZT-001 mintája),
az e28_migralt_nezetek.tsv sora és a motivumok.tsv `forras_study` mezője.

Csak hozzáfűzés, illetve egy üres mező kitöltése; írás előtti és utáni sorösszevetéssel, eltérésnél megállás.

    python naplok/F12_res_forras.py        # száraz futás
    python naplok/F12_res_forras.py --ir
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = 'TEREMT-002'
FORRAS = 'motivumok/TEREMT-002.md'
RES = os.path.join(GYOKER, 'adat', 'res_forras.tsv')
E28 = os.path.join(GYOKER, 'eszkozok', 'ellenorzes', 'e28_migralt_nezetek.tsv')
MOT = os.path.join(GYOKER, 'adat', 'motivumok.tsv')

RES_SOROK = [
    [ID, 'kivonat', '## Kivonat *(kézi)*', 'tanulmany', FORRAS],
    [ID, '2b', '### 2/b. Kiegészítő szótári adatok *(generált)*', 'adat', ''],
    [ID, 'miert_fontos', '### Miért fontos ez a lelet *(kézi)*', 'tanulmany', FORRAS],
    [ID, 'minosites', '### Minősítés *(generált)*', 'adat', ''],
    [ID, 'alatamasztas', '### Alátámasztás *(generált)*', 'adat', ''],
    [ID, 'ertelmezes', '## 6. Értelmezés *(kézi)*', 'tanulmany', FORRAS],
    [ID, 'alkalmazas', '### Alkalmazás és tanítványság *(kézi)*', 'tanulmany', FORRAS],
    [ID, 'tanitoi', '### Tanítói egyezés *(kézi)*', 'tanulmany', 'motivumok/naplok/TEREMT-002_tanitoi_kereses.md'],
    [ID, 'modszertan', '## 7. Módszertan és nyitott kérdések *(kézi)*', 'tanulmany', FORRAS],
]
E28_SOR = [ID, 'lexikon/TEREMT-002_TUDOMANYOS.md', 'lexikon', 'apparatus', '12', '2026-11-02']


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read()
    if '\r\n' in nyers or not nyers.endswith('\n'):
        raise SystemExit('megállás: váratlan sorvég: %s' % ut)
    return nyers[:-1].split('\n')


def ir(ut, sorok):
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(sorok) + '\n')
    if olvas(ut) != sorok:
        raise SystemExit('megállás: a visszaolvasott %s eltér' % ut)


def fejlec(sorok):
    return next(s for s in sorok if not s.startswith('#')).split('\t')


def main():
    r = olvas(RES)
    if fejlec(r) != ['id', 'res', 'fejlec', 'forras', 'tanulmany']:
        raise SystemExit('megállás: a res_forras.tsv fejléce eltér')
    if any(s.startswith(ID + '\t') for s in r):
        raise SystemExit('megállás: a res_forras.tsv-ben már van TEREMT-002-sor')
    r_uj = r + ['\t'.join(x) for x in RES_SOROK]

    e = olvas(E28)
    if fejlec(e) != ['id', 'fajl', 'cel', 'melyseg', 'feladat', 'datum']:
        raise SystemExit('megállás: az e28_migralt_nezetek.tsv fejléce eltér')
    if any(s.startswith(ID + '\t') for s in e):
        raise SystemExit('megállás: az e28-ban már van TEREMT-002-sor')
    e_uj = e + ['\t'.join(E28_SOR)]

    m = olvas(MOT)
    mfej = fejlec(m)
    ix = mfej.index('forras_study')
    m_uj = list(m)
    talalt = [i for i, s in enumerate(m) if s.split('\t')[0] == ID]
    if len(talalt) != 1:
        raise SystemExit('megállás: a motivumok.tsv TEREMT-002-sora nem egy')
    mezok = m[talalt[0]].split('\t')
    if mezok[ix]:
        raise SystemExit('megállás: a forras_study nem üres: %s' % mezok[ix])
    mezok[ix] = FORRAS
    m_uj[talalt[0]] = '\t'.join(mezok)
    if [s for i, s in enumerate(m_uj) if i != talalt[0]] != [s for i, s in enumerate(m) if i != talalt[0]]:
        raise SystemExit('megállás: a motivumok.tsv más sora is változna')

    print('res_forras.tsv: +%d sor; e28: +1 sor; motivumok.tsv: forras_study = %s' % (len(RES_SOROK), FORRAS))
    if '--ir' not in sys.argv:
        print('száraz futás: nincs írás (--ir)')
        return
    ir(RES, r_uj)
    ir(E28, e_uj)
    ir(MOT, m_uj)
    print('írva')


if __name__ == '__main__':
    main()
