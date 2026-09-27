# SZOTAR_BRIEF.md — szótári adatréteg: szerepmátrix-források, fordítási gyorsítótár, kiejtés

*FELADATOK #5 (és a #9 előkészítése) · v1 — 2026.09.23 · a `RENDER_BRIEF.md` v3 kettéválásából (ott D13); OCR-kezelés (D12), héber kiejtés-jelöltek (D13), LXX-korpuszszint (D14) · KIEJT-kiváltás (D15) · v1.1 — 2026.09.25: a Cremer kivezetve (D16); forrásszabály (D17) · **v1.2 — 2026.09.27: a Girdlestone kivezetve (D18); a TWOT-szám marad a héber 3. szerepben (D19); a 3. szerep új jelöltje az unfoldingWord Translation Words (S14, D20); az S0 kérdései lezárva (D21–D24); FJ-eredmény: a Macula küszöb alatt, az S13 versszintű marad (D25); a pilot terminológiája a kiinduló tábla (D26); új `allapot`-érték: `nincs forrás` (D27). Az S0 lefutott (`1046834`); új, rövid S0b-mérés ⛔. **v1.3 — 2026.09.27: az
S0b.1 megállt, majd a felhasználó jóváhagyta a hatókör-bővítést — a T2.2
(`ed79575`) két új héber tokenje (H8414 *tohu*, H0922 *bohu*) bekerül a
hatókörbe, a héber tokenszám 24→26 (D28); hatókör-szabály rögzítve (D28).***

**Cél.** A szerepmátrix (`adat/szotar_szerepek.tsv`, 10 szerep × 2 nyelv) minden cellája adatból
töltődjön, és a szótári réteg rendezett legyen: fordítási gyorsítótár, terminológia, görög kiejtés,
a TBESH egyesítése, az UBS DBH teljes importja, a Mounce/SECE, a BDB-etimológia, a TWOT-szám a
mátrixban, és — ha az S0b igazolja — a Translation Words a teológiai szócikk szerepben. A végén a
8 törzscikk 5. szakaszában nincs `nincs adatosítva` cella; ahol a szerepnek nincs forrása, ott
`nincs forrás` áll (D27).

**Előfeltétel:** a FELADATOK #1 (Károli-kulcs, `4b9ae49`), #2 (CI), #3 (fordítási próba, `9eb43fe`)
és #4 (karbantartás, `8ff7c71`) a `main`-ben. A `RENDER_BRIEF.md` 2. menete lezárva.

**Szerkezet.** S0 (lefutott) → **S0b kiegészítő mérés ⛔** → 1. menet: nulla-diff ⛔ →
2. menet: kimenet-változtató.

**Modell:** Sonnet. **Push csak külön kérésre.** Minden menet utolsó commitja frissíti a
`FELADATOK.md` #5 sorát (a 2. menet a #9-et is).

