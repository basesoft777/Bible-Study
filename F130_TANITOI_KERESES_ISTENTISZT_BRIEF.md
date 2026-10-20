---
feladat: 130
cim: Nevesített tanítói keresés az ISTENTISZT-001-re — a 7. lépés első valódi menete, a #127 előtt
kod: TANITOI_KERESES_ISTENTISZT
tipus: feladat
fazis: 1
munka: ertelmezo
modell: opus
allapot: nem_indult
ad: a motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md a 7. sablon szerinti, webes forrásokkal (mű, pontos hely, URL) igazolt eredményt hordozza a manual szétválasztás helyett; a régi változat archiválva; a #127 tanítói rése erre épülhet
kovetkezo: "Te: /kovetkezo; első lépés M0 (modell-ellenőrzés, előfeltételek), ⛔ az M4-nél (az eredmény és a régi manual változat összevetése, a forrás 5. pontjának esetleges szövegjavaslata)"
olvas: [motivumok/ISTENTISZT-001.md, "tematikus_lezart/ISTENTISZT-001*", "tematikus_lezart/naplok/ISTENTISZT-001*", motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md, archivum/ISTENTISZT-001/, sablonok/7_PaRDeS_tanitoi_kereses_sablon.md, sablonok/4_PaRDeS_tematikus_sablon.md, sablonok/PaRDeS_tanitok_lista.md, .claude/agents/tanito-kereso.md, adat/motivumok.tsv, naplok/F11_szetvalasztas_ISTENTISZT-001.tsv]
ir: [motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md, motivumok/ISTENTISZT-001.md, archivum/ISTENTISZT-001/ISTENTISZT-001_tanitoi_kereses_manual.md]
fugg: []
nem_fugg: [123, 127]
---

# F130_TANITOI_KERESES_ISTENTISZT_BRIEF.md — Nevesített tanítói keresés az ISTENTISZT-001-re

*FELADATOK #130 · Modell: opus (értelmező modell, DT-F32b; a keresést a `tanito-kereso` subagent végzi, saját modelljével) · v1 · 2026.10.20*

## 1. Cél

Az ISTENTISZT-001 („Segítségül hívni az Úr nevét”) tanítói rétege ma a régi tematikus tanulmányból
szétválasztással átvett szöveg (DT249 b): a `motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md`
fejlécében a `Dátum` és a `Modell` `manual`, nincs 1. Kiinduló motívum-kivonat, és a tanítói
forrásokhoz (Kenneth Hagin ✅, Derek Prince ⚠️) nincs forrás-URL. A DT249 indoklása kimondja, hogy
„az (a) új webes menete később is lefuthat, és a fájlt felülírja”. Ez a feladat ez a menet: a 7. lépés
(B9) a `sablonok/7_PaRDeS_tanitoi_kereses_sablon.md` szerint, a `sablonok/4_PaRDeS_tematikus_sablon.md`
„Nevesített tanítói egyezés-keresés módszere” öt lépésével és „Forrás-megbízhatóság jelölése”
szabályával, a jóváhagyott listából (`sablonok/PaRDeS_tanitok_lista.md`).

A sorrend a felhasználó döntése (DT-F130a): **előbb ez a feladat, utána a #127**, hogy a #127
`tanitoi` rése (DT-F127a) az igazolt eredményre épüljön, és a rés-jelölőket az új fájlba tegye.

## 2. Hatókör

**Benne van:**
- a tanítói fájl újraírása a 7. sablon négy pontja szerint (Fejléc tényleges dátummal és modellel;
  1. Kiinduló motívum-kivonat; 2. Névsor indoklással; 3. Keresések tanítónként; 4. Összegzés);
- a régi, manual változat archiválása (`archivum/ISTENTISZT-001/ISTENTISZT-001_tanitoi_kereses_manual.md`,
  `ARCHÍV` fejléccel, bájtra azonos törzzsel), nem törlés;
- a `motivumok/ISTENTISZT-001.md` 5. pontjának (az alkalmazási kérdések tanítói utalása, ma a
  376. sor körül: „Hagin ✅ erős/közvetlen, Derek Prince ⚠️ részleges/beágyazott”) szövegjavaslata,
  **csak ha** az eredmény ettől eltér; a javítás a ⛔ M4 jóváhagyása után.

**Nincs benne:**
- a lexikonlap (`lexikon/ISTENTISZT-001_TUDOMANYOS.md`) és a rés-jelölők: azok a #127 dolgai
  (a #127 `ir` listája tartalmazza a tanítói fájlt); ez a feladat rés-jelölőt nem tesz a fájlba;
- más motívum tanítói keresése; a jóváhagyott lista bővítése; akadémiai (research-sablonos) források;
- az alkalmazási kérdések (5. pont) átírása az M4-ben jóváhagyott tanítói utaláson túl.

## 3. Lépések (⛔ a kötelező megállások)

### M0 — előfeltételek
1. Modell-ellenőrzés (CLAUDE.md): a session `opus`; a `tanito-kereso` subagent a saját fájlja
   `model` mezőjéhez mér.
2. A #127 nem fut és nincs nyitott ága, amely a tanítói fájlt írja (`git branch -a`, a #127 briefjének
   `allapot` mezője); ha fut: megállás, jelentés.
3. Olvasás: a motívum forrása teljesen (`motivumok/ISTENTISZT-001.md`), a régi tematikus tanulmány és
   kereszthivatkozás-napló (`archivum/ISTENTISZT-001/`), a mostani tanítói fájl, a 7. és a 4. sablon
   hivatkozott szakaszai, a tanítói lista.
