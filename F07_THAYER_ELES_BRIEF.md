---
feladat: 7
cim: "Thayer teljes magyar fordítása (éles), API-n a B-úttal, mért költségű adagokban"
kod: THAYER_ELES
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: nem_indult
ad: "a teljes Thayer (a kész Strongok nélkül kb. 5 385 Strong) szakaszonkénti magyar fordítása az adat/forditasok.tsv-ben (allapot=sonnet, a tényleges modellnévvel), a #159 B-útján Message Batches API-n, kb. 500 000 karakteres adagokban, adagonként mért költséggel; a kétszer bukott Strongok a bukottak-táblában, kézi ítéletre"
kovetkezo: "/kovetkezo: M0 (a kötegelő javításai, a becslő újraillesztése, az effort-döntés ⛔ az orkesztrátornak), utána adagonként új session"
olvas: [adat/forditasok.tsv, F27_FP3_BRIEF.md, F158_THAYER_API_KOTEG_BRIEF.md, F159_THAYER_B_UT_BRIEF.md, naplok/FP3_naplo.md, naplok/FP3_sorrend.tsv, naplok/FP3_koltseg.py, naplok/FP3_arany.md, naplok/THAYER_B_UT_naplo.md, naplok/THAYER_B_UT_mero_strongok.txt, naplok/THAYER_API_KOTEG_naplo.md, forditas/prompt_v5_1.md, adat/terminologia.tsv, adat/kiejtes_kivetelek.tsv, adat/thayer_szakaszok.tsv, adat/thayer_forras_javitas.tsv, adat/karoli_strong/, adat/SEMA.md, konkordancia/Thayer_teljes.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, eszkozok/thayer_jelolt/, DONTESEK.md]
ir: [adat/forditasok.tsv, adat/thayer_sigla.tsv, adat/terminologia.tsv, eszkozok/thayer_api_koteg.py, eszkozok/teszt_thayer_api_koteg.py, eszkozok/normalizal.py, eszkozok/teszt_normalizal.py, eszkozok/forditas_kapuk.py, eszkozok/teszt_forditas_kapuk.py, eszkozok/thayer_jelolt/thayer_bemenet.py, forditas/thayer_api/, naplok/F132_THAYER_SZAKASZ_munka.tsv, naplok/F132_THAYER_SZAKASZ_bukottak.tsv, naplok/THAYER_ELES_naplo.md, naplok/THAYER_ELES_sorrend.tsv, naplok/THAYER_ELES_koltseg.tsv, naplok/THAYER_ELES_arany.md, naplok/THAYER_ELES_sigla_javaslat.tsv, naplok/THAYER_ELES_terminologia_javaslat.tsv, naplok/THAYER_ELES_M0.py, NYITOTT_FELADATOK.md, DONTESEK.md]
fugg: [3, 5, 14, 159]
nem_fugg: [9]
---

# F07_THAYER_ELES_BRIEF.md — a Thayer teljes magyar fordítása (éles)

*FELADATOK #7 · Modell: sonnet · v1 · 2026.11.02 · készítette: `claude-opus-5-5` az orkesztrátor megbízásából (a csonk-brief
kitöltése); a tartalmi döntések az orkesztrátoréi (a felhasználó megbízásából, 2026-11-02; DT-F07a); a merge a felhasználóé.*

**Címzett.** E brief minden ⛔ pontjának és döntési kérdésének címzettje az **orkesztrátor-session** (nem a felhasználó). A végrehajtó
a kérdést a `DONTESEK.md`-be veszi fel helyőrzővel (`DT-F07<betű>`), elküldi az orkesztrátornak, és megáll. Merge csak a
felhasználótól.

## 1. Cél

A Thayer (`konkordancia/Thayer_teljes.tsv`) minden még le nem fordított Strongjának szakaszonkénti magyar fordítása az
`adat/forditasok.tsv`-ben, a #132 szakaszos láncán (`eszkozok/thayer_jelolt/forditas.py`, prompt v5.1, adatblokk, javítóréteg,
1–16. kapu), a #158/#159 kötegelőjével (`eszkozok/thayer_api_koteg.py`), Message Batches API-n, a meglévő API-keretből.

