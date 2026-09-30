# F18 — Nave-import napló (DT5, 1. opció: basokant/nave, saját parszoló)

*Ág: `claude/nave-import` · 2026.09.30 · kimenet: `konkordancia/Nave_basokant.tsv` (+ `Nave_basokant_README.md`) · eszköz: `eszkozok/nave_import.py` · állapot: **javaslat***

## 1. Mi készült

| | |
|---|---|
| Forrás | `basokant/nave` @ `4f35c7d4ffd4933f4db1b9d5182db90dc04bd235` (a helyi klón HEAD-je egyezik), `data/nave.txt`, 4 537 041 karakter, sha256 `560dcb1a…052f43a` |
| Licenc | közkincs a README szerint (Nave, 1897); licencfájl nincs (`F18_licenc.md`) |
| Parszoló | saját (`eszkozok/nave_import.py`); a basokant szkriptjei és a `parsed-nave.json` nincs átvéve (a JSON csak ellenőrző összevetésre szolgált) |
| Kimenet | 85 116 adatsor (+ fejléc és 5 kommentsor), 5 322 `tema_id` *(első változat: 85 066; az egyfejezetes-javítás +50 sort adott, l. 2.4)* |
| Soronként | 77 985 `vers` (64 150 egyes vers, 11 615 tartomány, 2 207 fejezet, 13 `ismeretlen_konyv`) · 4 368 `lasd` · 2 763 `szoveg` (hivatkozás nélküli egység) *(régi: 77 935 · 64 138 · 11 577)* |
| Témák | 5 322 entry, 5 320 egyedi cím (`REVERENCE`, `SIN` kétszer) |
| Károli-állapot (egyes versek, 64 150) | `azonos` 41 327 · `eltero` 270 · `a_tablaban_nincs_kjv_megfelelo` 145 · `nincs_a_tablaban` 582 · `ujszovetseg_nincs_tabla` 21 826 (a `Karoli_versmegfeleltetes.tsv` ÓSZ-i) *(régi: 41 330 · 270 · — · 727 · 21 811; a 727 = 582 + 145)* |
| Gyanús sorok | 24 `gyanus_kijelzes` (20 lekaparási hiba, pl. „Azariah 2Ch 31:10” → `PrAzar.1.2`, + 4 egyfejezetes, versszám nélküli sor) *(régi: 20)*; 13 `ismeretlen_konyv` |

Mellékhatás: a meglévő `adat/` és `konkordancia/` fájlokból egy sor sem változott, nem csökkent (a munkafa csak három új fájlt tartalmaz az import során).

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
