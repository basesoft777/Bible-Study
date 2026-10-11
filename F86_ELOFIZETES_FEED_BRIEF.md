---
feladat: 86
cim: Előfizetéses adatcsomag (feed): szintek, szállítás, eseménycsatorna
kod: ELOFIZETES_FEED
tipus: feladat
fazis: 2
modell: opus
allapot: dontesre_var
ad: rögzített döntések az előfizetési szintek határáról, a prémium réteg szállításáról és lejáratáról, valamint az eseménycsatornáról; ezekre épül a csomag-generátor és a böngészős kliens
kovetkezo: "Te: döntés a DT-F86a–g pontokról (5. szakasz), utána a 3.1 lépés"
munka: folyamat
olvas: [adat/SEMA.md, adat/forditasok.tsv, adat/szotar_szerepek.tsv, adat/motivumok.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv, ADATVAGYON_TERV.md, ATALAKITASI_TERV.md.md]
ir: [adat/SEMA.md, eszkozok/feed_epit.py]
fugg: [79, 76]
---

# F86_ELOFIZETES_FEED_BRIEF.md — Előfizetéses adatcsomag (feed)

*FELADATOK #86 · Modell: opus · v1 · 2026.10.11 · chatben készült javaslat, a `/befogad` fogadja be*

## 1. Cél

Az előfizető böngészőjébe **verziózott adatcsomag** érkezik, freemium vagy prémium mélységben. A csomag két dolgot hoz: **adatot** (snapshot + delta) és **eseményeket** (mi történik a projektben: új jelölt, folyamatban lévő motívum, lezárás, rögzített kapcsolat). A feed ugyanannak az adatnak egy újabb nézete. Az adatból generálódik, nem kézzel készül (fő szabály, DT28 egyirányúság).

A brief első része **döntés-előkészítés**: hét döntési pont (5. szakasz), és mindegyik a felhasználóé. A megvalósító lépések (3.1–3.4) csak a döntések után indulnak.

Szemléltető vázlat (minta, nem specifikáció): a „PaRDeS műhely" artifact (https://claude.ai/artifact/WQKzU22twqFMDHqm4oWHbi). OS-szerű felület, középen a valódi motívumháló (a „Motívumháló 3D" adata, 2026.10.08), amely a 0 állapotból épül fel. Mellette Feladatkezelő a nyitott folyamatokkal, értesítések, freemium/prémium kapcsoló. A lépések menete benne szimulált.

## 2. Hatókör

**Benne van:**
- a szintek határa;
- a prémium réteg szállítása, védelme és lejárata;
- az eseménycsatorna szabályai;
- a csomag- és eseménynapló-séma;
- a generátor;
- a böngészős kliens (PWA) prototípusa.

**Nincs benne:**
- a fizetési rendszer és az árazás;
- a kereskedelmi licencelés jogi véleménye (DT-F33j, jogász);
- a #76 (#25a) olvasói konkordancia felülete, a #79 SQLite-építés (ezekre épül);
- az OS-mód végleges felülete (a DT-F86f szerint később).

## 3. Lépések

- **3.0** ⛔ A felhasználó dönt a DT-F86a–g pontokról. A döntések a `DONTESEK.md`-be kerülnek.
- **3.1** Szint-mező a sémában. A SEMA-ban mezőszinten rögzítjük, melyik adat `olvasoi`, `apparatus` vagy `belso` (D34), és melyik forrás melyik szintre mehet (DT-F86c). Ha egy mezőről nem dönthető el a szint, nem kerül csomagba. ⛔ A szint-táblát a felhasználó jóváhagyja.
- **3.2** Eseménynapló-séma. Az események a `main`-re került tételekből és a táblák különbségéből generálódnak. Mezők: `seq`, `ts` (valódi), `tipus`, `targy`, `allapot`, `szint`, `proveniencia`. Kis minta egy valódi merge-ből. ⛔ A minta jóváhagyása.
- **3.3** `eszkozok/feed_epit.py`. Snapshot és delta két tag között, a szintek szerint **build-időben** szétválasztva. A manifest mezői: `verzio`, `elozo_verzio`, `szint`, `sha256`, `licenc`, proveniencia. Determinisztikus: újrafuttatva azonos kimenetet ad. Független ellenőr (`fuggetlen-ellenor`).
- **3.4** PWA-prototípus. Service Worker, IndexedDB/OPFS, sqlite-wasm, Web Crypto, `navigator.storage.persist()`. Rétegek összerakása, delta alkalmazása, le- és felváltás. ⛔ Bemutatás.

## 4. Elfogadási feltételek

