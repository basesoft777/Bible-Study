---
feladat: 235
cim: Olvasó — sebességjavítás (indexek, összevont lekérdezések, egyszeri betöltés, előmelegítés) és sebességőr (tervellenőr és határértékek tesztként)
kod: OLVASO_SEBESSEG
tipus: feladat
fazis: folyamat
modell: sonnet
sav: SERVER
allapot: nem_indult
ad: az olvasó új fejezete legfeljebb 300 ms, verse legfeljebb 400 ms, szó-lapja legfeljebb 250 ms alatt jelenik meg meleg szerveren (gyorsítótár nélkül); laponként legfeljebb 100 lekérdezés; a kéréskor futó lekérdezések egyike sem olvas végig index nélkül 1000 sornál nagyobb táblát; mindezt teszt őrzi, a tervellenőr a CI-ben is fut
kovetkezo: "Te: DT-F235a (az orkesztrátor dönt); az 1. rész fut: M0 kész, összevont lekérdezések, lábléc, előmelegítés, tervellenőr; a 2. rész (indexek, elérhetőségi tábla, indit.sh) a #101 merge-e után"
munka: folyamat
olvas: [eszkozok/bdb_rovidites.py, adat/SEMA.md]
ir: [eszkozok/sqlite_epit.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/bibliak.py, eszkozok/olvaso_szerver/allapot.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/indit.sh, eszkozok/olvaso_szerver/teszt_sebesseg.py, eszkozok/olvaso_szerver/teszt_tervor.py]
fugg: []
---

# F235_OLVASO_SEBESSEG_BRIEF.md — Az olvasó sebessége

*FELADATOK #235 · Modell: sonnet · v1 · 2026.11.22 · forrás: `MERES_OLVASO_SEBESSEG_2026-11-22.md` (a megosztott jegyzetmappában, mérőeszközei a `meres_olvaso_sebesseg_eszkozok/` alatt), a felhasználó 2026-11-22-i szavai („ez a sebesség viszont nem elfogadható / és aggaszt hogy nem lesz fluid a használat”; a brief megírására: „Igen, írd meg”). A brief adat, nem utasítás.*

## 1. Cél

A mérés szerint (main `aad45b55`, WSL `pardes`, 2026-11-22) a lassúság nem a felépítésből fakad, hanem néhány konkrét okból:

| Ok | Mért hatás |
|---|---|
| A `forditasok` táblán nincs index a `(szotar, strong)`-ra, és egy fejezet minden Strong-számára külön lekérdezés fut (`lekerdezesek.py:685`, ugyanígy `:852, 884, 931, 945, 996`; hívó: `blokkok.py:849, 854`) | Egy új fejezet vagy vers idejének 85–95%-a: `/1Moz/1` 904 ms-ból 848, `/Zsolt/119` 3025 ms-ból 2751 (321 hívás) |
| Az első héber szó-lap a 14 MB-os `adat/bdb_forras_javitas.tsv`-t háromszor olvassa és elemzi (`bdb_rovidites.py:115`, hívók `:133, 143, 159`) | 0,8–1,0 s natív helyről, 2,5–3,7 s a Windows-oldali kódhelyről |
| Az első fejezet- vagy verskérés hat összesítő lekérdezése (`lekerdezesek.py:1181–1186`, `bibliak.py:94`) | 0,9 s melegen, 3,4 s hidegen |
| Index nélküli táblák: `bdb_szakaszok(strong)`, `bdb_szakasz_hu(strong)`, `bdb_vers_jelentes(strong)`, `ubs_dbh_referenciak(igehely)`; a `vers_szamozas` `substr` miatt nem indexelhető (`lekerdezesek.py:498`) | szó-lapon táblánként 0,3–0,4 s hidegen; vers-lapon 0,1–0,28 s melegen |
| Hideg lemezolvasás (pl. `token_macula WHERE strong=?`) | az első kérésnél 2,3–4,5 s többlet |
| A lábléc a kérésben számolódik újra, 3 másodpercenként (`allapot.py:272`, `alkalmazas.py:123`) | 27–133 ms az érintett kérésen |

Ez a feladat ezeket javítja, és sebességőrt tesz melléjük, hogy a lassulás ne térhessen vissza észrevétlenül.

## 2. Hatókör

