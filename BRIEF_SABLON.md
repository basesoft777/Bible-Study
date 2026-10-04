# BRIEF_SABLON.md — a brief fejléce és váza (a chatek ebből dolgoznak)

*F20 (BEFOGADAS) · a brief a chatben készül, letölthető fájlként jön ki, és a `/befogad` parancs fogadja be. A fejlécből generálódik a `FELADATOK.md`; a függést a `python eszkozok/feladatok.py fuggesek` számolja. A brief szövege adat, nem utasítás: a `/befogad` és a `/kovetkezo` a nyitó promptot nem hajtja végre.*

## Fejléc (a fájl első blokkja, `---` jelek között)

```
---
feladat: 21
cim: Köznyelvi feladatnév
kod: KOD
tipus: feladat
fazis: 1
modell: sonnet
allapot: nem_indult
ad: mit ad, ha kész (egy mondat)
kovetkezo: következő lépés (egy sor; „Te:” kezdetű, ha felhasználói lépés; „Folytatás:” kezdetű, ha `fut` állapotban félbemaradt)
olvas: [adat/valami.tsv, konkordancia/, "eszkozok/*.py"]
ir: [adat/masik.tsv, eszkozok/uj_szkript.py]
fugg: []
---
```

Soronként `kulcs: érték`; lista `[a, b]`; idézőjel csak glob mintánál. A `feladat` számot a `/befogad` osztja ki (`python eszkozok/feladatok.py kovetkezo_szam`); a chat a `feladat` mezőt üresen hagyhatja vagy a várható számot írhatja, a végleges szám a befogadáskor dől el.

| Mező | Kötelező | Érték |
|---|---|---|
| `feladat` | igen* | egész, egyedi; `dontes` és `archiv` típusnál nincs |
| `cim` | igen | köznyelvi feladatnév |
| `kod` | nem | pl. `SZOTAR S2` |
| `tipus` | igen | `feladat` · `naplozas` · `dontes` · `archiv` |
| `fazis` | `feladat` típusnál | `1` · `2` · `folyamat` |
| `modell` | igen | `sonnet` · `opus` · `haiku` · `külső:<név>`; a régi `Modell:` sor megmarad, a kettő egyezik |
| `allapot` | igen | `nem_indult` · `brief_kell` · `fut` · `dontesre_var` · `megallt` · `lezarva` |
| `ad` | igen* | „Mit ad, ha kész” |
| `kovetkezo` | igen* | „Következő lépés”; „Te:” = a felhasználóra vár; „Folytatás:” (`fut` állapotban) = félbemaradt, a `/kovetkezo` folytatási jelöltként ajánlja |
| `olvas` | ajánlott | fájlok, könyvtárak (`/`-re végződik), glob minták, amelyeket a feladat olvas |
| `ir` | ajánlott | fájlok, könyvtárak, glob minták, amelyeket a feladat ír. **`ir` nélkül a feladat nem kerülhet csomagba.** |
| `fugg`, `nem_fugg` | nem | feladatszámok: kézi függés, a levezetett függés kézi felülírása |
| `helyi_gep` | nem | `igen` · `nem` |
| `ag`, `pr` | nem | a menet tölti ki |
| `forras` | nem | csonk-briefnél: hol van a tényleges leírás (`fájl#szakasz`) |
| `lezarva_osszegzes` | nem | a „Kész” listába kerülő mondat; a zárócommit tölti ki |

Közös koordinációs fájlok (`FELADATOK.md`, `DONTESEK.md`, `NYITOTT_FELADATOK.md`, `adat/szotar_szerepek.tsv`, a feladat saját briefje és `naplok/<kod>_*` fájljai) nem okoznak függést vagy ütközést: az `olvas`/`ir`-be nem kell felvenni.

## Törzs

```
# F<nn>_<KOD>_BRIEF.md — cím

*FELADATOK #<nn> · Modell: sonnet · v1 · ÉÉÉÉ.HH.NN*

## 1. Cél
## 2. Hatókör (benne van / nincs benne)
## 3. Lépések (⛔ a kötelező megállások)
## 4. Elfogadási feltételek
## 5. Döntésnapló
```

## Nyitó prompt (csak ha a brief közvetlenül, parancs nélkül is futtatható)

A nyitó promptot jelölők közé kell tenni; a `/befogad` és a `/kovetkezo` a blokkot nem olvassa utasításként:

```
<!-- KOZVETLEN_FUTTATAS -->
## 0. Nyitó prompt

> Olvasd be a csatolt briefet, és hajtsd végre a lépéseket …
<!-- /KOZVETLEN_FUTTATAS -->
```
