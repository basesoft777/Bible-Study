# -*- coding: utf-8 -*-
"""lap-javit HAMART-001 (2026-11-11) — a HAMART-001 kapcsolat-sorainak `indoklas` szövege a lektor 18., 19., 20. és
32. tétele szerint (`naplok/KIADAS_HAMART-001_lektor.md`; a felhasználó: „mehet a javaslatokkal”, az orkesztrátor
továbbításában; a 18. tételben orkesztrátori döntés: a kapcsolat szintje a kapcsolat jellegét írja le, nem örökli a
célhely szintjét).

A döntés (beépítve/elutasítva, típus, funkció, bizonyosság, szint) NEM változik: a `naplok/F182_kapcsolat_dontes.py`
(DT748) `minosit()` függvénye adja ugyanazt az eredményt; csak az olvasói indoklás-szöveg új:
  19. a bizonyosság a mért egyezésen áll; a „lap prózája” nem tanú (a lap nem hivatkozik önmagára); ahol hagyományos
      kereszthivatkozás-gyűjtemény (TSK, Károli) nem köti össze a két helyet, ezt kimondja;
  20. a „további N szó” helyett a visszatérő szavak nevükkel;
  18. a tematikus sorokban: a kapcsolat szintje (Remez) a két hely egymásra mutatását írja le, a célhely saját szintje
      a 2. szakaszban áll;
  32. az Ez 12:19-ben nem a megtelés igéje, hanem a tövéből való teljesség főneve (מְלֹא) áll az erőszak mellett.
A sor farka (` | DT748 | scope=… | ts=…`) megmarad, a szöveg forrásával kiegészítve.

Írás: csak a HAMART-001 sorainak `indoklas` mezője; minden más mező és sor bájtra változatlan (összevetés).
A `csv` modult nem használja. Futtatás a repó gyökeréből: python naplok/F125_lapjavit_kapcsolat.py [--ir]"""
import importlib.util
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

_spec = importlib.util.spec_from_file_location('F182D', os.path.join('naplok', 'F182_kapcsolat_dontes.py'))
D = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D)

KAP = 'adat/kapcsolatok.tsv'
TS = '2026-11-11'
SZOVEG_FORRAS = 'a szöveg: naplok/F125_lapjavit_kapcsolat.py (lap-javit HAMART-001, ts=%s)' % TS

# a szó szerint visszatérő, nem köznapi szavak olvasói neve (TAHOT/TAGNT szótő, a kiejtés a gyorsreferencia szerint)
SZONEV = {
    'H8669': 'a vágyódás (תְּשׁוּקָה, tesúká)',
    'H4910': 'az uralkodás igéje (מָשַׁל, másal)',
    'H5110': 'a bujdosás igéje (נוּד, núd)',
    'H5128': 'a vándorlás igéje (נוּעַ, núa)',
    'H3336': 'a gondolat (יֵצֶר, jécer)',
    'H3820': 'a szív (לֵב, lév)',
    'H7451': 'a gonosz (רַע, ra)',
    'H0929': 'a barom (בְּהֵמָה, behémá)',
    'H4229': 'az eltörlés igéje (מָחָה, máchá)',
    'H5775': 'a madár (עוֹף, óf)',
    'H7431': 'a csúszómászó (רֶמֶשׂ, remes)',
    'H8064': 'az ég (שָׁמַיִם, sámajim)',
    'H1320': 'a test (בָּשָׂר, bászár)',
    'H3999': 'az özönvíz (מַבּוּל, mabbúl)',
    'H4325': 'a víz (מַיִם, majim)',
    'H3351': 'az élőlény (יְקוּם, jekúm)',
    'H0369': 'a tagadószó (אַיִן, ajin)',
    'H2896': 'a jó (טוֹב, tóv)',
    'H5036': 'a bolond (נָבָל, nával)',
    'H8581': 'az utálatosság igéje (תָּעַב, táav)',
    'H0622': 'az elvétel igéje (אָסַף, ászaf)',
    'H1709': 'a hal (דָּג, dág)',
    'H3220': 'a tenger (יָם, jám)',
    'G1401': 'a szolga (δοῦλος, dulosz)',
    'G2919': 'az ítélet igéje (κρίνω, krinó)',
    'G3173': 'a nagy (μέγας, megasz)',
}
EZ1219 = {('1Móz 6:11', 'Ez 12:19'), ('1Móz 6:13', 'Ez 12:19')}
EZ1219_ELEM = ('az erőszak szava (חָמָס, chámász) és a teljesség főneve (מְלֹא, meló), a megtelés igéjének tövéből: a '
               '„megtelt erőszakkal” szópár névszói változata (az előfordulás-tábla a helyet az erőszak szaván át veszi '
               'fel)')


