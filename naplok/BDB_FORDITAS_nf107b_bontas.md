# BDB_FORDITAS — a 98 N-F107b Strong újrafordítása: tábla-Δ és commitonkénti bontás (E17, DT3)

*A #38 (BDB_FORDITAS) 98 N-F107b Strong szakaszonkénti újrafordításának független ellenőrzése (`naplok/ELLENOR_F38_nf107b.md`, 6. tétel), javítókör 1 (`/elteres`). Tartomány: `fb53abbf` (a menet előtti alap) → az utolsó adat-commit (`681afc39`). Minden szám saját méréssel készült; az adatsor a komment- (`#`) és a fejlécsor nélküli, nem üres sor. Minta: `naplok/BDB_FORDITAS_adag7_bontas.md`.*

## 1. Tábla-Δ

| tábla | alap (`fb53abbf`) | fej (`681afc39`) | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` | 3 006 | 5 360 | +2 354 | 2451 / 97 |
| minden más `adat/` tábla | — | — | 0 | — |
| `konkordancia/` (minden tábla) | — | — | 0 | — |

A 2 354 új sor mind `sz<n>` sor (a 98 Strong teljes szakaszszáma; a szakasztábla szerint 2 354). A 97 módosított (−/+) sor a 97 régi `teljes` sor `elavult`-ra állítása: 95 az 1–4. szeletben, 2 (H2416, H5315) a javítókörben. A `numstat` +2 451 = 2 354 új + 97 módosított sor; a 95 szelet-beli sor `megjegyzes` mezőjét a `DT-F128e` → `DT289` csere (`ae721bbf`) még egyszer átírta, de ez a két végállapot-különbség között nem látszik (ugyanaz a 95 sor). Törölt sor: 0. A H8415 régi, jóváhagyott `kezi` sora változatlan.

Más változott fájl: `eszkozok/emeles.py` (1 / 1: a beégetett „DT-F128e” → „DT289”), `naplok/EMELES_munka.tsv` (2354 / 3), `F38_BDB_FORDITAS_BRIEF.md` (fejléc), `naplok/ELLENOR_F38_nf107b.md`, `DONTESEK.md` (DT-F38o, a fő szál sora; a javítókör nem nyúlt hozzá), és ez a napló.

*(proveniencia: scope=adat/forditasok.tsv @ fb53abbf és @ 681afc39; adat/, konkordancia/ | forras=`git show <rev>:adat/forditasok.tsv`, `split('\t')`, megszámolt nem üres, nem `#` sor a fejléc nélkül (→ 3006 és 5360); `git diff --numstat fb53abbf HEAD -- adat konkordancia naplok/EMELES_munka.tsv eszkozok` (→ 2451 97 adat/forditasok.tsv; 1 1 eszkozok/emeles.py; 2354 3 naplok/EMELES_munka.tsv) | ts=2026-10-25T18:47Z)*

## 2. Commitonkénti bontás (`adat/forditasok.tsv`)

Új sor: a commit utáni sorok, amelyeknek az 5 elsődleges kulcsmezője (`szotar`, `strong`, `entry_id`, `jelentes_szam`, `mezo`) a szülőben nem szerepelt. Módosított: ugyanaz a kulcs, de a sor tartalma más. Az `elavultra` a módosítottak közül az, amelyiknek az `allapot` mezője az `elavult` értékre változott.

