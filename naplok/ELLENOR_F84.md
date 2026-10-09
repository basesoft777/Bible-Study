ELTÉRÉS: 4 tétel

# ELLENOR_F84 — F84_TAHOT_JOB41_BRIEF.md · 6868d7c..HEAD (0d4bbde)

*A `fuggetlen-ellenor` jelentése. Az ellenőr fájlíró eszköz nélkül futott, a szöveget az orkesztrátor mentette változatlanul. Az ellenőr szkriptet nem futtatott, `git diff`-fel, `lekerdez.py`-vel, `futtat.py`-vel és Grep/Read-olvasással dolgozott.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| G (F84.2) 332 sor, jó helyen | OK | `konkordancia/TAHOT_kivonat.tsv:289099–289430` | `git diff --numstat 6868d7c..HEAD` → `332 0 konkordancia/TAHOT_kivonat.tsv`. `git diff -U0 …` → egyetlen hunk `@@ -289098,0 +289099,332 @@`, előtte `Jób 40:24 H0639`, utána `Jób 42:1 H9001`. Grep `^Jób 41:` → 332; Grep `^` → 469 301 sor (469 300 adat + fejléc). |
| Nulla-diff hatóköre (kötelező 3.) | OK | uo. | A meglévő 468 968 sor bájtazonos: a diffben nincs `-` sor, és a hunk egyetlen beszúrás. Nem terjed ki a többi fájlra, sem a beszúrt sorok sorvégére; ez utóbbit külön néztem: Grep `\r` a TAHOT_kivonat.tsv-n → 0 találat. A záró újsor megmaradt. |
| G (F84.2) a nyitott fájl | OK | `konkordancia/TAHOT_kivonat_nyitott_esetek.tsv:1` | `git diff -U0 … nyitott` → `@@ -2,332 +1,0 @@`, tehát a 2–333. sor törölve, a fejléc maradt. A 332 törölt sor mind `Job.41.n` kulcsú és `ADATMINOSEGI_GYANU` státuszú. |
| G (F84.2) adatoszlopok, kulcs | OK (szemrevételezés) | uo. | A 332 törölt sor 4–9. oszlopa soronként, sorrendben egyezik a 332 beszúrt sor 1–6. oszlopával (két `git diff -U0` kimenet). A kulcs mindenhol `Job.41.n` → `Jób 41:n`. A bájtszintű egyezést gépileg nem mértem. |
| G (F84.1) Macula-szúrópróba | OK | `konkordancia/Macula_heber_Job.tsv:11973–11982, 12057–12066, 12216–12223, 12298–12307` | A nem-H9xxx Strong-számok egyeznek: MT 40:25 = K 41:1; MT 41:1 = K 41:9; MT 41:17 = K 41:25 (a Macula H4480 = TAHOT H9006 מִ); MT 41:26 = K 41:34. |
| G lekérdezés H3882 | OK | — | `lekerdez.py scan H3882 --szakasz "Jób 41:1-41:34"` → Jób 41:1; `proveniencia: scope=range:Jób 41:1-41:34 \| forras=TAHOT_kivonat.tsv \| strong=H3882 \| n=1 \| ts=2026-10-09T06:22Z`. A teljes `scan H3882` → Jób 3:8, 41:1, Zsolt 74:14, 104:26, Ézs 27:1 (n=5). |
| G Károli-szöveg, 40 = 19, 41 = 34 | OK | — | `lekerdez.py karoli`: Jób 40:19 van, 40:20 nincs; 41:34 van, 41:35 nincs; 41:25 van (ts=2026-10-09T06:22Z). |
| D (DT-F84a (a) 1, (b) 1) végrehajtás | OK | `DONTESEK.md:161` | (a): a sorok törlődtek, a fejléc maradt. (b): a 41:25 jelölés nélkül bent van (8 sor). |
| D (DT-F84a) a döntés forrása | NEM ELLENŐRIZHETŐ | `DONTESEK.md:161` | A repóból nem dönthető el, hogy a döntést valóban a felhasználó hozta-e. |
| ⛔ 1 betartva | OK | — | Az F84.1 (4f3edc7) táblát nem írt; táblát először az F84.2 (1c3720c) írt. |
| G (F84.2) szkript: csv nélkül, UTF-8 őr | OK | `eszkozok/tahot_job41_potlas.py:24–31, 51, 72` | Nincs `import csv`; az őr az importok után; `split`/`'\t'.join`; CR-t elutasít. |
| G (F84.2) írás előtti összevetés | ELTÉRÉS (alacsony) | `eszkozok/tahot_job41_potlas.py:87–90` | Az `uj_fo`-t ugyanazokból a szeletekből építi, amelyekkel összeveti; az őr nem bukhat el. Az eredményt a git diff (+332/−0) utólag igazolja. |
| G (F84.3) generátor-megjegyzés | OK | `eszkozok/tahot_karoli_kulcs_generalas.py:51–61` | Csak megjegyzés; döntés-érték változatlan; [javaslat] jelölve. |
| G (F84.3) CLAUDE.md mondat | OK, részben NEM ELLENŐRIZHETŐ | `CLAUDE.md:107` | Jób 40:1–5 = TAHOT 39:34–38 (44 sor); a Jób 40 MT-kulcsú (40:6–24); a kézi tábla 19 Jób-sor. Nem ellenőrizhető: „fejezet-szinten nincs hiány” (a szkriptet nem futtattam). |
| G (F84.3) README | ELTÉRÉS (alacsony) | `konkordancia/TAHOT_TAGNT_README.md:308–309, 244` | A Méret táblázat elavult (468 232 / 1 068); a 244. sor „nincs Jób-sor”, pedig a fájl teljesen üres. |
| G (F84.3) NYITOTT_FELADATOK | OK / NEM ELLENŐRIZHETŐ | `NYITOTT_FELADATOK.md:679–682` | Az N-F83a és N-F34b lezárása igaz. Nem ellenőrizhető: a „vers-szintű rések … nem állnak fenn” (az F2 fejezet-szintű volt). |
| Helyőrzők | OK | diff | Csak `DT-F84a`, `N-F83a`, `N-F34b`; E26: 0 találat. |
| Brief fejléc | ELTÉRÉS (alacsony) | `F84_TAHOT_JOB41_BRIEF.md:11` | A `kovetkezo` még „Hátra: F84.3 …”. |
| Lefelé ható következmény (#22) | ELTÉRÉS (közepes) | `f22/versmegfeleltetes.tsv:78–103` | Generált fájl (`versbeosztas.py`, ts=2026-10-02); 26 Jób 41-es vers `nincs_eredeti`. Az F84 után elavult, nem generálták újra; a brief „a #22 a Jóbot egy menetben futtathatja” állítása így nem igazolt. |
| Proveniencia a jelentésben | OK (megjegyzéssel) | `naplok/F84_jelentes.md` | A 4–5. szakasznak nincs proveniencia-sora; a számokat az ellenőr igazolta. Az F84.1 mérőszkriptjei nincsenek verziózva. |
| A1 | OK | `naplok/F84_jelentes.md` | A H4480-értelmezés jelölve; az adat igazolja (TAHOT 41:25: H9006 מִ). |
| A2 | OK | `NYITOTT_FELADATOK.md` | — |
| A3, A4, A5 | nem alkalmazható | — | Nincs tanulmány, párhuzam, tanító. |
| A6 / E12–E15 | OK | — | `futtat.py --valtozott … --diff-alap 6868d7c --diff-fej HEAD` → E12–E15: 0; E25: 3 és E27: 33 találat, F84-et nem érintő régi tételek. |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | — | — |
| Kötelező 1. törölt sorok | OK | — | 332 nyitott sor (Job.41.1–34); más törlés nincs. |
| Kötelező 2. kulcstartomány | OK | — | Jób 41:1–34 folytonos. |
| Kötelező 4. táblasor-Δ | OK | numstat | `TAHOT_kivonat.tsv` +332 (468 968 → 469 300); nyitott −332 (332 → 0). |

**Eltérések súlyossági sorrendben:** (1) `f22/versmegfeleltetes.tsv` elavult Jób 41 `nincs_eredeti` sorai — közepes; (2) README 308–309, 244 — alacsony; (3) brief `kovetkezo` — alacsony; (4) `tahot_job41_potlas.py:89` hatástalan őr — alacsony.

**Utóirat (orkesztrátor):** a (2)–(4) javítása az F84.4 commitban; az (1) nincs az F84 `ir`-jében (a #22 fájlja), átadva a #22-nek (`naplok/F84_jelentes.md`, „Következmény a #22-re”).
