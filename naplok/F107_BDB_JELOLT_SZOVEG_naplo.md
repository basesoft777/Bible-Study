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

### 1.8 Döntés és alkalmazás (2026-10-18)

A felhasználó (chat, az orkesztrátoron át): „a #107 DT-F107a: (c) hibrid + (i) licenc + (x) a JSON a repóba;
DT-F107d: (a), a két szabály a playbook 2. pontjába, CI-kapu nélkül.”

- F107.5: a két `DONTESEK.md`-sor 🟢 (helyőrzővel).
- F107.6: `Rendszerfejlesztesi_playbook.md` 2. pont, a két szabály (CI-kapu nélkül).
- F107.7: `konkordancia/lexikonok_nyers/DictBDB.json` a repóban; a munkafa-fájl és a git-objektum SHA-256-ja is
  `5d826c58…e33d`; a git blob `9d6011ea9e3c61833be7a905d6d18e2363aaf37c` **azonos** az `adat/licencek.tsv`
  `BDB` sorában a 2026-09-02-i letöltésre rögzített blobbal (független megerősítése az 1.1 K7-reprodukciónak).
  A fájl LF-es; `core.autocrlf=true` mellett egy Windows-checkout CRLF-re írhatja a munkafában, ezért a hash
  a git-objektumra vonatkozik (a README-kben rögzítve). Repószintű méretkorlát vagy LFS-szabály nincs
  (`.gitattributes`: csak `*.tsv`, `.claude/agents/*.md`, `*.sh`; a CI méretkorlátja csak a `naplok/F06_*`-ra
  vonatkozik), ütközés nincs.

`scope=DictBDB.json a repóban | forras=sha256sum + git hash-object + git cat-file blob | ts=2026-10-18`

**Egyeztetett eltérés.** Az `adat/licencek.tsv` nem volt a brief `ir` mezőjében; a DT-F107a (i) alkalmazásához
a felhasználó döntése (2026-10-18, az orkesztrátoron át) alapján felvéve. Csak a `BDB` sor 3. mezője változott
(a JSON hash-e, blobja és helye), írás előtt soronkénti összevetéssel. **Nyitott javaslat (nem írva):** egy
`.gitattributes`-sor (`konkordancia/lexikonok_nyers/DictBDB.json -text`) a munkafa bájtazonosságát is
megőrizné; a `.gitattributes` nincs az `ir` mezőben.

## 2. lépés — szakasztábla és bontó (MEGÁLLT a STOP-feltételnél)

Eszköz: `eszkozok/bdb_jelolt/bont.py` (F107.8–F107.9). A tábla (`adat/bdb_szakaszok.tsv`), a SEMA-szakasz, a
`datasetek.tsv`-sor és a teszt **nem készült el**: a felhasználó STOP-feltétele (a Strongonkénti szócikk-illesztés a
Strongok >1%-ánál nem sikerül) teljesült, l. 2.3.

### 2.1 A bontás terve (a bont.py docstringje szerint)

- Egység: a JSON Strong-elemének egy bekezdése (`<p>`, `<p style="sub1">` (572 db, az alcímszó jelölője), vagy
  bekezdésen kívüli szövegdarab); a 0. a cím (`H40. Abimelek`). 8 090 Strong → 36 491 sor (a `--meres` szerint).
- Szöveg: a JSON-ból, a `_convert_bdb.py` tisztításával, egy eltéréssel: a `<sub>` a `gyakorisag` oszlopba kerül, nem
  `_N` lesz. A fej (szám, betű, római, igetörzs, nagybetű, zárójeles) a `jel` oszlopba kerül, a `szoveg` a fej utáni
  szöveg.
- `bdb_id`, szócikkhatár, `section`/`remarks`: a `BDB.lexicon`-ból, illesztéssel; a lexikon szöveget nem ad
  (DT-F107a (i)).
- **Útvonal (nem befagyasztott, DT190 🟡):** `<törzs>[.<nagybetű>]/<szám>/<betű>[/<zárójeles>]`, a hiányzó szint `-`,
  a törzsnév a szeletelő alakjában (`Pi'el`); a római fő tagolás külön `resz` oszlopban, az alcímszó sorszáma külön
  `alszocikk` oszlopban; `cim`, `fej` különleges értékek. Az alap a #99 aranymintájának és a `bdb_vers_jelentes.tsv`-nek
  a formátuma (SEMA 2.28–2.29), a #102 két bővítésével (nagybetűs csoport, zárójeles/görög szint) összehangolva.
  Kanonikus kulcsként **nincs befagyasztva**; a `strong`+`bdb_id`+`utvonal` egyedisége sem ellenőrzött (a
  jelöletlen bekezdések miatt nem is egyedi; a tényleges sorkulcs a `strong`+`sorszam`).

