---
feladat: 60
cim: Olvasói pilot — a konkordancia-nézet mérhető próbája két szakaszon, csak adatból, jelölt jelleggel
kod: OLVASOI_PILOT
tipus: feladat
fazis: folyamat
modell: sonnet
munka: adat
allapot: lezarva
ag: claude/olvasoi-pilot
pr: https://github.com/basesoft777/Bible-Study/pull/318
lezarva_osszegzes: "1Móz 1–25 és Zsolt 22 olvasói pilot, a két párhuzamos futás egyesítve (v3.2); M2/M2b mérés, M3 döntések (DT124, DT125, szeletelő-átnézés), M4 értékelés a #25a feltételeiről; 1. ellenőri kör 14, 2. kör 5 eltérés, mind javítva (F60.44–F60.53); K1 eltérés elfogadva (v3.5); 100 teszt, CI zöld; nyitott: DT126, a beerkezo-brief befogadása; zárójelentés: naplok/OLVASOI_PILOT_zaras.md"
ad: a repóban futó olvasói pilot (eszkozok/olvaso_pilot/) két szakaszon (1Móz 1–25 és Zsolt 22), minden blokk jellegjelöléssel (forrásadat / gépi feldolgozás / modell-kimenet), és egy értékelő jelentés számokkal, amely megmutatja, mit tud a repó adata az olvasói konkordanciához, és mi kell a #25a-hoz (FELADATOK #76, OLVASOI_KONKORDANCIA; a DT-M1 2026-10-06-án eldőlt: 1. opció)
kovetkezo: "lezárva; merge a felhasználótól"
olvas: [eszkozok/olvaso_pilot/README.md, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, "konkordancia/Macula_heber_*.tsv", "konkordancia/LXX_OS/*.tsv", konkordancia/TSK_kereszthivatkozasok.tsv, konkordancia/Karoli_kereszthivatkozasok.tsv, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/Strong_szotar.tsv, konkordancia/TBESG.txt, konkordancia/Thayer_teljes.tsv, konkordancia/UBS_DBH_referenciak.tsv, konkordancia/UBS_DBH_jelentesek.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, "adat/karoli_strong/*.tsv", adat/forditasok.tsv, adat/kulso/lxx_bridge.tsv, adat/licencek.tsv, MUNKATERV.md, ADATVAGYON_TERV.md, eszkozok/sqlite_epit.py, naplok/SQLITE_EPIT_meres.md, adat/morf_kulcs_heber.tsv, adat/morf_nyelv_aramai.tsv, adat/kapcsolatok.tsv, adat/elofordulasok.tsv, adat/lxx_dontesek.tsv, adat/motivumok.tsv, konkordancia/BSB_Strongs.tsv, konkordancia/KJV_Strongs_teljes.tsv, konkordancia/Nave_basokant.tsv, konkordancia/TIPNR_kivonat.tsv, konkordancia/SDBH_domenek.tsv, konkordancia/SDGNT_domenek.tsv, konkordancia/SECE_H_teljes.tsv, konkordancia/SECE_G_teljes.tsv, konkordancia/OSHL_lexikalis_index.tsv, konkordancia/LSJ_teljes.tsv, konkordancia/MCGED_teljes.tsv, konkordancia/UBS_DNTG_jelentesek.tsv, konkordancia/tW_szocikkek.tsv, konkordancia/TBESH.txt, konkordancia/LXX_versszintu_parok.tsv, konkordancia/LXX_tobblet_szakaszok.tsv, konkordancia/Verzifikacios_elteres_tabla.tsv]
ir: [eszkozok/olvaso_pilot/adat.py, eszkozok/olvaso_pilot/bdb_szelet.py, eszkozok/olvaso_pilot/epit.py, eszkozok/olvaso_pilot/sablon.html, eszkozok/olvaso_pilot/README.md, eszkozok/olvaso_pilot/teszt_olvaso_pilot.py, eszkozok/olvaso_pilot/db_meres.py, eszkozok/olvaso_pilot/kjv_osszevetes.py, eszkozok/olvaso_pilot/bovites.py, eszkozok/olvaso_pilot/felmeres.py, naplok/OLVASOI_PILOT_adatfelmeres.md, eszkozok/olvaso_pilot/meres.py, naplok/OLVASOI_PILOT_naplo.md, naplok/OLVASOI_PILOT_ertekeles.md, eszkozok/olvaso_pilot/szakasz.py, naplok/OLVASOI_PILOT_meres.md, naplok/OLVASOI_PILOT_ellenorzolista.md, naplok/OLVASOI_PILOT_szeletelo_atnezes.md, naplok/OLVASOI_PILOT_zaras.md, DONTESEK.md, beerkezo/ZSOLT_FELIRAT_SZAMOZAS_brief.md, naplok/ELLENOR_OLVASOI_PILOT.md]
fugg: []
nem_fugg: [7, 9, 22, 27, 38, 52, 54, 56, 57, 80, 88, 89]
---

