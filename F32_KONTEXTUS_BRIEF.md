---
feladat: 32
cim: Kontextus-őrzés: az értelmező munka egy kézben marad, a csomagmód csak adatfeladatra
kod: KONTEXTUS
tipus: feladat
fazis: folyamat
munka: folyamat
modell: sonnet
allapot: fut
ag: claude/f32-kontextus
pr: https://github.com/basesoft777/Bible-Study/pull/164
ad: négy munkaszabály a MUNKAMENET-ben és a brief-sablonban, a feladatok.py fejléc- és csomag-ellenőrzése, a #23 briefjének kiegészítése és függése; döntési tétel a TEREMT-002 3. lépésének előrehozásáról
kovetkezo: Folytatás: a DT-F32a eldőlt (🟢, 1. opció); hátra a független ellenőrzés az új E18/csomag/teszt-részre, a zárójelentés és a PR; az orkesztrátor végzi
olvas: [MUNKAMENET.md, CLAUDE.md, BRIEF_SABLON.md, DONTESEK.md, eszkozok/feladatok.py, F23_MOTIVUM_FORRAS_BRIEF.md, TEREMT002_KUTATAS_BRIEF.md, .claude/commands/kovetkezo.md, motivumok/TEREMT-002.md, "tematikus_lezart/TEREMT-002*", "tematikus_lezart/naplok/TEREMT-002*"]
ir: [MUNKAMENET.md, CLAUDE.md, BRIEF_SABLON.md, F32_KONTEXTUS_BRIEF.md, DONTESEK.md, eszkozok/feladatok.py, eszkozok/teszt_feladatok.py, eszkozok/tesztek/test_feladatok_kontextus.py, .claude/commands/kovetkezo.md, F23_MOTIVUM_FORRAS_BRIEF.md, naplok/KONTEXTUS_szabalyok.md, naplok/ELLENOR_KONTEXTUS.md]
fugg: []
nem_fugg: [22]
---

# F32_KONTEXTUS_BRIEF.md — Kontextus-őrzés

*FELADATOK #32 · Modell: sonnet · v1.2 · 2026.10.01 · a #23 (MOTIVUM_FORRAS) M1 lépése előtt kell lefutnia; a #23 ettől a feladattól függ (K4)*

<!-- KOZVETLEN_FUTTATAS -->
Olvasd el ezt a briefet és az `olvas` listát. Hajtsd végre a K1–K4 lépéseket külön commitokban, majd a K5-ben vedd fel a döntési tételt a `DONTESEK.md`-be 🟡 állapotban, és **állj meg**. Motívumfájlt (`tematikus_lezart/`, `motivumok/`, `lexikon/`, `genezis/`) nem írsz. Menetzárás a `CLAUDE.md` szerint: `fuggetlen-ellenor` → `naplok/ELLENOR_KONTEXTUS.md`, push, draft PR, záró összefoglaló (első sor: PR-link és CI-állapot).
<!-- KOZVETLEN_FUTTATAS -->

## 1. Cél

Az ISTENTISZT-001 pilot minősége nem abból jött, hogy egy ülésben készült. A lexikonoldal 8 briefben, sok javító körben állt össze. A minőség forrása az volt, hogy egyetlen összefüggő tematikus tanulmány volt az alap. Ezt egy kéz írta gondolatmenetként, és minden későbbi lépés ebből renderelt, illetve ehhez igazodott.

A B-út (D34) és a csomagmód (D20) ezt két irányból fenyegeti:

- Ha az értelmező munka feladatokra, modellekre és subagentekre oszlik, nincs, aki az egészet átlátja.
- Ha a forrásdokumentum mezőkből áll, amelyeket külön menetek töltenek, akkor lesz adat, de nem lesz gondolatmenet, és a render egy kitöltött űrlapot mutat.

A feladat négy szabályt rögzít a munkafolyamatban, és egy döntést tesz a felhasználó elé. Nem renderel, nem ír tanulmányt, és nem módosítja a `general.py`-t.

