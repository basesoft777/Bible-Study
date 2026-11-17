# F197 — harmadik tanú a BDB jelentésponthoz (Sefaria BDB): jelentés

*Proveniencia: scope=seed-103 (200 pont, 183 szócikk) + a 183 szócikk minden 2.29-sora (38 735 tanú-sor) | forras=Sefaria /api/words
(210 kérés, 2026-11-11; nyers válaszok: `D:\pardes_tanu\bdb\api`, napló: `D:\pardes_tanu\bdb\lekeresek.tsv`) + adat/bdb_vers_jelentes.tsv
(F185 utáni állapot) + naplok/BDB_SZELETELO_M2_minta_seed103_kulcs.tsv + `…seed103_kitoltott_A.tsv` (arany: A = B; s103-N182: B) |
kód: eszkozok/olvaso_szerver/bdb_sefaria_tanu.py `meres` | modell: claude-opus-5-5 | ts=2026-11-11.*

## 1. Licenc és letöltés

- **A forrás:** a Sefaria `/api/words` „BDB Dictionary” / „BDB Aramaic Dictionary” bejegyzései (Brown–Driver–Briggs, Oxford 1906). A
  BrownDriverBriggs.jl (GPL-3.0) csak burkoló ugyanehhez az API-hoz, saját adat nélkül; **nem használjuk**, kód nem került át.
- **A licenc:** a Sefaria lexikon-adatán nincs licencmező; a mű 1906-os, közkincs. A repó ezt már eldöntötte: **DT631** (a felhasználó,
  2026-11-08): „a tartalom közkincs, és a szerzői jog szerint senki nem korlátozhatja”; „a BDB-nél, ahol nincs licencmező, a
  közkincs-állítás az 1906-os kiadáson alapul; a letöltés útja (Sefaria-Export / API) az ÁSZF szerint megengedett”. Ugyanezt az API-t a
  DT-F185c már külső tanúként használja. A szó szerinti ÁSZF-idézet: `adat/licencek.tsv` (`BDB_rokon_irasok` sor) és `D:\pardes_tanu\bdb\LICENC.txt`.
  **Nem kétes, nem álltam meg.**
- **A repóba Sefaria-szöveg nem kerül:** csak a vers → normalizált jelentéspont (`homonima|rész|törzs/szám/betű`), a BDB 1906-os tagolása.
- **Letöltés:** 183 Strong, 210 kérés (≥ 1,1 s szünet, User-Agent `PaRDeS-research/1.0`, e-mail nélkül); 9 Strongra nincs BDB-bejegyzés.

## 2. ⛔ A 40 soros téves-riasztási próba

A minta: a seed-103 mind a 19 `ketes` sora, az egyetlen hibás `biztos` sor és 20 helyes `biztos` sor (`random.Random(195)`); részlet:
`naplok/F197_proba40_reszlet.tsv`.

| | db |
|---|---:|
| helyes pont | 28 |
| — a tanú egyezik | 21 |
| — **a tanú eltér (téves riasztás)** | **0** |
| — nincs adat (a Sefaria a verset nem linkeli) | 7 |
| hibás pont | 12 |
| — **a tanú eltér (megfogva)** | **7** |
| — a tanú egyezik | 5 |

**Ítélet a végleges (v3) szabállyal: a próba jó** (0 téves riasztás, 7/12 megfogott hiba). **De ez nem független kapu** (ELLENOR_F197, 1. eltérés), l. lent.

**Fontos, nyíltan:** a szabályt a mintán javítottam, a mérés ezért **mintán belüli**. Három változat volt:
- **v1** (homonima-összevetéssel): az első, még részleges adatú futáson a helyes `biztos` sorok közül sok homonima-eltérést jelzett. Ok: a
  Sefaria felső indexe (²) a Sefaria saját sorszáma az azonos alakú címszavakra, nem a BDB római száma. Például a H2022 הַר a BDB-ben
  számozatlan, a Sefariában „²”; a felmérés 3. korlátja ezt előre jelezte. **v2:** a homonimát nem vetjük össze.
- **v3:** a 2.29 kifejezetten törzs nélküli számozott pontja (`-/2`) és a Sefaria-törzs (`Pi./2`) eltérés. Ez a szám-szabály
  („a hiány is eltérés”) párja. A mintán egyetlen sort érint (s103-N061), és azt megfogja.
