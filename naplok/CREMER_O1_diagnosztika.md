# CREMER O1 diagnosztika (O0.5e/5)

A 20 pilot-lap MEGLEVO gyorsitotar- es hibanaplo-adatabol, halozati hivas NELKUL, a jelenlegi validalasi/dontesi szabalyokkal (elemszintu validalas + Qwen-zaj kulon kezelese, D15/D17) ujraertelmezve. `m1` = `qwen/qwen3-vl-32b-instruct`, `m2` = `google/gemini-3.8-flash`.

Teljes dontessel feldolgozott lap: **19 / 20**.
Adathianyos lap (legalabb az egyik modellnek nincs gyorsitotar-talalata, a teljes dontes-eloszlasbol kimaradt): **380**.

## a) dontes-eloszlas, nyelvenkent

| dontes | nyelv | darab |
|---|---|---|
| vitas | grc | 709 |
| hianyzo_m2 | grc | 507 |
| extra_vitas | grc | 407 |
| valtozatlan | nincs | 269 |
| auto | grc | 259 |
| hianyzo_m2 | heb | 64 |
| hianyzo_m1 | grc | 56 |
| extra_vitas | heb | 36 |
| vitas | heb | 25 |
| hianyzo_m2 | lat | 21 |
| hianyzo_m1 | lat | 13 |
| extra_vitas | lat | 7 |
| vitas | lat | 1 |
| **osszesen** | | **2374** |

## b) a `vitas` sorok bontasa

| tipus | darab |
|---|---|
| csak ekezet/hehezet kulonbseg | 66 |
| betukulonbseg | 490 |
| eltero szo_ids | 166 |
| eltero nyelv | 13 |

## c) `elvetett_nem_gyanus` es valodi `ervenytelen` elemek modellenkent

(a hibanaplo OSSZES eddig irt kiserletebol, a 20 pilot-lapra -- adathianyos lapoknal is, mert ott is lehetett mar hibanaplo-bejegyzes egy korabbi kiserletbol)

| modell | elvetett_nem_gyanus | valodi ervenytelen |
|---|---|---|
| qwen/qwen3-vl-32b-instruct | 1680 | 82 |
| google/gemini-3.8-flash | 10 | 99 |

## d) 30 veletlen `vitas` sor (mag: 20260924)

