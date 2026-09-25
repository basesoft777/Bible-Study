# ELŐKÉSZÍTÉS — cu31924098819406 ↔ biblicotheologic00cremuoft oldalkonkordancia

*Az O0.6.2(b) ÁLLJ-ra adott válasz: az O0.6.2(c) hat oldalszáma előtt oldalkonkordanciát
készítettünk a két kiadás között. Ez a fájl még nincs commitolva; a `CREMER_OCR_BRIEF.md`
és a `konkordancia/README.md` nem módosult.*

---

## 1. ᾅδης és ἐπικαλέω/ἐπικαλέομαι szócikkfej-előfordulások, Supplement-kezdet

### 1.1 `biblicotheologic00cremuoft` (van benne görög — közvetlen keresés)

Pontos alak-egyezéssel (NFC, hangjelek és kis/nagybetű nélkül) a `_hocr.html`-ben:

| Címszó | Level | JSON-oldal | Kontextus (rövidítve) |
|---|---|---|---|
| ἐπικαλέω (1.) | 347 | 335 | `᾿Εκκλησία ᾿Επικαλέω … Ἔπικαλέω to call to, to call upon` — szócikkfej |
| ἐπικαλέω (2.) | 348 | 336 | `᾿Επικαλέω Παρακαλέω οὖν ἐπικαλέσονται εἰς ὃν οὐκ` — folytatás |
| ἐπικαλέω (3., Supplement) | 757 | 745 | `Καλέω 742 * Exixaréo` — **futófejléc, a nyomtatott oldalszám a fejlécben szó szerint „742”** |
| ἐπικαλέω (4., Supplement) | 758 | 746 | `᾿Επικαλέω Καλύπτω ἐπικαλούμενον καὶ λέγοντα κύριε κατ` — folytatás |
| ἐπικαλέω (mutatóban) | 933 | 918 | görög szómutató sora |

A pontos alakkeresés a `ᾅδης`-re **nem adott találatot** — a szócikkfej OCR-je itt latin/görög
keveredésű torzkép (`Adns`, `4δης`), amit a szigorú alak-egyezés nem fog meg. Tágabb
(substring, `csv` nélküli `bare()`-normalizált) kereséssel és a futófejléc-mintázat
(`[bal őrszó] [oldalszám] [jobb őrszó]`) felhasználásával:

| Címszó | Level | Futófejléc szó szerint | Nyomtatott oldalszám a fejlécben |
|---|---|---|---|
| ᾅδης (1.) | 79–80 | `Ἀδελφότης 67 "ἅδης"` / `Adns 68 "4δης"` | **67–68** — pontosan egyezik a cu31924 §0.5-anchorral |
| ᾅδης (2., Supplement) | 625 | `Φιλάδελφος 610 A8ns` | **610** — a fejléc szó szerint ezt a számot tartalmazza |
| ᾅδης (3., Supplement, folyt.) | 626 | `Adns 611 Aidas` | 611 |

**Fontos módszertani észrevétel:** a `_page_numbers.json` `pageNumber` mezője a 625. levélre
**613**-at ad, miközben a nyomtatott oldal fejléce szó szerint **610**-et mutat (3 oldal
eltérés) — l. 2.3 pont, ez egy rendszerhiba a JSON-ban, nem kiadás-eltérés.

### 1.2 Supplement kezdőoldal mindkét kiadásban

- **cu31924** — a `SUPPLEMENT.` angol címsor level 607-en (JSON-oldal 592, üres
  címlap) és level 609-en (JSON-oldal 591, itt kezdődik ténylegesen a szöveg:
  `SUPPLEMENT. Ἀγαλλιάομαι, a deponent verb which appears exceptionally in an active
  form Luke i. 47…`).
- **cremuoft** — a `SUPPLEMENT.` címsor **level 605**-ön, ugyanazzal a szöveggel:
  `SUPPLEMENT. ᾿Αγαλλιάομαι, ἃ deponent verb which appears exceptionally in an active
  form Lake i 47…` — **szó szerint azonos szöveg**, ellentétben a címszavak ábécésorrendjének
  megszakadásával (az előző level 602 még a főszöveg vége, ω/ψ környéki szócikkek).
  A JSON ezt a levelet oldal 593-nak jelöli, de a következő level (606) futófejléce
  szó szerint „591”-et mutat (`Ἀγαλλιᾶσθαι 591 Ἀγαλλιᾶσθαι`) — vagyis a level 605
  valódi nyomtatott oldala **590**, a level 606-é **591**.

**Következtetés:** a Supplement mindkét kiadásban **ugyanazon az oldalszámon** (590–591)
kezdődik, szó szerint azonos szöveggel. A korábbi ÁLLJ-jelentésben feltételezett „a
cremuoft főszövege ~876-ig tart, a Supplement sokkal később kezdődik” **téves volt** — ez
a `_page_numbers.json` egy belső hibájának (2.3 pont) a félreértelmezéséből adódott.

---

## 2. Angol horgonyos konkordancia (cu31924 minden 20. oldala → cremuoft)

