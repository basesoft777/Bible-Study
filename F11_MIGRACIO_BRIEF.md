---
feladat: 11
cim: Migráció: egy forrásból renderelés
kod: MIGRACIO
tipus: feladat
fazis: 1
modell: opus
allapot: megallt
ag: claude/f11-migracio
munka: ertelmezo
ad: az `indoklas` oszlop felvéve a `kapcsolatok.tsv`-be (önálló séma-tétel), az ISTENTISZT-001 egyetlen kézi forrásból renderel (szétválasztással, leképezési táblával, N0/D2–D6 diffmérce szerint), a két élő sablon (2_ v18, 4_ v10) visszaírási szabálya teljesen átírva; a 2. lépcső (a többi 6 motívum) külön jóváhagyással
kovetkezo: Te: az M1 (leképezési tábla) jóváhagyva és a main-en (PR #393, 2026-10-18); az M2 (generátor-képességek) a #116 (E28/E29, D6) merge-e után, külön jóváhagyással indul
pr: #393
olvas: [tematikus_lezart/ISTENTISZT-001*, tematikus_lezart/naplok/ISTENTISZT-001*, ADATVAGYON_TERV.md, MUNKATERV.md, ATALAKITASI_TERV.md.md, adat/szotar_szerepek.tsv, adat/SEMA.md, naplok/MOTIVUM_FORRAS_pilot_terv.md, naplok/MOTIVUM_FORRAS_ci_terv.md, naplok/MOTIVUM_FORRAS_lekepezes.tsv, naplok/MOTIVUM_FORRAS_M0.py, naplok/F23_zaras.md, F23_MOTIVUM_FORRAS_BRIEF.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md, tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md, generalt_proba/F78_szerepmatrix_proba/, eszkozok/nulladiff.sh, eszkozok/general.py]
ir: [adat/SEMA.md, adat/kapcsolatok.tsv, adat/jeloltek.tsv, adat/lexikon_hivatkozasok.tsv, adat/res_forras.tsv, adat/auditok.tsv, eszkozok/betolt.py, eszkozok/ellenoriz.py, eszkozok/f3_1_betoltes.py, eszkozok/sqlite_epit.py, eszkozok/general.py, eszkozok/lexikon_general.py, eszkozok/torzscikk_general.py, motivumok/ISTENTISZT-001.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, lexikon/ISTENTISZT-001_TORZSCIKK.md, tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md, tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/4_PaRDeS_tematikus_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, naplok/F11_szetvalasztas_ISTENTISZT-001.tsv, naplok/F11_zaras.md, naplok/ELLENOR_F11_S.md, naplok/ELLENOR_F11_M.md]
fugg: [9, 23, 116]
nem_fugg: [27, 38, 52, 55, 107, 109, 110]
---

# F11_MIGRACIO_BRIEF.md — Migráció: egy forrásból renderelés

*FELADATOK #11 · Modell: opus · v1 · 2026.10.17 · döntések: D34, D38, DT28, DT66, DT74 (3), DT78 (22), DT84, DT182, DT183*

**Állapot-megjegyzés a befogadáshoz.** A #23 (a pilot-terv forrása) munkája a `main`-en van (PR #370 ága már nem hordoz saját commitot), de a #23 `allapot: fut`. A #11 `fugg: [9, 23]` ezért addig nem engedi a futtatást, amíg a #23 le nem zárul és a #9 el nem készül; a brief tartalma a pilot-tervre épül, és a `main`-en olvasható.

## 1. Cél

A D34 (B út) megvalósítása a **1. lépcsőn**: az ISTENTISZT-001 motívum egyetlen kézi forrásból (`motivumok/ISTENTISZT-001.md` + adattáblák) renderel. A migráció a DT28 szerint **szétválasztás**, nem visszaírás: minden egység pontosan egy rétegbe kerül (`adat` / `forras` / `generalt` / `archivum`). A mérce: a migrált forrásból generált lexikonoldal az aranymintától (`generalt_proba/F78_szerepmatrix_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md`) csak az elfogadott diff-kategóriákban (D2–D6) tér el, a nem migrált HAMART-001 kimenete bájtra azonos (N0). Az 1. lépcső merge-e oldja a DT74 (3) befagyasztását.

Két további kötelezettség (felhasználói döntések, 2026-10-17):

- **DT183:** az `indoklas` oszlop felvétele a `kapcsolatok.tsv`-be a #11 **első, önálló séma-tétele**, saját commitokkal és független ellenőrzéssel, a migráció előtt.
- **DT182:** a `sablonok/2_PaRDeS_bovitett_sablon.md` (v18) „Tartalmi visszaírás lezárt tematikus tanulmányba” és a `sablonok/4_PaRDeS_tematikus_sablon.md` (v10) „Tartalmi visszaírás bővített tanulmányokba” szabályának, valamint a 4_ Lezárási checklist 12. pontjának **teljes átírása** (ma felfüggesztő sor áll előttük, F23.D14). A két sablon ezért az `ir` mezőben van.

## 2. Hatókör

**Benne van:** S. séma-tétel (S1–S3) · M. az ISTENTISZT-001 migrációja (M1–M7) · T. a két sablon átírása · a visszaírás-számláló, a leképezési tábla, a diff-jelentés · a HAMART-001 kontroll.

**Nincs benne:** a másik 6 motívum migrációja (2. lépcső: az 1. lépcső ⛔ jóváhagyása után külön lépésenként, D38; ha a keret kicsi, külön brief) · a `genezis/` tartalma (a #23 pilot-terv 4.5: nem íródik) · a TEREMT-002 és a sablon `v1` véglegesítése (#12) · az E28/E29 CI-szabályok implementációja (külön ág, D6) · a törzscikk-generálás kivezetése az összes motívumra (csak az ISTENTISZT-001 törzscikke törlődik) · a repó láthatósága (N-F23c).

## 3. Lépések (⛔ a kötelező megállások)

**0. Modell-ellenőrzés** (CLAUDE.md): a kért modell `opus`; eltérésnél állj meg.

### S. Séma-tétel — a migráció előtt, önálló commitokkal

- **S1.** `adat/SEMA.md` 2.3: új `indoklas` mező (szabad szöveg, nem kötelező; az Alátámasztás soronkénti adata, SEMA 3.10.7 1.); a `kapcsolatok.tsv` fejléce kiegészül (`split('\t')` / `'\t'.join()`, a `csv` modul tilos); a meglévő sorok (az ISTENTISZT-001-nek 25, a többinek is) **üres** `indoklas` értéket kapnak — a tábla többi cellája bájtra változatlan (írás előtti és utáni összevetés, minta: `eszkozok/igazolas_migracio.py`).
- **S2.** A tábla olvasói és írói: a `grep` szerinti lista (`betolt.py`, `ellenoriz.py`, `f3_1_betoltes.py`, `sqlite_epit.py`, `lexikon_general.py`, `torzscikk_general.py`, `t2_*`, `zaro2_*`) átnézve, az oszlopsorrendtől függő olvasás (pozicionális indexelés, rögzített oszlopszám) javítva; a `sqlite_epit.py` és a CI-ellenőrzés az új oszlopot ismeri. A generált kimenet nem változhat (nulla-diff a HAMART-001-en és az ISTENTISZT-001-en).
- **S3. ⛔ Független ellenőrzés** (`fuggetlen-ellenor`): `naplok/ELLENOR_F11_S.md`. Csak zöld/javított ellenőrzés után indulhat az M.

### M. Az ISTENTISZT-001 migrációja (pilot-terv 4–7.)

- **M1. Leképezési tábla** `naplok/F11_szetvalasztas_ISTENTISZT-001.tsv` (pilot-terv 7.2 oszlopai): a 166 blokk, a vegyes blokkok részegységekre bontva (DT84 (11)); az ISTENTISZT-001 lapján álló 14 `【NAPLO】` (az összes éles lapon 36) egyenként ítélve (folyamat-nyom `belso`; megbízhatóságot érintő figyelmeztetés → apparátus-szövegként újraírva, külön indokolt sorral, DT84 (10) (ii)). A 7. Nyitott kérdések öt tétele a pilot-terv 4.4 szerint. **⛔ A tábla jóváhagyása a felhasználótól, mielőtt bármi mozog.**
- **M2. Generátor-képességek** (E28/E29 külön ágon előtte, D6): forrás olvasása szintszűréssel (`olvasoi`/`apparatus`/`belso`), kinyerés (`JELÖLT` → `jeloltek.tsv`, `ADAT-HIV`/`ADAT-ÉRTÉK` ellenőrzés, kinyerési jelentés; az audit-sort nem a lábjegyzet írja, DT84 (2)). Minden generátor-commit után: `eszkozok/nulladiff.sh` a HAMART-001-en, `--csere` nélkül, üres diff (N0).
- **M3. A szétválasztás végrehajtása** a jóváhagyott tábla szerint: az `adat` egységek a `jeloltek.tsv`-n át, döntéssel, `manual` provenienciával (nem igehely-kulcsú adat a SEMA 3.10.7 4. útján); a `forras` egységek bájtra a `motivumok/ISTENTISZT-001.md`-be; a kézi `indoklas` (Alátámasztás) a `kapcsolatok.tsv`-be; az `archivum` egységek a régi fájlok változatlan, archív fejlécű példányában. **⛔ Az archív könyvtár neve (DT-F11a, lásd 5.) a végrehajtás előtt eldöntve.**
- **M4. Mérés:** (a) aranyminta ↔ migrált render, `nulladiff.sh` `--csere` csak a D2 előre felsorolt literáljaira; minden más eltérés **ÁLLJ**; (b) HAMART-001 N0; (c) visszaírás-számláló = 0 (pilot-terv 7.4); (d) nincs egység két rétegben (n-gram, `MOTIVUM_FORRAS_M0.py` módszere, elvárt 0); (e) L1–L7 + DT2; (f) E28/E29 kézi futtatása.
- **M5.** A `lexikon/ISTENTISZT-001_TORZSCIKK.md` törlése (D6 diff-kategória; az éles ISTENTISZT-001 lap a migrált forrásból generált). A `FELADATOK.md` hivatkozásai ugyanabban a commitban.
- **M6. ⛔ Független ellenőrzés** (`naplok/ELLENOR_F11_M.md`) a teljes base..head diffen.
- **M7.** Az ISTENTISZT-001 forrásában a beemelt nevesített tanítói sor hivatkozássá alakul a 7. lépés saját fájljára (DT66 (2), DT88); ha a saját fájl nem létezik: DT-tétel és megállás.

### T. A két sablon átírása (DT182, a migrációval együtt)

- **T1.** `sablonok/2_PaRDeS_bovitett_sablon.md` 7. pont: a felfüggesztett szabály helyén a B-beli szabály (a bővítettben felmerült lelet adatrésze a `jeloltek.tsv`-n át, döntéssel; az értelmezés saját szöveggel a `motivumok/[ID].md`-be; a túloldalon csak hivatkozás; kézi másolás egyik irányban sincs); a „Korlát” bekezdés és a verziósor frissítve (a v21 tervezett, a tényleges szám a futtatáskor).
- **T2.** `sablonok/4_PaRDeS_tematikus_sablon.md`: a „Tartalmi visszaírás bővített tanulmányokba” alszakasz (447. sor körül) megszűnik / „megszűnt, l. DT84 (7)” jelölést kap; a Lezárási checklist 12. pontja átírva (a hivatkozott szabály megszűnt); a v10 verziósor és a szakaszra mutató belső hivatkozások (60., 243., 424–430. sor) frissítve. Lezárt tanulmányba és a `genezis/`-be nem kerül semmi.
- **T3.** A korábban visszaírt leletek soronkénti besorolása (pilot-terv 4.5): generált visszamutató link / `archivum` / törlés. A link forrása (N-F23a) a DT-F11b szerint.

## 4. Elfogadási feltételek

1. S3 ellenőrzés zöld, mielőtt az M1 elindul; az S-commitok külön állnak.
2. A leképezési tábla teljes (166 blokk + részegységek, pontosan egy sor mindegyikre), jóváhagyott.
3. Az aranymintához csak N0 és D2–D6 (pilot-terv 5.); a HAMART-001 diff üres, `--csere` nélkül.
4. A visszaírás-számláló 0; nem besorolt sor a táblában.
5. A két sablon szövege a B-beli alakot hordozza; nincs a repóban élő utasítás, amely kézi másolást ír elő (grep a `Tartalmi visszaírás` kifejezésre, eredmény a zárónaplóban).
6. `python eszkozok/feladatok.py ellenoriz` 0 hiba; a hivatkozás-ellenőrzés (E27) zöld.
7. Az M6 ellenőrzés után zárónapló `naplok/F11_zaras.md`; a befagyasztás oldása csak ezután (DT74 (3)).

## 5. Döntésnapló (helyőrzők; végleges számot a `szamkiosztas` Action ad)

- **DT-F11a** — az `archivum` kategória könyvtárának neve és fejléc-alakja (DT84 (12)). *Eldöntendő az M3 előtt.*
- **DT-F11b** — az N-F23a: a generált visszamutató link forrása (normalizált hivatkozás-mező az `elofordulasok.tsv`-ben, vagy más). *Eldöntendő a T3 előtt.*
- **DT-F11c** — a 2. lépcső (6 motívum) ütemezése: ugyanebben a feladatban, vagy külön briefben. *Eldöntendő az M6 után.*
- **N-F11a** — a MCGED (Mounce Concise Greek-English Dictionary, „© Mounce 1993”) licenckérdése: a tematikus 2/b Mounce-táblája (leképezési tábla T53–T54) a felhasználó 2026-10-18-i döntése szerint archívumba kerül, nem az adatrétegbe; nyitva, hogy a licenc (a `licencek.tsv` szerint csak nem kereskedelmi újraterjesztés, megjelöléssel) megengedi-e később a `lexikon_hivatkozasok.tsv`-be emelést. *A `NYITOTT_FELADATOK.md`-be a merge után, `/befogad` útján.*
- **Megjegyzés a #12-nek (sablon 9 véglegesítése)** — a sablon 9 4. pontja nem ad helyet az 1. Előfordulások szakaszban álló értelmező prózának (az 1.L feltétele csak igehely-tartományú sornál áll fenn); az ISTENTISZT-001-en ez hat blokk (leképezési tábla T15, T17, T18, T20/1, T22/1, T24), amely a felhasználó 2026-10-18-i döntése szerint RÉS-en kívüli kísérő prózaként áll az 1.T nézet után.
- **N-F23b / N-F23c** — a build-szűrő közös volta a #86-tal, a repó nyilvánossága: nyitva marad; a #11 nem dönti el.
