# F41 zárójelentés (FELADATOK #41; ág: `claude/f41-bsb-ujrameres`) — a főszál tölti ki: PR-link, CI-állapot, `allapot: lezarva`

**Elkészült:** versszintű BSB→MT megfeleltetés mind a 39 ÓSZ-könyvre (`naplok/F41_bsb_megfeleltetes.tsv`); nem egyező versek okkategóriával (`F41_nem_egyezo_versek.tsv`); újramérés és import: **36 ELÉRI, 3 NEM_ÉRI_EL** (2Sám 94,96; Ezsd 94,64; Dán 89,64: oka nem a számozás), 278 125 sor (volt 242 597). Új: 1Sám 96,91; Préd 96,85; Ézs 98,07; Hós 96,95; Jón 100,00.

**F41.10 (DT-F41f):** a 4Móz 12/13 átszámozása visszavonva (WLC: KJV = MT; az első 5 oszlopon bájtazonos a mainnel); a 4Móz 29/30 átszámozása marad. A `Számozás` (7. oszlop): `mt` / `kjv` / `ellenorizetlen`, versszintű WLC-összevetésből; a `tahot_szamozas` / `kjv_szamozas` megszűnt.

**F41.12 (DT-F41g; a harmadik független ellenőrzés 4 eltérése, `naplok/ELLENOR_F41_3.md`):** a kritérium szigorítva (`wlc_versek.vers_igazolt`): `mt`, ha a WLC-vers átfedése > 0,5, szigorúan jobb a WLC-környezet (fejezet + a szomszéd fejezetek 20 szélső verse) és a BSB-környezet bármely másik versénél, nem hibrid részvers, és a szomszéd vers is illeszkedik; döntetlen → `ellenorizetlen`. **Eredmény: `mt` 260 243 sor (20 180 vers), `kjv` 240 (37 vers: Jób 40 3, Jób 41 34), `ellenorizetlen` 17 642 (1 474 vers, 270 fejezet)** — az `ellenorizetlen` nem állítja, hogy a szám hibás. A 20 téves `mt` vers és a hibrid részversek (4Móz 26:1, 1Sám 20:42, 1Krón 12:4) mind `ellenorizetlen`; a kontroll fejezetek (Hós 12, Jón 2, Ézs 8:23, 1Sám 24, 1Kir 22:43/44, 4Móz 12/13/30:1) `mt`, a 4Móz 29:1 `ellenorizetlen` (döntetlen a 28:25-tel).

**BSB_Strongs.tsv 7 oszlopos:** 6. `Angol szó állapota` (forditva 247 173 / elhagyva 30 952 / ures_jelzo_nelkul 0; érintetlen).

**Nulla-diff** (`bsb_nulladiff.py` → `F41_nulladiff.txt`): 29 könyv mind az 5 oszlopon bájtazonos a mainnel, 2 változott (4Móz 29/30, 1Kir 22; sorszám és Strong+szó sorozat azonos), 5 új; hibák 0.

**WLC-ellenőrzés** (`bsb_wlc_versszam_ellenorzes.py` → `F41_wlc_versszam_ellenorzes.tsv`, 930 fejezet): fejezetek `mt` 610, `reszben_mt` 243, `nem_igazolt` 29, `nincs_bsb_sor` 48. Két ellenőrzés: (1) konzisztencia (NEM független: ugyanaz a `vers_igazolt` a fájlból, 0 eltérés), (2) független (saját Macula-olvasás, Jaccard: mind a 20 180 `mt` vers WLC-azonos-számú verse az egyetlen legjobb egyezés, 0 hiba).

**Dokumentumok:** `datasetek.tsv`, `konkordancia/README.md`, `adat/SEMA.md` igazítva; `DONTESEK.md`: DT-F41a 🟡, DT-F41b–f ✅, új DT-F41g ✅ (az ABLAK = 20 és a részvers-küszöb implementációs paraméter, megerősítést kér); `NYITOTT_FELADATOK.md`: N-F41b/d/g/h igazítva.

**A főszálra marad:** `FELADATOK.md`, DT6 ✅, `fuggetlen-ellenor` az F41.12 diffre, a PR frissítése, `allapot: lezarva`.
