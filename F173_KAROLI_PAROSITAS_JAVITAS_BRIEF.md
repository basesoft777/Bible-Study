---
feladat: 173
cim: A Károli–héber/görög szópárosítás pontosságának javítása
kod: KAROLI_PAROSITAS_JAVITAS
tipus: feladat
fazis: folyamat
modell: opus
munka: adat
allapot: nem_indult
ad: a Károli–Strong párosítás ismert hibáinak (N-F172a–c) javítása szabályalapú utófeldolgozással és Strong-konvenció átváltó táblával, új méréssel a #172 módszerével, a 2. kiadás előre rögzített minőségi céljához mérve
kovetkezo: "Csonk, indítás előtt kidolgozandó: a /befogad után a brief kidolgozása, majd /kovetkezo; előfeltétel a #172 (PR #643) mergelése"
olvas: [adat/karoli_strong/, naplok/KAROLI_PONTOSSAG_jelentes.md, f172/, eszkozok/karoli_strong/, adat/SEMA.md]
ir: [adat/karoli_strong/strong_atvalto.tsv, eszkozok/karoli_strong/utofeldolgozas.py, eszkozok/karoli_strong/strong_atvalto.py, eszkozok/karoli_strong/teszt_utofeldolgozas.py, f173/, naplok/KAROLI_PAROSITAS_JAVITAS_meres.md]
fugg: [172]
---

# F173_KAROLI_PAROSITAS_JAVITAS_BRIEF — csonk

*FELADATOK #173 · csonk-brief · Modell: opus · v1 · 2026.11.05 · **csonk, indítás előtt kidolgozandó**; a felhasználó jóváhagyása (2026-11-05): „a károli strong javítás … vegyük fel jövőbeni feladatnak / most csak brief csonk”.*

## 1. Cél

A #172 mérése (`naplok/KAROLI_PONTOSSAG_jelentes.md`; PR #643) szerint a gépi Károli–héber/görög párosítás fő szavakon 98,72% (külső forrás), minden páron 95,1% (vak Opus), a morfémapárokon 90,7%. A feladat az ismert hibák javítása, hogy a 2. kiadás előre rögzített minőségi célja (jelentés 7. pont) teljesüljön. A párosítás a mérés után nyílt adat (CC BY 4.0, DT-F172b), a megjelenítés fizetős lehet.

Forrás-tételek: N-F172a (az 5 megerősített párhiba), N-F172b (az „egység határa” / szomszédos token rendszerhiba), N-F172c (a morféma-párok ellenőrzése).

## 2. Javasolt lépések (sorrendben; a kidolgozás dolga)

- (a) Determinisztikus utófeldolgozás a szomszédos-token hibára: fölös héber előtag/névelő leválasztása; szabály + teszt + CI-kapu.
- (b) Strong-konvenció átváltó tábla (KJV-hagyomány ↔ TAHOT, pl. H3212/H1980, H7125/H7122).
- (c) Az ismert hibák javítása; visszacsatolási hurok a cikk-menetek ellenőrzött párjaiból.
- (d) Csak ha a mért pontosság alacsony marad: második modell a csak egymodelles könyvekre, harmadik ítélettel.

## 3. Mi a kész

- [ ] A szabály-utófeldolgozás és az átváltó tábla tesztekkel, generátorszinten (nem laponkénti folt).
- [ ] Az N-F172a–c tételek lezárva vagy indokoltan átvezetve.
- [ ] Új mérés a #172 módszerével (rétegzett minta, vak ellenőr, független külső forrás).
- [ ] A 2. kiadás minőségi célja teljesül: külső fő-szó egyezés alsó széle ≥ 98%; vak súlyozott egyezés alsó széle ≥ 93%, egy réteg sem 90% alatt.
- [ ] Közlés kapcsolattípusonként és rétegenként; a `bizonyossag` és a „javaslat” állapot megmarad.

*Ütközés: a #22 is írja az `adat/karoli_strong/`-t (számsorrend: a #22 előbb); a kidolgozáskor ellenőrizendő.*

*Az `ir` mező a csonkban szűk (új fájlok), hogy ne kerüljön függési körbe a #172-vel; a `parok_*.tsv` javítása és a meglévő szkriptek módosítása a kidolgozáskor kerül be, a függés/ütközés újraszámolásával.*
