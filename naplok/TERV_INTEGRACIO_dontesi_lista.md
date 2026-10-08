# TERV-INTEGRÁCIÓ — döntési lista (TI.2)

*Ág `claude/terv-integracio` · 2026-10-08 · forrás: `naplok/TERV_INTEGRACIO_leltar.md` (a „leltár” oszlop az R-sorszám). Egy körben megválaszolható: soronként egy betű (pl. `1a 2a 3b …`), eltérésnél egy mondat. A válaszok a 3. lépésben kerülnek a `DONTESEK.md`-be (helyőrzővel; mivel a menetnek nincs feladatszáma, a `DT-F<nn>` helyőrző alakját a 3. lépés elején egyeztetem), a `FELADATOK`-hoz tartozó brief-fejlécekbe és a tervekbe; addig semmi nem íródik át.*

**Sorrend-feltétel.** A 2., 5. és 8. tétel a #64 PR #247-re (DT-F64a/b, mérési jelentés) épül; a 3. lépés a #247 merge-e után indul.

## A) Az aranyminta és a szótári rész (a felhasználó (a), (e), (f) pontja)

**1. ISTENTISZT-001 rekonstrukció a szerepmátrix szerint** *(leltár R1)*
- Kérdés: hogyan épüljön újra az aranyminta, hogy a #23 M1, a #10 és a #11 mércéje a szerepmátrixot kövesse?
- a) **szerepmátrix-váz** új feladatként (folyamat, Sonnet, `munka: adat`): a generátor a `_TUDOMANYOS` 2. szakaszát szerepenként, a `szotar_szerepek.tsv` sorrendjében rendereli, a nem adatosított szerep explicit üres blokk; adatosítás nélkül; a #23 M1 előtt fut, és a #23 `fugg`-ja lesz
- b) teljes rekonstrukció egy menetben (váz + a hiányzó szerepek adatosítása), a #9 helyett
- c) nincs rekonstrukció; a #23 M1 a mai ISTENTISZT-001-et méri, a mátrixot a #9 hozza utólag
- **Javaslat: a)** — a váz adat nélkül megtöri a #23 M1 → aranyminta → #9-adat → #9 `fugg` #23 kört, és az üres blokk a „memória vs. lekérdezés” szabály renderbeli alakja (ADATVAGYON 18.5).
- Érinti: új FELADATOK-sor (`/befogad`), `eszkozok/lexikon_general.py`, a #23 brief (M1 előfeltétel, `fugg`), a #9 és #10 brief, ADATVAGYON 18.5, MUNKATERV 4a.

**2. A TEREMT-002 szótári részének újramérése** *(R2)*
- Kérdés: hol mérjük a TEREMT-002 szótári részét a rekonstruált aranymintához?
- a) az 1. tétel váz-feladatának második mintájaként (próbarender a `generalt_proba/` alá, mérési jelentéssel)
- b) a #12b (TEREMT-002 3. lépés) része, a lexikonoldal elkészültekor
- c) a #23 M1 része
- **Javaslat: a)** — a #23 M1 így egy örökölt és egy natív mintán látja a vázat; a TEREMT-002-nek lexikonoldala nincs, a próbarender elég.
- Érinti: az 1. tétel briefje, a #12 csonk `kovetkezo`-ja.

**3. Befagyasztás a #11 előtt** *(R3)*
- Kérdés: kerülhet-e a régi motívumokhoz tartalom a régi szerkezet szerint a #11 1. lépcsője előtt?
- a) a forrásréteg (`tematikus_lezart/`: #55 forrásjavítás, #70 ISTENTISZT-001 2/b) és az éles `lexikon/` újragenerálása (#36) fagy a #11 1. lépcsőjéig; az adatréteg (#63, #65: `jeloltek`/`elofordulasok`) mehet; a #13 a #11 után
- b) minden fagy, az adatréteg is (#63, #65 is a #11 után)
- c) nincs befagyasztás
- **Javaslat: a)** — a DT28 szerint az adat a migráción változatlanul átmegy, a régi prózába írt tartalmat viszont a #11 szétválasztásakor újra kellene osztani; a #70 Strong-szerinti alszakaszai a mátrix-vázzal ütköznének.
- Érinti: #36, #55, #70, #13 fejléce (`fugg` vagy `kovetkezo`), FELADATOK döntésnapló (új D-sor), MUNKAMENET.