### 2.2 Lelet: a `DictBDB.json` héber szövegében nincs dagesses pe

| | `DictBDB.json` (minden héber szó kétszer: `ref0 entry=` + szöveg) | `BDB.lexicon` `BDB…` sorai | `BDB_teljes_unabridged.tsv` |
|---|---|---|---|
| mem + dagesh | 13 562 | 2 705 | 6 788 |
| pe + dagesh | **0** | 4 106 | 7 (az F57/F72 lexikonból pótolt soraiban) |
| pe dagesh nélkül | 12 988 | 6 506 | — |

`scope=F107 pe/mem karakterszám (NFD, a betűt követő pontozójelek között dagesh) | forras=scratchpad pe_mem.py + a TSV-re egy soros számlálás; DictBDB.json@5d826c58, BDB.lexicon@c998a70b | ts=2026-10-18`

A JSON fele (13 562 / 2 ≈ 6 781) egyezik a lexikon dagesses mem + dagesses pe összegével (2 705 + 4 106 = 6 811).
Példák az illesztésből (mássalhangzó-váz, ahogy az ujjlenyomat mutatta): H6620 JSON מתנ ↔ lexikon פתנ; H6499
מר ↔ פר; H6597 מתאמ ↔ פתאמ; H6574 מרשדנה ↔ פרשדנה.
**A dagesses pe a JSON-ban dagesses memként áll, és a TSV ezt örökölte**; a 674 kész magyar fordítás héber
idézetei a TSV-ből jönnek, ezért valószínűleg ugyanígy érintettek (ezt ez a lépés nem mérte). A repóban erről nincs
korábbi feljegyzés (`grep` „dages”: a DONTESEK.md-ben, a BDB-naplókban és a README-kben nincs találat). Javaslat:
`DT-F107f`.

### 2.3 A Strongonkénti szócikk-illesztés (STOP)

Sikerfeltétel, a mérés előtt rögzítve (a `bont.py` docstringje): (a) az első tartalmi bekezdés szócikk-kezdethez
illeszkedik, és (b) minden szegmens szavainak lefedése a hozzárendelt lexikon-szócikkel mindkét irányban ≥ 0,90.
A bontót a mérés közben elvi okokból javítottam (F107.9): NFD-normalizálás, sorrendfüggetlen kezdet-összevetés, a
cím-átírás folytatása, a számozott fejű bekezdés nem nyit szócikket, pe = mem az ujjlenyomatban (2.2), a római
homonimaszám nem token. Ezek a szöveget nem érintik. Két utólag bevezetett kategória: `csonk` (a JSON-elem a cím
folytatása, legfeljebb 8 token, pl. H381 „ish-chayil”, H358 „Elon Beth Chanan”) és `szocikk_resze` (a JSON-szegmens
≥ 0,90-re benne van a szócikkben, de a szócikk más Strongok alá eső részeket is tartalmaz). **A STOP a szigorú
feltétel szerint dől el.**

| futás | egyezik | reszleges | sikertelen | csonk | szocikk_resze | nem egyező |
|---|---|---|---|---|---|---|
| első (sorrendfüggő, NFD nélkül) | 4 405 | 2 490 | 1 195 | — | — | 45,55% |
| NFD + latin lefedés | 7 205 | 367 | 518 | — | — | 10,94% |
| + szimmetrikus, csonk, szocikk_resze | 7 546 | 252 | 224 | 44 | 24 | 6,72% |
| + címfolytatás, indexkorlát | 7 640 | 158 | 146 | 45 | 101 | 5,56% |
| **+ pe = mem, római token nélkül (F107.9)** | **7 869** | **139** | **16** | **35** | **31** | **2,73%** (csonk nélkül 2,30%; csonk és szocikk_resze nélkül 1,92%) |

`scope=F107 2. lépés, Strongonkénti illesztés, 8 090 JSON-Strong | forras=python eszkozok/bdb_jelolt/bont.py --meres (F107.9, 27ab3fb4) | ts=2026-10-18`

