# F34 M0 — felmérés (csak olvasás): a BDB „ψ” hibás feloldása

*Brief: `F34_BDB_PSI_BRIEF.md` · ág: `claude/bdb-psi` · a forrás és az `adat/forditasok.tsv` NEM módosult.*
*Reprodukálható: `python naplok/F34_M0_felmeres.py`, `python naplok/F34_M0_forditasok.py`, `python naplok/F34_M0_jelentes_gen.py` (a szakaszok táblái).*
*Teljes találatlista (minden hely, hibás és javított alak, kontextus): `naplok/F34_M0_lista.tsv`.*

## 1. Fő megállapítás: a hiba sokkal szélesebb, mint a brief

A forrásban a „ψ” nem öt szócikkben hibás: **54 szócikkben** biztosan (A-lista, 104 hely), további **101 szócikkben** gyanúsan (B-lista, 201 hely).
A brief a 13. kapuból indult, az pedig csak a már lefordított BDB-szócikkeket látja. A mintázat: a „ψ” helyére a szövegben az *előző* könyvnév
került (pl. `Psalm Job 97:7`, `Hab 140:4`, `2Sam 72:20`), a zsoltár-fejezetszám maradt. A forrás részben maga is jelzi (`Psalm Zech 26:2`, `Paslm Isa 107:12`).

A javítás a forrásban történik, tehát a hatókör (54+ szócikk) az orkesztrátor döntése. Az `adat/forditasok.tsv`-t viszont csak **5 sor** érinti (4. pont).

## 2. Módszer és osztályozás

A forrás minden `Könyv fejezet:vers` alakját összevetettem a könyv fejezetszámával (a 13. kapu logikája, BDB-könyvrövidítésekkel, kiegészítve az `1Ki`/`2Ki` alakokkal, mert a forrás ezeket is használja).

- **A — egyértelmű ψ-hiba (javítandó lista):** a fejezet > a megnevezett könyv fejezetszáma, ÉS (a fejezet > 66, tehát csak a Zsoltárok lehet — vagy közvetlenül „Psalm”/„Paslm” szó áll előtte). Javított alak: a könyvrövidítés cseréje `Psa`-ra (az ismétlődő `Psalm Psa …` kezelése M1-es opció).
- **B — gyanús (NEM döntöttem):** a fejezet > a könyv fejezetszáma, de nem csak Zsoltár lehet: 51–66 között Zsoltár vagy Ézsaiás; ≤ 50 esetén Zsoltár vagy más hibás feloldás (pl. Jób/Kivonulás: `Lev 28:17`, `Ruth 25:3`, `Num 39:31`).
- **R — rejtett/lánc (NEM döntöttem):** a fejezet létezik a könyvben, ezért a kapu nem jelzi; láncban szomszédos egy A/B hellyel azonos könyvnévvel, vagy „Psalm” szó áll előtte. Ide került a brief rejtett esete, a H7585 `Ezek 16:10` (forrás-sor 7092; `Psa 16:10`-re utaló kontextus). Az R-lista nem teljes: az a ψ-hely, amelynek sem a fejezete nem hibás, sem lánc/jelző nem utal rá, gépileg nem ismerhető fel.
- **KIZÁRT:** `Dan 22:14` (H8034, forrás-sor 7501) — a forrás saját hibája, nem hatókör, csak jelezve.

## 3. Eredmény a forrásban (konkordancia/BDB_teljes_unabridged.tsv)

| Osztály | Szócikk | Hely |
|---|---|---|
| A (javítandó) | 54 | 104 |
| B (gyanús) | 101 | 201 |
| R (rejtett/lánc) | 17 | 17 |
| KIZÁRT | 1 | 1 |

A brief által említett **H6093, H7121, H1121** szócikkekben a mostani forrásban nincs találatom, és a mostani `forditasok.tsv`-sorok (56., 57., 58.) sem hordoznak hibás ψ-helyet — a brief valószínűleg a korábbi, azóta kicserélt sorokra utal. Kérdés a jóváhagyónak.

