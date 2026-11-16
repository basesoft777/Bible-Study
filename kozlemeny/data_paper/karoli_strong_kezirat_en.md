<!-- GENERÁLT: eszkozok/karoli_strong_export.py (a próza: eszkozok/karoli_strong_szovegek.py, a számok: adat/karoli_strong/ és f172/) — kézzel nem szerkesztendő; a #175 második data paperének kézirata, nem része a nyilt_karoli_strong/ csomagnak. -->
# Word-by-word alignment of the 1908 Károli Bible with the Hebrew and Greek source text: an open dataset with measured accuracy

*Data paper · submission draft for the Journal of Open Humanities Data · dataset DOI: 10.5281/zenodo.24141883*

**Tamás Demeter**, independent researcher · ORCID: https://orcid.org/0009-0005-9254-9731 · corresponding author: [e-mail address]

## Abstract

The dataset aligns the 599,367 words of the 1908 Károli Bible, the classic Hungarian translation, with the Hebrew
and Greek source text (STEPBible TAHOT/TAGNT) in 598,715 word pairs carrying the source word's Strong's number. A
language model marked word positions only; the Strong's numbers come from the source data. Accuracy is 95.06% (95%
CI 93.81–96.32%) against a blind model reviewer on a stratified sample, 98.72% on main words against an
independent Strong-tagged Károli edition, and [accuracy] by two human validators. The TSV tables (CC BY 4.0) support
Strong-based search, translation history and word-alignment research.

**Keywords:** Károli Bible; Strong's numbers; word alignment; Hungarian; biblical Hebrew; Koine Greek

**Author roles (CRediT):** Tamás Demeter: Conceptualization, Methodology, Software, Data curation, Validation,
Writing – original draft, Writing – review & editing.

## 1. Overview

### Repository location

https://doi.org/10.5281/zenodo.24141883 (concept DOI; current version 1.0).

### Context

The dataset was produced in the Logosz Lexikon, the author's independent research project. The Károli translation has been
the base text of Hungarian Protestant Bible reading for four centuries. Strong's numbers (Strong, 1890) link a
translation's words to the Hebrew and Greek vocabulary. Strong-tagged Károli editions exist; this alignment is openly
licensed, documented word by word, and its accuracy is measured.

For each verse it records which Hungarian word renders which source word, which Hungarian words are additions and
which source words remain untranslated. Links may be one-to-many or many-to-one: *Azután* covers *ʾaḥărê kēn*
(Joshua 8:34), and *meg van írva* renders *kātûb* (1 Kings 2:3).

## 2. Method

### Steps

**Texts and tokenisation.** The Hungarian side is the public-domain 1908 Károli text; the source side is the STEPBible
TAHOT (Hebrew and Aramaic Old Testament) and TAGNT (Greek New Testament) data (Tyndale House, Cambridge; CC BY 4.0).
TAHOT counts Hebrew prefixes and suffixes as separate words (H9001–H9049). Károli's verse division was mapped to the
source by deterministic length alignment; each verse merge was approved by hand.

**Alignment.** For each verse a language model (Claude Sonnet) received two numbered word lists: the Károli words, and
the source words with form, Strong's number and a short English gloss from TAHOT/TAGNT; the Strong's number was given
for information only and was forbidden in the answer. The fixed instructions also showed an optional Strong-tagged KJV
line in a worked example; no verse input contained one. The model returned position pairs only, with the additions and
untranslated words. In Genesis 1:1, for example, it paired *teremté* (2) with source word 3 (*bārāʾ*) and *Kezdetben*
(1) with words 1–2 (*bə-*, *rēʾšît*), and marked the object marker *ʾēt* (5) as untranslated; a program then attached
H1254, H9003 and H7225 by position. Twelve written rules decided disputed cases. Function words follow fixed
conventions: Hungarian articles, and auxiliaries without a source word, count as additions, and Hebrew and Greek
articles as untranslated, since article use does not correspond one to one between the languages; an article
functioning as a pronoun is linked. A program checked every answer (each Hungarian word exactly once, each source
word at least once, only existing positions); a failed answer was redone. The model thus could not invent a Strong's
number or lexicon entry; its possible error is a wrong pairing, and every pair points to one source word, which the
human validation checks. Meaning and Strong's number come from the open scholarly source data. Python programs rebuild
the tables byte-identically from the saved answers.

### Sampling strategy

The blind review used a stratified random sample: the pair set was divided by book group into seven strata
(the five books of Moses; historical, poetic and prophetic books; Gospels and Acts; Epistles; Revelation), with
200 pairs per stratum (400 from the five books of Moses, in two subsamples combined by pair weight).
The independent comparison is a cluster sample: one full chapter per stratum, two in the five books of Moses
(eight chapters, 2,663 main-word pairs).

### Quality control

**Blind model review and calibration.** A second model (Claude Opus) marked the source words for each sampled
Hungarian word itself, with the same rules, blind to the machine pair. On an earlier hand-compiled sample the reviewer agreed
in 96.79% and the machine alignment in 97.06%; as the reviewer is no more accurate than the alignment, its
agreement is a lower bound only if shared errors are negligible.

**Independent comparison.** Shared errors are measured against a Strong-tagged Károli edition, which marks one main
Strong's number per Hungarian word; only that pair is scored, so further pairs (morphemes, multi-word links) do not
count as errors. Differences were judged three ways (machine pair, source, blind reviewer). Only the aggregate rate is
published, not the external source's data.

**Human validation.** Two independent human validators, theology graduates with knowledge of biblical Hebrew and Greek,
judged a stratified random sample of [N] pairs and of unpaired words, each without seeing the other's judgements;
rule-determined function words were excluded from the unpaired sample. Accuracy by their judgement
is [accuracy] (95% CI [CI]); inter-rater agreement is Cohen's kappa = [kappa]; their agreement with the blind model
reviewer is [agreement with model reviewer].

