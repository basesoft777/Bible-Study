# Kockázat-szűrő riport — 18 auditálatlan bővített tanulmány

*Készült: 2026.09.03, gépi szűréssel (`eszkozok/kockazat_szures_18_tanulmany.py`), a 🥈 2. prioritású átadási dokumentum alapján. Célja rangsor a 🥉 3. prioritáshoz (melyik 3-5 tanulmányt írjuk újra teljesen). Ez a riport NEM módosítja a study-fájlokat, csak elemzi őket.*

## Módszertan és korlátok

A szkript minden tanulmány "## 2. Eredeti nyelvi szöveg" táblázatából kinyeri a (vers, héber szó, Strong-szám) hármasokat, a "## 4. Kapcsolódó igehelyek" 🔗-blokkjaiból pedig az idézett igehelyeket. Négy jelzőt számít minden kulcsszóra:

1. **Origin-lánc-kockázat** — a `Strong_szotar.tsv` "Gyök/Származtatás" oszlopában hivatkozott másik Strong-szám, amit a study sehol nem említ.
2. **Poliszémia-kockázat** — a `TBESH.txt` (elsődleges) vagy `BDB_teljes_unabridged.tsv` (tartalék) alapján számolt jelentés-ágak nyers száma.
3. **Kereszthivatkozás/LXX-kockázat** — a study genezisi verseinek LXX görög Strong-jai és az idézett újszövetségi versek görög Strong-jai közötti metszet (a >800 globális NT-előfordulású, tisztán nyelvtani "ragasztószavak" — και, ὁ, δέ, αὐτοῦ stb. — kizárásával, mert enélkül a metszet szinte soha nem lenne üres); üres tartalmi metszet = piros zászló (lehetséges hamis pozitív), ritka (globálisan <200 előfordulású), nem-kulcsszóként szereplő közös szó = kiaknázatlan lehetőség.
4. **Teljes-előfordulás-rés** — a kulcsszó összes bibliai előfordulása (`TAHOT_kivonat.tsv` / `TAGNT_kivonat.tsv`) mínusz a study bárhol már idézett igehelyei.

**Korlátok:**
- A Markdown-táblázat-parszolás nem tökéletes minden fájlban — lásd alább, mely tanulmányoknál volt hiányos a kulcsszó-kinyerés.
- Az Origin-lánc jelző csak azt jelzi, hogy VAN kiaknázatlan hivatkozás — nem dönti el, hogy az tartalmilag érdemi-e (ahogy a celem esetében 9 a 11-ből nem hozott újat). Ez emberi értékelést igényel.
- A 3. jelző (LXX-híd) csak a Genezis-only LXX-pilot hatókörén belül működik — más ószövetségi könyvekre hivatkozó study-részek nem ellenőrizhetők ezzel.
- A 3. jelző stopword-szűrése (>800 előfordulás) heurisztikus — nem valódi morfológiai szűrés, ezért elméletileg kiszűrhet egy ritka esetben tényleg releváns, de nagyon gyakori szót (pl. θεός), és átengedhet egy határeset körüli szót. A piros zászlók emberi átnézést igényelnek, nem automatikus törlést.
- **Fontos:** a 3. jelző piros zászlója NEM jelenti automatikusan, hogy a study hibás kereszthivatkozást tartalmaz — csak azt, hogy nincs azonos Strong-szám a genezisi vers és az idézett újszövetségi vers görög szókészlete között. Minden piros zászlót a study saját szövegkörnyezetében kell ellenőrizni, mielőtt hibának minősítenénk. Példa: `1Moz_7v1-24_bovitett.md` Róm 9:27 találatánál emberi ellenőrzés (2026.09.03) megállapította, hogy a Strong-szám-szintű üres metszet ellenére VAN gyök-szintű lexikai kapcsolat (héber שאר-gyök: 1Móz 7:23 יִשָּׁאֶר / Ézs 10:20-22 שְׁאָר; görög λείπω-család: LXX 1Móz 7:23 κατελείφθη / Róm 9:27 ὑπόλειμμα) — a piros zászló technikailag jogos volt (nincs azonos Strong-szám), de "hamis pozitív"-ként minősíteni pontatlan lett volna. A study szövege 2026.09.03-tól ezt dokumentálja.
- A poliszémia-szám (2. jelző) nyers jelentés-ág-szám, nem azt méri, hogy a study melyik ágat választotta helyesen vagy helytelenül.
- A teljes-előfordulás-rés (4. jelző) csak azt méri, hogy egy igehely szó szerint idézve szerepel-e valahol a dokumentumban (bold `**Könyv fej:vers**` minta) — parafrázisokat nem ismeri fel.

---

## Összefoglaló táblázat

