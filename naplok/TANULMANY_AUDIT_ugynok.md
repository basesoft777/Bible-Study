# Tanulmány-audit — ügynöki ellenőrzőlista (F37 T5)

*2026.10.07 · `claude/tanulmany-ellenorzes` · egyszeri audit a 23 meglévő tanulmányon (`genezis/` 20, `ujszovetseg/` 3), a `.claude/agents/fuggetlen-ellenor.md` „Tanulmány-ellenőrzés (F37 T4)” szakaszának 1–6. pontja szerint. Javítás nem történt (DT-F37-5); a javításról a T6 utófeladat-javaslata szól.*

*Készítette: a végrehajtó (`vegrehajto-opus`) menet, nem a független ellenőr. Ez a jelentés a brief T5 lépésének terméke, nem a menet ellenőrzése.*

**Proveniencia.**
- 1–3. és 6. pont (gépi rész): `python eszkozok/ellenorzes/tanulmany_ellenorzes.py --mind` — `scope=23 tanulmány | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv+TBESH.txt+TBESG.txt+Karoli_1908.tsv+motivumlog/PaRDeS_motivumok.md | ts=2026-10-07` (a teljes kimenet a B függelékben).
- Szúrópróba `lekerdez.py`-jal (minden ELTÉRÉS-re): `scan H5375 --szakasz "1Móz 14"` → n=0; `scan H7311 --szakasz "1Móz 14:22"` → n=1; `scan H1892 --szakasz "1Móz 4"` → n=0; `scan H1893 --szakasz "1Móz 4:2"` → n=1; `scan H5315 --szakasz "1Móz 6"` → n=0; `scan H0853 --szakasz "1Móz 1:1"` → n=1; `karoli "Jób 39:3"` → a holló-vers (= héber/angol Jób 38:41). Mind `scope=range:… | forras=TAHOT_kivonat.tsv | ts=2026-10-07T08:1xZ`.
- 4–5. pont: `manual` — a 3. szakasz (Peshat/Remez/Drash/Sod, ⚠️) teljes szövegének olvasata, tanulmányonként. Ítélet, nem lekérdezés.

## Összesítő

Jelek: **OK** · **RÉSZBEN** (a pont nagyobb része teljesül, egy eleme nem) · **ELTÉRÉS** · **NE** = nem ellenőrizhető. A 2. pontban a „KÉZI” a gép által el nem dönthető sor (ragozott alak, összetett kifejezés, eltérő átírási konvenció); ezeket szúrópróbával néztem, hangalak-hibát nem találtam.

| Tanulmány | 1. Strong a versben | 2. szótári alak / kiejtés | 3. igehelyek | 4. Sod | 5. ⚠️ képviselő | 6. motívumnapló (7 szakaszból említi) |
|---|---|---|---|---|---|---|
| `1Moz_1v1` | **ELTÉRÉS** 1 (5 OK) | OK 2, KÉZI 4 | OK (30) | RÉSZBEN | **ELTÉRÉS** | 3/7 |
| `1Moz_1v2-2v3` | OK 22 | OK 5, KÉZI 13 | OK (87) | OK | OK | 5/7, **ELTÉRÉS** (elavult jegyzet) |
| `1Moz_2v4-7` | OK 9 | OK 3, KÉZI 4 | OK (28) | RÉSZBEN | OK | 3/7 |
| `1Moz_2v8-25` | OK 19 | OK 8, KÉZI 6 | OK (18) | RÉSZBEN | OK | 6/7 |
| `1Moz_3v1-6` | OK 11 | OK 3, KÉZI 5 | OK (32) | OK | OK | 5/7 |
| `1Moz_3v7-24` | OK 19 | OK 7, KÉZI 12 | OK (49) | OK | OK | 6/7 |
| `1Moz_4v1-24` | **ELTÉRÉS** 1 (12 OK) | OK 8, KÉZI 4 | OK (24) | OK | RÉSZBEN | 6/7 |
| `1Moz_4v25-5v32` | OK 8 | OK 3, KÉZI 4 | OK (31) | OK | RÉSZBEN | 4/7 |
| `1Moz_6v1-8` | OK 13 | OK 8, KÉZI 3 | OK (15) | OK | RÉSZBEN | 7/7 |
| `1Moz_6v9-22` | **ELTÉRÉS** 1 (10 OK) | OK 7, KÉZI 3 | OK (13) | OK | OK | 6/7 |
| `1Moz_7v1-24` | OK 10 | OK 3, KÉZI 3 | OK (23) | OK | OK | 3/7 |
| `1Moz_8v1-22` | OK 10 | OK 4, KÉZI 3 | OK (15) | OK | OK | 5/7 |
| `1Moz_9v1-17` | OK 7 | OK 7 | OK (9) | RÉSZBEN | RÉSZBEN | 4/7 |
| `1Moz_9v18-29` | OK 8 | OK 1, KÉZI 5 | OK (11) | RÉSZBEN | OK | 6/7 |
| `1Moz_10v1-11v32` | OK 10 | OK 5, KÉZI 4 | RÉSZBEN (32; 1 verzifikáció) | OK | **ELTÉRÉS** | 7/7 |
| `1Moz_12v1-20` | OK 13 | OK 4, KÉZI 6 | OK (22) | OK | OK | 5/7 |
| `1Moz_13v1-18` | OK 14 | OK 1, KÉZI 6 | OK (10) | OK | **ELTÉRÉS** | 5/7 |
| `1Moz_14` | **ELTÉRÉS** 1 (9 OK) | OK 2, KÉZI 5 | OK (15) | RÉSZBEN | OK | 4/7 |
| `1Moz_15` | OK 11 | OK 9, KÉZI 2 | OK (18) | RÉSZBEN | OK | 6/7 |
| `1Moz_16` | OK 9 | OK 4, KÉZI 3 | OK (10) | RÉSZBEN | OK | 4/7, **ELTÉRÉS** (elavult jegyzet) |
| `1Thessz_5v23` | OK 8 | OK 5, KÉZI 3 | OK (10) | OK | OK | 3/7 |
| `Rom_8v10` | OK 7 | OK 4, KÉZI 3 | OK (12) | OK | OK | 3/7 |
| `Zsid_4v12` | OK 9 | OK 4, KÉZI 4 | OK (14) | RÉSZBEN | OK | 3/7 |
| **7. pont** (magyar szó ↔ Strong) | kihagyva: #22 | | | | | |

