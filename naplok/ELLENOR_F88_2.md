# Független újraellenőrzés: F88, 2. kör

*Proveniencia: `scope=F88.6 (cbf41912..7b0ec278) + 693c38d5, 5690e2f9 | forras=fuggetlen-ellenor (claude-opus-5-5) diff-ellenőrzés; a mérés a hívó session-ből (claude-opus-5-5): eszkozok/sqlite_epit.py --mod teljes --kimenet <repón kívül>, saját sqlite3-lekérdezés, python -m unittest eszkozok/teszt_sqlite_epit.py | ts=2026-10-13`*

Ítélet: **ELTÉRÉS: 3 tétel** (dokumentációs); a mért számok mind egyeznek.

## Független mérés (a kész pardes.db-n)

| mutató | állítás (`naplok/F88_meres.md`) | mért | |
|---|---:|---:|---|
| `tipnr` sorok | 35 522 | 35 522 | OK |
| `strong IS NULL` | 0 | 0 | OK |
| utótagos sor | 16 928 | 16 928 | OK |
| utótag nélküli, `strong` = `strong_nyers` | 18 594 | 18 594 | OK |
| `token_strong`-ban | 35 433 | 35 433 | OK |
| nem illeszkedő, utótagos | 1 (G6202) | 1 (`G6202`, `G6202G`, Millo) | OK |
| nem illeszkedő, utótag nélküli | 88 sor, 62 alapszám | 88 sor, 62 alapszám | OK |
| `tipnr` hash | `d4a93c34d0e36db8` | `d4a93c34d0e36db8…` | OK |
| tesztek | 43 zöld | `Ran 43 tests` — OK | OK |

A worktree a futások után tiszta (`git status --short` üres).

## Eltérések

1. `naplok/F88_meres.md:3` — a proveniencia `(--mod teljes)`, de a napló `--ketszer`/`--meret`-eredményt (két építés hash-egyezése, MB) állít; a mérés a megadott parancsból nem reprodukálható.
2. `F88_TIPNR_NORMALIZALAS_BRIEF.md:16,51` — az `ir` mezőből hiányzik a `naplok/F88_meres.md`, `naplok/F88_zaras.md`, `naplok/ELLENOR_F88.md`; a Hatókör szerint a mérés még a `SQLITE_EPIT_meres.md`-ben van. A `naplok/F88_zaras.md:9` „Egyeztetett eltérés: nincs”.
3. `naplok/SQLITE_EPIT_meres.md:175` — a generált fájlba kézzel írt mutatósort a következő `--naplo` futás törli (alacsony).

Megjegyzés: `naplok/F88_zaras.md:7` („A javítás utáni újraellenőrzés nem futott”) e kör után elavult. A `futtat.py` csak az F88.6-tartományon E5-öt jelez (törölt címsor), a teljes PR-tartományon nem — a CI zöld.
