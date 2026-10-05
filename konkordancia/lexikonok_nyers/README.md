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
- `TBESH.lexicon` (F42 óta nem itt van: `konkordancia/_nyers/tbesh/TBESH.lexicon`, gitignore-olt, csak helyben él; ez a leírás a fájlra továbbra is érvényes): egyetlen, konszolidált bejegyzés
  szavanként — ELTÉR a meglévő `TBESH.txt`-től, ahol egy szónak
  akár 4 alsora is lehet

## Tartalmi értékelés

L. `konkordancia/Uj_lexikon_fajlok_2026-09-07.md` — teljes,
fájlonkénti hasznossági rangsor.

## `konkordancia/MCGED_teljes.tsv` — Mounce-import (F05_SZOTAR_BRIEF.md S6)

**Generált** (`eszkozok/mcged_import.py`, kézzel nem szerkesztendő) a
`MCGED.lexicon` `G####` Strong-kulcsú sorai(ból — a `gkG5####` GK-kulcsú
sorok kihagyva, mert ugyanazt a szöveget ismétlik meg más kulccsal).
Fejléc: `strong gk_szam lemma_gorog atirat gyakorisag glossza`. A `gk_szam`
a HTML-ben beágyazott `lex("gkG5####")` `onclick`-hivatkozásból kinyerve
(a "gk" előtag levágva, `G5####` formában). 5 303 sor.

**Bemenet SHA-256** (`konkordancia/lexikonok_nyers/MCGED.lexicon`, a
generált `MCGED_teljes.tsv` fejlécében is szerepel):
`8d3b4e9c22e86c6e690febacb6639e07f8bc1d6d1f8e2336a7229514e6e271bb`.

**A `atirat` mező FONTOS eltérése a TBESG/TAGNT-konvenciótól:** a MCGED az
upsilont `y`-nal írja át (pl. `κύριος` → `kyrios`), NEM `u`-val, ahogy a
`TAGNT_kivonat.tsv`/`TBESG.txt` „Kiejtés” oszlopa (`kurios`) — két,
egymástól független forrás-konvenció, felfedezve az S1.4 importja során
(D33, `adat/kiejtes_szabalyok.tsv` fejléce). Ha ez a mező valaha a
`eszkozok/kiejtes.py`-n megy át, mindkét szabály (`u`→`ü` ÉS `y`→`ü`)
szükséges — mindkettő megvan a táblában, de a `y`→`ü` szabály **erre a
mezőre még nincs gold-párral igazolva**.

**Licenc:** © Mounce 1993, kötelező forrásmegjelöléssel
(`www.teknia.com/greek-dictionary`) minden idézetnél (F6 D16).
