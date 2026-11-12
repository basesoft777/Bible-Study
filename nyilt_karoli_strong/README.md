# Károli 1908 – Strong word alignment — open dataset

The 1908 text of the Károli Bible (the classic Hungarian translation), linked word by word to the Hebrew and Greek
source words and their Strong's numbers. One of the open data cores of the Logosz Lexikon.

This folder is the root of a self-contained public repository: its content can be uploaded unchanged, and every file
in it is part of the release (except the `kozlemeny/` subfolder, a draft until publication).

- **Licence:** CC BY 4.0 (`LICENSE`); attribution of the third-party data used: `ATTRIBUCIO.md`.
- **DOI:** 10.5281/zenodo.24141884 — release identifier and content hash: `RELEASE.txt`.
- **Author:** Demeter Tamás (ORCID 0009-0005-9254-9731).

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

- 66 books, 31,158 verses; 599,367 Hungarian and 611,396 source words (tokens).
- 598,715 word pairs on 488,659 Hungarian words (466,785 Hebrew, 131,930 Greek pairs; of these 157,163
  are Hebrew prefix or suffix morphemes).
- 109,914 Hungarian words are translator's additions, 63,017 source words are not rendered by a
  separate Hungarian word; 794 Hungarian and 794 source words are pending (45 verses).
- Accuracy: on main-word pairs 98.72% against an independent source (95%: 98.22–99.08%); on the full pair set
  95.06% agreement with a blind reviewer (95%: 93.81–96.32%); details: `meres.tsv`, `METHODS.md` 5.

## Quick guide

The key is the OSIS verse identifier (`Gen.1.1`) and the position of the word within the verse (`token`). Each row of
the `parok` table is one link; a Hungarian word appears in as many rows as source words it is linked to. The `szavak`
table lists every word exactly once, the two sides separately (`oldal` = `hu` or `er`): it shows what has no pair. The
Hebrew and Greek word forms are not in the package; a source word is identified by its position and Strong's number,
and the position matches the STEPBible TAHOT/TAGNT text.

Every pair is a machine proposal with measured accuracy (`allapot` = `javaslat`); the `bizonyossag` column marks where
two independent models agreed.

## Related datasets

- Modernised Károli – Strong (the same pairs on the modernised text): https://doi.org/10.5281/zenodo.24141950
- The open data core of the Logosz Lexikon (motifs): https://doi.org/10.5281/zenodo.24141612
