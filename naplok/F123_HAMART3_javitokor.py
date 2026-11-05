# -*- coding: utf-8 -*-
"""F123 HAMART-001 U4 javítókör (egy kör, DT566 / D2): a független ellenőr ELTÉRÉS-einek javítása
(naplok/ELLENOR_F123_HAMART-001.md). A próza gazdája javít (claude-opus-5-5); a döntések (DT-F123ha) nem változnak.

Ír: motivumok/HAMART-001.md; adat/elofordulasok.tsv és adat/jeloltek.tsv HAMART-001 sorai (a többi sor bájtra azonos).
"""
import io
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ID = 'HAMART-001'

MD = [
    # 7. Ez 12:19 a Kivonatban; 10. nem szó szerinti idézőjel
    ('Az sem tartozik ide, amely a föld elvesztését csak a szövetség rendjében mondja ki, mint Izrael fogságba vitele '
     '„a föld színéről” (1Kir 13:34, 2Kir 17:23); a különbséget az Ez 12:19 és a Sof 1:2-3 mutatja, amelyekben az '
     'erőszakkal megtelt föld, illetve az özönvíz előtti egyetemes felsorolás (ember, barom, madár) áll.',
     'Az sem tartozik ide, amely a föld elvesztését csak a szövetség rendjében mondja ki, mint Izrael fogságba vitele '
     'a föld színéről (1Kir 13:34, 2Kir 17:23). A különbséget az Ez 12:19 és a Sof 1:2-3 mutatja: az elsőben a föld a '
     'lakói erőszaka miatt üresedik ki teljességéből, a másodikban az özönvíz előtti egyetemes felsorolás (ember, '
     'barom, madár) áll.'),
    ('a próféták „megtelt erőszakkal” mondatait (Ez 7:23, 8:17)',
     'a próféták mondatait arról, hogy a föld megtelt erőszakkal (Ez 7:23, 8:17)'),
    ('„kezünk terhes fáradozását” (1Móz 5:29)', '„kezünk terhes fáradozásában” (1Móz 5:29)'),
    # 9. a tartomány-sorok száma
    ('**Tartományok.** Négy sor több verset fog össze, mert a lánc szava egy összefüggő szakaszban többször áll. Az 5Móz '
     '27:15-26 tizenkét átok-kimondása és az 5Móz 28:16-19 négy átka egy-egy liturgikus egység.',
     '**Tartományok.** Tizenegy sor több verset fog össze, mert a hely egy összefüggő mondatban vagy szakaszban áll '
     '(1Móz 4:2-3, 4:10-11, 5Móz 27:15-26, 28:16-19, Sof 1:2-3, Ézs 24:5-6, Hós 4:1-3, Róm 8:20-22, Zsid 6:7-8, '
     'Mk 7:21-23, 2Pét 3:6-7). Az 5Móz 27:15-26 tizenkét átok-kimondása és az 5Móz 28:16-19 négy átka egy-egy '
     'liturgikus egység.'),
    # 5. a Remez nem zárja le a 8:21 vitáját
    ('és a romlás rabságától vár szabadulást (Róm 8:20-22): a föld átka mint állapot nem szűnt meg.',
     'és a romlás rabságától vár szabadulást (Róm 8:20-22): Pál a teremtett világot a romlás állapotában látja; hogy ez '
     'az 1Móz 3:17 átkának folytatása-e, azt a vitatott pontok szakasza tárgyalja.'),
    # 3. Jel 22:3 TR-alak; „eltérés nincs”
    ('A motívum tíz újszövetségi helyén a motívum szava a Textus Receptusban és a kritikai kiadásokban ugyanott áll; '
     'eltérés nincs.',
     'A motívum tíz újszövetségi helyén a motívum szava a Textus Receptusban és a kritikai kiadásokban ugyanott áll. '
     'Egy alakváltozat van: a Jel 22:3 szava a kritikai kiadásokban κατάθεμα (katathema), a Textus Receptus egyes '
     'kiadásaiban κατανάθεμα (katanathema); a jelentés mindkettőben: elátkozott dolog. A vizsgált, de kizárt helyek '
     'közül a Ján 7:49-ben a Textus Receptus az átkozott szavát (ἐπικατάρατος) hozza, a kritikai kiadás rokon alakot '
     '(ἐπάρατος); a hely a farizeusok átkozódása, ezért nem tartozik ide.'),
]

