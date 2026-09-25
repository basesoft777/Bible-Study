# ELŐKÉSZÍTÉS — cu31924098819406 ↔ biblicotheologic00cremuoft oldalkonkordancia és O0.6.3–O0.6.4

*Negyedik kör (D20): a lapszámozás a két kiadás között ±1 oldal tűréssel egyenértékűnek
számít; az O0.6.3 és O0.6.4 elindult. A `CREMER_OCR_BRIEF.md` nem módosult.*

---

## 0. Fontos helyesbítés a harmadik kör jelentéséhez

A harmadik körben azt jelentettem, hogy a **cu31924098819406 saját `_page_numbers.json`-ja
rendszeresen +1-gyel magasabb** oldalszámot ad, mint az élőfej. **Ez tévedés volt.** A
`cu31924098819406_0035.jp2` és `..._0095.jp2` lapképét ténylegesen megnézve mindkét helyen a
JSON értéke (20, illetve 80) áll nyomtatva — az „élőfej-OCR" (`19`, `79`) egy, a cu31924
2008-as OCR-motorjára jellemző, **magas konfidenciájú, de téves** számjegy-felismerés
(feltehetően `0`↔`9` összetévesztés ebben a betűtípusban). A `_page_numbers.json` tehát a
cu31924-en **megbízható**, nem az élőfej saját OCR-je. A `biblicotheologic00cremuoft`
oldalán viszont a level 625-öt (állítólag „610") ténylegesen megnézve a lapkép **valóban
„610"-et mutat**, míg a cremuoft saját JSON-ja 613-at ad — ott tehát az élőfej a
megbízható forrás, a JSON téved (l. 1. pont). A két tétel más-más OCR-motorral készült, és
egymástól függetlenül, **ellentétes irányban** hibázik.

**Következmény:** a cu31924 oldalszámait mostantól kizárólag a saját `_page_numbers.json`-ja
adja (korrekció nélkül); a cremuoft oldalszámait az élőfej-alapú, simított tábla (1. pont).

---

## 1. Levél–oldal leképezés (végleges, változatlan az előző körhöz képest)

| Level-tartomány (cremuoft) | Oldaltartomány | Eltolás (level − oldal) |
|---|---|---|
| 14–605 | 2–593 | +12 |
| 606–958 | 591–943 | +15 |

A JSON `pageNumber` mezője level 606–890 között kb. 257+30 levélen **+3-mal magasabb**
értéket ad, mint a fenti (élőfej-alapú) tábla — ezt a `cremer_o06_meres.py` `CR_SZAKASZOK`
konstansa korrigálja.

---

## 2. Konkordancia — javított tábla (a 0. pont helyesbítése után)

**A cu31924 oldalát mostantól korrekció nélkül, a saját JSON-jából vesszük.** A horgony:
az oldal felső harmadában lévő szavak (szó-szintű `y`-koordináta) közül 6 egymást követő,
latin betűs szó.

| cu31924 oldal | cremuoft level | cremuoft oldal | eltolás |
|---|---|---|---|
| 20 | 31 | 19 | −1 |
| 40 | 51 | 39 | −1 |
| 60 | 70 | 58 | −2 |
| 80 | 91 | 79 | −1 |
| 100 | 110 | 98 | −2 |
| 120 | 131 | 119 | −1 |
| 140 | 151 | 139 | −1 |
| 160 | 171 | 159 | −1 |
| 180 | 191 | 179 | −1 |
| 200 | 210 | 198 | −2 |
| 220 | 231 | 219 | −1 |
| 240 | 250 | 238 | −2 |
| 260 | 270 | 258 | −2 |
| 280 | 290 | 278 | −2 |
| 300 | 310 | 298 | −2 |
| 320 | 331 | 319 | −1 |
| 340 | 350 | 338 | −2 |
| 360 | 370 | 358 | −2 |
| 380 | 391 | 379 | −1 |
| 400 | 411 | 399 | −1 |
| 420 | 431 | 419 | −1 |
| 440 | 450 | 438 | −2 |
| 460 | 471 | 459 | −1 |
| 480 | 491 | 479 | −1 |
| 500 | 511 | 499 | −1 |
| 520 | 530 | 518 | −2 |
| 540 | 550 | 538 | −2 |
| 560 | 571 | 559 | −1 |
| 580 | 591 | 579 | −1 |
| 600 | 613 | 598 | −2 |
| 620 | 634 | 619 | −1 |
| 640 | 654 | 639 | −1 |
| 660 | 673 | 658 | −2 |
| 680 | 694 | 679 | −1 |
| 700 | 714 | 699 | −1 |
| 720 | 733 | 718 | −2 |
| 740 | 753 | 738 | −2 |
| 760 | 773 | 758 | −2 |
| 780 | 793 | 778 | −2 |
| 800 | 813 | 798 | −2 |
| 820 | 834 | 819 | −1 |
| 840 | 854 | 839 | −1 |
| 860 | 873 | 858 | −2 |
| 880 | 893 | 878 | −2 |
| 900 | 914 | 899 | −1 |

**Az eltolás minden ponton −1 vagy −2** (24 pont −1, 21 pont −2), fokozatosan növekvő
tendenciával a könyv mélyebb pontjai felé (ez arra utal, hogy a cremuoft valamivel
sűrűbben szed, mint a cu31924 — l. a harmadik kör hipotézise). **D20 szerint ez ±1 oldal
tűréssel egyenértékűnek számít**, ezért az O0.6.3/O0.6.4 folytatódik.

### Sorszintű eltolás — kísérő adat (NEM leállási feltétel)

A cremuoft-oldal első törzsszöveg-sorát (az élőfej utáni első klaszter) kerestem meg a
cu31924 teljes sorfolyamában (globális sorindex-számozással); a 45 pontból **20-on** volt
egyedi találat (a többinél a rövid, gyakori szókapcsolat nem volt egyedi, vagy túl kevés
latin szó volt az első sorban):

| cu31924 oldal | cremuoft level | horgony eleje | sor-eltolás |
|---|---|---|---|
| 20 | 31 | messengers who came | 0 |
| 60 | 70 | atoned by the | −40 |
| 100 | 110 | *(kiugró, elvetve — l. lent)* | — |
| 160 | 171 | to give to | −1 |
| 180 | 191 | for the attic | +1 |
| 260 | 270 | the general object | −41 |
| 300 | 310 | to let let | −39 |
| 340 | 350 | himself at the | −40 |
| 360 | 370 | of the measured | −39 |
| 380 | 391 | and also as | −1 |
| 400 | 411 | to esteem or | +1 |
| 440 | 450 | in the that | −39 |
| 480 | 491 | a general opinion | 0 |
| 660 | 673 | and job the | −39 |
| 720 | 733 | other explains to | −40 |
| 760 | 773 | therefore the rendering | −39 |
| 780 | 793 | once with a | −38 |
| 820 | 834 | in the mostly | 0 |
| 860 | 873 | frequently for which | −41 |
| 880 | 893 | of the not | −40 |

Az oldal-100 pontnál a horgony (`from a privative`) egy teljesen más fejezetben, kb.
1261 sorral arrébb adott (hamis) egyedi találatot — rövid, gyakori szókapcsolat, elvetve,
nem vettem be a maximumba. **A többi 19 pont két csoportra esik szét:** ahol az eltolás
kicsi (0, ±1 — ezek egybeesnek a fenti oldalszintű táblázat −1-es pontjaival), és ahol kb.
−39-től −41-ig terjed (ezek a −2-es oldalszintű pontok: a cremuoft-oldal első sora a
cu31924-ben **egy egész oldallal korábban**, annak tetején jelenik meg — konzisztens azzal,
hogy egy nyomtatott oldal kb. 39-41 sorból áll). **Max |sor-eltolás| (a kiugró nélkül): 41**
— ez érdemben nem ad új információt az oldalszintű eltolásokhoz képest, csak ugyanazt
sor-granularitáson igazolja.

---

## 3. O0.6.3 — minta (mag: 20260925)

**Supplement-réteg definíciója (D20-kiegészítés):** a `SUPPLEMENT` címsor oldalától
(level 605, oldal 590/591) a mutatók előtti utolsó oldalig (level 928, oldal 913) tart.
Főrész: level 14–604.

| Level | Oldal | Indok |
|---|---|---|
| 14 | 2 | §0.5 ismert szócikk: ἄβυσσος |
| 79 | 67 | §0.5 ismert szócikk: ᾅδης (1.) |
| 121 | 109 | §0.5 ismert szócikk: ἐπικατάρατος |
| 347 | 335 | §0.5 ismert szócikk: ἐπικαλέω (1.) |
| 625 | 610 | §0.5 ismert szócikk: ᾅδης (2., Supplement) — **egyben a horgonylap-követelmény is** |
| 757 | 742 | §0.5 ismert szócikk: ἐπικαλέω (2., Supplement) — **egyben a horgonylap-követelmény is** |
| 929 | 914 | görög szómutató első levele |
| 949 | 934 | héber mutató első levele |
| 80 | 68 | 12-es minta: főrész 1. fele |
| 182 | 170 | 12-es minta: főrész 1. fele |
| 275 | 263 | 12-es minta: főrész 1. fele |
| 370 | 358 | 12-es minta: főrész 2. fele |
| 531 | 519 | 12-es minta: főrész 2. fele |
| 599 | 587 | 12-es minta: főrész 2. fele |
| 725 | 710 | 12-es minta: Supplement |
| 895 | 880 | 12-es minta: Supplement |
| 919 | 904 | 12-es minta: Supplement |
| 110 | 98 | 12-es minta: görögtoken-sűrű felső negyed |
| 422 | 410 | 12-es minta: görögtoken-sűrű felső negyed |
| 466 | 454 | 12-es minta: görögtoken-sűrű felső negyed |

**Megjegyzés:** a brief-utasítás szerinti „ᾅδης és ἐπικαλέω Supplement-beli szócikkfejét
tartalmazó két level, a 20-on felül" **ugyanaz a két level** (625, 757), amelyek már a
§0.5 hat ismert oldala miatt is a mintában vannak — nem ad új, egyedi levelet, ezért a
**végleges minta mérete 20, nem 22**.

---

## 4. O0.6.4 — ellenőrző csomag

### Sor-klaszterezés szabálya (fontos módszertani javítás)

A nyomtatott sor **nem** az `ocr_line` elem (az egy egész bekezdést fed le, l. korábbi
kör) — szó-szintű `y`-koordinátából klaszterezve: **egymást követő szavak, ha a `y`
(felső koordináta) különbsége ≤ 30 px, egy sorba tartoznak.**

**Validálás 3 véletlen levélen (lapkép vs. klaszterezett sorok száma):**

| Level | Klaszterezett sorok | Lapkép (kézzel számolva) | Eltérés |
|---|---|---|---|
| 14 | 40 | ~39 | 1 |
| 625 | 39 | 39 | 0 |
| 466 | 46 → **41 javítás után** | ~41 | 0 |

A level 466-on **5 hamis klasztert** talált az első futás: a lap jobb szélén (x ≈ 2291–2314
px, a nyomtatott szedéstükör 350–1998 px-es sávján kívül) álló, elszigetelt OCR-morzsák
(feltehetően lapszéli folt/kötésárnyék téves felismerése), amelyek `y`-koordinátája nem
esett egybe egyetlen valódi sorral sem, ezért önálló (5–25 px széles) mini-klasztert
alkottak. **Javítás:** minden 150 px-nél keskenyebb klasztert eldobunk (`SOR_MIN_SZELESSEG`
a `cremer_o06_meres.py`-ban) — a valódi nyomtatott sorok szélessége a teljes szedéstükör
(~1640 px), ez alatt biztosan nem sor. A javítás után mindhárom level ±2-n belül van
(0–1 eltérés), **ÁLLJ nem indokolt**.

### Gyanújel-logika

- **Latin torzkép-gyanú:** a szó nem szerepel az „angol szótárban" (cu31924 hOCR-jében
  `x_wconf ≥ 90` mellett legalább 3-szor előforduló, kisbetűsített, írásjel nélküli latin
  token), **és** a sorban görög karakter, héberkontextus-jelző (`Heb.`, `LXX`) vagy másik
  gyanús latin token is áll.
