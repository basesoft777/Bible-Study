# Logosz Lexikon — Open Core — Read Me

# GENERATED: export of the Logosz Lexikon open core (CC BY 4.0), generated from the project data — do not edit by hand; a line starting with "#" is a comment.

*Magyar változat: `OLVASSEL.md`.*

**Licence:** CC BY 4.0 (the open core's own data and text). The contents of the `cc_by_sa_reteg/` directory are under a separate licence, CC BY-SA 4.0; see the `OLVASSEL.md` there.

**What this is.** The open core of a study of biblical motifs (the PaRDeS method): the defining features of the motifs, the list of occurrences, the excluded passages with reasons, the relations between passages and the decision log. The files are reader-facing views generated from the data; working marks are resolved. The columns and codes are described in `kodkonyv.tsv` / `KODKONYV.md` (Hungarian and English).

**Processing stage.** Of the motifs, 4 are closed releases (their lexicon page is released and passed the reader check without error) and 5 come from an earlier stage and will be updated in later versions; the `feldolgozasi_allapot` column of `motivumok.tsv` gives the stage of each motif.

**Known errors:** see `KNOWN_ISSUES.md`.

## How to read

Three questions, step by step, on the motif `ISTENTISZT-001`. The numbers in the answers are generated from this release. The column names and values are Hungarian: next to each closed-vocabulary column the `_en` column gives the English label, next to each passage column the `_osis` column gives the OSIS reference, and every column is explained in `KODKONYV.md`.

### 1. Which verses belong to ISTENTISZT-001, and on which word?

1. Open `elofordulasok.tsv` and filter the `motivum_azonosito` column on `ISTENTISZT-001`.
2. The result is 20 rows: each row is one verse (`igehely`).
3. The `horgony` column gives the Hebrew or Greek word (Strong's number) the verse rests on: `H7121 + H8034` (16 rows), `G1941` (4 rows). The `karoli_szo` column gives the corresponding word of the Károli translation (e.g. 1Kir 18:24: "segítségül hívom az Úrnak nevét").
4. The processing stage of the motif is in the `feldolgozasi_allapot` column of `motivumok.tsv`: "lezárt kiadás".

### 2. Why is Róm 10:12 not included?

1. Open `kizarasok.tsv` and filter on `motivum_azonosito` = `ISTENTISZT-001` and `igehely` = `Róm 10:12` (`jelolt_tipus` = `elofordulas`).
2. The `kizaras_oka` column: "név nélküli forma". The `indoklas` column states the reason in full.
3. The `dontesek` column (`NYD-005`) is the public identifier of the decision; its text is in `dontesnaplo.tsv`.

### 3. Was every place where the word pair occurs examined?

1. Among the `ISTENTISZT-001` rows of `kizarasok.tsv`, those with a filled `csoport_versszam` column are summary rows: there are 6. Each stands for a group of verses excluded for one reason: "a hívás igéje a név nélkül" (246 verses, first verse: 1Móz 1:5); "elnevezés, nem a név segítségül hívása" (126 verses, first verse: 1Móz 2:19); "a Károli-szó más szót fordít" (51 verses, first verse: 2Móz 18:4); "a hívás és a név nem egy szerkezetben" (21 verses, first verse: 1Móz 41:52); "passzív szerkezet vagy megnevezés (negatív kritérium)" (14 verses, first verse: 5Móz 12:5); "nem az Úr neve áll a név után" (12 verses, first verse: 2Móz 31:2).
2. `kizaras_csoportok.tsv` lists every verse of these groups (filter: `motivum_azonosito` = `ISTENTISZT-001`): 470 verses.
3. Together: 20 occurrences, 109 verses excluded one by one and 470 verses excluded in groups, 599 verses with a decision in all. Candidates not yet decided are not in the package; their number is given under "What is not in the package".

## Files and their row counts

| File | Rows |
|---|---|
| `beepitesi_dontesek.tsv` | 250 |
| `cc_by_sa_reteg/szemantikai_domenek.tsv` | 231 |
| `dontesnaplo.tsv` | 15 |
| `elofordulasok.tsv` | 248 |
| `forrasok_es_licencek.tsv` | 65 |
| `kapcsolatok.tsv` | 86 |
| `kizaras_csoportok.tsv` | 3998 |
| `kizarasok.tsv` | 546 |
| `kodkonyv.tsv` | 440 |
| `motivum_kapcsolatok.tsv` | 3 |
| `motivumok.tsv` | 9 |
| `sblgnt_apparatus.tsv` | 60 |
| `visszhang_megfelelok.tsv` | 130 |
| `visszhang_tanuk.tsv` | 8 |
| `vitatott_forrasok.tsv` | 3 |

## Licence filtering

The filtering follows the project's licence inventory. **Excluded sources** (the package contains no value from them): `BDB_forditas`, `Chain_Lineage_Browser`, `Cremer_nyers`, `Girdlestone`, `Heber_ETCBC_modulok`, `KJV_ASV_Strongs`, `KJV_Strongs_teljes`, `KJV_teljes_szoveg`, `Karoli_Strong_kivonat`, `Karoli_versmegfeleltetes`, `LSJ`, `LXX_kivonat`, `LXX_lexicon`, `LXX_versszintu_parok`, `MCGED`, `SDBH_SDGNT_segedtablak`, `UBS_DBH`, `UBS_DNTG`, `karoli_modern`, `karoli_variancia`, `lexikonok_nyers`, `simplemma_nyelvi_adat`, `szoto_tablak`, `tW_szocikkek`. The reason for each is given in the `ok` column of `forrasok_es_licencek.tsv` (non-commercial or GPL licence, unclear licence, the project's closed derived layer). This is an inventory, not a legal opinion.

## Place of publication

The canonical place of publication of the package: `https://doi.org/10.5281/zenodo.24141612` (the DOI of the open data core: 10.5281/zenodo.24141612). The website of the lexicon: `https://logoszlexikon.hu`. A version is identified by the release identifier (`RELEASE.txt`: the date of the data state and the content hash), not by a development repository or a commit. The pairing of the Károli text with Strong numbers is a separate dataset (DOI: 10.5281/zenodo.24141884); it is not part of this package.

## Citation and the use of artificial intelligence

**Cite as:** Demeter Tamás (ORCID: 0009-0005-9254-9731): Logosz Lexikon — open data core. DOI: 10.5281/zenodo.24141612.

With the release, citation metadata (Citation File Format) and a statement on the use of artificial intelligence are provided at the place of publication. The statement separates two layers: the open data core (CC BY 4.0, this package) and the lexicon as a separate work (all rights reserved).

## English layer

The column names and values of the package are Hungarian; English parallel columns stand next to them. **Passages:** next to every passage column, `…_osis` (an OSIS reference, e.g. `1Kgs.13.31`); the book code is standard, chapter and verse follow the versification of the Károli translation — where it differs from the KJV or STEPBible numbering, the key denotes the Károli verse. **Closed values:** next to every closed-vocabulary column, `…_en`, with the edited English label of the codebook. **Free text** (rationale, function, the definition of the motif, the decision log): an `…_en` parallel field, a **machine translation**; the row’s `forditas_modja` column names the model and states any gap. **Word cue:** the `strong_glossza_en` column of `elofordulasok.tsv` is the STEPBible gloss of the Strong number (Data created by www.STEPBible.org based on work at Tyndale House Cambridge, CC BY 4.0); `jelentes_en` is separate, a dictionary excerpt.

## Reception history (the echo layer)

Four files give the echo of the motifs in the ancient translations and interpreters, with the licence for each source: `visszhang_megfelelok.tsv` (the counterparts of the chain words in the Targum, the Vulgate and the Septuagint), `visszhang_tanuk.tsv` (patristic, rabbinic and Glossa Ordinaria witnesses: who, in which work, what they see in the passage; no quotation, one sentence in our own words), `vitatott_forrasok.tsv` (the peer-reviewed literature on the disputed points: bibliographic data only; an empty author denotes a gap row: no peer-reviewed source on the question was found in the databases searched for that point) and `sblgnt_apparatus.tsv` (the critical apparatus for the New Testament passages). Only verified rows are included: of the Septuagint counterparts, those where a single lemma comes into question in the verse were verified by machine; all other rows were checked by a second hand.

**Not included:** the witnesses of the Chain Lineage Browser (the browser states no licence) and the cognate-language rows of the BDB (they await a separate decision). The text of the sources (quotation) is not in the package, only factual data and one sentence in our own words.

**Credits.** SBL Greek New Testament, Copyright 2010 Society of Biblical Literature and Logos Bible Software, CC BY 4.0 (https://sblgnt.com): the notes of `sblgnt_apparatus.tsv`. Sefaria, CC BY: the rabbinic witness (changes: filtering and conversion to Károli numbering). The Septuagint counterparts rest on the OpenScriptorium LXX-morph data (CC BY 4.0; the Rahlfs text is public domain). The metadata of the patristic witnesses come from the HistoricalChristianFaith collection (the collection’s public-domain dedication covers the compilation and the metadata; the quotation texts are not in the package). The text of the Targum (Sefaria edition), the Vulgate (Clementine) and the Glossa Ordinaria (Migne) is in the public domain.

## Group exclusion

Some rows of `kizarasok.tsv` are **summary rows**: they name the first verse of a group (verses excluded for the same reason), the `csoport_versszam` column gives the number of verses in the group, and `kizaras_csoportok.tsv` lists all verses of the group. The rationale of a summary row applies to the whole group.

## What is in it and what is not (the data core and the lexicon)

The open data core is the data layer of the lexicon; the lexicon itself (its interpretive text, the Hungarian translation of the dictionaries, and the printed volume) is a separate work, all rights reserved.

**Included (data layer):** the motif identifier, title and exclusion criterion; the occurrences (passage, lexical base, dictionary meaning, Károli word); the exclusions and inclusion decisions with rationale; the relations; provenance (the naming of the source, its licence, the type of query, the date); the decision log.

**Not included (the lexicon):** the interpretive prose (summary, interpretation, passage-by-passage exposition), the Hungarian dictionary translations, the volume material and the lexicon pages.

## What is not in the package

- Candidates in the `nyitva` (open, not yet decided) state: 20.
- The text of the lexicon (interpretive prose, Hungarian dictionary translations, Károli text with Strong's numbers), the studies and the lexicon pages.
- Internal working marks: identifiers, working files, query traces. Where a decision is referred to, the public identifier (`NYD-nnn`) can be resolved in `dontesnaplo.tsv`.

## Verification

The file `ELLENORZO_OSSZEG.sha256` contains the SHA-256 sum of every file; rerunning the export is byte-identical.
