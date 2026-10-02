# ELLENOR_F41 — F41_BSB_UJRAMERES_BRIEF.md — origin/main(898610a)..claude/f41-bsb-ujrameres(9ef6434)

*A `fuggetlen-ellenor` jelentése; a subagentnek nem volt írási eszköze, a főszál mentette változtatás nélkül (rövidítve a táblázat OK-soraival).*

**ELTÉRÉS: 6 tétel** (súlyosság szerint)

1. **D3/A1 — magas.** A Préd 11/12, az Ézs 2/3 és a Jób 38–40 átszámozása Károli-szerű, illetve hibrid TAHOT-számozásra történt, nem MT-re. `lekerdez.py karoli "Préd 12:1"` = KJV 11:9; `karoli "Ézs 3:1"` = KJV/MT 2:22; `karoli "Jób 39:1"` = KJV/MT 38:39; `scan H0930` → Jób 40:15 (KJV-szám). A Jób a main-en KJV-számozású volt, most egyik szabványnak sem felel meg. Az N-F41d és a DT-F41b „KJV/masszoréta keverékként” írja le a TAHOT-ot, a (4) Károli-opciót alternatívaként kínálja: a döntés alapja téves.
2. **G2/K5 — magas.** A Jób 41 223 sora (`modell=kjv_szamozas`, igazolatlan megfeleltetés) bekerült az importba, sorszintű jelölés nélkül (csak a naplóban). Ütközik a nyitó prompttal („nem igazolható → kimarad, jelölve”). A felhasználói jóváhagyásra („ne essen ki”) csak a d42b729 commit-üzenet hivatkozik.
3. **D3/b — közepes.** Az átszámozás, az 1Kir 22:43 két MT-versre osztása és a Jób 41 bennhagyása mellett a jóváhagyás nincs a `DONTESEK.md`-ben. Az osztás ütközik a brief 3.1 szabályával („több MT-vers → nem importálható”); maga az osztás tartalmilag helyes (`kollokacio H1116 H6999` → 1Kir 22:44).
4. **G6/b — alacsony.** A `naplok/F41_nulladiff.txt` commitolatlan ideiglenes szkripttel készült, nem reprodukálható; a számok halmazkülönbségek.
5. **3.4 — alacsony.** Az állapot-ellenőrzés a memóriabeli számlálóval vet össze, nem a „szurt sorok” számlálóival (hatókör eltér: szurt `elhagyva`=55588 / 66 könyv, importált 30952); nincs dokumentálva.
6. **D5 — alacsony.** A DT-F41a opciói nem szó szerint a DT6-ból valók.

**OK:** G1 (küszöb 95% változatlan, 36 ELÉRI), G3 (Jón/Préd/Hós/Ézs/1Sám ≥ diagnózis), G4 (2Sám 35, Ezsd 15, Dán 37 eltérés okkategóriával), G5 (278 125 sor, `ures_jelzo_nelkul`=0), D1, D2 (korláttal: a Jóbnál az R4 nem ellenőrzött, a KK részben a TAHOT-ból készült), D4, D6, 3.1 ⛔, 3.4 ⛔ (BSB_Strongs-ot oszlopsorszámmal senki nem olvas), N-F41c hangos hiba (kódban; teszt nem ellenőrizhető), CSV-tilalom, N-F41a (Jón 2:1), brief-javítás, A6, K1, K4. Saját `futtat.py` futás: E2–E16, E19 0 találat, EXIT=0.

**Nem ellenőrizhető:** G6 teljes nulladiff (205 320 sor), a CI-egyezés (CI-jelentés nem érkezett), a 3.1 chat-jelentés, a Macula-állítások (nincs `lekerdez.py` parancs). A2: merge után a `datasetek.tsv` / README / SEMA még „31 könyv / 242 597” (N-F41e).

*Megjegyzés: az ellenőrzés közben a munkafa átmenetileg a `main`-re állt; a vizsgálat a `9ef6434` SHA-n és mentett diffeken futott.*
