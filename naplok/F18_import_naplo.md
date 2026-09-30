# F18 — Nave-import napló (DT5, 1. opció: basokant/nave, saját parszoló)

*Ág: `claude/nave-import` · 2026.09.30 · kimenet: `konkordancia/Nave_basokant.tsv` (+ `Nave_basokant_README.md`) · eszköz: `eszkozok/nave_import.py` · állapot: **javaslat***

## 1. Mi készült

| | |
|---|---|
| Forrás | `basokant/nave` @ `4f35c7d4ffd4933f4db1b9d5182db90dc04bd235` (a helyi klón HEAD-je egyezik), `data/nave.txt`, 4 537 041 karakter, sha256 `560dcb1a…052f43a` |
| Licenc | közkincs a README szerint (Nave, 1897); licencfájl nincs (`F18_licenc.md`) |
| Parszoló | saját (`eszkozok/nave_import.py`); a basokant szkriptjei és a `parsed-nave.json` nincs átvéve (a JSON csak ellenőrző összevetésre szolgált) |
| Kimenet | *(F18.12 után: 85 246 adatsor, l. 2.8)* 85 116 adatsor (+ fejléc és 5 kommentsor), 5 322 `tema_id` *(első változat: 85 066; az egyfejezetes-javítás +50 sort adott, l. 2.4)* |
| Soronként | 77 985 `vers` (64 150 egyes vers, 11 615 tartomány, 2 207 fejezet, 13 `ismeretlen_konyv`) · 4 368 `lasd` · 2 763 `szoveg` (hivatkozás nélküli egység) *(régi: 77 935 · 64 138 · 11 577)* |
| Témák | 5 322 entry, 5 320 egyedi cím (`REVERENCE`, `SIN` kétszer) |
| Károli-állapot (egyes versek, 64 150) | `azonos` 41 327 · `eltero` 270 · `a_tablaban_nincs_kjv_megfelelo` 145 · `nincs_a_tablaban` 582 · `ujszovetseg_nincs_tabla` 21 826 (a `Karoli_versmegfeleltetes.tsv` ÓSZ-i) *(régi: 41 330 · 270 · — · 727 · 21 811; a 727 = 582 + 145)* |
| Gyanús sorok | **52 `gyanus_kijelzes`-sor, 54 jelölés-előfordulás** (F18.7 után; a 2 Abd 1:1-sor kétszer jelölt): 49 összeolvadt-töredékes (ebből 13 `ismeretlen_konyv`: 12 × `PrAzar.1.2`, 1 × `Wis.2`), 2 egyfejezetes versszám nélküli, 1 „Jeremiah 2” (valószínűleg helyes hivatkozás, csak a kijelzés szokatlan). *(F18.6 után: 24 jelölés = 20 + 4; az első változat: 20 — a 6 betűs névvel összeolvadt hibák jelöletlenek voltak, l. 2.6)*. A jelölt sorok `karoli_allapot`-a `nem_ertekelt` |

Mellékhatás: a meglévő `adat/` és `konkordancia/` fájlokból egy sor sem változott, nem csökkent, **kivéve az `adat/szotar_szerepek.tsv` +2 sorát** (a két 12. sorrendű Nave-szerepsor, l. DT18 (j)); a munkafa az import során ezen kívül három új fájlt, a napló- és licencfájlt, valamint a brief-fejlécet érintette.

Nem committolt: a nyers `nave.txt` (4,5 MB); reprodukálás a commit-hash + sha256 alapján (`--forras`). *Javaslat:* maradjon így (a sha256 a letöltött fájl ellenőrzésére szolgál; a commit-hash a GitHubon rögzített, de a repó eltűnése esetén a fájl nem állítható vissza) — az összesítő tételben.

**Eltérés a briefhez:** a brief `ir` listája `konkordancia/Nave_theonize.tsv`-t nevez. A fájl a DT5 miatt `konkordancia/Nave_basokant.tsv` (a „theonize” név félrevezető lenne). Javaslat; az összesítő tételben.

## 2. Eredet- és pontosság-ellenőrzés

