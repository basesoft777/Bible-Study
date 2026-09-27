# FORDITAS_P1 — minta és terminológia

*FORDITAS_PILOT_BRIEF.md v1, FP1 · 2026.09.26 · ág: `claude/forditas-pilot-brief-3afbbf` ·
építő szkript: `naplok/FORDITAS_P1_epit.py`*

## 1. A 20 szócikkes minta (§1)

| Csoport | Darab | Strongok |
|---|---|---|
| **E** (éles igény) | 13 | G0012, G0086, G0282, G0813, G0994, G1311, G1944, G2671, G4151, G5010, G5351, G5356, G5590 |
| **A** (arany) | 1 | G1941 — a kész fordítás `naplok/FORDITAS_P1_arany.tsv`-ben, a prompt ezt nem kapja meg |
| **N** (leendő igény) | 3 | G0035, G0540, G2672 |
| **V** (változatosság) | 3 | G0004, G0002, G3777 |

Táblázat: `naplok/FORDITAS_P1_minta.tsv` (`strong`, `csoport`, `hossz`, `forras_hash`).
A `hossz` és a `forras_hash` a `Thayer_teljes.tsv` `Teljes_szocikk` mezőjére számol
(SHA-1, a SZOTAR_BRIEF S1 `forras_hash` definíciója szerint).

## 2. A V-csoport választási szabálya (determinisztikus, `FORDITAS_P1_epit.py`)

A jelölt-halmaz mindhárom lépésben kizárja a már felhasznált (E+A+N, majd a korábban
kiválasztott V) Strong-számokat, és `Strong_padded` szerint növekvő sorrendben megy.

- **V1 (≤ 300 karakteres):** a legkisebb Strong_padded-ű szócikk, amelynek
  `Teljes_szocikk` hossza ≤ 300 karakter → **G0004** (220 kar.).
- **V2 (héber idézet):** a legkisebb Strong_padded-ű szócikk, amelynek szövegében
  héber betű (Unicode U+0590–U+05FF) fordul elő → **G0002** (469 kar., `אַהֲרֹן` stb.).
- **V3 (szövegkiadás-jelzetekkel sűrű):** a `\b(?:L|T|Tr|WH|Rec\.)\b` mintára illeszkedő
  nyers előfordulásszám maximális a **≤ 4 000 karakteres** szócikkek között (a G6-ban már
  rögzített "hosszú szócikk" határ); e korlát nélkül a legtöbb jelzetet tartalmazó szócikk
  szinte mindig egyben a leghosszabbak közé esik is (pl. ἐπί, G1909, 33 067 karakter, 226
  jelzet), ami a V csoport "változatosság" céljával szemben állna, és feleslegesen
  terhelné a G7 2 USD-s költségplafont. A 4 000 karakteres korláton belül a maximum:
  **G3777** (οὔτε, 2 345 kar., 50 jelzet). Döntetlennél a legkisebb Strong_padded dönt
  (nem volt rá szükség).

## 3. G5 ideiglenes terminológia

`naplok/FORDITAS_P_terminologia.tsv` (`angol`, `magyar`, `megjegyzes`, `verzio`), 13 sor:

- 3 sor a SZOTAR_BRIEF S2 induló javaslatából (`spirit` = szellem, `spiritual` = szellemi,
  `soul` = lélek);
- 10 sor a G1941 arany fordításából kinyert rövidítés-feloldás (`cf.` = vö., `cl.` =
  klasszikus, `pass.` = szenvedő alakban, `sc.` = ti., `see` = l., `Sept.` = Septuaginta,
  `i. e.` = azaz, `etc.` = stb., `p.` = o., `Heb.` = héb.) — mindegyik az arany szöveg
  tényleges, következetes fordítási megoldása, nem feltételezés.

A szövegkiadás-jelzetek (`L`, `T`, `Tr`, `WH`, `Rec.`, és az aranyban megfigyelt további
kritikai-apparátus sziglák, `R`, `G`) a G4/G5 szerint **változatlanok maradnak** — ezek nem
kerülnek a terminológiai táblába, mert nem fordítási megfeleltetések, hanem megőrzendő
jelölések.

## 4. Ellenőrzés

- 20 sor, 20 egyedi Strong (`assert` a szkriptben).
- Az E/N csoport a §0.2/§0.4 (FP0) mérésével egyezik (`assert` a szkriptben).
- Az arany (`G1941`) a mintában is szerepel (A csoport), forrásszövege ugyanaz, mint a
  `FORDITAS_P1_arany.tsv`-ben — a különbség csak az, hogy a minta táblázat nem tartalmazza
  a `forditas_hu`-t.
