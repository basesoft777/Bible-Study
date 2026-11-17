# -*- coding: utf-8 -*-
"""
karoli_strong_szovegek.py -- a Károli 1908 – Strong szóillesztés nyílt mag nyilvános szövegeinek prózája (F175).

Csak sablonok: a `{…}` mezőket a `karoli_strong_export.py` `fmt()` függvénye tölti ki az adatból és a mérőtáblákból;
szám kézzel nem kerül a szövegbe. A kész szövegeket a `karoli_strong_kapu.py` NYILVANOS pontja ellenőrzi (belső
jelölés, tiltott szavak, harmadik fél neve).

A fájlok útja az új szerkezet szerinti (`karoli_csomag.py`): gyökér, `data/`, `docs/hu|en/`. A rövid közlemény a csomagon kívül áll (`kozlemeny/note/karoli_strong/`).
"""
from karoli_csomag import attribucio_nyelvek

# ----------------------------------------------------------------------------- kódkönyv

KODKONYV_FAJLOK = [
    ('parok', '`data/parok/NN_Konyv.tsv`'),
    ('szavak', '`data/szavak/NN_Konyv.tsv`'),
    ('versek', '`data/versek.tsv`'),
    ('meres', '`data/meres.tsv`'),
]

KODKONYV_SOROK = [
    # fajl, oszlop, ertek, hu, en
    ('parok', 'osis', '', 'A vers OSIS-azonosítója (könyv.fejezet.vers), a Károli-versszámozás szerint.',
     'OSIS verse identifier (book.chapter.verse), in Károli versification.'),
    ('parok', 'token', '', 'A magyar szó sorszáma a versben (1-től; az írásjel nem szó).',
     'Position of the Hungarian word in the verse (from 1; punctuation is not a word).'),
    ('parok', 'alak_1908', '', 'A magyar szó alakja a Károli 1908-as szövegében.', 'Word form in the 1908 Károli text.'),
    ('parok', 'eredeti_token', '', 'Az eredeti szó sorszáma a TAHOT/TAGNT versében, a Károli-vers kulcsán (l. docs/hu/MODSZER.md 3.); a héber előtag és rag külön szónak számít.',
     'Position of the source word in the TAHOT/TAGNT verse, keyed to the Károli verse (see docs/en/METHODS.md 3); Hebrew prefixes and suffixes count as separate words.'),
    ('parok', 'strong', '', 'Az eredeti szó Strong-száma (H… héber, G… görög) a STEPBible TAHOT/TAGNT szerint; „+” két számot köt össze, ha a forrás egy szóhoz kettőt ad. A modell nem ír Strong-számot: a szám a sorszámból jön.',
     "Strong's number of the source word (H… Hebrew, G… Greek) from STEPBible TAHOT/TAGNT; \"+\" joins two numbers where the source gives two for one word. The model writes no Strong's number: it comes from the position."),
    ('parok', 'kapcsolat', 'szo', 'A pár egy eredeti szóhoz köti a magyar szót.', 'The pair links the Hungarian word to a source word.'),
    ('parok', 'kapcsolat', 'morfema', 'A pár egy héber előtag- vagy ragmorfémához köti (H9001–H9049: névelő, kötőszó, elöljáró, személyrag).',
     'The pair links it to a Hebrew prefix or suffix morpheme (H9001–H9049: article, conjunction, preposition, pronominal suffix).'),
    ('parok', 'allapot', 'javaslat', 'Gépi párosítási javaslat, mért pontossággal; nem kézzel ellenőrzött pár.',
     'Machine alignment proposal with measured accuracy; not a manually verified pair.'),
    ('parok', 'nem_tr', 'igen', 'Az eredeti görög szó nem szerepel a Textus Receptusban, amelyet Károli fordított; a Strong-szám a kritikai szöveg alakjáé (l. docs/hu/ISMERT_HIBAK.md).',
     'The Greek source word is not in the Textus Receptus, which Károli translated; the Strong number is that of the critical-text form (see docs/en/KNOWN_ISSUES.md).'),
    ('szavak', 'osis', '', 'A vers OSIS-azonosítója, a Károli-versszámozás szerint.', 'OSIS verse identifier, in Károli versification.'),
    ('szavak', 'oldal', 'hu', 'Magyar szó (Károli 1908).', 'Hungarian word (Károli 1908).'),
    ('szavak', 'oldal', 'er', 'Eredeti szó (héber vagy görög, TAHOT/TAGNT); az alakja nincs a csomagban, a sorszáma és a Strong-száma azonosítja.',
     'Source word (Hebrew or Greek, TAHOT/TAGNT); its form is not in the package, it is identified by its position and Strong number.'),
    ('szavak', 'token', '', 'A szó sorszáma a versben, az oldalán belül (1-től). Minden magyar és minden eredeti szó pontosan egy sorban áll.',
     'Position of the word in the verse, on its side (from 1). Every Hungarian and every source word appears in exactly one row.'),
    ('szavak', 'alak_1908', '', 'A magyar szó alakja; az eredeti szónál üres.', 'Form of the Hungarian word; empty for a source word.'),
    ('szavak', 'allapot', 'parositva', 'A szónak van párja a másik oldalon (l. partner_token).', 'The word has a pair on the other side (see partner_token).'),
    ('szavak', 'allapot', 'betoldas', 'Magyar szó eredeti megfelelő nélkül: a fordító betoldása, önálló névelő, segédige, kitett alanyi névmás.',
     "Hungarian word without a source counterpart: translator's addition, article, auxiliary, explicit subject pronoun."),
    ('szavak', 'allapot', 'forditatlan', 'Eredeti szó magyar megfelelő nélkül (pl. a héber tárgyjelölő, a névelő, ha a magyar nem fordítja).',
     'Source word without a Hungarian counterpart (e.g. the Hebrew object marker, an article the Hungarian does not render).'),
    ('szavak', 'allapot', 'fuggoben', 'A vers párosítása kézi döntésre vár (a versek megfeleltetése szavanként nem állt össze, vagy a válasz nem ment át a gépi kapun); pár nincs.',
     'The verse awaits a manual alignment decision (the verse mapping did not hold word by word, or the answer did not pass the machine gate); no pair.'),
    ('szavak', 'partner_token', '', 'A pár(ok) sorszáma a másik oldalon, vesszővel elválasztva.', 'Position(s) of the pair(s) on the other side, comma-separated.'),
    ('szavak', 'strong', '', 'Eredeti szónál a saját Strong-száma; magyar szónál a partnerei Strong-számai „+”-szal fűzve.',
     "For a source word its own Strong number; for a Hungarian word the Strong numbers of its partners joined by \"+\"."),
    ('versek', 'osis', '', 'A vers OSIS-azonosítója, a Károli-versszámozás szerint.', 'OSIS verse identifier, in Károli versification.'),
    ('versek', 'szoveg_1908', '', 'A vers Károli 1908 szövege, írásjelekkel; a szavak sorszáma ebből számolódik.',
     'The 1908 Károli text of the verse, with punctuation; word positions are counted on it.'),
    ('meres', 'szakasz', 'reteg', 'Rétegenkénti (könyvcsoportonkénti) egyezés a vak ellenőrrel: rétegenként egyszerű véletlen minta; Mózes öt könyvében két részminta, a pársúlyukkal összegezve.',
     'Agreement with the blind reviewer per stratum (book group): a simple random sample per stratum; in the five books of Moses two subsamples, combined by their pair weight.'),
    ('meres', 'szakasz', 'sulyozott', 'A rétegek pársúlyával súlyozott becslés (ÓSZ, ÚSZ, összes).',
     'Estimate weighted by the pair share of the strata (OT, NT, all).'),
    ('meres', 'szakasz', 'bontas', 'Kapcsolattípus szerinti bontás (tartalmi szó, morféma), leíró.',
     'Breakdown by link type (content word, morpheme), descriptive.'),
    ('meres', 'szakasz', 'hibatipus', 'A vak ellenőrtől eltérő párok típus szerint (`<réteg>:<típus>`; n = az eltérések száma a rétegben).',
     'Pairs differing from the blind reviewer, by type (`<stratum>:<type>`; n = number of differences in the stratum).'),
    ('meres', 'szakasz', 'leiro', 'Leíró szám, nem a pontosság része (hianyzo_par: ahol a vak ellenőr több eredeti szót jelölt).',
     'Descriptive count, not part of the accuracy (hianyzo_par: where the blind reviewer marked more source words).'),
    ('meres', 'szakasz', 'kalibracio', 'A vak ellenőr és a gépi pár egyezése egy korábbi, kézzel összeállított mintával.',
     'Agreement of the blind reviewer and of the machine pair with an earlier manually compiled sample.'),
    ('meres', 'szakasz', 'kulso', 'Összevetés egy független, Strong-számos Károli-kiadással, a fő szavak párjain (`_haromutas`: az eltérések háromutas ítélete után).',
     'Comparison with an independent Károli edition carrying Strong numbers, on main-word pairs (`_haromutas`: after the three-way judgement of the differences).'),
    ('meres', 'cimke', '', 'A sor tárgya: réteg (OSZ_mozes: Mózes öt könyve; OSZ_tortenet: történeti könyvek; OSZ_koltoi: költői könyvek; OSZ_profeta: próféták; USZ_evangelium: evangéliumok és Apostolok cselekedetei; USZ_level: levelek; USZ_jelenesek: Jelenések), csoport vagy hibatípus (folos_par, szomszedos_token, rossz_szo_a_versben, azonos_lexema_mas_elofordulas).',
     'Subject of the row: stratum (OSZ_mozes: the five books of Moses; OSZ_tortenet: historical books; OSZ_koltoi: poetic books; OSZ_profeta: prophets; USZ_evangelium: Gospels and Acts; USZ_level: Epistles; USZ_jelenesek: Revelation), group or error type (folos_par = superfluous pair, szomszedos_token = neighbouring word, rossz_szo_a_versben = wrong word in the verse, azonos_lexema_mas_elofordulas = same lexeme, other occurrence).'),
    ('meres', 'n', '', 'A mért párok száma.', 'Number of pairs measured.'),
    ('meres', 'x', '', 'Az egyező (helyes) párok száma; hibatípusnál az adott típusú eltérések száma.',
     'Number of agreeing (correct) pairs; for an error type, the number of differences of that type.'),
    ('meres', 'p', '', 'Arány (x / n; a súlyozott soroknál és a Mózes-rétegnél a súlyozott becslés).', 'Proportion (x / n; for weighted rows and the Moses stratum the weighted estimate).'),
    ('meres', 'also95', '', 'A 95%-os konfidencia-intervallum alsó széle.', 'Lower bound of the 95% confidence interval.'),
    ('meres', 'felso95', '', 'A 95%-os konfidencia-intervallum felső széle.', 'Upper bound of the 95% confidence interval.'),
    ('meres', 'modszer', 'wilson95', 'Wilson-intervallum.', 'Wilson interval.'),
    ('meres', 'modszer', 'retegzett_normal95', 'Rétegzett becslés, normál közelítésű intervallum.', 'Stratified estimate, normal-approximation interval.'),
    ('meres', 'modszer', 'retegzett_leiro', 'Rétegzett (a réteg teljes súlyával), leíró.', 'Stratified (with the full weight of the stratum), descriptive.'),
    ('meres', 'modszer', 'darab', 'Darabszám, intervallum nélkül.', 'Count, without interval.'),
]

