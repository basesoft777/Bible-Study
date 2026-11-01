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

Küszöbök (javaslat, DT-F125a): kevés = 150 karakter/elem alatt; eltérés = 4x a blokkok mediánjától; legalább 3 megnevezett elem.

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

Küszöbök (javaslat, DT-F125a): kevés = 150 karakter/elem alatt; eltérés = 4x a blokkok mediánjától; legalább 3 megnevezett elem.

Adatelemet egyáltalán nem megnevező bekezdés (értelmező, módszertani): 5 / 13


## DT-F125a — eldöntve (1. változat)

A felhasználó („a javaslat szerint”, az orkesztrátor-session idézetével): 150 karakter/elem alatt „kevés”; a blokk-medián négyszeresénél távolabb „egyenetlen”; legalább 3 elem; a csoportos említés külön kategória. Rögzítve: `DONTESEK.md`.

## F125.2 — eszköz és JELENTÉS-szabályok

- `proza_lefedettseg.py`: új „csoportosan fedett” oszlop (a „N egyedi igehely” gyűjtő mondat, csak az előfordulásokra; ALVIL-001: 72 / megnevezve 15 / csoportosan fedett 57 / hiány 0). A mérő nem tudja, a gyűjtő mondat melyik igehelyeket fedi: csak darabszám szerint kezeli. A fedett darabszám a gyűjtő mondat N-jéig terjed (legfeljebb a prózában álló legnagyobb N, a többi név nélküli előfordulás hiány marad; javítás: ELLENOR_F125 1., F125.6).
- `ellenoriz.py` 22. szabály (kiejtés nélküli héber/görög szó a `lexikon/*_TUDOMANYOS.md`-n, `kiejtes_szoveg.elemez`) és 23. szabály (próza-lefedettség a `motivumok/*.md`-n), mindkettő JELENTÉS, nem gátol. Mért: 22 → 192 jelzés, 23 → 77 jelzés a mai main-en. A 22. közelítés: a szakasz későbbi kiejtése nem pótolja az első előfordulás hiányát. *(A DT-F125b óta nem érvényes: l. „DT-F125b — a 22. szabály”.)*
- Tesztek: `teszt_proza_lefedettseg.py` (11, zöld) a két szabályt is lefedi; a briefben szereplő külön `teszt_ellenoriz_proza.py` nem készült (egy fájl, két téma).

## ⛔ A szövegjavaslatok

`naplok/F125_SZOVEGJAVASLAT.md` (13 sor). Jóváhagyásig a MUNKAMENET-hez és a sablonokhoz nem nyúltam.

## F125.3 — a szövegjavaslat jóváhagyva, beírva

A 13 pont jóváhagyása (az orkesztrátor-session idézete; előbb a jóváhagyást visszavonták, majd újra megadták): az orkesztrátor a 13 pontot négy csoportban mutatta be („mind a 13 mehet”), a felhasználó válasza szó szerint: **„a javaslatod szerint”**. Beírva: `MUNKAMENET.md` (A3b, A3c, prioritási-térkép mondat, C-x, C-y, C-z, C-w), `2_` sablon v22, a kiejtés-szabály (K) az 1_, 2_, 4_, 5_, 6_ sablonban és a gyorsreferenciában, a 6_ sablon L és O szakasza és kolofon-kiadás sora, az olvasói elv a gyorsreferenciában, `.claude/commands/kiadas.md`. A C-x/C-y szövege az `F148` 6. szakaszából szó szerint (a brief hatókörét ezzel bővítettem).

