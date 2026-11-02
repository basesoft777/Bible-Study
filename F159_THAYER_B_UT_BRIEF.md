---
feladat: 159
cim: "A Thayer-kötegelő csoportos útja (B-út), szűkített adatblokk, kalibrált becslő és mért költségű plafon — a #7 előfeltétele"
kod: THAYER_B_UT
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: nem_indult
ad: "eszkozok/thayer_api_koteg.py B-úttal (15–25 kicsi/közepes Strong egy kérésben, Strongonkénti visszabontás és kapuk, egyenkénti javító kör), a kérés Strongjaira szűkített terminológia- és Károli-blokkal, az F27 M1 mérésére kalibrált becslővel és mért futó összeggel számoló plafonnal; egy kb. 60 Strongos mérő batch effort=high és effort=medium mellett (legfeljebb 4 USD, csak naplóba), és a teljes Thayer B-úti kivetítése"
kovetkezo: "/kovetkezo a #27 (FP3) lezárása után; utána a #7 briefje ennek a mérésével készül"
olvas: [eszkozok/thayer_api_koteg.py, eszkozok/bdb_api_koteg.py, eszkozok/karoli_strong/api_koteg.py, eszkozok/thayer_jelolt/, forditas/prompt_v5_1.md, adat/terminologia.tsv, adat/karoli_strong/, adat/thayer_szakaszok.tsv, naplok/FP3_naplo.md, naplok/FP3_sorrend.tsv, naplok/THAYER_API_KOTEG_naplo.md, F158_THAYER_API_KOTEG_BRIEF.md, F27_FP3_BRIEF.md, DONTESEK.md]
ir: [eszkozok/thayer_api_koteg.py, eszkozok/teszt_thayer_api_koteg.py, forditas/thayer_api/, naplok/THAYER_B_UT_naplo.md]
fugg: [27]
nem_fugg: [7, 22, 38, 121, 158]
---

# F159_THAYER_B_UT_BRIEF.md — a Thayer-kötegelő csoportos útja (B-út)

*FELADATOK #159 · Modell: sonnet · v1 · 2026.11.02 · készítette: `claude-opus-5-5` a `/befogad` menetében; a felvételt a
felhasználó jóváhagyta (chat, 2026-11-02: „Igen, vedd fel”), a befogadás kérdéseiben az orkesztrátor döntött a felhasználó
megbízásából; a #7 (Thayer éles) előfeltétele.*

## 1. Cél és indok

