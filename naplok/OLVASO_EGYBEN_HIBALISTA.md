# Az olvasó nyitott hibái és el nem készült javításai — egy lista (2026-11-22)

Csak olvasás; a repóba nem írtam. Alap: `origin/main` @ `4cbefcae` (F230 és F232 beolvasztva; az F235 sebességág, az F231/F233/F234/F164/F134 még nem). Ellenőrzési módszer: a `main` olvasói pillanatképe (`eszkozok/olvaso_szerver/merce/*.txt`, az F232 rögzítette a mai állapotot) és a kód `git grep`-pel; élő szervert nem indítottam, ezért „biztosan nyitott” csak ott áll, ahol a pillanatkép, a kód vagy egy nyitott tétel ezt tényként mutatja. Ahol a pont a 2026-11-12-i felmérésből jön, és a mai állapotot nem mértem, ott „ellenőrizendő” áll (ezt az F233 M0 és az F234 hivatott eldönteni).

Rövidítések a forrásoknál: **F-OLV** = `OLVASO_BLOKK_ELLENORZES_2026-11-12.md` (pontszám = a felmérés sorszáma); **F-THAY** = `FELMERES_THAYER_OLVASO_SZOKARTYA_2026-11-21.md`; **F-BDBK** = `FABLE_VALASZ_BDB_KARTYA_2026-11-21.md`; **F-BDBT** = `FELMERES_BDB_THAYER_KJV_2026-11-12.md`; **F231/F233/F234/F235/F164/F134** = a `main` briefjei; **N…** = `NYITOTT_FELADATOK.md` tétel; **MERCE** = `eszkozok/olvaso_szerver/merce/<lap>.txt`; **FELH** = a felhasználó mai (2026-11-22) jelzése.

