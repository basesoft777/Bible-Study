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

## 2. ⛔ 0.3 — megállás és döntés

A DT-F131a–e (a brief 5. szakasza, az M0 szerint pontosítva) és az M0-ból adódó DT-F131h a `DONTESEK.md`-ben, 🟡 állapotban (F131.0.3); a végrehajtás a döntésig állt.

**Döntés (2026-10-26, a felhasználó, az orkesztrátoron át):** minden javaslat elfogadva — DT-F131a 1. ((i) marad, (ii) a gerincben, (iii) marad, (iv) a TBESH helyén mutató + egysoros magyar jelentés az `adat/glosszak_heber_hu.tsv` `fo=igen` soraiból); DT-F131b 2.; DT-F131c 1. + (a), a 7 Thayer-példahely felirat nélküli kiemelésével, a görög magyar szöveg a #142-re vár, addig átmenetként a 2.; DT-F131d 1. + (a); DT-F131e 1. + (c); DT-F131h (a). Rögzítve: `DONTESEK.md` (🟢), a brief fejléce és 8. szakasza (F131.0.6).

**A (iv) következménye:** az `olvas` az `adat/glosszak_heber_hu.tsv`-vel bővült, amelyet a #140 (`megallt`) ír; a `fuggesek` ezért a #140-re is várónak mutatta. A `nem_fugg` megkapta a 140-et (egyeztetett eltérés, brief 8.); a két sor hash-ét a 4.5 rögzíti.

## 3. Végrehajtás (F131.1–F131.2)

### 3.1 Adat (F131.1)

- `adat/szotar_szakasz_cimke.tsv` (SEMA 2.40), 13 sor, író: `naplok/F131_cimke_ir.py` (eltérésnél megáll; `split('\t')` / `'\t'.join()`):
  - BDB H7121 `Qal/2/c` ← `2.c` „segítségül hívni”; `Qal/3/-` ← `3` „kihirdetni”; `Qal/3/b` „a nevet kihirdetni”;
  - BDB H8034 `-/3/-` „név: Isten megjelölése”; `-/4/-` „név: hamis istenekről”;
  - TBESG G1941 `2` ← `2` „segítségül hívni, folyamodni valakihez”;
  - Thayer G1941 `cim`, `fej`, `-/1/-` … `-/5/-`: kézi határ a `forditasok.tsv` `Thayer G1941 teljes` magyar sorában (`forditas_hash` = `feeb2ad0…`), címke: `-/1/-` „melléknéven nevezni”, `-/5/-` „segítségül hívni a név kimondásával”. A határok a magyar sor „1. nevet tenni valakire”, „2. ἐπικαλεῖται τό ὄνομα”, „3. τίνι (tini), a tárgy”, „4. segítségül hívni (mint a német anrufen)”, „5. héber mintára” kezdeteinél; a fej az „ἐπικαλῶ (epikaló):” előtt.
  - A címkék a végrehajtó javaslatai a magyar szakaszok vezérszavaiból (`manual`); jóváhagyásuk a DT-F131f-nél.
- `ellenoriz.py` 17. szabály (SEMA 2.40): RENDBEN. A teljes `ellenoriz.py`: SÉRTÉS 0.

### 3.2 Generátor (F131.2)

- `eszkozok/lexikon_general.py`, kapcsoló: `SZOTARI_GERINC_MOTIVUMOK = {ISTENTISZT-001}`. A változás leírása: a commit üzenete és a SEMA 2.40.
- Teszt: `eszkozok/teszt_szotari_gerinc.py`, 22 eset, OK (a brief 2. lépésének minden pontja: BDB-példa / kutatói ⓘ, a 2Móz 33:19 → `Qal 3.b` elsőbbség, az ellentmondó eset GerincHiba-val, a minősítő, a `horgonnyal`, az `elakad`, a meg nem talált példahely; továbbá a kapcsoló, a 17. szabály, és a valódi adaton a 32 sor).
- `eszkozok/teszt_szerepmatrix.py`: a kapcsoló a tesztben kikapcsolva (az általános rendert vizsgálja; egyeztetett eltérés, brief 8.), OK. `teszt_lexikon_adatres`, `teszt_torzscikk_migralt`, `teszt_ellenoriz_11`, `teszt_ellenoriz_13`, `teszt_general_forras`, `teszt_render_diff_osztalyoz`: OK.
- **Előzetes hiba, nem e feladaté:** `teszt_general_ellenorzo.py` `SemaKulcsok.test_eles_sema` a main-en is bukik (a SEMA kulcsos tábláinak száma 29, a teszt 23-at vár); a SEMA 2.40 eggyel növeli (30).
- **Nulla-diff:** `eszkozok/nulladiff.sh 77bad810 2026-10-26` (a F131.1 előtti állapot ↔ a munkafa): egyetlen eltérő fájl az `ISTENTISZT-001_TUDOMANYOS.md`; a 7 másik lap és a törzscikkek bájtra azonosak.
- **CI a próba idején (várt):** E28 piros (az éles `lexikon/ISTENTISZT-001_TUDOMANYOS.md` a generátorhoz képest elavult) — az éles felülírás a ⛔ DT-F131g-hez kötött, addig várt állapot. E16: a PR címe „[ELLENŐRZŐ]” előtagot kíván, mert az `ellenoriz.py` változott (a PR-t nyitó dolga).

