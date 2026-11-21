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

**4. Átírás: NEM készült.** ⛔ megállás: a brief 3. lépés szerint a mért eloszlás (12 dataset nem mind a négy típusban) nem fejezhető ki a DT248 (a) alakjával (ez a brief 3. pontjának ⛔ feltétele). A SEMA `adat/SEMA.md` nem változott.

Tétel: `dontesek/uj/claude_f69-sema-dataset-szam.md`, `DT-F69a` (nyitott). Javaslat: „43 dataset, 136 sor: 31 × 4 + 12 × 1 (a 12 lexikon_oldal-only dataset a táblából olvasandó)”.

E2 („21 érték” → a mért darabszám, 43) és E3 (4 `openbible_crossrefs`-sor) a döntéstől függetlenül ugyanígy javítandó; E1 az alak döntésétől függ.

## Független ellenőrzés

Nem futott (a menet megállt, nincs átírt diff).

## Zárás

- Készült: brief fejléc (`F69.1`), mérés (szkript a scratchpadban, nem repó), döntés-tétel `DT-F69a`, ez a jelentés.
- Nem készült: SEMA 2.6 átírás (E1–E3), draft PR (a brief szerint a végén).
- Mérési eltérés: a datasetek száma 30 → 43 és a sorok 117 → 136 a 2026-10-19 óta; a briefbeli számok elavultak, a mért szám az irányadó (brief 3. pont).
- Tesztek: nem futottak (nincs kódváltozás).
- `ellenoriz`: nem futott (a 5. lépés csak az átírás után esedékes).
- Nyitott pontok: DT-F69a felhasználói döntése; a CLAUDE.md „17 dataset” mondata (a brief nem érinti; jelzés).

## Folytatási pont

A brief fejléce `allapot: megallt`. A folytatás: a felhasználó DT-F69a-ra választ (1., 2. vagy 3. opció), utána a 4. lépés (E1–E3 átírás a mért számokkal), majd az 5. lépés (`git diff --stat`, `python eszkozok/feladatok.py ellenoriz`, zárás, draft PR). A mérési szám újramérendő, ha a main közben változik.
