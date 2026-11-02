# GERINC_KARTYA_SZOVEG_naplo.md — a #125 naplója

*Modell: claude-sonnet-5-5 (a brief `modell`: sonnet, egyezik). Indítás: 2026-11-01, az orkesztrátor a felhasználó szó szerinti idézetével: „Igen, mind”, majd „#125: induljon az M0 mérés.”*

## Egyeztetett eltérés a briefhez képest

A felhasználó 2026-10-29-i („mehet”) tétele, a **két új munkamenet-lépés** (szakaszcímke ⛔ csak eltérésnél; fordítás a lap első generálása előtt, az `F148_*_BRIEF.md` 6. szakaszának szövege) a briefben **nem szerepel** (a 2.1 csak az A3b/A3c-t hozza). Az 1. lépés szövegjavaslatába felveszem; a brief szövegét jóváhagyás nélkül nem írtam át.

## M0 — a mérőszkript próbája (`eszkozok/proza_lefedettseg.py`, 2.4 és 2.5)

Mérés: `python eszkozok/proza_lefedettseg.py ISTENTISZT-001 ALVIL-001`, 2026-11-01, a `motivumok/[ID].md` kézi prózáján (táblasor, jelölő és `【NAPLO` kihagyva). A névmatch heurisztika (könyv + fejezet:vers a bekezdésben, vagy a könyv említése mellett puszta fejezet:vers); a „12. vers” szóbeli alakot nem látja, ezért a „nem” sorok kézi ellenőrzést igényelnek.

**Amit a mérés mutat:**
- ISTENTISZT-001: az előfordulás 33/33 megnevezve; 3 kapcsolat (1Móz 4:26 → Sof 3:9, Jóel 2:32, 2Móz 33:19) és 1 nyitott jelölt (Ézs 41:25) nincs megnevezve. A Kivonat blokk 56, az 1. pont 125 karakter/elem, a 3. pont 388, a 7. 706: a lap eleje sűrű adat, kevés próza.
- ALVIL-001: 72 előfordulásból 15 van megnevezve, 57 nem. Ezt a prózában a „63 egyedi igehely” gyűjtő mondat fedi, a generált tábla viszont soronként tartalmazza; a mérő jelenleg nem különbözteti meg a csoportos említést a hiánytól. A kapcsolat és a nyitott jelölt 0 (a kapcsolatok.tsv-ben nincs ALVIL-001 sor).
- A „Károli rejtett párhuzama” (14. szerep) nem mérhető: nincs gépi adatforrása (DT424).

### ISTENTISZT-001

Próza: 88 bekezdés, 42072 karakter (táblasor, jelölő és napló nélkül).

### Lefedettség (a próza nem nevezi meg)

| rovat | adat | megnevezve | nem |
|---|---|---|---|
| előfordulás | 33 | 33 | 0 |
| kapcsolat | 25 | 22 | 3 |
| motívumközi kapcsolat | 3 | 3 | 0 |
| nyitott jelölt | 6 | 5 | 1 |

Név nélküli elemek:

- kapcsolat: 1Móz 4:26 → Sof 3:9 (Párhuzam)
- kapcsolat: 1Móz 4:26 → Jóel 2:32 (Párhuzam)
- kapcsolat: 1Móz 4:26 → 2Móz 33:19 (Variáns)
- nyitott jelölt: Ézs 41:25 (elofordulas; F110 szűrő (DT283), B osztály, kézi olvasás: Károli: „hirdet)

*A „Károli rejtett párhuzama” (14. szerep) nem mérhető: nincs gépi adatforrása (l. DT424); a mérő ezt nem tölti ki.*

### Egyenetlenség (blokkonként)