## 4. Próbarender a repón kívül (F131.3)

`PARDES_DATUM=2026-10-26 python eszkozok/general.py --cel lexikon --id ISTENTISZT-001 --kimenet <a session scratchpadjának proba2/ könyvtára>` (a repón kívül; nem a `generalt_proba/`, nem a `lexikon/`). Mérés: `python naplok/F131_proba_meres.py <könyvtár>`.

`scope=ISTENTISZT-001 próbarender | forras=naplok/F131_proba_meres.py; general.py --kimenet (PARDES_DATUM=2026-10-26) | ts=2026-10-26 12:59`

### 4.1 Tiltott keretezés

A szótári gerinc két blokkjában és a „Jelentés (a szó)” oszlopban (`eltér`, `máshová sorol`, `NEM invokáció`, `szemben a BDB`, `a BDB szerint nem`, kis- és nagybetű nélkül): **0**.

### 4.2 `(fordításra vár)` előtte / utána: 65 → 1

| Kulcs | Előtte | Utána |
|---|---|---|
| G1941, 3. Teológiai szócikk (tW) | 1 | 0 |
| G1941, 5. Tömör jelentés (UBS DNTG 56.15 + Mounce) | 3 | 0 |
| G1941, Jelentéstartomány (UBS-doménsor: 56.15 glosszája) | 0 | 1 |
| H8034, 1. Alapjelentés (TBESH) | 1 | 0 |
| H7121, H8034, 3. Teológiai szócikk (tW) | 10 | 0 |
| H7121, H8034, 5. Tömör jelentés (UBS DBH) | 48 | 0 |
| H7121, 8. Nyelvi háttér (BDB-fej) | 1 | 0 |
| H8034, 8. Nyelvi háttér (BDB-fej) | 1 | 0 |

A maradék 1: a G1941 UBS-doménsorának 56.15-ös kódja („to appeal one’s case …”), amelynek nincs magyar glosszája. A brief a doménsort „a három Louw–Nida-kóddal” írta (33.176, 11.28, 33.131); az adat negyedik kódot is ad. A sor az adat minden kódját mutatja, a hiányt jelölve — **kérdés a DT-F131f-hez:** maradjon-e a 4. kód (jelölt hiánnyal), vagy csak a magyarul meglévő hármat mutassa a sor.

### 4.3 A 32 sor

Mind a 32 soron áll címke az elsődleges (kutatói) tokenen: 22 ÓSZ-sor H7121-címkével (`Qal 2.c` 20, `Qal 3.b` 2: 2Móz 33:19, 34:5), 10 ÚSZ-sor `TBESG 2` címkével. A H8034 mint második token 5 soron kap BDB-példa-címkét (`3`: 1Móz 4:26, 12:8, 13:4, 21:33; `4`: 1Kir 18:24), 17 soron kimondott hiányt (`*(nincs hozzárendelés)*`). A minősítő (`tagadva`, `rokon`) a cellában nem áll; az ⓘ-ben igen (N-F131b). Ellentmondás (GerincHiba): 0.

### 4.4 Kiemelt szótári példahelyek

| Szótár, Strong | Hivatkozás a motívumhelyeken | Kiemelve | A magyarban nem található |
|---|---|---|---|
| BDB H7121 | 9 (8 vers) | 9 | 0 |
| BDB H8034 | 6 (5 vers) | 5 | 1: `bdb_vers_jelentes.tsv` sorszam 3 (1Móz 12:8, `fej`) — a magyar fej-szakaszban nincs ilyen hivatkozás; kiemelés nincs, a lap kutatói megjegyzése és ez a napló rögzíti |
| Thayer G1941 | 7 | 7 | 0 |

A szótár nem idézi (nincs `bdb_vers_jelentes` / `thayer_vers_jelentes` sor): H7121-nél 14, H8034-nél 17, G1941-nél 3 motívumhely (ApCsel 9:21, ApCsel 22:16, Róm 10:14); a lapon a kutatói megjegyzésben.

### 4.5 Hash-rögzítés (DT-F131h, DT-F131a (iv))

| Tábla | H7121 + H8034 sorai | SHA-1 (a sorok `\n`-nel fűzve) |
|---|---|---|
| `adat/bdb_szakaszok.tsv` | 55 | `c8cc6851ccbbe79450b868ed754cef46ee9334d1` |
| `adat/bdb_szakasz_hu.tsv` | 55 | `661bd57569e01c669c8f12c051919aa289face65` |
| `adat/glosszak_heber_hu.tsv` | 5 | `8c18619040e42c9e3ab3f386020766a141f31e22` |

Egy későbbi #133 / #144 / #140 futás után ugyanez a mérés megmutatja, változott-e az arany Strongok sora.

### 4.6 Egyéb

