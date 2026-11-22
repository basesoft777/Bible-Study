# F232 jelentés — Olvasó: mérce és tesztfuttatás

*Végrehajtó: claude-sonnet-5-5 (a brief `modell: sonnet`, egyezik). Ág: `claude/f232-merce-192772`, alap: `origin/main` `d325f1ae`. 2026-11-22.*

## M0 — a futtatás helye (⛔ DT-F232a): mérések

Minden szám a `naplok/F232_m0_*` szkriptekkel mérve (WSL `pardes` disztró, natív `pardes.db`, `meta.epites_ts` = 2026-11-12T18:53:35Z; a mintakészlet oldalait a Flask-tesztkliens kérte le, a DB-kapcsolat SQLite-authorizere naplózta az olvasott táblákat). A méretek a `dbstat`-ból (tábla + indexei).

### 1. Mely táblák kellenek a mintához

- A mintakészlet 17 oldala (10 szó-lap, 6 versnézet, 2 fejezetnézet; a brief `Jn 1:1`-je a szerverben `Ján` kulccsal él, a `/Jn/1/1` 404-et ad, ezt a mérce írásakor javítani kell) összesen **57 táblát** olvas (`naplok/F232_m0_tablak.json`). Az első lap olvasása után a gyorsítótár miatt a többi lap már kevesebbet mutat; az unió a mérvadó.
- Ennek az 57 táblának a teljes mérete a mai `pardes.db`-ben **956 MB** (az egész DB 1 164 MB). A fele a hat token-tábla: `token_karoli` 183 MB, `lxx_token` 110, `token_macula` 89, `token_eredeti` 85, `token_par` 80, `token_strong` 37.
- A mintához szükséges *sorok* (6 vers, 2 fejezet, a pilot 1Móz 1:1–2:3 szakasz, 10 Strong-szám) a 31 158 versnek durván 1–2 százalékát teszik. **Becslés, nem mérés:** soralapú szűrt DB 15–40 MB között lenne; a pontos számhoz új szűrt-építő kód kellene, ami nincs meg, és a brief `ir` mezőjében sem szerepel (`sqlite_epit.py` csak `olvas`).
- A meglévő tesztek a teljes DB-t várják: `teszt_olvaso_szerver.py` 344. és 983. sora `SELECT COUNT(*) FROM vers = 31158`, a `_wilson`-tesztek az egész korpuszon mérnek. Szűrt DB-n a 112 tesztből álló fő fájl nem futna; csak az új mérce-teszt.

### 2. A repó saját „minta” módja

- `python eszkozok/sqlite_epit.py --mod minta` (1Mózes és a motívumok versei): **264,6 MB**, 104 tábla, az építés 79,8 s, a teljes parancs 3 perc 14 s (WSL, `/mnt/e` lassú fájlrendszerről; natív Linuxon kevesebb). Tehát a repó saját minta-DB-je a 20 MB-os küszöb **13-szorosa**, és nem tartalmazza a Zsolt 22-t és a Ján 1:1-et.
- A `--mod teljes` építési ideje **nem mért** (a 1,16 GB-os DB építése több perc; a `sqlite_epit.py` fejléce szerint a teljes mód „a felhasználó jóváhagyása előtt nem futtatandó”, ezért nem futtattam).

### 3. Licenc (`tabla_licenc`, az 57 tábla)

47 `tisztazott`/`igen`, 6 `kozkincs`/`igen`, és három kivétel: `kjv` **tisztázatlan** (a Strong-címkék GPL-eredetűek, DT124), `mcged` **kereskedelmi felhasználásra nem** (© Mounce 1993), `tw_szocikkek` és `szoveg_kjv` **feltételesen**. A CC BY-SA 4.0 táblák (`lsj`, `sdbh_domenek`, `sdgnt_domenek`, `ubs_dbh_*`, `ubs_dntg_*`) megosztás-azonos feltételűek. Következmény: a **kész teszt-adatbázist a repóba commitolni nem szabad** (a `kjv` tisztázatlan, az `mcged` nem kereskedelmi); a TSV-kből CI-ben építve nincs terjesztett DB, a TSV-ket a repó már tartalmazza.

### 4. CI-futás ideje (a mai `ellenorzes` workflow)

