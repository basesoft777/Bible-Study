<!-- Forrásréteg, kézi szöveg (F167.2, helyőrző tételszám; átnézés: F167.3). A data paper angol kézirata a JOHD Data Paper szerkezetében. Szöveg: claude-opus-5-5, 2026-11-04. Minden szám a `kozlemeny/data_paper/szamok.py` kimenetéből (l. „Number provenance”); a beküldött változatból a „BEKÜLDÉSI SZÖVEG VÉGE” jelölő utáni rész kivehető. A <…> helyőrzőket a szerző tölti ki; amíg helyőrző áll benne, a szöveg nem nyilvános. -->

# A motif-indexed dataset of biblical passages with documented inclusion and exclusion decisions

**Authors:** `<SZERZO>` (`<INTEZMENY>`; ORCID `<ORCID>`)

## Abstract

We describe an open dataset of nine biblical motifs, each defined by a lexical, formulaic or structural feature of the Hebrew or Greek text. It contains 255 occurrence rows and 3,509 verse-level exclusion decisions. Every occurrence names the original-language word or word pair it rests on; every examined but rejected candidate is kept with a categorised reason. Rows carry their source dataset, licence, query type and date; decisions were made in an AI-assisted workflow. Three motifs are fully checked, closed releases; six come from an earlier, less fully checked stage and will be updated in later versions. The data support research on biblical intertextuality, evaluation sets for passage classification with explicit negative examples, and transfer of the method to other corpora.

**Keywords:** biblical motifs; intertextuality; Hebrew Bible; New Testament; Septuagint; negative evidence

**Roles (CRediT):** `<SZERZO>`: `<CREDIT_SZEREPEK>`.

## (1) Overview

### Repository location

`<DOI>` (canonical record: `<KANONIKUS_FORRAS_URL>`)

### Context

The dataset is the open data layer of a long-term, Hungarian-language motif lexicon. A motif is a recurring biblical theme whose identity is tied to a verifiable feature of the original-language text: a word (six motifs, e.g. Sheol/Hades), a fixed phrase (two, e.g. "calling on the name of the LORD", Hebrew *qārāʾ bĕšēm YHWH*) or a recurring pattern of several words (one). Evidence is always the Hebrew or Greek text; the word of the Hungarian Károli translation is display data.

The motifs are at two stages. Three (Sheol/Hades, the pneuma/psychē distinction, "calling on the name") have passed the lexicon's full release procedure: their lexicon pages are released, pass an automated check for reader-facing errors and were reviewed by the author. The other six come from an earlier stage of the project: their data pass the same package gate but await full review and will be updated. The field `feldolgozasi_allapot` records each motif's stage, so users can select the closed material.

Entries may carry a PaRDeS level (Peshat, Remez, Drash, Sod). This is a reception label: it classifies how a passage connects to the motif in terms of the medieval Jewish fourfold reading scheme, not what the biblical author intended. The scope is the biblical corpus (Hebrew Bible, Greek New Testament, Septuagint correspondences); there is no ancient Near Eastern layer, so a missing parallel says nothing about its existence.

Interpretive essays and the printed volume built on these data are a separate product, not part of the dataset.

## (2) Method

### Steps

Each motif is derived in seven steps: (1) the Strong numbers shared by its core passages, with grammatical words filtered out; (2) a semantic-field hypothesis, the only generative step, logged; (3) a full Old and New Testament scan over the STEPBible tagged texts (TAHOT, TAGNT); (4) collocation (two words in one verse); (5) verb-form check; (6) the Septuagint correspondence; (7) agreement with named commentators (product layer only). Steps 1 and 3–6 are deterministic scripts.

No search hit enters the dataset directly. Every candidate passes through a candidate table, where it is accepted or rejected with a stated reason. An empty result is recorded as empty, never filled with associative material.

### Sampling strategy

