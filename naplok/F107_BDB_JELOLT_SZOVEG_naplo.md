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

## 4. lépés — ellenőrzés (MEGÁLLT a ⛔ osztályozási pontnál)

Eszköz: `eszkozok/bdb_jelolt/szerkezet_osszevet.py` (csak olvas). Útvonal-normalizálás az összevetéshez: a nagybetűs csoport és a
zárójeles szint elhagyva, a záró `-` szintek levágva; a szeletelő `tagolatlan`-ja és a tábla `cim`/`fej`-e = `fej`; a kombinált fej
(„1. a.”) a jelentés és az alpont csomópontját is megnyitja; az aranyminta `-/a` alakja (SEMA 2.28: jelentés nélküli alpont) = a tábla
`-/-/a`-ja. A tábla nem változott.

### 4.1 Aranyminta (`adat/bdb_aranyminta.tsv`, 32 szócikk)

A `torzs` / `jelentes` / `alpont` csomópontok (425; a `csoport` 184 és a `szakasz` 16 szintet a tábla nem bontja, a csoport a #103-é):
**egyezik 328 (77,2%)**; a 2 számozatlan jelentés nélkül 328 / 423 (77,5%). **A javasolt mérce (≥ 99%) nem teljesül.**

| Strong | hiányzó csomópont | ok (megnézve) | javasolt osztály |
|---|---|---|---|
| H6440 | 44 | a fej utáni „I.”, „II.” homonima-szakasz a táblában `resz` lett (a 2.28 `szakasz`-a); egy fej „7. 2. a.” (a „7.” a megelőző szöveg vége) | `tabla_hiba` (szakasz-római ↔ fő tagolás) + `forras_hiba` („7.”) |
| H7121 | 27 | a JSON a „(compare Pu`al)” közepén bekezdést tör; az új bekezdés elején álló félkövér „Pu`al” törzsfejnek számít, a Qal hátralevő része a Pu'al alá kerül | `tabla_hiba` (hamis fej: a fej után „)”, „,”, „;”) |
| H3615 | 7 | hamis „2” fej a ragozási sorban („2 ); masculine plural …”) | `tabla_hiba` (mint fent) |
| H0559 | 5 | a „Qal” név hiányzik, az „1” sima szöveg („263</sup>.1<i>Say</i>”, a nyers JSON-ban igazolva) | `forras_hiba` |
| H0834 | 5 | a héber alcímszavas szakaszok (בַּאֲשֶׁר, מֵאֲשֶׁר, שֶׁ) alpontjai | nem vizsgált |
| H4900, H1242, H0430 | 2 + 2 + 2 | — | nem vizsgált |
| H3176 | 2 | számozatlan jelentés (`Hiph'il/-1`, `-2`): jelölő nélkül a táblában nem bontható | `tabla_hiba` (korlát) |
| H2939 | 1 | `Pa'el` törzs | nem vizsgált |

### 4.2 Seed-101 (a #99 13 szeletelő-hibájának helye)

**7 / 13 egyezik** (M028, M031, M043, M146, M203, M236, M238 — a #102 1b. „igen” eseteiből 7; köztük a gyakoriságszámos jelölő, a
törzsfejléc „Hiph`il A./B.”, a fő tagolás „II.” és a jelöletlen alcímszó).

| hely | tábla | várt | ok | javasolt osztály |
|---|---|---|---|---|
| M102 H0559 | `fej` | `Qal/1` | az „1” sima szöveg a JSON-ban, a „Qal” név hiányzik (igazolva) | `forras_hiba` |
| M117 H0539 | `Qal/3` | `Niph'al/4` | nem vizsgált (a #102 1b. szerint „1.carried” szóköz nélkül) | nem vizsgált |
| M130 H8478 | (a horgony átnyúlik a bekezdéshatáron) | `II -/2/a` | a Hab 3:16 a 8. sorban, `II -/-/-`; az „1” nem félkövér | `forras_hiba` (az „1”) — nem igazolt |
| M140 H7626 | `-/2` | `-/1/a` | a fej összefoglalója („1 rod … 2 tribe”) félkövér pontokként jelenik meg, a „1.a.” fej nem félkövér | `tabla_hiba` + `forras_hiba` |
| M162 H3318 | `-/1/a` | `Qal/1/a` | a „Qal” név a forrásban hiányzik (a #102 1b. szerint mindkét formázásban) | `forras_hiba` |
| M243 H1129 | `Qal/-/i` | `Qal/1/i` | „— <i>build</i>, <b>1</b> (literal) </p><p><b>a.</b>”: a félkövér „1” a bekezdés közepén áll (igazolva) | `tabla_hiba` (bekezdésen belüli fej) |

### 4.3 Korpusz: a tábla ↔ a mai szeletelő (`adat/bdb_vers_jelentes.tsv`)

A szeletelő minden nem szűrt hivatkozása (a `nyers` alak a tábla szövegében, Strongonként sorrendben keresve): **159 804, ebből
egyezik 131 126 (82,1%)**.

| osztály | darab | minta |
|---|---|---|
| `egyezik` | 131 126 | — |
| `jelentes_elter` | 9 900 | H0068 1Chr 29:2: szeletelő `-/2`, tábla `-/3` (a „below 3 )” hamis fej, l. 3.) |
| `torzs_elter` | 8 131 | H0502 Job 15:5: szeletelő `Qal`, tábla `Pi'el`; H0539 Prov 11:13: szeletelő `Niph'al`, tábla `Qal/4/b` |
| `szeletelo_fej_tabla_tagolt` | 2 903 | H0053 1Kin 15:2: szeletelő `tagolatlan`, tábla `-/1` (a tábla jelölőt lát, a szeletelő nem) |
| `alpont_elter` | 2 372 | H0157 Deut 10:18: szeletelő `Qal`, tábla `Qal/-/n` |
| `csak_resz` | 1 948 | H0905 Job 18:13: azonos út, a tábla `resz` III |
| `nem_talalt` | 1 769 | a hivatkozás a TSV-ben utólag javított (F34/F46, l. 3.), a nyers JSON-ban más: H0040 „Psa 34:1” ↔ „Gen 34:1” |
| `tabla_fej_szeletelo_tagolt` | 1 655 | H0058 1Sam 6:18: szeletelő `-/1`, tábla `fej` |

(Kihagyva: 528 szűrt sor, 284 sor a tábla nélküli 9 Strongon.) A korpusz-eltérések soronkénti osztályozása (`tabla_hiba` /
`szeletelo_hiba` / `forras_hiba` / `szoveg_konverzio`) nincs elvégezve; a lista az eszközzel újragenerálható
(`--korpusz --lista N`).

`scope=F107 4. lépés: aranyminta (425 csomópont), seed-101 (13), korpusz (159 804 hivatkozás) | forras=python eszkozok/bdb_jelolt/szerkezet_osszevet.py --arany --seed101 --korpusz | ts=2026-10-18`

### 4.4 A megállás oka és a javaslat

A ⛔ pont a brief szerint az eltérés-lista osztályozásának jóváhagyása. A mérés szerint a tábla három **szabályszerű** `tabla_hiba`-
osztályt hordoz, amelyek a nyers jelölőből javíthatók: (1) **hamis fej** a JSON bekezdéstörése után (a fejet közvetlenül „)”, „,”, „;”
követi: H7121, H3615, H0068); (2) a **fej utáni homonima-római** (`I.`, `II.`) `resz` helyett szakasz (H6440); (3) a **bekezdés
közepén álló félkövér fej** (M243). A `forras_hiba`-osztály (hiányzó „Qal” név, nem félkövér „1”, „7. 2. a.”) a forrás jelölőjéből nem
javítható, csak a javítótáblával (5. lépés). Javaslat: `DT-F107g` (`DONTESEK.md`).

### 4.5 A DT-F107g alkalmazása: a három `tabla_hiba`-osztály (F107.22)

A felhasználó (chat, az orkesztrátoron át, 2026-10-18): „DT-F107g (a)+(b) — a három tabla_hiba osztály szabályos javítása,
újramérés; a forras_hiba csomópontok külön számolva, de mindegyik a nyers forrásban igazolva, tételesen, kézi sorral a
javítótáblába; a jelentés mindkét számot mutassa.”

1. **Hamis fej a JSON bekezdéstörése után** (`fej_valodi`): a fejet közvetlenül „)”, „,”, „;”, „]” követi → a félkövér hivatkozás, nem
   fej (a blokk `bekezdes`, a szám a szövegben marad). H7121 „(compare <b>Pu`al</b>); with name”, H3615 „2 );”, H0068 „below 3 );”.
2. **Homonima-szakasz** (új `szakasz` oszlop): ha a szócikk első római feje „I.”, és előtte nem volt szám-, betű- vagy törzsfej, a
   római fejek homonima-szakaszok (`szakasz`), nem `resz`; különben fő tagolás (`resz`; H3068 M203, H8478 M130 változatlan). H6440.
3. **Bekezdésen belüli félkövér fej** (`kozepfej_bont`): a 697 bekezdés közepi, csupa fej-tokenből álló félkövérből 126 felel meg (előtte
   „.”, „—”, „:”, „;”, „,”; utána nem „)”, „,”, „;”, „.”, „]”; törzsnév után nem szám — „compare Qal 42:10, Pi`el 38:7”); a többi 571 főleg
   hivatkozás („(see 2)”, „(= Qal 4)”). Mintavétel (25 elfogadott, seed 7): 24 valódi fej, 1 hivatkozás („[Pi`el] 38:7”), ezért került be a
   törzsnév-utáni-szám kizárás. A **bekezdés végi** fej (utána semmi) akkor valódi, ha a következő blokk fejjel nyit (H3615 „— <b>1</b>
   </p><p><b>a.</b>”; a `BDB.lexicon` ugyanitt „<b>1.</b> <br> <b>a.</b>”).
4. **A tokenizáló hibája (a jóváhagyott három osztályon kívül, jelzem):** a szóköz nélküli kombinált fejet („<b>1.a.</b>”, H7626 — mindkét
   forrásban félkövér bekezdésfej) a tokenizáló nem bontotta; javítva, két token.

Teszt: `teszt_bont.py` 31 teszt (az 1–4. mindegyikére egység- és táblateszt), OK. A tábla `--ellenoriz`-zel bájtra determinisztikus.

**Változás a régi (F107.15) táblához képest:** 36 491 → 36 621 sor (Δ +130); 366 érintett Strong: csak útvonal 239; sorszám + útvonal +
`resz` + illesztés 90 (a blokk-kettéválás miatt); útvonal + `resz` 16; egyéb mező (szöveg/jel) 15; útvonal + illesztés 6. A `szakasz`
oszlop 345 sorban (18 Strong) kitöltött. Az illesztés: `egyezik` 7 916 (7 920), `szocikk_resze` 30 (26), a többi változatlan
(nem egyező 2,15%). A 3. lépés nézet-ellenőrzése újrafuttatva: `azonos` 7 237 (7 097), `sub` 506, `tsv_utolagos` 237 + 10, `szokoz` 95
(297), `forras_html` 5, `nincs_a_tablaban` 9, ismeretlen okú 0.

`scope=F107 4.5, régi ↔ új tábla és nézet | forras=tabla_diff (scratchpad), python eszkozok/bdb_jelolt/nezet_ellenoriz.py | ts=2026-10-18`

### 4.6 A `forras_hiba` csomópontok — igazolás a nyers forrásban (DictBDB.json ÉS BDB.lexicon)

Minden tétel a két nyers fájl idézett részletével igazolva (az idézet rövidített; a JSON a `<ref0>`/`<font>`/`<a>` burok nélkül); mindegyiknek
kézi sora van az `adat/bdb_forras_javitas.tsv`-ben (`allapot=kezi`, `manual`; `forras_javit.py` `KEZI`).

| # | Strong | csomópont (érintett) | hiba | DictBDB.json | BDB.lexicon |
|---|---|---|---|---|---|
| 1 | H0559 | `Qal` (+ `Qal/2–4`; arany 4, seed M102) | `jelolo_hianyzik`: a „Qal” sima szöveg | „— Qal <i>Perfect</i> ׳א Gen 3:1” | „— Qal Perfect ׳א Gen 3:1” (nincs `<b>`) |
| 2 | H0559 | `Qal/1` (arany 1, seed M102) | `jelolo_hianyzik` a JSON-ban: az „1” a lapszám után | „April, 1887, 263</sup>.1<i>Say</i>” | „263</sup>.</p><div class="section"><p>1. Say” (a lexikon jelöl) |
| 3 | H0539 | `Niph'al` (seed M117) | `jelolo_hianyzik`: a „Niph`al” sima szöveg | „see אֵמֻן. Niph`al נֶאֱמַן Prov 11:13” | ugyanígy, `<b>` nélkül |
| 4 | H0539 | `Niph'al/1` (seed M117) | `jelolo_hianyzik`: az „1.” jelöletlen | „Deut 28:59. 1.<i>carried</i>” | „Deut 28:59. 1. carried by a nurse” (a 2. már `<div class="point"><b>2.</b>`) |
| 5 | H3318 | `Qal/1` (seed M162) | `jelolo_hianyzik`: a „Qal” név az első törzs előtt hiányzik | „&#8212; </p><p><b>1</b> <i>go</i> or <i>come out</i>” | „— <div class="point"><b>1.</b> go or come out” |
| 6 | H4900 | `Qal/6`, `Qal/7` (arany 2) | `hamis_jelolo`: a „compare Niph`al” törzsneve a 6. fejbe olvadt | „compare </p><p><b>Niph`al 6.</b> <i>trail</i> seed” | „compare </div><div class="point"><b>Niph`al 6.</b> trail seed” |
| 7 | H1242 | `-/1/g`, `-/1/h` (arany 2) | `hamis_jelolo`: téves „2.” a g. alpont fejében (a 2. jelentés később: „morrow, next day”) | „<b>d.</b> above, &amp; below </p><p><b>2. g.</b>” | „<b>d.</b> above, &amp; below </div><div class="point"><b>2. g.</b>” |

**7 tétel; aranyminta-csomópont 9 (H0559 5, H4900 2, H1242 2), seed-101 hely 3 (M102, M117, M162).**

**Átsorolva (nem igazolható forráshibaként, jelzem):**
- H2939 `Pa'el` (arany 1): mindkét forrásban „<b>verb Pa`el</b>” — a törzsnév a fejsor félkövér szófaj-elemében áll; ez a forrás szokása,
  nem hibája → `tabla_hiba` (korlát: fejsorbeli törzsnév).
- H0834 `-/a` (arany 2): a lexikonban „<b>4.</b> compounds: <br> <b>a.</b> בְּשֶּׁ, i. q. בַּאֲשֶׁר” — a forrás alpontként tagol, az aranyminta
  az összetett alakot szakasznak veszi → értelmezési eltérés, nem forráshiba.
- M130 (H8478): a Hab 3:16 első előfordulása a „II.” bevezetőjében áll (mindkét forrásban), a seed-101 várt helye (`II -/2/a`) a
  forrásból nem azonosítható egyértelműen → helyazonosítás, nem forráshiba.
- H6440 (arany 17): l. 4.7 — `tabla_hiba`, a lexikon igazolja.

### 4.7 Újramérés (F107.23) — mindkét mérce

| mérce | teljes | a `forras_hiba` csomópontok / helyek nélkül |
|---|---|---|
| aranyminta (425 törzs/jelentés/alpont) | **394 / 425 (92,7%)** (F107.19: 77,2%) | **394 / 416 (94,7%)** |
| seed-101 (13 hely) | **9 / 13** (F107.19: 7) | **9 / 10** |
| korpusz a mai szeletelővel (159 804) | **134 150 (83,9%)** (F107.19: 82,1%) | — (a korpuszon a forráshiba soronként nincs osztályozva) |

`scope=F107 4.7 | forras=python eszkozok/bdb_jelolt/szerkezet_osszevet.py --arany --seed101 --korpusz (F107.23, 59937a3f) | ts=2026-10-18`

**A mérce (a `forras_hiba` nélkül ≥ 99% az aranymintán) nem teljesül: 94,7%.** A maradék 22 hiányzó, nem forráshibás csomópont:

| Strong | csomópont | ok | osztály |
|---|---|---|---|
| H6440 | 17 (`II` szakasz `-/4/a` … `-/8/b`) | a JSON a mondat közepén tör bekezdést: „(God, with יראה pointed as </p><p><b>Niph`al</b>, see …” és „originally </p><p><b>Qal</b>, afterwards pointed as </p><p><b>Niph`al</b> to avoid …”; a `BDB.lexicon`-ban ugyanez a szövegen belül, `<b>` bekezdés nélkül („pointed as <b>Niph`al</b> to avoid”). A második „Niph`al” után szöveg áll, ezért az (1) szabály nem fogja; a szakasz többi része a hamis Niph'al alá kerül | `tabla_hiba` (hamis fej mondatközi bekezdéstörés után) |
| H3176 | 2 (`Hiph'il/-1`, `-2`) | számozatlan jelentés: jelölő nélkül nem bontható | `tabla_hiba` (korlát) |
| H0834 | 2 | l. 4.6 | értelmezési eltérés |
| H2939 | 1 (`Pa'el`) | l. 4.6 | `tabla_hiba` (korlát: fejsorbeli törzsnév) |

**Becslés (számítás a fenti számokból, nem mérés):** ha a H6440 17 csomópontja helyreállna, 411 / 416 (98,8%) lenne; a H2939-cel 412 /
416 (99,0%). A hamis fej megkülönböztetéséhez a JSON-ból a megelőző blokk végződése nem elég (a betűre végződő előzmény utáni 366 törzsfej
többsége valódi, pl. „— only || Qal Perfect”); a `BDB.lexicon` szerkezeti metaadata (ott a fej nyit-e blokkot) igen. Javaslat: `DT-F107h`.

### 4.8 A DT-F107h alkalmazása: a negyedik `tabla_hiba`-szabály (F107.29)

A felhasználó (chat, az orkesztrátoron át, 2026-10-18): „#107: a DT-F107h, a szakasztábla negyedik szabálya.” — az (a) változat, a
jóváhagyott feltétellel: a korpusz (83,9%) és a seed-101 (9 / 13, 9 / 10) nem romolhat; ha romlik, megállás.

**Első változat (elvetve):** a JSON blokk eleji feje hivatkozás, ha a `BDB.lexicon` ugyanazon szócikkében ugyanez a fej (ugyanazzal a
követő szöveggel) a szövegen belül áll. Mérés: aranyminta 350 / 425 (82,4%), seed-101 **8 / 13**, korpusz **78,4%** — **romlott** (a
törzs-csomópont 48 → 19): a lexikon a valódi törzsfejeket is gyakran a szövegen belül írja („— <b>Qal</b> Perfect”). A feltétel szerint
ez nem maradhatott; a tábla nem került commitba ebben az állapotban.

**A szabály (szűkítve, commitolva):** hivatkozás, ha a lexikonban a fej a szövegen belül áll, **és** közvetlenül előtte hivatkozó szó áll
(`as`, `see`, `compare`, `cf`, `read`, `like`, `than`, `under`, `also`; H6440 „pointed as <b>Niph`al</b>”); holtversenyben (azonos
hasonlóság) a blokkot nyitó előfordulás nyer (H0430 „3”: a holtverseny nélkül a valódi fej is hivatkozássá vált); ha a lexikonban nincs
megfelelő hely (a követő szöveg kezdete < 0,6 hasonló), a fej marad. A lexikon csak szerkezeti metaadat, a szöveg a JSON-é. **Fejsorbeli
törzsnév:** a fej-bekezdés `<b>verb <törzs></b>` eleme a szócikk törzsállapota a fej után (H2939 — ott a fejsoron kívül nincs több sor,
így a mérésben nem hat; a szabály a többsoros szócikkekben érvényesül).

Teszt: `teszt_bont.py` 33 (új: a lexikon-szabály egységtesztje — a hivatkozó szó utáni, a blokkot nyitó és a szövegen belüli, de nem
hivatkozó szó utáni eset —, és a H6440/H0430 táblateszt), OK; `--ellenoriz` bájtra azonos.

**Változás az F107.22-es táblához képest:** 36 621 sor (Δ 0); 95 érintett Strong (útvonal 90, egyéb mező 3, `resz` 1, útvonal + `resz` 1);
`jelolo`: point 15 410 → 15 337, bekezdes 2 517 → 2 589. A nézet-ellenőrzés: `azonos` 7 239, `sub` 507, `tsv_utolagos` 237 + 10, `szokoz`
92, `forras_html` 5, `nincs_a_tablaban` 9, ismeretlen okú 0.

| mérce | F107.19 | F107.23 (DT-F107g) | **F107.29 (DT-F107h)** |
|---|---|---|---|
| aranyminta, teljes | 328 / 425 (77,2%) | 394 / 425 (92,7%) | **411 / 425 (96,7%)** |
| aranyminta, a `forras_hiba` nélkül | — | 394 / 416 (94,7%) | **411 / 416 (98,8%)** |
| seed-101, teljes | 7 / 13 | 9 / 13 | **9 / 13** (nem romlott) |
| seed-101, a `forras_hiba` nélkül | — | 9 / 10 | **9 / 10** (nem romlott) |
| korpusz a mai szeletelővel | 82,1% | 83,9% | **136 538 / 159 804 (85,4%)** (nem romlott) |

`scope=F107 4.8 | forras=python eszkozok/bdb_jelolt/szerkezet_osszevet.py --arany --seed101 --korpusz (F107.29, 5aba58c9); nezet_ellenoriz.py | ts=2026-10-18`

**A maradék 5 nem forráshibás aranyminta-csomópont:** H3176 2 (számozatlan jelentés, korlát), H0834 2 (értelmezési eltérés), H2939 1
(fejsorbeli törzsnév, a szócikknek nincs további sora). **A ≥ 99%-os mérce (a `forras_hiba` nélkül) egy csomóponttal nem teljesül:
98,8%.** A felhasználó feltétele (korpusz, seed-101 nem romlik) teljesül; az orkesztrátor utasítása szerint a munka az 5–6. lépéssel
folytatódik, a 98,8% itt jelezve.

## 5. lépés — a forráshibák javítótáblája (állapot és a 247 utólag javított TSV-sor felmérése)

`adat/bdb_forras_javitas.tsv` (F107.29): 6 788 sor — `pe_mem` 6 781 (`javitva` 3 823 / 1 428 Strong, `valodi_mem` 2 402, `jelolt_marad`
556) + `kezi` 7 (a 4.6 tételei). A H7626 „145:” nem kapott sort (a nyers JSON-ban és a lexikonban is a szövegben áll, nincs eldöntve, hogy
hiba-e; *értelmezés:* gyakoriságszám lehet `<sub>` nélkül).

**A 247 `tsv_utolagos` Strong (mérés, döntés nélkül):** a `BDB_teljes_unabridged.tsv` ezeken a sorokon a nyers JSON-tól 412 szakaszban tér
el (szóközre bontott tokenek, `difflib`):

| osztály | szakasz | minta |
|---|---|---|
| könyvnév-csere `→ Psa` (F34, ψ) | 165 | H0040 «Gen» → «Psa»; H0430 «Job» → «Psa» |
| könyvnév-csere, egyéb (F46) | 141 | H0026 «2Sam» → «1Sam»; H0056 «1Sam» → «Isa» |
| kiírt könyvnév + szám (F46) | 92 | H0088 «Numbers 34:43;» → «Num 33:43;»; H0205 «Isaiah 55:17;» → «Isa 55:7;» |
| szám-csere (F46) | 14 | H0995 «28:33» → «28:23» |

Mind a 412 hivatkozás-javítás (könyv vagy fejezet:vers), a dokumentált F34/F46 javításokkal egyező jellegű. A táblából generált nézetbe
ezek csak akkor kerülnek át, ha a javítótábla egy új hibaosztályként (pl. `hivatkozas`, forrás: `naplok/F34_M2_csere.tsv`,
`naplok/F46_*`) átveszi őket — ez a DT-F107c része.

`scope=F107 5. lépés, tsv_utolagos | forras=python eszkozok/bdb_jelolt/nezet_hatas.py --utolagos | ts=2026-10-18`

## 6. lépés — a nézet-döntés mérései (⛔ DT-F107c)

Eszköz: `eszkozok/bdb_jelolt/nezet_hatas.py` (csak olvas).

**(1) A 3. lépés eltérés-listája (F107.29):** `azonos` 7 239, `sub` 507, `tsv_utolagos` 237 (+10 szóközzel), `szokoz` 92, `forras_html` 5,
`nincs_a_tablaban` 9 (F57/F72), ismeretlen okú 0.

**(2) A kész fordítások `forras_hash`-e** (`adat/forditasok.tsv` BDB-sorai; a `forras_hash` a TSV `Teljes_szocikk` SHA-1-e, `eszkozok/emeles.py`
`forras_hash`, `eszkozok/fordit.py`): 678 sor, 674 Strong; ma 674 egyezik, 4 már elavult.

| nézet | a `forras_hash` változna | változatlan |
|---|---|---|
| V1: a tábla nyers nézete (`jel` + `szoveg`, a `<sub>` nélkül) | 446 sor | 232 |
| V2: V1 + a pe/mem `javitva` javítás | 546 sor | 132 |

A fordítássorok közül 93 a 247 `tsv_utolagos` Strongé (ezeknél a V1/V2 a TSV hivatkozás-javítását is visszavonná, ha a javítótábla nem
veszi át). A V1 változásának nagy része technikai (a `_N` gyakoriságszám és a fej utáni szóköz), nem tartalmi.

**(3) A TSV olvasói:** `adat/datasetek.tsv` 4 sor fájlként (`BDB`, `mindig`, mind a négy study-típus) + 4 sor a megjegyzésben
(`OSHL_BDB_igehelyek`, ellenőrző szerep); 16 brief `olvas` mezője (F102, F103, F105, F106, F107, F28, F34, F38, F46, F56, F57, F60, F66, F72,
F73, F99); 29 Python-fájl az `eszkozok/` alatt (köztük `lexikon_general.py`, `sqlite_epit.py`, `olvaso_szerver/bdb_vers_jelentes.py`,
`emeles.py`, `bdb_adatblokk.py`, `ellenoriz.py` — a `lexikon_general.py` és az `olvaso_szerver/` ennek a feladatnak tiltott fájlja).

`scope=F107 6. lépés | forras=python eszkozok/bdb_jelolt/nezet_hatas.py --utolagos --forditas --olvasok | ts=2026-10-18`

**(4) A csere helye:** a fenti olvasók (köztük két, ennek a feladatnak tiltott fájl) és a 446–546 elavuló fordítás miatt a csere nem
fér el ebben a feladatban tiltott-fájl-érintés nélkül. Javaslat: `DT-F107c` (`DONTESEK.md`).

### 6.1 A DT-F107c alkalmazása: a nézet-generátor és a 247 sor hivatkozás-javítása (F107.33)

A felhasználó (chat, 2026-10-18): „DT-F107c: (d) — ebben a feladatban csak a nézet-generátor és a 247 sor F34/F46-javításának átvétele
a javítótáblába; a TSV cseréje és az olvasók átállása külön, /befogad-dal felvett feladat; a 674 fordítás forras_hash-e addig a
változatlan TSV-hez kötődik. Folytasd a 7. lépéssel.”

**A javítótábla `hivatkozas` osztálya** (`forras_javit.py`): a TSV és a nyers JSON (a `_convert_bdb.py` szerint) szóköz szerinti tokenjeinek
eltérő szakaszai — 412 sor, mind `javitva`, mind megtalálta a helyét a táblában. A forrásjavítás azonosítása az **új** hivatkozás kulcsával
(Strong, a könyvnév első 3 betűje, fejezet:vers; csak fejezet:vers változásnál a könyvnév az előző token): **F34 159** (`naplok/F34_M2_csere.tsv`
JAVIT — pontosan a 159 JAVIT-sor), **F46 250** (`naplok/BDB_KONYVFELOLDAS_csere.tsv` / `_kezi.tsv`), **F46.6 3** — H5973, H7588, H9005
„Phoenician” → „Pharaoh”: a csere-naplókban nem szerepel, a git-történet igazolja (`git log -G Pharaoh -- konkordancia/BDB_teljes_unabridged.tsv`:
`6400b5a7` „F46.6: gépi csere a DT-F46 szerint”).

**A nézet-generátor** (`eszkozok/bdb_jelolt/nezet_general.py`): a tábla sorai (`jel` + `szoveg`) + a `hivatkozas` javítások (+ `--pe-mem`: a
pe/mem `javitva` sorok, a forrás alakjában — a U+FB3E prezentációs formát is); a kimenet a `--ki` útvonalra (a repón kívül; a brief `ir`
mezője nem ad neki helyet), a `BDB_teljes_unabridged.tsv` változatlan. Bájtos összevetés a TSV-vel (whitespace-normalizálva):

| nézet | azonos | sub | szokoz | forras_html | pe_mem | nincs_a_nezetben | egyéb |
|---|---|---|---|---|---|---|---|
| a hivatkozás-javítással (412 alkalmazva) | 7 419 | 564 | 102 | 5 | — | 9 | **0** |
| + pe/mem (3 823 alkalmazva, 0 sikertelen) | 6 264 | 321 | 76 | 5 | 1 424 | 9 | **0** |

A `tsv_utolagos` osztály eltűnt (a 3. lépésben 247): a 247 sor javítása a nézetben megvan. A megmaradt eltérés csak a jóváhagyott
osztályokban: `sub` (a TSV `_N`-je), `szokoz` (a fej utáni forrás-szóköz), `forras_html` (a JSON hibás HTML-je, 5 Strong), `pe_mem` (a
DT-F107f javítása), `nincs_a_nezetben` (F57/F72, 9). Teszt: `teszt_bont.py` (`Nezet` osztály), OK.

`scope=F107 6.1 | forras=python eszkozok/bdb_jelolt/nezet_general.py --osszevet [--pe-mem] --ki <scratchpad>; forras_javit.py | ts=2026-10-18`

## 7. lépés — a kész magyar fordítás illesztése (⛔ DT-F107b)

Eszköz: `eszkozok/bdb_jelolt/hu_illeszt.py` → `adat/bdb_szakasz_hu.tsv` (SEMA 2.32). Bemenet: a szakasztábla és az `adat/forditasok.tsv`
BDB-sorai (csak olvasva; Strongonként az utolsó nem üres `forditas_hu`); a magyar oldali jelölő- és törzsnév-felismerés a tagolás-kapué
(`eszkozok/forditas_kapuk.py`, importálva). Módszer: a sor fej-jelölői (szám, betű, római, zárójeles, törzsnév) sorrendtartó, mohó
illesztése; ha a jelölő nem illeszkedik, horgony: a sor első fejezet:verse a magyarban az előző és a következő illesztett szakasz között, a
szakasz a sor saját jelölőjének ott álló utolsó előfordulásától (pl. H0040 „+? 1 Gerár királya”: a kapu regexe a kérdőjel után nem ismeri
fel az „1”-et, a horgony igen).

| mérés | illeszkedik | tagolatlan | horgonnyal | elakad |
|---|---|---|---|---|
| kiinduló (2026-10-16, `manual`, a lexikon jelölt tagolásán) | 355 | 89 | — | 230 |
| Strong-szint, a kapu szigorú `_illeszt`-jével a szakasztáblán | **380** | **94** | — | **200** |
| Strong-szint, horgonnyal | **385** | **83** | **105** | **101** |

Soronként (9 664 sor, 674 Strong): `illeszkedik` 6 210, `horgonnyal` 271, `elakad` 618, `jelolo_nelkul` 2 565. Az `elakad` 618 sor (101
Strong) jelölőtípus szerint: betű a–i 296, szám 259, törzsnév 52, betű j-től 7 (a kapu betű-regexe csak a–i), római/egyéb 4. Az
`adat/forditasok.tsv` nem íródott (git: változatlan). Teszt: `teszt_bont.py` (`HuIlleszt`), 43 teszt összesen, OK.

`scope=F107 7. lépés, 674 Strong | forras=python eszkozok/bdb_jelolt/hu_illeszt.py --ts 2026-10-18 (F107.34, f845b16d) | ts=2026-10-18`

Javaslat: `DT-F107b` (`DONTESEK.md`).

### 7.1 A DT-F107b alkalmazása: a magyar jelölő-felismerés bővítése (F107.38) és a maradék elakadó Strongok (N-F107b)

A felhasználó (chat, az orkesztrátoron át, 2026-10-18): „DT-F107b (d), majd (c) — előbb a magyar jelölő-felismerés bővítése (betű j-től,
kérdőjel utáni szám, ragozott törzsnév) teszttel és újramérés; a maradék elakadó Strong a #38 következő adagjában szakaszonként
újrafordítva; kézi illesztés nincs.”

**A bővítés** (`hu_illeszt.py`; a kapu, `eszkozok/forditas_kapuk.py` érintetlen, nincs az `ir` mezőben): (1) törzsnév **mindkét oldalon**
a bontó törzslistájából (a szeletelőével azonos), a forrás alakjában (`` ` `` ' ʿ ‘ ’), a magyaros alakokkal (Nifal, Hifil, Hofal, Hitpael) és a
magyar raggal, kötőjellel is; kulcs a kanonikus név. Ok (mérve a magyar szövegeken): a kapu mintája a „Hithpa`el”-t (78 előfordulás) nem
fogja, az arámi törzseket (Pa`el 29, Pe`al 28, Haph`el 15, Aph`el 15) egyáltalán nem; a ragozott alakokat („Hiph`ilben”, „Qal-ban”) a kapu is
fogta. (2) betű j-től, csak tagolásjel után (szövegközben rövidítés: „l. ott”); a szám utáni „k.” nem jelölő („632 k.”). (3) a kérdőjel utáni
szám („+? 1 Gerár”, H0040). Teszt (valós adatból): pozitív — H0040 „+? 1 Gerár”, H5674 „17:3. j. elmenni”, H0559 „Hithpa`el”, H5414 „Pe`al”,
H6213 „Pa`el”; negatív — „a 2 fiú”, „b) pont”, H5869 „, l. a kommentárokat”, H3117 „632 k.)”, „a q. jelű”, „papok”, „puszta”, „pap”,
„Pentateuchusban” (a rövid „Pi”/„Pu” tő nem jelölő). `teszt_bont.py` 45 teszt, OK; a tábla `--ellenoriz`-zel bájtra azonos; az
`adat/forditasok.tsv` és a `konkordancia/BDB_teljes_unabridged.tsv` változatlan (`git diff --quiet`).

| mérés | illeszkedik | horgonnyal | elakad | tagolatlan / jelölő nélküli |
|---|---|---|---|---|
| Strong-szint, horgonnyal — F107.34 | 385 | 105 | 101 | 83 |
| **Strong-szint, horgonnyal — F107.38** | **409** | **85** | **98** | **82** |
| Strong-szint, a kapu szigorú `_illeszt`-jével (a kapu regexei; a kiinduló 355 / — / 230 / 89 módszere) | 380 | — | 200 | 94 (változatlan) |
| soronként — F107.34 | 6 210 | 271 | 618 | 2 565 |
| **soronként — F107.38** | **6 395** | **202** | **606** | **2 461** |

`scope=F107 7.1 | forras=python eszkozok/bdb_jelolt/hu_illeszt.py --ts 2026-10-18 (F107.38, e285d4b6) | ts=2026-10-18`

A maradék elakadás főként nem a felismerés hiánya: a mohó, sorrendtartó illesztésben egy korábbi hivatkozás-előfordulás (pl. „(vö. Hiph`il
lent)”) vagy egy túlfutó jelölő elviszi a kurzort (mintavétel: H3254, H7323, H1980). A DT-F107b (c) szerint ezek nem kapnak kézi
illesztést.

**A maradék elakadó Strongok — átadandó tétel a #38-nak (N-F107b): 98 Strong, 606 sor** (jelölőtípus: betű 287, szám 252, törzs 63, római 4).
A kulcs a szakasztábla `strong` + `sorszam`-a (`adat/bdb_szakaszok.tsv`, `adat/bdb_szakasz_hu.tsv`).

| Strong | elakadt sor | elakadt szakaszok (`sorszam`:`utvonal` (jelölőtípus)) |
|---|---|---|
| H0068 | 8 | 6:-/3/- (szám); 7:-/4/- (szám); 8:-/5/- (szám); 9:-/6/- (szám); 10:-/7/- (szám); 11:-/8/- (szám); 12:-/9/- (szám); 15:-/1/- (szám) |
| H0157 | 1 | 4:Qal/-/n (betű) |
| H0259 | 9 | 5:-/3/- (szám); 6:-/4/- (szám); 7:-/5/- (szám); 8:-/6/- (szám); 9:-/7/- (szám); 10:-/8/- (szám); 11:-/8/a (betű); 12:-/8/b (betű); 15:-/1/- (szám) |
| H0352 | 2 | 4:-/2/- (szám); 5:-/3/- (szám) |
| H0410 | 1 | 9:-/5/- (szám) |
| H0539 | 1 | 11:Qal/4/- (szám) |
| H0637 | 1 | 6:-/1/- (szám) |
| H0702 | 1 | 10:-/2/a (betű) |
| H0834 | 34 | 16:-/5/- (szám); 17:-/6/- (szám); 18:-/7/- (szám); 19:-/7/a (betű); 20:-/7/b (betű); 21:-/7/c (betű); 22:-/8/- (szám); 24:-/8/a (betű); 25:-/8/b (betű); 26:-/8/c (betű); 27:-/8/d (betű); 28:-/8/e (betű); 29:-/8/f (betű); 37:-/-/b (betű); 39:-/-/d (betű); 42:-/-/b (betű); 43:-/-/c (betű); 45:-/1/- (szám); 46:-/1/a (betű); 47:-/1/b (betű); 48:-/1/c (betű); 49:-/1/d (betű); 50:-/1/e (betű); 51:-/2/- (szám); 52:-/3/- (szám); 56:-/2/- (szám); 58:-/3/- (szám); 60:-/3/a (betű); 61:-/3/b (betű); 62:-/4/- (szám); 63:-/4/a (betű); 64:-/4/b (betű); 65:-/4/c (betű); 66:-/4/d (betű) |
| H0995 | 17 | 20:Qal/4/- (szám); 21:Niph'al/-/- (törzs); 23:Hiph'il/-/- (törzs); 29:Hiph'il/3/a (betű); 30:Hiph'il/3/b (betű); 31:Hiph'il/3/c (betű); 32:Hiph'il/3/d (betű); 33:Hiph'il/3/e (betű); 34:Hithpa'el/-/- (törzs); 35:Hithpa'el/1/- (szám); 36:Hithpa'el/1/a (betű); 37:Hithpa'el/1/b (betű); 38:Hithpa'el/1/c (betű); 39:Hithpa'el/1/d (betű); 40:Hithpa'el/1/e (betű); 41:Hithpa'el/1/f (betű); 42:Hithpa'el/2/- (szám) |
| H1004 | 14 | 12:-/3/- (szám); 13:-/4/- (szám); 14:-/5/- (szám); 15:-/5/a (betű); 16:-/5/b (betű); 17:-/5/c (betű); 18:-/5/d (betű); 19:-/5/e (betű); 20:-/6/- (szám); 21:-/7/- (szám); 22:-/8/- (szám); 23:-/8/a (betű); 24:-/8/b (betű); 28:-/1/- (szám) |
| H1129 | 15 | 6:Qal/1/i (betű); 9:Qal/1/d (betű); 10:Qal/1/e (betű); 11:Qal/1/f (betű); 12:Qal/1/g (betű); 13:Qal/1/h (betű); 14:Qal/1/i (betű); 15:Qal/2/- (szám); 17:Qal/2/b (betű); 18:Niph'al/-/- (törzs); 19:Niph'al/1/a (szám); 20:Niph'al/1/b (betű); 21:Niph'al/2/a (szám); 22:Niph'al/2/b (betű); 23:Niph'al/2/c (betű) |
| H1197 | 10 | 9:Pi'el/1/- (szám); 10:Pi'el/2/- (szám); 11:Pi'el/3/- (szám); 12:Pu'al/-/- (törzs); 14:Hiph'il/1/- (szám); 15:Hiph'il/2/- (szám); 16:Hiph'il/3/- (szám); 18:Qal/-/- (törzs); 19:Niph'al/-/- (törzs); 21:Hiph'il/-/- (törzs) |
| H1242 | 1 | 10:-/1/d (betű) |
| H1288 | 7 | 30:Pu'al/2/a (betű); 31:Pu'al/2/b (betű); 33:Pu'al/4/- (szám); 34:Hiph'il/-/- (törzs); 35:Hithpa'el/-/- (törzs); 39:-/2/- (szám); 40:Pa'el/-/- (törzs) |
| H1320 | 1 | 10:-/6/- (szám) |
| H1419 | 7 | 4:-/2/- (szám); 5:-/3/- (szám); 6:-/4/- (szám); 7:-/5/- (szám); 8:-/6/- (szám); 9:-/6/a (betű); 10:-/6/b (betű) |
| H1568 | 1 | 22:-/6/- (szám) |
| H1870 | 6 | 6:-/3/- (szám); 7:-/4/- (szám); 12:-/5/- (szám); 13:-/6/a (szám); 14:-/6/b (betű); 15:-/6/c (betű) |
| H1875 | 11 | 7:Qal/2/a (betű); 8:Qal/2/b (betű); 10:Qal/3/a (betű); 11:Qal/3/b (betű); 12:Qal/4/a (szám); 13:Qal/4/b (betű); 14:Qal/5/- (szám); 15:Qal/6/- (szám); 16:Qal/7/- (szám); 18:Niph'al/1/- (szám); 19:Niph'al/2/- (szám) |
| H1980 | 40 | 27:Qal/5/d (betű); 28:Qal/5/e (betű); 29:Qal/-/- (római); 30:Qal/1/- (szám); 31:Qal/2/- (szám); 32:Qal/2/- (szám); 35:Qal/3/- (szám); 36:Qal/3/a (betű); 37:Qal/3/b (betű); 38:Qal/3/c (betű); 39:Qal/3/d (betű); 40:Qal/3/e (betű); 41:Qal/4/- (szám); 42:Niph'al/-/- (törzs); 43:Pi'el/-/- (törzs); 44:Pi'el/1/- (szám); 45:Hithpa'el/-/- (törzs); 46:Hithpa'el/2/- (szám); 48:Hithpa'el/3/- (szám); 49:Hithpa'el/4/- (szám); 50:Hithpa'el/-/- (törzs); 51:Hithpa'el/1/- (szám); 52:Hithpa'el/1/a (betű); 53:Hithpa'el/1/b (betű); 55:Hithpa'el/2/- (szám); 56:Hiph'il/-/- (törzs); 57:Qal/-/- (törzs); 58:Qal/1/- (szám); 59:Qal/1/a (betű); 60:Qal/1/b (betű); 61:Qal/1/c (betű); 62:Qal/1/d (betű); 63:Qal/1/e (betű); 64:Qal/2/- (szám); 65:Qal/3/- (szám); 66:Qal/3/a (betű); 67:Qal/3/b (betű); 68:Qal/4/- (szám); 70:-/5/a (szám); 71:-/5/b (betű) |
| H1984 | 1 | 23:Pu'al/1/- (szám) |
| H2091 | 1 | 11:-/9/- (szám) |
| H2220 | 1 | 7:-/2/- (szám) |
| H2388 | 11 | 41:Pi'el/5/- (szám); 42:Pi'el/6/- (szám); 43:Pi'el/6/a (betű); 44:Pi'el/6/b (betű); 45:Pi'el/6/c (betű); 46:Pi'el/6/c (betű); 47:Pi'el/6/d (betű); 48:Hithpa'el/-/- (törzs); 49:Hithpa'el/1/- (szám); 50:Hithpa'el/2/- (szám); 51:Hithpa'el/3/- (szám) |
| H2396 | 1 | 6:-/1/- (szám) |
| H2398 | 7 | 10:Pi'el/-/- (törzs); 14:Pi'el/4/- (szám); 15:Hiph'il/-/- (törzs); 18:Hiph'il/3/- (szám); 19:Hithpa'el/-/- (törzs); 20:Hithpa'el/1/- (szám); 21:Hithpa'el/2/- (szám) |
| H2416 | 4 | 14:-/1/a (betű); 19:-/4/- (szám); 26:-/3/- (szám); 28:-/1/- (szám) |
| H2451 | 1 | 7:-/5/- (szám) |
| H2470 | 1 | 23:Pi'el/1/- (szám) |
| H2506 | 2 | 8:-/2/- (szám); 14:-/3/- (szám) |
| H2568 | 1 | 11:-/2/- (szám) |
| H2572 | 2 | 9:-/3/- (szám); 12:-/4/- (szám) |
| H2617 | 13 | 10:-/1/- (szám); 11:-/1/a (betű); 12:-/1/b (betű); 13:-/1/c (betű); 14:-/1/d (betű); 15:-/1/e (betű); 16:-/2/- (szám); 17:-/3/- (szám); 18:-/3/a (betű); 19:-/3/b (betű); 20:-/3/c (betű); 21:-/3/d (betű); 22:-/4/- (szám) |
| H3027 | 25 | 10:-/3/- (szám); 11:-/3/a (betű); 12:-/3/b (betű); 13:-/3/c (betű); 14:-/3/d (betű); 15:-/3/e (betű); 16:-/4/- (szám); 17:-/4/a (betű); 18:-/4/b (betű); 19:-/4/c (betű); 20:-/4/d (betű); 21:-/4/e (betű); 22:-/4/f (betű); 23:-/4/g (betű); 24:-/5/- (szám); 26:-/5/b (betű); 27:-/5/c (betű); 28:-/5/d (betű); 29:-/5/e (betű); 30:-/5/f (betű); 31:-/5/g (betű); 32:-/5/i (betű); 33:-/5/h (betű); 34:-/5/i (betű); 35:-/5/g (betű) |
| H3068 | 10 | 6:-/-/- (római); 7:-/1/- (római); 12:-/1/e (betű); 13:-/1/f (betű); 14:-/1/g (betű); 15:-/1/h (betű); 16:-/2/- (szám); 18:-/2/b (betű); 19:-/2/c (betű); 20:-/2/d (betű) |
| H3083 | 8 | 3:-/1/- (szám); 4:-/2/- (szám); 5:-/3/- (szám); 6:-/2/- (szám); 7:-/4/- (szám); 8:-/5/- (szám); 9:-/6/- (szám); 22:-/2/- (szám) |
| H3092 | 1 | 4:-/5/- (szám) |
| H3117 | 23 | 13:-/3/f (betű); 17:-/3/- (szám); 18:-/2/- (szám); 19:-/4/- (szám); 20:-/4/a (betű); 21:-/4/b (betű); 22:-/4/c (betű); 23:-/5/- (szám); 24:-/5/a (betű); 26:-/5/c (betű); 27:-/6/- (szám); 28:-/6/a (betű); 29:-/5/- (szám); 30:-/5/b (betű); 31:-/5/c (betű); 33:-/7/- (szám); 34:-/7/a (betű); 36:-/7/c (betű); 37:-/7/d (betű); 38:-/7/e (betű); 40:-/7/g (betű); 43:-/7/h (betű); 45:-/7/i (betű) |
| H3254 | 1 | 7:Hiph'il/-/- (törzs) |
| H3384 | 8 | 10:Qal/1/- (szám); 11:Qal/2/- (szám); 12:Qal/3/- (szám); 14:Niph'al/-/- (törzs); 15:Hiph'il/-/- (törzs); 16:Hiph'il/1/- (szám); 17:Hiph'il/2/- (szám); 18:Hiph'il/3/- (szám) |
| H3423 | 3 | 10:Niph'al/-/- (törzs); 11:Pi'el/-/- (törzs); 19:Hiph'il/5/- (szám) |
| H3588 | 1 | 28:-/2/- (szám) |
| H3603 | 3 | 6:-/1/- (szám); 7:-/2/- (szám); 8:-/3/- (szám) |
| H3605 | 4 | 6:-/1/c (betű); 12:-/2/a (betű); 14:-/2/b (betű); 17:-/2/- (szám) |
| H3644 | 2 | 5:-/2/- (szám); 8:-/2/- (szám) |
| H3722 | 2 | 15:Pi'el/3/e (betű); 16:Pu'al/-/- (törzs) |
| H3742 | 1 | 9:-/5/- (szám) |
| H3772 | 11 | 16:Niph'al/2/- (szám); 19:Pu'al/-/- (törzs); 20:Pu'al/1/- (szám); 21:Pu'al/2/- (szám); 22:Hiph'il/-/- (törzs); 23:Hiph'il/1/- (szám); 24:Hiph'il/2/- (szám); 25:Hiph'il/2/a (betű); 26:Hiph'il/2/b (betű); 27:Hiph'il/2/c (betű); 28:Hiph'il/3/- (szám) |
| H3789 | 5 | 10:Qal/4/- (szám); 11:Niph'al/-/- (törzs); 13:Niph'al/2/- (szám); 14:Pi'el/-/- (törzs); 16:Pe'al/-/- (törzs) |
| H3808 | 1 | 9:-/2/- (szám) |
| H3881 | 5 | 5:-/3/- (szám); 6:-/1/- (szám); 12:-/2/a (betű); 13:-/2/b (betű); 14:-/2/c (betű) |
| H3947 | 4 | 34:Pu'al/4/- (szám); 35:Hoph'al/-/- (törzs); 36:Hoph'al/1/- (szám); 37:Hoph'al/2/- (szám) |
| H3967 | 1 | 10:-/2/- (szám) |
| H4217 | 1 | 4:-/2/- (szám) |
| H4264 | 2 | 4:-/1/- (szám); 7:-/2/- (szám) |
| H4480 | 29 | 7:-/2/- (szám); 11:-/2/c (betű); 12:-/2/d (betű); 13:-/2/e (betű); 16:-/2/f (betű); 18:-/3/- (szám); 20:-/3/a (betű); 21:-/3/b (betű); 22:-/4/- (szám); 23:-/4/a (betű); 24:-/4/b (betű); 25:-/4/c (betű); 26:-/5/- (szám); 27:-/5/a (betű); 28:-/5/b (betű); 29:-/5/c (betű); 30:-/5/d (betű); 31:-/6/- (szám); 32:-/6/a (betű); 35:-/6/c (betű); 36:-/6/d (betű); 37:-/7/- (szám); 38:-/7/a (betű); 39:-/7/b (betű); 40:-/7/c (betű); 42:-/8/- (szám); 46:-/9/- (szám); 47:-/9/a (betű); 48:-/9/b (betű) |
| H4605 | 1 | 9:-/2/- (szám) |
| H4639 | 1 | 6:-/2/a (szám) |
| H4672 | 24 | 23:Niph'al/-/- (törzs); 24:Niph'al/2/- (szám); 25:Niph'al/2/- (szám); 26:Niph'al/1/a (szám); 27:Niph'al/1/b (betű); 28:Niph'al/1/c (betű); 29:Niph'al/1/d (betű); 30:Niph'al/1/e (betű); 31:Niph'al/1/f (betű); 32:Niph'al/1/g (betű); 33:Niph'al/1/h (betű); 34:Niph'al/1/i (betű); 35:Niph'al/2/- (szám); 36:Niph'al/2/a (betű); 37:Niph'al/2/b (betű); 38:Niph'al/2/c (betű); 39:Niph'al/2/d (betű); 40:Niph'al/2/e (betű); 41:Niph'al/2/f (betű); 42:Niph'al/3/- (szám); 43:Hiph'il/-/- (törzs); 44:Hiph'il/1/- (szám); 45:Hiph'il/2/- (szám); 46:Hiph'il/3/- (szám) |
| H4940 | 1 | 11:-/3/- (szám) |
| H5127 | 4 | 7:Qal/4/- (szám); 10:Hiph'il/-/- (törzs); 12:Hiph'il/1/- (szám); 13:Hiph'il/2/- (szám) |
| H5307 | 3 | 18:Qal/7/- (szám); 36:Pil'el/-/- (törzs); 38:Pe'al/-/- (törzs) |
| H5315 | 2 | 3:-/1/- (szám); 22:-/6/- (szám) |
| H5324 | 5 | 12:Hiph'il/-/- (törzs); 13:Hiph'il/1/- (szám); 14:Hiph'il/2/- (szám); 16:Qal/-/- (törzs); 17:Qal/4/- (szám) |
| H5674 | 56 | 8:Qal/1/c (betű); 9:Qal/1/d (betű); 10:Qal/1/e (betű); 11:Qal/1/f (betű); 12:Qal/1/g (betű); 13:Qal/1/h (betű); 14:Qal/1/i (betű); 15:Qal/1/j (betű); 16:Qal/2/- (szám); 17:Qal/3/- (szám); 18:Qal/3/a (betű); 19:Qal/3/b (betű); 20:Qal/3/c (betű); 21:Qal/3/d (betű); 22:Qal/3/e (betű); 23:Qal/4/a (szám); 24:Qal/4/b (betű); 25:Qal/4/c (betű); 26:Qal/4/d (betű); 27:Qal/4/e (betű); 28:Qal/5/- (szám); 29:Qal/5/a (betű); 31:Qal/5/b (betű); 32:Qal/5/c (betű); 33:Qal/5/d (betű); 34:Qal/5/e (betű); 35:Qal/5/f (betű); 36:Qal/5/g (betű); 37:Qal/5/h (betű); 38:Qal/5/i (betű); 39:Qal/6/- (szám); 40:Qal/6/a (betű); 41:Qal/6/b (betű); 42:Qal/6/c (betű); 43:Qal/6/d (betű); 44:Qal/6/e (betű); 45:Qal/6/f (betű); 47:Niph'al/-/- (törzs); 48:Pi'el/1/- (törzs); 49:Pi'el/2/- (szám); 50:Hithpa'el/-/- (törzs); 51:Hiph'il/-/- (törzs); 52:Hiph'il/1/- (szám); 53:Hiph'il/1/a (betű); 54:Hiph'il/1/b (betű); 55:Hiph'il/1/c (betű); 56:Hiph'il/1/d (betű); 57:Hiph'il/2/a (szám); 58:Hiph'il/2/b (betű); 59:Hiph'il/3/a (szám); 60:Hiph'il/3/b (betű); 61:Hiph'il/3/c (betű); 62:Hiph'il/3/d (betű); 63:Hiph'il/4/- (szám); 67:-/1/- (szám); 68:-/2/a (szám) |
| H5797 | 1 | 15:-/5/- (szám) |
| H5869 | 2 | 16:-/1/k (betű); 21:-/1/o (betű) |
| H5971 | 16 | 6:-/2/a (betű); 7:-/2/b (betű); 8:-/2/c (betű); 9:-/2/d (betű); 10:-/3/- (szám); 11:-/4/- (szám); 12:-/5/- (szám); 13:-/5/a (betű); 14:-/5/b (betű); 16:-/5/c (betű); 17:-/5/d (betű); 18:-/5/e (betű); 19:-/5/f (betű); 20:-/5/g (betű); 21:-/5/h (betű); 22:-/5/i (betű) |
| H6086 | 2 | 3:-/1/- (szám); 7:-/2/- (szám) |
| H6213 | 1 | 37:Niph'al/2/- (szám) |
| H6240 | 2 | 24:-/6/- (szám); 30:-/8/- (szám) |
| H6242 | 7 | 12:-/2/a (betű); 14:-/2/c (betű); 15:-/2/d (betű); 16:-/2/e (betű); 17:fej (római); 18:-/1/- (szám); 19:-/2/a (szám) |
| H6588 | 1 | 5:-/3/- (szám) |
| H6942 | 16 | 21:Pi'el/3/a (betű); 26:Pi'el/4/c (betű); 27:Pi'el/4/d (betű); 28:Pu'al/-/- (törzs); 29:Hiph'il/-/- (törzs); 30:Hiph'il/1/- (szám); 31:Hiph'il/1/a (betű); 32:Hiph'il/1/b (betű); 33:Hiph'il/1/c (betű); 34:Hiph'il/2/- (szám); 35:Hiph'il/3/- (szám); 36:Hithpa'el/-/- (törzs); 37:Hithpa'el/1/- (szám); 38:Hithpa'el/2/- (szám); 39:Hithpa'el/3/- (szám); 40:Hithpa'el/4/- (szám) |
| H7122 | 1 | 6:Niph'al/-/- (törzs) |
| H7200 | 4 | 13:Qal/6/- (szám); 55:Hiph'il/2/a (betű); 56:Hiph'il/2/b (betű); 57:Hiph'il/2/c (betű) |
| H7218 | 1 | 7:-/3/- (szám) |
| H7227 | 8 | 3:-/1/- (szám); 8:-/1/e (betű); 9:-/1/f (betű); 10:-/1/g (betű); 11:-/2/- (szám); 12:-/2/a (betű); 13:-/2/b (betű); 14:-/2/c (betű) |
| H7323 | 3 | 8:Qal/2/a (betű); 9:Qal/2/b (betű); 11:Hiph'il/-/- (törzs) |
| H7626 | 1 | 9:-/2/- (szám) |
| H7651 | 1 | 14:-/5/- (szám) |
| H7657 | 3 | 11:-/3/a (betű); 12:-/3/b (betű); 13:-/3/c (betű) |
| H7673 | 3 | 13:Hiph'il/3/- (szám); 14:Hiph'il/4/- (szám); 16:Hiph'il/5/- (szám) |
| H7725 | 6 | 52:Hiph'il/2/e (betű); 53:Hiph'il/2/f (betű); 54:Hiph'il/2/g (betű); 65:Hiph'il/9/- (szám); 67:-/10/- (szám); 68:-/11/- (szám) |
| H7896 | 2 | 9:Qal/4/- (szám); 10:Hoph'al/-/- (törzs) |
| H7901 | 8 | 5:Qal/-/- (törzs); 6:Qal/1/- (szám); 15:Qal/4/a (szám); 16:Qal/4/b (betű); 17:Qal/4/c (betű); 18:Qal/5/- (szám); 19:Pu'al/-/- (törzs); 20:Pu'al/-/- (törzs) |
| H7969 | 1 | 9:-/2/- (szám) |
| H7971 | 17 | 21:Niph'al/-/- (törzs); 22:Pi'el/-/- (törzs); 24:Pi'el/1/a (betű); 25:Pi'el/1/b (betű); 26:Pi'el/1/c (betű); 27:Pi'el/1/d (betű); 28:Pi'el/1/e (betű); 29:Pi'el/2/a (szám); 30:Pi'el/2/b (betű); 31:Pi'el/2/c (betű); 32:Pi'el/2/d (betű); 34:Pi'el/4/- (szám); 36:Pi'el/5/- (szám); 37:Pi'el/6/- (szám); 38:Pi'el/7/- (szám); 39:Pu'al/-/- (törzs); 40:Hiph'il/-/- (törzs) |
| H7993 | 4 | 11:Hiph'il/2/a (betű); 12:Hiph'il/2/b (betű); 13:Hiph'il/2/c (betű); 16:Hoph'al/-/- (törzs) |
| H8064 | 1 | 10:-/4/- (szám) |
| H8074 | 4 | 14:Hiph'il/-/- (törzs); 16:Hiph'il/2/a (törzs); 17:Hiph'il/2/b (betű); 18:Hoph'al/-/- (törzs) |
| H8083 | 1 | 8:-/2/- (szám) |
| H8130 | 3 | 10:Niph'al/-/- (törzs); 11:Pi'el/-/- (törzs); 12:Pi'el/1/- (szám) |
| H8337 | 1 | 8:-/2/- (szám) |
| H8415 | 1 | 8:-/4/- (szám) |
| H8672 | 1 | 9:-/2/- (szám) |
| H9008 | 1 | 9:-/2/- (szám) |

## Átadandó tételek (a #107 nem veszi fel; a `/befogad` dolga)

- **A TSV cseréje és az olvasók átállása** (DT-F107c (d)): a `konkordancia/BDB_teljes_unabridged.tsv` helyett a `nezet_general.py` nézete;
  az olvasók: `adat/datasetek.tsv` 4 sor (+4 megjegyzés), 16 brief `olvas` mezője, 29 Python-fájl (l. 6. (3)); a 674 fordítás `forras_hash`-e
  (V1: 446, V2: 546 sor változna) és a `_N`/szóköz technikai eltérés kezelése.
- **A 8. lépés** (a #102 és a #38 briefjébe a tábla elérhetősége és a mért számok): a döntés után az orkesztrátor egyezteti (a két brief nincs
  az `ir` mezőben).
- **N-F107a** (a kész fordítások pe/mem-érintettsége) — nyitva, `NYITOTT_FELADATOK.md`.
- **N-F107b** (a #38 következő adagjában szakaszonként újrafordítandó 98 Strong, a lista: 7.1) — nyitva, `NYITOTT_FELADATOK.md`; a #38
  briefjének törzsébe a 8. lépés átadása beírta (l. 8.).
- **`.gitattributes`** (`konkordancia/lexikonok_nyers/DictBDB.json -text`) — javaslat, nem írva.

## 8. lépés — átadás a #102 és a #38 briefjébe (F107.41–F107.43)

A felhasználó (chat, 2026-10-18): „8. lépés: egyeztetett eltérésként az F102 és F38 brief törzse (fejléc nem) bekerül az ir mezőbe; az
átadás oda íródik (tábla elérhetősége, mért számok, N-F107b lista, a #102 hatókör-szűkítési javaslata), utána független ellenőrzés és zárás.”

**Egyeztetett eltérés:** az `F102_BDB_SZELETELO_JAVITAS_BRIEF.md` és az `F38_BDB_FORDITAS_BRIEF.md` felkerült a #107 `ir` mezőjére (F107.41) —
**csak a törzsük** íródik, a fejlécük nem (a beszúró szkript a második `---`-ig bájtra összeveti a fejlécet). `python eszkozok/feladatok.py
ellenoriz`: 137 brief, 0 hiba, 0 figyelmeztetés (előtte és utána is); `fuggesek`: a #107-tel nincs `KIZAR`; új `FUGGES`: a #27, a #67 és a
#103 olvassa az F38 briefet (állapotuk `nem_indult` / `brief_kell`); **a #38 `allapot: fut`** — a briefje törzsének írása merge-kor ütközhet
a #38 saját menetével (jelezve).

- **F102** (F107.42): „## 1c. Átadás a #107-ből (2026.10.18)” a 2. Hatókör előtt — a tábla, a javítótábla és az eszközök elérhetősége (DT190 🟡: a
  kulcs nincs befagyasztva), mindkét mérce (aranyminta 96,7% / 98,8%, seed-101 9 / 13 / 9 / 10, korpusz 85,4%), a seed-101 helyenként, és a
  hatókör-szűkítés **javaslatként** (megszűnő: zárójeles / gyakoriságszámos jelölő, törzsfejléc, fő tagolás, alcímszó, laza jelölő,
  fej-összefoglaló, útvonal-formátum; forrásban hibás → javítótábla: M102, M117, M162; marad: igehely → szakasz, öröklés, sigla-szűrés,
  M130, a korpusz-eltérések osztályozása, új vak mérés), a `/befogad`-dal jóváhagyandó.
- **F38** (F107.43): „## Átadás a #107-ből (2026.10.18)” a Megállási pont előtt — `adat/bdb_szakasz_hu.tsv` és a szakaszkulcs, 409 / 85 / 98 / 82,
  a DT-F107b döntés, az N-F107b lista helye (98 Strong, 606 szakasz, 7.1), a DT-F107c (d) (a `forras_hash` a változatlan TSV-hez kötött, a
  csere külön feladat), az N-F107a (pe/mem).

## Zárás-előkészítő összefoglaló (a független ellenőrzéshez; a zárójelentés és a `lezarva` állapot nem íródott)

**Döntések** (`DONTESEK.md`, helyőrzővel, mind 🟢):

| tétel | lényeg | alkalmazás |
|---|---|---|
| DT-F107a | (c) hibrid forrás (szöveg a `DictBDB.json`-ból, `bdb_id`/szócikkhatár/`section`/`remarks` a `BDB.lexicon`-ból, csak metaadat) + (i) licenc (a JSON közkincs; a lexikon tisztázatlan) + (x) a JSON a repóban | F107.5–.7 |
| DT-F107d | (a) a playbook 2. pontja: a nyers forrás megőrzése, a veszteséges konverzió naplózása (CI-kapu nélkül) | F107.6 |
| DT-F107e | (b), majd (a): a 0,5 alatti illesztési kör, utána a tábla a nem egyező Strongok `bdb_id`-je nélkül | F107.14–.15 |
| DT-F107f | (a) a pe/mem javítótábla; N-F107a | F107.13, .16 |
| DT-F107g | (a)+(b) a három `tabla_hiba`-osztály; a `forras_hiba` csomópontok igazolva, kézi sorral | F107.22–.25 |
| DT-F107h | (a) a negyedik szabály (lexikon-metaadat), feltétel: a korpusz és a seed-101 nem romlik | F107.29 |
| DT-F107c | (d) a nézet-generátor és a 247 sor F34/F46-javítása itt; a TSV cseréje és az olvasók átállása külön feladat | F107.33 |
| DT-F107b | (d), majd (c): a magyar jelölő-felismerés bővítése; a maradék 98 Strong a #38-ban újrafordítva (N-F107b) | F107.38–.39 |
| 8. lépés | egyeztetett eltérés: a két brief törzse az `ir`-ben, az átadás oda íródott | F107.41–.43 |

**Egyeztetett eltérések a brieftől:** az `adat/licencek.tsv` az `ir`-ben (csak a `BDB` sor 3. mezője, F107.7); az `F102_…` és az `F38_…`
brief törzse az `ir`-ben (8. lépés); a szakasztábla oszlopai a brief listáján túl `alszocikk`, `szakasz`, `resz`, `jel`, `illesztes`;
a `adat/bdb_szakasz_hu.tsv` mellé nem készült külön datasetek-sor (a brief nem írta elő).

**Tudnivalók a független ellenőrzéshez:**
- **A 4. szabály első változata elvetve** (4.8): a „lexikonban szövegen belül” jel önmagában rontott (korpusz 78,4%, seed-101 8 / 13; a
  feltétel szerint nem commitolva); a commitolt változat a hivatkozó szóra szűkít.
- **A mérce:** az aranyminta a `forras_hiba` nélkül **98,8%** (411 / 416), a javasolt ≥ 99% egy csomóponttal nem teljesül (maradék: H3176 2
  számozatlan jelentés, H0834 2 értelmezési eltérés, H2939 1 fejsorbeli törzsnév); az orkesztrátor a feltétel teljesülése miatt a munkát
  folytattatta.
- **A tokenizáló-hiba** („1.a.”) javítása a DT-F107g három osztályán kívül esett (4.5, jelezve).
- **A H0157 bontó-maradvány:** egy elakadt sor (`Qal/-/n`) valószínűleg a bontó hamis „n.” feje (a „n.” rövidítés) — nem javítva.
- **A H7626 „145:”** nincs a javítótáblában (a hiba-volta nincs eldöntve).
- **A `.gitattributes`-javaslat** (`DictBDB.json -text`): nem írva (nincs az `ir`-ben); a hash a git-objektumra vonatkozik.
- **SEMA-ütközés lehetősége:** a #107 csak a saját 2.30–2.32 szakaszát írta; a #11 M3 is írhatja az `adat/SEMA.md`-t.
- **A #38 fut:** a briefje törzsébe írt átadás merge-kor ütközhet.
- **Nyitott tételek:** N-F107a, N-F107b; átadandó: a TSV cseréje és az olvasók átállása (`/befogad`).

`scope=F107 zárás-előkészítés | forras=a napló 1–8. szakasza, git log F107.0–F107.43, python eszkozok/feladatok.py ellenoriz / fuggesek | ts=2026-10-18`
