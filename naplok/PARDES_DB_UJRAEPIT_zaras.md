# PARDES_DB_UJRAEPIT — zárónapló (#97) — VÁZLAT, a ⛔ megállásig

*Állapot: a 3. lépés 1–4. pontja kész; az 5. pontnál (⛔) megállt. A disztribúcióba másolás, a 3.12-es építő-tesztek, a takarítás és az E1/E3 lezárásának kimondása még hátravan; ezeket a jóváhagyás után egészíti ki a folytatás.*

Modell: `claude-sonnet-5-5`. Python (Windows, építés és mérés): 3.14.7.

## 1. M0 — a 3.12-es tesztfuttatás helye

Választás (javaslat, jóváhagyásra): **(a)** — a `pardes` disztribúció (Python 3.12.3) a Windows-oldali repót a `/mnt/c/Users/bases/Desktop/Bible-Study` úton csak olvassa; `PYTHONDONTWRITEBYTECODE=1` mellett fut, így a repóba nem ír. Indok: a ritka klón (`~/pardes`) nem tartalmazza a `konkordancia/` könyvtárat (389 MB), az (b) út a klón bővítését és ~0,4 GB lemezt jelentene a disztribúció `ext4.vhdx`-ében, és a teszt a tiszta `main` + ág tartalmát kell lássa; a `teszt_sqlite_epit.py` a repó `adat/` táblait ideiglenes könyvtárba másolja (`tempfile.mkdtemp`, a disztribúció `/tmp`-jében), a repóba nem ír. A `/mnt/c` (9p) lassabb; elfogadható, mert a teszt nem teljesítménytest.

## 2. Újraépítés

`python eszkozok/sqlite_epit.py --mod teljes --naplo` (kódváltoztatás nélkül), kilépési kód 0: `kész: pardes.db (894.8 MB, 81.9 s, 73 tábla)`.

| mért | érték |
|---|---|
| fájlméret | 938 303 488 bájt (a régi: 938 287 104) |
| táblaszám (`meta` hash-sor) | 73 |
| `meta.epites_ts` | 2026-10-14T09:35:00Z |
| sha256 | 500183a1cd515953c88034097edbd854150723b59ce9e4cd86a9d3393fdf708b |
| építési idő | 81,9 s |

Proveniencia: `scope=pardes.db teljes újraépítés a main 9e18cbde (F97 ág) TSV-iből | forras=eszkozok/sqlite_epit.py --mod teljes --naplo, kilépési kód 0 | ts=2026-10-14`

A `--naplo` frissítette: `naplok/SQLITE_EPIT_integritas.md`, `naplok/SQLITE_EPIT_meres.md` (a `SQLITE_EPIT_proba_teljes.md` csak `--proba` esetén készül, nem változott).

## 3. D5 — TSV-frissesség (az építés gépén)

`python eszkozok/olvaso_pilot/db_meres.py --db pardes.db --nincs-tomorites` (hash-újraszámítással): **eltérő táblák: nincs (0)**; `hash_ellenorzes_futott: true`; 47 vizsgált tábla, mindegyiknél a meta-hash egyezik a tartalommal; a három korábban eltérő tábla (`vers_szamozas`, `lxx_versszam`, `nave_vers`) már nem tér el. A futás ideje 5 perc 32 s.

Proveniencia: `scope=pardes.db (új, epites_ts=2026-10-14T09:35:00Z), hash-újraszámítás, a forrás-TSV-k git-állapota | forras=eszkozok/olvaso_pilot/db_meres.py D5 | ts=2026-10-14`

## 4. Manifest és másolat-épség (Windows-oldali példány)

`frissesseg.py --db pardes.db --manifest-keszit eszkozok/olvaso_szerver/manifest_pardes_db.tsv` → 73 tábla. Utóellenőrzés a manifesttel: 73 tábla újraszámolt hash-e = `meta` = manifest, **ÉP**. Ez másolat-épség, **nem** TSV-frissesség; a frissesség bizonyítéka a 3. szakasz D5-je.

Proveniencia: `scope=pardes.db + manifest_pardes_db.tsv (73 tábla) | forras=eszkozok/olvaso_szerver/frissesseg.py | ts=2026-10-14`

## 5. A törlendő könyvtárak (⛔ előtti állapot)

A brief 3. lépés 8. pontja a `pardes` disztribúció `~/probe/` és `~/szoto_arany/` könyvtárát nevezi (M0 4.3: „a `~/probe/app.py` és a `~/szoto_arany/` a disztribúcióban maradt”). Mérés (`wsl -d pardes`, felhasználó `basesoft`, home `/home/basesoft`, és root): egyik sem létezik (`ls`: „No such file or directory”; `find / -xdev -maxdepth 4 -name probe -o -name szoto_arany`: nincs találat); az `Ubuntu` disztribúcióban sincs. A törlés tehát tárgytalan, ha nem más helyen állnak; ezt a felhasználónak kell megerősítenie.

## 6. Építő-tesztek Python 3.12-n

Futtatás: `wsl -d pardes`, Python **3.12.3**, a repó `/mnt/c/Users/bases/Desktop/Bible-Study` úton csak olvasva (M0 (a) út), `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp` (a tesztek ideiglenes kimenete a disztribúció `/tmp`-jébe ment). `python3 eszkozok/teszt_sqlite_epit.py` (F79, F92, F95 tesztjei): **Ran 64 tests in 200,874 s — OK**. Futás után a repó munkafája tiszta (`git status` üres). Minden teszt futtatható volt, nem futtatott teszt nincs. (A kimenet „INTEGRITÁS-SÉRTÉS” sorai a negatív tesztek szándékos kimenetei.)

Proveniencia: `scope=eszkozok/teszt_sqlite_epit.py, 64 teszt | forras=unittest, Python 3.12.3, pardes disztribúció | ts=2026-10-14`

## 7. Takarítás

`~/probe/` és `~/szoto_arany/`: **tárgytalan — nem létezik a pardes disztribúcióban.** A keresés módja: `ls` a `/home/basesoft`, `/root`, `/tmp/probe` alatt (basesoft és root felhasználóként), és `find / -xdev -maxdepth 4 -name probe -o -name szoto_arany`: nincs találat. Az Ubuntu disztribúcióhoz nem nyúltam.

## 8. A disztribúció példányának cseréje — NEM FUTOTT LE

A régi `~/pardes/pardes.db` átnevezése `.regi`-re, az új másolása, sha256-egyezés és a másolat-épségi teszt a disztribúcióban **nem történt meg**: a Claude Code engedély-osztályozó a disztribúció módosítását megtagadta (a jóváhagyás az orkesztrátor üzenetében érkezett, nem a felhasználótól közvetlenül). Folytatás: a felhasználó engedélyével, vagy a felhasználó futtatja. A terv: `mv pardes.db pardes.db.regi` (a `.regi` törlése külön jóváhagyás nélkül tilos), `cp` az új db-t és a manifestet, `sha256sum` = 500183a1…708b, `python3 eszkozok/olvaso_szerver/frissesseg.py --db pardes.db --manifest eszkozok/olvaso_szerver/manifest_pardes_db.tsv`.

## 9. Az F76 E1 és E3 lezárása

**Nem mondható ki**, amíg a 8. szakasz le nem fut: az E1 (D5/TSV-frissesség) a build-gépi igazolással (3. szakasz) teljesült, de a disztribúció példánya még a régi; az E3 (3.12-es építő-tesztek) a 6. szakasz szerint teljesült. A teljes lezárás a csere után.
