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

## Független ellenőrzés — 1. ellenőrzés

ELTÉRÉS: 5 tétel

**Brief:** `F225_ELONEZET_BRIEF.md` · **tartomány:** `efb492ff..e56110f4` · **szint:** `teljes` (`python eszkozok/feladatok.py szint 225` → `SZINT #225 teljes 2 kör olvasói kimenetet állít elő: eszkozok/olvaso_szerver/indit.sh`)

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0. modell | OK | — | A session modellje `claude-opus-5-5`, a kért `opus`; egyezik. A menet `modell` mezői: a jelentés `claude-sonnet-5-5`-öt ír, és mind a 6 commit trailere `Claude Sonnet 5.5` (`git log efb492ff..HEAD --format='%h %s%n%(trailers:key=Co-Authored-By)'`); ez a brief `modell: sonnet` mezőjével egybevág. Adattábla-sor nincs a diffben. |
| 3. CI | OK | — | `gh run view 43826738845 --json headSha,status,conclusion,jobs` → headSha `e56110f43dab…` = HEAD, `completed/success`, a `feladatkovetes` és az `ellenorzes` job is success. Az E1–E37 eredményét innen veszem, a `futtat.py`-t nem futtattam újra. |
| Tesztek: teszt_indito | OK | `eszkozok/olvaso_szerver/teszt_indito.py` | `python eszkozok/teszt_futtat.py --fajl teszt_indito` → `Ran 80 tests in 47.830s OK (skipped=1)` (WSL). |
| Tesztek: `--diff efb492ff` és a lassú tesztek | NEM ELLENŐRIZHETŐ | `eszkozok/teszt_futtat.py:55` | A diff az `eszkozok/olvaso_szerver/`-t érinti, ezért a `LASSU_LEFEDETT` szerint a `teszt_szintek` és a `teszt_arculat` kötelező; ezeket a CI nem futtatja. Elindítottam (`python eszkozok/teszt_futtat.py --diff efb492ff`, háttérfeladat `bj22fqfxv`), de a jelentés zárásakor még a közös zárra várt: a zárat egy másik worktree tartja, `elegant-elion-896f84`, `futtat.py --valtozott (110 fájl)`, 09:01:26 óta. A lassú tesztek kb. 20–30 percig futnak. A meglévő oldaltesztek (`teszt_olvaso_szerver`, `teszt_tervezo`) a lap tetején megjelenő új sávval ezért nincsenek általam lefuttatva. |
| G A(1): lemaradás a láblécben | OK | `allapot.py:170-224, 294-299` | Kódolvasás és a `TesztLemaradas` (11 teszt, zöld). Csomagolt objektumok, `packed-refs`, worktree `--git-dir`: tesztelve. |
| G A(2): a főcheckout frissítése | OK, megjegyzéssel | `indit.sh:69-118` | A `pull --ff-only` helyett `fetch` + `merge --ff-only origin/main`; ez egyenértékű, és a fejléc dokumentálja. Minden feltétel le van fedve (`PARDES_FRISSIT`, belso, nem előnézet, `.git` könyvtár, `main` ág). Az újraindulás egyszeri: a `PARDES_FRISSITVE=1` miatt a második futás nem frissít újra; a `"$@"` a legfelső szinten megmarad; `set -u` mellett minden változó definiált. A `TesztInditFrissites` (11 teszt) ideiglenes repón fut. A hibakezelési hiányokat l. az E3 és E4 tételt. |
| G B: előnézeti védelmek | OK, megjegyzéssel | `indit.sh:47-57, 116-139, 155-158` | Előnézetben a `cp`/`mv`/`TMP` ág nem érhető el (`if [ "$ELONEZET" = "1" ]` előbb ágazik el). A szerver `mode=ro`-val nyit (`adatbazis.py:52`), és az `allapot.db_epites_ts` is (`allapot.py:45`). A testvérkönyvtár-előtag (`olvaso_szerver2`) a `"$CEL_REAL"/*` minta miatt kizárt. Ha a `readlink` hibázik vagy a `cwd` üres, a példány idegennek számít, és a szkript 3-as kóddal kilép (biztonságos irány). A felismerés kerülőútját l. az E2 tételt. |
| G B: kulcs-végpont, kliens, figyelt fájlok, felső sáv | ELTÉRÉS, l. E1 | `alkalmazas.py:66, 75-83`; `statikus/elonezet.js:1-2` | A végpont csak `belso`-ban él, és nem olvas adatbázist (a teszt a `db.kapcsolat`-ot lecseréli). A szkript viszont minden kiadásban kiszolgálható (E1). |
| G B: `.gitignore`, `launch.json`, README | OK | `.gitignore:10-14`, `.claude/launch.json` | A `!.claude/launch.json` kivétel a `.claude/*` után áll, tehát hat. Azt, hogy a panel valóban a worktree-ből indít, nem tudom igazolni: NEM ELLENŐRIZHETŐ, csak a jelentés állítja. |
| G: hatókör, „Nincs benne” | OK | brief 2. szakasz; `nyitott/uj/elonezet-ab-14ecb0.md` | Generált lap, `MUNKAMENET.md` és adat nincs a diffben (`git diff --numstat efb492ff..HEAD`: 13 fájl, mind a felsoroltak közül). |
| Elfogadás: PR zöld | OK | — | CI success (fent). |
| Elfogadás: a jelentés leírja az indítást | OK | `naplok/F225_jelentes.md:39`; `README.md` „Fejlesztői előnézet” | — |
| Elfogadás: a fő checkoutban semmi nem írt és nem húzott le | OK (a HEAD-re) | — | `git -C …/Desktop/Bible-Study log -g -8 HEAD`: az utolsó HEAD-mozgás `1352ac3c`, 2026-11-12 20:23. Az `origin/main` reflogjában 11-16 07:32 és 07:45 között két fetch áll; a 07:45-ös `--porcelain --no-write-fetch-head` alakja worktree-létrehozásra vall. A ref közös, ezért nem tudom a menethez kötni, és nem is HEAD-mozgás. |
| Elfogadás: a CSP nem lazul, nincs új CSS-osztály | OK | `teszt_indito.py` `test_a_csp_nem_lazul`, `test_a_lap_tetejen…` | A tesztek zöldek. A `regiszter_or.py:42` `JS_FAJLOK` listájában az `elonezet.js` nem szerepel: a védelem csak a szövegteszten (`assertNotIn('classList')`) múlik. Ez megjegyzés, nem eltérés. |
| D1 (`.bat` változatlan) | OK | — | A `.bat` a repón kívül áll, a diff nem érinti. |
| D2 (`git.exe` a `/mnt` alatt) | OK, de a mérés NEM ELLENŐRIZHETŐ | `indit.sh:76-80` | A 85 s és a 0,33 s mérést csak a fő checkouton lehetne megismételni, ott nem futtatok. A `git.exe` útvonalat egyetlen teszt sem járja be: a tesztrepó `/tmp`-ben van, ott a WSL-git fut. L. az E3 tételt. |
| D3 (`rev-list`, háttérszál) | OK | `allapot.py:176-224` | A versenyhelyzet zárva: a `_SZAMOL` jelzőt zár alatt állítja be, a szálat egyszer indítja. A `_tarol` metszése az utolsó 8 kész kulcsot tartja meg. A `safe.directory` `-c` kapcsolóval megy; parancssori beállításként ezt a git elfogadja. |
| D4 (a `fetch` a munkafa állapotától függetlenül fut) | OK | `indit.sh:84-88` | `test_piszkos_munkafan_kihagyja_de_a_fetch_lefut`. |
| D5 (előnézeti mód, felülírás) | ELTÉRÉS, l. E2 | `indit.sh:47-49` | — |
| A1 (memória vs. lekérdezés) | NEM ELLENŐRIZHETŐ | `naplok/F225_jelentes.md:15, 19-25` | A mérések proveniencia-sorral állnak, de a fő checkouton mért értékeket (201 commit, 0,19 s, 85 s) nem ismételhetem meg. |
| A2 (nyitott tételek) | OK, részben NEM ELLENŐRIZHETŐ | `nyitott/uj/elonezet-ab-14ecb0.md:1` | Az N-F225a új és nyitott. Azt, hogy „a #725 nyitott”, a megengedett parancsokkal (`gh run` csak) nem tudom ellenőrizni. |
| A3–A6 | OK, nem alkalmazható | — | A diffben nincs tartalmi réteg (adat, motívum, lexikon, tanulmány, tanító). Olvasói kimenetet csak a szerver-UI szövegei adnak (figyelmeztetések); ezekről az E5 szól. Az E12–E15 nem jelzett: a CI zöld. |
| Ellenőrzőlista 1: kiszűrt/törölt sorok | OK | — | `git diff --numstat efb492ff..HEAD`: törölt sorok csak kódban és README-ben (README 7, alkalmazas 2, allapot 17, indit.sh 7, teszt_indito 8). Mind átírás, adatsor nincs köztük. |
| Ellenőrzőlista 2: kulcstartomány | OK, nem alkalmazható | — | A diffben nincs kulcstartományos adat. |
| Ellenőrzőlista 3: nulla-diff | OK, nem alkalmazható | — | Nulla-diff állítás nincs; generált kimenet nincs a diffben. |
| Ellenőrzőlista 4: TSV-sorszám Δ | OK | — | `git diff --numstat efb492ff..HEAD -- adat/ konkordancia/ \| wc -l` → `0`. Minden tábla Δ = 0. |
| Ellenőrzőlista 5: ⛔ pontok | OK | — | A briefben nincs ⛔. A „fő checkoutot nem írja” vállalás teljesül (fent). |
| DT-F221a (hatókör-szűkítés) | OK | brief 2. szakasz | Az előnézet új eszköz, nem szűkít meglévő ellenőrzést. A korlátját (az adatváltozás nem látszik) a brief és a README is kimondja. |
| Újratöltési hurok (4. kérdés) | OK, megjegyzéssel | `oldalak.py:229, 632-642`; `alkalmazas.py:114-115` | A gyorsítótár-kulcs az azonosító mind a négy összetevőjét tartalmazza, tehát végtelen hurok nincs. Egy plusz újratöltés viszont várható: indulás után a lemaradás az első rendereléskor `None`, és amikor a háttérszál végez, az azonosító megváltozik, a lap egyszer újratölt. |

