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

## F145.5 — a két állapotfüggő teszt (`teszt_lanc.py`, DT-F142a)

Választás: **fixture** (a brief 3. pontjának második útja), mert a `test_g1941_reszei`-nek mindkét állapotot (a sigla-jóváhagyás előtti `javaslat` és az utáni
`besorolt`) igazolnia kell, nem a valódi tábla pillanatnyi állapotát. A `cf.` sor megjelenése külön teszt (`test_g1941_cf_a_sigla_tabla_allapota_szerint`),
`TK.sigla_betolt` helyettesítésével: `javaslat` -> `` `cf.` [besorolatlan a sigla-táblában; a terminológia szerint: `vö.`] ``, `besorolt` -> `` `cf.` → `vö.` ``
(pozitív és negatív állítással); a `test_g1941_reszei` többi állítása (sigla-független) a valódi táblával marad. A `test_beir_kezi_marad` az ideiglenes
`forditasok.tsv`-másolatból a `Thayer G1941 G1941 sz…` sorokat kiszűri (`_forditasok(torol=…)`), és azt is állítja, hogy a régi `teljes` sor megvan: így a valódi
tábla állapotától (G1941 szakaszsorok jelenléte) független. Eredmény: `main`-en és a #142 fáján is a két teszt zöld; a `teszt_lanc.py` egyetlen hibája a
fennálló `test_tabla_determinisztikus_es_kezi_vedett` (`# forras:` hash-eltérés, `main`-en is; M0).

## Mz — mérés a javítás után (F145.7)

Módszer: a #142 ágának fája (`2e60464`, a repón kívüli munkafa), a javított fájlokkal felülírva (`thayer_kapuk.py`, `ellenoriz.py`, `szabalyok.py`, a tesztek,
`SEMA.md`); a fa nem commitolt, nem pusholt. Nyers kimenet: `naplok/F145_meres_Mz.tsv`. Proveniencia: `scope=<Strong> | forras=python naplok/F145_meres.py --gyoker <a javított #142-fa> | ts=2026-10-26`.

| Strong | 16. kapu M0 | 16. kapu Mz | a változás oka |
|---|---|---|---|
| G1311 | SERTES `Homer -> Homérosz` | RENDBEN (9 sigla) | (b) `Homérosztól` találat |
| G5351 | SERTES `Homer -> Homérosz` | RENDBEN (14) | (b) |
| G1944 | SERTES `Macc. -> Makk` | RENDBEN (5) | (c) `4Makk` számjegy mögött |
| G5010 | SERTES `Macc. -> Makk` | RENDBEN (11) | (c) `2Makk` |
| G5590 | SERTES `Macc. -> Makk` | RENDBEN (39) | (b) `Homérosztól` + (c) `1Makk`, `4Makk` |
| G0012 | SERTES `Philo -> Philón` | RENDBEN (11 sigla; 1 változatlan átvételben: Philo) | (a) a `Philo's Lehre von der Weltschöpfung` műcím |
| G0282 | RENDBEN | RENDBEN | nem érintett (a `Philo` folyó szöveg, `Philón` kell) |
| G4151 | RENDBEN | RENDBEN | nem érintett (`Philo's use of …` folyó szöveg) |

Az 5. (`Homer down`) és a 11. kapu a próbán M0-n és Mz-n egyaránt RENDBEN (nem változott; a kontroll-próba azt mutatja, hogy a három kapu egyszerre
teljesíthető). Más kapu nem lazult: a kapusorból csak a `16_sigla` változott; a `forditas_kapuk.py` és a `normalizal.py` érintetlen. **A #142 már rögzített 5 Strongja**
(G0086, G0540, G1941, G2671, G5356): a teljes kapusor eredménye és részlete **bájtra azonos** az M0-val (`diff` üres), minden kapu RENDBEN.

| Mérés (Mz, a javított kód a #142 fáján) | M0 | Mz |
|---|---|---|
| `python eszkozok/ellenoriz.py` | SÉRTÉS 1 (13. szabály: 19) | **SÉRTÉS 0** (RENDBEN 14, KÉZI 2, JELENTÉS 3) |
| `futtat.py --valtozott adat/forditasok.tsv adat/lexikon_hivatkozasok.tsv` E19 | HIBA 3 | **0** |
| `python eszkozok/feladatok.py ellenoriz` | — | 165 brief, 0 hiba, 0 figyelmeztetés |
| `teszt_lanc.py` | 3 hiba | 32 teszt, 1 hiba (a fennálló `test_tabla_determinisztikus_es_kezi_vedett`) |
| `teszt_forditas_kapuk.py` / `teszt_ellenoriz_13.py` / `teszt_vers_jelentes.py` | OK | 90 OK / 45 OK / 9 OK |
| `test_szabalyok.py` | 1 hiba (`E16Esemeny…`) | 192 teszt, ugyanaz az 1 hiba |
| `teszt_bont.py` | 2 hiba | 2 hiba (fennálló hash-eltérés) |

`main`-en (ez az ág) ugyanez: `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba; E19 `--teljes` 0 találat; a tesztek eredménye a fentivel azonos.

**Nem e feladat (fennálló, csak mérve):** a `# forras:` hash-eltérés (`sigla_gyujt.py --ellenoriz`; `teszt_bont.py` `test_ellenoriz`, `test_forras_javit_ellenoriz`;
`teszt_lanc.py` `test_tabla_determinisztikus_es_kezi_vedett`) és az `E16EsemenyTest.test_push_ures_cimmel_nem_piros` `main`-en is bukik (M0). Az oka egyik
esetben sem vizsgálva; javítás/nyitott tétel nincs felvéve.

**Megfigyelések a #142-nek.** (1) A DT-F142b leírásával ellentétben a `Philo` német műcímben csak a G0012-ben áll; a G0282 és a G4151 `Philo`-ja folyó szöveg, ott `Philón` kell
és lehet (a kapu ezt követeli). (2) A 8 Strong *tényleges* újrafuttatása (fordítás) a #142 dolga; a próba csak azt mutatja, hogy a kapu nem akadályoz. (3) A műcím-kivétel
ismert határa: egy nagybetűs szóval induló, 3+ szavas angol mondatrész fordítatlanul hagyása a siglával együtt a 16. kapun átmegy (l. F145.2).

## Javítókör (ELLENOR_F145_1)

- **F145.9 (1a, ELLENOR_F145 1. tétel mechanikus rész):** a `thayer_kapuk.py` műcím-/átvétel-kivétele nem érvényesül a `tipus = rövidítés` sorra (`cf.`, `Cf.`, `Sept.`, `i. e.`); a `ROVIDITES` állandó és a feltétel a `ellenoriz_sigla`-ban, docstring és SEMA 2.37 frissítve. Teszt: `test_atvetel_rovidites_nem_mentesul` (`cf. Winers Grammar, § 12`, forrás = fordítás → SERTES; `vö. Winers Grammar, § 12` → RENDBEN; a Philo-műcím pozitív kontroll RENDBEN). Az `antik szerző`, `modern szerző` stb. típusokat nem módosítottam: az 1b (a szerző-típusú siglák kivétele) tartalmi döntés, a felhasználóra vár. Tesztek: `teszt_lanc.py` 33 teszt, 1 fennálló hiba (a `# forras:` hash-eltérés, `main`-en is); `teszt_bont.py` 2 fennálló hiba (ugyanaz); `teszt_forditas_kapuk.py` 90 OK; `teszt_vers_jelentes.py` 9 OK; `teszt_ellenoriz_13.py` 45 OK.