A maradék (F107.9):
- `reszleges` 139: a legrosszabb szegmens JSON-lefedése 0,8–0,9 sávban 71 (kis szövegeltérés: pl. H558 a JSON-ban a
  könyvnév kiírva („Kings”, „Chronicles”), a lexikonban `<ref>`-ben); 0,5–0,8 sávban 23; < 0,5 sávban 45 (hiányzó
  szócikkhatár: a JSON-szegmens egy további szócikket is tartalmaz, pl. H3: a BDB9264 arámi szócikket, mert a lexikonban
  a szócikk eleje előtt az arámi rész bevezetője áll); 20 Strongnak több szegmense van.
- `sikertelen` 16: H307 H390 H820 H890 H3216 H3222 H3823 H4330 H4538 H4548 H4866 H5351 H5446 H5654 …
- `csonk` 35, `szocikk_resze` 31.

**Nem kitöltve:** a nem egyező Strongok bekezdései a tervben `bdb_id` nélkül (üres, a kategória az `illesztes`
oszlopban) kerülnének a táblába; ezt a döntés előtt nem írtam ki. Javaslat: `DT-F107e`.

### 2.4 Ami nem készült el (a döntésig)

`adat/bdb_szakaszok.tsv`, a teszt (`eszkozok/bdb_jelolt/teszt_bont.py`), az `adat/SEMA.md` új szakasza, az
`adat/datasetek.tsv` sora; a 3–4. lépés. *(Elkészült a DT-F107e döntése után, l. 2.5.)*

### 2.5 A DT-F107e és DT-F107f alkalmazása (2026-10-18)

A felhasználó (chat, az orkesztrátoron át): „DT-F107e: (b), majd (a). DT-F107f: (a); a 674 kész fordítás héber idézeteinek
pe/mem-érintettségére most nyiss N-tételt.” (F107.12; N-F107a: F107.13.)

**(b) a 0,5 alatti sáv köre (F107.14).** A 45 Strong két mechanizmusa: (1) kettévágott szócikk-kezdet — a címszó egy rövid
blokkban, a szöveg a következő `sub1` blokkban (H108 „I. אוה” + „1Arabic …”, H176 „אוֺ , , ),” + „conjunction or”, H1055); a 4
tokennél rövidebb blokkot a következővel együtt mérjük; (2) elmaradt szócikkhatár a szigorúbb 0,85-ös küszöb miatt (H1817 → BDB1943);
a későbbi szócikk-kezdet küszöbe azonos az elsőével (0,80). A számozott fejű bekezdés továbbra sem nyit szócikket, és a
szegmenslefedés (≥ 0,90 mindkét irányban) őrzi a hamis határt.

| futás | egyezik | reszleges | sikertelen | csonk | szocikk_resze | nem egyező |
|---|---|---|---|---|---|---|
| F107.9 (a STOP) | 7 869 | 139 | 16 | 35 | 31 | 2,73% |
| **F107.14 (a 0,5 alatti kör)** | **7 920** | **94** | **15** | **35** | **26** | **2,10%** (csonk nélkül 1,67%) |

A `reszleges` 94 sávjai: 0,8–0,9: 75; 0,5–0,8: 8; < 0,5: 11 (45-ből). A küszöb (1%, szigorú) változatlan; a DT-F107e szerint a
tábla az (a) szerint kiíródik.

`scope=F107 2. lépés, Strongonkénti illesztés | forras=python eszkozok/bdb_jelolt/bont.py --meres (F107.14, 76f5b153) | ts=2026-10-18`

**(a) a tábla (F107.15).** `adat/bdb_szakaszok.tsv`: 36 491 sor, 8 090 Strong; `jelolo`: cim 8 090, fej 10 028, point 15 611,
bekezdes 2 194, alcimszo 308, section 254, remarks 6. A `reszleges` / `sikertelen` / `csonk` 144 Strong sorai `bdb_id` és
`section`/`remarks` nélkül, az `illesztes` oszlopban jelölve. Hiány: a TSV 9 JSON-kulcs nélküli sora (F57: H0747, H4123, H4725;
F72: H1753, H3367, H3848, H6433, H7560, H8065) nincs a táblában (a szövegük a lexikonból jött; DT-F107a (i)). Teszt:
`eszkozok/bdb_jelolt/teszt_bont.py`, 24 teszt, OK (benne a két `--ellenoriz` bájtos determinizmus). SEMA 2.30–2.31, `datasetek.tsv`
`BDB_szakaszok` (F107.17).

