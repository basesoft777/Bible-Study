# CREMER O1 próbafutás (O0.5f/6)

Két párosítás öt lapra (17, 124, 209, 432, 805), plafon 0,50 USD futásonként: **(i)** `openai/gpt-5-mini` + `google/gemini-3.8-flash`, **(ii)** `openai/gpt-5-mini` + `google/gemini-3.1-flash-lite`. A `gpt-5-mini` válaszai (ii)-nél a gyorsítótárból jöttek (nincs plusz költség az (i)-hez képest).

## Páros (i): GPT-5 Mini + Gemini 3.8 Flash

### Döntéseloszlás

| dontes | darab | arany |
|---|---|---|
| vitas | 557 | 66.5% |
| extra_vitas | 173 | 20.6% |
| hianyzo_m1 | 51 | 6.1% |
| hianyzo_m2 | 24 | 2.9% |
| auto | 22 | 2.6% |
| valtozatlan | 11 | 1.3% |
| **osszesen** | **838** | |

### `vitas` bontás

| tipus | darab |
|---|---|
| csak ekezet/hehezet kulonbseg | 10 |
| csak kis-/nagybetu kulonbseg | 1 |
| betukulonbseg | 276 |
| eltero szo_ids | 67 |
| eltero nyelv | 203 |

### Laponkénti átlag token és USD, vetítés 967 lapra

| modell | lapok | atlag be/lap | atlag ki/lap | atlag gondolkodas/lap | atlag USD/lap | vetites (967 lap) |
|---|---|---|---|---|---|---|
| openai/gpt-5-mini | 5 | 12600 | 2532 | 0 | 0.00602 | 5.82 USD |
| google/gemini-3.8-flash | 5 | 12460 | 4136 | 0 | 0.02486 | 24.03 USD |
| **együtt** | | | | | 0.03088 | **29.86 USD** |

### 20 véletlen `vitas` sor (mag: 20260924)

