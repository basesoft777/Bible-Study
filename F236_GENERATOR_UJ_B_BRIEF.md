---
feladat: 236
cim: A lapgenerátor újraírása, 2. rész — az olvasó szerver átkötése a lapmodellre (egy számítás, két megjelenítés)
kod: GENERATOR_UJ_B
tipus: feladat
fazis: folyamat
modell: opus
sav: SERVER
allapot: nem_indult
ad: az olvasó szerver kiejtése, szótári fordítása, olvasói nevei és alakosztály-kapuja ugyanabból a lapgen-számításból és bemeneti pontból jön, mint a lexikonlapé; a szerver és a lap számai gépi összevetésben azonosak; az F235 sebességhatárai és az F232 mércéje a 218b után is teljesülnek
kovetkezo: "A B0 (lapgen-felület) közvetlenül a #218 (F218.13) merge-e után fut, az F231 3. lépése megvárja (DT-F236c); a B-M0–B5 a #231, a #233 és a #235 merge-e után; az M0 bemenetenként méri a számítás helyét (DT-F236a; ha bármely bemenet a (b) változatot kéri: ⛔ az orkesztrátornál)"
munka: folyamat
olvas: [eszkozok/lapgen/, adat/lapgen_bemenetek.tsv, adat/olvasoi_nevtabla.tsv, adat/lapgen_sablonok.tsv, eszkozok/olvaso_szerver/teszt_sebesseg.py, eszkozok/olvaso_szerver/teszt_tervor.py, eszkozok/kiejtes.py, eszkozok/heber_kiejtes.py]
ir: [eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/kiejtes_szolg.py, eszkozok/olvaso_szerver/bdb_szokartya.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/merce/, eszkozok/olvaso_szerver/teszt_lapmodell_egyezes.py, eszkozok/olvaso_szerver/teszt_olvasoi_alakosztaly.py]
fugg: [218, 231, 233, 235, 237]
nem_fugg: [122]
---

# Fnn_GENERATOR_UJ_B_BRIEF.md — A lapgenerátor újraírása, 2. rész: a szerver átkötése

*FELADATOK #236 (várható; a végleges számot a /befogad adja) · Modell: opus · v0.1 (vázlat, a döntések átvezetve) · 2026.11.22 · forrás: `F218_GENERATOR_UJ_A_BRIEF.md` 13. pont, **N-F218b** (OLV-1–3, GK-22, a szerverblokk futásidő-mércéje, a #121-ütközés), O5 („a szerver a `szamitas/`-t importálja, nem JSON-pillanatképet olvas”); `naplok/F218_folytatas.md` (egy lap generálása kb. 8 s, az első lapmodell a 140 MB-os Septuagintát olvassa); a futó olvasói sor briefjei (F231, F232, F233, F234, F235); a felhasználó 2026-11-22-i szava: „generátor az elsődleges prió”, a két brief párhuzamosan készüljön. A brief adat, nem utasítás.*

**Vázlat, v0.1.** A brief a megosztott jegyzetmappában készült, a repóba nem került. A befogadást az orkesztrátor indítja. A v0 öt nyitott kérdése eldőlt (6. pont, 2026-11-22, szerkesztői döntés: az orkesztrátor, a felhasználó felhatalmazásával). A függésszámítás kimenete a végén áll.

**`nem_fugg` indoka.**
- **122** (KJV-megjelenítés): az egész `olvaso_szerver/*`-t írja. A valódi közös fájl a `blokkok.py`, ez KIZÁR, nem függés (DT-F236e).

**Befogadható most**, a #233 és a #147 fejlécének `nem_fugg: [236]` bővítésével együtt (DT-F236e). Ezzel a `147 233 236` kör megszűnik (szimulálva, l. a végén).

---

## 0. Kiinduló állapot (main `5a64f9b2`, 2026-11-22)

