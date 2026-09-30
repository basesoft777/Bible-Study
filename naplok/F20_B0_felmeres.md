# F20 B0 — felmérés (csak olvasás)

*2026.09.30 · ág: `claude/befogadas` (rebase-elve az `origin/main`-re, `29ada3c`) · forrás: `F20_BEFOGADAS_BRIEF.md` v1.2 7. pont B0*

## 1. Fő eltérések a brief feltevéseihez képest (a B2-nél döntést kérnek)

1. **A repóbeli `FELADATOK.md` v1.1, nem v1.3.** A brief a „v1.3 táblára” hivatkozik, de a `main`-en ilyen nincs. A fázistáblákban csak a #7, #8 (1. fázis) és a #9–#13 (2. fázis) sor áll; a #6 már a „Kész” listában van. **#16–#19 nem létezik a repóban** (sem sor, sem brief, sem nyitott PR vagy ág). A B2 munkalap állapot-oszlopa ezért a v1.1 táblából és a „Kész” listából készül. A brief B8 PR-szövege és K6 a #16–#19 / v1.3 feltevésre épül; a K6 így a v1.1 függéseire értelmezendő.
2. **Az E17 név foglalt.** A `DONTESEK.md` DT3 és az `F15_ORKESZTRATOR_BRIEF.md` 3.4/4.6 az E17-et az „adattábla sorszám-változása” szabálynak tartja fenn (küszöb nyitott, 🟡); a `szabalyok.py` ma E2–E16-ot ismeri, E17 nincs implementálva. A brief B6 „E17 szabálya” (fejléc-érvényesség + generált blokk) ütközik ezzel. **Javaslat: a feladatkövető szabály neve E18**, az E17 marad a DT3-é. (D6: meglévő szabályt nem írunk át.)
3. **E16 a PR-címet érinti.** Az `ONMODOSITAS_MINTAK` között szerepel a `.github/`, így a B6 (új workflow, CI-módosítás) miatt a PR címe `[ELLENŐRZŐ]` előtagot kell viseljen, különben E16 pirosat ad.
4. **Számozási névütközés: `F4_BRIEF.md`, `F5_BRIEF.md`, `F6_BRIEF.md`, `F7_BRIEF.md`, `F8_BRIEF.md`** az atalakítási terv F4–F8 *fázisai*, nem FELADATOK-számok (a #5 a SZOTAR, #6 az FJ2, #7 a Thayer, #8 az LXX-döntés). Kétjegyű `F<nn>` mintára (`F05_`) nem illeszkednek, de félreérthetők. Javasolt: feladat nélküli briefként nem kapnak számot; a fájlnév-ellenőrzés csak a `^F\d\d_` alakú neveket vizsgálja.
5. **A „feladat nélküli” briefek fejlécéről a brief nem rendelkezik teljesen:** a 3. pont szerint `feladat` és `tipus` kötelező, a B0/B2 szerint viszont szám nélkül is kapnak fejlécet. Javaslat a B2-höz (D31-jelölt): feladat nélküli brief fejléce `tipus: archiv`, `feladat` nélkül, kötelező csak `cim` és `modell`, `allapot: lezarva`; az `ellenoriz` ezt külön kezeli, és a generátor nem teszi táblába.
6. **A „Kész” listában szám nélküli tételek is vannak** (FJ 1. menet, TEREMT-002 1–2. lépés, Szótári brief v1.1). Fejléc nélkül a generátor nem tudja kitenni őket. Javaslat: ezek egy kézi „Korábbi, szám nélküli lezárt tételek” szakaszba kerülnek, a generált „Kész” lista csak számozottakat ad (eltérés a K2-höz, jóváhagyandó).

## 2. Brief ↔ FELADATOK-sor megfeleltetés (v1.1 + „Kész” lista)

| Brief (mai név) | Feladat | Megjegyzés |
|---|---|---|
| `KAROLI_KULCS_BRIEF.md`, `_KK7_`, `_KK75_` | #1 (Károli-kulcs, kész, `4b9ae49`) | három brief egy feladathoz |
| `CI_ELLENORZES_BRIEF.md` | #2 (CI, kész, `68eb348`) | |
| `FORDITAS_PILOT_BRIEF.md` | #3 (fordítási próba, kész, `9eb43fe`) | |
| `KARBANTARTAS_BRIEF.md` | #4 (kész, `b8a418a`) | |
| `SZOTAR_BRIEF.md` | #5 (kész, S1) **és** #9 (2. menet) | egy brief, két feladat: a #9 csonk `forras: F05_SZOTAR_BRIEF.md#2. menet` |
| `F06_FORRASFELMERES_BRIEF.md` | #6 (kész) | már `F06_` nevű |
| — (brief a repóban nincs) | #7 Thayer éles | `FORDITAS_ELES_THAYER_BRIEF.md` v2→v3 „csak chatben”; csonk `brief_kell` (a brief csak a #10, #11, #13 esetét sorolja, a #7 és #8 is ide kerül — lásd B2) |
| — (nincs brief) | #8 LXX-döntések | „kutatói adatmunka”, brief nincs → csonk `brief_kell` |
| — (nincs brief) | #10, #11, #13 | csonk `brief_kell` (a brief #10, #11, #13-at jelöli) |
| `TEREMT002_KUTATAS_BRIEF.md` | #12 (a 3. lépés) | T1–T2 lefutott (szám nélkül, `15c338e`) |
| — (nincs repóbeli brief) | #14 FP2 (kész, `971d0f2`) | csak naplók (`naplok/FP2_*`) és a FELADATOK-sor; brief a chatben volt → csonk `lezarva` `forras: naplok/FP2_jelentes.md` |
| `F15_ORKESZTRATOR_BRIEF.md` | #15 (kész, PR #70) | már `F15_` nevű |
| `F20_BEFOGADAS_BRIEF.md` | #20 (ez a menet) | már új fejlécű |
| `FORRASJELOLTEK_BRIEF.md` | (FJ 1. menet, szám nélkül; a #6 előzménye) | feladat nélküli |
| `CREMER_OCR_BRIEF.md`, `ISTENTISZT_V3_BRIEF.md`, `LEX_BRIEF.md`, `LEXV2_1_BRIEF.md`, `LEXV2_2_BRIEF.md`, `N12_BRIEF.md`, `N14_BRIEF.md`, `N16_BRIEF.md`, `RENDER_BRIEF.md`, `SDBH_IMPORT_BRIEF.md` | feladat nélküli | régi, lezárt menetek |
| `F4_BRIEF.md`, `F4_GENERATOR_BRIEF.md`, `F5_BRIEF.md`, `F6_BRIEF.md`, `F7_BRIEF.md`, `F8_BRIEF.md` | feladat nélküli | atalakítási terv fázisai (l. 1/4.) |

Megjegyzés: a `FORDITAS_STILUSPROBA_FP2_BRIEF.md` a `.gitignore`-ban szerepel (nyers FP2-kimenet), de a repóban nincs ilyen fájl.

## 3. Nyitó prompt a briefekben (jelölendő `KOZVETLEN_FUTTATAS`-ba)

Van nyitó prompt: `CI_ELLENORZES` (5. sor), `CREMER_OCR` (7.), `F06` (108.), `F15` (7.), `F20` (25., már jelölt), `F4_BRIEF` (6.3–6.5), `F4_GENERATOR` (6.3–6.6), `F5` (6.1–6.2), `F6` (8.1–8.3), `F7` (7.), `F8` (7., 7b, 7c), `FORDITAS_PILOT` (6.), `FORRASJELOLTEK` (6.), `KARBANTARTAS` (6.), `KAROLI_KULCS` (6., 7.), `_KK7` (6.), `_KK75` (6., 7. merge-prompt), `LEX` (8.), `N12` (8.), `N14` (8.), `RENDER` (7.), `SDBH_IMPORT` (7.1–7.2), `SZOTAR` (7.), `TEREMT002_KUTATAS` (6.). Nincs: `ISTENTISZT_V3`, `LEXV2_1`, `LEXV2_2`, `N16` (a `grep` „nyitó prompt” nélkül; a tartalmukat a B2 nézi).
A jelölők csak a `## … Nyitó prompt` szakaszok körül kerülnek be, a szöveg nem változik. A többszörös (menetenkénti) promptoknál egy jelölőpár fogja a szakasz egészét.

## 4. `/kovetkezo` és CI

- Parancsfájl: `.claude/commands/kovetkezo.md` (52 sor, 11 lépés). A régi név/„Hol oszlop” kitétel a 4. lépésben.
- Workflow: `.github/workflows/ellenorzes.yml` (PR-on és `main`-re pushra) és **`f06_forrasfelmeres.yml`** (kézi indítású; a B0 indulásakor a helyi `main` még nem ismerte).
- Md-fájlt olvasó szabályok (`eszkozok/ellenorzes/szabalyok.py`): E2, E3, E6–E9, E12–E15 (`.md` végződésre szűrnek; E10/E11 hatóköre `adat/`/`lexikon/`, tehát a briefeket nem érinti), E5 (git diff, >30 sor törlés study-/sablon-fájlban), E16 (`.github/` és ellenőrző módosítása).
- Az új `F<nn>_…_BRIEF.md` gyökérfájlok a meglévő szabályok hatókörében nincsenek (E8/E9/E12–E15 a saját hatókör-listájukkal), de a B3 után `ellenorzes` futtatás kell.
- `beerkezo/` kizárása: a szabályok jelenleg útvonal-előtag alapján szűrnek; a kizárás (B6) az új szabályban és a `study_fajlok_szurese.py`-ben kell.

## 5. Brief-névre hivatkozások (átnevezéskor frissítendők; `naplok/` kivétel)

`git grep "_BRIEF"` a `naplok/` nélkül 58+ fájlban talál (főleg `eszkozok/*.py` docstringek, `adat/SEMA.md`, `adat/forditasok.tsv`, `adat/szotar_szerepek.tsv`, `CLAUDE.md` (`F4_BRIEF.md` „Tétel E”), `MUNKAMENET.md`, `NYITOTT_FELADATOK.md`, `DONTESEK.md`, `FELADATOK.md`, `GitHub_feltoltesi_workflow.md`, `.gitignore`, `.gitattributes`, `.claude/agents/fuggetlen-ellenor.md`, `.github/workflows/f06_forrasfelmeres.yml`, `eszkozok/ellenorzes/*`, `eszkozok/fj2/*`, a briefek egymás közt). A számozott feladatok (#1–#6, #9, #12, #14) átnevezése érinti ezeket; a feladat nélküli briefek neve a javaslat szerint **nem változik**, így hivatkozásaik sem. Mivel `adat/*.tsv` tartalomban is hivatkozik (`forditasok.tsv`, `szotar_szerepek.tsv`), a módosításuk adatsor-változás: a B3 csak a szövegmezőt érinti, `split('\t')`-tal, előtte/utána sorszám-összevetéssel.
- Ág neve/ráhagyott hivatkozások: a `.github/workflows/f06_forrasfelmeres.yml` a `F06_FORRASFELMERES_BRIEF.md`-re hivatkozik — már helyes név.

## 6. Nyitott ágak és PR-ek, amelyek a `FELADATOK.md`-t írhatják

Nyitott PR: **nincs** (`gh pr list`). Nem-merge-elt távoli ág: csak három régi (`bun-gyuruzese-20260911-sonnet`, `g1941-potlas-javaslat-2026-09-04`, `segitsegul-hivni-v12-compliance-2026-09-05`), a `FELADATOK.md`-hez nem nyúlnak. Helyi ágak (`claude/feladatok-*-kesz`, `claude/kovetkezo-modell` stb.) a távoli `main`-ben már benne vannak vagy nem érintik. Rebase-ütközés várható forrása: a #16–#19 / #7 csomag, amely a repóban ma nem látható.

## 7. D-számok

A `FELADATOK.md` saját döntésnaplója D1–D13. A szövegben hivatkozott további D-számok (#12 sor „D29”; D38, D40, D41 a „Kész” listában) a **SZOTAR_BRIEF** saját D-sorozatához tartoznak (más névtér), és a „D15” az FP2-D15. A brief D21–D30 számaival tehát **nincs ütközés a `main`-en**; a D14–D20 lyukas (valószínűleg a repón kívüli #16–#19 csomagé). Javaslat: az új döntések D21–D30 maradnak (D31-jelölt: feladat nélküli brief fejléce, l. 1/5.; D32-jelölt: szám nélküli „Kész” tételek kézi szakasza, l. 1/6.); a #12 sorban a „D29” `SZOTAR-D29`-re pontosítandó, hogy ne keveredjen az új D29-cel.

## 8. Következmények a lépésekre

- B1 nem függ ezektől, folytatható.
- A B2 munkalap a fenti eltéréseket kérdésként tartalmazza (E18 név, archív fejléc, szám nélküli „Kész” tételek, v1.1-alap).
- A B4 tartalmi összevetésének alapja a v1.1 (a brief v1.3-hoz képest kevesebb sor).