| # | A hiba egy mondatban (olvasói nyelven) | Példa-URL | Forrás | Terület | Mekkora | Állapot |
|---|---|---|---|---|---|---|
| 1 | A szeletelő kettévágja a felsorolást: a „b” pontban a „Krónikák (31-szer)” önálló pont, alatta a „Dán 11:37” fej nélkül áll. | /szo/H0430 | FELH; F231 §2.2 (tagolási jelző, szakaszonként egybefüggő szöveg); F-BDBK b) (alpontok a hivatkozásmezőben) | szókártya-BDB | nagy | biztosan nyitott |
| 2 | A hivatkozásmezőbe próza csúszik, és a sorfej átrendezi a mondatot (a „vö.” elöl, a magyarázat a helyek közé kerül), ezért a szócikk nehezen olvasható; mért arány: H1242 8/50, H7451 36/144, H3615 28/87 sor. | /szo/H1242, /szo/H7451 | F231 §1 (mérés); F-BDBK a)–b); MERCE szo_H1242 74–81. sor | szókártya-BDB | nagy | biztosan nyitott |
| 3 | Magában álló „vö.”, „l.”, „vö. továbbá” sorfej, „—” helyőrző, elszórt „&” és „+,” látszik a szövegben. | /szo/H1242 | F-BDBK b); F231 §2.4; MERCE szo_H1242 50., 60., 72., 80. sor | szókártya-BDB | közepes | biztosan nyitott |
| 4 | A kártya hivatkozásainál sokszor nincs könyvnév (a „34:25” az előző könyv folytatása), mért: H1242 68/201, H7451 97/365 chip. | /szo/H1242 | F231 §1 és §2.3; F-BDBK a) | szókártya-BDB | közepes | biztosan nyitott |
| 5 | A dupla függőleges jel (‖) feloldatlan, és a „szemben X-val” fordulat héber szóra ragasztott magyar raggal áll („szemben לֵילוֺת-val”). | /szo/H1242 | F231 §2.3; F-BDBK b)/d); MERCE szo_H1242 52–54., 131. sor | szókártya-BDB | közepes | biztosan nyitott |
| 6 | Nyers tudósjel és felső index látszik: „Ézs^3”, „Ézs^2” (a felhasználónál önálló pontként is), „Dl^HWB”, „Ba^ZMG”, „Gie ^Beitr.”, „Dr^Intr.”, „CIS^iv.1”, „ᵑ7”. | /szo/H0430, /szo/H0251, /szo/H3615 | FELH; F231 §2.4; F-BDBK b); MERCE szo_H0251 52. sor, szo_H1242 125. sor | szókártya-BDB | közepes | biztosan nyitott |
| 7 | A „Di 7:13”-nak nincs linkje, és nem derül ki, hogy tudós-jelzés (Dillmann) vagy könyvhivatkozás; hasonló jelzések: „Hu”, „Che”, „Klo”. | /szo/H0430 | FELH; F231 §2.4 (jelmagyarázat) | szókártya-BDB | kicsi | biztosan nyitott |
| 8 | A héber rövidítőjel (׳) a vegyes irányú szövegben rossz oldalra kerül („׳לַבּ”, „׳בַּבּ ׳בַּבּ”, „עַדבּֿ ׳בָּעֶרֶב”). | /szo/H0430, /szo/H1242, /szo/H7837 | FELH; F-BDBK b) (írásirány-hiba a rövidítésben); MERCE szo_H1242 137–143. sor | szókártya-BDB | közepes | biztosan nyitott |
| 9 | Az „א׳ אדני אברהם” magyarázat nélkül áll (a héber rövidítés feloldása hiányzik). | /szo/H0430 | FELH; F231 §2.4 (a jelmagyarázat csak a kártya alján egyszer áll) | szókártya-BDB | kicsi | biztosan nyitott |
| 10 | Felirat nélküli számok állnak a kártyán: „131”, „71”, „Apparátus és szövegkritika 2”. | /szo/H1242 | F231 §2.4; F-BDBK b); MERCE szo_H1242 47–48., 62. sor | szókártya-BDB | kicsi | biztosan nyitott |
| 11 | Egyes szócikkek tagolatlanok vagy rosszul tagoltak: a H7837 teljes szövege az „Alakok” alatt áll; a H3615-nél alaktani paradigma („perfectum”, „3. nőnemű egyes szám”) lett jelentéspont, üres jelentéscímmel („a.”, „1 — 25”). | /szo/H7837, /szo/H3615 | F-BDBK b); F231 §2.2 (tagolási jelző + visszaesés egybefüggő szövegre) | szókártya-BDB | nagy | biztosan nyitott |
| 12 | A tagolt kártya néhány szócikknél nem adja vissza a magyar fordítás minden tagmondatát (111 szócikkből 6,3% 85% alatt; H4723 42%, H2416 78%: a Zsolt 68:11 jegyzet hiányzik); a csukott teljes szöveg a biztosíték. | /szo/H4723, /szo/H2416 | N224; F230 jelentés 2.3; F231 §2 | szókártya-BDB | közepes | biztosan nyitott |
| 13 | Kilenc szónak van magyar BDB-fordítása, de nincs szakasztáblája, ezért nyers blokk áll tagolt kártya helyett (pl. H0747). | /r/szo/H0747 | N225; F230 jelentés 2.4 | szókártya-BDB | kicsi | biztosan nyitott |
| 14 | Az LXX-sor adata gyanús: a H1242 „17 hivatkozás” mellett 8+6+5 = 19 áll, és a φωσφόρος 88 előfordulással szerepel (valószínűleg nem fordul elő ennyiszer); forrásból nem ellenőrzött. | /szo/H1242 | N247 (az F231 §5 szerint, nyitott tételként még nincs kiosztva); F-BDBK; MERCE szo_H1242 245–248. sor | szókártya-BDB | közepes | biztosan nyitott |
| 15 | Az apparátusban leválasztott forrásjelek állnak („forrásjel (J) (P) (mindkettő J E) (H)”), a versek nélkül értelmezhetetlenül. | /szo/H1242 | F-BDBK b); MERCE szo_H1242 63., 85., 127. sor | szókártya-BDB | kicsi | biztosan nyitott |
| 16 | A vers jelentéspontja „Ebben a versben” címkével áll, pedig a BDB besorolása; kétes besorolásnál (`ketes`, `tagolatlan`, `fej`) is jelölés áll. | /szo/H1242?vers=… (bármely szó-lap vers-kontextussal) | DT914 (DT-F231c); F231 §2.1 (a „A BDB besorolása” címke); F-BDBT a Fable-lektor véleménye (FABLE_VALASZ_BDB_DONTES_SAJAT_OLVASAT) | szókártya-BDB | közepes | biztosan nyitott |
| 17 | Szakaszcím- és glosszahibák: a H2403 „1.a — 5 hivatkozás” csukott sora egy helyet mutat, a „4. bűnért való áldozat” pontjai az 1.–1.c ponthoz fűződnek; három szakasz „Külön meghatározás nélkül” áll (H2403 1.f, H7451 6. és 8.). | /szo/H2403, /szo/H7451 | N137 (2. ok), N139 | szókártya-BDB | kicsi | lehet, hogy már javult: ellenőrizendő (az F231 kártyamodellváltása érintheti) |
| 18 | A tagolt fában nem álló „nem azonosítható” helyek: 440 jelentéspont a szakasztábla sorbelső fejein, 5 368 sor két azonos címkéjű szócikknél (H7451: HAMART-szavakon 172). | /szo/H7451 | N144, N145 | szókártya-BDB | közepes | lehet, hogy már javult: ellenőrizendő |
| 19 | Az angol eredeti szövegében a BDB hivatkozás-javítások (412 sor, 247 Strong: pl. H0026 `2Sám`→`1Sám`) és a maradék betű-eltérések (~873 Strong) nem érvényesülnek; csukott „Angol eredeti”. | /szo/H0026 | F-BDBT 1.; befogadásra váró tétel „Angol BDB/Thayer az olvasóban” (24.) | szókártya-BDB | kicsi | lehet, hogy már javult: ellenőrizendő |
| 20 | A pe/mem betűjavítás a maqqef után nem illeszkedik: a 4Móz 16:30 „אֶת־מִּיהָ” marad „אֶת־פִּיהָ” helyett. | /szo/H0127 | N176 | szókártya-BDB | kicsi | biztosan nyitott |
| 21 | A görög szó-lap szerkezete nem egyenértékű a héberrel: nincs Strong-szótár, Előfordulás, Károli-alakok és tagolt kártya; a lap a nyers angol TBESG-gel és Thayerrel kezdődik, a magyar jelentés csak a harmadik blokk. | /szo/G0264, /szo/G3056 | FELH (2026-11-21: „a görög teljesen rossz”); F231 §1, §2.5; F-BDBK f)–g); F-OLV 18; MERCE szo_G0264 16–30. sor | szókártya-Thayer | nagy | biztosan nyitott |
| 22 | Fordítás nélküli Thayernél nincs tagolt jelentésfa és „Ebben a versben”; az angol szöveg külön, nyers blokkban áll, mellette csak a „Magyar fordítás nincs · az angol eredeti áll” üzenet. | /szo/G0264 | F231 §1, §2.1; F-THAY A. pont; F-BDBK f) | szókártya-Thayer | nagy | biztosan nyitott |
| 23 | A Thayer magyar fordítása csak 354 / 5 426 Strongra kész (6,5%), ezért a legtöbb görög lapon angol Thayer áll (az F07 A4 adag, kb. 10,12 USD, a felhasználó költségdöntése). | /szo/G0264 | F-THAY 1.; UTEMEZES_OLVASO (költségdöntések) | szókártya-Thayer | nagy | biztosan nyitott |
| 24 | A görög szó alapjelentése 5 334 Strongon angol marad (a TBESG rövid glosszájának magyar fordítása csak ~269 szóra kész). | /szo/G3056 | N177; N-F203c; UTEMEZES_OLVASO (költségdöntés, „a glosszák az első”) | szókártya-Thayer | nagy | biztosan nyitott |
| 25 | A Thayer-szövegben nincs kiemelés és hivatkozás-feloldás: a vers helye a szövegben nem látszik, az „Ebben a versben” csak a pontok nevét sorolja. | /szo/G0266?vers=… | F-THAY 1. (hiányzó pont 2.); F231 §2.1 (utolsó alpont) | szókártya-Thayer | közepes | biztosan nyitott |
| 26 | A Thayer jelentéspont-besorolásának néhány mért, javítatlan esete (záró szinonima-jegyzet, hamis bekezdés-eleji fej, latin betűs alpont); vak mérés 98,0%, nem független a javításoktól. | /szo/G0266 | N123, N125 (K1e), N126 (K2c, K2d, K5), N-F203a; F-THAY 1. | szókártya-Thayer | kicsi | biztosan nyitott |
| 27 | A DNTG-/UBS-táblákban nyers 15 jegyű azonosító áll („000262001001000”), a DNTG-előfordulások soronként ismétlik. | /szo/G0264, /1Moz/1/1 | F231 §1, §2.5; F-OLV 23; F-BDBK e); MERCE szo_G0264 65–80. sor | szókártya-Thayer | közepes | biztosan nyitott |
| 28 | Az „ÚSZ-előfordulás és versek” blokk nem mondja ki, hogy csak az első néhány vers látszik (43 előfordulás / 37 vers, 5 sor), és nincs versenkénti UBS-sor. | /szo/G0264 | F-OLV 19; MERCE szo_G0264 30–36. sor | szókártya-Thayer | közepes | biztosan nyitott |
| 29 | A görög szó-lapon nincs „Ebben a versben” blokk (alaktani kulcs kell hozzá). | /szo/G0264?vers=… | N-F231c (F231 §5); F-BDBK f) | szókártya-Thayer | közepes | biztosan nyitott |
| 30 | A héber szócsempék morféma szerint külön kártyán állnak, keret és teljes szó nélkül (1Móz 1:1: 11 csempe 7 szóra); a Károli-párosítási táblában ugyanaz a magyar szó kétszer áll („Kezdetben”). | /1Moz/1/1 | F233 §1–§2; F-THAY 3.; befogadásra váró 42. tétel | szócsoport-csempe | nagy | biztosan nyitott |
| 31 | Utótagos szónál az alapszó kártyáján nem létező alak áll (לְאִישָׁהּ: az „אִישָׁ֛” a ה nélkül; a kiejtés az F230 óta a közös szolgáltatásból jön). | /1Moz/3/6 | F233 §1; F-THAY 3.; F230 jelentés 2.1 | szócsoport-csempe | közepes | lehet, hogy már javult: ellenőrizendő (a kiejtés javult, a héber alak nem biztos) |
| 32 | Az előtag- és toldalék-csempéknek nincs saját kiejtésük (az 1Móz 1:1 „בְּ” csempéjén nincs); a kiejtés csak a szótő-csempén áll. | /1Moz/1/1 | N226; F230 jelentés 2.1 | kiejtés | kicsi | biztosan nyitott |
| 33 | A maqqef utáni kiejtés végén nyers kötőjel állt („gam-”, „'im-”, „ta'a.vah-”), a kártyán nincs összekötés. | /1Moz/3/6 | F233 §1; F-THAY 3. | kiejtés | kicsi | lehet, hogy már javult: ellenőrizendő (az F230 kiejtés-szolgáltatása érinthette) |
| 34 | A görög „ἀρχῇ” kiejtése „archēa”-nak látszik (gyanús), a szó mellett nem létező hangalak. | /Jan/1/1 | N-F233a (F233 §2 „Nincs benne”); F-THAY 3. (nem ellenőrzött) | kiejtés | kicsi | lehet, hogy már javult: ellenőrizendő |
| 35 | A görög versnézetben a központozás a szóhoz tapad („λόγος,”, „θεόν,”) a „Szó” oszlopban. | /Jan/1/1 | N-F233a; F-THAY 3.; MERCE vers_Jan_1_1 79., 81. sor | versnézet | kicsi | biztosan nyitott |
| 36 | Ugyanaz az adat csempeként és 6–13 külön táblázatban is megjelenik (Károli–Strong, TAHOT/TAGNT, Macula-kódok, LXX…), a pilot csak csempét használ. | /1Moz/1/1 | F-OLV 21; F233 §1 (21. pont); MERCE vers_1Moz_1_1 blokkjai | versnézet | közepes | biztosan nyitott |
| 37 | A versszámozás („MT / KJV”, „LXX-versszám”) a Vers fül közepén áll, a pilotban egysoros összefoglaló a lap tetején. | /1Moz/1/1 | F-OLV 22; F233 §1 (22. pont); MERCE vers_1Moz_1_1 (`vers.versszamozas`) | versnézet | kicsi | biztosan nyitott |
| 38 | A párosítási tábla „Bizonyosság” oszlopa „alacsony” címkét ír, a szó-lap „Károli itt” sora „alacsony bizonyosság” megjegyzést, a fejezet-lap `par-magas` osztályt használ; a döntés szerint a pár könyvcsoportjának mért pontossága áll (pl. „95% (Mózes öt könyve)”). | /1Moz/1/5, /1Moz/1 | N-F175d; MERCE vers_1Moz_1_5 101., 106. sor | versnézet | közepes | biztosan nyitott |
| 39 | Az LXX-többlet és a számozási eltérés adata nincs betöltve; a blokk ezért „Ez az adat ebben a kiadásban még nem érhető el” szöveget ad, tehát nem lehet különbséget tenni a valódi „nincs többlet” és a hiányzó adat között. | /1Moz/1/1 | N-F76j; F-OLV 9 (maradék); F230 #9 (a szöveg javult, az adat nem); `sqlite_epit.py` (a két tábla nincs betöltve); UTEMEZES_OLVASO (az F101 után) | versnézet | közepes | biztosan nyitott |
| 40 | A BSB-blokk „Nincs adat” szöveget ad a Zsolt 22:2-nél (a Károli 22:2 = KJV 22:1: valószínű versszámozási eltérés). | /Zsolt/22/2 | MERCE vers_Zsolt_22_2 `vers.bsb`; saját észrevétel, nem felmérés | versnézet | közepes | lehet, hogy már javult: ellenőrizendő (nem tudom, hiba-e vagy hiányzó adat) |
| 41 | A KJV-blokk szavai a Strong-számmal összetapadva jelennek meg a pillanatképen („forsakenH5800farH7350”). | /Zsolt/22/2 | MERCE vers_Zsolt_22_2 `vers.kjv`; (az F232 normalizálója okozhatja) | versnézet | kicsi | lehet, hogy már javult: ellenőrizendő (valószínűleg a pillanatkép jellemzője) |
| 42 | A Nave-blokkban nyers „PROPHECY \| .” címke és angol témanevek látszanak. | /Zsolt/22/2 | F-OLV 24 (alacsony súlyú részek) | versnézet | kicsi | lehet, hogy már javult: ellenőrizendő |
| 43 | A TSK-kereszthivatkozások táblázatának címe nem mondja meg a darabszámot és a szűkítést. | /1Moz/1/1 | F-OLV 29 | versnézet | kicsi | lehet, hogy már javult: ellenőrizendő |
| 44 | A „Motívumadat” blokk „PaRDeS-szint” fejléccel áll („értelmezési szint” kellene). | /1Moz/4/7, /Zsolt/116/4 | F-OLV 11 | versnézet | kicsi | lehet, hogy már javult: ellenőrizendő (az F230 #11 a tanulmányblokkot javította, a fejlécet nem nevezte) |
| 45 | Minden blokk fejében belső jelleg-címkék állnak („forrásadat”, „gépi feldolgozás”, „modell-kimenet”), az „Ebben a versben” dobozban is; olvasónak jelmagyarázat nélkül belső kategóriák. | /szo/H1242, /1Moz/1/1 | FELH; `blokkok.py` 54–57., 2376–2380. sor; MERCE szo_H1242 17., 22., 26., 40. sor | feliratok-belső szöveg | közepes | biztosan nyitott |
| 46 | A „Forrás és licenc” sor belső táblanevekkel áll („Strong_szotar (strong_szotar)”, „projekt_adat (forditasok): minden jog fenntartva”); a felmérés szerint szándékos (proveniencia), de olvasói nevet és zárt alapállapotot kérdezett. | /szo/H1242 | F-OLV 6 (maradék); F-THAY B. 6. sor (V); MERCE szo_H1242 20., 24., 38. sor | feliratok-belső szöveg | kicsi | biztosan nyitott (szerkesztői döntés kell) |
| 47 | Sok egyforma „Nincs adat (üres eredmény, nem negatív lelet)” sor áll (Jn 1:1-en 11); a felirat olyan blokkon is megjelenhet, amely a hiányzó fordítás miatt, nem a valódi üres eredmény miatt üres. | /Jan/1/1, /Róm/3/23 | F-OLV 28, 30; MERCE vers_Jan_1_1 | feliratok-belső szöveg | kicsi | biztosan nyitott (a sorok); a 28. pont része: ellenőrizendő |
| 48 | A Versszámozás-táblában nyers belső azonosító áll („lxx_os_etalon_f91”, „térkép (KJV-kulcs) \| Psa.21:1-2”). | /Zsolt/22/2 | MERCE vers_Zsolt_22_2 195–201. sor; saját észrevétel | feliratok-belső szöveg | közepes | biztosan nyitott |
| 49 | A KJV-blokk jelzése belső jogi megjegyzést mond az olvasónak („a Strong-címkék GPL-eredetűek: nyilvános kiadásból kimarad”, „tisztázatlan”). | /Zsolt/22/2 | MERCE vers_Zsolt_22_2 `vers.kjv`; F-BDBT 2. (licenc) | feliratok-belső szöveg | kicsi | biztosan nyitott |
| 50 | A szó-lap alcíme belső („szó-lap önálló címen · előfordulások versenként”). | /szo/H1242 | MERCE szo_H1242 15. sor | feliratok-belső szöveg | kicsi | biztosan nyitott |
| 51 | A fejléc és az oldalcím „PaRDeS olvasó”; a PaRDeS nem nyilvános név (új név: Biblialex). | / | F-OLV 26; memória (lexikon neve); MERCE minden lap 4. sora | feliratok-belső szöveg | közepes | biztosan nyitott (belső kiadás; név-döntés a felhasználóé) |
| 52 | A szintválasztó ékezet nélküli feliratokat mutat („nyilvanos / regisztralt / kutato”). | / | F-OLV 26; MERCE szo_H1242 9. sor | navigáció | kicsi | biztosan nyitott (csak a belső kiadásban látszik) |
| 53 | A főoldalon nincs Biblia-választó: a régi Könyv/Fejezet/Vers űrlap áll. | / | F-OLV 25; F233 §1 (25. pont) | navigáció | közepes | lehet, hogy már javult: ellenőrizendő (a fejezetlapon a „Biblia” választó megvan) |
| 54 | Gyenge kontraszt az aktív „kis próféták” könyvgombon (4,26:1, a WCAG AA küszöb 4,5:1). | /1Moz/1 | F-OLV 27 | navigáció | kicsi | lehet, hogy már javult: ellenőrizendő |
| 55 | Kicsi érintési célok mobilon (24–32 px), a tanulmányjel kontrasztja halvány (3,73:1 világos téma). | / (mobil) | F-OLV 31, 32; F233 §2.5 (`DESIGN-APRO`) | navigáció | kicsi | lehet, hogy már javult: ellenőrizendő |
| 56 | Nincs szó-lap számkártya a lapfej alatt (három kártya a pilotban); a számok mondatként állnak blokkokban („214 előfordulás, 29 könyvben.”). | /szo/H1242 | F-OLV 16; F233 §1 (16. pont); MERCE szo_H1242 22–23. sor | egyéb | közepes | biztosan nyitott |
| 57 | A Károli-alakok blokkban nincs arányos sáv, és a bevezető mind a 66 könyvet felsorolja ékezet nélküli rövidítésekkel („1Moz”, „Peld”). | /szo/H1242 | F-OLV 17; F233 §1 (17. pont); MERCE szo_H1242 37. sor | egyéb | közepes | biztosan nyitott |
| 58 | A Strong-szótár „Rövid jelentés” cellájában a magyar és az angol jelentés együtt áll („reggel morning”). | /szo/H1242 | MERCE szo_H1242 19. sor; (az „angol csak magyar híján” szabály szerint ez lehet eltérés) | egyéb | kicsi | lehet, hogy már javult: ellenőrizendő (nem biztos, hogy hiba) |
| 59 | Nincs motívumlap: a `/motivum/HAMART-001` 404-et ad; a 26 lekérdezésből 8 útvonal nélküli (8, 10, 12, 18, 21, 24, 25, 26), 5 nem igazolt (2, 3, 5, 15, 16); a 12-es lelet-blokk és az apparátus-kapcsoló hiányzik. | /motivum/HAMART-001 | F164; F-OLV 15; befogadásra váró 1. és 18. tétel | egyéb | nagy | biztosan nyitott |
| 60 | Az olvasó lassú: új fejezet 0,8–3 s (Zsolt 119: ~3 s), új vers ~0,9–1,9 s, az első héber szó-lap 1,0–3,7 s, hidegen 4–7 s; cél: fejezet ≤ 300 ms, vers ≤ 400 ms, szó-lap ≤ 250 ms. A javítás az F235 ágon készül (indexek, összevont lekérdezés, előmelegítés), a main-en még nincs. | /1Moz/1, /Zsolt/119, /szo/H1242 | F235; MERES_OLVASO_SEBESSEG_2026-11-22; FELH („ez a sebesség nem elfogadható”) | egyéb | nagy | biztosan nyitott a main-en (javítás ágon, merge nélkül) |

## Kihagyva, mert javult (bizonyítékkal)

| Régi pont | Mi javította | Bizonyíték |
|---|---|---|
| A kiejtés ragozott alakból („cha.tov-”, „i.yik.Ra'”; F-OLV 1) | F230.1: a közös kiejtés-szolgáltatásból | MERCE szo_H2398 13. sor: „chátá · ige”; szo_H1242: „bóker”; szo_G0264: „hamartanó” (az N-F231b „hamartēsē” a szó-lapon megszűnt) |
| Háromszoros BDB (F-OLV 2) | F230.1 (egy tagolt kártya) | MERCE szo_H1242: egyetlen `szo.bdb_apparatus`, nincs `szo.bdb_magyar` / `szo.bdb_angol` |
| Nyers `<br>` a TBESH-ben (F-OLV 3) | F230 | MERCE: 0 találat a „<br” mintára az összes lapon |
| Felesleges „Nyelvtani Strong-számok szűrése” blokk (F-OLV 4) | F230 | MERCE szo_H1242: nincs `szo.nyelvtani` blokk |
| Belső azonosítók a blokkcímekben és jelzőkben, „#96”, „#121” (F-OLV 6–7, 12) | F230 | MERCE: „Görög megfelelő (Septuaginta)”; nincs „(#…” és „lxx_bridge” látható szövegben; a proveniencia olvasói alakja |
| LXX-többlet: fájlnév és N-szám a szövegben (F-OLV 9, a szöveg része) | F230 (#9) | `F230_jelentes.md` 1. tábla 9. sor (az adat hiánya a 39. sor) |
| UBS-blokk: nem a versben álló Strongok (F-OLV 10) | F230 (#10) | `F230_jelentes.md` 1. tábla 10. sor (H0854, H0855 kiesett) |
| Tanulmányblokk: nyers `*(…)*` és munkanapló-cím (F-OLV 11, a tanulmányblokk) | F230 (#11) | `F230_jelentes.md` 1. tábla 11. sor |
| KH-tartomány vége elvész (F-OLV 13) | F230 (#13) | `F230_jelentes.md`: „1Móz 2:4–5” |
| `{L:…<SDBH:…>}` feloldatlan jelölés (F-OLV 14) | F230 (#14) | `F230_jelentes.md`; MERCE: 0 találat a „{L:” mintára |
| Nave-hely rossz linkkel (F-OLV 24) | F230 (#24) | `F230_jelentes.md`: „Zsolt 22:1 (KJV-számozás; Károli: Zsolt 22:2)”, a link a Károli-versre mutat |
| „Ugrás a tartalomra” hiánya (F-OLV 33) | F230 (#33) | `F230_jelentes.md` 1. tábla 33. sor (a link vizuálisan rejtett, ezért a pillanatképen nem látszik) |
| Thayer „Nincs adat” felirat fordítás nélkül (F-THAY B. 5) | F230 (#3b) | MERCE szo_G0264 28. sor: „Magyar fordítás nincs · az angol eredeti áll.” (az angol külön blokkban állása a 22. sorban marad) |
| A Thayer 15 forrásbeszúrása az angol blokkban nem látszik (F-BDBT 1.) | F215 | `lekerdezesek.py:838–844` (`thayer_forras_javitas` a `main`-en) |
| A „Thayer-szeletelő hiányzik” (brieftervezet) | F186, F187 | F-THAY 1.: kész és bekötve; seed-204 98,0% |
| 1Móz 4:7 „modern szöveg” (F-OLV 8) | téves volt | az orkesztrátori utóellenőrzés: a MEK 00161 szó szerint ugyanezt adja |
| A G264 mint kivétel, és a TBESH-alapú kiejtés javaslata | téves, visszavonva | F-OLV orkesztrátori utóellenőrzés; befogadásra váró 36. tétel; F234 §2 |
| Két piros olvasó-teszt a main-en (N187; `teszt_szintek`, `teszt_visszhang_kapu`) | F232.1 | commit `dc138f6b`: a teszt várt szövege volt régi, a kód nem hibás |

Nem vettem fel (nem olvasói hiba, szerkesztői döntés vagy szerzői feladat): az UBS DBH és az OSHL-család blokk jóváhagyása (F-OLV 20, „V”); a DT914 (2) homonima-jelzés a szerzőnek (az új motívumcikk előfeltétele); az N228 többi része (feljegyzés); az N222, N223, N221 (lapgenerátor); az N-F232a–e (teszt- és licenc-teendők); az N227 (felvetés, nincs kiosztva); a mérce licenc-áttekintése (N-F232e). A régi lexikongenerátorra vonatkozó 11-13-i audit (357 tétel) nem az olvasóra vonatkozik; az F234 szűri.

## Összesítő

Összesen 60 sor: biztosan nyitott 45, lehet, hogy már javult (ellenőrizendő) 15. Területenként:

| Terület | Sor | ebből biztosan nyitott | ebből ellenőrizendő |
|---|---|---|---|
| szókártya-BDB | 20 | 17 | 3 |
| szókártya-Thayer | 9 | 9 | 0 |
| szócsoport-csempe | 2 | 1 | 1 |
| kiejtés | 3 | 1 | 2 |
| versnézet | 10 | 5 | 5 |
| fejezetnézet | 0 | 0 | 0 |
| feliratok-belső szöveg | 7 | 7 | 0 |
| navigáció | 4 | 1 | 3 |
| egyéb | 5 | 4 | 1 |
| Összesen | 60 | 45 | 15 |

(A fejezetnézet külön hibát nem hoz: a bizonyosság-címke fejezet-lapi része a 38. sorban, a sebesség a 60. sorban áll. A számokat a fenti táblázat oszlopaiból számoltam.)

## A 6–8 legsúlyosabb, legjobban látható hiba

1. **A BDB-kártya szétszedett sorai** (1., 2., 11. sor): a felsorolás kettévágva, a próza a hivatkozásmezőben, a tagolatlan szócikkek; ez a héber lap fő tartalma, és az összes szó-lapon látszik.
2. **A görög szó-lap szerkezete és a fordítás hiánya** (21., 22., 23., 24. sor): a görög lap nyers angol szöveggel kezdődik, a Thayer 94%-án nincs magyar, az alapjelentés 5 334 szónál angol.
3. **Az olvasó lassúsága** (60. sor): új fejezet 1–3 s, hideg indítás 4–7 s; a felhasználó szerint elfogadhatatlan; az F235 ág még nincs beolvasztva.
4. **Nyers tudósjelek, rossz oldalú héber rövidítőjel, link nélküli sziglák** (6., 7., 8., 9. sor): minden BDB-szócikken látszik, és megtévesztő.
5. **Belső jelleg-címkék és belső azonosítók a felületen** (45., 48., 49. sor): „forrásadat / gépi feldolgozás / modell-kimenet”, „lxx_os_etalon_f91”, a GPL-megjegyzés; olvasónak szánt felületen nem állhat.
6. **Nincs motívumlap** (59. sor): a rendszer fő terméke, a motívum nézete, az olvasóban 404.
7. **A héber szócsempék morfémánként külön kártyán** (30. sor): az 1Móz 1:1-ben 11 csempe 7 szóra, kerettel és teljes szóval nem összefogva.
8. **A vers jelentéspontja félrevezető címkével áll** (16. sor, DT914): a szótár besorolása a vers tényeként jelenik meg, kétes besorolásnál is.