# ----------------------------------------------------------------------------- olvass el / readme

OLVASSEL = """# {cim} — nyílt adatkészlet

A Károli Gáspár-féle bibliafordítás 1908-as szövege, szavanként összekapcsolva a héber és görög eredeti szavakkal és
azok Strong-számaival. A {lex_hu} nyílt adatmagjainak egyike.

A csomag minden fájlja a kiadás része.

- **Licenc:** CC BY 4.0 (`LICENSE`); a felhasznált külső adatok forrásmegjelölése: `docs/hu/ATTRIBUCIO.md`.
- **DOI:** {doi} — a kiadás azonosítója és a tartalmi hash: `KIADAS.txt`.
- **Szerző:** {szerzo} (ORCID {orcid}).

## Tartalom

| fájl | tartalom |
|---|---|
| `data/parok/NN_Konyv.tsv` | könyvenként minden szópár: magyar szó – eredeti szó, Strong-számmal |
| `data/szavak/NN_Konyv.tsv` | könyvenként minden magyar és minden eredeti szó, egyszer: párosított, betoldás, fordítatlan vagy függőben |
| `data/versek.tsv` | a Károli 1908 szövege versenként |
| `data/meres.tsv` | a párosítás mért pontossága rétegenként és kapcsolattípusonként, konfidencia-intervallummal |
| `data/kodkonyv.tsv`, `docs/hu/KODKONYV.md`, `docs/en/CODEBOOK.md` | az oszlopok és az értékek leírása (magyarul és angolul) |
| `docs/hu/MODSZER.md`, `docs/en/METHODS.md` | hogyan készült a párosítás, és hogyan mértük |
| `docs/hu/ISMERT_HIBAK.md`, `docs/en/KNOWN_ISSUES.md` | ismert hibák és korlátok |
| `docs/hu/ATTRIBUCIO.md`, `docs/en/ATTRIBUTION.md` | forrásmegjelölés és licencek |
| `CITATION.cff` | idézési adatok |
| `ELLENORZO_OSSZEG.sha256` | minden fájl SHA-256 összege |

## Számokban

- {konyv} könyv, {vers} vers; {hu_token} magyar és {er_token} eredeti szó (token).
- {par} szópár {hu_parositva} magyar szón ({heber_par} héber, {gorog_par} görög pár; ebből {morfema} héber
  előtag- vagy ragmorféma).
- {hu_betoldas} magyar szó a fordító betoldása, {er_forditatlan} eredeti szót a Károli nem fordít külön szóval;
  {hu_fuggoben} magyar és {er_fuggoben} eredeti szó párosítása függőben van ({fuggoben_vers} versben).
- Pontosság: a fő szavak párjain egy független forrás szerint {k_fs}% (95%: {k_fs_a}–{k_fs_f}%); a teljes
  párkészleten a vak ellenőrrel {p_osszes}% (95%: {p_osszes_a}–{p_osszes_f}%); részletesen: `data/meres.tsv`,
  `docs/hu/MODSZER.md` 5.

## Rövid használati útmutató

A kulcs a vers OSIS-azonosítója (`Gen.1.1`) és a szó sorszáma a versen belül (`token`). A `parok` tábla minden sora egy
kapcsolat; egy magyar szó annyi sorban áll, ahány eredeti szóhoz tartozik. A `szavak` tábla minden szót pontosan egyszer
sorol fel, a két oldalon külön (`oldal` = `hu` vagy `er`): innen olvasható ki, mi maradt pár nélkül. A héber és görög
szóalak nincs a csomagban; az eredeti szót a sorszáma és a Strong-száma azonosítja, és a sorszám a STEPBible
TAHOT/TAGNT szövegéhez illeszthető.

Minden pár gépi javaslat (`allapot` = `javaslat`), a fent megadott mért pontossággal; a pontosság rétegenként és
kapcsolattípusonként a `data/meres.tsv`-ben áll.

{egyutt}

## Kapcsolódó adatkészletek

- Modernizált Károli – Strong (ugyanezek a párok a modernizált szövegen): https://doi.org/{doi_modern}
- A {lex_hu} nyílt adatmagja (motívumok): https://doi.org/{doi_mag}
"""

README = """# {cim_en} — open dataset

The 1908 text of the Károli Bible (the classic Hungarian translation), linked word by word to the Hebrew and Greek
source words and their Strong's numbers. One of the open data cores of the {lex_en}.

Every file of the package is part of the release. Hungarian-language introduction: `docs/hu/OLVASSEL.md`.

- **Licence:** CC BY 4.0 (`LICENSE`); attribution of the third-party data used: `docs/en/ATTRIBUTION.md`.
- **DOI:** {doi} — release identifier and content hash: `RELEASE.txt`.
- **Author:** {szerzo} (ORCID {orcid}).

## Contents

| file | content |
|---|---|
| `data/parok/NN_Book.tsv` | per book, every word pair: Hungarian word – source word, with Strong's number |
| `data/szavak/NN_Book.tsv` | per book, every Hungarian and every source word once: aligned, addition, untranslated or pending |
| `data/versek.tsv` | the 1908 Károli text, verse by verse |
| `data/meres.tsv` | the measured accuracy of the alignment per stratum and link type, with confidence intervals |
| `data/kodkonyv.tsv`, `docs/hu/KODKONYV.md`, `docs/en/CODEBOOK.md` | description of the columns and values (Hungarian and English) |
| `docs/en/METHODS.md`, `docs/hu/MODSZER.md` | how the alignment was made and how it was measured |
| `docs/en/KNOWN_ISSUES.md`, `docs/hu/ISMERT_HIBAK.md` | known issues and limitations |
| `docs/hu/ATTRIBUCIO.md`, `docs/en/ATTRIBUTION.md` | attribution and licences |
| `CITATION.cff` | citation metadata |
| `ELLENORZO_OSSZEG.sha256` | SHA-256 checksum of every file |

## In numbers

- {konyv} books, {vers} verses; {hu_token} Hungarian and {er_token} source words (tokens).
- {par} word pairs on {hu_parositva} Hungarian words ({heber_par} Hebrew, {gorog_par} Greek pairs; of these {morfema}
  are Hebrew prefix or suffix morphemes).
- {hu_betoldas} Hungarian words are translator's additions, {er_forditatlan} source words are not rendered by a
  separate Hungarian word; {hu_fuggoben} Hungarian and {er_fuggoben} source words are pending ({fuggoben_vers} verses).
- Accuracy: on main-word pairs {k_fs}% against an independent source (95%: {k_fs_a}–{k_fs_f}%); on the full pair set
  {p_osszes}% agreement with a blind reviewer (95%: {p_osszes_a}–{p_osszes_f}%); details: `data/meres.tsv`, `docs/en/METHODS.md` 5.

## Quick guide

The key is the OSIS verse identifier (`Gen.1.1`) and the position of the word within the verse (`token`). Each row of
the `parok` table is one link; a Hungarian word appears in as many rows as source words it is linked to. The `szavak`
table lists every word exactly once, the two sides separately (`oldal` = `hu` or `er`): it shows what has no pair. The
Hebrew and Greek word forms are not in the package; a source word is identified by its position and Strong's number,
and the position matches the STEPBible TAHOT/TAGNT text.

Every pair is a machine proposal (`allapot` = `javaslat`), with the measured accuracy given above; the accuracy per
stratum and link type is in `data/meres.tsv`.

{egyutt}

## Related datasets

- Modernised Károli – Strong (the same pairs on the modernised text): https://doi.org/{doi_modern}
- The open data core of the {lex_en} (motifs): https://doi.org/{doi_mag}
"""

LICENSE = """{cim} / {cim_en}
Copyright (c) 2026 {szerzo}

A saját rész (a szópárosítás, a tokenállapotok és a mérés) licence:
The project's own part (the word alignment, the token states and the measurement) is licensed under:

Creative Commons Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/

A Károli 1908 szövege közkincs; a STEPBible TAHOT és TAGNT adatai CC BY 4.0 alatt állnak (docs/hu/ATTRIBUCIO.md).
The 1908 Károli text is in the public domain; the STEPBible TAHOT and TAGNT data are under CC BY 4.0 (docs/en/ATTRIBUTION.md).
"""

ATTRIBUCIO = """# Forrásmegjelölés és licencek / Attribution and licences

## Magyarul

| összetevő | licenc | megjegyzés |
|---|---|---|
| a szópárosítás, a tokenállapotok, a mérés | CC BY 4.0 | a projekt saját munkája ({szerzo}) |
| Károli Gáspár fordítása, 1908-as kiadás | közkincs | a szöveg kora miatt; digitális forrás: a HunKar-szöveg |
| STEPBible TAHOT (héber Ószövetség, Strong-számokkal) | CC BY 4.0 | a Strong-számok és az eredeti szó sorszáma innen |
| STEPBible TAGNT (görög Újszövetség, Strong-számokkal) | CC BY 4.0 | a Strong-számok, az eredeti szó sorszáma és a Textus Receptus-jelölés innen |

A TAHOT és a TAGNT kötelező forrásmegjelölése, szó szerint:

> {step}

A csomag a TAHOT és a TAGNT szövegéből semmit nem tartalmaz: a héber és görög szóalak nincs benne, csak a
Strong-szám és a szó sorszáma a versben. A pontosságmérés független összevetési forrásából csak az összesített
egyezési arány szerepel. Más külső adat nincs a csomagban.

## In English

| component | licence | note |
|---|---|---|
| the word alignment, the token states, the measurement | CC BY 4.0 | the project's own work ({szerzo}) |
| Károli Gáspár's translation, 1908 edition | public domain | by age; digital source: the HunKar text |
| STEPBible TAHOT (Hebrew Old Testament with Strong's numbers) | CC BY 4.0 | source of the Strong's numbers and source-word positions |
| STEPBible TAGNT (Greek New Testament with Strong's numbers) | CC BY 4.0 | source of the Strong's numbers, source-word positions and the Textus Receptus marking |

Required attribution of TAHOT and TAGNT, verbatim:

> {step}

The package contains none of the TAHOT or TAGNT text: no Hebrew or Greek word forms, only the Strong's number and
the position of the word in the verse. Of the independent comparison source used in the accuracy measurement, only the
aggregate agreement rate is given. No other third-party data is included.
"""

# a kétnyelvű sablon két önálló dokumentum: docs/hu/ATTRIBUCIO.md és docs/en/ATTRIBUTION.md
ATTRIBUCIO_HU, ATTRIBUCIO_EN = attribucio_nyelvek(ATTRIBUCIO)

