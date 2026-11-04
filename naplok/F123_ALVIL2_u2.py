# -*- coding: utf-8 -*-
"""F123 ALVIL-001 új cikk, U2 — a döntések átvezetése a `jeloltek.tsv`-ben (2. szabály).

1. A két határdöntés (a felhasználó, 2026-11-02, DT-F123b): az Mt 16:18 és az 1Kor 15:55
   jelöltsora `elutasítva` → `beépítve`, olvasói nyelvű indoklással.
2. A teljesség-mérés (DT548, `naplok/F123_teljesseg_ALVIL-001.md`) 28 új jelöltje `nyitva`
   sorként, a háló nevével (a döntés a válasz után, külön lépésben).
Írás előtt minden nem érintett sor bájtra egyezik (split('\\t'), CLAUDE.md); eltérésnél megáll.
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UT = os.path.join(GY, 'adat', 'jeloltek.tsv')
DATUM = '2026.11.02'
TS = '2026-11-02'

HATAR = {
    'Mt 16:18': dict(
        indoklas=('A vers a ᾍδης szót hordozza („a pokol kapui”), ezért a motívumhoz tartozik: a határt a szó húzza meg. '
                  'A funkciója más, mint a halál-szövegeké: itt a halál hatalma az egyház ellen áll, és nem győz rajta.'),
        karoli_szo='a pokol kapui'),
    '1Kor 15:55': dict(
        indoklas=('A Károli alapszövegében (Textus Receptus) a második felkiáltás a ᾍδης-t szólítja meg („Pokol! hol a te diadalmad?”), '
                  'ezért a motívumhoz tartozik. A kritikai szövegkiadások itt mindkét tagban θάνατε-t (halál) olvasnak; a lap ezt jelöli.'),
        karoli_szo='Pokol!'),
}
HATAR_FORRAS = ('a felhasználó határdöntése, 2026-11-02 (Kiadó-kártya: hatar:ALVIL-001:{k}; az orkesztrátor jegyzete, '
                'side-session-notes F123_UJ_CIKK_brief_bemenet.md) | scope=manual | forras=F123 ALVIL-001 új cikk, U2 | ts=' + TS)

TELJ = 'naplok/F123_teljesseg_ALVIL-001.md'
UJ = [
    # (igehely, háló, karoli_szo, mi áll a versben)
    ('Jób 3:17', 'szótár (BDB H7585 sorszam 60)', '', 'a halottak helyének leírása („Ott a gonoszok megszünnek…”), a seól szava nélkül'),
    ('Jób 10:21', 'szótár (BDB H7585 sorszam 58, 89; Thayer G0086 sorszam 2)', '', '„a sötétségnek és a halál árnyékának földébe” — a seól szava nélkül'),
    ('Jób 14:21', 'szótár (BDB H7585 sorszam 64)', '', 'a halott nem tud fiai sorsáról — a seól szava nélkül'),
    ('Jób 16:22', 'szótár (BDB H7585 sorszam 59)', 'a sír', '„vár rám a sír” — a Károli „sír”-ja itt nem a seól fordítása'),
    ('Jób 19:25', 'szótár (BDB H7585 sorszam 90)', '', '„az én megváltóm él” — a seól szava nélkül'),
    ('Jób 21:23', 'szótár (BDB H7585 sorszam 61)', '', '„Ez meghal…” — a seól szava nélkül'),
    ('Jób 26:5', 'szótár (BDB H7585 sorszam 35)', '', '„A halottak is megremegnek” (רְפָאִים, refáím) — a seól szava nélkül'),
    ('Jób 38:17', 'szótár (Thayer G0086 sorszam 11) és LXX-többlet', '', '„a halálnak kapui”; a Septuaginta itt ᾅδης-t hoz, a héber szöveg nem seólt'),
    ('Jón 2:7', 'szótár (BDB H7585 sorszam 37)', '', '„bezáródtak a föld závárjai” — a seól szava nélkül'),
    ('Préd 9:7', 'szótár (BDB H7585 sorszam 62; a BDB-ben Préd 9:5)', '', '„a halottak semmit nem tudnak” — a seól szava nélkül'),
    ('Zsolt 16:11', 'szótár (BDB H7585 sorszam 81)', '', 'a remény a halálon túl — a seól szava nélkül'),
    ('Zsolt 17:15', 'szótár (BDB H7585 sorszam 82)', '', 'a remény a halálon túl — a seól szava nélkül'),
    ('Zsolt 73:23', 'szótár (BDB H7585 sorszam 84)', '', 'a remény a halálon túl — a seól szava nélkül'),
    ('Zsolt 73:25', 'szótár (BDB H7585 sorszam 85)', '', 'a remény a halálon túl — a seól szava nélkül'),
    ('Zsolt 88:5', 'szótár (BDB H7585 sorszam 71)', 'a sírba', '„a sírba szállókhoz” — a héberben בּוֹר (bór, verem), nem seól'),
    ('Ézs 26:19', 'szótár (BDB H7585 sorszam 96)', '', '„visszaadja a föld az árnyakat” — a seól szava nélkül'),
    ('Ézs 57:1', 'szótár (BDB H7585 sorszam 86)', '', '„az igaz elvész” — a seól szava nélkül'),
    ('ApCsel 2:24', 'szótár (Thayer G0086 sorszam 14)', '', '„a halál fájdalmait” — a Károli alapszövegében θανάτου, a ᾅδου csak szövegváltozat'),
    ('Jób 28:22', 'Károli-szó (pokol)', 'A pokol', '„A pokol és halál” — a héberben אֲבַדּוֹן (abaddón), nem seól'),
    ('Jób 31:12', 'Károli-szó (pokol)', 'pokolig', '„pokolig emésztene” — a héberben אֲבַדּוֹן (abaddón), nem seól'),
    ('2Pét 2:4', 'Károli-szó (mélység)', 'mélységbe', '„mélységbe taszítván” — a görögben ταρταρόω (tartaroó), nem ᾍδης'),
    ('Jób 33:22', 'LXX-többlet', 'a sírhoz', '„közelget a sírhoz” — a héberben שַׁחַת (sahat); a Septuaginta ᾅδης-t hoz'),
    ('Péld 2:18', 'LXX-többlet', '', '„a halálra hanyatlik” — a héberben nincs seól; a Septuaginta ᾅδης-t hoz'),
    ('Péld 14:12', 'LXX-többlet', '', '„vége a halálra menő út” — a héberben nincs seól; a Septuaginta ᾅδης-t hoz'),
    ('Péld 16:25', 'LXX-többlet', '', '„vége a halálnak úta” — a héberben nincs seól; a Septuaginta ᾅδης-t hoz'),
    ('Zsolt 94:17', 'LXX-többlet', '', '„ott lakoznék lelkem a csendességben” — a héberben nincs seól; a Septuaginta ᾅδης-t hoz'),
    ('Zsolt 115:17', 'LXX-többlet', '', '„a kik alászállanak a csendességbe” — a héberben nincs seól; a Septuaginta ᾅδης-t hoz'),
    ('Ézs 14:19', 'LXX-többlet', '', '„messze vettetel sírodtól” — a héberben nincs seól; a Septuaginta ᾅδης-t hoz'),
]


def main():
    nyers = io.open(UT, encoding='utf-8', newline='').read()
    vegzodes = '\r\n' if '\r\n' in nyers else '\n'
    sorok = nyers.split(vegzodes)
    fej_i = next(i for i, s in enumerate(sorok) if s.startswith('id\t'))
    fej = sorok[fej_i].split('\t')
    ix = {k: i for i, k in enumerate(fej)}
    meglevo = set()
    valt = 0
    uj_sorok = []
    for i, s in enumerate(sorok):
        if i > fej_i and s:
            m = s.split('\t')
            if m[ix['id']] == 'ALVIL-001':
                meglevo.add((m[ix['igehely']], m[ix['jelolt_tipus']]))
            if m[ix['id']] == 'ALVIL-001' and m[ix['igehely']] in HATAR and m[ix['jelolt_tipus']] == 'elofordulas':
                h = HATAR[m[ix['igehely']]]
                assert m[ix['dontes']] == 'elutasítva', m
                m[ix['dontes']] = 'beépítve'
                m[ix['indoklas']] = h['indoklas']
                m[ix['karoli_szo']] = h['karoli_szo']
                m[ix['azonositas_modja']] = 'tartalom-alapú'
                m[ix['megbizhatosag']] = 'magas'
                m[ix['forras_kereses']] = (m[ix['forras_kereses']] + ' · ' +
                                           HATAR_FORRAS.format(k='mK1' if m[ix['igehely']] == 'Mt 16:18' else 'mK2'))
                m[ix['datum']] = DATUM
                s = '\t'.join(m)
                valt += 1
        uj_sorok.append(s)
    assert valt == 2, valt
    hozza = []
    for ige, halo, ksz, mi in UJ:
        assert (ige, 'elofordulas') not in meglevo, ige
        r = [''] * len(fej)
        r[ix['id']] = 'ALVIL-001'
        r[ix['igehely']] = ige
        r[ix['forras_kereses']] = ('F123 U1 teljesség-mérés, %s háló (%s) | scope=manual | forras=eszkozok/teljesseg_meres.py, '
                                   'naplok/F123_ALVIL2_lxx_hid.py | ts=%s' % (halo, TELJ, TS))
        r[ix['dontes']] = 'nyitva'
        r[ix['indoklas']] = 'Döntésre vár. A versben: ' + mi + '.'
        r[ix['karoli_szo']] = ksz
        r[ix['datum']] = DATUM
        r[ix['jelolt_tipus']] = 'elofordulas'
        hozza.append('\t'.join(r))
    # a beszúrás az ALVIL-001 utolsó sora után
    utolso = max(i for i, s in enumerate(uj_sorok) if s.startswith('ALVIL-001\t'))
    uj_sorok = uj_sorok[:utolso + 1] + hozza + uj_sorok[utolso + 1:]
    # kontroll: a nem érintett sorok változatlanok
    regi_tobbi = [s for s in sorok if not (s.startswith('ALVIL-001\tMt 16:18\t') or s.startswith('ALVIL-001\t1Kor 15:55\t'))]
    uj_tobbi = [s for s in uj_sorok if s not in hozza and not (s.startswith('ALVIL-001\tMt 16:18\t') or s.startswith('ALVIL-001\t1Kor 15:55\t'))]
    if regi_tobbi != uj_tobbi:
        sys.exit('ELTÉRÉS a nem érintett sorokban — nem írok')
    io.open(UT, 'w', encoding='utf-8', newline='').write(vegzodes.join(uj_sorok))
    print('kész: 2 határsor átvezetve, %d új nyitva sor' % len(hozza))


if __name__ == '__main__':
    main()
