# Olvasói szint — tervezési napló

Rögzítve: 2026.09.08. Státusz: PILOT FOLYAMATBAN — a teljes cikken végzett próba 3 valódi problémát tárt fel, ezekre a második, célzott pilot-kör választ adott; a fokozat-korlátozás elve tisztázva (tartalom-típus, nem hossz alapján); script és formális sablon-fájl még nem készült.

## 1. Előzmény és probléma

A studyk és a lexikon-cikkek jelenleg munkapéldányok: a nekem (Basesoftnak) szóló napló-/folyamat-üzenetek (dátumok, "TSK-eredetű", audit-eredmények, döntési indoklások) keverednek az olvasói prózával — van, hogy egy mondaton belül is. Ez a lexikon-cikkeknél is fennáll, ott ráadásul több technikai infó (Strong-számok, táblázatok) is terheli a szöveget.

Konkrét példa a `Segitsegul_hivni_az_Urat_tematikus.md`-ből — három, egymástól eltérő, inkonzisztens napló-jelölési minta ugyanabban a fájlban:
- `*(új, 2026.09.06, TSK-eredetű)*` (dőlt zárójeles címke táblázat-cellában)
- `**2026.09.05-i teljes v12-compliance frissítés:**` (félkövér dátumos bekezdés-nyitó)
- `*(Módszertani megjegyzés, 2026.09.05: ...)*` (dőlt zárójeles bekezdés)

Ez a három forma egy script számára megbízhatóan nem különíthető el egymástól és a sima prózai dőlt/félkövér szövegtől.

## 2. Cél

Olyan olvasóbarát változatot előállítani a munkapéldányokból, ami:
- nyomon követhető, reprodukálható folyamat eredménye — nem persona/skill szabad improvizációja,
- skálázható (bármelyik studyra/lexikon-cikkre alkalmazható),
- tudományos irányból közérthetőbb irány felé mozdít,
- megőrzi a "konfigurációt" — a munkapéldány marad az egyetlen forrás, minden infó megmarad benne, az olvasói változat mindig ebből generálódik.

## 3. Első javaslat (chat, 2026.09.08) — elvetve

Három diszkrét szint: TUDOMÁNYOS (munkapéldány) / KÖZÉRTHETŐ (a meglévő `ISTENTISZT-001_OLVASHATO.md` mintája) / EGYSZERŰSÍTETT (rövidebb mondatok, minimalizált idegen szó). Basesoft elvetette: a TUDOMÁNYOS→KÖZÉRTHETŐ ugrás túl nagy, "szélső tengely" — finomabb, kisebb lépésközű hangolhatóság kell.

## 4. Véglegesített javaslat — 6 fokozat, tengelyenként külön rubrika

Négy, egymástól független paraméter, mindegyik **1-6 fokozattal** (az eredeti 1-5-ös javaslatból bővült, miután a pilot során kiderült: az 1. és a korábbi "2." fokozat között túl nagy volt az ugrás — egy közbülső fokozat pótolta a hiányt, ami miatt az egész skála 6 fokozatúra bővült):

| Fokozat | Terminológia | Apparátus | Mondatszerkezet | Indoklás-sűrűség |
|---|---|---|---|---|
| **1** | Eredeti írásjel + transzliteráció + jelentés minden előforduláskor | Teljes 【NAPLO】-jelölés + minden hivatkozott igehely kiírva | Hosszú, többszörösen alárendelt mondatok (3-4 tagmondat) | Teljes érvelési lánc + kizárt alternatívák + explicit záró-korlátozás ("amit ez NEM állít") |
| **2** | Írásjel csak első előfordulásnál, utána csak transzliteráció | 【NAPLO】 megmarad, hivatkozások tömörítve (csak fő igehelyek) | Rövidebb, de még összetett mondatok (max 2 tagmondat) | Teljes érvelési lánc, kizárt alternatívák említve, záró korlátozás rövidítve |
| **3** | Csak transzliteráció (dőlttel), írásjel sehol | 【NAPLO】 eltávolítva, igehelyek még mind felsorolva | Egyszerű mondatok, egy gondolat/mondat | Fő érvelés megmarad, korlátozó megjegyzés egy tagmondatban |
| **4** | Transzliteráció csak 1-2 kulcsszónál, többi körülírva | Igehelyek kategóriánként csoportosítva, 1 reprezentatív hivatkozással | Rövid, aktív szerkezetű mondatok | Csak a következtetés + egy rövid "miért" |
| **5** | Elvétve, egy-egy szónál marad meg a transzliteráció | Igehelyek csak névvel/számmal említve, konkrét hely nélkül | Nagyon rövid, tőmondat-közeli | Csak a következtetés, "miért" nélkül |
| **6** | Nincs idegen nyelvi elem, teljes magyar körülírás | Nincs hivatkozás-apparátus, csak az állítás | Minimál mondatok, kijelentés-lánc | Csak a tény kimondása, indoklás nélkül |