- A törzsnév-kulcs az átírás ékezetei nélkül (Unicode NFD): „Pōʿlēl” ~ „Pol'el”. Ez a mintán nem változtat.
- Javítókör (ELLENOR_F197): a nem törzs jellegű `form` (pl. H0996 „With other prepositions:—”) nem törzs; több Sefaria-bejegyzésben
  álló versnél nincs bejegyzéseken átnyúló k-adik illesztés (`barmely`). A mintán egyik sem változtat.

**A ⛔ kapu menete, nyíltan.** A v1 hibáját egy még részleges adatú hibakereső futáson láttam, a formális 40 soros próba előtt; a szabályt
akkor javítottam, és a próbát a javított szabállyal futtattam. A ⛔ szándéka szerint a v1 zajánál meg kellett volna állnom, és a döntést
átadnom. A v1 a végleges adaton (utólag mérve: a `bdb_sefaria_tanu.meres` a v1 `pont_egyezik`-kel, scratch-szkript, a repóba nem került):

| szabály | 40 soros próba: téves riasztás / helyes | megfogva / 12 | 200 pont: téves riasztás / 188 | ebből `biztos` / 180 | megfogva / 12 |
|---|---:|---:|---:|---:|---:|
| v1 (homonimával) | 4 / 28 | 8 | 28 | 26 | 8 |
| **v3 (végleges)** | **0 / 28** | **7** | **1** | **1** | **7** |

A v1 a 40 soron még több hasznot adott, mint zajt (8 : 4); a 200 ponton már nem (8 : 28). A v2 és a v3 elvi javítás, nem egyes sorokra
szabott, de a „0 téves riasztás” **mintán belüli** érték: a felhasználó döntése (DT776, 🟢, 2026-11-11): a tanú kikapcsolva kerül be, és csak egy független, kb. 40 soros kézi szúrópróba után kapcsolható be (N-F197a); a mintán kívüli
mérés a következő vak minta (N-F197b).

## 3. A seed-103 200 pontjának újramérése

Részlet: `naplok/F197_seed103_reszlet.tsv`.

| | db |
|---|---:|
| a tanú: egyezik / eltér / nincs adat | 171 / 8 / 21 |
| helyes pont (188): téves riasztás | **1** (s103-N087 H1692 Jób 38:38 `Pu'al/1`: a Sefaria-fában a Pu`al alatt nincs „1.”) |
| hibás pont (12): **megfogva** | **7** — s103-N013, s103-N040, s103-N058, s103-N061, s103-N071, s103-N105, s103-N124 |
| hibás pont: nem fogva | 5 — s103-N028, s103-N076, s103-N094, s103-N122 (homonima-szám: a tanú nem látja); s103-N004 (a Sefaria is Qal-t ad, az arany Hiph`il) |

**Mit ad ez hozzá a mostani `bizonyossag`-hoz?** A 12 hibából 11 már most is `ketes` volt. Az új jelzés a `biztos` sorokon:

| bekötött szabály: csak az eltérés jelöl (egyezésnél a bizonyosság marad) | `biztos` sor | ebből hibás | `ketes` sor | ebből hibás |
|---|---:|---:|---:|---:|
| ma (F185) | 181 | 1 | 19 | 11 |
| **a tanúval** | **179** | **0** | 21 | 12 |
| elvetett változat: az egyezés is emel (`ketes` → `biztos`) | 189 | 5 | 11 | 7 |

Az egyetlen hibás `biztos` sort (s103-N013, `fej` ↔ `-/1`) a tanú megfogja, egy helyes sort (s103-N087) tévesen jelöl.

**Az egyezés nem emel** (DT776). A feladat szerint: „egyezésnél a pont `biztos` marad”. A mérés szerint az emelés 5 hibás pontot vinne
a `biztos` sorok közé: a homonima-hibákat a tanú nem látja, és az s103-N004-ben a Sefaria ugyanazt a téves törzset adja.

## 4. Mintán kívül: a zaj a teljes szócikkeken (arany nélkül)

A 183 szócikk minden nem szűrt ószövetségi 2.29-során (a bekapcsolt generátor memóriában, írás nélkül):

- **`biztos` → `ketes:jp_tanu_sefaria`: 635 / 33 490 sor (1,9%)**; más mező nem változik.
- A `ketes` sorok 34,5%-ánál a tanú is eltér (1 809 / 5 245).
- A 635 eltérés szintje: betű 274, szám 287 (a táblában üres 142, a Sefariában üres 101, más szám 44), törzs 74; illesztés: pontos 560,
  bármely 75. Csoportokban állnak: H3117 144, H3847 67, H5704 42, H1961 41, H1980 40, H7311 38.
