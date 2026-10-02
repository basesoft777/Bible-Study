---
feladat: 47
cim: Három állapot-ellentmondás javítása (F22-brief és jelöltlista, F24-brief, DT6)
kod: ALLAPOT_ELLENTMONDASOK
tipus: naplozas
fazis: folyamat
modell: sonnet
allapot: lezarva
ag: claude/f47-allapot-ellentmondasok
pr: "#136"
lezarva_osszegzes: a #22 (fut), a DT-F24 és a DT6 állapota a felhasználói döntésekhez igazítva (DT6: csak a (b) pont); ellenőrzés `naplok/ELLENOR_ALLAPOT_JAVITAS.md`; nyitott: a #41 briefje és a DT6 ütközése
ad: felhasznalo
kovetkezo: "Code — J1 3. pont csak ellenőrzés (`feladatok.py jeloltek` futtatása, kézi szerkesztés nincs); a #47 ne fusson #26-tal egy csomagban, futó #26 lezárásáig várjon"
olvas: [F22_KAROLI_STRONG_BRIEF.md, F24_LICENC_BRIEF.md, DONTESEK.md, FELADATOK.md]
ir: [F22_KAROLI_STRONG_BRIEF.md, F24_LICENC_BRIEF.md, DONTESEK.md, naplok/ELLENOR_ALLAPOT_JAVITAS.md]
---

<!-- KOZVETLEN_FUTTATAS -->
Futtasd ezt a briefet. Előtte ellenőrizd, hogy a futó modell egyezik-e a fejléc `modell` mezőjével (sonnet). Ha nem egyezik, állj meg és jelezz.
Három állapot-ellentmondást javítasz. A döntések már megszülettek, csak a fájlok maradtak le róluk. Új döntést nem hozol. Ha valamelyik fájl nem a leírt állapotban van, vagy nem találod egyértelműen, állj meg és kérdezz.
<!-- KOZVETLEN_FUTTATAS -->

## Általános szabályok

- Meglévő címsor szövegét nem módosítod. Az állapotváltozás a címsor alá kerül (különben a CI E5 szabálya törlésnek veszi).
- Ha a `jeloltek` generált kimenet, a forrását javítod és újragenerálod. A kimenetet nem szerkeszted kézzel.
- Mindhárom javítás egy commitba kerül.

## J1 — #22 (Károli–Strong teljes futás): a brief és a jelöltlista

Tényállás (a felhasználó döntései):
- A #22 Sonnettel, Claude Code-ban, könyvenként fut. A Genezis és az Exodus már lefutott (Sonnet + Gemini pár), Leviticustól csak Sonnet (DT-F22c ✅).
- DT-F22a lezárva (2026.10.02): a mérési alap a régi arany és a zárt forrással való összevetés; ez csak tájékoztató, küszöb nélküli, egész fejezeteken készül, és nem akasztja meg a #22-t.
- A DT-F21j 🟢 marad.

Teendő:
1. `F22_*_BRIEF.md` `allapot` mezője: `dontesre_var` helyett `fut` (vagy a `BRIEF_SABLON.md` szerinti megfelelő érték a futó feladatra).
2. Ugyanitt a `kovetkezo` mező: a DT-F22c ne szerepeljen nyitottként. Új érték: „Te: a következő könyvek ütemezése (Leviticustól, csak Sonnet)”.
3. A `jeloltek` listából a #22 kikerül, mert futó feladat, nem jelölt. A következő könyvek ütemezését a felhasználó adja meg; az orkesztrátor ne vegye fel magától.

## J2 — DT-F24 (licenc-leltár): a brief

Tényállás: a DT-F24 döntés 2026.10.01-én rögzült (PR #99):
- egy mérce: `tisztazott` csak szó szerinti licencidézettel; a README-összefoglaló nem elég;
- a Mounce/MCGED-re az F6 D16 érvényes;
- a repó a fejlesztés alatt nyilvános marad;
- korlátozott licencű nyers fájl csak a gitignore-olt `_nyers/` alá kerülhet.

Teendő az `F24_LICENC_BRIEF.md`-ben:
1. Az opciók alá kerüljön „Eldöntve (2026.10.01, DT-F24): …” sor a fenti tartalommal. A választott opció „elfogadva”, a többi „nem választott” jelölést kap.
2. A `kovetkezo` mező: „Utófeladat (LICENSE-idézetek, átsorolás, régi `LXX_kivonat` kivezetése, TBESH/STEPBible terjesztési feltételek) a `/befogad` útján, a #99 merge-e után”.

## J3 — DT6 / #41

Tényállás: a felhasználó a DT6 (b) pontját jóváhagyta (2026.10.02). A megvalósítás a #41-ben történik.

Teendő a `DONTESEK.md`-ben:
1. A DT6 jelölése 🟡 → 🟢.
2. A DT6 alá: „Eldöntve (2026.10.02): a (b) pont jóváhagyva, megvalósítása a #41-ben.”
3. Ha a DT6 opciókat sorol fel, a (b) „elfogadva”, a többi „nem választott”.
4. A #41 JELOLT marad.

## Ellenőrzés

- `grep` a három fájlban: a `dontesre_var` már nem szerepel az F22-briefben; a DT-F22c nem szerepel nyitottként; a #22 nincs a jelöltek között; a DT6 🟢.
- A CI E5 szabálya ne jelezzen címsor-törlést.

## Menetzárás

1. Commit (egy darab), üzenet: `allapot: F22/F24 brief és DT6 a döntésekhez igazítva`.
2. A `fuggetlen-ellenor` ügynök futtatása, jelentés a `naplok/ELLENOR_ALLAPOT_JAVITAS.md` fájlba, commitolva.
3. Push.
4. Draft PR a main-be.
5. A záró összefoglaló első sora a PR linkje és a CI állapota.

## Döntésnapló

| Dátum | Tétel | Döntés | Forrás |
|---|---|---|---|
| 2026.10.02 | DT-F22c | Leviticustól csak Sonnet, külső modell nélkül | felhasználó, korábbi döntés |
| 2026.10.02 | DT-F22a | A zárt összevetés tájékoztató, nem akasztja meg a #22-t | felhasználó, korábbi döntés |
| 2026.10.01 | DT-F24 | Licenc-mérce, a repó nyilvános, korlátozott nyers fájl csak a `_nyers/` alá | PR #99 |
| 2026.10.02 | DT6 | A (b) pont jóváhagyva, megvalósítása a #41-ben | felhasználó, ebben a chatben |
| 2026.10.02 | ez a brief | Állapot-igazítás, új döntés nélkül | — |
