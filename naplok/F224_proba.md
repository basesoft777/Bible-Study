# F224.13 — Elfogadási próba: a cikkírás új menetének szerepei visszajátszással

*Végrehajtó és pontozó: claude-opus-5-5, 2026-11-15. A nyers ügynöki kimenetek változtatás nélkül: `naplok/F224_proba/`; a bemenetek és eredetük: `naplok/F224_proba/bemenet/README.md`.*

## 1. Módszer (a 2026-11-15-i méréssel azonos)

- **Bemenet:** a javítás előtti állapot — HAMART-001 `f6da955e`, ISTENTISZT-001 `b2aea73f` (forrás, `elofordulasok`, `kapcsolatok`, `jeloltek`, a lap címsorai); a kézi lista az **új kinyeréssel** (F224.4): HAMART 118, ISTENTISZT 58 K-tétel.
- **Vakság:** az ügynökök nem látták a lektori listákat, a naplókat, a `motivumok/` mai állapotát és a git-történetet; a motívum sorait a bemenet-mappából olvasták.
- **Szerepek és modell (a brief 2. pontja):** F2 állítás-ellenőr ×3 (HAMART két szeletben, ISTENTISZT egyben), D bíráló ×2 (ISTENTISZT három vitatott pontja; HAMART 8:21), mind `claude-sonnet-5-5` (az ügynökök modell-ellenőrzése: egyezik).
- **Eltérés a tervtől:** a két új szerepfájl ebben a sessionben még nem volt regisztrált ügynöktípus (a session indulásakor töltődnek be), ezért az ügynök `general-purpose` típusú, `model: sonnet`, és első lépésként a szerepfájlt (`.claude/agents/allitas-ellenor.md`, `.claude/agents/biralo.md`) olvasta be utasításként. A tartalom azonos; a különbség, hogy az eszközkészletben az írás is megvolt (a scratch-mappán kívül nem írtak).
- **Az ISTENTISZT bíráló-bemenete:** az érvvázlatot nem az író fogalmazta (a végrehajtó a lektori listát már látta, így a vakság sérült volna), hanem gépi kivonat: a vitatott pontok szó szerint, és a lap más mondatai, amelyek ugyanazokra a versekre támaszkodnak (`naplok/F224_proba/ervvazlat_kinyer.py`). A 8:21-es bíráló a 2026-11-15-i érvvázlatot kapta változatlanul, és az F224.5 bizonyítéklapját.
- **Számolás (a brief szerint):** „megfogta” = az ítélet nem „igazolt”, és az indok a lektori tétel hibáját nevezi meg; „részben” külön (a tételt jelölte, más okból, vagy a hibát a K-listán kívül, a saját „lista-hézag” megjegyzésében nevezte meg) — a küszöbbe nem számít.

## 2. Eredmény — 1. kör

| Halmaz | Mérő | Küszöb | 2026-11-15 | **1. kör** | |
|---|---|---|---|---|---|
| HAMART, a lektor 18 kézi listás tétele | F2 | ≥ 80% | 56% (részlegessel 67%) | **10/18 = 56%** (részlegessel 12/18 = 67%; a bírálóval 11/18) | ✗ |
| ISTENTISZT, 10 vers- és adatállítás-tétel | F2 | ≥ 80% | 25% | **2/10 = 20%** (részlegessel 5/10) | ✗ |
| ISTENTISZT, 6 bíráló-típusú tétel | D | ≥ 4/6 | nem mérve | **5/6** | ✓ |
| HAMART 8:21, öt ismert pont | D | 5/5 | Sonnet 5/5 | **5/5** | ✓ |
| az F2 többlet-jelzései, vak minta (12) | — | hamis riasztás ≤ 30% | nem mérve | **5/10 = 50%** (2 nem dönthető el) | ✗ |

Az F2 „nem eldönthető” aránya: HAMART 1/59 + 4/59, ISTENTISZT 3/58 = 8/176 = **4,5%** (küszöb 15%, ✓).

### 2.1 HAMART — tételenként

| Lektor | K | F2 ítélet | Eredmény | Ha nem fogta meg: mechanizmus |
|---|---|---|---|---|
| 8 | K5 | nem eldönthető | ✗ | *Hány?* — „a görög szó” egyes szám (három szó), a keresés a két kivett szót is tartalmazza; a K-tételt a lefedettség felől nézte |
| 9 | K104 | hamis | ✓ | |
| 10 | K104, K106 | hamis, vitatott | ✓ | |
| 11 | K106 | vitatott | részben | *Ki?* — a hallás alanya Isten; az indok mást nevez meg |
| 12 | K105 | igazolt | ✗ | *Mit?* — az indokban maga írja, hogy erec áll, mégis igazolt (a lap „föld szava” = adámá) |
| 13 | K98 | vitatott | ✓ | |
| 14 | K98, K102 | vitatott | részben | *Mit?* — a föld nem szerepel; az indok a „visszautalás” értelmezés voltát nevezi |
| 21 | K14 | igazolt | ✗ | *Csoport* — a 6:20 nem a lap helye; az indokban leírja, mégis igazolt |
| 22 | K28 | igazolt | ✗ | *Hány?* — a felsorolás teljessége a tábla `karoli_szo` mezőjével nincs összevetve |
| 28 | K31 | vitatott | ✓ | |
| 29 | K33 (K45) | vitatott | ✓ | |
| 31 | K39 | vitatott | ✓ | |
| 33 | K41 | igazolt | ✗ | *Másik hely* — a belső utalás célpontját nem olvasta el (létezik, de mást tárgyal) |
| 34 | K44 | vitatott | ✓ | |
| 35 | K47 | vitatott | ✓ | |
| 36 | K50 (F2: igazolt) | — | ✓ (D) | a bíráló 2. tétele (a lap két iránya) |
| 38 | K55 | hamis | ✓ | |
| 42 | K71 | vitatott | ✓ | |

