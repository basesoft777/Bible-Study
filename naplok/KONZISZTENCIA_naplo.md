# KONZISZTENCIA_naplo.md — F51 (FELADATOK #51) munkanapló

*Brief: `F51_KONZISZTENCIA_BRIEF.md` · ág: `claude/konzisztencia` · modell: sonnet · indítás: 2026.10.05*

A napló a K0 felmérést, az eltéréseket és a K5 ütemezési tervet rögzíti. Kézi forrás.

## K0 — Hol élnek ma döntések (felmérés, csak olvasás)

*(proveniencia: scope=repó `*.md` táblasorai a `| <azonosító> |` mintára, a `.claude/worktrees/`, `konkordancia/`, `generalt_proba/`, a `beerkezo/` és az archívum/changelog fájlok nélkül | forras=manual (a K0 szkript a scratchpadben, nem a repóban) | ts=2026-10-05)*

| Forrás | Azonosító-forma | Sorszámok | Megjegyzés |
|---|---|---|---|
| `FELADATOK.md` „Döntésnapló” | `D<n>` | D1–D50 (50 sor) | a **globális** D-számozás; a D34–D41-et a #26 (F26) vitte át, a D42–D50-et a #29 (F29) |
| `DONTESEK.md` | `DT<n>`; `DT-F<n><betű>`; `DT-M<n>` | DT1–DT27 (15 sor); DT-F21a … DT-F52 (70 sor); DT-M1–M8 (8 sor) | a nyitott döntések sora; a `DT-F<n><betű>` a feladat száma + betű (a régi `DT19`–`DT21` az F21-ben `DT-F21h/i/j`-re költözött) |
| `F<nn>_*_BRIEF.md` „Döntésnapló” | brieflokális `D<n>` (F02: D1–D18; F05: D1–D42; F8: D1–D21 + G1–G10; RENDER: D1–D28 + G1–G16; F4_GENERATOR: D1–D15; N12/N14: D1–D13/D15; SDBH_IMPORT: D1–D21; CREMER_OCR: D1–D22 …) | l. a fájlonkénti tartományok | **a számozás fájlonként újraindul** — ezért a `dontes_hatas.tsv` kulcsa fájl + azonosító (DT-F51-5) |
| `F<nn>_*_BRIEF.md` „Döntésnapló” | `DT-F<n>-<k>` (F37: 1–8; F51: 1–5), `DT-F39a–e` | — | az újabb, feladatszámmal kezdődő forma |
| `*_BRIEF.md` kapu-táblák | `G<n>` (F01: G1–G11; F03: G1–G9; F04: G1–G8; F8: G1–G10; RENDER: G1–G16; LEXV2_2: G12–G…; FORRASJELOLTEK: G1–G8; TEREMT002_KUTATAS: G1–G7) | brieflokális | a „G” egyszerre jelent kapu- és döntésszámot |
| `MUNKATERV.md` | `DT-M<n>` | DT-M1–M6 | a `DONTESEK.md` DT-M1–M8-jával **ugyanaz a névtér, külön számozással** (lásd lent) |
| `ATALAKITASI_TERV.md.md`, `ADATVAGYON_TERV.md` | `D<n>`, `N<n>` | D1–D25, N1–N13 / D46, D50, DT23 … | az `ADATVAGYON_TERV.md` a globális D46/D50-et idézi |
| `NYITOTT_FELADATOK.md` | `N<n>`, `N-F<n><betű>` | N1–N45+; N-F34, N-F41a–h, N-F46a/b … | nyitott tételek, nem döntések |
| `DONTESEK_INDEX.tsv` | — | 9 sor (0–8. szakasz) | **nem döntésindex**: az archívum (`PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md`) szakaszainak belépője; a K0-ban nem használható döntésforrásként |

A K0 szkript a scratchpadben futott (nem része a repónak, a következő futás a `/konzisztencia` ügynök dolga).

### Ütköző azonosítók

