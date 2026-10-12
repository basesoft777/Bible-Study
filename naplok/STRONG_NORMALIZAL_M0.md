# STRONG_NORMALIZAL — M0 jelentés (F62)

*2026.10.11 · ág: `claude/strong-normalizal` · adattáblát nem írtam; a mérő szkriptek a munkamenet scratchpadjén futottak (`split('\t')`, `csv` nélkül), kimenetük az alábbi számok.*

## 1. Leltár — a `grep` által talált Strong-kezelő függvények (`eszkozok/`)

A mérés nem teljes bejárás: a függvénynevekre (`strong`/`norm`) kerestem, a törzset az A és B csoportnál olvastam végig; a C csoportot csak megneveztem.

**A. Négyjegyűre nulláz („pad-4”) — SEMA 1.2-hez közeli (14)**

| Függvény | Fájl | Bemenet → kimenet | Eltérés a SEMA 1.2-től |
|---|---|---|---|
| `strong_padded` | `emeles.py:99` | `^[GH]\d{1,4}[a-z]?$` → `G0012`; nem illő: `None` | betűutótagot megtart; csak 1–4 jegyet fogad |
| `strong_eredeti` | `emeles.py:107` | nullátlanít (`H0430`→`H430`) | ellentétes irány (kijelzés) |
| `_strong_padded` | `ellenoriz.py:624` | `^([GH])0*(\d{1,4})([a-z]?)$` | ua.; `None` hibára |
| `_e19_strong` | `ellenorzes/szabalyok.py:983` | mint fent, de nem illőt **változatlanul** ad | csendes átengedés |
| `strong_norm` | `ellenorzes/tanulmany_ellenorzes.py:181` | `[a-zA-Z]?` utótag **eldobva**; `None` hibára | utótagot elhagy |
| `strong_norm`/`strong_padded` | `bdb_adatblokk.py:85,102` | csak H; `H2617`-et ad (nem nullázott), `strong_padded` nullázott utótaggal | kétlépcsős, csak H |
| `norm_strong` | `lxx_osszevetes.py:61` | minden nem-számjegyet töröl, `"G"`-t tesz elé | betűt/előtagot eldob, mindig G; `0`→`""` |
| `normalize` | `merge_karoli_szofaj.py:33` | `^([HG])(\d+)([A-Za-z]*)$` → 4 jegy, utótag marad; nem illő: változatlan | 5+ jegyű számot nem hibáztat |
| `normalize_strong` | `tw_import.py:61` | H: `zfill(4)`; G: 5 jegynél az **utolsó** számjegyet levágja (`G20447`→`G2044`) | specifikus (tW 5 jegyű G); `G00120`-ot 5 jegynek veszi → `G0012` |
| `normalizal` | `tbesh_konszolidalt_import.py:77` | csak H, utótag marad, nem illő: változatlan | csak H |
| `_strong_nullaz` | `karoli_strong/tokenek.py:286` | `^[HG]\d+$` → 4 jegy; nem illő: változatlan | utótagot nem kezel |
| `normal` | `karoli_strong/elopar_kjv.py:102` | `H430`/`H0430a` → `H0430` | utótagot eldob; nem illő: változatlan |
| `lxx_os_strong_normalizalt` | `lexikon_general.py:1067` | csupasz szám → `G%04d`; nem szám: `""` | csak G, csak számjegy |
| `strong_alak` | `lekerdez.py:471` (beágyazott) | `^(\d+)([a-z]*)$` → `G%04d`+utótag | csak G, csupasz szám bemenet |

**B. A két célfájl mai kezelése (l. 3. pont).**