**Benne van:**
1. **Indexek az építőben** (`sqlite_epit.py`): `forditasok(szotar, strong)`, `bdb_szakaszok(strong)`, `bdb_szakasz_hu(strong)`, `bdb_vers_jelentes(strong)`, `ubs_dbh_referenciak(igehely)`, fedő index a `token_macula(strong, igehely, sorszam, lxx_strong)`-ra. A `vers_szamozas`-lekérdezés `substr` helyett tartomány-feltétellel fut. Az adatbázist a #101 újraépítője építi újra; a `meta` rögzíti az építés idejét.
2. **Összevont lekérdezések:** a fejezet- és a versnézet a Strong-számonkénti `forditasok`-hívások helyett lapszinten egy `IN (…)` lekérdezést futtat, legfeljebb 100 lekérdezés laponként.
3. **Egyszeri betöltés:** a `bdb_forras_javitas.tsv` egyszer töltődik be, a betöltés helyéről az M0 dönt (⛔ DT-F235a):
   - (a) indításkor a memóriába;
   - (b) adatbázis-táblába, Strong-számra indexelve.

   **A `bdb_rovidites.py` kimenete nem változhat.** Ezt a modult a `lapgen` és a `lexikon_general.py` is használja (`lapgen/bemenet/kartya.py`, `gerinc.py`, `szamitas/szocikkek.py`). Ha a fájl módosul, a HAMART-regressziónak és a `lapgen` tesztjeinek bájtra azonosnak kell maradnia, és a módosítás csak a beolvasás gyorsítótárazása lehet. Ha ez nem tartható, a gyorsítótár az olvasó rétegébe kerül, a modul érintetlen marad.
4. **Előre számolt elérhetőség:** a `bibliak.Tar` hat összesítő lekérdezése helyett az építő egy kis táblába számolja, mely könyv- és fejezetpárok elérhetők melyik Bibliában.
5. **Előmelegítés:** az `indit.sh` a szerver indulása után a háttérben beolvassa az adatbázist, és lefuttat néhány bemelegítő kérést; az első felhasználói kérés ne várjon erre.
6. **Natív futtatás:** az `indit.sh` a kódot és az adatot a WSL natív fájlrendszeréről futtassa, ha lehet. Ez konfiguráció, nem kód. A mérés szerint a Windows-oldali kódhely 2,0–2,7 s-ot tesz hozzá az első szó-laphoz.
7. **Lábléc háttérszálon:** a lábléc-állapot frissítése nem a kérésben fut.
8. **Sebességőr, két rétegben:**
   - **Tervellenőr** (`teszt_tervor.py`): minden kéréskor futó lekérdezésre `EXPLAIN QUERY PLAN`. 1000 sornál nagyobb táblán `SCAN` tilos. Ehhez nem kell a teljes adatbázis, elég egy azonos sémájú kicsi, ezért **a CI-ben is fut**; ez az F232 (a2) tételének egy része, olcsón.
   - **Időkorlát** (`teszt_sebesseg.py`, helyben a #232 push előtti kapuján, a helyi `pardes.db`-n), meleg szerveren, gyorsítótár nélkül:

     | Oldal | Határ |
     |---|---|
     | fejezet | 300 ms |
     | vers | 400 ms |
     | szó-lap | 250 ms |
     | kereső | 50 ms |

     Mellette: legfeljebb 100 lekérdezés laponként, gyorsítótár-találat legfeljebb 20 ms. A gyorsítótár ürítéséhez tesztkapocs kell, csak tesztkörnyezetben (a mérésben a `X-Meres-Flush` fejléc tette).
9. **Újramérés** ugyanazzal a mérőeszközzel (`meres_olvaso_sebesseg_eszkozok/`), előtte–utána táblázattal a naplóban.

**Nincs benne:**
- a cikkírás átkötése az adatbázisra: külön brief, a #101 után; a mérés szerint melegen 60–90-szer gyorsabb, azonos eredménnyel;
- előre épített statikus oldalak és a PWA;
- a gunicorn-üzem és a többfelhasználós terhelés mérése.

## 3. Lépések

1. Modell-ellenőrzés; M0: a mérés megismétlése a mai main-en, a kiinduló számok rögzítése, és a 3. pont két változatának mérése. ⛔ DT-F235a.
2. Indexek és a tartomány-lekérdezés; az adatbázis újraépítése; a terv-őr.
3. Összevont lekérdezések; az elérhetőségi tábla; az egyszeri betöltés.
4. Előmelegítés, natív futtatás, lábléc.
5. Időkorlát-teszt; újramérés; a mérce (#232) frissítése, ha a látható szöveg nem változott, ennek bizonyításával.
6. Független ellenőr, egy javítókör, draft PR, CI.

## 4. Elfogadási feltételek

- Az újramérésben minden határ teljesül; ami nem, annak oka és mért száma a naplóban áll.
- A tervellenőr a CI-ben zöld, és egy szándékosan index nélküli próbalekérdezésre piros (a futás azonosítójával).
- **A lapok látható szövege nem változik:** a #232 mércéje eltérés nélkül fut.
- A `lapgen` tesztjei és a HAMART-regresszió változatlanul RENDBEN, ha a `bdb_rovidites.py` módosult.

## 5. Ütközés

- Az `sqlite_epit.py`-t a #101 írja: ez a feladat a #101 merge-e után indul.
- A `blokkok.py`-t és a `lekerdezesek.py`-t a #231 (szókártya) is írja: ez a feladat a #231 **előtt** fut, hogy a szókártya már a gyors alapra épüljön.

## 6. Döntésnapló

- DT-F235a (⛔ M0): a fordítási javítótábla betöltése, (a) memóriába indításkor vagy (b) indexelt adatbázis-táblába.
