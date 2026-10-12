# F80 BDB_KAROLI_POTLAS — zárójelentés (claude/f80-karoli-potlas)

- **Elvégezve:** M0 felmérés (`naplok/BDB_KAROLI_POTLAS_M0.md`), M1 pótlás, M2 ellenőrzés. Az új `adat/bdb_karoli.tsv` (12,3 MB, 62 526 sor = 674 `szocikk` + 61 852 `alak`) mind a 674 kész BDB-szócikk Károli-alakját és példaversét hordozza, vers + Strong + Károli-alak kulccsal, sorszám és versszöveg nélkül; minden sor proveniencia-sorral.
- **Változatlan:** `adat/forditasok.tsv` bájtra azonos (blob `1060f59d`, sha256 az építés előtt és után egyezik); a `forditas_hu` nem változott.
- **Döntések:** DT-F80a (külön tábla, hivatkozás kulccsal, mind a 674) és DT-F80b (kanonikus példasorrend, minden sor proveniencia-sora), mindkettő 🟢, a felhasználó chatbeli döntése.
- **Kód:** `eszkozok/bdb_adatblokk.py` (`--karoli-epit`, `parok_konyvek()` a `Konyv_normalizalo_tabla.tsv` sorrendjében, hibával ismeretlen könyvre, `Sir`→`JSir` alias); SEMA 2.25; tesztek 45 zöld.
- **Mellékhatás a #38-ra:** az új BDB-adagok blokkjában más példaversek lesznek, és az 1. szakasz `par_db`-sora pontosabb; a kész fordítások szövege nem változik. Jelzés: `NYITOTT_FELADATOK.md` N-F80a.
- **Ellenőrzés:** `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba; független ellenőr kétszer (`naplok/ELLENOR_BDB_KAROLI_POTLAS.md`: 6 eltérés, `…_2.md`: 5 eltérés), mind javítva.
- **Eltérés a briefhez:** az ellenőr javításait és a v3 döntést a menet közben egyeztettük; két korábbi teszt (`test_nincs_karoli_alak`, `test_pelda_idezet_szo_szerinti`) a teljes ÓSZ-párosításhoz igazítva (az első mockkal, a második az első idézett versre).
- **Nyitott:** a tábla licenc-/regisztrációs kérdése (a testvértáblák sincsenek az `adat/datasetek.tsv`-ben vagy a `licencek.tsv`-ben) — a #89 hatóköre, licencdöntés nem született. A tesztek a main-re rebase után futottak, a CI-t a PR mutatja.
- **Merge:** nem történt; a PR draft.