**ELTÉRÉS-ek, súlyosság szerint:**

- **E1 (közepes): a belső kliens minden kiadásban kiszolgálható.**
  - Hol: `statikus/elonezet.js:1-2` és `alkalmazas.py:75-76`.
  - Mi a hiba: a megjegyzés szerint „más kiadásban sem az útvonal, sem a szkript nincs (404)”. A fájl viszont a `statikus/` könyvtárban van, amelyet a Flask static útvonala minden kiadásban kiszolgál (`alkalmazas.py:66`; `before_request` szűrő nincs). A `/statikus/elonezet.js` tehát `nyilvanos` és `kereskedelmi` kiadásban is elérhető.
  - Mi sérül: a #98 M2 mintája, amely a belső klienst a `tervezo_statikus/`-ba teszi; a `teszt_tervezo.py:499` erre 404-et vár. A `test_csak_a_belso_kiadasban` csak a lap HTML-jét és a `/elonezet/kulcs`-ot nézi, ezért nem veszi észre.
  - Javítás: a kliens kerüljön csak `belso`-ban bejegyzett útvonalra, plusz egy 404-teszt.
- **E2 (alacsony–közepes): érvénytelen `PARDES_ELONEZET` csendben kikapcsolja a védelmet.**
  - Hol: `indit.sh:47-50`.
  - Mi a hiba: bármely `1`-től eltérő érték (`true`, `yes`) nem-előnézetnek számít. Worktree-ben ilyenkor a szinkron a worktree saját `pardes.db`-jéből a közös `~/pardes/pardes.db`-be másol, ha van ilyen fájl és az építési ideje eltér, és a porton futó idegen példányt is leállítja. Mindezt figyelmeztetés nélkül.
  - Javítás: `case "$PARDES_ELONEZET" in 0|1) ;; *) exit 2 ;; esac`.
