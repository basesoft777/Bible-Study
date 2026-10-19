# F11 zárónapló — az ISTENTISZT-001 migrációja, 1. lépcső (S, R, M1–M6)

*2026-10-19 · ág: `claude/f11-m5` (PR #417, draft, nem mergelt); előzmények a main-en: PR #393 (S, M1–M2), PR #408 (R, M3–M4) · modell: claude-opus-5-5 · a brief `allapot`-a `megallt`, nem `lezarva`: az M7, a T1–T3 és a DT-F11c még nyitott.*

- **S (DT183):** a `kapcsolatok.tsv` `indoklas` oszlopa önálló séma-tételként (F11.S1–S3), ellenőrzés: `naplok/ELLENOR_F11_S.md` (ELTÉRÉS, 2; javítva).
- **M1–M4 + R:** a leképezési tábla (`naplok/F11_szetvalasztas_ISTENTISZT-001.tsv`), a generátor-képességek (DT202), az adatrés-renderelő (DT216), a szétválasztás (DT217–DT219). Mérés: `naplok/F11_M4_meres.md`, a HAMART-001 N0 zöld, CI-ben csak az E16 (a PR címe).
- **M5:** az ISTENTISZT-001 törzscikke archiválva a felhasználó szabálya szerint (törlés helyett): `archivum/ISTENTISZT-001/ISTENTISZT-001_torzscikk_regi.md`, DT215 fejléccel, bájtazonos tartalommal. Az éles lap újragenerálva, felkerült az E28-listára (DT243 a, 3 sor).
- **M6:** `naplok/ELLENOR_F11_M.md` 11. szakasz (ELTÉRÉS, 2 alacsony). A javítókör 1. köre (F11.M6.1–M6.4): az N-F09h elavult mondata törölve; az archív törzscikk átnevezve az alapnév-ütközés miatt (DT244 a, felhasználó, 2026-10-19). Újraellenőrzés: `naplok/ELLENOR_F11_M_2.md` **TISZTA**.
- **Ellenőrzés (e5df5ca6):** `feladatok.py ellenoriz` 141 brief, 0 hiba; `ellenorzes/futtat.py` diff-módban (`fd6ea4e3..d6ec2901`, `[ELLENŐRZŐ]` PR-címmel): HIBA 0, E28 0 (1 migrált nézet), E29 0.
- **Elfogadási feltételek (4. szakasz):** 1–4. és 6. teljesül (l. fent és az M4-mérés). Az 5. **nem**: a `Tartalmi visszaírás` szabály a két élő sablonban ma is felfüggesztő sorral áll (`2_…:252`, `4_…:447`), mert a T1–T2 nem futott. A 7. ezzel a naplóval teljesül; a DT74 (3) befagyasztás oldása a PR #417 merge-éhez kötött.
- **Hátra (a felhasználó döntései):** a PR #417 merge-e; az M7 (a tanítói sor hivatkozássá alakítása) külön kérésre; a T1–T3 (sablon-átírás; a T3 előtt a DT-F11b); a DT-F11c (a 2. lépcső, 6 motívum ütemezése: ebben a feladatban vagy külön briefben); az N-F11a–e befogadása a merge után, `/befogad` útján.
