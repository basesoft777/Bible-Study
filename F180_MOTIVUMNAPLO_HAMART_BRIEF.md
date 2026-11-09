---
feladat: 180
cim: A motívumnapló kézi HAMART-001-szakaszainak igazítása a határkörhöz (DT-F123hc, DT-F123hd)
kod: MOTIVUMNAPLO_HAMART
tipus: feladat
fazis: folyamat
modell: opus
allapot: lezarva
ag: claude/motivumnaplo-hamart
ad: a `motivumlog/PaRDeS_motivumok.md` kézi HAMART-001-szakaszai az `elofordulasok.tsv` mai soraihoz igazítva; a határkörben kikerült helyek mellett jelzés (nem törlés), a Gal 3:13-14 tárgyszerűen, kiemelés nélkül; a generált blokkok változatlanok, a CI (E28) zöld
kovetkezo: "lezárva (PR #662, 2026-11-09; [elteres_kor 1/2], ELLENOR_F180_2 TISZTA); a merge a felhasználóé"
pr: https://github.com/basesoft777/Bible-Study/pull/662
lezarva_osszegzes: a motívumnapló kézi HAMART-001-szakaszai és a kézi könyv-index a 48 soros előfordulás-állapothoz igazítva; 13 kikerült hely jelölve, nem törölve (DT-F123hc/hd), az 5Móz 21:23 nem önálló előfordulásként jelölve; a Gal 3:13-14 tárgyszerű, az indexben →1Móz 12:3 (DT-F123he); generált blokk változatlan, E28 0; egyeztetett eltérés: a #123 fejléce elavult, az orkesztrátor megerősítésével indult (`naplok/F180_zaras.md`)
munka: ertelmezo
olvas: [motivumlog/PaRDeS_motivumok.md, adat/elofordulasok.tsv, DONTESEK.md, naplok/ELLENOR_F123_HAMART3_javitokor2.md]
ir: [motivumlog/PaRDeS_motivumok.md]
fugg: [123]
---

# Brief-tervezet: a motívumnapló kézi HAMART-001-leletei

*Tervezet a `/befogad`-hoz. Forrása: `naplok/ELLENOR_F123_HAMART3_javitokor2.md` 4. tétele (#639, a független ellenőr, 2026-11-08). A tervezet adat, nem befogadott brief.*

**Lelet.** A `motivumlog/PaRDeS_motivumok.md` kézi szakaszai (kb. a 476–581. sor) még a határkör előtti állapotot hordozzák. HAMART-001-leletként áll bennük a Gal 3:10, a Jer 17:5, a Jón 3:8, a Hab 2:8 és 2:17 és az 5Móz 27:15-26. A Gal 3:13-nál a „Krisztus κατάρα-vá lesz … magára veszi” kiemelés is megmaradt. A szöveg régebbi a #639-nél (`git log -S` → 8f3e869c), a kör nem nyúlt hozzá, mert nincs az `ir`-ben.

**Teendő.**
1. A HAMART-001 kézi leleteinek összevetése az `adat/elofordulasok.tsv` mai 48 sorával. A kikerült helyek (DT-F123hc: 11 hely és a két szűkítés; DT-F123hd: Gal 3:10) mellé rövid jelzés kerül, hogy a határkörben kikerültek, a döntés helyőrzőjével vagy végleges számával. Ez nem törlés: a napló a kutatás története.
2. A Gal 3:13-14 szövege tárgyszerű legyen, kiemelés nélkül (a felhasználó: „így már látszik, hogy ezt nagyon ki akartuk domborítani”).
3. A generált blokkokhoz nem nyúl (`general.py --cel naplo`).

**Kész.** Egyik kézi szakasz sem nevez meg beépített leletként olyan helyet, amely ma nincs az előfordulások között. A generált blokkok változatlanok, a CI (E28) zöld.
