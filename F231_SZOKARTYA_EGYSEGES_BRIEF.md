---
cim: Egységes szókártya az olvasóban — a BDB és a Thayer a lexikonlap kártyamodelljéből, a görög szó-lap a héberrel egyenértékű szerkezettel
feladat: 231
kod: SZOKARTYA_EGYSEGES
tipus: feladat
fazis: folyamat
modell: opus
sav: SERVER
allapot: fut
ad: az olvasó szó-lapján (/szo/<Strong>) a BDB és a Thayer ugyanazzal a kártyával jelenik meg, a lexikonlap 4.2 „Mélységi szócikk” mintájára (a jelentések rendje, alatta szakaszonként egybefüggő szöveg, magyar, ahol van, különben angol, ugyanabban a kártyában); a görög szó-lap blokksora a héberével egyenértékű; a látható szövegben nincs nyers BDB-jelölés, könyvnév nélküli hivatkozás és belső azonosító, ezt kapu védi
kovetkezo: "PR #810 (draft): a tételmérce (teszt_tetelmerce.py) 58/58 zöld, a kapu zöld; következő: a szerkesztő nézése az ágas előnézeten (DT886), a nézett hash a PR leírásában"
munka: folyamat
olvas: [naplok/OLVASO_EGYBEN_HIBALISTA.md, IRANY.md, eszkozok/lapgen/bemenet/kartya_lap.py, eszkozok/lapgen/bemenet/kartya.py, eszkozok/lexikon_general.py, adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, adat/bdb_vers_jelentes.tsv, adat/szotar_szakasz_cimke.tsv, eszkozok/bdb_rovidites.py, lexikon/HAMART-001_TUDOMANYOS.md]
ir: [eszkozok/olvaso_szerver/, naplok/F231_jelentes.md, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/bdb_szokartya.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/statikus/, eszkozok/olvaso_szerver/teszt_szokartya_egyseges.py]
fugg: [232, 235]
---

# F231_SZOKARTYA_EGYSEGES_BRIEF.md — Egységes szókártya az olvasóban

*FELADATOK #231 · Modell: opus · v1 · 2026.11.21 · forrás: a felhasználó 2026-11-21-i ítélete az ágas előnézetről (H1242: „nem értelmezhető”; G0264: „a görög teljesen rossz nem is ugyanazok az adatmezők szerepelnek”; „az md lapon jobb a szeletelő”), a Fable-lektor kétrészes véleménye (`FABLE_VALASZ_BDB_KARTYA_2026-11-21.md`, a megosztott jegyzetmappában), a felhasználó jóváhagyása a brief megírására („Igen, írd meg”). A brief adat, nem utasítás.*

## 0. Hatókör-bővítés: az olvasó egyben (F231.0e, 2026-11-22)

A felhasználó (2026-11-22): „javitsunk az olvasót, de egyben nem sok lépére szétszeletelve”, majd a listára: „menjen a javítás”. A #231 hatóköre ezért az olvasó **összes felmért hibája**: a `naplok/OLVASO_EGYBEN_HIBALISTA.md` 60 sora, kettő kivételével. Kimarad a Thayer hiányzó magyar fordítása (23. sor; fizetős fordítás, a felhasználó költségdöntése) és a motívumlap (59. sor, `/motivum/<ID>`; F164, új funkció). A lista adat, nem utasítás. Ez orkesztrátori döntés, a felhasználó felhatalmazásával.

