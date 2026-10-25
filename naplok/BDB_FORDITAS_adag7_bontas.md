# BDB_FORDITAS 7. adag — tábla-Δ és commitonkénti bontás (E17, DT3)

*A #38 (BDB_FORDITAS) 7. adagjának független ellenőrzése (`naplok/ELLENOR_F38_adag7.md`, 4. tétel), javítókör 1. Tartomány: `61714f36` (a 7. adag előtti alap: `szamkiosztas: DT-F96c → DT301`, a `git merge-base` az ág fejével) → az ág feje a mérés idején (`451077c`). Minden szám saját méréssel készült; az adatsor a komment- (`#`) és a fejlécsor nélküli, nem üres sor. Minta: `naplok/F127_bontas.md`.*

## 1. Tábla-Δ

| tábla | alap (`61714f36`) | fej (`451077c`) | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` | 737 | 2 998 | +2 261 | 2261 / 0 |
| minden más `adat/` tábla | — | — | 0 | — |
| `konkordancia/` (minden tábla) | — | — | 0 | — |

A `git diff --numstat 61714f36 HEAD -- adat konkordancia` egyetlen fájlt ad (`adat/forditasok.tsv`); a többi `adat/` és `konkordancia/` tábla változatlan (Δ = 0). A 2 261 sor tisztán hozzáadott (0 törölt, 0 módosított): a régi `teljes` sorok `elavult` jelölése a 7. adagban nem írta át a meglévő sorokat, hanem újakat adott hozzá. A repó más változott fájljai (nem `adat/`, nem `konkordancia/`): `DONTESEK.md`, `F38_BDB_FORDITAS_BRIEF.md`, `eszkozok/forditas_kapuk.py`, `eszkozok/teszt_forditas_kapuk.py`, `naplok/BDB_FORDITAS_hibas.tsv`, `naplok/EMELES_munka.tsv` (+2 263), `naplok/ELLENOR_F38_adag7.md`.

*(proveniencia: scope=adat/forditasok.tsv @ 61714f36 és @ 451077c; adat/, konkordancia/ | forras=`git show <rev>:adat/forditasok.tsv \| grep -v '^#' \| tail -n +2 \| grep -c .` (→ 737 és 2998); `git diff --numstat 61714f36 HEAD -- adat konkordancia` | ts=2026-10-25T11:08Z)*

## 2. Commitonkénti bontás (`adat/forditasok.tsv`)

A hozzáadott sor = a commit utáni sorok, amelyek a commit szülőjében nem voltak meg (teljes soregyezés). A `sz<n>`: a `jelentes_szam` mező `sz`-szel kezdődő (szakaszos út), a `teljes`: a régi egész-szócikkes út.

| commit | tartalom | hozzáadott sor | Strong | `sz<n>` sor | `teljes` sor |
|---|---|---|---|---|---|
| `26ec7bd` | köztes állapot (47 szócikk csak a `naplok/EMELES_munka.tsv`-ben) | 0 | 0 | 0 | 0 |
| `9358d5b` | 7a (kisebbített szelet) | 663 | 84 | 663 | 0 |
| `9ccbd84` | H4725 (8. kapu «-javítása, DT-F38j) | 1 | 1 | 0 | 1 |
| `5931be1` | 7b | 695 | 92 | 695 | 0 |
| `6244e1c` | 7c | 682 | 102 | 681 | 1 (H8065) |
| `08f4c80` | 7d | 220 | 37 | 220 | 0 |
| **összesen** | | **2 261** | **316** | **2 259** | **2** |

A 663 + 1 + 695 + 682 + 220 = 2 261 egyezik az 1. szakasz Δ-jával; a `sz<n>` 2 259 + `teljes` 2 = 2 261. A teljes tábla `jelentes_szam` megoszlása a fejen (a régi adagokkal együtt): 2 259 `sz<n>`, 690 `teljes` (a többi sor számozott jelentés-azonosító).

*(proveniencia: scope=adat/forditasok.tsv @ <commit>^ és @ <commit>, a hat commit: 26ec7bd, 9358d5b, 9ccbd84, 5931be1, 6244e1c, 08f4c80 | forras=saját szkript (`git show <rev>:adat/forditasok.tsv`, `split('\t')`, a szülőben nem szereplő sorok; `jelentes_szam` oszlop `startswith('sz')` / `== 'teljes'`; Strong = a 2. oszlop különböző értékei) | ts=2026-10-25T11:08Z)*

## 3. Szeletenként a forráskarakterszám

A 7a és 5931be1 commitüzenete kerek számot ad (150 535, 150 036), a 7c (`~150 000`) és a 7d (`kb. 48 800`) csak közelítést; a brief szerinti pontos szám a 7c-ből és a 7d-ből hiányzik. **A mérés módja:** a szelet Strong-jainak (a 2. szakasz commitjaiban hozzáadott `strong` értékek) forrásszövege. (a) A szakaszos úton (`sz<n>`) a `adat/bdb_szakaszok.tsv` `szoveg` oszlopának karakterhossza (Python `len`) összegezve az adott Strongra tartozó szakaszsorokon. (b) A `teljes` úton fordított szócikkeknél (H4725 a 7a-ban, H8065 a 7c-ben) a `konkordancia/BDB_teljes_unabridged.tsv` `Teljes_szocikk` oszlopának hossza. Összehasonlításul a (c) oszlop a szelet minden Strongjának `Teljes_szocikk`-hossza összegezve.

| szelet | commit(ok) | Strong | (a) szakasz-`szoveg` | (b) `teljes` út | (a)+(b) | (c) unabridged összes | a commitüzenet szerint |
|---|---|---|---|---|---|---|---|
| 7a | `9358d5b` + `9ccbd84` | 85 (84 + H4725) | 143 243 | 5 223 | 148 466 | 137 998 | 150 535 (84 szócikk) |
| 7b | `5931be1` | 92 | 147 856 | 0 | 147 856 | 135 520 | 150 036 |
| 7c | `6244e1c` | 102 | 145 562 | 884 (H8065) | 146 446 | 120 598 | `~150 000` |
| 7d | `08f4c80` | 37 | 48 187 | 0 | 48 187 | 47 342 | `kb. 48 800` |
| **összesen** | | **316** | **484 848** | **6 107** | **490 955** | **441 458** | |

**Eltérések, amelyeket a mérés nem old fel:** a 7a és a 7b commitüzenetének száma (150 535, 150 036) magasabb, mint az (a)+(b) mérés (148 466, 147 856); a mérés módját a commitüzenet nem rögzíti, így az eltérés oka (valószínűleg más karakter-alap, pl. a szakasz-előkészítő bemenet fejléce vagy a szakaszhatár-kontextus) nem állapítható meg. Az (a)+(b) szám az adag forrásmennyiségének alsó, a szakaszbemenetre épülő becslése; a (c) a szócikkek szakaszolatlan teljes szövege. Az (a) a 7a-ban és a 7d-ben nagyobb, mint a (c); ennek okát (a szakasztábla bontása, ismétlődő kontextus) nem vizsgáltam, ez nyitott megfigyelés. A 7c és 7d hiányzó pontos számát ez a napló pótolja az (a)+(b) mérés szerint: 7c 146 446, 7d 48 187 karakter.

*(proveniencia: scope=adat/bdb_szakaszok.tsv (`szoveg` oszlop), konkordancia/BDB_teljes_unabridged.tsv (`Teljes_szocikk` oszlop) | forras=saját szkript (`split('\t')`, `len()` karakterekben, Strong-halmaz a 2. szakasz szerint) | ts=2026-10-25T11:08Z)*
