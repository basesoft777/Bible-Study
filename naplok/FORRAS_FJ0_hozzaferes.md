# FORRAS_FJ0_hozzaferes.md — kiindulás újramérése és forráshozzáférés

*FJ0 — FORRASJELOLTEK_BRIEF.md §3 szerint, 2026.09.25*

## 1. §0 számainak újramérése

| # | Mérés | Brief-érték | Újramért érték | Egyezik? |
|---|---|---|---|---|
| 0.1 | `main` | `a6783e4` | `a6783e4` | igen |
| 0.2 | 8 `lexikon/*_TUDOMANYOS.md` 3. szakasz "Egyezés" | egyező 123 · függőben 87 · szamozas_elteres 15 · eltérő 3 · nincs LXX_OS-könyv 5 · LXX-minusz 1 | ugyanaz (`naplok/FORRAS_FJ0_egyezes_szamlalo.py` szkripttel újraszámolva, 234 sor összesen) | igen |
| 0.3 | `adat/lxx_dontesek.tsv` | 4 sor (LD001–LD004), mind ISTENTISZT-001 | 4 sor, ellenőrizve | igen |
| 0.4 | `konkordancia/KJV_/ASV_Strongs_*.tsv` | 6 fájl (1Móz, 2Móz, Péld) | 6 fájl megvan | igen |
| 0.5 | `konkordancia/LXX_OS/` | `verse_pairs.jsonl`, TVTMS, ~99,57% | a `konkordancia/LXX_OS/README.md`-ben dokumentálva; a `verse_pairs.jsonl` maga a repóban NEM tárolt fájl (csak a lxx-morph forrás `db/seeds/mt_alignment/` alatt, letöltve ellenőrizve, l. lent) | igen (a leírás pontos) |
| 0.6 | SZOTAR S0.8 | H7121×G1941: 102/635 (14,8%) | `naplok/SZOTAR_S0_jelentes.md` 8. pont, szó szerint egyezik | igen |
| 0.7 | `eszkozok/ellenoriz.py` | RENDBEN 9 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2 | ugyanaz, frissen lefuttatva | igen |

Eltérés nincs a §0-hoz képest.

## 2. Forráshozzáférés a sessionből

Az outbound HTTPS a proxy-n megy át. A közvetlen `curl` a `github.com`-ra és
`raw.githubusercontent.com`-ra **403/404**-et ad (a proxy vagy GitHub UA-szűrése
miatt), de a **`git clone` a smart-HTTP protokollon keresztül működik** — ez a
tényleges hozzáférési útvonal minden alábbi forráshoz.

| Forrás | Repó | Hozzáférés | Módszer |
|---|---|---|---|
| CenterBLC/MT-LXX | `github.com/CenterBLC/MT-LXX` | **elérhető** | `git clone --depth 1`, commit `e9d803e36ea7da91ab37d8f7603dd2340c206ec2` |
| Macula Hebrew | `github.com/Clear-Bible/macula-hebrew` | **elérhető** | `git clone --filter=blob:none --no-checkout` + `sparse-checkout` (teljes klón ~90s alatt timeoutolt, mérete miatt), commit `47db250bd55d0d8577f2a94fba114ef16c35b23c` |
| Macula Greek | `github.com/Clear-Bible/macula-greek` | **nem tesztelve ebben a menetben** (az FJ1 fókusza a MT–LXX-illesztés, ami a Hebrew repóban van; a Greek repó licence-ellenőrzése a G3 szerint külön tétel, l. FJ1 jelentés) | — |
| eBible.org (KJV/ASV USFM) | `ebible.org` | **közvetlen web-hozzáférés nem elérhető** (`CONNECT tunnel failed, response 403`); helyette GitHub-tükrökön/USFM-projekteken keresztül kutatva (FJ3) | WebSearch + git clone |
| BSB-publishing | `github.com/BSB-publishing/*` | **elérhető** (git clone-nal, a helyes repónév megtalálása után) | l. FJ3 |
| Nave-jelöltek (basokant/nave, theonize/bible_database, elcafe7/lex) | github | **elérhető**, `basokant/nave` nem található (nincs ilyen repó) | l. FJ4 |

**Módszertani megjegyzés:** a `github.com` és `raw.githubusercontent.com` közvetlen
HTTP-lekérése (curl, WebFetch) ezen a sessionön blokkolva van vagy 403-at ad;
minden tényleges adatszerzés `git clone`-nal történt, a `konkordancia/_nyers/`
(gitignore-olt) alá, a repó gyökerén kívül eső `/tmp`-be pufferelve a nagy
klónokat (méretkorlát miatt nem kerültek be a repóba).

Egy forrásnál sem történt megakadás; minden tétel a §3 szerint folytatható.
