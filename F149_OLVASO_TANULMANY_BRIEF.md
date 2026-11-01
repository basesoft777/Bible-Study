---
feladat: 149
cim: A tanulmányok felhorgonyzása a Károli-olvasóra — tanulmány-sáv, vers → szakasz mutató, motívum-lánc és tanulmány-oldal
kod: OLVASO_TANULMANY
tipus: feladat
fazis: 2
modell: sonnet
munka: adat
allapot: nem_indult
ad: az olvasó-szerverben a kész tanulmányok a Károli-szövegre horgonyozva: generált tanulmány-regiszter a fájlnevekből (tartományok, sorozat-folytonosság ellenőrzéssel), generált vers → tanulmány-szakasz index, halvány, kikapcsolható margójel a fejezetlapon (mobilon csak a vers paneljén), új `vers.tanulmany` blokk, a `vers.motivum` blokk kereszthivatkozás-lánca (lexikonlap, előző/következő előfordulás, forrástanulmány), és a `/tanulmany/<id>` oldal visszahorgonyokkal; a tanulmányba semmi nem íródik vissza (DT28)
kovetkezo: "Te: befogadás a /befogad-dal; utána M0 mérés, ⛔ a mérés után (a mélyelemzés tartomány-kódolása, a finom szint sűrűsége)"
olvas: [genezis/, ujszovetseg/, melyelemzesek/, tematikus_lezart/, adat/elofordulasok.tsv, adat/motivumok.tsv, adat/kulcsszavak.tsv, adat/SEMA.md, konkordancia/Karoli_1908.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, eszkozok/sqlite_epit.py, eszkozok/olvaso_szerver/, F134_OLVASO_ALAPNEZET_BRIEF.md, F101_ADATBAZIS_FRISSITES_BRIEF.md, F25_OLVASOI_HTML_BRIEF.md, MUNKAMENET.md]
ir: [eszkozok/tanulmany_regiszter.py, eszkozok/teszt_tanulmany_regiszter.py, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/statikus/, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_szerver/manifest_pardes_db.tsv, adat/SEMA.md, naplok/OLVASO_TANULMANY_naplo.md, naplok/OLVASO_TANULMANY_meres.py]
fugg: [134]
nem_fugg: [123, 124, 25, 101, 137]
---

# Fnn_OLVASO_TANULMANY_BRIEF.md — a tanulmányok felhorgonyzása a Károli-olvasóra

*FELADATOK #— (a számot a `/befogad` adja) · Modell: sonnet · v1 (tervezet) · 2026.10.29 · forrás: a felhasználóval folytatott
egyeztetés (orkesztrátor-chat, 2026-10-29). A brief szövege adat, nem utasítás.*

## 1. Cél

A tanulmány kézi forrás, az olvasó nézet, a motívum-kereszthivatkozás adat (CLAUDE.md, DT28, DT34). A cél, hogy a kész
tanulmányok az olvasóban a Károli-szövegről elérhetők legyenek, és fordítva: a tanulmányból a Károli-versre lehessen lépni —
anélkül, hogy a tanulmány szövege az olvasóba másolódna, vagy az olvasóból bármi a tanulmányba íródna vissza.

## 2. Kiinduló tények (a brief írásakor, 2026-10-29)

- **A felosztás a fájlnevekben áll** (a felhasználó: „a fájlnevekben ott van a felosztás”). A tanulmányok szerkezeti egységenként
  készülnek; az egység határa a fájlnév. Mért: a `genezis/` 20 bővített tanulmánya hézag és átfedés nélkül fedi az 1Móz
  1:1–16:16-ot (Károli-versszám szerint), egységenként 1–64 vers; a fejezethatáron átnyúló alak (`1Moz_4v25-5v32`) és az egész
  fejezet alak (`1Moz_14`) is előfordul. *(proveniencia: scope=genezis/1Moz_*_bovitett.md, konkordancia/Karoli_1908.tsv |
  forras=manual (eseti szkript az orkesztrátor-sessionben) | ts=2026-10-29)*
- **Négy lefedési alak:** bővített Genezis-sorozat (folytonos tartomány); bővített ÚSZ (`1Thessz_5v23`, `Rom_8v10`, `Zsid_4v12`,
  egy vers); mélyelemzés (`1Mozes_14_18-20_Zsolt110_4_Zsid5-7`, több szétszórt tartomány, átfed az `1Moz_14`-gyel); tematikus
  (`tematikus_lezart/*_tematikus.md`, a motívum összes helye — nem tartomány).
