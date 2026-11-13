---
feladat: 218
cim: A lapgenerátor újraírása nulláról — bemeneti jegyzék, lapmodell, két megjelenítés
kod: GENERATOR_UJ
tipus: feladat
fazis: folyamat
modell: fable
allapot: nem_indult
ad: új lapgenerátor (`eszkozok/lapgen/`), amelyben minden bemenet egyetlen hozzáférési ponton lép be, a lap látható szövege csak kézi prózából, sablonmondatból vagy idézetből jön, a lapot és az olvasó szervert ugyanaz a lapmodell számolja; a HAMART-001 és az ISTENTISZT-001 lapja ezzel generálódik, a régi `lexikon_general.py` archívumba megy
kovetkezo: "azonnal indul (mag: új modulok); az átállási szakasz (F218.18–F218.20) a #217 (PR #725) után; a felhasználó kérése: a munka Fable-lel fusson; Te: /kovetkezo"
munka: folyamat
olvas: [adat/SEMA.md, tematikus_lezart/HAMART-001*, tematikus_lezart/naplok/HAMART-001*, tematikus_lezart/ISTENTISZT-001*, tematikus_lezart/naplok/ISTENTISZT-001*, adat/generalt_nezetek.tsv, adat/licencek.tsv, adat/lap_befagyasztas.tsv, "eszkozok/lexikon_general.py", "eszkozok/szerep_*.py", eszkozok/olvasoi_kovetkeztetes.py, eszkozok/olvasoi_utofeldolg.py, eszkozok/tablajegyzet.py, eszkozok/kiejtes.py, eszkozok/heber_kiejtes.py, eszkozok/bdb_tagolas.py, eszkozok/bdb_rovidites.py, eszkozok/bdb_vj_szabaly.py, eszkozok/karoli_kh_szuro.py, eszkozok/torzscikk_general.py, eszkozok/olvaso_szerver/, eszkozok/olvasoi_kapu.py, eszkozok/ellenoriz.py, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, naplok/HIBA_MECHANIZMUSOK.md, motivumok/HAMART-001.md, motivumok/ISTENTISZT-001.md, lexikon/HAMART-001_TUDOMANYOS.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md]
ir: [eszkozok/lapgen/, adat/lapgen_konfig.tsv, adat/olvasoi_nevtabla.tsv, adat/forras_allapot.tsv, adat/lapgen_elteres_engedely.tsv, adat/SEMA.md, eszkozok/olvaso_szerver/, eszkozok/olvasoi_kapu.py, eszkozok/ellenoriz.py, eszkozok/ellenorzes/szabalyok.py, adat/generalt_nezetek.tsv, lexikon/HAMART-001_TUDOMANYOS.md, lexikon/HAMART-001_KIZARASOK.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, archivum/lexikon_general/]
fugg: []
nem_fugg: [70, 121, 123, 146, 151, 178, 179, 181, 203, 212, 217]
---

# F218_GENERATOR_UJ_BRIEF.md — A lapgenerátor újraírása nulláról

*FELADATOK #218 · Modell: fable · v1 · 2026.11.13 · forrás: a felhasználó („vegyük korábbra a generátor írást”, 2026-11-13); DT-F212e, DT-F212f; a generátor-térkép (`GENERATOR_TERKEP_SPEC_2026-11-13.md`, `…_FUGGELEK_…`) és a súlyossági leltár (`GENERATOR_HIBALEltar_SULYOSSAG_2026-11-13.md`), mindhárom a megosztott jegyzetmappában; a végleges befogadáskor a három fájl a `naplok/F218_*` alá másolandó.*

**Függés.** A generátor magja (F218.1–F218.17) új modulokban készül, ezért azonnal indulhat; a #217 és a #709 (ISTENTISZT-001 forrása, DT-F194h szópár) merge-e nem előfeltétel. Az átállási szakasz (F218.18–F218.20: a jegyzék G01–G03 `parancs` mezője, az E28 lista megszűnése, a régi generátor archiválása) a #217 (PR #725) merge-e után jön. A `fugg` ezért üres, a `nem_fugg` a DT-F218h szerint áll.

---

## 1. Cél

A régi generátor (`eszkozok/lexikon_general.py`, 10 051 sor, kb. 20 segédmodul) helyett új, rétegzett generátor, amely a visszatérő hibák négy gyökérokát szerkezetileg zárja ki:

| Gyökérok | Hibanapló | Mi zárja ki az új generátorban |
|---|---|---|
| a látható szöveg belső adatból, regex-cserével készül | M-CSERE | alapszabály (2. pont): csak próza, sablonmondat, idézet; névtábla; nincs utólagos csere (GK-08) |
| ugyanazt az adatot több út olvassa, eltérő szabállyal | M-NYERS | bemeneti réteg, B-azonosítónként egy függvény (GK-01) |
| a javított adat mellett a nyers maradt a bemenet | M-NYERS | a nyers forrás csak a javító modulon belül érhető el (GK-02); pillanatkép csak frissességi kapuval (GK-03) |
| HAMART-ra szabott ágak | – | egy lapszerkezet, 0 motívumazonosító a kódban (GK-05); minden kapu minden lapon (GK-04) |

A súlyossági leltár szerint a 357 megerősített tételből 24 magas; ezek 10 különböző hibát jelentenek, és mind a négy osztály valamelyikébe esnek (a leltár „Magas tételek” táblája).

## 2. Alapszabály (DT-F212e)

