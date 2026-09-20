# F6 brief — lexikon-generátor (`lexikon/[ID]_TUDOMANYOS.md`)

*Készítette: chat-menet (Opus 5), 2026-09-16, **v5** (v1: első kiadás; v2: a tisztázatlan licencű források bekerülnek a generált rétegbe — D9; v3: az 1. menet lefutott és ellenőrizve — §1.5 —, a `forrasok`-blokk licenc-mezőjét az F6.5a javítja; v4: a licenc-státuszok tisztázva — §1.6 —, a Thayer, az LSJ és a SECE már nem `tisztazatlan`, a Mounce megjelölése kötelező; **v5**: a 2. menet lefutott, de az F6.5a *(v4)* fele kimaradt — §1.7 —, a K11 és a K21 szövege átvezetve a v4-re, új F6.5b tétel egy rövid 3. menetben). Kiindulási állapot: `main` = `origin/main` = **`cb4aac3`** (F0–F5 és az SDBH-import lezárva).*
*Végrehajtás: Claude Code, a repó gyökeréből, két menetben, Sonneten. A 2. menet az 1. menet független ellenőrzése után indul. A chat-menet nem hajtja végre — ez a brief a bemenete.*
*Előzmény: `ATALAKITASI_TERV.md.md` 6. szakasz F6, 1.C, 11.5, N11; `SDBH_IMPORT_BRIEF.md` v2 N3–N4. Felhasználói döntések (2026-09-16): a lexikon egyelőre belső használatra készül, a generátor rétegenként jelöli a forrás licencét; **a repó nyilvános marad**; a G0 javaslatok elfogadva (l. Döntésnapló D1–D12).*

---

## 0. Miért tér el ez a brief a terv F6-szakaszától

A terv szerint a `[ID]_TUDOMANYOS.md` 0–8. szakasza generálható, és ezt az ISTENTISZT-001 bizonyítja. A `cb4aac3`-en mérve **három állítás nem áll**.

**Egy — nem minden szakasz generálható.** A lexikon-sablon (`6_PaRDeS_lexikon_oldal_sablon.md` v1) több szakaszban szerzői munkát ír elő: a PaRDeS-keret bővítése, a szócikkek magyar fordítása, a „Miért fontos ez a lelet” bekezdés, a TSK-találatok minősítése, a módszertani napló. Ez a brief ezért **vegyes fájlt** generál, az F4 mintájára: a generált blokkok markerek között állnak, a kézi szakaszokat a generátor nem érinti (D1).

**Kettő — a pilot két motívumra igaz, hétből.** BDB-jelentés-hivatkozás csak az ISTENTISZT-001-nél (22/29) és a KIRALY-001-nél (5/9) van; kapcsolat-sor is csak ennél a kettőnél. Az öt másik motívum lexikon-oldala explicit „adat nincs” jelölésekkel generálódik. A hiányok kitöltése tartalmi munka, nem az F6 része (D6).

**Három — a lexikon adatrétege hiányos.** A `lexikon_hivatkozasok.tsv` üres. Az `elofordulasok.tsv` jelentés-hivatkozása csak BDB-re képes (`bdb_entry_id`), és ebben a mezőben valójában Strong-szám áll, mert a helyi BDB-fájl Strong-kulcsos. A `szotar` zárt listájából hiányzik a pilot által idézett TBESH és TBESG. A TWOT-számnak nincs jogtiszta forrása a repóban. Ezt az 1. menet F6.1–F6.3 tétele pótolja, a generátor előtt.

**Egy mellékes, de fontos eltérés a pilottól.** A generált 1. szakasz szövege nem egyezik a pilotéval: a `kapcsolodas` mező az F3 betöltéskor tömörödött (1Móz 4:26: a pilot három tagmondatot ír, a tábla kettőt). **A tábla a kanonikus** (`CLAUDE.md`, „Rétegek”), ezért a pilot-összevetés az igehely-halmazra vonatkozik, nem a szövegre (K12).

---

## 1. Mért kiindulási állapot *(`cb4aac3`)*

### 1.1 Adat

| Motívum | Előfordulás-sor | Strong-tokenek (`+` mentén) | Lexikon-hivatkozás kitöltve | `kapcsolatok.tsv` |
|---|---|---|---|---|
| KIRALY-001 | 9 | G0282, G0813, G5010, H3548, H3678, H4467, H8004 | 5 (`H3548`/`1` ×4, `H8004`/üres ×1) | 9 |
| ISTENTISZT-001 | 29 | G1941, H7121, H8034 | 22 (`H7121`) | 23 |
| TEREMT-001 | 41 | G0012, H8415 | 0 | 0 |
| ALVIL-001 | 72 | G0086, H7585 | 0 | 0 |
| MENNY-001 | 9 | H0430, H1121, H5303 | 0 | 0 |
| ANTROP-001 | 8 | G4151, G5590, H2416, H5315 | 0 | 0 |
| HODIT-001 | 33 | H5303, H7496, H7497 | 0 | 0 |
| **összesen** | **201** | | **27** | **32** |

- `elofordulasok.tsv`: a `bdb_entry_id` mezőt a kódban egyetlen olvasó használja, a `general.py` `render_study_egy_id` függvénye.
- `elofordulasok.tsv` `jelentes_szam`: a 27 kitöltött sorból 3 nem felel meg a `SEMA.md` 2.2.2 union-típusának: `2.c (tagadva)` ×2 és `2.c (rokon)` ×1. Egy sorban üres (`H8004`).
- `lexikon_hivatkozasok.tsv`: 0 adatsor; a fejléc `strong	szotar	entry_id	jelentes_szam	szoveg_en	forditas_hu	forrasfajl`; a komment szerinti kulcs `strong + entry_id + jelentes_szam`, `szotar` nélkül.
- `motivumok.tsv`: az ISTENTISZT-001 `forras_study` mezője két utat tart `;`-vel elválasztva (a study és a pilot lexikon-oldal).
- A 33 görög előfordulás-sor egyikén sincs jelentés-hivatkozás.

### 1.2 Eszközök és fájlok

- `eszkozok/general.py`: `--cel {naplo,index,naplok,study,nyitott,mind}`; `ELESITHETO = {'naplo','index','nyitott'}`; a marker `<!-- GENERÁLT-KEZDET: general.py --cel <kulcs> | forrás: … | ts=… -->` / `<!-- GENERÁLT-VÉGE: <kulcs> -->`; próba alapértelmezésben a `generalt_proba/` alá.
- `eszkozok/lekerdez.py`: betöltők `load_tsk`, `load_karoli_kh`, `load_sdbh_domenek`, `load_sdgnt_domenek`, `load_sdbh_sdgnt_anomaliak`; `to_step` igehely-konverzió; a `domen` a kivonat és az anomália-fájl alapján.
- `lexikon/` könyvtár nincs. A pilot: `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` (61 KB) és `_OLVASHATO.md`.
- A lexikon-sablon v1 (2026.09.07); a „Mikor használandó” a régi `PaRDeS_motivumok.md`-re és a `motivumlog/lexikon_pilot/` útvonalra hivatkozik.

### 1.3 Források licence *(a konkordancia README-k szerint)*

| Forrás | Licenc a generált rétegben |
|---|---|
| `BDB_teljes_unabridged.tsv`, `Karoli_kereszthivatkozasok.tsv` | `közkincs` |
| `TBESG.txt`, `TBESH.txt` (STEPBible, Tyndale House) | `CC BY 4.0` |
| `TSK_kereszthivatkozasok.tsv` (OpenBible.info) | `CC BY 4.0` |
| `OSHL_lexikalis_index.tsv` (F6.1, Open Scriptures) | `CC BY 4.0` |
| `SDBH_domenek.tsv`, `SDGNT_domenek.tsv` (UBS) | `CC BY-SA 4.0` |
| `LXX_kivonat_*.tsv` | `tisztazatlan` |
| `adat/*.tsv` | `projekt-adat` |
| `Thayer_teljes.tsv` | *(v4)* `közkincs` — Thayer 1886/1889; a formázási réteg másodkézből (§1.6) |
| `LSJ_teljes.tsv` | *(v4)* `CC BY-SA 3.0` — Perseus Digital Library, `lexica` |
| `SECE_G_teljes.tsv`, `SECE_H_teljes.tsv` | *(v4)* `közkincs` — OpenScriptures Strong's, kiegészített formázással |
| `lexikonok_nyers/MCGED.lexicon` | *(v4)* `© Mounce 1993` — **kötelező, szó szerinti megjelöléssel** (§1.6) |

