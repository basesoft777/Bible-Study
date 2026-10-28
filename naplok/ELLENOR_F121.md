# ELLENOR_F121 — F121_GLOSSZA_FORDITAS_BRIEF.md · `f3f9372b..4f363c5b`

*A `fuggetlen-ellenor` (claude-opus-5-5) jelentése, a végrehajtó rögzítette (az ellenőr nem tudott fájlt írni). Verdikt: **ELTÉRÉS: 9 tétel**. A végrehajtó kezelése a jobb oldali oszlopban.*

**OK:** forrásszöveg = konkordancia (6/6); meglévő sorok bájtra azonosak (0 törölt sor); az élő lap diffje csak a 6 egység (22 sor), más lap nem változott; a maradék `(fordításra vár)` a 136. sori lábjegyzet; helyőrző-megfeleltetés helyes (h→376, f→377), maradék 0; Károli/BDB-következetesség (`segítségül hívni`, `kiáltom előtted az Úr nevét`, `istenség` 58 előfordulás); `split('\t')`, `csv` nélkül; E5, E10, E17 rendben; A1 proveniencia.

| # | Eltérés (súly) | Kezelés |
|---|---|---|
| 1 | SEMA 2.14 nem bővült: `UBS_DBH` a `szotar` listában, a forrásszöveg leírása, `allapot=sonnet` UBS-re (közepes) | **Javítva** (F121.5, `adat/SEMA.md`) |
| 2 | A brief „Nincs benne” pontjait átlépték (generátor, éles lap), DONTESEK-tétel nélkül (közepes) | **Javítva**: DT-F121e, a felhasználó szó szerinti idézetével (az orkesztrátor chatjéből, „Mehet, javítással”) |
| 3 | Kimaradt mankók: szójegyzék-gyűjtő (DT240/E11), Károli-adatblokk (E9), visszamenőleges felmérés (DT242) (közepes) | **Nyitott — a felhasználó döntése**: elengedhető-e a 6 sorra? (a gyűjtő és az adatblokk-eszköz a #121 hatókörében sem készült el; a Károli-alakok kézzel, `lekerdez.py karoli`-val igazolva a naplóban) |
| 4 | CI E16: a PR címe `[ELLENŐRZŐ]` előtagú legyen (a csere két ellenőrző-fájl kommentjét érintette) | A PR-címben (még nincs PR) |
| 5 | Nincs `rogzit` alparancs, a rögzítés nem reprodukálható | **Részben**: az egyszeri szkript elmentve (`naplok/F121_rogzit_6sor.py`); általános `rogzit` nem készült (a 6 sor nem indokolja) |
| 6 | DT234 1. opció: „`licencek.tsv` új sora” nem készült | **Pontosítva** a DT234 sorában: az UBS_DBH/UBS_DNTG sor már CC BY-SA 4.0 |
| 7 | Fordítás-hűség: (i) „valakinek (valaminek) a nevét kiáltani” — a „(something)” a megnevezett tárgy; (ii) „remembered” → „emlegetnek” (pontosabb: „emlékeznek rá”); (iii) „the essence of one's being” → „a lény lényegét” (pontosabb: „létének lényegét”); a 007442001004000 „az azonosság magja” eltér a v4 `azonosságának magja` sortól (alacsony) | **Nyitott — a felhasználó döntése** (a szövegek jóváhagyottak, DT-F121d) |
| 8 | A brief `kovetkezo` mezője elavult | **Javítva** |
| 9 | Apróságok: napló kapu-oszlop, `15_tiltott`/`14_tiltott`, docstring DT-száma, két `F121.3` commit, halott kód (`_dbh_idx`, `forras_szoveg_dbh`) | A napló és a docstring **javítva**; a halott kód és a commit-számozás marad |

A 1b (SHA-1 újraszámolás), 2 E2 (13. szabály), E6 (kapuk), DT241 nem volt az ellenőr számára futtatható; a végrehajtó `ellenoriz.py` (SÉRTÉS 0) és a kapufuttatás (6/6 ÁTMENT) eredménye a naplóban áll.
