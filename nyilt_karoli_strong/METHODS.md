# Methods — word alignment of the 1908 Károli text with the source texts

*Károli 1908 – Strong word alignment · Logosz Lexikon · release 1 · data state: 2026-11-01 · DOI: 10.5281/zenodo.24141884*

## 1. What this dataset is

The 1908 text of Károli Gáspár's translation, linked word by word to the words of the Hebrew and Greek source text. The
link is carried by Strong's numbers: the Strong's numbers of a Hungarian word are those of the Hebrew or Greek word it
translates. The package holds 66 books, 31,158 verses, 599,367 Hungarian and 611,396 source words, and 598,715
word pairs.

The alignment is a proposal of language models, with measured accuracy. It is not manually verified data: every pair is
in the "proposal" state, and the package states how far it can be trusted — per stratum, per link type, with
confidence intervals (5).

## 2. The two texts

The Hungarian side is the public-domain 1908 Károli text. The source side is two STEPBible datasets: TAHOT (Hebrew and
Aramaic Old Testament) and TAGNT (Greek New Testament), both with a Strong's number and an English gloss for each
word. TAHOT splits the Hebrew word into its prefixes and suffixes: the conjunction (*ve-*), the article, the preposition
and the pronominal suffix stand as separate words with their own numbers (H9001–H9049). One Hungarian word is therefore
often linked to several source "words": *Kezdetben* ("in the beginning") to both the preposition and the noun.

Tokenisation is deterministic on both sides; punctuation is not a word. A word is identified by its verse and its
position within the verse, separately on each side.

## 3. Verse mapping

Károli's verse division differs in places from that of the Hebrew and Greek text (mainly at chapter
boundaries). Before alignment, each Károli verse was matched to its source verse: by deterministic alignment of verse
lengths, with each merge of two verses approved by hand. Source words are therefore keyed to the Károli verse;
`eredeti_token` is the position within the mapped source verse.

## 4. Alignment procedure

**The task.** For each verse the model received the Hungarian words, numbered, and the source words, numbered, with
form, Strong's number and English gloss. It had to state which Hungarian word translates which source word(s); which
Hungarian words have no source (additions); and which source words have no Hungarian counterpart (untranslated). The
model **writes no Strong's number**, only positions: the number comes from the position, from the source. The model
cannot invent a number.

**The rules.** Disputed cases were decided by a written rule set, derived from the conventions of an earlier
alignment sample. The main ones: the Hungarian article is an addition, the Hebrew and Greek article is untranslated
unless it stands as a pronoun; both words of a split Hungarian conjunction or relative pronoun (*a mely, a ki*) go to
the common source word; the Hebrew object marker is untranslated, and the object pronoun links to its suffix; a
possessive suffix belongs to the Hungarian word that carries the matching personal ending; a separated verbal prefix
belongs to the verb's source word; an explicit subject pronoun and the auxiliary *vala* are additions where the source
has no separate word; the Hebrew *ve-* links only where a conjunction stands in its place in Hungarian; a Greek word not
in the Textus Receptus is untranslated.

**The machine gate.** Every answer was checked by a program: each Hungarian word appears exactly once (in a pair or as an
addition), each source word at least once (in a pair or as untranslated), only existing positions occur, and the verse
is complete. An answer failing the gate was redone by the model. Where the verse mapping did not hold word by word, or the answer
finally failed the gate, the verse awaits manual review: all its words are `fuggoben`, without a pair
(45 verses).

**The models.** Genesis and Exodus were aligned by two independent models with the same task description: Claude
Sonnet and Gemini Flash. A program built the table from the two answers: where both gave the same pair, the pair has
`magas` (high) confidence (52,844 pairs); where they differed, the first model's pair was kept with `alacsony` (low)
confidence. For reasons of cost, the other books were aligned by one model, Claude
Sonnet; all their pairs are `alacsony` (545,871 pairs). The task description did not change during the run; the
tables can be rebuilt byte-identically from the models' saved answers, without new model calls.

**Result.** 488,659 Hungarian words have a pair, 109,914 are additions; 547,585 source words are
aligned, 63,017 untranslated. Of the 598,715 pairs, 466,785 are Hebrew and 131,930 Greek; 157,163
link a Hebrew prefix or suffix morpheme.

## 5. Measuring accuracy

Accuracy was measured in two complementary ways.

