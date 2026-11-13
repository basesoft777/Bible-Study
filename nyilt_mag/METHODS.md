# Methods — the motif data core

*Logosz Lexikon — open data core · data state: 2026-11-12 · DOI: 10.5281/zenodo.24141612*

## 1. What this dataset is

This package is an open dataset of biblical motifs. By a motif we mean a recurring biblical theme whose presence in
a verse can be checked on the Hebrew or Greek text: on a word, on a fixed phrase or on a co-occurrence of words. The
package contains 9 motifs with 250 occurrences. The other side is recorded in the same detail: 554
exclusion rows record, with a rationale, the passages that we examined but did not assign to the motif.

The open data core is the data layer of the lexicon; the lexicon itself (its interpretive text, the Hungarian translation of the dictionaries, and the printed volume) is a separate work, all rights reserved. The data core holds decisions and short rationales, not interpretive prose.

## 2. Defining a motif

A motif receives an identifier once four questions are answered. What carries its identity? What is the smallest
feature without which a passage does not belong to it (the exclusion criterion)? If a passage belongs to two motifs,
does it play a different role in each? And is the motif a subset of another one? Every motif also names the broader
concept towards which its boundary would dissolve (the superordinate concept). A passage that is connected to the
motif only through this broader concept is left out.

`motivumok.tsv` gives this in three columns: the carrier of identity (`azonossag_tipusa`; in this release
lexical: 6; formulaic: 2; structural: 1), the exclusion criterion (`negativ_kriterium`) and the superordinate concept (`folerendelt_fogalom`).
The reader-facing definition (`meghatarozas`) says in one or two sentences what the motif is; in this release it is
given for 2 of the motifs and empty for the rest. The boundary of a motif, however, is drawn by the exclusions,
not by the definition.

## 3. Gathering candidates

The possible occurrences, that is, the candidates, are brought up by searches in a fixed order:

1. the Strong's numbers of the words shared by the core passages of the motif, without articles, conjunctions and
   other grammatical words;
2. the hypothesis of the semantic field: this is the only step not done by machine, so the words of the field are
   recorded;
3. a scan of the whole Old and New Testament text by Strong's number, on the tagged text of STEPBible (TAHOT,
   TAGNT);
4. the co-occurrence of two words in one verse;
5. a check of the verb form;
6. the Septuagint correspondence.

Steps 1 and 3–6 are done by a program that always gives the same result for the same input. Further candidates came
from the cross-references (the Treasury of Scripture Knowledge and the cross-references of the Károli edition), from
dictionary entries and from the editorial completeness survey. Where a decided candidate came from is given by the
`keresesi_mod` column of `kizarasok.tsv` and `beepitesi_dontesek.tsv` (in this release 11 search
modes).

We found a copy-type error in the cross-reference table of the Károli edition. We corrected it with an independent
second witness, the cross-references of the MEK 00161 edition of the Károli translation, and the candidate search
already uses the corrected table. The open data core itself contains no cross-reference data; the error and the
correction are described in section 1 of `KNOWN_ISSUES.md`.

## 4. A decision on every candidate

A search hit never becomes an occurrence directly: every candidate receives a decision with a rationale. An accepted
candidate goes into `elofordulasok.tsv`, the rationale of the decision into `beepitesi_dontesek.tsv` (252 rows).
A rejected candidate goes into `kizarasok.tsv`, with an exclusion reason (62 reasons) and a rationale.

Of the exclusion rows, 454 concern a single passage each. 100 rows are summary rows: each stands for
a group whose verses were all rejected for the same reason. The 4,034 verses of the groups are listed in
`kizaras_csoportok.tsv`, and the rationale of the summary row applies to every verse of the group.

If a search is empty, the result stays empty: a gap is not filled with weak or associative material. Candidates not
yet decided (20) are not in the package. Where a row refers to an editorial decision, the public identifier
of the decision (`NYD-nnn`) is resolved in `dontesnaplo.tsv` (15 decisions).

## 5. The occurrence row

Every occurrence is a passage, and it names what its assignment rests on (`horgony_tipus`, `horgony`): lexical base: 195; shared lexical base: 33; collocation (word pair in one verse): 13; thematic link: 6; formula link: 1; reference link: 1; quotation link: 1.
The `strong` column is the Strong's number of the anchor word, `jelentes_en` an excerpt of the dictionary meaning,
`strong_glossza_en` the short English gloss of STEPBible.

**The Károli word.** Every occurrence also gives also give the corresponding word of the Károli translation. The Károli word is not
evidence: it shows what the Hungarian reader sees of the passage. The alignment (`azonositas_modja`) was made by the
editor reading the Károli text in 223 cases, by machine word alignment in 25 cases (only a
high-confidence pair may justify a row) and by inference in 2 cases. The confidence (`megbizhatosag`)
is high in 232 cases and medium in 18. The alignment of the other words of the verse is not
part of this dataset; it is in the related Károli – Strong datasets.

**Provenance.** Every row names where it comes from. If it comes from a query, it gives the type of the query, the
source, its licence and the date; if not, it states that it is a decision made by hand, without a query. Of the
occurrences, 246 are decisions made by hand and 4 the direct result of a query. "Made by hand" does not
mean that the row was verified; it means that no single query produced it. For 201 rows the Strong's
assignment was traced back item by item on the Hebrew text of TAHOT (`igazolas`).

