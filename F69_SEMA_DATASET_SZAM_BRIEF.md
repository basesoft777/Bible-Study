---
feladat: 69
cim: A SEMA 2.6 elavult darabszámának frissítése a datasetek.tsv alapján
kod: SEMA_DATASET_SZAM
tipus: feladat
fazis: folyamat
munka: folyamat
modell: haiku
allapot: nem_indult
ad: az adat/SEMA.md 2.6 bevezető mondata, a `dataset` mező sora és a `hianyzik`-mondat a datasetek.tsv futáskor mért értékeit mondja (2026-10-19-én: „30 dataset, 117 sor: 29 × 4 + az OSHL_lexikalis_index egy lexikon_oldal-sora”, 30 érték, 4 `openbible_crossrefs`-sor `hianyzik`), DT248 szerint; a SEMA más szakasza nem változik
kovetkezo: "a /kovetkezo indítja (DT248 eldöntve, 🟢)"
olvas: [adat/datasetek.tsv, adat/SEMA.md]
ir: [adat/SEMA.md]
fugg: []
nem_fugg: []
---
# F69_SEMA_DATASET_SZAM_BRIEF.md — a SEMA 2.6 elavult darabszámai

*FELADATOK #69 · Modell: haiku · v2 · 2026.10.19 (v2: DT248 döntése átvezetve) · előzmény: #56 zárójavaslata (b) (`naplok/F56_zaras.md`, „Nyitott javaslatok”), DT7 (f) (a SEMA 2.6 két mondata „a végleges datasetszámra frissül”)*

## 1. Mért állapot (main, `1a6a6eef`, 2026.10.19)

**Mérés:** `adat/datasetek.tsv` (sha256 eleje `b09d49aadf7f`), `split('\t')`-alapú olvasással (nem `csv`), a `#` kezdetű sorok és a fejlécsor nélkül. Proveniencia: `scope=adat/datasetek.tsv teljes | forras=adat/datasetek.tsv@1a6a6eef (sha256 b09d49aadf7f…) | ts=2026-10-19`.

| | Érték |
|---|---|
| fájlsor | 121 = 3 megjegyzéssor + 1 fejlécsor + **117 adatsor** |
| különböző `dataset` | **30** |
| `study_tipus` szerint | `bovitett` 29 · `tematikus` 29 · `melyelemzes` 29 · `lexikon_oldal` **30** |
| nem mind a négy típusban | egyetlen: `OSHL_lexikalis_index`, csak `lexikon_oldal` (F56.5, `92ac8424`, DT-F56b → DT47) |
| `allapot` | `elerheto` 77 · `korlatos` 32 · `hianyzik` **4** · `generalt_nezet` 4 |
| duplikált kulcs (`study_tipus`+`dataset`) | 0 |

A 30 dataset: BDB, BDB_szakaszok, BDB_vers_jelentes, BSB_Strongs, KJV_ASV_Strongs, KJV_teljes_szoveg, Karoli_1908, Karoli_KH, Karoli_Strong_kivonat, Karoli_Strong_parok, Karoli_Strong_szavak, LSJ, LXX_OS, Macula_gorog, Macula_heber, Nave_basokant, OSHL_BDB_igehelyek, OSHL_lexikalis_index, SDBH, SDGNT, SECE_G, SECE_H, Strong_szotar, TAGNT, TAHOT, TIPNR, TSK, Thayer, morf_kulcs_heber, openbible_crossrefs.

**Az elavult állítások a SEMA 2.6-ban** (`adat/SEMA.md`, a sorszám a `1a6a6eef` szerint):

