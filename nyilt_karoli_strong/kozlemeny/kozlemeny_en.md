# The Károli Bible linked word by word to the original languages — with measured accuracy

*Announcement draft · Károli 1908 – Strong word alignment · Logosz Lexikon · DOI: 10.5281/zenodo.24141884*

A reader of the Károli Bible, the classic Hungarian translation, who asks which Hebrew or Greek word stands behind a
Hungarian word, today turns to handbooks and concordances. The Logosz Lexikon now releases, under a free licence, a word-by-word
alignment of the 1908 Károli text with the source text: each of the 598,715 word pairs states which Hebrew or Greek word
the Hungarian word translates, and its Strong's number.

**How it was made.** The alignment was done by language models, verse by verse, following a written rule set: when the
Hungarian article is an addition, where a Hebrew possessive suffix belongs, what to do with a split relative pronoun.
The model only marked which word goes with which; it wrote no Strong's numbers, which come from the open STEPBible
Hebrew and Greek text. A program checked every answer, so that no word is left out and none appears twice. Genesis and
Exodus were aligned by two independent models; where they agreed, the pair is marked high confidence.

**How accurate.** The alignment is not error-free, and we do not claim it is. We claim that it has been measured, and we
publish every figure of the measurement. On a random sample drawn from eight strata, a third model that did not see the
pairs agreed with the alignment in 95.06% (95%: 93.81–96.32%). Main-word pairs were also compared with
an independent Károli edition marked with Strong's numbers: 98.72% agreed (95%: 98.22–99.08%). The weaker point is
the alignment of Hebrew prefixes and suffixes (90.74%), and the confirmed errors are listed by name.

**Why now.** Because the measurement is documented: whoever uses the data knows how far to trust it, per stratum and per
link type. The next release corrects the errors found and measures again with the same method; its quality target was
fixed in advance.

**For whom.** For Bible readers looking for the original behind a word of the Károli; for researchers studying Hungarian
biblical vocabulary together with the Hebrew and Greek text; for developers building on free, word-keyed Hungarian Bible
data. The same pairs are also available on the modernised Károli text (https://doi.org/10.5281/zenodo.24141950).

The dataset is freely usable under CC BY 4.0: https://doi.org/10.5281/zenodo.24141884
