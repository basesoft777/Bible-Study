# Methods — the motif data core

*Logosz Lexikon — open data core · data state: 2026-11-10 · DOI: 10.5281/zenodo.24141612*

## 1. What this dataset is

An open dataset of biblical motifs. A motif here is a recurring biblical theme whose presence in a verse can be
checked on the Hebrew or Greek text: on a word, a fixed phrase or a co-occurrence of words. The package contains
9 motifs with 250 occurrences. The other side is recorded in the same detail: 540 exclusion rows give, with
a rationale, the passages that were examined but not assigned to the motif.

The open data core is the data layer of the lexicon; the lexicon itself (its interpretive text, the Hungarian translation of the dictionaries, and the printed volume) is a separate work, all rights reserved. The data core holds decisions and short rationales, not interpretive prose.

## 2. Defining a motif

A motif receives an identifier once four questions are answered: what carries its identity; what is the smallest
feature without which a passage does not belong to it (the exclusion criterion); if a passage belongs to two motifs,
does it play a different role in each; and is it a subset of another motif. Every motif also names the broader
concept towards which its boundary would dissolve (the superordinate concept). A passage connected only through
that concept is left out.

`motivumok.tsv` gives this in three columns: the carrier of identity (`azonossag_tipusa`; in this release
lexical: 6; formulaic: 2; structural: 1), the exclusion criterion (`negativ_kriterium`) and the superordinate concept (`folerendelt_fogalom`).
The reader-facing definition (`meghatarozas`) says in one or two sentences what the motif is; in this release it is
given for 1 of the motifs and empty for the rest. The boundary of a motif, however, is drawn by the exclusions,
not by the definition.

## 3. Gathering candidates

Possible occurrences (candidates) are brought up by searches in a fixed order:

1. the Strong's numbers of the words shared by the core passages of the motif, without articles, conjunctions and
   other grammatical words;
2. a hypothesis of the semantic field: the only step not done by machine, so the words of the field are recorded;
3. a scan of the whole Old and New Testament by Strong's number, on the tagged STEPBible text (TAHOT, TAGNT);
4. two words occurring together in one verse;
5. a check of the verb form;
6. the Septuagint correspondence.

Steps 1 and 3–6 are run by programs and give the same result for the same input. Candidates also came from
cross-references (Treasury of Scripture Knowledge; the cross-references of the Károli edition, see
`KNOWN_ISSUES.md`), dictionary entries and editorial completeness surveys. Where a decided candidate came from is
given in the `keresesi_mod` column of `kizarasok.tsv` and `beepitesi_dontesek.tsv` (11 search modes
in this release).

## 4. A decision on every candidate

A search hit never becomes an occurrence directly. Every candidate receives a decision with a rationale. An included
candidate goes to `elofordulasok.tsv`, the rationale of the decision to `beepitesi_dontesek.tsv` (252 rows); a
rejected one goes to `kizarasok.tsv`, with a reason (61 reasons) and a rationale.

Of the 540 exclusion rows, 443 concern a single passage. 97 rows are summary rows: each stands
for a group of verses rejected for the same reason; `kizaras_csoportok.tsv` lists the 3,984 verses of the
groups, and the rationale of a summary row applies to every verse of its group.

If a search is empty, the result stays empty: a gap is not filled with weak or associative material. Candidates not
yet decided (20) are not in the package. Where a row refers to an editorial decision, its public identifier
(`NYD-nnn`) can be resolved in `dontesnaplo.tsv` (15 decisions).

## 5. The occurrence row

Every occurrence is a passage and names what its assignment rests on (`horgony_tipus`, `horgony`): lexical base: 197; shared lexical base: 33; collocation (word pair in one verse): 13; thematic link: 4; formula link: 1; reference link: 1; quotation link: 1.
The `strong` column is the Strong's number of the anchor word, `jelentes_en` an excerpt of the dictionary meaning,
and `strong_glossza_en` the short English STEPBible gloss.

**The Károli word.** Every occurrence also gives the corresponding word of the Károli translation. The Károli word
is not evidence: it shows what the Hungarian reader sees of the passage. The pairing (`azonositas_modja`) was made
in 223 cases by the editor reading the Károli text, in 25 cases by machine word alignment
(only a high-confidence pair may justify a row), and in 2 cases by inference. The confidence
(`megbizhatosag`) is high in 234 cases and medium in 16. The alignment of the other words of
the verse is not part of this dataset; it is in the related Károli – Strong datasets.

**Provenance.** Every row names its origin: if it comes from a query, the type of query, the source, its licence and
the date; if not, that it is an editorial decision without a query. Of the 250 occurrences, 246 are editorial
decisions and 4 the direct result of a query. "Editorial decision" does not mean that the row is verified, only
that no single query produced it. For 181 rows the Strong's assignment was traced item by item in the
Hebrew text of TAHOT (`igazolas`).

