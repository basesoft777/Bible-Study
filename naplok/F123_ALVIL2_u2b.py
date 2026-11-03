# -*- coding: utf-8 -*-
"""F123 ALVIL-001 új cikk, U2 — a döntés átvezetése (az orkesztrátor döntése a felhasználó
2026-11-02-i felhatalmazásával; DT-F123o):

1. a teljesség-mérés 28 `nyitva` jelöltje `elutasítva`, indoklás-típusonként
   (szótári összevető hely · a Károli más szót fordít · a Septuaginta többlete);
2. a Károli-háló további 295 más szavas eltérése lexémánként EGY blokk-sorként
   (a DT503 blokk-kizárási mintája): a sor igehelye a blokk első verse, az indoklás a
   blokk méretét és a szót mondja ki, a teljes verslista
   `naplok/F123_teljesseg_ALVIL-001_blokkok.tsv`.
Írás előtt a nem érintett sorok bájtra egyeznek (split('\\t')); eltérésnél megáll.
"""
import io
import os
import sys
from collections import OrderedDict, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L  # noqa: E402

DATUM, TS = '2026.11.02', '2026-11-02'
DONTES = ' Döntés: elutasítva, mert a versben a seól, illetve a hádész szava nem áll.'

SZOTAR = {'Jób 3:17', 'Jób 10:21', 'Jób 14:21', 'Jób 16:22', 'Jób 19:25', 'Jób 21:23', 'Jób 26:5', 'Jób 38:17',
          'Jón 2:7', 'Préd 9:7', 'Zsolt 16:11', 'Zsolt 17:15', 'Zsolt 73:23', 'Zsolt 73:25', 'Zsolt 88:5',
          'Ézs 26:19', 'Ézs 57:1', 'ApCsel 2:24'}
KAROLI = {'Jób 28:22', 'Jób 31:12', '2Pét 2:4'}
LXX = {'Jób 33:22', 'Péld 2:18', 'Péld 14:12', 'Péld 16:25', 'Zsolt 94:17', 'Zsolt 115:17', 'Ézs 14:19'}
ELO = {'szotar': 'Szótári összevető hely: a szótár a seól, illetve a hádész szócikkében idézi a verset, de a szó nem áll benne.',
       'karoli': 'A Károli itt más szót fordít pokolnak vagy mélységnek.',
       'lxx': 'A Septuaginta többlete: a görög fordítás ᾍδης (hadész) szót hoz, a héber szövegben viszont nincs seól.'}

# a blokkok sorrendje = elsőbbség: a vers az első olyan blokkba kerül, amelynek Strongja áll benne
BLOKK = OrderedDict([
    ('tehom', dict(strong={'H8415', 'G0012'}, karoli_szo='mélység',
                   szoveg='a kozmikus mélység, a תְּהוֹם (tehóm) és az ἄβυσσος (abüsszosz), amelyet a Károli mélységnek fordít')),
    ('verem', dict(strong={'H0953', 'H7845'}, karoli_szo='sír, mélység',
                   szoveg='a verem, a בּוֹר (bór) és a שַׁחַת (sahat), amelyet a Károli sírnak, sírgödörnek vagy mélységnek fordít')),
    ('temetkezes', dict(strong={'H6913', 'H6900', 'H6912', 'G3419', 'G3418', 'G5028'}, karoli_szo='sír, koporsó',
                        szoveg='a temetkezési sír, a קֶבֶר (kever) és a μνημεῖον (mnémeion), amelyet a Károli sírnak vagy koporsónak fordít')),
    ('siras', dict(strong={'H1058', 'H1065', 'H5594', 'H4553', 'H1832', 'H3213', 'H0056', 'G2799', 'G2805', 'G3996'},
                   karoli_szo='sír (ige)',
                   szoveg='a sírás, a בָּכָה (bákhá) és a κλαίω (klaió) igéje, amelyet a Károli sír igével fordít')),
    ('egyeb', dict(strong=None, karoli_szo='mélység, sír',
                   szoveg='más szavak fordítása: a tenger, a völgy és Isten gondolatainak mélysége, a siratás és a siratóének, valamint a sír és a koporsó szó egyéb előfordulásai')),
])


def nyit(ut):
    nyers = io.open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    return nyers.split(nl), nl