| blokk | karakter | megnevezett elem | karakter/elem | jel |
|---|---|---|---|---|
| Kivonat | 836 | 15 | 56 | kevés próza az elemre; a medián (388) 4x-ánál távolabb |
| 1. Előfordulások összegyűjtése | 5502 | 44 | 125 | kevés próza az elemre |
| 2. Eredeti nyelvi összevetés | 4809 | 18 | 267 |  |
| 3. A PaRDeS keretrendszer — a motívum egészére alkalmazva | 22113 | 57 | 388 |  |
| 4. Kapcsolódás a kutatási sablonhoz | 307 | 0 | – |  |
| 5. Alkalmazás és tanítványság | 1442 | 3 | 481 |  |
| 7. Módszertan és nyitott kérdések | 7063 | 10 | 706 |  |

Küszöbök (javaslat, DT471): kevés = 150 karakter/elem alatt; eltérés = 4x a blokkok mediánjától; legalább 3 megnevezett elem.

Adatelemet egyáltalán nem megnevező bekezdés (értelmező, módszertani): 41 / 88

### ALVIL-001

Próza: 13 bekezdés, 5878 karakter (táblasor, jelölő és napló nélkül).

### Lefedettség (a próza nem nevezi meg)

| rovat | adat | megnevezve | nem |
|---|---|---|---|
| előfordulás | 72 | 15 | 57 |
| kapcsolat | 0 | 0 | 0 |
| motívumközi kapcsolat | 2 | 2 | 0 |
| nyitott jelölt | 0 | 0 | 0 |

Név nélküli elemek:

- előfordulás: 1Móz 37:35 (Remez)
- előfordulás: 1Móz 42:38 (Remez)
- előfordulás: 1Móz 44:29 (Remez)
- előfordulás: 1Móz 44:31 (Remez)
- előfordulás: 4Móz 16:30 (Remez)
- előfordulás: 4Móz 16:33 (Remez)
- előfordulás: 5Móz 32:22 (Remez)
- előfordulás: 1Sám 2:6 (Remez)
- előfordulás: 1Kir 2:6 (Remez)
- előfordulás: 1Kir 2:9 (Remez)
- előfordulás: Jób 7:9 (Remez)
- előfordulás: Jób 11:8 (Remez)
- előfordulás: Jób 14:13 (Remez)
- előfordulás: Jób 17:12 (Remez)
- előfordulás: Jób 17:15 (Remez)
- előfordulás: Jób 21:13 (Remez)
- előfordulás: Jób 24:19 (Remez)
- előfordulás: Jób 26:6 (Remez)
- előfordulás: Zsolt 6:6 (Remez)
- előfordulás: Zsolt 9:18 (Remez)
- előfordulás: Zsolt 30:4 (Remez)
- előfordulás: Zsolt 49:15 (Remez)
- előfordulás: Zsolt 49:16 (Remez)
- előfordulás: Zsolt 86:13 (Remez)
- előfordulás: Zsolt 88:4 (Remez)
- előfordulás: Zsolt 89:49 (Remez)
- előfordulás: Zsolt 139:8 (Remez)
- előfordulás: Zsolt 141:7 (Remez)
- előfordulás: Péld 1:12 (Remez)
- előfordulás: Péld 5:5 (Remez)
- előfordulás: Péld 7:27 (Remez)
- előfordulás: Péld 9:18 (Remez)
- előfordulás: Péld 15:11 (Remez)
- előfordulás: Péld 15:24 (Remez)
- előfordulás: Péld 23:14 (Remez)
- előfordulás: Péld 27:20 (Remez)
- előfordulás: Péld 30:16 (Remez)
- előfordulás: Préd 9:12 (Remez)
- előfordulás: Én 8:6 (Remez)
- előfordulás: Ézs 5:14 (Remez)
- előfordulás: Ézs 7:11 (Remez)
- előfordulás: Ézs 28:15 (Remez)
- előfordulás: Ézs 28:18 (Remez)
- előfordulás: Ézs 38:10 (Remez)
- előfordulás: Ézs 38:18 (Remez)
- előfordulás: Ézs 57:9 (Remez)
- előfordulás: Ez 31:15 (Remez)
- előfordulás: Ez 31:16 (Remez)
- előfordulás: Ez 31:17 (Remez)
- előfordulás: Ez 32:21 (Remez)
- előfordulás: Ez 32:27 (Remez)
- előfordulás: Ámós 9:2 (Remez)
- előfordulás: Hab 2:5 (Remez)
- előfordulás: ApCsel 2:27 (Peshat/Drash)
- előfordulás: Luk 16:23 (Peshat)
- előfordulás: Jel 6:8 (Peshat/Remez)
- előfordulás: Mt 11:23 (Remez)