A 45003979537-es futás (main, `b9a168d1`) 3 perc 25 s: a checkout 26 s, az E1 24 s, az E38–E39 29 s, az E41 24 s, a szabály-tesztek 92 s. Az olvasó-tesztek nincsenek benne. Az olvasó-tesztek lokális ideje a `teszt_futtat.py` fejléce szerint kb. 2 perc natívan (a lassú `teszt_szintek.py` kb. 19, `teszt_arculat.py` ugyanebben a listában; **nem mértem újra**).

### 5. A két piros teszt (a 2.4 pont tárgya): lásd a „F232.1” szakaszt lent

## Döntés (DT-F232a)

A felhasználó 2026-11-22-én: „(b) + (a2) mehet” (az orkesztrátor szó szerinti idézetével, a `local_c8cc3610…` session üzenetében). (b) most; (a2) az N-F232a nyitott tétel. Rögzítve: `dontesek/uj/f232-merce-192772.md` (DT-F232a, 🟢), `nyitott/uj/f232-merce-192772.md` (N-F232a, N-F232b).

## F232.1 — a két piros teszt (`dc138f6b`)

Mindkettő **régi szöveget várt a teszt, a kód nem hibás**. Mérve a mai fán, natívan (`teszt_visszhang_kapu.py`) és WSL-ben a `pardes.db`-n (`teszt_szintek`):

| Teszt | Mit vár | Mi a mai, jóváhagyott szöveg | Mikor változott |
|---|---|---|---|
| `teszt_visszhang_kapu` `test_bevezeto_a_peshat_magot_es_a_kulcsszavak_szamat_mondja` | „Peshat-magjának (1Móz 3–9) azon verse” | „A versek a Genezis láncának (1Móz 3–9) azok a versei, amelyekben a kulcsszó…” (az új szerkezetű lap ága, `lexikon_general.py` `uj_szerkezet`) | `cee76546` F125.LJ1 (lap-javit HAMART-001, lektor 23–25.) |
| `teszt_visszhang_kapu` `test_v3_nincs_a_nem_azonositott_helyen` | a cella kisbetűvel kezd („a rokon írások lekérdezése…”) | a cella „A rokon írások…” nagybetűvel kezd (HAMART-001 lap 2107. sor; a generátor kisbetűs mondatrészt ad, `lexikon_general.py` 9803., a lapra a mondatkezdő nagybetűs alak kerül) | a változtató commit nem azonosítva (a `git log -S` a nagybetűs szövegre nem talált) |
| `teszt_szintek` `test_ebben_a_versben_es_az_interlinearis_csempek_koveti_a_blokkok_lathatosagat` | az „Ebben a versben” szöveg a lapon nincs, ha a `vers.ubs` zárt | a BDB-blokk saját doboza (`bdb-ebben`, `blokkok.py` 1470., 2170.) is ezt a feliratot hordozza, és az a `szo.bdb_*` blokkoktól függ, nem a `vers.ubs`-től; a `szo.ebben` blokk valóban nincs a lapon | DT178 (BDB „Ebben a versben” doboz) |

Javítás (teszt, nem kód): az első kettő a mai szöveghez igazítva; a harmadik a `data-blokk="szo.ebben"` hiányát nézi, és azt, hogy minden „Ebben a versben” felirat a BDB-dobozé. Eredmény: `teszt_visszhang_kapu` 22/22 OK (natívan, 12 s), a `teszt_szintek` teszt OK (WSL, 59 s).

*Ok-lánc (hibanapló, mechanizmus szerint):* az olvasó tesztjei sehol nem futottak automatikusan, így a generátor/blokk szövegváltozása a teszt frissítése nélkül ment át. **Javítva az 1. ellenőrzés után (F232.6):** a `teszt_visszhang_kapu` a `lexikon_general.py` és az `olvasoi_kapu.py` változásától lett piros, ami nincs az olvasó-kód listájában; a kapu ezt eredetileg nem fogta volna meg. A `teszt_futtat.py` `GYORS_FUGGO` és a `push_elott.py` `fuggo_tesztek` leképezése a fájl közvetlen bemeneteire futtatja (a `cee76546` fájljaival egységteszt).

## F232.2 — a mérce és a bekötés (`bb260600`)