CITATION = """cff-version: 1.2.0
message: "Ha az adatokat használja, kérjük, ezt az adatkészletet idézze. / If you use the data, please cite this dataset."
type: dataset
title: "{cim} / {cim_en}"
authors:
  - family-names: "Demeter"
    given-names: "Tamás"
    orcid: "https://orcid.org/{orcid}"
doi: "{doi}"
license: CC-BY-4.0
abstract: >-
  A Károli-biblia 1908-as szövege szavanként összekapcsolva a héber és görög
  eredeti szavakkal és azok Strong-számaival (STEPBible TAHOT/TAGNT, CC BY
  4.0): gépi párosítás, rétegenként és kapcsolattípusonként mért pontossággal.
  (English) The 1908 Károli Bible text aligned word by word to the Hebrew and
  Greek source words and their Strong's numbers (STEPBible TAHOT/TAGNT, CC BY
  4.0): a machine alignment with accuracy measured per stratum and link type.
keywords:
  - Károli-biblia
  - Strong-számok
  - szópárosítás
  - Hungarian Bible
  - word alignment
  - Strong's numbers
references:
  - type: dataset
    title: "Modernizált Károli – Strong / Modernised Károli – Strong"
    authors:
      - family-names: "Demeter"
        given-names: "Tamás"
    doi: "{doi_modern}"
  - type: dataset
    title: "{cim_mag_hu} / {cim_mag_en}"
    authors:
      - family-names: "Demeter"
        given-names: "Tamás"
    doi: "{doi_mag}"
"""

GITATTRIBUTES = """# Sorvég: minden fájl LF-fel, minden checkouton (az ellenőrző összeg az LF-es bájtokra szól).
* text eol=lf
"""

# ----------------------------------------------------------------------------- ismert hibák

ISMERT_HIBAK = """# Ismert hibák és korlátok

*{cim} · 1. kiadás · adatállapot: {adatallapot}*

Ez a kiadás a párosítást a mérés pillanatában álló állapotban adja közre, változatlanul. A lent felsorolt hibák
javítása a 2. kiadásba kerül, új méréssel (`docs/hu/MODSZER.md` 7.).

## Megerősített hibák

1. **Öt megerősített párhiba, négy helyen (a Péld 3:18-ban kettő)** a mintában és az összevetett fejezetekben: Péld 3:18 (az „Életnek” és a „fája” párja
   felcserélt, két pár), Ez 43:13 („közsinget”: a pár más szóra tartozik), 2Kir 10:15 (a kérdő „-é” a kérdő
   partikula, H9008, nem H3426), Róm 1:12 („Azaz”: a G1161 fordítatlan, nem része a párnak).

## Rendszerszintű hibák

2. **Szomszédos szó.** A vak ellenőrtől eltérő {elteres} mintapárból {h_szomszedos_token} „szomszédos token”: a gépi pár
   eredeti szava az ellenőr által jelölt szó szomszédja. Gyakran a héber kötőszó-előtag, névelő vagy elöljáró
   hozzákötése a szóhoz a párosítási szabályok ellenére; a címke azonban valódi felcserélést és ellenőri tévedést is
   takar. Típusonként: rossz szó a versben {h_rossz_szo_a_versben}, fölös pár {h_folos_par}, azonos lexéma más
   előfordulása {h_azonos_lexema_mas_elofordulas}.
3. **A morfémák mérése.** A héber előtag- és ragmorfémák párjai ({morfema} pár, a héber párok {heber_morfema_arany}%-a)
   csak a vak ellenőrrel mértek: {p_morf}% (95%: {p_morf_a}–{p_morf_f}%). A független összevetési forrás ezeket nem
   jelöli, más független mérésük még nincs.
4. **Hiányzó párok** (leíró, nem a pontosság része): a mintában {hianyzo_par} szónál jelölt a vak ellenőr több eredeti
   szót, mint a gépi párosítás.

## Korlátok

5. **Függőben lévő versek:** {fuggoben_vers} versben ({hu_fuggoben} magyar és {er_fuggoben} eredeti szó) a két szöveg
   versbeosztása szavanként nem illeszthető; ezek a szavak pár nélkül, `fuggoben` állapotban állnak.
6. **A görög szövegváltozat:** a Károli a Textus Receptust fordította, a párosítás alapja a TAGNT, amely több kiadás
   szövegét tartalmazza. {nem_tr_token} párosított görög szó ({nem_tr} pár) nem szerepel a Textus Receptusban: ott a
   Textus Receptus más alakot olvas, és a pár a kritikai szöveg alakjához kötött. A `nem_tr` oszlop jelöli őket.
7. **A mérés korlátai:** a vak ellenőr maga is nyelvi modell, és egy korábbi, kézzel összeállított mintán nem
   pontosabb a párosításnál ({kal_ell}% és {kal_gep}%); az egyezés ezért csak akkor alsó becslés, ha a közös hiba
   elhanyagolható. A független összevetés {kulso_fejezet} teljes fejezeten, a fő szavak párjain készült; a fejezetek
   klaszterek, nem véletlen mintaelemek, így az intervallum alulbecsüli a bizonytalanságot.

A kiadás a `KIADAS.txt` azonosítójával idézhető.
"""

KNOWN_ISSUES = """# Known issues and limitations

*{cim_en} · release 1 · data state: {adatallapot}*

This release publishes the alignment as it stood when it was measured, unchanged. Corrections of the issues below go
into release 2, with a new measurement (`docs/en/METHODS.md` 7).

## Confirmed errors

1. **Five confirmed pair errors, in four places (two in Prov 3:18)** in the sample and the compared chapters: Prov 3:18 (the pairs of "Életnek" and "fája"
   are swapped, two pairs), Ezek 43:13 ("közsinget": the pair belongs to another word), 2Kgs 10:15 (the
   interrogative "-é" is the interrogative particle, H9008, not H3426), Rom 1:12 ("Azaz": G1161 is untranslated and not
   part of the pair).

## Systematic errors

2. **Neighbouring word.** Of the {elteres} sample pairs differing from the blind reviewer, {h_szomszedos_token} are
   "neighbouring word" cases: the machine pair's source word is next to the one the reviewer marked. Often a Hebrew
   conjunction prefix, article or preposition attached to the word against the alignment rules; but the label also
   covers real swaps and reviewer mistakes. By type: wrong word in the verse {h_rossz_szo_a_versben}, superfluous pair
   {h_folos_par}, same lexeme at another occurrence {h_azonos_lexema_mas_elofordulas}.
3. **Measuring morphemes.** Pairs of Hebrew prefix and suffix morphemes ({morfema} pairs, {heber_morfema_arany}% of the
   Hebrew pairs) were measured by the blind reviewer only: {p_morf}% (95%: {p_morf_a}–{p_morf_f}%). The independent
   comparison source does not mark them, and no other independent measurement exists yet.
4. **Missing pairs** (descriptive, not part of the accuracy): in the sample, for {hianyzo_par} words the blind reviewer
   marked more source words than the machine alignment.

## Limitations

5. **Pending verses:** in {fuggoben_vers} verses ({hu_fuggoben} Hungarian and {er_fuggoben} source words) the verse
   division of the two texts cannot be matched word by word; these words have no pair and are marked `fuggoben`.
6. **Greek text form:** Károli translated the Textus Receptus, while the alignment uses TAGNT, which covers several
   editions. {nem_tr_token} aligned Greek words ({nem_tr} pairs) are not in the Textus Receptus: there the Textus
   Receptus reads another form, and the pair is linked to the critical-text form. The `nem_tr` column marks them.
7. **Limits of the measurement:** the blind reviewer is itself a language model, and on an earlier manually compiled
   sample it is not more accurate than the alignment ({kal_ell}% and {kal_gep}%); the agreement is a lower bound only
   if shared errors are negligible. The independent comparison covers {kulso_fejezet} full chapters, on main-word
   pairs; the chapters are clusters, not random sample units, so the interval understates the uncertainty.

A release is cited by its identifier in `RELEASE.txt`.
"""

# ----------------------------------------------------------------------------- módszer

