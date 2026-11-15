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

## Kapcsolódó adatkészletek

- Károli 1908 – Strong szóillesztés: https://doi.org/10.5281/zenodo.24141883
- A Logosz-lexikon nyílt adatmagja (motívumok): https://doi.org/10.5281/zenodo.24141611