**Mérce.** `eszkozok/olvaso_szerver/teszt_olvasoi_merce.py` + `merce/` (18 fájl, 540 KB): 10 szó-lap, 6 versnézet, 2 pilot-fejezet. A pillanatkép a lap blokksora (`## [data-blokk]`), a blokkcímek és a látható szöveg; a `<head>`, a `hidden` elemek, az ugrás-link, a láblécek és a figyelmeztető sávok (ág, commit, építési idő) kimaradnak, az ISO időbélyeg és a commit-hash kiszűrve; a csukott `<details>` sorai `▸ `-vel jelöltek. Frissítés csak `--merce-frissit`-tel. Eltérés = `MÉRCE-ELTÉRÉS` sorok (a diff első 60 sora oldalanként; figyelmeztetés, a `PARDES_MERCE_SZIGORU=1` hibává teszi). Hiba: nem 200-as mintaoldal, hiányzó mérce-fájl, nem determinisztikus kép. A normalizáló 7 egységtesztje DB nélkül is fut (a futás: 11 teszt, 3 kimarad DB nélkül, 14 s DB-vel).

*Eltérés a briefhez:* a brief `Jn 1:1`-je a szerverben **`/Jan/1/1`** (a Károli-rövidítés ékezet nélkül: `Ján` → `Jan`; a `/Jn/1/1` és a `/Ján/1/1` 404-et ad). A mérce `Jan`-t használ; a 404 a futásban hiba.

**Bekötés (DT-F232a (b)).** `push_elott.py`: ha az alap..fej diff az olvasó kódját érinti (`teszt_futtat.py` `_OLVASO_KOD`, az egy hely: `olvaso_erintett`), a kapu `teszt_futtat.py --diff <alap>`-ot futtat a helyi `pardes.db`-n; piros teszttel 1-et ad. A lépés nem része a részleges mód lépés-azonosítóinak (`LEPES_AZON` változatlan; a `teszt_push_elott.py` elvárásai érintetlenek), a saját feltétele a teljes diff. A `teszt_futtat.py` a zöld futásnál is kiírja a `MÉRCE-ELTÉRÉS` sorokat. A `--ci-egyezes` zöld (a lépés csak helyi; a CI-ben nem fut).

### Mérések

- **A teljes olvasó-tesztkészlet** (`python eszkozok/teszt_futtat.py`, WSL, natív `pardes.db`, a `bb260600` kódon, a gépen más futás nélkül): 19 fájl zöld, 1 033 mp (a lassú `teszt_szintek.py` + `teszt_arculat.py` 286 mp, a többi 747 mp). **Az 1. ellenőrzés ezt terhelés alatt nem tudta megismételni:** a `teszt_arculat.py` egy tesztje ingadozik (N-F232c), tehát a „mind zöld” csak terheletlen futásra igaz. Kimaradó teszt 2: `teszt_indito.py` 1 (nincs `node`, nem DB-s) és `teszt_olvaso_szerver.py` 1 (`test_bdb_apparatus_jellege…`: „nincs angol-only BDB-szócikk a mintában”, DB-tartalomtól függő kimaradás, N-F232d); a brief 4. feltétele („kihagyott DB-s teszt nélkül”) emiatt a (b)-ben **nem teljesül** teljesen.
- **A mérce eltérésének próbája** (detached HEAD, nem került az ágra): a `blokkok.py` `szo.szotar` blokkcíme „Strong-szótár (PRÓBA)”-ra írva; a `teszt_futtat.py --fajl teszt_olvasoi_merce` zöld, és mind a 10 szó-lapra kiírta a diffet (`-Strong-szótár forrásadat modell-kimenet` / `+Strong-szótár (PRÓBA) forrásadat modell-kimenet`, lap- és sorszámmal). *Első próbálkozásom a `szo.ebben` blokkcímmel semmit nem mutatott: az a blokk csak vers-kontextussal áll a lapon, a mintában nincs; a mérce ezt nem fedi, l. lent.*
- **Piros teszt a kapun** (detached HEAD próbacommit `db565cf3`: egy szándékosan piros teszt a `teszt_ubs_dbh.py`-ban): `push_elott.py --lepes F232` → `HIBA F232 olvasó-tesztek (teszt_futtat.py --diff) [905 mp] (kilépési kód: 1)`, a sor `teszt_ubs_dbh.py: HIBA (1)`, a kapu „A push ne menjen” üzenettel 1-gyel lépett ki. A bizonyíték helyi futás (nincs CI-futás azonosító: a (b) a CI-ben nem fut; az (a2) lesz az, N-F232a).
- **Zár-várakozás:** a `teszt_futtat.py` a közös helyi ellenőrzés-zárat veszi; a párhuzamos F218a S8c session futása alatt a mérce-próbám **1 145 mp-et** várt. Egy olvasót érintő push előtti kapu ezért 17 perc futás + a zárra várás; ez a (b) ára.

