# F186 — A Thayer vers → jelentéspont hozzárendelés mérése és javítása (THAYER_JELENTESPONT_97)

*FELADATOK #186 · végrehajtó: claude-opus-5-5 · ág: `claude/f186-thayer-jelentespont-97` · 2026-11-10*

A mérés a javítás előtt áll. Az 1. szakasz (eljárás és kapu) a seed-201 kitöltése **előtt** került commitba (F186.1).
A későbbi szakaszok a mért eredményeket rögzítik.

## 1. Az eljárás és a kapu (rögzítve a kitöltés előtt)

*Proveniencia: scope=adat/thayer_vers_jelentes.tsv (ÚSZ-sorok) + konkordancia/lexikonok_nyers/Thayer.lexicon |
forras=f186_minta.py (a 7. melléklet forrása) | ts=2026-11-10.*

### 1.1 Mit mérünk

A mért kimenet az `adat/thayer_vers_jelentes.tsv` egy sora: egy Thayer-szócikk egy ÚSZ-hivatkozása (a `bcv`-jelölt
hivatkozás, vagy a `</ref>` utáni jelöletlen folytatás), két mezővel:

- **könyv/vers:** `konyv` + `fejezet:vers` (a hivatkozott hely, Károli-könyvrövidítéssel);
- **jelentéspont:** `utvonal` (`<felső>/<szám>/<betű>`, a felső a nagybetű és a római szám ponttal: `A`, `I`, `A.I`;
  hiányzó szint `-`; különleges: `fej` — az első fej előtti rész, `cim` — a címsor).

A kettőt külön mérjük, külön számmal.

### 1.2 A minta (seed-201; a T4-ben seed-202)

- **Sokaság:** a tábla ÚSZ-sorai (a `konyv` a `Konyv_normalizalo_tabla.tsv` 40–66. könyve): 58 712 sor, 5 352 Strong.
- **Rétegzés gyakori és ritka Strongra:** a Strongok az ÚSZ-sorszámuk szerint csökkenő sorrendben (egyezésnél Strong
  szerint); **gyakori** az a legrövidebb előtag, amelynek kumulált sorszáma eléri a sokaság felét (213 Strong, 29 357
  sor, a küszöb 55 hivatkozás); **ritka** a többi (5 139 Strong, 29 355 sor).
- **Választás:** rétegenként 100 sor, `random.Random(seed).sample` a `(strong, sorszam)` szerint rendezett listán,
  majd a 200 sor ugyanazzal a generátorral keverve; azonosító `T001`–`T200` (seed-202: `U001`–`U200`, a seed-201
  sorai kizárva).
- **Súlyozás:** a két réteg a sokaság egy-egy fele, rétegenként egyenlő mintával, ezért a minta önsúlyozó: a 200 sor
  nyers aránya a sokaság becslése. A rétegenkénti szám tájékoztató.

### 1.3 A kitöltés (vak, két független kéz)

- **Két független kitöltő**, mindkettő Opus (`general-purpose` subagent, `model: opus`): **A** és **B**. A
  terjedelem miatt kitöltőnként két köteg (A1, A2, B1, B2; a köteg Strongonként zárt). A kitöltők egymás
  eredményét nem látják.
- **Vak:** a kitöltő a gépi hozzárendelést (`utvonal`, `konyv`, `fejezet`, `vers`), a szakasztáblát és a kulcsot nem
  látja, és a táblákat nem olvashatja. Amit kap: a munkalap (`azon`, `strong`, a hivatkozás megjelenő szövege,
  környezet) és a szócikkek teljes szövege (a `Thayer.lexicon` HTML-je címkék nélkül, a forrás bekezdéseivel, a mért
  hivatkozás előtt `⟦azon⟧` jelölővel; 40 000 karakter fölött a szöveg az utolsó jelölt bekezdés utáni bekezdésig).
- **Amit kitölt:** `konyv_vers` (Károli-rövidítéssel, pl. `Jn 3:16`; a folytatásnál a láncból feloldva);
  `jelentespont` a fenti formátumban, a szócikk **tényleges tagolása** szerint (a fejek: `A.`, `I.`, `1.`, `a.`; a
  bekezdéshatár nem dönt; a kereszthivatkozásban álló jelölő — pl. „cf. B. 2 c.” — nem fej); `melyebb` (a görög betűs
  vagy mélyebb szint, ha van; nem része a fő mutatónak); `megjegyzes` (bizonytalanság, forráshiba gyanúja).
- **Aki dönt, nem ellenőriz:** a kitöltők döntenek; az eltérések feloldását a végrehajtó végzi a forrásszöveg alapján
  (1.5), a független ellenőrzést a `fuggetlen-ellenor`.

### 1.4 Az összevetés szabályai

- **könyv/vers:** pontos egyezés (könyv + fejezet + vers).
- **jelentéspont, fő mutató:** a három szint (`felső/szám/betű`) pontos egyezése; a `melyebb` szint nem része. Egyenértékű:
  `fej` = `tagolatlan` (a szócikknek nincs fejes tagolása). A `cim` csak `cim`-mel egyezik.
- **`zaro`** (kiegészítés, a kitöltés előtt rögzítve, F186.2): a tagolás után álló, az utolsó jelentésponthoz tartalmilag
  nem tartozó záró rész (pl. szinonima-jegyzet, „[SYNONYMS …]”, összetételek felsorolása) hivatkozása. A gépi kimenetben
  ilyen érték nincs: ha az arany érték `zaro`, a gépi útvonal hibásnak számít.
- **jelentéspont, előtag-mutató (tájékoztató):** a gépi útvonal a kitöltött útvonal előtagja (a gépi durvább, de nem hibás).

### 1.5 Az eltérések feloldása (a BDB seed-101 mintája, `naplok/BDB_SZELETELO_M2_seed101_iteletek.md`)

Arany érték: ha A = B, az; ha A ≠ B, vagy A = B ≠ gépi, soronkénti ítélet a forrásszöveg alapján (idézettel). Kategóriák:
**hozzárendelés-hiba** (a gépi kimenet hibás), **kitöltő-hiba** (csak a forrással bizonyítva), **forrás-hiba** (a
forrás maga hibás, pl. a `bcv` mást mond, mint a megjelenő szöveg — a gépi kimenet hibásnak számít, javítása a
`adat/thayer_forras_javitas.tsv`-be). Az ítéletek az `adat/thayer_aranyminta.tsv`-be kerülnek (a kitöltések, az arany
érték, az ítélet, proveniencia és a tényleges modellnév), és a jelentés 3. szakaszába.

### 1.6 A mutatók és a kapu

- **Mutatók:** a gépi kimenet egyezése az arany értékkel, nyers számmal (x / 200) és **Wilson-féle 95%-os
  konfidencia-intervallummal**, külön a könyv/versre és a jelentéspontra; tájékoztatóul A-ra és B-re külön, és
  rétegenként.
- **A kapu (előre rögzítve):** a jelentéspont **≥ 97%**, azaz **≥ 194 / 200** egyezés az arany értékkel, és a
  könyv/vers is ≥ 194 / 200. A kapu a pontbecslésre vonatkozik; a CI a jelentésben áll.
- **T2 után** a seed-201 újramérése a javított táblán tájékoztató (ugyanazok a sorok, ezért nem független);
  **⛔ T3** csak akkor kell, ha a T2 utáni seed-201 érték 97% alatt marad (költségbecslés, megállás).