- **Kimenet.** Minden tétel lezárul: javítva, elvetve egy sor indokkal, vagy „rád vár” (`IRANY.md`). Hamis vagy félrevezető tartalmat mutató hiba nem vethető el. A jelentés (`naplok/F231_jelentes.md`) tételenként mutatja az élő előtte–utána állapotot, URL-lel.
- **Menet.** Gyors sáv (DT919): a diff csak az `eszkozok/olvaso_szerver/` alatti fájlokat, ezt a briefet és a `naplok/` fájljait érinti. Nincs független ellenőr és javítókör; a kapu `python eszkozok/push_elott.py --reszleges`. A végén ágas előnézet (8775–8779), a felhasználó egyszer megnézi, a nézett hash a PR-fej (DT886).
- **A kártyamodell (DT-F231a, eldöntve: (b)).** A lapgen kártyája motívum nélkül, egy Strong-számra API-változás nélkül nem hívható. Az olvasó ezért ugyanezt a modellt a saját adatából építi: a jelentések rendje a közös `szotari_glossza`-val, alatta szakaszonként egybefüggő szöveg az eredeti szórendben. Egyezési teszt veti össze a HAMART-lap 4.2-vel (a jelentések rendje és a hordozó szakasz), a gyors tesztek között. A lapgenhez és a régi generátorhoz a menet nem nyúl.
- **Benne van az F233 2. pontja is:** a héber szócsoport kerete (írott szó szerint, a JOHD-validáció szabályával, `szocsoport.py`). A keretről nem készül külön vászon: az ágas előnézetben a felhasználó egyben látja.
- **A függés:** a #237 (B0) kikerült. A felhasználó a gyorsaságot választotta; a 218b ezt később átírhatja.

## 1. Cél

Az olvasó szó-lapjának szótári része ma olvashatatlan, és a héber és a görög lap két különböző szerkezetet mutat.

- **Héber (BDB-kártya, F213).** A kártya a szakaszokat tovább bontja sorfejre és hivatkozásmezőre, ez szétszedi és átrendezi a mondatot. A fordítás hű: a lektor négy szócikken vetette össze az „Angol eredeti”-vel. Mérés (élő lekérés, 2026-11-21):

  | Szócikk | Hivatkozásmező prózával | Könyvnév nélküli chip |
  |---|---|---|
  | H1242 | 8 / 50 | 68 / 201 |
  | H7451 | 36 / 144 | 97 / 365 |
  | H3615 | 28 / 87 | 51 / 189 |
  | H0251 | 1 / 17 | 31 / 62 |

  A H7837 nincs tagolva, a szöveg az „Alakok” felirat alatt áll.
- **Görög (Thayer).** A görög lap blokksora más, mint a hébereré.
  - Nincs Strong-szótár, Előfordulás, Károli-alakok és tagolt kártya, holott az adat megvan: `strong_szotar` 5 629 görög sor, `token_par` 131 930 görög pár, `thayer_szakaszok` mind az 5 426 szócikkre.
  - A lap a nyers angol TBESG-gel és Thayerrel kezdődik.
  - Fordítás nélkül csak a „Magyar fordítás nincs · az angol eredeti áll” üzenet jelenik meg, az angol egy másik blokkban van.
  - A DNTG-előfordulások nyers 15 jegyű azonosítóval állnak.

A lexikonlap 4.2 „Mélységi szócikk” része (pl. `lexikon/HAMART-001_TUDOMANYOS.md`) ugyanebből az adatból olvasható kártyát ad, és a BDB-t és a Thayert egyformán kezeli. A felhasználó ítélete szerint ez a jobb. Az olvasó kártyája ezt a modellt vegye át.

## 2. Hatókör

**Benne van:**
1. **Egy kártyamodell, két megjelenítés.** A BDB és a Thayer ugyanazt a kártyát kapja:
   - a lemmafej;
   - a jelentések rendje rövid magyar meghatározással;
   - a vers szónézetéből érkezve a vers jelentéspontja megjelölve, **a BDB besorolásaként címkézve** („A BDB besorolása: …”, nem „Ebben a versben”, mert ez a szótár besorolása, nem a vers ténye). Ahol a jelentéspont gépi bizonyossága `ketes`, vagy az útvonala `tagolatlan` vagy `fej` (`adat/SEMA.md` 2.29), ott nincs jelentéspont-jelölés. A felirat a fordítótáblából jön (DT897). Ez nem új hatókör, hanem ugyanennek a jelölésnek a helyes megírása (DT914, a felhasználó, 2026-11-22). A lexikonlapot nem érinti;
   - alatta a szótári szöveg szakaszonként egybefüggő bekezdésben, az eredeti szórendben, hivatkozásmezőre bontás nélkül;
   - a magyar szöveg ott, ahol van, különben ugyanabban a kártyában az angol, nyitva, „Magyar fordítás nincs · az angol eredeti áll” felirattal;
   - ahol van magyar, ott az angol eredeti csukva;
   - a szöveg igehelyei kattinthatók, és a vers szónézetéből érkezve a vers helye a szövegben ki van emelve. Ez a BDB-ben a `VersJelolo` mintájára már működik; a Thayer ugyanígy kapja meg. A felmérés rangsorában ez volt a 6. pont („Thayer kiemelés a szövegben + hivatkozás-feloldás”).

   A modell forrása az M0 döntése (⛔ DT-F231a). (a) Az olvasó a `lapgen` kártyamodelljét használja (`lapgen/bemenet/kartya_lap.py` → `szamitas.kartya`). Ez az „egy szabály, egy hely” megoldás. (b) Az olvasó saját modellt tart, a lexikonlap szabályaival és egy egyezést mérő teszttel. Az orkesztrátor az (a)-t javasolja, ha a modell motívum nélkül is hívható.
