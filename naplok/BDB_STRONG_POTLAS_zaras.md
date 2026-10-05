# F57 BDB_STRONG_POTLAS — zárójelentés

*Proveniencia: scope=konkordancia/BDB_strong_potlas.tsv + BDB_strong_alias.tsv + BDB_strong_alias_elvetett.tsv + BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_strong_potlas.py | ts=2026-10-05*

- **Felmérés (M0):** a BDB.lexicon 10 022 szócikkéből 846 címke nélküli; az OSHL szerint 590 Strong hiányzik a táblából (529 másodlagos címke, 61 `H<n>` kulcs nélküli).
- **Párosítás (M1), 846 címke nélküli szócikk:** `egyertelmu` 3, `tobb_jelolt` 0, `nincs_par` 843 (két sorban mássalhangzó-egyezési tipp, jelölt marad).
- **Pótlás (M2):** a `BDB_teljes_unabridged.tsv` +3 sor a végén (H4725, H4123, H0747), 8090 → 8093 sor; a meglévő sorok bájtra azonosak; az új sorok feje a meglévő egyszerűsített átírást követi (Arisay tulajdonnévként nagybetűvel, mahatallot, maqom), a könyvnevek és az írásjelezés a meglévő sorokhoz igazítva.
- **Másodlagos címke (529), DT-F57f/g:** alias `BDB_strong_alias.tsv` **256** sor (héber 243, arámi 13); elvetett `BDB_strong_alias_elvetett.tsv` **273** sor (héber 99, arámi 174), jelölt marad. Feltétel: `bdb_id`-egyezés + a szócikk latin betűinek ≥ 0,9 hányada a testvérsor elején (héber szöveg és hivatkozások nélkül) + egy testvér. Elvetés: `nem_ebbol_a_szocikkbol` 220 (arámi 172), `a_testversor_mas_szocikk` 12, `tobb_testveres` 37, `kezi_dontes` 3, `kifejezes_tarscimke` 1. A várt ~294 aliastól való eltérés oka a 37 több testvéres sor kizárása.
- **Kint tartott sorok:** H2088 (kifejezés-társcímke), H3071, H3073, H3074 (`kezi_dontes`, a felhasználónak); H3347 → H4169 az új szabály szerint alias.
- **Arámi számok:** 187 (BDB.lexicon nyelvjelölés, a felhasználó száma) vs 198 (ellenőr): az utóbbi nem reprodukálható, a 11-es különbség oka nem azonosítható; mérvadó a feltétel.
- **Döntések:** DT-F57a, DT-F57b (az `ir` bővítése), DT-F57c, DT-F57e (felváltva: DT-F57f), DT-F57f, DT-F57g 🟢; **DT-F57d 🟡 nyitott: az elvetett arámi szócikkek (~190 sor) pótlása külön feladat a `/befogad` útján.**
- **Tesztek:** `eszkozok/teszt_bdb_strong_potlas.py` 23 teszt zöld (H4725, homonímia, kizárás, tábla, alias-feltétel, arámi eset, elejegyezés, átírás, stílus).
- **Hiány:** a `DictBDB.json` nem volt a repóban, közvetlen ellenőrzése nem történt; licenc: BDB és `lexikonok_nyers` „tisztázatlan” (a README is jelzi).
- **A #38 következő menete** újragenerálja a fordítási sorrendet (`BDB_FORDITAS_M0.py`), így a 3 pótolt szócikk bekerül; az arámi pótlásig a fordítási sor az arámi szócikkekre hiányos.