**Nincs benne:** fordítási pipeline élesítése (`eszkozok/fordit.py` éles futtatása = FELADATOK #7),
BDB SQLite-csere, héber gépi kiejtés, Trench, Girdlestone (D18), LXX-fordítói döntések a 87 függő
igehelyre (FELADATOK #8).

---

## 0. Kiindulás *(az S0b.1 újraméri; eltérésnél ÁLLJ — a hatókör-szabályt l. D28)*

*A 0.2–0.11 és 0.13–0.14 sor értéke 2026.09.27-én a `9eb43fe`-n újramérve, egyezik a v1-gyel.
Az S0b.1 (`3b8976b`, `70eb29c`-n) újramért mindent; a 0.4 sor eltért (l. D28) — a
felhasználó jóváhagyása után a tábla ezt a bővített hatókört (26 H-token) tükrözi.*

**Hatókör-szabály (D28):** a szótári réteg héber hatóköre a menet indító commitjának
tokenhalmaza; a szám ebből származik, nem rögzített. Ha a mérés és az indítás között a
halmaz változik, az új tokenek bekerülnek, és a jelentés felsorolja őket. Megállás csak
akkor kell, ha token kiesik, vagy a G-halmaz változik.

| # | Mérés | Érték |
|---|---|---|
| 0.1 | `main` = `origin/main` | `70eb29c` (az S0b.1 indító hash-e; vagy e brief commitja utáni hash) |
| 0.2 | `adat/lexikon_hivatkozasok.tsv` | 24 sor (Thayer 14, BDB 4, TBESG 4, TBESH 1, LSJ 1); `forditas_hu` kitöltve: 11 |
| 0.3 | `adat/forditas_ubs.tsv` | 20 sor; `definicio_hu` 20, `glosszak_hu` 20 |
| 0.4 | token a 8 motívum előfordulásaiban | **H 26, G 13** (a T2.2 `ed79575` két új héber tokent adott: H8414 *tohu*, H0922 *bohu* — 1Móz 1:2, TEREMT-001; D28) |
| 0.5 | TBESH: `.txt` bővebb / `.lexicon` bővebb / kb. egyenlő (26 H-token) | 9 / 13 / 2 a régi 24 tokenen; **a 2 új token (H8414, H0922) lefedettsége az S1.4-nél mérendő** |
| 0.6 | MCGED lefedettség (13 G-token) | 13/13 — a G-halmaz nem változott |
| 0.7 | SECE (13 G-token) | 13/13; `LN:`, `GK:`, `Hebrew:` almező gépileg kinyerhető — a G-halmaz nem változott |
| 0.8 | kiejtés-tesztkészlet | 200 pár (görög 112, héber 88); aranykészlet 99 (görög 50, héber 49); a tisztított változat: `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv` (a 101 további pár: 87 `valodi`, 14 `hamis`, automata triázs) |
| 0.9 | átírás-leltár | 936 tétel; a tisztított változat: `naplok/SZOTAR_S0_atirasok_tiszta.tsv` (`alak`: lxx_idezet 347, igeszoveg 386, egyeb 163) |
| 0.10 | nyers SQLite | `MCGED.lexicon` 10 666 sor; `TBESH.lexicon` 9 888 sor (az R0.1 mérése) |
| 0.11 | UBS DBH forrás | `UBSHebrewDic-v0.9.2-en.JSON`, SHA-256 a `konkordancia/SDBH_SDGNT_README.md`-ben; a (régi) 24 H-token mindegyikénél van jelentés, definíció, glossza és jelentésenkénti igehely-lista (S0.1); **a 2 új tokenre nincs még ellenőrizve** |
| 0.12 | `szotar_szerepek.tsv` | 20 sor: `adatosítva` 11, `nincs adatosítva` 9 — görög 3, 7, 10; héber 3, 5, 7, 8, 9, 10 |
| 0.13 | LXX-híd adata | `konkordancia/LXX_OS/*.tsv` (CC BY 4.0), versszintű; a KK7.5 után újragenerálva, `sha256(verse_pairs.jsonl)=3a91c571…2e985`; `adat/lxx_dontesek.tsv` |
| 0.14 | héber tudományos átírás és TWOT-szám | `konkordancia/OSHL_lexikalis_index.tsv` (`twot`, `atiras` mező; 10 225 sor); a TWOT-számot a `lexikon_general.py` (`oshl_twot_ehhez`) már rendereli a lexikonoldalon |
| 0.15 | grammatikai Strong-lista | `adat/grammatikai_strongok.tsv`: 85 sor (H 54, G 31) |
| 0.16 | a fordítási próba terminológiája | `naplok/FORDITAS_P_terminologia.tsv`: 13 sor (`angol`, `magyar`, `megjegyzes`, `verzio`) |
| 0.17 | a fordítási próba kimenet-sémája | `eszkozok/fordit.py` `KIMENET_FEJLEC` = az S1 gyorsítótár oszlopai (FORDITAS_PILOT G1) |
| 0.18 | szószintű MT–LXX-illesztés (FJ1) | Macula Hebrew 78,3% (115-ből 90), CenterBLC/MT-LXX 78,9% — mindkettő a 90%-os küszöb alatt (`naplok/FORRAS_jelentes.md`) |

---

## 1. Fogalmak

- **Fordítási gyorsítótár:** `adat/forditasok.tsv`, minden magyar fordítás egyetlen helye, forrás-hash-sel.
- **Adatosítva:** a szerep cellája a `konkordancia/` vagy az `adat/` egy importált, verziózott táblájából töltődik.
- **Nincs forrás** *(v1.2, D27)*: a szerepnek az adott nyelven nincs a D17-nek megfelelő forrása. Végleges állapot, nem pótlandó hiány.
- **Cella-értékek a törzscikk lefedettségi mátrixában:** forrás-hivatkozás; `a forrás nem tárgyalja` (a forrásban nincs szócikk — érdemi adat); `nincs forrás` (D27); `—` csak ott, ahol a szerep az adott nyelven nem értelmezett.
- **Nulla-diff:** `git status --porcelain lexikon/` üres az `--ir` után.

---

## 2. S-döntések *(jóváhagyásra; a v1.2 új vagy módosított sorai **félkövérrel** jelölt számúak)*

| # | Kérdés | Javaslat |
|---|---|---|
| **S1** | Fordítási gyorsítótár | **`adat/forditasok.tsv`**, oszlopok: `szotar`, `strong`, `entry_id`, `jelentes_szam`, `mezo`, `forras_hash`, `forditas_hu`, `allapot`, `modell`, `datum`, `terminologia_verzio` — azonos az `eszkozok/fordit.py` kimenet-sémájával (0.17). Kulcs: `szotar+strong+entry_id+jelentes_szam+mezo`. `forras_hash` = a forrásszöveg SHA-1-e. Migráció: 11 lexikon-fordítás + 20 UBS-definíció + 20 UBS-glossza = **51 sor**, `allapot=kezi`. A `lexikon_hivatkozasok.forditas_hu` oszlop és a `forditas_ubs.tsv` megszűnik. A próba kimenete (`naplok/FORDITAS_P3_kimenet.tsv`) **nem** kerül be: az éles fordítás a FELADATOK #7 dolga. |
| **S2** | Terminológia | **`adat/terminologia.tsv`** (`angol`, `magyar`, `megjegyzes`, `verzio`); induló sorok: **a `naplok/FORDITAS_P_terminologia.tsv` 13 sora változatlanul** (D26). Az `ellenoriz.py` csak jelent; a CI E10 hatóköre a táblát már lefedi (CI D17). |
| S3 | Kiejtés és átírás | **Görög: szabálytábla (`adat/kiejtes_szabalyok.tsv`) + `eszkozok/kiejtes.py`.** Héber: a render nem generál; lemma-kiejtés csak a kézi `adat/kiejtes_kivetelek.tsv`-ből. **Héber jelöltek:** az OSHL `atiras` mezőjéből szabálytábla (`adat/kiejtes_heber_jeloltszabalyok.tsv`) ad magyaros jelöltet; csak kézi jóváhagyás után kerül a kivételtáblába. **Cél: a 8 motívum 26/26 héber lemmája a kivételtáblában (D28: H8414, H0922 is a hatókörben).** Az alakszint marad STEP-átírás. **Tesztkészlet: a D23 szerint.** **Az élesítés mércéje** a tisztított átírás-lista (`naplok/SZOTAR_S0_atirasok_tiszta.tsv`) tételei; a 936 ellenőrző összeg. Élesítés feltétele: a görög aranykészlet 100%-os egyezése. |
| S4 | TBESH | **Unió, nem csere:** `konkordancia/TBESH_konszolidalt.tsv` a `.lexicon` strukturált mezőivel és a `.txt` teljes szövegével; szócikkenként a teljesebb szöveg, a forrás soronként jelölve (`forras` = `txt` / `lexicon`). Addig a render a mai `.txt`-ből dolgozik. |
| S5 | UBS DBH | **Teljes import a meglévő JSON-ból**, az `ubs_dntg_import.py` mintájára: `konkordancia/UBS_DBH_jelentesek.tsv`, `UBS_DBH_referenciak.tsv`, `eszkozok/ubs_dbh_import.py`. Definíció és glossza fordítása a gyorsítótárból. Az S0.1 igazolta a jelentésenkénti igehelyeket (0.11). |
| S6 | Mounce és SECE | **Mounce kiegészítő forrás:** `konkordancia/MCGED_teljes.tsv` a nyers SQLite-ból; GK-szám és tömör glossza. **SECE:** a megfelelő-lista a `SECE_G_teljes.tsv` / `SECE_H_teljes.tsv`-ből; az L–N-mező csak keresztellenőrzés az UBS DNTG ellen (eltérés = JELENTÉS). A Mounce szó szerinti megjelölése kötelező. |
| S7 | Cremer — **kivezetve (D16)** | Nincs import és nincs render. A görög 3. szerep forrása az S14 szerint. A `CREMER_OCR_BRIEF.md` (v3, lezárva) és az S0.2 munkalapja naplóként marad. |
| **S8** | Girdlestone — **kivezetve (D18)**; **TWOT-szám (D19)** | A Girdlestone nem kerül importra és renderre. Az S0.3 munkalapja (`naplok/SZOTAR_S0_girdlestone.tsv`) naplóként marad. **A héber 3. szerep TWOT-száma** a `konkordancia/OSHL_lexikalis_index.tsv` `twot` mezőjéből (0.14) jön, csak hivatkozásként (a D17 kivétele); a törzscikk 5. szakaszában is megjelenik. |
| S9 | BDB-etimológia (héber nyelvi háttér) | A `BDB_teljes_unabridged.tsv` szócikk-fejéből kivágott `nyelvi_hatter` mező. **A határ a D21 szerint (a régi 24 tokenre):** 14 tokennél gépi (em dash + „1 ” minta), 4 tokennél (H0430, H3678, H8004, H8034) kézi határ a `konkordancia/BDB_etimologia_kezi_hatarok.tsv`-ben, ⛔ jóváhagyással; 6 tokennél (H0779, H2555, H5303, H6093, H7496, H7497) `a forrás nem tárgyalja`. **D28 miatt a H8414 és a H0922 határ-besorolása az S1.4-nél mérendő és e 3 kategória valamelyikébe kerül** (vagy — ha a BDB szócikk nem tárgyalja — a szerepmátrixban ez a hiány rögzítendő, nem megállási ok). |
| S10 | Hol jelennek meg az új források? | **A törzscikk 5. szakaszában** (szerep- és lefedettségi mátrix) **és a lexikonoldal 2. szakaszában** (generált sorok a szócikknél). Az ÓSZ-igehelyeknél az UBS DBH versenkénti jelentése az ÚSZ-oldali UBS DNTG mintájára. |
| **S11** | Lábléc és kolofon | Mounce (kötelező megjelölés), SECE, UBS DBH (CC BY-SA 4.0, a ©-mondat szó szerint), TWOT (csak a szám, a mű megnevezésével), **és ha az S0b elfogadja: Translation Words** — CC BY-SA 4.0; a származékos műből az unfoldingWord® védjegyet el kell hagyni, a módosítást jelezni kell, és a forrásmegjelölés szó szerint: „The original work by unfoldingWord is available from unfoldingword.org/utw”. A ShareAlike a publikálást érinti (N11), a munkát nem blokkolja. |
| S12 | ISTENTISZT-001 2/b | Az S6 után a 2/b Mounce/SECE-táblái törlődnek a tanulmányból; a jelentőség-bekezdések a `miert_fontos` rés `#### H7121`, `#### H8034`, `#### G0994` alszakaszaiba kerülnek; a G0994-megjegyzés javítása. Ezzel teljesül a RENDER D7-je. |
| **S13** | LXX-híd korpuszszinten | **Versszintű együtt-előfordulás marad** (D25: a szószintű illesztés jelöltjei, a Macula és a CenterBLC, a küszöb alatt). Alap: a KK7.5 utáni `LXX_OS` (0.13) × TAHOT, **grammatikai szűréssel** az `adat/grammatikai_strongok.tsv` 31 G-sora alapján (D24). Ha az S0b.3 használhatónak méri: `konkordancia/LXX_versszintu_parok.tsv`, a mátrixban „versszintű együtt-előfordulás, nem szóillesztés” jelöléssel. Ha nem: a sor a motívum igehelyeire marad (ma is adatosítva). |
| **S14** | Teológiai szócikk (3. szerep, mindkét nyelv): **unfoldingWord Translation Words (tW)** | Nyílt (CC BY-SA 4.0) angol fogalomszótár, a `kt` (kulcsfogalmak) és `other` alkönyvtárral; ÓSZ és ÚSZ egyaránt. **Az S0b.2 dönt:** nyelvenként elfogadva, ha a motívumtokenek legalább felét Strong-számon át lefedi (G ≥ 7/13, H ≥ 13/26, D28) — a küszöb a ⛔-nél módosítható. Elfogadás esetén: `konkordancia/tW_szocikkek.tsv` (`tw_id`, `kategoria`, `cim`, `strong`, `szoveg`, `forras_commit`), a teljes `kt` + `other` állomány (nem csak a motívumtokenek), a README-ben commit, sha256 és szó szerinti licencidézet. A render a Thayer-sorok mintáját követi: az angol szöveg mellé a magyar fordítás a gyorsítótárból jön; ha még nincs, a cella `fordításra vár` jelölést kap. Elutasítás esetén az adott nyelv 3. szerepe: görögül `nincs forrás`; héberül csak a TWOT-szám (S8). |

---

## 3. Tételek

### S0 — kiegészítő felmérés *(lefutott, `1046834`; nem fut újra)*

Eredmény: `naplok/SZOTAR_S0_jelentes.md` és 8 munkalap. A 7 kérdés válasza: 1. Cremer → D16;
2. Girdlestone-URL → tárgytalan (D18); 3. BDB-határ → D21; 4. tesztkészlet-sortörés → D22;
5. a 101 pár triázsa → D23; 6. héber jelöltpróba → D24; 7. LXX-zaj → D24, D25.

### S0b — kiegészítő mérés *(csak olvas; egy commit)* ⛔

- **S0b.1** `main` = `origin/main`; a §0 0.2–0.18 újramérve. Eltérésnél **ÁLLJ**.
- **S0b.2** Translation Words (S14): letöltés a `git.door43.org/unfoldingWord/en_tw` legutóbbi kiadásából (tag, commit, sha256, a `LICENSE.md` szó szerint). Mérés: (a) hordoz-e a szócikk Strong-számot (melyik mezőben, milyen formában); (b) a 13 G- és 26 H-tokenből (D28) hánynak van szócikke, alkönyvtáranként (`kt` / `other`); (c) szócikkenként a szöveg hossza; (d) 3 minta szócikk szövege a munkalapon. `naplok/SZOTAR_S0b_tw.tsv`. **Ha a hálózat a letöltést nem engedi: ÁLLJ** — a mérés ekkor helyi gépen fut (mint az FJ 2. menete).
- **S0b.3** LXX versszint újramérve a KK7.5 utáni `LXX_OS`-en, **grammatikai szűréssel** (0.15): H7121 × G1941 és × G2564 (az LD001/LD002 próbakő), a zaj aránya szűrés előtt és után. `naplok/SZOTAR_S0b_lxx_versszint.tsv`.
- **S0b.4** Jelentés: `naplok/SZOTAR_S0b_jelentes.md` — az S14 küszöbének eredménye nyelvenként, az S13 döntése, kérdések egy listában. `FELADATOK.md` #5 sor frissítése. **ÁLLJ.**

### 1. menet — nulla-diff

- **S1.1** Fordítási gyorsítótár (S1): migráció 51 sorral; a generátor innen olvas; SEMA-bejegyzés; a régi oszlop és tábla megszűnik.
- **S1.2** `terminologia.tsv` (S2, a pilot 13 sorával), `kiejtes_szabalyok.tsv`, `kiejtes_kivetelek.tsv` (S3); SEMA-bejegyzések. A `kiejtes_kivetelek.tsv` induló sorai közé átkerül a `torzscikk_general.py` kódbeli `KIEJT` táblájának 5 szava; a kódbeli tábla itt még marad (nulla-diff).
- **S1.3** `eszkozok/kiejtes.py`: görög átírás; `--ellenoriz` mód a tesztkészleten (D23). Nem ír.
- **S1.4** Importok a `konkordancia/` alá, README-vel és licenccel: `TBESH_konszolidalt.tsv` (S4), `UBS_DBH_jelentesek.tsv` és `UBS_DBH_referenciak.tsv` (S5), `MCGED_teljes.tsv` (S6), `BDB_etimologia_kezi_hatarok.tsv` (S9, `allapot=javaslat`); ha az S0b elfogadta: `tW_szocikkek.tsv` (S14) és `LXX_versszintu_parok.tsv` (S13). A generátor még nem olvassa őket.
- **S1.5** `ellenoriz.py`: **13.** gyorsítótár (kulcs egyedi, `forras_hash` egyezik; eltérés = SÉRTÉS, `allapot` → `elavult` javaslat; terminológia-verzió elmaradás = JELENTÉS); **14.** kiejtés és terminológia (JELENTÉS).
- **S1.6** Dokumentáció: `adat/SEMA.md` (a `szotar_szerepek.allapot` zárt listája kiegészül a `nincs forrás` értékkel, D27), `konkordancia/README.md`, `NYITOTT_FELADATOK.md`.
- **S1.7** Héber kiejtés-jelöltek a 8 motívum 26 lemmájára (D28: a T2.2 két új tokenjével bővítve), az OSHL `atiras` mezőjéből (S3, D24): `naplok/SZOTAR_S1_heber_jeloltek.tsv`, a 26 lemmán mért egyezési aránnyal. Nem ír a kivételtáblába.
- **ÁLLJ — jóváhagyás:** a 26 héber kiejtés-jelölt és a (legfeljebb 6, D28 miatt esetleg bővülő) kézi BDB-etimológia-határ (`javaslat` → `jovahagyott`). A jóváhagyott értékek a 2. menet első commitjában kerülnek be. `FELADATOK.md` #5 sor frissítése.

### 2. menet — kimenet-változtató, elvárt diffel

- **S2.1** A jóváhagyott értékek rögzítése (26 héber lemma a `kiejtes_kivetelek.tsv`-be, D28; a BDB-határ `jovahagyott` sorai a S1.7/S9 szerinti végleges darabszámmal). Görög kiejtés a generált blokkokban (lemma és alak), a tisztított átírás-lista szerint; héber lemma a kivételtáblából. **A `torzscikk_general.py` kódbeli `KIEJT` táblája megszűnik.** Előfeltétel: 100%-os görög egyezés az aranykészleten.
- **S2.2** TBESH: átállás a konszolidált táblára (S4).
- **S2.3** UBS DBH a lexikonoldalba és a törzscikkbe (S5, S10).
- **S2.4** Mounce és SECE (S6); a Mounce angol glosszáinak fordítása a gyorsítótárból; a 2/b-ben meglévő 3 magyar glossza `kezi` sorként átkerül.
- **S2.5** Teológiai szócikk (S14: tW, ha elfogadva; TWOT-szám a törzscikkben, S8), BDB-etimológia (S9, csak gépi és `jovahagyott` határ), LXX versszintű párok (S13, ha importálva).
- **S2.6** ISTENTISZT-001 2/b a tanulmányban (S12).
- **S2.7** `szotar_szerepek.tsv`: `allapot` és `forras` frissítése (a 3. sor mindkét nyelven az S0b eredménye szerint; D27); lábléc és kolofon (S11).
- **S2.8** Újragenerálás (`lexikon` és `torzscikk`), diff-osztályozó kategóriák: `kiejtes`, `tbesh`, `ubs_dbh`, `mounce_sece`, `teologiai`, `nyelvi_hatter`, `lxx_korpusz`, `tanulmany`, `licenc`, `szerep`. Ismeretlen kategória: **ÁLLJ**. Ezzel eltűnik a 8 törzscikk régi Cremer/Girdlestone-sora (CI E11, CI D12).
- **S2.9** Lezárás: `NYITOTT_FELADATOK.md` (fordítási pipeline = #7, BDB SQLite-csere, héber gépi kiejtés, a 12 Thayer-szócikk és — ha elfogadva — a tW-szócikkek fordítása, Trench; javaslat: a CI E11 kiterjesztése a Girdlestone-ra), `MUNKAMENET.md`, `FELADATOK.md` #5 és #9 sora.

---

## 4. Várt számok

| Menet | Mérés | Várt |
|---|---|---|
| S0b | §0 újramérés | 0.2–0.18 egyezik |
| S0b | tW-lefedettség | nyelvenként jelentve (G …/13, H …/26, D28), a Strong-kötés módja leírva |
| S0b | LXX versszint | a zaj aránya szűrés előtt és után; H7121 × G1941 és × G2564 visszaadva |
| 1 | héber kiejtés-jelöltek | 26 (D28), egyezési arány jelentve |
| 1 | BDB-etimológia határ | gépi 14, kézi javaslat 4, `a forrás nem tárgyalja` 6 a régi 24 tokenen (D21); a H8414/H0922 besorolása az S1.4-nél jelentve, összesen legfeljebb 26 |
| 1 | `--cel lexikon --ir` és `--cel torzscikk --ir` után `git status --porcelain lexikon/` | üres |
| 1 | `adat/forditasok.tsv` | 51 sor, mind `kezi` |
| 1 | `adat/terminologia.tsv` | 13 sor |
| 1 | `kiejtes.py --ellenoriz` | görög egyezés az aranykészleten (50 pár) jelentve; cél 100% |
| 1 | `konkordancia/` új táblák | 5 (TBESH, UBS DBH ×2, MCGED, BDB-határ), + tW és LXX-párok, ha az S0b elfogadta (legfeljebb 7), mind README- és licenc-bejegyzéssel |
| 2 | diff-osztályozó | ismeretlen kategória: 0 |
| 2 | `szotar_szerepek.tsv` | 20 sor; `nincs adatosítva`: 0; `nincs forrás`: legfeljebb 1 (görög 3, ha a tW görögül elutasítva) |
| 2 | `kiejtes_kivetelek.tsv` | a 8 motívum 26/26 héber lemmája (D28) |
| 2 | törzscikkek lefedettségi mátrixa | `nincs adatosítva`: 0; Cremer- és Girdlestone-említés: 0 |
| 2 | `ellenoriz.py` és CI | SÉRTÉS 0, kód 0; a CI zöld |

---

## 5. Elfogadási kritériumok

### S0b
| # | Kritérium |
|---|---|
| K1 | a §0 minden sora jelentve; eltérésnél megállás |
| K2 | a tW-munkalapon URL, tag/commit, sha256 és szó szerinti licencidézet; a számok szkriptből, a szkript megnevezve |
| K3 | az éles `adat/`, `lexikon/`, `tematikus_lezart/`, `konkordancia/` bájtra változatlan |

### 1. menet
| # | Kritérium |
|---|---|
| K4 | nulla-diff a `lexikon/` egészén |
| K5 | `forditasok.tsv` 51 sor, kulcs egyedi, hash egyezik; a régi oszlop és tábla nincs |
| K6 | az új adattáblák SEMA-bejegyzéssel; a `nincs forrás` érték a SEMA-ban; a `kiejtes.py` nem ír |
| K7 | az importált táblák reprodukálhatók (importszkript + forrás-SHA a README-ben) |
| K7b | a jóváhagyás előtt a kivételtáblába és `jovahagyott` állapotba nem került semmi |
| K8 | TSV-kezelés `csv` modul nélkül; commitok a §6 szerint; `git status --porcelain` üres; a CI zöld |

### 2. menet
| # | Kritérium |
|---|---|
| K9 | S2.1 csak 100%-os görög egyezés után futott; `grep -c KIEJT eszkozok/torzscikk_general.py` = 0 |
| K10 | diff-osztályozó: ismeretlen kategória 0; a kategóriák darabszáma jelentve |
| K11 | a lábléc és a kolofon az S11 szerint, a Mounce, az UBS és (ha van) a tW megjelölése szó szerint; az unfoldingWord® védjegy a származékos szövegben nem szerepel |
| K12 | az ISTENTISZT-001 2/b rése csak prózát tartalmaz; a jelentőség-bekezdések a `miert_fontos` alatt |
| K13 | `ellenoriz.py` SÉRTÉS 0, kód 0; a törzscikkekben `nincs adatosítva` 0; a CI E11 a `lexikon/`-on 0 |
| K14 | commitok a §6 szerint; `git status --porcelain` üres |

---

## 6. Commitok

**S0b**
| Üzenet | Fájlok |
|---|---|
| `S0b: kiegészítő mérés — Translation Words, LXX versszint grammatikai szűréssel` | `naplok/SZOTAR_S0b_*.tsv`, `naplok/SZOTAR_S0b_jelentes.md`, a mérőszkriptek a `naplok/` alatt, `FELADATOK.md` |

**1. menet**
| Üzenet | Fájlok |
|---|---|
| `S1.1–S1.2: fordítási gyorsítótár, terminológia, kiejtés-táblák` | `adat/forditasok.tsv`, `adat/terminologia.tsv`, `adat/kiejtes_szabalyok.tsv`, `adat/kiejtes_kivetelek.tsv`, `adat/lexikon_hivatkozasok.tsv`, `adat/forditas_ubs.tsv` (törlés), `adat/SEMA.md`, `eszkozok/lexikon_general.py` |
| `S1.3: kiejtes.py` | `eszkozok/kiejtes.py` |
| `S1.4: szótári importok` | `konkordancia/TBESH_konszolidalt.tsv`, `konkordancia/UBS_DBH_*.tsv`, `konkordancia/MCGED_teljes.tsv`, `konkordancia/BDB_etimologia_kezi_hatarok.tsv`, `konkordancia/tW_szocikkek.tsv` (ha van), `konkordancia/LXX_versszintu_parok.tsv` (ha van), importszkriptek, `konkordancia/README.md` |
| `S1.5–S1.7: ellenőrző 13–14. szakasz, dokumentáció, héber kiejtés-jelöltek` | `eszkozok/ellenoriz.py`, `adat/SEMA.md`, `NYITOTT_FELADATOK.md`, `adat/kiejtes_heber_jeloltszabalyok.tsv`, `naplok/SZOTAR_S1_heber_jeloltek.tsv`, `FELADATOK.md` |

**2. menet**
| Üzenet | Fájlok |
|---|---|
| `S2.1: jóváhagyott kiejtések és BDB-határok; görög kiejtés a generált blokkokban` | `adat/kiejtes_kivetelek.tsv`, `konkordancia/BDB_etimologia_kezi_hatarok.tsv`, `eszkozok/lexikon_general.py`, `eszkozok/torzscikk_general.py`, `eszkozok/kiejtes.py`, `lexikon/*` |
| `S2.2–S2.5: TBESH, UBS DBH, Mounce/SECE, teológiai szócikk, BDB-etimológia a renderben` | `eszkozok/lexikon_general.py`, `eszkozok/torzscikk_general.py`, `adat/forditasok.tsv`, `lexikon/*` |
| `S2.6–S2.7: ISTENTISZT-001 2/b a tanulmányban, szerepmátrix, lábléc` | `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`, `adat/szotar_szerepek.tsv`, `eszkozok/*_general.py`, `lexikon/*` |
| `S2.8–S2.9: diff-osztályozó és lezárás` | `eszkozok/render_diff_osztalyoz.py`, `naplok/SZOTAR_S2_diff.tsv`, `NYITOTT_FELADATOK.md`, `MUNKAMENET.md`, `FELADATOK.md` |

---

## 7. Nyitó promptok *(Sonnet)*

### S0b
```
Olvasd el a CLAUDE.md-t, a FELADATOK.md-t és a SZOTAR_BRIEF.md-t (v1.2) teljes egészében,
valamint a naplok/SZOTAR_S0_jelentes.md-t.

0. main = origin/main. Új ág a main-ről. Push a távoli ágra ugyanebben a lépésben.
1. S0b.1: mérd újra a §0 tábláját. Ha bármi eltér, ÁLLJ MEG és jelents.
2. S0b.2–S0b.3 a §3 szerint. Az éles adat/, lexikon/, tematikus_lezart/, konkordancia/
   könyvtárba NE írj. Ha egy letöltést a hálózat nem enged, ÁLLJ MEG és jelents.
3. S0b.4: jelentés, a kérdések egy listában; a FELADATOK.md #5 sorának frissítése
   (csak a saját sor). Commit a §6 szerint. K1–K3.
4. ÁLLJ.
```

### 1. menet
```
Olvasd el a CLAUDE.md-t, a SZOTAR_BRIEF.md-t (a jóváhagyott verziót) és a
naplok/SZOTAR_S0b_jelentes.md-t.

0. main = origin/main = <az S0b utáni hash>. Ha nem, ÁLLJ MEG. Push a távoli ágra.
1. S1.1–S1.2. Utána: general.py --cel lexikon --ir és --cel torzscikk --ir, majd
   git status --porcelain lexikon/ — ha nem üres, ÁLLJ MEG, és ne commitolj.
2. S1.3–S1.7 a §3 szerint, minden tétel után újra a nulla-diff próba.
   Az S14 és az S13 importja csak akkor, ha az S0b jelentése és a jóváhagyás elfogadta.
3. K4–K8. Commitok a §6 1. menet-táblája szerint; a FELADATOK.md #5 sora.
4. ÁLLJ: mutasd be a 26 héber kiejtés-jelöltet (D28) és a kézi BDB-etimológia-határokat jóváhagyásra.
```

### 2. menet
```
Olvasd el a CLAUDE.md-t és a SZOTAR_BRIEF.md-t (a jóváhagyott verziót).

0. main = origin/main = <az 1. menet utáni hash>. Ha nem, ÁLLJ MEG. Push a távoli ágra.
1. S2.1 csak a jóváhagyott kiejtés-jelöltekkel és BDB-határokkal, és csak ha a
   kiejtes.py --ellenoriz görög egyezése 100%; ha nem, ÁLLJ MEG.
2. S2.2–S2.7, majd S2.8: ha a diff-osztályozó ismeretlen kategóriát talál, ÁLLJ MEG.
3. S2.9. K9–K14. Commitok a §6 2. menet-táblája szerint; a FELADATOK.md #5 és #9 sora.
4. ÁLLJ.
```

---

## 8. Döntésnapló

| # | Döntés | Indoklás |
|---|---|---|
| D1 | A szótári adatréteg külön briefben, a RENDER lezárása után | RENDER v3 D13: mindkét brief a `general.py`-t és a 8 oldalt módosítja, ezért sorrendben |
| D2 | A felmérés az R0.3–R0.6 munkalapjaira épül, az S0 csak az új forrásokat méri | a kiejtés-tesztkészlet, az átírás-leltár, a forrás-összevetés és a volumen már megvan |
| D3 | TBESH: unió, nem csere (S4) | 9 tokennél a `.txt`, 13-nál a `.lexicon` bővebb; csere tartalomvesztés volna |
| D4 | Az átírás-élesítés mércéje a tisztított tételes lista, nem a darabszám (S3) | az `alak` kategória zajos volt (az S0.6 szétválasztotta) |
| D5 | Kiejtés-aranykészlet: a 99 pár az ISTENTISZT-001 kézi szövegéből (S3) | emberi, ellenőrzött szöveg |
| D6 | Az UBS-pár a szerepmátrix gerince: UBS DNTG ↔ UBS DBH (S5) | ugyanaz a projekt és licenc |
| D7 | A Mounce kiegészítő forrás, a SECE L–N keresztellenőrzés (S6) | az UBS DNTG jelentésenként adja a Louw–Nida-számot, a glosszát és az előfordulást |
| D8 | *(visszavonva: D16)* Görög teológiai szócikk: Cremer | — |
| D9 | *(visszavonva: D18; a TWOT-rész a D19-ben él tovább)* Héber teológiai szócikk: Girdlestone | — |
| D10 | Héber nyelvi háttér: BDB-etimológia (S9) | a görög LSJ klasszikus hátterének héber megfelelője a BDB szócikk-fejének rokon nyelvi anyaga |
| D11 | A hiányzó forrásszócikk jelölése `a forrás nem tárgyalja`, nem `—` | a szelektív források (tW, BDB-etimológia) hiánya érdemi adat, nem adathiány |
| D12 | *(visszavonva: D16, D18)* Cremer- és Girdlestone-szöveg OCR-kezelése, javítási napló | — |
| D13 | Héber kiejtés: OSHL-alapú jelöltek, kézi jóváhagyás, cél 24/24 lemma (S3) | a tudományos átírásban a nehéz esetek már eldöntöttek; a render nem generál héber kiejtést |
| D14 | LXX-híd korpuszszinten csak versszintű együtt-előfordulásként, mérés után, jelölve (S13) | az `LXX_OS` nem szóillesztett |
| D15 | A törzscikk kódbeli `KIEJT` táblája az S1.2-ben a kivételtáblába költözik, az S2.1-ben megszűnik | adat nem lehet a kódban |
| D16 | A Cremer kivezetve (S7) | A felhasználó döntése, 2026.09.25 (`CREMER_OCR_BRIEF.md` v3, D20–D22) |
| D17 | Forrásszabály: csak saját repóban tárolható és onnan renderelhető forrás; kivétel a TWOT-szám | A felhasználó döntése, 2026.09.25 |
| **D18** | **A Girdlestone kivezetve:** sem szövegként, sem hivatkozásként nem kerül a szótári rétegbe; a D9 és a D12 Girdlestone-része, az S0.3 és az S1.4b visszavonva | A felhasználó döntése, 2026.09.27. Az S0.3 mérése (13/24 lefedés, valódi héber betűk) naplóként marad |
| **D19** | **A TWOT-szám marad a héber 3. szerepben** (nem kerül át az 5.-be), forrása az OSHL-index `twot` mezője | A felhasználó döntése (marad), 2026.09.27; a helyére a chat javaslata: a TWOT teológiai szótár, a száma teológiai szócikkre mutat; az 5. szerep a tömör jelentésé és az előfordulásé. A szám már adat (0.14), így a H3 akkor sem üres, ha a tW nem válik be |
| **D20** | **A 3. szerep jelöltje mindkét nyelven az unfoldingWord Translation Words, mérés után (S14, S0b.2)** | CC BY-SA 4.0 (ugyanaz a ShareAlike, mint az UBS-nél, a D17-nek megfelel); ÓSZ és ÚSZ egyaránt, így szimmetrikus. Kockázat: fordítóknak készült, rövid szócikkek; a Strong-kötés még nincs igazolva. Elvetett alternatívák: Tyndale Open Bible Dictionary (fogalomszerű, nem Strong-kulcsos; a licenc nincs igazolva), Trench (csak görög, a Girdlestone műfaja), Vine's (csak görög; az ÓSZ-rész jogvédett), ISBE 1915 (enciklopédia, Strong-leképezés nélkül) |
| **D21** | **BDB-etimológia (S0 3. kérdés):** 14 token gépi határ, 4 token (H0430, H3678, H8004, H8034) kézi határ ⛔ jóváhagyással, 6 token `a forrás nem tárgyalja` | az S0.4 szerint a 4 tokennél érdemi rokon-nyelvi anyag van, csak a határ mintázata eltér; kézzel olcsóbb, mint általános regexet írni |
| **D22** | **A kiejtés-tesztkészlet sortörése (S0 4. kérdés):** a `naplok/RENDER_kiejtes_tesztkeszlet.tsv` változatlan marad (napló); a mérce a tisztított `SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv` | naplót nem írunk utólag; a tisztított fájl már helyes |
| **D23** | **Tesztkészlet (S0 5. kérdés):** az élesítés kapuja csak a 99 pár aranykészlet (görögből 50, 100%); a 87 automatán `valodi` pár csak JELENTÉS, a 14 `hamis` kizárva | az automata triázs nem kézi ellenőrzés, ezért kapuként nem használható |
| **D24** | **Héber jelöltpróba és LXX-zaj (S0 6. és 7. kérdés):** az 55,6%-os próba nem mérföldkő; az S1.7 méri újra a 24 lemma OSHL-átírásán. Az LXX versszint zajszűrése a meglévő `grammatikai_strongok.tsv` G-soraival (31) az S0b.3-ban | az S0.7 más szavakon és más alapanyagon mért; a grammatikai lista már létezik, nem kell új |
| **D25** | **Az S13 versszintű marad** | FJ1: a Macula Hebrew (78,3%) és a CenterBLC/MT-LXX (78,9%) a 90%-os küszöb alatt; a CenterBLC-nek licence sincs. A Macula a jobb jelölt, ha puhább küszöbbel újramérik (`naplok/FORRAS_jelentes.md`); az 1–2Sám, 1–2Kir, 1–2Krón nincs benne |
| **D26** | **A terminológia induló sorai a fordítási próba 13 sora** (`naplok/FORDITAS_P_terminologia.tsv`), nem a v1 3 sora | a próba a 3 sort már tartalmazza, és a rövidítés-feloldásokat a G1941-arany igazolta; így a #7 éles fordítása ugyanazzal a táblával indul |
| **D27** | **Új `allapot`-érték a szerepmátrixban: `nincs forrás`** (a SEMA zárt listája bővül) | a görög 3. szerep (és a tW elutasítása esetén más cella) hiánya végleges, nem pótlandó; a `nincs adatosítva` ígéretet sugallna. A FELADATOK-ban a cél „`nincs adatosítva` 0” így mérhető marad |
| **D28** | **Hatókör-szabály + a T2.2 két új héber tokenje (H8414 tohu, H0922 bohu) bekerül a szótári réteg hatókörébe; a héber tokenszám 24→26.** Szabály: „A hatókör a menet indító commitjának tokenhalmaza; a szám ebből származik, nem rögzített. Ha a mérés és az indítás között a halmaz változik, az új tokenek bekerülnek, és a jelentés felsorolja őket. Megállás csak akkor kell, ha token kiesik, vagy a G-halmaz változik.” Ha a tohu/bohu valamelyik forrásban (pl. UBS DBH, TBESH) nem szerepel, azt a szerepmátrix `a forrás nem tárgyalja` hiányként rögzíti — ez nem megállási ok. | A felhasználó döntése, 2026.09.27, az S0b.1 ÁLLJ-jára válaszul (`naplok/SZOTAR_S0b_jelentes.md`): a T2.2 (`ed79575`, 2026.09.25) az S0 (09.23) után, de a jóváhagyás előtt bővítette az `elofordulasok.tsv`-t; a felhasználó a szűkítés helyett a bővítést választotta, és a jövőre nézve rögzítette, hogy a token-alapú célszámok a menet indításakori tényleges hatókört tükrözzék, ne egy korábban rögzített konstanst |

*A v1.1 → v1.2 változásai:* fejléc, cél, előfeltétel; §0 újramérve, 0.12 pontosítva, 0.13–0.18 új/bővített; §1 `nincs forrás`; S1, S2, S8, S9, S11, S13 módosítva, S14 új; S0b új menet (S0 lezárva); S1.4b törölve; 1. menet ⛔ tárgya: kiejtés + BDB-határ (Girdlestone helyett); §4–§7 ennek megfelelően; D9, D12 visszavonva, D18–D27 új.

*A v1.2 → v1.3 változásai:* fejléc (S0b.1 ÁLLJ + hatókör-döntés); §0 hatókör-szabály és 0.1/0.4/0.5/0.11/0.17 frissítve (26 H-token, `KIMENET_FEJLEC`); S3, S9, S14 a 26-os hatókörre igazítva; §3 S1.7, az ÁLLJ-sor és S2.1 24→26; §4 Várt számok a tW-küszöb, a héber kiejtés-jelöltek és a `kiejtes_kivetelek.tsv` sora 26-ra; §7 1. menet prompt ÁLLJ-sora 26-ra; D28 új.
