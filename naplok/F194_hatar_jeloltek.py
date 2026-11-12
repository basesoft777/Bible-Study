"""F194.1 (DT-F194a–d; `sablonok/KESZ_LAP_KOVETELMENY.md` K04, K06, K07, K47, K48, K93, K94): az ISTENTISZT-001
határdöntéseinek átvezetése és a jelölt-indoklások olvasói alakja.

- DT-F194a (K6 = A): az ApCsel 9:14 és 9:21 elutasítva (a név után nem az Úr megnevezése áll); a két `elofordulasok.tsv`-
  sor és a rájuk mutató `kapcsolatok.tsv`-sorok kikerülnek.
- DT-F194b (K8): a 2Móz 33:19 és 34:5 kivételjelölés nélkül; az indoklás: a héber szerkezet azonos, a magyar fordítás
  kihirdetésnek adja vissza.
- DT-F194c: mindenütt יְהוָה (Jahve).
- DT-F194d (K7): az összesítő sor „vagy az elóhím” fordulata kikerül.
- K47/K48/K04/K06: az ISTENTISZT-001 minden `elofordulas`-jelöltjének indoklása olvasói mondat; héber/görög szó írással
  és zárójeles kiejtéssel (`heber_kiejtes.kiejt`, `kiejtes.atir`); más sorra, tanulmányra, naplóra nem hivatkozik; a
  „korábban (…)” előzmény és a „felhasználó döntése” idézet kimarad (a nyom a `dontes_ref`-ben marad).
  A motívumközi (`motivumkozi`) jelöltekhez nem nyúl (a kapcsolat-lépés a CS3 után).

Ellenőrzések írás előtt (eltérésnél megáll):
1. minden ISTENTISZT-001 `elofordulas`-sor új szöveget kap, más sor nem változik (soronkénti összevetés);
2. az elutasítási ok besorolása (`szerep_kizart.elutasitas_oka`) a régi és az új mintával azonos, a megengedett
   címke-átnevezésen (JHVH → az Úr neve) és a két új elutasításon kívül;
3. az új indoklás az olvasói kapu indoklás-szabályain (`naplok/F194_indoklas_meres.merj`) csak Strong-számot adhat;
4. minden „…” idézet a vers (vagy a megnevezett forrásvers) Károli-szövegének szó szerinti része.

TSV: split('\\t') / '\\t'.join(). Futtatás: python naplok/F194_hatar_jeloltek.py [--ir]
"""
import os
import re
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
sys.path.insert(0, os.path.join(GYOKER, 'naplok'))
import szerep_kizart as SZK  # noqa: E402
import F194_indoklas_meres as IM  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
DATUM = '2026.11.12'
ADAT = os.path.join(GYOKER, 'adat')

KRITERIUM = (
    'Az igehelyen a קָרָא (kárá, hív) igét a בְּשֵׁם (besém, „a nevén”) követi, és a név után az Úr neve, a יְהוָה '
    '(Jahve) áll: aktív, invokáló szerkezet („[valaki] segítségül hívja az Úr nevét”). Nem tartozik ide, ahol a név '
    'helyén névmási rag áll („nevemet”, „nevedet”, „nevét”: Zak 13:9, Zsolt 105:1, Jer 10:25, Ézs 43:1, 45:3), vagy más '
    'név (Ézs 44:5). Az Újszövetségben az ἐπικαλέω (epikaleó) mellett a névnek, az ὄνομα (onoma) szónak és az Úr '
    'megnevezésének kell állnia; a puszta „nevedet”, „ezt a nevet” (ApCsel 9:14, 21) és a név nélküli segítségül hívás '
    '(2Tim 2:22, Róm 10:12, 14) a fölérendelt fogalomhoz tartozik. A mérce a Károli alapszövege, a Textus Receptus '
    '(ApCsel 22:16). Kivétel: a kontrasztként megtartott 1Kir 18:25–26, ahol a név után אֱלֹהֵיכֶם (elóhéchem, „a ti '
    'istenteknek”), illetve הַבַּעַל (habbaal, „a Baálnak”) áll. A szenvedő (passzív) נִקְרָא … עַל (nikrá … al) '
    'szerkezet (birtoklás, hovatartozás, nem invokáció) kizárja a besorolást, még ha ugyanazt a két gyököt használja is '
    '(2Sám 6:2, Jer 7:10–14, 5Móz 28:10; az Újszövetségben a Zsid 11:16).')

