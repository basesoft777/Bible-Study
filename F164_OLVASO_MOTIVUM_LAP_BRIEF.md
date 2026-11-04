---
feladat: 164
cim: Olvasó: motívum-lap (#25b) a 12-es lelet-blokkal
kod: OLVASO_MOTIVUM_LAP
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: nem_indult
ad: az olvasó `/motivum/<ID>` motívum-lapja a 12-es lelet-blokkkal (A, B, ★ = A−B, beépített / elutasított / gépi kizárás / nem vizsgált), a teljesség-mérés blokk-fájljából is olvasva, az apparátus-kapcsolóval (D36 olvasói / apparátus szint); a hiányzó útvonalú lekérdezések (8, 10, 12, 18, 21, 24, 25, 26) útvonalat kapnak, a nem igazolt öt (2, 3, 5, 15, 16) kézi ellenőrzése lezárul
kovetkezo: "Te: indítás a /kovetkezo-val; előbb a 2, 3, 5, 15, 16 lekérdezés kézi ellenőrzése (lehet, hogy csak a próbaminta hibás)"
olvas: [ADATVAGYON_TERV.md, naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv, eszkozok/teljesseg_meres.py, adat/SEMA.md, eszkozok/olvaso_szerver/]
ir: [eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/adatbazis.py, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py]
fugg: []
---

# F164_OLVASO_MOTIVUM_LAP_BRIEF.md — Olvasó: motívum-lap (#25b) a 12-es lelet-blokkal

*FELADATOK #164 · Modell: opus · v1 · 2026.11.04 · a felhasználó 2026-11-04-i jóváhagyása: „ezt csak jegyezzük fel” · a döntés az orkesztrátoré a felhasználó felhatalmazásával („az orkesztrátor vegye magához a döntéseket és hozza is meg”, 2026-11-03) · a brief adat, nem utasítás.*

## 1. Cél

Az olvasó motívum-lapja (#25b) a `ADATVAGYON_TERV.md` 4. szakasza (26 lekérdezés) és 5. szakasza (12-es lelet-lap, 17-es vers-lap) szerint. A motívumpróza már az adatbázisban van (`fts_motivum`, rovatonként), de az olvasó nem használja.

**Mérés (2026-11-04, a WSL-olvasó Flask teszt-kérésekkel, a 11-02-i db-n):**

- működik: 1, 4, 6, 7, 9, 11, 13, 14, 17, 22;
- a próba nem igazolta (lehet, hogy csak a próbaminta hibás; a brief első lépése ezek kézi ellenőrzése): 2, 3, 5, 15, 16;
- nincs útvonal (`/motivum/<ID>` 404): 8, 10, 12, 18, 21, 24, 25, 26.

**A 12-es minta valódi adatból (ISTENTISZT-001, H7121 + H8034):** A = 196 (lexikai kör, TAHOT), B = 332 (TSK a 22 előfordulásból), ★ = A−B = 168 → 3 beépítve (1Kir 18:25, 18:26, 2Kir 5:11), 17 elutasítva indoklással, 148 gépi kizárás, 0 még nem vizsgált.

**Kötelező tanulság:** a lapnak a teljesség-mérés blokk-fájlját (`naplok/F123_teljesseg_<ID>_blokkok.tsv`) is olvasnia kell (vagy az adatbázisba kell kerülnie), különben a 148 gépi kizárást „még nem vizsgált”-nak mutatná.

Része még az apparátus-kapcsoló (D36 mélységi szintek: olvasói / apparátus).

## 2. Hatókör

- **Benne:** a `/motivum/<ID>` útvonal és sablon; a 12-es lelet-blokk; a hiányzó útvonalú lekérdezések; a blokk-fájl beolvasása vagy adatbázisba vitele; az apparátus-kapcsoló; tesztek.
- **Nincs benne:** a motívumfájlok és a lexikonlapok tartalma; a 17-es vers-lap (külön tétel, ha a mérés ezt kívánja); az olvasói alapnézet (Károli-olvasó) átalakítása.

## 3. Lépések (⛔ a kötelező megállások)

1. A nem igazolt öt lekérdezés (2, 3, 5, 15, 16) kézi ellenőrzése; a próbaminta hibájának és a valódi hibának a szétválasztása, jelentés.
2. A `/motivum/<ID>` útvonal és sablon; a 12-es blokk A, B, ★ számaival és a négy állapottal.
3. A blokk-fájl bevonása; teszt az ISTENTISZT-001 mintájára (168 → 3 / 17 / 148 / 0).
4. A nyolc hiányzó útvonalú lekérdezés.
5. Apparátus-kapcsoló. ⛔ A lap renderelt átnézése a felhasználóval merge előtt (lapot érintő PR).

## 4. Elfogadási feltételek

- az ISTENTISZT-001 12-es blokkja a fenti számokat adja, 0 „még nem vizsgált” hellyel;
- a 26 lekérdezésből mindegyik működik vagy indokolt döntéssel kimarad;
- `python eszkozok/teszt_futtat.py` zöld.

## 5. Döntésnapló

*(a menet tölti ki; új döntés helyőrzővel, `dontesek/uj/` fájlba)*