- **Kézi szúrópróba (a forrásszöveg, `BDB_teljes_unabridged.tsv`):** H8081 Ez 23:41: a forrás „… k. offered to idols Isa 57:9; Ezek
  16:18-19, 23:41” — a tábla (`-/2/k`) helyes, a Sefaria (`j`) téved. H3847 3Móz 6:4: a forrás „1. a. literally put on …” — a tábla
  (`Qal/1/a`) helyes, a Sefaria-fából a „1.” hiányzik. A `biztos` sorokon mért 0,6%-os hibaarány (F185) mellett **a 635 jelzés nagy része
  várhatóan a Sefaria saját feldolgozási hibája**; a pontos arányt nem mértem (N-F197a).

## 5. Bekötés (kapcsolóval, alapból KIKAPCSOLVA)

- `eszkozok/olvaso_szerver/bdb_vers_jelentes.py`: `SEFARIA_TANU = False`; `--sefaria-tanu` egy futásra bekapcsolja. Bekapcsolva: a
  tanútól eltérő sor `ketes:jp_tanu_sefaria` (ha más ok nem áll előtte), egyezésnél és nem linkelt versnél változatlan, a `jp_kezi` sort nem
  érinti; a fejléc `# forras` sora ilyenkor a tanú-tábla hash-ét is hordozza.
- Kikapcsolva a 2.29 adatsorai **bájtra azonosak**, csak a `# forras` fejlécsor kód-hash-e változott (a `bdb_sefaria_tanu.py` bekerült a
  `KOD_FAJLOK`-ba). `--ts 2026-11-10 --ellenoriz`: bájtra azonos. A lexikonlapot nem generáltam újra; a HAMART-lap nem változik.
- `adat/bdb_jp_sefaria.tsv` (SEMA 2.29.1): 38 735 sor, csak a 183 lekérdezett Strong. A teljes BDB letöltése (≈ 8–9 ezer Strong, becslés
  3–4 óra) a bekapcsolás előfeltétele (N-F197a).

## 6. Nyitott

- N-F197a: a bekapcsolás külön lépés; előtte a teljes letöltés és a `biztos` → `ketes` jelzések kézi szúrópróbája (a téves riasztás mintán kívüli aránya).
- N-F197b: a mintán belüli szabály (v2, v3) mintán kívüli mérése a következő vak mintán.

## 7. N-F197a: a független, mintán kívüli kézi szúrópróba (DT776; 2026-11-16)

*Proveniencia: scope=a teljes Sefaria-tanú-tábla (8028 Strong; adat/bdb_vers_jelentes.tsv `biztos` sorai) | forras=Sefaria /api/words (a nyers válaszok és a teljes tábla a repón kívül: `D:\pardes_tanu\bdb\api`, `…\bdb_jp_sefaria_teljes.tsv`), `eszkozok/olvaso_szerver/bdb_sefaria_proba.py` (seed 20261116), a vak bírálat: Fable-ügynök, 40 lap, forrásnév nélkül | modell: claude-sonnet-5-5 (végrehajtó), Fable (bíráló) | ts=2026-11-16. A tanút **nem kapcsoltam be** (`SEFARIA_TANU = False`); a bekapcsolás a felhasználó döntése.*

**Letöltés.** 8028 Strong, 14:32–20:31 (≈ 6 óra, nem 3–4; 8112 kérés). 111 kérés kapott 502/503/504 hibát (a hiba nem kerül a gyorsítótárba); a futás újraindításra 79 kérést ismételt, mind sikerült. 2083 Stronghoz nincs Sefaria-BDB-szócikk (a lekérdezett 8028 negyede; a 183-as próbában 9 volt, mert az gyakori szavakból állt). A teljes tábla: 161 244 sor, a repón kívül (`tabla --ki`); az `adat/bdb_jp_sefaria.tsv` a 183 szócikkes marad.

**A váltások halmaza a teljes táblán:** 145 951 vizsgált `biztos` sorból **3040 váltana `ketes:jp_tanu_sefaria`-ra, 540 szócikken** (2,1%; a régi 635 / 183 szócikk volt; a 183 szócikken most 634, az adat azóta kissé változott). A bekapcsolt generátor memóriában ugyanezt a számot adja. Illesztés: pontos 2731, „bármely” 309. Szint: szám 1671 (+28 szám+betű), betű 569, törzs 656 (+116 kevert). A legtöbb váltású szócikk: H3117 144, H0559 134, H0413 126, H0310 117, H3847 67.

