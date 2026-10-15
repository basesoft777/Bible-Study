---
feladat: 99
cim: A BDB-szeletelő befejezése — hivatkozás-feloldás, jelentésen belüli tagolás, „ebben a versben”, gyökcsalád, héber szórend
kod: BDB_SZELETELO
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: dontesre_var
ag: claude/bdb-szeletelo
ad: a BDB-szócikk gépi szeletelése éles modulként, aranymintán mérve (0 eltérés), a „próba” felirat nélkül; minden igehely-hivatkozás feloldva (könyv, Károli-vers) és jelentésponthoz kötve (vers → jelentés tábla, proveniencia soronként); jelentésen belüli tagolás a használati csoportok mentén; a szó-lapon pontos hivatkozásszám, kattintható helyek, „ebben a versben” kiemelés és a hiány explicit jelölése; „rokon szavak” blokk az OSHL gyökcsaládjából; a héber idézetek helyes szórendje a megjelenítésben; a modell írta jelentésmagyarázat 20 szócikkes próbája
kovetkezo: "Te/orkesztrátor: az M2 ⛔ újramérése seed 101-gyel — a független ellenőrök VAKON töltik ki a naplok/BDB_SZELETELO_M2_minta_seed101_vak.tsv-t (250 sor: 200 véletlen + 25 kiszűrt + 25 bizonytalan; új resz oszlop, DT-F99i); a kulcs (naplok/BDB_SZELETELO_M2_minta_seed101_kulcs.tsv) az ellenőrnek nem adandó; összevetés: m2_minta_osszevet.py (9.5 + DT-F99i); mérce: könyv/vers ≥99%, jelentéspont ≥97% a 200 véletlen soron; ha nem teljesül, nincs seed-102. Nyitott: DT-F99h. Utána M3; ⛔ M4, ⛔ M5, ⛔ M6"
olvas: [eszkozok/olvaso_szerver/, eszkozok/sqlite_epit.py, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_teljes_unabridged_README.md, adat/forditasok.tsv, adat/terminologia.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/OSHL_lexikalis_index_README.md, konkordancia/OSHL_BDB_igehelyek.tsv, konkordancia/TAHOT_kivonat.tsv, eszkozok/bdb_konyv_javit.py, F38_BDB_FORDITAS_BRIEF.md, F98_TERVEZO_MOD_BRIEF.md, naplok/TERVEZO_MOD_M0.md, naplok/OLVASOI_PILOT_szeletelo_atnezes.md]
ir: [eszkozok/olvaso_pilot/bdb_szelet.py, eszkozok/olvaso_pilot/, eszkozok/olvaso_szerver/, eszkozok/oshl_index_import.py, konkordancia/OSHL_lexikalis_index.tsv, konkordancia/OSHL_lexikalis_index_README.md, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, adat/bdb_vers_jelentes.tsv, adat/bdb_aranyminta.tsv, adat/bdb_magyarazat_proba.tsv, adat/SEMA.md, adat/datasetek.tsv, naplok/BDB_SZELETELO_M0.md, naplok/BDB_SZELETELO_zaras.md, naplok/BDB_SZELETELO_M2_minta_vak.tsv, naplok/BDB_SZELETELO_M2_minta_kulcs.tsv, naplok/BDB_SZELETELO_M2_minta_kitoltott_A.tsv, naplok/BDB_SZELETELO_M2_minta_kitoltott_B.tsv, naplok/BDB_SZELETELO_M2_osszevetes_nyers.txt, naplok/BDB_SZELETELO_M2_karoli.md, naplok/BDB_SZELETELO_M2_minta_seed100_vak.tsv, naplok/BDB_SZELETELO_M2_minta_seed100_kulcs.tsv, naplok/BDB_SZELETELO_M2_seed100_kitoltott_A.tsv, naplok/BDB_SZELETELO_M2_seed100_kitoltott_B.tsv, naplok/BDB_SZELETELO_M2_seed100_osszevetes.txt, naplok/BDB_SZELETELO_M2_seed100_iteletek.md, naplok/BDB_SZELETELO_M2_minta_seed101_vak.tsv, naplok/BDB_SZELETELO_M2_minta_seed101_kulcs.tsv, naplok/BDB_SZELETELO_M2_seed101_kitoltott_A.tsv, naplok/BDB_SZELETELO_M2_seed101_kitoltott_B.tsv, naplok/BDB_SZELETELO_M2_seed101_osszevetes.txt, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, eszkozok/olvaso_szerver/teszt_bdb_vers_jelentes.py, DONTESEK.md, NYITOTT_FELADATOK.md]
fugg: []
nem_fugg: [27, 38]
---