UR_TAIL = 'A motívumba csak az a hely tartozik, ahol a név után az Úr neve áll (szerkesztői döntés).'
FORMULA = ('a héberben a קָרָא (kárá) után a בְּשֵׁם (besém) és az Úr neve, a יְהוָה (Jahve) áll, a görögben az '
           'ἐπικαλέω (epikaleó) mellett az ὄνομα (onoma) és az Úr megnevezése')

BEEPITETT = {
    '1Móz 4:26': 'לִקְרֹא בְּשֵׁם יְהוָה (likró besém Jahve) — a formula első előfordulása, Énós születése után: '
                 '„Akkor kezdték segítségül hívni az Úrnak nevét.”',
    '1Móz 12:8': 'וַיִּקְרָא בְּשֵׁם יְהוָה (vajjikrá besém Jahve) — Ábrám Bétel és Hái között oltárt épít, és '
                 'segítségül hívja az Úr nevét: az oltár és a segítségül hívás itt áll először együtt.',
    '1Móz 13:4': 'וַיִּקְרָא שָׁם אַבְרָם בְּשֵׁם יְהוָה (vajjikrá sám avrám besém Jahve) — Ábrám visszatér ahhoz '
                 'az oltárhoz, „melyet ott elsőben készített vala”, és ott újra segítségül hívja az Úr nevét.',
    '1Móz 21:33': 'וַיִּקְרָא שָׁם בְּשֵׁם יְהוָה אֵל עוֹלָם (vajjikrá sám besém Jahve él ólám) — Beérsebában a név '
                  'után isteni jelző áll: „az örökkévaló Úr Istennek nevét”.',
    '1Móz 26:25': 'וַיִּקְרָא בְּשֵׁם יְהוָה (vajjikrá besém Jahve) — Izsák oltárt épít, és ugyanazzal a formulával '
                  'hívja segítségül az Úr nevét, mint előtte Ábrahám.',
    '1Kir 18:24': 'וַאֲנִי אֶקְרָא בְשֵׁם יְהוָה (vaaní ekrá vesém Jahve) — Illés a Kármelen egy versben állítja '
                  'szembe a két hívást: „hívjátok segítségül a ti istenteknek nevét, és én is segítségül hívom az '
                  'Úrnak nevét”.',
    '1Kir 18:25': 'וְקִרְאוּ בְּשֵׁם אֱלֹהֵיכֶם (vekireú besém elóhéchem) — Illés felszólítja a Baál prófétáit, hogy '
                  'hívják segítségül istenük nevét. A név után nem a יְהוָה (Jahve), hanem az אֱלֹהֵיכֶם '
                  '(elóhéchem, „a ti istenteknek”) áll; a hely kontrasztként tartozik ide (szerkesztői döntés).',
    '1Kir 18:26': 'וַיִּקְרְאוּ בְשֵׁם הַבַּעַל (vajjikreú vesém habbaal) — a Baál prófétái reggeltől délig hívják '
                  'segítségül a Baál nevét, „De nem jött szó, sem felelet.” A név után a הַבַּעַל (habbaal, „a '
                  'Baálnak”) áll; a hely kontrasztként tartozik ide (szerkesztői döntés).',
    '2Kir 5:11': 'וְקָרָא בְּשֵׁם יְהוָה אֱלֹהָיו (vekárá besém Jahve elóháv) — Naámán, az arám hadvezér azt várja, '
                 'hogy Elizeus „segítségül hívja az Úrnak, az ő Istenének nevét”: a formula idegen szájában is ismert.',
    'Sof 3:9': 'לִקְרֹא כֻלָּם בְּשֵׁם יְהוָה (likró kullám besém Jahve) — ígéret a népekről: ajkuk tisztává lesz, '
               '„hogy mind segítségül hívják az Úr nevét”.',
    'Zsolt 116:4': 'וּבְשֵׁם יְהוָה אֶקְרָא (úvesém Jahve ekrá) — a zsoltáros személyes könyörgése: „Kérlek Uram, '
                   'szabadítsd meg az én lelkemet!”',
    'Zsolt 116:13': 'וּבְשֵׁם יְהוָה אֶקְרָא (úvesém Jahve ekrá) — ugyanez a mondat a hálaadásban, a szabadulás után: '
                    '„A szabadulásért való poharat felemelem”.',
    'Zsolt 116:17': 'וּבְשֵׁם יְהוָה אֶקְרָא (úvesém Jahve ekrá) — harmadszor ugyanez a mondat a zsoltárban, a '
                    'hálaáldozat bemutatásakor.',
    'Jóel 2:32': 'יִקְרָא בְּשֵׁם יְהוָה (jikrá besém Jahve) — „mindaz, a ki az Úrnak nevét hívja segítségül, '
                 'megmenekül”; ezt a verset idézi az ApCsel 2:21 és a Róm 10:13. A héber számozásban Jóel 3:5.',
    '1Kor 1:2': 'ἐπικαλουμένοις τὸ ὄνομα τοῦ κυρίου ἡμῶν Ἰησοῦ Χριστοῦ (epikalúmenoisz to onoma tú küriú hémón Iészú '
                'Khrisztú) — Pál a gyülekezetet azokkal együtt köszönti, „a kik a mi Urunk Jézus Krisztus nevét '
                'segítségül hívják bármely helyen”.',
    'ApCsel 22:16': 'ἐπικαλεσάμενος τὸ ὄνομα τοῦ κυρίου (epikaleszamenosz to onoma tú küriú) — Pál megtérésének '
                    'elbeszélésében a keresztség mellett áll: „segítségül híván az Úrnak nevét”. A Károli a Textus '
                    'Receptust követi; a kritikai szövegben az αὐτοῦ (autú, „az ő nevét”) áll.',
    '2Móz 33:19': 'וְקָרָאתִי בְשֵׁם יְהוָה (vekárátí vesém Jahve) — a héber szerkezet azonos a többi helyével; a '
                  'magyar fordítás kihirdetésnek adja vissza: „kiáltom előtted az Úr nevét”.',
    '2Móz 34:5': 'וַיִּקְרָא בְשֵׁם יְהוָה (vajjikrá vesém Jahve) — a héber szerkezet azonos a többi helyével; a magyar '
                 'fordítás kihirdetésnek adja vissza: „nevén kiáltá az Urat”.',
    'ApCsel 2:21': 'ἐπικαλέσηται τὸ ὄνομα κυρίου (epikaleszétai to onoma küriú) — Péter pünkösdi beszéde a Jóel 2:32-t '
                   'idézi: „mindaz, a ki az Úrnak nevét segítségül hívja, megtartatik”.',
    'Róm 10:13': 'ἐπικαλέσηται τὸ ὄνομα κυρίου (epikaleszétai to onoma küriú) — Pál a Jóel 2:32-t idézi: „minden, a ki '
                 'segítségül hívja az Úr nevét, megtartatik”.',
}

