# F241 átadó — F241.5 → F241.5b

*2026-11-24 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/f241a-kiadasi-ut` (A szelet), PR #841 · a döntések: `naplok/F241_dontesek.md` (D1–D14), előbb azt olvasd, és a fájl aktuális állapotát hajtsd végre.*

## Állapot

- **D13** (`7be53bbb`): az F241.3 leletei (ISTENTISZT-001: MINTA 91, LISTA_NEVELO 9, KONYV 2 „Zef”, MUNKASZO 1; HAMART-001: 2 BUKÁS és az `ellenoriz` 11. szabályának eltérése) az F241.5b bemenete; a MINTA-kapu szigorú, kimeneti regex-csere nem megoldás, a `jeloltek.tsv` indoklása döntési nyom (nem íródik át olvasói célból); a 91 hely forrásának mérése és a javaslat ⛔ az integrátorhoz a javítás előtt.
- **F241.4 kész** (`fea96302` D14, `23f48a83`, `cd835845`): licenckapu a Kolofonban (mondatszint + a forrás neve a forrástáblában, tisztázatlan licencnél a GK-28 mondatával), a bővített `KOLOFON_MEGJELOLES`, a MEK-sor megjegyzése a `megjegyzes` oszlopba; a mérce B01 hash-sora és 10 engedélysor (`S8D-LICENC-*`).
- **F241.5 kész** (`465f9c71`, `5fe3db7c`): 32 fordítássor (10 tW-cím, 22 doménnév), az ISTENTISZT-001 új lapja 0 „fordításra vár” jellel; a mérce B14 hash-sora.
- Részletek, mérések: `naplok/F241_jelentes.md`, „F241.4”, „F241.5”.

## Következő: F241.5b — a forrásmérés gépi kapui és generátor-javításai (D11, D12, D13)

1. A D11 (1)–(2) a TEREMT-001 112 hibájának forrásméréséből: `side-session-notes/local_911d4923…/F239_forrasmeres_112.md` (szókincs-kapu a B65/B66-ra, névtábla-identitás kapu, mezőtípus-jegyzék, prózamező festékkategória; az (a), (b1), (d) ág javítása; (b2) idézet-minőség kapu). A D12: a kapuk az `adat/lapgen_sablonok.tsv` és az `adat/olvasoi_nevtabla.tsv` minden során. Új sablonmondat ⛔ az integrátorhoz.
2. A D13: a 91 MINTA-hely forrásának mérése (melyik lapszakasz, melyik mező) és javaslat → ⛔ az integrátorhoz; LISTA_NEVELO, KONYV („Zef” → teljes könyvnév a könyvnormalizálóból), MUNKASZO („Lap teljesség-mérése” az Irodalom adatforrás-listájában) a generátorban/sablonban; a HAMART-001 2 BUKÁSA és a 11. szabály mérve.
3. A mérés eszköze: `lapgen.fo.lap_keszit` munka módban + `olvasoi_kapu.lap_meres` és `proza_1a` (l. a jelentés F241.3 provenienciáját).

## Szabályok, amelyek ezen a szeleten élnek

- A `claude/f241a-kiadasi-ut` ág másik worktree-ben ki van csekkolva: `git checkout -B <helyi> origin/claude/f241a-kiadasi-ut`, push: `git push origin HEAD:claude/f241a-kiadasi-ut`.
- Egyszerre egy lapgen-futás; előtte `python.exe`-lista (más session push előtti kapuja is futtat `general.py --cel lexikon`-t, azt megvárni); más session folyamatát soha nem állítod le.
- A teljes `lapgen/tesztek/futtat.py` több mint 30 perc: célzott részhalmazok (`kolofon szerkezet kapuk bemenet szoveg`) + a HAMART-001 regressziója (`PARDES_DATUM=2026-11-13 general.py --cel lexikon2 --id HAMART-001 --kimenet <repón kívül>`; `regresszio.py --id HAMART-001 --uj <kimenet>/lexikon --teljes`). A mérce bemenetének (pl. `adat/*.tsv`) változása után a `naplok/F218_referencia.tsv` hash-sora külön commitban frissül.
- A `szamitas/` rétegben a modell mezői kötött típusúak (GK-08a: nincs szabad `str` mező, nincs `.join`/f-string); a kapu üzenete `%`-formázással a kivételben.
- Nem a te feladatod: a `teszt_muhely_allapot` HAMART-határtesztje, a `test_szabalyok` helyi E27-hibái (jelentésbe, nem javítani).
- Kontextus-plafon: kb. 150 ezer token; lépéshatáron átadó.
