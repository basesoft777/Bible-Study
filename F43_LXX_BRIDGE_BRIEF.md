---
feladat: 43
cim: LXX-döntések ellenőrzése a lxx_bridge héber–görög párlistával
kod: LXX_BRIDGE
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ag: claude/f43-lxx-bridge
ad: a 86 LXX-döntés mindegyikéhez a lxx_bridge (MACULA-eredetű, LXX-en összesített héber→görög Strong-párok) egyezés/eltérés/nincs-adat ítélete, a bizonyosság-emelés jelöltjeivel; az lxx_dontesek.tsv nem változik
kovetkezo: "a végrehajtás fut (vegrehajto-sonnet)"
olvas: [adat/kulso/lxx_bridge.tsv, adat/lxx_dontesek.tsv, "konkordancia/LXX_OS/*.tsv", "konkordancia/LXX_kivonat_*.tsv", konkordancia/TAHOT_kivonat.tsv, konkordancia/Strong_szotar.tsv, konkordancia/LXX_OS/README.md]
ir: [eszkozok/lxx_bridge_egyezes.py, naplok/LXX_BRIDGE_egyezes.tsv, naplok/LXX_BRIDGE_naplo.md, adat/kulso/LICENC.md]
fugg: [8]
helyi_gep: nem
---

# Fnn_LXX_BRIDGE_BRIEF.md — LXX-döntések ellenőrzése a lxx_bridge párlistával

*FELADATOK #nn (a számot a `/befogad` adja; a fájlnév ezután `F<nn>_LXX_BRIDGE_BRIEF.md`) · Modell: sonnet · v1 · 2026.10.02*

## 1. Cél

Az `adat/lxx_dontesek.tsv` 86 sora (LD005–LD090; biztos 61 / valószínű 13 / nyitott 4 / nem_alkalmazhato 8, DT23) egy harmadik forrással kap ellenőrzést: a `bcv-commons/hebrew-lexical-references` dataset `lxx_bridge` alkonfigjával. Ez a tábla azt adja meg, hogy a LXX melyik görög Strong-számmal fordította az egyes héber Strong-számokat, előfordulás-számmal (3 301 sor, 1 862 héber és 1 571 görög Strong, ≥3 előfordulásra szűrve; a MACULA héber/görög Strong-címkézéséből, a Rahlfs-szöveg ellenében számolva; CC BY 4.0).

A feladat **nem módosítja** a döntéstáblát. Kimenete egy egyezés-tábla és egy döntési javaslat: mely `valoszinu`/`nyitott` sorokat erősíti meg a bridge, és hol mond ellent a `biztos` soroknak.

## 2. Hatókör

**Benne van**
- a `lxx_bridge.tsv` beolvasása, séma- és licenc-rögzítése;
- a 86 sor összevetése a bridge párjaival, a vers tényleges görög Strong-halmazával szűrve;
- egyezés-tábla + napló + döntési javaslat (DT-sor szövege, nem beírva).

**Nincs benne**
- az `adat/lxx_dontesek.tsv` bármely sorának módosítása (bizonyosság-emelés csak felhasználói döntés után, külön menetben);
- a `bdb_roots`, `hwn_synsets`, `tomim_parallelism` alkonfigok (nem tölthetők be ebben a feladatban);
- a lexikon-oldalak újragenerálása;
- bármely NuBerea-dataset (gated; külön feladat, ha lesz).

## 3. Lépések

**0. (Te, a futás előtt)** Letöltöd a `lxx_bridge` alkonfig TSV-jét (HF: `bcv-commons/hebrew-lexical-references`, Files → `lxx_bridge`), és commitolod `adat/kulso/lxx_bridge.tsv` néven, mellé `adat/kulso/LICENC.md` egy sorral: forrás-URL, alkonfig, letöltés dátuma, licenc (CC BY 4.0, bcv-commons; MACULA Hebrew/Greek CC BY 4.0; LXX-szöveg közkincs), a kártya állítása, hogy nem UBS/Louw-Nida/SDBH-eredetű.

**1. Séma és normalizálás.** A TSV fejlécének beolvasása (tabbal tagolt, `split('	')`) (várt oszlopok: `hebrew_strong`, `greek_strong`, `count`; az eltérést a napló rögzíti). A Strong-számok egész számmá normalizálása mindhárom oldalon: bridge (`H1254`/`G4160` vagy csupasz szám), `lxx_dontesek.tsv` (`H1254`, `G4160`), `LXX_OS` (`strong` = `4160`, G nélkül), régi `LXX_kivonat_*` (`G0746`). A kimenet egységesen `H####`/`G####` alakot ír. Ellenőrző számok a naplóba: sorok száma, egyedi héber és görög Strong-ok száma — a kártya 3 301 / 1 862 / 1 571 értékével összevetve.