*A „Károli rejtett párhuzama” (14. szerep) nem mérhető: nincs gépi adatforrása (l. DT424); a mérő ezt nem tölti ki.*

### Egyenetlenség (blokkonként)

| blokk | karakter | megnevezett elem | karakter/elem | jel |
|---|---|---|---|---|
| Kivonat | 778 | 4 | 194 |  |
| 1. Előfordulások összegyűjtése | 633 | 2 | 316 |  |
| 3. A PaRDeS keretrendszer — a motívum egészére alkalmazva | 3901 | 15 | 260 |  |
| 5. Alkalmazás és tanítványság | 289 | 0 | – |  |
| 7. Módszertan és nyitott kérdések | 277 | 0 | – |  |

Küszöbök (javaslat, DT471): kevés = 150 karakter/elem alatt; eltérés = 4x a blokkok mediánjától; legalább 3 megnevezett elem.

Adatelemet egyáltalán nem megnevező bekezdés (értelmező, módszertani): 5 / 13


## DT471 — eldöntve (1. változat)

A felhasználó („a javaslat szerint”, az orkesztrátor-session idézetével): 150 karakter/elem alatt „kevés”; a blokk-medián négyszeresénél távolabb „egyenetlen”; legalább 3 elem; a csoportos említés külön kategória. Rögzítve: `DONTESEK.md`.

## F125.2 — eszköz és JELENTÉS-szabályok

- `proza_lefedettseg.py`: új „csoportosan fedett” oszlop (a „N egyedi igehely” gyűjtő mondat, csak az előfordulásokra; ALVIL-001: 72 / megnevezve 15 / csoportosan fedett 57 / hiány 0). A mérő nem tudja, a gyűjtő mondat melyik igehelyeket fedi: csak darabszám szerint kezeli. A fedett darabszám a gyűjtő mondat N-jéig terjed (legfeljebb a prózában álló legnagyobb N, a többi név nélküli előfordulás hiány marad; javítás: ELLENOR_F125 1., F125.6).
- `ellenoriz.py` 22. szabály (kiejtés nélküli héber/görög szó a `lexikon/*_TUDOMANYOS.md`-n, `kiejtes_szoveg.elemez`) és 23. szabály (próza-lefedettség a `motivumok/*.md`-n), mindkettő JELENTÉS, nem gátol. Mért: 22 → 192 jelzés, 23 → 77 jelzés a mai main-en. A 22. közelítés: a szakasz későbbi kiejtése nem pótolja az első előfordulás hiányát. *(A DT472 óta nem érvényes: l. „DT472 — a 22. szabály”.)*
- Tesztek: `teszt_proza_lefedettseg.py` (11, zöld) a két szabályt is lefedi; a briefben szereplő külön `teszt_ellenoriz_proza.py` nem készült (egy fájl, két téma).

## ⛔ A szövegjavaslatok

`naplok/F125_SZOVEGJAVASLAT.md` (13 sor). Jóváhagyásig a MUNKAMENET-hez és a sablonokhoz nem nyúltam.

## F125.3 — a szövegjavaslat jóváhagyva, beírva