**4. A #9 szűkítése** *(R4)*
- Kérdés: a #9 a motívumokban szereplő szócikkekre szűküljön-e, a #38/#7 megvárása nélkül?
- a) igen: a #9 hatóköre a 8 motívum Strongjai (a #28 Opus-fordítással lefedte, D42), `nem_fugg: [7, 38]`; a szerepmátrix-váz blokkjait tölti
- b) igen, de a #38 lágy függése marad (a fordítás-gyorsítótár frissülhet közben)
- c) nem, a #9 a #38 teljes lefutását várja
- **Javaslat: a)** — a #38 a teljes BDB-t fordítja (a 7. adag következik), a lexikon szócikkei már készen vannak; a D50 szerint a lexikonba úgyis csak a motívumhoz illő jelentés kerül.
- Érinti: F09 fejléc (`nem_fugg`, `olvas`, `ad`), F05 2. menet hivatkozása, MUNKATERV 4a, ADATVAGYON 16.

**5. L2/L7 a lexikonoldal-sablon kapujába és a #10 mércéjébe** *(R7)*
- Kérdés: mikor és hol vezessük át a DT-F64a (2) L2/L7-jét?
- a) most, a 3. lépésben (a #247 merge-e után): a `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` kapuja L1–L7; a #10 mércéje L1–L7 + a DT2 két rés-szabálya + a szerepmátrix-váz; a #23 M1 előfeltétele („L1–L5, #10”) ugyanerre
- b) külön feladatként
- c) a #10 csonk-kitöltésekor
- **Javaslat: a)** — a DT-F64a „külön tételt” kér, és a #23 M1 előfeltétele ma elavult mércére hivatkozik; a sablon-átszámozás kis szerkesztés.
- Érinti: `sablonok/6_PaRDeS_lexikon_oldal_sablon.md`, F10 csonk, F23 brief M1, DT2 sor.

## B) Fázis- és függés-szabály (a felhasználó (d) pontja)

**6. A #62 fázisa** *(R5)*
- Kérdés: a `folyamat` fázisú #62 ne blokkolja észrevétlenül az 1. fázist (#54, #55, #63, #65)?
- a) a #62 (és a ráépülő #61) `fazis: 1`
- b) a /kovetkezo szabálya: az 1. fázisú feladatot blokkoló folyamat-feladat 1. fázisú jelölt (`feladatok.py jeloltek` módosítás, külön ág, D6)
- c) marad
- **Javaslat: a)** — egy fejléc-mező, eszközmódosítás nélkül; a #68 (ugyanez az eset) lezárult, tárgytalan.
- Érinti: F62, F61 fejléc; MUNKATERV 4a.

**7. A #76 (#25a) és a D1 fázisszabály** *(R6)*
- Kérdés: indulhat-e a #76 az 1. fázis lezárása előtt (a #22 teljes Bibliája és a #38 nélkül)?
- a) igen: a D1 kiegészítése — a #76 az SQLITE_EPIT után indul, a kész Károli–Strong könyvekkel; az ADATVAGYON 0.2/5 „1. fázis végig”-je a kész könyvekre értendő
- b) igen, de csak a #22 ÓSZ-ének lezárása után
- c) nem, a #76 a teljes 1. fázist várja
- **Javaslat: a)** — a DT-M1 és az ADATVAGYON 21 (a 2. lépcső „könyvenként, nem kell a teljes”) ezt mondja; a c) a D46 feloldását (#7) évekre tolja.
- Érinti: FELADATOK döntésnapló (D1-kiegészítés), Alapelv, F76 fejléc, ADATVAGYON 0.2/21, MUNKATERV 5.

**8. Elavult `kovetkezo` mezők és más briefek fejléce** *(R8, a felhasználó (g) pontja; G1–G5, G9)*
- Kérdés: frissítheti-e a TI 3. lépése más feladatok brief-fejlécét (a #22, #23, #38, #64 elavult `kovetkezo`-ja; a #9, #10, #11, #23, #76 `olvas`-a; a #12 `kovetkezo`-ja)?
- a) igen, egyszeri kivételként, ebben a menetben (a CLAUDE.md „minden menet a saját briefje fejlécét frissíti” szabálya alól; a zárójelentés felsorolja)
- b) nem; a feladatok saját következő menete frissít, a TI csak listát ad
- c) csak az `olvas`-sorok (a döntésekből következők), a `kovetkezo`-k a saját menetben
- **Javaslat: a)** — a felhasználó „véglegesen, egy menetben” kérte; a b) ugyanazt a rést hagyja nyitva, amit ez a menet zár.
- Érinti: F09, F10, F11, F12-csonk (`TEREMT002_KUTATAS_BRIEF.md`), F22, F23, F38, F64, F76 fejléc.

