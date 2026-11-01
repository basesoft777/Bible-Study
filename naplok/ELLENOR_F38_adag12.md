ELTÉRÉS: 4 tétel

# Független ellenőrzés: F38_BDB_FORDITAS_BRIEF.md, 12. adag (sorrend 3981–5670), PR #551

*A `fuggetlen-ellenor` subagent jelentése, változtatás nélkül mentve az orkesztrátor által (az ellenőrnek nem volt fájlíró eszköze). Az „Az ELTÉRÉS-ek” és a „Verdikt” az ellenőr szövege.*

- **Brief:** `F38_BDB_FORDITAS_BRIEF.md`
- **Tartomány:** `9cf0e43a..bf69bcf1` (10 commit: F38.434–F38.443; a `9cf0e43a` az `origin/main` hegye, így a main-hez mért Δ azonos a diffel)
- **Bontási napló:** `naplok/BDB_FORDITAS_adag12_bontas.md`

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell (ellenőr) | OK | — | A tényleges modell `claude-opus-5-5`, a kért modell `opus`. Egyezik. |
| 0 modell (menet) | OK (a tényleges modell csak a commit-trailerből látszik) | `adat/forditasok.tsv:18854–23849` | Grep count: `^BDB\t…\tforditas_hu\t[0-9a-f]{40}\t[^\t]*\tsonnet\tclaude-sonnet-5-5\t2026\.11\.01\tv4\t` → 4996. `git log --format='%B' 9cf0e43a..HEAD` → 10× `Co-Authored-By: Claude Sonnet 5.5`. A brief `modell: sonnet` mezője egyezik a sorok `claude-sonnet-5-5` értékével. |
| Numstat | OK | bontás:9–15 | `git diff --numstat 9cf0e43a..HEAD` → `forditasok.tsv` 4996/0, `EMELES_munka.tsv` 4996/0, `FORDITAS_kisnagybetu_csere.tsv` 2/0, `adag12_bontas.md` 85/0, brief 3/3. |
| Commitonkénti bontás | OK | bontás:27–37 | `git diff --numstat <c>~1 <c>` minden commitra: 1037, 639, 680, 771, 627, 557, 456, 229 (összesen 4996), törlés 0. Szócikk/commit: 330, 190, 255, 261, 208, 208, 156, 82 (összesen 1690). Az első és utolsó Strong commitonként egyezik a `BDB_FORDITAS_sorrend.tsv` határaival. A commitüzenetek „kb.” tartományainak helyesbítése (bontás:25) igaz. |
| Lefedettség (1690 Strong) | OK (a teljes halmazkülönbséget nem futtatta újra) | `naplok/BDB_FORDITAS_sorrend.tsv:3983–5672` | Grep count `\t12$` → 1690. A 2026.11.01-es sz1-sorok száma 1689, plusz 1 `teljes` sor (H3848), összesen 1690. 25 rétegzett minta: mind rendben. A H8546 (5671) nincs az adagban. |
| H3848 (régi út) | OK | `forditasok.tsv:19890` | A fordítás hű, `jelentes_szam=teljes`. |
| H3896 / 17_bdb_javitas | OK | `forditasok.tsv:19519`; `bdb_igehely_javitas.tsv:43` | A forrás „p. 2Sam 31:2above”, a fordítás „o. 2Sám 31:2 fent”: hű, nem javított. |
| H7966 megjegyzés | OK | `forditasok.tsv:20462–20465` | Mind a 4 sor `megjegyzes`-e jelöli a forráshibát (DT362 (1)(a), DT363). |
| DT361-felülbírálás: 8_idezojel (9 Strong) | OK | `forditasok.tsv:19205, 19286, 19966, 20977, 21615, 21705` és további sorok | A forrásban a „ (U+201E) OCR-maradvány pár nélkül áll; a fordítás változatlanul hordozza. 12 Strong, egyezik a napló listájával. |
| DT361: H6741, H6825 | OK | `forditasok.tsv:20175, 20204` | Helyes feloldás / változatlan siglum. |
| DT361: H7688 | **ELTÉRÉS** (hű fordítás) | `forditasok.tsv:20375` | A felülbírálás indokolt (a „see” itt ige), de a forrás `bdb_szakaszok.tsv:32502` „absolute: Participle … Song 2:9” részét a fordítás „status absolutus: participium”-nak adja; ide a `terminologia.tsv:67` `absolute (használat)` → „abszolút használatban” sor illik. |
| D10 (5): RV/AV után angolul marad | **ELTÉRÉS** | `forditasok.tsv:20206, 23019, 23650, 21374` | H6843 sz2: „AV morning” → „AV reggel”; H6289 sz2: „AV gather blackness” → „AV feketeséget gyűjtenek”; H8143 sz2: „AV RV ivory” → „AV RV elefántcsont”; H1999 sz2: „AV RV Da tumult” → „AV RV Da zajongás”. Az adagban más sorok angolul tartják a glosszát. |
| Hű fordítás, minták | OK | `forditasok.tsv:20636–20640, 19991–19993, 22234–22235, 23674–23676, 21261–21266, 22748–22753` | H0150, H6014, H4183, H8197, H1752 és H5533 soronként összevetve: a szakaszszám egyezik, a tartalom hű. |
| D11 (-szor/-szer/-ször) | OK | — | Hibás hangrendű alak 0. |
| Kisnagybetű-csere +2 | OK | `forditasok.tsv:21264, 22752` | Egyezik a `FORDITAS_kisnagybetu_csere.tsv` 2 új sorával. |
| D2, D3, D6 | OK | `F38_BDB_FORDITAS_BRIEF.md:8, 12` | `allapot: megallt`; a `kovetkezo` „13. adag (sorrend 5671-től)”: `^5671\t` → H8546, adag 13. |
| D7, DT56 Károli-lefedettség | NEM ELLENŐRIZHETŐ | bontás:3 | Megengedett paranccsal nem mérhető. |
| Brief `ir` mező | **ELTÉRÉS** | `F38_BDB_FORDITAS_BRIEF.md:14` | A `naplok/BDB_FORDITAS_adag12_bontas.md` nem került az `ir` listába (a 7–11. adag bontása benne van). |
| Commitüzenet ékezetei | **ELTÉRÉS** | `2c4b5fe3` | Az E30 4 figyelmeztetést ad (`reszleges`, `gyakorisagi`, `felulbiralas` és egy további szó). |
| A1 memória vs. lekérdezés | OK (két nem igazolt állítással) | bontás:77, 81–84 | A „kb. 60 szócikk” első kapubukás lekérdezés és proveniencia nélkül áll. |
| A2, A3–A5, A6 | OK / NEM ÉRINTETT | — | A diff nem érinti a `NYITOTT_FELADATOK.md`-t; E12–E15 mind 0. |
| CI ↔ saját futás | NEM ELLENŐRIZHETŐ | — | `futtat.py --valtozott … --diff-alap 9cf0e43a --diff-fej HEAD`: E2–E32 mind 0; E25: 4, E27: 40 JELENTÉS (nem a diff fájljai); E30: 4 figyelmeztetés. HIBA nincs. |
| Lista 1–5 | OK | — | Törölt adatsor 0; kulcstartomány lefedett; nulla-diff hatóköre pontos; tábla-Δ +4996 (bontási napló van); ⛔ pont nem érintett. |

**Az ELTÉRÉS-ek súlyossági sorrendben:**

1. **D10 (5) megsértése 4 sorban.** H6843 sz2, H6289 sz2, H8143 sz2 és H1999 sz2: a forrásban AV/RV után álló glosszát a fordítás magyarra fordította. Az adagon belül a kezelés következetlen.
2. **H7688 sz2: „absolute” → „status absolutus”.** A szövegkörnyezet szerint itt az „abszolút használatban” sor illik (`terminologia.tsv:67`).
3. **A brief `ir` mezőjéből hiányzik a `naplok/BDB_FORDITAS_adag12_bontas.md`.**
4. **Ékezet nélküli szavak a `2c4b5fe3` commitüzenetében** (E30, 4 figyelmeztetés).

Saját eljárás (az ellenőr jelzése): néhány parancsban a `git diff`/`git log` kimenetét `grep`/`cut`/`sed`-del szűrte, egyszer `git show`-t futtatott; csak olvastak, de kívül esnek a megengedett parancsok körén.

Verdikt: ELTÉRÉS
