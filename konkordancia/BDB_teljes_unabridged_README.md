# BDB teljes (unabridged) — `BDB_teljes_unabridged.tsv`

## Forrás

- **Repó:** [eliranwong/unabridged-BDB-Hebrew-lexicon](https://github.com/eliranwong/unabridged-BDB-Hebrew-lexicon) (GitHub, publikus)
- **Felhasznált fájl:** `DictBDB.json`
- **Letöltés URL:** `https://raw.githubusercontent.com/eliranwong/unabridged-BDB-Hebrew-lexicon/master/DictBDB.json`
- **Letöltés dátuma:** 2026-09-02
- **Eredeti szöveg szerzősége:** Brown, F., Driver, S. R., & Briggs, C. A. — *A Hebrew and
  English Lexicon of the Old Testament* (BDB)
- **Digitalizálás:** Tim Morton (Bible Analyzer) eredeti transzkripciója, BibleHub
  adataival kereszt-ellenőrizve; Eliran Wong JSON-formázása
- **Licenc:** közkincs (public domain) — az eredeti BDB szövege és annak digitalizált
  átirata is közkincs

## Konverzió

Python szkripttel (`_convert_bdb.py`, a `konkordancia/` mappában, egyszeri
segédszkript) HTML-jelölés eltávolítva, egyszerű szöveggé alakítva. A Strong-szám
oszlop a repó zero-padded konvencióját követi (4 számjegyre kitöltve, pl. `H8415`,
`H1` → `H0001`), homográf-toldalékkal együtt (pl. `H90a` → `H0090a`) — konzisztens a
`Strong_szotar.tsv` és a `TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv` konvenciójával.

## Kimenet

**`BDB_teljes_unabridged.tsv`** (8090 sor + fejléc, 3 oszlop):
```
Strong_padded | Strong_eredeti | Teljes_szocikk
```

- **Strong_padded:** zero-padded Strong-szám, pl. `H8415`, `H0001`
- **Strong_eredeti:** a forrásfájl eredeti, nem kitöltött azonosítója (pl. `H8415`, `H1`, `H90a`)
- **Teljes_szocikk:** a teljes BDB-szócikk, tiszta szövegként (HTML-jelölés eltávolítva)

## Minőségi mutató

- **8090/8090 sor sikeresen konvertálva, üres bejegyzés nélkül** (minden sor tartalmaz
  legalább egy rövid szöveget — 10 bejegyzés 20 karakternél rövidebb, ezek legitim
  kereszthivatkozások más szócikkre, pl. `H0381` „ish-chayil" → lásd a fő szócikket).
- Ez lényegesen teljesebb, mint az openscriptures `BrownDriverBriggs.xml`, ahol a
  gyök-bejegyzések **17,5%-a (453/2595) feldolgozatlan** („new" státuszú, üres).
- Ellenőrzött minta: `H8415` (תְּהוֹם) — teljes, tartalmas szócikk (kb. 2400 karakter).

## Szerep a determinisztikus BDB-ellenőrzési protokollban

**Ez a fájl az ELSŐDLEGES teljes-BDB forrás** a determinisztikus BDB-ellenőrzési
protokoll 2. lépésében. Az openscriptures `BrownDriverBriggs.xml` +
`LexicalIndex.xml` (lásd `TBESH_TBESG_README.md`) másodlagos/tartalék szerepbe kerül
a hiányossága miatt.

**Fontos megállapítás (2026-09-02):** a הום-gyök „morajló mélység" etimológiai adat
(ami korábban a תְּהוֹם/1Móz 1:2 kapcsán felmerült) **egyik ellenőrzött BDB-forrásban
sem található** — sem a `TBESH.txt`-ben, sem az openscriptures XML-ben, sem ebben a
teljes, unabridged verzióban. Ez azt jelzi, hogy az az adat valószínűleg NEM
BDB-ből származott, és felülvizsgálatra szorul azokban a fájlokban, ahol
felhasználásra került.

## Kereszthivatkozás

Ez a fájl önálló, a `Strong_padded` mezőn keresztül join-olható a meglévő
`Strong_szotar.tsv`, `Karoli_Strong_kivonat.tsv` stb. táblákkal (l.
`Join_tabla_folyamat_magyarazat.md` mintája szerint). A meglévő fájlok
változatlanok maradtak, semmi nem lett törölve vagy felülírva.