**C. Szám-kinyerők (`int`-et adnak, SEMA-alakot nem) (6):** `bdb_adatblokk.strong_szam`, `bdb_konyv_javit.strong_szam`, `fj2/kozos.strong_szam`, `f17/macula_futtat.strong_szam`, `tahot_verskulcs_esetlista.strong_szam`, `lxx_bridge_egyezes.norm`.
**D. Import-elemzők, törzsüket nem olvastam végig (≥8):** `f17/macula_import.strong_ertek/strong_feldolgoz`, `sdbh_sdgnt_import`/`ubs_dbh_import`/`ubs_dntg_import.parse_strong_codes`, `oshl_index_import.strong_from_attr`, `tahot_zarojeles_phaseA_kivonat.clean_strong`, `fj2/macula.szo_strong`, `sdbh_sdgnt_ellenoriz.normalized_codes_of`. A `lekerdez.py` két regexe (`_DOMEN_PLAIN_RE`, `_STRONG_PART_RE`) is saját mini-szabály.

Összesen **legalább 28 önálló Strong-függvény/regex**, ebből 14 pad-4 normalizáló. Az N37 „hét” alulbecslés. A 14 normalizáló három kérdésben **nem egyezik**: (i) betűutótag megtartása/eldobása, (ii) nem illő bemenetre `None` / változatlan érték / kivétel hiányzik mind, (iii) H és G kezelése. Hibát dobó egy sincs.

## 2. Bemeneti alakok (mért, a datasetekből; `konkordancia/*.tsv`, nem `adat/`)

| # | Alak | Példa | Hol | Darab (nagyságrend) | Javasolt kimenet |
|---|---|---|---|---|---|
| 1 | SEMA-alak | `H0779` | adat/, TAHOT, TAGNT | — | változatlan |
| 2 | nullázatlan 1–3 jegy, előtaggal | `H1`, `H70`, `H935`, `G976` | ASV/KJV/BSB, SECE/LSJ/Thayer/BDB `Strong_eredeti` | ~700 000 sor | `H0001`, `H0070`, `H0935`, `G0976` |
| 3 | előtag nélküli szám | `1078`, `976` | Macula `strong_x` (nyelv oszlop dönt), LXX_OS, CLI | ~275 000 | **kivétel** előtag nélkül; a hívó adja a nyelvet (`strong_normalizal(s, nyelv=)`) — ld. döntés a) |
| 4 | betűutótagos | `H2967a`, `G3924a`, `H0032a` | Macula, SDBH/SDGNT/UBS, LXX_versszintu_parok | ~230 000 | **döntés b)**: SEMA 1.2 nem ismer utótagot |
| 5 | 5 jegyű | `G20447`, `H07121` (kézi md) | Strong_szotar/TAGNT (kiegészítő kódok, 5 db), tW | kevés | tW-ben a záró számjegy; Strong_szotar/TAGNT esetén **érvényes, külön kiosztott** kód. Nem csonkolható egységesen — döntés c) |
| 6 | `A####` (arámi) | `A0002` | SDBH `strong_kod` | 2 086 | `strong_normalizal`: kivétel (H/G csak); az arámi külön kérdés — döntés d) |
| 7 | `+` lánc | `H8414+H0922`, `G5228+G1537+G4053` | Karoli_Strong_kivonat, Macula, tW, Strong_szotar | ~400 | elemenként normalizál, sorrendet megőriz |
| 8 | `,`/`\|`-elválasztott lista | `H0710,H0713`; `1886j\|2050b` | BDB_strong_alias_elvetett, Macula | 26 + 5 | nem lánc: **kivétel**; a hívó vágja szét |
| 9 | TIPNR-utótag | `H5653G`, `H5660I` | TIPNR_kivonat | 16 928 | nem Strong-alak (név-azonosító); **kivétel**, saját kezelés |
| 10 | gondolatjel/üres | `—`, `` | OSHL | 1 327 | üres/`—`: kivétel; hívó kezeli az üreset |
| 11 | kisbetű | `h0779`, `g2564` | kézi md (10 előfordulás), CLI | kevés | nagybetűsít |
| 12 | szóköz körülötte | ` H0779 ` | (nem mért; kézi bevitel) | — | `strip()` |
| 13 | kézi md-ben nullázatlan | `G994` (14), `H430` (10), `H410`, `G2` | tematikus tanulmányok szabad szövege | 91 találat | nem normalizálandó (szabad szöveg, a brief „Nincs benne”) |