**Blind review on a stratified sample.** The 598,715 pairs were divided into eight strata (Genesis–Deuteronomy with two
models and with one; the historical, poetic and prophetic books; the Gospels and Acts; the Epistles; Revelation), and
200 pairs were drawn at random per stratum. A third language model (Claude Opus) marked, for each target in the
sample, the matching source words from the verse text and the source words itself, with the same rules, without seeing
the machine pair. A pair is correct if its source word is among the reviewer's marks.

| stratum | n | correct | rate | 95% |
|---|---|---|---|---|
| Moses, two models agreeing | 200 | 198 | 99.00% | 96.43–99.73% |
| Moses, one model | 200 | 184 | 92.00% | 87.40–95.02% |
| historical books | 200 | 190 | 95.00% | 91.04–97.26% |
| poetic books | 200 | 190 | 95.00% | 91.04–97.26% |
| prophets | 200 | 186 | 93.00% | 88.59–95.78% |
| Gospels, Acts | 200 | 196 | 98.00% | 94.97–99.22% |
| Epistles | 200 | 191 | 95.50% | 91.67–97.61% |
| Revelation | 200 | 193 | 96.50% | 92.95–98.29% |
| **Old Testament, weighted** | 1,000 | | 94.50% | 92.95–96.05% |
| **New Testament, weighted** | 600 | | 97.07% | 95.55–98.59% |
| **all, weighted** | 1,600 | | **95.06%** | 93.81–96.32% |

The weighted estimate uses the pair share of the strata. By link type: content-word pairs 96.44% (95%:
95.20–97.69%), Hebrew morpheme pairs 90.74% (95%: 87.18–94.29%). The stratum where the
two models agreed reaches 99.00%, but this does not show that the second model causes the difference: the books of the two
Moses strata largely differ.

**Calibration.** The reviewer is not infallible. On an earlier manually compiled sample (374 measurable cases)
the reviewer agreed with it in 96.79% (95%: 94.48–98.16%), the machine alignment in 97.06% (95%:
94.81–98.35%): the reviewer is not more accurate than the alignment. Part of the differences are thus the
reviewer's errors, and the agreement is a lower bound only if shared (machine and reviewer) errors are negligible.

**Independent comparison.** Shared errors are measured by an independent source: a Károli edition marked with Strong's
numbers, which the package does not contain and of which only the aggregate agreement is given here. One full chapter
per stratum was compared (8 chapters, 2,663 main-word pairs). The source marks one main Strong's number
per word, not the secondary word in a suffix, preposition or article, nor the morpheme; this measurement applies to
main-word pairs only.

- Accepting the source's judgement, 98.72% of main-word pairs agree (95%: 98.22–99.08%; Old Testament 98.93%,
  New Testament 98.50%).
- The 34 differences were judged three ways (machine pair, source, blind reviewer); after this 5 remained
  errors of the alignment, giving a main-word accuracy of 99.81% (95%: 99.56–99.92%).
- The chapters are clusters, not random sample units; the true uncertainty is larger than the interval.

**Error types.** Of the 1,600 sample pairs, 72 differed from the reviewer: neighbouring word
37 (content 20, morpheme 17), wrong word in the verse
17, superfluous pair 16, same lexeme at another occurrence
2. Every figure of the measurement is in `meres.tsv`.

## 6. Why open data

The alignment is not error-free, and we do not publish it as such. By editorial decision it is released as open data
because its accuracy is **measured and documented**: per stratum and link type, with confidence intervals, with the
error types and the list of confirmed errors (`KNOWN_ISSUES.md`). The "proposal" state and the confidence label remain
on every pair. Publication does not rest on meeting a threshold set in advance: there was no fixed criterion before the
measurement, and a threshold set afterwards would be a post-hoc criterion.

## 7. The next release

This is release 1: the measured state, unchanged. Release 2 will correct the confirmed errors and the rule-violating
neighbouring-word cases (by rule-based post-processing, not pair-by-pair patches), then measure again with the same
protocol: stratified sample, blind reviewer, independent external source. The quality target for release 2 was fixed
in advance, in knowledge of the release 1 results: the lower bound of main-word agreement in the independent comparison
at least 98% (now 98.22%); the lower bound of the weighted agreement with the blind reviewer at least 93% (now
93.81%), with no stratum point estimate below 90% (now the lowest is 92.00%). The target does
not apply to release 1.

## 8. Related dataset

The same pairs also appear on the modernised Károli text (https://doi.org/10.5281/zenodo.24141950). The modernisation left every
word in its place, so the two packages can be joined word by word on the verse and word position key.
