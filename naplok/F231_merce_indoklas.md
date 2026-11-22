# F231 — az F232 olvasói mérce frissítésének indoklása (2026-11-22)

A `eszkozok/olvaso_szerver/merce/` 18 fájlja a `teszt_olvasoi_merce.py --merce-frissit` paranccsal frissült. Minden megváltozott sort (git diff a main-hez mérve, hozzáadott és törölt sor egyaránt) egy gépi besoroló rendelt egy okhoz: a sor blokkja (a `## [blokk]` jelölés a régi, illetve az új fájlban) vagy a sor mintája szerint. Az ok a hibalista sorszáma (`naplok/OLVASO_EGYBEN_HIBALISTA.md`). Besorolatlan sor: 0. A besoroló: a jegyzetmappa `olvaso-egyben-elokeszites/merce_ok.py` szkriptje (a session scratchpadjából).

## Okonként

| Ok (hibalista) | Sor |
|---|---|
| 1–13, 15, 16, 19 (BDB-kártya: egybefüggő szöveg, olvasói jelölések, DT914) | 1280 |
| 36 (csukva) | 920 |
| 45, 46 (jelleg és forrássor a csukott Forrás-lenyílóban) | 630 |
| 21, 22, 25 (Thayer-kártya) | 297 |
| 34, 35, 36 (iota-átírás, központozás, táblázatos nézet csukva) | 266 |
| 30, 38 (összevont sor, mért pontosság) | 242 |
| 45 (a jelleg-címke kikerült a blokkcímből) | 218 |
| 45, 46 (a forrássor a csukott Forrás-lenyílóba került) | 218 |
| 27/2.6 (doménkód csak súgóban) | 178 |
| 27 (UBS DNTG jelentésenként, azonosító nélkül) | 173 |
| 27 (UBS-azonosító csak súgóban) | 116 |
| 30–32 (szócsoport-keret, a kiejtés a kereten) | 111 |
| blokksorrend (21: görög blokksor; 37: versszámozás a tetején; 47: üres blokk rejtve) | 102 |
| 57 (arányos sáv, a 66 könyv felsorolása nélkül) | 60 |
| 45, 46, 58 (keret; angol a súgóban) | 59 |
| 28 (ÚSZ: hány vers látszik, UBS-jelentés) | 54 |
| 45, 46 (keret) | 54 |
| 21 (forrásszöveg alul, csukva) | 48 |
| 51 (a lap neve) | 36 |
| 52 (ékezetes szintnevek) | 36 |
| 21 (csukva) | 32 |
| 56 (számkártyák) | 30 |
| 58 (az angol a súgóban) | 30 |
| 47 (az üres blokkok összesítő sora) | 30 |
| 37, 48 (egysoros) | 21 |
| 50 (a szó-lap linkjei) | 20 |
| 37, 48 (egysoros összefoglaló, a forrásazonosító súgóban) | 20 |
| 45, 46, 58 (keret) | 18 |
| 45, 46 (a blokk keretének változása: címke és forrás a lenyílóban) | 14 |
| 40 (a forrás hiánya kimondva) | 8 |
| a mérce fejléce | 6 |
| 49 (a jogi megjegyzés a Forrás-lenyílóban) | 6 |
| 45, 46, 49 (keret) | 4 |

## Laponként

