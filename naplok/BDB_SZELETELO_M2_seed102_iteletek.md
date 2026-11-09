# F102 — a seed-102 újramérés eltéréseinek soronkénti ítélete (⛔ 3.6)

**Jóváhagyva** (orkesztrátori döntés, local_c8cc3610, a felhasználó felhatalmazásával, 2026-11-09): az ítéletek, a kérdéses tételekre: **M143** kulcs-hiba (alaktani megjegyzés, nem alpont), nem számít a szeletelő (és a tábla) ellen; **M018** a mérésből kizárva (jelölve); ~~**M036** és a seed-101 **M162** mindkettő `forras_hiba` a mai (1c.) szabály szerint~~ — **visszavonva** (orkesztrátori döntés, local_c8cc3610, 2026-11-09, ELLENOR_F102 3.): mindkettő **szeletelő-hiba**, mert a forrásban van „1 … h.” (ill. „1 … a.”) számozás, csak a „Qal” név hiányzik; **M091** `forras_hiba`; **M214** bibliai hely (a kitöltés „bizonytalan”-ja tehát kitöltő-hiba marad); **M039, M127, M196** a mai óvatos szabály marad (nem szeletelő-hiba); **M060** a könyvnév nélküli hely a szócikkben utoljára megnevezett könyvre oldódik, ha egyértelmű — itt a „compare Gen 19:20” után 1Móz 13:10; a szeletelő a könyvet örökli, de a sort szűri (a TAHOT-kapu a H6920-at keresi, a TSV H6920-sora viszont a Cóar (Zoar) szócikke: N-F102f), tehát saját hiba (csak ítélet, kódváltozás nincs). DT-F102d: (ii), a szeletelő marad. A kapu: a „próba” marad, a szó-lapon az új nyers szám CI-vel.

*Kézi ítélet a forrásszöveg alapján (`konkordancia/BDB_teljes_unabridged.tsv`, a Strong sora, a szeletelő „lapított” alakjában; a `poz` a
hivatkozás helye), a seed-101 mintájára (`naplok/BDB_SZELETELO_M2_seed101_iteletek.md`). Kategóriák: **szeletelő-hiba** (a 2.29 kulcsa hibás),
**szakasztábla-hiba** (a `--szakasztabla` kulcs útvonala hibás), **kitöltő-hiba** (csak a forrással bizonyítva), **kulcs-ellentmondás**,
**`forras_hiba`**. Mérés: kulcs `naplok/BDB_SZELETELO_M2_minta_seed102_kulcs.tsv` (F102.4), kitöltések `naplok/BDB_SZELETELO_M2_seed102_kitoltott_A.tsv`
és `_B.tsv` (F102.5), összevetés `m2_minta_osszevet.py` és `--szakasztabla` (`naplok/F102_BDB_SZELETELO_JAVITAS_naplo.md` 14.). A kapu
következménye az ítélet ELŐTT rögzítve: DT-F102c (a) (nyers szám); a forrás választása: DT-F102d (C). Proveniencia: `scope=seed-102 vak minta |
forras=BDB_teljes_unabridged.tsv (lapított; eseti szkript itel_dump.py, szakasz_ki.py) + m2_minta_osszevet.py [--szakasztabla] | ts=2026-11-09`;
az ítélet értelmezés (manual), nem gépi eredmény.*

**A törzsnév-írásmód ellenőrzése** (az orkesztrátor kérésére): az összevető a backticket aposztrófra normálja (`normal()`), és a törzs-eltérések
(M003, M009, M011, M027, M223, M233, M249) mind valódi törzs- vagy számeltérések (Niph'al ↔ Pi'el, Hithpa'el ↔ Hiph'il, Hiph'il ↔ Hithpa'lel,
Pi'el/- ↔ Pi'el/2), egyik sem az írásmódból jön. Az összevetőnek itt nincs hibája.

## 1. Összesítő

