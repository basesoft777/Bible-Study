# ELLENŐR — F170_NYILT_MAG_ANGOL_BRIEF.md · `aa61de89..614d95fa`

*A `fuggetlen-ellenor` subagent jelentése (2026-11-05). A subagentnek nem volt fájlíró eszköze, ezért a jelentését a
végrehajtó session (claude-opus-5-5) írta ide a subagent válaszából, tartalmi változtatás nélkül, rövidítve: az OK
sorok összevonva. A „Kezelés” szakasz a végrehajtóé.*

**ELTÉRÉS: 9 tétel.** A subagent a `nyilt_mag_kapu.py`-t, a `teszt_nyilt_mag.py`-t és a `nyilt_mag_angol.py allapot`-ot
szerepkorlát miatt nem futtatta (NEM ELLENŐRIZHETŐ); a számokat git-diff-szűréssel és kódolvasással mérte újra; az E35
bájtazonosságot a `futtat.py` igazolta (0 találat).

## OK (saját méréssel)

- G1 OSIS: 7 234 cella, 11 oszlop; a 66 könyv STEP→OSIS táblája helyes (OSIS 2.1.1); szúrópróba (`2Kor 1:22-23`,
  `ApCsel 2:27; ApCsel 2:31`, `JSir`, `Júd`, `Én`) helyes; ismeretlen könyvnévre `SystemExit`.
- `Sir`→`JSir`: 23 cella, a TAHOT-alak, a projektben máshol is így kezelt. Megjegyzés: a sorkulcs az alias előtt
  képződött (ma nincs ilyen szabadszöveg-sor).
- Versszámozás: a kódkönyv minden `_osis` sora kimondja (példa: `Zsolt 31:18` → `Ps.31.18`, KJV Ps 31:17).
- G2: 185 értéksor `cimke_en`-nel, 0 üres; 34 zárt `_en` oszlop.
- G3: `forditas_modja` 806 + 2 + 139 üres; 869 társo, 541 egyedi hash.
- G4 (kódolvasás): elavult fordítás → BUKÁS. Rés: a tárban maradt árva kulcsot a kapu nem méri.
- G5: 247/247 glossza, a TBESH/TBESG Gloss oszlopával egyezik; a KJV-adathalmazok kizárva. Megjegyzés: H1121 →
  `son: child / Beno` (a tulajdonnév is benne; dokumentált, de félrevezető).
- TSV `'\t'.join`, `csv` 0; a régi kódkönyv-sorokhoz csak a `cimke_en` jött (és a `jelentes_en` leírása változott).
- D1–D3, ⛔ 3. lépés (DT626 🟡 → 🟢 a döntés után), A1, A2, A6: OK.

## ELTÉRÉS (súlyossági sorrendben)

1. E16 HIBA: a PR az ellenőrzőt (`szabalyok.py`) érinti, a brief `ir`-ján kívül; az E10 fájlszintű kivételt kapott; a
   PR cím „[ELLENŐRZŐ]” nélkül bukik; a jelentés nem említi.
2. Az MI-nyilatkozat mondata nem a `kozlemeny/`-ben; az orkesztrátor döntésének nincs döntési tétele.
3. Hűség: `adat/nyilt_angol.tsv` 78. sor — a magyar idézet `"élő lelkével"` helyett `"élő lelke"`. Kisebb: az átírás
   nem egységes (pszükhé/psyche, Abüsszosz, Nefilim).
4. Az E17-bontás hiányos a `nyilt_angol.tsv` +869 soránál (nincs tábla–oszlop szerinti bontás).
5. A felmérés két száma: `Sir` 24 (mért 23), igehely-cella 7 233 (mért 7 234).
6. A forrásleltár félrevezető a TBESH-nál („a sorok forrásmegjelölésében szerepel”, de egyetlen sorban sem).
7. A kódkönyv `jelentes_en` sorának proveniencia-sora elavult (F162).
8. Az F170.4 nem külön commit.
9. A `nyilt_mag_angol.py` docstringje többet állít, mint amit a `tar_ir` ellenőriz.

NEM ELLENŐRIZHETŐ: G6 (kapu, tesztek futása), a ⛔ 5. lépés „mehet”-je (az orkesztrátor üzenete a sessionben van, a
repóban nincs nyoma), a Sonnet-modellnév (az alügynök saját bevallása).

## Kezelés (a végrehajtó, F170.6)

1. A PR címe „[ELLENŐRZŐ]” előtagú (a brief kérése szerint, mert a nyílt mag kapuja és az E10 is változott). Az E10
   kivétele **szűkítve**: az `adat/nyilt_angol.tsv`-ben a szabály csak az `angol` mezőt nézi, a magyar idézetek
   („…”, "…") nélkül; az idézeten kívül maradt `lélek`/`lelki` a `spirit` mellett továbbra is találat (teszt). Döntési
   tétel: DT628 (🟡, a felhasználó a merge-dzsel dönt).
2. DT627: az MI-nyilatkozat mondata a jelentésben (az orkesztrátor döntése, 2026-11-05) — tételként rögzítve.
3. A 78. sor javítva: `"élő lelkével" ["with living soul"]` (csak a fordításon; jelölés `… javítás: claude-opus-5-5`).
   Az átírás-ingadozás a jelentésben megjegyzésként áll (nem hiba: a forrás magyar átírását a fordító megtartotta).
4. A jelentésbe került a `nyilt_angol.tsv` tábla–oszlop szerinti bontása.
5. A felmérés két száma javítva (23; 7 234), a régi érték okával.
6. A TBESH/TBESG szerepe: `forrás (az angol szófogódzó oszlopé)` (új zárt érték, kódkönyv-sorral és címkével).
7. A `jelentes_en` sor proveniencia-sora F170-re frissítve.
8. Az F170.4 az F170.3-ba olvadt (a motívum-meghatározások ugyanabban a fordítási menetben készültek); a jelentés
   kimondja.
9. A docstring pontosítva. Továbbá: a sorkulcs most az igehely egységesítése (`Sir`→`JSir`) után képződik.
