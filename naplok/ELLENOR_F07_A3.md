# ELLENOR_F07_A3 — `F07_THAYER_ELES_BRIEF.md`, `49aabc12..2c06eba2` (F7.A3.1–A3.3)

*A `fuggetlen-ellenor` (claude-opus-5-5) jelentése, rövidítve; a javítások a végrehajtó F7.A3.4 commitjában.*

**Eredmény: ELTÉRÉS 5 tétel (mind javítva); a többi pont OK.** OK: modell (944 új sor `claude-sonnet-5-5`), a `forditasok.tsv` +944 / −0, megjegyzés (prompt v5.2, adag, batch), 144 Strong (141 + 3 A2), mért költség (első kör 8,3977, javító 3,0331, összesen 11,4307; futó 43,9775), plafonok (17,30 / 13,16), `JAVITO_ARANY` újraszámolva (0,652 / 0,214), bukottak-tábla (11), kapu-listák, napló ≤ 15 sor, A4 számok, DT620 feltételei a maszkban (csak bevezető után, nincs bevezető nélküli ág, legfeljebb 4 token).
Nem ellenőrizhető az ellenőr körében: a tesztek futtatása, a 203 soros regresszió, `ellenoriz.py` / `feladatok.py` (a végrehajtó futtatta: SÉRTÉS 0, 0 hiba).

| # | Eltérés | Súly | Javítás |
|---|---|---|---|
| 1 | 7. szabály: a kapu az adagon belül, a javító kör után változott | közepes | az orkesztrátor előzetes, kifejezett jóváhagyásával (DT620); a napló A3 4b. pontja rögzíti |
| 2 | nincs negatív teszt 4-nél több kitöltő szóra; a kötetszám-teszt első állítása nem negatív | alacsony | új teszt (`test_a3_negy_kitolto_szonal_tobb_nem_maszkol`), a kötetszám-teszt a forrás-oldali maszkot ellenőrzi; 133 teszt zöld |
| 3 | az adag702 `kapu_eredmeny.jsonl` A2-es bizonyítéka felülíródott | alacsony | az eredeti `adag702/kapu_eredmeny_a2_eredeti.jsonl` néven megőrizve |
| 4 | a brief 9. táblájából hiányzik a DT620 | alacsony | felvéve |
| 5 | a költségtábla A3-sorából hiányzik a „becslés manual” | alacsony | pótolva |