- `ellenoriz.py` 13. és 17. szabály: RENDBEN; `python eszkozok/feladatok.py ellenoriz`: 164 brief, 0 hiba.
- A Thayer magyar szövege a kézi határokból jön (a #142 nem futott); a lap ezt kimondja. *(Az F131.3.6 óta tárgytalan: l. 5.)*

## 5. Javítás a ⛔ 3.1 előtt (F131.3.1–F131.3.7)

**F131.3.1–3.5 (az orkesztrátor menete):** a Thayer 1. rész címkéje „elnevezni” (a „melléknéven nevezni” és a „más néven nevezni” sem természetes magyar); DT-F131i eldöntve (a): a `tiltott_fordulatok.tsv` `helyette` oszlopa javítva, új tétel „nevet tenni valakire”. A main beolvasztva; benne a #142 (PR #485): a G1941 szakaszonkénti magyar Thayer-szövege (`forditasok.tsv` `Thayer G1941 sz1…sz7`, `sonnet`).

**F131.3.6 (a felhasználó jóváhagyásával, az orkesztrátoron át):** a Thayer-gerinc a DT-F131c 1. opciójára áll át.
- A magyar Thayer-szöveg a #142 `sz<n>` soraiból jön (nem `elavult`); ahol nincs sor, ott angol szöveg és `(fordításra vár)` áll. A `teljes` sor kézi szeletelése megszűnt.
- `adat/szotar_szakasz_cimke.tsv`: 13 → 8 sor. A `hu_kezdet`, `hu_hossz`, `forditas_hash` oszlop és az 5 címke nélküli Thayer-sor kivezetve; a Thayer 1. „elnevezni” (DT-F131i) és 5. címkéje marad. Az író (`naplok/F131_cimke_ir.py`) határszámítása kivezetve. SEMA 2.40 igazítva.
- `ellenoriz.py` 17. szabály: a határ-ellenőrzés kivezetve; új: a címke a `tiltott_fordulatok.tsv` mintáit sem tartalmazhatja. Futás: RENDBEN, SÉRTÉS 0.
- Új a generátorban: a gerinc magyar szövegében a `tiltott_fordulatok.tsv` mintáinak találata „ismert hiány”-ként a kutatói megjegyzésbe kerül; a szöveget a lap nem írja át.
- Tesztek: `teszt_szotari_gerinc.py` 23 eset OK (új: a Thayer `sz` forrása, a hiányzó `sz` sor, a tiltott fordulat jelölése, a 17. szabály tiltott-fordulat ága); `teszt_forditas_kapuk`, `teszt_szerepmatrix`, `teszt_ellenoriz_13`, `teszt_lexikon_adatres` OK. Nulla-diff (`nulladiff.sh 77bad810 2026-10-27`): csak az ISTENTISZT-001 lap tér el.

**Ismert hiány (nem e feladat javítja):** a G1941 `sz3` (Thayer 1. rész) magyar szövege a tiltott „nevet tenni valakire, más néven is nevezni” alakot tartalmazza (a #142 a korábbi `helyette`-javaslatot vette át, DT-F131i). A javítás a #142 újrafuttatása, külön menetben; a #131 a `forditasok.tsv`-hez nem nyúl. A próbalap a Thayer-gerinc kutatói megjegyzésében jelöli.

### 5.1 Az új próba mérése (F131.3.7)

`PARDES_DATUM=2026-10-27 python eszkozok/general.py --cel lexikon --id ISTENTISZT-001 --kimenet <scratchpad/proba3>` (a repón kívül); `python naplok/F131_proba_meres.py <könyvtár>`.

`scope=ISTENTISZT-001 próbarender | forras=naplok/F131_proba_meres.py; general.py --kimenet (PARDES_DATUM=2026-10-27) | ts=2026-10-27 18:11`

- Tiltott keretezés: 0.
- `(fordításra vár)`: 65 → 1 (a G1941 UBS-doménsorának 56.15-ös kódja; változatlan, l. 4.2).
- A 32 sor: mind címkés az elsődleges tokenen; a cellák változatlanok a 4.3-hoz képest.
- Kiemelés: BDB H7121 9/9, H8034 5/6 (a meg nem talált: sorszam 3, 1Móz 12:8, `fej`), Thayer G1941 7/7 (most a #142 magyar szövegében: 1Pét 1:17 az 1. részben, a többi 6 az 5.-ben).
- Tiltott fordulat a gerinc magyar szövegében: 1 — Thayer 1 (`sz3`): „nevet tenni valakire” (ismert hiány, a lapon jelölve).
- Hash-rögzítés: változatlan (4.5).
- HTML-nézet (privát Artifact, ugyanaz az URL): https://claude.ai/artifact/QVHPBrCJWkSP7pT8z363vy

### 5.2 DT-F131j: az ÓSZ-sorok „UBS-jelentés” cellája a DBH-ból (F131.3.8–F131.3.11)

**Döntés:** DT-F131j (a), a felhasználó (F131.3.8). **Végrehajtás (F131.3.9):** az arany lapon (kapcsoló) az ÓSZ-sorok cellája tokenenként a `konkordancia/UBS_DBH_referenciak.tsv` hivatkozásait adja (`lexid` — rövid definíció a `UBS_DBH_jelentesek.tsv`-ből, a DNTG-cella mintájára; a Károli-vers a render meglévő `karoli_mt_vers` képzésével MT-re). Magyarul a `forditasok.tsv`-ből (`UBS_DBH`, entry_id = lexid, jelentes_szam = `—`, `definicio_hu`), ahol van — ma sehol —, különben az angol eredeti `(fordításra vár)` jelöléssel. Hivatkozás híján: `— (ÓSZ; nincs DBH-hivatkozás: <ok vagy keresett MT-vers>)`. A lap alji mondat és a blokk forráslistája (UBS_DBH, Karoli_versmegfeleltetes) igazítva; RENDER_BRIEF (a G6 után) és a lexikonsablon (1. Előfordulások) egy-egy bekezdéssel. Tesztek: `teszt_szotari_gerinc.py` 26 eset OK; `teszt_szerepmatrix` OK; `ellenoriz.py` SÉRTÉS 0; nulladiff (`da4323e4`): csak az ISTENTISZT-001 lap tér el.

**A próba (F131.3.11, `PARDES_DATUM=2026-10-28`, a repón kívül, `naplok/F131_proba_meres.py`):**

`scope=ISTENTISZT-001 próbarender | forras=naplok/F131_proba_meres.py; general.py --kimenet (PARDES_DATUM=2026-10-28) | ts=2026-10-28 13:44`

- ÓSZ-sor 22: DBH-jelentéssel 21, kimondott hiánnyal 1 (Jóel 2:32).
- A cellákban 44 DBH-hivatkozás (lexid), mind angolul, `(fordításra vár)` jelöléssel.
- `(fordításra vár)` a lapon: 1 → 46 (44 a DBH-cellákban, 1 a lap alji magyarázó mondatban, 1 a G1941 56.15-ös UBS-kódja). A szótári gerinc és a többi mérés (4., 5.1) változatlan.
- **Adathiba-gyanú (nem e feladaté):** a Jóel 2:32-t a `konkordancia/Karoli_versmegfeleltetes.tsv` `KJV` osztályúnak, MT-vers nélkül írja (a tábla a Jóel 2:28–32-t és a 3. fejezetet a KJV-vel azonosnak veszi); az MT-ben ez a Jóel 3:5, és a DBH ott hivatkozik a H7121-re (2 lexid) és a H8034-re. A render és a cella a táblát követi, ezért a cella hiányt mond, a keresett MT-verssel.

**A #121-nek (F131.3.10, csak olvasó mérés):** `naplok/F131_DBH_egysegek.tsv` (lexikon, strong, lexid, mezo, van_hu; proveniencia-sorral), író: `naplok/F131_dbh_meres.py --renderek <a 8 lap mai renderének könyvtára, a repón kívül>`.

`scope=8 lexikonoldal ÓSZ-sorainak H-tokenjei | forras=naplok/F131_dbh_meres.py; adat/elofordulasok.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/UBS_DBH_referenciak.tsv, adat/forditasok.tsv | ts=2026-10-28`

| | Érték |
|---|---|
| egyedi (strong, lexid) a 8 lap ÓSZ-sorain | 36 (ALVIL 1, ANTROP 3, HAMART 15, HODIT 3, ISTENTISZT 5, KIRALY 4, MENNY 3, TEREMT 2) |
| egység (× `definicio_hu`, `glosszak_hu`) | 72; lefordítva 0 |
| a #121 mai DBH-egységei (a 8 lap héber 5. szerepének `(fordításra vár)` sorai, mai render; ISTENTISZT-001: az éles lap) | 268 (134 lexid) |
| átfedés | 72 — a cellához szükséges minden egység már a #121 hatókörében van; új egység 0 |
| hivatkozás nélküli ÓSZ-vers × token | 16: KEZI osztály, MT-vers nélkül 8 (Préd 9:12, 4Móz 13:34 ×2, Jób 38:7 ×2, Jób 38:16, 38:30); a tábla szerinti MT-versen nincs hivatkozás 8 (Ézs 7:11, 1Móz 4:10, 1Krón 20:6, 20:8, Jóel 2:32 ×2, 1Móz 14:19, 14:20, Jób 41:32) |

Megjegyzés: az éles `lexikon/` 7 lapja a generátorhoz képest elavult (DT344), ezért a #121-egységeket a mai generátor repón kívüli renderéből számoltam; a 454-es #121-szám ennek megfelelő (a DBH része 268).

### 5.3 A DT-F131f 1. javítóköre (F131.3.13–F131.3.14): a H8034 két BDB-példa-hiánya

**Döntés (F131.3.13, a felhasználó):** DT-F131f (1) javítással újra, 1. kör a kettőből; (2) a címkék változatlanok; (3) az 56.15 (a). A kör tárgya a `adat/bdb_vers_jelentes.tsv` H8034-példáinak két hiánya.

**(a) 1Móz 26:25.** A BDB H8034 3. szakasza „so 12:8; 13:4; 21:33; 26:35” — a 26:35 a forrásban áll (a magyar 2.32 is „26:35”); a TAHOT szerint a H8034 az 1Móz 26:25-ben áll (a H7121-gyel), a 26:35-ben nem. Sajtóhiba-gyanú; a javítás módját a brief nem rögzíti, és a meglévő javítótáblák (2.23, 2.31) egyike sem fedi → **DT-F131k** (🟡, `DONTESEK.md`). Korrekció nem készült.

`scope=H8034, 1Móz 26:25/26:35 | forras=konkordancia/BDB_teljes_unabridged.tsv, konkordancia/TAHOT_kivonat.tsv | ts=2026-10-28`

**(b) 1Kir 18:25, 18:26.** A kinyerő (`eszkozok/olvaso_szerver/bdb_szelet.py` `hivatkozasok()`) a „1Kin 18:24-25, 26” alakban csak a 18:24-et ismeri fel: a folytatás-minta (`_FOLYTATAS`) a token végén keres, a „-25” tartomány után nem. A kinyerő és a 2.29 tábla a #102 (`nem_indult`) `ir`-ében áll; a #131 nem írta át, hanem a javítás két változatát a memóriában mérte a teljes táblán (`naplok/F131_bdb_tartomany_meres.py`, a `B.hivatkozasok` futásidejű cseréjével; a repó fájljai változatlanok):

`scope=adat/bdb_vers_jelentes.tsv, teljes | forras=naplok/F131_bdb_tartomany_meres.py; bdb_vers_jelentes.py general() --ts 2026-10-16 | ts=2026-10-28 13:59`

| | A: folytatás a tartomány után | B: A + a tartományok kibontása |
|---|---|---|
| a mai kód kimenete ↔ a commitolt tábla | azonos (160 616 sor) | azonos |
| hozzáadott sor / elveszett | 1 438 / 0 | 5 880 / 0 |
| érintett szócikk | 603 | 1 521 |
| új Károli-igehely | 1 429 | 5 715 |
| régi sor más `sorszam`-mal | 35 012 | 77 280 |
| arany (H7121, H8034) | + 1Kir 18:26 mindkettőnél; H7121 + 1Sám 3:8, 1Móz 5:29, Jer 7:14, 7:30 | + 1Kir 18:25 és 18:26 mindkettőnél; **de** a H7121 „4:25-26” (Qal 6.a) az 1Móz 4:26-ot második útvonalon is BDB-példává teszi → a gerinc GerincHibát ad (kézi kérdés) |

→ **DT-F131l** (🟡, `DONTESEK.md`). A javítás a #102-é; a #131 a tervet és a mérést adja át.

**Ezért ebben a körben a generátor, a tábla és a próbalap nem változott** (a két hiány javítása a DT-F131k/l döntésétől és a #102-től függ); új próbarender és Artifact-frissítés nem készült, a próbalap a 3. verzió (5.2).

### 5.4 A javítókör folytatása (F131.3.15–F131.3.19): DT-F131k/l döntés, main-beolvasztás, A–C

**Döntés (F131.3.15, a felhasználó):** DT-F131k és DT-F131l a javaslat szerint (a javítás a #102-ben, addig a lap jelöli a hiányt); a kör hatóköre a C) ponttal bővült.

- **Main-beolvasztás (F131.3.16):** a `DONTESEK.md` ütközésében mindkét oldal sorai maradtak; a SEMA 2.40-ben a main az F131.1-es, az ág az F131.3.6 utáni szöveget hordozta: az ág szövege maradt. A main-ben a javított Thayer G1941 `sz3` („1. nevet adni valakinek, elnevezni …”).
- **A) 1Móz 26:25 (F131.3.17):** a H8034 cellája „*(nincs hozzárendelés; BDB-sajtóhiba gyanúja, l. ⓘ)*”; az ⓘ: a BDB „26:35”-öt idéz, a TAHOT szerint a H8034 a 26:25-ben áll, a javítás a #102-ben (DT-F131k). Generátor: `BDB_HIVATKOZAS_GYANU` (a gerinc-ágon); teszt +1.
- **B) 1Kir 18:25–26:** nem változott (DT-F131l (C)); a cellák „nincs hozzárendelés”-t mondanak, a #102-re vár.
- **C) `motivumok/ISTENTISZT-001.md` (F131.3.18):** a 3. szakasz (az `ertelmezes` rés) „2. A Thayer jelentés-tagolása” pontja: az 1. ág „elnevezni” (DT-F131i); a 4. ág „segítségül hívni — segítőként, tanúként, illetve bíróként, azaz valakihez fellebbezni”, a Thayer sz6 szerint (a fellebbezés, ApCsel 25:11, a 4. ág egyik esete). A 3. ág („váddal illetni”) a sz5 szerint helyes („valamivel vádolni”, „váddal perbe hívni”), nem változott; a vázlatsor „τίνι a tárgy tárgyesetével” kezdete a szakasz első tagmondata, nem eltérő tagolás. Az értelmezés nem változott. A teljes 3. szakaszt elolvastam (K1). A brief `ir`-je és `munka` mezője (ertelmezo) egyeztetett eltérésként bővült.

**A próba (F131.3.19, `PARDES_DATUM=2026-10-28`, a repón kívül):**

`scope=ISTENTISZT-001 próbarender | forras=naplok/F131_proba_meres.py; general.py --kimenet (PARDES_DATUM=2026-10-28) | ts=2026-10-28`

- A Thayer `sz3` „ismert hiány” jelölése eltűnt: tiltott fordulat a gerincben 0 (előtte 1); a lapon „melléknéven” és „nevet tenni valakire” 0.
- A C) változása a generált lapon megjelenik (a próbarender 1416–1419. sora, az `ertelmezes` résben); a NAPLO-jelölés (belső) a lapra nem kerül.
- Az 1Móz 26:25 sor H8034-cellája a gyanút jelzi (A).
- Változatlan: tiltott keretezés 0; `(fordításra vár)` 65 → 46; a 32 sor címkés; ÓSZ-sor 22 (DBH 21, kimondott hiány 1); kiemelés BDB 14/15, Thayer 7/7.
- Tesztek: `teszt_szotari_gerinc` 27 OK, `teszt_szerepmatrix` OK, `teszt_forditas_kapuk` OK; nulladiff (`0ec48665`): csak az ISTENTISZT-001 lap tér el. `ellenoriz.py`: 17. szabály RENDBEN; **11. szabály SÉRTÉS (1), várt:** az éles `lexikon/ISTENTISZT-001_TUDOMANYOS.md` `ertelmezes` rése a módosított forrástól eltér, amíg a lap nem generálódik újra (⛔ DT-F131g); ugyanez a CI E28.

### 5.5 A DT-F131f 2. (utolsó) javítóköre (F131.3.20–F131.3.24): DT-F131k (a) és DT-F131l (A) a #131-ben

**Döntés (a felhasználó, 2026-10-28):** „meggondoltam. rövid úton legyen kész, de hibátlan a 131”. A DT-F131k és a DT-F131l korábbi változata („#102-ben, addig a lap jelöli”) helyett mindkét javítás a #131-ben készül: DT-F131k → (a), DT-F131l → (A), kibontás és új súlyszabály nélkül. A `DONTESEK.md` két sora erre íródott, a régi szöveg felülírtként áll (F131.3.23). A #102 briefje (1d) jelzi, hogy a két tétel elkészült, és mi maradt nála.

Modell-ellenőrzés: a session `claude-opus-5-5`, a brief `modell: opus`, egyezik.

**A) DT-F131k (a): kézi hivatkozás-javítás (F131.3.20–F131.3.21).**
- A 2.31-ben (`adat/bdb_forras_javitas.tsv`) új hibaosztály van: `hivatkozas_kezi`, a `forras_javit.py` `KEZI_HIVATKOZAS` listájából. Egy sor: H8034, a 2.30 7. sora, 1. előfordulás, `26:35` → `26:25`, `allapot=kezi`, proveniencia `manual`, az indok a TAHOT-ot és a szövegkörnyezetet nevezi meg. A tábla `--ts 2026-10-18`-cal újragenerálódott; a többi 7 202 sor változatlan, a fejlécben a 2.30 és a kód hash-e frissült.
- Egy mellékhatás: a commitolt 2.31 fejléce eddig elavult volt (a `szamkiosztas` a 2.30 fejlécét átírta, a 2.31 a régi 2.30-hash-t hordozta; a kód fejlécsablonjában a „DT-F107f” állt a „DT228” helyett). Ezért a `teszt_bont.py` `test_javitas_ellenoriz` a `0f19033e`-n bukott. Most átmegy.
- A szöveg-nézet (`nezet_general.py`, `szakasz_bemenet.py`) a `hivatkozas_kezi` sort nem alkalmazza (csak a `hivatkozas` osztályt). A fordító bemenete és az `sz<n>` hash ezért változatlan; az `ellenoriz.py` 13. szabálya RENDBEN.
- A 2.29 kinyerője (`bdb_vers_jelentes.py`) olvassa: a Strong `elofordulas`-adik, `26:35` fejezet:versű hivatkozása a 26:25-re oldódik. A `nyers` a forrás alakja marad, az okkód `forras_javitas`. A 2.31 hash-e a 2.29 `# forras:` fejlécébe került. Eredmény: H8034 `sorszam` 120 → 1Móz 26:25, `-/3`.

**B) DT-F131l (A): a tartomány utáni folytatás (F131.3.21).**
- `bdb_szelet.py` `hivatkozasok()`: a kiírt vagy örökölt hivatkozás utáni `-N` tartomány (`_TARTOMANY`) átlépése után a `_FOLYTATAS`-keresés ugyanúgy fut, mint tartomány nélkül; a tartomány nincs kibontva.
- Az első futás +1 441 sort adott a mérés 1 438-ával szemben. A 3 többletsor hamis volt: „16:8-9, 1 Samuel 21:16” (H2063), „1Sam 22:4-5, 1 Samuel 24:23” (H4686), „26:60-61, 1 Chronicles 5:…” (H5070). Az „, 1” itt a következő könyvnév része. A memóriabeli mérés ezeket a pozíció-ütközéssel kiszűrte. A javítás: a tartomány utáni ágon a folytatás nem indulhat egy kiírt hivatkozás kezdetén. Ezután az eredmény egyezik a méréssel.
- A tartomány nélküli ágon nincs ilyen ellenőrzés. A teljes táblán ott 1 ilyen sor van, és a javítás előtt is megvolt (H1004, „2Chr 10:19, 2 Chronicles 10…” → hamis 2Krón 10:2). Ez a #102-é (F102 brief 1d).
- Regressziós tesztek (`teszt_bdb_vers_jelentes.py`): „1Kin 18:24-25, 26” → 18:24 + 18:26 (a 25 nem); „Gen 18:18-19, 25-26” → 18:18, 18:25; „16:8-9, 1 Samuel 21:16” → nincs hamis 16:1; a H8034 táblasorai (26:25 `forras_javitas`; 1Kir 18:26 `folytatas`, 18:25 nincs).

