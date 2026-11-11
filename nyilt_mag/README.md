# [A LEXIKON CÍME] — Open Core — Read Me

# GENERATED: export of the [A LEXIKON CÍME] open core (CC BY 4.0), generated from the project data — do not edit by hand; a line starting with "#" is a comment.

*Magyar változat: `OLVASSEL.md`.*

**Licence:** CC BY 4.0 (the open core's own data and text). The contents of the `cc_by_sa_reteg/` directory are under a separate licence, CC BY-SA 4.0; see the `OLVASSEL.md` there.

**What this is.** The open core of a study of biblical motifs (the PaRDeS method): the defining features of the motifs, the list of occurrences, the excluded passages with reasons, the relations between passages and the decision log. The files are reader-facing views generated from the data; working marks are resolved. The columns and codes are described in `kodkonyv.tsv` / `KODKONYV.md` (Hungarian and English).

**Processing stage.** Of the motifs, 3 are closed releases (their lexicon page is released and passed the reader check without error) and 6 come from an earlier stage and will be updated in later versions; the `feldolgozasi_allapot` column of `motivumok.tsv` gives the stage of each motif.

**Known errors:** see `KNOWN_ISSUES.md`.

## How to read

Three questions, step by step, on the motif `ISTENTISZT-001`. The numbers in the answers are generated from this release. The column names and values are Hungarian: next to each closed-vocabulary column the `_en` column gives the English label, next to each passage column the `_osis` column gives the OSIS reference, and every column is explained in `KODKONYV.md`.

### 1. Which verses belong to ISTENTISZT-001, and on which word?

1. Open `elofordulasok.tsv` and filter the `motivum_azonosito` column on `ISTENTISZT-001`.
2. The result is 22 rows: each row is one verse (`igehely`).
3. The `horgony` column gives the Hebrew or Greek word (Strong's number) the verse rests on: `H7121 + H8034` (16 rows), `G1941` (6 rows). The `karoli_szo` column gives the corresponding word of the Károli translation (e.g. 1Kir 18:24: "segítségül hívom az Úrnak nevét").
4. The processing stage of the motif is in the `feldolgozasi_allapot` column of `motivumok.tsv`: "lezárt kiadás".

### 2. Why is Róm 10:12 not included?

1. Open `kizarasok.tsv` and filter on `motivum_azonosito` = `ISTENTISZT-001` and `igehely` = `Róm 10:12` (`jelolt_tipus` = `elofordulas`).
2. The `kizaras_oka` column: "név nélküli forma". The `indoklas` column states the reason in full.
3. The `dontesek` column (`NYD-005`) is the public identifier of the decision; its text is in `dontesnaplo.tsv`.

### 3. Was every place where the word pair occurs examined?

1. Among the `ISTENTISZT-001` rows of `kizarasok.tsv`, those with a filled `csoport_versszam` column are summary rows: there are 5. Each stands for a group of verses excluded for one reason: "a hívás igéje a név nélkül" (246 verses, first verse: 1Móz 1:5); "elnevezés, nem a név segítségül hívása" (126 verses, first verse: 1Móz 2:19); "a Károli-szó más szót fordít" (51 verses, first verse: 2Móz 18:4); "a hívás és a név nem egy szerkezetben" (21 verses, first verse: 1Móz 41:52); "nem JHVH áll a név után" (12 verses, first verse: 2Móz 31:2).
2. `kizaras_csoportok.tsv` lists every verse of these groups (filter: `motivum_azonosito` = `ISTENTISZT-001`): 456 verses.
3. Together: 22 occurrences, 104 verses excluded one by one and 456 verses excluded in groups, 582 verses with a decision in all. Candidates not yet decided are not in the package; their number is given under "What is not in the package".

## Files and their row counts

| File | Rows |
|---|---|
| `beepitesi_dontesek.tsv` | 252 |
| `cc_by_sa_reteg/szemantikai_domenek.tsv` | 231 |
| `dontesnaplo.tsv` | 11 |
| `elofordulasok.tsv` | 250 |
| `forrasok_es_licencek.tsv` | 63 |
| `kapcsolatok.tsv` | 88 |
| `kizaras_csoportok.tsv` | 3984 |
| `kizarasok.tsv` | 540 |
| `kodkonyv.tsv` | 359 |
| `motivum_kapcsolatok.tsv` | 3 |
| `motivumok.tsv` | 9 |

## Licence filtering

The filtering follows the project's licence inventory. **Excluded sources** (the package contains no value from them): `BDB_forditas`, `Cremer_nyers`, `Girdlestone`, `Heber_ETCBC_modulok`, `KJV_ASV_Strongs`, `KJV_Strongs_teljes`, `KJV_teljes_szoveg`, `Karoli_Strong_kivonat`, `Karoli_versmegfeleltetes`, `LSJ`, `LXX_kivonat`, `LXX_lexicon`, `LXX_versszintu_parok`, `MCGED`, `SDBH_SDGNT_segedtablak`, `UBS_DBH`, `UBS_DNTG`, `karoli_modern`, `karoli_variancia`, `lexikonok_nyers`, `simplemma_nyelvi_adat`, `szoto_tablak`, `tW_szocikkek`. The reason for each is given in the `ok` column of `forrasok_es_licencek.tsv` (non-commercial or GPL licence, unclear licence, the project's closed derived layer). This is an inventory, not a legal opinion.

## Place of publication

The canonical place of publication of the package: `<KANONIKUS_FORRAS_URL>` (a placeholder, filled in at publication). A version is identified by the release identifier (`RELEASE.txt`: the date of the data state and the content hash), not by a development repository or a commit.

## Citation and the use of artificial intelligence

With the release, citation metadata (Citation File Format) and a statement on the use of artificial intelligence are provided at the place of publication; their fields to be completed by the author are placeholders until publication. The statement separates two layers: the open data core (CC BY 4.0, this package) and the lexicon as a separate work (all rights reserved).

## English layer

The column names and values of the package are Hungarian; English parallel columns stand next to them. **Passages:** next to every passage column, `…_osis` (an OSIS reference, e.g. `1Kgs.13.31`); the book code is standard, chapter and verse follow the versification of the Károli translation — where it differs from the KJV or STEPBible numbering, the key denotes the Károli verse. **Closed values:** next to every closed-vocabulary column, `…_en`, with the edited English label of the codebook. **Free text** (rationale, function, the definition of the motif, the decision log): an `…_en` parallel field, a **machine translation**; the row’s `forditas_modja` column names the model and states any gap. **Word cue:** the `strong_glossza_en` column of `elofordulasok.tsv` is the STEPBible gloss of the Strong number (Data created by www.STEPBible.org based on work at Tyndale House Cambridge, CC BY 4.0); `jelentes_en` is separate, a dictionary excerpt.

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
