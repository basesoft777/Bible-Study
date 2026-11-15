---
feladat: 222
cim: Heti beosztás (heti terv a valós állapottal), felmérés munkatípus és ötlettár
kod: HETI_BEOSZTAS
tipus: feladat
fazis: folyamat
sav: SYSTEMS
modell: sonnet
allapot: fut
ag: claude/vibrant-borg-bbaa4d
ad: három adattábla (`adat/heti_terv.tsv`, `adat/otlettar.tsv`, a kézi keret-értékekkel: `adat/heti_keret.tsv`) és három mérési tábla (`adat/keret_sulyok.tsv`, `adat/keret_munkamappa.tsv`, `adat/heti_keret_meres.tsv`) a SEMA-ban; egy oldal-generátor (`eszkozok/heti_beosztas.py`), amely a heti tervet sávonként, a brief-fejlécekből és a PR-okból számolt valós állapottal, tervezett és elhasznált kerettel, a felhasználó teendőivel és visszanézéssel mutatja; a sávonkénti keretfogyás mérése a session-átiratokból (`eszkozok/keret_meres.py`); az ötlettár első feltöltése a szétszórt felvetésekből
kovetkezo: "lezárva: a PR #740 mergelve (2026-11-15, az orkesztrátor lezárása; a gépi lezárás kihagyta, mert a `kovetkezo` nem nevezte meg a merge-et)"
munka: folyamat
olvas: [CLAUDE.md, adat/SEMA.md, eszkozok/heti_attekinto.py, eszkozok/feladatok.py]
ir: [adat/heti_terv.tsv, adat/heti_keret.tsv, adat/otlettar.tsv, adat/keret_sulyok.tsv, adat/keret_munkamappa.tsv, adat/heti_keret_meres.tsv, adat/SEMA.md, eszkozok/heti_beosztas.py, eszkozok/keret_meres.py, eszkozok/tesztek/test_heti_beosztas.py, eszkozok/tesztek/test_keret_meres.py, eszkozok/teszt_feladatok.py, eszkozok/feladatok.py, eszkozok/brief_lezaras.py, eszkozok/heti_attekinto.py, BRIEF_SABLON.md, F222_HETI_BEOSZTAS_BRIEF.md]
fugg: []
nem_fugg: [123, 188, 201]
---

# F222_HETI_BEOSZTAS_BRIEF.md — Heti beosztás, felmérés munkatípus, ötlettár

*FELADATOK #222 · Modell: sonnet · 2026.11.15 · forrás: az orkesztrátor megbízása és a felhasználó jóváhagyása (2026-11-15: „Igen, így”). Előzmény: a heti áttekintő (F220) nyitott-lista lett; a felhasználó: „nem ez lett volna egy heti beosztás… ugyanaz mint a feladatleltár”.*

## 1. Cél

A heti beosztás **terv**, nem leltár: sávonként a hét sorai (sorrend, cél a hét végére, modell, becsült keret), mellettük a **valós állapot** (a brief fejlécéből és a PR-ból), a tervezett és az elhasznált keret, a felhasználó teendői, a végén a lezárt hét **visszanézése**. A kutatás és az ötletelés nem külön sáv, hanem munkatípus („felmérés”), saját kerettel; hozzá ötlettár tartozik.

## 2. Hatókör

**Benne van**
- `adat/heti_terv.tsv`, `adat/heti_keret.tsv`, `adat/otlettar.tsv` és a SEMA új szakaszai (2.60–2.62);
- `eszkozok/heti_beosztas.py` (új szkript; a heti áttekintőt, `heti_attekinto.py`, importálja és nem módosítja) és tesztje;
- a sávonkénti keretfogyás mérése (`eszkozok/keret_meres.py`, a megbízás bővítése, a felhasználó jóváhagyásával, 2026-11-15): a session-átiratokból, súlyozva, sávhoz rendelve, kalibrálva; tölti az oldal „elhasznált” oszlopát (`--meres`); SEMA 2.63–2.65;
- a mostani hét (`2026-11-14`) terve `jovahagyva=javaslat` jelzéssel; az ötlettár első feltöltése forrással, döntés nélkül;
- B rész: a `felmeres` `tipus` (a #736 mergelve, 2026-11-15): `feladatok.py` (típus, `sav` kötelező, kódot nem ír), `brief_lezaras.py` (lezárható), `BRIEF_SABLON.md`, a heti áttekintő típus-szűrői; a FELADATOK.md generált blokkja még nem listázza külön (külön döntés).

**Nincs benne**
- a brief-fejlécek és a `NYITOTT_FELADATOK.md` módosítása (másik session zárja a briefeket);
- az alkalmazásban látott százalék gépi lekérése (a kalibrációs pontokat az orkesztrátor tölti a `heti_keret_meres.tsv`-be);
- az ötlettár tételeiből döntés vagy brief.

## 3. Lépések

1. SEMA-szakaszok és három tábla.
2. Az oldal-generátor és a tesztek; a próba-HTML a repón kívülre.
3. Az ötlettár és a mostani hét feltöltése.
4. B rész (feltételesen).
5. Commit, push, draft PR; a CI egyszeri olvasása.

## 4. Elfogadási feltételek

- `python eszkozok/feladatok.py ellenoriz`: 0 hiba; a tesztek zöldek;
- lezárt tétel a heti tervben **csak a visszanézésben** áll;
- a próba-HTML a mai állapotból elkészül.

## 5. Döntésnapló

Új szkript és nem a `heti_attekinto.py` átalakítása: a két nézet adatforrása más (az F220 a brief-fejlécekből leltároz, ez a `heti_terv.tsv`-ből tervez és ahhoz méri a valós állapotot); az F220 tesztjei és a merge-elt kimenete érintetlen marad. A régi nézet kivezetése külön döntés.
