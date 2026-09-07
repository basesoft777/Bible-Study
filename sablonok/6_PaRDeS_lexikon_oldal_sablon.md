# 6. PaRDeS lexikon-oldal sablon (Motívumlexikon-pilot alapján)

*v1 — 2026.09.07 (visszafejtve az ISTENTISZT-001 pilot két kimeneti
fájljából — `ISTENTISZT-001_TUDOMANYOS.md` és `ISTENTISZT-001_
OLVASHATO.md` —, hogy a folyamat ismételhető és a kimenet
reprodukálható legyen. Ez a fájl önmagában is teljes, nem támaszkodik
a memóriára.)*

**Kimenet nyelve:** magyar

---

## Mikor használandó

Nem helyettesíti a tematikus study-t — **kizárólag már lezárt,
v12-compliant tematikus tanulmányból** készíthető, annak
"lexikon-nézeteként". Nem automatikus — mindig felhasználói jóváhagyás
után indul, motívumonként egyesével.

**Kötelező előfeltétel-ellenőrzés indítás előtt:**
1. Létezik-e a `[Motívum]_tematikus.md` a `tematikus_lezart/`
   könyvtárban, és szerepel-e "lezárt/önállóan feldolgozott témaként"
   a `PaRDeS_motivumok.md` naplóban?
2. Ha nem — **állj meg**, és javasold először a tematikus study
   lezárását. A lapos lexikon-szöveg (l. alább) csak egy már kiforrott
   study-módszertan (négyforrásos kereszt-ellenőrzés, lexikai/
   tematikus szigorú szétválasztás) mellett termel értelmezhető
   eredményt — enélkül a kimenet nem reprodukálható megbízhatóan.

---

## Kimenet: KÉT fájl, kötelezően mindkettő

| Fájl | Cél | Hossz-jelleg |
|---|---|---|
| `[MOTÍVUM-ID]_TUDOMANYOS.md` | Teljes, minden forrást szó szerint idéző referencia-lap | Hosszú, táblázatos |
| `[MOTÍVUM-ID]_OLVASHATO.md` | Rövid, prózai, nyomtatható változat | Rövid, folyó szöveg |

Ez nem opcionális kettősség — a `Bibliai_Motivumlexikon_tervezesi_
naplo.md` 12. pontja ("a motívumnaplónak önmagában is, adatbázis-
lekérdezés nélkül olvashatónak kell maradnia, akár nyomtatható
formában is") kifejezett tervezési elv, amit ez a két fájl valósít
meg.

Könyvtár: `motivumlog/lexikon_pilot/` (vagy a végleges, nem-pilot
elnevezésű könyvtár, ha a pilot-fázis lezárul).

---

## A) TUDOMÁNYOS változat — kötelező szakaszok, pontos sorrendben

### 0. Metaadatok
Táblázat, mezők pontosan ebben a sorrendben: `ID` (a motívum-
azonosító séma szerint, pl. `ISTENTISZT-001`) | `Rövid UI-címke`
(2-4 szó) | `Teljes cím` | `Formula` (eredeti nyelvi kifejezés,
kiejtéssel) | `Kapcsolódó motívum` (ha van, elhatárolással) |
`Forrás-study` (elérési út) | `Kereszthivatkozás-napló` (elérési
út, ha van) | `Sablon-megfelelőség` (verziószám + audit dátuma).

### 1. Előfordulások — teljes leírással
A forrás-study 1. pontjának táblázata **szó szerint átemelve** —
NEM újrafogalmazva. Oszlopok: Igehely | Kapcsolódás | PaRDeS-szint |
Funkció | Strong-szám(ok) | BDB sense (vagy más lexikon sense-
hivatkozás).

### 2-N. TELJES lexikon-szócikk(ek) szó szerint
Minden motívum-kulcsszóra (jellemzően 2, pl. az ige + a főnév) egy
külön szakasz. Minden szakaszban:
- A releváns sense(ek) **szó szerint, eredeti nyelven** idézve,
  forrásmegjelöléssel (fájlnév + sor).
- Közvetlenül alatta **magyar fordítás**, 🇭🇺 jelöléssel.
- **Forrás:** sor a szakasz végén (fájlnév, feldolgozási módszer).
- Ha a szócikk hosszú és sok, a motívum szempontjából nem releváns
  részt is tartalmaz (pl. morfológiai alakok teljes listája), ezt
  explicit jelezni kell: *"a teljes szócikk X karakter — itt csak a
  releváns N. és M. sense szerepel, mert a többi [ok]"*.

**Ha egy szóhoz TÖBB lexikon is elérhető** (pl. TBESG ÉS Thayer),
mindegyiket **külön alszakaszban, egymás után** kell idézni — ne
összeolvasztva, ne csak az egyiket választva. A cél a **kereszt-
olvasás lehetővé tétele**, nem a redundancia elkerülése — ez a
lapos, teljes-szöveges lexikon-struktúra tudatos kihasználása (l.
tervezési napló 15. pont).

Minden ilyen többforrásos szakasz után kötelező egy **"Miért fontos
ez a lelet"** bekezdés, ami kimondja: mit ad hozzá a második/
harmadik forrás, amit az első önmagában nem adott — vagy explicit
jelzi, ha nem ad hozzá semmi újat.

### N+1. LXX-híd nyers adat (ha a motívum ÓSZ-i eredetű és van ÚSZ-i
kapcsolódása)
Táblázat: Igehely | Görög szóalak | Morfológiai kód | Strong |
Forrás-jelzés (pl. `ABP-pótolt`, `LXX_WH`, `ELTERO_SZOVEGALAP`).
Forrás-fájlok felsorolva a táblázat alatt.

