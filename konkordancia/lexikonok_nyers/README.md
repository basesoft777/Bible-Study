# Nyers lexikon-fájlok (SQLite, biblematedata-csomag)

*Beemelve: 2026.09.07. Forrás: Eliran Wong `biblematedata` projektje
(github.com/eliranwong/biblematedata), Google Drive fájl-ID:
`1xlvJ6GURwYCxPnYwo2xuyREutWTeWMcH` (a projekt `main.py`
forráskódjából azonosítva).*

**⚠️ LICENC-STÁTUSZ TISZTÁZATLAN.** A fájlok maguk nem tartalmaznak
explicit licenc-jelzést. Ez a beemelés Basesoft explicit döntése
alapján történt, méret- és licenc-ellenőrzés NÉLKÜL — ezt utólag
tisztázni kell, mielőtt a tartalom bármilyen publikus vagy
harmadik féllel megosztott anyagba kerülne.

## Formátum

Mind a 12 fájl SQLite 3.x adatbázis, egyetlen `Lexicon` táblával,
`Topic`/`Definition` oszlopokkal. Lekérdezési minta:

```python
import sqlite3, re
conn = sqlite3.connect('konkordancia/lexikonok_nyers/Thayer.lexicon')
cur = conn.cursor()
cur.execute('SELECT Definition FROM Lexicon WHERE Topic=?', ('G1941',))
row = cur.fetchone()
text = re.sub('<[^>]+>', ' ', row[0])
```

**Kulcs-formátum eltérések** (teljes részletezés:
`motivumlog/lexikon_pilot/Atadasi_dokumentum_Motivumlexikon_pilot_2026-09-07.md`,
3.2 pont):

- `Thayer`, `LSJ`, `SECE`, `MGLNT`: görög Strong-szám NULLÁK NÉLKÜL
  (`G994`, nem `G0994`)
- `MCGED`: kétféle kulcs (`G####` Strong ÉS `gkG5####`
  Goodrick-Kohlenberger) — a kettő NEM ugyanaz a szó ugyanarra a
  számra
- `SECE`: mindkét nyelv egy fájlban (`G####` és `H####` is)
- `TBESH.lexicon` (ez a fájl): egyetlen, konszolidált bejegyzés
  szavanként — ELTÉR a meglévő `TBESH.txt`-től, ahol egy szónak
  akár 4 alsora is lehet

## Tartalmi értékelés

L. `konkordancia/Uj_lexikon_fajlok_2026-09-07.md` — teljes,
fájlonkénti hasznossági rangsor.