DONTES_VALT = {   # beépítve → elutasítva (DT-F194a)
    'ApCsel 9:14': 'A név után nem az Úr neve áll, hanem névmás: τὸ ὄνομά σου (to onoma szú, „a te nevedet”), az Úr '
                   'megnevezése nélkül. A mérce azonos a héber névmási ragos helyekével: a motívumba csak az a hely '
                   'tartozik, ahol a név az Úr megnevezett neve (szerkesztői döntés); a hely a fölérendelt fogalomhoz '
                   'tartozik.',
    'ApCsel 9:21': 'A név után nem az Úr neve áll, hanem mutató névmás: τὸ ὄνομα τοῦτο (to onoma túto, „ezt a nevet”), '
                   'az Úr megnevezése nélkül. A mérce azonos a héber névmási ragos helyekével: a motívumba csak az a '
                   'hely tartozik, ahol a név az Úr megnevezett neve (szerkesztői döntés); a hely a fölérendelt '
                   'fogalomhoz tartozik.',
}

EGYEDI = {
    'Zak 13:9': 'A יִקְרָא (jikrá) után בִשְׁמִי (vismí, „az én nevemet”) áll: névmási rag, nem az Úr neve, a יְהוָה '
                '(Jahve). ' + UR_TAIL,
    'Zsolt 105:1': 'A קִרְאוּ (kireú) után בִּשְׁמוֹ (bismó, „az ő nevét”) áll: névmási rag, nem az Úr neve, a '
                   'יְהוָה (Jahve). ' + UR_TAIL,
    '1Krón 16:8': 'A קִרְאוּ (kireú) után בִשְׁמוֹ (vismó, „az ő nevét”) áll: névmási rag, nem az Úr neve, a יְהוָה '
                  '(Jahve). ' + UR_TAIL,
    'Ézs 12:4': 'A קִרְאוּ (kireú) után בִשְׁמוֹ (vismó, „az Ő nevét”) áll: névmási rag, nem az Úr neve, a יְהוָה '
                '(Jahve). ' + UR_TAIL,
    'Jer 10:25': 'A קָרָאוּ (káráú) mellett בְּשִׁמְךָ (besimchá, „a te nevedet”) áll: névmási rag, nem az Úr neve, a '
                 'יְהוָה (Jahve). ' + UR_TAIL,
    'Zsolt 79:6': 'A קָרָאוּ (káráú) mellett בְּשִׁמְךָ (besimchá, „a te nevedet”) áll: névmási rag, nem az Úr neve, '
                  'a יְהוָה (Jahve). ' + UR_TAIL,
    'Ézs 64:6': 'A קוֹרֵא (kóré) után בְשִׁמְךָ (vesimchá, „nevedet”) áll: névmási rag, nem az Úr neve, a יְהוָה '
                '(Jahve). ' + UR_TAIL,
    'Ézs 41:25': 'A יִקְרָא (jikrá) után בִשְׁמִי (vismí, „nevemet”) áll: névmási rag, nem az Úr neve, a יְהוָה '
                 '(Jahve). ' + UR_TAIL,
    'Ézs 43:1': 'A קָרָאתִי (kárátí) után בְשִׁמְךָ (vesimchá, „neveden”) áll: a név a megszólított Jákóbé, nem az Úr '
                'neve, a יְהוָה (Jahve). ' + UR_TAIL,
    'Ézs 45:3': 'A הַקּוֹרֵא (hakkóré) után בְשִׁמְךָ (vesimchá, „neveden”) áll: a név a megszólított Círusé, nem az '
                'Úr neve, a יְהוָה (Jahve). ' + UR_TAIL,
    'Ézs 44:5': 'A יִקְרָא (jikrá) után בְשֵׁם יַעֲקֹב (vesém jaakóv, „Jákób nevét”) áll: más név, nem az Úr neve, a '
                'יְהוָה (Jahve). ' + UR_TAIL,
    'Róm 10:12': 'Név nélküli segítségül hívás: az ἐπικαλέω (epikaleó) áll („a kik őt segítségül hívják”), de az ὄνομα '
                 '(onoma) nem áll mellette. A név nélküli segítségül hívás a fölérendelt fogalomhoz tartozik '
                 '(szerkesztői döntés).',
    'Róm 10:14': 'Név nélküli segítségül hívás: az ἐπικαλέω (epikaleó) áll („Mimódon hívják azért segítségül azt, a '
                 'kiben nem hisznek?”), de az ὄνομα (onoma) nem áll mellette. A név nélküli segítségül hívás a '
                 'fölérendelt fogalomhoz tartozik (szerkesztői döntés).',
    '2Tim 2:22': 'Név nélküli segítségül hívás: az ἐπικαλέω (epikaleó) áll („a kik segítségül hívják az Urat tiszta '
                 'szívből”), de az ὄνομα (onoma) nem áll mellette. A név nélküli segítségül hívás a fölérendelt '
                 'fogalomhoz tartozik (szerkesztői döntés).',
    '1Pét 1:17': '„Atyának hívjátok őt” — megszólítás, nem az Úr nevének segítségül hívása; a versben az ὄνομα (onoma) '
                 'sem áll (szerkesztői döntés).',
    'Zsolt 105:15': 'A próféták érintetlenségéről szól ugyanabban a zsoltárban („Meg ne illessétek az én '
                    'felkentjeimet”); tartalmilag nem releváns.',
    'Róm 10:11': 'Nincs meg a formula a versben: sem az ἐπικαλέω (epikaleó), sem a καλέω (kaleó) nem áll benne.',
    '1Pét 1:6': 'A Zak 13:9 Károli-kereszthivatkozásának célhelye: a kapcsolat a próbatétel képe, a formula nem áll a '
                'versben.',
    '1Pét 1:7': 'A Zak 13:9 Károli-kereszthivatkozásának célhelye: a kapcsolat a próbatétel képe („tűz által kipróbált '
                'aranynál”), a formula nem áll a versben.',
    '2Kor 1:23': 'Esküformás tanúhívás: „Én pedig az Istent hívom bizonyságul az én lelkemre” — Istent tanúnak hívja, '
                 'nem segítségül.',
    'ApCsel 7:59': 'István imája („Uram Jézus, vedd magadhoz az én lelkemet!”) invokáció, de az ἐπικαλέω (epikaleó) '
                   'mellett nem áll az ὄνομα (onoma): a formulán kívül, a fölérendelt fogalomhoz tartozik.',
    'Mt 10:25': 'Megnevezés jellegű használat: „Ha a házigazdát Belzebubnak hívták” — gúnynév adása, nem a név '
                'segítségül hívása.',
    'ApCsel 15:17': 'Szenvedő (passzív) szerkezet: a név a népeken áll („a kik az én nevemről neveztetnek”), ez '
                    'hovatartozás, mint a héber נִקְרָא … עַל (nikrá … al); nem a név segítségül hívása.',
    'Jak 2:7': 'Szenvedő (passzív) szerkezet: a név a hívőkön áll („a melyről neveztettek”), ez hovatartozás, mint a '
               'héber נִקְרָא … עַל (nikrá … al); nem a név segítségül hívása.',
    'Zsid 11:16': 'Szenvedő (passzív) szerkezet: Isten nevezteti magát az atyák Istenének („hogy Istenöknek '
                  'neveztessék”), ez hovatartozás, mint a héber נִקְרָא … עַל (nikrá … al); nem a név segítségül '
                  'hívása.',
    'Zsolt 99:6': 'A versben a בְּקֹרְאֵי שְׁמוֹ (bekóreé semó, „az ő nevét segítségül hívókkal”) áll, a második tagban '
                  'pedig az Urat az אֶל (el, „-hoz”) elöljáróval hívják. A קָרָא (kárá) után sehol nem áll a בְּשֵׁם '
                  '(besém) és az Úr neve: az invokáló szerkezet nincs meg, ezért a hely nem tartozik ide '
                  '(szerkesztői döntés).',
}

