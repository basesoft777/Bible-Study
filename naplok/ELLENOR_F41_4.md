# ELLENOR_F41_4 — origin/main..claude/f41-bsb-ujrameres (b9b1b68), külön checkouttal

*A `fuggetlen-ellenor` jelentése, rövidítve; a főszál mentette. CI: `futtat.py --teljes` kétpontos és merge-base diffen azonos, HIBA 0, exit 0; `ellenoriz.py` 0 sértés.*

**Tartalmi eredmény:** a 20 korábban téves `mt` vers és a 3 hibrid vers (4Móz 26:1, 1Sám 20:42, 1Krón 12:4) most mind `ellenorizetlen` (332 sor). Saját mintavétel: 42 `mt` vers (20 saját Strong-átfedés-számolással) és 27 `ellenorizetlen`, 0 téves; a 774 versnyi, ismert KJV≠MT tartományban 0 `mt` sor. Darabszámok a valós fájlon: `mt` 260 243 / `kjv` 240 / `ellenorizetlen` 17 642, összesen 278 125. A Jób 38–41 és a 4Móz 12/13 az első 5 oszlopon a mainnel halmaz-azonos.

**ELTÉRÉS: 5 tétel**
1. **DT-F41g** ✅ alkalmazva, de felhasználói döntés nélkül (a paraméterek: ABLAK = 20, a (d) pont 0,5 / ≥ 2 küszöbe — implementációs paraméterek, megerősítést kérnek). → a főszál a DT-F41g állapotát 🟡-ra állítja.
2. **Elavult kritérium-/jelentésszöveg:** `naplok/F41_bsb_megfeleltetes.tsv:6`, `eszkozok/fj2/bsb_import.py:64,67-69`, `naplok/F41_wlc_versszam_ellenorzes.tsv:9`, `NYITOTT_FELADATOK.md:571,579` („mt = > ½”, „ellenorizetlen = TAHOT-hibrid számozás”); az `ellenorizetlen` nagy része formulás döntetlen KJV = MT fejezetekben.
3. **`kjv` címke** a Jób 40:1/3/6-on is áll (17 sor, KJV = MT); a DT-F41c és a README:304 csak a „Jób 41”-et említi.
4. **A2:** az N-F41e (ELVÉGEZVE) és az N-F41f a nyitott szakaszban maradt.
5. **A1:** a DT-F41g „0,2-es margó → ~3000 vers” állítása mögött nincs naplózott artefaktum.

**Nem ellenőrizhető:** a „független” ellenőrző futtatása (20 180 mt vers, 0 hiba), a merge utáni szkriptfutás, a nulladiff újrafuttatása.