*A munkaterv „20 ismert eltérő alak” helyett a mért alakszám 13 család, a darabszámok fenti nagyságrendje.*

## 3. A `lekerdez.py` és a `betolt.py` mai Strong-kezelése

- **`lekerdez.py`**: nincs normalizálás. `scan`/`igealak`: `strip().upper()`, majd `startswith('H'|'G')`, és szó szerinti `==` összevetés a TAHOT/TAGNT oszloppal. **Mért:** `scan H0779` → 52 igehely; `scan h0779` → ugyanaz; `scan H779` → **0 igehely, hibaüzenet nélkül** (néma nem-találat, a CLAUDE.md által leírt hibaosztály). `kollokacio`: `.strip().upper()`, szintén nincs nullázás. `domen`: `_DOMEN_PLAIN_RE = ^[HG]\d{4}$` dönt (egyszerű vs. `strong_kod` ág), a többi (`H779`) a `strong_kod`-egyezés ágra esik, szintén néma nem-találat. `_anomaly_part_matches` az `A####`→`H####` leképezést végzi. `lxx` ág: `strong_alak` (G-nullázás, betűutótag marad), `strong_tagnt` levágja az utótagot.
- **`betolt.py`**: a kulcsszó-táblázat `Strong-szám` oszlopát `split('+')` + `strip()` bontja, **normalizálás és validálás nélkül**; a kimenetben (`kulcsszavak.tsv`, `strong`) az érték úgy áll, ahogy a tanulmány írta. A `kulcsszavak.tsv` ma 0 nem üres sor (`nemüres=0`), tehát a betöltő Strong-ága jelenleg nem hoz létre adatot, a hibaosztály lappang.

## 4. Mérés — SEMA 1.2 az adattáblákon

| Hatókör | Oszlopok | Nem üres cella | SEMA 1.2-nek nem megfelelő |
|---|---|---|---|
| `adat/*.tsv` (kivéve `karoli_strong/`): `bdb_igehely_javitas`, `elofordulasok` (251; 8 üres), `forditasok`, `grammatikai_strongok`, `kiejtes_heber_kivetelek`, `kulcsszavak`, `lexikon_hivatkozasok`, `lxx_dontesek` (heber+gorog), `kulso/lxx_bridge` (heb+gör) | 11 | 5 000 körül | **0** |
| `adat/karoli_strong/parok_*`, `szavak_*` | 38 fájl | ~700 000 | **0** |
| `konkordancia/Karoli_Strong_kivonat.tsv` | `Strong-szám` (383) | 383 | **0** (65 `+` lánc, mind érvényes tagokból) |

**N21 tárgytalan:** a brief 1. szakaszának feltevése igazolt (0 találat). Az `adat/` tehát nem tartalmaz `H922`-t; a `+` láncok elemei mind négyjegyűek. (A `konkordancia/` többi datasetje külső forrásalakot tart — 2. pont — ez nem hiba, ott a nyers forrás az irányadó.)

## 5. Döntések, amelyeket az M0 felvet (a felhasználó dönt)

a) **Előtag nélküli szám** (`1078`): a függvény hibát dob, vagy kapjon `nyelv=` paramétert? Javaslat: hiba alapesetben, `nyelv='H'|'G'` megadva elfogadja.
b) **Betűutótag** (`H2967a`, `G3924a`): a SEMA 1.2 nem ismeri. Javaslat: `strong_normalizal` utótagnál hibát dob; külön `strong_alap_utotaggal` helyett egy `utotag='megtart'|'tilt'` kapcsoló, alapérték `tilt`. A mai hívók (`lekerdez` lxx ág, SDBH) a megtartót használják.
c) **5 jegyű kód**: `G00120` (vezető nulla) → `G0120`; `G20447` (érvényes kiegészítő kód a Strong_szotarban) → javaslat: öt jegynél csak a vezető nulla hagyható el, egyébként hiba; a tW-féle „utolsó számjegy levágása” **nem** része a közös függvénynek (tW-specifikus, marad a `tw_import.py`-ban).
d) **`A####`**: javaslat: kivétel (nem H/G); az arámi→H leképezés a hívó dolga.
e) **Érvénytelen bemenet**: `strong_normalizal` kivételt dob (`ValueError`), `strong_ervenyes` bool.
f) **Viselkedésváltozás az M2-ben:** a `lekerdez.py scan H779` eddig 0 találatot adott; normalizálással `H0779`-re oldódik — ez **szándékos javulás, de eltér** a brief „viselkedésváltozás nincs” kitételétől. Javaslat: a bekötés a nyers `H779` bemenetet hibával utasítsa el (`A Strong-szám H0779 alakú legyen`), ne némán kijavítsa; így a kimenet változatlan marad az érvényes bemenetekre.