NEVADAS = ('Névadás, nem segítségül hívás: a 25:25–26-ban a קָרָא (kárá) és a שֵׁם (sém) az ikrek elnevezésében áll '
           '(„azért nevezék nevét Ézsaúnak”); a 25:21–24 ugyanennek az elbeszélésnek a bevezetése.')
CSOPORT = [   # (a régi indoklás eleje, az új szöveg)
    ('ellenőrizve, nem tartalmazza a H7121+H8034', 'Nincs meg a formula a versben: sem a קָרָא בְּשֵׁם (kárá besém) '
     'szerkezet, sem az ἐπικαλέω (epikaleó) a névvel. A hely kereszthivatkozás nyomán került a jelöltek közé.'),
    ('név nélküli segítségül hívás (H7121', 'Név nélküli segítségül hívás: a קָרָא (kárá) Istenhez szól, de a בְּשֵׁם '
     '(besém) és az Úr neve nem áll mellette. Ez az imádság általános formája, a fölérendelt fogalomhoz tartozik.'),
    ('név nélküli H7121', 'Név nélküli segítségül hívás: a קָרָא (kárá) Istenhez szól, de a בְּשֵׁם (besém) és az Úr '
     'neve nem áll mellette. Ez az imádság általános formája, a fölérendelt fogalomhoz tartozik.'),
    ('a 25:25-26-ban a H7121+H8034 névadás', NEVADAS),
    ('az erkölcsi intelmet köti össze', 'A 2Tim 2:22 kereszthivatkozása ide az erkölcsi intelmet köti össze („Az '
     'ifjúkori kivánságokat pedig kerüld”), nem a segítségül hívást.'),
    ('A szűrő-szabály szerint jogi fellebbezés', 'Jogi fellebbezés: az ἐπικαλέω (epikaleó) itt a császárhoz való '
     'fellebbezést jelenti, nem a név segítségül hívását.'),
    ('A szűrő-szabály szerint passzív vagy megnevező alak', 'Megnevezés: az ἐπικαλέω (epikaleó) itt szenvedő (passzív) '
     'alakban áll, és egy ember mellék- vagy ragadványnevét adja meg; ez nem a név segítségül hívása.'),
    ('D-minta: passzív', 'Szenvedő (passzív) szerkezet: a נִקְרָא … עַל (nikrá … al) azt mondja, hogy az Úr neve egy '
     'házon, a ládán vagy a népen áll, vagyis az övé. Ez hovatartozás, nem a név segítségül hívása; a negatív '
     'kritérium kizárja.'),
]

