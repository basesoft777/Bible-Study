# BDB_HU_frissites — a `bdb_szakasz_hu.tsv` frissítésének naplója (2026-10-29)

*A döntés: `DONTESEK.md`, a BDB-frissítés sora (DT423); a nyitott tételek: N-F131f, N-F131g.*

## 1. Döntés és eredmény

- **E19 `KeyError: 'illesztes'`:** az ok nem a BDB-tábla, hanem a Windows-os CRLF.
  - A teszt `_ir` segédje szövegmódban ír; a `thayer_bemenet.tabla_olvas` newline=''-vel olvas, és nem vágja le a `\r`-t.
  - Javítva mindkét oldalon: (a) a teszt LF-fel ír, (b) az olvasó levágja a `\r`-t.
  - A `test_szabalyok` 192 tesztje zöld. A többi CRLF-sérülékeny olvasó csak listázva: `CRLF_olvaso_felmeres.md`.
- **A teljes újragenerálás nem került be.** A próbagenerálás 49 sor rontás-jelöltet adott (2. pont), a 30-as mintában pedig 2 Strongban hamis illesztés volt.
  - Egy célzott személy-szabály mérés után elvetve: javul 359/367, rontás-jelölt 100, a valódi szakaszfejből 36 változik.
  - A teljes frissítés az N-F131g (csoporthatár-alapú illesztés) után megy.
- **Részleges frissítés:** `hu_illeszt.py --ts 2026-10-29 --strong H4397,H8034,H9004`. A három Strong változása kizárólag a „Kö^ii.” szabályból jön.
  - Tartalmilag 6 sor változik, a 44 sor proveniencia-ts-e 2026-10-29. A többi sor bájtra a 2026-10-18-i generálásé; az első fejlécsor jelöli.
  - Az ISTENTISZT-001 lapon pontosan a 3 várt H8034-sor változik; a többi lap nulladiff.
- **`teszt_bont.HuIlleszt`:** 13 teszt, 11 zöld (köztük a 2 új). A `test_ellenoriz` és a `test_osszefuzo_a_mai_adaton_valtozatlan` a teljes tábla elavultsága miatt piros, az N-F131f-ig.
- **H3092 (jelölt hiány, elfogadva):** a szakaszos újrafordításban „— 1 ׳יְהוֺ” áll, pont nélküli „1” és utána héber. A magyar oldali felismerő ezt nem veszi jelölőnek, ezért a -/1/- szakasz `elakad`, a szövege a fej szakaszban marad. Nem hamis illesztés.

## 2. A teljes próbagenerálás összevetése

A kimenet a `python naplok/BDB_HU_frissites_osszevetes.py --minta 30` futtatásából származik, a teljes, NEM commitolt próbatáblán (ts 2026-10-29, mag 20261029). Tartalma:
- a 101 eltérő meglévő Strong okkategóriával: `forditas` = új fordítás, `illesztes` = illesztő-szabály;
- a 49 rontás-jelölt sor tételesen;
- a 30-as minta.

A minta hamis illesztései: H4843 Pi'el/1, Pi'el/2, Hiph'il; H6293 Qal/1.

