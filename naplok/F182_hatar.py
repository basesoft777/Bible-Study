# -*- coding: utf-8 -*-
"""F182 HAMART-001, 1. fázis, határ (2026-11-10): a `naplok/HATAR_HAMART-001.md` (48 sor, 6 kérdés) K1, K5 és K6
pontjának átvezetése a jeloltek.tsv-n át (DT28; CLAUDE.md 2. szabály). Helyőrzők: DT-F182a (K1), DT-F182b (K5),
DT-F182c (K6); a K2 lezárt (DT683 (B), DT685), a K3 lezárt (N116, DT686), a K4 a felhasználóé
(DT-F182d, nyitott) — ezekhez a szkript nem nyúl.

- K1 (DT-F182a): az 1Móz 4:2-3 elutasítva, és kikerül az elofordulasok.tsv-ből. Azonos jegy, azonos sors: az
  1Móz 2:5, 4:2-3 és 9:20 az אֲדָמָה (adámá) szót a megművelt talaj elbeszélő megnevezésében hozza, átok nélkül;
  a negatív kritérium szerint a „föld mint talaj” általános használat, és a vers az átkot nem mondja ki, nem
  ismétli, nem fordítja meg. Az 1Móz 9:20 indoklása ugyanerre a szövegre igazodik (a döntése nem változik).
  Az elutasitasi_okok.tsv HAMART 112-es mintája az új szöveget is felismeri („elbeszélő használat”).
- K5 (DT-F182b): az 1Móz 6:5 bent marad (DT683 (E), DT685 K8); az indoklása a kivezetett רַע (ra)
  helyett a mai hordozót mondja ki, és azt, miben különbözik a Jer 17:9, Jer 4:14, Mt 15:19, Mk 7:21-23 kizárásától.
- K6 (DT-F182c): a Zsid 6:7-8 tartománya marad; az indoklása kimondja, miért kezdődik a 6:7-tel (a 6:8 mondatának
  alanya, a föld, ott áll), szemben a Róm 8:21-gyel, amely maga hordozza az alanyt és a romlás szavát.

Írás előtt a sorokat összeveti az eredetivel, és csak a megnevezett sorok változhatnak (minta:
naplok/F123_HAMART3_hatar.py, eszkozok/igazolas_migracio.py). A `csv` modult nem használja.
Futtatás a repó gyökeréből: python naplok/F182_hatar.py [--ir]"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'HAMART-001'
DATUM = '2026.11.10'

# igehely -> (elvárt régi döntés, új döntés, új indoklás, dontes_ref)
VALTOZAS = {
    '1Móz 4:2-3': ('beépítve', 'elutasítva',
                   'Semleges, elbeszélő használat: Kain „földmívelő”, és „a föld gyümölcséből” visz ajándékot az Úrnak. '
                   'Az אֲדָמָה (adámá) itt a megművelt talaj, mint a kint álló 1Móz 2:5-ben és 9:20-ban; a vers az átkot '
                   'nem mondja ki, nem ismétli és nem fordítja meg. A föld átka Kainnál a 4:10-12-ben hangzik el, '
                   'azok a versek saját sorban állnak.',
                   'DT-F182a'),
    '1Móz 9:20': ('elutasítva', 'elutasítva',
                  'Semleges, elbeszélő használat: Noé „földmívelő kezde lenni, és szőlőt ültete”. Az אֲדָמָה (adámá) '
                  'itt a megművelt talaj, mint az 1Móz 2:5-ben és 4:2-3-ban; a vers az átkot nem mondja ki, nem '
                  'ismétli és nem fordítja meg.',
                  'DT-F182a'),
    '1Móz 6:5': ('beépítve', 'beépítve',
                 'Beépítve, „tematikus, nem lexikai” jelöléssel: a lánc szavai nem állnak a versben, de a vers az '
                 '1Móz 6:7 ítéletének indoka ugyanabban az elbeszélésben, és az 1Móz 8:21 ígérete ugyanezzel az '
                 'indokkal tér vissza rá („mert az ember szívének gondolatja gonosz”). A szív hajlamáról szóló többi '
                 'hely (Jer 17:9, Jer 4:14, Mt 15:19, Mk 7:21-23) a lánc elbeszélésén kívül áll, a láncra nem utal '
                 'vissza, és a szív romlott hajlamának önálló tárgyához tartozik, ezért kint.',
                 'DT683 · DT685 · DT-F182b'),
    'Zsid 6:7-8': ('beépítve', 'beépítve',
                   'Beépítve: a föld, „a mely pedig töviseket és bojtorjánokat terem, megvetett és közel van az '
                   'átokhoz”. A görög szöveg az 1Móz 3:17-18 görög fordításának három szavát hozza együtt: γῆ (gé, '
                   'föld), ἄκανθα (akantha, tövis) és τρίβολος (tribolosz, bogáncs), mellettük a κατάρα (katara, '
                   'átok). A tartomány a 6:7-tel kezdődik, mert a 6:8 mondatának alanya, a föld (γῆ), ott áll; a '
                   'Róm 8:21 ezzel szemben maga hordozza az alanyt és a romlás szavát, ezért ott a szomszédos vers '
                   'külön sorban áll.',
                   'DT-F182c'),
}
TOROL_ELOF = ['1Móz 4:2-3']
OK_SORREND, OK_REGI, OK_UJ = '112', 'narratív adamá', 'narratív adamá|elbeszélő használat'


def beolvas(ut):
    sorok = open(ut, encoding='utf-8', newline='').read().split('\n')
    fej_i = next(i for i, l in enumerate(sorok) if l and not l.startswith('#'))
    return sorok, fej_i, sorok[fej_i].split('\t')


def kiir(ut, sorok, ir):
    if ir:
        open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))


def jeloltek(ir):
    ut = 'adat/jeloltek.tsv'
    sorok, fej_i, fej = beolvas(ut)
    ix = {k: i for i, k in enumerate(fej)}
    eredeti = list(sorok)
    valtozott, latott = set(), set()
    for n in range(fej_i + 1, len(sorok)):
        r = sorok[n].split('\t')
        if len(r) < len(fej) or r[0] != ID or r[ix['jelolt_tipus']] != 'elofordulas':
            continue
        ige = r[1]
        if ige not in VALTOZAS:
            continue
        regi, uj, ind, ref = VALTOZAS[ige]
        assert r[ix['dontes']] == regi, (ige, r[ix['dontes']])
        assert ige not in latott, ige
        r[ix['dontes']], r[ix['indoklas']] = uj, ind
        r[ix['datum']], r[ix['dontes_ref']] = DATUM, ref
        latott.add(ige)
        sorok[n] = '\t'.join(r)
        valtozott.add(n)
    assert latott == set(VALTOZAS), set(VALTOZAS) - latott
    assert len(sorok) == len(eredeti)
    elter = {i for i in range(len(eredeti)) if sorok[i] != eredeti[i]}
    assert elter == valtozott, elter ^ valtozott
    for i in sorted(elter):
        a, b = eredeti[i].split('\t'), sorok[i].split('\t')
        mezok = [fej[k] for k in range(len(fej)) if a[k] != b[k]]
        assert set(mezok) <= {'dontes', 'indoklas', 'datum', 'dontes_ref'}, mezok
        print('  %s: %s' % (b[1], ', '.join(mezok)))
    print('%s: %d sor módosítva' % (ut, len(valtozott)))
    kiir(ut, sorok, ir)


def elofordulasok(ir):
    ut = 'adat/elofordulasok.tsv'
    sorok, fej_i, fej = beolvas(ut)
    ki, torolt = [], []
    for n, l in enumerate(sorok):
        r = l.split('\t')
        if n > fej_i and len(r) >= len(fej) and r[0] == ID and r[1] in TOROL_ELOF:
            torolt.append(r[1])
            continue
        ki.append(l)
    assert sorted(torolt) == sorted(TOROL_ELOF), torolt
    assert len(ki) == len(sorok) - len(TOROL_ELOF)
    n_ham = sum(1 for l in ki if l.startswith(ID + '\t'))
    print('%s: %d sor törölve; HAMART-001: %d sor' % (ut, len(torolt), n_ham))
    kiir(ut, ki, ir)


def okok(ir):
    ut = 'adat/elutasitasi_okok.tsv'
    sorok, fej_i, fej = beolvas(ut)
    assert fej[:3] == ['sorrend', 'id', 'minta'], fej
    eredeti = list(sorok)
    talalt = 0
    for n, l in enumerate(sorok):
        r = l.split('\t')
        if r[:2] == [OK_SORREND, ID]:
            if r[2] == OK_UJ:
                print('%s: a minta már bővítve' % ut)
                return
            assert r[2] == OK_REGI, r[2]
            r[2] = OK_UJ
            sorok[n] = '\t'.join(r)
            talalt += 1
    assert talalt == 1
    assert sum(1 for a, b in zip(eredeti, sorok) if a != b) == 1
    print('%s: 1 minta bővítve (%s)' % (ut, OK_UJ))
    kiir(ut, sorok, ir)


if __name__ == '__main__':
    ir = '--ir' in sys.argv
    okok(ir)
    jeloltek(ir)
    elofordulasok(ir)
    if not ir:
        print('(próba; írás: --ir)')