| level | hOCR | m1 | m2 |
|---|---|---|---|
| 124 | dpruos, | {"szo_ids": ["word_000124_000497"], "alak": "dpruos,", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000124_000497"], "alak": "ἄρτιος", "nyelv": "grc", "extra": false} |
| 124 | Xpiords | {"szo_ids": ["word_000124_000165"], "alak": "Χριστός", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000124_000165"], "alak": "Χριστὸς", "nyelv": "grc", "extra": false} |
| 17 | d8uccov | {"szo_ids": ["word_000017_000213"], "alak": "ἀβυσσος", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000017_000213"], "alak": "ἄβυσσον", "nyelv": "grc", "extra": false} |
| 17 | dvaBaivew | {"szo_ids": ["word_000017_000534"], "alak": "dvaBaivew", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000017_000534"], "alak": "ἀναβαίνειν", "nyelv": "grc", "extra": false} |
| 17 | €« tis | {"szo_ids": ["word_000017_000535"], "alak": "€«", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000017_000535", "word_000017_000536"], "alak": "ἐκ", "nyelv": "grc", "extra": false} |
| 17 | Xpiotov | {"szo_ids": ["word_000017_000353"], "alak": "Xpiotov", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000017_000353"], "alak": "Χριστὸν", "nyelv": "grc", "extra": false} |
| 209 | Sikacov | {"szo_ids": ["word_000209_000563"], "alak": "Sikacov", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000563"], "alak": "δίκαιον", "nyelv": "grc", "extra": false} |
| 209 | wxav, | {"szo_ids": ["word_000209_000291"], "alak": "wxav", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000209_000291"], "alak": "ἔδωκαν", "nyelv": "grc", "extra": false} |
| 209 | Kapdiav | {"szo_ids": ["word_000209_000486"], "alak": "Kapdiav", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000486"], "alak": "καρδίαν", "nyelv": "grc", "extra": false} |
| 209 | dicaiws | {"szo_ids": ["word_000209_000188"], "alak": "dicaiws", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000209_000188"], "alak": "δικαίως", "nyelv": "grc", "extra": false} |
| 209 | edccalwoen | {"szo_ids": ["word_000209_000495"], "alak": "edccalwoen", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000209_000495"], "alak": "ἐδικαίωσεν", "nyelv": "grc", "extra": false} |
| 432 | pyous Karots | [{"szo_ids": ["word_000432_000289"], "alak": "pyous", "nyelv": "grc", "extra": false}, {"szo_ids": ["word_000432_000290"], "alak": "Karots", "nyelv": "grc", "extra": false}] | {"szo_ids": ["word_000432_000289", "word_000432_000290"], "alak": "ἔργοις", "nyelv": "grc", "extra": false} |
| 432 | waptup® | {"szo_ids": ["word_000432_000168"], "alak": "waptup®", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000168"], "alak": "μαρτυρῶ", "nyelv": "grc", "extra": false} |
| 432 | iv Kai | {"szo_ids": ["word_000432_000219"], "alak": "iv", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000432_000219", "word_000432_000220"], "alak": "ἣν", "nyelv": "grc", "extra": false} |
| 432 | émawweicOar | {"szo_ids": ["word_000432_000293"], "alak": "émawweicOar", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000432_000293"], "alak": "ἐπαινεῖσθαι", "nyelv": "grc", "extra": false} |
| 805 | piOos, | {"szo_ids": ["word_000805_000014"], "alak": "πλάσμα", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000014"], "alak": "μῦθος", "nyelv": "grc", "extra": false} |
| 805 | eiow | {"szo_ids": ["word_000805_000054"], "alak": "μέν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000054"], "alak": "εἰσιν", "nyelv": "grc", "extra": false} |
| 805 | ypavol | {"szo_ids": ["word_000805_000474"], "alak": "ὑπαρχόν", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000474"], "alak": "βέβηλοι", "nyelv": "grc", "extra": false} |
| 805 | Té | {"szo_ids": ["word_000805_000053"], "alak": "τὸ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000053"], "alak": "τέ", "nyelv": "grc", "extra": false} |
| 805 | Tors | {"szo_ids": ["word_000805_000476"], "alak": "τοῖς", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000476"], "alak": "γραώδεις", "nyelv": "grc", "extra": false} |

## Páros (ii): GPT-5 Mini + Gemini 3.1 Flash Lite

### Döntéseloszlás

| dontes | darab | arany |
|---|---|---|
| vitas | 436 | 62.9% |
| hiba | 146 | 21.1% |
| auto | 43 | 6.2% |
| hianyzo_m1 | 27 | 3.9% |
| hianyzo_m2 | 27 | 3.9% |
| extra_vitas | 7 | 1.0% |
| valtozatlan | 7 | 1.0% |
| **osszesen** | **693** | |

### `vitas` bontás

| tipus | darab |
|---|---|
| csak ekezet/hehezet kulonbseg | 17 |
| csak kis-/nagybetu kulonbseg | 3 |
| betukulonbseg | 226 |
| eltero szo_ids | 3 |
| eltero nyelv | 187 |

### Laponkénti átlag token és USD, vetítés 967 lapra

| modell | lapok | atlag be/lap | atlag ki/lap | atlag gondolkodas/lap | atlag USD/lap | vetites (967 lap) |
|---|---|---|---|---|---|---|
| openai/gpt-5-mini | 5 | 12600 | 2532 | 0 | 0.00602 | 5.82 USD |
| google/gemini-3.1-flash-lite | 5 | 15394 | 12287 | 7843 | 0.02128 | 20.57 USD |
| **együtt** | | | | | 0.02730 | **26.40 USD** |

### 20 véletlen `vitas` sor (mag: 20260924)

| level | hOCR | m1 | m2 |
|---|---|---|---|
| 124 | Kpeuapevos | {"szo_ids": ["word_000124_000419"], "alak": "Κρεuαρενος", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000124_000419"], "alak": "κρεμάμενος", "nyelv": "grc", "extra": false} |
| 17 | x.7.d.); | {"szo_ids": ["word_000017_000058"], "alak": "x.7.d.);", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000017_000058"], "alak": "κ.τ.λ.", "nyelv": "grc", "extra": false} |
| 17 | THs | {"szo_ids": ["word_000017_000575"], "alak": "THs", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000017_000575"], "alak": "τῆς", "nyelv": "grc", "extra": false} |
| 17 | wnyav. | {"szo_ids": ["word_000017_000338"], "alak": "wnyav.", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000017_000338"], "alak": "πηγῶν", "nyelv": "grc", "extra": false} |
| 209 | 4 | {"szo_ids": ["word_000209_000461"], "alak": "4", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000209_000461"], "alak": "ἡ", "nyelv": "grc", "extra": false} |
| 209 | tHv | {"szo_ids": ["word_000209_000496"], "alak": "tHv", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000496"], "alak": "τὴν", "nyelv": "grc", "extra": false} |
| 209 | dccasody | {"szo_ids": ["word_000209_000511"], "alak": "dccasody", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000209_000511"], "alak": "δικαιοῦν", "nyelv": "grc", "extra": false} |
| 209 | adTovs | {"szo_ids": ["word_000209_000176"], "alak": "adTovs", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000209_000176"], "alak": "αὐτοὺς", "nyelv": "grc", "extra": false} |
| 209 | Bvexa | {"szo_ids": ["word_000209_000106"], "alak": "Bvexa", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000209_000106"], "alak": "ἕνεκα", "nyelv": "grc", "extra": false} |
| 209 | TupavviKds | {"szo_ids": ["word_000209_000193"], "alak": "TupavviKds", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000209_000193"], "alak": "τυραννικῶς", "nyelv": "grc", "extra": false} |
| 805 | vpiv | {"szo_ids": ["word_000805_000383"], "alak": "ὑπό", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000383"], "alak": "ὑμῖν", "nyelv": "grc", "extra": false} |
| 805 | Té | {"szo_ids": ["word_000805_000053"], "alak": "τὸ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000053"], "alak": "τέ", "nyelv": "grc", "extra": false} |
| 805 | GAN | {"szo_ids": ["word_000805_000015"], "alak": "μῦθος", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000015"], "alak": "ἀλλ'", "nyelv": "grc", "extra": false} |
| 805 | péev | {"szo_ids": ["word_000805_000147"], "alak": "μύθος", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000147"], "alak": "μέν", "nyelv": "grc", "extra": false} |
| 805 | avnyydvos | {"szo_ids": ["word_000805_000296"], "alak": "ἀννήγμενος", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000296"], "alak": "ἀνηγμένος", "nyelv": "grc", "extra": false} |
| 805 | oth | {"szo_ids": ["word_000805_000162"], "alak": "oth", "nyelv": "lat", "extra": false} | {"szo_ids": ["word_000805_000162"], "alak": "ἐστι", "nyelv": "grc", "extra": false} |
| 805 | eEaxorovOncarvtes | {"szo_ids": ["word_000805_000381"], "alak": "ἐξαχρονισμένοι", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000381"], "alak": "ἐξακολουθήσαντες", "nyelv": "grc", "extra": false} |
| 805 | tais | {"szo_ids": ["word_000805_000475"], "alak": "ταῑς", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000475"], "alak": "ταῖς", "nyelv": "grc", "extra": false} |
| 805 | doypati«y | {"szo_ids": ["word_000805_000212"], "alak": "δογματική", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000212"], "alak": "δογματικὴ", "nyelv": "grc", "extra": false} |
| 805 | oxpate | {"szo_ids": ["word_000805_000047"], "alak": "μυθικὴ", "nyelv": "grc", "extra": false} | {"szo_ids": ["word_000805_000047"], "alak": "σχήματι", "nyelv": "grc", "extra": false} |

