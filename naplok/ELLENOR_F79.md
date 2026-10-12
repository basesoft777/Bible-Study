# ELLENOR_F79 — F79_SQLITE_EPIT_BRIEF.md · `origin/main..HEAD` (0351f214 … ba0f9793)

*A `fuggetlen-ellenor` jelentése, írási eszköz híján az orchestrator mentette el, tartalmilag változatlanul tömörítve. Az ellenőr nem futtatta a teszteket, az építőt és a `feladatok.py ellenoriz`-t (NEM ELLENŐRIZHETŐ).*

**Eredmény: ELTÉRÉS, 9 tétel.**

## Rendben (OK)
- G1: a diff nem érinti az `adat/`, `konkordancia/`, `motivumok/`, `lexikon/` könyvtárat; `pardes.db` nincs a repóban (`.gitignore:27-30`).
- G3: nincs `csv` modul, beolvasás `general.tsv_beolvas` (`split('\t')`).
- G4: a szabályok az `ellenoriz.py`-ból jönnek (`sqlite_epit.py:164-177`); negatív teszt az 1–6., 8., 9., 13. szabályra; a 10. és 11. szabályra nincs.
- G8: méret és idő proveniencia-sorral a `SQLITE_EPIT_meres.md`-ben.
- D1–D3, DT109 (1), (5), (6): rendben; az FTS fájlköre 50 fájl.
- Sorszám-egyezés adat- és konkordancia-táblákon rendben; Δ = 0 minden `adat/` és `konkordancia/` táblán.
- ⛔ M0: rendben. CI-futtatás (`futtat.py`) exit 0.

## ELTÉRÉSEK (súlyosság szerint)
1. **G5:** a `Karoli_Strong_kivonat.tsv` (383 sor) a brief név szerinti normalizálandó datasetje, de nincs betöltve és a `normalizalas_jelentes`-ben sem szerepel; a zárónapló „nincs nevesítve” indoka téves.
2. **G7:** a 9 pontos lekérdezés-próba eredménye az F79.5 újragenerálásával (`t.db`, `--proba` nélkül) eltűnt a `SQLITE_EPIT_meres_minta.md`-ből; a zárónapló erre hivatkozik. Az ellenőr szúrópróbával (H0922, H8414, G0012) a törölt próba 1., 4., 14. pontját újra egyezőnek találta.
3. **G6:** a `morf_kulcs_heber` és a `morf_nyelv_aramai` saját `licencek.tsv`-sora (CC BY 4.0, kereskedelmi igen, tisztazott, megjelölés kötelező) helyett `projekt_adat` licencet kapnak (`sqlite_epit.py:686-691`).
4. **Méret:** a 786 MB a `licenc_*` oszlopok nélkül is ~574 MB; a túllépés zöme redundáns táblákból (`frazis_pozicio`, `token_strong`), a briefen túl betöltött táblákból (`ubs_*_referenciak`, `nave_basokant`) és indexekből jön; táblánkénti bájtméret nincs mérve, az N-F86b bemenete hiányos.
5. **Nem betöltött táblák:** a `KJV_Strongs_teljes` és a `TBESG`/`TBESH` az M0 séma-tervében szerepelt, mégsem épült; a `KJV_Strongs_teljes` „#48 vezeti ki” indoka téves (a #48 csak a régi `KJV_/ASV_Strongs_*`-t vezeti ki). Macula, `LXX_OS`, BDB-segéd, SDBH-domének nem hiányok.
6. **TIPNR:** 16 928 sor (47,7%) `strong`-ja NULL, mert `utotag='tilt'` fut; a `strong_util.py` `utotag='megtart'` támogatott.
7. **TAGNT:** a Károli-vers nélküli kulcsok (Róm 3:31, 1Kor 3:23, Róm 8:39) jelentés nélkül kerülnek a `token_eredeti`/`token_strong` táblákba.
8. **Brief:** a döntésnaplóban a DT109 „nyitott”, a DONTESEK.md-ben 🟢.
9. **M0 napló:** a sorszámok (11/261/41/594/225/25/105/58, licencek 52) fejléccel és megjegyzéssorokkal együtt számoltak; a valós érték 9/259/39/592/222/23/92/56, licencek 46.

## NEM ELLENŐRIZHETŐ
G2 (második teljes építés hash-táblája nincs naplózva), M3 ⛔ jóváhagyás bizonyítéka, a 30 teszt futtatása, `feladatok.py ellenoriz`.