### Ismert korlátok (nem hibák)

1. A mérce a **mintán** véd: a `szo.ebben` (vers-kontextusos) blokk és az interlineáris/több-Bibliás nézet nincs benne; ezek az olvasó tesztjeiben vannak.
2. A mérce a `pardes.db` egy építésére (2026-11-12) rögzített; újraépített DB eltérést adhat (adatváltozás, figyelmeztetés).
3. A (b) csak helyi: a PR-t nem védi a CI-ben (N-F232a).
4. A mérce a licenc alá eső táblák szövegét is tartalmazza (pl. `mcged` a G0264 lapon); a repó TSV-i már ugyanezeket tartalmazzák, új terjesztés nincs, de nyilvános repónál ezt a `merce/` mappánál is figyelembe kell venni.

## Független ellenőrzés — 1. ellenőrzés

*(a `fuggetlen-ellenor` válasza változtatás nélkül; head `7d7e83f0`, CI: futás 45011624326, success)*

ELTÉRÉS: 6 tétel

Brief: `F232_OLVASO_MERCE_TESZT_BRIEF.md` · tartomány: `aad45b55..7d7e83f0` · szint: `teljes` (2 kör)

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | A session modellje claude-opus-5-5, a kért modell `opus`: egyezik. A menet `modell`-mezői: a jelentés „claude-sonnet-5-5”-öt ír, az 5 commit `Co-Authored-By: Claude Sonnet 5.5` sort; ez egyezik a brief `modell: sonnet` mezőjével (`git log --format=%b aad45b55..7d7e83f0`). Hogy valóban Sonnet futott-e, azt nem tudom igazolni. Adattábla-sort a menet nem írt. |
| 3 CI | OK | – | `gh run view 45011624326 --json headSha,status,conclusion,jobs`: a headSha `7d7e83f0…`, completed, success (`feladatkovetes`, `ellenorzes`). Generált kimenet nincs a diffben (`git diff --numstat … -- 'lexikon/*' 'nyilt_mag/*' 'generalt*'` → 0 sor). Az E28 és az E29 a CI-ből zöld; a `futtat.py`-t nem futtattam újra. |
| D DT-F232a | OK / NEM ELLENŐRIZHETŐ | `dontesek/uj/f232-merce-192772.md:1` | A ⛔-nél a menet megállt (`cd4a80e0`, `allapot: dontesre_var`), utána 🟢 lett, a döntés szövegével. A felhasználó döntése csak az orkesztrátor idézetéből ismert, nem tudom ellenőrizni. |
| D DT-F232a döntési alap | ELTÉRÉS | `dontesek/uj/f232-merce-192772.md:1` | A (b) változat sora „kb. 2 perc, a lassú tesztek a `--diff` szerint” költséget ír. A lépés viszont csak `_OLVASO_KOD`-találatra indul, és az a `LASSU_LEFEDETT` mindkét lassú fájljának része (`eszkozok/teszt_futtat.py`). Ezért a lassú tesztek mindig futnak. Mért idő: nálam 861,7 + 456,2 mp, a jelentésben 1 033 mp plusz zár-várakozás. A döntés alapjául szolgáló sor alulbecsült költséget mutat. |
| 4.1 piros tesztek javítása (`teszt_visszhang_kapu`) | OK | `eszkozok/olvaso_szerver/teszt_visszhang_kapu.py:84-86, 204-207` | A régi elvárt szöveget igazítja, kódhibát nem fed el. Az új szöveg a `lexikon_general.py:9135-9138` `uj_szerkezet` ágában áll; a nagybetűs cella a `lexikon/HAMART-001_TUDOMANYOS.md:2107`-ben (Grep). `python eszkozok/olvaso_szerver/teszt_visszhang_kapu.py` → 22 teszt, OK. |
| 4.1 piros teszt javítása (`teszt_szintek`) | OK | `eszkozok/olvaso_szerver/teszt_szintek.py:286-291` | A „Ebben a versben” felirat a `blokkok.py:1470/1488` és `2170` BDB-dobozában is áll, a `szo.ebben` blokktól függetlenül. Az új állítás erősebb: a `szo.ebben` hiánya, és minden felirat a BDB-dobozé. Az egyetlen tesztet WSL-ben külön is futtattam → OK, 126,8 s. |
| 4.4 ok-lánc: „ezt a (b) kapu zárja” | ELTÉRÉS | `naplok/F232_jelentes.md:47`; `eszkozok/push_elott.py` `olvaso_erintett` | A `teszt_visszhang_kapu` attól lett piros, hogy a `cee76546` a `lexikon_general.py`-t és az `olvasoi_kapu.py`-t módosította (`git show --stat cee76546`). Egyik sincs az `_OLVASO_KOD`-ban, a `teszt_olvasoi_merce.py:218-220` pedig ki is mondja, hogy a `lexikon_general.py` nem érintett. Ugyanez a hiba ma is átjutna a kapun. Az állítás alátámasztatlan. Az `olvaso_erintett` egységtesztje csak helyben fut, a CI nem futtatja. |
| 4.2 normalizáló | ELTÉRÉS | `eszkozok/olvaso_szerver/teszt_olvasoi_merce.py:88-111` | WSL-ben futtatott `pillanatkep(...)`-próbák: (a) `<p>elotte <span hidden><div>x</div></span> utana</p>` → `'utana\n'`: a látható „elotte” elvész, mert a `_flush` a rejtett elem verembe tétele után fut. (b) `<a>A</a><a>B</a>` → `AB`: a szomszédos inline elemek összetapadnak (a mércében „KJVStrong”, „1Móz2Móz3Móz…”). (c) A CSS-sel rejtett tartalom jelöletlenül „látható szövegként” kerül be (`.jelolo-rovid`, `.szk-rejt`, `.szk-egyben`; `olvaso.css:233,246,484`). (d) A teljes navigáció minden lapon benne van, így egy navigációs változás mind a 18 lapon eltérést ad. Ezek egyike sem szerepel az „Ismert korlátok” között. Időbélyeg és hash a mércében nem maradt (Grep `<hash>`, `<időbélyeg>`, `basesoft`, `/mnt/`: nincs találat). |
| 4.2 determinizmus | OK | – | WSL-ben két hash-seeddel (`PYTHONHASHSEED=1` és `987`) → 11 teszt, OK, `MÉRCE-ELTÉRÉS` nélkül. `PARDES_MERCE_SZIGORU=1` mellett → OK. A HEAD-kódon (a beolvasztott main-nel együtt) a mérce eltérése nulla. |
| 4.3 `push_elott` bekötése | OK | `eszkozok/push_elott.py:551-569` | `python eszkozok/teszt_push_elott.py` → „Minden teszt zöld.”. `python eszkozok/push_elott.py --ci-egyezes` → „RENDBEN: … egyezik”. A `LEPES_AZON` változatlan. A `push_elott` maga nem veszi a zárat, így önmagát nem zárja ki. Piros tesztnél a `Futas.hibas`-on át 1-gyel lép ki (kódolvasás). |
| 4.4 elfogadás 1: zöld, kihagyott DB-s teszt nélkül | ELTÉRÉS | `naplok/F232_jelentes.md:59` | `python eszkozok/teszt_futtat.py --diff aad45b55` → 18 zöld, 1 HIBA: `teszt_arculat.py` `test_a_hash_a_lap_kulcsaban_es_etagjeben` (X-Cache MISS ≠ HIT). Külön futtatva előbb 2-ből 2 OK, a párhuzamos terhelés alatt 3-ból 2 HIBA: terhelésfüggően ingadozó teszt, amely mostantól a kaput is pirosra billentheti. A jelentés „mind zöld” állítását nem tudtam megismételni. A kihagyott tesztek: `teszt_olvaso_szerver.py:526` `test_bdb_apparatus_jellege…` „nincs angol-only BDB-szócikk a mintában”. Ez DB-tartalomtól függő kihagyás, a teszt gyakorlatilag üresen fut; a jelentés ezt nem azonosította, és rosszul találgatott. A `teszt_indito` kihagyása „nincs node”, nem DB-s. |
| 4.4 elfogadás 2: a mérce megmutatja a diffet | OK / NEM ELLENŐRIZHETŐ | `naplok/F232_jelentes.md:60` | A `db565cf3` próbacommit létezik (`git log -1 db565cf3`; a `blokkok.py:2292` környékét módosítja). A kimenet a végrehajtó saját közlése. Az `elteres_sorok` egységteszt zöld. |
| 4.4 elfogadás 3: futás-azonosító | NEM ELLENŐRIZHETŐ | `naplok/F232_jelentes.md:61` | A (b) változatnak nincs CI-futása. A bizonyíték egy helyi futás a `db565cf3`-on, saját közléssel. A kódút (`fut.lepes` → `hibas` → `return 1`) olvasva helyes. |
| 4.4 elfogadás 4 | OK | – | Az (a) változat nem jött, így nem kötelező. |
| 4.5 licenc / `merce/` | ELTÉRÉS | `eszkozok/olvaso_szerver/merce/szo_G0264.txt:60-64` | A mérce MCGED-szöveget („© Mounce 1993 [nem kereskedelmi]”) és „projekt_adat … minden jog fenntartva” fordítást tartalmaz. Az MCGED a repóban már megvan (`git ls-files` → `konkordancia/MCGED_teljes.tsv`), tehát új terjesztés nincs. A `merce/` alatt viszont nincs licenc-megjegyzés, és a jelentés 69. sorában szereplő „figyelembe kell venni” teendőhöz nincs N-tétel. |
| M0: a mintakészlet táblái | OK (megjegyzéssel) | `naplok/F232_m0_olvasott_tablak.py` | A szkript a `/Jn/1/1` útvonalat kérte le, ami 404-et ad. Az 57 tábla így a Ján 1:1 nézet nélkül értendő. A döntést ez nem változtatja meg. |
| A1 | ELTÉRÉS (a 4.4 ok-lánc sorában számolva) | `naplok/F232_jelentes.md:13, 59` | A becslés és a nem ellenőrzött állítás jelölve van. A 47. sor ok-lánc-állítása viszont jelöletlen és téves (l. fent). |
| A2 | OK | `nyitott/uj/f232-merce-192772.md` | N-F232a: a `.github/workflows` alatt nincs `olvaso_tesztek`/`teszt_futtat` (Grep: nincs találat). N-F232b: a `.claude/commands/kovetkezo.md` PUSH ELŐTT szakasza nem említi a lépést (Grep). Mindkettő valóban nyitott. |
| A3–A6 | OK (nem alkalmazható) | – | A diffben nincs tartalmi réteg (adat, motívum, lexikon, tanulmány); E12–E15-figyelmeztetés nincs a CI-ben. |
| K1 törölt sorok | OK | – | `git diff --numstat` szerint 6 törölt sor: brief-fejléc 2, `teszt_szintek` 1 (lecserélt állítás), `teszt_visszhang_kapu` 3 (két lecserélt elvárt szöveg). Adatsor nem törlődött. |
| K2 kulcstartomány | OK | `eszkozok/olvaso_szerver/merce/` | 10 szó-lap, 6 versnézet, 2 fejezet = 18 fájl, egyezik a brief 2.1 pontjával. A `Jn` helyett `Jan` áll, a jelentés jelöli. |
| K3 nulla-diff hatóköre | OK | – | Nulla a mérce eltérése a HEAD-kódon a 2026-11-12-i DB-építésen (a fenti futások). Nem vonatkozik más DB-építésre, a `szo.ebben` blokkra, az interlineáris nézetre, sem a mintán kívüli lapokra. |
| K4 adattábla Δ | OK | – | `git diff --numstat aad45b55..7d7e83f0 -- adat konkordancia` → nincs sor: minden `.tsv`-tábla Δ = 0. |
| K5 ⛔ | OK | – | Az M0 ⛔-nél megállt (`cd4a80e0`); a kód a döntés után készült. Kinézethez és laphoz nem nyúlt (a `blokkok.py` a diffben változatlan). |

