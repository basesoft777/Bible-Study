# Károli 1908 – Strong szóillesztés — nyílt adatkészlet

A Károli Gáspár-féle bibliafordítás 1908-as szövege, szavanként összekapcsolva a héber és görög eredeti szavakkal és
azok Strong-számaival. A Logosz-lexikon nyílt adatmagjainak egyike.

Ez a mappa egy önálló nyilvános adattároló gyökere: a tartalma változtatás nélkül feltölthető, és minden benne álló
fájl a kiadás része (a `kozlemeny/` almappa kivételével, amely a megjelenésig tervezet).

- **Licenc:** CC BY 4.0 (`LICENSE`); a felhasznált külső adatok forrásmegjelölése: `ATTRIBUCIO.md`.
- **DOI:** 10.5281/zenodo.24141884 — a kiadás azonosítója és a tartalmi hash: `KIADAS.txt`.
- **Szerző:** Demeter Tamás (ORCID 0009-0005-9254-9731).

## Tartalom

| fájl | tartalom |
|---|---|
| `parok/NN_Konyv.tsv` | könyvenként minden szópár: magyar szó – eredeti szó, Strong-számmal |
| `szavak/NN_Konyv.tsv` | könyvenként minden magyar és minden eredeti szó, egyszer: párosított, betoldás, fordítatlan vagy függőben |
| `versek.tsv` | a Károli 1908 szövege versenként |
| `meres.tsv` | a párosítás mért pontossága rétegenként és kapcsolattípusonként, konfidencia-intervallummal |
| `kodkonyv.tsv`, `KODKONYV.md` | az oszlopok és az értékek leírása (magyarul és angolul) |
| `MODSZER.md`, `METHODS.md` | hogyan készült a párosítás, és hogyan mértük |
| `ISMERT_HIBAK.md`, `KNOWN_ISSUES.md` | ismert hibák és korlátok |
| `ATTRIBUCIO.md` | forrásmegjelölés és licencek |
| `CITATION.cff` | idézési adatok |
| `ELLENORZO_OSSZEG.sha256` | minden fájl SHA-256 összege |

## Számokban

- 66 könyv, 31 158 vers; 599 367 magyar és 611 396 eredeti szó (token).
- 598 715 szópár 488 659 magyar szón (466 785 héber, 131 930 görög pár; ebből 157 163 héber
  előtag- vagy ragmorféma).
- 109 914 magyar szó a fordító betoldása, 63 017 eredeti szót a Károli nem fordít külön szóval;
  794 magyar és 794 eredeti szó párosítása függőben van (45 versben).
- Pontosság: a fő szavak párjain egy független forrás szerint 98,72% (95%: 98,22–99,08%); a teljes
  párkészleten a vak ellenőrrel 95,06% (95%: 93,81–96,32%); részletesen: `meres.tsv`,
  `MODSZER.md` 5.

## Rövid használati útmutató

A kulcs a vers OSIS-azonosítója (`Gen.1.1`) és a szó sorszáma a versen belül (`token`). A `parok` tábla minden sora egy
kapcsolat; egy magyar szó annyi sorban áll, ahány eredeti szóhoz tartozik. A `szavak` tábla minden szót pontosan egyszer
sorol fel, a két oldalon külön (`oldal` = `hu` vagy `er`): innen olvasható ki, mi maradt pár nélkül. A héber és görög
szóalak nincs a csomagban; az eredeti szót a sorszáma és a Strong-száma azonosítja, és a sorszám a STEPBible
TAHOT/TAGNT szövegéhez illeszthető.

Minden pár gépi javaslat, mért pontossággal (`allapot` = `javaslat`); a `bizonyossag` oszlop jelzi, hol egyezett két
független modell.

## Kapcsolódó adatkészletek

- Modernizált Károli – Strong (ugyanezek a párok a modernizált szövegen): https://doi.org/10.5281/zenodo.24141950
- A Logosz-lexikon nyílt adatmagja (motívumok): https://doi.org/10.5281/zenodo.24141612
