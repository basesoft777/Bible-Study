# IRÁNY — kelt: 2026-11-24 · gazdája: a szerkesztő · legfeljebb 40 sor

**Cél:** a Biblialex motívumlexikon. Most elsődleges az új lapgenerátor befejezése (az átállás, 218c), mellette a TEREMT-001-próba; az olvasót újraépítjük (2026-11-23: „elsődleges feladat a generátor befejezése”).

## Futó szálak (legfeljebb 2)
1. **Átállás az új lapgenerátorra (218c, #241):** indult 2026-11-23. **Kiadási minimum** (a te szavad, 2026-11-24: „elfogadom”): minden látható hiba javul a három lapon (ISTENTISZT-001, TEREMT-001, HAMART-001), a generátorig; az olvasóban csak az, ami a három lapon látszik, vagy halasztással drágul (2026-11-24); ha egy hibafajta már előfordult, a kapuja a javítással együtt készül. **Visszaesés-kapu** (a te szavad: „nem akarok visszaesést a régi laphoz képest”): a régi laphoz mért bármely romlás megállítja a lapot, átengedni csak indokolt elfogadási sorral lehet (#863, #873). Lépések: a belső szavak és a sablonszövegek javítása a három lapon (F241.5b; két rész bent, most a hamis LSJ-mondatok, a visszaesések, a szakszavak és a sablonsorok), független ellenőrzés, az ISTENTISZT-001 2. kiadása a nézéseddel, a TEREMT-001 generátorhibái, a HAMART-001 javítása és új kiadása a nézéseddel, a TEREMT-001 kiadása. Utána, nem hiba: a teljes kapuforma, a régi generátor archiválása, a lapon meg nem jelenő sablonsorok.
2. **Kis adatjavítás (#821):** a főrész bent (2026-11-24): 88 hamis „hajnalcsillag” a görög LXX-párokban (N247), nyelvtani szó (μου) az LXX-megfelelők közt, csonka fejléc és dupla könyvnév a fordított BDB-szövegben. Hátra: három olvasó-teszt mérése friss adatbázison, a BDB könyvhivatkozásai (L7) és a kiesett arab/etióp szavak (L8).
3. **A push előtti ellenőrzés kettévágása** (harmadik szálként, a te szavadra, 2026-11-24: „Igen, induljon”): munka közben gyors próba, a teljes csak a végén; a gépi sor és a gyors mód bent (#861, #866, #868, #870, #871), hátra a lapgen-tesztek közös gyorsítótára (kb. 36 → 17 perc).
- **Szünetel: a TEREMT-001 (tehóm) cikk** (a te szavad: „a TEREMT-001 legyen az első”): a javítókör a 29 döntéseddel elkészült, a PR-ba kerülése folyamatban (2026-11-24); kiadni az átállás után lehet.
- **Következő szálak**, ebben a sorrendben (2026-11-23):
  - a rendszer karcsúsítása: rövid tanulságfájl a teljes memória helyett; a lezárt tételek és memóriafájlok archiválása (nem törlés); a CLAUDE.md rövidítése. A brief kész (#243), a CLAUDE.md-tervre a „Mehet így”-ed megvan (2026-11-24); a kettévágás után indul, a diff merge előtt eléd kerül; mérce: a CLAUDE.md 192 sor → legfeljebb 110, az induló kontextus kb. 91 600 → 86 000 token.
- **Utána** (2026-11-11 és 2026-11-23): az olvasó újraépítése a generátor után: blokk-jegyzék adatként, a te jóváhagyásoddal (nézet × nyelv HU/EN × mélység három fokozatban × jogosultság; a tervezőtábla kész, az elrendezésed vár); egy névtábla, a forrássor a névtáblából; az olvasó a jegyzékből renderel, a kapuk mérik. Benne a motívumok megjelenítése: ez az „alap” olvasó.
- **Az ISTENTISZT-001 2. kiadása** után a cikk a lexikonban kész (a kézi prózára és adatra adott jóváhagyásod érvényes, DT933; az új generátoros lapra 2026-11-23-án adott jóváhagyás olvasói átolvasás nélkül született, ezért feltételes: az F241.7 és az F241.10 nézése rendezi); az olvasóban előbb csak adatként frissül, cikként az átkötés (#236) után látszik, addig minden lapjavítás az olvasóba is kell.

## Most NEM csináljuk
- Új lexikonlap: csak a TEREMT-001 (2026-11-12: „ez a következő a többi fagyasztva”). Befagyasztva: KIRALY, ALVIL, MENNY, ANTROP, HODIT, TEREMT-002.
- Új olvasó-felmérés és javítókör a régi olvasón. Az olvasó-szerverre csak nagyon indokolt esetben költünk (a te szavad, 2026-11-24: „olvasai serverre ne költsünk csak ha nagyon indokolt”): a kiadási minimum olvasói határa a 218c sorában áll; az LSJ-kártyák javítótáblája (PR-A, PR-B) az olvasó újraépítésére vár.
- Új motívumcikk, amíg nincs homonima-jelzés a jelöltlistán; kivétel a TEREMT-001 (DT914).
- A BDB-lektor többi javaslata a lapon: csak egy jövőbeli kiadásban (N228).
- Az olvasó átkötése az új generátor számításaira (#236) és a szókártyák motívum nélküli belépési pontjai (#237): nincsenek a sorban.
- Az olvasó maradék lassúsága (első megnyitás 1–3 s, 23 lassú lekérdezés; F235 2. rész, N230–N233): a te szavadig nem indul.
- Fizetős fordítás: a te döntésedig nem (lent).

## Így dolgozunk
- Egyszerre legfeljebb 2 szál; egy szál = egy ág + egy PR, a session cserélhető (150–200 ezer token kontextusnál csere átadó jegyzettel; cikkírásnál a lépéshatáron, a prózát egy modell egy menetben írja; minden döntés indoklással azonnal fájlba).
- A hibának három kimenete van: javítva / elvetve egy sor indokkal / rád vár; hamis tartalmat mutató hiba nem vethető el.
- Csak olvasó-kód: gyors sáv. Adat, generátor, próza: nehéz kör, független ellenőrrel (DT919).
- Új szabály helyett gépi kapu; az elvárt kimenetet ember írja vagy hagyja jóvá. Egy lépés = egy kis PR, és kész lépés rögtön a main-be megy; a menet közben talált hiba külön tétel, nem bővíti a futó lépést, kivéve a pár soros javítást (a te szavad, 2026-11-24: „Igen, így”).
- Technikai kérdésben a session dönt; tartalmi kérdés az integrátorhoz, a döntés a session döntésfájljába (DT920).
- A te mondatodat a sessionök szó szerint, idézőjelben kapják: a célhűség-próbán így a terv 13% helyett 77%-ban a mondatodat méri, de nem mindig, ezért a válasz az eredményt mérő kapu és a gyors visszajelzés, nem új nyilvántartás (2026-11-24, `naplok/CELHUSEG_PROBA_2026-11-24.md`).
- Az állapot csak leírva él: ez a lap, a PR-ok első sora (Mérce · Állapot · Következő · Akadály), a DONTESEK. Az integrátor kb. 300 ezer tokennél vagy naponta cserél, és karcsún indul: ez a lap és egy rövid átadó jegyzet.

## Rád vár
- **A JOHD-cikk validátorának megkeresése** (pénz, külső közlés; 568 tétel, ~5–6 óra, bruttó 60–100 ezer Ft): Susánszki Judit, tartalék Grüll Tiborné. Erre vár a két JOHD-PR (#762, #763), a kézirat végső köre és a decemberi beküldés.
- STEPBible-modul: az 1.1-es vagy az 1.2-es adatverzióból; a levél Davidnek (a KJV-eltéréslista és a levéltervezet egy kártyán).
- Fizetős fordítás, igen vagy elvetve: a görög szavak rövid magyar jelentése (~5 300 szó; N177, #24); a Thayer-szótár magyarja (354 / 5 426 kész; a következő adag kb. 10 USD; #23).
- Külső lépések: a Biblialex domain, utána a nyílt adatmag és a CITATION.cff átnevezése (2026-11-24: „Várjon a domainig”); a BiblIndex-levél (a tervezetben még „Logosz”); az SzPA-levél; a KJV-licenc (csak fizetős megjelenítés előtt).
- Az olvasó telefonos próbája (F134).
*Frissítés: amit a szerkesztő irányként kimond, azt az integrátor ugyanabban a válaszában beírja ide; az állapotot kötegelve frissíti. Minden sor egy olvasói mondattal mondja meg, miről szól; azonosító csak zárójelben. Legfeljebb 40 sor.*
