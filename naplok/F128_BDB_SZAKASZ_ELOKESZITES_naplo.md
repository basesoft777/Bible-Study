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

**Döntés (F128.3, `74e23809`):** a felhasználó 2026-10-21-én (chat, az orkesztrátor-sessionben továbbítva) mind az öt javaslatot
elfogadta: DT-F128a (a), DT-F128b (1), DT-F128c (2), DT-F128d (2)+(i), DT-F128e sors (2), sorrend (i). A H8415 `kezi` soráról nem
döntött: DT-F128f (🟡).

## M1 — bemenet-előállító (F128.4, `73cf712b`)

`eszkozok/bdb_jelolt/szakasz_bemenet.py`: Strongonként a szakasztábla sorai (`jel` + `szoveg`), a `hivatkozas` / `javitva`
javításokkal (a Strong-nézeten, a `nezet_general.py` logikájával, a szakaszhatár mentén visszavágva), pe/mem csere nélkül;
határtoken `⟪<sorszam>⟫` (a `⟦n⟧` az `emeles.py` héber/görög helyőrzője, ezért más jel). Szakaszonkénti SHA-1 (DT-F128b (1)),
hívás-csoportok (DT-F128c (2)), a közös összefűző `strong_magyar()` (DT-F128a (a)); a 9 táblán kívüli Strong `None` (DT-F128d (2)).
Előmérés: üres szakaszsor 0; a 412 hivatkozás-javításból szakaszhatáron átnyúló 0; `⟪⟫⟦⟧` jel a forrásszövegben 0.

`--ellenoriz`: 8 090 Strong, 36 621 szakasz; a token nélküli szöveg mind a 8 090-en azonos a `nezet_general.py` (`--pe-mem` nélküli)
nézetével; pe/mem eltérés a nyers táblához képest 0; determinisztikus. Több csoportos Strong 11 (a 20 000 fölöttiek), minden csoport
≤ 10 000 karakter: H0834 3, H1961 3, H1980 6, H3117 3, H3588 3, H4480 5, H5414 3, H5920 5, H6440 3, H7725 4, H9005 6 csoport.

`scope=adat/bdb_szakaszok.tsv + adat/bdb_forras_javitas.tsv, 8 090 Strong | forras=python eszkozok/bdb_jelolt/szakasz_bemenet.py --ellenoriz @73cf712b | ts=2026-10-21`

## M3 — szakasz-kapu (F128.5, `22c23db5`; az M2 elé került, mert az `emeles.py` ága erre épül)

`eszkozok/forditas_kapuk.py`: `ellenoriz_szakasz` (14. kapu, gátló: a tokenek száma és sorrendje a forrásé; nincs új, hiányzó,
duplázott token, üres szakasz, szöveg az első token előtt), `ellenoriz_tagolas_szakaszonkent` (a 9. kapu szakaszpáronként; a
szakasz elé mindkét oldalon `. ` kerül, hogy a szakasz eleji jelölő a folyó szövegbeli helyzetével azonosan ismerődjön fel),
`kapuk_futtat_szakaszos` (a többi kapu a token nélküli szövegen). A régi `kapuk_futtat` változatlan.

Tesztek (`eszkozok/teszt_forditas_kapuk.py`, 81, OK): 11 szintetikus eset (hiányzó, duplázott, felcserélt, új token, üres szakasz,
token előtti szöveg; a szomszéd szakaszba vándorolt jelentésszám: egészben átmegy, szakaszonként nem), és a 674 kész Strong:
a `bdb_szakasz_hu.tsv` `illeszkedik` sorainál kezdődő szakaszokból összerakott tokenes párokon **0 szakasz-kapu hiba (674/674)**.

## M2 — prompt v5 és `emeles.py` (F128.6, `7426d6a8`)

`forditas/prompt_v5.md`: a v4.2 szó szerinti másolata (a v4 mind a 193 sora sorrendben megvan, gépi ellenőrzéssel) + „Kiegészítő
szabály (v5) — szakaszhatár-tokenek” (hat szabály, példával). `eszkozok/emeles.py` új ága: `szakasz_elokeszit`, `szakasz_ellenoriz`,
`szakasz_rogzit` (`jelentes_szam = sz<sorszam>`, `forras_hash` a szakaszé), `szakasz_beir` (a régi `teljes` sor `--regi-elavult`-tal
`elavult`, a `megjegyzes` jelöli; enélkül megáll; `kezi` régi sor csak `--kezi-felulir`-ral). A régi út (prompt v4, `rogzit` / `beir`)
változatlan. Tesztek: `teszt_szakasz_bemenet.py` 23 (a rögzítés és a beírás ideiglenes táblákon; a repó `forditasok.tsv`-je nem
íródik), `teszt_emeles.py` 10, `teszt_bdb_zaras.py` 21 — OK. (Az `olvaso_pilot/teszt_olvaso_pilot.py` hibái — Macula-görög, TSK —
nem érintik a módosított kódot; a fájl nem importálja ezeket.)

## M4 — száraz próba (modellhívás nincs; a `forditasok.tsv` nem íródik)

