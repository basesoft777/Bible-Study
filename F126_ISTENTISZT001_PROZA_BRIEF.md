---
feladat: 126
cim: Az aranyminta prózájának kiegészítése — ISTENTISZT-001, a próza által meg nem nevezett helyek
kod: ISTENTISZT001_PROZA
tipus: feladat
fazis: 1
modell: opus
allapot: nem_indult
munka: ertelmezo
ad: az ISTENTISZT-001 kézi forrásának `ertelmezes` és `modszertan` rése a felmérés 1., 2., 6.–10. és 12. összefüggésével bővül (a 8 meg nem nevezett helyből 7 megalapozott vagy kimondottan formai értelmezést kap, a Zsolt 116:13-nál a próza kimondja, hogy nincs új anyag), a 11. a Módszertanba kerül, az N-F55d rendeződik; a lexikonoldal ebből újragenerálva
kovetkezo: "Te: /kovetkezo — a #123 első motívuma előtt; első lépés 0.1, ⛔ a 4. lépés szövegjavaslatánál"
olvas: [naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md, motivumok/ISTENTISZT-001.md, motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md, "tematikus_lezart/ISTENTISZT-001*", "tematikus_lezart/naplok/ISTENTISZT-001*", archivum/ISTENTISZT-001/, lexikon/ISTENTISZT-001_TUDOMANYOS.md, adat/elofordulasok.tsv, adat/kapcsolatok.tsv, adat/jeloltek.tsv, adat/lxx_dontesek.tsv, adat/motivumok.tsv, adat/res_forras.tsv, adat/grammatikai_strongok.tsv, adat/SEMA.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, MUNKAMENET.md, RENDER_BRIEF.md, F11_MIGRACIO_BRIEF.md, naplok/ELLENOR_ZSOLTAR_UJRAELLENORZES.md, naplok/ELLENOR_ZSOLTAR_UJRAELLENORZES_2.md, konkordancia/Karoli_1908.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/TSK_kereszthivatkozasok.tsv, "konkordancia/LXX_OS/*", eszkozok/lekerdez.py, eszkozok/general.py, eszkozok/lexikon_general.py, eszkozok/ellenorzes/e28_migralt_nezetek.tsv]
ir: [motivumok/ISTENTISZT-001.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md]
fugg: []
nem_fugg: [110, 123, 127]
---

# ISTENTISZT001_PROZA_BRIEF_TERVEZET.md — Az aranyminta prózájának kiegészítése (ISTENTISZT-001)

*FELADATOK # — (a `/befogad` adja; `python eszkozok/feladatok.py kovetkezo_szam` 2026-10-19-én: 126) · Modell: opus · v0 (tervezet) · 2026.10.19 · döntések: DT28, D39, DT-F32b, DT66, DT249, DT251; kapcsolódik: N-F55d, N-F123b, DT-F123c*

