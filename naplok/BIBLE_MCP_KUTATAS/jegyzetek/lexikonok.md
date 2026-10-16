# A bible-mcp lexikonrétegei (BDB, StrongsHebrew, Abbott-Smith) és értékük a PaRDeS-repó számára

*Állapot: 2026-10-16. Jelölés: **[mért]** = saját lekérdezés vagy szkript, a pontos lekérdezéssel; **[forrás]** = külső dokumentum; **[következtetés]** = értelmezés. A letöltött fájlok a scratchpadben vannak (`…/scratchpad/as_dl/as.xml` = translatable-exegetical-tools v1.0, `as_dl/as2.xml` = biblicalhumanities fork, `mcp_dl/as015.xml` = a bible-mcp saját forrásfájlja), a mérőszkriptek ugyanott: `as_elemez.py`, `as_kulcs.py`, `as_hiany.py`, `as015.py`, `osszevet.py`, `tbesg_as.py`, `thayer_lxx.py` (mind `python -I`, csak olvas).*

## 1. Az Abbott-Smith forrása: valódi szócikkszám, teljesség, verzió, licenc

### Takeaway
A „517 entries” nem elírás: a bible-mcp a **2012-es v0.15 részleges kiadást** (555 `<entry>`) töltötte be, nem a 2017-es v1.0-t (6 153 `<entry>`, kb. 5 416 Strong-kulcsú). A teljes, ellenőrzött v1.0 TEI közkincs, és a repó `adat/licencek.tsv`-je már rögzíti a forrás-commitot (`8c00cb2`, 2024-07-01).