A régi menetben a gépi (F1) tételek: 5, 6, 32, 41, 43 — változatlanul a gépi kapué. A 2026-11-15-i K-tétel nélküli tételek közül a 30. és a 37. most sem K-tétel; a 40. (K66) igazolt (✗).

### 2.2 ISTENTISZT — a 10 vers- és adatállítás-tétel

| Lektor | K | F2 ítélet | Eredmény | Ha nem fogta meg: mechanizmus |
|---|---|---|---|---|
| 1 | — (a Remez-mondat a gépi „egyezik” idézet mögött; K50 a helyes mondat) | — | ✗ | **kinyerés**: az idézettel lefedett mondat többet állít, mint az idézet, mégsem kerül a listára |
| 2 | — (a 13. sor mondata igehely nélkül) | — | részben | **kinyerés**: igehely nélküli szabály-mondat nem K-tétel; az F2 a „lista-hézag” megjegyzésében magától megtalálta (Zsolt 116:4, 13, 17) |
| 5 | K27 | igazolt | ✗ | *Mit?* — az adatsor „parafrazált, nincs szó szerinti egyezés”, a próza „ugyanaz a szókapcsolat” |
| 8 | K52 | vitatott | részben | *Ki?* — a „megáll Mózes mellett” az álla alanyát eldönti; az indok mást nevez meg |
| 10 | K25 | vitatott | ✓ | |
| 12 | K13, K15 | igazolt | ✗ | *Másik hely* — a BDB a kizárt Jer 10:25 = Zsolt 79:6-ot is ide sorolja |
| 13 | K22 | vitatott | ✓ | |
| 15 | K4 | igazolt | ✗ | *Ki?* — a vers a gyülekezet mellé állítja a segítségül hívókat |
| 16 | K5 | vitatott | részben | *Csoport* — az 1Móz 4:26 nem a pátriárkák története; az indok mást nevez meg |
| 17 | K7 | igazolt | ✗ | *Ki?* — az indokban maga írja, hogy az Ézs 43:1, 45:3-ban az Úr hív embert, mégis igazolt |

**Többlet a 10-es halmazon kívül:** az új kinyerés négy K-tétele közül az F2 hármat a lektor tétele szerint ítélt (K55 = a 4. tétel „három kapcsolat erős”, vitatott, 13 magas sorral; K56 = a 6. tétel, hamis; K57 = a 9. tétel, vitatott), és a „lista-hézag” megjegyzésben a 3. tételt (Jézus Krisztus neve) is megnevezte.

### 2.3 Bíráló — ISTENTISZT (6) és HAMART 8:21 (5)

| Tétel | A bíráló tétele | Eredmény |
|---|---|---|
| IST 3 (Jézus Krisztus: egy versből a csoportra, a Róm 10:13 pont ellen) | S3.3 | ✓ |
| IST 6 (2Móz 33:19, 34:5: „nem dönti el”, a lap dönt) | S1.1 | ✓ |
| IST 7 (a második olvasat csak a 34:5-re szól) | K1.3 | ✓ |
| IST 9 (1Móz 4:26: a pont dönt is; az olvasatok érvei) | S2.2, K2.2 | ✓ |
| IST 14 (Módszertan ↔ 9. táblázat, a kritikai szöveg) | — | ✗ (a mondat nem az érvvázlat pontjaihoz kötődik) |
| IST 18 (Róm 10:13: az első olvasat érv nélkül) | S3.2 | ✓ |
| 8:21: qalal és árar az 1Móz 12:3-ban | 1. | ✓ |
| 8:21: az 1. olvasat hallgatásból vett | 3. | ✓ |
| 8:21: a „-ért” (H5668) a 3:17-ben és a 8:21-ben | 5. | ✓ |
| 8:21: a Róm 8:21 recepció (szintkeverés) | 6. | ✓ |
| 8:21: a szakirodalmi támaszkodás ellenőrizetlen | 10. | ✓ (a 2026-11-15-i K9-cel azonos számolás) |

Többlet: a 8:21-en a qalal Qal-alakja ugyanebben a fejezetben (8:8, 8:11), a két „nem … többé” tagmondat, a Kivonat–Remez–Sod három iránya (= a HAMART-lektor 36. tétele); az ISTENTISZT-en a 34:5 wayyiqtol-láncának alanya, az Onkelos 34:5 alanya, a Róm 10:11–14 közvetlen szövegtanúja.

### 2.4 Az F2 többlet-jelzései — vak minta

A sokaság: az F2 nem „igazolt” ítéletei, amelyek a lektori listákon (HAMART 34 + az orkesztrátori tételek; ISTENTISZT 22 + a régi átnézés 9 HIBÁ-ja) nem szerepelnek: 16 tétel. Minta: 12, `random.Random(224).sample` (a sokaság kijelölése után; a HAMART K7-ről a minősítéskor kiderült, hogy a lektor 2. tétele fedi — nem került a mintába). Minősítés versszöveggel vagy adatsorral (`naplok/F224_proba/minosit.py`):

