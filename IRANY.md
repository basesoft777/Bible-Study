# IRÁNY — kelt: 2026-11-23 · gazdája: a szerkesztő · legfeljebb 40 sor

**Cél:** a Biblialex motívumlexikon. Most: hibátlan olvasó, és kész új generátor a TEREMT-001-próbához.

## Futó szálak (legfeljebb 2)
1. **Olvasó-javítás (#231, PR #810).** Az 58 tétel (a 60-ból; kívül: 23. fordítás, 59. motívumlap). Kész: „Mérce: 58/58 zöld” a PR-ban, utána egy nézés az ágas előnézeten; merge után tükör-újraindítás és DB-másolat ellenőrzése (integrátor).
2. **Új generátor (F218a, PR #809).** Kész: a HAMART-referencia és a 8.2/1 számlálók zöldek; a HAMART-001 és az ISTENTISZT-001 új generátoros lapja a szerkesztő átnézésén és jóváhagyásán (2026-11-23: „hamart az istentisztelettel - átnézésre / jóváhagyás után teremt”); utána F218.13 a main-en.
- **Következő szálak**, ebben a sorrendben:
  - rövid adat-PR az N-F231a-ra (hamis LXX-pár: „πρωὶ” → G5459, 88 hely);
  - **a JOHD-kézirat végső köre**, amint a validáció számai megvannak (decemberi beküldés; elsőbbsége van a kapu előtt);
  - a 15 perces kapu kettévágása (integrátor; benne a bukó test_11 és a BEHIND-kör);
  - TEREMT-001 (tehóm), nulláról, az új generátorral és az új cikkmenettel, a két lap jóváhagyása után (saját brief).
- **Utána** (a 2026-11-11-i ütemezés): a motívumok ráillesztése az olvasóra, ez az „alap” olvasó.

## Most NEM csináljuk
- Új lexikonlap: csak a TEREMT-001 (tehóm), nulláról (2026-11-12: „ez a következő a többi fagyasztva”). Befagyasztva: KIRALY, ALVIL, MENNY, ANTROP, HODIT, TEREMT-002.
- Új olvasó-felmérés, amíg a #231 nincs lezárva.
- Új motívumcikk a homonima-jelzés előtt; kivétel a TEREMT-001 (DT914, 2026-11-22: „a teremt re nem terjedhet ki az az új generátor próbája”).
- A BDB-lektor többi javaslata a lapon (N228): csak egy jövőbeli kiadásban (DT914, 2026-11-22: „a többi feljegyzés marad”).
- 218b, 218c, B0 (#236–#238): az F218.13 előtt nem indul.
- F235 2. rész (N230–N233: indexek, natív futás): a szerkesztő szaváig nem indul (2026-11-22, a régi orkesztrátor átadása szerint).
- Fizetős fordítás (N177 görög rövid jelentések; a Thayer következő adagja): a szerkesztő döntéséig nem („Rád vár”).

## Így dolgozunk
- Egyszerre legfeljebb 2 szál; egy szál = egy ág + egy PR, a session cserélhető.
- A hibának három kimenete van: javítva / elvetve egy sor indokkal / rád vár; hamis tartalmat mutató hiba nem vethető el.
- Csak olvasó-kód: gyors sáv. Adat, generátor, próza: nehéz kör (DT919).
- Technikai kérdésben a session dönt; tartalmi kérdés az integrátorhoz (DT920).
- Az állapot csak leírva él: ez a lap, a PR-ok első sora (Mérce · Állapot · Következő · Akadály), a DONTESEK. Az integrátor naponta cserél; az utód briefje: „olvasd el az IRANY.md-t és a nyitott PR-ok első sorát”.

## Rád vár
- **JOHD-validátor megkeresése** (pénz, külső közlés; 568 tétel, ~5–6 óra, bruttó 60–100 ezer Ft): Susánszki Judit, tartalék Grüll Tiborné. Erre vár a #762, a #763 és a decemberi beküldés.
- STEPBible: a modul 1.1-ből vagy 1.2-ből; a levél Davidnek (a KJV-eltéréslista és levéltervezet egy kártyán).
- Fordítás (pénz), igen vagy elvetve: #24 görög rövid jelentések; #23 Thayer (a következő adag kb. 10 USD).
- Külső lépések: Biblialex domain; BiblIndex-levél (a tervezetben még „Logosz”); SzPA-levél; KJV-licenc (csak fizetős megjelenítés előtt).
- F134 telefonos próba. BDB harmadik tanú (N212): a tábla javítása feladat legyen, vagy elvetve.
- Archiválható-e: levelek-uj-cimzettek; betu-szin-elonezet (6 merge-eletlen commit).

*Frissítés: amit a szerkesztő irányként kimond, azt az integrátor még ugyanabban a válaszában beírja ide, és megmutatja; az állapotot kötegelve frissíti (szálváltáskor vagy naponta). Részlet a PR-ba és a jelentésbe. Legfeljebb 40 sor.*
