# OLVASOI_PILOT zárás (F60, #60)

*scope=1Móz 1–25 és Zsolt 22 | forras=naplok/OLVASOI_PILOT_ertekeles.md (meres.py, db_meres.py; pardes.db meta.epites_ts=2026-10-12T08:27:32Z) | ts=2026-10-12*

- Készült: az `eszkozok/olvaso_pilot/` két szakaszon (1Móz 1–25: 693 vers; Zsolt 22: 32 vers), jellegjelöléssel és angol eredetivel a hiányzó magyar BDB/Thayer helyén; a két párhuzamos futás egyesítve (v3.2: a régi ág az alap, a mai ágból az 1Móz 1–25, a `db_meres.py`, az angol-pótlás); a brief v3.3 (az M4 a #25a feltételeit mutatja, DT-M1 eldőlt).
- Fő számok: kötött Károli-szó 58,8% / 59,7%; magyar BDB 40,8% / 70,4% a héber lapokon; görög lap magyar jelentéssel 0,7% / 1,0%; Zsolt 22 párosítása 100% „alacsony”; D1: 35/39 és 34/39 blokk csak a `pardes.db`-ből; D2: 0 eltérés; D4: 523,0 MB (≈112 MB tömörítve) a ~50 MB-os function-keret ellen.
- Döntések: DT-F60a (belső pilotban minden blokk; KJV-Strong kimarad minden nyilvános kiadásból; MCGED csak nem kereskedelmiben), DT-F60b (új feladat a feliratos zsoltárok számozására), a „Gépi szeletelés (próba)” felirat marad.
- BDB-szeletelő: 19 szócikk átnézve (11 javult, 5 romlott és visszaállítva, 3 mindkettő hibás); 147 szócikk szerkezete változott; a személyszám-jelölő tévesen jelentés-sorszám: 177 → 3.
- Tesztek: `teszt_olvaso_pilot.py` 85 teszt OK (1 kihagyva); `feladatok.py ellenoriz` 110 brief, 0 hiba, 0 figyelmeztetés.
- Nyitott: DT-F60c (a `KJV_Strongs_teljes.tsv` GPL-forrás a nyilvános repóban; 🟡).
- Nyitott: a szeletelő ismert hibái (H0834, H3318, H1157, H2009, homonima-törzsek) és az 510 számozott jelentés nélküli BDB-lap (47,4%) oka.
- Nyitott: a `tW_szocikkek.tsv` egy cikkében U+FFFD (forrásadat-hiba, nem javítva).
- Nyitott: `beerkezo/ZSOLT_FELIRAT_SZAMOZAS_brief.md` (befogadásra vár, `/befogad`).
- Nyitott: további M3-észrevételek; független ellenőr (`naplok/ELLENOR_OLVASOI_PILOT.md`), push, draft PR, a brief `lezarva` (az orkesztrátor).
- Javaslatok (döntés nélkül): `naplok/OLVASOI_PILOT_ertekeles.md` 8.4.
- Tanulság a két párhuzamos futásról: ugyanazt a feladatot két ágon, két munkamásolatban futtatni kétszeres munka és ütköző döntéssorok lett (egyesítés: F60.26); a brief frissüljön a döntés után, és egy feladathoz egy ág tartozzon.
