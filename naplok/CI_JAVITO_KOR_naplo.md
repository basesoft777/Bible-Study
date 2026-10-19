# CI_JAVITO_KOR_naplo.md — F50 (FELADATOK #50) munkanapló

*Modell: claude-sonnet-5-5 (a brief `modell: sonnet` mezőjével egyezik) · ág: `claude/f50-ci-javito-kor` · 2026-10-19*

## 0. Leltár

**A jelenlegi záró lépések (olvasva, nem módosítva).**
- `.claude/commands/befogad.md` 5. lépés: új ág, `git mv`, fejléc beírása, `feladatok.py ellenoriz` 0, commit, push, draft PR; a válasz első sora „PR-link + CI-állapot”. A CI eredményét a lépés nem olvassa, piros CI-re nem reagál. A 6. pont tiltja a meglévő brief tartalmának módosítását.
- `.claude/commands/kovetkezo.md` 10. lépés (ZÁRÁS): zárójelentés, fejléc `lezarva`, push, draft PR; a válasz első sora „PR-link + CI-állapot”. A CI olvasása itt sincs.

**Mely CI-szabályok adnak a PR saját fájljaira formai hibát** (`eszkozok/feladatok.py ellenoriz`, `.github/workflows/feladatok.yml`; `eszkozok/ellenorzes/szabalyok.py`).
- `feladatok.py ellenoriz` (job `feladatkovetes`): hiányzó vagy érvénytelen kötelező fejlécmező; `F<nn>_` nevű fájl `feladat` mező nélkül; fájlnév–szám eltérés; `KOR` (függési kör); `kizar`-ütközés; `REGI`/`OLVAS_HIANY`/`MUNKA_HIANY` (E18); a generált blokk módosítása (E18); a feladatterkep-fájlok módosítása (N-F53e).
- `ellenorzes` (job a `ellenorzes.yml`-ben): E2–E20, E25–E29. Formai, a PR saját fájljára vonatkozó: E8 (igehely-formátum), E9, E10, E11 (tiltott kifejezés), E27 (törött hivatkozás áthelyezés/átnevezés után), E26/E-számkiosztás (végleges `DT<n>`/`N<n>` szám ágon). Ezek közül a javíthatóság a 3.3 pontból dől el, nem a szabály nevéből.

## 1. Szöveg (F50.2)

A 3.1–3.7 szabályok szövege a DT-F50a jóváhagyása után (🟢, felhasználó, 2026-10-19, (a)) bekerült az F50.2 commitban a `.claude/commands/befogad.md` 5. lépésébe (a 3.7 is) és a `.claude/commands/kovetkezo.md` 10. lépésébe (CI-javító kör). A javítható és a nem javítható lista a briefben és a `DONTESEK.md` DT-F50a tételében áll; a próba (2. szakasz) besorolása ezekre épül. Ciklikus lekérdezés és időzítés nincs; az Auto-fix a `ccd_pr` dolga marad.

## 2. Próba (csak olvas) — az #158-as eset visszajátszása

**Forrás.** PR #158, commit `6962818ffca8d584cc1d48b392ff34d060de9e50` (`F48.0: befogadás …`), futás: run 37195412826, job `feladatkovetes`, lépés `python eszkozok/feladatok.py ellenoriz`. Proveniencia: `scope=gh run view 37195412826 --log-failed | forras=GitHub Actions log | ts=2026-10-19`.

**A log szó szerinti sorai** (a nyers sor elején a job/lépés előtag és az időbélyeg áll, itt elhagyva):

```
HIBA	F48_KJV_REGI_KIVEZETES_BRIEF.md	2. sor: a feladat egész szám
HIBA	F48_KJV_REGI_KIVEZETES_BRIEF.md	hiányzó kötelező mező: feladat
HIBA	F48_KJV_REGI_KIVEZETES_BRIEF.md	F<nn>_ nevű fájl, de nincs `feladat` mező
##[error]Process completed with exit code 1.
```

**Besorolás az új szabály szerint.**

| Log-sor | Besorolás | Indok |
|---|---|---|
| `hiányzó kötelező mező: feladat` (F48 brief) | **javítható** (3.3, 1. pont; 3.7) | a briefet a PR fogadta be (a commit `git mv`-vel hozta létre a végleges nevet); a log egyértelműen megnevezi a fájlt és a mezőt; a javítás a `feladat: 48` beírása, a brief szövege nem változik |
| `2. sor: a feladat egész szám` | javítható (ugyanaz az ok) | ugyanaz a mező, ugyanaz a javítás |
| `F<nn>_ nevű fájl, de nincs `feladat` mező` | javítható (ugyanaz az ok) | a fájlnév–szám egyezés a mező beírásával áll helyre; `git mv` nem kell |
| hipotetikus `KOR\t22 42 48\t-\tfüggési kör` | **nem javítható, jelentendő** (3.4, 2. pont) | a feloldás másik feladat fejlécének módosítását kérné (`nem_fugg`/`fugg`), ami tilos; a döntés a felhasználóé |

A dokumentált eset eredeti hibája nem a `KOR` volt (a befogadó session így tulajdonította), hanem a `feladat` mező hiánya; az új szabály ezt a két esetet külön osztályozza.

## 3. Állapot a jóváhagyás után

A szabályszöveg bekerült a parancsfájlokba (l. 1. szakasz); a `befogad.md` és a `kovetkezo.md` a megnevezett lépéseken kívül változatlan. Igazolás: `git diff origin/main..HEAD -- .claude/commands` (`scope=git diff | forras=helyi repó | ts=2026-10-19`): `befogad.md` egy hunk (`@@ -26,5 +26,6 @@`, az 5. lépés), `kovetkezo.md` egy hunk (`@@ -88,7 +88,8 @@`, a 10. lépés: a CI-javító kör sora és az F50.4 sorrend-javítása); más lépés nem érintett. Tétel: `DONTESEK.md` DT-F50a.

## 4. Ellenőrzés

`python eszkozok/feladatok.py ellenoriz` (`scope=feladatok.py ellenoriz | forras=helyi futtatás | ts=2026-10-19`), tényleges kimenet az F50.4 commit után:

```
141 brief, 0 hiba, 0 figyelmeztetés
```

## 5. Az ELLENOR_F50 két eltérésének javítása

- **1. eltérés** (`kovetkezo.md` 91. és 94. sor): F50.4 — a worktree-eltávolítás sora a CI-javító kör lezárása utánra szól, és kimondja, hogy a javító commitok a saját ágon, a worktree-ben készülnek; a csomag-válaszformátum feladatonként a „javító kör: n (javítva: …; jelentve: …)” sorral egészül ki.
- **2. eltérés** (e napló 3. szakasza elavult, az 1. és 4. szakasz hiányzott): F50.5 — a 3. szakasz átírva, az 1. és a 4. szakasz hozzáadva.
