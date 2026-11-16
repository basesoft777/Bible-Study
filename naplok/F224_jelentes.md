# F224 — A cikkírás új menete: jelentés

*Végrehajtó: claude-opus-5-5 (a kért `opus`, egyezik). Ág: `claude/f224-cikkiras-uj-menet`, alap: main `56da26c0`. A brief: `F224_CIKKIRAS_UJ_MENET_BRIEF.md`.*

## Ütközésvizsgálat (a fájlírás előtt, 2026-11-15)

`python eszkozok/feladatok.py fuggesek` és a nyitott PR-ok fájllistája (`gh api …/pulls/<n>/files`, lapozva):
- **#729 (F218a)** a brief `ir` mezőjéből két fájlt ír: `adat/SEMA.md` és `sablonok/9_PaRDeS_motivum_forras_sablon.md`. Ezekhez ez az ág nem nyúl a #729 merge-éig (a brief `fugg: [218]`): az F224.6 (érvnapló) és az F224.5, F224.11 SEMA-szakasza vár.
- **#725 (F217.1)** egyik fájlunkat sem írja.
- A Károli-csomagok PR-ja (#737) mergelve.

## Menet tételenként

### F224.1 — Az állítás-ellenőr szerepfájlja
Új `.claude/agents/allitas-ellenor.md` (`model: sonnet`, 0. lépés: modell-ellenőrzés; íróeszköz nincs). A hét kötelező kérdés a mérés példáival (ISTENTISZT K50 = a lektor 1. tétele, Zsolt 116 = 2., „hét helyből öt” = 10. (K25), Jézus Krisztus neve = 3.; HAMART erec/adámá, K39, K47); a 7. kérdés példája a lektor 6. tétele. A példák szövege a `2ae45dae:naplok/KIADAS_ISTENTISZT-001_lektor.md` és a mérés F2-mellékletei szerint. Ítélet az állítmányra, „nem” válasznál nem lehet „igazolt”; bizonyítéktípus; kétirányú tilalom; kimenet: a hívó menti a `naplok/ALLITAS_<ID>_itelet.md`-be. A menetbeli hely: `MUNKAMENET.md` C) F2 sor (F224.8).
*(proveniencia: scope=TERV_CIKKIRAS_v3 3. szakasz; MERES_VISSZAJATSZAS_2026-11-15 4–5. szakasz; 2ae45dae lektori lista | forras=manual | ts=2026-11-15)*

### F224.2 — A bíráló szerepfájlja
Új `.claude/agents/biralo.md` (`model: sonnet`). Bemenet: az érvvázlat vitatott pontjai, a bizonyítéklap, a blokkok vizsgálandó állításként, a lap Kivonat-/Remez-/Sod-/Módszertan-mondatai. Hét kérdés súllyal (egyensúly, valódi erő a 12:3-as példával, hiányzó érv a „-ért” példájával, szintkeverés, a lap két helyének ellentmondása, szakirodalmi hatókör, szerkezet jelölése); legfeljebb 10 lekérdezés vitatott pontonként, naplózva; „lekérdezendő”; határról nem ítél; elutasított tételek a lektorhoz és a felhasználóhoz.
*(proveniencia: scope=TERV_CIKKIRAS_v3 4. szakasz; BIRALO_821_sonnet.md (a mérés) | forras=manual | ts=2026-11-15)*

### F224.3 — A lektor szűkítése
`.claude/agents/lektor.md`: a bemenet egy eredetjelölés nélküli tétellista; ötödik kérdés: „a próza az érvnapló szerint íródott-e”; a négy érvelési kérdés a bírálóé (az 1. változat 32/c pontja a repóba sosem került be, ezért itt „nem a te kérdésed” mondat áll); minden ellenőrzendő tételre sor („rendben” is), hogy a hívó a vak mintát mérhesse. `model: fable` változatlan. `.claude/commands/kiadas.md` 3. lépés: a lektor bemenete (jelölt helyek, az F2 „vitatott”/„nem eldönthető” tételei, a bíráló elutasított tételei, vak minta az F2 „igazolt” tételeiből 10%, legalább 5), a felfüggesztés hibás mintánál, a három hatókör-szűkítés (a)/(b) mondata, hivatkozással a `BRIEF_SABLON.md` DT-F221a szabályára.

### F224.4 — A kinyerés bővítése
`eszkozok/proza_allitas.py`: három új K-fajta a rés mondatain (`UJ_FAJTAK`): **szám-kapcsolat** (a kapcsolat-tábla sorai bizonyosság szerint; „N helyből M”: a bekezdés felsorolt igehelyei), **belső utalás** (a célpont a forrás vagy a generált lap címsorai, félkövér bekezdés-címei között), **nem dönti el** (a pont igehelyei a bekezdésből, a pont címéből is; a lap más mondatai ugyanezekre a helyekre, legfeljebb 8). Gépi ELTÉR-ítélet az új fajtából soha nem lesz: ahol a gép dönt, a bizonyíték `JELENTÉS (ELTÉR-jellegű, F224.4)` kezdetű, ⚑-gel, és a `--kapu` motívumonként külön `JELENTÉS` sort ír. A régi K-tételek számozása nem változik (a régi fajták egységei kapják előbb a számot). A HIBA-szintre emelés javaslata: N-F224a (`nyitott/uj/f224-cikkiras-uj-menet.md`).

**Mérés** (a K-tétel-szám a futtatás előtt és után; `naplok/F224_proba/klista.py`, a forrás, az `elofordulasok.tsv`, a `kapcsolatok.tsv` és a lap a megnevezett commitról):

| Forrás | K előtte | K utána | Új K-tétel |
|---|---|---|---|
| ISTENTISZT-001, `b2aea73f` | 54 | 58 | K55 (89. sor, Remez: „három kapcsolat erős” — **a lektor 4. tétele**; ELTÉR-jellegű: 3 ↔ 13 magas sor), K56 (99., 2Móz 33:19/34:5 „nem dönti el”), K57 (101., 1Móz 4:26 „nem dönti el” — **a lektor 9. tétele**), K58 (103., Róm 10:13 „nem dönti el”) |
| HAMART-001, `f6da955e` | 114 | 118 | K115 (15., Kivonat), K116 (101.), K117 (105.), K118 (152., Módszertan) |
| ISTENTISZT-001, main | 62 | 64 | 2 |
| HAMART-001, main | 123 | 128 | 5 |

