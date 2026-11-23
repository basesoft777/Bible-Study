# IRÁNY — kelt: 2026-11-23 · gazdája: a szerkesztő · legfeljebb 40 sor

**Cél:** a Biblialex motívumlexikon. Most: hibátlan olvasó, és kész új lapgenerátor a TEREMT-001-próbához.

## Futó szálak (legfeljebb 2)
1. **Olvasó-javítás:** a felmért olvasóhibák javítása (#231, PR #810). A #810 egyszer bemegy (kódszintű független olvasás és a nézésed után), de nem „kész”: a belső nevek a felületen maradtak, mert a mérce a mai állapotot rögzítette, hibáival együtt, nem kapu. Ezért nincs több példányjavító kör (2026-11-23: „ezt a módszert nem fogadom el”); helyette: alak-kapu, amely minden oldaltípust bejár, és minden belső alakra bukik (a kimenete a hátralék); a forrássor a névtáblából; egy névtábla; blokk-jegyzék, hogy a vers- és a szónézet blokkjai kódírás nélkül be- és kivehetők legyenek (2026-11-23: „modulárisan … be és ki tudja venni blokkokat”).
2. **TEREMT-001 (tehóm) cikk:** nulláról, az új lapgenerátorral (az lezárult: F218a, #809, 2026-11-23); a te szavad 2026-11-23: „a TEREMT-001 legyen az első”. Lépéshatárokkal: adat-előkészítés → határ és érvvázlat → próza egy menetben → javítókör; a próza a táblákból készül. Kiadni az átállás (218c) után lehet, mert az új generátor addig nem ad ki lapot.
- **Következő szálak**, ebben a sorrendben:
  - kis adatjavítás: a görög LXX-párok közt 88 helyen hamis „hajnalcsillag” a „reggel” szónál (N-F231a), nyelvtani szó (μου) az LXX-megfelelők közt, csonka fejléc és dupla könyvnév a fordított BDB-szövegben (a brief elkészül, a futás a TEREMT-001 mellett, amint hely szabadul);
  - a rendszer karcsúsítása: egy rövid tanulságfájl, amelyet minden session induláskor olvas a teljes memória helyett; a lezárt tételek és memóriafájlok archiválása (nem törlés); a CLAUDE.md rövidítése a te jóváhagyásoddal; mérce: a CLAUDE.md sorszáma és a session induló kontextusa előtte és utána (2026-11-23: „#821 után, 218c előtt”);
  - az átállás (218c): a régi generátor archívumba, az ISTENTISZT-001 2. kiadása (előtte a 34 hiányzó fordítás), és ezzel válik kiadhatóvá a TEREMT-001; előtte az olvasóban a forrássor a névtáblából, és egy névtábla;
  - a 15 perces push előtti ellenőrzés kettévágása: munka közben gyors próba, a teljes csak a végén (integrátor).
- **Utána** (a 2026-11-11-i ütemezés): a motívumok megjelenítése az olvasóban, ez az „alap” olvasó.
- **Az ISTENTISZT-001 2. kiadása** az átállás (218c) első eredménye; a mostani jóváhagyásod érvényes marad, mert az átállás csak gépi részt változtathat (DT933, 2026-11-23). Ezzel a cikk a lexikonban kész; az olvasó a lapot nem olvassa, az adatbázisból maga számol, ezért ott előbb csak adatként frissül, cikként az olvasó átkötése (#236) és a motívumok olvasóba vitele után látszik. Addig minden lapjavítás az olvasóba is kell (mint a 4Móz 16:30 héber betűje).

## Most NEM csináljuk
- Új lexikonlap: csak a TEREMT-001 (tehóm), nulláról (2026-11-12: „ez a következő a többi fagyasztva”). Befagyasztva: KIRALY, ALVIL, MENNY, ANTROP, HODIT, TEREMT-002.
- Új olvasó-felmérés, amíg az olvasó-javítás tart.
- Új motívumcikk, amíg nincs homonima-jelzés a jelöltlistán; kivétel a TEREMT-001 (2026-11-22: „a teremt re nem terjedhet ki az az új generátor próbája”; DT914).
- A BDB-lektor többi javaslata a lapon: csak egy jövőbeli kiadásban (2026-11-22: „a többi feljegyzés marad”; N228).
- Az új generátor folytatásai a záró lépés (F218.13) előtt nem indulnak: az olvasó átkötése az új generátor számításaira (#236), a szókártyák motívum nélküli belépési pontjai (#237, B0), és az átállás, amely után a régi generátor archívumba kerül (218c).
- Az olvasó maradék lassúsága (gépindítás utáni első megnyitás 1–3 s, 23 lassú lekérdezés indexszel; F235 2. rész, N230–N233): a te szavadig nem indul.
- Fizetős fordítás: a te döntésedig nem (lent, „Rád vár”).

## Így dolgozunk
- Egyszerre legfeljebb 2 szál; egy szál = egy ág + egy PR, a session cserélhető: kb. 150–200 ezer token kontextusnál csere (teljes átadó jegyzettel) vagy tömörítés, a végrehajtó subagenteknél is; mert minden lépés a teljes kontextust újraolvassa (a HAMART-mérés, 2026-11-23). Cikkírásnál a plafon a lépéshatáron érvényes, prózaírás közben nem: az U3 a prózát egy menetben végigírja, és csak utána cserél; minden lépéshatáron átadó jegyzet, minden döntés indoklással azonnal fájlba („egy kéz” = egy modell, amely az egész prózát olvassa, nem egy session; 2026-11-23).
- A hibának három kimenete van: javítva / elvetve egy sor indokkal / rád vár; hamis tartalmat mutató hiba nem vethető el.
- Csak olvasó-kód: gyors sáv. Adat, generátor, próza: nehéz kör, független ellenőrrel (DT919).
- Új szabály helyett gépi kapu (teszt, hook); az elvárt kimenetet ember írja vagy hagyja jóvá (kézzel írt minta, nem a gép előző kimenete); egy feladat = egy kis PR, nem 50 fájl egy menetben (2026-11-23).
- Technikai kérdésben a session dönt; tartalmi kérdés az integrátorhoz (DT920).
- Az állapot csak leírva él: ez a lap, a PR-ok első sora (Mérce · Állapot · Következő · Akadály), a DONTESEK. Az integrátor kb. 300 ezer token kontextusnál vagy naponta cserél, amelyik előbb jön (a fix induló teher kb. 140 ezer, a 150–200 ezres plafon a munkasessionöké), és karcsún indul: csak ez a lap és egy rövid átadó jegyzet (állapot, a nap döntései, ami rád vár); memóriát és régi átadót csak akkor olvas, ha egy kérdés arról szól (2026-11-23).

## Rád vár
- **A JOHD-cikk validátorának megkeresése** (pénz, külső közlés; 568 tétel, ~5–6 óra, bruttó 60–100 ezer Ft): Susánszki Judit, tartalék Grüll Tiborné. Erre vár a két JOHD-PR (#762, #763), a kézirat végső köre és a decemberi beküldés (2026-11-23: „a JOHD rám vár”).
- STEPBible-modul: az 1.1-es vagy az 1.2-es adatverzióból készüljön; a levél Davidnek (a KJV-eltéréslista és a levéltervezet egy kártyán) (2026-11-23: „stepbible feladatok rám vár”).
- Fizetős fordítás, igen vagy elvetve: a görög szavak rövid magyar jelentése (~5 300 szó; N177, #24); a Thayer-szótár magyarja (354 / 5 426 kész; a következő adag kb. 10 USD; #23).
- Külső lépések: a Biblialex domain; a BiblIndex-levél (patrisztikus igehely-index; a tervezetben még „Logosz”); az SzPA-levél; a KJV-licenc kérdése (csak fizetős megjelenítés előtt).
- Az olvasó telefonos próbája (az alapnézet kis képernyőn; F134). A BDB-szótár harmadik tanúja: a mintán 70%-ban a mi táblánk téved; a javítás feladat legyen, vagy elvetve (N212).
- Archiválható-e két tétlen session: levelek-uj-cimzettek; betu-szin-elonezet (6 merge-eletlen commit).
*Frissítés: amit a szerkesztő irányként kimond, azt az integrátor ugyanabban a válaszában beírja ide; az állapotot kötegelve frissíti. Minden sor egy olvasói mondattal mondja meg, miről szól; azonosító csak zárójelben. Legfeljebb 40 sor.*
