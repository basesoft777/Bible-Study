# F4 brief — a generátorok (`general.py`)

*Készítette: chat-menet (Opus 5), 2026-09-15, **v4** (v1: első kiadás; v2: a G0 három kérdése eldöntve, a D3 lecserélve; v3: a `fo_elofordulas` csoportkulccsá vált, az 1. menet lefutott, három lelet kritériumként felvéve; v4: a 2. menet lefutott, a könyvnév-normalizálás a táblába kerül (K15/D14), a hiánylista kettéosztva, a study-összevetés módszertana pontosítva). Kiindulási állapot: `main` = `origin/main` = **`a7d23a6`** (F4-0, F4.0e, F4.1, F4.2, F4.2a, F4.3 lezárva).*
*Végrehajtás: Claude Code, a repó gyökeréből. A chat-menet nem hajtja végre — ez a brief a bemenete.*
*Előzmény: `F4_BRIEF.md` (F4-0, csv-mentesítés + stderr-őr). Ez a fájl az F4 tulajdonképpeni tartalmát írja le.*

---

## 0. Miért kell a terv elfogadási tesztjét újrafogalmazni

Az `ATALAKITASI_TERV.md.md` 446-450. sora szerint az F4 elfogadási tesztje ez:

> a generált `PaRDeS_motivumok.md` diffje a jelenlegihez képest csak formázási
> eltérést mutasson, tartalmit ne.

**Ez a teszt ebben a formában hamis riasztást ad, két, egymástól független okból.**

**Egy.** A viszonyítási alap nem korábbi generátor-kimenet, hanem **kézzel írt
forrásfájl**. A `motivumlog/PaRDeS_motivumok.md` ma 90 motívum-tételt tartalmaz
8 témacsoportban; az `adat/motivumok.tsv` **7 ID-t** ismer. A generált fájl és a
mai fájl között tehát nem formázási eltérés lesz, hanem **83 hiányzó tétel** —
és ez nem betöltési hiba, hanem a betöltés hatóköre: az F3 a hét lezárt
tematikus study-t töltötte be, nem a teljes naplót.

**Kettő.** Az F4-0 lezárása után a `kapcsolodas` mező **79 idézőjellel kezdődő
értéke** visszakerült a képbe (mérve `e253c2a`-n: 79 mező kezdődik `"`-tel, 127
tartalmaz `"`-t). Ezek az idézőjelek határolják el a szó szerinti igeidézetet a
magyarázattól. A generált szövegben tehát megjelennek — a mai kézzel írt
fájlokban viszont hol megvannak, hol nincsenek, mert az emberi szerkesztés nem
volt következetes. Ez is tartalmi diffnek fog látszani, holott a generátor
csinálja helyesen.

Ebből nem az következik, hogy a teszt rossz ötlet, hanem hogy **a viszonyítási
alapot kell megváltoztatni**. A §3.1 pont adja meg a helyére lépő tesztet.

---

## 1. Mért kiindulási állapot

Minden szám alább független méréssel készült az `e253c2a` munkapéldányán, nem
korábbi menet jelentéséből átvéve.

### 1.1 Az adatréteg — mit tud ma a tábla

| Tábla | adatsor | megjegyzés |
|---|---:|---|
| `adat/motivumok.tsv` | **7** | KIRALY-001, ISTENTISZT-001, TEREMT-001, ALVIL-001, MENNY-001, ANTROP-001, HODIT-001 |
| `adat/elofordulasok.tsv` | **201** | l. lent, ID-nkénti bontásban |
| `adat/kapcsolatok.tsv` | **32** | **csak 2 ID-hez**: ISTENTISZT-001 (23), KIRALY-001 (9) |
| `adat/jeloltek.tsv` | **221** | 201 *beépítve*, 17 *nyitva*, 3 *elutasítva* |
| `adat/lexikon_hivatkozasok.tsv` | **0** | fejléc van, adatsor nincs |

Előfordulások ID-nként: ALVIL-001 **72**, TEREMT-001 **41**, HODIT-001 **33**,
ISTENTISZT-001 **29**, MENNY-001 **9**, KIRALY-001 **9**, ANTROP-001 **8**.

Mezőkitöltöttség az `elofordulasok.tsv` 201 során:

| mező | kitöltött | | mező | kitöltött |
|---|---:|---|---|---:|
| `igehely`, `kapcsolodas`, `gerinc_elem` | 201 (100 %) | | `funkcio` | **38 (18 %)** |
| `karoli_szo`, `azonositas_modja` | 201 (100 %) | | `bdb_entry_id` | **27 (13 %)** |
| `megbizhatosag`, `proveniencia`, `igazolas` | 201 (100 %) | | `jelentes_szam` | **26 (12 %)** |
| `strong` | 198 (98 %) | | `jelentes_hu` | **25 (12 %)** |
| `pardes_szint` | 166 (82 %) | | `jelentes_en` | **10 (4 %)** |

Két további mért tény, amely a rendereléskor azonnal előjön:

- A `pardes_szint` **14 sorban `Pshat`-ot ír** (7 × `Pshat`, 3 × `Pshat/Remez`,
  3 × `Pshat/Drash`, 1 × `Pshat/Sod`), miközben a sablon és minden study-szöveg
  `Peshat`-ot használ. 35 sorban üres.
- A `proveniencia` **mind a 201 sorban `scope=manual`**. Ez helyes — az F3
  kinyerés volt, nem lekérdezés —, de azt jelenti, hogy a generált kimenet
  minden sora `manual` provenienciát fog hordozni. Nem hiba, de előre
  kimondandó, mielőtt valaki „ellenőrizetlennek" olvassa.

### 1.2 A kimenet — mit tartalmaz ma a fájl

`motivumlog/PaRDeS_motivumok.md`, 589 sor, 134 053 bájt, hat szakasz:

| szakasz | tartalom | generálható? |
|---|---:|---|
| Tematikus áttekintés | **90 tétel**, 8 témacsoport | részben — 7 tételre |
| ⭐ Emlékeztető küszöb | **22 bekezdés** | részben — 7 tételre, és csak a fejsor |
| Előrejelzett motívumok | **15 táblasor** | **nem** — nincs forrásmezője |
| Kulcsszó-index | **90 táblasor** | részben — 7 tételre |
| Kulcsszavak részletesen | ~45 alszakasz | **nem** — `motivumok/[ID].md` nem létezik |
| Könyv szerinti index | — | igen, `elofordulasok`-ból |

A naplóban **14 különböző `[ID: …]` szerepel**; ebből **7 van a táblában**.
Hiányzik: `ANTROP-002`, `ANTROP-003`, `ANTROP-004`, `HAMART-001`,
`ISTENTISZT-002`, `SZOVETS-001`, `TEREMT-002`. A maradék **76 motívum-tételnek
egyáltalán nincs ID-ja.**

A `HAMART-001` hiánya a legsúlyosabb: a `Lezart_tematikus_tanulmanyok_index.md`
**8. sora** ez a motívum (46 táblázat-sor, 2026.09.11-i lezárás), van hozzá
kereszthivatkozás-napló is — de sem a `motivumok.tsv`-ben, sem a
`jeloltek.tsv`-ben nincs egyetlen sora sem. Az F3 betöltés hét study-t vitt be,
és ez a nyolcadik.

### 1.3 A három rés — ezekre a generátor nem tud választ adni magától

**a) ID-rés.** 7 betöltött ID · 14 ID-vel jelölt napló-tétel · 90 napló-tétel.
Ha a generátor a `motivumok.tsv`-ből írja újra a Tematikus áttekintést, **83
tétel eltűnik**. Ez nem formázási diff.

**b) Számlálás-rés.** A „hány előfordulás" kérdésre ma **három különböző válasz**
él egyszerre, és mindhárom megtalálható a repóban:

| ID | napló, Tematikus áttekintés | index / részletes bejegyzés | `elofordulasok.tsv` sorszám |
|---|---:|---:|---:|
| ALVIL-001 | 4 | 6 | **72** |
| TEREMT-001 | 5 (Tóra-szintű fő) | 35 ÓSZ + 9 ÚSZ | **41** |
| ISTENTISZT-001 | 5 | 24 igehely | **29** |
| ANTROP-001 | 5 | 5 | **8** |
| KIRALY-001 | 1 | 1 fő genezisi | **9** |
| MENNY-001 | 1 | 1 fő | **9** |
| HODIT-001 | 1 | teljes lexikai ív | **33** |

A napló „fő előfordulást" számol (a motívum önálló megjelenéseit), a tábla
**minden igehely-sort**. A séma ma nem különbözteti meg a kettőt.

