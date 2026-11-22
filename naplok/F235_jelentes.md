# F235 jelentés — Olvasó: sebességjavítás és sebességőr (1. rész)

*Végrehajtó: claude-sonnet-5-5 (a brief `modell: sonnet`, egyezik). Ág: `claude/f235-sebesseg-1-c6fd61`, alap: `origin/main` `95cd2b86`. 2026-11-22. A feladat két részre bomlott (az orkesztrátor döntése, a felhasználó felhatalmazásával): az 1. rész (ez) az `sqlite_epit.py`-hoz és az `indit.sh`-hoz nem nyúl; a 2. rész a #101 merge-e után következik.*

## 1. M0 — a mérés megismétlése és a kiinduló számok

Környezet: WSL `pardes`, venv Python 3.12.3, SQLite 3.45.1; magánmásolat a `pardes.db`-ről (`~/f235/pardes.db`, `meta.epites_ts` = 2026-11-12T18:53:35Z), sima mód, kód a `/mnt/e` munkafáról, DB a gyorsítótárban (`cat pardes.db > /dev/null`). A mérőeszközök a `meres_olvaso_sebesseg_eszkozok/` másolatai (`meres_futtat.py`, `meres_burkolo.py`), egy módosítással: `--varakozas` (az indulás után ennyi másodpercet vár az első kérés előtt, az előmelegítés méréséhez). A terhelés a mérés alatt a többi munkamenet miatt 1,3–2,0 volt (`uptime`): az idők ±20% zajjal terheltek.

A kiinduló mérés (a main `95cd2b86` kódján) a 2026-11-22-i méréssel egyezik: `/1Moz/1` meleg-miss 884 ms (440 SQL), `/Zsolt/119` 2965 ms (1852 SQL), `/1Moz/1/1` 940 ms, `/1Moz/4/7` 1358 ms, `/szo/H1242` első kérés 3555 ms.

## 2. DT-F235a — a javítótábla betöltésének két változata (⛔, az orkesztrátor dönt)

A `bdb_forras_javitas.tsv` 43 828 sor, 14 MB; a három osztály (`heber_sorrend`, `atiras`, `zarojel`) 16 871 `javitva` sort tesz ki. Mérés (`m0_javitas_bench.py`, minimum / medián három futásból):

| Változat | natív WSL | `/mnt/e` |
|---|---|---|
| ma: három külön beolvasás az első H-szó-lapon | 507 / 620 ms | 1784 / 1999 ms |
| (a) egy beolvasás mindhárom osztályra (memóriában, a modulon belül) | 167 / 168 ms | 539 / 552 ms |
| (a) + előszűrés a nyers soron | 120 / 131 ms | 501 / 507 ms |
| (b) DB-tábla, Strongra indexelve: építés (egyszeri, az építőben) | 1405 ms | 5439 ms |
| (b) egy keresés | 0,03 ms | 0,03 ms |

Mindhárom változat kimenete azonos a mai modulé (`A0 == A1 == A2`). Javaslat: (a), mert nincs építő-függés, a `bdb_rovidites.py` kimenete bájtra azonos marad (csak a beolvasás gyorsítótárazása), a `lapgen` és a `lexikon_general.py` ugyanazt a modult használja, míg a (b) két utat követelne (az adatbázis és a TSV). A kérdés elküldve az orkesztrátornak.

**Döntés (2026-11-22): (a)**, szerkesztői döntés (az orkesztrátor, a felhasználó felhatalmazásával). Feltételek: a `bdb_rovidites.py` kimenete bájtra azonos (HAMART-regresszió és lapgen-tesztek), a gyorsítótár szálbiztos (az előmelegítéssel egyidejű első kérés nem olvas be másodszor), és a `/mnt/e`-s 539 ms a 2. rész natív futtatásával tűnik el (az `indit.sh`-ban: a 2. részre jelölve, N-F235c).

