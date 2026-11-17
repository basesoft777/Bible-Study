<!-- GENERÁLT: eszkozok/karoli_strong_export.py (a próza: eszkozok/karoli_strong_szovegek.py, a számok: adat/karoli_strong/ és f172/) — kézzel nem szerkesztendő; a #175 második data paperének kézirata, nem része a nyilt_karoli_strong/ csomagnak. -->
# Word-by-word alignment of the 1908 Károli Bible with the Hebrew and Greek source text: an open dataset with measured pair precision

*Data paper · submission draft for the Journal of Open Humanities Data · dataset DOI: 10.5281/zenodo.24141883*

**Tamás Demeter**, independent researcher · ORCID: https://orcid.org/0009-0005-9254-9731 · corresponding author: [e-mail address]

## Abstract

The dataset aligns the 599,367 words of the 1908 Hungarian Károli Bible with the Hebrew
and Greek source text (STEPBible TAHOT/TAGNT) in 598,715 pairs carrying the source word's Strong's number; a language
model marked word positions only. Pair precision (agreement with a blind model reviewer) is 95.06% (95% CI
93.81–96.32%) on a stratified sample; human validation gives [precision]; main-word agreement with a
closed Strong-tagged edition, a supplementary cross-check, is 98.72%. The CC BY 4.0 tables support Strong-based search.

**Keywords:** Károli Bible; Strong's numbers; word alignment; Hungarian; biblical Hebrew; Koine Greek

**Author roles (CRediT):** Tamás Demeter: Conceptualization, Methodology, Software, Data curation, Validation,
Writing – original draft, Writing – review & editing.

## 1. Overview

### Repository location

https://doi.org/10.5281/zenodo.24141883 (concept DOI; current version 1.0).

### Context

The dataset comes from the author's independent research project, the Logosz Lexikon. Strong's numbers (Strong, 1890) link
a translation's words to the Hebrew and Greek vocabulary. Strong-tagged editions of the Károli text, the Hungarian
Protestant base text for four centuries, exist; this alignment is openly licensed, documented word by word, and its
precision is measured. Per verse it records which Hungarian word renders which source word (one-to-many and
many-to-one), the additions and the untranslated source words.

## 2. Method

### Steps

**Texts.** The Hungarian side is the public-domain 1908 Károli text (HunKar); the source side is STEPBible TAHOT
(Hebrew/Aramaic) and TAGNT (Greek) (Tyndale House, Cambridge; CC BY 4.0;
commit efe428a, downloaded 2026-08-24). TAHOT counts Hebrew prefixes and suffixes as separate words (H9001–H9049). Verse divisions
were mapped by deterministic length alignment, each verse merge approved by hand.

**Alignment.** For each verse a language model received two numbered word lists: the Károli words, and the source
words with form, Strong's number and a short English gloss; the Strong's number was for information only and forbidden
in the answer. The fixed instructions also showed an optional Strong-tagged KJV line in a worked example; no verse
input contained one. The model returned position pairs, additions and untranslated words. In Joshua 8:34 it linked
*Azután* (1) to source words 2–3 (*ʾaḥărê kēn*) and *felolvasta* (3) to word 4 (*qārāʾ*); a program then attached
H0310, H3651 and H7121 by position. Twelve written rules decided disputed cases. Fixed conventions apply to function words: Hungarian articles and auxiliaries without a source word are
additions, Hebrew and Greek articles untranslated (article use differs between the languages); an article used as a
pronoun is linked.

**Runs and reproducibility.** All books were aligned by claude-sonnet-5-5: most through the Anthropic Batch API
(effort=high), Genesis–Deuteronomy, Joshua and Psalms in agent sessions. A program checked every
answer (each Hungarian word exactly once, each source word at least once, only existing positions); a failed answer was
redone. The model thus could not invent a Strong's number or lexicon entry; its possible error is a wrong pairing, and
every pair points to one checkable source word. Model answers were generated once and archived; pair construction,
Strong's number assignment and the gate are deterministic, so the tables rebuild byte-identically from the answers;
re-running the model may differ slightly.

