# F99 M2 — a seed-101 újramérés eltéréseinek soronkénti ítélete

*Kézi ítélet a forrásszöveg alapján (`konkordancia/BDB_teljes_unabridged.tsv`, a Strong sora, a szeletelő „lapított” alakjában; a `poz` a
hivatkozás helye), a seed-100 mintájára (`naplok/BDB_SZELETELO_M2_seed100_iteletek.md`). Kategóriák: **szeletelő-hiba**, **kitöltő-hiba**
(csak a forrással bizonyítva), **kulcs-ellentmondás**, **`forras_hiba`**. Az ítélet a mért állapothoz kötődik: kulcs
`naplok/BDB_SZELETELO_M2_minta_seed101_kulcs.tsv` (F99.25-ös tábla), kitöltések `naplok/BDB_SZELETELO_M2_seed101_kitoltott_A.tsv` és
`_B.tsv`, összevetés `naplok/BDB_SZELETELO_M2_seed101_osszevetes.txt` (F99.26). A kapu következménye az ítélet előtt rögzítve: DT-F99l
(F99.27). A szeletelőn a jóváhagyásig nincs javítás. Proveniencia: `scope=seed-101 vak minta | forras=BDB_teljes_unabridged.tsv +
TAHOT_kivonat.tsv (ellenőrzés) | ts=2026-10-15`; az ítélet értelmezés (manual), nem gépi eredmény.*

**Jóváhagyva** (felhasználó, 2026-10-15): az ítéletek; M029 kulcs-ellentmondás marad (a homonima/fő rész kérdés a javítási feladatba); M049, M121 `forras_hiba` (a táblában alkalmazva, F99.29); M092 `orokles_hibas` (a javítási feladatba); a kapu: DT-F99l (c).

## 1. Összesítő

| kategória | jelentéspont (16) | ebből a hely számozott szócikkben | nem számozott (tagolatlan, fej-/alaktani sor, jelöletlen alcímszó) |
|---|---:|---:|---:|
| szeletelő-hiba | **13** | 12 | 1 (M238) |
| kitöltő-hiba (forrással bizonyítva) | **0** | — | — |
| kulcs-ellentmondás | **3** (M008, M011, M029) | 3 | 0 |
| `forras_hiba` | 0 (a jelentéspont-eltérések között nincs) | — | — |

**Könyv/vers** (a felhasználó elfogadta): 0 valódi hiba (M011, M072, M119 rövidítés).

**A kapu kiértékelése (DT-F99l) — JAVASLAT, a jóváhagyás előtt:** 13 szeletelő-hiba > 6, tehát nem (a). A (b) feltétele (a hibák ≥ 2/3-a
nem számozott szócikkben): 1/13 = 8% — **nem teljesül**. A hibák szórtak (7 okcsoport, l. 3. pont) → **(c)**: a tábla „próba” jelöléssel
élesedik, a mért pontosság és intervalluma a lapon látszik (seed-101: jelentéspont 184/200 = 92,0%, Clopper–Pearson 95%: 87,3–95,4%; az
ítélet szerinti 13 szeletelő-hibával 187/200 = 93,5%, 89,1–96,5%); a további szeletelő-javítás külön feladat (brief-tervezet a
/befogad-hoz), a #99-ben nincs több mérési kör. Ha a felhasználó az M029-et szeletelő-hibának ítéli, 14 — a javaslat nem változik.

## 2. Soronkénti ítélet