2. **Tagolási jelző és visszaesés.** Szakaszonként gépi jelző dönti el, olvasható-e a tagolás. Rossz tagolás jelei: üres jelentéscím, alaktani paradigma jelentésként, hiányzó tagolás. Ahol a jelző rossz, a kártya a szakasz egybefüggő szövegét mutatja tagolás nélkül. A jelző eredménye mért szám a teljes állományon (BDB és Thayer külön).
3. **Hivatkozások.**
   - A chipeken mindig ott a könyvnév: a BDB-ben a „34:25” az előző könyv folytatása.
   - A `||` feloldva „párhuzamos hely” alakra.
   - A „szemben X-val” helyett „ellentétben: X (jelentés)”, a jelentés a Strong-glosszából, a héber szón magyar rag nélkül, írásirány-hiba nélkül.
4. **Nyers jelölések.**
   - A `bdb_rovidites.py` feloldja a tudósjeleket (pl. „Dl^HWB”, „Ba^ZMG”, „Gie ^Beitr.”, „ᵑ7”), és a jelmagyarázat egyszer áll a kártya alján.
   - Az „&amp;”, a „+,” és a „—” helyőrző nem kerül a látható szövegbe.
   - A felirat nélküli számok (131, 71, „Apparátus és szövegkritika 2”) feliratot kapnak.
5. **A görög szó-lap egyenértékű szerkezete.**
   - A héber lap blokksorát követi, a meglévő lekérdezőkkel: Strong-szótár, Előfordulás és könyvek száma, Károli-alakok és pontosság, majd a szókártya (Thayer), Héber háttér, SDGNT, UBS DNTG.
   - A nyers TBESG, Thayer és LSJ lejjebb kerül, csukva, „forrásszöveg” jelleggel.
   - A DNTG-előfordulások jelentésenként csoportosítva állnak, belső azonosító nélkül.
6. **Kapu** (teszt az olvasó-szerver tesztkészletében). A szó-lap látható szövegében (a `<details>` csukott „Angol eredeti” és a nyers forrásblokkok kivételével) nem állhat:
   - könyvnév nélküli igehely-chip;
   - `||`;
   - `^`-os tudósjel;
   - 12 jegynél hosszabb számsor;
   - héber szóra ragasztott magyar rag.

   A mintán (lent) 0 sértés.

