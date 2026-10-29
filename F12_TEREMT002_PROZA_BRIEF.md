---
feladat: 12
cim: TEREMT-002 3. lépés (próza, lexikonoldal) — a fordított irány pilotja az arany lap mércéjével (TEREMT002_LEXIKON)
kod: TEREMT002_LEXIKON
tipus: feladat
fazis: 2
munka: ertelmezo
modell: opus
allapot: nem_indult
ad: az első natív egyforrású motívum az új mércével: a jelentes_szam és a karoli_szo az adatban, a szakaszcímke gépileg, a szótári egységek a lap előtt lefordítva, a szótári gerinc kapcsoló nélkül, a motivumok/TEREMT-002.md a 9_ forrássablon szerint, a lexikon/TEREMT-002_TUDOMANYOS.md az ISTENTISZT-001 arany lapjának mércéjén zöld
kovetkezo: "Te: a #148 (védőkorlátok) merge-e után /kovetkezo (a #148 maga a #123 ALVIL-001-es PR-jára vár); első lépés a 0. mérés, utána ⛔ DT-F12a–e"
olvas: [motivumok/TEREMT-002.md, "tematikus_lezart/TEREMT-002*", "tematikus_lezart/naplok/TEREMT-002*", motivumok/ISTENTISZT-001.md, motivumok/TEREMT-001.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, lexikon/TEREMT-001_TUDOMANYOS.md, generalt_proba/TEREMT-002_proza_proba/, naplok/TEREMT002_PROZA_PROBA_meres.md, naplok/TEREMT002_PROZA_PROBA_M0.md, naplok/TEREMT002_PROZA_PROBA_lxx_friss.md, naplok/ELLENOR_TEREMT002_PROZA_PROBA.md, naplok/T1_TEREMT002_scan.md, naplok/T1_TEREMT002_gate.md, naplok/T2_TEREMT002_minosites.tsv, naplok/T2_TEREMT002_kapcsolatok_javaslat.tsv, naplok/ELLENOR_ISTENTISZT001_ARANY_JAVITAS.md, naplok/ELLENOR_ISTENTISZT001_ARANY_JAVITAS_2.md, naplok/F131_SZOTARI_GERINC_naplo.md, TEREMT002_KUTATAS_BRIEF.md, F64_TEREMT002_PROZA_PROBA_BRIEF.md, F131_SZOTARI_GERINC_BRIEF.md, F121_GLOSSZA_FORDITAS_BRIEF.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/7_PaRDeS_tanitoi_kereses_sablon.md, sablonok/PaRDeS_tanitok_lista.md, sablonok/PaRDeS_gyorsreferencia.md, MUNKAMENET.md, RENDER_BRIEF.md, adat/SEMA.md, adat/motivumok.tsv, adat/jeloltek.tsv, adat/kapcsolatok.tsv, adat/auditok.tsv, adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv, adat/bdb_forras_javitas.tsv, adat/glosszak_heber_hu.tsv, adat/terminologia.tsv, adat/tiltott_fordulatok.tsv, adat/szotar_szerepek.tsv, adat/grammatikai_strongok.tsv, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv, konkordancia/Karoli_kereszthivatkozasok.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, eszkozok/general.py, eszkozok/lekerdez.py, eszkozok/glossza_lexikon_forditas.py, eszkozok/forditas_kapuk.py, eszkozok/ellenoriz.py, eszkozok/kuszob.py, eszkozok/gate.py]
ir: [motivumok/TEREMT-002.md, motivumok/naplok/TEREMT-002_tanitoi_kereses.md, lexikon/TEREMT-002_TUDOMANYOS.md, adat/elofordulasok.tsv, adat/lexikon_hivatkozasok.tsv, adat/szotar_szakasz_cimke.tsv, adat/forditasok.tsv, adat/lxx_dontesek.tsv, adat/res_forras.tsv, adat/auditok.tsv, adat/motivumok.tsv, eszkozok/lexikon_general.py, eszkozok/teszt_szotari_gerinc.py, eszkozok/teszt_szerepmatrix.py, eszkozok/ellenorzes/e28_migralt_nezetek.tsv, motivumlog/PaRDeS_motivumok.md, naplok/F12_*, naplok/ELLENOR_F12_*]
fugg: [148]
nem_fugg: [10, 36, 38, 70, 74, 102, 103, 123, 131, 133, 138, 140, 144, 146]
---