- **E3 (alacsony): a `git.exe` ág nincs védve a hitelesítési kérdés ellen, és nincs tesztelve.**
  - Hol: `indit.sh:84-86`.
  - Mi a hiba: az `export GIT_TERMINAL_PROMPT=0` a WSL-interopon nem jut át a `git.exe`-hez, mert a `WSLENV` nem tartalmazza. Lejárt hitelesítésnél a Windows-oldali credential manager párbeszédablakot nyithat. A `timeout 90` a WSL-oldali folyamatot állítja le; azt nem igazoltam, hogy a Windows-oldali `git.exe` is leáll.
  - A jelentés nem mondja ki, hogy ezt a „mért” utat (`git.exe`, CRLF-kezelés) egyetlen teszt sem járja be.
  - Javítás: `WSLENV=GIT_TERMINAL_PROMPT/u` vagy `-c credential.interactive=never`, és ezt kimondani a jelentésben.
- **E4 (alacsony): a `status` kilépési kódját senki nem nézi.**
  - Hol: `indit.sh:89-90`.
  - Mi a hiba: ha a `status` időtúllépéssel vagy hibával, kimenet nélkül ér véget, a munkafa tisztának számít, és a `merge --ff-only` lefut. Ha nincs `git.exe`, a WSL-git kb. 85 s alatt fut a 90 s-os határ előtt, tehát ez a határeset reális.
  - Javítás: a `status` kilépési kódját külön ellenőrizni.
