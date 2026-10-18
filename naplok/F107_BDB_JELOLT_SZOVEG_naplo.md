# F107 napló — a BDB jelölt szövegrétege

*Futtatta: claude-opus-5-5 · 2026.10.18 · ág: `claude/f107-bdb-jelolt-szoveg` · brief: `F107_BDB_JELOLT_SZOVEG_BRIEF.md` (v3)*

## 1. lépés — forrásválasztás és lefedettség (2. hatókör 1.)

Eszköz: `eszkozok/bdb_jelolt/forras_osszevetes.py` (csak olvas; a `DictBDB.json`-t a repón kívüli
munkakönyvtárból `python -I`-vel olvassa, a `BDB.lexicon`-t `mode=ro`-val, a TSV-t `split('\t')`-tel).
Az alábbi számok egyetlen futás kimenetéből valók:

`scope=F107 1. lépés, DictBDB.json ↔ BDB.lexicon ↔ BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_jelolt/forras_osszevetes.py --minta 300 --seed 107; DictBDB.json sha256 5d826c580a4dd06f54a53d1e19b5e8c354aab0180e200849e3148b89f370e33d | ts=2026-10-18T14:42:17Z`

### 1.1 A `DictBDB.json` letöltése

| | |
|---|---|
| URL | `https://raw.githubusercontent.com/eliranwong/unabridged-BDB-Hebrew-lexicon/master/DictBDB.json` (a `BDB_teljes_unabridged_README.md` URL-je) |
| a forrásrepó `master` HEAD-je | `6e8326c6884f8ef1399c7a365d660da9bb9e2d01` (2018-11-24; GitHub API, a letöltéssel egy időben) — ugyanaz, amelyet az `adat/licencek.tsv` `BDB` sora rögzít |
| SHA-256 | `5d826c580a4dd06f54a53d1e19b5e8c354aab0180e200849e3148b89f370e33d` |
| méret | 24 726 362 bájt; 8 091 elem (`DictInfo` + 8 090 `H…` kulcs), minden elem `{top, def}` |
| a forrásrepó `README.md`-je | SHA-256 `c52b20a9356089a3d041b806576066b5eacd40eeef6c7e993f7ad540136f9fb8` |
| hely | a repón kívül, a session scratchpadjének `dictbdb_letoltes/` könyvtára (új, üres könyvtár; a fájlból semmi nem futott) |
| ts | 2026-10-18T14:35:49Z |

`scope=DictBDB.json letöltés | forras=curl, raw.githubusercontent.com + api.github.com/repos/eliranwong/unabridged-BDB-Hebrew-lexicon/commits/master | ts=2026-10-18T14:35:49Z`

**Azonos-e a 2026-09-02-i letöltéssel?** A JSON hash-e 2026-09-02-án nem került naplóba (csak a belőle
készült TSV-é, K7: `1d28a840…dfa5`). A `_convert_bdb.py` (`142ad625`) eljárása a mai letöltésre
változatlanul alkalmazva (a `strip_html` és a kulcsképzés szó szerinti másolata, mert a fájl importja
futna) **bájtra a K7-es TSV-t adja** (LF-sorvéggel; sha256 `1d28a840…dfa5`, 8 090 sor). A mai letöltés
tehát tartalmában azonos azzal, amelyből a TSV készült.

A mai `BDB_teljes_unabridged.tsv` 8 099 sorából 7 843 bájtra azonos az újrakonvertált szöveggel; 9 sornak
nincs JSON-kulcsa (az F57 3 és az F72 6 pótolt sora, a README szerint a `BDB.lexicon`-ból); a maradék 247 sor
eltér. Az eltérő sorok egyenkénti okát ez a lépés nem vizsgálta; a README a ψ-javítást (F34) és az F46-os
javításokat rögzíti ilyen szövegváltozásként. *(Értelmezés, nem mérés: a 247 sor ezekkel a dokumentált
javításokkal magyarázható; igazolása a 3. lépés nézet-ellenőrzésének része.)*

### 1.2 Jelölők a két nyers forrásban

| | `DictBDB.json` (8 090 H-elem) | `BDB.lexicon` `BDB…` sorai (10 022) | `BDB.lexicon` `H…` sorai (8 619) |
|---|---|---|---|
| `class="point"` | 0 | 9 194 | 11 361 |
| `class="section"` | 0 | 376 | 539 |
| `class="remarks"` | 0 | 232 | 280 |
| `<p>` | 36 110 | 11 951 | 12 947 |
| `<b>` | 46 108 | 27 289 | 33 710 |
| `<sub>` | 739 | 739 | 971 |

