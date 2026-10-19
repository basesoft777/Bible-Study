---
feladat: 75
cim: A régi tanulmányok tartalmi javítása (tanulmányonként egy menet)
kod: TANULMANY_JAVITAS
tipus: feladat
fazis: folyamat
munka: ertelmezo
modell: opus
allapot: nem_indult
ad: a #37 T5-auditjának leletei tanulmányonként javítva (Strong-eltérés, ⚠️ képviselő, Sod-levezetés, elavult jegyzet); a DT61 öt ⚠️-vita-esete tételenként eldöntve
kovetkezo: /kovetkezo (a #74 lezárása után): T0 ⛔ (a DT61 öt esete); a DT254 eldöntve (1., tartalmi javítás megengedett, két korláttal)
olvas: [naplok/TANULMANY_ELLENORZES_utofeladat.md, naplok/TANULMANY_AUDIT_ugynok.md, naplok/TANULMANY_AUDIT.md, .claude/agents/fuggetlen-ellenor.md, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/PaRDeS_gyorsreferencia.md, sablonok/PaRDeS_tanitok_lista.md, motivumlog/PaRDeS_motivumok.md, adat/motivumok.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/kulcsszavak.tsv, adat/SEMA.md, konkordancia/, eszkozok/lekerdez.py, eszkozok/ellenorzes/tanulmany_audit.py, eszkozok/ellenorzes/futtat.py, genezis/naplok/, genezis/1Moz_9v1-17_bovitett.md, genezis/1Moz_14_bovitett.md, genezis/1Moz_4v1-24_bovitett.md, genezis/1Moz_1v1_bovitett.md, genezis/1Moz_6v9-22_bovitett.md, genezis/1Moz_15_bovitett.md, genezis/1Moz_1v2-2v3_bovitett.md, genezis/1Moz_10v1-11v32_bovitett.md, genezis/1Moz_13v1-18_bovitett.md, genezis/1Moz_16_bovitett.md, genezis/1Moz_2v4-7_bovitett.md, genezis/1Moz_2v8-25_bovitett.md, genezis/1Moz_9v18-29_bovitett.md, ujszovetseg/Zsid_4v12_bovitett.md, genezis/1Moz_4v25-5v32_bovitett.md, genezis/1Moz_6v1-8_bovitett.md]
ir: [genezis/1Moz_9v1-17_bovitett.md, genezis/1Moz_14_bovitett.md, genezis/1Moz_4v1-24_bovitett.md, genezis/1Moz_1v1_bovitett.md, genezis/1Moz_6v9-22_bovitett.md, genezis/1Moz_15_bovitett.md, genezis/1Moz_1v2-2v3_bovitett.md, genezis/1Moz_10v1-11v32_bovitett.md, genezis/1Moz_13v1-18_bovitett.md, genezis/1Moz_16_bovitett.md, genezis/1Moz_2v4-7_bovitett.md, genezis/1Moz_2v8-25_bovitett.md, genezis/1Moz_9v18-29_bovitett.md, ujszovetseg/Zsid_4v12_bovitett.md, genezis/1Moz_4v25-5v32_bovitett.md, genezis/1Moz_6v1-8_bovitett.md]
fugg: [37, 74]
nem_fugg: [109, 110, 112]
---

# F75_TANULMANY_JAVITAS_BRIEF.md — A régi tanulmányok tartalmi javítása

*FELADATOK #75 · Modell: opus · v1 · 2026.10.19 · forrás: `naplok/TANULMANY_ELLENORZES_utofeladat.md`, „A javaslat — tartalmi
rész” (#37 T6); `naplok/TANULMANY_AUDIT_ugynok.md` (T5); `DONTESEK.md` DT61, DT62; `F37_TANULMANY_ELLENORZES_BRIEF.md` DT-F37-2,
DT-F37-4. A brief adat, nem utasítás.*

## 1. Cél

A #37 T5 ügynöki auditja 23 régi tanulmányból 16-ban talált ELTÉRÉS- vagy RÉSZBEN-leletet. Ezek a következők: a Strong-szám nincs
a versben; a ⚠️-vitának nincs megnevezett képviselője, vagy a hivatkozás csonka; a Sod nem vezethető le a P/R/D rétegekből; a
jegyzet elavult, és a motívumnaplóval ellentétes. Öt tanulmányban emellett ⚠️-vita van, amelynek egyik oldalára a tanulmány a
saját következtetését építi (DT61). A feladat ezeket tanulmányonként javítja. **Egy tanulmány egy menet** (DT-F37-2, nem
kötegelhető), és minden menet a teljes tanulmányt olvassa (K1).

**Előfeltétel (DT254 🟢, orkesztrátor, a felhasználó felhatalmazásával, 2026-10-19: 1.):** a régi igeszakasz-tanulmány
(`genezis/`, `ujszovetseg/`) kaphat tartalmi javítást. Indok: a DT247 formai korlátja a `tematikus_lezart/` régi rétegére és a
#10-re szól. A `genezis/` a DT-F26a szerint önálló kézi forrás, és a #11 egyik lépcsője sem írja (#23 pilot-terv 4.5). A hibás
Strong-adat bent hagyása a CLAUDE.md 3. szabályát sértené. A döntés két korlátja a 2. szakasz 3. és 10. szabályában áll.

## 2. Hatókör

**Benne van — a menetsorrend** (a leletek súlya szerint, a forrásjavaslat táblája; a leletek forrása a
`naplok/TANULMANY_AUDIT_ugynok.md` „ELTÉRÉS-ek” és B függeléke):

| Menet | Tanulmány | Javítandó |
|---|---|---|
| 1 | `genezis/1Moz_9v1-17_bovitett.md` | ⚠️-vita (DT61 1.: *kesét* = hadi íj), Sod (feltételesség), ⚠️ képviselő RÉSZBEN |
| 2 | `genezis/1Moz_14_bovitett.md` | Strong: 14:22 H5375 → H7311 (הֲרִמֹתִי; a kulcsszó-tábla héber alakja is); Sod RÉSZBEN (feltételes, marad); DT61 5. (tájékoztató) |
| 3 | `genezis/1Moz_4v1-24_bovitett.md` | Strong: 4:2 H1892 → H1893 (személynév; a *hevel*-szójáték értelmezésként marad, a Strong-adat javul); ⚠️ Nód „mások”; angol *later* a Sod-ban |
| 4 | `genezis/1Moz_1v1_bovitett.md` | Strong: 1:1 אֵת = H0853; két csonka ⚠️-hivatkozás (a 2026-10-07-i 32. és 177. sor); ⚠️-vita (DT61 3.); Sod: az idő teremtése |
| 5 | `genezis/1Moz_6v9-22_bovitett.md` | Strong: 6:17 H5315 nincs a versben (*rúach chajjim*) |
| 6 | `genezis/1Moz_15_bovitett.md` | ⚠️-vita (DT61 2.); Sod: Mt 27:45 párhuzam |
| 7 | `genezis/1Moz_1v2-2v3_bovitett.md` | ⚠️-vita (DT61 4.); elavult ⭐-jegyzet (272. sor, TEREMT-002) |
| 8 | `genezis/1Moz_10v1-11v32_bovitett.md` | ⚠️ „hetven nép” képviselő nélkül; nyelvzavar-⚠️ RÉSZBEN; `Jób 38:41` Károli-számozása (`Jób 39:3`) |
| 9 | `genezis/1Moz_13v1-18_bovitett.md` | ⚠️ „mint a föld pora”: név nélküli oldalak |
| 10 | `genezis/1Moz_16_bovitett.md` | elavult „Motívumnaplózásra váró elemek” jegyzet (198–203. sor); Sod RÉSZBEN |
| 11–16 | `genezis/1Moz_2v4-7_bovitett.md`, `genezis/1Moz_2v8-25_bovitett.md`, `genezis/1Moz_9v18-29_bovitett.md`, `ujszovetseg/Zsid_4v12_bovitett.md`, `genezis/1Moz_4v25-5v32_bovitett.md`, `genezis/1Moz_6v1-8_bovitett.md` | csak RÉSZBEN-leletek (Sod-levezetés vagy ⚠️ „mások”/„néhány értelmező”) |

A sorszámok a 2026-10-07-i állapotra vonatkoznak; a #74 E8-cseréje sorszámot nem tol el, de minden menet a lelet szövegét
keresi, nem a sorszámot.

**Szabályok minden menethez:**

1. **K1:** a menet a teljes tanulmányt olvassa, és ha van, a kereszthivatkozás-naplóját is (`genezis/naplok/`). Író subagent nem
   futhat; olvasó (`fuggetlen-ellenor`, `lexikai-scan`) igen.
2. **Forrás nélküli ⚠️-oldalt név nélkül nem szabad „kitölteni”** (CLAUDE.md 3. szabály). Ha nincs megnevezhető képviselő, az
   oldal törlendő, vagy explicit „képviselő nem azonosítva” jelölést kap. Új nevet csak forrással lehet beírni: a
   `sablonok/PaRDeS_tanitok_lista.md`-ből vagy webes forrásból, hivatkozással. A memóriából írt név nem forrás.
3. **Strong-javítás (DT254, 1. korlát):** a tanulmány szövegében a kulcsszó-tábla cellája javul, és a javítás mellé, a
   tanulmányban, a lekérdezés saját proveniencia-sora kerül (`lekerdez.py`, TAHOT/`Karoli_Strong_kivonat`, a CLAUDE.md
   igehely-normalizálásával); ugyanez a menet naplójába is. Ha a javított érték egy adattábla sorában is áll
   (`adat/elofordulasok.tsv`, `adat/jeloltek.tsv`, `adat/kulcsszavak.tsv`), ott a tanulmányból nem íródik vissza: csak a
   `jeloltek.tsv`-n át, döntéssel javul (DT28, 2. szabály). Ilyenkor ⛔. A brief írásakor egyik érintett Strong sem áll adattábla-soron (`kulcsszavak.tsv`: 0 adatsor;
   `scope=adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/kulcsszavak.tsv | forras=manual (szkript, split('\t')) | ts=2026-10-19`).
4. **Sod-levezetés (RÉSZBEN):** a Sod-állítás vagy kap egy kifejezett levezetési hivatkozást a P/R/D réteg megfelelő pontjára,
   vagy feltételes alakba kerül („Ha …”, DT62 (b)). Ha egyik sem lehetséges, ki kell venni. Új Sod-tartalom nem kerül be.
5. **Elavult jegyzet** (7. és 10. menet): a jegyzet nem törlődik nyom nélkül. Helyére egy rövid állapotmondat kerül arról, hogy
   az elem ma hol áll az adatrétegben (`adat/motivumok.tsv` ID, statusz), a lekérdezés proveniencia-sorával. A motívumnaplóba
   (`motivumlog/PaRDeS_motivumok.md`) nem íródik semmi; azt a menet csak olvassa (DT28: forrásba adat nem íródik vissza, a
   napló pedig a T5 szerint már tartalmazza az elemeket).
6. **DT61-esetek** (1., 4., 6., 7. menet; a 2. menetben tájékoztató): a T0 döntése szerint. „Elfogadott projekt-olvasat”: a
   szöveg marad, és kifejezett jelölést kap („a projekt munkahipotézise”, a döntés azonosítójával). „Feltételessé teendő”: az
   építő mondatok feltételes alakba kerülnek. „A Sod-ból törlendő”: az érintett Sod-rész kikerül, a P/R/D-ben a vita bemutatva
   marad.
7. **D8:** a megérintett sorokon az E13 és az E8 kötelező. Minden menet végén a következőt kell futtatni:
   `python eszkozok/ellenorzes/futtat.py --valtozott <tanulmány> --diff-alap <menet alapja> --diff-fej HEAD`. HIBA-szintű találat
   nem maradhat. A kiejtés pótlása a tanulmány saját átírásából vagy a szótári adatból történik; ha egyik sem ad egyértelmű
   alakot, a menet megáll.
8. **A 7. pont (magyar szó ↔ Strong) kimarad** a #22-ig (DT-F37-4). A menet nem javít más, az auditban nem szereplő tartalmat
   sem. Ha ilyet talál, a naplóba kerül, javítás nélkül.
9. A tanulmány fejléce verziósort kap (`*v<n> — <dátum> (F75, <menet>. menet: …)*`), amely felsorolja a javított leleteket.
10. **Később migráló motívum (DT254, 2. korlát):** ha a javított hely egy olyan motívumhoz tartozik, amely később migrál (a #11
    2. lépcsője), a javítás nem visz át értelmező szöveget a motívumforrásba (`motivumok/`, `tematikus_lezart/`). Az a migráció
    dolga; a menet a kapcsolatot legfeljebb a naplójában jelzi.

**Nincs benne:** a 7 tiszta tanulmány (`1Moz_3v1-6`, `1Moz_3v7-24`, `1Moz_7v1-24`, `1Moz_8v1-22`, `1Moz_12v1-20`,
`1Thessz_5v23`, `Rom_8v10`). A régi E13/E12 találatok közül csak a megérintett sorokon lévők tartoznak ide (D8). Nincs benne
továbbá a T4 7. pontjának részleges bekapcsolása (DT-F37-4, külön befogadandó), a motívumnapló és az adattáblák írása (3. és 5.
szabály), a #74 gépi javítása, és a `tematikus_lezart/` meg a `motivumok/` bármely fájlja.

## 3. Lépések

**T0 ⛔ — a DT61 öt esete** (egyszer, a feladat elején, saját session):

1. Modell-ellenőrzés (CLAUDE.md); ágellenőrzés. A #74 lezárva és mergelve? (A DT254 🟢: 1.)
2. Az öt eset mindegyikéhez a végrehajtó elkészíti a következőket: a vitatott állítás helye szó szerint idézve; a
   képviselők; a következtetés, amely rá épül (Remez/Sod sorok). Az 1Moz_1v1 és az 1Moz_1v2-2v3 esetében megállapítja, van-e
   proveniencia-sora a saját lexikai érvnek. Ha van, a DT62 (a) szerint az érv nem forrás nélküli lezárás. Ezután a három
   választás mindegyikéhez megírja, mi változna a szövegben, és ad egy javaslatot. Kimenet: `naplok/TANULMANY_JAVITAS_T0.md`.
3. Öt tétel kerül a `DONTESEK.md`-be (`DT-F75b`–`DT-F75f`, súlyossági sorrendben: `1Moz_9v1-17`, `1Moz_15`, `1Moz_1v1`,
   `1Moz_1v2-2v3`, `1Moz_14`). Mindegyik opciói: elfogadott projekt-olvasat / feltételessé teendő / a Sod-ból törlendő. Commit
   (`F75.0.<n>`), push, draft PR, megállás. A fejléc: `allapot: dontesre_var`.

**Menetek (1–16), menetenként külön session, a 2. szakasz sorrendjében:**

1. Modell-ellenőrzés. Melyik menet következik (a fejléc `kovetkezo` mezője)? Az előző menet PR-ja mergelve?
2. A teljes tanulmány olvasása (K1), majd a menet leletei az auditból és — ha DT61-eset — a T0 döntése.
3. Lekérdezések (Strong, igehely, Károli-számozás), proveniencia-sorral a menet naplójába
   (`naplok/TANULMANY_JAVITAS_<menet>_<tanulmány>.md`).
4. ⛔ Ha egy javítás tartalmi döntést kíván, amelyet sem az audit, sem a T0, sem a 2. szakasz szabályai nem adnak meg (pl. a
   Strong-javítás megdönti a tanulmány egy érvét, vagy egy ⚠️-oldalhoz csak gyenge forrás van): `DT-F75<betű>` tétel, megállás.
5. Javítás, verziósor (9. szabály), commit (`F75.<menet>.<n>: …`).
6. D8-ellenőrzés (7. szabály); `tanulmany_audit.py` a tanulmányra: a lelet az ügynöki ellenőrzőlista szerint OK, és az E-számok
   nem nőnek.
7. Független ellenőrzés: `fuggetlen-ellenor` a menet base..head diffjén, a tanulmány-ellenőrzőlistával (DT62) →
   `naplok/ELLENOR_F75_<menet>.md`. ELTÉRÉS esetén `/elteres`.
8. A fejléc `allapot: fut`, `kovetkezo: "Folytatás: <menet+1>. menet (<tanulmány>)"`. Push, menetenként egy PR (ág:
   `claude/f75-<menet>`); merge csak a felhasználótól. Megállás: egy session = egy menet.

**Zárás** (a 16. menet után): zárójelentés (`naplok/TANULMANY_JAVITAS_zaras.md`: menetenként a javított leletek, a DT-F75
döntések, a kihagyott és naplózott tételek). `tanulmany_audit.py` teljes futás, jelentés módban, a 2026-10-07-i összesítővel
összevetve. A fejléc: `allapot: lezarva`, `lezarva_osszegzes`.

## 4. Elfogadási feltételek

- A DT61 öt esete tételenként eldöntve (DT-F75b–f), és a döntés a megfelelő tanulmányban alkalmazva.
- A 16 tanulmány mindegyikében az audit ELTÉRÉS- és RÉSZBEN-leletei (1., 3., 4., 5., 6. pont) javítva vagy indokoltan
  meghagyva (a menet naplójában, tételenként). Ennek ellenőrzése: `fuggetlen-ellenor` menetenként, TISZTA vagy elfogadott
  eltérés.
- Minden javított Strong-szám mellett proveniencia-sor áll a menet naplójában. Név nélkül kitöltött ⚠️-oldal nincs. Új Sod-tartalom
  nincs.
- A megérintett sorokon E8 = 0 és E13 = 0 (D8, `futtat.py` diff-módban zöld). Az adattáblák és a motívumnapló változatlanok
  (bájtra), kivéve a 3. szabály szerinti, döntéssel futó jelölt-utat.
- `python eszkozok/feladatok.py ellenoriz`: 0 hiba.

## 5. Döntésnapló

- Brief írásakor (2026-10-19): a `motivumlog/PaRDeS_motivumok.md` a csonk `ir` listájáról az `olvas`-ba került. Indok: a DT28
  szerint forrásba adat nem íródik vissza, és a T5 szerint az elavult jegyzetek elemei a naplóban már szerepelnek; a javítás a
  tanulmány oldalán történik (5. szabály). A `konkordancia/` olvasása lekérdezésen át történik (`lekerdez.py`), a nyers adat nem
  kerül a fő szál kontextusába.
- Brief írásakor: a #11 a kézi `fugg`-ban nem áll, mert a #11 (1. és 2. lépcső) a `genezis/`-t nem írja (#23 pilot-terv 4.5,
  `beerkezo/MIGRACIO_2_LEPCSO_BRIEF_TERVEZET.md` „Nincs benne”). A `feladatok.py fuggesek` a #11-et a Tanulmány sablonon át
  (`sablonok/2_`, a PR #420 v21-e) levezeti, és a #74-en át a #75 amúgy is a #11 után fut. A `nem_fugg: [109, 110, 112]` oka:
  a #75 az adattáblákat és a `futtat.py`-t csak olvassa, ellenőrzésre. A #109 és a #110 más igehelyek sorait írja, a #112 egy
  új CI-szabályt vesz fel.
- Brief írásakor: menetenként külön ág és PR. Így egy menet mergelt PR-jára a következő nem pushol, és a tanulmányok egyenként
  átnézhetők.
- **DT254** 🟢 (orkesztrátor, a felhasználó felhatalmazásával, 2026-10-19): **1.** A `genezis/`/`ujszovetseg/` régi
  igeszakasz-tanulmány kaphat tartalmi javítást. Két korlát: az adattáblán is álló érték csak a `jeloltek.tsv`-n át, döntéssel
  javul, és a tanulmányban a javítás mellé proveniencia-sor kerül (3. szabály); később migráló motívumnál értelmező szöveg nem
  kerül át a motívumforrásba (10. szabály). Átvezetve: fejléc `kovetkezo`, 1. szakasz, 2. szakasz 3. és 10. szabály, T0 1. lépés.
- (helyőrző a futáskor: DT-F75b–f — a DT61 öt esete, T0; DT-F75g… — a menetek 4. lépésének ⛔-jei)
