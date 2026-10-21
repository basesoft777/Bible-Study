# F127 — tábla-Δ és a `res_forras.tsv` +16 sorának bontása (DT3)

*A #127 (LEXIKON_HALO_RES) javítókörének 1. köre, a független ellenőrzés 4. ELTÉRÉS-tétele (`naplok/ELLENOR_F127.md`, „Lista 4”). Tartomány: `9d602794` (a feladat ágának alapja) → az ág feje a mérés idején (`15ef1a2b`, F127.20; a mért táblák az F127.16 óta nem változtak). Mindegyik szám saját méréssel készült; az adatsor a komment- (`#`) és a fejlécsor nélküli, nem üres sor.*

## 1. Tábla-Δ

| tábla | alap (`9d602794`) | fej | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/jeloltek.tsv` | 627 | 634 | +7 | 636 / 629 |
| `adat/motivum_kapcsolatok.tsv` | — (nem létezett) | 3 | +3 (új tábla) | 5 / 0 |
| `adat/res_forras.tsv` | 56 | 72 | +16 | 16 / 0 |
| `konkordancia/` | — | — | 0 (0 változott fájl) | — |

*(proveniencia: scope=adat/jeloltek.tsv, adat/res_forras.tsv, adat/motivum_kapcsolatok.tsv, konkordancia/ @ 9d602794 és @ 15ef1a2b | forras=`git show <rev>:<fájl> \| grep -v '^#' \| tail -n +2 \| grep -c .`; `git diff --numstat 9d602794..HEAD`; `git diff --name-only 9d602794..HEAD -- konkordancia/ \| wc -l` | ts=2026-10-21T06:05Z)*

A `jeloltek.tsv` numstatja (636 / 629) nem 7 új sort jelent 629 törléssel: az F127.9 kulcsbővítése (DT-F127d) a 627 régi adatsort, a fejlécet és a kommentsort négy új oszloppal írta vissza, az első 9 mező változatlan; ezt a független ellenőrzés word-diff-fel igazolta (`naplok/ELLENOR_F127.md`, „DT-F127d (627 sor, első 9 mező)” és „Lista 1”). A +7 a `jelolt_tipus` szerint:

| `jelolt_tipus` | `dontes` | sor |
|---|---|---|
| `elofordulas` | `beépítve` / `elutasítva` / `nyitva` | 260 / 318 / 49 (= 627, a régi sorok) |
| `motivumkozi` | `beépítve` | 2 |
| `motivumkozi` | `nyitva` | 5 |

A 2 `beépítve` motívumközi jelölt 3 kapcsolat-sort ad, mert a DT-F127e (b) jelöltje (ISTENTISZT-001 ApCsel 2:21) két célverset (ALVIL-001 ApCsel 2:27 és 2:31) köt össze (DT-F127e F2, F127.13); a (d) (1Móz 12:8 ↔ HAMART-001 1Móz 12:3) egy sort ad.

*(proveniencia: scope=adat/jeloltek.tsv @ 15ef1a2b | forras=`git show HEAD:adat/jeloltek.tsv \| grep -v '^#' \| tail -n +2 \| awk -F'\t' '{print $10" \| "$4}' \| sort \| uniq -c` | ts=2026-10-21T06:05Z)*

## 2. A `res_forras.tsv` +16 sorának bontása: 2 + 14

A DT-F127a (3. opció; a 7 nem migrált motívumnál (i)) és az F127.4 commit (`72e00b2b`) szerint mind a 8 éles lexikonoldal két új rést kap (`alkalmazas`, `tanitoi`): 8 × 2 = 16 sor.

| rész | motívum | sor | `forras` | `tanulmany` |
|---|---|---|---|---|
| **2** | ISTENTISZT-001 (migrált) | `alkalmazas` | `tanulmany` | `motivumok/ISTENTISZT-001.md` |
| | | `tanitoi` | `tanulmany` | `motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md` |
| **14** | ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001 (7 nem migrált) | `alkalmazas` + `tanitoi` motívumonként | `adat` (rögzített átmeneti mondat) | — |

Mért: a két új rés 16 sora `forras` szerint 2 `tanulmany` + 14 `adat`, 8 különböző motívumon; a `tanulmany` értékű kettő az ISTENTISZT-001-é. A régi 56 sor változatlan (numstat: 0 törölt sor). A végösszeg 72 = 8 motívum × 9 rés.

*(proveniencia: scope=adat/res_forras.tsv @ 15ef1a2b | forras=`git show HEAD:adat/res_forras.tsv \| grep -v '^#' \| tail -n +2 \| awk -F'\t' '$2=="alkalmazas"\|\|$2=="tanitoi"{print $4}' \| sort \| uniq -c` (→ 14 adat, 2 tanulmany); ugyanez `{print $1}`-gyel (→ 8 motívum); `$4=="tanulmany"` szűréssel az id, a res és a tanulmany mező | ts=2026-10-21T06:05Z)*
