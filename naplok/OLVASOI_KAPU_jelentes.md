# Olvasói kapu — jelentés (2026-11-02)

*Végrehajtó: `claude-opus-5-5` (kért: opus; egyezik). Ág: `claude/olvasoi-kapu-c7019a`, tételek: OLVK.1–5.*
*Bemenet: a független lap-átvilágítás (2026-11-02, a megosztott jegyzetmappában: `LAP_ATVILAGITAS_2026-11-02.md`,
„Mi gépesíthető” táblázat), `naplok/1A_PROZA_jelentes.md` (PR #593), `eszkozok/muhely_allapot.py`, `eszkozok/ellenoriz.py`.*

A felhasználó (2026-11-02, az orkesztrátornak): „legyen igy. De a gate-eket amiknek ez ilyen hibát meg kellet volna
fogni irjuk meg.” Korábban („mehet”): a lezárás feltétele egy gépi és egy vizuális lapellenőrzés, 9. Feed-kapuként
(DT-F156k; a DT497 (3) ebben a pontban visszavonva).

## 1. Mi készült

| Elem | Fájl | Mit csinál |
|---|---|---|
| Gépi olvasói kapu | `eszkozok/olvasoi_kapu.py` | 19 ellenőrzés egy generált lapon; BUKÁS / FIGYELMEZTETÉS, sor, idézet; az azonos hiba ismétlődései egy tételbe vonva (`db`, `sorok`) |
| Tesztek | `eszkozok/teszt_olvasoi_kapu.py` | 42 teszt: az átvilágítás gépesíthető példái (negatív), az arany lap jó részei (pozitív), az arany lap G-sorai a valódi lapon |
| 9. Feed-kapu | `eszkozok/muhely_allapot.py` `kriterium_9` | zöld, ha 0 BUKÁS ÉS rögzített a felhasználó vizuális átnézése a lap mai változatáról |
| Feed-felület | `eszkozok/muhely_felulet/index.html`, `olvaso_elonezet.py` | 9. oszlop („Olvasói átnézés”), „kilenc kapu” |
| Károli-KH épség | `eszkozok/karoli_kh_epseg.py`, `naplok/KAROLI_KH_EPSEG_jelentes.md`, `naplok/KAROLI_KH_gyanus.tsv` | a másolt KH-listák felmérése a teljes táblán; N-F156a |
| Mérés | `naplok/OLVASOI_KAPU_meres.md` (generált) | motívumonként a javítandó lista — az új cikkek bemenete |

## 2. Az ellenőrzések és az átvilágítás sorai

| Ellenőrzés | Súlyosság | Elkapja (átvilágítás) |
|---|---|---|
| BELSO — DT/DT-F/N/F-tétel, #nnn, P1–P7, ELLENOR_, orkesztrátor, gerinc, .tsv/.py/.md, `manual`, „tanítói fájl” | BUKÁS | A4, A21 (1/a), T3 (P2/P4), T11 (`manual`), G4, G5, G7 |
| MOTIVUM_ID — más motívum ID-ja link nélkül | FIGY | A21 („l. HODIT-001”), T14 |
| PONT — „N. pont” nem létező szakaszra / rossz névvel BUKÁS, egyébként FIGY | BUKÁS/FIGY | T3 |
| ANGOL — szólista (study, gap, scan, was called, LXX_OS, `Isa.34.11` alak …) | BUKÁS | A22, T11, G4 |
| ANGOL_SOR — ≥3 angol funkciószó egy sorban | FIGY | (zsargon-maradék) |
| IDEZOJEL — egyenes `"` | BUKÁS | A10, G8 |
| ATIRAS — egy héber/görög szó két kiejtéssel | BUKÁS | A11 (hádész/hadész), T7 (tóhú/tohu, vábóhú/vávóhú) |
| ATIRAS_VALT — ékezet-eltérő változat dőlt/zárójeles helyen | FIGY | A11, T7 (*tohu va-vohu*) |
| KONYV — rövidítés nem a `Konyv_normalizalo_tabla.tsv` alakjával | BUKÁS | A11 (Mát, Mat, Ésa, Ezék, Csel), T16 |
| BDB_JEL — `^`, `®`, `°`, rafe, héberhez tapadt latin betű, `,,` | BUKÁS | A12, A23, T8, G9 |
| ZAROJEL — nyitva maradt zárójel (bekezdés-szinten) | BUKÁS a 2. szakaszban, máshol FIGY | T9 |
| FUNKCIO_URES — üres „Funkció” cella az 1. táblában | BUKÁS | A1 |
| IDEZET — az 1/a idézet nem a fölötte álló Károli-vers, és nincs „saját fordítás” jelölés | BUKÁS | A8 |
| KIVONAT_SZAM — Kivonat-darabszám ↔ 1. tábla / LXX-összesítő | FIGY | A7, T4 |
| KOLOFON — Kiadás, Próza modellje, Változásjegyzék, üres törzsadat | BUKÁS | A18, T13 |
| HIANYJEL — „*(nincs …)*”, „nincs a szakasztáblában” | FIGY | T10, G6 |
| SZINT_ALATT — hiányt jelző mondat; értelmező szakasz < 25% az arany lapénál | FIGY | A16, T12 |
| KH_MASOLT — a Károli-KH lista más vers másolata | FIGY | A5, T5, G1 |
| LABJEGYZET — definíció nélküli lábjegyzet (átvett: `ellenoriz.lap_labjegyzet_hianyok`, #595) | BUKÁS | T1 |
| PROZA_1A — 1/a próza és „Funkció:” (átvett: `proza_1a.meres`, #593, a main-re kerülése után) | BUKÁS | A2, T2, G2 |

**Nem gépesítve (kézi olvasói kapu marad):** A3, A6, A15, A17, A19, A20, A25, T15, T17, T18 (szemantika vagy sablonmondat
értelme); A9/T6/G3, A24 (a nézet, nem a lap); A13 (a BDB-sajtóhiba és a lábjegyzet „javítva” ellentmondása — nincs
általános mintája). A technikai dőlt sorokat (A14, A21 696/793: „*Szótári gerinc (DT272)…*”) a feladat szerint a kapu
kihagyja; ezek a Jelmagyarázat szerint a lap készítőinek szólnak.

## 3. Kalibráció az arany lapon (ISTENTISZT-001)

Első futás: 326 BUKÁS / 42 FIGY (soronként). Az ismétlődések összevonása (az 1/b ugyanazt az „F110 szűrő (DT283)”
jelet 20 sorban hordozza) után és a hamis pozitív osztályok kizárásával: **61 BUKÁS / 10 FIGY**.

| Kizárt hamis pozitív osztály | Javítás |
|---|---|
| a Thayer angol eredetijének szó szerinti idézete (`>` blokk) | az idézetblokk nem olvasói próza (a BDB_JEL fut rajta) |
| kézi sortöréssel tördelt bekezdés zárójele | a zárójel-egyensúly bekezdés-szinten |
| a táblacellába ágyazott proveniencia (`scope=… | forras=… | ts=…`, „forrás: `fájl`”) és a „Forrás” oszlop | kivágva |
| az Irodalom szakasz fájl-hivatkozása | a „belső fájl” szabály ott nem fut |
| a magyar „is” és „be” mint angol funkciószó; az „explicit” (magyar szó) | kivéve a listákból |
| a szótárak angol szövegében fordított sorrendű héber szócsoport | a kiejtés-párosítás mindkét irányt próbálja |
| a szakasz saját számozott alpontja („a 2. pont a fő szótár”) | nem jelez |
| deuterokanonikus/pszeudepigráf könyv (Sir, 1Énokh), mondatkezdő „Az 5:29”, bibliográfiai „Element. 2:6” | kivéve |
| a szótár alakját szó szerint idéző „a BDB-ben: „1Kin 18:24”” | kivéve |
| a Károli-vers „Seol” alakja | a Károli-sor nem kiejtés-forrás |
| az előfordulás-számmal arányos szakaszok (1., 1/b, 2–4.) hossza | a szintmérés csak az 5., 5/b, 6., 6/b, 7. szakaszon |
| a Károli-idézet modernizált helyesírással vagy kihagyott szavakkal | szavanként ≥ 0,75 hasonlóság, sorrendben, a darab szószámáig terjedő kihagyással |

**A maradék 61 BUKÁS, kézzel osztályozva:** a G-sorok mind megjelennek (G1 KH_MASOLT ×3, G4 BELSO/ANGOL, G5 BELSO
`jeloltek.tsv`, G6 HIANYJEL, G7 BELSO DT476, G8 IDEZOJEL, G9 BDB_JEL; G2/G3 a #593 és a nézet tétele). Azon túl valós,
az átvilágítás által nem listázott hibák: 5 jelöletlen saját fordítás az 1/a-ban (2Móz 33:19 „kihirdetem” ↔ Károli
„kiáltom”; 2Móz 34:5; 1Kir 18:24; Zsolt 116:4; Jóel 2:32), régi/idegen könyvrövidítések (Zef ×2, Csel, Ám, Lk, 1Jn),
belső fájlutak a 6/b és 7. szakaszban, „scan”, „LXX_OS” a prózában, egy kiejtés-ingadozás (Jahve/JHVH).
**Mért hamis pozitív: 1 biztos** (1664: a *Discipleship Evangelism study guide* angol könyvcím „study” szava) **és
1 bizonytalan** (759: a BDB „(||” párhuzamjele nyitott zárójelnek számít; lehet valódi csonkulás is). A FIGYELMEZTETÉS-ek
közül a 3 PONT a forrás saját számozására mutat (valós), a 2 MOTIVUM_ID a generált „Mit mutat” sorban áll (valós).

**Következmény:** az arany lap a jelenlegi súlyossággal a 9. kapun **piros**. Ez ⛔ kérdés az orkesztrátornak
(lásd 6.).

## 4. Mérés mind a 9 lapon

| Motívum | BUKÁS | FIGYELMEZTETÉS | Legnagyobb tételek |
|---|---|---|---|
| ALVIL-001 | 145 | 17 | PROZA_1A 72, IDEZET 43, BELSO 10, KONYV 5, IDEZOJEL 4, KOLOFON 3, FUNKCIO_URES 1 (72 cella) |
| ANTROP-001 | 37 | 8 | PROZA_1A 8, BELSO 10, IDEZOJEL 6, KOLOFON 4, IDEZET 4 |
| HAMART-001 | 118 | 12 | PROZA_1A 52, BELSO 20, KONYV 12, ANGOL 9, ATIRAS 9 |
| HODIT-001 | 78 | 24 | PROZA_1A 33, BELSO 16, ANGOL 8, IDEZET 7, IDEZOJEL 6, PONT 12 (F) |
| ISTENTISZT-001 | 61 | 7 | BELSO 25, ANGOL 9, IDEZOJEL 9, KONYV 6, IDEZET 5 |
| KIRALY-001 | 50 | 19 | PROZA_1A 8, BELSO 13, IDEZOJEL 8, ANGOL 7, PONT 5+9 |
| MENNY-001 | 45 | 29 | PROZA_1A 9, BELSO 14, ANGOL 6, IDEZOJEL 6, ATIRAS_VALT 9 (F) |
| TEREMT-001 | 109 | 19 | PROZA_1A 41, IDEZET 28, BELSO 14, KONYV 7, IDEZOJEL 7, KH_MASOLT 7 (F) |
| TEREMT-002 | 32 | 28 | PROZA_1A 1, BELSO 9, ANGOL 7, KOLOFON 5, PONT 3+8, ATIRAS 3, ATIRAS_VALT 12 (F) |

A #593 merge-e óta a PROZA_1A (az 1/a igehelyenkénti prózája, `proza_1a.meres`) is mér: igehelyenként egy BUKÁS, ahol a próza töredék vagy hiányzik, vagy nincs „Funkció:” sor (9 lapon 224; az arany lapon 0). A sorszám ezeknél 0 (a mérő igehelyet ad, nem sort).

Tételenként, sorszámmal: `naplok/OLVASOI_KAPU_meres.md`. A számok különálló hibák (egy szakaszon belül az ismétlődés
egy tétel). A LABJEGYZET a #595 merge-e után aktív: mind a 9 lapon 0. A PROZA_1A a #593 merge-e után kapcsol be
(addig a kimenet jelzi, hogy nem mért). Az öt régi sablonú lap (ANTROP, HAMART, HODIT, KIRALY, MENNY, TEREMT-001) a
régi generátorral készült; a számuk az új cikkek kiinduló javítandó listája, nem a régi lap javítási terve.

## 5. Károli-KH épség

`naplok/KAROLI_KH_EPSEG_jelentes.md`: a 19 817 forrásversből 12 322 listája szó szerint megegyezik egy másikéval;
**5 471 gyanús másolat** (8 688 KH-sor), a minták valódi hibát mutatnak (Act.2.27 = Act.7.14, Dan.3.10 = Dan.12.7,
Heb.6.19 = Heb.12.5). Az átvilágítás 11 ismert esetéből 9-et fog meg; az egyedi (nem duplikált) hibás listát (ApCsel
22:16 → Jón 1:5; Péld 9:18) nem — ez korlát. A javítás előtt a nyers HunKar-forrás és a 2026-08-24-i konverzió
vizsgálata kell (forrás- vagy konverziós hiba?): **N-F156a**. A lapon addig KH_MASOLT figyelmeztetés.

## 6. Döntések (az orkesztrátor, a felhasználó 2026-11-02-i felhatalmazásával)

- **DT-F156l (b):** a vizuális átnézés helye az `adat/lap_atnezesek.tsv` (SEMA 2.48), a lap commitjához kötve. A `ki`
  csak „felhasználó” lehet, az `idezet` az ő szavai szó szerint; üres idézettel vagy más szerzővel a sor nem érvényes
  (`muhely_allapot.atnezes_ervenyes`, teszttel). A tábla ma üres, ezért a 9. kapu minden lapon piros.
- **DT-F156m (1):** a kapu az arany lapra is érvényes, az ISTENTISZT-001 8/9. A kiadott lap a Stash-ben marad, a
  `kiadas_allapot` mondattal („Az 1. kiadás érvényes; a 2. kiadás javítandói nyitottak.”); ez a Feed Stash-táblájában
  („Kiadás” oszlop) és az olvasói előnézet kártyáján is látszik. Végponttól mérve (`muhely_allapot.py --motivum
  ISTENTISZT-001 ALVIL-001`): az arany lap 8/9, a Stash-ben marad; az ALVIL-001 6/9.
- **DT-F156n (1): a másolat-gyanús KH-listák nem kerülnek a lapra** (OLVK.10). A generátor (`lexikon_general.py`
  `kh_index`) kihagyja őket, a 4. szakasz hatókör-sora megnevezi a kimaradt igehelyeket; a három migrált lap
  (ISTENTISZT-001, ALVIL-001, TEREMT-002) újragenerálva, csak a 4. szakasz és a Minősítés összesítője változott
  (szó szerint: `naplok/KH_ELREJTES_lapdiff.md`). Az orkesztrátor két feltétele:
  - *Soronkénti igazolás* (`naplok/KH_ELREJTES_igazolas.md`): az első mérés 52 sora (35 forrásvers) közül a Károli-szöveg
    alapján 3 forrásvers / 3 sor hamis gyanú volt (Péld 1:12 → Jób 26:6, 1Krón 20:4 → Józs 21:21, Zsolt 76:3 →
    Zsolt 132:13: közös szó seol, Gézer, Sion). Ezek megmaradnak, a szabály pontosítva: nem gyanús a lista, ha valamelyik
    eleme 150-nél kevesebb versben álló tartalmi Strong-számon osztozik a forrásverssel. Elrejtve: **49 sor
    (32 forrásvers)**; 25 igehely-fejléc ürült ki. Bizonytalan, elrejtve: Hab 2:17 → Ézs 33:1 és Zsolt 49:15 → Jób 27:17
    (tartalmilag rokon, közös Strong nélkül). **A Minősítés KH-párjai közül egy sem esik ki** (az első mérés egyetlen
    kieső párja, Péld 1:12 → Jób 26:6, éppen a hamis gyanú volt).
  - *Az arany lap változása* a 2. kiadás függő változása: **N-F156b** (Zsolt 116:13, ApCsel 2:21, ApCsel 9:14; 5 sor;
    a 4. szakasz összesítője 26 → 21 utalás).
  - *Feed 3. kapu* (egyforrású, nulla-diff újragenerálás, `muhely_allapot.kriterium_3`) a három újragenerált lapon:
    ISTENTISZT-001, ALVIL-001, TEREMT-002 — mind **zöld (nulla-diff)**.
  - Az új mérés (4. szakasz tábla, `naplok/OLVASOI_KAPU_meres.md`) az újragenerált lapokon fut; a régi sablonú lapok
    FIGYELMEZTETÉS-száma is változott, mert a pontosított szabály kevesebb listát tart gyanúsnak.
  - **Korlát:** a 150-es küszöb a 9 lap 35 forrásversén kalibrált (a valódi kapcsolatok közös szava 14–139 versben áll, a
    hamis felmentéseké 150–205-ben). **A teljes 5 078 gyanús forrásversre nincs igazolva**; a hamis gyanú és a meg nem fogott
    másolat aránya a teljes táblán ismeretlen. Ez az N-F156a feladata (a nyers HunKar-forrással együtt).

## 7. Az arany lap 2. kiadásának javítandói, osztályonként (DT-F156m)

A 2026-11-02-i mérés 61 BUKÁS-tétele (az orkesztrátor üzenetében „63”: az a kalibráció korábbi állása; az idézet-tűrés
2 hamis jelzést megszüntetett). Sorszám: a `lexikon/ISTENTISZT-001_TUDOMANYOS.md` mai Markdown-sora; a teljes lista
idézettel: `naplok/OLVASOI_KAPU_meres.md`. A „hol javítandó” a valószínű forrás (a lap generált: a javítás a forrásban
történik, utána újragenerálás).

| Osztály | Tétel / előfordulás | Mi | Hol javítandó |
|---|---|---|---|
| BELSO | 25 / 167 | az 1/b indokaiban `F110 szűrő (DT283)`, `DT476 K2/K4`, `DT478`, `N59`, „orkesztrátor-chat”, `motivumok.tsv`; a Minősítés napló-fájlneve (1217–1220); `DT479`, `DT280` az 5. szakaszban; `DT476 K5` az 1/a-ban (206, 212); belső fájlutak és „tanítói fájl” a 6/b-ben és a 7.-ben (1633, 1637, 1657, 1664, 1721) | `adat/jeloltek.tsv` indoklás · `adat/kapcsolatok.tsv` · a kézi forrás (`motivumok/ISTENTISZT-001.md`) |
| IDEZOJEL | 9 / 67 | egyenes `"` a Kivonatban (9), az 1/a-ban (176–280), az 1/b-ben, a Rokon szavakban, a Minősítésben, a 6. PaRDeS-keretben (1424–1434) és a 7.-ben | kézi forrás; `jeloltek.tsv`; a szótári fordítás |
| ANGOL | 9 / 31 | „was called”, „having been called” (1/b), „LXX_OS” (807, 809), „study” (1586, 1624, 1695–1714), „gap” (6/b tábla), „scan/scanje” (1675, 1720); a 1664 „study guide” könyvcím — hamis jelzés | `jeloltek.tsv`; a generátor (LXX-híd mondata); kézi forrás |
| KONYV | 6 / 13 | „Zef” (328, 1222), „Csel” (1185, KH-megjelenítés), „Ám” (1595, 1615), „Lk”, „1Jn” (a TBESG/LSJ-fordításban) | `jeloltek.tsv`; a KH-tábla megjelenítő alakja (generátor: a normalizáló tábla alakjára kell fordítani); kézi forrás; szótári fordítás |
| IDEZET | 5 / 5 | jelöletlen saját fordítás az 1/a-ban: 2Móz 33:19 „kihirdetem” (Károli: „kiáltom”), 2Móz 34:5, 1Kir 18:24, Zsolt 116:4, Jóel 2:32 | kézi forrás (`kapcsolodas`) |
| BDB_JEL | 4 / 10 | `®°` (653), `^` (659–750), rafe (736, 750), `,,` (736, 750) | a BDB-fordítás / forrásszöveg (`adat/bdb_szakasz_hu.tsv`) |
| ZAROJEL | 2 / 2 | csonka BDB-szakasz (722 „(vö. Qal 5”); 759 bizonytalan (a BDB „(||” jele) | `adat/bdb_szakasz_hu.tsv` |
| ATIRAS | 1 / 1 | יְהוָה: „Jahve” (81) és „JHVH” (407) | kézi forrás és a Jelmagyarázat egységesítése |

FIGYELMEZTETÉS (nem blokkol, a 2. kiadásban átnézendő): PONT ×3
(„a tematikus study 2. és 3. pontjába”, „l. 1. pont”), MOTIVUM_ID ×2 (a 5/b „Mit mutat” sora), HIANYJEL ×1 (16 cellában
„*(nincs hozzárendelés)*”), ATIRAS_VALT ×1 (epikaleszetai / epikaleszétai).

## 8. Korlátok és követő tételek

- A súlyosságok a jelen kalibráció; a BELSO/ANGOL listák bővíthetők, ha új zsargon jelenik meg.
- A briefek (`F10_LEXIKON_LEZARAS_BRIEF.md`, `F123_MIGRACIO2_BRIEF.md`) „Feed 8/8” szövegét ez az ág nem írta át (a saját
  menetük fejléce); a `MUNKAMENET.md` C5 sora frissült.
- A PR #593 a `muhely_allapot.py` 6. kapuját és a `teszt_muhely_allapot.py`-t is módosítja: a később mergelt PR-nak
  a két változást össze kell fésülnie (a 6. kapu `proza1a` mezője és a 9. kapu egymástól független).
