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

## 6. Hátravan (jóváhagyás után)

Másolás a `~/pardes/pardes.db` helyére + sha256-egyezés + másolat-épségi teszt; `teszt_sqlite_epit.py` 3.12-n (F79/F92/F95); takarítás; az F76 E1 és E3 lezárásának kimondása; `feladatok.py ellenoriz`.
