# PaRDeS Open Core — Read Me

# GENERATED: export of the PaRDeS open core (CC BY 4.0), generated from the project data — do not edit by hand; a line starting with "#" is a comment.

*Magyar változat: `OLVASSEL.md`.*

**Licence:** CC BY 4.0 (the open core's own data and text). The contents of the `cc_by_sa_reteg/` directory are under a separate licence, CC BY-SA 4.0; see the `OLVASSEL.md` there.

**What this is.** The open core of a study of biblical motifs (the PaRDeS method): the defining features of the motifs, the list of occurrences, the excluded passages with reasons, the relations between passages and the decision log. The files are reader-facing views generated from the data; working marks are resolved. The columns and codes are described in `kodkonyv.tsv` / `KODKONYV.md` (Hungarian and English).

**Known errors:** see `KNOWN_ISSUES.md`.

## Files and their row counts

| File | Rows |
|---|---|
| `beepitesi_dontesek.tsv` | 257 |
| `cc_by_sa_reteg/szemantikai_domenek.tsv` | 237 |
| `dontesnaplo.tsv` | 8 |
| `elofordulasok.tsv` | 255 |
| `forrasok_es_licencek.tsv` | 54 |
| `kapcsolatok.tsv` | 32 |
| `kizaras_csoportok.tsv` | 3115 |
| `kizarasok.tsv` | 418 |
| `kodkonyv.tsv` | 210 |
| `motivum_kapcsolatok.tsv` | 3 |
| `motivumok.tsv` | 9 |

## Licence filtering

The filtering follows the project's licence inventory. **Excluded sources** (the package contains no value from them): `BDB_forditas`, `Cremer_nyers`, `Girdlestone`, `Heber_ETCBC_modulok`, `KJV_ASV_Strongs`, `KJV_Strongs_teljes`, `KJV_teljes_szoveg`, `Karoli_Strong_kivonat`, `Karoli_Strong_parok`, `Karoli_Strong_szavak`, `Karoli_versmegfeleltetes`, `LSJ`, `LXX_kivonat`, `LXX_lexicon`, `LXX_versszintu_parok`, `MCGED`, `SDBH_SDGNT_segedtablak`, `UBS_DBH`, `UBS_DNTG`, `karoli_modern`, `karoli_variancia`, `lexikonok_nyers`, `simplemma_nyelvi_adat`, `szoto_tablak`, `tW_szocikkek`. The reason for each is given in the `ok` column of `forrasok_es_licencek.tsv` (non-commercial or GPL licence, unclear licence, the project's closed derived layer). This is an inventory, not a legal opinion.

## Place of publication

The canonical place of publication of the package: `<KANONIKUS_FORRAS_URL>` (a placeholder, filled in at publication). A version is identified by the release identifier (`RELEASE.txt`: the date of the data state and the content hash), not by a development repository or a commit.

## Citation and the use of artificial intelligence

With the release, citation metadata (Citation File Format) and a statement on the use of artificial intelligence are provided at the place of publication; their fields to be completed by the author are placeholders until publication. The statement separates two layers: the open data core (CC BY 4.0, this package) and the entries as a related work (all rights reserved).

## Group exclusion

Some rows of `kizarasok.tsv` are **summary rows**: they name the first verse of a group (verses excluded for the same reason), the `csoport_versszam` column gives the number of verses in the group, and `kizaras_csoportok.tsv` lists all verses of the group. The rationale of a summary row applies to the whole group.

## What is in it and what is not (data layer and product layer)

**Included (data layer):** the motif identifier, title and exclusion criterion; the occurrences (passage, lexical base, dictionary meaning, Károli word); the exclusions and inclusion decisions with rationale; the relations; provenance (the naming of the source, its licence, the type of query, the date); the decision log.

**Not included (product layer):** the interpretive prose (summary, interpretation, passage-by-passage exposition), the Hungarian dictionary translations, the volume material and the lexicon pages.

## What is not in the package

- Candidates in the `nyitva` (open, not yet decided) state: 129.
- The interpretive prose, the paid layer (Hungarian dictionary translations, Károli text with Strong's numbers), the studies and the lexicon pages.
- Internal working marks: identifiers, working files, query traces. Where a decision is referred to, the public identifier (`NYD-nnn`) can be resolved in `dontesnaplo.tsv`.

## Verification

The file `ELLENORZO_OSSZEG.sha256` contains the SHA-256 sum of every file; rerunning the export is byte-identical.
