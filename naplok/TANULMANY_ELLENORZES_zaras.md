# F37 zárójelentés — TANULMANY_ELLENORZES

- Ág: `claude/tanulmany-ellenorzes`, F37.1–F37.12. A main (`07fcb39`) összefésülve, konfliktus nélkül (F37.11).
- T0: egyik ⛔-feltétel sem teljesült (`naplok/T0_felmeres.md`). T1: „Bővített sablon” → „Tanulmány sablon”, az alap sablon elavult-jelölést kapott. T2 elmaradt (DT-F37-9).
- T3: új szabály az E20 (kötelező szakaszok, a sablonból olvasva). Az E13, E8, E9 és E12 hatóköre tanulmányokra bővült (DT-F37-8). Új jelentés mód: `naplok/TANULMANY_AUDIT.md`, 23 tanulmány, 433 találat, nem bukik.
- T4: tanulmány-ellenőrzőlista a `fuggetlen-ellenor.md` végén, gépi segédszkripttel (`tanulmany_ellenorzes.py`). T5: ügynöki audit (`naplok/TANULMANY_AUDIT_ugynok.md`): 4 igazolt Strong-eltérés, 3 ⚠️ képviselő nélkül vagy csonka hivatkozással, 9 Sod csak részben levezethető, 5 ⚠️-vita-eset.
- Döntések: DT61 (az öt vita-eset nem ⛔, a javító utófeladat elején dől el), DT62 (a „valódi ⚠️-vita” meghatározása két pontosítással). Mindkettő ✅.
- T6: utófeladat-javaslat (`naplok/TANULMANY_ELLENORZES_utofeladat.md`): egy gépi menet és 16 tanulmányonkénti tartalmi menet. **`/befogad`-ra vár.** A menet eltérései ugyanott.
- Tesztek: `test_szabalyok.py` 74 OK, `test_tanulmany.py` 32 OK. CI a workflow szerint (`[ELLENŐRZŐ]` címmel): 0 HIBA.
- Független ellenőrzés: 1. kör `naplok/ELLENOR_TANULMANY_ELLENORZES.md` (ELTÉRÉS 6, mind javítva: F37.9–F37.10), 2. kör `naplok/ELLENOR_TANULMANY_ELLENORZES_2.md` (ELTÉRÉS 1, javítva: F37.12).
- Az orkesztrátor az 1. körben hibás base-t adott át (a frissítetlen helyi `main`-ből); az ellenőr a helyes merge-base-en dolgozott.
- Utófeladat-jelöltek (nem befogadva): (1) a `kozos.tanulmany_fajl_e` nem zárja ki a `.claude/worktrees/` alatti, git által nem követett másolatokat, ezért a helyi `futtat.py --teljes` ezeken is E20/E12/E13 találatot ad (a CI-t nem érinti); (2) a T4 7. pontjának részleges bekapcsolása az 1–5Móz-ra és Józsuéra (DT-F37-4).