| commit | tartalom | új sor (`sz<n>`) | `elavultra` állított | egyéb módosított | törölt | érintett Strong |
|---|---|---|---|---|---|---|
| `2dc9663e` | 1. szelet | 360 | 10 | 0 | 0 | 10 |
| `ff497bd1` | 2. szelet | 416 | 9 | 0 | 0 | 9 |
| `cc4bf755` | 3. szelet | 672 | 27 | 0 | 0 | 27 |
| `0c935e7f` | 4. szelet | 822 | 49 | 0 | 0 | 49 |
| `ae721bbf` | javítókör: „DT-F128e” → „DT289” a `megjegyzes`-ben (8.) | 0 | 0 | 95 (`megjegyzes`) | 0 | 95 |
| `3706ef49` | javítókör: H3789, H5324, H3117 hű fordítása, kapu-felülbírálás, DT-F38o (1., 2., 7.) | 0 | 0 | 86 (82 `megjegyzes`; 4 `forditas_hu` + `megjegyzes`) | 0 | 3 |
| `39e16970` | javítókör: H1984 sz21, H6242 sz14 pótlás (7.) | 0 | 0 | 2 (`forditas_hu`) | 0 | 2 |
| `8b1d7761` | javítókör: H8415 (`--kezi-marad`, DT290 (3)) (3.) | 11 | 0 | 0 | 0 | 1 |
| `681afc39` | javítókör: H2416, H5315 (`--regi-elavult`, DT289 (2)) (4.) | 73 | 2 | 0 | 0 | 2 |
| **összesen** | | **2 354** | **97** | (a javítókör felülírásai) | **0** | **98** |

Ellenőrzés: 360 + 416 + 672 + 822 + 11 + 73 = 2 354 = az 1. szakasz Δ-ja; 3 006 + 2 354 = 5 360. A 4 módosított sor a `3706ef49`-ben a H3789 sz12, a H5324 sz4, a H3117 sz34 és sz38; a többi 82 sor ugyanennek a három Strongnak a többi szakasza, amelynek csak a `megjegyzes` mezője kapta a „kapu-felülbírálás: <kapu> (DT-F38o)” jelölést (a H1984 és a H6242 sorain nincs felülbírálás-jelölés).

**A `0c935e7f` commitüzenetének hamis számai** (ELLENOR_F38_nf107b 3.): az „871 szakaszsor” a `git diff --numstat` hozzáadott soraiból jött (822 új `sz` sor + az 49 `elavult`-ra módosított sor); a helyes szakaszsor-szám 822. A „98 mind lefordítva” sem volt igaz: a 4. szelet végén 95 Strong készült el (a H2416, H5315 és H8415 hiányzott). A commitüzenet utólag nem javítható (történet-újraírás nincs); a helyes számokat ez a napló, a brief `kovetkezo` mezője és a `3706ef49`–`681afc39` commitok rögzítik.

*(proveniencia: scope=adat/forditasok.tsv @ <commit>^ és @ <commit>, kilenc commit: 2dc9663e, ff497bd1, cc4bf755, 0c935e7f, ae721bbf, 3706ef49, 39e16970, 8b1d7761, 681afc39 | forras=saját szkript (`git show <rev>:adat/forditasok.tsv`, `split('\t')`, kulcs = az első öt mező; módosított = azonos kulcs, eltérő sor; `elavultra` = az `allapot` (8. mező) értéke a szülőben nem, a commitban `elavult`) | ts=2026-10-25T18:47Z)*

## 3. Szeletenként a Strongok és a forráskarakterszám

**A mérés módja.** A szelet Strongjai: a 2. szakasz szerint az adott commitban hozzáadott `strong` értékek. (a) A `adat/bdb_szakaszok.tsv` `szoveg` oszlopának karakterhossza (Python `len`) összegezve a Strong minden szakaszán. (b) Ugyanez a fordító tényleges bemenetén: `eszkozok/bdb_jelolt/szakasz_bemenet.py` `szakaszok(strong)` → `nezet(...)` (a javítások, pe/mem, alkalmazva; token nélkül). (c) A commitüzenet száma.

| szelet | commit | Strong | szakaszsor | (a) szakasz-`szoveg` | (b) javított nézet | (c) a commitüzenet szerint |
|---|---|---|---|---|---|---|
| 1. | `2dc9663e` | 10 | 360 | 153 938 | 155 052 | 155 058 (a törzsben `~155 000`) |
| 2. | `ff497bd1` | 9 | 416 | 153 003 | 154 540 | 153 463 a brief szerint; `~153 000` a commitban |
| 3. | `cc4bf755` | 27 | 672 | 157 557 | 159 886 | 160 012 a brief szerint; `~160 000` a commitban |
| 4. | `0c935e7f` | 49 | 822 | 174 617 | 177 409 | 177 530 |
| javítókör: H8415 | `8b1d7761` | 1 | 11 | 1 942 | 1 966 | — |
| javítókör: H2416, H5315 | `681afc39` | 2 | 73 | 23 452 | 23 669 | — |
| **összesen** | | **98** | **2 354** | **664 509** | **672 522** | |

