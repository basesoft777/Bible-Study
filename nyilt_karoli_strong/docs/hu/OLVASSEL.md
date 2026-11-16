# Károli 1908 – Strong szóillesztés — nyílt adatkészlet

A Károli Gáspár-féle bibliafordítás 1908-as szövege, szavanként összekapcsolva a héber és görög eredeti szavakkal és
azok Strong-számaival. A Logosz-lexikon nyílt adatmagjainak egyike.

A csomag minden fájlja a kiadás része.

- **Licenc:** CC BY 4.0 (`LICENSE`); a felhasznált külső adatok forrásmegjelölése: `docs/hu/ATTRIBUCIO.md`.
- **DOI:** 10.5281/zenodo.24141883 — a kiadás azonosítója és a tartalmi hash: `KIADAS.txt`.
- **Szerző:** Demeter Tamás (ORCID 0009-0005-9254-9731).

## Tartalom

| fájl | tartalom |
|---|---|
| `data/parok/NN_Konyv.tsv` | könyvenként minden szópár: magyar szó – eredeti szó, Strong-számmal |
| `data/szavak/NN_Konyv.tsv` | könyvenként minden magyar és minden eredeti szó, egyszer: párosított, betoldás, fordítatlan vagy függőben |
| `data/versek.tsv` | a Károli 1908 szövege versenként |
| `data/meres.tsv` | a párosítás mért pontossága rétegenként és kapcsolattípusonként, konfidencia-intervallummal |
| `data/kodkonyv.tsv`, `docs/hu/KODKONYV.md`, `docs/en/CODEBOOK.md` | az oszlopok és az értékek leírása (magyarul és angolul) |
| `docs/hu/MODSZER.md`, `docs/en/METHODS.md` | hogyan készült a párosítás, és hogyan mértük |
| `docs/hu/ISMERT_HIBAK.md`, `docs/en/KNOWN_ISSUES.md` | ismert hibák és korlátok |
| `docs/hu/ATTRIBUCIO.md`, `docs/en/ATTRIBUTION.md` | forrásmegjelölés és licencek |
| `CITATION.cff` | idézési adatok |
| `ELLENORZO_OSSZEG.sha256` | minden fájl SHA-256 összege |

## Számokban

- 66 könyv, 31 158 vers; 599 367 magyar és 611 396 eredeti szó (token).
- 598 715 szópár 488 659 magyar szón (466 785 héber, 131 930 görög pár; ebből 157 163 héber
  előtag- vagy ragmorféma).
- 109 914 magyar szó a fordító betoldása, 63 017 eredeti szót a Károli nem fordít külön szóval;
  794 magyar és 794 eredeti szó párosítása függőben van (45 versben).
- Pontosság: a fő szavak párjain egy független forrás szerint 98,72% (95%: 98,22–99,08%); a teljes
  párkészleten a vak ellenőrrel 95,06% (95%: 93,81–96,32%); részletesen: `data/meres.tsv`,
  `docs/hu/MODSZER.md` 5.

## Rövid használati útmutató

A kulcs a vers OSIS-azonosítója (`Gen.1.1`) és a szó sorszáma a versen belül (`token`). A `parok` tábla minden sora egy
kapcsolat; egy magyar szó annyi sorban áll, ahány eredeti szóhoz tartozik. A `szavak` tábla minden szót pontosan egyszer
sorol fel, a két oldalon külön (`oldal` = `hu` vagy `er`): innen olvasható ki, mi maradt pár nélkül. A héber és görög
szóalak nincs a csomagban; az eredeti szót a sorszáma és a Strong-száma azonosítja, és a sorszám a STEPBible
TAHOT/TAGNT szövegéhez illeszthető.

Minden pár gépi javaslat (`allapot` = `javaslat`), a fent megadott mért pontossággal; a pontosság rétegenként és
kapcsolattípusonként a `data/meres.tsv`-ben áll.

## A két adatkészlet együtt

Ez az adatkészlet és a Modernizált Károli – Strong (https://doi.org/10.5281/zenodo.24141949) az 1908-as szöveg ugyanazon szavait írja le, és sorról
sorra összekapcsolható.

- **Közös kulcs.** Az `osis` + `token` az 1908-as szöveg szavának helye. A modernizált adatkészlet `data/konyvek/NN_Konyv.tsv` sora ennek az adatkészletnek a `data/parok/NN_Konyv.tsv` soraiból bővül: ugyanaz a `token`, `eredeti_token`, `strong` és `kapcsolat`, mellette az `alak_modern`, a `valtozott`, a `kieso` és a `gazda_token`. A pár nélküli szónak ott egy sora van, üres `strong` és `eredeti_token` oszloppal.
- **A modern szöveg olvasása.** A `data/konyvek/NN_Konyv.tsv` sorai közül a `kieso` oszlop üres soraiból, `token`
  sorrendben, szavanként egyszer olvasható az `alak_modern`. A `kieso` oszlopban értéket hordozó sor olyan szó, amely a
  modern szövegből kiesik; a `gazda_token` a gazdaszó helye ugyanabban a versben, és a Strong-száma a modern szövegben
  a gazdaszóhoz tartozik.
- **A forrásoldal teljes listája.** Az eredeti szavak teljes listája, köztük azokkal a héber és görög szavakkal,
  amelyeket a Károli magyarul külön szóval nem fordít, csak ennek az adatkészletnek a `data/szavak/NN_Konyv.tsv` táblájában van (`oldal` = `er`); az `osis` + `eredeti_token` szerint kapcsolható.

**Példa: 1Móz 1:1 (`Gen.1.1`), az első három szó.** A szóillesztés (`data/parok/01_Gen.tsv`):

| `token` | `alak_1908` | `eredeti_token` | `strong` | `kapcsolat` |
|---|---|---|---|---|
| 1 | Kezdetben | 1 | H9003 | morfema |
| 1 | Kezdetben | 2 | H7225 | szo |
| 2 | teremté | 3 | H1254 | szo |
| 3 | Isten | 4 | H0430 | szo |

A modernizált adatkészlet (`data/konyvek/01_Gen.tsv`), ugyanezek a szavak:

| `token` | `alak_1908` | `alak_modern` | `valtozott` | `eredeti_token` | `strong` | `kapcsolat` |
|---|---|---|---|---|---|---|
| 1 | Kezdetben | Kezdetben |  | 1 | H9003 | morfema |
| 1 | Kezdetben | Kezdetben |  | 2 | H7225 | szo |
| 2 | teremté | teremtette | igen | 3 | H1254 | szo |
| 3 | Isten | Isten |  | 4 | H0430 | szo |

Az eredeti szavak, az első öt (`data/szavak/01_Gen.tsv`, `oldal` = `er`):

| `token` | `allapot` | `partner_token` | `strong` |
|---|---|---|---|
| 1 | parositva | 1 | H9003 |
| 2 | parositva | 1 | H7225 |
| 3 | parositva | 2 | H1254 |
| 4 | parositva | 3 | H0430 |
| 5 | forditatlan |  | H0853 |

Az 5. eredeti szó (`H0853`) `allapot` oszlopa `forditatlan`: a `data/parok/` táblában nincs sora, csak a `data/szavak/` táblában szerepel.

## Kapcsolódó adatkészletek

- Modernizált Károli – Strong (ugyanezek a párok a modernizált szövegen): https://doi.org/10.5281/zenodo.24141949
- A Logosz-lexikon nyílt adatmagja (motívumok): https://doi.org/10.5281/zenodo.24141611
