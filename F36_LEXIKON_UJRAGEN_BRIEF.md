---
feladat: 36
cim: Az éles lexikon/ újragenerálása az F28, a BDB_PSI és a SIR_SZENTSZELLEM után
kod: LEXIKON_UJRAGEN
tipus: feladat
fazis: 2
modell: sonnet
munka: adat
allapot: nem_indult
ad: a lexikon/[ID]_TUDOMANYOS.md és _TORZSCIKK.md fájlok a jelenlegi adatból újragenerálva; a nulla-diff / várt diff dokumentálva (az F28 fordításai, a javított ψ-igehelyek, a Szent Szellem-szöveg)
kovetkezo: befagyasztva a #11 1. lépcsőjéig (DT74 (3): a régi forrásréteg és az éles lexikon nem bővül a régi szerkezet szerint); utána: M0 szárazfutás ideiglenes könyvtárba (a repón kívülre); ⛔ az éles fájlok felülírása előtt
olvas: [lexikon/, naplok/F89_M0_felmeres.md, adat/licencek.tsv, eszkozok/lexikon_general.py, RENDER_BRIEF.md, adat/forditasok.tsv, adat/res_forras.tsv, ATALAKITASI_TERV.md.md]
ir: [lexikon/, generalt_proba/]
fugg: [28, 34, 35, 113]
nem_fugg: [7, 10]
---

# Éles lexikon/ újragenerálása

## Háttér
Az F28 fordításai (39 szócikk), a ψ-javítás és a Szent Szellem-egységesítés a generált kimenetbe csak újragenerálás után kerülnek be. Generált fájlt kézzel szerkeszteni tilos (CLAUDE.md); a `generalt_proba/` verziózott könyvtár, nem scratch.

**Kiegészítés (N-F89a, DT-F89b 2., 2026.10.13).** A #89 (PR #332) a `projekt_adat` címkéjét `projekt-adat`-ról `minden jog fenntartva`-ra cserélte (`adat/SEMA.md` 2.19), de a lexikont nem generálta újra: a 8 éles `lexikon/*_TUDOMANYOS.md` 146 helyen még a régi címkét hordozza. A #89 próbafutása (`naplok/F89_M0_felmeres.md` 5. szakasz) szerint az éles írás 1476 beszúrt és 514 törölt sort adna, tartalmi blokkokkal is (pl. a KIRALY-001 kizárt jelöltjei 0 helyett 14). A címkecsere ezzel az újragenerálással együtt történik; a #89 merge-e az indulás előfeltétele.

## Lépések
1. **M0 — szárazfutás** ideiglenes könyvtárba a repón kívül (`--kimenet`): az összes lexikonoldal és törzscikk generálása.
2. **M1 — diff-elemzés:** a generált és az éles közti eltérés fájlonként; minden eltérés oka megnevezve (F28 fordítás / ψ-javítás / terminológia v3 / licenc-címkecsere, N-F89a / egyéb); a licenc-címkecsere sorai (`projekt-adat` → `minden jog fenntartva`) külön számolva, szabad licenc-jelölés (CC BY stb.) a saját adatra és a prózára nem kerülhet be. Váratlan eltérés → megállás.
3. **⛔ M2 — jóváhagyás** az éles fájlok felülírása előtt.
4. **M3 — éles generálás**, ellenoriz.py és a CI (E-szabályok) zölddel; a RENDER_BRIEF.md G1/G4/G7 szabályai szerint.

## Nem cél
Új render-funkció; a lexikonoldalak kézi szerkesztése; tartalmi átírás.
