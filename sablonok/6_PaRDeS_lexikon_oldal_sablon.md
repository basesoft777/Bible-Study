# 6. PaRDeS lexikon-oldal sablon (Motívumlexikon-pilot alapján)

*v3 — 2026.09.22 (LEXV2_2): a TUDOMÁNYOS változat oldalszerkezete
lexikon-oldal v2-re váltott (LEXV2_2_BRIEF.md G1). Az `LXX_OS` bekötve
a régi `LXX_kivonat_*.tsv` helyett (3. szakasz), a Thayer-szótár
kirakva (2. szakasz), az UBS-szótár (Louw–Nida) bekötve az ÚSZ-i
Strong-tokenekre (1. szakasz). A generátor a Tartalomjegyzéket, a
Jelmagyarázatot, az 1., 1/b., 2., 3., 4., 5., 8. szakaszt és a Kolofont
írja marker-blokkokként; a köztük álló szakaszok kézzel írandók, és a
generátor nem nyúl hozzájuk. Minden generált blokk markere licenc-mezőt
visel — l. „Licenc és nyilvános repó" alább. A lenti A) szakasz ennek
megfelelően frissült; a B) OLVASHATÓ változat és a közös szabályok
tartalmilag változatlanok maradtak.*

*v2 — 2026.09.19/20 (F6_BRIEF.md: a TUDOMÁNYOS változat mostantól
generált vázból és kézi szakaszokból áll — `eszkozok/lexikon_general.py`,
`python eszkozok/general.py --cel lexikon --ir`, célfájl
`lexikon/[ID]_TUDOMANYOS.md`. A generátor a 0., 1., 2., 3., 4., 5. és 9.
szakaszt írja marker-blokkokként; a köztük álló szakaszok kézzel
írandók, és a generátor nem nyúl hozzájuk. Minden generált blokk
markere licenc-mezőt visel — l. „Licenc és nyilvános repó" alább. A
lenti A) szakasz ennek megfelelően frissült; a B) OLVASHATÓ változat és
a közös szabályok tartalmilag változatlanok maradtak. — archív, l. a v3
bejegyzést fent.)*

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
"lexikon-nézeteként". A TUDOMÁNYOS változat generált váza automatikus
(`general.py --cel lexikon`), de csak akkor fut le értelmesen, ha az
alábbi előfeltétel teljesül — a kézi szakaszok (1/b, "Miért fontos ez a
lelet", Minősítés, Alátámasztás, Módszertani napló, Nyitott kérdések)
továbbra is felhasználói jóváhagyás után, motívumonként egyesével
íródnak.

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

| Fájl | Cél | Hossz-jelleg | Előállítás |
|---|---|---|---|
| `lexikon/[MOTÍVUM-ID]_TUDOMANYOS.md` | Teljes, minden forrást szó szerint idéző referencia-lap | Hosszú, táblázatos | **generált váz + kézi szakaszok** (`general.py --cel lexikon --ir`) |
| `[MOTÍVUM-ID]_OLVASHATO.md` | Rövid, prózai, nyomtatható változat | Rövid, folyó szöveg | **kézi**, motívumonként |

Ez nem opcionális kettősség — a `Bibliai_Motivumlexikon_tervezesi_
naplo.md` 12. pontja ("a motívumnaplónak önmagában is, adatbázis-
lekérdezés nélkül olvashatónak kell maradnia, akár nyomtatható
formában is") kifejezett tervezési elv, amit ez a két fájl valósít
meg.

**Könyvtár:** a TUDOMÁNYOS változat éles helye `lexikon/`
(`[MOTÍVUM-ID]_TUDOMANYOS.md`); az OLVASHATÓ változat helye egyelőre
szintén ott íródik, motívumonként kézzel. A `motivumlog/lexikon_pilot/`
**csak archívum** — az ISTENTISZT-001 és KIRALY-001 pilot-fájljai ott
maradnak, a generátor nem nyúl hozzájuk, és nem a jelenlegi folyamat
bemenete vagy kimenete (F6_BRIEF.md K17).

---

## A) TUDOMÁNYOS változat — kötelező szakaszok, pontos sorrendben

A sorrend és a címek a generátor fájlváza szerint kötöttek
(`eszkozok/lexikon_general.py` `VAZ_SABLON`, LEXV2_2_BRIEF.md G1).
Minden szakaszcím **(generált)** vagy **(kézi)** jelöléssel: a
**(generált)** szakasz tartalma a `general.py --cel lexikon` GENERÁLT-
marker-blokkja, kézzel nem szerkeszthető (a szerkesztés a legközelebbi
futtatáskor felülíródik); a **(kézi)** szakaszt a generátor nem érinti.

### `# 📖 ID — cím` + Kivonat (kézi)
A motívum ID-je és teljes címe fejlécként, alatta egy rövid (3-5
mondatos) prózai kivonat: mi a motívum, milyen azonosság-típusú, hány
igehelyen, mi a legfontosabb lexikai lelet.

### Tartalomjegyzék (generált)
A lenti szakaszok listája horgony-linkekkel (`[1. Előfordulások](#1-elofordulasok)`
stb.), a kézi szakaszokat is beleértve (üresen is felsorolva, ha még
nincs megírva).

### Jelmagyarázat és rövidítések (generált, közös szöveg)
Közös, minden oldalon szó szerint azonos blokk: a funkció-jelek
jelentése a `SEMA.md` funkció-értékkészletéből, a PaRDeS-szintek a
`PaRDeS_gyorsreferencia.md`-ből idézve (nem újrafogalmazva), és a
rövidítés-lista a használt forrásokat adja teljes névvel (BDB, TBESH,
TBESG, Thayer, UBS, L–N = Louw–Nida, SDBH, SDGNT, OSHL, TWOT, TSK, KH =
Károli-kereszthivatkozás, LXX, MT, KJV). Kötelező mondat: „A szótári
fordításokban a πνεῦμα (pneuma) mindig *szellem*, a ψυχή (pszükhé)
*lélek*; a Károli-idézetek szövege változatlan (pl. »Lélek«)."

### 1. Előfordulások (generált)
Tábla: Igehely | Kulcsszó (Károli-szó + eredeti szóalak **kiejtéssel**,
a `TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv` `Kiejtés` oszlopából) |
Funkció | PaRDeS-szint | Strong | Szótári jelentés | UBS-jelentés
(csak ÚSZ-sornál, `L–N kód — magyar definíció` alakban, a magyar
szöveg az `adat/forditas_ubs.tsv`-ből; hiányzó fordításnál az angol
eredeti `fordítás függőben` jelöléssel; `egyertelmu=nem` esetén minden
jelölt jelentés felsorolva) | Megbízhatóság · azonosítás módja. Az
igehely horgony-link az 1/a alszakaszra mutat. A `proveniencia` és az
`igazolas` a tábla alatti számozott lábjegyzetben.

#### 1/a. Az igehelyek szövege (generált)
Igehelyenként: horgony (`<a id="...">`), a Károli-vers szó szerinti
szövege (`Karoli_1908.tsv`-ből; tartomány esetén minden vers külön), és
alatta a `kapcsolodas` mező szövege.

### 1/b. Kizárt és vizsgált helyek (generált)
A `jeloltek.tsv` `elutasítva` és `nyitva` sorai indoklással, plusz a
`motivumok.tsv` `negativ_kriterium` mezője. A `beépítve` státuszú
jelöltek itt nem jelennek meg (azok az 1. szakaszban vannak).

### 2. Szótári háttér (generált)
A motívum minden Strong-tokenjére egy `###` alszakasz: TWOT-szám (ha
héber), szemantikai domén (SDBH/SDGNT), és a `lexikon_hivatkozasok.tsv`
minden hozzá tartozó sora — szótáranként és jelentés-számonként
alszakaszban, a forrásfájl megfelelő sorának **szó szerinti kivonatával**
(`szoveg_en`), alatta a magyar fordítással (`forditas_hu`, ha van,
egyébként `fordítás függőben` jelöléssel) és a forrásfájl
megjelölésével. **Ha egy szóhoz TÖBB szótár is elérhető** (pl. TBESG
ÉS Thayer), mindegyik saját `####` alszakaszban, egymás után jelenik
meg — ez a `lexikon_hivatkozasok.tsv` szótárankénti sorai szerint
automatikus, nem kézi döntés.

**Új jelentés felvétele:** ha egy motívum-token jelentés-hivatkozása
hiányzik vagy hiányos, az **nem** a lexikon-oldalon pótlandó, hanem az
`adat/lexikon_hivatkozasok.tsv` táblában — új sorral, a `szoveg_en`
mezőben a forrásfájl szó szerinti kivonatával és a `forditas_hu`
mezőben a magyar fordítással (l. `adat/SEMA.md` 2.5). A generátor
következő futtatása ezt automatikusan megjeleníti a szócikk-blokkban.

#### 2/b (kézi, ha van)
Kézzel írandó kiegészítés, ha a forrás-study pilotjában volt "Teljes
szótári anyag" jellegű bővítés, ami a generált szócikk-blokkon felül
indokolt.

#### Miért fontos ez a lelet (kézi)
Minden többforrásos szócikk-alszakasz után kötelező egy bekezdés, ami
kimondja: mit ad hozzá a második/harmadik forrás, amit az első
önmagában nem adott — vagy explicit jelzi, ha nem ad hozzá semmi újat.

### 3. LXX-fordítói döntések (generált)
Az `LXX_OS`-ből épül (a régi `LXX_kivonat_*.tsv` nem tartozik a
generált réteghez). Minden ÓSZ-előfordulás-sorra (tartománynál minden
versre) egy sor: Igehely (Károli) | LXX-igehely | Héber kulcsszó
(kiejtéssel) | Görög megfelelő (ékezetes szóalak, lemma, átírás,
G-szám) | Egyezés | Forrás. **Egyezés** = a motívum saját G-tokenje
előfordul az LXX-versben (`egyező`). Ha nem: az `adat/lxx_dontesek.tsv`
sora adja a görög megfelelőt (`eltérő`); ha ott sincs sor:
`kutatói azonosítás függőben`. Automatikus héber→görög tippelés nincs.
Ha a vers Károli-igehelye az `LXX_OS`-ben üres (`szamozas_elteres`), a
sor ezt kiírja, üres görög mezővel. Ha a motívumnak nincs ÓSZ-i
előfordulása, ezt a blokk explicit jelzi, tábla nélkül. Licenc:
CC BY 4.0 (lxx-morph, GreekWordList).

### 4. Kereszthivatkozások (generált)
A négyforrásos módszertan (`PaRDeS_gyorsreferencia.md`) szerinti,
**minden** vizsgált igehelyre lefuttatott TSK (Votes ≥ 15 szűréssel) és
Károli-KH eredmény, igehelyenkénti bekezdésekben, Károli-formátumban
írt igehelyekkel (`Zsolt 50:15`, nem `Zsolt 50,15`); a versenkénti
kereséssel nem vizsgálható igehelyek felsorolva a blokk végén.

#### Minősítés (kézi)
Igehelyenként/találatonként: független megerősítés / új találat / nem
releváns — indoklással. A hamis nyomok dokumentálása ugyanolyan
fontos, mint a találatoké.

### 5. Kapcsolatok (generált)
Elöl a tábla: Forrás | Cél | Típus | Funkció | Bizonyosság |
PaRDeS-szint — a `kapcsolatok.tsv` sorai szerint. Alatta, `<details>`
blokkban, a **Mermaid `graph LR` diagram** (minden érintett igehely
legalább egy élen szerepel). Ha nincs kapcsolat-sor a motívumhoz, ezt a
blokk explicit jelzi.

#### Alátámasztás (kézi)
A kapcsolatok táblájának MINDEN sorára: miért ez a funkció-címke, miért
ez a bizonyossági szint (Magas/Közepes/Alacsony), konkrét szövegi
indoklással (szó szerinti idézés vs. parafrázis vs. csak lexikai
egyezés). Ha egy eset nem fér bele a Forrás-igehely/Cél-igehely
kétpontos modellbe (pl. egy versen belüli kontraszt), ezt itt explicit
ki kell mondani, és jelezni a nyitott tervezési kérdést.

### 6. Értelmezés (kézi)
A forrás-study "3. A PaRDeS keretrendszer" szakasza (Peshat/Remez/
Drash/Sod, a motívum egészére alkalmazva) átemelendő, és **bővítendő**
minden olyan lexikai felismeréssel, amit a 2. szakasz többforrásos
lexikon-idézése hozott (pl. ha több forrás egybehangzóan megerősít egy
értelmezést, vagy egy forrás explicit jelentés-megkülönböztetést
tartalmaz, ami a Remez/Drash rétegek valamelyikét alátámasztja). A
bővítés a Remez és/vagy Drash rétegbe kerül (nem a Peshat vagy Sod
rétegbe, hacsak a lelet nem kifejezetten ott indokolt) — a Sod réteg
fegyelmezettsége külön kiemelendő indoklással védendő új adat esetén
is. Stílus: törekedjen közérthetőségre a tisztán tudományos leírás
helyett is, különösen a bővítő bekezdésekben — a cél, hogy a lelet
jelentősége ne csak szakértő olvasó számára legyen világos.

Ide kerül a régi "ÚJ FELISMERÉS" szakasz is, ha van: ha a lexikon-oldal
elkészítése közben olyan felismerés születik, ami **nincs** még a
tematikus study-ban, ezt **külön, explicit jelölt alszakaszként** kell
felvenni, a szakasz elején kötelező figyelmeztetéssel: *"Ez a szakasz
kizárólag a lexikon-oldalon rögzített megfigyelés — a
`[Motívum]_tematikus.md` fájlba szándékosan NEM került be, amíg külön
döntés nem születik róla."* A szakasz végén kötelező egy "Amit ez a
felismerés NEM állít" bekezdés és egy "Nyitott kérdés a folytatáshoz"
bekezdés.

### 7. Módszertan és nyitott kérdések (kézi)
Táblázat: # | Módszer | Eredmény — a study elkészítésekor futtatott
összes ellenőrzési réteg, tömören összefoglalva. Alatta egy mondat, ami
a teljes indoklás helyére mutat (chat-napló dátuma,
kereszthivatkozás-napló fájlneve).

Ide kerül a régi "Nyitott kérdések és séma-korlátok" szakasz is:
számozott lista — minden, ami a fenti szakaszokban "nyitva" maradt
(funkcionális besorolás hiánya, séma-korlát, forrás hiánya stb.), egy
helyen összegyűjtve. Lezárt tételek áthúzva (`~~...~~`) megtarthatók,
dátummal, ha időközben megoldódtak — ne töröld, hogy látszódjon a
folyamat.

### 8. Irodalom és idézés (generált)
„Hogyan hivatkozz" alszakasz (ID, cím, `statusz_verzio`,
`statusz_datum`, a generálás dátuma, a fájl GitHub-URL-je), alatta a
felhasznált szótárak listája a forrás-README-k szerinti teljes
megnevezéssel. A teljes szakirodalmi bibliográfia-tábla nem ennek a
menetnek a tárgya (LEXV2_3).

### Kolofon (generált)
Tábla: ID | Rövid UI-címke | Teljes cím | Téma | PaRDeS-szint | Státusz
| Azonosság típusa | Negatív kritérium | Fölérendelt fogalom |
Forrás-study | Kereszthivatkozás-napló | Sablon-megfelelőség — a
`motivumok.tsv` sora szerint. Alatta tábla: Forrás | Fájl | Licenc |
Blokk — a fájlban ténylegesen felhasznált forrásfájlok, fájlonkénti
licenc-hozzárendeléssel. L. "Licenc és nyilvános repó" alább.

---

## Licenc és nyilvános repó (kézi)

**A repó nyilvános marad.** Minden generált marker-blokk fejléce
(`<!-- GENERÁLT-KEZDET: … | forrás: … | licenc: … | ts=… -->`) a
blokkban ténylegesen felhasznált források licenceinek rendezett,
egyedi halmazát viseli; a Kolofon táblája ugyanezt forrásfájlonkénti
bontásban ismétli meg. Gépi kereséssel (`grep "licenc:.*tisztazatlan"`)
mindig visszakereshető, mely oldal melyik blokkja épül tisztázatlan
licencű forrásra.

**Thayer (közkincs, LEXV2_2 G4).** A `Thayer_teljes.tsv` közkincs
(public domain) forrás — a 13 görög Strong-tokenhez tartozó
`lexikon_hivatkozasok.tsv`-sorai a 2. szakaszban `licenc: kozkincs`
jelöléssel jelennek meg, nem `tisztazatlan`-ként.

**LXX (`LXX_OS`, CC BY 4.0, LEXV2_2 G5).** A 3. szakasz kizárólag az
`LXX_OS`-t (lxx-morph + GreekWordList, CC BY 4.0) olvassa. A régi
`LXX_kivonat_*.tsv` **nem** része a generált rétegnek — sem a 3.
szakaszban, sem máshol nem jelenik meg hivatkozásként.

**Tisztázatlan licencű források** (D9, F6_BRIEF.md 2. pont 8. sora):
az `LSJ_teljes.tsv`, a `SECE_*` fájlok és az `MCGED.lexicon`
**bekerülnek** a generált rétegbe — idézhetők, ugyanúgy, mint a
jogtiszta források —, de minden blokk, amely ilyet olvas, a
markerében és a Kolofon táblájában `tisztazatlan` licencet visel. Ha a
döntés később megfordul, a jelölés miatt gépileg visszakereshető, mely
oldal melyik blokkja érintett (l. Döntésnapló D9, N4, N5).

**TWOT-szabály:** a lexikon-szócikk csak a TWOT-**számot** idézi (az
`OSHL_lexikalis_index.tsv`-ből, CC BY 4.0), a TWOT szócikk **szövegét**
sosem — a TWOT-nak nincs jogtiszta forrása a repóban (D7).

---

## B) OLVASHATÓ változat — kötelező szakaszok, pontos sorrendben

**MEGSZŰNT (2026.09.21, felhasználói döntés):** a lexikon-oldalnak csak az A) TUDOMÁNYOS változata készül. Ez a szakasz csak archív referencia.

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

