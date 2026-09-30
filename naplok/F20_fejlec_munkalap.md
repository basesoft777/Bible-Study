# F20 B2 — fejléc-munkalap ⛔ (jóváhagyásra vár)

*2026.09.30 · alap: `origin/main` = `29ada3c`, `FELADATOK.md` v1.1 (nem v1.3 — l. `naplok/F20_B0_felmeres.md` 1/1) · forrás: a briefek szövege, a B0 felmérés, a FELADATOK v1.1 táblái és „Kész” listája. **Semmi nincs fejlécbe commitolva, semmi nincs átnevezve.***

Jelölések: **[javaslat]** = a brief szövege nem mond róla semmit, a B2 becslése; ezt külön jóvá kell hagyni. `—` = elhagyva (régi fejléc, 4.5).

## 0. Döntést igénylő kérdések (előbb ezek)

| # | Kérdés | Javaslat |
|---|---|---|
| Q1 | A v1.3 tábla a repóban nincs; a #16–#19 nem létezik. Az állapotot a v1.1-ből és a „Kész” listából veszem. | Elfogadni. A K6/B8 szövegében a „v1.3”/„#16–#19” a v1.1-re értendő; a B8 PR-leírásba a #16–#19 mondat is bekerül. |
| Q2 | Az **E17** név foglalt (DONTESEK DT3, F15 brief 3.4: sorszám-változás küszöb, nyitott). | A feladatkövető CI-szabály neve **E18**; E17 marad a DT3-é. |
| Q3 | Feladat nélküli (régi) briefek fejléce (D31-jelölt): `tipus: archiv`, `feladat` nélkül; kötelező `cim`, `modell`, `allapot: lezarva`; a generátor nem teszi táblába; az `ellenoriz` ezt külön kezeli (**már implementálva** a B1-ben). | Elfogadni. |
| Q4 | A „Kész” listában szám nélküli tételek (FJ 1. menet, TEREMT-002 1–2. lépés, Szótári brief v1.1) nem generálhatók (D32-jelölt). | A FELADATOK.md-ben kézi „Korábbi, szám nélküli lezárt tételek” szakasz, a mai sorok szó szerint; a generált „Kész” csak számozottat ad. |
| Q5 | A feladat nélküli briefek **neve nem változik** (a B0 1/4 és 5. pontja szerint); csak fejlécet kapnak. Ide tartozik az `F4_…`–`F8_BRIEF.md` is (az `F<nn>_` minta kétjegyű számot vár, ezeket az `ellenoriz` nem fogja számozottnak tekinteni). | Elfogadni. |
| Q6 | A három Károli-kulcs brief egy feladat (#1), de a szám egyedi: a fő brief kapja a számot, a KK7 és a KK75 archív marad. | Elfogadni. |
| Q7 | A lezárt számozott briefek `olvas`/`ir` mezője: a lezárt feladat sem függést, sem ütközést nem okoz (4.2/4.3 csak nyitottakra számít), a szövegből kinyert lista hibára ad okot, értéket nem. | **Elhagyni** a lezártaknál (régi fejléc), kitölteni csak a nyitott #9-re és #20-ra; a #7 stub listája [javaslat] (2/C). |
| Q8 | #12: a `TEREMT002_KUTATAS_BRIEF.md` csak a T1–T2-t írja le (lefutott, szám nélkül); a T3-hoz nincs brief. | A fájl **archív**, a #12 külön `brief_kell` stubot kap (`forras: TEREMT002_KUTATAS_BRIEF.md`). (A brief 7. pontja a #12-t a T3-hoz köti; ez a T3 tényleges hiányát is jelzi.) |
| Q9 | A stubok `modell` mezője kötelező, de a brief még nincs meg. | Javaslat az 2/B táblában; pontosítás a tényleges brief megírásakor. |
| Q10 | A `FELADATOK.md` #12 sorában „D29” a SZOTAR-brief saját D-sorozatára utal. | A generált sorban a `kovetkezo` mezőbe `SZOTAR-D29`-ként kerül. |

## 1. Briefek (minden meglévő `*_BRIEF.md`)

Oszlopok: jelenlegi → új név · `feladat` · `tipus` · `fazis` · `allapot` · `modell` · nyitó prompt jelölendő (szakasz) · megjegyzés. `olvas`/`ir`: 2. szakasz, máshol `—`.

### A) Számozott feladatok, meglévő briefből

| Jelenlegi → új | # | tipus | fazis | allapot | modell | Nyitó prompt jelölése | Megj. |
|---|---|---|---|---|---|---|---|
| `KAROLI_KULCS_BRIEF.md` → `F01_KAROLI_KULCS_BRIEF.md` | 1 | feladat | 1 | lezarva | sonnet (régi sor) | 6. (1b), 7. (1., archív) | kód: `KK`; `fugg` nincs |
| `CI_ELLENORZES_BRIEF.md` → `F02_CI_ELLENORZES_BRIEF.md` | 2 | feladat | 1 | lezarva | sonnet | „Nyitó prompt” (5. sor) | kód: `CI` |
| `FORDITAS_PILOT_BRIEF.md` → `F03_FORDITAS_PILOT_BRIEF.md` | 3 | feladat | 1 | lezarva | sonnet | 6. | kód: `FP` |
| `KARBANTARTAS_BRIEF.md` → `F04_KARBANTARTAS_BRIEF.md` | 4 | feladat | 1 | lezarva | sonnet | 6. | kód: `KB`; `fugg: [2]` (brief: #2 merge-e kell) |
| `SZOTAR_BRIEF.md` → `F05_SZOTAR_BRIEF.md` | 5 | feladat | 1 | lezarva | sonnet | 7. (S0, 1., 2. menet) | kód: `SZOTAR S1`; `fugg: [1, 2, 3, 4]` (brief 48. sor: #1–#4) |
| `F06_FORRASFELMERES_BRIEF.md` (marad) | 6 | feladat | 1 | lezarva | sonnet | „Nyitó prompt” (108. sor) | `fugg` nincs |
| `F15_ORKESZTRATOR_BRIEF.md` (marad) | 15 | feladat | folyamat | lezarva | sonnet | 0. | `fugg` nincs |
| `F20_BEFOGADAS_BRIEF.md` (marad) | 20 | feladat | folyamat | fut (a menet 1. commitjában) | sonnet | már jelölt | már új fejlécű |

### B) Számozott feladatok, új csonk-brief (a meglévő szövegből nem képezhető)

| Új fájl | # | tipus | fazis | allapot | modell | `forras` | Megj. |
|---|---|---|---|---|---|---|---|
| `F07_THAYER_ELES_BRIEF.md` | 7 | feladat | 1 | brief_kell | `külső:gemini-3.1-flash-lite` [javaslat: FP2-D13 szerint] | — (a `FORDITAS_ELES_THAYER_BRIEF.md` v2 csak chatben van) | `fugg: [3, 5, 14]` (kész) |
| `F08_LXX_DONTESEK_BRIEF.md` | 8 | feladat | 1 | brief_kell | opus [javaslat: kutatói ítélet, FELADATOK 3. pont] | — | `fugg: [1, 6]` (kész) |
| `F09_SZOTAR_S2_BRIEF.md` | 9 | feladat | 2 | nem_indult (brief megvan) | sonnet | `F05_SZOTAR_BRIEF.md#2. menet` | `olvas`/`ir`: 2/A |
| `F10_LEXIKON_LEZARAS_BRIEF.md` | 10 | feladat | 2 | brief_kell | [javaslat: opus; L6/L7 döntés] | — | |
| `F11_MIGRACIO_BRIEF.md` | 11 | feladat | 2 | brief_kell | [javaslat: sonnet] | — | |
| `F12_TEREMT002_PROZA_BRIEF.md` | 12 | feladat | 2 | brief_kell | [javaslat: opus; a T1–T2 brief opus] | `TEREMT002_KUTATAS_BRIEF.md` | Q8 |
| `F13_GENEZIS_KIADAS_BRIEF.md` | 13 | feladat | 2 | brief_kell | [javaslat: sonnet] | — | |
| `F14_FP2_STILUSPROBA_BRIEF.md` | 14 | feladat | 1 | lezarva | sonnet [javaslat] | `naplok/FP2_jelentes.md` | csak a „Kész” lista miatt kell |

A csonkok törzse 3–6 sor: cím, a v1.1 sor tartalma (mit ad, függés), a `forras`-ra mutató hivatkozás. A csonk sem hajt végre, sem nyitó promptot nem tartalmaz.

### C) Feladat nélküli briefek (nem kapnak számot, nem változik a nevük; `tipus: archiv`, `allapot: lezarva`)

| Fájl | modell | Nyitó prompt jelölése | Megj. |
|---|---|---|---|
| `KAROLI_KULCS_KK7_BRIEF.md` | sonnet (régi sor) | 6. | a #1 része (Q6) |
| `KAROLI_KULCS_KK75_BRIEF.md` | sonnet (régi sor) | 6., 7. (merge-prompt) | a #1 része |
| `FORRASJELOLTEK_BRIEF.md` | sonnet (régi sor) | 6. | FJ 1. menet; a #6 előzménye |
| `TEREMT002_KUTATAS_BRIEF.md` | opus (régi sor) | 6. | T1–T2 (Q8) |
| `CREMER_OCR_BRIEF.md` | sonnet [javaslat] | 7. | |
| `ISTENTISZT_V3_BRIEF.md` | sonnet [javaslat] | nincs | |
| `LEX_BRIEF.md` | sonnet [javaslat] | 8. | |
| `LEXV2_1_BRIEF.md` | sonnet [javaslat] | nincs | |
| `LEXV2_2_BRIEF.md` | sonnet [javaslat] | nincs | |
| `N12_BRIEF.md` | sonnet (törzs: „Sonnet”) [javaslat] | 8. | |
| `N14_BRIEF.md` | sonnet (törzs: „Sonnet”) [javaslat] | 8. | |
| `N16_BRIEF.md` | sonnet [javaslat] | nincs | |
| `RENDER_BRIEF.md` | sonnet (régi sor) | 7. | |
| `SDBH_IMPORT_BRIEF.md` | sonnet (törzs: „Sonnet”) [javaslat] | 7.1, 7.2 | |
| `F4_BRIEF.md` | sonnet [javaslat] | 6.3–6.5 | terv-F4 fázis, nem #4 |
| `F4_GENERATOR_BRIEF.md` | sonnet [javaslat] | 6.3–6.6 | |
| `F5_BRIEF.md` | sonnet [javaslat] | 6.1–6.2 | |
| `F6_BRIEF.md` | sonnet [javaslat] | 8.1–8.3 | |
| `F7_BRIEF.md` | sonnet [javaslat] | 7. | |
| `F8_BRIEF.md` | sonnet [javaslat] | 7., 7b, 7c | |

A `modell` az archív briefeknél csak a fejléc-kötelezettség miatt kell; a „régi sor” jelzésű helyeken az `ellenoriz` egyezést vár. A „[javaslat]” soroknál a törzsben nincs `Modell:` sor, tehát nincs mivel ütköznie.

A nyitó prompt jelölése: csak a felsorolt szakaszok köré kerül a `<!-- KOZVETLEN_FUTTATAS -->` … `<!-- /KOZVETLEN_FUTTATAS -->` pár (menetenként külön-külön, ahol több van); a szöveg nem változik.

## 2. `olvas` / `ir` a nyitott feladatokra

### A) #9 (F09, forrás: `SZOTAR_BRIEF.md` 2. menet, S2.1–S2.9)

- `olvas`: [adat/forditasok.tsv, adat/terminologia.tsv, adat/kiejtes_kivetelek.tsv, konkordancia/, lexikon/]
- `ir`: [lexikon/, adat/kiejtes_kivetelek.tsv, adat/szotar_szerepek.tsv, eszkozok/torzscikk_general.py, eszkozok/lexikon_general.py, eszkozok/render_diff_osztalyoz.py, MUNKAMENET.md, NYITOTT_FELADATOK.md]
- (`NYITOTT_FELADATOK.md` és `adat/szotar_szerepek.tsv` közös koordinációs fájl, a számításból kiesik; a listában a szövegbeli teljesség miatt szerepel.)

### B) #20 (már a fejlécében van)

- `olvas`: [FELADATOK.md, DONTESEK.md, CLAUDE.md, NYITOTT_FELADATOK.md, "*_BRIEF.md", .claude/commands/, .github/workflows/]
- `ir`: [eszkozok/feladatok.py, eszkozok/teszt_feladatok.py, "*_BRIEF.md", BRIEF_SABLON.md, beerkezo/, FELADATOK.md, CLAUDE.md, .claude/commands/, .github/workflows/]

### C) #7 csonk [javaslat, chatben lévő brief hiányában a FELADATOK v1.1 sorából és a SZOTAR S1 eredményeiből]

- `olvas`: [adat/terminologia.tsv, adat/kiejtes_kivetelek.tsv, konkordancia/Thayer_teljes.tsv]
- `ir`: [adat/forditasok.tsv]
- Indok: a #9 (S2) a fordítási gyorsítótárat (`adat/forditasok.tsv`) olvassa; a #7 (Thayer-fordítás) írja. Ez adja a v1.1-ből ismert #9→#7 függést levezetve.
- A #8, #10–#13 stubnak nincs `olvas`/`ir`-je (régi fejléc, 4.5): csomagba nem kerülhet, a függésüket a `fugg` adja.

## 3. Függések összevetése (v1.1 kézi ↔ levezetett)

| # | v1.1 „Függ ettől” | Megoldás a fejlécben | Levezetve? | Eltérés |
|---|---|---|---|---|
| 7 | #3, #5, #14 (kész) | `fugg: [3, 5, 14]` | — (mind lezárt) | megjelenés: „#3 (kész), #5 (kész), #14 (kész)” |
| 8 | #1, #6 | `fugg: [1, 6]` | — (lezártak) | megjelenés: „(kész)” jelöléssel |
| 9 | #5, #6, #7 | `fugg: [5, 6]` + levezetett **#7*** (2/A `olvas`, 2/C `ir`) | #7: igen (`adat/forditasok.tsv`) | „#5 (kész), #6 (kész), #7*” |
| 10 | #8, #9 | `fugg: [8, 9]` | nem (nincs `ir`) | — |
| 11 | #9 | `fugg: [9]` | nem | — |
| 12 | #11 | `fugg: [11]` | nem | — |
| 13 | #10 | `fugg: [10]` | nem | — |

A levezetett, de a v1.1-ben nem szereplő függés: **nincs** (a #9 `olvas`/`ir` listái és a #20 listái között sincs átfedés; a #20-nak nincs nyitott függése). K6 teljesül: minden v1.1-függés `fugg`-ban vagy levezetve van. `nem_fugg`: nem kell sehol.

Ütközések a nyitott feladatok között: nincs (`ir`-ük páronként különbözik; a #20 `*_BRIEF.md` és `.claude/commands/`, `.github/workflows/` listája senkivel nem fedi egymást). A #10–#13 és a #7/#8 stubok ír-listája üres: csomagba nem kerülhetnek.

## 4. A B4 eltéréslistája (előzetes; a K2 szerint a jóváhagyott eltérések)

1. „Állapot” oszlop: `⬜ nem futott` (1. fázis) / `⬜` (2. fázis) helyett egységesen a 5. pont jelei (`⬜`, `⬜ brief kell`, …).
2. „Függ ettől”: a lezárt függés „(kész)”, a levezetett `*` jelet kap; a v1.1 zárójeles megjegyzései (pl. „terminológia, kiejtés”) elmaradnak.
3. „Hol” oszlop: a brief fájlneve (vagy a `forras`); a v1.1 további útvonalai („`naplok/FORRAS_jelentes.md` …”, „brief v2 → v3”) a `kovetkezo` vagy a csonk törzsébe kerülnek.
4. „Kész” lista: formátuma `- cím (#n): összegzés`; a szám nélküli 3 tétel kézi szakaszba költözik (Q4); a lista a 14 napos ablakot a `git log`-ból kapja, ezért a mai tételek az átállás merge-e után 14 napig látszanak.
5. `Takarítás` szakasz: az átnevezési tétel törlődik (B3), a „briefek commitolása” tétel maradványa (#4, #7, #10, #11) a csonkokkal részben megoldódik; a többi tétel érintetlen. (Kézi szakasz, B5c-ben.)
6. A #12 sor „D29” → „SZOTAR-D29” (Q10).

## 5. Ami a jóváhagyás után történik

B3 (átnevezés `git mv`-vel: #1–#5 öt fájl; fejlécek 27 fájlra + 8 csonk + a #15/#6/#20 már nevezett), hivatkozásfrissítés (`grep -rn "_BRIEF.md"`, `naplok/` kivétel), B4. **Kérem: jóváhagyás vagy módosítás a Q1–Q10 kérdésekre és a 1–2. szakasz táblázataira.**
