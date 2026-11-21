---
feladat: 225
cim: Fejlesztői előnézet: a helyi tükör frissessége és az ágas előnézet
kod: ELONEZET
tipus: feladat
fazis: folyamat
sav: SERVER
modell: sonnet
allapot: lezarva
ad: a helyi tükör (8765) lemaradása látszik a láblécben, és induláskor a fő checkout a main-en magától frissül; az `indit.sh` két előnézeti védelmet kap (nem ír a közös adatbázis-másolatba, idegen checkout futó példányát nem állítja le); a `belso` kiadás önfrissítő (könnyű kulcs-végpont + kliensszkript); a lábléc figyelmeztetése a lap tetején is; `.claude/launch.json`
kovetkezo: "Lezárva: a #753, #754 és #757 a main-en (2026-11-16); az ágas előnézet és a tükör-frissesség kész, nincs nyitott maradék."
munka: folyamat
olvas: [CLAUDE.md]
ir: [eszkozok/olvaso_szerver/indit.sh, eszkozok/olvaso_szerver/allapot.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/sablonok/alap.html, eszkozok/olvaso_szerver/tervezo_statikus/elonezet.js, eszkozok/olvaso_szerver/regiszter_or.py, eszkozok/olvaso_szerver/teszt_indito.py, eszkozok/olvaso_szerver/README.md, .gitignore, .claude/launch.json, naplok/F225_jelentes.md]
fugg: []
---

# F225_ELONEZET_BRIEF.md — Fejlesztői előnézet: tükör-frissesség és ágas előnézet

*FELADATOK #225 · Modell: sonnet · v1 · 2026.11.16 · forrás: a felhasználó jóváhagyása („Igen, induljon az A+B”, 2026-11-16), az orkesztrátor terve és a Fable-vélemény (`FABLE_VELEMENY_FEJLESZTOI_ELONEZET_2026-11-16.md`, 3. szakasz A és B; a jegyzetmappában, nem a repóban)*

## 1. Cél

A felhasználó a változást a merge előtt, gyorsan, és ne csak a designra szeretné látni. Két gondolat:

- **A. A tükör frissessége.** A 8765-ös `belso` tükör az éles helyi tükre, de a fő checkout 201 committal az `origin/main` mögött állt (mért: `1352ac3c`, 2026-11-12), mert senki nem húzta le.
- **B. Ágas előnézet a meglévő elemekből.** Egy session a saját worktree-jéből indít egy `belso` példányt külön porton; a példány magától frissül, és nem zavarja a tükröt.

## 2. Hatókör

**Benne van:**

- A. (1) a lábléc kiírja, hány committal áll a futó checkout az `origin/main` mögött; (2) az `indit.sh` a fő checkoutban, a main-en, `belso` kiadásnál, tiszta munkafánál `git fetch` + `git pull --ff-only`, különben kihagyja és kiírja, miért.
- B. `indit.sh` előnézeti védelmek; kulcs-végpont és kliensszkript a `belso` kiadásban; `tervezo_statikus/` a figyelt könyvtárak közé; a lábléc-figyelmeztetés a lap tetején is; `.gitignore` + `.claude/launch.json`; tesztek; README.

**Nincs benne:**