**Eldöntve (D3 + D10):** mindkettő a táblából jöjjön, és a mező **nem logikai
érték, hanem csoportkulcs** — mert a napló többször egyetlen fő előfordulásként
nevez meg egy versközt (`1Móz 6:1-4`, `2Móz 15:5,8`, `Luk 1:46-47`,
`1Kor 2:14-15`, `Zsolt 16:10 ⇒ ApCsel 2:27,31`), amit a tábla külön sorokra
bontva tárol. Egy igen/nem mezővel vagy a szám nőne fel hamisan, vagy egy
igehely-sor tűnne el a számlálásból indoklás nélkül.

`fo_elofordulas` = a fő előfordulás azonosítója, a napló saját megnevezésével;
üres = nem tartozik fő előforduláshoz. A ⭐ küszöb ezután
**`COUNT(DISTINCT fo_elofordulas)`**, és a generált szöveg
`6 fő előfordulás / 72 igehely-sor` alakot ír.

Az ok nem esztétikai: ha az áttekintés a puszta sorszámot mutatná, a ⭐ küszöb
(„3+ előfordulás") értelmét vesztené — minden betöltött motívum messze túl lenne
rajta. Ráadásul a mező **visszamutat a napló szövegére**: grepelhető, tehát az
összevetés bármikor megismételhető.

**c) Forrásréteg-rés.** A terv 1.B szerint a `Kulcsszavak részletesen` szakasz
forrása `motivumok/[ID].md` — **ez a könyvtár nem létezik**. (A `CLAUDE.md`
ugyanezt `motivumlog/[ID].md` néven írja; a két hivatkozás eltér, ez is
eldöntendő.) Amíg a ⚠️-viták, a kizárások indoklásai és a szótartalmi jegyzetek
a napló prózájában ülnek, a szakasz nem generálható, csak megsemmisíthető.

### 1.4 Amit a többi kimenet ma mutat

- **`Lezart_tematikus_tanulmanyok_index.md`**: 8 sor. A `Megjegyzés` oszlop
  (soronként 3-10 mondat) **egyetlen tábla-mezőnek sem felel meg**. A generálható
  oszlopok: `#`, Motívum (`cim`), Fájlnév (`forras_study`), Érintett igehelyek
  (`elofordulasok`-ból összefűzve). A negyedik oszlop nem.
- **Kereszthivatkozás-naplók**: 7 fájl a `tematikus_lezart/naplok/` alatt. A
  `jeloltek.tsv`-ben viszont **TEREMT-001-hez 41 sor van, mind `beépítve`, 0
  `elutasítva`** — miközben a Tehóm-napló két indokolt elutasítást (ταρταρόω
  2Pét 2:4, Jel 21:1 θάλασσα) és egy named-teacher gapet dokumentál. Az
  elutasított és a gap-tételek **nincsenek a táblában**. A generált napló ezeket
  elveszítené. Elutasított sor egyedül a HODIT-001-hez van (3), nyitva 17
  (HODIT-001 14, MENNY-001 2, ANTROP-001 1).
- **Tematikus study 1. pont**: pl. `Tehom_tematikus.md` 1. pontja **3 oszlopos**
  (v2-alak), **5 sor**, utána négy prózai bekezdés. A sablon v15 **7 oszlopot**
  ír elő, a tábla ugyanehhez az ID-hez **41 sort** tartalmaz. A study
  `PaRDeS-szint, ahol felmerült` oszlopa `Peshat/Remez — 1Mózes 1 bővített
  tanulmány` alakú; a tábla `pardes_szint` mezője csak `Pshat/Remez`-t tárol —
  **a „hol merült fel" adatnak nincs mezője a sémában.**
- **`NYITOTT_FELADATOK.md`**: 35 085 bájt, gyakorlatilag végig kézzel írt próza,
  bekezdésenként 5-15 mondat, hivatkozásokkal. A terv szerinti forrás
  (`jeloltek` nyitva + `motivumok` státusz) ebből **17 sort** tudna előállítani.
  A fájlból ezen felül **hiányzik minden ATX-fejléc** (egyetlen `#` sincs benne)
  — ezt a generátor előtt érdemes helyretenni, különben a generált blokk
  fejléce lesz az egyetlen a fájlban.
- **`konkordancia/Karoli_Strong_kivonat.tsv`**: a terv 1.C szerint
  `elofordulasok`-ból generált nézet. A valóságban ma a
  `eszkozok/merge_karoli_szofaj.py` állítja elő a `Strong_szotar.tsv`-ből, és
  driftel is (F4.0d tétel). **Ütközés — ez a brief nem oldja fel** (l. §5).
- **`.claude/settings.json` nincs**, tehát a terv 2. pontjának három hookja
  közül egy sincs felállítva.

---

### 1.5 Az 1. menet mért eredménye *(független ellenőrzés, `8febf2a`)*

Az `F4.0e`/`F4.1`/`F4.2` kimenetét a chat-menet a munkapéldányon újramérte, nem
a Code-jelentésből vette át. Ami igazolódott:

| | mért |
|---|---|
| `elofordulasok.tsv` | 201 adatsor, 18 oszlop, 0 CRLF |
| `fo_elofordulas` | **32 sor / 24 csoport** — ID-nként pontosan a céltábla szerint |
| `Pshat` | 0 előfordulás; a `pardes_szint` kitöltöttsége változatlan (166) |
| a 16 régi mező | mind a 16 kitöltöttségi száma egyezik az F4.0e előtti méréssel |
| idézőjelek | 79 nyitó / 127 tartalmazó — sértetlen |
| `general.py` | nincs `csv` import; stdout+stderr őr az importok után; `argparse` + `__main__`; `py_compile` OK |
| K7 | éles index CRLF → generált CRLF; éles napló LF → generált LF |
| K8 | `HAMART-001` nevesítve a generált index ⚠️-blokkjában |

A céltábla, amelyhez a `fo_elofordulas` mérve lett:

| ID | megjelölt sor | distinct csoport | a próza száma |
|---|---:|---:|---:|
| ALVIL-001 | 9 | 6 | 6 |
| ANTROP-001 | 8 | 5 | 5 |
| TEREMT-001 | 6 | 5 | 5 |
| ISTENTISZT-001 | 5 | 5 | 5 |
| MENNY-001 | 2 | 1 | 1 |
| KIRALY-001 | 1 | 1 | 1 |
| HODIT-001 | 1 | 1 | 1 |
| **összesen** | **32** | **24** | |