| Tanulmány | Legkockázatosabb kulcsszó(k) | Jelző 1 (Origin) | Jelző 2 (poliszémia) | Jelző 3 (LXX-kereszthiv.) | Jelző 4 (feltáratlan előford.) | Összbenyomás |
|---|---|---|---|---|---|---|
| `1Moz_2v4-7_bovitett.md` | נֶפֶשׁ חַיָּה (H2416), נֶפֶשׁ חַיָּה (H5315), עָפָר (H6083) | 7 kiaknázatlan hiv. | max 4 jelentés-ág | 2 kiaknázatlan | max 681 sosem idézett | **Közepes**: 7 kiaknázatlan Origin-lánc-hivatkozás (H2416→H2421, H3335→H3331, H5315→H5314...); 2 kulcsszó erősen poliszémikus (4+ jelentés-ág); 7 kulcsszónál 15+ soha nem idézett előfordulás maradt; 2 kiaknázatlan ritka LXX/NT-szó a metszetben. |
| `1Moz_2v8-25_bovitett.md` | לֹא־טוֹב (H3808), עֵץ הַדַּעַת טוֹב וָרָע (H6086), לֹא־טוֹב (H2896) | 11 kiaknázatlan hiv. | max 15 jelentés-ág | 3 kiaknázatlan | max 3948 sosem idézett | **Közepes**: 11 kiaknázatlan Origin-lánc-hivatkozás (H1320→H1319, H1588→H1598, H1847→H3045...); 3 kulcsszó erősen poliszémikus (4+ jelentés-ág); 14 kulcsszónál 15+ soha nem idézett előfordulás maradt; 3 kiaknázatlan ritka LXX/NT-szó a metszetben. |
| `1Moz_3v1-6_bovitett.md` | וַתִּתֵּן (H5414), יֹדְעֵי טוֹב וָרָע (H3045), פֶּן־תְּמֻתוּן (H4191) | 5 kiaknázatlan hiv. | max 9 jelentés-ág | 3 kiaknázatlan | max 1815 sosem idézett | **Közepes**: 5 kiaknázatlan Origin-lánc-hivatkozás (H5175→H5172, H6175→H6191, H6435→H6437...); 2 kulcsszó erősen poliszémikus (4+ jelentés-ág); 10 kulcsszónál 15+ soha nem idézett előfordulás maradt; 3 kiaknázatlan ritka LXX/NT-szó a metszetben. |
| `1Moz_3v7-24_bovitett.md` | שׁוּב (H7725), עֵינֵי (H5869), הַחֶרֶב (H2719) | 10 kiaknázatlan hiv. | max 1 jelentés-ág | nincs kockázat | max 952 sosem idézett | **Közepes**: 10 kiaknázatlan Origin-lánc-hivatkozás (H2233→H2232, H2290→H2296, H2719→H2717...); 11 kulcsszónál 15+ soha nem idézett előfordulás maradt. |
| `1Moz_4v1-24_bovitett.md` | דְּמֵי (H1818), חַטָּאת (H2403), מִנְחָה (H4503) | 5 kiaknázatlan hiv. | max 5 jelentés-ág | 8 kiaknázatlan | max 294 sosem idézett | **Közepes**: 5 kiaknázatlan Origin-lánc-hivatkozás (H1818→H119, H1818→H1826, H1892→H1891...); 1 kulcsszó erősen poliszémikus (4+ jelentés-ág); 10 kulcsszónál 15+ soha nem idézett előfordulás maradt; 8 kiaknázatlan ritka LXX/NT-szó a metszetben. |
| `1Moz_4v25-5v32_bovitett.md` | הִתְהַלֵּךְ (H1980), לָקַח (H3947), קָרָא בְשֵׁם (H7121) | 4 kiaknázatlan hiv. | max 2 jelentés-ág | 4 kiaknázatlan | max 1347 sosem idézett | **Közepes**: 4 kiaknázatlan Origin-lánc-hivatkozás (H1823→H1819, H1980→H3212, H5146→H5118...); 7 kulcsszónál 15+ soha nem idézett előfordulás maradt; 4 kiaknázatlan ritka LXX/NT-szó a metszetben. |
| `1Moz_6v1-8_bovitett.md` | בְּנֵי־הָאֱלֹהִים (H1121), בְּנוֹת הָאָדָם (H1323), רוּחַ (H7307) | 8 kiaknázatlan hiv. | max 5 jelentés-ág | nincs kockázat | max 3657 sosem idézett | **Közepes**: 8 kiaknázatlan Origin-lánc-hivatkozás (H1121→H1129, H1320→H1319, H1323→H1129...); 1 kulcsszó erősen poliszémikus (4+ jelentés-ág); 9 kulcsszónál 15+ soha nem idézett előfordulás maradt. |
| `1Moz_6v9-22_bovitett.md` | הִתְהַלֵּךְ (H1980), נֶפֶשׁ חַיָּה (H5315), נֶפֶשׁ חַיָּה (H2416) | 9 kiaknázatlan hiv. | max 4 jelentés-ág | nincs kockázat | max 1346 sosem idézett | **Közepes**: 9 kiaknázatlan Origin-lánc-hivatkozás (H1285→H1254, H1285→H1262, H1980→H3212...); 1 kulcsszó erősen poliszémikus (4+ jelentés-ág); 9 kulcsszónál 15+ soha nem idézett előfordulás maradt. |
| `1Moz_7v1-24_bovitett.md` | נִשְׁמַת רוּחַ חַיִּים (H2416), אֲרֻבֹּת הַשָּׁמַיִם (H8064), נִשְׁמַת רוּחַ חַיִּים (H7307) | 5 kiaknázatlan hiv. | max 4 jelentés-ág | 1 piros zászló | max 448 sosem idézett | **Magas**: 5 kiaknázatlan Origin-lánc-hivatkozás (H2416→H2421, H2889→H2891, H5397→H5395...); 1 NT-idézet LXX-metszete üres (lehetséges hamis pozitív kereszthivatkozás: Róm 9:27); 1 kulcsszó erősen poliszémikus (4+ jelentés-ág); 8 kulcsszónál 15+ soha nem idézett előfordulás maradt. |
| `1Moz_8v1-22_bovitett.md` | רוּחַ (H7307), מִזְבֵּחַ (H4196), זָכַר (H2142) | 8 kiaknázatlan hiv. | max 2 jelentés-ág | nincs kockázat | max 346 sosem idézett | **Közepes**: 8 kiaknázatlan Origin-lánc-hivatkozás (H2132→H2099, H2142→H2145, H3336→H3335...); 8 kulcsszónál 15+ soha nem idézett előfordulás maradt. |
| `1Moz_9v1-17_bovitett.md` | עוֹלָם (H5769), דָּם (H1818), בְּרִית (H1285) | 8 kiaknázatlan hiv. | max 2 jelentés-ág | nincs kockázat | max 412 sosem idézett | **Közepes**: 8 kiaknázatlan Origin-lánc-hivatkozás (H1285→H1254, H1285→H1262, H1818→H119...); 6 kulcsszónál 15+ soha nem idézett előfordulás maradt. |
| `1Moz_9v18-29_bovitett.md` | וַיִּתְגַּל (H1540), עֶרְוָה (H6172), אֱלֹהֵי שֵׁם (H8035) | 2 kiaknázatlan hiv. | max 2 jelentés-ág | nincs kockázat | max 166 sosem idézett | **Közepes**: 2 kiaknázatlan Origin-lánc-hivatkozás (H6172→H6168, H8035→H8034); 4 kulcsszónál 15+ soha nem idézett előfordulás maradt. |
| `1Moz_10v1-11v32_bovitett.md` | שֵׁם (H8034), שָׂפָה אֶחָת (H8193), גִּבֹּר (H1368) | 11 kiaknázatlan hiv. | max 2 jelentés-ág | 2 kiaknázatlan | max 769 sosem idézett | **Közepes**: 11 kiaknázatlan Origin-lánc-hivatkozás (H1101→H1098, H1368→H1397, H4026→H1431...); 9 kulcsszónál 15+ soha nem idézett előfordulás maradt; 2 kiaknázatlan ritka LXX/NT-szó a metszetben; a kulcsszó-táblázat kinyerése részben vagy teljesen sikertelen volt — az alábbi jelzők hiányosak. |
| `1Moz_12v1-20_bovitett.md` | לֶךְ־לְךָ֛ (H1980), נְגָעִים גְּדֹלִים (H1419), קָרָא בְשֵׁם יְהוָה (H8034) | 10 kiaknázatlan hiv. | max 9 jelentés-ág | 2 kiaknázatlan | max 1347 sosem idézett | **Közepes**: 10 kiaknázatlan Origin-lánc-hivatkozás (H1419→H1431, H1471→H1465, H1980→H3212...); 3 kulcsszó erősen poliszémikus (4+ jelentés-ág); 12 kulcsszónál 15+ soha nem idézett előfordulás maradt; 2 kiaknázatlan ritka LXX/NT-szó a metszetben. |
| `1Moz_13v1-18_bovitett.md` | קָרָא בְשֵׁם יְהוָה (H3068), וַיִּשָּׂא־ל֣וֹט אֶת־עֵינָ֗יו וַיַּרְא (H5869), וַיִּשָּׂא־ל֣וֹט אֶת־עֵינָ֗יו וַיַּרְא (H5375) | 6 kiaknázatlan hiv. | max 8 jelentés-ág | nincs kockázat | max 5523 sosem idézett | **Közepes**: 6 kiaknázatlan Origin-lánc-hivatkozás (H2400→H2398, H3068→H1961, H4196→H2076...); 1 kulcsszó erősen poliszémikus (4+ jelentés-ág); 13 kulcsszónál 15+ soha nem idézett előfordulás maradt. |
| `1Moz_14_bovitett.md` | נָשָׂאתִי יָדִי (H3027), כֹּהֵן (H3548), נָשָׂאתִי יָדִי (H5375) | 6 kiaknázatlan hiv. | max 4 jelentés-ág | 3 kiaknázatlan | max 1446 sosem idézett | **Közepes**: 6 kiaknázatlan Origin-lánc-hivatkozás (H2593→H2596, H3548→H3547, H3899→H1036...); 1 kulcsszó erősen poliszémikus (4+ jelentés-ág); 8 kulcsszónál 15+ soha nem idézett előfordulás maradt; 3 kiaknázatlan ritka LXX/NT-szó a metszetben; a kulcsszó-táblázat kinyerése részben vagy teljesen sikertelen volt — az alábbi jelzők hiányosak. |
| `1Moz_15_bovitett.md` | בְּרִית (H1285), עָוֺן (H5771), צְדָקָה (H6666) | 8 kiaknázatlan hiv. | max 4 jelentés-ág | 2 kiaknázatlan | max 261 sosem idézett | **Közepes**: 8 kiaknázatlan Origin-lánc-hivatkozás (H1285→H1254, H1285→H1262, H1616→H1481...); 1 kulcsszó erősen poliszémikus (4+ jelentés-ág); 8 kulcsszónál 15+ soha nem idézett előfordulás maradt; 2 kiaknázatlan ritka LXX/NT-szó a metszetben. |
| `1Moz_16_bovitett.md` | מַלְאַךְ יְהוָה (H3068), מַלְאַךְ יְהוָה (H4397), עָנָה (Piél) (H6031) | 4 kiaknázatlan hiv. | max 6 jelentés-ág | 1 kiaknázatlan | max 5522 sosem idézett | **Közepes**: 4 kiaknázatlan Origin-lánc-hivatkozás (H2555→H2554, H3068→H1961, H3458→H8085...); 2 kulcsszó erősen poliszémikus (4+ jelentés-ág); 6 kulcsszónál 15+ soha nem idézett előfordulás maradt; 1 kiaknázatlan ritka LXX/NT-szó a metszetben. |

