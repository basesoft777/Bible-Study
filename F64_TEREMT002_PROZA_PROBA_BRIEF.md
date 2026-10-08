---
feladat: 64
cim: TEREMT-002 próza-próba (#12a) — a teljes értelmező réteg egy kézben, éles render nélkül
kod: TEREMT002_PROZA_PROBA
tipus: feladat
fazis: 1
modell: opus
munka: ertelmezo
allapot: lezarva
ag: claude/f64-teremt002-proza-proba
ad: a TEREMT-002 teljes értelmező rétege (a motívumcikk prózája a tematikus sablon szerkezetével) a motivumok/TEREMT-002.md forrásban, a próbarender csak a generalt_proba/ alatt, az LXX-helyek „függő” jelöléssel; egy mérési jelentés az ISTENTISZT-001 mércéje szerint, amely a #23 M1 bemenete (DT-F32a, KONTEXTUS K1/4)
kovetkezo: lezárva
pr: PR_HELYORZO
lezarva_osszegzes: "próza a motivumok/TEREMT-002.md-ben, mérés és 4 ellenőri kör (eltérés nélkül); a #23 M1 bemenete; a szerepmátrix-rész nem mért (az ISTENTISZT-001 aranyminta hiányos); naplok/TEREMT002_PROZA_PROBA_zaras.md"
olvas: [motivumok/TEREMT-002.md, "tematikus_lezart/TEREMT-002*", "tematikus_lezart/naplok/TEREMT-002*", motivumlog/PaRDeS_motivumok.md, TEREMT002_KUTATAS_BRIEF.md, naplok/T1_TEREMT002_gate.md, naplok/T1_TEREMT002_scan.md, naplok/T1_TEREMT002_jeloltek_munkalap.tsv, naplok/T1_TEREMT002_masodrendu_talalatok.tsv, naplok/T2_TEREMT002_minosites.tsv, naplok/T2_TEREMT002_kapcsolatok_javaslat.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/kapcsolatok.tsv, adat/auditok.tsv, adat/motivumok.tsv, adat/res_forras.tsv, adat/SEMA.md, sablonok/4_PaRDeS_tematikus_sablon.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/PaRDeS_gyorsreferencia.md, F23_MOTIVUM_FORRAS_BRIEF.md, naplok/MOTIVUM_FORRAS_lekepezes.tsv, naplok/KONTEXTUS_szabalyok.md, MUNKAMENET.md, eszkozok/general.py, lexikon/ISTENTISZT-001_TUDOMANYOS.md]
ir: [motivumok/TEREMT-002.md, generalt_proba/TEREMT-002_proza_proba/]
fugg: []
nem_fugg: [55, 63, 65]
---

# F64_TEREMT002_PROZA_PROBA_BRIEF.md — TEREMT-002 próza-próba (#12a)

*FELADATOK #64 · Modell: opus · v1 · 2026.10.05 · döntések: DT-F32a (a #12 kettéválik; ez a #12a), DT-F32b (értelmező modell), DT-F26b (a #12 sora változatlan; a pilot-szándékot a #12a teljesíti), D34, D38*

## 1. Cél

A KONTEXTUS K1/4 szabálya szerint a B-szerkezet forrássablonja (#23 M1) csak akkor véglegesíthető, ha (a) egy motívum teljes értelmező rétege a KONTEXTUS-szabályok szerint elkészült, és (b) az eredmény hozza az ISTENTISZT-001 mércéjét. A DT-F32a szerint ez a próba a #12 első fele: a **#12a próza-próba**, a #23 M0 után és az M1 előtt, egy Opus-briefben, a jelenlegi eszközökkel, éles render nélkül.

A TEREMT-002 az egyetlen natív egyforrású motívum: a kutatás és a minősítés (T1–T2, `TEREMT002_KUTATAS_BRIEF.md`) lefutott, az adat bent van, próza még nincs. A forrásréteg (`motivumok/TEREMT-002.md`) ma a napló átemelt blokkjait hordozza.

A #12b (élesítés: lexikonoldal, LXX-döntések) a #5, #8 és #11 után marad, és ennek a feladatnak a prózáját használja.

## 2. Hatókör

**Benne van:**
- a TEREMT-002 motívumcikkének teljes prózája (PaRDeS-értelmezés, a tematikus sablon szakaszsorrendjével), összefüggő érvelésként, markerekkel (K1/2: próza-elsőbbség, nem adatséma prózamezőkkel);
- a próza a már betöltött adatra épül (`elofordulasok`, `jeloltek`, `kapcsolatok`, `auditok`); minden lekérdezésből származó állítás mellett a proveniencia-sor (CLAUDE.md 1. szabály);
- a jelenlegi `general.py`-vel előállítható próbarender a `generalt_proba/TEREMT-002_proza_proba/` alá (a `--kimenet` próbák szabálya szerint);
- az LXX-helyek „függő” jelöléssel;
- mérési jelentés: az eredmény a mérce szerint, és amit a #23 M1-nek tudnia kell (melyik sablonszakasz működött kézi prózaként, melyik adatból, mi hiányzott).

**Nincs benne:**
- éles lexikonoldal, `lexikon/TEREMT-002_*` fájl, törzscikk (D1, D34; a #12b dolga);
- `adat/lxx_dontesek.tsv`-sor (a #12b dolga), `adat/res_forras.tsv`-sor;
- adattábla írása: új előfordulás, jelölt vagy kapcsolat nem kerül be (ha a próza írása közben hiány derül ki, jelentésbe kerül; CLAUDE.md 2. és 3. szabály);
- a 7. lépés (nevesített tanító; önálló menet);
- a forrássablon (`sablonok/9_…`) megírása (a #23 M1 dolga);
- a szakaszok felosztása több modell vagy subagent között (K1/1).

## 3. Lépések

### M0 — Bemenetek és ⛔

Jelentés: `naplok/TEREMT002_PROZA_PROBA_M0.md`.
1. **A #23 M0 kimenete:** a `naplok/MOTIVUM_FORRAS_lekepezes.tsv` megvan-e, és mit mond a tematikus sablon szakaszairól (`kezi_forras` / `adat` / `generalt`, `szint`, `aktivalas`). Ha a #23 M0 még nem futott vagy nincs jóváhagyva: ⛔, a feladat nem indul.
2. **A próza helye:** a D34 szerint a motívumcikk (a volt tematikus tanulmány) generált nézet, a kézi forrás a `motivumok/[ID].md`. *Javaslat:* a próza a `motivumok/TEREMT-002.md`-be kerül, a tematikus sablon szakaszsorrendjével; külön `tematikus_lezart/` fájl nem készül. *Alternatíva:* külön tanulmányfájl (a DT-F32a „a tematikus tanulmány prózája” szövegének szó szerinti olvasata), amely a második kézi forrás lenne.
3. **A mérce:** az „ISTENTISZT-001 mércéje (L1–L5, a #10 szerint)”. A repóban a lexikonoldal-sablon „Minőségi kapu” szakasza hordozza (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`, L1, L3, L4, L5, L6; L2 nincs benne, az F10 csonkja viszont L1–L7-et ír). A kapu a lexikonoldalra szól; az M0 leírja, melyik pont alkalmazható a forrásban álló prózára és a próbarenderre, és melyik nem (pl. az L1 szakaszlistája a TUDOMÁNYOS oldalra vonatkozik). A ⛔-nál a felhasználó megerősíti, hogy ez a DT-F32a szerinti mérce, és dönt az L2/L7 résről.
4. **A jelenlegi generátor képessége:** mit tud a `general.py` a `motivumok/TEREMT-002.md`-ből a `generalt_proba/` alá renderelni (rés-blokkok, napló, index); ami nem renderelhető, az a mérési jelentésben „nem renderelt” jelölést kap, a generátor nem módosul.
5. **Az adat-alap:** a TEREMT-002 előfordulásai, jelöltjei, kapcsolatai és auditjai számokkal; a T1–T2 naplók nyitott pontjai.

**⛔ Megállás:** a felhasználó dönt a próza helyéről (2.), és megerősíti a mércét (3.).

### M1 — Próza

- Egy kézben, egy modellel (`opus`, K1); ha a kontextus nem fér el, a folytató session ugyanezt a briefet viszi tovább, és a teljes forrást újraolvassa (K1/3).
- A tematikus sablon (`sablonok/4_PaRDeS_tematikus_sablon.md`) és a gyorsreferencia szabályai; a ⭐ küszöb alatti szakaszok inaktívak (D37).
- Szintjelölés a #23 M0 javaslata szerint, ha van (`olvasoi` / `apparatus` / `belso`); `【NAPLO】` csak `belso`.
- Az LXX-helyek: „függő (#12b)” jelölés, LXX-állítás csak a meglévő `lxx-hid` lekérdezés proveniencia-sorával.
- Commit tételenként: `F64.<n>: …`.

### M2 — Próbarender

- A `general.py` meglévő céljaival, a `generalt_proba/TEREMT-002_proza_proba/` alá (a `generalt_proba/` verziózott; meglévő fájl nem törölhető). Éles kimenet nem változik: a `general.py --ellenoriz` fixpontja a meglévő fájlokon zöld marad.

### M3 — Mérés és ⛔

Jelentés: `naplok/TEREMT002_PROZA_PROBA_meres.md`.
- A mérce pontjai egyenként: teljesül / részben / nem, indoklással.
- A #23 M1-nek: szakaszonként, mi működött kézi prózaként, mi adatból, mi hiányzott a sablonból; a K1/2 próza-elsőbbség tapasztalata (hol kellett mezőhatár, hol nem).
- A #12b-nek: a „függő” LXX-helyek listája, a lexikonoldalhoz szükséges, de hiányzó elemek.

**⛔ Megállás:** a felhasználó átnézi a prózát és a mérést; a K1/4 (b) teljesülését ő mondja ki. Ezután indulhat a #23 M1.

### M4 — Zárás

`naplok/TEREMT002_PROZA_PROBA_zaras.md` (≤20 sor), `fuggetlen-ellenor` (`naplok/ELLENOR_TEREMT002_PROZA_PROBA.md`: proveniencia-sorok, nincs adattábla- és éles kimenet-változás, nincs gyenge kitöltés), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** A próza egy kézben, egy modellel készült; a `motivumok/TEREMT-002.md` összefüggő érvelés markerekkel.
- **K2.** Minden lekérdezésből származó állítás mellett proveniencia-sor; a hiány explicit jelölt, nem gyenge anyaggal kitöltött (CLAUDE.md 1. és 3. szabály).
- **K3.** Adattábla, `lexikon/`, `tematikus_lezart/` (ha az M0 az 1. javaslatot fogadta el) és minden éles generált fájl változatlan; a próbarender csak a `generalt_proba/TEREMT-002_proza_proba/` alatt.
- **K4.** Az LXX-helyek „függő” jelölést kaptak; `lxx_dontesek.tsv` változatlan.
- **K5.** A mérési jelentés a mérce minden pontjára ítéletet ad, és tartalmazza a #23 M1 bemenetét.
- **K6.** Az `ellenoriz.py`, a `feladatok.py ellenoriz` és a CI zöld; a független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | A #12a önálló számot kap (#64); a #12 (most #12b) csonkja és sora változatlan. | DT-F32a, DT-F26b, befogadás |
| v1 | 2026-10-05 | A #23 M0-tól való függés számmal nem rögzíthető (a #23 egy része), ezért a `kovetkezo` mező és az M0 1. pontja hordozza. | befogadás (az F23 v1.2 mintája) |
| v1 | 2026-10-05 | A mérce a `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` Minőségi kapuja (L1, L3–L6); az L2/L7 rés és az alkalmazhatóság a prózára az M0 ⛔ pontján dől el. | befogadás (független átnézés javítása) |
| v1.1 | 2026-10-08 | Az L2/L7 rés kitöltve: L2 = „Napló-jelölés kötelező” (`4c4003b`), L7 = PaRDeS-rétegfegyelem (`f51851d`, az L6 (g) pontja); a #64 mércéje L1–L7 + a DT2 két rés-szabálya. | DT-F64a (2), felhasználó (chat) |
| v1.1 | 2026-10-08 | A próza helye a `motivumok/TEREMT-002.md` (DT-F64a (1)); az LXX-állítás friss `lxx-hid` futás proveniencia-sorával, audit-sor nélkül (DT-F64b). Az M0 ⛔ feloldva. | DT-F64a (1), DT-F64b, felhasználó (chat) |