- C. saját adatbázis az adatváltoztató ágnak (adat-, tanulmány- és motívumadat-változás adatbázis-építés nélkül nem látszik az előnézetben: **az előnézet csak a szerver kódját, sablonját, stíluslapját és konfigurációját mutatja**);
- a generált lapok újragenerálása (az S9 két lapját a lapnézet-eszköz mutatja, nem ez);
- a `MUNKAMENET.md` szerkesztése (a nyitott #725 írja): a session-szabály helyőrzőként a `nyitott/uj/`-ban áll.

## 3. Lépések

- **F225.0** brief + N-F helyőrző.
- **F225.1** A: lemaradás-jelzés a láblécben (`allapot.py`, fájlolvasású ref-kezelés; a commitok számolása csak ref-változáskor, háttérszálon, `git rev-list --count`-tal, mert az objektumok csomagolva vannak).
- **F225.2** A: a tükör frissítése az `indit.sh`-ban.
- **F225.3** B: az `indit.sh` két előnézeti védelme.
- **F225.4** B: kulcs-végpont, kliensszkript, `tervezo_statikus/` a figyelt fájlok közt, a lap tetejének figyelmeztetése.
- **F225.5** B: `.gitignore`, `.claude/launch.json`, README.
- Tesztek: `python eszkozok/teszt_futtat.py`; `python eszkozok/push_elott.py` 0 HIBA; push, draft PR, CI; egy célzott `fuggetlen-ellenor` (model: fable), legfeljebb egy javítókör.

**Függések és ütközések** (`python eszkozok/feladatok.py fuggesek`, 2026-11-16; `UTKOZES` sor nincs, a `KIZAR` sorok az idézendők):

```
KIZAR	101	225	eszkozok/olvaso_szerver/indit.sh	×
KIZAR	122	225	eszkozok/olvaso_szerver/indit.sh	×
KIZAR	134	225	eszkozok/olvaso_szerver/sablonok/alap.html	×
KIZAR	135	225	eszkozok/olvaso_szerver/indit.sh	×
KIZAR	139	225	eszkozok/olvaso_szerver/statikus/elonezet.js	×
KIZAR	147	225	eszkozok/olvaso_szerver/oldalak.py	×
KIZAR	164	225	eszkozok/olvaso_szerver/oldalak.py	×
FUGGES	101	225	eszkozok/olvaso_szerver/README.md*
FUGGES	147	225	eszkozok/olvaso_szerver/oldalak.py*
```

Mind a hét ütköző brief `nem_indult` (a #134 `megallt`), tehát futó munkával nincs ütközés. A korábbi, `olvas` mezős változat függési kört (#101 ↔ #122 ↔ #137 ↔ #147 ↔ #225) okozott; az `olvas` ezért csak a `CLAUDE.md`, a többi olvasott fájl a lépésekben áll.

## 4. Elfogadási feltételek

- A PR zöld, az ellenőrzés RENDBEN.
- A jelentés leírja, hogyan indítja a felhasználó az ágas előnézetet.
- A fő checkoutban (`C:\Users\bases\Desktop\Bible-Study`) a fejlesztés alatt semmi nem írt és nem húzott le; a frissítési lépés ideiglenes repón van tesztelve.
- A CSP nem lazul; új CSS-osztály nincs (a regiszter-őr zöld).

## 5. Döntésnapló

- **A fő checkout frissítése az `indit.sh`-ban, nem a parancsikon `.bat`-jában.** Ok: az `indit.sh` verziózott és tesztelhető; a `.bat` az asztalon áll, a repón kívül. A `.bat` változatlan marad.
- **A frissítés a Windows-oldali `git.exe`-vel megy (WSL-interop), ha a checkout `/mnt/<meghajtó>` alatt áll.** Mérés (2026-11-16, a fő checkouton, csak olvasás): a WSL `git status` 85 s alatt fut le, és hamisan módosítottnak mutat fájlokat (sorvég/jogosultság az `drvfs`-en); a `git.exe status` 0,3 s, és tiszta. A tiszta-munkafa vizsgálat a WSL-gittel tehát soha nem engedné a frissítést.
- **A lemaradás számolása `git rev-list --count`-tal, nem tisztán fájlolvasással.** Ok: a commit-objektumok csomagfájlokban vannak; a gráf bejárása tiszta Pythonban a csomagformátum megvalósítását kívánná. A ref-ek olvasása marad fájlolvasás (a `git` a worktree `.git` fájlját nem oldja fel, ezért a `--git-dir` a fájlból feloldott könyvtárra mutat), a számolás csak akkor fut, ha a HEAD vagy az `origin/main` hash-e változott, háttérszálon (mért: 0,19 s a fő checkouton, 201 commit).
- **A `fetch` a munkafa állapotától függetlenül lefut, a `pull` csak tiszta munkafánál.** Ok: a `fetch` a munkafát nem érinti, és a lábléc lemaradás-jelzése csak friss `origin/main` mellett igaz.
- **A kliens a `tervezo_statikus/`-ban áll, és a `/elonezet/elonezet.js` útvonalon szolgálódik ki (csak `belso`).** Ok: a `statikus/` könyvtárat minden kiadás kiszolgálja, a „csak `belso`” szabályt ott a 404 nem tartaná be (független ellenőr, E1); a `regiszter_or.py` a fájlt is olvassa.
- **A `git.exe` ág:** a `WSLENV`-en át `GIT_TERMINAL_PROMPT=0` és `GCM_INTERACTIVE=never` megy hozzá; a `git status` hibája kihagyás, nem tiszta munkafa; a `PARDES_ELONEZET` csak `0` vagy `1` lehet (más érték kilépési kód 2). A teszt a valódi `git.exe`-t a Windows-meghajtón lévő ideiglenes repón járja be (`TesztInditGitExe`).
- **Előnézeti mód:** az `indit.sh` automatikusan előnézetnek veszi, ha a szkript helye linkelt worktree (a `.git` egy fájl); felülírható `PARDES_ELONEZET=0|1`-gyel. Előnézetben nincs adatbázis-szinkron (a közös `~/pardes/pardes.db`-be soha nem ír, csak olvassa), nincs fő-checkout frissítés, és csak az olyan példányt állítja le a porton, amelynek munkakönyvtára ugyanez a checkout.
