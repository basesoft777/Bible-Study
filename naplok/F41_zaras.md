# F41 zárójelentés-tervezet (FELADATOK #41; ág: `claude/f41-bsb-ujrameres`) — a főszál tölti ki: PR-link, CI-állapot, `allapot: lezarva`

**Elkészült:** versszintű BSB→TAHOT_kivonat megfeleltetés mind a 39 ÓSZ-könyvre (`naplok/F41_bsb_megfeleltetes.tsv`, Strong-illeszkedés, fejezetenkénti igazolás); a nem egyező versek okkategóriával (`naplok/F41_nem_egyezo_versek.tsv`); újramérés és újraimport (`eszkozok/fj2/bsb_import.py`): **36 ELÉRI, 3 NEM_ÉRI_EL**, 278 125 sor (volt 242 597); a `BSB_Strongs.tsv` 6. oszlopa `Angol szó állapota` (forditva 247 173 / elhagyva 30 952 / ures_jelzo_nelkul 0, gépi visszaolvasás-ellenőrzés a szkript végén).

**Újonnan importált (küszöb 95%, változatlan):** 1Sám 96,91; Préd 96,85; Ézs 98,07; Hós 96,95; Jón 100,00 (mind ≥ a diagnózis értéke). **Marad küszöb alatt:** 2Sám 94,96; Ezsd 94,64; Dán 89,64.

**A három könyv oka (számok: `F41_nem_egyezo_versek.tsv` fejléce):** nem számozás. 2Sám: 35 szétszórt, egyedi Strong-eltérés (3 cimkezes, 32 egyeb). Ezsd: 15 eltérésből 7 arámi (ebből 4 a H1247/H1123 pár), 1 címkézés, 7 egyéb héber szakaszban. Dán: 37-ből csak 10 arámi, 25 címkézés (22 a Dániel-név H1840/H1841, héber fejezetekben), 2 egyéb: az „arámi címkézés” feltevés a fő okra cáfolva, az Ezsd-re részben igazolt. A 2Sám 18:33/19:1 és Dán 3/4, 5:31/6:1 számozási feltevés a TAHOT_kivonat számozásán nem eltérés.

**D3 (jóváhagyott):** átszámozva 4Móz 12/13, 29/30; 1Sám 23/24; 1Kir 22 (BSB 22:43 = MT 22:43+44, a két MT-vers uniója egyértelműen kettéosztva; 22:44–53 → 45–54); Jób 38–40 (BSB 40:1–5 = TAHOT 39:34–38); Préd, Ézs, Hós, Jón. A Jób 41 a TAHOT_kivonatban nincs → KJV-számozás marad, `kjv_szamozas` jelöléssel (Macula szerint a kért leképezés 30/34-en illeszkedik; átszámozás döntésre vár: DT-F41b). A másik 28 könyv sorai az első 5 oszlopon sorról sorra azonosak, a Lam és a Zsolt is (`naplok/F41_nulladiff.txt`).

**Lelet, fontos:** a TAHOT_kivonat versszámozása vegyes (25 könyvben tér el a Macula/WLC-től, több helyen KJV-s), ezért az „MT-számozás” valójában TAHOT_kivonat-számozás (N-F41d, DT-F41b). A brief 1Kir 4/5, Jóel 2/3, Neh 3/4 példái hibásak (0 eltolt vers); javítás a brief címsora alatt.

**Leletek kezelve:** N-F41c (Lam/JSir alias) → hangos hiba a `bsb_import.py`-ban (tesztelve), lezárva; N-F41a (KK `igehely_kjv` a Károli-hivatkozás másolata; Jón 2:1 igazolva), N-F41b (CI-javaslat), N-F41d, N-F41e (dokumentumok frissítése: README, SEMA, datasetek, a „31 könyv” szöveg), N-F41f felvéve a `NYITOTT_FELADATOK.md`-be.

**Nem érintett / a főszálra marad:** `FELADATOK.md`, DT6 ✅ (a zárócommit), `fuggetlen-ellenor` (`naplok/ELLENOR_F41.md`), draft PR; `DT-F41a` (Zsolt 13) 🟡 változatlan; új: `DT-F41b` 🟡. A 3.3 „illesztetlen fejezetek kimaradnak, jelölve”: csak a Zsolt 13. Az F16-os Zsoltár-naplók (`F16_bsb_zsolt_megfeleltetes.tsv`, `F16_zsolt_nem_egyezo_versek.tsv`) történetiek, az újrafuttatás már nem írja őket (nem az `ir`-ben vannak).
