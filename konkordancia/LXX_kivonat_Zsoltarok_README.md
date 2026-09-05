# LXX kivonat — Zsoltárok (teljes könyv)

Ez a dokumentum a `konkordancia/LXX_kivonat_Zsoltarok.tsv` fájlt írja le: forrás,
licenc-státusz, oszlopok, lefedettség és ismert nyitott kérdések.

## Forrás

- **Weboldalak:** [studybible.info](https://studybible.info/) `LXX_WH` (Septuagint
  OT, Westcott-Hort, elsődleges — megtartja a morfológiai kódot) **+**
  `interlinear` (ABP — Apostolic Bible Polyglot, kiegészítő forrás azokhoz a
  szavakhoz, amiket az LXX_WH oldal nem taggel Strong-számmal)
- **Szkript:** `eszkozok/lxx_kivonat_fetch_v2.py --konyv Psalms --fejezet-tol 1
  --fejezet-ig 150 --versifikacios-terkep konkordancia/LXX_versificacios_terkep.tsv
  --karoli-konyv-prefix Zsolt`
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

A Zsoltárok könyvhöz a `--versifikacios-terkep` opció **kötelező** volt: a görög
LXX zsoltár-számozása (és a zsoltár-feliratok saját LXX-vers-számot kapnak)
eltér a maszoretai/Károli számozástól.

## Sor-szám és lefedettség

- **34 848 adatsor** + fejléc.
- **96,3%** lefedettség ((LXX_WH + ABP-pótolt) / összes sor).

## Ismert nyitott kérdések

- **Zsolt 37:1 és Zsolt 54:1 vers-összevonás:** ezek a versek a Károliban EGY
  versbe olvasztják össze két, a görög/héber hagyományban külön (pl. cím-felirat
  + tartalom) számozott LXX-verset. Ez a `--versifikacios-terkep` opcióval
  helyesen fel van oldva (megerősítve: mind a 4 érintett vers — 36:1, 37:1,
  53:1, 54:1 — LXX_WH-natív szószáma pontosan egyezik a korábban validált
  adatállapottal). Ez a jelenség **nem általános a Zsoltárokban** — a legtöbb
  vers-áthelyezést a szkript zökkenőmentesen kezeli, ez a két konkrét eset azért
  érdemel külön említést, mert ezeken bukkant fel és lett javítva egy, a
  keresőszótár-építésben rejlő hiba (l. `eszkozok/lxx_kivonat_fetch.py`
  `load_versifikacios_terkep()` commit-történetét).
- **Zsolt 151 (apokrif toldalék):** a 150. zsoltár utáni apokrif szöveg
  helyesen kimarad (nincs Károli-megfeleltetés rá), nem szivárog be tévesen a
  150:6 alá.
- Néhány, betűvel megkülönböztetett fél-vers határánál (pl. Zsolt 13:5/13:6) a
  pontos elválasztás nem rekonstruálható a nyers forrásoldalból — ilyenkor a
  tartalom az egyik oldalra (jellemzően a korábbi versre) kerül, a másik
  üresen marad, nem becsültük meg a felosztást.
- 0 db betű-utótagos vers-albontási kizárás jár funkcionális hatással (van
  8 térkép-sor betű-utótaggal, de ezeknél mindegyiknél volt egy másik, betű
  nélküli térkép-sor is, ami már helyesen lefedte a tartalmat).