**2.1. A parszoló hivatkozás-darabszáma a nyers szöveghez képest (szkript; `scope=nave.txt teljes | forras=eszkozok/nave_import.py | ts=2026-09-30`).** A nyers fájlban 5 322 `$$$`-entry, 82 303 `<ref>` (77 935 `osisRef` + 4 368 `target`); a kimenetben 5 322 `tema_id`, 4 368 `lasd`-sor és 77 985 `vers`-sor (77 935 + 50: az egyfejezetes könyvek `:9,10`-szerű vesszős listái versenként külön sor). **Ez darabszám-egyezés** (nem veszett el és nem duplázódott hivatkozás), **nem helyesség**: az első változatban is „100%” volt, mégis 250 egyfejezetes hivatkozás hibás versszámmal szerepelt (l. 2.4). (A `tag`-szerkezet ellenőrzve: csak `entryFree, def, list, item, ref`; `list` mélysége legfeljebb 1; az `</entryFree>` mindenütt megvan.)

**2.2. A basokant-JSON mint belső összevetés** (`scope=parsed-nave.json teljes, mennyiségi | forras=eszkozok/nave_import.py --json (commit 4f35c7d) | ts=2026-09-30`). A `parsed-nave.json` (5 322 elem) verses-szám összege 56 645, relatedTopics 2 469 — a nyers szöveg 77 935 / 4 368 hivatkozásával szemben. Témánként 4 368 téma egyezik a versszámban (82,1%), 954 témában a JSON-ban kevesebb van (soha több: 0). Tehát a basokant JSON-ja **veszteséges**, a nyers fájl teljes: ez megerősíti, hogy saját parszolót kellett írni, és a JSON nem használható importforrásnak. (Csak mennyiségi összevetés; a veszteség okát — pl. a `<list>` elemek kezelése — a basokant szkriptjeinek olvasása nélkül nem vizsgáltuk.)

**2.3. Független kiadással való szúrópróba.** A Project Gutenberg / CCEL / Internet Archive teljes szövege az elérhető eszközökkel (WebFetch, JS-renderelt vagy csonkolt oldalak) **nem volt lekérdezhető**; ezt mértem: 4 kísérlet sikertelen. Elérhető volt a `biblestudytools.com/concordances/naves-topical-bible/` témánkénti oldala (a közkincs Nave-szövegre épülő, a basokant-lekaparástól független megjelenítés; maga is másodkézből való, tehát ez **nem** elsődleges kiadás-összevetés).
`scope=12 téma | forras=biblestudytools.com/concordances/naves-topical-bible (másodkézi, nem elsődleges kiadás; lekérdezés a menetben, nincs rögzített proveniencia-sor → manual) | ts=2026-09-30`. 12 téma összevetése az igehely-halmazra: `AARON` (kb. 100 hivatkozás, soronként), `ABEL`, `ABBA`, `ABAGTHA`, `ABDA`, `ACHBOR` (szemrevételezve), `ACHAN`, `AGABUS`, `ABIATHAR`, `ABISHAI`, `ABIGAIL`, `ABED-NEGO` (szkripttel, a tartomány-alak normalizálása után): **12/12 egyezik** a verses-halmazban, a hivatkozások sorrendjében és az altéma-csoportosításban is, ahol megvizsgáltam. A minta kicsi, **nem véletlen** (kézzel választott, kis/közepes témák az ábécé elejéről) és a forrás **nem elsődleges kiadás** (másodkézi megjelenítés), ezért **nem** általánosítható az 5 322 témára.

**2.4. Független ellenőri lelet és javítás (F18.6).** A független ellenőr kimutatta, hogy az egyfejezetes könyvek (Abd, Filem, 2Ján, 3Ján, Júd) hivatkozásai mind `X 1:1`-re sikerültek: a forrás az `osisRef`-et `X.1.1`-re tölti, a valódi versszám a `<ref>` UTÁN áll (130 sorban `utotag::8-13` alakban, 120 sorban a következő hivatkozás `cimke` mezőjébe csúszva). A `cimke` 688 sorban kezdődött `:<szám>`-mal. **Javítás:** a parszoló a `<ref>` után közvetlenül álló `:szám[-szám][,szám…]` listát a hivatkozáshoz rendeli. Mért eredmény (nyers `nave.txt`, `scope=teljes | forras=eszkozok/nave_import.py | ts=2026-09-30`):

| Mérőszám | régi | új |
|---|---|---|
| egyfejezetes hivatkozás `X 1:1`-gyel (hibás) | 250 | 21 (ebből 17 valódi „:1”; 4 jelölt, bizonytalan) |
| javított egyfejezetes hivatkozás | 0 | 246 |
| `:<szám>`-mal kezdődő `cimke` | 688 | 0 |
| `utotag::<szám>` | 130 | 0 |
| `vers` sorok | 77 935 | 77 985 |
| adatsorok | 85 066 | 85 116 |
| `gyanus_kijelzes` | 20 | 24 |