| | szeletelő (2.29) | szakasztábla (2.30 útvonal) |
|---|---:|---:|
| nyers jelentéspont, véletlen 200 | **183** (91,5%; 95% CI 86,7–95,0%) | **184** (92,0%; 87,3–95,4%) |
| eltérés | 17 | 16 |
| ebből saját hiba (szeletelő-, ill. szakasztábla-hiba) | 16 (M036-tal; ebből M143 utóbb kulcs-hiba) | 13 (+ 1 szeletelő-hiba a 2.29-ből átvett `szakasz`-ban: M058; ebből M143 utóbb kulcs-hiba, M018 kizárva) |
| kitöltő-hiba | 1 (M052) | 1 (M052) |
| `forras_hiba` | 0 (az M036 szeletelő-hiba, ELLENOR_F102 3.) | 1 (M036; ELLENOR_F102_2 1.) |
| kulcs-ellentmondás | 0 | 0 |
| ítélet utáni, a jóváhagyás előtti javaslat | 185 / 200 | 186 / 200 |
| ~~ítélet utáni, jóváhagyott (M036 `forras_hiba`-val)~~ | ~~185 / 199~~ | ~~187 / 199~~ |
| ~~ítélet utáni, javított (M036 a táblán is hiba)~~ | 184 / 199 | ~~186 / 199~~ |
| **ítélet utáni, végleges** (csak tájékoztató; M018 kizárva, n = 199; M143 kulcs-hiba; M036 a szeletelőn hiba, a táblán `forras_hiba`; ELLENOR_F102 3., ELLENOR_F102_2 1.) | **184 / 199** (92,5%) | **187 / 199** (94,0%) |
| könyv/vers, véletlen 200 | 199 (99,5%; 97,2–100%); az 1 eltérés `forras_hiba` (M091) → ítélet után 200 | ugyanaz |

**A kapu (DT-F102c (a), nyers szám):** könyv/vers 99,5% ≥ 99% teljesül, **jelentéspont 91,5% < 97% nem teljesül** → a „próba” jelölés marad; a
szó-lapon (`blokkok.py` `BDB_MERT_PONTOSSAG`) az új nyers szám és CI áll; a további javítás külön feladat, a #102-ben nincs több mérési kör.
**A forrás (DT-F102d):** a nyers jelentéspont szakasztábla 184, szeletelő 183; a különbség (1/200) a mérési szóráson belül van (a két CI szinte
azonos). A jóváhagyott döntés: **(ii) — a szeletelő marad**; az átállás a 2.30-ra az N-F102e javítása után, újraméréssel (~~a (C) a szóráson túli
különbségre értendő~~ — visszavonva: a (ii) a (C)-től való utólagos eltérés, l. DT-F102g; ELLENOR_F102_2 2.).

## 2. Jelentéspont — soronkénti ítélet

Jelölés: SZ = a szeletelő kulcsa, T = a szakasztábla kulcsa, K = a kitöltés. A helyes érték a forrás szerint.