### 3.A — egyértelmű ψ-hibák (javítandó lista)

| Strong | forrás-sor | hibás -> javított |
|---|---|---|
| H0319 | 296 | Eccl 139:9 -> Psa 139:9 |
| H0411 | 382 | Deut 93:3 -> Psa 93:3 |
| H0430 | 401 | Job 97:7 -> Psa 97:7 |
| H0595 | 556 | Gen 81:48 -> Psa 81:48 |
| H0974 | 912 | Zech 26:2 -> Psa 26:2; Zech 81:8 -> Psa 81:8; Jer 95:9 -> Psa 95:9 |
| H0982 | 920 | Amos 33:21 -> Psa 33:21 |
| H1366 | 1275 | Ezek 147:14 -> Psa 147:14 |
| H1369 | 1278 | Job 71:16 -> Psa 71:16 |
| H1732 | 1625 | 2Sam 72:20 -> Psa 72:20; 2Sam 89:36 -> Psa 89:36; 2Sam 89:50 -> Psa 89:50; 2Sam 122:5 -> Psa 122:5; 2Sam 132:1132 -> Psa 132:1132 |
| H1942 | 1824 | Prov 91:3 -> Psa 91:3; Prov 94:20 -> Psa 94:20 |
| H2363 | 2216 | 1Sam 70:2 -> Psa 70:2; 1Sam 71:12 -> Psa 71:12; 1Sam 70:6 -> Psa 70:6; 1Sam 141:1 -> Psa 141:1 |
| H2595 | 2435 | 2Sam 57:5 -> Psa 57:5 |
| H2617 | 2456 | Isa 89:50 -> Psa 89:50 |
| H2778 | 2608 | Neh 74:10 -> Psa 74:10; Neh 74:18 -> Psa 74:18; Neh 79:12 -> Psa 79:12; Neh 89:52 -> Psa 89:52; Neh 102:9 -> Psa 102:9 |
| H2787 | 2616 | Job 69:4 -> Psa 69:4 |
| H2896 | 2718 | Job 104:28 -> Psa 104:28 |
| H3336 | 3112 | Hab 103:14 -> Psa 103:14 |
| H3738 | 3492 | Jer 119:85 -> Psa 119:85 |
| H3781 | 3531 | Jer 74:6 -> Psa 74:6 |
| H3782 | 3532 | Isa 107:12 -> Psa 107:12; Isa 109:24 -> Psa 109:24; Neh 31:11 -> Psa 31:11; Prov 64:9 -> Psa 64:9 |
| H3852 | 3594 | Num 83:15 -> Psa 83:15 |
| H4383 | 4089 | Lev 119:165 -> Psa 119:165 |
| H4480 | 4181 | 2Sam 74:11 -> Psa 74:11; Job 76:7 -> Psa 76:7 |
| H4900 | 4582 | Neh 85:6 -> Psa 85:6 |
| H4908 | 4590 | Isa 74:7 -> Psa 74:7; Isa 78:60 -> Psa 78:60 |
| H5038 | 4711 | Josh 82:9 -> Psa 82:9 |
| H5414 | 5066 | 2Sam 69:12 -> Psa 69:12; 2Sam 135:12 -> Psa 135:12 |
| H5542 | 5188 | Hab 67:5 -> Psa 67:5; Hab 68:20 -> Psa 68:20; Hab 76:4 -> Psa 76:4; Hab 76:10 -> Psa 76:10; Hab 77:4 -> Psa 77:4; Hab 77:10 -> Psa 77:10; Hab 77:16 -> Psa 77:16; Hab 81:8 -> Psa 81:8; Hab 82:2 -> Psa 82:2; Hab 83:9 -> Psa 83:9; Hab 84:5 -> Psa 84:5; Hab 84:9 -> Psa 84:9; Hab 88:8 -> Psa 88:8; Hab 88:11 -> Psa 88:11; Hab 89:38 -> Psa 89:38; Hab 89:46 -> Psa 89:46; Hab 140:4 -> Psa 140:4; Hab 140:6 -> Psa 140:6; Hab 140:9 -> Psa 140:9; Hab 143:6 -> Psa 143:6; Hab 67:2 -> Psa 67:2; Hab 68:8 -> Psa 68:8; Hab 68:33 -> Psa 68:33; Hab 89:5 -> Psa 89:5; Hab 80:8 -> Psa 80:8 |
| H5591 | 5236 | Jer 107:25 -> Psa 107:25; Jer 148:8 -> Psa 148:8; Jer 107:29 -> Psa 107:29 |
| H5643 | 5285 | 2Sam 81:8 -> Psa 81:8 |
| H5645 | 5287 | 2Sam 77:18 -> Psa 77:18 |
| H5647 | 5289 | 2Ki 97:7 -> Psa 97:7 |
| H5650 | 5292 | Isa 69:13 -> Psa 69:13; Isa 69:14 -> Psa 69:14 |
| H5704 | 5342 | Jer 90:3 -> Psa 90:3 |
| H5869 | 5491 | 2Sam 131:1 -> Psa 131:1 |
| H5920 | 5534 | Prov 140:11 -> Psa 140:11 |
| H5982 | 5588 | Job 75:4 -> Psa 75:4 |
| H6403 | 5989 | 2Sam 71:4 -> Psa 71:4 |
| H6486 | 6067 | Num 109:8 -> Psa 109:8 |
| H6908 | 6468 | Neh 106:4 -> Psa 106:4 |
| H7130 | 6667 | 1Ki 138:7 -> Psa 138:7 |
| H7216 | 6749 | 1Ki 145:31 -> Psa 145:31 |
| H7287 | 6815 | Lev 110:2 -> Psa 110:2 |
| H7521 | 7032 | Hag 77:8 -> Psa 77:8 |
| H7585 | 7092 | Ezek 73:23 -> Psa 73:23; Ezek 73:25 -> Psa 73:25 |
| H7797 | 7284 | Isa 68:14 -> Psa 68:14 |
| H7843 | 7327 | Prov 75:1 -> Psa 75:1 |
| H8081 | 7544 | Prov 109:18 -> Psa 109:18 |
| H8398 | 7836 | Lam 89:12 -> Psa 89:12 |
| H8415 | 7850 | Isa 106:9 -> Psa 106:9; Isa 71:20 -> Psa 71:20 |
| H8549 | 7970 | 2Sam 84:12 -> Psa 84:12 |
| H9000 | 8090 | Job 104:25 -> Psa 104:25; Job 105:34 -> Psa 105:34 |
| H9005 | 8088 | Isa 143:6 -> Psa 143:6 |
| H9009 | 8091 | 1Ki 72:8 -> Psa 72:8 |


