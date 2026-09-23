# SZOTAR_BRIEF.md — szótári adatréteg: szerepmátrix-források, fordítási gyorsítótár, kiejtés

*v1 — 2026.09.23 · jóváhagyásra: a §2 S-döntései és a §0/§4 számai · a `RENDER_BRIEF.md` v3 kettéválásából (ott D13); OCR-kezelés (D12), héber kiejtés-jelöltek (D13), LXX-korpuszszint (D14) · KIEJT-kiváltás (D15)*

**Cél.** A `RENDER_BRIEF.md` G6 szerepmátrixának minden cellája adatból töltődjön, és a
szótári réteg rendezett legyen: fordítási gyorsítótár, terminológia, görög kiejtés, a
TBESH egyesítése, az UBS DBH teljes importja, a Mounce/SECE, a Cremer, a Girdlestone és a
BDB-etimológia adatosítása. A végén a 8 törzscikk 5. szakaszában nincs `nincs adatosítva` cella.

**Előfeltétel:** a `RENDER_BRIEF.md` 2. menete lezárva (a rések forrása a tanulmány, a
törzscikk és a `szotar_szerepek.tsv` megvan).

**Szerkezet.** S0 kiegészítő felmérés ⛔ → 1. menet: nulla-diff ⛔ → 2. menet: kimenet-változtató.
Az R0.3–R0.6 munkalapjai (`naplok/RENDER_R0_*`) ennek a briefnek a felmérését már elvégezték;
az S0 csak az új forrásokat méri.

**Modell:** Sonnet. **Push csak külön kérésre.**

**Nincs benne:** fordítási pipeline (`fordit.py`, külső modellek), BDB SQLite-csere, héber
gépi kiejtés, Trench (*Synonyms of the New Testament*, később kiegészítő forrás).

---

## 0. Kiindulás *(az S0.1 újraméri; eltérésnél ÁLLJ)*

| # | Mérés | Érték |
|---|---|---|
| 0.1 | `main` = `origin/main` | a RENDER 2. menete utáni hash |
| 0.2 | `adat/lexikon_hivatkozasok.tsv` | 24 sor (Thayer 14, BDB 4, TBESG 4, TBESH 1, LSJ 1); `forditas_hu` kitöltve: 11 |
| 0.3 | `adat/forditas_ubs.tsv` | 20 sor; `definicio_hu` 20, `glosszak_hu` 20 |
| 0.4 | token a 8 motívum előfordulásaiban | H 24, G 13 |
| 0.5 | TBESH: `.txt` bővebb / `.lexicon` bővebb / kb. egyenlő (24 H-token) | 9 / 13 / 2 — egyik sem tartalmazza a másikat |
| 0.6 | MCGED lefedettség (13 G-token) | 13/13 |
| 0.7 | SECE (13 G-token) | 13/13; `LN:`, `GK:`, `Hebrew:` almező gépileg kinyerhető |
| 0.8 | kiejtés-tesztkészlet (`naplok/RENDER_kiejtes_tesztkeszlet.tsv`) | 200 pár (görög 112, héber 88); ebből aranykészlet 99 (görög 50, héber 49, az ISTENTISZT-001 kézi szövegéből) |
| 0.9 | átírás-leltár (`naplok/RENDER_R0_atirasok.tsv`) | 936 tétel (görög lemma 15, alak 290; héber lemma 25, alak 606) |
| 0.10 | nyers SQLite | `MCGED.lexicon` 10 666 sor; `TBESH.lexicon` 9 888 sor |
| 0.11 | UBS DBH forrás | `UBSHebrewDic-v0.9.2-en.JSON`, SHA-256 a `konkordancia/SDBH_SDGNT_README.md`-ben; eddig csak a doménjei importálva |
| 0.12 | `szotar_szerepek.tsv` | 20 sor (10 szerep × 2 nyelv; az LXX-híd adatosítva); `nincs adatosítva`: Cremer, Girdlestone + Cremer héber mutatója, UBS DBH (3 szerep), Mounce, SECE (2), BDB-etimológia, kiejtés (görög, héber) |
| 0.13 | LXX-híd adata | `konkordancia/LXX_OS/*.tsv` (CC BY 4.0), **versszintű**, nem szóillesztett; `adat/lxx_dontesek.tsv` |
| 0.14 | héber tudományos átírás | `OSHL_lexikalis_index.tsv` `atiras` mező (pl. `ʾāb`) |