MODSZER = """# Módszer — a Károli 1908 és az eredeti szöveg szavankénti párosítása

*{cim} · {lex_hu} · 1. kiadás · adatállapot: {adatallapot} · DOI: {doi}*

## 1. Mi ez az adatkészlet

Károli Gáspár fordításának 1908-as szövege, szavanként összekapcsolva a héber és görög eredeti szöveg szavaival. A
kapcsolat hordozója a Strong-szám: egy magyar szó Strong-számait az a héber vagy görög szó adja, amelyet fordít. A
csomag {konyv} könyvet, {vers} verset, {hu_token} magyar és {er_token} eredeti szót, valamint {par} szópárt tartalmaz.

A párosítás nyelvi modell javaslata, mért pontossággal. Nem kézzel ellenőrzött adat: minden pár „javaslat” állapotú,
és a csomag megadja, mennyire bízhat benne az, aki használja — rétegenként, kapcsolattípusonként, konfidencia-intervallummal
(5.).

## 2. A két szöveg

A magyar oldal a Károli 1908 közkincs szövege. Az eredeti oldal a STEPBible két adatkészlete: a TAHOT (héber és arámi
Ószövetség) és a TAGNT (görög Újszövetség), mindkettő szavanként Strong-számmal és angol tükörfordítással. A TAHOT a
héber szót előtagjaira és ragjaira bontja: a kötőszó (*ve-*), a névelő, az elöljáró és a személyrag külön szóként, külön
számmal áll (H9001–H9049). Ezért egy magyar szóhoz gyakran több eredeti „szó” tartozik: a *Kezdetben* az elöljáróhoz és
a főnévhez is.

A szavakra bontás mindkét oldalon determinisztikus; az írásjel nem szó. Egy szót a vers és a versen belüli sorszáma
azonosít, oldalanként külön.

## 3. A versek megfeleltetése

A Károli versbeosztása helyenként eltér a héber és a görög szövegétől (főként a fejezethatárokon). A párosítás
előtt minden Károli-vershez megkerestük a neki megfelelő eredeti verset: a versek hosszának determinisztikus
igazításával, és ahol két vers egybe olvadt, kézi jóváhagyással. Az eredeti szavak ezért a Károli-vers kulcsán állnak;
az `eredeti_token` a megfeleltetett eredeti vers szavainak sorszáma.

## 4. A párosítás menete

**A feladat.** A modell versenként megkapta a magyar szavakat sorszámozva és az eredeti szavakat sorszámozva, alakkal,
Strong-számmal és angol tükörfordítással. Azt kellett megadnia, melyik magyar szó melyik eredeti szó(ka)t fordítja;
mely magyar szavaknak nincs eredetije (betoldás); és mely eredeti szavaknak nincs magyar megfelelője (fordítatlan). A
modell **Strong-számot nem ír**, csak sorszámokat: a Strong-szám a sorszámból, a forrásból jön. Így a modell nem találhat
ki számot.

**A szabályok.** A vitás esetekre írott szabálykészlet döntött, egy korábbi párosítási minta konvencióiból. A
fontosabbak: a magyar önálló névelő betoldás, a héber és görög névelő fordítatlan, kivéve, ha névmásként áll; a
kettéírt kötőszó és vonatkozó névmás (*a mely, a ki*) mindkét szava a közös eredetihez tartozik; a héber tárgyjelölő
fordítatlan, a tárgyi névmás a ragjához kötődik; a birtokos rag ahhoz a magyar szóhoz tartozik, amelyik a megfelelő
személyragot viseli; a különírt igekötő az ige eredetijéhez tartozik; a kitett alanyi névmás és a segédigei *vala* betoldás,
ha az eredetiben nincs külön szó; a héber *ve-* csak akkor kötődik, ha a magyarban a helyén kötőszó áll; a Textus
Receptusban nem szereplő görög szó fordítatlan.

**A gépi kapu.** Minden választ program ellenőrzött: minden magyar szó pontosan egyszer szerepel (párban vagy
betoldásként), minden eredeti szó legalább egyszer (párban vagy fordítatlanként), csak létező sorszám áll benne, és a
vers teljes. A kapun bukott választ a modell újra elkészítette. Ahol a versek megfeleltetése szavanként nem állt össze, vagy a
válasz végleg nem ment át a kapun, a vers kézi átnézésre vár: minden szava `fuggoben`, pár nélkül ({fuggoben_vers}
vers).

**A modell.** A szópárosítást nyelvi modell (Claude Sonnet) javasolta, minden könyvben ugyanazzal a feladatleírással.
A feladatleírás a futás alatt változatlan volt; a táblák a mentett modellválaszokból, újabb modellhívás nélkül, bájtra
azonosan újraépíthetők.

**Az eredmény.** {hu_parositva} magyar szónak van párja, {hu_betoldas} betoldás; {er_parositva} eredeti szó párosított,
{er_forditatlan} fordítatlan. A {par} párból {heber_par} héber és {gorog_par} görög; {morfema} egy héber előtag- vagy
ragmorféma párja.

## 5. A pontosság mérése

A pontosságot két, egymást kiegészítő úton mértük.

**Vak ellenőrzés, rétegzett mintán.** A {par} párt könyvcsoportonként {reteg_db} rétegre osztottuk (Mózes öt könyve; a
történeti, a költői és a prófétai könyvek; az evangéliumok és az Apostolok cselekedetei; a levelek; a Jelenések), és
rétegenként {reteg_n} párt húztunk véletlenszerűen; Mózes öt könyvéből {rn_OSZ_mozes} párt, két részmintában, amelyeket
a becslés a pársúlyuk szerint összegez. Egy második nyelvi modell (Claude Opus) a minta minden céljára a vers szövegéből
és az eredeti szavakból maga jelölte ki a megfelelő eredeti szavakat, ugyanazokkal a szabályokkal, a gépi pár ismerete
nélkül. A pár helyes, ha az eredeti szava az ellenőr jelölései között van.

| réteg | n | helyes | arány | 95% |
|---|---|---|---|---|
| Mózes öt könyve | {rn_OSZ_mozes} | {rx_OSZ_mozes} | {r_OSZ_mozes}% | {r_OSZ_mozes_a}–{r_OSZ_mozes_f}% |
| történeti könyvek | {rn_OSZ_tortenet} | {rx_OSZ_tortenet} | {r_OSZ_tortenet}% | {r_OSZ_tortenet_a}–{r_OSZ_tortenet_f}% |
| költői könyvek | {rn_OSZ_koltoi} | {rx_OSZ_koltoi} | {r_OSZ_koltoi}% | {r_OSZ_koltoi_a}–{r_OSZ_koltoi_f}% |
| próféták | {rn_OSZ_profeta} | {rx_OSZ_profeta} | {r_OSZ_profeta}% | {r_OSZ_profeta_a}–{r_OSZ_profeta_f}% |
| evangéliumok, Apostolok cselekedetei | {rn_USZ_evangelium} | {rx_USZ_evangelium} | {r_USZ_evangelium}% | {r_USZ_evangelium_a}–{r_USZ_evangelium_f}% |
| levelek | {rn_USZ_level} | {rx_USZ_level} | {r_USZ_level}% | {r_USZ_level_a}–{r_USZ_level_f}% |
| Jelenések | {rn_USZ_jelenesek} | {rx_USZ_jelenesek} | {r_USZ_jelenesek}% | {r_USZ_jelenesek_a}–{r_USZ_jelenesek_f}% |
| **Ószövetség, súlyozott** | {n_osz} | | {p_osz}% | {p_osz_a}–{p_osz_f}% |
| **Újszövetség, súlyozott** | {n_usz} | | {p_usz}% | {p_usz_a}–{p_usz_f}% |
| **összes, súlyozott** | {n_osszes} | | **{p_osszes}%** | {p_osszes_a}–{p_osszes_f}% |

A súlyozott becslés a rétegek pársúlyával számol; Mózes öt könyvének aránya is ilyen becslés (a két részmintáé), ezért
nem a helyes párok és az n hányadosa. Kapcsolattípus szerint: a tartalmi szavak párjai {p_tartalmi}%
(95%: {p_tartalmi_a}–{p_tartalmi_f}%), a héber morfémák párjai {p_morf}% (95%: {p_morf_a}–{p_morf_f}%).

**Kalibráció.** Az ellenőr nem tévedhetetlen. Egy korábbi, kézzel összeállított mintán ({kal_ell_n} mérhető eset) az
ellenőr {kal_ell}%-ban (95%: {kal_ell_a}–{kal_ell_f}%), a gépi párosítás {kal_gep}%-ban (95%: {kal_gep_a}–{kal_gep_f}%)
egyezett vele: az ellenőr nem pontosabb a párosításnál. Az eltérések egy része tehát az ellenőr hibája, és az egyezés
csak akkor alsó becslés, ha a közös (gépi és ellenőri) hiba elhanyagolható.

**Független összevetés.** Ezt a közös hibát egy független forrás méri: egy Strong-számokkal jelölt Károli-kiadás,
amelyet a csomag nem tartalmaz, és amelyből csak az összesített egyezés szerepel itt. Rétegenként egy, Mózes öt könyvében két teljes
fejezetet vetettünk össze ({kulso_fejezet} fejezet, {k_n} fő szó párja). A forrás szavanként egy fő Strong-számot jelöl, a ragban,
elöljáróban és névelőben álló mellékszót és a morfémát nem; ez a mérés tehát csak a fő szavak párjaira érvényes.

- A forrás ítéletét elfogadva a fő szavak párjainak {k_fs}%-a egyezik (95%: {k_fs_a}–{k_fs_f}%; Ószövetség {ko_fs}%,
  Újszövetség {ku_fs}%).
- A {k_elter} eltérést háromutasan ítéltük meg (gépi pár, forrás, vak ellenőr); ezek után {k_mi} maradt a párosítás
  hibája, a fő szavak pontossága így {k_h3}% (95%: {k_h3_a}–{k_h3_f}%).
- A fejezetek klaszterek, nem véletlen mintaelemek; a valódi bizonytalanság nagyobb, mint az intervallum.

**Hibatípusok.** A {minta} mintapárból {elteres} tért el az ellenőrtől: szomszédos szó {h_szomszedos_token} (tartalmi
{ht_szomszedos_token}, morféma {hm_szomszedos_token}), rossz szó a versben {h_rossz_szo_a_versben}, fölös pár
{h_folos_par}, azonos lexéma más előfordulása {h_azonos_lexema_mas_elofordulas}. A mérés minden száma a `data/meres.tsv`-ben
áll.

## 6. Miért nyílt adat

A párosítás nem hibátlan, és nem is ekként közöljük. Szerkesztői döntés alapján nyílt adatként jelenik meg, mert a
pontossága **mérve és dokumentálva van**: rétegenként és kapcsolattípusonként, konfidencia-intervallummal, a hibák
típusával és a megerősített hibák listájával (`docs/hu/ISMERT_HIBAK.md`). A „javaslat” állapot minden páron megmarad. A közlés nem egy előre kitűzött küszöb teljesülésén alapul: a mérés előtt nem volt rögzített
kritérium, és utólag felállított küszöb utólagos kritérium volna.

## 7. A következő kiadás

Ez az 1. kiadás: a mért állapot, változatlanul. A 2. kiadás javítja a megerősített hibákat és a szomszédos szó
szabályellenes eseteit (szabályalapú utófeldolgozással, nem páronkénti folttal), majd ugyanazzal a protokollal újra
mér: rétegzett minta, vak ellenőr, független külső forrás. A 2. kiadás minőségi célját az 1. kiadás eredményeinek
ismeretében, előre rögzítettük: a független összevetés fő-szó egyezésének alsó széle legalább 98% (most {k_fs_a}%); a
vak ellenőrrel mért súlyozott egyezés alsó széle legalább 93% (most {p_osszes_a}%), és egyetlen réteg pontbecslése sem
90% alatti (most a legkisebb {r_min}%, {r_min_nev}). A cél az 1. kiadásra nem vonatkozik.

## 8. Kapcsolódó adatkészlet

Ugyanezek a párok a Károli modernizált szövegén is megjelennek (https://doi.org/{doi_modern}). A modernizálás minden
szót a helyén hagyott, ezért a két csomag a vers és a szósorszám kulcsán szóról szóra összekapcsolható.
"""

