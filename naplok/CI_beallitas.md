# CI_beallitas — a `main` ág védelmének beállítása (CI.3)

*Ezt a felhasználó állítja be a GitHub felületén — Code ezt nem próbálja
automatizálni (a brief kifejezett kérése). Előfeltétel: a CI.2 workflow
(`.github/workflows/ellenorzes.yml`) legalább egyszer lefutott egy nyitott
PR-en, mert a "kötelező check" listája csak a már egyszer lefutott
check-neveket ajánlja fel.*

## Lépések

1. Nyisd meg a repót a böngészőben: `https://github.com/basesoft777/Bible-Study`.
2. **Settings** fül → bal oldali menü → **Branches**.
3. A "Branch protection rules" alatt **Add branch protection rule** (vagy
   ha már van szabály a `main`-re, **Edit**).
4. **Branch name pattern**: `main`.
5. Jelöld be: **Require a pull request before merging**.
   - Ez tiltja a közvetlen push-t a `main`-re — csak PR-en, review/merge
     gombbal lehet utána kerülni bele.
   - Opcionális, de ajánlott: **Require approvals** (min. 1), ha a
     felhasználón kívül más is review-zhat; egyszemélyes repónál
     kihagyható.
6. Jelöld be: **Require status checks to pass before merging**.
   - A keresőmezőbe írd be: `ellenorzes` (ez a `.github/workflows/ellenorzes.yml`
     job neve — l. a workflow `jobs.ellenorzes` kulcsát). Válaszd ki a
     listából, miután megjelent (ehhez a workflow-nak már le kellett
     futnia legalább egy PR-en vagy push-on).
   - Jelöld be: **Require branches to be up to date before merging**
     (ajánlott — így a check mindig a friss `main`-hez képesti diffet
     nézi, nem egy elavultat).
7. Jelöld be: **Do not allow bypassing the above settings** (ha elérhető
   a csomagban) — enélkül egy admin jogú fiók megkerülheti a szabályt.
8. Opcionális, de a brief szellemével összhangban: **Require linear
   history** — ha a repó konvenciója szerint nincs merge commit a
   `main`-en (ellenőrizd a `git log --oneline main` alapján; ha eddig
   voltak merge commit-ok, hagyd kikapcsolva, hogy ne törjön a meglévő
   munkafolyamat).
9. **Create** (vagy **Save changes**).

## Ellenőrzés

- Nyiss egy próba-PR-t egy apró, ártalmatlan változtatással (pl. egy
  elgépelés javítása egy README-ben).
- Ellenőrizd, hogy a PR oldalon megjelenik-e az `ellenorzes` check, és
  hogy a **Merge** gomb tiltva van-e, amíg a check nem zöld.
- Próbálj meg közvetlenül push-olni a `main`-re (pl. `git push origin
  HEAD:main`) — ennek el kell utasítania a szervert oldalon
  ("protected branch hook declined").

## Ha módosítani kell a checket később

Ha az `ellenorzes.yml` job neve vagy a workflow fájl neve változik, a
Branches beállításban a "Require status checks" listát frissíteni kell
manuálisan — GitHub nem követi automatikusan az átnevezést.