Előzmények (mért, a hivatkozott naplókból):

| Lánc | Eredmény | Forrás |
|---|---|---|
| #158 kötegelő | `thayer_api_koteg.py` (`szaraz` … `beir`) | `naplok/THAYER_API_KOTEG_naplo.md` |
| #27 M1 (egy Strong / kérés) | 32 Strong, 5,7054 USD (+ aranyminta 1,1069 USD); 28 Strong beírva; kivetítés 207–311 USD | `naplok/FP3_naplo.md` |
| #159 B-út, mérő batch | 60 Strong, 1,187 USD (high 0,6552, medium 0,5319); kivetítés a teljes Thayerre **88 USD (high) / 72 USD (medium)**, `manual` | `naplok/THAYER_B_UT_naplo.md` 4–6. |

A DT494 (a) szerint a #7 a #159 lezárása után indulhat; a #159 PR #581-gyel mergelve (main `f3d0435a`).

## 2. Hatókör

**Benne van:**
- **M0** (első session): a kötegelő #7 előtti javításai és mérései (4. pont), az effort-döntés előkészítése;
- **A1 … An** (adagonként új session): a fordítás kb. 500 000 forráskarakteres adagokban;
- **Mz**: lezárás, teljességi ellenőrzés.

**Nincs benne:**
- a prompt-gyorsítótár mérése (N71): külön tétel marad (DT494 (b));
- a `kezi` és `opus` sorok módosítása (a `kezi` sor a DT329 (ii) szerint érvényes marad; `beir --kezi-marad`);
- a `forditas/prompt_v5_1.md` szabálytartalmának módosítása (ha kell: ⛔, DT-F07 tétel);
- a `bdb_api_koteg.py` és az `api_koteg.py` módosítása;
- a lexikon szócikkeinek renderelése (#28 és a lexikon-ág dolga).

## 3. Út, modell, költségkeret

1. **Út: a #159 B-útja.** A kicsi (< 500 forráskarakter) és a közepes (500–2 999) Strongok csoportosan (`bszaraz`, `bbekuld`;
   alapérték 20 Strong / 16 000 forráskarakter / kérés, `--b-db`, `--b-kar`), a nagyok (≥ 3 000) és a többcsoportos szócikkek
   egyenként (`szaraz`, `bekuld`). Szűkített adatblokk (a terminológia- és a Károli-tábla csak a kérés Strongjainak releváns
   soraival; a `--nincs-szukites` nem használható). Plafon: a mért futó összeg + a függő batchek becslése + az új becslés
   (`plafon_ellenorzes`).
2. **Futás:** Message Batches, a kulcs a `PARDES_API_KEY` környezeti változóból (nem íródik ki, fájlba és naplóba nem kerül), a
   meglévő API-keretből.
3. **Modell:** `claude-sonnet-5-5` (a kötegelő `MODELL`-je). Az adattábla `modell` mezőjébe a Batch-válasz tényleges modellneve
   kerül; briefből vagy korábbi sorból másolni tilos. **Effort:** az M0 ⛔ (e) döntése szerint (`--effort high|medium`); a döntés
   után a futás végéig nem változik.