METHODS = """# Methods — word alignment of the 1908 Károli text with the source texts

*{cim_en} · {lex_en} · release 1 · data state: {adatallapot} · DOI: {doi}*

## 1. What this dataset is

The 1908 text of Károli Gáspár's translation, linked word by word to the words of the Hebrew and Greek source text. The
link is carried by Strong's numbers: the Strong's numbers of a Hungarian word are those of the Hebrew or Greek word it
translates. The package holds {konyv} books, {vers} verses, {hu_token} Hungarian and {er_token} source words, and {par}
word pairs.

The alignment is a proposal of a language model, with measured accuracy. It is not manually verified data: every pair is
in the "proposal" state, and the package states how far it can be trusted — per stratum, per link type, with
confidence intervals (5).

## 2. The two texts

The Hungarian side is the public-domain 1908 Károli text. The source side is two STEPBible datasets: TAHOT (Hebrew and
Aramaic Old Testament) and TAGNT (Greek New Testament), both with a Strong's number and an English gloss for each
word. TAHOT splits the Hebrew word into its prefixes and suffixes: the conjunction (*ve-*), the article, the preposition
and the pronominal suffix stand as separate words with their own numbers (H9001–H9049). One Hungarian word is therefore
often linked to several source "words": *Kezdetben* ("in the beginning") to both the preposition and the noun.

Tokenisation is deterministic on both sides; punctuation is not a word. A word is identified by its verse and its
position within the verse, separately on each side.

## 3. Verse mapping

Károli's verse division differs in places from that of the Hebrew and Greek text (mainly at chapter
boundaries). Before alignment, each Károli verse was matched to its source verse: by deterministic alignment of verse
lengths, with each merge of two verses approved by hand. Source words are therefore keyed to the Károli verse;
`eredeti_token` is the position within the mapped source verse.

## 4. Alignment procedure

**The task.** For each verse the model received the Hungarian words, numbered, and the source words, numbered, with
form, Strong's number and English gloss. It had to state which Hungarian word translates which source word(s); which
Hungarian words have no source (additions); and which source words have no Hungarian counterpart (untranslated). The
model **writes no Strong's number**, only positions: the number comes from the position, from the source. The model
cannot invent a number.

**The rules.** Disputed cases were decided by a written rule set, derived from the conventions of an earlier
alignment sample. The main ones: the Hungarian article is an addition, the Hebrew and Greek article is untranslated
unless it stands as a pronoun; both words of a split Hungarian conjunction or relative pronoun (*a mely, a ki*) go to
the common source word; the Hebrew object marker is untranslated, and the object pronoun links to its suffix; a
possessive suffix belongs to the Hungarian word that carries the matching personal ending; a separated verbal prefix
belongs to the verb's source word; an explicit subject pronoun and the auxiliary *vala* are additions where the source
has no separate word; the Hebrew *ve-* links only where a conjunction stands in its place in Hungarian; a Greek word not
in the Textus Receptus is untranslated.

**The machine gate.** Every answer was checked by a program: each Hungarian word appears exactly once (in a pair or as an
addition), each source word at least once (in a pair or as untranslated), only existing positions occur, and the verse
is complete. An answer failing the gate was redone by the model. Where the verse mapping did not hold word by word, or the answer
finally failed the gate, the verse awaits manual review: all its words are `fuggoben`, without a pair
({fuggoben_vers} verses).

**The model.** The word alignment was proposed by a language model (Claude Sonnet), with the same task description in
every book. The task description did not change during the run; the tables can be rebuilt byte-identically from the
saved model answers, without new model calls.

**Result.** {hu_parositva} Hungarian words have a pair, {hu_betoldas} are additions; {er_parositva} source words are
aligned, {er_forditatlan} untranslated. Of the {par} pairs, {heber_par} are Hebrew and {gorog_par} Greek; {morfema}
link a Hebrew prefix or suffix morpheme.

## 5. Measuring accuracy

Accuracy was measured in two complementary ways.

**Blind review on a stratified sample.** The {par} pairs were divided by book group into {reteg_db} strata (the five
books of Moses; the historical, poetic and prophetic books; the Gospels and Acts; the Epistles; Revelation), and
{reteg_n} pairs were drawn at random per stratum; from the five books of Moses {rn_OSZ_mozes} pairs, in two subsamples
that the estimate combines by their pair weight. A second language model (Claude Opus) marked, for each target in the
sample, the matching source words from the verse text and the source words itself, with the same rules, without seeing
the machine pair. A pair is correct if its source word is among the reviewer's marks.

| stratum | n | correct | rate | 95% |
|---|---|---|---|---|
| five books of Moses | {rn_OSZ_mozes} | {rx_OSZ_mozes} | {r_OSZ_mozes}% | {r_OSZ_mozes_a}–{r_OSZ_mozes_f}% |
| historical books | {rn_OSZ_tortenet} | {rx_OSZ_tortenet} | {r_OSZ_tortenet}% | {r_OSZ_tortenet_a}–{r_OSZ_tortenet_f}% |
| poetic books | {rn_OSZ_koltoi} | {rx_OSZ_koltoi} | {r_OSZ_koltoi}% | {r_OSZ_koltoi_a}–{r_OSZ_koltoi_f}% |
| prophets | {rn_OSZ_profeta} | {rx_OSZ_profeta} | {r_OSZ_profeta}% | {r_OSZ_profeta_a}–{r_OSZ_profeta_f}% |
| Gospels, Acts | {rn_USZ_evangelium} | {rx_USZ_evangelium} | {r_USZ_evangelium}% | {r_USZ_evangelium_a}–{r_USZ_evangelium_f}% |
| Epistles | {rn_USZ_level} | {rx_USZ_level} | {r_USZ_level}% | {r_USZ_level_a}–{r_USZ_level_f}% |
| Revelation | {rn_USZ_jelenesek} | {rx_USZ_jelenesek} | {r_USZ_jelenesek}% | {r_USZ_jelenesek_a}–{r_USZ_jelenesek_f}% |
| **Old Testament, weighted** | {n_osz} | | {p_osz}% | {p_osz_a}–{p_osz_f}% |
| **New Testament, weighted** | {n_usz} | | {p_usz}% | {p_usz_a}–{p_usz_f}% |
| **all, weighted** | {n_osszes} | | **{p_osszes}%** | {p_osszes_a}–{p_osszes_f}% |

The weighted estimate uses the pair share of the strata; the rate for the five books of Moses is such an estimate too
(of its two subsamples), so it is not the ratio of correct pairs to n. By link type: content-word pairs {p_tartalmi}%
(95%: {p_tartalmi_a}–{p_tartalmi_f}%), Hebrew morpheme pairs {p_morf}% (95%: {p_morf_a}–{p_morf_f}%).

**Calibration.** The reviewer is not infallible. On an earlier manually compiled sample ({kal_ell_n} measurable cases)
the reviewer agreed with it in {kal_ell}% (95%: {kal_ell_a}–{kal_ell_f}%), the machine alignment in {kal_gep}% (95%:
{kal_gep_a}–{kal_gep_f}%): the reviewer is not more accurate than the alignment. Part of the differences are thus the
reviewer's errors, and the agreement is a lower bound only if shared (machine and reviewer) errors are negligible.

**Independent comparison.** Shared errors are measured by an independent source: a Károli edition marked with Strong's
numbers, which the package does not contain and of which only the aggregate agreement is given here. One full chapter
per stratum, two in the five books of Moses, was compared ({kulso_fejezet} chapters, {k_n} main-word pairs). The source marks one main Strong's number
per word, not the secondary word in a suffix, preposition or article, nor the morpheme; this measurement applies to
main-word pairs only.

- Accepting the source's judgement, {k_fs}% of main-word pairs agree (95%: {k_fs_a}–{k_fs_f}%; Old Testament {ko_fs}%,
  New Testament {ku_fs}%).
- The {k_elter} differences were judged three ways (machine pair, source, blind reviewer); after this {k_mi} remained
  errors of the alignment, giving a main-word accuracy of {k_h3}% (95%: {k_h3_a}–{k_h3_f}%).
- The chapters are clusters, not random sample units; the true uncertainty is larger than the interval.

**Error types.** Of the {minta} sample pairs, {elteres} differed from the reviewer: neighbouring word
{h_szomszedos_token} (content {ht_szomszedos_token}, morpheme {hm_szomszedos_token}), wrong word in the verse
{h_rossz_szo_a_versben}, superfluous pair {h_folos_par}, same lexeme at another occurrence
{h_azonos_lexema_mas_elofordulas}. Every figure of the measurement is in `data/meres.tsv`.

## 6. Why open data

The alignment is not error-free, and we do not publish it as such. By editorial decision it is released as open data
because its accuracy is **measured and documented**: per stratum and link type, with confidence intervals, with the
error types and the list of confirmed errors (`docs/en/KNOWN_ISSUES.md`). The "proposal" state remains on every pair. Publication does not rest on meeting a threshold set in advance: there was no fixed criterion before the
measurement, and a threshold set afterwards would be a post-hoc criterion.

## 7. The next release

This is release 1: the measured state, unchanged. Release 2 will correct the confirmed errors and the rule-violating
neighbouring-word cases (by rule-based post-processing, not pair-by-pair patches), then measure again with the same
protocol: stratified sample, blind reviewer, independent external source. The quality target for release 2 was fixed
in advance, in knowledge of the release 1 results: the lower bound of main-word agreement in the independent comparison
at least 98% (now {k_fs_a}%); the lower bound of the weighted agreement with the blind reviewer at least 93% (now
{p_osszes_a}%), with no stratum point estimate below 90% (now the lowest is {r_min}%, {r_min_nev}). The target does
not apply to release 1.

## 8. Related dataset

The same pairs also appear on the modernised Károli text (https://doi.org/{doi_modern}). The modernisation left every
word in its place, so the two packages can be joined word by word on the verse and word position key.
"""

# ----------------------------------------------------------------------------- közlemény (tervezet)

KOZLEMENY_HU = """# A Károli-biblia szavanként az eredeti nyelvekhez kötve — mért pontossággal

*Közlemény-tervezet · {cim} · {lex_hu} · DOI: {doi}*

Aki a Károli-bibliát olvasva azt kérdezi, milyen héber vagy görög szó áll egy magyar szó mögött, eddig nem talált
olyan szabad adatot, amely ezt szavanként, mért pontossággal megmondja. A {lex_hu} most szabad licenccel közreadja a Károli 1908-as szövegének szavankénti
párosítását az eredeti szöveggel: a {par} szópár mindegyike megmondja, melyik héber vagy görög szót fordítja az adott
magyar szó, és mi a Strong-száma.

**Hogyan készült.** A párosítást nyelvi modell (Claude Sonnet) végezte, versenként, egy írott szabálykészlet szerint: mikor betoldás a
magyar névelő, hová tartozik a héber birtokos rag, mit kezdjünk a kettéírt *a mely*-vel. A modell csak azt jelölte,
melyik szó melyikhez tartozik; Strong-számot nem írt, azt a STEPBible nyílt héber és görög szövege adja. Minden választ
program ellenőrzött, hogy egy szó se maradjon ki, és egy se álljon kétszer.

**Mennyire pontos.** A párosítás nem hibátlan, és ezt nem is állítjuk. Azt állítjuk, hogy megmértük, és a mérés minden
számát közöljük. Könyvcsoportonként húzott véletlen mintán egy másik, a párokat nem látó modell {p_osszes}%-ban értett
egyet a párosítással (95%: {p_osszes_a}–{p_osszes_f}%). A fő szavak párjait egy független, Strong-számos
Károli-kiadással is összevetettük: {k_fs}% egyezett (95%: {k_fs_a}–{k_fs_f}%). A gyengébb pont a héber előtagok és ragok
párosítása ({p_morf}%), és a megerősített hibákat név szerint felsoroljuk.

**Miért most.** Mert a mérés dokumentált: aki az adatot használja, tudja, mennyire bízhat benne, rétegenként és
kapcsolattípusonként. A következő kiadás a feltárt hibákat javítja, és ugyanazzal a módszerrel újra mér; a minőségi
célját előre rögzítettük.

**Kinek.** Bibliaolvasóknak, akik a Károli egy szava mögött az eredetit keresik; kutatóknak, akik a magyar bibliai
szóhasználatot a héber és görög szöveggel együtt vizsgálják; fejlesztőknek, akik szavanként kulcsolt, szabad magyar
bibliai adatra építenének. Ugyanezek a párok a Károli modernizált szövegén is elérhetők
(https://doi.org/{doi_modern}).

Az adatkészlet CC BY 4.0 licenccel szabadon felhasználható: https://doi.org/{doi}
"""