A 6. oszlop azt méri, hány szakasz hivatkozik a tanulmány igeszakaszára (fájlnév vagy a szakaszba eső vers, `1Móz`/`1Mózes`, `Róm`/`Róma` alakban). A „Feldolgozott igeszakaszok” szakasz mind a 23-at említi. A többi szakasznál a hiány nem bizonyít elmaradt frissítést (a motívum lehet, hogy nem ehhez a szakaszhoz kötődik, és a blokkok egy része generált, `general.py --cel naplo#…`); az „összhangban van-e” kérdés gépileg **NE**, kivéve a két talált ellentmondást (6. pont lent).

## ELTÉRÉS-ek, súlyossági sorrendben

### 1. pont — a Strong-szám nincs a versben (4)

| Tanulmány:sor | Tanulmány állítása | A Strong-jelölt szöveg (TAHOT) | Parancs |
|---|---|---|---|
| `genezis/1Moz_14_bovitett.md:62` | 14:22 נָשָׂאתִי יָדִי, H5375 (+H3027) | a versben H7311 (הֲרִמֹתִי, „felemeltem”) áll, H5375 nincs | `scan H5375 --szakasz "1Móz 14"` n=0; `scan H7311 --szakasz "1Móz 14:22"` n=1 |
| `genezis/1Moz_4v1-24_bovitett.md:57` | 4:2 הֶבֶל, H1892 („pára, lehelet”) | a versben a személynév H1893 (Ábel) áll | `scan H1892 --szakasz "1Móz 4"` n=0; `scan H1893 --szakasz "1Móz 4:2"` n=1 |
| `genezis/1Moz_6v9-22_bovitett.md:51` | 6:17 נֶפֶשׁ חַיָּה, H5315+H2416 | H5315 a teljes 1Móz 6-ban nincs (a 6:17 *rúach chajjim*) | `scan H5315 --szakasz "1Móz 6"` n=0 |
| `genezis/1Moz_1v1_bovitett.md:57` | 1:1 אֵת „(nincs önálló Strong-szám)” | a TAHOT H0853-mal jelöli (2 szó-előfordulás a versben) | `scan H0853 --szakasz "1Móz 1:1"` n=1 |

### 5. pont — ⚠️ megnevezett képviselő nélkül vagy csonka hivatkozással

| Tanulmány:sor | Lelet | Jel |
|---|---|---|
| `genezis/1Moz_10v1-11v32_bovitett.md:127` | 4. ⚠️ („hetven nép” száma): egyik oldalon sincs megnevezett képviselő | ELTÉRÉS |
| `genezis/1Moz_13v1-18_bovitett.md:109` | „mint a föld pora” ⚠️: „egyes kommentátorok (pl. a fent idézett református igehirdetői hagyomány)” ↔ „mások (pl. az újszövetségi olvasat)” — a szöveg „nevesíthető” vitának mondja, de név nincs | ELTÉRÉS |
| `genezis/1Moz_1v1_bovitett.md:32` és `:177` | az Alapkérdések „lásd lent a ⚠️ jelzésnél” a szerzőség-vitára, a 177. sor a „fő tanulmány saját ⚠️ vitatott pontjára (Elohim többes alakja)” mutat — egyik ⚠️ pont sincs a tanulmányban (a 3. szakaszban csak a nyelvtani szerkezet és a *creatio ex nihilo* ⚠️ áll) | ELTÉRÉS (csonka hivatkozás) |
| `genezis/1Moz_10v1-11v32_bovitett.md:126` | 3. ⚠️ (nyelvzavar): az egyik oldal csak „hagyományos/fiatal-föld nézet”, a másik Walton | RÉSZBEN |
| `genezis/1Moz_4v1-24_bovitett.md:108` | Nód: Westermann ↔ „mások” | RÉSZBEN |
| `genezis/1Moz_4v25-5v32_bovitett.md:120` | Énokh 365 éve: „néhány értelmező (főként népszerű…)” ↔ Westermann, Hamilton | RÉSZBEN |
| `genezis/1Moz_6v1-8_bovitett.md:129` és `:131` | יָדוֹן: csak fordítások (Károli ↔ „több modern fordítás”); 120 év: Cassuto, Waltke ↔ „néhány korábbi kommentár” | RÉSZBEN |
| `genezis/1Moz_9v1-17_bovitett.md:124` | *kesét*: Wenham, Westermann ↔ „több konzervatívabb nyelvészeti elemzés” | RÉSZBEN |

