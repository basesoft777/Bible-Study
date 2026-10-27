---
feladat: 131
cim: A motívumlap szótári gerince — BDB és Thayer a motívumot hordozó szakaszokkal, magyarul, a szó jelentése és a hely funkciója két rétegben (pilot: ISTENTISZT-001)
kod: SZOTARI_GERINC
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: dontesre_var
ag: ccr-6dc5ac47-lksrko
ad: az ISTENTISZT-001 lexikonoldalán a szótári blokk a kulcsszavak jelentéstartományát a BDB (H7121, H8034) és a Thayer (G1941) tagolásában mutatja, a motívumot hordozó szakaszokat részletesen, magyarul, a görög szónál egy UBS-doménsorral; a tW, a TBESH, a teljes UBS és a Mounce helyén mutató a szónézetre; az előfordulás-táblában „Jelentés (a szó)” és „Funkció (a motívumban)” két oszlop, a címke forrása a kutatói ⓘ-ben (DT272)
kovetkezo: "Te: ⛔ 3.1 — DT-F131f (DONTESEK.md): a repón kívüli próbalap elfogadása, a címkék szövege, az 56.15-ös UBS-kód; utána /kovetkezo (javítókör vagy ⛔ 4. DT-F131g)"
olvas: [DONTESEK.md, RENDER_BRIEF.md, adat/SEMA.md, adat/elofordulasok.tsv, adat/lexikon_hivatkozasok.tsv, adat/forditasok.tsv, adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv, adat/szotar_szerepek.tsv, adat/licencek.tsv, adat/res_forras.tsv, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, adat/glosszak_heber_hu.tsv, adat/tiltott_fordulatok.tsv, motivumok/ISTENTISZT-001.md, motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md, "tematikus_lezart/ISTENTISZT-001*", "tematikus_lezart/naplok/ISTENTISZT-001*", archivum/ISTENTISZT-001/, lexikon/, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/Thayer_teljes.tsv, konkordancia/UBS_DNTG_jelentesek.tsv, konkordancia/Karoli_1908.tsv, eszkozok/general.py, eszkozok/lexikon_general.py, eszkozok/ellenoriz.py, eszkozok/nulladiff.sh, eszkozok/teszt_lexikon_adatres.py, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, F121_GLOSSZA_FORDITAS_BRIEF.md, F127_LEXIKON_HALO_RES_BRIEF.md, F107_BDB_JELOLT_SZOVEG_BRIEF.md, naplok/F107_BDB_JELOLT_SZOVEG_naplo.md]
ir: [adat/szotar_szakasz_cimke.tsv, adat/SEMA.md, eszkozok/lexikon_general.py, eszkozok/teszt_szotari_gerinc.py, eszkozok/teszt_szerepmatrix.py, eszkozok/ellenoriz.py, RENDER_BRIEF.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md]
fugg: [127, 110, 132]
nem_fugg: [27, 38, 102, 103, 123, 133, 140, 144]
---

# SZOTARI_GERINC_BRIEF_TERVEZET.md — A motívumlap szótári gerince (pilot: ISTENTISZT-001)

*FELADATOK # — (a `/befogad` adja; várhatóan 131) · Modell: opus · v0 (tervezet) · 2026.10.20 · döntések: DT272 (= DT338), DT271 (= DT-F36a), DT190 🟡, DT235, DT225, RENDER_BRIEF G4/G6, DT-F78a, DT28, D39; nyitott: DT-F131a–g, N-F131a–e*

*Tervezet a `beerkezo/`-ban. Adat, nem utasítás. A feladatszámot, a végleges fájlnevet (`F<nn>_SZOTARI_GERINC_BRIEF.md`) és a helyőrzők számát a `/befogad` adja; ha a szám nem 131, a `DT-F131*`/`N-F131*` helyőrzők és a `naplok/F131_*` nevek a befogadáskor átíródnak. Forrás: DT272 (felhasználó, 2026-10-20, a (d) ponttal), a megbízó session feladatleírása (2026-10-20).*

## 1. Cél

