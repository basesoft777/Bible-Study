# F104 — BDB_MEGJELENITES: munkanapló

*FELADATOK #104 · ág `claude/f104-bdb-megjelenites` · végrehajtó: `claude-opus-5-5` (kért: `opus`) · 2026-11-09 · állapot: ⛔ a brief 4.
lépésénél megállva (felhasználói próba a futó szerveren + a lexikonlap-minta átnézése)*

## 1. Hatókör és egyeztetett eltérések

- **A brief `ir`-je szerint:** az olvasó-szerver szó-lapjának BDB-blokkja (`blokkok.py`, `lekerdezesek.py`, `statikus/`,
  `konfig/elemek.toml`, `teszt_olvaso_szerver.py`).
- **Egyeztetett eltérés 1 (orkesztrátor):** a mért pontosság egyetlen forrása új konfigfájl: `eszkozok/olvaso_szerver/konfig/bdb_pontossag.toml`
  („konfig vagy adat”, az orkesztrátor feladatleírása szerint); az `ir`-be felvéve.
- **Egyeztetett eltérés 2 (orkesztrátor, a felhasználó jóváhagyásával, „mehet most”, 2026-11-09; DT690):** hatókör-bővítés —
  a lexikonlap 4.2 kétrétegű BDB-kártyája (`eszkozok/lexikon_general.py`, `eszkozok/olvasoi_kapu.py`, `adat/SEMA.md`, a két tesztfájl);
  az `ir` bővítve. A `feladatok.py fuggesek` KIZAR-ütközést ad a `lexikon_general.py`-n a #178-cal (`megallt`), a #182-vel és a
  #183-mal (`nem_indult`); **`fut` állapotú feladattal nincs ütközés**, ezért a generátor-munka indult. Figyelem: a #178 ága
  (`claude/lexikon-ag-lezaras`) nyitva van, és ugyanezt a fájlt írja — merge-ütközés lehetséges.