---

## Nyers, nem-szubjektív összesítő táblázat

*Csak számok — saját súlyozáshoz.*

| Tanulmány | Kulcsszavak száma | Igehely-hivatkozások száma | J1 db | J2 max | J2 átlag | J3 piros zászló | J3 kiaknázatlan | J4 max rés | J4 összes rés |
|---|---|---|---|---|---|---|---|---|---|
| `1Moz_2v4-7_bovitett.md` | 7 | 4 | 7 | 4 | 1.8 | 0 | 2 | 681 | 1800 |
| `1Moz_2v8-25_bovitett.md` | 14 | 4 | 11 | 15 | 2.9 | 0 | 3 | 3948 | 6798 |
| `1Moz_3v1-6_bovitett.md` | 8 | 4 | 5 | 9 | 2.6 | 0 | 3 | 1815 | 4844 |
| `1Moz_3v7-24_bovitett.md` | 19 | 5 | 10 | 1 | 1.0 | 0 | 0 | 952 | 2752 |
| `1Moz_4v1-24_bovitett.md` | 12 | 4 | 5 | 5 | 1.5 | 0 | 8 | 294 | 1142 |
| `1Moz_4v25-5v32_bovitett.md` | 7 | 3 | 4 | 2 | 1.1 | 0 | 4 | 1347 | 3149 |
| `1Moz_6v1-8_bovitett.md` | 11 | 3 | 8 | 5 | 1.9 | 0 | 0 | 3657 | 5121 |
| `1Moz_6v9-22_bovitett.md` | 10 | 4 | 9 | 4 | 1.4 | 0 | 0 | 1346 | 3252 |
| `1Moz_7v1-24_bovitett.md` | 6 | 4 | 5 | 4 | 1.5 | 1 | 0 | 448 | 1541 |
| `1Moz_8v1-22_bovitett.md` | 7 | 6 | 8 | 2 | 1.2 | 0 | 0 | 346 | 1298 |
| `1Moz_9v1-17_bovitett.md` | 7 | 5 | 8 | 2 | 1.2 | 0 | 0 | 412 | 1278 |
| `1Moz_9v18-29_bovitett.md` | 6 | 4 | 2 | 2 | 1.5 | 0 | 0 | 166 | 248 |
| `1Moz_10v1-11v32_bovitett.md` | 9 | 4 | 11 | 2 | 1.5 | 0 | 2 | 769 | 1371 |
| `1Moz_12v1-20_bovitett.md` | 9 | 3 | 10 | 9 | 3.1 | 0 | 2 | 1347 | 5159 |
| `1Moz_13v1-18_bovitett.md` | 7 | 2 | 6 | 8 | 2.0 | 0 | 0 | 5523 | 11714 |
| `1Moz_14_bovitett.md` | 7 | 3 | 6 | 4 | 1.4 | 0 | 3 | 1446 | 3272 |
| `1Moz_15_bovitett.md` | 11 | 2 | 8 | 4 | 1.5 | 0 | 2 | 261 | 989 |
| `1Moz_16_bovitett.md` | 7 | 3 | 4 | 6 | 2.3 | 0 | 1 | 5522 | 5944 |