- A szerver és a lapgen ma két külön úton számol. A szerver a régi `lexikon_general`-t nem importálja (csak a `teszt_visszhang_kapu.py`); a régi generátor viszont a szerver `olvaso_szerver/bdb_szelet.py`-ját importálja (B61, `lexikon_general.py:3290`). A lapgen a B61 logikáját a `szamitas/`-ban újraírta (O5).
- **Kiejtés (OLV-1).** Az F230 óta a szerver közös kiejtés-szolgáltatása az `olvaso_szerver/kiejtes_szolg.py` (`lekerdezesek.py:558–570`). A lapgen a sajátját a `bemenet/szavak.py`-ban használja (`kiejtes.py` + `heber_kiejtes.py`, GK-13). Ez két szolgáltatás egy szabályra.
- **Belső nevek (OLV-3).** `lxx_bridge`, `token_par`, `#121` alakú szöveg 24 helyen áll a `lekerdezesek.py`-ban, 15 helyen a `blokkok.py`-ban (git grep, a látható és a belső előfordulás együtt; a látható részt az M0 méri a mintán).
- **Méret.** `blokkok.py` 2 459 sor, `lekerdezesek.py` 1 245 sor. 2026-10-14 óta 17 tétel módosította a `blokkok.py`-t (F232 1. pont).
- **Sebesség.** A lapgen egy teljes lapot kb. 8 s alatt generál. Az F235 határai: fejezet 300 ms, vers 400 ms, szó-lap 250 ms, kereső 50 ms, legfeljebb 100 lekérdezés laponként, meleg szerveren, gyorsítótár nélkül. A kettő között egy-két nagyságrend a különbség, ezért **a „szerver a `szamitas/`-t importálja” (O5) csak úgy tartható, ha a kérés útján kis, Strong- vagy versszintű számítás fut, a nagy bemenet nem a kérésben töltődik.** Ez a 218b fő tervezési kérdése (⛔ DT-F236a).
- A HN-13 és a HN-14 (a 218a v1-ének szervert érintő esetei) tartalma a mai fájlokban nem áll külön; a 218a v2 13. pontja szerint az OLV-1–3 fedi őket. Az M0 ezt kimondja, vagy pótolja a leírást.

## 1. A 218b és a futó olvasói sor — mi marad a 218b-nek

