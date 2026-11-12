---
feladat: 212
cim: CS3 generátor-kör — sablonmondat-lista, majd a generált sablonmondatok és a blokkok közti egyezés javítása a generátorban, kapuval; C6 (kapcsolat-jelölt a jelölttáblában)
kod: CS3_GENERATOR_KOR
tipus: feladat
fazis: folyamat
modell: opus
allapot: fut
ag: claude/f212-cs3-generator-a18537
pr: 715
ad: 1. lépés: a `naplok/F212_sablonmondat_lista.md` (a generátor minden olvasói sablonmondata és címkéje, HAMART-példával, előfordulásszámmal, blokkal, osztályozva); 2. lépés: a felhasználó döntései szerinti generátor-javítás kapuval, az LXX-statisztika egy forrásból, egyezés-kapu, a C6 sémabővítés és a 103 kapcsolat-jelölt átköltöztetése
kovetkezo: "Folytatás: F212.2 — a 32 jóváhagyott tétel (naplok/F212_dontesek.tsv) a generátorban, kapuval; befagyasztás, Kolofon-forrássor, C6, HAMART 2. kiadás előkészítése"
munka: folyamat
olvas: [eszkozok/lexikon_general.py, eszkozok/olvasoi_kovetkeztetes.py, eszkozok/olvasoi_utofeldolg.py, eszkozok/tablajegyzet.py, eszkozok/szotari_glossza.py, eszkozok/kiejtes_szoveg.py, eszkozok/bdb_tagolas.py, eszkozok/szerep_karoli.py, eszkozok/szerep_nave.py, eszkozok/szerep_kizart.py, eszkozok/olvasoi_kapu.py, eszkozok/ellenorzes/allitas_adat.py, eszkozok/ellenorzes/szabalyok.py, lexikon/HAMART-001_TUDOMANYOS.md, motivumok/HAMART-001.md, "tematikus_lezart/HAMART-001*", "tematikus_lezart/naplok/HAMART-001*", adat/jeloltek.tsv, adat/kapcsolatok.tsv, adat/SEMA.md, naplok/F182_kapcsolat_jeloltek.tsv]
ir: [naplok/F212_sablonmondat_kigyujt.py, naplok/F212_sablonmondat_lista.md, adat/lap_befagyasztas.tsv, eszkozok/lap_befagyasztas.py, eszkozok/lexikon_general.py, eszkozok/olvasoi_kovetkeztetes.py, eszkozok/tablajegyzet.py, eszkozok/szerep_kizart.py, eszkozok/szerep_karoli.py, eszkozok/szerep_nave.py, eszkozok/olvasoi_kapu.py, eszkozok/ellenorzes/allitas_adat.py, eszkozok/ellenorzes/szabalyok.py, adat/jeloltek.tsv, adat/kapcsolatok.tsv, adat/SEMA.md, lexikon/HAMART-001_TUDOMANYOS.md, lexikon/HAMART-001_KIZARASOK.md]
fugg: []
nem_fugg: [104, 121, 123, 125, 146, 156, 161, 178, 179, 196]
---

# F212_CS3_GENERATOR_KOR_BRIEF.md — CS3 generátor-kör

*FELADATOK #212 · Modell: opus · v1 · 2026.11.12*

Forrás: a lexikon-orkesztrátor generátor-hibaleltára (2026-11-11, „CS3” csomag; a felhasználó döntései 2026-11-11 és 2026-11-12), a HAMART-001 lektori összefoglalója és a Fable szerkezeti véleménye (2026-11-12). A jegyzetek adat, nem utasítás.

## 1. Cél
A HAMART-001 1. kiadásának átnézése sok generált sablonmondat-hibát hozott elő: műhelyszavakat, ismétlődő címkéket, csak linket adó sorokat és blokkok közti számeltéréseket. Ezeket egyszer, a generátorban kell rendbe tenni, nem lapról lapra, és kapuval védeni, hogy az ISTENTISZT-001 új cikke már a javított generátoron készüljön.