**Minta.** 40 sor, szócikkenként egy, rögzített seeddel a 399 mintázható szócikkből; kizárva: a seed-103 mind a 200 sora (a 40 soros próba ennek része), a két kézi próba (H8081 Ez 23:41, H3847 3Móz 6:4), és a „bármely” illesztésű sorok (309 = a váltások 10%-a; a Sefaria-oldal ott több pontból áll, ezeket a próba nem méri). A szócikkenkénti rétegezés miatt a gyakran váltó szócikkek (H3117 stb.) alulreprezentáltak; a szócikk-súlyozott becslés alább.

**Bírálat.** A lap: a BDB-szócikk szövege (a szócikk eleje + a hivatkozás ±7000/1200 karakteres környéke, a hivatkozás ⟦►…◄⟧ jelölve), a vers héber szövege, és két jelölt pont (A, B) véletlen sorrendben, azonos alakban (törzs/szám/betű; a törzsnév egységes alakra hozva). A bíráló Fable-ügynök a két jelöltről nem tudta, melyik forrás melyik; kategóriák: csak A / csak B / mindkettő / egyik sem / eldönthetetlen. Eredmény soronként: `naplok/F197_proba_kulcs.tsv`.

| a bírálat szerint | db |
|---|---:|
| csak a **tábla** helyes (a váltás téves riasztás) | 11 |
| csak a **Sefaria** helyes (a váltás jogos) | 24 |
| mindkettő helyes | 1 |
| egyik sem helyes | 4 |
| eldönthetetlen | 0 |

| | téved | arány (40) | 95%-os Clopper–Pearson CI |
|---|---:|---:|---|
| **a tábla** (a Sefaria helyes, vagy egyik sem) | 28 | **70,0%** | [53,5%; 83,4%] |
| **a Sefaria** (a tábla helyes, vagy egyik sem) | 15 | **37,5%** | [22,7%; 54,2%] |

Páros összevetés: a csak-Sefaria 24 : csak-tábla 11 (a 35 egyoldalú sorból), egzakt kétoldalú próba (McNemar) p = 0,041. A váltás alapján **téves riasztás** (a tábla helyes vagy mindkettő helyes): 12 / 40 = 30,0% [16,6%; 46,5%]. Szócikk-súlyozott becslés (a szócikk mintázható soraival súlyozva): a tábla téved 43,5%, a Sefaria 23,5% (a súlyok néhány nagy szócikkre, H0310 117, H0214 29, koncentrálódnak; CI-t nem adok). A „egyik sem” 4 sor mind a szócikk végi megjegyzésekben áll (H2372, H0214, H7200, H2029: „Note.”, szövegkritikai jegyzet, törzsön kívüli utalás); ha ezeken a tábla szomszédos pontját elfogadhatónak tekintjük, a tábla hibája 24/40 = 60%, a Sefaria 15/40 marad.

**DT776 szabálya szerint:** „ha a Sefaria a próbán is többet téved, mint a tábla, a tanú kikapcsolva marad.” A próbán a Sefaria **kevesebbet téved** (15 : 28), a szabály tehát nem tartja kikapcsolva a tanút.

**Hibatípusok** (a 40 sor; a szint a `kulcs` fájl `szint` mezője szerint nézve is):
- *A tábla téved (28):* 8 törzs (a tábla Poal / Qal / Pealal / Pael stb., a hely a Sefaria és a bíráló szerint Hithpael, Piel, Polel, Haphel, Hiphil, Tiphel, Hithpa.: H5953, H5401, H2229, H5487, H3423, H7270, H4223, H5493), 6 sor, ahol a tábla `fej`-et ad, de a hely számozott jelentés alatt áll (H2268, H2023, H5871, H5945, H7764, H6976), 4 sor, ahol a tábla számozott pontot ad, de a hivatkozás a szócikk **fejének alaklistájában** áll („absolute ׳ח Hosea 9:6 8t”, H5035, H2336, H3759, H7626), 4 betű-csúszás (a szomszédos betű: H6119, H0475, H3605, H2603), 2 szám-csúszás (H4672, H4676), 4 „egyik sem” (szócikk végi megjegyzés).
- *A Sefaria téved (15):* 7 szám (a Sefaria számot ad, ahol a hely számozatlan, vagy fordítva: H3818, H1314, H6105, H4196, H6083, H2748, H5648), 3 betű-csúszás (H2388, H7068, H5003), 1 törzs+szám (H8327), a 4 „egyik sem”.
- *Mindkettő helyes (1):* H0310, a Sefaria „Plur” törzsneve a táblabeli számozott ponttal azonos.
- A hibák okát nem vizsgáltam. Annyi látszik, hogy a tábla hibái ismétlődő mintákat követnek (a fej-alaklista és a számozott szakasz határa, a törzsváltás), a Sefaria hibái számozási és betűsorrendi csúszások; az ok a N-F197c feladata.