Szövegkritikai és adatminőségi ⚠️ (vershez rendelés „TÖBBSZÖRÖS ELŐFORDULÁS, PONTOSÍTANDÓ”, Strong-javítás, forráskritikai megjegyzés a tanítói alkalmazásnál) nem vita, ezeket nem számoltam ELTÉRÉS-nek (legalább 6 tanulmányban fordulnak elő).

### 4. pont — a Sod nem vezethető le teljesen a P/R/D rétegekből (RÉSZBEN, 9)

| Tanulmány:sor | Ami csak a Sod-ban áll |
|---|---|
| `genezis/1Moz_1v1_bovitett.md:94` | az idő teremtése (sem a merizmus, sem a Drash nem említi az időt) |
| `genezis/1Moz_2v4-7_bovitett.md:82` | a LXX *pszükhén zószan* → 1Kor 15:45 kontraszt (a 2. pont ⚠️ jegyzetében van, a P/R/D-ben nincs) |
| `genezis/1Moz_2v8-25_bovitett.md:152` | Ef 5:31-32 (Krisztus–egyház) — az apostoli idézet a P/R/D-ben nem szerepel |
| `genezis/1Moz_9v1-17_bovitett.md:120` | a „felfüggesztett hadi íj” a Remez olvasatára épül, amely maga a ⚠️ 1. vitatott pont egyik oldala; a Sod ezt nem jelzi feltételesként |
| `genezis/1Moz_9v18-29_bovitett.md:100` | „sok értelmező szerint” (forrás nélkül) + Ef 2:13 |
| `genezis/1Moz_14_bovitett.md:92` | az utolsó vacsora-tipológia (a Sod maga feltételesnek jelöli: „Ha Melkizedek … Krisztus-előkép”) |
| `genezis/1Moz_15_bovitett.md:93` | a golgotai sötétség (Mt 27:45) párhuzama |
| `genezis/1Moz_16_bovitett.md:104` | Mózes, Illés és Krisztus pusztai találkozása (a Remez más mintázatokat sorol) |
| `ujszovetseg/Zsid_4v12_bovitett.md:71` | a *logosz* megtestesülése és a „főpapi Krisztus-téma” (a P/R/D-ben nincs) |

### 3. pont — igehely a Károli-számozásban

- `genezis/1Moz_10v1-11v32_bovitett.md:121`: `Jób 38:41` — a Károli 1908-ban nincs (a Jób 38 ott 38 versű); a holló-vers a Károliban `Jób 39:3` (`lekerdez.py karoli "Jób 39:3"`). Verzifikációs eltérés, nem téves hivatkozás; a tanulmány itt héber/angol számozást használ.

### 6. pont — a motívumnaplóval ellentétes jegyzet (2)

- `genezis/1Moz_1v2-2v3_bovitett.md:272`: „ez a lelet [תֹהוּ וָבֹהוּ, 3 előfordulás] motívumnapló-jelölt (⭐ küszöb) — a `PaRDeS_motivumok.md`-be még nem került be”. A napló ⭐ szakasza ma már tartalmazza (`TEREMT-002`, 3 fő előfordulás, feldolgozás alatt). A tanulmány jegyzete elavult.
- `genezis/1Moz_16_bovitett.md:198-203`: „Motívumnaplózásra váró elemek (jóváhagyásra vár)” — a felsorolt málach JHVH, Él Rói, *inná* a napló „Kulcsszavak részletesen” szakaszában már szerepel. A jegyzet elavult.

## ⛔-jelöltek

**⭐-küszöb:** nincs ⛔. Minden ⭐-átlépés, amelyet a tanulmányok állítanak (segítségül hívás, oltárépítés, bűn következményeinek gyűrűzése, uralom-megbízás, Isten képmása, brít, por/formáltatás, tohu va-vohu), szerepel a motívumnapló ⭐ szakaszában (a generált blokkban vagy a kézi küszöb-bekezdések között).

**Valódi ⚠️-vita** (a T4 meghatározása szerint: a megnevezett képviselők állításai a tanulmány következtetését is eldönthetik, vagy a tanulmány forrás nélkül zárja le a vitát). Az alábbiakban a tanulmány a vita egyik oldalára építi a saját következtetését. Mindegyik lezárt, régi tanulmány; hogy most ⛔-nek számítanak-e, vagy a javító utófeladatba kerülnek, az a felhasználó döntése (`DONTESEK.md` DT61):

