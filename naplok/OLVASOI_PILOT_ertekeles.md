# OLVASOI_PILOT — értékelő jelentés (F60, v3.2: a régi ág az alap)

*Állapot: **M2, M2b és az M4 értékelő jelentése (8. pont) kész; a független ellenőr 14 eltérését az M4-javítás kezelte (F60.44 és köv.: a CI E5, a K1-regresszió, az újramérés, a licencsor, a teljes angol szöveg, a `--kiadas` kapcsoló); hátra: az ellenőr újrafuttatása, a push és a draft PR.** M3: a felhasználó döntései rögzítve (7. pont); a további észrevételek ide kerülnek. Végrehajtó: `claude-sonnet-5-5`. Ág: `claude/olvasoi-pilot` (a `main` v3.1 brief + a mai ág, `claude/f60-olvasoi-pilot` átvett részei; a mai ág nem folytatódik, v3.2). Kimenet (nem a repóban): `<scratchpad>\f60_egyesitett\{1moz,zsolt22}\karoli_konkordancia_proba.html`.*

Minden mérőszám mellett a mérés proveniencia-sora áll. A szakaszok: **1Móz 1–25** (693 vers; a régi ág eddig az 1Móz 1:1–2:3-at, 34 verset mérte) és **Zsolt 22** (32 vers). A mérést `eszkozok/olvaso_pilot/meres.py` (TSV-út; teljes táblák: `naplok/OLVASOI_PILOT_meres.md`, `naplok/OLVASOI_PILOT_adatfelmeres.md`) és `eszkozok/olvaso_pilot/db_meres.py` (`pardes.db`) végezte; a `db_meres.py` nyers kimenete (`olvaso_pilot_db_meres.json`) a repón kívül maradt, a számok újra előállíthatók (`eszkozok/olvaso_pilot/README.md`).

## 1. Az olvasott adatállapot

- Az adat a `claude/olvasoi-pilot` ág `main`-nel egyesített állapotán áll (F60.26, `0828e4a7`); az első mérés commitja `94f68d91` (15:11Z); az M4-javításban újramértem (`1bceee07`; a szakasz-adatok `ts` ideje 2026-10-12T17:42Z, a `pardes.db`-mérésé 17:44Z). Az újramérés a BDB-bontás számait (az F60.35–F60.38 szeletelő-változás után) és a méreteket (a teljes angol TBESG/Thayer-szöveg, F60.45) változtatta; a többi mérőszám azonos. A mérés után a #27, #80, #88, #89 írhatja a `adat/forditasok.tsv`-t és az `eszkozok/sqlite_epit.py`-t, ezért a mérés újrafuttatható (a brief szerint a pilot az aktuális adatállapotot méri).
- A `main` egyesítése megváltoztatta a Zsolt 22 adatát (F54: `zsolt_felirat_eltolas` sorok a `konkordancia/LXX_OS/psalms-lxx.tsv`-ben). Következmény: a Zsolt 22:1 (felirat) ma kap LXX-szót (11), a korábbi „nincs LXX-szó a versre: 1” mérőszám 0; a sorok KJV-oszlopa Károli-számot hordoz, ezért az `adat.py` ezeket a KJV-kulcs levezetéséből kihagyja (F60.28).
- A `pardes.db` építése: `meta.epites_ts=2026-10-12T08:27:32Z`, `meta.mod=teljes`; a fájl 886 415 360 bájt = 886,4 MB (a jelentés végig MB = 10^6 bájtot használ; a `naplok/SQLITE_EPIT_meres.md` „MB”-ja valójában MiB: 845,4 MiB ugyanez a fájl), a fő munkamásolatban áll (`.gitignore`-ban). A mérés a meglévő adatbázison futott (`mode=ro`), nem építettem újra.

## 2. M2 — a TSV-út mérőszámai: a régi ág mérése 1:1–2:3 és 1–25 hatókörön

`scope=1Móz 1–25 | forras=naplok/OLVASOI_PILOT_meres.md (eszkozok/olvaso_pilot/meres.py, adat.py; adat/karoli_strong/parok_*.tsv, adat/forditasok.tsv, konkordancia/BDB_teljes_unabridged.tsv, TBESG.txt, Thayer_teljes.tsv, TAGNT_kivonat.tsv) | ts=2026-10-12T17:42Z`
`scope=1Móz 1:1–2:3 | forras=eszkozok/olvaso_pilot/meres.py --szakasz "1Móz 1:1-2:3" (a HEAD állapotán újramérve; a számok a TSV-útra) | ts=2026-10-12T17:43Z`
`scope=Zsolt 22 | forras=naplok/OLVASOI_PILOT_meres.md (ugyanaz) | ts=2026-10-12T17:42Z`

| Mérőszám | 1Móz 1:1–2:3 | 1Móz 1–25 | Zsolt 22 |
|---|---:|---:|---:|
| vers | 34 | 693 | 32 |
| Károli-szó (szótoken) | 662 | 12 961 | 407 |
| kötött tartalmas héber szóhoz | 399 (60,3%) | 7 617 (58,8%) | 243 (59,7%) |
| — ebből „magas” bizonyosság | 99,2% a kötöttekből | 98,5% | 0% (mind „alacsony”) |
| csak nyelvtani elemhez kötött / párosítás nélkül | 24,3% / 15,4% | 24,8% / 16,4% | 22,6% / 17,7% |
| héber szó-lap | 98 | 1 075 | 159 |
| magyar BDB-szócikk / csak angol / egyik sincs | 61 (62,2%) / 37 / 0 | 439 (40,8%) / 624 (58,0%) / 12 (1,1%) | 112 (70,4%) / 47 / 0 |
| BDB: legalább 2 jelentésre bomlik | 67 (68,4%) | 537 (50,0%) | 124 (78,0%) |
| BDB: nincs számozott jelentés a szeletelésben | 26 (26,5%) | 510 (47,4%) | 34 (21,4%) |
| görög szó-lap | 202 | 1 230 | 305 |
| görög lap magyar jelentéssel (Thayer / UBS DNTG) | 4 (2,0%) | 8 (0,7%) | 3 (1,0%) |
| Macula-párral rendelkező héber szó, ebből van görög megfelelő | 86,1% | 80,2% | 83,5% |
| UBS-jelentés az előfordulásra (héber) | 86,0% | 90,2% | 91,7% |
| `olvaso_pilot.json` mérete (bájt) | 5 513 526 | 35 701 319 | 7 468 564 |
| HTML mérete, gzip+base64 (bájt) | 2 245 312 | 11 248 603 | 3 097 455 |
| HTML mérete nyersen (bájt) | 5 608 053 | 35 795 837 | (nem épült) |

