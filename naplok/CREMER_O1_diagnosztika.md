# CREMER O1 diagnosztika (O0.5f/5)

A pilot-lapok MEGLEVO gyorsitotar- es hibanaplo-adatabol, halozati hivas NELKUL, a jelenlegi validalasi/dontesi szabalyokkal (D15/D17, O0.5f/1a-c: eszkoz-szamitott `extra`, tobbszavas alak szetbontasa, irasjel-levagas az osszevetes elott) ujraertelmezve. `m1` = `qwen/qwen3-vl-32b-instruct`, `m2` = `google/gemini-3.8-flash`.

Teljes dontessel feldolgozott lap: **19 / 20**.
`auto`+`extra_auto` arany a feldolgozott lapok osszes soraban: **14.0%**.
Adathianyos lap (legalabb az egyik modellnek nincs gyorsitotar-talalata, a teljes dontes-eloszlasbol kimaradt): **380**.

## a) dontes-eloszlas, nyelvenkent

| dontes | nyelv | darab |
|---|---|---|
| extra_vitas | grc | 904 |
| vitas | grc | 684 |
| hianyzo_m2 | grc | 524 |
| auto | grc | 340 |
| valtozatlan | nincs | 269 |
| extra_auto | grc | 87 |
| hianyzo_m2 | heb | 76 |
| hianyzo_m1 | grc | 59 |
| vitas | heb | 27 |
| hianyzo_m2 | lat | 22 |
| extra_vitas | heb | 21 |
| hianyzo_m1 | heb | 17 |
| hianyzo_m1 | lat | 13 |
| extra_vitas | lat | 10 |
| vitas | lat | 1 |
| **osszesen** | | **3054** |

## b) a `vitas` sorok bontasa

| tipus | darab |
|---|---|
| csak ekezet/hehezet kulonbseg | 59 |
| csak kis-/nagybetu kulonbseg | 20 |
| betukulonbseg | 496 |
| eltero szo_ids | 115 |
| eltero nyelv | 22 |

## c) valodi `ervenytelen` elemek modellenkent

(a hibanaplo OSSZES eddig irt kiserletebol, a jelenlegi szabaly szerint -- a korabban meg 'nem-x' miatt elutasitott, ma mar elfogadott/extra-kent kezelt elemek itt NEM szamitanak)

| modell | valodi ervenytelen |
|---|---|
| qwen/qwen3-vl-32b-instruct | 82 |
| google/gemini-3.8-flash | 99 |

## d) 30 veletlen `vitas` sor (mag: 20260924)