`BDB.lexicon`: SHA-256 `c998a70b432fe1c2661f20657e6aed8b7aa708ea1197131cd00121e420002778`, 18 642 sor
(10 022 `BDB…`, 8 619 `H…`, 1 `info`); egyetlen `Lexicon(Topic, Definition)` tábla.

**Eltérés a brief kiinduló számától:** a brief (és a DT181) `point` 20 515, `section` 913, `remarks` 512
értéket ír; a `BDB…` + `H…` sorok összege itt `point` 20 555, `section` 915, `remarks` 512. A brief
számának hatóköre nincs rögzítve (`manual`); az eltérés okát ez a lépés nem vizsgálta.

**A tagolás a JSON-ban is megvan, más jelöléssel.** A JSON-ban nincs `point`/`section`/`remarks` osztály: a
tagolás bekezdés (`<p>`) + félkövér fej (`<b>1</b>`, `<b>a.</b>`, `<b>Qal</b>` …). Minta (H40): a
`BDB.lexicon` `<div class="point"><b>1.</b> …`, a JSON `<p><b>1</b> <b>king of Gerar</b> …`. A brief
„+? 1 Gerár királya” esete (H0040) a JSON-ban `… +?</p><p><b>1</b> …`: a bekezdéshatár és a félkövér a
nyers JSON-ban megvan, a TSV-ben nincs.

### 1.3 Hol áll a jelölő blokk elején? (a teljes közös halmaz: 8 089 Strong)

Szerkezeti félkövér fej = a `<b>` tartalma szám (`1`, `1.`), kisbetű (`a.`), római szám (`I.`–`X.`) vagy
igetörzs neve. „Blokk elején”: a JSON-ban közvetlenül `<p>` után, a lexikonban `<div class="point|section|remarks">`,
`<p>` vagy `<br>` után (köztes szóköz / `&emsp;` megengedett). A lexikon `H…` sora egy Strong alatt több
BDB-szócikket fűz egymás után (l. 1.4), ezért két változat:

| fej | JSON: fej / blokk elején | lexikon, teljes H-sor | lexikon, csak az első szócikk |
|---|---|---|---|
| szám | 7 542 / 7 095 (94,1%) | 8 543 / 7 936 (92,9%) | 7 143 / 6 716 (94,0%) |
| betű | 4 789 / 4 667 (97,5%) | 5 588 / 5 409 (96,8%) | 4 337 / 4 236 (97,7%) |
| római | 59 / 53 (89,8%) | 64 / 27 (42,2%) | 49 / 18 (36,7%) |
| igetörzs | 3 565 / 3 463 (97,1%) | 3 978 / 1 571 (39,5%) | 3 204 / 1 262 (39,4%) |

A számozott fejek darabszáma Strongonként azonos: 7 806 / 8 089 (teljes H-sor), 7 735 / 8 089 (első szócikk).

**Melyikben vesznek el a jelölők (M102/M117)?** Mért válasz: **egyik nyers forrásban sem** — a számozott és
betűs jelentéspont mindkettőben ~94–98%-ban blokk elején áll. Az igetörzs- és a római fej a JSON-ban
bekezdést nyit (97,1% / 89,8%), a lexikonban többnyire nem (39,4% / 36,7%). A lexikon többlete a `section` és
a `remarks` osztály (a JSON-ban ezeknek nincs saját jelölése) és a BDB-azonosító. **A jelölők a
`_convert_bdb.py`-ban vesztek el** (l. 1.6).

### 1.4 Lefedettség és Strong ↔ BDB-azonosító

- A TSV 8 099 Strong-sorából 8 095-nek van `H…` kulcsú sora a `BDB.lexicon`-ban, és mind a 8 095 Strong címkeként
  is áll legalább egy `BDB…` szócikk fejlécében; a `H…` sor szócikkei mind a 8 095 esetben pontosan a címke
  szerinti szócikkek (a `H…` sor tehát a címkézett `BDB…` szócikkek másolata).