### 1.4 Az OSHL-forrás *(rögzítve, F6.1)*

| | |
|---|---|
| Repó | `openscriptures/HebrewLexicon` |
| Commit | `21c9add13bc727d3a951361778e97e3ff7afd1ce` |
| Letöltés | `https://codeload.github.com/openscriptures/HebrewLexicon/tar.gz/21c9add13bc727d3a951361778e97e3ff7afd1ce` |
| Fájl | `HebrewLexicon-<commit>/LexicalIndex.xml`, SHA-256 `8f7a605c58899d2f44430149c143c00903976e1e91232476677972a69e5bc85f` |
| Licenc | CC BY 4.0 (`readme.md`: forrásmegjelölés „Open Scriptures Hebrew Bible Project”; a TWOT-szám csak hivatkozásként szerepel, a TWOT szövegét nem írja át) |
| Szerkezet | `<part xml:lang="heb|arc">` → `<entry id>` → `<w xlit>`, `<pos>`, `<def>`, pontosan egy `<xref bdb strong? twot?>` |

### 1.5 Az 1. menet mért eredménye *(v3; független ellenőrzés, `2b2e642`)*

Commitok: `1139799` (brief v2), `55b1de5` (F6.1), `4ff5436` (F6.2), `5d904b6` (F6.3), `2b2e642` (F6.4); push `cb4aac3..2b2e642`.

Friss klónon megerősítve: az öt commit fájllistája (= §6); az `OSHL_lexikalis_index.tsv` és a `lexikon_hivatkozasok.tsv` SHA-256-ja; az `elofordulasok.tsv` új mezőpárja 27 `BDB`-sorral; hét próbafájl, fájlonként hét marker-pár, mindegyikben `licenc:` mezővel; a K13 minden motívumonkénti száma.

**Három lelet:**

| # | Mi | Kié | Hol javul |
|---|---|---|---|
| L1 | A `forrasok`-blokk markere `licenc: projekt-adat`, miközben `forrás:` mezője felsorolja az LXX-kivonatokat, és a blokk táblája `tisztazatlan`, illetve `CC BY-SA 4.0` sorokat is mutat. Öt fájlt érint (ALVIL, ANTROP, ISTENTISZT, KIRALY, TEREMT). A `tisztazatlan` blokkok gépi keresése így nem hozná elő ezeket az oldalakat — pont az ellen, amiért a K11 készült. | **brief**: a K11 csak az olvasott fájlokra fogalmazott, nem a blokkban megjelenített licencekre | F6.5a, K21 |
| L2 | A `forrasok`-blokk első változata blokk-szintű licenc-halmazt ragasztott minden fájlra (az OSHL-index `CC BY-SA 4.0`-t is kapott volna). A menet saját maga vette észre és javította, fájlonkénti licenc-követésre. | végrehajtás, javítva | — |
| L3 | A K8 „kilépési kód 0” feltétele teljesíthetetlen volt: az `index` már a menet előtt is 1-gyel állt (HAMART-001). A helyes feltétel: előtte és utána azonos. A `cb4aac3`-on visszamérve: `naplo` 0, `nyitott` 0, `index` 1. | **brief** | K8 szövege javítva (v3) |

Az L1 a 2. menet első tétele; a v1/v2 commitok nem íródnak át.

### 1.6 A licenc-státuszok tisztázása *(v4)*

A `biblematedata`-csomag (Eliran Wong) lexikon-moduljainak forrását és licencét a szerző saját forrásoldala (`marvel.bible/resource.php`) dokumentálja. A 2026-09-19-i lekérdezés szerint:

| Forrás | A szerző forrásoldala szerint | Besorolás |
|---|---|---|
| Thayer | 1886/1889, közkincs; a modul anyagát Tim Morton (Bible Analyzer) formázta, engedéllyel | `közkincs` — a formázási réteg eredete másodkézből, ezt a README rögzíti |
| LSJ | Perseus `lexica` repó, Creative Commons Attribution-ShareAlike 3.0 | `CC BY-SA 3.0` |
| SECE | közkincs, az `openscriptures/strongs` repóból, a szerző kiegészítő leképezésével | `közkincs` |
| MCGED | `billmounce/dictionary`, ezzel a kötelező megjelöléssel: *Mounce Concise Greek-English Dictionary, Copyright 1993 All Rights Reserved, www.teknia.com/greek-dictionary* | `© Mounce 1993`, megjelölés kötelező |
| Abbott-Smith (a TBESG alapja) | 1922-es kiadás, közkincs | `közkincs` |

**Fenntartás:** ezek a megállapítások a szerző forrásoldaláról származnak, nem a letöltött fájlokhoz csatolt licencszövegből — a `lexikonok_nyers/` fájljai nem tartalmaznak licenc-jelzést. A modulok azonossága erősen valószínű, de nem bizonyított; egy saját, rögzített import az eredeti forrásból (Perseus, OpenScriptures) ezt a bizonytalanságot is megszüntetné (N5).

**Felhasználói döntés (2026-09-19):** a Mounce marad a generált rétegben, a kötelező megjelöléssel; a Thayer beépíthető a görög oldal mélységi szintjeként.

### 1.7 A 2. menet mért eredménye és a hiányzó F6.5a-fél *(v5)*

Commitok: `cdf02dc` (F6.5a), `0fa6927` (F6.5), `0368f28` (F6.6), `7e23e61` (F6.7). `main` = **`7e23e61`**, push nincs. A K16–K22 a menet jelentése szerint teljesült.

**Három lelet:**

| # | Mi | Kié | Hol javul |
|---|---|---|---|
| L4 | Az F6.5a *(v4)* fele — a licenc-térkép frissítése (licenc-konstans, kötelező Mounce-megjelölés, `adat/SEMA.md` 2.5, `konkordancia/lexikonok_nyers/README.md`) — nem futott le: a `cdf02dc` fájllistája csak `eszkozok/lexikon_general.py` + `generalt_proba/lexikon/`, a §6 szerinti két dokumentum nélkül. A K20 ezt nem fogta meg, mert csak a *plusz* fájlokat vetette össze, a hiányzókat nem. | végrehajtás | F6.5b, K23–K26 |
| L5 | A **K23 kimaradt a zárójelentésből** (K16–K22 szerepel, a §8.2 prompt K16–K23-at kért) — épp az a kritérium, amelyik az L4-et elkapta volna. | végrehajtás | F6.5b |
| L6 | A v4 a §1.3-at, a §1.6-ot, a D16-ot és a K23-at megírta, de **a K11 és a K21 szövegét nem vezette át**: mindkettő a Thayer/LSJ/SECE/MCGED blokkokra is `tisztazatlan`-t követelt, ami a K23-mal ellentmondásban áll. A menet a K21-et a betű szerinti (v3-as) értelemben ellenőrizte, és üresen teljesült, mert ma egyetlen blokk sem olvas Thayert, LSJ-t, SECE-t vagy MCGED-et. | **brief** | K11 és K21 szövege javítva (v5) |

**Következmény a hatókörre:** mivel a hét lexikon-oldal ma csak BDB/TBESG/LXX/TSK/KH/SDBH/SDGNT/projekt-adat forrásokat olvas, a licenc-térkép javítása a generált fájlok törzsét **nem változtathatja meg**. Az F6.5b ezért szűk, dokumentum-túlsúlyos tétel; ha a hét fájl törzse mégis változik, az hiba (K25).

---

## 2. Rögzített döntések, röviden

A részletes indoklás a Döntésnaplóban.

1. **Vegyes fájl** (D1): generált blokkok + kézi szakaszok; a generátor új fájlnál vázat ír, meglévőnél csak a blokkokat cseréli.
2. **Kimenet** (D2): `lexikon/[ID]_TUDOMANYOS.md`; az 1. menetben csak próba a `generalt_proba/lexikon/` alá. Az OLVASHATÓ változat kézi, nem az F6 része. A pilot archívum marad.
3. **Jelentés-hivatkozás általánosítva** (D3): `bdb_entry_id` → `lexikon_szotar` + `lexikon_entry_id`.
4. **A jelentés fordítása adat** (D4): `lexikon_hivatkozasok.forditas_hu`, jelentésenként egyszer; az igehelyi alkalmazás az `elofordulasok.jelentes_hu`-ban marad.
5. **Kanonikus görög jelentés-forrás: TBESG** (D5).
6. **TWOT: csak a szám, OSHL-forrásból** (D7).
7. **Licenc-jelölés blokkonként** és a 9. szakaszban (D8).
8. **Licenc-jelölés forrásonként** (D9, *(v4)* D16): minden forrás a §1.3 szerinti tényleges licencét viseli. `tisztazatlan` már csak az LXX-kivonat. A Mounce-nál a szó szerinti megjelölés kötelező.

