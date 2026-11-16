# Károli 1908 – Strong word alignment — open dataset

The 1908 text of the Károli Bible (the classic Hungarian translation), linked word by word to the Hebrew and Greek
source words and their Strong's numbers. One of the open data cores of the Logosz Lexikon.

Every file of the package is part of the release. Hungarian-language introduction: `docs/hu/OLVASSEL.md`.

- **Licence:** CC BY 4.0 (`LICENSE`); attribution of the third-party data used: `docs/en/ATTRIBUTION.md`.
- **DOI:** 10.5281/zenodo.24141883 — release identifier and content hash: `RELEASE.txt`.
- **Author:** Demeter Tamás (ORCID 0009-0005-9254-9731).

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

- 66 books, 31,158 verses; 599,367 Hungarian and 611,396 source words (tokens).
- 598,715 word pairs on 488,659 Hungarian words (466,785 Hebrew, 131,930 Greek pairs; of these 157,163
  are Hebrew prefix or suffix morphemes).
- 109,914 Hungarian words are translator's additions, 63,017 source words are not rendered by a
  separate Hungarian word; 794 Hungarian and 794 source words are pending (45 verses).
- Accuracy: on main-word pairs 98.72% against an independent source (95%: 98.22–99.08%); on the full pair set
  95.06% agreement with a blind reviewer (95%: 93.81–96.32%); details: `data/meres.tsv`, `docs/en/METHODS.md` 5.

## Quick guide

The key is the OSIS verse identifier (`Gen.1.1`) and the position of the word within the verse (`token`). Each row of
the `parok` table is one link; a Hungarian word appears in as many rows as source words it is linked to. The `szavak`
table lists every word exactly once, the two sides separately (`oldal` = `hu` or `er`): it shows what has no pair. The
Hebrew and Greek word forms are not in the package; a source word is identified by its position and Strong's number,
and the position matches the STEPBible TAHOT/TAGNT text.

Every pair is a machine proposal (`allapot` = `javaslat`), with the measured accuracy given above; the accuracy per
stratum and link type is in `data/meres.tsv`.

## Using the two datasets together

This dataset and Modernised Károli – Strong (https://doi.org/10.5281/zenodo.24141949) describe the same words of the 1908 text and can be joined
row by row.

- **Common key.** `osis` + `token`: the position of a word in the 1908 text. A row of `data/konyvek/NN_Konyv.tsv` in the modernised dataset extends the rows of `data/parok/NN_Konyv.tsv` here: the same `token`, `eredeti_token`, `strong` and `kapcsolat`, and next to them `alak_modern`, `valtozott`, `kieso` and `gazda_token`. A word without a pair has one row there, with empty `strong` and `eredeti_token`.
- **Reading the modernised text.** Take the rows of `data/konyvek/NN_Konyv.tsv` with an empty `kieso` column in `token`
  order, once per word, and read `alak_modern`. A row with a `kieso` value is a word that drops out of the modern text;
  its `gazda_token` is the position of the host word in the same verse, and its Strong's number belongs to that host
  word in the modern text.
- **The source side.** The complete list of the source words, including the Hebrew and Greek words that the Károli
  does not translate with a separate Hungarian word, is only in the `data/szavak/NN_Konyv.tsv` table of this dataset (`oldal` = `er`); join it on `osis` + `eredeti_token`.

**Example: Genesis 1:1 (`Gen.1.1`), the first three words.** Word alignment (`data/parok/01_Gen.tsv`):

| `token` | `alak_1908` | `eredeti_token` | `strong` | `kapcsolat` |
|---|---|---|---|---|
| 1 | Kezdetben | 1 | H9003 | morfema |
| 1 | Kezdetben | 2 | H7225 | szo |
| 2 | teremté | 3 | H1254 | szo |
| 3 | Isten | 4 | H0430 | szo |

The modernised dataset (`data/konyvek/01_Gen.tsv`), the same words:

| `token` | `alak_1908` | `alak_modern` | `valtozott` | `eredeti_token` | `strong` | `kapcsolat` |
|---|---|---|---|---|---|---|
| 1 | Kezdetben | Kezdetben |  | 1 | H9003 | morfema |
| 1 | Kezdetben | Kezdetben |  | 2 | H7225 | szo |
| 2 | teremté | teremtette | igen | 3 | H1254 | szo |
| 3 | Isten | Isten |  | 4 | H0430 | szo |

The source words, the first five (`data/szavak/01_Gen.tsv`, `oldal` = `er`):

| `token` | `allapot` | `partner_token` | `strong` |
|---|---|---|---|
| 1 | parositva | 1 | H9003 |
| 2 | parositva | 1 | H7225 |
| 3 | parositva | 2 | H1254 |
| 4 | parositva | 3 | H0430 |
| 5 | forditatlan |  | H0853 |

Source word 5 (`H0853`) has `allapot` = `forditatlan`: it has no row in `data/parok/`, and appears only in `data/szavak/`.

## Related datasets

- Modernised Károli – Strong (the same pairs on the modernised text): https://doi.org/10.5281/zenodo.24141949
- The open data core of the Logosz Lexikon (motifs): https://doi.org/10.5281/zenodo.24141611