Nem javítható biztosan (4 sor, `gyanus_kijelzes:egyfejezetes_nincs_versszam`): a ref után nincs versszám. Mellékhatás: az `azonos` 41 330 → 41 327 (az 1:1 `azonos`-nak vett hamis hivatkozások kiestek).

**2.5. Mit mér a „kijelzett szöveg ↔ `osisRef`” ellenőrzés.** A javítás után a nem egyfejezetes 77 685 `osisRef`-re: a kijelzett szöveg első fejezet:vers száma egyezik az `osisRef`-fel 77 673 esetben, 12 nem (a jelölt `PrAzar.1.2` hibák). Ez a forrás két mezőjének **belső** konzisztenciája; független kiadáshoz mért helyességet (l. 2.3, 5.) nem bizonyít.

**2.6. Második ellenőri lelet és javítás (F18.7).** A `DISP_RE` (`[A-Za-z]{1,6}`) a legfeljebb 6 betűs könyvnevekkel (Micah, Ezra, Joel, Amos, Titus, Isaiah, Joshua, Jonah, Daniel, „So”) összeolvadt hibás kijelzést szabályosnak vette, így a hamis fejezet-hivatkozások (`Mik 2`, `Ezsd 1`, `Tit 2`, `Jóel 1`, … + `Wis.2`) jelöletlenek maradtak. Javítás: minden `osisRef`-nél, amelynek a `</ref>` utáni, szóköz nélküli szövege `Ch|Ki|Sa|Ti|Co|Th|Pe|Jn` + szám töredék, a sor `gyanus_kijelzes`-t, `toredek:`-ot és — ha a kijelzés számjegye az osisRef fejezetszámával (ismeretlen könyvnél: anélkül) egyezik és szám+betűk létező könyvrövidítés — `javaslat:`-ot kap (pl. `Mik 2` → `javaslat:2Krón 34:20`); az `igehely` nem íródik át (a forrás a rekonstrukciót nem bizonyítja). A töredék kikerül a következő hivatkozás `cimke`-jéből. Továbbá: (a) az egyfejezetes soroknál az `igehely_osis` szintetizált, az eredeti forrás-osisRef a `megjegyzes` `eredeti_osis:` eleme (296 sor); (b) minden jelölt sor `karoli_allapot=nem_ertekelt` (volt: 2 `azonos`, 2 `ujszovetseg_nincs_tabla`, 35 `fejezet`, 13 `n.a.`). Mért (nyers `nave.txt`, `scope=teljes | forras=eszkozok/nave_import.py | ts=2026-09-30`):

| Mérőszám | F18.6 | F18.7 |
|---|---|---|
| adatsor / `vers` / `lasd` / `szoveg` / `tema_id` | 85 116 / 77 985 / 4 368 / 2 763 / 5 322 | változatlan |
| `hely_tipus` (vers / tartomány / fejezet / ismeretlen_konyv) | 64 150 / 11 615 / 2 207 / 13 | változatlan |
| `gyanus_kijelzes` **sor** | 22 (24 jelölésből; 2 Abd-sor kétszer) | **52** |
| `gyanus_kijelzes` **jelölés-előfordulás** | 24 | **54** |
| ebből `toredek:` / `javaslat:` | 0 / 0 | 49 / 49 |
| `karoli_allapot` `azonos` / `ujszovetseg_nincs_tabla` | 41 327 / 21 826 | 41 325 / 21 824 |
| `karoli_allapot` `fejezet` / `n.a.` / `nem_ertekelt` | 2 207 / 13 / 0 | 2 172 / 0 / 52 |
| `tartomany` / `eltero` / `nincs_a_tablaban` / `a_tablaban_nincs_kjv_megfelelo` | 11 615 / 270 / 582 / 145 | változatlan |
| `cimke` töredékkel (`Ch 6:6,51`-szerű) | 4 | 0 |
| `eredeti_osis:` jelölt sor | — | 296 |

Megjegyzés: az F18.6 „24 gyanus_kijelzes sor” a jelölés-előfordulás volt (22 sor); a mostani két szám mindkettőt külön adja. Nem bizonyított, hogy a töredék-szabály minden összeolvadás-osztályt megfog; a teljes független kiadás-összevetés hiányzik.

