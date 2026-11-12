# Methods — the modernised Károli and the Strong linkage

*Modernised Károli – Strong · Logosz Lexikon · data state: 2026-11-01 · DOI: 10.5281/zenodo.24141950*

## 1. What this dataset is

The 1908 text of Gáspár Károli's Hungarian Bible translation in present-day spelling and present-day verb forms, linked
word by word to the Strong's numbers of the Hebrew and Greek source words. The text has 66 books, 31,158 verses and
599,367 words. The modernisation touches 64,388 words (including dropped words, 4.3) and 21,636 verses; all other words and verses are
unchanged.

The modernised text is the project's own work. The word alignment was made on the 1908 Károli text and is also
published as a separate dataset (https://doi.org/10.5281/zenodo.24141884). This dataset links the two.

## 2. Source text and key

The source is the public-domain 1908 Károli text. Every verse is split into words (tokens); a word is identified by its
verse and its position in the verse. The modernisation does not change this key: every modern form stands in the place
of the 1908 word. This is why the modern text can be linked to the alignment without a dictionary, re-alignment or
model.

## 3. Scope of the modernisation

By editorial decision the modernisation covers two things: **spelling** and **verb forms**. Vocabulary, word order,
punctuation and the marking of the translator's additions are unchanged. Where a form lay on the boundary, the editor
decided after measurement:

- the demonstrative *e* (*ez*), *oh*, *férfiú*, *leány* and similar word variants stay: that is vocabulary, not spelling;
- *reá* → *rá* and *néki, nékem, néked, nékik* → *neki, nekem…* are spelling;
- the possessive *-jok/-jök* → *-juk/-jük* is included; *-ök* without *j* → *-ük* only where the plural of the word is
  clearly different (*szívök* → *szívük*); back-vowel *-ok* stays, as it coincides with the plural;
- bare *a mi* becomes *ami* only where the context shows a relative pronoun (*a mi Istenünk*, "our God", stays);
- the old past with a linking vowel (*mondotta* → *mondta*, *szólott* → *szólt*) is replaced; the imperative
  *-jál/-jél* (*cselekedjél*) and *-jék* stay, as they are living, elevated variants today;
- the future in *-nd-* (*mondándok*) stays.

## 4. Procedure

### 4.1 Spelling

A rule set, word by word. Main rules: joining the separately written relative pronoun (*a kik* → *akik*, *a mely* →
*amely*; the "a" merges into the next word); old letter combinations (*cz* → *c*, *lyl* → *ll*, *szsz* → *ssz*); the
*néki* family and *reá*; old syllable spellings (*dícsér* → *dicsér*); and a dictionary table of the project giving the
present-day dictionary form of Károli's words, whose spelling differences (*miképen* → *miképpen*, *kivül* → *kívül*)
the rule adopts. The Hungarian Hunspell dictionary was only a benchmark: it was run to check the rules and did not
influence the published text.

### 4.2 Verb forms

A rule set for the frequent old verb forms (*teremté* → *teremtette*, *monda* → *mondta*, *lőn* → *lett*, *vagyon* →
*van*, *jő* → *jön*), with the project's own conjugation module (irregular stems, vowel elision, vowel harmony). The rule
separates the two roles of *vala*: existential *vala* → *volt*; auxiliary *vala* merges into the past-tense verb
(*mondja vala* → *mondta*) and drops out of the modern text. The choice between definite and indefinite conjugation is
not always readable from the old form: there the rule looks for a definite object in the clause and marks the word as
uncertain.

For rare and unmarked archaic forms the rule only proposes a candidate. These were reviewed by language models in
5 rounds, blind (the model did not see the rule's candidate):

1. a first model (Claude Sonnet) on every rare and suspect form;
2. a second model (Claude Opus) on the disputed forms, where the rule and the first model differed;
3–5. the second model in three further rounds: two on archaic forms re-surveyed over the whole text, the last word by
   word, with the full verse, on context-dependent cases.

A model's answer on its own changed nothing. A replacement was made where at least two candidates (the rule, the first
and the second model) agreed and the stem check passed: the modern form is a single word and keeps the verbal prefix
and stem of the old form, so the model could not substitute another word. Where there was no agreement, the word
stayed unchanged. The models ran on a subscription (Claude Code); tokens used according to the call logs: first model
1.42 M, second model 1.48 M.

Some forms went into a manual exception list where the rule or the dictionary table would have produced a wrong form
(*gyűl-*, *dűl-* stay; *érte* is a pronoun with postposition, not a verb).

### 4.3 Dropped and merged words

Two kinds of word disappear from the modern text: the "a" of the joined relative pronoun (11,128 words) and
auxiliary *vala* (2,618 words). A dropped word is not deleted: it keeps its own row, marked in the `kieso` column,
and `gazda_token` gives the word it merged into. If the dropped word has a Strong pair (6,723 such words),
that pair is kept and belongs to the host word in the modern text. When words merge, the Strong's numbers of both old
words are therefore kept.

### 4.4 Self-checks and review

An automatic self-check runs on every verse: re-tokenising the modern text must give exactly the modern forms of the
non-dropped words, in order, and the punctuation skeleton must not change. Every word key is in the table.

An independent reviewer examined the text in four rounds, followed by two correction rounds. Measured on samples (the
Wilson 95% intervals are computed by the release from the measured counts):

- spelling: 230 of the 230 replacements in the sample correct (95% upper bound of the error rate
  1.6%); on the 102-item check set for bare *a mi* 1 error (101/102,
  99.0%);
- verb forms: on the 120-verse sample 120 verses without error; on the second, 140-verse
  sample 216 replacements, 0 wrong (upper bound 1.7%); on the independent
  reviewer's fresh 100-verse sample 92 replacements, 0 wrong (upper bound 4.0%);
- coverage (did archaic verb forms remain): 94.8% on the same fresh sample (92 replacements,
  5 misses; 95%: 88.5–97.8%). This projects to about 1,560 verb forms left archaic in the
  whole text (95% Poisson band about 500–3,600). The higher coverage of the second sample is biased, because
  later rounds targeted exactly its misses.

The remaining known issues are listed in `KNOWN_ISSUES.md`.

## 5. The Strong alignment and its accuracy

The word alignment is a proposal of language models on the STEPBible TAHOT (Hebrew) and TAGNT (Greek) texts: for every
Hungarian word the model marks the Hebrew or Greek words; the Strong's number comes from these sources, the model does
not write it. In Genesis and Exodus two independent models aligned; where they agreed, the pair has `magas` (high)
confidence (52,844 pairs), elsewhere it is one model's proposal (`alacsony`, low; 545,871 pairs). Every pair has
the status "proposal".

Accuracy was measured on a stratified random sample with a blind reviewer, and against an independent Károli edition
with Strong's numbers:

- the full pair set (with function words and morphemes), agreement with the blind reviewer: 95.06% (95%:
  93.81–96.32%);
- pairs of main words against the independent source, on 2,663 pairs: 98.72% (95%: 98.22–99.08%); after
  three-way adjudication, which settled the differences with the blind reviewer, 99.81%;
- pairs of Hebrew prefix and suffix morphemes: 90.74% (95%: 87.18–94.29%); the independent
  source does not mark these.

## 6. The linkage

Linking the modern text and the alignment is a join on the key: verse and word position. No pair is created and none
is lost. An automatic gate verifies that all 598,715 pairs were carried over, that the key of all 488,659
aligned words is in the modern table with the same 1908 form, that every modern word is present, and that the package
regenerates byte for byte. Added (109,914) and pending (794) words have no pair.

## 7. Limitations

- The alignment is a machine proposal; its accuracy is given above, known issues in `KNOWN_ISSUES.md`.
- The modernisation is neither a new translation nor a revision: vocabulary and word order are Károli's.
- Some context-dependent verb forms are marked uncertain (2,361 words).