| Tanulmány:sor | Vita | Mire épít a tanulmány |
|---|---|---|
| `genezis/1Moz_9v1-17_bovitett.md:112, 120` | *kesét* = hadi íj (Wenham, Westermann) ↔ „konzervatívabb nyelvészeti elemzés” | a Remez és a Sod a „hadi íj” oldalra épül, feltételesség jelzése nélkül |
| `genezis/1Moz_15_bovitett.md:98` | 15:6 imputáció: Calvin ↔ N. T. Wright | „a projekt pünkösdi/karizmatikus munkahipotézise a hagyományos … olvasatot követi” — projekt-álláspont, nem forrás |
| `genezis/1Moz_1v1_bovitett.md:91` | *creatio ex nihilo*: Levenson ↔ Órigenész | a tanulmány saját lexikai érve („erősebb érv a hagyományos oldal mellett”, „eddig egyik tekintély … nem kötötte össze”) dönt |
| `genezis/1Moz_1v2-2v3_bovitett.md:230` | Isten képmása: Augustinus ↔ Barth ↔ Middleton | a tanulmány saját lexikai adata Middleton mellett dönt („Lexikai megerősítés … ÚJ”) |
| `genezis/1Moz_14_bovitett.md:92, 96` | Melkizedek: Prince ↔ Wenham, Mathews, Hamilton | a Sod a krisztus-előkép olvasatra épül, de feltételesként jelölve („Ha …”) — jelölt, nem biztos |

## További megfigyelések (nem az 1–6. pont tárgya)

- `genezis/1Moz_4v1-24_bovitett.md:102`: angol szó a Sod-ban („a kegyelem *later* kibontakozó…”). Az E9 csak a „sense” szót nézi.
- A gépi tanulmány-szabályok (CI jelentés mód) eredménye külön: `naplok/TANULMANY_AUDIT.md` (E13 206, E8 32, E12 195 találat; E20, E9, E2, E15 nulla).

---

## B függelék — a `tanulmany_ellenorzes.py --mind` teljes kimenete

### `genezis/1Moz_10v1-11v32_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 10:1 – 11:32

- **1. Strong a versben:** OK 10
- **2. szótári alak / kiejtés:** KÉZI 4, OK 5
- **3. igehelyek:** 32 teljes alakú hivatkozás, nem létező: 1
- **6. motívumnapló:** Tematikus áttekintés: említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 5 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 60 | תּוֹלְדֹת | H8435 | תּוֹלֵדוֹת | to.le.dah | toledot | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.71 |
| 61 | גִּבֹּר | H1368 | גִּבּוֹר | gib.bor | gibbor | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 1.00 |
| 64 | שָׂפָה אֶחָת | H8193+H0259 | — | — | safá echát | KÉZI | összetett kifejezés vagy nincs Strong |
| 67 | נָבְלָה | H1101 | בָּלַל | ba.lal | návelá* (→Bábel népetim.) | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.35 |

Nincs a Károli 1908 számozásában (nem létező igehely vagy verzifikációs eltérés, l. `konkordancia/Karoli_versmegfeleltetes.tsv`): 121. sor `Jób 38:41`

### `genezis/1Moz_12v1-20_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 12:1 – 12:20

- **1. Strong a versben:** OK 13
- **2. szótári alak / kiejtés:** KÉZI 6, OK 4
- **3. igehelyek:** 22 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 8 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 69 | לֶךְ־לְךָ֛ | H1980 | הָלַךְ | ha.lakh | lech-lechá | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.27 |
| 72 | גּוֹי גָּדוֹל | H1471+H1419 | — | — | gój gádól | KÉZI | összetett kifejezés vagy nincs Strong |
| 73 | אֲגַדְּלָה | H1431 | גָּדַל | ga.dal | agaddelá | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.62 |
| 74 | נִבְרְכוּ | H1288 | בָּרַךְ | ba.rakh | nivrechú | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.29 |
| 76 | קָרָא בְשֵׁם יְהוָה | H7121+H8034 | — | — | kará b'shém Adonáj | KÉZI | összetett kifejezés vagy nincs Strong |
| 78 | נְגָעִים גְּדֹלִים | H5061+H1419 | — | — | nega'ím gedolím | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_13v1-18_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 13:1 – 13:18