def main():
    # a blokkok
    tok = defaultdict(set)
    for r in list(L.load_tahot()) + list(L.load_tagnt()):
        tok[r['Igehely']].add(r['Strong-szám'])
    be = os.path.join(GY, 'naplok', 'F123_teljesseg_ALVIL-001.tsv')
    versek = []
    for s in io.open(be, encoding='utf-8'):
        m = s.rstrip('\n').split('\t')
        if m[0] == 'karoli' and len(m) > 2 and m[2] == 'ELTÉRÉS' and m[1] not in KAROLI:
            versek.append((m[1], m[4]))
    assert len(versek) == 295, len(versek)
    blokk_versek = defaultdict(list)
    for v, szo in versek:
        nev = next(k for k, b in BLOKK.items() if b['strong'] is None or tok.get(v, set()) & b['strong'])
        blokk_versek[nev].append((v, szo))
    ki = os.path.join(GY, 'naplok', 'F123_teljesseg_ALVIL-001_blokkok.tsv')
    with open(ki, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# F123 ALVIL-001 U2: a Károli-háló 295 más szavas eltérése lexémánként (naplok/F123_ALVIL2_u2b.py; DT-F123o) | '
                'scope=naplok/F123_teljesseg_ALVIL-001.tsv karoli ELTÉRÉS (a Jób 28:22, 31:12 és a 2Pét 2:4 nélkül) × '
                'TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | forras=split(\'\\t\') | ts=%s\n' % TS)
        f.write('blokk\tigehely\tkaroli_szoalak\n')
        for nev in BLOKK:
            for v, szo in sorted(blokk_versek[nev], key=lambda x: L.parse_igehely(x[0])):
                f.write('%s\t%s\t%s\n' % (nev, v, szo))

    ut = os.path.join(GY, 'adat', 'jeloltek.tsv')
    sorok, nl = nyit(ut)
    fi = next(i for i, s in enumerate(sorok) if s.startswith('id\t'))
    ix = {n: j for j, n in enumerate(sorok[fi].split('\t'))}
    uj, erintett, kulcsok = list(sorok), set(), set()
    for k, s in enumerate(sorok):
        m = s.split('\t')
        if k <= fi or m[0] != 'ALVIL-001':
            continue
        kulcsok.add(m[ix['igehely']])
        if m[ix['dontes']] != 'nyitva' or m[ix['jelolt_tipus']] != 'elofordulas':
            continue
        ige = m[ix['igehely']]
        tip = 'szotar' if ige in SZOTAR else 'karoli' if ige in KAROLI else 'lxx' if ige in LXX else None
        assert tip, ige
        regi = m[ix['indoklas']]
        assert regi.startswith('Döntésre vár. A versben: '), regi
        m[ix['dontes']] = 'elutasítva'
        m[ix['indoklas']] = ELO[tip] + ' A versben: ' + regi[len('Döntésre vár. A versben: '):] + DONTES
        if ige == 'Jób 38:17':
            m[ix['indoklas']] += ' A Septuaginta itt is ᾍδης (hadész) szót hoz.'
        uj[k] = '\t'.join(m)
        erintett.add(k)
    assert len(erintett) == 28, len(erintett)
    a = [s for k, s in enumerate(sorok) if k not in erintett]
    b = [s for k, s in enumerate(uj) if k not in erintett]
    if a != b:
        sys.exit('ELTÉRÉS a nem érintett sorokban — nem írok')
    hozza = []
    for nev, d in BLOKK.items():
        lst = sorted(blokk_versek[nev], key=lambda x: L.parse_igehely(x[0]))
        if not lst:
            continue
        elso = lst[0][0]
        assert elso not in kulcsok, elso
        r = [''] * len(ix)
        r[ix['id']] = 'ALVIL-001'
        r[ix['igehely']] = elso
        r[ix['forras_kereses']] = ('F123 U1 teljesség-mérés, Károli-szó háló, blokk-kizárás (DT-F123o): %d vers, az első itt; '
                                   'a lista: naplok/F123_teljesseg_ALVIL-001_blokkok.tsv (blokk=%s), naplok/F123_teljesseg_ALVIL-001.md | '
                                   'scope=manual | forras=eszkozok/teljesseg_meres.py, naplok/F123_ALVIL2_u2b.py | ts=%s' % (len(lst), nev, TS))
        r[ix['dontes']] = 'elutasítva'
        r[ix['indoklas']] = ('Összesítő sor %d versre (az első itt áll): a Károli-szó ezekben a versekben %s. '
                             'A versekben a seól, illetve a hádész szava nem áll, ezért egyik sem tartozik a motívumhoz; '
                             'a teljes lista a lap készítőinek módszertani naplójában.' % (len(lst), d['szoveg']))
        r[ix['karoli_szo']] = d['karoli_szo']
        r[ix['datum']] = DATUM
        r[ix['jelolt_tipus']] = 'elofordulas'
        hozza.append('\t'.join(r))
    utolso = max(i for i, s in enumerate(uj) if s.startswith('ALVIL-001\t'))
    uj = uj[:utolso + 1] + hozza + uj[utolso + 1:]
    io.open(ut, 'w', encoding='utf-8', newline='').write(nl.join(uj))
    print('28 elutasítva; blokkok:', ', '.join('%s %d' % (n, len(blokk_versek[n])) for n in BLOKK))


if __name__ == '__main__':
    main()