KOZLEMENY_EN = """# The Károli Bible linked word by word to the original languages — with measured accuracy

*Announcement draft · {cim_en} · {lex_en} · DOI: {doi}*

A reader of the Károli Bible, the classic Hungarian translation, who asks which Hebrew or Greek word stands behind a
Hungarian word has so far found no free data that answers this word by word, with measured accuracy. The {lex_en} now releases, under a free licence, a word-by-word
alignment of the 1908 Károli text with the source text: each of the {par} word pairs states which Hebrew or Greek word
the Hungarian word translates, and its Strong's number.

**How it was made.** The alignment was done by a language model (Claude Sonnet), verse by verse, following a written rule set: when the
Hungarian article is an addition, where a Hebrew possessive suffix belongs, what to do with a split relative pronoun.
The model only marked which word goes with which; it wrote no Strong's numbers, which come from the open STEPBible
Hebrew and Greek text. A program checked every answer, so that no word is left out and none appears twice.

**How accurate.** The alignment is not error-free, and we do not claim it is. We claim that it has been measured, and we
publish every figure of the measurement. On a random sample drawn per book group, another model that did not see the
pairs agreed with the alignment in {p_osszes}% (95%: {p_osszes_a}–{p_osszes_f}%). Main-word pairs were also compared with
an independent Károli edition marked with Strong's numbers: {k_fs}% agreed (95%: {k_fs_a}–{k_fs_f}%). The weaker point is
the alignment of Hebrew prefixes and suffixes ({p_morf}%), and the confirmed errors are listed by name.

**Why now.** Because the measurement is documented: whoever uses the data knows how far to trust it, per stratum and per
link type. The next release corrects the errors found and measures again with the same method; its quality target was
fixed in advance.

**For whom.** For Bible readers looking for the original behind a word of the Károli; for researchers studying Hungarian
biblical vocabulary together with the Hebrew and Greek text; for developers building on free, word-keyed Hungarian Bible
data. The same pairs are also available on the modernised Károli text (https://doi.org/{doi_modern}).

The dataset is freely usable under CC BY 4.0: https://doi.org/{doi}
"""

# ----------------------------------------------------------------------------- a kiadott szövegek listája

SZOVEGEK = [
    ('docs/hu/OLVASSEL.md', OLVASSEL, 'hu'),
    ('README.md', README, 'en'),
    ('LICENSE', LICENSE, 'hu'),
    ('docs/hu/ATTRIBUCIO.md', ATTRIBUCIO_HU, 'hu'),
    ('docs/en/ATTRIBUTION.md', ATTRIBUCIO_EN, 'en'),
    ('docs/hu/MODSZER.md', MODSZER, 'hu'),
    ('docs/en/METHODS.md', METHODS, 'en'),
    ('docs/hu/ISMERT_HIBAK.md', ISMERT_HIBAK, 'hu'),
    ('docs/en/KNOWN_ISSUES.md', KNOWN_ISSUES, 'en'),
    ('CITATION.cff', CITATION, 'hu'),
]

KOZLEMENY = [
    ('note_hu.md', KOZLEMENY_HU, 'hu'),
    ('note_en.md', KOZLEMENY_EN, 'en'),
]

# ----------------------------------------------------------------------------- a második data paper kézirata (tervezet; a csomagon kívül)