- **1. Strong a versben:** OK 14
- **2. szótári alak / kiejtés:** KÉZI 6, OK 1
- **3. igehelyek:** 10 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 2 sor, ⭐ 4 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 55 | קָרָא בְשֵׁם יְהוָה | H7121+H3068 | — | — | kará ve-shém Adonáj | KÉZI | összetett kifejezés vagy nincs Strong |
| 56 | וַיִּשָּׂא־ל֣וֹט אֶת־עֵינָ֗יו… | H5375+H5869+H7200 | — | — | vajissá Lot et-énáv vajj… | KÉZI | összetett kifejezés vagy nincs Strong |
| 58 | רָעִ֛ים וְחַטָּאִ֖ים | H7451+H2400 | — | — | ra'ím ve-chattá'ím | KÉZI | összetett kifejezés vagy nincs Strong |
| 59 | שָׂא נָ֣א עֵינֶ֗יךָ | H5375+H5869 | — | — | sá ná énéchá | KÉZI | összetett kifejezés vagy nincs Strong |
| 60 | כַּעֲפַ֣ר הָאָ֑רֶץ | H6083+H0776 | — | — | ka-afar ha-árec | KÉZI | összetett kifejezés vagy nincs Strong |
| 61 | וַיִּֽבֶן־שָׁ֥ם מִזְבֵּ֖חַ | H1129+H4196 | — | — | vajjíven shám mizbéach | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_14_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 14:1 – 14:vége

- **1. Strong a versben:** ELTÉRÉS 1, OK 9
- **2. szótári alak / kiejtés:** KÉZI 5, OK 2
- **3. igehelyek:** 15 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: nem említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 4 sor, ⭐ 0 sor

| sor | szó | Strong | hatókör | 1. pont | indok |
|---|---|---|---|---|---|
| 62 | נָשָׂאתִי יָדִי | H5375 | vers: 1Móz 14:22 | ELTÉRÉS | a Strong-szám nincs a vers(ek)ben |

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 56 | חֲנִיכָיו | H2593 | חָנִיךְ | cha.nikh | chanikáv | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.80 |
| 58 | לֶחֶם וָיַיִן | H3899+H3196 | — | — | lechem vö-jájin | KÉZI | összetett kifejezés vagy nincs Strong |
| 59 | אֵל עֶלְיוֹן | H0410+H5945 | — | — | Él Eljón | KÉZI | összetett kifejezés vagy nincs Strong |
| 60 | קֹנֵה שָׁמַיִם וָאָרֶץ | H7069 | קָנָה | qa.nah | konéh sámájim vá-árec | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.17 |
| 62 | נָשָׂאתִי יָדִי | H5375+H3027 | — | — | násáti jádí | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_15_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 15:1 – 15:vége

- **1. Strong a versben:** OK 11
- **2. szótári alak / kiejtés:** KÉZI 2, OK 9
- **3. igehelyek:** 18 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 2 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 48 | אָמַן (hiph.) | H0539 | אָמַן | a.man | he'emín | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.40 |
| 54 | עָנָה (pi.) | H6031 | עָנָה | a.nah | inná | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.50 |

### `genezis/1Moz_16_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 16:1 – 16:vége

- **1. Strong a versben:** OK 9
- **2. szótári alak / kiejtés:** KÉZI 3, OK 4
- **3. igehelyek:** 10 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: nem említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 2 sor, ⭐ 1 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 49 | עָנָה (Piél) | H6031 | עָנָה | a.nah | inná | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.50 |
| 50 | מַלְאַךְ יְהוָה | H4397+H3068 | — | — | málach JHVH | KÉZI | összetett kifejezés vagy nincs Strong |
| 52 | אֵל רֳאִי | H0410+H7210 | — | — | Él Rói | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_1v1_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 1:1 – 1:1

- **1. Strong a versben:** NEM ELLENŐRIZHETŐ 1, OK 5
- **2. szótári alak / kiejtés:** KÉZI 4, OK 2
- **3. igehelyek:** 30 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: nem említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: nem említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 10 sor, ⭐ 0 sor

| sor | szó | Strong | hatókör | 1. pont | indok |
|---|---|---|---|---|---|
| 57 | אֵת | — | vers: 1Móz 1:1 | NEM ELLENŐRIZHETŐ | nincs értelmezhető Strong-szám |

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 54 | בְּרֵאשִׁית | H7225 | רֵאשִׁית | re.shit | bereshít | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.86 |
| 57 | אֵת | — | — | — | ét | KÉZI | nincs Strong |
| 58 | הַשָּׁמַיִם | H8064 | שָׁמַיִם | sha.ma.yim | hasamájim | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.71 |
| 59 | הָאָרֶץ | H0776 | אֶ֫רֶץ | e.rets | haárec | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.36 |

### `genezis/1Moz_1v2-2v3_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 1:2 – 2:3