## 3. A 32254/4951/92610 (FJ4) ↔ 32253/4980/92609 (F06) eltérés oka

Mindkét szám a **theonize** `Topics.csv`/`TopicIndex.csv`-re vonatkozik; a theonize-adatot a DT5 szerint nem töltöttem le újra és nem használtam.

| Szám | FJ4 | F06 | Ok |
|---|---|---|---|
| `Topics.csv` | 32 254 „sor” | 32 253 „adatsor” | **+1 = a fejlécsor.** F06 (`F06_nave.tsv`) kifejezetten „adatsorai”-t mér, az FJ4 „sor”-t. Valószínű magyarázat (az FJ4 módszere nincs dokumentálva, ezért nem bizonyított). |
| `TopicIndex.csv` | 92 610 | 92 609 | **+1 = fejlécsor**, ugyanúgy. |
| Egyedi főtéma | 4 951 | 4 980 | **Nem tárható fel** a repóban meglévő mérési fájlokból: az FJ4 nem rögzíti, mi számít „főtémának” (egyedi `Topic`-érték? szűrés?). A +29 eltérés lehet eltérő egyediség-kulcs (kis/nagybetű, szóköz) vagy szűrés; mérni csak a theonize-adaton lehetne, amit a DT5 kizár. |

Az irányadó az F06. Mivel a theonize nincs importálva, az eltérés az F18 eredményét nem befolyásolja; `javaslat`: nem folytatjuk. Az összehasonlítás kedvéért a basokant: 5 322 entry, 5 320 egyedi cím — a theonize 4 980 egyedi `Topic`-jával nem egyezik (más szemcsézettség; nem szabad 1:1-nek venni).

## 4. A Gemini-lépés (3.2)

**Nem futott, költség 0 USD.** A 3.2 lépés a szkripttel nem illeszthető theonize↔basokant témapárokat ítélte volna meg; theonize nélkül nincs párosítandó oldal, az ítélet értelmét vesztette. A hivatkozás-szintű teljességet a 2.1 determinisztikusan mérte. `javaslat`: a LLM-lépést ne erőltessük; ha később kell (pl. kiadás-összevetés szövegszinten), új tétel.

## 5. Küszöb (<90% egyezés → `javaslat` státusz) az új helyzetben

A brief küszöbe az import és a basokant közti témaszintű egyezésre szólt. Az új helyzetben az importforrás maga a basokant, tehát a küszöb két mérhető mennyiségre vetül:

1. hivatkozás-darabszám-egyezés a nyers forráshoz képest: **egyezik** (2.1; ez nem helyesség-mérték, l. 2.4–2.5);
2. egyezés egy független (itt: másodkézből való, web, nem elsődleges) kiadással: **12/12 téma**, de n=12 nem véletlen és nem reprezentatív (2.3).

Döntésem (`javaslat`): az import **`javaslat` státuszú marad**, mert a 90%-os küszöb nem teljes, független kiadás-összevetésen (mind az 5 322 témán) teljesült, csak kis mintán; a `Nave_basokant.tsv` fejlécében és README-jében ez áll. A státusz akkor léphet `kész`-re, ha (a) a felhasználó elfogadja a közkincs-állítást és a lekaparás eredetét (DT5-ben elfogadta a forrást, de a licencfájl-hiányt a F24 tisztázza), és (b) egy teljes szövegű független kiadással (pl. Gutenberg/CCEL/IA letöltéssel, a felhasználó engedélyével) futhat az összevetés.

## 6. Nyitott tételek

- Független teljes kiadás-összevetés (letöltés-engedély kell).
- A `theonize` 4951↔4980 eltérés: nem folytatjuk.
- `adat/datasetek.tsv`: a Nave-hez nincs sor; nem az én fájlom (közös állomány), javaslat: az orkesztrátor vegye fel.
- A táblát semmilyen study-táblázat nem használja; minden felhasználás `adat/jeloltek.tsv`-n át (CLAUDE.md 2. szabály).
- N27 lezárva (`NYITOTT_FELADATOK.md`).

**Költség:** Gemini 0 USD; WebFetch/WebSearch díjmentes eszközhívás.

