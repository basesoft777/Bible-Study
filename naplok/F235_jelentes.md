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

Az „után” oszlopok az F235.3 commitig mért állapotot mutatják, **a `bdb_rovidites.py` egylépéses betöltése (F235.4) előtt**: ezért a `/szo/H1242` és a `/szo/H7451` első kérése előmelegítés nélkül itt még 3013 és 3280 ms; az F235.4 után a `/szo/H1242` 1880 ms (2. szakasz). „Első kérés”: az indulás utáni első kérés kliensideje. „Meleg-miss”: a lap újragenerálása kiürített lapgyorsítótárral (`X-Meres-Flush`). Az „előmelegítéssel” oszlop az indulás után 12 másodperccel kéri az első oldalt (az előmelegítés lefutott).

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

A tervellenőr 23 kéréskor (vagy az első kérésen) futó lekérdezés-függvényt talált, amely 1000 sornál nagyobb táblát olvas végig (`ELFOGADOTT`, célfeladattal; a darabszám rögzített, a lista nem hízhat el, és a javítás után a tételt törölni kell). A brief 2.1 pontja hat táblát nevezett meg; a brief hat táblájára 13 függvény esik, a másik 10 (`morf_nyelv_aramai`, `nave_basokant`, `lxx_bridge(greek_strong)`, `thayer_*`, `glosszak_heber_hu`, `tbesh` GLOB, a `bibliak.Tar` összesítői, a frázis-kereső) nem volt a briefben; mind a 2. részre marad: `nyitott/uj/f235-sebesseg-1-c6fd61.md` (N-F235a–d).

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
| Szándékosan piros próba a CI-ben (brief 4.) | futás **45055950279** (fej `89be94d0`, ág `claude/f235-tervor-piros-proba`, PR #800 zárva): a `Szabaly-tesztek` lépés bukott, a log sora szó szerint: `AssertionError: Lists differ: [('f235_piros_proba', 'token_macula', 'SCAN token_macula')] != []`. A zöld futás: **45053969709** (fej `5cfe8351`) és **45057462624** (fej `40e84a7e`), mindkettőben a K14 lépés (`teszt_tervor.py`) |

Tanulság: az előtöltés kapcsolatszintű authorizer-védelmet kerülhet meg, ha egy tiltott táblát feltétel nélkül tölt; a `szamlalok` a BDB-t csak `magyar_ok` esetén olvasta, az előtöltésnek is így kell. A `teszt_olvaso_szerver.py` ezt fogta meg, a `teszt_sebesseg.py` nem (a belső kiadásban minden tábla olvasható).

## Független ellenőrzés — 1. ellenőrzés

*Az ellenőr (`fuggetlen-ellenor`, modellje `opus`) jelentése változtatás nélkül. Megjegyzés a híváshoz: a `model` paraméter nélküli hívás `claude-fable-5-2`-n futott, ezért az ellenőr a „Modell-ellenőrzés” szerint megállt és munkát nem végzett; az orkesztrátor döntésére (2026-11-22) a hívás explicit `model: "opus"` paraméterrel ismétlődött, és a futó modell `claude-opus-5-5` volt, egyezik a kért `opus`-szal. Az ellenőrzött tartomány `4cbefcae..40e84a7e`; a javítókört a „Javítókör” szakasz írja.*

ELTÉRÉS: 9 tétel

**Brief:** `F235_OLVASO_SEBESSEG_BRIEF.md` (1. rész) · **tartomány:** `4cbefcae..40e84a7e` · **szint:** teljes, 2 kör (`python eszkozok/feladatok.py szint 235` → `SZINT #235 teljes 2 kör`)

A modellem `claude-opus-5-5`, a kért modell `opus`: a kettő egyezik. A menet `modell` mezői és a Co-Authored-By sorai a végrehajtó tényleges modelljét mutatják (Sonnet 5.5, a brief `modell: sonnet` mezőjével egyezik).

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | `naplok/F235_jelentes.md:3` | `git log --format="%h %(trailers:key=Co-Authored-By,valueonly)" 4cbefcae..40e84a7e` → Claude Sonnet 5.5; a jelentésben `claude-sonnet-5-5` áll |
| CI (head) | OK | – | `gh run view 45057462624 --json status,conclusion,headSha` → completed, success, headSha 40e84a7e (= head); E2–E37 a CI-ből, `futtat.py`-t nem futtattam újra |
| CI piros próba (brief 4.) | OK | – | `gh run view 45055950279` → failure, ág `claude/f235-tervor-piros-proba`, head 89be94d0; a log szerint `test_kereskor_futo_lekerdezes_nem_olvas_vegig_nagy_tablat` bukott: `[('f235_piros_proba','token_macula','SCAN token_macula')] != []`. A próba-commit csak `lekerdezesek.py` +5 sort hoz (`git diff 40e84a7e 89be94d0 --stat`) |
| **ELTÉRÉS 1** – 2.3 / DT-F235a feltétele („egyszer töltődik”; „az egyidejű első kérés nem olvas be másodszor”) | ELTÉRÉS (közepes) | `eszkozok/bdb_rovidites.py:354-362`, `eszkozok/olvaso_szerver/blokkok.py:889` | A `betu_javitasok()` (F185 P4) változatlanul külön, zár nélkül olvassa be a 14 MB-os `bdb_forras_javitas.tsv`-t. A `betolt_javitasok()` nem tölti; a hívása a `heber_sorrend_javit(..., betu=True)` alapértékén keresztül az olvasóban minden héber BDB-szövegen fut. Az alapban 4 beolvasás volt, nem 3 (`git show 4cbefcae:eszkozok/bdb_rovidites.py \| grep -n "open(ut or JAVITAS_UT"` → 120 és 339. sor), most 2. Az M0-mérés és a döntés tehát háromról beszél. Az előmelegítő szál és az első szó-lap kérés egyszerre kétszer is beolvashatja az `_BETU`-t. A kimenetet nem érinti |
| **ELTÉRÉS 2** – az előtöltés egyezésének őre | ELTÉRÉS (közepes–alacsony) | `eszkozok/olvaso_szerver/lekerdezesek.py:65-67` | A megjegyzés szerint az egyezést „a teszt_sebesseg.py és a teszt_olvaso_szerver.py egyezésvizsgálata” őrzi. `Grep elotolt\|elotoltes eszkozok/` → egyetlen tesztfájlban sincs találat, és a `teszt_sebesseg.py` sem vet össze. A megjegyzés állítása téves; a cache-ágakat közvetlen teszt nem fedi. Mérséklő tények: a `teszt_olvasoi_merce.py` zöld, és a saját összevetésem 28 oldalon 0 eltérést adott (l. „nulla-diff” sor) |
| **ELTÉRÉS 3** – brief 4. („piros … a futás azonosítójával”) | ELTÉRÉS (alacsony–közepes) | `naplok/F235_jelentes.md:89`, 95–104 | A 89. sor ígéri, hogy a futás azonosítója a 8. szakaszba kerül, de ott nincs. `git grep -n "45055950279\|f235-tervor-piros\|#800" 40e84a7e` → nincs találat (csak bináris LSJ). A PR #799 leírásában sem szerepel |
| **ELTÉRÉS 4** – a jelentés belső ellentmondása | ELTÉRÉS (alacsony) | `naplok/F235_jelentes.md:27` és `:49-50` | A 2. szakasz szerint a `/szo/H1242` első kérése „3013–3555 → 1880 ms”, vagyis a 3013 előtti érték. A 4. táblázat ugyanezt a 3013-at az „után, előmelegítés nélkül” oszlopba írja, a H7451-nél pedig 3301 → 3280 áll. Ez az oszlop láthatóan az F235.4 (bdb) előtti állapotot mutatja, jelölés nélkül. Ugyanitt a 85. sor „a többi 17 tétel” megfogalmazása nem egyezik a függvényszámmal: a brief hat táblájára 12 függvény esik, a többi 11 |
| **ELTÉRÉS 5** – brief 4. / DT-F235a („HAMART-regresszió RENDBEN”) | ELTÉRÉS (alacsony; jelentésben nyíltan jelölt) | `naplok/F235_jelentes.md:100` | A `lapgen/regresszio.py --id HAMART-001` nem futott le (a bemenet-hash őr a main saját változása miatt állt meg). Helyette a lexikon2 kimenet bájtra azonosságát hozták. Saját ellenpróbám: `python eszkozok/teszt_bdb_rovidites.py` → 42 teszt OK, köztük az `EgyszeriBetoltes`. A régi `_javitasok` és a `_javitasok_tobb` kódja soronként egyenértékű (`tab.get(d.get('hiba'))` ≡ `d.get('hiba') == hiba`). A feltétel formálisan nem teljesült; elfogadásához kifejezett döntés kell. Lapgen-tesztet nem indítottam (tiltott) |
| **ELTÉRÉS 6** – 2.7 lábléc háttérszálon | ELTÉRÉS (alacsony) | `eszkozok/olvaso_szerver/allapot.py:413-425` | (a) A `_szal_indit` zár nélkül vizsgálja és írja a `_szal_pid`-et: két egyidejű első `kap()` két háttérszálat indíthat. Ez dupla frissítést okoz, hibát nem. (b) A háttérfrissítésre nincs teszt: a `TesztLablecFigyelo` (`teszt_indito.py:188-198`) csak a ttl=3600 és a ttl=0 ágat nézi. (c) Viselkedésváltozás, dokumentálatlanul: a szál üresjáratban is 3 másodpercenként fut (`Lablec.keszit` → `adat_allapot`, a 452 fájl `stat`-ja, `db_epites_ts` a Windows-oldali DB-n, git-ref olvasás). Korábban ez csak kérés esetén futott. (d) `--preload` mellett elágazáskor a nem újrainduló szálak zárállapota öröklődhet; az alapkonfigban nincs preload (`gunicorn_conf.py`), ezért itt csak kockázat |
| **ELTÉRÉS 7** – 2.5 előmelegítés | ELTÉRÉS (alacsony) | `eszkozok/olvaso_szerver/alkalmazas.py:59-67`, `gunicorn_conf.py:9` | (a) Az `except Exception: pass` minden hibát némán elnyel, napló nélkül. Az `elomelegit`-et teszt nem hívja (`Grep elomelegit\|ELOMELEGIT` a teszteken → csak `elomelegit_ki=False`), így egy regresszió az előmelegítést észrevétlenül kikapcsolná. (b) A `gunicorn_conf.py` `setdefault` sora az `m4_meres.py` hideg méréseit is bemelegíti, és ott a háttérszál versenyez a mért kéréssel. A `blokkok.bdb_rovidites` attribútum létezik (`blokkok.py:48`). A belső szál saját, szálhelyi DB-kapcsolatot kap (`adatbazis.py:59-63`), a lapgyorsítótár zárt (`gyorsitotar.py:13`): ezek rendben |
| **ELTÉRÉS 8** – tervellenőr: téves negatív kockázatok | ELTÉRÉS (alacsony) | `eszkozok/olvaso_szerver/teszt_tervor.py:48-75`, 173-187, 249-258 | (a) Az `ELFOGADOTT` függvényszintű: egy elfogadott függvényben ugyanarra a táblára írt új, végigolvasó lekérdezés átmegy. (b) A `SEARCH … USING AUTOMATIC (COVERING) INDEX` sort nem jelzi, pedig az is teljes olvasás; hogy ma előfordul-e, a megengedett parancsokkal NEM ELLENŐRIZHETŐ. (c) A `test_sema_egyezik` csak nevet hasonlít, oszlopot nem: egy azonos nevű, de más oszlopú index nem bukik. A CI-ben ez a teszt kimarad. (d) A `pardes_meretek.tsv`-ből hiányzó tábla 0 sornak számít. Rendben levő pontok: `python eszkozok/olvaso_szerver/teszt_tervor.py -v` → 5 teszt, OK (1 skip), SQLite 3.50.4; WSL-ben `PARDES_DB=~/f235/pardes.db` mellett 5 OK, köztük a séma-egyezés (3.45.1). `--listaz` → 159 lekérdezés, 31 `SCAN!` sor; `len(ELFOGADOTT)`=23=`ELFOGADOTT_DB`. Az `EGYSZERI` függvényei mind a `Kozos.__init__`-ben futnak (`oldalak.py:107-124`). Nem SELECT-tel kezdődő SQL, f-string vagy `.format` a `lekerdezesek.py`-ban nincs; a dinamikus darabok előtag-SQL-ként bekerülnek |
| **ELTÉRÉS 9** – nyitott tételek és PR | ELTÉRÉS (alacsony) | `nyitott/uj/f235-sebesseg.md`, PR #799 | (a) A fájlnév nem `<ágnév>.md` (`f235-sebesseg-1-c6fd61.md`), szemben a CLAUDE.md szabályával; a `szamkiosztas.py` globbal olvas, ezért működik. (b) Az N-F235a az `ubs_dbh_referenciak(igehely)`-t „a többi” közé sorolja, pedig ez a brief 2.1 hat táblájának egyike. (c) A PR leírása szerint az N-F235a–d mind a 2. részé, holott az N-F235d célja a #232. Mind a négy N-tételnek van megnevezett célfeladata: OK |
| 2.2 összevont lekérdezések (≤100 SQL) | OK | `oldalak.py:581-594` | WSL, `PARDES_DB=~/f235/pardes.db … teszt_sebesseg.py -v` → `/1Moz/1` 86 ms, 17 SQL · `/Zsolt/119` 203 ms, 29 SQL · `/1Moz/1/1` 190 ms, 55 SQL · `/1Moz/4/7` 177 ms, 64 SQL · `/szo/H7451` 201 ms, 51 SQL. 3 teszt OK; a jelentés táblázatával ±10%-on belül egyezik |
| 2.8 sebességőr, határok | OK (megjegyzéssel) | `teszt_sebesseg.py:34-54, 102` | A határok (300/400/250/50 ms, 100 SQL, találat 20 ms) a briefével egyeznek, a `KIVETEL` üres. Apróság: az SQL-szám a három mérés minimuma, nem a „legjobb mérésé” (102. sor és a docstring) |
| előtöltés: sorrend, első sor, üres kulcs, másolat, 400-as csomag, tiltott tábla, élettartam | OK | `lekerdezesek.py:72-148`, 330-410, 718-870 | Kódolvasás alapján. ORDER BY verzión belül azonos (`igehely, sorszam` ≡ `sorszam`; `igehely, rowid` ≡ `rowid`; az lxx_token CAST-sorrendje azonos). A bdb első sora rowid-sorrendben, ahogy a régi `fetchone`. Hiányzó kulcsra `None`, illetve `[]`. A macula és az lxx_sorr dict-másolatot ad. A csomagolás nem vág szét kulcsot. A `bdb=False` ág nem olvassa a `forditasok`-at. A `finally` `None`-ra állít, a beágyazott hívás a külső hatókört használja. Az `aramai_xml` dict-sorrendje eltér, de a hívó (`oldalak.py:129`) csak kulcs szerint olvas |
| nulla-diff (látható szöveg) | OK (hatókör alább) | – | `osszevet.py ~/f235/alap <munkafa> ~/f235/pardes.db …` két futása 28 új oldalon, mindkettő „ELTÉRŐ oldal: 0”: /Jel/22, /Neh/7, /Zsolt/51, /Ezsd/7, /Dan/7, /Jer/52, /Eszt/3, /Mal/3, /2Kir/18, /Zsolt/51/1, /Dan/7/13, /Zsolt/119?reteg=il, /szo/H0430, /szo/H1121, /Jan/1, /Rom/8, /Jel/1, /Zsid/1, /Mk/16, /Mk/16/9, /Rom/8/28, /Ez/37, /Joel/3, /Mal/4, /szo/G0026 és további. Megjegyzés: az `~/f235/alap` a `95cd2b86` (régi main) kódja, nem a `4cbefcae`-é (`git diff --no-index --stat`) |
| tesztek (Diéta 3) | OK | – | `python eszkozok/teszt_futtat.py --diff 4cbefcae` → mind a 21 fájl zöld, köztük a lassú `teszt_szintek.py` (169,7 mp) és `teszt_arculat.py`, valamint `teszt_olvaso_szerver.py`, `teszt_olvasoi_merce.py`, `teszt_indito.py` és `teszt_sebesseg.py`. `python eszkozok/teszt_bdb_rovidites.py` → 42 OK |
| CI-bekötés | OK | `.github/workflows/ellenorzes.yml:281-284`, `push_elott.py:81` | `python eszkozok/push_elott.py --ci-egyezes` → „RENDBEN: a push_elott.py lépéslistája és a workflow egyezik.” |
| D: DT-F235a | OK | `dontesek/uj/f235-sebesseg-1-c6fd61.md` | Az (a) változat valósult meg, helyőrzővel, az orkesztrátor döntésével. A döntés a 8300b684-ben került be, a megvalósítás a 94391122-ben. A döntés feltételeiről l. ELTÉRÉS 1 és 5 |
| A1 | OK | `naplok/F235_jelentes.md` | A számok mérésből származnak, és a nyers fájl helye meg van adva. A tartalmi állítást nem hoz |
| A2 | OK | `nyitott/uj/f235-sebesseg.md` | Az N-F235a–d valóban nyitott. Az `sqlite_epit.py` és az `indit.sh` érintetlen (`git diff --stat` → nincs a listában), az `ELFOGADOTT` 23 tétele áll |
| A3–A5 | nem alkalmazható | – | A diffben nincs tartalmi réteg (adat, motívum, lexikon, forrás); `git diff --name-only … -- adat konkordancia` → 0 |
| A6 | OK | – | A CI-futás sikeres, E12–E15 figyelmeztetést nem kellett megítélni |
| lista 1 – törölt sorok | OK | – | `git diff --numstat` → 52 törölt sor, mind kódsor-átírás a `lekerdezesek.py`, `allapot.py`, `oldalak.py`, `bdb_rovidites.py`, `alkalmazas.py`, `ellenorzes.yml` és a brief fejlécében. Törölt fájl: 0 (`--diff-filter=D` → 0) |
| lista 2 – kulcstartomány | OK | `teszt_tervor.py:76` | Adatkulcs nem változott; az előtöltés minden kért kulcsot feltölt, a hiányzót üresen |
| lista 3 – a nulla-diff hatóköre | OK, korláttal | – | Csak a `belso` kiadásra vonatkozik, a lábléc git-állapotának, a `?v=` hasheknek és a „Figyelem” soroknak a kiszűrésével, meleg DB-n. Nem fedi a `nyilvanos`/`kereskedelmi` kiadást (a `bdb=False` ágat), azt csak a `teszt_olvaso_szerver.py` (zöld) őrzi |
| lista 4 – táblák sorszám-Δ | OK | – | `git diff --numstat 4cbefcae..40e84a7e -- adat konkordancia` → üres: minden `.tsv` Δ=0. A `teszt_adat/pardes_meretek.tsv` új, generált tesztbemenet (109 sor), nem adattábla |
| lista 5 – ⛔ | OK | – | A DT-F235a a megvalósítás előtt döntve; az `sqlite_epit.py`-hoz és az `indit.sh`-hoz nem nyúltak |

**Az eltérések súlyosság szerint:**
1. A javítótábla negyedik beolvasása (`betu_javitasok`) kimaradt az egyszeri, zárolt betöltésből. A brief 2.3 pontja és a DT-F235a szálbiztossági feltétele ezért csak részben teljesül.
2. Az előtöltés egyezésére nincs teszt, holott a kódmegjegyzés állítja, hogy van.
3. A piros próba futásának azonosítója (45055950279) nincs a jelentésben, pedig a jelentés maga ígéri.
4. A HAMART-regresszió formálisan nem futott; elfogadásához kifejezett döntés kell.
5. A jelentés 2. és 4. szakaszának számai ellentmondanak egymásnak.
6. Kisebb tételek: a lábléc-szál versenyhelyzete és üresjárati terhelése, a néma előmelegítés, a tervellenőr téves-negatív résein, valamint a nyitott-fájl neve és a PR-leírás pontatlanságai.

## Javítókör (az 1. ellenőrzés után, a legfeljebb egy kör)

| Lelet | Intézkedés |
|---|---|
| 1 (negyedik beolvasás) | Javítva: a `bdb_rovidites.betu_javitasok()` gyorsítótára zárolt (`_BETU_ZAR`, kétszeres ellenőrzés), a `betolt_javitasok()` ezt is tölti, tehát az előmelegítő szál mindkét táblát betölti, és az egyidejű első kérés megvárja, nem olvassa be másodszor. Maradt két beolvasás: a három osztály egyben, és a betűjavítás külön (más sorszűrés); mindkettő egyszeri és zárolt. A `teszt_bdb_rovidites.py` `EgyszeriBetoltes.test_egyszerre_kert_betoltes_egyszer_olvas` a betűjavítást is számolja (egy beolvasás, 15 szálindítás után). A kimenet változatlan (a `_betu_szamol` törzse a régi kód) |
| 2 (az előtöltésnek nincs tesztje) | Javítva: `teszt_sebesseg.py` `test_az_elotoltes_ugyanazt_adja_mint_az_egyedi_lekerdezes` (kilenc fejezet: Zsolt 119/78/89/105, 1Móz 1–3, Dán 2, Ezsd 4: >400 vers és >400 strong, tehát a csomaghatáron át; eredeti szavak, Macula, LXX, arámi nyelv, BDB angol és magyar, jelölés, LXX-híd, hiányzó strong; az előtöltött hatókörben <20 SQL; a hatókör után nincs szivárgás) és `test_a_tiltott_tabla_nem_olvasodik_az_elotoltesben`. A téves megjegyzés (`lekerdezesek.py`) javítva |
| 3 (a piros futás azonosítója a jelentésben) | Javítva, l. a 8. szakasz: futás **45055950279** (fej `89be94d0`, ág `claude/f235-tervor-piros-proba`, PR #800 zárva). Tartós védelem: a `teszt_tervor.py` `test_a_tervor_pirosat_ad_szandekosan_index_nelkuli_probalekerdezesre` (negatív eset az egységtesztben) és az ellenőrzési tartomány kapuja |
| 4 (a jelentés számai) | Javítva: a 4. szakasz az „után” oszlopokat az F235.4 előttiként jelöli; a hat tábla / függvényszám (13 + 10) a 6. szakaszban és az N-F235a szövegében |
| 5 (HAMART-regresszió formálisan) | Nem javítható itt: a `regresszio.py` bemenet-hash őre a main változásai miatt áll (a mérce az F218a menetéé). Az F235 bizonyítéka: a lexikon2 kimenet régi és új modullal bájtra azonos, a lapgen-tesztek 367/0. Az elfogadás az orkesztrátor döntése (a zárójelentés kérdése) |
| 6 (lábléc) | Javítva: a szálindítás zárolt (`_szal_zar`); két új teszt (`teszt_indito.py` `test_a_hatterszal_ttl_utan_frissit_es_a_kerest_nem_szamol`, `test_ket_egyideju_elso_kerest_egy_hatterszalat_indit`); az üresjárati újraolvasás dokumentálva a `LablecFigyelo` leírásában |
| 7 (előmelegítés) | Javítva: a hiba rögzül (`elomelegit_hiba`) és a `stderr`-re íródik; teszt: `teszt_sebesseg.py` `test_az_elomelegites_lefut_es_a_lapgyorsitotarba_tolt`. A `m4_meres.py` hideg mérésénél `PARDES_ELOMELEGIT=0` kell (README) |
| 8 (tervellenőr) | (a) és (b) elfogadott, kimondott korlát a modul leírásában; (c) javítva: a `test_sema_egyezik_az_adatbazissal` a séma SQL-szövegét is összeveti (oszlopok és index-oszlopok); (d) javítva: új `test_minden_tabla_szerepel_a_meretek_kozott` (a CI-ben is fut) |
| 9 (nyitott fájl, PR) | Javítva: `nyitott/uj/f235-sebesseg-1-c6fd61.md` (átnevezve), az N-F235a szövege a 13 + 10 függvénnyel, a PR leírása az N-F235d célfeladatával (#232) |

## Zárás

- **Teljesült (1. rész):** a lapszintű előtöltés (≤100 SQL laponként: 17–64 a mért oldalakon), a lábléc háttérszálon, az alkalmazáson belüli indulási előmelegítés, az egyszeri, szálbiztos javítótábla-betöltés (DT-F235a (a), az orkesztrátor döntése), a tervellenőr (CI-ben zöld, szándékosan piros próbán piros: futás 45055950279) és az időkorlát-teszt (minden határ teljesül, `KIVETEL` üres); az előtte–utána újramérés a 4. szakaszban.
- **Nem teljesült vagy részben:** a HAMART-regressziós mérce (`regresszio.py`) nem futtatható (a bemenet-hash őr a main változásai miatt áll, nem az F235 miatt); helyette a HAMART-001 lexikon2 kimenete régi és új modullal bájtra azonos, a lapgen-tesztek 367/0. A hideg lemez (kiürített gyorsítótár) és a `/mnt/e` kódhely költsége az 1. részben nem javul (N-F235c).
- **Egyeztetett eltérés:** a feladat két részre bomlott (orkesztrátor, a felhasználó felhatalmazásával, 2026-11-22); az 1. rész az `sqlite_epit.py`-hoz és az `indit.sh`-hoz nem nyúl. A független ellenőr első, `model` nélküli hívása `claude-fable-5-2`-n futott, ezért nem dolgozott; az orkesztrátor döntésére explicit `model: "opus"` paraméterrel ismétlődött.
- **Nyitott (a 2. részre, `nyitott/uj/f235-sebesseg-1-c6fd61.md`):** N-F235a (23 végigolvasó lekérdezés-függvény: indexek, átírt lekérdezések, utána `--sema-ment`), N-F235b (frázis-kereső terve), N-F235c (hideg lemez, natív futtatás, indításkori háttér-beolvasás, hideg újramérés), N-F235d (az időkorlát-teszt a CI-ben, a #232-vel).
- **Döntés kell (az orkesztrátortól):** a HAMART-regressziós mérce formális feltétele helyett a fenti bájtazonos bizonyíték elfogadása.