- **E5 (alacsony): az olvasói szöveg pontatlan.**
  - Hol: `allapot.py:296-297`.
  - Mi a hiba: a `main`-figyelmeztetés szerint „a parancsikon újraindításakor az indító frissíti”. Ez csak a `belso` parancsikonra és tiszta munkafára igaz. A szöveg a 8766-os (`nyilvanos`) és a 8768-as (`kereskedelmi`) lábléceiben is megjelenik, és most már a lap tetején is.

A háttérben futó `bj22fqfxv` feladat (`--diff efb492ff`) a jelentés után is fut, és a zárat 20–30 percre lefoglalja. A hívó szükség szerint leállíthatja, vagy megvárhatja, és az eredményét a lassú tesztek sorához csatolhatja.

### Válasz az 1. ellenőrzéshez

Mind az 5 tétel javítva az `F225.7` commitban (egy javítókör); célzott újraellenőrzés (hibahely-tábla), nem teljes újraolvasás:

| tétel | javítás | igazolás |
|---|---|---|
| E1 | a kliens `tervezo_statikus/elonezet.js`, útvonala `/elonezet/elonezet.js` (csak `belso`); a `regiszter_or.py` `JS_FAJLOK` listája is tartalmazza | `test_csak_a_belso_kiadasban`: `/elonezet/elonezet.js`, `/statikus/elonezet.js`, `/tervezo/elonezet.js` mind 404 a `nyilvanos` és a `kereskedelmi` kiadásban; `test_a_kliens_kiszolgalva_es_tartalma`: `belso`-ban 200, `/statikus/…` 404; `teszt_tervezo` zöld |
| E2 | `indit.sh:50`: a `PARDES_ELONEZET` csak `0` vagy `1`, más érték kilépési kód 2 | `test_ervenytelen_elonezet_ertek_hiba_nem_nem_elonezet` (`true` → 2, nincs másolás) |
| E3 | `indit.sh:85–86`: `GIT_TERMINAL_PROMPT=0`, `GCM_INTERACTIVE=never` a `WSLENV`-en át; a `git.exe`-s utat valódi `git.exe`-vel, Windows-meghajtón lévő ideiglenes repón járja be a teszt | `TesztInditGitExe` (nem kihagyott: a futás `skipped=1` csak a `node --check`) |
| E4 | a `git status` kilépési kódja külön ellenőrzött: hiba → `KIHAGYVA`, nincs `merge` | `test_sikertelen_status_nem_tiszta_munkafa` |
| E5 | `allapot.py:297`: „a belso parancsikon újraindításakor az indító frissíti a főcheckoutot (tiszta munkafánál)” | `test_a_figyelmeztetes_szovege_main_es_ag` |

