---
feladat: 190
cim: Mitől kész egy lexikonlap — a lezárt követelménylista a HAMART-001 mércéjével
kod: KESZ_LAP_KOVETELMENY
tipus: feladat
fazis: folyamat
modell: opus
allapot: dontesre_var
ag: claude/kesz-lap-kovetelmeny-15a3b5
pr: 683
ad: egy helyen, blokkonként áll, mitől kész egy lexikonlap; a HAMART-001 mért állapota soronként; a hiányok, az ellentmondások és a gépesíthető emberi ellenőrzések listája
kovetkezo: "Te: a lista elfogadása és a (b) tételek döntése (DT-F190a), utána a draft PR merge-e"
munka: folyamat
olvas: [sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, MUNKAMENET.md, DONTESEK.md, adat/SEMA.md]
ir: [sablonok/KESZ_LAP_KOVETELMENY.md, dontesek/uj/kesz-lap-kovetelmeny-15a3b5.md, F190_KESZ_LAP_KOVETELMENY_BRIEF.md]
fugg: []
---

# F190_KESZ_LAP_KOVETELMENY_BRIEF.md — Mitől kész egy lexikonlap

*FELADATOK #190 · Modell: opus · v1 · 2026.11.11*

*Az orkesztrátor indította, külön sessionben. A felhasználó jóváhagyása (2026-11-11): „igen. mert a hamartból akarjuk megírni a követelményt”. A brief a szabályos úthoz készült, ugyanezen az ágon; befogadás nélkül, mert a feladatot a felhasználó közvetlenül hagyta jóvá (a #189 mintájára).*

## 1. Cél

A lap követelményei ma négy helyen állnak: a lapsablonban, a döntésekben, a felhasználó memóriájában és a HAMART-leletekben (F1–F35). Ezért minden átnézéskor előkerül egy „még hiányzik”, és ez újabb kört nyit. A cél egy lezárt lista: ami rajta van, az a kész lap feltétele, ami nincs, az nem feltétele az 1. kiadásnak. A lista a lektor és a szerkesztő átnézésének bemenete, és a „Kiadható-e az 1. kiadás?” kérdés mércéje.

## 2. Hatókör

- Új fájl: `sablonok/KESZ_LAP_KOVETELMENY.md`, blokkonként a lap sorrendjében. Soronként: blokk, követelmény (egy mondat), forrás, ellenőrzés, HAMART-állapot. A végén három lista: (a) a HAMART hiányai, (b) az ellentmondó vagy elavult követelmények döntési javaslattal, (c) a gépesíthető emberi ellenőrzések.
- A mérce a HAMART-001 lapja a `claude/hamart-javito` ágon (a #182 2. fázisa), a legfrissebb lapváltozatán.
- **Nem része:** a lap, a generátor és az `adat/` módosítása; új kapu; új követelmény kitalálása (a HAMART-on látott, sehol le nem írt jó gyakorlat a (b) listába kerül „javasolt felvétel” jelöléssel).

## 3. Lépések

1. Modell-ellenőrzés (CLAUDE.md).
2. A források célzott olvasása; a `DONTESEK.md`-ből csak a lapra vonatkozó, érvényes döntések (az elavult jelölve).
3. A HAMART-lap mérése a legfrissebb commiton, ideiglenes, leválasztott munkafán (`olvasoi_kapu.py`, `proza_1a.py`, `ellenoriz.py`, `muhely_allapot.py`), és a lap célzott olvasása.
4. A lista megírása; a (b) döntésre váró tételei helyőrzős döntésként (DT-F190a).
5. Draft PR. ⛔ A lista elfogadása és a merge a felhasználóé.

## 4. Elfogadási feltételek

- A fájl blokkonként, a lap sorrendjében áll; minden sor öt oszlopa ki van töltve.
- Minden követelménynek van forrása; új követelmény nincs.
- A HAMART-állapot mért vagy kimondottan „nem eldönthető”, helyhivatkozással.
- A lap, a generátor és az `adat/` nem változott.
- A jelentés első sora: a követelmények száma, a HAMART-hiányok száma és az ellentmondások száma.

## 5. Döntésnapló

- **DT-F190a** 🟡 — a lista elfogadása és a (b) tételek döntése (`dontesek/uj/kesz-lap-kovetelmeny-15a3b5.md`).

## 6. Jelentés

**109 követelmény · 27 HAMART-hiány · 18 ellentmondó vagy elavult követelmény** (+ 4 javasolt felvétel, 16 gépesíthető emberi ellenőrzés).

- A 109 sor állapota: 52 teljesül, 29 hiányzik, 16 részben, 6 nem eldönthető, 6 hátralévő lépés. A 27 pótlandó tétel (az (a) lista) a 29 hiányzó és a 16 részben teljesülő sorból áll össze.
- Kiegészítés (F190.5, az orkesztrátor továbbításával): a felhasználó döntése (2026-11-11): „a visszhang 1-2 kötelező”. A K67 forrása ez, állapota „hiányzik (#183 folyamatban)”. A visszhang 2 hat sora (K67a–K67f) az `F183_VISSZHANG_USZ_TANU_BRIEF.md` V1–V3 pontjából és a `visszhang-reteg-terv` memóriából jön, „a briefből, a #183 után a HAMART szerint véglegesítendő” jelöléssel. Új (a)-tétel: A27.
- **Hátralévő:** a #183 után egy frissítés a K67a–K67f sorokat a tényleges HAMART visszhang 2 szerint pontosítja; a lista ezzel zárul le, a lektor előtt.

- A mérés alapja: a lap `4f51e371` (F182.21), az ág feje `9e74455e`. Olvasói kapu: 0 BUKÁS, 19 FIGYELMEZTETÉS; 1/a: 47/47; `ellenoriz.py`: a 36–40. szabály a HAMART-ra tiszta.
- A legsúlyosabb lelet: **hamis állítás** a lapon. Az Alátámasztás „A motívumhoz nincs rögzített kapcsolat.” mondatot hoz az 56 kapcsolatsor alatt (A01, K77). Ez a leletlistában nem szerepelt.
- Az F1–F35 leletekből a lapon még nem látszik: F1, F3, F4, F5, F6, F7, F8, F11, F12, F13, F14, F15, F17, F18, F35 (a #182 2. fázisa még fut).
- Egyeztetett eltérés: a feladat a lapot a `claude/bold-joliot-1d4089` ágon nevezte meg. A `bold-joliot-1d4089` munkafa valójában a `claude/hamart-javito` ágon áll; a mérés ezen az ágon készült.