A 13 pont jóváhagyása (az orkesztrátor-session idézete; előbb a jóváhagyást visszavonták, majd újra megadták): az orkesztrátor a 13 pontot négy csoportban mutatta be („mind a 13 mehet”), a felhasználó válasza szó szerint: **„a javaslatod szerint”**. Beírva: `MUNKAMENET.md` (A3b, A3c, prioritási-térkép mondat, C-x, C-y, C-z, C-w), `2_` sablon v22, a kiejtés-szabály (K) az 1_, 2_, 4_, 5_, 6_ sablonban és a gyorsreferenciában, a 6_ sablon L és O szakasza és kolofon-kiadás sora, az olvasói elv a gyorsreferenciában, `.claude/commands/kiadas.md`. A C-x/C-y szövege az `F148` 6. szakaszából szó szerint (a brief hatókörét ezzel bővítettem).

Nincs kész: a kolofon kiadás-sorát a generátor még nem rendereli (a `lexikon_general.py` a #152 fájlja); a `6_` sablon ezt szabályként rögzíti. Nyitott tételként felvéve: `N67` (`NYITOTT_FELADATOK.md`; ELLENOR_F125 4.).


## F125.9 — a mért számok proveniencia-sora és az újramérés (ELLENOR_F125 6.)

A fenti 57, 4, 192 és 77 szám az 1. tétel (F125.6) UTÁN újramérve, az ág `24971b44` állapotán; az eredmény a régivel egyező, eltérés nincs (az 57 azóta „csoportosan fedett”, mert a kód N-je, 64 [a `max(N)` a `motivumok/ALVIL-001.md:13` „64 egyedi igehely” mondatából jön; a :23 „63 egyedi igehely” mondata kisebb], nem kisebb nála; ELLENOR_F125_2 1′: az eredeti szöveg 63-at írt). A 15. sor „63 egyedi igehely” idézete a :23 mondatot idézi pontosan, azt nem módosítottam. A `teszt_proza_lefedettseg.py` `test_csoportos_ALVIL_eset_63_legalabb_57` tesztje saját, szintetikus 63-as adatot használ, szándékosan, ezért ahhoz nem nyúltam.

- ALVIL-001: 72 előfordulás, 15 megnevezve, 57 csoportosan fedett, 0 hiány; ISTENTISZT-001: 33/33 előfordulás megnevezve, 3 név nélküli kapcsolat + 1 nyitott jelölt = 4 név nélküli elem. `scope=python eszkozok/proza_lefedettseg.py ISTENTISZT-001 ALVIL-001 | forras=motivumok/ISTENTISZT-001.md, motivumok/ALVIL-001.md, adat/elofordulasok.tsv, adat/kapcsolatok.tsv, adat/jeloltek.tsv | ts=2026-11-01T16:52+01:00`
- 22. szabály: 192 jelzés; 23. szabály: 77 jelzés. `scope=python eszkozok/ellenoriz.py (teljes futás, a 22. és 23. szabály jelzésszáma; az eszköznek nincs szabályonkénti kapcsolója) | forras=lexikon/*_TUDOMANYOS.md (22.), motivumok/*.md és adat/*.tsv (23.) | ts=2026-11-01T16:52+01:00`

A régi (F125.2) mérés: 22 → 192, 23 → 77, ugyanezzel a paranccsal a mai main-en; az F125.6 nem változtatta a 23. szabály jelzésszámát.

## DT472 — a 22. szabály

A felhasználó döntése (DT472, 2026-11-01, az orkesztrátor-session továbbításával): „a) kód a szöveghez”. A 22. szabály (`eszkozok/ellenoriz.py` `szabaly22_kiejtes_hiany`) a jóváhagyott K-szöveghez igazítva: egy héber/görög szót akkor jelez, ha a szakaszban (két `##`/`###` cím között) SEHOL nem kap kiejtést; ha bármelyik előfordulása kap, nem jelez (`kiejtes_szoveg.elemez_szakaszonkent`). A hatókör a `lexikon/*_TUDOMANYOS.md` mellett a tanulmányok is: `tematikus_lezart/`, `genezis/`, `ujszovetseg/`, `melyelemzesek/` (a CLAUDE.md rétegtáblájának forrás-rétege; közvetlen `.md` fájlok, a `naplok/` almappa és a `Konnyu_ellenorzes*osszesito*` összesítők nélkül). Az F125.2 mérés (192) csak a `lexikon/` hatókörű volt.