| level | hOCR | m1 | m2 |
|---|---|---|---|
| 17 | iroxdta Tis | [{"szo_ids": ["word_000017_000442"], "alak": "ὑποκάτω", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000017_000443"], "alak": "τῆς", "nyelv": "grc", "extra": false}] | {"szo_ids": ["word_000017_000442", "word_000017_000443"], "alak": "ὑποκάτω", "nyelv": "grc", "extra": false} |
| 28 | wrovovos | {"szo_ids": ["word_000028_000229"], "alak": "ὑπομονῆς", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000028_000229"], "alak": "πλούσιος", "nyelv": "grc", "extra": false} |
| 28 | erepov | {"szo_ids": ["word_000028_000011"], "alak": "ἐρέπου", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000028_000011"], "alak": "ἕτερον", "nyelv": "grc", "extra": false} |
| 28 | hryatra | {"szo_ids": ["word_000028_000155"], "alak": "ὑπὸ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000028_000155"], "alak": "ἠγάπα", "nyelv": "grc", "extra": false} |
| 28 | épider | {"szo_ids": ["word_000028_000163"], "alak": "ἐπίδερ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000028_000163"], "alak": "ἐφίλει", "nyelv": "grc", "extra": false} |
| 82 | rd dewdés kal | {"szo_ids": ["word_000082_000409", "word_000082_000410", "word_000082_000411"], "alak": "τὸ ἀειδὲς καὶ ἄορατον", "nyelv": "grc", "extra": false} | [{"szo_ids": ["word_000082_000409"], "alak": "τὸ", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000082_000410"], "alak": "ἀειδὲς", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000082_000411"], "alak": "καὶ", "nyelv": "grc", "extra": false}] |
| 124 | Katdpa | {"szo_ids": ["word_000124_000127"], "alak": "Καταρᾶ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000124_000127"], "alak": "κατάρα", "nyelv": "grc", "extra": false} |
| 124 | Kardpa | {"szo_ids": ["word_000124_000169"], "alak": "καταρᾶ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000124_000169"], "alak": "κατάρα", "nyelv": "grc", "extra": false} |
| 124 | WW, | {"szo_ids": ["word_000124_000424"], "alak": "WW", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000124_000424"], "alak": "אָרַר", "nyelv": "heb", "extra": false} |
| 124 | Katriyappa | {"szo_ids": ["word_000124_000267"], "alak": "κατήχαρμα", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000124_000267"], "alak": "κἀπίχαρμα", "nyelv": "grc", "extra": false} |
| 209 | Tovs | {"szo_ids": ["word_000209_000117"], "alak": "αὐτόν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000117"], "alak": "τοὺς", "nyelv": "grc", "extra": false} |
| 209 | adjOea | {"szo_ids": ["word_000209_000272"], "alak": "ἁλήθεια", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000272"], "alak": "ἀλήθεια", "nyelv": "grc", "extra": false} |
| 209 | Toté), | {"szo_ids": ["word_000209_000100"], "alak": "τὸ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000100"], "alak": "ποτέ", "nyelv": "grc", "extra": false} |
| 252 | Tov | {"szo_ids": ["word_000252_000145"], "alak": "ἐξουσίαν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000252_000145"], "alak": "τῶν", "nyelv": "grc", "extra": false} |
| 252 | adpy7 | {"szo_ids": ["word_000252_000169"], "alak": "ἐξουσίαν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000252_000169"], "alak": "ἀρχή", "nyelv": "grc", "extra": false} |
| 300 | ayabn | {"szo_ids": ["word_000300_000543"], "alak": "ἄγαθη", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000300_000543"], "alak": "ἀγαθή", "nyelv": "grc", "extra": false} |
| 350 | ’"Emixanréa, | {"szo_ids": ["word_000350_000462"], "alak": "Ἐπικαλεῖα", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000350_000462"], "alak": "Ἐπικαλέω,", "nyelv": "grc", "extra": false} |
| 432 | Maryn», an | [{"szo_ids": ["word_000432_000482"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000432_000483"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": true}] | {"szo_ids": ["word_000432_000482", "word_000432_000483"], "alak": "Μάτην", "nyelv": "grc", "extra": false} |
| 432 | tpav, | {"szo_ids": ["word_000432_000575"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000575"], "alak": "ὑμῶν", "nyelv": "grc", "extra": false} |
| 432 | epi | {"szo_ids": ["word_000432_000012"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000012"], "alak": "περί", "nyelv": "grc", "extra": false} |
| 432 | waprupetras for | [{"szo_ids": ["word_000432_000435"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000432_000436"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": true}] | {"szo_ids": ["word_000432_000435", "word_000432_000436"], "alak": "μαρτυρεῖται", "nyelv": "grc", "extra": false} |
| 432 | ws. | {"szo_ids": ["word_000432_000011"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000011"], "alak": "μ", "nyelv": "grc", "extra": false} |
| 432 | "Emtpaptupéa, | {"szo_ids": ["word_000432_000444"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000444"], "alak": "Ἐπιμαρτυρέω", "nyelv": "grc", "extra": false} |
| 432 | paptupyon | {"szo_ids": ["word_000432_000151"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000151"], "alak": "μαρτυρήσῃ", "nyelv": "grc", "extra": false} |
| 506 | oxn | {"szo_ids": ["word_000506_000183"], "alak": "יָכֵן", "nyelv": "heb", "extra": false} | {"szo_ids": ["word_000506_000183"], "alak": "לא", "nyelv": "heb", "extra": false} |
| 506 | weusacpevors | {"szo_ids": ["word_000506_000584"], "alak": "μεμιασμένους", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000506_000584"], "alak": "μεμιασμένοις", "nyelv": "grc", "extra": false} |
| 805 | TOS | {"szo_ids": ["word_000805_000078"], "alak": "παλιγγενεσίαν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000078"], "alak": "τοὺς", "nyelv": "grc", "extra": false} |
| 805 | mapadéSotar | {"szo_ids": ["word_000805_000038"], "alak": "πραγμάτων", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000038"], "alak": "παραδέδοται", "nyelv": "grc", "extra": false} |
| 805 | S& | {"szo_ids": ["word_000805_000064"], "alak": "τίνες", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000064"], "alak": "δὲ", "nyelv": "grc", "extra": false} |
| 934 | evocéBeca, | {"szo_ids": ["word_000934_000083"], "alak": "θέλημα", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000934_000083"], "alak": "εὐσέβεια", "nyelv": "grc", "extra": false} |