| measurement | estimate | 95% CI |
|---|---|---|
| full pair set, blind reviewer, weighted | 95.06% | 93.81–96.32% |
| of which Old / New Testament | 94.50% / 97.07% | 92.95–96.05% / 95.55–98.59% |
| content word / Hebrew morpheme | 96.44% / 90.74% | 95.20–97.69% / 87.18–94.29% |
| main words, by the independent source | 98.72% | 98.22–99.08% |
| main words, after three-way judgement | 99.81% | 99.56–99.92% |
| human validation | [accuracy] | [CI] |

Agreement per stratum ranges from 93.00% (prophets) to 98.00% (Gospels and Acts); per stratum: `data/meres.tsv`. Of
the 1,600 sample pairs, 72 differed from the reviewer, most often by a neighbouring word
(37): typically a Hebrew prefix, article or preposition attached against the rules. Of the
34 differences in the independent comparison, five remained alignment errors; all confirmed errors are
listed in the dataset.

## 3. Dataset Description

- **Repository name:** Zenodo
- **Object name:** `karoli-1908-strongs-1.0.zip`
- **Format names and versions:** TSV (UTF-8, tab-separated, LF line endings) for the data and the machine-readable
  codebook; Markdown for the bilingual documentation (codebook, methods description, known issues); CFF citation file;
  SHA-256 checksum list
- **Creation dates:** 2026-10-01 – 2026-11-01
- **Dataset creators:** Tamás Demeter (independent researcher; ORCID: 0009-0005-9254-9731): rules, processing pipeline, measurement,
  curation. Source-side words and Strong's numbers: STEPBible (Tyndale House, Cambridge).
- **Language:** Hungarian (word forms, column names and codes); Hungarian and English (documentation, bilingual codebook)
- **License:** CC BY 4.0
- **Publication date:** 2026-11-15

**Contents.** `data/parok/` (per book, one row per link: positions, Hungarian form, Strong's number, link type, state,
Textus Receptus flag); `data/szavak/` (per book, every word once, with its state: aligned, addition, untranslated,
pending); `data/versek.tsv` (the 1908 Károli text); `data/meres.tsv` (every figure of the measurement). The key is the
OSIS verse identifier and the word position. Source word forms are not included; positions match the STEPBible text.

**Size.** 66 books, 31,158 verses, 598,715 pairs (466,785 Hebrew, 131,930 Greek; of these 157,163
morphemes), 109,914 additions, 63,017 untranslated source words, 794 pending Hungarian words
(45 verses).

## 4. Reuse Potential

Bible software can offer Strong-based search on the Hungarian text: every Károli rendering of a source word is one
filter away. Translation historians can study Károli's consistency, additions and untranslated words. For language
technology it is word-alignment data for a low-resource language pair (Hungarian–Hebrew, Hungarian–Greek) with error
measured per stratum; the sample pairs and error types can also serve to evaluate word aligners. The Logosz Lexikon, a
motif-indexed, cross-referenced biblical lexicon, is built on this alignment.

A companion dataset carries the same pairs on a modernised Károli text (Demeter, 2026b). The modernisation, the
author's own work, changes only spelling and verb forms, by rules; for rare verb forms, language models proposed
changes, applied only where independent proposals agreed and passed a stem check; the result was independently
reviewed. Every word kept its position, so the two datasets join on the verse and word-position key.

Limitations. The alignment is a machine proposal, and the blind reviewer is itself a model. The independent comparison
covers main words only, on a small cluster sample; the Hebrew morpheme pairs (157,163) are outside it. Károli
translated the Textus Receptus and the alignment uses TAGNT; the 369 aligned Greek words absent from the
Textus Receptus are flagged. Release 2 will correct the confirmed errors and remeasure against quality targets fixed in
advance.

## Data Accessibility Statement

Both datasets are openly available on Zenodo under CC BY 4.0: https://doi.org/10.5281/zenodo.24141883 and
https://doi.org/10.5281/zenodo.24141949.

## Acknowledgements

The author thanks [name of validator 1] and [name of validator 2] for the human validation.

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

Generative AI was used in three places. (1) Alignment: Claude Sonnet (Anthropic; the batch runs are logged as
claude-sonnet-5-5) returned position pairs only (see Method). For Genesis and Exodus, another language model was also
run as a cross-check; no published pair derives from it alone. (2) Quality control: Claude Opus served as blind
reviewer on the sample; human validation used no AI. (3) Companion dataset: language models proposed rare verb forms
only (see Reuse Potential). All other processing is deterministic. The claude-opus-5-5 model assisted in drafting and
editing the manuscript text from the dataset's data; figures come from the data. The author designed the study, made
all editorial decisions, verified every statement against the data, and takes full responsibility for the content; an
AI tool is not an author.

<!-- END OF SUBMISSION TEXT — the part below can be removed from the submitted version. -->

---

## Submission notes

Word count: sections 1–4 without title, author line, abstract, table and references (as the JOHD template counts)
1,147; with the unnumbered statements 1,320; with the references as well 1,394 (the submission page says
the limit includes references; it does not say whether the abstract counts); with the abstract too 1,488. The JOHD
data paper length is 1,000–1,500 words; the editorial office can confirm which count applies.

To fill in before submission: the human validation fields ([N], accuracy, CI, kappa, agreement with the model
reviewer), the corresponding author's e-mail address, the two validators' names. The text goes into the official JOHD
Word or LaTeX template; cover letter: `kozlemeny/data_paper/johd_cover_letter_en.md`.