Before a motif receives an identifier, four questions are answered: what carries its identity; the minimal feature without which a passage does not belong (the negative criterion); whether a passage shared with another motif has a different function there; and whether the motif is a subset of another. Each motif also names the broader concept it would dilute into ("sin" for the spreading consequences of sin). A passage linked only through that concept is excluded: a safeguard against "parallelomania" (Sandmel, 1962). All nine motifs have both fields filled. The motifs follow the research programme; they are not a representative sample.

### Quality control

*Completeness.* For four motifs we compared the occurrence list with three independent nets over the whole canon: Strong numbers (TAHOT, TAGNT), the Károli word, and the verses cited in the Brown–Driver–Briggs and Thayer lexicons. For Sheol/Hades and "calling on the name", no net found a verse that has the defining feature but is missing from the data. For the pneuma/psychē distinction, every verse with the Greek word pair is in the data, as an occurrence or as a decided candidate. For the spreading-consequences motif, the Strong net returned 1,233 verses outside the data: 651 were rejected as a block (a word outside the negative criterion) and 582 await manual review; 12 occurrence verses are found by no net (thematic links, or the word stands elsewhere in a range). That motif is not shown to be complete. In general, the nets test lexical coverage; thematic links fall outside them.

*Exclusions.* There are 418 exclusion rows: 394 single verses and 24 aggregate rows, which stand for 3,115 verses rejected for a shared reason. Together they record 3,509 decisions in 54 reason categories. By number of verses, the largest are: only one of the two words is present (1,713), another lexeme stands in the verse (651), and the same Károli word renders another Hebrew or Greek word (295).

*Verification chain.* (a) A package gate checks internal notation, codebook coverage, licence filtering, reference resolution and byte-identical regeneration (this release: 0 failures, 9 warnings); a reader gate requires zero reader-facing errors on every released lexicon page. (b) A fresh-context AI checker re-verifies each change with its own queries; a second model checks motif boundaries. (c) The three closed motifs have also passed the formal release procedure, with eight recorded visual reviews and 29 corrections approved by the author.

*Limitations.* The six motifs from the earlier stage have not had the release review and may change. All checkers except the author are scripts or language models; there has been no independent expert review and no inter-annotator measurement. 251 of 255 occurrence rows rest on editorial decisions and cannot be reproduced by rerunning one query; 183 Strong assignments were confirmed against TAHOT, 36 fall outside its scope and 36 were not confirmed. The Károli cross-reference table contains copied lists (5,078 suspect source verses); none of its data is included, but 28 exclusion rows were found through it.

*Third-party content.* Rows draw on TAHOT and TAGNT (CC BY 4.0; STEPBible, n.d.), OpenBible.info cross references (CC BY; OpenBible.info, n.d.) and the Károli text of 1908 (public domain by age). Twenty-five sources are excluded (closed project layers, unclear or non-commercial licences, unused CC BY-SA sources). Semantic domains (United Bible Societies, 2023) form a separate CC BY-SA 4.0 layer of 237 rows.

## (3) Dataset description

**Repository name:** `<REPOZITORIUM>`

**Object name:** PaRDeS open core, release 2026-11-04-8029b0fc0ab84836

**Format names and versions:** UTF-8 TSV (tab-separated, no quoting), Markdown, SHA-256 manifest; 17 files, 490,952 bytes. Tables: motifs (9, with processing stage), occurrences (255), inclusion decisions (257), exclusions (418) with group members (3,115), passage links (32), motif links (3), decision log (8), sources and licences (54), codebook (210 entries, Hungarian and English).

**Creation dates:** 2026-08-22 to 2026-11-04

**Dataset creators:** `<SZERZO>`

**Language:** Hungarian (column names and values, with Hebrew and Greek words); codebook in Hungarian and English

**License:** CC BY 4.0 (semantic-domain layer: CC BY-SA 4.0)

**Publication date:** `<KOZZETETEL_DATUMA>`

## (4) Reuse potential