Nincs kész: a kolofon kiadás-sorát a generátor még nem rendereli (a `lexikon_general.py` a #152 fájlja); a `6_` sablon ezt szabályként rögzíti. Nyitott tételként felvéve: `N-F125a` (`NYITOTT_FELADATOK.md`; ELLENOR_F125 4.).


## F125.9 — a mért számok proveniencia-sora és az újramérés (ELLENOR_F125 6.)

A fenti 57, 4, 192 és 77 szám az 1. tétel (F125.6) UTÁN újramérve, az ág `24971b44` állapotán; az eredmény a régivel egyező, eltérés nincs (az 57 azóta „csoportosan fedett”, mert a gyűjtő mondat N-je, 63, nem kisebb nála).

- ALVIL-001: 72 előfordulás, 15 megnevezve, 57 csoportosan fedett, 0 hiány; ISTENTISZT-001: 33/33 előfordulás megnevezve, 3 név nélküli kapcsolat + 1 nyitott jelölt = 4 név nélküli elem. `scope=python eszkozok/proza_lefedettseg.py ISTENTISZT-001 ALVIL-001 | forras=motivumok/ISTENTISZT-001.md, motivumok/ALVIL-001.md, adat/elofordulasok.tsv, adat/kapcsolatok.tsv, adat/jeloltek.tsv | ts=2026-11-01T16:52+01:00`
- 22. szabály: 192 jelzés; 23. szabály: 77 jelzés. `scope=python eszkozok/ellenoriz.py (teljes futás, a 22. és 23. szabály jelzésszáma; az eszköznek nincs szabályonkénti kapcsolója) | forras=lexikon/*_TUDOMANYOS.md (22.), motivumok/*.md és adat/*.tsv (23.) | ts=2026-11-01T16:52+01:00`

A régi (F125.2) mérés: 22 → 192, 23 → 77, ugyanezzel a paranccsal a mai main-en; az F125.6 nem változtatta a 23. szabály jelzésszámát.

## DT-F125b — a 22. szabály

A felhasználó döntése (DT-F125b, 2026-11-01, az orkesztrátor-session továbbításával): „a) kód a szöveghez”. A 22. szabály (`eszkozok/ellenoriz.py` `szabaly22_kiejtes_hiany`) a jóváhagyott K-szöveghez igazítva: egy héber/görög szót akkor jelez, ha a szakaszban (két `##`/`###` cím között) SEHOL nem kap kiejtést; ha bármelyik előfordulása kap, nem jelez (`kiejtes_szoveg.elemez_szakaszonkent`). A hatókör a `lexikon/*_TUDOMANYOS.md` mellett a tanulmányok is: `tematikus_lezart/`, `genezis/`, `ujszovetseg/`, `melyelemzesek/` (a CLAUDE.md rétegtáblájának forrás-rétege; közvetlen `.md` fájlok, a `naplok/` almappa és a `Konnyu_ellenorzes*osszesito*` összesítők nélkül). Az F125.2 mérés (192) csak a `lexikon/` hatókörű volt.

- Régi: 192 jelzés (lexikon, első előfordulás szerint). Új: 729 jelzés összesen, ebből a `lexikon/` hatókörön 176, a tanulmányokon 553. `scope=python eszkozok/ellenoriz.py (teljes futás, 22. szabály) | forras=lexikon/*_TUDOMANYOS.md, tematikus_lezart/*.md, genezis/*.md, ujszovetseg/*.md, melyelemzesek/*.md | ts=2026-11-01T19:24+01:00`

## DT-F125d — commit-granularitás

A felhasználó döntése (DT-F125d, 2026-11-01, az orkesztrátor-session továbbításával): „a) elfogadjuk”. Az `e6e7955d` (üzenet: „F125.2: eszköz és JELENTÉS-szabályok (22–23.), tesztek, DT-F125a eldöntve; F125.1: szövegjavaslat ⛔”) két tételt visz egy commitban; a pusholt történetet nem írjuk át (force-push nincs), a DT447 mintájára ez a helyesbítés.

Mely tétel mely fájlt érintette (`git show --stat e6e7955d`):
- F125.2 (eszköz, szabályok, mérés, DT-F125a): `eszkozok/proza_lefedettseg.py`, `eszkozok/teszt_proza_lefedettseg.py`, `eszkozok/ellenoriz.py`, `DONTESEK.md` (DT-F125a sora), `naplok/GERINC_KARTYA_SZOVEG_naplo.md`.
- F125.1 (szövegjavaslat ⛔): `naplok/F125_SZOVEGJAVASLAT.md`; a brief hatókörének bővítése: `F125_GERINC_KARTYA_SZOVEG_BRIEF.md` (a fejléc).
