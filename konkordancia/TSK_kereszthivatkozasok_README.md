# TSK (Treasury of Scripture Knowledge) kereszthivatkozások

Ez a dokumentum a `konkordancia/TSK_kereszthivatkozasok.tsv` fájlt írja le: forrás,
licenc, generálás módszere. Ez a projekt **második** editoriális kereszthivatkozás-
forrása a `Karoli_kereszthivatkozasok.tsv` (szentiras.hu/HunKar) mellett — lásd a
`PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` 4.6 pontját, ahol ez a forrás
(openbible.info alapú, szavazat-súlyozott) eredetileg azonosításra került, akkor még
a `krisek/HunKar`-nál gyengébb, másodlagos jelöltként.

## Forrás

- **Eredeti adat:** [OpenBible.info](https://www.openbible.info/labs/cross-references/)
  — Treasury of Scripture Knowledge (TSK) alapú, közösségi szavazattal (votes) súlyozott
  kereszthivatkozás-adatbázis.
- **Elérési út:** az `openbible.info` domain közvetlenül nem elérhető ebből a
  környezetből, ezért a GitHub-tükrön keresztül lett letöltve:
  [scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases),
  `formats/sql/extras/cross_references_0.sql` .. `cross_references_6.sql` (7 fájl).
- **Letöltés dátuma:** 2026-08-26 (`raw.githubusercontent.com`, `master` branch).
- **Licenc:** Creative Commons Attribution (CC BY) — az OpenBible.info saját
  nyilatkozata szerint (a cross-reference adatkészlet újrafelhasználható,
  forrásmegjelöléssel).
- **Nyers méret:** 7 SQL-dump, összesen ~111 MB, 432 949 `INSERT` sor. A nyers fájlok
  **nem** kerültek be a repóba (a projekt eddigi gyakorlatának megfelelően — lásd pl.
  a TVTMS-fájl kezelését a `Validacios_naplo.md`-ben), csak a belőlük generált
  kimenetek.

## Nyers séma

```sql
CREATE TABLE cross_references (
  id INT, from_book VARCHAR, from_chapter INT, from_verse INT,
  to_book VARCHAR, to_chapter INT, to_verse_start INT, to_verse_end INT,
  votes INT
);
```

A `from_book`/`to_book` mezők teljes angol könyvnevet használnak (pl. `Genesis`,
`1 Samuel`, `Song of Solomon`) — ez eltér a projekt STEPBible-natív konvencióitól,
ezért külön konverziós tábla készült (lásd lent). A `votes` mező **előjeles** lehet
(a nyers adatban 1359 sornak negatív a szavazata) — ez azt jelzi, hogy a TSK
közösségi szavazói szerint az adott kapcsolat vitatott/gyenge, nem hibás adat.

## Könyv-név konverzió — angol teljes név → STEPBible-kód

`konkordancia/Angol_konyvnev_STEPBible_tabla.tsv` (66 sor + fejléc), oszlopok:
`Angol_teljes_nev`, `STEPBible_kod`.

A nyers adatban ténylegesen előforduló 66 egyedi angol könyvnév (`from_book`/`to_book`
mezők uniója) lett kigyűjtve és egyenként megfeleltetve a projekt STEPBible-natív
kódjainak (`Konyv_normalizalo_tabla.tsv` első oszlopa). A ténylegesen használt alakok
ellenőrzésre kerültek — a feltételezett elnevezési eltérések (pl. `Song of Songs`,
`Revelation of John`) **nem** fordultak elő; a forrás mindkét esetben a standard KJV-
alakot használja (`Song of Solomon`, `Revelation`). Validáció: mind a 66 generált
STEPBible-kód szerepel a `Konyv_normalizalo_tabla.tsv`-ben, és fordítva — **66/66
egyezés mindkét irányban**, 0 eltérés.

## Kimeneti fájl és oszlopok

```
Igehely | Kapcsolódó igehely | Kapcsolódó igehely magyar megjelenítése | Votes
```

- **Igehely:** Károli-natív formátumban (pl. `1Móz 1:1`) — a `from_book/from_chapter/
  from_verse`-ből, a `Konyv_normalizalo_tabla.tsv` és az `Angol_konyvnev_STEPBible_
  tabla.tsv` láncolt alkalmazásával (angol név → STEPBible-kód → magyar rövidítés).
- **Kapcsolódó igehely:** ugyanabban a Károli-natív, kettősponttal tagolt formátumban,
  a `to_book/to_chapter/to_verse_start(-to_verse_end)`-ből. Ha `to_verse_start` ≠
  `to_verse_end`, tartományként jelenik meg (`Könyv fejezet:vers-vers`), a
  `Karoli_kereszthivatkozasok.tsv` mintájára.
- **Kapcsolódó igehely magyar megjelenítése:** ugyanaz a hivatkozás, magyar
  tipográfiai konvenció szerint (vessző a fejezet és a vers között, pl. `Péld 8,22`,
  `1Krón 16,26`) — **módszertani megjegyzés:** a TSK nyers adat (szemben a
  `Karoli_kereszthivatkozasok.tsv` OSIS-forrásával) nem tartalmaz saját, kész
  megjelenítési szöveget, ezért ez az oszlop a `Kapcsolódó igehely` oszlopból lett
  szabályalapon (kettőspont → vessző csere) előállítva, nem egy forrás-mezőből
  átvéve.
- **Votes:** változatlanul, szűretlenül átvéve a nyers adatból (beleértve a negatív
  értékeket is) — a szűrés (pl. votes ≥ 15-20) a tanulmányírás idején, felhasználáskor
  történjen, nem itt, hogy ne vesszen el adat.

**Strong-szám nincs a fájlban** — ugyanúgy, mint a `Karoli_kereszthivatkozasok.tsv`
esetén, ez a forrás sem lexikai konkordancia, hanem szerkesztőségi/tematikus
kereszthivatkozás-lista.

## Nem illeszthető sorok

A teljes 432 949 nyers sor **mindegyike** sikeresen konvertálódott Károli-natív
formára — **0 nem-illeszthető sor**, tehát a
`konkordancia/TSK_kereszthivatkozasok_nem_illesztheto.tsv` fájl **nem jött létre**
(nem volt mit belé gyűjteni). Ha egy jövőbeli frissítés során a forrás bővülne olyan
könyvvel, ami nincs az `Angol_konyvnev_STEPBible_tabla.tsv`-ben (pl. deuterokanonikus
könyv), a generáló szkriptet újra kell futtatni, és az akkor keletkező nem-illeszthető
sorokat ebbe a fájlba kell gyűjteni, a nyers angol hivatkozással.

## Votes oszlop — eloszlás és használati javaslat

- Tartomány: -31 – 1268
- Medián: 3
- Negatív értékek is előfordulnak (pl. 1Móz 1:1 → 2Móz 31:18, votes=-31) — ez valódi
  nyers adat a forrásból, nem feldolgozási hiba (ellenőrizve a nyers SQL-ben).
- A 432 949 sor túlnyomó része alacsony megbízhatóságú (medián=3) — használatnál
  szűrés javasolt: Votes ≥ 15 → 25 473 sor marad; Votes ≥ 20 → 16 874 sor marad.
- A szűrés a FELHASZNÁLÁS (tanulmányírás) idején történjen, nem itt — ez a fájl a
  teljes, szűretlen adatot tartalmazza, hogy semmi ne vesszen el.

## Irányfüggőség — fontos figyelmeztetés

A TSK adat IRÁNYFÜGGŐ: ugyanahhoz a verspárhoz két külön sor tartozhat, eltérő
Votes-értékkel (pl. `1Móz 1:1 → Ján 1:1` = 304, de `Ján 1:1 → 1Móz 1:1` = 276 —
ellenőrizve, 2026.08.27). Ez NEM hiba, hanem a TSK saját adatszerkezetének
sajátossága. Lekérdezéskor MINDIG a vizsgált igehely SAJÁT sorából induljunk
(nem a célvers oldaláról) — ez konzisztens módszertant ad, még ha a két irány
száma eltér is.

## Méret és validáció

| Mérőszám | Érték |
|---|---|
| Nyers `INSERT` sorok (7 SQL-fájl összesen) | 432 949 |
| Generált sorok (`TSK_kereszthivatkozasok.tsv`) | 432 949 |
| Eltérés a nyers és a generált sorszám között | 0% |
| Nem illeszthető sorok | 0 |

**Validáció — Gen 1:1 (`1Móz 1:1`):**

| Kapcsolódó igehely | Votes | Eredmény |
|---|---|---|
| Péld 8:22 | 59 | egyezik |
| Péld 8:30 | 59 | egyezik |
| Zak 12:1 | 49 | egyezik |
| ApCsel 14:15 | 62 | egyezik |

Mind a négy megadott validációs eset pontosan egyezik.

## Fontos korlát — ez is csak JELÖLTLISTA

Ugyanúgy, mint a `Karoli_kereszthivatkozasok.tsv` esetén: **ez a dataset kizárólag a
3/b pont (Kapcsolódó igehelyek) kiindulási jelöltlistájául szolgál — nem helyettesíti
a tartalmi mérlegelést.** A TSK egy szerkesztőségi (nem lexikai, nem közös görög/héber
szótő alapú) kereszthivatkozás-gyűjtemény — lehet tematikus, teológiai vagy tipológiai
összefüggés is a `votes` értékétől függetlenül. **Minden találatot kézzel kell
értékelni** a `sablonok/PaRDeS_gyorsreferencia.md` "3/b. Kereszthivatkozási réteg"
szakasza szerint (lexikai vs. tematikus elhatárolás, STEPBible TAHOT/TAGNT-
ellenőrzéssel), mielőtt egy adott kapcsolódás bekerül egy tanulmányba.

**A két editoriális kereszthivatkozás-forrás (`Karoli_kereszthivatkozasok.tsv` és
`TSK_kereszthivatkozasok.tsv`) egymáshoz való viszonya továbbra is nyitott kérdés** —
a Károli-specifikus forrás szűkebb (32 408 sor), de közvetlenül a magyar hagyományból
származik; a TSK jóval szélesebb (432 949 sor) és szavazat-súlyozott, de angol nyelvű
köztes hagyományból. Melyik mikor megbízhatóbb, illetve hogyan egészítik ki egymást —
tényleges összevetéssel eldöntendő, jövőbeli kérdés, nem ennek a feladatnak a része.
