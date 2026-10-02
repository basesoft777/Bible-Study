# ELLENOR_ALLAPOT_JAVITAS

Tétel: F47 (ALLAPOT_ELLENTMONDASOK) · Tartomány: `origin/main..HEAD` (origin/main = 4eb39ae; b1fa21a, 6424457, b9278ff)
Ellenőr: `fuggetlen-ellenor` (fájlíró eszköze nem volt; az orkesztrátor mentette a jelentés lényegét, az eltéréseket tartalmilag változtatás nélkül). Az ellenőr a `feladatok.py`-t a szerepköre miatt nem futtatta; a #22 jelölt-státuszát a végrehajtó jelentése szerint a `jeloltek` kimenete igazolja (`KIHAGYVA: állapot fut`).

Eredmény: **ELTÉRÉS: 5 tétel**. OK: J1.1, J1.2, J2.1, J2.2, J3.1, J3.2, a DT5 és a DT-F24 sor byte-azonos, táblaszerkezet, commitok, E2–E19 helyi futás 0 találat, `adat/` és `konkordancia/` Δ=0.

| # | Súly | Hely | Eltérés |
|---|---|---|---|
| 1 | magas | `DONTESEK.md:19` (DT6 Döntés cella) | A beírt „a (b) elfogadva, a többi ((a), (c)–(g)) nem választott” elvetést rögzít az (a)-ra és (f)-re, holott az eredeti javaslat (a)+(b)+(f) volt; a brief tényállása csak a (b) jóváhagyását mondja ki. Az (e) és (g) a sorban továbbra is „döntésre vár”, miközben a sor 🟢. A végrehajtó a zárójelentésben jelezte az ellentmondást, de nem állt meg (a brief megállást ír elő). |
| 2 | közepes | `F22_KAROLI_STRONG_BRIEF.md:159` | A D9 sor szerint a DT-F22c „nyitva”, a `DONTESEK.md:36` szerint ✅; a zárójelentés „nyitottként nincs” állítása téves. |
| 3 | alacsony | `DONTESEK.md:15`, `:29` | A DT-F21j sora szerint a #22 „marad `dontesre_var`”; ütközik az `allapot: fut` értékkel. A brief hatókörén kívül, a DT-F21j 🟢 marad. |
| 4 | alacsony | `F22_KAROLI_STRONG_BRIEF.md:11` | A régi `kovetkezo` nyitott tételei (4Móz 30 kézi jóváhagyás, Ézs 9:17–20, PR #114 merge, zárt összevetés) kiestek a követett mezőből; csak a `naplok/F22_*_jelentes.md`-ben maradtak. |
| 5 | alacsony | `DONTESEK.md:19` | A DT6 Döntés cellája nem nevezi meg a döntéshozót („Felhasználó, 2026.10.02 (chat)” formát használják a szomszéd sorok). |

Megállás: az 1. pont felhasználói döntést igényel (a brief szerint „új döntést nem hozol”); a PR addig nem nyílik meg.

---

## 2. kör (a javító kör után; tartomány: `origin/main..HEAD`, 8d91f48-ig)

Eredmény: az 1–5. korábbi eltérés megoldva (DT6: csak a (b), „nincs eldöntve”; D9: DT-F22c lezárva; DT-F21j: kiegészítve; döntéshozó megnevezve); DT5, DT-F24, DT-F22a/c byte-azonos; táblaszerkezet, E5, E2–E19 helyi futás: 0 találat; `adat/`, `konkordancia/` Δ=0. Az ellenőr 3 új eltérést jelzett:

| # | Súly | Hely | Eltérés | Kezelés |
|---|---|---|---|---|
| 1 | közepes | `F41_BSB_UJRAMERES_BRIEF.md:57–59, 112, 128, 131` | A #41 briefje az (a), (d), (e), (f) pontot eldöntöttként kezeli, és a DT6-ot átírná / ✅-re tenné; ütközik az „a többi pont nincs eldöntve” szöveggel. A #41 JELOLT. | **felhasználói döntés kell a #41 indítása előtt** (nem az F47 hatóköre) |
| 2 | alacsony | `DONTESEK.md:29` (DT-F21g ✅) | „a #22 `dontesre_var` marad” szöveg ütközik az `allapot: fut` értékkel. | a ✅ sor szövegét nem módosítottuk; a kiegészítés a DT-F21j sorában (15.); felhasználói döntés, ha mégis kell |
| 3 | alacsony | `F22_KAROLI_STRONG_BRIEF.md:11` | a `kovetkezo`-ből kiesett a „következő könyv előtt” kapu, a „jelzett fejezetek” és a „hamis”. | javítva a 2. kör után (a forrás: `naplok/F22_3Moz_jelentes.md:31`) |
