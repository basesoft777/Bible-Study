---
feladat: 227
cim: DESIGN sáv a brief-fejlécben és a heti beosztásban
kod: DESIGN_SAV
tipus: feladat
fazis: folyamat
modell: sonnet
sav: SYSTEMS
allapot: lezarva
ag: claude/f227-design-sav
ad: a `DESIGN` sáv-érték a brief-fejlécben, az `ellenoriz` kapujában, a SEMA-ban és a heti beosztásban; a FELADATOK.md sávonként csoportosít
kovetkezo: "—"
munka: folyamat
olvas: [BRIEF_SABLON.md, adat/SEMA.md, eszkozok/feladatok.py, eszkozok/heti_beosztas.py, eszkozok/teszt_feladatok.py]
ir: [BRIEF_SABLON.md, adat/SEMA.md, eszkozok/feladatok.py, eszkozok/heti_beosztas.py, eszkozok/teszt_feladatok.py, eszkozok/tesztek/test_heti_beosztas.py, eszkozok/keret_meres.py, eszkozok/tesztek/test_keret_meres.py]
fugg: []
nem_fugg: [123, 156, 220]
---

# F227_DESIGN_SAV_BRIEF.md — DESIGN sáv

*FELADATOK #227 · Modell: sonnet · v1 · 2026.11.18*

<!-- KOZVETLEN_FUTTATAS -->
Hajtsd végre ezt a briefet a `/kovetkezo` szerint; a ⛔ pontokon állj meg.
<!-- /KOZVETLEN_FUTTATAS -->

**Előzetes felmérés (2026-11-18, a main-en).** A `sav` mező már **létezik**: a `feladatok.py` `SAVOK = ('SYSTEMS','CONTENT','SERVER','USER','BUSINESS')`, az `ellenoriz` kötelezővé teszi és értékellenőrzést végez (`feladatok.py` ~443–447), a FELADATOK.md generált blokkja sávonként csoportosít (`feladatok.py` ~1061), a `BRIEF_SABLON.md` leírja. **Hiányzik** a `DESIGN` érték. A brief csak ezt írja elő; a mező és a csoportosítás újraírása nem feladat. Indításkor a felmérést újra le kell futtatni (az ágak közben változhattak), és csak a tényleges hiányt pótolni.

**Teendő** (a `DESIGN` = az olvasó-szerver kinézete és arculata: CSS, arculat-konfig, vászon/mockup, design-system; a felhasználó, 2026-11-18):
1. `eszkozok/feladatok.py`: `SAVOK` bővítése `DESIGN`-nal; a hibaüzenet az új listát írja; a sávonkénti csoportosítás a sorrendben a `DESIGN`-t is adja.
2. `BRIEF_SABLON.md`: a `sav` sor értékkészlete és a `DESIGN` meghatározása (egy mondat; „kétes esetben a fő termék szerint” marad).
3. `adat/SEMA.md`: a sáv értékkészlete **mind a három helyen** (a `heti_terv`, a `heti_keret`/`heti_otlet` és a mérési tábla `sav` oszlopainak szabálya; a pontos sorokat keresd meg a `grep -n "SYSTEMS"` kimenetével, ne találgass).
4. `eszkozok/heti_beosztas.py`: `SAV_SORREND`, `SAV_CIMKE` (`'DESIGN': 'Design'`), `OTLET_SAVOK`; a `KERET_SAVOK` a `SAV_SORREND`-ből jön. Ha a heti-áttekintő vagy a `keret_meres.py` külön sávlistát tart, azt csak jelentsd (nincs az `ir`-ben).
5. Kapu a sáv-értékre: teszt a `teszt_feladatok.py`-ban (`DESIGN` elfogadott, ismeretlen érték elutasított, a csoportosítás a `DESIGN`-t megjeleníti), és a `heti_beosztas` érvényességi ellenőrzése fogadja el az új értéket.

⛔ **Megállás**, ha a `SEMA.md` sávszabálya egy generált nézettel vagy kapuval (`eszkozok/ellenorzes/`) ellentmond, vagy ha a `/kovetkezo` ütközést jelez a #220/#123-mal.

**Kész, ha:** `python eszkozok/feladatok.py ellenoriz` 0 hiba; a `teszt_feladatok.py` és a `heti_beosztas` tesztjei zöldek; a FELADATOK.md generált blokkját nem kézzel írtad.

## Zárás (orkesztrátor, 2026-11-18)
Az 1. ellenőrzés három ELTÉRÉSE a javítókörben (F227.3–F227.6) rendezve; célzott újraellenőrzés a diffen: `keret_meres.SAVOK`/`CIM_SAV` DESIGN + teszt (`test_design_sav_osszesitese_nem_dob_hibat`), címke `Design`, az `ir` lista kiegészítve. Új teljes ellenőri kör nincs (1 ellenőrzés + 1 javítókör). A #123-mal szembeni KIZAR/SORREND átlépése a felhasználó döntése (2026-11-18); a #123 nem futott.
