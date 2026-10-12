# SQLITE_EPIT -- lekérdezés-próba (kis minta) (F79 M3)

*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py --proba (--mod minta) | ts=2026-10-12T08:08:25Z`; az ADATVAGYON_TERV 4. pontjának 1–6., 13–15. pontja; a várt eredmény mindig a megnevezett forrásból, nem az adatbázisból. Ez a fájl külön napló: a `SQLITE_EPIT_meres*.md` újragenerálása nem írja felül.*

Összesítés: 9/9 egyezik.

### 1. pont -- H0922 -> összes vers: **MEGEGYEZIK**

- SQL: `SELECT DISTINCT igehely FROM token_strong WHERE strong='H0922' ORDER BY igehely`
- eredmény: `['1Móz 1:2', 'Jer 4:23', 'Ézs 34:11']`
- várt: ['1Móz 1:2', 'Jer 4:23', 'Ézs 34:11']
- forrás: adat/elofordulasok.tsv TEREMT-002 (H8414+H0922, 3 sor), ADATVAGYON 4. pont mintaképe

### 2. pont -- „mélység” -> Strong-lista: **MEGEGYEZIK**

- SQL: `SELECT strong, COUNT(*) FROM token_par WHERE hu_szo='mélység' GROUP BY strong ORDER BY COUNT(*) DESC`
- eredmény: `[('H8415', 9), ('H8482', 1)]`
- várt: ['H8415 szerepel']
- forrás: adat/elofordulasok.tsv TEREMT-001 1Móz 1:2 (karoli_szo=mélység, strong=H8415)

### 3. pont -- H3548 -> Károli-szóalakok: **MEGEGYEZIK**

- SQL: `SELECT hu_szo, COUNT(*) FROM token_par WHERE strong='H3548' GROUP BY hu_szo ORDER BY COUNT(*) DESC`
- eredmény: `[('papjának', 5), ('papok', 3), ('pap', 3), ('papja', 2), ('papoknak', 1), ('papnak', 1), ('főtanácsos', 1), ('fők', 1), ('fő', 1), ('embere', 1), ('Pap', 1)]`
- várt: ['papja szerepel']
- forrás: adat/elofordulasok.tsv KIRALY-001 1Móz 14:18-20 (karoli_szo=papja, strong=H3548)

### 4. pont -- H8414 + H0922 egy versben: **MEGEGYEZIK**

- SQL: `SELECT DISTINCT a.igehely FROM token_strong a JOIN token_strong b ON a.igehely=b.igehely WHERE a.strong='H8414' AND b.strong='H0922' ORDER BY a.igehely`
- eredmény: `['1Móz 1:2', 'Jer 4:23', 'Ézs 34:11']`
- várt: ['1Móz 1:2', 'Jer 4:23', 'Ézs 34:11']
- forrás: adat/elofordulasok.tsv TEREMT-002 (1Móz 1:2, Jer 4:23, Ézs 34:11)

### 5. pont -- frázis: H7121 és H8034 (±6 token): **MEGEGYEZIK**

- SQL: `SELECT DISTINCT a.igehely FROM token_strong a JOIN token_strong b ON a.igehely=b.igehely AND b.sorszam<>a.sorszam AND ABS(b.sorszam-a.sorszam)<=6 WHERE a.strong='H7121' AND b.strong='H8034' ORDER BY a.igehely`
- eredmény: `['1Kir 18:24', '1Kir 18:25', '1Kir 18:26', '1Krón 16:8', '1Móz 11:9', '1Móz 12:8', '1Móz 13:4', '1Móz 16:11', '1Móz 16:13', '1Móz 16:15', '1Móz 17:15', '1Móz 17:19', '1Móz 17:5', '1Móz 19:22', '1Móz 19:37', '1Móz 19:38', '1Móz 21:3', '1Móz 21:33', '1Móz 22:14', '1Móz 25:25', '1Móz 25:26', '1Móz 25:30', '1Móz 26:18', '1Móz 26:20', '1Móz 26:21', '1Móz 26:22', '1Móz 26:25', '1Móz 26:33', '1Móz 27:36', '1Móz 28:19', '1Móz 29:32', '1Móz 29:33', '1Móz 29:34', '1Móz 29:35', '1Móz 2:20', '1Móz 30:11', '1Móz 30:13', '1Móz 30:18', '1Móz 30:20', '1Móz 30:21', '1Móz 30:24', '1Móz 30:6', '1Móz 30:8', '1Móz`
- várt: 22 elofordulasok-sor mindegyike szerepel (ISTENTISZT-001, gerinc H7121+H8034)
- forrás: adat/elofordulasok.tsv ISTENTISZT-001 (gerinc_elem=H7121+H8034)
- megjegyzés: hiányzó sor: - | az elvárt listán kívüli találat: 61 vers (a puszta Strong-pár a névadó „hívta a nevét” fordulatot is fogja; ez keresési találat, nem study-sor: CLAUDE.md 2. szabály) 1Móz 11:9, 1Móz 16:11, 1Móz 16:13, 1Móz 16:15, 1Móz 17:15, 1Móz 17:19, 1Móz 17:5, 1Móz 19:22, 1Móz 19:37, 1Móz 19:38, 1Móz 21:3, 1Móz 22:14

### 6. pont -- gyök (H0922, H8414): **MEGEGYEZIK**

- SQL: `SELECT strong, gyok_szarmaztatas FROM strong_szotar WHERE strong IN ('H0922','H8414')`
- eredmény: `[('H0922', 'from an unused root (meaning to be empty)'), ('H8414', 'from an unused root meaning to lie waste')]`
- várt: ['unused root mindkettőnél']
- forrás: konkordancia/Strong_szotar.tsv (Gyök/Származtatás)

### 13. pont -- BDB H7121: jelentés-sorok és a motívum tartománya: **MEGEGYEZIK**

- SQL: `SELECT l.strong, l.szotar, l.jelentes_szam, length(b.teljes_szocikk), (SELECT COUNT(*) FROM elofordulasok e WHERE e.jelentes_szam=l.jelentes_szam AND e.strong LIKE '%'\|\|l.strong\|\|'%' AND e.id='ISTENTISZT-001') FROM lexikon_hivatkozasok l JOIN bdb b ON b.strong=l.strong WHERE l.strong='H7121' AND l.szotar='BDB' ORDER BY l.jelentes_szam`
- eredmény: `[('H7121', 'BDB', '2.c', 10780, 17), ('H7121', 'BDB', '3', 10780, 2)]`
- várt: jelentes_szam: 2.c, 3; a 2.c-hez ISTENTISZT-001 sorok
- forrás: adat/lexikon_hivatkozasok.tsv, adat/elofordulasok.tsv (jelentes_szam=2.c)

### 14. pont -- LXX-híd H8415 -> G0012 -> ÚSZ: **MEGEGYEZIK**

- SQL: `SELECT greek_strong, count FROM lxx_bridge WHERE hebrew_strong='H8415' ORDER BY CAST(count AS INTEGER) DESC ; SELECT DISTINCT igehely FROM token_strong WHERE strong='G0012' ORDER BY igehely`
- eredmény: `{'hid': [('G0012', '24')], 'usz': ['Jel 11:7', 'Jel 17:8', 'Jel 20:1', 'Jel 20:3', 'Jel 9:1', 'Jel 9:11', 'Jel 9:2', 'Luk 8:31', 'Róm 10:7']}`
- várt: híd: [('G0012', '24')]; az ÚSZ-találat lefedi mind a 7 elofordulasok-sort
- forrás: adat/kulso/lxx_bridge.tsv; adat/elofordulasok.tsv TEREMT-001 (G0012)
- megjegyzés: nem lefedett elofordulasok-sor: - (a tartomány-sorok, pl. Jel 20:1-3, egy versen kapnak találatot)

### 15. pont -- kiejtés (H8415, 1Móz 1:2): **MEGEGYEZIK**

- SQL: `SELECT DISTINCT kiejtes FROM token_eredeti WHERE igehely='1Móz 1:2' AND strong_lanc='H8415'`
- eredmény: `['te.Hom']`
- várt: ['te.Hom']
- forrás: konkordancia/Strong_szotar.tsv H8415 Kiejtés