### Sampling strategy

For the blind review, the pair set was divided by book group into seven strata (the five books of Moses;
historical, poetic and prophetic books; Gospels and Acts; Epistles; Revelation), with 200 random pairs per
stratum; in the five books of Moses 400 pairs from two subsamples, combined by pair weight. The human
validation sample has [N] pairs and [M] unpaired words from the same strata, plus all 72 reviewer disagreements
as a weighted oversample. The closed-edition cross-check used eight purposively selected chapters (per stratum the one
with most reviewer disagreements).

### Quality control

**Blind model review.** A second model (Claude Opus) independently marked the source words of each sampled Hungarian
word with the same rules, blind to the machine pair; a pair is correct if its source word is among those marks. Pair precision is therefore agreement with a model, not ground truth.

**Human validation.** An external validator, a theology graduate with knowledge of biblical Hebrew and Greek, judged
every item; a second validator, also a theology graduate, is a family member of the author; neither validator was
involved in producing the dataset. Judging is not blind: validators see the machine pair. Rule-determined function
words were excluded from the unpaired sample. The external validator gives the main figure: precision [precision] (95%
CI [CI]), or [conservative] counting uncertain items as errors. The second validator ([precision 2]) and inter-rater
kappa ([kappa]) are supplementary; there is no adjudicator. Agreement with the blind model reviewer is [agreement
with model reviewer].

**Cross-check with a closed edition.** As a supplementary check, pairs were compared locally with the Bible-Discovery
Strong-tagged Károli (HUN module), a closed-licence edition; only the aggregate can be published,
and readers cannot check it. It is not a gold standard: it marks one main word per Hungarian word;
our segmentation is finer (one-to-many links, morphemes, e.g. *Azután* ↔ *ʾaḥărê* + *kēn*). Main-word pairs are content-word pairs whose Hungarian word has a Strong's number in the edition, excluding
secondary pairs of already matched words: 2,663 of 3,388 (522 without a Strong's number there, 197
secondary, 6 unalignable); secondary pairs and segmentation differences are not errors.

| measurement | estimate | 95% CI |
|---|---|---|
| pair precision, blind model reviewer, weighted | 95.06% | 93.81–96.32% |
| content word / Hebrew morpheme | 96.44% / 90.74% | 95.20–97.69% / 87.18–94.29% |
| human validation (external); uncertain as errors | [precision]; [conservative] | [CI] |
| main-word agreement, closed edition | 98.72% | – |

Precision per stratum ranges from 93.00% (prophets) to 98.00% (Gospels and Acts). Of the 1,600 sample pairs,
72 differed from the reviewer, most often a neighbouring word (37). Of the 34 differences from the closed edition,
five were judged alignment errors (three-way judgement; the dataset lists them); secondary pairs are not
differences.

## 3. Dataset Description

- **Repository name:** Zenodo
- **Object name:** `karoli-1908-strongs-1.0.zip`
- **Format names and versions:** TSV (UTF-8) for the data and
  codebook; Markdown for the bilingual documentation; CFF citation file; SHA-256 checksum list
- **Creation dates:** 2026-10-01 – 2026-11-01
- **Dataset creators:** Tamás Demeter (independent researcher; ORCID: 0009-0005-9254-9731): rules, processing pipeline, measurement,
  curation.
- **Language:** Hungarian (data); Hungarian and English (documentation)
- **License:** CC BY 4.0
- **Publication date:** 2026-11-15