**2.7. Harmadik ellenőri kör (célzott, F18.7-re).** Helyesbítés a 2.6-hoz: a „Titus/`Tit 2`” és a `Co` előtag nem teljesen lefedett — 4 `Tit 2` sor és 8 `Kol 8:x/12:18` sor (valójában 2Kor) jelöletlen, mert a töredék önálló `<ref>`-et kapott (TSV 16103–16106, 19518–19519, 51735–51737, 52528–52530). A `Jer 2` (84711) nem „valószínűleg helyes”: a forrás `Jeremiah 2</ref> <ref>2 Ch 36:12`, a sor jelölt. Jelöletlen rokon osztályok: 15 római számos névhez tapadt, `<ref>` nélküli hivatkozás-sor; „with N:N” folytató-hivatkozás (72 `utotag`, 54 `cimke`). Részletek: `naplok/ELLENOR_F18.md` 3. kör, DONTESEK DT18.


**2.8. Javító kör a 3. ellenőri körre (F18.12, felhasználói döntés).** A 3. kör hét tételéből öt kódjavítást kapott (a 6. és 7. a 2.7-ben zárult); a parszoló újrafutott a nyers `nave.txt`-ről (sha256 azonos), a TSV újragenerálva. Mérés: a régi TSV (F18.7, `679723e`-ből generált) és az új sorról sorra összevetve: a **174 eltérő régi sor mind besorolható** a tételek egyikébe (72 `utotag`-with + 59 `cimke`-with + 16 `javaslat` + 12 Titus/Kol + 9 `szoveg` + 6 római-számos cimke = 174; `egyéb`: 0); az új oldalon 304 sor. Más sor nem változott.

| # | tétel | régi | új |
|---|---|---|---|
| 1 | `javaslat` csonkolt tartomány/lista (a `toredek:` több helyet tartalmaz, a `javaslat:` csak az elsőt) | **13 sor** (a brief ≥8-a pontosan mérve; pl. `Ch 4:17,19` → `1Krón 4:17`; `Ki 19:1-4` → `2Kir 19:1`; `Ch 15:1-15` → `2Krón 15:1` ×3; `Ch 24:2,17-25` → `2Krón 24:2`) | **0** (a `javaslat:` a töredék teljes helylistáját őrzi: `1Krón 4:17,19`, `2Kir 19:1-4`, `2Krón 24:2,17-25`; ellenőrizve: a 53 `toredek:`-os sor közül 0, ahol a `javaslat:` hely ≠ a `toredek:` helye) |
| 2 | önálló `<ref>`-es töredék (`Titus 2` + `Co 8:16`, valójában 2Kor) | **12 jelöletlen sor** (TSV 16103–16106, 19518–19519, 51735–51737, 52528–52530: 4 × `Tit 2` + 8 nem létező `Kol 8:x/12:18`) | **0 jelöletlen**: 8 sor javítva (`2Kor 8:16`, `8:17`, `12:18`, `8:22`, `8:19`, `8:23`, `8:16`, `8:17`; `igehely_osis` = `2Cor.…`, megjegyzés `javitva:eredeti_osis=Col.8.16`, `karoli_allapot` újraszámolva = `ujszovetseg_nincs_tabla`); 4 `Tit 2` sor `gyanus_kijelzes:Titus 2;toredek:Co 8:16;javaslat:2Kor 8:16`, `nem_ertekelt` (a név+szám összevonás maga nem hivatkozás; az `igehely` itt sem íródik át, mint az F18.7-es töredékes soroknál). `Col.8.x` sor az új TSV-ben: 0 |
| 3 | római számos név után `<ref>` nélküli hivatkozás (`Ben-hadad I 1Ki 20`, `Herod Agrippa II Ac 26:2,3`) | **15 sor** (9 hivatkozás nélküli `szoveg`-sor + 6 `cimke`-be csúszott; 12 igehely nem lett sor) | **0 jelöletlen**: 14 új `vers`-sor (`megjegyzes`: `ref_nelkuli_hivatkozas:<eredeti szöveg>`, a név a `cimke`-ben marad), a 9 `szoveg`-sor helyébe 12 `vers`-sor lépett; `szoveg` 2 763 → 2 754 |
| 4 | „with N:N” folytató-hivatkozás | **72 `utotag`-sor + 59 `cimke`-sor** (a 3. kör 54 `cimke`-sort mért; a mostani újramérés minden sort számol, amelynek `cimke`-je `with <szám>`-ot tartalmaz: 59; a cimke a következő hivatkozások sorára is öröklődött) | **0 / 0**; 125 új `vers`-sor, `megjegyzes`: `with_folytato:<eredeti szöveg>;konyv_oroklve:<OSIS-könyv>`. A cimke-öröklődés megszűnt: a „with …” szöveg kikerült a `cimke`-ből (a soron mögötte álló cimke a megelőző szöveg); 125 sor közül a könyv-öröklés mind azonos sorból/egységből történt (0 sorok közötti örökség). Nem egyértelmű: 1 sor (`AMNESTY`: az előző hivatkozás maga összeolvadt töredék, `Ámós 2` ← `2Sám 19:13`): `Ámós 17:25`, `gyanus_kijelzes:with_folytato_bizonytalan_konyv`, `nem_ertekelt`, `javaslat:2Sám 17:25` |
| 5 | SEMA 2.13 `javaslat` állapotérték | nem volt (a két 12. sor `nincs adatosítva`) | felvéve (definícióval), a két sor `javaslat` |

