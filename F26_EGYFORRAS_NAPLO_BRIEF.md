---
feladat: 26
cim: Egyforrású lánc (B) döntéseinek rögzítése és az érintett briefek fejléce
kod: EGYFORRAS_NAPLO
tipus: naplozas
modell: sonnet
ag: claude/f26-egyforras-naplo
allapot: lezarva
ad: a D34–D41 a FELADATOK.md döntésnaplójában; a #9–#12 fejléce a B szerkezethez igazítva; CLAUDE.md átmeneti sor; BRIEF_SABLON D39-sor
kovetkezo: lezárva
olvas: [FELADATOK.md, CLAUDE.md, BRIEF_SABLON.md, "F*_BRIEF.md"]
ir: [FELADATOK.md, F09_SZOTAR_S2_BRIEF.md, F10_LEXIKON_LEZARAS_BRIEF.md, F11_MIGRACIO_BRIEF.md, F12_TEREMT002_PROZA_BRIEF.md, CLAUDE.md, BRIEF_SABLON.md]
fugg: []
pr: 168
lezarva_osszegzes: D34–D41 rögzítve, #9–#12 fejléc; DT-F26b/c alkalmazva (DT-F32a irányadó; F10 LXX-előfeltétel vissza); DT-F26a a #11-re vár
---

# F<nn>_EGYFORRAS_NAPLO_BRIEF.md — Egyforrású lánc (B) döntéseinek rögzítése

*FELADATOK #<nn> · Modell: sonnet · v1 · 2026.09.30 · naplózás, tartalmi munka nélkül*

## 1. Cél

A chat 2026.09.30-án eldöntötte a render-lánc átalakítását. A régi lánc: tanulmány → tematikus → lexikonoldal → törzscikk. Az új: tanulmány → **egy kézi forrás motívumonként** → generált nézetek állítható mélységgel („B” út). Ez a brief rögzíti a döntéseket, és a 2. fázis érintett briefjeinek fejlécét hozzáigazítja, hogy a `feladatok.py` a helyes sorrendet számolja: #9 → #12 (pilot) → #11 → #10.

## 2. Előfeltétel

A MOTIVUM_FORRAS, a LICENC és az OLVASOI_HTML brief befogadása a `main`-en van. A számukat a `main` fejléceiből vedd, a `kod` mező alapján. Az alábbiakban `#MF` = MOTIVUM_FORRAS, `#LIC` = LICENC, `#HTML` = OLVASOI_HTML. Ha bármelyik hiányzik a `main`-ről, állj meg és jelezd.

## 3. Lépések

### N1 — Döntésnapló (`FELADATOK.md`, „Döntésnapló” kézi szakasz)

