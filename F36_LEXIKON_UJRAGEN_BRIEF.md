---
feladat: 36
cim: Az éles lexikon/ újragenerálása az F28, a BDB_PSI és a SIR_SZENTSZELLEM után
kod: LEXIKON_UJRAGEN
tipus: feladat
fazis: 2
modell: sonnet
allapot: nem_indult
ad: a lexikon/[ID]_TUDOMANYOS.md és _TORZSCIKK.md fájlok a jelenlegi adatból újragenerálva; a nulla-diff / várt diff dokumentálva (az F28 fordításai, a javított ψ-igehelyek, a Szent Szellem-szöveg)
kovetkezo: M0 szárazfutás ideiglenes könyvtárba (a repón kívülre); ⛔ az éles fájlok felülírása előtt
olvas: [lexikon/, eszkozok/lexikon_general.py, RENDER_BRIEF.md, adat/forditasok.tsv, adat/res_forras.tsv, ATALAKITASI_TERV.md.md]
ir: [lexikon/, generalt_proba/]
fugg: [28, 34, 35]
---

# Éles lexikon/ újragenerálása

## Háttér
Az F28 fordításai (39 szócikk), a ψ-javítás és a Szent Szellem-egységesítés a generált kimenetbe csak újragenerálás után kerülnek be. Generált fájlt kézzel szerkeszteni tilos (CLAUDE.md); a `generalt_proba/` verziózott könyvtár, nem scratch.

## Lépések
1. **M0 — szárazfutás** ideiglenes könyvtárba a repón kívül (`--kimenet`): az összes lexikonoldal és törzscikk generálása.
2. **M1 — diff-elemzés:** a generált és az éles közti eltérés fájlonként; minden eltérés oka megnevezve (F28 fordítás / ψ-javítás / terminológia v3 / egyéb). Váratlan eltérés → megállás.
3. **⛔ M2 — jóváhagyás** az éles fájlok felülírása előtt.
4. **M3 — éles generálás**, ellenoriz.py és a CI (E-szabályok) zölddel; a RENDER_BRIEF.md G1/G4/G7 szabályai szerint.

## Nem cél
Új render-funkció; a lexikonoldalak kézi szerkesztése; tartalmi átírás.