1. **A lap látható szövege csak három forrásból jöhet:**
   - kézi próza (a rések a `motivumok/<ID>.md`-ből és a kézi forrásokból, változatlanul);
   - strukturált értékű sablonmondat: zárt értékkészletű mező (enum) → rögzített mondat a sablontáblából; forrás → a forrásjegyzék olvasói neve; szám → a lapmodell száma;
   - szó szerinti idézet (bibliavers, szótárszöveg), forrásmegjelöléssel.
2. **Belső szövegből cserével olvasói szöveg nem készül.** Nincs olyan lépés, amely renderelt Markdownt vagy belső mezőszöveget regexszel átír (a mai `olvasoi_atiras`, `kesz_lap_elotte`, `kesz_lap_utana`, `UJ_SZOVEGCSERE`, `UJ_JELMAGYARAZAT_CSERE`, `_lxx_ujraminosit` cseréje, `nevelo_le`, `OU.alkalmaz`, `TJ.onref_csere` funkciója a sablonba kerül).
3. **Olvasói névtábla minden belső kulcsra** (`adat/olvasoi_nevtabla.tsv`): forrás-azonosító, mezőnév, állapotérték, szerepnév, hálónév, igazolás-érték → olvasói név. **Ismeretlen kulcs kemény hiba** (a generálás megáll, a lap nem íródik ki), nem átengedett nyers szöveg.
4. **Proveniencia csak HTML-megjegyzésben és a Kolofonban.** A látható mondatba nem kerül `scope=`, fájlnév, döntésszám (DT…, #…, N…, G…, F…), mezőnév vagy belső számláló.
5. **A kapu pozitív szerkezeti szabályokat ellenőriz** (a mintalaphoz mérve: szakaszrend, minden igehely alatt teljes mondat + „Funkció:”, a táblák alatti jegyzet nem ismétli a cellát, a forrásnév a jegyzet végén áll), és **alakosztályokat** a renderelt szövegen (aláhúzásos azonosító, `.tsv`/`.py` fájlnév, `DT\d+`, `#\d+`, `N-?F?\d+`, `[HG]\d{3,5}\.` nyers szótárfej, héber + `_\d+` számláló, `sz<n>`, nyers `<br>`, tört írásjel `,;` `;.`). **Szólista nem kapu.**

*A szabály szövege a `sablonok/6_PaRDeS_lexikon_oldal_sablon.md`-be kerül (F184: lapszabály ott áll); a brief csak hivatkozik rá.*

## 3. Hatókör

**Benne van.**
- Új csomag `eszkozok/lapgen/` négy réteggel (5. pont), a meglévő modulok érintetlenül hagyásával az átállásig.
- A lexikon TUDOMANYOS-, KIZARASOK- és TORZSCIKK-nézete (G01–G03).
- Az olvasó szerver blokkjainak átkötése ugyanarra a lapmodellre (6.2).
- A lapszövegre kereső kapuk (`olvasoi_kapu.py`, `ellenoriz.py` lapszöveg-szabályai) átírása a modellre, az átállás commitjában.
- Az átállás: a jegyzék G01–G03 `parancs` mezője, az E28 lista megszűnése, a régi generátor archiválása.

**Nincs benne.**
- Új tartalom, új próza, új motívum. A rések szövege nem változik.
- A befagyasztott lapok (`adat/lap_befagyasztas.tsv`, DT816): nem generálódnak; az új generátor kihagyja őket, kimondott üzenettel (T2 eldőlt).
- Az ISTENTISZT-001 2. kiadása: a `/kiadas` külön menete az átállás után (a felhasználó döntése: az új generátorral jön ki).
- A nyílt mag exportja (`nyilt_mag_export.py`): csak a körkörös függés (B62) szűnik meg; az export maga külön tétel.

## 4. Bemeneti jegyzék

A bemenetek a #217 jegyzékében (`adat/generalt_nezetek.tsv`) állnak, `tipus=bemenet` sorként, a térkép B01–B64 számaival (változatlanul; új bemenet B65-től). Ez a brief **nem hoz létre második jegyzéket**: a `hozzaferesi_pont` oszlop a #217 óta dokumentáció, ez a brief teszi végrehajtottá.

**A bemeneti réteg szerződése (`eszkozok/lapgen/bemenet/`):**
- B-azonosítónként pontosan egy nyilvános függvény (`b07_karoli_1908()` stb.); a modul a jegyzékből tölti az útvonalat, kódba írt `adat/` vagy `konkordancia/` útvonal nincs.
- Betöltéskor kapu: létezés; oszlopnév szerinti fejléc-ellenőrzés (nem oszlopszám, l. seged_A.22); a javítótábla alkalmazva (B17, B18, B20, B43); frissesség a pillanatképeken (B05, B06, B18, B19, B21, B36, B38, B49: forrás-hash vagy a mai Strong-halmaz).
- Hiányzó kötelező bemenet → BUKÁS. Opcionális bemenet hiánya → a lapmodellben kimondott hiány (`hiany` mező), nem üres lista (GK-06).
- Kimenet: immutábilis adat (tuple / frozen dataclass). Folyamat-szintű gyorsítótár csak a bemeneti rétegben, kulcsa a fájl hash-e.
- **Olvasási napló**: (B-azonosító, útvonal, hash) — a Kolofon, a 12. Irodalom és a blokkfejlécek forráslistája ebből jön (GK-07).
- A TSV-olvasás `split('\t')`, az írás `'\t'.join()` (CLAUDE.md).

**A térkép B-sorainak módosításai (a #217 jegyzékébe, `forras=manual`):**

| B | Változás | Ok |
|---|---|---|
| B04/B06 | a csoportos kizárás versszáma nem a `forras_kereses` szövegéből, hanem a B06 mérésből, frissességi kapuval | M13 |
| B08 | a TAHOT (vers, Strong) ismétlődési szabálya nevesített paraméter (T4) | M1, GK-14 |
| B10/B12/B13 | **egy kiejtés-szolgáltatás** (`kiejtes.py` + `heber_kiejtes.py` + `LEMMA_VALTOZAT`), a lap és a szerver is ezt hívja | M2, H6, GK-13, OLV-1 |
| B11 | kivezetve (a `--helyi-lexicon` kapcsoló megszűnik) | O7 |
| B14 | a fordítás `allapot` mezője a lapmodellbe kerül; az `elavult` sor munka közben jelölve jelenik meg, kiadáskor kapu tiltja (T5) | M5, GK-15 |
| B15 | egy glossza-függvény, egyféle hiánymondat | M10, GK-16 |
| B17 | a betűjavítás minden lapon (a `BDB_BETU_JAVIT` halmaz megszűnik); az olvasói réteg is a teljesen javított szöveget kapja | GK-18, seged_B.2 |
| B20 | `thayer_bemenet.szakaszok(strong)` | M8, GK-N178 |
| B43 | csak `karoli_kh_szuro.megerositett_sorok`; az elvetett-szám a szűrő nyilvános API-jából; a deklaráció a javított forrást nevezi | kapuk.1, lg_6500.18 |
| B48 | a jóváhagyás érvényessége a `lap_commit`-hoz kötve (T9) | lg_5200.31 |
| B49 | a lektor-sor adattáblából (`adat/kiadasok.tsv` vagy új oszlop), nem a napló regexéből | lg_5200.12 |
| B51 | a döntés dátuma a `dontes_allapot` modulból, nem a `DONTESEK.md` regexéből | lg_6500.5 |
| B54 | minden párosítás használható, szűrő és páronkénti jelölés nélkül; a `bizonyossag` címke belső, nem jelenik meg; hiányzó könyvfájl = kimondott hiány (T6) | H10, GK-19 |
| B60 | **nem bemenet** (a meglévő lap); a régi `frissit_meglevo_fajlt` út megszűnik | GK-12 |
| B61/B62 | a `bdb_szelet._lapit` és a `csoport_tagjai` a `szamitas/` rétegbe költözik; a szerver és az export onnan importál | O5 |
| B63 | egyetlen könyvnév-normalizálás; a `KH_KONYV_JAVIT` és az `EXTRA_KONYV` sorai a táblába | M17, H12, GK-17 |
| B65 | `adat/olvasoi_nevtabla.tsv` (új) | 2. pont 3. |
| B66 | `adat/lapgen_konfig.tsv` (új): küszöbök, szűrő-halmazok, kiadási azonosítók | spec 5. pont |
| B67 | `adat/forras_allapot.tsv` (új): a források állapota (Peshitta, Targum-fedés, közel-keleti réteg, Chain Lineage licenc) | T7 |

## 5. Felépítés

Négy csomag, egyirányú függéssel (`bemenet` ← `szamitas` ← `megjelenites`; a `konfig` mindenkié). A függés irányát statikus teszt ellenőrzi.

1. **`lapgen/bemenet/`** — az egyetlen hely, amely fájlt nyit (4. pont).
2. **`lapgen/konfig/`** — a `lapgen_konfig.tsv`, a névtábla és a sablontábla betöltése. A spec 5. pontjának minden rögzített száma, szűrő-halmaza, heurisztikája innen jön (TSK `Votes ≥ 15`, `ALAPVONAL_*`, `LXX_TARS_KUSZOB`, `KAROLI_*`, `LXX_PAROK_TOP`, `NEVELO_MONDAT_SZO`, `LXX_DONTES_MEGJELENO_*`, `BDB_ARAMI_ELSO`, a görög/latin tő-heurisztikák, `TORZS_MAGYAR`, `ROKON_NYELVEK`); a mondatban álló szám a konfig értékéből formázódik.
3. **`lapgen/szamitas/`** — tiszta függvények, motívumazonosító-ág nélkül; kimenetük a **lapmodell** (6.1). A gépi számegyezés-kapuk itt futnak, a modellen (GK-04, GK-09).
4. **`lapgen/megjelenites/`** — `md/` (TUDOMANYOS, KIZARASOK, TORZSCIKK) és `olvaso/` (a szerver blokkjai). Az olvasói szöveg itt keletkezik, sablonból; utána az alakosztály-kapu és a pozitív szerkezeti kapu fut a kész szövegen, csak ellenőrzésre.

**Belépési pont:** `python eszkozok/general.py --cel lexikon2 --id <ID> --kimenet <könyvtár>` az átállásig; az átállás után a `--cel lexikon` erre mutat, és a jegyzék G01 `parancs` mezője ezt nevezi.

## 6. Lapmodell és két megjelenítés

### 6.1 Lapmodell

Szakaszonként egy adatosztály: `Szakasz(azonosito, cim_kulcs, sorszam, horgony, szamok, sorok, hianyok, kovetkeztetes_kod, forrasok)`.
- `sorszam` és `horgony` a szakaszmodellből generált; a szövegben álló „N. szakasz”, „4.x pont”, `#horgony` ebből jön (GK-10).
- `forrasok`: B-azonosítók halmaza az olvasási naplóból; a megjelenítés a névtáblán át nevezi meg őket.
- `hianyok`: kimondott hiány (enum + paraméter), sablonmondatból renderelődik.
- `kovetkeztetes_kod`: az `olvasoi_kovetkeztetes` szabályainak enum-kimenete; a mondat a sablontáblában.
- A modell JSON-ba sorosítható (teszthez és a szerver gyorsítótárához), de a szerver **nem** generált JSON-pillanatképet olvas, hanem a `szamitas/` függvényeit hívja (O5).
- Globális állapot nincs (GK-11): két motívum generálása fordított sorrendben bájtra azonos kimenetet ad.

### 6.2 Két megjelenítés: md-lap és olvasó szerver

„Egy számítás, két megjelenítés”: ugyanaz a szabály egy helyen él (a ma közös `bdb_vj_szabaly` mintájára).
- **OLV-1 (kiejtés).** A szerver szó-lapja és versnézete a kiejtést a lap kiejtés-szolgáltatásából veszi (`kiejtes.py`, `heber_kiejtes.py`, `LEMMA_VALTOZAT`), nem a `strong_szotar.kiejtes` mezőből (`lekerdezesek.py:522`) és nem a `token_eredeti.kiejtes`-ből. Teszt: H2398, H7121 (ma a szerveren ragozott alakból jön, pl. „i.yik.Ra”); a szerver és a lap ugyanazt a karakterláncot adja.
- **OLV-2 (szótári fordítás).** A szerver a magyar szótári szöveget ugyanazon a B14/B18/B20 ponton veszi, mint a lap (F213-eset, M-NYERS).
- **OLV-3 (belső szavak).** A szerver blokkjai ugyanazt a névtáblát és alakosztály-kaput használják (pl. „lxx_bridge”, „token_par”, „glosszak_heber_hu”, „(#121)” a mai felületen).
- **GK-22.** Egy motívumon a szerver blokkjainak és a Markdownnak a számai gépi összevetésben azonosak.

## 7. Követelménylista

Minden sor egy teszt az `eszkozok/lapgen/tesztek/`-ben (a futtató: `python eszkozok/teszt_futtat.py`, ha az olvasó-szerver tesztjeit érinti). Az azonosító a tesztfüggvény nevében áll.

### 7.1 Szerkezeti követelmények (a spec 6.4, kiegészítve)

| ID | Követelmény | Mérhető teljesülés |
|---|---|---|
| GK-01 | egy adat, egy hozzáférési pont | statikus teszt: `adat/` vagy `konkordancia/` útvonalat csak a `bemenet/` nyit; minden olvasás egy B-azonosítóhoz kötött |
| GK-02 | a javított változat kötelező | a nyers függvény (`_nyers_sorok`, nyers TSV) a bemeneti rétegen kívül nem hívható |
| GK-03 | pillanatkép csak kapuval | a 4. pont pillanatképei eltérésnél BUKÁS; teszt egy elavított másolattal |
| GK-04 | kapu minden lapon | `lxx_egyezes`, `hely_egyseg`, `teljesseg` (minden hálóra: strong, karoli, szotar), melléklet-kapu minden generált lapon |
| GK-05 | nincs motívumazonosító a kódban | `[A-Z]+-\d{3}` a `lapgen/` kódján 0 találat (tesztek kivételével) |
| GK-06 | nincs néma hiány | B39, B40, B46, B35 slug, B59 hiánya: kötelezőnél BUKÁS, opcionálisnál kimondott hiánymondat |
| GK-07 | a forrásmegjelölés a valódi olvasásból | a Kolofon/Irodalom/blokkfej forrás-halmaza = olvasási napló; a licencszöveg csak B01-ből |
| GK-08 | nincs utólagos szövegcsere | 0 `re.sub`/`.replace` renderelt lapszövegen a `megjelenites/` alatt (statikus teszt; engedélylista csak HTML-escape-re) |
| GK-09 | kapu a modellen | a számegyezés-kapuk a lapmodellt olvassák, nem a lapszöveget |
| GK-10 | szakaszszám és horgony a modellből | szakaszrend-csere után 0 hibás belső link |
| GK-11 | nincs globális állapot | fordított sorrendű generálás bájtra azonos |
| GK-12 | a generált fájl nem bemenet | a `lapgen/` nem olvas `lexikon/` alatti fájlt |
| GK-13 | egy kiejtési út | lap és szerver ugyanazt adja; H2403a/b, H2398, H7121 |
| GK-14 | TAHOT-ismétlődés szabálya | (vers, Strong) ismétlődésnél a T4 szerinti választás; az összevont 9 versnél a kulcs a versösszevonás szerint |
| GK-15 | fordítás-állapot (T5) | egy `elavult` sorral: (1) munka közben a régi magyar szöveg áll, „a fordítás felülvizsgálat alatt” sablonjelöléssel; (2) a kiadási kapu BUKÁS-t ad, ha a lap bármely fordítása `elavult` vagy hiányzik; (3) a lapmodell listázza az érintett sorokat, hogy a cikk menete újrafordíttathassa őket (ma 311 `elavult` sor a táblában) |
| GK-16 | egy glossza-út | egy függvény, egyféle hiánymondat |
| GK-17 | könyvnév egy táblából | 0 kódba írt könyvnév-alias |
| GK-18 | BDB-betűjavítás minden lapon | a lap, az olvasói réteg és a szerver ugyanazt a javított BDB-szöveget adja |
| GK-19 | Károli–Strong párosítás (T6) | minden pár számít; a látható szövegben 0 „alacsony”/„magas” bizonyossági címke és 0 páronkénti bizonytalan-jelölés; a mért pontosság (95,06%, `naplok/KAROLI_PONTOSSAG_jelentes.md`, F172) egyszer áll, a Módszertanban, a konfigból; hiányzó könyvfájl = kimondott hiány |
| GK-20 | törzscikk a lapmodellből | a TORZSCIKK nem olvassa vissza a TUDOMANYOS-t |
| GK-21 | a HAMART-001 regressziós kapui | sablon 597: 0 BUKÁS az olvasói kapun; a Döntési út számai összeadódnak; döntés nélküli vers 0; Nave-blokk nem üres; `ellenoriz.py` 37–40. zöld |
| GK-22 | olvasó = lap | 6.2 |
| GK-23 | olvasói névtábla | minden belső kulcs a táblában; ismeretlen kulcs → kivétel (teszt egy kitalált kulccsal) |
| GK-24 | alakosztály-kapu | a 2. pont 5. alakosztályai a renderelt lapon 0 találat; a kapu a HTML-megjegyzéseket kihagyja |
| GK-25 | pozitív szerkezeti kapu | a 2. pont 5. szerkezeti szabályai a mintalaphoz mérve |
| GK-26 | kapu-mutációs próba (Fable 6.) | a tesztkészlet szándékosan hibás lapváltozatokat állít elő (szivárgó mezőnév, ismételt címke, tört írásjel, jegyzet = cella, belső szám a mondatban, hiányzó „Funkció:”); mindegyiket legalább egy kapu megfogja; a jelentés kapunként mutatja, mit fog |
| GK-27 | jóváhagyás a lapállapothoz kötve | a Kolofon jóváhagyás-mondata a T9 szerint, a `lap_commit` alapján (ma a mezőt senki nem olvassa) |
| GK-28 | állapotmondat adatból | a SECE-, Peshitta-, Targum-, közel-keleti, Chain Lineage-mondat a B67-ből és az adat tényleges állapotából számolódik; teszt: a görög rövid glossza-tábla léte esetén a „még nincs” mondat nem áll (ma hamisan áll: HAMART 2×, ISTENTISZT 3×) |
| GK-29 | determinizmus (GK-B9) | a `ts=` a bemenetek hash-éből vagy explicit `PARDES_DATUM`-ból; két futás bájtra azonos |

### 7.2 N-F212a (a hibaleltár CS3-maradéka)

A spec 6.1 táblája változatlanul: GK-A1, GK-A6, GK-A10, GK-A11, GK-A12, GK-A13, GK-A14, GK-A15, GK-B5, GK-B8, GK-B9, GK-C3, GK-C9, GK-D3. A cím nélküli tételek leírását az 1. fázis veszi át a `GENERATOR_HIBALELTAR_2026-11-11.md`-ből (jegyzetmappa), és a teszt docstringjébe írja. Mérce: újramérve az új generátoron, 0 eltérés.

### 7.3 N-F215a (N178): GK-N178

A 4.2 Thayer-kártya a `thayer_bemenet.szakaszok(strong)`-ból; a 15 érintett Strongon (G0260, G0575, G0846, G1100, G1909, G2675, G3536, G3563, G4151, G4404–G4407, G5132, G5567) a lapra kerülő angol szöveg = a javított szöveg. A két mai lapot a cáfoló keresése szerint nem érinti; az 1. fázis ezt méri.

### 7.4 DT-F194h (szópár): GK-SZOPAR

A spec 6.3 nyolc feltétele, a #709 merge-e után a main-ről portolva; a `teszt_f194_szopar.py` `SzoparLanc` az új generátoron is zöld.

### 7.5 A spec 5. pontja tesztesetként (Fable 6. pont)

A spec 5. pontjának minden sora (motívumkapcsoló, felülírás, küszöb, adathalmaz-konstans, állapotmondat, licenc/forrás a kódban, személy és kiadás, szakaszszám a szövegben, döntésszám a lapon, szövegmintás kapu, heurisztika, globális állapot, holt kód) egy `TS-<nn>` teszt: a régi helyen álló értéket az új generátor a konfigból / az adatból / a szakaszmodellből veszi, vagy (holt kód, motívumkapcsoló) nincs megfelelője. A tesztváz az 1. fázis első tétele, a kód előtt.

### 7.6 A hibanapló és a leltár példányai tesztesetként

Minden eset egy `HN-<nn>` teszt a mai lapról vett valódi szövegrészlettel (bemenet: a lapmodell adott sora; elvárt: a helyes olvasói szöveg vagy a kapu BUKÁS-a):

| ID | Mechanizmus | Eset |
|---|---|---|
| HN-01 | M-CSERE | ISTENTISZT 2·5, 3·10, 3·13: a jegyzet ismétli a cellát |
| HN-02 | M-CSERE | címke-ismétlés: „A formula nincs a versben: Nincs meg a formula a versben…” |
| HN-03 | M-CSERE | forrásnév a mondat közepén: „(a BDB-szótár)” |
| HN-04 | M-CSERE | „hivatkozas_kezi,;”, „kollokacio … szerkesztő-chat … negativ_kriterium” |
| HN-05 | M-CSERE | „felhasználó”, „orkesztrátor” a lapon (#178) |
| HN-06 | M-CSERE | „gerinc” a látható szövegben |
| HN-07 | M-CSERE | HAMART 4.2: „…Thayer-fordításból (a lexikon fordítástáblája, sz<n> sorok,; …)” (5×) |
| HN-08 | M-CSERE | ISTENTISZT: DT-számok (73), „#142”, „N59”, fejlesztői „(G10)”, „(F131, DT272 (d))” a látható szövegben |
| HN-09 | M-CSERE | ISTENTISZT: nyers BDB-fej „H7121. q…”, héber számláló „…_724”; HAMART: `_226` (generalt_proba 2438) |
| HN-10 | M-NYERS | Károli-KH: a lap, a nyílt mag és a forrásdeklaráció a nyerset nevezi (3 eset) |
| HN-11 | M-NYERS | teljesség-mérés pillanatképe (HAMART 1.2); az ISTENTISZT-naplóban 0 `strong=` token |
| HN-12 | M-NYERS | angol Thayer nyersen (N-F215a) |
| HN-13 | M-NYERS | szótári fordítás rossz bekötése az olvasóban (F213) |
| HN-14 | M-NYERS | szerver-kiejtés a `strong_szotar` mezőből (OLV-1) |
| HN-15 | állapotmondat | „magyar rövid glossza-tábla a görögre még nincs” |
| HN-16 | HAMART-ág | `TEMATIKUS_SAJAT_SZO` néma `replace` (Jel 22:3, G2652) |
| HN-17 | HAMART-ág | `lxx_osszesites` kapu az új szerkezeten némán kimarad („3. LXX” előtag) |
| HN-18 | M-ZOLD | „0 BUKÁS” ≠ minőség: a GK-26 mutációs próba fedi |

A `naplok/HIBA_MECHANIZMUSOK.md` minden új bejegyzése az átállásig ide is bekerül (a menet végén összevetés: 0 hiányzó eset).

## 8. Regressziós mérce

**Referencia.** Az 1. fázis elején, a #709 és a #217 merge-e utáni main-en, a régi generátorral, rögzített `PARDES_DATUM`-mal, a repón kívüli ideiglenes könyvtárba:
- **R-HAMART**: `lexikon/HAMART-001_TUDOMANYOS.md` és `_KIZARASOK.md` (a #709 javítása utáni állapot);
- **R-ISTENTISZT**: az ISTENTISZT-001 lapja a #709 forrásából (új szerkezet, DT-F194h, minta-kapu).
A referencia hash-e a jelentésbe kerül; a fájlok nem kerülnek a repóba.

**Mérce.** Az új generátor kimenete a referenciától csak az `adat/lapgen_elteres_engedely.tsv` sorai szerint térhet el. Oszlopok: `id`, `lap`, `szakasz`, `mechanizmus` (HN/GK/T azonosító), `regi_minta`, `uj_minta`, `ok`. Minden más diff-sor BUKÁS. A gépi összevető szakaszonként vödröz, és minden diff-sort egy engedélysorhoz rendel, vagy BUKÁS-t ad.

**Előre engedélyezett eltérés-osztályok** (a sorokat a 6. fázis tölti ki, mérés után):
- (a) a `ts=` determinisztikus (GK-29);
- (b) a forrásnév a valóban olvasott javított forrást nevezi (Károli-KH, Thayer; GK-07);
- (c) a Thayer-szöveg a javított forrásból (GK-N178; csak ha a lap érintett);
- (d) a fordítás-állapot (GK-15, T5);
- (e) az N-F212a tételek javításai (7.2);
- (f) a HN-esetek javítása: a látható belső szó, a cellát ismétlő jegyzet, a címke-ismétlés, a hamis állapotmondat eltűnik;
- (g) a T3, T4, T7, T9 döntéseinek következménye (a T6 a lap állításait nem szűkíti; a T5 csak `elavult` sornál hat).

A HAMART-001-en a várt diff kicsi (a mai csere-lánc olvasói kimenetét a felhasználó jóváhagyta; a sablonmondatok ezt adják vissza). Az ISTENTISZT-001-en a diff nagyobb, de minden sora az (a)–(g) osztály valamelyikébe esik.

**A számok szintje.** A lapmodell számai (igehely-halmazok, Döntési út, LXX-összesítés, KH-darabszám) a referencia lapszövegéből kinyert számokkal **eltérés nélkül** egyeznek, kivéve a (c)–(e) és (g) osztályt, ahol az eltérés oka soronként áll.

## 9. Lépések és commit-tételek

Minden tétel külön commit: `F218.<t>: …`. Az ág a saját új döntéseit a `dontesek/uj/<ágnév>.md`-be, a nyitott tételeit a `nyitott/uj/<ágnév>.md`-be írja, helyőrzővel.

**0. Előkészítés**
- F218.0 — modell-ellenőrzés; a magot nem blokkolja a #709/#217 (az átállási szakasz a #217 után); a T3–T9 válaszai a briefben (5. Döntésnapló). Hiányzó válasznál ⛔.
- F218.1 — referencia (8. pont) és alapmérés: a HN-esetek és a magas leltártételek előfordulása a két mai lapon (szám, hely); a 15 Thayer-Strong érintettsége; a TAHOT-ismétlődés (T4: hány sor kiejtése változik) és az `elavult` fordítások érintettsége a két lapon. Jelentés: `naplok/F218_jelentes.md`.

**1. Tesztváz (kód előtt)**
- F218.2 — a 7. pont minden sora egy failing teszt (GK, N-F212a, GK-N178, GK-SZOPAR, TS, HN); a mutációs próba váza (GK-26).

**2. Bemeneti réteg**
- F218.3 — `bemenet/` váza, jegyzék-olvasó, olvasási napló, fejléc- és frissességi kapuk; GK-01, GK-02, GK-03 zöld.
- F218.4 — B01–B33 függvényei. · F218.5 — B34–B67 függvényei. A 4. pont módosításai itt.

**3. Konfig és névtábla**
- F218.6 — `lapgen_konfig.tsv`, `olvasoi_nevtabla.tsv`, `forras_allapot.tsv`, a SEMA-bejegyzések; a névtábla kezdő sorai a mai `olvasoi_atiras`, `OLVASOI_FORRASNEV`, `_HALO_OLVASOI`, `IGAZOLAS_OLVASOI`, `AZONOSSAG_OLVASOI`, `UJ_OLVASOI_SZEREP` leképezéseiből (gépi kinyerés, kézi átnézés). TS-tesztek zöldek.

**4. Számítás (lapmodell)**
- F218.7 — szakaszmodell, Döntési út és melléklet, előfordulások.
- F218.8 — szótári pontok (gerinc, BDB/Thayer-kártya, Nave, 4.13/4.14).
- F218.9 — LXX, kereszthivatkozás, kapcsolatok, Minősítés.
- F218.10 — Hatástörténet (benne a `szopar_motivum`), Kolofon.
- F218.11 — a modell-kapuk (GK-04, GK-09); GK-11.

**5. Megjelenítés**
- F218.12 — sablontábla és md-renderelő (TUDOMANYOS, KIZARASOK); GK-08, GK-10.
- F218.13 — TORZSCIKK a modellből (GK-20).
- F218.14 — alakosztály- és pozitív szerkezeti kapu; a mutációs próba zöld (GK-24–26).
- F218.15 — az olvasó szerver blokkjai a `szamitas/`-ból (OLV-1–3, GK-22); a szerver tesztjei `teszt_futtat.py`-vel.

**6. Regresszió**
- F218.16 — a két lap generálása, a diff vödrözése, az eltérés-engedély sorai okkal. ⛔ **A felhasználó** megnyitja a két renderelt lapot (a szerveren is) és a diff-összefoglalót; jóváhagyás nélkül nincs átállás.
- F218.17 — független ellenőrzés (`fuggetlen-ellenor`), legfeljebb egy javítókör. Ha a felhasználó kéri: a generátor-PR átnézése legfeljebb 6 ügynökkel (Fable 1.2), a heti keret 60%-a alatt.

**7. Átállás (a #217 után, a végén)**
- F218.18 — a lapszövegre kereső kapuk átírása a modellre (`olvasoi_kapu.py`, `ellenoriz.py` 25., 26., 32., 35–40., 43. szabály; E38, E39), egy commitban a fogyasztóikkal.
- F218.19 — a jegyzék G01–G03 `parancs` mezője az új generátorra; az `e28_migralt_nezetek.tsv` utódját a #217 adja; a `feladatok.yml` nem változik (a #217 Actionje a jegyzéket olvassa).
- F218.20 — a régi generátor és a csak általa használt modulok `archivum/lexikon_general/` alá, `ARCHÍV` fejléccel; minden hivatkozás frissítése ugyanabban a commitban (FELADATOK, NYITOTT, briefek `olvas` mezője; E27).
- F218.21 — zárás: jelentés, a `kovetkezo`: „Te: ISTENTISZT-001 2. kiadás (/kiadas)”.

## 10. Technikai döntések (O1–O8, a brief írója döntötte el)

- **O1 — nincs új ellenőrző kör.** A spec 4.b pontja téves (Fable 0.): a tételek cáfolón átmentek. A 357 tétel súlyossági leltára elkészült; a 24 magas tételt saját grep és kódolvasás ellenőrizte. A közepes tételek a 7. pont követelményeiben és a tesztekben ellenőrződnek, nem külön körben.
- **O2 — a #217 jegyzékformátuma.** `adat/generalt_nezetek.tsv`, B- és G-sorok egy táblában; az új generátor csak a G01–G03 `parancs` mezőt cseréli, és a B-sorok `hozzaferesi_pont` oszlopát teszi végrehajtottá. Második jegyzék nem készül.
- **O3 — a 4.11 egysoros mutató marad** a 9. szakaszra (Hatástörténet), a szakaszmodellből generált horgonnyal. Ok: a 4.12–4.14 számozása így nem változik (a kiadott HAMART-lap hivatkozásai és a regressziós diff nem mozdul), a mutató egy sor.
- **O4 — a `fordit.py`/`emeles.py` egész-szócikkes útja archívumba megy** az átállással (F218.20), mert a Thayer a `thayer_bemenet`-ből jön (GK-N178), és más fogyasztója a lapon nincs; ha a nyílt mag vagy más eszköz hívja, az 1. alapmérés kimutatja, és akkor marad.
- **O5 — a szerver a `szamitas/` csomagot importálja**, nem generált lapmodell-JSON-t olvas. Ok: a JSON újabb pillanatkép lenne (M-NYERS), frissességi kapuval; az import egy számítás. A `bdb_szelet._lapit` és a `nyilt_mag_export.csoport_tagjai` a `szamitas/`-ba költözik (a körkörös függés megszűnik).
- **O6 — a lapszöveg-kapuk átírása az átállás commitjában** (F218.18), nem előbb: addig a régi generátor kimenetét védik. Az új generátor a saját kapuit a modellen futtatja; a két kapukészlet az átállásig párhuzamosan él, közös fájlt az ág csak a 7. fázisban ír.
- **O7 — a `TBESH_konszolidalt` (B11) kivezetve.** A `--helyi-lexicon` kapcsoló alapértéke ma is hamis; az új generátor nem olvassa.
- **O8 — a holt kód nem portolandó, külön mérés nélkül.** A regressziós diff (8. pont) kimutatja, ha valami mégis élt.

**Becslés.** A régi generátor kb. 10 000 sora és 20 modulja helyett kb. 4–6 ezer sor + tesztek. Modell: fable, egy író session; a tételek mérete miatt a session a 4. fázis után új sessionben folytatható a jelentés „Folytatási pont”-jából (memória: cikk-session kontextus). Keret: a 6. fázis átnézése ügynökökkel csak 60% alatti heti kerettel.

## 11. Elfogadási feltételek

1. A 7. pont minden tesztje zöld; a mutációs próba minden hibaváltozatát megfogja egy kapu.
2. A regressziós összevető (8. pont) 0 engedély nélküli diff-sort ad mindkét lapon; a számok szintje egyezik.
3. A `lapgen/` kódjában 0 motívumazonosító, 0 `adat/`/`konkordancia/` útvonal a `bemenet/`-en kívül, 0 csere renderelt szövegen.
4. A szerver és a lap számai és kiejtése egyezik (GK-22, OLV-1).
5. A felhasználó a két renderelt lapot megnyitotta és jóváhagyta (F218.16 ⛔).
6. A független ellenőrzés `TISZTA`, vagy az egy javítókör után az.

## 12. Döntésnapló

*A T1 és a T2 eldőlt (a felhasználó, 2026-11-13): az ISTENTISZT-001 az új generátorral jön ki; egy lapszerkezet marad; a befagyasztott lapok nem generálódnak csendben. A T3–T9 válaszai a döntési oldalról (https://claude.ai/artifact/7bH2eSKPfcrasLA9aSBqB2, `dontesek` gyűjtemény, kiolvasva 2026-11-13); a T5 és a T6 szövegét az orkesztrátor is továbbította, a két forrás szó szerint egyezik. A /befogad ezekből `DT-F218a`–`g` sorokat ír a `dontesek/uj/<ágnév>.md`-be.*

| T | Kérdés | Válasz | Forrás |
|---|---|---|---|
| T3 | A Jel 22:3 saját szava (G2652) adatba kerül-e, és kapjon-e szócikket? | **Adatba kerül, szócikk nélkül**: külön „a vers saját szava” mező az előfordulás-táblában; a `TEMATIKUS_SAJAT_SZO` megszűnik; a 4. szakasz nem kap róla szócikket | a felhasználó, döntési oldal, 2026-11-13 (gomb: „Adatba kerül, szócikk nélkül”) |
| T4 | Ha egy szó kétszer áll egy versben, melyik alak kiejtése álljon? | **Az első előfordulás** a vers szövegrendje szerint; a változó sorok listája a regressziós engedélyfájlba kerül | a felhasználó, döntési oldal, 2026-11-13 (gomb: „Az első előfordulás”) |
| T5 | Elavult magyar fordítás helyett mi álljon? | **Munka közben a régi magyar szöveg áll, jelölve; kiadni elavult fordítással nem lehet (kapu); az érintett sorokat a cikk menete újrafordíttatja.** A megjegyzés az irányadó, nem a gomb (a gomb az 1. lehetőségen állt) | a felhasználó, döntési oldal, 2026-11-13, szó szerint: „Kiadás előtt újra kell fordítani. Kapu tiltja, hogy egy lap elavult fordítással kiadásra kerüljön. Az érintett sorokat a cikk menete újrafordíttatja, ahogy korábban döntöttél: az új cikk hiányzó fordításai az előfizetésből készülnek. Munka közben a piszkozatban a 2. változat áll” |
| T6 | Kell-e bizonyossági küszöb a Károli–Strong párosításra? | **Nem kell.** Minden párosítás használható; a mért pontosság egyszer, a Módszertanban áll; páronkénti bizonytalan-jelölés nincs; a címke belső | a felhasználó, döntési oldal, 2026-11-13, szó szerint: „Minden párosítás használható; a mért pontosság (95%, F172) egyszer, a módszertanban áll; páronkénti bizonytalan-jelölés nincs; az alacsony/magas címke belső, nem jelenik meg.” Előzmény a chatben: „ez igy nagyon bizonytalannak hat az olvasónak / miközben a mérésünk jók” |
| T7 | A forrás-állapotot leíró mondatok szövege marad-e? | **Adattáblából, az állapot szerint** (`adat/forras_allapot.tsv`, B67); a mai mondatok a kiinduló értékek, a táblát a felhasználó hagyja jóvá | a felhasználó, döntési oldal, 2026-11-13 (gomb: „Adattáblából, az állapot szerint”) |
| T8 | A szerző neve, a lexikon címe, a webcím és a DOI-k hova kerülnek? | **A mostani értékek mennek át** a `lapgen_konfig.tsv`-be, változatlanul | a felhasználó, döntési oldal, 2026-11-13 (gomb: „A mostani értékek mennek át”) |
| T9 | Mit mondjon a Kolofon, ha a szerző a lap egy korábbi változatát hagyta jóvá? | **Kiadott lap csak friss jóváhagyással**: munka közben „a szerző a lap korábbi változatát hagyta jóvá (dátum)”; a kiadási kapu a `lap_commit` egyezését követeli | a felhasználó, döntési oldal, 2026-11-13 (gomb: „Kiadott lap csak friss jóváhagyással”) |

**A T6 indoklása (javítva).** A `parok_<könyv>.tsv` `bizonyossag` mezője nem mért bizonytalanság, hanem a párosítás módjának címkéje: a „magas” az 1–2Móz, ahol két modell egyezett; az „alacsony” a többi könyv, egy modellel. A mérés (`naplok/KAROLI_PONTOSSAG_jelentes.md`, F172) szerint az összes pár 95,06%-ban helyes (93,81–96,32; 1 600 pár, 8 réteg), a külső összevetésben a fő-szó párok 98,72%-ban (98,22–99,08; n = 2 663), rétegenként 92–99%. A korábbi javaslatom („csak a magas párosítás”) a címkét tévesen pontosságnak olvasta, és a párok 91%-át dobta volna el. *Proveniencia: `scope=naplok/KAROLI_PONTOSSAG_jelentes.md 11., 14., 55. sor | forras=cf68d0a9 | ts=2026-11-13`.*
