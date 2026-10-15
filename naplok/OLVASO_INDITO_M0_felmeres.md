# #100 OLVASO_INDITO — M0 felmérés

*Ág: `claude/olvaso-indito` · végrehajtó: `claude-sonnet-5-5` · mérés napja: 2026-10-15 (helyi idő, +02:00) · a mérések a `pardes` WSL-disztribúcióban és a Windows-gépen futottak, a mérőszkriptek a session scratch-könyvtárában vannak (nem a repóban). Minden szám mellett a mérés időpontja; ahol nem mérhető, jelölve.*

## 1. A három asztali parancsikon (csak olvasva)

Proveniencia: `cat` a három fájlra, 2026-10-15 ~09:38.

| Fájl | Port | Kiadás |
|---|---|---|
| `PaRDeS olvaso - belso (tervezo).bat` | 8765 | `belso` |
| `PaRDeS olvaso - nyilvanos.bat` | 8766 | `nyilvanos` |
| `PaRDeS olvaso - kereskedelmi.bat` | 8768 | `kereskedelmi` |

Mindhárom azonos szerkezetű: `start` + `wsl -d pardes -- bash -lc "fuser -k -TERM <port>/tcp; sleep 1; cd /mnt/c/Users/bases/Desktop/Bible-Study/eszkozok/olvaso_szerver && PARDES_DB=$HOME/pardes/pardes.db exec $HOME/pardes/eszkozok/olvaso_szerver/.venv/bin/python alkalmazas.py --port <port> --kiadas <kiadás>"`, majd `timeout /t 7`, majd a böngésző megnyitása (`/1Moz/1/1?ful=vers`). Megfigyelések:

- A kód a **főcheckoutból** (`C:\Users\bases\Desktop\Bible-Study`, az ott éppen kiválasztott ágról) fut; a mérés pillanatában ez az ág `claude/tervezo-mod` (HEAD `3b52c6a4`), nem a `main`. Ez a brief 1.3 pontjának élő példája.
- A `venv` a WSL `~/pardes` klónjában van, a kód a `/mnt/c`-n.
- Az adatbázis a `$HOME/pardes/pardes.db` (WSL-példány).
- A böngésző 7 másodperc fix várakozás után nyílik, nem a szerver készenlétére.

## 2. A WSL `~/pardes` állapota

Proveniencia: `wsl -d pardes -- bash -l m0a.sh`, 2026-10-15T09:39:59+02:00.

| Elem | Mért állapot |
|---|---|
| disztribúciók | `Ubuntu` (alapértelmezett) és `pardes`, mindkettő WSL2, Running (`wsl -l -v`, 09:38) |
| `~/pardes` | **git-klón** (`git rev-parse --is-inside-work-tree` = true), HEAD `f6f6f50 F76.7: …` (a Windows-checkouthoz képest régi; ritka klón) |
| venv | `eszkozok/olvaso_szerver/.venv/bin/python` megvan, Python 3.12.3 |
| `python3` / `uv` / `fuser` | `/usr/bin/python3` 3.12.3; `~/.local/bin/uv`; `/usr/bin/fuser` — mind megvan |
| `pardes.db` | 938 303 488 bájt (895 MB), módosítva 2026-10-14 12:00:24 +0200 |
| `konkordancia/` | **nincs** (`ls: cannot access 'konkordancia'`) |
| erőforrás | 8 mag (`nproc`), 7905 MB RAM, 7298 MB szabad |
| futó példány | egy: PID 4690, `alkalmazas.py --port 8765 --kiadas belso`, 08:30 óta (**nem bántva**) |

A Windows-oldali `konkordancia/` mérete: **3,1 GB**, 118 bejegyzés (`du -sh`, 09:41). A CLAUDE.md „389 MB, 17 dataset” sora ehhez képest elavult; ez a (b) opció másolati költségét érinti.

## 3. `meta.epites_ts` és a `meta` olvasási ideje

Proveniencia: `python3 meta.py <db>` (sqlite3, `mode=ro`, `SELECT … FROM meta WHERE kulcs='epites_ts'`), WSL-ből, 2026-10-15T09:40:09+02:00, két kör.

| Példány | `epites_ts` | meta sorok | olvasási idő (1. / 2. kör) |
|---|---|---|---|
| Windows-oldali `Bible-Study/pardes.db` (`/mnt/c`-ről) | `2026-10-14T09:35:00Z` | 107 | 0,018 s / 0,012 s |
| WSL `~/pardes/pardes.db` | `2026-10-14T09:35:00Z` | 107 | 0,001 s / 0,002 s |