- A régi K-tételek: a számuk és a helyük mind a négy forráson változatlan; új bizonyítéksort (és ezzel ⚑-et) kapott: ISTENTISZT `b2aea73f` K25 („hét helyéből ötben” — a lektor 10. tétele; a bekezdés öt felsorolt igehelye) és K42 (Módszertan, „22 helyből 20”); HAMART `f6da955e` K54; a main forrásain ISTENTISZT K26, K48, K50, K52, HAMART K47, K60.
- A lektor 11. tétele („jelentés a névből”) értelmezés, nem lett K-tétel (a brief szerint nem elvárt).
- A `--kapu` kimenete a main forrásain bájtra azonos a változtatás előttivel (`diff` üres; ELTÉR 0, egyezik és kézi-számláló változatlan, a kézi-számláló csak a régi fajtákat számolja), kilépőkód 0.
- A 113 helyett 114 K-tétel a `f6da955e`-n: a mérés (2026-11-15) óta az eszköz változott; a régi K-számok a mai eszközzel és a mai eszköz után egyeznek, a 113-as szám a mérés napjáé.
- Teszt: `eszkozok/teszt_proza_allitas.py` 51 teszt OK (11 új, `F224_4` osztály: mindhárom fajtára pozitív és negatív eset, a stabil számozás és a kapu JELENTÉS-sora).
*(proveniencia: scope=motivumok/ISTENTISZT-001.md @b2aea73f, motivumok/HAMART-001.md @f6da955e, a main két forrása | forras=eszkozok/proza_allitas.py (az ág feje) | ts=2026-11-15)*

### F224.5 — A bizonyítéklap
Új `eszkozok/bizonyiteklap.py` (+ `eszkozok/teszt_bizonyiteklap.py`, 11 teszt OK). Bemenet: a kulcsversek (`--versek` vagy a motívum sorai) és a lánc szavai (`--lanc` vagy a motívum `strong` mezői). Kimenet: gyakorisági alapvonal (versszám és arány a teljes ÓSZ/ÚSZ táblán); versenként a vers állapota a motívum adatában (eldöntött / jelölt döntéssel / nem áll az adatban — csak az eldöntött vehető át), a Károli-szöveg, a lánc szavai pozícióval, az együttállások (megfigyelt együttes versszám és a véletlen-alapvonal szerint várt `n_A · n_B / N`), a fordított sorrendű ismétlés csak versen belül, a vers lánc-szavainak összes sorrendjéből számolt alapvonallal; ítélet-, erősség- vagy keret-mező nincs; minden vers proveniencia-sorral; a tanulmány csak hivatkozás (`--tanulmany`).
**A mérés bizonyítéklapjával összevetve** (HAMART 1Móz 3:14–12:3, a lánc hat szava + H7043): az alapvonal betűre azonos (H0779 52, H0127 211, H6093 3, H2403 271, H2555 59, H7843 135 vers); minden versben ugyanazok a lánc-szavak; az árar + adámá együttállása 5 vers (a Sonnet-bíráló mérése is 5). Többlet: a 12:3-ban a H7043 (qalal) is áll — a mérés bizonyítéklapjáról ez kimaradt, és a bíráló ezt külön kifogásolta (`BIRALO_821_sonnet.md` K1).
**A SEMA-szakasz** (a kimenet formája) a #729 merge-e után, a merge-kori következő szabad számmal készül (a brief `fugg` indoka); addig a forma egyetlen leírása a modul docstringje. A CI-be vétel: N-F224b (a workflow az F217-é).
*(proveniencia: scope=HAMART-001, 11 vers (1Móz 3:14–12:3), lánc H0779, H0127, H6093, H2403, H2555, H7843, H7043 | forras=python eszkozok/bizonyiteklap.py; konkordancia/TAHOT_kivonat.tsv | ts=2026-11-15)*

### F224.7 — A tanulmány blokkjai
`sablonok/2_PaRDeS_bovitett_sablon.md` 4/b. pont (v24), a meglévő hat blokk újraírása nélkül: (1) **a szakaszhatár előbb**, független (motívumtól nem függő) indokkal, egy mondatban a blokkok előtt; (2) a vita-blokkban **név csak forrással**; (3) a **pótolt blokk** a fejlécben `pótolt: nem vak olvasás` jelölést kap (az F205 „meglévő tanulmány utólag nem kap blokkot” mondata kivétellel bővült: csak ha a motívum menete kimondja, pl. a TEREMT-001); (4) a funkció-blokk a **szakaszbeli szerepet** adja, a láncbeli a cikké (DT-F224a). A minta (HAMART 1Móz 8:21) funkció-sora az F224 előtti, láncbeli alakban maradt, ezt a minta címe kimondja: új funkciómondatot ide nem írtam (értelmező próza, a próza gazdájáé).
**A kinyerő:** az `eszkozok/tanulmany_kinyer.py` a main-en **még nem létezik** (az F205 M3/M5 lépése, `fut`, a `kovetkezo` szerint az F212 merge-e után, main-behozással). A `pótolt` mező ezért most nem olvasható gépileg, és nem is kell: az F205 a kinyerőt ezen az állapoton építi (a brief `fugg`-indoka szerint az F224 utáni állapotra épül); a mező opcionális, a fejléc régi alakja érvényes marad. Az F205 ágainak nincs függő változása a két közös fájlon (`git diff origin/main...origin/claude/f205-*`: üres), nyitott PR-ja nincs.