- **1. Strong a versben:** OK 22
- **2. szótári alak / kiejtés:** KÉZI 13, OK 5
- **3. igehelyek:** 87 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: említi; Kulcsszó-index: említi; Kulcsszavak részletesen: nem említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 8 sor, ⭐ 1 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 84 | תֹהוּ וָבֹהוּ | H8414+H0922 | — | — | tohú vavohú | KÉZI | összetett kifejezés vagy nincs Strong |
| 86 | רוּחַ אֱלֹהִים | H7307+H0430 | — | — | ruach elohím | KÉZI | összetett kifejezés vagy nincs Strong |
| 87 | מְרַחֶפֶת | H7363 | רָחַף | ra.chaph | merachefet | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.47 |
| 106 | וַיֹּאמֶר | H0559 | אָמַר | a.mar | vajjómer | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.50 |
| 107 | יְהִי | H1961 | הָיָה | ha.yah | jehí | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.22 |
| 123 | נַעֲשֶׂה | H6213 | עָשָׂה | a.sah | na'aszé | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.40 |
| 127 | זָכָר וּנְקֵבָה | H2145+H5347 | — | — | zachár u-nekévá | KÉZI | összetett kifejezés vagy nincs Strong |
| 168 | פְּרוּ וּרְבוּ | H6509+H7235 | — | — | perú u-revú | KÉZI | összetett kifejezés vagy nincs Strong |
| 169 | כִּבְשֻׁהָ | H3533 | כָּבַשׁ | ka.vash | kivsuha | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.62 |
| 170 | רְדוּ | H7287 | רָדָה | ra.dah | redú | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.44 |
| 183 | וַיִּשְׁבֹּת | H7673 | שָׁבַת | sha.vat | vajjisbot | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.40 |
| 184 | וַיְבָרֶךְ | H1288 | בָּרַךְ | ba.rakh | vajvárech | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.40 |
| 185 | וַיְקַדֵּשׁ | H6942 | קָדַשׁ | qa.dash | vajkaddés | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.40 |

### `genezis/1Moz_2v4-7_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 2:4 – 2:7

- **1. Strong a versben:** OK 9
- **2. szótári alak / kiejtés:** KÉZI 4, OK 3
- **3. igehelyek:** 28 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: nem említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: nem említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 3 sor, ⭐ 1 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 48 | יָצַר (וַיִּיצֶר) | H3335 | יָצַר | ya.tsar | jacar* (*vajjícer*) | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.32 |
| 51 | נָפַח (וַיִּפַּח) | H5301 | נָפַח | na.phach | nafach* (*vajjipach*) | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.45 |
| 52 | נִשְׁמַת חַיִּים | H5397+H2416 | — | — | nismat chajjim | KÉZI | összetett kifejezés vagy nincs Strong |
| 53 | נֶפֶשׁ חַיָּה | H5315+H2416 | — | — | nefes chajjá | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_2v8-25_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 2:8 – 2:25

- **1. Strong a versben:** OK 19
- **2. szótári alak / kiejtés:** KÉZI 6, OK 8
- **3. igehelyek:** 18 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 13 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 56 | עֵץ הַחַיִּים | H6086+H2416 | — | — | ec ha-chajjím | KÉZI | összetett kifejezés vagy nincs Strong |
| 57 | עֵץ הַדַּעַת טוֹב וָרָע | H6086+H1847 | — | — | ec ha-daat tóv vará | KÉZI | összetett kifejezés vagy nincs Strong |
| 84 | לֹא־טוֹב | H3808+H2896 | — | — | ló tóv | KÉZI | összetett kifejezés vagy nincs Strong |
| 85 | עֵזֶר כְּנֶגְדּוֹ | H5828+H5048 | — | — | ézer kenegdó | KÉZI | összetett kifejezés vagy nincs Strong |
| 116 | בָּשָׂר אֶחָד | H1320+H0259 | — | — | bászár echád | KÉZI | összetett kifejezés vagy nincs Strong |
| 117 | עֲרוּמִּים | H6174 | עָרוֹם | a.rom | arummím | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.55 |

### `genezis/1Moz_3v1-6_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 3:1 – 3:6

- **1. Strong a versben:** OK 11
- **2. szótári alak / kiejtés:** KÉZI 5, OK 3
- **3. igehelyek:** 32 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 6 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 43 | תִגְּעוּ | H5060 | נָגַע | na.ga | tiggeú | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.20 |
| 44 | פֶּן־תְּמֻתוּן | H6435+H4191 | — | — | pen-temutún | KÉZI | összetett kifejezés vagy nincs Strong |
| 45 | יֹדְעֵי טוֹב וָרָע | H3045+H2896+H7451 | — | — | jodeéj tov vára | KÉZI | összetett kifejezés vagy nincs Strong |
| 47 | נֶחְמָד | H2530 | חָמַד | cha.mad | nechmád | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.77 |
| 48 | וַתִּתֵּן | H5414 | נָתַן | na.tan | vattittén | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.43 |

### `genezis/1Moz_3v7-24_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 3:7 – 3:24