**Napló-jelölés kötelező:** minden folyamat-/napló-jellegű megjegyzést
(dátum, forrás-eredet, döntési indoklás) `【NAPLO: ...】` formában, külön
egységben kell rögzíteni — sosem prózai mondatba ágyazva. Részletek:
`PaRDeS_gyorsreferencia.md` "Napló-jelölés" szakasza.

**Konkrét, ismétlődően előforduló triggerek** (2026.09.09-i
ISTENTISZT-001 átfésülésből, nem kimerítő lista — ha valami ebbe a
mintába esik, de nincs felsorolva, akkor is NAPLO-ba kerül):
- inline `*(új, dátum)*` vagy `*(dátum, eredet)*` tag egy táblázat-
  cellában vagy mondatba ágyazva — a dátum/eredet a NAPLO-ba kerül,
  a tartalmi cella/mondat tisztán marad
- bold `**Forrás:**` vagy dőlt `*(Forrás: ...)*` sor futószövegben —
  ehelyett `【NAPLO: forrás — ...】`
- első/többes szám első személyű ellenőrzési állítás ("ellenőriztem",
  "ellenőriztük", "találtuk", "megnéztük") tartalmi mondatba ágyazva —
  a tartalmi következtetés marad a mondatban, az ellenőrzés ténye
  NAPLO-ba kerül
