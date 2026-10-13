---
feladat: 92
cim: A pardes.db kiegészítése az olvasói lapokhoz — a hat hiány pótlása, újraépítés, egyezési teszt
kod: PARDES_DB_OLVASOI
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: lezarva
ad: a pardes.db új táblái (token_macula, lxx_token, bdb_alias, nave_vers, lxx_versszam) táblaszintű licenccel és meta-sorral, az adatbázis újraépítve; a #60 pilot D1–D5 mérése mindkét szakaszon újrafuttatva (D1 39/39, D2 0 eltérés, D5 friss); mérethatár nélkül (DT127); index a magyar szavakra (v1.1)
kovetkezo: "—; nyitott: DT-F92c (kanonikus ÚSZ-számlálás), DT-F92d (a térkép versbeosztása), N-F92a"
ag: claude/f92-pardes-db-olvasoi
pr: PRSZAM
lezarva_osszegzes: "pardes.db +5 olvasói tábla (token_macula, lxx_token, lxx_versszam, bdb_alias, nave_vers) meta-sorral és licenccel, magyar szó index (K5 334→9 ms); D1 1Móz 39/39, Zsolt 22 38/39 (forrásoldali hiány); D2 0 eltérés az ÚSZ-láncelemek kivételével (elfogadva, nem végleges); térkép nem forrás; DT-F92a–d, N-F92a"
olvas: [eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, naplok/SQLITE_EPIT_meres.md, adat/SEMA.md, adat/licencek.tsv, "konkordancia/Macula_heber_*.tsv", "konkordancia/LXX_OS/*.tsv", konkordancia/BDB_strong_alias.tsv, konkordancia/Nave_basokant.tsv, konkordancia/LXX_versszintu_parok.tsv, ADATVAGYON_TERV.md, DONTESEK.md]
ir: [eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, eszkozok/nave_bontas.py, eszkozok/f92_db_igazolas.py, naplok/PARDES_DB_OLVASOI_db_igazolas.md, eszkozok/olvaso_pilot/sablon.html, DONTESEK.md, eszkozok/olvaso_pilot/db_meres.py, eszkozok/olvaso_pilot/teszt_olvaso_pilot.py, NYITOTT_FELADATOK.md, naplok/SQLITE_EPIT_meres.md, adat/SEMA.md, naplok/PARDES_DB_OLVASOI_M0.md, naplok/PARDES_DB_OLVASOI_zaras.md]
fugg: []
nem_fugg: [52]
---

# A `pardes.db` kiegészítése az olvasói lapokhoz — a hat hiány pótlása, újraépítés, egyezési teszt (PARDES_DB_OLVASOI)

*Befogadásra váró brief-tervezet. Forrás: a #60 olvasói pilot értékelő jelentése (`naplok/OLVASOI_PILOT_ertekeles.md` 8.3, M2b D1–D5) és a felhasználó döntése a chatben (2026-10-12): a hat hiány pótlása, saját szerveres kiszolgálással (DT127). A fejlécet a `/befogad` adja.*

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

A feladat: a hat hiány pótlása az építőben, az adatbázis újraépítése, és a TSV–adatbázis egyezés tesztje. **Mérethatár nincs** (DT127: saját szerver megoldható; a Netlify-keret nem köt). A méretet mérni és naplózni kell, de nem elfogadási feltétel.

## 2. Hatókör