**Mit mutat ez, és mit nem.**
- A váltásokból a próba szerint ~70% [54%; 83%] valódi táblahiba. Ez nem mond ellent az F185 `biztos` sorokon mért 0,6%-os hibaarányának (1/181, CI kb. 0,0–3,0%): ha a 3040 váltás ~70%-a hiba, az a 145 951 `biztos` sor ~1,5%-a (≈ 2100 sor), ami az F185 CI-jén belül marad. Ugyanakkor a hiba nagyobb, mint az F185 pontbecslése. A tanú tehát a `biztos` halmaz egy valódi hibaosztályát fogja meg, nem csak zajt.
- A bekapcsolás 3040 sor bizonyosságát mozdítaná (`biztos` → `ketes`), 540 szócikken, a lapok bizonyossági jelölését is (gyenge jelölés, `bdb_vj_szabaly.vj_bizonytalan`); a váltások ~30%-a téves riasztás.
- **Korlátok:** 40 sor, egy bíráló, egy menet (nincs második vélemény); a „bármely” illesztésű 309 sor és a gyakran váltó szócikkek alulreprezentáltak; a bírálat részben vak (a lapon a Sefaria törzsnevei egységes alakra hozva, de „Plur”, „Tiph”, „Haph” jelleg a Sefaria forrásjegye lehetett); a P26 lapon a hivatkozás-jelölés néhány karakterrel arrébb áll (a bíráló a szócikk szövegéből is látta a helyet). A bíráló egy modell, nem szaktudós; a 28 „tábla téved” sor emberi (vagy második modelles) felülvizsgálata a bekapcsolás előtt ajánlott (N-F197c).

**Javaslat (a DT776 szabálya szerint):** a Sefaria-tanú a próba alapján nem marad kikapcsolva (a Sefaria kevesebbet téved, mint a tábla: 15 : 28, p = 0,041), a bekapcsolás **indokolható**; a döntés a felhasználóé. A bekapcsolás előtt: (1) az `adat/bdb_jp_sefaria.tsv` cseréje a teljes táblára (161 244 sor; a fájl mérete és a repóba kerülés is döntés); (2) a lexikonlapok bizonyossági jelölésének változása a 3040 sorra; (3) N-F197c (a fejlistás és a törzs-hibaosztály a táblában).

## 8. A bekapcsolás (DT-F197b; 2026-11-17)

*Proveniencia: scope=a 2.29 (adat/bdb_vers_jelentes.tsv) és a teljes tanú-tábla (adat/bdb_jp_sefaria.tsv) | forras=a felhasználó döntése: „legyen így” (az orkesztrátor közvetítésével), a 7. szakasz mérése alapján | kód: eszkozok/olvaso_szerver/bdb_vers_jelentes.py (`SEFARIA_TANU = True`) | modell: claude-sonnet-5-5 | ts=2026-11-17.*

