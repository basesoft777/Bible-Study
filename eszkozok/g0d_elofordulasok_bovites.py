#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
g0d_elofordulasok_bovites.py -- F4 G0/d: ket uj mezo felvetele az elofordulasok.tsv-be
(fo_elofordulas, felmerult_tanulmany), es a pardes_szint mezo 14 "Pshat" ertekenek
javitasa "Peshat"-ra.

Miert csoportkulcs a fo_elofordulas, nem igen/nem: a naplo (PaRDeS_motivumok.md)
tobbszor egyetlen "fo elofordulaskent" nevez meg egy verskozt vagy verspart
(pl. 1Moz 6:1-4, 2Moz 15:5,8, Luk 1:46-47, 1Kor 2:14-15), miközben az
elofordulasok.tsv ezt kulon sorokra bontva tarolja. A mezo erteke a naplo sajat
megnevezese szo szerint; ures = nem tartozik fo elofordulashoz. A kuszob ezutan
COUNT(DISTINCT fo_elofordulas) ID-nkent, nem sorszamlalas -- l. a chat-menet
2026.09.15-i dontese (D10 modositasa).

A felmerult_tanulmany mezo a study-k "1. Elofordulasok osszegyujtese" tablazatanak
3. oszlopabol jon ("PaRDeS-szint, ahol felmerult"), ahol az a tablazat letezik.
Mechanikus szabaly, nem tartalmi itelet: a 3. oszlop szovegebol a PaRDeS-szint
utani resz (elso "--" vagy zarojel utan) kerul at, tovabbi ertelmezes nelkul; ha
a 3. oszlop csak a szintet ismetli, a mezo ures marad. Harom ID-nel (KIRALY-001,
ISTENTISZT-001, HODIT-001) a study tablazata nem tartalmaz ilyen oszlopot --
ezeknel a mezo minden soron ures.

I/O -- FONTOS: sima split('\\t') / '\\t'.join(), NEM a csv modul (CLAUDE.md,
"TSV-olvasas" szakasz). Iras elott bajt-szintu korut-ellenorzes: minden mar
letezo mezo (a pardes_szint 14 sora kivetelevel) valtozatlan kell maradjon.

Futtatas a repo gyokerebol:
    python eszkozok/g0d_elofordulasok_bovites.py            # szarazon, csak jelent
    python eszkozok/g0d_elofordulasok_bovites.py --ir       # tenylegesen ir