Három lelet a próba-kimenetből, amely a 2. menet bemenete (K12', K13, D12):
a hatókör-sor granularitás-hibája, a nem kanonikus igehely-rendezés, és a
generált index `#` oszlopának instabilitása. Részletek a 3. és a 6.4 pontban.

### 1.6 A 2. menet mért eredménye *(független ellenőrzés, `a7d23a6`)*

| | mért |
|---|---|
| K12' | a hatókör-sor egy granularitás: „90 tételt sorol fel (84 felső szint + 6 alpont), ebből 83 még nincs a táblában" ✓ |
| K13 | könyv-index: `1Móz · 2Móz · 4Móz · 5Móz · Józs · 1Sám · 2Sám · 1Kir` — kanonikus (a 3Móz és a Bír nincs betöltve) ✓ |
| K14 | ALVIL-001 kulcsszó-sora 6 tétel, kanonikus sorrendben ✓ |
| K9 | `generalt_proba/naplok/F4_naplo_hianylista.tsv`, 56 sor, jól formált ✓ |

**Egy lelet, amely a 3. menet bemenete.** A K13-at a Code-menet egy
renderelő-oldali alias-táblával oldotta meg:

```python
KONYV_ALIAS = {'Jelenések': 'Jel', 'Lukács': 'Luk', 'Máté': 'Mt', 'Róma': 'Róm'}
```

Mérve, miért kellett: az `elofordulasok.tsv` **ugyanazt a könyvet két alakban
tárolja** — `Luk 1:46` **és** `Lukács 16:23`; `Róm 10:14` **és** `Róma 10:7`;
továbbá 8 sor `Jelenések …` és 1 sor `Máté 11:23`. Összesen **13 hibás alakú
sor**. A `CLAUDE.md` házi alakja `Mt 24:38`, a
`konkordancia/Konyv_normalizalo_tabla.tsv` pedig `Mt`, `Luk`, `Róm`, `Jel`.

Miért nem kozmetika: az `elofordulasok.tsv` kulcsa **`id + igehely`**, tehát a
`Luk 16:23` és a `Lukács 16:23` két különböző kulcs. Az alias a generátort
megjavítja, de a `gate.py`-t, a `lekerdez.py`-t és minden jövőbeli, igehelyre
épülő joint nem — azok továbbra is néma nem-találatot adnak. A szkript
`hianyzo_konyvek` jelentése sem fogja meg, mert az aliasoltak odáig sem jutnak.
L. **K15** és **D14**.

**Két mérési pontatlanság a Code-jelentésben**, javítva:

- Az ID-nkénti összevetés ISTENTISZT-001 sora (29 vs. 52) **nem 21 sor
  veszteség**: a `## 1.` és `## 2.` közötti szakasz három táblázatot tartalmaz,
  mert benne van az `## 1/b. Kapcsolatok` is. 29 (`elofordulasok`) + 23
  (`kapcsolatok`, ugyanerre az ID-re) = 52. A Tehóm (41 vs. 5) és a Hádész
  (72 vs. 6) viszont valódi szerkezeti átrendezés, ahogy a D8 előre jelezte.
- A hiánylista 56 sorából **32 a HAMART-001-é**, amelynek egyetlen sora sincs a
  `jeloltek.tsv`-ben — ott nem hiányzó elutasítás van, hanem a már ismert
  F3-hiány következménye. A hat betöltött ID-re **24 tényleges sor** marad.
  L. **K9'**.

---

---

## 2. Mit kell csinálni

Hét tétel. A **G0** hatókör-kérdései eldöntve (2026-09-14); ami belőle munka
maradt — a G0/d adat-előkészítés —, az minden renderelő előtt elvégzendő.

A phase egészére egy vezérelv, amely minden tételre vonatkozik:

> **A generátor első körben semmit nem ír felül.** Alapértelmezésben a
> `generalt_proba/` alá termel, és a kimenet maga a diff. Az élesítés — a
> marker-blokkok tényleges beírása az éles fájlokba — külön tétel (G7), külön
> commit, kimenetenként emberi jóváhagyás után.

Indok: a §1.3 három rése miatt az első futás kimenete **biztosan** eltér a mai
fájloktól, és a diff az egyetlen eszköz, amivel eldönthető, hogy az eltérés
javítás-e vagy veszteség.

---

### Tétel G0 — a döntések és az adat-előkészítés

A három hatókör-kérdés **eldöntve, 2026-09-14** (l. D2-D4). Az alábbi G0/d az,
ami a döntésekből kódon kívüli munkaként következik, és minden renderelő előtt
elvégzendő.

**G0/a — a 76 ID nélküli motívum → marker-alapú részleges generálás.**

A generált szakaszok `<!-- GENERÁLT-KEZDET … -->` / `<!-- GENERÁLT-VÉGE -->`
blokkok közé kerülnek; a blokkon kívüli kézi tartalom érintetlen marad. A
felmerült két alternatíva elvetve: mind a 90 tétel ID-zése egy teljes F3-menet
(tételenként a 4.6 gate négy kérdése), a napló kettévágása pedig a
keresztolvashatóságot rontja.

A döntés indoka nem az, hogy a teljes ID-zés drága, hanem hogy **sosem lenne
elég**: a napló akkor is emberi prózát tartalmaz majd, ha mind a 90 tétel ID-t
kap — az „Előrejelzett motívumok" tábla jóslás, a ⚠️-viták ítéletek. A
`PaRDeS_motivumok.md` szerkezetéből adódóan vegyes fájl, nem átmenetileg az. A
marker tehát **véglegesnek szánt architektúra**, nem állvány.

Két feltétel tartozik hozzá:

- A `CLAUDE.md` réteg-táblázata mondja ki, hogy a „generált fájlt kézzel
  szerkeszteni tilos" szabály itt **blokk-szintű**: a marker közti tartalmat
  tilos kézzel írni, a blokkon kívülit szabad.
- Minden generált blokk **nevezze meg a saját hatókörét** egy sorban, pl.
  *„Ez a blokk a 7 betöltött ID-t fedi; a fájl további 83 tétele kézi."*
  Enélkül az olvasó nem tudja megkülönböztetni a „nincs ilyen motívum" és a
  „még nincs betöltve" esetet.

**G0/b — az előfordulás-szám → két szám, mindkettő a tábláról.**

Új mező: `elofordulasok.fo_elofordulas` — **csoportkulcs**, nem logikai érték
(D10): értéke a fő előfordulás azonosítója a napló saját megnevezésével
(`Luk 1:46-47`, `Zsolt 16:10 ⇒ ApCsel 2:27,31`), üres = nem tartozik fő
előforduláshoz. A ⭐ küszöb `COUNT(DISTINCT fo_elofordulas)`. A generált szöveg
alakja `6 fő előfordulás / 72 igehely-sor`. Indoklás: l. §1.3 b).

**G0/c — a forrásréteg neve → `motivumok/[ID].md`.**

A terv 1.B így írja. A `motivumlog/` foglalt (tervezési naplók, pilotok,
changelog) — egy `KIRALY-001.md` ott idegen test lenne. Az `adat/motivumok.tsv`
névhasonlóságát az útvonal egyértelműsíti. A `CLAUDE.md` réteg-táblázata
javítandó (ma `motivumlog/[ID].md`-t ír).

**G0/d — adat-előkészítés** — ✅ **lefutott, `F4.0e`** *(l. §1.5)*

Három tétel, egy commitban:

1. **`fo_elofordulas` mező felvétele** az `elofordulasok.tsv`-be és az
   `adat/SEMA.md` 2.2 pontjába, **csoportkulcsként**. Kitöltés: a hét ID-nél
   **32 sor** kap értéket, **24 csoportban** (a v2-beli „kb. 22 sor" becslés
   alulbecslés volt — a csoportosítás hozta ki). A forrás a
   `PaRDeS_motivumok.md` mai szövege, amely mindegyiket néven nevezi — ez
   átvezetés, nem kutatás. Önellenőrzés: ID-nként a distinct-szám egyezzen a
   ⭐-szakasz kimondott számával, eltérésnél megállás.

   *Az ALVIL-001 4↔6 ütközése eldöntve: **6**. Három hely (index-fejléc a
   dátumozott 4→6 javítással, a napló ⭐-szakasza, a Kulcsszó-index) mond 6-ot,
   egyedül a Tematikus áttekintés bekezdése maradt elavult — az pedig a G7-nél
   generált blokkba kerül, tehát kézzel nem javítandó. A tagságra a napló
   ⭐-szakasza az irányadó: az index #2 sorából **hiányzik a `Jel 1:18`**,
   miközben 6-ot állít (felvéve a `NYITOTT_FELADATOK.md`-be).*
2. **`felmerult_tanulmany` mező felvétele** (l. G6) ugyanígy, `SEMA.md` 2.2-vel
   együtt. Kitöltés a study-fájlok 1. pontjának harmadik oszlopából, ahol van;
   máshol üres.
3. **`Pshat` → `Peshat` javítás** a `pardes_szint` mező 14 sorában. A javítás a
   **táblában** történik, nem a renderelőben: a `CLAUDE.md` szerint
   ellentmondásnál a tábla az irányadó, tehát a tábla legyen helyes. A 35 üres
   `pardes_szint` **marad üresen** — kitöltésük tartalmi ítélet, nem ide
   tartozik.

Mindhárom tábla-írás: `split('\t')` olvasás, `'\t'.join()` írás, **írás előtti
bájt-szintű körút-ellenőrzés**, eltérésnél megállás (minta:
`eszkozok/igazolas_migracio.py`). A `.gitattributes` szerint a `*.tsv` LF-es —
ez nem változhat.

---

### Tétel G1 — `general.py` váza

Egyetlen szkript, `eszkozok/general.py`. Kötelező elemei, sorrendben:

1. Docstring.
2. Importblokk.
3. **stdout ÉS stderr őr, az importok után** (`CLAUDE.md`, „Shell" szakasz,
   `e253c2a`). Az F4-0 E tétele pontosan ezt zárta le — ne kezdődjön újra.
4. **`argparse` + `if __name__ == "__main__":` őr.** Ez itt nem stílus, hanem
   adatvédelem: a `NYITOTT_FELADATOK.md` szerint ma 10 `eszkozok/*.py`-nak
   egyik sincs, és közülük 8 modulszinten fájlt ír — az F4-0 füstteszt
   ténylegesen felülírt két kanonikus táblát ezen a módon. A `general.py`-nak
   **soha nem szabad írnia, ha nem kapott explicit `--ir` kapcsolót.**

