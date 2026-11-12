# Known Errors in the Source Data

# GENERATED: export of the Logosz Lexikon open core (CC BY 4.0), generated from the project data — do not edit by hand; a line starting with "#" is a comment.

The makers of the open core state here the source errors that their own measurements revealed, and how the package handles them. A gap is not filled: where a source is faulty or incomplete, an empty result is not a negative finding.

## 1. Károli cross-references: a copy of another verse's list

Part of the cross-reference table of the Károli Bible (the cross-references of the Károli edition, KH) carries not the list of its own verse but that of another verse (for example, the rows of Acts 2:27 are identical to those of Acts 7:14; Isa 34:11 = Isa 40:11; Ps 116:13 = Ps 140:4).

| Measure | Value |
|---|---|
| source verses in the KH table (with a cross-reference list) | 19817 |
| KH rows in total | 32407 |
| list identical word for word to that of another source verse | 12322 |
| of these, suspect (copied) source verses | 5078 |
| KH rows of the suspect lists | 7971 |

A source verse is **suspect** if its list is identical word for word to that of another source verse, no element of its own list is supported (neither the TSK context of ±3 verses nor the back-reference of the target confirms it), while the list of the verse with the identical list is supported.

**Handling.** The open core does not contain the KH table data, and none of its rows builds on it: candidates based on cross-references appear in the `kizarasok.tsv` here on the basis of the TSK and hand-made assessment, marked with the search mode "Károli cross-reference". The limit: the measurement catches the copy-type error, not an individual faulty list that is not duplicated. Correcting the faulty lists is an open task of the project; after the correction the measures will change.

## 2. Semantic domains: incomplete coverage

The separate layer (`cc_by_sa_reteg/`) contains the UBS SDBH/SDGNT semantic domains for the lexical bases (Strong's numbers) of the package. The domain data cover about 90% of the Old Testament vocabulary: a missing entry is **not a negative finding**, and the domain is a support, not a substitute for the definition of the motif.

## 3. Machine alignment of the Károli word

The value `szó-szintű-gépi` of the `azonositas_modja` column of `elofordulasok.tsv` is model output: the alignment of the Károli word with the Strong's number was done by machine, and only a high-confidence pair may justify a row. The mode states how the word was identified, not that a human verified the alignment.