ELTÉRÉS-ek súlyossági sorrendben:
1. A kapu nem fogja meg azt a hibamechanizmust, amely a `teszt_visszhang_kapu`-t pirosra vitte: a `lexikon_general.py` és az `olvasoi_kapu.py` nincs az `_OLVASO_KOD`-ban. A jelentés 47. sorának állítása emiatt téves.
2. A `teszt_arculat` terhelésfüggően ingadozik, ezért a push előtti kapu hamis pirosat adhat. A jelentés „19 fájl, mind zöld” eredményét nem tudtam megismételni. Egy DB-tartalomtól függő kihagyás (`teszt_olvaso_szerver.py:526`) azonosítatlan maradt, holott az 1. elfogadási feltétel épp ezt tiltja.
3. A DT-F232a sora „kb. 2 perc” költséggel került a felhasználó elé, a mért idő 17–22 perc.
4. A normalizáló hibái: látható szöveg veszhet el, a szomszédos inline elemek összetapadnak, a CSS-sel rejtett tartalom jelöletlenül bekerül, és a navigáció zaja minden lapon ott van.
5. A `merce/` alatt nincs licenc-megjegyzés, és a jelentés licenc-teendőjéhez nincs N-tétel.

*Az ellenőr utójegyzete:* a `teszt_futtat.py --diff aad45b55` háttérfutásának kilépési kódja 1 (a `teszt_arculat.py` bukásából); az első sor és a táblázat változatlan.

