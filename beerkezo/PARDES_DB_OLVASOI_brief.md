# A `pardes.db` kiegészítése az olvasói lapokhoz — a hat hiány pótlása, újraépítés, egyezési teszt (PARDES_DB_OLVASOI)

*Befogadásra váró brief-tervezet. Forrás: a #60 olvasói pilot értékelő jelentése (`naplok/OLVASOI_PILOT_ertekeles.md` 8.3, M2b D1–D5) és a felhasználó döntése a chatben (2026-10-12): a hat hiány pótlása, saját szerveres kiszolgálással (DT-F92a). A fejlécet a `/befogad` adja.*

**Javasolt fejléc-adatok:** `tipus: feladat` · `fazis: 1` · `modell: sonnet` · `munka: adat` · `fugg: [88, 89]` (mindhárom az `eszkozok/sqlite_epit.py`-t írja; a #88 → #89 → ez a sorrend) · `kovetkezo: "/kovetkezo; ⛔ M0 után (a táblaterv és a mért méret jóváhagyása)"`.

## 1. Cél

A #60 pilot mérése szerint az olvasói lap 39 blokkjából 35 állítható elő csak a `pardes.db`-ből (D1). A hiányzó blokkok és az eltérések (D2):

1. igealak-kód és szófaj (Macula héber);
2. szavankénti héber–görög párosítás (Macula héber);
3. görög szóalak és az LXX-vers szavai (LXX_OS);
4. BDB-alias tábla (`konkordancia/BDB_strong_alias.tsv`; a TSV-úttal 9 + 6 / 1 + 1 szó-lapon eltér);
5. Nave-témák versekre bontása (ma a pilot `adat.py` gépi szabálya);
6. LXX-versszám minden versre (ma 356 / 28 versnél eltér vagy hiányzik, mert az `lxx_versszintu_parok` csak Strong-párral rendelkező versre ad sort).

Az adatbázis ráadásul elmarad a forrás-TSV-ktől (D5: TAGNT +350 sor, `token_par`), ezért az ÚSZ-előfordulás 117 / 52 görög lapon eltér.

A feladat: a hat hiány pótlása az építőben, az adatbázis újraépítése, és a TSV–adatbázis egyezés tesztje. **Mérethatár nincs** (DT-F92a: saját szerver megoldható; a Netlify-keret nem köt). A méretet mérni és naplózni kell, de nem elfogadási feltétel.

## 2. Hatókör

**Benne van**
- Új táblák az `eszkozok/sqlite_epit.py`-ban, mindegyik `meta`-sorral (sorszám, hash) és táblaszintű licenccel (DT113, a #89 után):
  - `token_macula`: héber token → igealak-kód, szófaj, `lxx_strong`, `lxx_szo` (Macula héber);
  - `lxx_token`: LXX-vers, pozíció, szóalak, lemma, Strong, morfológia (LXX_OS);
  - `bdb_alias` (a `BDB_strong_alias.tsv`-ből);
  - `nave_vers`: téma × vers. A tartomány-bontás szabálya a pilot `adat.py`-jából az építőbe (vagy közös modulba) kerül, hogy egy helyen éljen;
  - `lxx_versszam`: Károli-vers → LXX-vers minden versre (az LXX_OS verskulcsából).
- Az adatbázis újraépítése a mostani TSV-kből; a `naplok/SQLITE_EPIT_meres.md` táblánkénti mérete frissítve.
- A #60 `db_meres.py` D1–D5 újrafuttatása mindkét pilot-szakaszon (1Móz 1–25, Zsolt 22).
- Tesztek: minden új táblára betöltési teszt; a D2-egyezés tesztje.

**Nincs benne**
- A kiszolgálás (szerver, API, felület): a #76 (#25a) dolga, a DT-F92a bemenetként megy oda.
- Karcsú olvasói kivonat (`olvaso.db`): saját szerver mellett nem kell; később optimalizálásként felvehető.
- Adatjavítás a forrás-TSV-kben (pl. a `tW_szocikkek.tsv` U+FFFD-je, a zsoltárfeliratok számozása — az utóbbi a #91).

## 3. Lépések

- **M0 — felmérés (csak olvas).** Táblaterv oszlopokkal és kulcsokkal; a betöltendő sorok száma és a várható méret forrástáblánként; a Nave-bontás szabályának helye. ⛔ A táblaterv és a mért méret jóváhagyása.
- **M1 — építés.** Az új táblák az építőben, tesztekkel; újraépítés.
- **M2 — mérés.** `db_meres.py` mindkét szakaszon; D1, D2, D5 eredménye a jelentésben, proveniencia-sorral.
- **M3 — zárás.** Zárójelentés, független ellenőr, draft PR.

## 4. Elfogadás

- **K1.** A D1: mind a 39 blokk előállítható csak a `pardes.db`-ből, mindkét szakaszon.
- **K2.** A D2: 0 eltérés a TSV-út és az adatbázis-út között minden blokkon, mindkét szakaszon; ahol mégis eltér, az ok a forrásban dokumentált, és a felhasználó elfogadja.
- **K3.** A D5: a `meta` hash minden betöltött táblára egyezik a forrás-TSV mostani állapotával.
- **K4.** A tesztek zöldek, a CI zöld, a független ellenőr eltérés nélkül zár.

## 5. Kapcsolódás

#79 (SQLITE_EPIT), #88 (TIPNR_NORMALIZALAS), #89 (LICENC_RENDEZES), #60 (OLVASOI_PILOT: `db_meres.py`, értékelő jelentés 8.3), #76 (OLVASOI_KONKORDANCIA, hosting ⛔), DT113, DT-F92a, ADATVAGYON_TERV 3. szakasz.