### N+2. TSK és Károli-KH kereszthivatkozás — nyers eredmény
A négyforrásos módszertan (`PaRDeS_gyorsreferencia.md`) szerinti,
**minden** vizsgált igehelyre lefuttatott TSK (Votes ≥ 15 szűréssel)
és Károli-KH eredmény, felsorolva:
- Ami **független megerősítés** egy már ismert kapcsolatra
- Ami **új, valódi találat** — ezt kiemelve, külön bekezdésben
  indokolva
- Ami ellenőrizve lett, de **nem releváns** — ezt is fel kell
  sorolni, ne csak hallgatni róla (a hamis nyomok dokumentálása
  ugyanolyan fontos, mint a találatoké)

### N+3. Kapcsolatok — teljes relációs adat, diagrammal és
alátámasztással
1. **Mermaid `graph LR` diagram** — minden előfordulás legalább egy
   élen szerepeljen. Szín-konvenció: `style X fill:#fff3cd,
   stroke:#856404` sárga az ELŐKÉP/BETELJESEDÉS csomópontra;
   `fill:#f8d7da,stroke:#721c24` piros a kivételes/nyitott/be nem
   sorolható csomópontra; szaggatott nyíl (`-.->`) bizonytalanabb,
   csak lexikai (nem funkcionális) kapcsolatnál.
2. Jelmagyarázat bekezdés közvetlenül a diagram alatt.
3. **⚠️ Séma-korlát bekezdés, ha releváns** — ha egy eset nem fér
   bele a Forrás-igehely/Cél-igehely kétpontos modellbe (pl. egy
   versen belüli kontraszt), ezt itt explicit ki kell mondani, és
   jelezni, hogy ez nyitott tervezési kérdés a `Bibliai_
   Motivumlexikon_tervezesi_naplo.md` KAPCSOLATOK-fejezetéhez.
4. **"A kapcsolatok alátámasztása" táblázat** — MINDEN sorra: miért
   ez a funkció-címke, miért ez a bizonyossági szint (Magas/
   Közepes/Alacsony), konkrét szövegi indoklással (szó szerinti
   idézés vs. parafrázis vs. csak lexikai egyezés).
5. Zárósor: hivatkozás a nyers, gépileg olvasható forrásra
   (`Motivum_kapcsolatok_PILOT.tsv` vagy véglegesített megfelelője),
   az oszlopnevek felsorolásával.

### N+4. Módszertani napló
Táblázat: # | Módszer | Eredmény — a study elkészítésekor futtatott
összes ellenőrzési réteg (jellemzően a projekt 8 rétegű
ellenőrzési sorozata, l. `method-learnings`), tömören összefoglalva.
Alatta egy mondat, ami a teljes indoklás helyére mutat (chat-napló
dátuma, kereszthivatkozás-napló fájlneve).

