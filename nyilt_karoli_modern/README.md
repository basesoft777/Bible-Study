# Modernised Károli – Strong — open dataset

A modernised version of the 1908 text of the Károli Bible (the classic Hungarian translation), linked word by word
to the Hebrew and Greek source words and their Strong's numbers. One of the open data cores of the Logosz Lexikon.

- **Licence:** CC BY 4.0 (`LICENSE`); attribution of the third-party data used: `ATTRIBUCIO.md`.
- **DOI:** 10.5281/zenodo.24141950 — release identifier and content hash: `RELEASE.txt`.
- **Author:** Demeter Tamás (ORCID 0009-0005-9254-9731).

## Contents

| file | content |
|---|---|
| `konyvek/NN_Book.tsv` | per book: every word in its 1908 and modern form, with the Strong's numbers aligned to it |
| `versek.tsv` | the modernised text, verse by verse |
| `kodkonyv.tsv`, `KODKONYV.md` | description of the columns and values (Hungarian and English) |
| `METHODS.md`, `MODSZER.md` | how the modernisation and the Strong linkage were made |
| `KNOWN_ISSUES.md`, `ISMERT_HIBAK.md` | known issues and limitations |
| `ATTRIBUCIO.md` | attribution and licences |
| `CITATION.cff` | citation metadata |
| `ELLENORZO_OSSZEG.sha256` | SHA-256 checksum of every file |

## In numbers

- 66 books, 31,158 verses, 599,367 words (tokens); 64,388 words and 21,636 verses changed in
  the modernisation.
- 598,715 word pairs (Hungarian word – Hebrew or Greek word, with Strong's number) on 488,659 Hungarian
  words; 109,914 words are translator's additions (no source word), 794 words are pending alignment.

## Quick guide

The key is the OSIS verse identifier (`Gen.1.1`) and the position of the word within the verse (`token`). A word
appears in as many rows as source words it is aligned to; a word without a pair appears in one row. To read the
modern text, take the rows with an empty `kieso` column in `token` order, once per word; the punctuated text is in
`versek.tsv`.

The alignment is a machine proposal with measured accuracy (`METHODS.md`, section 5); the `bizonyossag` column marks
where two independent models agreed.

## Related datasets

- Károli 1908 – Strong word alignment: https://doi.org/10.5281/zenodo.24141884
- The open data core of the Logosz Lexikon (motifs): https://doi.org/10.5281/zenodo.24141612