---

## 3. Tételek — 1. menet

### Tétel F6.0 — előfeltétel-mérés *(nincs commit)*

Mérd újra az 1.1–1.2 minden állítását. Ha bármi eltér, **állj meg, és jelentsd**.

### Tétel F6.1 — OSHL lexikális index import *(TWOT-szám és BDB-azonosító)*

**`eszkozok/oshl_index_import.py`**, az `sdbh_sdgnt_import.py` mintájára (`CLAUDE.md` UTF-8 őr; `--letolt` a §1.4 URL-ről ideiglenes könyvtárba a repón kívül, SHA-256-ellenőrzéssel; eltérésnél 2-es kód, írás nélkül). XML-olvasás: `xml.etree.ElementTree`.

**Kimenet: `konkordancia/OSHL_lexikalis_index.tsv`**, a három `#`-sorral (`# GENERÁLT: eszkozok/oshl_index_import.py — kézzel nem szerkesztendő.` / `# forras: openscriptures/HebrewLexicon @ 21c9add13bc727d3a951361778e97e3ff7afd1ce | LexicalIndex.xml sha256=8f7a605c…` teljes hash-sel / `# licenc: CC BY 4.0 — Open Scriptures Hebrew Bible Project; l. konkordancia/OSHL_lexikalis_index_README.md`).

Fejléc: `strong	strong_eredeti	twot	bdb_id	nyelv	oshl_id	lemma	atiras	szofaj	def_en`

Minden `<xref>` egy sor:

- `strong`: `H` + a `strong` attribútum 4 jegyre nullával kitöltve, ha az attribútum csak számjegy; különben `—`.
- `strong_eredeti`, `twot`, `bdb_id`: az attribútum, ahogy áll.
- `nyelv`: `heb` → `heber`, `arc` → `arameus`.
- `oshl_id`: az `<entry id>`.
- `lemma`, `szofaj`, `def_en`: a `<w>`, `<pos>`, `<def>` elem `itertext()`-je.
- `atiras`: a `<w xlit>` attribútuma.

Minden szöveg: `\s+` → egy szóköz, `strip()`; üres vagy hiányzó → `—`. Rendezés: tuple, `sorted()`. UTF-8, `\n` sorvég.

**Elvárt értékek** (a chat-menet referencia-futtatásából):

| | |
|---|---|
| adatsor | **10 221** |
| SHA-256 a `#`-sorok nélkül | `f5b9e02fbf8ba707eaaecccccbc5512176cc5c3c9b29c81e22a983b30b4eeef3` |
| `strong = —` | 930, ebből 8 betűs `strong_eredeti` (`b`, `c`, `d`, `i`, `k`, `l`, `m`, `s`) |
| `twot = —` | 2 918 |
| `strong ≠ —` és `twot ≠ —` | 6 640 |
| `nyelv = arameus` | 789 |
| különböző `strong` (`—` nélkül) | 8 673 |
| mintasorok (`strong` → `twot`, `bdb_id`) | `H0001` → `4a`, `a.ae.ab`; `H3548` → `959a`, `k.as.ab`; `H7121` → `2063`, `s.cy.aa`; `H8034` → `2405`, `v.dv.ab` |

*A `H7121` → `2063` és a `H8034` → `2405` egyezik a pilot SECE-ből vett TWOT-számával — ez független megerősítés.*

**`konkordancia/OSHL_lexikalis_index_README.md`**: forrás (repó, commit, hash, reprodukáló parancs); licenc és forrásmegjelölés (CC BY 4.0, „Open Scriptures Hebrew Bible Project”); a TWOT-szám hivatkozási jellege (**a TWOT-szöveg nem kerül a repóba**, tervezési napló 14. pont); oszlopok és szabályok; mért értékek; ismert korlátok (a `strong` hiánya 930 sorban; 419 Strong-számhoz több TWOT-szám tartozik, homográfok miatt *(v3: nyelvi bontás nélkül számolva; nyelvenként 417 — a join a Strong-számra megy, ezért a 419 a helyes érték)*). **`konkordancia/Validacios_naplo.md`**: új bejegyzés.

A tábla **nem kerül** az `adat/datasetek.tsv` mátrixába (D7).

### Tétel F6.2 — jelentés-hivatkozás általánosítása

**a) Migráció — `eszkozok/f6_2_lexikon_hivatkozas_migracio.py`**, az `igazolas_migracio.py` mintájára (írás előtt soronkénti összevetés, eltérésnél megállás).

- Az `adat/elofordulasok.tsv` fejlécében a `bdb_entry_id` oszlop helyére, ugyanarra a pozícióra, két oszlop kerül: `lexikon_szotar`, `lexikon_entry_id`.
- Ha a régi érték nem üres: `lexikon_szotar = BDB`, `lexikon_entry_id` = a régi érték. Ha üres: mindkettő üres.
- Minden más mező byte-azonos. A komment-sorok változatlanok.
- Elvárt: 201 adatsor; 27 sor `BDB`; 174 sor üres; a `lexikon_entry_id` értékkészlete `H7121` (22), `H3548` (4), `H8004` (1).

**b) `eszkozok/general.py`, `render_study_egy_id`:** a `BDB-entry-id` cella értéke `lexikon_entry_id`, ha `lexikon_szotar == 'BDB'`, különben `—`. **A study-próba kimenete byte-azonos marad** (K7).

**c) `adat/SEMA.md` 2.2:** a `bdb_entry_id` sor helyett:

> | `lexikon_szotar` | zárt: a 2.5 `szotar` értékkészlete | | Melyik szótár jelentésére hivatkozik a sor. Kötelező, ha `lexikon_entry_id` ki van töltve. |
> | `lexikon_entry_id` | szabad szöveg | | A szócikk azonosítója az adott szótár kulcsa szerint (l. 2.5). |

A `jelentes_szam` leírása kiegészül: *„A `lexikon_szotar` + `lexikon_entry_id` + `jelentes_szam` hármas a `lexikon_hivatkozasok.tsv` kulcsára mutat (2.5).”*

**d) `adat/SEMA.md` 2.5:**

- Kulcs: `szotar` + `strong` + `entry_id` + `jelentes_szam`.
- `szotar` értékkészlete: `BDB` | `TBESH` | `TBESG` | `Thayer` | `LSJ` | `Strong` | `SDBH` | `SDGNT` | `SECE_G` | `SECE_H`.
- `szotar` értékkészlete kiegészül: `MCGED`.
- `entry_id` szótáranként: BDB, Thayer, LSJ, SECE → a konkordancia-fájl `Strong_padded` kulcsa; MCGED → a `lexikonok_nyers/MCGED.lexicon` `G####` Strong-kulcsa (a `gkG5####` GK-kulcs nem használható, l. `lexikonok_nyers/README.md`); TBESH/TBESG → a fájl első oszlopa; SDBH/SDGNT → `entry_id` (`MainId`), a `jelentes_szam` pedig a `lexid`.
- `szoveg_en`: marad (*rövid kivonat*), kiegészítve: *„a forrásfájl sorának szó szerinti részlete; a generált lexikon innen idéz”*.
- `forditas_hu`: *„A jelentés magyar fordítása — jelentésenként egyszer. Az igehelyi alkalmazás az `elofordulasok.jelentes_hu` mezőben áll, nem itt.”*
- Új bekezdés: *„Tisztázatlan licencű szótár (Thayer, LSJ, SECE, MCGED) sora a táblába felvehető, és a generált lexikon-oldal ugyanúgy idéz belőle, mint a többiből, `tisztazatlan` licenc-jelöléssel (F6 D9).”*

**e) `adat/lexikon_hivatkozasok.tsv` komment-sora:** `# Szotari hivatkozasok. Kulcs: szotar + strong + entry_id + jelentes_szam. Sema: adat/SEMA.md 2.5`.

### Tétel F6.3 — `lexikon_hivatkozasok.tsv` első sorai

Öt sor, a meglévő fejléccel. **A `szoveg_en` minden sorban a forrásfájl megfelelő sorának szó szerinti részlete.** A szkript kinyeri, és ellenőrzi, hogy részsztring-e.

