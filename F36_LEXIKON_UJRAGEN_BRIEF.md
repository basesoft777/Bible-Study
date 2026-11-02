---
feladat: 36
cim: Az éles lexikon/ újragenerálása az F28, a BDB_PSI és a SIR_SZENTSZELLEM után
kod: LEXIKON_UJRAGEN
tipus: feladat
fazis: 2
modell: sonnet
munka: adat
allapot: lezarva
ad: a lexikon/[ID]_TUDOMANYOS.md és _TORZSCIKK.md fájlok a jelenlegi adatból újragenerálva; a nulla-diff / várt diff dokumentálva (az F28 fordításai, a javított ψ-igehelyek, a Szent Szellem-szöveg)
kovetkezo: "okafogyott (az orkesztrátor döntése a felhasználó 2026-11-02-i felhatalmazásával, DT496): a #11 egyforrású modellje óta a lap motívumonként generálódik; a #123 X.M5 újragenerál; az élő maradék: N-F123c, N-F123d"
lezarva_osszegzes: "(11.02) Okafogyott, futás nélkül (DT496). Az éles lexikon/ egészének újragenerálását a #11 (D34) óta a motívumonkénti generálás váltja fel: az ISTENTISZT-001 és az ALVIL-001 lapja migrálva, a többi hat a #123 X.M5-ben generálódik újra, a törzscikk archiválással megszűnik. Mért maradék (2026-11-02) a hat nem migrált lapon: 17–17 projekt-adat címke (N-F89a), a TAHOT hiánya az Irodalomból (N-F36a), a KIRALY-001 G0813-alszakasza (N-F132a) → N-F123c, N-F123d."
olvas: [lexikon/, naplok/F89_M0_felmeres.md, adat/licencek.tsv, eszkozok/lexikon_general.py, RENDER_BRIEF.md, adat/forditasok.tsv, adat/res_forras.tsv, ATALAKITASI_TERV.md.md]
ir: [lexikon/, generalt_proba/]
fugg: [28, 34, 35, 113]
nem_fugg: [7, 10, 27, 38, 121, 123, 126, 127, 131, 132]
---

# Éles lexikon/ újragenerálása

