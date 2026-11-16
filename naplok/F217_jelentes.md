# F217 — független ellenőrzés és javítókör

*FELADATOK #217 · `F217_GENERALAS_MAINEN_BRIEF.md` · ellenőr: `fuggetlen-ellenor` (claude-opus-5-5) · diff: `72d33fa1..cf524e4d` (F217.2–F217.7) · 2026-11-15 · szint: `teljes` (2 kör)*

## 1. Az ellenőr jelentése (összefoglaló)

**ELTÉRÉS: 7 tétel.** Rendben: a modell (`claude-opus-5-5`, kért: `opus`); a tesztek (`teszt_generalt_nezetek.py` 0 bukott, `teszt_torzscikk_migralt.py` OK, `teszt_push_elott.py` zöld, `test_szabalyok.py` 269 OK a TEMP=E: beállítással); a brief 2.1 (leltár), 2.2 (jegyzék, 11 G-sor, 13 oszlop az O2-módosítás szerint), 2.3 (Action); a két ⛔ pont (a SEMA és a `futtat.py` nincs a diffben, a #729 nincs bent); az O1–O5; a `general.py`, a `lexikon_general.py` és a `lapgen/` érintetlen; a régi lista fogyasztói (csak a tiltás és a teszt); a `migralt_idk()` új jele ugyanazt az 5 ID-t adja, mint a régi lista; a CLAUDE.md szabályai (UTF-8 wrapper, `split('\t')`, proveniencia); A1–A6; a táblák sorszáma (csak az új tábla, Δ = +11).

Helyben futott `futtat.py` (a HAMART-001 lap-ága szűkítve, mert a valós generátor nem futott): E28 marker-blokk 0, E29 0, E35 0; egyetlen HIBA az E16 (a PR az ellenőrzőt érinti: a PR címe `[ELLENŐRZŐ]` előtaggal). A `teszt_szintek.py` 2 FAIL-je (olvasó-szerver) a diff fájljait nem olvassa; régebbi-e, nem ellenőrizte.

| # | Eltérés | Hely |
|---|---|---|
| 1 | Az E28 (4) (őrzött lap) csak indító-mintás diffnél fut, a PR-lépés a 2-es kódot elnyelte: a PR zöld, a main tartósan piros lehet (a lap más bemenetén, pl. `olvasoi_utofeldolg.py`, `konkordancia/*.tsv` át) | `.github/workflows/ellenorzes.yml`, `szabalyok.py` `E28_INDITO_MINTAK` |
| 2 | A (b) számkiosztás-kivétel csak a DT-tokent normalizálta; az olvasói szövegben a feloldott döntésdátum (`szerkesztői döntés, ÉÉÉÉ-HH-NN`) áll | `generalt_nezetek.py`; `lexikon_general.py` `_DT_RX` |
| 3 | Az egyetlen belépési pont: hat eszköz ma is közvetlenül hívja a `general.py --cel lexikon`-t, N-tétel nélkül | `lexikon_ket_ut_meres.py`, `lap_javit_proba.py`, `muhely_allapot.py`, `glossza_lexikon_forditas.py`, `f08/f08_nulladiff.py`, `nulladiff.sh` |
| 4 | Az E29 hatóköre csendben 5 lapról 1-re szűkült (kiesett három kiadott lap) | `szabalyok.py` E29 |
| 5 | A `--gyoker` Windowson meghajtó-eltérésnél `ValueError`-t dob (`os.path.commonpath`) | `generalt_nezetek.py` `gyoker_mod` |
| 6 | A bot-feltétel eseménytípus nélkül a bot által nyitott PR-ra is hat | `ellenorzes.yml` |
| 7 | A MUNKAMENET C5 még a commitolt lapgenerálást írja elő | `MUNKAMENET.md` C5 |

## 2. Javítókör (egy kör, F217.7a)

| # | Javítás |
|---|---|
| 1 | A PR-lépés a kilépési kódot kiírja (`kilepes`), a 2-es kódnál továbbmegy (a kapuk lefutnak), a végső bukás-lépés a `GENERALT_KILEPES`-t is nézi: őrzött lap változásánál a PR piros, az E28 indító-mintájától függetlenül. Helyben a `push_elott.py` ezt eddig is HIBA-ként kezelte. |
| 2 | `_dt_norm`: a DT-token és a `szerkesztői döntés(, dátum)` alak egyaránt normalizált; teszt: `teszt_dt_normalizalas` (a döntésen kívüli dátum nem normalizált). |
| 3 | N-F217d (`nyitott/uj/f217-generalas-mainen-f752cc.md`): a hat közvetlen hívó átkötése a generátorcsere előtt, utána kapu. Az F217 kódja (workflow-k, E28, végrehajtó) csak a belépési pontot hívja; a hat eszköz az F217 hatókörén kívül esik. |
| 4 | Az E29 hatóköre: `generalt_nezetek.migralt_lapok()` (forrás és lap van, törzscikk nincs; a befagyasztottakkal együtt) = a régi lista öt lapja; a teszt: `test_befagyasztott_lap_is_a_hatokorben`. Az E28 továbbra is csak az aktív (nem befagyasztott) lapon generál. |
| 5 | `gyoker_mod`: a `ValueError` (más meghajtó) a repón kívülinek számít. |
| 6 | A szigor és a generálás kihagyása csak `push` eseményen és bot szereplőn (`github.event_name == 'push' && endsWith(github.actor, '[bot]')`). |
| 7 | A MUNKAMENET C5: a lapot a merge után a main-en az Action generálja; átnézéshez helyben `generalt_nezetek.py --ir --id`. |

A PR címe `[ELLENŐRZŐ]` előtagot kap (E16).

## 3. Sorrend a többi ággal

- A `.github/workflows/ellenorzes.yml`-t az F212.2 (a 32 tétel a generátorban, még hátravan) később szintén írhatja: ott sorrendben kell haladni (az orkesztrátor, 2026-11-15). Az F217 változása a fájlban kicsi és elkülönült: két új lépés (ideiglenes generálás, artefakt), egy környezeti változó és egy kilépési kód a meglévő lépésekben, egy tesztsor (`K13`).
- A `feladatok.py fuggesek` KIZAR-sorai: 123 (a régi lista), 205 (`MUNKAMENET.md`), 212 (`ellenorzes.yml`), 223 (`szabalyok.py`); nyitott PR egyik fájlt sem írja (2026-11-15).
