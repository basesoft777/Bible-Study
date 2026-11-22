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

### 5. A két piros teszt (a 2.4 pont tárgya, még nem vizsgáltam)

`teszt_visszhang_kapu.py` két tesztje és `teszt_szintek.py` `test_ebben_a_versben_es_az_interlinearis_csempek_koveti_a_blokkok_lathatosagat` tesztje. Oka és javítása a ⛔ utáni 2. lépés.

## Állapot

⛔ DT-F232a megállás. A döntésig semmi nem készült a kódban; a döntés `dontesek/uj/f232-merce-192772.md`-ben áll (helyőrző).