- **T4:** új vak mérés (seed-202) ugyanezzel az eljárással; ez a kapu döntő mérése.

## 2. A seed-201 mérés (a javítás előtt)

*Proveniencia: scope=seed-201 (200 ÚSZ-hivatkozás, 163 szócikk) | forras=adat/thayer_vers_jelentes.tsv (a mérés előtti
állapot, ts=2026-10-28) + Thayer.lexicon + négy vak kitöltés (A1, A2, B1, B2; mind `claude-opus-5-5`, külön subagent) + kézi
ítélet (claude-opus-5-5) | ts=2026-11-10. Az összevetést a repón kívüli `f186_osszevet.py` végezte; az ítéletek és a
kitöltések soronként: `adat/thayer_aranyminta.tsv` (`seed = 201`).*

- **A kitöltők egymással:** A és B **mind a 200 sorban** azonos könyv/verset és azonos jelentéspontot adott (eltérés 0).
- **Nyers egyezés a gépi kimenettel:** könyv/vers A: 198/200, B: 198/200; jelentéspont A: 189/200, B: 189/200.
- **Ítélet után (a mért érték):**

| mutató | gépi = arany | arány | Wilson 95% |
|---|---:|---:|---|
| könyv/vers | **200 / 200** | 100,0% | 98,1–100,0 |
| jelentéspont (fő mutató) | **189 / 200** | **94,5%** | 90,4–96,9 |
| jelentéspont, előtagként helyes (tájékoztató) | 192 / 200 | 96,0% | 92,3–98,0 |

- **Rétegenként (tájékoztató):** gyakori — könyv/vers 100/100, jelentéspont 91/100; ritka — könyv/vers 100/100,
  jelentéspont 98/100. A hiba szinte mind a nagy, sokszintű szócikkekben van.
- **A kapu (≥ 194/200): nem teljesül** — a T2 szükséges.

## 3. A seed-201 eltéréseinek ítélete

A 13 eltérő sorban A és B egybehangzóan tért el a gépitől. A forrás nyers HTML-je (`Thayer.lexicon`) alapján:

| azon | Strong | gépi | arany | ítélet | osztály | forrásidézet (rövidítve) |
|---|---|---|---|---|---|---|
| T004 | G4336 | Mt 6:5 · fej | Mt 6:5 · fej | kitöltő-alak | — | „Mat 6:5-7”: a kitöltők tartományt írtak; a tábla a `bcv` kezdőversét adja, a tartomány nincs kibontva (SEMA 2.35) — a gépi helyes |
| T104 | G2344 | Mt 6:19 · -/2/- | Mt 6:19 · -/2/- | kitöltő-alak | — | „Mat 6:19-21”, mint T004 |
| T007 | G3588 | II/5/- | II/5/a | hozzárendelés-hiba | K1 | „**5.** The article prefixed to participles a. gives them the force of substantives …; ὁ ὀλοθρεύων, Heb 11:28” |
| T025 | G3004 | II/1/g | II/1/i | hozzárendelés-hiba | K1 | „…:12. h. with the dative … :18. i.: λέγω followed by prepositions … Joh 2:21” |
| T029 | G3360 | -/1/- | -/1/a | hozzárendelés-hiba | K1 | „**1.** … and is used a. of time: … 1Ti 6:14” |
| T044 | G4487 | -/2/- | -/2/a | hozzárendelés-hiba | K1 | „**2.** In imitation of the Hebrew …; and that a. so far forth as it is a matter of narration: … Act 10:37” |
| T114 | G5479 | fej | -/-/a | hozzárendelés-hiba | K1 | „… joy, gladness; a: Luk 1:14 … 3Jo 1:4” (kettősponttal nyitó „a:”) |
| T147 | G0846 | I/1/e | I/2/a | hozzárendelés-hiba | K1 | „**e.** … Joh 16:27 (…). 2. When it gives Prominence, it answers a. to our emphatic he, she, it: Mat 1:21” |
| T159 | G2228 | -/4/b | -/4/c | hozzárendelés-hiba | K1 | „**b.** ἤ γάρ, see γάρ, I. at the end c. ἤ καί (…) … Luk 11:12” |
| T171 | G3367 | fej | -/-/a | hozzárendelés-hiba | K1 | „… in the same constructions as μή; accordingly a. with an imperative: … Luk 9:3” |
| T191 | G2192 | I/2/g | I/2/h | hozzárendelés-hiba | K1 | „… Joh 15:22, etc. h. of age and time: … Mar 3:26” |
| T145 | G4151 | -/4/b | -/4/a | hozzárendelés-hiba | K2 | „**b.** bb.; γεννάω, 1 at the end and 2 d.; ἐκχέω b.; χρίω, a.) …” — a bekezdés eleji félkövér „b.” egy kereszthivatkozás („βαπτίζω, II. b. bb.”) töredéke; a valódi „b.” a következő bekezdés |
| T181 | G2513 | -/-/d | zaro | hozzárendelés-hiba | K3 | „**d.** in a levitical and ethical sense: … (Synonym: see εἰλικρινής; cf. Westcott on 1Jo 3:3.)” |

**Kitöltő-hiba: 0; forrás-hiba: 0** (a T119 G0027 „Luk 8:18” gyanúját mindkét kitöltő jelezte — „Ascensio Isa. … Luk 7:23;
Luk 8:18” —, de a jelentéspont `fej` és a könyv/vers a forrás `bcv`-je szerint egyezik; a forrás itt valószínűleg az
Ézsaiás mennybemenetelét Lukácsnak jelöli. Ez a `bcv` tartalmi hibája, nem a hozzárendelésé; N-tétel jelölt, l. 6.).

**Hibaosztályok (11 hiba):**

- **K1 — bekezdésen belüli fej (9: T007, T025, T029, T044, T114, T147, T159, T171, T191).** A `bont.py` feltevése („a
  forrásban bekezdésen belüli fej nem fordul elő”) csak a félkövér (`<b>…</b>`) fejekre igaz. A forrás a bekezdés
  belsejében félkövér nélkül is nyit pontot: betűt („used a. of time”, „that a. so far”, „; a:”, „etc. h. of age”,
  „:12. h. with”, „:18. i.:”, „at the end c. ἤ καί”) és számot („). 2. When it gives Prominence, it answers a.”).
- **K2 — hamis bekezdés-eleji fej (1: T145).** A forrás a kereszthivatkozás közepén bekezdést tör, és a töredék eleje
  félkövér betűként áll („**b.** bb.;”). Ugyanilyen a G1909 B/2 „**c.**)):”, „**d.**):”, „**e.**):” bekezdései.
- **K3 — záró szinonima-jegyzet (1: T181).** A „(Synonym: …)” a szócikk végén a teljes szóra vonatkozik, a gépi kimenet
  az utolsó alpontra teszi.

## 4. T2 — javítás hibaosztályonként

*Proveniencia: scope=eszkozok/thayer_jelolt/bont.py, a teljes Thayer (5 426 szócikk) | forras=Thayer.lexicon + a seed-201
aranyminta | ts=2026-11-10.*

**K2 — hamis bekezdés-eleji fej** (`bont.fej_felismer`, `HAMIS_FEJ_UTAN`): a bekezdés eleji félkövér szám/betű nem fej, ha
közvetlenül „)”, „,”, „;”, „]” vagy kettőzött betű („bb.”) követi. A teljes korpuszon **20 bekezdés** (pl. G0575 „c.; Winers
Grammar …”, G1519 „b. aa.); …”, G1909 öt bekezdése, G2532 három). Ezek a bekezdések az előző útvonalat öröklik, és a
belső-fej keresés a jelölőjüket kihagyja.

