# F69 jelentés — SEMA 2.6 elavult darabszámai

Modell: claude-haiku-5-5 (brief: haiku). Ág: `claude/f69-sema-dataset-szam` (origin/main `f5d4d874`).

## Menet

**0. Modell-ellenőrzés:** egyezik (haiku).

**1. Döntés:** DT248 🟢 (felhasználó, 2026-10-19; (a) 1., (b) 1.). Rendben.

**2. Ág és fejléc:** a brief fejléce `allapot: fut`, `ag: claude/f69-sema-dataset-szam`. Commit `F69.1` (a commit üzenete tartalmazza a Co-Authored-By sort).

**3. Újramérés:** `split('\t')`, a `#` sorok és a fejléc nélkül. Szkript a scratchpadban: `C:\Users\bases\AppData\Local\Temp\claude\990fa511d9c87807\d2a9621a-bbe6-4bb8-bc4c-b1bab5fdf0e6\scratchpad\meres_f69.py`.
Proveniencia: `scope=adat/datasetek.tsv teljes | forras=adat/datasetek.tsv@f5d4d874 (sha256 2bbe87ad8630) | ts=2026-11-21`.

| | Brief (2026-10-19, `1a6a6eef`) | Mért (2026-11-21, `f5d4d874`) |
|---|---|---|
| megjegyzéssor / fejléc | 3 / 1 | 3 / 1 |
| adatsor | 117 | **136** |
| különböző `dataset` | 30 | **43** |
| `bovitett` / `tematikus` / `melyelemzes` | 29 / 29 / 29 | **31 / 31 / 31** |
| `lexikon_oldal` | 30 | **43** |
| nem mind a négy típusban | 1 (`OSHL_lexikalis_index`) | **12** |
| `allapot` | elerheto 77 · korlatos 32 · hianyzik 4 · generalt_nezet 4 | elerheto 86 · korlatos 42 · hianyzik 4 · generalt_nezet 4 |
| duplikált kulcs | 0 | 0 |

A 12 csak `lexikon_oldal`-ban álló dataset: `OSHL_lexikalis_index`, `Targum_PD`, `Vulgata_Clementina`, `Glossa_Ordinaria`, `Chain_Lineage_Browser`, `SBLGNT_apparatus`, `TAGNT_valtozatok`, `BDB_rokon_irasok`, `Karoli_KH_MEK`, `Karoli_KH_javitott`, `Tanu_atyak_index`, `Tanu_rabbinikus_index`.

Hianyzik-sorok (változatlanul 4): `openbible_crossrefs` × 4 study-típus.

**4. Átírás (a DT-F69a 1. alakja szerint, felhasználói döntés 2026-11-21, 🟢):** `adat/SEMA.md` 2.6 három sora változott, más sor nem:
- E1 (409. sor): „43 dataset, 136 sor: 31 × 4 + 12 × 1 (a 12 lexikon_oldal-only dataset a táblából olvasandó)”
- E2 (414. sor): „(43 érték)”
- E3 (423. sor): „jelenleg 4 sor viseli: az `openbible_crossrefs` mind a négy study-típusban (jelölt, nem importált, DT33)”

Tétel: `dontesek/uj/claude_f69-sema-dataset-szam.md`, `DT-F69a` 🟢.

## Független ellenőrzés

Nem futott (a menet megállt, nincs átírt diff).

## Zárás

- Készült: brief fejléc (`F69.1`), mérés (szkript a scratchpadban, nem repó), döntés-tétel `DT-F69a` (🟢), a SEMA 2.6 E1–E3 átírása, ez a jelentés.
- Mérési eltérés: a datasetek száma 30 → 43 és a sorok 117 → 136 a 2026-10-19 óta; az átírás a mért, 2026-11-21-i számokat írja be.
- Ellenőrzés: `git diff --stat adat/SEMA.md`: 1 fájl, csak a 2.6 E1–E3 sorai változtak. A `git diff --stat -- adat/datasetek.tsv` kimenete üres. `python eszkozok/feladatok.py ellenoriz`: 245 brief, 0 hiba (a figyelmeztetések más briefekre vonatkoznak).
- Tesztek: nem futottak (nincs kódváltozás).
- Megjegyzés (nem javítva, a brief hatókörén kívül): a CLAUDE.md „Adat-tár” „17 dataset” mondata elavulhat; a mondat a `konkordancia/` fájlkészletéről szól, nem a `datasetek.tsv` mátrixáról. Elavultsága nincs külön megvizsgálva.
- Nyitott pontok: nincs a F69-ben; a `datasetek.tsv` következő bővítésénél a SEMA 2.6 számai ismét elavulnak (gépi őrzés nem e feladat).
- PR: draft, a main-be (l. a brief fejlécét és a végi commitot).