## 6. Következmény a briefre

A 3. pont (mérés) 0, ezért a javítás nem szükséges; a feladat az M1 szerint folytatható, ha a felhasználó elfogadja a 2. pont táblázatát és az 5. pont döntéseit.

## 7. Pontosítás (F62.5, az ellenőri jelentés alapján)

**Hatókör.** A 4. pont „0 eltérés” a **STRONG-típusú oszlopokra** áll (fejléc `strong`-ot tartalmaz): 11 oszlop az `adat/` nem-`karoli_strong` tábláiban (9 fájl: `bdb_igehely_javitas`, `elofordulasok`, `forditasok`, `grammatikai_strongok`, `kiejtes_heber_kivetelek`, `kulcsszavak`, `kulso/lxx_bridge` 2 oszloppal, `lexikon_hivatkozasok`, `lxx_dontesek` 2 oszloppal) + 38 `adat/karoli_strong/` fájl (1-1 oszlop) + a `Karoli_Strong_kivonat.tsv` 1 oszlopa = 50 oszlop, 48 fájl (9 + 38 + 1; a `strong_meres.py` kimenete: 50 oszlop, 48 fájl). A nem üres cellák 1 068 624 darabja: 1 060 305 a `karoli_strong/` fájlokban és 8 319 a többiben; a 4. pont „~700 000” a `karoli_strong/` fájlokra egy durva, első becslés volt, a mért szám 1 060 305. **Nem** a STRONG-típusú oszlopban álló, Strong-kódnak látszó, nem SEMA-alakú **forrásalakú érték 113** van: `adat/forditasok.tsv` `entry_id` 108, `adat/lexikon_hivatkozasok.tsv` `entry_id` 5 (a szótári forrás eredeti kulcsa, pl. nullázatlan `H430`). Ezek nem normalizálandók (a brief hatókörén kívül: forrásalakot hordozó mező), de a „0” állítás rájuk nem vonatkozik.

**Reprodukálható mérés:** `python eszkozok/strong_meres.py [--reszlet]` (csak olvas, tabra vágva (`split` tab-karakterrel), kódolási őr). Futás (2026-10-11):

```
(A) STRONG-típusú oszlop: 50 oszlop, 48 fájl; nem üres cella: 1068624; nem SEMA 1.2: 0
(B) forrásalakú, nem STRONG-típusú oszlopban álló, nem SEMA 1.2 alakú érték: 113
proveniencia: scope=adat/**/*.tsv+konkordancia/Karoli_Strong_kivonat.tsv | forras=eszkozok/strong_meres.py | a=0 | b=113 | ts=2026-10-11T08:05Z
```

**Az 5 jegyű alak (DT94, a 2. pont c) döntés módosítása):** a `G20447` (2 előfordulás) és `G20833` (1) a TAGNT érvényes G-kiegészítő kódja, nem csonkolandó és nem hiba: a SEMA 1.2 egysoros bővítést kap, a függvény G-nél változatlanul hagyja; H-nál az ötjegyű (nem nullával kezdődő) ValueError. A vezető nullás ötjegyű (`G00120`) továbbra is `G0120`.

**`domen`:** az egyszerű `H####`/`G####` argumentum szigorú (`domen H779` -> hiba a `H0779` alakkal); az `A####` és betűutótagos (`H0032a`) `strong_kod` a `domen` saját kódtere, kivétel.