- **1. Strong a versben:** OK 19
- **2. szótári alak / kiejtés:** KÉZI 12, OK 7
- **3. igehelyek:** 49 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 8 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 49 | וַתִּפָּקַחְנָה | H6491 | פָּקַח | pa.qach | vattippakachnah | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.48 |
| 50 | עֵינֵי | H5869 | עַ֫יִן | a.yin | ejnei | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.22 |
| 51 | עֵרֻמִּם | H5903 | עֵירֹם | e.rom | erumím | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.60 |
| 52 | חֲגֹרֹת | H2290 | חֲגוֹר | cha.gor | chagorot | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.86 |
| 62 | אָרוּר | H0779 | אָרַר | a.rar | arur | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.75 |
| 65 | יְשׁוּפְךָ | H7779 | שׁוּף | shuph | jeshufcha | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.57 |
| 76 | עִצְּבוֹנֵךְ | H6093 | עִצָּבוֹן | its.tsa.von | itzevonekh | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.53 |
| 77 | תְּשׁוּקָתֵךְ | H8669 | תְּשׁוּקָה | te.shu.qah | teshuqatekh | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.84 |
| 78 | יִמְשָׁל | H4910 | מָשַׁל | ma.shal | jimshol | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.62 |
| 97 | כָּתְנוֹת | H3801 | כֻּתֹּ֫נֶת | ke.to.net | kotnot | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.46 |
| 106 | כְּרֻבִים | H3742 | כְּרוּב | ke.ruv | keruvim | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.83 |
| 108 | הַחֶרֶב | H2719 | חֶ֫רֶב | che.rev | hacherev | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.86 |

### `genezis/1Moz_4v1-24_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 4:1 – 4:24

- **1. Strong a versben:** ELTÉRÉS 1, OK 12
- **2. szótári alak / kiejtés:** KÉZI 4, OK 8
- **3. igehelyek:** 24 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 6 sor, ⭐ 0 sor

| sor | szó | Strong | hatókör | 1. pont | indok |
|---|---|---|---|---|---|
| 57 | הֶבֶל | H1892 | vers: 1Móz 4:2 | ELTÉRÉS | a Strong-szám nincs a vers(ek)ben |

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 56 | קָנִיתִי | H7069 | קָנָה | qa.nah | kaníti | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.36 |
| 61 | רֹבֵץ | H7257 | רָבַץ | ra.vats | rovéc | KÉZI | szótári alak egyezik, kiejtés eltér (0.36) |
| 64 | דְּמֵי | H1818 | דָּם | dam | demé | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.57 |
| 65 | נָע וָנָד | H5128+H5110 | — | — | ná vánád | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_4v25-5v32_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 4:25 – 5:32

- **1. Strong a versben:** OK 8
- **2. szótári alak / kiejtés:** KÉZI 4, OK 3
- **3. igehelyek:** 31 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: nem említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 6 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 62 | קָרָא בְשֵׁם | H7121 | קָרָא | qa.ra | qara b'shem | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.62 |
| 63 | תּוֹלְדֹת | H8435 | תּוֹלֵדוֹת | to.le.dah | toledot | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.71 |
| 66 | הִתְהַלֵּךְ | H1980 | הָלַךְ | ha.lakh | hithalek | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.57 |
| 68 | נֹחַ / יְנַחֲמֵנוּ | H5146+H5162 | — | — | Noach / yenachamenu | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_6v1-8_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 6:1 – 6:8

- **1. Strong a versben:** OK 13
- **2. szótári alak / kiejtés:** KÉZI 3, OK 8
- **3. igehelyek:** 15 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 9 sor, ⭐ 1 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 44 | בְּנֵי־הָאֱלֹהִים | H1121+H0430 | — | — | bené ha'Elohim | KÉZI | összetett kifejezés vagy nincs Strong |
| 45 | בְּנוֹת הָאָדָם | H1323+H0120 | — | — | benot ha'adam | KÉZI | összetett kifejezés vagy nincs Strong |
| 49 | גִּבֹּרִים | H1368 | גִּבּוֹר | gib.bor | gibborim | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.86 |

### `genezis/1Moz_6v9-22_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 6:9 – 6:22

- **1. Strong a versben:** ELTÉRÉS 1, OK 10
- **2. szótári alak / kiejtés:** KÉZI 3, OK 7
- **3. igehelyek:** 13 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 3 sor, ⭐ 2 sor

| sor | szó | Strong | hatókör | 1. pont | indok |
|---|---|---|---|---|---|
| 51 | נֶפֶשׁ חַיָּה | H5315 | vers: 1Móz 6:17 | ELTÉRÉS | a Strong-szám nincs a vers(ek)ben |

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 45 | הִתְהַלֵּךְ | H1980 | הָלַךְ | ha.lakh | hithalech | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.53 |
| 49 | עֲצֵי־גֹפֶר | H1613 | גֹּ֫פֶר | go.pher | atzé-gófer | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.53 |
| 51 | נֶפֶשׁ חַיָּה | H5315+H2416 | — | — | nefesh chajjá | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_7v1-24_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 7:1 – 7:24

- **1. Strong a versben:** OK 10
- **2. szótári alak / kiejtés:** KÉZI 3, OK 3
- **3. igehelyek:** 23 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: nem említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: nem említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 3 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 58 | אֲרֻבֹּת הַשָּׁמַיִם | H0699+H8064 | — | — | arubbot hasámájim | KÉZI | összetett kifejezés vagy nincs Strong |
| 60 | נִשְׁמַת רוּחַ חַיִּים | H5397+H7307+H2416 | — | — | nismat rúach chajjím | KÉZI | összetett kifejezés vagy nincs Strong |
| 61 | וַיִּשָּׁאֶר אַךְ | H7604+H0389 | — | — | vajjisáér ách | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_8v1-22_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 8:1 – 8:22