| level | hOCR | m1 | m2 |
|---|---|---|---|
| 17 | els To 1répay THs Oardoons), | {"szo_ids": ["word_000017_000405", "word_000017_000406", "word_000017_000407", "word_000017_000408", "word_000017_000409"], "alak": "ἐις τὸ πέραν τῆς θαλάσσης", "nyelv": "grc", "extra": false} | [{"szo_ids": ["word_000017_000405"], "alak": "εἰς", "nyelv": "grc", "extra": true}, {"szo_ids": ["word_000017_000406"], "alak": "τὸ", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000017_000407"], "alak": "πέραν", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000017_000408"], "alak": "τῆς", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000017_000409"], "alak": "θαλάσσης", "nyelv": "grc", "extra": false}] |
| 28 | Incods; | {"szo_ids": ["word_000028_000157"], "alak": "ἐνκοσμία", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000028_000157"], "alak": "Ἰησοῦς", "nyelv": "grc", "extra": false} |
| 28 | S¢ | {"szo_ids": ["word_000028_000031"], "alak": "ὅτι", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000028_000031"], "alak": "δὲ", "nyelv": "grc", "extra": false} |
| 28 | euionoa | {"szo_ids": ["word_000028_000033"], "alak": "εὐίονος", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000028_000033"], "alak": "ἐμίσησα", "nyelv": "grc", "extra": false} |
| 82 | 4 év koopm tudv | {"szo_ids": ["word_000082_000271", "word_000082_000272", "word_000082_000273", "word_000082_000274"], "alak": "ἐν κόσμῳ ὑμῶν ἀδελφότης", "nyelv": "grc", "extra": false} | [{"szo_ids": ["word_000082_000271"], "alak": "ἡ", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000082_000272"], "alak": "ἐν", "nyelv": "grc", "extra": true}, {"szo_ids": ["word_000082_000273"], "alak": "κόσμῳ", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000082_000274"], "alak": "ὑμῶν", "nyelv": "grc", "extra": true}] |
| 124 | éFepyerar | {"szo_ids": ["word_000124_000010"], "alak": "ἐξεφέραρ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000124_000010"], "alak": "ἐξέρχεται", "nyelv": "grc", "extra": false} |
| 124 | etdoyia | {"szo_ids": ["word_000124_000011"], "alak": "ἐπιδούση", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000124_000011"], "alak": "εὐλογία", "nyelv": "grc", "extra": false} |
| 124 | Katriyappa | {"szo_ids": ["word_000124_000267"], "alak": "κατήχαρμα", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000124_000267"], "alak": "κἀπίχαρμα", "nyelv": "grc", "extra": false} |
| 209 | uynv | {"szo_ids": ["word_000209_000497"], "alak": "ψυχήν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000497"], "alak": "ψυχὴν", "nyelv": "grc", "extra": false} |
| 209 | TpocenticaTw | {"szo_ids": ["word_000209_000082"], "alak": "Προσεκτισάτω", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000082"], "alak": "προσεκτισάτω", "nyelv": "grc", "extra": false} |
| 209 | adixlay | {"szo_ids": ["word_000209_000113"], "alak": "παράπαυ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000113"], "alak": "ἀδικίαν", "nyelv": "grc", "extra": false} |
| 209 | Tuva, | {"szo_ids": ["word_000209_000513"], "alak": "τινὰ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000513"], "alak": "τινά", "nyelv": "grc", "extra": false} |
| 209 | déeny | {"szo_ids": ["word_000209_000071"], "alak": "δέενυ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000071"], "alak": "δίκην", "nyelv": "grc", "extra": false} |
| 300 | Odvaros | {"szo_ids": ["word_000300_000000"], "alak": "Θάνατος", "nyelv": "grc", "extra": true} | {"szo_ids": ["word_000300_000000"], "alak": "Θάνατος", "nyelv": "grc", "extra": false} |
| 300 | év dirla | {"szo_ids": ["word_000300_000539", "word_000300_000540"], "alak": "ἐν φιλίᾳ", "nyelv": "grc", "extra": false} | [{"szo_ids": ["word_000300_000539"], "alak": "ἐν", "nyelv": "grc", "extra": true}, {"szo_ids": ["word_000300_000540"], "alak": "φιλίᾳ", "nyelv": "grc", "extra": false}] |
| 300 | aidvis. | {"szo_ids": ["word_000300_000516"], "alak": "ἀίδιος", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000300_000516"], "alak": "αἰώνιος", "nyelv": "grc", "extra": false} |
| 350 | obca | {"szo_ids": ["word_000350_000185"], "alak": "ἐν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000350_000185"], "alak": "οὖσα", "nyelv": "grc", "extra": false} |
| 432 | peyaptipnrar edvap- | [{"szo_ids": ["word_000432_000339"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000432_000340"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false}] | {"szo_ids": ["word_000432_000339", "word_000432_000340"], "alak": "μεμαρτύρηται", "nyelv": "grc", "extra": false} |
| 432 | waptupet may | {"szo_ids": ["word_000432_000437"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000437", "word_000432_000438"], "alak": "μαρτυρεῖ", "nyelv": "grc", "extra": false} |
| 432 | udtyv in | {"szo_ids": ["word_000432_000492"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000492", "word_000432_000493"], "alak": "μάτην", "nyelv": "grc", "extra": false} |
| 432 | 60 %s | {"szo_ids": ["word_000432_000325"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000325", "word_000432_000326"], "alak": "δι’", "nyelv": "grc", "extra": false} |
| 432 | elvas | {"szo_ids": ["word_000432_000328"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000328"], "alak": "εἶναι", "nyelv": "grc", "extra": false} |
| 432 | mw. | {"szo_ids": ["word_000432_000081"], "alak": "ἐπιμαρτυρῶν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000081"], "alak": "μ", "nyelv": "grc", "extra": false} |
| 506 | Kiptov; | {"szo_ids": ["word_000506_000236"], "alak": "Κύριῳ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000506_000236"], "alak": "κύριον", "nyelv": "grc", "extra": false} |
| 659 | "A peartos, | {"szo_ids": ["word_000659_000431", "word_000659_000432"], "alak": "Ἀπεστός", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000659_000431", "word_000659_000432"], "alak": "Ἀρεστός,", "nyelv": "grc", "extra": false} |
| 805 | KaTarererpeva | {"szo_ids": ["word_000805_000048"], "alak": "ἄγενήτων", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000048"], "alak": "καταλελειμμένα", "nyelv": "grc", "extra": false} |
| 805 | LoTOpia | {"szo_ids": ["word_000805_000159"], "alak": "xvii.", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000159"], "alak": "μὲν", "nyelv": "grc", "extra": false} |
| 805 | oynuats | {"szo_ids": ["word_000805_000032"], "alak": "ἰστορία", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000032"], "alak": "σχήματι", "nyelv": "grc", "extra": false} |
| 934 | emixanéa, | {"szo_ids": ["word_000934_000028"], "alak": "ἐποικοδομέω", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000934_000028"], "alak": "ἐπικαλέω", "nyelv": "grc", "extra": false} |
| 950 | nape, . 4177, | {"szo_ids": ["word_000950_000093", "word_000950_000094", "word_000950_000095"], "alak": "אַנְקִיא", "nyelv": "heb", "extra": true} | [{"szo_ids": ["word_000950_000093"], "alak": "אֱמוּנָה", "nyelv": "heb", "extra": false}, {"szo_ids": ["word_000950_000095"], "alak": "477", "nyelv": "lat", "extra": false}] |

