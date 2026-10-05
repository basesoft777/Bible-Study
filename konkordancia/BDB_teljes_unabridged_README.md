# BDB teljes (unabridged) — `BDB_teljes_unabridged.tsv`

## Forrás

- **Repó:** [eliranwong/unabridged-BDB-Hebrew-lexicon](https://github.com/eliranwong/unabridged-BDB-Hebrew-lexicon) (GitHub, publikus)
- **Felhasznált fájl:** `DictBDB.json`
- **Letöltés URL:** `https://raw.githubusercontent.com/eliranwong/unabridged-BDB-Hebrew-lexicon/master/DictBDB.json`
- **Letöltés dátuma:** 2026-09-02
- **Eredeti szöveg szerzősége:** Brown, F., Driver, S. R., & Briggs, C. A. — *A Hebrew and
  English Lexicon of the Old Testament* (BDB)
- **Digitalizálás:** Tim Morton (Bible Analyzer) eredeti transzkripciója, BibleHub
  adataival kereszt-ellenőrizve; Eliran Wong JSON-formázása
- **Licenc:** közkincs (public domain) — az eredeti BDB szövege és annak digitalizált
  átirata is közkincs
- **SHA-256** (`konkordancia/BDB_teljes_unabridged.tsv`, K7, F05b):
  `dfb5b2aaa722291736d567c4e56c10d2890f2c860eadf416629e5d02f0e59acc` (F46 javított verzió, a DT-F46 kiegészítés 2 utáni állapot: 16 csere visszaállítva, F46.14; előzmények: F46.6 `ff5357fe69c19262aa2464fbae03e02a177f4a8e044b8f47290751fee4f427a0`; F34 javított verzió `5c176037617813e330eb57e883ab7fd728c19a244c42196668ea712d0f502f14`; az eredeti, K7: `1d28a84004817b8ee09eff92d762038ae2eac7351f24abd0a8b1cc5df380dfa5`)

## Konverzió

Python szkripttel (`_convert_bdb.py`, a `konkordancia/` mappában, egyszeri
segédszkript) HTML-jelölés eltávolítva, egyszerű szöveggé alakítva. A Strong-szám
oszlop a repó zero-padded konvencióját követi (4 számjegyre kitöltve, pl. `H8415`,
`H1` → `H0001`), homográf-toldalékkal együtt (pl. `H90a` → `H0090a`) — konzisztens a
`Strong_szotar.tsv` és a `TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv` konvenciójával.

## Kimenet

**`BDB_teljes_unabridged.tsv`** (8090 sor + fejléc az eredeti konverzióban; F57 óta 8093, l. „Pótlás”; 3 oszlop):
```
Strong_padded | Strong_eredeti | Teljes_szocikk
```

- **Strong_padded:** zero-padded Strong-szám, pl. `H8415`, `H0001`
- **Strong_eredeti:** a forrásfájl eredeti, nem kitöltött azonosítója (pl. `H8415`, `H1`, `H90a`)
- **Teljes_szocikk:** a teljes BDB-szócikk, tiszta szövegként (HTML-jelölés eltávolítva)

## Minőségi mutató

- **8090/8090 sor sikeresen konvertálva, üres bejegyzés nélkül** (minden sor tartalmaz
  legalább egy rövid szöveget — 10 bejegyzés 20 karakternél rövidebb, ezek legitim
  kereszthivatkozások más szócikkre, pl. `H0381` „ish-chayil" → lásd a fő szócikket).
- Ez lényegesen teljesebb, mint az openscriptures `BrownDriverBriggs.xml`, ahol a
  gyök-bejegyzések **17,5%-a (453/2595) feldolgozatlan** („new" státuszú, üres).
- Ellenőrzött minta: `H8415` (תְּהוֹם) — teljes, tartalmas szócikk (kb. 2400 karakter).

## Szerep a determinisztikus BDB-ellenőrzési protokollban

**Ez a fájl az ELSŐDLEGES teljes-BDB forrás** a determinisztikus BDB-ellenőrzési
protokoll 2. lépésében. Az openscriptures `BrownDriverBriggs.xml` +
`LexicalIndex.xml` (lásd `TBESH_TBESG_README.md`) másodlagos/tartalék szerepbe kerül
a hiányossága miatt.

**Helyesbítés (2026-09-02, pontosítva 2026-09-03):** a הום-gyök „morajló
mélység" etimológiai adat (תְּהוֹם/1Móz 1:2 kapcsán) **valós és forrással
alátámasztott** — de a forrás-hozzárendelés pontosítást igényelt. A H8415
(תְּהוֹם) BDB-szócikke saját szövegében **NEM tartalmaz gyök-eredeztető
megjegyzést** (sem "Origin:" jelölést, sem H1949-hivatkozást) — ez
ellenőrizve mind az eredeti eliranwong-forrású `DictBDB.json`-ban, mind a
belőle készült ezen `BDB_teljes_unabridged.tsv`-ben. Az "Origin: from
H1949" hivatkozás ténylegesen a **`Strong_szotar.tsv`** (openscriptures
Strong-szótár, CC BY 4.0) "Gyök/Származtatás" oszlopából származik, ahol a
H8415 sora szó szerint "from H1949"-et rögzíti — ez egy **másik lexikon**
(Strong's Concise Dictionary) tartalma, nem a BDB-é. A gyök (H1949,
"morajlani, zúgni, megzavarodni") jelentése önmagában valós BDB-tartalom
is (l. e fájl H1949 sora), csak a תְּהוֹם↔הום kapcsolatot nem a BDB, hanem a
Strong-szótár mondja ki explicit módon.

**Módszertani tanulság (pontosítva):** a determinisztikus BDB-ellenőrzési
protokollnak a fejszó eredeztetési láncát a **`Strong_szotar.tsv`
"Gyök/Származtatás" mezőjéből** kell követnie (nem a BDB szabadszöveges
szócikkéből, ami nem tartalmaz strukturált gyök-hivatkozást). A
`Strong_szotar.tsv`-ben 4245+ sor tartalmaz "from H####" vagy hasonló
(„corresponding to H####", „variation of H####", „feminine of H####")
keresztre mutató mintázatot — ez az elsődleges, program által is
kinyerhető forrás az Origin-lánc-ellenőrzéshez, nem a BDB-fájl.

## Kereszthivatkozás

Ez a fájl önálló, a `Strong_padded` mezőn keresztül join-olható a meglévő
`Strong_szotar.tsv`, `Karoli_Strong_kivonat.tsv` stb. táblákkal (l.
`Join_tabla_folyamat_magyarazat.md` mintája szerint). A meglévő fájlok
változatlanok maradtak, semmi nem lett törölve vagy felülírva.

## `BDB_etimologia_kezi_hatarok.tsv` — nyelvi háttér, D28 hatókörű 26 token (F05_SZOTAR_BRIEF.md S9)

**Részben generált, részben kézi javaslat**
(`eszkozok/bdb_etim_hatarok_import.py`). A `nyelvi_hatter` mező a szócikk
fejének (címszó, szófaj, etimológia/rokon-nyelvi anyag) az ELSŐ,
zárójelen kívüli (nulla mélységű) em-dash-ig tartó része (D41) — a héber
lexikai nyelvi háttér szerepéhez (S9). Fejléc: `strong allapot
nyelvi_hatter szocikk_hossz hatar_pozicio`.

`allapot` négy érték egyike:
- **`gepi`** (14 token) — a `nyelvi_hatter` az ELSŐ, ZÁRÓJELEN KÍVÜLI
  (nulla mélységű) em-dash (—) előtt ér véget (D41, F05b, 2026.09.29;
  `eszkozok/bdb_etim_hatarok_import.py` `zero_melysegu_emdash()`), és a
  határ a szócikk hosszának legfeljebb 40%-ánál van. A korábbi `—\s*1\s`
  minta (csak a számozott „1.” értelem kezdetét kereste) hibás volt: nem
  vette figyelembe az igealak-paradigmákat és a zárójelen belüli
  véletlen „1”-eket — l. `naplok/ELLENOR_SZOTAR_S1.md`.
- **`javaslat`** — nincs korai (a 40%-os küszöbön belüli), nulla mélységű
  em-dash; a `nyelvi_hatter` **kézzel kijelölt** szöveg, a szkript
  `KEZI_JAVASLATOK` konstansában — jóváhagyásra vár.
- **`jovahagyott`** (6 token: `H0430`, `H0922`, `H2403`, `H3678`, `H8004`,
  `H8034`) — mint a `javaslat`, de a kézi határt a felhasználó
  chat-döntéssel már jóváhagyta (2026.09.29, `naplok/
  SZOTAR_S1_7_jelentes.md`). **`H2403` NEM a „nincs korai em-dash” eset**
  — a szócikknek VAN nulla mélységű em-dash-a (a szócikk 5,8%-ánál, a
  40%-os küszöbön messze belül), de addig a pontig egy hosszú, em-dash
  nélküli, vesszővel csatolt inflektált-alak/citációs lista áll
  (construct/suffix/plural alakok versekkel), ami NEM etimológia — ez a
  D41-szabály egy ismert gyengesége: csak az em-dash-sel határolt
  használati/alak-blokkokat ismeri fel, az em-dash nélkülit nem. A kézi
  határ ezért éppen ott vágja el a szöveget, ahol az érdemi etimológia
  ténylegesen véget ér („…sin, sin-offering” után). A szkript
  `JOVAHAGYOTT` halmaza dönti el, hogy `javaslat` vagy `jovahagyott`
  legyen a kimeneti címke.
- **`nem_targyalja`** (6 token: `H0779`, `H2555`, `H5303`, `H6093`,
  `H7496`, `H7497`) — rövid szócikk, nincs külön etimológiai bekezdés;
  `nyelvi_hatter` üres. Ez **végleges állapot, nem pótlandó hiány** (D11).

A 26 token a D28 hatókör-szabálya szerinti motívum-Strong-készlet (l.
`F05_SZOTAR_BRIEF.md` §0 0.4). Az S0-beli mérés (`naplok/SZOTAR_S0_bdb_etim.tsv`,
a régi 24-tokenes hatókörön) csak a `gepi`/nem-`gepi` elkülönítést mérte
(talál-e határt a regex, igen/nem), a tényleges `nyelvi_hatter` szöveget
és a `H8414`/`H0922` besorolását ez a tétel (S1.4) adja először.

## Javítás (F34, 2026.10.01): „ψ” (Zsoltárok) hibás feloldása

A forrás a „ψ” jelet több száz helyen az előző könyvnévre oldotta fel (pl. `Isa 106:9`, `Job 97:7`). Javított dataset-verzió: 159 helyhivatkozás (56 szócikk) `Psa`-ra cserélve (TAHOT-igazolással; az A-maradék 15 helye TAHOT nélkül, a Macula MT-versszámozási táblával igazolva), mezőkulcsos táblával; csak helyhivatkozás változott. Nyers JSON nincs a repóban, ezért a TSV közvetlen javítása történt. Proveniencia és a maradék (156 hely, 94 szócikk, kézi nézet; N-F34, N-F34c): `naplok/F34_M2_naplo.md`, `naplok/F34_M2_csere.tsv`, `naplok/F34_M2_maradek.tsv`; eszköz: `eszkozok/bdb_psi_javit.py`.

## Pótlás (F57, 2026.10.05): Strong-címke nélküli szócikkek

**Mi történt.** A `DictBDB.json`-ból készült tábla minden szócikkhez egyetlen Strong-kulcsot ad. A BDB-azonosító szerint kulcsolt `konkordancia/lexikonok_nyers/BDB.lexicon` (ugyanaz a BDB-kiadás, közkincs; `adat/licencek.tsv` BDB-sor, új licencsor nem kellett) két osztályban mutatott eltérést (felmérés: `naplok/BDB_STRONG_POTLAS_M0.md`).

**1. Címke nélküli szócikkek (a tábla +3 sora).** A BDB.lexicon 846 szócikkének fejlécében nincs Strong-címke. A párosítás szabálya (`naplok/BDB_STRONG_POTLAS_M1.md` 1. szakasz; `eszkozok/bdb_strong_potlas.py`): az OSHL-lemma és a BDB-címszó normalizált alakja egyezik (holem-waw egységesítve, kantilláció és meteg nélkül, magánhangzók megmaradnak); homonímiánál a glossza dönt, különben jelölt; ha a szócikknek van címkéje, vagy a Strongnak van sora a táblában, nem párosítható. Eredmény: 3 `egyertelmu`, 0 `tobb_jelolt`, 843 `nincs_par` (`konkordancia/BDB_strong_potlas.tsv`, minden sorban `indok` és proveniencia). A felhasználó a 3 párt jóváhagyta (DT-F57a, 2026-10-05): **H4725, H4123, H0747**. Ezek a sorok a tábla **végére** kerültek (a meglévő sorok bájtra azonosak, ellenőrzés az írás előtt/után). A sor fejében az átírás az OSHL `atiras` mezője (nem a JSON anglicizált neve), a szöveg a BDB.lexicon HTML-jéből a `_convert_bdb.py` tisztításával készült.

**2. Másodlagos címke (nem kerül a táblába).** A BDB.lexicon 529 Strong-kulcsa (pl. H0136, H0341) címkével áll egy szócikk fejlécében, de a szöveg a táblában a testvér-Strong sora alatt már megvan (H0136 → H0113, H0341 → H0340). Szövegduplikáció helyett a megfeleltetés a `konkordancia/BDB_strong_alias.tsv`-ben van (generált: `python eszkozok/bdb_strong_potlas.py --alias`; oszlopok: `masodlagos_strong`, `tabla_strong`, `bdb_id`, `cimszo`, `cimszo_a_sorban`, `proveniencia`). A `cimszo_a_sorban=nem` sorok (16) címszavát a testvér-sor szövege nem igazolta (főleg többszavas nevek): ezek a megfeleltetések nem ellenőrzöttek.

**Darabszám.** A tábla 8093 sor + fejléc; a pótlás előtti SHA-256 az előző bejegyzésben áll. Új SHA-256 (`BDB_teljes_unabridged.tsv`, F57 utáni állapot): `0931fd74f7f98bc01d6ac43ca69bcdae4e39ddf798af493904906cc8decdb098`.

**Reprodukálás.** Az `--m1` a pótlás *előtti* táblaállapotra írja a párosítást (a pótolt Strongok a táblában már szerepelnek, ezért újrafuttatva `nincs_par`-ra esnének); az `--m2` idempotens (a már meglévő Strongot nem írja újra).
