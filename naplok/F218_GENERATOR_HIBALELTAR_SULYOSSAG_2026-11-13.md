# Generátor-hibaleltár súlyosság szerint (2026-11-13)

*Bemenet: `GENERATOR_TERKEP_FUGGELEK_2026-11-13.md` (357 tétel, 13 szelet). Készítette: claude-opus-5-5. A besorolás szabályalapú kivonat + kézi felülírás; a **magas** tételeket egyenként a kódban (main, cf68d0a9) és a két mai lap látható szövegén ellenőriztem (grep, HTML-megjegyzések kivágva). A közepes/alacsony tételek besorolása a cáfoló szövegéből jön, nem saját mérésből.*

## Mércék

- **magas**: a HAMART-001 vagy az ISTENTISZT-001 mai lapján olvasó által látható hibát okoz (vagy egy kapu a lapon némán nem fut), és ezt ellenőriztem.
- **közepes**: a lapot ma nem mérhetően rontja, de a gyökérok egyik osztályába esik (több út, nyers a javított mellett, kódba írt állapotmondat/küszöb, szövegcsere, néma hiány); az új generátornak kezelnie kell.
- **alacsony**: CI-/ellenőrző oldali, holt kód, stabil konstans, kozmetikai vagy latens tétel.
- **lap**: H = HAMART-001, I = ISTENTISZT-001, HI = mindkettő, HI? = a cáfoló nem mérte, kapu = csak ellenőrző kapun át, – = egyiket sem.
- **bizonyíték**: lekérdezés / forrásidézet (fájl:sor) / emlékezet (= nem ellenőrzött). A cáfoló szinte mindenhol fájl:sort idéz; saját lekérdezés ritka.
- **osztály** (gyökérok, gépi kulcsszó-besorolás): 1 csere/regex · 2 több út · 3 nyers a javított mellett · 4 HAMART-ág · 5 kódba írt szöveg/küszöb · 6 néma hiány · 7 egyéb.

## Összesítés

| szelet | magas | közepes | alacsony | össz. |
|---|---|---|---|---|
| kapuk | 2 | 13 | 9 | 24 |
| lg_1 | 3 | 19 | 8 | 30 |
| lg_1300 | 1 | 24 | 4 | 29 |
| lg_2600 | 3 | 20 | 4 | 27 |
| lg_3900 | 3 | 24 | 6 | 33 |
| lg_5200 | 1 | 32 | 5 | 38 |
| lg_6500 | 2 | 21 | 6 | 29 |
| lg_7800 | 1 | 28 | 2 | 31 |
| lg_9000 | 2 | 22 | 2 | 26 |
| seged_A | 0 | 15 | 8 | 23 |
| seged_B | 2 | 20 | 2 | 24 |
| seged_C | 1 | 21 | 3 | 25 |
| szabalyok | 3 | 13 | 2 | 18 |
| **össz.** | **24** | **272** | **61** | **357** |

Osztályok (magas+közepes): 1 csere/regex: 77 · 2 több út: 4 · 3 nyers a javított mellett: 87 · 4 HAMART-ág: 80 · 5 kódba írt szöveg/küszöb: 27 · 6 néma hiány: 6 · 7 egyéb: 15

Bizonyíték: forrásidézet: 287 · lekérdezés: 69 · emlékezet (nem ellenőrzött): 1

## Magas tételek (ellenőrizve)

