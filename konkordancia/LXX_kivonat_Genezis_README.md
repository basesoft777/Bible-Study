# LXX kivonat — Genezis (1Móz, teljes könyv)

Ez a dokumentum a `konkordancia/LXX_kivonat_Genezis.tsv` fájlt írja le: forrás,
licenc-státusz, oszlopok, lefedettség és ismert nyitott kérdések.

## Forrás

- **Weboldalak:** [studybible.info](https://studybible.info/) `LXX_WH` (Septuagint
  OT, Westcott-Hort, elsődleges — megtartja a morfológiai kódot) **+**
  `interlinear` (ABP — Apostolic Bible Polyglot, kiegészítő forrás azokhoz a
  szavakhoz, amiket az LXX_WH oldal nem tagged Strong-számmal)
- **Szkript:** `eszkozok/lxx_kivonat_fetch_v2.py --konyv Genesis --fejezet-tol 1
  --fejezet-ig 50 --versifikacios-terkep konkordancia/LXX_versificacios_terkep.tsv
  --karoli-konyv-prefix 1Móz`
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
  pótlás, mert a két forrás szórendje/szóhasználata túl eltér ahhoz, hogy
  biztonságosan illesszük)
- *(üres)* — sem az LXX_WH, sem az ABP nem ad Strong-számot erre a szóra
  (jellemzően valódi tulajdonnév)

## Sor-szám és lefedettség

- **32 565 adatsor** + fejléc.
- **94,6%** lefedettség ((LXX_WH + ABP-pótolt) / összes sor).

## Ismert nyitott kérdések

- **1Móz 31:55–32:32 (és kisebb mértékben 5:32/6:1) fejezethatár-eltolódás:** a
  studybible.info nyers oldal-helyi vers-számozása ezen a szakaszon nem egyezik a
  Károlival — amit a raw oldal "32:1"-nek jelöl, az valójában (a
  `LXX_versificacios_terkep.tsv` szerint) Károli 31:55, és a további versek is
  +1 eltolással követik egészen 32:32-ig. Ez a `--versifikacios-terkep` opcióval
  helyesen fel van oldva (megerősítve: mind az 5 érintett vers LXX_WH-natív
  szószáma pontosan egyezik a korábbi, kézzel validált adatállapottal) — ez a
  konkrét eset azért érdemel külön említést, mert **Genezisben ez az egyetlen
  ismert ilyen jellegű eltolódás**, nem általános mintázat a könyvben.
- 204 sor esetén sem az LXX_WH, sem az ABP nem ad Strong-számot (tulajdonnevek).
- 0 db betű-utótagos vers-albontási kizárás (l. `Betu_utotag_kizarva.tsv`) —
  Genezist ez a jelenség nem érinti.
