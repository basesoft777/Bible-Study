---
feladat: 229
cim: „Csak szövegek” mód a két Károli-csomag exportálójában (N-F223b)
kod: CSAK_SZOVEGEK_KAROLI
tipus: feladat
fazis: folyamat
modell: sonnet
sav: SYSTEMS
allapot: nem_indult
ad: a Károli–Strong és a Károli-modern exportáló `--csak-szovegek` módja, ha a mérés szerint megéri; az adatfájlok bájtra változatlanok maradnak
kovetkezo: "Te: `/kovetkezo`, a #223 lezárása után (ütköznek: nyilt_mag_export.py, a két Károli-exportteszt)"
munka: folyamat
olvas: [eszkozok/karoli_strong_export.py, eszkozok/karoli_modern_export.py, eszkozok/nyilt_mag_export.py, eszkozok/teszt_karoli_strong_export.py, eszkozok/teszt_karoli_modern_export.py, F223_RESZLEGES_KAPU_BRIEF.md]
ir: [eszkozok/karoli_strong_export.py, eszkozok/karoli_modern_export.py, eszkozok/teszt_karoli_strong_export.py, eszkozok/teszt_karoli_modern_export.py]
fugg: []
---

# F229_CSAK_SZOVEGEK_KAROLI_BRIEF.md — „Csak szövegek” mód a Károli-csomagokra

*FELADATOK #229 · Modell: sonnet · v1 · 2026.11.18 · forrás: N-F223b (NYITOTT_FELADATOK.md)*

<!-- KOZVETLEN_FUTTATAS -->
Hajtsd végre ezt a briefet a `/kovetkezo` szerint; a ⛔ pontokon állj meg.
<!-- /KOZVETLEN_FUTTATAS -->

**Előzetes felmérés (2026-11-18).** A `--csak-szovegek` mód a **nyílt magra már kész** (F223 (a): `nyilt_mag_export.py` `export_csak_szovegek`, `SZOVEG_RELEK`/`OSSZEG_RELEK`; 15 mp → 0,6 mp, a teljes exporttal bájtra azonos, teszttel). **Hiányzik** a két Károli-csomag: a `karoli_strong_export.py` és a `karoli_modern_export.py` `main()`-jének nincs ilyen kapcsolója; a teljes futásuk 20, ill. 21 mp. Az N-F223b szerint a nyereség kicsi, és a szövegek számai a mérésből jönnek (`f172/`, nem-tr tábla, igealak-tokenek, git-napló dátuma), ezért a commitolt csomagból való visszaépítés kockázatos. Indításkor ezt újra ellenőrizd.

**Kizárás.** A Károli–Strong **1.1-re való átállás** külön nyitott tétel (#762): ez a brief **nem érinti az adatot, a kapukat és a csomag tartalmát**; ha a mód megvalósításához ilyen változtatás kellene, ⛔ megállás.

1. **Mérés előbb:** futtasd mindkét exportálót a mostani teljes móddal egy ideiglenes `--kimenet` könyvtárba (a repón kívül), és mérd: melyik rész adja a 20–21 mp-et, és a szövegfájlok mekkora része épül újra az adatfájloktól függetlenül. A mérés a naplóba kerül. ⛔ **Megállás és kérdés a felhasználónak**, ha a „csak szövegek” mód nyeresége 5 mp alatt marad, vagy a szöveg számai nem állíthatók elő a commitolt csomagból és a repó adataiból a mérés újrafuttatása nélkül: ilyenkor az eredmény az N-F223b lezárása „nem éri meg” indoklással (döntés a felhasználóé), kód nincs.
2. **Ha megéri:** a nyílt mag mintájára (`export_csak_szovegek`): a szövegrész külön függvény; az adatfájlokat a commitolt csomagból olvassa, nem generálja újra és nem írja; az ellenőrzőösszeg-fájl (`ELLENORZO_OSSZEG.sha256`, kiadás-fájlok) a szövegfájlok sorait újraszámolja, az adatfájlokét a commitolt csomagból veszi.
3. **Fájlonkénti összevetés (E35):** a mód után az adatfájl **bájtra változatlan** (hash-összevetés a módosítás előtti állapottal), a szövegfájlok a teljes exporttal egyeznek.
4. **Teszt** mindkét exportálóhoz (`teszt_karoli_strong_export.py`, `teszt_karoli_modern_export.py`): a „csak szövegek” és a teljes export kimenete bájtra azonos; az adatfájl nem íródik újra (mtime/hash).
5. A `nyilt_mag_export.py`-hoz csak olvasóként nyúlsz (minta); az `ir`-ben nincs.

**Kész, ha:** a mérés a naplóban; vagy (a) mindkét mód kész, tesztelt, a csomag bájtra változatlan, vagy (b) a felhasználó döntése az N-F223b lezárásáról. Az `adat/`, `nyilt_mag/` és a commitolt csomagok nem változnak.
