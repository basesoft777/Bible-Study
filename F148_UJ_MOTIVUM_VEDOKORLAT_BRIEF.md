---
feladat: 148
cim: Az új motívumok védőkorlátjai — a szótári gerinc alapból bekapcsol, ellenőrző-szabályok, a szakaszcímke gépi levezetése (UJ_MOTIVUM_VEDOKORLAT)
kod: UJ_MOTIVUM_VEDOKORLAT
tipus: feladat
fazis: folyamat
munka: folyamat
modell: opus
allapot: nem_indult
ad: új motívumon a szótári gerinc kapcsoló nélkül fut, a még nem migrált régiek egy kivétellistán állnak (amely a #123 végén kiürül); az ellenoriz.py négy új szabálya gépileg kizárja a hiányos adatot és a hibás generált lapot; a szakaszcímke a jelentes_szam-ból gépileg vezetődik le, és eltérésnél jelez
kovetkezo: "Te: a #123 ALVIL-001 PR-jának merge-e után /kovetkezo; első lépés a 0. mérés, utána ⛔ DT-F148a–d"
olvas: [eszkozok/lexikon_general.py, eszkozok/ellenoriz.py, eszkozok/general.py, eszkozok/teszt_szotari_gerinc.py, eszkozok/teszt_szerepmatrix.py, eszkozok/teszt_ellenoriz_11.py, eszkozok/teszt_ellenoriz_13.py, eszkozok/glossza_lexikon_forditas.py, adat/SEMA.md, adat/elofordulasok.tsv, adat/motivumok.tsv, adat/szotar_szakasz_cimke.tsv, adat/lexikon_hivatkozasok.tsv, adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, adat/tiltott_fordulatok.tsv, adat/forditasok.tsv, lexikon/, DONTESEK.md, NYITOTT_FELADATOK.md, F131_SZOTARI_GERINC_BRIEF.md, naplok/F131_SZOTARI_GERINC_naplo.md, F123_MIGRACIO2_BRIEF.md, F125_GERINC_KARTYA_SZOVEG_BRIEF.md, MUNKAMENET.md, naplok/ELLENOR_ISTENTISZT001_ARANY_JAVITAS.md, naplok/ELLENOR_ISTENTISZT001_ARANY_JAVITAS_2.md, .github/workflows/ellenorzes.yml]
ir: [eszkozok/lexikon_general.py, eszkozok/ellenoriz.py, eszkozok/szakasz_cimke_levezet.py, eszkozok/teszt_szakasz_cimke_levezet.py, eszkozok/teszt_ellenoriz_vedokorlat.py, eszkozok/teszt_szotari_gerinc.py, eszkozok/teszt_szerepmatrix.py, adat/SEMA.md, adat/szotar_szakasz_cimke.tsv, naplok/F148_*]
fugg: []
nem_fugg: [7, 12, 27, 38, 102, 103, 121, 123, 131, 133, 144]
---

# F148_UJ_MOTIVUM_VEDOKORLAT_BRIEF.md — az új motívumok védőkorlátjai

*FELADATOK #148 (várható; a végleges számot a `/befogad` adja) · Modell: opus · v0 (tervezet) · 2026.10.29 · előzmény: DT272 (= DT338), DT372–DT374, DT377, DT401, N-F131a, N-F131b, D38, DT-F32a · párja: `F12_TEREMT002_PROZA_BRIEF.md` (#12)*

**A függésről.** A `fugg` mező feladatszintű, a tényleges előfeltétel viszont egy PR: a #123 **ALVIL-001-es** PR-jának merge-e. Ez a PR ugyanazt a három fájlt írja (`eszkozok/lexikon_general.py`, `adat/szotar_szakasz_cimke.tsv`, `adat/elofordulasok.tsv`), és az ALVIL-001-et rákapcsolja a gerincre. A `fugg: [123]` hibás volna, mert a #123 hét motívuma után futtatná a feladatot. A kivétellista viszont éppen azért kell, hogy a #123 *közben* is érvényes legyen. Ezért a kapu a `kovetkezo` mezőben áll („Te: …”). A `nem_fugg` a levezetett függéseket írja felül. A #7, #27, #38, #102, #103, #121, #131, #133 és #144 tábláit (`forditasok.tsv`, `bdb_*.tsv`) és a `lexikon_general.py`-t a feladat csak olvassa, a futáskori main-állapotukban: a levezetéshez és a regressziós teszthez. Ezekre várni évekig tartó (#38) vagy a main-en már mergelt, csak fejlécben nyitott (#121, #131) feladatokra várást jelentene. A #12 kifejezetten erre a feladatra vár; a #148 → #12 levezetett él (a #12 is írja a `lexikon_general.py`-t) kört okozna. A #123-ra a fenti ok miatt nem vár. Mérve: `python eszkozok/feladatok.py ellenoriz` 0 hiba, a `fuggesek`-ben a feladatnak nincs függése (2026-10-29, a két brief ideiglenesen a végleges nevén).

## 1. Cél

Az irány megfordul. Eddig a régi motívumokat hozták az új mércére (#11, #123). Mostantól az új motívumok eleve teljes adattal készülnek (#12, #13). Ehhez a rendszernek gépileg ki kell zárnia azt, ami az ISTENTISZT-001 arany lapján kézi javítókörökben derült ki:
- gerinc nélküli lap, mert a kapcsoló a motívumot nem ismeri;
- `jelentes_szam` nélküli sor (mért: ALVIL-001 0/72);
- `karoli_szo` nélküli sor (mért: HAMART-001 0/52);
- funkció-értelmezés a szó jelentésének mezőjében (N-F131a);
- helyőrző, „a(z)”, jelöletlen fordítatlan egység és nem létező tételre mutató hivatkozás a generált lapon (N-F131b, `ELLENOR_ISTENTISZT001_ARANY_JAVITAS.md` g2).

Három rész:
- **(a)** a gerinc-kapcsoló megfordítása;
- **(b)** négy ellenőrző-szabály tesztekkel;
- **(c)** a szakaszcímke gépi levezetése a `jelentes_szam`-ból, jelzéssel eltérésnél.

## 2. Hatókör

**Benne van:**
- **(a)** `eszkozok/lexikon_general.py`: a `SZOTARI_GERINC_MOTIVUMOK` (ma `frozenset({'ISTENTISZT-001'})`, 1778. sor) helyett kivétellista. Az új motívumon a gerinc alapból bekapcsol. A még nem migrált régiek a listán állnak. A `gerinc_aktiv()` a lista ellentettje lesz. A lista a #123 végén kiürül, és ezzel a kapcsoló megszűnik (a #123 utolsó motívuma törli a konstanst és a `gerinc_aktiv()` ágát).
- **(b)** `eszkozok/ellenoriz.py`: négy új tábla-szabály (18–21) tesztekkel. Az E1 CI-lépés (`.github/workflows/ellenorzes.yml`) futtatja, tehát a merge-kor a main-en **SÉRTÉS 0** kell.
- **(c)** új eszköz (`eszkozok/szakasz_cimke_levezet.py`): a `jelentes_szam` → szótári szakasz leképezést gépileg vezeti le. Eltérésnél jelez, és nem választ. Írni csak az eltérés nélküli sorokat írja, és csak `--ir` kapcsolóval.
- A SEMA 2.2.2 és 2.40 pontosítása a DT-F148b és a DT-F148c szerint.

**Nincs benne:**
- **A `MUNKAMENET.md` módosítása.** Az a #125-é. Ez a brief a 6. szakaszban csak javasolja a két új lépés szövegét; a #125 írja át.
- **Adatjavítás.** Nem tölti ki az ALVIL/HAMART/… hiányzó mezőit (az a #123), és nem tisztítja az ISTENTISZT-001 `jelentes_hu`-ját (N-F131a, az ISTENTISZT-menet).
- **Lap újragenerálása.** A `lexikon/` nem változik; a lapokat a tesztek repón kívüli ideiglenes könyvtárba renderelik.
- **A TEREMT-002 adata.** Az a #12 dolga.

**Párhuzamosan futó menetek, amelyek fájljához ez a feladat nem nyúl:** #123 (amíg az ALVIL-001-es PR nincs a main-en), az ISTENTISZT-001 „teljes” menete (N-F131a/b, 12–14. szerep), #124.

## 3. Lépések (⛔ a kötelező megállások)

**0. Modell-ellenőrzés és mérés.** A saját modellnév összevetése a `modell: opus` mezővel; eltérésnél megállás. Utána a friss main-en, saját szkripttel (`split('\t')`, a `naplok/F148_meres.py`-ba) mérni:
1. A #123 ALVIL-001-es PR-ja a main-en van-e (`git log origin/main`); ha nincs: **⛔ megállás**.
2. Motívumonként a `jelentes_szam`, a `karoli_szo` és a `lexikon_entry_id` kitöltöttsége az `adat/elofordulasok.tsv`-ben. A 2026-10-29-i állapot a brief írásakor mérve:

   | id | sor | `jelentes_szam` | `karoli_szo` | `lexikon_entry_id` |
   |---|---|---|---|---|
   | ALVIL-001 | 72 | 0 | 72 | 0 |
   | ANTROP-001 | 8 | 0 | 8 | 0 |
   | HAMART-001 | 52 | 26 | 0 | 42 |
   | HODIT-001 | 33 | 0 | 33 | 0 |
   | ISTENTISZT-001 | 33 | 33 | 33 | 33 |
   | KIRALY-001 | 9 | 4 | 9 | 5 |
   | MENNY-001 | 9 | 0 | 9 | 0 |
   | TEREMT-001 | 42 | 0 | 42 | 0 |
   | TEREMT-002 | 3 | 0 | 3 | 0 |

   `scope=adat/elofordulasok.tsv (9 id, 261 sor) | forras=split('\t')-számlálás (a brief írójának szkriptje) | ts=2026-10-29`
3. A gerincen álló motívumok listája (a main-en a `SZOTARI_GERINC_MOTIVUMOK` értéke; az ALVIL-001-es PR után várhatóan `ISTENTISZT-001`, `ALVIL-001`).
4. A négy új szabály (l. 2. lépés) próbafutása a main-en, kivétellistával: hány SÉRTÉS lenne. Ha a gerincen álló motívumon (ISTENTISZT-001, ALVIL-001) bármelyik szabály SÉRTÉST adna, például mert az N-F131a 8 sora még nincs kitisztítva: **⛔ megállás**. A szabály nem lazul, a sor nem kerül kivételre; az adatjavítás az ISTENTISZT-menet vagy a #123 dolga.
5. A `lexikon/` lapjain a 21. szabály mintáinak találatai laponként (helyőrző, „a(z)”, fordítatlan egység, nem létező DT/N).

Napló: `naplok/F148_UJ_MOTIVUM_VEDOKORLAT_naplo.md`, 0. szakasz.
**⛔ megállás: a mérés és a DT-F148a–d a felhasználóé.**

**1. A gerinc-kapcsoló megfordítása (a).** A DT-F148a szerint.
- A régi konstans helyett `GERINC_KIVETEL_MOTIVUMOK` (vagy a DT-F148a szerinti forma). Értéke a 0.3 mérés szerint a még nem migrált régiek, az ALVIL-001-es PR után várhatóan: ANTROP-001, HAMART-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001.
- A `gerinc_aktiv(id)` = `id not in GERINC_KIVETEL_MOTIVUMOK`.
- A két teszt, amely a konstanst felülírja (`eszkozok/teszt_szerepmatrix.py:45`, `eszkozok/teszt_szotari_gerinc.py:489`), az új formára áll át. A szerepmátrix általános renderét vizsgáló teszt a kivétellistát az összes motívumra állítja; ez nem lazítás, ugyanazt méri.
- **Elfogadás:** a meglévő 8 lexikonlap és 7 törzscikk repón kívüli ideiglenes könyvtárba renderelve bájtra azonos a main-en renderelt lappal (a kapcsoló megfordítása a meglévő lapokon semmit nem változtat). A TEREMT-002-nek ma nincs lapja (nincs `res_forras.tsv`-sora); rá ez a lépés nem ad kimenetet.
- Commit: `F148.1: a szótári gerinc alapból bekapcsol, kivétellista a nem migrált motívumokra`.

**2. Ellenőrző-szabályok (b).** Az `eszkozok/ellenoriz.py`-ban, a meglévő 17 szabály után. Ha közben más ág is számozott szabályt ad, a következő szabad szám. Minden szabályhoz pozitív és negatív teszt (`eszkozok/teszt_ellenoriz_vedokorlat.py`, a `teszt_ellenoriz_11.py` / `_13.py` mintájára, ideiglenes `adat/` könyvtárral). A kivétellista a szabályokban ugyanaz az objektum, mint a generátorban (import, nem másolat), hogy a kettő ne térhessen el. A `RETROAKTIV_IDK` (8. szabály) más fogalom; nem keverendő.
- **18. Gerinc-Strong címkéje.** A gerincen álló motívum minden előfordulás-sorára: a `lexikon_szotar` + `lexikon_entry_id` + `jelentes_szam` által kijelölt szakasznak legyen sora az `adat/szotar_szakasz_cimke.tsv`-ben. A leképezés ugyanaz a függvény, mint a generátoré (`kutatoi_szakasz`), vagy a 3. lépés eszköze. Kivétellistás motívumon: nem fut. Hiány: SÉRTÉS.
- **19. `jelentes_szam` és `karoli_szo` kötelező.** Nem kivétellistás motívum előfordulás-során a `karoli_szo`, a `lexikon_szotar`, a `lexikon_entry_id` és a `jelentes_szam` nem üres. Tagolatlan szócikknél (a DT-F148b szerint) az ott rögzített explicit érték is elfogadható; az üres soha. Kivétellistás motívumon JELENTÉS (darabszám), nem SÉRTÉS, így a #123 haladása is látszik.
- **20. A `jelentes_hu` a szóról szól (N-F131a).** Tiltó minta a funkció-értelmezésre. Kiinduló minták, a 0.4 mérés szerint pontosítandók: zárójeles tagadó minősítés („(NEM …)”), „tagadó szerkezet”, „vádjaként”, „motívum”, „funkció”, „invokáció” mint értelmező címke, valamint a `tiltott_fordulatok.tsv` mintái. A minták helye egy kódbeli lista vagy a `tiltott_fordulatok.tsv` új oszlopa; döntés a 0. ⛔-nél. **Kötelező negatív teszt:** az 1Kir 18:25–26 „Baál nevével” értéke BDB-szöveg, nem értelmezés (az ISTENTISZT-001 „teljes” menetének mérése szerint), ezért a szabály nem jelezheti. Gerincen álló motívumon SÉRTÉS, kivétellistáson JELENTÉS.
- **21. A generált lap tisztasága.** Minden `lexikon/*_TUDOMANYOS.md` (és `*_TORZSCIKK.md`) lapon:
  - (i) **nincs helyőrző:** `DT-F\d+`, `N-F\d+`, a generátor ismert helyőrző-szövegei (pl. „Kézzel írandó”);
  - (ii) **nincs „a(z)”** (a PR #502 névelő-hibája);
  - (iii) **nincs jelöletlen fordítatlan egység:** a `glossza_lexikon_forditas.py lista` `hianyzik` állapotú egységeinek száma egyenlő a lapon álló `(fordításra vár)` jelölések számával;
  - (iv) **minden `DT\d+` és `N\d+` hivatkozás létező tételre mutat:** a `DT` a `DONTESEK.md` táblasorára, az `N` a `NYITOTT_FELADATOK.md` tételére. Ez az N-F131b-eset: a generátor nem létező tételre hivatkozott.

  Súlyosság a DT-F148d szerint. Kivétellistás motívum lapján JELENTÉS, amíg a #123 el nem éri.
- Commit tételenként: `F148.2: 18. szabály …`, `F148.3: …`, és így tovább.

**3. A szakaszcímke gépi levezetése (c).** Új eszköz: `eszkozok/szakasz_cimke_levezet.py`, a CLAUDE.md shell- és TSV-szabályai szerint.
- `ellenoriz --id <ID>`: soronként a `jelentes_szam`-ból levezetett szakaszt adja. A BDB-nél a binyan + számozás → útvonal (`2.c` → `Qal/2/c`, `1` → `-/1/-`), a Thayernél a 2.39 kulcsa. A leképezés a `bdb_szakaszok.tsv` / `thayer_szakaszok.tsv` létező útvonalai közül választ, más forrásból nem.
- **Jelzés (nem választ, nem tölt ki):**
  - (1) a szótár saját példahelye (`bdb_vers_jelentes.tsv`, `thayer_vers_jelentes.tsv`) más pontra mutat, mint a levezetett, és egyik sem esik a másik alá (a `GerincHiba`-eset, DT374);
  - (2) két pont: alternatíva (`Nif'ál / Hif'íl`), két szám, vagy a példák két útvonalra mutatnak;
  - (3) üres mező;
  - (4) a jelnek nincs útvonala a szótárban;
  - (5) tagolatlan szócikk (a `bdb_vers_jelentes.tsv` `tagolatlan` útja, pl. a H0922 *bohu*);
  - (6) minősítő alak (`2.c (tagadva)`, N-F131b).
- Kimenet: `naplok/F148_levezetes_<ID>.tsv`; minden sor proveniencia-sorral (`scope=… | forras=szakasz_cimke_levezet.py | ts=…`).
- `--ir`: csak a jelzés nélküli sorokat írja a `szotar_szakasz_cimke.tsv`-be. A `cimke_hu` értékét a DT-F148c szerint adja. Írás előtt az eredeti sorokkal összevet, eltérésnél megáll (minta: `eszkozok/igazolas_migracio.py`).
- **Regresszió (kötelező teszt):** az ISTENTISZT-001 33 és az ALVIL-001 (az ALVIL-001-es PR szerinti) sorára a levezetett szakasz azonos a táblában ma álló kézi leképezéssel. Ahol nem, az lelet, nem lazítás: **⛔ megállás**, a felhasználó dönt.
- Commit: `F148.n: a szakaszcímke gépi levezetése (szakasz_cimke_levezet.py)`.

**4. SEMA.** A 2.2.2 pontban a DT-F148b értéke; a 2.40 pontban a levezetett sor proveniencia-alakja és a DT-F148c. Commit külön.

**5. Zárás.**
- `python eszkozok/ellenoriz.py`: SÉRTÉS 0 a main-állapoton.
- A tesztek: `teszt_ellenoriz_vedokorlat.py`, `teszt_szakasz_cimke_levezet.py`, `teszt_szotari_gerinc.py`, `teszt_szerepmatrix.py`, `teszt_ellenoriz_11.py`, `teszt_ellenoriz_13.py`.
- `python eszkozok/feladatok.py ellenoriz`: 0 hiba.
- Független ellenőr (`fuggetlen-ellenor`), draft PR, a brief fejléce. A 6. szakasz javaslata a #125-nek a naplóba kerül.
- **⛔ a merge a felhasználóé.**

## 4. Elfogadási feltételek

1. A meglévő 8 lexikonlap és 7 törzscikk ideiglenes könyvtárba renderelve bájtra azonos a main-en renderelttel (1. lépés).
2. Egy kivétellistán kívüli, tesztben felvett új motívum lapján a gerinc megjelenik kapcsolóbejegyzés nélkül (teszt).
3. A 18–21. szabálynak van pozitív és negatív tesztje. A 20. szabály az 1Kir 18:25–26 BDB-szövegét nem jelzi. A 21. szabály (iv) pontja egy kitalált `N9999` hivatkozást jelez, egy létezőt nem.
4. Az `ellenoriz.py` a main-állapoton SÉRTÉS 0, és az E1 CI-lépés zöld.
5. A levezető eszköz az ISTENTISZT-001 és az ALVIL-001 sorain a kézi leképezést adja vissza, és a hat jelzéstípus mindegyikére van teszteset.
6. A kivétellista egyetlen helyen áll; az `ellenoriz.py` importálja.
7. A `lexikon/`, az `adat/elofordulasok.tsv` és a `MUNKAMENET.md` nem változott.
8. Nincs `csv` modul; a szkriptek a CLAUDE.md wrapperével indulnak.

## 5. Döntésnapló

**DT-F148a — a kivétellista helye és formája.** Kérdés: hol éljen a még nem migrált motívumok listája, amelyen a gerinc nem fut, és a 19–21. szabály csak jelent?
- (1) **Kódbeli konstans** az `eszkozok/lexikon_general.py`-ban, az `ellenoriz.py` importálja. A #123 motívumonként egy sort töröl belőle, az utolsó a konstanst is.
- (2) **Új oszlop a `motivumok.tsv`-ben** (pl. `gerinc` = `kivétel`). Sémamódosítás, és a #123 végén egy kiürült oszlop marad utána.
- (3) A meglévő `motivumok.tsv` `statusz`/`forras_study` mezőből levezetve (migrált = van `motivumok/[ID].md` RÉS-jelölőkkel).

*Javaslat: (1).* Átmeneti állapotot ír le, amely a #123 végén megszűnik, ezért nem való az adatrétegbe. A (3) rejtett szabály volna: a migráció félkész állapotában egy `motivumok/[ID].md` már létezhet.

**DT-F148b — tagolatlan szócikk a `jelentes_szam`-ban.** Kérdés: mi álljon a mezőben, ha az előfordulás `lexikon_entry_id`-jének szócikke nem tagol? Ilyen a H0922 *bohu*: a BDB-ben csak `cim`/`fej` sora van, a `bdb_vers_jelentes.tsv` útja `tagolatlan`. A SEMA 2.2.2 szerint a `teljes`/`részlet` itt tilos.
- (1) **új, explicit érték** (pl. `tagolatlan`) a SEMA 2.2.2-ben, csak akkor, ha a `bdb_szakaszok.tsv`-ben a Strongnak nincs `point` sora; a gerinc a `fej` szakaszt mutatja, a címke a DT-F148c szerint;
- (2) a mező üres marad, és a 19. szabály tagolatlan szócikknél kivételt tesz;
- (3) az ilyen Strong nem lehet `lexikon_entry_id`; összetett soron (H8414+H0922) a tagolt token az entry, a tagolatlan csak szótári példahelyként jelenik meg.

*Javaslat: (3), és mellette (1) arra az esetre, ha a sor egyetlen Strongja tagolatlan.* A (2) üres mezőt engedne, ezt a CLAUDE.md 3. szabálya kizárja (a hiány explicit jelölendő).

**DT-F148c — a gépileg levezetett szakasz `cimke_hu`-ja.** Kérdés: ha az eszköz új szakaszt vezet le, honnan jön a címke szövege?
- (1) **a `bdb_szakasz_hu.tsv` (Thayernél a 2.39 magyar sora) szakaszszövegének első glosszája**, a 17. szabály tiltó mintáin és a `tiltott_fordulatok.tsv`-n átengedve, `forras=szakasz_cimke_levezet.py (gépi)` proveniencia-sorral. ⛔ csak akkor, ha jelzés van, a minta tiltott, vagy a glossza üres vagy fordításra vár.
- (2) a leképezés gépi, a `cimke_hu` mindig kézi, ⛔-vel motívumonként;
- (3) címke nélkül: a cella csak a jelet mutatja („*(nincs címke: Qal 2.c)*”), amíg kézi címke nem kerül be.

*Javaslat: (1).* A felhasználói kérés szerint a címke gépi, és ⛔ csak eltérésnél kell. A meglévő kézi címkék (ISTENTISZT-001, ALVIL-001) nem íródnak felül: az eszköz csak hiányzó sort ír.

**DT-F148d — a 21. szabály súlyossága az ágon és a main-en.** A g2-eset (`ELLENOR_ISTENTISZT001_ARANY_JAVITAS.md`): a `szamkiosztas` a forrásban kicserélte a helyőrzőt, a generált lapon `(DT-F121g)` maradt. Az ágon viszont a generátor új döntésre csak helyőrzővel hivatkozhat (a CI E26 a végleges számot elutasítja).
- (1) a helyőrző a lapon mindig SÉRTÉS; a generátor szövege új döntést csak a számkiosztás után idézhet;
- (2) **az ágon JELENTÉS, a main-en SÉRTÉS**; a merge utáni első main-futás így kikényszeríti az újragenerálást a kiosztott számmal;
- (3) mindig JELENTÉS.

*Javaslat: (2).* Az (1) az ágon lehetetlenné tenné az új döntés idézését. A (3) nem védene a g2-eset ellen. A (ii)–(iv) pont (a(z), fordítatlan, nem létező tétel) ágtól függetlenül SÉRTÉS a gerincen álló motívum lapján.

**N-F148a — a (iii) pont korlátja.** A „jelöletlen fordítatlan egység” mérése a #121 listázó eszközén múlik. Ami a generátor `forditas_ehhez()` hívásán kívül kerül angolul a lapra (szabad szövegű ⓘ, kolofon), azt a szabály nem látja. A 0.5 mérés megmutatja, van-e ilyen. Ha igen, nyitott tétel lesz.

## 6. Javaslat a #125-nek (a `MUNKAMENET.md` szövege — ezt nem ez a feladat írja)

A #125 (`F125_GERINC_KARTYA_SZOVEG_BRIEF.md`, `ir: [MUNKAMENET.md, …]`) a gerinc-kártya szövegével együtt ezt a két lépést is beírhatja a C-ívbe, a lexikonlap generálása elé:

> **C-x. Szakaszcímke (⛔ csak eltérésnél).** Az előfordulás-sorok `jelentes_szam`-ából a szótári szakaszt és a címkét a `python eszkozok/szakasz_cimke_levezet.py ellenoriz --id [ID]` vezeti le. Jelzés nélkül az `--ir` rögzíti. Jelzésnél (a szótár példahelye más pontra mutat, két pont, üres mező, nincs útvonal, tagolatlan szócikk, minősítő) a menet megáll, és a kutató dönt; kitöltés nem gyenge vagy asszociatív anyaggal történik.
>
> **C-y. Fordítás a lap előtt.** A lap generálása előtt a `python eszkozok/glossza_lexikon_forditas.py lista --id [ID]` listázza a lap fordítatlan szótári egységeit. A hiányzókat a #121 eszköze és kapui rögzítik az `adat/forditasok.tsv`-be. Ami a lapon fordítatlan marad, `(fordításra vár)` jelölést kap; a 21. szabály ezt méri.

| Verzió | Dátum | Változás |
|---|---|---|
| v0 | 2026.10.29 | Tervezet a felhasználó 2026-10-29-i kérésére („ez a teljes feladatsort orkesztráld le”), az orkesztrátor megbízásából; befogadásra vár. |