A BDB-bontás sorai az F60.35–F60.38 szeletelő-változás után mért értékek (az első mérés a változás előtt: 531 / 123 bomló, 34 / 2 egyben maradó szócikk); a méretek a teljes angol TBESG/Thayer-szöveggel (F60.45) mért értékek (az első mérés a vágott szöveggel: 10 204 234 / 2 538 866 bájt). MB = 10^6 bájt.

Megfigyelések, amelyeket a mérés ad (értelmezés nélkül):

- A magyar BDB-szócikkes szó-lapok aránya 62,2%-ról 40,8%-ra esik; az angol eredeti áll helyettük (a lapon állapotjelzéssel, l. 4.). 12 szó-lapnak (H0553, H1746, H3231, H3252, H4138, H4176, H5503, H5668, H5745, H6820, H7742, H8646) sem magyar, sem angol BDB-szócikke nincs; 15 másiknak (6 magyar, 9 angol szócikkel) a saját szócikke helyett a `BDB_strong_alias.tsv` szerinti másik Strong-szám alatti szócikk áll (az alias a lapon jelezve). A 12 lap ellenőrzése (saját lekérdezés, a 8.2 „Fordítások” pont szerint): a 12 Strong-számnak nincs sora a `BDB_teljes_unabridged.tsv`, a `BDB_strong_alias.tsv`, a `BDB_strong_potlas.tsv`, a `BDB_aram_potlas.tsv` és az `adat/forditasok.tsv` BDB-soraiban; négynél (H3231, H4176, H5745, H6820) a `BDB_strong_alias_elvetett.tsv` ad sort (`nem_ebbol_a_szocikkbol`: a testvér-sor más BDB-szócikkből való), a másik nyolcnál semmilyen BDB-tábla sem.
- A „számozott jelentés nélküli” BDB-szócikkek aránya 26,5%-ról (1Móz 1:1–2:3) 47,4%-ra (1Móz 1–25) nő (a példák között tulajdonnevek: pl. H0085 אַבְרָהָם; az ok külön vizsgálatot igényel).
- A Zsolt 22 Károli–Strong párosítása továbbra is 100%-ban „alacsony” (nincs egyezés-ellenőrzés).
- A HTML a nyers változatban 35,8 MB (a 16 MB-os határ fölött), a tömörítettben 11,2 MB: a gzip+base64 beágyazás (F60.27) a határ alatt tartja; tömörítés nélküli változathoz `epit.py --nyers`. A tömörítés régebbi böngészőben (Safari < 16.4) nem működik (`DecompressionStream`).
- A hatókör bővítése a Macula-alak ≠ LXX_OS-alak eltérések számát 33-ról 354-re emelte (302 a χ/ξ felcserélésével magyarázva): a Macula χ/ξ-hibája az 1–25 hatókörön 26 szóalakot érint.

## 3. M2b — a `pardes.db` mérése

Gép: Windows-11-10.0.26300, 8 CPU, Python 3.14.7; `pardes.db` 886,4 MB (886 415 360 bájt). Az időmérés a Windows-fájlgyorsítótárat nem ürítette; a „hideg” = új SQLite-kapcsolaton az első lekérdezés (üres SQLite-gyorsítótár), a „meleg” = a teljes futás második menete ugyanazon a kapcsolaton.

`scope=1Móz 1–25 | forras=pardes.db meta.epites_ts=2026-10-12T08:27:32Z meta.mod=teljes hash(tábla=sha12)=vers=120ad7544c1f; token_par=d1b0a20b21ea; token_eredeti=6a015e467965; token_strong=15f82e2751e3; tsk=f52ca5dd9594; kh=95e3bca57713; vers_szamozas=23e40f6e7d3e; strong_szotar=bb4529cabf93; bdb=b03d01e3cec3; forditasok=0dec518d8198; thayer=30c9e70e4f70; tbesg=a8676a180b1b; lxx_bridge=c2395bb7bc42; lxx_versszintu_parok=d02bcff50a31; ubs_dbh_referenciak=fcf6ea52341c; ubs_dbh_jelentesek=86d4d0f6b636; grammatikai_strongok=5707058f65fb; licencek=8c0f11b06ba4; bsb=c8e376a4a559; kjv=57b7d1044fd9; tipnr=09bc3fc2a803; nave_basokant=62e5001364e4; igehely_tartomany=e23668936ded; lxx_dontesek=1978159f0a63; kapcsolatok=33aa058ff673; motivumok=6b7ec84b16cc; morf_kulcs_heber=b5e37d0f7bb3; sdbh_domenek=7820f7cc9006; sdgnt_domenek=67edd94815da; sece_h=6de1a0614762; sece_g=e98f40533706; tbesh=c36c5e5e6057; lsj=4ed5a849db08; mcged=5af29f685a42; ubs_dntg_jelentesek=335d4fb7b3a6; ubs_dntg_referenciak=a34483703b73; tw_szocikkek=26ff279266dc; oshl_lexikalis_index=88c18fcc8187; oshl_bdb_igehelyek=7183aa23ee59 | ts=2026-10-12T17:44Z`
`scope=Zsolt 22 | forras=(ugyanaz a meta és hash) | ts=2026-10-12T17:44Z`

A régi ág blokkjai bővebbek, mint a mai ágé, ezért a D1 a régi ág 39 blokkját sorolja (a mai ág 23-at).

### D1 — blokk-lefedettség

