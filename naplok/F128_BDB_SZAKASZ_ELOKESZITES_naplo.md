# F128 — A BDB szakaszonkénti fordításának előkészítése: napló

*Brief: `F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md` · ág: `claude/f128-bdb-szakasz-elokeszites-a2fc2f` (a main `72eee13d`-jéről) ·
végrehajtó: `claude-opus-5-5` (a brief `modell: opus` mezőjével egyezik).*

## M0 — felmérés (csak olvas)

A menet a felhasználó jóváhagyása szerint („mehet: a #128 egyedül, az M0 ⛔-ig”) az M0 ⛔ pontig fut. Kód a repóba nem került; a
mérés két eseti szkripttel futott a repón kívül (a menet scratchpadjában: `m0_meres.py`, `m0_meres2.py`). A TSV-ket `split('\t')`-tel
olvasták, csak olvastak. A nézetet a `eszkozok/bdb_jelolt/nezet_general.py` `general(pe_mem=False)` függvénye adta (importálva, a kimenet
nem íródott ki). Bemenetek az ág bázisán (`72eee13d`): `adat/forditasok.tsv` (737 sor), `adat/bdb_szakaszok.tsv`,
`adat/bdb_forras_javitas.tsv`, `adat/bdb_szakasz_hu.tsv`, `adat/lexikon_hivatkozasok.tsv`, `konkordancia/BDB_teljes_unabridged.tsv`,
`naplok/BDB_FORDITAS_sorrend.tsv`.

`scope=F128 M0 | forras=python m0_meres.py + m0_meres2.py (eseti, a repón kívül; nezet_general.general(pe_mem=False)) @72eee13d | ts=2026-10-21`

### 0. Kiinduló számok

| | érték |
|---|---|
| `adat/forditasok.tsv` sorai | 737 (BDB 678, UBS_DNTG 40, Thayer 14, TBESG 4, LSJ 1) |
| BDB-sorok `jelentes_szam` szerint | `teljes` 674, `2.c` 1, `3` 1, `1` 1, `részlet` 1 (a négy nem `teljes` sor `kezi`: H7121 ×2, H3548, H8034) |
| BDB `teljes` sorok | 674 sor = 674 Strong (Strongonként pontosan egy; üres `forditas_hu` 0); `allapot`: `sonnet` 648, `opus` 20, `kezi` 10 (a 678 sorra) |
| a kész Strongok illesztése (`bdb_szakaszok.tsv`) | `egyezik` 661, `szocikk_resze` 7, `reszleges` 3, `csonk` 2, `sikertelen` 1, táblán kívüli 0 |
| hátralék (`BDB_FORDITAS_sorrend.tsv`, nem kész) | 7 425 Strong (a táblában 7 416, táblán kívül 9); 26 957 szakasz; 3 559 007 karakter (nézet) |
| 7. adag | 317 Strong, sorszám 649–965, 499 483 karakter (a `sorrend` `karakter` mezője) |

`scope=adat/forditasok.tsv, naplok/BDB_FORDITAS_sorrend.tsv, adat/bdb_szakaszok.tsv | forras=m0_meres.py @72eee13d | ts=2026-10-21`

### 1. A `jelentes_szam = teljes` BDB-sorok olvasói (a tárolási kulcs, DT-F128a)

Keresés: `grep` a `forditasok.tsv` / `forditasok` / `'teljes'` mintákra az `eszkozok/`, `naplok/`, `.github/workflows/` alatt, majd a
találatok kódjának olvasása. Az alábbi tábla a futó (nem eseti) olvasókat sorolja; mit kellene átállítani (a) szakaszonkénti sorok
(`jelentes_szam = sz<sorszam>`) és (b) egy `teljes` sor határtokenekkel esetén.

| # | olvasó | mit olvas | (a) szakaszsorok | (b) `teljes` + token |
|---|---|---|---|---|
| 1 | **render**: `eszkozok/lexikon_general.py` (`forditas_ehhez`) | a BDB magyart csak a `lexikon_hivatkozasok.tsv` soraihoz, kulcs szerint; a 4 BDB-hivatkozás (H7121 `2.c`, `3`; H3548 `1`; H8034 `részlet`) egyike sem `teljes` | nincs teendő | nincs teendő |
| 2 | **olvasó szerver**: `olvaso_szerver/lekerdezesek.py` `bdb_magyar`, `bdb_magyar_meta` → `blokkok.py` `szo.bdb_magyar`, `szo.bdb_apparatus`, `alapjelentes` (a `bdb_szelet` a magyar szövegen) | a DB `forditasok` táblájából Strongonként az **utolsó nem üres** BDB-sor, `jelentes_szam`-tól függetlenül (`ORDER BY rowid`) | átállítandó: a szakaszsorok `sorszam` szerinti összefűzése; az utolsó sor ma csak az utolsó szakaszt adná | átállítandó: a token levétele (vagy a szeletelő a tokent használja határként) |
| 3 | `eszkozok/sqlite_epit.py` | a táblát általánosan tölti (manifest: `forditasok` 737 sor), és meghívja a 13. szabályt | a sorszám változik; teendő nincs | nincs teendő |
| 4 | **CI E1** (`ellenorzes.yml` → `eszkozok/ellenoriz.py` 13. szabály) | a kulcs egyedisége és a `forras_hash`: a forrásszöveg `teljes` sornál a TSV `Teljes_szocikk`-je; más `jelentes_szam`-nál a `lexikon_hivatkozasok.tsv`, ennek híján „nincs hozzá forrásszöveg” = SÉRTÉS | átállítandó: új forrás-ág az `sz<n>` sorokra (a szakasz bemenete a táblából és a javítótáblából) | átállítandó: az új `teljes` sorok hash-alapja nem a TSV (l. 2.), tehát a sorok megkülönböztetése kell |
| 5 | **CI E19** (`ellenorzes/szabalyok.py`) | a `lexikon_hivatkozasok.tsv` BDB-soraihoz kell `forditas_hu` ugyanarra a `jelentes_szam`-ra vagy `teljes` szintre; a 4 sor pontos kulcsú `kezi` sort talál | nincs teendő | nincs teendő |
| 6 | **CI E10** (`ellenorzes/szabalyok.py`) | szövegminta a `forditas_hu` tartalmán (kulcsfüggetlen) | nincs teendő | nincs teendő |
| 7 | `eszkozok/emeles.py` (`lista_epit`, `naplo_nezet`, `minta`, `rogzit`, `beir`) | a kész halmaz és a minta a `teljes` sorokból; a rögzítés `teljes`-t ír | átállítandó (M2 része) | átállítandó (M2 része) |
| 8 | `eszkozok/bdb_adatblokk.py` (`--karoli-epit`, a kész szócikkek halmaza) | a `teljes` / `forditas_hu` BDB-sorok | átállítandó: a kész halmazba az `sz<n>` sorok Strongjai is | nincs teendő |
| 9 | `eszkozok/bdb_jelolt/hu_illeszt.py` | Strongonként az utolsó nem üres BDB-sor | átállítandó (az utolsó szakaszt kapná) vagy a szakaszonként fordított Strongok kizárása (náluk az illesztés tárgytalan) | átállítandó: a token levétele, vagy a tokenes Strong illesztése közvetlenül |
| 10 | `eszkozok/forditas_kapuk.py` | nem olvassa a táblát; a fordítás szövegén fut | a kapu szakaszonként | a meglévő kapuk előtt a token levétele (M3 része) |
| 11 | `eszkozok/olvaso_pilot/adat.py` (a #60 pilot) | Strongonként az utolsó nem üres BDB-sor | átállítandó, ha a pilot újragenerálódik | átállítandó, ha a pilot újragenerálódik |
| 12 | eseti karbantartó eszközök: `bdb_atvezet_m5.py`, `bdb_konyv_javit.py`, `bdb_psi_javit.py`, `bdb_jelolt/nezet_hatas.py` | a `teljes` sorok | az `sz<n>` sorokat nem látják (a TSV-csere / pe-mem feladatánál számít, DT269 (1)) | látják; a token a token-cserét nem zavarja |

Tesztek, amelyek a táblát olvassák: 10 fájl (`teszt_bdb_adatblokk.py`, `teszt_bdb_zaras.py`, `teszt_ellenoriz_13.py`,
`teszt_forditas_kapuk.py`, `teszt_sqlite_epit.py`, `teszt_strong_util.py`, `olvaso_szerver/teszt_olvaso_szerver.py`,
`olvaso_szerver/teszt_szintek.py`, `olvaso_pilot/teszt_olvaso_pilot.py`, `ellenorzes/tesztek/test_szabalyok.py`); a `naplok/` alatt 14
eseti szkript (a #28/#38/#34 korábbi menetei, nem futnak újra).

Összesen: a 12 futó olvasóból (a) esetén 7-nél van teendő (2, 4, 7, 8, 9, 11, 12), (b) esetén 6-nál (2, 4, 7, 9, 10, 11; a 10 itt a
kapu előtti levétel; az új szakasz-kapu, M3, mindkét opcióban kell). Ebből CI-szabály: (a) és (b) esetén is egy, az E1 (13. szabály). A különbség a jellegben van: az (a) az **összefűzést** viszi minden szövegolvasóba (2, 9, 11), és új
forrás-ágat a 13. szabályba; a (b) a **token levételét** viszi minden szövegolvasóba (2, 9, 10, 11), és egy jelölést a hash-alap
megkülönböztetésére. A (b) minden olvasónál hibát okozhat, ha a levétel elmarad (a token a megjelenített szövegbe kerül), az (a) a régi
olvasót csendben az utolsó szakaszra szűkíti. A #132 (Thayer) a #128 láncára épül (`F132_THAYER_SZAKASZ_BRIEF.md` M0 4.), tehát a döntött
kulcs várhatóan a Thayerre is érvényes lesz.

`scope=eszkozok/, naplok/, .github/workflows/ (olvasók) | forras=grep forditasok / 'teljes' + kódolvasás @72eee13d | ts=2026-10-21`

### 2. A `forras_hash` alapja (DT-F128b)

| mérés | érték |
|---|---|
| a 674 kész `teljes` sor `forras_hash`-e = SHA-1(TSV `Teljes_szocikk`) | **674 / 674** |
| ugyanez a szakasztábla nézetével (`hivatkozas` javítással, pe/mem nélkül — a DT269 (1) bemenete) | **273 / 674** (401 sor hash-e változna) |
| összevetés: a DT231 (2) mérése a nyers táblanézettel (hivatkozás-javítás nélkül) | 446 sor változna (a különbség a 412 `hivatkozas` javítás) |
| nézet = TSV szöveg, minden Strong | 7 419 / 8 090 |
| nézet = TSV szöveg, a hátralék táblabeli Strongjai | 7 146 / 7 416 (270 Strongnál eltér: `_N`, szóköz, `forras_html`) |

A szakasztábla saját `forras_hash`-e a bekezdés **nyers HTML**-jének SHA-256-ja (16 jegy, SEMA 2.30): a `hivatkozas` javítást nem
tükrözi, tehát a fordítás bemenetének hash-eként önmagában nem elég. A javítótábla `hivatkozas` sorai a **Strong nézet-szövegében**
állnak (`elofordulas` = a token hányadik előfordulása a teljes nézetben), ezért a szakaszonkénti szöveg a javítással a Strong-szintű
nézetből vezethető le, nem soronként külön.

`scope=adat/forditasok.tsv BDB teljes sorai × konkordancia/BDB_teljes_unabridged.tsv × nezet_general.general(pe_mem=False) | forras=m0_meres.py @72eee13d | ts=2026-10-21`

### 3. A darabolás egysége (DT-F128c)

| mérés | érték |
|---|---|
| 20 000 karakter fölötti szócikk (nézet), mind | 11 (H9005 45 411, H1980 43 728, H5920 37 652, H4480 35 800, H1961 24 987, H3588 23 687, H5414 23 358, H0834 22 464, H7725 21 583, H6440 21 154, H3117 20 301) |
| ebből a hátralékban | **1** (H5920, 37 652; sorszám 3785, 11. adag) |
| ebből a 98 N-F107b Strong között | **6** (H1980, H4480, H3588, H0834, H7725, H3117) |
| a tokenes bemenet (a szakaszonként egy `⟦n⟧ ` tokennel) 20 000 fölött | ugyanez a 11 (a tokenek nem lépnek át határt) |
| a leghosszabb egyes szakasz | 6 969 karakter (H1980 `sorszam` 14); 10 000 fölötti szakasz **0**, 5 000 fölötti 1 |
| szakasz / Strong | átlag 4,53, max. 96 |

Következmény: a 10 000 karakteres vázlatrész (a #38 M0 4. pontjának gyakorlata) mindig kialakítható pusztán tokenhatáron, szakasz
kettévágása nélkül. A korábbi gyakorlat (F38 napló 4.): a 20 000 fölötti szócikk mohón, kb. 10 000 karakteres szegmensekben készült,
„strukturális helyzetű” jelölő előtt vágva, és egyben került a kapukra és a táblába.

`scope=adat/bdb_szakaszok.tsv + javítótábla nézete, 8 090 Strong | forras=m0_meres.py @72eee13d | ts=2026-10-21`

### 4. A nem `egyezik` illesztésű Strongok (DT-F128d)

| kategória | Strong | nézet = TSV | hossz (medián / max.) | szakasz/Strong (medián) | kész | hátralék | a 7. adagban |
|---|---|---|---|---|---|---|---|
| `reszleges` | 94 | 86 | 292 / 35 800 | 3 | 3 (H4480, H5542, H7381) | 91 | 5 (H0558, H2778, H5355, H5511, H7346) |
| `sikertelen` | 15 | 15 | 401 / 3 964 | 3 | 1 (H9008) | 14 | 0 |
| `csonk` | 35 | 35 | 22 / 40 | 2 | 2 (H1168, H3778) | 33 | 0 |
| táblán kívüli (F57/F72) | 9 | — (nincs szakaszsor) | 74–5 223 | — | 0 | 9 | 2 (H4725 5 223, H8065 884) |
| *`szocikk_resze` (a briefben nem szerepel; `bdb_id` kitöltve)* | 30 | 22 | 688 / 6 583 | 5 | 7 | 23 | 4 (H2549, H3119, H5838, H8040) |

A `reszleges` / `sikertelen` / `csonk` Strongok **mind** kapnak szakaszsort a táblában (a JSON szövegével és tagolásával; csak a `bdb_id`
üres, DT227 (a)); szakaszsor nélkül csak a 9 táblán kívüli áll. Egy szakaszos Strong nincs (minden Strong legalább a cím + egy bekezdés).
A `csonk` Strongok szövege csak a cím (pl. „H62. Abel Beth-maakah”, 22 karakter medián). A hátralékban a nem `egyezik` (a briefben
felsorolt három kategória + a táblán kívüliek) **147** Strong; a 7. adagban 7.

`scope=adat/bdb_szakaszok.tsv illesztes × forditasok.tsv × BDB_FORDITAS_sorrend.tsv | forras=m0_meres2.py @72eee13d | ts=2026-10-21`

### 5. A 98 elakadó Strong (N-F107b, DT-F128e)

A lista a `bdb_szakasz_hu.tsv` `elakad` soraiból újraszámolva **98 Strong, 606 sor** — halmazként azonos a
`naplok/F107_BDB_JELOLT_SZOVEG_naplo.md` 7.1 táblájával (`diff`: azonos).

| mérés | érték |
|---|---|
| illesztés | `egyezik` 92, `szocikk_resze` 4, `reszleges` 1 (H4480), `sikertelen` 1 (H9008) |
| a meglévő `teljes` sor állapota | `sonnet` 95, `opus` 2 (H2416, H5315), `kezi` 1 (H8415; DT25 (a)) |
| adag (a `sorrend` szerint) | 1: 3 · 2: 13 · 3: 16 · 4: 26 · 5: 19 · 6: 18 · nincs a sorrendben (a #28 kész szócikkei): 3 (H2416, H5315, H8415) |
| terjedelem | 672 522 karakter (nézet), 2 354 szakasz; 20 000 fölött 6 (l. 3.) |
| `forras_hash` = TSV | 98 / 98 |
| pe/mem `javitva` sort hordozó Strong | 62 / 98 (a 674 kész közül 332) |

Mind a 98 Strong sorszáma a 7. adag eleje (649) előtt van, vagy a #28 kész szócikke: a „gyakorisági hely” tehát mind a 98-nál a 7. adag
előtti tartomány. A 98 együtt kb. 1,35 adagnyi (500 000 karakteres adaggal számolva); a 7. adag maga 499 483 karakter.

`scope=adat/bdb_szakasz_hu.tsv elakad × forditasok.tsv × BDB_FORDITAS_sorrend.tsv × bdb_forras_javitas.tsv | forras=m0_meres.py @72eee13d | ts=2026-10-21`

### ⛔ M0 — döntésre vár

Az öt tétel a `DONTESEK.md`-ben: **DT-F128a** (tárolási kulcs), **DT-F128b** (`forras_hash`), **DT-F128c** (darabolás), **DT-F128d** (nem
`egyezik` Strongok), **DT-F128e** (N-F107b). A döntésig kódírás nincs (brief M0).
