# F41 zárójelentés (FELADATOK #41; ág: `claude/f41-bsb-ujrameres`) — a főszál tölti ki: PR-link, CI-állapot, `allapot: lezarva`

**Elkészült:** versszintű BSB→MT megfeleltetés mind a 39 ÓSZ-könyvre (`naplok/F41_bsb_megfeleltetes.tsv`: + `tahot_vers`, `szamozas`); nem egyező versek okkategóriával (`F41_nem_egyezo_versek.tsv`); újramérés és import: **36 ELÉRI, 3 NEM_ÉRI_EL** (2Sám 94,96; Ezsd 94,64; Dán 89,64: oka nem a számozás), 278 125 sor (volt 242 597). Új: 1Sám 96,91; Préd 96,85; Ézs 98,07; Hós 96,95; Jón 100,00 (mind ≥ a diagnózis értéke).

**F41.7 (felhasználói döntés: DT-F41c (a), DT-F41b lezárva — célszámozás MT/WLC, D3: nem igazolható → KJV + jelölés):** a Jób 38–41 vissza a main KJV-számozására (a main-nel az első 5 oszlopon bájtazonos, a d42b729 Jób-logikája kivéve); a Préd 11/12 és Ézs 2/3 átszámozása visszavonva: a WLC fejezet-max szerint KJV = MT (Préd 10/14, Ézs 22/26), a TAHOT_kivonat Károli-szerű (8/16, 21/27) — `naplok/F41_wlc_hatar_ellenorzes.tsv`, **a feltevés igazolódott**. Marad: 4Móz, 1Sám, Hós, Jón átszámozás, 1Kir 22:43 osztás.

**BSB_Strongs.tsv 7 oszlopos:** 6. `Angol szó állapota` (forditva 247 173 / elhagyva 30 952 / ures_jelzo_nelkul 0), 7. `Számozás` (tahot_szamozas 276 417 / kjv_szamozas 1 708 sor = Jób 38–41: 890, Préd 11/12: 326, Ézs 2/3: 492); az olvasók ellenőrizve (oszlopsorszámmal senki). A lefedettségi napló `kjv_szamozasu_fejezetek`: Jób 38–41, Préd 11 12, Ézs 2 3.

**Nulla-diff** (commitolt `eszkozok/fj2/bsb_nulladiff.py`): 29 könyv mind az 5 oszlopon bájtazonos a main-nel (a Jób is), 2 változott (4Móz 12/13/29/30, 1Kir 22; sorszám és Strong+szó sorozat azonos), 5 új; a fejléc és a könyvsorrend igazolt.

**WLC-ellenőrzés** (`eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py` → `F41_wlc_versszam_ellenorzes.tsv`, 930 fejezet): wlc_egyezik 829, **wlc_elter 45** (a TAHOT_kivonat hibrid számozása: 22 könyv, l. N-F41h), kjv_jelolt 8 (ebből a Jób 41 nem WLC-egyező), nincs_bsb_sor 48 (2Sám, Ezsd, Dán, Zsolt 13, Jóel 4: a WLC-ben van, a BSB-ben nincs). Az egyezés-eloszlás kétcsúcsú (28+2+1 fejezet 30% alatt, 851 fejezet 90% felett), a 90%-os határ nem vág el valós fejezetet.

**⚠ A felhasználó tudomására:** a **4Móz 12/13 átszámozása a WLC szerint nem MT** (WLC: 12:16, 13:33 = KJV; a TAHOT_kivonat Károli-szerű), a döntés szerint mégis marad; a 4Móz 13 `wlc_elter`. A 4Móz 29/30, 1Sám 23/24, 1Kir 22, Ézs 9, Hós 11/12, Jón 1/2 átszámozása WLC-egyező.

**Dokumentumok (N-F41e, elvégezve):** `datasetek.tsv`, `konkordancia/README.md`, `adat/SEMA.md`, `szotar_szerepek.tsv` (36 könyv, 278 125 sor, 7 oszlop). `DONTESEK.md`: DT-F41a (opció szó szerint a DT6-ból), DT-F41b ✅ lezárva, DT-F41c ✅, DT-F41d (D3) ✅, DT-F41e (1Kir 22:43) ✅; ellenőri 5. (hatókör: szűrt = importált + nem importált, gépi ellenőrzés + napló-fejléc) és 6. eltérés javítva. Új N-tételek: N-F41g (Jób MT-re, gépi táblából), N-F41h (45 `wlc_elter` fejezet).

**A főszálra marad:** `FELADATOK.md`, DT6 ✅ (a zárócommit), `fuggetlen-ellenor` az F41.7–F41.9 diffre, a draft PR frissítése; a `DT-F41a` (Zsolt 13) 🟡 változatlan.