ELO = [
    # 10. „az Izráel vétke”; 3. Jel 22:3; Zsolt 14:1 igealak; Zsid 6:8; Jer 51:25 (6.); 8:21 (5.); Róm 8 (5.)
    ('A görög szó (κατάθεμα, katathema) nem a Genezis átok-szava',
     'A görög szó (κατάθεμα, katathema; a Textus Receptus egyes kiadásaiban κατανάθεμα) nem a Genezis átok-szava'),
    ('A „Megromlottak” ugyanaz a héber igealak, mint az 1Móz 6:12-ben,',
     'A „Megromlottak” ugyanannak az igének ugyanaz a törzse (hif\'íl), mint az 1Móz 6:12-ben,'),
    ('A föld, a tövis, a bojtorján és az átok együtt az 1Móz 3:17-18 görög szövegének szavai: a genezisi átok itt '
     'erkölcsi példázattá lesz.',
     'A föld, a tövis és a bojtorján az 1Móz 3:17-18 görög szövegének szavai, az átok (κατάρα, katara) pedig a '
     'Genezis átok-szavának rokona: a genezisi átok itt erkölcsi példázattá lesz.'),
    ('és Lámek vigasztalás-várását (1Móz 5:29) így csak részben teljesíti.',
     'és hogy Lámek vigasztalás-várását (1Móz 5:29) teljesíti-e, azt a lap vitatott pontként tárgyalja.'),
    ('a mondat azt mondja ki, hogy a föld átka mint állapot nem szűnt meg: az egész teremtett világ együtt nyög.',
     'a mondat szerint az egész teremtett világ még együtt nyög, és szabadulásra vár.'),
    ('A romlás igéje (sáchat) és az egész föld együtt az 1Móz 6:11-13 mondata, és ugyanez a vád tér vissza a Jel '
     '19:2-ben',
     'A romlás igéje (sáchat) és az egész föld együtt az 1Móz 6:11-13 mondata; a hely nem egy hadjárat pusztítását '
     'írja le, hanem egy birodalom vádját, amely az egész földet rontotta meg, és ugyanez a vád tér vissza a Jel '
     '19:2-ben'),
]

JEL = [
    ('„Tövis és bogácskóró növi be oltáraikat”, és a vers megnevezi „az Izráel vétkét” is.',
     '„Tövis és bogácskóró növi be oltáraikat”, és a vers „az Izráel vétke” szavakkal a bűnt is megnevezi.'),
    ('Beépítve: Babilon „romlásnak hegye, … a ki az egész földet megrontottad”. A romlás igéje (sáchat) és az egész '
     'föld együtt az 1Móz 6:11-13 mondata,',
     'Beépítve: Babilon „romlásnak hegye”, „a ki az egész földet megrontottad”. A romlás igéje (sáchat) és az egész '
     'föld együtt az 1Móz 6:11-13 mondata; a hely nem a katonai pusztítás általános esete (az elutasítva), hanem egy '
     'birodalom vádja, amely az egész földet rontotta meg,'),
]
JAN749_UJ = ('Összesítő sor 1 versre (a sor igehelye a blokk egy verse áll): a farizeusok mondják a sokaságról, hogy '
             '„átkozott”. A Textus Receptusban itt az átkozott szava (ἐπικατάρατος, epikataratosz) áll, a kritikai '
             'kiadásban rokon alak (ἐπάρατος); ez emberi átkozódás, a genezisi láncra való visszautalás nélkül, ezért '
             'a vers nem tartozik a motívumba.')
BELSO_RX = re.compile(r' Ugyanez a vers a (?:Károli-szó háló|szótár-háló \(BDB/Thayer\)) blokkban is áll '
                      r'\(halo=[^)]*\): \d+ vers, a versek listája a teljesség-mérés blokk-táblájában áll\.')
BELSO_UJ = ' Ugyanez a vers a teljesség-mérés egy másik csoportjában is szerepel.'


def csere(s, parok, hol):
    for a, b in parok:
        n = s.count(a)
        if n != 1:
            sys.exit('%s: %d találat: %s' % (hol, n, a[:60]))
        s = s.replace(a, b)
    return s


def tabla(ut, parok, extra=None):
    nyers = io.open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    sorok = nyers.split(nl)
    fej = next(s for s in sorok if s and not s.startswith('#')).split('\t')
    ix = {n: i for i, n in enumerate(fej)}
    blokk = nl.join(s for s in sorok if s.startswith(ID + '\t'))
    blokk = csere(blokk, parok, ut)
    uj_h = blokk.split(nl)
    k = 0
    for i, s in enumerate(sorok):
        if s.startswith(ID + '\t'):
            r = uj_h[k].split('\t')
            k += 1
            if extra:
                extra(r, ix)
            sorok[i] = '\t'.join(r)
    io.open(ut, 'w', encoding='utf-8', newline='').write(nl.join(sorok))


def elo_extra(r, ix):
    # 1. a jelentes_en / jelentes_hu a régi szótári jelentésből maradt: a lap és a nyílt mag a szakaszcímkéből dolgozik
    # (mint az ALVIL-001 és az ANTROP-001 új cikkén), ezért a két mező üres
    r[ix['jelentes_en']] = ''
    r[ix['jelentes_hu']] = ''


def jel_extra(r, ix):
    if r[ix['igehely']] == 'Ján 7:49' and 'G6035' in r[ix['indoklas']]:
        r[ix['indoklas']] = JAN749_UJ
    r[ix['indoklas']] = BELSO_RX.sub(BELSO_UJ, r[ix['indoklas']])


md = io.open('motivumok/HAMART-001.md', encoding='utf-8', newline='').read()
io.open('motivumok/HAMART-001.md', 'w', encoding='utf-8', newline='').write(csere(md, MD, 'md'))
tabla('adat/elofordulasok.tsv', ELO, elo_extra)
tabla('adat/jeloltek.tsv', JEL, jel_extra)
print('javítókör: kész')