- A freemium csomag **nem tartalmaz** prémium vagy `belso` adatot: build-idejű kizárás, ellenőrző szkript igazolja (nem kliensoldali rejtés).
- A freemium csomagban nincs sor az `adat/forditasok.tsv`-ből (DT-F86c).
- BY-SA-eredetű tartalom nincs zárt prémium rétegben (DT-F86c).
- Minden esemény valódi időbélyeggel és proveniencia-sorral jön. Ahol szimulált elem van (pl. bemutató), az jelölve van.
- A delta-lánc megszakadásakor a kliens teljes snapshotra vált.

## 5. Döntésnapló

| Tétel | Kérdés | Javaslat | Állapot |
|---|---|---|---|
| **DT-F86a** | Hol a freemium/prémium határ? | A D34 szintekre képezve. **Freemium = `olvasoi`:** Károli 1908 + Strong-kulcs, Károli-megfelelők, konkordancia, motívum-kivonat, a háló alakja (csomópontok, élek részletek nélkül). **Prémium = `apparatus`:** a kereszthivatkozás-gráf részletekkel (`gerinc_elem`, közös igehely), ★ leletek, `_TUDOMANYOS` lexikonoldal, a döntések indoklása, kizárások. **`belso`:** soha, egyik szinten sem. | javaslat |
| **DT-F86b** | Hogyan jut el a prémium réteg a klienshez? | **Összeadható rétegcsomagok** (alap + prémium réteg, közös azonosítókkal), nem titkosított teljes csomag. Felváltáskor csak a prémium réteg töltődik le, leváltáskor törlődik. Offline: titkosított gyorsítótár, nem exportálható `CryptoKey`, bérleti idő (pl. 30 nap türelmi idő), előfizetőnkénti vízjel. Alternatíva: a prémium csak szerveroldali lekérdezés (ADATVAGYON_TERV 3.), offline nélkül. | javaslat |
| **DT-F86c** | Milyen forrás mehet melyik szintre? | **Saját fordítás nem freemium:** az `adat/forditasok.tsv` (BDB, Thayer, TBESH, TBESG, LSJ, UBS_DNTG) egyetlen sora sem kerül a freemium csomagba. **BY-SA-eredetű tartalom nem zárható:** a Louw–Nida (UBS_DNTG) és az SDBH, a fordításukkal együtt, vagy nyílt mellékcsomagban megy, vagy kimarad, zárt prémium rétegben nem lehet (CC 4.0: tilos a technikai korlátozás, a ShareAlike továbbviszi a licencet). | javaslat |
| **DT-F86d** | Mi mehet ki a jelöltekből és a kizárásokból? | Az állapotcsatorna a `belso` munkaanyagból **csak összesítve** mutat: állapot, darabszám, munkacím. A kizárások indoklással `apparatus` (prémium). A nyers indoklás, a nyitott jegyzetek és a jelöltlista `belso` marad. Mezőlista a 3.1-ben. | javaslat |
| **DT-F86e** | Az eseménycsatorna ütemezése és hitelessége | Delta **minden main-merge után**, valódi dátummal, nincs színlelt élő lejátszás. Az elő-scan nem lelet: a szöveg a folyamatot nevezi meg („vizsgálat alatt"), nem az eredményt. Az elvetett jelöltek is megjelennek. Prémium: merge-enkénti delta. Freemium: heti összesítő. | javaslat |
| **DT-F86f** | Milyen felület kell, és milyen sorrendben? | **PWA, natív app nem kell.** Sorrend: (1) eseménynapló-séma és delta-generátor; (2) „Mi történik a projektben" panel a #76 hagyományos oldalain; (3) OS-mód („műhely-nézet") választható nézetként, amikor kb. 15–20 motívum van, és látható az ütem. A 3D háló a kirakat, a navigáció 2D-ben vagy listában történik. | javaslat |
| **DT-F86g** | Mi történik megújításkor és lejáratkor? | Lejáratkor nincs több prémium delta. A türelmi idő végén a prémium réteg olvashatatlan, és a kliens törli. A már kimentett adat befagyott pillanatkép marad; ezt a felhasználási feltételek és a vízjel kezeli. Döntendő: a türelmi idő hossza, és hogy leváltáskor azonnal törlődjön-e. | javaslat |

**Nyitott tételek:**

| Tétel | Leírás |
|---|---|
| **N-F86a** | A BDB és a TBESH licencállapota `tisztazatlan` (F42). A BDB-fordítás terjesztése a szinttől függetlenül nyitott; ezt a kereskedelmi döntéskor a jogásznak meg kell néznie (DT-F33j). |
| **N-F86b** | Az adatvagyon SQLite-méretét le kell mérni (#79), mielőtt a csomagméretről és az első letöltés hosszáról döntünk (ADATVAGYON_TERV 3.). |
| **N-F86c** | iOS Safari: a nem telepített oldalak tárhelyét 7 nap használaton kívüli idő után törölheti. A prémium felhasználónál ezért telepített PWA-ra kell terelni; a kliensnek kezelnie kell a tárhely elvesztését (teljes snapshot újra). |