## F232.6 — az 1. ellenőrzés javítókörének (egyetlen kör) kezelése

| # | Eltérés | Kezelés |
|---|---|---|
| 1 | a kapu nem fogja a `lexikon_general.py`/`olvasoi_kapu.py` miatti piros tesztet | javítva: `teszt_futtat.py` `GYORS_FUGGO` + `push_elott.py` `fuggo_tesztek`, a `teszt_visszhang_kapu` külön fut a közvetlen bemenetei változásakor; egységteszt a `cee76546` fájljaival; az ok-lánc mondat javítva |
| 2 | `teszt_arculat` ingadozik; DB-tartalom miatti kimaradás | az `ir`-en kívüli fájlok: N-F232c, N-F232d; a jelentés „mind zöld” állítása pontosítva; a brief 4. feltétele nem teljesül teljesen (l. fent) |
| 3 | a DT-F232a „kb. 2 perc” sora alulbecslés | a döntés sorában utólagos pontosítás (mért 17–22 perc + zár); az orkesztrátornak jelezve |
| 4 | normalizáló: (a) rejtett elem előtti szöveg elvész, (b) szomszédos gombok/hivatkozások összetapadnak, (c) CSS-sel rejtett tartalom, (d) navigáció-zaj | (a) és (b) javítva + egységteszt, a mérce újragenerálva (13 fájl, csak az összetapadás/szóköz); (c) és (d) a modul „Ismert korlátok” szakaszába írva, nem javítva (a DOM-szöveg a mérce tárgya) |
| 5 | nincs licenc-megjegyzés a `merce/` alatt, nincs N-tétel | `merce/README.md` + N-F232e |