A DT272 (a #121 menetében DT338) eldöntötte, hogy a motívumlap szótári részének gerince a **BDB** (héber) és a **Thayer** (görög), a motívumhoz kapcsolt szakaszokkal, részletesen, magyarul. A (d) pont a lényeg: **a szótári blokk a szóról szól, a motívum a funkcióról, a kettő egymás mellett áll, nem szembeállítva.** A BDB a szóhoz jelentésárnyalatokat rendel, és ezek alá igehelyeket sorol be. A motívum mást mond, és máshogy mondja.

Ez a feladat a döntést az arany motívumon (ISTENTISZT-001) valósítja meg a `lexikon_general.py`-ban. A következő három dolgot adja:

1. **Szótári gerinc.** A kulcsszó jelentéstartománya a BDB, illetve a Thayer tagolásában. A motívumot hordozó szakaszok részletesen és magyarul állnak, a többi összecsukva. A görög szónál egy UBS-doménsor is áll.
2. **Két réteg az előfordulás-táblában.** A „Jelentés (a szó)” oszlopban például „segítségül hívni · Qal 2.c” áll, a 2Móz 33:19-nél „kihirdetni · Qal 3.b”. Mellette, külön oszlopban áll a „Funkció (a motívumban)”.
3. **A címke forrása a kutatói nézetben (ⓘ).** Az ⓘ megmondja, hogy a címke a BDB saját példalistájából jön-e, vagy a kutatás rendelte hozzá a BDB tagolása szerint.

A feladat a többi 7 lapot nem változtatja (DT272 (f): előbb az arany lap, utána a régi motívumok, külön feladatban).

## 2. Mért helyzet (2026-10-20, a tervezet írásakor; az M0 megismétli)

*proveniencia: scope=ISTENTISZT-001 (32 hely); H7121, H8034, G1941 | forras=adat/elofordulasok.tsv, adat/lexikon_hivatkozasok.tsv, adat/forditasok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv (`szurt≠1`), lexikon/ISTENTISZT-001_TUDOMANYOS.md; eseti olvasó szkriptek (`split('\t')`), a session közös jegyzetmappájában: `SZOTARI_GERINC_meres*.py` | ts=2026-10-20. A számok tájékoztatók, az M0 a saját szkriptfájljával méri újra.*

**Az előfordulások szótári hivatkozása (`elofordulasok.tsv`).**
- 22 ÓSZ-hely: `lexikon_szotar=BDB`, `lexikon_entry_id=H7121`. Ebből `jelentes_szam`=`2.c` 17 helyen, `2.c (rokon)` 1 helyen (Sof 3:9), `2.c (tagadva)` 2 helyen (Jer 10:25, Zsolt 79:6), `3` 2 helyen (2Móz 33:19, 34:5).
- 10 ÚSZ-hely: `lexikon_szotar=TBESG`, `G1941`, `jelentes_szam=2`. **Nem Thayer:** a görög előfordulások ma a TBESG tagolására mutatnak.
- A H8034-re egyetlen sor sem mutat: a `strong` mező `H7121+H8034`, a `jelentes_szam` csak a H7121-é.
- **A minősítő alak** (`2.c (rokon)`, `2.c (tagadva)`) nincs benne a SEMA 2.2.2 union-értékkészletében. A `lexikon_hivatkozasok.tsv` kulcsára (`2.c`) így csak a zárójeles rész levágásával mutat (N-F131b).
- **A `jelentes_hu` mező a szó jelentését és a motívumbeli értelmezést vegyíti.** Mért értékek: `kihirdetni, kinyilatkoztatni (NEM invokáció)` (2 sor), `invokálni — tagadó szerkezetben, a mulasztás vádjaként` (2), `Baál nevével` (2), `Jahve nevével, konkrét felszólítás hatalma megmutatására` (1), üres (2). A mai „Szótári jelentés” oszlop ezt rendereli. Ez éppen az a szembeállító keretezés, amelyet a DT272 (d) kizár (N-F131a).

**A BDB-tagolás három helyen, három alakban (DT190 🟡).**
- A `lexikon_hivatkozasok.tsv` 4 BDB-sora: `H7121 2.c`, `H7121 3`, `H8034 részlet`, `H3548 1`. Ezek kézi `jelentes_szam`-ok, angol kivonattal.
- A `bdb_szakaszok.tsv` / `bdb_szakasz_hu.tsv` (2.30, 2.32) útvonala: `Qal/2/c`, `Qal/3/b`, `-/3/-`.
- A `bdb_vers_jelentes.tsv` (2.29) útvonala: `Qal/2/c`, `-/3`. A 2.29 a záró `/-` nélkül írja (H8034: `-/3` ↔ `-/3/-`).
- A `2.c` → `Qal/2/c` leképezés nem gépiesíthető biztonságosan: a H7121-ben `Niph'al/2/c` is van.

**A magyar BDB szakaszolása.**
- H7121: 43 sor, ebből `illeszkedik` 40, `jelolo_nelkul` 3. Nincs `horgonnyal`, nincs `elakad`.
- H8034: 12 sor, ebből `illeszkedik` 6, `jelolo_nelkul` 5, `horgonnyal` 1 (`-/5/-`, horgony `55:13`), `elakad` 0.
- A szakaszok magyar kezdete. `Qal/3/-`: „3 kihirdetni:”. `Qal/2/c`: „c. … hívni ׳י nevével (azaz használni azt a segítségül hívásban): 1Móz 4:26; 12:8; …”. `Qal/3/b`: „b. … így (korábban) ׳ק י ׳בְשֵׁם 2Móz 33:19; 34:5 (JE)…”. `H8034 -/3/-`: „3 név, mint Isten megjelölése…”.

**A BDB saját példahelyei a motívumhelyek között (`bdb_vers_jelentes.tsv`).**
- H7121: 9 hivatkozás 8 versre. `Qal/2/c` alatt 7: 1Móz 4:26, 12:8, 2Kir 5:11, Jer 10:25, Zsolt 79:6, 1Kir 18:24 (kétszer). `Qal/3/b` alatt 2: 2Móz 33:19, 34:5.
- H8034: 6 hivatkozás 5 versre. `-/3` alatt 4: 1Móz 4:26, 12:8, 13:4, 21:33. `-/4` alatt 1: 1Kir 18:24. `fej` alatt 1: 1Móz 12:8.
- Összevetés a kutatói hozzárendeléssel. A 8 H7121-vers mindegyikén a BDB-példa útvonala a kutatói `jelentes_szam` alá esik: `2.c` ⊇ `Qal/2/c`, `3` ⊇ `Qal/3/b`. **Ellentmondás: 0.** A 2Móz 33:19 és a 34:5 kutatói hozzárendelése durvább (`3`), a BDB-példa finomabb (`Qal/3/b`).

**A Thayer G1941 magyarul.**
- A `forditasok.tsv` `teljes` sora 4 601 karakter, szakasztábla nincs hozzá. A fő számozott részek (1–5) a szövegben vannak, de az egyszerű számminta hamis találatot is ad: „1. aorisztosz”, „3. személy”, „1. pontot”, „7. kiadásában”.
- Szemrevételezett határokkal a 10 ÚSZ-motívumhelyből 7 az 5. részben áll („héber mintára … kárá besém JHVH”), 1 az 1. részben (1Pét 1:17; a határ itt bizonytalan), 2 nincs idézve (Róm 10:14, ApCsel 9:21). Az ApCsel 22:16 csak könyv nélkül, folytatásként áll.
- A „4. segítségül hívni (mint a német anrufen), invokálni” rész a TBESG 2-vel rokon. Mindez tájékoztató; a határ adat nélkül nem rögzíthető (DT-F131c).
- A G1941 UBS-doménjei (33.176, 11.28, 33.131) magyarul megvannak, `UBS_DNTG` `kezi` sorokként.

**A mai lap (`lexikon/ISTENTISZT-001_TUDOMANYOS.md`, generált, a #11 utáni állapot).**
- A „2. Szótári háttér” a szerepmátrix (RENDER_BRIEF G6, DT-F78a) 13 szerepét hozza, mindkét nyelven, a rokon szavakkal és a 2/b réssel.
- A BDB a 2. szerepben három kivonatként áll (2.c, 3, részlet), a teljes szócikkek a szerepek között szétszórva.
- A `(fordításra vár)` jelölés 65 helyen áll (a #121 mérése). A #121 szerint a 62 hiányzó egység így oszlik meg: 48 UBS DBH, 2 DNTG, 1 TBESH, 1 Mounce, 10 tW.

**A szónézet.** Az olvasó-szerver (`eszkozok/olvaso_szerver/alkalmazas.py`) a `/szo/<strong>` útvonalon szónézetet ad. A `lexikon/*.md` ma sehova nem mutat oda.

## 3. Hatókör

### Benne van

- **Szótári gerinc** az ISTENTISZT-001 lapjának „2. Szótári háttér” szakaszában, a DT-F131a szerinti helyen:
  - *héber (H7121, H8034):* a BDB jelentéstartománya a 2.30 tagolásában. A motívumot hordozó szakaszok (DT-F131d) teljes magyar szövege a `bdb_szakasz_hu.tsv`-ből jön. A többi szakasz összecsukva áll, a jelével és a címkéjével (DT-F131d (e)). A `horgonnyal` szakaszhatár a kutatói nézetben ellenőrzésre jelölve. Az `elakad` szakasz explicit hiányként áll: angol szöveg a 2.30-ból, `(fordításra vár)` jelöléssel, a DT272 „Következmény” mondata szerint. A H7121/H8034-en ma 0 `elakad` van; a viselkedést teszt igazolja.
  - *görög (G1941):* a Thayer magyar szövege a DT-F131c szerinti tagolásban, egy UBS-doménsorral. A sor a három Louw–Nida-kódot a magyar glosszával adja, a teljes UBS-szócikk nélkül (DT272 (a)).
  - **A BDB (és a Thayer) saját példahelyei a fordított szakaszban kiemelve, felirat nélkül** (DT272 (d)). A forrás a `bdb_vers_jelentes.tsv`, illetve a DT-F131c táblája. A kiemelés a magyar szövegben keresett igehelyen áll, nem az angol `poz`-on (DT272 (e)). Ahol a hivatkozás a magyarban nem található meg, ott nincs kiemelés. Ilyenkor a naplóba és a kutatói ⓘ-be kerül, kitalálás nélkül (3. szabály).
- **Az előfordulás-tábla két oszlopa.** A „Jelentés (a szó)” a DT-F131d szerinti címkét és a tagolási jelet adja. A „Funkció (a motívumban)” a mai `funkcio` címke. A kettő egymás mellett áll. A mai „Szótári jelentés” oszlop és a `jelentes_hu` megjelenítése az arany lapon megszűnik (N-F131a). A „Funkció” oszlop tartalma nem változik.
- **A címke forrása a kutatói ⓘ-ben** (DT-F131e). Két érték lehet. *BDB-példa*: a BDB e szakaszban maga idézi a helyet; a sor `bdb_vers_jelentes` `sorszam`-ával. *Kutatói hozzárendelés a BDB tagolása szerint*: az `elofordulasok.tsv` `jelentes_szam` értéke a DT-F131b szerinti leképezéssel. A megfogalmazás a BDB tagolására utal, nem a BDB versről tett állítására.
- **A tW, a TBESH, a teljes UBS (DBH és DNTG) és a Mounce lekerül az arany lapról.** A helyükön egy mutató áll a szónézetre (DT272 (b)(c); a mutató alakja: DT-F131e). A szerepmátrix többi szerepe a DT-F131a szerint alakul.
- **Adat:** a DT-F131b–d szerinti kis kézi tábla (javaslat: `adat/szotar_szakasz_cimke.tsv`). Ha a DT-F131b így dönt, a `lexikon_hivatkozasok.tsv` új attribútum-oszlopa is. Mindkettőhöz SEMA-szakasz és `ellenoriz.py`-szabály tartozik.
- **Kapcsoló a generátorban:** az új szótári blokk és a két oszlop csak az ISTENTISZT-001-en él. **A többi 7 lap bájtra változatlan** (`eszkozok/nulladiff.sh`).
- RENDER_BRIEF (G6 mellé egy mondat: az arany lapon a szerepmátrix a DT272 és e feladat döntései szerint szűkül) és a lexikonsablon.

### Nincs benne

- **A szónézet** (olvasó-szerver): a teljes szócikk, a releváns igehelyre mutató BDB-hivatkozás jelölése, a jelölés igazítása a magyar szakaszhoz (DT272 (1) és (e) második fele). Ez a szónézet ága, külön feladat (N-F131e).
- **A motívumlap blokkstruktúrája** (DT272: „külön döntés”). A Motívumlap-terv és -mockup (2026-10-19) csak terv, erre a feladat nem épít. A szakaszszámozás (1–8) és a többi blokk változatlan marad. A feladat csak a „2. Szótári háttér” tartalmát és az előfordulás-tábla két oszlopát érinti.
- **Fordítás.** A feladat a meglévő magyar adatból dolgozik (DT272 (f)), `forditasok.tsv`-sort nem ír. A három `elakad` gerincszó (H2416, H5315, H8415) újrafordítása a #128/#38-é. A teljes #38 és a #27 a szónézet ága.
- **A régi 7 motívum** kiterjesztése: külön feladat ennek lezárása után (DT272 (f)).
- **A DT190 eldöntése.** A feladat a DT190 egyik opcióját sem zárja ki, és nem fagyaszt be útvonal-formátumot (l. 5. szakasz, DT-F131b).
- **Az `elofordulasok.tsv` sorainak tartalmi javítása** (a `jelentes_hu` keverése, a minősítő alakok, a görög sorok Thayer-hozzárendelése). Ez kutatói adat; N-F131a, N-F131b, illetve a DT-F131c (b) ága.
- **A törzscikk** (kivezetés alatt, D34; az ISTENTISZT-001-é archív, E28).

### A #121 hatókörének viszonya (mit vesz át ez a feladat)

A DT272 kimondja: a #121 mostani hatóköre (454 egység) szűkítendő, vagy a szónézet ágára kerül, és erről a #121 a saját menetében dönt. Ez a feladat a #121 fejlécét és briefjét nem írja. Az átfedés:

| A #121 tétele | Viszony ehhez a feladathoz |
|---|---|
| Az arany lap 62 hiányzó egysége (48 UBS DBH, 2 DNTG, 1 TBESH, 1 Mounce, 10 tW) | A tW, a TBESH, a teljes UBS és a Mounce e feladat után **nem áll az arany lapon**, tehát a lap nem várja a fordításukat. A fordításuk a szónézet ágán dől el (#121). Az M0 egységenként listázza, melyik tűnik el a lapról. A maradék `(fordításra vár)` jelölést (pl. a rokon szavaknál) a napló kulcsonként rögzíti. |
| A #121 M1 mintája (az ISTENTISZT-001 mint minta-lap) | Ez a feladat után az arany lap már nem jó minta a glosszafordításra. A #121-nek új minta kell (javaslat: a szónézet, vagy egy régi lap). N-F131d. |
| N-F121a (a BDB nyelvi háttere a teljes fordítás feje, renderbe kötés) | **Részben átveszi:** ha a DT-F131a a 8. szerepet a gerinc `fej`-szakaszába vonja, a H7121 és a H8034 nyelvi hátterét a `bdb_szakasz_hu.tsv` `fej` sora adja. A többi 16 Strongé a #121-nél, illetve a kiterjesztésnél marad. |
| N-F121b (a héber 9. szerep DBH-táblája angolul) | Az arany lapon tárgytalan (a teljes UBS lekerül). A többi lapon változatlan. |
| A G1941 két kézi sorának javítása (F121.0, „melléknév”) | **Nem veszi át.** Ez a feladat `forditasok.tsv`-t nem ír. Ha az F121.0 előbb lefut, a Thayer-szakasz a javított szöveget mutatja. Ha később fut, a DT-F131c táblájának `forras_hash`-e jelzi az elavulást (l. 4.1). |

## 4. Lépések (⛔ a kötelező megállások)

**0. Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév összevetése a `modell: opus` mezővel. Eltérésnél megállás.

**0.1 Előfeltételek.**
- A #127 `lezarva`: ugyanazt a generátort és lapot írja, és a 6/b, 5/b blokkjai után a nulla-diff alapja más.
- A #110 `lezarva`: a felhasználó sorrendje (2026-10-20) „#127 → #110 → a szótári réteg”.
- Az `ir` fájljain nem fut más feladat (D39). A #36 sorrendje a DT271 szerint előbb jöhet; a levezetett kizárást a `feladatok.py fuggesek` adja.
- A `main` lap-állapota az alap.

**0.2 M0 — újramérés** (szkriptfájlból, `split('\t')`, `naplok/F131_SZOTARI_GERINC_naplo.md` 1. szakasz, proveniencia-sorral): a 2. szakasz minden száma, a #127 utáni lapon. Eltérésnél a napló okot ad. A 62 #121-egység sorsa egységenként: lekerül / marad.

**0.3 ⛔ DT-F131a–e** eldöntése az 5. szakasz opciói szerint, a `DONTESEK.md`-be helyőrzős tételként. A felhasználó dönt (vagy az orkesztrátor a felhasználó felhatalmazásával, a tartalmi kérdésekben utólagos jelentéssel). A végrehajtás a döntés után indul.

**1. Adat (`F131.1`)** — a DT-F131b–d szerint.
- Új kézi tábla (javaslat: `adat/szotar_szakasz_cimke.tsv`) és SEMA-szakasz. Ha a DT-F131b (1) nyer, a `lexikon_hivatkozasok.tsv` új oszlopa is.
- A táblát író szkript írás előtt összeveti a sorokat az eredetivel, és eltérésnél megáll (CLAUDE.md, TSV-szabály; minta: `eszkozok/igazolas_migracio.py`).
- Új `ellenoriz.py`-szabály:
  - minden BDB-címke útvonala létezik a 2.30-ban (a záró `/-` normalizálásával);
  - a Thayer-határok egymás után fűzve bájtra a `forditasok.tsv` sor `forras_hash`-ével rögzített fordítást adják; eltérés esetén a sor `elavult`, HIBA;
  - minden `lexikon_jelentes_szam` létező `lexikon_hivatkozasok.tsv`-kulcsra mutat (DT-F131b 2.), illetve az 1. esetén minden `bdb_utvonal` a 2.30 egy útvonalára.
- A címkék szövegét (`cimke_hu`) a végrehajtó javasolja a magyar szakasz vezérszavaiból, `manual` provenienciával. **A címke a szóról szól:** benne nem állhat motívumra, invokációra vagy „nem”-re utaló minősítés. A szöveg az 1. lépés ⛔-ánál, a DT-F131f próbájával együtt kerül a felhasználó elé.
- Commit.

**2. Generátor (`F131.2`)** — a 3. szakasz „Benne van” pontjai, a kapcsolóval.
- Az új teszt (`eszkozok/teszt_szotari_gerinc.py`) legalább ezeket vizsgálja:
  - a BDB-példa és a kutatói hozzárendelés címkeforrása (az ⓘ szövege);
  - a finomabb BDB-példa elsőbbsége a kutatói út alatt (2Móz 33:19 → `Qal 3.b`);
  - **az ellentmondó eset** (a BDB-példa nem esik a kutatói út alá): nincs címke, a futás HIBA-val megáll, választás nélkül (szintetikus sor);
  - a minősítő alak (`2.c (tagadva)`) kulcsa `2.c`, a minősítő nem kerül a Jelentés-oszlopba;
  - `horgonnyal`: a H8034 `-/5/-` jelölve;
  - `elakad`: szintetikus, vagy a H2416 egy szakasza; explicit hiány, angol szöveg, `(fordításra vár)`;
  - a magyar szövegben meg nem talált példahely: nincs kiemelés, napló.
- A 7 lap nulla-diff (`eszkozok/nulladiff.sh`).
- Commit.

**3. Próbarender a repón kívülre (`F131.3`).** `python eszkozok/general.py --cel lexikon --id ISTENTISZT-001 --kimenet <ideiglenes könyvtár a repón kívül>`. Nem a `generalt_proba/`-ba és nem a `lexikon/`-ba (CLAUDE.md). Gépi mérés a naplóba:
- a szótári blokk és a Jelentés-oszlop nem tartalmaz szembeállító keretezést. Tiltott minták a blokkban, kis- és nagybetű nélkül: `eltér`, `máshová sorol`, `NEM invokáció`, `szemben a BDB`, `a BDB szerint nem`. Találatnál javítás, nem kivétel;
- a `(fordításra vár)` jelölések száma előtte és utána, kulcsonként;
- az `ellenoriz.py` 13. szabálya és az új szabály RENDBEN; `python eszkozok/feladatok.py ellenoriz` zöld;
- a 22 ÓSZ- és a 10 ÚSZ-sor mindegyikén van címke, vagy kimondott hiány;
- a kiemelt BDB-példák száma a 2. szakasz 9 + 6 hivatkozásához mérve, a meg nem találtak listájával.

**3.1 ⛔ DT-F131f — az elfogadási próba.** A felhasználó a renderelt lapot olvassa (a repón kívüli kimenetet, vagy annak HTML-nézetét; a végrehajtó megnyitja, nem összefoglalja). A kérdés: *a szó jelentését és a hely motívumbeli funkcióját két külön dolognak látja-e?* Ugyanitt dönt a címkék szövegéről is. „Nem” vagy részleges „igen” esetén a végrehajtó a felhasználó megjegyzései szerint javít, és újra a 3. lépés jön (legfeljebb két kör, utána megállás és jelentés).

**4. ⛔ DT-F131g — az éles lexikon felülírása (`F131.4`).** A jóváhagyott próba után, külön jóváhagyásra: `general.py --cel lexikon --id ISTENTISZT-001 --ir`. A `git diff lexikon/` csak az ISTENTISZT-001 lapot és azon csak a várt blokkokat (2. Szótári háttér, 1. Előfordulások táblája, a tartalomjegyzék, ha változik) érinti; ezt a napló rögzíti. A 7 lap diffje üres. Commit.

**5. Független ellenőrzés** (`fuggetlen-ellenor`, `naplok/ELLENOR_SZOTARI_GERINC.md`) a base..head diffen:
- séma ↔ tábla ↔ generátor egyezése;
- a 7 lap nulla-diff;
- minden címke mögött létező 2.30-útvonal vagy Thayer-határ;
- nincs `forditasok.tsv`-írás;
- a tiltott keretezés 0;
- minden kiemelés mögött `bdb_vers_jelentes`-sor (vagy a Thayer-tábla igehelye);
- a proveniencia-sorok megvannak.

ELTÉRÉS esetén `/elteres` (2 kör).

**6. Zárás:** a brief fejléce, zárónapló, az N-F131a–e a `NYITOTT_FELADATOK.md`-be, a RENDER_BRIEF és a sablon mondata, a #121-nek szóló N-F131d.

## 5. Nyitott döntések (helyőrzők; végleges számot a `szamkiosztas` Action ad)

### DT-F131a — mi marad a szerepmátrixból az arany lapon (⛔ 0.3)

**Kérdés:** a DT272 a lapról a tW-t, a TBESH-t, a teljes UBS-t és a Mounce-ot veszi le. Mi legyen a G6 szerepmátrix többi szerepével (TBESG, TWOT-szám, SDBH-domén, SECE, LSJ, BDB-etimológia, kiejtés, 12–14., rokon szavak, 2/b), és hol álljon a gerinc?

**Opciók:**
1. **Minimális:** a gerinc a „2. Szótári háttér” elejére kerül, nyelvenként („A kulcsszó jelentéstartománya”). A szerepmátrixból csak a DT272 négy forrása kerül le, mutatóval a szónézetre. A BDB 2. szerepének mai kivonatai (2.c, 3, részlet) és a Thayer teljes szövege a gerincbe olvadnak, nem ismétlődnek. Minden más szerep változatlan.
2. **Teljes csere:** a „2. Szótári háttér” csak a gerincből és a UBS-doménsorból áll, minden más szerep a szónézetre mutat. Ez már blokkstruktúra-döntés, amelyet a DT272 külön döntésnek tart.
3. **Hozzáadás:** a gerinc új blokk a mai szerepmátrix előtt, és semmi nem kerül le. Ez a DT272 (b)(c)-vel ellentétes.

**Részkérdések:**
- *(i) a héber SDBH-doménsor:* a görög UBS-doménsor mintájára egy sorban maradjon (javaslat), vagy lekerüljön, mint a teljes UBS.
- *(ii) a 8. szerep (nyelvi háttér):* a BDB `fej`-szakasza a gerincben (javaslat; N-F121a részbeni átvétele), vagy változatlanul a 8. szerepben.
- *(iii) az előfordulás-tábla „UBS-jelentés” oszlopa* (versenkénti DNTG-jelentés, csak ÚSZ): maradjon, mert ez az egyetlen versenkénti görög jelentés (javaslat), vagy olvadjon a „Jelentés (a szó)” oszlopba.

**Javaslat: 1., (i) marad, (ii) a gerincben, (iii) marad.** Indok: a DT272 csak a négy forrásról döntött, a többi a blokkstruktúra-döntésé. A minimális változat a döntést hajtja végre, és nem dönt helyette. A kivonatok beolvasztása nélkül a BDB 2.c kétszer állna a lapon.

### DT-F131b — az előfordulástól a BDB-szakaszig vezető út (DT190 🟡 mellett) (⛔ 0.3)

**Kérdés:** a kutatói `jelentes_szam` (`2.c`, `3`) hogyan mutasson a 2.30 szakaszára (`Qal/2/c`, `Qal/3/-`), ha a DT190 (a BDB-tagolás közös kulcsa) nyitott?

**Opciók:**
1. **A `lexikon_hivatkozasok.tsv` új attribútum-oszlopa (`bdb_utvonal`).** A 2.30 útvonalára mutat, nem kulcs. Csak az arany sorokon van kitöltve: `H7121 2.c` → `Qal/2/c`, `H7121 3` → `Qal/3/-`, `H8034 részlet` → `fej`. Üres érték: nincs leképezve. A lánc: `elofordulasok` → `lexikon_hivatkozasok` kulcsa → `bdb_utvonal` → 2.30/2.32.
2. **A leképezés az új kézi táblában** (`lexikon_jelentes_szam` oszlop). A meglévő tábla sémája nem változik, de a BDB-tagolásnak egy negyedik tartója lesz (a DT190 éppen ezt kifogásolja).
3. **Gépi szabály** (az első törzs, amelyben az útvonal létezik). Mért ellenpélda: a `Niph'al/2/c` is létezik, tehát nem elfogadható.
4. **Várni a DT190-re.** Ez blokkolja a feladatot.

A 2.29 és a 2.30 útvonal-alakja eltér (`-/3` ↔ `-/3/-`). Az összevetés mindkét oldalon a záró `/-` levágásával történik, ezt teszt rögzíti; egyik tábla sem íródik át.

**Javaslat: 2.** A tábla sora: `szotar=BDB`, `strong`, `szakasz` (2.30-útvonal), `lexikon_jelentes_szam`. Csak a 2.30 kulcsára és a `lexikon_hivatkozasok.tsv` kulcsára mutat, saját tagolást nem tart. A 2.30 útvonal-alakja nem fagy be.

Indok: a DT190 fő gondja, hogy a tagolást több hely egymástól függetlenül tartja. Ezt a 2. sem súlyosbítja: a sor létező 2.30-útvonalra mutat, és az új `ellenoriz.py`-szabály ezt hangos hibaként őrzi. Ha a DT190 (a) nyer, a sor egy lépésben átvihető a `lexikon_hivatkozasok.tsv`-be; ez a DT190 kimondott utótétele, „a 4 sor átkulcsolása”.

Az 1. mellett szólna, hogy az a DT190 (a) iránya. Ára azonban, hogy a `lexikon_hivatkozasok.tsv`-t a #123 is írja: a két feladat kizárná egymást, és a `feladatok.py` sorszám szerint a teljes #123-at tenné e feladat elé (próbafutás, 8. szakasz). Ez ellentétes a felhasználó sorrendjével. Ha a 0.3 mégis az 1.-et választja, a `lexikon_hivatkozasok.tsv` egyeztetett eltérésként kerül az `ir`-be (a DT225 mintája), és a #123-mal a sorrendet a felhasználó dönti el.

### DT-F131c — a Thayer tagolása és a görög címke (⛔ 0.3)

**Kérdés:** a Thayerhez nincs szakasztábla (a DT190 Thayer-ága „külön kérdés”), a görög előfordulások pedig a TBESG 2-re mutatnak. Hogyan álljon a G1941 a gerincben, és honnan jöjjön a 10 ÚSZ-sor címkéje?

**Opciók — tagolás:**
1. **Kézi határtábla a G1941-re** (az új táblában: `szotar=Thayer`, `szakasz` = a fő rész száma, `hu_kezdet`, `hu_hossz`, `forras_hash` = a fordítássoré). Az `ellenoriz.py` ellenőrzi, hogy a részek egymás után fűzve bájtra a fordítást adják. Ez a 2.32 mintája, kézi határral. `manual` proveniencia.
2. **A Thayer egészben, összecsukva,** a motívumhelyek kiemelésével, szakaszolás nélkül. Olcsó, de a „motívumot hordozó szakaszok részletesen” elv a görög oldalon nem teljesül.
3. **Gépi Thayer-szeletelő** (a #107 mintájára). Külön feladat, blokkol.

**Opciók — a görög címke:**
- (a) **marad a TBESG 2** („segítségül hívni · TBESG 2”), kutatói hozzárendelésként. Az ⓘ ezt mondja ki.
- (b) **a 10 ÚSZ-sor `lexikon_szotar`/`jelentes_szam` mezője Thayer-részre vált.** Kutatói adatváltozás az `elofordulasok.tsv`-ben, soronkénti ⛔-vel. A mért 5. rész (7 hely) és a 4. rész („segítségül hívni”) közti választás tartalmi kérdés.
- (c) **Thayer-példa, ahol a Thayer idézi a helyet** (7 hely), máshol a TBESG 2. Egy oszlopban két tagolás.

**Javaslat: 1. + (a).** Indok: az 1. a gerincet a döntés szerint adja, és a határt adattá teszi, nem kódba írja. Az (a) nem változtat kutatói adatot ebben a feladatban. A Thayer-hozzárendelés (b) az értelmező tulajdonosé, a feladat N-tételként adja tovább (N-F131c). A (c)-t nem javaslom: az olvasó egy oszlopban két tagolást látna.

### DT-F131d — a motívumot hordozó szakasz, a címke és a tartomány megjelenítése (⛔ 0.3)

**Kérdés:**
- Mely szakaszok állnak „részletesen”?
- Honnan jön a „Jelentés (a szó)” címke szövege?
- Hogyan látszik a tartomány többi része?

**Opciók — „motívumot hordozó”:**
1. **A kutatói út szakaszai ∪ a BDB-példa szakaszai.** A BDB-példa csak akkor számít, ha a hely motívumhely; a `fej` és a `cim` nem számít. Az arany lapon ez a H7121-nél a `Qal/2/c`, a `Qal/3/-` és a `Qal/3/b`, a H8034-nél a `-/3/-` és a `-/4/-`, a G1941-nél a DT-F131c szerinti rész.
2. **Csak a kutatói út szakaszai.** Ekkor a H8034 nem kapna részletes szakaszt, mert nincs rá kutatói hozzárendelés.
3. **Csak a BDB-példa szakaszai.** Ekkor a nem idézett motívumhelyek (a 22-ből 14) szakasza nem állna részletesen.

**Opciók — a címke szövege:**
- (a) **szakaszonkénti kézi címke az új táblában** (`szotar` + `strong` + `szakasz` → `cimke_hu`). Egy hely, minden előfordulás ugyanazt örökli; a címke a szóról szól.
- (b) **az `elofordulasok.tsv` `jelentes_hu`-ja.** Mért: 7 soron motívumbeli értelmezést hordoz, ez a DT272 (d)-vel ütközik.
- (c) **gépi vezérszó a magyar szakasz elejéből.** Mért: a `Qal/2/c` eleje („c. … hívni ׳י nevével (azaz …)”) nem ad tiszta címkét.

**A címke és az elsőbbség szabálya:**
- Ha a BDB a helyet maga idézi, és útja a kutatói út alá esik, a címke a finomabb BDB-útvonalé („kihirdetni · Qal 3.b”).
- Ha egyik sem esik a másik alá: HIBA, megállás, kézi kérdés (a mért ellentmondás az arany lapon 0).
- A tagolási jel a 2.30 útvonalából készül (`Qal/2/c` → „Qal 2.c”).

**A tartomány megjelenítése** (DT272 (e)): a teljes BDB-tagolás vázlatként áll, szakaszonként egy sorral (jel + címke, vagy ha címke nincs, a magyar szakasz első tagmondata). A motívumot hordozó szakaszok kibontva állnak, a többi `<details>`-ben, összecsukva. A végén link a teljes szócikkre (a szónézet, DT-F131e).

**Javaslat: 1. + (a), a fenti elsőbbséggel és megjelenítéssel.** Indok: az 1. adja a DT272 két forrását (a BDB-példát és a kutatói hozzárendelést). Az (a) a DT272 (d) „a címke a BDB tagolására utal” mondatát szó szerint adatosítja, a (b) keverését nem viszi a lapra. A `<details>` a lexikonban új elem: ha a felhasználó a markdown-nézetben nem kéri, a tartalék a behúzott, rövidített vázlat.

### DT-F131e — az ⓘ és a szónézet-mutató alakja (⛔ 0.3)

**Kérdés:** a statikus `lexikon/*.md` a „kutatói nézet”. Hol álljon benne az ⓘ, és hogyan mutasson a szónézetre?

**Opciók — ⓘ:**
1. **A sor meglévő lábjegyzetének bővítése** (`proveniencia | igazolas | jelentés-címke: …`), és egy „ⓘ” jel a Jelentés-cellában, amely a lábjegyzetre mutat.
2. Külön lábjegyzet csak a címkeforrásnak.
3. A szótári blokk végén egy összesítő tábla (hely → címkeforrás).

**Opciók — szónézet:**
- (a) markdown-link az olvasó útvonalára (`[szónézet](/szo/H7121)`). Az olvasóban és az exportban működik, a GitHub-nézetben nem.
- (b) szöveges mutató az útvonallal (`szónézet: /szo/H7121`).
- (c) mindkettő: link és a teljes szócikk forrásfájlja.

**Javaslat: 1. + (c).** Indok: az 1. a meglévő proveniencia-helyet használja, és a cella rövid marad. A (c) a kétféle olvasási helyen is használható.

### DT-F131f — ⛔ elfogadási próba (3.1)

A felhasználó a renderelt próbalapon ítéli meg: *a szó jelentését és a hely motívumbeli funkcióját két külön dolognak látja-e?* Ugyanitt hagyja jóvá a címkék szövegét. Opciók: elfogad / javítással újra (legfeljebb két kör) / elvet (megállás, a döntés újranyitása).

### DT-F131g — ⛔ az éles lexikon felülírása (4.)

Az elfogadott próba után külön jóváhagyás az `--ir` futásra és a várt diffre. Opciók: felülír / vár (például a #36 vagy a #121 utánig).

## 6. Nyitott tételek (helyőrzők)

- **N-F131a** — az `elofordulasok.tsv` `jelentes_hu` mezője 7 ISTENTISZT-001 soron motívumbeli értelmezést hordoz („(NEM invokáció)”, „tagadó szerkezetben, a mulasztás vádjaként”, „Baál nevével”, „Jahve nevével, konkrét felszólítás…”). E feladat után az arany lap nem jeleníti meg. A mező sorsa (tisztítás, átkerülés a `funkcio`/`kapcsolodas` mezőbe, vagy megszüntetés) értelmező döntés, és a régi motívumok kiterjesztése előtt esedékes.
- **N-F131b** — a `jelentes_szam` minősítő alakja (`2.c (rokon)`, `2.c (tagadva)`) nincs benne a SEMA 2.2.2 értékkészletében. A generátor a kulcshoz levágja. Dokumentálandó vagy adatban rendezendő.
- **N-F131c** — Thayer-tagolás (a DT190 Thayer-ága): a G1941 kézi határai átmenetiek. A görög előfordulások Thayer-hozzárendelése (DT-F131c (b)) kutatói döntés.
- **N-F131d** — a #121-nek: az arany lapon e feladat után nem jelenik meg a 62 egységből a tW, a TBESH, a teljes UBS és a Mounce egysége (pontos lista: a napló M0-ja). A #121 M1 mintájához új minta kell. A szűkítésről a #121 dönt (DT272).
- **N-F131e** — a szónézet ága (DT272 (1), (e) második fele): a teljes szócikk, a releváns BDB-hivatkozás jelölése a magyar szakaszhoz igazítva, és a tW/TBESH/UBS/Mounce megjelenítése a szónézeten. Az olvasó-szerver feladata.

## 7. Elfogadási feltételek

1. A DT-F131a–e el van döntve, a bevezetés a döntést követi. A DT-F131f-en a felhasználó a renderelt lapon „igen”-t mondott, a DT-F131g-n jóváhagyta az éles felülírást.
2. Az arany lap szótári blokkjában a H7121, a H8034 és a G1941 jelentéstartománya a BDB, illetve a Thayer tagolásában áll. A motívumot hordozó szakaszok magyarul, kibontva állnak. A `horgonnyal` határ jelölve, az `elakad` explicit hiányként (teszttel). A görög szónál egy UBS-doménsor áll.
3. A tW, a TBESH, a teljes UBS és a Mounce nem áll az arany lapon; a helyükön a szónézet-mutató áll.
4. Az előfordulás-táblában a „Jelentés (a szó)” és a „Funkció (a motívumban)” két szomszédos oszlop. Mind a 32 soron van címke vagy kimondott hiány, és a címke forrása az ⓘ-ben áll.
5. A BDB saját példahelyei a fordított szakaszban felirat nélkül kiemelve állnak. A meg nem találtak listázva vannak, kitalált kiemelés nincs.
6. A szótári blokkban és a Jelentés-oszlopban a tiltott keretezés 0 találat.
7. A 7 többi lap bájtra változatlan. Nincs `forditasok.tsv`-írás. Az `ellenoriz.py`, a `feladatok.py ellenoriz`, a CI és a független ellenőrzés zöld.
8. A TSV-írás `split('\t')` / `'\t'.join()`, `csv` modul nélkül. A próbarender a repón kívül készült.

## 8. Döntésnapló és sorrend

- **Függés.** `fugg: [127, 110]`.
  - A #127 ugyanazt a generátort, `RENDER_BRIEF`-et, sablont, `SEMA`-t, `ellenoriz.py`-t és lapot írja; a feladat a #127 blokkjai utáni lapon mér (a megbízó: „legalább [127]”).
  - A #110 a felhasználó sorrendje miatt áll itt (2026-10-20: „#127 → #110 → a szótári réteg”). Fájlszintű ütközés nincs vele: a #110 csak a `jeloltek.tsv`-t írja. Ha a befogadás a sorrendet másként kezeli, a 110 kivehető.
  - `nem_fugg: [27, 38, 102, 103, 123]`. A #27 és a #38 a `forditasok.tsv`-t írja, de a DT272 szerint a fordítás nem előfeltétel. Az arany szavak sorai `kezi`/`opus` sorok, és ha mégis változnak, a `forras_hash` jelez. A #102 és a #103 a `bdb_vers_jelentes.tsv`-t generálja újra; ha előbb fut, az M0 újramér. A #123 az `elofordulasok.tsv`-t írja, de a felhasználó sorrendjében a #123 később jön (a #127 DT268-mintája).
  - **Egyeztetett eltérés (DT-F131h, 2026-10-26).** A `feladatok.py fuggesek` a #131-et levezetetten a #133-ra (`adat/bdb_szakaszok.tsv`) és a #144-re (`adat/bdb_szakasz_hu.tsv`) várónak mutatta. A felhasználó döntése: a #131 nem vár, a `nem_fugg` megkapja a 133-at és a 144-et; a mért hatás az arany Strongokon 0 (napló 1.3), és a 3. lépés rögzíti a két tábla H7121/H8034-sorainak hash-ét, hogy egy későbbi újragenerálás eltérése hangos legyen.
  - **A görög magyar szöveg (DT-F131c, 2026-10-26).** A tagolás a `thayer_szakaszok.tsv` (#132) szerint; a magyar szöveg a #142 szakaszsoraiból, amíg azok nincsenek, átmenetként a `teljes` sor kézi határokkal. Az `olvas` ezért a két Thayer-táblával, a DT-F131a (iv) miatt az `adat/glosszak_heber_hu.tsv`-vel bővült.
  - **Egyeztetett eltérés (DT-F131a (iv) következménye).** Az `adat/glosszak_heber_hu.tsv`-t a #140 (`megallt`) írja; az `olvas`-bővítés miatt a `fuggesek` a #131-et a #140-re várónak mutatta. A felhasználó a (iv)-ben a tábla meglévő `fo=igen` sorait (H7121, H8034) választotta, ezért a `nem_fugg` megkapja a 140-et; a 3. lépés e két sor hash-ét is rögzíti.
  - **Egyeztetett eltérés (F131.2, `ir`-bővítés).** Az `eszkozok/teszt_szerepmatrix.py` a szerepmátrix általános renderét az ISTENTISZT-001-en mint mintán vizsgálja; az arany lapon a gerinc a szerepmátrixot szűkíti (DT-F131a), ezért a teszt a kapcsolót (`LG.SZOTARI_GERINC_MOTIVUMOK`) kikapcsolja, és a többi lapon élő renderet vizsgálja tovább. A gerinc-render tesztje az `eszkozok/teszt_szotari_gerinc.py`.
  - **Befogadási teendő (a PROZA/#127 pár mintája, DT-F39g).** A #127 olvassa a `RENDER_BRIEF.md`-t, amelyet ez a feladat ír, ezért a #127 `nem_fugg`-ja megkapja e feladat számát. Enélkül kör keletkezik: #110 ↔ #127 ↔ #131. A #36 a `lexikon_general.py` miatt levezetetten e feladatra várna, ami ütközik a DT271-gyel („a #36 előbb fut”). Ezért a #36 `nem_fugg`-ja is megkapja a számot. A #10 és a #121 várakozása e feladatra helyes: a #10 a kész lapot zárja, a #121 a DT272 szerint e feladat után szűkít.
  - *Próbafutás* (a tervezet ideiglenes `F131_SZOTARI_GERINC_BRIEF.md` másolatával a gyökérben, és a #127 fejlécének ideiglenes `nem_fugg: [123, 131]` alakjával; a futás után mindkettő visszaállítva): 150 brief, 0 hiba, nincs kör; sorrend: #127 → e feladat. Levezetett várakozók: #10, #36, #121. Az első változat (`nem_fugg` nélkül, `lexikon_hivatkozasok.tsv`-vel az `ir`-ben) kört adott (#110 ↔ #123 ↔ #127 ↔ #131), és a #123-at tette volna e feladat elé. *(proveniencia: scope=a tervezet fejléce | forras=`python eszkozok/feladatok.py ellenoriz` és `fuggesek` | ts=2026-10-20)*
- **`munka: folyamat`.** A feladat generátort és generált lapot ír, motívumfájlt nem (`lexikon/` nem motívumfájl, DT28). A `lexikon/ISTENTISZT-001*` miatt az `olvas` a K1/3 szerint a motívum forrását, tematikus tanulmányát és naplóját is tartalmazza. Az `opus` a #127 mintája: a két réteg megkülönböztetése a lapon megjelenítési, de érzékeny munka.
- **DT272** (= DT338, 🟢): a megvalósított döntés, a (d) ponttal. A DT272 „Motívumlap-terv és -mockup” hivatkozása terv, nem döntés; e feladat nem épít rá.
- **DT190** (🟡): nyitva marad; a DT-F131b javaslata mindkét fő opciójával összefér.
- **DT235** (Mounce: kimarad): a DT272 (c) megerősíti.
- **DT-F131a–g, N-F131a–e:** l. 5–6. szakasz.
