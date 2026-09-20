# Nyers lexikon-fájlok (SQLite, biblematedata-csomag)

*Beemelve: 2026.09.07. Forrás: Eliran Wong `biblematedata` projektje
(github.com/eliranwong/biblematedata), Google Drive fájl-ID:
`1xlvJ6GURwYCxPnYwo2xuyREutWTeWMcH` (a projekt `main.py`
forráskódjából azonosítva).*

## Licenc-státusz *(F6_BRIEF.md §1.6, v4/v5)*

A fájlok maguk nem tartalmaznak explicit licenc-jelzést. A
`biblematedata`-csomag (Eliran Wong) lexikon-moduljainak forrását és
licencét a szerző saját forrásoldala (`marvel.bible/resource.php`)
dokumentálja. A 2026-09-19-i lekérdezés szerint:

| Forrás | A szerző forrásoldala szerint | Besorolás |
|---|---|---|
| Thayer | 1886/1889, közkincs; a modul anyagát Tim Morton (Bible Analyzer) formázta, engedéllyel | `közkincs` — a formázási réteg eredete másodkézből, ezt a README rögzíti |
| LSJ | Perseus `lexica` repó, Creative Commons Attribution-ShareAlike 3.0 | `CC BY-SA 3.0` |
| SECE | közkincs, az `openscriptures/strongs` repóból, a szerző kiegészítő leképezésével | `közkincs` |
| MCGED | `billmounce/dictionary`, ezzel a kötelező megjelöléssel: *Mounce Concise Greek-English Dictionary, Copyright 1993 All Rights Reserved, www.teknia.com/greek-dictionary* | `© Mounce 1993`, megjelölés kötelező |
| Abbott-Smith (a TBESG alapja) | 1922-es kiadás, közkincs | `közkincs` |

**Fenntartás:** ezek a megállapítások a szerző forrásoldaláról származnak, nem a
letöltött fájlokhoz csatolt licencszövegből — a `lexikonok_nyers/` fájljai nem
tartalmaznak licenc-jelzést. A modulok azonossága erősen valószínű, de nem
bizonyított; egy saját, rögzített import az eredeti forrásból (Perseus,
OpenScriptures) ezt a bizonytalanságot is megszüntetné (F6_BRIEF.md N5).

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