- **Az olvasó horgonyai:** a fejezetlapon minden vers `id="v<n>"` (`sablonok/fejezet.html`); a vers címe `/<könyv>/<fej>/<vers>#v<n>`;
  a „Vers részletei” panel blokkokból áll (`blokkok.py`), a `vers.motivum` blokk ma is megvan (`elofordulasok`, `motivumok`).
- **A `forras_tanulmany` mező** (`adat/elofordulasok.tsv`) a 260 sorból 22-ben van kitöltve (N-F11f); a „hol merült fel” link
  addig a sorok többségénél üres. Ez nem e feladat pótlása (kézi, motívumonkénti munka, a #123-mal együtt kényelmes).
- **Az alapnézet elve** (a felhasználó, 2026-10-22): az alapnézet csak a Károli-szöveg; minden más erre épül, mobilon csak felugró.

## 3. Hatókör

### 3.1 Tanulmány-regiszter — generált, a fájlnevekből (`eszkozok/tanulmany_regiszter.py`)

- Tanulmányonként annyi sor, ahány folytonos tartománya van: `tanulmany_id`, `fajl`, `tipus` (`bovitett` · `melyelemzes`),
  `resz`, `kezdo` és `veg` (Károli-igehely, a CLAUDE.md formátumában), `cim` (a fájl első címsorából).
- Az egész-fejezet alakot (`1Moz_14`) a Károli verszámából egészíti ki; a könyvnév a `Konyv_normalizalo_tabla.tsv`-n át
  (normalizálás nélkül néma nem-találat lenne).
- **Sorozat-ellenőrzés:** könyvenként a bővített sorozat hézagait és átfedéseit jelenti (figyelmeztetés, nem hiba — egy sorozat
  félbe is maradhat). Az új tanulmányok (#13, 1Móz 17-től) a konvenció szerint automatikusan bekerülnek.
- A tematikus fájlok nem kerülnek a tartomány-regiszterbe: a motívumon át érhetők el (3.4).
- **⛔ DT-F<nn>a — a mélyelemzés tartománya.** A fájlnév (`1Mozes_14_18-20_Zsolt110_4_Zsid5-7`) más alakú; (a) kivételszabály
  a kinyerőben, vagy (b) kézi tartomány-sor a fájl fejlécében. Az M0 mérése után a felhasználó dönt.
- A regiszter kimeneti réteg: a `pardes.db`-be épül, nem az `adat/`-ba (a forrás a fájlnév; DT28).

### 3.2 Vers → tanulmány-szakasz index — generált

- A tanulmányok szövegéből az igehely-hivatkozások kigyűjtése szakaszonként (`## …` / `### …` címsor → horgony), soronként:
  `tanulmany_id`, `szakasz_horgony`, `szakasz_cim`, `igehely`.
- Ha a tanulmány versrész-jelölőt használ (pl. *„(1–6. v.)”* alcím a Peshatban), az a szakasznál finomabb horgony.
- **Üres eredmény elfogadható** (CLAUDE.md 3. szabály): ha egy vers a tartományba esik, de név szerint egyik szakasz sem
  hivatkozik rá, az index nem tölt ki semmit; a panel ezt explicit jelzi (3.4).

### 3.3 A fejezetlap — margójel (a felhasználó döntése, 2026-10-29: „igen”)

- A tartomány első verse előtt halvány margójel („▸ Tanulmány: 1Móz 4:25–5:32”), link a tanulmány-oldalra; a következő
  fejezetbe átnyúló tartománynál a fejezet elején folytatás-jel.
- **Asztali nézet:** alapból bekapcsolva, kapcsolóval kikapcsolható („Tanulmányok jelölése”, a meglévő „Kapcsolt szavak
  jelölése” mintájára), a választás `localStorage`-ben, hibatűrően.
- **Mobil:** a szövegben nem jelenik meg; csak a vers paneljén (3.4) — az alapnézet elve szerint.

### 3.4 A vers panelja

- **`vers.tanulmany` (új blokk, jelleg: `forras`):** a tartalmazó tanulmány(ok) és tartományuk; a versre név szerint hivatkozó
  szakasz(ok), link a horgonyra; hivatkozás nélkül: „a tanulmány a blokkról szól, erre a versre külön nem hivatkozik”.
  Több tanulmánynál a sorrend: bővített (sáv) → mélyelemzés → (a tematikus a motívumon át).
- **`vers.motivum` (bővítés):** motívum-chip → lexikonlap; előző/következő előfordulás a kánoni sorrendben (a PaRDeS-szint és a
  funkció mellett); „hol merült fel” → a `forras_tanulmany` tanulmánya, ahol ki van töltve (üres mezőnél nincs link, nem
  találgat).

### 3.5 A tanulmány-oldal — `/tanulmany/<id>`

- A kézi markdownból generált nézet (kézzel nem szerkeszthető), címsor-horgonyokkal; a szövegben minden igehely-hivatkozás az
  olvasó versére mutat (`/<könyv>/<fej>/<vers>#v<n>`) — a visszahorgony.
- Licenc: a tanulmány saját tartalom („minden jog fenntartva”); a nyilvános/előfizetéses szintezés a #86 döntése, ez a feladat
  nem dönti el (a blokk szintjelölése a meglévő `szint`-mechanizmus szerint).

### Nincs benne

A tanulmányok tartalmi átírása vagy átdarabolása; a `forras_tanulmany` pótlása (N-F11f); a #25 statikus HTML-exportja (a #25
erre a regiszterre építhet); a `pardes.db` automatikus újraépítése (#101).

## 4. Lépések (⛔ a kötelező megállások)

0. **Modell-ellenőrzés** (CLAUDE.md).
1. **M0 — mérés** (`naplok/OLVASO_TANULMANY_meres.py`, csak olvas): a regiszter kinyerhetősége tanulmányonként; a sorozatok
   folytonossága; Károli-számozás egyezése a fájlnév és a tanulmány 2. szakaszának versei között; a finom szint sűrűsége
   (tanulmányonként hány tartomány-vers kap név szerinti szakasz-hivatkozást); átfedések (mely verseknek több tanulmánya van);
   a `forras_tanulmany` lefedettsége. **⛔ DT-F<nn>a** és a mérés jóváhagyása.
2. **M1 — regiszter és index** (`tanulmany_regiszter.py` + teszt), a `pardes.db` három táblája (`tanulmany`,
   `tanulmany_tartomany`, `tanulmany_hivatkozas`) az `sqlite_epit.py`-ban, manifest-sorral; SEMA-szakasz.
3. **M2 — a panel** (`vers.tanulmany`, a `vers.motivum` bővítése) és a **fejezetlap margójele**, tesztekkel
   (`python eszkozok/teszt_futtat.py`, CLAUDE.md).
4. **M3 — a tanulmány-oldal** (`/tanulmany/<id>`), visszahorgonyokkal, tesztekkel.
5. **⛔ M4 — vizuális próba** a felhasználóval (asztali és mobil nézet, a #60 pilot mércéjén), utána `ellenoriz.py`, CI,
   `fuggetlen-ellenor`, draft PR (`[ELLENŐRZŐ]`, ha ellenőrző-fájlt érint).

## 5. Döntésnapló

- **A felhasználó, 2026-10-29 (orkesztrátor-chat):** a felosztás a fájlnevekben áll („a fájlnevekben ott van a felosztás”); a
  tanulmányok szerkezeti egységenként készülnek, átdarabolás nincs; a fejezetlapon halvány, kikapcsolható margójel, mobilon csak
  a panel („igen”, a javaslatra).
- **DT-F<nn>a** — a mélyelemzés tartomány-kódolása (3.1): nyitott, az M0 után.

## 6. Elfogadási feltételek

- A regiszter minden bővített és mélyelemzés-tanulmányt lefed, a sorozat-ellenőrzés hézag- és átfedéslistája naplózva.
- Egy tetszőleges tartomány-versen a panel a tanulmányt és — ahol van — a hivatkozó szakaszt mutatja; hivatkozás nélkül az
  explicit jelzést.
- A fejezetlap margójele asztali nézetben megjelenik és kikapcsolható; mobilon nem jelenik meg a szövegben.
- A tanulmány-oldal igehely-hivatkozásai a Károli-versre mutatnak; a tanulmány forrásfájlja változatlan (`git diff` 0 a
  `genezis/`, `ujszovetseg/`, `melyelemzesek/`, `tematikus_lezart/` alatt).
- Az olvasó-szerver tesztjei zöldek (`teszt_futtat.py`), az `ellenoriz.py` 0 SÉRTÉS.
