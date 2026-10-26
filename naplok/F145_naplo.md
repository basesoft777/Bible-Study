# F145 — a Thayer-lánc kapujavítása: napló

*Végrehajtó: `claude-sonnet-5-5` (a kért: `sonnet`, egyezik). Ág: `ccr-4d66ac1d-v5f9un` (a `main` + a #142 ága, `origin/ccr-d5dec8d2-infvx9`, `2e60464`,
csak olvasva: a mérés git-fát használ a repón kívül). A mérés eszköze: `naplok/F145_meres.py --gyoker <fa>`; nyers kimenet: `naplok/F145_meres_M0.tsv`,
`naplok/F145_meres_Mz.tsv`. Proveniencia (minden mérésre): `scope=<Strong> | forras=python naplok/F145_meres.py --gyoker <a #142 ágának fája> | ts=2026-10-26`;
a `.py` / `.tsv` olvasása `split('\t')`.*

## M0 — mérés a javítás előtt (F145.1)

**Állapot a #142 ágán (`2e60464`, javítatlan eszközökkel):**

| Mérés | Eredmény |
|---|---|
| `python eszkozok/ellenoriz.py` 13. szabály | **SÉRTÉS (19)**: a 19 új Thayer `sz<n>` sor (G0086 4, G0540 2, G1941 7, G2671 3, G5356 3) `nincs hozzá forrásszöveg`; összesítő: RENDBEN 13 \| SÉRTÉS 1 \| KÉZI 2 \| JELENTÉS 3 |
| `main` (ugyanez) | SÉRTÉS 0 (a 19 sor ott nincs) |
| CI E19 (`futtat.py --valtozott adat/forditasok.tsv adat/lexikon_hivatkozasok.tsv`, #142 fája) | **HIBA 3**: `lexikon_hivatkozasok.tsv` 9. (G0086), 15. (G2671), 19. (G5356) sor — a PR #482 jelzésének reprodukciója |
| `teszt_lanc.py` (main) | 25 teszt, 1 hiba: `test_tabla_determinisztikus_es_kezi_vedett` (fennálló `# forras:` hash-eltérés, nem e feladat) |
| `teszt_lanc.py` (#142 ága) | 25 teszt, 3 hiba: a fenti + `test_g1941_reszei`, `test_beir_kezi_marad` (a két állapotfüggő teszt, DT-F142a) |
| `teszt_bont.py` (main és #142) | 23 teszt, 2 hiba: `test_ellenoriz`, `test_forras_javit_ellenoriz` (fennálló hash-eltérés, nem e feladat) |
| `teszt_forditas_kapuk.py`, `teszt_ellenoriz_13.py` | 90 / 25 teszt, OK |
| `ellenorzes/tesztek/test_szabalyok.py` | 185 teszt, 1 hiba: `E16EsemenyTest.test_push_ures_cimmel_nem_piros` (main-en is; a git-állapottól függ, nem e feladat) |

**A 8 érintett Strong (kontroll-próba, `F145_meres.py` B csoport).** A bukott vázlatok szövege nem maradt meg, ezért a mérés nem fordítás, hanem
egy *kontroll-próba*: a tokenes forrás, a `Homer down` → `Homérosztól kezdve` (terminológia, 5. kapu) és a könyvnév → Károli/apokrif alak
(11. kapu saját táblája, `4 Macc. 2:19` → `4Makk 2:19`) cserével, minden besorolt sigla a tábla magyar alakjára cserélve (a G0012 német műcíme
változatlan). A próba azt méri, a három kapu egyszerre teljesíthető-e.

| Strong | 5. (Homer/down) | 11. | 16. M0 | ok |
|---|---|---|---|---|
| G1311 | RENDBEN | RENDBEN | SERTES: `Homer -> Homérosz hiányzik` | `Homérosztól` — a 16. kapu szó végi határa (DT-F142c i) |
| G5351 | RENDBEN | RENDBEN | SERTES: `Homer -> Homérosz hiányzik` | ugyanaz |
| G1944 | RENDBEN | RENDBEN | SERTES: `Macc. -> Makk hiányzik` | `4Makk`: a `Makk` számjegy mögött (DT-F142c ii) |
| G5010 | RENDBEN | RENDBEN | SERTES: `Macc. -> Makk hiányzik` | `2Makk` ugyanígy |
| G5590 | RENDBEN | RENDBEN | SERTES: `Macc. -> Makk hiányzik` | `1Makk`/`4Makk`; a `Homérosztól` itt is |
| G0012 | RENDBEN | RENDBEN | SERTES: `Philo -> Philón hiányzik` | a `Philo's Lehre von der Weltschöpfung` német műcím változatlan (DT-F142b) |
| G0282 | RENDBEN | RENDBEN | RENDBEN (10 sigla) | a `Philo` egyetlen előfordulása folyó szöveg (`by Philo in de temul.`): `Philón` kell és lehet |
| G4151 | RENDBEN | RENDBEN | RENDBEN (52 sigla) | a `Philo` egyetlen előfordulása folyó szöveg (`Philo's use of τό θεῖον πνεῦμα`) |

*Megfigyelés (DT-F142b leírásához):* a G0282-ben és a G4151-ben a `Philo` nem német műcímben áll (nyers `Philo` részlet: 1/1 és 1/1, a
regex-találat is 1/1); a műcím-kivétel ezért valójában csak a G0012-t érinti. Ezek a #142 „várakozó” Strongjai, nem a kapu miatt: a prózai
`Philo` `Philón`-t kap, a kapu ezt jól követeli.

**A #142 már rögzített 5 Strongja** (G0086, G0540, G1941, G2671, G5356; a `forditasok.tsv` végleges sorai, a rögzítéskor használt
terminológia-kivételekkel): minden kapu RENDBEN (a 16. kapu: 16 / 1 / 28 / 5 / 9 besorolt sigla rendben); a teljes lista: `naplok/F145_meres_M0.tsv`.