Fontos, pilot közben felismert tulajdonság: a tengelyek **nem feltétlenül lépnek együtt** egy adott mintaszövegben — pl. a Basesoft által legjobbnak jelölt próba (l. 8. pont, 3. mintaszöveg) valójában Terminológia≈1-2, Apparátus=3, Mondat=3, Indoklás=3 kombináció, nem egy tiszta "mindegyik=3". Ez megerősíti a többtengelyes megközelítés jogosságát a diszkrét szintekkel szemben.

Tervezett hívási forma (még nem implementálva): `olvasoi_valtozat_generalo.py --terminologia N --apparatus N --mondat N --indoklas N`

## 5. Kapcsolódó, megoldandó gyökér-probléma

A fenti négy paraméter csak akkor működtethető megbízhatóan, ha előbb:
- a napló-/folyamat-jelölés egységesítve van egyetlen, sosem máshol előforduló jelölőre (javaslat, a pilotban használva: `【NAPLO: ...】`),
- új írási szabály tiltja a mondaton belüli keveredést (próza és napló-infó soha ne legyen ugyanabban a mondatban) — enélkül semmilyen script nem tud kockázat nélkül szétválasztani.

A meglévő, lezárt studykban a napló-infó jelenleg vegyes formátumú (l. 1. pont) — ezeket egy egyszeri, retrospektív átalakítással kellene egységesíteni, mielőtt bármelyik script rajtuk futtatható lenne.

## 6. Döntés

Basesoft: "pilotozni kellene" — a 4 paraméter fokozatainak konkrét rubrikáját, az egységes napló-jelölést és a script-koncepciót **egy kiválasztott dokumentumon kell először kipróbálni**, mielőtt bármi bekerülne a `study-rules.md`-be vagy a `method-learnings.md`-be mint kötelező szabály.

## 7. Pilot állapota és következő lépés

**Elvégezve (chat, 2026.09.08):** a `Segitsegul_hivni_az_Urat_tematikus.md` A/B/C tipológia bekezdésén (l. 8. pont) mind a 6 fokozatra elkészült egy kézi, nem script-alapú próba-mintaszöveg, a 【NAPLO】-jelöléssel retrofitolt eredetivel együtt. Basesoft visszajelzése alapján a **3. fokozat** áll legközelebb az elképzeléshez.

**Még hátravan:**
- a rubrika kipróbálása **legalább még egy, eltérő jellegű** szövegrészen (pl. egy lexikon-cikk technikai bekezdésén, nem csak egy tematikus study prózai részén), mielőtt véglegesítenénk
- a napló-jelölés retrospektív bevezetése a `Segitsegul_hivni_az_Urat_tematikus.md` teljes szövegében (jelenleg csak az egy próba-bekezdésben történt meg, l. 8. pont)
- a `7_PaRDeS_olvasoi_szint_sablon.md` sablon-fájl elkészítése a rubrikából
- az `olvasoi_valtozat_generalo.py` script megtervezése — egyelőre nyitott, hogy a tengelyenkénti automatikus generálás egyáltalán megbízhatóan gépesíthető-e, vagy ez mindig kézi/LLM-asszisztált marad rögzített rubrika mentén

## 8. Pilot — próba-generálás a Segitsegul_hivni_az_Urat_tematikus.md A/B/C bekezdésén

**Eredeti szöveg (a study jelenlegi, élő verziójából):**
> **A 2Móz 33:19/34:5 eset tágabb mintázata — A/B/C tipológia** *(2026.09.06, a Motívumlexikon-pilot felismerése, itt visszaírva)*: a 2026.09.05-i audit során elutasított jelöltek (Ézs 43:1, 44:5, 45:3 — "Isten néven szólít egy embert") és a fenti "be nem sorolható" eset (2Móz 33:19/34:5 — "Isten kihirdeti saját nevét") együtt nézve nem véletlen zaj, hanem egy koherens, háromtagú mintázat részei...

