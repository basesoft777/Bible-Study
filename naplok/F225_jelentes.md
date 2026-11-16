# F225_jelentes.md — Fejlesztői előnézet: tükör-frissesség és ágas előnézet

*Végrehajtó: `claude-sonnet-5-5` (a kért modell: `sonnet`, egyezik). Ág: `claude/elonezet-ab-14ecb0`. Nyitó adat: a Fable-vélemény 3. szakaszának A és B része.*

## 1. A menet (tételenként)

### F225.0 — brief, helyőrző

`F225_ELONEZET_BRIEF.md` (a `kovetkezo_szam` 225-öt adott); `nyitott/uj/elonezet-ab-14ecb0.md`: N-F225a, a session-szabály (a `MUNKAMENET.md`-t a nyitott #725 írja, azt nem érintettem). A `fuggesek` KIZAR/FUGGES sorai a brief 3. szakaszában; az első változat `olvas` mezője függési kört (#101 ↔ #122 ↔ #137 ↔ #147 ↔ #225) okozott, ezért az `olvas` csak a `CLAUDE.md`.

### F225.1 — lemaradás a láblécben

`allapot.py`: `lemaradas()`, `checkout_szerep()`, `Lablec.lemaradas`, a figyelmeztetés szövege. Eltérés a feladatleírástól: a számolás **nem** tiszta fájlolvasás, mert a commit-objektumok csomagfájlokban vannak. A ref-ek (HEAD, `refs/remotes/origin/main`) hash-ét fájlolvasás adja; a `git rev-list --count` a feloldott `--git-dir`-rel csak ref-változáskor, háttérszálon fut.

`scope=fo checkout (C:\Users\bases\Desktop\Bible-Study), HEAD..origin/main | forras=wsl -d pardes, git --git-dir=<.git> rev-list --count (csak olvasás) | ts=2026-11-16`: **201** commit, 0,19 s. Ugyanaz a szám, mint a Fable-véleményben.

### F225.2 — a főcheckout frissítése (`indit.sh`)

Az `indit.sh`-ban, nem a `.bat`-ban (a `.bat` a repón kívül áll, nem tesztelhető). **Mérés, amely a kivitelezést megszabta** (`scope=fo checkout, csak olvasás | forras=wsl -d pardes | ts=2026-11-16`):

| parancs | idő | eredmény |
|---|---|---|
| WSL `git status --porcelain --untracked-files=no` | **85 s** | hamisan módosítottnak mutat fájlokat (pl. `.claude/commands/*.md`) |
| `git.exe --no-optional-locks status --porcelain --untracked-files=no` (WSL-interopon) | 0,33 s | tiszta |
| WSL `git --git-dir … rev-list --count` | 0,19 s | 201 |

Következmény: a tiszta-munkafa vizsgálat a WSL-gittel soha nem engedné a frissítést (és 85 s-ig tartana), ezért a `/mnt/<meghajtó>` alatti checkoutnál a Windows `git.exe` fut. A `fetch` a munkafa állapotától függetlenül lefut (a lábléc-jelzés csak friss `origin/main` mellett igaz), az előreléptetés csak tiszta munkafánál; a frissített `indit.sh`-val újraindul.

### F225.3 — az előnézeti védelmek

A közös `~/pardes/pardes.db`-be előnézetben soha nem ír; idegen checkout példányát nem állítja le (`/proc/<pid>/cwd` a sajáttal), megáll (kilépési kód 3), szabad portot javasol. A main-checkout parancsikonjai változatlanul bármit leállítanak a portjukon.

### F225.4 — önfrissítés

`/elonezet/kulcs` és `/elonezet/elonezet.js` (csak `belso`; a kliens a `tervezo_statikus/elonezet.js`, l. a 2. ellenőrzés E1 javítását), `tervezo_statikus/` a figyelt fájlok közt, a lap tetején is a lábléc figyelmeztetése (`labjegyzet`, regisztrált osztály; új osztály nincs, a regiszter-őr zöld). A lap a renderelés pillanatának azonosítóját a szkript-címkében hordozza, így az első lekérdezés előtti változás sem vész el.

### F225.5 — `launch.json`, `.gitignore`, README

A böngészőpanel **kipróbálva**: a `.claude/launch.json` `olvaso-ag` bejegyzése a worktree könyvtárából elindítja a `wsl -d pardes -e bash -lc "./eszkozok/olvaso_szerver/indit.sh belso 8775"` parancsot (a `wsl` a Windows-munkakönyvtárat `/mnt/…`-re fordítja), a napló: `mód: ELŐNÉZET`, `nincs főcheckout-frissítés`, `NINCS másolás`. Élő igazolás a panelben (8775): (1) a lap tetején sáv a nem `main` ágról; (2) egy fájlváltozás után az újratöltő újraindítja a szervert, a lap magától újratöltődik (a JS-változó törlődött, a görgetés megmaradt, új azonosító); (3) `data-tervezo` mellett a frissítés szünetel, a kikapcsolás után pótolódik.

## 2. Tesztek

`python eszkozok/teszt_futtat.py --fajl teszt_indito` (WSL): 80 teszt, zöld (1 kihagyva: a `node --check` WSL-ben nincs node; Windowson lefutott: `JS_SZINTAXIS_OK`). `--fajl teszt_tervezo`: 51, zöld (a regiszter-őr a sablonon). Új tesztosztályok: `TesztLemaradas` (11), `TesztInditFrissites` (11), `TesztInditElonezet` (9), `TesztElonezetAlkalmazas` (10).

## 3. Zárás

*(a független ellenőrzés után töltődik)*