The occurrence and link tables form a graph of passages joined by shared Hebrew or Greek words, with explicit negative evidence, useful for studies of inner-biblical allusion alongside criteria-based approaches (Hays, 1989). Accepted and rejected candidates with reasons can serve as an evaluation set for retrieval or classification, e.g. whether a system separates invoking the divine name from naming. The Károli word recorded for each occurrence, with its identification method and confidence, supports Hungarian reception history. The negative criterion, the broader concept and the three-net completeness test can be transferred to other corpora. Users should note the small sample and the Hungarian column names and values, besides the limitations above.

## AI declaration

The queries are deterministic programs. Inclusion and exclusion decisions were made in sessions assisted by Anthropic Claude language models (models logged per session), each with a stated reason; the dataset contains decisions and short reasons, not model-written interpretive prose. Part of the Károli word alignment is machine output, marked as such. The AI checks described above are model runs. This manuscript was drafted by claude-opus-5-5 from the repository data. No AI tool is an author; `<SZERZO>` reviewed the data and the text and is responsible for both. `<SZERZOI_NYILATKOZAT>`

## Competing interests

The author also publishes a paid product (interpretive entries and a printed volume) built on these data. `<OSSZEFERHETETLENSEG_MEGFOGALMAZAS>`

## Funding statement

`<TAMOGATO>`

## Acknowledgements

`<KOSZONET>`

## References

Hays, R. B. (1989). *Echoes of Scripture in the letters of Paul*. Yale University Press.

OpenBible.info. (n.d.). *Cross references* [Data set]. https://www.openbible.info/labs/cross-references/

Sandmel, S. (1962). Parallelomania. *Journal of Biblical Literature, 81*(1), 1–13. https://doi.org/10.2307/3264821

STEPBible. (n.d.). *STEPBible data: Translators Amalgamated Hebrew OT (TAHOT) and Greek NT (TAGNT)* [Data set]. Tyndale House, Cambridge. https://github.com/STEPBible/STEPBible-Data

United Bible Societies. (2023). *UBS Dictionary of Biblical Hebrew* (v0.9.2) and *UBS Dictionary of New Testament Greek* (v1.1) [Data set]. https://github.com/ubsicap/ubs-open-license

<!-- BEKÜLDÉSI SZÖVEG VÉGE — az alábbi részek a beküldött változatból kivehetők. -->

---

## Number provenance

Every number in the text above comes from one run of `python kozlemeny/data_paper/szamok.py` (2026-11-04), on the closed package `nyilt_mag/` (release `2026-11-04-8029b0fc0ab84836`; the SHA-256 manifest checked on LF-normalised bytes: 15 files, 0 mismatches), except where the source is named otherwise. The key in the first column is the key printed by the script.