---

## 1. Fogalmak

- **Fordítási gyorsítótár:** `adat/forditasok.tsv`, minden magyar fordítás egyetlen helye, forrás-hash-sel.
- **Adatosítva:** a szerep cellája a `konkordancia/` egy importált, verziózott táblájából töltődik.
- **Cella-értékek a törzscikk lefedettségi mátrixában:** forrás-hivatkozás; `a forrás nem tárgyalja` (a forrásban nincs szócikk — érdemi adat); `—` csak ott, ahol a szerep az adott nyelven nem értelmezett.
- **Nulla-diff:** mint a RENDER-ben: `git status --porcelain lexikon/` üres az `--ir` után.

---

## 2. S-döntések *(jóváhagyásra)*

| # | Kérdés | Javaslat |
|---|---|---|
| S1 | Fordítási gyorsítótár | **`adat/forditasok.tsv`**, oszlopok: `szotar`, `strong`, `entry_id`, `jelentes_szam`, `mezo`, `forras_hash`, `forditas_hu`, `allapot`, `modell`, `datum`, `terminologia_verzio`. Kulcs: `szotar+strong+entry_id+jelentes_szam+mezo`. `forras_hash` = a forrásszöveg SHA-1-e. Migráció: 11 lexikon-fordítás + 20 UBS-definíció + 20 UBS-glossza = **51 sor**, `allapot=kezi`. A `lexikon_hivatkozasok.forditas_hu` oszlop és a `forditas_ubs.tsv` megszűnik. |
| S2 | Terminológia | **`adat/terminologia.tsv`** (`angol`, `magyar`, `megjegyzes`, `verzio`); induló sorok: spirit = szellem, spiritual = szellemi, soul = lélek. Az ellenőrző csak jelent. |
| S3 | Kiejtés és átírás | **Görög: szabálytábla (`adat/kiejtes_szabalyok.tsv`) + `eszkozok/kiejtes.py`.** Héber: a render nem generál; lemma-kiejtés csak a kézi `adat/kiejtes_kivetelek.tsv`-ből. **Héber jelöltek:** az OSHL tudományos átírásából (`atiras`, amelyben a hangzó svá, a dagesh-kettőzés és a qamets qatan már eldöntött) szabálytábla (`adat/kiejtes_heber_jeloltszabalyok.tsv`) ad magyaros jelöltet; a jelölt csak kézi jóváhagyás után kerül a kivételtáblába. **Cél: a 8 motívum 24/24 héber lemmája a kivételtáblában.** Az alakszint (606 tétel) marad STEP-átírás. **Tesztkészlet:** a 99 pár aranykészlet; a további 101 pár csak az S0.5 tisztítása után kerül be. **Az élesítés mércéje** nem darabszám, hanem a tisztított átírás-lista (S0.6) tételei: az S2.1 diffjének pontosan ezeket kell érintenie; a 936 ellenőrző összeg. Élesítés feltétele: a görög tesztkészlet 100%-os egyezése. |
| S4 | TBESH | **Unió, nem csere:** `konkordancia/TBESH_konszolidalt.tsv` a `.lexicon` strukturált mezőivel és a `.txt` teljes szövegével; szócikkenként a teljesebb szöveg, a forrás soronként jelölve (`forras` = `txt` / `lexicon`). Addig a render a mai `.txt`-ből dolgozik. |
| S5 | UBS DBH | **Teljes import a meglévő JSON-ból**, az `ubs_dntg_import.py` mintájára: `konkordancia/UBS_DBH_jelentesek.tsv`, `UBS_DBH_referenciak.tsv`, `eszkozok/ubs_dbh_import.py`. Definíció és glossza fordítása a gyorsítótárból. Feltétel: az S0.1 igazolja a jelentésenkénti igehelyeket. |
| S6 | Mounce és SECE (a v2 G11-e, szűkítve) | **Mounce kiegészítő forrás:** `konkordancia/MCGED_teljes.tsv` a nyers SQLite-ból; GK-szám és tömör glossza. **SECE:** a megfelelő-lista a `SECE_G_teljes.tsv` / `SECE_H_teljes.tsv`-ből; az L–N-mező csak keresztellenőrzés az UBS DNTG ellen (eltérés = JELENTÉS). A Mounce szó szerinti megjelölése kötelező. |
| S7 | Cremer (görög teológiai szócikk) | **`konkordancia/Cremer_szocikkek.tsv`** (`lemma`, `strong`, `strong_parositas` = `auto`/`kezi`, `oldal`, `szoveg`, `allapot` = `nyers`/`javitott`/`jovahagyott`, `ocr_gyanus`), **szócikk-szinten, csak a motívumok tokenjeire** (ma 13 G), nem az egész kötet. Forrás: gépelt átirat (levendwater.org HTML); az archive.org OCR csak tartalék és keresztellenőrzés — a választást az S0.2 hibaaránya dönti el. A szócikk kulcsa (Strong, lemma) a saját adatból jön, nem a beolvasott szövegből. **OCR-kezelés:** a szövegben lévő görög és héber szavakat gépi ellenőrzés veti össze a lemmalistával (TBESG/TBESH); ami nem illeszkedik (vegyes írásrendszer, hiányzó ékezet, törött szó), `ocr_gyanus`. A kézi javítás soronként a `konkordancia/Cremer_javitasi_naplo.tsv`-be kerül (`lemma`, `eredeti`, `javitott`, `ok`). **A render csak `jovahagyott` szöveget használ; fordítás csak javított szövegből készül.** Párosítás lemma alapján. **`konkordancia/Cremer_heber_mutato.tsv`** (héber lemma → Cremer-szócikk). Render: szócikk-hivatkozás (oldal) + az első bekezdés, fordítás a gyorsítótárból, hiányzó fordításnál „*Fordítás függőben.*"; nincs szócikk: `a forrás nem tárgyalja`. |
| S8 | Girdlestone (héber teológiai szócikk) | **`konkordancia/Girdlestone_szocikkek.tsv`** (`fejezet`, `heber_lemma`, `strong`, `strong_parositas`, `oldal`, `szoveg`, `allapot`, `ocr_gyanus`), szócikk-szinten, csak a motívumok tokenjeire (ma 24 H). Forrás: gépelt átirat (preceptaustin.org PDF), tartalék az archive.org OCR — az S0.3 dönti el. OCR-kezelés, javítási napló (`konkordancia/Girdlestone_javitasi_naplo.tsv`) és render-szabály, mint az S7. A héber cella: Girdlestone + a Cremer héber mutatója; a TWOT-szám hivatkozásként marad. |
| S9 | BDB-etimológia (héber nyelvi háttér) | A `BDB_teljes_unabridged.tsv` szócikk-fejéből (a jelentésszámozás előtti rész) kivágott `nyelvi_hatter` mező a modellben. Feltétel: az S0.4 igazolja a kivághatóságot. |
| S10 | Hol jelennek meg az új források? | **A törzscikk 5. szakaszában** (szerep- és lefedettségi mátrix, a szó szócikk-blokkjában) **és a lexikonoldal 2. szakaszában** (generált sorok a szócikknél). Az ÓSZ-igehelyeknél az UBS DBH versenkénti jelentése az ÚSZ-oldali UBS DNTG mintájára. |
| S11 | Lábléc és kolofon (a pilot D12-je kiegészül) | Mounce (kötelező megjelölés), SECE, Cremer és Girdlestone (közkincs, kiadással), UBS DBH (CC BY-SA 4.0, a ©-mondat szó szerint). A ShareAlike a publikálást érinti (N11), a munkát nem blokkolja. |
| S13 | LXX-híd korpuszszinten | A motívum igehelyein túli, teljes LXX-re vonatkozó szóstatisztika (hányszor fordítja az LXX a héber szót az adott görög szóval) csak **versszintű együtt-előfordulásként** közelíthető (TAHOT-Strong × `LXX_OS`-Strong a párhuzamos versekben), mert az `LXX_OS` nem szóillesztett. Ha az S0.8 használhatónak méri: `konkordancia/LXX_versszintu_parok.tsv`, a mátrixban „versszintű együtt-előfordulás, nem szóillesztés" jelöléssel. Ha nem: a sor a motívum igehelyeire marad (ma is adatosítva). |
| S12 | ISTENTISZT-001 2/b (a v2 R2.4-e, most a tanulmányban) | Az S6 után a 2/b Mounce/SECE-táblái törlődnek a tanulmányból; a 2/b jelentőség-bekezdései (BDB 2.c/3 kiemelés, „√ unknown", a három ige kereszt-elemzése) a `miert_fontos` rés `#### H7121`, `#### H8034`, `#### G0994` alszakaszaiba kerülnek; a G0994-megjegyzés javítása. Ezzel teljesül a RENDER D7-je (a 2/b szétosztása a forrásban). |

---

## 3. Tételek

### S0 — kiegészítő felmérés *(csak olvas; egy commit)* ⛔

- **S0.1** `main` = `origin/main` = e brief commitja utáni állapot; a §0 0.2–0.12 újramérve. Eltérésnél **ÁLLJ**. Utána: UBS DBH JSON a 24 H-tokenre — jelentések száma, definíció, glossza, jelentésenkénti igehely-lista megléte. `naplok/SZOTAR_S0_ubs_dbh.tsv`.
- **S0.2** Cremer: szövegforrás-jelöltek (levendwater.org HTML, archive.org OCR) összevetése a 13 G-tokenen: hibaarány **külön a latin és külön a görög/héber betűs szövegre**, megmaradtak-e a görög betűk (vagy átírásra cserélődtek), szócikkhatárok; lefedettség a 13 G-tokenre. `naplok/SZOTAR_S0_cremer.tsv`. Ha a hálózat a letöltést nem engedi: **ÁLLJ** és jelents.
- **S0.3** Girdlestone: ugyanez a 24 H-tokenre (preceptaustin.org PDF, archive.org OCR), a héber betűk megmaradásával; a Cremer héber mutatójának lefedettsége a 24 H-tokenre. `naplok/SZOTAR_S0_girdlestone.tsv`.
- **S0.4** BDB-etimológia kivághatósága a 24 H-tokenen. `naplok/SZOTAR_S0_bdb_etim.tsv`.
- **S0.5** Kiejtés-tesztkészlet tisztítása: a 99 arany pár ellenőrzése + a 101 további pár besorolása (`valodi` / `hamis`). `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv`.
- **S0.6** Átírás-lista tisztítása: az `alak` kategória szétválasztása (`lxx_idezet`, `igeszoveg`, `egyeb`), a hamis találatok kiszűrése. `naplok/SZOTAR_S0_atirasok_tiszta.tsv` — ez az S2.1 mércéje.
- **S0.7** Héber kiejtés-jelöltek próbája: az OSHL `atiras` → magyaros jelöltszabályok egyezése a 49 arany héber párral (egyezik / eltér, eltérésenként ok). `naplok/SZOTAR_S0_heber_jeloltek.tsv`.
- **S0.8** LXX korpuszszint: a versszintű együtt-előfordulás próbája a motívum ismert párjain (pl. H7121 × G1941 az ISTENTISZT-001 LXX-sorain: visszaadja-e őket, és mennyi a zaj). `naplok/SZOTAR_S0_lxx_versszint.tsv`.
- **S0.9** Jelentés: `naplok/SZOTAR_S0_jelentes.md`, a kérdések egy csokorban. **ÁLLJ.**

### 1. menet — nulla-diff

- **S1.1** Fordítási gyorsítótár (S1): migráció 51 sorral; a generátor innen olvas; SEMA-bejegyzés; a régi oszlop és tábla megszűnik.
- **S1.2** `terminologia.tsv` (S2), `kiejtes_szabalyok.tsv`, `kiejtes_kivetelek.tsv` (S3); SEMA-bejegyzések. A `kiejtes_kivetelek.tsv` induló sorai közé átkerül a `torzscikk_general.py` kódbeli `KIEJT` táblájának 5 szava (SBL → magyaros, ISTENTISZT-001); a kódbeli tábla itt még marad (nulla-diff).
- **S1.3** `eszkozok/kiejtes.py`: görög átírás; `--ellenoriz` mód a tisztított tesztkészleten. Nem ír.
- **S1.4** Importok a `konkordancia/` alá, README-vel és licenccel: `TBESH_konszolidalt.tsv` (S4), `UBS_DBH_*` (S5), `MCGED_teljes.tsv` (S6), `Cremer_szocikkek.tsv`, `Cremer_heber_mutato.tsv` (S7), `Girdlestone_szocikkek.tsv` (S8), és ha az S0.8 engedi, `LXX_versszintu_parok.tsv` (S13). A generátor még nem olvassa őket.
- **S1.4b** Cremer és Girdlestone: OCR-ellenőrzés (`ocr_gyanus`), kézi javítás a javítási naplóba, `allapot` → `javitott`. Összesítő: `naplok/SZOTAR_S1_ocr.tsv` (szócikkenként gyanús tételek, javítások száma).
- **S1.5** `ellenoriz.py`: **13.** gyorsítótár (kulcs egyedi, `forras_hash` egyezik; eltérés = SÉRTÉS, `allapot` → `elavult` javaslat; terminológia-verzió elmaradás = JELENTÉS); **14.** kiejtés és terminológia (JELENTÉS).
- **S1.6** Dokumentáció: `adat/SEMA.md`, `konkordancia/README.md`, `NYITOTT_FELADATOK.md`.
- **S1.7** Héber kiejtés-jelöltek a 8 motívum 24 lemmájára (S3): `naplok/SZOTAR_S1_heber_jeloltek.tsv`. Nem ír a kivételtáblába.
- **ÁLLJ — jóváhagyás:** a javított Cremer- és Girdlestone-szócikkek (`javitott` → `jovahagyott`) és a 24 héber kiejtés-jelölt. A jóváhagyott állapot és a jóváhagyott jelöltek a 2. menet első commitjában kerülnek be.

### 2. menet — kimenet-változtató, elvárt diffel

- **S2.1** A jóváhagyott állapot rögzítése (Cremer/Girdlestone `jovahagyott`; a 24 héber lemma a `kiejtes_kivetelek.tsv`-be). Görög kiejtés a generált blokkokban (lemma és alak), a tisztított átírás-lista szerint; héber lemma a kivétel-táblából. **A `torzscikk_general.py` kódbeli `KIEJT` táblája megszűnik**: a törzscikk is a `kiejtes.py`-ból és a kivételtáblából olvas, így a 8 törzscikk egységesen magyaros átírást kap (a pilot D10 konvenciója). Előfeltétel: 100%-os görög egyezés.
- **S2.2** TBESH: átállás a konszolidált táblára (S4).
- **S2.3** UBS DBH a lexikonoldalba és a törzscikkbe (S5, S10).
- **S2.4** Mounce és SECE (S6); a Mounce angol glosszáinak fordítása a gyorsítótárból; a 2/b-ben meglévő 3 magyar glossza `kezi` sorként átkerül.
- **S2.5** Cremer, Girdlestone (csak `jovahagyott` szöveg), BDB-etimológia (S7–S9, S10); ha az S1.4 importálta, az LXX versszintű párok (S13).
- **S2.6** ISTENTISZT-001 2/b a tanulmányban (S12).
- **S2.7** `szotar_szerepek.tsv` `allapot` frissítése; lábléc és kolofon (S11).
- **S2.8** Újragenerálás (`lexikon` és `torzscikk`), diff-osztályozó kategóriák: `kiejtes`, `tbesh`, `ubs_dbh`, `mounce_sece`, `teologiai`, `nyelvi_hatter`, `lxx_korpusz`, `tanulmany`, `licenc`, `szerep`. Ismeretlen kategória: **ÁLLJ**.
- **S2.9** Lezárás: `NYITOTT_FELADATOK.md` (fordítási pipeline, BDB SQLite-csere, héber gépi kiejtés, a 12 Thayer-szócikk és a Cremer/Girdlestone-szövegek fordítása, Trench), `MUNKAMENET.md`.

---

## 4. Várt számok

| Menet | Mérés | Várt |
|---|---|---|
| S0 | kiejtés-tesztkészlet | 99 arany pár ellenőrizve; a 101 további pár besorolva |
| S0 | átírás-lista | a 936 tétel besorolva; a tisztított darabszám jelentve |
| S0 | Cremer / Girdlestone | forrásonkénti hibaarány, külön latin és görög/héber betűs szövegre; lefedettség 13 G / 24 H |
| S0 | héber kiejtés-jelöltek | egyezés a 49 arany párral jelentve |
| 1 | Cremer- és Girdlestone-szócikkek | mind `javitott`, a gyanús tételek mind kezelve (javítva vagy indokoltan elfogadva) |
| 1 | héber kiejtés-jelöltek | 24 |
| 1 | `--cel lexikon --ir` és `--cel torzscikk --ir` után `git status --porcelain lexikon/` | üres |
| 1 | `adat/forditasok.tsv` | 51 sor, mind `kezi` |
| 1 | `kiejtes.py --ellenoriz` | görög egyezési arány jelentve (cél 100%; alatta a kivételtábla bővítése jóváhagyásra) |
| 1 | `konkordancia/` új táblák | 7 (az S13-mal 8) + 2 javítási napló, mind README- és licenc-bejegyzéssel |
| 2 | diff-osztályozó | ismeretlen kategória: 0; a `kiejtes` kategória tételei = a tisztított átírás-lista görög tételei + a kivételtábla héber lemmái |
| 2 | `szotar_szerepek.tsv` | 20 sor, `nincs adatosítva`: 0 |
| 2 | `kiejtes_kivetelek.tsv` | a 8 motívum 24/24 héber lemmája |
| 2 | a renderben használt Cremer/Girdlestone-szöveg | csak `jovahagyott` |
| 2 | törzscikkek lefedettségi mátrixa | `nincs adatosítva`: 0 |
| 2 | `ellenoriz.py` | SÉRTÉS 0, kód 0 |

---

## 5. Elfogadási kritériumok

### S0
| # | Kritérium |
|---|---|
| K1 | a §0 minden sora jelentve; eltérésnél megállás |
| K2 | a nyolc munkalap és a jelentés megvan; a kérdések egy listában |
| K3 | az éles `adat/`, `lexikon/`, `tematikus_lezart/`, `konkordancia/` bájtra változatlan |

### 1. menet
| # | Kritérium |
|---|---|
| K4 | nulla-diff a `lexikon/` egészén (lexikonoldal és törzscikk) |
| K5 | `forditasok.tsv` 51 sor, kulcs egyedi, hash egyezik; a régi oszlop és tábla nincs |
| K6 | az új adattáblák SEMA-bejegyzéssel; a `kiejtes.py` nem ír |
| K7 | az importált táblák reprodukálhatók (importszkript + forrás-SHA a README-ben); a Cremer/Girdlestone javításai a naplóból visszakövethetők |
| K7b | a jóváhagyás előtt a kivételtáblába és `jovahagyott` állapotba nem került semmi |
| K8 | TSV-kezelés `csv` modul nélkül; commitok a §6 szerint; `git status --porcelain` üres |

### 2. menet
| # | Kritérium |
|---|---|
| K9 | S2.1 csak 100%-os görög egyezés után futott; `grep -c KIEJT eszkozok/torzscikk_general.py` = 0 |
| K10 | diff-osztályozó: ismeretlen kategória 0; a kategóriák darabszáma jelentve |
| K11 | a lábléc és a kolofon az S11 szerint, a Mounce és az UBS megjelölése szó szerint |
| K12 | az ISTENTISZT-001 2/b rése csak prózát tartalmaz; a jelentőség-bekezdések a `miert_fontos` alatt |
| K13 | `ellenoriz.py` SÉRTÉS 0, kód 0; a törzscikkekben `nincs adatosítva` 0 |
| K14 | commitok a §6 szerint; `git status --porcelain` üres |

---

## 6. Commitok

**S0**
| Üzenet | Fájlok |
|---|---|
| `S0: felmérés — UBS DBH, Cremer, Girdlestone, BDB-etimológia, tisztított tesztkészlet és átírás-lista` | `naplok/SZOTAR_S0_*.tsv`, `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv`, `naplok/SZOTAR_S0_jelentes.md` |

**1. menet**
| Üzenet | Fájlok |
|---|---|
| `S1.1–S1.2: fordítási gyorsítótár, terminológia, kiejtés-táblák` | `adat/forditasok.tsv`, `adat/terminologia.tsv`, `adat/kiejtes_szabalyok.tsv`, `adat/kiejtes_kivetelek.tsv`, `adat/lexikon_hivatkozasok.tsv`, `adat/forditas_ubs.tsv` (törlés), `adat/SEMA.md`, `eszkozok/lexikon_general.py` |
| `S1.3: kiejtes.py` | `eszkozok/kiejtes.py` |
| `S1.4: szótári importok` | `konkordancia/TBESH_konszolidalt.tsv`, `konkordancia/UBS_DBH_*.tsv`, `konkordancia/MCGED_teljes.tsv`, `konkordancia/Cremer_*.tsv`, `konkordancia/Girdlestone_*.tsv`, `konkordancia/LXX_versszintu_parok.tsv` (ha van), importszkriptek, `konkordancia/README.md` |
| `S1.4b: Cremer és Girdlestone OCR-javítás` | `konkordancia/Cremer_szocikkek.tsv`, `konkordancia/Girdlestone_szocikkek.tsv`, `konkordancia/*_javitasi_naplo.tsv`, `naplok/SZOTAR_S1_ocr.tsv` |
| `S1.5–S1.7: ellenőrző 13–14. szakasz, dokumentáció, héber kiejtés-jelöltek` | `eszkozok/ellenoriz.py`, `adat/SEMA.md`, `NYITOTT_FELADATOK.md`, `adat/kiejtes_heber_jeloltszabalyok.tsv`, `naplok/SZOTAR_S1_heber_jeloltek.tsv` |

**2. menet**
| Üzenet | Fájlok |
|---|---|
| `S2.1: jóváhagyott szócikkek és héber kiejtések; görög kiejtés a generált blokkokban` | `konkordancia/Cremer_szocikkek.tsv`, `konkordancia/Girdlestone_szocikkek.tsv`, `adat/kiejtes_kivetelek.tsv`, `eszkozok/lexikon_general.py`, `eszkozok/kiejtes.py`, `lexikon/*` |
| `S2.2–S2.5: TBESH, UBS DBH, Mounce/SECE, Cremer, Girdlestone, BDB-etimológia a renderben` | `eszkozok/lexikon_general.py`, `eszkozok/torzscikk_general.py`, `adat/forditasok.tsv`, `lexikon/*` |
| `S2.6–S2.7: ISTENTISZT-001 2/b a tanulmányban, szerepmátrix, lábléc` | `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`, `adat/szotar_szerepek.tsv`, `eszkozok/*_general.py`, `lexikon/*` |
| `S2.8–S2.9: diff-osztályozó és lezárás` | `eszkozok/render_diff_osztalyoz.py`, `naplok/SZOTAR_S2_diff.tsv`, `NYITOTT_FELADATOK.md`, `MUNKAMENET.md` |

---

## 7. Nyitó promptok *(Sonnet)*

### S0
```
Olvasd el a CLAUDE.md-t, a SZOTAR_BRIEF.md-t teljes egészében, a RENDER_BRIEF.md
v3 G6-ját és a naplok/RENDER_R0_jelentes.md-t.

0. Ellenőrizd, hogy a RENDER_BRIEF 2. menete lezárult (NYITOTT_FELADATOK.md). Ha nem, ÁLLJ MEG.
1. S0.1: mérd újra a §0 tábláját. Ha bármi eltér, ÁLLJ MEG és jelents.
2. S0.1–S0.8 a §3 szerint. Az éles adat/, lexikon/, tematikus_lezart/, konkordancia/
   könyvtárba NE írj. Ha egy letöltést a hálózat nem enged, ÁLLJ MEG és jelents.
3. S0.9: jelentés, a kérdések egy listában. Commit a §6 szerint. K1–K3.
4. ÁLLJ.
```

### 1. menet
```
Olvasd el a CLAUDE.md-t, a SZOTAR_BRIEF.md-t (a jóváhagyott verziót) és a
naplok/SZOTAR_S0_jelentes.md-t.

0. main = origin/main = <az S0 utáni hash>. Ha nem, ÁLLJ MEG.
1. S1.1–S1.2. Utána: general.py --cel lexikon --ir és --cel torzscikk --ir, majd
   git status --porcelain lexikon/ — ha nem üres, ÁLLJ MEG, és ne commitolj.
2. S1.3–S1.7 a §3 szerint, minden tétel után újra a nulla-diff próba.
3. K4–K8. Commitok a §6 1. menet-táblája szerint.
4. ÁLLJ: mutasd be a javított Cremer/Girdlestone-szócikkeket (az ocr_gyanus
   tételekkel és a javítási naplóval) és a 24 héber kiejtés-jelöltet jóváhagyásra.
```

### 2. menet
```
Olvasd el a CLAUDE.md-t és a SZOTAR_BRIEF.md-t (a jóváhagyott verziót).

0. main = origin/main = <az 1. menet utáni hash>. Ha nem, ÁLLJ MEG.
1. S2.1 csak a jóváhagyott szócikkekkel és kiejtés-jelöltekkel, és csak ha a
   kiejtes.py --ellenoriz görög egyezése 100%; ha nem, ÁLLJ MEG.
2. S2.2–S2.7, majd S2.8: ha a diff-osztályozó ismeretlen kategóriát talál, ÁLLJ MEG.
3. S2.9. K9–K14. Commitok a §6 2. menet-táblája szerint.
4. ÁLLJ.
```

---

## 8. Döntésnapló

| # | Döntés | Indoklás |
|---|---|---|
| D1 | A szótári adatréteg külön briefben, a RENDER lezárása után | RENDER v3 D13: a 8 oldal lezárása nem várhat a TBESH-kérdésre; mindkét brief a `general.py`-t és a 8 oldalt módosítja, ezért sorrendben, nem párhuzamosan |
| D2 | A felmérés az R0.3–R0.6 munkalapjaira épül, az S0 csak az új forrásokat méri | a kiejtés-tesztkészlet, az átírás-leltár, a forrás-összevetés és a volumen már megvan |
| D3 | TBESH: unió, nem csere (S4) | R0: 9 tokennél a `.txt`, 13-nál a `.lexicon` bővebb; egyik sem tartalmazza a másikat, csere tartalomvesztés volna |
| D4 | Az átírás-élesítés mércéje a tisztított tételes lista, nem a darabszám (S3) | a 859 és a 936 eltérése módszertani; az `alak` kategória zajos (LXX-idézet és igeszöveg nincs szétválasztva) |
| D5 | Kiejtés-aranykészlet: a 99 pár az ISTENTISZT-001 kézi szövegéből (S3) | emberi, ellenőrzött szöveg; a regex-kinyerés többi párja zajos |
| D6 | Az UBS-pár a szerepmátrix gerince: UBS DNTG ↔ UBS DBH (S5) | ugyanaz a projekt és licenc; a héber JSON már letöltve, eddig csak a doménjei importálva; a TAHOT és az OSHL kiesett |
| D7 | A Mounce kiegészítő forrás, a SECE L–N keresztellenőrzés (S6) | az UBS DNTG jelentésenként adja a Louw–Nida-számot, a glosszát és az előfordulást |
| D8 | Görög teológiai szócikk: Cremer (S7) | közkincs (1895); a TDNT a Cremer átdolgozásaként indult; klasszikus → LXX → ÚSZ útvonal, mint a projekt LXX-hídja |
| D9 | Héber teológiai szócikk: Girdlestone + a Cremer héber mutatója; a TWOT-szám csak hivatkozás (S8) | a TWOT szövege jogvédett, a repóban csak a száma van; a Girdlestone közkincs, tematikus, LXX-en át az ÚSZ-hez köt |
| D10 | Héber nyelvi háttér: BDB-etimológia (S9) | a görög LSJ klasszikus hátterének héber megfelelője a rokon nyelvi anyag, amelyet a BDB szócikk-feje hordoz |
| D11 | A hiányzó forrásszócikk jelölése `a forrás nem tárgyalja`, nem `—` | a Cremer és a Girdlestone csak teológiai szavakat tárgyal; a hiány érdemi adat, nem adathiány |
| D12 | Cremer és Girdlestone: gépelt átirat az OCR helyett, szócikk-szintű import csak a motívumok tokenjeire, `ocr_gyanus` jelölés, javítási napló, a render csak `jovahagyott` szöveget használ, és ⛔ jóváhagyás a render előtt (S7, S8) | az OCR a görög és héber betűs részeknél megbízhatatlan (az archive.org Cremer-OCR görögje olvashatatlan); néhány tucat szócikk kézzel ellenőrizhető; a kulcs a saját adatból jön; a fordítás csak javított szövegből készülhet, hogy a hiba ne terjedjen a gyorsítótárba |
| D13 | Héber kiejtés: OSHL-alapú jelöltek, kézi jóváhagyás, cél 24/24 lemma (S3) | a tudományos átírásban a nehéz esetek (hangzó svá, dagesh, qamets qatan) már eldöntöttek, ezért jelöltnek megbízható; a render továbbra sem generál héber kiejtést (RENDER v2 D6) |
| D14 | LXX-híd korpuszszinten csak versszintű együtt-előfordulásként, mérés után, jelölve (S13) | az `LXX_OS` nem szóillesztett; a motívum igehelyeire vonatkozó LXX-híd már adatosítva van (RENDER G6, D19) |
| D15 | A törzscikk kódbeli `KIEJT` táblája (a RENDER 1. menetében került be, 5 szó, csak az ISTENTISZT-001-re) az S1.2-ben a kivételtáblába költözik, az S2.1-ben megszűnik | adat nem lehet a kódban; a RENDER 1. menete után a 8 törzscikk vegyes átírást mutat (az ISTENTISZT-001 magyaros, a többi tudományos), ez a SZOTAR 2. menetével egységesül, `kiejtes` diff-kategóriában |