### 3.B — gyanús (NEM javítandó, döntés kell)

| Strong | forrás-sor | hibás -> javított |
|---|---|---|
| H0001 | 2 | 1Ki 50:1 -> Psa 50:1; 1Ki 50:5 -> Psa 50:5; Esth 11:32 -> Psa 11:32 |
| H0026 | 22 | 2Sam 25:18 -> Psa 25:18 |
| H0056 | 50 | 1Sam 33:9 -> Psa 33:9 |
| H0251 | 229 | Joel 7:10 -> Psa 7:10 |
| H0398 | 370 | Lev 28:17 -> Psa 28:17 |
| H0413 | 384 | Deut 37:36 -> Psa 37:36 |
| H0479 | 448 | Ezra 16:8 -> Psa 16:8 |
| H0539 | 503 | Josh 25:16 -> Psa 25:16 |
| H0646 | 605 | Lev 29:5 -> Psa 29:5; Lev 39:22 -> Psa 39:22 |
| H0734 | 689 | 2Sam 31:32 -> Psa 31:32 |
| H0821 | 766 | Lam 19:19 -> Psa 19:19 |
| H0834 | 779 | Ruth 8:12 -> Psa 8:12; Ruth 8:14 -> Psa 8:14; Ruth 9:1 -> Psa 9:1 |
| H0974 | 912 | Zech 66:10 -> Psa 66:10 |
| H1008 | 942 | Hos 35:15 -> Psa 35:15 |
| H1157 | 1082 | Lam 9:10 -> Psa 9:10 |
| H1931 | 1815 | 2Ki 33:23 -> Psa 33:23; Hos 19:21 -> Psa 19:21; Hos 22:9 -> Psa 22:9; Hos 24:12 -> Psa 24:12; Lam 6:10 -> Psa 6:10 |
| H1942 | 1824 | Prov 55:12 -> Psa 55:12; Prov 57:2 -> Psa 57:2 |
| H1945 | 1827 | 1Ki 34:5 -> Psa 34:5 |
| H1961 | 1843 | 1Ki 23:25 -> Psa 23:25 |
| H2063 | 1940 | Esth 25:12 -> Psa 25:12 |
| H2232 | 2095 | Judg 31:8 -> Psa 31:8 |
| H2320 | 2178 | 1Ki 25:1 -> Psa 25:1; 1Ki 25:3 -> Psa 25:3; 1Ki 25:8 -> Psa 25:8; 1Ki 25:25 -> Psa 25:25; 1Ki 25:27 -> Psa 25:27 |
| H2363 | 2216 | 1Sam 38:23 -> Psa 38:23; 1Sam 40:14 -> Psa 40:14 |
| H2406 | 2259 | 1Ki 27:5 -> Psa 27:5 |
| H2597 | 2437 | Ezra 16:17 -> Psa 16:17 |
| H2778 | 2608 | Neh 42:11 -> Psa 42:11; Neh 44:17 -> Psa 44:17; Neh 55:13 -> Psa 55:13; Neh 57:4 -> Psa 57:4 |
| H3001 | 2817 | Eccl 17:10 -> Psa 17:10 |
| H3117 | 2914 | Dan 40:4 -> Psa 40:4 |
| H3289 | 3067 | Nah 7:5 -> Psa 7:5; Nah 19:12 -> Psa 19:12; Nah 23:8 -> Psa 23:8 |
| H3318 | 3094 | Jer 58:8 -> Psa 58:8 |
| H3335 | 3111 | 2Ki 46:11 -> Psa 46:11 |
| H3425 | 3195 | Jer 61:6 -> Psa 61:6 |
| H3426 | 3196 | Ruth 25:3 -> Psa 25:3; Ruth 28:1 -> Psa 28:1; Ruth 38:28 -> Psa 38:28 |
| H3444 | 3213 | 2Sam 42:12 -> Psa 42:12; 2Sam 53:7 -> Psa 53:7 |
| H3462 | 3231 | 1Ki 44:24 -> Psa 44:24 |
| H3478 | 3247 | 1Ki 24:7 -> Psa 24:7; 1Ki 24:10 -> Psa 24:10 |
| H3588 | 3350 | 1Ki 32:29 -> Psa 32:29; 1Ki 47:18 -> Psa 47:18 |
| H3738 | 3492 | Jer 57:7 -> Psa 57:7 |
| H3808 | 3556 | 2Sam 26:1 -> Psa 26:1 |
| H3896 | 3635 | 2Sam 31:2 -> Psa 31:2 |
| H3899 | 3638 | Prov 65:25 -> Psa 65:25 |
| H4100 | 3826 | Judg 33:15 -> Psa 33:15 |
| H4196 | 3909 | Judg 22:28 -> Psa 22:28 |
| H4421 | 4124 | Judg 22:35 -> Psa 22:35 |
| H4427 | 4130 | 2Ki 33:34 -> Psa 33:34 |
| H4428 | 4131 | Eccl 15:26 -> Psa 15:26 |
| H4480 | 4181 | 1Ki 32:47 -> Psa 32:47 |
| H4605 | 4302 | Num 39:31 -> Psa 39:31 |
| H4672 | 4364 | Eccl 25:8 -> Psa 25:8 |
| H4700 | 4391 | 2Sam 25:6 -> Psa 25:6 |
| H4832 | 4516 | Eccl 15:4 -> Psa 15:4 |
| H4948 | 4628 | 1Ki 25:16 -> Psa 25:16 |
| H5002 | 4677 | Jer 57:57 -> Psa 57:57 |
| H5035 | 4708 | Amos 14:11 -> Psa 14:11 |
| H5046 | 4719 | 1Ki 29:41 -> Psa 29:41 |
| H5139 | 4810 | Lam 49:26 -> Psa 49:26 |
| H5158 | 4829 | 1Ki 23:6 -> Psa 23:6 |
| H5377 | 5031 | Obad 3:7 -> Psa 3:7 |
| H5414 | 5066 | 2Sam 39:6 -> Psa 39:6 |
| H5532 | 5178 | Eccl 22:2 -> Psa 22:2; Eccl 15:3 -> Psa 15:3; Eccl 22:22 -> Psa 22:22 |
| H5542 | 5188 | Hab 24:10 -> Psa 24:10; Hab 46:12 -> Psa 46:12; Hab 9:21 -> Psa 9:21; Hab 4:3 -> Psa 4:3; Hab 4:5 -> Psa 4:5; Hab 7:6 -> Psa 7:6; Hab 9:17 -> Psa 9:17; Hab 24:6 -> Psa 24:6; Hab 32:4 -> Psa 32:4; Hab 32:5 -> Psa 32:5; Hab 32:7 -> Psa 32:7; Hab 39:6 -> Psa 39:6; Hab 39:12 -> Psa 39:12; Hab 46:4 -> Psa 46:4; Hab 46:8 -> Psa 46:8; Hab 47:5 -> Psa 47:5; Hab 48:9 -> Psa 48:9; Hab 49:13 -> Psa 49:13; Hab 49:14 -> Psa 49:14; Hab 49:16 -> Psa 49:16; Hab 50:6 -> Psa 50:6; Hab 52:5 -> Psa 52:5; Hab 52:7 -> Psa 52:7; Hab 54:5 -> Psa 54:5; Hab 59:6 -> Psa 59:6; Hab 59:14 -> Psa 59:14; Hab 61:5 -> Psa 61:5; Hab 62:5 -> Psa 62:5; Hab 62:9 -> Psa 62:9; Hab 66:4 -> Psa 66:4; Hab 66:7 -> Psa 66:7; Hab 66:15 -> Psa 66:15; Hab 44:9 -> Psa 44:9; Hab 55:8 -> Psa 55:8; Hab 57:7 -> Psa 57:7; Hab 60:6 -> Psa 60:6 |
| H5650 | 5292 | Jonah 14:25 -> Psa 14:25 |
| H5710 | 5348 | Prov 38:19 -> Psa 38:19 |
| H5715 | 5353 | Lev 30:6 -> Psa 30:6 |
| H5838 | 5467 | Ezra 12:33 -> Psa 12:33 |
| H5973 | 5582 | 2Sam 26:16 -> Psa 26:16 |
| H5975 | 5583 | 2Ki 31:2 -> Psa 31:2 |
| H5997 | 5601 | Zech 19:11 -> Psa 19:11; Zech 24:19 -> Psa 24:19; Zech 25:17 -> Psa 25:17; Zech 18:20 -> Psa 18:20; Zech 19:15 -> Psa 19:15; Zech 19:17 -> Psa 19:17; Zech 25:14 -> Psa 25:14; Zech 25:15 -> Psa 25:15 |
| H6240 | 5834 | Nah 5:14 -> Psa 5:14 |
| H6258 | 5851 | 2Ki 46:34 -> Psa 46:34 |
| H6403 | 5989 | 2Sam 37:40 -> Psa 37:40; 2Sam 43:1 -> Psa 43:1 |
| H6428 | 6012 | Mic 25:34 -> Psa 25:34 |
| H6437 | 6020 | Nah 47:3 -> Psa 47:3 |
| H6440 | 6022 | 2Ki 36:12 -> Psa 36:12; Zech 17:3 -> Psa 17:3; Zech 17:5 -> Psa 17:5 |
| H6607 | 6181 | Num 39:38 -> Psa 39:38 |
| H6677 | 6251 | Judg 45:14 -> Psa 45:14; Judg 46:29 -> Psa 46:29; Judg 33:4 -> Psa 33:4; Judg 45:14 -> Psa 45:14; Judg 46:29 -> Psa 46:29; Judg 27:16 -> Psa 27:16 |
| H6805 | 6372 | Hab 63:1 -> Psa 63:1 |
| H6881 | 6444 | Dan 19:41 -> Psa 19:41 |
| H6915 | 6474 | 1Ki 29:20 -> Psa 29:20 |
| H6923 | 6481 | Mic 17:3 -> Psa 17:3 |
| H6981 | 6532 | Judg 26:1 -> Psa 26:1 |
| H7200 | 6735 | 1Sam 32:31 -> Psa 32:31; 1Sam 46:30 -> Psa 46:30; 1Sam 48:11 -> Psa 48:11 |
| H7223 | 6756 | Eccl 17:10 -> Psa 17:10 |
| H7230 | 6762 | 1Ki 24:24 -> Psa 24:24; 1Ki 30:13 -> Psa 30:13 |
| H7389 | 6913 | Mal 28:19 -> Psa 28:19; Mal 31:7 -> Psa 31:7; Mal 13:18 -> Psa 13:18; Mal 24:34 -> Psa 24:34; Mal 10:15 -> Psa 10:15; Mal 30:8 -> Psa 30:8; Mal 6:11 -> Psa 6:11; Mal 24:34 -> Psa 24:34 |
| H7458 | 6973 | 1Ki 25:3 -> Psa 25:3 |
| H7585 | 7092 | Ezek 49:16 -> Psa 49:16 |
| H7676 | 7175 | Lev 28:8 -> Psa 28:8 |
| H7725 | 7221 | 2Sam 26:23 -> Psa 26:23 |
| H7760 | 7251 | Deut 45:7 -> Psa 45:7; Lev 40:15 -> Psa 40:15 |
| H7843 | 7327 | 2Ki 36:10 -> Psa 36:10; Prov 57:1 -> Psa 57:1; Prov 58:1 -> Psa 58:1; Prov 59:1 -> Psa 59:1 |
| H7940 | 7418 | 2Sam 26:4 -> Psa 26:4 |
| H7999 | 7470 | Eccl 50:14 -> Psa 50:14 |
| H8034 | 7501 | Dan 22:19 -> Psa 22:19 |
| H8313 | 7759 | 1Ki 23:16 -> Psa 23:16; 1Ki 23:20 -> Psa 23:20 |
| H8398 | 7836 | Lam 24:1 -> Psa 24:1 |
| H8478 | 7905 | Dan 18:4 -> Psa 18:4; Dan 21:15 -> Psa 21:15; Dan 24:2 -> Psa 24:2 |
| H8548 | 7969 | Lev 46:14 -> Psa 46:14 |
| H9004 | 8087 | Dan 23:22 -> Psa 23:22 |
| H9005 | 8088 | Joel 9:9 -> Psa 9:9; Hab 41:47 -> Psa 41:47 |
| H9009 | 8091 | 1Ki 45:14 -> Psa 45:14; 1Ki 45:16 -> Psa 45:16; 1Ki 61:7 -> Psa 61:7; 1Ki 66:6 -> Psa 66:6; 1Ki 59:7 -> Psa 59:7; 1Ki 59:15 -> Psa 59:15 |


