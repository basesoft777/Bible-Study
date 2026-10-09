ELTÉRÉS: 5 tétel

# ELLENŐR — F52_TERV_SZINKRON_BRIEF.md (v1.1), 3. futás
Tartomány: 2108fc67..6e2336d5 (a 2108fc67 szülője: 1f420a7c = main; a 78844919 annak szülője)

*A jelentés szövegét a `fuggetlen-ellenor` subagent adta vissza; írási eszköze nem volt, ezért az orkesztrátor változtatás nélkül mentette ide (2026-10-09). A `feladatok.py ellenoriz` futtatását az ellenőr nem végezhette el; az orkesztrátor futtatta: 104 brief, 0 hiba, 0 figyelmeztetés.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| Hatókör | OK | — | `git diff --name-status main 6e2336d5`: M ADATVAGYON_TERV.md, ATALAKITASI_TERV.md.md, DONTESEK.md, F52_TERV_SZINKRON_BRIEF.md, MUNKATERV.md, VIBE_GUIDE.md, naplok/F52_TERV_SZINKRON_naplo.md — mind a brief `ir`-jében; FELADATOK nem változott (8. pont) |
| 7/1 delta-sorok | OK | naplo:304–338 | 33 delta-sor, mind igen/nem + indok; a KONZISZTENCIA_20261009 1.16 (6. pont) a 20. sorban, és a diffben átvezetve (ATALAKITASI 13.4 :1004–1006; MUNKATERV :168) |
| 7/2 átírt szakaszok = diff | ELTÉRÉS | naplo:371; ADATVAGYON:16, :916 | `git diff -U0 2108fc67..6e2336d5`: minden hunk szerepel a listában, de az ADATVAGYON :781 (18.1, ATALAKITASI 4.7 sor) és :812 (18.4, N-F34b) „17.2” alatt áll |
| 7/3 hivatkozás minden átírt állításnál | OK | — | diff-olvasás: minden csere mellett DT/N/#-hivatkozás |
| 7/4 nem maradt megfordított állítás | ELTÉRÉS | ATALAKITASI:845 | a 9. kockázat-tábla TAHOT-sora jelen időben: „van egy … rés — Jób 40:1-5 és a teljes Jób 41. fejezet”; az F84/DT86 megfordította, a D23/N13 sor jelölést kapott, ez nem |
| 7/4 (DT56) | ELTÉRÉS | ADATVAGYON:13, :738 | „a 7. adag a DT56 küszöbével”; DONTESEK DT56: „A 7. adag (86%) indulhat; a 8. adagtól (ma 78%) a küszöb dönt” |
| 7/5 döntésnapló- és kiindulási sor | OK | ATALAKITASI:4; MUNKATERV:209; ADATVAGYON:5, :916; VIBE:172 | diff; megjegyzés: a kiindulás `78844919`, a tényleges alap `1f420a7c` (csak a DT87–89 számkiosztás) |
| 7/6 a többi rész bájtazonos | OK | — | `git diff --numstat --ignore-cr-at-eol` = `--numstat` (29/27, 11/10, 2/0, 1/1, 64/57, 4/3, 146/5) → nincs sorvég-változás; a napló hunkjai `@@ -290,0 +291,140`, `-293/-295/-297` (csak hozzáfűzés + a „Nyitott” szakasz); a CR-t tartalmazó diffsorok száma 0 |
| 7/7 terv → feladat (3b) | OK (megjegyzés) | naplo:396–407; ADATVAGYON:935 | minden résnek van kimenete; a 6. lépcsőnél a „feladat a döntéskor nyílik, /befogad” DT nélküli új állítás |
| 7/7 `feladatok.py ellenoriz` | NEM ELLENŐRIZHETŐ | — | a parancs kívül esik a megengedett Bash-körön; a napló „0 hiba (104 brief)” állítása nincs igazolva |
| 4./3b ADATVAGYON 21. 6. lépcső | OK (megjegyzés) | ADATVAGYON:935 | a brief 3b „feltételes” jelölést gépiesnek nevez; az eredeti oszlop („felhasználó dönt”) alátámasztja; a SZPA-auditra a DT77 (13) |
| 4. ATALAKITASI 13.3 | ELTÉRÉS | ATALAKITASI:996; ADATVAGYON:843 | DONTESEK DT80: „az `adatosítva` szerepnél … hivatkozás kell (S4), nem üres blokk”; DT81 (1) és DT82 (c): „a 7. szerep (SECE): l. 2/b”; DT83: „H7121 = jelölt üres blokk, mutató … BDB 2.c” → a 13.3-ból hiányzik a hivatkozás-ág, és a „mutatóval a #9-re” nem általános |
| 4. ATALAKITASI 13.4 | OK | ATALAKITASI:1004–1006 | FELADATOK :18 (#23 ⏸, fugg #32, #78 kész), Kész :118 (#78); DT84 🟡 |
| 4. MUNKATERV 4a sorai | OK (megjegyzés) | MUNKATERV:79–149 | FELADATOK :16–31, :39–47, :55–62 összevetve: 16 + 9 + 8 = 33 nyitott sor, az állapotok és függések egyeznek; kivétel a #52 (▶ fut vs ⬜; a napló :298 indokolja) |
| 4. #22 PR-számok | OK | MUNKATERV:84 | `git log --merges 7dd0183..78844919`: #249 (wonderful-einstein; az F22.Jer és az Ézs-döntések a `cdf947ea^1..^2`-ben), #253 f22-1kron, #255 f22-2kron, #259 f22-ez; FELADATOK :119 (#77: „az Ézs és a Jer API-n lefutott, PR #249”); „a Bír később” = DT57 szövege |
| 4. Kész-lista PR-számai | OK (megjegyzés) | MUNKATERV:185 | #240, #242, #247, #227, #244, #236, #249, #254/#256, #250, #260, #262 = a merge-listával; #71 → F71 `pr: 226` (merge `4ded4eb`), #73 → merge `4afc717` = PR #231; ezek kimaradtak |
| 4. Összesítés | OK | MUNKATERV:188 | 3 + 5 + 5 + 3 + 17 = 33; a 17 „marad” megszámolva (#7, 23, 27, 54, 55, 9, 10, 12, 13, 36, 70, 45, 50, 67, 69, 74, 75) |
| 4. ADATVAGYON 18.5 „13 szerep, 26 sor” | OK | ADATVAGYON:838 | Grep `.` count `adat/szotar_szerepek.tsv` = 28 (1 megjegyzés + 1 fejléc + 26 adatsor) |
| 4. ADATVAGYON 19. terminologia-pipa | OK | ADATVAGYON:878 | Grep `^olvas:.*terminologia` F38_BDB_FORDITAS_BRIEF.md: 1 |
| 4. DT-M8 (d) | OK | MUNKATERV:7, 30, 42 | F11_MIGRACIO_BRIEF.md:12 `olvas: [ADATVAGYON_TERV.md, MUNKATERV.md, …]` |
| 4. ADATVAGYON 22.5 / SEMA 4 | ELTÉRÉS | ADATVAGYON:1003; adat/SEMA.md:1229 | a SEMA 4 ma is: „Jób 40:1-5 és a teljes Jób 41. fejezet hiányzik”; a CLAUDE.md az ellenkezőjét írja → két forrás ellentmond (brief 6.2: napló + ⛔), a napló 27. sora „nem” |
| 6. ⛔ alapfeltevés | OK | naplo:298 | nincs alapfeltevés-fordítás; a D23 DT-be ment |
| 6. VIBE-korlát | OK (megjegyzés) | VIBE:7, 122, 126 | az 5. szakaszban csak szám- és névcsere; az 1. szakasz cseréje a 6. pont betűje szerint nem engedett (precedens: v4) |
| 3b DT90 | OK (megjegyzés) | DONTESEK:165 | 8 oszlop (az `awk -F'|'` NF = 10 = DT89); 🟡, a Döntés üres; a helyőrző a DT-F52g (→ DT78, `cfa45d0f`) után következik; CLAUDE.md „Adat-tár” és naplok/F84_jelentes.md :50, :89, :97 egyezik; a `lekerdez.py:12, :375` `TAHOT-teljes`-t ír (Grep); a SEMA :1232–1235 indoka nincs idézve |
| 3b DT91 | OK | DONTESEK:166 | a brief 6. pontja miatt valóban döntés |
| 8. Nincs benne | OK | — | FELADATOK változatlan; a DONTESEK-be csak 2 új sor (`git diff --numstat`: 2/0) |
| A1 | OK | naplo:409–417 | a `manual` és a lekérdezés szétválasztva |
| A2 | OK | naplo:435–440 | DT90/i 🟡, DT84 🟡 (DONTESEK:159), a #22 Jób/Péld nyitott (FELADATOK:17) |
| A3–A5 | OK (nem alkalmazható) | — | nincs tanulmány, párhuzam vagy tanító a diffben |
| A6 | OK | — | futtat.py: E12–E15 0 találat |
| CI | NEM ELLENŐRIZHETŐ (egyezés) / OK (saját futás) | — | nem kaptam CI-jelentést, így az egyezés nem vethető össze; `python eszkozok/ellenorzes/futtat.py --valtozott <7 fájl> --diff-alap 2108fc67 --diff-fej 6e2336d5`: E2–E16, E19, E20, E26 0 találat; E25 3 (CLAUDE.md:33, MUNKAMENET.md:67, :181) és E27 33 jelentés/figyelmeztetés, mind a diffen kívüli fájlokban; HIBA nincs |
| L1 törölt sorok | OK | — | numstat: ADATVAGYON 27, ATALAKITASI 10, VIBE 3, brief 1 – mind cseresor; MUNKATERV 57: cseresorok + 4a-sorok mozgatása (#40, #64, #66 → Kész; #30 → Folyamat; #61, #62 → 1. fázis) + 1 ábrasor (SZPA_AUDIT); napló 5 („Nyitott” szakasz) |
| L2 kulcstartomány | OK | — | FELADATOK nyitott sorai: 33/33 a 4a-ban |
| L3 nulla-diff hatóköre | OK | naplo:1–290 | a napló 1–2. futása bájtazonos; a „Nyitott” szakasz szándékosan új; a tervdokumentumokban nincs sorvég-változás; nem vonatkozik a tartalmi cserékre |
| L4 .tsv Δ | OK | — | `git diff --stat main 6e2336d5 -- 'adat/*.tsv' 'konkordancia/*.tsv'`: üres → minden adat/ és konkordancia/ tábla Δ = 0, bontási napló nem kell |
| L5 ⛔ pontok | ELTÉRÉS (= a 22.5-sor) | — | a forrás-ellentmondás ⛔-ja (6.2) elmaradt; a többi ⛔ teljesült |

Eltérések súlyosság szerint: (1) ATALAKITASI:845, megfordított TAHOT-állítás; (2) SEMA 4 ↔ CLAUDE.md ellentmondás ⛔ nélkül (ADATVAGYON:1003); (3) 13.3/18.5 hiányos összefoglalás; (4) ADATVAGYON DT56-pontatlanság (:13, :738); (5) a napló 3.2 szakasz-besorolása (18.1/18.4 → „17.2”).