**1. fokozat** (retrofitolt eredeti, egységes jelöléssel):
> **A 2Móz 33:19/34:5 eset tágabb mintázata — A/B/C tipológia** 【NAPLO: 2026.09.06, a Motívumlexikon-pilot felismerése, itt visszaírva】: a 2026.09.05-i audit során elutasított jelöltek (Ézs 43:1, 44:5, 45:3 — "Isten néven szólít egy embert") és a fenti "be nem sorolható" eset (2Móz 33:19/34:5) együtt nézve nem véletlen zaj, hanem egy koherens, háromtagú mintázat részei. A קָרָא (*kará*, "hívni") + שֵׁם (*shém*, "név") szerkezet ugyanazokkal a szavakkal, de szisztematikusan variálódó alany/tárgy-szereposztással három, egymástól élesen elkülönülő teológiai aktust fejez ki: **A** — fő motívum (alany: ember, tárgy: Isten neve — 15 eset); **B** (alany: Isten, tárgy: saját neve — 2Móz 33:19, 34:5); **C** (alany: Isten, tárgy: ember neve — Ézs 43:1, 44:5, 45:3, korábban elutasítva mint zaj). Amit ez NEM állít: hogy A/B/C motívum-szinten összetartozna — csak azt, hogy lexikai szerkezet szintjén van egy közös minta.

**2. fokozat:**
> **A 2Móz 33:19/34:5 eset tágabb mintázata — A/B/C tipológia** 【NAPLO: 2026.09.06, a Motívumlexikon-pilot felismerése, itt visszaírva】: a 2026.09.05-i audit két korábban elutasított jelöltjét (Ézs 43:1, 44:5, 45:3 — "Isten néven szólít egy embert") és a "be nem sorolható" 2Móz 33:19/34:5 esetet együtt kell nézni. Ezek nem véletlen zaj, hanem egy koherens, háromtagú mintázat részei. A קָרָא (*kará*, "hívni") + שֵׁם (*shém*, "név") szerkezet ugyanazokkal a szavakkal, de más alany/tárgy-szereposztással három, egymástól elkülönülő teológiai aktust fejez ki. **A** — fő motívum: az ember hívja segítségül Isten nevét (15 eset). **B**: Isten maga hirdeti ki a saját nevét (2Móz 33:19, 34:5). **C**: Isten nevez meg egy embert a saját nevén (Ézs 43:1, 44:5, 45:3 — korábban elutasítva mint zaj). Amit ez NEM állít: hogy A/B/C egy motívumhoz tartozna — csak azt, hogy lexikai szerkezet szintjén rokonok.

**3. fokozat (Basesoft szerint ez áll legközelebb a célhoz):**
> Van egy tágabb minta is a 2Móz 33:19/34:5 eset mögött. A קָרָא (*kará*, "hívni") + שֵׁם ("név") szókapcsolat itt háromféleképpen fordul elő: van, hogy az ember hívja segítségül Isten nevét (a study fő vonala, 15 eset); van, hogy Isten maga hirdeti ki a saját nevét (2Móz 33:19, 34:5); és van, hogy Isten nevez meg egy embert a saját nevén (Ézs 43:1, 44:5, 45:3 — korábban kizárva). A három eset ugyanannak a nyelvi szerkezetnek a szisztematikus variánsa. Fontos: ez nem jelenti, hogy egy motívumhoz tartoznának — csak azt, hogy nyelvi szerkezet szintjén rokonok.

**4. fokozat:**
> Van egy tágabb minta is a 2Móz 33:19/34:5 eset mögött. A *kará* ("hívni") + *shém* ("név") szókapcsolat háromféle szereposztásban jelenik meg. Az ember hívja segítségül Isten nevét — ez a fő téma, 15 eset. Isten maga hirdeti ki saját nevét (2Móz 33:19, 34:5). Isten néven nevez egy embert (Ézs 43:1, 44:5, 45:3). A három eset egyetlen szisztematikus minta három változata. A "B" eset tehát nem kivétel, hanem ennek a mintának a tagja.

**5. fokozat:**
> Van itt egy érdekes, tágabb minta is. A "hívni" és a "név" szó együtt háromféleképpen bukkan fel. Az ember hívja segítségül Isten nevét — ez a fő téma. Isten maga is kihirdeti a saját nevét Mózesnek. És Isten néven nevez egy embert. Mindhárom ugyanazt a mintát követi, csak az cserélődik, ki a cselekvő. Ez nem véletlen egybeesés.

**6. fokozat:**
> Van egy másik minta is. Van, amikor az ember szólítja Istent a nevén. Van, amikor Isten maga mondja ki a saját nevét. És van, amikor Isten nevez meg valakit. Mindhárom ugyanazt a szerkezetet követi. Ez nem véletlen.

Forrás: chat-alapú beszélgetés, 2026.09.08.

## 9. Második pilot-kör — teljes cikk + célzott utóvizsgálat

### 9.1 Teljes cikk próba (lokális, nem repóba szánt)