`scope=adat/bdb_vers_jelentes.tsv, teljes (régi: d5968201) | forras=naplok/F131_bdb_tartomany_valtozas.py; bdb_vers_jelentes.py --ts 2026-10-28 | ts=2026-10-28 15:36`

| | érték |
|---|---|
| sorok | 160 616 → 162 054 |
| hozzáadott sor (kulcs: strong, poz, nyers, karoli_vers, utvonal) | 1 439 = 1 438 `folytatas` + 1 (a H8034 26:35 sora 26:25-re javítva; ugyanez 1 „elveszett”) |
| érintett Strong | 603 |
| új Károli-igehely | 1 430 (1 429 a folytatásból + 1Móz 26:25) |
| régi sor más `sorszam`-mal | 35 012 |
| arany | H7121 + 1Kir 18:26 (Qal/2/c), + 1Sám 3:8, 1Móz 5:29, Jer 7:14, 7:30; H8034 + 1Kir 18:26 (-/4), 1Móz 26:35 → 26:25 (-/3) |

Ez egyezik a DT-F131l A-mérésével (+1 438, 603, 35 012; `naplok/F131_bdb_tartomany_meres.py`).

**A `sorszam`-eltolódás fogyasztói.** A #131 ⓘ-i: a 2Móz 33:19 és a 2Móz 34:5 H7121-sora 128/129 → 129/130 lett, a próbalap újragenerálódik. A `nulladiff.sh 0f19033e 2026-10-28` szerint (a HEAD 6a4df95f) csak az `ISTENTISZT-001_TUDOMANYOS.md` tér el, a többi lap és a törzscikkek azonosak. Az olvasó-szerver tesztjei közül a `teszt_bdb_vers_jelentes.py` zöld. A `teszt_olvaso_szerver.py` (2 hiba) és a `teszt_pilot_aranymintaval.py` (5 hiba) a 2026-10-14-i `pardes.db`-vel fut, amely a mostani 2.29-et nem tartalmazza. A hibák a 2.29-től függetlenek (D2-pilot, szónézet). Sorszámra egyik szerver-teszt sem hivatkozik; az `m2_minta_osszevet.py` strong + poz kulccsal illeszt.

