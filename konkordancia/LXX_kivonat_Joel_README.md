# LXX kivonat — Jóel (teljes könyv)

Ez a dokumentum a `konkordancia/LXX_kivonat_Joel.tsv` fájlt írja le: forrás,
letöltés dátuma, licenc-státusz, módszertan, sor-szám és a validációs
eredmény.

**Ez a teljes Jóel könyv (3 fejezet) kivonata**, a
`LXX_kivonat_Zsoltar_Joel_pilot.tsv` 3 igehelyre célzott pilotjának
hatókör-bővítése. A pilot-fájl megmarad, nem törlődik — validációs
referenciaként szolgál (l. lent).

## Forrás

- **Weboldal:** [studybible.info](https://studybible.info/), verzió: `LXX_WH`
  ("Septuagint OT and Westcott-Hort Greek NT")
- **URL-minta:** `https://studybible.info/LXX_WH/Joel%20<fejezetszám>`
  (1-től 3-ig, fejezetenként külön oldal, változatlan a Genezis- és a
  pilot-README-hez képest)
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
célra készült, a fenti licenc-kérdés tisztázásáig nem kerülhet publikált vagy
továbbterjesztett kimenetbe.

## Módszertan

Az `eszkozok/lxx_kivonat_fetch.py` újrafelhasználható szkripttel:

```bash
python eszkozok/lxx_kivonat_fetch.py --konyv Joel --fejezet-tol 1 --fejezet-ig 3 \
  --versifikacios-terkep konkordancia/LXX_versificacios_terkep.tsv \
  --karoli-konyv-prefix Jóel \
  --kimenet konkordancia/LXX_kivonat_Joel.tsv
```

### Miért kellett a `--versifikacios-terkep` opció

Jóelnél a Károli fejezetszámozás a **görög (LXX) hagyományt** követi, nem a
héberét: a héber szöveg 4 fejezetre osztja a könyvet (a mai "2:28–32" angol/
Károli szakasz héberül önálló 3. fejezet, a mai "3." fejezet pedig héberül a
4.), míg a görög LXX — és ezt követve a Károli is — 3 fejezetre. A
studybible.info oldal maga is ezt a hármas (Károlival megegyező) felosztást
használja az URL-ben (`Joel 1`, `Joel 2`, `Joel 3` — ellenőrizve: a `Joel 2`
oldal mind a 32 verset tartalmazza, a `Joel 4` oldal nem is létezik).

A nyers HTML-ben viszont a szó elejére írt `[fejezet:vers]` zárójeles jelölés
a **héber (Heber_vers) fejezetszámozást** használja (pl. Jóel 3:1 → `[4:1]`,
mert a héber ezt a szakaszt 4. fejezetnek számozza) — ez az egyetlen lényegi
eltérés a Zsoltárok-kivonathoz képest, ahol a zárójel a `Gorog_LXX_vers`
oszloppal egyezett. A szkript mindkét oszlopot (elsődlegesen `Gorog_LXX_vers`,
tartalékként `Heber_vers`) beépíti a kereső-szótárba, így könyvenként
automatikusan a ténylegesen előforduló zárójel-konvenció talál egyezést — a
Zsoltárok-README "Módszertan" szakasza részletezi ennek okát és a
kereső-kulcs pontos szerkezetét (a kért Károli-fejezetszámot is tartalmazza,
hogy elkerülje a két különböző oldalon előforduló, azonos zárójel-értékű, de
eltérő jelentésű hivatkozások hamis ütközését).

Jóelnél a `LXX_versificacios_terkep.tsv` **teljesen tiszta**: 0 `EGYIK_SEM`,
0 `ELLENORZESRE_VAR` sor (szemben a Zsoltárokkal) — nincs szükség kizárásra
vagy a Zsoltárok-README-ben leírt cím-felirat-/záró-vers-pótló szabályokra.

## Kimeneti fájl és oszlopok

**`LXX_kivonat_Joel.tsv`** (4 oszlop, azonos séma, mint a
`LXX_kivonat_Genezis.tsv`, a `LXX_kivonat_Zsoltarok.tsv` és a pilot-fájl):
```
Igehely | Strong-szám | Görög szóalak | Morfológiai kód
```

## Sor-szám és lefedettség

- **1469 adatsor** + 1 fejléc-sor = 1470 sor összesen.
- A `Karoli_1908.tsv` szerint Jóel könyve 73 verset tartalmaz (20 + 32 + 21
  fejezetenként). Mind a **73 vers legalább egy Strong-taggelt szót kapott —
  teljes, 100%-os lefedettség**, nincs kizárt vagy lefedetlen vers.

## Validáció

A korábbi 3-verses pilot Jóel 2:32 sora szó szerint egyezik a teljes-könyves
kimenettel:

```bash
diff <(grep "^Jóel 2:32	" konkordancia/LXX_kivonat_Joel.tsv) \
     <(grep "^Jóel 2:32	" konkordancia/LXX_kivonat_Zsoltar_Joel_pilot.tsv)
```

Üres kimenetet ad (teljes egyezés) — ellenőrizve 2026-09-04. (A pilot másik
két sora, Zsolt 16:10 és Zsolt 110:4, a `LXX_kivonat_Zsoltarok_README.md`-ben
van validálva.)

Emellett ellenőrizve: a `Joel 3` oldal nyers HTML-je `[4:1]`–`[4:21]`
zárójeleket használ (héber-konvenció), és ezek helyesen `Jóel 3:1`–`Jóel
3:21` Károli-igehelyekre kerülnek a Gorog→Heber tartalék-kereséssel — ez a
Zsoltárok-kivonat két-szótáras (Gorog elsődleges, Heber tartalék) tervezésének
közvetlen, könyvek közötti ellenőrzése.