# F99_BDB_SZELETELO_BRIEF.md — A BDB-szeletelő befejezése

*Befogadásra váró brief-tervezet · v1 · 2026.10.15 · forrás: a felhasználó döntései a chatben (2026-10-14/15): a szó-lap BDB-blokkja „így sokkal érthetőbb” (egy kézzel tagolt szócikk-magyarázat nyomán); a tagolás, a hivatkozás-feloldás és a gyökcsalád egy briefben, külön mérföldkövekkel; a héber szórend és a modell-magyarázat is ide kerül, saját megállással. Előzmény: F98.9–F98.13 (a `claude/tervezo-mod` ágon: a pilot jelentéslista-szabályai, vázlat, jelentéscím, kölcsönzött cím, „N hivatkozás” felirat, jelmagyarázat — `konfig/bdb_jelek.tsv`).*

**Javasolt fejléc-adatok:** `modell: opus` (heurisztikus szeletelés és megjelenítés; a M6 próbája külön modellt nevezhet meg, l. DT-F99d) · `munka: folyamat` (motívumfájlt nem ír) · **halasztva a #98 lezárásáig** (`kovetkezo: Halasztva: …`, `fugg: []`) — **ütközés:** a #98 (TERVEZO_MOD) ugyanazt az `ir`-t írja (`eszkozok/olvaso_szerver/`), és az M2-je elem-regisztert és regiszter-őrt vezet be; ez a feladat a #98 lezárása után indul, és minden új elemét a regiszterbe veszi. Kézi `fugg: [98]` helyett halasztás, mert a #98 (és a #76) `olvas`-a az F99 által írt fájlokat sorolja fel, így a levezetett függés fordított irányú lett volna, és kört okozott volna (`feladatok.py fuggesek`, DT-F39d); a #98 lezárásakor a `kovetkezo` mező „/kovetkezo”-ra vált. `nem_fugg: [27, 38]`: az `adat/forditasok.tsv`-t csak olvassa (pillanatkép), nem várja meg a fordítások végét. **Kapcsolódás a #38-hoz (BDB_FORDITAS, fut):** a M3 terminológiai része a fordítás kötelező alakjait bővíti (DT-F99b); a #38 adagjai közé kell illeszteni, nem párhuzamosan írni az `adat/terminologia.tsv`-t.

## 1. Cél

A szó-lap BDB-blokkja most gépi szeletelést mutat „próba” felirattal: a jelentések és alpontok szerkezete helyes, de egy jelentésen belül a használati csoportok (pl. „abszolút használatban”, „infinitivus absolutus határozószóként”, „utána בְּ”) egyetlen bekezdésben állnak, a hivatkozásszám közelítő (csak a `fejezet:vers` alakokat számolja), a héber idézetek szórendje fordított, és nem derül ki, melyik jelentés vonatkozik arra a versre, ahonnan a szót megnyitották. A feladat végén:

1. A szeletelő **éles modul** a szerver mellett, aranymintán mérve (0 eltérés), a „Gépi szeletelés (próba)” felirat nélkül.
2. **Minden igehely-hivatkozás feloldva** (könyv, fejezet, vers; a könyv öröklése a folytató hivatkozásoknál; MT → Károli átkulcsolás), az irodalmi álhivatkozások kiszűrve, és **jelentésponthoz kötve** (törzs + jelentés + alpont + használati csoport): `adat/bdb_vers_jelentes.tsv`, soronkénti provenienciával.
3. **Tagolás egy jelentésen belül** a BDB saját bevezető jelölői mentén, külön sorban, a bevezető kiemelve; hamis határ nélkül (biztonságos szabály, l. M3).
4. A szó-lapon: **pontos hivatkozásszám**, **kattintható igehelyek** (a feloldott könyvvel súgóban), **„ebben a versben” kiemelés** (a versből megnyitott szónál az a jelentés, ahol a BDB a verset idézi, kiemelve és odagörgetve), és ha a BDB a verset nem idézi, **ezt kifejezetten kiírja** („a BDB ezt a verset nem idézi” — nem negatív lelet, nem találgatás).
5. **„Rokon szavak” blokk** az OSHL gyökcsaládjából (`<etym>`: gyök és származékai).
6. A héber idézetek **helyes szórendje** a megjelenítésben (a forrásfájl változatlan).
7. A modell írta, olvasóbarát **jelentésmagyarázat 20 szócikkes próbája** „modell-kimenet” jelöléssel; a teljes futásról külön döntés.

## 2. Hatókör

- **Benne:**
  - **Aranyminta** (`adat/bdb_aranyminta.tsv`): kézzel ellenőrzött szócikkek a várt szerkezettel (törzsek, jelentések, alpontok, címek, használati csoportok, hivatkozások); vegyesen főnév, ige több törzzsel, homonima-sor, arámi rész, csonk szócikk, magyar és csak angol szöveg. Legalább 30 szócikk; benne a beszélgetésben vizsgáltak: H1242 בֹּקֶר, H0776 אֶרֶץ, H7451 רַע, H3615 כָּלָה, H0559 אָמַר, H6440 פָּנֶה, H7307 רוּחַ, H0430 אֱלֹהִים.
  - **Hivatkozás-feloldás** (M2): a szeletelő kimenete hivatkozásonként: nyers alak, feloldott könyv, fejezet:vers (MT), Károli-vers, a jelentéspont útvonala; az álhivatkozások (irodalmi jel után álló, pl. `De^Job 2:598`, „Dr^§ 115”) kiszűrve, okkóddal.
  - **Vers → jelentés tábla** (`adat/bdb_vers_jelentes.tsv`, új; SEMA-bejegyzéssel és `adat/datasetek.tsv`-sorral): Strong, BDB-azonosító, Károli-vers, MT-vers, jelentéspont-útvonal, nyers hivatkozás, a feloldás módja (`kiirt` / `orokolt` / `atkulcsolt`), proveniencia (`scope=… | forras=BDB_teljes_unabridged.tsv+bdb_szelet@<commit> | ts=…`). A pardes.db-be a `sqlite_epit.py` viszi.
  - **Tagolás** (M3): a jelölők mérése az **angol** forráson (teljes, 8099 szócikk); a magyar megfelelők rögzítése a terminológiában (DT-F99b); magyar bontás csak egyező jelölőszámnál.
  - **Megjelenítés** (M4): a fenti 4. pont; a szeletelő kiemelése a pilotból; az irodalmi jelek listája a `konfig/bdb_jelek.tsv`-ből (a mai `SIGLA` minta csak a `^`-os alakot ismeri, a `J^R`-t tévesen irodalminak veszi).
  - **Gyökcsalád** (M1): az `oshl_index_import.py` a `LexicalIndex.xml` `<etym>` elemét is beolvassa (`etym_tipus`: `main` / `sub` / `single`; `etym_cel`: a gyök OSHL-kulcsa; `gyok`: a `main` `root` attribútuma), a generált `konkordancia/OSHL_lexikalis_index.tsv` új oszlopai; a szó-lapon „Rokon szavak (OSHL-gyökcsalád)” blokk.
  - **Héber szórend** (M5): a többszavas héber idézetek szórendjének helyreállítása a megjelenítéskor, maqqéf-javítással (`עַדכַּֿלֵּה` → `עַד־כַּלֵּה`); a forrás (`BDB_teljes_unabridged.tsv`, `adat/forditasok.tsv`) változatlan.
  - **Modell-magyarázat próbája** (M6): 20 szócikk, külön tábla (`adat/bdb_magyarazat_proba.tsv`), `modell` mező a ténylegesen futott modell nevével.
