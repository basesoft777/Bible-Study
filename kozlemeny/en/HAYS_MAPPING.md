# The Method in the Light of Hays's Seven Criteria

*Magyar változat: [HAYS_LEKEPEZES.md](../HAYS_LEKEPEZES.md)*

<!-- Source layer, hand-written text (F169.1); English version of kozlemeny/HAYS_LEKEPEZES.md (F163.2). The mapping is interpretation (claude-opus-5-5); the naming and order of Hays's criteria were confirmed by a web source check (claude-sonnet-5-5 subagent, 2026-11-04), see Sources. The Hungarian file is authoritative in case of divergence. -->

*Status: 4 November 2026.*

Richard B. Hays proposed seven tests for weighing whether a New Testament text genuinely echoes an Old Testament passage. They have become a common language of research on biblical intertextuality; according to the methodological literature they are not rules to be scored but considerations to be weighed together, yielding degrees of confidence. This page shows which elements of the method correspond to each test, and where no corresponding element exists.

**One difference up front.** Hays's tests weigh an author's intentional allusion. This work primarily decides whether a passage is an occurrence of the same motif; it says something about authorial intent only where it records relations between passages. The mapping is therefore a correspondence, not an identity.

| Hays's criterion | What it asks | Corresponding element of the method | Coverage |
|---|---|---|---|
| 1. Availability | Could the author and the first readers have had access to the source text? | Septuagint correspondence: for a New Testament passage, the Greek rendering of the Hebrew passage is looked up and it is recorded whether the Greek text carries the same word | partial: toward the New Testament, yes; the chronological relation of the Old Testament books to one another is not examined |
| 2. Volume | How much verbal and structural agreement is there, how prominent is the source, how great is the rhetorical stress? | shared lexical base (identical Hebrew or Greek words, by Strong's number), word pair within a verse, verb-form check; every occurrence names the shared word it hangs on | partial: it measures lexical agreement and structure; rhetorical stress is discussed only in the interpretive prose, without measurement |
| 3. Recurrence | Does the author refer to the same passage elsewhere? | a complete Old and New Testament scan of the shared lexical base: every occurrence is processed, not only the conspicuous ones | covered in reformulated form: the method measures distribution over the whole corpus, not by author |
| 4. Thematic coherence | Does the proposed echo fit the line of argument of the text? | a recorded exclusion criterion per motif (the feature without which a passage does not belong); a named superordinate concept toward which the motif would dilute, which by itself is a ground for exclusion; for every occurrence, separately, the meaning of the word and the function of the passage in the motif | covered |
| 5. Historical plausibility | Could the author have intended this meaning, and could the first readers have understood it? | only the Septuagint correspondence | **not covered**: there is no ancient Near Eastern comparative layer and no dating layer (see *The Boundary of the Ancient Near Eastern Background*) |
| 6. History of interpretation | Have others also heard this echo? | agreement of named interpreters with a source (the Tanítói egyezés / named-teacher match section), where this step was run; the PaRDeS level as a label of the tradition's modes of reading (see *The PaRDeS Level as a Reception Label*); the Károli translation as Hungarian reception-historical data | partial: not a systematic history of effects (*Wirkungsgeschichte*) but a selection of interpreters |
| 7. Satisfaction | Does the reading make sense, does it illuminate the text? | the Interpretation section | as interpretation only: a judgement, not a measurement; written by artificial intelligence and approved by the author (see *Statement on the Use of Artificial Intelligence and on Authorship*) |

## What the method adds beyond Hays's questions

In 1962 Samuel Sandmel called "parallelomania" the error in which a scholar exaggerates the similarity of texts and then derives dependence from it. Hays's questions supply a discipline of weighing against this; this method adds a decision trail:

- **Rejection with rationale.** Every passage examined receives a decision (accepted, rejected or open), and the reason for rejection is readable. Today, of 792 passages examined, 411 are rejected (52%).
<!-- provenance: scope=main be54d328, occurrence candidates by decision: rejected 411, accepted 255, open 126 | source=adat/jeloltek.tsv | ts=2026-11-04 -->
- **Row-by-row source attribution.** Every row derived from a query names the source, the scope and the date of the query; where no query was run, the row is marked as a manual decision.
- **An empty result is also a result.** If a query finds nothing, this is stated, and the method does not fill the gap with weaker, associative material.
- **Boundary check.** An automated analysis checks whether one motif is a subset of another, and a second reader checks whether the boundary is consistent.

What does not follow from this: the exclusion criterion and the decisions are produced by the method's own working process; no external scholarly body checks them today.

## Sources

- Richard B. Hays: *Echoes of Scripture in the Letters of Paul.* New Haven – London: Yale University Press, 1989; the seven tests in the section "Seven Tests", approx. pp. 29–32 (the page numbers were taken from a secondary source and not verified in the original edition).
- Samuel Sandmel: "Parallelomania." *Journal of Biblical Literature* 81/1 (1962) 1–13. https://doi.org/10.2307/3264821
- David A. Shaw: "Converted Imaginations? The Reception of Richard Hays's Intertextual Method." *Currents in Biblical Research* 11/2 (2013) 234–245. https://doi.org/10.1177/1476993X12440561 (on the reception and debate of the criteria)

<!-- provenance (Hays, Sandmel, Shaw): scope=web | source=Crossref API (Sandmel 10.2307/3264821; Shaw 10.1177/1476993x12440561, read directly); Hays's seven criteria and their order: secondary sources (intertextual.bible, "Intertextual criteria are guides, not rules"; naplok/kutatas_2026-10-27/jegyzetek/Motivumlexikon_mint_kutatoi_termek/exegetikai_fogadtatas.md), the page image of the original was not available; Hays's words on non-mechanical application only from a secondary summary | ts=2026-11-04 -->
<!-- provenance (elements of the method): scope=main be54d328 | source=CLAUDE.md (seven steps, four questions, three rules), adat/SEMA.md 2.1 (negativ_kriterium, folerendelt_fogalom), 2.2, 2.4, lexikon/ISTENTISZT-001_TUDOMANYOS.md (Meaning/Function columns), MUNKAMENET.md C-h | ts=2026-11-04 -->
