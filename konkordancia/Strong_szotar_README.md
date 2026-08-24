# Strong-szótár — deduplikált, teljes Biblia, 6 oszlopos

Ez a dokumentum a `konkordancia/Strong_szotar.tsv` fájlt írja le: forrás, letöltés
dátuma, licenc, és — mivel a mezőazonosítás és a görög oldal Strong↔lemma
megfeleltetése nem triviális — a pontos módszertan, hogy egy jövőbeli bővítésnél ne
kelljen újra kitalálni.

## Kimenet

**`Strong_szotar.tsv`** (14 347 sor, egyedi Strong-szám soronként):
```
Strong-szám | Szótő | Kiejtés | Szófaj | Gyök/Származtatás | Jelentés
```

- **Strong-szám:** tiszta, 4 számjegyre nulla-kitöltött forma (`H0430`, `G0032`),
  homográf-betűjelölés nélkül — konzisztens a `TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv`
  konvenciójával.
- **Szótő, Kiejtés, Jelentés:** az eredeti (v1, 4 oszlopos) szótárból változatlanul
  átemelve — ezek forrása a `TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv` első előfordulása
  Strong-számonként (lásd korábbi changelog-bejegyzés).
- **Szófaj, Gyök/Származtatás:** ÚJ oszlopok, ebben a körben kerültek be, az alábbi két
  külső lexikai forrásból.

## Fejlesztéstörténet

1. **v1 (korábbi kör):** 4 oszlopos alapváltozat (`Strong-szám | Szótő | Kiejtés |
   Rövid jelentés`), 13 676 egyedi Strong-szám, a `TAHOT_kivonat.tsv` +
   `TAGNT_kivonat.tsv` deduplikálásából.
2. **v2 (ez a kör):** bővítve `Szófaj` és `Gyök/Származtatás` oszloppal, az alábbi
   forrásokból; emellett 671 új Strong-szám került be (480 héber + 191 görög), amik a
   lexikonokban szerepeltek, de a TAHOT/TAGNT-kivonatban nem — végleges összesen: 14 347
   sor (8718 héber, 5629 görög).

## 1. Héber oldal — openscriptures/HebrewLexicon

