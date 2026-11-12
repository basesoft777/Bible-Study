# Kódkönyv / Codebook

<!-- GENERÁLT: a Logosz-lexikon nyílt adatmagjának exportja, a projekt adataiból generálva; kézzel nem szerkesztendő. -->

Minden oszlop, érték és kód leírása magyarul és angolul. / Description of every column, value and code, in Hungarian and English.

**Adatréteg / data layer.** A nyílt adatmag a lexikon adatrétege: motívumok, előfordulások, kizárások. Maga a lexikon (értelmező szövege, a szótárak magyar fordítása és a kötet) önálló mű, minden jog fenntartva. / The open data core is the data layer of the lexicon; the lexicon itself (its interpretive text, the Hungarian translation of the dictionaries, and the printed volume) is a separate work, all rights reserved.


## (nem exportált mezők)

- `elofordulasok.tsv / funkcio (magyarázó rész)` = `a lexikon része` (en: `part of the lexicon`): A funkció-címke utáni magyarázó mondat. Értelmező szöveg vagy a szótárak magyar fordítása: a lexikon része (önálló mű, minden jog fenntartva), nem része a nyílt adatmagnak. / The explanatory sentence after the function label. Interpretive text or the Hungarian translation of the dictionaries: part of the lexicon (a separate work, all rights reserved), not part of the open data core.
- `elofordulasok.tsv / jelentes_hu` = `a lexikon része` (en: `part of the lexicon`): A szótári jelentés magyar fordítása. Értelmező szöveg vagy a szótárak magyar fordítása: a lexikon része (önálló mű, minden jog fenntartva), nem része a nyílt adatmagnak. / The Hungarian translation of the dictionary meaning. Interpretive text or the Hungarian translation of the dictionaries: part of the lexicon (a separate work, all rights reserved), not part of the open data core.
- `elofordulasok.tsv / kapcsolodas` = `a lexikon része` (en: `part of the lexicon`): A vers kapcsolódásának szabad prózai magyarázata. Értelmező szöveg vagy a szótárak magyar fordítása: a lexikon része (önálló mű, minden jog fenntartva), nem része a nyílt adatmagnak. / Free-prose explanation of how the verse connects to the motif. Interpretive text or the Hungarian translation of the dictionaries: part of the lexicon (a separate work, all rights reserved), not part of the open data core.
- `kapcsolatok.tsv / funkcio` = `a lexikon része` (en: `part of the lexicon`): A kapcsolat szerepének prózai leírása. Értelmező szöveg vagy a szótárak magyar fordítása: a lexikon része (önálló mű, minden jog fenntartva), nem része a nyílt adatmagnak. / Prose description of the link’s role. Interpretive text or the Hungarian translation of the dictionaries: part of the lexicon (a separate work, all rights reserved), not part of the open data core.
- `kapcsolatok.tsv / indoklas` = `a lexikon része` (en: `part of the lexicon`): A kapcsolat szerepének és bizonyosságának prózai indoklása. Értelmező szöveg vagy a szótárak magyar fordítása: a lexikon része (önálló mű, minden jog fenntartva), nem része a nyílt adatmagnak. / Prose rationale of the link’s role and certainty. Interpretive text or the Hungarian translation of the dictionaries: part of the lexicon (a separate work, all rights reserved), not part of the open data core.
- `motivum_kapcsolatok.tsv / funkcio` = `a lexikon része` (en: `part of the lexicon`): A motívumközi kapcsolat szerepének prózai leírása. Értelmező szöveg vagy a szótárak magyar fordítása: a lexikon része (önálló mű, minden jog fenntartva), nem része a nyílt adatmagnak. / Prose description of the motif-to-motif link’s role. Interpretive text or the Hungarian translation of the dictionaries: part of the lexicon (a separate work, all rights reserved), not part of the open data core.
- `motivum_kapcsolatok.tsv / indoklas` = `a lexikon része` (en: `part of the lexicon`): A motívumközi kapcsolat prózai indoklása a mért adatokkal. Értelmező szöveg vagy a szótárak magyar fordítása: a lexikon része (önálló mű, minden jog fenntartva), nem része a nyílt adatmagnak. / Prose rationale of the motif-to-motif link with measured data. Interpretive text or the Hungarian translation of the dictionaries: part of the lexicon (a separate work, all rights reserved), not part of the open data core.

### `szabály`

A csomagba csak az adatréteg kerül: azonosító, cím, kizáró jegy, igehely, szóbázis, besorolás-címke, kizárás és döntés indoklással, proveniencia. A kizárások és beépítések indoklása és a kizáró jegy adat (a döntés tartalmát mondja ki), ezért bent van.

*Only the data layer is included: identifier, title, exclusion criterion, passage, lexical base, classification label, exclusions and decisions with rationale, provenance. The rationale of exclusions/incorporations and the exclusion criterion are data (they state the content of a decision) and are therefore included.*


## beepitesi_dontesek.tsv


### `cel_igehely`

Motívumközi jelöltnél a másik motívum oldali igehely(ek); egyébként üres.

*For a link between motifs, the passage(s) on the other motif’s side; otherwise empty.*


### `cel_igehely_osis`