### N+5. ÚJ FELISMERÉS (ha van) — pilot-only jelöléssel
Ha a lexikon-oldal elkészítése közben olyan felismerés születik,
ami **nincs** még a tematikus study-ban, ezt **külön, explicit
jelölt szakaszként** kell felvenni, a szakasz elején kötelező
figyelmeztetéssel: *"Ez a szakasz kizárólag a lexikon-pilotban
rögzített megfigyelés — a `[Motívum]_tematikus.md` fájlba
szándékosan NEM került be, amíg külön döntés nem születik róla."*
A szakasz végén kötelező egy "Amit ez a felismerés NEM állít"
bekezdés (a túlterjeszkedés explicit korlátozására) és egy "Nyitott
kérdés a folytatáshoz" bekezdés.

### Utolsó szakasz. Nyitott kérdések és séma-korlátok
Számozott lista — minden, ami a fenti szakaszokban "nyitva" maradt
(funkcionális besorolás hiánya, séma-korlát, forrás hiánya stb.),
egy helyen összegyűjtve. Lezárt tételek áthúzva (`~~...~~`)
megtarthatók, dátummal, ha időközben megoldódtak — ne töröld, hogy
látszódjon a folyamat.

---

## B) OLVASHATÓ változat — kötelező szakaszok, pontos sorrendben

1. **Cím + rövid bevezető bekezdés** — a formula bemutatása, eredeti
   nyelven + kiejtéssel + magyar jelentéssel, 2-3 mondatban.
2. **"Hol jelenik meg a Bibliában?"** — az összes előfordulás
   **prózában**, kronológiai/logikai csoportosításban (NEM
   táblázat) — minden csoport egy bekezdés, félkövérrel kiemelt
   nyitómondattal (pl. *"A történet Énóssal kezdődik..."*).
3. **Kivétel/ellenpélda szakasz(ok)**, ha van — külön alcímmel
   kiemelve (pl. *"Egy meglepő fordulat"*, *"Egy figyelmeztető
   ellenpélda"*), prózában elmagyarázva, miért lóg ki a mintából.
4. **"Hogyan kapcsolódnak egymáshoz az igehelyek?"** — egyszerűsített
   Mermaid-diagram (kevesebb csomópont, mint a TUDOMÁNYOS
   változatban — csak a fő ív + a legfontosabb kivétel), ugyanazzal
   a szín-konvencióval.
5. **"Miért fontos ez ma?"** — rövid alkalmazási bekezdés; ha van
   jóváhagyott nevesített tanító, aki erre a motívumra épít, itt
   említhető, forrásmegjelöléssel.
6. **"Rövid nyelvi jegyzet"** — felsorolás, 2-4 kulcsszó, kiejtéssel
   és tömör jelentéssel; a görög megfelelő is itt, ha releváns.
7. **Záró dőlt megjegyzés** — visszamutatás a teljes study-ra és a
   TUDOMÁNYOS változatra, elérési úttal.

**Terjedelmi szabály:** az OLVASHATÓ változat nem tartalmazhat
táblázatot, szó szerinti idézetet lexikonból, vagy módszertani
naplót — ha egy tartalom csak táblázatosan fejezhető ki érthetően,
az a TUDOMÁNYOS változatba való, nem ide.

---

## Közös terminológiai és formai szabályok (megegyezik a többi
sablonnal)

- „Szentlélek" helyett mindig **„Szent Szellem"**
- Minden görög/héber szótári szó mellett feltüntetve a **kiejtés**
- Igehely-rövidítések egységesen, szóköz nélkül (pl. „1Kir 18:24")
- Forrásmegjelölés kötelező minden idézetnél — fájlnév + (ha van)
  sor/Strong-szám

## Fájlnév-konvenció

`[MOTÍVUM-ID]_TUDOMANYOS.md` és `[MOTÍVUM-ID]_OLVASHATO.md` — a
motívum-azonosító séma szerinti ID-vel (pl. `ISTENTISZT-001`), nem a
leíró magyar névvel.

## Konfliktuskezelés

Ha két elmentett szabály ütközni látszik, explicit rákérdezés
következik, nem önkényes döntés.

---

*A két fájl elkészítése előtt belső önellenőrzés fut le: megvan-e a
lezárt tematikus study, a négyforrásos módszertan lefutott-e minden
igehelyre (nem csak mintavétellel), és a lexikai/tematikus
kapcsolatok explicit el vannak-e választva egymástól.*