| azon | Strong | kulcs | kitöltés | forrásidézet (a hely környezete) | számozott? | ítélet | ok |
|---|---|---|---|---|---|---|---|
| M008 | H4519 | `-/1/b` | `-/1/b/(2)/δ` | „γ. מ ׳מַטֵּה … δ. מ שֵׁבֶט ׳חֲצִי Deut 3:13 (D), Josh 13:29; 22:13, 15 (all P)” | igen | **kulcs-ellentmondás** | a görög betűs negyedik szintet (δ) a szabály nem kezeli; a kulcs előtagként helyes |
| M011 | H6485 | `Qal/3` | `Qal/A/3` | „A. 1. a. pay attention to … 3 with עַל person, visit upon … Amos 3:2 … B. appoint: 1 …” | igen | **kulcs-ellentmondás** | a nagybetűs csoportszint (A./B.) nincs az útvonal-formátumban; a 3. pont mindkét olvasatban helyes |
| M028 | H7379 | `-/2` | `-/3` | „2. of public hostilities … 3_39 especially dispute, controversy … Deut 21:5 (+נֶגַע), 25:1” | igen | **szeletelő-hiba** | a gyakoriság-számmal tapadt jelölő („3_39”) nem jelölő |
| M029 | H6440 | `II -/4/e` | `-/4/e`, rész `II` | „II. מְּנֵי with prepositions … 4 לִפְנֵי … e. Of time … Gen 13:10” | igen | **kulcs-ellentmondás** | a „II. פְּנֵי” fej héber címszóval áll (az aranyminta `szakasz` II-ként rögzíti), de a szócikken belüli fő rész is lehet (DT-F99i); a szabály nem dönti el |
| M031 | H5117 | `Qal/2/c` | `Hiph`il/B/2` | „Hiph`il A. Perfect3masculine singular הֵנִיחַ … B. Perfect … הִנִּיחַ … leave or bequeath … Eccl 2:18” | igen | **szeletelő-hiba** | a „Hiph`il A. Perfect” törzsfejléc nem ismert fel (a betűcsoport a törzsnév és a „Perfect” között áll), a Hiph`il a Qal-ba olvad |
| M043 | H8057 | `-/1` | `-/2` | „… malicious joy Ezek 35:15 … 2_46 (especially Psalms Chronicles) religious: … Joel 1:16” | igen | **szeletelő-hiba** | „2_46” — mint M028 |
| M102 | H0559 | `Qal/-` | `Qal/1` | „… see Dr^Expositor, April, 1887, 263.1Say (subject God Gen 3:1 … 1Chr 17:4” | igen | **szeletelő-hiba** | OCR: a „1” a megelőző lapszámhoz és a szóhoz tapad („263.1Say”) |
| M117 | H0539 | `I Niph'al/-` | `I Niph`al/4` | „Deut 28:59. 1.carried by a nurse … 2 made firm … 3 confirmed … 4. verified, confirmed … 93:5” | igen | **szeletelő-hiba** | OCR: „1.carried” (szóköz nélkül); a sorozat nem indul |
| M130 | H8478 | `-/2/a` | `-/2/a`, rész `II` | „— 1 as adverb accusative … Ezek 47:1b II. as preposition; … 2 … a. … Hab 3:16” | igen | **szeletelő-hiba** | a fő tagolás „II.”-je („as preposition”) nem ismert fel: a forrásban nincs „I.”, a `TAGOLAS` I.-gyel kezdődő sorozatot vár |
| M140 | H7626 | `-/2` | `-/1/a` | „(…): 1 rod, staff, club, sceptre. 2 tribe; — ׳שׁ absolute … 2Sam 7:14 … 2 145:tribe” | igen | **szeletelő-hiba** | a fejléc glossza-számozása a szerkezetnek számít; a valódi „2” OCR-torzult („2 145:tribe”) |
| M146 | H7227 | `I fej` | `I -/1/g` | „— 1 (often opposed to מְעַט) a.-1much: … g. as adverb much … HPS^2Sam 22:15” | igen | **szeletelő-hiba** | a zárójellel folytatódó „1 (often …)” jelölő kimarad (csak a gyakoriság-zárójel engedett) |
| M162 | H3318 | `fej` | `Qal/1/a` | „… — 1 go or come out: a. … Hag 2:5; Psa 114:1. b go forth …” (a digitális szövegben a „Qal” fej hiányzik) | igen | **szeletelő-hiba** | törzsnév nélküli első törzs: a jelentésszerkezet (1, a.) a fejbe esik; a forrásban számozás van |
| M203 | H3068 | `-/2/a` | `-/2/a`, rész `II` | „II. 1. … 2 the phrase יהוה אֲנִי is noteworthy: — a. after אמר … Judg 6:10” | igen | **szeletelő-hiba** | a fő tagolás (II.) az angol szövegben nem ismert fel |
| M236 | H5437 | `Qal/1/c` | `Qal/2/c` | „ᵑ0 De and others 2. a. march, or walk, around … c. make a round … — See also 2Sam 5:23” | igen | **szeletelő-hiba** | a kisbetűs szó utáni „2. a.” jelölő kimarad (a laza minta „a” után szóközt vár, nem pontot) |
| M238 | H5608 | `Pu'al/1/b` | `-/1/b` (סֹפֵר) | „… Hab 1:5. סוֺפֵר סֹפֵר, noun masculine^Psa 45:2 enumerator … — 1. a. … b. king's official … Isa 36:3, 22” | **nem** (jelöletlen alcímszó) | **szeletelő-hiba** | a vesszős, két alakú alcímszó („סוֺפֵר סֹפֵר, noun”) nem ismert fel (a vessző csak a „_N” előtt engedett) |
| M243 | H1129 | `Qal/-/i` | `Qal/1/i` | „— build, 1 (literal) a. with accusative … i. = rebuild … Ezra 1:3” | igen | **szeletelő-hiba** | „1 (literal)” — mint M146 |

**Okcsoportok (szórt):** zárójellel vagy „_N”-nel folytatódó jelölő (M028, M043, M146, M243); OCR (M102, M117, M140); törzsfejléc (M031,
M162); fő tagolás (M130, M203); laza „2. a.” (M236); jelöletlen alcímszó (M238); fejléc-glossza (M140).

## 3. A könyv/vers és a szűrés melléklete (nem a jelentéspont-mérce része)

| azon | forrásidézet | ítélet |
|---|---|---|
| M049 H1802 | „— draw (water, but no object expressed) 2:6, 19” (örökölt: Exod) | **`forras_hiba`-jelölt**: a TAHOT a H1802-t a 2Móz 2:16-ban és 2:19-ben hordozza, a 2:6-ban nem; a forrás (2:6 a 2:16 helyett) eldönti — `forras_hiba`, nem szeletelő-hiba |
| M121 H7804 | „suffix יְשֵׁיזְבִנָּךְ 6:17, נְִ֯כבוֺן 3:13” (örökölt: Dan) | **`forras_hiba`-jelölt**: a TAHOT a H7804-et a Dán 3:15-ben hordozza, a 3:13-ban nem — `forras_hiba` |
| M092 H0669 | „א ׳עָרֵי2Chr 17:2; compare 34:6; א ׳שְׂדֵה Obadiah 19; hence ׳א alone in local sense 31:1” | **nem `forras_hiba`**: a forrás helyes (a TAHOT a H0669-et a 2Krón 31:1-ben hordozza); a tábla `orokles_hibas` (bizonytalan), mert az egyfejezetes Abdiás után a 31:1 nem öröklődhet — a közbeékelt egyfejezetes könyv előtti könyv (2Krón) folytatása a szeletelő javítási jelöltje (külön feladat) |
