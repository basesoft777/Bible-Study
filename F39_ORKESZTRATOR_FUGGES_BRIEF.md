---
feladat: 39
cim: Az orkesztrátor függés-levezetésének javítása (körök feloldása)
kod: ORKESZTRATOR_FUGGES
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: dontesre_var
ad: a közös írási útvonalból kizárás lesz, nem sorrend; nincs több levezetett kör; a halasztott, brief nélküli és 2. fázisú feladat nem tart vissza 1. fázisú feladatot; a /kovetkezo újra ad jelöltet (várhatóan #35, #38, #23)
kovetkezo: "M3 folyamatban (kovetkezo.md, DONTESEK, próbafuttatás kész), majd fuggetlen-ellenor és draft PR"
olvas: [eszkozok/feladatok.py, .claude/commands/kovetkezo.md, .claude/commands/befogad.md, BRIEF_SABLON.md, FELADATOK.md, DONTESEK.md]
ir: [eszkozok/feladatok.py, eszkozok/tesztek/test_feladatok_fugges.py, eszkozok/teszt_feladatok.py, .claude/commands/kovetkezo.md, DONTESEK.md, naplok/ELLENOR_ORKFUGG.md]
fugg: []
ag: claude/upbeat-wright-81rpah
nem_fugg: [26, 30, 32]
---

# Az orkesztrátor függés-levezetésének javítása

> **Megjegyzés (M0, 2026.10.01):** a premissza pontosítása: a `*` jelű levezetett függés a kódban már írás–olvasás (A `olvas` ∩ B `ir`), nem írás–írás; az írás–írás ütközés külön `UTKOZES`/`SORREND` sor volt. A körök oka a tág `olvas`-bejegyzés (`CLAUDE.md`, könyvtárak) és a `naplok/` helyettesítő. A felhasználó DT-F39g döntése (2026.10.01): a tág kontextus-olvasás nem ad sorrendet, a kölcsönös írás–olvasás `kizar` figyelmeztetéssel; `naplok/F39_M0_felmeres.md`.

**Verzió:** v1 · 2026.10.01 · készült a chatben
**Fájlnév a befogadás után:** `F39_ORKESZTRATOR_FUGGES_BRIEF.md` (az `39`-t a `/befogad` adja)

## 1. Miért kell

A `/kovetkezo` 2026.10.01-i futása nem adott végrehajtható feladatot. Ennek nem a feladatok az okai, hanem a levezetés szabálya:

1. **A közös írási útvonalból sorrendi függés lesz.** Ha két feladat ugyanazt az útvonalat írja, az orkesztrátor úgy kezeli, hogy az egyiknek a másikra kell várnia. Ebből körök keletkeznek: #35↔#37 (`naplok/*`, `genezis/*`), illetve #30→#37→#30. Valójában a közös írás csak annyit jelent, hogy a két feladat **nem futhat egyszerre**, de bármelyik mehet előbb.
2. **A `naplok/*` szinte mindent mindennel összeköt.** Minden menet ide írja az ellenőr-jelentését (`naplok/ELLENOR_<menet>.md`), ezért ez a minta minden `ir`-listában szerepel.
3. **Halasztott és 2. fázisú feladat blokkol 1. fázisút.** A #38 (BDB-fordítás) a halasztott, brief nélküli #7-re és a 2. fázisú #9-re vár. Ez ellentmond a D1-nek: a render nem tarthatja vissza az adatréteget.

## 2. Hatókör

**Benne van:** a levezetés szabálya, az `ellenoriz` figyelmeztetései, tesztek, a `/kovetkezo` leírásának frissítése.

**Nincs benne (⛔ tartalmi döntés, nem az orkesztrátoré):**
- egyetlen brief explicit `fugg`-mezőjének vagy `ir`-listájának módosítása;
- bármely feladat elindítása. A `/kovetkezo` a menet végén csak próbafuttatást végez (2026.09.29-i döntés: futtatás csak kifejezett jóváhagyással).

## 3. Lépések

### M0 — felmérés (csak olvas)

1. Keresd meg a `feladatok.py`-ban a levezetett (`*`) függést számoló részt. Rögzítsd a naplóba a pontos függvényneveket.
2. Készíts táblát a jelenlegi levezetett függésekről: feladat, függ ettől, melyik útvonal okozza.
3. Jelöld meg, melyik pár származik csak a `naplok/*`-ból, melyik halasztott vagy brief nélküli feladatból, és melyik 2. fázisúból.
4. Sorold fel a körök mindegyikét.

Ha az M0 olyan levezetett függést talál, amely **valódi tartalmi sorrendet** fejez ki (az egyik feladat a másik kimenetét olvassa, és ez az `olvas`-listából látszik), akkor ⛔ állj meg, és sorold fel ezeket. Különben menj tovább.

### M1 — a szabály javítása

**1. szabály: írás–írás ütközés = kizárás, nem sorrend.**
- A levezetett kapcsolat új neve `kizar` (kölcsönös kizárás), a kimenetben külön jelöléssel (például `×`), nem `*`-gal.
- Egy feladat akkor jelölt, ha minden explicit függése kész, és nincs `kizar`-párja **futó** (⏳) állapotban.
- Két `kizar`-pár nem kerülhet egy csomagba és nem futhat párhuzamosan. Ha mindkettő jelölt, a kisebb sorszámú kerül előre, a másik a következő körben jön.

**2. szabály: írás–olvasás = valódi sorrend.**
- Ha A `olvas`-listájában szerepel olyan útvonal, amelyet B ír, és B nincs kész, az sorrendi függés marad (`*`), mert A B kimenetét használja.
- Ha ez kört alkot, a kör hiba az `ellenoriz`-ben, és a döntés a felhasználóé.

**3. szabály: kivételek az ütközésvizsgálatból.**
- Egy konstans listában (például `UTKOZES_KIVETEL`) szerepeljenek azok a minták, amelyek menetenként egyedi fájlt írnak. Legalább: `naplok/ELLENOR_*`, és a menetenként egyedi naplók, amelyeket az M0 talál.
- Az `ir`-listában álló `naplok/*` helyettesítő minta figyelmeztetést kapjon az `ellenoriz`-ben („adj meg konkrét fájlt”). A BRIEF_SABLON szerint az `ir`-ben konkrét fájlok vannak.

**4. szabály: ki nem ad levezetett kapcsolatot.**
- A halasztott, a brief nélküli és a 2. fázisú feladat nem ad levezetett kapcsolatot (sem `*`, sem `kizar`) 1. fázisú feladatnak.
- Ha egy 1. fázisú feladatnak **explicit** függése van 2. fázisúra, az `ellenoriz` figyelmeztessen a D1-re hivatkozva. Ne javítsd automatikusan.

### M2 — tesztek és próbafuttatás

1. Tesztek a `eszkozok/tesztek/test_feladatok_fugges.py`-ban, a mostani állapotot visszajátszó fixture-rel:
   - a #35↔#37 és a #30↔#37 kör nem jön létre;
   - a #38 nem vár a #7-re és a #9-re;
   - két `naplok/ELLENOR_*`-t író feladat nem ütközik;
   - egy valódi írás–olvasás függés megmarad;
   - egy explicit kör hibát ad.
2. `feladatok.py ellenoriz`: 0 hiba (figyelmeztetés lehet, ezeket listázd).
3. `/kovetkezo` próbafuttatás indítás nélkül. A kimenet bekerül a naplóba. Várhatóan jelölt a #35, a #38 és a #23, de ha a valós állapot mást ad, az a helyes eredmény; írd le, miért.

### M3 — zárás

1. A `.claude/commands/kovetkezo.md` frissítése: a `kizar` jelentése és a kivétellista.
2. Bejegyzés a `DONTESEK.md`-be (az ágon helyőrző számmal, lásd a döntésnaplót).
3. A `FELADATOK.md` saját sorának frissítése.
4. Menetzárás a szokott módon: `fuggetlen-ellenor` → `naplok/ELLENOR_ORKFUGG.md`, push, draft PR a main-be, a záró összefoglaló első sora a PR linkje és a CI állapota.

## 4. Elfogadási feltételek

| # | Feltétel |
|---|---|
| K1 | Nincs levezetett kör a mostani feladatlistán |
| K2 | Az írás–írás ütközés `kizar`, és csak futó feladat ellen blokkol |
| K3 | Az írás–olvasás függés megmarad sorrendinek |
| K4 | A `naplok/ELLENOR_*` nem okoz ütközést |
| K5 | Halasztott, brief nélküli vagy 2. fázisú feladat nem blokkol 1. fázisút |
| K6 | Explicit `fugg`-mező és brief-tartalom nem változott (diff-ellenőrzés) |
| K7 | Tesztek zöldek, `ellenoriz` 0 hiba, a CI zöld |
| K8 | Egyetlen feladat sem indult el |

## 5. Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| DT-F39a | A közös írási útvonal kölcsönös kizárás, nem sorrend | a közös írás csak az egyidejű futást tiltja; a sorrendi értelmezés köröket gyárt | a körök kézi feloldása függés-felülbírálással |
| DT-F39b | Sorrendi függést csak az írás–olvasás kapcsolat vezet le | csak ez fejez ki valódi adatfüggést | minden közös útvonal sorrend |
| DT-F39c | A menetenként egyedi naplók kimaradnak az ütközésvizsgálatból | a `naplok/*` minden feladatot összeköt | minden brief `ir`-listájának kézi szűkítése |
| DT-F39d | Halasztott, brief nélküli és 2. fázisú feladat nem blokkol 1. fázisút | a D1 szerint a render nem tarthatja vissza az adatréteget | a fázishatár figyelmen kívül hagyása |
| DT-F39e | Az orkesztrátor a függéseket nem írja át, csak a levezetés szabályát | a függés tartalmi döntés, a felhasználóé | automatikus függés-javítás |

## 6. Nyitó prompt

<!-- KOZVETLEN_FUTTATAS -->
Olvasd el ezt a briefet (`F39_ORKESZTRATOR_FUGGES_BRIEF.md`), és hajtsd végre az M0–M3 lépéseket egy menetben, Sonnettel.

Szabályok:
- Az M0 csak olvas. Akkor állj meg, ha valódi írás–olvasás sorrendet találsz, amelyet a javítás megszüntetne.
- Egyetlen brief explicit `fugg`-mezőjét, `ir`-listáját vagy tartalmát sem módosíthatod.
- Egyetlen feladatot sem indíthatsz el. A `/kovetkezo` csak próbafuttatás.
- A `FELADATOK.md`-ben csak a saját sorodat frissítheted.
- A döntések az ágon helyőrző számot kapnak (`DT-F39a`–`e`).
- Zárás: `fuggetlen-ellenor` → `naplok/ELLENOR_ORKFUGG.md`, push, draft PR a main-be. A záró összefoglaló legfeljebb 20 sor, az első sora a PR linkje és a CI állapota, benne a `/kovetkezo` próbafuttatásának jelöltjei.
<!-- KOZVETLEN_FUTTATAS -->