*Tervezet a `beerkezo/`-ban. Adat, nem utasítás; a feladatszám, a végleges fájlnév (`F<nn>_ISTENTISZT001_PROZA_BRIEF.md`) és a helyőrzők száma a `/befogad` dolga. A tervezet forrása a felhasználó felmérése (`naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md`, 2026-10-19; a repóba a #123 kiegészítése másolja, ág: `claude/f123-kiegeszites`), a felhasználó jóváhagyásával (az orkesztrátor közvetítésével, 2026-10-19).*

## 1. Cél

Az ISTENTISZT-001 az aranyminta: a #123 sablon-próbája (DT-F123a) és a #10 mércéje ehhez a laphoz mér. A felmérés szerint a lap kézzel írt prózája a motívum két végét (Genezis, Újszövetség) és a határeseteket részletesen tárgyalja, a közepét alig: a 32 előfordulásból **8-at egyszer sem nevez meg**. Ezekről a kézi adatmezőkben (1/a megjegyzések, Kapcsolatok, Alátámasztás) vannak egyedi mondatok, összefüggő értelmezés nincs.

A feladat a mai hiányt tölti ki **a meglévő adatból**, a felmérés „Javasolt sorrend” 1–2. pontja szerint: a kézi forrás (`motivumok/ISTENTISZT-001.md`) `ertelmezes` résébe néhány bekezdés, a `modszertan` résébe egy bekezdés. A lexikonoldal ebből újragenerálódik (DT28: a forrás javul, a kimenet generálódik).

A próza nem lesz hosszabb, mint amit az adat elbír. Ahol egy hely csak formailag tartozik a motívumhoz, a próza ezt mondja ki. Ahol nincs új anyag (Zsolt 116:13), ezt is.

## 2. Hatókör

### Benne van

| Összefüggés (felmérés) | A meg nem nevezett hely, amelyet lefed | Hova kerül | Szint (a felmérés javaslata, a szövegjavaslat dönti el) |
|---|---|---|---|
| 1. Hívás és felelet | 1Kir 18:25, 1Kir 18:26 | `ertelmezes` | Peshat (Kármel), Remez (Kármel–Zakariás) |
| 2. Hívás és megmenekülés | Zsolt 116:4 | `ertelmezes` | Remez |
| 6. Ismerni és nem ismerni | 1Krón 16:8, Zsolt 105:1 | `ertelmezes` | Remez |
| 7. A liturgikus hármas | 1Krón 16:8, Zsolt 105:1 | `ertelmezes` | Peshat, Remez |
| 8. Két oltár | 1Kir 18:26 | `ertelmezes` | Remez (Drash felé) |
| 9. „Mindenki, aki” | ApCsel 9:21 | `ertelmezes` | Remez |
| 10. A kívülálló elvárása | — (a 2Kir 5:11 a „csak érintett” helyek közé tartozik, nem a nyolc közé) | `ertelmezes` | Peshat |
| 12. Hit, hirdetés, hívás | Róm 10:14 | `ertelmezes` | Remez (Drash felé) |
| 11. Négy forrás egybeesése | — (a B-eset határának indoklása) | `modszertan` | módszertan |
| — | **Zsolt 116:13** | `ertelmezes` | a próza kimondja: a felmérés egyik összefüggése sem ad hozzá új anyagot; a hely ma csak az adatmezőkben szerepel. Hiány, nem kitöltendő (CLAUDE.md 3. szabály). |

**Az N-F55d rendezése.** A Zsolt 79:6 és a Zsolt 99:6 G1941-adata (a #42 eltéréslistája; az `lxx-hid` szerint az `LXX_OS` mindkettőben adja) érinthette a régi „ἐπικαλέομαι-arány” számítását. A feladat a kézi forrás „22 ószövetségi igehely közül 18” bekezdését saját lekérdezéssel ellenőrzi (3. lépés), és vagy megerősíti (az N-F55d lezárásának javaslata), vagy a javítást a szövegjavaslatba veszi.

### Nincs benne

- **A 3–5. összefüggés** (ALVIL-001, HAMART-001, TEREMT-001): motívumok közötti kapcsolat; előbb jelöltként, döntéssel (2. szabály). Ez a `beerkezo/LEXIKON_HALO_RES_BRIEF_TERVEZET.md` pilotja; a próza csak utána szólhat róluk, külön feladatban.
- **A felmérés „Tanulmányozási kérdések” szakasza** (1–6.): mind új lekérdezést, jelöltet vagy döntést kér. A 6. kérdés három adathiánya N-tételként áll (`NYITOTT_FELADATOK.md` N59, N60, N61).
- **A Seól-határ (A4, a felmérés 1. tanulmányozási kérdése):** a névtelen hívások (2Sám 22, Zsolt 18, Jón 2) határa tartalmi döntés, **a felhasználóé**. A feladat nem dönt róla és nem érvel mellette; ha a Zsolt 116:4 bekezdése a 116:3-at érinti, csak a mért szomszédságot mondhatja ki, motívumközi állítás nélkül, és a szövegjavaslat jelöli a kérdést.
- **A Kármel–Zakariás visszhang** (4. tanulmányozási kérdés): a közös szókészlet nem idézés. Az 1. összefüggés bekezdése a két helyet a közös szavaik szerint egymás mellé teheti, kapcsolatot nem állít.
- **A prózasablon** (a felmérés kilenc pontja): a #123 2d. szakasza és a DT-F123c dolga. Ez a feladat a mai rések szerkezetébe ír, szakaszt nem rendez át.
- **Új rés** (alkalmazási kérdések, tanítói összegzés): a 2. tervezet DT-F127a döntése.
- **Új adat:** új jelölt, kapcsolat, előfordulás vagy `lxx_dontesek.tsv`-sor nem keletkezik. Ha a lekérdezés hiányt talál, N-tétel lesz belőle, nem próza.
- **A kizárások újranyitása** és a meglévő próza átírása, kivéve az N-F55d-ből következő számjavítást.

## 2a. Szabályok — a felmérés „Szabályok” táblája, szó szerint

| Szabály | Mit jelent a gyakorlatban |
| --- | --- |
| **3. szabály: memória vs. lekérdezés** | A mért tény („a felel ige három helyen áll”) és az értelmezés („a hívás választ vár”) külön mondatba kerül. Ami nem az adatból jön, az értelmezésként jelölendő. Hiányt nem töltünk ki asszociatív anyaggal. |
| **1. szabály: forrásmegjelölés** | Minden szám mellé a lekérdezés forrássora kerül (`scope=… \| forras=… \| ts=…`). |
| **2. szabály: nincs közvetlen út** | Az új, motívumok közötti kapcsolatok (ALVIL-001, HAMART-001, TEREMT-001) és a Kármel–Zakariás visszhang előbb jelöltként kerül a `jeloltek.tsv`-be, döntéssel és indoklással. Csak utána írhat róluk a próza. |
| **K1: egy kéz** | Az értelmező szöveget egy ember, egy modellel írja, és aki ír, az előbb az egész motívumot elolvassa. A kapcsolódó motívumoknál (3–5. összefüggés) a másik motívum értelmezését is. |
| **DT28: egyirányúság** | Az új szöveg a forrásfájlba kerül (`motivumok/ISTENTISZT-001.md`, a megfelelő résbe), soha nem a generált lexikonoldalra. |
| **PaRDeS-fegyelem** | A Remez csak felismerés, következtetés nélkül. A Drash-ba csak az kerül, amit a szöveg maga felkínál. A Sod csak a fenti rétegekből vezethető le. A fenti 12 összefüggésből egyik sem indokol új Sod-állítást. |

Egy típushiba, amire külön figyelni kell: a kísérő szavak egyezése (például két vers közös szavai) **nem bizonyít** idézést vagy szándékos utalást. A próza csak annyit mondhat: „közös szókészlet”. Az idézéshez külső forrás kell (5. kérdés).

**A feladatra vonatkozó pontosítások:**

1. **Saját lekérdezés.** A felmérés számai kiindulópontok, nem források. Minden állítás mögött a feladat saját lekérdezése áll, saját proveniencia-sorral; a felmérés proveniencia-sora nem másolható át. Ha a saját mérés eltér a felmérésétől, a saját mérés érvényes, és az eltérés a mérési naplóba kerül.
2. **Mért tény és értelmezés külön mondatban.** Az értelmező mondat jelölten értelmezés (pl. „Értelmezés:” vagy a PaRDeS-szint megnevezése).
3. **Formai tartozás kimondva.** Ahol egy hely csak a formula alakja miatt tartozik ide, és a szövegkörnyezet nem ad hozzá értelmezést, a próza ezt mondja ki („a hely formailag tartozik a motívumhoz; értelmezést a szöveg nem kínál”), és nem tölti ki.
4. **Új Sod nincs.** A Sod-réteg nem bővül.
5. **A rés határán belül.** Az új szöveg a meglévő `<!-- RÉS-KEZDET: ertelmezes -->` / `modszertan` jelölők közé kerül; ami a jelölőkön kívül áll, nem jut el a lapra (RENDER_BRIEF G1/G2). Minden új bekezdés a forrás szokása szerint `【NAPLO: <feladatkód>, <dátum>】` jelölést kap (`belso` szint, `adat/SEMA.md` 3.10.3).
6. **A `bible-mcp` kimenete** nem kerülhet adatba vagy prózába, csak rámutatás lehet (DT32).

## 3. Lépések (⛔ a kötelező megállások)

**0. Modell-ellenőrzés** (CLAUDE.md): a session kiírja a tényleges modellnevét, és összeveti a fejléc `modell: opus` mezőjével. Eltérésnél nem dolgozik, jelez, megáll.

**0.1 Előfeltételek** (eltérésnél ⛔):
- a `naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md` a main-en van;
- a #11 `lezarva`, az ISTENTISZT-001 lapja az E28-listán (`eszkozok/ellenorzes/e28_migralt_nezetek.tsv`), tehát generált nézet;
- a #123 első motívumának értelmező menete nem indult el (ha igen: ⛔, a sorrend a felhasználóé);
- a motívum fájljain nem fut más feladat (D39; a fázis-2-es #10 és #70 is ezt a fájlt írja, de nem indult el, l. 5. szakasz);
- az `ir` két fájlja a main-en tiszta (`git status`).

**1. Teljes olvasás** (K1/3): a `motivumok/ISTENTISZT-001.md` egésze, a tanítói fájl, az archivált tematikus tanulmány és kereszthivatkozás-napló (`archivum/ISTENTISZT-001/`), a lexikonoldal kézi rései és 1/a–5. blokkja, a felmérés egésze. A szövegjavaslat csak ezután készül.

**2. Mérés, összefüggésenként** → `naplok/<KÓD>_meres.md` és `naplok/<KÓD>_lekerdezesek.tsv`:
- a felmérés minden olyan adatállítását, amelyre a próza épít (Strong-előfordulás a 32 helyen, kísérő szó, Károli-szöveg, `kapcsolatok.tsv`-sor, LXX-megfelelő), a feladat újraméri;
- eszköz: a `lekerdez.py` megfelelő parancsa (`karoli`, `kollokacio`, `lxx-hid`, `tsk`, `scan`) `--naplo F<nn> --lepes adhoc` kapcsolóval (**nem** motívum-ID-vel: a részleges auditsor a DT103 szerint nem kerülhet az `adat/auditok.tsv`-be); ahol nincs parancs, fájlba írt szkript (`naplok/<KÓD>_*.py`, a CLAUDE.md shell- és TSV-szabályai szerint: `split('\t')`, kódlap-őr), saját proveniencia-sorral;
- a napló táblája: összefüggés · a felmérés állítása · a saját mérés · proveniencia · egyezik / eltér (és miben).

**3. Két célzott ellenőrzés:**
- **N-F55d:** a „22 közül 18” állítás újraszámolása az `lxx-hid` alapján a 22 ószövetségi helyre (a Zsolt 79:6 és 99:6 külön soron, a 99:6 akkor is, ha nem a motívum előfordulása). Kimenet: megerősítés vagy javítási javaslat, mindkét esetben proveniencia-sorral.
- **Róm 10:14 (12. összefüggés):** a TR/Byz alakeltérés mérése a `konkordancia/TAGNT_kivonat.tsv` `kritikai_kiadas` adatából (szkript-fájllal). Ha az eltérés a motívum szavát érinti, a próza csak a mért tényt mondja ki, szövegkritikai következtetés nélkül. Az eredmény az N-F126c-hez kerül (megerősítés vagy lezárási javaslat).

**4. ⛔ Szövegjavaslat a felhasználónak** → `naplok/<KÓD>_szovegjavaslat.md`, **mielőtt bármi a forrásba kerül**:
- bekezdésenként: célrés és beszúrási pont (a meglévő alszakasz neve), a javasolt szöveg, a mögötte álló proveniencia-sorok, a PaRDeS-szint;
- a **mérce-tábla** a 8 helyre: megalapozott értelmezést kapott / a próza kimondta a formai tartozást / nincs új anyag (Zsolt 116:13), soronként azzal a mondattal, amely ezt teljesíti;
- külön sor: az N-F55d eredménye, a Róm 10:14 mérése, és ha a Zsolt 116:4 bekezdése a 116:3-at érinti, a Seól-határ (A4) jelölése: „nyitott, a felhasználó dönti el”.
- **Megállás.** A felhasználó bekezdésenként jóváhagy, javít vagy elvet. Az elvetett bekezdés helyére nem kerül pótlás.

**5. Beírás a forrásba:** csak a jóváhagyott szöveg, a 2a. szakasz 5. pontja szerint. Commit (`F<nn>.1: …`).

**6. Újragenerálás** (`python eszkozok/general.py --cel lexikon`, ISTENTISZT-001):
- várt diff: csak a lexikonoldal `6. Értelmezés` és `7. Módszertan` szakasza (és a változott blokkok `ts=` értéke); más blokk változása ⛔;
- `python eszkozok/ellenoriz.py` (11. szakasz: a lap rése = tábla + forrás) és `python eszkozok/feladatok.py ellenoriz`: 0 hiba;
- commit (`F<nn>.2: …`).

**7. Független ellenőrzés** (`fuggetlen-ellenor`, `naplok/ELLENOR_<KÓD>.md`) a base..head diffen: minden új állítás mögött van-e saját proveniencia-sor; a mért tény és az értelmezés külön mondat-e; van-e új Sod, motívumközi állítás vagy idézés-állítás; a 8 hely mérce-táblája teljesül-e. ELTÉRÉS esetén `/elteres` (2 kör).

**8. Zárás:** a brief fejléce (`allapot`, `lezarva_osszegzes`), zárónapló (`naplok/<KÓD>_zaras.md`), az N-F55d és az N61 állapota a `NYITOTT_FELADATOK.md`-ben. A #123 0.1/b előfeltétele (N-F123b) ezzel teljesül; a #123 `fugg` mezőjébe e feladat száma a befogadáskor kerül (l. 5. szakasz).

## 4. Elfogadási feltételek

1. A 8 meg nem nevezett helyből 7 a mérce-tábla szerint megalapozott értelmezést kapott, vagy a próza kimondta a formai tartozását; a Zsolt 116:13-nál a próza kimondja, hogy nincs új anyag.
2. A 11. összefüggés a `modszertan` résben áll, új adat nélkül.
3. Minden új szám vagy adatállítás mellett a feladat saját proveniencia-sora áll; a felmérés proveniencia-sora sehol nem szerepel forrásként.
4. Nincs új Sod-állítás, motívumközi állítás, idézés-állítás és új adatsor (jelölt, kapcsolat, előfordulás, LXX-döntés).
5. A Seól-határ (A4) nincs eldöntve, és ha a szöveg érinti, jelölve van.
6. Az N-F55d megerősítve vagy javítva, proveniencia-sorral.
7. A lexikonoldal diffje csak a 6. és a 7. szakaszt érinti; az `ellenoriz.py` és a `feladatok.py ellenoriz` 0 hibát ad.
8. A független ellenőrzés zöld, a felhasználó jóváhagyta a szövegjavaslatot (4. ⛔) és a zárást.

## 5. Döntésnapló (helyőrzők; végleges számot a `szamkiosztas` Action ad)

- **Sorrend: a #123 első motívuma előtt** (felhasználói kérés, 2026-10-19; a #123 0.1/b, N-F123b). Az aranyminta a mérce (DT-F123a sablon-próba, #32 4. szabály (b)).
- **`nem_fugg: [110, 123]`.** A #123 `ir`-je az `adat/jeloltek.tsv`-t, a `kapcsolatok.tsv`-t, az `elofordulasok.tsv`-t és a `res_forras.tsv`-t is írja, ezeket ez a feladat olvassa, ezért a `feladatok.py` levezetett függést adna a #123-ra; a sorrend fordított, ezért a levezetés kézzel felülírva. A #123 viszont a `motivumok/ISTENTISZT-001.md` olvasása miatt levezetetten függ ettől a feladattól: a „#123 első motívuma előtt” sorrendet így a fájlok maguk biztosítják. A #110 (`fazis: 1`, `nem_indult`) szintén a `jeloltek.tsv`-t írja; a #110 új jelöltjei a 2. szakasz hatókörét nem érintik, és a felülírás nélkül a 2. tervezettel együtt függési kör keletkezik (#110 ↔ #123 ↔ e feladat ↔ HALO_RES). *(proveniencia: scope=a két tervezet ideiglenes `F126_*`/`F127_*` másolata a repó gyökerében, a futás után törölve | forras=`python eszkozok/feladatok.py ellenoriz` és `fuggesek` | ts=2026-10-19)*
- **Fázis-2-es ütközés, kapcsolat nélkül:** a #10 és a #70 (`fazis: 2`) is írja a `motivumok/ISTENTISZT-001.md`-t; a DT-F39d szerint fázis-2-es feladat nem ad levezetett kapcsolatot fázis-1-esnek. A #10 így a kiegészített lapot méri, ami a cél.
- **A 2. tervezettel (LEXIKON_HALO_RES) való sorrend:** az is írja a `motivumok/ISTENTISZT-001.md`-t (a rés-jelölőket) és az `adat/jeloltek.tsv`-t, ezért a két feladat kölcsönösen levezetett függést kapna (DT-F39g: kizárás, a kisebb sorszám előre). A javasolt sorrend: e feladat → HALO_RES → #123 (a HALO_RES DT268 tétele). **A befogadáskor:** e feladat `nem_fugg`-ja a HALO_RES számát is kapja, a HALO_RES `fugg`-ja e feladatét; így a próbafutás 0 hibát és kör nélküli sorrendet adott. *(proveniencia: scope=a két tervezet ideiglenes `F126_*`/`F127_*` másolata a repó gyökerében, a futás után törölve | forras=`python eszkozok/feladatok.py ellenoriz` és `fuggesek` | ts=2026-10-19)*
- **A4 (Seól-határ):** nem e feladat döntése; jelölve, a felhasználó dönti el.
- Új DT-tétel nem kell: a szövegjavaslat jóváhagyása a 4. ⛔-ben történik, a brief szerint.
