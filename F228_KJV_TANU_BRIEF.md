---
feladat: 228
cim: KJV mint harmadik tanú a Károli–Strong párosításhoz — csak a jelöltlista (N211)
kod: KJV_TANU
tipus: feladat
fazis: folyamat
modell: sonnet
sav: SYSTEMS
allapot: nem_indult
ad: modellhívás nélküli szkript és jelöltlista könyvcsoportonként (döntés nélkül), arányokkal a 7 könyvcsoportra; az 1.2 alapanyaga
kovetkezo: "Te: `/kovetkezo`"
munka: adat
olvas: [konkordancia/KJV_Strongs_teljes.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, adat/karoli_strong/, eszkozok/karoli_strong/forras_kjv_ellenorzes.py, eszkozok/karoli_strong/kjv_osszevet.py, eszkozok/karoli_strong/meres_kjv.py, adat/grammatikai_strongok.tsv]
ir: [eszkozok/karoli_strong/kjv_tanu_jeloltek.py, eszkozok/karoli_strong/teszt_kjv_tanu_jeloltek.py]
fugg: []
---

# F228_KJV_TANU_BRIEF.md — KJV mint harmadik tanú (jelöltlista)

*FELADATOK #228 · Modell: sonnet · v1 · 2026.11.18 · forrás: NYITOTT_FELADATOK.md N211*

<!-- KOZVETLEN_FUTTATAS -->
Hajtsd végre ezt a briefet a `/kovetkezo` szerint; a ⛔ pontokon állj meg.
<!-- /KOZVETLEN_FUTTATAS -->

**Hatókör.** Az N211 első fele: csak a jelöltlista. **Adatot nem módosít** (`adat/karoli_strong/` és a nyílt csomagok érintetlenek); a lista az 1.2-es osztályszintű újrapárosítás alapanyaga, a javítás döntése későbbi tétel. A KJV a promptban nem igazolt (F21), ezért itt csak ellenőrző tanú. Az eszközök az 1.1-es átállástól és a #762/#763 fájljaitól (`karoli_strong_validacio*`, `kozlemeny/data_paper/`, `adat/karoli_strong_11/`) függetlenek, azokhoz nem nyúlunk.

1. **Szkript** `eszkozok/karoli_strong/kjv_tanu_jeloltek.py` (modellhívás nincs, determinisztikus). Versenként: a mi párjaink Strong-halmaza (`adat/karoli_strong/`, az 1.0) és a KJV-vers Strong-címkéinek halmaza (`konkordancia/KJV_Strongs_teljes.tsv`; a versek összerendelése a `Karoli_versmegfeleltetes.tsv` KJV-oszlopa szerint). A Strong-alakot normalizáld (a `grammatikai_strongok.tsv` nyelvtani címkéit a (2) jelölt-osztályból zárd ki; a két forrás Strong-jelölése eltérhet: ezt mérd és rögzítsd, ne feltételezd).
2. **Két jelölt-osztály:** (1) a pár, amelynek Strong-száma a KJV-versben **nincs**; (2) a KJV-címkézett, **nem nyelvtani** Strong, amelyhez nálunk **nincs** magyar pár.
3. **Kimenet** (a repón kívülre, a `--kimenet` mappába; a repóba legfeljebb egy rövid `naplok/F228_naplo.md` kerül számokkal): jelöltlista könyvcsoportonként, **döntés nélkül** (jeloltek-elv: nincs automatikus javítás); az arány a **7 könyvcsoportra** (a csoportbontás a repó meglévő könyvcsoport-táblájából/`f172/` mérésből, ne találd ki; ha nincs, ⛔).
4. **ÚSZ külön.** A `Karoli_versmegfeleltetes.tsv` ma csak az ÓSZ 39 könyvét fedi, a KJV-tábla mind a 66-ot. Az ÚSZ-höz egyszerű Károli↔KJV versmegfeleltetés kell: alapeset azonos vers + kivétellista (pl. Róm 16 vége, 2Kor 13 vége, 3Jn vége), a táblát versszintű egyezéssel ellenőrizve. Az ÚSZ-ben a KJV erős tanú (mindkét fordítás a Textus Receptusra épül; a felhasználó, 2026-11-16). Az ÚSZ-jelöltek külön szakaszban, ÓSZ-arányoktól elkülönítve.
5. **Újrahasznosítás:** a `forras_kjv_ellenorzes.py`, `kjv_osszevet.py`, `meres_kjv.py` kódját használd, ahol illik (importtal vagy mintaként); ne duplikáld, és ne módosítsd őket (nincsenek az `ir`-ben).
6. **Teszt:** `teszt_kjv_tanu_jeloltek.py` kis, kézzel ellenőrzött mintán (egy-két vers mindkét osztályra, egy kivétel a versmegfeleltetésben).

**Licenc (rögzített).** A KJV-adat licence (GPL-kérdés) miatt a jelöltlista **belső**, nyílt csomagba, `nyilt_mag/`-ba, közleménybe nem kerül; a briefben és a naplóban ez szerepel. ⛔ Megállás, ha a kimenet bármelyik nyílt/kiadott útvonalra kerülne.

**Kész, ha:** a szkript futott a teljes ÓSZ-ön és az ÚSZ-ön; a számok (jelöltek száma osztályonként, könyvcsoportonként; arány) a naplóban; a teszt zöld; adat nem változott (`git status` az `adat/` alatt üres).
