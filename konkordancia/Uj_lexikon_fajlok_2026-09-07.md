# Új lexikon-fájlok felmérése (2026.09.07)

*A `Javasolt_gorog_oldal_erositese.md`-ben (2026.09.05) dokumentált
"3. lehetőség" (LSJ/Thayer beszerzése) folytatása — a felhasználó
ténylegesen letöltötte a `biblematedata` (Eliran Wong) projekt teljes
lexikon-csomagját Google Drive-ról (fájl-ID:
`1xlvJ6GURwYCxPnYwo2xuyREutWTeWMcH`, a `biblematedata` package
`main.py` forráskódjából azonosítva). 12 SQLite-fájl, mindegyik
`Lexicon` táblával, `Topic`/`Definition` oszlopokkal. A fájlok
egyelőre NINCSENEK a repóba emelve — ez a dokumentum csak a
tartalom-felmérés eredménye, döntés még nem történt.*

## A 12 fájl és projekt-szintű hasznossága

| Fájl | Tartalom | Kulcs-formátum | Projekt-szintű érték |
|---|---|---|---|
| **Thayer.lexicon** | Teljes Thayer's Greek-English Lexicon, 5427 bejegyzés | `G1`, `G2`, ... (nincs nullákkal kitöltve) | **Magas** — a görög oldal BDB-párja, minden görög szót érintő study profitálna belőle |
| **LSJ.lexicon** | Liddell-Scott-Jones klasszikus szótár — átlag 5068, max 61 640 karakteres szócikkek | `G1`, `G2`, ... | **Célzottan magas** — összetett igéknél (pl. ἐπικαλέω) csak az alapigére irányít át, DE az alapige (pl. καλέω) szócikke hatalmas és mély; különösen értékes klasszikus/filozófiai gyökerű szavaknál (pl. πνεῦμα/ψυχή a Pneuma/pszükhé tematikus study-hoz) |
| **MCGED.lexicon** | Mounce Concise Greek-English Dictionary (GK+Strong) | `G####` ÉS `gkG5####` (kétféle kulcs, óvatosan kezelendő — az azonos szám más szót jelenthet a két rendszerben!) | **Közepes** — pontos NT-előfordulás-szám minden szóra (gyorsítja a 2/c lépést), tömör modern gloss |
| **SECE.lexicon** | Kibővített Strong's: kiejtés, Louw-Nida szemantikai domain, GK-szám, **teljes célnyelvi megfelelő-lista** (héber szónál az összes LXX-görög fordítás, görög szónál az összes héber forrás) | `G####`, `H####` (mindkét nyelv!) | **Magas** — a Louw-Nida domain-számok teljesen új, szemantikai (nem gyök-alapú) keresési dimenziót nyitnak; a teljes megfelelő-lista függetlenül megerősítette a mai LXX-fordítói-változatosság megfigyelést (l. lent) |
| **BDB.lexicon** (SQLite) | Ugyanaz a BDB, mint a meglévő `BDB_teljes_unabridged.tsv`, de **teljesebb** (H7121-nél 13 027 vs. 10 781 tisztított karakter — kb. 21%-kal több szöveg, benne további Gesenius-grammatika-hivatkozásokkal) | `H####` | **Közepes** — nem vált ki semmit, de gazdagítja a meglévő TSV-t |
| **TBESH.lexicon** (SQLite) | Ugyanaz, mint a meglévő `TBESH.txt`, de **konszolidált, egyetlen bejegyzés** szavanként (nincs többsoros G/H/I/J-probléma) | `H####` (egységes) | **Magas** — ez ténylegesen megoldja a `TBESH_TBESG_README.md`-ben dokumentált, nyitott "többsoros Strong-szám" módszertani kérdést |
| **TBESG.lexicon** (SQLite) | Ugyanaz, mint a meglévő `TBESG.txt` | `G####` | Már ismert, nincs új tartalom |
| **LXX.lexicon** | Klasszikus görög szójegyzék (LSJ-alapú, alfabetikus) | `L7######` (belső sorszám, NEM Strong-szám) | **Alacsony** — nehezen hasznosítható Strong-szám-alapú kereséssel |
| **MGLNT.lexicon** | Abbott-Smith szövege, de héber szavak helyett Strong H-szám-hivatkozásokkal | `G####` | **Nincs** — duplikátum, a meglévő TBESG/Abbott-Smith ugyanezt adja, valódi héber szöveggel |
| **ConcordanceBook.lexicon** | Könyv-index konkordancia-kereséshez | `E7#####` (belső kód) | **Alacsony** — navigációs segédeszköz, a meglévő TAHOT/TAGNT kényelmesebben kiszolgálja |
| **Morphology.lexicon** | Héber morfológiai paradigma-táblák (prefixek, toldalékok) | `E7#####` | **Alacsony** — általános nyelvtani segédanyag, nem szó-specifikus |
| **ConcordanceMorphology.lexicon** | Vegyes morfológia + konkordancia | `E7#####` | **Alacsony** — hasonló az előzőhöz |

## Kiemelt, projekt-szintű felfedezés — a SECE héber→görög lista

A SECE H7121 (קָרָא) bejegyzése felsorolja **az ÖSSZES görög igét**,
amit a LXX valaha használt e szó fordítására — ebben a listában
egyszerre szerepel **βοάω, καλέω és ἐπικαλέομαι** is. Ez független
forrásból (teljes LXX-átfogó kereszthivatkozás, nem csak a
"Segítségül hívni" motívum 17 igehelye) **megerősíti**: a קָרָא
fordítói rutinszerűen választanak mindhárom görög ige közül,
kontextustól függően — ez NEM a 2Móz 33:19/34:5 és Ézs 12:4
egyedi sajátossága, hanem egy jól ismert, széles körű mintázat.

## Rangsorolt javaslat, ha a beépítés mellett döntenél

1. **SECE** (Louw-Nida + teljes megfelelő-lista) — legnagyobb új
   képesség
2. **Thayer** — a görög oldal BDB-párja
3. **TBESH.lexicon (SQLite, konszolidált)** — lezárja a nyitott
   "többsoros Strong-szám" kérdést
4. **MCGED** — gyorsítja a napi munkát (előfordulás-szám)
5. **LSJ** — célzottan, ahol releváns (pl. Pneuma/pszükhé study)
6. **BDB.lexicon (SQLite)** — csak ha a plusz ~20% szöveg
   ténylegesen hiányzik valahol
7. MGLNT, LXX.lexicon, ConcordanceBook, Morphology,
   ConcordanceMorphology — nem javasolt beépítésre

## Amit ez a dokumentum NEM tesz

- Nem emeli be egyik fájlt sem a repóba
- Nem dönt a licenc-kérdésről (a fájlok maguk nem tartalmaznak
  explicit licenc-jelzést — ezt tisztázni kellene, mielőtt bármelyik
  ténylegesen bekerülne)
- Nem konvertál semmit tiszta TSV-vé (a HTML-jelöléses `Definition`
  mezők tisztítása külön munka lenne, hasonlóan a BDB-nél korábban
  elvégzetthez)
