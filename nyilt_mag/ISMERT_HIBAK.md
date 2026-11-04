# Ismert hibák a forrásadatokban

# GENERÁLT: a PaRDeS nyílt mag exportja (CC BY 4.0), a projekt adataiból generálva — kézzel nem szerkesztendő; a „#” kezdetű sor megjegyzés.

A nyílt mag készítői itt mondják ki azokat a forráshibákat, amelyeket a saját méréseik kimutattak, és azt, hogyan kezeli őket a csomag. A hiányt nem töltjük ki: ahol a forrás hibás vagy hiányos, az üres eredmény nem negatív lelet.

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

**Kezelés.** A nyílt mag a KH-tábla adatát nem tartalmazza, és egyetlen sora sem épít rá: a kereszthivatkozás-alapú jelöltek az itteni `kizarasok.tsv`-ben a TSK és a kézi minősítés alapján szerepelnek, a „Károli-kereszthivatkozás” keresési móddal jelölve. A határ: a mérés a másolat-típusú hibát fogja meg, az egyedi, nem duplikált hibás listát nem. A hibás listák javítása a projekt nyitott tétele; a javítás után a mérőszámok megváltoznak.

## 2. Szemantikai domének: nem teljes lefedés

A külön réteg (`cc_by_sa_reteg/`) az UBS SDBH/SDGNT szemantikai doménjeit tartalmazza a csomag szóbázisaira. A domén-adat az ószövetségi szókincs kb. 90%-át fedi: a hiányzó bejegyzés **nem negatív lelet**, és a domén támasz, nem a motívum meghatározásának helyettesítője.

## 3. A Károli-szó gépi párosítása

Az `elofordulasok.tsv` `azonositas_modja` oszlopának `szó-szintű-gépi` értéke modell-kimenet: a Károli-szó és a Strong-szám párosítását gép végezte, csak magas bizonyosságú pár igazolhat sort. A mód azt mondja meg, hogyan azonosítottuk a szót, nem azt, hogy a párosítást ember ellenőrizte.
