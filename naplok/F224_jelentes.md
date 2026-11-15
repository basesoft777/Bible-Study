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


- **Döntve (2026-11-15):** DT-F224b, DT-F224c, DT-F224d 🟢, N-F224f az ágon megoldva. A független mérés a következő új motívum cikkírásakor (DT-F224d). Előzmény: az F224.13 döntése. A felhasználó 2026-11-15-én az (A) helyett a (C)-t választotta („nézzük meg erősebb modellel”); a C-futás (az F2 Opusszal, egy futás, javítókör nélkül) kész: HAMART 83% (✓), ISTENTISZT 30%, hamis riasztás 45–50% (`naplok/F224_proba.md` 7. szakasz). A következő lépés (a modell kiosztása, N-F224c, szeletméret, küszöb) a felhasználóé, a 7.6 pont szerint. A döntés után: ha (A), egy mondat a `kiadas.md` 3. lépésébe; ha új mérés, az a döntés szerinti felállással, a `naplok/F224_proba/` bemeneteivel.
- **A #729 (F218a) merge-e után** (a brief `fugg: [218]`): behozott main-nel (1) F224.6: az érvnapló szakasza a `sablonok/9_PaRDeS_motivum_forras_sablon.md`-ben (állítás · érvtípus · bizonyíték vagy „lekérdezendő” · döntés; a vitás pont egy helyen; a bíráló kérdéseire adott válasz helye), a 10_ sablon és a `MUNKAMENET.md` C-ev sora csak hivatkozik; (2) SEMA-szakasz a bizonyítéklap kimenetének formájára (F224.5) és a mérőtáblára (F224.11), a merge-kori következő szabad számokkal; a `MUNKAMENET.md` C-bl és C-sz sorában a hivatkozás számra cserélése; (3) a mérőtáblák (`naplok/SZIVARGAS_HAMART-001.tsv`, `naplok/SZIVARGAS_ISTENTISZT-001.tsv`) kitöltése a próba végleges eredményéből (a ⛔ döntése után).
- **A zárás előtt:** a független ellenőrzés (`fuggetlen-ellenor`, a szint a `feladatok.py szint 224` szerint) és a jelentés „Zárás” szakasza.
- N-F224b (a `teszt_bizonyiteklap.py` CI-be vétele) az F217 (#725) merge-e után.
