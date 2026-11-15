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
