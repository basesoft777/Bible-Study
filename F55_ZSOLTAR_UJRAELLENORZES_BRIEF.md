---
feladat: 55
cim: A régi, egy verssel eltolt zsoltár-kivonatra épülő állítások újraellenőrzése
kod: ZSOLTAR_UJRAELLENORZES
tipus: feladat
fazis: 1
modell: opus
munka: ertelmezo
allapot: brief_kell
ad: minden állítás, amely a régi LXX_kivonat eltolt zsoltárverseire épült, újraellenőrizve a helyes vers LXX_OS-szövegével; ítélet soronként (megáll / módosul / visszavonandó), indoklással
kovetkezo: brief kell (a /befogad csonk-kitöltése)
fugg: [42]
olvas: ["konkordancia/LXX_OS/*.tsv", naplok/FORRASKIVEZETES_M5_M7.md]
ir: [adat/auditok.tsv, naplok/T1_TEREMT002_auditok_munkalap.tsv, tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md, tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md]
---

# F55_ZSOLTAR_UJRAELLENORZES_BRIEF — csonk

*FELADATOK #55 · csonk-brief (F20 B3): nem végrehajtható, csak a feladat fejlécét hordozza. Forrás: a #42 (FORRASKIVEZETES, PR #176) nyitott tétele, `naplok/FORRASKIVEZETES_M5_M7.md` (f3).*

- **Mit ad, ha kész:** az érintett helyek ítélete — `adat/auditok.tsv` TEREMT-002 B4 sorai (Zsolt 107:40, 104:30, 33:6, 80:6, 80:7) és másolatuk a `naplok/T1_TEREMT002_auditok_munkalap.tsv`-ben; `tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md` (Zsolt 14:1, 53:1); `tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` (92. sor); `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` (370. sor, pilot-példány: csak jelölés).
- **Következő lépés:** a brief megírása.

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
