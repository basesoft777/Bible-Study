# Known issues and limitations

<!-- GENERATED: export of the Logosz Lexikon open data core, generated from the project data; do not edit by hand. -->

*Logosz Lexikon — open data core · data state: 2026-11-12*

We state here the source errors that our own measurements revealed, and how the package handles them. A gap is not filled: where a source is faulty or incomplete, an empty result is not a negative finding. The limitations of the method are listed in section 12 of `METHODS.md`.

## 1. Károli cross-references: correcting the faulty lists

Part of the cross-reference table of the Károli Bible (the cross-references of the Károli edition, KH) carried not the list of its own verse but that of another verse (for example, the rows of Acts 2:27 were identical to those of Acts 7:14; Isa 34:11 = Isa 40:11; Ps 116:13 = Ps 140:4).

**The corrected table.** We corrected the error with an independent second witness: we compared the table with the cross-references of the Károli translation in the edition of the Hungarian Electronic Library (MEK 00161). In the corrected table every row receives a level:

| Level | Rows |
|---|---|
| confirmed: the two witnesses agree, or the second witness gives the row and nothing contradicts it | 23,979 |
| drops out | 11,040 |
| candidate: not yet decided | 181 |

The remaining error of the rows taken over from the second witness is the MEK's own misprints; we measured it with a sample check.

**Use.** The candidate search and the reader database use only the confirmed rows of the corrected table. The lexicon pages, too, use only the confirmed rows.

**Open.** The 181 rows at the candidate level are not yet decided; until they are, no consumer uses them.

**In the package.** The open core does not contain the KH table data, and none of its rows builds on it: candidates based on cross-references appear in the `kizarasok.tsv` here on the basis of the TSK and hand-made assessment, marked with the search mode "Károli cross-reference".

**The measurement before the correction.** The error was revealed by the integrity measurement of the uncorrected table:

| Measure | Value |
|---|---|
| source verses in the KH table (with a cross-reference list) | 19817 |
| KH rows in total | 32407 |
| list identical word for word to that of another source verse | 12322 |
| of these, suspect (copied) source verses | 5078 |
| KH rows of the suspect lists | 7971 |

A source verse is **suspect** if its list is identical word for word to that of another source verse, no element of its own list is supported (neither the TSK context of ±3 verses nor the back-reference of the target confirms it), while the list of the verse with the identical list is supported. This measurement catches the copy-type error, not an individual faulty list that is not duplicated; the second witness also flags places where the lists of the two editions differ.

## 2. Semantic domains: incomplete coverage

The separate layer (`cc_by_sa_reteg/`) contains the UBS SDBH/SDGNT semantic domains for the lexical bases (Strong's numbers) of the package. The domain data cover about 90% of the Old Testament vocabulary: a missing entry is **not a negative finding**, and the domain is a support, not a substitute for the definition of the motif.

## 3. Machine alignment of the Károli word

The value `szó-szintű-gépi` of the `azonositas_modja` column of `elofordulasok.tsv` is model output: the alignment of the Károli word with the Strong's number was done by machine, and only a high-confidence pair may justify a row. The mode states how the word was identified, not that a human verified the alignment.

Corrections go into the next release; a release can be cited by the identifier in `RELEASE.txt`.