- Régi: 192 jelzés (lexikon, első előfordulás szerint). Új: 729 jelzés összesen, ebből a `lexikon/` hatókörön 176, a tanulmányokon 553. `scope=python eszkozok/ellenoriz.py (teljes futás, 22. szabály) | forras=lexikon/*_TUDOMANYOS.md, tematikus_lezart/*.md, genezis/*.md, ujszovetseg/*.md, melyelemzesek/*.md | ts=2026-11-01T19:24+01:00`

**Javítás (ELLENOR_F125_2 4.): azonos bemeneten újramérve.** A fenti 192 → 176 összevetés két különböző bemeneten készült: a 192 a `24971b44` állapotán (16:52), a 176/729 a main merge UTÁN (19:24), és a merge a lexikonlapokat is megváltoztatta (ALVIL-001_TUDOMANYOS, ISTENTISZT-001_TUDOMANYOS), ezért a különbség nem csak a szabályváltozásból ered. Ugyanazon a HEAD-en (`be458e5b` munkafa-adatai, ideiglenes worktree), a két kódot egymás után futtatva:

- Régi kód (`ca82e428~1`: `ellenoriz.py` és `kiejtes_szoveg.py`): **186** jelzés, mind a `lexikon/` hatókörön (a régi kód csak azt nézte), tanulmány: nincs mérve.
- Új kód (a mostani `ellenoriz.py`): **729** jelzés, ebből `lexikon/` **176**, tanulmány **553**.
- Azonos bemeneten tehát a lexikon-hatókörön a szabályváltozás hatása 186 → 176 (-10); a korábban jelzett 192 → 176 különbség 6 jelzése a merge által módosított lexikonlapok bemenet-különbsége. A 729 értéke (176 + 553) nem változott.

`scope=python eszkozok/ellenoriz.py `szabaly22_kiejtes_hiany` (a 22. szabály, mindkét kód ugyanazon a munkafa-adaton, HEAD be458e5b) | forras=lexikon/*_TUDOMANYOS.md, tematikus_lezart/*.md, genezis/*.md, ujszovetseg/*.md, melyelemzesek/*.md | ts=2026-11-01T19:47+01:00`

## DT474 — commit-granularitás

A felhasználó döntése (DT474, 2026-11-01, az orkesztrátor-session továbbításával): „a) elfogadjuk”. Az `e6e7955d` (üzenet: „F125.2: eszköz és JELENTÉS-szabályok (22–23.), tesztek, DT471 eldöntve; F125.1: szövegjavaslat ⛔”) két tételt visz egy commitban; a pusholt történetet nem írjuk át (force-push nincs), a DT447 mintájára ez a helyesbítés.

Mely tétel mely fájlt érintette (`git show --stat e6e7955d`):
- F125.2 (eszköz, szabályok, mérés, DT471): `eszkozok/proza_lefedettseg.py`, `eszkozok/teszt_proza_lefedettseg.py`, `eszkozok/ellenoriz.py`, `DONTESEK.md` (DT471 sora), `naplok/GERINC_KARTYA_SZOVEG_naplo.md`.
- F125.1 (szövegjavaslat ⛔): `naplok/F125_SZOVEGJAVASLAT.md`; a brief hatókörének bővítése: `F125_GERINC_KARTYA_SZOVEG_BRIEF.md` (a fejléc).

## DT475 — gyűjtő mondat

