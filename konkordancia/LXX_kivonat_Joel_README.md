# LXX kivonat — Jóel (teljes könyv)

Ez a dokumentum a `konkordancia/LXX_kivonat_Joel.tsv` fájlt írja le: forrás,
licenc-státusz, oszlopok, lefedettség és ismert nyitott kérdések.

## Forrás

- **Weboldalak:** [studybible.info](https://studybible.info/) `LXX_WH` (Septuagint
  OT, Westcott-Hort, elsődleges — megtartja a morfológiai kódot) **+**
  `interlinear` (ABP — Apostolic Bible Polyglot, kiegészítő forrás azokhoz a
  szavakhoz, amiket az LXX_WH oldal nem taggel Strong-számmal)
- **Szkript:** `eszkozok/lxx_kivonat_fetch_v2.py --konyv Joel --fejezet-tol 1
  --fejezet-ig 3 --versifikacios-terkep konkordancia/LXX_versificacios_terkep.tsv
  --karoli-konyv-prefix Jóel`
- **Letöltés dátuma:** 2026-09-05

## Licenc-státusz — explicit gap

A studybible.info-n (sem az LXX_WH, sem az ABP verziónál) nem található explicit
copyright- vagy licencnyilatkozat a görög szövegre vagy a Strong-taggelésre
vonatkozóan. **Ez a fájl kizárólag belső munkafolyamat-célú, nem publikus**
kimenet, amíg a licenckérdés nem tisztázódik.

## Oszlopok

```
Igehely | Strong-szám | Görög szóalak | Morfológiai kód | Forrás
```

A `Forrás` oszlop értékei soronként:
- `LXX_WH` — a szó eredetileg is Strong-taggelt volt az LXX_WH oldalon
- `ABP-pótolt` — a Strong-számot az ABP oldalról pótoltuk, kizárólag akkor, ha a
  közvetlen szövegkörnyezet (előző/következő Strong-szám) egyértelműen egyezett
- `ELTERO_SZOVEGALAP` — a vers szövegcsalád-eltérés miatt jelzett rése (nincs
  pótlás)
- *(üres)* — sem az LXX_WH, sem az ABP nem ad Strong-számot erre a szóra

Jóelnél a Károli fejezetszámozás a görög (LXX) hagyományt követi (3 fejezet),
míg a nyers oldal belső zárójeles hivatkozásai a héber (4 fejezetes)
számozást használják — a `--versifikacios-terkep` opció ezt hidalja át.

## Sor-szám és lefedettség

- **1580 adatsor** + fejléc.
- **96,5%** lefedettség ((LXX_WH + ABP-pótolt) / összes sor).

## Ismert nyitott kérdések

- Nincs Jóelre jellemző, egyedi strukturális eltérés — a könyv 3 fejezete
  tisztán, kivétel nélkül feldolgozható volt.
- 0 db betű-utótagos vers-albontási kizárás.
- 16 sor esetén sem az LXX_WH, sem az ABP nem ad Strong-számot.