- **Mi változott.** `SEFARIA_TANU = True`; az `adat/bdb_jp_sefaria.tsv` a teljes tábla (161 244 sor, 8027 Strong, 18,5 MB; korábban 38 735 sor, 183 szócikk); az `adat/bdb_vers_jelentes.tsv` újragenerálva `--sefaria-tanu` nélkül, `--ts 2026-11-10`-zel (az azonos `ts` miatt csak a 3040 váltó sor és a `# forras` fejléc változik; a sorok proveniencia-mezője a régi nap marad, a fejlécsor viszi az új tábla hash-ét). `--ts 2026-11-10 --ellenoriz`: bájtra azonos.
- **A váltás:** 3040 sor `biztos` → `ketes:jp_tanu_sefaria`, 540 szócikken; más oszlop nem változik.
- **Licenc és méret** (az orkesztrátor feltételei): a tábla csak normalizált útvonalat tartalmaz (`homonima|rész|törzs/szám/betű`), Sefaria-szöveget nem; a forrás Brown–Driver–Briggs, 1906 (közkincs, DT631; `adat/licencek.tsv` `BDB_rokon_irasok`: a Sefaria lexikon-adatán nincs licencmező). A fájl 18,5 MB, a 20 MB-os küszöb alatt, ezért commitoltam. A nyers letöltés (≈ 17 MB… a gyorsítótár `D:\pardes_tanu\bdb\api`) a repón kívül marad.
- **A mércelapok (előbb mérve, a kapcsoló előtt és után, azonos `PARDES_DATUM=2026-11-13`):** a HAMART-001 lap kimenete **bájtra változatlan** mindkét generátoron: a régi (`--cel lexikon`: `_TUDOMANYOS.md`, `_KIZARASOK.md`) és az új (`--cel lexikon2`: ugyanaz a két fájl) is 0 eltérő sor, sorvég-normalizálva. Az ISTENTISZT-001 nem generálódik újra (`adat/lap_befagyasztas.tsv`: BEFAGYASZTVA), a committolt lapja nem változik. Az olvasó-szerver gyenge jelölése (`bdb_vj_szabaly.vj_bizonytalan`) a 3040 sorra élőben változik; ez nem lapfájl.
- **A mérce hash-őre.** A `naplok/F218_referencia.tsv` B19 sora (`adat/bdb_vers_jelentes.tsv`) az új tartalom hash-ére frissül külön commitban (a brief 8.1 pontja: a lap bájtra egyezik).
- **Tesztek:** `teszt_bdb_sefaria_tanu.py` (a „alapból kikapcsolva” teszt „alapból bekapcsolva”-ra; a kapcsoló és a tábla útvonala), `teszt_bdb_vers_jelentes.py` (az újragenerálás-teszt a kapcsoló állapotával hívja a `kiir`-t).

## 9. N-F197c: a tábla négy ismétlődő hibaosztályának javítása (2026-11-17)

*Proveniencia: scope=a 2.29 (adat/bdb_vers_jelentes.tsv) pont-meghatározása és a 2.30 (adat/bdb_szakaszok.tsv) táblaszövege | forras=a 7. szakasz 28 „tábla téved” sora és a teljes tábla (8027 Strong) mérése a Sefaria-tanúval mint orákulummal | kód: eszkozok/olvaso_szerver/bdb_vers_jelentes.py (`TablaPont`, `torzs_fejek`, `osszegzo_sorok`) | modell: claude-sonnet-5-5 | ts=2026-11-17.*