### 3.R — rejtett és láncban gyanús helyek (NEM javítandó, döntés kell)

| Strong | forrás-sor | hibás -> javított |
|---|---|---|
| H0040 | 35 | Gen 34:1 -> (Psa 34:1?) |
| H0056 | 50 | 1Sam 24:4 -> (Psa 24:4?) |
| H0479 | 448 | Ezra 4:21 -> (Psa 4:21?) |
| H0834 | 779 | Ruth 2:29 -> (Psa 2:29?) |
| H2778 | 2608 | Neh 6:13 -> (Psa 6:13?) |
| H3425 | 3195 | Jer 32:8 -> (Psa 32:8?) |
| H3899 | 3638 | Prov 6:8 -> (Psa 6:8?) |
| H5035 | 4708 | Amos 5:23 -> (Psa 5:23?) |
| H5542 | 5188 | Hab 3:9 -> (Psa 3:9?) |
| H5645 | 5287 | 2Sam 23:4 -> (Psa 23:4?) |
| H5920 | 5534 | 1Sam 2:10 -> (Psa 2:10?) |
| H5982 | 5588 | Job 9:5 -> (Psa 9:5?) |
| H6981 | 6532 | Judg 9:19 -> (Psa 9:19?) |
| H7585 | 7092 | Ezek 16:10 -> (Psa 16:10?) |
| H7725 | 7221 | 2Sam 16:12 -> (Psa 16:12?) |
| H7999 | 7470 | Eccl 5:3 -> (Psa 5:3?) |
| H8415 | 7850 | Isa 63:13 -> (Psa 63:13?) |


