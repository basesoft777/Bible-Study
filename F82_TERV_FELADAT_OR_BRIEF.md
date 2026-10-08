---
feladat: 82
cim: Terv → feladat gépi őr — a tervek jelölt mutató-tábláinak minden sora feladatban, briefben vagy jelölten elavult/feltételes
kod: TERV_FELADAT_OR
tipus: feladat
fazis: 1
modell: sonnet
munka: folyamat
allapot: fut
ag: claude/f82-terv-feladat-or
ad: a `feladatok.py ellenoriz` (és így a CI E18 és a /kovetkezo 1. lépése) HIBÁT ad, ha a tervdokumentumok jelölt mutató-táblájának egy sora sem FELADATOK-számra/briefre (`#nn`, `kod`), sem „elavult”/„feltételes”/„lezárva” jelölésre nem mutat; a jelölő-formátum rögzítve, tesztekkel; a mai repón 0 hiba
kovetkezo: M1 (szabály és teszt), majd M2, M3
olvas: [ATALAKITASI_TERV.md.md, MUNKATERV.md, ADATVAGYON_TERV.md, eszkozok/feladatok.py, eszkozok/teszt_feladatok.py, BRIEF_SABLON.md, naplok/TERV_INTEGRACIO_zaras.md, naplok/TERV_INTEGRACIO_leltar.md, naplok/TERV_INTEGRACIO_dontesi_lista.md]
ir: [eszkozok/feladatok.py, eszkozok/teszt_feladatok.py, ATALAKITASI_TERV.md.md, MUNKATERV.md, ADATVAGYON_TERV.md]
fugg: []
nem_fugg: [52]
---

# F82_TERV_FELADAT_OR_BRIEF.md — Terv → feladat gépi őr

*FELADATOK #82 · Modell: sonnet · v1 · 2026.10.08 · döntés: DT78 (19) (1): „gépi őr: #82, külön ágon, D6” (Felhasználó, 2026-10-08, chat) · ág: `claude/f82-terv-feladat-or`*

## 1. Cél

A TERV-INTEGRÁCIÓ (`naplok/TERV_INTEGRACIO_leltar.md`) gyökéroka: a tervdokumentumok feladat-, lépcső- és döntés-elemei a #52 naplójában maradtak, és senki nem hajtotta be őket. A kemény zár (DT78 (19)) három rétegéből a (2) `/konzisztencia` 5. kategória, a (3) #52 terv → feladat lépés (3b) és a `/kovetkezo` megállási mondata kész (TI.11); ez a feladat az **(1) gépi őr**: a `python eszkozok/feladatok.py ellenoriz` HIBÁT ad, ha egy jelölt tervelem nincs feladatként.

