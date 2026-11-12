# Kódkönyv / Codebook

*Károli 1908 – Strong szóillesztés / Károli 1908 – Strong word alignment*

## `parok/NN_Konyv.tsv`

| oszlop / column | érték / value | leírás | description |
|---|---|---|---|
| `osis` |  | A vers OSIS-azonosítója (könyv.fejezet.vers), a Károli-versszámozás szerint. | OSIS verse identifier (book.chapter.verse), in Károli versification. |
| `token` |  | A magyar szó sorszáma a versben (1-től; az írásjel nem szó). | Position of the Hungarian word in the verse (from 1; punctuation is not a word). |
| `alak_1908` |  | A magyar szó alakja a Károli 1908-as szövegében. | Word form in the 1908 Károli text. |
| `eredeti_token` |  | Az eredeti szó sorszáma a TAHOT/TAGNT versében, a Károli-vers kulcsán (l. MODSZER.md 3.); a héber előtag és rag külön szónak számít. | Position of the source word in the TAHOT/TAGNT verse, keyed to the Károli verse (see METHODS.md 3); Hebrew prefixes and suffixes count as separate words. |
| `strong` |  | Az eredeti szó Strong-száma (H… héber, G… görög) a STEPBible TAHOT/TAGNT szerint; „+” két számot köt össze, ha a forrás egy szóhoz kettőt ad. A modell nem ír Strong-számot: a szám a sorszámból jön. | Strong's number of the source word (H… Hebrew, G… Greek) from STEPBible TAHOT/TAGNT; "+" joins two numbers where the source gives two for one word. The model writes no Strong's number: it comes from the position. |
| `kapcsolat` | `szo` | A pár egy eredeti szóhoz köti a magyar szót. | The pair links the Hungarian word to a source word. |
| `kapcsolat` | `morfema` | A pár egy héber előtag- vagy ragmorfémához köti (H9001–H9049: névelő, kötőszó, elöljáró, személyrag). | The pair links it to a Hebrew prefix or suffix morpheme (H9001–H9049: article, conjunction, preposition, pronominal suffix). |
| `bizonyossag` | `magas` | Két független nyelvi modell ugyanazt a párt adta (Mózes 1–2. könyve). | Two independent language models gave the same pair (Genesis and Exodus). |
| `bizonyossag` | `alacsony` | Egy nyelvi modell javaslata, vagy a két modell eltért; a pontosságát a mérés adja meg (meres.tsv). | Proposal of one language model, or the two models differed; its accuracy is given by the measurement (meres.tsv). |
| `allapot` | `javaslat` | Gépi párosítási javaslat, mért pontossággal; nem kézzel ellenőrzött pár. | Machine alignment proposal with measured accuracy; not a manually verified pair. |
| `nem_tr` | `igen` | Az eredeti görög szó nem szerepel a Textus Receptusban, amelyet Károli fordított; a Strong-szám a kritikai szöveg alakjáé (l. ISMERT_HIBAK.md). | The Greek source word is not in the Textus Receptus, which Károli translated; the Strong number is that of the critical-text form (see KNOWN_ISSUES.md). |

## `szavak/NN_Konyv.tsv`

| oszlop / column | érték / value | leírás | description |
|---|---|---|---|
| `osis` |  | A vers OSIS-azonosítója, a Károli-versszámozás szerint. | OSIS verse identifier, in Károli versification. |
| `oldal` | `hu` | Magyar szó (Károli 1908). | Hungarian word (Károli 1908). |
| `oldal` | `er` | Eredeti szó (héber vagy görög, TAHOT/TAGNT); az alakja nincs a csomagban, a sorszáma és a Strong-száma azonosítja. | Source word (Hebrew or Greek, TAHOT/TAGNT); its form is not in the package, it is identified by its position and Strong number. |
| `token` |  | A szó sorszáma a versben, az oldalán belül (1-től). Minden magyar és minden eredeti szó pontosan egy sorban áll. | Position of the word in the verse, on its side (from 1). Every Hungarian and every source word appears in exactly one row. |
| `alak_1908` |  | A magyar szó alakja; az eredeti szónál üres. | Form of the Hungarian word; empty for a source word. |
| `allapot` | `parositva` | A szónak van párja a másik oldalon (l. partner_token). | The word has a pair on the other side (see partner_token). |
| `allapot` | `betoldas` | Magyar szó eredeti megfelelő nélkül: a fordító betoldása, önálló névelő, segédige, kitett alanyi névmás. | Hungarian word without a source counterpart: translator's addition, article, auxiliary, explicit subject pronoun. |
| `allapot` | `forditatlan` | Eredeti szó magyar megfelelő nélkül (pl. a héber tárgyjelölő, a névelő, ha a magyar nem fordítja). | Source word without a Hungarian counterpart (e.g. the Hebrew object marker, an article the Hungarian does not render). |
| `allapot` | `fuggoben` | A vers párosítása kézi döntésre vár (a versek megfeleltetése szavanként nem állt össze, vagy a válasz nem ment át a gépi kapun); pár nincs. | The verse awaits a manual alignment decision (the verse mapping did not hold word by word, or the answer did not pass the machine gate); no pair. |
| `partner_token` |  | A pár(ok) sorszáma a másik oldalon, vesszővel elválasztva. | Position(s) of the pair(s) on the other side, comma-separated. |
| `strong` |  | Eredeti szónál a saját Strong-száma; magyar szónál a partnerei Strong-számai „+”-szal fűzve. | For a source word its own Strong number; for a Hungarian word the Strong numbers of its partners joined by "+". |
| `bizonyossag` | `magas` | A két modell ugyanazt a partnerhalmazt (vagy ugyanazt a betoldás/fordítatlan döntést) adta a szóra. | The two models gave the same partner set (or the same addition / untranslated decision) for the word. |
| `bizonyossag` | `alacsony` | Egy modell döntése, vagy a két modell eltért. | Decision of one model, or the two models differed. |

