# ELLENOR_F27 — `F27_FP3_BRIEF.md` (v3) · `origin/main (1a5e3a78)..4e4305bd`

*Független ellenőr: `fuggetlen-ellenor` (claude-opus-5-5, a kért `opus`-szal egyező). A jelentést a végrehajtó mentette ide (az ellenőrnek nincs fájlíró eszköze), tartalma szerint, tömörítve. Eredmény: **12 ELTÉRÉS** — az alábbi javítókör zárja (a javítások az F27.7 commitban).*

## Rendben (saját lekérdezéssel igazolva)

- **Modell:** `forditasok.tsv` 185 sor és `bukottak.tsv` 4 sor = `claude-sonnet-5-5`, egyezik a `futasnaplo.tsv`-vel.
- **(1) `forditasok.tsv`:** `numstat` 185 0; egyetlen hunk (`@@ -30249,0 +30250,185 @@`); mind `sonnet`, `claude-sonnet-5-5`, `2026.11.02`, `sz<n>`.
- **(2) kész sorok érintetlenek:** 0 törölt sor; az M1 Strongjaihoz korábban nem volt sor; a 4 bukott Strongnak 0 sora van.
- **(3) költség és kapu:** M1 5,7054 USD, aranyminta 1,1069 USD, tokenek kézzel összeadva egyeznek; 28 `kesz` / 4 `javitando`; 185 = Σszakasz.
- **(4) adagterv, alsó kivetítés (206,7 USD), kategóriaarányok, illesztés:** egyezik.
- **(7) tiltott fájlok:** `git diff --stat` üres.
- **(8) CLAUDE.md:** nincs `csv` modul; `split('\t')` / `'\t'.join()`; proveniencia-sorok megvannak.
- **Lista 4 (tábla-Δ):** csak `adat/forditasok.tsv` +185.

## ELTÉRÉS-ek és javításuk (F27.7)

| # | Tétel | Javítás |
|---|---|---|
| 1 | Kemény plafon átlépve (5,7054 > 5 USD); a javító batch a `javit` tévedésből indult; a jóváhagyás az orkesztrátortól jött, a plafon megadójának forrása a naplóban nincs | A tényt a napló rögzíti (M1, „Plafon”, „Hiba, őszintén”); az orkesztrátor a túllépést tudomásul vette (2026-11-02). A plafont az orkesztrátor adta meg (nem a felhasználó); a DT-F27b a felhasználó elé viszi. **Nem javítható utólag**, N-F27b/g vezeti ki. |
| 2 | CI piros: E9 HIBA (`sense` a G4151 forrásában, `FP3_arany.md:71`) | A `FP3_arany.py` a forrást kódblokkba teszi; újragenerálva; E9 0 találat. |
| 3 | K2: `teszt_bont.py` 2, `teszt_vers_jelentes.py` 1 bukás nem mérve a main-en; `FP3_hibas.tsv` hiányzik | Ugyanezek a tesztek a friss `origin/main` ideiglenes worktree-jében is ugyanígy buknak (igazolva, naplózva). `naplok/FP3_hibas.tsv` létrehozva (adag, strong, kapu, szakasz, ok; 10 sor). |
| 4a | „max_tokens mindkét körben” hamis: az 1. kör `end_turn`, a G1722/G1510 kapun bukott; `max_tokens` csak a javító körben | Napló és N-F27c javítva. |
| 4b | „a költség ~86%-a a prompt” hibás: a bemeneti tokenek ~85%-a, költségben ~53% | Napló és N-F27d javítva. |
| 4c | 310,9 USD indoklása (0,74) nem egyezik: 0,759 az M1+aranyminta együttes aránya | Napló javítva (0,759, 176,76 × 1,759). |
| 4d | „Cor. c, v vessző-alak 0” hamis | Újramérve: 119; napló javítva. |
| 4e | `FP3_M0.py` a head állapotán nem reprodukálja a naplózott M0-t; a `szaraz` ír; `minta` a doc-ot is kiírja | Docstring-megjegyzés (az M0 pillanatának állapota); a commitolt `FP3_sorrend.tsv` az M0 állapota. |
| 5 | DT-F27b „Mért:” / „mért kivetítés” címke a becslésre | Javítva: „Becslés (nem mért)”. |
| 6 | M1-adag a briefen túl bővült (dokumentált); `ir` mezőn kívüli fájlok | A bővítés az orkesztrátor egyeztetett döntése (DT-F27b-be rögzítve); a brief `ir` mezője bővítve a ténylegesen írt fájlokkal. |
| 7 | Az aranyminta javító körének engedélye a repóban nem nyom | Az engedély az orkesztrátor 2026-11-02-i üzenete; a napló rögzíti. |

*Nem ellenőrizhető (az ellenőr nem futtathat szkriptet): sigla 5 758 / 79, `Sir` 536, terminológia-lista; az `ellenoriz.py` / `feladatok.py` eredménye (a végrehajtó futtatta: SÉRTÉS 0, 0 hiba).*

**Összegzés:** a javítókör után a tartalmi eltérések zártak vagy dokumentáltak; a plafon-átlépés és a bővített adag nem visszacsinálható, a felhasználó (DT-F27b) elé kerül.
