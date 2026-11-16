# Codebook

*Modernised Károli – Strong*

## `data/konyvek/NN_Konyv.tsv`

| column | value | description |
|---|---|---|
| `osis` |  | OSIS verse identifier (book.chapter.verse), in Károli versification. |
| `token` |  | Position of the word in the verse (from 1), counted on the 1908 text; (osis, token) is the word key. |
| `alak_1908` |  | Word form in the 1908 Károli text. |
| `alak_modern` |  | Modernised word form; empty if the word drops out of the modern text (see kieso). |
| `valtozott` | `igen` | The modern form differs from the 1908 form, or the word drops out. |
| `kieso` | `osszevonva` | The word merged with the following one (a kik → akik); the modern form is on the host word. |
| `kieso` | `segedige` | Auxiliary "vala", dropped in the modern past tense (mondja vala → mondta); the host word is the verb. |
| `gazda_token` |  | For a dropped word, the position of its host word in the same verse; its Strong pair belongs to that word in the modern text. |
| `bizonytalan` | `igen` | The modern form is regular, but the choice depends on context (e.g. definite or indefinite conjugation); treat with care. |
| `allapot` | `javaslat` | The row is a word pair: a machine alignment proposal with measured accuracy (docs/en/METHODS.md 5). |
| `allapot` | `betoldas` | Translator's addition: the word has no Hebrew or Greek counterpart. |
| `allapot` | `fuggoben` | Alignment of the word is pending (awaiting a manual decision); no pair. |
| `strong` |  | Strong's number of the aligned source word (H… Hebrew, G… Greek), from STEPBible TAHOT/TAGNT; "+" joins two numbers for a compound source word. |
| `eredeti_token` |  | Position of the source word in the TAHOT/TAGNT verse (keyed to the Károli verse). |
| `kapcsolat` | `szo` | The pair links the Hungarian word to a source word. |
| `kapcsolat` | `morfema` | The pair links it to a Hebrew prefix or suffix morpheme (H9001–H9049: article, conjunction, preposition). |

## `data/versek.tsv`

| column | value | description |
|---|---|---|
| `osis` |  | OSIS verse identifier. |
| `szoveg_modern` |  | Modernised verse text, with punctuation. |
| `valtozott` | `igen` | The verse text changed in the modernisation. |
| `valtozott` | `nem` | The verse text is unchanged. |
