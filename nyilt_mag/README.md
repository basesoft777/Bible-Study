# Logosz Lexikon — open data core: biblical motifs

<!-- GENERATED: export of the Logosz Lexikon open data core, generated from the project data; do not edit by hand. -->

An open dataset of biblical motifs: the defining and excluding features of the motifs, their occurrences on the words of the Hebrew and Greek text, the passages examined but excluded with reasons, the relations between passages, and the decision log. One of the open data cores of the Logosz Lexikon. *Magyar változat: `OLVASSEL.md`.*

- **Licence:** CC BY 4.0 (`LICENSE`); the `cc_by_sa_reteg/` directory is under a separate licence, CC BY-SA 4.0. Attribution of the third-party data used, and the excluded sources: `ATTRIBUCIO.md`.
- **DOI:** 10.5281/zenodo.24141612 — release identifier and content hash: `RELEASE.txt`.
- **Author:** Demeter Tamás (ORCID 0009-0005-9254-9731).

## Contents

| file | content | rows |
|---|---|---:|
| `motivumok.tsv` | the motifs: title, definition, carrier of identity, exclusion criterion, superordinate concept, processing stage | 9 |
| `elofordulasok.tsv` | the occurrences: passage, anchor word and its Strong's number, dictionary meaning, Károli word, provenance | 250 |
| `beepitesi_dontesek.tsv` | the inclusion decisions, with rationale | 252 |
| `kizarasok.tsv` | the passages examined but excluded, with reason and rationale; a summary row stands for a group | 540 |
| `kizaras_csoportok.tsv` | every verse of the summary-row groups | 3,984 |
| `kapcsolatok.tsv` | relations between passages within a motif | 88 |
| `motivum_kapcsolatok.tsv` | relations between two motifs | 3 |
| `dontesnaplo.tsv` | the editorial decisions referred to (`NYD-nnn`) | 15 |
| `visszhang_megfelelok.tsv` | the counterparts of the anchor words in the Targum, the Vulgate and the Septuagint | 101 |
| `visszhang_tanuk.tsv` | patristic, rabbinic and Glossa Ordinaria witnesses, without quotation | 6 |
| `vitatott_forrasok.tsv` | the peer-reviewed literature on the disputed points (bibliographic data) | 3 |
| `sblgnt_apparatus.tsv` | the critical apparatus of the SBL Greek New Testament for the New Testament passages | 61 |
| `forrasok_es_licencek.tsv` | the project's source inventory: licence and role in the package | 65 |
| `kodkonyv.tsv` | description of the columns, values and codes (Hungarian and English) | 440 |
| `KODKONYV.md` | the same in readable form |  |
| `cc_by_sa_reteg/szemantikai_domenek.tsv` | semantic domains (UBS SDBH/SDGNT), **separate licence: CC BY-SA 4.0** | 231 |
| `cc_by_sa_reteg/OLVASSEL.md` | licence and attribution of the separate layer |  |
| `METHODS.md` | how the data were made (Hungarian: `MODSZER.md`) |  |
| `KNOWN_ISSUES.md` | known issues and limitations (Hungarian: `ISMERT_HIBAK.md`) |  |
| `ATTRIBUCIO.md` | attribution, licences, excluded sources |  |
| `LICENSE` | the licence of the package |  |
| `CITATION.cff` | citation metadata |  |
| `RELEASE.txt` | release identifier and content hash (Hungarian: `KIADAS.txt`) |  |
| `ELLENORZO_OSSZEG.sha256` | SHA-256 checksum of every file |  |

## In numbers

- 9 motifs: 1 closed release(s), 8 earlier processing, being rewritten; their data stay in the package (`motivumok.tsv`, `feldolgozasi_allapot`).
- 250 occurrences and 252 inclusion decisions.
- 540 exclusion rows with 61 reasons: 443 passages decided one by one, and 97 summary rows standing for 3,984 verses.
- 88 relations between passages, 3 relations between motifs, 15 public editorial decisions.
- In the echo layer: 101 counterparts, 6 witnesses, 3 disputed points and 61 apparatus notes.

**Known issues:** `KNOWN_ISSUES.md`. **Methods:** `METHODS.md`.

## How to read

