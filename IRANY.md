# IRÁNY — kelt: 2026-11-22 · gazdája: a szerkesztő · legfeljebb 40 sor

**Cél:** a Biblialex motívumlexikon. Most: hibátlan olvasó, és kész új generátor a TEREMT-próbához.

## Futó szálak (legfeljebb 2)
1. **Olvasó-javítás (#231).** Kész, ha a 60 felmért hiba mindegyike javítva, elvetve vagy „rád vár”, és a szerkesztő megnézte az ágas előnézetben. Következő lépés: indulás a #799 merge-e után.
2. **Új generátor (F218a).** Kész, ha az F218.13 a main-en van. Következő lépés: #797 merge → S9c → a szerkesztő megnézi a nézési csomagot → F218.13.
- Ma zárul, nem számít szálnak: #799 (olvasó-gyorsítás, 1. rész).
- **Utána** (a 2026-11-11-i ütemezés): a motívumok ráillesztése az olvasóra, ez az „alap” olvasó.

## Most NEM csináljuk
- Új lexikonlap: az új generátorral csak a TEREMT készül (próba).
- Új olvasó-felmérés, amíg a #231 nincs lezárva.
- Új motívumcikk a homonima-jelzés előtt (kivétel: TEREMT).
- BDB-szerkesztői javaslat a lapon: egy jövőbeli kiadásba.
- 218b, 218c, B0 (#236–#238): az F218.13 előtt nem indul.
- F235 2. rész (indexek, natív futás): a szerkesztő szaváig nem indul.
- Fizetős fordítás (N177, #24 görög glossza): a szerkesztő döntéséig nem.

## Így dolgozunk
- Egyszerre legfeljebb 2 szál. Az integrátor viszi az egyiket, és merge-el.
- A hibának három kimenete van: javítva / elvetve egy sor indokkal / rád vár. „Majd egyszer” nincs.
- Hamis vagy félrevezető tartalmat mutató hiba nem vethető el.
- Csak olvasó-kód: gyors sáv. Adat, generátor, próza: nehéz kör (DT919).
- Technikai kérdésben a session dönt; tartalmi kérdés az integrátorhoz (DT920).

## Rád vár
- #24: a görög rövid jelentések fordítása (pénz): igen vagy elvetve.
- #40 (BSB: 184 zsoltárvers hiányzik a forrásból) és #14 (LXX-számok forrása): elvetve vagy feladat.
- A Biblialex domain regisztrációja; a JOHD deposit formátuma.
- Az adatbázis-újraépítés kipróbálása (a parancsikon újraindítása, nincs figyelmeztetés).
- Archiválható-e: levelek-uj-cimzettek, betu-szin-elonezet.

*Frissítés: amit a szerkesztő irányként kimond, azt az integrátor még ugyanabban a válaszában beírja ide, és megmutatja. Új irányt magától nem ír bele, csak az állapotot (lezárult szál, megválaszolt kérdés). Új sor csak egy másik törlésével; legfeljebb 40 sor.*
