# A bible-mcp keresési, szemantikus, fogalomgráf- és kutatási kimenet rétege — értékelés a PaRDeS-módszer szemszögéből

*Kutatói jegyzet, 2026-10-16. Végrehajtó modell: claude-opus-5-5. A repóban csak olvasás történt; egyetlen segédszkript a scratchpadben futott (`teremt.py`, `python -I`, `split('\t')`).*
*Jelölés: **[M]** = mért tény, a pontos lekérdezéssel; **[É]** = értelmezés. Az MCP-hívásoknak nincs URL-jük; forrásként a hívás pontos alakja áll (`bible-mcp:<eszköz>(…)`, ts=2026-10-16). Repóforrásnál a fájlút.*

## 1. kérdés — semantic_search / find_similar / search: mit adnak vissza, determinisztikus-e, verziózott-e; mini-kísérlet a TEREMT-001 és TEREMT-002 motívumon

### Takeaway
A szemantikus réteg a TEREMT-001-en a repó 41 sorából 21-et talált meg 80 találati helyen (pontosság a negatív kritériumra: 26/80 = 33%), **új, a kritériumot teljesítő igehelyet egyet sem**; a repó valódi hiányát (Jób 41:32 תְּהוֹם) a determinisztikus `word_study('H8415')` és a kulcsszavas `search` találta meg, a szemantikus keresés egyik megfogalmazásban sem. A rétegből szerver-oldali verzió nem kérdezhető le, a pontszám csak a `find_similar`-ban látszik, és a modell csak angolul működik — tehát jelölt-generálásra gyenge, negatív próbára és hígulás-tükörnek viszont használható.

### Cited Findings

