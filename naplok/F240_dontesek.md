# F240 (LXXBDB) — az integrátor döntései (MUNKAMENET „Szereposztás”, #835)

A session ennek a fájlnak az aktuális állapotát hajtja végre. Egy sor: sorszám, dátum, kérdés – döntés – indok, a szerkesztő szava, ha van; a visszavont sor „visszavonja: D<n>” jelölést kap. Az 1–8. sor a #835 előtt üzenetben érkezett, itt utólag, az üzenetek szövege szerint rögzítve.

| # | Dátum | Kérdés | Döntés | Indok | A szerkesztő szava | Integrátor |
|---|---|---|---|---|---|---|
| D1 | 2026-11-23 | Indul-e most a végrehajtás? | Nem: „a kis adatjavítás most csak a briefig megy”; „Javítást, lapgen-futást és független ellenőrt most ne indíts.” A `kovetkezo`: „vár: szabad szálhely (IRANY)”. | Irányváltás: a TEREMT-001 lett az első. | (irányváltás, a szerkesztő) | local_e56f6f28 |
| D2 | 2026-11-23 | A brief jóváhagyása és száma | „A brief jóváhagyva”; a szám a `kovetkezo_szam --foglal` által adott (240, `foglalas/F240`). | A #238 foglaltnak látszott; „amit az ad, az legyen a tiéd”. | — | local_e56f6f28 |
| D3 | 2026-11-23 | ⛔1: az LXX_OS homográf-hibái | (b) külön N-tétel és külön PR (N-F240a); a #240 kapuja addig „az LXX_OS-re kivétellel éljen, darabszám-plafonnal, amely csak csökkenhet”. (DT-F240a) | A letöltés új forrás; egy feladat = egy kis PR (IRANY). | — | local_e56f6f28 |
| D4 | 2026-11-23 | ⛔2: Strong-szám nélküli helyes lemma | Igen: „megfelelő nélkül”, „kifejezetten jelölve, nem csendben üres”. (DT-F240b) | A hamis megfelelés rosszabb a hiányzónál (CLAUDE.md 3. szabály). | — | local_e56f6f28 |
| D5 | 2026-11-23 | Letöltési engedély az N-F240a-hoz | Megvan: lxx-morph `verse_pairs.jsonl` és `GreekWordList.js`, rögzített verzióval; az N-F240a-ba beírandó. | — | „Igen, letölthető” | local_e56f6f28 |
| D6 | 2026-11-23 | Hatókör-bővítés: tehóm „örvény · 5” | A #240 egy tétellel bővül (L5): a `bdb_vers_jelentes.py` gyökérok-javítása minden szóra, a teljes tábla újragenerálása soronkénti diffel, kapu; a kiadott lapok mérése, találat esetén azonnali jelzés. | A „see N infra” utalás jelentéskezdetként olvasva. | — | local_8f20af99 |
| D7 | 2026-11-23 | Hatókör-bővítés: πόντος → Pontusz | A #240 egy tétellel bővül (L6): gyökérok, a többi eset mérése, gépi kapu. | LXX-címkehiba. | — | local_8f20af99 |
| D8 | 2026-11-23 | ⛔3: a πόντος javításának helye | Az N-F240a PR-jában (az LXX_OS újragenerálásával); a #240 csak mér és csökkenő plafonú kaput tesz rá. Az N-F240a sorrendje: a #240 után, a TEREMT-001 1. kiadása előtt. | Ugyanaz a gyökérok, mint a καρπός → Κάρπος esetben; a D3 is külön PR-ba tette. | — | local_8f20af99 |
| D9 | 2026-11-24 | Mikor indul a végrehajtás? | Az integrátor adja meg az indítást, „amikor a TEREMT-001 a 218c-re vár; addig ne kezdj.” | Lépésrend: a TEREMT-001 az első (D1). | — | local_5140778b |
