# The Károli Bible in present-day spelling, linked word by word to the original languages

*Announcement draft · Modernised Károli – Strong · Logosz Lexikon · DOI: 10.5281/zenodo.24141950*

Gáspár Károli's Bible translation is one of the foundational texts of the Hungarian language, but the spelling and verb
forms of its 1908 edition — *teremté, monda, vala, lőn, a kik* — stop the present-day reader. The Logosz Lexikon now releases a
modernised version of the text under an open licence, and links every word to the Hebrew or Greek word it translates.

**What, and what not.** The modernisation is deliberately narrow: only spelling and verb forms change (*teremtette,
mondta, volt, lett, akik*). Vocabulary, word order, punctuation and the translator's additions remain Károli's. Where a
form lay on the boundary — *reá*, or the possessive *-jok* — an editorial decision was taken after measurement, and it
is documented in the methods description. Of the text's 31,158 verses, 21,636 changed.

**How.** Most of the work was done by rules, word by word, with the project's own dictionary table and conjugation
module. Rare and doubtful verb forms were reviewed by language models, blind, in five rounds; a form changed only where
at least two independent proposals agreed and the stem check let it through. An independent reviewer examined the text
in four rounds. On the reviewer's fresh 100-verse sample 0 of the 92 verb-form replacements
were wrong (95% upper bound of the error rate 4.0%), and 0 of the 230 replacements
in the spelling sample; the 102-item check set for bare "a mi" had 1 error. On the same fresh sample
94.8% of archaic verb forms were modernised (92 replacements, 5 misses; 95%:
88.5–97.8%), which projects to about 1,560 verb forms left archaic in the whole text (95% band about
500–3,600). The remaining errors are named in the published list of known issues.

**The Strong's numbers.** The word alignment was made on the 1908 Károli text and is also published as a separate
dataset. Since the modernisation left every word in its place, the two layers join on a simple key — verse and word
position: no re-alignment was needed and no pair was lost. Where two old words merged (*a kik* → *akik*), the pairs of
both were kept. The accuracy of the alignment was measured against an independent source: 98.72% on main words, and
95.06% on the full pair set against a blind reviewer.

**For whom.** Bible readers who want the familiar Károli in present-day form and open towards the original words;
researchers studying Hungarian biblical usage together with the Hebrew and Greek text; developers building on an open,
word-keyed Hungarian Bible text.

The dataset is freely usable under CC BY 4.0: https://doi.org/10.5281/zenodo.24141950
