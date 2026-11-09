# 6. PaRDeS lexikon-oldal sablon (Motívumlexikon-pilot alapján)

*v4 — 2026.11.08 (F178): az új lapszerkezet és a HAMART-001 regressziós kapui — a fájl végén, „Az új lapszerkezet és a HAMART-001 regressziós kapui”.*

*v3.1 — 2026.11.02 (F123.3, DT546, DT547): az 1/a igehelyenként a `kapcsolodas` kerek mondata alatt a „Funkció:” sort is mutatja (DT-F1Ab); a két mező kötelező formáját a `9_PaRDeS_motivum_forras_sablon.md` 4. pontja rögzíti. A Minőségi kapu kiegészül az L8 ponttal (24., 25. szabály, olvasói kapu, a felhasználó vizuális átnézése). A kapu többi pontjának elavulása (OLVASHATÓ, törzscikk) változatlanul nyitott: N-F10a.*

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
Az alábbi **(generált)** / **(kézi)** jelölés ennek a sablonnak a
munkajelölése, **a lapon nem áll** (F123.GENKOR, DT603): a
**(generált)** szakasz tartalma a `general.py --cel lexikon` GENERÁLT-
marker-blokkja, kézzel nem szerkeszthető (a szerkesztés a legközelebbi
futtatáskor felülíródik); a **(kézi)** szakasz törzse a motívum kézi
forrásából jön, a lapon nem szerkeszthető. A lap címsorai jelölés
nélküliek; a szerzőséget a Kolofon mondata adja (l. ott). Az olvasói
kapu a „(kézi)” / „(generált)” jelölést a lapon belső jelnek veszi
(BELSO, BUKÁS).

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
Tábla: Igehely | Kulcsszó (Károli-szó + eredeti szóalak magyaros **kiejtéssel**; nem a TAHOT/TAGNT angolos átírása, l. „Kiejtés és olvasói szöveg”) |
Funkció | PaRDeS-szint | Strong | Szótári jelentés | UBS-jelentés
(csak ÚSZ-sornál, `L–N kód — magyar definíció` alakban, a magyar
szöveg az `adat/forditas_ubs.tsv`-ből; hiányzó fordításnál az angol
eredeti `fordítás függőben` jelöléssel; `egyertelmu=nem` esetén minden
jelölt jelentés felsorolva) | Megbízhatóság · azonosítás módja. Az
igehely horgony-link az 1/a alszakaszra mutat. A `proveniencia` és az
`igazolas` a tábla alatti számozott lábjegyzetben.
*Arany lap (ISTENTISZT-001, F131; a többi lapra a kiterjesztés külön
feladat):* a „Szótári jelentés” helyén „Jelentés (a szó)” áll (a szótári
szakasz címkéje és jele, `adat/szotar_szakasz_cimke.tsv`; a címke forrása
a sor lábjegyzetében; a lábjegyzet-jel mellett külön ⓘ nem áll), mellette „Funkció (a motívumban)” (ikon/emoji nélkül, csak a címke szövege); az
„UBS-jelentés” ÓSZ-sornál is kitöltött: az UBS DBH igehelyszintű
jelentése tokenenként (csak a definíció szövege, a 15 jegyű kód nem látszik, az adatban marad; magyarul, ahol van, különben
az angol `(fordításra vár)` jelöléssel; hivatkozás híján kimondott hiány).
A „2. Szótári háttér” a szótári gerinccel kezdődik (SEMA 2.40).

#### 1/a. Az igehelyek szövege (generált)
Igehelyenként: horgony (`<a id="...">`), a Károli-vers szó szerinti
szövege (`Karoli_1908.tsv`-ből; tartomány esetén minden vers külön),
alatta a `kapcsolodas` mező szövege (legalább egy kerek mondat), és
`Funkció:` sor (mindig új bekezdésben, a renderelt nézetben is új sorban) a `funkcio` mező „ — ” utáni részéből (DT-F1Ab). A két
mező kötelező formája és a minta (ISTENTISZT-001, 1Móz 4:26):
`9_PaRDeS_motivum_forras_sablon.md` 4. pont; mérője a 25. szabály.

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

