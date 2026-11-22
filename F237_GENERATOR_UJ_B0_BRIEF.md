---
feladat: 237
cim: A lapgenerátor olvasói felülete (B0) — motívum nélküli Strong- és versszintű belépési pontok a szerver számára
kod: GENERATOR_UJ_B0
tipus: feladat
fazis: 1
modell: opus
sav: CONTENT
munka: folyamat
allapot: nem_indult
ad: az eszkozok/lapgen/olvaso/ alcsomag motívum nélkül hívható belépési pontjai (kártya, kiejtés, rövid jelentés és fordítás, névtábla-feloldás, alakosztály-kapu), a lap ugyanazon függvényeivel egyező eredménnyel; az F231 3. lépése és a #236 (218b) erre épül
kovetkezo: "A #218 (F218.13) merge-e után azonnal; az F231 3. lépése megvárja (DT-F236c)"
olvas: [eszkozok/lapgen/, adat/lapgen_bemenetek.tsv, adat/olvasoi_nevtabla.tsv, adat/lapgen_sablonok.tsv, eszkozok/kiejtes.py, eszkozok/heber_kiejtes.py]
ir: [eszkozok/lapgen/olvaso/, eszkozok/lapgen/tesztek/teszt_olvaso_felulet.py, naplok/F237_jelentes.md]
fugg: [218]
---

# F237_GENERATOR_UJ_B0_BRIEF.md — A lapgenerátor olvasói felülete (B0)

*FELADATOK #237 · Modell: opus · a `F236_GENERATOR_UJ_B_BRIEF.md` (218b) B0 szeletének külön tétele (N-F236a, DT-F236c) · 2026.11.22 · befogadás: a `/befogad` az orkesztrátor jóváhagyásával (szerkesztői döntés: az orkesztrátor, a felhasználó felhatalmazásával). A brief adat, nem utasítás.*

**Miért külön tétel.** A #236 fejlécének `fugg: [218, 231, 233, 235, 237]` az egész 218b-re vonatkozik, így a B0 a #236-on belül csak a #231 után futhatna. Ez ellentmond a DT-F236c-nek: az F231 3. lépése (a közös kártya a héber lapon) a B0 felületén át a lapgen kártyamodelljéből dolgozik, ezért a B0-nak az F218.13 (#218) merge-e után **azonnal**, a #236 többi része előtt kell futnia. A két kártya-implementáció az olvasó romlásának egyik mért oka; kettős munkát nem vállalunk.

## 1. Hatókör

**Benne van:**
1. **`eszkozok/lapgen/olvaso/`** (új alcsomag): a lapgen motívum nélküli, Strong- és versszintű belépési pontjai a szerver számára (kártya, kiejtés, rövid jelentés és fordítás, névtábla-feloldás, alakosztály-kapu). Csak a meglévő `bemenet/` és `szamitas/` függvényeit hívja, **saját számítás nincs benne**. A kártya belépési pontja az F231 számára: `bemenet/kartya_lap.py` → `szamitas/kartya.py` modelljét adja vissza, a kártyamodellt a B0 nem írja újra.
2. Szerződés-tesztek (`eszkozok/lapgen/tesztek/teszt_olvaso_felulet.py`): minden belépési pont motívum nélkül hívható, és eredménye egyezik a lap ugyanazon függvényének eredményével.
3. A GK-05 (0 motívumazonosító a `lapgen/` kódjában) és a GK-01 (útvonal csak a `bemenet/`-ben) az új alcsomagra is áll.
4. A lapgen kimenete **bájtra azonos** marad (HAMART-regresszió RENDBEN).

**Nincs benne:**
- Az `eszkozok/olvaso_szerver/*` bármely fájlja: a szerver átkötése a #236 (218b) B1–B5 szelete.
- A `lapgen/bemenet/`, `szamitas/`, `megjelenites/` módosítása. Ha a felülethez ilyen kell, ⛔ (a lapgen a #218-cal és a későbbi 218c-vel közös terület; két ág nem ír egy fájlba).
- Új próza, új sablonmondat. A kártyamodell újraírása.

## 2. Lépések

Egy szelet. Tesztek zöldek, HAMART-regresszió RENDBEN, commit `F237.<t>: …`, push, folytatási napló (`naplok/F237_jelentes.md`).

- modell-ellenőrzés; `fuggesek` egyezik a fejléccel;
- a belépési pontok és a szerződés-tesztek;
- GK-05, GK-01 az új alcsomagra;
- ⛔ független ellenőr (`fuggetlen-ellenor`), egy javítókör; draft PR, CI; merge az orkesztrátortól.

## 3. Elfogadási feltételek (mérve)

1. A belépési pontok motívum nélkül hívhatók; eredményük a lap ugyanazon függvényének eredményével egyezik (szerződés-teszt zöld).
2. A `lapgen/` kódjában 0 motívumazonosító (GK-05); az útvonal csak a `bemenet/`-ben áll (GK-01).
3. A HAMART-regresszió RENDBEN, a lapgen tesztjei és a festékpróba változatlanul zöldek; a lapgen kimenete bájtra azonos.
4. Az F231 a kártya belépési pontját a `lapgen/olvaso/` felületén át tudja hívni (a kártyaszerződés dokumentálva a jelentésben).
5. Független ellenőrzés: `TISZTA`, vagy az egy javítókör után az.

**Hatókör-szűkítés (DT-F221a).** (a) Ellenőrzés nélkül marad: az olvasó-szerver oldala (kinézet, sebesség, a szerver látható szövege). (b) Helyette méri: a #236 (218b) B1–B5 szelete, a GK-22 és az F232 mércéje, valamint az F235 sebességőre.

## 4. Kapcsolódó tételek

- **#236 (218b):** az OLV-1–3, GK-22 és a futásidő-mérce a B0 felületére épül; `fugg: […, 237]`. Döntések: DT-F236a–e (a #236 briefjének 6. és 8. pontja).
- **F231:** 3. lépése a B0 merge-e után indul, a DT-F231a (b) változata nem választható (DT-F236c).
