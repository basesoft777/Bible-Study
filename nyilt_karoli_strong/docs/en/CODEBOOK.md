# Codebook

*Károli 1908 – Strong word alignment*

## `data/parok/NN_Konyv.tsv`

| column | value | description |
|---|---|---|
| `osis` |  | OSIS verse identifier (book.chapter.verse), in Károli versification. |
| `token` |  | Position of the Hungarian word in the verse (from 1; punctuation is not a word). |
| `alak_1908` |  | Word form in the 1908 Károli text. |
| `eredeti_token` |  | Position of the source word in the TAHOT/TAGNT verse, keyed to the Károli verse (see docs/en/METHODS.md 3); Hebrew prefixes and suffixes count as separate words. |
| `strong` |  | Strong's number of the source word (H… Hebrew, G… Greek) from STEPBible TAHOT/TAGNT; "+" joins two numbers where the source gives two for one word. The model writes no Strong's number: it comes from the position. |
| `kapcsolat` | `szo` | The pair links the Hungarian word to a source word. |
| `kapcsolat` | `morfema` | The pair links it to a Hebrew prefix or suffix morpheme (H9001–H9049: article, conjunction, preposition, pronominal suffix). |
| `allapot` | `javaslat` | Machine alignment proposal with measured accuracy; not a manually verified pair. |
| `nem_tr` | `igen` | The Greek source word is not in the Textus Receptus, which Károli translated; the Strong number is that of the critical-text form (see docs/en/KNOWN_ISSUES.md). |

## `data/szavak/NN_Konyv.tsv`

| column | value | description |
|---|---|---|
| `osis` |  | OSIS verse identifier, in Károli versification. |
| `oldal` | `hu` | Hungarian word (Károli 1908). |
| `oldal` | `er` | Source word (Hebrew or Greek, TAHOT/TAGNT); its form is not in the package, it is identified by its position and Strong number. |
| `token` |  | Position of the word in the verse, on its side (from 1). Every Hungarian and every source word appears in exactly one row. |
| `alak_1908` |  | Form of the Hungarian word; empty for a source word. |
| `allapot` | `parositva` | The word has a pair on the other side (see partner_token). |
| `allapot` | `betoldas` | Hungarian word without a source counterpart: translator's addition, article, auxiliary, explicit subject pronoun. |
| `allapot` | `forditatlan` | Source word without a Hungarian counterpart (e.g. the Hebrew object marker, an article the Hungarian does not render). |
| `allapot` | `fuggoben` | The verse awaits a manual alignment decision (the verse mapping did not hold word by word, or the answer did not pass the machine gate); no pair. |
| `partner_token` |  | Position(s) of the pair(s) on the other side, comma-separated. |
| `strong` |  | For a source word its own Strong number; for a Hungarian word the Strong numbers of its partners joined by "+". |

## `data/versek.tsv`

| column | value | description |
|---|---|---|
| `osis` |  | OSIS verse identifier, in Károli versification. |
| `szoveg_1908` |  | The 1908 Károli text of the verse, with punctuation; word positions are counted on it. |

## `data/meres.tsv`

| column | value | description |
|---|---|---|
| `szakasz` | `reteg` | Agreement with the blind reviewer per stratum (book group): a simple random sample per stratum; in the five books of Moses two subsamples, combined by their pair weight. |
| `szakasz` | `sulyozott` | Estimate weighted by the pair share of the strata (OT, NT, all). |
| `szakasz` | `bontas` | Breakdown by link type (content word, morpheme), descriptive. |
| `szakasz` | `hibatipus` | Pairs differing from the blind reviewer, by type (`<stratum>:<type>`; n = number of differences in the stratum). |
| `szakasz` | `leiro` | Descriptive count, not part of the accuracy (hianyzo_par: where the blind reviewer marked more source words). |
| `szakasz` | `kalibracio` | Agreement of the blind reviewer and of the machine pair with an earlier manually compiled sample. |
| `szakasz` | `kulso` | Comparison with an independent Károli edition carrying Strong numbers, on main-word pairs (`_haromutas`: after the three-way judgement of the differences). |
| `cimke` |  | Subject of the row: stratum (OSZ_mozes: the five books of Moses; OSZ_tortenet: historical books; OSZ_koltoi: poetic books; OSZ_profeta: prophets; USZ_evangelium: Gospels and Acts; USZ_level: Epistles; USZ_jelenesek: Revelation), group or error type (folos_par = superfluous pair, szomszedos_token = neighbouring word, rossz_szo_a_versben = wrong word in the verse, azonos_lexema_mas_elofordulas = same lexeme, other occurrence). |
| `n` |  | Number of pairs measured. |
| `x` |  | Number of agreeing (correct) pairs; for an error type, the number of differences of that type. |
| `p` |  | Proportion (x / n; for weighted rows and the Moses stratum the weighted estimate). |
| `also95` |  | Lower bound of the 95% confidence interval. |
| `felso95` |  | Upper bound of the 95% confidence interval. |
| `modszer` | `wilson95` | Wilson interval. |
| `modszer` | `retegzett_normal95` | Stratified estimate, normal-approximation interval. |
| `modszer` | `retegzett_leiro` | Stratified (with the full weight of the stratum), descriptive. |
| `modszer` | `darab` | Count, without interval. |
