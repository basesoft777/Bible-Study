# TSK_VERSSZAM — zárójelentés (FELADATOK #114)

*Ág: `claude/tsk-versszam` (origin/main be85d5de-ről) · végrehajtó: `vegrehajto-sonnet` (claude-sonnet-5-5) · orkesztrátor: claude-opus-5-5 · 2026-10-18 · push/PR: nincs (kérésre)*

1. **Eredmény.** Új közös átváltó: `eszkozok/tsk_kulcs.py` (KJV↔Károli, explicit „nincs pár”, egységtesztekkel). Mind az öt fogyasztó ezen át olvas: `lexikon_general`, `lekerdez`, `nem_vizsgalt`, `sqlite_epit`, `olvaso_pilot/adat`. A `TSK_kereszthivatkozasok.tsv` érintetlen.
2. **Mérés** (`naplok/TSK_VERSSZAM_jelentes.md`): az ÓSZ-en 0 rossz és 0 elmaradó sor. A kivétel-verseken ez körkörös, mert a kivétellel bővített megfeleltetéshez mér. Nem körkörös veszteségmérés a main-hez képest: `naplok/F114_elveszett_sorok.tsv`, osztályonként.
3. **Döntések** (helyőrzők, 🟢):
   - DT199: 7 HAMART-001-jelölt átkulcsolva (`jeloltek.tsv` 7 sor).
   - DT197: az ÚSZ-en kimondott korlát (N-F114a).
   - DT198 és DT201: `tsk_kulcs_javitas` kategória, 46 név szerinti sor.
   - DT200: MT-tartalék csak az `MT|szamlalas` osztályra. „Nincs pár” kivétel: 1Kir 22:46–49, Ézs 3:1–26, Jón 2:2–10, 1Sám 24:1–22.
4. **Nyitott maradék, kimondott korlátként:**
   - N-F54a: táblahibák és tábla-lyukak.
   - Az ALVIL-001 Jón 2:3 és a TEREMT-001 Jón 2:6 TSK nélkül marad.
   - Az 1Kir 22:45 eltolt.
   - Jón 2:1 (N-F41a).
   - N-F114a, N-F114b.
   - Az N-F09g a merge után zárul.
5. **Független ellenőrzés** (`naplok/ELLENOR_TSK_VERSSZAM.md`, négy kör). Az 5, 3, 3 és 4 eltérést mind javítottuk, vagy a felhasználó döntésére kimondott korlátként rögzítettük.
6. **Egyeztetett eltérés.** A #114 felülbírálja a #115-ből levezetett függést. A felhasználó szavai: „a #114 felülbírálhatja a #115-függést, a #115 csak a #114 merge-e után fut.”
   - **A #115-nek:** az átfedés egyetlen fájl, az `eszkozok/sqlite_epit.py` (`_kereszthivatkozasok()`, `import tsk_kulcs`). A #115 a #114 merge-e után rebase-eljen.
7. **Ismert, nem #114-hatás.** `teszt_bdb_vers_jelentes.Ujrageneralas.test_bajtra_azonos` (DT-F99n/DT179 számozás). Az olvasó-szerver régi `pardes.db`-je a `tsk` táblát a #101-ig KJV-kulccsal tartja.
8. **Írási halmaz.** A brief `ir` mezőjén kívül csak a `DONTESEK.md`, a `NYITOTT_FELADATOK.md`, a brief fejléce és a `naplok/` változott. Az `eszkozok/ellenorzes/`, a workflow, a `motivumlog/PaRDeS_motivumok.md` és a `FELADATOK.md` érintetlen.