- `fejezet_1Moz_1.txt`: 51 (2); 52 (2)
- `fejezet_Zsolt_22.txt`: 51 (2); 52 (2)
- `szo_G0264.txt`: 27 (48); 45, 46 (42); 28 (14); 21 (12); 57 (12); 21, 22, 25 (12); blokksorrend (11); 45 (11); 45, 46 (11); 21 (8); 45, 46, 58 (7); 27/2.6 (5); 56 (3); 58 (3); 51 (2); 52 (2); 50 (2); 45, 46 (2); 45, 46 (1); 45, 46, 49 (1)
- `szo_G1311.txt`: 21, 22, 25 (54); 45, 46 (42); 27 (23); 28 (13); 21 (12); blokksorrend (11); 45 (11); 45, 46 (11); 57 (10); 27/2.6 (9); 21 (8); 45, 46, 58 (7); 56 (3); 58 (3); 51 (2); 52 (2); 50 (2); 45, 46 (2); 45, 46 (1); 45, 46, 49 (1)
- `szo_G2671.txt`: 45, 46 (42); 21, 22, 25 (24); 27 (21); 28 (13); 21 (12); blokksorrend (11); 45 (11); 45, 46 (11); 27/2.6 (9); 57 (8); 21 (8); 56 (3); 58 (3); 45, 46, 58 (3); 51 (2); 52 (2); 50 (2); 45, 46 (2); 45, 46 (1); 45, 46, 49 (1)
- `szo_G3056.txt`: 21, 22, 25 (207); 27 (81); 45, 46 (42); 27/2.6 (27); 28 (14); 21 (12); 57 (12); blokksorrend (11); 45 (11); 45, 46 (11); 21 (8); 56 (3); 58 (3); 51 (2); 52 (2); 50 (2); 45, 46 (2); 45, 46 (1); 45, 46, 49 (1); 45, 46, 58 (1)
- `szo_H0251.txt`: 1–13, 15, 16, 19 (70); 45, 46 (36); 27 (21); 27/2.6 (21); 45 (12); 45, 46 (12); 45, 46, 58 (8); 45, 46 (4); 56 (3); 58 (3); 57 (3); 51 (2); 52 (2); 50 (2); 45, 46 (1)
- `szo_H1242.txt`: 1–13, 15, 16, 19 (165); 45, 46 (33); 45 (12); 45, 46 (12); 27 (5); 27/2.6 (5); 45, 46 (4); 56 (3); 58 (3); 57 (3); 45, 46, 58 (3); 51 (2); 52 (2); 50 (2); 47 (2); 45, 46 (1); blokksorrend (1)
- `szo_H2398.txt`: 1–13, 15, 16, 19 (289); 45, 46 (36); 27 (27); 27/2.6 (27); 45, 46, 58 (16); 45 (12); 45, 46 (12); 45, 46 (4); 56 (3); 58 (3); 57 (3); 51 (2); 52 (2); 50 (2); 45, 46 (1)
- `szo_H3615.txt`: 1–13, 15, 16, 19 (327); 45, 46 (36); 27 (35); 27/2.6 (35); 45, 46, 58 (16); 45 (12); 45, 46 (12); 45, 46 (4); 56 (3); 58 (3); 57 (3); 51 (2); 52 (2); 50 (2); 45, 46 (1)
- `szo_H7451.txt`: 1–13, 15, 16, 19 (418); 45, 46 (33); 27/2.6 (33); 27 (21); 45, 46, 58 (13); 45 (12); 45, 46 (12); 45, 46 (4); 56 (3); 58 (3); 57 (3); 51 (2); 52 (2); 50 (2); 47 (2); 45, 46 (1); blokksorrend (1)
- `szo_H7837.txt`: 45, 46 (33); 45 (12); 45, 46 (12); 1–13, 15, 16, 19 (11); 27 (7); 27/2.6 (7); 45, 46 (4); 56 (3); 58 (3); 57 (3); 45, 46, 58 (3); 51 (2); 52 (2); 50 (2); 47 (2); 45, 46 (1); blokksorrend (1)
- `vers_1Moz_1_1.txt`: 36 (98); 45, 46 (48); 34, 35, 36 (25); 45 (17); 45, 46 (17); 30, 38 (17); 30–32 (13); blokksorrend (7); 45, 46 (5); 37, 48 (4); 37, 48 (4); 51 (2); 52 (2); 47 (2); a mérce fejléce (1); 40 (1); 49 (1)
- `vers_1Moz_1_5.txt`: 36 (178); 45, 46 (48); 34, 35, 36 (41); 30, 38 (40); 45 (17); 45, 46 (17); 30–32 (10); blokksorrend (9); 45, 46 (5); 37, 48 (4); 37, 48 (4); 51 (2); 52 (2); 47 (2); a mérce fejléce (1); 40 (1); 49 (1)
- `vers_1Moz_3_6.txt`: 36 (316); 34, 35, 36 (81); 30, 38 (67); 30–32 (49); 45, 46 (45); 45 (17); 45, 46 (17); blokksorrend (9); 45, 46 (4); 37, 48 (4); 37, 48 (4); 47 (3); 51 (2); 52 (2); a mérce fejléce (1); 40 (1); 49 (1)
- `vers_1Moz_4_7.txt`: 36 (182); 30, 38 (56); 45, 46 (51); 34, 35, 36 (49); 30–32 (20); 45 (17); 45, 46 (17); 45, 46 (6); blokksorrend (6); 37, 48 (4); 37, 48 (4); 51 (2); 52 (2); a mérce fejléce (1); 40 (1); 49 (1)
- `vers_Jan_1_1.txt`: 34, 35, 36 (37); 30, 38 (28); 45, 46 (18); 45 (17); 45, 46 (17); blokksorrend (15); 47 (13); 51 (2); 52 (2); 45, 46 (2); 40 (2); a mérce fejléce (1); 49 (1)
- `vers_Zsolt_22_2.txt`: 36 (146); 45, 46 (45); 30, 38 (34); 34, 35, 36 (33); 30–32 (19); 45 (17); 45, 46 (17); blokksorrend (9); 37, 48 (5); 45, 46 (4); 37, 48 (4); 47 (4); 51 (2); 52 (2); 40 (2); a mérce fejléce (1); 49 (1)

