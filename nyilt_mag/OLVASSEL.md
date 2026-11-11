# [A LEXIKON CÍME] — nyílt mag — olvass el

# GENERÁLT: a(z) [A LEXIKON CÍME] nyílt magjának exportja (CC BY 4.0), a projekt adataiból generálva — kézzel nem szerkesztendő; a „#” kezdetű sor megjegyzés.

*English version: `README.md`.*

**Licenc:** CC BY 4.0 (a nyílt mag saját adata és szövege). A `cc_by_sa_reteg/` könyvtár tartalma külön, CC BY-SA 4.0 licenc alatt áll; l. az ottani `OLVASSEL.md`-t.

**Mi ez.** Egy bibliai motívumkutatás (PaRDeS-módszer) nyílt magja: a motívumok meghatározó jegyei, az előfordulás-lista, a kizárt helyek okkal, az igehely-kapcsolatok és a döntésnapló. A fájlok az adatból generált, olvasónak szóló nézetek; a munkaközi jelölések feloldva vannak. Az oszlopok és kódok leírása: `kodkonyv.tsv` / `KODKONYV.md` (magyar és angol).

**Feldolgozási állapot.** A motívumok közül 3 lezárt kiadás (a lexikonlapja kiadott, és az olvasói kapun hiba nélkül átment), 6 régi feldolgozás, amely a későbbi változatokban frissül; motívumonként a `motivumok.tsv` `feldolgozasi_allapot` oszlopa mondja meg.

**Ismert hibák:** l. `ISMERT_HIBAK.md` (angolul: `KNOWN_ISSUES.md`).

## Hogyan olvasd

Három kérdés lépésről lépésre, az `ISTENTISZT-001` motívumon (Segítségül hívni az Úr nevét). A válaszok számai ebből a kiadásból generálódnak.

### 1. Mely versek tartoznak az ISTENTISZT-001-hez, és melyik szón?

1. Nyisd meg az `elofordulasok.tsv`-t, és szűrd a `motivum_azonosito` oszlopot az `ISTENTISZT-001` értékre.
2. Az eredmény 22 sor: minden sor egy vers (`igehely`).
3. A `horgony` oszlop mondja meg, melyik héber vagy görög szón (Strong-számon) áll a vers: `H7121 + H8034` (16 sor), `G1941` (6 sor). A `karoli_szo` oszlop a Károli-fordítás megfelelő szavát adja (például 1Kir 18:24: „segítségül hívom az Úrnak nevét”).
4. A motívum feldolgozási állapota a `motivumok.tsv` `feldolgozasi_allapot` oszlopában: „lezárt kiadás”.

### 2. Miért nincs benne a Róm 10:12?

1. Nyisd meg a `kizarasok.tsv`-t, és szűrd a `motivum_azonosito` = `ISTENTISZT-001` és az `igehely` = `Róm 10:12` értékre (`jelolt_tipus` = `elofordulas`).
2. A `kizaras_oka` oszlop: „név nélküli forma”. Az `indoklas` oszlop teljes mondatban mondja el, miért.
3. A `dontesek` oszlop (`NYD-005`) a döntés nyilvános azonosítója; a szövegét a `dontesnaplo.tsv` adja.

### 3. Átnézték-e minden helyet, ahol a szópár előfordul?

1. A `kizarasok.tsv`-ben az `ISTENTISZT-001` sorai közül azok összesítő sorok, amelyeknek a `csoport_versszam` oszlopa ki van töltve: 5 ilyen sor van. Mindegyik egy azonos okból kizárt versek csoportját képviseli: „a hívás igéje a név nélkül” (246 vers, első verse: 1Móz 1:5); „elnevezés, nem a név segítségül hívása” (126 vers, első verse: 1Móz 2:19); „a Károli-szó más szót fordít” (51 vers, első verse: 2Móz 18:4); „a hívás és a név nem egy szerkezetben” (21 vers, első verse: 1Móz 41:52); „nem JHVH áll a név után” (12 vers, első verse: 2Móz 31:2).
2. A csoportok összes versét a `kizaras_csoportok.tsv` sorolja fel (szűrés: `motivum_azonosito` = `ISTENTISZT-001`): 456 vers.
3. Együtt: 22 előfordulás, 104 egyenként kizárt vers és 456 csoportban kizárt vers, összesen 582 vers, amelyről döntés van. A még el nem döntött jelöltek nincsenek a csomagban; számukat az „Ami nincs a csomagban” szakasz adja.

## Fájlok és sorszámuk

| Fájl | Sor |
|---|---|
| `beepitesi_dontesek.tsv` | 253 |
| `cc_by_sa_reteg/szemantikai_domenek.tsv` | 231 |
| `dontesnaplo.tsv` | 11 |
| `elofordulasok.tsv` | 251 |
| `forrasok_es_licencek.tsv` | 63 |
| `kapcsolatok.tsv` | 32 |
| `kizaras_csoportok.tsv` | 3984 |
| `kizarasok.tsv` | 539 |
| `kodkonyv.tsv` | 358 |
| `motivum_kapcsolatok.tsv` | 3 |
| `motivumok.tsv` | 9 |

