# F30 zárójelentés — számkiosztás merge-kor

- **Ág / PR:** `claude/szamozas`; a PR-t az orkesztrátor nyitja. **A PR címe `[ELLENŐRZŐ]` előtagú legyen (E16: a PR a `.github/`-ot és az `eszkozok/ellenorzes/`-t érinti).** Ellenőrzés: `naplok/ELLENOR_F30.md` (az orkesztrátor futtatja).
- **Kész:** `eszkozok/szamkiosztas.py` (`--proba`/`--ir`, idempotens), `.github/workflows/szamkiosztas.yml`, CI-szabály E26, tesztek (10 új, a meglévő 74 zöld), `CLAUDE.md`/`BRIEF_SABLON.md`/`DONTESEK.md` fejléc.
- **SZ.0:** main: DT1–7, DT18, DT19, DT22–28; legnagyobb N: N46; 99 helyőrző definíciós sorral (70 DT-F, 29 N-F), 17 árva; nyitott ágon átállítandó azonosító nincs.
- **DT18:** a #18 feladatszámából képzett hibás szám; átszámozva **DT29**-re („korábbi azonosító” jelzéssel); a lezárt `ELLENOR_*` és `F16_zaras.md` régi említése változatlan.
- **D-sorozat:** a FELADATOK.md „Döntésnapló” kézzel nő, ezért `D-F<nn>` helyőrző; az Action és az E26 kezeli.
- **Döntés (felhasználó, 2026-10-05):** DT-F30a, 1. opció: az örökölt 99 helyőrző marad (`szamkiosztas_oroklott.txt`), csak az újak kapnak számot; a 3. később lépésenként; a tömeges kiosztás nem.
- **Egyeztetett eltérés:** (a) az `ir` lista bővül: `futtat.py`, `test_szamkiosztas.py`, `szamkiosztas_oroklott.txt`, `naplok/F30_*` (rögzítve: N-F30a (5)); (b) az `ir` listán kívül kizárólag a DT18→DT29 csere (F18 brief, SEMA, datasetek.tsv, `naplok/F18_*`), a diffen ellenőrizve; (c) SZ.6 próba helyben, próba-PR nélkül (a megbízás tiltotta).
- **Próba:** helyőrzős döntések E26 zöld; végleges szám (`DT44`) E26 piros; `--proba`/`--ir` helyes és idempotens (`naplok/F30_szamozas_naplo.md`).
- **Nyitott (N-F30a):** a DT19 ugyanilyen feladatszám-alakú (és ütközik a régi F21-kimenetek „DT19”-ével); 17 árva helyőrző; a GitHub-oldali Action-futást csak az első main-merge igazolja (várható: DT-F30a → DT30, N-F30a → N47).
- **Folytatási pont:** nincs; az örökölt helyőrzők fokozatos kiosztása (DT-F30a 3. opció) külön, lépésenkénti döntés.