A felhasználó döntése (DT475, 2026-11-01, az orkesztrátor-session továbbításával): „Igen, a+b+c”. Az orkesztrátor értelmezése: (a) az összlétszámmal egyező N nem gyűjtő mondat; (b) a gyűjtő mondatban név szerint megnevezett helyek levonódnak az N-ből; (c) mindkettőre teszt. Alkalmazva: `eszkozok/proza_lefedettseg.py` `mer()`: az N-t a motívum `adat/elofordulasok.tsv`-beli sorainak száma (`len(el)`, ugyanaz a forrás, amelyből a lefedettség is számol) ellen vetjük; egyenlőségnél a mondat kimarad; különben keret = N − (a bekezdésben megnevezett előfordulás-sorok száma), a csoportos fedés a legnagyobb keretig terjed. A mondat azonosítása változatlanul a bekezdés. Értelmezés: az egyenlőség a sorok számával történik; a szkript egyedi igehelyet nem számol (ALVIL-001-en a 72 sor 72 különböző igehely, így a két mérték egybeesik, és az „N egyedi igehely” 64-es/63-as mondata nem összlétszám-mondat: a teljes ÓSZ-i részhalmazra szól, tehát gyűjtő marad).

Tesztek: `test_dt_f125e_osszletszam_mondat_nem_gyujto` (5 előfordulás, „5 igehely”, 2 megnevezve → 0 csoportos, 3 hiány), `test_dt_f125e_megnevezett_helyek_levonodnak` („3 igehelyen”, mind a 3 megnevezve + 3 név nélküli → 0, 3), `test_dt_f125e_vegyes` („4 igehelyen”, 1 megnevezve, 5 név nélküli → 3 fedett, 2 hiány). A régi kódon mindhárom elbukik (21 teszt, 3 hiba), az újon mind zöld.

Újramérés (előfordulás-rovat: adat, megnevezve, csoportosan fedett, hiány):

| motívum | régi | új |
|---|---|---|
| ISTENTISZT-001 | 33, 33, 0, 0 | 33, 33, 0, 0 |
| ALVIL-001 | 72, 15, 57, 0 | 72, 15, 57, 0 |
| TEREMT-002 | 3, 3, 0, 0 | 3, 3, 0, 0 |

A három valódi motívumon a szám nem változik (ISTENTISZT-001-en és TEREMT-002-n a megnevezés már teljes, ezért az összlétszám-mondat kiesése nem hoz hiányt; ALVIL-001-en a keret 64−4 = 60, illetve 63−1 = 62 ≥ 57). A javítás a kitett hibaosztályt zárja, nem e három mért értéket változtatja.

`scope=python eszkozok/proza_lefedettseg.py ISTENTISZT-001 ALVIL-001 TEREMT-002 (régi: bdae32ef kódja, új: F125.27 munkafa; osszesit()['el']) | forras=motivumok/ISTENTISZT-001.md, motivumok/ALVIL-001.md, motivumok/TEREMT-002.md, adat/elofordulasok.tsv | ts=2026-11-01T20:30+01:00, ág-HEAD bdae32ef` — *a `ts` utólag írt, nem a futásé; a mérés a „DT475 — a névfelismerés javítása” szakasz újramért, valódi időbélyegű sorában áll (ELLENOR_F125_3 1.).*

### DT475 — a névfelismerés javítása (ELLENOR_F125_3 1.)

A `megnevezett()` két hibája, az ellenőr jelentése szerint: (a) a kötőjeles ragos alak („Hós 13:14-ben”, „Zsolt 49:15-ben”, „Jel 1:18-ban”) üres versek-halmazt adott, mert a záró kötőjel után `int('')` hibát nyelt a kód; (b) a „Mát 11:23” nem egyezett az adatbeli `Mt 11:23`-mal. Javítás: a verscsoport záró `-`, `–`, `,` karaktere rag, nem tartomány (a tartományhoz számjegy kell a kötőjel után, így a „Jel 20:13-14” és az „1Móz 1:1–3” változatlanul tartomány). A „Mát” nincs a `konkordancia/Konyv_normalizalo_tabla.tsv`-ben (a tábla `Mt`-hez nem vesz fel forrás-alakot), és nincs közös normalizáló-függvény a magyar prózai alakokra (az eszkozok/f3_4_*.py szkriptek saját helyi `HOSSZU` szótárat tartanak), ezért a legszűkebb, kódban dokumentált kiegészítés: `KONYV_VALTOZAT = {'Mt': ('Mát',)}`, csak a ténylegesen előforduló változat. Tesztek: `test_ragos_alak_megnevezi_a_verset` és `test_konyvnev_valtozat_mat` (a régi kódon elbuknak), `test_ragos_alak_nem_fed_mas_verset` és `test_tartomany_tovabbra_mindket_verset_fedi` (védőtesztek); összesen 25 teszt, mind zöld az újon.

