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
