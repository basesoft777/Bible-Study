# Modernizált Károli – Strong — nyílt adatkészlet

A Károli Gáspár-féle bibliafordítás 1908-as szövegének modernizált változata, szavanként összekapcsolva a héber
és görög eredeti szavaival és azok Strong-számaival. A Logosz-lexikon nyílt adatmagjainak egyike.

- **Licenc:** CC BY 4.0 (`LICENSE`); a felhasznált külső adatok forrásmegjelölése: `docs/hu/ATTRIBUCIO.md`.
- **DOI:** 10.5281/zenodo.24141949 — a kiadás azonosítója és a tartalmi hash: `KIADAS.txt`.
- **Szerző:** Demeter Tamás (ORCID 0009-0005-9254-9731).

## Tartalom

| fájl | tartalom |
|---|---|
| `data/konyvek/NN_Konyv.tsv` | könyvenként: minden szó 1908-as és modern alakja, és a hozzá párosított Strong-számok |
| `data/versek.tsv` | a modernizált szöveg versenként |
| `data/kodkonyv.tsv`, `docs/hu/KODKONYV.md`, `docs/en/CODEBOOK.md` | az oszlopok és az értékek leírása (magyarul és angolul) |
| `docs/hu/MODSZER.md`, `docs/en/METHODS.md` | hogyan készült a modernizálás és a Strong-összekapcsolás |
| `docs/hu/ISMERT_HIBAK.md`, `docs/en/KNOWN_ISSUES.md` | ismert hibák és korlátok |
| `docs/hu/ATTRIBUCIO.md`, `docs/en/ATTRIBUTION.md` | forrásmegjelölés és licencek |
| `CITATION.cff` | idézési adatok |
| `ELLENORZO_OSSZEG.sha256` | minden fájl SHA-256 összege |

## Számokban

- 66 könyv, 31 158 vers, 599 367 szó (token); ebből 64 388 szó és 21 636 vers változott
  a modernizálásban.
- 598 715 szópár (magyar szó – héber vagy görög szó, Strong-számmal) 488 659 magyar szón; 109 914 szó a
  fordító betoldása (nincs eredeti megfelelője), 794 szó párosítása függőben van.

## Rövid használati útmutató

A kulcs a vers OSIS-azonosítója (`Gen.1.1`) és a szó sorszáma a versen belül (`token`). Egy szó annyi sorban áll,
ahány eredeti szóhoz párosítva van; a pár nélküli szó egy sorban. A modern szöveg olvasásához a `kieso` oszlop
üres sorait kell a `token` sorrendjében venni, szavanként egyszer; a szöveg írásjelekkel a `data/versek.tsv`-ben áll.

A párosítás gépi javaslat, mért pontossággal (`docs/hu/MODSZER.md`, 5. pont).

## A két adatkészlet együtt

Ez az adatkészlet és a Károli 1908 – Strong szóillesztés (https://doi.org/10.5281/zenodo.24141883) az 1908-as szöveg ugyanazon szavait írja le, és sorról
sorra összekapcsolható.

- **Közös kulcs.** Az `osis` + `token` az 1908-as szöveg szavának helye. Ennek az adatkészletnek a `data/konyvek/NN_Konyv.tsv` sora a szóillesztés `data/parok/NN_Konyv.tsv` soraiból bővül: ugyanaz a `token`, `eredeti_token`, `strong` és `kapcsolat`, mellette az `alak_modern`, a `valtozott`, a `kieso` és a `gazda_token`. A pár nélküli szónak itt egy sora van, üres `strong` és `eredeti_token` oszloppal.
- **A modern szöveg olvasása.** A `data/konyvek/NN_Konyv.tsv` sorai közül a `kieso` oszlop üres soraiból, `token`
  sorrendben, szavanként egyszer olvasható az `alak_modern`. A `kieso` oszlopban értéket hordozó sor olyan szó, amely a
  modern szövegből kiesik; a `gazda_token` a gazdaszó helye ugyanabban a versben, és a Strong-száma a modern szövegben
  a gazdaszóhoz tartozik.
- **A forrásoldal teljes listája.** Az eredeti szavak teljes listája, köztük azokkal a héber és görög szavakkal,
  amelyeket a Károli magyarul külön szóval nem fordít, csak a szóillesztés `data/szavak/NN_Konyv.tsv` táblájában van (`oldal` = `er`), ebben az adatkészletben nincs; az `osis` + `eredeti_token` szerint kapcsolható.

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

- Károli 1908 – Strong szóillesztés: https://doi.org/10.5281/zenodo.24141883
- A Logosz-lexikon nyílt adatmagja (motívumok): https://doi.org/10.5281/zenodo.24141611