| `strong` | `szotar` | `entry_id` | `jelentes_szam` | `szoveg_en` kinyerése | `forditas_hu` |
|---|---|---|---|---|---|
| H7121 | BDB | H7121 | 2.c | a `H7121` sor 3. mezőjében: kezdet = a `'c. '` utolsó előfordulása a `'call with name of'` első előfordulása előtt; vég = a `' d. late,'` első előfordulása (kizárólagos) → 239 karakter | a pilot 184. sora, a `**🇭🇺 Magyarul:** ` előtag nélkül |
| H7121 | BDB | H7121 | 3 | kezdet = `'3 proclaim:'`; vég = az ezt követő első `' b. '` → 555 karakter | üres — a pilot fordítása csak részleteket fordít, a kivonatot nem fedi |
| H3548 | BDB | H3548 | 1 | kezdet = `'1 priest-king:'`; vég = az ezt követő első `' 2 '` → 623 karakter | üres — a pilotban nincs fordítás |
| G1941 | TBESG | G1941 | 1 | a `TBESG.txt` `G1941`-gyel kezdődő sorának utolsó mezője: `<[^>]+>` → szóköz, `\s+` → szóköz, `strip()`, majd felosztás a `\s*__(\d+)\.\s*` mintán; az `1` szegmens → 244 karakter | a pilot 232. sora, szó szerint |
| G1941 | TBESG | G1941 | 2 | ugyanígy, a `2` szegmens → 446 karakter | a pilot 234. sora, szó szerint |

`forrasfajl`: `konkordancia/BDB_teljes_unabridged.tsv`, illetve `konkordancia/TBESG.txt`. A pilot-sorszámok 1-alapúak, a `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` `cb4aac3`-beli állapotában; a szkript ellenőrzi, hogy a 184. sor `**🇭🇺 Magyarul:** `-lal, a 232. `**1.**`-gyel, a 234. `**2.`-vel kezdődik, és eltérésnél megáll.

**Elvárt SHA-256** a tábla `#`-sor nélküli tartalmára, a fenti sorrendben írva: `1dc9f69ff0a4d642d30b02c8869213dfdf4dbe0ebd089111dd81b1fee766deb3`.

*A pilot 9 fordítási blokkjából 3 került be. A többi oka: a H8034 blokk szócikk-fejléc, nem jelentés; a G2564 és a G0994 blokk egész szócikket fordít, jelentésenként nem bontható; a Thayer G1941-blokk két jelentést (4–5.) fordít együtt, a Thayer G0994-blokk egész szócikket, az LSJ-blokk pedig csak kivonatosan (D10).*

### Tétel F6.4 — a lexikon-generátor *(próba)*

**Hely:** a render-logika új modulba kerül: `eszkozok/lexikon_general.py`. A `general.py` új céllal hívja: `--cel lexikon [--id ID]`. A betöltés a `general.py` saját TSV-olvasóját és a `lekerdez.py` betöltőit használja (import, nem másolás). Az 1. menetben a `lexikon` **nem** kerül az `ELESITHETO` halmazba, és a `mind` sem futtatja.

**Kimenet:** `generalt_proba/lexikon/<ID>_TUDOMANYOS.md`, mind a 7 motívumra.

**Fájlváz** (új fájlnál teljes egészében; a `‹…›` a táblából jön):

```
# 📖 ‹id› — ‹cim›

## TUDOMÁNYOS REFERENCIA-VÁLTOZAT

*Vegyes fájl. A GENERÁLT-blokkok az `adat/` táblákból állnak elő (`python eszkozok/general.py --cel lexikon`), kézzel nem szerkeszthetők. A blokkokon kívüli szakaszok kézzel írandók; a generátor nem írja felül őket.*

## 0. Metaadatok
[blokk: metaadat]

## 1. Előfordulások
[blokk: elofordulasok]

## 1/b. PaRDeS keretrendszer *(kézi)*

*Kézzel írandó — a forrás-study 3. pontja alapján, a 2. szakasz lexikai adataival bővítve.*

## 2. Lexikon-szócikkek
[blokk: szocikkek]

### Miért fontos ez a lelet *(kézi)*

*Kézzel írandó.*

## 3. LXX-híd — nyers adat
[blokk: lxx]

## 4. TSK és Károli-KH — nyers eredmény
[blokk: tsk_kh]

### Minősítés *(kézi)*

*Kézzel írandó: független megerősítés / új találat / nem releváns.*

## 5. Kapcsolatok
[blokk: kapcsolatok]

### Alátámasztás *(kézi)*

*Kézzel írandó.*

## 6. Módszertani napló *(kézi)*

*Kézzel írandó.*

## 7. ÚJ FELISMERÉS *(kézi, ha van)*

## 8. Nyitott kérdések és séma-korlátok *(kézi)*

*Kézzel írandó.*

## 9. Források és licencek
[blokk: forrasok]
```

**Marker:** a cél-kulcs `lexikon#‹ID›#‹blokk›`, a meglévő formában, egy új `licenc:` mezővel a `forrás:` után:

```
<!-- GENERÁLT-KEZDET: general.py --cel lexikon#ISTENTISZT-001#szocikkek | forrás: adat/lexikon_hivatkozasok.tsv, konkordancia/OSHL_lexikalis_index.tsv, konkordancia/SDBH_domenek.tsv, konkordancia/SDGNT_domenek.tsv | licenc: közkincs, CC BY 4.0, CC BY-SA 4.0 | ts=2026-09-16 -->
…
<!-- GENERÁLT-VÉGE: lexikon#ISTENTISZT-001#szocikkek -->
```

A `licenc:` érték a blokkban **ténylegesen felhasznált** források licenceinek rendezett, vesszővel elválasztott halmaza, a §1.3 táblája szerint. A `forrás:` a ténylegesen olvasott fájlok listája. Minden blokk első sora a meglévő hatókör-sor mintájára egy dőlt mondat, a táblából számolt számokkal.

**A hét blokk tartalma:**

1. **`metaadat`** — `| Mező | Érték |` tábla: ID, Rövid UI-címke (`ui_cimke`), Teljes cím (`cim`), Téma, PaRDeS-szint, Státusz (`statusz` `statusz_verzio`, `statusz_datum`), Azonosság típusa, Negatív kritérium, Fölérendelt fogalom, Forrás-study (a `forras_study` `;` mentén bontva, soronként egy út), Kereszthivatkozás-napló (`tematikus_lezart/naplok/` + a `general.py` `ID_NAPLO_TERKEP`-je; ha nincs → `—`), Sablon-megfelelőség (`sablon_verzio`). Licenc: `projekt-adat`.
2. **`elofordulasok`** — `| Igehely | Kapcsolódás | PaRDeS-szint | Funkció | Strong-szám(ok) | Lexikon-jelentés |`, kanonikus sorrendben (`igehely_rendezo_kulcs`). A Lexikon-jelentés cella: `‹lexikon_szotar› ‹lexikon_entry_id› ‹jelentes_szam›`, és ha a `jelentes_hu` ki van töltve: ` — ‹jelentes_hu›`; ha nincs hivatkozás: `—`. Hatókör-sor: sorok száma, ebből lexikon-jelentéssel. Licenc: `projekt-adat`.
3. **`szocikkek`** — a motívum Strong-tokenjei (a `strong` mező `+` mentén bontva, a `^[HG]\d{4}[A-Za-z]?$` mintára illeszkedők), rendezve; tokenenként egy `### ‹strong›` alszakasz:
   - `**TWOT:**` az `OSHL_lexikalis_index.tsv` `twot` értékei ehhez a `strong`-hoz (`—` nélkül, rendezve, vesszővel); görög tokennél és találat nélkül `—`.
   - `**Szemantikai domén:**` a `domen_kod` + `domen` párok (`—` nélkül, kód szerint rendezve) az SDBH-, illetve SDGNT-kivonatból, ugyanazzal az illesztéssel, mint a `lekerdez.py domen`. **A domének száma egyezik a `lekerdez.py domen ‹strong›` `n` értékével** (K13). Az elemzetlen bejegyzésre ugyanaz a figyelmeztetés kerül, mint a `domen` kimenetében.
   - A `lexikon_hivatkozasok.tsv` sorai ehhez a `strong`-hoz, `szotar`, majd `jelentes_szam` szerint rendezve, egyenként: `#### ‹szotar› ‹entry_id› — ‹jelentes_szam›. jelentés`, alatta `> ‹szoveg_en›`, alatta `**🇭🇺** ‹forditas_hu›` vagy *„Fordítás nincs (a `forditas_hu` üres).”*, végül `*Forrás: ‹forrasfajl›*`. Ha nincs sor: *„Nincs jelentés-hivatkozás a `lexikon_hivatkozasok.tsv`-ben.”*
   - **Tisztázatlan licencű szótár sora** (`Thayer`, `LSJ`, `SECE_G`, `SECE_H`, `MCGED`) ugyanígy idéződik; ilyenkor a blokk `licenc:` mezője tartalmazza a `tisztazatlan` értéket.