**2. Lefedettség.** A 86 sor `lxx_igehely` mezője szerint: mely versekhez van `konkordancia/LXX_OS/*.tsv` sor (Strong-os, pozíciós), melyekhez csak régi `LXX_kivonat_*.tsv`, melyekhez egyik sem. A `LXX_OS/README.md`-ből a `strong_ok` és `karoli_ok` oszlop jelentése; üres érték = „nem ellenőrzött”, külön oszlopban jelölve, nem szűrünk rá.

**3. Egyezés-tábla** (`eszkozok/lxx_bridge_egyezes.py` → `naplok/LXX_BRIDGE_egyezes.tsv`, 86 sor). Oszlopok:

| oszlop | tartalom |
|---|---|
| `id`, `igehely`, `lxx_igehely`, `heber_strong`, `tipus`, `bizonyossag` | a döntéstáblából |
| `dontes_gorog_strong`, `dontes_gorog_lemma` | a döntéstábla értéke (üres `lxx_minusz`, `nincs_heber_kulcsszo`, `nyitott` sornál) |
| `bridge_jeloltek` | a héber Strong összes bridge-párja `G####:count` alakban, count szerint csökkenő |
| `vers_strongok_forras` | `LXX_OS` / `LXX_kivonat` / `nincs` |
| `bridge_a_versben` | a bridge-jelöltek metszete a vers görög Strong-halmazával, `G####:count` |
| `bridge_lemma` | a metszet elemeinek lemmája a `LXX_OS`-ből (ha onnan jön) vagy a `Strong_szotar.tsv`-ből |
| `kategoria` | lent |
| `megjegyzes` | szabad szöveg |

Kategóriák:
- `egyezik` — a döntés görög Strong-ja a bridge-párok között van **és** a versben áll;
- `egyezik_lexema` — a bridge-párok között van, de a vers Strong-halmaza nem elérhető (`vers_strongok_forras=nincs`);
- `elter` — a döntés görög Strong-ja nincs a bridge-párok között, de a bridge ad versben álló jelöltet;
- `nincs_adat` — a héber Strong nem szerepel a bridge-ben (≥3 szűrés), vagy nincs versben álló bridge-jelölt;
- `lxx_minusz_osszhang` / `lxx_minusz_ellentmond` — `lxx_minusz` sornál: a bridge ad-e versben álló jelöltet (ha igen, az ellentmond a minusz-döntésnek);
- `nem_alkalmazhato` — `nincs_heber_kulcsszo` sorok, változatlanul átvezetve;
- `nyitott_jelolt` — `nyitott` sornál: a `megjegyzes`-beli jelölt bridge-státusza (`egyezik`/`elter`/`nincs_adat` a megjegyzésben).

**4. Napló** (`naplok/LXX_BRIDGE_naplo.md`): a futás parancsai, az 1–2. lépés ellenőrző számai, összesítés kategóriánként és bizonyosságonként (biztos×kategória, valószínű×kategória, nyitott×kategória), az `elter` és `lxx_minusz_ellentmond` sorok egyenként, egy-egy mondattal. A „memória vs. lekérdezés” szabály: minden szám a napló parancsából származik.

