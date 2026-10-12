# OLVASOI_PILOT zárás (F60, #60)

*scope=1Móz 1–25 és Zsolt 22 | forras=naplok/OLVASOI_PILOT_ertekeles.md (meres.py, db_meres.py; pardes.db meta.epites_ts=2026-10-12T08:27:32Z; az M4-javításban újramérve) | ts=2026-10-12T17:44Z*

- Készült: az `eszkozok/olvaso_pilot/` két szakaszon (1Móz 1–25: 693 vers; Zsolt 22: 32 vers), jellegjelöléssel és angol eredetivel a hiányzó magyar BDB/Thayer helyén; a két párhuzamos futás egyesítve (v3.2: a régi ág az alap, a mai ágból az 1Móz 1–25, a `db_meres.py`, az angol-pótlás); a brief v3.3 (az M4 a #25a feltételeit mutatja, DT-M1 eldőlt).
- Fő számok: kötött Károli-szó 58,8% / 59,7%; magyar BDB 40,8% / 70,4% a héber lapokon; görög lap magyar jelentéssel 0,7% / 1,0%; Zsolt 22 párosítása 100% „alacsony”; BDB-bontás (az F60.35–F60.38 után): 537 / 124 szócikk bomlik 2+ jelentésre; D1: 35/39 és 34/39 blokk csak a `pardes.db`-ből; D2: 0 eltérés a felsorolt blokkokra (Károli, párosítás, héber szó, versszámozás, TSK, UBS, Strong-szótár, héber előfordulás, TBESG/Thayer, lxx_bridge), **négy blokkban van eltérés**: BDB-alias (9 + 6 / 1 + 1 héber lap), ÚSZ-előfordulás (117 / 52 görög lap, TAGNT +350 sor az építés óta), LXX-versszám (356 / 28 vers); D4: 548,4 MB (≈118 MB tömörítve; MB = 10^6 bájt, a fájl 886,4 MB) a ~50 MB-os function-keret ellen; a HTML 11,2 MB / 3,1 MB (gzip+base64, a teljes angol TBESG/Thayer-szöveggel).
- Döntések: DT124 (belső pilotban minden blokk; KJV-Strong kimarad minden nyilvános kiadásból; MCGED csak nem kereskedelmiben), DT125 (új feladat a feliratos zsoltárok számozására), a „Gépi szeletelés (próba)” felirat marad.
- BDB-szeletelő: 19 szócikk átnézve (11 javult, 5 romlott és visszaállítva, 3 mindkettő hibás); 147 szócikk szerkezete változott; a személyszám-jelölő tévesen jelentés-sorszám: 177 → 3.
- M4-javítás (az ellenőr 14 eltérése): CI E5, K1 (értékazonos prototípus-regresszió engedélyezett-eltérés listával, 1Móz 1–25 teszt), újramérés, teljes angol szöveg, TBESH licencsor adatból, `adat.py --kiadas {belso,nyilvanos,kereskedelmi}` (DT124 2. előkészítése), A1-ellenőrzés (a 12 BDB nélküli lap nincs alias alatt).
- Tesztek: `teszt_olvaso_pilot.py` 100 teszt OK (0 kihagyva); `feladatok.py ellenoriz` 110 brief, 0 hiba, 0 figyelmeztetés.
- Nyitott: DT126 (a `KJV_Strongs_teljes.tsv` GPL-forrás a nyilvános repóban; 🟡).
- Nyitott: a szeletelő ismert hibái (H0834, H3318, H1157, H2009, homonima-törzsek) és az 510 számozott jelentés nélküli BDB-lap (47,4%) oka.
- Nyitott: a `tW_szocikkek.tsv` egy cikkében U+FFFD (forrásadat-hiba, nem javítva).
- Nyitott: `beerkezo/ZSOLT_FELIRAT_SZAMOZAS_brief.md` (befogadásra vár, `/befogad`).
- Lezárás: a K1 eltérése (értékazonosság, `ertekeles.md` 5.3) a felhasználó elfogadásával (v3.5); független ellenőr két köre (`ELLENOR_OLVASOI_PILOT.md`, `_2.md`), mind javítva; draft PR: basesoft777/Bible-Study#318.
- Javaslatok (döntés nélkül): `naplok/OLVASOI_PILOT_ertekeles.md` 8.4.
- Tanulság a két párhuzamos futásról: ugyanazt a feladatot két ágon, két munkamásolatban futtatni kétszeres munka és ütköző döntéssorok lett (egyesítés: F60.26); a brief frissüljön a döntés után, és egy feladathoz egy ág tartozzon.
