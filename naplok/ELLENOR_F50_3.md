ELTÉRÉS: 1 tétel

*(A `fuggetlen-ellenor` subagent jelentése, claude-opus-5-5; fájlíró eszköze nem volt, az orkesztrátor mentette, a táblázat azonos tartalmú OK-soraival összevonva; az ELTÉRÉS-tétel és a megjegyzések szó szerint.)*

# ELLENOR_F50_3: F50_CI_JAVITO_KOR_BRIEF.md · `b8dacb58..ef5ccb57` (F50.8, F50.9; a 2. javítókör utáni újraellenőrzés, a teljes feladat `1a6a6eef..HEAD` szempontjából is)

| pont | eredmény | indok |
|---|---|---|
| ELLENOR_F50_2 1. (b): futtat.py naplózva | OK | napló `:57`: parancs, proveniencia, exit-kód, szabályonkénti számok; `--minta 1000`-rel megismételve: EXIT=0, E25: 4, E27: 42, a többi 0 |
| fájlonkénti bontás, „mind a hat fájl változatlan”, diff-alap | OK | a napló bontása egyezik; a 6 találati fájl nincs a 7 változott között; merge-base `1a6a6eef` |
| **A találatok jellege** | **ELTÉRÉS** | napló `:57`: „E25: D34 átmeneti jelölés; E27: nem létező távoli ágra mutató hivatkozások” csak részben igaz: az E25 `F10_LEXIKON_LEZARAS_BRIEF.md:138` találat `DONTESEK.md#DT74`, nem D34; az E27 42 találatából csak 3 nem létező ágra mutat (`FELADATOK.md:20, 76, 81`), 8 nem létező commitra, 1 `olvas`-mezőre (`F46…:14`), 30 nem létező fájlra/könyvtárra. A számok és a következtetés (a 7 változott fájlban 0 találat) helyesek. |
| ELLENOR_F50_2 1. (a): feladatok.py a headre | NEM ELLENŐRIZHETŐ | a napló a futtatás commitját megnevezi (`b8dacb58`); F50.8/F50.9 óta a brief fejléce módosult, a mostani HEAD-re a „0 hiba” nincs igazolva (az ellenőr nem futtathatja) |
| ELLENOR_F50_2 1. (c) | OK | a parancsfájlokban egy-egy hunk, F50.8/F50.9 nem nyúlt hozzájuk |
| Brief fejléce, D1–D5, 5. elfogadási feltételek, ⛔, A1–A6, E26, listák 1–5 | OK | `allapot: megallt`, `[elteres_kor 2/2]`; nulla-diff az `adat/`, `konkordancia/`, `.github/`, `eszkozok/`, `FELADATOK.md` alatt |

**ELTÉRÉS-ek súlyossági sorrendben:**
1. (alacsony, csak szöveg) `naplok/CI_JAVITO_KOR_naplo.md:57`: a találatok jellegének leírása pontatlan (l. fent).

Az ELLENOR_F50_2 1. tételét az F50.8 tartalmilag megoldja. Mivel a körszámláló elérte a 2/2-t, az ELTÉRÉS kezeléséről a felhasználó dönt.