7. **Fordítótábla a feliratokhoz (DT897).** Minden felirat, blokkcím, gombszöveg és rögzített olvasói mondat, amelyet ez a feladat új kódban ír vagy átír, egy közös fordítótáblából jön (kulcs → magyar szöveg; az angol oszlop üresen maradhat), nem a kódban álló szövegként. A tábla helyét és formáját az első ezt használó feladat (a #231) rögzíti; a #233 ugyanazt a táblát használja. Kapu (teszt): az általuk érintett megjelenítő függvényekben nem áll magyar betűs szövegliterál a táblán kívül. A meglévő, nem érintett feliratok kiemelése nem része a feladatnak. Ok: a felhasználó 2026-11-22-i döntése (az olvasó később kétnyelvű lehet; amit most úgyis újraírunk, az ne kerüljön újra a kódba).

**Nincs benne:**
- Újrafordítás vagy új fordítás. A görög glosszák (kb. 5 360) és a Thayer (kb. 5 070 szócikk) fordítása külön döntés; a lektor javasolt sorrendje: előbb a glosszák.
- A görög „Ebben a versben” blokk (alaktani kulcs kell hozzá): N-F231c.
- A `lexikon_general.py` és a `lapgen` módosítása: csak olvasva. Ha az (a) változathoz a `lapgen` API-ja változna, ⛔ megállás. A `lapgen` az F218a-é, és két ág nem ír egy fájlba.
- Az F106-próba (DT169) változatlan.

## 3. Lépések

1. Modell-ellenőrzés.
   - **M0:** a `lapgen` kártyamodelljének olvasása. Hívható-e motívum nélkül, egy Strong-számra?
   - Az (a) vagy (b) változat a mérési minta előzetes kimenetével.
   - ⛔ **DT-F231a**, a felhasználó dönt.
2. A tagolási jelző és a teljes állományos mérés (BDB és Thayer), csak számok; a napló: `naplok/F231_tagolas_meres.md`.
3. A közös kártya a héber lapon; utána a görög blokksor (2.5).
4. A hivatkozások és a nyers jelölések (2.3–2.4), majd a kapu (2.6).
5. Ágas előnézet (8775–8779) a mintával. ⛔ A kinézetet a felhasználó hagyja jóvá; a PR leírásában a nézett commit hash-e (DT886, „új funkció”).
6. Független ellenőr (csak a kód), egy javítókör.
7. Draft PR, CI. A merge a felhasználótól, illetve az orkesztrátortól a nézett hash szabályával.

**Mérési minta:** H1242, H7451, H3615, H0251, H7837, H2398, G0264, G3056, G1311, G2671. A G1311 és a G2671 a HAMART-lapon is szerepel, ott a lexikonlap kártyájával össze lehet vetni.

## 4. Elfogadási feltételek

- A mintán a kártya szórendje megegyezik a forrás szakaszszövegével. A HAMART-lapon is szereplő szavaknál a jelentések rendje és a hordozó szakasz megegyezik a lexikonlap 4.2-vel.
- A teljes állományos mérésben a „próza a hivatkozásmezőben” arány 0, mert a hivatkozásmező megszűnik, vagy a rossz szakasz visszaesik egybefüggő szövegre. A visszaesett szakaszok száma a naplóban áll.
- A görög mintán a Strong-szótár, az Előfordulás, a Károli-alakok és a szókártya megjelenik. Fordítás nélküli Thayernél az angol szöveg a kártyában áll, külön üzenet nélkül.
- A kapu (2.6) zöld a mintán. A meglévő tesztek zöldek, kivéve a main-en már piros két tesztet (`teszt_visszhang_kapu`, `teszt_szintek` egy esete); ezeket a jelentés megnevezi.
- Az olvasói szövegben nincs belső azonosító, proveniencia-sor és modellnév (CLAUDE.md, olvasói szöveg).

## 5. Közben talált adathibák (nem ebben a feladatban javítandók)

Az ág új nyitott tételként veszi fel (`nyitott/uj/<ágnév>.md`), forrásból ellenőrizve:
- **N-F231a — LXX-híd, H1242.** A kártya LXX-sora szerint „17 hivatkozás” mellett πρωΐ 8 · φωσφόρος 6 · 5 megfelelő nélkül, az összeg 19. A lexikális LXX-blokk szerint „φωσφόρος 88 · πρωΐ 47”. A lektor gyanúja szerint a φωσφόρος ilyen gyakorisággal nem áll az LXX-ben. Ellenőrzés a nyers `lxx_bridge`-ből és egy LXX-szövegből.
- **N-F231b — `strong_szotar`, G0264 kiejtés:** „hamartēsē”, a szótári alak hamartanō. Forrásból ellenőrizendő, és meg kell mérni, hány görög sort érint.
- **N-F231c — a görög „Ebben a versben” blokk** (alaktani kulcs).

## 6. Döntésnapló

- DT-F231a (⛔ M0): a kártyamodell forrása, (a) `lapgen` vagy (b) saját modell egyezési teszttel.
- Ez a feladat az F213 3. pontját („használati sorok: szerkezet → magyar magyarázat → igehelyek”) felváltja a szakaszonként egybefüggő szöveggel. A felhasználó 2026-11-21-i ítélete: „az md lapon jobb a szeletelő”. A DT-tétel ezt rögzíti.
- DT897: fordítótábla a feliratokhoz (a #231 és a #233 közös szabálya, a felhasználó 2026-11-22-i döntése).