Az őr **csak a jelölt mutató-táblákat** olvassa, nem a terv szabad szövegét: a száraz próba (`naplok/TERV_INTEGRACIO_zaras.md` 4. pont) a teljes szövegen zömmel hamis találatot adott — PR-számok (#205, #167, #218…), fájl- és dataset-nevek (SECE_H, LXX_OS, VIBE_GUIDE, F4_BRIEF), oszlopnevek (AZONOSITAS_MODJA), a lezárt TERV_BEFOGAD.

## 2. Hatókör

**Benne van:**
- a jelölő-formátum: a mutató-tábla jelölőpár közé kerül (javaslat: `<!-- TERVELEM-MUTATO -->` … `<!-- /TERVELEM-MUTATO -->`, a `RÉS-KEZDET` / `GENERÁLT-KEZDET` mintájára); a tábla oszlopai `terv-elem | feladat | állapot`; a formátum leírása az `ATALAKITASI_TERV.md.md` 13.4 bevezető mondatában (ha az M0 úgy dönt, az `adat/SEMA.md`-ben — ehhez a brief `ir`-je bővül, tételként rögzítve);
- a jelölők elhelyezése: az ATALAKITASI 13.4 táblája biztosan; a MUNKATERV 4. szakasz táblája és az ADATVAGYON 21. lépcső-táblája az M0 javaslata szerint;
- a szabály a `feladatok.py ellenoriz`-ben: a jelölt tábla minden sorában a `feladat` cella (a `\_` → `_` visszaalakítás után) tartalmaz (a) egy létező feladatszámot (`#nn`, a brief-fejlécek `feladat` mezője szerint), vagy (b) egy létező `kod`-ot, vagy (c) „elavult” / „feltételes” / „lezárva” jelölést, vagy (d) DT-/D-tétel hivatkozást, amely a `DONTESEK.md`-ben / a `FELADATOK.md` döntésnaplójában létezik; különben HIBA (`fájl:sor`, a sor első cellája, a hiányzó elem);
- tesztek az `eszkozok/teszt_feladatok.py`-ban (fixture-tervvel, a meglévő minta szerint).

**Nincs benne:** a terv szabad szövegének elemzése; a tervek tartalmi átírása (csak a jelölőpár és, ha hiányzik, a mutató-tábla sora); a `/konzisztencia` és a #52 (azok kész rétegek); új CI-szabályszám (az `ellenoriz` már az E18-ban fut).

## 3. Lépések (⛔ a kötelező megállások)

**M0 — felmérés (csak olvas).** A három terv táblái közül melyik „feladat-mutató” (sor = tervelem, oszlop = feladat); a jelölő-formátum javaslata; száraz próba a javasolt szabállyal a mai repón (a hibás sorok listája, proveniencia-sorral). ⛔ **Megállás:** a jelölő-formátum és a jelölt táblák listája a felhasználóé (`DONTESEK.md`, helyőrző `DT-F82a`).

**M1 — szabály és teszt.** A szabály a `feladatok.py`-ban (egy függvény, a meglévő `ellenoriz` hibalistájába kötve); `split('\t')`/szövegfeldolgozás, a `csv` modul nem kell. Tesztek legalább: jó sor `#nn`-nel; jó sor `kod`-dal (`SQLITE\_EPIT` escape-pel is); `feltételes`/`elavult`/`lezárva` sor; nem létező `#99` → HIBA; jelölőn kívüli `#205` és `SECE_H` → nem számít; hiányzó záró jelölő → HIBA (a tábla nem tűnhet el csendben).

**M2 — jelölők a tervekben, 0 hiba.** A jelölőpárok beírása az M0 döntése szerint; ahol egy sor ma hibát adna, az a 3b (#52) szabálya szerint kap kimenetet: hivatkozást, „elavult”/„feltételes” jelölést, vagy ⛔ (új feladat nem itt születik). `python eszkozok/feladatok.py ellenoriz` = 0 hiba a repón.

**M3 — zárás.** `python eszkozok/teszt_feladatok.py`, `python eszkozok/ellenoriz.py`, `python eszkozok/ellenorzes/futtat.py --teljes` zöld; zárás `naplok/F82_zaras.md`; draft PR; a `fuggetlen-ellenor` az orkesztrátoré. A `.claude/commands/kovetkezo.md` 1. lépésének őr-mondata ettől kezdve fed le valamit (a jelölés „a #82 vezeti be” törölhető — ez az orkesztrátor/felhasználó lépése, nem a #82 `ir`-je).

## 4. Elfogadási feltételek

1. Jelölt mutató-tábla legalább az ATALAKITASI 13.4-ben; a formátum leírva (a terv vagy a SEMA egy helyén).
2. Az `ellenoriz` HIBÁT ad a hibás jelölt sorra, és csak arra: a száraz próba hamis találatai (jelölőn kívüli PR-szám, fájl-, dataset- és oszlopnév) 0 találatot adnak.
3. A tesztek az M1 hat esetét lefedik, zöldek.
4. A mai repón `feladatok.py ellenoriz` = 0 hiba; `ellenoriz.py` SÉRTÉS 0; `futtat.py --teljes` exit 0.
5. A D6 szerint a PR csak ezt a feladatot hozza (külön ág), más feladat tartalmát nem módosítja.

## 5. Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| — | Az őr csak jelölt mutató-táblát olvas (DT78 (19) (1), a felhasználó „a” válasza, 2026-10-08) | a szabad szövegen a száraz próba zömmel hamis találatot adott |
| — | Külön feladat, külön ág (D6) | a PR ne írja meg a saját ellenőrzését |
| — | `fazis: 1` | a /kovetkezo csak 1. fázisú jelöltet ajánl; a zár az egész feladatláncot védi (D51 elve) |