**K1 — bekezdésen belüli fej** (`bont.belso_fejek`): a bekezdés belsejében álló kisbetű (`a.`, `a:`, `i.:`) vagy szám (`2.`)
fej, ha (1) a sorrendben várt következő jelölő, és (2) nem hivatkozás vagy rövidítés. A kizárások a teljes korpusz jelöltjeinek
átnézéséből (két véletlen 40-es minta és mind a 16 számfej): betű után szám („h. a. 5, 19” — Historia animalium), egybetűs
rövidítés („a. d. Heb”, „b. g. 1”, „i. e.”, „e. g.”), „below/above/at the end”, „)”, „,”, „;”; betű előtt „,”, számjegy, „§”,
„(” vagy rövidítés/utalás („cf.”, „see”, „to”, „p.”, római szám); szám után római szám („1. ix. quaest.”), szám előtt
egybetűs rövidítés („orac. def. c. 1.”, „§ 27, 6 N. 1.”). Fejnél a bekezdés **kettéválik** (egy sor = egy szakasz), így
a `vers_jelentes.py` (amely a `bont.szerkezet`-et használja) változtatás nélkül követi, és a szakasztábla jelentésfája is
tartalmazza az új pontot.

- **A korpuszon:** 181 belső fej 132 szócikkben; a szakasztábla 17 093 → **17 266 sor** (+173; 124 Strong). Az illesztés
  változatlan (`egyezik` 5 411, `javitassal` 15): a vágás a szöveget nem rontja.
- **A becsült pontosság:** a 40-es véletlen mintában (a végleges szabállyal) nincs nyilvánvaló hamis fej; a számfejek közül
  a két hamisat (G0855, G0896) a végleges szabály kizárja, a G4525 kétes „I. 2. metaphorically”-t is (konzervatív).
- **K3 (záró szinonima-jegyzet, T181): nem javítva.** A javítás új `utvonal`-értéket (`zaro`) kívánna, amelyet a tábla
  fogyasztói (a lapgenerátor, a #187 kártyája) is kezelnének — ezek nincsenek az `ir`-ben. Nyitott kérdés (6.).
- **Forráshiba: nincs mért.** A `adat/thayer_forras_javitas.tsv` adattartalma nem változott, csak két sor `sorszam`-a
  (G0575 12 → 13, G0846 19 → 23) a szakaszok újraszámozása miatt (a tábla generált, újragenerálva).
- **Tesztek:** `teszt_bont.py` `F186Fejek` (a K1 öt alakja a seed-201 eseteiből, kilenc negatív alak, a sorrend, a K2);
  `teszt_vers_jelentes.py` `Aranyminta` (a K1 kilenc és a K2 egy sora a mai táblán; minden nem K3 aranysor egyezik; a vers-sor
  `szakasz`-ának útvonala a sor útvonala). A `teszt_bont.py` három régi tesztje („egy sor = egy bekezdés”) az új szabályhoz
  igazítva: a sorok a `szerkezet` szakaszai, és a szakaszok szövege bekezdésenként összefűzve a bekezdés szövege.
- **A seed-201 a javított táblán (tájékoztató, nem független):** könyv/vers 200/200; jelentéspont **199/200** (99,5%,
  Wilson 97,2–99,9); a maradék a K3 (T181). A **⛔ T3 nem szükséges** (a T2 utáni érték ≥ 97%).
- **Mellékes javítás:** a `bont.py` fejléc-literáljában a kiosztott helyőrző (`DT-F132a`, `DT-F132i`) a kiosztott számra írva
  (DT327, DT333; a CI E32 szabálya), így a tábla fejléce a régivel azonos szöveget ad.

## 5. T4 — új vak mérés (seed-202, a javított táblán)

*Proveniencia: scope=seed-202 (200 ÚSZ-hivatkozás, 159 szócikk; a seed-201 sorai kizárva) | forras=adat/thayer_vers_jelentes.tsv
(a T2 utáni állapot, F186.4, ts=2026-11-10) + Thayer.lexicon + négy vak kitöltés (A1, A2, B1, B2; mind `claude-opus-5-5`,
külön subagent, ugyanazzal az utasítással, mint a seed-201) + kézi ítélet (claude-opus-5-5) | ts=2026-11-10. Soronként:
`adat/thayer_aranyminta.tsv` (`seed = 202`).*

- **A kitöltők egymással:** megint **mind a 200 sorban** azonosak.
- **Ítélet után (a mért érték):**

| mutató | gépi = arany | arány | Wilson 95% |
|---|---:|---:|---|
| könyv/vers | **200 / 200** | 100,0% | 98,1–100,0 |
| jelentéspont (fő mutató) | **192 / 200** | **96,0%** | 92,3–98,0 |
| jelentéspont, előtagként helyes (tájékoztató) | 195 / 200 | 97,5% | 94,3–98,9 |

- **Rétegenként:** gyakori — jelentéspont 92/100; ritka — 100/100.
- **A kapu (≥ 194/200): NEM teljesül** (192/200). A könyv/vers teljesül.

**Az eltérések ítélete (8 sor; kitöltő-hiba 0):**

| azon | Strong | gépi | arany | ítélet | osztály | forrásidézet (rövidítve) |
|---|---|---|---|---|---|---|
| U009 | G4314 | I/1/- | I/1/a | hozzárendelés-hiba | K1b | „… πρός τινα or τί, a. properly, after verbs of going … Luk 7:4” — a „,” utáni belső „a.”-t a T2-szabály kizárta |
| U034 | G4396 | II/1/- | II/1/a | hozzárendelés-hiba | K1b | „The title is applied to a. the O. T. prophets … Heb 1:1” — a „to” utáni „a.”-t a T2-szabály kizárta |
| U180 | G4396 | II/1/- | II/1/a | hozzárendelés-hiba | K1b | ugyanaz a hely, „… Luk 10:24” |
| U140 | G2307 | fej | -/-/a | hozzárendelés-hiba | K1b | „will, i. e., a. what one wishes … 1Pe 4:2” — az „i. e.,” utáni „a.” |
| U036 | G3004 | II/1/i | II/1/k | hozzárendelés-hiba | K1c | „… Joh 8:26 (…). k. with adverbs … 1Co 9:8” — a forrás a „j”-t kihagyja (i → k) |
| U165 | G2192 | I/2/i | I/2/k | hozzárendelés-hiba | K1c | „… Rom 15:17. k. ἔχειν τί is used … 1Co 7:25” — i → k |
| U014 | G1519 | B.II/3/d | B.II/3/c | hozzárendelés-hiba | K2b | „**d.** at the end): Luk 20:20 R G; … 2Th 2:2” — a bekezdés eleji „d.” kereszthivatkozás-töredék („… d. at the end)”) |
| U049 | G3004 | -/4/- | -/5/- | forrás-hiba | K4 | „… (Buttmann, 237 (204)). 5 B a Hebraism εἰπεῖν ἐν ἑαυτῷ … Luk 12:45” — az 5. pont jelölője a forrásban torzult („5 B a” = „5. By a”) |

