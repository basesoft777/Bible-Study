# F201 jelentés — a gépi Actionök három folyamathibája

*2026-11-11 · sonnet · brief: `F201_SZAMKIOSZTAS_BRIEF.md` · döntések: DT-F201a–c (javaslat, jóváhagyás a felhasználóé)*

## Mi változott
| Hiba | Javítás | Hol |
|---|---|---|
| 1. számkiosztás után piros E28/E35 | a csere után ugyanabban a commitban újragenerálás | `eszkozok/szamkiosztas_ujragen.py`, `feladatok.yml` |
| 2. azonos F-szám párhuzamos ágakon | `kovetkezo_szam --tavoli` (távoli ágak briefjei és foglalások), `--foglal <ágnév>` (atomi push `foglalas/F<nn>`); takarítás | `eszkozok/feladatok.py`, `eszkozok/foglalas_takarit.py`, `/befogad` |
| 3. szétszórt gépi commitok | egy workflow, egy futás, egy commit | `feladatok.yml` (a `szamkiosztas.yml` törölve; `gerinc_terkep.yml`, `jelolt_eloszures.yml` csak ütemezett/kézi), `eszkozok/gepi_commit_uzenet.py` |

**Miért az újragenerálás, és nem a „szám nélküli lap”:** a lap a DT-számból oldja fel a döntés dátumát („szerkesztői döntés, 2026-11-10”), ezért a szám nélküli lap más szöveg lenne, és ehhez a generátor tartalmi részét kellene módosítani (ezen a HAMART javítókör dolgozik).
**Miért a foglalás, és nem az `F-<ágnév>` helyőrző:** a helyőrző a fájlnevek, mappák, ágnevek és pontszámok merge utáni átnevezését kívánná.

## Teszt: a számkiosztás utáni E28/E35 (a workflow lépéseinek helyi szimulációja)
Próba-állapot: a #182 számkiosztása előtti commit (`7095bc63^`, 31 helyőrző: DT-F141a, DT-F182a…r, N-F182a…). A lépések: `szamkiosztas.py --ir`, majd E28 (teljes) és E35.

| Lépés | E28 | E35 |
|---|---|---|
| csak a számkiosztás (a régi workflow) | **1 találat** (HAMART-001: a „közös forrásmegjelölések” sor eltér) | **8 találat** (`nyilt_mag/*`) |
| + `szamkiosztas_ujragen.py`, commit (az új workflow) | **0** (a `PARDES_E28_CSAK=HAMART-001` szűréssel; az első futásban csak ez a lap volt piros) | **0** |

Az újragenerálás idempotens: a jelenlegi fán lefuttatva (Windows, `autocrlf`) a `git diff --ignore-space-at-eol` üres, tehát számkiosztás nélkül nincs diff, nincs commit.

## Egységtesztek
`eszkozok/teszt_f201.py` (7 teszt: távoli ág briefje számít, két foglalás két számot ad, a versenyhelyzet újrapróbál, a takarítás törli a teljesült foglalást, a commit-üzenet első sora) és `eszkozok/teszt_feladatok.py` (134) zöld. Foglalás-atomitás: helyi bare origin ellen, második push ugyanarra a refre elutasítva.

## Amit nem lehet itt kipróbálni
- Maga a workflow (App-token, push a main-re) csak a main-en fut; a próbája `workflow_dispatch` a merge után. A `gerinc`/`eloszures` ágak (útvonal-szűrő) a merge utáni első releváns push-on élesednek.
- Egy hibás számkiosztás-újragenerálás a workflow-t megállítja (nincs commit, a számok kiosztatlanok maradnak a következő futásig): ez szándékos, hangos hiba.
- A PR címének `[ELLENŐRZŐ]` előtag kell (E16: `.github/` érintett).

## Nyitva
- A `/befogad` a `--foglal`-t az 5. lépésben hívja; amíg nem fut ténylegesen, az orkesztrátor adja a számot.
- A foglalás push: a CLAUDE.md „push csak kérésre” szabálya miatt a `--foglal` külön kapcsoló.

## Bővítés (az orkesztrátor kérése)
- **`.py` literálba írt helyőrző (N-F119a, N-F12d):** nincs új szabály, mert az E32 (`eszkozok/ellenorzes/szabalyok.py`, #141) ezt már jelzi az `eszkozok/**/*.py` string-literáljaiban: a már kiosztott és a merge-kor kiosztásra váró helyőrzőt is, PR-ban. A szabály a diff által nem érintett sorokat JELENTÉS-re minősíti (D8), ezért egy régi literál nem blokkol, de látszik. A `szamkiosztas.py` a `.py`-t szándékosan nem írja át (egy kód-literál átírása a tábla és a generátor eltérését rejtené el). Ha egy konkrét eset (pl. `bdb_jelolt/forras_javit.py`) mégis átcsúszott, annak az E32 `--teljes` futása mutatja meg a sorát; ezt külön tétel vizsgálja.
- **Rossz helyű döntésfájl:** új E26-ág (DT-F201d): a helyőrzős tételt tartalmazó fájl csak a `dontesek/uj/`, `nyitott/uj/` mappában vagy a fő fájlban állhat; a `dontes/`, a `dontesek/` és a `nyitott/` gyökerében álló .md HIBA. Teszt: `test_szamkiosztas.py` (16 teszt zöld).