Megjegyzések az ellenőrtől: a `regiszter_or.py` `JS_FAJLOK` bővítve (E1-gyel együtt); a „plusz újratöltés” indulás után a README-ben leírva. A „panel a worktree-ből indít” állítást az ellenőr nem tudta igazolni; a menet során élőben igazolva (l. F225.5). Hibát a javítás során külön is találtam: a `Lablec.keszit`-et hívó három meglévő teszt a valódi checkout lemaradásától függött (a main előreléptével a `figyelmeztetesek == []` elromlott); `PARDES_LEMARADAS=0` rögzíti őket (`F225.9`).

## 3. Zárás

- **Elkészült:** A. lemaradás-jelzés a láblécben (201 a fő checkouton) és főcheckout-frissítés az `indit.sh`-ban (`git.exe`-vel a `/mnt/…` alatt); B. előnézeti mód két védelemmel, `/elonezet/kulcs` és kliens (csak `belso`), `tervezo_statikus/` figyelt, a lap tetején is a figyelmeztetés, `.claude/launch.json`. A C rész, a generált lapok újragenerálása és a `MUNKAMENET.md` nem.
- **Tesztek (WSL):** `teszt_indito` 83 (kihagyva 1: `node` hiányzik WSL-ben; Windowson `node --check` rendben), `teszt_tervezo` 51, `teszt_olvaso_szerver`, `teszt_pilot_aranymintaval`, `teszt_kereses`, `teszt_arculat` és a többi olvasó-teszt zöld. `push_elott.py`: 0 HIBA (a javítások után is). CI: zöld.
- **Régi, nem általam okozott hibák:** `teszt_szintek.py` (2 teszt) és `teszt_visszhang_kapu.py` (2 teszt) az `efb492ff`-en (main) **ugyanúgy, ugyanazokkal a tesztnevekkel** buknak, ideiglenes worktree-ben mérve; a WSL adatbázisa (`2026-11-12T18:53:35Z`) régebbi, mint a main kódja. Nem része ennek a tételnek; az adatbázis újraépítése után ellenőrizendő.
- **Nyitott:** N-F225a (a session-szabály a `MUNKAMENET.md`-be a #725 után). A `mcp__Claude_Browser__preview_stop` ebben a menetben nem kapott jóváhagyást: az `olvaso-ag` előnézet (8775, ez a worktree) fut tovább; a panelből vagy `fuser -k 8775/tcp`-vel leállítható.
- **A felhasználó indítása:** a panelben az `olvaso-ag`, vagy kézzel: `wsl -d pardes -e bash -lc "cd /mnt/<meghajtó>/<worktree útja> && ./eszkozok/olvaso_szerver/indit.sh belso 8775"`; cím `http://localhost:8775/`.
- **PR:** [#753](https://github.com/basesoft777/Bible-Study/pull/753) (draft).

### Kiegészítés az 1. ellenőrzéshez (az ellenőr zárójelentése)

Az ellenőr zárójelentése ugyanazt az öt tételt (E1–E5) hozza, mint a fent szó szerint mentett közbenső jelentés; az egyetlen új tartalma a lassú tesztek eredménye: `teszt_szintek` (2 teszt) és `teszt_visszhang_kapu` (2 teszt) bukik, és az ellenőr nem tudta eldönteni, hogy a base-en is. **Válasz:** a base-en (`efb492ff`, ideiglenes worktree, WSL, ugyanaz az adatbázis) mindkét fájl ugyanazokkal a tesztnevekkel ugyanígy bukik, tehát nem az F225 okozza (l. a Zárást). Az E1–E5 az `F225.7`-ben javítva.