**5. ⛔ Döntési javaslat** (a napló végén, a DONTESEK.md-be szánt szöveg, nem beírva):
- (a) Számít-e a bridge-egyezés második független forrásnak a SEMA 2.11 `biztos` definíciójához? Opciók: 1. igen — a módszer eltér (korpusz-szintű összesítés, nem vers-szintű illesztés), így a `valoszinu` + `egyezik` sorok `biztos`-ra emelhetők; 2. nem — a bridge ugyanabból a MACULA-címkézésből származik, mint a Macula szó-szintű illesztés, ezért csak tájékoztató; az emelés nem automatikus. **Javaslat: 2., azzal, hogy az `egyezik` sorok a DT-sorban név szerint felsorolva kapnak felhasználói emelési lehetőséget** (a DT23 (a) mintájára: „a felhasználó soronként biztosra állíthatja”).
- (b) Az `elter` és `lxx_minusz_ellentmond` sorok: újranyitás `nyitott`-ra, vagy marad a döntés, a bridge-eltérés a `megjegyzes`-be. Javaslat: soronként, a napló mondata alapján.
- (c) A 4 `nyitott` sor (LD008, LD009, LD058, LD064) bridge-jelöltje: elfogadás soronként vagy marad nyitott.
- (d) Forráspolitika-kiegészítés (D17 mellé): „Nem kereskedelmi (NC) vagy csak-hivatkozási licencű forrás nem kerül a repóba, származtatott adaton át sem; HF-dataset importja előtt a kártya attribúciós táblája ellenőrizendő. Kizárva: CrossWire `GreekHebrew` és `HebrewGreek` (Pierre Leblanc, Abbott-Smith + Hatch–Redpath alapján; „copyrighted, free non-commercial distribution”) és származékaik (pl. NuBerea/lxx-analysis, NuBerea/crosswire-greekhebrew).”

**6. Zárás** a CLAUDE.md menetzárási szabálya szerint: `fuggetlen-ellenor`, `naplok/ELLENOR_LXX_BRIDGE.md`, push, draft PR a main-be; a záró összefoglaló első sora a PR-link és a CI-állapot.

## 4. Elfogadási feltételek

- `naplok/LXX_BRIDGE_egyezes.tsv` pontosan 86 sor, az `id` halmaza azonos az `adat/lxx_dontesek.tsv` LD005–LD090 halmazával; minden sor kap kategóriát.
- Az 1. lépés ellenőrző számai a naplóban; eltérés a kártya számaitól (3 301 / 1 862 / 1 571) megmagyarázva.
- `git diff -- adat/lxx_dontesek.tsv` üres a PR-ben.
- `adat/kulso/LICENC.md` tartalmazza a lxx_bridge sort a 0. lépés szerint.
- A `fuggetlen-ellenor` jelentése commitolva; a napló minden száma a napló parancsából reprodukálható.
- A script determinisztikus (újrafuttatva azonos TSV), nem hív hálózatot.

## 5. Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | Külön feladat, nem a #6/#8 része | a #6 és a #8 lezárt (FELADATOK v1.3); a feladat önálló audit, új forrással |
| D2 | A döntéstábla nem változik ebben a menetben | a bizonyosság-emelés a SEMA 2.11 definíciójának értelmezését igényli (5. lépés (a)), ez felhasználói döntés |
| D3 | A bridge-jelölt csak versben álló görög Strong-gal számít egyezésnek; lexémaszintű egyezés külön kategória | a bridge korpusz-szintű, a döntés vers-szintű |
| D4 | `LXX_OS` elsődleges, régi `LXX_kivonat` tartalék | az `LXX_OS` szó-szintű, lemmával és pozícióval; a régi kivonat kivezetés alatt (#33) |
| D5 | A TSV a repóba kerül (`adat/kulso/`), nem csak helyi | a script hivatkozik rá; 48 kB; CC BY 4.0 attribúció a `LICENC.md`-ben |
| D6 | NuBerea-datasetek, `bdb_roots` nincs a hatókörben | gated, ill. más feladat tárgya; a `lxx-analysis` NC-származék miatt kizárva (5. lépés (d)) |
| D7 | ASV: nem importáljuk (felhasználó, 2026.10.02) — N29 lezárandó ezzel a döntéssel | a szerepmátrix 9. szerepét a KJV tölti be, az ASV-nek nincs szerepe; a luvlylavnder ASV-Strongs (CC0) marad megnevezett pótlásként, ha igény lesz |

<!-- KOZVETLEN_FUTTATAS -->
## 0. Nyitó prompt

> Olvasd be a csatolt briefet (`Fnn_LXX_BRIDGE_BRIEF.md`), és hajtsd végre a 3. szakasz 1–6. lépését sorban. A 0. lépés már megtörtént (az `adat/kulso/lxx_bridge.tsv` és a `LICENC.md` a repóban van; ha hiányzik, állj meg és jelezd). Az `adat/lxx_dontesek.tsv`-t nem módosíthatod. Minden számot a naplóban rögzített parancsból vezess le. Az 5. lépésnél (⛔) állj meg: a döntési javaslatot a napló végére írd, a DONTESEK.md-be ne. Zárás a 6. lépés szerint; a záró összefoglaló első sora a PR-link és a CI-állapot.
<!-- /KOZVETLEN_FUTTATAS -->
