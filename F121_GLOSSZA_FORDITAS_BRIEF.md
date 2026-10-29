---
feladat: 121
cim: A lexikonoldalak szótári glosszáinak és szócikkeinek magyar fordítása a gyorsítótárba, a #36 előtt
kod: GLOSSZA_FORDITAS
tipus: feladat
fazis: 2
modell: sonnet
munka: adat
allapot: megallt
ag: claude/f121-glossza-istentiszt-10e2a8
ad: **szűkítve (DT387, 2026-10-28):** az ISTENTISZT-001 lexikonlapon `(fordításra vár)` jelölést viselő egyedi szótári egységek (a #131 után 6: 5 UBS DBH definíció + az UBS DNTG G1941 56.15 glosszája) magyar fordítása az adat/forditasok.tsv-ben, kapukon átengedve, forrás-hash-sel; a 13. szabály az UBS_DBH-ra is ellenőriz; az eszközök és a terminológia a többi lapra is használhatók. *(Eredeti ad: a 8 motívum 454 egysége, UBS DBH/DNTG, TBESH, tW, Mounce.)*
kovetkezo: "Te: ⛔ a mankók 9 eltérő sorának kézi ítélete (naplok/F121_GLOSSZA_FORDITAS_naplo.md 10.); utána a PR #504 zöld CI-je; a merge a felhasználóé"
olvas: [tematikus_lezart/ISTENTISZT-001*, tematikus_lezart/naplok/ISTENTISZT-001*, konkordancia/SECE_G_teljes.tsv, konkordancia/SECE_H_teljes.tsv, konkordancia/LXX_versszintu_parok.tsv, adat/forditasok.tsv, adat/terminologia.tsv, adat/licencek.tsv, adat/SEMA.md, adat/karoli_strong/, konkordancia/Karoli_1908.tsv, eszkozok/bdb_adatblokk.py, naplok/FORDITAS_P3_kimenet.tsv, eszkozok/lexikon_general.py, eszkozok/general.py, eszkozok/emeles.py, eszkozok/forditas_kapuk.py, eszkozok/ellenoriz.py, konkordancia/tW_szocikkek.tsv, konkordancia/UBS_DBH_jelentesek.tsv, konkordancia/UBS_DNTG_jelentesek.tsv, konkordancia/TBESH.txt, konkordancia/MCGED_teljes.tsv, archivum/ISTENTISZT-001/, F38_BDB_FORDITAS_BRIEF.md, F28_EMELES_BRIEF.md, generalt_proba/F09_szotar_s2_proba/lexikon/]
ir: [adat/forditasok.tsv, adat/terminologia.tsv, adat/tiltott_fordulatok.tsv, adat/licencek.tsv, adat/SEMA.md, eszkozok/glossza_lexikon_forditas.py, eszkozok/teszt_glossza_lexikon_forditas.py, naplok/F121_GLOSSZA_FORDITAS_manko.tsv, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/teszt_ubs_dbh.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_szerver/teszt_szintek.py, eszkozok/olvaso_szerver/konfig/hozzaferes_proba.toml, eszkozok/teszt_szotari_gerinc.py, eszkozok/teszt_szerepmatrix.py, naplok/F121_ubs_csomag_tervezet.py, naplok/F121_ubs_csomag_tervezet.tsv, naplok/F121_ubs_csomag_rogzit.py, eszkozok/teszt_ellenoriz_13.py, DONTESEK.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, eszkozok/lexikon_general.py, eszkozok/ellenoriz.py, eszkozok/teszt_forditas_kapuk.py, eszkozok/teszt_szerepmatrix.py, eszkozok/teszt_szotari_gerinc.py, eszkozok/bdb_jelolt/forras_javit.py, eszkozok/bdb_jelolt/teszt_bont.py, eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/tesztek/test_szabalyok.py, eszkozok/olvaso_szerver/bdb_szelet.py, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, eszkozok/olvaso_szerver/teszt_bdb_vers_jelentes.py, eszkozok/thayer_jelolt/vers_jelentes.py, eszkozok/ellenoriz.py, eszkozok/forditas_kapuk.py, eszkozok/teszt_forditas_kapuk.py, naplok/F121_GLOSSZA_FORDITAS_naplo.md, naplok/F121_GLOSSZA_FORDITAS_lista.tsv, naplok/F121_GLOSSZA_FORDITAS_bukottak.tsv, naplok/F121_GLOSSZA_FORDITAS_szojegyzek_javaslat.tsv, naplok/F121_GLOSSZA_FORDITAS_visszamenoleges.tsv]
fugg: [11]
nem_fugg: [7, 27, 38]
---

# F121_GLOSSZA_FORDITAS_BRIEF.md — a lexikonoldalak szótári glosszáinak magyar fordítása

*FELADATOK #121 · Modell: sonnet · v1 · 2026.10.18*

## 1. Cél

A #9 (SZOTAR S2) óta a lexikonoldal szerepmátrixa öt szótárból hoz angol szöveget, amelynek
magyar fordítása a `adat/forditasok.tsv`-ből (SEMA 2.14) jönne. Ilyen sor ma egy sincs, ezért
ezeken a helyeken `*(fordításra vár)*` áll (N-F09a). A #36 (az éles `lexikon/` újragenerálása)
ezt a jelölést mind a nyolc éles lapra kivinné. Ennek a feladatnak az eredménye: a nyolc
motívum hiányzó egységei lefordítva a gyorsítótárban, úgy, hogy a #36 utáni éles lapokon a
jelölés csak ott maradjon, ahol egy döntés kizárja a fordítást (D2, D4).

A fordítás nem veszett el. A migráció előtti éles lapokon azért volt 0 jelölés, mert ezek a
blokkok csak a #9 óta vannak a lapon.

## 2. Felmérés (2026.10.18, a brief írásakor)

*proveniencia: scope=a 8 motívum `lexikon` célú renderje (`general.py --cel lexikon --id <ID> --kimenet <repón kívüli könyvtár>`), a `lexikon_general.forditas_ehhez` hívásainak naplózásával (monkeypatch, a repó nem változott) | forras=a munkafa `main`-állapota (2eaab468), `adat/forditasok.tsv` (737 adatsor) | ts=2026-10-18. A mérőszkriptek és a teljes kulcslista (540 sor, forráshash-sel) a session közös jegyzetmappájában: `F121_meres_naplozo.py`, `F121_meres_elemez.py`, `F121_meres_kulcsok.tsv`. Az M0 ezt a mérést a saját lista-eszközével megismétli; a brief számai addig tájékoztatók.*

**A jelölés helyei.** A mai generátor kimenete jelölésszámban azonos a
`generalt_proba/F09_szotar_s2_proba/` lapjaival. Az élő `lexikon/ISTENTISZT-001_TUDOMANYOS.md`
is azonos a próbalappal: 65 jelölés 40 sorban (a laza `grep -c 'fordításra vár'` 43-at ad, mert a bevezető mondatokat is számolja; a HAMART-001-en ugyanígy 106 ↔ 103). A többi hét éles lap még a régi
generátorral készült, ezeken 0 jelölés van.

| Motívum | sor (`grep -c '(fordításra vár)'`) | jelölés | hiányzó egyedi egység | forráskarakter |
|---|---|---|---|---|
| HAMART-001 | 103 | 155 | 146 | 67 886 |
| ANTROP-001 | 61 | 100 | 97 | 35 123 |
| MENNY-001 | 52 | 77 | 75 | 58 246 |
| ISTENTISZT-001 | 40 | 65 | 62 | 22 818 |
| KIRALY-001 | 36 | 52 | 48 | 23 333 |
| HODIT-001 | 10 | 17 | 17 | 1 538 |
| ALVIL-001 | 11 | 13 | 10 | 8 720 |
| TEREMT-001 | 7 | 9 | 8 | 2 340 |
| **össz.** | **320** | **488** | **454** (9 egység két motívumon is áll) | **≈205 700** |

*(A sorösszeg az N-F09a „320 sor”-ával egyezik. A „hiányzó egyedi egység” oszlop a BDB-nyelvi
hátteret és a SECE-t nem tartalmazza, l. lent; a jelölésszám a BDB-nyelvi háttér 18 helyét
igen.)*

**Szótáranként (egyedi kulcs: `szotar`+`strong`+`entry_id`+`jelentes_szam`+`mezo`):**

| `szotar` | `jelentes_szam` / `mezo` | a lap keresi | megvan | hiányzik | hiányzó karakter | licenc (`adat/licencek.tsv`) |
|---|---|---|---|---|---|---|
| `tW_szocikkek` | `—` / `forditas_hu` | 78 | 0 | 78 | 174 154 (min. 624, medián 1 824, max. 5 526 / szócikk) | CC BY-SA 4.0, kereskedelmi: feltételesen (védjegy) |
| `UBS_DBH` | `—` / `definicio_hu` | 134 | 0 | 134 | 15 890 | CC BY-SA 4.0 |
| `UBS_DBH` | `—` / `glosszak_hu` | 134 | 0 | 134 | 2 532 | CC BY-SA 4.0 |
| `UBS_DNTG` | L–N kód / `definicio_hu` | 53 | 20 | 33 | 2 842 | CC BY-SA 4.0 |
| `UBS_DNTG` | L–N kód / `glosszak_hu` | 53 | 20 | 33 | 862 | CC BY-SA 4.0 |
| `TBESH` | `teljes` / `forditas_hu` | 29 | 0 | 29 | 5 564 | CC BY 4.0 (DT-F33f), a változtatás jelölendő |
| `MCGED` | `—` / `glosszak_hu` | 13 | 0 | 13 | 3 867 | © Mounce, csak nem kereskedelmi; kereskedelmi=nem |
| `BDB` | `nyelvi_hatter` / `forditas_hu` | 18 | 0 | 18 | 5 251 | közkincs; **nem ide tartozik**, l. lent |
| `BDB`, `Thayer`, `TBESG`, `LSJ` | szócikk-szint | 25 | 25 | 0 | – | – |
| `SECE_G`, `SECE_H` | `forditas_hu` | 5 | 0 | 5 | – | jelölés nélkül renderel, nem ide tartozik |

**Elavult sor nincs.** Az `ellenoriz.py` 13. szabálya RENDBEN: a lap 63 meglévő találatánál
mindegyik hash egyezik. A 14. szabály (terminológia-verzió) 89/737 sor elmaradását jelzi. Ebből
a lapokon áll: 13 `v1` sor (BDB, Thayer) és 46 üres verziójú, migrált sor (40 UBS DNTG, 4 TBESG,
1 LSJ, 1 Thayer). Ezek újrafordítása nem e feladat dolga.

**A BDB-nyelvi háttér nem kerül fordításra.** A 18 Strong (H0127, H0430, H1121, H2403, H2416,
H3548, H3678, H4467, H5315, H6975, H7043, H7121, H7451, H7585, H7843, H8004, H8034, H8415) teljes
BDB-szócikke már magyarul van a gyorsítótárban (`jelentes_szam=teljes`, az F28 `opus`/`kezi`
soraiként). A nyelvi háttér a szócikk feje, tehát a meglévő fordítás elejének kivágása, nem új
fordítás. A határ illesztése a #107 szakaszhatár-illesztésének (`adat/bdb_szakasz_hu.tsv`) a
dolga, a renderbe kötése generátor-feladat. Kettős fordítás így nincs: ami BDB, azt a #28/#38
fordítja, ez a feladat nem ír `szotar=BDB` sort. Erről N-F121a szól (5. szakasz).

**Séma- és ellenőrzési rés (N-F09a).** A `UBS_DBH`, `MCGED`, `tW_szocikkek` és a `TBESH`
`teljes` a SEMA 2.14 `szotar`-listájában nem szerepel. Az `ellenoriz.py` 13. szabálya ezekre ma
`nincs hozzá forrásszöveg` sértést adna, mert a forrásszöveg-indexe csak a
`lexikon_hivatkozasok.tsv`-t, a `UBS_DNTG_jelentesek.tsv`-t és a Thayer/BDB teljes szócikket
ismeri. Az első gyorsítótár-sor előtt tehát a sémát és a szabályt bővíteni kell (M0). A
`forditas_kapuk.py` CLI-je is csak `--szotar Thayer|BDB`-t fogad el; könyvtárként bármelyik
szótárnevet elfogadja.

## 2a. A négy mankó (a felhasználó kérése, 2026-10-18)

A fordítás minden adagja ezt a négy eszközt használja. Ezek nélkül adag nem indul.

1. **Terminológiai szójegyzék kapuval.** `adat/terminologia.tsv` (SEMA 2.15), a `kapu`
   oszloppal; a `forditas_kapuk.py` 5. kapuja ellenőrzi. Az új sorok `v4` verziót kapnak.
2. **Tiltott fordulatok listája.** Új tábla: `adat/tiltott_fordulatok.tsv` (új SEMA-szakasz:
   `magyar_alak`, `ertelem`, `helyette`, `indoklas`, `verzio`). Olyan magyar alakok, amelyek a
   kimenetben hibának számítanak. Új kapu (`14_tiltott`) méri: találatnál a sor nem rögzül
   automatikusan, hanem kézi ítéletre áll meg (a `…_bukottak.tsv`-be kerül, `tiltott` okkal).
   Első elemek: „melléknéven nevezni”, „melléknevet adni” (ige értelemben; helyette: „más néven
   nevezni”).
3. **Károli-alakok az adatblokkból.** A glosszafordító is megkapja a Strong Károli-fordításait,
   ahogy a BDB-fordító az `eszkozok/bdb_adatblokk.py`-ból: a #22 párosítás
   (`adat/karoli_strong/parok_*.tsv`) Strongonkénti Károli-alakjai gyakorisággal és
   proveniencia-sorral. Ezt a `glossza_forditas.py` saját adatblokk-függvénye állítja elő. A
   `bdb_adatblokk.py` csak olvasott, a módosítása nem e feladat dolga. A Károli-lefedettség az
   M0-ban mérendő a 454 egység Strongjaira (a megbízó szerint ma 100%); 100% alatt a hiányzó
   Strongok a naplóba kerülnek, és ott nincs Károli-alak, nem pótoljuk.
4. **Igehely-idézet Károli-alakban.** Ha a glossza vagy a tW-szöveg igehelyet vagy
   példamondatot idéz, a magyarítás az adott vers Károli-szövegéhez igazodik
   (`konkordancia/Karoli_1908.tsv`; a könyvnév a `Konyv_normalizalo_tabla.tsv` szerint).
   Az adatblokk az idézett versek Károli-szövegét is tartalmazza.

## 2b. Fordítási elvek (a felhasználó kérése, 2026-10-18; mind az öt jóváhagyásra vár)

A G1941/H7121 „nevezni” eset nem egyszeri javítás, hanem az alábbi elvek első alkalmazása
(M0 0. pont). Az elvek a gyorsítótár minden szótárára érvényesek, nem csak e feladat öt
forrására. Helyőrzőjük az 5. szakaszban: DT238–i. Amíg a felhasználó nem hagyja jóvá
őket, az M1 nem indul.

**Jóváhagyva:** a felhasználó 2026-10-19-én mind az öt elvet elfogadta; a DT238–i a `DONTESEK.md`-ben 🟢.

1. **Nyelvközi egységesség (DT238).** Ugyanaz a fogalom a héber és a görög szócikkekben
   (BDB, Thayer/TBESG, tW, UBS DBH/DNTG, Mounce stb.) ugyanazt a magyar szót kapja. A párokat a
   meglévő kapcsolatok adják: a SECE héber↔görög megfelelő-listái (`SECE_G/H_teljes.tsv`), az
   LXX versszintű párok (`LXX_versszintu_parok.tsv`) és a Strong-megfelelések. Ha egy fogalomnak
   valamelyik oldalon már van elfogadott magyar alakja, a másik oldal azt örökli: az adatblokk
   (2a/3) a pár másik oldalának elfogadott alakjait is felsorolja, forrással.
2. **Rangsor eltérő fordításnál (DT239):** (a) a terminológiai szójegyzék `kapu=igen`
   sora; (b) a Károli szóhasználata az adott Strongra (adatblokk); (c) a már elfogadott
   BDB-fordítás; (d) a szótár saját szövege. Ha két szint ellentmond egymásnak, a fordítás nem
   dönt magától: a sor kézi ítéletre áll meg (`…_bukottak.tsv`, `rangsor` ok, a jelöltek
   felsorolásával, szintenként).
3. **A szójegyzék építése folyamat (DT240).** Minden adag előtt gépi lépés fut
   (`glossza_forditas.py szojegyzek`). Kigyűjti a gyorsítótárból, mely angol kulcskifejezések
   kaptak már magyar alakot, és hol van több versengő alak. Kimenet:
   `naplok/F121_GLOSSZA_FORDITAS_szojegyzek_javaslat.tsv` (angol kulcs, magyar alakok
   gyakorisággal, sorhivatkozások, javasolt sor). A `terminologia.tsv`-be csak a felhasználó
   által jóváhagyott sor kerül. A gépi lépés javasol, nem ír.
4. **A tiltott fordulatok listája általános (DT241).** Nem egy szóhoz kötött: tükörfordítások
   és hamis barátok gyűjtőhelye. Új elemet a javítások hoznak. A tétel **értelemhez kötött
   mintát** tartalmaz, nem puszta szót. Mérés (2026-10-18, `adat/forditasok.tsv`): a „melléknév”
   szóalak 93 sorban áll, nyelvtani értelemben (BDB/Thayer „melléknév”, „melléknévvel” stb.),
   és ez helyes. Igei értelemben („melléknéven nevezni/neveznek/nevezzenek”, „melléknevet
   adni”) csak a két G1941 sorban fordul elő, 4 helyen. A kapu tehát csak az igei mintát
   fogja meg (pl. `melléknéven nevez\w*`, `melléknevet ad\w*`). A tábla sémája ennek
   megfelelően: `minta` (regex), `ertelem`, `helyette`, `indoklas`, `forras_javitas`, `verzio`.
5. **Visszamenőleges érvény (DT242).** Az elvek a meglévő kézi és gépi fordításokra is
   vonatkoznak, de **automatikus javítás nincs**. Az M0 felméri, hány sort érint, és
   tételes javaslatot ad (`naplok/F121_GLOSSZA_FORDITAS_visszamenoleges.tsv`: sor-kulcs,
   elv, mai alak, javasolt alak, rangsor-indoklás). A javítást a felhasználó soronként vagy
   csoportonként hagyja jóvá; a jóváhagyott javítás külön tétel (`F121.R<n>`), `allapot`
   változatlan, a `megjegyzes` mezőben a döntés hivatkozása. A felmérés köre: a 89 régi
   terminológia-verziós sor (14. szabály: 20 BDB `opus` v1, 8 BDB `kezi` v1, 2 BDB `kezi`
   üres, 13 Thayer v1, 1 Thayer üres, 4 TBESG, 1 LSJ, 40 UBS DNTG üres) és a 648 BDB `sonnet` v3
   sor az új v4 kapus sorokra, valamint a tiltott minták.
   Ha a felmérés a #38 BDB-sorait is érinti, a javaslat a #38-nak megy, ez a feladat
   `szotar=BDB` sort nem ír (E5).

## 3. Hatókör

**SZŰKÍTÉS (DT387, a felhasználó döntése, 2026-10-28: „#121 szűkítve”).** Ez a menet csak az `lexikon/ISTENTISZT-001_TUDOMANYOS.md` lap `(fordításra vár)` jelölésű egységeit fordítja. A #131 (DT371/DT272) óta a tW, a TBESH, a Mounce és a teljes UBS-szócikk lekerült a lapról, ezért a 454 egységből a lapon **6 egyedi egység** maradt (5 UBS DBH `definicio_hu` — H7121: `006562001001000`, `…009000`, `…011000`; H8034: `007442001001000`, `…004000` — és az UBS DNTG G1941 `001957001003000` `56.15` `glosszak_hu`). A szám körül kétféle mérés van: a laza `grep -c` 23 sort, a `(fordításra vár)` karaktersorozat 46 előfordulást ad (44 DBH-definíció-előfordulás, 1 domén, 1 a lap magyarázó lábjegyzete); egység-szinten 6. A D1 érinti a 6 sort (CC BY-SA forrás); a D2 (Mounce), D3 (TBESH-dedup) és D4 (tW) ezen a lapon tárgytalan, a többi lapra marad. A többi 7 lap és a további szótárak nem feladat; a lista-eszköz és a 13. szabály bővítése viszont általános. Az alábbi eredeti hatókör a későbbi lapokra érvényes tervként marad.

**Eszköznév (DT388, a DT338 (c) szerint):** külön fájl, `eszkozok/glossza_lexikon_forditas.py`; a #140 `glossza_forditas.py`-ja érintetlen.

**Benne van:**
- a 454 hiányzó egység fordítása a fenti négy forrásból (`UBS_DBH`, `UBS_DNTG`, `TBESH`,
  `tW_szocikkek`), az `MCGED` a D2 szerint;
- a fordító- és rögzítőeszköz (`eszkozok/glossza_forditas.py`). A listát a generátor saját
  kulcsaiból állítja elő, a `forditas_ehhez` hívásainak naplózásával, repón kívüli
  renderrel. Így a kulcs és a forrásszöveg pontosan az, amit a lap keres. A SEMA 2.14 „egy
  forrásszöveg-szabály”-ához egyetlen feloldó függvény tartozik, ezt importálja az
  `ellenoriz.py` 13. szabálya is (két külön másolat nem lehet);
- a SEMA 2.14 bővítése: `szotar`-lista, a `forras_hash` forrásszövege szótáranként;
- a 13. szabály forrásszöveg-indexének bővítése (teszttel);
- a `forditas_kapuk.py` CLI-választékának bővítése. A kapuk tW-re és rövid glosszára való
  alkalmasságát az M1 méri; kaput lazítani csak ⛔ után lehet;
- terminológia v4 (`adat/terminologia.tsv`): a glosszák és a tW teológiai kulcsszavai;
- licencjelölés a D1 szerint.

**Nincs benne:**
- `szotar=BDB` bármely sora (a #28/#38-é; a nyelvi háttér N-F121a);
- a generátor (`lexikon_general.py`) módosítása, beleértve a héber 9. szerep versenkénti
  DBH-táblájának glosszáit is: ezek ma `forditas_ehhez` nélkül, angolul renderelnek
  (N-F121b);
- a SECE- és más kiegészítő szótári sorok (jelölés nélkül renderelnek);
- a 14. szabály szerint elmaradt (`v1`, üres verziójú) sorok újrafordítása;
- a 8 motívumon kívüli Strongok (a későbbi motívumoké): a lista-eszköz `--id` nélkül is fut,
  de ez a feladat csak a 8 motívum kulcsait fordítja;
- az éles `lexikon/` újragenerálása (#36). A próbarender csak repón kívüli könyvtárba megy, a
  `generalt_proba/`-ba nem.

## 4. Lépések (⛔ a kötelező megállások)

**Minden futás első lépése a modell-ellenőrzés** (CLAUDE.md): a kért modell `sonnet`.

### M0 — eszközök, séma, terminológia-tervezet

0. **Első tétel (`F121.0`): a „nevezni” szócsalád egységesítése** (a felhasználó döntése,
   2026-10-18). A héber és a görög oldal egységes szóhasználatot kap, a BDB H7121 kézi
   fordításához igazodva („hívni = nevezni”, „nevet adni valaminek”, Niph'al „hívatni,
   neveztetni”; „melléknév” abban nem szerepel).
   - `adat/terminologia.tsv`, `v4`: `call` / `name` (ige, nevet adni értelemben) → „nevezni,
     nevet adni”; `surname` (ige) → „más néven nevezni” (a görög többlet: még egy név);
     passzív `be called` / `be surnamed` → „neveztetni”, illetve „akit …-nak is neveznek”. A
     `call` többjelentésű (hívni, segítségül hívni), ezért `kapu=nem` javasolt; a többi
     `kapu=igen`.
   - `adat/tiltott_fordulatok.tsv`: „melléknéven nevezni”, „melléknevet adni” (ige értelemben).
   - A G1941 két kézi sorának javítása az `adat/forditasok.tsv`-ben (`allapot=kezi` marad, a
     `forras_hash` nem változik, mert a forrás nem változott; a `megjegyzes` mező kapja:
     „F121.0: melléknév → más néven (felhasználói döntés, 2026-10-18); proveniencia: manual”):
     - **Thayer G1941 `teljes`:** „1. nevet tenni valakire, melléknéven nevezni” → „1. nevet
       tenni valakire, más néven is nevezni”; „ὁ ἐπικαλούμενος (ho epikalúmenosz): akit
       melléknéven neveznek” → „akit …-nak is neveznek” alak. A szócikkben van egy harmadik
       előfordulás is: „megengedni, hogy valakit melléknéven nevezzenek: Zsid 11:16”. Ezt a
       szójegyzék szerint kell átírni, a javasolt alakkal a naplóban.
     - **TBESG G1941 `1`:** „hívni, nevezni, melléknevet adni” → „hívni, nevezni, más néven is
       nevezni”.
   - Ez a 2b. szakasz elveinek első alkalmazása (DT238: a görög oldal a H7121 elfogadott
     alakját örökli; DT241: az első tiltott minta).
   - Háttér: a 2026-09-26-i fordítási pilot (`naplok/FORDITAS_P3_kimenet.tsv`) modelljei „nevet
     adni / elnevezni / megnevezni” alakot adtak, a „melléknév” csak a kézi sorban szerepel.
   - Az írás előtt az eszköz a táblát összeveti az eredetivel: csak a megnevezett sorok
     változhatnak. A szöveges diff a naplóba kerül. Ha a felhasználó külön kéri, ez a tétel
     a befogadással együtt egy kis PR-ban is mehet.

1. `eszkozok/glossza_forditas.py lista --id <ID>…`: a 2. szakasz mérésének determinisztikus
   megismétlése. Kimenet: `naplok/F121_GLOSSZA_FORDITAS_lista.tsv` (kulcs, forrásszöveg-hossz,
   `forras_hash`, motívumok, állapot: `megvan` / `hianyzik` / `elavult`). Ha a számok
   eltérnek a 2. szakasztól, a napló okot ad (pl. a #11 merge-e óta változott a token-készlet).
2. A forrásszöveg-feloldó (szótáranként) és a 13. szabály bővítése, teszttel. A teszt
   minden új `szotar`-ra egy helyes és egy elrontott hash-t vizsgál. Az `ellenoriz.py` a
   bővítés után is RENDBEN a mai 737 sorra.
3. SEMA 2.14: a `szotar`-lista (`UBS_DBH`, `MCGED`, `tW_szocikkek`; `TBESH` `teljes`), a
   forrásszöveg szótáranként, és az `allapot` értéke az új sorokra (javaslat: `sonnet`,
   mint az F38-ban, DT-F38e).
4. A `forditas_kapuk.py --szotar` választéka bővül. A kapuk a 62 ISTENTISZT-001 egység
   forrásán szárazon futnak (fordítás helyett a forrás önmagán); a napló rögzíti, melyik kapu
   értelmetlen vagy hamis riasztó rövid glosszán (pl. a 6. hosszarány) és tW-markdownon
   (fejlécek, listák, `rc://` hivatkozások, `(See also: …)`).
5. Terminológia v4 többi sorának tervezete (a 0. pont sorain túl): a 454 egység angol kulcsszavainak gyakorisága. Jelölt sor csak
   az, amelyik egynél több egységben fordul elő vagy motívum-kulcsszó (pl. `spirit`, `soul`,
   `Holy Spirit`, `Yahweh`, `Lord`, `Yahweh of hosts`, `curse`, `sin`, `call on the name`,
   `Sheol`, `hades`, `abyss`). A magyar alak forrása sorrendben: a meglévő v3, a `kezi`
   gyorsítótár-sorok, a 12. (szentlélek) kapu szabálya, a Károli, végül az archivált régi
   tanulmány (`archivum/ISTENTISZT-001/`) magyar prózája. Az archívum csak terminológiai
   forrás. Mondatot 1:1 nem emelünk át belőle a gyorsítótárba (DT28: a forrásból az
   adatrétegbe csak döntéssel, kinyerésként mozog adat; itt nem kinyerés történik).
6. Visszamenőleges felmérés (2b/5): `…_visszamenoleges.tsv`, csak javaslat.
7. Az első szójegyzék-javaslat (2b/3) a teljes gyorsítótárból.
8. **⛔ Megállás:** D1–D4 döntés, a DT238–i elvek, a v4 tervezete és a visszamenőleges
   javaslatok jóváhagyása (ez utóbbi tételesen; ami nincs jóváhagyva, változatlan marad). Commit-pontok:
   `F121.0` (a „nevezni” tétel), `F121.1` (lista), `F121.2` (feloldó + 13. szabály + teszt),
   `F121.3` (SEMA, a tiltott-fordulat tábla szakasza is), `F121.4` (kapuk CLI + `14_tiltott`
   kapu + adatblokk). A v4 többi sora csak a jóváhagyás után kerül be (`F121.5`).

### M1 — minta: ISTENTISZT-001 (62 egység, ≈22 800 karakter)

A minta szándékosan az élő lap. Mind az öt forrástípust tartalmazza: 48 DBH, 2 DNTG, 1 TBESH,
1 Mounce, 10 tW.

1. Fordítás egységenként, a v4 terminológiával. A tW-szöveg markdown-szerkezete
   (fejlécek, felsorolás, `rc://`-hivatkozás, `\n`-jelölés) helyőrzővel védett (az
   `emeles.py helyorzo_bont` mintájára). A hivatkozás célja nem fordítható.
2. Kapuk, egy önújrapróba, utána `naplok/F121_GLOSSZA_FORDITAS_bukottak.tsv` (az F28 E4
   rendje).
3. Rögzítés a `glossza_forditas.py rogzit`-tel. Írás előtt az eszköz a táblát összeveti az
   eredetivel: a meglévő sorok (az `F121.0` utáni állapot) bájtra azonosak maradnak, csak új sor kerülhet be. `modell` = a
   saját környezetből vett tényleges modellnév.
4. Próbarender a repón kívülre. Mérés: az ISTENTISZT-001 lapon a jelölés 65 → 0 (vagy a D2
   szerinti maradék), a 13. szabály RENDBEN.
5. **⛔ Megállás a minta után.** A felhasználó a repón kívüli renderen olvassa el a lapot
   (minőség, terminológia, a tW olvashatósága), és dönt a folytatásról. Commit: `F121.6`.

### M2 — a többi hét motívum, adagonként

Sorrend (javaslat): előbb a rövid egységek mind a hét motívumon (DBH, DNTG, TBESH, és a D2
szerint a Mounce: ≈24 000–28 000 karakter, egy adag), utána a tW-szócikkek motívumonként, a legtöbb jelölést viselő
lappal kezdve: HAMART-001, MENNY-001, ANTROP-001, KIRALY-001, ALVIL-001, HODIT-001,
TEREMT-001. A két motívumon közös egység az elsőnél fordítódik. Adagméret: legfeljebb
≈35 000 forráskarakter, így a tW-re 4–5 adag jut. Minden adag külön commit (`F121.7`, …), és
mindegyik után kapueredmény és próbarender-mérés kerül a naplóba. Minden adag előtt lefut a
szójegyzék-gyűjtő (2b/3). Ha új versengő alakot talál, az adag a jóváhagyásig nem indul.
Egyébként adagonként nincs ⛔, csak „folytasd”-ra várás (az F38 D6 tapasztalata). A
rangsor-ütközés (2b/2) soronként áll meg, nem adagonként.

### Mz — zárás

- A 8 motívum repón kívüli próbarenderje: a `(fordításra vár)` jelölés 0, vagy csak a D2/D4
  szerint kizárt egységeken áll (kulcsonként felsorolva).
- `ellenoriz.py` 13. szabály RENDBEN; a 14. szabály új elmaradást nem mutat.
- `fuggetlen-ellenor` a teljes base..head diffen.
- A #36 → #121 függés a `fuggesek` szerint levezetett (5. szakasz, „Függés és fázis”). Ha a
  #36-ot a felhasználó kézi `fugg`-gal is rögzíteni akarja, az a #36 saját menetéé; ez a
  feladat a #36 fejlécét nem írja.

## 5. Döntésnapló

| Azonosító | Kérdés | Opciók | Javaslat |
|---|---|---|---|
| D1 (DT234) | A CC BY-SA forrásból (tW, UBS DBH, UBS DNTG) készült fordítás licence. A projekt saját rétege „minden jog fenntartva” (DT116), a fordítás viszont a SA-forrás átdolgozása. | 1. a `licencek.tsv` új sora: a `forditasok.tsv` sorainak licence a `szotar` forrásáé, a SA-forrásból készült sor CC BY-SA 4.0, a projekt_adat nem terjed ki rá · 2. a `forditasok.tsv` új `licenc` oszlopa · 3. a SA-forrás nem fordítható | 1. A meglévő 40 UBS DNTG `kezi` sor már ilyen, és séma-változást nem igényel. |
| D2 (DT235) | Mounce (MCGED, 13 egység, 3 867 karakter): nem kereskedelmi, „All Rights Reserved”, a licencsor szerint „a nyilvános nézetből kimarad”. | 1. kimarad, a jelölés a lapon marad · 2. fordítás nem kereskedelmi jelöléssel | 1., amíg a #36 a Mounce-blokk nyilvánosságáról nem dönt. |
| D3 (DT236) | A TBESH `forras_hash`-e mire készüljön? A lap a `tbesh_szoveg_dedup` utáni szöveget mutatja. | 1. a lapon látható (dedup) szövegre, a 13. szabály ugyanazzal a függvénnyel számol · 2. a nyers `TBESH.txt` mezőre | 1. Az fordítódik, amit az olvasó lát. |
| D4 (DT237) | A tW-szócikkek (174 000 karakter, a munka 85%-a) teljes fordítása vagy csak a `Definition` része? | 1. teljes · 2. csak a definíció, a többi angol marad (a jelölés részlegesként marad) | 1. A lap a teljes szöveget mutatja, és részleges jelölés ma nincs a generátorban. |
| DT238 | Nyelvközi egységesség (2b/1) | 1. elfogad · 2. elvet | 1. |
| DT239 | Rangsor: szójegyzék > Károli > elfogadott BDB > a szótár szövege; ütközésnél kézi ítélet (2b/2) | 1. elfogad · 2. más sorrend | 1. |
| DT240 | Szójegyzék-építés minden adag előtt, gépi javaslat, kézi jóváhagyás (2b/3) | 1. elfogad · 2. csak az M0-ban egyszer | 1. |
| DT241 | Általános, értelemhez kötött (regex) tiltott-fordulat tábla (2b/4) | 1. elfogad · 2. szóhoz kötött lista | 1. A puszta „melléknév” 93 helyes nyelvtani sort fogna meg. |
| DT242 | Visszamenőleges érvény: felmérés és tételes javaslat, automatikus javítás nélkül (2b/5) | 1. elfogad · 2. csak előre érvényes | 1. |
| N-F121a | A BDB-nyelvi háttér (18 Strong) magyarja a meglévő teljes fordítás feje. A kivágás a #107 szakaszhatár-illesztésére épül, a renderbe kötés generátor-feladat. | – | külön feladat a #107 után |
| N-F121b | A héber 9. szerep DBH-táblája a glosszát `forditas_ehhez` nélkül, angolul rendereli. A #121 fordításai után ez a tábla is magyarulhatna. | – | generátor-feladat, a #36 előtt vagy vele |

**Költségbecslés.** ≈205 700 forráskarakter. Az F38 mért aránya (2,6 token / forráskarakter,
a session teljes rezsijével, `naplok/BDB_FORDITAS_naplo.md`) szerint ez ≈0,55 millió token
végrehajtói kontextus. A tW-markdown helyőrzői és a kapuk miatt ≈0,6–0,8 millió token
reális; ebből a minta (M1) ≈60 000 token. Az F38 brief durva becslése (120–300 USD ≈4,8 millió
forráskarakterre) arányosan **≈5–15 USD**. A tényleges kreditet a felhasználó olvassa le, a
menet nem becsül pénzösszeget.

**Modell.** `sonnet`, az F38 döntése szerint (DT-F38e): a Sonnet-fordítás közelebb áll a
Károli-stílushoz. A tW teológiai szócikkei értelmező jellegűek, de a feladat fordítás, nem
értelmezés: `munka: adat`. Ha a minta után a felhasználó a tW-hez Opust kér, az az M1 ⛔-nél
dől el.

**Függés és fázis.** `fugg: [11]`: az `ellenoriz.py` és a `SEMA.md` a #11 `ir` listáján is
szerepel, és a minta a #11 utáni ISTENTISZT-001 lapon mér. `nem_fugg: [7, 27, 38]`: a #7 a
teljes Thayert, a #27 a Thayer-FP3-at, a #38 a teljes BDB-t fordítja. E feladat egyikük
kulcsát sem írja, és egyikük kulcsát sem olvassa. `fazis: 2`: a feladat a lexikon kiadását
(#36, szintén 2. fázis) szolgálja. Az 1. fázisú feladatok a DT-F39d szerint így nem kapnak
tőle levezetett függést. 1. fázissal a közös `adat/forditasok.tsv` miatt a #38, #67, #86, #103
és #107 mind a #121-re várna, a futó #38 és #107 is (`feladatok.py fuggesek --extra`,
2026-10-18). 2. fázissal a levezetett kapcsolat: #36 → #121 (ez a kívánt sorrend, ezért a
#36 fejlécéhez nem kell nyúlni), #86 → #121, és #67 ↔ #121 kizárás (a `forditas_kapuk.py`
miatt nem futhatnak egyszerre).

## 6. Elfogadási feltételek

| # | Feltétel |
|---|---|
| E1 | A 8 motívum repón kívüli renderjén a jelölés 0, vagy csak a D2/D4 szerint kizárt kulcsokon áll; a napló kulcsonként felsorolja ezeket. |
| E2 | `ellenoriz.py` 13. szabály RENDBEN; minden új sor `forras_hash`-e a SEMA 2.14 szerinti forrásszövegből újraszámolható. |
| E3 | A meglévő 737 sor bájtra változatlan, a két G1941 kézi sor kivételével (az írás előtti összevetés naplózva). |
| E4 | Minden új sor: `terminologia_verzio=v4`, `modell` = a tényleges modellnév, `allapot` a SEMA szerint. |
| E5 | Egy sor sem `szotar=BDB` (#28/#38). Kivétel nincs; a meglévő sorok közül csak a két G1941 kézi sor (Thayer, TBESG) változik, az `F121.0` szerint. |
| E8 | A `14_tiltott` kapu az új sorokban 0 találatot hagy rögzítve; a G1941 két sorában „melléknév” nem marad. |
| E10 | A DT238–i jóváhagyása előtt nincs M1; a jóvá nem hagyott visszamenőleges javaslat egyetlen sort sem változtat. |
| E11 | Minden adag előtt a szójegyzék-gyűjtő lefutott, a kimenete a naplóban. |
| E9 | Minden adag adatblokkja tartalmazza a Strongok Károli-alakjait és az idézett versek Károli-szövegét, proveniencia-sorral. |
| E6 | Kapuk: minden rögzített sor átment a gátló kapukon; a bukottak a `…_bukottak.tsv`-ben, okkal. |
| E7 | A TSV-írás `split('\t')` / `'\t'.join()`, `csv` modul nélkül (CLAUDE.md). |