4. **`lxx`** — a motívum ÓSZ-i igehelyeire (a `konyv_teszamentum` szerint) a megfelelő `LXX_kivonat_*.tsv` sorai, **csak a motívum görög Strong-tokenjeire szűrve**: `| Igehely | Görög szóalak | Morfológiai kód | Strong | Forrás-jelzés |`. Ha a motívumnak nincs görög tokenje: *„A motívum előfordulásaiban nincs görög Strong-szám, ezért az LXX-szűrés nem végezhető.”* Licenc: `tisztazatlan`.
5. **`tsk_kh`** — igehelyenként, kanonikus sorrendben: a TSK sorai `Votes ≥ 15` szűréssel, `Votes` szerint csökkenő sorrendben (`Kapcsolódó igehely magyar megjelenítése`, Votes), majd a Károli-KH sorai (a kulcs `to_step`-pel). Csak a legalább egy találatot adó igehely kap bekezdést. A `to_step`-pel nem konvertálható igehely (tartomány, jelölt alak) felsorolva a blokk végén: *„Versenkénti kereséssel nem vizsgálható: …”*. Licenc: `CC BY 4.0`, `közkincs`.
6. **`kapcsolatok`** — a `kapcsolatok.tsv` `id` szerinti sorai: Mermaid `graph LR` diagram markdown `mermaid` kódblokkban (csomópont-azonosító `n1, n2, …` az igehelyek kanonikus sorrendjében, címkéje az igehely; él-címke a `tipus`), alatta `| Forrás | Cél | Típus | Funkció | Bizonyosság | PaRDeS-szint |`. Ha nincs sor: *„Nincs kapcsolat-sor a `kapcsolatok.tsv`-ben ehhez a motívumhoz.”* Licenc: `projekt-adat`.
7. **`forrasok`** — `| Forrás | Fájl | Licenc | Blokk |`: a fájlban ténylegesen felhasznált források, a §1.3 szerint, a CC BY-SA sornál a forrásmegjelölés hivatkozásával (`konkordancia/SDBH_SDGNT_README.md`), a CC BY sorokban a forrásmegjelöléssel (STEPBible / Tyndale House; OpenBible.info; Open Scriptures Hebrew Bible Project).

**Tisztázatlan licencű forrás a generált rétegben:** megengedett, de minden blokk, amely ilyet olvas, a markerében és a 9. szakasz táblájában `tisztazatlan` licencet visel (K11).

**Új fájl vs. meglévő:** ha a célfájl nem létezik, a teljes váz íródik; ha létezik, a hét blokk törzse cserélődik a meglévő `blokk_beilleszt` logikával, a kézi szakaszok érintetlenek. Az 1. menetben ez a `generalt_proba/lexikon/` alatt fut.

---

## 4. Tételek — 2. menet *(az 1. menet független ellenőrzése után)*

### Tétel F6.5a — a `forrasok`-blokk licenc-mezője *(az élesítés előtt)*

`eszkozok/lexikon_general.py`, a `blokk_forrasok` markere. A `licenc:` mező értéke a blokk **táblájában megjelenített** licencek rendezett, egyedi, vesszővel elválasztott halmaza (az ISTENTISZT-001-nél: `CC BY 4.0, CC BY-SA 4.0, közkincs, projekt-adat, tisztazatlan`). A `forrás:` mező és a tábla tartalma nem változik.

Ugyanez az elv minden blokkra: **a marker `licenc:` mezője a blokkban ténylegesen felhasznált források licenceinek uniója.** A többi hat blokknál ez ma már teljesül.


*(v4)* **Ugyanebben a tételben a licenc-térkép is frissül**, a §1.3 és a §1.6 szerint:

- a `lexikon_general.py` licenc-konstansa: `Thayer_teljes.tsv` → `közkincs`, `LSJ_teljes.tsv` → `CC BY-SA 3.0`, `SECE_G_teljes.tsv` és `SECE_H_teljes.tsv` → `közkincs`, `lexikonok_nyers/MCGED.lexicon` → `© Mounce 1993`; `tisztazatlan` csak az `LXX_kivonat_*.tsv` marad;
- ha a fájlban bárhol MCGED-tartalom szerepel, a 9. szakasz táblája alatt **szó szerint** megjelenik: *Mounce Concise Greek-English Dictionary, Copyright 1993 All Rights Reserved, www.teknia.com/greek-dictionary*; az LSJ-sornál a Perseus-forrásmegjelölés;
- `adat/SEMA.md` 2.5, az F6.2-ben felvett bekezdés: a „tisztázatlan licencű szótár (Thayer, LSJ, SECE, MCGED)” felsorolás helyett a forrásonkénti licenc a `konkordancia/lexikonok_nyers/README.md`-re hivatkozik;
- `konkordancia/lexikonok_nyers/README.md`: a „LICENC-STÁTUSZ TISZTÁZATLAN” figyelmeztetés helyére a §1.6 táblája kerül, a forrásoldal megjelölésével és a fenntartással.

Futtasd újra a próbát (`--cel lexikon`), és vesd össze: a hét fájlban a `forrasok` marker `licenc:` mezője és a licenc-oszlop értékei változhatnak, más nem.

### Tétel F6.5 — élesítés

- A `lexikon` bekerül az `ELESITHETO` halmazba; célfájl: `lexikon/‹ID›_TUDOMANYOS.md`. A `mind` ettől kezdve a lexikont is futtatja.
- `python eszkozok/general.py --cel lexikon --ir` mind a 7 motívumra.
- A pilot (`motivumlog/lexikon_pilot/`) **nem változik**.

### Tétel F6.6 — lexikon-sablon v2 *(külön commit, elvethető)*

`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`. Tartalmi követelmények (a szöveget a menet írja, a K-kritériumok ellenőrzik):

1. Új v2 fejléc-bejegyzés a v1 elé: az F6 generátorra, a vegyes fájlra és a licenc-szabályra hivatkozva.
2. „Mikor használandó” és „Kimenet”: a TUDOMÁNYOS változat `lexikon/‹ID›_TUDOMANYOS.md`, **generált váz + kézi szakaszok**; a `motivumlog/lexikon_pilot/` csak archívumként említve; az OLVASHATÓ változat kézi.
3. „A) TUDOMÁNYOS változat”: a szakaszok sorrendje és címe a §3 F6.4 fájlváza szerint, mindegyiknél `(generált)` vagy `(kézi)` jelöléssel.
4. A „TELJES lexikon-szócikk(ek) szó szerint” követelmény helyett: a jelentés-kivonat a `lexikon_hivatkozasok.tsv` `szoveg_en` mezőjéből jön, a fordítás a `forditas_hu`-ból; új jelentés felvétele a táblába történik, nem a lexikon-oldalra.
5. Új alszakasz „Licenc és nyilvános repó”: a D9 szabálya (a tisztázatlan licencű források — Thayer, LSJ, SECE, MCGED, LXX-kivonat — idézhetők, `tisztazatlan` jelöléssel) és a TWOT-szabály (csak szám, a TWOT-szöveg nem).

### Tétel F6.7 — nyitott tételek felvétele

`NYITOTT_FELADATOK.md`, a generált blokkon **kívül**, új pontokként az N1–N6 (l. alább) egy-egy mondatban, `ÚJ (F6)` jelöléssel.

---

## 4/b. Tétel — 3. menet *(javító, v5)*

### Tétel F6.5b — a licenc-térkép élesítése *(az F6.5a kimaradt fele)*

Tartalmilag azonos a §4 F6.5a *(v4)* blokkjával; itt csak a mai állapothoz igazítva. Négy dolog:

1. **`eszkozok/lexikon_general.py`, licenc-konstans:** `Thayer_teljes.tsv` → `közkincs`; `LSJ_teljes.tsv` → `CC BY-SA 3.0`; `SECE_G_teljes.tsv` és `SECE_H_teljes.tsv` → `közkincs`; `lexikonok_nyers/MCGED.lexicon` → `© Mounce 1993`. `tisztazatlan` **csak** az `LXX_kivonat_*.tsv` marad.
2. **Mounce-megjelölés:** ha a fájlban bárhol MCGED-tartalom szerepel, a 9. szakasz táblája alatt **szó szerint** megjelenik: *Mounce Concise Greek-English Dictionary, Copyright 1993 All Rights Reserved, www.teknia.com/greek-dictionary*; az LSJ-sornál a Perseus-forrásmegjelölés. Ma egyik oldal sem olvas MCGED-et vagy LSJ-t — a kódágnak akkor is léteznie kell, és a menet ideiglenes próbával (commit nélkül) igazolja, hogy működik.
3. **`adat/SEMA.md` 2.5** — az F6.2-ben felvett bekezdésben a „tisztázatlan licencű szótár (Thayer, LSJ, SECE, MCGED)” felsorolás helyett a forrásonkénti licenc a `konkordancia/lexikonok_nyers/README.md`-re hivatkozik.
4. **`konkordancia/lexikonok_nyers/README.md`** — a „LICENC-STÁTUSZ TISZTÁZATLAN” figyelmeztetés helyére a §1.6 táblája kerül, a forrásoldal (`marvel.bible/resource.php`, 2026-09-19-i lekérdezés) megjelölésével és a §1.6 **fenntartásával** (a megállapítások a szerző forrásoldaláról valók, nem a letöltött fájlokhoz csatolt licencszövegből; l. N5).

Ezután `--cel lexikon` próba **és** `--cel lexikon --ellenoriz` az éles `lexikon/`-ra. A hét fájl törzse nem változhat (§1.7); ha változik, **állj meg és jelentsd**.

Egy commit, a §6 szerint. Az `F6_BRIEF.md` v5 saját, tétel-azonosító nélküli commitot kap.

---

## 5. Elfogadási kritériumok

### 1. menet

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K1 | Az OSHL-forrás a rögzített | az import SHA-256-ot ellenőriz; hibás hash-sel 2-es kód, írás nélkül |
| K2 | Az OSHL-kivonat a §F6.1 szerint | mind a hat mért érték és az SHA-256 egyezik; két egymás utáni futtatás byte-azonos |
| K3 | Nincs nyers adat a repóban | `git status --porcelain` csak a §6 fájljait mutatja; nincs XML, tarball, ideiglenes könyvtár |
| K4 | Nincs `csv` modul | `grep -n "import csv\|csv\." ` az új szkriptekre = 0 |
| K5 | A migráció a §F6.2 szerint | 201 sor; 27 `BDB`; 174 üres; minden más mező byte-azonos (a migrációs szkript összevetése) |
| K6 | Nincs maradék hivatkozás | `grep -rn "bdb_entry_id" eszkozok/ adat/` csak a migrációs szkriptben ad találatot |
| K7 | A study-próba nem változott | `python eszkozok/general.py --cel study` után a `git diff -- generalt_proba/tematikus_lezart/` üres |
| K8 | A régi célok nem regresszáltak | `--cel naplo --ellenoriz`, `--cel index --ellenoriz`, `--cel nyitott --ellenoriz`: a kilépési kód **az F6.2 előtti és utáni futásban azonos** *(v3: a `naplo` és a `nyitott` 0, az `index` 1 — utóbbi a HAMART-001 hiányzó betöltése miatt már a menet előtt is)* |
| K9 | A `lexikon_hivatkozasok.tsv` a §F6.3 szerint | 5 sor, az SHA-256 egyezik; minden `szoveg_en` részsztringje a `forrasfajl` megfelelő sorának |
| K10 | Hét próbafájl, ép markerekkel | `generalt_proba/lexikon/` alatt 7 fájl; fájlonként 7 `GENERÁLT-KEZDET` és 7 `GENERÁLT-VÉGE`, páronként azonos kulccsal; minden `GENERÁLT-KEZDET` tartalmaz `\| licenc: ` részt |
| K11 | *(v5)* A forrás licence jelölve | minden blokk `licenc:` mezője a `forrás:`-ában szereplő fájlok **§1.3 szerinti tényleges** licencét viseli, és a 9. szakasz táblája ugyanezt mutatja; `tisztazatlan` csak az `LXX_kivonat`-nál. Ma ez csak az `lxx` blokkot érinti, mert a `lexikon_hivatkozasok.tsv` 5 sora BDB/TBESG. *(A v1–v3 szövege a Thayer/LSJ/SECE/MCGED forrásokra is `tisztazatlan`-t kért; a §1.6 után ez érvénytelen — l. §1.7 L6.)* |
| K12 | Pilot-összevetés | ISTENTISZT-001: az 1. szakasz igehely-halmaza 29 elemű, és a pilot 1. szakaszának halmazával egyezik, egyetlen ismert kulcsalak-eltéréssel (`Jóel 2:32 (MT) / 3:5 (Károli)` ↔ `Jóel 2:32`) |
| K13 | Blokk-tartalom az adatból | fájlonként: az 1. szakasz sorainak száma = §1.1; a `###` szócikk-alszakaszok száma = a Strong-tokenek száma (7, 3, 2, 2, 3, 4, 3); a `####` jelentés-sorok: ISTENTISZT-001 4, KIRALY-001 1, a többi 0; a `**🇭🇺**` sorok: ISTENTISZT-001 3; minden domén-szám = a `lekerdez.py domen` `n` értéke; a TWOT az ISTENTISZT-001-nél `H7121` → 2063, `H8034` → 2405, `G1941` → `—`; a kapcsolat-táblák sorszáma ISTENTISZT-001 23, KIRALY-001 9, a többi az üres-mondat |
| K14 | Determinizmus és kézi szakasz | két egymás utáni próbafuttatás byte-azonos; egy próbafájl kézi szakaszába beírt tesztsor az újrafuttatás után megmarad, majd a tesztsor visszavonva (commit nélkül) |
| K15 | Tétel-szintű commitok | minden `F6.*` commit fájllistája a §6 szerint |

### 2. menet

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K16 | Élesítés | `lexikon/` alatt 7 fájl; `--cel lexikon --ellenoriz` kilépési kódja 0; a második `--ir` után `git diff` üres; a `lexikon/` generált blokkjainak törzse (a marker-sorok nélkül) byte-azonos a `generalt_proba/lexikon/` blokkjaiéval |
| K17 | A pilot érintetlen | `git diff cb4aac3 -- motivumlog/lexikon_pilot/` üres |
| K18 | Lexikon-sablon v2 | `grep -c "TELJES lexikon-szócikk"` = 0; `lexikon/` útvonal jelen; minden `##`/`###` szakaszcím a TUDOMÁNYOS részben `(generált)` vagy `(kézi)` jelölést visel; a „Licenc és nyilvános repó” alszakasz jelen; a v2 bejegyzés jelen |
| K19 | Nyitott tételek | az N1–N6 hat `ÚJ (F6)` pontként jelen; a generált blokk a diffben nem változik |
| K20 | Commitok | az `F6.5a`–`F6.7` fájllistája a §6 szerint |
| K21 | *(v3, v5)* Minden marker licence teljes | minden `GENERÁLT-KEZDET` sorra: a `licenc:` mező a blokkban felhasznált összes forrás **§1.3 szerinti** licencének uniója — `LXX_kivonat` → `tisztazatlan`, `Thayer` és `SECE_` → `közkincs`, `LSJ` → `CC BY-SA 3.0`, `MCGED` → `© Mounce 1993`; a `forrasok`-blokknál a `licenc:` a tábla licenc-oszlopának egyedi halmaza |
| K22 | *(v3, v4)* Az F6.5a nem változtat mást | a próba újrafuttatása után a `git diff -- generalt_proba/lexikon/` csak a `forrasok` markerek `licenc:` mezőjét, a 9. szakasz licenc-oszlopát (és a `ts=` értékét) érinti |
| K23 | *(v4)* Licenc-térkép — **a 2. menetben elmaradt, l. §1.7 L5 és a 3. menet táblája** | `grep -c "tisztazatlan"` a hét fájlban csak `LXX_kivonat`-ot tartalmazó blokkokban ad találatot; a `Thayer`, `LSJ`, `SECE` sorok a §1.3 szerinti licencet viselik; MCGED-tartalom esetén a Mounce-megjelölés szó szerint jelen van |