OSSZ_TAIL = ' A motívumhoz az a vers tartozik, amelyben a hívás az Úr nevére irányul: %s. Ezért egyik sem tartozik ide.' % FORMULA
OSSZESITO = {
    '1Móz 1:5': 'Összesítő sor 246 versre (az első itt áll): a קָרָא (kárá, hív, kiált) igéje a név, a שֵׁם (sém) '
                'nélkül áll a versben: hívás, kiáltás vagy meghívás, a név segítségül hívása nélkül.' + OSSZ_TAIL,
    '1Móz 2:19': 'Összesítő sor 126 versre (az első itt áll): a קָרָא (kárá) és a שֵׁם (sém) egy versben áll, de '
                 'elnevezésként („nevét X-nek nevezte”), nem a név segítségül hívásaként.' + OSSZ_TAIL,
    '2Móz 18:4': 'Összesítő sor 51 versre (az első itt áll): a Károli hív, kiált vagy segítségül szava ezekben a '
                 'versekben más héber vagy görög szót fordít; a motívum szavai nem állnak a versben.' + OSSZ_TAIL,
    '1Móz 41:52': 'Összesítő sor 21 versre (az első itt áll): a קָרָא (kárá) és a שֵׁם (sém) egy versben áll, de nem '
                  'egy szerkezetben: a hívás nem a névre irányul.' + OSSZ_TAIL,
    '2Móz 31:2': 'Összesítő sor 12 versre (az első itt áll): a קָרָא (kárá) és a בְּשֵׁם (besém) egy szerkezetben áll, '
                 'de a név után nem az Úr neve, a יְהוָה (Jahve) áll, hanem névmási rag vagy más név.' + OSSZ_TAIL,
}