Eseti szkript a repón kívül (`m4_szaraz.py`); a promptok a menet scratchpadjába íródtak, a repóba nem. A három Strong gépi választás:
a legrövidebb kész, `egyezik`, 3 szakaszos, 300 karakter fölötti; a legtöbb törzsű kész `egyezik`; a legrövidebb (3 000 fölötti),
legalább 3 törzsű `egyezik` N-F107b Strong.

| Strong | szakasz | karakter | törzs | csoport | prompt (karakter) | token a promptban | kitöltetlen `{{…}}` | a kész magyar csoportjai (összeolvasztott sor) | 14. kapu | a többi kapu a kész magyaron |
|---|---|---|---|---|---|---|---|---|---|---|
| H0609 (rövid) | 3 | 307 | 0 | 1 | 26 362 | 3 | 0 | 1 (2) | RENDBEN | mind RENDBEN |
| H1540 (több törzs) | 32 | 5 223 | 10 | 1 | 31 663 | 32 | 0 | 29 (3) | RENDBEN | 4_formazas, 5_terminologia SERTES |
| H8130 (N-F107b) | 14 | 3 140 | 3 | 1 | 29 507 | 14 | 0 | 9 (5) | RENDBEN | 1, 2, 4, 9, 11 SERTES |

A 674 kész Strongon (a kész magyar az `illeszkedik` soroknál kezdődő csoportokban): **14. szakasz-kapu 674/674 RENDBEN**; a 9.
tagolás szakaszonként 578, egészben 657 RENDBEN; a teljes szakaszos kapusor 235-ön megy át (SERTES: 4_formazas 401, 9_tagolas 96,
2_versszam 24, 11_konyvek 24, 1_gorog_heber 19, 5_terminologia 16, 10_torzs 1, 8_idezojel 1). Összevetésül a régi kapusor a TSV
forrásán: 658/674 (csak 5_terminologia 16).

A különbség oka nem a kapu, hanem a próba két mérhető tulajdonsága, ezért a kész magyaron a teljes kapusor nem mérce, csak a 14.:
- a régi fordítás a TSV-ből készült: 346 Strongban `_<szám>` maradványt hordoz (a TSV `_N` gyakoriságszáma, DT181), a nézetből a
  `<sub>` kimarad — ez a 4. kapu `_`-jelzése; a nézet és a TSV szövege a kész Strongok közül 401-nél eltér (M0 2.);
- a `bdb_szakasz_hu.tsv`-ben 22 Strong magyar szakaszai átfednek (H0068, H0259, H0410, H0637, H0995, H1004, H1870, H1980, H1984,
  H2388, H2416, H3384, H3644, H3772, H3947, H4264, H4672, H5127, H5674, H6242, H7725, H8130) — az összerakás itt duplikál (1., 2., 11.
  kapu „többlet”). **Mind a 22 a 98 N-F107b Strong között van**, tehát újrafordul; új tétel nem kell.
- a szakaszonkénti 9. kapu 96 hibájából 77 az összeolvasztott (elakad / horgony / átfedő) Strongoké; 19 más (pl. H0001 1. szakasz:
  a „37 1. 2” „1.”-je; H0559 „I”): a szakaszonkénti illesztés szigorúbb, mint az egészben futó (ott a jelölő a következő szakaszban is
  „megtalálható”). Új fordításon ez a cél (brief M3), a kész szövegen nem javítunk.

`scope=F128 M4, H0609 / H1540 / H8130 + 674 kész Strong | forras=m4_szaraz.py, m4_atfedes.py, m4_tagolas.py (eseti, a repón kívül) @7426d6a8 | ts=2026-10-21`

## M4.2 — SEMA és a #38 briefje

`adat/SEMA.md` 2.14: a `jelentes_szam` (`sz<sorszam>`), a `forras_hash` (az `sz<n>` sor alapja) és az `allapot` (`elavult` a
felváltott `teljes` sorra) sora, és egy bekezdés a szakaszonkénti sorokról (összefűző, olvasók, a 9 táblán kívüli, csoportok, kapuk).
`F38_BDB_FORDITAS_BRIEF.md` „Lépések”: rövid hivatkozás a szakaszonkénti útra (a fejléchez nem nyúl).

## Nyitott (F128.8 állapota; azóta eldöntve, l. lent)

- **DT-F128f** (🟡): a H8415 `kezi` sora — újrafordul-e (a `szakasz_beir` ma megáll rajta, `--kezi-felulir` nélkül).
- **DT-F128g** (🟡, ⛔): az olvasók átállítása az első `sz<n>` sor beírása előtt. Az `ir` mezőn kívül: `eszkozok/ellenoriz.py`
  13. szabály (CI E1: az `sz<n>` sorhoz ma „nincs hozzá forrásszöveg” = SÉRTÉS), `olvaso_szerver/lekerdezesek.py` `bdb_magyar` /
  `bdb_magyar_meta` (az utolsó nem üres sort veszi: az utolsó szakaszt mutatná), `bdb_adatblokk.py --karoli-epit` (a kész halmaz
  csak `teljes`), `bdb_jelolt/hu_illeszt.py` (az utolsó nem üres sor). A #38 első szakaszos beírása nélküle a CI-t megbuktatja.