**Értékelés.** A hibák a T2 osztályainak folytatásai: a K1 kizáró szabályai két helyen túl szigorúak (K1b: „,” és „to”
előzmény), a Thayer betűsora a „j”-t kihagyja (K1c), a K2 egy további alakja („**d.** at the end)”: K2b), és egy
forrás-torzulás (K4). A hiba most is a gyakori rétegben van (a nagy, sokszintű szócikkek).

**⛔ Megállás.** A seed-202 eseteire hangolt javítás után a seed-202 már nem független mérés: a kapu igazolásához új vak minta
(seed-203) kellene, ami nem része a briefnek. A döntés az orkesztrátoré (6.3, DT-F186a). Tájékoztatóul egy **repón
kívüli, nem commitolt prototípus** (`f186_proto.py`, memóriában felülírt szabály: a „,” és a „to” kizárás helyett a nyitott
zárójelen belüli jelölő nem fej; i után k is; a K2 alakja „at the end)/above)/below)”-val bővítve) a két aranymintán
**199/200** (seed-201) és **198/200** (seed-202; maradék: U014, U049) értéket ad, a korpuszon 239 belső fejet (167 Strong,
17 324 szakasz), és a 40-es véletlen korpuszmintában 2 hamis fejet („I. 1 a. and c.”, „Brief an d. Heb”) mutat — ezek
további kizárást kívánnak. A prototípus nem mérés; a T3 (modelles döntés) nem szükséges, ha a második szabálykör a seed-203-on
≥ 97%.

## 6. A megváltozott szakaszkulcsok és a #7-re gyakorolt hatás

### 6.1 A megváltozott Thayer-szakaszkulcsok

*Proveniencia: scope=adat/thayer_szakaszok.tsv, a F186.3 (6289c687) és a F186.4 utáni állapot összevetése | forras=f186_lista_md.py
(repón kívül) | ts=2026-11-10.*

A kulcs (`strong` + `sorszam`) megváltozott, ha az adott sorszámon álló szakasz útvonala, jele vagy szövege eltér, vagy a sor új.
**140 Strong, 1 009 kulcs**: 173 új sor (bekezdésen belüli fejnél nyíló szakasz), 706 szöveg- és útvonal-változás (a vágás utáni
sorszám-eltolódás), 130 csak szöveg/jel-változás (a vágott bekezdés első része és a K2-bekezdések). Csak útvonal-változás (azonos
szöveg és jel mellett) nincs. A tételes lista Strongonként: 8. melléklet, A tábla.

### 6.2 A #7 (és a #153, #158) érintett fordítássorai — a meglévő mechanizmus

**A mechanizmus** (a kódból kiderítve):

- az `adat/forditasok.tsv` Thayer-sora szakaszonként `jelentes_szam = sz<n>`, `forras_hash` = a szakasz (`jel` + javított
  `szoveg`) SHA-1-e (`thayer_jelolt/thayer_bemenet.szakaszok`, `forditas.py rogzit`);
- a **jelzés** automatikus: `eszkozok/thayer_jelolt/szolista.py` az eltérő hash-ű Strongot `forditando` / `elavult_hash`
  okkal listázza, az `eszkozok/ellenoriz.py` **13. szabálya** SÉRTÉS-ként jelzi, `allapot=elavult` javaslattal (a táblát nem
  írja);
- az **`elavult` állapotot** külön parancs nem állítja: az újrafordítás (`forditas.py rogzit` → `beir`) ugyanazon a kulcson
  felülírja a sort (a `beir` csak a régi `teljes` sort teszi `elavult`-tá).

**A hatás (mért):** a változtatás előtt a 13. szabály RENDBEN volt; a T2 után **SÉRTÉS, 694 tétel**: **636 hash-eltérő `sz<n>`
sor 61 Strongban** (a 2 920 nem elavult Thayer `sz`-sorból), plusz 58 lefedési tétel (Strongonként egy: a fordítássorok nem
fedik le az új szakaszszámot).
A 636-ból **539 csak eltolódott** (a régi szöveg változatlanul megvan ugyanabban a Strongban, más sorszámon), **97 szövege
valóban megváltozott** (a kettévágott bekezdés első része, a K2-bekezdések). A tételes lista: 8. melléklet, B tábla.

