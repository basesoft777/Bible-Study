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

## F145.2 — a 16. kapu (`thayer_kapuk.py`)

A pontos szabályok a modul docstringjében; röviden:

- **(a) változatlan átvétel:** egy sigla-előfordulás átvett, ha utána ≥ 3 szó áll, az első ilyen szó nagybetűs (cím-jelleg), és a sigla szava +
  3 szó (záró írásjel nélkül, szóközre normalizálva) szó szerint, szóhatáron kezdődően megvan a fordításban. A sor csak a nem átvett
  előfordulásokra követeli meg a magyar alakot; ha mind átvett: `N sigla változatlan átvételben, nem ellenőrzött (…)` a részletben (RENDBEN). A
  nagybetűs-első-szó feltétel azért kell, hogy a ⛔ (i) ne álljon elő: a G4151 `Philo's use of τό θεῖον …` és a `Homer, under the word` folyó
  angol szöveg, amelyet a puszta „3 szó szó szerint megvan” szabály átvételnek venne. Ismert, dokumentált határ: nagybetűs szóval induló, 3+
  szavas angol mondatrész fordítatlanul hagyása a siglával együtt a 16. kapun átmegy (a többi kapu és az ellenőr fogja).
- **(b) ragozás-tűrés:** a legalább 4 betűs, nem `könyvrövidítés` cél-alaknál nincs záró szóhatár; rövidebbnél (`Tr`, `WH`) és `könyvrövidítés`nél
  (`Bölcs` ~ `Bölcsesség`) marad. **(c) számjegy-előtag:** `könyvrövidítés` cél-alakja számjegy mögött is találat (`4Makk`).
- **⛔ (ii) mérés — nincs hamis pozitív** (`naplok/F145_ragozas_audit.py`, a #142 fájának összes nem `elavult` `forditas_hu` szövege: 5 238 sor,
  3,44 M karakter, Thayer + BDB): a toldalékot kapó 21 cél-alakból 6-nál van toldalékos találat (9 alak, 14 előfordulás): `Philónnál`,
  `Philónnal`, `Platónnál`, `Xenophónnál`, `Xenophóntól`, `Hérodotosztól`×3, `Homérosztól`×4, `Homérosznál`, `Thuküdidésztől` — mind valódi
  ragozott névalak; más szó eleje egy sem. (A `Sept.` -> `Septuaginta`, a `Josephus`, `Gesenius` stb.: 0 toldalékos találat.)
- Tesztek (`teszt_lanc.py` `Sigla`): `test_atvetel_mucim_pozitiv`, `test_atvetel_hamis_negativ_ellen`, `test_atvetel_nem_mucim`,
  `test_atvetel_valtozatlan_sor_nem_erintett`, `test_ragozas_tures`, `test_szamjegy_elotag_konyvrovidites` (pozitív és negatív minta
  mindhárom esetre; a hamis negatív ellen: a műcím megmaradt, a folyó szövegbeli `Philo` nem `Philón` -> SERTES). A meglévő tesztek
  változatlanok és zöldek (a fennálló `test_tabla_determinisztikus_es_kezi_vedett` kivételével).
- Közbenső mérés a javított kapuval a #142 fáján (a `thayer_kapuk.py` bemásolva a `git`-fán kívüli munkafába): a 8 próba mindegyikén a 16. kapu
  RENDBEN (a G0012: `1 sigla változatlan átvételben`), az 5 rögzített Strong teljes kapusora bájtra azonos az M0-val.

## F145.3 — a 13. szabály Thayer-ága és az E19 szakasz-lefedettsége

**13. szabály (`ellenoriz.py`, F145.3):** a `szotar = Thayer`, `sz<n>` sor forrásszövege a `thayer_bemenet.szakaszok(strong, adat/thayer_szakaszok.tsv,
adat/thayer_forras_javitas.tsv)` szakasza (a `forditas.py rogzit` szövege és `sha1`-e); az `entry_id` a Strong eredeti alakja (`G86`); a
nem `elavult` `sz<n>` sorok együtt a Strong összes szakaszát fedik (a BDB-vel azonos módon, a hibaüzenet a szótárt nevezi meg); a javítótábla
nem illeszkedő sora (`ValueError`) SÉRTÉS az okkal, nem összeomlás. **⛔ (iii) nem állt elő:** a 19 meglévő sor (#142 ága) mindegyikén a
`forras_hash` egyezik; `python eszkozok/ellenoriz.py` a #142 fáján: 13. szabály RENDBEN, SÉRTÉS 0 (M0: SÉRTÉS 19). Tesztek:
`teszt_ellenoriz_13.py` `Szabaly13Thayer` (10 új teszt: rendben, javított nézet, nyers szöveg hash, hibás hash, hiányos lefedés, `elavult`,
táblán kívüli Strong, `entry_id`, szótár-keveredés, nem illeszkedő javítás, hiányzó tábla); 45 teszt, OK.

**E19 (`szabalyok.py` `e19_szotari_forditas_hiany`, F145.3):** a `jelentes_szam = teljes` hivatkozás fedett, ha a (szótár, strong, entry_id) nem `elavult`
(`opus` / `sonnet` / `kezi`) `sz<n>` sorai együtt a Strong szótári szakaszkészletét lefedik (`kell <= van`; a készlet a `thayer_bemenet.szakaszok`-ból,
illetve a `bdb_jelolt/szakasz_bemenet.szakaszok`-ból, az ADAT `thayer_szakaszok.tsv` / `bdb_szakaszok.tsv` tábláiból, vagyis a 13. szabállyal azonos
forrásból); részleges lefedettség, `elavult` / `pilot` szakasz, másik Strong szakaszsora, vagy szakasztábla hiánya nem fed. A `lexikon_hivatkozasok.tsv` nem
változott. Mérés: a #142 fáján `futtat.py --valtozott adat/forditasok.tsv adat/lexikon_hivatkozasok.tsv`: **E19 0 HIBA** (M0: 3). Tesztek:
`test_szabalyok.py` `E19SzakaszTeszt` (7 új: teljes lefedettség — nincs találat; hiányzó Thayer-szakasz, részleges BDB-lefedés, `elavult`/`pilot`, másik Strong,
nincs szakasztábla, nem `teljes` hivatkozás — HIBA); az `E19Teszt` változatlan; 192 teszt, 1 hiba (az `E16EsemenyTest`, `main`-en is).