# F12_TEREMT002_PROZA_BRIEF.md — TEREMT-002: lexikonlap a fordított irányban

*FELADATOK #12 · a `F12_TEREMT002_PROZA_BRIEF.md` csonkot váltja fel (`/befogad` 2b: csonk kitöltése, ugyanazon a számon; a végleges fájlnév a befogadóé) · Modell: opus · v0 (tervezet) · 2026.10.29 · előzmény: D38, DT-F32a, DT-F26b, DT68, DT187, DT272, DT374, DT401; a #64 mérése (`naplok/TEREMT002_PROZA_PROBA_meres.md`); párja: `F148_UJ_MOTIVUM_VEDOKORLAT_BRIEF.md` (#148)*

**A függésről.** A `fugg: [148]` a kért függés: a #148 adja a gerinc-kivétellistát, a 18–21. szabályt és a levezető eszközt, és maga a #123 ALVIL-001-es PR-jára vár (a `kovetkezo` mezőjében). A `nem_fugg` a levezetett függéseket írja felül. A #38, #74, #102, #103, #131, #133, #138, #140, #144 és #146 tábláit (BDB, TAHOT, glosszák, az ISTENTISZT-001 forrása és lapja mint minta) a feladat csak olvassa, a futáskori main-állapotukban. A #10, #36 és #70 a lexikon-lezárás, illetve a befagyasztott 2/b; a TEREMT-002-t nem érintik. A #123-ra azért nem vár, mert a TEREMT-002 nincs a hét migrálandó motívum között. A 0. lépés ezek helyett a ténylegesen szükséges állapotot méri (a #148 és az ISTENTISZT-001 „teljes” PR-jai a main-en). Mérve: `python eszkozok/feladatok.py ellenoriz` 0 hiba, a `fuggesek`-ben egyetlen függés: #148 (2026-10-29, a két brief ideiglenesen a végleges nevén).

## 1. Cél