**Benne van**
- Új táblák az `eszkozok/sqlite_epit.py`-ban, mindegyik `meta`-sorral (sorszám, hash) és táblaszintű licenccel (DT113, a #89 után):
  - `token_macula`: héber token → igealak-kód, szófaj, `lxx_strong`, `lxx_szo` (Macula héber);
  - `lxx_token`: LXX-vers, pozíció, szóalak, lemma, Strong, morfológia (LXX_OS);
  - `bdb_alias` (a `BDB_strong_alias.tsv`-ből);
  - `nave_vers`: téma × vers. A tartomány-bontás szabálya a pilot `adat.py`-jából az építőbe (vagy közös modulba) kerül, hogy egy helyen éljen;
  - `lxx_versszam`: Károli-vers → LXX-vers minden versre (az LXX_OS verskulcsából).
- Index a magyar szavakra (v1.1): kisbetűs, normalizált szóoszlop (`hu_szo_kis`, `szo_kis`; a Károli-írásjel nélkül) a `token_par`-ban és a `token_karoli`-ban, rajta index. Ok: a #76 kiinduló mérése (2026-10-12) szerint a magyar szóra és frázisra keresés ma 1–3 s (pontos „kép” 3,2 s; „segítségül hív…” frázis 1,3 s), mert ezeken a mezőkön nincs index. A szótövezés nem része (külön döntés).
- Az adatbázis újraépítése a mostani TSV-kből; a `naplok/SQLITE_EPIT_meres.md` táblánkénti mérete frissítve.
- A #60 `db_meres.py` D1–D5 újrafuttatása mindkét pilot-szakaszon (1Móz 1–25, Zsolt 22).
- Tesztek: minden új táblára betöltési teszt; a D2-egyezés tesztje; az index használatának tesztje (a lekérdezésterv indexet használ).

**Nincs benne**
- A kiszolgálás (szerver, API, felület): a #76 (#25a) dolga, a DT127 bemenetként megy oda.
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
- **K5.** A magyar szóra (pontos alak, kisbetűsen) és a kétszavas magyar frázisra keresés 100 ms alatt fut ugyanazon a gépen, ahol a kiinduló mérés 1–3 s volt; a mérés proveniencia-sorral a jelentésben.

## 5. Kapcsolódás

#79 (SQLITE_EPIT), #88 (TIPNR_NORMALIZALAS), #89 (LICENC_RENDEZES), #60 (OLVASOI_PILOT: `db_meres.py`, értékelő jelentés 8.3), #76 (OLVASOI_KONKORDANCIA, hosting ⛔), DT113, DT127, ADATVAGYON_TERV 3. szakasz.

## 6. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-12 | Befogadás (F92.1): a hat hiány pótlása, újraépítés, egyezési teszt; mérethatár nélkül (DT127). | a felhasználó jóváhagyása a chatben (2026-10-12) |
| v1.1 | 2026-10-13 | Index a magyar szavakra (normalizált kisbetűs szóoszlop + index a `token_par`-ban és a `token_karoli`-ban), K5. Ok: a #76 kiinduló mérése, magyar szóra és frázisra 1–3 s. A szótövezés nem része. | a felhasználó jóváhagyása a chatben (2026-10-13) |
| v2 | 2026-10-13 | DT-F92a: az M0 táblaterv és a mért méret (kb. +209 MB) jóváhagyva. (1) `lxx_versszam`: a versifikációs térkép második forrásként elfogadva, minden ÓSZ versre sor, `forras` = `LXX_OS` / `versificacios_terkep` / `nincs` (kitöltés nélkül); ahol mindkettő ad értéket, összevetés, az eltérés naplózva. (2) `nave_vers`: fejezet-szintű és igehely nélküli sor nem kerül bele (a kihagyott sorok száma a zárójelentésbe; teszt: `nave_basokant` sorszáma = bontott + kihagyott); a bontás közös modulban, `eszkozok/nave_bontas.py`. (3) `bdb_alias` licenc: `[BDB, projekt_adat]`, új `licencek.tsv`-sor nélkül. (4) `db_meres.py` és `teszt_olvaso_pilot.py` minimális módosítása (csak az olvasási út) engedélyezve, az `ir` listába felvéve. (5) `bovites.py` nem áll át; N-F92a: a #76 kiolvasója a közös modult használja, a pilot-példány ott megszűnik. (6) Macula–TAHOT: vers+Strong illesztés; az egy versben többször álló azonos Strong kétértelmű, külön számolva és jelentve, feloldás pozíció-sorrend szerint; a „0 eltérés” ilyenkor nem jelent helyes illesztést. | a felhasználó jóváhagyása a chatben (2026-10-13) |
| v3 | 2026-10-13 | DT-F92b: (K1) Zsolt 22 D1 = 38/39 elfogadva „részben”-ként (a 39. blokk forrásoldali hiány, nem adatbázis-hiány; a lap explicit jelöli, kitöltés tilos). (K2) a TAGNT `+` láncelemek miatti ÚSZ-eltérés (27/1230 és 11/305 lap) a #92 lezárásához elfogadva, nem végleges; a kanonikus számlálás: DT-F92c. (3.) A versifikációs térkép VISSZAVONVA második forrásként (módosítja DT-F92a 1.-et): `lxx_versszam.forras` = `LXX_OS` / `nincs`, a térkép értéke csak a nem kanonikus `terkep_ertek` oszlopban; a térkép beosztása: DT-F92d. | a felhasználó jóváhagyása a chatben (2026-10-13) |