Three questions, step by step, on the motif `HAMART-001`. The numbers in the answers are generated from this release. The column names and values are Hungarian: next to each closed-vocabulary column the `_en` column gives the English label, next to each passage column the `_osis` column gives the OSIS reference, and every column is explained in `KODKONYV.md`.

### 1. Which verses belong to HAMART-001, and on which word?

1. Open `elofordulasok.tsv` and filter the `motivum_azonosito` column on `HAMART-001`.
2. The result is 47 rows: each row is one verse (`igehely`).
3. The `horgony` column gives the Hebrew or Greek word (Strong's number or word combination) the verse rests on: `H0127` (10 rows), `H7843` (7 rows), `málé + chámász` (6 rows), and 13 further anchors. The `karoli_szo` column gives the corresponding word of the Károli translation (e.g. 1Móz 12:3: "megátkozom").
4. The processing stage of the motif is in the `feldolgozasi_allapot` column of `motivumok.tsv`: "lezárt kiadás".

### 2. Why is 1Móz 9:25 not included?

1. Open `kizarasok.tsv` and filter on `motivum_azonosito` = `HAMART-001` and `igehely` = `1Móz 9:25` (`jelolt_tipus` = `elofordulas`).
2. The `kizaras_oka` column: "emberi átkozódás, nem a genezisi lánc folytatása". The `indoklas` column states the reason in full.
3. The `dontesek` column (`NYD-010`) is the public identifier of the decision; its text is in `dontesnaplo.tsv`.

### 3. Was every place where the words of the motif occur examined?

1. Among the `HAMART-001` rows of `kizarasok.tsv`, those with a filled `csoport_versszam` column are summary rows: there are 76. Each stands for a group of verses excluded for one reason: "más szó áll a versben, nem a motívum lexémája" (573 verses, first verse: 1Kir 1:52); "a szó áll, de általános használatban, a lánc nélkül" (255 verses, first verse: 1Kir 8:36); "a szó áll, de általános használatban, a lánc nélkül" (174 verses, first verse: 1Kir 7:46); and 73 further groups.
2. `kizaras_csoportok.tsv` lists every verse of these groups (filter: `motivum_azonosito` = `HAMART-001`): 1520 verses.
3. Together: 47 occurrences, 212 verses excluded one by one and 1520 verses excluded in groups, 1779 verses with a decision in all. Candidates not yet decided are not in the package; their number is given under "What is in it and what is not".

## What is in it and what is not (the data core and the lexicon)

The open data core is the data layer of the lexicon; the lexicon itself (its interpretive text, the Hungarian translation of the dictionaries, and the printed volume) is a separate work, all rights reserved.

**Included (data layer):** the motif identifier, title and exclusion criterion; the occurrences (passage, lexical base, dictionary meaning, Károli word); the exclusions and inclusion decisions with rationale; the relations; provenance (the naming of the source, its licence, the type of query, the date); the decision log.

**Not included (the lexicon):** the interpretive prose (summary, interpretation, passage-by-passage exposition), the Hungarian dictionary translations, the volume material and the lexicon pages.

**Also not in the package:** candidates not yet decided (20); the text of the sources (quotation); internal working marks (identifiers, working files, query traces). Where a row refers to a decision, the public identifier (`NYD-nnn`) can be resolved in `dontesnaplo.tsv`.

## Citation and place of publication

**Cite as:** Demeter Tamás (ORCID: 0009-0005-9254-9731): Logosz Lexikon — open data core: biblical motifs. DOI: 10.5281/zenodo.24141612. Citation metadata: `CITATION.cff`.

The canonical place of publication of the package: `https://doi.org/10.5281/zenodo.24141612`. A version is identified by the release identifier (`RELEASE.txt`: the date of the data state and the content hash), not by a development repository or a commit. The website of the lexicon: `https://logoszlexikon.hu`.

## Related datasets

- Károli 1908 – Strong word alignment: https://doi.org/10.5281/zenodo.24141884
- Modernised Károli – Strong: https://doi.org/10.5281/zenodo.24141950

The full Strong's alignment of the Károli text is in these; this package gives only the Károli counterpart of the motif word.

## Verification

The file `ELLENORZO_OSSZEG.sha256` contains the SHA-256 sum of every released file; rerunning the export is byte-identical. The `kozlemeny/` folder holds the draft announcement; it is not part of the release.