A mérce újragenerálása ugyanebben a PR-ban a normalizáló javításának következménye (a lapok tartalma nem változott, a pillanatkép formája igen); a PR leírása jelzi.

## F232.8 — az orkesztrátori döntés (2026-11-22): `--gyors` kapu, egyszeri újrafuttatás

Az orkesztrátor (a felhasználó felhatalmazásával, CLAUDE.md, PR #787): (1) a push előtti kapu az olvasó tesztjeit `teszt_futtat.py --gyors` móddal futtatja (a lassú `teszt_szintek.py` és `teszt_arculat.py` nélkül), a mércével együtt; a teljes tesztsor a menet saját futása a draft PR előtt; (2) egy elbukott tesztfájl egyszer újrafut: ha az ismétlés zöld, a kimenet ingadozást jelez, és a kapu nem áll meg; ha másodszor is piros, megáll; (3) a brief 4. feltétele részben teljesül, elfogadva; (4) a javítókör után nincs új független ellenőrzés.

Megvalósítás (`152df27f`): `push_elott.py` `olvaso_tesztek_futtatasa` (az első futás után az elbukott `[teszt_futtat] <fájl>: HIBA` fájlokat egyszer `--fajl`-lal újrafuttatja; környezeti hiba, kilépési kód 2 és nem azonosítható fájl esetén nincs újrafuttatás); a kapu kiírja, hogy a lassú tesztek nem futottak, és hogy a teljes sor a menet saját futása. 6 egységteszt (`TestKapuUjrafuttatas`: zöld egyszer fut; ingadozás ismétlésre zöld nem bukik; másodszor is piros bukik; két fájl, egyik ingadozik, másik piros; környezeti hiba nem fut újra; nem azonosítható fájl nem fut újra).

**A kapu-próba másodszor** (detached HEAD próbacommit `d1d20b23`, nem került az ágra: egy ingadozó teszt a `teszt_ubs_dbh.py`-ban — elsőre piros, ismétlésre zöld, jelzőfájllal — és egy tartósan piros a `teszt_tanulmany_oldal.py`-ban; `python eszkozok/push_elott.py --lepes F232`):
- első futás (`--gyors`, a lassú fájlok nélkül): **662 mp**, kilépési kód 1, két bukott fájl;
- `FIGYELEM: elbukott olvasó-teszt (teszt_tanulmany_oldal.py, teszt_ubs_dbh.py); egyszeri újrafuttatás`; az ismétlés **8 mp**;
- `FIGYELEM: INGADOZÓ olvasó-teszt (elsőre piros, az ismétlésre zöld): teszt_ubs_dbh.py -- a lépés nem áll meg`, a tartósan piros `teszt_tanulmany_oldal.py` másodszor is bukott: `HIBA: 1 bukott lépés … A push ne menjen`, kilépési kód 1;
- a teljes próba ideje 676 mp (a közös zárra várás nélkül, a gépen más teszt nem futott).

**A teljes tesztsor a végleges kódon** (a menet saját futása a draft PR előtt, `python eszkozok/teszt_futtat.py`, `152df27f`): 19 fájl, **mind zöld**, kilépési kód 0, 768 mp a falióra szerint (a fájlok összege 817 mp: a gyors fájlok 627 mp, a lassú `teszt_szintek.py` + `teszt_arculat.py` 189 mp), `MÉRCE-ELTÉRÉS` nélkül; kimaradt: `teszt_indito.py` 1 (nincs `node`) és `teszt_olvaso_szerver.py` 1 (N-F232d). A korábbi 1 033 mp-es mérés a párhuzamos terhelés nélküli, de más időzítésű futás volt: a költség a géptől és a terheléstől függ (17–22 perc a lassú fájlokkal együtt, a mérések szórnak).

## Zárás

- **Kész:** a két piros teszt javítása (`dc138f6b`, 3 teszt, teszt-oldali: a várt szöveg volt régi); a mérce (`teszt_olvasoi_merce.py`, `merce/`, 18 oldal); a bekötés a push előtti kapuba (`push_elott.py`, `teszt_futtat.py`); az 1. ellenőrzés (ELTÉRÉS, 6 tétel) javítókörrel (`0d9c3a79`).
- **Döntések:** DT-F232a 🟢 (felhasználó, 2026-11-22: „(b) + (a2) mehet”); nyitott: N-F232a (CI a TSV-ből épített DB-n), N-F232b (kovetkezo.md PUSH ELŐTT), N-F232c (teszt_arculat ingadozik), N-F232d (üres kimaradás a teszt_olvaso_szerver.py-ban), N-F232e (merce/ licenc-áttekintés).
- **Nem teljesült teljesen:** a brief 4. feltétele („kihagyott DB-s teszt nélkül zöld”): az N-F232d kimaradás DB-tartalomfüggő, a `teszt_arculat.py` egy tesztje terhelés alatt ingadozik (N-F232c); a feltétel emiatt a (b)-ben csak a terheletlen, teljes futásra igaz. A (b) kapu költsége mért 17–22 perc + a zárra várás; a CI-futás azonosító (4. feltétel 3.) a (b)-nél nincs, a bizonyíték helyi (`db565cf3` próba).
- **A javítókör után nem futott új független ellenőr** (az orkesztrátor döntése: 1 ellenőrzés és legfeljebb 1 javítókör); a javítás ellenőrzése: a normalizáló és a leképezés egységtesztjei, a mérce 14 teszt zöld WSL-ben, a `teszt_visszhang_kapu` zöld, a `E2-E39` zöld helyben.
- **Eltérés a briefhez (egyeztetett):** a `Jn 1:1` mintaoldal a szerverben `/Jan/1/1`.
- **Orkesztrátor figyelmébe:** a DT-F232a sorában az „kb. 2 perc” alulbecslés volt (l. F232.6 #3); az orkesztrátor döntött: a kapu `--gyors` módban fut (F232.8).
- **Az orkesztrátor döntése (2026-11-22) beépítve:** a kapu `--gyors` + egyszeri újrafuttatás (F232.8); a 4. feltétel részleges teljesülése elfogadva; a DT-F232a sora kiegészítve a mért idővel.