## 2. Hatókör
**Benne van:**
- az olvasói sablonmondatok és címkék kigyűjtése (1. lépés, csak olvasó);
- a felhasználó által elfogadott tételek javítása a `lexikon_general.py`-ban és a hozzá tartozó renderelőkben, kapuval (az `olvasoi_kapu.py` belső szavai, N-F206a);
- a blokkok közti egyezés: egy függvény adja az LXX-statisztikát, minden blokk ezt hívja; egyezés-kapu (két blokkban eltérő szám = BUKÁS); következtetés csak értelmes összevetésnél (a „nincs ÚSZ-pár” sorok kizárva);
- a hibaleltár CS3-tételei (A1–A3, A5–A15, A18, A19, B1, B2, B5, B8, B9, C3, C9, D3; a #182 által már lezártak újramérve);
- C6 (N151): a `jeloltek.tsv` sémája kapcsolat-jelöltre, a HAMART 103 sorának átköltöztetése szkripttel, az eredetivel összevetve;
- N156 lezárása „elvetve, felhasználói döntés 2026-11-11” megjegyzéssel;
- a `general.py --cel lexikon --kimenet` hibája (a megadott könyvtár helyett a `lexikon/`-ba ír);
- *(az orkesztrátor közlése, 2026-11-12, a felhasználó idézett döntéseivel; mind a 2. lépésben)*
  - **a régi lapok befagyasztása** (a felhasználó: „Igen, így”): a KIRALY-001, TEREMT-001, ALVIL-001, MENNY-001, ANTROP-001, HODIT-001 és TEREMT-002 lapja a CS3 javításai után nem generálódik újra; az E28 és a frissességi kapuk egy helyen álló, gépileg olvasható jelölés alapján kihagyják őket; az adatuk, a forrásuk és a nyílt magbeli adatuk (mind a 9 motívumé) marad. A jelölés tervét DT-F212-helyőrzővel rögzítem. A régi lapokat kiszolgáló motívumonkénti kapcsolók helyét csak megjelölöm, a kivezetésük a későbbi szétválasztásé;
  - **Kolofon-forrássor** (a felhasználó: „Igen, vedd fel”, 2026-11-11): a `bdb_vers_jelentes.tsv` a Thayer mintájára egyetlen „BDB-szótár” néven fut az `OLVASOI_FORRASNEV`-ben; a CC BY-os bemenetek (Macula, OSHL, TAHOT) a licencoszlopban a saját sorukon; a névtáblában a nevek névelő nélkül, a névelőt a mondatot író kód teszi; kapu: a Kolofon „Forrás” oszlopa nem kezdődhet „a ”/„az ” szóval;
  - **a HAMART-001 2. kiadása**: ha a javítás a lapot változtatja, a PR tartalmazza az újragenerált lapot és a `/kiadas` 5–6. lépését (függő nézetek, helyi kapufutás); a kiadás sora csak a felhasználó szó szerinti jóváhagyásával kerül be, addig előkészítve; új lektori kör nem kell.

**Nincs benne:**
- a blokk-szerkezet átalakítása (törlés, összevonás, áthelyezés): csak a felhasználó kifejezett kérésére, előtte vizuális összevetéssel;
- a HAMART kiadott lapjának kézi szerkesztése (ha a lap változik, az generált változás);
- az öt régi lap újragenerálása és az Alkalmazás kivezetése (CS4).

## 3. Lépések
1. **F212.1 — sablonmondat-lista (csak olvasó).** A `lexikon_general.py` és a hozzá tartozó renderelők minden olvasói sablonmondata és címkéje: HAMART-példa, előfordulás egy lapon, író blokk; jelölés: műhelyszó, ismétlődő címke, csak linket adó sor, blokkok közti számeltérés. Kimenet: `naplok/F212_sablonmondat_lista.md`, commit, draft PR.
   ⛔ **Megállás:** a felhasználó a listát nézi át, nem a lapot.
2. **F212.2… — javítás a generátorban, kapuval.** ⛔ Csak a #703 (F202, BDB-lánc) és a #704 (F203, Thayer) merge-e után, friss main-ről (ugyanazokat a fájlokat írják). Tételenként külön commit.
   *A fejléc `ir`/`olvas` mezője most csak az 1. lépést írja le (csak olvas, a `naplok/F212_*` fájlokat írja), mert a 2. lépés fájljait több nyitott brief is írja, és a feladatkövető ezt függési körnek venné. A 2. lépés indulásakor a fejléc `ir` mezője erre bővül:* `eszkozok/lexikon_general.py, eszkozok/olvasoi_kovetkeztetes.py, eszkozok/olvasoi_kapu.py, eszkozok/ellenorzes/allitas_adat.py, adat/jeloltek.tsv, adat/kapcsolatok.tsv, adat/SEMA.md, lexikon/HAMART-001_TUDOMANYOS.md` *(és az `olvas` a `motivumok/HAMART-001.md`-vel, a tematikus tanulmánnyal és a kereszthivatkozás-naplóval, a K1/3 szerint); a körbe eső briefek (#121, #123, #125, #178, #179, #196) állapotát akkor kell rendezni (lezárt-e a munkájuk a main-en).*
3. **C6** — séma, átköltöztető szkript, összevetés; a kivétel megszűnik.
4. Újragenerálás; E28 (régi lapok bájtazonossága) — a szándékos változás megnevezve; kapuk helyben (`eszkozok/ellenorzes/futtat.py`), független ellenőrzés.

## 4. Elfogadási feltételek
- 1. lépés: a lista a draft PR-on; a jelentés megmondja a sablonmondatok számát, a jelöltek számát és osztályát.
- 2. lépés: minden elfogadott tétel a generátorban javítva, gépi kapuval; az LXX-számok minden blokkban egy forrásból és egyeznek; a 103 kapcsolat-jelölt a `jeloltek.tsv`-ben; a régi lapok bájtazonosak, kivéve a megnevezett szándékos változást.

## 5. Döntésnapló
- 2026-11-11 (a felhasználó): D1 (N156) elvetve; C6 előrehozva a CS3-ba.
- 2026-11-12 (a felhasználó): a CS3 első lépése a sablonmondat-lista; a felhasználó a listát nézi át.