**A sor:** F232 mérce (PR #786, nyitva) → F235 sebesség → F231 egységes szókártya → F233 szócsoport → F234 felmérés-maradék.

| Tétel | Mit ad a 218b-nek | Mi marad a 218b-nek |
|---|---|---|
| **F232** | olvasói pillanatkép a mintakészletre (`merce/`), az olvasó tesztjei kapuban | a 218b minden látható változása a mércén diffként jelenik meg; a mérce frissítése a 218b-ben a szabálya szerint (kifejezett parancs, jóváhagyás) |
| **F235** | indexek, összevont lekérdezések, egyszeri betöltés, előmelegítés, sebességőr (`teszt_sebesseg.py`, `teszt_tervor.py`) | a 218b a sebességőrt **nem írja**, csak futtatja; a kérés útjára kerülő lapgen-hívás a határokon belül marad (4. pont) |
| **F231**, DT-F231a = (a) | a szó-lap BDB- és Thayer-kártyája a lapgen kártyamodelljéből (`bemenet/kartya_lap.py` → `szamitas/kartya.py`) | a kártyán csak a GK-22 számegyezés (B4); a kártyamodellt a 218b nem írja újra |
| **F231**, DT-F231a = (b) | — | **nem választható** (DT-F236c): a kártya a B0 felületén át a lapgenből jön, saját modell nem készül |
| **F233** | szócsoport, a felmérés tervezési pontjai | nincs átfedés a 218b tartalmával; csak fájlütközés (`blokkok.py`), ezért előbb fut |
| **F234** | a két régi felmérés még fennálló pontjai N-tételként | a 218b az OLV-1–3-ba eső F234-tételeket a saját szeleteiben zárja (`lezar:`), külön javítómenet nélkül |

**A 218b ezek után:** OLV-1 (egy kiejtés-szolgáltatás), OLV-2 (a szótári fordítás egy bemeneti pontja), OLV-3 (névtábla és alakosztály-kapu a szerver felületén), GK-22 (a szerver és a lap számai gépi összevetésben azonosak), a szerverblokk futásidő-mércéje, és a kettő közé a lapgen motívum nélküli olvasói felülete (`lapgen/olvaso/`, B0). A kártya nem marad a 218b-nek, ha a DT-F231a (a).

**Sorrend, hogy semmi ne készüljön kétszer:**

1. **F232 → F235 → F231 → F233** a mai sorrendben. A `blokkok.py`-t és a `lekerdezesek.py`-t mind írják; a 218b csak utánuk írhat (KIZÁR).
2. **F234** a 218b előtt, vagy a 218b M0-jával párhuzamosan (csak naplót ír). A 218b M0-ja az F234 szerver-tételeit bemenetként olvassa.
3. **218a vége (S8c, S8d, S9, F218.13)** a fenti sorral párhuzamosan. A `lapgen/` írása addig a 218a-é; az F231 a lapgent csak olvassa (az F231 briefje szerint).
4. **218c** közvetlenül az F218.13 merge-e után indul, párhuzamosan az olvasói sorral: fájlt az olvasói sorral és a 218b-vel nem közösen ír (l. a C vázlat 1. pontját). **Ez tölti ki a szünetet** a 218a és a 218b között.
5. **218b** az F233 (és lehetőleg az F234) után. Az M0 (csak olvas) az F218.13 után bármikor mehet.

**Kivétel a sorrend alól: a B0 felület (DT-F236c).** A B0 közvetlenül az F218.13 merge-e után fut, a 218b többi része előtt. Az F231 3. lépése megvárja, és a kártyát a B0 felületén át a lapgen modelljéből veszi. Az F231 saját kártyamodellt nem épít. Ok: a két kártya-implementáció az olvasó romlásának egyik mért oka, kettős munkát nem vállalunk. A B-K szelet ezzel tárgytalan. Az F231-re vonatkozó következmény az N-F236a tétel (9. pont); az F231 fejlécéhez ez a brief nem nyúl.

## 2. Cél

„Egy számítás, két megjelenítés”: ahol a lexikonlap és az olvasó szerver ugyanarról a szóról vagy versről mond valamit (kiejtés, rövid jelentés, fordítás, szótári kártya, számok, belső kulcsok olvasói neve), ott **egy** függvény számol, és a szerver ugyanazt a bemeneti pontot használja, mint a lap. Ellenőrzése: a GK-22 gépi összevetése és a meglévő lapgen-tesztek, a sebesség pedig az F235 őrével mérve nem romlik.

## 3. Hatókör

**Benne van:**
1. **`eszkozok/lapgen/olvaso/`** (új alcsomag): a lapgen motívum nélküli, Strong- és versszintű belépési pontjai a szerver számára (kártya, kiejtés, rövid jelentés és fordítás, névtábla-feloldás, alakosztály-kapu). Csak a meglévő `bemenet/` és `szamitas/` függvényeit hívja, saját számítás nincs benne; a GK-05 (0 motívumazonosító) és a GK-01 (útvonal csak a `bemenet/`-ben) rá is áll.
2. **OLV-1:** az `olvaso_szerver/kiejtes_szolg.py` a lapgen kiejtés-szolgáltatására delegál (vagy fordítva, az M0 mérése szerint: a jobbik marad, a másik vékony burok). Teszt: H2398, H7121, H2403a/b, és a teljes `strong_szotar` héber és görög soraira az egyezés száma.
3. **OLV-2:** a szótári fordítás (rövid jelentés, glossza, a javítótábla és az elavult-jelölés) a szerveren ugyanazon a bemeneti ponton, mint a lapon (az F213-eset tesztje). A megvalósítás helye a DT-F236a szerint.
4. **OLV-3:** a szerver látható szövegében a belső kulcs olvasói neve a `adat/olvasoi_nevtabla.tsv`-ből jön, ismeretlen kulcs kemény hiba (GK-23 a szerveren); a renderelt szerverblokkon a lapgen típus szerinti alakosztály-kapuja fut (GK-24 sablon-szabályai: aláhúzásos azonosító, `.tsv`/`.py`, `DT\d+`, `#\d{2,3}`, `N-?F?\d+`, nyers szótárfej, `sz<n>`, tört írásjel). Kalibrálás: 0 hamis találat a mintakészlet (F232) prózáján és idézetein.
5. **GK-22:** `teszt_lapmodell_egyezes.py` — a HAMART-001 és az ISTENTISZT-001 minden Strong-számára és versére a szerver számai (előfordulás, könyvek száma, Károli-alakok, KH-darab, LXX-társítás, és a DT-F231a (a) esetén a kártya jelentésrendje) a lapmodell számaival egyeznek.
6. **Futásidő-mérce szerverblokkra** (N-F218b): a kérés útján hívott lapgen-függvények ideje blokkonként, az F235 mérőeszközével; a határ az F235 határain belül (4. pont).

**Nincs benne:**
- A sebességőr (`teszt_sebesseg.py`, `teszt_tervor.py`), az indexek és az előmelegítés: az F235-é. A 218b futtatja őket, nem írja.
- A kártyamodell újraírása, ha a DT-F231a (a). A szókártya kinézete (F231), a szócsoport (F233).
- A `lexikon/` bármely fájlja, a régi generátor, a lapszöveg-kapuk, a `general.py`: a 218c-é.
- A `lapgen/bemenet/`, `szamitas/`, `megjelenites/` módosítása. Ha a felülethez ilyen kell, ⛔ (a lapgen a 218c-vel közös terület; két ág nem ír egy fájlba).
- Új próza, új sablonmondat. Ha a szerverre új olvasói mondat kell, az a fordítótáblába (DT897) kerül, a felhasználó jóváhagyásával (⛔).
- Az `sqlite_epit.py` (DT-F236a). ⛔ Ha az M0 bármely bemenetre az adatbázis-építős (b) változatot kéri, megállás és kérdés az orkesztrátorhoz; csak az ő döntésével bővül az `ir` az `sqlite_epit.py`-val és a `nem_fugg`-gal (a #101, a #122, a #137, a #235 is írja).

## 4. A sebességőr határai a 218b után is

- Az F235 négy időhatára és a 100 lekérdezés/lap határ **változatlanul** áll; a 218b nem lazít rajtuk. A tervellenőr (`EXPLAIN QUERY PLAN`, nincs `SCAN` 1000 sor fölött) a 218b új lekérdezéseire is fut.
- A kérés útján a lapgen-hívás **blokkonként legfeljebb 30 ms** meleg szerveren (becslés; az M0 méri, és ha a mért érték alapján más határ kell, ⛔).
- Indításkor a lapgen-bemenetek előtöltése az F235 előmelegítésének része, háttérben; **az első felhasználói kérés nem vár rá.** Az előtöltés ideje legfeljebb 10 s, a szerver memóriája legfeljebb 300 MB-tal nő (becslés; az M0 méri).
- Nagy bemenet (pl. a Septuaginta 140 MB-ja) a kérés útján nem töltődik be.

## 5. Lépések — egy-egy napos szeletek

Minden szelet: tesztek zöldek, a HAMART-regresszió RENDBEN (a lapgen kimenete bájtra azonos), az F232 mérce fut (eltérés csak indokolt, jóváhagyott frissítéssel), az F235 sebességőre zöld, commit `F236.<t>: …`, push, folytatási napló (`naplok/F236_jelentes.md`).

- **B-M0 (csak olvas, sonnet is mehet)** — modell-ellenőrzés; `fuggesek` egyezik a fejléccel; `get_usage`. Mérés a main-en:
  1. kiejtés: a `kiejtes_szolg` és a lapgen szolgáltatása a teljes `strong_szotar`-on, eltérő sorok száma és mintája;
  2. fordítás: a szerver és a lap rövid jelentése a HAMART- és az ISTENTISZT-Strongokon; az F213-eset;
  3. belső nevek: a látható szövegben a mintakészleten (F232) talált belső kulcsok száma, blokkonként;
  4. sebesség: a kártya, a kiejtés és a fordítás lapgen-hívásának ideje Strongonként; a szükséges bemenetek előtöltési ideje és memóriája;
  5. a DT-F231a kimenete, és hogy mi maradt a kártyából;
  6. az F234 szerver-tételei, amelyek az OLV-1–3-ba esnek.
  A DT-F236a szerint bemenetenként (a) vagy (b), a küszöbök alapján; ⛔ csak ha bármely bemenet a (b)-t kéri, vagy ha a lapgen-hívás a 30 ms-ot meghaladja. Az eredmény a jelentés M0 szakaszában, számokkal.
- **B0 — az F218.13 merge-e után azonnal, a B-M0 előtt (DT-F236c)** — a `lapgen/olvaso/` felület (köztük a kártya belépési pontja az F231 számára): belépési pontok, szerződés-tesztek (motívum nélkül hívható, a lap ugyanazon függvényének eredményével egyezik), GK-05, GK-01. A lapgen kimenete bájtra azonos.
- **B1 (OLV-1)** — egy kiejtés-szolgáltatás; a `kiejtes_szolg` burok vagy forrás, az M0 szerint; tesztek; a mérce diffje (ha a kiejtés változik a mintán, soronként indokolva).
- **B2 (OLV-2)** — a szótári fordítás egy bemeneti pontja, a DT-F236a szerint; F213-teszt; a frissességi kapu (a bemenet hash-e az indításkor vagy az építéskor rögzítve, eltérésnél kimondott figyelmeztetés).
- **B3 (OLV-3)** — névtábla és alakosztály-kapu a szerver felületén; a kapu kalibrálása a mintán; a mérce diffje.
- **B4 (GK-22)** — `teszt_lapmodell_egyezes.py`; a futásidő-mérce blokkonként; az F235 mérőeszközével előtte–utána táblázat.
- **B5** — ⛔ **független ellenőr** (`fuggetlen-ellenor`; csak a kód és a mérések, a kinézetet nem nézi), egy javítókör; draft PR, CI; a mérce frissítésének jóváhagyása a PR leírásában az orkesztrátortól (DT-F236d). Merge az orkesztrátortól.

**Becsült terjedelem:** 7 szelet (B-M0, B0–B5), 5–7 munkanap; a B0 ebből kb. 1 nap, az F218.13 után azonnal.

## 6. Döntések (2026-11-22; szerkesztői döntés: az orkesztrátor, a felhasználó felhatalmazásával)

*A v0 öt nyitott kérdése eldőlt. Az orkesztrátor üzenete, a felhatalmazás forrása: a felhasználó 2026-11-22-i szavai („a döntéseket te hozod meg. a sessionok neked küldjék a kérdést”).*

1. **DT-F236c — a B0 és az F231 viszonya: (a).** A B0 közvetlenül az F218.13 merge-e után fut, és az F231 3. lépése megvárja. Ok: a két kártya-implementáció az olvasó romlásának egyik mért oka, kettős munkát nem vállalunk. Következmény az F231-re: N-F236a (9. pont). A B-K szelet kikerült.
2. **DT-F236a — a közös számítás helye: vegyes, bemenetenként az M0 mérése szerint.**
   - A kis bemenetek az (a) szerint indításkor a memóriába kerülnek.
   - A nagy bemenetek a (b) szerint az adatbázis-építőn át töltődnek.
   - Küszöbök: előtöltés ≤ 10 s, háttérben; memória-többlet ≤ 300 MB; blokkonként ≤ 30 ms lapgen-hívás.
   - **Kötelező feltétel:** az F235 határai (fejezet 300 ms, vers 400 ms, szó-lap 250 ms, legfeljebb 100 lekérdezés laponként) és a `teszt_sebesseg.py` a 218b után is zöldek.
   - **Az `sqlite_epit.py` most nem kerül az `ir`-be.** ⛔ **Ha az M0 bármely bemenetre a (b) változatot kéri: megállás, és a kérdés az orkesztrátorhoz megy.** Ilyenkor az `ir` bővül az `sqlite_epit.py`-val és a szükséges `nem_fugg`-gal.
3. **DT-F236b — a névtábla és a DT897 fordítótábla: két tábla, két entitás.** A fordítótábla a felület feliratait tartja (blokkcím, gomb, rögzített mondat), a névtábla a belső kulcsok olvasói nevét. Gépi kapu tiltja, hogy egy kulcs mindkettőben álljon. A szerver a belső kulcs nevét csak a névtáblából veheti.
4. **DT-F236d — a mérce frissítésének jóváhagyása.** A soronként indokolt mérce-diffet az orkesztrátor hagyja jóvá a PR leírásában. Ha egy blokk szerkezete változik: ágas előnézet (DT886) és a felhasználó nézete kell.
5. **DT-F236e — a függések.** A #233 és a #147 `nem_fugg: [236]`-ot kap (a befogadás végzi), a 218b `nem_fugg: [122]`-t (fejléc). A `fugg: [231, 233]` kézi függés marad.

**Megmaradt ⛔ pontok:**
- DT-F236a (b)-kérése az M0-ban;
- a lapgen `bemenet/`, `szamitas/`, `megjelenites/` módosításának igénye (3. pont);
- új olvasói mondat a fordítótáblába;
- a mért lapgen-hívásidő a 30 ms fölött;
- a független ellenőrzés (B5).

## 7. Elfogadási feltételek (mérve)

1. **OLV-1:** a szerver és a lap kiejtése a teljes `strong_szotar` héber és görög során egyezik, vagy az eltérés soronként indokolt a jelentésben. H2398, H7121, H2403a/b teszt zöld. Egy kiejtés-szolgáltatás marad, a másik vékony burok saját szabály nélkül (statikus teszt).
2. **OLV-2:** az F213-eset tesztje zöld; a HAMART- és az ISTENTISZT-Strongokon a szerver rövid jelentése a lapéval egyezik.
3. **OLV-3:** a mintakészlet látható szövegében 0 belső kulcs és 0 alakosztály-találat; a kalibrálásban 0 hamis találat; ismeretlen kulcs → kivétel (teszt); egy kulcs sem áll egyszerre a névtáblában és a fordítótáblában (kapu, DT-F236b).
4. **GK-22:** `teszt_lapmodell_egyezes.py` zöld mindkét mintamotívum minden Strongján és versén, a kártya jelentésrendjével együtt.
5. **Sebesség:**
   - az F235 négy határa, a 100 lekérdezés/lap határ, a `teszt_sebesseg.py` és a tervellenőr zöld;
   - blokkonként a lapgen-hívás ≤ 30 ms;
   - előtöltés ≤ 10 s, háttérben; memória-többlet ≤ 300 MB;
   - előtte–utána táblázat a jelentésben.
6. **Lap:** a HAMART-regresszió RENDBEN, a lapgen tesztjei és a festékpróba változatlanul zöldek; a `lapgen/` kódjában 0 motívumazonosító.
7. **Mérce:** az F232 mércéje fut; minden eltérés jóváhagyott frissítéssel (DT-F236d).
8. **Független ellenőrzés:** `TISZTA`, vagy az egy javítókör után az.

**Hatókör-szűkítés (DT-F221a).** A független ellenőr a kinézetet nem nézi.
- (a) Ellenőrzés nélkül marad: a blokkok vizuális rendje.
- (b) Helyette méri: az F232 mércéje (blokksor, látható szöveg), szerkezeti változásnál pedig az ágas előnézet (DT-F236d).

## 8. Döntésnapló

*A `dontesek/uj/<ágnév>.md`-be kerülő sorok (helyőrzővel). Forrás mindegyiknél: szerkesztői döntés (az orkesztrátor, a felhasználó felhatalmazásával), 2026-11-22.*

| Helyőrző | Döntés |
|---|---|
| DT-F236a | A közös számítás helye vegyes, bemenetenként az M0 mérése szerint (kis bemenet: memória indításkor; nagy: adatbázis-építő a lapgen bemeneti függvényén át). Küszöb: 10 s előtöltés, 300 MB, 30 ms/blokk. Az F235 határai és a `teszt_sebesseg.py` kötelezően zöldek. Az `sqlite_epit.py` csak az orkesztrátor újabb döntésével kerül az `ir`-be |
| DT-F236b | Névtábla és DT897 fordítótábla: két tábla; kapu tiltja, hogy egy kulcs mindkettőben álljon |
| DT-F236c | A B0 (`lapgen/olvaso/`) az F218.13 után, a 218b többi része előtt fut; az F231 3. lépése megvárja, saját kártyamodell nem készül |
| DT-F236d | A soronként indokolt mérce-diffet az orkesztrátor hagyja jóvá; szerkezeti blokkváltozásnál ágas előnézet és a felhasználó |
| DT-F236e | `nem_fugg`: #233 és #147 → [236]; 218b → [122] |

Előzmény: O5 (a 218a briefje): a szerver a `szamitas/`-t importálja, JSON-pillanatkép nem készül. A DT-F236a (b) része ezt nem sérti: az adatbázis a bemeneti réteg tárolója marad, a számítás a `szamitas/`-ban fut.

## 9. Nyitott tételek (a `nyitott/uj/<ágnév>.md`-be)

- **N-F236a** (DT-F236c; az F231 következménye): az F231 3. lépése (a közös kártya a héber lapon) a 218b B0 szeletének merge-e után indul, és a kártyát a `lapgen/olvaso/` felületén át a lapgen kártyamodelljéből veszi. A DT-F231a (b) változata (saját modell egyezési teszttel) nem választható. A teendő az F231 sessionjéé vagy a befogadóé, ez a brief nem végzi el:
  - **A B0 a feladatkövetőben külön tétel kell legyen.** A 236 fejlécének `fugg: [218, 231, 233, 235]`-je az egész tételre vonatkozik, így a B0 a 236-on belül csak a #231 után futhatna: ez ellentmond a DT-F236c-nek. Javaslat a befogadónak: a B0 külön kis brief (vagy csonk) legyen, `fugg: [218]` és `ir: [eszkozok/lapgen/olvaso/]` fejléccel; az F231 `fugg`-ja erre a számra bővül; a 236 `fugg`-ja is kapja meg;
  - a briefjének M0-ja a „hívható-e motívum nélkül” kérdés helyett a B0 felületét veszi alapul.

---

## Függésszámítás (ideiglenes fejléccel, a main `5a64f9b2`-n, 2026-11-22; a döntések után)

`python eszkozok/feladatok.py fuggesek --extra <B fejléc> --extra <C fejléc> --extra <a 147, 153, 205, 229, 231, 233, 234 brief másolata a döntés szerinti nem_fugg-gal>`.

A másolatok a repón kívül, a session ideiglenes könyvtárában álltak. Az `--extra` azonos számnál felváltja a meglévő briefet, így a befogadás utáni állapotot méri. A 236-ot érintő sorok:

```
FUGGES	236	218	adat/lapgen_bemenetek.tsv*
FUGGES	236	231	kezi
FUGGES	236	233	kezi
FUGGES	236	235	eszkozok/olvaso_szerver/teszt_sebesseg.py*
KIZAR	106	236	eszkozok/olvaso_szerver/blokkok.py	×
KIZAR	122	236	eszkozok/olvaso_szerver/blokkok.py	×
KIZAR	134	236	eszkozok/olvaso_szerver/sablonok/	×
KIZAR	135	236	eszkozok/olvaso_szerver/blokkok.py	×
KIZAR	138	236	eszkozok/olvaso_szerver/blokkok.py	×
KIZAR	139	236	eszkozok/olvaso_szerver/sablonok/	×
KIZAR	164	236	eszkozok/olvaso_szerver/alkalmazas.py	×
KIZAR	218	236	eszkozok/lapgen/olvaso/	×
KIZAR	232	236	eszkozok/olvaso_szerver/merce/	×
KIZAR	235	236	eszkozok/olvaso_szerver/lekerdezesek.py	×
KIZAR	236	147	eszkozok/olvaso_szerver/lekerdezesek.py	×
KIZAR	236	231	eszkozok/olvaso_szerver/blokkok.py	×
KIZAR	236	233	eszkozok/olvaso_szerver/blokkok.py	×
SORREND	106	236	számból (a kisebb sorszám előre)
SORREND	122	236	számból (a kisebb sorszám előre)
SORREND	134	236	számból (a kisebb sorszám előre)
SORREND	135	236	számból (a kisebb sorszám előre)
SORREND	138	236	számból (a kisebb sorszám előre)
SORREND	139	236	számból (a kisebb sorszám előre)
SORREND	164	236	számból (a kisebb sorszám előre)
SORREND	218	236	függésből
SORREND	232	236	számból (a kisebb sorszám előre)
SORREND	235	236	függésből
SORREND	147	236	számból (a kisebb sorszám előre)
SORREND	231	236	függésből
SORREND	233	236	függésből
KOR	218 237	-	függési kör
```

**Olvasat.**
- **A `147 233 236` kör megszűnt** a DT-F236e három `nem_fugg`-jával (a 218b fejlécében [122]; a #233 és a #147 fejlécében [236], ezt a befogadás írja be).
- `KIZAR` = nem futhat egyszerre, bármelyik mehet előbb (`feladatok.py`); `UTKOZES` típusú sor a kimenetben nincs.
- A megmaradt `218 237` kör a C vázlaté: a #218 `olvas`-a és a C `ir`-je (`lexikon_general.py`) adja. A számítás a lezárt briefet csak akkor hagyja ki, ha a main-en is `lezarva` (`feladatok.py` `statusz`). A 218b-t ez nem érinti.
- **Befogadhatóság: a B most befogadható**, a #233 és a #147 `nem_fugg` bővítésével egy menetben, a B0-t külön tételként (N-F236a).