## `versek.tsv`

| oszlop / column | érték / value | leírás | description |
|---|---|---|---|
| `osis` |  | A vers OSIS-azonosítója, a Károli-versszámozás szerint. | OSIS verse identifier, in Károli versification. |
| `szoveg_1908` |  | A vers Károli 1908 szövege, írásjelekkel; a szavak sorszáma ebből számolódik. | The 1908 Károli text of the verse, with punctuation; word positions are counted on it. |

## `meres.tsv`

| oszlop / column | érték / value | leírás | description |
|---|---|---|---|
| `szakasz` | `reteg` | Rétegenkénti egyezés a vak ellenőrrel: rétegenként egyszerű véletlen minta. | Agreement with the blind reviewer per stratum: a simple random sample per stratum. |
| `szakasz` | `sulyozott` | A rétegek pársúlyával súlyozott becslés (ÓSZ, ÚSZ, összes). | Estimate weighted by the pair share of the strata (OT, NT, all). |
| `szakasz` | `bontas` | Kapcsolattípus szerinti bontás (tartalmi szó, morféma), leíró. | Breakdown by link type (content word, morpheme), descriptive. |
| `szakasz` | `hibatipus` | A vak ellenőrtől eltérő párok típus szerint (`<réteg>:<típus>`; n = az eltérések száma a rétegben). | Pairs differing from the blind reviewer, by type (`<stratum>:<type>`; n = number of differences in the stratum). |
| `szakasz` | `leiro` | Leíró szám, nem a pontosság része (hianyzo_par: ahol a vak ellenőr több eredeti szót jelölt). | Descriptive count, not part of the accuracy (hianyzo_par: where the blind reviewer marked more source words). |
| `szakasz` | `kalibracio` | A vak ellenőr és a gépi pár egyezése egy korábbi, kézzel összeállított mintával. | Agreement of the blind reviewer and of the machine pair with an earlier manually compiled sample. |
| `szakasz` | `kulso` | Összevetés egy független, Strong-számos Károli-kiadással, a fő szavak párjain (`_haromutas`: az eltérések háromutas ítélete után). | Comparison with an independent Károli edition carrying Strong numbers, on main-word pairs (`_haromutas`: after the three-way judgement of the differences). |
| `cimke` |  | A sor tárgya: réteg (OSZ_mozes_magas, OSZ_mozes_alacsony, OSZ_tortenet, OSZ_koltoi, OSZ_profeta, USZ_evangelium, USZ_level, USZ_jelenesek), csoport vagy hibatípus (folos_par, szomszedos_token, rossz_szo_a_versben, azonos_lexema_mas_elofordulas). | Subject of the row: stratum (OSZ_mozes_magas, OSZ_mozes_alacsony, OSZ_tortenet, OSZ_koltoi, OSZ_profeta, USZ_evangelium, USZ_level, USZ_jelenesek), group or error type (folos_par = superfluous pair, szomszedos_token = neighbouring word, rossz_szo_a_versben = wrong word in the verse, azonos_lexema_mas_elofordulas = same lexeme, other occurrence). |
| `n` |  | A mért párok száma. | Number of pairs measured. |
| `x` |  | Az egyező (helyes) párok száma; hibatípusnál az adott típusú eltérések száma. | Number of agreeing (correct) pairs; for an error type, the number of differences of that type. |
| `p` |  | Arány (x / n, súlyozott soroknál a súlyozott becslés). | Proportion (x / n; for weighted rows the weighted estimate). |
| `also95` |  | A 95%-os konfidencia-intervallum alsó széle. | Lower bound of the 95% confidence interval. |
| `felso95` |  | A 95%-os konfidencia-intervallum felső széle. | Upper bound of the 95% confidence interval. |
| `modszer` | `wilson95` | Wilson-intervallum. | Wilson interval. |
| `modszer` | `retegzett_normal95` | Rétegzett becslés, normál közelítésű intervallum. | Stratified estimate, normal-approximation interval. |
| `modszer` | `retegzett_leiro` | Rétegzett (a réteg teljes súlyával), leíró. | Stratified (with the full weight of the stratum), descriptive. |
| `modszer` | `darab` | Darabszám, intervallum nélkül. | Count, without interval. |