- **1Móz 1–25: 39 blokkból 35 állítható elő csak a `pardes.db`-ből**; Zsolt 22: 34 / 39.
- 3 blokk TSV-t igényel mindkét szakaszon: igealak-kód és szófaj (Macula), héber–görög párosítás szavanként (Macula), görög szóalak és az LXX-vers szavai (LXX_OS): az építő ezeket szándékosan nem tölti be.
- „Részben”: a **Nave-témák** (a `nave_basokant` nem igehely-kulcsú, a versekre bontáshoz az `igehely_tartomany` 124 sora az 1Móz 1–25-re, 0 a Zsolt 22-re kell; a bontás ma az `adat.py` gépi feldolgozása); Zsolt 22-n az **LXX-döntés / kapcsolat** sorok (0 sor, mert nincs rájuk adat).
- A D1 táblánkénti sorszámai (`D1.blokkok[].sorok_a_szakaszra`) a `olvaso_pilot_db_meres.json`-ban.

### D2 — egyezés a TSV-úttal

Minden vers (693 / 32), minden héber szó-lap (1 075 / 159) és görög szó-lap (1 230 / 305) összevetve blokkonként (Károli-szöveg, Károli–Strong párosítás szavanként, TAHOT-szavak, UBS-azonosítók, TSK darab és top-6, Károli-kereszthivatkozás darab, versszámozás; Strong-szótár, BDB angol és magyar szöveg, előfordulás, Károli-alakok, lxx_bridge, TBESG, Thayer, magyar szócikk, héber háttér). **A „0 eltérés” csak ezekre a blokkokra igaz:** a Károli-szövegben, a párosításban, a héber szavakban, a versszámozásban, a TSK- és UBS-adatban, a Strong-szótárban, az előfordulásban (héber), a Károli-alakokban, az lxx_bridge-ben, a TBESG- és Thayer-szövegben (F60.45 óta a JSON a teljes szöveget hordozza, a mérés a teljes szövegeket veti össze; a korábbi, vágott JSON-t a hasonlító előtag-egyezéssel kezelte), a magyar szócikk-számban és a héber háttérben. **Négy blokkban van eltérés, ezekre a „0 eltérés” nem igaz:**