A szabályok két munkafajtára épülnek:

- **Adatmunka** (import, szótárfordítás, LXX-megfelelő, licenctábla, Károli–Strong, CI, szkript): nem kell hozzá a motívum átlátása. Csomagmód, modellkiosztás és subagent szabadon használható.
- **Értelmező munka** (tematikus tanulmány, kereszthivatkozás-napló, értelmezés, kivonat, a jelentéstartomány kiválasztása a D50 szerint, a `motivumok/[ID].md` kézi forrása): a próza egy kézben készül, és aki később belenyúl, az egészet olvassa.
- **Folyamatmunka** (szabály, sablon, orkesztrátor, ez a brief): csomagolható, ha nem ír motívumfájlt.

## 2. Hatókör

**Benne van:**

- a `MUNKAMENET.md` és a `CLAUDE.md` szabálysora;
- a `BRIEF_SABLON.md` új `munka` mezője;
- a `feladatok.py` két új ellenőrzése, és ezek bekötése a `/kovetkezo` csomagolási lépésébe;
- a `F23_MOTIVUM_FORRAS_BRIEF.md` 1. és 2. pontjának kiegészítése, valamint a fejlécének függése;
- egy `DONTESEK.md`-tétel.

**Nincs benne:**

- bármely `tematikus_lezart/`, `motivumok/`, `lexikon/` vagy `genezis/` fájl írása;
- a `general.py` és a sablonok módosítása;
- a TEREMT-002 3. lépésének futtatása (az a #12, külön brief);
- a CI-szabály implementálása (D6, külön ág).

## 3. Lépések

### K1 — a négy szabály a `MUNKAMENET.md`-ben (új szakasz: „Kontextus-őrzés”)

1. **Az értelmező réteg egy kézben készül.** Egy motívum értelmező rétegének prózáját egy brief írja, egy modellel (`DONTESEK.md` DT-F32b: az értelmező modell; jelenleg `opus`). Nem kerül csomagba, és nem osztható író subagentekre. A session-határ megengedett: ha a kontextus nem fér el, a folytató session ugyanazt a briefet viszi tovább, és a 3. szabály szerint az egészet olvassa.
   - **Kivétel:** csak olvasó subagent (például `fuggetlen-ellenor`, audit-szkript) értelmező menetben is futhat. Író subagent nem futhat.
   - A csomagmódba `munka: adat`, valamint motívumfájlt nem író `munka: folyamat` feladat kerülhet.
2. **A forrásdokumentum próza-elsőbbségű.** A `motivumok/[ID].md` összefüggő érvelés markerekkel, amelyekből a generátor kinyeri az adatot. Nem adatséma, amelybe prózamezők vannak beszúrva.
   - Az `adat/SEMA.md` a kinyerést írja le, nem a dokumentum szerkezetét.
   - A sablon (`9_PaRDeS_motivum_forras_sablon.md`) szakaszsorrendet és markereket adhat, mezőhatárokat nem.
3. **Aki motívumba ír, az egészet olvassa.** Ha egy feladat `ir` listájában `motivumok/[ID]`, `tematikus_lezart/[ID]*` vagy `lexikon/[ID]*` szerepel, akkor az `olvas` listájának kötelezően tartalmaznia kell a motívum teljes tematikus tanulmányát és a kereszthivatkozás-naplóját. Ez a javító körökre is érvényes. A `feladatok.py` ellenőrzi (K3).
4. **A lánc próbája megelőzi a szerkezet véglegesítését.** A B-szerkezet forrássablonja (#23 M1) csak akkor véglegesíthető, ha két feltétel teljesül:
   - egy motívum teljes értelmező rétege a fenti szabályok szerint elkészült;
   - az eredmény hozza az ISTENTISZT-001 mércéjét (L1–L5 a #10 szerint).

   A próba jelöltje a TEREMT-002 3. lépése (#12), lásd K5.

A `CLAUDE.md` rétegtáblája alá egy sor kerül: „Az értelmező próza egy kézben, egy modellel készül, és aki belenyúl, az egészet olvassa; csomagmód csak adat- és motívumot nem író folyamatfeladatra (KONTEXTUS K1).”

### K2 — `BRIEF_SABLON.md`: új `munka` mező

| Mező | Kötelező | Érték |
|---|---|---|
| `munka` | `feladat` típusnál | `adat` · `ertelmezo` · `folyamat` |

A táblázat alá kerülő szabályok:

- Egy `munka: ertelmezo` feladat modellje az értelmező modell, nem kerül csomagba, és az `olvas` listája a K1/3 szerint teljes.
- Egy `munka: folyamat` feladat csomagolható, ha az `ir` listája nem tartalmaz motívumfájlt. Ha tartalmaz, `ertelmezo`-ként kezelendő.
- A régi fejlécű (mező nélküli) brief `munka: adat`-nak számít. Kivétel, ha az `ir` listája motívumfájlt tartalmaz: ilyenkor a mező hiányzónak számít, és a feladat nem fut, amíg ki nincs töltve.
- A `fazis` mező a projektfázist jelöli, a `munka` mező a munka fajtáját. A kettő független egymástól.

**K2.1** Ugyanebben a commitban az `ellenoriz` (E18) ismert kulcsai közé felveszed a `munka` kulcsot az értékkészletével, és **ennek a briefnek a fejlécébe** beírod: `munka: folyamat`. A befogadáskor a mező szándékosan hiányzott (K-D13).

### K3 — `eszkozok/feladatok.py`: két ellenőrzés és a bekötésük

**K3.0** Azonosítsd, hol dől el ma a csomagba sorolás: a `feladatok.py` egy függvényében, vagy csak a `.claude/commands/kovetkezo.md` prompt-szövegében. Az eredményt rögzítsd a naplóban.

**K3.1** Új alparancs: `python eszkozok/feladatok.py csomag <id> <id> ...`. Hibát ad, ha a felsorolt feladatok közül bármelyik nem csomagolható a K2 szerint (`ertelmezo`, motívumot író `folyamat`, vagy hiányzó `munka` mező motívumot író briefben).

A `/kovetkezo` parancs csomagjavaslat előtt kötelezően futtatja ezt. Ha hibát kap, az érintett feladatot egyedül ajánlja.

**K3.2** A `fuggesek` alparancs fejléc-ellenőrzése bővül: ha egy feladat motívumfájlt ír, de az `olvas` listájából hiányzik a motívum tanulmánya vagy naplója, az hiba, a hiányzó fájl nevével.

Mindkettő az E18 szabály (fejléc-érvényesség) része. A CI-implementáció külön ágon készül (D6). Itt csak a `feladatok.py`, a `kovetkezo.md` és a szabály leírása készül el a `naplok/KONTEXTUS_szabalyok.md`-ben.

Próbák a naplóban, a parancs tényleges kimenetével:

- legalább egy pozitív és egy negatív fejléc a K3.1-hez és a K3.2-höz;
- a TEREMT-002-re szabott negatív próba: `ertelmezo` feladat, amelyiknek az `olvas` listájából hiányzik a napló.

### K4 — a `F23_MOTIVUM_FORRAS_BRIEF.md` kiegészítése és függése

**K4.0** Ellenőrizd, van-e a #23-nak távoli ága (`git branch -r`), és futott-e már menete. Ha van nyitott ága, ⛔ állj meg és kérdezz: a K4 csak a main-en lévő briefet módosítja, és a futó ággal ütközhet.

Ha nincs nyitott ág, a módosítások:

- **Fejléc:** a `fugg` mezőbe a `32` kerül, a `nem_fugg` mezőből pedig kikerül.
- **1. Cél:** egy bekezdés a próza-elsőbbségről (K1/2), és arról, hogy az M1 forrássablon tervezet marad a K5 szerinti próbáig.
- **2. Hatókör, „Nincs benne”:** „a forrásdokumentum mezőkre bontása; a szakaszok külön feladatra vagy író subagentre osztása”.
- **M0, 1. pont, `B_helye` oszlop:** `kezi_forras` esetén kötelező a `szint` megadása, és a megjegyzés, hogy a szakasz az összefüggő érvelés része, nem önálló mező.
- **Ha a #23 értelmező lépést tartalmaz:** annak `munka: ertelmezo` jelölése és az `olvas` lista K1/3 szerinti kiegészítése.

### K5 — ⛔ `DONTESEK.md`-tétel: a próba helye

**Kérdés:** a TEREMT-002 3. lépése (#12) ma a #11 (migráció) után áll, és a T3 eredetileg prózát, lexikonoldalt és LXX-döntéseket is tartalmaz. A K1/4 szabály szerint a próbának a #23 M1 *előtt* kell lefutnia. A D1 viszont tiltja az éles rendert az 1. fázis (#5, #8) előtt.

**Opciók:**

1. **A #12 kettéválik.**
   - **#12a — próza-próba:** a #23 M0 után fut, egy Opus-briefben, a jelenlegi eszközökkel, a T1–T2-ből. Kimenete a tematikus tanulmány prózája és a `motivumok/TEREMT-002.md`. A render csak a `generalt_proba/` alá kerül, éles lexikonoldal nincs. Az LXX-helyek „függő” jelölést kapnak. Az eredmény a #23 M1 bemenete.
   - **#12b — élesítés:** lexikonoldal, LXX-döntések és élesítés. Az eredeti helyén marad (#5, #8 és #11 után), és a #12a prózáját használja.
2. **Marad a mai sorrend.** A próba ebben az esetben az ISTENTISZT-001 újraírása a B-sablonnal, a #23 után. Ez drágább, és már egyszer megírt anyagon mér.
3. **Más motívum a próbára.**

**Javaslat:** az 1. opció. Nem sérti a D1-et, mert éles render nem készül, a próza pedig a D50 szerint amúgy is a tanulmányban születik. A tétel a felhasználóé; a menet itt megáll.

## 4. Elfogadási feltételek

- A `MUNKAMENET.md` és a `CLAUDE.md` tartalmazza a négy szabályt, az olvasó subagentre vonatkozó kivétellel együtt. A `BRIEF_SABLON.md` tartalmazza a `munka` mezőt a három értékkel és a `folyamat` szabályával.
- A `feladatok.py csomag` és a `feladatok.py fuggesek` a negatív próbákon hibát jelez, a pozitívakon nem. A kimenet a naplóban van. A `/kovetkezo` parancs szövege hivatkozik a `csomag` ellenőrzésre.
- A `F23_MOTIVUM_FORRAS_BRIEF.md` a K4 szerint módosítva, a `fugg` mezője tartalmazza ezt a feladatot, és a fejléce érvényes (E18). Ha a K4.0 megállást adott, a K4.0 kérdése szerepel a záró összefoglalóban.
- Ennek a briefnek a fejléce a K2.1 után tartalmazza a `munka: folyamat` mezőt, és átmegy az `ellenoriz`-en és a saját K3.2 ellenőrzésén.
- A K5 tétel a `DONTESEK.md`-ben van, 🟡 állapotban.
- A CI zöld, és a `naplok/ELLENOR_KONTEXTUS.md` elkészült.
- Egyetlen `tematikus_lezart/`, `motivumok/`, `lexikon/` vagy `genezis/` fájl sem változott; a `git diff --stat` kimenete a naplóban.

## 5. Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| K-D1 | A szabályok külön folyamat-briefben szerepelnek, nem a #23 részeként | a #23 Opus-menet tervez; a szabálynak meg kell előznie a tervet, és más feladatokra (#9, #12, #13) is vonatkozik | a #23 1. lépéseként |
| K-D2 | A próbát (#12) nem ez a brief futtatja, csak a helyéről dönt | az értelmező munka saját brief (K1/1); ez a brief maga is betartja | a próba beépítése K6-ként |
| K-D3 | `munka` mező a fejlécben, nem fájlminta-alapú felismerés | a csomagolási tilalom legyen explicit, és a generátor tudja olvasni; a fájlminta csak az `olvas`-ellenőrzéshez elég | csak a `feladatok.py` következtet az `ir` listából |
| K-D4 | A régi fejlécű, motívumfájlt író brief nem fut a mező nélkül | a D27 mintájára: hiányos fejléc ne engedjen értelmező munkát csomagba | alapértelmezés `adat` mindenre |
| K-D5 | *(v1.1)* „Egy kéz” az „egy session” helyett: session-határ megengedett, a feladat-, modell- és író subagent-szétosztás nem | az ISTENTISZT-001 minősége az egy összefüggő tanulmányból jött, nem az egy ülésből (a lexikonoldal 8 briefben készült); nagy motívumnál az egy session a kontextusablak miatt betarthatatlan | szigorú egy session |
| K-D6 | *(v1.1)* Olvasó subagent értelmező menetben is futhat | a `fuggetlen-ellenor` minden menetzárás kötelező lépése, és nem ír prózát | teljes subagent-tilalom |
| K-D7 | *(v1.1)* A K5 javaslata a #12 kettéválasztása: a próza-próba (#12a) előre kerül, éles render nélkül | így a K1/4 próbája megelőzi a #23 M1-et, és a D1 sem sérül (az éles render a #5 és #8 után marad) | a #12 egészének előrehozása éles lexikonoldallal |
| K-D8 | *(v1.1)* `munka: folyamat` csomagolható, ha nem ír motívumfájlt; a `fazis` és a `munka` mező független | a v1 nem mondta meg, mi a folyamatmunka csomagolási státusza, és a két mező összemosódott | a `folyamat` érték elhagyása |
| K-D9 | *(v1.1)* Az értelmező modell a `DONTESEK.md`-ben rögzített, a szabály nem égeti be | egy modellváltás ne igényeljen szabálymódosítást | `opus` a szabály szövegében |
| K-D10 | *(v1.1)* A #23 függése ettől a feladattól a fejlécben rögzül, ütközés-ellenőrzéssel (K4.0) | a v1 sorrendjét csak a szöveg mondta ki, gépileg semmi nem állította meg az M1-et | `nem_fugg: [23]` |
| K-D11 | *(v1.1)* A csomag-ellenőrzés külön alparancs (`csomag`), amelyet a `/kovetkezo` kötelezően hív | a csomagba sorolás a `/kovetkezo`-ban dől el, nem a `fuggesek`-ben; a helyét a K3.0 tisztázza | az ellenőrzés a `fuggesek`-be építve |
| K-D12 | *(v1.1)* Az `olvas` lista egy motívumra (TEREMT-002) szűkítve | a K3 próbáihoz egy motívum elég; a teljes `tematikus_lezart/` és `motivumok/` olvasása felesleges tokenköltség | teljes könyvtárak |
| K-D13 | *(v1.2)* A brief `munka` mező nélkül fogadható be; a mezőt a K2.1 veszi fel a saját fejlécébe, az `ellenoriz` bővítésével együtt | a mezőt maga a brief vezeti be, így befogadáskor az `ellenoriz` ismeretlen kulcsként elutasítaná; a K2 régi fejlécre vonatkozó szabálya szerint mező nélkül `adat`-nak számít, ami csomagolhatóság szempontjából megegyezik a `folyamat`-tal, mert motívumfájlt nem ír | az `ellenoriz` előzetes, kézi bővítése a main-en; YAML-megjegyzésbe tett mező |
