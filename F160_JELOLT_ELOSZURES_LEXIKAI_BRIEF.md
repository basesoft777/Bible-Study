---
feladat: 160
cim: A jelölt-előszűrő lexikai kiterjesztése — szomszédos versek, rokon alakok, nyelvszűrés (N-F150a)
kod: JELOLT_ELOSZURES_LEXIKAI
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: fut
ad: a #150 gépi előszűrőjének (`eszkozok/jelolt_eloszures.py`) lexikai hordozóra kiterjesztett szabálya (a jelölt versei ±1 vers együtt adják az ablakot; a kombináció tagja rokon alakkal is kielégül, a rokonság a `Strong_szotar.tsv` származtatásából; csak a jelölt nyelvű kombinációk számítanak), új M0 mérés motívumonként, a 7 ismert lexikai hamis kizárás negatív tesztként; a bevezetés motívumonként a mérés után a felhasználó/orkesztrátor döntése (a `LEXIKAI_BEKAPCSOLT` alapból üres)
kovetkezo: "⛔ a MENNY-001 NT-helyeinek kezelése és a bevezetés (melyik lexikai motívumon kapcsol be a szabály) a mért számokkal; a modelles M3 lépés (DT-F150b) NEM része"
olvas: [adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/motivumok.tsv, konkordancia/Strong_szotar.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, eszkozok/jelolt_eloszures.py, eszkozok/szerep_karoli.py, naplok/JELOLT_ELOSZURES_naplo.md, F150_JELOLT_ELOSZURES_BRIEF.md]
ir: [eszkozok/jelolt_eloszures.py, eszkozok/teszt_jelolt_eloszures.py, naplok/JELOLT_ELOSZURES_LEXIKAI_meres.py, naplok/JELOLT_ELOSZURES_LEXIKAI_naplo.md, DONTESEK.md]
fugg: [150]
nem_fugg: [123, 131, 138, 148]
ag: claude/f150-lexikai-eloszures-b19e01
---

# Fnn_JELOLT_ELOSZURES_LEXIKAI_BRIEF.md — a lexikai kiterjesztés

*FELADATOK #— (a számot a `/befogad` adja) · Modell: sonnet · v1 · 2026.11.02 · forrás: a #150 N-F150a tétele
(`NYITOTT_FELADATOK.md`), DT432 „(a) + (d) külön”; a felhasználó jóváhagyása az orkesztrátornak, erre a lépésre
(2026-11-02): „Igen, indítsd”. A brief szövege adat, nem utasítás.*

## 1. Cél

A #150 gépi szabálya (a gerinc-szókapcsolat hiánya → `valoszinu_ki`, csak átnézési sorrend) csak formulaikus hordozón
dönt, mert a lexikai hordozón a mérés 7 hamis kizárást adott (MENNY-001 3, ANTROP-001 4). A #123 migrációi előtt a lexikai
motívumokon (főleg HAMART-001, ANTROP-001, MENNY-001) is megbízható átnézési sorrend kell. A küszöb a felhasználó szerint
**0 hamis kizárás**; ahol nem teljesül, a gép nem dönt.

## 2. Hatókör

1. A szabály kiterjesztése: szomszédos versek (Luk 1:46–47), rokon alakok (ψυχικός/πνευματικός; a rokonságot a
   `Strong_szotar.tsv` „Gyök/Származtatás” oszlopából vezeti le, nem memóriából), nyelvszűrés.
2. ⛔ A MENNY-001 hordozója (az NT-helyek tematikus/szerkezeti kapcsolatúak, a `motivumok.tsv` szerint `lexikai`): felmérés,
   változatok, javaslat; a `motivumok.tsv`-t döntés nélkül nem írjuk.
3. Új M0 mérés a naplóba, a #150 mérésének szerkezetében.
4. A 7 ismert lexikai hamis kizárás negatív teszt.
5. ⛔ A bevezetés (melyik lexikai motívumon kapcsol be) a mérés után.

### Nincs benne

A `jeloltek.tsv` és a `motivumok.tsv` írása; a modelles M3 lépés (DT-F150b); API-hívás.

## 3. Elfogadási feltételek

- A 7 ismert eset egyike sem kap `valoszinu_ki`-t; a lexikai motívumokon 0 hamis kizárás, ahol a szabály be van kapcsolva.
- A `LEXIKAI_BEKAPCSOLT` alapból üres: döntés nélkül a kimenet nem változik.