| # | Hol | Mit mond | Mért | Mihez képest |
|---|---|---|---|---|
| E1 | 375. sor (bevezető) | „21 dataset × 4 = 84 sor” | 30 dataset, 117 sor; **nem** egyenletes ×4: 29 × 4 + 1 | a teljes tábla; a +1 a `lexikon_oldal`/`OSHL_lexikalis_index` sor |
| E2 | 380. sor (`dataset` mező) | „a dataset rövid neve (21 érték)” | 30 érték | a `dataset` oszlop különböző értékei |
| E3 | 389. sor (`hianyzik`) | „jelenleg egyetlen sor sem viseli” | 4 sor viseli: `openbible_crossrefs` × 4 study-típus (F44, `b0303c68`, 2026-10-05; DT33: „jelölt, nem importált”) | az `allapot` oszlop |

Az E1–E2 a #56 javaslatának (b) tárgya és a csonk `ad` mezője; az E3 a mérésnél derült ki, a #56 nem említi; a DT248 (b) 1. döntése szerint a #69 hatókörébe tartozik. A 2.6 többi számadata (KJV-, BSB-darabszámok) a datasetek fájljairól szól, nem a `datasetek.tsv`-ről: nem e feladat tárgya.

**Történet (miért csúszik a szám):** a „21 dataset × 4 = 84 sor” alak a `23616837` (F17, 2026-09-30) óta áll; azóta a datasetfelvételek a táblát bővítették (+9 dataset, +33 sor), a SEMA-mondatot nem. A szám tehát a következő datasetfelvételnél újra elavul; ennek gépi őrzése (pl. `ellenoriz.py`-szabály) nem e feladat része, l. 2. pont.

## 2. Hatókör

**Benne:** csak az `adat/SEMA.md` 2.6 szakaszának E1, E2 és E3 mondata (DT248 (b) 1.). Szövegcsere, új szabály vagy új szakasz nélkül.

**Nincs benne:**
- az `adat/datasetek.tsv` bármilyen módosítása (csak olvasott);
- a SEMA más szakaszai és a 2.6 dataset-leírásai (KJV_teljes_szoveg, BSB stb.);
- a `CLAUDE.md` „Adat-tár” „17 dataset” mondata (a `konkordancia/` fájlkészletéről szól, nem a mátrixról; elavultsága külön vizsgálandó, a végrehajtó csak jelzi a zárójelentésben);
- az elavulás gépi megelőzése (CI- vagy `ellenoriz.py`-szabály): ha a felhasználó kéri, külön feladat a `/befogad`-dal.

**Átfedés:** az `adat/SEMA.md`-t más feladat is írhatja. A 2026-10-19-i állapotban nyitott PR: #420 (#11 folytatás); a #50 (`.claude/commands/`), a #22 és egy `/befogad`-session párhuzamosan fut. A `python eszkozok/feladatok.py fuggesek` (2026-10-19) a #69-re nem vezet le függést, ütközést vagy sorrendet, ezért a `fugg` és a `nem_fugg` üres. **Ha a végrehajtás előtt a main-en a 2.6 szakasz vagy a `datasetek.tsv` megváltozott, a végrehajtó újramér (3. lépés), és az új számot írja be; a briefbeli 117/30 csak tájékoztató.**

## 3. Lépések (⛔ a kötelező megállások)