4. **Költségkeret.**
   - Kivetítés (a #159 mérése, `manual`): 72–88 USD a teljes Thayerre.
   - **Összplafon: 120 USD mért költség** a #7 egészére (M0 mérő batchjei + minden adag első és javító köre). A #27 (6,81 USD) és a
     #159 (1,19 USD) költsége nem számít bele. Az összplafont **csak az orkesztrátor emelheti** (DT-F07 tétel).
   - **Adagplafon:** az adag kalibrált becslésének (első kör + javító kör, 4. pont (a)) **1,3-szerese**, a kötegelő `--plafon`
     paraméterében, mért futó összeggel. Beküldés előtt: eddigi összes mért költség + az adagplafon ≤ 120 USD; különben ⛔.
   - **Megállás:** ha egy adag mért költsége a becslést 30%-kal meghaladja (mért > 1,3 × becslés), vagy a kötegelő a plafonon
     megáll (kilépési kód 3): az adag félbemaradt része nem megy tovább, ⛔ az orkesztrátornak (jelentés: becslés, mért, eltérés oka,
     a kategóriánkénti bontás).
   - **Költségnapló:** `naplok/THAYER_ELES_koltseg.tsv` — `szakasz` (M0, A1, A2 …, Mz), `becsles_usd`, `plafon_usd`, `mert_usd`,
     `osszes_mert_usd`, `batch_azonositok`, `proveniencia`. A mért érték csak a kötegelő `futasnaplo.tsv`-jéből jöhet; becslés nem
     kerül mért érték helyére.

## 4. M0 — előkészítés (első session; csak mérő batch, éles beírás nincs)

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév vs. `modell: sonnet`; eltérésnél nincs munka.
1. **Kiinduló állapot** újramérve (proveniencia-sorral): `thayer_api_koteg.py lista` (fordítandó / kész Strongok), a
   `naplok/F132_THAYER_SZAKASZ_bukottak.tsv` sorai, a `feladatok.py fuggesek` kizárásai (a #38 és a #154 nem futhat egyszerre a
   `beir`-rel).

**(a) A becslő újraillesztése (N68 lezárása).** A `BE_KERES`, `BE_KAR`, `KI_KERES`, `KI_KAR`, `ALLANDO_REF_KAR` konstansok
újraillesztése a #27 M1 (51 első körös kérés, egy Strongos út, a nagy kategória egyetlen mért alapja) és a #159 mérő batch (4 B-kérés
mindkét effortra, 15 javító kérés) mért adataiból, kategóriánként (kicsi/közepes B-kérés, nagy egy Strongos kérés, javító kérés),
effortonként külön kimeneti együtthatóval. A becslő a javító kört is becsülje: a kategóriánként mért bukási arány × a mért javító
kérés költsége (a #159 szerint a kicsi/közepes költség kb. harmada a javító kör). Szkript: `naplok/THAYER_ELES_M0.py`; az
illesztés, a pontszám és a maradék hiba a naplóba. A `szaraz`/`bszaraz` kiírja az első kör és a javító kör becslését külön és
együtt. Az N68 és az N69 (mért futó összeg, a #159-ben kész) lezárása a `NYITOTT_FELADATOK.md`-ben, hivatkozással.

**(b) B-stílusú javító kör.** A kapun bukott vagy a B-válaszból hiányzó kicsi/közepes Strongok javító köre csoportosan menjen
(B-javító kérés: a közös szabály-rész egyszer, utána Strongonként a forrás, az előző nyers válasz és a kapu hibaüzenete; a hiányzó
Strongnál friss kérés). A nagy Strongok javító köre egyenként marad. Tesztek (`eszkozok/teszt_thayer_api_koteg.py`, hálózat
nélkül): a B-javító kérés Strongonkénti része a hibaüzenettel bájtra a várt; a visszabontás és a kapuzás Strongonként; a már
beküldött javító kérés nem megy újra; a plafon a B-javító batchre is a mért futó összeggel számol.

**(c) A max_tokens-bukások a nagy szócikkeken (N70, N75).** A #27 M1-ben a G1722 és a G1510 (és az aranyminta G4151) javító
kérése `max_tokens`-szel állt le; a G3588 és a G1519 kapun bukott kétszer. Mérés: a nyers válaszok usage-e (beállított vs.
használt kimenet, csoportonként) a `forditas/thayer_api/adag1/` és `adag99/` mappából; a csoportméret (`CSOPORT_CEL`) és a
javító kör bemenete (az előző válasz assistant-fordulóként: a kimenet kétszer megy). Két út: **(1)** a `max_tokens` emelése (a
modell megengedett kimeneti maximumáig, a `claude-api` referencia szerint), vagy **(2)** további darabolás (kisebb csoportok a
`thayer_bemenet.csoportok`-ban, illetve a javító kör csak a bukott csoportra). Kis mérő batch a négy Strongon (G3588, G1722,
G1510, G1519) a választott út(ak)kal. **⛔ (c): az út kiválasztása mérésből, az orkesztrátor dönt** (DT-F07b).

**(d) A #27 M0/M1 talált hiányai (N72).**
- **Apokrif könyvek leképezése** a `11_konyvek` kapuban és a `normalizal.py`-ban (Makk, 3Macc., Tób, Judit, Bölcs/Wis., 1 Esdr.;
  a #27 M1 és a #159 bukásai: G0846, G3588, G1161, G1519, G1632, G2837, G0163, G5009, G2253). Teszt a `teszt_normalizal.py`-ban és a
  `teszt_forditas_kapuk.py`-ban.
- **`1 Cor.` alias** (112 előfordulás a teljes Thayerben): előbb kontextus-mérés, hány esetben az 1Kor és hány esetben Kelemen
  (`Clem. Rom. 1 Cor.`) a hivatkozás; az alias csak az egyértelmű alakra kerül be. Ha a kettő gépileg nem választható szét: ⛔.
- **`Sir` alias** (536 előfordulás): a fordítás a Sirák fiát `Sir`-ként írja, a `lekerdez.py` / `nave_bontas.py` viszont a
  `Sir`-t a JSir aliasaként olvassa (N-F142a). Mérés: melyik olvasót érinti a teljes Thayer beírása. A javítás helye (az olvasó
  aliasa vagy a fordítás alakja) ⛔ (DT-F07c), mert a `lekerdez.py` nem ennek a feladatnak az `ir`-je.
- **Sigla-jóváhagyás a teljes Thayerre:** a 5 758 `jelolt` sigla-előfordulás (`adat/thayer_sigla.tsv`) besorolási javaslata
  (`naplok/THAYER_ELES_sigla_javaslat.tsv`: sigla, kibontás, előfordulás, példa-Strong; külön a „Sept.” és a „Wis.”). **⛔ (d1)**:
  az orkesztrátor soronként jóváhagyja; a `thayer_sigla.tsv` csak a jóváhagyás után változik (`besorolt`).
- **Terminológia-javaslatlista** (`naplok/THAYER_ELES_terminologia_javaslat.tsv`: angol · javasolt magyar · előfordulás · példa;
  a #27 M0 5. pontjának listája: grammar, aorist, passive, genitive, infinitive, participle, …). **⛔ (d2)**: jóváhagyás után kerül
  az `adat/terminologia.tsv`-be.
- **A G0282 kész sorának `Heb.` kapuhibája** (`5_terminologia`: „Heb. → héb. hiányzik”): a G0282 az A1 adagba kerül, és
  újrafordul (`beir --regi-elavult --kezi-marad`); a `kezi` sora marad. A sor kézi javítása tilos, mert így a gépi sor
  provenienciája tiszta marad (DT-F07a 3.).

**(e) Effort-döntés.** Az aranyminta (G0282, G1941, G1944, G4151, G5590; a `kezi` sorok az összevetés alapja) egy kis Batch-csel
`effort=high` és `effort=medium` mellett is, a #7 útján (B-út, az (a)–(d) javításai után; a G4151 a (c) döntése után). Az eredmény
nem kerül a `forditasok.tsv`-be (`beir` nem fut), csak a `naplok/THAYER_ELES_arany.md`-be: szakaszonként forrás, `kezi`, high,
medium egymás alatt, és Strongonként a tartalmi eltérések listája (kihagyás, terminológia, értelmi eltérés, a `kezi`-től eltérő
szóválasztás, kapueredmény), plusz mért költség és kapubukás effortonként. Ítéletet a végrehajtó nem hoz. **⛔ (e): az effort-döntés
az orkesztrátoré** (DT-F07d).

**(f) A #159 mérő Strongjainak beírása (0 USD; DT-F07a 2.).** A #159 mérő batchének 60 Strongja
(`naplok/THAYER_B_UT_mero_strongok.txt`) nincs a `forditasok.tsv`-ben. Az (e) döntése után a választott effort ágának eredménye
(`forditas/thayer_api/adag1591/`: high, `adag1592/`: medium) a mostani, (a)–(d) utáni kapukkal **újrakapuzódik** (`kapuz`);
ami átmegy, az `rogzit` és `beir --regi-elavult --kezi-marad --allapot sonnet` útján kerül be. Ennek a sornak a `megjegyzes`
mezőjében álljon, hogy a #159 mérő batchéből származik, újrakapuzva, az adag (`adag1591`/`adag1592`) és a batch azonosítójával.
A `modell` a futásnapló tényleges modellneve. Ami nem megy át, az az adagokban újrafordul (a sorrendtáblában marad).

2. **Sorrend és adagterv** (`naplok/THAYER_ELES_sorrend.tsv`): a `naplok/FP3_sorrend.tsv` sorrendje, a már kész Strongok nélkül
   (a #27 M1 28 beírt Strongja, az (f) szerint beírtak és minden, amelynek szakaszsora már az `adat/forditasok.tsv`-ben van;
   a G0282 az A1 elejére kerül); oszlopok: `sorszam`, `strong`,
   `gyakorisag`, `karakter`, `szakasz`, `kategoria` (kicsi/közepes/nagy), `adag`. Adagok kb. 500 000 forráskarakterrel (az utolsó
   lehet kisebb); adagonként a kalibrált becslés (első kör + javító kör) és az adagplafon (1,3 ×). Ha az összes adag becslése
   120 USD fölött van: ⛔.
3. **M0 plafon:** az M0 mérő batchjei ((c) és (e)) együtt legfeljebb **5 USD** mért költség, ami az összplafonba
   beszámít (DT-F07a 1.). Az (f) nem küld be semmit.
4. **Zárás:** tesztek zöldek (`eszkozok/teszt_thayer_api_koteg.py`, `teszt_normalizal.py`, `teszt_forditas_kapuk.py`,
   `eszkozok/thayer_jelolt/teszt_*.py`; a `teszt_lanc.py` N66-tesztje és a #27 naplójában igazolt előzetes bukások kivételek),
   `python eszkozok/ellenoriz.py` SÉRTÉS 0, `python eszkozok/feladatok.py ellenoriz` 0 hiba, `fuggetlen-ellenor`, draft PR. **⛔ M0:**
   jelentés az orkesztrátornak a (c), (d1), (d2), (e) és a Sir-kérdés döntéseivel; az A1 csak ezek után, a M0 PR mergelése után indul.

## 5. A1 … An — éles adagok (adagonként új session)

Tájékozódás: ez a brief, a `naplok/THAYER_ELES_sorrend.tsv` és a `naplok/THAYER_ELES_koltseg.tsv`. A következő adag az első
olyan `adag` értékkel kezdődik, amelynek Strongjai közül még van, aminek nincs szakaszsora az `adat/forditasok.tsv`-ben és a
bukottak-táblában sem áll. Munkamappa: `forditas/thayer_api/adag7<nn>/` (A1 = `adag701`; a meglévő `adag1`, `adag99`,
`adag1591`, `adag1592` nem írható). Az adag csak az előző adag PR-jának mergelése után indul (az `adat/forditasok.tsv`-nek egy
írója van).

0. Modell-ellenőrzés; `git log` a main-en: az előző adag benne van.
1. `bszaraz` és `szaraz` az adag Strong-listájára → becslés (első kör + javító kör, kategóriánként) a koltseg-táblába; adagplafon
   = 1,3 × becslés; eddigi összes mért + adagplafon ≤ 120 USD, különben ⛔.
2. `bbekuld --plafon <adagplafon>` (B-kérések) és `bekuld --plafon <adagplafon>` (a nagyok), a választott `--effort`-tal → `allapot`
   (legfeljebb 5 percenként) → `begyujt` → `kapuz`.
3. `javit` (a B-stílusú javító kör a kicsi/közepesre, egyenként a nagyokra; egy kör) → `begyujt` → `kapuz`.
4. `rogzit` (a kétszer bukottak a `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`-be) → `beir --regi-elavult --kezi-marad --allapot sonnet`.
5. Mért költség a koltseg-táblába; ha mért > 1,3 × becslés: ⛔ (3. pont 4.).
6. Ellenőrzés: `python eszkozok/ellenoriz.py` SÉRTÉS 0; `python eszkozok/feladatok.py ellenoriz` 0 hiba; a `forditasok.tsv`
   diffjében csak új szakaszsorok és a `--regi-elavult` által `elavult`-ra tett régi `teljes` sorok (minden más sor bájtra azonos).
   Piros esetén nem commitol, csak jelent.
7. Napló (`naplok/THAYER_ELES_naplo.md`, adagonként egy szakasz, legfeljebb 15 sor): Strong-szám, forráskarakter, kérésszám
   (B / egyenkénti / javító), batch-azonosítók, becslés és mért költség, első körös és javító kör utáni bukás kapunként, összesen
   kész / hátra, proveniencia-sor.
8. Commit csomagonként és az adag végén (`F7.A<n>.<k>: …`, UTF-8 fájlból), push, draft PR a main-re; rövid jelentés az
   orkesztrátornak (≤ 8 sor). **Megállás**: a következő adag új sessionben, az orkesztrátor indítja.

## 6. Mz — lezárás (ha a sorrendtábla elfogyott)

1. **Teljességi ellenőrzés:** a `naplok/THAYER_ELES_sorrend.tsv` minden Strongja vagy `kesz` (szakaszsora az
   `adat/forditasok.tsv`-ben `allapot=sonnet`, illetve a `kezi` sor mellett `--kezi-marad`), vagy a bukottak-táblában áll; a lista a
   naplóba (két szám és a különbség: 0). A `lista` parancs fordítandó listája üres, vagy csak bukott Strongot tartalmaz.
2. **Bukottak:** a `naplok/F132_THAYER_SZAKASZ_bukottak.tsv` összesítése kapunként, Strongonként a hibaüzenettel; **⛔ Mz**:
   kézi ítéletre az orkesztrátornak (újrafordítás, kézi javítás vagy angol marad).
3. `python eszkozok/ellenoriz.py` SÉRTÉS 0, a CI E19 zöld, `python eszkozok/feladatok.py ellenoriz` 0 hiba.
4. Összköltség (mért) és összevetés a 72–88 USD-s kivetítéssel.
5. `fuggetlen-ellenor` (a teljes #7 diffjén, szúrópróbával: 10 Strong különböző hosszból és gyakoriságból), zárójelentés, a
   saját fejléc (`allapot: lezarva`, `lezarva_osszegzes`), draft PR.

## 7. Szabályok

- **Egy session = egy ág = egy PR** (M0, minden adag, Mz).
- **A prompt, a terminológia, a sigla-tábla, a kapuk és az effort az A1-től a futás végéig nem változnak.** Változtatás csak adagok
  között, ⛔-val; a korábbi adagok sorait ez nem fordítja újra, csak ha az orkesztrátor kéri.
- **Kapuhiba:** egy javító kör a kapu hibaüzenetével; másodszori bukás → bukottak-tábla, a futás továbbmegy.
- **Szellem-szabály** (DT25, DT-F38g), **R. V. / A. V. után angolul, szó szerint** (DT-F38f 5), **forráshiba**: a javított
  forrásnézet az irányadó (DT333 (2)) — a #27 brief 6. pontja szerint.
- **A plafon kemény:** elérése megállás, nem emelés. Emelést csak az orkesztrátor adhat, a `DONTESEK.md`-ben rögzítve.
- **Számok** csak futtatott parancsból vagy a kötegelő naplójából; minden lekérdezésből származó szám mellett proveniencia-sor.
- **TSV:** `split('\t')` / `'\t'.join()`, a `csv` modul tilos; táblát író szkript írás előtt összeveti a sorokat az eredetivel.
  **Shell:** görög vagy magyar szöveget tartalmazó kód fájlból fut; az új szkript az importok után ráteszi a UTF-8 wrappert.
- A scratchpadben nem maradhat semmi, ami kell; a munkamappa a repóban (`forditas/thayer_api/`), a `--munka` próbák a repón kívül.

## 8. Kész, ha

- K1 (M0): a becslő újraillesztve, a B-stílusú javító kör és az (c)–(d) javításai a kötegelőben és a normalizálóban, tesztekkel;
  az N68, N69 lezárva; a `THAYER_ELES_sorrend.tsv` és az adagterv kész; a DT-F07b–d eldöntve.
- K2 (adagonként): az adag szakaszsorai az `adat/forditasok.tsv`-ben (`allapot=sonnet`, tényleges modellnév), minden más sor
  bájtra változatlan; ellenőrzések zöldek; mért költség a koltseg-táblában, az adagplafonon belül.
- K3 (Mz): a teljességi ellenőrzés különbsége 0; a bukottak kézi ítéletre átadva; az összköltség ≤ 120 USD (vagy az orkesztrátor
  rögzített emelése); `fuggetlen-ellenor`: `TISZTA`.

## 9. Döntésnapló

| Tétel | Tárgy | Állapot |
|---|---|---|
| DT-F07a | a brief kerete (út, M0 tartalma, adagméret, plafonok, címzett); 1. M0 plafon 5 USD; 2. a #159 mérő Strongjai újrakapuzva beírhatók; 3. G0282 újrafordul, kézi javítás nélkül; 4. a függési kör: a #27 és a #159 fejlécének lezárása (külön PR, előbb mergelendő); 5. a #138 és a #154 `nem_fugg`-jába a 7 | ✅ orkesztrátor, 2026-11-02 (`DONTESEK.md`) |
| DT-F07b | ⛔ M0 (c): max_tokens-emelés vagy további darabolás | nyitva, M0 |
| DT-F07c | ⛔ M0 (d): a `Sir` alias javításának helye (és ha kell, az `1 Cor.`) | nyitva, M0 |
| DT-F07d | ⛔ M0 (e): effort (`high` / `medium`) | nyitva, M0 |
| DT-F07e … | a sigla- és terminológia-jóváhagyás (d1, d2), adag-megállások, plafonemelés | a menet veszi fel |

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.11.02 | A csonk kitöltése: B-út, M0 (a)–(f), adagok ~500 000 karakterrel, adagplafon 1,3 × becslés, 30%-os megállás, összplafon 120 USD, Mz. A befogadás kérdései (a kitöltött fejléc függési köre, `feladatok.py ellenoriz`): a #27 és a #159 fejléce lezárul, külön, előbb mergelendő PR-ban (mindkettő tartalmilag kész és mergelve: PR #578, PR #581); a #7 `fugg: [159]` marad; az `olvas` a `forditasok.tsv`-vel bővül (a `lista` és a `beir` olvassa); a #138 és a #154 `nem_fugg`-jába bekerül a 7, mert a #138 és a #154 BDB- és alapjelentés-sorokat ír, Thayer-sort nem. Csak a sorrendi függés esik ki: a `KIZAR 7 154` (`forditasok.tsv`, írás–írás) megmarad; a #138 a `forditasok.tsv`-t nem írja, ezért vele nincs KIZAR-él, és nem is kell | orkesztrátor (a felhasználó megbízásából), 2026-11-02; DT-F07a |