"""

import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(ROOT, 'adat', 'elofordulasok.tsv')

# --- Pshat -> Peshat: 14 sor, id+igehely kulccsal azonositva (nem sorszammal,
# hogy a szkript akkor is helyesen talaljon rájuk, ha a fajl sorrendje valaha
# valtozik). ---
PSHAT_JAVITANDO = {
    ('KIRALY-001', '1Móz 14:18-20'),
    ('TEREMT-001', '1Móz 1:2'),
    ('TEREMT-001', 'Lukács 8:31'),
    ('ALVIL-001', 'Zsolt 16:10'),
    ('ALVIL-001', 'ApCsel 2:27'),
    ('ALVIL-001', 'ApCsel 2:31'),
    ('ALVIL-001', 'Lukács 16:23'),
    ('ALVIL-001', 'Jelenések 6:8'),
    ('MENNY-001', '1Móz 6:2'),
    ('MENNY-001', '1Móz 6:4'),
    ('ANTROP-001', '1Thessz 5:23'),
    ('ANTROP-001', 'Zsid 4:12'),
    ('ANTROP-001', 'Luk 1:46'),
    ('ANTROP-001', 'Luk 1:47'),
}

# --- fo_elofordulas: (id, igehely) -> csoportkulcs (a naplo sajat megnevezese).
# Forras: PaRDeS_motivumok.md Kulcsszo-index + a hét ID sajat "### ..." reszletes
# bejegyzese + a Lezart_tematikus_tanulmanyok_index.md. A 2026.09.15-i chat-döntés
# szerinti vegleges lista (ALVIL-001: a naplo csillag-szakasza az iranyado, 6 tag,
# Jel 1:18-cal egyutt -- az index sajat listaja hianyos, l. NYITOTT_FELADATOK.md). ---
FO_ELOFORDULAS = {
    # TEREMT-001 -- 5 csoport, 6 sor (Tehom_tematikus.md 1. pont)
    ('TEREMT-001', '1Móz 1:2'): '1Móz 1:2',
    ('TEREMT-001', '1Móz 7:11'): '1Móz 7:11',
    ('TEREMT-001', '1Móz 8:2'): '1Móz 8:2',
    ('TEREMT-001', '1Móz 49:25'): '1Móz 49:25',
    ('TEREMT-001', '2Móz 15:5'): '2Móz 15:5,8',
    ('TEREMT-001', '2Móz 15:8'): '2Móz 15:5,8',
    # ALVIL-001 -- 6 csoport, 9 sor (naplo ⭐-szakasz, 145. sor)
    ('ALVIL-001', 'Zsolt 16:10'): 'Zsolt 16:10 ⇒ ApCsel 2:27,31',
    ('ALVIL-001', 'ApCsel 2:27'): 'Zsolt 16:10 ⇒ ApCsel 2:27,31',
    ('ALVIL-001', 'ApCsel 2:31'): 'Zsolt 16:10 ⇒ ApCsel 2:27,31',
    ('ALVIL-001', 'Lukács 16:23'): 'Luk 16:23',
    ('ALVIL-001', 'Jelenések 1:18'): 'Jel 1:18',
    ('ALVIL-001', 'Jelenések 6:8'): 'Jel 6:8',
    ('ALVIL-001', 'Lukács 10:15'): 'Luk 10:15/Mát 11:23',
    ('ALVIL-001', 'Máté 11:23'): 'Luk 10:15/Mát 11:23',
    ('ALVIL-001', 'Jelenések 20:13-14'): 'Jel 20:13-14',
    # ISTENTISZT-001 -- 5 csoport, 5 sor (genezisi gerinc)
    ('ISTENTISZT-001', '1Móz 4:26'): '1Móz 4:26',
    ('ISTENTISZT-001', '1Móz 12:8'): '1Móz 12:8',
    ('ISTENTISZT-001', '1Móz 13:4'): '1Móz 13:4',
    ('ISTENTISZT-001', '1Móz 21:33'): '1Móz 21:33',
    ('ISTENTISZT-001', '1Móz 26:25'): '1Móz 26:25',
    # HODIT-001 -- 1 csoport, 1 sor
    ('HODIT-001', '1Móz 14:5'): '1Móz 14:5',
    # KIRALY-001 -- 1 csoport, 1 sor
    ('KIRALY-001', '1Móz 14:18-20'): '1Móz 14:18-20',
    # MENNY-001 -- 1 csoport, 2 sor (4Móz 13:34 NEM fo elofordulas)
    ('MENNY-001', '1Móz 6:2'): '1Móz 6:1-4',
    ('MENNY-001', '1Móz 6:4'): '1Móz 6:1-4',
    # ANTROP-001 -- 5 csoport, 8 sor
    ('ANTROP-001', '1Thessz 5:23'): '1Thessz 5:23',
    ('ANTROP-001', 'Zsid 4:12'): 'Zsid 4:12',
    ('ANTROP-001', '1Móz 2:7'): '1Móz 2:7 ⇒ 1Kor 15:45',
    ('ANTROP-001', '1Kor 15:45'): '1Móz 2:7 ⇒ 1Kor 15:45',
    ('ANTROP-001', 'Luk 1:46'): 'Luk 1:46-47',
    ('ANTROP-001', 'Luk 1:47'): 'Luk 1:46-47',
    ('ANTROP-001', '1Kor 2:14'): '1Kor 2:14-15',
    ('ANTROP-001', '1Kor 2:15'): '1Kor 2:14-15',
}

# ID-nkent a naplo altal kimondott csoportszam -- onellenorzeshez.
FO_ELOFORDULAS_VART_CSOPORTSZAM = {
    'TEREMT-001': 5,
    'ALVIL-001': 6,
    'ISTENTISZT-001': 5,
    'HODIT-001': 1,
    'KIRALY-001': 1,
    'MENNY-001': 1,
    'ANTROP-001': 5,
}

# --- felmerult_tanulmany: (id, igehely) -> szoveg. Csak ott, ahol a study 1.
# pontjanak tablazata tartalmaz "PaRDeS-szint, ahol felmerult" oszlopot ES az
# a szint utani resz nem ures. ---
FELMERULT_TANULMANY = {
    # Tehom_tematikus.md 1. pont
    ('TEREMT-001', '1Móz 1:2'): '1Mózes 1 bővített tanulmány',
    ('TEREMT-001', '1Móz 7:11'): '1Mózes 7:1–24 bővített tanulmány',
    ('TEREMT-001', '1Móz 8:2'): '1Mózes 7:1–24 bővített tanulmány (kereszthivatkozásként)',
    ('TEREMT-001', '1Móz 49:25'): 'jelen tanulmány',
    ('TEREMT-001', '2Móz 15:5'): 'jelen tanulmány',
    ('TEREMT-001', '2Móz 15:8'): 'jelen tanulmány',
    # Hadesz_Seol_tematikus.md 1. pont -- csak azok a sorok, ahol a 3. oszlop a
    # szinten tul mas szoveget is tartalmaz
    ('ALVIL-001', 'Jelenések 6:8'):
        'a Halál+Hádész páros első megjelenése, amely a 20:13-14-es végső '
        '„kiadja halottait” jelenetben teljesedik be',
    ('ALVIL-001', 'Lukács 10:15'): 'második, önálló hádész-használati mintázat, ld. lent',
    ('ALVIL-001', 'Máté 11:23'): 'második, önálló hádész-használati mintázat, ld. lent',
    # Isten_fiai_Nefilim_Gibborim_tematikus.md 1. pont
    ('MENNY-001', '1Móz 6:2'): '1Móz 6:1-8 tanulmány',
    ('MENNY-001', '1Móz 6:4'): '1Móz 6:1-8 tanulmány',
    ('MENNY-001', 'Jób 1:6'): 'jelen tanulmányban felvéve, korábban nem feldolgozva',
    ('MENNY-001', 'Jób 2:1'): 'jelen tanulmányban felvéve',
    ('MENNY-001', 'Jób 38:7'): 'jelen tanulmányban felvéve',
    ('MENNY-001', '4Móz 13:34'): 'napló-alpontból, jelen tanulmányban kifejtve',
    ('MENNY-001', 'Júd 1:6'): 'ÚSZ, korábban jelzett kereszthivatkozás',
    ('MENNY-001', 'Júd 1:14-15'): 'ÚSZ, jelen tanulmányban pontosítva',
    ('MENNY-001', '2Pét 2:4-5'): 'ÚSZ, korábban jelzett kereszthivatkozás, jelen tanulmányban pontosítva',
    # Pneuma_pszukhe_megkulonboztetes_tematikus.md 1. pont
    ('ANTROP-001', '1Thessz 5:23'): 'saját bővített tanulmány',
    ('ANTROP-001', 'Zsid 4:12'): 'saját bővített tanulmány',
    ('ANTROP-001', '1Móz 2:7'): 'keresztutalás az 1Móz 2:4-7 tanulmányból',
    ('ANTROP-001', '1Kor 15:45'): 'keresztutalás az 1Móz 2:4-7 tanulmányból',
    ('ANTROP-001', 'Luk 1:46'): 'negyedik, valódi lexikai előfordulás',
    ('ANTROP-001', 'Luk 1:47'): 'negyedik, valódi lexikai előfordulás',
    ('ANTROP-001', '1Kor 2:14'): 'ötödik előfordulás, melléknévi alakban',
    ('ANTROP-001', '1Kor 2:15'): 'ötödik előfordulás, melléknévi alakban',
    # KIRALY-001, ISTENTISZT-001, HODIT-001: a study tablazata nem tartalmaz
    # ilyen oszlopot -- nincs bejegyzes, minden sor ures marad.
}


def main():
    ir = '--ir' in sys.argv

    with io.open(TABLA, encoding='utf-8', newline='') as f:
        nyers = f.read()

    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    vege_ujsor = nyers.endswith(sorveg)
    sorok = nyers.split(sorveg)
    if vege_ujsor:
        sorok = sorok[:-1]

    fejlec_idx = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fejlec = sorok[fejlec_idx].split('\t')

    if 'fo_elofordulas' in fejlec:
        print('A bővítés már lefutott (a fo_elofordulas oszlop létezik). Nincs teendő.')
        return 0

    i_id = fejlec.index('id')
    i_igehely = fejlec.index('igehely')
    i_pardes = fejlec.index('pardes_szint')

    hibak = []
    kimenet = list(sorok[:fejlec_idx])
    kimenet.append('\t'.join(fejlec + ['fo_elofordulas', 'felmerult_tanulmany']))

    pshat_talalt = set()
    fo_talalt = set()
    felmerult_talalt = set()
    fo_szamlalo = {}

    for sorszam, nyers_sor in enumerate(sorok[fejlec_idx + 1:], start=fejlec_idx + 2):
        if not nyers_sor.strip() or nyers_sor.startswith('#'):
            kimenet.append(nyers_sor)
            continue

        mezok = nyers_sor.split('\t')
        if len(mezok) != len(fejlec):
            hibak.append('%d. sor: %d oszlop %d helyett' % (sorszam, len(mezok), len(fejlec)))
            continue

        kulcs = (mezok[i_id], mezok[i_igehely])

        # Pshat -> Peshat
        eredeti_pardes = mezok[i_pardes]
        if kulcs in PSHAT_JAVITANDO:
            if 'Pshat' not in eredeti_pardes:
                hibak.append('%d. sor: %s/%s a javítandó listában, de nincs benne "Pshat" (%r)'
                              % (sorszam, kulcs[0], kulcs[1], eredeti_pardes))
                continue
            uj_pardes = eredeti_pardes.replace('Pshat', 'Peshat')
            pshat_talalt.add(kulcs)
        else:
            if 'Pshat' in eredeti_pardes:
                hibak.append('%d. sor: %s/%s "Pshat"-ot tartalmaz, de nincs a javítandó listában (%r)'
                              % (sorszam, kulcs[0], kulcs[1], eredeti_pardes))
                continue
            uj_pardes = eredeti_pardes
        mezok[i_pardes] = uj_pardes

        fo = FO_ELOFORDULAS.get(kulcs, '')
        if fo:
            fo_talalt.add(kulcs)
            fo_szamlalo.setdefault(kulcs[0], set()).add(fo)

        felmerult = FELMERULT_TANULMANY.get(kulcs, '')
        if felmerult:
            felmerult_talalt.add(kulcs)

        kimenet.append('\t'.join(mezok + [fo, felmerult]))

    # onellenorzes: minden bejegyzett kulcs tenylegesen elo is fordult a tablaban
    hianyzo_pshat = PSHAT_JAVITANDO - pshat_talalt
    hianyzo_fo = set(FO_ELOFORDULAS) - fo_talalt
    hianyzo_felmerult = set(FELMERULT_TANULMANY) - felmerult_talalt
    for kulcs in sorted(hianyzo_pshat):
        hibak.append('PSHAT_JAVITANDO kulcs nem található a táblában: %r' % (kulcs,))
    for kulcs in sorted(hianyzo_fo):
        hibak.append('FO_ELOFORDULAS kulcs nem található a táblában: %r' % (kulcs,))
    for kulcs in sorted(hianyzo_felmerult):
        hibak.append('FELMERULT_TANULMANY kulcs nem található a táblában: %r' % (kulcs,))

    for azon, csoportok in fo_szamlalo.items():
        vart = FO_ELOFORDULAS_VART_CSOPORTSZAM.get(azon)
        if vart is not None and len(csoportok) != vart:
            hibak.append('%s: %d distinct fo_elofordulas csoport, %d helyett'
                          % (azon, len(csoportok), vart))

    print('Sorok: %d' % (len(sorok) - fejlec_idx - 1))
    print('Pshat -> Peshat javítva: %d sor' % len(pshat_talalt))
    print('fo_elofordulas kitöltve: %d sor' % len(fo_talalt))
    for azon in sorted(fo_szamlalo):
        print('  %-16s %2d sor / %2d distinct csoport' % (azon, sum(1 for k in FO_ELOFORDULAS if k[0] == azon), len(fo_szamlalo[azon])))
    print('felmerult_tanulmany kitöltve: %d sor' % len(felmerult_talalt))

    if hibak:
        print('\nHIBA (%d) -- nem írtam semmit:' % len(hibak))
        for h in hibak[:30]:
            print('  ' + h)
        return 1

    # bajthusseg-proba: minden mezo valtozatlan, a pardes_szint (csak a 14
    # javitott soron) es a ket uj oszlop kivetelevel
    ellenorzott = 0
    for eredeti, uj in zip(sorok[fejlec_idx + 1:], kimenet[fejlec_idx + 1:]):
        if not eredeti.strip() or eredeti.startswith('#'):
            continue
        a = eredeti.split('\t')
        b = uj.split('\t')[:-2]
        kulcs = (a[i_id], a[i_igehely])
        for oszlop, (x, y) in enumerate(zip(a, b)):
            if oszlop == i_pardes and kulcs in PSHAT_JAVITANDO:
                if y != x.replace('Pshat', 'Peshat'):
                    hibak.append('bájthűség sérült a(z) %s oszlopban (%r)' % (fejlec[oszlop], kulcs))
                continue
            if x != y:
                hibak.append('bájthűség sérült a(z) %s oszlopban (%r)' % (fejlec[oszlop], kulcs))
        ellenorzott += 1

    if hibak:
        print('\nHIBA -- nem írtam semmit:')
        for h in hibak[:30]:
            print('  ' + h)
        return 1

    print('\nHiba nincs. Bájthűség ellenőrizve %d soron.' % ellenorzott)
    if not ir:
        print('Szárazon futott. Tényleges íráshoz: --ir')
        return 0

    with io.open(TABLA, 'w', encoding='utf-8', newline='') as f:
        f.write(sorveg.join(kimenet) + (sorveg if vege_ujsor else ''))
    print('Megírva: adat/elofordulasok.tsv')
    return 0


if __name__ == '__main__':
    sys.exit(main())