| blokk | 1Móz 1–25 / Zsolt 22 | ok |
|---|---:|---|
| BDB angol szócikk (héber lap) | 9 / 1 | a szócikk a `BDB_strong_alias.tsv` (#57) szerint másik Strong-szám alatt áll; a `pardes.db` az alias-táblát nem hordozza |
| BDB magyar szócikk (héber lap) | 6 / 1 | ugyanaz |
| ÚSZ-előfordulás (görög lap) | 117 / 52 | a TAGNT-kivonat az építés óta módosult (F90.4: +350 sor; D5): TSV 611 396 sor, adatbázis 611 046 |
| LXX-versszám (vers-lap) | 356 / 28 | az `lxx_versszintu_parok` csak a héber–görög Strong-párral rendelkező versekre ad sort |

### D3 — lekérdezési idő (ez a lekérdezés-készlet; nem optimalizált)

| lap | meleg medián | meleg p95 | hideg medián | hideg p95 |
|---|---:|---:|---:|---:|
| vers-lap, 1Móz 1–25 (693; hideg: 40) | 93,4 ms | 161,2 ms | 87,9 ms | 166,9 ms |
| vers-lap, Zsolt 22 (32) | 51,1 ms | 78,1 ms | 52,4 ms | 85,9 ms |
| héber szó-lap, 1Móz 1–25 (1 075) | 3,9 ms | 12,8 ms | 4,9 ms | 19,1 ms |
| héber szó-lap, Zsolt 22 (159) | 5,4 ms | 29,6 ms | 6,2 ms | 34,0 ms |
| görög szó-lap, 1Móz 1–25 (1 230) | 3,4 ms | 5,3 ms | 4,3 ms | 5,1 ms |
| görög szó-lap, Zsolt 22 (305) | 3,6 ms | 7,9 ms | 4,5 ms | 7,5 ms |

A D3 a régi ág szó-lapjának részhalmazát méri (a `db_meres.py` lekérdezései a mai ág blokkjaira írtak; az újabb blokkok — SDBH, SECE, TBESH, tW stb. — lekérdezési ideje nincs benne). A hideg és a meleg érték alig tér el (az OS-gyorsítótár mindkét esetben meleg volt).

### D4 — a lapokhoz szükséges részhalmaz mérete

Forrás: `naplok/SQLITE_EPIT_meres.md` táblánkénti mérete (indexszel); a régi ág lapjai 40 táblát használnak (a mai ágé 19-et). **Egység: MB = 10^6 bájt.** A forrás-táblázat „MB”-ja MiB (lapszám × lapméret / 2^20), ezért a `db_meres.py` ×1,048576-tal átszámolja; az első mérés a két egységet keverte (843,8 „MB” a táblák összegére, 886,4 MB a fájlra).

- szükséges részhalmaz: **548,4 MB** a táblák 884,8 MB-os összegéből (62,0%); a `licenc_*` oszlopok nélkül 424,5 MB; a teljes fájl 886,4 MB;
- a lapokhoz nem kell: `token_karoli` 147,2 MB, `frazis_pozicio` 120,6 MB, `strong_parok` 58,0 MB, `karoli_variancia` 8,8 MB;
- ha a Macula és az LXX_OS is az adatbázisba kerülne (ma TSV): +207,6 MB TSV-méret;
- a teljes fájl gzip-aránya 0,215 (mérve, 11,9 s); a szükséges részhalmaz becsült tömörített mérete ≈ 117,8 MB (arányos becslés, nem külön mérés).

Viszonyítás az `ADATVAGYON_TERV.md`-hez: a 3. szakasz Netlify-function-határa (~50 MB tömörítve, ~250 MB kicsomagolva) mellett a szükséges rész **a határ fölött** van (548 MB kicsomagolva, ≈ 118 MB tömörítve); a 7. szakasz „50–150 MB indexekkel” becslése alatt marad a teljes adatbázis kb. hatszorosa.

### D5 — frissesség

A `meta` táblánkénti sorszáma és hash-e mind a 39 vizsgált táblára **egyezik a tábla jelenlegi tartalmával** (a hash újraszámítva az építő függvénye szerint). A forrás-TSV-k az építés (2026-10-12T08:27:32Z) után módosultak: `token_eredeti`, `token_strong` (`konkordancia/TAGNT_kivonat.tsv`, F90.7, sorszám +350), `token_par` (`adat/karoli_strong/`, utolsó commit 2026-10-12T10:58:16Z). A `token_par` eltérése a két mért szakaszra nem hatott (0 eltérés).

## 4. M1 — a v3.1 angol-pótlás szabályának ellenőrzése (K2) és a „csak adat” szabály

Az angol-pótlás a régi sablonban megvolt a héber szó-lapon (a BDB-blokk „Magyar fordítás nincs · az angol eredeti áll” állapotjelzéssel, forrássorral és a teljes angol szócikkel; az apparátusokra bontás is az angol szövegből). Két hiányt pótoltam (F60.29): (a) a görög lapon a magyar jelentés hiányában a „Jelentés” blokk állapotjelzése kimondja, hogy az angol eredeti áll (TBESG / Thayer), és a Thayer-szócikk megnyitva jelenik meg; (b) ha sem magyar, sem angol BDB-szócikk nincs (12 lap), az állapotjelzés ezt mondja ki (korábban „az angol eredeti áll” állt, üres szöveggel). A független ellenőr 6. eltérése nyomán (F60.45–F60.45) a görög lapon a TBESG- és a Thayer-szöveg **vágás nélkül**, gördíthető blokkban áll (a prototípus 900, illetve 700 karakterre vágta „…”-tal: 38, illetve 64 lap érintett az 1Móz 1:1–2:3 szakaszon). A TBESH forrás-sorából a rögzített licenc-mondat („a licenc-kérdés nyitott”) kikerült: a licenc-jelzés az `adat/licencek.tsv`-ből jön, mint a többi forrásnál (TBESH: `tisztazott`, CC BY 4.0, DT-F33f).

A mai ág „kivett szövegek” listájának (9 tétel) összevetése a régi sablonnal:

| mai ág tétele | a régi ágon | kezelés |
|---|---|---|
| „TAHOT nem teljes (Zsolt 88/89/140/142 hiányzik)” | megvolt (lábjegyzet), a forrássor is „(nem teljes)” | **kivettem** (F60.29); elavult, hibás (F85 óta fejezet-szinten teljes) |
| „Macula-illesztés kb. 78%” | megvolt | **kivettem** (átvett szám hivatkozás nélkül) |
| „SDBH/DBH a szókincs kb. 90%-át fedi; az üres eredmény nem negatív lelet” | megvolt kétszer (UBS-jelentés, domén) | **kivettem** (a CLAUDE.md tudása, nem adat) |
| „a jelkulcs nincs a repóban” | megvolt (a BDB-jel `title`-jában) | **kivettem** |
| „Gépi szeletelés (próba) … hibás határ előfordulhat” | megvan a BDB-blokkban | **marad** — a felhasználó döntése az M3-ban (2026-10-12, 7. pont); a jellegcímke is gépi feldolgozást mond |
| „Thayer teljes fordítása halasztva (#7)”, „#38 sorrend”, „folyamatban” | nincs a régi sablonban | — |
| „a Károli–Strong párosítás az ÚSZ-re még nem készült el”; „(1–5Móz, Józs)” | nincs | — |
| a sosem hívott szókártya-kód | a régi ágon a szókártya hívott és működik | **marad** (nem hibás) |

## 5. Eltérések a brieftől

1. A `db_meres.py` D2-je a régi ág JSON-szerkezetéhez igazodik: a versszámozás `forras` mezője a JSON-ban nincs (osztály, KJV, MT hasonlítandó); a TBESG/Thayer a JSON-ban F60.45 óta teljes (a hasonlító a vágott JSON-t is kezeli).
2. A mai ág tesztjeiből a K5 (vers-lap és szó-lap D2-egyezés, „nem mérhető” ág) átvéve; a régi ág tesztjei (73) változatlanok, egy elavult elvárás módosult (Zsolt 22:1 ma kap LXX-szót). A tesztek összesen 100 (az M4-javítás után: a prototípus-regresszió, az 1Móz 1–25, a teljes angol szöveg és a `--kiadas` tesztjei), kihagyás nélkül (a D2-tesztek a meglévő `pardes.db`-n futnak; adatbázis nélkül kihagyódnának).
3. **Egyeztetendő eltérés (K1).** A brief K1-e az 1Móz 1:1–2:3 kimenetet a prototípussal „bájtra azonosnak, a `ts` kivételével” írja elő. Ez a bővítés (v2) és a v3.1 szabály mellett nem tartható (a prototípus a TBESG/Thayer-szöveget vágta, a morfológiai feloldás üres volt, a BDB-szeletelő a prototípus óta többször változott), ezért a regresszió (`teszt_olvaso_pilot.py`, `TestRegresszioProto`) **értékazonosságot** ellenőriz: a prototípus (`ce4ef98f`) minden kulcsának értéke megegyezik az 1Móz 1:1–2:3 szakaszon, a `ts=` időbélyeg és az alábbi, darabszámmal rögzített **engedélyezett-eltérés lista** kivételével. A teszt maga állítja elő a prototípus-kimenetet: a `ce4ef98f` `adat.py`-ját és `bdb_szelet.py`-ját (az egyetlen modul, amelyet a prototípus importál) együtt írja repón kívüli ideiglenes könyvtárba, és onnan futtatja, tehát a prototípus saját szeletelőjével (nem a HEAD-ével); a repóba semmi nem kerül; nem kihagyható. A brief szövegét nem írtam át. (Az első változat a prototípus `adat.py`-ját a HEAD `bdb_szelet.py`-jával futtatta, ezért a szeletelő változásai láthatatlanok voltak; a független ellenőr 2. köre jelezte, a lista újramérve.) Az engedélyezett eltérések:

| minta | darab | indok |
|---|---:|---|
| `versek[].heber[].macula.morf_hu` | 746 | a prototípusban üres volt; a v2 az `adat/morf_kulcs_heber.tsv`-ből magyarul feloldja (F60.5, gépi feldolgozás) |
| `gor_lapok.*.tbesg` | 38 | a prototípus 900 karakterre vágta „…”-tal; a teljes angol szöveg áll a lapon (v3.1, F60.45); a prototípus-érték a teljes szöveg előtagja |
| `gor_lapok.*.thayer` | 64 | ugyanez, 700 karakterre vágva |
| `lapok.*.appar` (40 szó-lap) | 40 | a BDB-szeletelő változásai a prototípus óta (F60.17, F60.18, F60.21, F60.23, F60.25, F60.35): jelentés-határok, jelentés-sorszámok és személyszám-jelölők kezelése, fejléc, irodalom-/kritika-sorok; a prototípus-kulcsok értéke ezeken a lapokon eltér. A 40 lap: H0215, H0559, H0914, H1254, H1288, H1876, H1961, H2009, H2232, H2416, H2822, H2895, H3117, H3318, H3533, H3605, H3615, H3651, H3915, H4390, H4723, H4725, H4910, H5414, H5774, H6213, H6440, H6509, H6635, H6942, H6960, H7121, H7200, H7235, H7287, H7363, H7430, H7637, H8147, H8317; a többi 58 szó-lap `appar`-ja a prototípus-kulcsokon azonos |
| `lapok.{H1254, H2416, H3651, H4723, H6960, H7235, H7287, H7363}.appar` | 8 szó-lap (a fenti 40-nel átfedve) | a `szeletel(szoveg, lemma)` második argumentuma (F60.17, `8b642341`): a homonima-szerepet jelöli (`azonos_lemma` / `masik_lemma` / `elo`); külön teszt igazolja, hogy a lemma-argumentum pontosan ennél a 8 lapnál módosítja a kimenetet |
| `prov.elofordulas` | 1 | a „(nem teljes)” megjegyzés kivéve (F60.29: a TAHOT fejezet-szinten teljes, F85) |

   A `prov` többi mezője csak a `ts=` időben tér el. Az 1Móz 1–25-re külön teszt (`TestTeljes1Moz1_25`, ~30 s): 693 vers, az `adat.py` hibátlanul lefut, a kimenet első 34 verse és a közös szó-lapok egyeznek az 1Móz 1:1–2:3 futásával.

## 6. Mért hiányok és nyitott kérdések

- A `konkordancia/tW_szocikkek.tsv` egy cikkében (az `OBS` „Examples from the Bible stories” rész, „God said, “I promise I will never again curse the ground …”) egy U+FFFD karakter áll (forrásadat-hiba; az oldal a szöveget változtatás nélkül mutatja). Nem javítottam (adatjavítás, nem a pilot dolga).
- A Zsolt 22 KJV-számozása: az LXX_OS `zsolt_felirat_eltolas` sorainak KJV-oszlopa Károli-számot hordoz (671 sor a `psalms-lxx.tsv`-ben); a `Karoli_versmegfeleltetes.tsv` és az LXX_OS KJV-oszlopa a Zsolt 22 31 versében ellentmond (a pilot jelzi, nem javítja). A DT-F60b ezzel összefügg.
- A `pardes.db` a TAGNT és a Károli–Strong párosítás későbbi módosításaitól elmaradt (D5); az adatbázis újraépítése nem része a feladatnak.
- A `pardes.db` nem hordozza a BDB-alias táblát és a Nave-témák versekre bontását (D1/D2); az LXX-versszám a vers-laphoz az LXX_OS-ből kell.
- A 12 BDB-szócikk nélküli szó-lap (2. pont) és a 47–624 csak angol szócikkes lap a #38 / #80 dolga.

## 7. M3 — felhasználói átnézés

*Nyitva. A két oldal (a felhasználó nyitja meg; a HTML gzip+base64 beágyazású, `DecompressionStream`-et támogató böngésző kell; a böngészőben az 1Móz 1–25 oldal betöltése hibátlan, 0 konzolhiba; az M4-javítás előtti változaton mérve; az újragenerált oldalak HTML-szövegében 0 U+FFFD, a beágyazott JSON-ban 1, a `tW_szocikkek.tsv` ismert forrásadat-hibája, 6. pont):*
- `C:\Users\bases\AppData\Local\Temp\claude\C--Users-bases-Desktop-Bible-Study\203cb7c8-e0ff-4860-a8e8-943bca62f11f\scratchpad\f60_egyesitett\1moz\karoli_konkordancia_proba.html` (11 247 353 bájt; az M4-javításban újragenerálva, `adat.py --kiadas belso`)
- `C:\Users\bases\AppData\Local\Temp\claude\C--Users-bases-Desktop-Bible-Study\203cb7c8-e0ff-4860-a8e8-943bca62f11f\scratchpad\f60_egyesitett\zsolt22\karoli_konkordancia_proba.html` (3 096 205 bájt; ugyanígy újragenerálva)

*A felhasználó észrevételei (mi hiányzik, mi felesleges, melyik mérőszám a döntő; a „Gépi szeletelés (próba)” szöveg sorsa; a H7121-szeletelő 19 jelentés-szerkezet-változása): ide kerülnek.*

Az M3 eddigi döntései (a felhasználó a chatben, 2026-10-12):
- **„Gépi szeletelés (próba)” felirat: marad** a BDB-blokkban. A 4. pont kivétele ezzel lezárva.
- A H7121-szeletelő 19 jelentés-szerkezet-változásának átnézése elkészült (2026-10-12): a 19-ből 11 javult, 5 romlott (a végleges bontás a régi), 3 mindkettő hibás (ebből 2 javítva, a H0834 ismert hiba); 85 teszt zöld, a két HTML újragenerálva (1Móz 1–25: 10 209 602 bájt; Zsolt 22: 2 544 178 bájt). Részletek: `naplok/OLVASOI_PILOT_szeletelo_atnezes.md`.
- **DT-F60a eldöntve (pontosítva, F60.39–F60.40):** a belső pilotban minden blokk marad, a „?” súgó jelzi a licenc-állapotot. A KJV Strong-címkeréteg GPL (CrossWire kjv.conf: „DistributionLicense=GPL”), ezért a KJV-Strong blokk minden nyilvános kiadásból kimarad; a BSB (CC0) szavankénti angol blokkja marad. Az MCGED ingyenes, nem bevételt hozó nyilvános kiadásban marad (kötelező megjelöléssel), kereskedelmi kiadásból kimarad, vagy írásos engedély kell (a kapcsoló a DT-M6-hoz kötött). A következmény a repó egészére: **DT-F60c** (a `konkordancia/KJV_Strongs_teljes.tsv` GPL-forrás a nyilvános repóban; 🟡 nyitva).
- **DT-F60b eldöntve (1., F60.34):** új feladat a feliratos zsoltárok Károli–KJV számozására; brief-tervezet: `beerkezo/ZSOLT_FELIRAT_SZAMOZAS_brief.md` (befogadás: `/befogad`). A pilot kerülőútja (az LXX_OS KJV-oszlopa, a 31 ellentmondó vers jelzése) addig marad.
- **A BDB-szeletelő átnézése (F60.35–F60.38):** 19 szócikk: 11 javult, 5 romlott (a végleges bontás a régi), 3 mindkettő hibás (a H0834 ismert hiba marad); a teljes magyar BDB-táblán a régi → végleges összevetés 147 szócikknél változtat jelentés-szerkezetet (jelek + szövegkezdet), a személyszám-jelölők száma a jelentés-sorszámok között 177 → 3. Ismert hibák: H0834, H3318, H1157, H2009, és a homonima-törzsek (H2490, H2790, H3384, H6299, H6743, H6965). Részletek, proveniencia: `naplok/OLVASOI_PILOT_szeletelo_atnezes.md` 2–5. pont (`scope=adat/forditasok.tsv BDB (678 magyar sor) | forras=bdb_szelet.py 18a927f6^, 18a927f6, 31e51419 | ts=2026-10-12T18:09`).
- Nyitva: további felhasználói észrevételek (mi hiányzik, mi felesleges, melyik mérőszám a döntő); ezek ide, a 7. pontba kerülnek.

## 8. M4 — mit tud a repó adata, és mi kell a #25a-hoz

*A brief v3.3 szerint: a DT-M1 2026-10-06-án eldőlt (1. opció: a #25 kettéválik, #25a = FELADATOK #76 OLVASOI_KONKORDANCIA, #25b = motívumos nézet), ezért ez a pont nem opciókat vet össze, hanem a mért adatállapot mellett azt mutatja meg, mi kell a #25a briefjéhez. A „javaslat” jelölésű tételek javaslatok, nem döntések. A számok a 2–3. pont méréséből jönnek (a proveniencia-sorok ott állnak); ahol más forrás kell, a tétel saját sora jelzi.*

### 8.1 Mit tud a repó adata az olvasói konkordanciához (motívumréteg nélkül)

`scope=1Móz 1–25 és Zsolt 22 | forras=a 2. és 3. pont (meres.py, db_meres.py; hivatkozott táblák ott) | ts=2026-10-12T17:44Z`

**Erősségek (mért):**
- A Károli-szöveg, a TAHOT-szavak, az UBS-azonosítók, a TSK-adat, a versszámozás és az lxx_bridge a TSV-úton és a `pardes.db`-ben **0 eltéréssel** egyezik (D2, 693 + 32 vers, 1 075 + 159 héber és 1 230 + 305 görög szó-lap); a négy eltérő blokk (BDB angol szócikk, BDB magyar szócikk, ÚSZ-előfordulás, LXX-versszám) a 3. pont D2 táblájában áll.
- Az 1Móz 1–25-ben a Károli-szavak 58,8%-a kötött tartalmas héber szóhoz, ebből 98,5% „magas” bizonyosságú; az előfordulások 90,2%-ához van UBS-jelentés; a Macula-párral rendelkező héber szavak 80,2%-ához van görög megfelelő.
- A lapok blokkjainak 35/39-e (1Móz 1–25), illetve 34/39-e (Zsolt 22) csak a `pardes.db`-ből előállítható (D1); a lekérdezés vers-lapra 93 ms (meleg medián, p95 161 ms), szó-lapra 3,4–5,4 ms (D3).

**Hiányok (mért):**
- Magyar BDB-szócikke a héber szó-lapok 40,8%-ának (439/1 075) van az 1Móz 1–25-ben, 70,4%-ának (112/159) a Zsolt 22-ben; a többinél az angol eredeti áll (624, illetve 47 lap), 12 lapnak (1Móz 1–25) egyik sincs.
- A görög szó-lapok magyar jelentéssel: 0,7% (8/1 230), illetve 1,0% (3/305); a többinél az angol TBESG/Thayer áll.
- A Zsolt 22 Károli–Strong párosítása 100%-ban „alacsony” bizonyosságú (nincs egyezés-ellenőrzés).
- A Károli-szavak 24,8% (Zsolt 22: 22,6%) csak nyelvtani elemhez kötött, 16,4% (17,7%) párosítás nélkül: a szavak kb. 41%-a nem kattintható szó-lapra.
- A BDB-szeletelés (gépi feldolgozás): a héber szó-lapok 47,4%-ánál (510/1 075) nincs számozott jelentés a szeletelésben (1Móz 1–25; a H0085 típusú tulajdonnevek is; az ok külön vizsgálatot igényel). A szeletelő ismert hibái: H0834 (az 1. jelentés eleje), H3318, H1157, H2009 és a homonima-törzsek (H2490, H2790, H3384, H6299, H6743, H6965); a felirat („Gépi szeletelés (próba)”) ezért marad (3. pont, M3).
- A Macula χ/ξ-hibája az 1–25 hatókörön 26 szóalakot érint; a `tW_szocikkek.tsv` egy cikkében U+FFFD áll (forrásadat-hiba, nem javítottam).

### 8.2 A #25a feltételei, egyenként, a mért adat szerint

**Licenc.**
`scope=a pilot adatforrásai | forras=adat/licencek.tsv; DONTESEK.md DT-F60a, DT-F60c, DT-M6, DT116; FELADATOK #89 | ts=2026-10-12`
- Eldöntött: **DT-F60a**: a KJV-Strong blokk minden nyilvános kiadásból kimarad (GPL), a BSB (CC0) blokk marad; az MCGED csak ingyenes, nem kereskedelmi kiadásban marad, megjelöléssel (a kapcsoló a DT-M6-hoz kötött); **DT-M6**: az első kiadás nem kereskedelmi, blokkonként dataset-kulccsal, forrás- és licencjelöléssel; **DT116**: a projekt saját adata (a Károli–Strong párosítás és származékai) minden jog fenntartva.
- Nyitva: **DT-F60c**: a `KJV_Strongs_teljes.tsv` (GPL-forrás) a nyilvános repóban áll és a `pardes.db` betöltheti; a `licencek.tsv` sora ma „tisztázatlan”. A kiadáshoz a fájl sorsa (kivezetés / marad) és a kiadási kapcsoló kell. A **#89** (LICENC_RENDEZES) a `licencek.tsv` `projekt_adat` sorát és a táblaszintű licencet rendezi; a pilot méri, nem oldja meg.
- Mért következmény a blokkokra: a CC BY-SA források (SDBH/SDGNT, UBS, LSJ, tW) share-alike jelölést kérnek; a `pardes.db` szükséges részhalmaza tartalmaz licenc-oszlopot (D4: 548,4 MB, a `licenc_*` oszlopok nélkül 424,5 MB).
- A kiadási kapcsoló **elkészült** (F60.45): az `adat.py --kiadas {belso,nyilvanos,kereskedelmi}` (alap: `belso`, az eddigi kiadások változatlanok): a `nyilvanos` a KJV-Strong blokkot (GPL), a `kereskedelmi` a KJV-Strong és az MCGED blokkot is kiveszi (adat, statisztika, proveniencia-sor, a lapról a blokk); teszt mindhárom értékre (`TestKiadas`).
- Javaslat: a #25a briefje a generátor szintjén a kapcsolót vegye át, és a DT-F60c lezárását feltételként vegye fel.

**Tárhely.**
`scope=pardes.db a lapokhoz szükséges táblákra | forras=pardes.db meta.epites_ts=2026-10-12T08:27:32Z (hash: 3. pont); naplok/SQLITE_EPIT_meres.md (MiB-ből MB-ra átszámolva); ADATVAGYON_TERV 3. és 7. szakasz | ts=2026-10-12T17:44Z`
- A szükséges részhalmaz 548,4 MB kicsomagolva (a táblák 884,8 MB-os összegének 62,0%-a; a fájl 886,4 MB), becsült tömörített mérete ≈ 117,8 MB (arányos becslés a mért 0,215-ös gzip-arányból, nem külön mérés).
- Az ADATVAGYON_TERV 3. szakasza a Netlify-function határát ~50 MB tömörítve / ~250 MB kicsomagolva adja: a szükséges rész **a határ fölött** van (≈118 MB a ~50 MB ellen). A terv 3. szakasza erre a Cloudflare Workers + D1-et vagy a külön fájlként (Netlify Blobs) tárolt SQLite-ot nevezi kiútnak; a 7. szakasz „50–150 MB indexekkel” becslése alatt a szükséges rész 548 MB kicsomagolva nem marad.
- A statikus oldal mérete: az 1Móz 1–25 oldala 11,2 MB (gzip+base64; nyersen 35,8 MB), a Zsolt 22 3,1 MB. A tömörítés a böngészőben `DecompressionStream`-et igényel (Safari < 16.4 nem).
- Javaslat: a #25a briefje a hosting-⛔ előtt dönti el a kiszolgálás módját (statikus oldalak vagy lekérdező function); a két mért adat: ≈118 MB tömörítve a függvény-keret fölött, és 11,2 MB 25 fejezetenként a statikus oldalaknál (a teljes ÓSZ+ÚSZ statikus kiadásának mérete nincs mérve).

**Fordítások (#38, #80, #27/#7).**
`scope=1Móz 1–25 és Zsolt 22 | forras=a 2. pont táblája; FELADATOK #38, #80, #27, #7 sorai; konkordancia/BDB_teljes_unabridged.tsv, BDB_strong_alias.tsv, BDB_strong_alias_elvetett.tsv, BDB_strong_potlas.tsv, BDB_aram_potlas.tsv, adat/forditasok.tsv (a 12 szó-lap Strong-száma szerint; ellenőrző szkript a repón kívül) | ts=2026-10-12T17:50Z`
- **#38** (BDB magyar fordítás, ▶ fut, gyakorisági sorrendben): a magyar BDB-lefedettség 40,8% / 70,4% a két szakaszon; a 12 szó-lapnak, amelynek sem magyar, sem angol szócikke van (H0553, H1746, H3231, H3252, H4138, H4176, H5503, H5668, H5745, H6820, H7742, H8646), a #38-ban nincs pótlása. **Ellenőrzés (saját lekérdezés, 2026-10-12):** a 12 Strong-számnak nincs sora a `BDB_teljes_unabridged.tsv`, a `BDB_strong_alias.tsv`, a `BDB_strong_potlas.tsv`, a `BDB_aram_potlas.tsv` táblában és az `adat/forditasok.tsv` BDB-soraiban sem; négynél (H3231, H4176, H5745, H6820) a `BDB_strong_alias_elvetett.tsv` ad elvetett alias-sort (`nem_ebbol_a_szocikkbol`), nyolcnál (H0553, H1746, H3252, H4138, H5503, H5668, H7742, H8646) semmilyen BDB-tábla nem említi. Az alias-szal megjelenő lapok (15: 6 magyar, 9 angol szócikkel) **más** szó-lapok, ezekre a #57 alias-táblája ad szócikket. A 12 lap szócikke tehát a jelenlegi BDB-táblákban nem található: pótlásához új forrás-lekérdezés (a `lexikonok_nyers/BDB.lexicon`) kell, ez a #38 / #80 dolga.
- **#80** (BDB_KAROLI_POTLAS, kész): az `adat/bdb_karoli.tsv` a Károli-támasz nélkül fordított szócikkek adatblokkja, a `forditasok.tsv` változatlan; a pilot a magyar szócikk-szöveget a `forditasok.tsv`-ből veszi.
- **#27 / #7** (Thayer fordítás; halasztott, D46: az OLVASOI_KONKORDANCIA oldja fel a #7-et): a görög szó-lapok magyar jelentése 0,7% / 1,0%; ma az angol TBESG/Thayer áll, az állapotjelzéssel. A #7 indítása a #25a (#76) menetében eldöntendő.
- Javaslat: a #25a első kiadása az angol eredetit állapotjelzéssel vállalja (a pilot ezt kipróbálta, K2), a magyar lefedettséget pedig kiadási küszöbként ne írja elő; a küszöb a #38 ütemétől függene, és ezt a felhasználó dönti.

**Versszámozás (DT-F60b).**
`scope=Zsolt 22 (31 vers) | forras=konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/LXX_OS/psalms-lxx.tsv (zsolt_felirat_eltolas), 3. és 6. pont; DONTESEK.md DT-F60b | ts=2026-10-12`
- A `Karoli_versmegfeleltetes.tsv` és az LXX_OS KJV-oszlopa a Zsolt 22 31 versében ellentmond; a pilot az LXX_OS Károli-kulcsával kerüli meg és jelzi.
- DT-F60b eldöntve (1.): új feladat a feliratos zsoltárok (kb. 60+) Károli–KJV számozására (`beerkezo/ZSOLT_FELIRAT_SZAMOZAS_brief.md`, befogadásra vár).
- Javaslat: a #25a a Zsoltárokat a feladat lezárásáig (vagy a pilot kerülőútjával, jelzéssel) vegye fel; az 1Móz 1–25-ben a versszámozás D2-egyezése 0 eltérés (más könyvet a pilot nem mért).

### 8.3 TSV vagy `pardes.db` (M2b, D1–D5)

`scope=1Móz 1–25 és Zsolt 22 | forras=pardes.db meta.epites_ts=2026-10-12T08:27:32Z meta.mod=teljes (hash: 3. pont) | ts=2026-10-12T17:44Z`

- **Mi mondja az adatbázis mellett:** a blokkok 35/39 (34/39) csak belőle állítható elő (D1), a D2 szerint a felsorolt blokkokban a két út azonos (0 eltérés), négy blokkban eltér (BDB angol és magyar alias-szócikk 9 + 6 / 1 + 1 héber lap, ÚSZ-előfordulás 117 / 52 görög lap, LXX-versszám 356 / 28 vers; az okok a 3. pont D2 táblájában), és a lekérdezési idő ms-tartományú (D3).
- **Mi hiányzik az adatbázisból (D1/D2):** (a) az igealak-kód és szófaj (Macula), (b) a héber–görög párosítás szavanként (Macula), (c) a görög szóalak és az LXX-vers szavai (LXX_OS): az építő ezeket szándékosan nem tölti be (+207,6 MB TSV-méret, ha betöltené); (d) a BDB-alias tábla (`BDB_strong_alias.tsv`; 9 + 6 szó-lapot érint az 1Móz 1–25-ben); (e) a Nave-témák versekre bontása (a bontás az `adat.py` gépi feldolgozása; az `igehely_tartomany` 124 sora kell); (f) az LXX-versszám a vers-laphoz (356 / 28 eltérés), mert az `lxx_versszintu_parok` csak a héber–görög Strong-párral rendelkező versekre ad sort.
- **Frissesség (D5):** a 39 tábla `meta` hash-e egyezik a tábla mai tartalmával; a forrás-TSV-k az építés után módosultak (`token_eredeti`, `token_strong`: TAGNT +350 sor; `token_par`); ennek a következménye az ÚSZ-előfordulás-eltérés (117 / 52 görög lap). Az adatbázis tehát az építés pillanatának képe, nem élő nézet.
- **Méret:** 886,4 MB a fájl, a lapokhoz kell 548,4 MB (D4; l. 8.2 Tárhely; MB = 10^6 bájt).
- Javaslat: az olvasói felület ma **TSV-ből épüljön** (statikus lap, a három Macula/LXX_OS-blokkal együtt; a felsorolt blokkokban a két út mindkét szakaszon azonos, a négy eltérő blokk okai a 3. pont D2 táblájában), a `pardes.db` az **interaktív lekérdezésre** (keresés, szó-lap, vers-lap) kerüljön, a hiányok (a)–(f) pótlásával az építőben (ezek a #79 vagy egy utódfeladat dolga), és a két út D2-egyezését a #25a tesztje őrizze. A döntés a felhasználóé.

### 8.4 Javaslatok (döntés nélkül)

1. A #25a briefjébe: a kiadási kapcsolók (KJV-Strong ki; MCGED a kereskedelmi módban ki) — **a kapcsoló elkészült** (F60.45, `adat.py --kiadas {belso,nyilvanos,kereskedelmi}`, tesztelve; a briefbe a generátor-szintű átvétel kerül) —, a DT-F60c lezárása feltételként, a #89 licenc-rendezés után indulás.
2. A tárhely a brief első pontja: ≈118 MB tömörítve az ~50 MB-os function-keret fölött, tehát a statikus kiadás vagy a külön tárolt SQLite/D1 dönt a hostingról.
3. Az első kiadás az angol eredetit vállalja (állapotjelzés), magyar lefedettségi küszöb nélkül; a #38 és a #27/#7 külön ütem.
4. A feliratos zsoltárok számozása a külön feladatban (DT-F60b); addig a pilot kerülőútja.
5. A felület: minden Károli-szó kattinthatóságának kérdése (a szavak kb. 41%-a ma nem kattintható); a mockup (réteges szó-lap, igazítási sáv, Ctrl+K, mobil lap) kipróbálva, a #25a briefjébe vihető.
6. A BDB-szeletelés „próba” felirata addig marad, amíg az 510 számozott jelentés nélküli szócikk (47,4%) okát nem vizsgálták (külön feladat vagy a #38 folytatásában).
7. A pilot újrafuttatható (a #27, #80, #88, #89 után a mérés frissíthető: `eszkozok/olvaso_pilot/README.md`).

### 8.5 Korlátok

A D3 a régi ág szó-lapjainak részhalmazát méri (az újabb blokkok lekérdezési ideje nincs benne); a tömörített részhalmaz-méret becslés; az 1Móz 1–25 és a Zsolt 22 két szakasz, a költői könyvek és az ÚSZ általánosítása nincs mérve. A független ellenőr első jelentése (`naplok/ELLENOR_OLVASOI_PILOT.md`, 14 eltérés) javítva (F60.44 és köv.); az ellenőr újrafuttatása és a felhasználói M3 további észrevételei még hátra vannak.