| tétel | lap | osztály | tárgy | saját ellenőrzés |
|---|---|---|---|---|
| kapuk.4 | HI | 4 HAMART-ág | lexikon_general.py:7367 `strong=` | ell.: az ISTENTISZT-napló 0 `strong=` tokent tart; a kapu csak az új ágon fut (10001) |
| kapuk.22 | H | 1 csere/regex | olvasoi_kapu.py:139 | ell.: `olvasoi_kapu.py:1142` csak „3. LXX” előtagot keres, a HAMART-on „## 5. LXX-fordítói döntések” (2357) |
| lg_1.11 | HI | 4 HAMART-ág | lexikon_general.py:7099 | ell.: 7099 `UJ_LAPSZERKEZET={HAMART-001}`, 68 `uj_szerkezet(` hívás; a 3 F212-kapu csak ezen az ágon (9999–10001) |
| lg_1.14 | H | 4 HAMART-ág | lexikon_general.py:871 | ell.: 871 + 962 `labjegyzetek[-1].replace(...)` szövegre épül, őr nélkül |
| lg_1.30 | I | 1 csere/regex | Pontosítás: a fejlesztői hivatkozások ((G3) 1027,  | ell.: az ISTENTISZT látható szövegében 12 „(G…)/(F…)” fejlesztői hivatkozás |
| lg_1300.19 | HI | 5 kódba írt szöveg/küszöb | lexikon_general.py:1920 | ell.: „magyar rövid glossza-tábla a görögre még nincs” HAMART 2×, ISTENTISZT 3×; a tábla létezik (269 sor) |
| lg_2600.13 | HI | 4 HAMART-ág | lexikon_general.py:7099 `uj_szerkezet(mid)` | ua. (UJ_LAPSZERKEZET, duplikátum) |
| lg_2600.14 | I | 4 HAMART-ág | lexikon_general.py:3885 | ua. (KETRETEGU_BDB_KARTYA, duplikátum) |
| lg_2600.26 | I | 5 kódba írt szöveg/küszöb | lexikon_general.py:3503 | ell.: az ISTENTISZT látható szövegében 73 DT-szám (pl. DT381, DT382) |
| lg_3900.27 | I | 5 kódba írt szöveg/küszöb | lexikon_general.py:4485 | ell.: az ISTENTISZT látható szövegében „#142” |
| lg_3900.28 | I | 4 HAMART-ág | lexikon_general.py:4548 | ell.: 4548 `BDB_BETU_JAVIT={HAMART-001}`: az ISTENTISZT BDB-szövege betűjavítás nélkül |
| lg_3900.30 | HI | 5 kódba írt szöveg/küszöb | lexikon_general.py:4431 `elavult` | ell.: a HAMART-on 5× „…Thayer-fordításból (a lexikon fordítástáblája, sz<n> sorok,; …)” |
| lg_5200.31 | HI | 5 kódba írt szöveg/küszöb | lexikon_general.py:5992 | ell.: a `lap_commit` mezőt a generátor sehol nem olvassa (0 találat); ISTENTISZT átnézése 2026.11.04-i |
| lg_6500.9 | HI | 5 kódba írt szöveg/küszöb | Pontosított állítás: a lexikon_general.py rovid_je | ua. (SECE_LABJEGYZET, duplikátum) |
| lg_6500.16 | HI | 4 HAMART-ág | lexikon_general.py:7099 `, 7102 ` | ua. (UJ_LAPSZERKEZET, duplikátum) |
| lg_7800.31 | HI | 1 csere/regex | `H7451. ra ' ` | ell.: ISTENTISZT látható szövegében „‎_724”, „H7121. q”; HAMART a generalt_proba 2438. sorában |
| lg_9000.10 | HI | 4 HAMART-ág | lexikon_general.py:7099 | ua. (UJ_LAPSZERKEZET, duplikátum) |
| lg_9000.24 | I | 1 csere/regex | lexikon_general.py:9728 | ell.: `run()` régi ága `frissit_meglevo_fajlt(meglevo…)` — a kész lap a bemenet |
| seged_B.2 | HI | 3 nyers a javított mellett | `glossza(jel, cimke, hu)` | ell.: 4283–4284 a `BT.szocikkek` csak `zarojel_javit`-ot kap; az olvasói réteg nem a teljesen javított szöveg |
| seged_B.24 | I | 4 HAMART-ág | Három, egymástól független, egyelemű frozenset({'H | ua. (három HAMART-kapcsoló, duplikátum) |
| seged_C.24 | HI | 4 HAMART-ág | lexikon_general.py:7099 | ua. (UJ_LAPSZERKEZET, duplikátum) |
| szabalyok.8 | HI | 4 HAMART-ág | lexikon_general.py:7099 | ua. (UJ_LAPSZERKEZET, duplikátum) |
| szabalyok.9 | I | 4 HAMART-ág | lexikon_general.py:3885 ` a lexikon_general.py:3885-ön áll, a ` | ua. (KETRETEGU_BDB_KARTYA, duplikátum) |
| szabalyok.11 | H | 4 HAMART-ág | lexikon_general.py:871 | ua. (TEMATIKUS_SAJAT_SZO, duplikátum) |

A 24 magas tétel 10 különböző hiba (a többi ugyanannak a hibának más szeletben megtalált példánya): (1) `UJ_LAPSZERKEZET` két szerkezet és kapuk csak az új ágon; (2) HAMART-only BDB-kapcsolók; (3) `TEMATIKUS_SAJAT_SZO` néma csere; (4) belső azonosító a látható szövegben (DT, #142, (G…), fájlnév, `sz<n>`); (5) hamis SECE-állapotmondat; (6) nyers BDB-fej és héber számláló; (7) jóváhagyás lapállapothoz kötés nélkül; (8) a kész lap mint bemenet; (9) a BDB olvasói réteg csak részben javított szövegből; (10) kapuk, amelyek a mintalapon némán nem futnak.

## Minden tétel szeletenként

### kapuk

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:5501 `KHS._nyers_sorok()` |
| 2 | közepes | kapu | forrásidézet | 3 | olvasoi_kapu.py:1284 |
| 3 | alacsony | kapu | lekérdezés | 1 | szabalyok.py:3538 |
| 4 | magas | HI | forrásidézet | 4 | lexikon_general.py:7367 `strong=` |
| 5 | alacsony | kapu | forrásidézet | 3 | ellenoriz.py:890 `teljes` |
| 6 | alacsony | kapu | forrásidézet | 3 | szabalyok.py:1085 `_e19_bdb_szocikk_sorszamok` |
| 7 | közepes | kapu | lekérdezés | 6 | ellenoriz.py:2162 `ellenoriz.py:main` |
| 8 | közepes | HI? | forrásidézet | 7 | lap_befagyasztas.py:42 |
| 9 | közepes | HI | forrásidézet | 3 | olvasoi_kapu.py:1404 `vh_nem_azonositott()` |
| 10 | közepes | HI? | lekérdezés | 7 | szabalyok.py:2028 `_migralt_lista` |
| 11 | alacsony | kapu | forrásidézet | 3 | olvasoi_kapu.py:128 `ARANY='ISTENTISZT-001'` |
| 12 | közepes | HI? | forrásidézet | 1 | ellenoriz.py:750 `import lexikon_general as LG` |
| 13 | közepes | HI? | emlékezet | 5 | `kovetelmeny_kapu.py HAMART-001 --szigoru` |
| 14 | közepes | HI | forrásidézet | 5 | olvasoi_kapu.py:137 `(?m)^## 1\. Döntési út[ \t]*$` |
| 15 | alacsony | kapu | forrásidézet | 5 | Az állítás lényegében igaz, két pontosítással. (1) |
| 16 | közepes | kapu | lekérdezés | 1 | allitas_adat.py:303 |
| 17 | alacsony | kapu | forrásidézet | 5 | ellenoriz.py:66 |
| 18 | közepes | HI? | lekérdezés | 7 | muhely_allapot.py:44 |
| 19 | közepes | kapu | forrásidézet | 1 | lexikon_general.py:3895 `megj` |
| 20 | alacsony | kapu | lekérdezés | 1 | szabalyok.py:3520 |
| 21 | közepes | HI? | forrásidézet | 7 | szabalyok.py:2078 `fajl` |
| 22 | magas | H | lekérdezés | 1 | olvasoi_kapu.py:139 |
| 23 | alacsony | kapu | forrásidézet | 7 | ellenoriz.py:2038 |
| 24 | alacsony | kapu | lekérdezés | 3 | allitas_adat.py:449 `_MELL_CIM` |

### lg_1

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | H | forrásidézet | 4 | lexikon_general.py:317 |
| 2 | közepes | HI? | forrásidézet | 3 | lekerdez.py:280 |
| 3 | közepes | HI | forrásidézet | 3 | lexikon_general.py:317 |
| 4 | közepes | HI? | forrásidézet | 7 | lekerdez.py:280 |
| 5 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:784 `adat/forditasok.tsv` |
| 6 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:3237 `gerinc_adat()` |
| 7 | alacsony | HI? | forrásidézet | 2 | lexikon_general.py:3240 |
| 8 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:3248 `gerinc_adat()` |
| 9 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:3255 `for r in be(GLOSSZAK_HEBER_HU_FAJL)` |
| 10 | közepes | HI? | lekérdezés | 3 | lexikon_general.py:3251 `gerinc_adat()` |
| 11 | magas | HI | forrásidézet | 4 | lexikon_general.py:7099 |
| 12 | alacsony | HI? | forrásidézet | 3 | lexikon_general.py:3266 |
| 13 | közepes | H | forrásidézet | 4 | lexikon_general.py:1104 |
| 14 | magas | H | forrásidézet | 4 | lexikon_general.py:871 |
| 15 | közepes | H | forrásidézet | 4 | Igaz, pontosítva. A cellaszövegek betűre a kódban  |
| 16 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:153 |
| 17 | alacsony | HI? | forrásidézet | 1 | lexikon_general.py:3284 `BDB_ARAMI_ELSO = 9264` |
| 18 | alacsony | HI? | forrásidézet | 3 | lexikon_general.py:138 `lexica` |
| 19 | közepes | HI | forrásidézet | 3 | lexikon_general.py:1166 |
| 20 | közepes | H | forrásidézet | 4 | lexikon_general.py:677 |
| 21 | közepes | HI? | forrásidézet | 5 | lexikon_general.py:132 |
| 22 | közepes | H | forrásidézet | 1 | lexikon_general.py:686 `if uj_szerkezet(m['id'])` |
| 23 | közepes | H | forrásidézet | 4 | lexikon_general.py:666 |
| 24 | közepes | HI | forrásidézet | 3 | lexikon_general.py:702 |
| 25 | közepes | H | forrásidézet | 4 | lexikon_general.py:612 |
| 26 | alacsony | HI | forrásidézet | 5 | lexikon_general.py:3184 |
| 27 | alacsony | H | forrásidézet | 4 | lexikon_general.py:462 `utolso` |
| 28 | alacsony | HI? | forrásidézet | 4 | lexikon_general.py:807 `eszkozok/lexikon_general.py` |
| 29 | alacsony | HI? | forrásidézet | 1 | lexikon_general.py:220 |
| 30 | magas | I | forrásidézet | 1 | Pontosítás: a fejlesztői hivatkozások ((G3) 1027,  |

### lg_1300

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:1384 |
| 2 | alacsony | HI? | forrásidézet | 3 | lexikon_general.py:1435 `), az 1438 ` |
| 3 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:1416 `_tbesh_txt_sorok()` |
| 4 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:1571 `kell` |
| 5 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:1571 |
| 6 | közepes | HI? | forrásidézet | 3 | Az állítás lényegében igaz, a sorszámok pontosítan |
| 7 | közepes | HI? | lekérdezés | 1 | `\s%s:\s(.*?)\sDerivation:` |
| 8 | alacsony | kapu | forrásidézet | 6 | ellenoriz.py:1013 `forditas_ehhez` |
| 9 | közepes | HI? | lekérdezés | 7 | lexikon_general.py:1841 |
| 10 | közepes | H | lekérdezés | 4 | lexikon_general.py:2206 |
| 11 | közepes | H | forrásidézet | 1 | lexikon_general.py:2424 |
| 12 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:2601 `eszkozok/lexikon_general.py` |
| 13 | közepes | H | forrásidézet | 4 | lexikon_general.py:2577 `_szerep_blokk` |
| 14 | közepes | HI | forrásidézet | 3 | `adat/szotar_szerepek.tsv` |
| 15 | alacsony | HI | forrásidézet | 2 | lexikon_general.py:1411 `--helyi-lexicon` |
| 16 | alacsony | HI? | forrásidézet | 5 | lexikon_general.py:1456 `forras` |
| 17 | közepes | HI? | forrásidézet | 3 | `_dbh_hu` |
| 18 | közepes | HI? | lekérdezés | 3 | lexikon_general.py:1617 |
| 19 | magas | HI | forrásidézet | 5 | lexikon_general.py:1920 |
| 20 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:2093 |
| 21 | közepes | HI? | lekérdezés | 3 | lexikon_general.py:1525 `javitva` |
| 22 | közepes | HI? | forrásidézet | 1 | `_HELY_14_RX` |
| 23 | közepes | HI | forrásidézet | 1 | lexikon_general.py:1969 `kutatói azonosítás függőben` |
| 24 | közepes | HI | lekérdezés | 7 | lexikon_general.py:2326 |
| 25 | közepes | HI | forrásidézet | 3 | lexikon_general.py:1347 |
| 26 | közepes | I | forrásidézet | 2 | lexikon_general.py:2403 |
| 27 | közepes | H | forrásidézet | 4 | `helyek[:4]` |
| 28 | közepes | H | forrásidézet | 1 | lexikon_general.py:2073 |
| 29 | közepes | H | forrásidézet | 4 | lexikon_general.py:2546 |

### lg_2600

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | H | forrásidézet | 1 | lexikon_general.py:1779 |
| 2 | alacsony | H | forrásidézet | 4 | lexikon_general.py:2711 `eszkozok/lexikon_general.py:2711` |
| 3 | közepes | H | forrásidézet | 4 | lexikon_general.py:3065 `konyv_teljes_nev` |
| 4 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:3698 |
| 5 | közepes | HI | forrásidézet | 3 | betolt.py:304 `adat/elofordulasok.tsv` |
| 6 | közepes | HI? | lekérdezés | 3 | lexikon_general.py:3237 |
| 7 | közepes | HI? | forrásidézet | 5 | lexikon_general.py:3251 `eszkozok/lexikon_general.py:3251-3253` |
| 8 | közepes | HI | forrásidézet | 3 | lexikon_general.py:3255 `gerinc_adat` |
| 9 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:3266 `gerinc_adat()` |
| 10 | közepes | HI | forrásidézet | 3 | lexikon_general.py:3124 `aktiv` |
| 11 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:3289 `poz` |
| 12 | közepes | HI | forrásidézet | 3 | lexikon_general.py:3248 `adat/thayer_szakaszok.tsv` |
| 13 | magas | HI | forrásidézet | 4 | lexikon_general.py:7099 `uj_szerkezet(mid)` |
| 14 | magas | I | forrásidézet | 4 | lexikon_general.py:3885 |
| 15 | alacsony | HI? | forrásidézet | 5 | lexikon_general.py:3284 `BDB_ARAMI_ELSO = 9264` |
| 16 | közepes | H | forrásidézet | 4 | lexikon_general.py:2694 |
| 17 | közepes | HI | forrásidézet | 4 | lexikon_general.py:2546 `nyelv` |
| 18 | közepes | H | forrásidézet | 4 | lexikon_general.py:2855 |
| 19 | közepes | H | lekérdezés | 4 | lexikon_general.py:2882 `KAROLI_MIN_HELY = 3` |
| 20 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:2527 `szerep_olvasoi` |
| 21 | közepes | H | forrásidézet | 4 | szerep_karoli.py:142 |
| 22 | alacsony | HI | forrásidézet | 3 | `eszkozok/lexikon_general.py` |
| 23 | alacsony | HI? | forrásidézet | 3 | lexikon_general.py:3132 `_HANYSZOR = {2..5}` |
| 24 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:3819 `eszkozok/lexikon_general.py:3819` |
| 25 | közepes | H | forrásidézet | 4 | Pontosítva: a 3139. sor a GERINC_BEVEZETO (régi sz |
| 26 | magas | I | lekérdezés | 5 | lexikon_general.py:3503 |
| 27 | közepes | HI | forrásidézet | 3 | lexikon_general.py:3354 `_bdb_sor_kezdetek` |

### lg_3900

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:3250 `karoli_vers` |
| 2 | közepes | HI? | lekérdezés | 3 | lexikon_general.py:3247 `r.get('szoveg')` |
| 3 | közepes | HI | forrásidézet | 5 | lexikon_general.py:784 `allapot != 'elavult'` |
| 4 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:4306 `thayer_gerinc_szakaszok` |
| 5 | közepes | HI | forrásidézet | 3 | A lapgenerátorban a BDB-szakaszszöveg a nyers adat |
| 6 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:3266 `bdb_en` |
| 7 | közepes | H | lekérdezés | 4 | lexikon_general.py:4853 `_gerinc_tbesh` |
| 8 | közepes | HI | forrásidézet | 3 | lexikon_general.py:317 |
| 9 | közepes | HI | forrásidézet | 3 | lexikon_general.py:4934 `aktiv` |
| 10 | közepes | HI? | lekérdezés | 3 | lexikon_general.py:4959 `_gerinc_nave` |
| 11 | közepes | HI | forrásidézet | 3 | lexikon_general.py:4937 |
| 12 | közepes | HI? | forrásidézet | 2 | lexikon_general.py:1965 |
| 13 | alacsony | HI | forrásidézet | 1 | lexikon_general.py:3284 `BDB_ARAMI_ELSO = 9264` |
| 14 | közepes | H | forrásidézet | 4 | lexikon_general.py:5162 |
| 15 | közepes | HI | lekérdezés | 4 | Az állítás lényegében igaz. A kód a lexikon_genera |
| 16 | közepes | HI | forrásidézet | 4 | lexikon_general.py:4612 |
| 17 | alacsony | HI? | lekérdezés | 7 | lexikon_general.py:4026 `, ahol ` |
| 18 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:4027 |
| 19 | közepes | HI | lekérdezés | 1 | szotari_glossza.py:80 `lexikon_general.py` |
| 20 | közepes | HI | forrásidézet | 4 | lexikon_general.py:4695 |
| 21 | közepes | HI? | lekérdezés | 1 | lexikon_general.py:3942 `_ALAK_UTAN` |
| 22 | közepes | HI | lekérdezés | 4 | lexikon_general.py:4735 `continue` |
| 23 | alacsony | HI | forrásidézet | 3 | lexikon_general.py:5103 `szamozas_elteres` |
| 24 | alacsony | HI | forrásidézet | 3 | lexikon_general.py:4311 |
| 25 | közepes | HI? | forrásidézet | 6 | lexikon_general.py:5043 |
| 26 | alacsony | HI? | forrásidézet | 5 | Az állítás nagyjából igaz, de csak alacsony kockáz |
| 27 | magas | I | lekérdezés | 5 | lexikon_general.py:4485 |
| 28 | magas | I | forrásidézet | 4 | lexikon_general.py:4548 |
| 29 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:4229 |
| 30 | magas | HI | forrásidézet | 5 | lexikon_general.py:4431 `elavult` |
| 31 | közepes | H | forrásidézet | 1 | lexikon_general.py:4817 |
| 32 | közepes | HI | forrásidézet | 5 | Az állítás lényege igaz, de két ponton pontatlan.  |
| 33 | alacsony | kapu | forrásidézet | 4 | `eszkozok/lexikon_general.py` |

### lg_5200

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | HI? | forrásidézet | 1 | Pontosítás: (1) Az 5160. sor sajat_dontes halmaza  |
| 2 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:5160 |
| 3 | közepes | H | forrásidézet | 4 | lexikon_general.py:5421 `G.tsv_beolvas(VISSZHANG_TSV)` |
| 4 | közepes | H | forrásidézet | 4 | lexikon_general.py:5372 `idx = vh_lxx_index(...)` |
| 5 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:5305 |
| 6 | közepes | HI? | forrásidézet | 3 | lekerdez.py:308 `tsk_index()` |
| 7 | közepes | HI | forrásidézet | 3 | Pontosítva: az eszkozok/lexikon_general.py kh_inde |
| 8 | közepes | HI? | forrásidézet | 3 | ellenoriz.py:704 `_tanulmany_szoveg` |
| 9 | alacsony | HI? | forrásidézet | 5 | `adat/kiadasok.tsv` |
| 10 | közepes | H | lekérdezés | 1 | ellenoriz.py:778 |
| 11 | közepes | HI? | forrásidézet | 7 | lexikon_general.py:6006 |
| 12 | közepes | HI? | forrásidézet | 1 | `claude-…` |
| 13 | közepes | HI? | forrásidézet | 7 | lexikon_general.py:5689 |
| 14 | közepes | HI? | forrásidézet | 3 | Pontosítás. A sor nem az 5939., hanem a kolofon_na |
| 15 | közepes | H | forrásidézet | 4 | lexikon_general.py:6101 |
| 16 | alacsony | – | lekérdezés | 3 | lexikon_general.py:6036 `proza_emlites` |
| 17 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:5208 |
| 18 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:5311 `_lxx_csalad_cella` |
| 19 | közepes | HI | forrásidézet | 4 | lexikon_general.py:5516 |
| 20 | közepes | H | lekérdezés | 1 | lexikon_general.py:5402 |
| 21 | közepes | H | forrásidézet | 1 | lexikon_general.py:5342 `if vh_idx is not None` |
| 22 | közepes | H | forrásidézet | 1 | lexikon_general.py:5537 `int(r['Votes']) >= 15` |
| 23 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:5563 `elfogad` |
| 24 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:5421 `LXX_OS` |
| 25 | közepes | HI | forrásidézet | 5 | lexikon_general.py:6566 |
| 26 | közepes | H | forrásidézet | 4 | lexikon_general.py:5659 `if uj_szerkezet(m['id'])` |
| 27 | közepes | H | lekérdezés | 1 | Rögzített forrás-/licenc-/névtáblák a lapgenerátor |
| 28 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:6083 |
| 29 | alacsony | HI? | lekérdezés | 1 | lexikon_general.py:6163 `if uj` |
| 30 | közepes | HI? | forrásidézet | 5 | lexikon_general.py:5883 |
| 31 | magas | HI | forrásidézet | 5 | lexikon_general.py:5992 |
| 32 | közepes | H | forrásidézet | 4 | `eszkozok/lexikon_general.py` |
| 33 | alacsony | I | lekérdezés | 5 | lexikon_general.py:5982 |
| 34 | közepes | H | forrásidézet | 1 | lexikon_general.py:5678 |
| 35 | alacsony | I | forrásidézet | 4 | Az állítás lényegében igaz, de pontosítandó. A szö |
| 36 | közepes | H | forrásidézet | 4 | lexikon_general.py:6133 |
| 37 | közepes | H | forrásidézet | 4 | lexikon_general.py:666 |
| 38 | közepes | H | forrásidézet | 1 | lexikon_general.py:6120 `kolofon_lektor_uj` |

### lg_6500

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | HI? | forrásidézet | 7 | lexikon_general.py:784 `fordításra vár` |
| 2 | közepes | HI | forrásidézet | 3 | lexikon_general.py:6769 |
| 3 | közepes | HI | forrásidézet | 3 | lexikon_general.py:6779 `_nyers_sorok()` |
| 4 | alacsony | HI | forrásidézet | 3 | lexikon_general.py:6983 `tanulmany` |
| 5 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:7932 `dontes_datum` |
| 6 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:7344 |
| 7 | közepes | H | forrásidézet | 4 | lexikon_general.py:7367 |
| 8 | alacsony | HI? | lekérdezés | 3 | lexikon_general.py:7442 `eszkozok/lexikon_general.py:7442` |
| 9 | magas | HI | forrásidézet | 5 | Pontosított állítás: a lexikon_general.py rovid_je |
| 10 | közepes | HI? | forrásidézet | 5 | lexikon_general.py:6526 |
| 11 | alacsony | kapu | forrásidézet | 1 | lexikon_general.py:7395 `eszkozok/lexikon_general.py:7395–7417` |
| 12 | alacsony | HI | forrásidézet | 5 | lexikon_general.py:6534 |
| 13 | közepes | HI | forrásidézet | 1 | `int(r['Votes']) >= 15` |
| 14 | közepes | H | forrásidézet | 4 | lexikon_general.py:6579 `elif csoportok:` |
| 15 | közepes | HI? | lekérdezés | 5 | `forras_kereses` |
| 16 | magas | HI | forrásidézet | 4 | lexikon_general.py:7099 `, 7102 ` |
| 17 | közepes | H | forrásidézet | 1 | lexikon_general.py:7106 |
| 18 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:6779 `forras=` |
| 19 | alacsony | kapu | lekérdezés | 1 | `regi_szerkezetre` |
| 20 | közepes | H | forrásidézet | 4 | lexikon_general.py:7263 |
| 21 | közepes | I | lekérdezés | 3 | lexikon_general.py:7360 |
| 22 | közepes | HI? | lekérdezés | 1 | lexikon_general.py:7545 ` és ` |
| 23 | közepes | H | forrásidézet | 4 | lexikon_general.py:7638 |
| 24 | közepes | H | forrásidézet | 4 | lexikon_general.py:7721 `[:5]` |
| 25 | közepes | H | forrásidézet | 4 | lexikon_general.py:7474 |
| 26 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:6607 `indoklas` |
| 27 | alacsony | H | forrásidézet | 4 | lexikon_general.py:7768 `megbizhatosag` |
| 28 | közepes | HI | forrásidézet | 1 | lexikon_general.py:5512 |
| 29 | közepes | HI | forrásidézet | 4 | lexikon_general.py:7331 |

### lg_7800

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | H | forrásidézet | 1 | lexikon_general.py:8270 |
| 2 | közepes | H | forrásidézet | 1 | lexikon_general.py:7932 `^\\| (DT\d+) \\|` |
| 3 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:8647 `lemma` |
| 4 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:2206 |
| 5 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:8582 |
| 6 | közepes | HI? | forrásidézet | 6 | lexikon_general.py:8598 |
| 7 | alacsony | HI? | forrásidézet | 3 | lexikon_general.py:8592 |
| 8 | közepes | HI | forrásidézet | 2 | lexikon_general.py:8789 `eszkozok/lexikon_general.py:8789` |
| 9 | közepes | H | lekérdezés | 4 | lexikon_general.py:8436 `lexikon_general.py:8436–8458` |
| 10 | közepes | HI? | forrásidézet | 2 | lexikon_general.py:8769 `utvonal` |
| 11 | közepes | HI | lekérdezés | 3 | lexikon_general.py:8675 `eszkozok/lexikon_general.py:8675` |
| 12 | közepes | H | lekérdezés | 3 | lekerdez.py:280 `idx = tahot_vers_index()` |
| 13 | közepes | HI? | lekérdezés | 1 | lexikon_general.py:8509 |
| 14 | közepes | H | forrásidézet | 1 | `if regi not in szoveg: raise ValueError` |
| 15 | alacsony | HI? | lekérdezés | 1 | lexikon_general.py:7815 `[\w-]*_kereszthivatkozas_naplo\.md` |
| 16 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:8076 |
| 17 | közepes | HI | forrásidézet | 3 | lexikon_general.py:8893 |
| 18 | közepes | HI | forrásidézet | 1 | `int(r['Votes']) >= 15` |
| 19 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:8073 |
| 20 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:8120 `igazolas` |
| 21 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:8271 |
| 22 | közepes | – | forrásidézet | 5 | lexikon_general.py:8469 `< 0.05` |
| 23 | közepes | – | forrásidézet | 1 | lexikon_general.py:8252 |
| 24 | közepes | H | forrásidézet | 1 | Fájl: eszkozok/lexikon_general.py. attekinto_beszu |
| 25 | közepes | HI? | forrásidézet | 7 | `len(jo)` |
| 26 | közepes | HI? | forrásidézet | 5 | lexikon_general.py:8635 |
| 27 | közepes | H | forrásidézet | 4 | lexikon_general.py:8567 |
| 28 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:8901 |
| 29 | közepes | H | forrásidézet | 1 | `uj_szerkezet(m['id'])` |
| 30 | közepes | HI? | lekérdezés | 1 | lexikon_general.py:7952 `) + (` |
| 31 | magas | HI | forrásidézet | 1 | `H7451. ra ' ` |

### lg_9000

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | H | forrásidézet | 1 | lexikon_general.py:9188 `_strong_szarmazas` |
| 2 | közepes | H | forrásidézet | 4 | lexikon_general.py:9361 `ellenorzes` |
| 3 | közepes | HI | forrásidézet | 1 | lexikon_general.py:9591 |
| 4 | közepes | H | lekérdezés | 1 | lexikon_general.py:9213 `alak in a.get('jegyzet','')` |
| 5 | közepes | HI | forrásidézet | 3 | lexikon_general.py:9241 `r['ellenorzes']` |
| 6 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:8592 `bdb_helyi_szocikk(strong)` |
| 7 | alacsony | HI | forrásidézet | 3 | lexikon_general.py:9945 `BEFAGYASZTOTT = LB.befagyasztott_idk()` |
| 8 | közepes | HI? | lekérdezés | 3 | lexikon_general.py:9893 |
| 9 | közepes | H | forrásidézet | 1 | lexikon_general.py:8576 |
| 10 | magas | HI | forrásidézet | 4 | lexikon_general.py:7099 |
| 11 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:9136 `pardes_szint` |
| 12 | közepes | H | forrásidézet | 1 | Igaz, pontosítva: eszkozok/lexikon_general.py 9131 |
| 13 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:9143 |
| 14 | közepes | H | forrásidézet | 4 | Az állítás lényegében igaz, de a sorszámok és a ha |
| 15 | közepes | – | forrásidézet | 4 | lexikon_general.py:9453 |
| 16 | közepes | H | forrásidézet | 4 | lexikon_general.py:8567 |
| 17 | közepes | H | forrásidézet | 4 | lexikon_general.py:9237 `cimke` |
| 18 | közepes | H | forrásidézet | 4 | lexikon_general.py:9231 |
| 19 | közepes | H | forrásidézet | 4 | lexikon_general.py:9150 `x.strip().lower()[:5]` |
| 20 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:9098 `eszkozok/lexikon_general.py` |
| 21 | közepes | H | forrásidézet | 3 | lexikon_general.py:8565 `teljes[f]` |
| 22 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:9312 |
| 23 | alacsony | kapu | forrásidézet | 1 | lexikon_general.py:9097 |
| 24 | magas | I | forrásidézet | 1 | lexikon_general.py:9728 |
| 25 | közepes | HI? | forrásidézet | 3 | olvasoi_kapu.py:529 `s not in van_sora` |
| 26 | közepes | H | forrásidézet | 4 | `run` |

### seged_A

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | HI? | forrásidézet | 7 | general.py:235 `tsv_beolvas` |
| 2 | közepes | HI | lekérdezés | 3 | lekerdez.py:280 |
| 3 | közepes | HI? | lekérdezés | 3 | tsk_kulcs.py:65 |
| 4 | alacsony | HI? | forrásidézet | 3 | Az állítás lényegében igaz, de gyenge kockázat. A  |
| 5 | alacsony | kapu | forrásidézet | 5 | `python eszkozok/kiejtes.py --ellenoriz` |
| 6 | közepes | – | forrásidézet | 6 | lekerdez.py:207 `to_step` |
| 7 | közepes | HI? | forrásidézet | 7 | general.py:170 `G.TS` |
| 8 | közepes | HI? | forrásidézet | 5 | general.py:91 `adat/jeloltek.tsv` |
| 9 | közepes | HI? | lekérdezés | 3 | lexikon_general.py:38 |
| 10 | alacsony | – | forrásidézet | 5 | lexikon_general.py:6244 `NAPLO_ID_TERKEP` |
| 11 | alacsony | HI? | lekérdezés | 5 | general.py:185 |
| 12 | közepes | HI? | forrásidézet | 3 | lekerdez.py:109 `kell` |
| 13 | alacsony | HI | forrásidézet | 5 | general.py:119 `import general as G` |
| 14 | közepes | HI? | forrásidézet | 6 | `eszkozok/ubs_hozzarendeles.py` |
| 15 | alacsony | HI? | forrásidézet | 3 | tsk_kulcs.py:75 `NINCS_PAR_KIVETEL = frozenset()` |
| 16 | közepes | HI? | forrásidézet | 6 | lekerdez.py:147 |
| 17 | közepes | HI? | lekérdezés | 1 | kiejtes.py:100 |
| 18 | alacsony | HI? | forrásidézet | 3 | heber_kiejtes.py:35 `GEPI_JEL = 'gépi'` |
| 19 | közepes | HI? | forrásidézet | 3 | `TK.karoli_index(L.load_tsk())` |
| 20 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:374 |
| 21 | alacsony | HI? | forrásidézet | 7 | ubs_hozzarendeles.py:37 |
| 22 | közepes | HI? | lekérdezés | 3 | lekerdez.py:82 `.get('Kiejtés','')` |
| 23 | közepes | HI | forrásidézet | 3 | lexikon_general.py:5537 `lexikon_general.py:5537` |

### seged_B

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:4548 `except OSError` |
| 2 | magas | HI | lekérdezés | 3 | `glossza(jel, cimke, hu)` |
| 3 | közepes | HI? | forrásidézet | 3 | Pontosítva: (1) a zárt lista a bdb_vj_szabaly.py 2 |
| 4 | közepes | HI? | lekérdezés | 3 | bdb_tagolas.py:75 `eszkozok/bdb_tagolas.py:75` |
| 5 | közepes | – | forrásidézet | 3 | lekerdezesek.py:777 `angol` |
| 6 | közepes | HI? | forrásidézet | 4 | szotari_glossza.py:39 |
| 7 | közepes | HI? | lekérdezés | 3 | Az állítás lényegében igaz. Pontosítás: (1) lxx_os |
| 8 | alacsony | HI? | forrásidézet | 7 | bdb_rovidites.py:35 |
| 9 | közepes | HI? | forrásidézet | 5 | bdb_vj_szabaly.py:29 |
| 10 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:3632 |
| 11 | közepes | HI? | forrásidézet | 3 | bdb_rovidites.py:155 |
| 12 | közepes | HI | forrásidézet | 3 | bdb_rovidites.py:105 |
| 13 | közepes | HI? | lekérdezés | 5 | bdb_rovidites.py:31 |
| 14 | közepes | HI? | forrásidézet | 1 | tablajegyzet.py:207 |
| 15 | közepes | HI? | forrásidézet | 1 | szotari_glossza.py:148 `thayer_csak_alak(hu)` |
| 16 | közepes | HI? | forrásidézet | 5 | tablajegyzet.py:26 |
| 17 | közepes | HI? | lekérdezés | 1 | tablajegyzet.py:47 `teljesség-mérés…` |
| 18 | közepes | H | forrásidézet | 1 | lexikon_general.py:9998 `eszkozok/tablajegyzet.py` |
| 19 | közepes | HI? | lekérdezés | 7 | tablajegyzet.py:349 |
| 20 | közepes | HI? | forrásidézet | 1 | tablajegyzet.py:117 `ige-<könyv>-` |
| 21 | közepes | HI? | forrásidézet | 1 | tablajegyzet.py:165 `alpont == '10'` |
| 22 | alacsony | HI? | forrásidézet | 3 | lxx_os_import.py:34 |
| 23 | közepes | HI? | forrásidézet | 5 | lxx_os_import.py:284 |
| 24 | magas | I | forrásidézet | 4 | Három, egymástól független, egyelemű frozenset({'H |

### seged_C

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | alacsony | HI? | forrásidézet | 3 | szerep_karoli.py:56 |
| 2 | közepes | H | lekérdezés | 4 | szerep_karoli.py:201 `parok()` |
| 3 | alacsony | kapu | forrásidézet | 6 | szerep_karoli.py:50 |
| 4 | közepes | HI? | forrásidézet | 3 | szerep_nave.py:91 `_sorok(ut)` |
| 5 | közepes | HI | lekérdezés | 3 | szerep_nave.py:73 `_lxx_kjv` |
| 6 | alacsony | HI? | lekérdezés | 3 | szerep_kizart.py:276 `s['kapcsolodas']` |
| 7 | közepes | HI | forrásidézet | 3 | lexikon_general.py:9995 `lexikon_general.strong_cim` |
| 8 | közepes | HI? | forrásidézet | 5 | szerep_karoli.py:379 |
| 9 | közepes | H | forrásidézet | 1 | lexikon_general.py:1105 `import szerep_kizart as SZKZ` |
| 10 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:4934 |
| 11 | közepes | HI? | lekérdezés | 5 | szerep_karoli.py:86 |
| 12 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:47 `m['id'] in MINOSITES_STAT` |
| 13 | közepes | HI | forrásidézet | 3 | szerep_karoli.py:395 `SZPA_JOIN` |
| 14 | közepes | HI? | lekérdezés | 1 | szerep_kizart.py:225 |
| 15 | közepes | HI | forrásidézet | 1 | szerep_kizart.py:98 |
| 16 | közepes | HI? | forrásidézet | 4 | szerep_nave.py:158 |
| 17 | közepes | HI? | forrásidézet | 5 | szerep_nave.py:42 |
| 18 | közepes | HI? | lekérdezés | 1 | szerep_kizart.py:345 `import olvasoi_utofeldolg as OU` |
| 19 | közepes | HI? | lekérdezés | 3 | szerep_kizart.py:267 |
| 20 | közepes | H | lekérdezés | 1 | szerep_kizart.py:503 |
| 21 | közepes | HI? | forrásidézet | 3 | lexikon_general.py:6893 `import olvasoi_kovetkeztetes as OK` |
| 22 | közepes | HI? | lekérdezés | 1 | lexikon_general.py:50 `import olvasoi_utofeldolg as OU` |
| 23 | közepes | H | forrásidézet | 1 | lexikon_general.py:5489 `kozepes` |
| 24 | magas | HI | forrásidézet | 4 | lexikon_general.py:7099 |
| 25 | közepes | HI? | forrásidézet | 4 | olvasoi_kovetkeztetes.py:482 `fo_t.lower()=='beteljesedés'` |

### szabalyok

| # | súly | lap | biz. | oszt. | tárgy |
|---|---|---|---|---|---|
| 1 | közepes | HI? | forrásidézet | 1 | lexikon_general.py:5489 `KHS.megerositett_sorok()` |
| 2 | közepes | HI? | lekérdezés | 1 | lexikon_general.py:7367 |
| 3 | közepes | HI? | forrásidézet | 4 | lexikon_general.py:3127 `adat/bdb_szakaszok.tsv` |
| 4 | közepes | HI? | forrásidézet | 3 | `Thayer_teljes.tsv` |
| 5 | alacsony | HI? | forrásidézet | 2 | lexikon_general.py:9945 |
| 6 | közepes | HI? | forrásidézet | 1 | `eszkozok/lexikon_general.py` |
| 7 | közepes | HI? | forrásidézet | 7 | `eszkozok/lexikon_general.py` |
| 8 | magas | HI | lekérdezés | 4 | lexikon_general.py:7099 |
| 9 | magas | I | forrásidézet | 4 | lexikon_general.py:3885 ` a lexikon_general.py:3885-ön áll, a ` |
| 10 | közepes | HI? | forrásidézet | 4 | A lexikon_general.py a visszhang_sorok (8598), vis |
| 11 | magas | H | forrásidézet | 4 | lexikon_general.py:871 |
| 12 | alacsony | HI? | forrásidézet | 7 | lexikon_general.py:9945 |
| 13 | közepes | HI | forrásidézet | 5 | tablajegyzet.py:259 |
| 14 | közepes | H | forrásidézet | 1 | Rögzített szakaszcím- és szövegcsere a lexikon_gen |
| 15 | közepes | H | forrásidézet | 4 | lexikon_general.py:3896 |
| 16 | közepes | HI? | forrásidézet | 4 | olvasoi_kapu.py:125 `pct >= 80` |
| 17 | közepes | H | forrásidézet | 4 | lexikon_general.py:9143 |
| 18 | közepes | HI | forrásidézet | 3 | lexikon_general.py:5792 |

