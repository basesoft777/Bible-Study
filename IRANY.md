# IRÁNY — kelt: 2026-11-22 · gazdája: a szerkesztő · legfeljebb 40 sor

**Cél:** a Biblialex motívumlexikon. Most: hibátlan olvasó, és kész új generátor a TEREMT-próbához.

## Futó szálak (legfeljebb 2)
1. **Olvasó-javítás (#231).** Lefedi: a 60 felmért hibát, benne a héber szócsoport-csempéket (F233: írott szó szerinti keret, a teljes szó felül, nem létező alak nélkül; a lista 30–31.), az F233 többi tervezési pontját (36., 37., 53.) és az F234 pontjait. Nem fedi (a 60-ból kettő): a motívumlapot (59., az „Utána” szál) és a pénzes fordítást (lent, „Rád vár”). Kész, ha a 60 felmért hiba mindegyike javítva, elvetve vagy „rád vár”, és a szerkesztő megnézte az ágas előnézetben; a merge után az integrátor újraindítja a tükröt, és ellenőrzi az adatbázis-másolatot (az új építés 2026-11-22 18:58). Fut (a #799 2026-11-22-én bent).
2. **Új generátor (F218a).** Lefedi: az új lapgenerátor 1. részét, a HAMART-lapon mérve; az S9c az utolsó szelet és a nézési csomag (a 11 hely előtte/utána). Kész, ha az F218.13 a main-en van. A #797 bent; fut az S9c → a szerkesztő megnézi a nézési csomagot → F218.13.
- **Következő szál** (az olvasó-javítás után, gazdája az integrátor): a 15 perces kapu kettévágása; munka közben füstteszt, a teljes kapu egyszer, a merge-kész állapotra; benne a main-en bukó `teszt_sqlite_epit.py` test_11 és a merge-enkénti BEHIND-kör.
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
- A hibának három kimenete van: javítva / elvetve egy sor indokkal / rád vár. „Majd egyszer” nincs; hamis vagy félrevezető tartalmat mutató hiba nem vethető el.
- Csak olvasó-kód: gyors sáv. Adat, generátor, próza: nehéz kör (DT919).
- Technikai kérdésben a session dönt; tartalmi kérdés az integrátorhoz (DT920).
- Az állapot csak leírva él: ez a lap, a nyitott PR-ok első sora (Állapot · Következő · Akadály), a DONTESEK. Az integrátor naponta vagy fél kontextusnál cserél; az utód briefje: „olvasd el az IRANY.md-t és a nyitott PR-ok első sorát”.

## Rád vár
- Fordítás (pénz), igen vagy elvetve: #24 a görög rövid jelentések (N177); #23 a Thayer magyarja (354 / 5 426 kész; a következő adag kb. 10 USD).
- JOHD (#762, #763, draft): az emberi validáció és a 21 fejezetes újramérés bemásolása; a deposit formátuma.
- Külső lépések: a Biblialex domain; a BiblIndex-levél (patrisztikus igehely-index, a visszhang-réteghez: küldés vagy elvetve; a tervezetben még a régi „Logosz-lexikon” név áll); a KJV-licenc kérdése a CrossWire-nek (csak a fizetős megjelenítés előtt).
- Az F134 telefonos próbája. A BDB harmadik tanúja (N212: a mintán 70%-ban a mi táblánk téved): a tábla javítása feladat legyen, vagy elvetve.
- Archiválható-e: levelek-uj-cimzettek; betu-szin-elonezet (6 merge-eletlen commit: a betűválasztó előnézete).

*Frissítés: amit a szerkesztő irányként kimond, azt az integrátor még ugyanabban a válaszában beírja ide, és megmutatja. Új irányt magától nem ír bele, csak az állapotot (lezárult szál, megválaszolt kérdés). Új sor csak egy másik törlésével; legfeljebb 40 sor.*