# Az idézet forrásverse, ha nem a sor saját verse.
IDEZET_FORRAS = {'1Móz 25:21': '1Móz 25:25', '1Móz 25:22': '1Móz 25:25', '1Móz 25:23': '1Móz 25:25',
                 '1Móz 25:24': '1Móz 25:25', '1Móz 25:26': '1Móz 25:25', '1Pét 2:11': '2Tim 2:22',
                 '1Pét 3:11': '2Tim 2:22', '1Kor 6:18': '2Tim 2:22', 'Zsolt 119:9': '2Tim 2:22',
                 '1Tim 6:11': '2Tim 2:22', 'Zsid 12:14': '2Tim 2:22', '1Tim 4:12': '2Tim 2:22',
                 'ApCsel 2:21': 'ApCsel 2:21', '1Móz 2:19': None}
NEM_IDEZET = {'„a nevén”', '„nevét X-nek nevezte”', '„az ő nevét”', '„-hoz”'}   # glossza, nem Károli-idézet

OKOK_CSERE = {   # (sorrend) -> {mező: új érték} az elutasitasi_okok.tsv ISTENTISZT-001 soraiban
    '5': {'cimke': 'nem az Úr neve áll a név után (összesítő sor)',
          'megjegyzes': 'a besém után névmási rag vagy más név áll'},
    '101': {'minta': 'nem az Úr neve', 'cimke': 'nem az Úr neve áll a név után',
            'megjegyzes': 'a név után névmási rag, névmás vagy más név áll, nem az Úr megnevezett neve'},
}
CIMKE_ATNEVEZES = {'nem JHVH áll a név után': 'nem az Úr neve áll a név után',
                   'nem JHVH áll a név után (összesítő sor)': 'nem az Úr neve áll a név után (összesítő sor)'}