**Contents.** `data/parok/` (one row per link: positions, Strong's number, link type, state, Textus Receptus flag),
`data/szavak/` (every word once, with its state: aligned, addition, untranslated, or pending, i.e. not yet aligned),
`data/versek.tsv`, `data/meres.tsv`; keyed by OSIS verse and word position.

**Size.** 66 books, 31,158 verses, 598,715 pairs (466,785 Hebrew, 131,930 Greek; of these 157,163
morphemes), 109,914 additions, 63,017 untranslated source words, 794 pending Hungarian words
(45 verses).

## 4. Reuse Potential

Bible software can offer Strong-based search of the Hungarian text. Translation historians can study Károli's
consistency and additions. For language technology it is alignment data for a low-resource pair with
error measured per stratum. The Logosz Lexikon, a motif-indexed, cross-referenced biblical
lexicon, is built on this alignment. A companion dataset (Demeter, 2026b) carries the same pairs on the author's
rule-based modernisation of the text (rare verb forms changed only on agreeing independent model proposals; measured
separately): every word kept its position and merged words keep both pairs, so the figures above apply.

### Limitations

The blind reviewer is itself a model, and human validation is not blind. Pair precision does not cover untranslated
source words. The closed-edition chapters were selected purposively and exclude Hebrew morphemes. In Genesis–Exodus,
3,256 pairs (1,486 verses) where the second model proposed a different pair are weaker:
three of 12 sampled were correct, so roughly 1,500–3,000 may be wrong; listed in the known-issues file of
version 1.1, they will be re-aligned in the next release. The 369 aligned Greek words
absent from the Textus Receptus, which Károli translated, are flagged.

## Data Accessibility Statement

Both datasets: Zenodo, CC BY 4.0 (see References). The prompt,
archived model answers, verse mapping and 1,600 judged sample pairs will be added in version 1.1, planned before
publication.

## Acknowledgements

The author thanks [name of the external validator] and [name of the second validator] for the human validation.

## Funding Statement

This work received no external funding.

## Competing Interests

The author has no competing interests to declare.

## References

Demeter, T. (2026a). *Logosz Lexikon – Károli Bible (1908): Word alignment with Hebrew and Greek Strong's numbers*
(Version 1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.24141883

Demeter, T. (2026b). *Logosz Lexikon – Modernized Károli Bible: Word alignment with Hebrew and Greek Strong's numbers*
(Version 1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.24141949

STEPBible. (n.d.). *Translators Amalgamated Hebrew OT (TAHOT) and Translators Amalgamated Greek NT (TAGNT)* [Data set].
Tyndale House, Cambridge. https://www.STEPBible.org

Strong, J. (1890). *The exhaustive concordance of the Bible*. Hunt & Eaton.

## AI Declaration

(1) Alignment: Claude Sonnet (Anthropic) returned position pairs only (see Method). For Genesis and Exodus, another
language model was also run as a cross-check; no published pair derives from it alone. (2) Quality control: Claude Opus
served as blind reviewer on the sample; human validation used no AI. (3) Companion dataset: see Reuse Potential. The
claude-opus-5-5 model assisted in drafting and editing the text; figures are generated from the
data. The author designed the study, made all editorial decisions, verified every statement
against the data, and takes full responsibility for the content; an AI tool is not an author.

<!-- END OF SUBMISSION TEXT — the part below can be removed from the submitted version. -->

---

## Submission notes

Word count: sections 1–4 without title, author line, abstract, table and references (as the JOHD template counts)
1,088; with the unnumbered statements 1,248; with the references as well 1,322 (the submission page says
the limit includes references; it does not say whether the abstract counts); with the abstract too 1,400. The JOHD
data paper length is 1,000–1,500 words; the editorial office can confirm which count applies. Everything from the
abstract to the AI Declaration, with headings, keywords, author roles and the table: 1,494.

To fill in before submission: the human validation fields ([N], accuracy, CI, kappa, agreement with the model
reviewer), the corresponding author's e-mail address, the two validators' names. The text goes into the official JOHD
Word or LaTeX template; cover letter: `kozlemeny/data_paper/johd_cover_letter_en.md`.