### 3. menet *(v5)*

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K23 | *(v4; a 2. menetben elmaradt)* Licenc-térkép | `grep` a hét éles fájlban: `tisztazatlan` csak olyan blokkban, amelynek `forrás:` mezőjében `LXX_kivonat` áll; a licenc-konstansban a `Thayer`/`SECE_` `közkincs`, az `LSJ` `CC BY-SA 3.0`, az `MCGED` `© Mounce 1993` |
| K24 | Dokumentumok átvezetve | `konkordancia/lexikonok_nyers/README.md`: `grep -c "LICENC-STÁTUSZ TISZTÁZATLAN"` = 0, a §1.6 öt sora és a fenntartás jelen; `adat/SEMA.md` 2.5: a négyes felsorolás helyén a README-hivatkozás |
| K25 | Szűk hatókör | `git diff -- lexikon/ generalt_proba/lexikon/` a marker `ts=` mezőjén kívül üres, mind a 14 fájlban; `--cel lexikon --ellenoriz` kilépési kódja 0 |
| K26 | Mounce-ág bizonyítva | ideiglenes, commit nélküli próbával (pl. egy MCGED-sor ideiglenes felvétele a `lexikon_hivatkozasok.tsv`-be): a 9. szakasz alatt a megjelölés szó szerint megjelenik, a marker `licenc:`-e `© Mounce 1993`-at kap; a próba után minden visszaállítva, `git status --porcelain` a §6-on kívül üres |
| K27 | Commit | az `F6.5b` fájllistája a §6 szerint; a `naplo`/`index`/`nyitott` `--ellenoriz` kilépési kódja változatlan (0 / 1 / 0) |

---

## 6. Commit és push

Tétel-szintű commitok, magyar üzenettel, UTF-8 fájlból (`git -c i18n.commitEncoding=UTF-8 commit -F commit_uzenet.txt`).

| Commit-üzenet | Fájlok |
|---|---|
| `F6.1: OSHL lexikális index import — TWOT-szám és BDB-azonosító kivonat` | `eszkozok/oshl_index_import.py`, `konkordancia/OSHL_lexikalis_index.tsv`, `konkordancia/OSHL_lexikalis_index_README.md`, `konkordancia/Validacios_naplo.md` |
| `F6.2: elofordulasok.tsv — bdb_entry_id → lexikon_szotar + lexikon_entry_id; SEMA 2.2/2.5` | `eszkozok/f6_2_lexikon_hivatkozas_migracio.py`, `adat/elofordulasok.tsv`, `adat/SEMA.md`, `adat/lexikon_hivatkozasok.tsv`, `eszkozok/general.py` |
| `F6.3: lexikon_hivatkozasok.tsv — öt jelentés-sor (BDB, TBESG), három pilot-fordítással` | `eszkozok/f6_3_lexikon_hivatkozasok_toltes.py`, `adat/lexikon_hivatkozasok.tsv` |
| `F6.4: general.py --cel lexikon — lexikon-generátor, próba a generalt_proba/lexikon/ alá` | `eszkozok/lexikon_general.py`, `eszkozok/general.py`, `generalt_proba/lexikon/` (7 fájl) |
| `F6.5a: lexikon_general.py — teljes licenc-halmaz a markerben, tisztázott licenc-térkép` | `eszkozok/lexikon_general.py`, `adat/SEMA.md`, `konkordancia/lexikonok_nyers/README.md`, `generalt_proba/lexikon/` (7 fájl) |
| `F6.5: lexikon élesítve — lexikon/[ID]_TUDOMANYOS.md, hét motívum` | `eszkozok/general.py`, `lexikon/` (7 fájl) |
| `F6.6: lexikon-sablon v2 — generált váz, kézi szakaszok, licenc-szabály` | `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` |
| `F6.7: NYITOTT_FELADATOK.md — az F6 nyitott tételei` | `NYITOTT_FELADATOK.md` |
| *(v5)* `F6.5b: licenc-térkép élesítve — Thayer/SECE közkincs, LSJ CC BY-SA 3.0, kötelező Mounce-megjelölés` | `eszkozok/lexikon_general.py`, `adat/SEMA.md`, `konkordancia/lexikonok_nyers/README.md` |

Az F6.0 nem commitol. A brief saját commitja tétel-azonosító nélkül megy (`F6_BRIEF.md v5: …`). **Push csak külön kérésre.**

*(v5)* Az F6.5b commitjában a `lexikon/` és a `generalt_proba/lexikon/` **nem szerepel**: a §1.7 szerint a törzsük nem változhat. Ha mégis szerepelnie kellene, az a K25 sérülése — előtte megállás és jelentés.

---

## 7. Amit ez a brief szándékosan nem kér

- **A jelentés-hivatkozások kitöltését** az öt adatszegény motívumra és a 33 görög sorra — külön tartalmi menet, Opuson (N1).
- **A `jelentes_szam` három union-sértő értékének** (`2.c (tagadva)`, `2.c (rokon)`) szétválasztását (N2).
- **A Formula és a Kapcsolódó motívum mezőt** a `motivumok.tsv`-ben (N3).
- **Az OLVASHATÓ változatot** — kézi, motívumonként.
- **A tisztázatlan források licencének tisztázását** (N4, N5).
- **A `CLAUDE.md` N4-es eltéréseit** (`F5_BRIEF.md`) és a `general.py` más céljainak módosítását.
- **A `datasetek.tsv` bővítését** az OSHL-indexszel (D7).

---

## 8. Futtatás és modellválasztás

**Két menet, Sonnet.** Migrációs és generátor-menet (terv D11); a tartalmi ítéletet igénylő rész (fordítás, minősítés) kívül esik.

**Megállási pontok:** az F6.0 után, ha bármi eltér; SHA-eltérésnél (F6.1, F6.3); a migráció soronkénti összevetésénél (F6.2); ha a pilot horgonysorai nem a várt előtaggal kezdődnek (F6.3); minden commit előtt a hozzá tartozó K-kritériumok.

### 8.1 Az 1. menet nyitó promptja

```
Olvasd el a CLAUDE.md-t, majd az F6_BRIEF.md-t teljes egészében.

0. F6.0: main = origin/main = cb4aac3? Mérd újra a brief 1.1–1.2 pontját.
   Ha bármi eltér, állj meg és jelentsd — ne írj semmit.
1. F6.1: eszkozok/oshl_index_import.py --letolt; a kivonat, a README és a
   validációs naplóbejegyzés. Futtasd kétszer (K2). K1–K4. Commit.
2. F6.2: futtasd a K8 három ellenőrzését MOST (előtte-állapot). Migrációs
   szkript soronkénti összevetéssel; general.py render_study_egy_id; SEMA 2.2
   és 2.5; lexikon_hivatkozasok.tsv komment-sora. K5–K8. Commit.
3. F6.3: eszkozok/f6_3_lexikon_hivatkozasok_toltes.py a brief táblája szerint.
   K9. Commit.
4. F6.4: eszkozok/lexikon_general.py + general.py --cel lexikon; próba mind
   a 7 motívumra. K10–K14. Commit.
5. K15 az F6.1–F6.4 commitokra.

Héber vagy görög karaktert tartalmazó kódot csak fájlból futtass.
Push nincs. Zárójelentés: commit-hash-ek, K1–K15 kritériumonként, a K13
számai motívumonként táblázatban, a TSK/KH-blokkok találatszáma és a
„versenként nem vizsgálható” igehelyek motívumonként, és minden eltérés.
```

### 8.2 A 2. menet nyitó promptja *(az 1. menet független ellenőrzése után)*

```
Olvasd el az F6_BRIEF.md 4. pontját és az 5. pont 2. menet-tábláját.

0. Ellenőrizd: main = origin/main = 2b2e642. Ha nem, állj meg.
1. F6.5a: lexikon_general.py blokk_forrasok marker licenc-mezője + a
   licenc-térkép frissítése (SEMA 2.5, lexikonok_nyers/README.md);
   próba újrafuttatása. K21, K22, K23. Commit.
2. F6.5: ELESITHETO + lexikon; --cel lexikon --ir. K16, K17, K21 az éles
   fájlokra is. Commit.
3. F6.6: lexikon-sablon v2 a brief öt követelménye szerint. K18. Commit.
4. F6.7: NYITOTT_FELADATOK.md, hat új pont. K19. Commit.
5. K20.

Push nincs. Zárójelentés: hash-ek, K16–K23 kritériumonként, a sablon-diff
szakaszcímei, és minden eltérés.
```

