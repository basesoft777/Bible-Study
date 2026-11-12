# Known issues and limitations

*Károli 1908 – Strong word alignment · release 1 · data state: 2026-11-01*

This release publishes the alignment as it stood when it was measured, unchanged. Corrections of the issues below go
into release 2, with a new measurement (`METHODS.md` 7).

## Confirmed errors

1. **Five confirmed pair errors** in the sample and the compared chapters: Prov 3:18 (the pairs of "Életnek" and "fája"
   are swapped, two pairs), Ezek 43:13 ("közsinget": the pair belongs to another word), 2Kgs 10:15 (the
   interrogative "-é" is the interrogative particle, H9008, not H3426), Rom 1:12 ("Azaz": G1161 is untranslated and not
   part of the pair).

## Systematic errors

2. **Neighbouring word.** Of the 72 sample pairs differing from the blind reviewer, 37 are
   "neighbouring word" cases: the machine pair's source word is next to the one the reviewer marked. Often a Hebrew
   conjunction prefix, article or preposition attached to the word against the alignment rules; but the label also
   covers real swaps and reviewer mistakes. By type: wrong word in the verse 17, superfluous pair
   16, same lexeme at another occurrence 2.
3. **Measuring morphemes.** Pairs of Hebrew prefix and suffix morphemes (157,163 pairs, 33.7% of the
   Hebrew pairs) were measured by the blind reviewer only: 90.74% (95%: 87.18–94.29%). The independent
   comparison source does not mark them, and no other independent measurement exists yet.
4. **Missing pairs** (descriptive, not part of the accuracy): in the sample, for 18 words the blind reviewer
   marked more source words than the machine alignment.

## Limitations

5. **Pending verses:** in 45 verses (794 Hungarian and 794 source words) the verse
   division of the two texts cannot be matched word by word; these words have no pair and are marked `fuggoben`.
6. **Greek text form:** Károli translated the Textus Receptus, while the alignment uses TAGNT, which covers several
   editions. 369 aligned Greek words (436 pairs) are not in the Textus Receptus: there the Textus
   Receptus reads another form, and the pair is linked to the critical-text form. The `nem_tr` column marks them.
7. **Confidence:** two models aligned only Genesis and Exodus; every pair in the other books is the proposal of one
   model (`alacsony`). The `alacsony` label therefore means a single source, not a suspected error.
8. **Limits of the measurement:** the blind reviewer is itself a language model, and on an earlier manually compiled
   sample it is not more accurate than the alignment (96.79% and 97.06%); the agreement is a lower bound only
   if shared errors are negligible. The independent comparison covers 8 full chapters, on main-word
   pairs; the chapters are clusters, not random sample units, so the interval understates the uncertainty.

A release is cited by its identifier in `RELEASE.txt`.
