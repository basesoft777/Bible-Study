# ELLENOR_F78 — F78_SZEREPMATRIX_VAZ_BRIEF.md · `origin/main..claude/f78-szerepmatrix-vaz` (merge-base `c4f7003` … `55262dc`)

*Készítette: `fuggetlen-ellenor` (nincs fájlíró eszköze; az orkesztrátor mentette a jelentést, tartalmilag lerövidítve, a sorok azonosítói megtartva). Proveniencia: `manual` (az ellenőr saját `git diff`/`lekerdez.py` futtatásai). Megjegyzés: az ellenőr két szabálysértést jelzett (a `futtat.py` kimenetét szűrőn át olvasta, több parancs `cd …&&` előtaggal futott); fájlt egyik sem írt. A munkakönyvtár a futás közben `c4f7003`-ra (main) váltott, ezért az ág tartalmát blob–blob diffből olvasta.*

**Eredmény: ELTÉRÉS, 9 tétel.** Hatókör: a `FELADATOK.md`, `feladatterkep.json`, `FELADATTERKEP.html` változása a main gépi commitjából jön (`f0eaff8`), az ág nem nyúl hozzájuk (10 fájl).

| pont | eredmény | indok |
|---|---|---|
| G1 (a) | ELTÉRÉS (döntés kell) | az `adatosítva` szerep (héber 1., TBESH; ISTENTISZT-001, TEREMT-002 héber 1–2.) üres blokkot kap harmadik állapotértékkel (`adatosítva, nincs sor`); a DT80 szerint üres blokk csak `nincs adatosítva`/`javaslat` szerepnél lehet. A végrehajtó jelezte (`naplok/F78_meres.md:106`) |
| G1 (b) | ELTÉRÉS (döntés kell) | token nélküli nyelvnél (TEREMT-002 görög) a szerepfejlécek elmaradnak, egy mondat áll: a „minden szerep megjelenik” feltétel szűkítő értelmezése |
| G2 | OK | `szotar_szerepek.tsv` 22 → 26 sor, 0 törölt sor, a régi sorok bájtra változatlanok; 13–14. `javaslat`; SEMA egyezik |
| G2a | ELTÉRÉS (kicsi) | `adat/SEMA.md:693`: a `javaslat` leírás („ma: a 12. Tematikus index”) nem frissült a 13–14. szerepre |
| G3 | NEM ELLENŐRIZHETŐ | az ellenőr a teszteket nem futtathatta; a végrehajtó állítása: 13 teszt zöld, `ellenoriz` 0 hiba (az orkesztrátor `ellenoriz` futása: 0 hiba) |
| G4 | OK | az éles `lexikon/`, `torzscikk_general.py`, `general.py`, `NYITOTT_FELADATOK.md` érintetlen; a `generalt_proba/` alatt csak hozzáadás |
| G5 | OK | domén (G1941, H8414, H0922) és TWOT lekérdezéssel egyezik a renderrel; `\tTBESH\t` 0 találat a `lexikon_hivatkozasok.tsv`-ben |
| G5a | ELTÉRÉS (kicsi) | `TEREMT-002_2_SZOTARI_HATTER.md:45`: „l. a 3. szakaszt” lógó hivatkozás, a TEREMT-002 lexikonoldala nem létezik (#12b) |
| G6 | ELTÉRÉS | lásd fent; a DT-F78a-ban hivatkozott scratchpad ugyanannak a sessionnek a scratchpadje |
| D3 | ELTÉRÉS (kicsi) | a brief döntésnaplója (`F78_…_BRIEF.md:71`) a DT-F78a-t „nyitva”-nak mutatja, a DT81 hiányzik; a `DONTESEK.md` szerint mindkettő 🟢 |
| DT81 / S4 | ELTÉRÉS (döntés kell) | az S4 szerint az 5. és a 7. szerep „l. 2/b” hivatkozást kap; a megvalósítás csak az 5.-nél; a 7. szerep (SECE, kézzel a 2/b-ben) `ÜRES-BLOKK`-ot kap hivatkozás nélkül (a DT80 és az S4 itt ellentmond) |
| Teszt-lefedettség | ELTÉRÉS (kódolvasás alapján) | nem fogja: hamis `ÜRES-BLOKK` a héber `adatosítva` szerepeknél (2., 4., 6.); lógó hivatkozási cél; forrásszöveg-szivárgás a héber 3., 10., görög 10., 12–14. szerepbe (a `'\n> '` ellenőrzés csak 5 szerepre fut). Mutációs próba nem futtatható |
| M2 „bájtra azonos” | ELTÉRÉS (kicsi) | a bizonyíték karakterszám-egyezés (19 451 = 19 451), nem bájtazonosság; a „Rokon szavak” rész blob–blob diffen azonos |
| M3 próba-TORZSCIKK | ELTÉRÉS (közepes) | a `torzscikk_general.py:471` `--kimenet` esetén is az éles `lexikon/…_TUDOMANYOS.md`-ből olvas, a próba-törzscikk nem az F78 próba-lexikonoldalából készült; a nulla-diff a törzscikkre nem áll (21+/174−, whitespace nélkül 484+/637−), a mérés nem jelzi; a lefedettségi mátrix (H7121/H8034 „TBESH”, G1941 „LSJ, ha releváns”) ellentmond a próbának. Az eltolódás az F78-tól független (éles törzscikk: `300ce93`, 09-23) |
| A1–A5 | OK / nem érintett | A2, A3, A4, A5 nem érintett |
| A6 | OK, fenntartással | E12–E15 0 találat; E11/E25/E27 JELENTÉS a diffen kívüli sorokból; a munkakönyvtár-váltás miatt nem biztos, hogy az ág fájljain futott |
| Kötelező 1 | OK | törölt sorok: brief 2, SEMA 2 (cserélt), `lexikon_general.py` 27 (refaktor), TSV 0; adattartalom nem tűnt el |
| Kötelező 2 | OK | 26 kulcs = gorog/heber × {1–10, 12, 13, 14}, a 11 szándékosan kiosztatlan; kivétel a token nélküli nyelv (G1 b) |
| Kötelező 4 | OK | táblasor-Δ: csak `szotar_szerepek.tsv` +4 |
| Kötelező 5 | OK, részben NEM ELLENŐRIZHETŐ | M0 ⛔ és M2 ⛔ rendben; hogy a döntést a felhasználó hozta, a repóból nem igazolható |
| TSV csv nélkül | OK | nincs `csv` használat a diffben |

## Súlyossági sorrend

1. G1 (a), (b): két tartalmi kérdés, a felhasználó dönt.
2. DT81 S4 és DT80 ellentmondása a 7. szerepnél (SECE, 2/b).
3. A próba-TORZSCIKK az éles lexikonból készült, dokumentálatlanul tér el (#11 aranyminta).
4. Teszt-lefedettségi rések.
5. Kisebbek: G5a, D3, G2a, „bájtra azonos”.

## 2. kör — `01a1d21` (a végrehajtó F78.7–F78.8 után)

*`fuggetlen-ellenor`, `manual`. Lezárult: G1 (a) (héber 1. szerep az ISTENTISZT-001-nél a meglévő BDB-sorokra hivatkozik, TBESH-szöveg nem került vissza: `\tTBESH\t` 0 találat a `lexikon_hivatkozasok.tsv`-ben és a `forditasok.tsv`-ben), G1 (b) (`ÜRES-NYELV` jelölő), S4 (a 7. szerep „l. 2/b”), G2a (SEMA), G5a (a lógó hivatkozás jelölve), a teszt-lefedettségi rések, az éles `lexikon/` és a régi `szotar_szerepek.tsv` sorok bájtazonossága, N-F78a.*

Új eltérések (4, mind dokumentációs), javítva az F78.9-ben (`e5c3d1e`): (1) a DT82/DT83 döntési nyom (a negyedik út rögzítve, a DT83 marad 🟡); (2) a `naplok/F78_meres.md` M0/M3 táblája; (3) a brief döntésnaplója és `ir` mezője; (4) a DT80 változatai a repóba (`naplok/F78a_valtozatok/`).

NEM ELLENŐRIZHETŐ az ellenőrnek: a tesztek és az `ellenoriz` futtatása (az orkesztrátor futtatta az F78.9 után: 16 teszt OK, 102 brief 0 hiba), a hash-állítás, a CI-jelentés (az E5 HIBA a main előnyéből jön; a merge-base-szel futtatva exit 0), hogy a döntéseket a felhasználó hozta (chat). Megjegyzés: a `SZEREP_SZOTAR` TBESH-t ír a héber 1. szerephez; általános kódőr a DT-F42a ellen nincs, erről a DT83 dönt. A javítások utáni harmadik ellenőri kör nem futott (csak dokumentáció változott).