**A rétegek és a korpusz (mért)**
- [M] A `corpus_info()` 8 bibliai/lexikai réteget (BSB, WEB, LXX = Brenton angol fordítás 1851, LXX-GRC Swete, MACULA-GRC/HEB, BDB, StrongsHebrew, AbbottSmith), ~25 prózai művet (Ágoston, Kempis, Bunyan, apostoli atyák, Iréneusz, Jusztinosz), az Easton-szótárt (2491 szócikk) és **6 projekt-generált „research output” dokumentumot** listáz; a fogalomgráfra: 5673 csomópont, 17 627 fogalom–vers említés, **438 tipizált, kézzel ellenőrzött él és 139 675 mechanikus „associated” él**. — `bible-mcp:corpus_info()`
- [M] A `corpus_info()` **nem ad vissza** index-verziót, embedding-modell nevet, build-dátumot vagy hash-t; az egyetlen dátumszerű adat a research output dokumentumok `date=` mezője (2026-07-17/18) és a forrásszövegek kiadási éve. — `bible-mcp:corpus_info()`
- [M] Az LXX-réteg Swete-szövege (LXX-GRC) a forrás leírása szerint „surface Greek only”, lemma/Strong/morfológia nélkül; Jeremiás, Dániel, Exodus, Jób, Eszter megőrzi a natív LXX fejezet/vers-szerkezetet. — `bible-mcp:corpus_info()`
- [M] A beágyazási modell (bge-small-en-v1.5) **csak angol**, 384 dimenziós, max. 512 token; a modellkártya szerint a BGE-pontszámok kb. 0,6–1 között szóródnak, ezért „a relatív sorrend számít, nem az abszolút érték”, küszöböt saját adatból kell választani; a lekérdezés-prefix v1.5-nél opcionális. — [BAAI/bge-small-en-v1.5 modellkártya](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [M] Nyelvi próba: `semantic_search(query="a mélység vizei a teremtés előtt", kind=verse, top_k=10, hybrid=false)` → 10 találatból 10 zaj (névlisták: 1Krón 1:25, Józs 15:30, Józs 21:14 …; 1Kir 7:44). Magyar lekérdezés használhatatlan. — `bible-mcp:semantic_search(…)`

**Kimeneti alak, rangsor, determinizmus (mért)**
- [M] A `semantic_search` kimenete `[Ref] (VERZIÓ) szöveg` sorok — **pontszám nélkül**; a verzió találatonként BSB, WEB, LXX (Brenton angol) vagy prózai mű. Alapértelmezett `kind` mellett ablak-találat is jön (`[Ezek.31.4–Ezek.31.8]`). — `bible-mcp:semantic_search(query="the deep, the primeval waters before creation", top_k=12)`
- [M] A `find_similar` koszinusz-szerű pontszámot ad (pl. Jer 4:23 → 1Móz 1:2 **0.768**, CONFESSIONS.12.3 0.747, Jel 21:1 0.738; Jón 2:5 → JSir 3:54 0.791), és vegyesen hoz Szentírást és prózát (15-ből 6 Ágoston/Julian a Jer 4:23-nál). — `bible-mcp:find_similar(reference="Jeremiah 4:23", top_k=15)`; `bible-mcp:find_similar(reference="Jonah 2:5", top_k=15)`
- [M] **Determinizmus:** ugyanaz a hívás kétszer (`semantic_search(query="the deep, the primeval waters before creation", kind=verse, top_k=20)`, hybrid=true) **sorrendre és tartalomra azonos** 20 találatot adott ugyanabban a sessionben. — `bible-mcp:semantic_search(…)` ×2
- [M] **A hibrid mód dominál:** ugyanez a lekérdezés `hybrid=false`-szal 20-ból 3 תְּהוֹם-verset ad (1Móz 1:2, Jób 38:30, Péld 8:28), `hybrid=true`-val 9-et. A kulcsszavas `search(query="\"the deep\"", limit=40)` (BSB) 24 találatából 16 תְּהוֹם-vers — köztük a **Jób 41:32**. — `bible-mcp:semantic_search(…, hybrid=false)`; `bible-mcp:search(query="\"the deep\"", limit=40)`
- [M] **Verszám-normalizálási csapdák a kimenetben:** `[Jonah.2.6] (LXX)` = BSB Jón 2:5 (Brenton számozás); a TEREMT-002 lekérdezésben ugyanaz a vers kétszer jön: `[Jer.50.23] (BSB)` és `[Jer.27.23] (LXX)`. — `bible-mcp:semantic_search(…)`

**Mini-kísérlet — alapadat a repóból (mért)**
- [M] `adat/elofordulasok.tsv`: TEREMT-001 = 41 sor (34 ÓSZ, gerinc_elem `H8415`; 7 ÚSZ, `G0012`: Luk 8:31, Róm 10:7, Jel 9:1-2, 9:11, 11:7, 17:8, 20:1-3); TEREMT-002 = 3 sor (`tohu+bohu`: 1Móz 1:2, Jer 4:23, Ézs 34:11). — `C:\Users\bases\Desktop\Bible-Study\adat\elofordulasok.tsv`
- [M] Negatív kritériumok (`adat/motivumok.tsv`): TEREMT-001 — „az igehelynek a תְּהוֹם gyököt kell tartalmaznia (ÚSZ-ben az LXX-közvetített ἄβυσσος megfelelőjét) — tematikus vízkép önmagában (pl. יָם) nem elég”; fölérendelt fogalom: „vízi/kozmikus káosz-képzetek általában”. TEREMT-002 — H8414 + H0922 egy versben; a תֹּהוּ önmagában nem elég (Ézs 40:17, 44:9; 5Móz 32:10, Zsolt 107:40). — `C:\Users\bases\Desktop\Bible-Study\adat\motivumok.tsv` 5. és 11. sor
- [M] A MACULA-alapú `word_study('H8415', limit=40)` 36 előfordulást ad; ezek között a **Jób 41:32 (héb. 41:24)** („one would think the deep had white hair”), amelyet a `get_interlinear('Job 41:32')` is H8415-nek mutat. A repó 41 sora és a `adat/jeloltek.tsv` 111 TEREMT-sora közül egyik sem Jób 41; a `tematikus_lezart/Tehom_tematikus.md`-ben sincs „Jób 41”. — `bible-mcp:word_study(query="H8415", limit=40)`; `bible-mcp:get_interlinear(reference="Job 41:32")`; grep a repón
- [M] A repó TEREMT-001 sorai `TAHOT_kivonat.tsv visszakeresés (eszkozok/f3_2_betoltes.py)` provenienciájúak; a CLAUDE.md szerint a Jób 41 TAHOT-hiányát csak az F84 pótolta (2026.10.) — a hiány keletkezése ezzel konzisztens. — `adat/jeloltek.tsv`; `CLAUDE.md` „Adat-tár”

**Mini-kísérlet — mérés (top_k=20, kind=verse, hybrid=true, ts=2026-10-16)**

| # | Lekérdezés | ismert (repó-sor) | új | új, a negatív kritériumot teljesíti |
|---|---|---|---|---|
| Q1 | `the deep, the primeval waters before creation` | 9 | 11 | 0 |
| Q1′ | ua., `hybrid=false` | 3 | 17 | 0 |
| Q2 | `the fountains of the great deep burst open` | 6 | 14 | 0 |
| Q3 | `God rebukes the sea and leads his people through the depths` | 8 | 12 | 0 |
| Q4 | `the abyss, the bottomless pit where evil spirits are confined` | 3 | 17 | 0 |
| Q5 (TEREMT-002) | `the earth was formless and empty, a desolate void` | 2 (1Móz 1:2, Jer 4:23) | 18 | 0 |

- [M] Q1–Q4 együtt (hibrid, 80 hely): 26 kritérium-teljesítő találat, a repó 41 sorából **21 különböző sor** (51%) került elő; a Jel 9:11, 11:7, 17:8, 20:1-3, Róm 10:7, az 1Móz 49:25, 2Móz 15:5/8, 5Móz 8:7, Jób 38:16, Zsolt 42:7, 71:20, 77:16, 78:15, 107:26, Péld 3:20, 8:24, 8:27, Ez 26:19, 31:15 egyik megfogalmazásban sem jött elő. A Q4 a démoni szóra húzott (1Sám 16:14-15, ApCsel 19:15, Jak 3:16), a Jel 20:1-3 („bottomless pit … bound”) kimaradt. — `bible-mcp:semantic_search(…)` Q1–Q4
- [M] Q5 a TEREMT-002 harmadik tagját (**Ézs 34:11**, „line of chaos … plumb line of emptiness”) nem találta (felidézés 2/3); a 18 új közül a Jób 26:7 („hangs the earth upon nothing”, תֹּהוּ önmagában) éppen a kizárt kategória. — `bible-mcp:semantic_search(query="the earth was formless and empty, a desolate void", kind=verse, top_k=20)`
- [M] Az „új” találatok jellemző héber szava (interlinearral ellenőrizve kettőnél): Zsolt 107:24 = מְצוֹלָה H4688; Ézs 44:27 = צוּלָה H6683, **de az LXX-ben ἀβύσσῳ**. — `bible-mcp:get_interlinear(reference="Psalm 107:24")`; `bible-mcp:get_interlinear(reference="Isaiah 44:27")`

### Inferences
- [É] Az 54 „új” találat zöme a fölérendelt fogalom felé hígul („mély víz” mint szorongás — Zsolt 69:2/14, 18:16; „deep” mint átvitt értelem — Péld 18:4, 20:5, Préd 7:24; tenger-átkelés más szóval — Neh 9:11, Zak 10:11; „pit/בּוֹר” — Zsolt 143:7, Ézs 24:22). Ez pontosan a `motivumok.tsv` fölérendelt fogalma; a szemantikus keresés tehát **a hígulás irányát mutatja meg, nem a motívum határát**.
- [É] A motívum lexikai/formulaikus azonosság-hordozójú; az angol beágyazás a fordítási szóra („deep”) érzékeny, nem a héber lemmára. A BSB a תְּהוֹם-ot és a מְצוֹלָה-t is „deep”-nek fordítja, így a hasonlóság a fordító döntését méri. Lexikai motívumnál a `word_study`/repó-CLI mindig felülmúlja; a szemantikus réteg legfeljebb **fogalmi vagy strukturális** azonosság-hordozójú motívumnál adhat valódi újat — ezt ez a kísérlet nem mérte.
- [É] Mellékhozam: az Ézs 44:27 (צוּלָה → LXX ἄβυσσος) típusú helyek a 6. lépés (LXX-híd) jelöltjei lehetnek — a TEREMT-001 ÓSZ-kritériumán kívül esnek, de az ÚSZ-oldali ἄβυσσος-jelentés hátterét bővítik. Ez a jeloltek.tsv-be való, döntéssel.
- [É] A legértékesebb mért eredmény nem a szemantikából jött: a Jób 41:32 repóhiány. Ez az MCP mint **független kereszt-ellenőrző** szerepét támasztja alá (a repó Strong-scanjének MACULA-val való összevetése), nem a jelölt-generálóét.

### Gaps
- Csak két, lexikai/formulaikus motívumon mértem; fogalmi/strukturális motívumon (ahol a szemantikának esélye van) nincs mérés.
- A `semantic_search` nem ad pontszámot, így küszöb-alapú szűrés és a „mennyire biztos” kérdés nem vizsgálható; a hibrid fúzió módja (RRF? súly?) a szerver kimenetéből nem derül ki.
- A determinizmus csak egy sessionön belül igazolt; index-újraépítés utáni stabilitás nem mérhető, mert verzió nem kérdezhető le.
- A Sir 24:29 („the great deep”) görög szövegét nem ellenőriztem.

## 2. kérdés — A fogalomgráf: tipizált élek lefedettsége, Strong → téma kapcsolatok, „hígulás-tükör”, kockázatok

### Takeaway
A tipizált élréteg ritka és egyenetlen (18 központi fogalomból 4-nek nincs éle, kettő nem is oldható fel), a dokumentált „weight>=10” küszöb a kimenetben nem érvényesül, a névfeloldás csendben téved (`Sea` → „Judgment seat”, `G12` → G129/G1242…), és a keretezés az Easton-szótár 1897-es, református-krisztológiai szemléletét viszi. Hígulás-tükörként az „associated” élek *irányt* mutatnak (a Deep esetén a pokol/eszkatológia felé), de határt nem rajzolnak.

### Cited Findings
- [M] Tipizált élek, `get_concept_relations(name=…)`, alapértelmezett limit=20 (2026-10-16):

| Kérés | Feloldott csomópont | Tipizált élek |
|---|---|---|
| Deep | Deep | 0 |
| Creation | Creation | 2 (causes Heaven w1; is caused by Sovereignty w1) |
| Sacrifice | Sacrifice | 2 (broader than Burnt offering w1, Lamb w1) |
| Atonement | Atonement | 6 (caused by Humiliation of Christ w11; causes Eternal life w10; …) |
| Sin | Sin | 3 (broader than Concupiscence w18, Idolatry w13; **causes Reconcilation** w10) |
| Temple | Temple | 2 (part of Jerusalem w10; broader than Temple, Solomon's w1) |
| Priest | Priest | 0 |
| Sabbath | Sabbath | 1 (narrower than Festivals, Religious w9) |
| Hell | Hell | 3 (symbolized by Fire w11, Furnace w1; contrasts Abraham's bosom w1) |
| Faith | Faith | 2 (causes Justification w3, Assurance w1) |
| Grace | Grace | 1 |
| Messiah | Messiah | 1 (caused by Anoint w4) |
| Resurrection | **Resurrection of Christ** | 3 |
| Flood | — („No concept found”) | — |
| Circumcision | Circumcision | 1 (narrower than Covenant w1) |
| Sea | **Judgment seat** | 0 |
| Abyss | — („No concept found”) | — |
| Kingdom of God | **Kingly office of Christ** | 2 (narrower than Christ w12) |

— `bible-mcp:get_concept_relations(name=<fenti>)`; a korábbi (2026-10-16) szúrópróba: Wilderness 0, Passover: has part Lamb, Bread; Covenant: has part Blood (megbízói kontextus).
- [M] Az eszköz leírása szerint a tipizált élek „hand-reviewed …, weight>=10 only”; a fenti 29 visszaadott tipizált élből **csak 8 éri el a 10-es súlyt**, 21 w1–w9. — `bible-mcp:get_concept_relations` eszközleírás vs. kimenet
- [M] Strong → téma: `get_concept('H8415')` → kulcsszó-csomópont `kw-h8415`, „No definition stored”, szülő téma: **Deep**. `get_concept('G12')` → **nem az ἄβυσσος**, hanem G129 (αἷμα), G1242, G1216, G1228, G1290 (prefix-egyezés); `get_concept('G0012')` → „No concept found”. `get_concept('H8414')` (tohu) → „No concept found”. — `bible-mcp:get_concept(…)`
- [M] `get_concept('Deep', concept_type=theme)`: Easton-definíció négy jelentéssel (sír/abüsszosz; a tenger legmélye; 1Móz 1:2 káosza; feneketlen mélység, pokol), 8 említés (1Móz 1:2, Luk 8:31, Zsolt 69:15, Jel 9:1, 9:2, 11:7, **20:13**, Róm 10:7), 143 associated él. A Jel 20:13 görögje θάλασσα/θάνατος/ᾅδης, ἄβυσσος nincs benne; a Zsolt 69:15 nem תְּהוֹם-vers (nincs a 36 H8415-helyen). — `bible-mcp:get_concept(name="Deep", concept_type="theme")`; `bible-mcp:get_interlinear(reference="Revelation 20:13")`; `bible-mcp:word_study("H8415")`
- [M] A Deep „associated” élei súly szerint: Eternal death 12, Resurrection of Christ 8, Antichrist 8, Hell 7, Pit 6, Resurrection of the dead 6, Angel 6, Furnace 5, Judgment, The final 5, Millennium 5, Creation 4, Astronomy 4, Sadducees 3, Dragon 3, **Hades 3**, Eclipse 3, Devil 3, … Herb 2, Hour 2. — `bible-mcp:get_concept_relations(name="Deep", verb="associated", limit=30)`
- [M] `concepts_in_passage('Genesis 1:2')` → Creation, Deep, Dove, Earth, **Wilderness** (a „Dove” a Szellem-galamb tipológiai olvasat, a „Wilderness” a tohu angol fordításán át). — `bible-mcp:concepts_in_passage(reference="Genesis 1:2")`
- [M] Easton-háttér: Matthew George Easton (1823–1894), skót református presbiteriánus (Reformed Presbyterian, 1876-tól Free Church) lelkész; a szótár 1893-ban jelent meg, a közkézen lévő 3. kiadás 1897 (Thomas Nelson), közkincs. — [Wikipedia: Matthew George Easton](https://en.wikipedia.org/wiki/Matthew_George_Easton); [Wikipedia: Easton's Bible Dictionary](https://en.wikipedia.org/wiki/Easton%27s_Bible_Dictionary)

### Inferences
- [É] **Hígulás-tükör:** a Deep associated-szomszédsága két irányt mutat: (a) pokol/halál/eszkatológia (Eternal death, Hell, Pit, Hades, Antichrist, Millennium) — ez a repó ALVIL-001 (seól/hádész) határa, amelyet a motivumok.tsv már explicit kizárással kezel; (b) teremtés/sötétség (Creation, Darkness, Astronomy). A **tenger/vízi káosz** irány — a repó saját fölérendelt fogalma — hiányzik, mert a `Sea` csomópont nem oldható fel. A tükör tehát hasznos ellenőrző kérdést ad („a motívum nem csúszik-e a Hades felé?”), de nem helyettesíti a 4 kérdést, és vakfoltja ott van, ahol az Easton-anyag hiányos.
- [É] A Deep-téma Easton-horgonyai (8) egyharmada pontatlan (Jel 20:13, Zsolt 69:15), és a téma négy különböző lexémát köt egybe (תְּהוֹם, מְצוֹלָה, ἄβυσσος, ᾅδης-közeli helyek) — azaz *pont az a fölérendelt kategória*, amely felé a PaRDeS-motívum hígulna. Ezért a gráf-téma soha nem lehet motívum-ID forrása; legfeljebb a „fölérendelt fogalom” megnevezésének segédje.
- [É] Keretezési kockázat: a krisztológiai csomópontok (Humiliation of Christ, Kingly office of Christ, Resurrection of Christ) a feloldásban elsőbbséget kapnak (`Kingdom of God` → „Kingly office of Christ”), és „Sin causes Reconcilation” típusú élek a dogmatikai rendszerből, nem a szövegből jönnek. Ha egy motívumcikk ilyen élt idéz, a PaRDeS Peshat/Remez-rétegébe egy 19. századi protestáns dogmatikai olvasat szivárog, provenienciát mutató jelölés nélkül.
- [É] Csendes névfeloldás (`Sea`→Judgment seat, `G12`→G129, `Resurrection`→…of Christ, korábban `Water`→Drawer of water, `Melchizedek`→Melchi) a CLAUDE.md 3. szabályát sérti, ha az eredményt ellenőrzés nélkül veszik át: „nincs él” és „rossz csomópont, nincs él” megkülönböztethetetlen. Minden gráf-lekérdezés után a feloldott csomópont nevét és id-ját naplózni kell, és eltérésnél az eredmény érvénytelen.

### Gaps
- A teljes 438 tipizált él eloszlását nem tudtam lekérni (nincs listázó végpont); a mintavétel 18 kézzel választott fogalomra szól.
- Az „associated” élek képzési szabálya (közös vers? közös Easton-hivatkozás?) a szerver kimenetéből nem állapítható meg; a leírás csak „mechanical shared-evidence edges”-t mond. A DESIGN.md (#5), amelyre az eszköz hivatkozik, nem elérhető ebből a környezetből.

## 3. kérdés — A „research outputs” réteg: mi ez, hogyan készült, miért torzítana a 2. lépés előtt, és mikor biztonságos

### Takeaway
A hat dokumentum (POTTER-, WATER-, WILD- × L0/BRIEF) a szerver saját, LLM-szerű szintézis-folyamatának kimenete („corpus-survey” → „corpus-composer”), ugyanazon korpuszra építve, és a beágyazási indexben ugyanúgy szerepel, mint a Szentírás — tehát egy `semantic_search` észrevétlenül is visszaadhatja. A 2. lépés (mező-hipotézis) előtt olvasva kész mezőt és kész értelmezést kínál; a WILD-BRIEF konkrétan a TEREMT-002 által kizárt „tohu önmagában” kapcsolatot építi be a „pusztaság” témába.

### Cited Findings
- [M] A `corpus_info()` szerint: POTTER-L0 (10 bekezdés, `stage=layer0-raw-survey skill=corpus-survey date=2026-07-18 derived_from=None`), POTTER-BRIEF (25, `stage=layer2-composed skill=corpus-composer derived_from=layer0-raw-survey.md`), WATER-L0 (11, 2026-07-17), WATER-BRIEF (13), WILD-L0 (13), WILD-BRIEF (12); licenc-mező: „Project-generated (research output) (tier A)” — ugyanabban a tierben, mint a közkincs szövegek. — `bible-mcp:corpus_info()`
- [M] A WATER-L0 1. fejezete a szerver eszközeinek kimenetét foglalja össze (BSB-teljesszöveges találatszám, Strong-gyakoriságok: *mayim* 581, *maqor* 18, *be'er* 37, *hydōr* 79), és saját maga jelöli az adat/következtetés határát („that sequencing is corpus data; what to make of it is inference”). Kész „regiszter-térképet” ad (7 funkció: tulajdonvita, rituális oldószer, szerelmi líra, szövetségi per, eszkatologikus földrajz, felkínálás, beteljesedés). — `bible-mcp:read_work(work="WATER-L0", start=1, end=4)`
- [M] A WILD-BRIEF 1.3 bekezdése az 5Móz 32:10 *tohu*-ját összeköti az 1Móz 1:2-vel („*Tohu* is Genesis 1:2's 'formless'; the verse reaches for cosmology”). A repó TEREMT-002 negatív kritériuma ugyanezt az 5Móz 32:10-et név szerint kizárja. — `bible-mcp:read_work(work="WILD-BRIEF", start=1, end=4)`; `adat/motivumok.tsv` 11. sor
- [M] A `semantic_search` leírása szerint a keresés „across the whole corpus — scripture AND prose works”; a `kind` szűrő csak verse/window/paragraph, réteg- vagy dokumentum-kizárás nincs. — `bible-mcp:semantic_search` eszközleírás

### Inferences
- [É] **Torzítás a 2. lépés előtt:** a CLAUDE.md szerint a mező-hipotézis „az egyetlen *generatív* lépés”, és a mező-szavak a naplóba kerülnek. Ha a kutató előbb egy BRIEF-et olvas, a mező-szavak egy része egy másik generatív folyamat terméke lesz, de a napló a kutatóénak tünteti fel — a proveniencia meghamisul. Ráadásul a BRIEF-ek határa tematikus (pl. „emptiness” → midbar + shemamah + tohu), a repó határa lexikai-negatív; az előzetes olvasás éppen a kizárásokat puhítja.
- [É] **Rejtett csatorna:** mivel a research output bekezdések ugyanabban az indexben vannak, egy paragraph- vagy alapértelmezett `kind` szemantikus keresés visszaadhatja őket (a Jer 4:23 `find_similar`-ja 15-ből 6 prózai találatot hozott; ezek ott Ágoston/Julian voltak, de a mechanizmus azonos). A pilotban `kind=verse` kötelező, és minden nem-szentírási ref (POTTER-*, WATER-*, WILD-*) automatikusan kiszűrendő a 2. lépés előtt.
- [É] **Biztonságos használat:** a motívum lezárása után (gerinc, scan, kollokáció, LXX-híd kész; elofordulasok.tsv lezárt), a BRIEF *ellenpróbaként* olvasható: amit a BRIEF a motívumhoz köt, de a repó kizárt, az a kizárás-lista tesztje (ha a kizárás indoklása megáll, a motívum határa erős). A BRIEF állítása így sem kerülhet a motívumcikkbe; ha igen, csak a 7. lépés mintájára, külön fájlban, „másodlagos szintézis, bible-mcp research output, date=…” provenienciával.

### Gaps
- A szintézis-folyamat modelljét, promptjait és a „layer1” köztes réteget a korpusz nem írja le; a `derived_from` mező csak a fájlnevet adja.
- Nem mértem, hogy a research output bekezdések ténylegesen milyen gyakran jönnek elő egy tematikus `semantic_search`-ben.

## 4. kérdés — Milyen proveniencia-sor tenné reprodukálhatóvá a szemantikus lekérdezést? Ad-e verziót a corpus_info?

### Takeaway
Nem ad: a `corpus_info()` sem index-, sem modell-, sem build-verziót nem mond, ezért a szemantikus lekérdezés szerver-oldalon nem reprodukálható; a reprodukálhatóságot csak a lekérdezés teljes paraméterezésének és a **teljes találatlista pillanatképének (hash-sel)** naplózása biztosíthatja. A repó `scope=… | forras=… | ts=…` formátuma bővítendő.

### Cited Findings
- [M] `corpus_info()`: nincs verzió-, hash- vagy dátummező az indexre/beágyazásra; a darabszámok (pl. 139 675 associated él, 438 tipizált él) változása az egyetlen közvetett változásjelző. — `bible-mcp:corpus_info()`
- [M] A `semantic_search` paraméterei: `query`, `top_k` (alap 12), `kind` (alap üres = vegyes), `hybrid` (alap true); a `hybrid` kapcsoló a találatlistát lényegesen megváltoztatja (Q1: 9 vs. 3 תְּהוֹם-vers 20-ból). — `bible-mcp:semantic_search` eszközleírás és Q1/Q1′
- [M] A bge-small-en-v1.5 pontszámai kontextusfüggők, abszolút küszöbként nem értelmezhetők. — [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
- [M] A repó proveniencia-szabálya: „Minden lekérdezésből származó állítás mellé a lekérdezés saját proveniencia-sora kerül (`scope=… | forras=… | ts=…`). Ha nem futott lekérdezés, az érték `manual`.” — `C:\Users\bases\Desktop\Bible-Study\CLAUDE.md`

### Inferences
- [É] Javasolt sor (egy mezőben, a repó elválasztójával):
  `scope=mcp_szemantikus | forras=bible-mcp:semantic_search | q="the fountains of the great deep burst open" | kind=verse | hybrid=true | top_k=20 | modell=bge-small-en-v1.5 (szerver állítása, nem ellenőrizhető) | korpusz_ujjlenyomat=sha1(corpus_info kimenet) | talalat_hash=sha1(rendezett ref-lista) | pillanatkep=naplok/<tétel>_mcp_<n>.tsv | ts=2026-10-16T…`
- [É] A `korpusz_ujjlenyomat` a verzió hiányának pótléka: ha a `corpus_info()` kimenete változik, az index valószínűleg újraépült. A `talalat_hash` + pillanatkép-fájl teszi az eredményt *ellenőrizhetővé* akkor is, ha *újrafuttathatatlan*.
- [É] Gráf-lekérdezésnél kötelező a **feloldott** csomópont neve és id-ja (`kért=Sea | feloldott=Judgment seat (judgment-seat)`), mert a csendes eltérés különben a proveniencia-sorban sem látszik.
- [É] Minden MCP-ből származó jelölt `igazolas` értéke a jeloltek.tsv-ben a determinisztikus repó-CLI újraellenőrzéséig nem lehet „ellenőrizve” — az MCP-sor jelölt-forrás, nem igazolás.

### Gaps
- A szerver ismeretlen; nem tudtam ellenőrizni, hogy van-e rejtett verzió-végpont vagy changelog (a hivatkozott DESIGN.md/ROADMAP.md nem érhető el innen).

## 5. kérdés — Pilot-terv: lépések, metrikák, megállási feltételek

### Takeaway
A pilot egy kérdésre feleljen: *ad-e a bible-mcp a determinisztikus repó-CLI-n túl olyan jelöltet, amely a kizárások után megmarad?* A mai mérés (TEREMT-001/002: 0 ilyen jelölt 100 helyből) alapján lexikai motívumon a várható válasz „nem”; ezért a pilotot egy lexikai kontroll + egy fogalmi/strukturális motívumon kell futtatni, előre rögzített megállási feltételekkel, és az MCP-t a 2. lépés *után* engedni a folyamatba.

### Cited Findings
- [M] A 7 lépés sorrendje és a „nincs közvetlen út” szabály (minden jelölt a `adat/jeloltek.tsv`-n át, döntéssel), valamint a `gerinc_elem` kötelezősége: „ha egy sor nem tudja megnevezni a horgonyát, a jeloltek.tsv-ben marad”. — `C:\Users\bases\Desktop\Bible-Study\CLAUDE.md`; `adat/SEMA.md` 2.2, 2.2.1
- [M] Mai alapvonal: lexikai motívumon a szemantikus keresés felidézése a repó soraihoz 21/41 (Q1–Q4), 2/3 (Q5); kritérium-pontosság 26/80 és 2/20; kizárás után megmaradó új jelölt 0/100; a determinisztikus `word_study` 36/36 + 1 repóhiány. — 1. kérdés mérései

### Inferences
- [É] **Pilot-lépések**
  0. *Előkészítés:* `corpus_info()` ujjlenyomat; két motívum kiválasztása: **kontroll** = TEREMT-001 (lexikai, lezárt); **teszt** = egy fogalmi vagy strukturális azonosság-hordozójú, lezárt motívum a `motivumok.tsv`-ből. A negatív kritérium és a fölérendelt fogalom szó szerint kimásolva a pilot-naplóba, a futás előtt.
  1. *Vakítás:* a 2. lépés mező-szavait a kutató az MCP megnyitása **előtt** rögzíti (commit), research output olvasása tilos.
  2. *Lekérdezés-generálás:* motívumonként 5 angol megfogalmazás, a mező-szavakból képezve (nem a meglévő igehelyekből!), előre a naplóba írva; mindegyik `kind=verse`, `top_k=20`, `hybrid=true` **és** `hybrid=false`; plusz `find_similar` a motívum 3 fő előfordulására (top_k=15). Prózai/research output találat automatikusan levágva, de számolva.
  3. *Normalizálás:* BSB/WEB/LXX ref → Károli-igehely a `Konyv_normalizalo_tabla.tsv`-vel, Brenton-eltérésnél (Jón, Jer, Zsolt) kézi táblázattal; duplikátumok összevonva.
  4. *Osztályozás* minden egyedi versre: **ismert** (elofordulasok.tsv), **ismert-jelölt** (jeloltek.tsv bármely döntéssel), **új**. Az új versek a jeloltek.tsv-be, `proveniencia` = a 4. kérdés szerinti sor, `dontes` üres.
  5. *Kizárás:* az új jelölteket a negatív kritérium és a 4 kérdés szerint, gerinc_elem-megnevezéssel kell elbírálni (`beépítve` / `elvetve` + indoklás). A lexikai feltételt a repó CLI-je igazolja, nem az MCP.
  6. *Független ellenőrzés:* a `fuggetlen-ellenor` a döntések 20%-át vakon újrabírálja.
- [É] **Metrikák**
  - *felidézés* = ismert sorok, amelyeket bármely lekérdezés visszaadott / a motívum összes sora;
  - *kritérium-pontosság* = negatív kritériumot teljesítő találatok / összes találat;
  - *új-arány* = új egyedi versek / összes egyedi vers;
  - **elfogadási arány a kizárások után** = `beépítve` új jelöltek / új jelöltek (a pilot fő metrikája);
  - *zaj-osztályok*: fölérendelt-fogalom-hígulás / fordítási-szó-egyezés / tárgytalan / szomszéd-vers / próza; a hígulás-osztály aránya a „hígulás-tükör” mérőszáma;
  - *költség*: perc / elbírált jelölt.
  - *kereszt-ellenőrzési hozam* (külön sor): a `word_study`/`get_interlinear` hány repóhiányt vagy -hibát mutat ki (mai alapvonal: 1, Jób 41:32).
- [É] **Megállási feltételek** (előre rögzítve)
  - Kontroll-motívumon: ha az elfogadási arány 0, és az MCP egy repón kívüli helyet sem ad, a szemantikus réteg lexikai motívumra **lezárva „nem használjuk”** — csak a kereszt-ellenőrzés marad.
  - Teszt-motívumon: ha 100 elbírált új jelöltből < 3 kerül `beépítve` állapotba, vagy perc/elfogadott jelölt > a repó-CLI scan ugyanilyen mutatójának 3-szorosa → leállítás.
  - Azonnali leállítás, ha (a) egy research output szöveg a 2. lépés előtt bárhol a naplóba került; (b) MCP-sor közvetlenül, jeloltek.tsv nélkül kerülne elofordulasok.tsv-be; (c) a `corpus_info` ujjlenyomata a pilot közben megváltozik (az eredmények nem összemérhetők).
  - Sikeres kimenet: teszt-motívumon ≥ 5% elfogadási arány és legalább egy olyan elfogadott jelölt, amelyet a repó-CLI scan nem hozott — ekkor az MCP a 3. lépés utáni *opcionális* „szemantikus utópróba” lehet, nem a 3. lépés része.
- [É] **Hol van a haszon, hol a veszély — összegzés**
  - *Haszon:* (1) független kereszt-ellenőrzés MACULA/BDB-vel (mért: Jób 41:32); (2) negatív próba — a szemantikus találatlista mint „mi NEM tartozik ide” lista a kizárás-indoklások teszteléséhez; (3) hígulás-tükör a fölérendelt fogalom megnevezéséhez; (4) LXX-híd jelöltek (Ézs 44:27 típus); (5) interoperabilitás: a ref-formátum (`Gen.1.2`) a repó STEPBible-alakjával megegyezik, a normalizáló táblán át illeszthető.
  - *Veszély:* (1) a fordítási szóra épülő hasonlóság lexikai motívumnál álpozitívokkal árasztja el a jeloltek.tsv-t; (2) a 2. lépés előtti használat a mező-hipotézist idegen generatív forrásból tölti; (3) csendes névfeloldás és Easton-horgonyhibák „üres” vagy rossz eredményt adnak, amely leletnek látszik; (4) nincs verzió → az eredmény nem reprodukálható, csak pillanatképként ellenőrizhető; (5) a magyar nyelvű lekérdezés zajt ad, ezért a lekérdezés-fordítás maga is generatív lépés, amelyet naplózni kell.

### Gaps
- Nem futtattam fogalmi/strukturális motívumon; a teszt-motívum kiválasztása a felhasználó döntése.
- A költség-metrika (perc/jelölt) alapvonala a repó-CLI scanre nincs meg ebben a jegyzetben.
