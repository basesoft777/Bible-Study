# F57 BDB_STRONG_POTLAS — zárójelentés

*Proveniencia: scope=konkordancia/BDB_strong_potlas.tsv + BDB_strong_alias.tsv + BDB_strong_alias_elvetett.tsv + BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_strong_potlas.py | ts=2026-10-05*

- **Felmérés (M0):** a BDB.lexicon 10 022 szócikkéből 846 címke nélküli; az OSHL szerint 590 Strong hiányzik a táblából (529 másodlagos címke, 61 `H<n>` kulcs nélküli).
- **Párosítás (M1), 846 címke nélküli szócikk:** `egyertelmu` 3, `tobb_jelolt` 0, `nincs_par` 843 (két sorban mássalhangzó-egyezési tipp, jelölt marad).
- **Pótlás (M2):** a `BDB_teljes_unabridged.tsv` +3 sor a végén (H4725, H4123, H0747), 8090 → 8093 sor; a meglévő sorok bájtra azonosak; az új sorok stílusa a meglévőkhöz igazítva (1Kin/Psa/Hosea…).
- **Másodlagos címke (529):** alias `BDB_strong_alias.tsv` 290 sor (héber 276, arámi 14); elvetett `BDB_strong_alias_elvetett.tsv` 239 sor (héber 66, arámi 173), jelölt marad. Feltétel: a testvérsor ugyanabból a BDB-szócikkből származik (`bdb_id`) + szövegegyezés (DT-F57c).
- **Arámi számok:** 187 (BDB.lexicon nyelvjelölés, a felhasználó száma) vs 198 (ellenőr): az utóbbi nem reprodukálható, a 11-es különbség oka nem azonosítható; mérvadó a `bdb_id`-feltétel.
- **Döntések:** DT-F57a, DT-F57b (az `ir` bővítése, alias és elvetett fájl, jelentések), DT-F57c 🟢; **DT-F57d 🟡 nyitott: az elvetett arámi szócikkek (~190 sor) pótlása külön feladat a `/befogad` útján.**
- **Tesztek:** `eszkozok/teszt_bdb_strong_potlas.py` 15 teszt zöld (H4725, homonímia, kizárás, tábla, alias bdb_id-feltétel, arámi eset, stílus).
- **Hiány:** a `DictBDB.json` nem volt a repóban, közvetlen ellenőrzése nem történt; licenc: BDB és `lexikonok_nyers` „tisztázatlan” (a README is jelzi).
- **A #38 következő menete** újragenerálja a fordítási sorrendet (`BDB_FORDITAS_M0.py`), így a 3 pótolt szócikk bekerül; az arámi pótlásig a fordítási sor az arámi szócikkekre hiányos.
- **Hátra:** ismételt független ellenőrzés, draft PR, `lezarva` állapot (orkesztrátor).
