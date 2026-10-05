---
feladat: 42
cim: Forrásfájlok kivezetése és a licencállapot egyetlen forrása
kod: FORRASKIVEZETES
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: fut
ag: claude/forraskivezetes
ad: A TBESH-család a gitignore-olt _nyers/ alatt, letöltő szkripttel. Az LXX_kivonat kivezetve. A generátor licencjelölése az adat/licencek.tsv-ből olvas.
kovetkezo: "M1–M8 a DT-F42a–i szerint; az M5 a #43 merge-e után"
fugg: [33, 35]
olvas: [adat/licencek.tsv, adat/SEMA.md, adat/lexikon_hivatkozasok.tsv, DONTESEK.md, NYITOTT_FELADATOK.md, konkordancia/README.md, .gitignore]
ir: [eszkozok/forras_letolt.py, eszkozok/utvonalak.py, eszkozok/cremer_ocr_javit.py, eszkozok/istentiszt_2b_d1_toltes.py, eszkozok/kockazat_szures_18_tanulmany.py, eszkozok/lexikon_general.py, eszkozok/tbesh_konszolidalt_import.py, konkordancia/TBESH.txt, konkordancia/lexikonok_nyers/TBESH.lexicon, konkordancia/TBESH_konszolidalt.tsv, konkordancia/README.md, adat/licencek.tsv, adat/lexikon_hivatkozasok.tsv, adat/SEMA.md, NYITOTT_FELADATOK.md, DONTESEK.md, naplok/FORRASKIVEZETES_M0.md, naplok/FORRASKIVEZETES_zaras.md, naplok/ELLENOR_FORRASKIVEZETES.md, .gitignore, eszkozok/lekerdez.py, eszkozok/t1_teremt002_munkalap.py, eszkozok/lxx_osszevetes.py, eszkozok/lxx_kivonat_fetch.py, eszkozok/lxx_kivonat_fetch_v2.py, eszkozok/f08/f08_dontesek.py, eszkozok/f08/f08_dt_sor.py, eszkozok/f17/macula_import.py, eszkozok/istentiszt_2b_d3_szerkeszt.py, "konkordancia/LXX_kivonat_*.tsv", konkordancia/LXX_kivonat_README.md]
---

# Forrásfájlok kivezetése és a licencállapot egyetlen forrása

A feladatszámot a `/befogad` adja. Az ágon a helyőrzők `DT-F<nn>` és `N-F<nn>` alakúak.

## Miért egy menet

Két javasolt tétel van összevonva:

- **N-F33:** a forrásfájlok kivezetése (#33);
- **N9:** a licencállapot egyetlen forrása.

Mindkettő ugyanazokat a fájlokat érinti: a `lexikon_general.py`-t, az `adat/licencek.tsv`-t és a SEMA 2.19-et. Külön menetben kétszer kellene ugyanazt a kódot és a render-diffet átnézni.

## Kiinduló döntések (nem kell újra eldönteni)

- **DT-F24:** a `tisztazott` állapothoz szó szerinti licencidézet kell. A korlátozott licencű nyers fájl csak a gitignore-olt `_nyers/` alá kerülhet. A repó nyilvános marad.
- **DT-F33a:** a TBESG marad a repóban. A három TBESH-fájl (`TBESH.txt`, `TBESH.lexicon`, `TBESH_konszolidalt.tsv`) a `_nyers/` alá kerül, mert az Online Bible-záradék tisztázatlan.
- **DT-F33b:** az `LXX_kivonat` olvasói az `LXX_OS`-re állnak át, utána a fájl törlődik.
- **DT-F33c:** a forrásrepó README-je csak akkor licencforrás, ha a jogtulajdonos saját, szó szerinti nyilatkozata, és lefedi az adott fájlt.
- **DT-F33d:** az értékkészlet `tisztazott` / `kozkincs` / `tisztazatlan`. A TBESH és a BDB `tisztazatlan`, a KJV_Strongs_teljes `kozkincs`.
- **Git-történet:** a mozgatott fájlok a korábbi commitokban megmaradnak. A történetet nem írjuk át, ezt csak rögzítjük (lásd M7).

## Hatókör

**Benne van:**

- a TBESH-család áthelyezése, letöltő szkripttel;
- az olvasók átírása;
- a `forrasfajl` mezők átírása;
- a származtatott tartalom felmérése;
- az `LXX_kivonat` kivezetése;
- a KJV Strong-címkéinek licencellenőrzése;
- az N9 megoldása;
- a render-diff.

**Nincs benne:**

- a BDB licencének tisztázása (külön tétel);
- a többi sor átsorolása `kozkincs`-ra;
- az N-F33b ellenőrző szabály (ez a #30, #37 és #40 köre);
- a lexikonoldalak tartalmi átírása, kivéve az M0-ban jóváhagyott Online Bible-eredetű szövegeket.

## Lépések

### M0 — Felmérés, és egyetlen ⛔ megállás minden kérdéssel

Jelentés: `naplok/FORRASKIVEZETES_M0.md`.

1. Az olvasók teljes listája, minden fájlra: a TBESH-család három fájlja és az `LXX_kivonat` összes fájlja. Grep a teljes repón: `eszkozok/`, `tests/`, a workflow-k, a `.md`-ben lévő parancsok. A listában szerepeljen a fájl, a sor, és hogy olvasásról vagy csak említésről van-e szó.
2. A CI és a tesztek függése: melyik teszt vagy CI-lépés olvassa ezeket a fájlokat, és mi történik, ha a fájl hiányzik.
3. A `TBESH.lexicon` eredete: honnan származik, és letölthető-e rögzített forrásból (URL, commit). Ha nem, ezt rögzítsd. Ilyenkor a fájl csak helyben él, és az olvasói a hiányát kezelik.
4. **A származtatott tartalom felmérése (a legfontosabb rész).** Került-e Online Bible-eredetű szöveg (a TBESH rövid meghatározásai) nyilvános, verziózott helyre? Átnézendő:
   - `adat/lexikon_hivatkozasok.tsv` (különösen a `forditas_hu` mező és az `istentiszt_2b_d1_toltes.py` által írt sorok);
   - a `lexikon/*_TUDOMANYOS.md` oldalak;
   - a törzscikkek;
   - a `generalt_proba/` könyvtár.

   Minden találatnál rögzítsd:
   - a helyet;
   - a szöveget, legfeljebb az első 15 szóig;
   - hogy szó szerinti átvétel vagy saját fordítás;
   - hogy van-e más forrásból (BDB, TBESG) azonos tartalmú helyettesítő.
5. Az N9 leképezése: a `lexikon_general.py` szótárkulcsai (a `TISZTAZATLAN_SZOTARAK` és a licenc-konstans) hogyan felelnek meg az `adat/licencek.tsv` sorainak. Melyik kulcsnak nincs sora, és melyik sornak nincs kulcsa?
6. A KJV Strong-címkék: az eBible `eng-kjv_usfm.zip`-ben lévő Strong-címkézés eredete (CrossWire vagy más), és az eredet licencnyilatkozata szó szerint, ha elérhető.

**⛔ Megállás.** Az összes kérdés egy csokorban, minden kérdésnél javaslattal és alternatívával. Várható kérdések:

- **(a)** Mi legyen az Online Bible-eredetű szövegekkel? Javaslat: a lehetőségek
  - kiváltás BDB- vagy TBESG-alapú szöveggel, ahol van megfelelő;
  - saját átfogalmazás;
  - törlés.
- **(b)** Ha a `TBESH.lexicon` nem tölthető le: elég-e, hogy csak helyben él, és az olvasók hiányra jeleznek?
- **(c)** Ha teszt függ a fájloktól: a teszt hiányzó fájlnál kihagyással fusson, vagy a CI futtassa a letöltő szkriptet?
- **(d)** Ha a KJV Strong-címkéinek licence eltér: a sor visszakerül `tisztazatlan`-ra?

### M1 — Letöltő szkript

Új fájl: `eszkozok/forras_letolt.py`.

- A STEPBible-Data `b99716b` állapotából letölti a `TBESH.txt`-t a `konkordancia/_nyers/stepbible/` alá.
- A letöltést sha256-tal ellenőrzi. Az ellenőrzőösszeg a szkriptben vagy egy kis manifest-fájlban áll.
- Ha az M0 szerint letölthető, a `TBESH.lexicon`-t is letölti.
- A `TBESH_konszolidalt.tsv`-t nem tölti le, hanem a `tbesh_konszolidalt_import.py` generálja újra a `_nyers/` alá.
- Idempotens: ha a fájl már megvan és az ellenőrzőösszeg egyezik, nem tölt le újra.
- Friss klónban, a cloud sessionben és szükség esetén a CI-ben is fut.

### M2 — Áthelyezés és közös útvonal-konstans

- A három fájl a `konkordancia/_nyers/` alá kerül, a `.gitignore` ezt lefedi.
- Minden olvasó egy közös konstansból veszi az útvonalat (`eszkozok/utvonalak.py` vagy a meglévő közös modul).
- Ha a fájl hiányzik, az olvasó egyértelmű hibát ad, amely a letöltő szkriptre mutat. Csendes kihagyás vagy üres eredmény nem lehet.

### M3 — A `forrasfajl` mezők

- Az `adat/lexikon_hivatkozasok.tsv` és minden más tábla `forrasfajl` mezője az új útvonalra mutat.
- A cseréhez a mező kulcsa alapján készülő csere-tábla kell, nem sorszám alapú.
- A jelentésben szereplő darabszámot a végső mezőtartalom megszámolásából kell venni, nem a csereszkript kimenetéből. A korábbi tanulság szerint a csereszkript egy kulcs több sorát némán eldobhatja.

### M4 — A származtatott tartalom

Az M0 ⛔ döntése szerint. Minden javítás a forrásrétegben történik, utána render.

### M5 — Az `LXX_kivonat` kivezetése

- Az olvasók átállnak az `LXX_OS`-re.
- Ahol a két forrás eltérő eredményt ad, az eltérést fel kell sorolni a jelentésben. Csendben nem simítható el.
- Utána a fájl törlődik.
- A `licencek.tsv` sora megszűnik vagy `kivezetve` megjegyzést kap. A SEMA értékkészlete szerint kell eljárni, új állapotérték nem jön létre.
- A `konkordancia/README.md` „kivezetésre vár” szakasza lezárul.

### M6 — N9: a licencállapot egyetlen forrása

- A `lexikon_general.py` az `adat/licencek.tsv`-ből olvassa a licencállapotot.
- A `TISZTAZATLAN_SZOTARAK` és a kódban lévő licenc-konstans megszűnik.
- A leképezés:
  - `tisztazott` és `kozkincs`: nincs tisztázatlan-jelölés;
  - `tisztazatlan`: van jelölés.
- Ha egy szótárkulcsnak nincs sora a `licencek.tsv`-ben, a generátor hibát ad. Alapértelmezett érték nem lehet.
- A SEMA 2.19-be bekerül, hogy a generátor licencjelölése a `licencek.tsv`-ből származik.
- Az N9 lezárul a `NYITOTT_FELADATOK.md`-ben.

### M7 — Ellenőrzés és render-diff

- Futtatandó: `general.py --cel lexikon`, a törzscikkek és a futtató ellenőrzés.
- A diff minden eltérése kategóriába kerül:
  - **várt licencjelölés-változás:** például a BDB-réteg most tisztázatlan-jelölést kap a 8 oldalon, a KJV-ből közkincs lett;
  - **M4 szerinti tartalomcsere;**
  - **nem várt eltérés:** ilyen nem lehet. Ha mégis van, a menet megáll.
- A git-történet döntése bekerül a `DONTESEK.md`-be (`DT-F<nn>` helyőrzővel): a TBESH-fájlok a korábbi commitokban megmaradnak, a történet nem íródik át.

### M8 — Zárás (a menetzárási szabály szerint)

1. A `fuggetlen-ellenor` ügynök lefut. A jelentése: `naplok/ELLENOR_FORRASKIVEZETES.md`, commitolva.
2. Push.
3. Draft PR a `main`-be.
4. A záró összefoglaló első sora a PR linkje és a CI állapota.
5. A brief fejlécében az állapot `lezarva`. Meglévő címsor szövege nem változik, az állapotváltozás a címsor alá kerül.

## Elfogadási feltételek

- **K1.** A repó fájlfáján (`git ls-files`) nincs TBESH-fájl, és nincs `LXX_kivonat`.
- **K2.** Friss klónban a `forras_letolt.py` után minden olvasó hibátlanul fut.
- **K3.** Ha a fájl hiányzik, minden olvasó a letöltő szkriptre mutató hibát ad.
- **K4.** A CI zöld, és az M0 (c) döntése szerint kezeli a fájlfüggést.
- **K5.** Nincs `forrasfajl` mező, amely nem létező útvonalra mutat. A darabszám a végső mezőtartalomból számolva.
- **K6.** A nyilvános rétegben nincs jóváhagyás nélküli Online Bible-eredetű szövegátvétel.
- **K7.** A `lexikon_general.py`-ban nincs licenc-konstans. A licencállapot egyetlen forrása a `licencek.tsv`, és a hiányzó sor hibát ad.
- **K8.** A render-diffben nincs nem várt kategória.
- **K9.** A KJV Strong-címkéinek licence idézve van, vagy a sor az M0 (d) döntése szerint átsorolva.
- **K10.** A futtató ellenőrzés HIBA 0. A független ellenőr eltérés nélkül zár, vagy az eltérései javítva vannak.

## Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-02 | Az N-F33 és az N9 egy menetben fut, mert közös fájlokat érintenek. | chat |
| v1 | 2026-10-02 | A TBESH-család a `_nyers/` alá kerül, letöltő szkripttel (STEPBible-Data `b99716b`, sha256). | DT-F33a |
| v1 | 2026-10-02 | A git-történet nem íródik át, ezt csak rögzítjük. | chat |
| v1 | 2026-10-02 | Az `LXX_kivonat` kivezetése ebbe a menetbe kerül. | DT-F33b |
| v1 | 2026-10-02 | A KJV Strong-címkéinek (CrossWire) licencellenőrzése bekerül. | #33 nyitott pontja |
| v1 | 2026-10-02 | A licencjelölés a `licencek.tsv`-ből jön; a hiányzó sor hibát ad, nincs alapértelmezett érték. | N9 |
| v1 | 2026-10-02 | Egyetlen ⛔ megállás van (M0), minden kérdés egy csokorban. | munkamód |

## Nyitó prompt

<!-- KOZVETLEN_FUTTATAS -->
Olvasd el ezt a briefet és a fejlécben az `olvas` alatt felsorolt fájlokat. Futtasd az M0-t, írd meg a `naplok/FORRASKIVEZETES_M0.md` jelentést, commitold, és állj meg ⛔: az összes kérdést egy csokorban tedd fel, mindegyiknél javaslattal. Jóváhagyás után az M1–M8 lépések sorban, egy menetben futnak. Commit minden lépés után, a lépés kódjával az üzenetben. A végén a zárási szabály szerint zárj: független ellenőr, push, draft PR, az összefoglaló első sora a PR linkje és a CI állapota.
<!-- KOZVETLEN_FUTTATAS -->