A `Segitsegul_hivni_az_Urat_tematikus.md` egy bekezdése után a teljes `ISTENTISZT-001_TUDOMANYOS.md` cikken (547 sor) is végigment a kézi pilot, mind a 6 fokozatban, ~22 prózai blokkon. A nyers forrásidézetek/táblázatok/diagram invariánsnak lettek jelölve (nem regiszterezhetők egy szótári idézet meghamisítása nélkül) — ez a döntés helyesnek bizonyult, később a felhasználó kifejezetten kérte az invariáns tartalom visszahelyezését is a fájlba (teljes, nem csak jelölt formában).

**Három probléma merült fel:**

1. **A 4 tengely a gyakorlatban nem volt független.** A pilot során minden blokknál mind a 4 paramétert (terminológia, apparátus, mondatszerkezet, indoklás-sűrűség) együtt, átlósan mozgattam (1,1,1,1 → 6,6,6,6) — nem teszteltem tudatosan aszimmetrikus kombinációkat. A négytengelyes függetlenség tehát még nincs ténylegesen bizonyítva.
2. **A magas fokozatok rövid, tömör blokkoknál tartalom nélkülivé váltak.** Első felvetés: a fokozat-tartományt a blokk *hosszához* kellene igazítani. Ezt a felhasználó elvetette (l. 9.2) — a hossz csak korrelált a problémával, nem az ok.
3. **A 【NAPLO】 jelölés határa nem egyértelmű.** Egy blokk (TSK "Miért fut most rendszeresen") folyamat-jegyzetnek lett jelölve, de vitatható, hogy egy tudományos olvasó számára ez inkább legitim módszertani indoklás — a "nekem szóló" vs. "az olvasónak is releváns módszertani megjegyzés" határvonal tisztázatlan maradt.

### 9.2 Felhasználói korrekció — tartalom-típus, nem hossz

A felhasználó pontosította: nem a blokk hossza, hanem a **tartalmának típusa** szabja meg, hány fokozatot bír el. Négy tartalom-típus azonosítva:

| Típus | Jellemző | Kockázat magas fokozaton | Javasolt tartomány |
|---|---|---|---|
| Ténymegállapítás | egyetlen állítás, nincs benne törékeny megkülönböztetés | alacsony | 1-6 |
| Módszertani indoklás | az érv ereje a forrás-redundanciából jön (pl. "3 független szótár") | a bizonyító erő elveszhet, ha a redundancia-tény kimarad | 1-6, de a konklúziónak (pl. "független megerősítés") minden fokozaton meg kell maradnia |
| Finom megkülönböztetés / határeset | a pontosság maga a tartalom (pl. névvel jelzett vitás olvasat) | a megkülönböztetés teljesen eltűnhet | 1-3 |
| Leíró/narratív összegzés | történetet mesél el, nincs törékeny elem | alacsony | 1-6 |

### 9.3 Célzott utóvizsgálat — 3 blokk, típus szerint kezelve

- **Sod + Rashi-vita** (határeset-típus, korlátozva 1-3-ra): a korábbi, korlátozás nélküli 4-6. fokozat ténylegesen elvesztette a Rashi-vita tényét (a névvel jelzett alternatív olvasatot) — ez tartalmi hiba volt, nem csak stiláris egyszerűsítés. Az új, 3-ra korlátozott verzió megtartja.
- **BDB H8034 "Jelentősége"** (ténymegállapítás-típus, teljes 1-6): a korábbi 6. fokozat ("A szó eredete nem ismert.") elvesztette, hogy ez egy *lezárt kutatási kérdés*, nem csak egy tény. Az új 6. fokozat ezt megtartja — a blokk típusa valójában elviseli a teljes 6 fokozatot, a korábbi hiba figyelmetlen vágás volt, nem a tartomány hibája.
- **BDB H7121 "Kiemelés jelentősége"** (módszertani indoklás-típus, teljes 1-6): a korábbi 6. fokozat elvesztette a *függetlenség* tényét (hogy a szótár tőlünk függetlenül jutott ugyanarra) — ez a bizonyító erő forrása. Az új 6. fokozat megtartja.

### 9.4 Végső felismerés

A korlátozás kulcsa nem egy fix fokozat-tartomány típusonként, hanem egy tudatos kérdés minden fokozat megírásakor: **"mi az az egy dolog, aminek itt muszáj megmaradnia?"** — a határeset-blokknál ez egy név (Rashi), a módszertani blokknál egy tény (függetlenség). A tartomány-korlátozás (1-3 vs. 1-6) csak a valódi határeset-típusnál indokolt; a másik három típusnál a teljes 6 fokozat is működik, ha ez a load-bearing elem tudatosan megmarad minden lépésben.

Forrás: chat-alapú beszélgetés, 2026.09.08 (második pilot-kör).