| Azonosító | Hol és mit jelent | Megjegyzés |
|---|---|---|
| **D34–D37** | `F05_SZOTAR_BRIEF.md` (a héber kiejtés-jelölt gépezet: spirantizáció, ח → `ch`, H2555 kivétel, alef/ajin-elhagyás; az `adat/SEMA.md` 2.18 címe is „D34–D37”) **kontra** `FELADATOK.md` / `F26_EGYFORRAS_NAPLO_BRIEF.md` (D34 motívumonként egy kézi forrás, D35 generált fájlba kézzel nem írunk, D36 mélységi szintek, D37 egy forrássablon) | a brief kiinduló esete; a `F26` brief maga is jelzi, hogy „a számok a befogadáskor csúszhatnak” |
| **D38–D41** | `F05_SZOTAR_BRIEF.md` (D38 betű-utótagos STEP-kulcs, D39 javítás még az S1-ben, D40 mintavétel, D41 BDB-etimológia-határ) **kontra** `FELADATOK.md` / F26 (D38 pilot két lépcsőben, D39 egy motívumon egy feladat, D40 olvasói felület, D41 licenc-átnézés) | az F05 helyi, a `FELADATOK.md` a globális szám |
| **D42** | `F05_SZOTAR_BRIEF.md` (F05b javítókör hatóköre) **kontra** `FELADATOK.md` / F29 (D42 Opus fordítja a lexikon szócikkeit) | |
| **D20–D33** | `F05_SZOTAR_BRIEF.md` (D20–D33: S14, BDB-etimológia, tesztkészlet, kiejtés-szabályok, MCGED …) **kontra** `FELADATOK.md` (D20 csomagmód … D33 🔀-jel); `F20_BEFOGADAS_BRIEF.md` D21–D30 ugyanezt a globális tartományt idézi, azonos tartalommal | az F05-ben a számok a brieflokális tartományt jelentik |
| **D1–D18** | `F02_CI_ELLENORZES_BRIEF.md`, `F4_GENERATOR_BRIEF.md`, `F5_BRIEF.md`, `F6_BRIEF.md`, `F8_BRIEF.md`, `ATALAKITASI_TERV.md.md` … **kontra** `FELADATOK.md` D1–D18 | mind brieflokális, mind a globális tartományban ott van; ez az egész rendszer jellemzője, nem egyedi ütközés |
| **DT-M1–M6** | `MUNKATERV.md` **kontra** `DONTESEK.md` DT-M1–M8 | ellenőrizendő: azonos döntések-e, vagy két külön lista |
| **G1–G16** | `RENDER_BRIEF.md`, `F8_BRIEF.md`, `F01_*`, `F03_*`, `F04_*`, `FORRASJELOLTEK_BRIEF.md`, `TEREMT002_KUTATAS_BRIEF.md` | a G egy briefen belüli kapuszám, nem globális; a `G<n>` hivatkozás fájl nélkül nem egyértelmű |

*(A K0 szkript a `G<n>` mintán két hamis találatot adott a `G1941`/`G0012` Strong-számokon; ezeket a fenti összegzés nem számolja.)*

### Következtetés a kulcsról

A D-számozás **fájlonként értelmes**, a `FELADATOK.md` D1–D50 az egyetlen globális sor, és ez ütközik a briefek helyi számaival. Ezért a `dontes_hatas.tsv` kulcsa a **fájl + azonosító** (DT-F51-5), a `dontes_forras` mező alakja `fájl#azonosító`.

## K1 — a tábla és a SEMA (2.21)

A tábla: `adat/dontes_hatas.tsv`, séma: `adat/SEMA.md` 2.21. Oszlopok a brief szerint (`dontes_forras`, `datum`, `erintett_fajl`, `tilos_minta`, `atmeneti_jeloles`, `tovabbvivo_feladat`, `megjegyzes`). Kulcs: `dontes_forras` + `erintett_fajl` + `tilos_minta` (egy döntéshez több sor tartozhat egy fájlban is, több mintával).

## K2 — induló sorok

**Jóváhagyva (2026.10.05, a felhasználó chatben), módosításokkal.** A `RENDER_BRIEF.md` két sora (G1, G7) kikerült: az E25 általánosan kihagyja a `tipus: archiv` fejlécű fájlokat (archívumot nem szerkesztünk, a történeti állapot nem hiba), nem fájlhoz kötötten. Plusz sor nem került fel (a „tanulmány” kettős jelentése, a KJV/ASV és az LXX-hivatkozás a K4 ügynök dolga; a KJV/ASV → F19, az LXX → F42 később külön döntéshez kötött sor lehet). A tábla szövegmintára illeszt; a sorszám (67., 181.) csak a megjegyzésben áll. Mind a három sor a D34-é (`F26_EGYFORRAS_NAPLO_BRIEF.md#D34`, datum 2026-09-30, `tovabbvivo_feladat` 11).