- **Nincs benne:**
  - a BDB-forrásfájl vagy a magyar fordítás szövegének javítása (a szórend-hiba és az OCR-hibák, pl. „3 2-Jan” = 3 1/2, „Sh®°ôl”, a forrásban maradnak; a megjelenítés javít, a forrás nem);
  - a vers → jelentés tábla motívum- vagy tanulmányadatként való használata: a tábla lexikai index; **keresési találatból nem lehet közvetlenül study-sor** (CLAUDE.md 2. szabály), bármely felhasználása a `jeloltek.tsv`-n megy át;
  - a modell-magyarázat teljes futása (kb. 8000 szócikk) — külön feladat a DT-F99d után;
  - a design system artifact feltöltése (a #98 szinkron-szkriptje adja a `tokens.json`-t; a feltöltést a felhasználó kéri);
  - a mellékesen talált hibák: a translationWords-blokk nyers Markdownja (`szo.tw_h`), az OSHL-táblázat túlcsordulása mobilon — külön tételek (N-F99a, N-F99b).

## 3. Lépések

### M0 — aranyminta és mérések ⛔

1. **Aranyminta** (`adat/bdb_aranyminta.tsv`): a 2. szakasz szerinti ≥30 szócikk várt szerkezete, kézzel; a mai szeletelő kimenetével összevetve az eltérések listája (`naplok/BDB_SZELETELO_M0.md`). A minta **a mérések előtt** készül (a projekt szabálya: előbb a minta, utána a mérés).
2. **Hivatkozás-mérés** az angol BDB-n: kiírt / örökölt / feloldhatatlan könyv; álhivatkozás-jelöltek (irodalmi jel után álló `fejezet:vers`) száma; MT ↔ Károli eltérő helyek (a `Karoli_versmegfeleltetes.tsv` szerint: zsoltárfeliratok, Jóel 3/4, Malakiás 4 stb.) száma. *Előzetes, nem ellenőrzött mérés egy másik sessionből (2026-10-14, scratchpad, csak olvasott):* 150 082 hivatkozás 8025/8099 szócikkben; 103 293 kiírt könyvvel, 46 438 örökölt, 351 feloldhatatlan; az `OSHL_BDB_igehelyek.tsv` ezzel szemben 4054 hivatkozás 2836 szócikkben. Az M0 ezt saját lekérdezéssel megismétli.
3. **Jelölő-mérés** az angol BDB-n: a használati csoportok bevezetői („absolute”, „Inf. abs. as adverb”, „followed by”, „opposed to”, „so”, „also”, „especially”, „in phrases”, „figurative” …), előfordulás, és hogy hányszor állnak jelentéshatáron vs. mondat közben; a magyar fordításban (678 szócikk) a mai megfelelőik és azok szórása.
4. **OSHL `<etym>`**: a teljes `LexicalIndex.xml` (a rögzített commiton, amelyről az import dolgozik) feldolgozása: `main` / `sub` / `single` darabszám, a `sub`-célok feloldhatósága a mi Strong-kulcsainkra, mintaként a לַ֫יְלָה (H3915) családja.
5. ⛔ **Döntések** (`DONTESEK.md`): DT-F99a–d (5. szakasz). Megállás.

### M1 — gyökcsalád

1. `oshl_index_import.py`: az `<etym>` beolvasása, új oszlopok; a generált tábla és README frissítése; teszt (a `main`/`sub`/`single` darabszám egyezik az M0-éval).
2. `sqlite_epit.py`: az új oszlopok a pardes.db-be; teszt.
3. Szó-lap: „Rokon szavak (OSHL-gyökcsalád)” blokk (a regiszterbe véve, l. #98); a gyök és a származékok Strong-linkkel; üres családnál „nincs OSHL-gyökcsalád” (nem negatív lelet).

### M2 — hivatkozás-feloldás és vers → jelentés tábla ⛔

1. A szeletelő hivatkozásonként feloldja a könyvet (kiírt / örökölt; a `Konyv_normalizalo_tabla.tsv` és a `bdb_konyv_javit.py` alakjaival), kiszűri az álhivatkozásokat (okkód), és MT → Károli átkulcsol a `Karoli_versmegfeleltetes.tsv`-n át.
2. `adat/bdb_vers_jelentes.tsv` generálása (GENERÁLT fejléc, a tábla a szkriptből bármikor újra előáll), SEMA-bejegyzés, `datasetek.tsv`-sor, a pardes.db-be.
3. ⛔ **Minta-ellenőrzés:** 200 véletlen hivatkozás (rögzített seeddel) kézi ellenőrzése a BDB nyomtatott szerkezete szerint: helyes könyv, vers, jelentéspont. Az eredmény a naplóba; a küszöb az elfogadási feltételekben. Megállás.

### M3 — jelentésen belüli tagolás

1. A DT-F99b szerinti jelölők az angol szövegen: a szeletelő a jelentést (és alpontot) használati csoportokra bontja; a bevezető a csoport címe.
2. Magyar szövegen: bontás csak akkor, ha az adott jelentésben az angol és a magyar jelölők száma és sorrendje egyezik; különben tagolatlan marad (nincs hamis határ). A le nem fordított szócikkeknél az angol tagolás látszik.
3. Terminológia: a DT-F99b szerinti kötelező alakok az `adat/terminologia.tsv`-be, a #38-cal egyeztetett időpontban (két adag között); a kész magyar szócikkeken a régi alakok mérése és listája (csere nincs, csak jelentés).

### M4 — megjelenítés és kiemelés a pilotból ⛔

1. A szó-lapon: pontos hivatkozásszám (a feloldott, szűrt hivatkozásoké), kattintható igehelyek (súgó: a feloldott hely), használati csoportok külön sorban.
2. **„Ebben a versben”:** a versből megnyitott szónál (a jobb oldali panel szó-füle, és a szó-lap `?vers=` paraméterrel) a vers → jelentés tábla alapján kiemelés és odagörgetés; több találatnál mind kiemelve; ha nincs, a blokk tetején: „A BDB ezt a verset nem idézi.”
3. Az irodalmi jelek a `konfig/bdb_jelek.tsv` alapján (a `SIGLA` minta helyett).
4. A szeletelő éles modul (helye: DT-F99c); a „Gépi szeletelés (próba)” felirat lekerül, ha az aranyminta 0 eltérést ad; a pilot (`eszkozok/olvaso_pilot/`) az éles modult használja, kódmásolás nélkül.
5. Minden új elem a #98 elem-regiszterében (magyar név, állítható tulajdonságok), új méret csak tokenből; a regiszter-őr zöld.
6. ⛔ **Felhasználói próba** a futó szerveren (legalább a H1242, H7451, H3615 lapon és egy versből megnyitva). Megállás.

### M5 — héber szórend ⛔

1. A többszavas héber idézetek szórendjének helyreállítása a megjelenítéskor; maqqéf-javítás.
2. **Gépi ellenőrzés:** ahol az idézet egy hivatkozott vers szövegéből van, a helyreállított szórend összevetése a vers héber szövegével (`TAHOT_kivonat.tsv`, a Károli-kulcson); egyezési arány a naplóba.
3. ⛔ **Minta:** 50 idézet kézi ellenőrzése. Megállás; az összes szócikkre csak a minta után.

### M6 — modell-magyarázat próbája ⛔

1. 20 szócikk (az aranymintából), jelentésenként olvasóbarát magyarázat: a használati csoportok rövid összefoglalója, a hivatkozott helyek tartalma egy mondatban. Csak a BDB szövegéből és a hivatkozott versekből; ami nem onnan jön, az nem kerül bele (CLAUDE.md 3. szabály).
2. `adat/bdb_magyarazat_proba.tsv`: Strong, jelentéspont, magyarázat, `modell` (a ténylegesen futott modell neve), proveniencia; a szó-lapon „modell-kimenet” jelleggel (arany címke), külön a BDB-szövegtől.
3. ⛔ **DT-F99d:** folytatódjon-e a teljes BDB-re, milyen modellel, mennyi költséggel (mérve a 20 szócikken). Megállás.

### Zárás

`naplok/BDB_SZELETELO_zaras.md`; a brief fejléce; N-F99a–b a `NYITOTT_FELADATOK.md`-be.

## 4. Elfogadási feltételek

- **Aranyminta:** a szeletelő kimenete a ≥30 szócikken **0 eltérés** a várt szerkezettől (törzsek, jelentések, alpontok, használati csoportok, címek). Ennek teljesülése nélkül a „próba” felirat marad.
- **Hivatkozás-feloldás:** a 200-as mintán a könyv és a vers ≥ 99%-ban, a jelentéspont ≥ 97%-ban helyes; az eltérések okkal listázva. Az álhivatkozás-szűrés hamis pozitívja és negatívja a mintán külön számolva.
- **Vers → jelentés tábla:** minden sor megnevezi a jelentéspontot és a feloldás módját; proveniencia minden soron (`manual` nem lehet, mert gépi); a tábla a szkriptből bájtra újragenerálható; `ellenoriz.py` SÉRTÉS 0.
- **Tagolás:** magyar szövegen csak egyező jelölőszámnál bont; az aranymintán hamis határ 0.
- **„Ebben a versben”:** a versből megnyitott szónál a kiemelés a tábla szerinti jelentés(ek)en áll; idézet nélküli versnél a „nem idézi” felirat, kiemelés nélkül.
- **Gyökcsalád:** a blokk darabszámai egyeznek az M0 `<etym>`-mérésével; üres családnál explicit „nincs” felirat.
- **Szórend:** az M5 gépi ellenőrzésének egyezési aránya és az 50-es minta eredménye a naplóban; a minta jóváhagyása nélkül nincs teljes bevezetés.
- **Felület:** a regiszter-őr zöld (minden új elem regisztrált vagy indokolva kizárt), új méret csak tokenből; a meglévő tesztek zöldek (`teszt_olvaso_szerver.py`, `teszt_arculat.py`, `teszt_pilot_aranymintaval.py`, `teszt_szintek.py`), a futtatás a projekt venv-jében, `PARDES_DB` a natív adatbázis-példányra.
- **Szabályok:** a három alapszabály (proveniencia, nincs közvetlen út, memória vs. lekérdezés) sértetlen; a TSV-k `split('\t')`-tel olvasva, `'\t'.join()`-nal írva.

## 5. Döntésnapló

- **DT-F99a** (M0): az álhivatkozás-szűrés és az MT → Károli átkulcsolás szabálya a mérés alapján (mely irodalmi jelek után álló `fejezet:vers` szűrendő; mi történik a Károliban nem létező MT-versekkel).
- **DT-F99b** (M0): a használati csoportok bevezetőinek kötelező magyar alakja (pl. „opposed to” → „ellentéte”, „followed by” → „utána”, „absolute (használat)” → „abszolút használatban”, ma kapu nélkül), kapuval vagy anélkül; bevezetésük időpontja a #38 adagjai között; a kész 678 magyar szócikk kezelése (csak mérés, vagy újrafordítás).
- **DT-F99c** (M0): a szeletelő helye élesben (`eszkozok/olvaso_szerver/bdb_szelet.py`, a pilot onnan tölti be — vagy marad a pilotban, és a szerver tölti be, mint ma, DT-F76g).
- **DT-F99d** (M6): a modell-magyarázat teljes futása (igen / nem; modell; költségkeret a 20 szócikk mérése alapján).
- **N-F99a:** a translationWords-blokk (`szo.tw_h`) nyers Markdownt mutat (szó szerinti `\n`, `#`).
- **N-F99b:** az OSHL-blokk táblázata mobilon kilóg (375 px-en 484 px széles).