---

## Részletes jelző-1 (Origin-lánc) találatok

**`1Moz_2v4-7_bovitett.md`**
- `H8435` (תוֹלְדוֹת) → hivatkozott, de nem tárgyalt `H3205`
- `H3335` (יָצַר (וַיִּיצֶר)) → hivatkozott, de nem tárgyalt `H3331`
- `H6083` (עָפָר) → hivatkozott, de nem tárgyalt `H6080`
- `H5397` (נִשְׁמַת חַיִּים) → hivatkozott, de nem tárgyalt `H5395`
- `H2416` (נִשְׁמַת חַיִּים) → hivatkozott, de nem tárgyalt `H2421`
- `H5315` (נֶפֶשׁ חַיָּה) → hivatkozott, de nem tárgyalt `H5314`
- `H2416` (נֶפֶשׁ חַיָּה) → hivatkozott, de nem tárgyalt `H2421`

**`1Moz_2v8-25_bovitett.md`**
- `H1588` (גַּן) → hivatkozott, de nem tárgyalt `H1598`
- `H5731` (עֵדֶן) → hivatkozott, de nem tárgyalt `H5730`
- `H6086` (עֵץ הַחַיִּים) → hivatkozott, de nem tárgyalt `H6095`
- `H2416` (עֵץ הַחַיִּים) → hivatkozott, de nem tárgyalt `H2421`
- `H6086` (עֵץ הַדַּעַת טוֹב וָרָע) → hivatkozott, de nem tárgyalt `H6095`
- `H1847` (עֵץ הַדַּעַת טוֹב וָרָע) → hivatkozott, de nem tárgyalt `H3045`
- `H5828` (עֵזֶר כְּנֶגְדּוֹ) → hivatkozott, de nem tárgyalt `H5826`
- `H5048` (עֵזֶר כְּנֶגְדּוֹ) → hivatkozott, de nem tárgyalt `H5046`
- `H6763` (צֵלָע) → hivatkozott, de nem tárgyalt `H6760`
- `H1320` (בָּשָׂר אֶחָד) → hivatkozott, de nem tárgyalt `H1319`
- `H6174` (עֲרוּמִּים) → hivatkozott, de nem tárgyalt `H6191`

