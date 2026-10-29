ELTÉRÉS: 1 tétel

# Független ellenőrzés: F38_BDB_FORDITAS_BRIEF.md, 11. adag, 2/2. javítókör

- **Brief:** `F38_BDB_FORDITAS_BRIEF.md`
- **Tartomány:** `419d2ea4..8b3857d0` (1 commit: F38.431)
- **Előzmény:** `naplok/ELLENOR_F38_adag11_2.md` (ELTÉRÉS: 2 tétel)

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell (ellenőr) | OK | — | A tényleges modell `claude-opus-5-5`, a kért modell (subagent-fájl `model` mezője) `opus`. Egyezik. |
| 0 modell (menet) | OK | — | `git log --format='%h %an%n%B' 419d2ea4..8b3857d0` → társszerző `Claude Sonnet 5.5`. A brief `modell: sonnet`. Adattáblában nincs új `modell` mező, mert adat nem változott. |
| Numstat ↔ orkesztrátor | OK | — | `git diff --numstat 419d2ea4..8b3857d0` → `F38_BDB_FORDITAS_BRIEF.md` 1/1, `naplok/BDB_FORDITAS_adag11_bontas.md` 8/2. Egyezik. |
| Adat nem változott | OK | — | `git diff --numstat 419d2ea4..8b3857d0 -- adat konkordancia eszkozok forditas naplok/EMELES_munka.tsv DONTESEK.md NYITOTT_FELADATOK.md` → 0 sor. |
| Előző 2. tétel: „helyben csere” | OK (megszűnt) | `naplok/BDB_FORDITAS_adag11_bontas.md:86`, `:111` | `git diff --numstat e0cc8e48..2e3a5335` → `EMELES_munka.tsv` 114/114. `git diff -U0 e0cc8e48..2e3a5335 -- naplok/EMELES_munka.tsv` → 10 törlő hunk és egy hozzáadó hunk (`@@ -17962,0 +17849,114`), vagyis a fájl végére került. `git diff -U0 --color-moved=plain …` → 208 mozgatottként színezett sor, azaz 104 azonos sor a régi és az új oldalon. Ez egyezik az új leírással: 114 sor a végére, 104 azonos, 10 javított, a sorrend megváltozott. |
| Előző 1. tétel / passim | OK | bontás:101 | Grep `\bpassim\b` az `adat/forditasok.tsv`-n → 3396, 10252, 11047, 16571, 17080. Közülük ≤14 668 csak a 3396, 10252 és 11047. A Strongok: a 3396 sor H1980 sz28 (grep `^BDB\tH1980\tH1980\tsz28\t` → 3396), a 10252 sor H6206 sz2, a 11047 sor H5015 sz8. Egyezik. |
| Előző 1. tétel / „szétszórtan” | OK | bontás:101 | Grep count `szétszórtan` → 0 (a teljes fájlban). |
| Előző 1. tétel / „ k.” 360 | OK | bontás:101 | Grep `^BDB\t…\t.* k\.` count → 428 BDB-sor. A 300. eltolástól listázva az utolsó ≤14 668 találat a 14633 (355. BDB-sor), a következő a 14861. A nem-BDB sorok (`^[^B]…  k\.`) mind ≤14 668-ban vannak, 5 db (8064–8069). Összesen 355 + 5 = 360. Megjegyzés: a 360-ban 5 nem-BDB sor is benne van. A scope (`fájlsor 1–14 668`) ezt fedi, de a szöveg „korábbi adagok”-at mond. |
| Előző 1. tétel / „kk.” 503 | OK | bontás:101 | Grep `-o kk\.` 500. eltolástól: az 503. előfordulás a 14633-as soron, az 504. a 14854-esen. 503 egyezik. |
| Előző 1. tétel / „nőnemű” 1512 | OK | bontás:101 | Grep `-o ^.*nőnemű` 1510. eltolástól: az 1512. találat a 14667-es soron, az 1513. a 14670-esen. 1512 egyezik. |
| Előző 1. tétel / „k.” 186 törölve | OK | bontás:101, 103 | A diff szerint a 186 kikerült, a proveniencia-sor jelzi, hogy nem volt reprodukálható. |
| **Előző 1. tétel / fordítatlan feminine „f.” „2 korábbi sorban”** | **ELTÉRÉS** | bontás:101, 103, 111 | Grep `.{0,40}\bf\..{0,30}` (174 sor), kézi átnézéssel, majd célzott grep `^…\t.*(f\. הִתְכַּבְּדִי\|>f\. absolutus\|2Sám 22:6; f\. \|Qal participium f\. \|, f\. alany)`. A fordítatlan, „feminine” jelentésű „f.” legalább **5** korábbi sorban áll, nem 2-ben. A napló által felsorolt kettő: **14049** H6958 sz3 („Qal participium f. קָאָה”) és **14667** H1753 („f. alany”). Fel nem sorolt: **460** H3513 teljes („Hithpa`el imperativus הִתְכַּבֵּד Náh 3:15; f. הִתְכַּבְּדִי 3:15”, nőnemű imperativus), **1782** H7356 sz2 („>f. absolutus Kö^ii. 1. 159”, nőnemű status absolutus), **6801** H4170 sz2 („מֹקְשֵׁי 2Sám 22:6; f. מֹקְשׁוֺת Zsolt 141:9”, nőnemű többes szám). A 2-es szám az előző ellenőri jelentésből (`ELLENOR_F38_adag11_2.md:45`) jött, és az is hiányos volt. A napló viszont „kézi átnézéssel” mértként közli, és a nyitott lista ezért hiányos. A többi „f.” betűjelű szakaszmarker (pl. 56, 87, 1574, 17836). Nem minősítettem a 3922-es sor „f.o.”-ját és az 5042/532-es sor „f.”-jét. Ezek nem a feminine jelentést hordozzák, vagy kétesek. |
| Proveniencia-sor formája | OK (megjegyzéssel) | bontás:103 | Mindhárom mező megvan (`scope=… \| forras=… \| ts=2026-10-28`). A `forras` a repón kívüli `<scratchpad>/meres2.py`, `meres3.py`, ezért nem verziózott és nem reprodukálható. A számokat (360/503/1512/3/0) saját greppel reprodukáltam. Az „f.” elem „kézi átnézéssel” jelölése nem lekérdezés, és téves (lásd fent). |
| Brief `kovetkezo` | OK | `F38_BDB_FORDITAS_BRIEF.md:12` | A diff szerint „Te: [elteres_kor 2/2] /elteres 38 — újraellenőrzés függ: naplok/ELLENOR_F38_adag11_3.md”. Az `allapot: megallt`, más fejlécmező nem változott. |
| Commitüzenet | OK (a tartalmi hiba azonos) | — | A `git log` szerint a cím tétel-azonosítóval kezdődik és ékezetes. Az üzenet ugyanazt a hiányos „f.” 2 sor állítást ismétli. |
| G/D pontok | NEM ÉRINTETT | — | A tartomány csak naplószöveget és briefsort módosít. Adat, prompt, terminológia és eszköz nem változott (numstat). D6, megállás: `allapot: megallt` betartva. |
| A1 memória vs. lekérdezés | ELTÉRÉS (az „f.” sor) | bontás:101 | A mért számok helytállóak. A „kézi átnézés” eredménye mért adatként szerepel, pedig hiányos (lásd az ELTÉRÉS-sort). Nem külön tétel, hanem ugyanaz. |
| A2 nyitott tételek | ELTÉRÉS (ugyanaz a tétel) | bontás:101, 111 | A 14049 és a 14667 valóban nyitott: a fordítatlan „f.” a fenti greppel ma is megvan. A nyitott lista viszont 3 sorral hiányos (460, 1782, 6801). A nyitott tétel csak a naplóban áll, a `NYITOTT_FELADATOK.md`-be nem került helyőrző. A megbízás ezt nem írta elő. |
| A3, A4, A5 | NEM ÉRINTETT | — | Nincs tanulmány, párhuzam vagy nevesített tanító. Az F37 T4 nem él, mert nincs `*_bovitett.md` vagy `*_tanulmany.md` a diffben. |
| A6 (E12–E15) | OK | — | A saját futásban E12–E15: 0. |
| CI ↔ saját futás | NEM ELLENŐRIZHETŐ (nincs csatolt CI-jelentés) | — | `python eszkozok/ellenorzes/futtat.py --valtozott F38_BDB_FORDITAS_BRIEF.md naplok/BDB_FORDITAS_adag11_bontas.md --diff-alap 419d2ea4 --diff-fej 8b3857d0 --pr-cim "F38.431: BDB_FORDITAS 11. adag javítókör 2/2"`. Eredmény: E2–E16, E19, E20, E26, E28 (nem futott, nincs érintett fájl), E29, E30, E31, E32 mind 0. Az E25 JELENTÉS 4 (`CLAUDE.md:33`, `MUNKAMENET.md`) és az E27 JELENTÉS 40 (`FELADATOK.md`) nem ennek a diffnek a fájljai. HIBA nincs. |
| Lista 1: kiszűrt vagy törölt sorok | OK | — | numstat: a briefben 1 törlés, a `kovetkezo` cseréje. A bontási naplóban 2 törlés: a 86. sor (helyben csere leírása) és a 101. sor (rövidítés-elv), mindkettő cserélve. Adatsor-törlés 0. |
| Lista 2: kulcstartomány-lefedettség | OK | — | Kulcs nem változott, mert adatfájl nincs a diffben. |
| Lista 3: a nulla-diff hatóköre | OK | — | A „nulla” az `adat/`, `konkordancia/`, `eszkozok/`, `forditas/` és `naplok/EMELES_munka.tsv` tartalmára vonatkozik ebben a tartományban. Nem vonatkozik a bontási napló szövegére (8/2), és nem vonatkozik a korábbi, 1. javítókörbeli adatváltozásra (`e0cc8e48..2e3a5335`), amelyet az előző jelentés nézett. |
| Lista 4: adattábla-Δ (E17, DT3) | OK | bontás:11–13, 34 | A tartományban minden `adat/*.tsv` és `konkordancia/*.tsv` Δ 0 (numstat üres). A main-hez képest (`git diff --numstat main...8b3857d0 -- adat konkordancia`) csak az `adat/forditasok.tsv` +4066 (≥10). Ehhez van bontási napló: a `naplok/BDB_FORDITAS_adag11_bontas.md` 11–13. és 34. sora hivatkozik a 4066-ra. A bontás kategóriáit ebben a körben nem mértem újra. |
| Lista 5: a brief ⛔ pontjai | OK | brief:80, 95, 97 | M1, Mz és Mj ebben a körben nem érintett: prompt, terminológia és adat nem változott. A menet megállt (`allapot: megallt`), push nincs (`origin/ccr-f38-adag11-1` nem létezik). |

**Az ELTÉRÉS-ek súlyossági sorrendben:**

1. **A fordítatlan feminine „f.” hiányos számbavétele (`naplok/BDB_FORDITAS_adag11_bontas.md:101`, `:103`, `:111`).** A napló „2 korábbi sort” közöl „kézi átnézéssel”, mért tényként. Valójában legalább 5 ilyen sor van ≤14 668-ban:
   - a napló által felsorolt kettő: 14049 H6958 sz3 és 14667 H1753;
   - a fel nem soroltak: 460 H3513 teljes, 1782 H7356 sz2 és 6801 H4170 sz2.

   A hiba forrása az előző ellenőri jelentés (`ELLENOR_F38_adag11_2.md:45`), amelyet a megbízás továbbadott. Adatot nem érint. A nyitott, felhasználói döntésre váró lista azonban 3 sorral rövidebb a valósnál. Ugyanez a hiányos állítás áll az F38.431 commitüzenetében is.

A korábbi 2 tételből a 2. (helyben csere) megszűnt. Az 1. tételből a passim, „szétszórtan”, „k.”, „kk.” és „nőnemű” állítás rendben van, az „f.” rész hiányos maradt.