### F224.8 — A menet
`MUNKAMENET.md` C) szakasz: a tábla előtt egy mondatban a lépéssor (A → … → 1. kiadás), mindegyik lépés a sor azonosítójával; négy új sor (C-ia, C-bl, C-ev, C-bi), mindegyik a szabályhelyre mutat, a szabály szövege nélkül; új C-sz sor a mérőtábla küszöbeivel (a brief F224.11: „a küszöbök a `MUNKAMENET.md` C) szakaszában”); a C-a sor átírva (F1 a próza gazdája, F2 az `allitas-ellenor`; a „kézi listát olcsó modell vagy ember nézi” kikerült; a „hamis” a gazdához, a „vitatott” és „nem eldönthető” a lektorhoz); a C-h sorban a `hatar-ellenor` modellje Sonnet.
**Jelzés a felhasználónak:** a C-h sor indoka („kreditből fizetendő, a havi csomagba nem fér; DT546”) a Fable-hez tartozott; a Sonnettel ez nem áll. A ⛔ (a felhasználó indítja, minden futás előtt az ő jóváhagyásával) változatlan maradt, mert a megszüntetése a brief hatókörén kívüli döntés.
A C-bl és a C-sz a SEMA-szakaszra még szám nélkül hivatkozik (a #729 merge-éig); a C-ev a 9_ sablon még meg nem írt érvnapló-szakaszára (F224.6).

### F224.9 — A ⚑-szabály ellentmondása
`sablonok/10_PaRDeS_U3_proza_prompt_sablon.md` (v1.3), „⚑ tétel a kézi listán”: a „Mindet magad nézed át” kikerült; a ⚑ csak sorrend, minden K-tételt az állítás-ellenőr ítél (hivatkozás: `.claude/agents/allitas-ellenor.md`, `MUNKAMENET.md` C-a); az író a „hamis” ítéletet javítja. A „többi kézi tétel … olcsó modell (Sonnet) vagy ember” mondat is az F2-re mutat. A jelzés-fajták listája az F224.4 három új fajtájával bővült. `grep "magad\|olcsó modell"` a 10_ sablonban: 0 találat.
**A hatókör-szűkítés 3. pontja** (a brief 3. pontja, `BRIEF_SABLON.md` DT-F221a): *a ⚑ tételeket nem az író nézi át, hanem az F2.* (a) Ellenőrzés nélkül marad: semmi új — az író átnézése önellenőrzés volt. (b) Méri helyette: az F2 minden K-tételt állításonként ítél; a „vitatott” és „nem eldönthető” a lektorhoz megy. A mondat a `.claude/commands/kiadas.md` 3. lépésében hivatkozással áll.

### F224.10 — A funkció két mezője (döntés)
`dontesek/uj/f224-cikkiras-uj-menet.md`: DT-F224a 🟢, a jóváhagyás idézetével. A megfogalmazás a terv 5. szakaszán belül marad: új sémamező, adatoszlop vagy lapgenerátort érintő változás nincs (ezért nem 🟡). A DT803 többi része változatlan. Az alkalmazás helye: a 2_ sablon 4/b. pontja (F224.7, kész) és a 9_ sablon érvnaplója (F224.6, a #729 után).

### F224.12 — A határ-ellenőr modellje
`.claude/agents/hatar-ellenor.md`: `model: sonnet`, a 0. lépés modellneve `sonnet`; a bemenet a határesetek negatív próbáival bővült, a negatív kritérium szűkebb és tágabb változatával. `grep -i fable .claude/agents/hatar-ellenor.md`: 0 találat. A `MUNKAMENET.md` C-h sorának modellneve az F224.8-ban.

### F224.13 — Elfogadási próba (⛔)
A részletek, a nyers kimenetek, a bemenetek és a költség: `naplok/F224_proba.md`, `naplok/F224_proba/`. Keret-ellenőrzés a próba előtt (`get_usage`): 5 órás 37%, heti 20% → a becslés belefért; a 2. kör előtt 54% / 22%.

| Halmaz | Küszöb | 1. kör | 2. kör (a javítókör után) |
|---|---|---|---|
| HAMART 18 (F2) | ≥ 80% | 56% | 61% |
| ISTENTISZT 10 (F2) | ≥ 80% | 20% | 30% |
| ISTENTISZT 6 (bíráló) | ≥ 4/6 | 5/6 | — (teljesült) |
| HAMART 8:21 (bíráló) | 5/5 | 5/5 | — (teljesült) |
| hamis riasztás (vak minta) | ≤ 30% | 50% | 50% |

**⛔ A javítókör után is három küszöb alatt:** megállás, a felhasználó dönt (küszöb, szerep, modell). A javaslat (`naplok/F224_proba.md` 6. szakasz): (A) a lektor hatókör-szűkítésének 1. pontja most nem lép életbe; (B) a következő mérés előtt N-F224c, kisebb szeletek, két futás uniója; (C) egy Opus-futás a modell és a szerep szétválasztására. A TEREMT-001 a teljes menettel addig nem indul.
**Eltérés a tervtől:** az új szerepfájlok a sessionben nem voltak regisztrált ügynöktípusok; az ügynök `general-purpose`, `model: sonnet`, a szerepfájl törzsével. A 2. körben az ügynökök a kimenetet maguk írták fájlba (a hívó kontextusa miatt).

### F224.14 — N-F224c: a kinyerés két hézaga (`eszkozok/proza_allitas.py`)

*A felhasználó döntése (2026-11-15, az orkesztrátoron át): „Igen, így menjen” — a 7.6 pontra tett javaslat 2. pontja.*

Két új K-fajta, csak kézi tétel (gépi ELTÉR soha; az E41 nem változik):
- **idézeten túl:** ha a mondat Károli-idézete gépileg egyezik, de a mondat az idézeten és az igehelyen kívül legalább három tartalmi szót mond, K-tétel lesz (eddig kézi tétel nélkül maradt). A puszta idézet („A vers így szól: „…””) továbbra sem tétel.
- **szabály-mondat:** a rés igehely nélküli határszabálya („Ide az a hely tartozik, …”, „… nem tartozik ide”) K-tétel; a gépi sor a gerinc-szavak sorrendjét adja a motívum minden helyén (TAHOT/TAGNT), a többségtől eltérő helyek név szerint.
- **A K-számozás három szintje:** a régi fajták, az F224.4 fajtái, az F224.14 fajtái — egyik korábbi K-szám sem mozdul (a próba ISTENTISZT-bemenetén K1–K58 hely, forrás és szöveg szerint azonos).

**Mérés (az F224.13 ISTENTISZT-bemenetén, `b2aea73f`):** 58 → 75 K-tétel (17 idézeten túl: 5 rés-mondat, 12 adatsor-próza; 1 szabály-mondat). A Remez-mondat („ugyanaz a formula áll Illés és a Baál prófétáinak szájában …”) K61, a Kivonat szabály-mondata K60: a gépi sor szerint a gerinc-szavak sorrendje 13 helyen H7121 → H8034, a Zsolt 116:4, 13, 17-ben fordított. Az E41 (`--kapu`) kimenete a main forrásain bájtra azonos a változás előttivel. *Proveniencia: `scope=python naplok/F224_proba/klista2.py ISTENTISZT-001 (a b2aea73f-es forrás, elofordulasok, kapcsolatok, jeloltek, lap) és python eszkozok/proza_allitas.py --kapu | forras=eszkozok/proza_allitas.py | ts=2026-11-15`.*

### F224.15 — a mondaton kívüli adat a K-tétel alatt (`eszkozok/proza_allitas.py`)

*Ugyanaz a döntés, 3. pont: „a kinyerés az F2 elé a mondaton kívüli, az állítást hordozó adatot is adja … a 7. szakasz ISTENTISZT-hibáiból általánosítva, nem tételenként kézzel”.*

A kézi lista minden K-tétele alatt „Mondaton kívüli adat” (ítélet nélkül): (1) a hely funkció-mezője (a lapon a hely mellett álló állítás); (2) szótári hivatkozásnál a szótár versei (`adat/bdb_vers_jelentes.tsv`, `adat/thayer_vers_jelentes.tsv`, az előfordulás-sor szótár + Strong + jelentéskód szerint) a motívum helyeire, az elutasított és a nyitott jelöltekre (`adat/jeloltek.tsv`) és a többire bontva; (3) a gerinc-szavak környezete az angol tükörfordításban (TAHOT/TAGNT, ±5 szó: ki beszél, ki cselekszik, kinek a neve); (4) a lap más mondatai ugyanarról a forrásról (Targum, LXX, Vulgata, BDB, Thayer, szövegkiadás; legfeljebb 3, a közös versűek elöl); (5) Targum-hivatkozásnál a Targum sora (a Tóra versein). Az általánosítás a 7.2 szakasz négy mechanizmusából: a hibás állítás a funkció-mezőben áll (IST 1), a szótár a kizárt helyet is ide sorolja (IST 12), a vers alanya (IST 8, 17), a lap más mondata ugyanarról a forrásról (IST 10). A lista mérete a próba ISTENTISZT-bemenetén 107 → 192 KB. Tesztek: `eszkozok/teszt_proza_allitas.py` `F224_14`, `F224_15` (10 új teszt, összesen 61, OK).

### F224.16 — az F2 Opusra (DT-F224b, DT-F224c), N-F224d, N-F224e

- `.claude/agents/allitas-ellenor.md`: `model: opus`, a 0. lépés `opus`; a bemenet új bekezdése: a „Mondaton kívüli adat” a K-tétel része (a funkció-mező a hét kérdéssel ítélendő; a tükörfordítás a *Ki?*, a szótári besorolás és a lap más mondata a 7. kérdés adata), és a két új K-fajta. A példák mechanizmust írnak le, nem a próbahalmaz tételeit (egy, a 10. tétel válaszát hordozó példát a végrehajtó a commit előtt kivett).
- **DT-F224b 🟢:** az F2 modellje Opus (a felhasználó döntése).
- **DT-F224c (javaslatként 🟡, a felhasználó 2026-11-15-i „Igen, elfogadom” döntésével 🟢):** a szerepfájl eddigi 0. lépése szerint az F2 nem fut, ha a próza modellje azonos; a próza Opusszal készül, így a DT-F224b e záradékkal nem lépne életbe. Javaslat: a függetlenséget a friss kontextus és a vak bemenet adja, a modell-függetlenséget a lektor (Fable); a szerepfájl e szerint áll. A felhasználó megerősítésére vár.
- **N-F224d:** a hamis riasztás csökkentése (a felhasználó döntése szerint nem e kör része). **N-F224e:** a `MUNKAMENET.md` C-a „(Sonnet)” szava a #725 merge-e után (a #725 a fájlt írja).

### F224.17 — újramérés az ISTENTISZT-szeleten (Opus, új kinyerés)

Egy F2-ügynök (Opus) a 75 tételes új listán, vakon, javítókör nélkül; a HAMART nem futott újra. Eredmény: **7/10 = 70%** (részlegessel 8/10; Opus a régi kinyeréssel 30%), „nem eldönthető” 2,7%; a lektori listán kívüli többlet-jelzés 3 (2 valódi, 1 nem dönthető el); új mellékhatás: az 1Kir 18:25 funkció-mezőjének hibája hat K-tétel alatt is „hamis” ítéletet ad (N-F224f). **A mérés nem független:** a javítás ugyanennek a tíz tételnek a mechanizmusaiból készült. Költség: 342 780 token (Opus); heti keret 29% → 29%. Részletek: `naplok/F224_proba.md` 8. szakasz; nyers kimenet: `naplok/F224_proba/F2_ISTENTISZT_opus2.md`.

### F224.18 — N-F224f (a funkció-mező csak a saját tételnél) és DT-F224d (küszöb, független mérés)

*A felhasználó döntése (2026-11-15, az orkesztrátoron át): „igen” — a két javaslatra.*

- **N-F224f:** `eszkozok/proza_allitas.py` `kontextus()`: a funkció-mező csak az `adat:kapcsolodas` egységnél, a hely saját versére; teszt (62 OK); a szerepfájl Funkció-mező pontja. Célzott ellenőrzés (új teljes mérés nélkül): az 1Kir 18:25 funkció-mezője hat K-tétel helyett csak a K50 alatt áll; a K-halmaz azonos (75). `naplok/F224_proba.md` 8.5.
- **DT-F224d 🟢:** a küszöb marad 80%; a független mérés a következő új motívum cikkírásakor fut.

### F224.6, F224.5 (SEMA), F224.11 — a #729 és a #725 merge-e után (2026-11-16)

*Az orkesztrátor jelzése (2026-11-16): a #729 és a #725 a main-en (`6932be23`); a main behozva (`e99282a6`, ütközés nélkül). Az ütközés-ellenőrzés: nyitott PR nem írja e fájlokat.*

- **F224.6 — az érvnapló** (`sablonok/9_PaRDeS_motivum_forras_sablon.md` v2.5, 4. pont, „Az érvnapló”): pontonként egy blokk, állításonként egy sor — állítás · érvtípus (szövegtanú / hiány / recepció) · bizonyíték vagy „lekérdezendő” · döntés (eldöntve / nyitva / kimarad); „lekérdezendő” nem kerül a prózába; a vita egy helyen: a Vitatott pontok az érvnapló „nyitva” pontjainak olvasói nézete, a lap többi mondata nem dönt másként; a láncbeli szerep az érvnapló döntése szerint (DT-F224a); a bírálatra adott válasz helye (elfogadva / elutasítva). A 10_ sablon (v1.4) bemenete és a `MUNKAMENET.md` C-ev sora csak hivatkozik. **Végrehajtói értelmezés (kimondva):** az érvnapló külön belső fájl (`naplok/ERVNAPLO_<ID>.md`), nem a `motivumok/<ID>.md` új szakasza — a forrás új `##` szakaszát a lapgenerátornak kezelnie kellene, és a generátor e brief hatókörén kívül esik (3. pont); a terv „érvnapló-szakasz” szava a 9_ sablon szakaszára (a szabály helyére) vonatkozik. A korábbi C-ev szöveg („a motívumforrás érvnaplója”) ennek megfelelően javítva.
- **F224.5 — SEMA 2.71** (`adat/SEMA.md`): a `naplok/BIZONYITEK_<ID>.md` formája (gyakorisági alapvonal, versenkénti blokk az állapottal, együttállás, versen belüli fordított ismétlés; tiltott mezők); a `bizonyiteklap.py` docstringje és a `MUNKAMENET.md` C-bl sora a számra hivatkozik.
- **F224.11 — SEMA 2.72 és a két mérőtábla:** a `naplok/SZIVARGAS_<ID>.tsv` oszlopai (`id`, `hely`, `allitas`, `mechanizmus`, `hol`, `sulyos`, `generalt`, `meres`, `forras`). A `mechanizmus` a hibanapló kódja; mivel a hibanapló (`naplok/HIBA_MECHANIZMUSOK.md`) a felhasználó találta hibák mechanizmusait gyűjti, a versállítás-hibáknál az állítás-ellenőr kérdése (`K-KI` … `K-MASIK`), a kinyerés hézaga (`KINYERES`) és az érvelési hiba (`ERVELES`) is érvényes érték. Kitöltve a próbából (`naplok/F224_proba/szivargas_kitolt.py`): **HAMART-001** 34 sor (a lektor pontossági tételei): F1 5, F2 15, F3 14 (ebből 8 generált blokk, a próba nem mérte); **ISTENTISZT-001** 18 sor (a 2. kiadás lektorának 1–18. tétele): F1 1, F2 7, D 5, F3 5. A `hol` a menet mai felállása szerinti próbán megfogó lépés (F2 = Opus; az ISTENTISZT-en az új kinyeréssel, ami nem független mérés).
- **N-F224e** megoldva: a `MUNKAMENET.md` C-a sora Opus (DT-F224b, DT-F224c). **N-F224b** nyitva: a `.github/workflows/ellenorzes.yml` és a `eszkozok/push_elott.py` nincs az `ir` mezőben.

## Független ellenőrzés — 1. ellenőrzés

*`fuggetlen-ellenor`, `claude-fable-5-2` (a szerepfájl `model: fable`), 2026-11-16; tartomány `6932be23..bcbb14b9`, szint: teljes; a jelentés változtatás nélkül. Egy előző indítás az ügynöktípus session-indításkori (Opus) definíciójával futott, és a 0. lépésnél szabályosan megállt („A kért modell `fable`, a session `claude-opus-5-5`”): nem számít ellenőrzésnek.*

ELTÉRÉS: 7 tétel

Brief: `F224_CIKKIRAS_UJ_MENET_BRIEF.md` · tartomány: `6932be2381db77501731a6248dbe455a0c3bf7b0..bcbb14b95b74e4c2b0ef616d8ac9d843c198633a` · szint: teljes · 1. független ellenőrzés

A briefben nincs „G”/„D” jelű pont, ezért a 13 tétel „Kész” feltételeit, az elfogadási feltételeket és a ⛔ pontokat vettem sorra. A `python eszkozok/teszt_futtat.py --diff 6932be23…` futás a jelentés írásakor még nem ért véget, eredménye nincs.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0. modell | OK | `.claude/agents/fuggetlen-ellenor.md:5` | Tényleges modell: `claude-fable-5-2`; a frontmatter `model: fable` a head-en és az `origin/main`-en is (`git diff --numstat base..head -- .claude/agents`: a fájl nem változott). |
| 0. modell, mellékes | ELTÉRÉS | `.claude/agents/fuggetlen-ellenor.md:40` | A törzs 0. pontja `opus`-t ír, a frontmatter `fable`-t (main: `68472a49 F218.z1`). Nem az F224 diffje okozta; a brief 2. pontja is „független ellenőr: Opus”-t ír. |
| 0. `modell` mezők | OK | `naplok/F224_proba/*.md`, `naplok/SZIVARGAS_*.tsv` | `Grep forras=modell:`: a Sonnet-futások `claude-sonnet-5-5`, az Opus-futások `claude-opus-5-5`; a mérőtáblák `forras` mezője ezzel egyezik. `git log --format=%(trailers…)`: mind a 26 commit `Claude Opus 5.5`. |
| F224.1 állítás-ellenőr | NEM ELLENŐRIZHETŐ | `.claude/agents/allitas-ellenor.md:5` | A hét kérdés, az ítélet, a bizonyítéktípus, a kétirányú tilalom és a kimenet megvan. A „Kész” `model: sonnet`-et kér, a fájl `opus` (DT-F224b). A döntés „a felhasználó … az orkesztrátoron át” idézettel áll, ezt a repóból nem tudom igazolni. A brief 2. pontja és `ad` mezője még Sonnetet ír. |
| F224.2 bíráló | OK | `.claude/agents/biralo.md` | `model: sonnet`; hét kérdés súllyal, 10 lekérdezés vitatott pontonként, „lekérdezendő”, határról nem ítél; hívás: `MUNKAMENET.md` C-bi. |
| F224.3 lektor | OK | `.claude/agents/lektor.md`, `.claude/commands/kiadas.md:15-21` | `model: fable` változatlan; ötödik kérdés, vak minta (10%, legalább 5), felfüggesztés, a három (a)/(b) mondat hivatkozással. Az 5. kérdés tartalmi hibája az F224.6 sorban. |
| F224.4 kinyerés | OK | `eszkozok/proza_allitas.py` | `python eszkozok/teszt_proza_allitas.py` → `Ran 62 tests … OK`. A b2aea73f-es listán a K55–K58 megvan (`naplok/F224_proba/bemenet/ist/ist_lista.md:129-150`). A `--kapu` „kézi sor” számlálója kizárja az új fajtákat. |
| F224.4 `--kapu` bájtazonosság | NEM ELLENŐRIZHETŐ | — | A `proza_allitas.py --kapu` nincs a megengedett parancsaim között. A CI E41 zöld, de a „bájtra azonos a main-nel” állítást nem futtattam. |
| F224.5 bizonyítéklap, teszt és alapvonal | OK | `eszkozok/teszt_bizonyiteklap.py` | `python eszkozok/teszt_bizonyiteklap.py` → `Ran 11 tests … OK`. `lekerdez.py scan H0779` → `n=52`; `lekerdez.py kollokacio H0779 H0127` → `n=5`; mindkettő egyezik a `bemenet/d821/bizonyitek_821.md` 13. és 49. sorával. |
| F224.5 a vers állapota | ELTÉRÉS | `eszkozok/bizonyiteklap.py:174` | A `vers_allapot` az `igehely` mezőt szó szerint veti össze az egyes verssel, miközben a `keszit` a tartományt versekre bontja. Az `adat/elofordulasok.tsv` 13 sora tartomány (HAMART-001: 6, pl. `1Móz 4:10-11`, `Sof 1:2-3`). Ezek versei `--motivum` futásnál „nem áll a motívum adatában (nem vehető át)” állapotot kapnának, pedig eldöntöttek. Kódolvasásból; az eszközt nem futtathattam, a tesztben nincs tartomány. |
| F224.5 SEMA 2.71 | OK | `adat/SEMA.md:2607` | A forma, a tiltott mezők és a proveniencia leírva; a szám a 2.70 után következő szabad szám. |
| F224.6 érvnapló | ELTÉRÉS | `.claude/agents/lektor.md:20`, `sablonok/9_PaRDeS_motivum_forras_sablon.md:191` | A 9_ sablon szerint az érvnapló `naplok/ERVNAPLO_<ID>.md`, „nem a forrás szakasza”. A lektor 5. kérdése szerint „az érvnapló a forrásban áll; ha nincs, jelzed”, és a lektor bemenete csak a próza és az adat, így a kérdés mindig „nincs”-et adna. Ugyanez a szóhasználat: `biralo.md:9`, `sablonok/2_…:233`, DT-F224a („a motívumforrás érvnaplója”). |
| F224.6 az érvnapló helye mint döntés | ELTÉRÉS | `naplok/F224_jelentes.md:122` | Az érvnapló helyét a végrehajtó „végrehajtói értelmezésként” döntötte el, a 🟢 DT-F224a szövegétől eltérően. Erre nincs DT-F sor (CLAUDE.md: tartalmi döntésnél tétel, majd megállás). |
| F224.7 tanulmányblokk | ELTÉRÉS | `eszkozok/tanulmany_kinyer.py:174`, `sablonok/2_PaRDeS_bovitett_sablon.md:210` | A kinyerő a base-en már megvan (`aa06c044`), és pontosan három fejlécmezőt fogad el. A v24 `… \| pótolt: nem vak olvasás` fejlécét „hibás IGEHELY-BLOKK fejléc”-ként elutasítaná. A jelentés indoka („a main-en még nem létezik”) a head-en már nem igaz. A hivatkozott `adat/SEMA.md` 3.10.5 nem említi a „pótolt” mezőt. A kinyerő nincs az `ir` mezőben, és N-tétel sincs róla. |
| F224.8 menet | ELTÉRÉS | `MUNKAMENET.md:70` és a C-a, C-g, C-h sorok | Az új sorrend-mondat szerint F1 (benne C-g, C-o) → F2, a C-a sor szerint viszont az állítás-ellenőrzés „a gépi kapuk (C-g) előtt” fut. A mondat szerint a határ a próza előtt áll, a C-g sor szerint „a C-h csak zöld gépi kapuk után indul”. Az öt új sor és a hivatkozások megvannak; az E27 a CI-ben zöld. |
| F224.9 ⚑-szabály | OK | `sablonok/10_PaRDeS_U3_proza_prompt_sablon.md:93` | `Grep "magad nézed\|olcsó modell"` a sablonokon, a `MUNKAMENET.md`-n és a `.claude/` alatt: 0 találat. |
| F224.10 DT-F224a | NEM ELLENŐRIZHETŐ | `dontesek/uj/f224-cikkiras-uj-menet.md:1` | 🟢, idézettel, helyőrzővel; sémamező vagy generátor-változás nincs. A jóváhagyás közvetített idézet. |
| F224.11 mérőtábla | OK | `adat/SEMA.md:2642`, `naplok/SZIVARGAS_*.tsv` | Kézi számolás a diffből. HAMART 34 sor: F1 5, F2 15, F3 14, generált 8. ISTENTISZT 18 sor: F1 1, F2 7, D 5, F3 5. Egyezik a jelentéssel és a próba 7.1, 8.1, 2.3 tábláival. |
| F224.12 határ-ellenőr | OK | `.claude/agents/hatar-ellenor.md:5` | `model: sonnet`; `Grep -i fable` a fájlban: 0; a határ-ellenőrre mint Fable-re máshol sincs hivatkozás. |
| F224.13 HAMART-nevező | ELTÉRÉS | `naplok/F224_proba.md:171`, `naplok/F224_proba/F2_HAMART_1_opus.md:38` | A „15/18 = 83% ✓” nem számolja a lektor 40. tételét. Ez a használt listán K66 (`bemenet/ham/ham_lista.md:473`), az Opus „igazolt”-nak ítélte, a mérőtábla S031 sora F3. Vele együtt 15/19 = 78,9%, a küszöb alatt. A brief a halmazt 18-ban rögzítette, a napló 2.1 szakasza megemlíti a tételt. |
| F224.13 küszöbök, ⛔ | NEM ELLENŐRIZHETŐ | `naplok/F224_proba.md` 6–8. szakasz | A megállás megtörtént (`c16f4d3d`). Záró állapot: bíráló 5/6 és 5/5 ✓; ISTENTISZT 70% (nem független) ✗; hamis riasztás 45–50% ✗ (N-F224d). A folytatást adó döntések (C-futás, F224.14–.18, DT-F224b–d) mind közvetített idézetek. A `kiadas.md` szűkítése („a lektor nem olvassa újra az igazolt tételeket”) él, miközben két F2-küszöb nem teljesül. |
| A1 | OK | `.claude/agents/allitas-ellenor.md`, `biralo.md` | `scan H0779 --szakasz "1Móz 9:25"` → n=1; `kollokacio H7043 H0779` → 1Móz 12:3; `kollokacio H5668 H0127` → 1Móz 3:17, 8:21; `karoli "1Kir 18:25"` → „monda Illés a Baál prófétáinak”; `scan H0776/H0127 --szakasz "Jer 51:46"` → 1 / 0. A Zsolt 116 szórendje a lekérdezővel nem dönthető el; a `kollokacio H7121 H8034` csak az együttállást adja. |
| A2 | ELTÉRÉS | `nyitott/uj/f224-cikkiras-uj-menet.md:3,5,6` | Hat tételből három (N-F224c, e, f) „az ágon megoldva”, mégis nyitott felsorolási tételként áll, így a `szamkiosztas` nyitottként olvasztaná be. Az N-F224e megoldását a diff igazolja (C-a sor: „Opus, DT-F224b”). N-F224b valóban nyitott: a `teszt_bizonyiteklap` nincs a workflow-ban és a `push_elott.py`-ban. |
| A3–A6 | OK | — | A diffben nincs motívumadat, lexikonlap, tanulmány vagy nevesített tanító; a Remez/Sod és az E12–E15 nem érintett. A sablonok új szabályai („keret, khiazmus mindig értelmezés”, „név csak forrással”) az A3 és A5 irányába szigorítanak. |
| 3. CI | OK | — | `gh run view 43840364110 --json headSha,conclusion,jobs` → `headSha=bcbb14b9…`, `success`, `ellenorzes` és `feladatkovetes` zöld. A `futtat.py`-t nem futtattam újra. |
| Tesztek (Diéta 3.) | NEM ELLENŐRIZHETŐ | — | A két érintett tesztfájl zöld (fent). A `teszt_futtat.py --diff` még fut; az `adat/SEMA.md` miatt a lassú `teszt_szintek.py` is érintett (`LASSU_LEFEDETT`: `adat/`), és azt a CI nem futtatja. |
| L1 törölt sorok | OK | — | `git diff --name-status --diff-filter=DR base..head`: üres. 56 fájl, 7752 beszúrás, 35 törlés; a törlések szerep-, sablon- és munkamenet-sorok cseréi. |
| L2 kulcstartomány | OK | — | A SEMA 2.71, 2.72 a 2.70 után folytonos. A mérőtáblák `id`-je S001–S034 és S001–S018, hézag nélkül. |
| L3 „nulla-diff” hatóköre | OK | — | `git diff --numstat base..head -- lexikon nyilt_mag 'generalt*' motivumok motivumlog .github eszkozok/push_elott.py eszkozok/ellenorzes DONTESEK.md NYITOTT_FELADATOK.md FELADATOK.md CLAUDE.md`: üres. A nulla-diff nem vonatkozik a `proza_allitas.py` kimenetére: a kézi lista új K-tételeket és „Mondaton kívüli adat” sorokat kap. |
| L4 adattáblák | OK | — | `git diff --numstat base..head -- adat konkordancia`: csak `adat/SEMA.md` (+62). Minden `.tsv` Δ = 0. Új tábla a `naplok/` alatt: `SZIVARGAS_HAMART-001.tsv` 34 sor, `SZIVARGAS_ISTENTISZT-001.tsv` 18 sor; a bontás a fájlok fejlécében és az F224.11 sorban. |
| L5 ⛔ pontok | OK | — | Generátor, 6_ sablon, E41 szintje és hatóköre, workflow: érintetlen. Az `ir` mezőn kívül csak a brief fejléce és a `dontesek/uj/`, `nyitott/uj/` fájl változott. Végleges DT/N szám nincs az ágon. A keret-ellenőrzés csak a naplóban áll. |

Az ELTÉRÉS-ek súlyossági sorrendben:

1. **F224.7:** a meglévő `tanulmany_kinyer.py` elutasítja a sablon új, „pótolt” fejlécét. Az első pótolt blokknál (TEREMT-001) a kinyerés hibával áll meg, és a teendőnek nincs gazdája.
2. **F224.6:** az érvnapló helyéről a szabályhelyek ellentmondanak egymásnak, ezért a lektor új, 5. kérdése a mai szöveggel nem működik. A hely eldöntése DT-sor nélkül történt.
3. **F224.5:** a bizonyítéklap a tartományos előfordulás-sorok verseit „nem vehető át” állapottal jelölné (kódolvasásból, futtatás nélkül).
4. **F224.13:** a HAMART 83%-a a 40. tétel (K66) kihagyásán múlik; vele 78,9%. A hatókör-szűkítés úgy él, hogy két F2-küszöb nem teljesül; ez a felhasználó döntése.
5. **F224.8:** a `MUNKAMENET.md` új sorrend-mondata ellentmond a változatlan C-a, C-g, C-h soroknak.
6. **A2:** három megoldott tétel nyitottként áll a `nyitott/uj/` fájlban.
7. **0. pont, mellékes:** a `fuggetlen-ellenor.md` törzse `opus`-t ír, a frontmatter `fable`-t.

**Kiegészítés (az ellenőr utólagos jelentése, változtatás nélkül):**

A korábbi jelentés „Tesztek” sora módosul: a `python eszkozok/teszt_futtat.py --diff 6932be23…` futás befejeződött, és két tesztfájl piros. A többi sor és az első sor (`ELTÉRÉS: 7 tétel`) változatlan, mert a két bukás okát nem tudtam az F224 diffjéhez kötni.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| Tesztek (Diéta 3.) | NEM ELLENŐRIZHETŐ | `eszkozok/olvaso_szerver/teszt_visszhang_kapu.py`, `eszkozok/olvaso_szerver/teszt_szintek.py` | 16 fájlból 14 zöld, kettő piros (részletek lent). A diff a két teszt lefedett kódját nem érinti: `git diff --numstat base..head -- eszkozok/olvaso_szerver eszkozok/visszhang eszkozok/olvasoi_kapu.py adat/visszhang_megfelelok.tsv adat/visszhang_tanuk.tsv` → 0 sor. Hogy a base-en is pirosak-e, nem tudtam megnézni (checkout nincs a megengedett parancsaim között). A CI egyiket sem futtatja. |

A két piros fájl hibái:

- **`teszt_visszhang_kapu.py`** (22 tesztből 2 bukik): `python eszkozok/teszt_futtat.py --fajl teszt_visszhang_kapu --reszletes`
  - `LancAMotivumadatbol.test_bevezeto_a_peshat_magot_es_a_kulcsszavak_szamat_mondja`: a teszt a „Peshat-magjának (1Móz 3–9) azon verse” szöveget várja, a generált blokk mást mond („A versek a Genezis láncának (1Móz 3–9) azok a versei…”).
  - `Rontott.test_v3_nincs_a_nem_azonositott_helyen`: a rontott és az eredeti blokk azonos.
- **`teszt_szintek.py`** (13 tesztből 2 bukik): `python eszkozok/teszt_futtat.py --fajl teszt_szintek --reszletes`
  - `test_ebben_a_versben_es_az_interlinearis_csempek_koveti_a_blokkok_lathatosagat`: az „Ebben a versben” szöveg ott is megjelenik, ahol nem kellene.
  - `test_heber_szavak_alacsony_es_magas_szinten`: a várt „H120. adam …” alak helyett a lapon „H0120 אָדָם …” áll.

Ez a teszt csak azért került a válogatásba, mert a `LASSU_LEFEDETT` az `adat/` előtagot figyeli, és a diff az `adat/SEMA.md`-t módosítja.

A hibák a visszhang-blokk szövegét és a szókártya alakját érintik, ami a main-en nemrég változott kódra utal (#729, F213), nem az F224-re; ez következtetés, nem igazolt. Ha a main-en is pirosak, az külön tétel a main gazdájának, nem ennek az ágnak.

## Javítókör (az 1. független ellenőrzés után, egy kör, 2026-11-16)

| ELTÉRÉS | Javítás | Fájl |
|---|---|---|
| 1. F224.7: a kinyerő elutasítja a fejléc „pótolt” mezőjét | A jelölés a fejléc helyett külön sorban, a kezdőjelölő előtt (`<!-- IGEHELY-PÓTOLT: nem vak olvasás -->`); a fejléc három mezője változatlan. A kinyerő a blokkon kívüli sort nem olvassa: próbával igazolva (`tanulmany_kinyer.blokkok_elemez` egy pótolt blokkon: 1 blokk, 0 hiba). A kinyerés nem kell (a jelölt-sor `nyitva` döntéssel egyébként is ellenőrzésre megy). **Helyesbítés:** az F224.7 szakasz „a kinyerő a main-en még nem létezik” mondata a behozott main-en már nem igaz (`aa06c044`); a kinyerő az `ir` mezőn kívül esik, és nem kellett módosítani. | `sablonok/2_PaRDeS_bovitett_sablon.md` v25 |
| 2. F224.6: az érvnapló helye ellentmondásos, DT-sor nélkül | **DT-F224e 🟡** (a felhasználó döntése): (b) `naplok/ERVNAPLO_<ID>.md`, mert a forrás új `##` szakaszát a lapgenerátor a Vitatott pontok szövegébe olvasná (`eszkozok/lapgen/bemenet/motivum.py`, `_VITATOTT_RX`), és a generátor az F218-é. A szabályhelyek a (b) szerint egységesítve: a lektor 5. kérdése (az érvnaplót a hívó adja), a `kiadas.md` 3. lépés bemenete (új sor), a bíráló bemenete, a 2_ sablon funkció-pontja, a 9_ sablon (hivatkozás a DT-re). | `.claude/agents/lektor.md`, `.claude/agents/biralo.md`, `.claude/commands/kiadas.md`, `sablonok/2_…`, `sablonok/9_…`, `dontesek/uj/` |
| 3. F224.5: a tartomány-sor versei „nem vehető át” | A `vers_allapot` a tartományt versekre bontja (`adat.versek`); teszt: `1Móz 1:4-5` tartomány-sor, mindkét verse „eldöntött” (11 teszt OK). | `eszkozok/bizonyiteklap.py`, `eszkozok/teszt_bizonyiteklap.py` |
| 4. F224.13: a HAMART-nevező | A napló 7.7 pontja kimondja: a 40. tétellel (K66) együtt 15/19 = 78,9%; a „✓” a brief 18 tételes halmazára szól. A hatókör-szűkítés és a két teljesületlen F2-küszöb a felhasználó döntése (DT-F224d, „a” nem kell) — változatlan. | `naplok/F224_proba.md` 7.7 |
| 5. F224.8: a sorrend-mondat ↔ C-a, C-g, C-h | A mondat a C-a szerint: F1 (a próza-állítás gépi része) → F2 → a gépi kapuk a lapon (C-g, C-o). A határ (C-h) időzítésének eltérése (terv és 10_ sablon: a próza előtt; C-h, C-g: utána) régebbi, a DT546-hoz kötött: **N-F224g**, a felhasználó döntése; a mondat csak hivatkozik. | `MUNKAMENET.md` |
| 6. A2: megoldott N-tételek nyitottként | Az N-F224c, e, f a fájl végén `### 2026-11-16 (lezárt, F224 — az ágon megoldva)` blokkban. | `nyitott/uj/f224-cikkiras-uj-menet.md` |
| 7. mellékes: a `fuggetlen-ellenor.md` törzse `opus`, a fejléc `fable` | Az F224 `ir` mezőjén kívül (a fájl az F218.z1-é, DT-F218o): nem javítva, utókövetés (l. a Folytatási pontot). | — |
| Kiegészítés: a `teszt_visszhang_kapu.py` és a `teszt_szintek.py` piros | A végrehajtó ellenőrizte a main-en: az `origin/main` (`6932be23`) ideiglenes worktree-jében mindkét fájl ugyanígy HIBA (`python eszkozok/teszt_futtat.py --fajl teszt_visszhang_kapu`, `--fajl teszt_szintek`). Nem az F224 okozza; a main gazdájának tétele (l. a Folytatási pontot). | — |
| F224.1: a brief 2. pontja és `ad` mezője Sonnetet ír | A brief 2. pontjában az F2 sora „Sonnet → Opus (DT-F224b)”, az `ad` mező ugyanígy. | `F224_CIKKIRAS_UJ_MENET_BRIEF.md` |

## Folytatási pont

- **Döntve (2026-11-15):** DT-F224b, DT-F224c, DT-F224d 🟢, N-F224f az ágon megoldva. A független mérés a következő új motívum cikkírásakor (DT-F224d). Előzmény: az F224.13 döntése. A felhasználó 2026-11-15-én az (A) helyett a (C)-t választotta („nézzük meg erősebb modellel”); a C-futás (az F2 Opusszal, egy futás, javítókör nélkül) kész: HAMART 83% (✓), ISTENTISZT 30%, hamis riasztás 45–50% (`naplok/F224_proba.md` 7. szakasz). A következő lépés (a modell kiosztása, N-F224c, szeletméret, küszöb) a felhasználóé, a 7.6 pont szerint. A döntés után: ha (A), egy mondat a `kiadas.md` 3. lépésébe; ha új mérés, az a döntés szerinti felállással, a `naplok/F224_proba/` bemeneteivel.
- **A #729 és a #725 merge-e után (2026-11-16) elkészült:** F224.6 (érvnapló), SEMA 2.71 (bizonyítéklap), SEMA 2.72 és a két mérőtábla (F224.11), N-F224e; l. fent.
- **A zárás előtt:** a független ellenőrzés (`fuggetlen-ellenor`, a szint a `feladatok.py szint 224` szerint) és a jelentés „Zárás” szakasza.
- N-F224b (a `teszt_bizonyiteklap.py` CI-be vétele): a #725 a main-en, de a `.github/workflows/ellenorzes.yml` és a `eszkozok/push_elott.py` az F224 `ir` mezőjén kívül esik — külön kérésre (az orkesztrátor: nyitva maradhat).
- **Utókövetés (az F224-en kívül):** a main-en (`6932be23`) piros a `eszkozok/olvaso_szerver/teszt_visszhang_kapu.py` (2/22) és a `teszt_szintek.py` (2/13) — a CI nem futtatja őket (a visszhang-blokk szövege és a szókártya alakja; #729/F213 körüli változás valószínű, nem igazolt); a `.claude/agents/fuggetlen-ellenor.md` törzsének 0. pontja `opus`-t ír, a fejléce `fable`-t (F218.z1, DT-F218o).
- **Döntve (2026-11-16):** DT-F224e 🟢 („Igen, (b)”: `naplok/ERVNAPLO_<ID>.md`). Nyitva: N-F224g (a határ időzítése, javaslat).

## Zárás

*2026-11-16, claude-opus-5-5; ág `claude/f224-cikkiras-uj-menet`, draft PR #749 (a merge az orkesztrátoré).*

- **Mi készült:** a cikkírás új menete tizenhárom tétele a saját szabályhelyén (F224.1–.13) és a döntések szerinti folytatás (F224.14–.19): az állítás-ellenőr (Opus, DT-F224b, a függetlenség módja DT-F224c), a bíráló (Sonnet), a szűkített lektor (Fable), a kinyerés négy új K-fajtája és a mondaton kívüli adat (`eszkozok/proza_allitas.py`), a bizonyítéklap (`eszkozok/bizonyiteklap.py`, SEMA 2.71), az érvnapló (9_ sablon v2.5, `naplok/ERVNAPLO_<ID>.md`, DT-F224e), a tanulmányblokk-szabály (2_ sablon v25), a mérőtábla (SEMA 2.72; HAMART 34, ISTENTISZT 18 sor), a `MUNKAMENET.md` C) menete, a határ-ellenőr Sonnetre.
- **Döntések:** DT-F224a–e 🟢 (a b–e a felhasználó 2026-11-15/16-i döntései, az orkesztrátoron át).
- **Elfogadási próba** (`naplok/F224_proba.md`): bíráló 5/6 és 5/5 ✓; F2 HAMART 15/18 = 83% (Opus; a 40. tétellel 78,9%), ISTENTISZT 7/10 = 70% (Opus, új kinyerés; nem független mérés), hamis riasztás 45–50% (N-F224d); a küszöb 80% marad, a független mérés a következő új motívum cikkírásakor (DT-F224d). Költség: kb. 2,9 millió token (Sonnet 1,93 M; Opus 1,19 M).
- **Tesztek:** `teszt_proza_allitas.py` 62 OK, `teszt_bizonyiteklap.py` 11 OK; a `--kapu` (E41) kimenete a main forrásain bájtra azonos; `feladatok.py ellenoriz` 0 hiba; a teljes push előtti kapu 0 HIBA; a CI zöld.
- **Független ellenőrzés:** 1 kör (Fable), 7 ELTÉRÉS, 1 javítókör (F224.19), minden tételre válasz a „Javítókör” táblában.
- **Nyitva (külön tételként):** N-F224a (az F1 összevetések HIBA-szintje), N-F224b (a bizonyítéklap-teszt a CI-be; az `ir` mezőn kívül), N-F224d (hamis riasztás), N-F224g (a határ időzítése); utókövetés: a `fuggetlen-ellenor.md` törzse/fejléce, a main két piros olvasó-szerver tesztje.