**`1Moz_3v1-6_bovitett.md`**
- `H5175` (נָחָשׁ) → hivatkozott, de nem tárgyalt `H5172`
- `H6175` (עָרוּם) → hivatkozott, de nem tárgyalt `H6191`
- `H6435` (פֶּן־תְּמֻתוּן) → hivatkozott, de nem tárgyalt `H6437`
- `H7451` (יֹדְעֵי טוֹב וָרָע) → hivatkozott, de nem tárgyalt `H7489`
- `H8378` (תַאֲוָה) → hivatkozott, de nem tárgyalt `H183`

**`1Moz_3v7-24_bovitett.md`**
- `H6174` (עֵרֻמִּם) → hivatkozott, de nem tárgyalt `H6191`
- `H2290` (חֲגֹרֹת) → hivatkozott, de nem tárgyalt `H2296`
- `H2233` (זֶרַע) → hivatkozott, de nem tárgyalt `H2232`
- `H6119` (עָקֵב) → hivatkozott, de nem tárgyalt `H6117`
- `H6093` (עִצְּבוֹנֵךְ) → hivatkozott, de nem tárgyalt `H6087`
- `H6083` (עָפָר) → hivatkozott, de nem tárgyalt `H6080`
- `H3801` (כָּתְנוֹת) → hivatkozott, de nem tárgyalt `H3802`
- `H5785` (עוֹר) → hivatkozott, de nem tárgyalt `H5783`
- `H3858` (לַהַט) → hivatkozott, de nem tárgyalt `H3857`
- `H2719` (הַחֶרֶב) → hivatkozott, de nem tárgyalt `H2717`

**`1Moz_4v1-24_bovitett.md`**
- `H1892` (הֶבֶל) → hivatkozott, de nem tárgyalt `H1891`
- `H2734` (חָרָה) → hivatkozott, de nem tárgyalt `H2787`
- `H2403` (חַטָּאת) → hivatkozott, de nem tárgyalt `H2398`
- `H1818` (דְּמֵי) → hivatkozott, de nem tárgyalt `H1826`
- `H1818` (דְּמֵי) → hivatkozott, de nem tárgyalt `H119`

