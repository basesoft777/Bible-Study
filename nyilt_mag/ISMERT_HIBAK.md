# Ismert hibák és korlátok

<!-- GENERÁLT: a Logosz-lexikon nyílt adatmagjának exportja, a projekt adataiból generálva; kézzel nem szerkesztendő. -->

*Logosz-lexikon — nyílt adatmag · adatállapot: 2026-11-10*

Itt mondjuk ki azokat a forráshibákat, amelyeket a saját méréseink kimutattak, és azt, hogyan kezeli őket a csomag. A hiányt nem töltjük ki: ahol a forrás hibás vagy hiányos, az üres eredmény nem negatív lelet. A módszer korlátait a `MODSZER.md` 12. pontja sorolja fel.

## 1. Károli-kereszthivatkozások: más vers listájának másolata

A Károli-Biblia kereszthivatkozás-táblájának (a Károli-kiadás kereszthivatkozásai, KH) egy része nem a saját versének, hanem egy másik versnek a listáját hordozza (például az ApCsel 2:27 sorai azonosak az ApCsel 7:14 soraival; Ézs 34:11 = Ézs 40:11; Zsolt 116:13 = Zsolt 140:4).

| Mérőszám | Érték |
|---|---|
| a KH-táblában forrásvers (van kereszthivatkozás-listája) | 19817 |
| KH-sor összesen | 32407 |
| a listája szó szerint megegyezik egy másik forrásversével | 12322 |
| ebből gyanús (másolt) forrásvers | 5078 |
| a gyanús listák KH-sorai | 7971 |

**Gyanús** az a forrásvers, amelynek a listája szó szerint megegyezik egy másik forrásversével, a saját listájának egyetlen eleme sem támogatott (sem a TSK ±3 verses környezete, sem a cél visszautalása nem igazolja), a vele azonos listájú vers listája viszont támogatott.

**Kezelés.** A nyílt mag a KH-tábla adatát nem tartalmazza, és egyetlen sora sem épít rá: a kereszthivatkozás-alapú jelöltek az itteni `kizarasok.tsv`-ben a TSK és a kézi minősítés alapján szerepelnek, a „Károli-kereszthivatkozás” keresési móddal jelölve. A határ: a mérés a másolat-típusú hibát fogja meg, az egyedi, nem duplikált hibás listát nem.

**Javítás.** A táblát egy független második tanúval, a Károli-fordítás Magyar Elektronikus Könyvtárbeli kiadásának (MEK 00161) kereszthivatkozásaival vetettük össze. A javított táblában minden sor szintet kap: 23 979 sor megerősített (a két tanú egyezik, vagy a második tanú adja, és nem mond neki ellent), 11 040 sor kiesik, 181 sorról még nincs döntés. A második tanútól átvett sorok maradék hibája a MEK saját elírása; ezt szúrópróbával mértük. A jelöltkeresés már a javított táblát használja; a fenti táblázat a javítás előtti, eredeti tábla mérése. **Nyitva maradt:** a döntés nélküli 181 sor, és a lexikonlapok kereszthivatkozás-blokkja, amely a lapok következő generálásakor áll át a javított táblára.

## 2. Szemantikai domének: nem teljes lefedés

A külön réteg (`cc_by_sa_reteg/`) az UBS SDBH/SDGNT szemantikai doménjeit tartalmazza a csomag szóbázisaira. A domén-adat az ószövetségi szókincs kb. 90%-át fedi: a hiányzó bejegyzés **nem negatív lelet**, és a domén támasz, nem a motívum meghatározásának helyettesítője.

## 3. A Károli-szó gépi párosítása

Az `elofordulasok.tsv` `azonositas_modja` oszlopának `szó-szintű-gépi` értéke modell-kimenet: a Károli-szó és a Strong-szám párosítását gép végezte, csak magas bizonyosságú pár igazolhat sort. A mód azt mondja meg, hogyan azonosítottuk a szót, nem azt, hogy a párosítást ember ellenőrizte.

A javítások a következő kiadásba kerülnek; a kiadás a `KIADAS.txt` azonosítójával idézhető.
