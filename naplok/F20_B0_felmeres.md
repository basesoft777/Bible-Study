# F20 B0 — felmérés (csak olvasás) — v2, a FELADATOK v1.3 alapján

*2026.09.30 · ág: `claude/befogadas`, rebase-elve az `origin/main`-re (`51f9291`, PR #77: `FELADATOK.md` v1.3 és a csomagos `/kovetkezo`) · forrás: `F20_BEFOGADAS_BRIEF.md` v1.2, 7. pont B0. A v1 felmérés (v1.1 alapon) érvénytelen; ez váltja.*

## 1. Eltérések a brief feltevéseihez képest (a B2-nél döntést kérnek, vagy már eldőltek)

1. **A v1.3 a main-ben van** (PR #77, `51f9291`): #16–#19 sorokkal, D14–D20-szal, csomagmóddal (Munkamenet 8.) és a csomagos `kovetkezo.md`-vel (3b, 6b lépés). A B5b ezt a main-beli fájlt módosítja. *(Eldőlt.)*
2. **A briefek közül az F07, F08, F16, F17, F18, F19 nincs a repóban.** A v1.3 „Hol” oszlopa e neveket már használja (`F07_THAYER_ELES_BRIEF.md`, `F08_LXX_DONTESEK_BRIEF.md`, `F16_BSB_IMPORT_BRIEF.md`, `F17_MACULA_IMPORT_BRIEF.md`, `F18_NAVE_IMPORT_BRIEF.md`, `F19_KJV_ASV_IMPORT_BRIEF.md`). A #10, #11, #13 sorai „brief csak chatben”/„—”. Mindegyikhez csonk kell (2. pont), a tényleges brief a `/befogad` csonk-kitöltésével kerül a helyére.
3. **Csomagmód vs. `ir` nélküli csonk.** A v1.3 a #16–#19 és a #7 csomagját írja elő. A csonknak nincs `ir`-je, így a 4.5 szerint csomagba nem kerülhet: a csomag a valódi briefek megérkezéséig (fejléccel, `olvas`/`ir`-rel) nem indulhat. *Ez a B7 egyik tesztesete lesz.*
4. **Az E17 név foglalt** (DONTESEK DT3, F15 brief 3.4: sorszám-változás küszöb). A feladatkövető szabály neve **E18** *(eldőlt, Q2)*.
5. **E16:** a `.github/` módosítása miatt a PR címe `[ELLENŐRZŐ]` előtagot kap *(eldőlt)*.
6. **Számozási névütközés:** `F4_BRIEF.md` … `F8_BRIEF.md` a terv fázisai; `tipus: archiv`, szám és átnevezés nélkül; az `ellenoriz` az archív briefeknél a fájlnév–szám egyezést nem vizsgálja *(eldőlt, Q3)*.
7. **A „Kész” listában szám nélküli tételek:** FJ 1. menet, TEREMT-002 1–2. lépés, Szótári brief v1.1 → kézi szakasz *(eldőlt, Q4)*.

## 2. Brief ↔ FELADATOK-sor megfeleltetés (v1.3 + „Kész” lista)

| Brief | Feladat | Megjegyzés |
|---|---|---|
| `KAROLI_KULCS_BRIEF.md` (+ `_KK7_`, `_KK75_`) | #1 (kész, `4b9ae49`) | a fő brief kapja a számot |
| `CI_ELLENORZES_BRIEF.md` | #2 (kész) | |
| `FORDITAS_PILOT_BRIEF.md` | #3 (kész) | |
| `KARBANTARTAS_BRIEF.md` | #4 (kész) | |
| `SZOTAR_BRIEF.md` | #5 (kész, S1) és #9 (S2) | a #9 csonk `forras: F05_SZOTAR_BRIEF.md#2. menet` |
| `F06_FORRASFELMERES_BRIEF.md` | #6 (kész, a „Kész” listában) | már `F06_` nevű |
| — | #7 Thayer éles | v1.3 „Hol”: `F07_THAYER_ELES_BRIEF.md` v3; nincs a repóban → csonk |
| — | #8 LXX-döntések | `F08_LXX_DONTESEK_BRIEF.md`; nincs → csonk |
| — | #16 BSB, #17 Macula, #18 Nave, #19 KJV/ASV | `F16…F19_…_BRIEF.md`; nincs → csonk (mind függ #6-tól; #8 függ #17-től) |
| — | #10, #11, #13 | „brief csak chatben” → csonk |
| `TEREMT002_KUTATAS_BRIEF.md` | #12 (3. lépés) | a fájl csak T1–T2-t ír le (kész) → archív; #12 külön csonk |
| — | #14 FP2 (kész) | csak naplók → `lezarva` csonk |
| `F15_ORKESZTRATOR_BRIEF.md` | #15 (kész) | már `F15_` nevű |
| `F20_BEFOGADAS_BRIEF.md` | #20 | már új fejlécű |
| `FORRASJELOLTEK_BRIEF.md`, `CREMER_OCR_BRIEF.md`, `ISTENTISZT_V3_BRIEF.md`, `LEX_BRIEF.md`, `LEXV2_1/2_BRIEF.md`, `N12/N14/N16_BRIEF.md`, `RENDER_BRIEF.md`, `SDBH_IMPORT_BRIEF.md`, `F4_BRIEF.md`, `F4_GENERATOR_BRIEF.md`, `F5–F8_BRIEF.md`, `KAROLI_KULCS_KK7/KK75_BRIEF.md` | feladat nélküli | `archiv` |

## 3. Nyitó prompt a briefekben

Van (jelölendő `KOZVETLEN_FUTTATAS`-ba): `CI_ELLENORZES` (5. sor), `CREMER_OCR` (7.), `F06` (108.), `F15` (7.), `F4_BRIEF` (6.3–6.5), `F4_GENERATOR` (6.3–6.6), `F5` (6.1–6.2), `F6` (8.1–8.3), `F7` (7.), `F8` (7., 7b, 7c), `FORDITAS_PILOT` (6.), `FORRASJELOLTEK` (6.), `KARBANTARTAS` (6.), `KAROLI_KULCS` (6., 7.), `_KK7` (6.), `_KK75` (6., 7.), `LEX` (8.), `N12` (8.), `N14` (8.), `RENDER` (7.), `SDBH_IMPORT` (7.1–7.2), `SZOTAR` (7.), `TEREMT002_KUTATAS` (6.). `F20`: már jelölt. Nincs: `ISTENTISZT_V3`, `LEXV2_1`, `LEXV2_2`, `N16`. A jelölők csak a szakaszok köré kerülnek, a szöveg nem változik.

## 4. `/kovetkezo` és CI

- `.claude/commands/kovetkezo.md` (v1.3, 73 sor): a 3b (csomag) és a 6b (worktree, párhuzamos subagentek) már benne van; a 4. lépésben még a régi név / „Hol” oszlop kitétele áll; a 6b/10. lépés a „saját sor” közös fájlba írását írja elő (ezt a B5b fejléc-írásra cseréli).
- Workflow-k: `.github/workflows/ellenorzes.yml` (PR-on és main-push-ra), `f06_forrasfelmeres.yml` (kézi indítású).
- Md-fájlt olvasó szabályok (`eszkozok/ellenorzes/szabalyok.py`): E2, E3, E6–E9, E12–E15; E5 (git diff, >30 sor törlés study-/sablon-fájlban); E10/E11 hatóköre `adat/`/`lexikon/`; E16 (`.github/`, ellenőrző módosítása → `[ELLENŐRZŐ]` cím).
- Új szabály neve **E18**; a B6-ban külön jobként kerül a workflow-ba (meglévő lépést nem módosít, D6).
- `beerkezo/` kizárása: az új szabály a gyökér `*_BRIEF.md` fájljait nézi, a `beerkezo/` a hatókörén kívül van; a `study_fajlok_szurese.py` nem érinti.

## 5. Brief-névre hivatkozások

`git grep "_BRIEF"` (a `naplok/` nélkül) 58+ fájlban (főleg `eszkozok/*.py` docstringek, `adat/SEMA.md`, `adat/forditasok.tsv`, `adat/szotar_szerepek.tsv`, `CLAUDE.md`, `MUNKAMENET.md`, `NYITOTT_FELADATOK.md`, `DONTESEK.md`, `FELADATOK.md`, `GitHub_feltoltesi_workflow.md`, `.gitignore`, `.gitattributes`, `.claude/agents/fuggetlen-ellenor.md`, `f06_forrasfelmeres.yml`, `eszkozok/ellenorzes/*`, `eszkozok/fj2/*`, briefek egymás közt). Átnevezés csak a #1–#5 briefet érinti (öt `git mv`); a többi név marad, hivatkozásaik is. Az `adat/*.tsv` szövegmezőit csak `split('\t')`-tal, sorszám-összevetéssel szabad módosítani.

## 6. Nyitott ágak és PR-ek

Nyitott PR: nincs. Nem-merge-elt távoli ág: csak három régi (nem érintik a `FELADATOK.md`-t). A #7, #16–#19 csomag sessionje a repóban nem látszik (nincs ága); rebase-ütközés várható forrása, ha elindul: a `FELADATOK.md` sorai — a B8 PR-szövege ezt a v1.3-as csomagra rögzíti.

## 7. D-számok

A `FELADATOK.md` döntésnaplója D1–D20. A D21–D30 **szabad**, nincs ütközés; a #12 sor „D29” a SZOTAR-brief saját sorozata (más névtér), ezért a generált sorban `SZOTAR-D29`. A brief D22 a D3-at, a D26 a Munkamenet 6. pontját, a D20 (csomag) a B5b/6b-t érinti: a D20 „saját sorait írja” szabálya fejléc-írásra változik.

## 8. Következmények

- B1 (kész) nem függ ezektől.
- A B2 munkalap a v1.3-ra épül: #16–#19 és #7 csonk (csomag-próbához `ir` kell), függések a v1.3 szerint.
- B5c: a Munkamenet 1., 2., 5., 6. és **8.** pontja változik (a 8. „közös fájlban a saját sorait” → saját brief-fejléc).