TSV-olvasás kizárólag `split('\t')`-vel, írás `'\t'.join()`-nal
(`CLAUDE.md`, „TSV-olvasás"). A `csv` modul importja is tilos.

CLI:

```
python eszkozok/general.py --cel {naplo,index,naplok,study,nyitott,mind}
                           [--id ID]
                           [--kimenet DIR]      # alapértelmezés: generalt_proba/
                           [--ir]               # csak ezzel ír éles fájlba
                           [--ellenoriz]        # nem ír; diffel, és 1-gyel lép ki eltérésnél
```

**Fejléc minden generált kimeneten**, a terv 1.C szerint:

```
<!-- GENERÁLT: general.py --cel naplo | forrás: adat/motivumok.tsv, adat/elofordulasok.tsv | ts=2026-09-14 -->
```

Marker-blokk (G0/a), vegyes fájlban — a hatókör-sorral együtt:

```
<!-- GENERÁLT-KEZDET: general.py --cel naplo#attekintes | forrás: … | ts=… -->

*Ez a blokk a 7 betöltött motívum-ID-t fedi; a fájl további 83 tétele kézi.*

…
<!-- GENERÁLT-VÉGE: naplo#attekintes -->
```

A hatókör-sor **számai is a tábláról jöjjenek** (betöltött ID-k száma, illetve a
blokkon kívüli tételek száma), ne legyenek beégetve — különben az első
`HAMART-001`-betöltéskor hazudni kezd.

**Sorvég-szabály.** A `.gitattributes` ma csak a `*.tsv`-t köti LF-re. A
generátor minden `.md` kimenetnél **olvassa ki a célfájl mai domináns sorvégét,
és azzal írjon** — ne egységesítsen. Fájlonként mérje meg a CRLF/LF arányt írás
előtt és után, és tegye a jelentésbe (ugyanaz a fegyelem, mint az F4-0 D
tételénél).

**Idézőjel-szabály.** A `kapcsolodas` mező tartalma **karakterhűen** kerül a
kimenetbe: a 79 nyitó idézőjel nem hagyható el és nem cserélhető tipográfiai
idézőjelre. Ez a G-fázis egyik elfogadási kritériuma (K6).

---

### Tétel G2 — a forrásréteg leválasztása *(7 fájl)*

A `motivumok/[ID].md` létrehozása a hét betöltött ID-re. Tartalma **kizárólag
az, ami ma a naplóban áll, és nem vezethető le a tábláról**:

- a ⚠️-viták nevesített képviselőkkel,
- a kizárások/elhatárolások indoklása,
- a kiegészítő szótartalmi jegyzetek,
- a nevesített tanítói alkalmazás és a gap-jelzések,
- a `【NAPLO: …】` blokkok.

**Módszertani kötelezettség.** A kivágás **pontos old/new szövegblokkokkal**
történjen, soha nem „a következő `##` fejlécig" alakú utasítással — ez a
mintázat korábban dokumentáltan vezetett záró tartalom elvesztéséhez. Minden
átvitt blokkra: bájt-szintű összevetés a forrás és a cél között, és a napló
eredeti szövegéből csak akkor kerül ki a blokk, ha a cél-fájlban igazoltan
megvan.

Ez a tétel **Opus-munka** — tartalmi ítélet, nem mechanikus csere.

---

### Tétel G3 — `PaRDeS_motivumok.md` generált szakaszai

Négy renderelő, mindegyik önálló marker-blokk:

| blokk | forrás | tartalom |
|---|---|---|
| `naplo#attekintes` | `motivumok` + `elofordulasok` | a 7 ID tétele, `tema` szerint csoportosítva, `cim` + **`N fő előfordulás / M igehely-sor`** + státusz |
| `naplo#kuszob` | `motivumok` + `elofordulasok` | a 7 ID fejsora (`statusz`, `statusz_verzio`, `statusz_datum`, a **fő előfordulás** száma); a bekezdés-próza a `motivumok/[ID].md`-ből fűződik hozzá |
| `naplo#kulcsszo_index` | `motivumok` + `elofordulasok` | 7 sor: kulcsszó (`ui_cimke`), téma, ÓSZ/ÚSZ-irány, **fő előfordulás**, igehelyek |

A ⭐ küszöb-blokk kizárólag a `COUNT(DISTINCT fo_elofordulas)` értéket számolja —
ez az egyetlen szám, amelyre a „3+ előfordulás" szabály értelmesen alkalmazható.

**Rendezés — kötelező, és az 1. menetben nem teljesült (K13).** Minden
igehely-lista és minden könyv-csoport **kanonikus sorrendben** álljon, nem
tábla-sorrendben és nem ábécében. A sorrend forrása a
`konkordancia/Konyv_normalizalo_tabla.tsv`: **a fájl sorrendje maga a kanonikus
sorrend** (nincs benne külön sorszám-oszlop, a sorindex a kulcs). Könyvön belül
fejezet, majd vers szerint **numerikusan** (a `18:24` a `2:6` után áll ma — ez
hibás). Tartomány (`9:1-2`, `7:1-28`) a kezdő fejezet/vers szerint rendezendő.

**A Kulcsszó-index igehely-oszlopa a fő előfordulásokat hozza**, ne a teljes
listát: az 1. menet kimenetében az ALVIL-001 sora 72 igehelyet zsúfolt egy
cellába, ami olvashatatlan, és nem is az, amit a mai kulcsszó-index ad. A teljes
lista helye a könyv-index. (A generált *index* már így működik, és jól olvasható
— ez a minta.)
| `naplo#konyv_index` | `elofordulasok` | könyv szerinti bontás, mind a 201 sorból |

Amit **nem** generál: az `Előrejelzett motívumok` táblát (nincs forrásmezője) és
a `Kulcsszavak részletesen` szakaszt (a G2 után az `motivumok/[ID].md`-ből
*beolvasztás*, nem generálás — a tartalom emberi).

Két mérendő ütközés, amit a renderelőnek jelentenie kell, nem elsimítania:

- **`HODIT-001` témája a táblában `Teremtéstan`**, a naplóban a *Hamartológia*
  csoport alatt, a „Isten fiai/Nefilim" bejegyzés alpontjaként áll. A generált
  áttekintés áthelyezné. Ez adathiba vagy naplóhiba — döntendő, nem elfedendő.
- **Az ALVIL-001 fő-előfordulás-száma**: a napló 4-et, az index 6-ot mond. A
  G0/d 1. tétele ezt felszínre hozza; a renderelő innentől azt látja, amit a
  `fo_elofordulas` mező mond, és ha az ellentmond a kézi szövegnek, jelentse.

(A `Pshat`/`Peshat` eltérés itt már nem jelenik meg — a G0/d 3. tétele a
táblában javítja.)

---

### Tétel G4 — `Lezart_tematikus_tanulmanyok_index.md`

Generálható: `#`, Motívum, Fájlnév, Érintett igehelyek. **Nem generálható: a
`Megjegyzés` oszlop.**

Két következmény:

- A `Megjegyzés` oszlop tartalma a `motivumok/[ID].md`-be tartozik (G2), és a
  generált táblába onnan fűződik be — vagy az oszlop a marker-blokkon kívül
  marad. **Javaslat: az utóbbi**, mert az index megjegyzései tanulmányok közti
  elhatárolásokat írnak le, nem egy motívum saját jegyzeteit.
- **A `#` oszlop nem hivatkozási alap (D12).** Az 1. menet kimenete ID-ábécé
  szerint számoz, tehát a mai #1 (Tehóm) ott #7. A kézzel írt `Megjegyzés`
  oszlop viszont — ami a blokkon **kívül** marad — szövegesen hivatkozik
  sorszámokra („l. #2", „a fenti táblázat #8 tétele"): az élesítés így
  elszakítaná a hivatkozásokat a soroktól. A `#` ezért **puszta vizuális
  számláló**, és a prózai hivatkozások `[ID: …]`-ra írandók át — **a G7
  élesítés előfeltétele**, nem utómunka.
- **A generált index 7 soros lesz, a mai 8 helyett** — a `HAMART-001` hiányzik
  a tábláról. A generátor ezt **explicit hiányként jelentse** (kilépési kód 1,
  `--ellenoriz` módban), ne csendben hagyja ki a sort.

---

### Tétel G5 — kereszthivatkozás-naplók

`[könyv-mappa]/naplok/[motívum]_kereszthivatkozas_naplo.md`, a `jeloltek.tsv`-ből.
A sablon előírta szerkezet: vizsgált kulcsszavak → nyers találatok forrásonként
→ **tartalmi minősítés MINDEN jelöltre** → végső döntés és indoklás → összegzés.

Ebből ma a táblából levezethető: a `forras_kereses` (7 különböző érték adja a
„források" bontást), a `dontes` + `indoklas` (a minősítő táblázat), a `datum`.
Nem vezethető le: a vizsgált kulcsszavak Strong-listája (részben pótolható a
`gerinc_elem`-ből) és a named-teacher gap-jelzés.

**A kritikus pont:** a `jeloltek.tsv` ma **17 nyitott és 3 elutasított** sort
tartalmaz összesen, három ID-hez. A meglévő hét napló ennél lényegesen több
elutasítást és elhatárolást dokumentál. **A generált napló tehát nem
helyettesítheti a meglévőt** — a kimenet a `generalt_proba/` alá megy, és a
diff a bemenete annak a döntésnek, hogy mely elutasítás-sorokat kell
visszamenőleg felvenni a `jeloltek.tsv`-be. Ez a G-fázis legfontosabb
mellékterméke: **a napló-generátor első futása egy hiánylista.**

---

### Tétel G6 — tematikus study 1. pont

A sablon v15 hét oszlopa: Igehely | Kapcsolódás | PaRDeS-szint, ahol felmerült |
Strong-szám(ok) | BDB-entry-id | Sense-szám | Jelentés-szöveg (EN + HU).

Leképezés: `igehely`, `kapcsolodas`, `pardes_szint`, `strong`, `bdb_entry_id`,
`jelentes_szam`, `jelentes_en` + `jelentes_hu`. Az utolsó négy oszlop 4-13 %-ban
kitöltött — a sablon ezt engedi (`—`), de az oszlop nem hagyható el.

**Egy séma-hiány, ami itt derül ki.** A harmadik oszlop fejléce *„PaRDeS-szint,
ahol felmerült"*, és a mai study-k ki is töltik: `Peshat/Remez — 1Mózes 1
bővített tanulmány`. Az `elofordulasok.tsv` csak a szintet tárolja. **Eldöntve
(D6): új mező, `felmerult_tanulmany`** — additív, visszafelé kompatibilis;
felvétele és kitöltése a G0/d 2. tétele. Enélkül a generált táblázat minden
sorból elvesz egy információt.

**Hatókör-figyelmeztetés:** a mai Tehóm-study 1. pontja 5 soros, a tábla 41-et
ismer ehhez az ID-hez (a többi a study 2/b pontjában él). A generált 1. pont
tehát **nemcsak formátumot vált, hanem a study szerkezetét is átrendezi**. Ez a
G-fázis legnagyobb tartalmi kockázata — ezért megy a `generalt_proba/` alá, és
ezért nem része a G7 élesítésnek egyik study sem, amíg a diffet valaki soronként
át nem nézte.

---

### Tétel G7 — élesítés

Csak azokra a kimenetekre, amelyeknek a diffjét a chat-menet jóváhagyta. Tétele
kimenetenként külön commit. **A study-fájlok (G6) alapértelmezésben NEM
élesíthetők ebben a fázisban.**

A `NYITOTT_FELADATOK.md`-ből egyetlen blokk generálódik — a nyitott jelöltek
(17 sor) és a motívum-státuszok (7 sor) táblája —, marker közé, a fájl többi
része érintetlen. A fájl hiányzó ATX-fejléceinek pótlása **nem** ennek a tételnek
a része, de a jelentésben szerepeljen.

---

## 3. Elfogadási kritériumok

| # | kritérium | mérés |
|---|---|---|
| **K1** | `general.py` `py_compile`-ra hibátlan, és az `import_sorrend_ellenoriz.py` 0-val lép ki | a két meglévő eszköz futtatása |
| **K2** | stdout **és** stderr őr megvan, az importblokk **után** | grep |
| **K3** | `argparse` és `if __name__ == "__main__":` őr megvan; `python eszkozok/general.py` argumentum nélkül **nem ír egyetlen fájlt sem** | `git status` a futtatás után: tiszta |
| **K4** | a `csv` modul sehol nincs importálva a `general.py`-ban | grep |
| **K5** | `--ir` nélkül futtatva a kimenet kizárólag a `--kimenet` könyvtár alá kerül | `git status` a futtatás után: csak `generalt_proba/` új |
| **K6** | a `kapcsolodas` **79 nyitó idézőjele** karakterhűen megjelenik a próba-kimenetben | a próba-kimenet grepje: 79 találat |
| **K7** | a próba-kimenet sorvége fájlonként megegyezik a célfájl mai domináns sorvégével | CRLF/LF arány mérése |
| **K8** | a generált index a `HAMART-001` hiányát **explicit hibaként** jelenti, nem hallgatja el | `--ellenoriz` kilépési kód 1 + a hiányzó ID neve a kimeneten |
| **K9** | a napló-generátor első futása előállítja a **hiánylistát**: mely elutasítás/gap-tétel van a meglévő hét naplóban, de nincs a `jeloltek.tsv`-ben | TSV-riport a `naplok/` alá |
| **K10** | a G2 után a hét `motivumok/[ID].md` együttes tartalma bájtra lefedi a naplóból kivett blokkokat | összevetés, eltérésnél megállás |
| **K11** | a G0/d három tábla-írása után az `elofordulasok.tsv` **201 adatsora és minden korábbi mezőértéke változatlan**; csak két új oszlop és a 14 `Pshat` javítása tér el | `git diff` soronkénti elemzése; a 79 nyitó idézőjel továbbra is 79 |
| **K12** | minden generált blokk tartalmaz hatókör-sort, és annak számai a tábláról jönnek | a próba-kimenet grepje; `HAMART-001` fiktív felvételével a szám 7→8-ra vált |
| **K12'** | a hatókör-sor **számlálója és nevezője azonos granularitású** | az 1. menet „84 tételt sorol fel, ebből 77" sora hibás: 84 = csak felső szintű bullet, 7 = minden betöltött ID, de a HODIT-001 **alpont**. Helyes: 84 felső szint → 78 hiányzik, **vagy** 90 tétel (84 + 6 alpont) → 83 hiányzik. A kettő nem keverhető |
| **K13** | minden igehely-lista és könyv-csoport **kanonikus sorrendben** áll | a könyv-index első öt könyve `1Móz, 2Móz, 3Móz, 4Móz, 5Móz` legyen, ne `1Kir, 1Krón, 1Móz, 1Sám, 2Kir`; könyvön belül `1Kir 2:6` előzze meg a `1Kir 18:24`-et |
| **K14** | a Kulcsszó-index igehely-oszlopa a **fő előfordulásokat** hozza, nem a teljes listát | az ALVIL-001 sor legfeljebb 6 tételt soroljon, ne 72-t |
| **K9'** | a hiánylista **két blokkra bontva**: a hat betöltött ID tényleges hiányai, külön a `HAMART-001` soraitól | a mai 56 sorból 32 a HAMART-001-é (a teljes ID hiányzik a `jeloltek.tsv`-ből) — ez egyetlen ismert F3-hiány következménye, nem 32 önálló lelet; a valódi lista **24 sor** |
| **K15** | az `elofordulasok.tsv` **egységes igehely-alakot** használ (`Mt`, `Luk`, `Róm`, `Jel`), és a `KONYV_ALIAS` ezután **üres** | 13 sor javítandó (8 × `Jelenések`, 3 × `Lukács`, 1 × `Róma`, 1 × `Máté`); utána egyetlen könyvnév sem fordul elő két alakban, és az alias nélkül is 0 a `hianyzo_konyvek` |

### 3.1 A terv elfogadási tesztje helyére

> **Új teszt.** A `--ellenoriz` mód a **generált blokkokra** fut, nem a teljes
> fájlra. Egy blokk akkor zöld, ha a generátor kimenete **karakterre azonos** a
> fájlban álló marker-blokk tartalmával. A blokkon kívüli kézi tartalom nem
> része a tesztnek.
>
> Az **első** futásnál ez definíció szerint piros lesz minden blokkon, mert még
> nincs marker a fájlokban. A G7 élesítés az, ami zöldre viszi — és onnantól
> minden későbbi futásnak zöldnek kell maradnia, amíg a tábla nem változik.
>
> A terv eredeti tesztje (a teljes `PaRDeS_motivumok.md` diffje) ehelyett
> **mérésként** marad meg, nem kapuként: a próba-kimenet és a mai fájl diffje a
> G0/a döntés bemenete, és a diff nagysága (83 hiányzó tétel) az, amit a döntés
> megmagyaráz.

---

## 4. Commit és push

`CLAUDE.md` szerint: munkaág `main`, magyar üzenet, tétel-azonosítóval kezdve,
**tétel-szintű granularitás**, UTF-8 fájlból (`git commit -F uzenet.txt`), soha
nem inline `-m`-mel.

```
F4.0e: séma-kiegészítés és adat-előkészítés (fo_elofordulas, felmerult_tanulmany, Pshat→Peshat)
F4.1:  general.py váza — argparse, __main__ őr, stdout/stderr, split('\t') I/O
F4.2:  general.py — motívumnapló és index renderelők, próba-kimenettel
F4.2a: a renderelők kanonikus rendezése, a hatókör-sor granularitása, a kulcsszó-index szűkítése
F4.3:  general.py — kereszthivatkozás-napló és study-1.-pont renderelők
F4.3a: egységes igehely-alak a táblában (13 sor), a KONYV_ALIAS kiürítése, a hiánylista kettéosztása
F4.4:  a motívum-forrásréteg leválasztása (motivumok/[ID].md, 7 fájl)
F4.5:  a generált blokkok élesítése a napló és az index fájlban
```

Push `origin main` ugyanabban a menetben, amelyikben a commitok születtek — nem
külön kérésre várva. Push előtt `git status` tiszta, és `git log --oneline -5`
a jelentésbe.

---

## 5. Amit ez a brief szándékosan nem kér

- **Nem kéri a `HAMART-001` betöltését.** 46 táblázat-sor, tartalmi kinyerés —
  ez F3-munka, saját menettel. Ide csak az tartozik, hogy a generátor
  *jelentse* a hiányt (K8).
- **Nem kéri a 76 ID nélküli motívum ID-kiosztását.** L. G0/a; ez az F3
  kiterjesztése.
- **Nem kéri a `konkordancia/Karoli_Strong_kivonat.tsv` generátorba emelését.**
  A terv 1.C ezt `elofordulasok`-ból generált nézetnek mondja, ma viszont a
  `merge_karoli_szofaj.py` állítja elő a `Strong_szotar.tsv`-ből. A két
  meghatározás kizárja egymást. Előbb döntés, aztán kód — és a 32 soros drift
  (F4.0d) is ennek a döntésnek a bemenete.
- **Nem kéri a hookok felállítását.** A terv 2. pontja három hookot ír le
  (`ellenoriz.py --all` commit előtt, proveniencia-ellenőrzés íráskor,
  `general.py` tábla-írás után). Az utolsó **kifejezetten veszélyes addig, amíg
  a G7 élesítés nem futott le** minden kimenetre: egy tábla-írás után
  automatikusan induló generátor felülírná a még jóvá nem hagyott blokkokat.
  A hookok az F5 után jöjjenek.
- **Nem kéri a study-fájlok átírását.** A G6 renderelője elkészül, a kimenete a
  `generalt_proba/` alá kerül, az élesítés külön döntés.

---

## 6. Futtatási rend és modellválasztás

### 6.1 Tételenkénti modelljavaslat

| tétel | a munka jellege | modell | indok |
|---|---|---|---|
| **G0/d** adat-előkészítés | két oszlop felvétele, ~22 sor megjelölése, 14 sor javítása | **Sonnet** | átvezetés a napló meglévő szövegéből; a körút-ellenőrzés és a K11 zárja. Ütközésnél (ALVIL-001) megáll, nem dönt |
| **G1** váz | argparse, I/O, marker-kezelés, sorvég-megtartás | **Sonnet** | mechanikus; a K1-K5 egyértelműen zárja |
| **G3, G4** renderelők | tábla → markdown, csoportosítás, összefűzés | **Sonnet** | a helyesség mérhető: a kimenet a tábla determinisztikus képe |
| **G5, G6** renderelők | ugyanaz, de a hiánylista tartalmi ítéletet készít elő | **Sonnet** | a szkript írja a listát, a döntést a chat-menet hozza |
| **G2** forrásréteg | próza szétvágása, blokkhatárok megítélése | **Opus** | tartalmi ítélet; a hibája visszafordíthatatlan tartalomvesztés |
| **G7** élesítés | marker-blokkok beírása éles fájlokba | **Opus** | irreverzibilis írás kézzel írt fájlokba |

### 6.2 Menetbeosztás

Három menet, egymás után — párhuzamos Code-menet ugyanazon az ágon tilos.

| menet | tételek | modell | commit | állapot |
|---|---|---|---|---|
| 1. | **G0/d**, majd G1, G3, G4 + próba-kimenet | Sonnet | `F4.0e`, `F4.1`, `F4.2` | ✅ **lefutott, `8febf2a`**, független ellenőrzésen átment (§1.5) |
| 2. | a K12'/K13/K14 javítása, majd G5, G6 + a hiánylista | Sonnet | `F4.2a`, `F4.3` | ✅ **lefutott, `a7d23a6`**, független ellenőrzésen átment (§1.6) |
| 3. | **K15/K9'**, majd G2, majd a D12 hivatkozás-migráció, majd G7 | **Opus** | `F4.3a`, `F4.4`, `F4.5` | következő |

A K15 (13 sor javítása) és a K9' (a hiánylista kettéosztása) mechanikus, tehát
önmagában Sonnet-munka volna — de egy külön menet többe kerülne, mint amennyit
megspórol, ezért a 3. menet első tételeként megy. Sorrendben előre, mert a G2 és
a G7 már a javított táblára épül.

A terv kettőt szánt az F4-re. A harmadik onnan jön, hogy a G2 és a G7 más
modellt kíván, mint a renderelők, és a menethatár az egyetlen hely, ahol modellt
lehet váltani. A 3. menet rövid (7 fájl szétvágása + két fájl blokkjainak
beírása).

**A G0/a-c döntés megszületett** (2026-09-14, l. döntésnapló); a G0/d az 1.
menet első tétele, mert a renderelők a két új mezőre épülnek.

### 6.3 Az 1. menet nyitó promptja

```
Olvasd el az F4_GENERATOR_BRIEF.md-t, a CLAUDE.md „TSV-olvasás" és „Shell"
szakaszát, és az adat/SEMA.md 2.1-2.2 pontját.

Ebben a menetben a G0/d, a G1, a G3 és a G4 tétel megy, ebben a sorrendben.

ELŐSZÖR G0/d (brief 2. pont, „Tétel G0", G0/d szakasz) — adat-előkészítés:
 - fo_elofordulas (igen/nem) és felmerult_tanulmany mező felvétele az
   adat/elofordulasok.tsv-be ÉS az adat/SEMA.md 2.2 pontjába;
 - a fo_elofordulas kitöltése a PaRDeS_motivumok.md mai szövege alapján
   (kb. 22 sor kap igen-t); ahol a napló és a
   Lezart_tematikus_tanulmanyok_index.md eltér — ALVIL-001: 4 vs 6 —,
   ÁLLJ MEG és jelentsd, ne válassz;
 - felmerult_tanulmany kitöltése a study-k 1. pontjának 3. oszlopából,
   ahol van; máshol üres;
 - pardes_szint: a 14 „Pshat" javítása „Peshat"-ra. A 35 üres marad üres.
 - írás előtt bájt-szintű körút-ellenőrzés, eltérésnél megállás
   (minta: eszkozok/igazolas_migracio.py). A tábla LF-es marad.
Commit: F4.0e.

UTÁNA G1 — eszkozok/general.py váza:
 - docstring, importblokk, UTÁNA stdout ÉS stderr őr;
 - argparse + if __name__ == "__main__": őr — ez kötelező, nem opcionális;
 - --ir kapcsoló nélkül a szkript SOHA nem ír éles fájlba, csak a
   --kimenet könyvtárba (alapértelmezés: generalt_proba/);
 - TSV-olvasás split('\t'), írás '\t'.join(); a csv modult importálni sem
   szabad;
 - minden .md kimenetnél a célfájl mai domináns sorvégével írj.
Commit: F4.1.

G3 és G4 — a négy napló-blokk és az index renderelője, a brief 2. pontja
szerint. A kimenet a generalt_proba/ alá megy, éles fájlt NEM módosítasz.
Minden blokk kapjon hatókör-sort, tábláról vett számokkal (K12).
Az előfordulás-szám alakja: „N fő előfordulás / M igehely-sor"; a ⭐ blokk
csak a fo_elofordulas='igen' sorokat számolja.
A HODIT-001 téma-ütközését jelentsd, ne simítsd el.
A generált index a HAMART-001 hiányát explicit hibaként jelezze.
Commit: F4.2.

A commit-üzeneteket UTF-8 fájlból add át (git commit -F). A három commit után
push origin main, ugyanebben a menetben.

A jelentésbe kerüljön: a K1-K8, a K11 és a K12 mért értéke, a G0/d után a
`git diff --stat` az adat/ alatt, a generalt_proba/ alatti fájlok listája
mérettel, a `git status` a futtatások után (tisztának kell lennie a
generalt_proba/-n kívül), és a git log --oneline -5.
```

### 6.4 A 2. menet nyitó promptja

```
Olvasd el az F4_GENERATOR_BRIEF.md G3, G5 és G6 tételét, a §3 K12'/K13/K14
kritériumokat, valamint a sablonok/4_PaRDeS_tematikus_sablon.md 1. pontját
(„Kötelező napló" bekezdés és a hétoszlopos táblázat).

ELŐSZÖR a meglévő renderelők három hibáját javítsd (commit: F4.2a) — az 1.
menet próba-kimenete ezeket hozta felszínre, és a G5/G6 ugyanerre az I/O-ra
épül, tehát előbb kell rendben lennie:

 K13 — KANONIKUS RENDEZÉS. Ma minden igehely-lista tábla-sorrendű, a
   könyv-index pedig ábécében áll (1Kir, 1Krón, 1Móz, 1Sám, 2Kir, 2Móz,
   2Sám, 4Móz, 5Móz, Ez...). A sorrend forrása a
   konkordancia/Konyv_normalizalo_tabla.tsv: A FÁJL SORRENDJE maga a
   kanonikus sorrend (nincs benne sorszám-oszlop, a sorindex a kulcs).
   Könyvön belül fejezet, majd vers szerint NUMERIKUSAN — ma az
   1Kir 18:24 megelőzi az 1Kir 2:6-ot, ez hibás. Tartomány (9:1-2,
   7:1-28) a kezdő fejezet/vers szerint rendezendő. A táblában szereplő,
   de a normalizáló táblában nem található könyvnevet jelentsd, ne
   rendezd a lista végére némán.

 K12' — A HATÓKÖR-SOR GRANULARITÁSA. A naplo#attekintes sora ma azt írja:
   „84 tételt sorol fel, ebből 77 még nincs a táblában". Mérve: a
   Tematikus áttekintés 84 felső szintű bullet + 6 alpont, és a hét
   betöltött ID-ből HAT felső szintű, a HODIT-001 (Rafeusok) ALPONT.
   A számláló és a nevező tehát két különböző granularitás. Válassz
   egyet és tartsd következetesen: 84 felső szint -> 78 hiányzik, VAGY
   90 tétel -> 83 hiányzik. Írd a kódba, melyiket számolod.

 K14 — A KULCSSZÓ-INDEX igehely-oszlopa a FŐ ELŐFORDULÁSOKAT hozza
   (COUNT(DISTINCT fo_elofordulas) tételeit), ne a teljes listát: az
   ALVIL-001 sora ma 72 igehelyet zsúfol egy cellába. A teljes lista
   marad a könyv-indexben. Minta: a generált index Érintett igehelyek
   oszlopa már így működik.

UTÁNA a G5 és a G6 renderelő, szintén csak generalt_proba/ kimenettel.

G5 mellékterméke kötelező: naplok/F4_naplo_hianylista.tsv — soronként egy
olyan elutasítás/elhatárolás/gap-tétel, amely a tematikus_lezart/naplok/ alatti
hét meglévő naplóban dokumentálva van, de a adat/jeloltek.tsv-ben nincs sora.
Oszlopok: id, jelolt, tipus (elutasitva|gap|elhatarolas), forras_naplo, indoklas.

G6-nál a hétoszlopos táblázat generálódik; a hiányzó BDB-mezők helyén „—" áll.
A harmadik oszlop a pardes_szint + felmerult_tanulmany összefűzése (a mezőket
az előző menet G0/d tétele vette fel); ahol a felmerult_tanulmany üres, csak a
szint áll ott — ne pótold találgatással.

Commit: F4.2a (a három javítás), majd F4.3 (G5+G6), mindkettő UTF-8
üzenetfájlból, majd push origin main ugyanebben a menetben.

A jelentésbe kerüljön: a K12', a K13 és a K14 mért eredménye (a K13-hoz a
könyv-index első öt könyve szó szerint), a K9, és ID-nként a próba-kimenet
sorszáma a mai study-k 1. pontjának sorszámához hasonlítva.
```

### 6.5 A 3. menet nyitó promptja *(Opus)*

```
Olvasd el az F4_GENERATOR_BRIEF.md §1.6-ot, a K15/K9' kritériumot, valamint a
G2 és G7 tételét.

ELŐSZÖR K15 + K9' (commit: F4.3a) — a G2 és a G7 már a javított táblára épül:

 K15 — EGYSÉGES IGEHELY-ALAK A TÁBLÁBAN. Az adat/elofordulasok.tsv 13 sora
   hosszú könyvnevet használ: 8 x "Jelenések" -> "Jel", 3 x "Lukács" -> "Luk",
   1 x "Róma" -> "Róm", 1 x "Máté" -> "Mt". A célalakot a
   konkordancia/Konyv_normalizalo_tabla.tsv "Magyar rövidítés" oszlopa adja
   (a CLAUDE.md házi alakja ugyanez: "Mt 24:38"). Ma a Luk/Lukács és a
   Róm/Róma egyszerre él ugyanabban a táblában, a tábla kulcsa viszont
   id + igehely — tehát két kulcs.
   Írás előtt bájt-szintű körút-ellenőrzés, eltérésnél megállás; a tábla LF
   marad; a 201 sor és minden más mezőérték változatlan.
   UTÁNA a general.py KONYV_ALIAS szótára KIÜRÜL (vagy jelentő őrként marad,
   amely NEM javít), és a --cel mind újrafuttatva a hianyzo_konyvek továbbra
   is 0 kell legyen. Ez a bizonyíték, hogy a javítás a táblában történt meg.

   NE nyúlj a fo_elofordulas csoportkulcsokhoz: azok a napló saját szövegének
   idézetei (pl. "Luk 10:15/Mát 11:23"), nem igehely-kulcsok — a "Mát" ott
   szándékos, l. D10.

 K9' — a hiánylista KÉT BLOKKRA bontva: a hat betöltött ID tényleges hiányai
   (24 sor), külön a HAMART-001 32 sorától, amely egyetlen ismert F3-hiány
   következménye, nem 32 önálló lelet. A blokkhatár a fájlban is látszódjon.

UTÁNA G2 — a motivumok/[ID].md forrásréteg létrehozása a hét betöltött ID-re, a
motivumlog/PaRDeS_motivumok.md prózájából.

KÖTELEZŐ MÓDSZER: minden kivágás pontos, teljes old/new szövegblokkal
történik. „A következő ## fejlécig" típusú utasítás tilos — ez korábban
dokumentáltan vezetett záró tartalom elvesztéséhez. Blokkonként: a cél-fájlban
igazold a meglétét, és csak azután vedd ki a naplóból.
Commit: F4.4.

A G2 UTÁN, AZ ÉLESÍTÉS ELŐTT: D12 — a Lezart_tematikus_tanulmanyok_index.md
Megjegyzés oszlopában minden „#N" alakú hivatkozás írandó át „[ID: …]"-ra
(ma pl. „l. #2", „a fenti táblázat #8 tétele"). A generált # oszlop puszta
vizuális számláló, amely minden ID-felvételkor átszámozódik — élesítés után
a rá hivatkozó próza rossz sorra mutatna. Commit ugyanabban a tételben.

G7 — a jóváhagyott blokkok élesítése a motivumlog/PaRDeS_motivumok.md és a
Lezart_tematikus_tanulmanyok_index.md fájlban, marker-párok közé. Study-fájlt
NEM élesítesz. Élesítés után futtasd a --ellenoriz módot: minden élesített
blokknak zöldnek kell lennie.
Commit: F4.5, UTF-8 üzenetfájlból, majd push origin main.

A jelentésbe kerüljön: a K15 (a 13 javított sor, és hogy KONYV_ALIAS nélkül is
0 a hianyzo_konyvek), a K9' (24 + 32 blokk), a K10, a --ellenoriz kimenete
blokkonként, és a sorvég-mérés élesítés előtt/után.
```

### 6.6 A menetek közé

Minden menet után a jelentés jöjjön vissza a chat-menetbe ellenőrzésre, mielőtt
a következő elindul. **Az 1. menet próba-kimenete a legfontosabb kapu**: a
napló-diff nagysága ott derül ki, és a G0/a döntés csak annak ismeretében
véglegesíthető.

---

## Döntésnapló

| # | Döntés | Indok | Ki döntötte |
|---|---|---|---|
| D1 | A generátor alapértelmezésben `generalt_proba/` alá termel; élesítés külön tétel | a §1.3 három rése miatt az első kimenet biztosan eltér; a diff a döntés bemenete, nem hiba | chat-menet javaslata, 2026-09-14 |
| D2 | Marker-alapú részleges generálás vegyes fájlokban; a tiltás blokk-szintű, és minden blokk hatókör-sort kap | 7 ID / 90 napló-tétel mellett a teljes fájl generálása 83 tételt semmisítene meg — és a napló a teljes ID-zés után is vegyes fájl marad, tehát a marker végleges, nem átmeneti | **felhasználó, 2026-09-14 (G0/a)** |
| D3 | ~~A generált szakasz a tábla sorszámát mutatja, a „fő előfordulás" a forrásfájlba kerül~~ → **visszavonva.** Helyette: **két szám, mindkettő a tábláról** (`N fő előfordulás / M igehely-sor`), új `fo_elofordulas` mezővel | a puszta sorszám kiütötte volna a ⭐ küszöbszabályt (72 > 3 minden motívumnál); így a szabály először válik gépileg ellenőrizhetővé, és az ALVIL-001 4↔6 ellentmondás is felszínre jön | **felhasználó, 2026-09-14 (G0/b)** |
| D4 | A forrásréteg neve `motivumok/[ID].md` | a terv 1.B így írja; a `motivumlog/` foglalt | **felhasználó, 2026-09-14 (G0/c)** |
| D5 | A `Pshat` → `Peshat` javítás a **táblában** történik, nem a renderelőben; a 35 üres `pardes_szint` marad üres | `CLAUDE.md`: ellentmondásnál a tábla az irányadó, tehát a tábla legyen helyes. Az üresek kitöltése tartalmi ítélet | chat-menet javaslata |
| D6 | Új mező: `elofordulasok.felmerult_tanulmany` | a sablon oszlopfejléce („ahol felmerült") ma nem képezhető le semmire | chat-menet javaslata |
| D7 | Az index `Megjegyzés` oszlopa a marker-blokkon kívül marad | tanulmányok közti elhatárolást ír le, nem egy motívum jegyzetét | chat-menet javaslata |
| D8 | A study-fájlok élesítése kimarad az F4-ből | a Tehóm-példa szerint az 1. pont 5 sorról 41-re nőne — szerkezeti átrendezés, nem formázás | chat-menet javaslata |
| D9 | A tábla-írás utáni `general.py` hook az F5 utánra marad | a G7 előtt automatikusan felülírná a jóvá nem hagyott blokkokat | chat-menet javaslata |
| D10 | Új mező: `elofordulasok.fo_elofordulas` — **csoportkulcs** (a napló saját igehely-megnevezése; üres = nem fő előfordulás), nem `igen`/`nem`. A ⭐ küszöb `COUNT(DISTINCT fo_elofordulas)` | a napló egyetlen fő előfordulásként nevez meg versközöket (`1Móz 6:1-4`, `Luk 1:46-47`), amit a tábla külön sorokra bont: logikai mezővel vagy a szám nő fel hamisan, vagy egy sor tűnik el indoklás nélkül. A csoportkulcs mindkettőt elkerüli, és visszamutat a napló szövegére | **felhasználó, 2026-09-14/15** |
| D11 | A `CLAUDE.md` réteg-táblázata két ponton javítandó: `motivumlog/[ID].md` → `motivumok/[ID].md`, és a generált-fájl-tiltás blokk-szintűvé pontosítva | a D2 és a D4 következménye; a szabályszöveg és a kód ne mondjon mást | chat-menet javaslata |
| D12 | A generált index `#` oszlopa **puszta vizuális számláló**, nem hivatkozási alap; a `Megjegyzés` próza `#N` hivatkozásai `[ID: …]`-ra írandók át, **a G7 élesítés előtt** | a `#` minden ID-felvételkor átszámozódik, a rá hivatkozó próza viszont a blokkon kívül, kézzel írva marad — az élesítés elszakítaná a hivatkozásokat a soroktól | chat-menet javaslata, 2026-09-15 |
| D13 | Az ALVIL-001 fő-előfordulás-száma **6**; a tagságra a napló ⭐-szakasza az irányadó, nem az index #2 sora | három hely mond 6-ot, köztük az index fejléce a dátumozott 4→6 javítással; az index sorából viszont hiányzik a `Jel 1:18`, miközben 6-ot állít | **felhasználó, 2026-09-15** |
| D14 | A könyvnév-normalizálás a **táblában** történik (13 sor), nem a renderelőben; a `KONYV_ALIAS` utána kiürül, vagy legfeljebb **jelentő** őrként marad, amely nem javít | ugyanaz az eset, mint a D5 (`Pshat`→`Peshat`): a `CLAUDE.md` szerint ellentmondásnál a tábla az irányadó. A tábla kulcsa `id + igehely`, tehát a két alak két kulcs — az alias csak a generátort javítja meg, a `gate.py`-t, a `lekerdez.py`-t és minden jövőbeli joint nem | **felhasználó, 2026-09-15** |

### Nyitott, a briefben szándékosan el nem döntött kérdések

1. **`HAMART-001` betöltése** — F3-munka, de az index 8. sora és a napló négy
   `[ID: HAMART-001]` hivatkozása addig lóg a levegőben.
2. **`Karoli_Strong_kivonat.tsv`** — a terv 1.C és a mai `merge_karoli_szofaj.py`
   két különböző forrást mond. A 32 soros drift (F4.0d) csak ezután dönthető el.
3. **A `NYITOTT_FELADATOK.md` hiányzó ATX-fejlécei** — mérve: a fájlban egyetlen
   `#` kezdetű fejléc sincs. Külön, apró tétel.

---

## Függelék — mezőnkénti forrás-leképezés

Amit a generátor **le tud** vezetni:

| kimenet-elem | forrás | megjegyzés |
|---|---|---|
| motívum címe | `motivumok.cim` | |
| kulcsszó-címke | `motivumok.ui_cimke` | |
| témacsoport | `motivumok.tema` | HODIT-001-nél ütközik a naplóval |
| státusz-jelölés | `motivumok.statusz` + `_verzio` + `_datum` | a mai „✅ LEZÁRVA" helyére |
| igehely-lista | `elofordulasok.igehely` | ID-re szűrve, kanonikus sorrendben |
| fő előfordulás száma | `COUNT(DISTINCT elofordulasok.fo_elofordulas)` | **új mező** (csoportkulcs), G0/d; a ⭐ küszöb ezt számolja |
| kanonikus könyv-sorrend | `konkordancia/Konyv_normalizalo_tabla.tsv` **sorrendje** | nincs sorszám-oszlop: a sorindex a kulcs (K13) |
| igehely-szám | `elofordulasok` sorszám | a fő szám mellett, nem helyette (D3) |
| „ahol felmerült" | `elofordulasok.felmerult_tanulmany` | **új mező**, G0/d |
| kapcsolódás-szöveg | `elofordulasok.kapcsolodas` | **79 nyitó idézőjel karakterhűen** |
| PaRDeS-szint | `elofordulasok.pardes_szint` | 35 üres, 14 `Pshat` |
| Strong / BDB / sense / jelentés | `elofordulasok.strong`, `bdb_entry_id`, `jelentes_szam`, `jelentes_en`, `jelentes_hu` | 4-13 % kitöltött, üresnél `—` |
| kapcsolat-típus, funkció | `kapcsolatok.tipus`, `.funkcio` | **csak 2 ID-hez van adat** |
| jelölt-minősítés | `jeloltek.dontes` + `.indoklas` + `.datum` | 221 sor |
| keresés-forrás bontás | `jeloltek.forras_kereses` | 7 különböző érték |
| fájlnév | `motivumok.forras_study` | ISTENTISZT-001-nél két érték, `;`-vel |

Amit **nem** tud levezetni, és ezért forrásrétegben kell maradnia:

⚠️-viták és képviselőik · kizárások indoklása · named-teacher találatok és
gapek · szótartalmi jegyzetek · `【NAPLO: …】` blokkok · az „Előrejelzett
motívumok" tábla · az index `Megjegyzés` oszlopa · a study 1. pontját követő
prózai bekezdések · a `NYITOTT_FELADATOK.md` négy nagy tétele.

*(A „hol merült fel" adat és a fő-előfordulás-szám a G0/d után már levezethető —
mindkettő átkerült a felső táblába.)*