**Összesített mérés (régi → új).** Adatsor **85 116 → 85 246** (+130: +125 `with`-sor, +14 római-számos sor, −9 sor, amely `szoveg` volt és most a hivatkozás-sor(ok) része: 85 116 + 125 + 14 − 9 = 85 246 — a bontás több sort ad). `kapcsolat`: `vers` 77 985 → 78 124 (+139) · `lasd` 4 368 → 4 368 · `szoveg` 2 763 → 2 754. `tema_id` 5 322 (változatlan). `hely_tipus` (vers/tartomany/fejezet/ismeretlen_konyv): 64 150 / 11 615 / 2 207 / 13 → 64 236 / 11 663 / 2 212 / 13. `karoli_allapot`: `azonos` 41 325 → 41 389 · `eltero` 270 · `a_tablaban_nincs_kjv_megfelelo` 145 · `nincs_a_tablaban` 582 → 585 · `ujszovetseg_nincs_tabla` 21 824 → 21 842 · `tartomany` 11 615 → 11 663 · `fejezet` 2 172 → 2 173 · `nem_ertekelt` 52 → 57.

**A korábbi 52 `gyanus_kijelzes`-sor alakulása:** 52 → **57 sor** (54 → **59** jelölés-előfordulás; `toredek:`-sor 49 → 53, `javaslat:` 49 → 54, `nem_ertekelt` 52 → 57). A 52 változatlanul jelölt (13 sor javaslata bővült a teljes listára); +4 (`Titus 2`-sorok, tétel 2) +1 (`AMNESTY` with-sor, tétel 4). Az új jelölt sorok mind `nem_ertekelt`.

**Amit a javítás nem mér / ami nyitva marad:**
- **8 `utotag` „with N” fejezetszám-folytatás** (`with 20`, `with 1; 2`, `with 9`, `with 57; 58; 59`, `with 13; 14; 15; 16`, `with 1; 2; 3; 4`, `with 8; 9`, `with 22; 23`; TSV-sorok 5262, 30165, 37101, 38335, 38736, 38740, 52627, 73969): nem „N:N” alakúak, a fejezet/vers értelmezés nem egyértelmű, ezért nem parszoltuk és nem is jelöltük — a 3. kör hét tétele közé nem tartoztak; **nyitott**, DT18-ban jelezve.
- A `with N:N` és a római-számos szabály a **forrás szövegmintájára** épül (előző hivatkozás könyve; `I/II/III…` + Nave-rövidítés + szám); hogy más, ettől eltérő szövegbe csúszott hivatkozás-osztály nincs, **nem bizonyított**. A `Co` rövidítés szándékosan kimaradt a római-számos szabály táblájából (1Co/2Co nem egyértelmű).
- A `with` folytatás könyve az entry előző hivatkozásának (a szabály szerinti utolsó `osisRef`) könyve; a forrás szerint ez volt az összes 125 esetben ugyanabban a sorban/egységben; a szemantikai helyességet szúrópróba sem ellenőrizte független kiadás.
- A javítás a forrást **nem írja át**: a TSV-ben a javított sorok a `javitva:eredeti_osis=` jelöléssel követhetők vissza.
- Az ellenőrző-futtatás (E1–E17, `feladatok.py ellenoriz`) eredménye a commit-üzenetben és a jelentésben; független ellenőr a 4. körre nem futott.
