<!-- GENERÁLT: eszkozok/karoli_strong_export.py (a próza: eszkozok/karoli_strong_szovegek.py, a számok: adat/karoli_strong/ és f172/) — kézzel nem szerkesztendő; a #175 második data paperének kézirata, nem része a nyilt_karoli_strong/ csomagnak. -->
# Word-by-word alignment of the 1908 Károli Bible with the Hebrew and Greek source text: an open dataset with measured accuracy

*Manuscript draft (data paper) · Károli 1908 – Strong word alignment · Logosz Lexikon · DOI: 10.5281/zenodo.24141884*

## Abstract

The dataset links the 599,367 words of the 1908 text of the Károli Bible, the classic Hungarian translation, to the
611,396 words of the Hebrew and Greek source text through 598,715 word pairs, each carrying the Strong's number of the
source word. The alignment was produced by language models following a written rule set; the model marked positions
only, and the Strong's number comes from the open STEPBible TAHOT and TAGNT data. Accuracy was measured in two ways: with
a blind model reviewer on a random sample drawn from eight strata (95.06% on the full pair set, 95%:
93.81–96.32%), and against an independent Károli edition marked with Strong's numbers, on main-word pairs
(98.72%, 95%: 98.22–99.08%). The dataset publishes the measured state, with a list of confirmed errors and a
quality target for the next release fixed in advance. Licence: CC BY 4.0.

## 1. Overview

**Context.** For four centuries the Károli translation has been the base text of Hungarian Protestant Bible reading, yet
a free, word-by-word assignment of the Hebrew and Greek words behind it has been missing. In English, the King James
text with Strong's numbers has long been a basic tool for readers and researchers; no comparable open data existed for
Hungarian. This dataset fills that gap, as one of the open data cores of the Logosz Lexikon.

**The question it answers.** Which Hungarian word translates which source word; which Hungarian word is a translator's
addition; which source word is not rendered by a separate Hungarian word. The third question matters as much as the
first: the `szavak` table lists every word once, so the "gaps" of the translation can be read off too.

## 2. Method

**Texts and tokenisation.** The Hungarian side is the public-domain 1908 Károli text; the source side is the STEPBible
TAHOT (Hebrew and Aramaic Old Testament) and TAGNT (Greek New Testament) datasets. TAHOT treats Hebrew prefixes and
suffixes as separate words (H9001–H9049), so one Hungarian word is often linked to several source "words". Before
alignment, Károli's verse division was mapped to that of the source by deterministic alignment of verse lengths; each
merge of two verses was approved by hand.

**Alignment.** For each verse the model received numbered Hungarian and source words (the source with form, Strong's
number and English gloss) and returned pairs of positions, together with additions and untranslated words. Disputed
cases were decided by twelve written rules: on articles, split conjunctions and relative pronouns, the object marker,
possessive suffixes, separated verbal prefixes, explicit subject pronouns and auxiliaries, the Hebrew conjunction *ve-*,
and Greek words absent from the Textus Receptus. A program checked every answer (each Hungarian word exactly once, each
source word at least once, only existing positions); a failed answer was redone by the model. Genesis and Exodus were
aligned by two independent models (Claude Sonnet and Gemini Flash): where they agreed, the pair has `magas` (high)
confidence (52,844 pairs). For reasons of cost, the other books were aligned by one model, Claude Sonnet (`alacsony`,
545,871 pairs). The tables can be rebuilt byte-identically from the saved model answers.

**Accuracy measurement.** (1) *Blind review.* The pair set was divided into eight strata (Genesis–Deuteronomy with two
models and with one; historical, poetic and prophetic books; Gospels and Acts; Epistles; Revelation), with 200
random pairs per stratum. A third model (Claude Opus) marked the source words for each target Hungarian word itself,
with the same rules, without seeing the machine pair. (2) *Calibration.* On an earlier manually compiled sample, the
reviewer agreed with the sample in 96.79% and the machine alignment in 97.06%: the reviewer is not more accurate
than the alignment, so the agreement is a lower bound only if shared errors are negligible. (3) *Independent
comparison.* Shared errors are measured against a Károli edition marked with Strong's numbers, on one full chapter per
stratum (8 chapters, 2,663 main-word pairs); the source marks the main word only, not secondary words or
morphemes. Differences were judged three ways (machine pair, source, blind reviewer). The external source's data are not
part of the dataset, only the aggregate rate.

## 3. Results

| measurement | estimate | 95% |
|---|---|---|
| full pair set, blind reviewer, weighted | 95.06% | 93.81–96.32% |
| of which Old / New Testament | 94.50% / 97.07% | 92.95–96.05% / 95.55–98.59% |
| content word / Hebrew morpheme | 96.44% / 90.74% | 95.20–97.69% / 87.18–94.29% |
| main words, by the independent source | 98.72% | 98.22–99.08% |
| main words, after three-way judgement | 99.81% | 99.56–99.92% |