**C) Generátor (F131.3.22).** A `BDB_HIVATKOZAS_GYANU` (DT-F131k (c)) kikerült. A `forras_javitas` okkódú BDB-példánál az ⓘ a javítás forrását mondja ki: „a BDB forrásszövege itt a „26:35” helyet idézi (sajtóhiba); javítva: 1Móz 26:25 — a javítás forrása: `adat/bdb_forras_javitas.tsv`, kézi sor (`hivatkozas_kezi`, `manual`; …)”. A kiemelő (`hivatkozasok_a_szovegben`) a vers-folytatást a 2.29-cel egyezően ismeri fel, a tartomány után is („**1Kir 18:24**-25, **26**”). A forrásjavított sornál a forrás alakját emeli ki („**26:35**”), mert a magyar szöveg a forrást fordítja.

**A próba (F131.3.24, `PARDES_DATUM=2026-10-28`, a repón kívül; a HEAD 15590cea renderével bájtra azonos):**

`scope=ISTENTISZT-001 próbarender | forras=naplok/F131_proba_meres.py; general.py --kimenet (PARDES_DATUM=2026-10-28) | ts=2026-10-28 15:38`

- **1Móz 26:25:** a H8034-cella „név: Isten megjelölése · 3”, BDB-példa (`sorszam` 120); az ⓘ a javítás forrása; a „26:35” a H8034 3. szakaszában kiemelve.
- **1Kir 18:26:** a H7121 „Qal 2.c” BDB-példa (`sorszam` 100), a H8034 „név: hamis istenekről · 4” BDB-példa (`sorszam` 209); a „26” mindkét szakaszban kiemelve.
- **1Kir 18:25:** a H7121 kutatói hozzárendelés (Qal 2.c), a H8034 „*(nincs hozzárendelés)*”. A DT-F131l (A) szerint a 18:25 a „18:24-25” tartomány belseje, nem BDB-példa (kibontás nincs; a (B) mérése szerint a kibontás a H7121 „4:25-26” miatt GerincHibát okozna). Az ⓘ szövege: „ehhez a tokenhez nincs kutatói hozzárendelés és szótári példahely”. Ez pontatlan: a BDB a helyet tartományként idézi. → a ⛔ 3.1 kérdése.
- **Kiemelés:** BDB 17/18 (H7121 10/10, H8034 7/8; előtte 14/15, a nevező a 3 új példával nőtt). A hiány a korábbi: H8034 `sorszam` 3 (1Móz 12:8, `fej`). Thayer 7/7.
- **Változatlan:** tiltott keretezés 0; a 32 sor mind címkés (az elsődleges tokenen címke nélkül: 0); `(fordításra vár)` 65 → 46; ÓSZ-sor 22 (DBH 21, kimondott hiány 1).
- **Artifact:** https://claude.ai/artifact/QVHPBrCJWkSP7pT8z363vy, 5. verzió (privát, ugyanaz az URL).