### 3.X — más forráshiba-családok (nem ψ; csak jelezve)

- `1Ki`/`2Ki` rövidítésű, a könyvnél nagyobb fejezetű helyek (pl. a H7843-ben `2Ki 36:10`, a fordításban `2Kir 36:10`): valószínűleg `Isa 36:10`, nem ψ. A fejezet szerint az A/B listában szerepelnek.
- `Paslm 119:93` (H2271): elírás; `2Sam 132:1132:11` (H1732): összeolvadt alak a forrásban — kézi nézet kell.
- A B-lista nagy része (fejezet ≤ 50) valószínűleg nem ψ, hanem más szimbólum hibás feloldása (Jób, Kivonulás) — külön hatókör-döntés.

## 4. Érintett `adat/forditasok.tsv` sorok

Fájlsor-számok (1. sor a megjegyzés, 2. a fejléc). A 13. kapu a mostani fájlon ugyanezt az 5 sort jelzi (78, 81, 84, 85, 89).

| Sor | Szótár | Strong | jelentes_szam | Állapot | A (hibás ψ) | B (gyanús) | R (rejtett/lánc) |
|---|---|---|---|---|---|---|---|
| 78 | BDB | H8415 | teljes | **kezi** | Ézs 106:9; Ézs 71:20 | — | Ézs 63:13 |
| 81 | BDB | H7585 | teljes | **kezi** | Ez 73:23; Ez 73:25 | Ez 49:16 | Ez 16:10 (rejtett) |
| 84 | BDB | H7843 | teljes | opus | Péld 75:1 | Péld 57:1; Péld 58:1; Péld 59:1; 2Kir 36:10 | — |
| 85 | BDB | H8034 | teljes | opus | — | Dán 22:19 | (Dán 22:14: kizárt) |
| 89 | BDB | H0430 | teljes | opus | Jób 97:7 | — | — |

- **Érintett sor összesen: 5**; A-hely a 78., 81., 84., 89. sorban van, a 85. sorban csak B-hely.
- **`kezi` sorok (az érintésükhöz külön jóváhagyás kell):** 78. sor (H8415) és 81. sor (H7585). Mindkettő A-helyet hordoz; a 81. sor a rejtett `Ez 16:10`-et is.
- A 9. sor (H8034, `részlet`, `kezi`) forrása érintett, de a fordított szövegben nincs hibás hely.
- A `forras_hash` a *forrásból* számolódik (`eszkozok/emeles.py: forras_hash`): a forrás javítása után az érintett sorok hash-e elavul. M3-ban ellenőrizendő, hogy az újraszámolt hash-t a 13. szabály (`ellenoriz.py`) és az E19 elfogadja-e.

## 5. Következő lépés

⛔ M1: az A-lista (javítandó) és a B/R-lista (gyanús) jóváhagyása. A forrás és az `adat/forditasok.tsv` a jóváhagyásig érintetlen.