0. **Modell-ellenőrzés:** a tényleges modellnév kiírása és összevetése a fejléc `modell: haiku` mezőjével; eltérésnél megállás (CLAUDE.md).
1. **Döntés:** a DT248 🟢 (felhasználó, 2026-10-19): (a) 1., (b) 1. Ha a végrehajtáskor a `DONTESEK.md` sora nem 🟢/✅, ⛔ megállás.
2. Ág a friss main-ről (`claude/f69-sema-dataset-szam`), a brief fejléce `allapot: fut`, `ag:`. Commit: `F69.1: …`.
3. **Újramérés** szkripttel (fájlba írva, `eszkozok/` alá nem kerül; a scratch a repón kívül), `split('\t')`-tel, az 1. pont táblázatának soraira: adatsor, különböző dataset, study-típusonkénti szám, a nem mind a négy típusban álló datasetek, `hianyzik`-sorok. Az eredmény és a proveniencia-sor (`scope=adat/datasetek.tsv teljes | forras=adat/datasetek.tsv@<main-commit> (sha256 <12 jegy>) | ts=<nap>`) a zárójelentésbe (`naplok/SEMA_DATASET_SZAM_zaras.md`). Ha a számok eltérnek a briefétől: nem hiba, az újramért érték az irányadó; a zárójelentés rögzíti a különbséget.
4. **Átírás** a DT248 döntése szerint, a 3. lépés mért számaival:
   - E1: „… négy study-típusra kifejtve (…), **<D> dataset, <S> sor: <D−1> × 4 + az `OSHL_lexikalis_index` egy `lexikon_oldal`-sora**” (2026-10-19-én: 30, 117, 29); a mért egyenetlenség szerint, ha az eltér, ⛔;
   - E2: „(<D> érték)”;
   - E3: a „jelenleg egyetlen sor sem viseli” helyett a mért sorok megnevezése (2026-10-19-én: a 4 `openbible_crossrefs`-sor, mind a négy study-típusban, jelölt, nem importált, DT33); a mondat folytatása (SDBH/SDGNT, az értékkészlet nyitottsága) megmarad.
   Más sor nem változik. Commit: `F69.2: …`.
5. **Önellenőrzés:** `git diff --stat adat/SEMA.md` legfeljebb a 2.6 szakaszt érinti (E1–E3 sorai); a beírt számok egyeznek a 3. lépés mérésével. `python eszkozok/feladatok.py ellenoriz` 0 hiba. Zárójelentés, a brief fejléce (`allapot: lezarva`, `lezarva_osszegzes`, `pr`). Commit: `F69.3: …`, push, draft PR. Merge a felhasználótól.

**⛔ Megállás** továbbá: ha a 3. lépés mérése szerint újabb egyenetlenség van (egynél több dataset nem mind a négy típusban, vagy duplikált kulcs) és a DT248 (a) választott alakja ezt nem tudja kifejezni; ha az átírás a 2.6-on kívüli sort érintene.

## 4. Elfogadási feltételek

- **G1.** A SEMA 2.6 bevezető mondata a 3. lépésben mért adatsor- és datasetszámot mondja, a DT248 (a) szerinti alakban; „× 4 = …” egyenletes szorzat nem marad benne, ha a mérés szerint az eloszlás egyenetlen.
- **G2.** A `dataset` mező sorának zárójele a mért különböző datasetszám.
- **G3.** Az E3 mondat a mért `hianyzik`-sorokat nevezi meg (DT248 (b) 1.); „egyetlen sor sem” nem marad benne.
- **G4.** `git diff main -- adat/SEMA.md` csak a 2.6 szakasz E1–E3 sorait érinti; `adat/datasetek.tsv` diffje üres.
- **G5.** A zárójelentésben a mérés proveniencia-sora és a mért táblázat áll; az ellenőr saját szkripttel ugyanezt kapja.
- **G6.** `python eszkozok/feladatok.py ellenoriz` 0 hiba.

## 5. Döntésnapló

- **DT248** (🟢, felhasználó, 2026-10-19, `DONTESEK.md`): (a) 1. „30 dataset, 117 sor: 29 × 4 + az OSHL_lexikalis_index egy lexikon_oldal-sora” (a számok a végrehajtáskori mérésből); (b) 1. a `hianyzik`-mondat is javítandó a mért sorokkal. Kérdés volt: (a) a bevezető mondat alakja az egyenetlen eloszlásnál; (b) az E3 (`hianyzik`) javítása e feladat része-e. Az eredeti javaslat: (a) „30 dataset, 117 sor: 29 dataset mind a négy study-típusban (29 × 4 = 116), az `OSHL_lexikalis_index` csak `lexikon_oldal`-ban (DT47)” — a számok a futáskori mérésből; (b) igen, mert ugyanaz a szakasz, ugyanabból a táblából mérhető, és a ma hamis „egyetlen sor sem” állítás a `hianyzik` értéket olvasó felhasználót félrevezeti.