## 6. Processing stage

1 motifs are closed releases (HAMART-001): their lexicon pages are released and passed the reader check
without error. The other 8 were made at an earlier stage of the project with an older procedure. Their data are
in the current schema and pass the same check, but the reviews of the release procedure do not yet cover them, and
they may change in later versions. The stage is in the `feldolgozasi_allapot` column of `motivumok.tsv`; to work only
with the closed material, filter on it.

## 7. The echo layer

Four tables give the echo of the motifs in the ancient translations and interpreters, with the licence for each
source:

- `visszhang_megfelelok.tsv` (101 rows): the counterparts of the anchor words in the Targum (32), the
  Vulgate (38) and the Septuagint (31);
- `visszhang_tanuk.tsv` (6 rows): patristic, rabbinic and Glossa Ordinaria witnesses: who, in which work,
  what they see in the passage, in one sentence in our own words, without quotation;
- `vitatott_forrasok.tsv` (3 rows): the peer-reviewed literature on the disputed points, bibliographic data only;
  an empty author means that no peer-reviewed source on the point was found in the databases searched;
- `sblgnt_apparatus.tsv` (61 rows): the critical apparatus for the New Testament passages.

Only verified rows are included. Of the Septuagint counterparts, those where a single lemma comes into question in
the verse were checked by machine; every other row was reviewed by a second hand. Not in the package: the witnesses
of the Chain Lineage Browser (the browser states no licence), the cognate-language rows of the BDB (they await a
separate decision), and the text of the sources.

## 8. The English layer

Column names and values are Hungarian; English parallel columns stand next to them.

- **Passages:** next to every passage column, `…_osis`, with a standard OSIS key. The book code is standard; chapter
  and verse follow the versification of the Károli translation, and where this differs from the STEPBible numbering,
  the key denotes the Károli verse.
- **Closed values:** next to every closed-vocabulary column, `…_en`, with the edited English label of the codebook.
- **Free text** (rationale, function, the definition of the motif, the decision log): an `…_en` parallel field, a
  **machine translation** (mainly `claude-sonnet-5-5`; in a few cells `claude-opus-5-5`). The `forditas_modja` column of the row names the model and states any gap
  (the translation is missing wholly or in part in 38 rows).

## 9. Licence filtering

The package takes values only from public-domain, CC0 or CC BY 4.0 sources, following the project's licence
inventory. 23 sources were excluded: those under a non-commercial or GPL licence, those with an unclear
licence, and the project's closed derived layers. The list of excluded sources and the reason for each are in
`ATTRIBUCIO.md` and `forrasok_es_licencek.tsv`. The semantic domains (UBS SDBH/SDGNT), under CC BY-SA 4.0, are in a
separate directory (`cc_by_sa_reteg/`), because the ShareAlike condition extends to work derived from them; the rest
of the package is independent of it. The inventory is not a legal opinion.

## 10. Use of artificial intelligence

The searches are deterministic programs. Whether a candidate belongs to the motif is decided in a working session
assisted by artificial intelligence, under the direction of the editor, and every decision is recorded with a
rationale. Machines also made the machine alignment of the Károli word (section 5), the English translation of the
free-text fields (section 8) and the check of the unambiguous Septuagint counterparts (section 7). The data tables
are produced from the data by a program, not written by a language model; the same data always yield the same
package. The descriptive texts (these methods, the read-me and the announcement) were drafted by a language model,
the numbers come from the export, and the text was approved by the editor. The model is not an author; the author is
responsible for the content.

## 11. Verification

The package's own automatic check runs before every release. It measures internal working marks, codebook coverage
(every column and closed value, in both languages), licence filtering, the resolution of decision and motif
references, the member counts of summary rows, the OSIS keys, the freshness of the translation, and byte-identical
regeneration. `ELLENORZO_OSSZEG.sha256` contains the SHA-256 sum of every released file; the content hash in
`RELEASE.txt` is the sum of that list.

On a released lexicon page the reader check requires zero errors. The changes of every step of the work are
re-checked by a fresh-context model with its own queries; the boundary of the motif is reviewed by a second model.
This is not independent peer review: apart from the author, every checker is a program or a language model.

## 12. Limitations

- Only 1 motifs are closed releases; 8 come from an earlier stage (section 6).
- Completeness is not proven. The searches measure how much the list catches on lexical features; thematic links
  are not measured.
- There was no independent peer review and no inter-annotator agreement measurement.
- The motifs were chosen by the research programme; they are not a representative sample of the Bible.
- The known errors of the source data and their handling are described in `KNOWN_ISSUES.md`.
