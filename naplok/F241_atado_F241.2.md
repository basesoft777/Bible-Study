# F241 átadó — F241.2 → F241.3

*2026-11-23 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/f241a-kiadasi-ut` (A szelet), PR #841 · a döntések: `naplok/F241_dontesek.md` (D1–D8, változatlan), előbb azt olvasd, és a fájl aktuális állapotát hajtsd végre.*

## Állapot

- **F241.1 kész** (`89315956`, `21488d0c`): a kiadás mód kapuja (GK-27) a `lap_commit`-ból és a kézi bemenetek lenyomatából (`lapgen/bemenet/jovahagyas.py`, `konfig.JOVAHAGYAS_BEMENETEK`); FRISS / CSAK_GENERALT (átmegy) / ELAVULT, NINCS_ATNEZES, NINCS_LAP (BUKÁS). Kiadás módban a mondat „a szerző jóváhagyta” (`kolofon.jovahagyas.friss`). A mérce B66 hash-sora frissítve (regresszió RENDBEN).
- **F241.2 kész** (`5efecab2`, `d06a1eef`): `--cel lexikon` = új generátor, `--cel lexikon_regi` = régi; motívumonkénti átállás: `general.py` `ATALLT_MOTIVUMOK` (üres) — a commitolt, át nem állt lap a régi generátorral (visszaút), lap nélküli/átállt motívum az újjal. A G01 parancsa `--mod {mod}`: kiadott lap kiadás módban.
- Részletek, mérések: `naplok/F241_jelentes.md`, „F241.1” és „F241.2”.
- **Valós állapot (kiadás mód):** ISTENTISZT-001 → ELAVULT (átnézés `ee33a860`, 11.04; a 2. kiadáshoz új nézés kell — az F241.7 ⛔-je), HAMART-001 → NINCS_ATNEZES (a B szelet HAMART-kiadásához átnézés-sor kell).
- Nyitott ⛔ nincs. Az integrátornak jelezve: a `JOVAHAGYAS_BEMENETEK` halmaza technikai döntés (a jelentés F241.1), szólhat, ha a jóváhagyás tárgyát másként érti.

## Az F241.7-re hagyott tételek (ebből a két lépésből)

- Az új generátor ma csak repón kívülre ír (`lapgen/fo.futtat`); a `lexikon/` végleges helyére írás (és hogy az olvasási napló ne kerüljön a `lexikon/` alá) az F241.7 dolga.
- Az ISTENTISZT-001 kiadási commitjában: `ATALLT_MOTIVUMOK` += ISTENTISZT-001; a befagyasztás feloldása; az átnézés-sor (`lap_atnezesek.tsv`) a szerkesztő szavával a 2. kiadás lapváltozatára.
- A G02 `bemenetek` listája (`B03;B04;B05;B06;B07;B56`) a régi generátor KIZARASOK-olvasásai; az átálláskor az új generátor olvasási naplójával összevetni.

## Következő: F241.3 — lapszöveg-kapuk a modellre (N243 (3)) + N-F239b

A brief 4. pontja szerint: `olvasoi_kapu.py`, az `ellenoriz.py` lapszöveg-szabályai, E38, E39, HN-17 („3. LXX” előtag) a modellen; a fogyasztóikkal egy commitban. Az N-F239b (a „Szakirodalom” sor dőlt, eredeti nyelvű műcíme ne legyen ANGOL/MUNKASZO-bukás) ugyanitt. Az `ellenoriz.py` javítási megjegyzéseit (`--cel lexikon --id <ID> --ir`) itt nézd újra. Nagy lépés: valószínűleg F241.3a/b alszeletekre bontandó.

## Szabályok, amelyek ezen a szeleten élnek

- Egyszerre egy lapgen-futás; a TEREMT-001 U5-csomagja (local_4c553509) is lapgent futtat: futtatás előtt `python.exe`-lista; más session folyamatát soha nem állítod le.
- A worktree-ben a `claude/f241a-kiadasi-ut` ág egy korábbi worktree-ben (`xenodochial-tesla-3c2679`) ki van csekkolva: helyi ágon dolgozz, és `git push origin HEAD:claude/f241a-kiadasi-ut`.
- Heredocban a `\` egy `\`-re csökkenhet: Python-szkriptet a Write eszközzel írj fájlba.
- Kontextus-plafon: kb. 150 ezer token; lépéshatáron átadó.
- Az A szelet végén egy `fuggetlen-ellenor` (F241.6) és legfeljebb egy javítókör, a teljes `push_elott` a PR előtt.
