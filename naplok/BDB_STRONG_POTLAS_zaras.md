# F57 BDB_STRONG_POTLAS — zárójelentés

*Proveniencia: scope=konkordancia/BDB_strong_potlas.tsv + BDB_strong_alias.tsv + BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_strong_potlas.py | ts=2026-10-05*

- **Felmérés (M0):** a BDB.lexicon 10 022 szócikkéből 846 címke nélküli; az OSHL szerint 590 Strong hiányzik a táblából (529 másodlagos címke, 61 `H<n>` kulcs nélküli).
- **Párosítás (M1), állapotonként (846 címke nélküli szócikk):** `egyertelmu` 3, `tobb_jelolt` 0, `nincs_par` 843 (két sorban mássalhangzó-egyezési tipp, jelölt marad).
- **Pótlás (M2):** a `BDB_teljes_unabridged.tsv` +3 sor a végén (H4725 mákóm, H4123, H0747), 8090 → 8093 sor; a meglévő sorok bájtra azonosak (írás előtt/után: a régi tartalom prefixum, csak 3 új sor).
- **Másodlagos címke:** 529 Strong (H0136, H0341 is) nem kerül a táblába; `konkordancia/BDB_strong_alias.tsv` (generált, 529 sor, 513 címszóval igazolt).
- **Döntések:** DT-F57a 🟢 (felhasználó, 2026-10-05), DT-F57b (az `ir` bővítése).
- **Tesztek:** `eszkozok/teszt_bdb_strong_potlas.py` 11 teszt zöld (H4725, homonímia, kizárás, tábla, alias).
- **Hiány:** a `DictBDB.json` nem volt a repóban, közvetlen ellenőrzése nem történt (M0 5. pont); licenc: a `lexikonok_nyers` és a BDB sor „tisztázatlan”, azonos kiadás.
- **A #38 következő menete** újragenerálja a fordítási sorrendet (`BDB_FORDITAS_M0.py`), ezzel a 3 pótolt szócikk bekerül a sorba; az alias-tábla a szó-lapok Strong→sor feloldásához kell.
- **Hátra:** független ellenőr (`naplok/ELLENOR_BDB_STRONG_POTLAS.md`), draft PR, a brief `lezarva` állapota; ezt az orkesztrátor végzi.