- **1. Strong a versben:** OK 10
- **2. szótári alak / kiejtés:** KÉZI 3, OK 4
- **3. igehelyek:** 15 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 6 sor, ⭐ 1 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 59 | עֲלֵה־זַיִת | H5929+H2132 | — | — | álé-zájit | KÉZI | összetett kifejezés vagy nincs Strong |
| 60 | פָּרוּ וְרָבוּ | H6509+H7235 | — | — | párú vörávú | KÉZI | összetett kifejezés vagy nincs Strong |
| 62 | רֵיחַ הַנִּיחֹחַ | H7381+H5207 | — | — | réach hannichóach | KÉZI | összetett kifejezés vagy nincs Strong |

### `genezis/1Moz_9v1-17_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 9:1 – 9:17

- **1. Strong a versben:** OK 7
- **2. szótári alak / kiejtés:** OK 7
- **3. igehelyek:** 9 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: nem említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 5 sor, ⭐ 1 sor

### `genezis/1Moz_9v18-29_bovitett.md`

Igeszakasz (fájlnévből): 1Móz 9:18 – 9:29

- **1. Strong a versben:** OK 8
- **2. szótári alak / kiejtés:** KÉZI 5, OK 1
- **3. igehelyek:** 11 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: említi; Kulcsszó-index: említi; Kulcsszavak részletesen: említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 7 sor, ⭐ 1 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 44 | אִישׁ הָאֲדָמָה | H0376+H0127 | — | — | is há'adámá | KÉZI | összetett kifejezés vagy nincs Strong |
| 45 | וַיִּתְגַּל | H1540 | הֶגְלָם | ga.lah | vajjitgál | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.43 |
| 47 | אָרוּר | H0779 | אָרַר | a.rar | árúr | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.75 |
| 48 | אֱלֹהֵי שֵׁם | H0430+H8035 | — | — | Elohé Shém | KÉZI | összetett kifejezés vagy nincs Strong |
| 49 | יַפְתְּ | H6601 | פָּתָה | pa.tah | jaft | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.44 |

### `ujszovetseg/1Thessz_5v23_bovitett.md`

Igeszakasz (fájlnévből): 1Thessz 5:23 – 5:23

- **1. Strong a versben:** OK 8
- **2. szótári alak / kiejtés:** KÉZI 3, OK 5
- **3. igehelyek:** 10 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: nem említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: nem említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 3 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 37 | ἁγιάσαι | G0037 | ἁγιάζω | hagiazō | hagiaszai | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.75 |
| 38 | ὁλοτελεῖς | G3651 | ὁλοτελής | holotelēs | holoteleisz | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.90 |
| 43 | τηρηθείη | G5083 | τηρέω | tēreō | téréthei | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.62 |

### `ujszovetseg/Rom_8v10_bovitett.md`

Igeszakasz (fájlnévből): Róm 8:10 – 8:10

- **1. Strong a versben:** OK 7
- **2. szótári alak / kiejtés:** KÉZI 3, OK 4
- **3. igehelyek:** 12 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: nem említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: nem említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 3 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 38 | νεκρὸν | G3498 | νεκρός | nekros | nekron | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.83 |
| 39 | ἁμαρτίαν | G0266 | ἁμαρτία | hamartia | hamartian | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.94 |
| 42 | δικαιοσύνην | G1343 | δικαιοσύνη | dikaiosunē | dikaioszünén | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.91 |

### `ujszovetseg/Zsid_4v12_bovitett.md`

Igeszakasz (fájlnévből): Zsid 4:12 – 4:12

- **1. Strong a versben:** OK 9
- **2. szótári alak / kiejtés:** KÉZI 4, OK 4
- **3. igehelyek:** 14 teljes alakú hivatkozás, nem létező: 0
- **6. motívumnapló:** Tematikus áttekintés: nem említi; Kulcsszó-index: említi; Kulcsszavak részletesen: nem említi; Könyv szerinti index: említi; ⭐ Emlékeztető küszöb: nem említi; Még nem feldolgozott: nem említi; Feldolgozott igeszakaszok: említi
- **4–5. kigyűjtve:** ⚠️ 3 sor, ⭐ 0 sor

| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |
|---|---|---|---|---|---|---|---|
| 37 | ζῶν | G2198 | ζάω | zaō | dzón | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.57 |
| 40 | μάχαιραν δίστομον | G3162+G1366 | — | — | makhairan disztomon | KÉZI | összetett kifejezés vagy nincs Strong |
| 41 | ψυχῆς | G5590 | ψυχή | psuchē | pszükhész | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.67 |
| 42 | πνεύματος | G4151 | πνεῦμα | pneuma | pneumatosz | KÉZI | nem szótári alak (ragozott?), kiejtés-hasonlóság 0.75 |

proveniencia: scope=23 tanulmány | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv+TBESH.txt+TBESG.txt+Karoli_1908.tsv+motivumlog/PaRDeS_motivumok.md | ts=2026-10-07T08:19Z