**Az `adat/forditasok.tsv`-t nem írtam** (nincs az `ir`-ben, és a #121/#153/#161 is írja). A CI E1 (`ellenoriz.py`) ezért
a PR-on a 13. szabálynál SÉRTÉS-t ad, amíg a sorok sorsáról nincs döntés (6.3, DT-F186b). A lehetséges parancsok:

- jelzés és lista: `python eszkozok/thayer_jelolt/szolista.py` (a #7 futási listája), `python eszkozok/ellenoriz.py`;
- `elavult`-ra állítás: a meglévő eszközök közül egyik sem teszi meg újrafordítás nélkül; egy egyszeri, bájtőrző szkript kell,
  amely a B tábla 636 sorában az `allapot`-ot `elavult`-ra írja (a többi sor bájtra változatlan, az `igazolas_migracio.py`
  mintájára), vagy
- **átkulcsolás hash szerint** az 539 eltolódott sorra (`jelentes_szam` sz<régi> → sz<új>, a `forras_hash` változatlan), és
  csak a 97 megváltozott + az új szakaszok mennek újrafordításra — ez új mechanizmus, a #7 dönti el.

### 6.3 Nyitott kérdések (az orkesztrátornak; helyőrzővel)

- **DT-F186a — a T4 kapuja nem teljesült (192/200).** (a) második szabálykör a seed-202 osztályaira (K1b, K1c, K2b; a K4
  forrás-torzulás tételesen) és új vak mérés **seed-203**-mal (költség: négy Opus-kitöltő, mérésenként ≈ 1,2 M subagent-token,
  a seed-201/202 alapján) · (b) a T3: kétes esetek modelles döntése (költségbecslés előbb) · (c) a mért 96,0% elfogadása „próba”
  jelöléssel (a BDB DT177 (c) mintája). **Javaslat: (a)** — a hibák osztályokba rendeződnek, a prototípus szerint olcsón
  javíthatók, és a ritka réteg már 100/100.
- **DT-F186b — a 636 hash-eltérő fordítássor (és a CI 13. szabálya).** (a) egyszeri bájtőrző `elavult`-ra állítás mind a
  636 sorra · (b) átkulcsolás hash szerint az 539 eltolódott sorra, `elavult` csak a 97-re · (c) a szakasztábla vágása
  helyett a vers-sor útvonala a hivatkozás pozíciójából (a szakaszkulcsok nem változnak, 0 elavuló sor; a mért mennyiség
  ugyanaz, de a vers útvonala a szakasztáblában nem létező pontra mutathat, és a #187 jelentésfája ezt nem látja). **Javaslat:
  (b)**, ha a #7 lánca ezt vállalja; különben (a).
- **DT-F186c — `ir`-en kívüli, egysoros javítások** (a döntés nélkül nem írtam): `eszkozok/thayer_jelolt/teszt_lanc.py:59` a
  szakaszszámot rögzíti (`17093` → `17266`, a `Betolto.test_ellenoriz` most bukik); `eszkozok/thayer_jelolt/forras_javit.py:125`
  fejléc-literálja a kiosztott helyőrzőt írja (`DT-F132i` → `DT333`; a regenerált `thayer_forras_javitas.tsv` fejlécében így a
  helyőrző áll). A `teszt_lanc.py` `Sigla.test_tabla_determinisztikus_es_kezi_vedett` már a változtatás előtt bukott
  (`thayer_sigla.tsv` darabszám-eltérés, 66 ≠ 60) — nem a #186 okozta.
- **N-F186a — K3, a záró szinonima-jegyzet** (T181): új `utvonal`-érték (`zaro`) vagy a jegyzet leválasztása; a fogyasztók
  (lapgenerátor, #187) érintettek. 1/200 a seed-201-en, 0/200 a seed-202-n.
- **N-F186b — a `bcv` tartalmi hibája** (T119 G0027 „Luk 8:18”: a forrás valószínűleg az Ascensio Isaiae-t jelöli Lukácsnak;
  mindkét kitöltő jelezte; a jelentéspontot nem érinti).

## 7. Melléklet — a mintavevő forrása (`f186_minta.py`)

A szkript a repón kívül fut (a brief `ir` mezője nem tartalmaz mérőszkriptet); a mintát ez a forrás és a seed teljesen meghatározza.

```python
"""F186 T1/T4 — a Thayer vers -> jelentéspont vak mintája (seed-201 / seed-202).

Sokaság: az adat/thayer_vers_jelentes.tsv ÚSZ-sorai (konyv a Konyv_normalizalo_tabla 40-66. könyve), egy sor = egy hivatkozás.
Rétegek: a Strongok az ÚSZ-sorszámuk szerint csökkenő sorrendben (egyezésnél Strong szerint); `gyakori` az az előtag, amelynél a
kumulált sorszám először éri el a sokaság felét; `ritka` a többi. Rétegenként 100 sor egyenletesen (random.Random(seed).sample a
(strong, sorszam) szerint rendezett listán), majd a 200 sor ugyanazzal a generátorral keverve, azon T001..T200 (seed-202: U001..).
Mivel a két réteg a sokaság egy-egy fele, a minta önsúlyozó: a 200 nyers aránya a sokaság becslése.

Kimenet (a --ki könyvtárba): <tag>_vak.tsv (a kitöltőnek), <tag>_szocikkek.txt (a szócikkek szövege a jelölőkkel, a kitöltőnek),
<tag>_kulcs.tsv (a gépi hozzárendelés; a kitöltőnek NEM adandó).
Használat: python f186_minta.py --seed 201 --elotag T --ki <könyvtár> [--kizar <kulcs.tsv> ...]
"""
import argparse
import collections
import html
import os
import random
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = r'E:\Claude\Bible-Study\cranky-easley-763e7c'
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'thayer_jelolt'))
import bont  # noqa: E402
import vers_jelentes as VJ  # noqa: E402

TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'[ \t\r\n]+')
MAX_SZOCIKK = 40000


def olvas(ut):
    L = [l.rstrip('\n').rstrip('\r').split('\t') for l in open(ut, encoding='utf-8') if l.strip() and not l.startswith('#')]
    return [dict(zip(L[0], r)) for r in L[1:]]


def usz_konyvek():
    L = [l.rstrip('\n').split('\t') for l in open(VJ.KONYV_UT, encoding='utf-8')]
    i = L[0].index('Magyar rövidítés')
    return [r[i] for r in L[40:67]]


def hivatkozas_poziciok(raw, f0):
    """A bekezdés hivatkozásai a vers_jelentes.general sorrendjében: [(poz a raw-ban, megjelenő szöveg)]."""
    ki = []
    for m in VJ.BCV.finditer(raw):
        vege = VJ.REF_VEG.search(raw, m.end())
        ki.append((m.start(), TAG.sub('', raw[m.end():vege.start() if vege else m.end()])))
        if not vege:
            continue
        # a folytatás-lánc pozíciói (a VJ.folytatasok logikája, pozícióval)
        q = vege.end()
        t = VJ.FOLYT_TARTOMANY.match(raw, q)
        if t:
            q = t.end()
        while True:
            mm = VJ.FOLYT_VERS.match(raw, q)
            if mm:
                ki.append((mm.start(1), mm.group(1)))
            else:
                mm = VJ.FOLYT_FEJEZET.match(raw, q)
                if not mm:
                    break
                ki.append((mm.start(1), mm.group(1) + ':' + mm.group(2)))
            q = mm.end()
            t = VJ.FOLYT_TARTOMANY.match(raw, q)
            if t:
                q = t.end()
    return ki


def sima_jelolovel(raw, jelolok):
    """A bekezdés sima szövege; a jelolok {raw-poz: azon} helyére „⟦azon⟧ ” kerül."""
    darabok, p = [], 0
    for poz in sorted(jelolok):
        darabok.append(raw[p:poz])
        darabok.append('\x00%s\x01' % jelolok[poz])
        p = poz
    darabok.append(raw[p:])
    s = html.unescape(TAG.sub('', ''.join(darabok)))
    s = WS.sub(' ', s).strip()
    return s.replace('\x00', '⟦').replace('\x01', '⟧ ')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--elotag', required=True)
    ap.add_argument('--ki', required=True)
    ap.add_argument('--kizar', nargs='*', default=[])
    a = ap.parse_args()
    usz = set(usz_konyvek())
    sorok = [r for r in olvas(VJ.KI_UT) if r['konyv'] in usz]
    kizart = set()
    for k in a.kizar:
        kizart |= {(r['strong'], r['sorszam']) for r in olvas(k)}
    db = collections.Counter(r['strong'] for r in sorok)
    rend = sorted(db, key=lambda s: (-db[s], s))
    fel, acc, gyakori = len(sorok) / 2, 0, set()
    for s in rend:
        if acc >= fel:
            break
        gyakori.add(s)
        acc += db[s]
    retegek = {'gyakori': [], 'ritka': []}
    for r in sorok:
        if (r['strong'], r['sorszam']) in kizart:
            continue
        retegek['gyakori' if r['strong'] in gyakori else 'ritka'].append(r)
    rng = random.Random(a.seed)
    minta = []
    for nev in ('gyakori', 'ritka'):
        L = sorted(retegek[nev], key=lambda r: (r['strong'], int(r['sorszam'])))
        for r in rng.sample(L, 100):
            minta.append(dict(r, reteg=nev))
    rng.shuffle(minta)
    for i, r in enumerate(minta, 1):
        r['azon'] = '%s%03d' % (a.elotag, i)
    print('sokaság ÚSZ-sor: %d; Strong: %d; gyakori Strong: %d (%d sor), ritka Strong: %d (%d sor); kizárt: %d'
          % (len(sorok), len(db), len(gyakori), acc, len(db) - len(gyakori), len(sorok) - acc, len(kizart)))

    lex = bont.lexikon_beolvas()
    cel = collections.defaultdict(dict)  # strong -> {sorszam: azon}
    for r in minta:
        cel[r['strong']][int(r['sorszam'])] = r['azon']
    szoveg, kornyezet, nyers = {}, {}, {}
    for sp in sorted(cel):
        topic, d = lex[sp]
        n, bekezdesek, utolso = 0, [], -1
        for x in bont.szerkezet(d):
            jel = {}
            for poz, megj in hivatkozas_poziciok(x['raw'], 0):
                n += 1
                if n in cel[sp]:
                    az = cel[sp][n]
                    jel[poz] = az
                    nyers[az] = megj
            bekezdesek.append(sima_jelolovel(x['raw'], jel))
            if jel:
                utolso = len(bekezdesek) - 1
        for az in cel[sp].values():
            for b in bekezdesek:
                i = b.find('⟦%s⟧' % az)
                if i >= 0:
                    kornyezet[az] = b[max(0, i - 160):i + 120]
        teljes = '\n\n'.join(bekezdesek)
        if len(teljes) > MAX_SZOCIKK:
            teljes = '\n\n'.join(bekezdesek[:utolso + 2]) + '\n\n[… a szócikk folytatódik; a jelölt hivatkozások mind a fenti részben állnak]'
        szoveg[sp] = teljes
    os.makedirs(a.ki, exist_ok=True)
    tag = 'seed%d' % a.seed
    with open(os.path.join(a.ki, tag + '_szocikkek.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for sp in sorted(szoveg):
            f.write('=== %s ===\n%s\n\n' % (sp, szoveg[sp]))
    with open(os.path.join(a.ki, tag + '_vak.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['azon', 'strong', 'nyers', 'kornyezet', 'konyv_vers', 'jelentespont', 'melyebb', 'megjegyzes']) + '\n')
        for r in sorted(minta, key=lambda r: r['azon']):
            f.write('\t'.join([r['azon'], r['strong'], nyers[r['azon']], kornyezet[r['azon']].replace('\t', ' '), '', '', '', '']) + '\n')
    with open(os.path.join(a.ki, tag + '_kulcs.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        mezok = ['azon', 'reteg', 'strong', 'sorszam', 'szakasz', 'konyv', 'fejezet', 'vers', 'utvonal']
        f.write('\t'.join(mezok) + '\n')
        for r in sorted(minta, key=lambda r: r['azon']):
            f.write('\t'.join(r[m] for m in mezok) + '\n')
    print('szócikk: %d; szöveg összesen %d karakter' % (len(szoveg), sum(len(v) for v in szoveg.values())))
    hiany = [az for az in (r['azon'] for r in minta) if az not in nyers or az not in kornyezet]
    print('jelölő nélkül maradt: %s' % hiany)


if __name__ == '__main__':
    main()
```

## 8. Melléklet — tételes listák

### A. A megváltozott szakaszkulcsok Strongonként (6.1)

*A „megváltozott kulcsok” oszlop a régi és az új tábla összes eltérő `sorszam`-a; az „új szakasz” a bekezdésen belüli fejnél nyíló sor az új sorszámával; a „K2” a régi tábla azon sora, amelynek feje hamis volt (most örökölt útvonal).*

| Strong | sor (régi → új) | megváltozott kulcsok (`sorszam`) | új szakasz: belső fej (új `sorszam` · útvonal · jel) | K2 (fej → örökölt) |
|---|---|---|---|---|
| G0188 | 2 → 3 | sz2–sz3 | sz3 · -/-/a · a. | — |
| G0214 | 5 → 6 | sz4–sz6 | sz5 · -/-/c · c. | — |
| G0217 | 7 → 8 | sz7–sz8 | sz8 · -/4/- · 4. | — |
| G0225 | 9 → 11 | sz4–sz11 | sz5 · I/1/a · a.; sz8 · I/2/a · a. | — |
| G0316 | 4 → 5 | sz3–sz5 | sz4 · -/-/b · b. | — |
| G0331 | 5 → 6 | sz4–sz6 | sz5 · -/2/a · a. | — |
| G0350 | 4 → 4 | sz3 | sz3 · -/-/a · a. | — |
| G0387 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G0435 | 6 → 8 | sz3–sz8 | sz4 · -/1/a · a.; sz5 · -/1/b · b. | — |
| G0444 | 16 → 18 | sz3–sz18 | sz4 · -/1/a · a.; sz14 · -/4/- · 4.; sz15 · -/4/a · a. | — |
| G0450 | 12 → 13 | sz8–sz13 | sz8 · II/1/- · 1.; sz9 · II/1/a · a. | — |
| G0473 | 13 → 15 | sz6–sz15 | sz7 · -/2/c · c.; sz10 · -/3/- · 3.; sz11 · -/3/a · a. | — |
| G0476 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G0575 | 29 → 31 | sz11–sz31 | sz12 · I/4/a · a.; sz24 · II/2/- · 2.; sz25 · II/2/a · a. | sz21 |
| G0629 | 5 → 6 | sz2–sz6 | sz3 · -/-/a · a. | — |
| G0703 | 5 → 6 | sz4–sz6 | sz5 · -/2/a · a. | — |
| G0752 | 3 → 4 | sz3–sz4 | sz4 · -/-/d · d. | — |
| G0831 | 4 → 4 | sz4 | sz4 · -/-/b · b. | — |
| G0846 | 19 → 23 | sz4–sz23 | sz5 · I/1/a · a.; sz10 · I/2/- · 2.; sz11 · I/2/a · a.; sz20 · II/7/- · 7. | — |
| G0863 | 21 → 22 | sz21–sz22 | sz22 · -/3/h · h. | — |
| G0891 | 7 → 8 | sz3–sz8 | sz4 · -/1/a · a. | — |
| G0908 | 6 → 6 | sz6 | — | sz6 |
| G1060 | 8 → 9 | sz6–sz9 | sz7 · -/2/a · a. | — |
| G1063 | 20 → 24 | sz14–sz24 | sz15 · II/9/a · a.; sz16 · II/9/b · b.; sz17 · II/9/c · c.; sz19 · II/10/a · a. | — |
| G1096 | 17 → 18 | sz17–sz18 | sz18 · -/5/g · g. | — |
| G1135 | 3 → 4 | sz3–sz4 | sz4 · -/2/- · 2. | — |
| G1163 | 8 → 9 | sz2–sz9 | sz3 · -/-/a · a. | — |
| G1325 | 38 → 40 | sz13–sz40 | sz14 · B.I/6/a · a.; sz15 · B.I/6/b · b. | sz25 |
| G1330 | 8 → 8 | sz5 | sz5 · -/1/b · b. | — |
| G1343 | 6 → 7 | sz4–sz7 | sz5 · -/1/b · b. | — |
| G1380 | 7 → 7 | sz6 | sz6 · -/3/a · a. | — |
| G1392 | 9 → 9 | sz7 | sz7 · -/4/a · a. | — |
| G1437 | 18 → 20 | sz8–sz20 | sz9 · I/2/a · a.; sz10 · I/2/b · b. | — |
| G1453 | 13 → 14 | sz5–sz14 | sz6 · -/3/a · a. | — |
| G1510 | 91 → 99 | sz16–sz99 | sz17 · II/4/a · a.; sz20 · II/4/c · c.; sz46 · IV/1/h · h.; sz72 · V/4/h · h.; sz73 · V/5/- · 5.; sz74 · V/5/a · a.; sz77 · V/6/- · 6.; sz78 · V/6/a · a.; sz82 · V/8/- · 8.; sz83 · V/8/a · a.; sz92 · V/11/- · 11.; sz93 · V/11/a · a. | — |
| G1519 | 43 → 46 | sz5–sz46 | sz6 · A.I/1/a · a.; sz7 · A.I/1/b · b.; sz35 · B.II/3/- · 3.; sz36 · B.II/3/a · a. | sz37 |
| G1544 | 15 → 16 | sz10–sz16 | sz11 · -/1/h · h. | — |
| G1588 | 6 → 7 | sz3–sz7 | sz3 · -/1/- · 1.; sz4 · -/1/a · a. | — |
| G1590 | 5 → 6 | sz4–sz6 | sz5 · -/2/a · a. | — |
| G1622 | 3 → 4 | sz3–sz4 | sz4 · -/-/b · b. | — |
| G1632 | 3 → 4 | sz3–sz4 | sz4 · -/-/b · b. | — |
| G1680 | 5 → 6 | sz4–sz6 | sz5 · -/2/a · a. | — |
| G1699 | 4 → 5 | sz4–sz5 | sz5 · -/-/c · c. | — |
| G1722 | 42 → 50 | sz5–sz50 | sz6 · I/1/b · b.; sz12 · I/3/a · a.; sz20 · I/5/d · d.; sz23 · I/5/f · f.; sz24 · I/5/g · g.; sz25 · I/5/h · h.; sz30 · I/6/d · d.; sz38 · II/-/- · II.; sz39 · II/-/a · a. | sz18 |
| G1777 | 7 → 8 | sz2–sz8 | sz3 · -/-/a · a. | — |
| G1807 | 5 → 6 | sz4–sz6 | sz4 · -/2/- · 2.; sz5 · -/2/a · a. | — |
| G1899 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G1909 | 63 → 63 | sz25–sz27, sz29, sz32 | — | sz25, sz26, sz27, sz29, sz32 |
| G2135 | 4 → 6 | sz3–sz6 | sz3 · -/-/a · a.; sz4 · -/-/b · b.; sz6 · -/-/c · c. | — |
| G2192 | 22 → 24 | sz18–sz24 | sz19 · I/2/h · h.; sz20 · I/2/i · i. | — |
| G2193 | 23 → 24 | sz4–sz24 | sz5 · I/1/a · a. | — |
| G2197 | 5 → 6 | sz5–sz6 | sz6 · -/2/d · d. | — |
| G2228 | 23 → 24 | sz21–sz24 | sz21 · -/4/b · b.; sz22 · -/4/c · c. | — |
| G2396 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G2398 | 8 → 10 | sz3–sz10 | sz3 · -/1/- · 1.; sz4 · -/1/a · a.; sz6 · -/1/c · c. | — |
| G2443 | 23 → 24 | sz13–sz24 | sz14 · II/2/a · a. | — |
| G2519 | 3 → 4 | sz3–sz4 | sz4 · -/-/b · b. | — |
| G2532 | 33 → 35 | sz9–sz35 | sz10 · I/2/b · b.; sz18 · I/2/h · h. | sz11, sz15, sz24 |
| G2588 | 6 → 7 | sz4–sz7 | sz5 · -/2/a · a. | — |
| G2673 | 2 → 3 | sz2–sz3 | sz3 · -/1/- · 1. | — |
| G2817 | 5 → 6 | sz4–sz6 | sz5 · -/2/a · a. | — |
| G2937 | 7 → 8 | sz4–sz8 | sz5 · -/2/a · a. | — |
| G2962 | 5 → 6 | sz2–sz6 | sz3 · -/-/a · a. | — |
| G2974 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G3000 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G3004 | 42 → 45 | sz7–sz45 | sz8 · -/2/a · a.; sz37 · II/1/h · h.; sz38 · II/1/i · i. | — |
| G3008 | 5 → 7 | sz5–sz7 | sz6 · -/2/b · b.; sz7 · -/2/c · c. | — |
| G3009 | 7 → 8 | sz6–sz8 | sz6 · -/3/- · 3.; sz7 · -/3/a · a. | — |
| G3056 | 26 → 27 | sz7–sz27 | sz8 · I/2/c · c. | — |
| G3123 | 9 → 10 | sz5–sz10 | sz6 · -/1/c · c. | — |
| G3140 | 6 → 6 | sz4 | — | sz4 |
| G3173 | 11 → 12 | sz3–sz12 | sz3 · -/1/- · 1.; sz4 · -/1/a · a. | — |
| G3326 | 23 → 25 | sz11–sz25 | sz12 · I/2/d · d.; sz16 · I/2/h · h. | — |
| G3360 | 6 → 7 | sz3–sz7 | sz4 · -/1/a · a. | — |
| G3367 | 10 → 12 | sz2–sz12 | sz3 · -/-/a · a.; sz10 · -/-/h · h. | — |
| G3371 | 9 → 10 | sz9–sz10 | sz10 · -/-/h · h. | — |
| G3379 | 8 → 8 | sz5 | — | sz5 |
| G3386 | 2 → 4 | sz2–sz4 | sz3 · -/-/a · a.; sz4 · -/-/b · b. | — |
| G3398 | 7 → 8 | sz2–sz8 | sz3 · -/-/a · a. | — |
| G3458 | 3 → 4 | sz2–sz4 | sz3 · -/1/- · 1. | — |
| G3471 | 5 → 6 | sz4–sz6 | sz4 · -/2/- · 2.; sz5 · -/2/a · a. | — |
| G3521 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G3588 | 41 → 47 | sz8–sz47 | sz9 · II/1/a · a.; sz13 · II/1/e · e.; sz24 · II/5/- · 5.; sz25 · II/5/a · a.; sz28 · II/6/- · 6.; sz29 · II/6/a · a.; sz39 · II/9/c · c.; sz40 · II/10/- · 10.; sz41 · II/10/a · a. | — |
| G3598 | 9 → 10 | sz6–sz10 | sz7 · -/1/c · c. | — |
| G3606 | 4 → 5 | sz2–sz5 | sz3 · -/-/a · a. | — |
| G3625 | 7 → 8 | sz6–sz8 | sz7 · -/1/d · d. | — |
| G3686 | 12 → 13 | sz10–sz13 | sz11 · -/2/f · f. | — |
| G3687 | 4 → 5 | sz3–sz5 | sz4 · -/-/b · b. | — |
| G3717 | 3 → 4 | sz3–sz4 | sz4 · -/-/b · b. | — |
| G3739 | 24 → 25 | sz10–sz25 | sz10 · II/3/- · 3.; sz11 · II/3/a · a. | — |
| G3745 | 6 → 7 | sz2–sz7 | sz3 · -/-/a · a. | — |
| G3761 | 6 → 6 | sz4 | — | sz4 |
| G3767 | 7 → 9 | sz2–sz9 | sz3 · -/-/a · a.; sz9 · -/-/h · h. | — |
| G3778 | 23 → 24 | sz12–sz24 | sz12 · I/2/- · 2.; sz13 · I/2/a · a. | — |
| G3779 | 13 → 14 | sz7, sz13–sz14 | sz14 · -/5/f · f. | sz7 |
| G3825 | 7 → 8 | sz7–sz8 | sz8 · -/3/- · 3. | — |
| G3844 | 24 → 25 | sz14–sz25 | sz15 · II/-/e · e. | — |
| G3908 | 5 → 6 | sz3–sz6 | sz4 · -/1/a · a. | — |
| G3918 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G3958 | 5 → 5 | sz4 | — | sz4 |
| G3962 | 12 → 14 | sz3–sz14 | sz4 · -/1/a · a.; sz5 · -/1/b · b. | — |
| G4101 | 3 → 4 | sz3–sz4 | sz4 · -/-/b · b. | — |
| G4102 | 9 → 10 | sz6–sz10 | sz7 · -/1/d · d. | — |
| G4135 | 5 → 6 | sz5–sz6 | sz6 · -/-/d · d. | — |
| G4151 | 17 → 17 | sz14 | — | sz14 |
| G4160 | 24 → 25 | sz14–sz25 | sz14 · I/2/b · b.; sz15 · I/2/c · c. | — |
| G4164 | 3 → 4 | sz3–sz4 | sz3 · -/-/a · a.; sz4 · -/-/b · b. | — |
| G4176 | 7 → 8 | sz5–sz8 | sz6 · -/3/a · a. | — |
| G4183 | 6 → 7 | sz2–sz7 | sz3 · -/-/a · a. | — |
| G4202 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G4226 | 4 → 5 | sz2–sz5 | sz3 · -/-/a · a. | — |
| G4229 | 5 → 6 | sz2–sz6 | sz3 · -/-/a · a. | — |
| G4253 | 5 → 6 | sz2–sz6 | sz3 · -/-/a · a. | — |
| G4291 | 6 → 7 | sz4–sz7 | sz5 · -/2/a · a. | — |
| G4314 | 30 → 32 | sz13–sz32 | sz14 · I/2/b · b.; sz16 · I/3/a · a. | — |
| G4352 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G4396 | 13 → 14 | sz12–sz14 | sz13 · II/1/g · g. | — |
| G4442 | 3 → 3 | sz3 | — | sz3 |
| G4459 | 8 → 10 | sz3–sz10 | sz4 · I/-/a · a.; sz6 · I/-/c · c. | — |
| G4487 | 9 → 10 | sz7–sz10 | sz8 · -/2/a · a. | — |
| G4510 | 2 → 4 | sz2–sz4 | sz3 · -/1/- · 1.; sz4 · -/2/- · 2. | — |
| G4525 | 4 → 5 | sz2–sz5 | sz3 · -/1/- · 1. | — |
| G4624 | 4 → 5 | sz4–sz5 | sz5 · -/-/c · c. | — |
| G4815 | 7 → 8 | sz6–sz8 | sz6 · -/2/- · 2.; sz7 · -/2/a · a. | — |
| G4934 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G4984 | 4 → 4 | sz3 | sz3 · -/-/a · a. | — |
| G5037 | 12 → 13 | sz3–sz13 | sz4 · -/1/a · a. | — |
| G5101 | 11 → 12 | sz8–sz12 | sz9 · -/1/e · e. | — |
| G5206 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G5259 | 13 → 14 | sz5–sz14 | sz6 · I/2/a · a. | — |
| G5287 | 7 → 8 | sz7–sz8 | sz8 · -/2/d · d. | — |
| G5302 | 8 → 8 | sz4 | sz4 · -/1/a · a. | — |
| G5342 | 17 → 18 | sz10–sz18 | sz11 · -/1/d · d. | — |
| G5442 | 8 → 9 | sz7–sz9 | sz7 · -/2/- · 2.; sz8 · -/2/a · a. | — |
| G5479 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a: | — |
| G5547 | 6 → 7 | sz4–sz7 | sz5 · -/2/a · a. | — |
| G5548 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G5591 | 4 → 4 | sz3 | sz3 · -/-/a · a. | — |
| G5599 | 3 → 4 | sz2–sz4 | sz3 · -/-/a · a. | — |
| G5613 | 25 → 26 | sz5–sz26 | sz6 · I/2/a · a. | — |

Összesen: 140 Strong, 1009 megváltozott kulcs.

### B. A #7 érintett fordítássorai (`adat/forditasok.tsv`, `szotar = Thayer`, `mezo = forditas_hu`, nem `elavult`, a `forras_hash` a T2 után eltér; 6.2)

| Strong | eltolódott (a szöveg változatlan, más sorszámon) | megváltozott szövegű |
|---|---|---|
| G0225 | sz5, sz7–sz9 | sz4, sz6 |
| G0316 | sz4 | sz3 |
| G0435 | sz4–sz6 | sz3 |
| G0444 | sz4–sz12, sz14–sz16 | sz3, sz13 |
| G0450 | sz9–sz12 | sz8 |
| G0575 | sz12–sz20, sz22, sz24–sz29 | sz11, sz21, sz23 |
| G0846 | sz5–sz7, sz9–sz15, sz17–sz19 | sz4, sz8, sz16 |
| G0863 | — | sz21 |
| G1063 | sz16–sz20 | sz14–sz15 |
| G1096 | — | sz17 |
| G1135 | — | sz3 |
| G1163 | sz3–sz8 | sz2 |
| G1325 | sz14–sz38 | sz13 |
| G1343 | sz5–sz6 | sz4 |
| G1437 | sz9–sz18 | sz8 |
| G1453 | sz6–sz13 | sz5 |
| G1510 | sz17, sz19–sz42, sz44–sz67, sz70–sz71, sz73–sz75, sz77–sz84, sz86–sz91 | sz16, sz18, sz43, sz68–sz69, sz72, sz76, sz85 |
| G1519 | sz6–sz32, sz34–sz43 | sz5, sz33 |
| G1544 | sz11–sz15 | sz10 |
| G1632 | — | sz3 |
| G1722 | sz6–sz9, sz11–sz16, sz18, sz20–sz22, sz24–sz30, sz32–sz42 | sz5, sz10, sz17, sz19, sz23, sz31 |
| G1909 | — | sz25–sz27, sz29, sz32 |
| G2192 | sz19–sz22 | sz18 |
| G2193 | sz5–sz23 | sz4 |
| G2228 | sz22–sz23 | sz21 |
| G2398 | sz5–sz8 | sz3–sz4 |
| G2443 | sz14–sz23 | sz13 |
| G2532 | sz10, sz12–sz14, sz17–sz23, sz25–sz33 | sz9, sz11, sz15–sz16, sz24 |
| G2588 | sz5–sz6 | sz4 |
| G2962 | sz3–sz5 | sz2 |
| G3004 | sz8–sz34, sz36–sz42 | sz7, sz35 |
| G3056 | sz8–sz26 | sz7 |
| G3123 | sz6–sz9 | sz5 |
| G3140 | — | sz4 |
| G3173 | sz4–sz11 | sz3 |
| G3326 | sz12–sz13, sz15–sz23 | sz11, sz14 |
| G3367 | sz3–sz7, sz9–sz10 | sz2, sz8 |
| G3398 | sz3–sz7 | sz2 |
| G3598 | sz7–sz9 | sz6 |
| G3686 | sz11–sz12 | sz10 |
| G3739 | sz11–sz24 | sz10 |
| G3745 | sz3–sz6 | sz2 |
| G3761 | — | sz4 |
| G3767 | sz3–sz6 | sz2, sz7 |
| G3778 | sz13–sz23 | sz12 |
| G3779 | — | sz7, sz13 |
| G3825 | — | sz7 |
| G3844 | sz15–sz24 | sz14 |
| G3962 | sz4–sz12 | sz3 |
| G4102 | sz7–sz9 | sz6 |
| G4160 | sz15–sz24 | sz14 |
| G4314 | sz15–sz30 | sz13–sz14 |
| G4396 | sz13 | sz12 |
| G4459 | sz5–sz8 | sz3–sz4 |
| G4487 | sz8–sz9 | sz7 |
| G5037 | sz4–sz12 | sz3 |
| G5101 | sz9–sz11 | sz8 |
| G5259 | sz6–sz13 | sz5 |
| G5442 | sz8 | sz7 |
| G5547 | sz5–sz6 | sz4 |
| G5613 | sz6–sz25 | sz5 |

Összesen: 61 Strong, 636 sor (eltolódott 539, megváltozott szövegű 97).
