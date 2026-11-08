# -*- coding: utf-8 -*-
"""F123 HAMART-001, határkör (2026-11-08): a független határ-ellenőrzés (naplok/HATAR_HAMART-001.md, K1–K10) elfogadott
döntései a jeloltek.tsv-n át (DT28; a felhasználó: „Igen, előbb határ”, „Elfogadom”). Helyőrző: DT-F123hc.

- 11 beépített sor elutasítva, és kikerül az elofordulasok.tsv-ből: 1Móz 9:25 (K6), Jer 51:25 (K1), Mal 3:11 (K2),
  Hab 2:8, Hab 2:17, Jón 3:8 (K3), Jer 17:5 (K4), 5Móz 27:15-26 (K7), Mt 15:19, Mk 7:21-23 (K8), 2Pét 3:6-7 (K9);
- szűkítve: 5Móz 28:16-19 → 5Móz 28:18 (K7: árar + adamá), Róm 8:20-22 → Róm 8:21 (K10); a kimaradt versek saját,
  elutasított sort kapnak (5Móz 28:16-17, 5Móz 28:19; Róm 8:20, Róm 8:22);
- marad, új indoklással: 1Móz 12:3 (K5: a határ az árar és az adamá együttállása);
- a Jel 19:2 sora a Jer 51:25 helyett a saját „megrontotta a földet” alakjára hivatkozik;
- új elutasítási ok: „szövetségi átok-formula, a föld szava nélkül” (5Móz 27–28).

A Gal 3:10 és a Gal 3:13 nem változik: a felhasználó dönt (⛔).

Írás előtt a sorokat összeveti az eredetivel, és csak a megnevezett sorok változhatnak (minta: eszkozok/igazolas_migracio.py).
Futtatás a repó gyökeréből: python naplok/F123_HAMART3_hatar.py [--ir]"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ID = 'HAMART-001'
DT = 'DT-F123hc'
DATUM = '2026.11.08'
PROV = 'scope=manual | forras=F123 HAMART-001 határkör (claude-opus-5-5; naplok/HATAR_HAMART-001.md K1–K10, DT-F123hc) | ts=2026-11-08'

ELUTASIT = {
    '1Móz 9:25': 'Emberi átkozódás: Noé átka egy leszármazottra, Kánaánra szól, a föld (adámá) szava nélkül. Ugyanez a beszédhelyzet, mint az 1Móz 49:7 pátriárkai átka, amely kint áll; a fejezetszám nem határ.',
    'Jer 51:25': 'Fizikai pusztítás: a romlás igéje (sáchat) itt a BDB 1. jelentésében (elront, elpusztít) áll, mint a kizárt Jer 51:20-ban ugyanarra a Babilonra. Az „egész föld” tárgy ettől nem lesz erkölcsi megromlás.',
    'Mal 3:11': 'A föld termésének megóvása a tized szövetségi rendjében (Mal 3:10-11), mint az 1Kir 8:34-35-ben; a 3:9 átka is kint áll, és a szöveg a Genezisre nem utal vissza.',
    'Hab 2:8': 'A chámász szava itt a megtorlás elveként áll, a „megtelt erőszakkal” és a „hallatszik az erőszak” szókapcsolata nélkül, mint a csoportosan kizárt chámász-versekben.',
    'Hab 2:17': 'A chámász szava itt a megtorlás elveként áll, a „megtelt erőszakkal” és a „hallatszik az erőszak” szókapcsolata nélkül, mint a csoportosan kizárt chámász-versekben.',
    'Jón 3:8': 'A chámász szava itt a megtérés tárgyaként áll, a „megtelt erőszakkal” és a „hallatszik az erőszak” szókapcsolata nélkül, mint a csoportosan kizárt chámász-versekben.',
    'Jer 17:5': 'Az arar itt rituális, jogi vagy indulati átok-kimondás: prófétai feddés egyéni bizalmi döntésre, mint a kizárt Jer 11:3 és Zsolt 119:21. A föld (adámá) szava nem áll benne, és a következmény nem terjed tovább.',
    '5Móz 27:15-26': 'Szövetségi átok-formula: tizenkét átok-kimondás a szövetség megszegőjére, a föld (adámá) szava nélkül. A negatív kritérium szerint a szövetség átka nem a lánc folytatása.',
    'Mt 15:19': 'Ugyanaz a másik motívum, mint a Jer 17:9-nél: a szív romlott hajlama. A lánc egyetlen szava sem áll a versben, és az 1Móz 6:5, amelyre utal, maga is tematikus sor.',
    'Mk 7:21-23': 'Ugyanaz a másik motívum, mint a Jer 17:9-nél: a szív romlott hajlama. A lánc egyetlen szava sem áll a versben, és az 1Móz 6:5, amelyre utal, maga is tematikus sor.',
    '2Pét 3:6-7': 'Noé alakja és az özönvíz ítélete újszövetségi felidézésként, mint a kizárt 2Pét 2:5-ben; a lánc szavai nélkül.',
}
# szűkítés: régi kulcs -> (új kulcs, új jelölt-indoklás, új kapcsolódás, új funkció vagy None)
SZUKIT = {
    '5Móz 28:16-19': ('5Móz 28:18',
                      'Beépítve: „Átkozott lesz … a te földednek gyümölcse”. Az átok igéje (árar) és a föld (adámá) együtt áll, az 1Móz 3:17 két szava; a szövetség többi átka (28:16-17, 28:19) a föld szava nélkül kint áll.',
                      'A szövetség átkai között egy mondat a föld termésére szól: „Átkozott lesz a te méhednek gyümölcse és a te földednek gyümölcse.” Az átok igéje (árar) és a föld (adámá) itt együtt áll, ugyanaz a két szó, amely az 1Móz 3:17-ben a föld átkát kimondja.',
                      '📜 törvényi formula — a föld termése az átok alá esik; az 1Móz 3:17 két szava a szövetség átkai között'),
    'Róm 8:20-22': ('Róm 8:21',
                    'Beépítve: „megszabadul a rothadandóság rabságától”. A φθορά (fthora) ugyanabból a φθείρω-szócsaládból való, amellyel a görög Ószövetség az 1Móz 6:11-13 romlás-igéjét (sáchat) fordítja; a 8:20 és a 8:22 ugyanennek az érvelésnek a része, a romlás szava nélkül.',
                    'Pál szerint a teremtett világ „azzal a reménységgel” él, „hogy maga a teremtett világ is megszabadul a rothadandóság rabságától”. A rothadandóság (φθορά, fthora) a görög Ószövetség romlás-szócsaládjából való: a teremtett világ még a romlás rabságában van, és szabadulásra vár.',
                    None),
}
UJ_ELUTASITOTT = [
    ('5Móz 28:16-17', 'Szövetségi átok-formula: a városra, a mezőre, a kosárra és a teknőre szóló átok, a föld (adámá) szava nélkül; a 28:18 a föld szavával külön sorban áll.'),
    ('5Móz 28:19', 'Szövetségi átok-formula: a ki- és bejövetelre szóló átok, a föld (adámá) szava nélkül; a 28:18 a föld szavával külön sorban áll.'),
    ('Róm 8:20', 'A hely a Róm 8:21 sorának folytatása: a teremtett világ „hiábavalóság alá vettetett”; a romlás szava (φθορά) a 8:21-ben áll, és az a motívumban van.'),
    ('Róm 8:22', 'A hely a Róm 8:21 sorának folytatása: a teremtett világ „egyetemben fohászkodik és nyög”; a romlás szava (φθορά) a 8:21-ben áll, és az a motívumban van.'),
]
UJ_INDOKLAS = {
    '1Móz 12:3': 'Beépítve: „és megáldatnak te benned a föld minden nemzetségei”. A határ az átok igéje (árar) és a föld (adámá) együttállása, ugyanaz a két szó, mint az 1Móz 3:17-ben, most az áldás keretében. Az 1Móz 27:29 és a 4Móz 24:9 formulája a föld szava nélkül áll, ezért kint.',
}
JEL192 = ('A mennyei sokaság Isten ítéletét dicséri a nagy parázna felett, „a mely a földet megrontotta az ő paráznaságával”. A romlás igéje (φθείρω, ftheiró) a földdel együtt az Újszövetségben csak itt és a Jel 11:18-ban áll: ugyanaz az ige és tárgy, mint a görög Ószövetségben az 1Móz 6:11 mondata, amely szerint a föld romlott vala.',
          '⚖️ ítélet — a föld megrontójának elítélése; az 1Móz 6:11 romlás-mondatának igéjével')
UJ_OK = ('126', ID, 'szövetségi átok-formula', 'szövetségi átok-formula, a föld szava nélkül',
         'a szövetség átkait mondja ki az átok igéjével, de a föld (adámá) szava nélkül; a negatív kritérium szerint a szövetségi rend nem a lánc folytatása',
         'scope=manual | forras=F123 HAMART-001 határkör (naplok/HATAR_HAMART-001.md K7, DT-F123hc) | ts=2026-11-08')


def beolvas(ut):
    sorok = open(ut, encoding='utf-8', newline='').read().split('\n')
    fej_i = next(i for i, l in enumerate(sorok) if l and not l.startswith('#'))
    return sorok, fej_i, sorok[fej_i].split('\t')


def jeloltek(ir):
    ut = 'adat/jeloltek.tsv'
    sorok, fej_i, fej = beolvas(ut)
    ix = {k: i for i, k in enumerate(fej)}
    eredeti = list(sorok)
    valtozott, latott = set(), set()
    minta = None
    for n in range(fej_i + 1, len(sorok)):
        r = sorok[n].split('\t')
        if len(r) < len(fej) or r[0] != ID or r[ix['jelolt_tipus']] != 'elofordulas':
            continue
        ige = r[1]
        if ige in ELUTASIT:
            assert r[ix['dontes']] == 'beépítve', ige
            r[ix['dontes']], r[ix['indoklas']] = 'elutasítva', ELUTASIT[ige]
        elif ige in SZUKIT:
            assert r[ix['dontes']] == 'beépítve', ige
            r[1], r[ix['indoklas']] = SZUKIT[ige][0], SZUKIT[ige][1]
            minta = list(r)
        elif ige in UJ_INDOKLAS:
            r[ix['indoklas']] = UJ_INDOKLAS[ige]
        else:
            continue
        r[ix['datum']], r[ix['dontes_ref']] = DATUM, DT
        latott.add(ige)
        sorok[n] = '\t'.join(r)
        valtozott.add(n)
    vart = set(ELUTASIT) | set(SZUKIT) | set(UJ_INDOKLAS)
    assert latott == vart, vart - latott
    # az új elutasított sorok a szűkített sor mintájára (forras_kereses: négyforrásos audit), a fájl HAMART-001 blokkjának végére
    utolso = max(n for n in range(fej_i + 1, len(sorok)) if sorok[n].startswith(ID + '\t'))
    uj = []
    for ige, ind in UJ_ELUTASITOTT:
        r = [''] * len(fej)
        r[0], r[1] = ID, ige
        r[ix['forras_kereses']] = minta[ix['forras_kereses']]
        r[ix['dontes']], r[ix['indoklas']] = 'elutasítva', ind
        r[ix['datum']], r[ix['jelolt_tipus']], r[ix['dontes_ref']] = DATUM, 'elofordulas', DT
        uj.append('\t'.join(r))
    sorok[utolso + 1:utolso + 1] = uj
    # összevetés: csak a megnevezett sorok változtak
    assert len(sorok) == len(eredeti) + len(uj)
    elter = [i for i in range(len(eredeti)) if i <= utolso and sorok[i] != eredeti[i]]
    assert set(elter) == valtozott, (set(elter) ^ valtozott)
    print('%s: %d sor módosítva, %d új sor' % (ut, len(valtozott), len(uj)))
    if ir:
        open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))


def elofordulasok(ir):
    ut = 'adat/elofordulasok.tsv'
    sorok, fej_i, fej = beolvas(ut)
    ix = {k: i for i, k in enumerate(fej)}
    ki, torolt, modositott = [], [], []
    for n, l in enumerate(sorok):
        r = l.split('\t')
        if n <= fej_i or len(r) < len(fej) or r[0] != ID:
            ki.append(l)
            continue
        ige = r[1]
        if ige in ELUTASIT:
            torolt.append(ige)
            continue
        if ige in SZUKIT:
            uj, _, kapcs, funk = SZUKIT[ige]
            r[1], r[ix['kapcsolodas']] = uj, kapcs
            if funk:
                r[ix['funkcio']] = funk
            r[ix['proveniencia']] = PROV
            modositott.append(ige)
        elif ige == 'Jel 19:2':
            r[ix['kapcsolodas']], r[ix['funkcio']] = JEL192
            r[ix['proveniencia']] = PROV
            modositott.append(ige)
        ki.append('\t'.join(r))
    assert sorted(torolt) == sorted(ELUTASIT), set(ELUTASIT) - set(torolt)
    assert sorted(modositott) == sorted(list(SZUKIT) + ['Jel 19:2']), modositott
    print('%s: %d sor törölve, %d módosítva' % (ut, len(torolt), len(modositott)))
    if ir:
        open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(ki))


def okok(ir):
    ut = 'adat/elutasitasi_okok.tsv'
    sorok, fej_i, fej = beolvas(ut)
    assert fej[:6] == ['sorrend', 'id', 'minta', 'cimke', 'megjegyzes', 'proveniencia'], fej
    if any(l.split('\t')[:2] == [UJ_OK[0], ID] for l in sorok):
        print('%s: az új ok már megvan' % ut)
        return
    # a HAMART-001 utolsó saját sora után
    utolso = max(n for n, l in enumerate(sorok) if l.split('\t')[1:2] == [ID])
    sorok.insert(utolso + 1, '\t'.join(UJ_OK))
    print('%s: 1 új ok' % ut)
    if ir:
        open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))


if __name__ == '__main__':
    ir = '--ir' in sys.argv
    okok(ir)
    jeloltek(ir)
    elofordulasok(ir)
    if not ir:
        print('(próba; írás: --ir)')
