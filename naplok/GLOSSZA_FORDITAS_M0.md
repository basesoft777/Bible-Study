# GLOSSZA_FORDITAS — M0 napló (mérés, sor-választási szabály, kulcsséma, prompt, 30 szavas próba)

*F140 (#140) · M0 · 2026-10-25 · a session modellje: `claude-sonnet-5-5` (a brief `modell`: sonnet, egyezik) · állapot: **⛔ megállva, a felhasználó jóváhagyására vár***

Minden mért szám a `python eszkozok/glossza_forditas.py --m0` kimenete. Proveniencia: `scope=konkordancia/TBESH.txt H-sorai + konkordancia/Strong_szotar.tsv + konkordancia/TAHOT_kivonat.tsv | forras=helyi-futtatas | ts=2026-10-25`. A fordítási próbát (3. szakasz) ez a session írta, nem külső modell; a próba a prompt és a szabályok bemutatása, nem kész adat (az `adat/glosszak_heber_hu.tsv` még nem jött létre).

## 1. Mérés

| Mért érték | Szám |
|---|---|
| TBESH héber adatsor (`H` + 4 számjegy [+ betű]) | 11 682 |
| ebből a `Strong_szotar.tsv` 8 718 héber Strongjához tartozó sor | **11 677** |
| a szótárban nem szereplő alap (H9015–H9019: előtag/utótag-elemek) | 5 alap, 5 sor — kimarad a hatókörből |
| a szótár mind a 8 718 Strongjának van TBESH-sora | igen (0 hiány) |
| `entry_id` (a `dStrong` oszlop első szava, pl. `H2763A`) egyedi | 11 677 / 11 677 — alkalmas kulcsnak |
| 1 soros alap / több soros alap | 7 326 / 1 392 |
| kapcsolat nélküli sor (a `dStrong` oszlop `=` utáni része üres) | 9 579 |
| kapcsolt sor: `in Aramaic of` 581 · `a Meaning of` 477 · `a Name of` 429 · `a Spelling of` 283 · `a group of` 157 · `a Part of` 102 · `a form of` 31 · `combination of` 22 · `in Hebrew of` 16 | 2 098 |
| alap, amelynek **nincs** kapcsolat nélküli sora | 1 097 (ezek többsége az arám szó: `H0576A` `in Aramaic of` „me”; vagy a névhez kötött `H0430G` `a Name of` „God”) |
| alap, amelynek több kapcsolat nélküli sora van (homonima, vagy név-változatok) | 1 010 |
| glossza hossza (mind a 11 677 sorra / a 10 676 kapcsolat nélküli+fő sorra) | max. 33 karakter; 76 437 karakter (10 676 sor) |
| a definíció első 200 karaktere (10 676 sor) | 1 214 571 karakter ≈ 0,4 M token bemenet |
| glossza zárójeles/szögletes 133 · perjeles (`a/b`) 52 · 2-nél több szavas 268 | — |
| a glossza-formák: „szó: árnyalat” kettősponttal a TBESH-ban jellemző (`land: soil`, `house: home`, `to come (in): come`) | — |

**Fontos megfigyelés (a brief feltevését módosítja).** A brief a „névhez kapcsolt alsorokat” (`= a Part of` / `= a Name of`) tartja kimaradónak. A mérés szerint három dolog árnyalja:

1. A **fő glossza nem mindig a „kapcsolat nélküli” sor**: a H0430-nak (`Isten`) nincs kapcsolat nélküli sora (a fő sor `H0430G` `= a Name of`, „God”), 1 097 alapnál így van — ezeknél az 1. sor (vagy az első nem „gyenge” kapcsolatú) a fő glossza.
2. Egy alapon belül **kapcsolat nélküli, de nem fő sorok** is vannak: névtöredékek (`H1004G` „Beth-(ashbea)”, `H1004J` „House (of the Forest)”), más személyek azonos névvel (`H5971G` „Ammi”), vagy a fő sor *után* álló szó (`H0410H` „El (Berith)” a `H0410K` „god” előtt).
3. A **TAHOT_kivonat.tsv csak a négyjegyű Strongot hordozza** (0 betűs kulcs), tehát az `entry_id` szintű (`H1004B`) különbségtételt az előfordulások nem használják; a szó-lap Strongonként egy kiemelt jelentést kér.

## 2. Javasolt szabályok (⛔ jóváhagyásra)

### 2.1 Melyik sor fordul (K1)

Két változat; a próba (3. szakasz) a **B** szerint készült.

- **A — a brief javaslata:** minden *kapcsolat nélküli* sor fordul (homonimák saját `entry_id`-val); ha egy alapnak nincs ilyen sora, az első nem „gyenge” kapcsolatú sor (a „gyenge”: `a Part of`, `combination of`, `a Meaning of`) a fő sor; minden más kapcsolt alsor **kimarad**. Fordítandó sor: **10 676**; kimarad: 1 001. Veszteség: pl. a H5945B „Most High” (a `Felséges` istennév), a H0776G „land: country/planet”, a H1004P/Q „house: palace/temple” nem kerül a táblába.
- **B — ajánlott:** **minden** sor fordul (11 677), a tábla a `kapcsolat` oszlopban őrzi a TBESH kapcsolatát, és a Strongonkénti kiemelt jelöltet a `fo` oszlop jelöli. Ok: (i) nincs kimaradó, így nincs mit utólag pótolni; (ii) a plusz 1 001 sor rövid (átlag ~7 karakter glossza); (iii) a TBESH kapcsolt sorai valódi jelentés-árnyalatok (`house: temple`), amelyeket a #139 szó-lap később használhat; (iv) az `entry_id`↔sor 1:1, ellenőrzése egyszerű (11 677 = a TBESH sorai).

### 2.2 Melyik a Strong kiemelt jelöltje (`fo`)

Szabály (a script `fo_jelolt()`): az első **kapcsolat nélküli** sor, amelynek glosszájában nincs `(` és a definíciója nem névtöredék (`This name…`, ` means…`, `Combined with…`); ha ilyen nincs, az első kapcsolat nélküli sor; ha az sincs, az A-szabály fallbackja. Eredmény: Strongonként pontosan 1 `fo` (8 718), ebből 25 helyen tér el az „első kapcsolat nélküli sortól” (pl. H0410: `El (Berith)` helyett `god`; H1588: `Garden (of Uzza)` helyett `garden`).

**Ismert hiba (a próba megmutatta, a 300-as átnézőlistán javítható):** a H1004 `fo`-ja a `H1004A` „place” (a fájlsorrendben első), pedig a ház jelentés a H1004B. A H1121 `fo`-ja „son: child”, a H0776-é „land: soil” — a kettőspontos árnyalat a kiemelt sorban zavaró lehet. Ezt a #139 vagy a felhasználó dönti el (K2).

### 2.3 Kulcsséma — `adat/glosszak_heber_hu.tsv`

Kulcs: `entry_id` (a Strong az első 5 karakter; az `entry_id` globálisan egyedi, 11 677/11 677). Mezők:

| Mező | Tartalom |
|---|---|
| `strong` | `H0430` (a SEMA STRONG-típusa) |
| `entry_id` | a TBESH `dStrong` első szava, pl. `H0430G`, `H2763A` |
| `kapcsolat` | a TBESH kapcsolata (`a Name of`, `in Aramaic of`, …); üres, ha nincs (csak a B változatban) |
| `fo` | `igen` / üres; Strongonként pontosan egy `igen` (a 2.2 szerint, vagy kézi felülírás) |
| `glossza_en` | a TBESH 7. oszlopa szó szerint |
| `forras_hash` | `glossza_en` SHA-1-e (UTF-8) |
| `glossza_hu` | a magyar jelentés |
| `allapot` | `sonnet` (a modell által fordított) \| `kezi` (a felhasználó átírta) |
| `modell` | a ténylegesen futó modell neve (`claude-sonnet-5-5`; a saját környezetből, nem briefből) |
| `datum` | a fordítás napja |
| `megjegyzes` | a fordító bizonytalansága (`?`), kapukat felülíró indok |

A `fo` mező a brief javaslati sémájához új; ha az A változat marad, a `kapcsolat` és a `fo` elhagyható (a fő sor = a Strong kiemelt jelöltje; homonimánál a `fo` akkor is kell). A SEMA-bejegyzés az M1 előtt készül, a jóváhagyott sémával.

### 2.4 Kapuk (a `kapuk()` függvény; 9 egységteszt: `eszkozok/teszt_glossza_forditas.py`)

1. nem üres;
2. nincs héber vagy görög betű;
3. hossz: legfeljebb **50 karakter** és **6 szó** (a TBESH-glossza max. 33 karakter; a magyar hosszabb);
4. nincs angol szó: (a) angol funkciószó-lista (`the`, `of`, `to`, `and`, …); (b) a forrás-glossza 4+ betűs kisbetűs szava nem szerepelhet változatlanul a kimenetben; a nagybetűs szavak (tulajdonnevek) és a kivétel-lista szavai mentesek. **A brief „szótár-alapú ellenőrzést” kér: a repóban nincs angol szólista (`/usr/share/dict` sincs), ezért ez forrás-alapú közelítés** (K9);
5. nincs idézőjel és kérdőjel (a bizonytalanságot a `megjegyzes` mező hordozza);
6. a `forras_hash` egyezik (az M1-ben, a tábla írásakor).

### 2.5 Fordítási konvenciók (a promptban; K3–K6)

- **Ige:** főnévi igenév („mondani”, „lenni”). **Főnév:** alanyeset. **Melléknév:** alapfok. Szófaj nélkül.
- **„szó: árnyalat” glossza** a kettőspontot megtartja: `house: palace` → „ház: palota”; `to come (in): towards` → „bejönni: felé”.
- **Tulajdonnév:** a magyar (Károli) alak, ahol van: Roboám, Izráel, Dávid, Benó. Névtöredék: „Bét-(Asbea)”. Ha nincs hagyományos magyar alak, magyaros átírás és `?` (H5971J „Amav”).
- **Istennév:** H3068G „az ÚR”, H0430G „Isten”, H0410K „isten” (a közszó), H0410G „Isten”, H5945B „Felséges”.
- **Jelölők:** `[Obj.]` → „[tárgyjel]”.
- **Terminológia:** a `terminologia.tsv` kulcsai közül a kötegben előforduló (4+ betűs, `kapu≠nem`) kerül a promptba; a próba 30 szavában 2 ilyen volt (`verb`→ige, `accusative`→tárgyeset, a definíciók eleje miatt).

## 3. Prompt (v1; a script `PROMPT_V1`, a köteg-összeállító `prompt_epit()`)

```
Feladat: a TBESH héber szótár rövid angol glosszájának (Gloss) magyar fordítása.
Kimenet: szavanként EGY sor, `<entry_id><TAB><magyar jelentés>`; semmi más.

Szabályok:
1. A magyar jelentés rövid: legfeljebb ~5 szó; több értelem pontosvesszővel (`;`) elválasztva.
2. Szófaj nélkül írd (ne legyen benne „ige”, „főnév”); főnév alanyesetben, ige főnévi igenévvel
   („mondani”), melléknév alapfokon, a glosszában jelzett nemet/számot (pl. „(f.s.)”) megtartva.
3. A glossza a fő támpont. A héber lemma, az átírás, a szófaj és a definíció eleje csak
   kontextus a többértelmű glosszához (pl. `to devote/destroy`): a glosszát ne cseréld le a definícióra.
4. Tulajdonnév: a magyar (Károli-hagyományú) névalak (Rehoboam → Roboám, Abijah → Abija);
   ha nincs hagyományos magyar alak, magyaros átírás. Személy- és helynévnél semmi magyarázat.
5. Istennevek (Károli-szóhasználat): `YHWH`/`LORD` (H3068) → „az ÚR”; `God` (H0430) → „Isten”;
   `Lord` (H0136) → „Úr”; `El` → „Isten” vagy „El” (a glossza szerint). Ne írj „Jehova”-t, ha a glossza nem.
6. Jelölők: `[Obj.]`, `(f.s.)`, `+` és hasonló szögletes/zárójeles jelölők jelentése megmarad
   magyarul (pl. „[tárgyjel]”); kettősponttal bővített glossza („land: country”) → „föld: ország”.
7. Nincs benne héber vagy görög betű, angol szó, idézőjel, magyarázat, kérdőjel.
8. Terminológia (kötelező megfelelők): {a kötegben előforduló terminologia.tsv-kulcsok}
9. Bizonytalanságot ne jelezz a szövegben; a nehéz esetre a sor végére `<TAB>?` kerül.

Bemenet (soronként: entry_id | lemma | átírás | szófaj | Gloss | definíció eleje):
{köteg}
```

Egy köteg javasolt mérete 100 sor (≈ 11 000 karakter bemenet), vagyis a teljes futás 11 677 sorra kb. 117 köteg. A teljes bemenet ≈ 0,4 M token, a kimenet ≈ 0,15 M token.

## 4. Próba: 30 Strong, 101 sor

A 30 Strong: H0430, H3068, H5945, H2763, H1581, H7346, H0853 (a brief hét kötelező szava) + H1961, H0559, H0776, H1121, H3478, H1004, H3117, H5971, H1696, H2896, H7227, H3605, H0834, H3808, H5921, H0935, H8064, H6944, H1732, H0001, H0576 (arám), H0410, H0120. A **B** változat szerint minden soruk lefordítva (a 101 sorból 30 az `fo`). Gyakori ige (H1961, H0559, H1696, H0935), főnév (H0776, H8064, H3117), melléknév (H2896A, H7227A, H5945A), partikula (H0853, H3808, H5921, H0834), tulajdonnév (H7346, H3478, H1732), istennév (H0430, H3068, H0410), homonima (H2763, H5945, H2896, H1004), arám (H0576).

**Kapuk eredménye: 101 sor, 0 kapuhiba.** (A kapu a negatív tesztekben fog: `the teve`, héber betű, hosszú szöveg, `?`.) A `?` oszlop a fordító bizonytalanságát jelzi (6 sor); ez nem kapuhiba.

### A 101 sor (a `fo` oszlop: a Strong kiemelt jelöltje; `?`: a fordító bizonytalan)

| entry_id | fo | kapcsolat | glossza_en | glossza_hu | ? | kapu |
|---|---|---|---|---|---|---|
| H0430G | fo | a Name of | God | Isten |  | OK |
| H0430H |  | a Part of | (LORD)-Elohe | (az ÚR)-Elohé |  | OK |
| H0430I |  | a Part of | (Gibeath)-elohim | (Gibeát)-Elóhim |  | OK |
| H3068G | fo | - | LORD | az ÚR |  | OK |
| H3068H |  | a Name of | The Lord | az ÚR | ? | OK |
| H3068I |  | a Part of | (Jerusalem of) the Lord | (az ÚR Jeruzsálemje) | ? | OK |
| H5945A | fo | - | high | magas |  | OK |
| H5945B |  | in Hebrew of | Most High | Felséges |  | OK |
| H5945G |  | a Part of | Upper (Beth Horon) | Felső (Bét-Hóron) |  | OK |
| H5945H |  | a Part of | (LORD) Most High | (az ÚR) Felséges |  | OK |
| H2763A | fo | - | to devote/destroy | kiirtásra szentelni; elpusztítani |  | OK |
| H2763B |  | - | to slash | felhasítani |  | OK |
| H1581 | fo | - | camel | teve |  | OK |
| H7346 | fo | - | Rehoboam | Roboám |  | OK |
| H0853 | fo | - | [Obj.] | [tárgyjel] |  | OK |
| H1961 | fo | - | to be | lenni |  | OK |
| H0559 | fo | - | to say | mondani |  | OK |
| H0776G |  | in Hebrew of | land: country/planet | föld: ország/bolygó |  | OK |
| H0776H | fo | - | land: soil | föld: talaj |  | OK |
| H1121A | fo | - | son: child | fiú: gyermek |  | OK |
| H1121B |  | - | Beno | Benó |  | OK |
| H1121G |  | a Meaning of | son: descendant/people | fiú: leszármazott/nép |  | OK |
| H1121H |  | a Meaning of | son: young animal | fiú: állatkölyök |  | OK |
| H1121I |  | a Meaning of | son: type of | fiú: -féle | ? | OK |
| H1121J |  | a Meaning of | son | fiú |  | OK |
| H1121K |  | a Meaning of | son: warrior | fiú: harcos |  | OK |
| H1121L |  | a Meaning of | son: aged | fiú: -éves | ? | OK |
| H3478 | fo | - | Israel | Izráel |  | OK |
| H1004A | fo | - | place | hely |  | OK |
| H1004B |  | - | house: home | ház: otthon |  | OK |
| H1004G |  | - | Beth-(ashbea) | Bét-(Asbea) |  | OK |
| H1004H |  | - | Beth (Haggan) | Bét (Haggán) |  | OK |
| H1004I |  | a Part of | Beth-(togarmah) | Bét-(Tógarma) |  | OK |
| H1004J |  | - | House (of the Forest) | (az erdő) háza |  | OK |
| H1004K |  | - | House (of the Forests of Lebanon) | (Libanon erdejének) háza |  | OK |
| H1004L |  | a Part of | Beth-(baal-meon) | Bét-(Baál-Meon) |  | OK |
| H1004M |  | a Meaning of | house: household | ház: háznép |  | OK |
| H1004N |  | a Meaning of | house: container | ház: tartály |  | OK |
| H1004O |  | a Meaning of | house: inside | ház: belső |  | OK |
| H1004P |  | in Hebrew of | house: palace | ház: palota |  | OK |
| H1004Q |  | in Hebrew of | house: temple | ház: templom |  | OK |
| H3117G | fo | - | day | nap |  | OK |
| H3117H |  | a Meaning of | day: old | nap: régmúlt |  | OK |
| H3117I |  | a Meaning of | day: year | nap: év |  | OK |
| H3117J |  | a Meaning of | day: daily | nap: naponta |  | OK |
| H3117K |  | a Meaning of | day: always | nap: mindig |  | OK |
| H3117L |  | a Meaning of | day: today | nap: ma |  | OK |
| H5971A | fo | - | people | nép |  | OK |
| H5971B |  | - | kinsman | rokon |  | OK |
| H5971G |  | - | Ammi | Ammi |  | OK |
| H5971H |  | - | People's (Gate) | A nép (kapuja) |  | OK |
| H5971I |  | a Part of | (Ibleam)-am | (Jibleám)-ám | ? | OK |
| H5971J |  | - | Amaw | Amav | ? | OK |
| H5971K |  | a Meaning of | people: soldiers | nép: katonák |  | OK |
| H5971L |  | a Meaning of | people: creatures | nép: teremtmények |  | OK |
| H1696G | fo | - | to speak: speak | szólni: beszélni |  | OK |
| H1696H |  | a Meaning of | to speak: subdue | szólni: leigázni |  | OK |
| H1696I |  | a Meaning of | to speak: promise | szólni: ígérni |  | OK |
| H2896A | fo | - | pleasant | kellemes |  | OK |
| H2896B |  | - | good | jó |  | OK |
| H2896C |  | - | welfare | jólét |  | OK |
| H7227A | fo | - | many | sok |  | OK |
| H7227B |  | - | chief | főnök |  | OK |
| H7227G |  | a Part of | (Sidon) the Great | (Szidon) a nagy |  | OK |
| H3605 | fo | - | all | minden |  | OK |
| H0834A | fo | - | which | amely; aki |  | OK |
| H0834B |  | combination of | in which | amelyben |  | OK |
| H0834C |  | combination of | whence | ahonnan |  | OK |
| H0834D |  | combination of | as which | ahogyan |  | OK |
| H3808 | fo | - | not | nem |  | OK |
| H5921A | fo | - | upon | fölött; -on/-en |  | OK |
| H5921B |  | a Meaning of | as | mint |  | OK |
| H0935G | fo | - | to come (in): come | bejönni: jönni |  | OK |
| H0935H |  | a Part of | Lebo-(Hamath) | Lebó-(Hamát) |  | OK |
| H0935I |  | a Meaning of | to come (in): towards | bejönni: felé |  | OK |
| H0935J |  | a Meaning of | to come (in): advanced | bejönni: előrehaladott |  | OK |
| H0935K |  | a Meaning of | to come (in): (sun)set | bejönni: (nap)nyugta |  | OK |
| H0935L |  | a Meaning of | to come (in): marry | bejönni: megházasodni |  | OK |
| H0935M |  | a Meaning of | to come (in): fulfill | bejönni: beteljesülni |  | OK |
| H0935N |  | a Meaning of | to come (in): besiege | bejönni: ostromolni |  | OK |
| H0935O |  | a Name of | Lebo | Lebó |  | OK |
| H0935P |  | a Meaning of | to come (in): bring | bejönni: hozni |  | OK |
| H8064 | fo | - | heaven | ég |  | OK |
| H6944G | fo | - | holiness | szentség |  | OK |
| H6944H |  | - | Most Holy Place | Szentek Szentje |  | OK |
| H6944I |  | a Part of | (Way of) Holiness | (a szentség) útja |  | OK |
| H6944J |  | - | Holy Place | szent hely |  | OK |
| H1732 | fo | - | David | Dávid |  | OK |
| H0001G | fo | - | father | atya |  | OK |
| H0001H |  | a Part of | (Huram)-abi | (Hurám)-Abi |  | OK |
| H0001I |  | a Part of | father of | atyja |  | OK |
| H0576A | fo | in Aramaic of | me | én; engem |  | OK |
| H0576B |  | in Aramaic of | me | én; engem |  | OK |
| H0410G |  | a Name of | God | Isten |  | OK |
| H0410H |  | - | El (Berith) | El (Berit) |  | OK |
| H0410I |  | combination of | El (Elohe) | El (Elohé) |  | OK |
| H0410J |  | a Part of | El (Most High) | El (Felséges) |  | OK |
| H0410K | fo | - | god | isten |  | OK |
| H0410L |  | a Meaning of | god: power | isten: hatalom |  | OK |
| H0120G | fo | - | man | ember |  | OK |
| H0120H |  | a Spelling of | the man (Adam) | az ember (Ádám) |  | OK |

sorok: 101, kapuhiba: 0

## 5. Megfigyelések a próbából

- **Kettőspontos glossza** („land: soil”, „son: child”): a kiemelt sorban a kettőspont utáni árnyalat zavarhat; ezt a megjelenítés (#139) vághatja le a kettőspontnál, vagy a tábla külön mezőt kap — a döntés K2.
- **Azonos nevek** (pl. Abijah 8 sora) ugyanazt a glosszát kapják; az M1 a `(glossza_en, szófaj)` párra gyorsítótárat használ, hogy a névalak következetes legyen.
- **Bizonytalan sorok (`?`)**: H3068H/I (Jeruzsálem neve, „az ÚR”), H1121I „son: type of”, H1121L „son: aged”, H5971I, H5971J (ismeretlen névalak).
- **A H1004 `fo`-ja hibás** (`place` a `house` helyett; 2.2) — a szabály nem látja a fájlsorrend mögötti gyakoriságot. A TAHOT-glossza-vizsgálat (a leggyakoribb TAHOT-„Rövid jelentés” egyezik-e az `fo`-val) megoldhatná, de a TAHOT „LORD”-hibás oszlopai a #138 alatt változnak; ezért csak a 300 leggyakoribb szó kézi átnézése véd.
- **Licenc:** a TBESH sora a `licencek.tsv`-ben `tisztazott` (DT-F33f kivétel az Online Bible-eredetű Meaning oszlopra), tehát a fordítás levezetett mű CC BY 4.0 szerint; a `sqlite_epit.py` `ADAT_LICENC` szótárában a `glosszak_heber_hu` ma nincs, így az általános betöltő a `projekt_adat` licencet adná neki (K8).

## 6. Kérdések (⛔; tétel: `DONTESEK.md` DT346)

| # | Kérdés | Opciók | Javaslat |
|---|---|---|---|
| K1 | Melyik sorok fordulnak? | (A) kapcsolat nélküli + fő sorok, 10 676 sor, a kapcsolt alsorok kimaradnak · (B) mind a 11 677 TBESH-sor, `kapcsolat` oszloppal | **B** |
| K2 | A Strongonkénti kiemelt jelölt (`fo`) és a kettőspontos árnyalat | (a) `fo` oszlop a 2.2 szabállyal, a tábla a teljes fordítást őrzi, a kettőspont-levágás a #139 dolga · (b) `fo` + külön `rovid` mező (a kettőspont előtti rész) · (c) nincs `fo`, a #139 választ | **(a)** |
| K3 | A „szó: árnyalat” forma magyarul | (a) a kettőspont megmarad („ház: palota”) · (b) a kettőspont helyett vessző | **(a)** |
| K4 | Az ige alakja | (a) főnévi igenév („mondani”) · (b) a szótári 3. egyes szám múlt („mondta”) | **(a)** (a brief is ezt írja) |
| K5 | Az istennevek | H3068 „az ÚR”, H0430 „Isten”, H0136 „Úr”, H0410K „isten”, H5945B „Felséges” a promptban rögzítve | jóváhagyás |
| K6 | Az ismeretlen magyar névalak | magyaros átírás + `?` a `megjegyzes`-ben; a 300-as listán átnézendő | jóváhagyás |
| K7 | Az M1 végrehajtása | (a) a session maga fordít kötegenként (~117 köteg, több session, „Folytatási pont”-tal), a script csak köteget készít, rögzít és ellenőriz · (b) külső API-hívás (a repóban van minta: `eszkozok/karoli_strong/api_koteg.py` [Anthropic Message Batches, F77] és `eszkozok/fordit.py` [OpenRouter, F03]; API-kulcsot és költséget kíván) | **(a)** |
| K8 | Licenc-bejegyzés | az `sqlite_epit.py` `ADAT_LICENC`-ébe `glosszak_heber_hu: ['TBESH']` (külön, a felhasználó elé kerülő módosítás) · vagy marad az alapértelmezett `projekt_adat` | az `ADAT_LICENC`-bejegyzés külön kisfeladatként |
| K9 | Az „nincs angol szó” kapu | (a) a jelenlegi forrás-alapú közelítés + kivétel-lista · (b) angol szólista behozatala (új dataset, licenc-ellenőrzéssel, playbook 2. pont) | **(a)** |
| K10 | Hossz-korlát | 50 karakter / 6 szó (a javaslat) · szigorúbb (40 / 5) | a javaslat |

## 7. DT346 alkalmazása (2026-10-25, a felhasználó döntése, chat)

A K1–K10 a `DONTESEK.md` DT346 sora szerint eldőlt (a K2, K5, K8 kifejezett megerősítéssel). A napló fenti szövege a döntés előtti állapotot rögzíti; az alkalmazás: `K1` a (B) változat (a próba is ez szerint készült); `K2` a `fo` a TAHOT-többséggel egyező glosszájú sor (`fo_jelolt()`, `tahot_tobbseg()`; a K5-lista a 11 istenneves Strongnál; a 2.2 heurisztika a nem illeszthetőnél; mért: a 1 392 többsoros alapból 1 304 illeszkedik a TAHOT-többséghez, 83 nem, 5 a K5-listán); `K5` a prompt 5. szabálya és az `ISTENNEV_FIX` (a szkript írja be, a modell nem fordítja); `K3` a kettőspont-kapu; a K7 szerint a napló fenti „nincs ilyen szkript” állítása téves volt (l. a K7 sor javítását); a K8-at a #140 nem hajtja végre: javaslat a zárójelentésben.