A (b) összeg (672 522) azonos a DT289 mért 672 522 karakterével (a 98 Strong, 2 354 szakasz). Az (a) a nyers szakaszszöveg (a javítások nélkül), ezért kisebb; a commitüzenetek számai a (b)-hez közelebb állnak (a különbség 6, 1 077, 126, 121 karakter), de egyikkel sem azonosak, a méréskor használt alapjukat (valószínűleg a tokenes bemenet vagy a javítás előtti állapot) a commitok nem rögzítik; a 2. szelet brief-beli 153 463 a (b)-nél 1 077-tel kisebb.

A szeletek Strongjai:

- 1.: H0834 H1004 H3027 H3068 H3117 H3588 H3605 H3808 H5971 H6213
- 2.: H0259 H1980 H3947 H4480 H5869 H7200 H7725 H7971 H9008
- 3.: H0068 H0410 H0702 H1129 H1288 H1320 H1419 H1870 H2091 H2388 H2568 H2617 H3772 H3881 H3967 H4672 H4940 H5307 H5674 H6086 H6240 H6242 H7218 H7227 H7651 H7969 H8064
- 4.: H0157 H0352 H0539 H0637 H0995 H1197 H1242 H1568 H1875 H1984 H2220 H2396 H2398 H2451 H2470 H2506 H2572 H3083 H3092 H3254 H3384 H3423 H3603 H3644 H3722 H3742 H3789 H4217 H4264 H4605 H4639 H5127 H5324 H5797 H6588 H6942 H7122 H7323 H7626 H7657 H7673 H7896 H7901 H7993 H8074 H8083 H8130 H8337 H8672
- javítókör: H8415; H2416, H5315

A javítókör fordítási számai (a `szakasz_rogzit` kimenete, a fordítás karaktere): H8415 11 szakaszsor, 2 120 karakter; H2416 30 szakaszsor, 10 696 karakter; H5315 43 szakaszsor, 13 512 karakter. A H3789 (17 sor, 6 659), H5324 (20 sor, 4 182), H3117 (49 sor, 20 348), H1984 (28 sor, 10 422) és H6242 (20 sor, 1 856) a megadott szakaszokban módosult, a többi sora tartalmilag változatlan.

*(proveniencia: scope=adat/bdb_szakaszok.tsv (`szoveg` oszlop), `eszkozok/bdb_jelolt/szakasz_bemenet.py` `szakaszok()`/`nezet()` | forras=saját szkript (`split('\t')`, `len()` karakterekben, Strong-halmaz a 2. szakasz szerint) | ts=2026-10-25T18:47Z)*

## 4. A kapu-felülbírálások és a nyitott pont

- DT-F38o: `5_terminologia` (H3789 sz12, H5324 sz4), `8_idezojel` (H3117 sz34, sz38). Csak a megnevezett kapu bukott; a többi kapu átment. A `megjegyzes`-jelölés a Strong sorain áll.
- A H8415 új szakaszsorai `allapot=sonnet`; a `kezi` állapotot csak a felhasználó jóváhagyása után kaphatják (DT290 (3)). Addig a régi `teljes` `kezi` sor az érvényes.
- A `eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py` `test_kezi_regi_sor_dt_f128f` tesztje a valódi `forditasok.tsv`-t másolta, és a H8415 szakaszsorainak hiányát feltételezte; a H8415 beírása után elbukott. A tesztkör most a másolatból elhagyja a vizsgált Strong valódi `sz` sorait (csak a régi `teljes` sor marad); a teszt tartalma és az eszköz nem változott (F38.380).
- Nyitott: a (b) és (c) közti eltérés oka (3. szakasz); a kovetkezo/commit-üzenet hamis számai utólag nem javíthatók.
