# IRÁNY — kelt: 2026-11-23 · gazdája: a szerkesztő · legfeljebb 40 sor

**Cél:** a Biblialex motívumlexikon. Most elsődleges az új lapgenerátor befejezése (az átállás, 218c), mellette a TEREMT-001-próba; az olvasót újraépítjük (2026-11-23: „elsődleges feladat a generátor befejezése”).

## Futó szálak (legfeljebb 2)
1. **Olvasó:** a felmért hibák javítása (#231, PR #810) alapvonalként megy be, a main-összevetés és a nézésed után. Utána nincs több javítókör a régi olvasón (2026-11-23: a javítás végtelen ciklus volt, „mint a generátor foltozása”). Helyette újraépítés: blokk-jegyzék adatként, a te jóváhagyásoddal (nézet × nyelv HU/EN × mélység három fokozatban × jogosultság, amely a mélység felső határa); az olvasó a jegyzékből renderel, a kapuk (alak-kapu, bekötés-összevetés) mérik, mindhárom tengelyen. Most a tervezőtábla készül: csak terv.
2. **TEREMT-001 (tehóm) cikk:** nulláról, az új lapgenerátorral (F218a, #809); a te szavad: „a TEREMT-001 legyen az első”. Lépéshatárokkal (adat → határ és érvvázlat → próza egy menetben → javítókör); most az U5, a nézésed. Kiadni csak az átállás (218c) után lehet.
- **Következő szálak**, ebben a sorrendben (2026-11-23):
  - az átállás (218c), a #810 merge-e után azonnal, az olvasó szálhelyén: a 3/b-ben talált generátorhibák javítása, a régi generátor archívumba, az ISTENTISZT-001 2. kiadása (előtte a 34 hiányzó fordítás), és ezzel válik kiadhatóvá a TEREMT-001; előtte az olvasóban a forrássor a névtáblából, egy névtábla;
  - kis adatjavítás (#821): 88 hamis „hajnalcsillag” a görög LXX-párokban (N247), nyelvtani szó (μου) az LXX-megfelelők közt, csonka fejléc és dupla könyvnév a fordított BDB-szövegben;
  - a rendszer karcsúsítása: rövid tanulságfájl a teljes memória helyett; a lezárt tételek és memóriafájlok archiválása (nem törlés); a CLAUDE.md rövidítése a te jóváhagyásoddal (a tervre „mehet”, a diff merge előtt eléd); mérce: a CLAUDE.md sorszáma és az induló kontextus előtte és utána;
  - a 15 perces push előtti ellenőrzés kettévágása: munka közben gyors próba, a teljes csak a végén.
- **Utána** (2026-11-11): a motívumok megjelenítése az olvasóban, ez az „alap” olvasó.
- **Az ISTENTISZT-001 2. kiadása** után a cikk a lexikonban kész (a jóváhagyásod érvényes, az átállás csak gépi részt változtat; DT933); az olvasóban előbb csak adatként frissül, cikként az átkötés (#236) után látszik, addig minden lapjavítás az olvasóba is kell.

## Most NEM csináljuk
- Új lexikonlap: csak a TEREMT-001 (2026-11-12: „ez a következő a többi fagyasztva”). Befagyasztva: KIRALY, ALVIL, MENNY, ANTROP, HODIT, TEREMT-002.
- Új olvasó-felmérés és javítókör a régi olvasón.
- Új motívumcikk, amíg nincs homonima-jelzés a jelöltlistán; kivétel a TEREMT-001 (DT914).
- A BDB-lektor többi javaslata a lapon: csak egy jövőbeli kiadásban (N228).
- Az olvasó átkötése az új generátor számításaira (#236) és a szókártyák motívum nélküli belépési pontjai (#237): nincsenek a sorban.
- Az olvasó maradék lassúsága (első megnyitás 1–3 s, 23 lassú lekérdezés; F235 2. rész, N230–N233): a te szavadig nem indul.
- Fizetős fordítás: a te döntésedig nem (lent).

## Így dolgozunk
- Egyszerre legfeljebb 2 szál; egy szál = egy ág + egy PR, a session cserélhető (150–200 ezer token kontextusnál csere átadó jegyzettel; cikkírásnál a lépéshatáron, a prózát egy modell egy menetben írja; minden döntés indoklással azonnal fájlba).
- A hibának három kimenete van: javítva / elvetve egy sor indokkal / rád vár; hamis tartalmat mutató hiba nem vethető el.
- Csak olvasó-kód: gyors sáv. Adat, generátor, próza: nehéz kör, független ellenőrrel (DT919).
- Új szabály helyett gépi kapu; az elvárt kimenetet ember írja vagy hagyja jóvá; egy feladat = egy kis PR.
- Technikai kérdésben a session dönt; tartalmi kérdés az integrátorhoz, a döntés a session döntésfájljába (DT920).
- Az állapot csak leírva él: ez a lap, a PR-ok első sora (Mérce · Állapot · Következő · Akadály), a DONTESEK. Az integrátor kb. 300 ezer tokennél vagy naponta cserél, és karcsún indul: ez a lap és egy rövid átadó jegyzet.

## Rád vár
- **A JOHD-cikk validátorának megkeresése** (pénz, külső közlés; 568 tétel, ~5–6 óra, bruttó 60–100 ezer Ft): Susánszki Judit, tartalék Grüll Tiborné. Erre vár a két JOHD-PR (#762, #763), a kézirat végső köre és a decemberi beküldés.
- STEPBible-modul: az 1.1-es vagy az 1.2-es adatverzióból; a levél Davidnek (a KJV-eltéréslista és a levéltervezet egy kártyán).
- Fizetős fordítás, igen vagy elvetve: a görög szavak rövid magyar jelentése (~5 300 szó; N177, #24); a Thayer-szótár magyarja (354 / 5 426 kész; a következő adag kb. 10 USD; #23).
- Külső lépések: a Biblialex domain; a BiblIndex-levél (a tervezetben még „Logosz”); az SzPA-levél; a KJV-licenc (csak fizetős megjelenítés előtt).
- Az olvasó telefonos próbája (F134). A BDB-szótár harmadik tanúja: a mintán 70%-ban a mi táblánk téved; feladat legyen, vagy elvetve (N212).
- Archiválható-e két tétlen session: levelek-uj-cimzettek; betu-szin-elonezet (6 merge-eletlen commit).
*Frissítés: amit a szerkesztő irányként kimond, azt az integrátor ugyanabban a válaszában beírja ide; az állapotot kötegelve frissíti. Minden sor egy olvasói mondattal mondja meg, miről szól; azonosító csak zárójelben. Legfeljebb 40 sor.*