# A második data paper kézirata, a Journal of Open Humanities Data (JOHD) data paper-sablonjának szerkezetében
# (Overview, Method, Dataset Description, Reuse Potential, nyilatkozatok; a sablon lekérése: 2026-11-16, l.
# kozlemeny/data_paper/folyoirat_kovetelmenyek.md). A beküldési szöveg végét a VEGE_JEL jelzi; a szószám a jel előtti
# részből számolódik (karoli_strong_export.szoszam), a jel utáni jegyzet a beküldött változatból kivehető.
# A szögletes zárójeles mezőket (az emberi validáció eredménye, e-mail, nevek) a beküldés előtt kell kitölteni.
KEZIRAT_HU = """# A Károli-biblia 1908-as szövegének szavankénti párosítása a héber és görög eredetivel: nyílt adatkészlet mért párprecizitással

*Data paper · kézirat-tervezet a Journal of Open Humanities Data számára · az adatkészlet DOI-ja: {doi}*

**Demeter Tamás**, független kutató · ORCID: https://orcid.org/{orcid} · levelező szerző: [e-mail-cím]

## Kivonat

Az adatkészlet a Károli-biblia, a klasszikus magyar fordítás 1908-as szövegének {hu_token} szavát kapcsolja a héber és
görög eredetihez (STEPBible TAHOT/TAGNT) {par} párral, mindegyik az eredeti szó Strong-számával; egy nyelvi modell csak
szósorszámokat jelölt. A párprecizitás (egyezés egy vak modell-ellenőrrel) rétegzett mintán {p_osszes}% (95%-os KI:
{p_osszes_a}–{p_osszes_f}%); az emberi validáció szerint [precizitás]; a fő szavak egyezése egy zárt, Strong-számos
kiadással, kiegészítő keresztellenőrzésként, {k_fs}%. A CC BY 4.0 licencű táblák Strong-alapú keresést szolgálnak.

**Kulcsszavak:** Károli-biblia; Strong-számok; szóillesztés; magyar; bibliai héber; koiné görög

**Szerzői szerepek (CRediT):** Demeter Tamás: Conceptualization, Methodology, Software, Data curation, Validation,
Writing – original draft, Writing – review & editing.

## 1. Áttekintés

### A tárhely helye

https://doi.org/{doi} (concept DOI; jelenlegi változat: {verzio}).

### Háttér

Az adatkészlet a szerző független kutatási projektjéből, a {lex_hu}ból származik. A Strong-számok (Strong, 1890) egy
fordítás szavait a héber és görög szókincshez kötik. A Károli-szövegnek, amely négy évszázada a magyar protestáns
bibliaolvasás alapszövege, léteznek Strong-számos kiadásai; ez a párosítás nyílt licencű, szavanként dokumentált, és a
precizitása mért. Versenként rögzíti, melyik magyar szó melyik eredeti szót adja vissza (egy–több és több–egy
kapcsolattal is), a betoldásokat és a fordítatlan eredeti szavakat.

## 2. Módszer

### Lépések

**Szövegek.** A magyar oldal a Károli 1908 közkincs szövege (HunKar), az eredeti oldal a STEPBible TAHOT (héber és
arámi Ószövetség) és TAGNT (görög Újszövetség) adata (Tyndale House, Cambridge; CC BY 4.0; commit efe428a, letöltve 2026-08-24). A
TAHOT a héber előtagokat és ragokat külön szóként számolja (H9001–H9049). A versbeosztásokat determinisztikus
vershossz-igazítás feleltette meg egymásnak; minden vers-egybeolvadást kézzel hagytunk jóvá.

**Párosítás.** Egy nyelvi modell versenként két számozott szólistát kapott: a Károli szavait, és az eredeti szavakat
alakkal, Strong-számmal és rövid angol glosszával; a Strong-szám csak tájékoztatásul állt ott, a válaszban tilos volt. A
rögzített utasítás egy kidolgozott példában egy választható, Strong-címkés KJV-sort is mutatott; versbemenet ilyet nem
tartalmazott. A modell sorszámpárokat, betoldásokat és fordítatlan szavakat adott vissza. A Józs 8:34-ben az *Azután*
(1) szót a 2–3. eredeti szóhoz (*ʾaḥărê kēn*), a *felolvasta* (3) szót a 4. szóhoz (*qārāʾ*) kötötte; a H0310, H3651 és
H7121 számot ezután program tette hozzá a sorszám alapján. A vitás eseteket tizenkét írott szabály döntötte el. A
funkciószavakra rögzített konvenció érvényes: a magyar névelő és az eredeti szó nélküli segédige betoldás, a héber és
görög névelő fordítatlan (a névelőhasználat a nyelvek között eltér); a névmásként álló névelő párosított.

**Futtatás és megismételhetőség.** Minden könyvet a claude-sonnet-5-5 párosított: a többséget az Anthropic Batch
API-n, az 1–5Mózest, a Józsuét és a Zsoltárokat ügynöki futásban. Minden
választ program ellenőrzött (minden magyar szó pontosan egyszer, minden eredeti szó legalább egyszer, csak létező
sorszám); a bukott választ a modell újra elkészítette. A modell így nem tudott Strong-számot vagy szótári tételt
kitalálni; legfeljebb rossz szót párosíthatott, és minden pár egy ellenőrizhető eredeti szóra mutat. A modellválaszok
egyszer készültek, és archiválva vannak; a párok építése, a Strong-szám hozzárendelése és a kapu determinisztikus, ezért
a táblák a válaszokból bájtra azonosan újraépíthetők, a modell újrafuttatása kis eltérést adhat.

### Mintavétel

A vak ellenőrzéshez a párkészletet könyvcsoportonként {reteg_db_szo} rétegre osztottuk (Mózes öt könyve; történeti,
költői és prófétai könyvek; evangéliumok és ApCsel; levelek; Jelenések), rétegenként {reteg_n} véletlen párral; Mózes
öt könyvében {rn_OSZ_mozes} pár két részmintából, pársúllyal összegezve. Az emberi validáció mintája [N] pár és [M] pár
nélküli szó ugyanezekből a rétegekből, és mind a {elteres} ellenőr-eltérés súlyozott túlmintaként. A zárt kiadással való
keresztellenőrzés célzottan kiválasztott fejezeteken futott: rétegenként az a fejezet, amelyben a legtöbb
ellenőr-eltérés és mintapár volt, Mózes öt könyvében kettő ({kulso_fejezet_szo} fejezet).

### Minőség-ellenőrzés

**Vak modell-ellenőrzés.** Egy második modell (Claude Opus) a mintába került magyar szóhoz maga jelölte ki az eredeti
szavakat, ugyanazokkal a szabályokkal, a gépi pár ismerete nélkül; a pár helyes, ha az eredeti szava az ellenőr
jelölései között van. A párprecizitás tehát egy modellel való egyezés, nem abszolút mérce.

**Emberi validáció.** Egy külső ellenőr, végzett teológus, bibliai héber és görög ismerettel, minden tételt megítélt;
a második ellenőr, szintén végzett teológus, a szerző családtagja; egyikük sem dolgozott az adatkészlet
előállításán. Az ítélet nem vak: az ellenőrök látják a gépi párt. A pár nélküli szavak mintájából a szabály által
meghatározott funkciószavak kimaradtak. A fő szám a külső ellenőré: precizitás [precizitás] (95%-os KI: [KI]), a
bizonytalan tételeket hibának számítva [konzervatív]. A második ellenőr száma ([precizitás 2]) és a kettejük egyezése
(kappa = [kappa]) kiegészítő adat; döntnök nincs. Az egyezés a vak modell-ellenőrrel [egyezés a modell-ellenőrrel].

**Keresztellenőrzés zárt kiadással.** Kiegészítő ellenőrzésként a párokat helyben összevetettük a Bible-Discovery
Strong-számos Károlijával (HUN modul), egy zárt licencű kiadással, amely nem terjeszthető; csak az összesített
eredmény nyilvános, és az olvasó nem ellenőrizheti. Nem mérce: magyar szavanként egy fő szót jelöl, a mi felbontásunk
részletesebb (egy–több kapcsolat, morféma, pl. *Azután* ↔ *ʾaḥărê* + *kēn*). Fő szó párja az a tartalmi pár, amelynek magyar szavához a kiadás
Strong-számot ad, és amely nem egy már egyező szó másodlagos párja: {k_osszes} párból {k_n} (kimaradt {k_nincs} a
kiadásban Strong-szám nélkül, {k_masod} másodlagos, {k_forma} nem illeszthető alak). A másodlagos párok és a
felbontási különbségek nem hibák.

| mérés | becslés | 95%-os KI |
|---|---|---|
| párprecizitás, vak modell-ellenőr, súlyozott | {p_osszes}% | {p_osszes_a}–{p_osszes_f}% |
| tartalmi szó / héber morféma | {p_tartalmi}% / {p_morf}% | {p_tartalmi_a}–{p_tartalmi_f}% / {p_morf_a}–{p_morf_f}% |
| emberi validáció (külső); a bizonytalan hibaként | [precizitás]; [konzervatív] | [KI] |
| a fő szavak egyezése, zárt kiadás | {k_fs}% | – |

A rétegek precizitása {r_min}% ({r_min_nev}) és {r_max}% ({r_max_nev}) között mozog.
A {minta} mintapárból {elteres} tért el az ellenőrtől, leggyakrabban szomszédos szóval ({h_szomszedos_token}).
A zárt kiadástól való {k_elter} eltérésből {k_mi_szo}
bizonyult párosítási hibának (háromutas ítélet; az adatkészlet felsorolja őket); a másodlagos párok nem
eltérések.

## 3. Az adatkészlet leírása

- **Tárhely neve:** Zenodo
- **Objektum neve:** `{objektum}`
- **Formátumok és változatok:** TSV (UTF-8) az adathoz és a kódkönyvhöz;
  Markdown a kétnyelvű dokumentációhoz; CFF hivatkozási fájl; SHA-256 ellenőrző összeg
- **Létrehozás dátumai:** {kezdet} – {adatallapot}
- **Az adatkészlet készítője:** Demeter Tamás (független kutató; ORCID: {orcid}): szabályok, feldolgozási lánc, mérés,
  gondozás.
- **Nyelv:** magyar (adat); magyar és angol (dokumentáció)
- **Licenc:** CC BY 4.0
- **Közzététel dátuma:** {kozzetetel}

**Tartalom.** `data/parok/` (kapcsolatonként egy sor: sorszámok, Strong-szám, kapcsolattípus, állapot, Textus
Receptus-jelölés), `data/szavak/` (minden szó egyszer, állapottal: párosított, betoldás, fordítatlan vagy függőben,
azaz még nem párosított), `data/versek.tsv`, `data/meres.tsv` (a mérés minden száma); kulcs: OSIS-vers és szósorszám.

**Méret.** {konyv} könyv, {vers} vers, {par} pár ({heber_par} héber, {gorog_par} görög; ebből {morfema} morféma),
{hu_betoldas} betoldás, {er_forditatlan} fordítatlan eredeti szó, {hu_fuggoben} függőben lévő magyar szó
({fuggoben_vers} vers).

## 4. Újrahasznosítási lehetőségek

Bibliaprogramok Strong-alapú keresést kínálhatnak a magyar szövegen. A fordítástörténet vizsgálhatja a Károli
következetességét és betoldásait. Nyelvtechnológiai célra kis erőforrású nyelvpár szóillesztési adata, rétegenként
mért hibával. A párosításra a {lex_hu}, egy motívum-indexelt, kereszthivatkozott bibliai lexikon épül. Egy kísérő
adatkészlet (Demeter, 2026b) ugyanezeket a párokat a szöveg szerző által készített, szabályalapú modernizálásán adja (a
ritka igealak csak egyező független modelljavaslatok után változott; a modernizálást külön ellenőrzés és mérés
vizsgálta): minden szó a helyén maradt, az összeolvadt szavak mindkét párja megmaradt, így a fenti számok rá is
érvényesek.

### Korlátok

A vak ellenőr maga is modell, és az emberi validáció nem vak. A párprecizitás a fordítatlan eredeti szavakat nem méri.
A zárt kiadással összevetett fejezetek célzottan kiválasztottak, és a héber morfémákat nem fedik. Az 1–2Mózesben
{nehez_par} pár ({nehez_vers} vers), amelyre a második modell (l. MI-nyilatkozat) más párt javasolt, gyengébb: a mintából
{nehez_minta} közül {nehez_helyes_szo} helyes, így nagyjából {nehez_hibas_a}–{nehez_hibas_f} lehet hibás; az 1.1-es változat ismert-hibák
listája felsorolja őket, javítás nélkül; az 1.2-es változat újrapárosítja és újra méri őket.
A Textus Receptusban, amelyet Károli fordított, nem szereplő {nem_tr_token} párosított görög szó jelölve van.

## Adat-elérhetőség

Mindkét adatkészlet nyíltan elérhető a Zenodón, CC BY 4.0 licenccel (l. Hivatkozások). Az 1.1-es változat,
amely a beküldés előtt jelenik meg, hozzáadja a promptot (naplózott hash: 84f12ca7aafb), mind a {konyv} könyv nyers
modellválaszát, a versmegfeleltetést és a vers-összevonásokat, az {minta} mintapárt az ellenőr ítéletével, az
ismert-hibák listát és az emberi ítéleteket, a STEPBible-commit és a modellazonosító rögzítésével; kódot nem.

## Köszönetnyilvánítás

A szerző köszöni [a külső ellenőr neve] és [a második ellenőr neve] munkáját az emberi validációban.

## Finanszírozás

A munka külső finanszírozás nélkül készült.

## Érdekütközés

A szerzőnek nincs bejelentendő érdekütközése.

## Hivatkozások

Demeter, T. (2026a). *Logosz Lexikon – Károli Bible (1908): Word alignment with Hebrew and Greek Strong's numbers*
(változat: {verzio}) [adatkészlet]. Zenodo. https://doi.org/{doi}

Demeter, T. (2026b). *Logosz Lexikon – Modernized Károli Bible: Word alignment with Hebrew and Greek Strong's numbers*
(változat: {verzio_modern}) [adatkészlet]. Zenodo. https://doi.org/{doi_modern}

STEPBible. (é. n.). *Translators Amalgamated Hebrew OT (TAHOT) és Translators Amalgamated Greek NT (TAGNT)*
[adatkészlet]. Tyndale House, Cambridge. https://www.STEPBible.org

Strong, J. (1890). *The exhaustive concordance of the Bible*. Hunt & Eaton.

## Nyilatkozat a mesterséges intelligencia használatáról

(1) Párosítás: a Claude Sonnet (Anthropic) csak sorszámpárokat adott vissza (l. Módszer). Az 1Móz és a 2Móz
párosításánál egy másik nyelvi modell is futott keresztellenőrzésként; egyetlen közölt pár sem csak tőle származik. (2)
Minőség-ellenőrzés: a Claude Opus a mintán vak ellenőr volt; az emberi validáció MI nélkül készült. (3) Kísérő
adatkészlet: l. Újrahasznosítás. A kézirat szövegének megfogalmazásában és
szerkesztésében a claude-opus-5-5 modell segített, az adatkészlet adataiból; a számok az adatokból generáltak. A
kutatást a szerző tervezte, minden szerkesztői döntést ő hozott, minden állítást az adatokon ellenőrzött, és a
tartalomért teljes felelősséget vállal; MI-eszköz nem szerző.

<!-- BEKÜLDÉSI SZÖVEG VÉGE — az alábbi rész a beküldött változatból kivehető. -->

---

## Beküldési jegyzet

Szószám (a beküldési szöveg angol változatában): az 1–4. szakasz, a cím, a szerzői sor, a kivonat, a táblázat és a
hivatkozások nélkül (a JOHD-sablon számítása) {szo_fo}; a számozatlan nyilatkozatokkal {szo_nyil}; a
hivatkozásokkal is {szo_hiv} (a beküldési oldal szerint a korlát a hivatkozásokat is tartalmazza; a kivonatról nem
szól); a kivonattal együtt {szo_kiv}. A JOHD data paper terjedelme 1000–1500 szó; a szerkesztőség megerősítheti, melyik
számítás érvényes. A kivonattól az MI-nyilatkozatig minden szó, a címsorokkal, a kulcsszavakkal, a szerzői
szerepekkel és a táblázattal: {szo_mind}.

Beküldés előtt kitöltendő: az emberi validáció mezői ([N], pontosság, KI, kappa, egyezés a modell-ellenőrrel), a
levelező szerző e-mail-címe, a két ellenőr neve. A szöveg a JOHD hivatalos Word- vagy LaTeX-sablonjába kerül; a
kísérőlevél: `kozlemeny/data_paper/johd_cover_letter_en.md`.
"""