- **Repó:** [openscriptures/HebrewLexicon](https://github.com/openscriptures/HebrewLexicon) (GitHub, publikus)
- **Felhasznált fájlok:** `HebrewStrong.xml` (8674 bejegyzés), `PartsOfSpeech.xml`
  (52 szófaji kód → angol név megfeleltetés)
- **Letöltés dátuma:** 2026-08-24 (`git clone --depth 1`)
- **Licenc:** *"Creative Commons Attribution 4.0 International license. The actual
  text of Brown, Driver, Briggs and Strong's Hebrew dictionary remain in the public
  domain."* — a repó `readme.md`-jéből szó szerint idézve.

**Mezőmegfeleltetés:**
- `Szófaj`: a `<w pos="...">` attribútum, a `PartsOfSpeech.xml` kódtáblája alapján
  magyarra fordítva (pl. `n-f` → "főnév, nőnemű"). Összetett kódoknál (pl. `"a n-f"`,
  ha egy szó melléknévként ÉS főnévként is előfordul) mindkét fordítás szerepel,
  " / "-lel elválasztva.
- `Gyök/Származtatás`: a `<source>` elem tartalma, tisztított formában, a hivatkozott
  Strong-szám megtartásával (pl. `<source>from the same as <w src="H7218">7218</w>;
  </source>` → `"from the same as H7218"`). Ha egy szónak nincs `<source>` eleme (azaz
  önmagában gyökszó), a mező üresen marad.
- **Validáció (H7225):** az eredmény szó szerint egyezik a feladat kiindulási
  mintájával — `רֵאשִׁית` / `n-f` → "főnév, nőnemű" / "from the same as H7218" /
  "the first, in place, time, order or rank...".
- **Lefedettség:** mind a 8674 bejegyzésnél sikerült szófajt hozzárendelni; 8667-nél
  van gyök/származtatás adat (7 bejegyzésnek nincs `<source>` eleme — ezek önálló
  gyökszavak).

## 2. Görög oldal — openscriptures/GreekResources

- **Repó:** [openscriptures/GreekResources](https://github.com/openscriptures/GreekResources) (GitHub, publikus)
- **Felhasznált fájl:** `GreekWordList.js` (16 352 lemma-kulcsos bejegyzés, ebből 5543-nak
  van `strong` mezője)
- **Letöltés dátuma:** 2026-08-24 (`git clone --depth 1`)
- **Licenc:** *"These files are released under a Creative Commons Attribution 4.0
  International License. For attribution purposes, credit the Open Scriptures
  Septuagint Project."* — a repó `README.md`-jéből szó szerint idézve.

**Fontos szerkezeti különbség a héber oldalhoz képest:** a `GreekWordList.js` egy
ékezet nélküli lemma-alakkal kulcsolt index (nem Strong-szám-kulcsos), és minden
lemma-bejegyzésnek CSAK OPCIONÁLISAN van `strong` mezője. Emiatt a feldolgozás iránya
fordított: végig kellett menni MINDEN kulcson, és összegyűjteni azokat, amiknek van
`strong` mezője.

**Mezőmegfeleltetés:**
- `Szófaj`: a `pos` mező (Packard-féle rövidítés), a feladatban megadott 10 kódos
  táblázat szerint magyarra fordítva (`N`→főnév, `Np`→tulajdonnév, `V`→ige,
  `A`→melléknév, `R`→névmás, `C`→kötőszó, `X`→partikula, `I`→indulatszó,
  `M`→ragozhatatlan számnév, `P`→elöljárószó, `D`→határozószó). Összetett kódoknál
  (pl. `"N A"`) mindkét fordítás szerepel, " / "-lel elválasztva.
- `Gyök/Származtatás`: a `src` mező feloldva — lásd az alábbi külön szabályt.
- **Lefedettség:** 5629 egyedi Strong-számhoz sikerült bejegyzést találni (191 új, ami
  nem volt a TAHOT/TAGNT-kivonatban); ebből 4274-nél van szófaj, 4268-nál gyök/
  származtatás adat (a `def`/`src`/`pos` mezők egy része hiányzik a forrásban magában
  is — ez a forrás-adat jellemzője, nem feldolgozási hiba).

### 2a. `src`-feloldási szabály (felhasználói döntés, 2026-08-24)

A `src` mező egy másik, ékezet nélküli lemma-kulcsra hivatkozik, ami KÉTFÉLE lehet:

- **Ha a hivatkozott kulcs maga is szerepel a listában, saját `strong` mezővel** —
  akkor a `Gyök/Származtatás` mezőbe az az ékezetes lemma + a Strong-száma kerül.
  Példa: **G26** (`ἀγάπη`, "love") `src` mezője `"αγαπαω"` — ez a kulcs a listában
  `{"lemma": "ἀγαπάω", "strong": "25", ...}` bejegyzésre mutat, tehát a végeredmény:
  `ἀγαπάω (G0025)`.
- **Ha a hivatkozott kulcs NEM szerepel önálló, Strong-számos bejegyzésként** (mert
  csak feltételezett/nem önállóan előforduló görög gyökszó) — akkor a nyers, ékezet
  nélküli forma kerül be, jelölve, hogy nem önálló szócikk. Példa: **G700**
  (`ἀρέσκω`, "to please") `src` mezője `"αρω"` — ez a kulcs nem létezik önálló
  bejegyzésként, tehát a végeredmény: `ἄρω (nem önálló Strong-számos szócikk)`
  (illetve ha a kulcs sem oldható fel lemmára, a nyers `src` string marad,
  ugyanazzal a jelöléssel).

### 2b. Strong-szám-ütközés feloldási szabály (felhasználói döntés, 2026-08-24)

Mivel a lista lemma-kulcsos, előfordul, hogy **két különböző lemma ugyanarra a
Strong-számra hivatkozik** — ez vagy (a) egy elsődleges/alternatív alak-pár (a
másodlagosnak van `"v"` mezője, ami az elsődlegesre mutat), vagy (b) a forrásfájl saját
homográf-toldaléka (pl. `"32"` és `"32a"`, ami normalizáláskor ugyanarra a
`G0032`-re esik — ld. `H7225G`-stílusú homográf-normalizálás máshol a projektben).

19 ilyen ütközés fordult elő. Mindegyiknél a **"teljesebb" bejegyzést** választottuk
elsődlegesnek, egy pontozásos szabály szerint: `deriv` mező megléte +2 pont, `def`
mező megléte +1, `src` mező megléte +1, valódi (nem másik görög szóra mutató)
betacode `l` mező +1, `"v"` mező megléte (= másodlagos alak jelzése) −3 pont.
Példák:
- **G32:** `ἄγγελος` ("angel", van `deriv`, `def`, betacode `l`, pontszám 4) nyert
  `ἀγγέλλω` ("to deliver a message", csak `def`+`l`, pontszám 2) ellenében.
- **G3156:** `Ματθαῖος` (nincs `"v"` mezője) nyert `Μαθθαῖος` (van `"v": "ματθαιος"`,
  −3 pont) ellenében.
- **G4405, G4481:** hasonlóan, a `"v"` mező nélküli alak nyert.

A teljes 19 eset listája (Strong-szám, nyertes/vesztes lemma) reprodukálható a
feldolgozó szkript naplójából; a döntési logika maga determinisztikus és
Strong-szám-független (nem esetenkénti kézi döntés).

**Kizárt, nem valódi Strong-hivatkozás:** 1 bejegyzés (`ιππικον` / `ἱππικόν`) `strong`
mezője a `"A"` string volt (nem szám) — ez nyilvánvalóan nem Strong-szám-hivatkozás,
hanem a forrásfájl saját belső jelölése, ezért kihagyva.

## Validáció

- H7225 (héber): egyezik a mintával — lásd fent.
- G4151 (`πνεῦμα`, "spirit/breath"): `Szófaj` = "főnév", `Gyök` = `πνέω (G4154)`.
- G5590 (`ψυχή`, "soul"): `Szófaj` = "főnév", `Gyök` = `ψύχω (G5594)`.
- 0 hibás formátumú Strong-szám (`NaN` vagy hiányos oszlopszám) az eredmény fájlban.

A pontos módszertani döntésekért és a feladat kontextusáért lásd a döntési fájl
[PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md](../PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md)
changelog-ját (v31).
