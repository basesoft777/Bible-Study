# Statement on the Use of Artificial Intelligence and on Authorship

*Magyar változat: [MI_NYILATKOZAT.md](../MI_NYILATKOZAT.md)*

<!-- Source layer, hand-written text (F169.1); English version of kozlemeny/MI_NYILATKOZAT.md (F163.1). Wording is adapted, not word-for-word; the Hungarian file is authoritative in case of divergence. The [PLACEHOLDER: …] parts are to be filled in or approved by the author; while a placeholder remains, the text is not public. -->

*Status: 4 November 2026. This statement describes the actual practice of the work as it stands today, not a plan.*

## Two layers, two units of citation

The work consists of two layers, and artificial intelligence (AI) bears on them differently.

| Layer | Contents | Role of AI | Citation and licence |
|---|---|---|---|
| **Open data core** | motif identifier, definition, exclusion criterion, occurrences, excluded passages, decisions with rationale | queries are deterministic programs; classification decisions are made in AI-assisted working sessions; every row names its origin: the query it derives from, or "manual" (a hand decision) | a stand-alone dataset, CC BY 4.0 (in force from the open release), with its own identifier: `<KANONIKUS_FORRAS_URL>` |
| **The lexicon (work)** | interpretive text, the Hungarian translation of the lexica, the Károli alignment, the volume, tools | the interpretive prose and the lexicon translation were written by a language model; the Károli alignment is largely machine-generated | a separate work, all rights reserved |

The open data core is the data layer of the lexicon; the lexicon itself (its interpretive text, the Hungarian translation of the dictionaries, and the printed volume) is a separate work, all rights reserved. Model-written prose is therefore part of the lexicon. The data core contains no model prose, only decisions and short rationales, each with a provenance mark.
<!-- provenance: the boundary between the layers: #86 implementation plan 1.5 (the separation of the open data core and the lexicon), the user's additions relayed through the orchestrator (the data layer is kept apart, according to the research; "GitHub does not remain the source", 2026-11-04; the open data core / lexicon scheme: "this scheme is good", 2026-11-04); the current LICENSE is still all rights reserved, and CC BY takes effect with the open export (#162) | ts=2026-11-04 -->

## What AI wrote

**The interpretive sections.** The interpretive sections of the motif pages (Summary; Why this finding matters; Interpretation; Application and discipleship; Named-teacher match, where present; Methodology and open questions) were written by a large language model on the basis of the data. The model's name appears in the colophon of every published page, per release (at present on every published page: `claude-opus-5-5`, Anthropic). The interpretive prose of a page is written by one model, and whoever revises it rereads the whole.

**The classification of occurrences.** Candidate occurrences of a motif are retrieved from the Hebrew and Greek text by deterministic queries (lexical match, word pair within a verse, verb form, Septuagint correspondence). Whether a passage belongs to the motif is decided in an AI-assisted working session, and every decision is recorded with a rationale: accepted and rejected passages alike. At present, of 792 passages examined, 411 are rejected, 255 accepted and 126 open.
<!-- provenance: scope=main be54d328, occurrence candidates (jelolt_tipus=elofordulas) by decision | source=adat/jeloltek.tsv | ts=2026-11-04 -->

**The Hungarian translation of the lexicon material.** The Hungarian text of the dictionary entries quoted on the pages (Brown–Driver–Briggs, Thayer, and short Hebrew–Greek glosses) is in large part machine-translated by a language model (`claude-sonnet-5-5`) and to a small extent corrected by hand. The translation follows a fixed glossary of technical terms, and for every translated unit the model that produced it is stored.
<!-- provenance: scope=main be54d328, count by state and model (BDB sonnet 29,862, Thayer sonnet 1,967; manual/opus rows orders of magnitude fewer) | source=adat/forditasok.tsv, adat/glosszak_heber_hu.tsv | ts=2026-11-04 -->

**The alignment of Károli words.** Which word of the Károli translation (the classic Hungarian Protestant Bible) corresponds to which Hebrew or Greek word is supplied largely by machine alignment. Every such row on a page states the method of identification and the degree of confidence.

## What AI did not write

The parts generated from the data tables (occurrence tables, dictionary blocks, relations, source list, colophon) are produced by programs, not by a language model; from the same data they always come out the same. The underlying texts (the Hebrew and Greek text, the Károli translation, the lexica) are third-party sources; every page lists the sources and their licences.

## Who and what checks

| Check | Performed by | What it does |
|---|---|---|
| Automated gates | program | measures reader-facing defects on every page (internal markup, residual English, mismatch between text and table, missing source, etc.); on a published page the number of defects must be zero |
| Change verification | a separate model run with fresh context | re-verifies the changes of each work step with its own queries |
| Reviewer's question list | a model other than the one that wrote the prose (`claude-fable-5-1`) | asks questions at marked places in the prose (does it contradict the data, is it comprehensible, does it assert without support); it does not rewrite. It has so far been run on three motifs; its questions are inputs to the next release |
| Boundary check | automated analysis and a second model | examines whether the boundary of a motif is consistent and whether it is not diluting |
| Visual review | the author | reviews the rendered page before release; approval is tied to the given version of the page and must be repeated if the page changes |
| Page correction | the author (or an external reviewer) | points to a place and approves the correction; the page's colophon lists the number of corrected places and the approvers |

## What this statement does not claim

- **This is not independent expert peer review.** Part of the checking is done by programs, part by a language model (a model checking a model); the human review is carried out by the author alone.
- **There is at present no named external editorial board or advisory body.**
- The model is not an author and bears no responsibility for the text.

## Authorship and responsibility

[PLACEHOLDER: AUTHOR'S STATEMENT OF RESPONSIBILITY — the author's own sentence. Suggestion: "The author and publisher of [PLACEHOLDER: TITLE OF THE LEXICON] is [PLACEHOLDER: AUTHOR'S NAME]. I have reviewed and approved the AI-assisted texts in the manner described above; I am responsible for the content."]

According to the practice of scholarly publishers, an AI tool cannot be an author, its use must be named and described, and responsibility rests with the human author (Cambridge University Press, 2023; De Gruyter Brill does not accept an article or chapter written primarily by AI). In its present form this work is therefore **an AI-assisted database and lexicon**, not a peer-reviewed scholarly publication. Argumentative text intended for a journal is written by the author, who names the above in a separate declaration there. We have not found a relevant rule of the Society of Biblical Literature.

## Sources

- Cambridge University Press: *Cambridge launches AI research ethics policy* (2023). https://www.cambridge.org/sv/news-and-insights/cambridge-launches-ai-research-ethics-policy
- De Gruyter Brill: *AI-Policy for Authors.* https://degruyterbrill.com/en/ai-for-authors (the content of the publisher's page is known to us from a search excerpt)
- Elsevier: *Generative AI policies for books.* https://www.elsevier.com/de-de/about/policies-and-standards/publishing-ethics-books/generative-ai-policies

<!-- provenance (facts of the statement): scope=main be54d328 | source=adat/kiadasok.tsv (proza_modell: 5/5 rows claude-opus-5-5), naplok/KIADAS_{ALVIL-001,ISTENTISZT-001,TEREMT-002}_lektor.md (reviewer: claude-fable-5-1), .claude/agents/{lektor,hatar-ellenor,fuggetlen-ellenor}.md, MUNKAMENET.md C-g…C5, C-j, adat/SEMA.md 2.46, 2.48, 2.49, eszkozok/lexikon_general.py kolofon_szerzoseg; publishers' rules: naplok/kutatas_2026-10-27/jelentesek/Motivumlexikon_mint_kutatoi_termek.md | ts=2026-11-04 -->
