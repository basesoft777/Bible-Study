# F241 átadó — F241.0 → F241.1

*2026-11-23 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/f241a-kiadasi-ut` (A szelet) · a döntések: `naplok/F241_dontesek.md` (D1–D8), előbb azt olvasd, és a fájl aktuális állapotát hajtsd végre.*

## Állapot

- Az F241.0 kész: az előfeltételek igazolva (#809, #810, #839 a main-en; az integrátor jele: D8), a #820 N-tételei beolvasva (N-F239a → F241.8, N-F239b → F241.3; az N-F239c a #820 U5-csomagjából még jön), a függések változatlanok (nincs `KOR`), a `lexikon_general` 40 importáló fogyasztója mind az `ir`-ben. Részletek: `naplok/F241_jelentes.md`, „F241.0”.
- A fejléc: `allapot: fut`, `ag: claude/f241a-kiadasi-ut`; a `pr` mezőt az A szelet draft PR-ja tölti ki.
- Nyitott ⛔ nincs. Az integrátornak jelezve: a #231 briefje a #810 merge-e után is `fut`, ezért a 241-gyel kizárás-listán áll (`teszt_olvasoi_merce.py`).

## Következő: F241.1 — kiadás mód és frissesség (N221; DT933 (1); GK-27, T9)

A brief 4. pontja szerint. Olvasd: `eszkozok/lapgen/szamitas/kolofon.py` (`kapu`), a `teszt_kolofon.py` `Jovahagyas` osztályát, az `adat/lap_atnezesek.tsv` sémáját (SEMA 2.48), a `naplok/F218_jelentes.md`-ből csak a GK-27/T9 és az N-F218w helyét (grep). Mindhárom ág teszttel: egyező `lap_commit`; csak generált blokk változott (→ változásjegyzék-sor, nem új nézés); kézi próza vagy adat változott (→ új nézés, BUKÁS kiadás módban).

## Szabályok, amelyek ezen a szeleten élnek

- Egyszerre egy lapgen-futás; a TEREMT-001 U5-csomagja (local_4c553509) is lapgent futtat: futtatás előtt `python.exe`-lista, ütközésnél várni; más session folyamatát soha nem állítod le.
- Kontextus-plafon: kb. 150–200 ezer token; minden lépéshatáron átadó jegyzet `naplok/F241_atado_<lépés>.md`.
- Az A szelet végén egy `fuggetlen-ellenor` (F241.6) és legfeljebb egy javítókör, a teljes `push_elott` a PR előtt.