## C) Nyitott MUNKATERV-döntések

**9. DT-M4: 13. szerep (Károli-megfelelők + SZPA) és 14. szerep (rejtett/hamis párhuzam)** *(R9)*
- Kérdés: bővüljön-e a SEMA 2.13 szerepmátrix?
- a) felvétel `javaslat` állapottal, amíg a #22 nem teljes (a váz üres/részleges blokként mutatja)
- b) felvétel csak a #22 teljes lefutása után
- c) nem
- **Javaslat: a)** — a 13. szerep a #64 mérése szerint az aranymintából is hiányzik; a váz így eleve 13–14 sorral épül.
- Érinti: `adat/szotar_szerepek.tsv`, SEMA 2.13, ADATVAGYON 18.5, a váz-feladat, #76.

**10. DT-M5: külső `bible-mcp`** *(R10)*
- Kérdés: használjuk-e a külső connectort?
- a) a DT-M5 lezárása a DT32-re hivatkozva: chatben ellenőrzésre használható, a kimenete adatba, briefbe, tanulmányba nem kerül; bekötés (`.mcp.json`) nincs
- b) elvetés egyelőre, újratárgyalás a saját MCP után (a DONTESEK eredeti 1. opciója)
- c) használat most, a saját MCP mellett
- **Javaslat: a)** — a DT32 a kérdés érdemét már eldöntötte; a nyitott DT-M5 csak duplikátum.
- Érinti: DONTESEK DT-M5, MUNKATERV 2., ADATVAGYON 0.4/15.

**11. DT-M6: a saját kimenet licence és a kiadás módja** *(R11)*
- Kérdés: milyen módban és milyen licenccel menjen az első olvasói kiadás?
- a) az első kiadás nem kereskedelmi; minden blokk dataset-kulccsal, forrás- és licencjelöléssel; szűrés a `kereskedelmi` oszlop szerint; a saját réteg licence külön tétel (javaslat: CC BY 4.0 az adatra); jogász a kereskedelmi döntéskor
- b) a kiadás a saját réteg licencének eldöntéséig vár
- c) most dönteni a saját réteg licencéről is (CC BY 4.0 az adatra, a prózára külön)
- **Javaslat: a)** — a #76 így a hosting-döntésig haladhat; a saját licenc a publikálás előtt dől el (17. tétellel együtt).
- Érinti: DONTESEK DT-M6, F76, `adat/licencek.tsv` `projekt_adat` sor.

## D) Befogadandó tervezett feladatok

**12. SQLITE_EPIT** *(R12)*
- Kérdés: mikor kerüljön be az SQLITE_EPIT (a #76 előfeltétele)?
- a) `/befogad` most, a MUNKATERV 4. sora szerint (folyamat, Sonnet, `munka: adat`, függ #62; a SEMA 3. integritási szabályai tesztként; KK-alapú vers-kulcs, `szamozas`)
- b) a #76 brief-írásakor, vele együtt
- c) később (a #22 lezárása után)
- **Javaslat: a)** — a #76 `kovetkezo`-ja kifejezetten erre vár, és a 7. tétel a) válasza mellett ez a #25a kritikus útja.
- Érinti: új brief + FELADATOK-sor, F76 `fugg`, MUNKATERV 4a.