- **Kényszerű teszt-igazítás `ir`-en kívül** (a brief „a meglévő tesztek zöldek” feltétele miatt): `teszt_tervezo.py` (a regiszter
  elemszáma 101 → 106; két új töredék a szelektor-próbához), `teszt_pilot_aranymintaval.py` (a nyers BDB-szöveg összevetése a
  sor-kulcs és a `_N` számláló normalizálásával: ezeket a #104 szándékosan nem rendereli). Mindkettő az `ir`-be felvéve.
- **Nem készült el (a brief 2. pontja):** a `/szo/<strong>?vers=` paraméter. A vers-kontextus a versből megnyitott szó-fülön
  (`/<könyv>/<f>/<v>?szo=…&ful=szo`, `/r/szo/…?ig=…`) működik; az önálló szó-lap `?vers=` paramétere az `alkalmazas.py` és az
  `oldalak.py` módosítását kívánná, ezek nincsenek az `ir`-ben. Döntésre: a #104 javítókörébe kerüljön-e (két fájl, néhány sor), vagy
  külön tétel. → Döntés: kimarad, N118 (8. szakasz).

## 2. A szó-lap BDB-blokkja (F104.1)

*proveniencia: scope=pardes.db (`~/pardes/pardes.db`, epites_ts 2026-11-02T12:55:43Z), bdb_vers_jelentes 162 054 sor | forras=a szerver
`lekerdezesek.bdb_vers_jelentes` + `blokkok.VersJelolo` | ts=2026-11-09*

- **A tábla a szerverben:** `lekerdezesek.bdb_vers_jelentes(con, strong)` — a 2.29 sorai a szócikkön belüli sorrendben; a `csoport`
  oszlop opcionális (a helyi DB 2026-11-02-i, az F103 két új oszlopa még nincs benne: a csoportsor-jelölés a DB újraépítése után
  hat; a csoportsorok megjelenítése a szeletelőből már most működik). DB-újraépítés nem kellett és nem történt.
- **Leképezés:** a tábla kulcsa (szakasz-címke, útvonal) → a megjelenített (magyar, ennek híján angol) bontás csomópontja. A szakasz-címke
  a `bdb_szelet._szakasz_cimke` szerint (fő címszó: a homonima-szám; tagolás: `gazda§jel`); a kétszer előforduló kulcs nem köt (nincs
  tippelés). A magyar bontás a mintán (H1242, H3615, H6975, H7451) csomópontra azonos az angollal; ahol eltér, a sor „nem azonosítható”
  marad, és a blokk kimondja, hány ilyen hivatkozás van.
- **Erős** („a BDB itt idézi ezt a verset”): a sor Károli-verse a lap verse, nem szűrt, nem bizonytalan. A csomópont (li) és a
  szövegbeli igehely (a) is kiemelve; a `fej` / `tagolatlan` sor a szövegbeli hely kiemelésével és a doboz szövegével.
- **Gyenge** („vonatkozhat”): (a) a bizonytalan sor — a SEMA 2.29 „bizonytalan, a táblában marad” okkódjai (`sigla_kozel`,
  `tobbertelmu`, `ismeretlen_alak`, `nincs_elozmeny`, `orokles_hibas`), a `forras_hiba` és az `atkulcsolt_bizonytalan`; a helyi DB-ben
  Károli-verssel csak 5 ilyen sor van, mind `forras_hiba` (H1802 2Móz 2:6, H3051, H5591, H7804, H7913). (b) idézet nélküli versnél az
  igetörzs szakasza, jelentéspont nélkül (DT689).
- **„A BDB ezt a verset nem idézi”**: kiemelés nélkül; ha a szó ige és a törzse azonosítható, a (b) gyenge jelölés.
- **A próba felirat és a mért pontosság** a vers-kontextusban az „Ebben a versben” dobozban, a jelölés mellett.
- **Pontos hivatkozásszám:** csomópontonként és a címszónál a tábla feloldott, szűrt sorai (`szurt` ≠ 1, van maszoréta vers); a súgó ezt
  mondja. Tábla nélkül (régi DB) a korábbi gépi szám marad.
- **Kattintható igehelyek:** a szöveg „fejezet:vers” alakjai a csomópont sorai szerint (fejezet + vers egyezés, legfeljebb 4 sor
  átugrásával; a fej/tagolatlan sorok sorrend nélkül) a Károli-versre mutatnak; súgó: „feloldva: <Károli-vers>” (+ a héber
  versszámozás, ha eltér; + a bizonytalanság oka). A H1242 lapján 205 sorból 204 link.
- **Csoportsorok (F103):** a csomópont szövege a használati csoportoknál új sorban (`bdb-csop`), a szöveg változatlan (teszt).
- **Odagörgetés:** `olvaso.js` `bdbOdagorget` — az első erős pontra (ennek híján az első gyenge jelölésre), a lap ragadós fejsora alá.
- **Regiszter:** 5 új elem (`bdb-ebben`, `bdb-itt`, `bdb-vonatkozhat`, `bdb-jelzes`, `bdb-csop`), 1 kizárt horog (`bdb-pontossag`); az
  értékek meglévő tokenekből (új méret nincs). Regiszter-őr: `hiba: 0`.

## 3. DT689 — a gyenge (b) szint igetörzs-forrása

A TAHOT kivonata (és a `token_eredeti`) nem hordoz morfológiát. A javasolt (a): a jelenlét a TAHOT szerint, az igetörzs a versbeli azonos
Strongú Macula-sor OSHB-kódjából (`morf_kulcs_heber` `igetorzs`; arámi szónál az arámi kulcs). A végrehajtó ezzel haladt tovább; az orkesztrátor
megerősítette (🟢, a licenc-ellenőrzés után, 8. szakasz) (`dontesek/uj/f104-bdb-megjelenites.md`).

## 4. A mért pontosság egy forrásból

A DT658 (a) előre rögzítette, hogy a lapon az új nyers szám áll: seed-102, a szeletelő 183/200 (91,5%, Clopper–Pearson 95%: 86,7–95,0%;
`naplok/F102_BDB_SZELETELO_JAVITAS_naplo.md` 14.). A brief DT177 (c)-s 92,0%-a a seed-101 régi száma — **nem kétséges, melyik érvényes**,
ezért nincs rá DT-tétel. A szám a `konfig/bdb_pontossag.toml`-ban áll (proveniencia-sorral); a százalékot a kód számolja, a CI-t a teszt
a 183/200-ból újraszámolja; a `blokkok.py`-ban a szám nem áll (teszt). A lapon a proveniencia a súgóban.

## 5. HAMART-001 F10 a szerveren

| Lelet | A szerveren | Mi történt |
|---|---|---|
| (5) „H6975. qots I. קוֺץ”, „H7451. ra ' I. רַע‎_226” | az apparátus Címszó-sora STEP-átírást mutatott; a nyers angol/magyar blokk a sor kulcsát és a `_226`-ot | a Címszó a jóváhagyott kiejtést mutatja („(kóc)”, „(ra)”), jóváhagyott kiejtés híján átírást nem; a nyers blokkban a sor kulcsa (Strong + STEP-átírás) nem áll, a `_N` a BDB saját alsó indexe (`<sub>`, súgóval) |
| (5) „ק׳”, „(J)”, „(E)”, „Co törli” | a ק׳ feloldott (címszó-rövidítés); a (J), (E), Co csak a jelentések szövegében | a jelmagyarázat az alapjelentésre, a nyelvi háttérre és az alaktanra is kiterjed: a H6975 és a H7451 lapján mind feloldott |
| (5) „status absolutus/constructus” | feloldatlan | **N117**: a `bdb_jelek.tsv`-ből hiányzik (és: SS, Wetzst, Hu, De); nem találtam ki |
| (3) „BDB8032 (a H7451 1. BDB-szócikke a 3-ből)” | a szerveren nem látszik; az alias-megjegyzés viszont a belső BDB-azonosítót és a párosító tábla nevét mutatta, a blokk-felirat a `bdb_szelet.py` fájlnevet | olvasói alakra hozva |

## 6. A lexikonlap 4.2 kétrétegű BDB-kártyája (F104.3; DT690)

- **Csak a kapcsolóval bekapcsolt új szerkezetű lapon** (`ctx['bdb_kartya']` = `bdb_kartya_aktiv(id)`; a kapcsoló a 9. szakaszban); a régi út változatlan (teszt). A görög (Thayer)
  4.2-ben csak a bevezető ismétlődése szűnt meg.
- **Olvasói réteg:** a jelentések rendje (a hordozó szakasz félkövér; a glossza a `szotar_szakasz_cimke.tsv` címkéje, ennek híján a
  magyar szöveg első tagmondata az első zárójel, igehely, héber szó, rövidítés és hivatkozó szó előtt; az alakjegyzékkel nyíló szakasz
  „külön meghatározás nélkül”; a tagolatlan szócikk egésze a fej meghatározásával); „**A motívum helyein:** vers → jelentés”, a nem
  idézett hely „a szótár ezt a helyet nem idézi”, a csak tartományban idézett és a nem azonosítható pont külön mondatban — tippelt pont
  nincs (DT178).
- **Kutatói réteg:** a korábbi teljes tartalom (fej, kibontott szakaszok kiemeléssel, összecsukott futamok, kutatói megjegyzés,
  szónézet-mutató) változatlanul, alapból csukott `<details>`-ben, „Szótári apparátus” felirattal. **Jelölő:** `<!-- APPARATUS-KEZDET: <Strong> -->`
  … `<!-- APPARATUS-VÉGE: <Strong> -->` (egy helyen: `lexikon_general.APPARATUS_KEZDET`, `APPARATUS_VEGE`, `APPARATUS_RX`; a SEMA 2.40 és a
  kapu csak hivatkozik). A `<details>` sor szándékosan attribútum nélküli.
- **F10 (2):** a csukott futam címe glosszával: „2. — földdarab, földbirtok (N hivatkozás)”, futamnál „5. – 7. (3 szakasz): ország,
  terület, vidék · …” — a #182-nek ezt már nem kell megcsinálnia (N108 a generátorban teljesül; a lap még nem generálódott újra).
- **Egy bevezető:** a „Szótári tagolás” bekezdés szótáranként egyszer, a 4.2 elején, olvasói szöveggel. **Egy törzsalak:**
  „Hithpa'el — Hithpael — perfectum” → „Hithpa'el — perfectum”.
- **Kapu:** `olvasoi_kapu.py` `BDB_OLVASOI` (BUKÁS): az olvasói rétegben feloldatlan rövidítés (`_N`, zárójeles forrásjel, ᵐ ᵑ ⅏ √,
  egybetűs rövidítés, a `bdb_jelek.tsv` 3+ betűs szerző-/szövegtanú-jele, „szerző mű szám” alak), belső címke vagy nyers sorszám
  (sorszám, BDB-azonosító, „nincs címke”, ⓘ, kutatói jel). Csak a kétrétegű kártyát hordozó új szerkezetű lapon fut; a SEMA 3.11
  újragenerálva (`szabalyok.py --kapulista --ir`: naprakész). Mérés: a minta 0 BUKÁS (az olvasói kapu összesen 0 BUKÁS, 25 FIGY; a
  jelenlegi lap is 0 BUKÁS, 25 FIGY); a régi lapokon a kapu 0 találatot ad.
- **A meglévő `<details>`-kezelés:** `kiejtes_szoveg.py` a `<details>`-számlálóval dolgozik — a jelölő ezért attribútum nélküli; a
  kiejtés-mérés (`naplok/KIEJTES_elso_elofordulas_meres.py`) a mintán és a jelenlegi lapon azonos. `torzscikk_general.py` csak az 5.
  szakasz `<details>`-ét olvassa (a 4.2-t nem). Az olvasói kapu a HTML-megjegyzést kiveszi. A lektor-felület (`lektor_felulet/lapnezet.py`)
  üres sorral határolt blokkokra bont; a `<details>` és a megjegyzés-sor már ma is előfordul a lapon — **nem futtattam**, kódolvasás alapján
  nem bukik.
- **E28:** l. a 8. szakaszt (a kapcsolóval mind az öt nézet bájtra azonos).
- **Minta (a repón kívül):** `C:\Users\bases\AppData\Local\Temp\claude\aa58ea4f1403746e\4a9af85a-3b17-4dbd-95ea-f0d25820c95d\scratchpad\f104_minta\`
  — a teljes lap: `lexikon\HAMART-001_TUDOMANYOS.md`; kivágva: `HAMART-001_4.2_heber.md`, `HAMART-001_4.2_gorog.md`.
- **Nem a #104-é (változatlan):** a 2. táblázat „(nincs címke: 1.b)” cellája, a lábjegyzetek „‹E1› … sorszám” nyelve, a 4.9 tömörítése. A
  módosított kódban egyik sem áll. A kutatói rétegben (apparátus) a „BDB8032 *(a H7451 1. BDB-szócikke a 3-ből)*” sor és a „sorszám” a
  kutatói megjegyzésben megmarad (kutatói réteg); az olvasói rétegben nincs.

## 7. Tesztek

- `python eszkozok/teszt_futtat.py --gyors` (WSL, `~/pardes/pardes.db`): 11 fájl zöld, összesítő sor: `együtt 312.1 mp  (a lassú fájlok
  nélkül)` (`teszt_olvaso_szerver.py`: „Ran 104 tests … OK (skipped=2)”; `teszt_tervezo.py` 49, `teszt_pilot_aranymintaval.py` 22 OK).
  A lassú `teszt_szintek.py` nem futott (N110: a main-en is piros).
- Új tesztek: `TestF104Egysegek` (4), `TestF104BdbJeloles` (9) — `teszt_olvaso_szerver.py`; `KetreteguBdbKartya` (4) —
  `teszt_szotari_gerinc.py`; `BdbOlvasoiReteg` (3) — `teszt_olvasoi_kapu.py`.
- A lexikon-tesztek (`teszt_szotari_gerinc`, `teszt_olvasoi_kapu`, `teszt_lexikon_adatres`, `teszt_szerepmatrix`,
  `teszt_ellenoriz_vedokorlat`, `teszt_torzscikk_migralt`) Windowson: a változtatás előtt és után **ugyanazok** a tesztek buknak
  (6, 1, 1, 3, 1, 1; előzetes, a #104-től független — a lexikon-fájlok ideiglenes visszaállításával mérve); az új tesztek zöldek.

## 8. Az orkesztrátor döntései után (F104.5–F104.7; DT689 🟢, DT691, N118)

- **Kapcsoló (DT691 (1)):** `eszkozok/lexikon_general.py` `KETRETEGU_BDB_KARTYA` (frozenset, ma üres; egyetlen hely), a
  `bdb_kartya_aktiv(id)` = benne van **és** új szerkezetű lap. **A #182 teendője:** a HAMART-001 újragenerálásakor a kapcsolóba
  felvenni a `'HAMART-001'`-et, és a lapot a teljes folyamattal újragenerálni (az E28 akkor az új alakot várja). A régi lapok a saját
  teljes folyamatukban kerülnek bele. A `BDB_OLVASOI` kapu a lap `APPARATUS` jelölőjéhez igazodik: kikapcsolt kártyánál (régi alak)
  nem fut.
- **E28 (kikapcsolt kapcsolóval):** az E28-utánzat (`general.py --kimenet` a repón kívülre, a commitolt fájl `ts=` dátumával;
  a munkafa `lexikon/` = `origin/main`): ISTENTISZT-001, ALVIL-001, TEREMT-002, ANTROP-001, HAMART-001 — mind **AZONOS**.
- **Bekapcsolt minta:** a kapcsoló csak egy repón kívüli futtató folyamatában bekapcsolva
  (`scratchpad\minta_bekapcsolva.py`); a minta az eddigivel azonos, kivéve a (3) sorait és a dátumsorokat. Olvasói kapu a mintán:
  0 BUKÁS, 25 FIGY (mint a mai lapon).
- **Alakjegyzékes szakasz (DT691 (3)):** ha a szakasznak van magyar meghatározása az alak után, az áll („Niph'al — átkozott”,
  „Hoph'al — átkozottnak lenni”, „Hoph'al — elrontott, tönkretett, forrásról”); ha nincs: „Pi'el — a szótár csak alakot közöl
  (5 hely)”. Teszt: `test_csak_alakot_kozlo_szakasz`.
- **Licenc (DT689 🟢):** `adat/licencek.tsv` 26. sor `Macula_heber` (CC BY 4.0, `tisztazott`), a használt fájl
  `konkordancia/Macula_heber_*.tsv` (`datasetek.tsv`; a DB `token_macula`); `morf_kulcs_heber` (51.), `morf_nyelv_aramai` (52.)
  szintén `tisztazott`. A szó-lap BDB-blokkjának forrássora mostantól ezeket a táblákat és a `bdb_vers_jelentes`-t is megnevezi (F104.7).
- **`?vers=`:** kimarad (DT691 (2)), N118.

## 9. ⛔ Felhasználói próba (a brief 4. lépése)

**Indítás:** a „PaRDeS olvaso - belso (tervezo)” parancsikon a főcheckoutot indítja; ezt az ágat így:

```bash
wsl -d pardes -e bash -lc "cd /mnt/e/Claude/Bible-Study/charming-almeida-256e42/eszkozok/olvaso_szerver && PARDES_DB=\$HOME/pardes/pardes.db PARDES_KIADAS=belso ~/pardes/eszkozok/olvaso_szerver/.venv/bin/python alkalmazas.py --port 8791"
```

(leállítás: Ctrl+C, vagy `wsl -d pardes -e bash -lc "fuser -k 8791/tcp"`). A próba után a szerver nem fut (leállítva).

**Lapok (versből megnyitva, a szó-fülön):**

| Mit mutat | URL |
|---|---|
| erős: a BDB idézi (1. e., és az alaktanban) | http://localhost:8791/1Moz/1/5?szo=H1242&ful=szo |
| erős, másik címszó (II. szakasz: 3.) | http://localhost:8791/1Moz/2/9?szo=H7451&ful=szo |
| „nem idézi”, kiemelés nincs (melléknév) | http://localhost:8791/1Moz/19/19?szo=H7451&ful=szo |
| gyenge (b): idézet nélkül, a Pi'el szakasz, jelentéspont nélkül | http://localhost:8791/1Moz/6/16?szo=H3615&ful=szo |
| gyenge (a): a BDB nyomtatott igehelye hibás (forras_hiba) | http://localhost:8791/2Moz/2/6?szo=H1802&ful=szo |
| csoportsorok | http://localhost:8791/1Moz/1/1?szo=H0430&ful=szo |
| vers nélkül: pontos hivatkozásszám, kattintható helyek, kiejtés a Címszóban, `<sub>` a nyers blokkban | http://localhost:8791/szo/H6975 , http://localhost:8791/szo/H7451 |

**A lexikonlap-minta:** a 6. szakasz útvonala; a pilot (ISTENTISZT-001 / a HAMART-001 jelenlegi lapja) 4.2-ével összevetve.