def indoklas(d):
    a, b = d['forras_sor'], d['cel_sor']
    dontes, biz, elem, mut, ok, csak_tem = D.minosit(d)
    assert dontes == 'beépítve', (a, b)
    lanc = [x for x in d['kozos_lanc_strong'].split(',') if x]
    szoszer = [x for x in d['kozos_tartalmi_strong'].split(',') if x and x not in D.KOZNAPI and x not in D.LANC]
    if len(szoszer) >= 2:
        hiany = [x for x in szoszer if x not in SZONEV]
        assert not hiany, ('nincs olvasói név', a, b, hiany)
        regi = 'a két helyen további %d szó szó szerint visszatér' % len(szoszer)
        uj = 'szó szerint visszatér %s' % D.felsorol([SZONEV[x] for x in szoszer])
        elem = [uj if e == regi else e for e in elem]
    if (a, b) in EZ1219:
        elem = [EZ1219_ELEM if e == D.FORDULAT['málé+chámász'] else e for e in elem]
    kulso = [x for x in mut if x != 'a lap prózája' and x != 'a tematikus sor megjelölése']
    if kulso:
        hagyomany = 'A hagyományos kereszthivatkozások közül %s is összeköti a két helyet.' % D.felsorol(kulso)
    else:
        hagyomany = 'Hagyományos kereszthivatkozás-gyűjtemény (TSK, Károli) a két helyet nem köti össze.'
    if csak_tem:
        szoveg = ('A tematikus hely, amely a lánc szavai nélkül áll a lapon, a láncnak ezt a versét nevezi meg; közös '
                  'lánc-szó nincs. A kapcsolat szintje (Remez) azt írja le, hogy a két hely egymásra mutat; a célhely '
                  'saját szintje a 2. szakaszban áll. A %s bizonyosság a tematikus megnevezésen áll. %s' % (biz, hagyomany))
    else:
        szoveg = 'Mért: %s. A %s bizonyosság ezen a mért egyezésen áll. %s' % ('; '.join(elem), biz, hagyomany)
    return szoveg[0].upper() + szoveg[1:], biz, lanc


def main(ir):
    jel = open(D.JEL, encoding='utf-8', newline='').read().split('\n')
    fej = jel[1].split('\t')
    uj_ind = {}
    for l in jel[2:]:
        if not l:
            continue
        d = dict(zip(fej, l.split('\t')))
        if d['dontes'] != 'beépítve':
            continue
        szoveg, biz, _ = indoklas(d)
        uj_ind[(d['forras_sor'], d['cel_sor'])] = (szoveg, biz)
    s = open(KAP, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    sorok = s.split(nl)
    kfej = sorok[1].split('\t')
    ii, ib = kfej.index('indoklas'), kfej.index('bizonyossag')
    ki, n = [], 0
    for l in sorok:
        c = l.split('\t')
        if len(c) == len(kfej) and c[2] == D.ID:
            szoveg, biz = uj_ind[(c[0], c[1])]
            assert c[ib] == biz, ('a bizonyosság eltérne', c[0], c[1], c[ib], biz)
            fo, _, farok = c[ii].partition(' | ')
            assert farok.startswith('DT748 | scope=manual | forras=naplok/F182_kapcsolat_jeloltek.tsv'), farok[:60]
            farok = farok.replace(' | ts=2026-11-10', '; %s | ts=2026-11-10' % SZOVEG_FORRAS) \
                if SZOVEG_FORRAS not in farok else farok
            regi = list(c)
            c[ii] = szoveg + ' | ' + farok
            assert [x for j, x in enumerate(c) if j != ii] == [x for j, x in enumerate(regi) if j != ii]
            n += 1
            ki.append('\t'.join(c))
        else:
            ki.append(l)
    assert n == len(uj_ind) == 56, (n, len(uj_ind))
    assert sum(1 for x, y in zip(ki, sorok) if x != y) <= n and len(ki) == len(sorok)
    print('HAMART-001 kapcsolat-sor: %d; „a lap prózája” a szövegekben: %d' % (
        n, sum('lap prózája' in x for x in ki if x.split('\t')[2:3] == [D.ID])))
    if ir:
        open(KAP, 'w', encoding='utf-8', newline='').write(nl.join(ki))
        print('írva: %s' % KAP)


if __name__ == '__main__':
    main('--ir' in sys.argv)
