# ELLENOR_F41_3 — a harmadik független ellenőrzés (F41.10–F41.11 diff), kivonat

*Forrás: a `fuggetlen-ellenor` jelentésének kivonata, az orkesztrátor átadásából (a teljes szöveg nem került a repóba). Az alábbi pontok állítások, nem saját lekérdezésem; a javítás utáni számok: `naplok/F41_wlc_versszam_ellenorzes.tsv`.*

**4 eltérés:**

1. **Kritérium.** A `wlc_versek.vers_egyezik` (> 0,5 Strong-halmaz-átfedés) formulás szomszéd versekkel is teljesül: 20 vers / 281 sor kapott téves `mt` címkét KJV-számozású fejezetekben (1Móz 32:28; 2Móz 8:15; 3Móz 6:1; 4Móz 17:1/8/9; 5Móz 23:3/20; 1Sám 21:5; 2Kir 12:1/7/15; 1Krón 6:1/22; Neh 7:70/71, 10:31; Ez 21:1/2; Zak 2:1). A korábban helyes `mt` fejezetek (Hós 12:1, Jón 2:1, Ézs 8:23, 1Sám 24:1, 1Kir 22:43/44, 4Móz 12/13, 29/30) maradjanak `mt`.
2. **Hibrid részversek:** 4Móz 26:1 (13 sor), 1Sám 20:42 (27 sor), valószínűleg 1Krón 12:4: a BSB-vers ⊋ WLC-vers esetek `mt` címkét kaptak.
3. **A „független újraszámolás” túlzó:** a WLC-szkript ugyanazt a kritériumot használta, mint az import (fájlolvasás-ellenőrzés, nem független kódút).
4. **Dokumentáció:** az N-F41b, N-F41d szövege a megszűnt `tahot_szamozas` / `kjv_szamozas` értékeket említi; a README/SEMA/datasetek „igazolt MT-szám” megfogalmazása és a számok igazításra szorulnak; a DT-F41f ne állítson többet, mint az adat.

**Javítás (F41.12):** `wlc_versek.vers_igazolt` (környezet-egyértelműség a WLC- és BSB-oldalon, részvers-szűrő, szomszéd-egyezés); a WLC-szkript konzisztencia-ellenőrzésre nevezve át (nem független) + valóban független Jaccard-ellenőrzés (saját Macula-olvasás); DT-F41g (a DT-F41f pontosítása), N-F41b/d/g/h, README/SEMA/datasetek igazítva.