Az előző oszlop (cel_igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (cel_igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `cel_motivum`

Motívumközi jelöltnél a másik motívum azonosítója; egyébként üres.

*For a link between motifs, the other motif’s identifier; otherwise empty.*


### `datum`

A döntés napja (ÉÉÉÉ.HH.NN).

*The date of the decision (YYYY.MM.DD).*


### `dontesek`

A döntés nyilvános azonosítói (NYD-nnn), a dontesnaplo.tsv-ben oldhatók fel; `;`-vel elválasztva.

*Public identifiers (NYD-nnn) of the decisions, resolvable in dontesnaplo.tsv; separated by `;`.*


### `forditas_modja`

A sor angol párhuzamos mezőinek (`…_en`, szabad szöveg) készítési módja: `gépi fordítás (<modell>)` — a ténylegesen futott modell neve; `…; részben hiányzik` — a sor egyik szabad szöveges mezőjének nincs érvényes fordítása; `nincs fordítás` — egyiknek sincs; üres — a sorban nincs szabad szöveg. A zárt értékek `_en` címkéje nem gépi fordítás, hanem a kódkönyv szerkesztett címkéje.

*How the row’s English parallel fields (`…_en`, free text) were made: `gépi fordítás (<model>)` = machine translation by the model actually run; `…; részben hiányzik` = one free-text field of the row has no valid translation; `nincs fordítás` = none has; empty = the row has no free text. The `_en` labels of closed-vocabulary values are not machine translations but edited codebook labels.*


### `igehely`

A beépített igehely, Károli-számozással; az elofordulasok.tsv sorának kulcsa.

*The incorporated passage, in Károli numbering; the key of the row in elofordulasok.tsv.*


### `igehely_osis`

Az előző oszlop (igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `indoklas`

A beépítés szerkesztői indoklása.

*The editorial rationale for incorporation.*


### `indoklas_en`

Az előző oszlop (indoklas) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (indoklas): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `jelolt_tipus`

Mit vizsgáltunk: egy motívum lehetséges előfordulását vagy két motívum közti kapcsolatot.

*What was examined: a candidate occurrence of a motif, or a link between two motifs.*

- `jelolt_tipus` = `elofordulas` (en: `occurrence`): a motívum lehetséges előfordulása / a candidate occurrence of the motif
- `jelolt_tipus` = `motivumkozi` (en: `between motifs`): lehetséges kapcsolat két motívum között / a candidate link between two motifs

### `jelolt_tipus_en`

Az előző oszlop (jelolt_tipus) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (jelolt_tipus), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `keresesi_mod`

Hogyan jutottunk a jelölthöz.

*How the candidate was found.*

- `keresesi_mod` = `Károli-kereszthivatkozás` (en: `Károli cross-reference`): a Károli-kiadás kereszthivatkozásai (az ismert hibákat l. ISMERT_HIBAK.md) / the cross-references of the Károli edition (for known errors see ISMERT_HIBAK.md)
- `keresesi_mod` = `TSK-kereszthivatkozás` (en: `TSK cross-reference`): a Treasury of Scripture Knowledge kereszthivatkozásai / the cross-references of the Treasury of Scripture Knowledge
- `keresesi_mod` = `kollokáció (két szó egy versben)` (en: `collocation (two words in one verse)`): két szó együttes előfordulása egy versben / co-occurrence of two words in one verse
- `keresesi_mod` = `motívumközi kapcsolat vizsgálata` (en: `examination of a link between motifs`): két motívum közti kapcsolat vizsgálata / examination of a link between two motifs
- `keresesi_mod` = `rokon szavak (szócsalád) keresése` (en: `search for related words (word family)`): egy szócsalád rokon szavainak keresése / a search for related words of one word family
- `keresesi_mod` = `szerkesztői teljességi felmérés` (en: `editorial completeness survey`): a motívum teljességét ellenőrző szerkesztői felmérés / an editorial survey checking the completeness of the motif
- `keresesi_mod` = `szerkesztői vizsgálat (a keresés módja külön nincs rögzítve)` (en: `editorial examination (search method not recorded separately)`): szerkesztői vizsgálat; a keresés módját nem rögzítettük külön / an editorial examination; the search method was not recorded separately
- `keresesi_mod` = `szó-szintű visszakeresés a héber/görög szövegben` (en: `word-level look-up in the Hebrew/Greek text`): szó szerinti visszakeresés a héber vagy görög szövegben / word-level look-up in the Hebrew or Greek text
- `keresesi_mod` = `szóbázis (Strong-szám) szerinti teljes szövegkeresés` (en: `full-text search by lexical base (Strong's number)`): a Strong-szám szerinti keresés a teljes szövegben / a search by Strong number across the whole text
- `keresesi_mod` = `szótári (BDB) szócikk alapján` (en: `from the dictionary (BDB) entry`): a BDB szótári szócikke alapján talált hely / a passage found through the BDB dictionary entry
- `keresesi_mod` = `többforrásos ellenőrzés` (en: `multi-source check`): több forrás összevetésével végzett ellenőrzés / a check carried out by comparing several sources

### `keresesi_mod_en`

Az előző oszlop (keresesi_mod) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (keresesi_mod), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `korabbi_minosites`

A jelölt korábbi minősítése és annak indoklása, ha volt; egyébként üres.

*The candidate’s earlier assessment and its rationale, if any; otherwise empty.*


### `korabbi_minosites_en`

Az előző oszlop (korabbi_minosites) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (korabbi_minosites): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `motivum_azonosito`

A motívum, amelybe a helyet beépítettük (l. motivumok.tsv).

*The motif into which the passage was incorporated (see motivumok.tsv).*


## cc_by_sa_reteg/szemantikai_domenek.tsv


### `domen_kod`

A szemantikai domén kódja a forrásszótár szerint.

*The code of the semantic domain according to the source dictionary.*


### `domen_neve`

A szemantikai domén neve angolul, a forrásszótár szerint.

*The name of the semantic domain in English, according to the source dictionary.*


### `glossza`

A jelentés rövid angol glosszája a forrásszótárból.

*The short English gloss of the meaning from the source dictionary.*


### `jelentes_azonosito`

A jelentés azonosítója a forrásszótárban.

*The identifier of the meaning in the source dictionary.*


### `lemma`

A szótári alak (héber vagy görög).

*The dictionary form (Hebrew or Greek).*


### `strong`

A szóbázis Strong-száma (H = héber, G = görög).

*The Strong number of the lexical base (H = Hebrew, G = Greek).*


### `szotar`

A domén-adat forrása.

*The source of the domain data.*

- `szotar` = `SDBH` (en: `SDBH`): az UBS szemantikai héber szótára (v0.9.2), CC BY-SA 4.0 / UBS Semantic Dictionary of Biblical Hebrew (v0.9.2), CC BY-SA 4.0
- `szotar` = `SDGNT` (en: `SDGNT`): az UBS szemantikai újszövetségi görög szótára (v1.1), CC BY-SA 4.0 / UBS Semantic Dictionary of the Greek New Testament (v1.1), CC BY-SA 4.0

### `szotar_en`

Az előző oszlop (szotar) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (szotar), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


## dontesnaplo.tsv


### `datum`

A döntés napja a szövegből (ÉÉÉÉ-HH-NN), vagy „nincs rögzítve”.

*The date of the decision taken from the text (YYYY-MM-DD), or “nincs rögzítve” (not recorded).*


### `dontes`

A döntés szövege, a belső jelölések nélkül; hosszú szövegnél az elejét közli.

*The text of the decision without internal markers; the opening is given for long texts.*


### `dontes_azonosito`

A döntés nyilvános azonosítója (NYD-nnn); a többi fájl ezzel hivatkozik a döntésre.

*The public decision identifier (NYD-nnn); the other files refer to the decision by it.*


### `dontes_en`

Az előző oszlop (dontes) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (dontes): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `forditas_modja`

A sor angol párhuzamos mezőinek (`…_en`, szabad szöveg) készítési módja: `gépi fordítás (<modell>)` — a ténylegesen futott modell neve; `…; részben hiányzik` — a sor egyik szabad szöveges mezőjének nincs érvényes fordítása; `nincs fordítás` — egyiknek sincs; üres — a sorban nincs szabad szöveg. A zárt értékek `_en` címkéje nem gépi fordítás, hanem a kódkönyv szerkesztett címkéje.

*How the row’s English parallel fields (`…_en`, free text) were made: `gépi fordítás (<model>)` = machine translation by the model actually run; `…; részben hiányzik` = one free-text field of the row has no valid translation; `nincs fordítás` = none has; empty = the row has no free text. The `_en` labels of closed-vocabulary values are not machine translations but edited codebook labels.*


### `kerdes`

A döntés tárgya: a feltett kérdés egy-két mondatban.

*The subject of the decision: the question asked, in a sentence or two.*


### `kerdes_en`

Az előző oszlop (kerdes) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (kerdes): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


## elofordulasok.tsv


### `azonositas_modja`

Hogyan azonosítottuk a Károli-szót a Strong-számmal.

*How the Károli word was matched to the Strong number.*

- `azonositas_modja` = `kikövetkeztetett` (en: `inferred`): a párosítás következtetésből származik, nem közvetlen megfeleltetésből / the match is inferred, not a direct correspondence
- `azonositas_modja` = `szó-szintű-gépi` (en: `word-level, machine`): gépi (modell-kimenet) szópárosítás, csak magas bizonyosságú pár igazolhat sort; nem emberi ellenőrzés / machine (model output) word alignment; only high-confidence pairs can confirm a row; not human verification
- `azonositas_modja` = `tartalom-alapú` (en: `content-based`): a szerkesztő a Károli-szöveget olvasva rendelte a szót a Strong-számhoz / the editor assigned the word to the Strong number by reading the Károli text

### `azonositas_modja_en`

Az előző oszlop (azonositas_modja) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (azonositas_modja), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `datum`

A lekérdezés vagy a döntés napja (ÉÉÉÉ-HH-NN).

*The date of the query or decision (YYYY-MM-DD).*


### `forditas_modja`

A sor angol párhuzamos mezőinek (`…_en`, szabad szöveg) készítési módja: `gépi fordítás (<modell>)` — a ténylegesen futott modell neve; `…; részben hiányzik` — a sor egyik szabad szöveges mezőjének nincs érvényes fordítása; `nincs fordítás` — egyiknek sincs; üres — a sorban nincs szabad szöveg. A zárt értékek `_en` címkéje nem gépi fordítás, hanem a kódkönyv szerkesztett címkéje.

*How the row’s English parallel fields (`…_en`, free text) were made: `gépi fordítás (<model>)` = machine translation by the model actually run; `…; részben hiányzik` = one free-text field of the row has no valid translation; `nincs fordítás` = none has; empty = the row has no free text. The `_en` labels of closed-vocabulary values are not machine translations but edited codebook labels.*


### `forras_dataset`

A forrásként használt, licenccel rendelkező adatkészlet(ek) neve; üres, ha nincs ilyen.

*The name(s) of the licensed dataset(s) used as source; empty when there is none.*


### `forras_licenc`

A forrás-adatkészlet licence.

*The licence of the source dataset.*

- `forras_licenc` = `CC BY 4.0` (en: `CC BY 4.0`): Creative Commons Nevezd meg! 4.0 (a forrást meg kell nevezni) / Creative Commons Attribution 4.0 (the source must be credited)

### `forras_licenc_en`

Az előző oszlop (forras_licenc) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (forras_licenc), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `forras_megnevezes`

A forrás olvasói neve: szerkesztői tanulmány, napló vagy adatkészlet.

*The reader-facing name of the source: editorial essay, log or dataset.*

- `forras_megnevezes` = `TAGNT (CC BY 4.0)` (en: `TAGNT (CC BY 4.0)`): A sor forrásának megnevezése: TAGNT (CC BY 4.0). / Name of the source of the row: TAGNT (CC BY 4.0).
- `forras_megnevezes` = `TAHOT (CC BY 4.0)` (en: `TAHOT (CC BY 4.0)`): A sor forrásának megnevezése: TAHOT (CC BY 4.0). / Name of the source of the row: TAHOT (CC BY 4.0).
- `forras_megnevezes` = `a kézi kereszthivatkozás-napló` (en: `the hand-kept cross-reference log`): A sor forrásának megnevezése: a kézi kereszthivatkozás-napló. / Name of the source of the row: the hand-kept cross-reference log.
- `forras_megnevezes` = `a motívum kézi tematikus tanulmánya` (en: `the hand-written thematic study of the motif`): A sor forrásának megnevezése: a motívum kézi tematikus tanulmánya. / Name of the source of the row: the hand-written thematic study of the motif.
- `forras_megnevezes` = `a projekt saját mérése és naplója` (en: `the project's own measurement and log`): A sor forrásának megnevezése: a projekt saját mérése és naplója. / Name of the source of the row: the project's own measurement and log.
- `forras_megnevezes` = `szerkesztői döntés` (en: `editorial decision`): A sor forrásának megnevezése: szerkesztői döntés. / Name of the source of the row: editorial decision.

### `forras_megnevezes_en`

Az előző oszlop (forras_megnevezes) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (forras_megnevezes), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `funkcio`

A vers szerepének besorolása a motívumban: rövid címke (pl. „alap-előfordulás”, „ismétlődés”). **Adatréteg**, mert a hely motívumbeli szerepét osztályozza; a címkét követő magyarázó mondat értelmező próza, a lexikon része, ezért kimaradt.

*Classification of the verse’s role in the motif: a short label (e.g. “alap-előfordulás” = foundational occurrence). **Data layer**, because it classifies the place’s role in the motif; the explanatory sentence that follows the label is interpretive prose, belongs to the lexicon and is omitted.*


### `funkcio_en`

Az előző oszlop (funkcio) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (funkcio): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `horgony`

A horgony értéke: Strong-szám(ok), szópár vagy a hivatkozott hely.

*The value of the anchor: Strong number(s), word pair or the referenced passage.*


### `horgony_tipus`

Mire támaszkodik a sor: a szóbázis típusa.

*What the row rests on: the type of the lexical anchor.*

- `horgony_tipus` = `formula-kapcsolat` (en: `formula link`): rögzített formula, amely nem egyetlen szón áll / a fixed formula that does not rest on a single word
- `horgony_tipus` = `hivatkozás-kapcsolat` (en: `reference link`): hivatkozás egy másik szövegre (pl. apokrif könyv helye) / a reference to another text (e.g. a passage of an apocryphal book)
- `horgony_tipus` = `idézet-kapcsolat` (en: `quotation link`): idézet vagy idézés egy másik szövegből / a quotation or citation from another text
- `horgony_tipus` = `kollokáció (szópár egy versben)` (en: `collocation (word pair in one verse)`): két szó, amelynek együtt kell állnia a versben / two words that must stand together in the verse
- `horgony_tipus` = `közös szóbázis` (en: `shared lexical base`): két vagy több Strong-szám együtt (pl. H7121 + H8034) / two or more Strong numbers together (e.g. H7121 + H8034)
- `horgony_tipus` = `szóbázis` (en: `lexical base`): egyetlen Strong-szám, az igehely szavának szótári alapja / a single Strong number, the dictionary base of the word in the verse
- `horgony_tipus` = `tematikus kapcsolat` (en: `thematic link`): tematikus kapcsolat egy megnevezett igehellyel, nem lexikai horgony / a thematic link to a named passage, not a lexical anchor

### `horgony_tipus_en`

Az előző oszlop (horgony_tipus) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (horgony_tipus), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `igazolas`

Megerősítette-e a sor Strong-hozzárendelését egy lekérdezés a héber szövegben; ez nem a forrás, hanem az ellenőrzés állapota.

*Whether a query against the Hebrew text confirmed the row’s Strong assignment; the state of verification, not the source.*

- `igazolas` = `TAHOT-hatokoron-kivul` (en: `outside the scope of TAHOT`): a TAHOT héber szövege nem fedi ezt a helyet (például újszövetségi hely) / the TAHOT Hebrew text does not cover this place (for example a New Testament passage)
- `igazolas` = `TAHOT-igazolt` (en: `confirmed in TAHOT`): a Strong-hozzárendelést a TAHOT héber szövegben tételesen visszakerestük / the Strong assignment was looked up item by item in the TAHOT Hebrew text
- `igazolas` = `nincs` (en: `none`): nem történt igazoló lekérdezés / no confirming query was run

### `igazolas_en`

Az előző oszlop (igazolas) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (igazolas), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `igehely`

Az igehely Károli-számozással (pl. 1Móz 3:16); a héber/görög szöveget a vers sora hordozza.

*The passage in Károli numbering (e.g. 1Móz 3:16 = Gen 3:16); the Hebrew/Greek text is carried by the verse row.*


### `igehely_osis`

Az előző oszlop (igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `jelentes_en`

A szótári jelentés angolul: kivonat a sor `szotar` oszlopában megnevezett szótár (BDB, Thayer: közkincs; TBESG: CC BY 4.0) szócikkének szövegéből, a jelentés számával (`jelentes_szam`). Szótári kivonat, nem a STEPBible rövid glosszája; az angol szófogódzót a `strong_glossza_en` adja.

*The dictionary meaning in English: an excerpt from the text of the entry in the dictionary named in the row’s `szotar` column (BDB, Thayer: public domain; TBESG: CC BY 4.0), for the meaning numbered in `jelentes_szam`. A dictionary excerpt, not the short STEPBible gloss; the short English word cue is `strong_glossza_en`.*


### `jelentes_szam`

A szótári jelentés száma vagy tagolása (számozott jelentés, igetörzs-címke vagy „tagolatlan”).

*The dictionary meaning number or division (numbered meaning, verb-stem label or “tagolatlan” = undivided).*


### `karoli_szo`

A szóalak a Károli-fordításban ezen a helyen.

*The word form in the Károli translation at this place.*


### `lekerdezes_tipusa`

A sor forrásának lekérdezés-típusa; kézi döntésnél nincs lekérdezés.

*The query type behind the row’s source; a decision made by hand involves no query.*

- `lekerdezes_tipusa` = `kézi döntés, lekérdezés nélkül` (en: `editorial decision, without a query`): a sor szerkesztői döntésből származik, nem lekérdezés eredménye (értelmezés, nem ténymegállapítás) / the row comes from an editorial decision, not a query result (interpretation, not a stated fact)
- `lekerdezes_tipusa` = `teljes ószövetségi szöveg (TAHOT)` (en: `full Old Testament text (TAHOT)`): a teljes ószövetségi héber szövegen futtatott lekérdezés / a query run over the full Old Testament Hebrew text
- `lekerdezes_tipusa` = `teljes ószövetségi és újszövetségi szöveg (TAHOT + TAGNT)` (en: `full Old and New Testament text (TAHOT + TAGNT)`): a teljes ószövetségi és újszövetségi szövegen futtatott lekérdezés / a query run over the full Old and New Testament text

### `lekerdezes_tipusa_en`

Az előző oszlop (lekerdezes_tipusa) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (lekerdezes_tipusa), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `megbizhatosag`

A Károli-szó azonosításának bizonyossága.

*The confidence of the Károli word identification.*

- `megbizhatosag` = `közepes` (en: `medium`): valószínű, de nem biztos azonosítás / probable but not certain identification
- `megbizhatosag` = `magas` (en: `high`): biztos azonosítás / secure identification

### `megbizhatosag_en`

Az előző oszlop (megbizhatosag) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (megbizhatosag), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `motivum_azonosito`

A motívum azonosítója (l. motivumok.tsv).

*The motif identifier (see motivumok.tsv).*


### `pardes_szint`

A vers PaRDeS-szintje.

*The PaRDeS level of the verse.*

- `pardes_szint` = `Drash` (en: `Drash`): a kifejtés szintje: a hely szerepe a motívum ívében / the level of exposition: the passage’s role in the motif’s arc
- `pardes_szint` = `Drash/Sod` (en: `Drash/Sod`): több szint együtt: a kifejtés szintje: a hely szerepe a motívum ívében; a rejtett, titokzatos jelentés szintje / several levels together: the level of exposition: the passage’s role in the motif’s arc; the level of the hidden, mystical meaning
- `pardes_szint` = `Peshat` (en: `Peshat`): a szó szerinti, történeti-nyelvtani jelentés szintje / the literal, historical-grammatical meaning
- `pardes_szint` = `Peshat/Drash` (en: `Peshat/Drash`): több szint együtt: a szó szerinti, történeti-nyelvtani jelentés szintje; a kifejtés szintje: a hely szerepe a motívum ívében / several levels together: the literal, historical-grammatical meaning; the level of exposition: the passage’s role in the motif’s arc
- `pardes_szint` = `Peshat/Drash/Sod` (en: `Peshat/Drash/Sod`): több szint együtt: a szó szerinti, történeti-nyelvtani jelentés szintje; a kifejtés szintje: a hely szerepe a motívum ívében; a rejtett, titokzatos jelentés szintje / several levels together: the literal, historical-grammatical meaning; the level of exposition: the passage’s role in the motif’s arc; the level of the hidden, mystical meaning
- `pardes_szint` = `Peshat/Remez` (en: `Peshat/Remez`): több szint együtt: a szó szerinti, történeti-nyelvtani jelentés szintje; az utalás szintje: kereszthivatkozás, párhuzam / several levels together: the literal, historical-grammatical meaning; the level of allusion: cross-reference, parallel
- `pardes_szint` = `Peshat/Sod` (en: `Peshat/Sod`): több szint együtt: a szó szerinti, történeti-nyelvtani jelentés szintje; a rejtett, titokzatos jelentés szintje / several levels together: the literal, historical-grammatical meaning; the level of the hidden, mystical meaning
- `pardes_szint` = `Remez` (en: `Remez`): az utalás szintje: kereszthivatkozás, párhuzam / the level of allusion: cross-reference, parallel
- `pardes_szint` = `Remez/Drash` (en: `Remez/Drash`): több szint együtt: az utalás szintje: kereszthivatkozás, párhuzam; a kifejtés szintje: a hely szerepe a motívum ívében / several levels together: the level of allusion: cross-reference, parallel; the level of exposition: the passage’s role in the motif’s arc
- `pardes_szint` = `Remez/Sod` (en: `Remez/Sod`): több szint együtt: az utalás szintje: kereszthivatkozás, párhuzam; a rejtett, titokzatos jelentés szintje / several levels together: the level of allusion: cross-reference, parallel; the level of the hidden, mystical meaning
- `pardes_szint` = `Sod` (en: `Sod`): a rejtett, titokzatos jelentés szintje / the level of the hidden, mystical meaning

### `pardes_szint_en`

Az előző oszlop (pardes_szint) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (pardes_szint), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `strong`

A sor Strong-száma (H = héber, G = görög); üres, ha a sor nem lexikai horgonyon áll.

*The row’s Strong number (H = Hebrew, G = Greek); empty when the row does not rest on a lexical anchor.*


### `strong_glossza_en`

Rövid angol szófogódzó: a sor Strong-számának glosszája a STEPBible TBESH (héber) és TBESG (görög) lexikonjából (a Gloss oszlop; a Meaning oszlop nem). Több Strong-számnál ` + `-szal fűzve, a sorrendjük szerint; ha a Strong-számnak több fő bejegyzése van (pl. név és köznév), ` / `-rel. A glossza a Strong-szám egészére szól, nem az adott vers jelentésére (arra a `jelentes_en`). Forrás: Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0).

*Short English word cue: the gloss of the row’s Strong number from the STEPBible TBESH (Hebrew) and TBESG (Greek) lexicons (the Gloss column, not the Meaning column). With several Strong numbers joined by ` + ` in their order; where a Strong number has several main entries (e.g. a name and a common noun), by ` / `. The gloss belongs to the Strong number as a whole, not to the meaning in the verse (for that, see `jelentes_en`). Source: Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0).*


### `szotar`

Melyik szótár jelentésére hivatkozik a sor.

*Which dictionary’s meaning the row refers to.*

- `szotar` = `BDB` (en: `BDB`): Brown–Driver–Briggs héber szótár (1906, közkincs) / Brown–Driver–Briggs Hebrew lexicon (1906, public domain)
- `szotar` = `TBESG` (en: `TBESG`): a Tyndale bővített Strong-számos görög rövid szótára (CC BY 4.0) / Tyndale Brief Lexicon of Extended Strongs for Greek (CC BY 4.0)
- `szotar` = `Thayer` (en: `Thayer`): Thayer görög–angol újszövetségi szótára (közkincs) / Thayer’s Greek–English lexicon of the New Testament (public domain)

### `szotar_en`

Az előző oszlop (szotar) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (szotar), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `szotari_szocikk`

A szócikk azonosítója az adott szótár kulcsa szerint.

*The entry identifier according to the dictionary’s own key.*


## forrasok_es_licencek.tsv


### `dataset`

Az adatkészlet (forrás) neve.

*The name of the dataset (source).*


### `licenc`

Az adatkészlet licence rövid címkével.

*The licence of the dataset as a short label.*

- `licenc` = `CC BY 4.0` (en: `CC BY 4.0`): Creative Commons Nevezd meg! 4.0: szabadon használható forrásmegjelöléssel / Creative Commons Attribution 4.0: free to use with attribution
- `licenc` = `CC BY-SA 4.0` (en: `CC BY-SA 4.0`): Creative Commons Nevezd meg! – Így add tovább! 4.0: a származtatott munka is ezen a licencen adható tovább / Creative Commons Attribution-ShareAlike 4.0: derived works must be shared under the same licence
- `licenc` = `CC0 1.0` (en: `CC0 1.0`): közkincs-nyilatkozat, korlátozás nélkül használható / public-domain dedication, free to use without restriction
- `licenc` = `közkincs` (en: `public domain`): a mű kora miatt közkincs / public domain because of the work’s age
- `licenc` = `minden jog fenntartva` (en: `all rights reserved`): a projekt zárt vagy fizetős származtatott rétege; nem része a csomagnak / a closed or paid derived layer of the project; not part of the package
- `licenc` = `tisztázatlan` (en: `unclear`): a licenc nem igazolt; ezért kizárva / the licence is not established; therefore excluded
- `licenc` = `© Mounce 1993` (en: `© Mounce 1993`): nem kereskedelmi használatra szóló licenc; kizárva / a licence for non-commercial use only; excluded

### `licenc_en`

Az előző oszlop (licenc) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (licenc), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `ok`

A besorolás oka (a kizárásé vagy a külön rétegé); üres, ha nincs külön ok.

*The reason for the classification (for exclusion or a separate layer); empty when there is no special reason.*

- `ok` = `CC BY-SA 4.0, de a csomag nem használja (nem kerül bele)` (en: `CC BY-SA 4.0, but not used by the package (not included)`): A licenc szerinti besorolás oka: CC BY-SA 4.0, de a csomag nem használja (nem kerül bele). / Reason for the licence classification: CC BY-SA 4.0, but not used by the package (not included).
- `ok` = `CC BY-SA 4.0: külön rétegben, attribúcióval, nem zárható` (en: `CC BY-SA 4.0: in a separate layer, with attribution, cannot be closed`): A licenc szerinti besorolás oka: CC BY-SA 4.0: külön rétegben, attribúcióval, nem zárható. / Reason for the licence classification: CC BY-SA 4.0: in a separate layer, with attribution, cannot be closed.
- `ok` = `a kereskedelmi használat nem szabad (feltetelesen: CC BY-SA 4.0)` (en: `commercial use not free (conditional: CC BY-SA 4.0)`): A licenc szerinti besorolás oka: a kereskedelmi használat nem szabad (feltetelesen: CC BY-SA 4.0). / Reason for the licence classification: commercial use not free (conditional: CC BY-SA 4.0).
- `ok` = `a kereskedelmi használat nem szabad (feltetelesen: közkincs)` (en: `commercial use not free (conditional: public domain)`): A licenc szerinti besorolás oka: a kereskedelmi használat nem szabad (feltetelesen: közkincs). / Reason for the licence classification: commercial use not free (conditional: public domain).
- `ok` = `a kereskedelmi használat nem szabad (nem: © Mounce 1993)` (en: `commercial use not free (no: © Mounce 1993)`): A licenc szerinti besorolás oka: a kereskedelmi használat nem szabad (nem: © Mounce 1993). / Reason for the licence classification: commercial use not free (no: © Mounce 1993).
- `ok` = `a nyílt mag licence CC BY 4.0 (a jogtulajdonos döntése)` (en: `the licence of the open core is CC BY 4.0 (decision of the rights holder)`): A licenc szerinti besorolás oka: a nyílt mag licence CC BY 4.0 (a jogtulajdonos döntése). / Reason for the licence classification: the licence of the open core is CC BY 4.0 (decision of the rights holder).
- `ok` = `a projekt saját adata` (en: `the project's own data`): A licenc szerinti besorolás oka: a projekt saját adata. / Reason for the licence classification: the project's own data.
- `ok` = `a projekt zárt (fizetős) származtatott rétege` (en: `the project's closed (paid) derived layer`): A licenc szerinti besorolás oka: a projekt zárt (fizetős) származtatott rétege. / Reason for the licence classification: the project's closed (paid) derived layer.
- `ok` = `nem része a nyílt magnak` (en: `not part of the open core`): A licenc szerinti besorolás oka: nem része a nyílt magnak. / Reason for the licence classification: not part of the open core.
- `ok` = `tisztázatlan licenc` (en: `unclear licence`): A licenc szerinti besorolás oka: tisztázatlan licenc. / Reason for the licence classification: unclear licence.

### `ok_en`

Az előző oszlop (ok) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (ok), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `szerepe_a_csomagban`

Mi az adatkészlet szerepe a nyílt csomagban.

*The dataset’s role in the open package.*

- `szerepe_a_csomagban` = `a csomag saját adata` (en: `the package's own data`): a projekt saját adata, a csomag licence alatt (CC BY 4.0) / the project’s own data, under the package licence (CC BY 4.0)
- `szerepe_a_csomagban` = `engedett, de a csomag nem használja` (en: `permitted, but not used by the package`): licence megengedné, de a csomag nem tartalmaz belőle értéket / the licence would allow it, but the package contains no value from it
- `szerepe_a_csomagban` = `forrás (a sorok forrásmegjelölésében szerepel)` (en: `source (named in the source credits of rows)`): a csomag sorainak forrásmegjelölésében szerepel; az adatot a csomag nem másolja / named in the source credits of package rows; the package does not copy the data
- `szerepe_a_csomagban` = `forrás (az angol szófogódzó oszlopé)` (en: `source (of the English word-cue column)`): a csomag értéket vesz át belőle: az elofordulasok.tsv strong_glossza_en oszlopa (a Strong-szám glosszája), attribúcióval a kódkönyvben és az olvass-el fájlokban / the package takes values from it: the strong_glossza_en column of elofordulasok.tsv (the gloss of the Strong number), with attribution in the codebook and the read-me files
- `szerepe_a_csomagban` = `kizárva` (en: `excluded`): a licenc miatt a csomag nem tartalmaz értéket belőle / because of the licence the package contains no value from it
- `szerepe_a_csomagban` = `külön réteg (cc_by_sa_reteg/)` (en: `separate layer (cc_by_sa_reteg/)`): a CC BY-SA 4.0 miatt külön könyvtárban, attribúcióval / in a separate directory with attribution because of CC BY-SA 4.0

### `szerepe_a_csomagban_en`

Az előző oszlop (szerepe_a_csomagban) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (szerepe_a_csomagban), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


## kapcsolatok.tsv


### `bizonyossag`

A kapcsolat bizonyossága; a küszöb alatti kapcsolat nem kerül ide.

*The certainty of the link; links below the threshold are not included.*

- `bizonyossag` = `alacsony` (en: `low`): gyenge, de megtartott kapcsolat / weak but retained link
- `bizonyossag` = `közepes` (en: `medium`): valószínű kapcsolat / probable link
- `bizonyossag` = `magas` (en: `high`): biztos kapcsolat / secure link

### `bizonyossag_en`

Az előző oszlop (bizonyossag) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (bizonyossag), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `cel_igehely`

A kapcsolat célja: a másik igehely.

*The target passage of the link.*


### `cel_igehely_osis`

Az előző oszlop (cel_igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (cel_igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `datum`

A rögzítés napja (ÉÉÉÉ-HH-NN); üres, ha nincs rögzítve.

*The date of recording (YYYY-MM-DD); empty when not recorded.*


### `forras_igehely`

A kapcsolat kiinduló igehelye.

*The starting passage of the link.*


### `forras_igehely_osis`

Az előző oszlop (forras_igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (forras_igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `forras_megnevezes`

A kapcsolat forrásának olvasói neve; üres, ha nincs rögzítve.

*The reader-facing name of the link’s source; empty when not recorded.*

- `forras_megnevezes` = `a projekt saját mérése és naplója` (en: `the project's own measurement and log`): A sor forrásának megnevezése: a projekt saját mérése és naplója. / Name of the source of the row: the project's own measurement and log.
- `forras_megnevezes` = `szerkesztői döntés` (en: `editorial decision`): A sor forrásának megnevezése: szerkesztői döntés. / Name of the source of the row: editorial decision.

### `forras_megnevezes_en`

Az előző oszlop (forras_megnevezes) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (forras_megnevezes), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `lekerdezes_tipusa`

A kapcsolat forrásának lekérdezés-típusa; üres, ha nincs rögzítve.

*The query type behind the link’s source; empty when not recorded.*

- `lekerdezes_tipusa` = `kézi döntés, lekérdezés nélkül` (en: `editorial decision, without a query`): a szerkesztői döntésből származó kapcsolat, nem lekérdezésből / a link from an editorial decision, not from a query

### `lekerdezes_tipusa_en`

Az előző oszlop (lekerdezes_tipusa) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (lekerdezes_tipusa), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `motivum_azonosito`

A motívum, amelyhez a kapcsolat tartozik.

*The motif the link belongs to.*


### `pardes_szint`

A kapcsolat PaRDeS-szintje.

*The PaRDeS level of the link.*

- `pardes_szint` = `Drash` (en: `Drash`): a kifejtés szintje: a hely szerepe a motívum ívében / the level of exposition: the passage’s role in the motif’s arc
- `pardes_szint` = `Drash/Sod` (en: `Drash/Sod`): több szint együtt: a kifejtés szintje: a hely szerepe a motívum ívében; a rejtett, titokzatos jelentés szintje / several levels together: the level of exposition: the passage’s role in the motif’s arc; the level of the hidden, mystical meaning
- `pardes_szint` = `Remez` (en: `Remez`): az utalás szintje: kereszthivatkozás, párhuzam / the level of allusion: cross-reference, parallel

### `pardes_szint_en`

Az előző oszlop (pardes_szint) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (pardes_szint), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `tipus`

A kapcsolat típusa.

*The type of the link.*

- `tipus` = `Beteljesedés` (en: `fulfilment`): az egyik hely a másik beteljesedése / one passage is the fulfilment of the other
- `tipus` = `Előkép` (en: `prefiguration`): az egyik hely a másiknak előképe / one passage prefigures the other
- `tipus` = `Kontraszt` (en: `contrast`): a két hely szembeállítás / the two passages stand in contrast
- `tipus` = `Párhuzam` (en: `parallel`): a két hely párhuzamos / the two passages are parallel
- `tipus` = `Variáns` (en: `variant`): a két hely ugyanannak a szövegnek változata / the two passages are variants of the same text

### `tipus_en`

Az előző oszlop (tipus) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (tipus), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


## kizaras_csoportok.tsv


### `csoport_sor_igehely`

Az összesítő sor igehelye a kizarasok.tsv-ben: a csoport egy (jelölő) verse; a csoport kulcsa.

*The passage of the summary row in kizarasok.tsv: one (marker) verse of the group; the key of the group.*


### `csoport_sor_igehely_osis`

Az előző oszlop (csoport_sor_igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (csoport_sor_igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `igehely`

A csoport egy tagja: egy kizárt vers, Károli-számozással; a csoport tagjainak száma a csoport_versszam.

*A member of the group: one excluded verse in Károli numbering; the number of members is csoport_versszam.*


### `igehely_osis`

Az előző oszlop (igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `motivum_azonosito`

A motívum, amelyből a csoportot kizártuk (l. motivumok.tsv).

*The motif from which the group was excluded (see motivumok.tsv).*


## kizarasok.tsv


### `azonositas_modja`

A Károli-szó azonosításának módja (l. elofordulasok.tsv).

*How the Károli word was identified (see elofordulasok.tsv).*

- `azonositas_modja` = `tartalom-alapú` (en: `content-based`): a szerkesztő a Károli-szöveget olvasva rendelte a szót a Strong-számhoz / the editor assigned the word to the Strong number by reading the Károli text

### `azonositas_modja_en`

Az előző oszlop (azonositas_modja) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (azonositas_modja), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `cel_igehely`

Motívumközi jelöltnél a másik motívum oldali igehely(ek); egyébként üres.

*For a link between motifs, the passage(s) on the other motif’s side; otherwise empty.*


### `cel_igehely_osis`

Az előző oszlop (cel_igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (cel_igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `cel_motivum`

Motívumközi jelöltnél a másik motívum azonosítója; egyébként üres.

*For a link between motifs, the other motif’s identifier; otherwise empty.*


### `csoport_versszam`

Csoportos kizárásnál (összesítő sor) a csoport verseinek száma; a sor a csoport egy versét nevezi meg, a csoport összes verse a kizaras_csoportok.tsv-ben áll, az indoklás a csoportra érvényes. Egyedi kizárásnál üres.

*For a group exclusion (summary row) the number of verses in the group; the row names one (marker) verse of the group, all verses of the group are listed in kizaras_csoportok.tsv, and the rationale applies to the group. Empty for an individual exclusion.*


### `datum`

A döntés napja (ÉÉÉÉ.HH.NN).

*The date of the decision (YYYY.MM.DD).*


### `dontesek`

A kizárást megalapozó döntések nyilvános azonosítói (NYD-nnn), a dontesnaplo.tsv-ben oldhatók fel; `;`-vel elválasztva.

*Public identifiers (NYD-nnn) of the decisions behind the exclusion, resolvable in dontesnaplo.tsv; separated by `;`.*


### `forditas_modja`

A sor angol párhuzamos mezőinek (`…_en`, szabad szöveg) készítési módja: `gépi fordítás (<modell>)` — a ténylegesen futott modell neve; `…; részben hiányzik` — a sor egyik szabad szöveges mezőjének nincs érvényes fordítása; `nincs fordítás` — egyiknek sincs; üres — a sorban nincs szabad szöveg. A zárt értékek `_en` címkéje nem gépi fordítás, hanem a kódkönyv szerkesztett címkéje.

*How the row’s English parallel fields (`…_en`, free text) were made: `gépi fordítás (<model>)` = machine translation by the model actually run; `…; részben hiányzik` = one free-text field of the row has no valid translation; `nincs fordítás` = none has; empty = the row has no free text. The `_en` labels of closed-vocabulary values are not machine translations but edited codebook labels.*


### `igehely`

A kizárt igehely, Károli-számozással.

*The excluded passage, in Károli numbering.*


### `igehely_osis`

Az előző oszlop (igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `indoklas`

A kizárás szerkesztői indoklása.

*The editorial rationale for the exclusion.*


### `indoklas_en`

Az előző oszlop (indoklas) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (indoklas): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `jelolt_tipus`

Mit vizsgáltunk: egy motívum lehetséges előfordulását vagy két motívum közti kapcsolatot.

*What was examined: a candidate occurrence of a motif, or a link between two motifs.*

- `jelolt_tipus` = `elofordulas` (en: `occurrence`): a motívum lehetséges előfordulása / a candidate occurrence of the motif
- `jelolt_tipus` = `motivumkozi` (en: `between motifs`): lehetséges kapcsolat két motívum között / a candidate link between two motifs

### `jelolt_tipus_en`

Az előző oszlop (jelolt_tipus) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (jelolt_tipus), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `karoli_szo`

A szóalak a Károli-fordításban ezen a helyen, ha rögzítettük.

*The word form in the Károli translation at this place, if recorded.*


### `keresesi_mod`

Hogyan jutottunk a jelölthöz.

*How the candidate was found.*

- `keresesi_mod` = `Károli-kereszthivatkozás` (en: `Károli cross-reference`): a Károli-kiadás kereszthivatkozásai (az ismert hibákat l. ISMERT_HIBAK.md) / the cross-references of the Károli edition (for known errors see ISMERT_HIBAK.md)
- `keresesi_mod` = `TSK-kereszthivatkozás` (en: `TSK cross-reference`): a Treasury of Scripture Knowledge kereszthivatkozásai / the cross-references of the Treasury of Scripture Knowledge
- `keresesi_mod` = `kollokáció (két szó egy versben)` (en: `collocation (two words in one verse)`): két szó együttes előfordulása egy versben / co-occurrence of two words in one verse
- `keresesi_mod` = `motívumközi kapcsolat vizsgálata` (en: `examination of a link between motifs`): két motívum közti kapcsolat vizsgálata / examination of a link between two motifs
- `keresesi_mod` = `rokon szavak (szócsalád) keresése` (en: `search for related words (word family)`): egy szócsalád rokon szavainak keresése / a search for related words of one word family
- `keresesi_mod` = `szerkesztői teljességi felmérés` (en: `editorial completeness survey`): a motívum teljességét ellenőrző szerkesztői felmérés / an editorial survey checking the completeness of the motif
- `keresesi_mod` = `szerkesztői vizsgálat (a keresés módja külön nincs rögzítve)` (en: `editorial examination (search method not recorded separately)`): szerkesztői vizsgálat; a keresés módját nem rögzítettük külön / an editorial examination; the search method was not recorded separately
- `keresesi_mod` = `szó-szintű visszakeresés a héber/görög szövegben` (en: `word-level look-up in the Hebrew/Greek text`): szó szerinti visszakeresés a héber vagy görög szövegben / word-level look-up in the Hebrew or Greek text
- `keresesi_mod` = `szóbázis (Strong-szám) szerinti teljes szövegkeresés` (en: `full-text search by lexical base (Strong's number)`): a Strong-szám szerinti keresés a teljes szövegben / a search by Strong number across the whole text
- `keresesi_mod` = `szótári (BDB) szócikk alapján` (en: `from the dictionary (BDB) entry`): a BDB szótári szócikke alapján talált hely / a passage found through the BDB dictionary entry
- `keresesi_mod` = `többforrásos ellenőrzés` (en: `multi-source check`): több forrás összevetésével végzett ellenőrzés / a check carried out by comparing several sources

### `keresesi_mod_en`

Az előző oszlop (keresesi_mod) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (keresesi_mod), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `kizaras_oka`

A kizárás oka szöveges besorolásban.

*The reason for exclusion, as a textual category.*

- `kizaras_oka` = `a Károli-szó itt más szót fordít` (en: `the Károli word translates a different word here`): Kizárási ok: a Károli-szó itt más szót fordít. / Reason for exclusion: the Károli word translates a different word here.
- `kizaras_oka` = `a Károli-szó más szót fordít (összesítő sor)` (en: `the Károli word translates a different word (summary row)`): Kizárási ok: a Károli-szó más szót fordít (összesítő sor). / Reason for exclusion: the Károli word translates a different word (summary row).
- `kizaras_oka` = `a Septuaginta többlete, a héberben nincs seól` (en: `a Septuagint plus; sheol is absent from the Hebrew`): Kizárási ok: a Septuaginta többlete, a héberben nincs seól. / Reason for exclusion: a Septuagint plus; sheol is absent from the Hebrew.
- `kizaras_oka` = `a Septuaginta többlete, az eredetiben nincs a szópár` (en: `a Septuagint plus; the word pair is absent from the original`): Kizárási ok: a Septuaginta többlete, az eredetiben nincs a szópár. / Reason for exclusion: a Septuagint plus; the word pair is absent from the original.
- `kizaras_oka` = `a besorolás nincs rögzítve` (en: `classification not recorded`): Kizárási ok: a besorolás nincs rögzítve. / Reason for exclusion: classification not recorded.
- `kizaras_oka` = `a fejezet más témája, nem a motívum` (en: `another theme of the chapter, not the motif`): Kizárási ok: a fejezet más témája, nem a motívum. / Reason for exclusion: another theme of the chapter, not the motif.
- `kizaras_oka` = `a formula nincs a versben` (en: `the formula is not in the verse`): Kizárási ok: a formula nincs a versben. / Reason for exclusion: the formula is not in the verse.
- `kizaras_oka` = `a fáradság bölcsességirodalmi toposza, a genezisi szó nélkül` (en: `wisdom-literature topos of toil, without the Genesis word`): Kizárási ok: a fáradság bölcsességirodalmi toposza, a genezisi szó nélkül. / Reason for exclusion: wisdom-literature topos of toil, without the Genesis word.
- `kizaras_oka` = `a föld elvesztése vagy terméketlensége a szövetségi rendben, nem a lánc` (en: `loss or barrenness of the land within the covenant order, not the chain`): Kizárási ok: a föld elvesztése vagy terméketlensége a szövetségi rendben, nem a lánc. / Reason for exclusion: loss or barrenness of the land within the covenant order, not the chain.
- `kizaras_oka` = `a föld gyásza vagy pusztulása megnevezett bűn és a lánc szava nélkül` (en: `the land mourns or is laid waste without a named sin or a word of the chain`): Kizárási ok: a föld gyásza vagy pusztulása megnevezett bűn és a lánc szava nélkül. / Reason for exclusion: the land mourns or is laid waste, but no sin is named and no word of the chain occurs.
- `kizaras_oka` = `a hely egy másik sorban áll` (en: `the passage stands in another row`): Kizárási ok: a hely egy másik sorban áll. / Reason for exclusion: the passage stands in another row.
- `kizaras_oka` = `a hívás igéje a név nélkül (összesítő sor)` (en: `the verb of calling without the name (summary row)`): Kizárási ok: a hívás igéje a név nélkül (összesítő sor). / Reason for exclusion: the verb of calling without the name (summary row).
- `kizaras_oka` = `a hívás és a név nem egy szerkezetben (összesítő sor)` (en: `calling and name not in one construction (summary row)`): Kizárási ok: a hívás és a név nem egy szerkezetben (összesítő sor). / Reason for exclusion: calling and name not in one construction (summary row).
- `kizaras_oka` = `a jelölés forrásadata hibás` (en: `the source data of the candidate are faulty`): Kizárási ok: a jelölés forrásadata hibás. / Reason for exclusion: the source data of the candidate are faulty.
- `kizaras_oka` = `a két szó nem egy mondatban áll` (en: `the two words are not in one sentence`): Kizárási ok: a két szó nem egy mondatban áll. / Reason for exclusion: the two words are not in one sentence.
- `kizaras_oka` = `a két szó nem megkülönböztető szerepben` (en: `the two words are not in a distinguishing role`): Kizárási ok: a két szó nem megkülönböztető szerepben. / Reason for exclusion: the two words are not in a distinguishing role.
- `kizaras_oka` = `a mező füve mint táplálék, nem a tövis-átok` (en: `grass of the field as food, not the curse of thorns`): Kizárási ok: a mező füve mint táplálék, nem a tövis-átok. / Reason for exclusion: grass of the field as food, not the curse of thorns.
- `kizaras_oka` = `a romlás igéje a szövetséges nép hűtlenségére, az egyetemes szerkezet nélkül` (en: `the verb of corruption applied to the covenant people’s unfaithfulness, without the universal structure`): Kizárási ok: a romlás igéje a szövetséges nép hűtlenségére, az egyetemes szerkezet nélkül. / Reason for exclusion: the verb of corruption applied to the covenant people’s unfaithfulness, without the universal structure.
- `kizaras_oka` = `a szó más jelentésben áll` (en: `the word is used with another meaning`): Kizárási ok: a szó más jelentésben áll. / Reason for exclusion: the word is used with another meaning.
- `kizaras_oka` = `a szó nem ebben a versben áll, hanem a tartomány másikában` (en: `the word is not in this verse but in another verse of the range`): Kizárási ok: a szó nem ebben a versben áll, hanem a tartomány másikában. / Reason for exclusion: the word is not in this verse but in another verse of the range.
- `kizaras_oka` = `a szó áll, de általános használatban, a lánc nélkül (összesítő sor)` (en: `the word occurs, but in general usage, without the chain (summary row)`): Kizárási ok: a szó áll, de általános használatban, a lánc nélkül (összesítő sor). / Reason for exclusion: the word occurs, but in general usage, without the chain (summary row).
- `kizaras_oka` = `a szócsalád más használata, nem a romlás szerkezete` (en: `other use of the word family, not the structure of corruption`): Kizárási ok: a szócsalád más használata, nem a romlás szerkezete. / Reason for exclusion: other use of the word family, not the structure of corruption.
- `kizaras_oka` = `a szótár idézi, de a Károli-versben a szó nem áll (összesítő sor)` (en: `cited by the lexicon, but the word is absent from the Károli verse (summary row)`): Kizárási ok: a szótár idézi, de a Károli-versben a szó nem áll (összesítő sor). / Reason for exclusion: cited by the lexicon, but the word is absent from the Károli verse (summary row).
- `kizaras_oka` = `a tohu és bohu szópár nincs a versben` (en: `the word pair tohu and bohu is not in the verse`): Kizárási ok: a tohu és bohu szópár nincs a versben. / Reason for exclusion: the word pair tohu and bohu is not in the verse.
- `kizaras_oka` = `a „vég” formulája, más kulcsszóval` (en: `the formula of "the end", with another key word`): Kizárási ok: a „vég” formulája, más kulcsszóval. / Reason for exclusion: the formula of "the end", with another key word.
- `kizaras_oka` = `az erőszak szava más használatban, nem a föld megtelése` (en: `the word for violence in another use, not the filling of the earth`): Kizárási ok: az erőszak szava más használatban, nem a föld megtelése. / Reason for exclusion: the word for violence in another use, not the filling of the earth.
- `kizaras_oka` = `az öröklött bűnösség kérdése, amelyet a lap nem dönt el` (en: `the question of inherited sinfulness, which the entry leaves open`): Kizárási ok: az öröklött bűnösség kérdése, amelyet a lap nem dönt el. / Reason for exclusion: the question of inherited sinfulness, which the entry leaves open.
- `kizaras_oka` = `az özönvíz-elbeszélés felidézése, az átok terjedése nélkül` (en: `recalling the flood narrative, without the spread of the curse`): Kizárási ok: az özönvíz-elbeszélés felidézése, az átok terjedése nélkül. / Reason for exclusion: recalling the flood narrative, without the spread of the curse.
- `kizaras_oka` = `az „Isten előtt” kifejezés, nem a motívum` (en: `the expression "before God", not the motif`): Kizárási ok: az „Isten előtt” kifejezés, nem a motívum. / Reason for exclusion: the expression "before God", not the motif.
- `kizaras_oka` = `csak az egyik szó vagy más szó áll a versben (összesítő sor)` (en: `only one of the words, or another word, in the verse (summary row)`): Kizárási ok: csak az egyik szó vagy más szó áll a versben (összesítő sor). / Reason for exclusion: only one of the words, or another word, in the verse (summary row).
- `kizaras_oka` = `csak tematikus párhuzam, lexikai kapcsolat nélkül` (en: `thematic parallel only, without a lexical link`): Kizárási ok: csak tematikus párhuzam, lexikai kapcsolat nélkül. / Reason for exclusion: thematic parallel only, without a lexical link.
- `kizaras_oka` = `egy bent lévő hely folytatása, a szerkezet ott áll` (en: `continuation of an included passage, where the structure stands`): Kizárási ok: egy bent lévő hely folytatása, a szerkezet ott áll. / Reason for exclusion: continuation of an included passage, where the structure stands.
- `kizaras_oka` = `egy másik motívum tárgya` (en: `subject of another motif`): Kizárási ok: egy másik motívum tárgya. / Reason for exclusion: subject of another motif.
- `kizaras_oka` = `elnevezés, nem a név segítségül hívása (összesítő sor)` (en: `naming, not calling on the name (summary row)`): Kizárási ok: elnevezés, nem a név segítségül hívása (összesítő sor). / Reason for exclusion: naming, not calling on the name (summary row).
- `kizaras_oka` = `emberi átkozódás, nem a genezisi lánc folytatása` (en: `human cursing, not a continuation of the Genesis chain`): Kizárási ok: emberi átkozódás, nem a genezisi lánc folytatása. / Reason for exclusion: human cursing, not a continuation of the Genesis chain.
- `kizaras_oka` = `erkölcsi intelem, nem a formula` (en: `moral admonition, not the formula`): Kizárási ok: erkölcsi intelem, nem a formula. / Reason for exclusion: moral admonition, not the formula.
- `kizaras_oka` = `eskü vagy tanúhívás` (en: `oath or calling of witnesses`): Kizárási ok: eskü vagy tanúhívás. / Reason for exclusion: oath or calling of witnesses.
- `kizaras_oka` = `fizikai pusztítás, nem erkölcsi megromlás` (en: `physical destruction, not moral corruption`): Kizárási ok: fizikai pusztítás, nem erkölcsi megromlás. / Reason for exclusion: physical destruction, not moral corruption.
- `kizaras_oka` = `halálveszélyben elmondott ima, a seól szava nélkül` (en: `prayer in mortal danger, without the word sheol`): Kizárási ok: halálveszélyben elmondott ima, a seól szava nélkül. / Reason for exclusion: prayer in mortal danger, without the word sheol.
- `kizaras_oka` = `invokáció a formulán kívül` (en: `invocation outside the formula`): Kizárási ok: invokáció a formulán kívül. / Reason for exclusion: invocation outside the formula.
- `kizaras_oka` = `jogi fellebbezés` (en: `legal appeal`): Kizárási ok: jogi fellebbezés. / Reason for exclusion: legal appeal.
- `kizaras_oka` = `jogi, bűnbánati vagy panasz-használat, a lánc nélkül` (en: `legal, penitential or lament usage, without the chain`): Kizárási ok: jogi, bűnbánati vagy panasz-használat, a lánc nélkül. / Reason for exclusion: legal, penitential or lament usage, without the chain.
- `kizaras_oka` = `megszólítás, nem a név segítségül hívása` (en: `address, not calling on the name`): Kizárási ok: megszólítás, nem a név segítségül hívása. / Reason for exclusion: address, not calling on the name.
- `kizaras_oka` = `más szó a Károli-fordításban (összesítő sor)` (en: `another word in the Károli translation (summary row)`): Kizárási ok: más szó a Károli-fordításban (összesítő sor). / Reason for exclusion: another word in the Károli translation (summary row).
- `kizaras_oka` = `más szó áll a versben, nem a motívum lexémája (összesítő sor)` (en: `another word in the verse, not the lexeme of the motif (summary row)`): Kizárási ok: más szó áll a versben, nem a motívum lexémája (összesítő sor). / Reason for exclusion: another word in the verse, not the lexeme of the motif (summary row).
- `kizaras_oka` = `más szókapcsolat (Isten letekint, minden test), nem a romlás szerkezete` (en: `another word combination (God looks down, all flesh), not the structure of corruption`): Kizárási ok: más szókapcsolat (Isten letekint, minden test), nem a romlás szerkezete. / Reason for exclusion: another word combination (God looks down, all flesh), not the structure of corruption.
- `kizaras_oka` = `nem JHVH áll a név után` (en: `the name is not followed by YHWH`): Kizárási ok: nem JHVH áll a név után. / Reason for exclusion: the name is not followed by YHWH.
- `kizaras_oka` = `nem JHVH áll a név után (összesítő sor)` (en: `the name is not followed by YHWH (summary row)`): Kizárási ok: nem JHVH áll a név után (összesítő sor). / Reason for exclusion: the name is not followed by YHWH (summary row).
- `kizaras_oka` = `nincs meg a hívás + név szerkezete` (en: `the structure calling + name is missing`): Kizárási ok: nincs meg a hívás + név szerkezete. / Reason for exclusion: the structure calling + name is missing.
- `kizaras_oka` = `név nélküli forma` (en: `form without the name`): Kizárási ok: név nélküli forma. / Reason for exclusion: form without the name.
- `kizaras_oka` = `névadás` (en: `name-giving`): Kizárási ok: névadás. / Reason for exclusion: name-giving.
- `kizaras_oka` = `passzív szerkezet vagy megnevezés (negatív kritérium)` (en: `passive construction or designation (exclusion criterion)`): Kizárási ok: passzív szerkezet vagy megnevezés (negatív kritérium). / Reason for exclusion: passive construction or designation (exclusion criterion).
- `kizaras_oka` = `romlás más értelemben, nem a genezisi szerkezet` (en: `corruption with another meaning, not the Genesis structure`): Kizárási ok: romlás más értelemben, nem a genezisi szerkezet. / Reason for exclusion: corruption with another meaning, not the Genesis structure.
- `kizaras_oka` = `semleges, elbeszélő használat, nem az átok-szerkezet` (en: `neutral, narrative use, not the curse structure`): Kizárási ok: semleges, elbeszélő használat, nem az átok-szerkezet. / Reason for exclusion: neutral, narrative use, not the curse structure.
- `kizaras_oka` = `száműzetés-büntetés, a föld kulcsszava nélkül` (en: `punishment of banishment, without the key word for the ground`): Kizárási ok: száműzetés-büntetés, a föld kulcsszava nélkül. / Reason for exclusion: punishment of banishment, without the key word for the ground.
- `kizaras_oka` = `szótári összevető hely, a szó nem áll benne` (en: `dictionary comparison passage; the word is not in it`): Kizárási ok: szótári összevető hely, a szó nem áll benne. / Reason for exclusion: dictionary comparison passage; the word is not in it.
- `kizaras_oka` = `szövetségi átok-formula, a föld szava nélkül` (en: `covenant curse formula, without the word for ground`): Kizárási ok: szövetségi átok-formula, a föld szava nélkül. / Reason for exclusion: covenant curse formula, without the word for ground.
- `kizaras_oka` = `szövetségi átok-szakasz, az átok-ige nélkül` (en: `covenant curse section, without the verb of cursing`): Kizárási ok: szövetségi átok-szakasz, az átok-ige nélkül. / Reason for exclusion: covenant curse section, without the verb of cursing.
- `kizaras_oka` = `tartalmilag nem kapcsolódik` (en: `not related in content`): Kizárási ok: tartalmilag nem kapcsolódik. / Reason for exclusion: not related in content.
- `kizaras_oka` = `tövis-kép, a genezisi szókapcsolat nélkül` (en: `image of thorns, without the Genesis word combination`): Kizárási ok: tövis-kép, a genezisi szókapcsolat nélkül. / Reason for exclusion: image of thorns, without the Genesis word combination.
- `kizaras_oka` = `általános bűn-leírás, a terjedés szerkezete nélkül` (en: `general description of sin, without the structure of spreading`): Kizárási ok: általános bűn-leírás, a terjedés szerkezete nélkül. / Reason for exclusion: general description of sin, without the structure of spreading.
- `kizaras_oka` = `általános engedetlenség-téma, a föld-átok szerkezete nélkül` (en: `general theme of disobedience, without the structure of the curse on the ground`): Kizárási ok: általános engedetlenség-téma, a föld-átok szerkezete nélkül. / Reason for exclusion: general theme of disobedience, without the structure of the curse on the ground.
- `kizaras_oka` = `átok-kimondás, a következmény továbbterjedése nélkül` (en: `pronouncing a curse, without the consequence spreading further`): Kizárási ok: átok-kimondás, a következmény továbbterjedése nélkül. / Reason for exclusion: pronouncing a curse, without the consequence spreading further.

### `kizaras_oka_en`

Az előző oszlop (kizaras_oka) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (kizaras_oka), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `korabbi_minosites`

A jelölt korábbi minősítése és annak indoklása, ha volt; egyébként üres.

*The candidate’s earlier assessment and its rationale, if any; otherwise empty.*


### `korabbi_minosites_en`

Az előző oszlop (korabbi_minosites) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (korabbi_minosites): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `megbizhatosag`

A Károli-szó azonosításának bizonyossága.

*The confidence of the Károli word identification.*

- `megbizhatosag` = `közepes` (en: `medium`): valószínű, de nem biztos azonosítás / probable but not certain identification
- `megbizhatosag` = `magas` (en: `high`): biztos azonosítás / secure identification

### `megbizhatosag_en`

Az előző oszlop (megbizhatosag) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (megbizhatosag), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `motivum_azonosito`

Az a motívum, amelyből a helyet kizártuk (l. motivumok.tsv).

*The motif from which the passage was excluded (see motivumok.tsv).*


## kodkonyv.tsv


### `ertek`

A zárt értékkészletű oszlop egy értéke; üres, ha a sor az oszlopot magát írja le.

*One value of a closed-value column; empty when the row describes the column itself.*


### `leiras_en`

A leírás angolul.

*The description in English.*


### `leiras_hu`

A leírás magyarul.

*The description in Hungarian.*


### `oszlop`

Az oszlop neve a táblában.

*The column name in the table.*


### `tabla`

A fájl, amelynek az oszlopát vagy értékét a sor leírja.

*The file whose column or value the row describes.*


## motivum_kapcsolatok.tsv


### `alpont_a`

Az A motívum alpontja, ha a kapcsolat egy alpontra irányul; egyébként üres.

*The sub-point of motif A if the link targets a sub-point; otherwise empty.*


### `alpont_b`

A B motívum alpontja, ha a kapcsolat egy alpontra irányul; egyébként üres.

*The sub-point of motif B if the link targets a sub-point; otherwise empty.*


### `bizonyossag`

A kapcsolat bizonyossága.

*The certainty of the link.*

- `bizonyossag` = `közepes` (en: `medium`): valószínű, de nem biztos kapcsolat / probable but not certain link

### `bizonyossag_en`

Az előző oszlop (bizonyossag) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (bizonyossag), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `datum`

A rögzítés napja (ÉÉÉÉ-HH-NN).

*The date of recording (YYYY-MM-DD).*


### `dontesek`

A döntés nyilvános azonosítói (NYD-nnn), a dontesnaplo.tsv-ben oldhatók fel.

*Public identifiers (NYD-nnn) of the decision, resolvable in dontesnaplo.tsv.*


### `forras_megnevezes`

A forrás olvasói neve.

*The reader-facing name of the source.*

- `forras_megnevezes` = `Karoli_1908 (közkincs)` (en: `Karoli_1908 (public domain)`): A sor forrásának megnevezése: Karoli_1908 (közkincs). / Name of the source of the row: Karoli_1908 (public domain).
- `forras_megnevezes` = `a projekt saját mérése és naplója` (en: `the project's own measurement and log`): A sor forrásának megnevezése: a projekt saját mérése és naplója. / Name of the source of the row: the project's own measurement and log.

### `forras_megnevezes_en`

Az előző oszlop (forras_megnevezes) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (forras_megnevezes), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `igehely_a`

Az A motívum oldali igehely.

*The passage on the A motif’s side.*


### `igehely_a_osis`

Az előző oszlop (igehely_a) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (igehely_a) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `igehely_b`

A B motívum oldali igehely.

*The passage on the B motif’s side.*


### `igehely_b_osis`

Az előző oszlop (igehely_b) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11; több igehely szóközzel). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása. Ahol ez eltér a KJV- vagy a STEPBible-számozástól (például a zsoltárfeliratoknál), az OSIS-kulcs a Károli-verset jelöli, nem a KJV azonos számú versét; más korpuszokkal közvetlenül csak ott kapcsolható össze, ahol a két számozás egyezik.

*The passage of the preceding column (igehely_b) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11; several passages separated by a space). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation. Where it differs from the KJV or STEPBible numbering (for example in the Psalm titles), the OSIS key denotes the Károli verse, not the KJV verse with the same number; it links directly to other corpora only where the two versifications agree.*


### `lekerdezes_tipusa`

A kapcsolat forrásának lekérdezés-típusa.

*The query type behind the link’s source.*

- `lekerdezes_tipusa` = `megadott igehely-tartomány` (en: `given passage range`): a megadott igehely-tartományon futtatott mérés / a measurement run over a given passage range

### `lekerdezes_tipusa_en`

Az előző oszlop (lekerdezes_tipusa) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (lekerdezes_tipusa), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `motivum_a`

A kapcsolat egyik motívuma.

*One motif of the link.*


### `motivum_b`

A kapcsolat másik motívuma.

*The other motif of the link.*


### `pardes_szint`

A kapcsolat PaRDeS-szintje.

*The PaRDeS level of the link.*

- `pardes_szint` = `Remez` (en: `Remez`): az utalás szintje: kereszthivatkozás, párhuzam / the level of allusion: cross-reference, parallel

### `pardes_szint_en`

Az előző oszlop (pardes_szint) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (pardes_szint), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `tipus`

A motívumközi kapcsolat típusa.

*The type of the link between motifs.*

- `tipus` = `szomszédos` (en: `adjacent`): a két motívum egy-egy előfordulása közel áll egymáshoz (mért távolsággal), de a közelség önmagában nem bizonyít szándékos utalást / one occurrence of each motif lie close together (with a measured distance), but proximity alone does not prove deliberate allusion

### `tipus_en`

Az előző oszlop (tipus) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (tipus), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


## motivumok.tsv


### `azonossag_tipusa`

Az azonosság hordozója: mitől ugyanaz a motívum két helyen.

*The carrier of identity: what makes two passages instances of the same motif.*

- `azonossag_tipusa` = `formulaikus` (en: `formulaic`): ugyanaz a rögzített kifejezés vagy formula köti össze a helyeket / the same fixed expression or formula links the passages
- `azonossag_tipusa` = `lexikai` (en: `lexical`): ugyanaz a szó vagy szógyök (szóbázis) köti össze a helyeket / the same word or word root (lexical base) links the passages
- `azonossag_tipusa` = `strukturális` (en: `structural`): ugyanaz a szerkezet köti össze a helyeket, nem feltétlenül ugyanaz a szó / the same structure links the passages, not necessarily the same word

### `azonossag_tipusa_en`

Az előző oszlop (azonossag_tipusa) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (azonossag_tipusa), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `cim`

A motívum teljes neve.

*The full name of the motif.*


### `cim_en`

Az előző oszlop (cim) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (cim): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `feldolgozasi_allapot`

A motívum feldolgozási állapota, az adatból számolva: lezárt kiadás, ha a motívum lexikonlapja a kész lap mai mércéje szerint (2026-11-11 óta) jelent meg, az olvasói kapu nem talál rajta hibát, és a lap nincs újraírásra félretéve; minden más motívum korábbi feldolgozás, újraírás alatt.

*The processing stage of the motif, computed from the data: a closed release if the lexicon page of the motif was released under the current standard for a finished page (since 2026-11-11), the reader check finds no error on it, and the page is not set aside for rewriting; every other motif is an earlier processing, being rewritten.*

- `feldolgozasi_allapot` = `korábbi feldolgozás, újraírás alatt` (en: `earlier processing, being rewritten`): A motívum a projekt korábbi szakaszában, régebbi eljárással készült, és a lexikonlapja a mai mérce szerint újraíródik. Adatai a mai sémában állnak, és a csomagban maradnak, de az újraírás során módosulhatnak. / The motif was built at an earlier stage of the project with an older procedure, and its lexicon page is being rewritten to the current standard. Its data follow the current schema and stay in the package, but they may change during the rewrite.
- `feldolgozasi_allapot` = `lezárt kiadás` (en: `closed release`): A motívum végigment a teljes kiadási eljáráson: lexikonlapja kiadott, az olvasói kapun hiba nélkül átment, és a szerző átnézte. / The motif has passed the full release procedure: its lexicon page is released, passed the reader check without error and was reviewed by the author.

### `feldolgozasi_allapot_en`

Az előző oszlop (feldolgozasi_allapot) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (feldolgozasi_allapot), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `folerendelt_fogalom`

A tágabb fogalom, amely felé a motívum hígulhat; ami csak ezen keresztül tartozna ide, kizárandó.

*The broader concept toward which the motif may dilute; whatever would belong only through it is excluded.*


### `folerendelt_fogalom_en`

Az előző oszlop (folerendelt_fogalom) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (folerendelt_fogalom): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `forditas_modja`

A sor angol párhuzamos mezőinek (`…_en`, szabad szöveg) készítési módja: `gépi fordítás (<modell>)` — a ténylegesen futott modell neve; `…; részben hiányzik` — a sor egyik szabad szöveges mezőjének nincs érvényes fordítása; `nincs fordítás` — egyiknek sincs; üres — a sorban nincs szabad szöveg. A zárt értékek `_en` címkéje nem gépi fordítás, hanem a kódkönyv szerkesztett címkéje.

*How the row’s English parallel fields (`…_en`, free text) were made: `gépi fordítás (<model>)` = machine translation by the model actually run; `…; részben hiányzik` = one free-text field of the row has no valid translation; `nincs fordítás` = none has; empty = the row has no free text. The `_en` labels of closed-vocabulary values are not machine translations but edited codebook labels.*


### `meghatarozas`

A motívum olvasói meghatározása egy-két mondatban: mi a motívum. Nem a cím, nem az azonosság típusa, és nem a negatív kritérium; üres, ha a motívumnak még nincs meghatározása.

*The reader-facing definition of the motif in one or two sentences: what the motif is. Not the title, not the identity type and not the exclusion criterion; empty when the motif has no definition yet.*


### `meghatarozas_en`

Az előző oszlop (meghatarozas) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (meghatarozas): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `motivum_azonosito`

A motívum azonosítója: TÉMAKÓD-sorszám (pl. ALVIL-001); a többi fájl ezzel hivatkozik a motívumra.

*The motif identifier: THEME CODE-number (e.g. ALVIL-001); the other files refer to the motif by it.*


### `negativ_kriterium`

A kizáró jegy: az a minimális jegy, amely nélkül egy igehely nem tartozik a motívumhoz. A határt a kizárások húzzák meg.

*The exclusion criterion: the minimal feature without which a passage does not belong to the motif. The boundary is drawn by the exclusions.*


### `negativ_kriterium_en`

Az előző oszlop (negativ_kriterium) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (negativ_kriterium): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `pardes_szint`

A motívum súlypontja a PaRDeS-szintek között.

*The motif’s centre of gravity among the PaRDeS levels.*

- `pardes_szint` = `Drash` (en: `Drash`): a kifejtés szintje: a hely szerepe a motívum ívében / the level of exposition: the passage’s role in the motif’s arc
- `pardes_szint` = `Drash/Sod` (en: `Drash/Sod`): több szint együtt: a kifejtés szintje: a hely szerepe a motívum ívében; a rejtett, titokzatos jelentés szintje / several levels together: the level of exposition: the passage’s role in the motif’s arc; the level of the hidden, mystical meaning
- `pardes_szint` = `Pshat/Drash` (en: `Peshat/Drash`): több szint együtt: a Peshat másik írásmódja; a kifejtés szintje: a hely szerepe a motívum ívében / several levels together: an alternative spelling of Peshat; the level of exposition: the passage’s role in the motif’s arc
- `pardes_szint` = `Remez` (en: `Remez`): az utalás szintje: kereszthivatkozás, párhuzam / the level of allusion: cross-reference, parallel
- `pardes_szint` = `Remez/Drash` (en: `Remez/Drash`): több szint együtt: az utalás szintje: kereszthivatkozás, párhuzam; a kifejtés szintje: a hely szerepe a motívum ívében / several levels together: the level of allusion: cross-reference, parallel; the level of exposition: the passage’s role in the motif’s arc

### `pardes_szint_en`

Az előző oszlop (pardes_szint) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (pardes_szint), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `rovid_cimke`

A motívum rövid megjelenítési címkéje.

*A short display label for the motif.*


### `rovid_cimke_en`

Az előző oszlop (rovid_cimke) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (rovid_cimke): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


### `statusz`

A motívum kidolgozottsága.

*The maturity of the motif entry.*

- `statusz` = `feldolgozás alatt` (en: `in progress`): A motívum nyitott; jelöltjei még minősítetlenek lehetnek. / The motif is open; its candidates may still be unqualified.
- `statusz` = `publikálható` (en: `publishable`): A motívum kidolgozott és kapuzott, de új lexikai bizonyíték vagy szerkesztői szándék újranyithatja. / The motif is worked out and gate-checked, but new lexical evidence or an editorial decision may reopen it.

### `statusz_datum`

A státusz felvételének napja (ÉÉÉÉ.HH.NN).

*The date the status was assigned (YYYY.MM.DD).*


### `statusz_en`

Az előző oszlop (statusz) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás); a `;`-vel összetett érték részenként.

*Short English label of the value in the preceding column (statusz), taken from the codebook (an edited label, not a machine translation); a compound value separated by `;` is labelled part by part.*


### `tema`

Szisztematikus témabesorolás (többértékű lehet); nem része az azonosítónak.

*Systematic subject classification (may be multi-valued); not part of the identifier.*


### `tema_en`

Az előző oszlop (tema) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik (forrás-hash); ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt. Bibliai idézetnél a magyar Károli-szöveg marad, mögötte szögletes zárójelben szó szerinti angol fordítás (nem angol bibliafordítás szövege).

*English counterpart of the text in the preceding column (tema): a **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text (source hash); if the Hungarian text has changed, the cell is empty and `forditas_modja` states the gap. In a biblical quotation the Hungarian Károli text is kept, followed by a literal English rendering in square brackets (not the text of an English Bible translation).*


## sblgnt_apparatus.tsv


### `forras_licenc`

A forrás-adatkészlet licence.

*The licence of the source dataset.*

- `forras_licenc` = `CC BY 4.0` (en: `CC BY 4.0`): Creative Commons Nevezd meg! 4.0 (a forrást meg kell nevezni) / Creative Commons Attribution 4.0 (the source must be credited)

### `forras_licenc_en`

Az előző oszlop (forras_licenc) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás).

*Short English label of the value in the preceding column (forras_licenc), taken from the codebook (an edited label, not a machine translation).*


### `forras_megnevezes`

A forrás olvasói neve; a teljes kötelező megjelölés (SBL Greek New Testament, Copyright 2010 Society of Biblical Literature and Logos Bible Software, CC BY 4.0, sblgnt.com) az OLVASSEL.md-ben áll.

*The reader-facing name of the source; the full required credit (SBL Greek New Testament, Copyright 2010 Society of Biblical Literature and Logos Bible Software, CC BY 4.0, sblgnt.com) is given in README.md.*


### `igehely`

Az igehely, amelyhez az apparátus-jegyzet tartozik: magyar könyvrövidítés és a forrás saját fejezet:vers számozása (nem Károli-átszámozás).

*The passage the apparatus note belongs to: Hungarian book abbreviation and the source’s own chapter:verse numbering (not a Károli renumbering).*


### `igehely_osis`

Az előző oszlop (igehely) igehelye OSIS-kulccsal; a fejezet- és versszám itt a forrás (SBLGNT) saját számozása, nem a Károli-fordításé.

*The passage of the preceding column (igehely) as an OSIS reference; chapter and verse here follow the source’s own (SBLGNT) numbering, not that of the Károli translation.*


### `jegyzet`

Az SBLGNT kritikai apparátusának jegyzete szó szerint a forrásból (az SBLGNT alapszövege nincs a csomagban).

*A note of the critical apparatus of the SBLGNT, verbatim from the source (the SBLGNT base text is not in the package).*


### `motivum_azonosito`

A motívum azonosítója, amelyhez a sor tartozik.

*The identifier of the motif the row belongs to.*


### `sorszam`

A jegyzet sorszáma a vers alatt.

*The running number of the note under the verse.*


## visszhang_megfelelok.tsv


### `alak`

A fordításbeli megfelelő a versben, szó szerint (arámi, latin vagy görög); üres, ha a fordítás a szónak nem ad megfelelőt, vagy a megfelelő nem állapítható meg egyértelműen (a hiányt a sor nem tölti ki).

*The counterpart in the translation, verbatim (Aramaic, Latin or Greek); empty if the translation gives the word no counterpart or none can be identified unambiguously (the gap is not filled in).*


### `betoldas`

A fordítás a lánc szavát olyan láncversbe teszi-e, ahol a héber szövegben nincs (betoldás).

*Whether the translation puts the chain word into a chain verse where the Hebrew text has none (insertion).*

- `betoldas` = `igen` (en: `yes`): igen / yes
- `betoldas` = `nem` (en: `no`): nem / no

### `betoldas_en`

Az előző oszlop (betoldas) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás).

*Short English label of the value in the preceding column (betoldas), taken from the codebook (an edited label, not a machine translation).*


### `datum`

A rögzítés vagy a lekérdezés napja (ÉÉÉÉ-HH-NN); üres, ha nincs rögzítve.

*The date of recording or of the query (YYYY-MM-DD); empty when not recorded.*


### `forditas_modja`

A sor angol párhuzamos mezőinek (`…_en`, szabad szöveg) készítési módja: `gépi fordítás (<modell>)` — a ténylegesen futott modell neve; `…; részben hiányzik` — a sor egyik szabad szöveges mezőjének nincs érvényes fordítása; `nincs fordítás` — egyiknek sincs; üres — a sorban nincs szabad szöveg. A zárt értékek `_en` címkéje nem gépi fordítás, hanem a kódkönyv szerkesztett címkéje.

*How the row’s English parallel fields (`…_en`, free text) were made: `gépi fordítás (<model>)` = machine translation by the model actually run; `…; részben hiányzik` = one free-text field of the row has no valid translation; `nincs fordítás` = none has; empty = the row has no free text. The `_en` labels of closed-vocabulary values are not machine translations but edited codebook labels.*


### `forras`

A megfelelő forrása: az ókori fordítás.

*The source of the counterpart: the ancient translation.*

- `forras` = `lxx` (en: `Septuagint`): a görög Septuaginta (Rahlfs-szöveg) / the Greek Septuagint (Rahlfs text)
- `forras` = `targum` (en: `Targum`): az arámi Targum (Onkelos a Tórához, Jonatán a Prófétákhoz) / the Aramaic Targum (Onkelos on the Torah, Jonathan on the Prophets)
- `forras` = `vulgata` (en: `Vulgate`): a latin Vulgata (Clementina, 1598) / the Latin Vulgate (Clementine, 1598)

### `forras_en`

Az előző oszlop (forras) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás).

*Short English label of the value in the preceding column (forras), taken from the codebook (an edited label, not a machine translation).*


### `forras_licenc`

A forrás-adatkészlet licence.

*The licence of the source dataset.*

- `forras_licenc` = `CC BY 4.0` (en: `CC BY 4.0`): Creative Commons Nevezd meg! 4.0 (a forrást meg kell nevezni) / Creative Commons Attribution 4.0 (the source must be credited)
- `forras_licenc` = `közkincs` (en: `public domain`): közkincs (a mű kora vagy a forrás nyilatkozata miatt) / public domain (by the age of the work or the source’s declaration)

### `forras_licenc_en`

Az előző oszlop (forras_licenc) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás).

*Short English label of the value in the preceding column (forras_licenc), taken from the codebook (an edited label, not a machine translation).*


### `forras_megnevezes`

A forrás olvasói neve (a licenc megnevezésével, ahol a licenc ezt kéri).

*The reader-facing name of the source (including the licence credit where the licence asks for it).*


### `igehely`

A láncvers, Károli-számozással.

*The chain verse, in Károli numbering.*


### `igehely_osis`

Az előző oszlop (igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása; ahol ez eltér a KJV- vagy a STEPBible-számozástól, az OSIS-kulcs a Károli-verset jelöli.

*The passage of the preceding column (igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation; where it differs from the KJV or STEPBible numbering, the key denotes the Károli verse.*


### `jelentes`

A megfelelő rövid magyar jelentése.

*A short Hungarian meaning of the counterpart.*


### `jelentes_en`

Az előző oszlop (jelentes) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik; ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt.

*The English counterpart of the text of the preceding column (jelentes): **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text; if the Hungarian text changed, the cell is empty and `forditas_modja` states the gap.*


### `kiejtes`

Magyaros kiejtés, ahol van (arámi és görög szónál gépi átírás); egyébként üres.

*A Hungarian-style pronunciation where available (machine transliteration for Aramaic and Greek words); otherwise empty.*


### `lemma`

A megfelelő szótári alakja.

*The dictionary form of the counterpart.*


### `megjegyzes`

Legfeljebb egy mondat a sorhoz (mit állít a sor, mire kell vigyázni); üres, ha nincs.

*At most one sentence on the row (what it claims, what to watch for); empty if none.*


### `megjegyzes_en`

Az előző oszlop (megjegyzes) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik; ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt.

*The English counterpart of the text of the preceding column (megjegyzes): **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text; if the Hungarian text changed, the cell is empty and `forditas_modja` states the gap.*


### `motivum_azonosito`

A motívum azonosítója, amelyhez a sor tartozik.

*The identifier of the motif the row belongs to.*


### `strong`

A héber lánc-szó Strong-száma; a betoldás-soroknál a betoldott szóé.

*The Strong number of the Hebrew chain word; for insertion rows, of the inserted word.*


## visszhang_tanuk.tsv


### `datum`

A rögzítés vagy a lekérdezés napja (ÉÉÉÉ-HH-NN); üres, ha nincs rögzítve.

*The date of recording or of the query (YYYY-MM-DD); empty when not recorded.*


### `forditas_modja`

A sor angol párhuzamos mezőinek (`…_en`, szabad szöveg) készítési módja: `gépi fordítás (<modell>)` — a ténylegesen futott modell neve; `…; részben hiányzik` — a sor egyik szabad szöveges mezőjének nincs érvényes fordítása; `nincs fordítás` — egyiknek sincs; üres — a sorban nincs szabad szöveg. A zárt értékek `_en` címkéje nem gépi fordítás, hanem a kódkönyv szerkesztett címkéje.

*How the row’s English parallel fields (`…_en`, free text) were made: `gépi fordítás (<model>)` = machine translation by the model actually run; `…; részben hiányzik` = one free-text field of the row has no valid translation; `nincs fordítás` = none has; empty = the row has no free text. The `_en` labels of closed-vocabulary values are not machine translations but edited codebook labels.*


### `forras`

A tanú adatának forrása.

*The source of the witness data.*

- `forras` = `glossa` (en: `Glossa Ordinaria`): a Glossa Ordinaria jegyzete (Migne, 1880) / a note of the Glossa Ordinaria (Migne, 1880)
- `forras` = `hcf` (en: `HCF database`): a HistoricalChristianFaith-adatbázis metaadata (szerző, mű, kor) és a helyi szöveg olvasása / the metadata of the HistoricalChristianFaith database (author, work, date) and the reading of the passage
- `forras` = `sefaria` (en: `Sefaria`): a Sefaria szövege és adatbázisa (rabbinikus tanú) / the Sefaria text and database (rabbinic witness)

### `forras_en`

Az előző oszlop (forras) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás).

*Short English label of the value in the preceding column (forras), taken from the codebook (an edited label, not a machine translation).*


### `forras_licenc`

A forrás-adatkészlet licence.

*The licence of the source dataset.*

- `forras_licenc` = `CC BY 4.0` (en: `CC BY 4.0`): Creative Commons Nevezd meg! 4.0 (a forrást meg kell nevezni) / Creative Commons Attribution 4.0 (the source must be credited)
- `forras_licenc` = `közkincs` (en: `public domain`): közkincs (a mű kora vagy a forrás nyilatkozata miatt) / public domain (by the age of the work or the source’s declaration)

### `forras_licenc_en`

Az előző oszlop (forras_licenc) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás).

*Short English label of the value in the preceding column (forras_licenc), taken from the codebook (an edited label, not a machine translation).*


### `forras_megnevezes`

A forrás olvasói neve (a licenc megnevezésével, ahol a licenc ezt kéri).

*The reader-facing name of the source (including the licence credit where the licence asks for it).*


### `forras_url`

A forrás nyilvános helye; üres, ha csak az adatbázis megnevezése áll.

*The public location of the source; empty if only the database is named.*


### `hagyomany`

A tanú hagyománya (nyelve).

*The tradition (language) of the witness.*

- `hagyomany` = `gorog` (en: `Greek`): görög nyelvű egyházi hagyomány / Greek-language church tradition
- `hagyomany` = `latin` (en: `Latin`): latin nyelvű egyházi hagyomány / Latin-language church tradition
- `hagyomany` = `rabbinikus` (en: `rabbinic`): rabbinikus hagyomány / rabbinic tradition
- `hagyomany` = `szir` (en: `Syriac`): szír nyelvű egyházi hagyomány / Syriac-language church tradition

### `hagyomany_en`

Az előző oszlop (hagyomany) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás).

*Short English label of the value in the preceding column (hagyomany), taken from the codebook (an edited label, not a machine translation).*


### `igehely`

A motívum helye (Károli-számozással), amelyhez a tanú tartozik.

*The passage of the motif (Károli numbering) the witness belongs to.*


### `igehely_osis`

Az előző oszlop (igehely) igehelye OSIS-kulccsal (pl. 1Kgs.13.31; tartomány: Gen.4.10-Gen.4.11). A könyvkód az OSIS 2.1.1 szabványé, a fejezet- és versszám a Károli-fordítás versszámozása; ahol ez eltér a KJV- vagy a STEPBible-számozástól, az OSIS-kulcs a Károli-verset jelöli.

*The passage of the preceding column (igehely) as an OSIS reference (e.g. 1Kgs.13.31; range: Gen.4.10-Gen.4.11). The book code follows the OSIS 2.1.1 standard; chapter and verse numbers follow the versification of the Károli translation; where it differs from the KJV or STEPBible numbering, the key denotes the Károli verse.*


### `kapcsolat`

Egy mondat, saját szavakkal, idézet nélkül: mit lát a tanú a helyen. A nyers szöveg (idézet) nincs a csomagban.

*One sentence in our own words, without quotation: what the witness sees in the passage. No source text (quotation) is in the package.*


### `kapcsolat_en`

Az előző oszlop (kapcsolat) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik; ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt.

*The English counterpart of the text of the preceding column (kapcsolat): **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text; if the Hungarian text changed, the cell is empty and `forditas_modja` states the gap.*


### `kor`

A forrás szerinti kor (N. sz.); a forrás nélkül üres.

*The date given by the source (century); empty without a source.*


### `motivum_azonosito`

A motívum azonosítója, amelyhez a sor tartozik.

*The identifier of the motif the row belongs to.*


### `mu`

A mű címe a forrás alakjában.

*The title of the work in the form of the source.*


### `tanu`

A tanú: a szerző (magyar névalakkal, ahol van) vagy a rabbinikus mű.

*The witness: the author (with a Hungarian name form where one exists) or the rabbinic work.*


### `tanu_hely`

Ahol a tanú a kapcsolatot teszi: a tárgyalt vers(ek), Károli-számozással, `; `-vel.

*Where the witness makes the connection: the verse(s) discussed, in Károli numbering, separated by `; `.*


## vitatott_forrasok.tsv


### `cim`

A forrás címe.

*The title of the source.*


### `datum`

A rögzítés vagy a lekérdezés napja (ÉÉÉÉ-HH-NN); üres, ha nincs rögzítve.

*The date of recording or of the query (YYYY-MM-DD); empty when not recorded.*


### `doi`

A forrás DOI-ja, ahol van.

*The DOI of the source, where there is one.*


### `ev`

A megjelenés éve.

*The year of publication.*


### `forditas_modja`

A sor angol párhuzamos mezőinek (`…_en`, szabad szöveg) készítési módja: `gépi fordítás (<modell>)` — a ténylegesen futott modell neve; `…; részben hiányzik` — a sor egyik szabad szöveges mezőjének nincs érvényes fordítása; `nincs fordítás` — egyiknek sincs; üres — a sorban nincs szabad szöveg. A zárt értékek `_en` címkéje nem gépi fordítás, hanem a kódkönyv szerkesztett címkéje.

*How the row’s English parallel fields (`…_en`, free text) were made: `gépi fordítás (<model>)` = machine translation by the model actually run; `…; részben hiányzik` = one free-text field of the row has no valid translation; `nincs fordítás` = none has; empty = the row has no free text. The `_en` labels of closed-vocabulary values are not machine translations but edited codebook labels.*


### `megjelenes`

A megjelenés helye (folyóirat vagy kötet, kiadó, oldalszám).

*Where it appeared (journal or volume, publisher, pages).*


### `motivum_azonosito`

A motívum azonosítója, amelyhez a sor tartozik.

*The identifier of the motif the row belongs to.*


### `nyilt_eleres`

Nyílt hozzáférésű-e a forrás (az adatbázis jelzése szerint).

*Whether the source is open access (as flagged by the database).*

- `nyilt_eleres` = `igen` (en: `yes`): igen / yes
- `nyilt_eleres` = `nem` (en: `no`): nem / no

### `nyilt_eleres_en`

Az előző oszlop (nyilt_eleres) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem gépi fordítás).

*Short English label of the value in the preceding column (nyilt_eleres), taken from the codebook (an edited label, not a machine translation).*


### `pont`

A motívum vitatott pontja (a lap „Vitatott pontok” részének címe).

*The disputed point of the motif (the heading in the “Disputed points” part of the page).*


### `pont_en`

Az előző oszlop (pont) szövegének angol párja: **gépi fordítás**, a sor `forditas_modja` oszlopa nevezi meg a modellt. A fordítás a magyar szöveg adott változatához tartozik; ha a magyar szöveg változott, a cella üres, és a `forditas_modja` kimondja a hiányt.

*The English counterpart of the text of the preceding column (pont): **machine translation**; the row’s `forditas_modja` column names the model. The translation belongs to the given version of the Hungarian text; if the Hungarian text changed, the cell is empty and `forditas_modja` states the gap.*


### `szerzo`

A lektorált forrás szerzője; **üres: hiány-sor**, ehhez a ponthoz a kérdésről szóló lektorált forrás a vizsgált adatbázisokban nem került elő.

*The author of the peer-reviewed source; **empty: a gap row**, no peer-reviewed source on the question was found in the databases searched for this point.*


### `url`

A forrás hivatkozása.

*The link to the source.*

