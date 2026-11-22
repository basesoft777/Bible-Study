# IRÁNY — kelt: 2026-11-22 · gazdája: a szerkesztő · legfeljebb 40 sor

**Cél:** a Biblialex motívumlexikon. Most: hibátlan olvasó, és kész új generátor a TEREMT-próbához.

## Futó szálak (legfeljebb 2)
1. **Olvasó-javítás (#231).** Kész, ha a 60 felmért hiba mindegyike javítva, elvetve vagy „rád vár”, és a szerkesztő megnézte az ágas előnézetben. Fut (a #799 2026-11-22-én bent).
2. **Új generátor (F218a).** Kész, ha az F218.13 a main-en van. A #797 bent; fut az S9c → a szerkesztő megnézi a nézési csomagot → F218.13.
- **Következő szál** (az olvasó-javítás után, gazdája az integrátor): a 15 perces kapu kettévágása; munka közben füstteszt, a teljes kapu egyszer, a merge-kész állapotra.
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
- Fordítás (pénz), igen vagy elvetve: #24 a görög rövid jelentések (N177); #23 a Thayer magyarja (354 / 5 426 kész; a következő adag kb. 10 USD).
- JOHD (#762, #763, draft): az emberi validáció és a 21 fejezetes újramérés bemásolása; a deposit formátuma.
- Külső lépések: a Biblialex domain; a BiblIndex-levél (patrisztikus igehely-index, a visszhang-réteghez: küldés vagy elvetve; a tervezetben még a régi „Logosz-lexikon” név áll); a KJV-licenc kérdése a CrossWire-nek (csak a fizetős megjelenítés előtt).
- Az F134 telefonos próbája. A BDB harmadik tanúja (N212: a mintán 70%-ban a mi táblánk téved): a tábla javítása feladat legyen, vagy elvetve.
- Archiválható-e: levelek-uj-cimzettek; betu-szin-elonezet (6 merge-eletlen commit: a betűválasztó előnézete).

*Frissítés: amit a szerkesztő irányként kimond, azt az integrátor még ugyanabban a válaszában beírja ide, és megmutatja. Új irányt magától nem ír bele, csak az állapotot (lezárult szál, megválaszolt kérdés). Új sor csak egy másik törlésével; legfeljebb 40 sor.*
