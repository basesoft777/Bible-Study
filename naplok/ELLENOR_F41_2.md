# ELLENOR_F41_2 — origin/main..claude/f41-bsb-ujrameres (3897b30), újraellenőrzés külön checkouttal

*A `fuggetlen-ellenor` jelentése, rövidítve; a főszál mentette. Az előző jelentés 1–4. és 5. eltérése javítva (Jób 38–41 / Préd / Ézs `kjv_szamozas` 1708 sor, DONTESEK DT-F41c/d/e rögzítve, commitolt nulladiff-szkript).*

**ELTÉRÉS: 5 tétel**
1. **Magas — 4Móz 12/13.** A main MT-helyes sorait (12:16, 13:1–33; WLC = KJV) az F41 Károli-számozásra tolta. Ez ugyanaz, mint a visszavont Préd/Ézs eset; itt megmaradt, a DT-F41d „alkalmazva”, felhasználói döntés a WLC-lelet után nincs. **Döntést kíván.**
2. **Közepes — hibrid számozás csak a naplóban kiszűrt.** 45 fejezet (22 könyv, 15 904 sor) KJV-számozású, mégis `tahot_szamozas` címkét visel; a DT-F41b szerint jelölendő lenne (N-F41h-ra halasztva). A `bsb_wlc_versszam_ellenorzes.py` a BSB ⊆ WLC részfejezeteket (4Móz 12, 25/26) `wlc_egyezik`-nek sorolja; a „szűri a hibrid számozást” állítás ennyiben túlzó. A README:304 ezzel ellentmond.
3. **Közepes — CI.** Az ág lemaradt a main mögött (F44–F46); a kétpontos diffen E5 HIBA 20, a merge-base-en EXIT=0. A main behúzása kell (`sync_with_base_branch`).
4. **Alacsony — elavult NYITOTT-szöveg** (N-F41e, N-F41g: Jób sorai `kjv_szamozas`).
5. **Alacsony — DT-F41a** kérdésszövege nem szó szerint a DT6-ból.

**OK:** G1–G5, D1, D2, D4, D6, A1, A6, K1, K2, K4; `Számozás` 7. oszlop olvasói; darabszámok (278 125 sor; 247 173 forditva / 30 952 elhagyva); DT-F41b/c/e.
**Nem ellenőrizhető:** a nulladiff újrafuttatása, a CI-jelentés egyezése, DT6 ✅.
