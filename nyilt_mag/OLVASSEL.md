# Logosz-lexikon — nyílt adatmag: bibliai motívumok

<!-- GENERÁLT: a(z) Logosz-lexikon nyílt adatmagjának exportja, a projekt adataiból generálva; kézzel nem szerkesztendő. -->

Bibliai motívumok nyílt adatkészlete: a motívumok meghatározó és kizáró jegyei, előfordulásaik a héber és görög szöveg szavain, a megvizsgált, de kizárt helyek okkal, az igehely-kapcsolatok és a döntésnapló. A Logosz-lexikon nyílt adatmagjainak egyike. *English version: `README.md`.*

- **Licenc:** CC BY 4.0 (`LICENSE`); a `cc_by_sa_reteg/` könyvtár külön, CC BY-SA 4.0 licenc alatt áll. A felhasznált külső adatok forrásmegjelölése és a kizárt források: `ATTRIBUCIO.md`.
- **DOI:** 10.5281/zenodo.24141612 — a kiadás azonosítója és a tartalmi hash: `KIADAS.txt`.
- **Szerző:** Demeter Tamás (ORCID 0009-0005-9254-9731).

## Tartalom

| fájl | tartalom | sor |
|---|---|---:|
| `motivumok.tsv` | a motívumok: cím, meghatározás, az azonosság hordozója, kizáró jegy, fölérendelt fogalom, feldolgozási állapot | 9 |
| `elofordulasok.tsv` | az előfordulások: igehely, a horgonyszó és Strong-száma, szótári jelentés, Károli-szó, eredetjelölés | 250 |
| `beepitesi_dontesek.tsv` | a felvett helyek döntése, indoklással | 252 |
| `kizarasok.tsv` | a vizsgált, de kizárt helyek, okkal és indoklással; az összesítő sor egy csoportot képvisel | 540 |
| `kizaras_csoportok.tsv` | az összesítő sorok csoportjainak minden verse | 3 984 |
| `kapcsolatok.tsv` | igehely-kapcsolatok egy motívumon belül | 88 |
| `motivum_kapcsolatok.tsv` | kapcsolatok két motívum között | 3 |
| `dontesnaplo.tsv` | a hivatkozott szerkesztői döntések (`NYD-nnn`) | 15 |
| `visszhang_megfelelok.tsv` | a horgonyszavak megfelelője a Targumban, a Vulgatában és a Septuagintában | 101 |
| `visszhang_tanuk.tsv` | egyházatyai, rabbinikus és Glossa Ordinaria-tanúk, idézet nélkül | 6 |
| `vitatott_forrasok.tsv` | a vitatott pontok lektorált szakirodalma (bibliográfiai adat) | 3 |
| `sblgnt_apparatus.tsv` | az SBL Greek New Testament kritikai apparátusa az újszövetségi helyekhez | 61 |
| `forrasok_es_licencek.tsv` | a projekt forrásleltára: licenc és szerep a csomagban | 65 |
| `kodkonyv.tsv` | az oszlopok, értékek és kódok leírása (magyarul és angolul) | 440 |
| `KODKONYV.md` | ugyanez olvasható formában |  |
| `cc_by_sa_reteg/szemantikai_domenek.tsv` | szemantikai domének (UBS SDBH/SDGNT), **külön licenc: CC BY-SA 4.0** | 231 |
| `cc_by_sa_reteg/OLVASSEL.md` | a külön réteg licence és forrásmegjelölése |  |
| `MODSZER.md` | hogyan készült az adat (angolul: `METHODS.md`) |  |
| `ISMERT_HIBAK.md` | ismert hibák és korlátok (angolul: `KNOWN_ISSUES.md`) |  |
| `ATTRIBUCIO.md` | forrásmegjelölés, licencek, kizárt források |  |
| `LICENSE` | a csomag licence |  |
| `CITATION.cff` | idézési adatok |  |
| `KIADAS.txt` | a kiadás azonosítója és tartalmi hash-e (angolul: `RELEASE.txt`) |  |
| `ELLENORZO_OSSZEG.sha256` | minden fájl SHA-256 összege |  |

## Számokban

- 9 motívum: 4 lezárt kiadás, 5 régi feldolgozás, amely a későbbi változatokban frissül (`motivumok.tsv`, `feldolgozasi_allapot`).
- 250 előfordulás és 252 felvételi döntés.
- 540 kizárás-sor 61 okkal: 443 egyenként eldöntött hely, és 97 összesítő sor, amely 3 984 verset képvisel.
- 88 igehely-kapcsolat, 3 motívumközi kapcsolat, 15 nyilvános szerkesztői döntés.
- A visszhang-rétegben 101 megfelelő, 6 tanú, 3 vitatott pont és 61 apparátus-jegyzet.

**Ismert hibák:** `ISMERT_HIBAK.md` (angolul: `KNOWN_ISSUES.md`). **Módszer:** `MODSZER.md`.

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
3. Együtt: 22 előfordulás, 104 egyenként kizárt vers és 456 csoportban kizárt vers, összesen 582 vers, amelyről döntés van. A még el nem döntött jelöltek nincsenek a csomagban; számukat a „Mi van benne, mi nincs” szakasz adja.

## Mi van benne, mi nincs (az adatmag és a lexikon)

A nyílt adatmag a lexikon adatrétege: motívumok, előfordulások, kizárások. Maga a lexikon (értelmező szövege, a szótárak magyar fordítása és a kötet) önálló mű, minden jog fenntartva.

**Benne van (adatréteg):** a motívum azonosítója, címe és kizáró jegye; az előfordulások (igehely, szóbázis, szótári jelentés, Károli-szó); a kizárások és a felvételi döntések indoklással; a kapcsolatok; az eredetjelölés (a forrás megnevezése, licence, a lekérdezés típusa, dátum); a döntésnapló.

**Nincs benne (a lexikon):** az értelmező próza (kivonat, értelmezés, igehelyenkénti kifejtés), a magyar szótári fordítások, a kötetanyag és a lexikonlapok.

**Nincs a csomagban továbbá:** a még el nem döntött jelöltek (20); a források szövege (idézet); a belső munkajelek (azonosítók, munkafájlok, lekérdezés-nyomok). Ahol egy sor döntésre hivatkozik, a nyilvános azonosító (`NYD-nnn`) a `dontesnaplo.tsv`-ben oldható fel.

## Idézés és közzétételi hely

**Idézd így:** Demeter Tamás (ORCID: 0009-0005-9254-9731): Logosz-lexikon — nyílt adatmag: bibliai motívumok. DOI: 10.5281/zenodo.24141612. Az idézési adatok: `CITATION.cff`.

A csomag kanonikus közzétételi helye: `https://doi.org/10.5281/zenodo.24141612`. A változatot a kiadás azonosítója jelöli (`KIADAS.txt`: az adatállapot dátuma és a tartalmi hash), nem egy fejlesztői tár vagy commit. A lexikon honlapja: `https://logoszlexikon.hu`.

## Kapcsolódó adatkészletek

- Károli 1908 – Strong szóillesztés: https://doi.org/10.5281/zenodo.24141884
- Modernizált Károli – Strong: https://doi.org/10.5281/zenodo.24141950

A Károli-szöveg teljes Strong-párosítása ezekben áll; ez a csomag csak a motívumszó Károli-megfelelőjét adja.

## Ellenőrzés

Az `ELLENORZO_OSSZEG.sha256` minden kiadott fájl SHA-256 összegét tartalmazza; az export újrafuttatva bájtazonos. A `kozlemeny/` mappa a megjelenési közlemény tervezete, nem része a kiadásnak.