A sorokat a következő szabad D-számtól vedd fel, sorrendben. A chat D34-től számolt; ha közben foglalt lett, csússzon, és a három másik brief `D3x`/`D4x` hivatkozásait **csak a zárójelentésben** jelezd, a briefeket ne írd át. A `#MF`, `#LIC`, `#HTML` helyére a valódi számot írd.

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D34 | Motívumonként egy kézi forrás (`motivumok/[ID].md` + `adat/`), a tematikus sablon szerkezetével; a tematikus tanulmány, a lexikonoldal és az olvasói nézetek generáltak; a törzscikk a #11-ben megszűnik; a bővített tanulmányok önállóak, a forrás hivatkozik rájuk, nem másol | a teljes Biblia korpusznál a párhuzamos kézi dokumentumok nem tarthatók fenn; az ISTENTISZT-001 8 briefje | a tematikus önálló forrás marad („A” út); lexikonoldal + törzscikk |
| D35 | Generált fájlba kézzel nem írunk; CI: az újragenerált nézet bájtazonos a commitolttal (leírás: #MF, implementálás külön ágon, D6) | a szabályt gép őrzi, nem fegyelem | marker-fegyelem vegyes fájlban |
| D36 | Mélységi szintek blokkszintű jelöléssel a SEMA-ban, három szinttel indulva (olvasói / apparátus / belső); a belső réteg buildkor kimarad | a csukott vagy CSS-sel rejtett blokk a forrásban olvasható | rejtett belső réteg; négy szint előre |
| D37 | Egy forrássablon minden motívumra; a ⭐ küszöb alatt a tematikus szakaszok inaktívak | nincs második sablon, nincs átköltöztetés a küszöb elérésekor | küszöb alatt csak adatsor |
| D38 | Pilot két lépcsőben: #12 TEREMT-002 (natív), majd a #11 1. lépcsője ISTENTISZT-001-en (örökölt, legnagyobb); a többi 6 motívum ezután | a kicsi natív pilot nem mutatja a migráció nehéz eseteit | csak TEREMT-002; mind a 8 egyszerre |
| D39 | Egy motívumon egyszerre egy feladat fut: a motívumot érintő brief `ir` listája motívumszinten nevezi meg a fájlokat (`motivumok/<ID>.md`, `lexikon/<ID>_*`), így a meglévő ütközésszámítás soros futást ad | egy forrásfájl, ütközés nélkül; nem kell eszközmódosítás | fájlszintű merge-feloldás; új orkesztrátor-szabály |
| D40 | Olvasói felület: statikus HTML (Netlify), később PWA (#HTML); modul-export (MyBible/e-Sword) későbbi opció | nincs telepítés, egy kódbázis, linkkel megosztható; az UniqueBible utódra cserélődött, GPL-köt, mobilon nehézkes | app; UniqueBible-alap |
| D41 | Forráslicencek átnézése az 1. fázisban, adatkészlet-szintű licenctáblával (`adat/licencek.tsv`, #LIC) | nyilvános vagy kereskedelmi kiadás fő korlátja; adatréteg-kérdés | élesítés előtt; soronkénti licencoszlop |

A generált blokkokhoz ne nyúlj: a táblákat a `main`-re futó Action frissíti a fejlécekből (D24, D25).

### N2 — Az érintett briefek fejléce és csonk-szövege

Csak az alábbi mezőket és a csonk „Mit ad” / „Következő lépés” sorát írd át, a kettő egyezzen. Más tartalomhoz ne nyúlj.

| Brief | Mező | Új érték |
|---|---|---|
| F09 | `ad` | az 1. fázis adatai megjelennek a 8 lexikonoldalon és a 8 törzscikkben; a törzscikk utoljára itt generálódik (D34) |
| F09 | `fugg` | `[5, 6, #MF]` |
| F10 | `kovetkezo` | **Te:** döntés az L6 és L7 feltételről. Ide tartozik N18, N19. Az L-feltételek törzscikkre vonatkozó pontjai kikerülnek (D34) |
| F10 | `fugg` | `[8, 9, 11]` |
| F11 | `ad` | minden motívum egyetlen kézi forrásból renderel (D34); a törzscikk, a 8. sablon és a CI E11 kivezetve (a CI-rész külön ágon, D6) |
| F11 | `kovetkezo` | 1. lépcső ISTENTISZT-001, utána a többi 6 (D38); brief a #12 után |
| F11 | `fugg` | `[9, 12, #MF]` |
| F12 | `ad` | az első natív egyforrású motívum a D34 szerkezetben, a B pilotja (D38) |
| F12 | `fugg` | `[9, #MF]` (a 11 kikerül) |

### N3 — `CLAUDE.md`

A „Rétegek” táblázat alá egy sor:

> *Átmenet (D34): a cél motívumonként egyetlen kézi forrás, minden más nézet generált. A fenti táblázat a #11 lezárásáig érvényes; a törzscikket addig a meglévő generátor állítja elő.*

### N4 — `BRIEF_SABLON.md`

A „Közös koordinációs fájlok” bekezdés után egy sor:

> *Motívumot érintő feladat `ir` listájában a motívum fájljai egyenként szerepelnek (`motivumok/<ID>.md`, `lexikon/<ID>_*`), nem csak a könyvtár; így egy motívumon egyszerre egy feladat fut (D39).*

## 4. Ellenőrzés és zárás

1. `python eszkozok/feladatok.py ellenoriz` = 0.
2. `python eszkozok/feladatok.py fuggesek`: a kimenetben körkörös függés nincs, és a sorrend #MF → #9 → #12 → #11 → #10. A kimenetet idézd a zárójelentésben.
3. Zárás a `/kovetkezo` szerint: `fuggetlen-ellenor`, draft PR, a saját fejléc `lezarva`.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.09.30 | első változat | a chat D21–D28-as munkaszámai ütköztek a `main` D21–D33 soraival, ezért D34-től; a törzscikk a #9-ben még generálódik (így az E11 jelzése is megszűnik), és csak a #11-ben szűnik meg; a D39 eszközmódosítás nélkül, az `ir` listán át érvényesül |
