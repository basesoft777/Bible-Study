# F239 lépésnapló — TEREMT-001 (tehóm)

*A menet döntései indoklással, lépésenként (brief 5. pont). A határ részletei: `naplok/F239_hatar.md`; a vitatott pontok: `naplok/ERVNAPLO_TEREMT-001.md`.*

## U2 — határ és érvvázlat (2026-11-23, `claude-opus-5-5`)

**Technikai döntések (DT920: a session dönti, itt rögzítve):**
- A 28 U1-jelölt döntése a meglévő negatív kritérium alkalmazása, nem új határ: a sorok `elutasítva` (`F239_hatar.md` 4. pont). A gépi lexéma-hozzárendelést versenként átnéztem; öt egyverses blokknál a ténylegesen fordított szó áll az indoklásban.
- A Septuaginta-többlet két verse (Jób 36:16, Zsolt 71:21) új, `elutasítva` jelölt-sor lett (a 2. szabály: a lekérdezés-találat a jelölttáblán át; az ALVIL-001 mintája szerint). A 14 deuterokanonikus G0012-token Károli-kulcs híján nem kap sort.
- Az elutasítási okok mintaszótára két TEREMT-001 sorral bővült (a brief `ir` listáján kívül, gépies, külön commit: F239.4).
- A `naplok/HATAR_TEREMT-001.md` gépi része a mai adaton újrafutott.
- A Jób 42:8 szótári sora (`adat/bdb_vers_jelentes.tsv` 27. H8415-sor) generált tábla, már `ketes:jp_illesztes` jelzésű: a jelölt elutasítva, a generátorhoz nem nyúlok (elvetve: a jelzés a fogyasztóknak már szól, olvasói tartalmat nem érint).
- Az N58 (a régi tanulmány számai) a régi tanulmány archiválásával zárul az U3-ban; a régi szöveget nem javítjuk.
- A `res_forras.tsv` kilenc sora (a `kivonat` B47-et ad, az `alkalmazas` sor kivezetendő): az U3 technikai része, a kézi forrás megírásával egy commitban.

**⛔ Tartalmi kérdés 1 — motívumközi kapcsolat** (az integrátornak elküldve, 2026-11-23):
A közös vers az ALVIL-001-gyel az Ez 31:15 (a cédrus a seólba száll, a tehóm gyászba borul), a TEREMT-002-vel az 1Móz 1:2. A funkció mindkét párnál más (két motívum marad). Javaslat: az ALVIL-001-gyel az Ez 31:15-ön adatsor (motívumközi jelölt `beépítve` + `motivum_kapcsolatok.tsv`, típus: azonos vers), mert a halál mélye (Jón 2:6, Zsolt 71:20, Róm 10:7) a két motívum valódi érintkezése; a TEREMT-002-vel csak a próza említse az 1Móz 1:2-t (a TEREMT-002 fagyasztott, az adatához nem nyúlunk).
Döntés: **(a), a javaslat** (DT-F239a, szerkesztői döntés, a felhasználó, 2026-11-23: „Adatsor is (Recommended)”; alkalmazva: F239.7). Előzmény: az integrátor előbb (a) döntést küldött (F239.5-ben alkalmazva), majd visszavonta: a motívumhatár a szerkesztő döntése, nem az integrátoré (a szerkesztő, 2026-11-23: „ez nem az én döntésem kell legye?”). A sorok az F239.6-ban kivéve; a felvevő szkript (`naplok/F239_U2_dontesek_ir.py`) a szerkesztő szava után változatlanul újrafuttatható. Feltétel (az integrátortól): a befagyasztott ALVIL-001 lapfájljához nem nyúlunk (az E28 a befagyasztott lapot nem veti össze). A kérdés: `naplok/F239_szerkeszto_kerdesek.md`.

**⛔ Tartalmi kérdés 2 — Nave-döntések** (a mérce a funkció; az integrátornak elküldve, 2026-11-23). Javaslat (11 jelölt, `naplok/F239_U1_TEREMT-001_nave_jeloltek.tsv`):