# Csalik (elültetett hibás párok) a validációs mintában: a felhasználó még nem döntött róla (2026-11-17). Ha bekerülnek,
# a „Human validation” bekezdésbe egy mondat kell a csalik számáról és a felismerési arányról ([decoy detection]).
KEZIRAT_EN = """# Word-by-word alignment of the 1908 Károli Bible with the Hebrew and Greek source text: an open dataset with measured pair precision

*Data paper · submission draft for the Journal of Open Humanities Data · dataset DOI: {doi}*

**Tamás Demeter**, independent researcher · ORCID: https://orcid.org/{orcid} · corresponding author: [e-mail address]

## Abstract

The dataset aligns the {hu_token} words of the 1908 Hungarian Károli Bible with the Hebrew
and Greek source text (STEPBible TAHOT/TAGNT) in {par} pairs carrying the source word's Strong's number; a language
model marked word positions only. Pair precision (agreement with a blind model reviewer) is {p_osszes}% (95% CI
{p_osszes_a}–{p_osszes_f}%) on a stratified sample; human validation gives [precision]; main-word agreement with a
closed Strong-tagged edition, a supplementary cross-check, is {k_fs}%. The CC BY 4.0 tables support Strong-based search.

**Keywords:** Károli Bible; Strong's numbers; word alignment; Hungarian; biblical Hebrew; Koine Greek

**Author roles (CRediT):** Tamás Demeter: Conceptualization, Methodology, Software, Data curation, Validation,
Writing – original draft, Writing – review & editing.

## 1. Overview

### Repository location

https://doi.org/{doi} (concept DOI).

### Context

The dataset comes from the author's independent research project, the {lex_en}. Strong's numbers (Strong, 1890) link
a translation's words to the Hebrew and Greek vocabulary. Strong-tagged editions of the Károli text, the Hungarian
Protestant base text for four centuries, exist; this alignment is openly licensed, documented word by word, and its
precision is measured. Per verse it records which Hungarian word renders which source word (one-to-many and
many-to-one), the additions and the untranslated source words.

## 2. Method

### Steps

**Texts.** The Hungarian side is the public-domain 1908 Károli text (HunKar); the source side is STEPBible TAHOT
(Hebrew/Aramaic) and TAGNT (Greek) (Tyndale House, Cambridge; CC BY 4.0;
commit efe428a, downloaded 2026-08-24). TAHOT counts Hebrew prefixes and suffixes as separate words (H9001–H9049). Verse divisions
were mapped by deterministic length alignment, each verse merge approved by hand.

**Alignment.** For each verse a language model received two numbered word lists: the Károli words, and the source
words with form, Strong's number and a short English gloss; the Strong's number was for information only and forbidden
in the answer. The fixed instructions also showed an optional Strong-tagged KJV line in a worked example; no verse
input contained one. The model returned position pairs, additions and untranslated words. In Joshua 8:34 it linked
*Azután* (1) to source words 2–3 (*ʾaḥărê kēn*) and *felolvasta* (3) to word 4 (*qārāʾ*); a program then attached
H0310, H3651 and H7121 by position. Twelve written rules decided disputed cases. Fixed conventions apply to function words: Hungarian articles and auxiliaries without a source word are
additions, Hebrew and Greek articles untranslated, as article use differs; an article used as a
pronoun is linked.

**Runs and reproducibility.** All books were aligned by claude-sonnet-5-5: most through the Anthropic Batch API,
Genesis–Deuteronomy, Joshua and Psalms in agent sessions. A program checked every
answer (each Hungarian word exactly once, each source word at least once, only existing positions); a failed answer was
redone. The model thus could not invent a Strong's number or lexicon entry; its possible error is a wrong pairing, and
every pair points to one checkable source word. Model answers were generated once and archived; pair construction,
Strong's number assignment and the gate are deterministic, so the tables rebuild byte-identically from the answers;
re-running the model may differ slightly.

### Sampling strategy

For the blind review, the pair set was divided by book group into {reteg_db_szo} strata (the five books of Moses;
historical, poetic and prophetic books; Gospels and Acts; Epistles; Revelation), with {reteg_n} random pairs per
stratum; in the five books of Moses {rn_OSZ_mozes} pairs from two subsamples, combined by pair weight. The human
validation sample has [N] pairs and [M] unpaired words from the same strata, plus all {elteres} reviewer disagreements
as a weighted oversample. The closed-edition cross-check used {kulso_fejezet_szo} purposively selected chapters (per stratum the one
with most reviewer disagreements).

### Quality control

**Blind model review.** A second model (Claude Opus) independently marked the source words of each sampled Hungarian
word with the same rules, blind to the machine pair; a pair is correct if its source word is among those marks. Pair precision is therefore agreement with a model, not ground truth.

**Human validation.** An external validator, a theology graduate with knowledge of biblical Hebrew and Greek, judged
every item; a second validator, also a theology graduate, is a family member of the author; neither validator was
involved in producing the dataset. Judging is not blind: validators see the machine pair. Rule-determined function
words were excluded from the unpaired sample. The external validator gives the main figure: precision [precision] (95%
CI [CI]), or [conservative] counting uncertain items as errors. The second validator ([precision 2]) and inter-rater
kappa ([kappa]) are supplementary; there is no adjudicator. Agreement with the blind model reviewer is [agreement
with model reviewer].

**Cross-check with a closed edition.** As a supplementary check, pairs were compared locally with the Bible-Discovery
Strong-tagged Károli (HUN module), a closed-licence edition; only the aggregate can be published,
and readers cannot check it. It is not a gold standard: it marks one main word per Hungarian word;
our segmentation is finer (one-to-many links, morphemes, e.g. *Azután* ↔ *ʾaḥărê* + *kēn*). Main-word pairs are content-word pairs whose Hungarian word has a Strong's number in the edition, excluding
secondary pairs of already matched words: {k_n} of {k_osszes} ({k_nincs} without a Strong's number there, {k_masod}
secondary, {k_forma} unalignable); secondary pairs and segmentation differences are not errors.

| measurement | estimate | 95% CI |
|---|---|---|
| pair precision, blind model reviewer, weighted | {p_osszes}% | {p_osszes_a}–{p_osszes_f}% |
| content word / Hebrew morpheme | {p_tartalmi}% / {p_morf}% | {p_tartalmi_a}–{p_tartalmi_f}% / {p_morf_a}–{p_morf_f}% |
| human validation (external); uncertain as errors | [precision]; [conservative] | [CI] |
| main-word agreement, closed edition | {k_fs}% | – |

Precision per stratum ranges from {r_min}% ({r_min_nev}) to {r_max}% ({r_max_nev}). Of the {minta} sample pairs,
{elteres} differed from the reviewer, most often a neighbouring word ({h_szomszedos_token}). Of the {k_elter} differences from the closed edition,
{k_mi_szo} were judged alignment errors (three-way judgement; listed in the dataset); secondary pairs are not
differences.

## 3. Dataset Description

- **Repository name:** Zenodo
- **Object name:** `{objektum}`
- **Format names and versions:** TSV (UTF-8) for the data and
  codebook; Markdown for the bilingual documentation; CFF; SHA-256 checksums
- **Creation dates:** {kezdet} – {adatallapot}
- **Dataset creators:** Tamás Demeter (independent researcher; ORCID: {orcid}): rules, processing pipeline, measurement,
  curation.
- **Language:** Hungarian (data); Hungarian and English (documentation)
- **License:** CC BY 4.0
- **Publication date:** {kozzetetel}

**Contents.** `data/parok/` (one row per link: positions, Strong's number, link type, state, Textus Receptus flag),
`data/szavak/` (every word once, with its state: aligned, addition, untranslated, or pending, i.e. not yet aligned),
`data/versek.tsv`, `data/meres.tsv`; keyed by OSIS verse and word position.

**Size.** {konyv} books, {vers} verses, {par} pairs ({heber_par} Hebrew, {gorog_par} Greek; of these {morfema}
morphemes), {hu_betoldas} additions, {er_forditatlan} untranslated source words, {hu_fuggoben} pending Hungarian words
({fuggoben_vers} verses).

## 4. Reuse Potential

Bible software can offer Strong-based search of the Hungarian text. For language technology it is alignment data for a low-resource pair with
error measured per stratum. The {lex_en}, a motif-indexed, cross-referenced biblical
lexicon, is built on this alignment. A companion dataset (Demeter, 2026b) carries the same pairs on the author's
rule-based modernisation of the text (rare verb forms changed only on agreeing independent model proposals; measured
separately): every word kept its position and merged words keep both pairs, so the figures above apply.

### Limitations

The blind reviewer is itself a model, and human validation is not blind. Pair precision does not cover untranslated
source words. The closed-edition chapters were selected purposively and exclude Hebrew morphemes. In Genesis–Exodus,
{nehez_par} pairs ({nehez_vers} verses) where the second model proposed a different pair are weaker:
{nehez_helyes_szo} of {nehez_minta} sampled were correct, so roughly {nehez_hibas_a}–{nehez_hibas_f} may be wrong; listed uncorrected in the known-issues file of
version 1.1, they will be re-aligned and remeasured in version 1.2. The {nem_tr_token} aligned Greek words
absent from the Textus Receptus, which Károli translated, are flagged.

## Data Accessibility Statement

Both datasets: Zenodo, CC BY 4.0. Version 1.1, deposited
before submission, adds the prompt (logged hash 84f12ca7aafb), raw model answers ({konyv} books), the verse mapping
and merges, the {minta} judged sample pairs, the known-issues list and the human judgements, with the STEPBible commit
and model identifier; no code.

## Acknowledgements

The author thanks [name of the external validator] and [name of the second validator] for the human validation.

## Funding Statement

This work received no external funding.

## Competing Interests

The author has no competing interests to declare.

## References

Demeter, T. (2026a). *Logosz Lexikon – Károli Bible (1908): Word alignment with Hebrew and Greek Strong's numbers*
(Version {verzio}) [Data set]. Zenodo. https://doi.org/{doi}

Demeter, T. (2026b). *Logosz Lexikon – Modernized Károli Bible: Word alignment with Hebrew and Greek Strong's numbers*
(Version {verzio_modern}) [Data set]. Zenodo. https://doi.org/{doi_modern}

STEPBible. (n.d.). *Translators Amalgamated Hebrew OT (TAHOT) and Translators Amalgamated Greek NT (TAGNT)* [Data set].
Tyndale House, Cambridge. https://www.STEPBible.org

Strong, J. (1890). *The exhaustive concordance of the Bible*. Hunt & Eaton.

## AI Declaration

(1) Alignment: Claude Sonnet (Anthropic) returned position pairs only (see Method). For Genesis and Exodus, another
language model was also run as a cross-check; no published pair derives from it alone. (2) Quality control: Claude Opus
served as blind reviewer on the sample; human validation used no AI. (3) Companion dataset: see Reuse Potential. The
claude-opus-5-5 model assisted in drafting and editing the text; figures are generated from the
data. The author designed the study, made all editorial decisions, verified every statement
against the data, and takes full responsibility for the content; an AI tool is not an author.

<!-- END OF SUBMISSION TEXT — the part below can be removed from the submitted version. -->

---

## Submission notes

Word count: sections 1–4 without title, author line, abstract, table and references (as the JOHD template counts)
{szo_fo}; with the unnumbered statements {szo_nyil}; with the references as well {szo_hiv} (the submission page says
the limit includes references; it does not say whether the abstract counts); with the abstract too {szo_kiv}. The JOHD
data paper length is 1,000–1,500 words; the editorial office can confirm which count applies. Everything from the
abstract to the AI Declaration, with headings, keywords, author roles and the table: {szo_mind}.

To fill in before submission: the human validation fields ([N], accuracy, CI, kappa, agreement with the model
reviewer), the corresponding author's e-mail address, the two validators' names. The text goes into the official JOHD
Word or LaTeX template; cover letter: `kozlemeny/data_paper/johd_cover_letter_en.md`.
"""

# a kézirat nem része a csomagnak: a repó gyökerében, a folyóiratcikkek mellett áll (DT-F175b)
KEZIRAT = [
    ('kozlemeny/data_paper/karoli_strong_kezirat_hu.md', KEZIRAT_HU, 'hu'),
    ('kozlemeny/data_paper/karoli_strong_kezirat_en.md', KEZIRAT_EN, 'en'),
]
NOTE_FEJ = ('<!-- GENERÁLT: eszkozok/karoli_strong_export.py (a próza: eszkozok/karoli_strong_szovegek.py, a számok: '
            'adat/karoli_strong/ és f172/) — kézzel nem szerkesztendő; a #175 csomagjának rövid közleménye, belső '
            'anyag, nem része a nyilt_karoli_strong/ csomagnak. -->\n')
KEZIRAT_FEJ = ('<!-- GENERÁLT: eszkozok/karoli_strong_export.py (a próza: eszkozok/karoli_strong_szovegek.py, a számok: '
               'adat/karoli_strong/ és f172/) — kézzel nem szerkesztendő; a #175 második data paperének kézirata, '
               'nem része a nyilt_karoli_strong/ csomagnak. -->\n')
