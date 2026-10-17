# SZOTAR S2 (#9) — `elavult_adat` szúrópróba (DT-F09g)

*Ág: `claude/f09-szotar-s2` · modell: `claude-sonnet-5-5` · mintavétel: `naplok/F09_J_elavult_szuropr.py` (seed 20261017, n=15) · proveniencia: scope=`generalt_proba/F09_szotar_s2_proba/lexikon/*_TUDOMANYOS.md` vs `lexikon/` | forras=`eszkozok/render_diff_osztalyoz.py` (`proba_osztalyoz`) + `naplok/F09_J_elavult_szuropr.py` | ts=2026-10-17*

A `_TUDOMANYOS` fájlokban 371 `elavult_adat`-sor van: 51 törölt (régi tartalom) és 320 hozzáadott. A minta a **törölt** sorokból való (a „hol él tovább a régi tartalom?” kérdés csak ott értelmes); a hozzáadott sorok az új adatréteg sorai. A „mechanikus” oszlop a `ProbaSzoveg.tovabb_el` eredménye (a próba szövegében megvan-e a normalizált sor, vagy a sor minden igehelye): ez gyenge bizonyíték, ezért a kézi megítélés a döntő.

| # | Fájl, éles sor | Régi sor (rövidítve) | Mechanikus | Hol él tovább / miért elavult | Ítélet |
|---|---|---|---|---|---|
| 1 | ALVIL-001, 812 | `#### Jób 17:13` (kereszthivatkozás-fejléc) | igehely | A sor az F87.3-mal (98f22fc6, DT-F87b) átkulcsolt `Jób 17:13` → `Jób 17:12` sor jelölt-listájának fejléce. A próbában `#### Jób 17:12` fejléc nincs (az új kulcsra a TSK/Károli-táblában nincs találat); a próba-táblázat a `Jób 17:12`-t a 82. sorban hordozza. | elavult (átkulcsolás), a tartalom nem vész el: a régi kulcs jelölt-listája a téves versre vonatkozott |
| 2 | ALVIL-001, 69 | `\| [1Móz 42:38] \| a koporsóba — שְׁאֽוֹלָ …` előfordulás-sor | igehely | Ugyanez a sor a próba 69. sorában, csak a módszer-jelző változott (`tartalom-alapú` → `szó-szintű-gépi`, `adat/elofordulasok.tsv` mai értéke). | tovább él (jelző-frissítés) |
| 3 | ISTENTISZT-001, 70 | `\| [1Móz 12:8] …` | igehely | Próba 69. sor, azonos tartalom, módszer-jelző frissítve. | tovább él |
| 4 | ALVIL-001, 296 | `*(Jób 17:16: nincs Károli-szöveg)*` | igehely | F87.3: `Jób 17:16` → `Jób 17:15`; a próba 295–296. sorában a `Jób 17:15` mellett ott a Károli-szöveg („Leszáll az majd a sír üregébe…”). A régi jelzés a téves kulcs hiányát mondta. | elavult (átkulcsolás), a tartalom megvan |
| 5 | MENNY-001, 146 | `*Ez a blokk … 2 elutasított/nyitva maradt jelöltjét fedi …*` | nincs | Sablonmondat a blokk adatából számolt számmal; a próba 146. sora ugyanaz 3-mal (`adat/jeloltek.tsv` MENNY-001: 12 sor, a blokk ebből a kizárt/nyitva maradtakat számolja). | elavult (a szám frissült) |
| 6 | ALVIL-001, 289 | `<a id="ige-jób-17-13"></a>` | sor | F87.3 átkulcsolás: a próba 289. sora `<a id="ige-jób-17-12">`, a 294.: `ige-jób-17-15`. A régi horgony a téves kulcs volt (a mechanikus „sor” találat egy más helyen álló azonos horgonyra vonatkozik). | elavult (átkulcsolás) |
| 7 | ISTENTISZT-001, 73 | `\| [1Móz 26:25] …` | igehely | Próba 72. sor, azonos, jelző frissítve. | tovább él |
| 8 | ISTENTISZT-001, 75 | `\| [2Móz 34:5] …` | igehely | Próba 74. sor, azonos, jelző frissítve. | tovább él |
| 9 | TEREMT-001, 68 | `\| [1Móz 1:2] \| mélység — תְה֑וֹם …` | igehely | Próba 68. sor, azonos, jelző frissítve. | tovább él |
| 10 | TEREMT-001, 71 | `\| [1Móz 49:25] …` | igehely | Próba 71. sor, azonos, jelző frissítve. | tovább él |
| 11 | ISTENTISZT-001, 336 | `Nincs kizárt vagy nyitva maradt jelölt a jeloltek.tsv-ben ehhez a motívumhoz.` | nincs | A próbában a blokk 81 jelöltet számlál (333. sor), tehát a régi „nincs” állítás ma hamis; ez adat-frissülés, nem tartalomvesztés. | elavult |
| 12 | MENNY-001, 68 | `\| [1Móz 6:2] \| az Istennek fiai — בְנֵי …` | igehely | Próba 68. sor, azonos, jelző frissítve. | tovább él |
| 13 | ANTROP-001, 137 | `*Ez a blokk … 1 elutasított/nyitva maradt jelöltjét …*` | nincs | A próba 137. sora 3-mal (`adat/jeloltek.tsv` ANTROP-001: 3 elutasított/nyitva sor, mért). | elavult (a szám frissült) |
| 14 | KIRALY-001, 69 | `\| [2Móz 19:6] \| papok — כֹּהֲנִ֖ים …` | igehely | Próba 69. sor: a glossza `papok birodalma`, a jelző frissítve; az F87.3 (98f22fc6) az `adat/elofordulasok.tsv` `karoli_szo` mezőjét `papok` → `papok birodalma`-ra javította. | elavult (adatjavítás), a sor tovább él |
| 15 | TEREMT-001, 72 | `\| [2Móz 15:5] \| a mélységbe — תְּהֹמֹ֖ת …` | igehely | Próba 72. sor: `a hullámok` (F87.3: `karoli_szo` `a mélységbe` → `a hullámok`), jelző frissítve. | elavult (adatjavítás), a sor tovább él |

**Összegzés:** a 15 mintából 0 olyan sor van, amelynek tartalma sehol nem él tovább és nem igazoltan elavult. A 15-ből 7 sor azonos tartalommal él tovább (jelző-frissítés), 8 sor elavult (átkulcsolás: 1, 4, 6; adatjavítás: 14, 15; sablonmondat-szám/állítás: 5, 11, 13). Az 1., 4. és 6. minta igazolása a mechanikus „igehely” szerint gyenge, a kézi nézés (F87.3-commit, próba-sorok) viszont egyértelmű.

**Figyelem:** a szúrópróba a 371-ből csak a 51 törölt `elavult_adat`-sort fedi. A **nem** `elavult_adat`-ba sorolt, de ugyanebből az okból törölt 14 sor `ismeretlen` (`naplok/SZOTAR_S2_ismeretlen.tsv`): l. `naplok/SZOTAR_S2_zaras.md` 4. pont.