**`1Moz_4v25-5v32_bovitett.md`**
- `H8435` (תּוֹלְדֹת) → hivatkozott, de nem tárgyalt `H3205`
- `H1823` (דְּמוּת) → hivatkozott, de nem tárgyalt `H1819`
- `H1980` (הִתְהַלֵּךְ) → hivatkozott, de nem tárgyalt `H3212`
- `H5146` (נֹחַ / יְנַחֲמֵנוּ) → hivatkozott, de nem tárgyalt `H5118`

**`1Moz_6v1-8_bovitett.md`**
- `H1121` (בְּנֵי־הָאֱלֹהִים) → hivatkozott, de nem tárgyalt `H1129`
- `H1323` (בְּנוֹת הָאָדָם) → hivatkozott, de nem tárgyalt `H1129`
- `H7307` (רוּחַ) → hivatkozott, de nem tárgyalt `H7306`
- `H1320` (בָּשָׂר) → hivatkozott, de nem tárgyalt `H1319`
- `H5303` (נְפִלִים) → hivatkozott, de nem tárgyalt `H5307`
- `H1368` (גִּבֹּרִים) → hivatkozott, de nem tárgyalt `H1397`
- `H3336` (יֵצֶר) → hivatkozott, de nem tárgyalt `H3335`
- `H2580` (חֵן) → hivatkozott, de nem tárgyalt `H2603`

**`1Moz_6v9-22_bovitett.md`**
- `H6662` (צַדִּיק) → hivatkozott, de nem tárgyalt `H6663`
- `H8549` (תָּמִים) → hivatkozott, de nem tárgyalt `H8552`
- `H1980` (הִתְהַלֵּךְ) → hivatkozott, de nem tárgyalt `H3212`
- `H2555` (חָמָס) → hivatkozott, de nem tárgyalt `H2554`
- `H3999` (מַבּוּל) → hivatkozott, de nem tárgyalt `H2986`
- `H5315` (נֶפֶשׁ חַיָּה) → hivatkozott, de nem tárgyalt `H5314`
- `H2416` (נֶפֶשׁ חַיָּה) → hivatkozott, de nem tárgyalt `H2421`
- `H1285` (בְּרִית) → hivatkozott, de nem tárgyalt `H1262`
- `H1285` (בְּרִית) → hivatkozott, de nem tárgyalt `H1254`

**`1Moz_7v1-24_bovitett.md`**
- `H2889` (טָהוֹר) → hivatkozott, de nem tárgyalt `H2891`
- `H8415` (תְּהוֹם) → hivatkozott, de nem tárgyalt `H1949`
- `H5397` (נִשְׁמַת רוּחַ חַיִּים) → hivatkozott, de nem tárgyalt `H5395`
- `H7307` (נִשְׁמַת רוּחַ חַיִּים) → hivatkozott, de nem tárgyalt `H7306`
- `H2416` (נִשְׁמַת רוּחַ חַיִּים) → hivatkozott, de nem tárgyalt `H2421`

**`1Moz_8v1-22_bovitett.md`**
- `H2142` (זָכַר) → hivatkozott, de nem tárgyalt `H2145`
- `H7307` (רוּחַ) → hivatkozott, de nem tárgyalt `H7306`
- `H5929` (עֲלֵה־זַיִת) → hivatkozott, de nem tárgyalt `H5927`
- `H2132` (עֲלֵה־זַיִת) → hivatkozott, de nem tárgyalt `H2099`
- `H4196` (מִזְבֵּחַ) → hivatkozott, de nem tárgyalt `H2076`
- `H7381` (רֵיחַ הַנִּיחֹחַ) → hivatkozott, de nem tárgyalt `H7306`
- `H5207` (רֵיחַ הַנִּיחֹחַ) → hivatkozott, de nem tárgyalt `H5117`
- `H3336` (יֵצֶר) → hivatkozott, de nem tárgyalt `H3335`

**`1Moz_9v1-17_bovitett.md`**
- `H1818` (דָּם) → hivatkozott, de nem tárgyalt `H1826`
- `H1818` (דָּם) → hivatkozott, de nem tárgyalt `H119`
- `H1285` (בְּרִית) → hivatkozott, de nem tárgyalt `H1262`
- `H1285` (בְּרִית) → hivatkozott, de nem tárgyalt `H1254`
- `H7198` (קֶשֶׁת) → hivatkozott, de nem tárgyalt `H7185`
- `H7198` (קֶשֶׁת) → hivatkozott, de nem tárgyalt `H6983`
- `H2142` (זָכַר) → hivatkozott, de nem tárgyalt `H2145`
- `H5769` (עוֹלָם) → hivatkozott, de nem tárgyalt `H5956`

**`1Moz_9v18-29_bovitett.md`**
- `H6172` (עֶרְוָה) → hivatkozott, de nem tárgyalt `H6168`
- `H8035` (אֱלֹהֵי שֵׁם) → hivatkozott, de nem tárgyalt `H8034`