**Gyökérok.** A 2.30 (`bont.py`) a DictBDB.json félkövér fejeiből és a lexikon fejeiből épül; négy ismétlődő mintán a forrás szerkezetét rosszul adja, és a 2.29 a táblából olvassa a pontot:
1. **Fel nem ismert törzsfej** (a 7. szakasz 8 törzshibájából 5; `Hithpa. Perfect`, `Po. Perfect`, `Haph`el put an end to: Imperfect`, `Tiph`el, Perfect`, `Pô`lel Perfect`): a forrás a törzsnevet nem emeli ki félkövérrel, a 2.30 a rövidítést („a hivatkozásban áll”, F185 N106) és a köztes szavas alakot nem tekinti fejnek; a hely az előző törzs pontján marad.
2. **„= Qal” mint új törzs** (P14 H5401, P25 H3423): a forrás „kiss = </p><p><b>Qal</b>: with …” bekezdésszakadása a visszautalást törzsfejnek mutatja.
3. **A fej összefoglaló sora** (P02 H5035, P08 H2336, P19 H3759, P20 H7626): „1 brier, bramble. 2 hook, ring, fetter; — absolute Hosea 9:6 8t; —”: a számozott mini-glosszákat a 2.30 pontnak veszi, az alaklista hivatkozásai a 2. pont alá esnek; a testben a számozás újraindul.
4. **Az 1. jelentés a fej sorában** (a 7. szakasz „`fej` a tábla szerint, de számozott pont alatt áll a hely” 6 sora): „שׁוּנִי 1. proper name … Num 26:15 … 2. adjective”: az 1. jelentés nem félkövér, a 2.30 nem bontja ki, a hely `fej` marad (a 2.30-ban a számozás 2-vel indul).

**A javítás helye.** A 2.29 `TablaPont`-ja (nem a 2.30 és nem a bont.py): a 2.30 változása a fordítás-táblát (`bdb_szakasz_hu`, soronként kulcsolt) és a lapok BDB-blokkját is mozgatná, a mércelapot (HAMART-001) is. Négy szabály, mindegyik a táblaszövegen: (1) `torzs_fejek` (teljes név, rövidítés, köztes szó, ékezet; mondat-, tagmondat- vagy zárójeles mondatvégi határ után, „i.e. Niph`al” és „(c. Niph`al Imperfect)” nem fej; zárójeles mondat folytatása nem fej), a következő sorok törzse az új törzsre átíródik a következő valódi törzsfejig; (2) „=” után álló törzssor az előző sor pontján marad; (3) `osszegzo_sorok`: legalább két, 1-ről induló egész számozott, igehely nélküli sor (az utolsóban az első „—” után kezdődik az alaklista), utána ugyanott 1-ről újraindul a számozás: a sorok a fejhez (törzs alatt a törzs fejéhez) tartoznak; (4) a fej (vagy alcímszó) sorában álló „1.”/„1” jelentés, ha az első pont a 2: pótolt `-/1/-` fej a sor belsejében.

**Mérés** (a tanú mint orákulum; a mérce nem a bírálat, a 28 sor ítélete külön szempont):
- A 2.29 633 sorának pontja változik (164 szócikk); a `jp_tanu_sefaria` jelzések száma **3040 → 2546** (−494): 479 sor jelzése megszűnik (a pont a Sefariával egyezik), 7 új jelzés, 22 sor `jp_tanu_sefaria` → `jp_tanu_elter` (a szeletelő mint tanú is eltér), 8 sor `biztos` → `ketes:jp_tanu_elter` (a javított pont a szeletelőtől tér el; H0349: a „1. interrogative How?” a fej sorában, a szeletelő `fej`-et ad), 1 sor `jp_tanu_elter` → `biztos`.
- A szabályonkénti hatás (az egyes szabály önmagában, a tanú egyezése a régi → az új pontnál): összefoglaló sor 89 javul, 0 romlik; „=” utáni törzs 20 javul, 0 romlik; fel nem ismert törzsfej 58 javul, 8 még eltér, 7 romlik (H0947 Pol., H0995 Po., H8199 Pô`el: a táblaszövegben a törzsfej a bekezdés elején áll, a Sefaria az előző törzsbe sorolja; kézzel, a forrás alapján nem bíráltam, a Sefaria téves voltát nem állítom); 1. jelentés a fej sorában 345 javul, 0 romlik.
- **A 40 soros minta 24 „Sefaria helyes” sorából 16 most egyezik** (P02, P03, P08, P14, P15, P18, P19, P20, P25, P26, P27, P30, P34, P35, P37, P38); marad 8: betű-csúszás (P01, P07, P28, P29), számcsúszás vagy hiányzó szám (P11, P22), P13 (a Sefaria-fából az 1. hiányzik, a törzs már helyes), P33 (Hithpa./Hithpe nevezéktan).
- **A mércelap:** a HAMART-001 mindkét generátoron (`--cel lexikon`, `--cel lexikon2`) bájtra változatlan (0 eltérő sor); `regresszio.py --id HAMART-001`: RENDBEN (engedély nélküli diff-sor: 0). Az ISTENTISZT-001 befagyasztva. A mérce B19 sora (`adat/bdb_vers_jelentes.tsv`) frissítve, és új `uj_bemenet` sor a `dontesek/uj/sefaria-tanu-proba-b13e41.md`-hez (N200: a szamkiosztas után a sor elavul).
- **Gépi kapu** (`teszt_bdb_vers_jelentes.py`, `TablaJavitasok`): szabályonként szintetikus pozitív és negatív eset; a javítások alkalmazásainak száma a teljes 2.30-on rögzített (egyes 130, összefoglaló 76, törzsfej 44, egyenlő 4): ha a 2.30 újragenerálása megváltoztatja, a teszt megáll; a 16 mintasor tanú-egyezése.
- **Maradék:** a 2546 jelzés nagy része a Sefaria saját feldolgozási hibája (betű- és számcsúszás, hiányzó „1.”), egy része a tábla további, még fel nem tárt hibája; ennek a hibaosztály-térképe külön tétel (N-F197d).