Agreement per stratum ranges from 92.00% (Moses, one model) to 99.00% (Moses, two
models agreeing); the per-stratum table is in the dataset's `meres.tsv` and its methods description. Of the 1,600
sample pairs, 72 differed from the reviewer; the most frequent type is the neighbouring word
(37), typically a Hebrew prefix, article or preposition attached to the word against the rules. Of the
34 differences in the independent comparison, 5 remained errors of the alignment; these and the other
confirmed errors are listed by name in the dataset.

## 4. Dataset description

**Location and identifier.** Zenodo, DOI: 10.5281/zenodo.24141884; licence: CC BY 4.0; language: Hungarian (data), Hungarian and English
(documentation); data state: 2026-11-01.

**Files.** `parok/` (per book, one row per link: verse, position and form of the Hungarian word, position of the source
word, Strong's number, link type, confidence, state, Textus Receptus flag); `szavak/` (per book, every Hungarian and
source word once, with its state: aligned, addition, untranslated, pending); `versek.tsv` (the 1908 Károli text);
`meres.tsv` (every figure of the measurement); bilingual codebook, methods description, known issues, checksum. The key
is the OSIS verse identifier and the word position. Hebrew and Greek word forms are not in the package: the position
matches the STEPBible TAHOT/TAGNT text.

**Size.** 66 books, 31,158 verses, 598,715 pairs (466,785 Hebrew, 131,930 Greek; of these 157,163
morphemes), 109,914 additions, 63,017 untranslated source words, 794 pending Hungarian words
(45 verses).

## 5. Reuse potential

For Bible reading and study applications the dataset provides Strong-based search on the Hungarian text: every Károli
rendering of a Hebrew or Greek word can be collected with one filter. In translation history, Károli's consistency and
the distribution of additions and untranslated words can be studied. For language technology it is word-alignment data
for a low-resource language pair (Hungarian–Hebrew, Hungarian–Greek) with error measured per stratum; the sample pairs
and error types can also serve to evaluate word aligners. The same pairs also appear on the modernised Károli text
(https://doi.org/10.5281/zenodo.24141950); the two datasets join word by word on the verse and word position key.

## 6. Limitations and the next release

The alignment is a machine proposal. The blind reviewer is itself a model; the independent comparison covers main words
only, on a small cluster sample; the accuracy of the Hebrew morpheme pairs (157,163 pairs; 90.74%) is measured by
the blind reviewer only. Outside Genesis and Exodus every pair is one model's proposal. Károli translated the Textus
Receptus, while the alignment uses TAGNT: 369 aligned Greek words are not in the Textus Receptus, and are
flagged.

Publication rests on an editorial decision: the alignment is released as open data because its accuracy is measured and
documented — per stratum and link type, with confidence intervals and error types. It does not rest on meeting a
threshold set in advance. Release 2 will correct the confirmed errors and the rule-violating neighbouring-word cases,
then measure again with the same protocol. Its quality target was fixed in advance: lower bound of independent main-word
agreement at least 98%, lower bound of weighted agreement with the blind reviewer at least 93%, and no stratum below 90%.

## AI declaration

The alignment was done by language models (Claude Sonnet, Gemini Flash) and the blind review by a third model (Claude
Opus), as described above; the models wrote no Strong's numbers. Tokenisation, the machine gate, table assembly and the
statistics are deterministic programs. The text of the manuscript was drafted by the claude-opus-5-5 model from the
dataset's data; the figures are generated from the data. An AI tool is not an author; the author is responsible for the
data and the text.

## References

Demeter, T. (2026). *Modernised Károli – Strong* [dataset]. Zenodo. https://doi.org/10.5281/zenodo.24141950

STEPBible. (n.d.). *Translators Amalgamated Hebrew OT (TAHOT) and Translators Amalgamated Greek NT (TAGNT)* [dataset].
Tyndale House, Cambridge. https://www.STEPBible.org

<!-- END OF SUBMISSION TEXT — the part below can be removed from the submitted version. -->

---

## Venue suggestion

The manuscript is written as a data paper (overview, method, dataset, reuse). Two kinds of venue fit it. One is a
humanities data journal (for example the Journal of Open Humanities Data), with an explicit data paper type and a place
for the AI declaration, but a length of 1000–1500 words, so sections 2 and 3 would need shortening. The other is a venue
for language resources, where the alignment reaches readers as a low-resource language pair with measured error. A
fee-free alternative is a data mining and digital humanities journal that accepts short articles on open datasets. A
Zenodo deposit is a precondition for all three; the same manuscript may be submitted to only one venue at a time.
