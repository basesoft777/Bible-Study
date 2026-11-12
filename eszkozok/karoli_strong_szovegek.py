# -*- coding: utf-8 -*-
"""
karoli_strong_szovegek.py -- a Károli 1908 – Strong szóillesztés nyílt mag nyilvános szövegeinek prózája (F175).

Csak sablonok: a `{…}` mezőket a `karoli_strong_export.py` `fmt()` függvénye tölti ki az adatból és a mérőtáblákból;
szám kézzel nem kerül a szövegbe. A kész szövegeket a `karoli_strong_kapu.py` NYILVANOS pontja ellenőrzi (belső
jelölés, tiltott szavak, harmadik fél neve).
"""

# ----------------------------------------------------------------------------- kódkönyv

KODKONYV_FAJLOK = [
    ('parok', '`parok/NN_Konyv.tsv`'),
    ('szavak', '`szavak/NN_Konyv.tsv`'),
    ('versek', '`versek.tsv`'),
    ('meres', '`meres.tsv`'),
]

KODKONYV_SOROK = [
    # fajl, oszlop, ertek, hu, en
    ('parok', 'osis', '', 'A vers OSIS-azonosítója (könyv.fejezet.vers), a Károli-versszámozás szerint.',
     'OSIS verse identifier (book.chapter.verse), in Károli versification.'),
    ('parok', 'token', '', 'A magyar szó sorszáma a versben (1-től; az írásjel nem szó).',
     'Position of the Hungarian word in the verse (from 1; punctuation is not a word).'),
    ('parok', 'alak_1908', '', 'A magyar szó alakja a Károli 1908-as szövegében.', 'Word form in the 1908 Károli text.'),
    ('parok', 'eredeti_token', '', 'Az eredeti szó sorszáma a TAHOT/TAGNT versében, a Károli-vers kulcsán (l. MODSZER.md 3.); a héber előtag és rag külön szónak számít.',
     'Position of the source word in the TAHOT/TAGNT verse, keyed to the Károli verse (see METHODS.md 3); Hebrew prefixes and suffixes count as separate words.'),
    ('parok', 'strong', '', 'Az eredeti szó Strong-száma (H… héber, G… görög) a STEPBible TAHOT/TAGNT szerint; „+” két számot köt össze, ha a forrás egy szóhoz kettőt ad. A modell nem ír Strong-számot: a szám a sorszámból jön.',
     "Strong's number of the source word (H… Hebrew, G… Greek) from STEPBible TAHOT/TAGNT; \"+\" joins two numbers where the source gives two for one word. The model writes no Strong's number: it comes from the position."),
    ('parok', 'kapcsolat', 'szo', 'A pár egy eredeti szóhoz köti a magyar szót.', 'The pair links the Hungarian word to a source word.'),
    ('parok', 'kapcsolat', 'morfema', 'A pár egy héber előtag- vagy ragmorfémához köti (H9001–H9049: névelő, kötőszó, elöljáró, személyrag).',
     'The pair links it to a Hebrew prefix or suffix morpheme (H9001–H9049: article, conjunction, preposition, pronominal suffix).'),
    ('parok', 'bizonyossag', 'magas', 'Két független nyelvi modell ugyanazt a párt adta (Mózes 1–2. könyve).',
     'Two independent language models gave the same pair (Genesis and Exodus).'),
    ('parok', 'bizonyossag', 'alacsony', 'Egy nyelvi modell javaslata, vagy a két modell eltért; a pontosságát a mérés adja meg (meres.tsv).',
     'Proposal of one language model, or the two models differed; its accuracy is given by the measurement (meres.tsv).'),
    ('parok', 'allapot', 'javaslat', 'Gépi párosítási javaslat, mért pontossággal; nem kézzel ellenőrzött pár.',
     'Machine alignment proposal with measured accuracy; not a manually verified pair.'),
    ('parok', 'nem_tr', 'igen', 'Az eredeti görög szó nem szerepel a Textus Receptusban, amelyet Károli fordított; a Strong-szám a kritikai szöveg alakjáé (l. ISMERT_HIBAK.md).',
     'The Greek source word is not in the Textus Receptus, which Károli translated; the Strong number is that of the critical-text form (see KNOWN_ISSUES.md).'),
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
    ('szavak', 'bizonyossag', 'magas', 'A két modell ugyanazt a partnerhalmazt (vagy ugyanazt a betoldás/fordítatlan döntést) adta a szóra.',
     'The two models gave the same partner set (or the same addition / untranslated decision) for the word.'),
    ('szavak', 'bizonyossag', 'alacsony', 'Egy modell döntése, vagy a két modell eltért.', 'Decision of one model, or the two models differed.'),
    ('versek', 'osis', '', 'A vers OSIS-azonosítója, a Károli-versszámozás szerint.', 'OSIS verse identifier, in Károli versification.'),
    ('versek', 'szoveg_1908', '', 'A vers Károli 1908 szövege, írásjelekkel; a szavak sorszáma ebből számolódik.',
     'The 1908 Károli text of the verse, with punctuation; word positions are counted on it.'),
    ('meres', 'szakasz', 'reteg', 'Rétegenkénti egyezés a vak ellenőrrel: rétegenként egyszerű véletlen minta.',
     'Agreement with the blind reviewer per stratum: a simple random sample per stratum.'),
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
    ('meres', 'cimke', '', 'A sor tárgya: réteg (OSZ_mozes_magas, OSZ_mozes_alacsony, OSZ_tortenet, OSZ_koltoi, OSZ_profeta, USZ_evangelium, USZ_level, USZ_jelenesek), csoport vagy hibatípus (folos_par, szomszedos_token, rossz_szo_a_versben, azonos_lexema_mas_elofordulas).',
     'Subject of the row: stratum (OSZ_mozes_magas, OSZ_mozes_alacsony, OSZ_tortenet, OSZ_koltoi, OSZ_profeta, USZ_evangelium, USZ_level, USZ_jelenesek), group or error type (folos_par = superfluous pair, szomszedos_token = neighbouring word, rossz_szo_a_versben = wrong word in the verse, azonos_lexema_mas_elofordulas = same lexeme, other occurrence).'),
    ('meres', 'n', '', 'A mért párok száma.', 'Number of pairs measured.'),
    ('meres', 'x', '', 'Az egyező (helyes) párok száma; hibatípusnál az adott típusú eltérések száma.',
     'Number of agreeing (correct) pairs; for an error type, the number of differences of that type.'),
    ('meres', 'p', '', 'Arány (x / n, súlyozott soroknál a súlyozott becslés).', 'Proportion (x / n; for weighted rows the weighted estimate).'),
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

Ez a mappa egy önálló nyilvános adattároló gyökere: a tartalma változtatás nélkül feltölthető, és minden benne álló
fájl a kiadás része (a `kozlemeny/` almappa kivételével, amely a megjelenésig tervezet).

- **Licenc:** CC BY 4.0 (`LICENSE`); a felhasznált külső adatok forrásmegjelölése: `ATTRIBUCIO.md`.
- **DOI:** {doi} — a kiadás azonosítója és a tartalmi hash: `KIADAS.txt`.
- **Szerző:** {szerzo} (ORCID {orcid}).

## Tartalom

| fájl | tartalom |
|---|---|
| `parok/NN_Konyv.tsv` | könyvenként minden szópár: magyar szó – eredeti szó, Strong-számmal |
| `szavak/NN_Konyv.tsv` | könyvenként minden magyar és minden eredeti szó, egyszer: párosított, betoldás, fordítatlan vagy függőben |
| `versek.tsv` | a Károli 1908 szövege versenként |
| `meres.tsv` | a párosítás mért pontossága rétegenként és kapcsolattípusonként, konfidencia-intervallummal |
| `kodkonyv.tsv`, `KODKONYV.md` | az oszlopok és az értékek leírása (magyarul és angolul) |
| `MODSZER.md`, `METHODS.md` | hogyan készült a párosítás, és hogyan mértük |
| `ISMERT_HIBAK.md`, `KNOWN_ISSUES.md` | ismert hibák és korlátok |
| `ATTRIBUCIO.md` | forrásmegjelölés és licencek |
| `CITATION.cff` | idézési adatok |
| `ELLENORZO_OSSZEG.sha256` | minden fájl SHA-256 összege |

## Számokban

- {konyv} könyv, {vers} vers; {hu_token} magyar és {er_token} eredeti szó (token).
- {par} szópár {hu_parositva} magyar szón ({heber_par} héber, {gorog_par} görög pár; ebből {morfema} héber
  előtag- vagy ragmorféma).
- {hu_betoldas} magyar szó a fordító betoldása, {er_forditatlan} eredeti szót a Károli nem fordít külön szóval;
  {hu_fuggoben} magyar és {er_fuggoben} eredeti szó párosítása függőben van ({fuggoben_vers} versben).
- Pontosság: a fő szavak párjain egy független forrás szerint {k_fs}% (95%: {k_fs_a}–{k_fs_f}%); a teljes
  párkészleten a vak ellenőrrel {p_osszes}% (95%: {p_osszes_a}–{p_osszes_f}%); részletesen: `meres.tsv`,
  `MODSZER.md` 5.

## Rövid használati útmutató

A kulcs a vers OSIS-azonosítója (`Gen.1.1`) és a szó sorszáma a versen belül (`token`). A `parok` tábla minden sora egy
kapcsolat; egy magyar szó annyi sorban áll, ahány eredeti szóhoz tartozik. A `szavak` tábla minden szót pontosan egyszer
sorol fel, a két oldalon külön (`oldal` = `hu` vagy `er`): innen olvasható ki, mi maradt pár nélkül. A héber és görög
szóalak nincs a csomagban; az eredeti szót a sorszáma és a Strong-száma azonosítja, és a sorszám a STEPBible
TAHOT/TAGNT szövegéhez illeszthető.

Minden pár gépi javaslat, mért pontossággal (`allapot` = `javaslat`); a `bizonyossag` oszlop jelzi, hol egyezett két
független modell.

## Kapcsolódó adatkészletek

- Modernizált Károli – Strong (ugyanezek a párok a modernizált szövegen): https://doi.org/{doi_modern}
- A {lex_hu} nyílt adatmagja (motívumok): https://doi.org/{doi_mag}
"""

README = """# {cim_en} — open dataset

The 1908 text of the Károli Bible (the classic Hungarian translation), linked word by word to the Hebrew and Greek
source words and their Strong's numbers. One of the open data cores of the {lex_en}.

This folder is the root of a self-contained public repository: its content can be uploaded unchanged, and every file
in it is part of the release (except the `kozlemeny/` subfolder, a draft until publication).

- **Licence:** CC BY 4.0 (`LICENSE`); attribution of the third-party data used: `ATTRIBUCIO.md`.
- **DOI:** {doi} — release identifier and content hash: `RELEASE.txt`.
- **Author:** {szerzo} (ORCID {orcid}).

## Contents

| file | content |
|---|---|
| `parok/NN_Book.tsv` | per book, every word pair: Hungarian word – source word, with Strong's number |
| `szavak/NN_Book.tsv` | per book, every Hungarian and every source word once: aligned, addition, untranslated or pending |
| `versek.tsv` | the 1908 Károli text, verse by verse |
| `meres.tsv` | the measured accuracy of the alignment per stratum and link type, with confidence intervals |
| `kodkonyv.tsv`, `KODKONYV.md` | description of the columns and values (Hungarian and English) |
| `METHODS.md`, `MODSZER.md` | how the alignment was made and how it was measured |
| `KNOWN_ISSUES.md`, `ISMERT_HIBAK.md` | known issues and limitations |
| `ATTRIBUCIO.md` | attribution and licences |
| `CITATION.cff` | citation metadata |
| `ELLENORZO_OSSZEG.sha256` | SHA-256 checksum of every file |

## In numbers

- {konyv} books, {vers} verses; {hu_token} Hungarian and {er_token} source words (tokens).
- {par} word pairs on {hu_parositva} Hungarian words ({heber_par} Hebrew, {gorog_par} Greek pairs; of these {morfema}
  are Hebrew prefix or suffix morphemes).
- {hu_betoldas} Hungarian words are translator's additions, {er_forditatlan} source words are not rendered by a
  separate Hungarian word; {hu_fuggoben} Hungarian and {er_fuggoben} source words are pending ({fuggoben_vers} verses).
- Accuracy: on main-word pairs {k_fs}% against an independent source (95%: {k_fs_a}–{k_fs_f}%); on the full pair set
  {p_osszes}% agreement with a blind reviewer (95%: {p_osszes_a}–{p_osszes_f}%); details: `meres.tsv`, `METHODS.md` 5.

## Quick guide

The key is the OSIS verse identifier (`Gen.1.1`) and the position of the word within the verse (`token`). Each row of
the `parok` table is one link; a Hungarian word appears in as many rows as source words it is linked to. The `szavak`
table lists every word exactly once, the two sides separately (`oldal` = `hu` or `er`): it shows what has no pair. The
Hebrew and Greek word forms are not in the package; a source word is identified by its position and Strong's number,
and the position matches the STEPBible TAHOT/TAGNT text.

Every pair is a machine proposal with measured accuracy (`allapot` = `javaslat`); the `bizonyossag` column marks where
two independent models agreed.

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

A Károli 1908 szövege közkincs; a STEPBible TAHOT és TAGNT adatai CC BY 4.0 alatt állnak (ATTRIBUCIO.md).
The 1908 Károli text is in the public domain; the STEPBible TAHOT and TAGNT data are under CC BY 4.0 (ATTRIBUCIO.md).
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
    title: "{lex_en} — open data core"
    authors:
      - family-names: "Demeter"
        given-names: "Tamás"
    doi: "{doi_mag}"
"""

GITATTRIBUTES = """# Sorvég: minden fájl LF-fel, minden checkouton (az ellenőrző összeg az LF-es bájtokra szól).
* text eol=lf
# A közlemény-tervezet a megjelenésig nem része a kiadásnak.
kozlemeny/ export-ignore
"""

# ----------------------------------------------------------------------------- ismert hibák

ISMERT_HIBAK = """# Ismert hibák és korlátok

*{cim} · 1. kiadás · adatállapot: {adatallapot}*

Ez a kiadás a párosítást a mérés pillanatában álló állapotban adja közre, változatlanul. A lent felsorolt hibák
javítása a 2. kiadásba kerül, új méréssel (`MODSZER.md` 7.).

## Megerősített hibák

1. **Öt megerősített párhiba** a mintában és az összevetett fejezetekben: Péld 3:18 (az „Életnek” és a „fája” párja
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
7. **Bizonyosság:** két modell csak Mózes első két könyvét párosította; a többi könyv minden párja egy modell
   javaslata (`alacsony`). Az `alacsony` jelölés ezért nem hibagyanút, hanem egyetlen forrást jelent.
8. **A mérés korlátai:** a vak ellenőr maga is nyelvi modell, és egy korábbi, kézzel összeállított mintán nem
   pontosabb a párosításnál ({kal_ell}% és {kal_gep}%); az egyezés ezért csak akkor alsó becslés, ha a közös hiba
   elhanyagolható. A független összevetés {kulso_fejezet} teljes fejezeten, a fő szavak párjain készült; a fejezetek
   klaszterek, nem véletlen mintaelemek, így az intervallum alulbecsüli a bizonytalanságot.

A kiadás a `KIADAS.txt` azonosítójával idézhető.
"""

KNOWN_ISSUES = """# Known issues and limitations

*{cim_en} · release 1 · data state: {adatallapot}*

This release publishes the alignment as it stood when it was measured, unchanged. Corrections of the issues below go
into release 2, with a new measurement (`METHODS.md` 7).

## Confirmed errors

1. **Five confirmed pair errors** in the sample and the compared chapters: Prov 3:18 (the pairs of "Életnek" and "fája"
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
7. **Confidence:** two models aligned only Genesis and Exodus; every pair in the other books is the proposal of one
   model (`alacsony`). The `alacsony` label therefore means a single source, not a suspected error.
8. **Limits of the measurement:** the blind reviewer is itself a language model, and on an earlier manually compiled
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

A párosítás nyelvi modellek javaslata, mért pontossággal. Nem kézzel ellenőrzött adat: minden pár „javaslat” állapotú,
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

**A modellek.** Mózes első két könyvét két független modell párosította ugyanazzal a feladatleírással: a Claude Sonnet
és a Gemini Flash. A két válaszból program állította össze a táblát: ahol a két modell ugyanazt a párt adta, a pár
`magas` bizonyosságú ({magas} pár); ahol eltértek, az első modell párja került be, `alacsony` bizonyossággal. A többi
könyvet a költségkeret miatt egy modell, a Claude Sonnet párosította; ezek párjai mind `alacsony`
({alacsony} pár). A feladatleírás a futás alatt változatlan volt; a táblák a modellek mentett válaszaiból, újabb
modellhívás nélkül, bájtra azonosan újraépíthetők.

**Az eredmény.** {hu_parositva} magyar szónak van párja, {hu_betoldas} betoldás; {er_parositva} eredeti szó párosított,
{er_forditatlan} fordítatlan. A {par} párból {heber_par} héber és {gorog_par} görög; {morfema} egy héber előtag- vagy
ragmorféma párja.

## 5. A pontosság mérése

A pontosságot két, egymást kiegészítő úton mértük.

**Vak ellenőrzés, rétegzett mintán.** A {par} párt nyolc rétegre osztottuk (Mózes két modellel és egy modellel; a
történeti, a költői és a prófétai könyvek; az evangéliumok és az Apostolok cselekedetei; a levelek; a Jelenések), és
rétegenként {reteg_n} párt húztunk véletlenszerűen. Egy harmadik nyelvi modell (Claude Opus) a minta minden céljára a
vers szövegéből és az eredeti szavakból maga jelölte ki a megfelelő eredeti szavakat, ugyanazokkal a szabályokkal, a gépi
pár ismerete nélkül. A pár helyes, ha az eredeti szava az ellenőr jelölései között van.

| réteg | n | helyes | arány | 95% |
|---|---|---|---|---|
| Mózes, két modell egyezése | {rn_OSZ_mozes_magas} | {rx_OSZ_mozes_magas} | {r_OSZ_mozes_magas}% | {r_OSZ_mozes_magas_a}–{r_OSZ_mozes_magas_f}% |
| Mózes, egy modell | {rn_OSZ_mozes_alacsony} | {rx_OSZ_mozes_alacsony} | {r_OSZ_mozes_alacsony}% | {r_OSZ_mozes_alacsony_a}–{r_OSZ_mozes_alacsony_f}% |
| történeti könyvek | {rn_OSZ_tortenet} | {rx_OSZ_tortenet} | {r_OSZ_tortenet}% | {r_OSZ_tortenet_a}–{r_OSZ_tortenet_f}% |
| költői könyvek | {rn_OSZ_koltoi} | {rx_OSZ_koltoi} | {r_OSZ_koltoi}% | {r_OSZ_koltoi_a}–{r_OSZ_koltoi_f}% |
| próféták | {rn_OSZ_profeta} | {rx_OSZ_profeta} | {r_OSZ_profeta}% | {r_OSZ_profeta_a}–{r_OSZ_profeta_f}% |
| evangéliumok, Apostolok cselekedetei | {rn_USZ_evangelium} | {rx_USZ_evangelium} | {r_USZ_evangelium}% | {r_USZ_evangelium_a}–{r_USZ_evangelium_f}% |
| levelek | {rn_USZ_level} | {rx_USZ_level} | {r_USZ_level}% | {r_USZ_level_a}–{r_USZ_level_f}% |
| Jelenések | {rn_USZ_jelenesek} | {rx_USZ_jelenesek} | {r_USZ_jelenesek}% | {r_USZ_jelenesek_a}–{r_USZ_jelenesek_f}% |
| **Ószövetség, súlyozott** | {n_osz} | | {p_osz}% | {p_osz_a}–{p_osz_f}% |
| **Újszövetség, súlyozott** | {n_usz} | | {p_usz}% | {p_usz_a}–{p_usz_f}% |
| **összes, súlyozott** | {n_osszes} | | **{p_osszes}%** | {p_osszes_a}–{p_osszes_f}% |

A súlyozott becslés a rétegek pársúlyával számol. Kapcsolattípus szerint: a tartalmi szavak párjai {p_tartalmi}%
(95%: {p_tartalmi_a}–{p_tartalmi_f}%), a héber morfémák párjai {p_morf}% (95%: {p_morf_a}–{p_morf_f}%). A két modell
egyezésének rétege {r_OSZ_mozes_magas}%-os, de ebből nem következik, hogy a második modell okozza a különbséget: a két Mózes-réteg
könyvei nagyrészt eltérnek.

**Kalibráció.** Az ellenőr nem tévedhetetlen. Egy korábbi, kézzel összeállított mintán ({kal_ell_n} mérhető eset) az
ellenőr {kal_ell}%-ban (95%: {kal_ell_a}–{kal_ell_f}%), a gépi párosítás {kal_gep}%-ban (95%: {kal_gep_a}–{kal_gep_f}%)
egyezett vele: az ellenőr nem pontosabb a párosításnál. Az eltérések egy része tehát az ellenőr hibája, és az egyezés
csak akkor alsó becslés, ha a közös (gépi és ellenőri) hiba elhanyagolható.

**Független összevetés.** Ezt a közös hibát egy független forrás méri: egy Strong-számokkal jelölt Károli-kiadás,
amelyet a csomag nem tartalmaz, és amelyből csak az összesített egyezés szerepel itt. Rétegenként egy teljes fejezetet
vetettünk össze ({kulso_fejezet} fejezet, {k_n} fő szó párja). A forrás szavanként egy fő Strong-számot jelöl, a ragban,
elöljáróban és névelőben álló mellékszót és a morfémát nem; ez a mérés tehát csak a fő szavak párjaira érvényes.

- A forrás ítéletét elfogadva a fő szavak párjainak {k_fs}%-a egyezik (95%: {k_fs_a}–{k_fs_f}%; Ószövetség {ko_fs}%,
  Újszövetség {ku_fs}%).
- A {k_elter} eltérést háromutasan ítéltük meg (gépi pár, forrás, vak ellenőr); ezek után {k_mi} maradt a párosítás
  hibája, a fő szavak pontossága így {k_h3}% (95%: {k_h3_a}–{k_h3_f}%).
- A fejezetek klaszterek, nem véletlen mintaelemek; a valódi bizonytalanság nagyobb, mint az intervallum.

**Hibatípusok.** A {minta} mintapárból {elteres} tért el az ellenőrtől: szomszédos szó {h_szomszedos_token} (tartalmi
{ht_szomszedos_token}, morféma {hm_szomszedos_token}), rossz szó a versben {h_rossz_szo_a_versben}, fölös pár
{h_folos_par}, azonos lexéma más előfordulása {h_azonos_lexema_mas_elofordulas}. A mérés minden száma a `meres.tsv`-ben
áll.

## 6. Miért nyílt adat

A párosítás nem hibátlan, és nem is így kerül közlésre. Szerkesztői döntés alapján nyílt adatként jelenik meg, mert a
pontossága **mérve és dokumentálva van**: rétegenként és kapcsolattípusonként, konfidencia-intervallummal, a hibák
típusával és a megerősített hibák listájával (`ISMERT_HIBAK.md`). A „javaslat” állapot és a bizonyosság-jelölés minden
páron megmarad. A közlés nem egy előre kitűzött küszöb teljesülésén alapul: a mérés előtt nem volt rögzített
kritérium, és utólag felállított küszöb utólagos kritérium volna.

## 7. A következő kiadás

Ez az 1. kiadás: a mért állapot, változatlanul. A 2. kiadás javítja a megerősített hibákat és a szomszédos szó
szabályellenes eseteit (szabályalapú utófeldolgozással, nem páronkénti folttal), majd ugyanazzal a protokollal újra
mér: rétegzett minta, vak ellenőr, független külső forrás. A 2. kiadás minőségi célját az 1. kiadás eredményeinek
ismeretében, előre rögzítettük: a független összevetés fő-szó egyezésének alsó széle legalább 98% (most {k_fs_a}%); a
vak ellenőrrel mért súlyozott egyezés alsó széle legalább 93% (most {p_osszes_a}%), és egyetlen réteg pontbecslése sem
90% alatti (most a legkisebb {r_OSZ_mozes_alacsony}%). A cél az 1. kiadásra nem vonatkozik.

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

The alignment is a proposal of language models, with measured accuracy. It is not manually verified data: every pair is
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

**The models.** Genesis and Exodus were aligned by two independent models with the same task description: Claude
Sonnet and Gemini Flash. A program built the table from the two answers: where both gave the same pair, the pair has
`magas` (high) confidence ({magas} pairs); where they differed, the first model's pair was kept with `alacsony` (low)
confidence. For reasons of cost, the other books were aligned by one model, Claude
Sonnet; all their pairs are `alacsony` ({alacsony} pairs). The task description did not change during the run; the
tables can be rebuilt byte-identically from the models' saved answers, without new model calls.

**Result.** {hu_parositva} Hungarian words have a pair, {hu_betoldas} are additions; {er_parositva} source words are
aligned, {er_forditatlan} untranslated. Of the {par} pairs, {heber_par} are Hebrew and {gorog_par} Greek; {morfema}
link a Hebrew prefix or suffix morpheme.

## 5. Measuring accuracy

Accuracy was measured in two complementary ways.

**Blind review on a stratified sample.** The {par} pairs were divided into eight strata (Genesis–Deuteronomy with two
models and with one; the historical, poetic and prophetic books; the Gospels and Acts; the Epistles; Revelation), and
{reteg_n} pairs were drawn at random per stratum. A third language model (Claude Opus) marked, for each target in the
sample, the matching source words from the verse text and the source words itself, with the same rules, without seeing
the machine pair. A pair is correct if its source word is among the reviewer's marks.

| stratum | n | correct | rate | 95% |
|---|---|---|---|---|
| Moses, two models agreeing | {rn_OSZ_mozes_magas} | {rx_OSZ_mozes_magas} | {r_OSZ_mozes_magas}% | {r_OSZ_mozes_magas_a}–{r_OSZ_mozes_magas_f}% |
| Moses, one model | {rn_OSZ_mozes_alacsony} | {rx_OSZ_mozes_alacsony} | {r_OSZ_mozes_alacsony}% | {r_OSZ_mozes_alacsony_a}–{r_OSZ_mozes_alacsony_f}% |
| historical books | {rn_OSZ_tortenet} | {rx_OSZ_tortenet} | {r_OSZ_tortenet}% | {r_OSZ_tortenet_a}–{r_OSZ_tortenet_f}% |
| poetic books | {rn_OSZ_koltoi} | {rx_OSZ_koltoi} | {r_OSZ_koltoi}% | {r_OSZ_koltoi_a}–{r_OSZ_koltoi_f}% |
| prophets | {rn_OSZ_profeta} | {rx_OSZ_profeta} | {r_OSZ_profeta}% | {r_OSZ_profeta_a}–{r_OSZ_profeta_f}% |
| Gospels, Acts | {rn_USZ_evangelium} | {rx_USZ_evangelium} | {r_USZ_evangelium}% | {r_USZ_evangelium_a}–{r_USZ_evangelium_f}% |
| Epistles | {rn_USZ_level} | {rx_USZ_level} | {r_USZ_level}% | {r_USZ_level_a}–{r_USZ_level_f}% |
| Revelation | {rn_USZ_jelenesek} | {rx_USZ_jelenesek} | {r_USZ_jelenesek}% | {r_USZ_jelenesek_a}–{r_USZ_jelenesek_f}% |
| **Old Testament, weighted** | {n_osz} | | {p_osz}% | {p_osz_a}–{p_osz_f}% |
| **New Testament, weighted** | {n_usz} | | {p_usz}% | {p_usz_a}–{p_usz_f}% |
| **all, weighted** | {n_osszes} | | **{p_osszes}%** | {p_osszes_a}–{p_osszes_f}% |

The weighted estimate uses the pair share of the strata. By link type: content-word pairs {p_tartalmi}% (95%:
{p_tartalmi_a}–{p_tartalmi_f}%), Hebrew morpheme pairs {p_morf}% (95%: {p_morf_a}–{p_morf_f}%). The stratum where the
two models agreed reaches {r_OSZ_mozes_magas}%, but this does not show that the second model causes the difference: the books of the two
Moses strata largely differ.

**Calibration.** The reviewer is not infallible. On an earlier manually compiled sample ({kal_ell_n} measurable cases)
the reviewer agreed with it in {kal_ell}% (95%: {kal_ell_a}–{kal_ell_f}%), the machine alignment in {kal_gep}% (95%:
{kal_gep_a}–{kal_gep_f}%): the reviewer is not more accurate than the alignment. Part of the differences are thus the
reviewer's errors, and the agreement is a lower bound only if shared (machine and reviewer) errors are negligible.

**Independent comparison.** Shared errors are measured by an independent source: a Károli edition marked with Strong's
numbers, which the package does not contain and of which only the aggregate agreement is given here. One full chapter
per stratum was compared ({kulso_fejezet} chapters, {k_n} main-word pairs). The source marks one main Strong's number
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
{h_azonos_lexema_mas_elofordulas}. Every figure of the measurement is in `meres.tsv`.

## 6. Why open data

The alignment is not error-free, and it is not published as such. By editorial decision it is released as open data
because its accuracy is **measured and documented**: per stratum and link type, with confidence intervals, with the
error types and the list of confirmed errors (`KNOWN_ISSUES.md`). The "proposal" state and the confidence label remain
on every pair. Publication does not rest on meeting a threshold set in advance: there was no fixed criterion before the
measurement, and a threshold set afterwards would be a post-hoc criterion.

## 7. The next release

This is release 1: the measured state, unchanged. Release 2 will correct the confirmed errors and the rule-violating
neighbouring-word cases (by rule-based post-processing, not pair-by-pair patches), then measure again with the same
protocol: stratified sample, blind reviewer, independent external source. The quality target for release 2 was fixed
in advance, in knowledge of the release 1 results: the lower bound of main-word agreement in the independent comparison
at least 98% (now {k_fs_a}%); the lower bound of the weighted agreement with the blind reviewer at least 93% (now
{p_osszes_a}%), with no stratum point estimate below 90% (now the lowest is {r_OSZ_mozes_alacsony}%). The target does
not apply to release 1.

## 8. Related dataset

The same pairs also appear on the modernised Károli text (https://doi.org/{doi_modern}). The modernisation left every
word in its place, so the two packages can be joined word by word on the verse and word position key.
"""

# ----------------------------------------------------------------------------- közlemény (tervezet)

KOZLEMENY_HU = """# A Károli-biblia szavanként az eredeti nyelvekhez kötve — mért pontossággal

*Közlemény-tervezet · {cim} · {lex_hu} · DOI: {doi}*

Aki a Károli-bibliát olvasva azt kérdezi, milyen héber vagy görög szó áll egy magyar szó mögött, ma kézikönyvekhez és
konkordanciákhoz fordul. A {lex_hu} most szabad licenccel közreadja a Károli 1908-as szövegének szavankénti
párosítását az eredeti szöveggel: a {par} szópár mindegyike megmondja, melyik héber vagy görög szót fordítja az adott
magyar szó, és mi a Strong-száma.

**Hogyan készült.** A párosítást nyelvi modellek végezték, versenként, egy írott szabálykészlet szerint: mikor betoldás a
magyar névelő, hová tartozik a héber birtokos rag, mit kezdjünk a kettéírt *a mely*-vel. A modell csak azt jelölte,
melyik szó melyikhez tartozik; Strong-számot nem írt, azt a STEPBible nyílt héber és görög szövege adja. Minden választ
program ellenőrzött, hogy egy szó se maradjon ki, és egy se álljon kétszer. Mózes első két könyvét két független modell
párosította; ahol egyeztek, a pár „magas” bizonyosságot kapott.

**Mennyire pontos.** A párosítás nem hibátlan, és ezt nem is állítjuk. Azt állítjuk, hogy megmértük, és a mérés minden
számát közöljük. Nyolc rétegből húzott véletlen mintán egy harmadik, a párokat nem látó modell {p_osszes}%-ban értett
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
Hungarian word, today turns to handbooks and concordances. The {lex_en} now releases, under a free licence, a word-by-word
alignment of the 1908 Károli text with the source text: each of the {par} word pairs states which Hebrew or Greek word
the Hungarian word translates, and its Strong's number.

**How it was made.** The alignment was done by language models, verse by verse, following a written rule set: when the
Hungarian article is an addition, where a Hebrew possessive suffix belongs, what to do with a split relative pronoun.
The model only marked which word goes with which; it wrote no Strong's numbers, which come from the open STEPBible
Hebrew and Greek text. A program checked every answer, so that no word is left out and none appears twice. Genesis and
Exodus were aligned by two independent models; where they agreed, the pair is marked high confidence.

**How accurate.** The alignment is not error-free, and we do not claim it is. We claim that it has been measured, and we
publish every figure of the measurement. On a random sample drawn from eight strata, a third model that did not see the
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
    ('OLVASSEL.md', OLVASSEL, 'hu'),
    ('README.md', README, 'en'),
    ('LICENSE', LICENSE, 'hu'),
    ('ATTRIBUCIO.md', ATTRIBUCIO, 'hu'),
    ('MODSZER.md', MODSZER, 'hu'),
    ('METHODS.md', METHODS, 'en'),
    ('ISMERT_HIBAK.md', ISMERT_HIBAK, 'hu'),
    ('KNOWN_ISSUES.md', KNOWN_ISSUES, 'en'),
    ('CITATION.cff', CITATION, 'hu'),
]

KOZLEMENY = [
    ('kozlemeny_hu.md', KOZLEMENY_HU, 'hu'),
    ('kozlemeny_en.md', KOZLEMENY_EN, 'en'),
]

# ----------------------------------------------------------------------------- a data paper kézirata (tervezet)

KEZIRAT_HU = """# A Károli-biblia 1908-as szövegének szavankénti párosítása a héber és görög eredetivel: nyílt adatkészlet mért pontossággal

*Kézirat-tervezet (data paper) · {cim} · {lex_hu} · DOI: {doi}*

## Kivonat

Az adatkészlet a Károli-biblia 1908-as szövegének {hu_token} szavát és a héber és görög eredeti szöveg {er_token} szavát
kapcsolja össze {par} szópárral, minden párt az eredeti szó Strong-számával. A párosítást nyelvi modellek végezték egy
írott szabálykészlet szerint; a modell csak sorszámot jelölt, a Strong-szám a STEPBible nyílt TAHOT és TAGNT adataiból
jön. A pontosságot kétféleképpen mértük: nyolc rétegből húzott véletlen mintán egy vak modell-ellenőrrel (a teljes
párkészleten {p_osszes}%, 95%: {p_osszes_a}–{p_osszes_f}%), és egy független, Strong-számos Károli-kiadással a fő szavak
párjain ({k_fs}%, 95%: {k_fs_a}–{k_fs_f}%). Az adatkészlet a mért állapotot adja közre, a megerősített hibák listájával
és a következő kiadás előre rögzített minőségi céljával. Licenc: CC BY 4.0.

## 1. Áttekintés

**Háttér.** A Károli-fordítás négy évszázada a magyar protestáns bibliaolvasás alapszövege, de a mögötte álló héber és
görög szavak szavankénti, szabadon használható hozzárendelése eddig hiányzott. Az angol nyelvterületen a Strong-számos
King James-szöveg régóta az olvasók és a kutatók alapeszköze; magyarul hasonló nyílt adat nem volt hozzáférhető. Ez az
adatkészlet ezt a hiányt pótolja, a {lex_hu} egyik nyílt adatmagjaként.

**A kérdés, amelyre válaszol.** Melyik magyar szó melyik eredeti szót fordítja; mely magyar szó a fordító betoldása;
mely eredeti szót nem ad vissza külön magyar szó. A harmadik kérdés ugyanolyan fontos, mint az első: a `szavak` tábla
minden szót egyszer sorol fel, így a fordítás „hiányai” is kiolvashatók.

## 2. Módszer

**Szövegek és szavakra bontás.** A magyar oldal a Károli 1908 közkincs szövege, az eredeti oldal a STEPBible TAHOT
(héber és arámi Ószövetség) és TAGNT (görög Újszövetség) adatkészlete. A TAHOT a héber előtagokat és ragokat külön
szóként kezeli (H9001–H9049); ezért egy magyar szóhoz gyakran több eredeti „szó” tartozik. A Károli versbeosztását a
párosítás előtt determinisztikus vershossz-igazítással feleltettük meg az eredetiének; két vers egybeolvadását kézzel
hagytuk jóvá.

**Párosítás.** A modell versenként sorszámozott magyar és eredeti szavakat kapott (az eredetinél alakkal,
Strong-számmal és angol tükörfordítással), és sorszámpárokat adott vissza, a betoldásokkal és a fordítatlan szavakkal
együtt. A vitás eseteket tizenkét írott szabály döntötte el: a névelőkről, a kettéírt kötőszóról és vonatkozó
névmásról, a tárgyjelölőről, a birtokos ragról, a különírt igekötőről, a kitett alanyi névmásról és a segédigéről, a
héber *ve-* kötőszóról, valamint a Textus Receptusban nem szereplő görög szóról. Minden választ program ellenőrzött
(minden magyar szó pontosan egyszer, minden eredeti szó legalább egyszer, csak létező sorszám); a bukott választ a modell
újra elkészítette. Mózes első két könyvét két független modell (Claude Sonnet és Gemini Flash) párosította: ahol
egyeztek, a pár `magas` bizonyosságú ({magas} pár). A többi könyvet a költségkeret miatt egy modell (Claude Sonnet)
párosította (`alacsony`, {alacsony} pár). A táblák a mentett modellválaszokból bájtra azonosan újraépíthetők.

**Pontosságmérés.** (1) *Vak ellenőrzés.* A párkészletet nyolc rétegre osztottuk (Mózes két modellel és egy modellel;
történeti, költői és prófétai könyvek; evangéliumok és ApCsel; levelek; Jelenések), rétegenként {reteg_n} véletlen
párral. Egy harmadik modell (Claude Opus) a cél magyar szóhoz maga jelölte ki az eredeti szavakat, ugyanazokkal a
szabályokkal, a gépi pár ismerete nélkül. (2) *Kalibráció.* Egy korábbi, kézzel összeállított mintán az ellenőr
{kal_ell}%-ban, a gépi párosítás {kal_gep}%-ban egyezett a mintával: az ellenőr nem pontosabb a párosításnál, ezért az
egyezés csak akkor alsó becslés, ha a közös hiba elhanyagolható. (3) *Független összevetés.* Ezt a közös hibát egy
Strong-számokkal jelölt Károli-kiadás méri, rétegenként egy teljes fejezeten ({kulso_fejezet} fejezet, {k_n} fő szó
párja); a forrás csak a fő szót jelöli, a mellékszót és a morfémát nem. Az eltéréseket háromutasan (gépi pár, forrás,
vak ellenőr) ítéltük meg. A külső forrás adata nem része az adatkészletnek, csak az összesített arány.

## 3. Eredmények

| mérés | becslés | 95% |
|---|---|---|
| teljes párkészlet, vak ellenőr, súlyozott | {p_osszes}% | {p_osszes_a}–{p_osszes_f}% |
| ebből Ószövetség / Újszövetség | {p_osz}% / {p_usz}% | {p_osz_a}–{p_osz_f}% / {p_usz_a}–{p_usz_f}% |
| tartalmi szó / héber morféma | {p_tartalmi}% / {p_morf}% | {p_tartalmi_a}–{p_tartalmi_f}% / {p_morf_a}–{p_morf_f}% |
| fő szavak, a független forrás szerint | {k_fs}% | {k_fs_a}–{k_fs_f}% |
| fő szavak, háromutas ítélet után | {k_h3}% | {k_h3_a}–{k_h3_f}% |

A rétegek egyezése {r_OSZ_mozes_alacsony}% (Mózes, egy modell) és {r_OSZ_mozes_magas}% (Mózes, két modell egyezése)
között mozog; a rétegenkénti táblát az adatkészlet `meres.tsv` fájlja és módszertani leírása közli. A {minta} mintapárból
{elteres} tért el az ellenőrtől; a leggyakoribb típus a szomszédos szó ({h_szomszedos_token}), jellemzően egy héber
előtag, névelő vagy elöljáró hozzákötése a szóhoz a szabályok ellenére. A független összevetés {k_elter} eltéréséből
{k_mi} maradt a párosítás hibája; ezeket és a többi megerősített hibát az adatkészlet név szerint felsorolja.

## 4. Az adatkészlet

**Hely és azonosító.** Zenodo, DOI: {doi}; licenc: CC BY 4.0; nyelv: magyar (adat), magyar és angol (dokumentáció);
adatállapot: {adatallapot}.

**Fájlok.** `parok/` (könyvenként, kapcsolatonként egy sor: vers, a magyar szó sorszáma és alakja, az eredeti szó
sorszáma, Strong-szám, kapcsolattípus, bizonyosság, állapot, Textus Receptus-jelölés); `szavak/` (könyvenként minden
magyar és eredeti szó egyszer, állapottal: párosított, betoldás, fordítatlan, függőben); `versek.tsv` (a Károli 1908
szövege); `meres.tsv` (a mérés minden száma); kétnyelvű kódkönyv, módszertani leírás, ismert hibák, ellenőrző összeg. A
kulcs az OSIS-versazonosító és a szó sorszáma. A héber és görög szóalak nincs a csomagban: a sorszám a STEPBible
TAHOT/TAGNT szövegéhez illeszthető.

**Méret.** {konyv} könyv, {vers} vers, {par} pár ({heber_par} héber, {gorog_par} görög; ebből {morfema} morféma),
{hu_betoldas} betoldás, {er_forditatlan} fordítatlan eredeti szó, {hu_fuggoben} függőben lévő magyar szó
({fuggoben_vers} vers).

## 5. Újrahasznosítás

Az adatkészlet bibliaolvasó és -tanulmányozó alkalmazásoknak Strong-alapú keresést ad a magyar szövegen: egy héber vagy
görög szó minden Károli-megfelelője egy szűréssel összegyűjthető. Fordítástörténeti kutatásban vizsgálható a Károli
fordítói következetessége, a betoldások és a fordítatlan szavak eloszlása. Nyelvtechnológiai célra kis erőforrású
nyelvpár (magyar–héber, magyar–görög) szóillesztési adata, rétegenként mért hibával; a mintapárok és a hibatípusok
szóillesztő programok értékeléséhez is használhatók. Ugyanezek a párok a Károli modernizált szövegén is megjelennek
(https://doi.org/{doi_modern}); a két adatkészlet a vers és a szósorszám kulcsán szóról szóra összekapcsolható.

## 6. Korlátok és a következő kiadás

A párosítás gépi javaslat. A vak ellenőr maga is modell; a független összevetés csak a fő szavakat méri, és kis
klaszter-mintán; a héber morfémák párjainak ({morfema} pár) pontossága ({p_morf}%) csak a vak ellenőrrel mért. Mózes két
könyvén kívül minden pár egy modell javaslata. A Károli a Textus Receptust fordította, a párosítás alapja a TAGNT:
{nem_tr_token} párosított görög szó nem szerepel a Textus Receptusban, és jelölve van.

A közlés szerkesztői döntés: a párosítás azért jelenik meg nyílt adatként, mert a pontossága mérve és dokumentálva
van — rétegenként és kapcsolattípusonként, konfidencia-intervallummal, hibatípusokkal. Nem egy előre kitűzött küszöb
teljesülésén alapul. A 2. kiadás javítja a megerősített hibákat és a szomszédos szó szabályellenes eseteit, majd
ugyanazzal a protokollal újra mér. Minőségi célját előre rögzítettük: a független fő-szó egyezés alsó széle legalább 98%,
a vak ellenőrrel mért súlyozott egyezés alsó széle legalább 93%, és egyetlen réteg sem 90% alatti.

## Nyilatkozat a mesterséges intelligencia használatáról

A párosítást nyelvi modellek (Claude Sonnet, Gemini Flash), a vak ellenőrzést egy harmadik modell (Claude Opus) végezte,
a fent leírt módon; a modellek Strong-számot nem írtak. A szavakra bontás, a gépi kapu, a táblák összeállítása és a
statisztika determinisztikus program. A kézirat szövegét a claude-opus-5-5 modell fogalmazta az adatkészlet adataiból;
a számok az adatokból generáltak. MI-eszköz nem szerző; az adatokért és a szövegért a szerző felel.

## Hivatkozások

Demeter, T. (2026). *{cim_modern_hu}* [adatkészlet]. Zenodo. https://doi.org/{doi_modern}

STEPBible. (é. n.). *Translators Amalgamated Hebrew OT (TAHOT) és Translators Amalgamated Greek NT (TAGNT)*
[adatkészlet]. Tyndale House, Cambridge. https://www.STEPBible.org

<!-- BEKÜLDÉSI SZÖVEG VÉGE — az alábbi rész a beküldött változatból kivehető. -->

---

## Csatornajavaslat

A kézirat data paper-alakban készült (áttekintés, módszer, adatkészlet, újrahasznosítás). Két csatornatípus illik hozzá.
Az egyik egy bölcsészeti adatközlő folyóirat (például a Journal of Open Humanities Data), amelynek kimondott data
paper-típusa és MI-nyilatkozati helye van, de a terjedelme 1000–1500 szó, ezért a 2. és a 3. szakasz rövidítendő. A
másik egy nyelvi erőforrásokat közlő hely, ahol a szóillesztés kis erőforrású nyelvpárként és mért hibájú adatként kap
közönséget. Díjmentes alternatíva a nyílt adatkészletekről rövid cikket fogadó adatbányászati és digitális bölcsészeti
folyóirat. A Zenodo-letét mindhárom út előfeltétele; ugyanaz a kézirat egyszerre csak egy helyre küldhető.
"""

KEZIRAT_EN = """# Word-by-word alignment of the 1908 Károli Bible with the Hebrew and Greek source text: an open dataset with measured accuracy

*Manuscript draft (data paper) · {cim_en} · {lex_en} · DOI: {doi}*

## Abstract

The dataset links the {hu_token} words of the 1908 text of the Károli Bible, the classic Hungarian translation, to the
{er_token} words of the Hebrew and Greek source text through {par} word pairs, each carrying the Strong's number of the
source word. The alignment was produced by language models following a written rule set; the model marked positions
only, and the Strong's number comes from the open STEPBible TAHOT and TAGNT data. Accuracy was measured in two ways: with
a blind model reviewer on a random sample drawn from eight strata ({p_osszes}% on the full pair set, 95%:
{p_osszes_a}–{p_osszes_f}%), and against an independent Károli edition marked with Strong's numbers, on main-word pairs
({k_fs}%, 95%: {k_fs_a}–{k_fs_f}%). The dataset publishes the measured state, with a list of confirmed errors and a
quality target for the next release fixed in advance. Licence: CC BY 4.0.

## 1. Overview

**Context.** For four centuries the Károli translation has been the base text of Hungarian Protestant Bible reading, yet
a free, word-by-word assignment of the Hebrew and Greek words behind it has been missing. In English, the King James
text with Strong's numbers has long been a basic tool for readers and researchers; no comparable open data existed for
Hungarian. This dataset fills that gap, as one of the open data cores of the {lex_en}.

**The question it answers.** Which Hungarian word translates which source word; which Hungarian word is a translator's
addition; which source word is not rendered by a separate Hungarian word. The third question matters as much as the
first: the `szavak` table lists every word once, so the "gaps" of the translation can be read off too.

## 2. Method

**Texts and tokenisation.** The Hungarian side is the public-domain 1908 Károli text; the source side is the STEPBible
TAHOT (Hebrew and Aramaic Old Testament) and TAGNT (Greek New Testament) datasets. TAHOT treats Hebrew prefixes and
suffixes as separate words (H9001–H9049), so one Hungarian word is often linked to several source "words". Before
alignment, Károli's verse division was mapped to that of the source by deterministic alignment of verse lengths; each
merge of two verses was approved by hand.

**Alignment.** For each verse the model received numbered Hungarian and source words (the source with form, Strong's
number and English gloss) and returned pairs of positions, together with additions and untranslated words. Disputed
cases were decided by twelve written rules: on articles, split conjunctions and relative pronouns, the object marker,
possessive suffixes, separated verbal prefixes, explicit subject pronouns and auxiliaries, the Hebrew conjunction *ve-*,
and Greek words absent from the Textus Receptus. A program checked every answer (each Hungarian word exactly once, each
source word at least once, only existing positions); a failed answer was redone by the model. Genesis and Exodus were
aligned by two independent models (Claude Sonnet and Gemini Flash): where they agreed, the pair has `magas` (high)
confidence ({magas} pairs). For reasons of cost, the other books were aligned by one model, Claude Sonnet (`alacsony`,
{alacsony} pairs). The tables can be rebuilt byte-identically from the saved model answers.

**Accuracy measurement.** (1) *Blind review.* The pair set was divided into eight strata (Genesis–Deuteronomy with two
models and with one; historical, poetic and prophetic books; Gospels and Acts; Epistles; Revelation), with {reteg_n}
random pairs per stratum. A third model (Claude Opus) marked the source words for each target Hungarian word itself,
with the same rules, without seeing the machine pair. (2) *Calibration.* On an earlier manually compiled sample, the
reviewer agreed with the sample in {kal_ell}% and the machine alignment in {kal_gep}%: the reviewer is not more accurate
than the alignment, so the agreement is a lower bound only if shared errors are negligible. (3) *Independent
comparison.* Shared errors are measured against a Károli edition marked with Strong's numbers, on one full chapter per
stratum ({kulso_fejezet} chapters, {k_n} main-word pairs); the source marks the main word only, not secondary words or
morphemes. Differences were judged three ways (machine pair, source, blind reviewer). The external source's data are not
part of the dataset, only the aggregate rate.

## 3. Results

| measurement | estimate | 95% |
|---|---|---|
| full pair set, blind reviewer, weighted | {p_osszes}% | {p_osszes_a}–{p_osszes_f}% |
| of which Old / New Testament | {p_osz}% / {p_usz}% | {p_osz_a}–{p_osz_f}% / {p_usz_a}–{p_usz_f}% |
| content word / Hebrew morpheme | {p_tartalmi}% / {p_morf}% | {p_tartalmi_a}–{p_tartalmi_f}% / {p_morf_a}–{p_morf_f}% |
| main words, by the independent source | {k_fs}% | {k_fs_a}–{k_fs_f}% |
| main words, after three-way judgement | {k_h3}% | {k_h3_a}–{k_h3_f}% |

Agreement per stratum ranges from {r_OSZ_mozes_alacsony}% (Moses, one model) to {r_OSZ_mozes_magas}% (Moses, two
models agreeing); the per-stratum table is in the dataset's `meres.tsv` and its methods description. Of the {minta}
sample pairs, {elteres} differed from the reviewer; the most frequent type is the neighbouring word
({h_szomszedos_token}), typically a Hebrew prefix, article or preposition attached to the word against the rules. Of the
{k_elter} differences in the independent comparison, {k_mi} remained errors of the alignment; these and the other
confirmed errors are listed by name in the dataset.

## 4. Dataset description

**Location and identifier.** Zenodo, DOI: {doi}; licence: CC BY 4.0; language: Hungarian (data), Hungarian and English
(documentation); data state: {adatallapot}.

**Files.** `parok/` (per book, one row per link: verse, position and form of the Hungarian word, position of the source
word, Strong's number, link type, confidence, state, Textus Receptus flag); `szavak/` (per book, every Hungarian and
source word once, with its state: aligned, addition, untranslated, pending); `versek.tsv` (the 1908 Károli text);
`meres.tsv` (every figure of the measurement); bilingual codebook, methods description, known issues, checksum. The key
is the OSIS verse identifier and the word position. Hebrew and Greek word forms are not in the package: the position
matches the STEPBible TAHOT/TAGNT text.

**Size.** {konyv} books, {vers} verses, {par} pairs ({heber_par} Hebrew, {gorog_par} Greek; of these {morfema}
morphemes), {hu_betoldas} additions, {er_forditatlan} untranslated source words, {hu_fuggoben} pending Hungarian words
({fuggoben_vers} verses).

## 5. Reuse potential

For Bible reading and study applications the dataset provides Strong-based search on the Hungarian text: every Károli
rendering of a Hebrew or Greek word can be collected with one filter. In translation history, Károli's consistency and
the distribution of additions and untranslated words can be studied. For language technology it is word-alignment data
for a low-resource language pair (Hungarian–Hebrew, Hungarian–Greek) with error measured per stratum; the sample pairs
and error types can also serve to evaluate word aligners. The same pairs also appear on the modernised Károli text
(https://doi.org/{doi_modern}); the two datasets join word by word on the verse and word position key.

## 6. Limitations and the next release

The alignment is a machine proposal. The blind reviewer is itself a model; the independent comparison covers main words
only, on a small cluster sample; the accuracy of the Hebrew morpheme pairs ({morfema} pairs; {p_morf}%) is measured by
the blind reviewer only. Outside Genesis and Exodus every pair is one model's proposal. Károli translated the Textus
Receptus, while the alignment uses TAGNT: {nem_tr_token} aligned Greek words are not in the Textus Receptus, and are
flagged.

Publication rests on an editorial decision: the alignment is released as open data because its accuracy is measured and
documented — per stratum and link type, with confidence intervals and error types. It does not rest on meeting a
threshold set in advance. Release 2 will correct the confirmed errors and the rule-violating neighbouring-word cases,
then measure again with the same protocol. Its quality target was fixed in advance: lower bound of independent main-word
agreement at least 98%, lower bound of weighted agreement with the blind reviewer at least 93%, and no stratum below 90%.

## AI declaration

The alignment was done by language models (Claude Sonnet, Gemini Flash) and the blind review by a third model (Claude
Opus), as described above; the models wrote no Strong's numbers. Tokenisation, the machine gate, table assembly and the
statistics are deterministic programs. The text of the manuscript was drafted by the claude-opus-5-5 model from the
dataset's data; the figures are generated from the data. An AI tool is not an author; the author is responsible for the
data and the text.

## References

Demeter, T. (2026). *{cim_modern_en}* [dataset]. Zenodo. https://doi.org/{doi_modern}

STEPBible. (n.d.). *Translators Amalgamated Hebrew OT (TAHOT) and Translators Amalgamated Greek NT (TAGNT)* [dataset].
Tyndale House, Cambridge. https://www.STEPBible.org

<!-- END OF SUBMISSION TEXT — the part below can be removed from the submitted version. -->

---

## Venue suggestion

The manuscript is written as a data paper (overview, method, dataset, reuse). Two kinds of venue fit it. One is a
humanities data journal (for example the Journal of Open Humanities Data), with an explicit data paper type and a place
for the AI declaration, but a length of 1000–1500 words, so sections 2 and 3 would need shortening. The other is a venue
for language resources, where the alignment reaches readers as a low-resource language pair with measured error. A
fee-free alternative is a data mining and digital humanities journal that accepts short articles on open datasets. A
Zenodo deposit is a precondition for all three; the same manuscript may be submitted to only one venue at a time.
"""

KOZLEMENY += [
    ('kezirat_hu.md', KEZIRAT_HU, 'hu'),
    ('kezirat_en.md', KEZIRAT_EN, 'en'),
]