**Megvalósítás:** `bdb_rovidites._javitasok_tobb` (egyetlen beolvasás, osztályonként ugyanaz az eredmény), `betolt_javitasok()` (zárral védett, a három gyorsítótárat egyszerre tölti), az `alkalmazas.elomelegit` ezt hívja elsőként. Egységtesztek (`teszt_bdb_rovidites.py` `EgyszeriBetoltes`): a három osztály azonos a régi osztályonkénti beolvasással; kilenc egyidejű hívás (három osztály × három szál, plusz a közvetlen betöltő) pontosan egy beolvasást végez. Mért hatás az első héber szó-lapon előmelegítés nélkül, `/mnt/e`-ről: 3013–3555 → 1880 ms (a gépen közben másik munkamenet lapgen-futása ment: ±30% zaj); előmelegítéssel 131–143 ms.

## 3. Mi változott

| Pont | Változás | Hol |
|---|---|---|
| 2. összevont lekérdezések | `elotoltes()` hatókör és `elotolt_versek` / `elotolt_strongok`: a vers `token_eredeti`, `token_macula`, `lxx_token`, a `morf_nyelv_aramai`, a strong `bdb`, `forditasok` (BDB) és `lxx_bridge` sorai csomagonként (400) egy `IN (...)` lekérdezéssel; a függvények a nyitott gyorsítótárból válaszolnak, másolatot adva a módosítható szerkezetekről | `lekerdezesek.py`, `oldalak.py` (`szamlalok`) |
| 7. lábléc háttérszálon | `LablecFigyelo`: az újraolvasás `ttl` másodpercenként háttérszálon fut; az első kérés szinkron számol; `ttl <= 0` szinkron (a tesztek kapcsolója); a szál a figyelő megszűnésével kilép, elágazás után újraindul | `allapot.py` |
| 5. előmelegítés (alkalmazáson belül) | indulás után háttérszál három bemelegítő kéréssel (`/1Moz/1`, `/szo/H0430`, `/kereses?q=szeretet`) a Flask belső kliensével; `main` és `gunicorn_conf.py` kéri, `PARDES_ELOMELEGIT=0` kikapcsolja; az `indit.sh`-hoz nem nyúltam | `alkalmazas.py`, `gunicorn_conf.py` |
| 8. tervellenőr | `teszt_tervor.py`: az `ast`-tal kigyűjtött minden SELECT `EXPLAIN QUERY PLAN`-ja a tárolt sémán (`teszt_adat/pardes_sema.sql`, `pardes_meretek.tsv`, generált); a CI-ben is fut (`ellenorzes.yml` K14, `push_elott.py` `STATIKUS_TESZTEK`; a `--ci-egyezes` RENDBEN) | új fájlok |
| 8. időkorlát | `teszt_sebesseg.py`: a 300/400/250/50 ms és a 100 SQL, gyorsítótár-találat 20 ms, a helyi `pardes.db`-n | új fájl |

## 4. Újramérés — előtte–utána (ms, sima mód, DB meleg)

„Első kérés”: az indulás utáni első kérés kliensideje. „Meleg-miss”: a lap újragenerálása kiürített lapgyorsítótárral (`X-Meres-Flush`). Az „előmelegítéssel” oszlop az indulás után 12 másodperccel kéri az első oldalt (az előmelegítés lefutott).

| Oldal | előtte: első kérés | előtte: meleg-miss | előtte: SQL | után, előmelegítés nélkül: első kérés | után: meleg-miss | után: SQL | után, előmelegítéssel: első kérés | után: meleg-miss |
|---|---|---|---|---|---|---|---|---|
| `/1Moz/1` | 3067 | 884 | 440 | 629 | 76 | 17 | 94 | 100 |
| `/Zsolt/119` | 3856 | 2965 | 1852 | 728 | 228 | 29 | 246 | 210 |
| `/1Moz/1/1` | 1488 | 940 | 477 | 866 | 290 | 55 | 231 | 245 |
| `/1Moz/4/7` | 2056 | 1358 | 590 | 738 | 201 | 64 | 243 | 201 |
| `/szo/H1242` | 3555 | 153 | 46 | 3013 | 133 | 46 | 131 | 132 |
| `/szo/H7451` | 3301 | 205 | 51 | 3280 | 260 | 51 | 206 | 216 |
| `/szo/G3056` | 249 | 65 | 35 | 294 | 100 | 35 | 86 | 76 |
| `/kereses?q=szeretet` | 150 | 13 | 7 | 199 | 29 | 7 | 3 | 16 |
| `/kereses?q=H7451` | 187 | 22 | 7 | 286 | 37 | 7 | 30 | 33 |
| `/kereses?frazis=Isten+szeretete` | 204 | 10 | 3 | 194 | 9 | 3 | 11 | 7 |