KI_ELOF = {'ApCsel 9:14', 'ApCsel 9:21'}


def nyers(nev):
    with open(os.path.join(ADAT, nev), encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def fej_index(sorok):
    for i, s in enumerate(sorok):
        if s and not s.startswith('#'):
            return i, s.rstrip('\r').split('\t')
    raise SystemExit('nincs fejléc')


def karoli():
    d = {}
    for s in nyers('../konkordancia/Karoli_1908.tsv'):
        m = s.rstrip('\r').split('\t')
        if len(m) > 1:
            d[m[0]] = m[1]
    return d


def uj_indoklas(r):
    h = r['igehely']
    if h in DONTES_VALT:
        return DONTES_VALT[h]
    if r['dontes'] == 'beépítve':
        return BEEPITETT[h]
    if h in OSSZESITO and r['indoklas'].startswith('Összesítő sor'):
        return OSSZESITO[h]
    if h in EGYEDI:
        return EGYEDI[h]
    talalt = [uj for elo, uj in CSOPORT if r['indoklas'].startswith(elo)]
    if len(talalt) != 1:
        raise SystemExit('nincs (vagy több) új szöveg: %s | %s' % (h, r['indoklas'][:80]))
    return talalt[0]


def main():
    ir = '--ir' in sys.argv
    hibak = []
    kar = karoli()
    regi_minta = SZK.okok(ID)

    # --- elutasitasi_okok.tsv ---
    ok_sorok = nyers('elutasitasi_okok.tsv')
    fi, okf = fej_index(ok_sorok)
    ok_uj = list(ok_sorok)
    for i in range(fi + 1, len(ok_sorok)):
        s = ok_sorok[i].rstrip('\r')
        m = s.split('\t')
        if len(m) < len(okf):
            continue
        d = dict(zip(okf, m))
        if d['id'] == ID and d['sorrend'] in OKOK_CSERE:
            for k, v in OKOK_CSERE[d['sorrend']].items():
                d[k] = v
            ok_uj[i] = '\t'.join(d[k] for k in okf) + ('\r' if ok_sorok[i].endswith('\r') else '')
    # az új mintaszótár a módosított sorokból (ideiglenes fájl a repón kívül)
    tmp = os.path.join(os.environ.get('TEMP', '/tmp'), 'F194_okok.tsv')
    with open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(ok_uj))
    uj_minta = SZK.okok(ID, tmp)

    # --- jeloltek.tsv ---
    j_sorok = nyers('jeloltek.tsv')
    fi, jf = fej_index(j_sorok)
    j_uj = list(j_sorok)
    valtozott = 0
    for i in range(fi + 1, len(j_sorok)):
        s = j_sorok[i].rstrip('\r')
        m = s.split('\t')
        if len(m) < len(jf):
            continue
        r = dict(zip(jf, m))
        if r['id'] != ID or r['jelolt_tipus'] != 'elofordulas':
            continue
        regi = dict(r)
        r['indoklas'] = uj_indoklas(r)
        if r['igehely'] in DONTES_VALT:
            r['dontes'] = 'elutasítva'
            r['datum'] = DATUM
            r['dontes_ref'] = ' · '.join(x for x in (r['dontes_ref'], 'DT-F194a') if x)
        if r['igehely'] == '2Móz 31:2':
            r['dontes_ref'] = r['dontes_ref'] + ' · DT-F194d'
        # 2. besorolás
        if r['dontes'] == 'elutasítva':
            uj_c = SZK.elutasitas_oka(r['indoklas'], uj_minta)
            if regi['dontes'] == 'elutasítva':
                regi_c = SZK.elutasitas_oka(regi['indoklas'].partition(' | ')[0], regi_minta)
                if CIMKE_ATNEVEZES.get(regi_c, regi_c) != uj_c:
                    hibak.append('besorolás változott: %s: %s → %s' % (r['igehely'], regi_c, uj_c))
            elif uj_c != 'nem az Úr neve áll a név után':
                hibak.append('új elutasítás besorolása: %s: %s' % (r['igehely'], uj_c))
        # 3. olvasói kapu
        for nev, mi in IM.merj(r['indoklas']):
            if nev != 'Strong-szám':
                hibak.append('kapu: %s: %s: %s' % (r['igehely'], nev, mi))
        # 4. idézetek
        forras = IDEZET_FORRAS.get(r['igehely'], r['igehely'])
        for q in re.findall(r'„([^”]*)”', r['indoklas']):
            if '„%s”' % q in NEM_IDEZET or forras is None:
                continue
            szoveg = kar.get(forras, '') + ' ' + kar.get(r['igehely'], '')
            if q not in szoveg and q.rstrip('.') not in szoveg:
                hibak.append('idézet nem Károli-szó szerinti: %s: „%s”' % (r['igehely'], q))
        uj_sor = '\t'.join(r[k] for k in jf) + ('\r' if j_sorok[i].endswith('\r') else '')
        if uj_sor != j_sorok[i]:
            valtozott += 1
            j_uj[i] = uj_sor

    # --- elofordulasok.tsv, kapcsolatok.tsv: kivétel ---
    e_sorok = nyers('elofordulasok.tsv')
    fi, ef = fej_index(e_sorok)
    e_uj = [s for k, s in enumerate(e_sorok)
            if not (k > fi and s.split('\t')[0] == ID and s.split('\t')[1] in KI_ELOF)]
    e_ki = len(e_sorok) - len(e_uj)
    k_sorok = nyers('kapcsolatok.tsv')
    fi, kf = fej_index(k_sorok)
    k_uj, k_ki = [], []
    for k, s in enumerate(k_sorok):
        m = s.rstrip('\r').split('\t')
        if k > fi and len(m) >= 3 and m[2] == ID and (m[0] in KI_ELOF or m[1] in KI_ELOF):
            k_ki.append('%s → %s' % (m[0], m[1]))
            continue
        k_uj.append(s)

    # --- motivumok.tsv ---
    mo = nyers('motivumok.tsv')
    fi, mf = fej_index(mo)
    mo_uj = list(mo)
    for i in range(fi + 1, len(mo)):
        m = mo[i].rstrip('\r').split('\t')
        if m[0] == ID:
            d = dict(zip(mf, m))
            d['negativ_kriterium'] = KRITERIUM
            mo_uj[i] = '\t'.join(d[k] for k in mf) + ('\r' if mo[i].endswith('\r') else '')

    # összevetés: a változott sorok száma
    def diff(a, b):
        return sum(1 for x, y in zip(a, b) if x != y) if len(a) == len(b) else None
    print('jeloltek.tsv: %d sor változik (ISTENTISZT-001 elofordulas)' % valtozott)
    print('elofordulasok.tsv: %d sor kikerül' % e_ki)
    print('kapcsolatok.tsv: %d sor kikerül: %s' % (len(k_ki), '; '.join(k_ki)))
    print('elutasitasi_okok.tsv: %d sor változik' % diff(ok_sorok, ok_uj))
    print('motivumok.tsv: %d sor változik' % diff(mo, mo_uj))
    if e_ki != 2:
        hibak.append('elofordulasok: 2 helyett %d sor' % e_ki)
    if len(k_ki) != 2:
        hibak.append('kapcsolatok: 2 helyett %d sor' % len(k_ki))
    if diff(ok_sorok, ok_uj) != 2 or diff(mo, mo_uj) != 1:
        hibak.append('váratlan sorszám az okok vagy a motívum táblában')
    for h in hibak:
        print('HIBA:', h)
    if hibak:
        raise SystemExit('%d hiba, nem írok' % len(hibak))
    if not ir:
        print('próba: rendben (írás: --ir)')
        return
    for nev, sorok in (('jeloltek.tsv', j_uj), ('elofordulasok.tsv', e_uj), ('kapcsolatok.tsv', k_uj),
                       ('elutasitasi_okok.tsv', ok_uj), ('motivumok.tsv', mo_uj)):
        with open(os.path.join(ADAT, nev), 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(sorok))
    print('írva.')


if __name__ == '__main__':
    main()
