---
feladat: 58
cim: Héber igealak-jelkulcs — a morfológiai kódok magyar feloldása nyílt forrásból, adatként
kod: MORF_KULCS
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: dontesre_var
ag: claude/morf-kulcs
ad: egy nyílt licencű forrásból importált, forrás- és licencsorral ellátott jelkulcs-tábla (adat/morf_kulcs_heber.tsv), amely a Macula_heber morfológiai kódjainak minden pozícióját magyarul feloldja; a feloldó függvény ebből a táblából dolgozik, emlékezetből írt leképezés nincs
kovetkezo: Te: válaszd ki a jelkulcs-forrást és a nyelv-kezelést (DT-F58a: javaslat OSHB HebrewMorphologyCodes.html, CC BY 4.0, nyelv külön bemenet), és hagyd jóvá a licencsort; utána /kovetkezo az M1-gyel
olvas: ["konkordancia/Macula_heber_*.tsv", adat/licencek.tsv, adat/SEMA.md, adat/datasetek.tsv]
ir: [adat/morf_kulcs_heber.tsv, adat/SEMA.md, adat/licencek.tsv, adat/datasetek.tsv, eszkozok/morf_feloldas.py, eszkozok/teszt_morf_feloldas.py, adat/kulso/morf_kulcs_LICENC.txt]
fugg: []
---

# F58_MORF_KULCS_BRIEF.md — Héber igealak-jelkulcs

*FELADATOK #58 · Modell: sonnet · v1 · 2026.10.05 · forrás: az olvasói pilot (1Móz 1:1–2:3) tapasztalata, felhasználói döntés 2026-10-05*

## 1. Cél

A `konkordancia/Macula_heber_*.tsv` minden szóhoz morfológiai kódot ad (pl. `Vqp3ms`, `Ncfsa`, `Sp3ms`). Az olvasói pilot ezt csak nyers kódként tudja mutatni, mert a repóban nincs a kódhoz jelkulcs. A meglévő morfológiai modul (`konkordancia/lexikonok_nyers/Morphology.lexicon`) ETCBC-eredetű, CC BY-NC 4.0, ezért a forráspolitika szerint kizárt. A feladat egy nyílt licencű jelkulcsot importál adatként, és arra épít egy feloldó függvényt.

**Előfelmérés (a befogadáskor, `manual`, ts=2026-10-05):** a `Macula_heber_*.tsv` `morf` oszlopában **748 különböző kód** áll. A leggyakoribbak az 1Mózesben: `C` 4 538, `R` 3 777, `Np` 2 618, `Td` 1 808, `Ncmsc` 1 773, `Ncmsa` 1 282, `Vqw3ms` 1 177, `Sp3ms` 1 177. A kódrendszer az OpenScriptures Hebrew Bible (OSHB) morfológiai kódolására hasonlít, a nyelvjelölő (`H`/`A`) nélkül. Ezt az M0 igazolja.

## 2. Hatókör

**Benne van:** a kódrendszer azonosítása, a jelkulcs-forrás kiválasztása és licencének rögzítése, a kulcs importja, a magyar megnevezések felvétele, a feloldó függvény és a lefedettség mérése.

**Nincs benne:** görög kódok (TAGNT/Macula görög; külön feladat, ha kell); a megjelenítés (olvasói nézet); a magyar nyelvtani magyarázat a jelölésen túl (ez a #59 szószedet).

## 3. Lépések

### M0 — Kódrendszer és forrás (⛔)

Jelentés: `naplok/MORF_KULCS_M0.md`.
1. A Macula-kódok szerkezete: pozíciónként mi szerepel (szófaj, törzs, aspektus, személy, nem, szám, állapot, suffixum, nyelv); a 748 kód listája gyakorisággal.
2. Jelölt jelkulcs-források, mindegyiknél a jogtulajdonos **szó szerinti** licencnyilatkozatával (DT-F33c mérce):
   - a Macula saját dokumentációja (Clear-Bible/macula-hebrew);
   - az OSHB morfológiai kódjegyzéke (openscriptures/morphhb);
   - egyéb nyílt forrás, ha a fenti kettő nem fedi le.
3. Melyik forrás fedi le a 748 kód minden pozícióját?

**⛔ Megállás:** a felhasználó választja ki a forrást (javaslattal), és jóváhagyja a licencsort. NC vagy csak-hivatkozási licencű forrás nem választható (`adat/kulso/LICENC.md` forráspolitika).

### M1 — Import

- `adat/morf_kulcs_heber.tsv`: pozíciónként egy sor. Oszlopai: `pozicio`, `kod`, `jelentes_forras` (a forrás saját megnevezése, szó szerint), `jelentes_hu`, `forras`, `proveniencia`.
- A `jelentes_hu` a forrás megnevezésének fordítása, a projekt magyar nyelvtani szóhasználatával (pl. „egyes szám”, „hímnem”). Új magyarázó szöveg nem kerül bele, csak a megnevezés.
- Licenc: `adat/licencek.tsv` új sor, `adat/kulso/morf_kulcs_LICENC.txt` a szó szerinti nyilatkozattal; `adat/datasetek.tsv` új sor.
- SEMA: új szakasz a tábla sémájáról.

### M2 — Feloldó függvény

- `eszkozok/morf_feloldas.py`: kód → magyar feloldás, kizárólag a táblából. Ismeretlen jel → a nyers jel marad, és a kimenet jelzi a hiányt; csendes kitöltés nincs.
- Lefedettség-mérés a teljes Macula-táblán: hány kód oldódik fel teljesen, hány részlegesen; a részleges kódok listája a jelentésben.
- `eszkozok/teszt_morf_feloldas.py`: legalább 10 ismert kód (pl. `Vqp3ms`, `Vqw3ms`, `Ncfsa`, `Ncmsc`, `Sp3ms`, `Td`, `R`, `C`, `Np`) és egy ismeretlen jel.

### M3 — Zárás

`naplok/MORF_KULCS_zaras.md` (≤20 sor), `fuggetlen-ellenor` (`naplok/ELLENOR_MORF_KULCS.md`), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** A jelkulcs forrása nyílt licencű, a licenc szó szerint idézve; NC-forrás nincs.
- **K2.** A tábla minden sora forrásmegnevezésen áll; a magyar oszlop csak a megnevezés fordítása.
- **K3.** A feloldó függvény csak a táblából dolgozik; ismeretlen jel esetén jelez.
- **K4.** A lefedettség mérve és dokumentálva; a teszt zöld; a CI zöld; a független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | Az igealak magyar feloldása csak adatként importált jelkulcsból készülhet; az emlékezetből írt leképezés kikerült a pilotból. | felhasználó |
| v1 | 2026-10-05 | Az ETCBC-modul (CC BY-NC 4.0) nem lehet forrás. | `adat/kulso/LICENC.md` forráspolitika |