Az SQL-szám a gyorsítótár nélküli kérésben futó utasítások száma. A nyers adatok: `~/f235/m0_alap.jsonl`, `m0_uj_ki.jsonl`, `m0_uj_be.jsonl` (a WSL-ben; nem a repóban).

A `teszt_sebesseg.py` saját mérése (Flask belső kliens, legjobb a három mérésből, gyorsítótár nélkül; a határokkal):

| Oldal | idő | határ | SQL | határ |
|---|---|---|---|---|
| `/1Moz/1` | 79 ms | 300 | 17 | 100 |
| `/Mt/5` | 36 ms | 300 | 12 | 100 |
| `/Zsolt/23` | 44 ms | 300 | 19 | 100 |
| `/Zsolt/119` (a leghosszabb fejezet, 176 vers) | 210 ms | 300 | 29 | 100 |
| `/1Moz/1/1` | 207 ms | 400 | 55 | 100 |
| `/1Moz/4/7` | 208 ms | 400 | 64 | 100 |
| `/szo/H1242` | 138 ms | 250 | 46 | 100 |
| `/szo/H7451` | 192 ms | 250 | 51 | 100 |
| `/szo/G3056` | 62 ms | 250 | 35 | 100 |
| `/kereses?q=szeretet` | 13 ms | 50 | 7 | 100 |
| `/kereses?q=H7451` | 19 ms | 50 | 7 | 100 |
| `/kereses?frazis=Isten+szeretete` | 6 ms | 50 | 3 | 100 |

Minden határ az indexek nélkül, az 1. résszel teljesül; kivétel nincs (`KIVETEL` üres).

## 5. A látható szöveg nem változott

- **A lapok bájtra azonosak:** `osszevet.py` (két szerver, az alap `origin/main` kódja és az új, ugyanazon az adatbázison): 19 oldal (fejezetek: `/1Moz/1`, `/Zsolt/119`, `/Zsolt/22`, `/Mt/5`, `/Dan/2`, `/Ezsd/4`, `/Jer/10`; versek, `?reteg=il`; szó-lapok; kereső; a vers-töredék) a lábléc git-állapotának és az eszköz-verzióhashek kiszűrése után **0 eltérés**.
- **Az F232 mércéje** (`teszt_olvasoi_merce.py`, `PARDES_MERCE_SZIGORU=1`, tehát az eltérés hiba): RENDBEN, a `merce/` fájljai nem változtak.
- A tervellenőr és a sebességőr Python 3.12 (SQLite 3.45.1) és 3.14 (SQLite 3.50.4) alatt is zöld; a CI Python 3.11-et használ (`ubuntu-latest`).

## 6. A tervellenőr leletei (a 2. részre jelölve)

A tervellenőr 23 kéréskor (vagy az első kérésen) futó lekérdezés-függvényt talált, amely 1000 sornál nagyobb táblát olvas végig (`ELFOGADOTT`, célfeladattal; a darabszám rögzített, a lista nem hízhat el, és a javítás után a tételt törölni kell). A brief 2.1 pontja hat táblát nevezett meg; a többi 17 tétel (pl. `forditasok` hét függvénye, `morf_nyelv_aramai`, `nave_basokant`, `lxx_bridge(greek_strong)`, `thayer_*`, `glosszak_heber_hu`, `tbesh` GLOB) a 2. részre marad: `nyitott/uj/f235-sebesseg.md` (N-F235a–d).

