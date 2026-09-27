# CI_alapallapot — CI.0 (alapállapot-mérés)

*Forrás: `CI_ELLENORZES_BRIEF.md`, CI.0 tétel. Első mérés: `--teljes`, teljes
repóra, 2026.09.26. **Ez a 2. mérés**, a D8–D15 (a felhasználó jóváhagyása,
2026.09.27) átvezetése után, `origin/main` (`4b9ae49`) tetejére rebase-elt
ágon. Az E1-et (SEMA §3 1–12, Q1, Q7) a meglévő `eszkozok/ellenoriz.py` már
gépesíti — ez a mérés nem ismétli meg.*

## A D8–D15 hatása a mérési módszerre

- **D8** — mostantól a HIBA a diff által **hozzáadott/módosított sorokra**
  vonatkozik, nem a teljes fájlra. `--teljes` módban nincs diff (nincs
  base/head), ezért minden szabály **JELENTÉS** szinten fut — ez a mérés
  tehát a valós PR-hatókörnél *tágabb* felső korlát, nem a tényleges
  HIBA-szám. E4, E5, E6, E7, E16 kivétel (`SZ.FAJLSZINTU_SZABALYOK`):
  ezek motívum-/fájl-szintű állítások, nem egy konkrét sorhoz köthetők,
  így diff-módban is a saját szintjükön jelentkeznek majd.
- **D9–D12** — E2, E9, E11 hatóköre/mintája szűkült (l. lent szabályonként).
- **D13** — E12, E13 hatóköre `tematikus_lezart/`, `genezis/`,
  `ujszovetseg/`, `melyelemzesek/`, `motivumlog/`, `lexikon/`-ra szűkült
  (korábban a teljes repó, beleértve a brief-/tervdokumentumokat is).
- **D14** — `naplok/CI_*.md` és `naplok/ELLENOR_*.md` minden szabály alól
  kizárva.

## Összegzés — 1. mérés → 2. mérés (D8–D15 után)

| Szabály | Szint (D9–D13 után) | 1. mérés (teljes fájl, teljes repó) | 2. mérés (szűkített minta/hatókör) |
|---|---|---|---|
| E2 | HIBA (szűkítve, D10) | 140 | **7** |
| E3 | HIBA | 0 | 0 |
| E4 | HIBA (fájlszintű) | 0 | 0 |
| E5 | HIBA (fájlszintű, diff-alapú) | 0 (N/A) | 0 (N/A, `--teljes`-ben nincs diff) |
| E6 | HIBA (fájlszintű) | 1 | 1 |
| E7 | HIBA (fájlszintű) | 0 | 0 |
| E8 | HIBA (kizárva: inline kód/kódblokk, D16) | 0 | 0 |
| E9 | HIBA (szűkítve, D11) | 99 | **86** |
| E10 | HIBA (szűkítve+hatókör, D17) | 0 | 0 |
| E11 | HIBA (szűkítve+hatókör, D12) | 61 | **9** |
| E12 | FIGYELMEZTETÉS (hatókör, D13) | 4087 | **1853** |
| E13 | FIGYELMEZTETÉS (hatókör, D13) | 3837 | **1395** |
| E14 | FIGYELMEZTETÉS | 0 | 0 |
| E15 | FIGYELMEZTETÉS | 0 | 0 |
| E16 | HIBA (fájlszintű, PR-alapú) | 0 (N/A) | 0 (N/A, `--teljes`-ben nincs PR-cím) |

**E8/E10 története — 2. mérés → 3. mérés (D16–D18 után).** A 2. mérésben,
miután a `CI_ELLENORZES_BRIEF.md` maga bekerült a repóba, E8 3, E10 2
találatot adott — mindkettő a brief saját táblázatának szó szerinti
idézete volt (`` `1 Móz` ``, "spirit = szellem, ... soul = lélek"), nem
tényleges study-/adatréteg-sértés. A saját PR-diffre futtatva ez exit
1-et okozott, mert ezek a sorok a diffben "hozzáadott sor"-nak számítottak
(D8) — a D14 root-szintű brieffájlokra nem terjed ki, és E8/E10-nek nem
volt hatókör-szűkítése.

A javítás (D16, D17, D17a):
- **E8** kizárja a backtickes inline kódot és a kódblokkot — a brief
  táblázata pont ilyen backtickben idézi a tiltott mintákat.
