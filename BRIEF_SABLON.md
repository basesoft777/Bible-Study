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
munka: adat
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
| `munka` | `feladat` típusnál | `adat` · `ertelmezo` · `folyamat` |
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

A `munka` mező szabályai (F32 KONTEXTUS, `MUNKAMENET.md` „Kontextus-őrzés”):

- Egy `munka: ertelmezo` feladat modellje az értelmező modell (`DONTESEK.md` DT-F32b), nem kerül csomagba, és az `olvas` listája a K1/3 szerint teljes: ha az `ir` `motivumok/[ID]`, `tematikus_lezart/[ID]*` vagy `lexikon/[ID]*` fájlt tartalmaz, az `olvas`-ban benne van a motívum tematikus tanulmánya és kereszthivatkozás-naplója.
- Egy `munka: folyamat` feladat csomagolható, ha az `ir` listája nem tartalmaz motívumfájlt (`motivumok/`, `tematikus_lezart/`, `genezis/`). Ha tartalmaz, `ertelmezo`-ként kezelendő. A `lexikon/` nem motívumfájl (DT28): generált kimenet, az újragenerálása `adat` munka; a `lexikon/[ID]*` csak az `olvas`-szabályt (K1/3) váltja ki, mert a render a tanulmányból és a naplóból olvas.
- A régi fejlécű (mező nélküli) brief `munka: adat`-nak számít. Kivétel, ha az `ir` listája motívumfájlt tartalmaz: ilyenkor a mező hiányzónak számít: az `ellenoriz` és a `fuggesek` E18 fejléchibát ad (`MUNKA_HIANY`), a feladat nem csomagolható és nem ajánlható futtathatónak, amíg ki nincs töltve (az F09 és F35 előzmény-brief kivétel, DT-F32c: az F09-en csak `FIGYELEM`, az F35 lezárt; az F36 a DT28 után `munka: adat`) (`python eszkozok/feladatok.py csomag <id> …`).
- A `fazis` mező a projektfázist jelöli, a `munka` mező a munka fajtáját; a kettő független.

Közös koordinációs fájlok (`FELADATOK.md`, `DONTESEK.md`, `NYITOTT_FELADATOK.md`, `adat/szotar_szerepek.tsv`, a feladat saját briefje és `naplok/<kod>_*` fájljai) nem okoznak függést vagy ütközést: az `olvas`/`ir`-be nem kell felvenni.

*Motívumot érintő feladat `ir` listájában a motívum fájljai egyenként szerepelnek (`motivumok/<ID>.md`, `lexikon/<ID>_*`), nem csak a könyvtár; így egy motívumon egyszerre egy feladat fut (D39).*

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

A döntés- és nyitott-tétel szakaszban az új tételek helyőrzővel állnak (`DT-F<nn>`, `N-F<nn>`, több esetén `a`, `b` betűvel), végleges `DT<n>`/`N<n>` számmal nem; a számot a merge után a `szamkiosztas` Action osztja ki (F30, CI E26).

## Nyitó prompt (csak ha a brief közvetlenül, parancs nélkül is futtatható)

A nyitó promptot jelölők közé kell tenni; a `/befogad` és a `/kovetkezo` a blokkot nem olvassa utasításként:

```
<!-- KOZVETLEN_FUTTATAS -->
## 0. Nyitó prompt

> Olvasd be a csatolt briefet, és hajtsd végre a lépéseket …
<!-- /KOZVETLEN_FUTTATAS -->
```