**13. SZPA_AUDIT és a hiányzó profilfájl** *(R13)*
- Kérdés: mi legyen az SZPA_AUDIT-tal, amelynek bemenete (`SZPA_FORDITOI_PROFIL_prompt.md`) nincs a repóban?
- a) a profilfájl kézi 0. lépésként a repóba (a felhasználó tölti fel), a feladat a 6. lépcsőben (hasznosítás) kerül befogadásra
- b) profilfájl és befogadás most (az 1. hullám szerint)
- c) elvetés; a MUNKATERV-ből kivezetendő
- **Javaslat: a)** — brief a fájl nélkül nem írható; a profil v0.1 egyetlen mintán (Mt 1–4) áll, a mostani hullámban nincs ráépülő feladat.
- Érinti: MUNKATERV 0. lépcső és 4., ADATVAGYON 10./21.

**14. openbible.info-import (DT34)** *(R14)*
- Kérdés: mikor kerüljön be a DT34 szerint külön feladatként eldöntött import?
- a) a #76 brief-írásával együtt (a szó-/vers-lap „kapcsolódó igehelyek” blokkja; a forrás a `jeloltek.forras_kereses` új értéke, ADATVAGYON 22.1)
- b) `/befogad` most, önállóan
- c) a #25b (motívumos nézet) után
- **Javaslat: a)** — a DT34 a kérdést eldöntötte, csak az időzítés nyitott; az első felhasználója a #76.
- Érinti: új FELADATOK-sor, F76 `olvas`/`fugg`, `adat/datasetek.tsv` (4 `hianyzik` sor).

**15. BDB javító menet a teljes Károli–Strong után** *(R15)*
- Kérdés: legyen-e javító menet a Károli-támasz nélkül fordított BDB-szócikkekre (a DT54 „a javító menet pótol” és a DT56 „utólagos visszaellenőrzés elvetve” ellentmondása)?
- a) igen, szűken: a #22 lezárása után a [NINCS KÁROLI-ALAK] szócikkek adatblokkja (Károli-alakok, példaversek) pótlódik, újrafordítás nélkül; külön feladat
- b) nincs javító menet; a DT54 szövege javítandó (a DT56 1. opciója elég)
- c) igen, teljes újrafordítással az érintett szócikkekre
- **Javaslat: a)** — az adat (Károli-alak) pótlása olcsó és nem ütközik a DT56 indokával (az újrafordítás a drága rész).
- Érinti: DONTESEK DT54/DT56 (pontosító sor), F38 brief, ADATVAGYON 19./21., MUNKATERV 6.

**16. Károli-ujjlenyomat (motívum-index előre)** *(R16)*
- Kérdés: kerüljön-e be az ADATVAGYON 1.4 (minden kész motívum Károli-ujjlenyomata, új #22-könyvenként jelentés)?
- a) befogadás a #65 után (a variancia-térképre ül), jelentés-kimenettel, adatírás nélkül (új találat csak a `jeloltek.tsv`-n át)
- b) a #65 hatókörébe
- c) halasztás a #23/#11 utánig
- **Javaslat: a)** — a #65 már nagy; az ujjlenyomat a „nincs közvetlen út” szabály szerint csak jelöltet adhat, ez külön brief.
- Érinti: új FELADATOK-sor, ADATVAGYON 1.4/21.

## E) Szabályok és folyamat

**17. Idézési szabály a saját prózára** *(R17)*
- Kérdés: legyen-e DT-tétel arról, hogy a saját próza csak közkincs/CC BY forrásból idéz szó szerint, NC/SA forrásra csak hivatkozik?
- a) DT-tétel a DT-M6-tal együtt, a #76 publikálása előtt
- b) DT-tétel most, CLAUDE.md-sorral
- c) nem kell
- **Javaslat: a)** — a publikálás előtt számít; a mai kutatói munkát nem korlátozza.
- Érinti: DONTESEK (új helyőrző), ADATVAGYON „Javaslat” 2., később CLAUDE.md / study-rules.

**18. VIBE_GUIDE `lepes=MCP` sora** *(R18)*
- Kérdés: átírható-e a VIBE 5. szakaszának elavult `lepes=MCP` állítása a #52 brief 6. pontja ellenére?
- a) igen: „`lepes` a kutatási lépés kódja vagy `adhoc`, `csatorna=mcp`” (DT-M3)
- b) marad, mert az MCP_BUROK feltételes
- c) a sor „feltételes (DT-M7)” jelölést kap, változatlan szöveggel
- **Javaslat: a)** — a DT-M3 eldöntötte, az elavult mondat félrevezet.
- Érinti: `VIBE_GUIDE.md` 5. szakasz.