- **E10** hatóköre `adat/` és `lexikon/`-ra szűkült (a szótári fordítás
  tényleges helye), a gyökér brief-/tervfájlok kívül esnek rajta. A D17
  eredetileg inline kódot ÉS idézőjeles/blockquote-példát is kizárt volna,
  de a D17a ezt pontosította: csak az **inline kód** marad kizárva — a
  hatókör-szűkítés önmagában elég volt az önhivatkozás ellen, az
  idézőjel-/blockquote-kizárás viszont a lexikon valódi magyar
  glosszáit (idézőjelben, pl. `„lélek"`) és a Thayer-fordítás (#7)
  blockquote-os renderjét rejtette volna el.

A 3. mérésben (`--teljes`) mindkettő **0**-ra esett vissza. A saját
PR-diffre (`origin/main..HEAD`, `--pr-cim "[ELLENŐRZŐ] CI.0–CI.5"`)
futtatva minden szabály 0 találatot ad, a `futtat.py` kilépési kódja 0.

(Közben, a CI.1 tesztírás során egy másik hiba is kiderült és javításra
került: az eredeti E10-minta a `lel(ek|ki)` alakot kereste, ami az
ékezetes "lélek" szót nem ismerte fel.)

## Találatszám könyvtáranként (2. mérés, `--teljes`)

| Szabály | Könyvtárankénti bontás |
|---|---|
| E2 (7) | gyökér: 3 · lexikon: 2 · tematikus_lezart: 2 |
| E6 (1) | tematikus_lezart: 1 |
| E9 (86) | motivumlog: 20 · lexikon: 17 · gyökér: 13 · naplok: 13 · tematikus_lezart: 12 · sablonok: 8 · adat: 2 · motivumok: 1 |
| E11 (9) | lexikon: 9 |
| E12 (1853) | lexikon: 1129 · motivumlog: 260 · tematikus_lezart: 257 · genezis: 193 · ujszovetseg: 11 · melyelemzesek: 3 |
| E13 (1395) | genezis: 553 · lexikon: 306 · tematikus_lezart: 263 · motivumlog: 234 · ujszovetseg: 33 · melyelemzesek: 6 |
| E3, E4, E5, E7, E8, E10, E14, E15, E16 | 0 találat mindenhol (3. mérés, D16–D18 után) |

A lexikon/ magas E12/E13-részesedése várható: ez a kimenet-réteg, generált
fájlokból (l. CLAUDE.md "Rétegek" szakasz) — a forrás javítása után
újragenerálódik, tehát ezek a találatok nem a study-szerzés hibái, hanem a
generátor jövőbeli feladatai (E12/E13 egyelőre FIGYELMEZTETÉS marad, D13).

## Minta-találatok szabályonként (max. 3, 2. mérés)

### E2 — szűkített jelölés (🔍/🔬/STEPBible-ellenőrizve) proveniencia nélkül (7)
- `Atadasi_dokumentum_2026_09_11.md:189` -- memóriából, de jelölni kell. *Incidens: egy "🔍 STEPBible-ellenőrizve"
- `F8_BRIEF.md:62` -- | G4 | Az **`ellenoriz.py` hatóköre:** ... `--study <fájl>` esetén Q1 és Q7 ...
- `Join_tabla_folyamat_magyarazat.md:71` -- | Kapcsolódás a Lezárási checklisthez | ... igen — a 11. pont (🔍 STEPBible-ellenőrizve) ...

### E6 — hiányzó "0. Forrás-összegyűjtés" (1)
- `tematikus_lezart/Pneuma_pszukhe_megkulonboztetes_tematikus.md:0` -- hiányzik a "0. Forrás-összegyűjtés" szakasz

### E9 — angol "sense", blockquote/kódblokk nélkül (86)
- `Atadasi_dokumentum_2026_09_11.md:145` -- ### 3.8 ⚠️ Sense-szám mező nem-numerikus értékei — indoklás nélkül
- `Atadasi_dokumentum_2026_09_11.md:149` -- igegyököket binyan szerint tagolja, nem számozott sense-ekkel. Ez
- `F4_GENERATOR_BRIEF.md:576` -- Strong-szám(ok) | BDB-entry-id | Sense-szám | Jelentés-szöveg (EN + HU).

### E11 — Cremer/NIDNTTE/NIDOTTE, `lexikon/`-hatókörben (9)
- `lexikon/ALVIL-001_TORZSCIKK.md:1150` -- Cremer említve: | Teológiai szócikk | Cremer (1895) | Girdlestone (1897) + Cremer héber mutatója; TWOT-szám hivatkozásként |
- `lexikon/ANTROP-001_TORZSCIKK.md:195` -- ugyanez a sor
- `lexikon/HAMART-001_TORZSCIKK.md:971` -- ugyanez a sor

*(A D12 szerint ez a 8 törzscikk ismert régi Cremer-sora — a SZOTAR S2.8
újragenerálása javítja, most nem javítandó. Diff-módban ezek a sorok — mivel
nem részei egyetlen jövőbeli PR diffjének sem, amíg a generátor újra nem
írja őket — JELENTÉS szinten maradnak, nem blokkolnak.)*

### E12 — proveniencia prózában, szűkített hatókörben (1853)
- `genezis/1Moz_10v1-11v32_bovitett.md:4` -- *v7 — 2026.09.03 (Sod-pont kiegészítve ...)*
- `genezis/1Moz_10v1-11v32_bovitett.md:9` -- *v6 — 2026.08.15 (...)*
- `genezis/1Moz_10v1-11v32_bovitett.md:116` -- Ehhez a mintázathoz egy önálló lexikai szál is társul: ...

### E13 — kiejtés hiánya, szűkített hatókörben és mintával (1395)
- `genezis/1Moz_10v1-11v32_bovitett.md:4` -- *v7 — 2026.09.03 (Sod-pont kiegészítve a מִגְדָּל/אֲגַדְּלָה [11:4↔12:2] közös...*
- `genezis/1Moz_10v1-11v32_bovitett.md:5` -- גדל gyök lelettel — ellentétes visszhang: Bábel önerőből, Ábrám ajándékba
- `genezis/1Moz_10v1-11v32_bovitett.md:60` -- | 10:1 | תּוֹלְדֹת | *toledot* | H8435 | nemzetség(történet), "amik születtek" |

## Következő lépés

A megállás lezárva (a felhasználó jóváhagyta a D8–D15-öt); a munka
CI.1-gyel folytatódik.