- üzemeltetői/pipeline-stílusú státuszjelzés egy tartalmi cellában
  (pl. "csak részlegesen ellenőrizhető", "hiba miatt" egy adat
  minőségi állapotára utalva) — a cella a **tartalmi tényt** írja le
  (mit mond a szöveg), nem az adatfeldolgozás állapotát

**Formázási szabály:** minden `【NAPLO: ...】` blokk saját, elkülönülő
bekezdés — üres sor kötelezően közvetlenül elé (kivéve, ha a NAPLO egy
felsorolás/idézet-blokk közvetlen folytatása, és ez így egyértelműbb).

**Idézés-formázási szabály:** blockquote (`>`) csak az eredeti nyelvű
(héber/görög/latin) szövegre vonatkozik; a magyar fordítás **mindig**
normál bekezdés, közvetlenül az idézet után, nem a blockquote
folytatásaként.

**TUDOMÁNYOS-hangnem szabály:** a TUDOMÁNYOS változat semleges,
harmadik személyű előadásban íródik — nincs benne olvasót megszólító
vagy "mi"-hangú fogalmazás (pl. "hadd fogalmazzam egyszerűbben", "ha
csak a mi olvasatunk lenne", "tőlünk függetlenül"). Ez a casual
regiszter az OLVASHATÓ változatnak van fenntartva, ott is csak
mérve.

**PaRDeS-réteg fegyelem:** egy réteg (Peshat/Remez/Drash/Sod)
tanítása nem "mélyíthető" vagy egészíthető ki közvetlenül egy másik
réteg elemzési eszközével (pl. a KAPCSOLATOK-réteg A/B/C tipológiája
nem válik a Drash-tanítás részévé). Ha a rétegek között valódi
kapcsolat van, azt külön, a másik réteg nevével explicit megjelölve,
keresztre hivatkozva kell megadni ("(Remez-szintű kiegészítés, l. X.
pont)"), nem összeolvasztva a befogadó réteg saját mondatával.

## Minőségi kapu — a két fájl közzététele/commitolása ELŐTT
futtatandó

A `4_PaRDeS_tematikus_sablon.md` Minőségi kapujából adaptálva, a
lexikon-oldal saját kockázataira szabva:

- [ ] **L1. Szerkezeti teljesség** — a TUDOMÁNYOS változat mind a 13
      kötelező szakasza jelen van (cím+Kivonat, Tartalomjegyzék,
      Jelmagyarázat és rövidítések, 1. Előfordulások + 1/a, 1/b. Kizárt
      és vizsgált helyek, 2. Szótári háttér [+2/b és Miért fontos ez a
      lelet, ha van], 3. LXX-fordítói döntések, 4. Kereszthivatkozások
      + Minősítés, 5. Kapcsolatok + Alátámasztás, 6. Értelmezés, 7.
      Módszertan és nyitott kérdések, 8. Irodalom és idézés, Kolofon —
      LEXV2_2_BRIEF.md G1), és az OLVASHATÓ változat mind a 7 kötelező
      szakasza jelen van. Utólagos szerkesztésnél külön ellenőrizendő,
      hogy egy korábban meglévő szakasz nem maradt-e ki.
- [ ] **L3. Lexikai vs. tematikus kapcsolat szétválasztva** — minden
      forrás-hivatkozás, ami nem a motívum saját Strong-számán/szaván
      keresztül kapcsolódik, hanem csak fogalmilag (pl. egy másik
      motívum auditjából átvett, kategória-szintű párhuzam), explicit
      "tematikus, nem lexikai" jelöléssel szerepel.
- [ ] **L4. Kereszt-motívum szennyeződés kizárva** — a lexikon-oldal
      kizárólag a saját motívumára (a fájlnévben szereplő
      MOTÍVUM-ID-ra) vonatkozó leleteket tartalmazza. **Külön
      ellenőrizendő**, hogy egy másik motívum auditjából (pl. egy
      másik `[MOTÍVUM-ID]_TUDOMANYOS.md` vagy egy másik tematikus
      study feldolgozása közben talált lelet) nem került-e át ide
      névtévesztéssel vagy figyelmetlenségből — ez a hiba már
      ténylegesen előfordult (2026.09.07, Zakariás 6:13/Melkizedek-
      lelet egy ISTENTISZT-001 mintaoldalon).
- [ ] **L5. Nevesített tanítói szakasz átvéve** — ha a forrás-study
      5. pontja tartalmaz nevesített tanítói egyezés-keresést, az a
      lexikon-oldalon is szerepel (jelenleg nincs kötelező szakaszként
      nevesítve a fő struktúrában — ha hiányzik, ez önmagában nem
      buktatja a kaput, de jelezni kell a Nyitott kérdések
      szakaszban).
- [ ] **L6. Napló-/formázási-/hangnem-fegyelem** — nincs a fájlban:
      (a) inline dátum/eredet-tag tartalmi cellában/mondatban; (b)
      bold/dőlt "Forrás:" sor futószövegben; (c) első személyű
      ellenőrzési állítás tartalmi mondatba ágyazva; (d) 【NAPLO】 blokk
      üres sor nélkül a szövegtől; (e) magyar fordítás blockquote-ban
      (csak az eredeti nyelvű idézet lehet ott); (f) olvasót
      megszólító/"mi"-hangú mondat a TUDOMÁNYOS változatban; (g)
      egy réteg elemzési eszköze egy másik réteg tanításába
      összeolvasztva, keresztre hivatkozás nélkül. Részletek: l. a
      "Napló-jelölés kötelező" bekezdés.

Ha L1, L3, L4 vagy L6 bármelyike bukik, a lexikon-oldal NEM tehető
közzé/commitolható, amíg nincs javítva.

---

*A két fájl elkészítése előtt belső önellenőrzés fut le: megvan-e a
lezárt tematikus study, a négyforrásos módszertan lefutott-e minden
igehelyre (nem csak mintavétellel), és a lexikai/tematikus
kapcsolatok explicit el vannak-e választva egymástól.*
