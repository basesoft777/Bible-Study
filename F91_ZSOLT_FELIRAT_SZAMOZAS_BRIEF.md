---
feladat: 91
cim: Feliratos zsoltárok Károli–KJV számozása — felmérés és a versmegfeleltető táblák javítása
kod: ZSOLT_FELIRAT_SZAMOZAS
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: dontesre_var
ag: claude/f91-zsolt-felirat-szamozas
ad: minden feliratos zsoltár felmérve (felirat-hossz, eltolás, a két tábla állítása), proveniencia-sorral; a Karoli_versmegfeleltetes.tsv és a LXX_versificacios_terkep.tsv javítva a jóváhagyott szabály szerint (a Zsolt 22-n 0 ellentmondás az LXX_OS-szel); hatásmérés a #60 pilotra és a pardes.db-re
kovetkezo: "Te: DT-F91d (E1) eldöntése; utána zárás (független ellenőr újrafuttatása a változásokra, zárójelentés)"
olvas: [konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, "konkordancia/LXX_OS/*.tsv", konkordancia/LXX_OS/README.md, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/LXX_versificacios_terkep.tsv, konkordancia/Nave_basokant.tsv, naplok/KAROLI_KK1b_hianyzo_es_zsoltar.md, naplok/OLVASOI_PILOT_adatfelmeres.md, naplok/LXX_OS_LEFEDETTSEG_M2.md, DONTESEK.md]
ir: [konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/LXX_versificacios_terkep.tsv, naplok/ZSOLT_FELIRAT_SZAMOZAS_M0.md, naplok/ZSOLT_FELIRAT_SZAMOZAS_M0b.md, naplok/ZSOLT_FELIRAT_SZAMOZAS_M0b_terkep.md, eszkozok/terkep_kjv_kulcs_felmeres.py, naplok/ZSOLT_FELIRAT_SZAMOZAS_M2a.md, eszkozok/f91_versmegf_javit.py, naplok/KAROLI_KK4_tabla_veglegesit.py, naplok/ZSOLT_FELIRAT_SZAMOZAS_M2b_macula.md, eszkozok/f91_macula_hatasmeres.py, naplok/ZSOLT_FELIRAT_SZAMOZAS_M2c.md, naplok/ZSOLT_FELIRAT_SZAMOZAS_zaras.md, DONTESEK.md, NYITOTT_FELADATOK.md, adat/SEMA.md, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, eszkozok/f92_db_igazolas.py, eszkozok/zsolt_felirat_felmeres.py, eszkozok/olvaso_pilot/README.md, eszkozok/olvaso_pilot/felmeres.py, eszkozok/zsolt_felirat_halmaz.py, naplok/ZSOLT_FELIRAT_SZAMOZAS_M2d.md, naplok/ZSOLT_FELIRAT_SZAMOZAS_M2e_lxx_os.md, eszkozok/f91_lxx_os_replay.py]
fugg: []
---

# Feliratos zsoltárok Károli–KJV számozása — felmérés és a táblák javítása (ZSOLT_FELIRAT_SZAMOZAS)

*Befogadásra váró brief-tervezet. Forrás: DT125, 1. opció (a felhasználó döntése a chatben, 2026-10-12), a #60 olvasói pilot leletéből. A fejlécet a `/befogad` adja.*

**Javasolt fejléc-adatok:** `tipus: feladat` · `fazis: 1` · `modell: sonnet` · `munka: adat` · `kovetkezo: "/kovetkezo; ⛔ M1 után (a javítási szabály jóváhagyása)"`.

## 1. Cél

A Károli 1908 a feliratos zsoltárokat a héber szöveg (MT) szerint számozza: a felirat az 1. vers. A KJV a feliratot nem számozza. A Zsolt 22-n: „Én Istenem, én Istenem” = Károli 22:2 = KJV 22:1. Két tábla mégis Károli = KJV azonosságot ad ezekre a zsoltárokra:

- `konkordancia/Karoli_versmegfeleltetes.tsv`;
- `konkordancia/LXX_versificacios_terkep.tsv`.

A `Nave_basokant.tsv` `karoli_allapot` oszlopa ezt a hibát örökli. A #60 pilot a Zsolt 22-n 31 ellentmondó verset mért. A pilot ezt az LXX_OS KJV-oszlopával kerüli meg és jelzi, de a táblákat nem javítja.

A feladat: felmérni az összes feliratos zsoltárt (kb. 60 vagy több), és javítani a két táblát, valamint azt, ami tőlük örököl.

## 2. Lépések

- **M0 — felmérés (csak olvas).**
  - Melyik zsoltárban van számozott felirat a Károliban? Forrás: `Karoli_1908.tsv`, MT-összevetés a TAHOT-kulccsal.
  - Zsoltáronként: a felirat hossza (1 vagy 2 vers), a versenkénti eltolás, és hogy a két tábla mit állít. Mindezt proveniencia-sorral.
  - A már helyes forrás: az LXX_OS Károli-kulcsa (`zsolt_felirat_eltolas`, F54). Ezt etalonként kell használni, és rögzíteni kell, hogy honnan helyes.
- **M1 — ⛔ javítási szabály.** Javaslat a táblák javításának szabályára, a kivételekre, és arra, hogy a javítás érinti-e a Nave `karoli_allapot` oszlopát. Felhasználói jóváhagyás kell.
- **M2 — javítás.** A táblák írása a CLAUDE.md TSV-szabálya szerint: `split('\t')` és `'\t'.join()`, írás előtt összevetés az eredetivel. Bontási napló, ha a sorszám-változás táblánként legalább 10 (DT3).
- **M3 — hatás.** Mit változtat a javítás a #60 pilot vers-lapjain (Zsolt 22) és a `pardes.db`-ben. A #60 kerülőútja ezután kivezethető.

## 3. Elfogadás

- Minden feliratos zsoltár felmérve, és a lelet proveniencia-sorral áll.
- A két tábla a Zsolt 22-n 0 ellentmondást ad az LXX_OS-szel.
- A tesztek zöldek, a független ellenőr eltérés nélkül zár.

## 4. Kapcsolódás

DT125 (#60), #54 (LXX_OS-lefedettség, F54 `zsolt_felirat_eltolas`), `naplok/OLVASOI_PILOT_adatfelmeres.md` 5. pont, `naplok/KAROLI_KK1b_hianyzo_es_zsoltar.md`.