### Cited Findings
- A bible-mcp repójában az Abbott-Smith forrásfájl neve `data/sources/abbott-smith/abbott-smith.v0.15.xml` **[mért]**: `curl https://api.github.com/repos/nirajagarwal/bible-mcp/git/trees/HEAD?recursive=1` → path-lista — [bible-mcp fa](https://github.com/nirajagarwal/bible-mcp)
- A bible-mcp README szó szerint: „Abbott-Smith's Manual Greek Lexicon of the New Testament (1922, 517 entries) … First1KGreek / Open Greek and Latin Project, via github.com/biblicalhumanities/Abbott-Smith | Public Domain” (README 15. sor; utolsó commit 2026-09-28, „Bump to v0.14.1”) — [bible-mcp README](https://raw.githubusercontent.com/nirajagarwal/bible-mcp/master/README.md)
- A v0.15 fájlban 555 `<entry>` van, 571 G-kulcs, tartomány G1–G5613; **0** `type="septuagint"` szegmens, **0** H-számmal kulcsolt héber szó **[mért]**: `python -I as015.py mcp_dl/as015.xml as_dl/as.xml`
- A changelog szerint a v0.15 (2012-12-12) 555 szócikket tartalmazott, a v1.0 (2017-02-03): „The lexicon is complete”; a README: „The work of marking up and checking the text are complete.” — [translatable-exegetical-tools/Abbott-Smith](https://github.com/translatable-exegetical-tools/Abbott-Smith)
- A kanonikus repó (translatable-exegetical-tools) 1 235 commit, utolsó commit 2024-07-01 („epta to hepta”, helmadik PR #114); a biblicalhumanities fork 1 005 commit, utolsó commit 2015-12-02, a README-je még a v0.5-ös „Total entries: 5,726 … much editing remains” állapotot mutatja **[mért]**: GitHub API `commits?per_page=3` mindkét repóra — [kanonikus](https://github.com/translatable-exegetical-tools/Abbott-Smith); [fork](https://github.com/biblicalhumanities/Abbott-Smith)
- A v1.0 `abbott-smith.tei.xml` (5 698 817 bájt): 6 153 `<entry>`, ebből 5 896 `n` attribútummal; 5 441 `n="lemma|G…"` alakú; 455 `n` Strong-szám nélküli (pl. `ἀγγέλλω`, `Ἀβειληνή`, `ἄγγος`); 30 többszörös/betűs kulcs (pl. `ἅγιος|G40|G39`, `αὐτός|G846|G4571|…`, `βαθέως|G0901a`) **[mért]**: `python -I as_kulcs.py as_dl/as.xml`, `as_hiany.py`
- A G1–G5624 tartományból 151 szám nem fordul elő kulcsként; ebből 100 a Strong-számozás üres sávja (G3203–G3302), tehát kb. 51 valódi Strong-szám hiányzik (pl. G90 ἀφθορία, G348, G566, G567, G680, G1400) **[mért]**: `as_hiany.py`
- Licenc: „The lexicon (abbott-smith.tei.xml), including the marked up version in this repository, is in the public domain”; a forrás-PDF-re (archive.org szkennelés) külön korlátozás vonatkozik — [translatable-exegetical-tools/Abbott-Smith README](https://github.com/translatable-exegetical-tools/Abbott-Smith)
- A TEI-fejlécben nincs `<availability>` elem; `<edition>1st</edition>` **[mért]**: `as_kulcs.py`
- A nyomtatott mű: New York, Scribner's, 1922 (előszó: Montreal, 1921. szeptember); a szerző George Abbott-Smith (1864–1947) — [archive.org PDF](https://dn790008.ca.archive.org/0/items/manualgreeklexic00abborich/manualgreeklexic00abborich.pdf); [Logos szerzői oldal](https://www.logos.com/authors/19627) (másodlagos forrás); későbbi kiadások: T&T Clark 1981, 2005 — [enzyklothek](https://enzyklothek.de/en/werk/abbott-smith-1981-%E2%80%93-a-manual-greek-lexicon-d129e2d6-ad2c-4405-822c-746f042a490a)
- A repó már nyilvántartja: `adat/licencek.tsv` 44. sor `MGLNT_lexicon` — „közkincs (Abbott-Smith, 1922 …); az Abbott-Smith digitális kiadása: translatable-exegetical-tools/Abbott-Smith @ 8c00cb244761aa23659421a8cbbbf7a3b27b7d59 (2024-07-01); ellenőrzés 2026-10-04” **[mért]**: `grep -n -i abbott adat/licencek.tsv`
- A bible-mcp `corpus_info` szerint az AbbottSmith réteg „TEI markup from the Open Greek and Latin Project's First1KGreek transcription” — [bible-mcp corpus_info, 2026-10-16]; First1KGreek-beli Abbott-Smith átiratot a keresés nem talált (`First1KGreek Abbott-Smith Manual Greek Lexicon TEI` → csak a két GitHub-repó és könyvtári rekordok).

### Inferences
- A bible-mcp First1KGreek-hivatkozása az Abbott-Smithnél valószínűleg téves átvétel a Swete-LXX sorából (ott a First1KGreek-eredet és a CC BY-SA 4.0 igaz); a tényleges forrás a translatable-exegetical-tools/biblicalhumanities TEI, közkincs-nyilatkozattal. **CC BY-SA nem terheli** az Abbott-Smith TEI-t.
- A nyomtatott 1922-es szöveg az USA-ban (1927 előtti kiadás) és az EU-ban / Magyarországon (szerző †1947, +70 év → 2018. jan. 1-től) is közkincs. A későbbi T&T Clark kiadások esetleges kiegészítései nem tárgyai a TEI-nek (a szkennelés az 1922-es Scribner-kiadás).
- A repó tehát licencszempontból készen áll; a kérdés csak az, ad-e a TEI olyat, amit a TBESG/MGLNT nem.

### Gaps
- A v1.0 TEI-ben nincs gépi teljességi szám a nyomtatott kötet szócikkszámához mérve; a nyomtatott kötet címszószámát forrás nem adja meg.
- A szerző halálozási évére csak a Logos-oldal (másodlagos) támaszt talált a keresés.

## 2. TEI-jelölés: jelentéstagolás (`sense`), „[in LXX for …]” héber ekvivalensek, Strong-kulcs

### Takeaway
A v1.0 TEI **gépileg kinyerhető**: a szócikk-kulcs `lemma|G-szám`, az LXX-ekvivalens külön `<seg type="septuagint">` szegmensben áll, és a héber szavak 97,9%-a `n="H…"` Strong-számot visel; a jelentések egymásba ágyazott, számozott `<sense n="…">` elemek, az igehelyek `osisRef`-esek.

### Cited Findings
- Mintaszócikk (v1.0, `ἔλεος`), szó szerint **[mért]**: `python -I as_hiany.py as_dl/as.xml ἀγγέλλω ἔλεος`
  ```xml
  <entry n="ἔλεος|G1656">
    <note type="occurrencesNT">27</note>
    <form><orth>ἔλεος</orth>, <foreign xml:lang="grc">-ους, τό</foreign></form>
  <etym>
    <seg type="derivation">(cl. <foreign xml:lang="grc">-ου, ὁ</foreign>, and so Rec., …)</seg>
    <seg type="septuagint">[in LXX chiefly for <foreign xml:lang="heb" n="H2617">חֶסֶד</foreign> ;] </seg>
  </etym>
    <sense><gloss>mercy, pity, compassion</gloss>; </sense>
      <sense n="1.">of men: <ref osisRef="Matt.9.13">Mt 9:13</ref> <hi rend="superscript">(LXX)</hi> …
  ```
- `ἀγάπη|G26`: `<seg type="septuagint">[in LXX for <foreign xml:lang="heb" n="H160">אַהֲבָה</foreign>, which is also rendered by <ref><foreign xml:lang="grc">ἀγάπησις</foreign></ref> …]</seg>`; a jelentések `<sense n="1.">` → `<sense n="(a)">` kétszintű fában; a szinonimablokk `<re><emph>SYN.</emph>: …</re>` **[mért]**: `as_elemez.py as_dl/as.xml ἀγάπη πνεῦμα`
- Számok a v1.0-ban **[mért]** (`as_elemez.py`, `as_kulcs.py`): `<seg type="septuagint">` 3 756; `<seg type="derivation">` 2 728; `<sense>` 9 370 (4 821 `n` attribútummal); `<foreign xml:lang="heb">` 5 288, ebből `n="H…"`-val 5 177; `xml:lang="arc"` 70; `<note type="occurrencesNT">` 5 623; `<ref>` 46 431; `<re>` 401; `osisRef`-et tartalmazó szócikk 5 565; LXX-et említő szócikk 3 748; héber betűs szócikk 3 392.
- A biblicalhumanities fork régebbi: `n="H…"`-s héber 4 325 / 5 112, `<entry>` 5 805 **[mért]**: `as_kulcs.py as_dl/as2.xml`.
- A bible-mcp v0.15-ös fájljában az LXX-ekvivalens még a `<form>`-ba ágyazott sima szöveg, H-szám nélkül: `<orth>ζωή, -ῆς, ἡ</orth> (…), [in LXX chiefly for <foreign xml:lang="heb">חַיִּים</foreign>;]` **[mért]**: `as015.py`
- A changelog: v0.11-ben `<def>` → `<gloss>`; v0.5-ben „added Hebrew text to DSAW's entries”; `<etym>` és `<re>` bevezetve — [translatable-exegetical-tools/Abbott-Smith](https://github.com/translatable-exegetical-tools/Abbott-Smith)

### Inferences
- A `seg[@type="septuagint"]/foreign[@xml:lang="heb"]/@n` útvonal egyetlen XPath-tal G→H LXX-megfeleltetési táblát ad (kb. 3 700 görög címszó, ~5 200 héber hivatkozás), Strong-kulccsal mindkét oldalon — ez a hét lépés **6. (LXX-híd)** lépésének lexikográfiai (nem korpusz-alapú) támasza lehetne, `manual`-tól eltérő, `forras=AbbottSmith-TEI@8c00cb2` proveniencia-sorral.
- Az „[in LXX chiefly for X]” állítás Abbott-Smith ítélete (Hatch–Redpath alapján), nem mért korpuszgyakoriság: a repó LXX-hídjában ezért legfeljebb **támasz**, nem a korpuszlekérdezés helyettesítője (3. szabály).

### Gaps
- Nem mértem, hány `n="H…"` érték hibás (pl. rossz homográf); szúrópróba (H2617, H160, H7307, H5046, H7411) helyes volt, de a teljes hibaarány ismeretlen.

## 3. Tartalmi összevetés: Thayer (1889) – Abbott-Smith (1922) – TBESG

### Takeaway
A TBESG **gyakorlatilag a teljes Abbott-Smith-szöveget** hordozza (minden G-kulcsú AS-szócikkhez van TBESG-sor; az LXX-állítások 96,6%-a, a SYN.-blokkok 98%-a, a papirusz-hivatkozások 99,6%-a átment), STEP-alakú igehelyekkel és feloldott rövidítésekkel. Ami elvész: a TEI-szerkezet (`seg type="septuagint"`, jelentésfa (`sense`)) és a héber szavak **H-Strong-kulcsa** (a TBESG-ben csak héber betű áll). A Thayer hosszabb, klasszikus párhuzamokkal, de papiruszanyag nélkül és rendszertelen LXX-adattal.

### Cited Findings
- `tbesg_as.py` **[mért]** (`python -I tbesg_as.py as_dl/as.xml`; TBESG sorok `split('\t')`, kulcs `G\d{4}`):
  - AS G-kulcsú szócikk (első G): 5 416; ebből TBESG-ben is megvan: **5 416** (0 hiányzik).
  - AS-ben LXX-szegmens: 3 664 → TBESG-ben is „in LXX”: 3 541 (96,6%); közülük TBESG-ben héber betű: 3 020.
  - AS-ben SYN. (`<re>`): 393 → TBESG-ben 385.
  - AS-ben papirusz-hivatkozás (MM / VGT / Deiss): 900 → TBESG-ben 896.
  - TBESG sorai, amelyek definíciómezőjében H-szám áll: **18**.
  - TBESG záró forrásjel: `(AS)` 5 695 sor, `(ML)` 1 982 sor, jelöletlen 1 873 sor (összesen 9 550 G-sor, 9 362 különböző 5 jegyű G-kulcs).
- A TBESG saját leírása: „based on the Abbott-Smith definitions … corrected”; ahol AS nem ad definíciót, ott MiddleLiddell vagy STEPBible-tudósok pótolják — `konkordancia/TBESH_TBESG_README.md` 16. sor; `adat/licencek.tsv` 30. sor (TBESG fejléc, CC BY 4.0, STEPBible-Data @ b99716b).
- Négy szócikk egymás mellett **[mért]** (`python -I osszevet.py as_dl/as.xml G1656 G3341 G2347 G3884`; karakterhossz):

  | Strong | Thayer | Abbott-Smith (sima szöveg) | TBESG | megjegyzés |
  |---|---|---|---|---|
  | G1656 ἔλεος | 697 | 682 | 1 463 (HTML-lel) | AS/TBESG: „[in LXX chiefly for חֶסֶד]”, + `עִם חֶסֶד עָשָׂה` Ge 21:23; Thayer: nincs LXX-ekvivalens |
  | G3341 μετάνοια | 1 816 | 465 | 1 027 | AS/TBESG: LXX-előfordulások listája (Pr 14:15, Wi, Si); Thayer: klasszikus párhuzamok (Thuc., Polyb., Plut., Jos.) |
  | G2347 θλῖψις | 1 614 | 773 | 1 607 | mindhárom ad héber ekvivalenst (צָרָה); Thayer bővebb (Vulgata-megfelelők) |
  | G3884 παραλογίζομαι | 363 | 121 | 290 | AS: „רמה pi.” (TEI: `n="H7411"`); TBESG: „רָמָה pi.”, `(AS)` záró jellel |

- A TBESG szövegszinten bővít: „seq.” → „before”, „c.” → „with”, „q.v.” → „which see”, és jelentésszámokat tesz ki (`__1.`, `__2.`), ahol az AS csak tördel (pl. G3884) **[mért]**: `osszevet.py` kimenet.
- Thayer egész fájlra **[mért]** (`python -I thayer_lxx.py`): 5 426 szócikk, átlag 818 karakter; „Sept.”-et említ 1 451; héber betűt tartalmaz 1 610; papirusz/Deissmann/Moulton-említés **5**. AS v1.0: 6 153 szócikk, átlag 228 karakter (a kereszthivatkozó csonkokkal együtt), papirusz-hivatkozás 1 372 helyen (`as_kulcs.py`).
- A repó `lexikonok_nyers/MGLNT.lexicon` (SQLite, `Lexicon(Topic, Definition)`, 5 477 sor) szintén az Abbott-Smith szövege, és a héber szavak helyén **H-szám-hivatkozás** áll: `[in LXX for <ref onclick="lex('H6869')">H6869</ref>, etc.;]` (G2347), `<ref onclick="lex('H7411')">H7411</ref> pi.` (G3884) **[mért]**: `osszevet.py`
- A repó korábbi értékelése: „MGLNT.lexicon | Abbott-Smith szövege, de héber szavak helyett Strong H-szám-hivatkozásokkal | … | Nincs — duplikátum, a meglévő TBESG/Abbott-Smith ugyanezt adja, valódi héber szöveggel” — `konkordancia/Uj_lexikon_fajlok_2026-09-07.md` 25. sor; ugyanígy `Javasolt_gorog_oldal_erositese.md` 67. sor.

### Inferences
- **Új datasetként az Abbott-Smith szövege nem hoz új tartalmat** a TBESG mellé: a TBESG az AS teljes szövegét adja, CC BY 4.0-val, Strong-kulccsal, és a repó már használja. A Thayer funkciója (klasszikus/patrisztikus párhuzam, mélyebb etimológia) továbbra is külön marad; az AS nem helyettesíti, hanem a TBESG-ben már jelen van.
- **Az egyetlen valódi többlet a szerkezet**: (1) a gépi G→H LXX-ekvivalencia Strong-kulccsal (TBESG: héber betű, kulcs nélkül, 18 sor kivétel; MGLNT: H-szám, de HTML-onclickben, szerkezeti jelölés nélkül), (2) a számozott jelentésfa (`sense`), (3) a `occurrencesNT` szám. Ezért ha a projekt bármit átvesz, az **nem lexikon-dataset, hanem egy kinyert táblázat** (pl. `AS_LXX_ekvivalens`: `G-szám | héber H-szám | héber alak | minősítő („chiefly”, „freq.”, „also”) | proveniencia`), a TEI-ből, a `jeloltek.tsv`-t nem kerülve, ha study-sorrá válna.
- Az MGLNT ugyanezt a H-kulcsot hordozza; a TEI előnye vele szemben a tiszta közkincs-nyilatkozat és commit-hash (a lexikonok_nyers modulok licence „tisztázatlan”, `adat/licencek.tsv` 43. sor), valamint a `seg type="septuagint"` határolás (az MGLNT-ben az LXX-zárójel csak szövegminta).

### Gaps
- Nem vizsgáltam, miben „javított” a TBESG az AS-hez képest (a STEPBible nem dokumentálja tételesen); a 123 olyan AS-LXX-szegmens, amely a TBESG-ben nem „in LXX” alakban áll, lehet átfogalmazás vagy elhagyás — egyenként nem néztem meg.

## 4. Lefedettségi teszt a word_study-val

### Takeaway
A bible-mcp-ben élő Abbott-Smith-réteg a 19 próbaszámból **8-at** adott vissza (42%), de ez a minta gyakori szavak felé torzít; a hiányok mind a v0.15-ös forrásfájl hiányai. A v1.0 TEI-ben ugyanebből 18 megvan (G90 mindkettőből hiányzik). A tényleges MCP-lefedettség kb. 517/5 400 ≈ **10%** az ÚSZ-címszókra.

### Cited Findings
- Lekérdezés: `word_study(query=<Strong>, limit=1)`, 2026-10-16 **[mért]**; „van” = a kimenetben `Full entry (AbbottSmith, …)` blokk áll:

  | Strong | lemma | ÚSZ-előf. | MCP AbbottSmith | v0.15 fájl | v1.0 TEI |
  |---|---|---|---|---|---|
  | G3 | Ἀβαδδών | 1 | van (`G0003`) | van | van |
  | G26 | ἀγάπη | 116 | van (korábbi kézi ellenőrzés) | van | van |
  | G3056 | λόγος | – | van (korábbi kézi ellenőrzés) | van | van |
  | G4151 | πνεῦμα | 379 | van (korábbi kézi ellenőrzés) | van | van |
  | G4102 | πίστις | 243 | van | van | van |
  | G4314 | πρός | 700 | van | van | van |
  | G5485 | χάρις | 155 | van | van | van |
  | G2992 | λαός | 142 | van | van | van |
  | G1515 | εἰρήνη | 92 | **nincs** | nincs | van |
  | G1342 | δίκαιος | 79 | **nincs** | nincs | van |
  | G2347 | θλῖψις | 45 | **nincs** | nincs | van |
  | G1656 | ἔλεος | 27 | **nincs** | nincs | van |
  | G3341 | μετάνοια | 22 | **nincs** | nincs | van |
  | G5624 | ὠφέλιμος | 4 | **nincs** | nincs | van |
  | G3499 | νεκρόω | 3 | **nincs** | nincs | van |
  | G3884 | παραλογίζομαι | 2 | **nincs** | nincs | van |
  | G1594 | ἐκνήφω | 1 | **nincs** | nincs | van |
  | G90 | ἀφθορία | 1 | **nincs** | nincs | **nincs** |
  | `ἀγγέλλω` (lemma-lekérdezés; MCP: G518) | ἀγγέλλω | 1 | **nincs** | nincs | van, de Strong-kulcs nélkül (`<entry n="ἀγγέλλω">`) |

  (a „v0.15 / v1.0” oszlop: `python -I as015.py mcp_dl/as015.xml as_dl/as.xml`)
- A v0.15 555 szócikke betűrendben szórt (első `α|G1`, utolsó orth `ὡς`), tehát nem egy betűtartomány, hanem a korai munkafázis válogatása **[mért]**: `as015.py`.
- Az MCP kimenete a TEI `occurrencesNT` számát a szócikk elejére ragasztja („155 χάρις …”), és egy átírói megjegyzést szövegként jelenít meg („Abbott-Smith does not include the article here.”) **[mért]**: `word_study("G5485")`.

### Inferences
- A word_study Abbott-Smith-blokkjának hiánya **nem negatív lelet** (a szó nem „nincs Abbott-Smithben”, csak a v0.15-ben): ugyanaz a csapda, mint az SDBH üres doménje. Élő használatra a görög oldalon a repó TBESG-je mindig jobb.
- A v1.0-ban a Strong-kulcs nélküli 455 szócikk (pl. `ἀγγέλλω`, MCP-ben G518) lemma szerinti illesztést igényelne; a TBESG ezeket már Strong-hoz kötötte.

### Gaps
- A mintavétel nem véletlen (szándékosan gyakorisági sávok szerint); a 10%-os becslés a README 517-es számából és a v0.15 fájl 555 szócikkéből adódik, nem teljes körű MCP-lekérdezésből.

## 5. MCP BDB és StrongsHebrew a repóhoz képest; a betűs homográf-bontás

### Takeaway
A bible-mcp héber lexikonrétegei **ugyanabból az OpenScriptures HebrewLexicon-forrásból** valók, amelyből a repó `Strong_szotar.tsv`, `OSHL_lexikalis_index.tsv` és `OSHL_BDB_igehelyek.tsv` készült; új adatot nem hoznak. A betűs homográf-bontás hasznos jelzés, de a word_study **két különböző betűzési rendszert keveri egy kimenetben** (H2617a a MACULA-ban „shame”, az MCP BDB-blokkjában „goodness”).

### Cited Findings
- A bible-mcp BDB-forrásai: `data/sources/bdb/BrownDriverBriggs.xml`, `HebrewStrong.xml`, `LexicalIndex.xml` **[mért]**: GitHub tree API; a README: „Brown-Driver-Briggs … (1906, 9,290 entries) + Strong's Hebrew Dictionary (1890, revised, 8,674 entries) … including BDB's own lettered homographs (e.g. H2617a "lovingkindness" vs H2617b "reproach")” — [bible-mcp README](https://raw.githubusercontent.com/nirajagarwal/bible-mcp/master/README.md)
- A repó `OSHL_lexikalis_index.tsv` fejléce: „forras: openscriptures/HebrewLexicon @ 21c9add… | LexicalIndex.xml sha256=8f7a605c…”; a H2617-hez két BDB-azonosító tartozik: `698a` („goodness”) és `699a` („shame”) **[mért]**: `grep -P "\tH2617|^H2617" OSHL_lexikalis_index.tsv`
- A repó `Strong_szotar.tsv` forrása: „openscriptures/HebrewLexicon @ 21c9add…; openscriptures/GreekResources @ dd5a2fd…” — `adat/licencek.tsv` 18. sor. A H2617 sora: `H2617	חֶ֫סֶד	chas.de.	főnév, hímnemű	from H2616	kindness` **[mért]**: `grep "^H2617" Strong_szotar.tsv`
- Az MCP StrongsHebrew-blokkja ugyanerre a teljes Strong-definíciót és KJV-fordításlistát adja: „kindness; by implication (towards God) piety; rarely (by opposition) reproof, or (subject.) beauty favour, good deed(-liness, -ness) … reproach, wicked thing.” **[mért]**: `word_study("H2617", limit=1)`
- Az MCP BDB-blokkjai csak jelentés-fejléceket adnak, igehely nélkül, és „base” szóval zárulnak: „רוּחַ 378 n.f. (less oft. m.) breath, wind, spirit breath of mouth or nostrils (33 t.) wind (117 t.) … spirit of God (94 t.) base” **[mért]**: `word_study("H7307", limit=1)`; „חֶ֫סֶד n.m. shame, reproach base” (`word_study("H2617")`).
- A repó ezt a korlátot már rögzítette: `OSHL_BDB_igehelyek` — „KORLÁTOS: 4053 sor, 2815 Strong; a forrás szócikkeinek többsége igehely nélküli vázlat” — `adat/datasetek.tsv` 91. sor.
- Homográf-ütközés **[mért]**: `word_study("H2617a", limit=3)` → „Lemmas: חֶסֶד (H2617a, hbo, 2x) / Gloss range: a.shame (1); [is].a.shame (1) / Distribution: Prov 1, Lev 1” (Lev 20:17, Péld 14:34), ugyanebben a kimenetben „Full entry (BDB, H2617a): חֶ֫סֶד 247 n.m. goodness, kindness …” és „(BDB, H2617b): … shame, reproach”. A MACULA-szóadat betűje tehát a „shame” homográfot jelöli `a`-val, a BDB/LexicalIndex-illesztés `b`-vel.
- A repó TBESH-je a BDB-sorrendet követi: `H2617a … kindness | goodness, kindness, faithfulness`, `H2617b … shame | a reproach, shame` **[mért]**: `grep -E "^H2617" konkordancia/TBESH.txt`

### Inferences
- A **StrongsHebrew** egyetlen lehetséges többlete a teljes Strong-definíció + KJV-fordításlista, amelyet a repó `Strong_szotar.tsv` „Jelentés” mezője (legalábbis a H2617-nél) csak egyszavas glosszra rövidít. Ez a repó saját forrásfájljából (HebrewStrong.xml, már letöltve, 21c9add) is kinyerhető; MCP nem kell hozzá.
- Az **MCP BDB** a repó `BDB_teljes_unabridged.tsv`-jénél és a #107 tervezett `BDB.lexicon`-szakasztáblájánál szegényebb (fejlécek, igehely nélkül, ~700 karakterre vágva). Értéke legfeljebb egy gyors gyökér-/fejléc-áttekintés; adatforrásként nem.
- A **betűs bontás** fogalmilag egyezik a repó homográf-utótagjaival (TBESH `a/b`, OSHL kettős BDB-id), de a word_study-ban a MACULA-betű és a BDB-betű **nem azonos rendszer**: a H2617a-ra érkező „2 előfordulás” a „shame”-szó, a mellé tett BDB „H2617a” a „goodness”. Élő használatnál ezért a homográfot mindig a BDB-azonosítóval (`OSHL_lexikalis_index.tsv`) vagy a TBESH-kulccsal kell rögzíteni, sosem az MCP betűjével.

### Gaps
- Nem mértem tömegesen, hány Strong-számnál tér el a MACULA- és a BDB-betűzés; csak a H2617 dokumentált eset. Egy teljes összevetés (MACULA-lemma betű ↔ LexicalIndex BDB-id) lekérdezést igényelne, amit a word_study nem ad tömegesen.
- Nem ellenőriztem, hogy a `Strong_szotar.tsv` minden sorában rövidített-e a definíció, vagy csak a H2617-nél.

## 6. A word_study élő használatának gyakorlati korlátai

### Takeaway
A word_study a gyors tájékozódásra jó, adatforrásként a repó szabályai szerint nem használható: vágott, proveniencia nélküli, részleges (görög: v0.15), és glossz-lekérdezésnél lemmákat kever.

### Cited Findings
- A szócikk ~700 karakterre vágva, „…” jellel (pl. G4314 πρός: „… of purpose, Mt 26:12, Ro…”; G4102: „… By meton.,…”) **[mért]**: `word_study("G4314")`, `word_study("G4102")`; a tool leírása: „truncated to ~700 chars”.
- A tool saját figyelmeztetése: „Gloss-keyed queries match substrings and may conflate lemmas — prefer Strong's or lemma queries for exact counts” — [bible-mcp word_study leírás, 2026-10-16].
- A kimenetben nincs forrásverzió, commit vagy időbélyeg; a lexikonblokk címkéje csak „(AbbottSmith, G4314)”, „(BDB, H7307)”, „(StrongsHebrew, H2617)” **[mért]**: fenti lekérdezések. A `corpus_info` licencet ad (BDB/StrongsHebrew CC BY 4.0 markup, AbbottSmith Public Domain), verziót nem.
- Az MCP egy szót több Strong-alakban jelöl: „AbbottSmith, G0003” (nullázott) vs. a lekérdezés „G3” **[mért]**: `word_study("G3")`.
- Az Abbott-Smith-blokkban a TEI-ből az `occurrencesNT` szám és átírói jegyzet szövegként keveredik a szócikkbe (G5485) **[mért]**.

### Inferences
- A repó 1. szabálya (proveniencia-sor) miatt word_study-eredmény csak `forras=bible-mcp v0.14.1 word_study | ts=…` kézi sorral, és **nem lexikon-idézetként** kerülhet a naplóba; lexikai állításhoz a repó saját táblái (TBESG, BDB_teljes, OSHL) az irányadók.
- A görög Abbott-Smith-blokk hiánya a word_study-ban rendszeresen előfordul (a v0.15 miatt); üres eredményt explicit „MCP-forráshiány, nem lexikai hiány” jelöléssel kell rögzíteni.
- Összegzett javaslat: (a) **Abbott-Smith mint új lexikon-dataset: nem** (a TBESG lefedi); (b) **Abbott-Smith TEI v1.0-ból kinyert LXX-ekvivalencia-tábla (G→H Strong): igen, megfontolandó** a 6. lépés lexikográfiai támaszaként, közkincs, commit `8c00cb2`; (c) MCP BDB/StrongsHebrew: nincs új adat; a StrongsHebrew teljes definíciója a repó saját HebrewStrong.xml-jéből pótolható; (d) MCP betűs homográf: csak jelzésként, a BDB-id a kanonikus.

### Gaps
- Nem vizsgáltam az MCP `server.py` lexikon-illesztő kódját (pl. hogyan választja a „top-matching word”-öt), így a H2617a-keveredés pontos oka (MACULA-betű ↔ LexicalIndex-betű) a kimenetből következtetett, nem kódból igazolt.