## Az olvasók átállítása (DT-F128g (a), DT-F128f (3); F128.9–.14)

**Döntés (F128.9, `b34f835b`):** a felhasználó 2026-10-21-én (chat, az orkesztrátor-sessionben továbbítva): DT-F128g (a) — a brief
`ir` mezője bővül a négy olvasóval és tesztjeikkel, az átállítás ebben a menetben, a közös `strong_magyar` összefűzővel; DT-F128f (3) —
a H8415 szakaszonként újrafordul, de az új szakaszsorok csak a felhasználó jóváhagyása után kapnak `kezi`-t; addig a régi,
jóváhagyott `kezi` sor az érvényes.

| tétel | mi változott | teszt |
|---|---|---|
| F128.10 `6b8bbf78` | `szakasz_bemenet.py`: `strong_magyar_sorok` (a felhasznált sorokkal); a nem `elavult` `kezi` `teljes` sor elsőbbsége, amíg a szakaszsorok nem mind `kezi`-k (DT-F128f (3)); paraméterezhető táblaútvonal; a `forras_javit` / `nezet_general` importja lusta. `emeles.py szakasz_beir --kezi-marad` (a régi `kezi` sor bájtra érintetlen), a jóváhagyás `--allapot kezi --regi-elavult --kezi-felulir` | `teszt_szakasz_bemenet.py` 25, OK |
| F128.11 `5aba229c` | `ellenoriz.py` 13. szabály (CI E1): az `sz<n>` sor forrásszövege az `adat_dir` szakasztáblájából (hivatkozás-javítással, pe/mem nélkül); új: a nem `elavult` szakaszsorok együtt a Strong összes szakaszát fedik | `teszt_ellenoriz_13.py` 25 (7 új), OK; `ellenoriz.py` a repón: SÉRTÉS 0 |
| F128.12 `8a78bfea` | `olvaso_szerver/lekerdezesek.py` `bdb_magyar`, `bdb_magyar_meta`: a közös összefűzőn át (fájlútvonalról, `sys.path` nélkül); a meta a felhasznált sorok modelljei („ / ”) és legkésőbbi dátuma | `teszt_futtat.py --gyors` (WSL-natív `~/pardes/pardes.db`, épült 2026-10-14): a 3 új teszt zöld; l. lent |
| F128.13 `1720b1d6` | `bdb_adatblokk.py` `kesz_bdb_strongok`: `teljes` vagy `sz<n>` sor | `teszt_bdb_adatblokk.py` 46 (1 új), OK |
| F128.14 `61517df7` | `hu_illeszt.py` `forditasok()`: a közös összefűzőn át; szakaszonként fordított Strongnál a `forditas_forras_hash` a token nélküli forrásnézet SHA-1-e | `teszt_bont.py` 47 (2 új, zöld) |

**Változatlanság a mai adaton:** a valós adatbázison (`~/pardes/pardes.db`) a régi (utolsó nem üres sor) és az új `bdb_magyar` /
`bdb_magyar_meta` mind a 674 BDB-Strongon azonos (eltérés 0); a `hu_illeszt.py` által generált `bdb_szakasz_hu.tsv`-törzs bájtra
azonos a táblával (új teszt); a `kesz_bdb_strongok` halmaza változatlan (nincs `sz` sor).

`scope=olvaso_szerver bdb_magyar(_meta), 674 BDB-Strong | forras=bdb_magyar_regi_uj.py (eseti, a repón kívül; WSL venv, ~/pardes/pardes.db) @8a78bfea | ts=2026-10-21`

**A tesztfuttatás mellékleletei (nem e menet okozta):**
- `teszt_futtat.py --gyors`: zöld `teszt_arculat`, `teszt_bdb_vers_jelentes`, `teszt_indito`, `teszt_kereses`, `teszt_tervezo`;
  HIBA `teszt_olvaso_szerver` (2: `TestD2PilotEgyezes` 1Móz 1:25 és Zsolt 22 — első eltérő kulcs `vers:macula`, `vers:tsk_darab`,
  `gorog_szo:usz_elofordulas`; a BDB-magyar nem érintett, l. a fenti 674/674-et) és `teszt_pilot_aranymintaval` (Károli-könyvek
  57 ≠ 61): az adatbázis (2026-10-14) és a pilot-aranyminta eltérése.
- `teszt_bont.py`: a 3 `--ellenoriz`-teszt (bont, forras_javit, hu_illeszt) Windowson a CRLF-checkout miatt bukik (a generátorok
  `\n`-nel írnak, a munkapéldány CRLF; a `bont.py` / `forras_javit.py` kódja és bemenete változatlan); a `bdb_szakasz_hu.tsv`
  fejlécében rögzített `forditas_kapuk.py@91730dafdb40` és `bdb_szakaszok.tsv@495d1c81cfc0` már a 72eee13d-n sem egyezett a fájlok
  LF-hash-ével (`bcb8369a851f`, `66bd24b9abb6`). A tábla nem regenerálódott (nincs az `ir`-ben, a törzse változatlan).