> **Lezárva, okafogyott (2026-11-02, F36.2, DT496).** A brief az egyforrású modell (#11, D34) előtti állapotra készült: egy futás az egész `lexikon/`-t generálta volna újra a régi forrásrétegből. Ma a lap motívumonként, a kézi forrásból generálódik. A két migrált lap (ISTENTISZT-001, ALVIL-001) friss, a hat nem migrált lapot a #123 X.M5 lépése generálja újra, a törzscikkét archiválja. Az alábbi kiegészítések élő tételei nem vesznek el: a #123 méri őket motívumonként (N-F123c: licenc-címke, TAHOT-forrásmegjelölés, STEPBible-kettőzés; N-F123d: KIRALY-001 G0813 → G0540). A brief többi szövege történeti.

## Háttér
Az F28 fordításai (39 szócikk), a ψ-javítás és a Szent Szellem-egységesítés a generált kimenetbe csak újragenerálás után kerülnek be. Generált fájlt kézzel szerkeszteni tilos (CLAUDE.md); a `generalt_proba/` verziózott könyvtár, nem scratch.

**Kiegészítés (N-F89a, DT-F89b 2., 2026.10.13).** A #89 (PR #332) a `projekt_adat` címkéjét `projekt-adat`-ról `minden jog fenntartva`-ra cserélte (`adat/SEMA.md` 2.19), de a lexikont nem generálta újra: a 8 éles `lexikon/*_TUDOMANYOS.md` 146 helyen még a régi címkét hordozza. A #89 próbafutása (`naplok/F89_M0_felmeres.md` 5. szakasz) szerint az éles írás 1476 beszúrt és 514 törölt sort adna, tartalmi blokkokkal is (pl. a KIRALY-001 kizárt jelöltjei 0 helyett 14). A címkecsere ezzel az újragenerálással együtt történik; a #89 merge-e az indulás előfeltétele.

**Kiegészítés (N-F132a, DT369 (b), 2026.10.28).** A #143 M0 szárazfutása (`naplok/F143_szarazfutas.md`) szerint a KIRALY-001 lexikonoldalainak G0813 → G0540 javítása (N-F132a; az `adat/elofordulasok.tsv` Zsid 7:1-28 sora, F132.19, DT337 (a)) nem választható le a rendszerszintű drifttől, ezért itt, az éles újragenerálással együtt élesedik; a #143 ebbe olvadt. Tudnivalók a futáshoz:
- A „Grep `G0813` → 0” ellenőrzés a `lexikon/KIRALY-001_TUDOMANYOS.md`-n szó szerint nem teljesülhet: a G0813 egyszer marad a [^9] proveniencia-lábjegyzetben, amely a javítást dokumentálja. A várt állapot: a „G0813 — ἄτακτος” alszakasz és a Thayer G813-szakasz megszűnik, a TORZSCIKK-ben a G0813 0 előfordulású, a Strong-mező `G5010+G0540+G0282`.
- A törzscikk-render a lexikonoldalra épül: a `--cel lexikon` és a `--cel torzscikk` ugyanabba a `--kimenet` könyvtárba menjen (N-F78a); külön könyvtárral az éles, elavult oldalból renderelne, és visszahozná a G0813-at.
- A G0540-hez nincs Thayer-sor és önálló Thayer G540 alszakasz: ez a #132 hatóköre marad, a #36 nem tölti ki (hiány, CLAUDE.md 3. szabály).

**Kiegészítés (N-F36a, a #131 hatókörén kívüli kimeneti hibái, PR #497, 2026.10.28).** A #131 (SZOTARI_GERINC) csak az ISTENTISZT-001 lapot generálta újra. A PR-leírás három, a többi lapot érintő hibát hagyott itt; mindhárom a kimenetet érinti, ezért az M1 diff-elemzés tételesen ellenőrzi:
- **TAHOT-forrásmegjelölés:** a TAHOT (CC BY 4.0, STEPBible) a másik 6 lap Irodalmából és licenclistájából hiányzik, pedig a lapok a `TAHOT_kivonat.tsv`-t forrásként nevezik meg (a #131 elve: DT383, ha a lap egy forrást megnevez, a forrásmegjelölés is ott áll). Várt: a #131 generátorával újragenerálva a lapokon megjelenik; ha nem, megállás.
- **STEPBible kettőzés a kolofonban:** a STEPBible-megjelölés kétszer áll. Ha az újragenerálás nem szünteti meg, ez generátorhiba (`eszkozok/lexikon_general.py`), amely nincs az `ir`-ben: ⛔ megállás, az `ir` bővítése a felhasználó döntése.
- **Elavult commitolt változat:** a másik 7 lap commitolt változata eltér a mai generátor kimenetétől (a #131 nulladiffje, `naplok/F131_SZOTARI_GERINC_naplo.md`). Ez a #36 tárgya; az eltérések oka az M1 kategóriái szerint nevezendő meg, a #131 szótári gerince (szakaszcímkék, BDB/Thayer-példák, DBH) külön kategória.
*(Helyőrző-azonosító; a végleges számot a `szamkiosztas` adja.)*

## Lépések
1. **M0 — szárazfutás** ideiglenes könyvtárba a repón kívül (`--kimenet`): az összes lexikonoldal és törzscikk generálása.
2. **M1 — diff-elemzés:** a generált és az éles közti eltérés fájlonként; minden eltérés oka megnevezve (F28 fordítás / ψ-javítás / terminológia v3 / licenc-címkecsere, N-F89a / egyéb); a licenc-címkecsere sorai (`projekt-adat` → `minden jog fenntartva`) külön számolva, szabad licenc-jelölés (CC BY stb.) a saját adatra és a prózára nem kerülhet be. Váratlan eltérés → megállás.
3. **⛔ M2 — jóváhagyás** az éles fájlok felülírása előtt.
4. **M3 — éles generálás**, ellenoriz.py és a CI (E-szabályok) zölddel; a RENDER_BRIEF.md G1/G4/G7 szabályai szerint.

## Nem cél
Új render-funkció; a lexikonoldalak kézi szerkesztése; tartalmi átírás.