4. Commit: `F130.0:` (a brief fejléce `allapot: fut`, `ag`).

### M1 — a régi változat archiválása
A mostani fájl bájtra azonos másolata az `archivum/ISTENTISZT-001/ISTENTISZT-001_tanitoi_kereses_manual.md`-be,
a fájl elején `ARCHÍV` jelöléssel (mi ez, mikor és miért került ide: F130, DT249 a), a törzs változatlan.
Commit: `F130.1:`.

### M2 — 1. Kiinduló motívum-kivonat (a session írja, nem a subagent)
A tanulmány saját Peshat/Remez/Drash/Sod megállapításaiból, **kizárólag a forrás szövegéből**, webes
keresés nélkül: a teológiailag súlyos csomópontok, amelyekhez tanítói egyezés kereshető (a 4. sablon
öt lépésének 1. lépése). Minden csomópont mellett a forrásbeli helye (szakasz, igehely). Ez értelmező
próza: egy kézben, a teljes forrás olvasása után (KONTEXTUS K1).

### M3 — keresés (`tanito-kereso` subagent)
A subagent bemenete: a motívum-ID, a study-fájl és az M2 kivonata. A 7. sablon 2–4. pontja szerint:
- 2. Névsor a jóváhagyott listából, a választás indoklásával (a régi eredmény két tanítója, Kenneth
  Hagin és Derek Prince, a listán van; a választás nem kötelezően rájuk szűkül, de a kihagyásuk is
  indoklandó);
- 3. tanítónként célzott keresés (tanító neve + a konkrét vers vagy téma, nem általános tematikus
  egyezés); minden találatnál a mű, a pontos hely és a **forrás-URL**; erősség ✅ / ⚠️ / gap; saját
  szavas összefoglalás, szó szerinti idézet legfeljebb egy rövid mondat;
- 4. Összegzés tanítónként; **az üres eredmény elfogadott kimenet**, explicit jelölve.
A subagent csak a tanítói fájlt írja, a fő szálnak legfeljebb 10 soros összegzést ad.

### M4 — forrás-ellenőrzés és összevetés (⛔)
1. A session minden ✅ és ⚠️ találat forrását maga is megnyitja (WebFetch), és ellenőrzi, hogy az
   ténylegesen az adott igehelyre vagy témára hivatkozik (a 4. sablon 4. lépése); puszta asszociatív
   vagy tematikus rokonság törlendő vagy gap-re minősítendő. Az ellenőrzés eredménye a naplóba
   (`naplok/F130_TANITOI_KERESES_ISTENTISZT_naplo.md`), találatonként: URL, lekérés ideje, ítélet.
2. Összevetés a régi manual változattal: mely tanító és erősség maradt, változott, tűnt el vagy jött
   új; ha a `motivumok/ISTENTISZT-001.md` 5. pontjának tanítói utalása eltér, szövegjavaslat.
3. **⛔ Megállás:** a felhasználó jóváhagyja az eredményt és a szövegjavaslatot (vagy azt, hogy nincs
   javítandó). Commit az M3–M4 állapotról: `F130.2:`; a jóváhagyott forrásjavítás: `F130.3:`.

### Mz — zárás
`fuggetlen-ellenor` a base..head diffen (a 7. sablon pontjai, a forrás-URL-ek elérhetősége mintán,
proveniencia, archiválás bájtra), zárónapló, draft PR. Push és merge csak a felhasználótól.

## 4. Elfogadási feltételek

1. A tanítói fájl a 7. sablon mind a négy pontját tartalmazza; a Fejléc `Dátum` és `Modell` mezője a
   tényleges érték (a modell a saját környezetből, nem a briefből másolva).
2. Minden ✅ és ⚠️ találatnál: mű, pontos hely, forrás-URL, lekérési dátum; a session ellenőrizte (M4).
3. A gap explicit; gyenge vagy asszociatív anyag nincs (CLAUDE.md 3. szabály).
4. A régi manual változat az archívumban bájtra azonos törzzsel, `ARCHÍV` fejléccel.
5. A tanítói fájlban nincs rés-jelölő (az a #127 dolga); a lexikonlap nem változott.
6. A `motivumok/ISTENTISZT-001.md` csak a jóváhagyott tanítói utalásban változott (vagy sehol).
7. `python eszkozok/ellenoriz.py` SÉRTÉS 0.

## 5. Döntésnapló

| Azonosító | Kérdés | Opciók | Javaslat / döntés |
|---|---|---|---|
| DT-F130a | A tanítói keresés és a #127 sorrendje (mindkettő írja a `motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md`-t; a #127 rés-jelölőt tesz bele) | 1. előbb a #130, utána a #127 (a rés az igazolt eredményre épül) · 2. előbb a #127, utána a #130 (a #130 megőrzi a rés-jelölőket, utána újragenerálás) | **Felhasználó, 2026-10-20 (chat): 1.** Alkalmazás a befogadáskor: a #127 fejlécében `fugg: [126, 130]`. |
| DT-F130b | A régi, manual tanítói fájl sorsa | 1. archiválás (`archivum/ISTENTISZT-001/`, `ARCHÍV` fejléc) · 2. felülírás, a történet a gitben | 1. (a migrációs gyakorlat: régi fájl nem törlődik, archívumba kerül) |