### 8.3 A 3. menet nyitó promptja *(javító, v5; Sonnet)*

```
Olvasd el az F6_BRIEF.md §1.7, §4/b és §5 „3. menet” pontját.

0. Ellenőrizd: main = 7e23e61, a munkafa tiszta (az F6_BRIEF.md
   módosítottan állhat). Ha nem, állj meg.
1. F6.5b a §4/b négy pontja szerint. K23, K24, K26.
2. --cel lexikon próba, majd --cel lexikon --ellenoriz az éles lexikon/-ra.
   K25. Ha bármelyik fájl törzse változik, ÁLLJ MEG és jelentsd — ne commitolj.
3. naplo/index/nyitott --ellenoriz regresszió (0 / 1 / 0). K27.
4. Commit a §6 F6.5b sora szerint. Külön commit: F6_BRIEF.md v5.

Héber vagy görög karaktert tartalmazó kódot csak fájlból futtass.
Push nincs. Zárójelentés: hash-ek, K23–K27 kritériumonként (mindegyik
külön sorban, kihagyás nélkül), a K26 ideiglenes próbájának kimenete,
és minden eltérés — külön kiemelve a hiányzó és a plusz fájlokat a §6
táblájához képest.
```

---

## Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | Vegyes fájl: generált blokkok + kézi szakaszok, marker-alapon | A sablon több szakasza szerzői munka. Az F4 G0 döntése (marker-alapú részleges generálás) itt is működik, és a kézi szöveg újragenerálásnál sem vész el. |
| D2 | `lexikon/[ID]_TUDOMANYOS.md`; előbb próba, élesítés a 2. menetben | A terv 1.C útvonala. Az F4 mintája: a próba maga a diff, az élesítés független ellenőrzés után. |
| D3 | `bdb_entry_id` → `lexikon_szotar` + `lexikon_entry_id` | A mező csak BDB-re képes, a görög oldalnak nincs helye. Az általánosítás a `lexikon_hivatkozasok.tsv` kulcsára mutat; egyetlen kódbeli olvasó van. |
| D4 | A jelentés fordítása a `lexikon_hivatkozasok.forditas_hu`-ban, jelentésenként egyszer | Az `elofordulasok.jelentes_hu` igehelyi glossza (a H3548/1-hez négy különböző szöveg). Ha a lexikon-oldal fordítása kézi szöveg, minden oldalon újra íródik és szétcsúszik. |
| D5 | Kanonikus görög jelentés-forrás: TBESG | Jogtiszta (CC BY 4.0), számozott jelentésekkel, a héber LXX-megfelelőt is jelzi. A Thayer mélyebb, de a digitalizált fájl licence tisztázatlan. |
| D6 | Az 5 adatszegény motívum explicit „adat nincs” jelöléssel generálódik; a kitöltés külön menet | `CLAUDE.md` 3. szabály: üres eredmény elfogadható, hiány nem tölthető ki. A generátor a hiányt láthatóvá teszi, és abból lesz a tartalmi menet munkalistája. |
| D7 | TWOT: csak szám, az OSHL `LexicalIndex.xml`-ből; a tábla nem kerül a `datasetek.tsv`-be | A tervezési napló 14. pontja; a SECE_H licence tisztázatlan. A tábla generátor-segédtábla (Strong ↔ BDB-azonosító ↔ TWOT), study nem hivatkozza közvetlenül. |
| D8 | Licenc a markerben és a 9. szakaszban | A felhasználó 3. iránya: a publikálási döntés halasztva, de minden generált blokkról gépileg kiolvasható, milyen licencű forrásból áll. |
| D9 | A tisztázatlan licencű források (Thayer, LSJ, SECE, MCGED, LXX-kivonat) bekerülnek a generált rétegbe, `tisztazatlan` jelöléssel | Felhasználói döntés (2026-09-16, a brief v1 átnézésekor). A repó nyilvános marad. **Rögzített kockázat:** az MCGED (Mounce) valószínűleg védett kereskedelmi mű, és a terv 11.5/3.10 elve a hosszú, szó szerinti harmadik-fél-szöveg ellen szól. A blokkonkénti jelölés miatt gépileg visszakereshető, mi érintett, ha a döntés később megfordul. |
| D10 | A pilot 9 fordításából 3 kerül a táblába | Csak az, amelyik egyetlen jelentéshez rendelhető, és a teljes kivonatot fedi. A többi a pilotban marad. |
| D11 | A pilot-összevetés az igehely-halmazra vonatkozik, nem a szövegre | A `kapcsolodas` mező az F3-ban tömörödött; a tábla a kanonikus. |
| D12 | A TSK/KH-blokk a `lekerdez.py` pontos igehely-illesztését követi | Egy igazságforrás: a lexikon ugyanazt mutassa, amit a lekérdezés. A tartományos igehelyek felsorolva, nem csendben kihagyva. |
| D13 | A render-logika külön modulban | A `general.py` már 1 193 sor; a lexikon hét blokktípusa külön modulban tesztelhető. |
| D14 | Két menet, Sonnet | Terv D11; a tartalmi ítélet kívül esik. |
| D16 | *(v4)* A Thayer, az LSJ és a SECE a tényleges licencét kapja; a Mounce marad, kötelező megjelöléssel | A §1.6 tisztázása után a `tisztazatlan` gyűjtőcímke ezeknél félrevezető lenne. A Mounce az egyetlen kifejezetten jogfenntartott forrás, ezért nála a megjelölés nem díszítés, hanem feltétel; felhasználói döntés (2026-09-19), hogy benne marad. |
| D17 | *(v5)* A kimaradt licenc-térkép önálló F6.5b tételként, rövid 3. menetben fut, a `cdf02dc` átírása nélkül; a K11 és a K21 szövege a v4-hez igazítva | A v1–v3 commitok nem íródnak át (a §1.5 elve). A K21 és a K23 ellentmondása a brief hibája volt — javítás nélkül a 3. menet ugyanabba futna bele. Az F6.5b hatóköre szándékosan dokumentum-túlsúlyos: a generált törzs változása itt hiba, nem eredmény. |
| D15 | *(v3)* A marker `licenc:` mezője a blokkban megjelenített licencek uniója, nem csak az olvasott adatfájloké | Felhasználói döntés (2026-09-19). A 9. szakasz azért van, hogy egy helyen lássuk az oldal licenc-képét; ha a marker ezt nem tükrözi, a gépi keresés kihagyja az érintett oldalakat. A `forrás:` mező marad az, amit a blokk olvasott. |

### Nyitott, a briefben szándékosan el nem döntött kérdések

- **N1 — Jelentés-hivatkozások kitöltése.** Az 5 adatszegény motívum héber sorai (BDB) és a 33 görög sor (TBESG), a hozzájuk tartozó `lexikon_hivatkozasok` sorokkal és fordításokkal. Külön Opus-menet; a munkalista a generált lexikon „Nincs jelentés-hivatkozás” soraiból áll össze.
- **N2 — A `jelentes_szam` három union-sértő értéke.** A `(tagadva)` és a `(rokon)` igehelyi megjegyzés, nem jelentésszám. Hová kerüljön: a `kapcsolodas`-ba, új mezőbe, vagy a `jelentes_hu`-ba?
- **N3 — Formula és Kapcsolódó motívum.** A sablon 0. szakasza kéri, a `motivumok.tsv`-ben nincs mezőjük. Új mezők, vagy maradnak kézi szövegként?
- **N4 — A tisztázatlan források kockázata.** A D9 szerint idézhetők; az MCGED (Mounce) valószínűleg védett. Ha publikálás vagy megkeresés merül fel, a `tisztazatlan` jelölésű blokkok az elsők, amelyeket jogilag át kell nézni.
- **N5 — Saját import az eredeti forrásokból.** *(v4: a licenc-státuszok tisztázva, l. §1.6.)* A Thayer, az LSJ és a SECE ma egy köztes csomagon át érkezett. Egy rögzített commitra hivatkozó saját import (Perseus `lexica`, `openscriptures/strongs`) a proveniencia-bizonytalanságot is megszüntetné, és megnyitná a Thayert a görög oldal mélységi szintjeként (kétszintű fordítási séma).
- **N6 — A KIRALY-001 `G0813` tokenje.** A `NYITOTT_FELADATOK.md` szerint téves (helyesen `G0540`), és a generált szócikk-alszakasz ezt továbbviszi. Felhasználói megerősítésre vár.
