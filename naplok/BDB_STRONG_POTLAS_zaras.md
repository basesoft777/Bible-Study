# F57 BDB_STRONG_POTLAS — zárójelentés

*Proveniencia: scope=konkordancia/BDB_strong_potlas.tsv + BDB_strong_alias.tsv + BDB_strong_alias_elvetett.tsv + BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_strong_potlas.py | ts=2026-10-05*

- **Felmérés (M0):** a BDB.lexicon 10 022 szócikkéből 846 címke nélküli; az OSHL szerint 590 Strong hiányzik a táblából (529 másodlagos címke, 61 `H<n>` kulcs nélküli).
- **Párosítás (M1), 846 címke nélküli szócikk:** `egyertelmu` 3, `tobb_jelolt` 0, `nincs_par` 843 (két sorban mássalhangzó-egyezési tipp, jelölt marad).
- **Pótlás (M2):** a `BDB_teljes_unabridged.tsv` +3 sor a végén (H4725, H4123, H0747), 8090 → 8093 sor; a meglévő sorok bájtra azonosak; az új sorok feje a meglévő egyszerűsített átírást követi (Arisay tulajdonnévként nagybetűvel, mahatallot, maqom), a könyvnevek és az írásjelezés a meglévő sorokhoz igazítva.
- **Másodlagos címke (529), DT42/g/h/i:** alias `BDB_strong_alias.tsv` **296** sor (héber 282, arámi 14); elvetett `BDB_strong_alias_elvetett.tsv` **233** sor (héber 60, arámi 173), jelölt marad. Feltétel: `bdb_id`-egyezés + a szócikk latin betűinek ≥ 0,9 hányada a testvérsor elején (héber szöveg és hivatkozások nélkül); több testvérnél a pontosan egy megfelelő az alias célja. Elvetés (`indok_kod`): `nem_ebbol_a_szocikkbol` 220 (arámi 172), `a_testversor_mas_szocikk` 9, `kuszob_alatt` 3 (H0706, H6737, H8112; jelöltek, nincs egyenkénti beemelés), `kifejezes_tarscimke` 1 (H2088: a „zeh” egy attá-kifejezés társcímkéje, téves alias volna).
- **Alias a H3071, H3073, H3074 is** (DT45: az alias azt mondja meg, hol áll a BDB-szövege). A várt ~294-nél 2-vel több: H5853/H5855 → H5852 (0,981) a szabály szerint alias.
- **Arámi számok:** 187 (BDB.lexicon nyelvjelölés, a felhasználó száma) vs 198 (ellenőr): az utóbbi nem reprodukálható, a 11-es különbség oka nem azonosítható; mérvadó a feltétel.
- **Döntések:** DT37, DT38 (az `ir` bővítése), DT39, DT41 (felváltva: DT42), DT42, DT43, DT44, DT45 🟢; **DT40 🟡 nyitott: az elvetett arámi szócikkek (~190 sor) pótlása külön feladat a `/befogad` útján.**
- **Tesztek:** `eszkozok/teszt_bdb_strong_potlas.py` 27 teszt zöld (H4725, homonímia, kizárás, tábla, alias-feltétel, arámi eset, elejegyezés, átírás, stílus).
- **Hiány:** a `DictBDB.json` nem volt a repóban, közvetlen ellenőrzése nem történt; licenc: BDB és `lexikonok_nyers` „tisztázatlan” (a README is jelzi).
- **A #38 következő menete** újragenerálja a fordítási sorrendet (`BDB_FORDITAS_M0.py`), így a 3 pótolt szócikk bekerül; az arámi pótlásig a fordítási sor az arámi szócikkekre hiányos.
