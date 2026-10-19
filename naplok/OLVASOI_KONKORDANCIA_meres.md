# OLVASOI_KONKORDANCIA — M4 mérés (#76)

*Végrehajtói mérés (`claude-opus-5-5`; a brief `modell: opus`), nem független ellenőri. Ág: `claude/olvasoi-konkordancia-m3`, HEAD a mérés idején `7e4b6c5c` (merge a main-ről; az M3 és a javítókör F76.42–F76.55 rajta), a munkafán az új `eszkozok/olvaso_szerver/m4_meres.py`. A szerver kódja a mérés alatt nem változott. A Windows-WSL2 mérés tájékoztató (DT146/5); a mérvadó szám az M6 (VPS) mérése lesz.*

## 0. Összefoglaló

| Elfogadás | Eredmény |
|---|---|
| **K1 (D2)** | 1Móz 1–25: 21 991 összevetés, Zsolt 22: 3 022 összevetés; **az egyetlen eltérő blokk-csoport a `gorog_szo:usz_elofordulas`** (27 + 11 görög szó-lap), mind a dokumentált „+” Strong-lánc okkal (DT147). Más eltérés nincs. |
| **K5 vers-lap** | 1 vCPU / 2 GB korláttal, meleg OS-gyorsítótárral a teljes vers-lap (Olvasópult, a fejezet szövegével és a vers-panellel) **medián 217 ms, p95 310 ms**; a vers-panel töredéke (`/r/vers/…`) 126 / 312 ms. A pilot 93 ms-a a D3 lekérdezés-készlet ideje (nem teljes lap); ugyanez a készlet ezen az adatbázison korlát nélkül 38,8 ms (1Móz 1–25) és 24,9 ms (Zsolt 22). **Hideg** (üres OS-gyorsítótár) a vers-lap **medián 4,8 s, p95 8,9 s**. |
| **K5 magyar szó < 100 ms** | Meleg mediánnal **nem teljesül** a leggyakoribb szavakon: *és* alapmódban 152 ms (p95 162), pontos módban 97 ms (p95 118, a határon); a (c) mód *föld* 158 ms, *ki* 531 ms. A többi magyar szó 8–61 ms. **Hideg** gyorsítótárral minden magyar keresés 100 ms fölött van (219–2 098 ms). → **DT-F76k** (döntés, megállás). |
| **K6 tesztek** | a teljes futás (a lassú `teszt_szintek.py`-jal): 9 fájlból 7 zöld; **2 piros**: `teszt_bdb_vers_jelentes.py` (a main-ről örökölt, ismert hiba, #119), `teszt_olvaso_szerver.py` (a saját `m4_meres.py` első változata sértette a „SQL csak a `lekerdezesek.py`-ban” szabályt; javítva, újrafuttatva: l. 5. szakasz). |

## 1. Gép és környezet

`scope=a mérés gépe | forras=/proc/cpuinfo, /proc/meminfo, platform, systemctl --version, /etc/os-release (m4_meres.py gep_adatai) | ts=2026-10-18T18:31:16Z`

| | |
|---|---|
| gazda | Windows 11 Pro 10.0.26300, AMD Ryzen 3 3100 (4 mag / 8 szál) |
| WSL | `pardes` disztribúció (Ubuntu 24.04.5 LTS), kernel 6.18.54.1-microsoft-standard-WSL2, systemd 255 (255.4-1ubuntu8.18), a disztribúció 8 CPU-t és 7 905 MB RAM-ot lát (`memtotal` 8 095 424 kB) |
| szerver | Python 3.12.3 (a `~/pardes/eszkozok/olvaso_szerver/.venv`), gunicorn 26.2.0, Flask 3.1.3, SQLite 3.45.1; `gunicorn_conf.py`: gthread, 1 worker, 4 szál |
| adatbázis | `/home/basesoft/pardes/pardes.db` (WSL-natív ext4), 969 646 080 bájt, `meta.epites_ts=2026-10-18T12:18:16Z`, `meta.mod=teljes`; nem építettem újra |
| kód | a szerver a munkafából fut (`/mnt/c/…/eszkozok/olvaso_szerver`), a sablonok és a konfig onnan olvasódnak |
| egyidejű terhelés | a felhasználó fejlesztői szervere (8765, `alkalmazas.py --ujratolt`, üresjáratban, ~1% egy magon) futott; a teljes tesztfutás a mérés előtt befejeződött; a mérés alatt más saját folyamat nem futott |

## 2. A korlát (1 vCPU, 2 GB RAM): módja és igazolása

**Mód:** `systemd-run --scope -p AllowedCPUs=0 -p CPUQuota=100% -p MemoryMax=2G -p MemorySwapMax=0`, benne `runuser -u basesoft -- env PARDES_DB=… gunicorn -c gunicorn_conf.py "alkalmazas:letrehoz()"`. A scope rootként indul (`wsl -d pardes -u root`, jelszó nélkül: a disztribúció alapértelmezése, M1 4.3); a szerver `basesoft` felhasználóként fut. Ez a DT146/5 módszere (`AllowedCPUs=0`, `MemoryMax=2G`, ugyanaz, mint a `telepit.sh indit-korlat`), kiegészítve a `CPUQuota=100%`-kal és a `MemorySwapMax=0`-val (a VPS-en nincs csere). A mérő kliens a korláton kívül, az 1. CPU-n fut (`sched_setaffinity({1})`), új HTTP-kapcsolattal kérésenként.

**Igazolás** (`m4_meres.py` `igazolas()` és `korlat_probak()`):

`scope=a pardes-m4-nolru.scope cgroup-fájljai és folyamatai; két próba ugyanilyen tulajdonságú scope-ban | forras=/sys/fs/cgroup/system.slice/pardes-m4-nolru.scope, /proc/<pid>/status | ts=2026-10-18T18:31Z`

| Mit | Érték |
|---|---|
| `cpuset.cpus.effective` | `0` |
| `cpu.max` | `100000 100000` (= 1 CPU) |
| `memory.max` | `2147483648` (2 GiB) |
| `memory.swap.max` | `0` |
| a scope folyamatai (`Cpus_allowed_list`) | `runuser` (uid 0), a gunicorn mester és a worker (uid 1000): mind `0` |
| CPU-próba: 4 párhuzamos, 3 s-ig pörgő folyamat | scope-ban: falióra 3,01 s, a gyerekek CPU-ideje **2,64 s**, `nproc=1`; korlát nélkül (`taskset -c 0-7`): 3,00 s, **10,76 s**, `nproc=8` |
| memória-próba | 2,5 GB foglalás a scope-ban: **SIGKILL** (kilépés −9, OOM); 1,5 GB: lefut |
| a szerver memóriája a mérés végén | a scope `memory.peak` 292 MB (a lap-gyorsítótár része is), `oom_kill 0`; a worker RSS 114 MB |

A korlát tehát hat. **Hiányosság:** a WSL2 virtuális lemeze (vhdx a gazda NTFS-én) nem a VPS lemeze; az I/O-t nem korlátoztam, és a scope `io.stat`-ja üres (a WSL-kernel I/O-elszámolása nem érhető el, `/proc/self/io` sincs), ezért a hideg kérések lemezolvasását rendszerszinten mértem (4. szakasz).

## 3. Módszer

- **Minta** (`--seed 76`): 30 vers (20 az 1Móz 1–25-ből, 10 a Zsolt 22-ből: 1Móz 15:19, 19:17, 17:1, 8:21, 12:6, 2:24, 18:4, 10:9, 11:22, 12:10, 18:24, 20:6, 10:2, 4:6, 14:6, 12:11, 9:27, 14:4, 21:32, 3:6; Zsolt 22:1, 22, 14, 19, 20, 26, 13, 24, 8, 11), 20 héber szó-lap (H0430, H0216 + 18 véletlen, nem nyelvtani Strong a két szakaszból), 20 görög szó-lap (G2316 + 19 véletlen LXX-Strong a két szakaszból), 15 fejezet (1Móz 1, 5, 6, 12, 14, 18, 19, 20, 23; Zsolt 22, Ézs 53, Ján 1, Róm 8, Jel 21, Zsolt 119), 25 keresés a négy ágon (az M3 4. szakaszának esetei).
- **Lapok:** a vers-lap mindhárom nézetben (`?nezet=`); a vers-panel és a szó-lap töredéke (`/r/vers/…`, `/r/szo/…`, 10 héber + 10 görög); a szó-lap Olvasópult-nézetben.
- **Hideg:** minden kérés előtt `sync; echo 3 > /proc/sys/vm/drop_caches` (az OS lap-gyorsítótára üres), a szerver lap-LRU-ja kikapcsolva (a `konfig/` másolata a repón kívül, `max_lap = 0`). **Meleg:** egy be nem számított bemelegítő kérés után laponként 5 kérés, a lap-LRU kikapcsolva (minden kérés valódi lapelőállítás; a válasz `X-Cache: MISS`). **LRU:** az eredeti konfiggal (`max_lap = 512`) a kész lap a gyorsítótárból (`X-Cache: HIT`), 10 vers- és 10 szó-lap × 5.
- **Statisztika:** medián és p95 (legközelebbi rang) a kérésekre; a meleg sorban laponként 5 kérés. Az idő a kliens oldali teljes HTTP-válaszidő (kapcsolat + lapelőállítás + átvitel).
- **Futtatás:** `wsl -d pardes -u root -e ~basesoft/pardes/eszkozok/olvaso_szerver/.venv/bin/python eszkozok/olvaso_szerver/m4_meres.py --kimenet /tmp/pardes_m4`; a nyers eredmény a WSL-ben: `/tmp/pardes_m4/m4_meres.json` (a repón kívül), 18:31:16Z–18:49:11Z.

## 4. Mért idők (1 vCPU, 2 GB RAM)

`scope=m4_meres.py, 30 vers, 20 + 20 szó-lap, 15 fejezet, 25 keresés; hideg: 1 kérés/lap drop_caches után, meleg: 5 kérés/lap, lap-LRU nélkül; LRU: 20 lap × 5 | forras=pardes.db meta.epites_ts=2026-10-18T12:18:16Z (~/pardes/pardes.db, WSL pardes), gunicorn gthread 1×4, systemd-run --scope AllowedCPUs=0 CPUQuota=100% MemoryMax=2G MemorySwapMax=0 | ts=2026-10-18T18:49:11Z`

### 4.1 Lapok

| Lap | n lap | hideg medián (ms) | hideg p95 (ms) | meleg medián (ms) | meleg p95 (ms) | pilot / cél |
|---|---:|---:|---:|---:|---:|---|
| vers-lap, Olvasópult | 30 | 4 778 | 8 939 | **217** | **310** | pilot: 93 ms (D3, csak lekérdezés) |
| — ebből 1Móz 1–25 | 20 | 4 778 | — | 215 | 300 | pilot 1Móz: 93,4 / 161,2 |
| — ebből Zsolt 22 | 10 | 4 681 | — | 225 | 345 | pilot Zsolt: 51,1 / 78,1 |
| vers-lap, Interlineáris | 30 | 4 440 | 8 257 | 204 | 380 | |
| vers-lap, Munkaasztal | 30 | 4 626 | 9 168 | 206 | 397 | |
| vers-panel töredéke (`/r/vers/…`) | 30 | 3 301 | 6 587 | 126 | 312 | |
| héber szó-lap | 20 | 1 076 | 5 272 | **16** | **44** | pilot: 3,9–5,4 ms (D3) |
| görög szó-lap | 20 | 2 517 | 5 220 | **12** | **22** | pilot: 3,4–3,6 ms (D3) |
| szó-lap töredéke (`/r/szo/…`) | 20 | 2 630 | 4 394 | 13 | 45 | |
| fejezet-lap | 15 | 1 485 | 7 391 | 73 | 300 | |
| kész lap a gyorsítótárból (LRU HIT) | 20 | — | — | 1,2 | 2,4 | |

Minden mért válasz 200; minden LRU nélküli kérés `X-Cache: MISS`. A meleg sorban a legrosszabb lapmedián: vers-lap Interlineáris 704 ms (egy hosszú fejezet), Olvasópult 284 ms.

**Összevetés ugyanazzal a lekérdezés-készlettel (a pilot D3-a ezen az adatbázison, korlát nélkül):** `db_meres.py` D3 — vers 38,8 / 70,4 ms (1Móz 1–25, meleg medián / p95), 24,9 / 38,3 ms (Zsolt 22); héber szó 1,5 / 6,3 és 2,4 / 14,9 ms; görög szó 1,3 / 2,3 és 1,5 / 3,2 ms. `scope=db_meres.py --db ~/pardes/pardes.db --json-konyvtar <a pilot 2026-10-18-i JSON-jai> --nincs-hash --nincs-tomorites, taskset -c 2-7 | forras=pardes.db meta.epites_ts=2026-10-18T12:18:16Z | ts=2026-10-18T18:27Z`. A pilot 93 ms-a tehát a régebbi adatbázison és gépállapotban mért szám; a mai készlet korlát nélkül gyorsabb, a teljes szerver-lap 1 vCPU-n ennek kb. 5,6-szorosa (217 ms), mert a vers-lap a teljes fejezetet (minden vers szövegét, szópárjait, csempéit) és a 23 blokkos vers-panelt is előállítja (egy vers-lap ~490 SQL-utasítás: `diag_scan`, l. lent), a HTML-t rendereli, és egy CPU-n fut.

### 4.2 Keresés

| Ág | Keresés | hideg (ms) | meleg medián (ms) | meleg p95 (ms) | K5 (< 100 ms, meleg medián) |
|---|---|---:|---:|---:|---|
| Strong | H0216 | 2 491 | 13,0 | 110,2 | |
| Strong | H0430 (gyakori) | 4 281 | 60,1 | 151,5 | |
| Strong | H9002 (leggyakoribb) | 5 373 | 106,4 | 114,3 | |
| Strong | G3056 (görög) | 1 484 | 9,7 | 10,1 | |
| Strong | H1254 H0430 | 3 684 | 19,3 | 19,6 | |
| magyar szó, pontos | világosság | 2 098 | 8,0 | 8,4 | igen |
| magyar szó, pontos | föld | 1 475 | 22,5 | 27,7 | igen |
| magyar szó, pontos | Isten | 2 090 | 18,6 | 21,0 | igen |
| magyar szó, pontos | **és** | 219 | **97,1** | **117,8** | határon (medián alatta, p95 fölötte) |
| magyar szó, alap (a) | világosság | 1 766 | 15,9 | 20,4 | igen |
| magyar szó, alap (a) | föld | 1 187 | 21,7 | 22,8 | igen |
| magyar szó, alap (a) | amely | 1 008 | 20,8 | 22,0 | igen |
| magyar szó, alap (a) | mond | 419 | 26,0 | 26,8 | igen |
| magyar szó, alap (a) | ő | 669 | 61,1 | 101,0 | igen (p95 a határon) |
| magyar szó, alap (a) | **és** | 393 | **152,2** | **162,1** | **nem** |
| magyar szó, (c) | világosság | 4 381 | 22,9 | 25,0 | igen |
| magyar szó, (c) | **föld** | 6 264 | **158,0** | 176,4 | **nem** |
| magyar szó, (c) | **ki** (funkciószó) | 6 957 | **530,6** | 576,8 | **nem** |
| frázis | a föld | 1 929 | 46,0 | 54,4 | |
| frázis | kietlen és | 597 | 6,7 | 7,5 | |
| frázis | és monda az úr | 1 306 | 35,5 | 36,7 | |
| héber frázis | בראשית ברא | 97 | 4,8 | 5,4 | |
| héber frázis | את השמים | 6 906 | 48,6 | 91,5 | |
| héber frázis | ויאמר אלהים | 4 985 | 28,3 | 28,8 | |
| héber frázis | יהוה (1 szó) | 1 930 | 31,9 | 46,4 | |

Ágonként (meleg medián / p95, ms): Strong 19,6 / 114,3; magyar szó pontos 20,7 / 104,3; alap 24,1 / 159,8; (c) 158,0 / 576,8; frázis 35,5 / 54,4; héber frázis 29,8 / 53,5. Hideg mediánok: 3 684, 1 783, 839, 6 264, 1 306, 3 457 ms. Az M3 korlát nélküli tájékoztató mérésével (M3 4. szakasz) a meleg számok nagyságrendben egyeznek (*és* alap: 169 ms ott, 152 ms itt; *ki* (c): 597 / 531 ms).

### 4.3 A hideg idők oka (diagnózis)

`scope=OldalGyar közvetlen hívása (Flask és HTTP nélkül), CPU 0, drop_caches után és újra; a rendszerszintű /proc/vmstat pgpgin és pgmajfault különbsége | forras=pardes.db meta.epites_ts=2026-10-18T12:18:16Z | ts=2026-10-18T18:55Z` (diagnosztikai szkript a repón kívül)

| Lap | hideg | lemezről beolvasva | meleg |
|---|---:|---:|---:|
| vers-lap 1Móz 15:19 | 4 417 ms | 129,4 MB | 168 ms |
| vers-lap Zsolt 22:13 | 4 742 ms | 120,9 MB | 254 ms |
| szó-lap G3735 | 2 761 ms | 25,1 MB | 68 ms |
| szó-lap H8435 | 1 955 ms | 24,6 MB | 21 ms |

A hideg vers-lap ~120–130 MB-ot olvas szétszórtan a 970 MB-os fájlból (≈ 30 MB/s a WSL2 virtuális lemezén): a fejezet minden versének tokenjei, párjai, csempéi és a nagy táblák indexlapjai. A teljes táblát bejáró (index nélküli) lekérdezések kis táblákon futnak (`forditasok` 737 sor, `morf_nyelv_aramai` 7 549 sor — a fejezet minden versére egyszer —, `tw_szocikkek`, `nave_basokant` fejezet-szintű sorai, `lxx_bridge` görög irányban, a négy adatréteg-tábla); ezek meleg gyorsítótárral olcsók, a hideg időt nem ők okozzák. Egy vers-lap ~494 SQL-utasítás, ebből 150 teljes bejárás (`EXPLAIN QUERY PLAN`, 1Móz 15:19). A 2 GB-os korlát mellett a 970 MB-os adatbázis elfér az OS lap-gyorsítótárában (a mérés alatt a scope `memory.peak`-je 292 MB, OOM nem volt), tehát a hideg idő a szerver (vagy a gép) indulása utáni első kérésekre jellemző. A VPS lemeze (NVMe) más; a hideg szám ott újramérendő (M6).

## 5. Tesztek (K6)

`scope=python eszkozok/teszt_futtat.py (mind a 9 tesztfájl, a lassú teszt_szintek.py-jal), a WSL pardes disztribúcióban, taskset -c 2-7 | forras=unittest, Python 3.12.3, pardes.db meta.epites_ts=2026-10-18T12:18:16Z (~/pardes/pardes.db), a munkafa 7e4b6c5c + az m4_meres.py első változata | ts=2026-10-18T18:06:30Z–18:30:03Z`

| Fájl | Eredmény | Idő |
|---|---|---:|
| `teszt_arculat.py` | zöld, 22 teszt | 8,6 s |
| `teszt_bdb_vers_jelentes.py` | **piros**, 26-ból 1: `Ujrageneralas.test_bajtra_azonos` | 59,7 s |
| `teszt_indito.py` | zöld, 39 | 22,4 s |
| `teszt_kereses.py` | zöld, 36 | 11,1 s |
| `teszt_olvaso_szerver.py` | **piros**, 73-ból 1: `TestSzabalyok.test_sql_csak_a_lekerdezesekben` (`m4_meres.py:107: .execute( a lekerdezesek.py-n kívül`) | 1 152 s |
| `teszt_pilot_aranymintaval.py` | zöld, 22 | 107,2 s |
| `teszt_szintek.py` | zöld, 13 | 144,3 s |
| `teszt_tervezo.py` | zöld, 48 | 17,1 s |

(A `teszt_futtat.py` kilépési kódja 1.) A `teszt_olvaso_szerver.py` ideje a szokásos ~2 perc helyett 19 perc volt, mert a futással párhuzamosan a mérőszkript próbafutása `drop_caches`-szel többször kiürítette az OS-gyorsítótárat.

- **`teszt_bdb_vers_jelentes.py`**: a main-ről merge-elt állapotban **még nem zöld**. Az eltérés a generált `adat/bdb_vers_jelentes.tsv` 2. (fejléc) sora: a generátor (`eszkozok/olvaso_szerver/bdb_vers_jelentes.py:266-270`) helyőrzőket ír (`DT-F99n` …), a tábla a végleges számokat hordozza (`DT179` …). Ez a #119 (`F119_BDB_HEADER_DT_BRIEF.md`, `allapot: nem_indult`) tárgya; a #76 `ir` mezőjében a generátor benne van, de a tábla (`adat/`) nincs, ezért nem javítottam.
- **`teszt_olvaso_szerver.py`**: a saját mérőszkriptem első változata a mintavételt közvetlen SQL-lel végezte. Javítva (minden lekérdezés a `lekerdezesek.py` meglévő függvényein át: `meta`, `fejezet_versek`, `heber_d2`, `lxx_szavak`, `nyelvtani_strongok`), a fájl újrafuttatva: l. 5.1.
- **D2 a tesztben:** `TestD2PilotEgyezes` — „D2: 21991 összevetés, eltérő blokk-csoport: {'gorog_szo:usz_elofordulas': 27}” és „D2: 3022 összevetés, … {'gorog_szo:usz_elofordulas': 11}” (a teszt kimenete), egyezik a 6. szakasz `db_meres.py` futásával.

### 5.1 Újrafuttatás a javított mérőszkripttel

`scope=python eszkozok/teszt_futtat.py --fajl teszt_olvaso_szerver, WSL pardes, taskset -c 2-7 | forras=unittest, Python 3.12.3, pardes.db meta.epites_ts=2026-10-18T12:18:16Z | ts=2026-10-18T18:54:38Z–18:57:20Z`: **zöld, 73 teszt, 172,4 s** (köztük a `test_sql_csak_a_lekerdezesekben` és a D2). A teljes futás többi fájlja a javítás után nem futott újra (a javítás csak az `m4_meres.py`-t érinti, amelyet más teszt nem olvas). **Eredmény a K6-hoz:** 8 fájl zöld, 1 piros (`teszt_bdb_vers_jelentes.py`, #119); a CI és a független ellenőr nem futott.

## 6. D2-egyezés a #60 pilottal (K1)

`scope=db_meres.py D2, 1Móz 1–25 (693 vers, 1 075 héber és 1 230 görög szó-lap) és Zsolt 22 (32 vers, 159 + 305 szó-lap), a pilot JSON-ja az adat.py 2026-10-18-i futásából (a repón kívül) | forras=pardes.db meta.epites_ts=2026-10-18T12:18:16Z meta.mod=teljes; a pilot a konkordancia/ TSV-iből (munkafa 7e4b6c5c) | ts=2026-10-18T18:27Z`

| Szakasz | blokk-csoport | összevetés | eltérő |
|---|---:|---:|---|
| 1Móz 1–25 | 24 | 21 991 | `gorog_szo:usz_elofordulas`: 27 (mind „a pilot TSV-útja a „+” Strong-láncok elemeit nem számolja …; DB-szám = TSV-szám + láncelem”) |
| Zsolt 22 | 24 | 3 022 | `gorog_szo:usz_elofordulas`: 11 (ugyanaz az ok) |

A többi blokk-csoport (vers: Károli-szöveg, Károli–Strong párosítás, héber szavak, TSK darab és top-6, Károli-KH darab, versszámozás, LXX-versszám, LXX-szavak, Macula, Nave, UBS; héber szó: Strong-szótár, BDB angol/magyar/alias, előfordulás, Károli-alakok, lxx_bridge; görög szó: TBESG, Thayer, magyar szócikk, héber háttér) 0 eltérés. **A K1 teljesül** az egyetlen dokumentált kivétellel (DT147). A D2 a darabszámot és a fő adatot veti össze; a vizuális összevetés két olyan eltérést talált, amelyet a D2 nem fog meg (a Károli-KH tartományának vége, a TIPNR ismétlődő sora: `naplok/OLVASOI_KONKORDANCIA_pilot_osszevetes.md` 8. szakasz, N-F76l).

**Frissesség (K4, mellékes lelet):** ugyanez a futás D5-je (hash-újraszámítás nélkül) a `tsk` táblára sorszám-eltérést mér: `meta` 423 955 sor, a munkafa `konkordancia/TSK_kereszthivatkozasok.tsv`-je 432 949. A két pilot-szakasz TSK-adata ettől egyezik; a `pardes.db` újraépítése az M5 előtt kell (N-F76m; nem a #76 `ir` mezője).

## 7. Vizuális összevetés

A blokkonkénti vizuális összevetés a `naplok/OLVASOI_KONKORDANCIA_pilot_osszevetes.md` 8. szakaszában (1Móz 1:1 és Zsolt 22:2 vers-panel, H0430 szó-lap vers-kontextusban, G2316, keresőlap; mindhárom nézet). Két új, mechanikus eltérés (N-F76l); a többi ismert.

## 8. Nyitott (döntés, megállás)

- **DT-F76k** (`DONTESEK.md`): a K5 nem teljesül (a magyar szóra keresés a leggyakoribb szavakon és a (c) módban 100 ms fölött, hideg gyorsítótárral minden lap és keresés másodperces), és a vers-lap 1 vCPU-n a pilot 93 ms-ának kb. 2,3-szorosa. Opciók és javaslat ott.
- **N-F76l**, **N-F76m** (`NYITOTT_FELADATOK.md`).
- A hideg idő a WSL2 virtuális lemezén mért; a VPS-en (M6) újramérendő.

## 9. Mi maradt ellenőrizetlen

- A mérés I/O-korlát nélkül futott (a WSL-kernelben nincs I/O-elszámolás); a hideg lemezolvasás rendszerszintű (`/proc/vmstat`) szám.
- A párhuzamos terhelés (több egyidejű kérés 1 vCPU-n) nem mért; a 2 workeres gunicorn összevetése (M0 5. szakasz) sem.
- A hash-szintű frissesség (D5 hash-újraszámítással) nem futott.
- A független ellenőr nem nézte.