**`1Moz_10v1-11v32_bovitett.md`**
- `H8435` (תּוֹלְדֹת) → hivatkozott, de nem tárgyalt `H3205`
- `H1368` (גִּבֹּר) → hivatkozott, de nem tárgyalt `H1397`
- `H4467` (מַמְלָכָה) → hivatkozott, de nem tárgyalt `H4427`
- `H8193` (שָׂפָה אֶחָת) → hivatkozott, de nem tárgyalt `H5595`
- `H8193` (שָׂפָה אֶחָת) → hivatkozott, de nem tárgyalt `H8192`
- `H8193` (שָׂפָה אֶחָת) → hivatkozott, de nem tárgyalt `H5490`
- `H4026` (מִגְדָּל) → hivatkozott, de nem tárgyalt `H1431`
- `H8034` (שֵׁם) → hivatkozott, de nem tárgyalt `H7760`
- `H8034` (שֵׁם) → hivatkozott, de nem tárgyalt `H8064`
- `H1101` (נָבְלָה) → hivatkozott, de nem tárgyalt `H1098`
- `H1101` (בָּלַל) → hivatkozott, de nem tárgyalt `H1098`

**`1Moz_12v1-20_bovitett.md`**
- `H1980` (לֶךְ־לְךָ֛) → hivatkozott, de nem tárgyalt `H3212`
- `H4138` (מוֹלֶדֶת) → hivatkozott, de nem tárgyalt `H3205`
- `H1471` (גּוֹי גָּדוֹל) → hivatkozott, de nem tárgyalt `H1465`
- `H1419` (גּוֹי גָּדוֹל) → hivatkozott, de nem tárgyalt `H1431`
- `H4196` (מִזְבֵּחַ) → hivatkozott, de nem tárgyalt `H2076`
- `H8034` (קָרָא בְשֵׁם יְהוָה) → hivatkozott, de nem tárgyalt `H7760`
- `H8034` (קָרָא בְשֵׁם יְהוָה) → hivatkozott, de nem tárgyalt `H8064`
- `H7458` (רָעָב) → hivatkozott, de nem tárgyalt `H7456`
- `H5061` (נְגָעִים גְּדֹלִים) → hivatkozott, de nem tárgyalt `H5060`
- `H1419` (נְגָעִים גְּדֹלִים) → hivatkozott, de nem tárgyalt `H1431`

**`1Moz_13v1-18_bovitett.md`**
- `H3068` (קָרָא בְשֵׁם יְהוָה) → hivatkozott, de nem tárgyalt `H1961`
- `H4945` (מַשְׁקֶה) → hivatkozott, de nem tárgyalt `H8248`
- `H7451` (רָעִ֛ים וְחַטָּאִ֖ים) → hivatkozott, de nem tárgyalt `H7489`
- `H2400` (רָעִ֛ים וְחַטָּאִ֖ים) → hivatkozott, de nem tárgyalt `H2398`
- `H6083` (כַּעֲפַ֣ר הָאָ֑רֶץ) → hivatkozott, de nem tárgyalt `H6080`
- `H4196` (וַיִּֽבֶן־שָׁ֥ם מִזְבֵּ֖חַ) → hivatkozott, de nem tárgyalt `H2076`

**`1Moz_14_bovitett.md`**
- `H2593` (חֲנִיכָיו) → hivatkozott, de nem tárgyalt `H2596`
- `H3548` (כֹּהֵן) → hivatkozott, de nem tárgyalt `H3547`
- `H3899` (לֶחֶם וָיַיִן) → hivatkozott, de nem tárgyalt `H3898`
- `H3899` (לֶחֶם וָיַיִן) → hivatkozott, de nem tárgyalt `H1036`
- `H5945` (אֵל עֶלְיוֹן) → hivatkozott, de nem tárgyalt `H5927`
- `H4643` (מַעֲשֵׂר) → hivatkozott, de nem tárgyalt `H6240`

**`1Moz_15_bovitett.md`**
- `H4043` (מָגֵן) → hivatkozott, de nem tárgyalt `H1598`
- `H7939` (שָׂכָר) → hivatkozott, de nem tárgyalt `H7936`
- `H6666` (צְדָקָה) → hivatkozott, de nem tárgyalt `H6663`
- `H8639` (תַּרְדֵּמָה) → hivatkozott, de nem tárgyalt `H7290`
- `H1616` (גֵּר) → hivatkozott, de nem tárgyalt `H1481`
- `H5771` (עָוֺן) → hivatkozott, de nem tárgyalt `H5753`
- `H1285` (בְּרִית) → hivatkozott, de nem tárgyalt `H1262`
- `H1285` (בְּרִית) → hivatkozott, de nem tárgyalt `H1254`