- **Héberdetektor:** a fenti latin torzkép-gyanú `Heb.`/`LXX` jelzővel egy soron.
- **C5 alakellenőrzés:** a sorban lévő görög szavakra `alak_igazolt_e()` (a meglévő
  `cremer_ocr_javit.py`-ból, változtatás nélkül importálva) — nincs találat → `c5_nem_igazolt`
  jelzés (ez **nem hiba**, csak jelölés, l. a brief C5 pontja).

### Eredmény

- **Minta:** 20 level (l. 3. pont).
- **Megjelölt sor** (görög karakter, latin torzkép-gyanú vagy héberdetektor-találat van
  rajta): **604**.
- **ATNEZES-oldalak:** **13** (`naplok/CREMER_O06_ellenorzes/ATNEZES_01.md` … `_13.md`,
  50 sor/oldal, az első oldal tetején a brief O0.6.4 ítéletkód-listájával).
- **Kísérő fájlok:** `naplok/CREMER_O06_ellenorzes/sorok.tsv` (604 sor + fejléc, `csv`
  modul nélkül, tab-elválasztva), `naplok/CREMER_O06_ellenorzes/kepek/` (604 JPEG kivágás,
  soronként, legfeljebb 1000 px széles).
- Az ítéleteket a felhasználó tölti ki.

---

## Ellenőrzés a commit előtt

- `lexikon/`, `adat/`, `tematikus_lezart/`: nem érintett.
- `konkordancia/_nyers/`: egyik fájl sincs staged állapotban.
- Az egyetlen új/módosult tétel: `eszkozok/cremer_o06_meres.py`,
  `naplok/CREMER_O06_ellenorzes/` (ez a fájl, `ATNEZES_01-13.md`, `sorok.tsv`, `kepek/`).