- **Hiány (4):** `H747`, `H4123`, `H4725` — az F57 címke nélküli szócikkekből pótolt sorai (BDB754, BDB2246,
  BDB7372; `konkordancia/BDB_strong_potlas.tsv`), a lexikonban `BDB…` kulccsal megvannak, Strong-címke nélkül;
  `H1296` — a JSON-ban és a TSV-ben is csonk („H1296. Berekyah or Berekyahu”), a lexikonban sem `H1296` kulcs, sem
  címke nincs. *Üres eredmény: a H1296-nak a `BDB.lexicon`-ban nincs szócikke; nem pótolva.*
- Szócikk / Strong (a TSV Strongjaira): 1 szócikk 6 538, 2 szócikk 1 253, 3 szócikk 239, 4+ szócikk 65, 0 szócikk 4.
- Strong-címke / szócikk (mind a 10 022 `BDB…` sorra): 0 címke 846, 1 címke 7 972, 2 címke 1 017, 3+ címke 187.
- A lexikonban 524 olyan `H…` kulcs van, amelynek nincs TSV-sora (az alias-táblák köre, F57/F72).

A megfeleltetés tehát **csak a `BDB.lexicon`-ból** vezethető le: a JSON-ban nincs BDB-azonosító, egy Strong-eleme
több szócikket is összefűzhet (pl. H2436: BDB2635 + BDB2636 egy elemben), határjelölés nélkül.

### 1.5 Azonos átirat-e? (minta: 300 Strong, seed 107, a 8 089 közösből)

Mérőszám: a JSON latin szavainak (≥3 kisbetű; a héber, a könyvnevek és a számok kimaradnak; a lexikonban a
`<ref>` elemek is) hányada, amely a lexikon szövegében sorrendben megvan (`difflib`, `autojunk=False`).

| lexikon-oldal | ≥ 0,95 | 0,80–0,95 | < 0,80 |
|---|---|---|---|
| teljes H-sor | 193 | 80 | 27 |
| csak az első szócikk | 168 | 86 | 46 |

A legalacsonyabb értékek szócikk-határ eltérések, nem szövegeltérések (H381: a JSON-ban 2 szavas utaló, a
lexikonban a teljes célszócikk; H2436, H8210: a JSON-elem több szócikket fűz össze, mint a lexikon első
szócikke). Kézi minta (H40): a két szöveg azonos, a ψ-hiba is mindkettőben ugyanaz („king of Gath Psalm
Gen 34:1”). **Értelmezés:** ugyanaz az átirat (Tim Morton / Bible Analyzer); a lexikon hozzáadja a
hivatkozás-jelölést (`<ref …>`, más könyvrövidítéssel: `Ps`, `1Kgs`), a `checkingNeeded` (1 333) és
`wrongReferenceRemoved` (327) jelölőt a `BDB…` sorokban, és a BDB-szócikkhatárt. A forrásrepó README-je egy
BibleHub-adatokkal átnézett `.csv.zip` változatot is említ; azt ez a lépés nem töltötte le és nem mérte.

### 1.6 A `_convert_bdb.py` (`142ad625`, 2026.09.02) szerkezetvesztése — utólagos naplózás

A szkript `strip_html()`-je (a fenti mérés újrafuttatta, l. 1.1) a JSON 8 090 H-eleméből ezt dobja el:

| jelölő | JSON-ban | a TSV-ben |
|---|---|---|
| `<p>` bekezdéshatár (a jelentéspont, alpont, igetörzs blokkja) | 36 110 | szóköz (`<[^>]+>` → ` `), a határ nem ismerhető fel |
| `<b>` félkövér (a jelölő-fej és a glossza) | 46 108 | törölve; a „1”, „a.” sima szövegként marad |
| `<sub>` gyakoriságszám | 739 | `_N` (konverziós maradvány: a magyarban „N_M”) |
| `<sup>` felső index | 14 167 | `^…` |
| `<i>` dőlt | 51 525 | törölve |

A JSON a repóba nem került, csak a veszteséges TSV; a szerkezet ezért 2026.09.02 óta a repóban csak a
`BDB.lexicon`-ban (2026.09.07-i beemelés) volt meg. A README-be került szakasz: `konkordancia/BDB_teljes_unabridged_README.md`
„Szerkezetvesztés a konverzióban (utólagos naplózás, F107)”.

### 1.7 Javaslatok (⛔, `DONTESEK.md`)

- `DT-F107a` — melyik forrásból bont a tábla, és a licenc-státusz.
- `DT-F107d` — a playbook 2. pontjának kiegészítése (nyers forrás megőrzése; veszteséges konverzió naplózása).

A megállás után a 2. lépés csak a két döntés után indul.