# F60_OLVASOI_PILOT_BRIEF.md — Olvasói pilot

*FELADATOK #60 · Modell: sonnet · v3.4 · 2026.10.12 · kiinduló állapot: `eszkozok/olvaso_pilot/` (a 2026-10-05-i prototípus, README-vel) · döntés-előkészítés: DT-M1 (eldőlt, 1.), a #25a feltételei*

## 1. Cél

A munkaterv DT-M1 döntése azt kérdezte, kiadható-e az olvasói konkordancia (vers- és szó-lap, motívum nélkül) a migráció (#11, #23) előtt; a felhasználó 2026-10-06-án eldöntötte (1.: a #25 kettéválik, #25a = FELADATOK #76). A #25a briefjéhez mérés kell arról, mit tud a repó adata egy valós olvasási helyzetben. A 2026-10-05-i prototípus (1Móz 1:1–2:3) ezt megmutatta egy szakaszon. A feladat ezt **reprodukálható, mérhető pilottá** teszi.

**Alapszabály (felhasználói döntés, 2026-10-05):** a pilot csak adatból dolgozik. Ami nem változatlan forrásadat, az jelölve van: **gépi feldolgozás** (determinisztikus szabály) vagy **modell-kimenet** (nyelvi modell fordítása vagy párosítása). Magyarázó szöveg nem kerülhet a lapra; az a #59 jóváhagyott szószedetén át jöhet később.

## 2. Hatókör

**Benne van:**
- a prototípus paraméterezése szakaszra (`--szakasz`), és egy második szakasz, a **Zsoltárok 22** (költői szöveg, feliratos zsoltár versszámozással, a Károli–Strong párosításon kívüli könyv);
- a jellegjelölés teljessége és ellenőrzése (M1);
- mérőszámok és értékelő jelentés (M2, M4);
- a `pardes.db` mérése ugyanazon a két szakaszon (M2b): előállítható-e belőle a lap, ugyanazt adja-e, mint a TSV-út, és milyen gyorsan, mekkora részhalmazból;
- tesztek.

**Nincs benne:**
- nyilvános közzététel, tárhely, kereskedelmi licenc (DT-M6, a 4. hullám);
- motívumréteg (#25b);
- új adat előállítása: a hiányokat a pilot méri és jelzi, nem pótolja (a pótlás a #54, #57, #58, #59 dolga). Ahol a BDB- vagy a Thayer-szócikk magyar fordítása hiányzik, ott az **angol eredeti** áll (forrásadat-jelleggel, „magyar fordítás hiányzik” állapotjelzéssel); ez megjelenítés, nem adatpótlás (felhasználói döntés, 2026-10-12).

## 3. Lépések

### M0 — Átvétel és paraméterezés

- Az `adat.py` kapjon `--szakasz` paramétert (pl. `"1Móz 1-25"`, `"Zsolt 22"`). A versek listája a `Karoli_1908.tsv`-ből jön, a könyvfájlok (Macula, LXX_OS) a `Konyv_normalizalo_tabla.tsv` és a meglévő névkonvenciók szerint.
- Az 1Móz 1:1–2:3 kimenete (az 1Móz 1–25 szakasz elejeként) legyen azonos a prototípuséval (bájtra azonos JSON, a `ts` mező kivételével). Ez a regressziós alap.

### M1 — Jellegjelölés és „csak adat” ellenőrzés

- Minden blokk jelleg-címkéje a README táblázata szerint. A Károli–Strong párosításon alapuló aláhúzás modell-kimenet.
- Hiányzó magyar BDB- vagy Thayer-fordítás helyén az angol eredeti áll (`BDB_teljes_unabridged.tsv`, `Thayer_teljes.tsv`), `forras` jelleggel és állapotjelzéssel; a szócikk-blokk nem maradhat üresen, ha az angol eredeti megvan.
- **Ellenőrző lista** a jelentésben: a sablon minden szövege vagy (a) felületi utasítás (mire lehet kattintani), vagy (b) adatból jön. Ami egyik sem, az kikerül. A független ellenőr ezt külön ellenőrzi.
- `teszt_olvaso_pilot.py`: legalább a fő szó választása (1Móz 1:4 „világosságot” → H0216, „setétségtől” → H2822), a görög szóalak párosítása (1Móz 1:1 → ἀρχῇ), a BDB-bontás (H7225: 1. a., 1. b., 2.; H0216: 11 jelentés).

### M2 — Mérés

Mindkét szakaszra, proveniencia-sorral (`scope=… | forras=… | ts=…`):
- a Károli-szavak hány százaléka kötött héber szóhoz (magas / alacsony bizonyosság);
- a héber szó-lapok hány százalékának van magyar BDB-szócikke, angol szócikke, vagy egyik sem;
- a BDB-bontás: hány szócikk bomlik legalább 2 jelentésre, hány marad egyben (lista);
- a görög szó-lapok: magyar jelentés, újszövetségi előfordulás, héber háttér aránya;
- a görög szóalak forrása (LXX_OS / Macula) és a χ/ξ-eltérések száma;
- a UBS-jelentés lefedettsége, a versszámozási eltérések (Zsolt 22 felirat).

### M2b — A `pardes.db` mérése

Az `eszkozok/olvaso_pilot/db_meres.py` mindkét szakaszon méri, mit ad a `pardes.db` (#79) az olvasói lapnak. Csak olvas (`mode=ro`), külön szkript; a pilot fő kimenete (`adat.py` → JSON → HTML) továbbra is a TSV-kből készül. A meglévő adatbázist méri, nem építi újra; a jelentés megadja, melyik építésen mért (`meta.epites_ts`, `meta.mod`). Ha nincs `pardes.db`, az M2b „nem mérhető” eredményt ír, nem hibát.

Mindkét szakaszra, proveniencia-sorral; a `forras=` mezőben a `pardes.db` építési időpontja és a felhasznált táblák `meta` hash-e:
- **D1 — blokk-lefedettség:** a lap blokkjai közül melyik állítható elő csak a `pardes.db`-ből, és melyikhez kell TSV, forrástáblánként listázva. Ismert kiindulás: az építő a Macula- és az LXX_OS-táblákat szándékosan nem tölti be (`eszkozok/sqlite_epit.py`, „Szándékosan nem betöltött konkordancia-táblák”), ezért az igealak, a héber–görög párosítás és a görög szóalak várhatóan TSV-n marad; ezt a mérés igazolja vagy cáfolja.
- **D2 — egyezés:** a TSV-ből és a `pardes.db`-ből előállított blokkok összevetése versenként (a D1 szerint előállítható blokkokon); az eltérések száma és listája, okkal (normalizálás, versszámozás, építés óta változott TSV).
- **D3 — lekérdezési idő:** vers-lap és szó-lap adatának előállítása, medián és p95, hideg és meleg gyorsítótárral; a gép és a fájl mérete a jelentésben.
- **D4 — szükséges részhalmaz mérete:** a lapokhoz ténylegesen használt táblák (és indexeik) bájtmérete a teljes adatbázishoz képest (`naplok/SQLITE_EPIT_meres.md` táblánkénti mérete alapján); viszonyítás az ADATVAGYON_TERV 3. és 7. szakaszának korlátaihoz.
- **D5 — frissesség:** a `meta` táblánkénti sorszám és hash összevetése a forrás-TSV-k mérés kori állapotával; az eltérő táblák listája.

A kereskedelmi licencszűrés (DT-F33j) nem része a mérésnek (DT-M6).

### M3 — ⛔ Felhasználói átnézés

A felhasználó megnézi mindkét szakasz oldalát. A közzétételt privát artifactként az orkesztrátor végzi; a végrehajtó a HTML-t a `--kimenet` könyvtárba írja, és a jelentésben megadja az útvonalát. A felhasználó jelzi, mi hiányzik, mi felesleges, és melyik mérőszám a döntő. Az észrevételek a jelentésbe kerülnek.

### M4 — Értékelő jelentés és zárás

- `naplok/OLVASOI_PILOT_ertekeles.md`: a mérőszámok, az M3 észrevételei, és annak az adatalapú bemutatása, **mi kell a #25a-hoz** (licenc, tárhely, hiányzó fordítások, versszámozás) a mért adatállapot mellett (v3.3: a DT-M1 opcióinak összevetése már nem feladat, a döntés megszületett). Az M2b alapján külön pont: az olvasói felület a `pardes.db`-ből vagy a TSV-kből épüljön, és ha az adatbázisból, mi hiányzik belőle (D1). Javaslat lehet, döntés nem: a döntés a felhasználóé.
- `naplok/OLVASOI_PILOT_zaras.md` (≤20 sor), `fuggetlen-ellenor` (`naplok/ELLENOR_OLVASOI_PILOT.md`), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Az 1Móz 1–25 lefut, és az 1Móz 1:1–2:3 része azonos a prototípuséval; a Zsolt 22 is lefut, hiba nélkül.
- **K2.** Minden blokk jelleg-címkét és adatforrás-jelzést kap; a lapon nincs adatforrás nélküli tartalmi szöveg; magyar fordítás hiányában az angol BDB-/Thayer-szócikk áll.
- **K3.** A mérőszámok mindkét szakaszra proveniencia-sorral állnak a jelentésben, és a jelentés külön pontban adja a #25a feltételeit a mért adat szerint (v3.3).
- **K4.** A tesztek zöldek; a kimenet nem kerül a repóba (CLAUDE.md: `--kimenet` a repón kívül); a CI zöld; a független ellenőr eltérés nélkül zár.
- **K5.** A D1–D5 mindkét szakaszra proveniencia-sorral áll a jelentésben (`forras=` a `pardes.db` építési időpontjával és `meta` hash-ével), vagy „nem mérhető” jelöléssel, ha nincs adatbázis; a teszt legalább egy vers-lap és egy szó-lap D2-egyezését ellenőrzi.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | A pilot csak adatból dolgozik; ami értelmezés (gépi feldolgozás, modell-kimenet), az jelölve van. | felhasználó |
| v1 | 2026-10-05 | Kiinduló állapot a prototípus (`eszkozok/olvaso_pilot/`); második szakasz a Zsolt 22 (költői szöveg, feliratos zsoltár, párosításon kívüli könyv). | befogadás |
| v1 | 2026-10-05 | `fazis: folyamat`: döntés-előkészítő eszköz, nem az adat- vagy a render-fázis része; a #57, #58 lezárása után újrafuttatható. | befogadás |
| v1 | 2026-10-05 | `nem_fugg: [52]`: a tervdokumentum olvasása kontextus. | kontextus-olvasás |
| v1 | 2026-10-05 | `nem_fugg: [7, 9, 22, 38, 54, 56, 57]`: a pilot az aktuális adatállapotot méri, nem vár a táblákat író feladatokra; ezek lezárása után újrafuttatható (a jelentés rögzíti, melyik állapoton mért). | befogadás |
| v2 | 2026-10-07 | **Egyeztetett eltérés a briefhez (bővítés „maxra”):** a pilotot a repó minden használható, már meglévő adatával bővíteni kell, és fel kell mérni a pilot datasetjét (`naplok/OLVASOI_PILOT_adatfelmeres.md`). Új adat nem készül; csak meglévő táblát jelenítünk meg vagy mérünk. Az alapszabály marad (jelleg-, adatforrás-jelzés, licenc; magyarázó szöveg nincs). A hatókör „nincs benne: új adat előállítása” nem változik. | felhasználó (orkesztrátor útján) |
| v1.1 | 2026-10-12 | `nem_fugg` + 80: a #80 (BDB_KAROLI_POTLAS) az `adat/forditasok.tsv`-t írja, ezért a #60 levezetett függést kapott (`FUGGES 60 80 adat/forditasok.tsv*`); ugyanaz az indok, mint a #38-nál: a pilot az aktuális adatállapotot méri, a hiányt jelzi, nem pótolja | a felhasználó jóváhagyása a chatben (2026-10-12) |
| v2 | 2026-10-12 | Az első szakasz hatóköre 1Móz 1:1–2:3 helyett **1Móz 1–25**; a Zsolt 22 marad. Az 1Móz 1:1–2:3 a regressziós alap marad (a prototípussal bájtra azonos rész). | a felhasználó jóváhagyása a chatben (2026-10-12) |
| v3 | 2026-10-12 | Új M2b lépés: a `pardes.db` mérése (D1 blokk-lefedettség, D2 egyezés a TSV-úttal, D3 lekérdezési idő, D4 szükséges részhalmaz mérete, D5 frissesség) és K5; `ir` + `db_meres.py`, `olvas` + `sqlite_epit.py`, `SQLITE_EPIT_meres.md`. A pilot fő kimenete TSV-ből marad; az adatbázist nem építi újra. Ok: az ADATVAGYON_TERV szerint a `pardes.db` elsődleges felhasználója az olvasói felület, a pilot eddig nem próbálta ki. | a felhasználó jóváhagyása a chatben (2026-10-12) |
| v3.1 | 2026-10-12 | `nem_fugg` + 27, 88, 89: mindhárom levezetett függés olvasás–írás átfedés (#27: `adat/forditasok.tsv`; #88, #89: `eszkozok/sqlite_epit.py`), nem tartalmi; a pilot az aktuális adatállapotot méri (az M2b a `meta.epites_ts`-t rögzíti), a lezárásuk után újrafuttatható. Hiányzó magyar BDB-/Thayer-fordítás helyén az angol eredeti áll (M1, K2). | a felhasználó jóváhagyása a chatben (2026-10-12) |
| v3.2 | 2026-10-12 | A #60 két párhuzamos futása egyesítve: a régi ág (`claude/olvasoi-pilot`, 2026-10-07) az alap; a mai ágból (`claude/f60-olvasoi-pilot`) átvéve: az 1Móz 1–25 hatókör, a `db_meres.py` (M2b), a v3.1 angol-pótlás szabálya; a mai ág nem folytatódik | a felhasználó döntése a chatben (2026-10-12) |
| v3.3 | 2026-10-12 | Az M4 pontosítása: a DT-M1 2026-10-06-án eldőlt (1. opció: a #25 kettéválik #25a-ra és #25b-re), ezért az értékelő jelentés nem a DT-M1 három opcióját veti össze, hanem a mért adatállapot mellett megmutatja, **mi kell a #25a-hoz** (licenc, tárhely, hiányzó fordítások, TSV vagy `pardes.db`). `ad`, Cél, M4, K3 igazítva. | a felhasználó jóváhagyása a chatben (2026-10-12) |
| v3.4 | 2026-10-12 | Az M3 döntései: a „Gépi szeletelés (próba)” felirat marad; **DT124** (F60.39–F60.40: a belső pilotban minden blokk marad; a KJV-Strong blokk minden nyilvános kiadásból kimarad (GPL); az MCGED csak nem kereskedelmi kiadásban marad; a kiadási kapcsoló előkészítése: `adat.py --kiadas`, F60.45); **DT125** (F60.34: új feladat a feliratos zsoltárok Károli–KJV számozására, `beerkezo/ZSOLT_FELIRAT_SZAMOZAS_brief.md`); a BDB-szeletelő átnézése (F60.35–F60.38). **K1:** a prototípussal (`ce4ef98f`) való azonosság az 1Móz 1:1–2:3 szakaszon értékazonosság, a `ts` és egy indokolt, darabszámmal rögzített engedélyezett-eltérés lista kivételével (nem bájtra azonos): *Egyeztetendő eltérés*, `naplok/OLVASOI_PILOT_ertekeles.md` 5. pont 3.; a K1 és az M0 brief-szövege változatlan. | a felhasználó döntései a chatben (2026-10-12); az eltérés a független ellenőr jelentése nyomán (`naplok/ELLENOR_OLVASOI_PILOT.md`), egyeztetésre vár |
| v3.5 | 2026-10-12 | A K1 egyeztetendő eltérése elfogadva: a prototípussal (`ce4ef98f`) értékazonosság a bájtazonosság helyett, a `naplok/OLVASOI_PILOT_ertekeles.md` 5.3 engedélyezett-eltérés listájával (`TestRegresszioProto`). A feladat lezárva. | a felhasználó döntése a chatben (2026-10-12) |