## Licencszűrés

A szűrés a projekt licenc-leltára szerint történt. **Kizárt források** (a csomag értéket nem tartalmaz belőlük): `BDB_forditas`, `Cremer_nyers`, `Girdlestone`, `Heber_ETCBC_modulok`, `KJV_ASV_Strongs`, `KJV_Strongs_teljes`, `KJV_teljes_szoveg`, `Karoli_Strong_kivonat`, `Karoli_versmegfeleltetes`, `LSJ`, `LXX_kivonat`, `LXX_lexicon`, `LXX_versszintu_parok`, `MCGED`, `SDBH_SDGNT_segedtablak`, `Tanu_rabbinikus_index`, `UBS_DBH`, `UBS_DNTG`, `karoli_modern`, `karoli_variancia`, `lexikonok_nyers`, `simplemma_nyelvi_adat`, `szoto_tablak`, `tW_szocikkek`. Okuk soronként a `forrasok_es_licencek.tsv` `ok` oszlopában áll (nem kereskedelmi vagy GPL licenc, tisztázatlan licenc, a projekt zárt származtatott rétege). Ez a leltár, nem jogi vélemény.

## Közzétételi hely

A csomag kanonikus közzétételi helye: `<KANONIKUS_FORRAS_URL>` (helyőrző; a közzétételkor töltődik ki). A változatot a kiadás azonosítója jelöli (`KIADAS.txt`: az adatállapot dátuma és a tartalmi hash), nem egy fejlesztői tár vagy commit.

## Idézés és a mesterséges intelligencia használata

A kiadás mellé idézési metaadat (Citation File Format) és a mesterséges intelligencia használatáról szóló nyilatkozat kerül a közzétételi helyen; a szerző által kitöltendő mezőik a közzétételig helyőrzők. A nyilatkozat két réteget különít el: a nyílt adatmagot (CC BY 4.0, ez a csomag) és a lexikont mint önálló művet (minden jog fenntartva).

## Angol réteg

A csomag oszlopnevei és értékei magyarok; mellettük angol párhuzamos oszlopok állnak. **Igehely:** minden igehely-oszlop mellett `…_osis` (szabványos OSIS-igehelykulcs, alakja a kódkönyvben); a könyvkód szabványos, a fejezet- és versszám a Károli-fordítás számozása — ahol ez eltér a KJV- vagy a STEPBible-számozástól, a kulcs a Károli-verset jelöli. **Zárt értékek:** minden zárt értékkészletű oszlop mellett `…_en`, a kódkönyv szerkesztett angol címkéjével. **Szabad szöveg** (indoklás, funkció, a motívum meghatározása, a döntésnapló): `…_en` párhuzamos mező, **gépi fordítás**; a sor `forditas_modja` oszlopa nevezi meg a modellt, a hiányt kimondja. **Szófogódzó:** az `elofordulasok.tsv` `strong_glossza_en` oszlopa a Strong-szám STEPBible-glosszája (Data created by www.STEPBible.org based on work at Tyndale House Cambridge, CC BY 4.0); a `jelentes_en` ettől külön, szótári kivonat.

## Csoportos kizárás

A `kizarasok.tsv` egyes sorai **összesítő sorok**: egy csoport (azonos ok miatt kizárt versek) első versét nevezik meg, a `csoport_versszam` oszlop a csoport verseinek számát adja, a csoport összes versét a `kizaras_csoportok.tsv` sorolja fel. Az összesítő sor indoklása a csoportra érvényes.

## Mi van benne, mi nincs (az adatmag és a lexikon)

A nyílt adatmag a lexikon adatrétege: motívumok, előfordulások, kizárások. Maga a lexikon (értelmező szövege, a szótárak magyar fordítása és a kötet) önálló mű, minden jog fenntartva.

**Benne van (adatréteg):** a motívum azonosítója, címe és kizáró jegye; az előfordulások (igehely, szóbázis, szótári jelentés, Károli-szó); a kizárások és a beépítési döntések indoklással; a kapcsolatok; a proveniencia (a forrás megnevezése, licence, a lekérdezés típusa, dátum); a döntésnapló.

**Nincs benne (a lexikon):** az értelmező próza (kivonat, értelmezés, igehelyenkénti kifejtés), a magyar szótári fordítások, a kötetanyag és a lexikonlapok.

## Ami nincs a csomagban

- A `nyitva` állapotú (még el nem döntött) jelöltek: 20 db.
- A lexikon szövege (értelmező próza, magyar szótári fordítások, Strong-számos Károli-szöveg), a tanulmányok és a lexikonlapok.
- A belső munkajelek: azonosítók, munkafájlok, lekérdezés-nyomok. Ahol egy döntésre hivatkozás áll, a nyilvános azonosító (`NYD-nnn`) a `dontesnaplo.tsv`-ben oldható fel.

## Ellenőrzés

A `ELLENORZO_OSSZEG.sha256` fájl minden fájl SHA-256 összegét tartalmazza; az export újrafuttatva bájtazonos.