A TEREMT-002 (תֹהוּ וָבֹהוּ, *tohu va-vohu*) visszakapja a pilot szerepét (D38). A különbség: ma már nem a B-szerkezet próbája, hanem **a fordított irány első próbája**. Eddig a régi motívumokat hozták az új mércére (#11, #123). Ez az első motívum, amely eleve az ISTENTISZT-001 arany lapjának mércéjével készül (a lapot a felhasználó 2026-10-29-én elfogadta). Ami itt kézi javítókört igényel, az a #13 (1Móz 17-től) új motívumainál a folyamat hibája; a zárónapló ezért külön listázza.

Az új mérce öt eleme:
1. a `jelentes_szam` és a `karoli_szo` az adatban (`adat/elofordulasok.tsv`);
2. a szakaszcímke gépileg a `jelentes_szam`-ból, ⛔ csak eltérésnél (a #148 eszköze);
3. a szótári egységek fordítása **a lap előtt**, a #121 eszközével;
4. a szótári gerinc kapcsoló nélkül fut (a #148 után alapból bekapcsol);
5. ellenőrzés az arany lap mércéje szerint (4. szakasz), a #148 18–21. szabályával együtt.

A D38 / DT-F32a / DT-F26b szerint a #12a (a próza-próba) a #64-ben lefutott, a mostani #12 a #12b: lexikonoldal, LXX-döntések, élesítés, „a #11 után”. A #11 kész (`F11_MIGRACIO_BRIEF.md`). A brief a #12b-t a fordított irány mércéjével bővíti.

## 2. Hatókör

**Benne van:**
- a három előfordulás-sor szótári mezői (`lexikon_szotar`, `lexikon_entry_id`, `jelentes_szam`, `jelentes_en`, `jelentes_hu`); a `karoli_szo` már ki van töltve;
- a `lexikon_hivatkozasok.tsv` és a `szotar_szakasz_cimke.tsv` TEREMT-002-sorai;
- a lap szótári egységeinek fordítása (`adat/forditasok.tsv`);
- a három „függő (#12b)” LXX-hely döntése (`adat/lxx_dontesek.tsv`);
- a `motivumok/TEREMT-002.md` átírása a #64 tematikus szakaszrendjéből a 9_ forrássablon szerkezetébe (RÉS-jelölők), értelmező prózával;
- a 7. lépés (nevesített tanító) a DT-F12d szerint;
- a `res_forras.tsv` sorai; a `lexikon/TEREMT-002_TUDOMANYOS.md` első generálása;
- a DT187-mutató kivezetése a generátorból (`lexikon_general.py`, `_TEREMT002_MUTATO`, a `SZEREP_TOKEN_MUTATO` négy H8414/H0922-sora): a mutató azt mondja, hogy „a TEREMT-002 szótári bekötése a #12b dolga”, és ez a feladat éppen ezt köti be.

**Nincs benne:**
- a TEREMT-001 adata és forrása. Az 1Móz 1:2 közös hely, de a TEREMT-001 a #123 sorában áll; ez a feladat csak olvassa;
- `TORZSCIKK`: az ISTENTISZT-001 mintájára migrált/natív motívum lapjához ma nem készül;
- a `MUNKAMENET.md` (a #125-é);
- a #148 eszközeinek és szabályainak módosítása. Ha a #12 hibát talál bennük, az lelet a #148-nek (N-F12-tétel), nem itteni javítás.

## 3. Kiindulás *(a 0. lépés újraméri; eltérésnél ⛔)*

`scope=adat/elofordulasok.tsv (id=TEREMT-002, n=3) + adat/*.tsv + konkordancia/TAHOT_kivonat.tsv | forras=split('\t')-számlálás (a brief írójának szkriptje) | ts=2026-10-29`

| # | Mérés | Érték (2026-10-29, main `0e607b2f`) |
|---|---|---|
| 3.1 | előfordulás-sorok | 3: 1Móz 1:2 (Peshat), Jer 4:23 (Remez), Ézs 34:11 (Remez); mindhárom `gerinc_elem` = `tohu+bohu`, `strong` = `H8414+H0922` |
| 3.2 | `jelentes_szam` / `lexikon_szotar` / `lexikon_entry_id` / `jelentes_en` / `jelentes_hu` | mind üres (0/3) |
| 3.3 | `karoli_szo` | 3/3: „kietlen és puszta” (×2), „pusztaság … semmiségnek” (Ézs 34:11) |
| 3.4 | BDB-tagolás (`bdb_szakaszok.tsv`) | H8414: `cim`, `fej`, `-/1/-` („formlessness, of primaeval earth …”), `-/2/-` („figurative of what is empty, unreal …”); **H0922: csak `cim` és `fej`, tagolatlan** |
| 3.5 | a BDB saját példahelyei (`bdb_vers_jelentes.tsv`) | H8414: mindhárom vers a `-/1` alatt; H0922: mindhárom vers `tagolatlan` |
| 3.6 | token a versben (TAHOT) | mindhárom versben 1-1 H8414 és 1-1 H0922 token (a versszintű BDB-példa tehát a tokenhez rendelhető, ELLENOR_SZOTARI_GERINC 1. / 7.4a) |
| 3.7 | magyar BDB-szakasz (`bdb_szakasz_hu.tsv`) | H8414 `-/1/-` és `-/2/-` `illeszkedik`; a H0922 `fej` sora megvan |
| 3.8 | `forditasok.tsv` | 2 sor (H8414, H0922, `teljes`, `forditas_hu`); a #64 szerint `allapot=opus`, ugyanaz a modell, amely a prózát írta (#64 5.3) |
| 3.9 | `szotar_szakasz_cimke.tsv` / `lexikon_hivatkozasok.tsv` / `res_forras.tsv` / `lxx_dontesek.tsv` | 0 / 0 / 0 / 0 TEREMT-002- vagy H8414/H0922-sor |
| 3.10 | `jeloltek.tsv` | 68 sor érinti (TEREMT-002 vagy H8414/H0922) |
| 3.11 | `motivumok.tsv` | 1 sor, `statusz` = `feldolgozás alatt`, `v1`, `azonossag_tipusa` = `formulaikus` |
| 3.12 | `motivumok/TEREMT-002.md` | 239 sor, a #64 tematikus szakaszrendjében (Kivonat, 1., 2., 3., 5., 7., Proveniencia-sorok, 3 archív blokk); RÉS-jelölő nincs |
| 3.13 | gerinc | a main-en `SZOTARI_GERINC_MOTIVUMOK = {'ISTENTISZT-001'}` (a #148 után: kivétellista, a TEREMT-002 nincs rajta) |

**A mért állapotból adódó ⛔ pontok (5. szakasz):**
- az összetett sor (H8414+H0922) entry-tokenje → DT-F12a;
- a H0922 tagolatlan → DT-F12a, illetve a #148 DT-F148b-je;
- a BDB-forrás két hibája (a #64 6.1–6.2) → DT-F12b;
- a három függő LXX-hely → DT-F12c;
- a 7. lépés → DT-F12d;
- a `statusz` lezárása → DT-F12e.

A H8414-en eltérés nem várható. A BDB mindhárom verset a `-/1` alatt idézi, a kutatói `1` ugyanoda mutat, tehát a #148 eszköze jelzés nélkül vezet le. Ha mégis jelez, az lelet: ⛔.

## 4. Lépések (⛔ a kötelező megállások)

**0. Modell-ellenőrzés és mérés.** A saját modellnév összevetése a `modell: opus` mezővel; eltérésnél megállás. Utána:
- a #148 a main-en van-e: kivétellista, 18–21. szabály, `eszkozok/szakasz_cimke_levezet.py`. Ha nincs: ⛔;
- az ISTENTISZT-001 „teljes” menetének PR-jai (N-F131a/b, a 12–14. szerep-blokk) a main-en vannak-e. Ha nincsenek, a lap a régi szerepkészlettel készülne: ⛔, a felhasználó dönt, várjon-e;
- a 3. szakasz újramérése (`naplok/F12_meres.py`, `split('\t')`);
- a #148 levezető eszközének próbafutása (`ellenoriz --id TEREMT-002`), még írás nélkül.

Napló: `naplok/F12_TEREMT002_LEXIKON_naplo.md`. **⛔ DT-F12a–e: a felhasználó dönt.**

**1. Adat: a szótári mezők.** A DT-F12a szerint, a három sorra:
- `lexikon_szotar` = BDB, `lexikon_entry_id` = H8414 (javaslat), `jelentes_szam` = `1`;
- `jelentes_en` a BDB `-/1/-` szakaszának szövegéből, szó szerint;
- `jelentes_hu` a `bdb_szakasz_hu.tsv` azonos szakaszából, szó szerint. **A szóról szól, nem a motívumbeli funkcióról** (DT272 (d), N-F131a; a #148 20. szabálya méri).

A `lexikon_hivatkozasok.tsv` sorai: (BDB, H8414, `1`), valamint a H0922 a DT-F12a szerint. Írás előtt a sorok összevetése az eredetivel, eltérésnél megállás (`eszkozok/igazolas_migracio.py` mintája). A proveniencia a lekérdezésé, ha futott, egyébként `manual`. Commit: `F12.1: TEREMT-002 szótári mezői (jelentes_szam, lexikon_entry_id)`.

**2. Szakaszcímke, gépileg.** `python eszkozok/szakasz_cimke_levezet.py ellenoriz --id TEREMT-002`.
- Jelzés nélkül: `--ir` (a `cimke_hu` a #148 DT-F148c-je szerint).
- **Jelzésnél ⛔:** a jelzés típusa és a sor a naplóba kerül, a felhasználó dönt; kitöltés nem gyenge vagy asszociatív anyaggal (CLAUDE.md 3.).

A generátor DT187-mutatójának kivezetése itt történik: `_TEREMT002_MUTATO` és a `SZEREP_TOKEN_MUTATO` négy sora. Utána tesztek (`teszt_szotari_gerinc.py`, `teszt_szerepmatrix.py`). Commit: `F12.2: TEREMT-002 szakaszcímke; a DT187-mutató kivezetése`.

**3. Fordítás a lap előtt.** `python eszkozok/glossza_lexikon_forditas.py lista --id TEREMT-002 --kimenet <repón kívüli könyvtár>`: a lap minden fordítatlan szótári egysége.
- A hiányzókat a #121 eszköze és kapui (`eszkozok/forditas_kapuk.py`) rögzítik az `adat/forditasok.tsv`-be, forrás-hash-sel.
- A fordítási kör a #121 mintájára a `vegrehajto-sonnet` subagentre bízható. A `modell` mezőbe a ténylegesen futott modell neve kerül, a subagent saját kimenetéből.
- A #64 5.3 lelete (a H8414/H0922 `teljes` fordítását ugyanaz a modell írta, mint a prózát) a naplóba kerül, nem írja felül a sort.

**Elfogadás:** a lista `hianyzik` állapota 0, vagy a maradék a lapon `(fordításra vár)` jelölésű (a #148 21. szabályának (iii) pontja). Commit: `F12.3: TEREMT-002 szótári egységeinek fordítása`.

**4. LXX-döntések.** A DT-F12c szerint, a `naplok/TEREMT002_PROZA_PROBA_lxx_friss.md` friss futásából:
- 1Móz 1:2: ἀόρατος καὶ ἀκατασκεύαστος (az ἀκατασκεύαστος Strong-szám nélkül);
- Jer 4:23: οὐθέν;
- Ézs 34:11: σπαρτίον γεωμετρίας ἐρήμου; a *bohu*-köveknek nincs görög megfelelője.

A régi 58 `lxx-hid` audit-sor kivezetett forrásra mutat; a három vers sora friss `lekerdez.py lxx-hid` futással újraírandó (az `auditok.tsv`-be). Commit: `F12.4: TEREMT-002 LXX-döntések`.

**5. 7. lépés (nevesített tanító).** A DT-F12d szerint. Ha fut: `tanito-kereso` subagent (webes lépés, a felhasználó tapasztalata szerint Sonnet), a `sablonok/7_PaRDeS_tanitoi_kereses_sablon.md` és a `sablonok/PaRDeS_tanitok_lista.md` szerint, kimenet: `motivumok/naplok/TEREMT-002_tanitoi_kereses.md`, önálló menet, saját fájl. Ha nem fut: `INAKTÍV` hiányjelzés a forrásban (a #64 L5-mintája). Commit: `F12.5: …`.

**6. Forrás: `motivumok/TEREMT-002.md` a 9_ sablon szerint (értelmező próza, egy kézben).**
- A #64 prózája a sablon 4. pontjának szakaszrendjébe kerül, `<!-- RÉS-KEZDET: [rés] --> … <!-- RÉS-VÉGE -->` jelölőkkel (a `motivumok/ISTENTISZT-001.md` mintája).
- A `res_forras.tsv` kilenc sora a TEREMT-002-re.
- Az `eszkozok/ellenorzes/e28_migralt_nezetek.tsv` sora.
- A három archív blokk sorsa a #11 döntése szerint (archív, nem törlés).

A #64 5. szakaszának három értelmezői döntése (Vitatott pontok aktív és kiegyensúlyozott; a 4. pont inaktív; a BDB-fordítás nem független) és a felhasználó (a) döntése (2026-10-08) érvényes; ezeket nem nyitja újra. Az L4-elhatárolás a TEREMT-001-gyel az 1Móz 1:2-n explicit marad. A TEREMT-001 sora csak olvasva.

Aki a prózába belenyúl, az egészet olvassa (KONTEXTUS K1). Commit: `F12.6: motivumok/TEREMT-002.md a 9_ forrássablon szerint`.

**7. Generálás.**
- Először repón kívüli ideiglenes könyvtárba: `python eszkozok/general.py --cel lexikon --id TEREMT-002 --kimenet <ideiglenes>`, majd a `naplo` és a `nyitott` cél `--ellenoriz` fixponttal.
- A próbalap mérése a 8. lépés szerint.
- **⛔ az éles `lexikon/TEREMT-002_TUDOMANYOS.md` első írása előtt:** a felhasználó a próbalapot látja (a #76/#131 mintájára olvasható nézetben is, ha kéri).

Commit (a jóváhagyás után): `F12.7: lexikon/TEREMT-002_TUDOMANYOS.md generálva`.

**8. Ellenőrzés az arany lap mércéje szerint.**
- (a) **Gépi:** `python eszkozok/ellenoriz.py`: SÉRTÉS 0, ezen belül a #148 18–21. szabálya a TEREMT-002-n (gerinc-címke, `jelentes_szam`/`karoli_szo`, `jelentes_hu`, lap-tisztaság: nincs helyőrző, „a(z)”, jelöletlen fordítatlan egység, nem létező DT/N). Továbbá a `kuszob.py` és a `gate.py` (TEREMT-001-ütközés: jelentés).
- (b) **Sablon-kapu:** a lexikonoldal-sablon L1–L7-je és a DT2 két rés-szabálya (DT68 (2)); a forrásra a 9_ sablon 8. pontja szerint.
- (c) **Arany-összevetés, blokkonként és vizuálisan:** a TEREMT-002 lapja az ISTENTISZT-001 lapja mellett. Minden blokk, amely ott megvan (szótári gerinc, a „Jelentés (a szó)” / „Funkció (a motívumban)” oszlopok, ⓘ-lábjegyzetek, LXX-sor, kolofon, 12–14. szerep), itt is megvan, vagy explicit hiányjelölésű.
- (d) **A fordított irány mérése:** a zárónapló külön táblája minden olyan pontot listáz, ahol kézi javítás kellett. Ezek a #13 folyamatának hibái, a #148/#125-nek szóló N-F12-tételként.

Független ellenőr (`fuggetlen-ellenor`), jelentés: `naplok/ELLENOR_F12_*.md`.

**9. Zárás.** Draft PR, a brief fejléce, a zárónapló.
- **⛔ DT-F12e** (a `motivumok.tsv` `statusz`-a).
- **⛔ a merge a felhasználóé.**

## 5. Elfogadási feltételek

1. A három előfordulás-sor `jelentes_szam`-a, `lexikon_entry_id`-je, `jelentes_en`-je és `jelentes_hu`-ja ki van töltve vagy a DT-F12a szerint explicit; a `jelentes_hu` nem hordoz funkció-értelmezést.
2. A gerinc-Strongok minden szakaszának van sora a `szotar_szakasz_cimke.tsv`-ben, és a sorok a #148 eszközéből jöttek (proveniencia); kézi címke csak ⛔-döntés után.
3. A lapon nincs jelöletlen fordítatlan szótári egység.
4. A lapon a szótári gerinc megjelenik, kapcsolóbejegyzés nélkül (a TEREMT-002 nincs a kivétellistán, és nem került rá).
5. `ellenoriz.py`: SÉRTÉS 0. A tesztek zöldek. `feladatok.py ellenoriz`: 0 hiba.
6. Az L1–L7 és a DT2 két rés-szabálya a lapon és a forráson teljesül (8. b).
7. Az arany-összevetés (8. c) táblája kitöltött, hiánynál explicit jelöléssel.
8. A zárónapló „fordított irány” táblája (8. d) megvan, akkor is, ha üres; az üres eredményt kimondja.
9. A TEREMT-001 fájljai és sorai változatlanok. Nincs `csv` modul. Minden lekérdezésből származó állítás mellett proveniencia-sor áll.

## 6. Döntésnapló

**DT-F12a — az összetett sor entry-tokenje és a H0922.** Kérdés: a `H8414+H0922` soron melyik token a `lexikon_entry_id`, és mi a tagolatlan H0922 sorsa?
- (1) **entry = H8414, `jelentes_szam` = `1`**; a H0922 a gerincen a BDB saját példahelyeként jelenik meg (`fej`, tagolatlan), kutatói hozzárendelés nélkül; a `lexikon_hivatkozasok.tsv`-be a H0922 a #148 DT-F148b szerinti értékkel kerül;
- (2) entry = H0922: a `jelentes_szam` a DT-F148b explicit értéke, a H8414 csak példahelyként;
- (3) a sor két sorra bomlik (H8414, H0922), mindkettő saját `jelentes_szam`-mal. Ez a `gerinc_elem` = `tohu+bohu` páralakjával (SEMA 2.2, a T2 G5-döntése) ütközik.

*Javaslat: (1).* A H8414 tagolt; a BDB maga mindhárom verset a `-/1` alatt idézi, és a H0922 szócikke szerint a *bohu* „mindig a תֹּהוּ szóval” áll. A (3) a formulaikus azonosságot (`azonossag_tipusa` = `formulaikus`) bontaná szét.

**DT-F12b — a BDB-forrás két hibája (a #64 6.1–6.2).** A H8414/H0922 héber idézetei sérültek (fordított szórend, hibás maqqef: pl. `קַותֿֿהֹוּ`); a H8414 szócikk „49:19”-et ír, a *tohu*-vers az Ézs 49:4. A gerinc a szakaszszöveget mutatja, ezért a hiba a lapra kerülne.
- (1) kézi sor a `bdb_forras_javitas.tsv`-ben (a DT381 (a) mintája, `manual`, indokkal), az ⓘ a javítás forrását nevezi meg;
- (2) a hiba a lapon marad, NAPLO-jelöléssel;
- (3) külön feladat a BDB-forrás héber idézeteire.

*Javaslat: (1) a „49:19”-re, (3) a héber idézetekre*, mert az utóbbi nem TEREMT-002-specifikus (a #64 6.1 a `forditasok.tsv`-ben is továbbviszi). Ha az (1) mellett dönt a felhasználó, az `ir` kiegészül az `adat/bdb_forras_javitas.tsv`-vel; a befogadáskor ez eldönthető.

**DT-F12c — a három függő LXX-hely.** A javasolt `lxx_dontesek.tsv`-sorokat a 4. lépés munkalapja adja.
- (1) mindhárom vers döntése most, a friss futásból; az ἀκατασκεύαστος Strong-szám nélküli állapota explicit;
- (2) csak az 1Móz 1:2 és a Jer 4:23; az Ézs 34:11 (a *bohu*-köveknek nincs görög megfelelője) nyitott tétel.

*Javaslat: (1)*, a hiány explicit jelölésével (CLAUDE.md 3.).

**DT-F12d — a 7. lépés.** A #64-ben nem futott (L5: `INAKTÍV` hiányjelzés).
- (1) most fut, `tanito-kereso` subagenttel, saját fájlba;
- (2) inaktív marad, a hiány explicit; később önálló menet.

*Javaslat: (1).* Az arany lapnak van nevesített tanítói szakasza (#130); a fordított irány próbája csak teljes lappal mér.

**DT-F12e — a `motivumok.tsv` `statusz`-a a zárás után.** Ma `feldolgozás alatt` (T2 G2).
- (1) a lezárt motívumok értéke a 9_ sablon / #11 szerint;
- (2) marad, amíg a #13 első új motívuma meg nem erősíti a folyamatot.

*Javaslat: (1)*, mert a lap az arany mércén zöld.

| Verzió | Dátum | Változás |
|---|---|---|
| v0 | 2026.10.29 | Tervezet a felhasználó 2026-10-29-i kérésére („ez a teljes feladatsort orkesztráld le”; a TEREMT-002 visszakapja a pilot szerepét, D38; az új motívumok az arany lap mércéjével készüljenek), az orkesztrátor megbízásából; a `F12_TEREMT002_PROZA_BRIEF.md` csonkot váltja fel; befogadásra vár. |
