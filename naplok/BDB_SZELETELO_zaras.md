# BDB_SZELETELO (#99) — zárójelentés (a célzott újraellenőrzés előtt, 2026-10-15)

- **Hatókör (felhasználó, 2026-10-15):** a #99 az M0–M2 tartalommal zárul, „próba” jelöléssel; az M3–M6 nem készült el, külön feladatba ment.
- **Kész:** M0 (aranyminta 32 szócikk, mérések), M1 (OSHL-gyökcsalád blokk), M2 (`adat/bdb_vers_jelentes.tsv`, 160 616 sor, soronkénti proveniencia, a fejlécben minden forrás és a kód LF-re normalizált hash-sel, bájtra újragenerálható).
- **NEM teljesült:** az aranyminta 0 eltérés (EN 7/32, HU 4/14 hibás szócikk); a jelentéspont ≥ 97% (seed-101: **92,0%**, 95% CI 87,3–95,4%; az ítélet után 93,5%). DT-F99l (c): a tábla „próba” jelöléssel élesedett, a nyers mért szám a szó-lapon.
- **Az aranyminta átnézése modell-ellenőrzés volt** (független ellenőr + második modell-ellenőr); a felhasználó az eltérésekről döntött, a szócikkeket nem nézte át.
- **Károli-kulcs (DT-F99h (b)):** az F85 esetlistája és az Ézs 3 alapján 514 sor más Károli-versre került; maradék nyitott: 1Krón 12, 5Móz 5 (N-F99e), Neh 7:68 (N-F99d).
- **Szűrés a seed-101-en:** kiszűrt réteg 3/25 hamis pozitív (2 TAHOT-igazolt), bizonytalan réteg 7/22 eltérés a vak kitöltéssel — a javítási feladatba.
- **Külön feladat (brief-tervezetek, `beerkezo/`):** szeletelő-javítás (BDB_SZELETELO_JAVITAS), M3 tagolás + terminológia a #38-kötéssel (BDB_M3_TAGOLAS), M4 megjelenítés a DT-F99m-mel (BDB_M4_MEGJELENITES), M5 héber szórend (BDB_M5_SZOREND), M6 modell-magyarázat, DT-F99d (BDB_M6_MAGYARAZAT).
- **Nyitott tételek:** N-F99a (tW nyers Markdown), N-F99b (OSHL-táblázat mobilon), N-F99c (pilot Zsolt 22-tesztek), N-F99d, N-F99e.
- **Napló:** `naplok/BDB_SZELETELO_M0.md` (0. összegzés, 2–9.14); ítéletek: `naplok/BDB_SZELETELO_M2_seed100_iteletek.md`, `…_seed101_iteletek.md`; ellenőr: `naplok/ELLENOR_F99.md`.
