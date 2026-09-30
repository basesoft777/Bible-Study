# F20 B2 — fejléc-munkalap ⛔ (jóváhagyásra vár) — v2, a FELADATOK v1.3 alapján

*2026.09.30 · alap: `origin/main` = `51f9291` (PR #77: v1.3 + csomagos `/kovetkezo`) · forrás: a briefek szövege, a B0 v2 felmérés, a FELADATOK v1.3 táblái, „Kész” listája és D14–D20. **Semmi nincs fejlécbe commitolva, semmi nincs átnevezve.***

Jelölések: **[javaslat]** = a brief szövege nem mond róla semmit, a B2 becslése. `—` = elhagyva (régi fejléc, 4.5).

## 0. Döntések

**Már eldőltek (a felhasználó válasza szerint):** Q1 (v1.3-alap, PR #77), Q2 (a szabály neve **E18**), Q3 (`archiv`, szám és átnevezés nélkül; az `ellenoriz` az archív briefnél nem vizsgál fájlnév–szám egyezést — a B1-ben így implementált), Q4 (szám nélküli „Kész” tételek kézi szakaszba), Q5 (a feladat nélküli briefek neve nem változik, az `F4–F8` is ide tartozik), Q6 (Károli-kulcs: a fő brief kapja a számot), Q7 (lezártaknál `olvas`/`ir` elhagyva), E16 (`[ELLENŐRZŐ]` PR-cím).

**Még nyitott (a tábla alapján jóváhagyandó):**

| # | Kérdés | Javaslat |
|---|---|---|
| Q8 | A stubok `modell` mezője (a tényleges brief még nincs meg) | 1/B tábla |
| Q9 | #12: a `TEREMT002_KUTATAS_BRIEF.md` csak T1–T2 (lefutott) → archív; a #12 külön stubot kap | elfogadni |
| Q10 | A #12 sor „D29”-a a SZOTAR-brief sorozata; a generált sorban `SZOTAR-D29` (a D21–D30 szabad, az új D29-cel nem keveredhet) | elfogadni |
| Q11 | **A B5a csonk-kitöltési szabálya** (a „korábbi Q-döntések … kiegészítve” mondat): a brief v1.2 B5a szövege ilyet nem tartalmaz. Az alábbi stub-terv erre épül: a csonk fejléce `brief_kell`, `olvas`/`ir` nélkül; a valódi brief megérkezésekor a `/befogad` a csonkot a beérkezett brieffel **váltja fel** (azonos szám és név). Kérem a szabály szövegét, vagy hagyjam jóvá ezt. | megadni / jóváhagyni |
| Q12 | A v1.3 csomagja (#16–#19 + #7) az `ir` nélküli csonkokkal a 4.5 miatt nem futtatható, amíg a valódi briefek (fejléccel, `olvas`/`ir`-rel) meg nem érkeznek. Csonk szándékosan nem kap találgatott `ir`-t. | elfogadni |

## 1. Briefek

Oszlopok: jelenlegi → új név · `feladat` · `tipus` · `fazis` · `allapot` · `modell` · nyitó prompt jelölése · megjegyzés. `olvas`/`ir`: 2. szakasz.

### A) Számozott feladatok, meglévő briefből

| Jelenlegi → új | # | tipus | fazis | allapot | modell | Nyitó prompt jelölése | Megj. |
|---|---|---|---|---|---|---|---|
| `KAROLI_KULCS_BRIEF.md` → `F01_KAROLI_KULCS_BRIEF.md` | 1 | feladat | 1 | lezarva | sonnet (régi sor) | 6., 7. | kód `KK`; archív társai: `_KK7_`, `_KK75_` |
| `CI_ELLENORZES_BRIEF.md` → `F02_CI_ELLENORZES_BRIEF.md` | 2 | feladat | 1 | lezarva | sonnet | „Nyitó prompt” (5. sor) | kód `CI` |
| `FORDITAS_PILOT_BRIEF.md` → `F03_FORDITAS_PILOT_BRIEF.md` | 3 | feladat | 1 | lezarva | sonnet | 6. | kód `FP` |
| `KARBANTARTAS_BRIEF.md` → `F04_KARBANTARTAS_BRIEF.md` | 4 | feladat | 1 | lezarva | sonnet | 6. | kód `KB`; `fugg: [2]` (brief: a #2 merge-e kell) |
| `SZOTAR_BRIEF.md` → `F05_SZOTAR_BRIEF.md` | 5 | feladat | 1 | lezarva | sonnet | 7. (S0, 1., 2. menet) | kód `SZOTAR S1`; `fugg: [1, 2, 3, 4]` (brief 48. sor) |
| `F06_FORRASFELMERES_BRIEF.md` (marad) | 6 | feladat | 1 | lezarva | sonnet | „Nyitó prompt” (108. sor) | |
| `F15_ORKESZTRATOR_BRIEF.md` (marad) | 15 | feladat | folyamat | lezarva | sonnet | 0. | |
| `F20_BEFOGADAS_BRIEF.md` (marad) | 20 | feladat | folyamat | fut (a menet első commitja) | sonnet | már jelölt | már új fejlécű |

### B) Számozott feladatok, csonk-brief (a v1.3 „Hol” neveivel)

| Új fájl | # | tipus | fazis | allapot | modell | `forras` | `fugg` |
|---|---|---|---|---|---|---|---|
| `F07_THAYER_ELES_BRIEF.md` | 7 | feladat | 1 | brief_kell | `külső:gemini-3.1-flash-lite` (FP2-D13; a v1.3 sor: „külső modell, keret 15 USD”) | — (v3 csak chatben) | [3, 5, 14] |
| `F08_LXX_DONTESEK_BRIEF.md` | 8 | feladat | 1 | brief_kell | opus [javaslat: kutatói ítélet] | — | [1, 17] |
| `F09_SZOTAR_S2_BRIEF.md` | 9 | feladat | 2 | nem_indult (a brief megvan) | sonnet | `F05_SZOTAR_BRIEF.md#2. menet` | [5, 6] + levezetett 7* |
| `F10_LEXIKON_LEZARAS_BRIEF.md` | 10 | feladat | 2 | brief_kell | opus [javaslat: L6/L7 döntés] | — | [8, 9] |
| `F11_MIGRACIO_BRIEF.md` | 11 | feladat | 2 | brief_kell | sonnet [javaslat] | — | [9] |
| `F12_TEREMT002_PROZA_BRIEF.md` | 12 | feladat | 2 | brief_kell | opus [javaslat: a T1–T2 brief opus] | `TEREMT002_KUTATAS_BRIEF.md` | [11] |
| `F13_GENEZIS_KIADAS_BRIEF.md` | 13 | feladat | 2 | brief_kell | sonnet [javaslat] | — | [10] |
| `F14_FP2_STILUSPROBA_BRIEF.md` | 14 | feladat | 1 | lezarva | sonnet [javaslat] | `naplok/FP2_jelentes.md` | — |
| `F16_BSB_IMPORT_BRIEF.md` | 16 | feladat | 1 | brief_kell | sonnet [javaslat: importszkript] | — | [6] |
| `F17_MACULA_IMPORT_BRIEF.md` | 17 | feladat | 1 | brief_kell | sonnet [javaslat] | — | [6] |
| `F18_NAVE_IMPORT_BRIEF.md` | 18 | feladat | 1 | brief_kell | sonnet [javaslat; a Gemini-bírálat a D17 szerint szkriptből fut] | — | [6] |
| `F19_KJV_ASV_IMPORT_BRIEF.md` | 19 | feladat | 1 | brief_kell | sonnet [javaslat] | — | [6] |

Csonk-törzs: 3–6 sor (cím, a v1.3 sor „Mit ad” és „Következő lépés” szövege, `forras`-hivatkozás). A `kovetkezo` mező a v1.3 „Következő lépés/Megjegyzés” cellájának szó szerinti szövege. A csonk nem hajt végre, nyitó promptot nem tartalmaz.

### C) Feladat nélküli briefek (`tipus: archiv`, `allapot: lezarva`, név nem változik)

| Fájl | modell | Nyitó prompt jelölése |
|---|---|---|
| `KAROLI_KULCS_KK7_BRIEF.md` | sonnet (régi sor) | 6. |
| `KAROLI_KULCS_KK75_BRIEF.md` | sonnet (régi sor) | 6., 7. |
| `FORRASJELOLTEK_BRIEF.md` | sonnet (régi sor) | 6. |
| `TEREMT002_KUTATAS_BRIEF.md` | opus (régi sor) | 6. |
| `RENDER_BRIEF.md` | sonnet (régi sor) | 7. |
| `CREMER_OCR_BRIEF.md`, `ISTENTISZT_V3_BRIEF.md`, `LEX_BRIEF.md`, `LEXV2_1_BRIEF.md`, `LEXV2_2_BRIEF.md`, `N12_BRIEF.md`, `N14_BRIEF.md`, `N16_BRIEF.md`, `SDBH_IMPORT_BRIEF.md`, `F4_BRIEF.md`, `F4_GENERATOR_BRIEF.md`, `F5_BRIEF.md`, `F6_BRIEF.md`, `F7_BRIEF.md`, `F8_BRIEF.md` | sonnet [javaslat; a törzsben nincs `Modell:` sor] | CREMER 7.; LEX 8.; N12 8.; N14 8.; SDBH 7.1–7.2; F4 6.3–6.5; F4_GEN 6.3–6.6; F5 6.1–6.2; F6 8.1–8.3; F7 7.; F8 7., 7b, 7c; ISTENTISZT_V3, LEXV2_1, LEXV2_2, N16: nincs |

A nyitó prompt jelölése csak a felsorolt szakaszok köré kerül (menetenként külön pár), a szöveg nem változik.

## 2. `olvas` / `ir` a nyitott feladatokra

- **#9** (forrás: `SZOTAR_BRIEF.md` 2. menet, S2.1–S2.9)
  - `olvas`: [adat/forditasok.tsv, adat/terminologia.tsv, adat/kiejtes_kivetelek.tsv, konkordancia/, lexikon/]
  - `ir`: [lexikon/, adat/kiejtes_kivetelek.tsv, adat/szotar_szerepek.tsv, eszkozok/torzscikk_general.py, eszkozok/lexikon_general.py, eszkozok/render_diff_osztalyoz.py, MUNKAMENET.md, NYITOTT_FELADATOK.md]
- **#20** (a fejlécében már benne van): `olvas` [FELADATOK.md, DONTESEK.md, CLAUDE.md, NYITOTT_FELADATOK.md, "*_BRIEF.md", .claude/commands/, .github/workflows/]; `ir` [eszkozok/feladatok.py, eszkozok/teszt_feladatok.py, "*_BRIEF.md", BRIEF_SABLON.md, beerkezo/, FELADATOK.md, CLAUDE.md, .claude/commands/, .github/workflows/].
- **#7 csonk** [javaslat, a chatben lévő brief hiányában a v1.3 sorából és a SZOTAR S1 eredményeiből]: `olvas` [adat/terminologia.tsv, adat/kiejtes_kivetelek.tsv, konkordancia/Thayer_teljes.tsv]; `ir` [adat/forditasok.tsv]. Ez adja a v1.3-ból ismert #9→#7 függést levezetve; a valódi brief megérkezésekor felülíródik.
- **#8, #10–#13, #16–#19 csonk:** `olvas`/`ir` nincs (régi fejléc, 4.5), a függést a `fugg` adja (Q12).

## 3. Függések összevetése (v1.3 ↔ fejléc)

| # | v1.3 „Függ ettől” | Fejléc | Levezetve? | Eltérés a generált cellában |
|---|---|---|---|---|
| 7 | #3, #5, #14 (kész) | `fugg: [3, 5, 14]` | — (lezártak) | „#3 (kész), #5 (kész), #14 (kész)” (a zárójeles „terminológia, kiejtés” megjegyzés elmarad) |
| 8 | #1, #17 (Macula-import) | `fugg: [1, 17]` | nem (nincs `ir`) | „#1 (kész), #17” |
| 9 | #5, #6, #7 | `fugg: [5, 6]` + **7*** | #7: igen | „#5 (kész), #6 (kész), #7*” |
| 10 | #8, #9 | `fugg: [8, 9]` | nem | — |
| 11 | #9 | `fugg: [9]` | nem | — |
| 12 | #11 | `fugg: [11]` | nem | — |
| 13 | #10 | `fugg: [10]` | nem | — |
| 16, 17, 18, 19 | #6 | `fugg: [6]` | — (lezárt) | „#6 (kész)” |

Levezetett, de a v1.3-ban nem szereplő függés: **nincs**. K6 teljesül: minden v1.3-függés `fugg`-ban vagy levezetve van. `nem_fugg`: nem kell. Ütközések a nyitott feladatok között: nincs (a #9 és #20 `ir`-je páronként eltér; a csonkoknak nincs `ir`-je). Csomagolhatóság: a #9 és a #20 csomagképes; a #7 csonk (javasolt `ir`-rel) csomagképes, a többi csonk nem (Q12).

## 4. A B4 eltéréslistája (előzetes, a K2 szerint a jóváhagyott eltérések)

1. „Állapot”: `⬜ nem futott` (1. fázis) és `⬜` (2. fázis) helyett egységesen a 5. pont jelei (`⬜`, `⬜ brief kell`, …).
2. „Függ ettől”: lezárt függés „(kész)”, levezetett `*`; a v1.3 zárójeles megjegyzései elmaradnak.
3. „Hol”: a brief fájlneve (csonknál a fájl), a #9-nél a `forras` (`F05_SZOTAR_BRIEF.md#2. menet`), a #12-nél a csonk; a v1.3-ban „brief csak chatben”, „—” helyén a csonk neve áll. A #7–#8 és #16–#19 „Hol” cellája változatlan (a csonk neve = a v1.3 neve). A v1.3 „Hol” dokumentáló kiegészítései (pl. „v3”, a #6 sor) a `kovetkezo`-ba vagy a csonk törzsébe kerülnek.
4. A #6 sor a v1.3 táblájában nem szerepel (a „Kész” listában van, PR #76); a generált „Kész” lista formátuma `- cím (#n): összegzés`; szám nélküli 3 tétel kézi szakaszba (Q4).
5. A #12 sor „D29” → „SZOTAR-D29” (Q10).
6. `Takarítás`: az átnevezési tétel törlődik (B3); a „chatben készült briefek commitolása” tétel részben megoldódik (csonkok). A Munkamenet-szakasz (1., 2., 5., 6. és **8.** pont) a B5c-ben, nem a generált blokkban változik.

## 5. Ami a jóváhagyás után történik

B3 (öt `git mv` #1–#5; fejlécek 27 meglévő + 12 csonk fájlra; `#6`, `#15`, `#20` már nevezett), hivatkozásfrissítés (`grep -rn "_BRIEF.md"`, `naplok/` kivétel), B4. **Kérem: jóváhagyás vagy módosítás a Q8–Q12 kérdésekre és a 1–2. szakasz táblázataira.**
