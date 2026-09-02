# LXX kivonat — 1Mózes (pilot)

Ez a dokumentum a `konkordancia/LXX_kivonat_Genezis.tsv` fájlt írja le: forrás,
letöltés dátuma, licenc-státusz, sor-szám és a validációs eredmény.

**Ez egy szűkített, 1Mózes-only pilot a `Validacios_naplo.md`-ben rögzített
LXX-fázisolt terv 3. fázisából.** Teljes LXX-lefedettség (51 könyv) külön,
jövőbeli feladat, csak sikeres pilot után.

## Forrás

- **Weboldal:** [studybible.info](https://studybible.info/), verzió: `LXX_WH`
  ("Septuagint OT and Westcott-Hort Greek NT")
- **URL-minta:** `https://studybible.info/LXX_WH/Genesis%20<fejezetszám>`
  (1-től 50-ig, fejezetenként külön oldal — a `https://studybible.info/LXX_WH/Genesis`
  URL önmagában csak az 1. fejezetet adja vissza, NEM a teljes könyvet)
- **Letöltés dátuma:** 2026-09-02

## Licenc-státusz — explicit gap

A studybible.info oldalon (sem a főoldalon/about-on, sem a `/version/LXX_WH`
verzió-leíró oldalon) **nem található explicit copyright- vagy
licenc-nyilatkozat** a Septuaginta-szövegre vagy a Strong-taggelésre
vonatkozóan. A `/version/LXX_WH` oldal csak annyit közöl, hogy a szöveg
"Septuagint LXX Greek Old Testament keyed to Strong's numbers with complete
parsing information" — forrást vagy jogi státuszt nem jelez.

**Ez nyitott kérdés marad.** A LXX görög alapszövege (Rahlfs/Swete-hagyomány)
önmagában közkincs, de a Strong-számozás és morfológiai kódolás hozzáadott
szerkesztői munka lehet, aminek jogi státusza a studybible.info-n nincs
dokumentálva. Mielőtt ez az adat bármilyen publikált vagy továbbterjesztett
kimenetbe kerülne, a licenc-kérdést tisztázni kell (pl. a studybible.info
üzemeltetőjének megkeresésével, vagy alternatív, explicit CC-licencű LXX-forrás
keresésével, mint pl. a Rahlfs-LXX STEPBible-féle Strong-taggelt változata,
amit a `Validacios_naplo.md` 1. fázisa már azonosított jövőbeli alternatívaként).

## Módszertan

Minden 1Mózes-fejezet (1-50) külön HTML-oldalról lett letöltve
(`Genesis%20<N>`), majd szavankénti bontásban kinyerve: Strong-szám
(`G####`/`H####`), morfológiai kód (pl. `N-DSF`, `V-AAI-3S`), görög szóalak.
A versszám-hivatkozás két HTML-mintában fordul elő a forrásoldalon
(`<span class="ref greek">N</span>` és `<span class="ref greek"><a ...>N</a></span>`
— utóbbi olyan verseknél, amiknek van ÚSZ-parallel-hivatkozása) — a parser
mindkettőt kezeli.

Az "Genesis N:M" hivatkozás "1Móz N:M" formátumra alakítása a
`Konyv_normalizalo_tabla.tsv` alapján történt (Gen → 1Móz, közvetlen 1:1
fejezet/vers-megfeleltetés).

## Kimeneti fájl és oszlopok

**`LXX_kivonat_Genezis.tsv`** (4 oszlop):
```
Igehely | Strong-szám | Görög szóalak | Morfológiai kód
```

Külön fájl a `TAGNT_kivonat.tsv`-től (nem lett összemosva vele), mert ez
LXX-előfordulás (ÓSZ-görög), nem ÚSZ-előfordulás — a két adat összemosása
torzítaná a jövőbeli globális gyakoriság-számításokat.

## Sor-szám

- **29 727 adatsor** + 1 fejléc-sor = 29 728 sor összesen.
- A tervezett becslés (kb. 15 000-20 000 sor, 1533 vers × 8-15 szó) alacsonyabb
  volt a ténylegesnél — a LXX görög szövege verzenként átlagosan kb. 19,4 szót
  tartalmaz (jóval több önálló szótoken, mint a héber, mert a görög
  nyelvtan több névelőt, kötőszót és elöljárószót különít el önálló szóként).
  A gyakorlati eredmény nagyságrendileg nem tér el a becsléstől, csak a
  becslés volt alacsony — nincs jele parszolási hibának.
- Fejezetenkénti vers-szám 1:1 egyezik a `Karoli_1908.tsv`-ben szereplő
  1Mózes-vers-számokkal minden fejezetnél (1-50), összesen 1533 vers —
  ez megerősíti, hogy a parser helyesen dolgozta fel mind az 50 fejezetet
  (két fejezet, a 28. és több más, kezdetben 0 sort adott egy HTML-mintázat-
  eltérés miatt, ami javítva lett és utólag ellenőrizve).

## Validáció

```bash
grep "^1Móz 1:1" konkordancia/LXX_kivonat_Genezis.tsv
```

Elvárt és megerősített eredmény: a sorok között szerepel `G0746` (ἀρχή —
1Móz 1:1 "kezdetben" / Ján 1:1 "kezdetben" közös LXX-ÚSZ szóhasználat,
l. a fázis motivációját a `Validacios_naplo.md`-ben és a code-promptban).

```
1Móz 1:1	G0746	αρχη	N-DSF
```