A tárolt séma (`pardes_sema.sql`) egyezését a valódi adatbázissal a PARDES_DB-vel futó `test_sema_egyezik_az_adatbazissal` őrzi (a CI-ben nincs adatbázis, ott kimarad); enélkül a tervellenőr elavult tervet nézhetne.

A szándékosan index nélküli próbalekérdezésre a tervellenőr piros: egységtesztje a `test_a_tervor_pirosat_ad_szandekosan_index_nelkuli_probalekerdezesre`, és a CI-ben is bizonyítva lesz egy szándékosan piros ideiglenes committal (a futás azonosítóját a 8. szakasz rögzíti).

## 7. Ami a 2. részre maradt

Indexek és átírt lekérdezések az `sqlite_epit.py`-ban (a `forditasok(szotar, strong)` és a 6. szakasz 17 tétele; a `vers_szamozas` tartomány-lekérdezése; a `token_macula` fedő index), az előre számolt elérhetőségi tábla (`bibliak.Tar`), a natív futtatás és az indításkori háttér-beolvasás az `indit.sh`-ban, a hideg DB újramérése. Lásd: N-F235a–c.

## 8. Ellenőrzések és leletek

| Ellenőrzés | Eredmény |
|---|---|
| HAMART-001, `general.py --cel lexikon2`, a régi (`HEAD`) és az új `bdb_rovidites.py`-val | a három kimeneti fájl (`_TUDOMANYOS.md`, `_KIZARASOK.md`, `_olvasasi_naplo.tsv`) bájtra azonos (`diff -r`) |
| HAMART-regressziós mérce (`lapgen/regresszio.py --id HAMART-001`) | **nem futtatható**: „a mérce bemenete megváltozott: B51 DONTESEK.md; B68 adat/lapgen_bemenetek.tsv; B51 dontesek/uj/f218a-s8d-96a364.md (hiányzik)”. Nem az F235 változása (a `naplok/F218_referencia.tsv` bemenet-hash őr a main saját változásaira vall; az F218a menetei vezetik); a bájtra azonos kimenet fent a közvetlen bizonyíték |
| `python eszkozok/lapgen/tesztek/futtat.py` (az F235.4 commit után) | 367 teszt, 0 hiba, 0 bukás, 21 kihagyva; „RENDBEN F218 mérce hash-őr: a változás nem érinti a lapgenerátort” |
| `python eszkozok/push_elott.py` (teljes, a beolvasztott `main` `4cbefcae` fölött, fej `5cfe8351`) | minden lépés RENDBEN, kivéve az E16 (a PR címe nem `[ELLENŐRZŐ]` előtagú, mert az `ellenorzes.yml` változott); a F232 olvasó-tesztek (`teszt_futtat.py --gyors`) 666 mp, RENDBEN. A cím javítása után `--lepes E2 --pr-cim …`: 0 HIBA |
| `teszt_olvaso_szerver.py` | az első futás egy bukást mutatott (`test_alapjelentes_es_szamlalo_a_blokk_szuresen_at`, 500): az előtöltés a kizárt `forditasok` táblát is olvasta, amikor a BDB nem látszik. Javítva (F235.5: `elotolt_strongok(..., bdb=False)` ilyenkor csak az LXX-hidat tölti); a teljes fájl azóta RENDBEN |
| `teszt_indito.py` (lábléc, beolvasztott main) | 111 teszt, RENDBEN |

Tanulság: az előtöltés kapcsolatszintű authorizer-védelmet kerülhet meg, ha egy tiltott táblát feltétel nélkül tölt; a `szamlalok` a BDB-t csak `magyar_ok` esetén olvasta, az előtöltésnek is így kell. A `teszt_olvaso_szerver.py` ezt fogta meg, a `teszt_sebesseg.py` nem (a belső kiadásban minden tábla olvasható).