### 5/b. Kapcsolódó motívumok (generált)
*(DT277 (α), #127.)* Az `adat/motivum_kapcsolatok.tsv` sorai, amelyekben
a motívum az egyik fél (SEMA 2.33): a másik motívum (hivatkozással a
lapjára), az igehely-pár, típus, funkció, bizonyosság, PaRDeS-szint,
indoklás; a sor mindkét motívum lapján megjelenik. Minden sor mögött
`beépítve` motívumközi jelölt áll a `jeloltek.tsv`-ben (2. szabály). A
döntésre váró motívumközi jelöltek csak számként szerepelnek. Kapcsolat
nélkül kimondott hiánymondat. A törzscikkben nem jelenik meg (D34). A
motívumközi kapcsolatról szóló próza nem ide, hanem később az
`ertelmezes` résbe kerül.

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

### 6/b. Alkalmazás és tanítói egyezés (kézi)
*(DT276, #127.)* Két rés egy szakaszban, a 6. Értelmezés után (a
szakaszszámozás nem tolódik, az „1/b.” mintájára):

- **Alkalmazás és tanítványság** (`alkalmazas` rés) — a motívum kézi
  forrásának „5. Alkalmazás és tanítványság” pontja (az alkalmazási
  kérdések), a forrásban `<!-- RÉS-KEZDET: alkalmazas -->` jelölők közt.
- **Tanítói egyezés** (`tanitoi` rés) — a 7. lépés saját fájljának
  (`motivumok/naplok/[ID]_tanitoi_kereses.md`) „Összegzés” szakasza,
  `<!-- RÉS-KEZDET: tanitoi -->` jelölők közt.

A még nem migrált motívumnál mindkét rés rögzített átmeneti mondatot
hordoz (`adat/res_forras.tsv`, `forras=adat`); a jelölőket a #123
ciklusai teszik a forrásba. A törzscikkben a szakasz nem jelenik meg
(D34).

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

### Kiejtés és olvasói szöveg (kézi szabály)

Az előfordulás-tábla „Kulcsszó” cellájában a Károli-szó mellett az eredeti szó **magyaros kiejtése** áll (nem a TAHOT angolos átírása: *k.Ro'*, *Shem* helyett héberül a lemma magyaros kiejtése, görögül gépi magyaros). Szó szerinti szótári idézetben nincs kiejtés. „Gépi” jelölés a kiejtés mellett nem áll.

Minden olvasói magyarázó szöveg **a lelettel kezdődik** (számok, konkrét szavak kiejtéssel, példahely), és **szabály szerinti következtetéssel zárul**. A következtetés determinisztikus, az adatból számolt szabály (küszöb, arány), a kódban (`eszkozok/olvasoi_kovetkeztetes.py`) és a lap üzemeltetői sorában rögzítve; új blokknál a függvényt oda kell felvenni. Belső szakszó (gerinc, szerep) nem kerül olvasói szövegbe: a motívum saját szavait nevezzük meg. *(A felhasználó: „mindig vanjuk le a következtetést a találtakból . a magyarázó szöveg az adatokból induljon.”)*

### Kolofon (generált)
Tábla: ID | Rövid UI-címke | Teljes cím | Téma | PaRDeS-szint | Státusz
| Azonosság típusa | Negatív kritérium | Fölérendelt fogalom |
Forrás-study | Kereszthivatkozás-napló | Sablon-megfelelőség — a
`motivumok.tsv` sora szerint. Alatta tábla: Forrás | Fájl | Licenc |
Blokk — a fájlban ténylegesen felhasznált forrásfájlok, fájlonkénti
licenc-hozzárendeléssel. L. "Licenc és nyilvános repó" alább.
A Kolofon a **kiadás** sorát is viseli: kiadásszám (1 = a generált első lap) és változásjegyzék (kiadás | dátum | mi változott). **Forrása az `adat/kiadasok.tsv`** (SEMA 2.46, DT492): a kiadásszám a motívum legnagyobb `kiadas` értéke, a változásjegyzék a motívum sorai; motívum sora nélkül a kolofon nem ír kiadás-sort. A kolofont kézzel szerkeszteni tilos, a sor a táblába kerül. **Lezáráskor** (`MUNKAMENET.md` C5: a Feed mind a 9 kapuja zöld, DT547) ide kerül az **1. kiadás** sora (`kiadas=1`); a további kiadások és a helyi javítások sorát a `/kiadas <ID>` és a `/lap-javit <ID>` írja (SEMA 2.46, 2.49; `MUNKAMENET.md` C5, C-k, C-j). A `/lap-javit` naplójából (`adat/lap_javitasok.tsv`) generálódik a Kolofon **„Emberi lektorálás”** sora („N hely (dátumok); lektorálók: …”, a nem generátor típusú sorokból); sor nélkül a sor nem áll (DT599).
A Kolofon rögzíti a **próza modelljét** is: a tényleges modellnevet (pl. `claude-opus-5-5`), a CLAUDE.md modell-szabálya szerint a futó környezetből, nem briefből másolva; ez teszi ellenőrizhetővé, hogy a `/kiadas` lektora (`.claude/agents/lektor.md`) a prózát író modelltől eltér (DT473).
A Kolofon első sora a **szerzőségi mondat** (F123.GENKOR, DT603), adatból: az értelmező szakaszok neve (`adat/res_forras.tsv`, `tanulmany` forrású rések), a legutóbbi kiadás `proza_modell`-je és az átnézés (`adat/lap_atnezesek.tsv`), pl. „Az értelmező szakaszokat (Kivonat, …, Módszertan) mesterséges intelligencia (`claude-opus-5-5`) írta az adatok alapján; a szerző átnézte és jóváhagyta. A többi szakasz az adattáblákból generált.” `manual` modellnél a mondat azt mondja, hogy a kiadás nem rögzít modellnevet; kiadás nélkül azt, hogy a szakaszok még nincsenek kiadva.

**Strong-szám az olvasói prózában** (DT602): ahol a héber/görög szó mellett a kiejtés és a Strong-szám áll, a forrás „(מִזְבֵּחַ, mizbéah, H4196)” alakja a generátor bemenete; a lapon a kiejtés a szónézetre mutató hivatkozás, a Strong-szám kis, halvány felső index, egér alatt a szám és a rövid jelentés (`[mizbéah](/szo/H4196)<sup class="strong" title="H4196 · oltár">H4196</sup>`), nyomtatásban a halvány felső index. A csupasz, zárójeles szám a lapon hiba (olvasói kapu, BELSO).

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
- **Kiejtés.** A görög és a héber szó kiejtése szakaszonként (két `##`/`###` cím között) az **első előfordulásnál** kötelező, továbbá **minden címsorban és táblázatfejben**; ugyanabban a bekezdésben ugyanarra a szóra nem ismétlendő. Szó szerinti forrásidézetben (BDB, Thayer, LSJ, TBESG) nincs. Héberül a jóváhagyott `adat/kiejtes_kivetelek.tsv` alak, ennek híján a gépi magyaros kiejtés (`eszkozok/heber_kiejtes.py`), **jelölés nélkül**; görögül gépi magyaros átírás (`eszkozok/kiejtes.py`); a ragozott alak a saját kiejtését kapja. Ha egy szó egy szakaszban egyszer sem kap kiejtést, az `ellenoriz.py` 22. szabálya JELENTÉS-sorban jelzi (nem gátol).
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

- [ ] **L1. Szerkezeti teljesség** — a TUDOMÁNYOS változat mind a 15
      kötelező szakasza jelen van (cím+Kivonat, Tartalomjegyzék,
      Jelmagyarázat és rövidítések, 1. Előfordulások + 1/a, 1/b. Kizárt
      és vizsgált helyek, 2. Szótári háttér [+2/b és Miért fontos ez a
      lelet, ha van], 3. LXX-fordítói döntések, 4. Kereszthivatkozások
      + Minősítés, 5. Kapcsolatok + Alátámasztás, 5/b. Kapcsolódó
      motívumok (DT277), 6. Értelmezés, 6/b.
      Alkalmazás és tanítói egyezés (DT276), 7.
      Módszertan és nyitott kérdések, 8. Irodalom és idézés, Kolofon —
      LEXV2_2_BRIEF.md G1), és az OLVASHATÓ változat mind a 7 kötelező
      szakasza jelen van. Utólagos szerkesztésnél külön ellenőrizendő,
      hogy egy korábban meglévő szakasz nem maradt-e ki.
- [ ] **L2. Napló-jelölés kötelező** — minden folyamat-/napló-jellegű
      megjegyzés (dátum, eredet, döntés, folyamat- vagy állapotmondat)
      `【NAPLO: …】` blokkban áll, prózai mondatba ágyazva soha; l. a
      "Napló-jelölés kötelező" bekezdés (DT68 (2), 2026.10.08).
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
- [ ] **L8. Gépi és olvasói kapuk** (v3.1) — az `ellenoriz.py` 24.
      (lábjegyzet-definíció) és 25. (1/a próza: kerek mondat + „Funkció:”
      sor, a forma: `9_PaRDeS_motivum_forras_sablon.md` 4. pont) szabálya
      RENDBEN; új cikknél a teljesség-mérés (három háló, `9_` 4. pont)
      lefutott; az olvasói kapu (Feed 9) 0 BUKÁS; a felhasználó a renderelt lapot
      átnézte, és ez rögzítve (`MUNKAMENET.md` C-o, C-v). Ez a pont a
      lezárás feltétele, nem csak a commité.
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
      megszólító/"mi"-hangú mondat a TUDOMÁNYOS változatban. Részletek:
      l. a "Napló-jelölés kötelező" bekezdés.
- [ ] **L7. PaRDeS-rétegfegyelem** — egy réteg elemzési eszköze nem
      olvad össze egy másik réteg tanításával; valódi kapcsolat csak
      külön, a másik réteg nevével, keresztre hivatkozva (l. fent a
      rétegfegyelem bekezdését; az L6 korábbi (g) pontja, DT68 (2)).

Ha L1, L2, L3, L4, L6 vagy L7 bármelyike bukik, a lexikon-oldal NEM
tehető közzé/commitolható, amíg nincs javítva. *(L1–L7: DT68 (2),
DT74 (5); a #10 mércéje ez + a DT2 két rés-szabálya.)*

---

*A két fájl elkészítése előtt belső önellenőrzés fut le: megvan-e a
lezárt tematikus study, a négyforrásos módszertan lefutott-e minden
igehelyre (nem csak mintavétellel), és a lexikai/tematikus
kapcsolatok explicit el vannak-e választva egymástól.*

*Olvasói bevezető (2026-11-03, a felhasználó észrevétele):* a „Mit mutat ez a rész?” címke nem látszik; az összefoglaló bekezdés marad, a generátor a bekezdés végén álló láthatatlan jellel (`<!-- olvasói -->`) azonosítja.

## Az új lapszerkezet és a HAMART-001 regressziós kapui (v4, F178)

*v4 — 2026.11.08 (F178.3–F178.5, a felhasználó jóváhagyásával: „a hamart lesz az új arany / fontos hogy most már visszaesés ne legyen innen”; „Számozzuk is át / ne legyen b/ alszekció. Folyamatos számozás”). Egyeztetett eltérés: az új szerkezet első lépésben csak a HAMART-001 lapján áll (`lexikon_general.UJ_LAPSZERKEZET`); a többi lap motívumonként, a teljes folyamaton át követi (határ, próza, kinyerés két kézzel, visszhang, kapuk, a felhasználó átnézése; a felhasználó: „Ne a régi hibákkal írjuk újra a többi lapot. Minden menjen át a teljes folyamaton”), nem egy generátor-körben. Ahol ez a szakasz és a fenti A) rész eltér, az új szerkezetű lapon ez az irányadó.*

**Szakaszrend (folyamatos számozás, „/b” alszakasz nincs):** Kivonat · Tartalomjegyzék · Jelmagyarázat · **1. Döntési út** (1.1 Mit keresünk · 1.2 Hol kerestünk · 1.3 Mi esett ki és miért · 1.4 Mi maradt és miért · 1.5 Határesetek és nyitott kérdések; makett: artifact `BWNbfmsofYpnfT9v87of1G`) · **2. Előfordulások** (2.1 Az igehelyek szövege) · **3. Kizárt és vizsgált helyek** · **4. Szótári háttér** (elején az áttekintő tábla: szavanként kiejtés, alapjelentés, LXX-megfelelő, helyek száma; a szótári pontok 4.1–4.14; 4.11 a visszhang-blokk) · **5. LXX-fordítói döntések** · **6. Kereszthivatkozások** · **7. Kapcsolatok** · **8. Kapcsolódó motívumok** · **9. Értelmezés** · **10. Alkalmazás** · **11. Módszertan és nyitott kérdések** · **12. Irodalom és idézés** · Kolofon. A nevesített tanítói rész nem áll a lapon (a `tanitoi` rés sorsa: DT643).

**A Döntési út szabályai:** minden vers egyszer számít; az összeadás-sor kiírva (a motívumhoz tartozik + csoportosan kizárva + egyenként elutasítva [+ döntésre vár] = megvizsgált vers); a döntés nélküli vers száma kimondva; a csoportos és az egyenkénti okok lenyitható részletekben; az 1.4 a beépített sorok szavai szerint csoportosít, tételenként a `funkcio` magyarázatával.

**Olvasható döntések, belső jel olvasói formában:** fájlnév, döntés- és feladatazonosító, a blokk technikai kódja, a nyers proveniencia-sor helyett olvasói forrásnév és dátum; a nyers proveniencia-sor a lap forrásában HTML-megjegyzésben megmarad (CLAUDE.md 1. szabály). A döntés olvasói neve „szerkesztői döntés”.

**Visszhang-blokk (4.11; DT639, DT645, DT-F184a):** lánc-szavanként egy sor (Targum, Vulgata, LXX, Mit mutat); a szabályok tételesen alább („A 4.11 visszhang-blokk szabályai”; a kiemelés: 3. pont). Forrás: `adat/visszhang_megfelelok.tsv` (SEMA 2.53), ellenőrizetlen sor nem renderel.

**A 4.11 visszhang-blokk szabályai, tételesen** (DT639, DT645, DT646, DT-F184a; kapu: `olvasoi_kapu.py` VISSZHANG, a V-alszabályok: `adat/SEMA.md` 3.11;
teszt: `eszkozok/olvaso_szerver/teszt_visszhang_kapu.py`, arany minta: a HAMART-001 4.11 blokkja):

0. A lánc a motívumadatból (DT648, SEMA 2.53): lánc-szó a beépített sorok egyetlen héber Strongból álló `gerinc_elem`-je (a szópár, a tematikus és a görög elem nem), a lánc kulcsszavai a gerinc-elemek, nem az 1.2 teljes szólistája (HAMART-001: 6 kulcsszó); láncvers a motívum Pesat-gerincének azon verse, amelyben a kulcsszó a héber szövegben (TAHOT) áll — a motívum saját verse (a beépített sorok versei, a tartomány versenként), nem a szó teljes előfordulása (a gerincen belül sem); a motívum Pesat-gerince: ha a negatív kritérium (2.1) megnevezi a láncot („az 1Móz 3–9 láncára”), az; különben a motívum Pesat-sorainak (`pardes_szint` ∋ Peshat) fejezet-tartománya az első Pesat-sor könyvében; Pesat-sor nélkül nincs lánc (rögzített szakasz nincs; `lexikon_general.lanc_mag`). A lapon a „gerinc” szó nem állhat (olvasói kapu): a bevezető „Peshat-mag”-ot és „a lánc N kulcsszava”-t mond, az 1.2 szólistájától megkülönböztetve (ELLENOR_F178_2 1.). A szabályt a blokk bevezetője és lábjegyzete kimondja. A kinyerő tábla csak a cellákat adja; lánc-szó a tábla soraiból nem lesz. Tórán kívüli láncversnél a Targum-cella „nincs Targum-forrás (az Onkelos csak a Mózes-könyveket fedi)” — nem hiány-kitöltés, és a Targum `N`-jébe nem számít.
1. Lánc-szavanként egy sor; a lánc-szó lemmája (a 4.11-ben és a BDB-háttérben) a láncversek saját Strong-változatából (TBESH `a`/`b`: 1Móz 4:7 → H2403b חַטָּאת, chattát, nem az alapváltozat; `lexikon_general.strong_valtozat_versben`, ELLENOR_F178_2 3.); a cella a fordítás szava kiejtéssel és az `n/N` (a lelet a cellában áll, a „Mit mutat” nem ismétli). A lánc-szó glosszája a láncbeli jelentés: ha a láncversekben a BDB más törzset ad, mint a Qal, a törzs szerinti magyar glossza („megátkozni (Piél)”, `lanc_szo_jelentes`). Két különböző héber lánc-szó két sor.
2. A „Mit mutat” csak a LXX alapvonalát és a különleges leletet mondja; a Targum és a Vulgata alapvonala nem mérhető, ezt a bevezető egyszer mondja ki, a sorok nem ismétlik. A LXX alapvonala gépi: a héber szó láncon kívüli ószövetségi verseiben — csak a láncbeli jelentés előfordulásain (a TAHOT-tükörfordítás közös szótöve) — ugyanaz a szócsalád (`lexikon_general.lxx_alapvonal`); a mondat a nevezőt és a találatot külön mondja: „a láncon kívüli N versből x versben (y%)” — nem „a versek y%-ában (N vers)”, mert a zárójeles szám a nevező, az olvasó találatnak érti (ELLENOR_F178 5.; V7 a három szám egyezését is méri); a sávok (V7): ≥ 80% „a szó szokásos fordítása, a lánc egysége megmarad, de ez önmagában nem lelet”; 40–80% „a szó gyakori, de nem kizárólagos fordítása”; < 40% kiemelt „a láncban más szót választ, mint máshol”; a láncon kívül elő nem forduló szónál „az alapvonal nem mérhető”.
3. Kiemelt (félkövér) következtetés csak alapvonallal (V5). Két héber lánc-szó egy szóval / szócsaláddal: a Targumnál és a Vulgatánál „a láncban mindkét héber szót ugyanazzal a szóval adja vissza; hogy máshol is így fordítja-e, ebből a forrásból nem mérhető” (nem kiemelt); a LXX-nél a két szó alapvonalával: mindkettő ≥ 80% „ez a láncon kívül is így van (x%, y%)”, bármelyik < 40% kiemelt („a láncon kívül viszont nem így”), egyébként „gyakran, de nem kizárólag”. A mondat az első szó sorában áll, a másodikban „l. az … sorát”.
4. Két lemma: „ugyanaz a szócsalád”, nem „ugyanaz a szó” (V4); egy eltérő vers: „egy versben más szó (…)”; csupa különböző szónál „három különböző szó”, szám nélkül.
5. Betoldás-sor: a betoldó fordítás cellája „… · betoldás”, a többi „nincs betoldás”; a következtetés csak a lelet (a fordító a lánc szavát olyan láncversbe teszi, ahol a héberben nincs).
6. BDB-háttér: a háttér-táblában csak a lánc-szavak és tövük állnak; csak valódi rokon nyelv (akkád/asszír, arab, etióp, szír, arámi, óarámi, ugariti, Tell el-Amarna, sabeus); újhéber, targumi arámi (ᵑ7), Sirák nem (V2); nyelvenként egy sor; tartalom nélküli sor nem áll; angol maradék nem állhat (V1); „nem azonosítható” (a BDB-szócikk a lekérdezésben nem azonosított) ≠ „nincs rokon nyelvi adat” (V3). Minden nem latin betűs alak mellett kiejtés; pontozatlan héber betűs alaknál mássalhangzós átírás a kiejtési szabály betűivel (קללם → k-l-l-m). Főnévnél, amelynek szócikkében nincs rokon alak, az igei tő szócikke (`bdb_to_strong`: חָמָס → חָמַס, עִצָּבוֹן → עָצַב): „a főnév szócikkében nincs; a tő, a … ige szócikke szerint:”, alatta a tő nyelvenkénti sorai.
7. Ugyanaz a tagmondat (a számok és a fordító neve nélkül) legfeljebb kétszer a táblán, cellán belül is számolva (V6).
8. Hiány kimondva, nem kitöltve: kinyerés nélkül „a megfelelő kinyerése még nem történt meg”, ellenőrizetlen sorral „nincs ellenőrzött adat”, ellenőrzött, alak nélküli sorral „nincs megfelelő szó”; a „Mit mutat” a más szót és az adat nélküli verset nem keveri („3 versben nincs ellenőrzött adat”, nem „más szó”). A háttér-táblában lánc-szó `bdb` sor nélkül: „a rokon nyelvi adat kinyerése még nem történt meg”.

**A HAMART-001 regressziós kapui (HIBA; `ellenoriz.py` 40. szabály, az új szerkezetű lapon SÉRTÉS, a régin a 2. kiadás tétele):** minden igehelyen kerek próza + „Funkció:” sor; olvasói kapu 0 BUKÁS **kivétel nélkül** (a Tartalomjegyzék, a Jelmagyarázat, a Kolofon, az Irodalom, a technikai dőlt sor és a lábjegyzet is: Károli-idézet, belső jel, „felhasználó” / „orkesztrátor”); a Döntési út számai összeadódnak; döntés nélküli vers 0; a Nave-blokk nem üres. Mellettük: határ-frissesség (39. szabály, Feed 5. kritérium), a beépített sor nem esik a csoportos kizárási okba (37.), nem „csak e szó miatt” (38.), Nave angol maradék nélkül (olvasói kapu NAVE_ANGOL).
