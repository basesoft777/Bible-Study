# F18 — Nave-import napló (DT5, 1. opció: basokant/nave, saját parszoló)

*Ág: `claude/nave-import` · 2026.09.30 · kimenet: `konkordancia/Nave_basokant.tsv` (+ `Nave_basokant_README.md`) · eszköz: `eszkozok/nave_import.py` · állapot: **javaslat***

## 1. Mi készült

| | |
|---|---|
| Forrás | `basokant/nave` @ `4f35c7d4ffd4933f4db1b9d5182db90dc04bd235` (a helyi klón HEAD-je egyezik), `data/nave.txt`, 4 537 041 karakter, sha256 `560dcb1a…052f43a` |
| Licenc | közkincs a README szerint (Nave, 1897); licencfájl nincs (`F18_licenc.md`) |
| Parszoló | saját (`eszkozok/nave_import.py`); a basokant szkriptjei és a `parsed-nave.json` nincs átvéve (a JSON csak ellenőrző összevetésre szolgált) |
| Kimenet | 85 066 adatsor (+ fejléc és 5 kommentsor), 5 322 `tema_id` |
| Soronként | 77 935 `vers` (64 138 egyes vers, 11 577 tartomány, 2 207 fejezet) · 4 368 `lasd` · 2 763 `szoveg` (hivatkozás nélküli egység) |
| Témák | 5 322 entry, 5 320 egyedi cím (`REVERENCE`, `SIN` kétszer) |
| Károli-állapot (egyes versek, 64 138) | `azonos` 41 330 · `eltero` 270 · `nincs_a_tablaban` 727 · `ujszovetseg_nincs_tabla` 21 811 (a `Karoli_versmegfeleltetes.tsv` ÓSZ-i) |
| Gyanús sorok | 20 `gyanus_kijelzes` (lekaparási hiba, pl. „Azariah 2Ch 31:10” → `PrAzar.1.2`); 13 `ismeretlen_konyv` |

Mellékhatás: a meglévő `adat/` és `konkordancia/` fájlokból egy sor sem változott, nem csökkent (a munkafa csak három új fájlt tartalmaz az import során).

Nem committolt: a nyers `nave.txt` (4,5 MB); reprodukálás a commit-hash + sha256 alapján (`--forras`). *Javaslat:* maradjon így (a sha256 a letöltött fájl ellenőrzésére szolgál; a commit-hash a GitHubon rögzített, de a repó eltűnése esetén a fájl nem állítható vissza) — az összesítő tételben.

**Eltérés a briefhez:** a brief `ir` listája `konkordancia/Nave_theonize.tsv`-t nevez. A fájl a DT5 miatt `konkordancia/Nave_basokant.tsv` (a „theonize” név félrevezető lenne). Javaslat; az összesítő tételben.

## 2. Eredet- és pontosság-ellenőrzés

**2.1. A parszoló teljessége a nyers szöveghez képest (szkript).** A nyers fájlban 5 322 `$$$`-entry, 82 303 `<ref>` (77 935 `osisRef` + 4 368 `target`), a kimenetben 5 322 `tema_id`, 77 935 `vers`-sor és 4 368 `lasd`-sor. Hivatkozás-szinten **100%**. (A `tag`-szerkezet ellenőrzve: csak `entryFree, def, list, item, ref`; `list` mélysége legfeljebb 1; az `</entryFree>` mindenütt megvan.)

**2.2. A basokant-JSON mint belső összevetés.** A `parsed-nave.json` (5 322 elem) verses-szám összege 56 645, relatedTopics 2 469 — a nyers szöveg 77 935 / 4 368 hivatkozásával szemben. Témánként 4 368 téma egyezik a versszámban (82,1%), 954 témában a JSON-ban kevesebb van (soha több: 0). Tehát a basokant JSON-ja **veszteséges**, a nyers fájl teljes: ez megerősíti, hogy saját parszolót kellett írni, és a JSON nem használható importforrásnak. (Csak mennyiségi összevetés; a veszteség okát — pl. a `<list>` elemek kezelése — a basokant szkriptjeinek olvasása nélkül nem vizsgáltuk.)

**2.3. Független kiadással való szúrópróba.** A Project Gutenberg / CCEL / Internet Archive teljes szövege az elérhető eszközökkel (WebFetch, JS-renderelt vagy csonkolt oldalak) **nem volt lekérdezhető**; ezt mértem: 4 kísérlet sikertelen. Elérhető volt a `biblestudytools.com/concordances/naves-topical-bible/` témánkénti oldala (a közkincs Nave-szövegre épülő, a basokant-lekaparástól független megjelenítés; maga is másodkézből való, tehát ez **nem** elsődleges kiadás-összevetés).
12 téma összevetése az igehely-halmazra: `AARON` (kb. 100 hivatkozás, soronként), `ABEL`, `ABBA`, `ABAGTHA`, `ABDA`, `ACHBOR` (szemrevételezve), `ACHAN`, `AGABUS`, `ABIATHAR`, `ABISHAI`, `ABIGAIL`, `ABED-NEGO` (szkripttel, a tartomány-alak normalizálása után): **12/12 egyezik** a verses-halmazban, a hivatkozások sorrendjében és az altéma-csoportosításban is, ahol megvizsgáltam. A minta kicsi és nem véletlen (kis/közepes témák az ábécé elejéről), ezért **nem** általánosítható az 5 322 témára.

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

1. parszolási teljesség a nyers forráshoz képest: **100%** (2.1);
2. egyezés egy független (itt: másodkézből való, web) kiadással: **12/12 téma (100%)**, de n=12 nem reprezentatív (2.3).

Döntésem (`javaslat`): az import **`javaslat` státuszú marad**, mert a 90%-os küszöb nem teljes, független kiadás-összevetésen (mind az 5 322 témán) teljesült, csak kis mintán; a `Nave_basokant.tsv` fejlécében és README-jében ez áll. A státusz akkor léphet `kész`-re, ha (a) a felhasználó elfogadja a közkincs-állítást és a lekaparás eredetét (DT5-ben elfogadta a forrást, de a licencfájl-hiányt a F24 tisztázza), és (b) egy teljes szövegű független kiadással (pl. Gutenberg/CCEL/IA letöltéssel, a felhasználó engedélyével) futhat az összevetés.

## 6. Nyitott tételek

- Független teljes kiadás-összevetés (letöltés-engedély kell).
- A `theonize` 4951↔4980 eltérés: nem folytatjuk.
- `adat/datasetek.tsv`: a Nave-hez nincs sor; nem az én fájlom (közös állomány), javaslat: az orkesztrátor vegye fel.
- A táblát semmilyen study-táblázat nem használja; minden felhasználás `adat/jeloltek.tsv`-n át (CLAUDE.md 2. szabály).
- N27 lezárva (`NYITOTT_FELADATOK.md`).

**Költség:** Gemini 0 USD; WebFetch/WebSearch díjmentes eszközhívás.
