# BSB Bible Data

Auto-generated Bible data files from the Berean Standard Bible with Strong's numbers,
cross-references, topics, and morphology.

> **Note:** Do not edit these files directly. They are rebuilt automatically from
> source data by the bsb-data build pipeline.

## Directory Structure

```
.
├── base/                    # Core data files
│   ├── display/             # Per-chapter JSONL for web rendering
│   │   └── {BOOK}/
│   │       └── {BOOK}{chapter}.jsonl
│   ├── index-cc-by/         # CC-BY index split by chapter (CC-BY 4.0)
│   │   └── {BOOK}/
│   │       └── {BOOK}{chapter}.jsonl
│   ├── concordance/         # Strong's to verse mapping
│   │   ├── strongs-to-verses.json
│   │   └── strongs-to-verses.jsonl
│   ├── headings.jsonl       # Section headings index
│   └── paragraphs.jsonl     # Paragraph/poetry/list break index
├── vector-db/               # Vector DB index files
│   ├── index-pd/            # Vector DB index (Public Domain)
│   │   └── bible-index.jsonl
│   └── index-cc-by/         # Vector DB index with morphology (CC-BY 4.0)
│       └── bible-index.jsonl
├── schema/                  # JSON schemas for all formats
│   ├── display.schema.json
│   ├── headings.schema.json
│   ├── paragraphs.schema.json
│   ├── book-codes.schema.json
│   └── vector-db/
│       ├── index-pd.schema.json
│       └── index-cc-by.schema.json
├── VERSION.json             # Source versions and build date
└── README.md                # This file
```

## Licenses

| Directory | License | Attribution Required |
|-----------|---------|---------------------|
| `base/display/` | CC0 (Public Domain) | No |
| `base/index-cc-by/` | CC-BY 4.0 | **Yes** |
| `base/concordance/` | CC0 (Public Domain) | No |
| `vector-db/index-pd/` | CC0 (Public Domain) | No |
| `vector-db/index-cc-by/` | CC-BY 4.0 | **Yes** |
| `schema/` | CC0 (Public Domain) | No |

### CC-BY Attribution (required for index-cc-by)

When using `base/index-cc-by/` or `vector-db/index-cc-by/` data, include this attribution:

> Hebrew morphology data from [Open Scriptures Hebrew Bible (OSHB)](https://hb.openscriptures.org/),
> licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Data Formats

### Display Format (`base/display/{BOOK}/{BOOK}{chapter}.jsonl`)

Compact format with English and original language (Hebrew/Greek) text. Each line is a single verse:

```json
{"eng":{1:[["In the beginning","H7225"],["God","H430"],["created","H1254"],...]},"heb":{1:[["בְּרֵאשִׁ֖ית","H7225"],["בָּרָ֣א","H1254"],["אֱלֹהִ֑ים","H430"],...]}}
```

For NT books, `grk` is used instead of `heb`:
```json
{"eng":{1:[["[This is the] record","G976"],["of [the] genealogy","G1078"],...]},"grk":{1:[["Βίβλος","G976"],["γενέσεως","G1078"],...]}}
```

Verses that begin a new section heading or paragraph/poetry/list break carry a `structure` field (BSB edition only), keyed by verse number, so display is self-sufficient for reconstructing BSB's original layout without a separate join against `headings.jsonl`/`paragraphs.jsonl`:

```json
{"eng":{...},"heb":{...},"structure":{"6":{"headings":[{"level":"s2","text":"The Second Day"}],"para":["pmo"]}}}
```

### Index Format (`vector-db/index-pd/bible-index.jsonl`)

Enriched format for vector DB indexing:

```json
{
  "id": "GEN.1.1",
  "b": "GEN",
  "c": 1,
  "v": 1,
  "t": "In the beginning God created the heavens and the earth.",
  "s": ["H7225", "H430", "H1254", "H8064", "H853", "H776"],
  "x": ["JHN.1.1", "HEB.11.3", "PSA.33.6"],
  "tp": ["Creation", "God, Creator"],
  "g": {"H7225": "beginning", "H430": "God", "H1254": "to create"}
}
```

### Index Format with Morphology (`vector-db/index-cc-by/bible-index.jsonl`)

Same as index-pd plus morphology data:

```json
{
  "...all index-pd fields...",
  "m": [
    {"s": "H7225", "m": "HR/Ncfsa", "p": "noun", "l": "רֵאשִׁית"},
    {"s": "H430", "m": "HNcmpa", "p": "noun", "l": "אֱלֹהִים"}
  ]
}
```

## For Downstream Projects

This data is designed to be extended. To add your own enrichments:

1. Fork or clone this repository
2. Read from `base/` directories
3. Write your enhanced data to a new directory (e.g., `enhanced/`)
4. The schemas allow `additionalProperties` for custom fields

Example structure for an enhanced project:

```
your-project/
├── bsb-data-output/          # This repo as submodule
│   └── base/
├── scripts/
│   └── enhance.py            # Your enrichment code
└── enhanced/
    └── bible-enhanced.jsonl  # Your output with added fields
```

## Version Info

See [VERSION.json](VERSION.json) for source commit SHAs and build timestamp.

## Source Repositories

- **BSB-USJ:** https://github.com/BSB-publishing/bsb2usfm
- **Bible Databases:** https://github.com/scrollmapper/bible_databases
- **OSHB:** https://github.com/openscriptures/morphhb