| Tétel | F2 | Minősítés | Forrás |
|---|---|---|---|
| HAM K101 (Sof 1:2-3 „az özönvíz szavaival”) | vitatott | valódi | TAHOT: a Sof igéi ászaf/kárat, a Gen 6:7-é máchá; közös csak a „föld színe” és a felsorolás |
| HAM K30 („minden test” a következmény alatt, 6:12) | vitatott | valódi | TAHOT/Károli 6:12: a „minden test” a cselekvő; a következmény a 6:13 |
| HAM K60 (a négy tematikus helyet „a lexikai keresés nem látja”) | vitatott | valódi | a keresés Strong-listájában a H7451 áll, és az a 6:5-ben is áll |
| HAM K64 (573 vers csak ra'-val) | nem eldönthető | valódi | TAHOT: a H7451 621 verséből a többi héber lánc-szó nélkül 582 (a qalal nélkül is 582) |
| HAM K90 (6:17: „a megromlott föld elvesztése”) | vitatott | valódi | TAHOT 6:17: az ige tárgya „minden test” |
| HAM K11 („egyetlen hely tér el … erősítő törzs”) | vitatott | hamis riasztás | a mondat a törzsről szól; a lánc árar-helyei közül csak az 5:29 Pi'el (a 12:3 Qal) |
| HAM K36 („három hely mutat a láncon túlra”) | vitatott | hamis riasztás | képes beszéd (előremutat); a „láncon belül állnak” nem cáfolja |
| HAM K57 (1 074 vers) | vitatott | hamis riasztás | a forrás állapotán (`f6da955e`) a BDB+Thayer uniója 1 074; a mai tábla 1 075 |
| HAM K94 (Zsolt 14: „mint ott, letekint”) | vitatott | hamis riasztás | mindkét helyen Isten tekint le; a tárgy eltérése az állítást nem cáfolja |
| IST K33 („az egyik olvasat szerint …”) | vitatott | hamis riasztás | olvasatként jelölt olvasat leírása, pontos |
| HAM K67 (κατανάθεμα jelentése) | vitatott | nem dönthető el | a Thayer G2652 jelentést nem ad, csak utal |
| HAM K73 (Gal 5:3 mint a feltételes átok) | vitatott | nem dönthető el | olvasat; a vers az átkot nem mondja, de az olvasatot nem is zárja ki |

## 3. A meg nem fogott tételek mechanizmusai (a javítókör alapja)

1. **Észrevett, de „igazolt” (M-IGAZOLT-ESZREVETT, új):** az F2 az indokban leírja az eltérést, és mégis „igazolt”-at ad (HAM 12, 21; IST 17). A szerepfájl szabálya („ha bármelyik kérdésre nem, nem lehet igazolt”) megvan, de az ügynök a kérdést „i”-re töltötte, mert a „fő állítást” ítélte.
2. **A mellékige alanya (Ki?):** a mondat mellékigéjének alanyát nem nézte (IST 8: „megáll Mózes mellett”; IST 15; HAM 11).
3. **A lap saját szóhasználata (Mit?):** a lap „a föld szava” = adámá; az erec ott eltérés (HAM 12, 14).
4. **A felsorolás teljessége és a szám-nyelvtan (Hány?):** a felsorolás nincs a tábla mezőjével összevetve (HAM 22), az egyes szám nem a darabszám (HAM 8).
5. **A belső utalás tartalma:** a célpont létezik, de nem azt tárgyalja (HAM 33).
6. **Adatsor ↔ próza árnyalat:** „parafrazált” ↔ „ugyanaz a szókapcsolat” (IST 5).
7. **Kinyerés (nem a szerepfájlé):** az idézettel lefedett mondat többletállítása és az igehely nélküli szabály-mondat nem K-tétel (IST 1, 2). Ez az F224.4 kinyerésének hézaga; a javítása a szerepfájl javítókörén kívül esik (javaslat: 6. szakasz).
8. **Hamis riasztás:** a képes beszéd betű szerinti cáfolata (K36, K94), az olvasatként jelölt olvasat „vitatott”-ja (IST K33), a mai tábla a forrás állapota helyett (K57), a mondat saját vonatkoztatásának figyelmen kívül hagyása (K11).

## 4. Költség — 1. kör

| Lépés | Modell | Token | Eszközhívás | Idő |
|---|---|---|---|---|
| F2 HAMART 1. szelet | sonnet | 292 100 | 34 | 959 s |
| F2 HAMART 2. szelet | sonnet | 290 555 | 43 | 913 s |
| F2 ISTENTISZT | sonnet | 245 367 | 51 | 1 094 s |
| D ISTENTISZT | sonnet | 144 504 | 14 | 319 s |
| D HAMART 8:21 | sonnet | 97 302 | 6 | 132 s |
| **összesen** | | **1 069 828** | 148 | |

Keret (`get_usage`): előtte (15:00 körül) 5 órás 37%, heti 20%, Fable 6%. A becslés (kb. 1 millió token, 1–2 százalékpont a heti keretből, ×1,7) a tokenre stimmelt.

## 5. Javítókör (egy, a brief szerint) és ismétlés — 2. kör

**A javítókör** (`3e0c4385`, `.claude/agents/allitas-ellenor.md`), a 3. szakasz mechanizmusai szerint: a mondat minden része állítás; az indokba írt eltérés „nem” válasz („igazolt, de …” nincs); *Ki?* minden igénél; *Mit?* a lap és az adatsor saját szóhasználatához mérve; *Hány?* a felsorolás teljessége és az egyes szám; a belső utalás célpontjának tartalma; a hamis riasztás ellen: olvasat, képes beszéd, saját vonatkoztatás, a forrás állapota. **A javítás példái nem a próbahalmaz tételei** (különben az ismétlés a választ kapná meg, nem a mechanizmust). *Mérési korlát:* a szerepfájl eredeti, a brief által előírt példái a 2026-11-15-i mérésből valók, így az ISTENTISZT 1., 2., 3., 10. és a HAMART 31., 35. tétele mindkét körben példaként szerepelt.

**Ismétlés** ugyanazon a bemeneten, ugyanazzal a módszerrel (3 F2-ügynök, Sonnet; a kimenetet maguk írták fájlba: `naplok/F224_proba/*_2kor.md`).

| Halmaz | Küszöb | 1. kör | **2. kör** | A két kör uniója (tájékoztató) |
|---|---|---|---|---|
| HAMART 18 | ≥ 80% | 10/18 = 56% | **11/18 = 61%** (részlegessel 13/18 = 72%; a bírálóval 12/18) | 12/18 = 67% |
| ISTENTISZT 10 | ≥ 80% | 2/10 = 20% | **3/10 = 30%** (részlegessel 4/10) | 4/10 |
| hamis riasztás, vak minta (12) | ≤ 30% | 5/10 = 50% | **6/12 = 50%** | — |
| „nem eldönthető” | ≤ 15% | 4,5% | 10/176 = 5,7% | — |

**Változás tételenként (2. kör):**
- HAMART — új találat: 22 (K28, a felsorolás hiányos: „erőszaktétel”, „erőszakkal”, „erőszak”); megmaradt: 9, 10, 21, 28, 29, 31, 34, 35, 38, 42; **visszaesés:** 13 (K98 most igazolt); továbbra sem: 8 (K5 most igazolt), 12 (K105 igazolt), 33 (K41 igazolt); részben: 11, 14.
- ISTENTISZT — új találat: 1 (K50: a funkció-mező szerint a formula „a Baál prófétáinak szájában”, a versben Illés mondja), 15 (K4: a gyülekezet nem azonos azok közösségével); megmaradt: 13 (K22); **visszaesés:** 10 (K25 most igazolt); továbbra sem: 2 (nem K-tétel), 5, 8, 12, 17 (mind igazolt); részben: 16.
- A vak minta (2. kör, `random.Random(224)`, a 13 tételes többlet-sokaságból 12): valódi hiba K30, K90, K95 („Ezékiel láncot készíttet” — a versben ő készíti), K100, K113, IST K37 (a 395 csak a két igére áll, a mondat három szót nevez); hamis riasztás K32, K78, K88 (a BDB szerint a kol-basar itt „mankind”), K89, K94, K107.

**Költség (2. kör):** F2 HAMART 1. szelet 284 092, 2. szelet 274 977, ISTENTISZT 297 390 token — együtt 856 459 (Sonnet). Keret a 2. kör előtt: 5 órás 54%, heti 22%. A két kör együtt 1 926 287 token.

## 6. ⛔ Eredmény és javaslat (a felhasználó dönt)

**A javítókör után is a küszöb alatt marad mindhárom F2-mérőszám** (HAMART 61%, ISTENTISZT 30%, hamis riasztás 50%). A bíráló mindkét küszöbe teljesül (5/6, 5/5). A TEREMT-001 a teljes menettel a brief szerint nem indul.

**Mit mutat a két kör:**
1. **A Sonnet-F2 ingadozik:** a két kör között tételek fordultak meg mindkét irányba (HAM 13, 22; IST 1, 10, 15), azonos bemeneten. Egyetlen futás nem megbízható szűrő; a két kör uniója is csak 67% / 40%.
2. **A szabály megvan, a végrehajtás hiányos:** a „ha bármelyik kérdésre nem, nem lehet igazolt” szabály mellett az ügynök a 2. körben is adott „igazolt”-at olyan tételre, amelynek eltérését az 1. körben ugyanaz a szerep megnevezte (HAM K105, IST K7, K25). A hiba nem a kérdéslistában, hanem a figyelem elosztásában van: 59 tételt egy menetben, tételenként 7 kérdéssel.
3. **Két tétel kinyerési hézag** (IST 1. a K-listán csak a helyes mondattal, 2. egyáltalán nem): N205. Ezek nélkül az ISTENTISZT-halmazon a 80% csak hibátlan munkával érhető el.
4. **A hamis riasztás fele értelmezésnek jelölt vagy az adattal alátámasztott mondatot kifogásol** — a javítókör szabálya ezen nem változtatott (50% → 50%).

**Javaslat:**
- **(A) most:** az F2 marad, de **a lektor hatókör-szűkítésének 1. pontja nem lép életbe** — a lektor az F2 „igazolt” tételeit is olvassa (vak minta helyett mind), amíg az F2 egy újabb próbán nem éri el a küszöböt. Ez a `kiadas.md` 3. lépésében egy mondat. Ára: a lektor terhe nem csökken; haszna: a menet többi része (bíráló, bizonyítéklap, kinyerés, érvnapló) használható, és az F2 jelzései többletet adnak (mindkét körben új, valódi hibákat talált a lektor listáján kívül).
- **(B) a következő mérés előtt:** (1) N205 (a kinyerés két hézaga); (2) **kisebb szeletek** (20–25 K-tétel ügynökönként a 59 helyett), mert a figyelem a tételszámmal romlik; (3) **két független futás uniója** a „nem igazolt” jelzésre (a hamis riasztást a lektor szűri).
- **(C) modell:** a szerepfájl `model` mezője cserélhető; egy Opus-futás ugyanezen a halmazon megmutatná, hogy a hiány a modellé vagy a szerepé. Ez a felhasználó döntése (a 2. pont kiosztása jóváhagyott, Sonnettel).
- **A küszöb** változatlan javaslatként; a 80% a jelenlegi felállással nem elérhető.

## 7. C-futás: az állítás-ellenőr Opusszal (a felhasználó döntése, 2026-11-15)

*A döntés szó szerint (az orkesztrátor továbbításában): „'a' nem kell úgysem lesz új cikkírás a generátorig / nézzük meg erősebb modellel”. A futás: 3 ügynök (`general-purpose`, `model: opus`, a tényleges modell `claude-opus-5-5`, a modell-ellenőrzésük: egyezik), a szerepfájl a `3e0c4385` állapotában (változatlan), ugyanazok a bemenetek és szeletek, mint a 2. körben, javítókör nélkül, egy futás. Az összevetés pontos párja a **Sonnet 2. köre** (azonos szerepfájl-szöveg); az 1. kör a javítókör előtti szerepfájllal futott, ezért vele csak tájékoztató az összevetés. A vak szabály egy ponton szigorúbb a 2. körnél: a Sonnet-futások kimeneteit (`proba/*.md`, `munka2_*`) is tiltotta. Nyers kimenetek: `naplok/F224_proba/*_opus.md`; összevetés: `naplok/F224_proba/opus_osszevet.py`; minta: `naplok/F224_proba/opus_minta.py`.*

| Halmaz | Küszöb | Sonnet 1. kör | **Sonnet 2. kör (pár)** | **Opus** | |
|---|---|---|---|---|---|
| HAMART 18 | ≥ 80% | 10/18 = 56% | 11/18 = 61% (részlegessel 13/18) | **15/18 = 83%** (részlegessel 17/18) | ✓ |
| ISTENTISZT 10 | ≥ 80% | 2/10 = 20% | 3/10 = 30% (részlegessel 4/10) | **3/10 = 30%** (részlegessel 4/10) | ✗ |
| hamis riasztás, vak minta (12) | ≤ 30% | 5/10 = 50% | 6/12 = 50% | **5/11 = 45%** (a K57-tel együtt 6/12 = 50%) | ✗ |
| „nem eldönthető” | ≤ 15% | 4,5% | 5,7% | **10/176 = 5,7%** | ✓ |

**Az ítéletek eloszlása:** az Opus több tételt jelöl. Nem „igazolt”: HAMART 52/118 (Sonnet 2. kör 39, 1. kör 39), ISTENTISZT 21/58 (18, 19); „hamis”: HAMART 22 (6), ISTENTISZT 9 (4).

### 7.1 HAMART — tételenként (Sonnet 2. kör → Opus)

| Lektor | K | S2 | Opus | Eredmény | Megjegyzés |
|---|---|---|---|---|---|
| 8 | K5 | igazolt | hamis | ✓ új | az egyes számú „a görög szó” három szóval szemben; a φθείρω-család három tagja kimaradt a keresésből |
| 9 | K104 | hamis | hamis | ✓ | |
| 10 | K104, K106 | hamis, vitatott | hamis, hamis | ✓ | |
| 11 | K106 | vitatott | hamis | részben | az indok a 10. tétel hibája (a szópár nincs a Genezisben); a hallás alanyát (Isten) pontosnak mondja |
| 12 | K105 | igazolt | hamis | ✓ új | a Jer 51:46-ban erec |
| 13 | K98 | igazolt | vitatott | ✓ (S1-ben is ✓) | Tírus királya (28:12), a „fejedelem” a 28:2-é |
| 14 | K98, K102 | igazolt, vitatott | vitatott, vitatott | részben | a Sof 1:9 hiányzó kapcsolat-sorát nevezi; azt nem, hogy a föld nem szerepel |
| 21 | K14 | vitatott | igazolt | ✗ visszaesés | *Csoport* — a 6:20-at a 6:9-22 helyének veszi; nem nézi, hogy a lap helye-e |
| 22 | K28 | vitatott | hamis | ✓ | |
| 28 | K31 | vitatott | hamis | ✓ | |
| 29 | K33, K45 | vitatott | vitatott | ✓ | |
| 31 | K39 | vitatott | vitatott | ✓ | |
| 33 | K41 | igazolt | vitatott | ✓ új | a belső utalás célpontja mást tárgyal |
| 34 | K44 | vitatott | hamis | ✓ | |
| 35 | K47 | vitatott | vitatott | ✓ | |
| 36 | K50 (+K116) | igazolt (D: ✓) | vitatott, vitatott | ✓ új (F2) | a Sod és a Kivonat ellentmondása; K116: a lap másutt a második olvasat felé dönt |
| 38 | K55 | hamis | hamis | ✓ | |
| 42 | K71 | vitatott | hamis | ✓ | |

**Új az Opusnál:** 8, 12, 33, 36 (és a 13 vissza). **Visszaesés:** 21. A lektori listán túl az F1-gépi 43. tételt (K72, „de más kulcsszóval”) is megfogta.

### 7.2 ISTENTISZT — tételenként (Sonnet 2. kör → Opus)

| Lektor | K | S2 | Opus | Eredmény | Megjegyzés |
|---|---|---|---|---|---|
| 1 | K50 / funkció-mező | vitatott | igazolt | ✗ visszaesés | a K-mondat helyes; a hibás funkció-mezőt nem nézte meg (*Másik hely*), a Remez-mondat kinyerési hézag (N205) |
| 2 | — | — | — | ✗ | kinyerési hézag (N205); az Opus a „lista-hézag” megjegyzést sem tette |
| 5 | K27 | igazolt | hamis | ✓ új | „parafrazált, nincs szó szerinti egyezés” ↔ „ugyanaz a szókapcsolat” |
| 8 | K52 | igazolt | igazolt | ✗ | *Ki?* — a LXX (παρέστη αὐτῷ) alapján az álla alanyát az Úrnak veszi, a vers ezt nem dönti el |
| 10 | K25 | igazolt | igazolt | ✗ | *Mit?* — az 1Móz 4:26 Targumában a celá szava megvan, a mondat jelentése fordított; ezt ötödiknek számolja |
| 12 | K13, K15 | igazolt | igazolt | ✗ | *Másik hely* — a BDB a kizárt Jer 10:25-öt is ide sorolja |
| 13 | K22 | hamis | hamis | ✓ | 13/2/1, nem 12/3/1 |
| 15 | K4 | vitatott | vitatott | ✓ | |
| 16 | K5 | vitatott | hamis | részben | a régi átnézés hibáját nevezi (a 34:5 elbeszélés), a pátriárkákat nem |
| 17 | K7 | igazolt | igazolt | ✗ | *Ki?* — az Ézs 43:1, 45:3-ban az Úr hív embert; nem vette észre |

**A 10-es halmazon kívül** az Opus az ISTENTISZT-lektor bíráló-típusú tételei közül négyet F2-ítéletként fogott meg: 3. (K58, „Jézus Krisztus” egy versből), 4. (K55, 13 magas sor), 6. (K56, „nem dönti el”, a lap másutt dönt), 9. (K57); a Sonnet 2. köre ezekből kettőt (K55, K56). A régi átnézés 9 HIBÁ-jából az Opus nyolcat jelöl (a K23 igazolt). Mellékes adatlelete az `adat/kapcsolatok.tsv` 1Móz 13:4 „Beérseba” hibája — ez a 2. kiadás lektorának generált-adat megjegyzése.

### 7.3 Ingadozás és „igazolt eltéréssel”

- **Fordulat az „igazolt / nem igazolt” határon** (azonos bemenet): Sonnet 1. ↔ 2. kör 22/118 + 7/58; Sonnet 2. kör ↔ Opus 29/118 + 5/58. Az Opus egy futás, a saját ingadozása nem mért; az eltérés a Sonnettől nagyobb, mint a Sonnet két köre között, és túlnyomórészt egyirányú (HAMART: 16 tétel az Opusnál új jelzés, 8 tétel csak a Sonnet 2. körében jelzett).
- **„Igazolt eltéréssel” (M-IGAZOLT-ESZREVETT):** az Opus-kimenetben ilyen eset nincs. A gépi keresés („azonban”, „viszont”, „de a …”, „pontatlan”, „eltér” egy „igazolt” sor indokában) egy sort ad (K68), ott az ellentét a szövegváltozatra vonatkozik, nem a mondatra. A Sonnet 2. körében ugyanez a keresés 5 sort ad (HAM K2, K67, K75; IST K3, K15). Az Opus meg nem fogott tételeinél az eltérést nem vette észre (IST 8, 10, 12, 17; HAM 21), de egyiknél sem írta le úgy, hogy közben „igazolt”-at adott.

### 7.4 A többlet-jelzések — vak minta

A sokaság: az Opus nem „igazolt” ítéletei, amelyeket a lektori listák (HAMART 1–46; ISTENTISZT 2. kiadás 1–22 és a régi átnézés 9 HIBÁ-ja) nem fednek: 25 tétel (a fedésnél a lektori tételnek ugyanarra a mondatra kell vonatkoznia; a K72-t a 43., a K115-öt a 36. tétel, az IST K39 és K41 mondatát a 22. tétel fedi). Minta: 12, `random.Random(224).sample` a rögzített sokaságból (`opus_minta.py`).

| Tétel | Opus | Minősítés | Forrás |
|---|---|---|---|
| HAM K2 (6:11-13 „föld”, a Kivonat adámá-láncában) | vitatott | valódi | TAHOT 6:11-13: H0776; a lektor 28. tételének mércéje szerint (a váltás jelöletlen) |
| HAM K30 („minden test” a következmény alatt) | hamis | valódi | ua. mint a 2.4 és az 5. szakaszban |
| HAM K90 (6:17 „a föld elvesztése”) | hamis | valódi | ua. |
| HAM K97 (Ez 12:19: a kiürülő föld adámá) | hamis | valódi | TAHOT Ez 12:19: a kiürülő föld `אַרְצָהּ` (H0776), az adámá a megszólítás („Izráel földje”); a „melóá” a ragos alak (מְלֹאָהּ), ez a részállítás nem hiba |
| HAM K99 (Zsolt 74:20 „a megtelt föld”) | vitatott | valódi | TAHOT: a `מָלְאוּ` alanya a föld rejtekhelyei (H4285) |
| IST K37 (395 vers, három szóra mondva) | vitatott | valódi | ua. mint az 5. szakaszban |
| HAM K9 (Ézs 24, Hós 4: a föld erec) | vitatott | hamis riasztás | a mondat a négy helyet maga vezeti be „a lánc szavai nélkül” (ham_forras.md:21); az ügynök maga írja, hogy ez „enyhíti” |
| HAM K21 (sáchat: „a két jelentés egymásba fordul”) | vitatott | hamis riasztás | a bekezdés a sáchat két jelentéséről szól, adámát nem állít; az erec-kifogás a mondaton kívülről jön |
| HAM K46 (Drash: „a földet többé nem átkozza meg”, 8:21) | vitatott | hamis riasztás | a vers hű parafrázisa; az árart nem állítja |
| HAM K48 („A láncban az átok kimondott szó, nem személytelen erő”) | vitatott | hamis riasztás | saját vonatkoztatás: „a láncban” = a lánc átok-szavai; az Ézs 24:6 (álá) tematikus hely |
| HAM K94 (Zsolt 14: „mint ott, letekint”) | hamis | hamis riasztás | ua. mint a 2.4 szakaszban (a tárgy eltérése az állítást nem cáfolja) |
| HAM K57 (1 074 vers) | nem eldönthető | nem hiba, szabályos „nem eldönthető” | a szerepfájl „a forrás állapota” szabálya szerint helyes ítélet; a lektorhoz kerül, de nem téves jelzés |

### 7.5 Költség

| Lépés | Modell | Token | Eszközhívás | Idő |
|---|---|---|---|---|
| F2 HAMART 1. szelet | opus | 303 426 | 38 | 1 068 s |
| F2 HAMART 2. szelet | opus | 289 342 | 42 | 940 s |
| F2 ISTENTISZT | opus | 258 054 | 29 | 677 s |
| **összesen** | | **850 822** | 109 | |

Ugyanannyi token, mint a Sonnet 2. körében (856 459), Opus-áron. Keret: előtte 5 órás 0% (a 18:50Z-i nullázás után), heti 26%; utána 5 órás 13%, heti 28%.

### 7.6 Mit mutat (a következő lépésről a felhasználó dönt)

1. **A HAMART-hiány nagyrészt a modellé volt:** ugyanazzal a szerepfájllal az Opus 61% helyett 83%-ot ér el, és megfogja azt a négy tételt, amelyet a Sonnet két körben sem (8, 12, 33, 36 F2-ként). Az „észrevett, de igazolt” hibamód eltűnt.
2. **Az ISTENTISZT-hiány nem a modellé:** 30% mindkét modellel. A tíz tételből kettő kinyerési hézag (N205: 1., 2.), egy a bizonyíték mérlegelésén múlik (8.: a LXX alanya), három pedig a „másik hely” és a „Ki?” kérdésé, ahol a hibát egy, a mondaton kívüli adat hordozza (12.: a BDB a kizárt helyet is ide sorolja; 17.: az Ézs 43:1-ben az Úr hív; 10.: a Targum mondatának iránya). Az N-F224c-vel a felső korlát 8/10, a küszöb pedig hibátlan munkát kívánna a maradék nyolcon.
3. **A hamis riasztás nem csökkent** (45–50%): az Opus többet jelöl (HAMART 52 nem igazolt a 39 helyett), a valódi és a téves jelzés aránya hasonló. A többlet a lektor terhe, nem a kiadás kockázata.
4. **Ingadozás:** egy Opus-futás; a saját stabilitása nem mért. A Sonnet két köre között 29 fordulat volt; az Opus és a Sonnet 2. köre között 34.

## 8. Újramérés az ISTENTISZT-szeleten: Opus, a kinyerés javítása után (F224.14–.17)

*A felhasználó döntése (2026-11-15, az orkesztrátoron át): „Igen, így menjen” — az F2 Opusra (DT879), N205 (F224.14), a mondaton kívüli adat a kinyerésben (F224.15), utána egy újramérés csak az ISTENTISZT-szeleten Opusszal, ugyanazokkal a mérőkkel; a HAMART nem fut újra, a hamis riasztás csökkentése nem e kör része (N203). A futás: 1 ügynök (`general-purpose`, `model: opus`, a tényleges modell `claude-opus-5-5`, a modell-ellenőrzése: egyezik; „a próza modellje is ez” — DT880 🟡), a szerepfájl a `489c7ebd` állapotában, a bemenet a `b2aea73f`-es forrás és adatok, a lista az új kinyeréssel (`bemenet/ist/ist_lista_v2.md`, 75 K-tétel), javítókör nélkül. Nyers kimenet: `naplok/F224_proba/F2_ISTENTISZT_opus2.md`.*

**Mérési korlát (kimondva):** a javítás (F224.14–.15 és a szerepfájl új bekezdése) ugyanannak a tíz tételnek a 7.2 szakaszbeli mechanizmusaiból készült, amelyen most mérünk. A végrehajtó a próbahalmaz tételeit nem írta példának (egy ilyen példát a commit előtt kivett), de a mechanizmus-választás e tíz tételből jön; az újramérés ezért **nem független**. A független mérés egy új motívumon vagy egy új mintán lehetséges.

| Mérő | Küszöb | Sonnet 2. kör | Opus (7. sz.) | **Opus, új kinyerés (8. sz.)** | |
|---|---|---|---|---|---|
| ISTENTISZT 10 | ≥ 80% | 3/10 = 30% | 3/10 = 30% | **7/10 = 70%** (részlegessel 8/10) | ✗ |
| „nem eldönthető” | ≤ 15% | 5,2% (3/58) | 8,6% (5/58) | **2,7%** (2/75) | ✓ |
| hamis riasztás (vak minta) | ≤ 30% | 50% | 45% | **0/2** a lektori listán kívüli sokaságon (3 tétel, 12-es minta nem állítható elő); a funkció-mező miatti ismételt jelzéssel együtt 3/5 | — (l. lent) |

### 8.1 Tételenként (Opus 7. sz. → Opus 8. sz.)

| Lektor | K (új lista) | 7. sz. | 8. sz. | Eredmény | Megjegyzés |
|---|---|---|---|---|---|
| 1 | K50 (funkció-mező), K61 (Remez, új: idézeten túl) | igazolt, — | hamis, hamis | ✓ új | a funkció-mező és a Remez-mondat: a formulát Illés mondja, a próféták szájában „Baál! hallgass meg minket!” |
| 2 | K60 (új: szabály-mondat) | — | hamis | ✓ új | a Zsolt 116:4, 13, 17-ben előbb a név, utána az ige |
| 5 | K27 | hamis | vitatott | ✓ | az adatsor („nincs szó szerinti egyezés”) és a próza ellentéte |
| 8 | K52 | igazolt | vitatott | ✓ új | a „megáll” alanyát a vers nem nevezi meg, a mondat eldönti |
| 10 | K25 | igazolt | igazolt | ✗ | *Mit?* — az 1Móz 4:26 Targumában a celá szava áll, a mondat iránya fordított; a K-tétel alatt a lap más mondata ezt kimondta („a Targum a mondatot megfordítja”), az ügynök a szót számolta |
| 12 | K13, K15 | igazolt | hamis, igazolt | ✓ új | a BDB 2.c a kizárt Jer 10:25-öt és Zsolt 79:6-ot is ide sorolja (a szótári besorolás sorából) |
| 13 | K22 | hamis | hamis | ✓ | |
| 15 | K4 | vitatott | vitatott | ✓ | |
| 16 | K5 | hamis | vitatott | részben | más okból (a 34:5 alanya); a pátriárkák csoportját nem |
| 17 | K7 | igazolt | igazolt | ✗ | *Ki?* — a tükörfordítás („I have called you by your name”) a K-tétel alatt állt; az ügynök a ragos alakot nézte, azt nem, kinek a neve |

**Új az új kinyeréssel:** 1, 2, 8, 12. **Továbbra sem:** 10, 17 (mindkettőnél az adat a K-tétel alatt állt). A 80% egy tételen múlik.

**A 10-es halmazon kívül:** a bíráló-típusú tételek közül a 3. (K58), 4. (K55), 6. (K56), 9. (K57) változatlanul F2-ítéletként megvan; a régi átnézés 9 HIBÁ-jából az F2 hatot jelöl (K5, K11, K17, K21, K22, K29); a K23-at, a K26-ot és a K54-et igazolja (a 7. szakaszban a K26 és a K54 vitatott volt).

### 8.2 Többlet-jelzések és hamis riasztás

- **A lektori listán kívüli sokaság** 3 tétel (K12, K14, K19), a 12-es minta nem állítható elő; mind a három minősítve: K12 valódi (a Károli mindkét helyen „kiált”, a „kihirdetés” nem a fordítás szava), K19 valódi (`adat/thayer_vers_jelentes.tsv`: a G1941 7. pontja alatt a kizárt Róm 10:12 és 2Tim 2:22 is áll, a mondat a kizártak közül csak az ApCsel 9:14-et és 9:21-et nevezi), K14 nem dönthető el (a BDB 3.b az Ézs 44:5-öt „compare … but read” jelöléssel hozza; hogy a felsorolás hiánya hiba-e, a szócikk jelölése nem dönti el). Hamis riasztás: 0/2.
- **Új mellékhatás — egy hiba több tételen:** az 1Kir 18:25 funkció-mezője (a lektor 1. tétele) az F224.15 szerint minden olyan K-tétel alatt áll, amely a verset idézi, és a szerepfájl szerint a K-tétel része. Az ügynök ezért hat tételt (K2, K10, K40, K50, részben K13, K17) ítélt „hamis”-nak ugyanazon egy adatsor-hiba miatt; a K2, K10, K40 mondata maga helyes. Ezt a mintába nem soroltam (az ok a lektori 1. tétel), de a lektor terhét növeli: ha ezeket hamis riasztásnak számítjuk, 3/5. **Javaslat (a felhasználó dönt):** a funkció-mező csak a hely saját adatsor-tételénél (`adat:kapcsolodas`) legyen a K-tétel része, a többi tétel alatt tájékoztató; ez egy feltétel a `kontextus()`-ban és egy mondat a szerepfájlban.

### 8.3 Költség és keret

F2 ISTENTISZT, Opus, 75 K-tétel: 342 780 token, 59 eszközhívás, 926 s (a 7. szakaszé 58 K-tétellel 258 054 token). A lista mérete 107 → 192 KB. Keret: előtte heti 29%.

### 8.4 Mit mutat (a következő lépésről a felhasználó dönt)

1. **A kinyerés a hiány nagyobb része volt:** ugyanaz a modell (Opus) ugyanazon a halmazon 30% helyett 70%-ot ér el, mert a hibát hordozó adat (funkció-mező, szabály-mondat, Remez-mondat, szótári besorolás, alany) most a K-tétel alatt áll. A korlát: a mérés nem független (l. fent).
2. **A maradék két tétel a mérlegelésé:** az adat mindkettőnél a K-tétel alatt volt (a lap Targum-mondata; a tükörfordítás), az ügynök mégsem kötötte össze. Ez már nem kinyerési hézag.
3. **A hamis riasztás** a lektori listán kívül most kicsi (0/2), de a sokaság is kicsi (3); az új mellékhatás (egy adatsor-hiba hat tételen) a lektor terhét növeli — a 8.2 javaslata.

### 8.5 Kiegészítés: N207 és a küszöb (a felhasználó döntése, 2026-11-15: „igen”)

**N207 (F224.18):** a funkció-mező csak a hely saját adatsor-tételénél (`adat:kapcsolodas`) áll a K-tétel alatt, a többi K-tétel alól kikerül (`eszkozok/proza_allitas.py` `kontextus()`, teszt: `F224_15.test_funkcio_csak_a_sajat_tetelnel`; a szerepfájl Funkció-mező pontja). Új teljes mérés nem futott (a döntés szerint); célzott ellenőrzés a 8.2 hat érintett tételén, az újragenerált listán (ugyanaz a bemenet, 75 K-tétel, a K-halmaz azonos; a funkció-sorok száma a listán 103 → 20):

| K | 8. sz. ítélet | Az ítélet oka (az ügynök szerint) | Az 1Kir 18:25 funkció-mezője alatta | Ami marad |
|---|---|---|---|---|
| K2 | hamis | csak a funkció-mező | kikerül | nincs más ok (a mondat a versekkel egyezik) |
| K10 | hamis | csak a funkció-mező | kikerül | nincs más ok |
| K40 | hamis | csak a funkció-mező | kikerül | nincs más ok |
| K13 | hamis | a BDB 2.c a kizárt helyeket is hozza + a funkció-mező | kikerül | a BDB-ok (a lektor 12. tétele) |
| K17 | hamis | a BDB „1Kin 18:24-25, 26” három vers + a funkció-mező | kikerül | a háromvers-ok (a régi átnézés HIBÁ-ja) |
| K50 | hamis | a funkció-mező (a hely saját tétele) | **marad** | a lektor 1. tétele itt és a K61-ben (Remez) |

Következmény a 8. szakasz mérőire (számolás, nem új futás): az ISTENTISZT 10-es halmaza változatlanul 7/10 (az 1. tételt a K50 és a K61 hordozza); az egy adatsor-hiba miatti ismételt „hamis” ítélet 6 tételről 1-re csökken (a K13 és a K17 saját okkal marad); a hamis riasztás a lektori listán kívül 0/2, a 8.2-ben jelzett 3/5-ös számolás alapja (K2, K10, K40) megszűnik. *Hogy az ügynök a K2, K10, K40 tételt a funkció-mező nélkül valóban „igazolt”-nak ítélné, futás nélkül nem igazolt; az ügynök saját indoka szerint más oka nem volt.*

**A küszöb és a független mérés (DT881 🟢):** a küszöb marad 80%; a független mérés a következő új motívum cikkírásának F2-lépésén fut, ugyanazokkal a mérőkkel. A 8. szakasz 70%-a addig nem független eredmény.

### 7.7 Kiegészítés: a HAMART-halmaz nevezője (a független ellenőrzés, 2026-11-16)

A 15/18 = 83% a brief 18 tételes halmazán áll (`F224_CIKKIRAS_UJ_MENET_BRIEF.md` F224.13: „a lektor 18 kézi listás tétele”). A lektor 40. tétele (K66, a Jel 22:3 a hat újszövetségi hely között) a 2026-11-15-i mérésben K-tétel nélküli volt, ezért a 18-ba nem került; az új kinyeréssel K-tétel, az Opus „igazolt”-nak ítélte (✗, a mérőtábla S031 sora: F3). **A 40. tétellel együtt 15/19 = 78,9%, a küszöb alatt.** A 7.6 pont 1. állítása („a HAMART-hiány nagyrészt a modellé volt”) ettől nem változik, a „✓” a brief halmazára szól.