```
régi: 674 Strong, 9664 sor; új: 4000 Strong, 25228 sor; új Strong: 3326; eltűnt Strong: 0 []
eltérő meglévő Strong: 101

== a meglévő, eltérő Strongok ==
H0068  forditas   16 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H0157  forditas   13 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H0259  forditas   16 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H0352  forditas    8 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H0410  forditas   11 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H0539  forditas    9 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H0637  forditas    5 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H0702  forditas   13 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('elakad', 'illeszkedik'): 1, ('horgonnyal', 'illeszkedik'): 1}
H0834  forditas   67 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('elakad', 'illeszkedik'): 34, ('horgonnyal', 'illeszkedik'): 1}
H0995  forditas   23 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1004  forditas   29 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('horgonnyal', 'illeszkedik'): 2, ('elakad', 'illeszkedik'): 13}
H1129  forditas   24 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1197  forditas    9 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1242  forditas   13 sor  mezők: hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('elakad', 'illeszkedik'): 1}
H1288  forditas   40 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1320  forditas   13 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1419  forditas   15 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1568  forditas   20 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1870  forditas   17 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1875  forditas   21 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1980  forditas   74 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H1984  forditas   24 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2091  forditas   27 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('horgonnyal', 'illeszkedik'): 1, ('illeszkedik', 'elakad'): 11, ('illeszkedik', 'horgonnyal'): 2, ('horgonnyal', 'elakad'): 1}
H2220  forditas    9 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2388  forditas   52 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2396  forditas    6 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2398  forditas   23 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2416  forditas   17 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2451  forditas    8 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2470  forditas   20 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2506  forditas   15 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2568  forditas   27 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('elakad', 'illeszkedik'): 1, ('illeszkedik', 'elakad'): 7, ('illeszkedik', 'horgonnyal'): 1}
H2572  forditas   16 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H2617  forditas   20 sor  mezők: hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('elakad', 'illeszkedik'): 13}
H3027  forditas   39 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('elakad', 'illeszkedik'): 24, ('horgonnyal', 'illeszkedik'): 1}
H3068  forditas   26 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3083  forditas   13 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3092  forditas    8 sor  mezők: hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('illeszkedik', 'elakad'): 1}
H3117  forditas   49 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('illeszkedik', 'elakad'): 9, ('elakad', 'horgonnyal'): 1}
H3254  forditas   15 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('horgonnyal', 'illeszkedik'): 1}
H3384  forditas   13 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3423  forditas   20 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3588  forditas   25 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3603  forditas    6 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3605  forditas    9 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3644  forditas    4 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3722  forditas   16 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3742  forditas   14 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3772  forditas   31 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3789  forditas   17 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3808  forditas   26 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3881  forditas   14 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3947  forditas   34 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H3967  forditas   19 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H4217  forditas    7 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H4264  forditas   10 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H4397  illesztes   2 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H4480  forditas   56 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H4605  forditas   17 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H4639  forditas    8 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('horgonnyal', 'illeszkedik'): 1, ('elakad', 'illeszkedik'): 1}
H4672  forditas   49 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H4940  forditas   11 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H5127  forditas   14 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H5307  forditas   41 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('illeszkedik', 'elakad'): 16, ('illeszkedik', 'horgonnyal'): 1}
H5315  forditas   43 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H5324  forditas   10 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H5674  forditas   69 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H5797  forditas   13 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H5869  forditas   43 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H5971  forditas   24 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H6086  forditas   13 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H6213  forditas   45 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H6240  forditas   35 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H6242  forditas   20 sor  mezők: hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('elakad', 'illeszkedik'): 1}
H6588  forditas   10 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H6942  forditas   38 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('horgonnyal', 'illeszkedik'): 4, ('elakad', 'illeszkedik'): 16}
H7122  forditas    8 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7200  forditas   61 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7218  forditas   23 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7227  forditas   17 sor  mezők: hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('elakad', 'illeszkedik'): 7}
H7323  forditas    6 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7626  forditas   13 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('horgonnyal', 'illeszkedik'): 1}
H7651  forditas   18 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('horgonnyal', 'illeszkedik'): 1}
H7657  forditas   14 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7673  forditas   18 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7725  forditas   74 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7896  forditas    8 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7901  forditas   18 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('elakad', 'illeszkedik'): 6, ('horgonnyal', 'illeszkedik'): 1}
H7969  forditas   14 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7971  forditas   42 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H7993  forditas   20 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H8034  illesztes   2 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H8064  forditas   14 sor  mezők: horgony,hu_hossz,hu_kezdet,kategoria,szoveg_hu  kategória: {('horgonnyal', 'illeszkedik'): 1}
H8074  forditas   12 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H8083  forditas   16 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H8130  forditas   14 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H8337  forditas   14 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H8415  forditas    5 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H8672  forditas   13 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H9004  illesztes   2 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -
H9008  forditas    9 sor  mezők: hu_hossz,hu_kezdet,szoveg_hu  kategória: -

ok szerint: {'forditas': 98, 'illesztes': 3}
mezők (sor): {'forditas_forras_hash': 1685, 'hu_hossz': 1321, 'szoveg_hu': 1368, 'hu_kezdet': 1391, 'kategoria': 184, 'horgony': 22}

== rontás-jelöltek: 49 sor ==
H2091 5 -/3/- (forditas): illeszkedik → elakad | régi: '3 az arany mint hadizsákmány Józs 6:19 (+ בַּרְזֶל כְּלֵינְֿחשֶׁת, כֶּס' | új: ''
H2091 6 -/4/- (forditas): illeszkedik → elakad | régi: '4 az arany mint árucikk Ez 27:22 (+ כָּלבּֿשֶֹׁם ראֹשׁ יְקָרָה, אֶבֶן),' | új: ''
H2091 7 -/5/- (forditas): illeszkedik → elakad | régi: '5 az arany mint drága ajándék: prófétának וְז כֶּסֶף בֵּיתוֺ ׳מְלֹא (f' | új: ''
H2091 8 -/6/- (forditas): illeszkedik → elakad | régi: '6 az arany mint anyag: (orr- vagy fül-) gyűrűről, נֶזֶם 1Móz 24:22; 2M' | új: ''
H2091 9 -/7/- (forditas): illeszkedik → elakad | régi: '7 az arany származási helye szerint megnevezve, különösen az ofíri ara' | új: ''
H2091 10 -/8/- (forditas): illeszkedik → horgonnyal | régi: '8 az arany különféle melléknevekkel és participiumokkal meghatározva: ' | új: '7:50) 10:16; 12:28; 14:26; 2Krón 4:7-8, 19; 12:9; 13:8, és különösen P'
H2091 12 -/9/a (forditas): illeszkedik → elakad | régi: 'a. = aranysékel, ז ׳עֲשָׂרָה מִשְׁקָלָם 1Móz 24:22; ז עֲשָׂרָה אַחַת ׳כַּ' | új: ''
H2091 16 -/10/- (forditas): horgonnyal → elakad | régi: '10 ׳ז = aranyos olaj, a színéről, Zak 4:12.' | új: ''
H2091 17 -/11/- (forditas): illeszkedik → elakad | régi: '11 a ׳ז-ot gyakran a כֶּסֶף-tel együtt említik, és ilyenkor a korábbi ' | új: ''
H2091 18 -/12/- (forditas): illeszkedik → elakad | régi: '12 a ׳ז-mal használt fő igék:' | új: ''
H2091 19 -/12/a (forditas): illeszkedik → elakad | régi: 'a. עָשָׂה készíteni valamiből (két tárgyesettel) 1Kir 7:48 (vö. 7:49; 7' | új: ''
H2091 20 -/12/b (forditas): illeszkedik → elakad | régi: 'b. יָצַק (tárgya ז ׳טַבְּעֹת) 2Móz 25:12; 37:3, 13 (mind P);' | új: ''
H2091 21 -/12/c (forditas): illeszkedik → elakad | régi: 'c. צִמָּה bevonni valamivel (két tárgyesettel) 1Kir 6:20-21, (a versbe' | új: ''
H2091 22 -/12/d (forditas): illeszkedik → horgonnyal | régi: 'd. ז ׳וַיְחַמֵּהוּ 2Krón 3:5, vö. 3:7; 3:8; 3:9, és' | új: 'd. ז ׳וַיְחַמֵּהוּ 2Krón 3:5 vö. 3:7; 3:8; 3:9, és'
H2568 12 -/2/a (forditas): illeszkedik → elakad | régi: 'a. עֶשְׂרֵה חֲמֵשׁ (c. nőnemű főnévvel) 1Móz 5:10; 7:20; 2Móz 27:14-15, ' | új: ''
H2568 17 -/3/- (forditas): illeszkedik → elakad | régi: '3 מֵאוֺת חֲמֵשׁ = 500 1Móz 5:30, 32 összesen 49-szer + Ez 42:16 Qr.' | új: ''
H2568 18 -/4/- (forditas): illeszkedik → elakad | régi: '4 אֲלָפִים חֲמֵשֶׁת = 5000 4Móz 31:32; Józs 8:12; Bír 20:45; 1Sám 17:5;' | új: ''
H2568 19 -/5/- (forditas): illeszkedik → elakad | régi: '5 más számnevekkel:' | új: ''
H2568 20 -/5/a (forditas): illeszkedik → elakad | régi: 'a. חָמֵשׁ nagyobb számnév előtt: (1) a főnév megismételve 1Móz 5:6 össz' | új: ''
H2568 21 -/5/b (forditas): illeszkedik → elakad | régi: 'b. חָמֵשׁ nagyobb szám után: (1) a főnév megismételve 1Móz 25:7; (2) a ' | új: ''
H2568 22 -/5/c (forditas): illeszkedik → elakad | régi: 'c. kitett főnév nélkül, ׳ח más számok között, pl. ח מאות ׳שֵׁשׁ ושׁבעים 4' | új: ''
H2568 23 -/5/d (forditas): illeszkedik → horgonnyal | régi: 'd. חֲמִשָּׁה nagyobb szám előtt, a főnév a nagyobb szám után 4Móz 1:25' | új: 'd. חֲמִשָּׁה a nagyobb szám előtt, a főnév a nagyobb szám után követke'
H3092 3 -/1/- (forditas): illeszkedik → elakad | régi: '1 a ׳יְהוֺ (így mindenki, kivéve az 5-öt és a 6-ot) Júda királya, Ászá' | új: ''
H3117 9 -/2/- (forditas): illeszkedik → elakad | régi: '2. összekapcsolódik: וָיוֺם לַיְלָה יָמִים שְׁלשֶׁת וְאַלתִּֿשְׁתּוּ ne e' | új: ''
H3117 10 -/3/- (forditas): illeszkedik → elakad | régi: '3 י ׳יוֺם az Úr napja, főleg mint az ítéletre való eljövetelének ideje' | új: ''
H3117 11 -/3/d (forditas): illeszkedik → elakad | régi: 'd. יוֺם status constructusban igéket határoz meg, mind szó szerint: va' | új: ''
H3117 12 -/3/e (forditas): illeszkedik → elakad | régi: 'e. R. 1, 2 és különösen Dr 1Sám 1:4; 19:3); הַזֶּה בַּיּוֺם 1Móz 7:11 ' | új: ''
H3117 15 -/3/h (forditas): illeszkedik → elakad | régi: 'h. ׃כְּ כַּיּוֺם-val: mint a nap, a naphoz hasonlóan Zsolt 139:12; הַה' | új: ''
H3117 16 -/3/i (forditas): illeszkedik → elakad | régi: 'i. ׃לְ לְיוֺם-val: -kor, valamikor (szó szerint: valamire vonatkozóan)' | új: ''
H3117 46 -/7/j (forditas): illeszkedik → elakad | régi: 'j. ׃מִן מִיּוֺם-val: attól a naptól (időtől) fogva, (amikor), 2Móz 10:' | új: ''
H3117 47 -/7/k (forditas): illeszkedik → elakad | régi: 'k. לְמִן-val (l. לְ a vége felé): אֲשֶׁר הַיּוֺם לְמִן 5Móz 4:32; 9:7; ' | új: ''
H3117 48 -/1/- (forditas): illeszkedik → elakad | régi: '1 וגו הָאֶחָד יוֺם ׳עַד (ה)יום ׃עַד 2Móz 12:18 a 21. napig, 3Móz 19:6 ' | új: ''
H5307 19 Hiph'il/-/- (forditas): illeszkedik → elakad | régi: 'Hiph`il Ézs 26:19); = elébe terjesztetni, könyörgésről (י ׳לִפְנֵי) Je' | új: ''
H5307 21 Hiph'il/1/a (forditas): illeszkedik → elakad | régi: 'a. fát kivágni 2Kir 3:19, 25; vö. 6:5.' | új: ''
H5307 22 Hiph'il/1/b (forditas): illeszkedik → elakad | régi: 'b. falat ledönteni 2Sám 20:15.' | új: ''
H5307 23 Hiph'il/1/c (forditas): illeszkedik → elakad | régi: 'c. fogat kiütni 2Móz 21:27 (E).' | új: ''
H5307 24 Hiph'il/1/d (forditas): illeszkedik → elakad | régi: 'd. leteríteni 5Móz 25:2 (botozáshoz).' | új: ''
H5307 25 Hiph'il/1/e (forditas): illeszkedik → elakad | régi: 'e. (cédrusoszlopokat) tűzbe (עַלֿ) vetni Jer 22:7; így (ב vonzattal) g' | új: ''
H5307 26 Hiph'il/1/f (forditas): illeszkedik → elakad | régi: 'f. a kardot kiejteni a (מִן) kézből Ez 30:22 (átvitt értelemben), vö. ' | új: ''
H5307 27 Hiph'il/1/g (forditas): illeszkedik → elakad | régi: 'g. követ ráejteni עַל 4Móz 35:23, húst Zsolt 78:28 (בְּקֶרֶב), csillag' | új: ''
H5307 30 Hiph'il/4/- (forditas): illeszkedik → elakad | régi: '4 Átvitt értelemben elejteni, meghiúsítani (vö. Qal 5), Bír 2:19; Eszt' | új: ''
H5307 31 Hiph'il/5/- (forditas): illeszkedik → elakad | régi: '5 Mély álmot bocsátani (עַלֿ) 1Móz 2:21 (J), Péld 19:15 (abszolút hasz' | új: ''
H5307 32 Hiph'il/6/- (forditas): illeszkedik → elakad | régi: '6 Egyéb szólások: életre hozni (tulajdonképpen: fiat ellik) Ézs 26:19 ' | új: ''
H5307 33 Hithpa'el/-/- (forditas): illeszkedik → elakad | régi: 'Hithpa`el vetni magát vagy leborulni, 1 infinitivus constructus הִתְנַ' | új: ''
H5307 34 Hithpa'el/1/- (forditas): illeszkedik → elakad | régi: '1. egyes szám הִתְנַמָּ֑לְתִּי 5Móz 9:25; imperfectum 1. egyes szám וָ' | új: ''
H5307 35 Hithpa'el/2/- (forditas): illeszkedik → elakad | régi: '2. hímnemű többes szám תִּמְּלוּן 3:5, 15; participium többes szám נָֽ' | új: ''
H5307 39 Pe'al/1/- (forditas): illeszkedik → elakad | régi: '1 esni, עַלאַֿנְמּוֺהִי Dán 2:46; leborulni és hódolni 3:5-6, 7, 10, 1' | új: ''
H5307 40 Pe'al/2/- (forditas): illeszkedik → horgonnyal | régi: '2 erőszak által elesni Dán 7:20 (קֳדָם vonzattal).' | új: '7:20 neked jut (szükséged lesz rá), hogy add (vö. keresztény-palesztin'
H5307 41 Pe'al/3/- (forditas): illeszkedik → elakad | régi: '3 לָךְ יִמֵּל Ezsd 7:20 neked jut (neked lesz szükséged rá), hogy adj ' | új: ''

== 30 véletlen új Strong (mag: 20261029) ==

H0857  4 sor  {'jelolo_nelkul': 2, 'illeszkedik': 2}
  1 cim          jelolo_nelkul EN:  H857. athah                                                 | HU: 
  2 fej          jelolo_nelkul EN:  אָתָה verb come (in Hebrew only poetry) (Arabic , Sabean את | HU: H857. athah אָתָה ige jön (a hébernél csak költészetben) (ar
  3 Qal/-/-      illeszkedik   EN: Qal Perfect ׳א Deut 33:2; אָתָא Isa 21:12 see Ges^§ 75 R. 22 | HU: Qal perfectum ׳א 5Móz 33:2; אָתָא Ézs 21:12 l. Ges^§ 75 R. 2
  4 Hiph'il/-/-  illeszkedik   EN: Hiph`il bring, Imperative מַיִם הֵתָ֫יוּ Isa 21:14 bring wat | HU: Hiph`il elhoz, imperativus מַיִם הֵתָ֫יוּ Ézs 21:14 hozzatok

H1067  2 sor  {'jelolo_nelkul': 2}
  1 cim          jelolo_nelkul EN:  H1067. bekirah                                              | HU: 
  2 fej          jelolo_nelkul EN:  בְּכִירָה noun feminine first-born, always of women Gen 19: | HU: H1067. bekirah בְּכִירָה nőnemű főnév elsőszülött, mindig nő

H1396  12 sor  {'jelolo_nelkul': 5, 'illeszkedik': 7}
  1 cim          jelolo_nelkul EN:  H1396. gabar                                                | HU: 
  2 fej          jelolo_nelkul EN:  גָּבַר verb be strong, mighty (Late Hebrew id. Aramaic גְּב | HU: H1396. gabar גָּבַר ige erős, hatalmas (késői héber ugyanaz 
  3 Qal/-/-      illeszkedik   EN: Qal Perfect ׳ג Psa 103:11 5t.; גָּבְרוּ Gen 7:19 6t.; גָּבֵ֑ | HU: Qal perfectum ׳ג Zsolt 103:11 5-ször; גָּבְרוּ 1Móz 7:19 6-s
  4 Qal/1/-      illeszkedik   EN: 1 be strong, mighty, absolute חַיִל גָּבְרוּ mighty in power | HU: 1 erős, hatalmas, önállóan חַיִל גָּבְרוּ hatalmas erőben Jó
  5 Qal/2/-      illeszkedik   EN: 2 prevail: —                                                 | HU: 2 felülkerekedik: — a önállóan pl. ellenségek 2Móz 17:11 (a 
  6 Qal/2/-      jelolo_nelkul EN:  a absolute e.g. enemies Exod 17:11 (twice in verse) (E) 1Sa | HU: 
  7 Qal/2/b      illeszkedik   EN: b. with עַל prevail over, subject enemies 2Sam 11:23, blessi | HU: b. עַל-val felülkerekedik fölött, alanya ellenségek 2Sám 11:
  8 Pi'el/-/-    illeszkedik   EN: Pi`el Perfect גִּבַּרְתִּי Zech 10:6; suffix גִּבַּרְתִּים 1 | HU: Pi`el perfectum גִּבַּרְתִּי Zak 10:6; suffixummal גִּבַּרְת
  9 Hiph'il/-/-  illeszkedik   EN: Hiph`il Perfect לְ בְּרִית הִגְבִּיר confirm a covenant Dan  | HU: Hiph`il perfectum לְ בְּרִית הִגְבִּיר szövetséget megerősít
  10 Hithpa'el/-/- illeszkedik   EN: Hithpa`el Imperfect יִתְגַּבָּ֑ר Job 15:25; Isa 42:13; יִתְג | HU: Hithpa`el imperfectum יִתְגַּבָּ֑ר Jób 15:25; Ézs 42:13; יִת
  11 Hithpa'el/-/- jelolo_nelkul EN:  גִּבַר see following.                                       | HU: 
  12 fej          jelolo_nelkul EN:  גבר (√ of following; be strong, so ᵑ7; Biblical Hebrew גָּב | HU: 

H1538  4 sor  {'jelolo_nelkul': 2, 'illeszkedik': 2}
  1 cim          jelolo_nelkul EN:  H1538. gulgoleth                                            | HU: 
  2 fej          jelolo_nelkul EN:  גֻּלְגֹּ֫לֶת noun feminine skull, head, poll (person) (on f | HU: H1538. gulgoleth גֻּלְגֹּ֫לֶת nőnemű főnév koponya, fej, sze
  3 -/1/-        illeszkedik   EN: 1 skull, as broken by a stone Judg 9:53; as severed from bod | HU: 1 koponya, mint kővel összezúzott Bír 9:53; mint a testtől e
  4 -/2/-        illeszkedik   EN: 2 head, poll (in counting, taxing, etc.; only P and late) לַ | HU: 2 fej, személy (összeszámlálásban, adóztatásban stb.; csak P

H1851  4 sor  {'jelolo_nelkul': 2, 'illeszkedik': 2}
  1 cim          jelolo_nelkul EN:  H1851. daq                                                  | HU: 
  2 fej          jelolo_nelkul EN:  דַּק adjective thin, small, fine — absolute masculine ׳דּ E | HU: H1851. daq דַּק melléknév vékony, apró, finom — absolutus hí
  3 -/1/-        illeszkedik   EN: 1 thin, of kine ׳דּ בָּשָׂר Gen 41:3 compare 41:4 (⅏ has in b | HU: 1 vékony, tehenekről ׳דּ בָּשָׂר 1Móz 41:3 vö. 41:4 (⅏ mindke
  4 -/2/-        illeszkedik   EN: 2 small, fine, of the manna כַּכְּפֹר דַּק מְחֻסְמָּס דַּק E | HU: 2 apró, finom, a mannáról כַּכְּפֹר דַּק מְחֻסְמָּס דַּק 2Mó

H2354  8 sor  {'jelolo_nelkul': 3, 'illeszkedik': 5}
  1 cim          jelolo_nelkul EN:  H2354. Chur                                                 | HU: 
  2 fej          jelolo_nelkul EN:  II. חוּר proper name, masculine (meaning dubious; compare N | HU: H2354. Chur II. חוּר tulajdonnév, hímnemű (jelentése kétsége
  3 -/1/-        illeszkedik   EN: 1 ᵐ5 Ωρ, named with Aaron as compan. of Moses Exod 17:10, 12 | HU: 1 ᵐ5 Ωρ, Áron mellett említve mint Mózes társa 2Móz 17:10, 1
  4 -/2/-        illeszkedik   EN: 2 ᵐ5 Ωρ, a Judahite Exod 31:2 = 35:30, compare 38:22 (all P) | HU: 2 ᵐ5 Ωρ, egy júdabeli 2Móz 31:2 = 35:30, vö. 38:22 (mind P) 
  5 -/3/-        illeszkedik   EN: 3 ᵐ5 Ουρ, a king of Midian Num 31:8; Josh 13:21 (both P).    | HU: 3 ᵐ5 Ουρ, Midián királya 4Móz 31:8; Józs 13:21 (mindkettő P)
  6 -/4/-        illeszkedik   EN: 4 ᵐ5^L Εουρ (B omitted) head of fam. of returned exiles Neh  | HU: 4 ᵐ5^L Εουρ (B kihagyja) a hazatért száműzöttek egy családfő
  7 -/5/-        illeszkedik   EN: 5 בֶּןחֿוּר officer of Solomon 1Kin 4:8, see below בֵּן p. 1 | HU: 5 בֶּןחֿוּר Salamon tisztje 1Kir 4:8, l. alább בֵּן o. 122. 
  8 fej          jelolo_nelkul EN:  III. חוּר = חֻר see below III. חרר.                         | HU: 

H2399  8 sor  {'jelolo_nelkul': 3, 'illeszkedik': 5}
  1 cim          jelolo_nelkul EN:  H2399. chet                                                 | HU: 
  2 fej          jelolo_nelkul EN:  חֵטְא noun masculine^Deut 15:9 sin (on formation see Lag^ B | HU: H2399. chet חֵטְא főnév hímnemű^5Móz 15:9 vétek (a képzésről
  3 -/1/-        illeszkedik   EN: 1 sin:                                                       | HU: 1 vétek:
  4 -/1/a        illeszkedik   EN: a. against man Gen 41:9 (E) Eccl 10:4.                       | HU: a. ember ellen 1Móz 41:9 (E) Préd 10:4.
  5 -/1/b        illeszkedik   EN: b. elsewhere ag. God, absolute Isa 31:7; Hosea 12:9; ׳ח חָטָ | HU: b. másutt Isten ellen, önállóan Ézs 31:7; Hós 12:9; ׳ח חָטָא
  6 -/2/-        illeszkedik   EN: 2 guilt of sin: ב חטא היה sin (the guilt of sin) come on one | HU: 2 a vétek bűne: ב חטא היה vétek (a vétek bűne) száll valakir
  7 -/3/-        illeszkedik   EN: 3 punishment for sin: ח ׳נשׂא bear sin (its punishment) Lev 2 | HU: 3 büntetés a vétekért: ח ׳נשׂא viseli a vétket (büntetését) 3
  8 fej          jelolo_nelkul EN:  [חֲטָי] noun [masculine] sin (see Biblical Hebrew חטא); — s | HU: 

H2553  2 sor  {'jelolo_nelkul': 2}
  1 cim          jelolo_nelkul EN:  H2553. chamman                                              | HU: 
  2 fej          jelolo_nelkul EN:  [חַמָּן] noun masculine sun-pillar, used in idolatrous wors | HU: H2553. chamman [חַמָּן] hímnemű főnév naposzlop, bálványimád

H2658  7 sor  {'jelolo_nelkul': 2, 'illeszkedik': 5}
  1 cim          jelolo_nelkul EN:  H2658. chaphar                                              | HU: 
  2 fej          jelolo_nelkul EN:  I. חָפַר verb dig, search for (Arabic id.; Aramaic חֲפַר, , | HU: H2658. chaphar I. חָפַר ige ás, keres (arab ugyanaz; arámi ח
  3 Qal/-/-      illeszkedik   EN: Qal Perfect ׳ח Job 39:29; וְחָפַרְתָּ֫ 11:18; וְחָפַרְתָּ֫ה  | HU: Qal perfectum ׳ח Jób 39:29; וְחָפַרְתָּ֫ 11:18; וְחָפַרְתָּ֫
  4 Qal/1/-      illeszkedik   EN: 1 dig:                                                       | HU: 1 ás:
  5 Qal/1/a      illeszkedik   EN: a. a well, with accusative בְּאֵר Gen 21:30 (E), 26:15, 18 ( | HU: a. kutat, tárgyesettel בְּאֵר 1Móz 21:30 (E), 26:15, 18 (a v
  6 Qal/1/b      illeszkedik   EN: b. dig for something hidden, with accusative Job 3:21 (figur | HU: b. valami rejtettet keres ásva, tárgyesettel Jób 3:21 (átvit
  7 Qal/2/-      illeszkedik   EN: 2 search, search out, explore, with accusative הָאָרֶץ Josh  | HU: 2 kutat, kikutat, felderít, tárgyesettel הָאָרֶץ Józs 2:3 (a

H2722  2 sor  {'jelolo_nelkul': 2}
  1 cim          jelolo_nelkul EN:  H2722. Choreb                                               | HU: 
  2 fej          jelolo_nelkul EN:  חוֺרֵב חֹרֵב, proper name, of a mountain Horeb (waste, dese | HU: H2722. Choreb חוֺרֵב חֹרֵב, tulajdonnév, hegyé Hóreb (puszta

H2836  8 sor  {'jelolo_nelkul': 3, 'illeszkedik': 5}
  1 cim          jelolo_nelkul EN:  H2836. chashaq                                              | HU: 
  2 fej          jelolo_nelkul EN:  I. חָשַׁק verb be attached to, love (Late Hebrew press toget | HU: H2836. chashaq I. חָשַׁק ige ragaszkodik valakihez, szeret (k
  3 Qal/-/-      illeszkedik   EN: Qal Perfect ׳ח Deut 7:7 4t.; חָֽשְׁקָה Gen 34:8; חָשַׁקְתָּ Is | HU: Qal perfectum ׳ח 5Móz 7:7 összesen 4-szer; חָֽשְׁקָה 1Móz 34:
  4 fej          jelolo_nelkul EN:  II. [חשׁק] verb denominative only                            | HU: 
  5 Pi'el/-/-    illeszkedik   EN: Pi`el furnish with fillets or rings, and                     | HU: Pi`el pántokkal vagy gyűrűkkel ellát, és
  6 Pu'al/-/-    illeszkedik   EN: Pu`al passive;                                               | HU: Pu`al szenvedő;
  7 Pi'el/-/-    illeszkedik   EN: Pi`el Perfect3masculine singular חִשַּׁק Exod 38:28 (P), sub | HU: Pi`el perfectum 3. hímnemű egyes szám חִשַּׁק 2Móz 38:28 (P)
  8 Pu'al/-/-    illeszkedik   EN: Pu`al Participle כֶּסֶף מְחֻשָּׁקִים Exod 27:17; 38:17 finis | HU: Pu`al participium כֶּסֶף מְחֻשָּׁקִים 2Móz 27:17; 38:17 ezüs

H2976  6 sor  {'jelolo_nelkul': 4, 'illeszkedik': 2}
  1 cim          jelolo_nelkul EN:  H2976. yaash                                                | HU: 
  2 fej          jelolo_nelkul EN:  [יָאַשׁ] verb despair (not in                                | HU: H2976. yaash [יָאַשׁ] ige kétségbeesik (nincs Qal-ban) (késői
  3 fej          jelolo_nelkul EN:  Qal) (Late Hebrew Hithpa`el despair of, יֵאוּשׁ desperation; | HU: 
  4 Niph'al/-/-  illeszkedik   EN: Niph`al Perfect וְנוֺאַש consecutive 1Sam 27:1; Participle נ | HU: Niph`al perfectum וְנוֺאַש consecutivummal 1Sám 27:1; partic
  5 Pi'el/-/-    illeszkedik   EN: Pi`el Infinitive כָּלהֶֿעָמָל עַל אֶתלִֿבִּי לְיַאֵשׁ Eccl 2: | HU: Pi`el infinitivus כָּלהֶֿעָמָל עַל אֶתלִֿבִּי לְיַאֵשׁ Préd 2
  6 Pi'el/-/-    jelolo_nelkul EN:  יאֹשִׁיָּה יאֹשִׁיָּ֫הוּ, see below אשׁה above                 | HU: 

H3779  4 sor  {'jelolo_nelkul': 2, 'illeszkedik': 2}
  1 cim          jelolo_nelkul EN:  H3779. Kasday                                               | HU: 
  2 fej          jelolo_nelkul EN:  כַּשְׂדָּ֑י proper name, of a people Chaldean (see Biblical  | HU: H3779. Kasday כַּשְׂדָּ֑י tulajdonnév, népnév káldeus (l. bib
  3 -/1/-        illeszkedik   EN: 1 Chaldean By race Dan 3:8; 5:30; Ezra 5:12.                 | HU: 1 káldeus származású Dán 3:8; 5:30; Ezsd 5:12.
  4 -/2/-        illeszkedik   EN: 2 as learned, of the class of Magi (Biblical Hebrew ׳כ 1c),  | HU: 2 mint tudós, a mágusok osztályából (bibliai héber ׳כ 1c), D

H3926  4 sor  {'jelolo_nelkul': 4}
  1 cim          jelolo_nelkul EN:  H3926. lemo                                                 | HU: 
  2 fej          jelolo_nelkul EN:  לְמוֺ in poetry for לְ (see מוֺ) Job 27:14; 29:21; 38:40; 4 | HU: H3926. lemo לְמוֺ költészetben לְ helyett (l. מוֺ) Jób 27:14
  3 fej          jelolo_nelkul EN:  לְמוֺ in poetry for לְ, Job 27:14; 29:21; 38:40; 40:4, like | HU: 
  4 fej          jelolo_nelkul EN:  לְמוֺ in poetry for לְ.                                     | HU: 

H4612  5 sor  {'jelolo_nelkul': 2, 'illeszkedik': 3}
  1 cim          jelolo_nelkul EN:  H4612. maamad                                               | HU: 
  2 fej          jelolo_nelkul EN:  [מַעֲמָד] noun [masculine] office, function, service; —     | HU: H4612. maamad [מַעֲמָד] főnév [hímnemű] hivatal, tisztség, s
  3 -/1/-        illeszkedik   EN: 1 station, office, post (מַעֲמָֽדְךָ) Isa 22:19 (|| מַצָּֽבְ | HU: 1 állomás, hivatal, őrhely (מַעֲמָֽדְךָ) Ézs 22:19 (|| מַצָּ
  4 -/2/-        illeszkedik   EN: 2 office, function 1Chr 23:28.                               | HU: 2 hivatal, tisztség 1Krón 23:28.
  5 -/3/-        illeszkedik   EN: 3 service, probably specifically waiting at table (strictly  | HU: 3 szolgálat, valószínűleg konkrétan az asztalnál felszolgálá

H4617  2 sor  {'jelolo_nelkul': 2}
  1 cim          jelolo_nelkul EN:  H4617. maaneh                                               | HU: 
  2 fej          jelolo_nelkul EN:  מַעֲנֶה noun masculine^Prov 15:1 answer, response; — absolu | HU: H4617. maaneh מַעֲנֶה hímnemű főnév^Péld 15:1 válasz, felele

H4843  13 sor  {'jelolo_nelkul': 2, 'illeszkedik': 10, 'horgonnyal': 1}
  1 cim          jelolo_nelkul EN:  H4843. marar                                                | HU: 
  2 fej          jelolo_nelkul EN:  I. מָרַר verb be bitter (Late Hebrew id.; Assyrian marâru a | HU: H4843. marar I. מָרַר ige keserű lenni (késői héber ua.; ass
  3 Qal/-/-      illeszkedik   EN: Qal Perfect3masculine singular מַר Isa 38:17 2t.; 3 feminine | HU: Qal perfectum 3. hímnemű egyes szám מַר Ézs 38:17 összesen 2
  4 Qal/1/-      illeszkedik   EN: 1 literal לְשֹׁתָיו שֵׁכָר יֵמַר Isa 24:9.                     | HU: 1 szó szerint לְשֹׁתָיו שֵׁכָר יֵמַר Ézs 24:9.
  5 Qal/2/-      illeszkedik   EN: 2 figurative נֶפֶשׁ מָ֫רָה 1Sam 30:6 the soul of all the peop | HU: 2 képletesen נֶפֶשׁ מָ֫רָה 1Sám 30:6 az egész nép lelke megke
  6 Pi'el/-/-    illeszkedik   EN: Pi`el Imperfect1singular אֲמָרֵר Isa 22:4; 3masculine plural | HU: Pi`el imperfectum
  7 Pi'el/1/-    illeszkedik   EN: 1 ׳וַיְמ Gen 49:23 (poem) and the archers shewed bitterness  | HU: 1. egyes szám אֲמָרֵר Ézs 22:4; 3. hímnemű többes szám וַיְמ
  8 Pi'el/2/-    illeszkedik   EN: 2 ׳וַיְמ אֶתחַֿיֵּיהֶם Exod 1:14 (P) and they made their liv | HU: 2. hímnemű egyes szám תַּמֵּר 2Móz 23:21 (de olv. תֶּ֫מֶר √ 
  9 Hiph'il/-/-  illeszkedik   EN: Hiph`il Perfect3masculine singular הֵמַר Ruth 1:20; Job 27:2 | HU: Hiph`il l. ott);
  10 Hiph'il/-/-  horgonnyal    EN: Hiph`il q. v.); Infinitive absolute הָמֵר Zech 12:10 (twice  | HU: infinitivus absolutus הָמֵר Zak 12:10 (a versben kétszer); —
  11 Hiph'il/1/-  illeszkedik   EN: 1 נַפְשִׁי הֵמַר שַׁדַּי Job 27:2 Shadday, who hath embittered | HU: 1 נַפְשִׁי הֵמַר שַׁדַּי Jób 27:2 Sadaj, aki megkeserítette le
  12 Hiph'il/2/-  illeszkedik   EN: 2 עַלהַֿבְּכוֺר כְּהָמֵר עָלָיו וְהָמֵר Zech 12:10 and a bit | HU: 2 עַלהַֿבְּכוֺר כְּהָמֵר עָלָיו וְהָמֵר Zak 12:10 és keserve
  13 Hithpalpel/-/- illeszkedik   EN: Hithpalpel Imperfect וְיִתְמַרְמַר Dan 11:11 and the king of | HU: Hithpalpel imperfectum וְיִתְמַרְמַר Dán 11:11 és a déli kir

H5011  5 sor  {'jelolo_nelkul': 3, 'illeszkedik': 1, 'horgonnyal': 1}
  1 cim          jelolo_nelkul EN:  H5011. Nob                                                  | HU: 
  2 fej          jelolo_nelkul EN:  נֹב proper name, of a location1. ancient priestly city 1Sam | HU: H5011. Nob נֹב tulajdonnév, helynév1. ősi papi város 1Sám 22
  3 -/2/-        illeszkedik   EN: 2 Isa 10:32 just north of Jerusalem, station in (ideal) Assy | HU: 2 Ézs 10:32 közvetlenül Jeruzsálemtől északra, állomás az (e
  4 -/1/-        horgonnyal    EN: 1 — 2Sam 21:6 read גֹּב (q. v. p.146 above)                  | HU: 1 — 2Sám 21:6 olv. גֹּב (l. ott o.146 fent) נבא (a következő
  5 fej          jelolo_nelkul EN:  נבא (√ of following; **see in Biblical Aramaic Appendix. Ew | HU: 

H5031  6 sor  {'jelolo_nelkul': 2, 'illeszkedik': 4}
  1 cim          jelolo_nelkul EN:  H5031. nebiah                                               | HU: 
  2 fej          jelolo_nelkul EN:  נְבִיאָה noun masculine prophetess; —                       | HU: H5031. nebiah נְבִיאָה főnév hímnemű prófétanő; —
  3 -/1/a        illeszkedik   EN: 1. a. of the ancient type endowed with gift of song, Miriam  | HU: 1. a. az ősi típusból, az énekajándékkal megáldott, Mirjám 2
  4 -/1/b        illeszkedik   EN: b. of the later type consulted for a word of ׳י, Huldah 2Kin | HU: b. a későbbi típusból, akit ׳י szavára kérdeztek meg, Hulda 
  5 -/2/-        illeszkedik   EN: 2 false prophetess, Noadiah Neh 6:14.                        | HU: 2 hamis prófétanő, Noádia Neh 6:14.
  6 -/3/-        illeszkedik   EN: 3 wife of Isaiah Isa 8:3.                                    | HU: 3 Ézsaiás felesége Ézs 8:3.

H5445  5 sor  {'jelolo_nelkul': 2, 'illeszkedik': 3}
  1 cim          jelolo_nelkul EN:  H5445. sabal                                                | HU: 
  2 fej          jelolo_nelkul EN:  [סָבַל] verb bear a heavy load (Late Hebrew id.; Arabic סְב | HU: H5445. sabal [סָבַל] ige nehéz terhet hord (késői héber ua.;
  3 Qal/-/-      illeszkedik   EN: Qal Perfect3masculine singular suffix סְבָלָם Isa 53:4; 1plu | HU: Qal perfectum 3. hímnemű egyes szám suffixummal סְבָלָם Ézs 
  4 Pu'al/-/-    illeszkedik   EN: Pu`al Participle plural מְסֻבָּלִים laden, Psa 144:14 (i.e.  | HU: Pu`al participium többes szám מְסֻבָּלִים megrakott, Zsolt 1
  5 Hithpa'el/-/- illeszkedik   EN: Hithpa`el Imperfect הֶחָגָב וְיִסְתַּכֵּל Eccl 12:5 drag one | HU: Hithpa`el imperfectum הֶחָגָב וְיִסְתַּכֵּל Préd 12:5 vonszo

H5777  3 sor  {'jelolo_nelkul': 3}
  1 cim          jelolo_nelkul EN:  H5777. ophereth                                             | HU: 
  2 fej          jelolo_nelkul EN:  עֹפֶרֶת noun masculine^Jer 6:29 (si vera lectio Qr) lead (√ | HU: H5777. ophereth עֹפֶרֶת hímnemű főnév^Jer 6:29 (si vera lect
  3 fej          jelolo_nelkul EN:  עֵפָ֫תָה see עֵיפָה below II. עוף. עֵץ see II.עצה.          | HU: 

H6293  12 sor  {'jelolo_nelkul': 2, 'illeszkedik': 9, 'horgonnyal': 1}
  1 cim          jelolo_nelkul EN:  H6293. paga                                                 | HU: 
  2 fej          jelolo_nelkul EN:  מָּגַע verb meet, encounter, reach (Late Hebrew id.; Aramai | HU: H6293. paga מָּגַע ige: találkozni, szembetalálkozni, elérni
  3 Qal/-/-      illeszkedik   EN: Qal Perfect3masculine singular ׳פ 1Kin 2:32 +, suffix וּפְגָ | HU: Qal perfectum 3. hímnemű egyes szám ׳פ 1Kir 2:32 és máshol, 
  4 Qal/1/-      illeszkedik   EN: 1 meet, light upon, with accusative of person 1Sam 10:5; Exo | HU: 1. többes szám נְפְגַּע Jób 21:15, stb.; imperativus hímnemű
  5 Qal/2/-      illeszkedik   EN: 2 meet, with kindness, with accusative of person Isa 64:5 (s | HU: 2 találkozni, jósággal, személy tárgyesetével Ézs 64:5 (alan
  6 Qal/3/-      illeszkedik   EN: 3 encounter with hostility, fall upon with ב person Josh 2:1 | HU: 3 ellenségesen szembeszállni, rátámadni ב személlyel Józs 2:
  7 Qal/4/-      illeszkedik   EN: 4 encounter with request, entreat, with ב person Jer 7:16; J | HU: 4 kéréssel találkozni, könyörögni, ב személlyel Jer 7:16; Jó
  8 Qal/5/-      horgonnyal    EN: 5 strike, touch, of boundary, with ב location Josh 16:7; 19: | HU: 5 érinteni, érni, a határról, ב helyhatározóval Józs 16:7; 1
  9 Hiph'il/1/-  illeszkedik   EN: Hiph`il 1. cause to light upon, Perfect3masculine singular ה | HU: Hiph`il 1. ráhozni, perfectum 3. hímnemű egyes szám הִפְגִּי
  10 Hiph'il/2/-  illeszkedik   EN: 2 cause one (accusative) to entreat1singular הִפְגַּעְתִּי ( | HU: 2 valakit (tárgyeset) könyörgésre késztetni 1. egyes szám הִ
  11 Hiph'il/3/-  illeszkedik   EN: 3 make entreaty, 3 plural הִפְגִּעוּ Jer 36:25 with ב person | HU: 3 könyörgést tenni, 3. többes szám הִפְגִּעוּ Jer 36:25 ב sz
  12 Hiph'il/4/-  illeszkedik   EN: 4 make attack, only Participle Job 36:32 assailant, but Ol B | HU: 4 támadást intézni, csak participium Jób 36:32 támadó, de Ol

H6845  9 sor  {'jelolo_nelkul': 4, 'illeszkedik': 5}
  1 cim          jelolo_nelkul EN:  H6845. tsaphan                                              | HU: 
  2 fej          jelolo_nelkul EN:  צָפַן verb hide, treasure up (Late Hebrew id.; Tel Amarna ƒ | HU: H6845. tsaphan צָפַן ige elrejt, felhalmoz (késői héber ugya
  3 Qal/-/-      illeszkedik   EN: Qal Perfect3masculine singular ׳צ Prov 27:16: 2masculine sin | HU: Qal perfectum 3. hímnemű egyes szám ׳צ Péld 27:16: 2. hímnem
  4 Qal/1/-      illeszkedik   EN: 1 transitive hide, with accusative of person Exod 2:2 (E), J | HU: 1 áttételes elrejt, személy tárgyesetével 2Móz 2:2 (E), Józs
  5 Qal/2/-      illeszkedik   EN: 2 intransitive lie hid, lurk, absolute Psa 56:7, with ל pers | HU: 2 tárgyatlan elrejtőzve fekszik, lesben áll, önállóan Zsolt 
  6 Niph'al/-/-  illeszkedik   EN: Niph`al Perfect3masculine singular נִצְמֵּן Jer 16:17 be hid | HU: Niph`al perfectum 3. hímnemű egyes szám נִצְמֵּן Jer 16:17 e
  7 Hiph'il/-/-  illeszkedik   EN: Hiph`il hide, =                                              | HU: Hiph`il elrejt, = Qal: imperfectum 2. hímnemű egyes szám suf
  8 Hiph'il/-/-  jelolo_nelkul EN:  Qal: Imperfect2masculine singular suffix תַּצְמִּנֵנִי Job  | HU: 
  9 Hiph'il/-/-  jelolo_nelkul EN:  Qal); Infinitive construct suffix הַצְּפִינוֺ (Ges^§ 20h) E | HU: 

H7058  2 sor  {'jelolo_nelkul': 2}
  1 cim          jelolo_nelkul EN:  H7058. qemach                                               | HU: 
  2 fej          jelolo_nelkul EN:  קֶ֫מַח noun [masculine] flour, meal; — absolute ׳ק 1Sam 1:2 | HU: H7058. qemach קֶ֫מַח főnév [hímnemű] liszt, dara; — absolutu

H7292  4 sor  {'jelolo_nelkul': 2, 'illeszkedik': 2}
  1 cim          jelolo_nelkul EN:  H7292. rahab                                                | HU: 
  2 fej          jelolo_nelkul EN:  [רָהַב] verb act stormily, boisterously, arrogantly (Ecclus | HU: H7292. rahab [רָהַב] ige viharosan, zajosan, gőgösen cseleks
  3 Qal/-/-      illeszkedik   EN: Qal Imperfect3masculine plural בַּזָּקֵן הַנַּעַר יִרְחֲבוּ  | HU: Qal imperfectum 3. hímnemű többes szám בַּזָּקֵן הַנַּעַר יִ
  4 Hiph'il/-/-  illeszkedik   EN: Hiph`il Perfect3masculine plural suffix הִרְהִיבֻ֑נִי Song 6 | HU: Hiph`il perfectum 3. hímnemű többes szám suffixummal הִרְהִי

H7386  4 sor  {'jelolo_nelkul': 2, 'illeszkedik': 2}
  1 cim          jelolo_nelkul EN:  H7386. req                                                  | HU: 
  2 fej          jelolo_nelkul EN:  [רֵיק], רֵק adjective empty, vain — masculine absolute רֵק  | HU: H7386. req [רֵיק], רֵק melléknév üres, hiábavaló — hímnemű a
  3 -/1/-        illeszkedik   EN: 1 empty, of vessels 2Kin 4:3; Judg 7:16; Ezek 24:11 +? Jer 1 | HU: 1 üres, edényekről 2Kir 4:3; Bír 7:16; Ez 24:11 +? Jer 14:3 
  4 -/2/-        illeszkedik   EN: 2 empty, idle, worthless, ethically; ריקים אנשׁים worthless f | HU: 2 üres, tétlen, értéktelen, erkölcsileg; ריקים אנשׁים értékte

H7410  5 sor  {'jelolo_nelkul': 2, 'illeszkedik': 3}
  1 cim          jelolo_nelkul EN:  H7410. Ram                                                  | HU: 
  2 fej          jelolo_nelkul EN:  רָם proper name, masculine                                  | HU: H7410. Ram רָם tulajdonnév, hímnemű
  3 -/1/a        illeszkedik   EN: 1. a. an ancestor of David, Ruth 4:19 (twice in verse), brot | HU: 1. a. Dávid egyik őse, Ruth 4:19 (a versben kétszer), Jerach
  4 -/1/b        illeszkedik   EN: b. son of J. 1Chr 2:25, 27. — Αρραν, Ραμ, etc.               | HU: b. J. fia 1Krón 2:25, 27. — Αρραν, Ραμ, stb.
  5 -/2/-        illeszkedik   EN: 2 name of Elihu's family, Job 32:2 (Ραμ[α], Αραμ), dubious,  | HU: 2 Elihu családjának neve, Jób 32:2 (Ραμ[α], Αραμ), kétséges,

H7667  6 sor  {'jelolo_nelkul': 2, 'illeszkedik': 4}
  1 cim          jelolo_nelkul EN:  H7667. sheber                                               | HU: 
  2 fej          jelolo_nelkul EN:  I. שֵׁ֫בֶר שֶׁ֫בֶר, noun masculine^Jer 4:5 breaking, fracture | HU: H7667. sheber I. שֵׁ֫בֶר שֶׁ֫בֶר, főnév hímnemű^Jer 4:5 törés,
  3 -/1/-        illeszkedik   EN: 1 breaking of pottery Isa 30:14, fracture of member, limb Le | HU: 1 cserépedény törése Ézs 30:14, végtag, tag törése 3Móz 21:1
  4 -/2/-        illeszkedik   EN: 2 crashing, Zeph 1:10 (|| יְלָלָה צְעָקָה, קוֺל), Jer 50:22  | HU: 2 robaj, Sof 1:10 (|| יְלָלָה צְעָקָה, קוֺל), Jer 50:22 (|| 
  5 -/3/-        illeszkedik   EN: 3 breaking of a dream, i.e. its interpretation (solution of  | HU: 3 egy álom megtörése, azaz megfejtése (a titok megoldása) Bí
  6 -/4/-        illeszkedik   EN: 4 הַשְּׁבָרִים Josh 7:5, perhaps (Di Benn Steuern) the quarr | HU: 4 הַשְּׁבָרִים Józs 7:5, talán (Di Benn Steuern) a kőbányák 

H8266  8 sor  {'jelolo_nelkul': 6, 'illeszkedik': 2}
  1 cim          jelolo_nelkul EN:  H8266. shaqar                                               | HU: 
  2 fej          jelolo_nelkul EN:  [שָׁקַר] verb denominative do or deal falsely; —             | HU: H8266. shaqar [שָׁקַר] ige denominativum hamisan cselekszik v
  3 Qal/-/-      illeszkedik   EN: Qal Imperfect2masculine singular; תִּשְׁקֹר Gen 21:23 thou wi | HU: Qal imperfectum 2. hímnemű egyes szám; תִּשְׁקֹר 1Móz 21:23 n
  4 Pi'el/-/-    illeszkedik   EN: Pi`el Perfect1plural נוּ שִׁקַּ֫רְ Psa 44:18; Imperfect3mascu | HU: Pi`el perfectum 1. többes szám נוּ שִׁקַּ֫רְ Zsolt 44:18; imp
  5 Pi'el/-/-    jelolo_nelkul EN:  שִׁקֲתוֺת שֹׁקֶת, see שׁקה. שֹׁרsee שׁרר.                        | HU: 
  6 Pi'el/-/-    jelolo_nelkul EN:  שַׁרְאֶ֫צֶר                                                  | HU: 
  7 fej          jelolo_nelkul EN:  proper name, masculine see שַׂרְאֶ֫צֶר                       | HU: 
  8 fej          jelolo_nelkul EN:  שׁרב (√ of following, parch; Late Hebrew שָׁרַב be scorched ( | HU: 

H8370  2 sor  {'jelolo_nelkul': 2}
  1 cim          jelolo_nelkul EN:  H8370. Shethar                                              | HU: 
  2 fej          jelolo_nelkul EN:  Bozenay בּוֺזְנַי שְׁתַר proper name, masculine Persian offi | HU: H8370. Shethar Bozenay בּוֺזְנַי שְׁתַר tulajdonnév, hímnemű 

a minta kategóriái: {'jelolo_nelkul': 78, 'illeszkedik': 85, 'horgonnyal': 3}
```