**`1Moz_16_bovitett.md`**
- `H2555` (חָמָס) → hivatkozott, de nem tárgyalt `H2554`
- `H3068` (מַלְאַךְ יְהוָה) → hivatkozott, de nem tárgyalt `H1961`
- `H3458` (יִשְׁמָעֵאל) → hivatkozott, de nem tárgyalt `H8085`
- `H7210` (אֵל רֳאִי) → hivatkozott, de nem tárgyalt `H7200`

---

## Részletes jelző-3 (LXX-kereszthivatkozás) találatok

**`1Moz_2v4-7_bovitett.md`**
- 🟡 kiaknázatlan: **1Kor 15:45** ↔ `G5590` (globális NT-előfordulás: 106) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **1Kor 15:45** ↔ `G2198` (globális NT-előfordulás: 143) — a study nem nevezi meg kulcsszóként

**`1Moz_2v8-25_bovitett.md`**
- 🟡 kiaknázatlan: **Jel 22:1-2** ↔ `G2222` (globális NT-előfordulás: 136) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Jel 22:1-2** ↔ `G3319` (globális NT-előfordulás: 60) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Jel 22:1-2** ↔ `G3586` (globális NT-előfordulás: 20) — a study nem nevezi meg kulcsszóként

**`1Moz_3v1-6_bovitett.md`**
- 🟡 kiaknázatlan: **2Kor 11:3** ↔ `G3789` (globális NT-előfordulás: 14) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **1Ján 2:16** ↔ `G3788` (globális NT-előfordulás: 101) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Jel 12:9** ↔ `G3789` (globális NT-előfordulás: 14) — a study nem nevezi meg kulcsszóként

**`1Moz_4v1-24_bovitett.md`**
- 🟡 kiaknázatlan: **Zsid 11:4** ↔ `G0006` (globális NT-előfordulás: 4) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 11:4** ↔ `G1435` (globális NT-előfordulás: 19) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 11:4** ↔ `G4374` (globális NT-előfordulás: 48) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 11:4** ↔ `G2378` (globális NT-előfordulás: 29) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 11:4** ↔ `G2535` (globális NT-előfordulás: 3) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **1Ján 3:12** ↔ `G2535` (globális NT-előfordulás: 3) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 12:24** ↔ `G0129` (globális NT-előfordulás: 100) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 12:24** ↔ `G0006` (globális NT-előfordulás: 4) — a study nem nevezi meg kulcsszóként

**`1Moz_4v25-5v32_bovitett.md`**
- 🟡 kiaknázatlan: **Zsid 11:5** ↔ `G2100` (globális NT-előfordulás: 3) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 11:5** ↔ `G1802` (globális NT-előfordulás: 3) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 11:5** ↔ `G3346` (globális NT-előfordulás: 6) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 11:5** ↔ `G2147` (globális NT-előfordulás: 177) — a study nem nevezi meg kulcsszóként

**`1Moz_7v1-24_bovitett.md`**
- 🔴 piros zászló: **Róm 9:27** — üres a metszet a genezisi vers(ek) LXX görög Strong-jaival (lehetséges hamis pozitív kereszthivatkozás)

**`1Moz_10v1-11v32_bovitett.md`**
- 🟡 kiaknázatlan: **ApCsel 2:4** ↔ `G0757` (globális NT-előfordulás: 86) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **ApCsel 2:4** ↔ `G1100` (globális NT-előfordulás: 50) — a study nem nevezi meg kulcsszóként

**`1Moz_12v1-20_bovitett.md`**
- 🟡 kiaknázatlan: **Gal 3:8** ↔ `G1484` (globális NT-előfordulás: 164) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Gal 3:8** ↔ `G1757` (globális NT-előfordulás: 2) — a study nem nevezi meg kulcsszóként

**`1Moz_14_bovitett.md`**
- 🟡 kiaknázatlan: **Zsid 7:2** ↔ `G0935` (globális NT-előfordulás: 115) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 7:2** ↔ `G4532` (globális NT-előfordulás: 2) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Zsid 7:2** ↔ `G1182` (globális NT-előfordulás: 7) — a study nem nevezi meg kulcsszóként

**`1Moz_15_bovitett.md`**
- 🟡 kiaknázatlan: **Róm 4:3** ↔ `G1343` (globális NT-előfordulás: 94) — a study nem nevezi meg kulcsszóként
- 🟡 kiaknázatlan: **Róm 4:3** ↔ `G3049` (globális NT-előfordulás: 41) — a study nem nevezi meg kulcsszóként

**`1Moz_16_bovitett.md`**
- 🟡 kiaknázatlan: **Gal 4:24-25** ↔ `G0028` (globális NT-előfordulás: 2) — a study nem nevezi meg kulcsszóként

---

## Sikertelen vagy hiányos kulcsszó-kinyerés

- `1Moz_10v1-11v32_bovitett.md` — kulcsszó-táblázat kinyerése hiányos vagy sikertelen
- `1Moz_14_bovitett.md` — kulcsszó-táblázat kinyerése hiányos vagy sikertelen