## 6. Processing stage

A motif is a closed release if its lexicon page was released under the current standard for a finished page (this
standard has applied since 2026-11-11) and passed the reader check without error. The number of such motifs in
this release is 1: HAMART-001.

The other motifs, 8 in number, are earlier processing, being rewritten. They were built at an earlier stage of
the work with an older procedure, and their lexicon pages are being rewritten to the current standard. Their data
stay in the package, follow the current schema and pass the package's own automated check just as the closed motifs
do; the reviews of the release procedure, however, do not yet apply to them, so their data may change during the
rewrite.

The stage is given in the `feldolgozasi_allapot` column of `motivumok.tsv`; anyone who wishes to work only with
closed material can filter on this column.

## 7. The echo layer

Four tables give the echo of the motifs in ancient translations and interpreters, with the licence of each source:

- `visszhang_megfelelok.tsv` (144 rows): the counterparts of the anchor words in the Targum (42),
  the Vulgate (55) and the Septuagint (47);
- `visszhang_tanuk.tsv` (8 rows): patristic, rabbinic and Glossa Ordinaria witnesses: who, in which work,
  sees what in the passage, in one sentence in our own words, without quotation;
- `vitatott_forrasok.tsv` (3 rows): the peer-reviewed literature on the disputed points, bibliographic data only;
  an empty author means that no peer-reviewed source on the point was found in the databases searched;
- `sblgnt_apparatus.tsv` (60 rows): the critical apparatus for the New Testament passages.

Only verified rows enter these tables. Of the Septuagint counterparts, those where a single lemma comes into question
in the verse were checked by machine; every other row was reviewed by a second hand. Three things are not in the
package: the witnesses of the Chain Lineage Browser (the browser states no licence), the cognate-language rows of the
BDB (they await a separate decision) and the text of the sources.

## 8. The English layer

Column names and values are Hungarian; English parallel columns stand next to them.

- **Passages:** next to every passage column, `…_osis`, with a standard OSIS key. The book code is standard; chapter
  and verse follow the versification of the Károli translation, and where this differs from the STEPBible numbering,
  the key denotes the Károli verse.
- **Closed values:** next to every closed-vocabulary column, `…_en`, with the edited English label of the codebook.
- **Free text** (rationale, function, the definition of the motif, the decision log): an `…_en` parallel field, a
  **machine translation** (mainly `claude-sonnet-5-5`; in a few cells `claude-opus-5-5`). The `forditas_modja` column of the row names the model and states any gap
  (the translation is missing wholly or in part in 220 rows).

## 9. Licence filtering

The package takes values only from sources in the public domain or under CC0 or CC BY 4.0, according to the licence
inventory of the project. 23 sources were excluded: those under non-commercial and GPL licences, those with
an unclear licence, and the closed, derived layers of the project. The list of excluded sources and the reason for
each exclusion are in `ATTRIBUCIO.md` and `forrasok_es_licencek.tsv`. The semantic domains under CC BY-SA 4.0 (UBS
SDBH/SDGNT) are in a separate directory (`cc_by_sa_reteg/`), because the ShareAlike condition extends to work derived
from them; the rest of the package is independent of it. The inventory is not a legal opinion.

## 10. Use of artificial intelligence

The searches are deterministic programs. Whether a candidate belongs to the motif is decided in a working session
assisted by artificial intelligence under the direction of the editor, and every decision is recorded with a
rationale. Machines also did the machine alignment of the Károli word (section 5), the English translation of the
free-text fields (section 8) and the check of the unambiguous Septuagint counterparts (section 7). The data tables are
produced from the data by a program; a language model does not write them, and the same data always yield the same
package. The descriptive texts (these methods, the readme and the announcement) were drafted by a language model, the
numbers come from the export, and the text was approved by the editor. The model is not an author; the author is
responsible for the content.

## 11. Verification

The package's own automated check runs before every release. It checks that no internal working mark remains in the
package, that the codebook covers every column and closed value in both languages, that the licence filtering holds,
that every reference to a decision or a motif can be resolved, that the member counts of the summary rows agree, that
the OSIS keys are correct, that the translation is current, and that regeneration yields a byte-identical package.
`ELLENORZO_OSSZEG.sha256` contains the SHA-256 checksum of every released file; the content fingerprint (hash) in
`RELEASE.txt` is the checksum of this list.

On a released lexicon page the reader check requires zero errors. The changes of every step of the work are checked
again, with its own queries, by a language model that starts without prior context; the boundary of a motif is
reviewed by a second model. This is not independent scholarly peer review: apart from the author, every checker is a
program or a language model.

## 12. Limitations

- The number of closed releases is only 1. The other motifs, 8 in number, are earlier processing,
  being rewritten, and their data may change during the rewrite (section 6).
- Completeness is not proven. The searches measure how much the list catches on lexical features; they do not measure
  thematic connection.
- There was no independent scholarly peer review, and no inter-annotator agreement was measured.
- The motifs were chosen by the research programme; they are not a representative sample of the Bible.
- The known errors of the source data and their handling are described in `KNOWN_ISSUES.md`; the correction of the
  cross-references of the Károli edition is in its section 1.