| # | Fájl | Minta (`tilos_minta`) | Találat (sor) | Átmeneti jelölés | Hatás |
|---|---|---|---|---|---|
| 1 | `CLAUDE.md` | `\[ID\]_TORZSCIKK\.md` | 33, 47 | `Átmenet \(D34\)` (megvan, 35. sor) | JELENTES |
| 2 | `MUNKAMENET.md` | `^\| C1 \| lexikon TUDOMÁNYOS szakaszainak \+ a törzscikk generálása` | 67 | nincs | FIGYELMEZTETES |
| 3 | `MUNKAMENET.md` | ``a \*\*törzscikk\*\* \(`lexikon/`` | 181 | nincs | FIGYELMEZTETES |

**Eltérések a briefhez képest (jelezve):**
- A brief a `MUNKAMENET.md` C1 sorát „139. sor körül” adja; a mai fájlban a C1 a **67.** sor, a törzscikk bemutatása a **181.** sor. A minta a szövegre illik, nem a sorszámra, ezért ez nem érinti a szabályt.
- A brief a `tovabbvivo_feladat` értékét „26, illetve 11”-nek adja. A #26 (EGYFORRAS_NAPLO) azóta **lezárva** és mergelve (`117bafc`, 2026.10.04): a `CLAUDE.md` átmeneti sorát (`Átmenet (D34)`) ő vitte át. A tényleges továbbvivő a **#11** (MIGRACIO, `brief_kell`): a törzscikk megszűnése és a `CLAUDE.md`/`MUNKAMENET.md`/`RENDER_BRIEF.md` végleges átírása ott történik. Ezért mind a sor a 11-et viszi (a tábla a K3-ban 3 sorra szűkült); a 26 nem szerepel (lezárt feladatnál az E25 (b) úgysem szólna).
- A (b) ág ma még nem szól: a #11 `brief_kell`, de a D34 (2026-09-30) óta 5 nap telt el; a 14. nap 2026-10-14.
- A `CLAUDE.md` D34-sora azért csak JELENTES, mert a #26 átmeneti jelölést tett a fájlba. Az elfogadási feltétel („az E25 legalább a D34 `CLAUDE.md`-sorát jelzi”) ezzel teljesül: jelzi, de nem riaszt.

**Nem vettem fel (nem egyértelmű regex):** a „tanulmány” szó kettős jelentése (F37 kontra D34); a `CLAUDE.md` „`KJV_/ASV_Strongs` csak Genezis, Exodus, Példabeszédek” sora az F19-import (és a függő F48) után; a `sablonok/2_PaRDeS_bovitett_sablon.md` 277. sorának `LXX_kivonat_Genezis.tsv` hivatkozása az F42 után (a hivatkozás forráslistában példa, nem nyilvánvalóan hibás). Ezek az ügynök (K4) dolga.

## K3 — az E-szám (egyeztetett eltérés, rögzítve)

A brief az új szabályt **E25**-ként jelöli, azzal a megjegyzéssel, hogy a végleges szám az implementáláskor dől el a `szabalyok.py` és a #37 aktuális állapota szerint. Állapot 2026.10.05-én: a `szabalyok.py` utolsó szabálya az **E19**; az E20–E24 helye a #37-nek (`F37_TANULMANY_ELLENORZES_BRIEF.md` T3) van fenntartva, a #37 nem indult (⬜), egy `E20`–`E24` sor sincs a kódban. A **végleges szám: E25** — a #37 számait nem foglalja el, és nem ütközik vele, akkor sem, ha a #37 később indul. A felhasználó által jóváhagyott eltérés: a #37-től való lágy, levezetett függés (`.github/workflows/ellenorzes.yml*`) nem akadály. *(A `FELADATOK.md` #51 sora `fugg: #37*`-gal jelzi a levezetett függést.)*

## K3 — megvalósítás (E25)

- `eszkozok/ellenorzes/szabalyok.py`: `e25_dontes_atvezetes`; fájlszintű (`FAJLSZINTU_SZABALYOK`) és adattáblán futó (`HATOKOR_SZABALYOK`), alapszint FIGYELMEZTETES; a hívott `futtat.py` a `SZABALYOK_FUGGVENYEI`-ből veszi.
- (a) régi állapot: FIGYELMEZTETES, `atmeneti_jeloles`-szel JELENTES; a `tipus: archiv` fejlécű érintett fájl kimarad; (b) a továbbvivő feladat állapotát a gyökér `*_BRIEF.md` fejlécek `feladat:`/`allapot:` mezője adja; 14 napnál régebbi döntés, `nem_indult`/`brief_kell` → FIGYELMEZTETES; (c) hiányzó forrásfájl / azonosító / érintett fájl, hibás regex vagy dátum → HIBA.
- Tesztek: `eszkozok/ellenorzes/tesztek/test_szabalyok.py` `E25Teszt`, 18 teszt (köztük az archív kivétel, a 14. nap határa, a lezárt továbbvivő, a `futtat.fut` teljes és változott módja, a valódi tábla nulla HIBA); az egész modul 74 teszt, zöld.
- `futtat.py --teljes`: nulla HIBA, kilépési kód 0; az E25 a `CLAUDE.md:33` D34-sorát (JELENTES) és a `MUNKAMENET.md` két sorát jelzi.
- A CI workflow (`.github/workflows/ellenorzes.yml`) nem módosult: a lépés neve „E2-E19”, de a `futtat.py` az E25-öt is futtatja; a név átírása a brief `ir` listáján kívül van (D6: CI-javítás külön ágon), ezért nem nyúltam hozzá.

## K4 — az ügynök és az első jelentés

`.claude/commands/konzisztencia.md` (csak olvas, egy fájlt ír). Az első, kézi próbafutás jelentése: `naplok/konzisztencia/KONZISZTENCIA_20261005.md` (D34 ↔ `CLAUDE.md`, a D34-számütközés, a „tanulmány” kettős jelentése; 0 régóta álló továbbvivő). A `ir` listához a jelentés fájlja (`naplok/konzisztencia/KONZISZTENCIA_20261005.md`) bekerült.

## K5 — helyi ütemezés (jóváhagyva, létrehozva)

- **Gyakoriság:** napi egy futás, minden nap 9:00 (helyi idő). *(Egyeztetett eltérés: a brief heti futást írt, a felhasználó 2026-10-05-én napit kért.)*
- **Hely:** helyi ütemezett feladat (a gépen, nem felhőben: DT-F51-2). Csak akkor fut, ha a gép be van kapcsolva; a kimaradt futás pótlódik a következő bekapcsoláskor.
- **Modell:** sonnet. **Tartalom:** a `/konzisztencia` parancs a repó `main` állapotán; kimenet: `naplok/konzisztencia/KONZISZTENCIA_<ééééhhnn>.md`.
- **Munkakönyvtár (egyértelműen):** NEM a fő munkapéldányban fut. Külön, csak erre használt, leválasztott (detached) worktree: `../Bible-Study-konzisztencia`. Ha nincs meg, a futás elején létrehozza: `git worktree add --detach ../Bible-Study-konzisztencia origin/main`. Minden futás elején ott `git fetch`, majd `git checkout --detach origin/main` (ff-only frissítés; a worktree-ben nincs kézi munka). A fő munkapéldányhoz és a futó session-ágakhoz nem nyúl; a jelentés is a worktree `naplok/konzisztencia/` mappájában keletkezik (követetlen marad, a repóba nem kerül).
- **Napi összevetés:** a jelentés elején „Új az előző jelentés óta” (a `konzisztencia.md` 5. lépése); az E25 3 JELENTES-e a #11 lezárásáig naponta újra megjelenik: várható, nem hiba.
- **Jogosultság:** csak olvasás és egyetlen jelentésfájl írása; nem commitol, nem pushol, nem nyit ágat (DT-F51-3). A jelentést a felhasználó átnézi, és a javaslatok (`dontes_hatas.tsv`-sor, `/befogad`-jelölt, `DONTESEK.md`-tétel) sorsáról dönt.
- **Értesítés:** a jelentés elkészültekor (a végén egy sor: a jelentés útvonala és az új találatok száma).
- **Jóváhagyás:** a felhasználó a K5 tervet a fenti pontosításokkal és napi gyakorisággal jóváhagyta (2026-10-05); az ütemezett feladat létrehozva (`konzisztencia-napi`, minden nap 9:00).
- **Külön tétel (nem a #51 ága):** a CI lépésneve („E2-E19”) és az, hogy a CI nem futtatja a `test_szabalyok.py`-t: új feladatként a `/befogad` veheti fel.