| téma | versek | javaslat | indok |
|---|---|---|---|
| NAVE-3885 PIT („The bottomless pit”) | Jel 9:11, 11:7, 17:8 | kivalasztott | funkció-téma: a feneketlen mélység, az ÚSZ ἄβυσσος-a |
| NAVE-1502 EARTH („Created by God; Primitive condition of”) | Zsolt 104:6, Péld 8:24 | kivalasztott | funkció-téma: a föld teremtés előtti állapota, amelyet a mélység borít |
| NAVE-1400 DEW („A merciful providence”) | 5Móz 33:13, Péld 3:20 | kivalasztott | funkció-téma: a mélység és a harmat mint Isten gondviselő áldása |
| NAVE-3986 PSALMS („Of Moses, celebrating the deliverance at the Red Sea”) | 2Móz 15:5, 15:8 | kivalasztott | funkció-téma: a vörös-tengeri szabadítás, ahol a mélység az ítélet eszköze; a négy műfaji téma közül ez nevezi meg a funkciót |
| NAVE-1682 EPIC, NAVE-4643 SONG, NAVE-3906 POETRY | 2Móz 15:5, 15:8 | kizart | ugyanannak a két versnek műfaji címkéi; a PSALMS-téma lefedi őket |
| NAVE-0305 ANIMALS | 1Móz 7:11, Zsolt 36:7, Jel 11:7 | kizart | a versek az állatok miatt esnek bele, nem a mélység funkciója miatt |
| NAVE-1213 CONTINENTS | Jób 38:16, Zsolt 104:6 | kizart | a téma a szárazföldet indexeli; a teremtés-funkciót az EARTH lefedi |
| NAVE-3189 MANASSEH, NAVE-1676 EPHRAIM | 1Móz 49:25, 5Móz 33:13 | kizart | az áldás címzettjét indexelik, nem a mélység funkcióját |

`tiltott` sor nem kell: egyik jelölt sem a fölérendelt fogalom (vízi és kozmikus káosz általában) felé visz. A négy kiválasztott téma magyar neve az `adat/nave_tema_hu.tsv`-ben még nincs: az U3 technikai része (`glossza_lexikon_forditas.py nave`).
Döntés: **(a), a javaslat** (DT-F239b, szerkesztői döntés, a felhasználó, 2026-11-23: „A javaslat (Recommended)”; alkalmazva: F239.7). Előzmény (mint az 1. kérdésnél: az integrátor (a) döntése visszavonva; a sorok az F239.6-ban kivéve, a felvevő szkript újrafuttatható). A kérdés: `naplok/F239_szerkeszto_kerdesek.md`.

**A határ státusza:** a szerkesztő 2026-11-23-án a határt és a 28 jelölt döntését elfogadta („A javaslat (Recommended)”, DT-F239c), a határ-ellenőr többi pontjára adott válaszokkal együtt („Elfogadom (Recommended)”). Előzmény (az integrátor, 2026-11-23): az F239.3 határa (`naplok/F239_hatar.md`) és a 28 jelölt döntése javaslat, a szerkesztő döntésére vár; nem vonjuk vissza, de végleges lépés nem épül rá. A határt meghúzó, nem triviális pontok a szerkesztői kérdéslistán.

**A határ-ellenőr** (`hatar-ellenor`, `claude-sonnet-5-5`, a mai adaton; az első indítás a session leállásakor megszakadt, újraindítva): 5 kérdés a `naplok/HATAR_TEREMT-001.md` Modelles részében; a válaszok a `naplok/F239_hatar.md` 6. pontjában (K2 elfogadva: U3-feladat; K3 javítva; K5 elvetve indokkal; K1 és K4 az alábbi két kérdés).

**⛔ Tartalmi kérdés 3 — a negatív kritérium szövege** (az integrátornak elküldve, 2026-11-23): a `motivumok.tsv` „ÚSZ-ben az LXX-közvetített ἄβυσσος (abüsszosz) megfelelőjét” helyett: „az Újszövetségben a görög ἄβυσσος (abüsszosz) szót, a Septuaginta tehóm-fordításának szavát”. A tagság nem változik; a mostani szöveg azt sugallja, hogy a Luk 8:31-nél és a Róm 10:7-nél a Septuagintát kell nézni.
Döntés: a javaslat (szerkesztői döntés, a felhasználó, 2026-11-23; DT-F239c: „Új szöveg (Recommended)”, DT-F239d: „Két igehely (Recommended)”; alkalmazva: F239.7, `naplok/F239_U2_szerkesztoi_dontes.py`).

**⛔ Tartalmi kérdés 4 — a Jel 20:1–3 tartomány-sor** (az integrátornak elküldve, 2026-11-23): a sor kettéválik Jel 20:1-re és Jel 20:3-ra (a 20:2-ben a szó nem áll), így a motívum versszáma a scanével egyezik (44); a lapon két igehely áll egy helyett. A Jel 9:1–2 marad (mindkét versben áll a szó).
Döntés: a javaslat (szerkesztői döntés, a felhasználó, 2026-11-23; DT-F239c: „Új szöveg (Recommended)”, DT-F239d: „Két igehely (Recommended)”; alkalmazva: F239.7, `naplok/F239_U2_szerkesztoi_dontes.py`).
