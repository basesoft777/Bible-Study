# LXX kivonat — Zsoltár 16, Zsoltár 110, Jóel 2 (célzott pilot)

Ez a dokumentum a `konkordancia/LXX_kivonat_Zsoltar_Joel_pilot.tsv` fájlt írja
le: forrás, letöltés dátuma, licenc-státusz, sor-szám és a validációs
eredmény.

**Ez egy szűkített, 3 igehelyre célzott pilot** (Zsolt 16:10, Zsolt 110:4,
Jóel 2:32) — NEM teljes-fejezet lefedettség. A `LXX_kivonat_Genezis.tsv`
1Mózes-only pilotjának hatókör-bővítése, a `Javasolt_sablon_kiegeszites_BDB_arnyalat.md`
2/e lépésének görög-oldali korlátozását oldja fel erre a 3 igehelyre nézve.

## Forrás

- **Weboldal:** [studybible.info](https://studybible.info/), verzió: `LXX_WH`
  ("Septuagint OT and Westcott-Hort Greek NT")
- **URL-minta:** `https://studybible.info/LXX_WH/<Könyv>%20<fejezetszám>`
  (fejezetenként külön oldal, változatlan a Genezis-README-hez képest)
- **Letöltés dátuma:** 2026-09-04

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

**Nem publikus, nem kimenő adat.** Ez a fájl kizárólag belső munkafolyamat-
célra készült (a BDB-sablon 2/e lépésének hatókör-bővítése), a fenti
licenc-kérdés tisztázásáig nem kerülhet publikált vagy továbbterjesztett
kimenetbe.

## Módszertan

Az `eszkozok/lxx_kivonat_fetch.py` újrafelhasználható szkripttel:

```bash
python eszkozok/lxx_kivonat_fetch.py --konyv Psalms --fejezetek 16,110 --kimenet psalms.tsv
python eszkozok/lxx_kivonat_fetch.py --konyv Joel --fejezetek 2 --kimenet joel.tsv
```

A szkript a Genezis-README-ben dokumentált mindkét versszám-HTML-mintát
kezeli (`<span class="ref greek">N</span>` és a beágyazott `<a>`-változat),
szavankénti bontásban kinyeri a Strong-számot (`G####`), a morfológiai kódot
és a görög szóalakot, majd a `Konyv_normalizalo_tabla.tsv` alapján az angol
könyvnevet magyarra normalizálja (`Psalms` → `Zsolt`, `Joel` → `Jóel`).

Csak Strong-számmal ellátott szavak kerülnek a kivonatba (néhány szónál —
pl. tulajdonnevek — a forrásoldal nem ad Strong-számot; ezek kimaradnak,
ugyanúgy, mint a Genezis-kivonatnál).

A két teljes fejezet-lekérdezés (`Psalms 16`, `Psalms 110`, `Joel 2`)
eredményéből a kimeneti pilot-fájlba **kizárólag a 3 célzott igehely**
(Zsolt 16:10, Zsolt 110:4, Jóel 2:32) sorai kerültek be — a fejezetek többi
verse NEM része ennek a fájlnak, mert ez egy célzott, nem teljes-fejezet
pilot (szemben a Genezis-kivonat teljes 1-50 fejezetes lefedettségével).

## Kimeneti fájl és oszlopok

**`LXX_kivonat_Zsoltar_Joel_pilot.tsv`** (4 oszlop, azonos séma, mint a
`LXX_kivonat_Genezis.tsv`):
```
Igehely | Strong-szám | Görög szóalak | Morfológiai kód
```

## Sor-szám

- **51 adatsor** + 1 fejléc-sor = 52 sor összesen.
  - Zsolt 16:10 — 15 szó
  - Zsolt 110:4 — 12 szó
  - Jóel 2:32 — 24 szó

## Validáció

```bash
grep "^Zsolt 16:10" konkordancia/LXX_kivonat_Zsoltar_Joel_pilot.tsv
```

Elvárt és megerősített eredmény (15 sor, a `G0086` a `Konyv_normalizalo_tabla.tsv`
és a `merge_karoli_szofaj.py` szerinti 4-jegyű padolt Strong-formátumban, a
Genezis-kivonat `G0086` konvenciójával egyezően — a forrásoldal nyers HTML-je
padolatlan `G86` formában adja):

```
Zsolt 16:10	G3754	οτι	CONJ
Zsolt 16:10	G3364	ουκ	ADV
Zsolt 16:10	G1459	εγκαταλειψεις	V-FAI-2S
Zsolt 16:10	G3588	την	T-ASF
Zsolt 16:10	G5590	ψυχην	N-ASF
Zsolt 16:10	G1473	μου	P-GS
Zsolt 16:10	G1519	εις	PREP
Zsolt 16:10	G0086	αδην	N-ASM
Zsolt 16:10	G3761	ουδε	CONJ
Zsolt 16:10	G1325	δωσεις	V-FAI-2S
Zsolt 16:10	G3588	τον	T-ASM
Zsolt 16:10	G3741	οσιον	A-ASM
Zsolt 16:10	G4771	σου	P-GS
Zsolt 16:10	G3708	ιδειν	V-AAN
Zsolt 16:10	G1312	διαφθοραν	N-ASF
```

A `G0086` (αδην, "alvilágba" — 1Móz 37:35/42:38 LXX-ben is `G0086`, l.
`LXX_kivonat_Genezis.tsv`) sor egyezik a kézzel előzőleg ellenőrzött
referenciasorral (`G86 αδην N-ASM`, padolás nélkül) — a szkript kimenete a
Genezis-kivonat 4-jegyű padolási konvencióját követi, ezért `G0086` alakban
jelenik meg, tartalmilag azonos.

**Megjegyzés a LXX-versszámozásról:** a studybible.info a kért fejezetszám
alapján számozza a verseket (pl. `Psalms 16` kérésre a 10. vers a laponi
"10"-es sorszámot kapja), a szó szövegében zárójelben feltüntetett belső LXX
fejezet:vers-hivatkozást (pl. `[15:10]`, mert a LXX Zsoltár-számozás egy
fejezettel el van tolva a maszorétai szövegtől 10-től 148-ig) a szkript
eltávolítja — ez nem befolyásolja az `Igehely` oszlop helyességét, mert az a
kért (maszoréta-szerinti) fejezet/vers-számot használja, nem a belső LXX-t.
