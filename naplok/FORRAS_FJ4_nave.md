# FORRAS_FJ4_nave.md — 3c: tiszta Nave-adatforrás

*FJ4 — FORRASJELOLTEK_BRIEF.md §3 szerint.*

## 1. A megvizsgálandó jelöltek

- **`basokant/nave`** — **nem létezik ilyen néven GitHub-repó** (`git clone` és
  `WebSearch` sem talál ilyet). Kizárva.
- **`theonize/bible_database`** — létezik, elérhető (`git clone --depth 1`).
- **`elcafe7/lex`** — létezik, elérhető (`git clone --depth 1`).

## 2. theonize/bible_database

- **URL:** `github.com/theonize/bible_database` · adat: `topics/Topics.csv`,
  `topics/TopicIndex.csv`, `topics/MainIndex.csv`
- **Szerkezet:** relációs, gépileg feldolgozható: `Topics.csv` (32 254 sor:
  TopicID, Topic, Subtopic — pontosan a Nave/Torrey "témakör → altéma"
  szerkezete), `TopicIndex.csv` (92 610 sor: TopicID→VerseID), `MainIndex.csv`
  (790 686 sor: szó-szintű teljes bibliaszöveg VerseID-kulccsal). **4 951
  egyedi főtémakör.**
- **Licenc:** a repó gyökér `LICENSE` fájlja **GNU GPLv3** szó szerint. A
  `README.md` mindössze ennyit mond: *"Database of open-source Bible texts and
  topical and cross references"* — **nem nevezi meg explicit forrásként
  Nave-et vagy Torrey-t**, bár a `Topics.csv` szerkezete (téma/altéma,
  igehely-hivatkozások) egyértelműen ráismerhető Nave/Torrey mintázatra. A
  GPLv3 **copyleft-kötelezettséget** ró a származékos műre, ami a jelen
  projekt saját licenc-céljaival ütközhet — ezt egy jogosult (a repó
  tulajdonosa vagy a projekt vezetője) tisztázása nélkül **nem lehet
  egyértelműen D17-kompatibilisnek** minősíteni.
- **3 témakör mintája (subtopic-darabszám a `Topics.csv`-ben):** Aaron: 27,
  Faith: 124, Prayer: 120 altéma-sor.

## 3. elcafe7/lex

- **URL:** `github.com/elcafe7/lex` · adat: `runtime-data/naves.db` (SQLite,
  `topics` tábla, `id, section, subject, entry, subject_upper` oszlopokkal,
  **5 319 témakör**, mindegyiknél egy hosszú, igehely-hivatkozásokkal teli
  `entry` szövegmező — pl. `AARON` entry 24 alpontja, mindegyik végén
  Strong-formátumú igehely-lista, "EXO 6:16-20; JOS 21:4,10; …").
- **Licenc:** a projekt saját `docs/LICENSING.md`-je **maga is
  bizonytalanként kezeli** a beágyazott adatokat ("Verify upstream terms
  before redistribution", "Data remains under source terms") — a Nave-adatot
  **nem is nevesíti** explicit tételként a licenclistában (csak "Strong's
  data", "TSK/OpenBible cross-references", "STEPBible", "UBS", "Easton",
  "ISBE" szerepel néven). Ez azt jelenti, hogy a `naves.db` eredete és
  licence **dokumentálatlan ebben a repóban** — a legrosszabb eset a hármas
  (`basokant`, `theonize`, `elcafe7`) közül licenc-tisztaság szempontjából.
- **3 témakör mintája:** `AARON` (24 alpont egy `entry`-ben), `ABADDON` (1
  alpont), `ABAGTHA` (1 alpont) — a struktúra kevésbé gépi feldolgozásra
  szánt (egy nagy szövegmező altémánként, nem külön sorok), az igehelyek
  kinyeréséhez saját regex-parszolás kellene.

## 4. Feldolgozhatósági arány

| Jelölt | Témakör-darabszám | Igehely-index | Szerkezet | Feldolgozhatóság |
|---|---|---|---|---|
| theonize/bible_database | 4 951 fő + 32 254 altéma | 92 610 (kész Topic↔Vers reláció) | 3 külön CSV, azonnal betölthető reláció | **magas** — nincs szükség parszolásra |
| elcafe7/lex | 5 319 | nincs kész reláció, csak szabad szöveg `entry` mezőben | SQLite, 1 táblás, szabadszöveges | **közepes** — igehely-kinyeréshez saját regex kell |

## 5. Verdikt

| Forrás | Javaslat | Indok |
|---|---|---|
| `basokant/nave` | **nem létezik** | — |
| `theonize/bible_database` | **feltétellel** | szerkezetileg a legjobb (kész reláció, magas feldolgozhatóság), de a GPLv3 repólicenc és a forrás meg nem nevezése (nincs explicit "Nave 1897, közkincs" nyilatkozat) miatt **jogosulti tisztázás szükséges** import előtt |
| `elcafe7/lex` | **feltétellel, gyengébb** | a saját `LICENSING.md` is bizonytalanként kezeli a `naves.db` eredetét — ez explicit dokumentálatlanság, rosszabb kiindulópont, mint a theonize GPLv3-nyilatkozata (ami legalább egyértelmű, ha korlátozó is) |

**Egyik jelölt sem "beválik" feltétel nélkül.** Mindkettő azonos alapproblémára
fut ki: **egyik repó sem idézi szó szerint, saját LICENSE/README-szövegéből,
hogy a Nave (1897) szövege maga közkincs** — ezt (a Wikipedia és a
`navestopicalbible.org` szerint) a jelen menet csak másodkézből tudja
megerősíteni, nem az adott repó saját nyilatkozatából, ahogy a §1 mércéje
megköveteli. **Javaslat a 2. menet előtt:** vagy egy tisztább, a Nave
közkincs-státuszát explicit nyilatkozó forrás felkutatása (pl. Project
Gutenberg-féle szövegkiadás gépi feldolgozása közvetlenül, saját
parszolóval), vagy a `theonize/bible_database` szerzőjének megkeresése
tisztázás céljából.