**Tesztek.** Zöldek: `teszt_szotari_gerinc` 28, `teszt_bdb_vers_jelentes` 29 (a bájtazonossággal), `teszt_szerepmatrix` 44, `teszt_forditas_kapuk` 108, `teszt_ellenoriz_13` 45, `teszt_lexikon_adatres` 20. A `forras_javit.py --ellenoriz` és a `bdb_vers_jelentes.py --ts 2026-10-28 --ellenoriz` bájtra azonos.

**A kiinduló commiton (`0f19033e`, ideiglenes worktree) is meglévő hibák, nem e kör okozta:**
- `teszt_bont.py`: a `Determinizmus.test_ellenoriz` (a 2.30 ELTÉR), a `HuIlleszt.test_ellenoriz` és a `test_osszefuzo_a_mai_adaton_valtozatlan`;
- `teszt_general_ellenorzo.py` `test_eles_sema` (30 ≠ 23).

A `0f19033e`-n bukó `test_javitas_ellenoriz` most átmegy (A). `ellenoriz.py`: 14 RENDBEN, 1 SÉRTÉS. A sértés a 11. szabály, várt: az éles lap a DT-F131g-ig eltér (5.4).

## 6. ⛔ 3.1 — DT-F131f: az elfogadási próba

A felhasználó a renderelt próbalapot olvassa. A kérdés: *a szó jelentését és a hely motívumbeli funkcióját két külön dolognak látja-e?* Ugyanitt dönt a címkék szövegéről (3.1) és a 4.2 kérdéséről (az 56.15-ös kód). A próbalap az 5.5 szerinti (F131.3.24; az 5.4-é az F131.3.19). A végrehajtás itt áll.

