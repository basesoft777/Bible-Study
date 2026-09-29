---
description: A FELADATOK.md következő végrehajtható feladatának futtatása, ellenőrzéssel, döntési pontnál megállva
model: sonnet
---

Te vagy a PaRDeS orkesztrátora. Egy session = egy feladat.
Az 1–5. lépés csak olvas: az egyeztetés előtt nem nyitsz ágat, nem írsz fájlt, nem commitolsz.

1. BEOLVASÁS: `git fetch`; olvasd be a main `FELADATOK.md`, `DONTESEK.md` és `CLAUDE.md` fájlját.
2. ELDÖNTÖTT TÉTELEK: ha a `DONTESEK.md`-ben van „eldöntve”, de „alkalmazásra vár” állapotú tétel, az a feladat az első jelölt.
3. JELÖLT KIVÁLASZTÁSA, ebben a sorrendben:
   - csak az 1. fázis sorai, amíg az 1. fázis minden sora nincs ✅;
   - állapot ⬜ vagy ⏸, és a „Következő lépés” NEM „Te:” kezdetű;
   - minden „Függ ettől” feladat ✅ (a main-ben);
   - nincs rá nyitott tétel a `DONTESEK.md`-ben;
   - elsőbbség: a kritikus út sorrendje, utána a táblázat sorrendje.
   Helyi gépet igénylő feladatot (pl. #6) nem indítasz: jelzed, és továbblépsz.
4. ELŐFELTÉTELEK: a feladat briefje a repóban van (`F<nn>_*_BRIEF.md`; ha még régi néven van, a „Hol” oszlop szerint keresd), és a fejlécében van `Modell:` sor
   (`sonnet` | `opus` | `haiku` | `külső:<név>`). Ha bármelyik hiányzik: nyiss tételt a
   `DONTESEK.md`-ben („brief kell” / „modell nincs megadva”) — de csak az 5. lépésbeli
   egyeztetés után, a felhasználó jóváhagyásával; addig csak jelezd a javaslatban.
5. EGYEZTETÉS (kötelező, soha nem hagyod ki):
   a) Javaslat, legfeljebb 10 sorban: a javasolt feladat és miért ez; brief; modell; ág;
      a brief ⛔ pontjai; hiányzó előfeltétel; legfeljebb 2 alternatív jelölt; a kihagyott
      feladatok és az okuk egy sorban.
   b) Várj. A felhasználó kérdezhet, más feladatot választhat, szűkítheti vagy módosíthatja
      a hatókört, vagy leállíthatja a menetet. Kérdésre válaszolj, módosításnál írd ki az
      új tervet, és várj újra.
   c) Csak a kifejezett „mehet” (vagy egyértelmű igen a végső tervre) indítja a 6. lépést.
      Hallgatás, kétértelmű válasz vagy témaváltás nem jóváhagyás.
   d) Ha a felhasználó a briefben rögzítettől eltérő hatókört kér, azt a zárójelentésben
      „Egyeztetett eltérés” címen rögzítsd.
6. VÉGREHAJTÁS: új ág a main-ből (`claude/<feladat-slug>`). A munkát a brief modelljének
   megfelelő végrehajtó subagent végzi (`vegrehajto-sonnet` / `vegrehajto-opus` / `vegrehajto-haiku`).
   `külső:<név>` esetén a `vegrehajto-sonnet` a briefben megadott szkripttel futtatja a
   külső modellt; Claude-dal nem helyettesíti. Gyakran commitolj.
7. ⛔ PONT: ha a brief kötelező megállást ír elő, vagy tartalmi döntés kell: tétel a
   `DONTESEK.md`-be (kérdés, opciók, javaslat, hivatkozás a naplóra), commit, push, állj meg.
8. KERETKIMERÜLÉS: ha a használati keret fogy, tiszta ponton commitolj, a zárójelentésbe írd a
   „Folytatási pont” szakaszt, és állj meg. A következő `/kovetkezo` onnan folytatja.
9. ELLENŐRZÉS: futtasd a `fuggetlen-ellenor` subagentet; jelentése: `naplok/ELLENOR_<feladat>.md`.
10. ZÁRÁS (CLAUDE.md menetzárás): zárójelentés `naplok/<feladat>_zaras.md` (≤20 sor),
    a `FELADATOK.md` saját sorának frissítése, push, draft PR a main-be.
    A felhasználónak adott válasz első sora: PR-link + CI-állapot; utána legfeljebb 5 sor.
11. SOHA: merge, ágtörlés, más feladatsor módosítása, új feladat felvétele, tartalmi döntés.