| Number in text | Key | Source (file, field) |
|---|---|---|
| 9 motifs; 6 lexical, 2 formulaic, 1 structural | P1.motivum, P1.azonossag | `nyilt_mag/motivumok.tsv`, `azonossag_tipusa` |
| three closed releases, six from the earlier stage | P1.feldolgozasi_allapot | `nyilt_mag/motivumok.tsv`, `feldolgozasi_allapot` (derived from `adat/kiadasok.tsv` and the reader gate `eszkozok/olvasoi_kapu.py` on the released page) |
| both fields filled for all nine | P1.ures_negativ_kriterium = 0, P1.ures_folerendelt = 0 | `nyilt_mag/motivumok.tsv`, `negativ_kriterium`, `folerendelt_fogalom` |
| 255 occurrence rows | P2.elofordulas_sor | `nyilt_mag/elofordulasok.tsv` |
| 251 of 255 editorial decisions | P2.kezi_dontes = 251, P2.lekerdezesbol = 4 | `nyilt_mag/elofordulasok.tsv`, `lekerdezes_tipusa` |
| 183 / 36 / 36 Strong confirmations | P2.igazolas | `nyilt_mag/elofordulasok.tsv`, `igazolas` (TAHOT-igazolt / TAHOT-hatokoron-kivul / nincs) |
| 3,509 verse-level exclusion decisions | P3.kizart_vers_osszesen | 394 single rows + 3,115 verses in aggregate rows |
| 418 / 394 / 24 / 3,115 exclusion rows | P3.kizaras_sor, P3.egyedi_sor, P3.osszesito_sor, P3.csoport_vers | `nyilt_mag/kizarasok.tsv`, `csoport_versszam` |
| 54 reason categories | count of P3.ok lines | `nyilt_mag/kizarasok.tsv`, `kizaras_oka` (with the "(összesítő sor)" suffix removed) |
| 1,713 / 651 / 295 verses by reason | P3.ok | "csak az egyik szó vagy más szó áll a versben" (11 rows), "más szó áll a versben, nem a motívum lexémája" (3 rows), "más szó a Károli-fordításban" (5 rows) |
| 28 exclusion rows via the Károli cross-reference table | P3.keresesi_mod | `nyilt_mag/kizarasok.tsv`, `keresesi_mod` = Károli-kereszthivatkozás |
| 3,115 group members; every aggregate row enumerated | P3.csoport_tabla_sor = 3,115 = P3.csoport_vers; P3.osszesito_tag_nelkul = 0 | `nyilt_mag/kizaras_csoportok.tsv` (after PR #635) |
| 257 inclusion decisions | P4.beepitesi_dontes | `nyilt_mag/beepitesi_dontesek.tsv` |
| 32 / 3 / 8 / 210 rows | P4.kapcsolatok, P4.motivum_kapcsolatok, P4.dontesnaplo, P4.kodkonyv | the files of the same name |
| 237 semantic-domain rows | P4.domen_sor | `nyilt_mag/cc_by_sa_reteg/szemantikai_domenek.tsv` |
| 54 sources; 25 excluded (9 closed project layers / 9 unclear / 3 non-commercial / 4 unused CC BY-SA); 4 sources used in rows | P5.forras_sor, P5.szerep, P5.kizart_ok, P5.hasznalt_forras | `nyilt_mag/forrasok_es_licencek.tsv`, `szerepe_a_csomagban`, `ok` |
| 12 occurrence verses found by no net | P8.HAMART-001 (reverse direction) | `naplok/F123_teljesseg_HAMART-001.md`, 1. Összegzés (thematic rows and range effects) |
| 17 files, 490,952 bytes | P6.fajl, P6.meret_bajt | `nyilt_mag/` (bytes LF-normalised) |
| 2026-08-22 to 2026-11-04 | P6.datum_tartomany | `datum` and `statusz_datum` fields of the package tables |
| release identifier | P0.kiadas | `nyilt_mag/KIADAS.txt` |
| 0 failures, 9 warnings | — | `python eszkozok/nyilt_mag_kapu.py`, run 2026-11-04 in this session; same result in `naplok/NYILT_MAG_jelentes.md` |
| three released motifs | P7.kiadott_motivum | `adat/kiadasok.tsv` (ALVIL-001, ANTROP-001, ISTENTISZT-001) |
| eight visual reviews | P7.atnezes_sor | `adat/lap_atnezesek.tsv` (ALVIL-001 4, ANTROP-001 3, ISTENTISZT-001 1) |
| 29 corrections approved by the author | P7.lapjavitas_sor, P7.lapjavitas_jovahagyta | `adat/lap_javitasok.tsv` (`jovahagyta` = felhasználó in all 29) |
| 1,233 / 651 / 582 / 12 (spreading-consequences motif) | P8.HAMART-001 | `naplok/F123_teljesseg_HAMART-001.md`, 1. Összegzés and Eredmény 1 (the 582 is stated there, not recomputed by the script) |
| no missing verse (Sheol/Hades, "calling on the name") | P8.ALVIL-001, P8.ISTENTISZT-001 | `naplok/F123_teljesseg_ALVIL-001.md`, `…ISTENTISZT-001.md`, 1. Összegzés (motif feature in the deviating verses: 0; reverse direction: 0) |
| Greek pair verses all in data | P8.ANTROP-001 | `naplok/F123_teljesseg_ANTROP-001.md`, 1. Összegzés and Eredmény |
| 5,078 suspect source verses | — | `nyilt_mag/ISMERT_HIBAK.md`, section 1 |

Numbers deliberately not used in the text: the candidate-table status counts (`adat/jeloltek.tsv`, occurrence candidates of the nine motifs: 255 accepted, 416 rejected, 126 open; key P7.jelolt_dontes) — they agree with the package (255 occurrence rows, 416 occurrence-type exclusion rows), and the 129 open candidates of all types are excluded from the package (key P7.nyitva_minden_tipus; `nyilt_mag/OLVASSEL.md`).

## Átírási jegyzet: JDMDH rövid cikk

A *Journal of Data Mining and Digital Humanities* (az összevetés első helye) rövid cikkéhez a következő változik:

1. **Szerkezet.** A JOHD kötött szakaszai (Overview / Method / Dataset description / Reuse potential) helyett szabad tagolású rövid cikk: Bevezetés (a kutatási kérdés: hogyan dokumentálható a negatív döntés motívumkutatásban), Adat és módszer, Eredmények (a teljesség-mérés és a kizárási okok megoszlása táblázatban), Korlátok, Következtetés. A *Dataset description* mezőlistája egy rövid adat-elérhetőségi szakasszá zsugorodik.
2. **Hangsúly.** A JOHD az újrahasznosíthatóságot kéri; a JDMDH-ban a módszer a tárgy: a negatív kritérium és a fölérendelt fogalom mint kizárási eszköz, a három háló mint visszahívás-mérés. A „Quality control” anyaga így a cikk magja lesz, egy táblázattal a négy motívum háló-eredményeiről (a P8 kulcsok).
3. **Terjedelem.** A JOHD 1000–1500 szavas határa helyett a JDMDH rövid cikkének kerete (a pontos szólimitet a beküldés előtt az élő oldalon ellenőrizni kell, a mai összevetés nem rögzítette); a felszabaduló helyre a kizárási okok teljes táblázata és egy kidolgozott példa (a „calling on the name” motívum: elnevezés kontra segítségül hívás) fér.
4. **Ami kimarad vagy rövidül.** A CRediT-sor, az APC-ügy és a *Repository location* külön szakasza; az MI-nyilatkozat és az összeférhetetlenség a folyóirat saját formájában marad.
5. **Ami nem változik.** A számok és a „Number provenance” melléklet; a két rögzített elv (nincs GitHub-URL; csak a nyílt adatmag, a termékréteg legfeljebb egy mondat); a korlátok kimondása.

## Jegyzet: kettős közlés

Készül egy magyar kézirat is (`kezirat_hu.md`, Digitális Bölcsészet, „Labor” rovat). Ugyanaz a mű nem lehet egyszerre két folyóiratnál elbírálás alatt (a JDMDH és az RDJ beküldési feltétele ki is mondja). A két kézirat ezért csak eltérő hangsúllyal és kölcsönös hivatkozással két külön mű: az angol az adatkészletet írja le, a magyar a módszer kizárási eszközeit és a magyar olvasói réteget (a Károli-szót). A számok egy része szükségszerűen közös. Ha a szerkesztőség átfedésnek tekinti, a második közlés csak másodközlésként, mindkét folyóirat tudtával, az elsőre hivatkozva lehetséges.

**Javasolt sorrend** (a döntés a felhasználóé): (1) a nyílt mag letétele (DOI); (2) az angol data paper beküldése a fő csatornára; (3) a magyar kézirat beküldése az angol elfogadása után, a kísérőlevélben a két közlés viszonyát kimondva. Párhuzamos beküldés csak mindkét szerkesztőség előzetes hozzájárulásával. Ha a magyar jelenik meg előbb, az angol Context szakasza egy mondattal hivatkozik rá (`<MAGYAR_KOZLEMENY_HIVATKOZAS>`).

## Kitöltendő helyőrzők (a szerző)

| Helyőrző | Mi kell |
|---|---|
| `<SZERZO>` | szerző(k) neve (a fejlécben, a CRediT-sorban, a Dataset creators és az AI declaration mezőben) |
| `<INTEZMENY>` | affiliáció; független kutatóként „Independent researcher” és helység |
| `<ORCID>` | ORCID-azonosító (a JOHD erősen ajánlja) |
| `<CREDIT_SZEREPEK>` | CRediT-szerepek (javaslat: Conceptualization, Data curation, Methodology, Validation, Writing – review & editing) |
| `<DOI>` | a letét DOI-ja (Zenodo vagy más, a JOHD által elfogadott repozitórium) |
| `<KANONIKUS_FORRAS_URL>` | a kanonikus közzétételi hely (nem GitHub) |
| `<REPOZITORIUM>` | a letéti repozitórium neve |
| `<KOZZETETEL_DATUMA>` | a letét közzétételének napja (ÉÉÉÉ-HH-NN) |
| `<SZERZOI_NYILATKOZAT>` | a szerző saját mondata a felelősségvállalásról (az MI-nyilatkozat mintájára), vagy törlendő |
| `<OSSZEFERHETETLENSEG_MEGFOGALMAZAS>` | a fizetős termék és a nyílt adat viszonyának végleges megfogalmazása |
| `<TAMOGATO>` | finanszírozó és támogatási szám, vagy „This research received no external funding.” |
| `<KOSZONET>` | köszönetnyilvánítás, vagy a szakasz törlése |
| `<MAGYAR_KOZLEMENY_HIVATKOZAS>` | csak ha a magyar közlemény jelenik meg előbb (l. a kettős közlés jegyzetét) |

## Nyitott kérdések

1. **Csoport-taglisták és sorvég:** megoldva a #635-tel (a 3 115 tag a csomagban; `nyilt_mag/** text eol=lf`). A számok a #635 utáni exportból valók.
2. **A Károli-szöveg licence.** A csomag közkincsnek veszi (a mű kora), a felső források nyilatkozatai eltérnek (`adat/licencek.tsv`: a HunKar „Public Domain”, a scrollmapper-tár MIT). A JOHD a harmadik fél tartalmához engedélyt és licencet kér: jogi ellenőrzés.
3. **Az 582 kézi átnézésre váró vers** (HAMART-001) a kézirat szerint nyitott; ha a letét előtt eldől, a Quality control mondata és a szám frissül (a `naplok/F123_teljesseg_HAMART-001.md`-ből, nem a szkriptből jön).
4. **Hivatkozások.** A Hays-kötet oldalszáma és pontos adatai csak másodlagos forrásból ellenőrzöttek (`kozlemeny/HAYS_LEKEPEZES.md`); a STEPBible, OpenBible.info és UBS tételek dátum nélküliek vagy a letöltés napjához kötendők. A BDB és a Thayer a szövegben név szerint áll, de az irodalomjegyzékben nincs (a szólimit miatt); a JOHD-szabály szerint minden hivatkozásnak léteznie kell, ezért beküldés előtt egy forrásellenőrző menet kell.
5. **Folyóirat.** A kézirat a JOHD szerkezetét követi; a választás (az összevetés rangsorában a JDMDH az első) és a beküldés a felhasználóé. JOHD esetén az APC (£1 070) mentességi kérelme a kísérőlevélbe kerül.
6. **Külső lektor.** Nevesített külső lektor ma nincs; ha lesz, a Quality control „Limitations” bekezdése bővül.
7. **Nyelv.** A JOHD nem végez nyelvi lektorálást; angol anyanyelvi átolvasás javasolt. A mezőnevek magyarok: a kódkönyv angol leírása ezt fedi, de egy lektor angol oszlopnév-aliast kérhet.