**Megfigyelés a 4. lépéshez (H7626):** a „145:” a nyers JSON-ban a szövegben áll (`<b>2</b> 145:tribe`), tehát nem konverziós
maradvány; ugyanitt a szócikk-fej összefoglalója („1 rod … 2 tribe”) félkövér pontokként jelenik meg, a „1.a.” fej nem félkövér, ezért az
útvonal elcsúszik (`-/2/b` a `-/1/b` helyett). *(Értelmezés, nem mérés: a „145” a „tribe” jelentés gyakoriságszáma lehet `<sub>` nélkül.)*

**DT-F107f (a), a javítótábla (F107.16).** `adat/bdb_forras_javitas.tsv`: 6 781 sor (a tábla szövegének minden dagesses memje);
`javitva` 3 823 (1 428 Strong), `valodi_mem` 2 402, `jelolt_marad` 556 (ebből 112 `bdb_id` nélküli sorban, 444 ahol egyik alak
sincs a szócikkben). Szúrópróba: מִשְׁמַּט → מִשְׁפַּט (H2835), יִמֹּל → יִפֹּל (H5307), אַמִּי → אַפִּי (H7626); `valodi_mem`: לָרִמָּה, קִמּוֺשׁ.
A tábla szövege a nyers JSON-é; a javított nézet a DT-F107c-é (SEMA 2.30, javaslatként jelölve).

`scope=F107 5. lépés, pe/mem | forras=python eszkozok/bdb_jelolt/forras_javit.py --ts 2026-10-18 | ts=2026-10-18`

**A `.gitattributes` javaslata (nem írva, nincs az `ir` mezőben):** `konkordancia/lexikonok_nyers/DictBDB.json -text`, hogy a
munkafa is bájtra a hash-elt alakot tartsa (l. 1.8).

## 3. lépés — nézet-ellenőrzés

Eszköz: `eszkozok/bdb_jelolt/nezet_ellenoriz.py` (csak olvas). A nézet Strongonként: a tábla sorainak `jel` + `szoveg` mezője egy
szóközzel összefűzve, whitespace-normalizálva; a javítótábla javításai nem alkalmazódnak. Összevetés a `BDB_teljes_unabridged.tsv`-vel
és a JSON újrakonvertált alakjával.

| osztály | Strong | ok |
|---|---|---|
| `azonos` | 7 097 | — |
| `sub` | 444 | csak a `<sub>` (a TSV `_N`-je; a táblában a `gyakorisag` oszlop): `szoveg_konverzio` |
| `tsv_utolagos` | 206 | a TSV utólag javított sora (F34 ψ, F46 könyvfeloldás), a nézet a nyers JSON-t adja: pl. H0040 TSV „Psa 34:1” ↔ JSON „Gen 34:1”; H0026 „1Sam 25:18” ↔ „2Sam 25:18” |
| `tsv_utolagos+szokoz` | 41 | mint fent, és szóköz-eltérés is |
| `szokoz` | 297 | csak szóköz: a táblában a fej és a szöveg közötti forrás-szóköz nincs rögzítve (tapadt fej: „a.-1”, „Pi`el3masculine”, „1Arabic”; vagy hamis fej a bekezdéshatár után: „below 3);” → `3 )`) |
| `forras_html` | 5 | a JSON hibás HTML-je (töredékes `<a href=…>`, `<e …>` tag, benne `<p>`): a bekezdés-bontás nyers jelölést enged a szövegbe (H1980, H3117, H4639, H4714, H8104; 6 sor) |
| `nincs_a_tablaban` | 9 | a TSV F57/F72 sorai (JSON-kulcs nélkül) |
| `egyeb` (ismeretlen ok) | **0** | — |

A `tsv_utolagos` összesen 247 = az 1.1-ben mért 247 eltérő TSV-sor. **Következmény a 6. lépéshez (DT-F107c):** ha a sima szöveg a
táblából generált nézet lenne, a 247 utólag javított sor javításai elvesznének, hacsak a javítótábla nem veszi át őket (F34, F46).

`scope=F107 3. lépés, nézet ↔ BDB_teljes_unabridged.tsv (8 099 sor) | forras=python eszkozok/bdb_jelolt/nezet_ellenoriz.py | ts=2026-10-18`