- A két példány **ma azonos építésű** (azonos `epites_ts`, azonos méret: 938 303 488 bájt); a fájl-mtime eltér (Windows 11:35:36, WSL 12:00:24: a másolás ideje), ezért az mtime nem használható szinkron-kulcsnak, az `epites_ts` igen.
- A `meta` olvasása a `/mnt/c`-ről is ~0,01–0,02 s: az `indit.sh` szinkron-döntése olcsó (a 938 MB-ot nem kell beolvasni).
- Nyers átvitel (`dd bs=1M count=300`, 09:41:44): `/mnt/c`-ről 3,05 s (103 MB/s), WSL-lemezről 3,04 s (104 MB/s). A teljes másolás becsült ideje ~9–10 s (938 MB / ~100 MB/s; **becslés, a másolás nem futott**). A brief 45 perces teszt-lassulása tehát a véletlen (SQLite-lapos) hozzáférés 9p-költsége, nem a szekvenciális olvasásé.

## 4. A Werkzeug `stat`-újratöltő a `/mnt/c`-n

Proveniencia: `reload_szamol.py` (az `alkalmazas.letrehoz(…)` után a `werkzeug._reloader._find_stat_paths` hívása) és `reload_fut.py` (`app.run(port=18799, use_reloader=True, reloader_type='stat')`), a worktree-ből (`/mnt/c/Users/bases/Desktop/wt-olvaso-indito/…`), `PARDES_DB=$HOME/pardes/pardes.db`, 2026-10-15T09:40:29 és 09:41:15. Werkzeug 3.1.9. A próbaszerver a 18799-es porton futott, a mérés végén leállítva (`pkill`, ellenőrizve); az éles 8765-ös példány (PID 4690) érintetlen.

- **Figyelt fájlok alapból: 126** (22 a `/mnt/c`-n: a szerver betöltött modulfájljai; 104 a venv-ben). Egy teljes stat-kör 126 `stat`-tal: **0,015 s** (~0,12 ms/stat), a bejárás 0,029 s. Az újratöltő 1 s-os lekérdezési ciklusában ez elhanyagolható.
- **Üresjárati CPU:** a gyerekfolyamat (PID 5204) 39 → 62 óraütem 30 másodperc alatt (`/proc/<pid>/stat` utime+stime, CLK_TCK=100) = **0,23 CPU-s / 30 s ≈ 0,8% egy magon**; a szülő (reloader-felügyelő) 32 → 32 (0%). Kérés nélkül.
- A próbaszerver az újratöltővel elindult, a `/statusz` 200-at adott.
- **Fontos eltérés a briefhez:** az alap `stat`-újratöltő **csak a betöltött Python-modulokat figyeli**, a sablonokat (`sablonok/`, 8 fájl), a `konfig/` fájljait (6) és a statikus fájlokat nem. Ezeket az `extra_files` paraméterrel kell hozzáadni (a Werkzeug könyvtárakat is bejár). A brief ezt már így írja (`konfig/`, `sablonok/`), de az `alkalmazas.py` mai `main()`-je nem használ `use_reloader`-t, és a hívás a `Flask.run`-on át a `reloader_type='stat'`-ot csak `run_simple` kwargs-ként adja át.
- Nem mértem: az újraindulás tényleges késleltetését kódváltozás után (az M2 gépi próbája), és a tesztszuite futásidejét (nem volt a M0 tárgya).

## 5. Windows-oldali tesztkörnyezet (a DT-F100a (a) opcióhoz)

Proveniencia: `python --version`, `py -0p`, `python -c "import flask"`, `which uv`, 2026-10-15 ~09:42.

- Windowson csak **Python 3.14.7** van (`C:\Python314`); Flask nincs benne; `uv` Windowson nincs (WSL-ben van).
- Az (a) opció tehát: Windows-os `uv` telepítése + 3.12 + venv + függőségek. Az `uv.lock` 3.12-re készült; a 3.14 nem azonos az aranyminta (szótövező) 3.12-es bájtazonosságával (a #76 zárónapló szerint a 3.12 az aranyminta alapján véglegesedett). **Telepítés nem történt**, jóváhagyás nélkül nem is lesz.

## 6. Ütemezett feladat (a DT-F100b-hez)

Proveniencia: `powershell Get-ScheduledTask | Where TaskName -like '*pardes*'`, 09:42: **nincs ilyen ütemezett feladat** (üres kimenet). Az automatikus indítás ma sehol sincs beállítva.

## 7. Következtetések a két döntéshez

- **DT-F100a:** a WSL-nek már megvan a 3.12-es venv-je és a natív `pardes.db`; a hiányzó rész a `konkordancia/` (3,1 GB). A (b) opció másolat-karbantartást (3,1 GB, szinkron) hozna, a (c) a `konkordancia/`-t olvasó tesztek lassúságát; a nyers szekvenciális átvitel azonban 103 MB/s, tehát a `konkordancia/`-t olvasó tesztek lassúsága nem a sávszélességből, hanem a sok kis fájl / véletlen hozzáférés költségéből jön — ez **nincs külön mérve** (az M1-ben a `TestD2PilotEgyezes` tényleges idejét kell lemérni).
- **DT-F100b:** nincs ütemezett feladat; a WSL-példány most is fut (08:30 óta) — a bejelentkezéskori indítás a Windows Feladatütemező tartós beállítása, felhasználói jóváhagyással.