**Módszer:** a cu31924 minden 20. nyomtatott oldalán (mutatók nélkül, oldal 20–900) a
3. sortól kezdve 6 egymást követő, kizárólag latin betűs (görög/fejléc-token nélküli) szót
vettünk, kisbetűsítve, írásjel nélkül; a cremuoft teljes angol szóláncában kerestük
(csak egyedi találat számít, egyébként a következő sor). A találat levelét a cremuoft
`_page_numbers.json`-jából (`json_oldal`) **és** a level saját futófejléc-számjegyéből
(`header_oldal`, ha volt tiszta olvasat az első ~6 tokenben) is jelentjük.

| cu31924 oldal | cremuoft level | json_oldal | header_oldal | eltolás (cu−json) |
|---|---|---|---|---|
| 20 | 31 | 19 | 1* | +1 |
| 40 | 51 | 39 | 9* | +1 |
| 60 | 71 | 59 | 59 | +1 |
| 80 | 91 | 79 | 79 | +1 |
| 100 | 111 | 99 | 99 | +1 |
| 120 | 131 | 119 | 119 | +1 |
| 140 | 151 | 139 | 189* | +1 |
| 160 | 171 | 159 | 159 | +1 |
| 180 | — | — | — | nincs egyedi horgony |
| 200 | — | — | — | nincs egyedi horgony |
| 220 | — | — | — | nincs egyedi horgony |
| 240 | 250 | 238 | 238 | +2 |
| 260 | 271 | 259 | 259 | +1 |
| 280 | — | — | — | nincs egyedi horgony |
| 300 | 311 | 299 | 299 | +1 |
| 320 | 331 | 319 | 819* | +1 |
| 340 | 351 | 339 | 339 | +1 |
| 360 | — | — | — | nincs egyedi horgony |
| 380 | 391 | 379 | — | +1 |
| 400 | — | — | — | nincs egyedi horgony |
| 420 | 431 | 419 | 419 | +1 |
| 440 | 451 | 439 | 439 | +1 |
| 460 | 471 | 459 | 459 | +1 |
| 480 | 491 | 479 | 479 | +1 |
| 500 | 511 | 499 | 499 | +1 |
| 520 | 531 | 519 | 519 | +1 |
| 540 | — | — | — | nincs egyedi horgony |
| 560 | 571 | 559 | 559 | +1 |
| 580 | 591 | 579 | 579 | +1 |
| **600** | 614 | **602** | **599** | **−2 (json), +1 (header)** |
| **620** | 634 | **622** | **619** | **−2 (json), +1 (header)** |
| 640 | — | — | — | nincs egyedi horgony |
| 660 | — | — | — | nincs egyedi horgony |
| **680** | 694 | **682** | **679** | **−2 (json), +1 (header)** |
| 700 | 714 | 702 | 99* | +1 (json) |
| **720** | 734 | **722** | **719** | **−2 (json), +1 (header)** |
| **740** | 754 | **742** | **739** | **−2 (json), +1 (header)** |
| 760 | — | — | — | nincs egyedi horgony |
| **780** | 794 | **782** | **779** | **−2 (json), +1 (header)** |
| **800** | 814 | **802** | **799** | **−2 (json), +1 (header)** |
| **820** | 834 | **822** | **819** | **−2 (json), +1 (header)** |
| **840** | 854 | **842** | **839** | **−2 (json), +1 (header)** |
| **860** | 874 | **862** | **859** | **−2 (json), +1 (header)** |
| 880 | — | — | — | nincs egyedi horgony |
| 900 | 914 | 899 | 899 | +1 |

*A csillagozott `header_oldal` értékek hibás olvasatok — a naiv „első számjegy-token az
első 6 tokenben” heurisztika idézetben szereplő verzőszámot vagy sorszámot talált el a
valódi oldalszám helyett (pl. Igehely-hivatkozás). Ezeket a 2.3 pont nem használja fel;
csak a tiszta, futófejléc-mintázatú olvasatok (nem csillagozottak) számítanak bizonyítéknak.*

### 2.1 Főszöveg (oldal 20–580)

**Eltolás: cu31924 oldal − cremuoft valódi oldal = +1, egyenletesen** (a `header_oldal`
oszlop ezt közvetlenül igazolja, ahol tiszta olvasat volt). A `json_oldal` ugyanezt az
egyenletes +1-et mutatja — **a JSON ezen a szakaszon megbízható**.

### 2.2 Supplement eleje (oldal 600–860, level ~614–874)

**A `json_oldal` −2-re vált (vagyis json_oldal = cu_oldal − 2, szemben a főszöveg −1-ével)
— ez egy +1 oldalas romlás a json-ban.** Ezzel szemben a **`header_oldal` (ahol tiszta
olvasat volt) továbbra is szigorúan +1-et mutat, ugyanúgy, mint a főszövegben.** Ez azt
jelenti: **a `_page_numbers.json` `pageNumber` mezője ezen a szakaszon (kb. level 605-től
890-ig) szisztematikusan 3-mal magasabb értéket ad, mint a lapon ténylegesen nyomtatott
oldalszám** — l. 2.3.