| azon | Strong | SZ | T | K | forrásidézet (a hely környezete) | ítélet SZ | ítélet T | ok |
|---|---|---|---|---|---|---|---|---|
| M002 | H2388 | `Hiph'il/6/c` | `Pi'el/6/c` | `Hiph`il/6/c` | „6 … a. … b. have or keep hold of … c. hold up … Dan 11:1 (\|\| מָעוֺז), 11:6” | — | **szakasztábla-hiba** | a 6. pont a Hiph`il-é (a BDB חזק Hiph. 6 „take or keep hold”); a tábla a Hiph`il fejet nem látja |
| M221 | H2388 | `Hiph'il/6/a` | `Pi'el/6/a` | `Hiph`il/6/a` | „laying hold of wisdom Prov 3:18 … Job 2:3, 9; 27:6; Jer 8:5. b. have or keep hold” | — | **szakasztábla-hiba** | mint M002 |
| M003 | H2505 | `I Niph'al/3` | `Pi'el/1` | `I Pi`el/1` | „(see above Niph`al) … Imperative חַלֵּק … — 1 divide, apportion: food … 1Chr 16:3” | **szeletelő-hiba** | — | a „see above Niph`al” visszautalás hamis törzsfej; a hely a Pi`el 1. pontja |
| M009 | H5674 | `Hithpa'el/2/a` | `Hiph'il/2/a` | `Hiph`il/2/a` | „— Hithpa`el see [עָבַר] below Hiph`il Perfect … 2. a. … Neh 8:15. b. let pass through” | **szeletelő-hiba** | — | a „Hithpa`el see … below” kereszthivatkozás hamis törzsfej, a rögtön utána álló Hiph`il elvész |
| M011 | H3254 | `Niph'al/2` | `Hiph'il/-` | `Hiph`il` | „Hiph`il172Perfect הֹסִיף 2Kin 24:7” | **szeletelő-hiba** | — | a gyakoriságszámhoz tapadt „Hiph`il172” törzsfejet a szeletelő nem ismeri fel; a hely a Hiph`il alaktani feje |
| M016 | H2161 | `-/2/b` | `Qal/2/b` | `Qal/2/b` | „b. of evil purpose … absolute Prov 30:32 … **the text of Prov 30:32 is questioned” | **szeletelő-hiba** | — | a szócikk igei, a Qal fej (poz 195) elveszett; a lábjegyzet a Qal 2.b-hez tartozik |
| M018 | H2534 | `-/2/c` | `-/2/-` | `-/2/c` | „Vbs. used with חֵמָה … 2. c.: הֵשִׁיב turn away wrath … arises עלה 2Chr 36:16” | **kizárva** | **kizárva** | a függelék „2. c.:” címkéje alatt; a jóváhagyás szerint a mérésből kizárva (n = 199) |
| M027 | H7323 | `Hiph'il/1` | `Qal/1` | `Qal/1` | „(… compare Hiph`il below); … אֵת person accompare Jer 12:5” | **szeletelő-hiba** | — | a „compare Hiph`il below” kereszthivatkozás hamis törzsfej |
| M034 | H2490 | `III Hiph'il/-/b` | `III Hiph'il/2` | `III Hiph`il/2` | „Hiph`il 1. a. … b. … 2 begin, Perfect הֵחֵל … with Infinitive (ל) begin to … 2Chr 3:1-2, 29:17” | **szeletelő-hiba** | — | a „2 begin,” jelentésfej elvész, a hely az 1.b-be csúszik |
| M036 | H3318 | `fej` | `-/1/h` | `Qal/1/h` | „h. … with idea of unfolding, growth Job 8:16; 14:2; 31:40” | **szeletelő-hiba** (javítva, ELLENOR_F102 3.; korábban `forras_hiba`) | **`forras_hiba`** (visszaállítva, ELLENOR_F102_2 1.: a 2.30 `-/1/h`-t ad, a hiányzó „Qal” a 2.31 `jelolo_hianyzik` kézi sora — H3318 sorszam 3 → `Qal/1` —, az 1c. `forras_hiba` osztálya; az ELLENOR_F102 3. döntése csak a szeletelő-oldalra szólt) | a szeletelő a forrásban meglévő „1 … h.” számozást sem látja (`fej`) — szeletelő-hiba; a tábla a számozást hordozza, csak a forrásban hiányzó törzsnevet nem |
| M042 | H5066 | `Qal/-` | `Qal/-` | `Qal/1` | „— draw or come near, 1 human subject: followed by אֶלֿ person … Exod 19:15” | **szeletelő-hiba** | **szakasztábla-hiba** | a fej-glossza utáni „1” jelentésfejet egyik sem ismeri fel |
| M050 | H2063 | `-/3/i` | `-/6/g` | `-/6/g` | „6 … f. זֶה עַל on this account … g. זֶה עִם in spite of this Neh 5:18” | **szeletelő-hiba** | — | a hely a 6.g-ben áll; a szeletelő a 3.i-nél ragad |
| M052 | H9003 | `I r:III -/5` | `I r:III -/5` | `-/5 r:III` | „ב בּ ב,, Bêth, 2nd letter; … I. בְּ, preposition” | — | — | **kitöltő-hiba**: a címszó előtt a forrás „I.”-t ír; a vak lap (1) szabálya szerint a fő címszónál is írandó |
| M056 | H3452 | `-/-/b` | `-/-/a` | `-/b` | „b. without article, a waste or wilderness … Psa 68:8; 78:40; 106:14” | — | **szakasztábla-hiba** | a hely a b.-ben áll; a tábla a b. fejet nem bontja |
| M194 | H3452 | `-/-/b` | `-/-/a` | `-/b` | „b. without article … with reference to returning exiles Isa 43:19-20” | — | **szakasztábla-hiba** | mint M056 |
| M058 | H3651 | `I -/3/f` | `I fej` | `tagolatlan` | „IV. כֵּן see II. כנן. p. 467, below adverb thus … Dan 2:24 …, 2:25; 4:11” | **szeletelő-hiba** | **szeletelő-hiba** (a 2.29-ből átvett `szakasz` I) | a szócikk végi jelöletlen arámi כֵּן címszó tagolatlan; a szeletelő az I. 3.f-be teszi, a `--szakasztabla` útvonala (`fej`) helyes, de a `szakasz` I a 2.29-é |
| M143 | H1980 | `Qal/-/a` | `Qal/-/a` | `Qal` | „Imperative rarely a. הֲלוֺךְ Prov 13:20 (Kt.; Qr הֹלֵךְ” | **kulcs-hiba** (jóváhagyva; nem számít) | **kulcs-hiba** (nem számít) | az „a.” az alaktani felsorolás (Imperative-alakok) betűje, nem jelentés-alpont |
| M198 | H3117 | `-/2/e` | `-/3/e` | `-/2/e` | „(see Zech 14:7 below 3 below) d. day as defined by evening … e. day of month … Exod 12:10” | — | **szakasztábla-hiba** | a „below 3 below” visszautalás hamis „3” fej (a H2403 „see 1 above” osztálya) |
| M201 | H3117 | `-/2/e` | `-/3/e` | `-/2/e` | ugyanott: „… Exod 12:10; 2Kin 25:1, 3; Ezek 1:1-2” | — | **szakasztábla-hiba** | mint M198 |
| M205 | H5595 | `Qal/-` | `Qal/2` | `Qal/2` | „2 transitive: Imperfect … suffix לִסְמּוֺתָהּ Psa 40:15” | **szeletelő-hiba** | — | a „2 transitive:” jelentésfej elvész |
| M208 | H7617 | `Qal/-` | `Qal/2` | `Qal/2` | „2 with accusative of congnate meaning … 2Chr 28:5, 11” | **szeletelő-hiba** | — | mint M205 |
| M223 | H7812 | `Hiph'il/1/b` | `Hiph'il/1/b` | `Hithpa`lel/1/b` | „Hithpa`lel_170 (Ges^§ 75kk) Perfect … b. with ל … Isa 60:14” | **szeletelő-hiba** | **szakasztábla-hiba** | a „Hithpa`lel” törzset (gyakoriságszámmal) egyik sem ismeri fel; a hely a Hithpa`lel 1.b-je |
| M233 | H7812 | `Hiph'il/2/c` | `Hiph'il/2/c` | `Hithpa`lel/2/c` | „c. with לְ only: 1Sam 1:28” | **szeletelő-hiba** | **szakasztábla-hiba** | mint M223 |
| M226 | H5676 | `I -/1` | `I -/-/-` | `I -/1/B` | „1 … B. West Jordan … + יָ֫מָּה Josh 5:1” | — | **szakasztábla-hiba** | a hely az 1. pont B. csoportjában; a nagybetűs szintet a DT-F102a (a) szerint a fő mutató elhagyja, a tábla viszont az „1”-et is elveszti |
| M242 | H5973 | `h:מעם -/-/a` | `-/5/a` | `-/a` | „(a jelöletlen מֵעִם címszó) … after שׁאל to ask … Isa 7:11” | — | **szakasztábla-hiba** | a jelöletlen מֵעִם alcímszó saját a.-ja; a tábla az עִם 5.a-jába vonja |
| M249 | H2076 | `Pi'el/-` | `Pi'el/2` | `Pi`el/2` | „but 2 elsewhere of sacrifice to other deities … Hab 1:16” | **szeletelő-hiba** | — | a mondat belsejében álló „2” jelentésfej elvész |

Szeletelő-hiba 16: M003, M009, M011, M016, M027, M034, M036, M042, M050, M058, M143, M205, M208, M223, M233, M249. Szakasztábla-hiba 13: M002, M018,
M042, M056, M143, M194, M198, M201, M221, M223, M226, M233, M242 (+ M058 a 2.29-ből átvett `szakasz`-szal). (A jóváhagyás szerint az M143
kulcs-hiba, az M018 kizárva.)
**Okcsoportok** — szeletelő: kereszthivatkozásból hamis törzsfej (M003, M009, M027), gyakoriságszámhoz tapadt törzsnév (M011, M223, M233), mondat
belsejében álló vagy fej-glossza utáni jelentésfej (M034, M042, M205, M208, M249), elveszett törzsfej (M016), elcsúszott számozás (M050),
jelöletlen alcímszó (M058), alaktani betű (M143). Szakasztábla: elveszett törzsfej (M002, M221 Hiph`il; M223, M233 Hithpa`lel), visszautalásból
hamis fej (M198, M201), kimaradt betűfej (M056, M194), durvább szint (M018, M042, M226), alcímszó (M242), alaktani betű (M143).

## 3. Könyv/vers és szűrés (a jelentéspont-mércén kívül)

| azon | forrásidézet | ítélet |
|---|---|---|
| M091 H2370 (VERS) | „3 usually behold in dream or vision …, Ezra 4:20, accusative of thing 2:41” | **`forras_hiba`**: a forrás „Ezra 4:20”-at ír a Dán 4:20 helyett (a 4:14 valóban Ezsdrás); a 2:41 ezt a hibás könyvet örökli (Ezsd 2:41). **A TAHOT dönt** (javítva, ELLENOR_F102 4.): `lekerdez.py scan H2370 --szakasz "Dán 2:41"` → n=1 (2 szó-előfordulás) *(scope=range:Dán 2:41 \| forras=TAHOT_kivonat.tsv \| strong=H2370 \| n=1 \| ts=2026-11-09T17:15Z)*; `--szakasz "Ezsd 2:41"` → n=0 *(scope=range:Ezsd 2:41 \| forras=TAHOT_kivonat.tsv \| strong=H2370 \| n=0 \| ts=2026-11-09T17:15Z)*; a helyes Dán 2:41 — a kitöltés szerint |
| M015 H0473 (véletlen) | „Italy, … compare ᵑ7 … Ezek, Di Gen 10:4; Carthage = Elissa” | **szeletelő-hiba** (szűrés): „Di Gen 10:4” = Dillmann kommentárja a helyhez (`^` nélküli szerző-sigla, a szeletelő nem ismeri fel); a DT-F102e (B) szerint szűrendő |
| M214 H3707 (véletlen) | „— The phrase is characteristic of D …; see Dr^Intr 191; Deut 4:25 Holz^eini. Hexateuch 287” | **kitöltő-hiba** — *kérdéses*: a „Dr^Intr 191;” lezárt hivatkozás után a Deut 4:25 a kifejezés fent már idézett bibliai helye (a 2.b-ben), nem Driver lapszáma |
| M248 H4266 (véletlen) | „site unknown, see Di^Gn; הַמַּחֲנָ֑יִם כִּמְחֹלַת Cant 7:1 is put here by Ew Hi Öttli” | **szeletelő-hiba** (szűrés): bibliai idézet (Én 7:1); a `sigla_kozel` szűrte, mert a TAHOT nem igazolta |
| M156 H2022 (szűrt) | „but Ezek 18:6, 15 read perhaps הַדָּם for הרים compare RS^K 310 & 33:25” | **szeletelő-hiba** (szűrés): a 33:25 (Ez 33:25) bibliai hely, nem a sigla része |
| M188 H6994 (szűrt) | „(ה)ק ׳הר Isa 11:9 6t. Isa^2; Isa^3; Jer 31:23” | **szeletelő-hiba** (szűrés): az „Isa^2; Isa^3;” könyvrész-jel (Deutero-/Trito-Ézsaiás), nem kommentár; a Jer 31:23 bibliai |
| M039 H1121 (bizonytalan) | „1Chr 9:18; … 12:27; Nehemiah 10:40; הַלֵּוִי בְּנֵי 15:15; 24:30” | **nem hiba** (jóváhagyva: a mai óvatos szabály marad; `orokles_hibas`, bizonytalan): a közbeékelt Nehemiásnak nincs 15. fejezete; a helyes 1Krón 15:15 (a szeletelő `orokles_hibas`-t ad, a szabály szerint bizonytalan) |
| M127 H5203 (bizonytalan) | „1Sam 30:16 …; … Hosea 12:15 …; leave in charge of … sheep 17:20, 28; baggage 17:22” | **nem hiba** (jóváhagyva: a mai óvatos szabály marad; `orokles_hibas`, bizonytalan): mint M039 (1Sám 17:20) |
| M196 H1736 (bizonytalan) | „noun masculine^Gen 30:14 … 30:14; Cant 7:14; construct דּוּדָאֵי 30:14 3t.” | **nem hiba** (jóváhagyva: a mai óvatos szabály marad; `orokles_hibas`, bizonytalan): mint M039 (1Móz 30:14) |
| M060 H6920 (bizonytalan) | „— Σηλωρ, ᵐ5^L Σιλωρ, but 13:10; Jer 48:34 Ζογορ(α)” | **szeletelő-hiba** (jóváhagyva): a könyvnév nélküli hely a szócikkben utoljára megnevezett könyvre oldódik („compare Gen 19:20” → 1Móz 13:10); a szeletelő a könyvet örökli, de a TAHOT-kapu szűri (a TSV H6920-sora a Cóar szócikke, a TAHOT a H6920-at keresi: N-F102f) |

Szűrés, ítélet után: véletlen 197 → 199 kitöltő-hiba nélkül (M214), a szeletelő 2 hibája (M015, M248) marad; szűrt 23/25 (M156, M188 szeletelő-hiba);
bizonytalan 21/25 (M039, M127, M196 szeletelő-hiba — a közbeékelt, nem létező fejezetű könyv átugrása, az F102 (b) szabályának kiterjesztése
lenne —, M060 kulcs-ellentmondás).

## 4. Kérdéses (nem egyértelmű) tételek

- **M143** H1980: az „Imperative rarely a. הֲלוֺךְ” „a.”-ja alaktani felsorolás vagy szerkezeti alpont? Az ítélet: alaktani (mindkét kulcs hibás).
- **M018** H2534: a „Vbs. used with חֵמָה … 2. c.:” függelék címkéje jelentéspont-e; az ítélet a kulcsot és a kitöltést fogadja el (a tábla durvább).
- **M036** H3318: eldöntve (ELLENOR_F102 3.): **szeletelő-hiba** a szeletelő-oldalon, mint a seed-101 M162 (a forrásban van számozás, csak a „Qal” név hiányzik); a szakasztábla-oldalon `forras_hiba` (ELLENOR_F102_2 1.).
- **M091** H2370: a forrás „Ezra 4:20”-a könyvnév-hiba (Dán) — ~~a TAHOT itt nem dönt (… 0 találat mindkét versre)~~ **javítva** (ELLENOR_F102 4.; a korábbi állítás hamis volt és proveniencia nélküli): a TAHOT dönt, Dán 2:41 n=1, Ezsd 2:41 n=0 (l. 3.).
- **M214** H3707: a „Dr^Intr 191; Deut 4:25” Deut 4:25-je bibliai visszautalás (az ítélet) vagy Driver kommentár-helye.
- **M039, M127, M196**: a közbeékelt könyv utáni, abban nem létező fejezetű hely a korábbi könyvet folytatja-e — a mai szabály (bizonytalan) szándékosan óvatos.
- **M060** H6920: a könyvnév nélküli „13:10” (LXX-alak helye) — a forrás nem nevezi meg a könyvet.