**Döntés (2026-10-28):** orkesztrátor, a felhasználó felhatalmazásával („vedd át a döntéseket”). A felhasználó ebben a sessionben megerősítette: „Igen, az orkesztrátor döntései (2026-10-28) az én döntéseim, hajtsd végre.”

- **Az 1Kir 18:25 ⓘ-je (F131.3.25), szövegpontosítás, nem 3. kör.** A H8034-cella marad „*(nincs hozzárendelés)*”. Az ⓘ kimondja, hogy a BDB a helyet a „1Kin 18:24-25” verstartomány belsejében idézi (H7121 Qal 2.c, `sorszam` 99; H8034 4, `sorszam` 208), és a tartomány nincs kibontva (DT-F131l (A)).
  - Generátor: `bdb_tartomanyban()`. Az azonos `nyers`-ű 2.29-sorokat a 2.30 szövegbeli előfordulásokkal sorrendben párosítja; a H7121 97-es sora („1Kin 18:24 annak konkrét kérésére”) nem tartomány.
  - A 32 sorból csak ezen az egyen jelenik meg ilyen ⓘ. A próbarenderben csak ez a lábjegyzet változik. Az Artifact a 6. verzión van.
- **DT-F131f: elfogadva** a 4. próbalappal és az ⓘ-pontosítással. Az ismert maradék a lapon jelölt hiányként marad: a H8034 1Móz 12:8 fejsora (BDB-kiemelés 17/18), 46 `(fordításra vár)` (#121), a Jóel 2:32 DBH-hiánya (#146).

## 7. ⛔ 4. — DT-F131g: az éles lexikon felülírása (F131.4)

**Döntés:** felülír (orkesztrátor, a felhasználó felhatalmazásával és megerősítésével, mint fent).

`scope=lexikon/ISTENTISZT-001_TUDOMANYOS.md | forras=general.py --cel lexikon --id ISTENTISZT-001 --ir; git diff 66965807..5f0bfacd -- lexikon/ | ts=2026-10-28`

- **Lefutott:** `general.py --cel lexikon --id ISTENTISZT-001 --ir`. Az élő lap bájtra azonos a jóváhagyott próbarenderrel (F131.3.25, `PARDES_DATUM=2026-10-28`; CRLF nélkül összevetve).
- **`git diff lexikon/`:** csak az `ISTENTISZT-001_TUDOMANYOS.md` változott (+243 / −652 sor). A 7 másik lap diffje üres; a `nulladiff.sh` (5.5) szerint újragenerálva is azonosak.
- **Blokkonként** (11 blokk, ugyanazok):
  - `elofordulasok` (az 1. Előfordulások táblája: a „Jelentés (a szó)” és a „Funkció (a motívumban)” oszlop, az ⓘ-k) és `szocikkek` (a 2. Szótári háttér: a BDB/Thayer-gerinc; 764 → 347 sor): a várt tartalom;
  - `idezes` és `kolofon`: a forrás- és licenclista a két blokk új forrásait követi (`bdb_szakaszok`, `bdb_szakasz_hu`, `bdb_vers_jelentes`, `thayer_*`, `glosszak_heber_hu`, `szotar_szakasz_cimke`, `tiltott_fordulatok`). A tW és a Mounce sora és licencszövege kikerült (a brief 3. elfogadási feltétele);
  - a többi blokk (`tartalom`, `jelmagyarazat`, `kizart`, `lxx`, `kereszthivatkozasok`, `kapcsolatok`, `kapcsolodo`): csak a `ts` (2026-10-20 → 2026-10-28) és a „Generálva” dátum;
  - blokkon kívül: az `ertelmezes` rés az F131.3.18 Thayer-tagolásával (5.4: várt). A tartalomjegyzék nem változott.
- **`ellenoriz.py`:** 15 RENDBEN, 0 SÉRTÉS. A 11. szabály most RENDBEN (előtte 1 várt sértés).
- **CI-ellenőrző** (`eszkozok/ellenorzes/futtat.py`, a main-hez mért diffen): az E28 0 találat, zöld.
  - Az E16 `[ELLENŐRZŐ]` előtagot kér, mert az ág az `eszkozok/ellenoriz.py`-t módosítja (a #131 korábbi tételeiben, 17. szabály). Az előtag az E16 miatt kell, nem az E28 miatt.
  - Az előtaggal minden E-szabály zöld (kilépési kód 0); a JELENTÉS-ek (E12, E13, E25, E27, E30, E32) nem blokkolnak.
