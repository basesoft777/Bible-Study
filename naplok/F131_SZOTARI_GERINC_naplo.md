# F131 napló — a motívumlap szótári gerince (pilot: ISTENTISZT-001)

*2026.10.26 · ág: `ccr-6dc5ac47-lksrko` · brief: `F131_SZOTARI_GERINC_BRIEF.md` · alap: `0a8fdf5a` (main; a #127, #110, #132 lezárva)*

## 0. Előfeltételek (0.1)

- #127 `lezarva`, #110 `lezarva`, #132 `lezarva` (a fejléc `fugg`-ja, DT282).
- A felhasználó a `kovetkezo` mező várakozását kifejezetten felülbírálta; a feladat egyedül fut (nem csomag).
- `python eszkozok/feladatok.py ellenoriz`: 164 brief, 0 hiba, 0 figyelmeztetés.
- **Levezetett függés (a briefben nem szerepel):** a `feladatok.py fuggesek` a #131-et a #133-ra (`adat/bdb_szakaszok.tsv`) és a #144-re (`adat/bdb_szakasz_hu.tsv`) várónak mutatja, mert azok a #131 `olvas`-ában álló táblákat írják. Mindkettő `nem_indult`. Az `ir` fájljain más feladat nem fut (D39). A kérdés: DT-F131h (`DONTESEK.md`).

`scope=FELADATOK fejlécek | forras=python eszkozok/feladatok.py ellenoriz; fuggesek | ts=2026-10-26`

## 1. M0 — újramérés (0.2)

Eszköz: `naplok/F131_M0_meres.py` (csak olvas, `split('\t')`, `csv` nélkül). Minden szám egyetlen futás kimenetéből.

`scope=ISTENTISZT-001 (adat/elofordulasok.tsv, 32 sor); H7121, H8034, G1941 | forras=naplok/F131_M0_meres.py (adat/elofordulasok.tsv, adat/lexikon_hivatkozasok.tsv, adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv szurt≠1, adat/forditasok.tsv, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, lexikon/ISTENTISZT-001_TUDOMANYOS.md) | ts=2026-10-26 12:09`

### 1.1 Összevetés a brief 2. szakaszával

| Tétel (brief 2.) | A brief száma (2026-10-20) | M0 (2026-10-26) | Eltérés |
|---|---|---|---|
| ÓSZ-sorok `BDB`/`H7121` | 22 | 22 | — |
| `jelentes_szam` `2.c` / `2.c (rokon)` / `2.c (tagadva)` / `3` | 17 / 1 / 2 / 2 | 17 / 1 (Sof 3:9) / 2 (Jer 10:25, Zsolt 79:6) / 2 (2Móz 33:19, 34:5) | — |
| ÚSZ-sorok `TBESG`/`G1941`/`2` | 10 | 10 | — |
| H8034-re mutató sor | 0 | 0 (a `strong` mező 22 soron `H7121+H8034`) | — |
| `jelentes_hu` (ÓSZ) | „(NEM invokáció)” 2, „tagadó szerkezetben…” 2, „Baál nevével” 2, „Jahve nevével…” 1, üres 2 | ugyanaz; a maradék 13 sor „invokálni, segítségül hívni”; az ÚSZ 10 sora „segítségül hívni, invokálni” | — |
| `lexikon_hivatkozasok` BDB-sorok | 4 (`H7121 2.c`, `H7121 3`, `H8034 részlet`, `H3548 1`) | 4, ugyanazok | — |
| a `Niph'al/2/c` létezik a H7121-ben | igen | igen | — |
| `bdb_szakasz_hu` H7121 | 43 sor: `illeszkedik` 40, `jelolo_nelkul` 3 | ugyanaz | — |
| `bdb_szakasz_hu` H8034 | 12 sor: `illeszkedik` 6, `jelolo_nelkul` 5, `horgonnyal` 1 (`-/5/-`, `55:13`) | ugyanaz | — |
| a szakaszok magyar kezdete (`Qal/3/-`, `Qal/2/c`, `Qal/3/b`, H8034 `-/3/-`) | „3 kihirdetni:”, „c. … hívni ׳י nevével (azaz használni azt a segítségül hívásban): 1Móz 4:26; 12:8; …”, „b. … így (korábban) ׳ק י ׳בְשֵׁם 2Móz 33:19; 34:5 (JE)…”, „3 név, mint Isten megjelölése…” | ugyanaz | — |
| BDB-példa H7121 (`bdb_vers_jelentes`, `szurt≠1`) | 9 hivatkozás 8 versre: `Qal/2/c` 7, `Qal/3/b` 2 | ugyanaz (sorszám 92–97, 99: `Qal/2/c`; 128, 129: `Qal/3/b`) | — |
| BDB-példa H8034 | 6 hivatkozás 5 versre: `-/3` 4, `-/4` 1, `fej` 1 | ugyanaz (116–119: `-/3`; 208: `-/4`; 3: `fej`, 1Móz 12:8) | — |
| ellentmondás (BDB-példa nem esik a kutatói út alá) | 0 | 0 | — |
| a 2.29 ↔ 2.30 útvonal-alak | `-/3` ↔ `-/3/-` | ugyanaz | — |
| Thayer G1941 magyarul | `teljes` sor 4 601 karakter, szakasztábla nincs | `teljes` sor 4 601 karakter; **a #132 óta van angol szakasztábla** (l. 1.2); magyar szakaszsor (`sz<n>`) **0** a teljes `forditasok.tsv`-ben | **új** |
| a Thayer-motívumhelyek | szemrevételezve: 7 az 5. részben, 1 az 1.-ben (1Pét 1:17, „a határ bizonytalan”), 2 nincs idézve | **adatból** (`thayer_vers_jelentes.tsv`): `-/5/-` 6 (ApCsel 2:21, 9:14, Róm 10:12, 10:13, 1Kor 1:2, 2Tim 2:22), `-/1/-` 1 (1Pét 1:17), hivatkozás nélkül 3 (ApCsel 9:21, ApCsel 22:16, Róm 10:14) | az 5. részben 6, nem 7: az ApCsel 22:16 (a brief szerint „csak könyv nélkül, folytatásként”) a táblában nem kap hivatkozást; a többi egyezik, most adat |
| a teljes magyar Thayer számmintájának hamis találatai | „1. aorisztosz”, „3. személy”, „1. pontot”, „7. kiadásában” | ugyanezek, plusz „1. nevet” | — |
| UBS-domének G1941 | 33.176, 11.28, 33.131, `kezi` | ugyanaz (6 sor: glossza + definíció) | — |
| `(fordításra vár)` a lapon | 65 | 65 előfordulás 40 sorban | — |

### 1.2 Új adat a #132 után: a Thayer G1941 szakaszai

A `thayer_szakaszok.tsv` (SEMA 2.34) G1941-re 7 szakaszt ad: `cim`, `fej`, `-/1/-` … `-/5/-`, angolul. A `thayer_vers_jelentes.tsv` (SEMA 2.35) 43 G1941-sora közül 7 esik motívumhelyre:

| sorszam | Károli-vers | Thayer-útvonal |
|---|---|---|
| 15 | 1Pét 1:17 | `-/1/-` |
| 37 | ApCsel 2:21 | `-/5/-` |
| 39 | ApCsel 9:14 | `-/5/-` |
| 40 | Róm 10:13 | `-/5/-` |
| 41 | 1Kor 1:2 | `-/5/-` |
| 42 | Róm 10:12 | `-/5/-` |
| 43 | 2Tim 2:22 | `-/5/-` |

Hivatkozás nélkül: ApCsel 9:21, ApCsel 22:16, Róm 10:14.

A szakaszonkénti magyar Thayer a #142 (THAYER_M3, `nem_indult`, Sonnet) dolga; amíg az nem fut, a G1941 magyar szövege csak a `teljes` sor. Ez a DT-F131c opcióit megváltoztatja (l. `DONTESEK.md` DT-F131c).

Az 1Pét 1:17 a Thayer saját besorolásában az 1. részben áll („to put a name upon, to surname”), a kutatói hozzárendelés a TBESG 2 („segítségül hívni”). A két tagolás különböző szótáré, ezért a brief elsőbbségi szabálya (a BDB-példa a kutatói út alá esik-e) itt nem értelmezhető; a görög címkéről a DT-F131c dönt.

### 1.3 Az #144 tárgya az arany Strongokon

A #144 a `bdb_szakasz_hu.tsv` csak a jelölőt hordozó `illeszkedik` sorait javítja. A H7121-en és a H8034-en ilyen sor **0**; a két Strong a #144 alapjelentésében (`naplok/BDB_SZAKASZ_HU_JELOLO_JELENTES.md`) és briefjében nem szerepel. A #133 csak a fejléc-literálokat írja át (a sorok változatlanok). (DT-F131h.)

### 1.4 A #121 62 egységének sorsa egységenként

A lap 65 `(fordításra vár)` jelölése 40 egységen áll (a nyelvenkénti blokkban ugyanaz a tW-szócikk kétszer: G1941 és H7121 alatt). A #121 62 egysége (48 UBS DBH, 2 DNTG, 1 TBESH, 1 Mounce, 10 tW) a glossza- és definíciómezőt külön egységnek, a tW-szócikket egyszer számolja; a 65 = 62 + 1 (a `kt/call-speakloudly` második helye) + 2 (BDB `fej`).

| Nyelv | Szerep | Egység | Jelölés | Sors (a DT-F131a 1. vagy 2. opciója szerint) |
|---|---|---|---|---|
| G1941 | 3. Teológiai szócikk | tW `kt/call-speakloudly` | 1 | lekerül (tW, DT272 (b)) |
| G1941 | 5. Tömör jelentés | DNTG `001957001003000` (56.15) glossza + definíció | 2 | lekerül (teljes UBS) |
| G1941 | 5. Tömör jelentés | Mounce (GK 2126) | 1 | lekerül (DT272 (c), DT235) |
| H8034 | 1. Alapjelentés | TBESH H8034 (teljes) | 1 | lekerül (TBESH) |
| H7121, H8034 | 3. Teológiai szócikk | tW `kt/call-speakloudly`, `kt/call-toname`, `kt/call-tosummon`, `other/cry`, `other/declare`, `other/praise`, `other/preach`, `other/renown`, `kt/pray`, `other/report` | 10 | lekerül (tW) |
| H7121 | 5. Tömör jelentés | DBH `006562001001000`–`006562001012000`, `006562002001000`–`006562002007000` (19 lexid, glossza + definíció) | 38 | lekerül (teljes UBS) |
| H8034 | 5. Tömör jelentés | DBH `007442001001000`–`007442001004000`, `007442002001000` (5 lexid, glossza + definíció) | 10 | lekerül (teljes UBS) |
| H7121 | 8. Nyelvi háttér | BDB H7121 `fej` | 1 | **a DT-F131a (ii)-től függ**: a gerincbe vonva megszűnik (a `bdb_szakasz_hu.tsv` `fej` sora magyarul megvan: „H7121. qara I. קָרָא … ige: hívni, kihirdetni, olvasni …”); a 8. szerepben maradva marad |
| H8034 | 8. Nyelvi háttér | BDB H8034 `fej` | 1 | ugyanígy („H8034. shem I. שֵׁם … hímnemű főnév … név …”) |

Összesen: a 62 #121-egység mind lekerül (az 1. és a 2. opció szerint; a 3. szerint egyik sem); a 2 BDB-`fej` jelölés a (ii)-től függ. A rokon szavaknál (G0994, G2564) jelölés nincs. A héber 9. szerep (versenkénti UBS DBH-tábla) jelölést nem hordoz, de angol glosszákat igen; a teljes UBS-szel lekerül (N-F121b).

### 1.5 Ami a brief 2. szakaszához képest nem változott

A 2. szakasz minden más száma egyezik; a briefet a 0.3 előtt nem kell átírni. Az eltérések: a Thayer-szakasztábla megléte (#132) és a #133/#144 levezetett függése — mindkettő döntési tétel lett.

## 2. ⛔ 0.3 — megállás

A DT-F131a–e (a brief 5. szakasza, az M0 szerint pontosítva) és az M0-ból adódó DT-F131h a `DONTESEK.md`-ben, 🟡 állapotban. A végrehajtás (1. lépés, `F131.1`) a döntés után indul.
