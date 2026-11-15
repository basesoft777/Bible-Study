---
feladat: 221
cim: Két védőszabály a szabályhelyekre (hatókör-szűkítés, felhasználó által talált hiba)
kod: VEDOSZABALYOK
tipus: feladat
fazis: folyamat
sav: SYSTEMS
modell: sonnet
allapot: fut
ad: a hatókör-szűkítés szabálya (kimondni, mi marad ellenőrzés nélkül és mi méri helyette) és a „felhasználó által talált hiba = hibanapló-tétel” szabály a repó szabályhelyein; a hibanapló három új mechanizmussal (M-RÁRAKÓDÁS, M-GAZDÁTLAN, M-VAKFOLT)
kovetkezo: "Te: a PR átnézése és merge; a BRIEF_SABLON.md szabályszövege a `sav` mezős PR (local_b39fa535) mergelése után kerül be (kész diff: naplok/F221_jelentes.md)"
munka: folyamat
olvas: [naplok/HIBA_MECHANIZMUSOK.md, .claude/commands/befogad.md, .claude/commands/lap-javit.md, .claude/commands/kiadas.md]
ir: [naplok/HIBA_MECHANIZMUSOK.md, .claude/commands/befogad.md, .claude/commands/lap-javit.md, .claude/commands/kiadas.md, naplok/F221_jelentes.md]
fugg: []
nem_fugg: [111, 165, 188, 201, 216, 217, 218]
---

# F221_VEDOSZABALYOK_BRIEF.md — Két védőszabály a szabályhelyekre

*FELADATOK #221 · Modell: sonnet · v1 · 2026.11.15 · forrás: a felhasználó jóváhagyása (2026-11-15, „Igen, kerüljön be”), az orkesztrátor gyökérok-jelentése a lapgenerátor késői felismeréséről*

## 1. Cél

Két védőszabály kerül a szabályhelyekre, egy szabály egy helyen (F184).

1. **Hatókör-szűkítés.** Ha egy brief vagy döntés egy ellenőrzés hatókörét szűkíti, kimondandó (a) mi marad ellenőrzés nélkül, (b) mi méri helyette; ha (b)-re nincs válasz, ⛔, a felhasználó dönt. Szövegének helye a `BRIEF_SABLON.md`; a `/befogad` csak hivatkozik rá és ellenőrző pontot ad.
2. **Felhasználó által talált hiba = hibanapló-tétel.** A `/lap-javit` és a `/kiadas` javítókörében kötelező lépés; a szabály szövege a hibanapló fejlécében áll.

## 2. Hatókör

Benne: a három parancsfájl, a hibanapló, a jelentés. Nincs benne: `NYITOTT_FELADATOK.md`, brief-fejlécek, a `BRIEF_SABLON.md` addig, amíg a `sav` mezős PR nincs a main-en.

## 3. Lépések

1. A hibanapló fejléce és három új mechanizmus. 2. A `/befogad` 2. lépés ellenőrző pontja. 3. A `/lap-javit` és a `/kiadas` kötelező lépése. 4. A `BRIEF_SABLON.md` szabályszövege a feltétel teljesülése után (⛔ addig a jelentésben kész diffként).

## 4. Elfogadási feltételek

`python eszkozok/feladatok.py ellenoriz` 0 hiba; a hivatkozás-ellenőrzés (E27) zöld.

## 5. Döntésnapló

DT852 (`dontesek/uj/youthful-pare-e6946f.md`).