**19. A terv → feladat irány gazdája (a rés gyökéroka)** *(R19)*
- Kérdés: ki hajtsa be a jövőben a tervből a feladatokba és a döntésekbe kerülő tételeket?
- a) a #52 brief bővítése: minden futás a repó → terv mellett terv → feladat résjelentést is ad (`naplok/`), és a döntést igénylő tételekből DONTESEK-tételt nyit; plusz a #51 `dontes_hatas.tsv`-jébe a tervdokumentumok sorai
- b) csak a #52 bővítése
- c) csak a #51 gépi őre
- **Javaslat: a)** — a tartalmi résjelentéshez olvasó kell (#52), a visszacsúszás ellen gépi őr (#51); egyik a másik nélkül ugyanoda vezet, ahol most vagyunk.
- Érinti: `F52_TERV_SZINKRON_BRIEF.md`, `adat/dontes_hatas.tsv`, `.claude/commands/konzisztencia.md` (csak leírás; eszközmódosítás külön ágon, D6).

**20. Az ATALAKITASI_TERV állapota** *(R20)*
- Kérdés: kapjon-e az alapterv állapot- és kiegészítés-szakaszt, és kerüljön-e a #52 hatókörébe?
- a) igen: új „Állapot és kiegészítések” szakasz (F0–F7 lezárva; D34/B út, DT28; mutató az ADATVAGYON 18.5/21-re és a MUNKATERV-re; a 4. szakasz elavult pontjainak jelölése), és a #52 hatókörébe vétel
- b) csak az elavult pontok jelölése (4.3, 2. hookok, 10.), a #52 hatóköre marad
- c) az alapterv archív, a két kiegészítő terv a hatályos
- **Javaslat: a)** — a felhasználó szerint az ATALAKITASI az alap; a mutató nélkül a következő olvasó ugyanazt a kiegészítés nélküli tervet látja, amely a rést okozta.
- Érinti: `ATALAKITASI_TERV.md.md` (fejléc, új szakasz, 2., 4.3, 10.), F52 brief.

**21. Célvonal: meddig tart a korpusz** *(R21)*
- Kérdés: mikor dőljön el az ATALAKITASI 11.1 (korpusz-határ; minden motívum végigmegy-e a három szakaszon)?
- a) DT-tétel a #13 (1Móz 17-től) befogadásakor
- b) DT-tétel most
- c) marad a tervben nyitott kérdésként
- **Javaslat: a)** — a #13 az első korpusz-bővítés; addig nem blokkol.
- Érinti: F13 csonk `kovetkezo`, ATALAKITASI 11.1/10.

**22. Arany-készlet a regresszióhoz** *(R22)*
- Kérdés: hol valósuljon meg az ATALAKITASI 11.4 (ISTENTISZT-001, HAMART-001 referencia minden eszközváltozás után)?
- a) a #11 része: a rekonstruált ISTENTISZT-001 és a HAMART-001 a migráció nulla-diff referenciája; a CI-rész (N33-mal) külön ágon (D6)
- b) önálló feladat most
- c) elvetés
- **Javaslat: a)** — a #23 M1/4 már a migráció nulla-diff kategóriáit tervezi; a referencia oda tartozik.
- Érinti: F11 csonk, N33, ATALAKITASI 11.4.

**23. CCR mérőműszer (ATALAKITASI D16)** *(R23)*
- Kérdés: mi legyen a meg nem valósult „CCR bevezetendő” döntéssel?
- a) elavultnak jelölés: a költségmérés az API-naplókból (#21, #77) és a Max-keretből jön
- b) feladat a bevezetésére
- c) nyitva marad
- **Javaslat: a)** — a mérési igényt a #21/#77 mérései fedik; harmadik féltől származó proxy a terv saját indoka szerint is kockázat.
- Érinti: ATALAKITASI 10. D16, 11.6.

---

**Válaszminta:** `1a 2a 3a 4a 5a 6a 7a 8a 9a 10a 11a 12a 13a 14a 15a 16a 17a 18a 19a 20a 21a 22a 23a` — eltérésnél csak a megváltoztatott sor kell.
