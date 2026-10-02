# F41 zárójelentés (FELADATOK #41; ág: `claude/f41-bsb-ujrameres`) — a főszál tölti ki: PR-link, CI-állapot, `allapot: lezarva`

**Elkészült:** versszintű BSB→MT megfeleltetés mind a 39 ÓSZ-könyvre (`naplok/F41_bsb_megfeleltetes.tsv`); nem egyező versek okkategóriával (`F41_nem_egyezo_versek.tsv`); újramérés és import: **36 ELÉRI, 3 NEM_ÉRI_EL** (2Sám 94,96; Ezsd 94,64; Dán 89,64: oka nem a számozás), 278 125 sor (volt 242 597). Új: 1Sám 96,91; Préd 96,85; Ézs 98,07; Hós 96,95; Jón 100,00 (mind ≥ a diagnózis értéke).

**F41.10 (felhasználói döntés, DT-F41f):** (1) a **4Móz 12/13 átszámozása visszavonva** (WLC: 12:16, 13:33 = KJV = MT); az első 5 oszlopon bájtazonos a mainnel. A 4Móz 29/30 a WLC-vel összevetve KJV ≠ MT (WLC 39/17, KJV 40/16), az átszámozás marad; az 1Sám 23/24, Hós 11/12, Jón 1/2, 1Kir 22, Ézs 9 minden verse versszinten `mt`: további visszavonás nincs. A Préd 11/12, Ézs 2/3 korábban vonódott vissza (DT-F41c). (2) A **`Számozás` (7. oszlop) értékei `mt` / `kjv` / `ellenorizetlen`**, versszintű WLC-összevetésből (`wlc_versek.vers_egyezik`: a WLC-vers Strong-halmazának több mint fele az Igehely-vers soraiban): **mt 268 482 sor** (20 937 vers), **kjv 223** (Jób 41, 34 vers), **ellenorizetlen 9 420** (720 vers, 46 fejezet). A `tahot_szamozas` / `kjv_szamozas` megszűnt.

**BSB_Strongs.tsv 7 oszlopos:** 6. `Angol szó állapota` (forditva 247 173 / elhagyva 30 952 / ures_jelzo_nelkul 0; érintetlen); olvasók ellenőrizve (oszlopsorszámmal senki). A lefedettségi napló `kjv_szamozasu_fejezetek`: Jób 41.

**Nulla-diff** (`eszkozok/fj2/bsb_nulladiff.py` → `F41_nulladiff.txt`): 29 könyv mind az 5 oszlopon bájtazonos a mainnel (a Jób is), 2 változott (4Móz 29/30, 1Kir 22; sorszám és Strong+szó sorozat azonos; a 4Móz 12/13 sorai külön igazoltan bájtazonosak), 5 új; hibák 0. **Figyelem:** a 4Móz egésze nem bájtazonos a mainnel, mert a 29/30 átszámozása a WLC szerint helyes és marad.

**WLC-ellenőrzés** (`eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py` → `F41_wlc_versszam_ellenorzes.tsv`, 930 fejezet; versszintre javítva, a 7. oszlopot függetlenül újraszámolja, 0 eltérés): fejezetek `mt` 835, `reszben_mt` 29, `nem_igazolt` 18 (ebből Jób 41 `kjv`), `nincs_bsb_sor` 48 (2Sám, Ezsd, Dán, Zsolt 13, Jóel 4). A részfejezetes téves egyezés (BSB ⊆ WLC: 4Móz 12, 25/26) megszűnt.

**Dokumentumok:** `datasetek.tsv`, `konkordancia/README.md`, `adat/SEMA.md`, `szotar_szerepek.tsv` a valós fájlhoz igazítva. `DONTESEK.md`: DT-F41a (kérdés és opció szó szerint a DT6-ból, 🟡), DT-F41b–e ✅, új **DT-F41f ✅** (1–2. pont); DT-F41d „Alkalmazva” a 4Móz-visszavonáshoz igazítva. `NYITOTT_FELADATOK.md`: N-F41e/g/h frissítve (az N-F41h az `ellenorizetlen` sorok teljes MT-átszámozásáról szól).

**A főszálra marad:** `FELADATOK.md`, DT6 ✅ (a zárócommit), `fuggetlen-ellenor` az F41.10 diffre, a PR frissítése, `allapot: lezarva`; a `DT-F41a` (Zsolt 13) 🟡 változatlan.
