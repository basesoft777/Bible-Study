# OLVASO_INDITO — zárójelentés (#100)

*2026-10-15 · végrehajtó: claude-sonnet-5-5 · ág: `claude/olvaso-indito`*

- **Kész:** M0 (felmérés, `OLVASO_INDITO_M0_felmeres.md`), M1 (`indit.sh`, `allapot.py`, `--ujratolt`, élő lábléc, `teszt_indito.py` 39 teszt, `teszt_futtat.py`, CLAUDE.md-sor, README), M2.1 gépi próba (36 ellenőrzés, 0 hiba, `OLVASO_INDITO_M2_gepi_proba.md`).
- **Döntések:** DT-F100a (c); DT-F100b igen, csak a belső 8765, az ütemezett feladat az M2 után, a felhasználó külön jóváhagyásával.
- **Mérés** (`OLVASO_INDITO_M1_merés.md`): a hat tesztfájl együtt 274,6 mp (5 percen belül); `teszt_olvaso_szerver.py` 122,4 mp, `teszt_szintek.py` 77,5 mp egyedül futtatva.
- **Ellenőr:** `ELLENOR_F100.md`, 5 eltérés (E1–E5), mind javítva.
- **Egyeztetett eltérések a briefhez:** élő lábléc (`LablecFigyelo`); `.gitattributes` `*.sh eol=lf`; a `.bat` fájlokban a `timeout /t 7` helyett `/statusz`-ra váró hurok; tartalék ág a `.bat`-okban (törölhető a merge után).
- **Ismert korlát:** szintaxishibás szerverfájl mentése után a szerver leáll, és a javítás nem indítja újra; a parancsikon újraindítja (felügyelő a hatókörön kívül).

## M2.2 és DT-F100b (2026-10-15, lezárva)

- **M2.2 ⛔: SIKERES** (a felhasználó jelentése, 11:06): a belső parancsikon az `indit.sh`-val indult (a régi példány leállt, DB-másolás nem kellett, `--ujratolt`), a lap magától megnyílt, a lábléc `main`-t mutat, figyelmeztetés nélkül.
- **Két hiba a `.bat` fájlokban** (a repón kívül, mindháromban javítva): (1) `wsl -d pardes -- bash -lc "…$S…"`: a `--` miatt a WSL alapértelmezett shellje a `$S`-t üresre fejtette ki, az `indit.sh` el sem indult → `wsl -d pardes -e bash -lc`; (2) a várakozó ciklus `-TimeoutSec 2`, a hideg első `/statusz` 2,1 mp → `-TimeoutSec 15`, 60 próbálkozás, „ne zárd be az ablakot” üzenet. A README a `-e` formát rögzíti.
- **DT-F100b (a felhasználó jóváhagyásával):** ütemezett feladat `PaRDeS olvaso belso 8765` (Windows Feladatütemező, bejelentkezéskor, rejtett PowerShell → `wsl -d pardes -e bash -lc` → `indit.sh belso 8765`, csak ha az `indit.sh` megvan). Egyszeri indítással igazolva: `/statusz` 200. Visszavonás: a feladat törlése (`Unregister-ScheduledTask -TaskName "PaRDeS olvaso belso 8765"`). A nyilvános (8766) és a kereskedelmi (8768) példányra nincs ütemezés.
- **Még nyitott:** a `.bat` fájlok tartalék ága (régi indítás) törölhető, mert az `indit.sh` a `main`-en van.