### 2.3 A `_page_numbers.json` hibája (level ~605–890)

A hiba mértéke pontosan 3 oldal, és a Supplement címlapjánál (level 605) kezdődik: a
level 606 futófejléce szó szerint „591”, a JSON viszont 594-et ad ugyanarra a levélre.
A hiba a teljes Supplement első kb. 285 levelén át egyenletesen fennmarad (a 610-es és
742-es ᾅδης/ἐπικαλέω-horgonyoknál igazoltan, l. 1.1), majd valahol level 890–900 között
magától helyreáll (900-nál json_oldal=899, ismét a főszöveghez hasonló −1-es mintázat).
**Ez nem kiadás-eltérés, hanem az archive.org automatikus oldalszám-felismerő moduljának
hibája ezen a tételen — a `pageNumber` mező level 605–~890 között kb. 3-mal magasabb
értéket ad, mint a nyomtatott oldal.** Bármely további eszköz, amely a `_page_numbers.json`
`pageNumber` mezőjét használja pontos oldalazonosításra ezen a szakaszon, **3-at
vonjon le** belőle, vagy a futófejléc-számjegyet olvassa közvetlenül.

### 2.4 Az oldal 900 utáni szakasz

A minta itt véget ér (a mutatók előtt); a 900-as pont már ismét a főszöveg-mintázatú
(json_oldal = cu_oldal − 1) viselkedést mutatja, összhangban a korábban mért level
890/891 határponttal (l. az eredeti ÁLLJ-jelentés offset-szegmensei), ahol a JSON saját
belső képlete `+12`-ről `+15`-re vált — ez a képlet-váltás időben egybeesik a 3 oldalas
hiba magától való megszűnésével.

---

## 3. A §0.5 hat Abbott-Smith-hivatkozás cremuoft-oldala a konkordancia szerint

| Címszó | cu31924 oldal | cremuoft valódi oldal (konkordancia/futófejléc szerint) | A címszó valóban ott áll-e |
|---|---|---|---|
| ἄβυσσος | 2 | 2 | **igen** — közvetlenül igazolva (O0.6.2b, első ÁLLJ-jelentés) |
| ᾅδης (1.) | 67 | 67 | **igen** — közvetlenül igazolva |
| ᾅδης (2., Supplement) | 610 | **610** (a futófejléc szó szerint ezt írja; a JSON hibásan 613-at adna) | **igen** — l. 1.1 |
| ἐπικατάρατος | 109 | 109 | **igen** — közvetlenül igazolva |
| ἐπικαλέω (1.) | 335 | 335 | **igen** — közvetlenül igazolva |
| ἐπικαλέω (2., Supplement) | 742 | **742** (a futófejléc szó szerint ezt írja; a JSON hibásan 745-öt adna) | **igen** — l. 1.1 |

**Mind a hat anchor pontosan egyezik**, ha a valódi (futófejléc szerinti) oldalszámot
használjuk a `_page_numbers.json` helyett a Supplement-szakaszon. Az eredeti O0.6.2(b)
ÁLLJ tehát **a JSON 2.3 pontban leírt hibájából adódott, nem a két kiadás közötti valódi
oldalszám-eltérésből** — a két kiadás Supplementje ugyanott (oldal ~590) kezdődik, és a
benne lévő szócikkek oldalszáma (legalábbis a két mintavett címszónál) **pontosan
megegyezik** a két kiadás között.

---

## Összegzés és javaslat a folytatásra

1. A cremuoft **`_page_numbers.json` `pageNumber` mezője megbízhatatlan a level ~605–890
   tartományban** (kb. 3 oldallal magasabb értéket ad a valódinál). Az O0.6.3–O0.6.4
   (mintavétel, ellenőrző csomag) és minden további O0.6-tétel, amely oldalszámot jelenít
   meg vagy oldal alapján válogat, **ne a JSON `pageNumber` mezőjét, hanem a level saját
   futófejlécéből olvasott oldalszámot** használja ezen a szakaszon (vagy a JSON értékéből
   vonjon le 3-at, miután a hiba pontos határait — a level 605 és kb. 890 közötti szakaszt —
   megerősítettük).
2. A két kiadás (cu31924 3. angol kiadás, cremuoft 4. angol kiadás) **főszövege és
   Supplementje azonos oldalszámozású** (±1 oldal jitter, ami az automatikus
   horgony-illesztés pontatlanságából ered, nem valódi eltérésből) — a korábbi
   feltételezés, hogy a cremuoft Supplementje sokkal később kezdődne, hibás volt.
3. Javaslat: az O0.6.3 mintavétel és az O0.6.4 ellenőrző csomag futhat tovább, de a
   levél↔oldal leképezéshez (ahol a §0.5-höz hasonló pontos oldalszám kell) a **futófejléc-
   alapú oldatszám-olvasást** kell elsődlegesnek tekinteni a level 605–890 tartományban,
   a JSON-t csak azon kívül.