Újramérés (előfordulás-rovat: adat, megnevezve, csoportosan fedett, hiány):

| motívum | F125.27 (ts-hibás sor) | F125.32 |
|---|---|---|
| ISTENTISZT-001 | 33, 33, 0, 0 | 33, 33, 0, 0 |
| ALVIL-001 | 72, 15, 57, 0 | 72, 17, 55, 0 |
| TEREMT-002 | 3, 3, 0, 0 | 3, 3, 0, 0 |

ALVIL-001: a keret az ellenőr szerint a :13 gyűjtő mondaton 64−5 = 59, a :23-on 63−3 = 60; mindkettő ≥ 55, a hiány 0 marad.

`scope=python eszkozok/proza_lefedettseg.py ISTENTISZT-001 ALVIL-001 TEREMT-002 (osszesit()['el']; ág-HEAD 19db9998 + F125.32 munkafa) | forras=motivumok/ISTENTISZT-001.md, motivumok/ALVIL-001.md, motivumok/TEREMT-002.md, adat/elofordulasok.tsv | ts=2026-11-01T20:12:50+01:00`

### DT475 — hatókör: mondat (ELLENOR_F125_3 3.)

A felhasználó döntése (2026-11-01, az orkesztrátor-session továbbításával): „Igen, mondatból”. Alkalmazva: `eszkozok/proza_lefedettseg.py` `mer()`: a gyűjtő mondat N-jéből csak az ugyanabban a mondatban név szerint megnevezett előfordulások vonódnak le; az új `mondatok()` bont (határ: `.`, `!`, `?` után szóköz és nagybetűs/idézőjeles/zárójeles kezdet; nem vág a „12.” típusú, csak számjegyből álló sorszámnál és a kisbetűvel folytatott rövidítésnél, de vág a „Hós 13:14.” igehely-záró ponttal). Az összlétszám-szabály és a csoportos fedés logikája változatlan. Tesztek: `test_dt_f125e_levonas_a_mondatbol_nem_a_bekezdesbol` (egy bekezdés, két mondat: „4 igehelyen” + 1 megnevezett, a második mondatban 2 további; keret 4−1 = 3, a régi kódon fedett 1 / hiány 4 → `(8, 3, 1, 4)`, az újon `(8, 3, 3, 2)`), `test_mondatbontas_sorszam_es_rovidites_nem_vag`; 27 teszt, mind zöld az újon.

Újramérés (előfordulás-rovat: adat, megnevezve, csoportosan fedett, hiány):

| motívum | F125.32 | F125.35 |
|---|---|---|
| ISTENTISZT-001 | 33, 33, 0, 0 | 33, 33, 0, 0 |
| ALVIL-001 | 72, 17, 55, 0 | 72, 17, 55, 0 |
| TEREMT-002 | 3, 3, 0, 0 | 3, 3, 0, 0 |

A három valódi motívumon a szám nem változik (az ALVIL-001 gyűjtő mondatai egy mondatban nevezik meg a helyeiket, vagy a keret így is ≥ 55).

`scope=python eszkozok/proza_lefedettseg.py ISTENTISZT-001 ALVIL-001 TEREMT-002 (osszesit()['el']; ág-HEAD e1690e0f + F125.35 munkafa) | forras=motivumok/ISTENTISZT-001.md, motivumok/ALVIL-001.md, motivumok/TEREMT-002.md, adat/elofordulasok.tsv | ts=2026-11-01T20:13:58+01:00`