A #27 (FP3) M1 mérő adagja a #158 kötegelőjével (`eszkozok/thayer_api_koteg.py`) lefutott: 5,71 USD, 32 Strong. A teljes Thayerre
vett kivetítés a mostani úton **207–311 USD** (5 437 kérés, egy Strong / kérés; `naplok/FP3_naplo.md`, a #27 ágán). A költség
~86%-a a kérésenként ismétlődő állandó prompt-rész (terminológia, Károli-tábla, szabályok): az M1 illesztése szerint
17 136 bemeneti token / kérés, cache nélkül; a kicsi Strongok fajlagosan ötször drágábbak a nagyoknál. Ehhez jön a sok gondolkodási
token.

A BDB API-része (#38, 13–14. adag) a B-úttal (`eszkozok/bdb_api_koteg.py`, `bbekuld`, B-csoportok) 1 878 Strongot 9,96 USD-ből
fordított. Ugyanezzel az úttal a Thayer becsült költsége 79–113 USD; az adatblokk szűkítésével és `effort=medium`-mal várhatóan
kevesebb (becslés, `manual`). Ez a feladat a B-utat, a szűkítést, a kalibrált becslőt és a mért költségű plafont építi be a
Thayer-kötegelőbe, és egy mérő batch-csel számszerűsíti a hatásukat, hogy a #7 briefje mért alapra készüljön.

A #27 nyitott tételei közül ez a feladat zárja az **N-F27a**-t (a becslő kalibrálása a mért modellre) és az **N-F27b**-t (mért futó
összeg a plafon-ellenőrzésben); l. `naplok/FP3_naplo.md`.

## 2. Hatókör

**Benne van:** az 1–6. követelmény a `eszkozok/thayer_api_koteg.py`-n és a tesztjén; egy mérő batch valódi beküldéssel, a meglévő
API-keretből (`PARDES_API_KEY`), összesen legfeljebb 4 USD mért költséggel; napló és kivetítés.

**Nincs benne:**
- a teljes Thayer fordítása (#7), és az `adat/forditasok.tsv` írása (a mérő batch eredménye csak naplóba kerül);
- a max_tokens-bukások (G1722, G1510, G4151) kezelése: a #7 briefjéé;
- a prompt-gyorsítótár mérése (N-F27d): külön marad, mert a B-út a kérésszám csökkentésével az állandó részt már leosztja, a BDB-n
  pedig a Batch-cache rontott (4,23 M token írás, 1,41 M olvasás);
- a #132 eszközeinek (`eszkozok/thayer_jelolt/`), a `bdb_api_koteg.py`-nak, az `api_koteg.py`-nak és a `prompt_v5_1.md`
  szabálytartalmának módosítása (ha a B-út ezek nélkül nem megy: ⛔ megállás, tétel a `DONTESEK.md`-be).

## 3. Követelmények

1. **B-út.** A kicsi (< 500 forráskarakter) és a közepes (500–2 999) Strongok csoportosan mennek, 15–25 Strong / kérés (a pontos
   méret a mérés tárgya, paraméter); a nagy (≥ 3 000) Strongok és a többcsoportos szócikkek maradnak egyenként. Minta: a
   `bdb_api_koteg.py` B-útja (`b_prompt`, `b_csoportok_epit`, `b_szetbont`, `bszaraz`, `bbekuld`): a közös szabály-rész egyszer áll,
   utána Strongonként az adatblokk és a forrás, a válasz Strongonként egy objektumot tartalmazó JSON-tömb. A szabálytartalom
   ugyanabból a `forditas.prompt_epit`-ből jön, nem másolat.
   - A visszabontás Strongonként **betűhű** (a helyőrzők Strongon belül számozottak, `emeles.helyorzo_visszaallit`);
   - a kapuk Strongonként futnak (`forditas.utofeldolgoz`, a 14–16. kapuval együtt), mintha egy Strongos kérés lett volna;
   - a bukott vagy hiányzó Strong a javító körben **egyenként** megy (A-stílus), a kapu hibaüzenetével.
2. **Adatblokk-szűkítés.** A terminológia- és a Károli-tábla a kérésben csak a kérés Strongjainak releváns soraival áll (a
   kötelező alakok uniója, mint a `kot_unio`-nál). A szűkítés előtti és utáni állandó rész tokenszáma a naplóba (a kiinduló érték:
   ~17 ezer token / kérés, F27 M1, mért).
3. **Kalibrált becslő.** A `TOKEN_KARAKTER`, a kimeneti és a gondolkodási szorzó az F27 M1 mért illesztéséből: bemenet =
   17 136 token / kérés + 3,721 token / forráskarakter; kimenet = 1 134 token / kérés + 1,654 token / forráskarakter
   (`naplok/FP3_naplo.md`, `naplok/FP3_koltseg.py`). B-úton és szűkítés után a kérésenkénti állandót a szűkített prompt
   adja; a becslés `manual` jelölésű marad, és a mérő batch után újraillesztendő (az új együtthatók a naplóba).
4. **Plafon mért költséggel.** A beküldés előtti ellenőrzés: a már lefutott batchek usage-éből vett futó összeg (USD) + a még
   beküldendő kérések kalibrált becslése ≤ plafon; különben nincs beküldés (kilépési kód 3, a `bdb_api_koteg.py` szerint). Ok: az
   F27 M1-ben a becslés-alapú plafon 14%-kal túlléphető volt. A `PLAFON_USD` alapértéke 0 marad.
5. **Mérő batch** (valódi beküldés): kb. 60 kicsi és közepes Strong a #27 sorrendjéből (`naplok/FP3_sorrend.tsv`), az M1 Strongjai
   nélkül; B-úttal `effort=high` és `effort=medium` mellett is (ugyanazok a Strongok). Összevetés: USD / forráskarakter,
   kapubukási arány (első kör, javító kör), a ténylegesen használt és a beállított max_tokens. **Plafon: összesen 4 USD, mért
   költséggel.** Munkamappa: `forditas/thayer_api/` alatt külön adag; az eredmény nem kerül a `forditasok.tsv`-be (a `beir` nem fut),
   csak a naplóba. A `modell` mezőbe a Batch-válasz tényleges modellneve kerül.
6. **Kivetítés** a teljes Thayerre a B-úttal (első kör + javító kör, kategóriánként: kicsi, közepes, nagy), mindkét `effort`-ra,
   `manual` jelöléssel, a mért arányokból; összevetés az F27 M1 207–311 USD-s kivetítésével.
7. **TSV és szkript:** `split('\t')` / `'\t'.join()`, a `csv` modul tilos; a szkript az importok után ráteszi a UTF-8 wrappert
   (CLAUDE.md); a kulcs sehol nem íródik ki.

## 4. Lépések

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév vs. `modell: sonnet`; eltérésnél nincs munka.
1. **Felmérés:** a `bdb_api_koteg.py` B-útjának és a `thayer_api_koteg.py`-nak az összevetése: mi vehető át, mi új (a naplóba).
2. **Kötegelő:** az 1–4. követelmény; a `szaraz` kiírja a B-úti kérésszámot, a szűkített állandó részt és a kalibrált becslést.
3. **Tesztek** (`eszkozok/teszt_thayer_api_koteg.py`, hálózat nélkül): a B-prompt Strongonkénti része bájtra azonos az egy Strongos
   prompt bemeneti részével; a visszabontás és a helyőrző-visszaállítás körútja betűhű; hamis B-válaszból a kapuk Strongonként
   futnak, a hiányzó Strong javítandó lesz; a szűkített blokk minden, a kérés Strongjaira vonatkozó sort tartalmaz, és mást nem; a
   plafon a mért futó összeggel számol (0 plafonnal nincs beküldés); a meglévő tesztek zöldek.
4. **Száraz futás** a mérő adagra és a teljes Thayerre; a becslés a naplóba.
5. ⛔ **A mérő batch beküldése előtt** a száraz becslés (mindkét `effort`) a naplóban; ha a becslés a 4 USD-t meghaladja, megállás,
   és a Strong-szám csökkentésére javaslat. Különben: beküldés (`high`, majd `medium`), begyűjtés, kapuzás, javító kör.
6. **Napló és kivetítés** (`naplok/THAYER_B_UT_naplo.md`): mért költség (USD, token: bemenet, kimenet, gondolkodás),
   bukási arányok, max_tokens, újraillesztett együtthatók, kivetítés a teljes Thayerre; proveniencia-sorral, a becslés jelölve.
7. **Zárás:** tesztek, `python eszkozok/feladatok.py ellenoriz`, `fuggetlen-ellenor`, draft PR.

## 5. Kész, ha

- K1: a `thayer_api_koteg.py` B-úttal, szűkített adatblokkal, kalibrált becslővel és mért futó összeget használó plafonnal; a #132
  eszközei, a `bdb_api_koteg.py` és az `api_koteg.py` bájtra változatlan.
- K2: a tesztek zöldek, hálózati hívás nélkül.
- K3: a mérő batch lefutott mindkét `effort`-ral, a mért összköltség ≤ 4 USD; az `adat/forditasok.tsv` változatlan.
- K4: a napló a mért összevetéssel, az újraillesztett együtthatókkal és a teljes Thayer kivetítésével (`manual`); az N-F27a és az
  N-F27b lezárásra javasolva, hivatkozással.
- K5: a `fuggetlen-ellenor` jelentése `TISZTA`.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.11.02 | Első változat: B-út, adatblokk-szűkítés, kalibrált becslő, mért költségű plafon, mérő batch (≤ 4 USD), kivetítés | felvétel: a felhasználó (chat, 2026-11-02: „Igen, vedd fel”); a befogadás kérdései (a #27 `nem_fugg: [159]` a függési kör feloldására; a #7 `fugg`-ja kiegészítve a 159-cel; az N-F27d kívül marad): orkesztrátori döntés a felhasználó megbízásából, 2026-11-02 |
