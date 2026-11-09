ELTÉRÉS: 4 tétel

# ELLENOR_F166 — F166_KAROLI_IDEZET_SZABALY_BRIEF.md

*A `fuggetlen-ellenor` subagent jelentése (2026-11-09). Az ellenőr fájlt nem tudott írni; a szöveget az orkesztráló session másolta ide, tartalmi változtatás nélkül, a táblázatot tömörítve.*

**Vizsgált tartományok:** PR #631 `9a12edf..c4494d5`; a zárás `origin/main...HEAD` (`5171b7fd`).
**Modell:** az ellenőr tényleges modellje `claude-opus-5-5`, a saját subagent-fájlja szerint kért `opus`: egyezik. A diffben nincs `.tsv`, `modell` mező sincs.

| pont | eredmény | fájl:sor | indok / parancs |
|---|---|---|---|
| Hatókör (zárás) | OK | – | `git diff --stat origin/main...HEAD`: 3 fájl (brief, `naplok/F166_zaras.md`, `nyitott/uj/f166-zaras.md`); a generált blokkhoz nem nyúlt. |
| ⛔ 3. lépés, 1. pont | **ELTÉRÉS** | `dontesek/uj/jolly-sutherland-85d152.md:1` | `git log --reverse 9a12edf..c4494d5`: f4d72906 18:05:29 (helyőrző, 🟡, már „a javaslat (a) már megvalósítva az E34-ben”), a682ba9d 18:05:30 (F166.2), 6c44e06e 18:07:21 (🟢). A ⛔ tartalmi döntés előtt a menet nem állt meg. |
| „gátló” szabály | OK (döntéssel) | `eszkozok/ellenorzes/szabalyok.py` (E34) | HIBA a kiadott motívumon, FIGYELMEZTETÉS a többin: DT614 (a), a 🟢 döntés fedi. |
| SEMA 2.50 szövege | **ELTÉRÉS** | `adat/SEMA.md:1940` | A cím „az `ellenoriz.py` 34. szabálya”, de az `eszkozok/ellenoriz.py`-ban nincs `szabaly34` (32, 33, 35–39 van). Az E34 a CI szabálykészletében (`szabalyok.py`) él; a megnevezés téves. |
| SEMA 2.50 kétszer | OK | `adat/SEMA.md:1940`, `:1953` | Igaz; N-F166a nyitva (`nyitott/uj/f166-zaras.md:1`). |
| A 46 hely listája jelentésben | **ELTÉRÉS** | `naplok/F166_zaras.md:6-9` | A PR #631 diffjében nincs jelentésfájl; a lista csak a zárásban jelent meg (41 hellyel). A brief 46-ot, a DT 45-öt mond; a 46 → 45 különbséget a repóban semmi nem magyarázza. A 45 → 41 a `b6807740` (F123.HAMART3.3) commitra mutat, létezik. A #631 idejének 45-ös száma nem ellenőrizhető. |
| 41 hely a main-en | OK | `adat/elofordulasok.tsv` | `futtat.py --valtozott naplok/F166_zaras.md --diff-alap origin/main --diff-fej HEAD --minta 100`: `E34 (JELENTES: 41)`, KIRALY 5, TEREMT 28, MENNY 1, HODIT 7, HAMART 0; tételesen egyezik a zárójelentéssel. |
| Hamis bukás | OK | `adat/kiadasok.tsv:3-7` | A kiadott motívumokon (ISTENTISZT-001, ALVIL-001, ANTROP-001) nincs HIBA. Szúrópróba (`lekerdez.py karoli`): Zsolt 76:3, Zsolt 42:8, 1Móz 6:4, Jón 2:6, Ez 31:4, 5Móz 3:13 — mind valódi eltérés. |
| ISTENTISZT A1–A5 a tesztben | OK (korláttal) | `test_szabalyok.py` (`test_negativ_eltero_szo_kihirdetem_tipus`) | A szinonimacserét fogja (kitalált Károli-szöveggel); a valós A1–A5 szórendcseréjére („segítségül hívom az Úr nevét” → „az Úrnak nevét segítségül hívám”, `2f39c153`) nincs teszt, a sorrendi illesztés logikailag megfogná. |
| 1Móz 7:23 nincs jelezve | OK | `adat/elofordulasok.tsv:219` | Szó szerinti részlet, az E34 nem jelzi; döntés: lektori tétel. |
| „kézi 1/a-próza” lefedése | OK | `eszkozok/lexikon_general.py:908-919` | Az 1/a-blokk egyetlen útja a `kapcsolodas` mezőből jön (`olvasoi_indok(kapcsolodas)`); a régi kézi 1/a archív. |
| TSV-olvasás | OK | `szabalyok.py` `_e34_karoli`; `kozos.py:145` | `split('\t')`; `csv` nincs. |
| `ellenoriz.py` és tesztek | NEM ELLENŐRIZHETŐ (ellenőri korlát) | – | Az ellenőr nem futtathatta; az E34 függvény az élő adaton lefutott. |
| Zárás: proveniencia | **ELTÉRÉS** | `naplok/F166_zaras.md:5` | A `scope=… \| forras=…e34_karoli_idezet \| ts=…` sort sem az E34, sem a `futtat.py` nem adja ki — kézzel készült, `manual` lenne a helyes. A „11/11 zöld” (6. sor) mellől hiányzik a parancs és a proveniencia. |
| Silent skip | OK (megjegyzéssel) | `szabalyok.py` (`if not vers: continue`) | A fel nem oldható igehelyű sor jelzés nélkül kimarad; ma nincs érintett sor. |
| CI (saját futtatás) | OK | – | `futtat.py` a #631 négy fájljára a PR-címmel, és a zárás három fájljára: kilépés 0; csak JELENTES (E25 3, E27 43, E34 41). |
| A1–A6, F37 T4 | OK / nem érintett | – | – |
| Ellenőrzőlista 1–4 | OK | – | #631: +201/−0 sor; zárás: +21/−3 (fejléc, döntésnapló); adattábla Δ = 0. |
| Ellenőrzőlista 5 (⛔) | **ELTÉRÉS** | – | Ugyanaz, mint a ⛔-sor. |

**Az ELTÉRÉS-ek súlyosság szerint:**
1. **A ⛔ megsértése** (#631): a megvalósítás 18:05:30, a DT-F166a megerősítése 18:07:21; a 🟡 sor már „megvalósítva” állapotot írt.
2. **Téves megnevezés a SEMA 2.50 címében**: „az `ellenoriz.py` 34. szabálya” — az E34 a `szabalyok.py` CI-szabálya, a `python eszkozok/ellenoriz.py` nem futtatja.
3. **A találati lista nem a #631-ben készült el**, és a brief 46 ↔ DT 45 különbsége a repóban nincs magyarázva.
4. **Kézzel írt proveniencia a zárásban**, `manual` jelölés nélkül; a „11/11 zöld” mellett nincs parancs.

*Az orkesztráló session megjegyzései (nem az ellenőré):* a 3. ponthoz — a #631 menete a 45 helyes listát és a 46 → 45 magyarázatot (HAMART-001 Ézs 24:5-6: az adat szó szerinti Károli, a lap 1/a blokkja tartománynál csak az első verset mutatta) a PR #631 leírásába és a session-csoport megosztott jegyzetmappájába írta, a repóba nem. A tesztkört a session futtatta (2026-11-09, `5171b7fd`): `test_szabalyok.py` 26 hiba, mind az E27Teszt (`ValueError: path is on mount 'E:', start on mount 'C:'`, Windows-worktree), a többi teszt és az `ellenoriz.py` (SÉRTÉS: 0) zöld.
