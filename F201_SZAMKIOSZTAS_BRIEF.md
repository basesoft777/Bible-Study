---
feladat: 201
cim: A gépi Actionök három folyamathibája — a számkiosztás utáni E28, az F-szám ütközése, a szétszórt gépi commitok
kod: SZAMKIOSZTAS
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: fut
ag: claude/f201-szamkiosztas-083885
ad: a `szamkiosztas` workflow a csere után újragenerálja a számtól függő nézeteket; az F-szám atomi foglalása az originen; egy futás egy gépi commit
kovetkezo: "Te: a draft PR áttekintése; merge-et az orkesztrátor végzi a felhasználó kérésére"
munka: folyamat
olvas: [.github/workflows/feladatok.yml, .github/workflows/gerinc_terkep.yml, .github/workflows/jelolt_eloszures.yml, eszkozok/szamkiosztas.py, eszkozok/feladatok.py]
ir: [.github/workflows/feladatok.yml, .github/workflows/szamkiosztas.yml, .github/workflows/gerinc_terkep.yml, .github/workflows/jelolt_eloszures.yml, eszkozok/szamkiosztas_ujragen.py, eszkozok/gepi_commit_uzenet.py, eszkozok/foglalas_takarit.py, eszkozok/feladatok.py, eszkozok/szamkiosztas.py, eszkozok/teszt_f201.py, .claude/commands/befogad.md, dontesek/uj/f201-szamkiosztas-083885.md, F201_SZAMKIOSZTAS_BRIEF.md, naplok/F201_jelentes.md]
fugg: []
nem_fugg: [111, 121, 123, 133, 151, 156, 182, 188, 192]
---

# F201_SZAMKIOSZTAS_BRIEF.md — A gépi Actionök három folyamathibája

*FELADATOK #201 · Modell: sonnet · v1 · 2026.11.11*

**Jóváhagyás (a felhasználó, 2026-11-11, az orkesztrátor közvetítésében), szó szerint:** „csináljuk meg a generátor hibákat”.

**Hatókör.** Csak a GitHub Actionök és a feladatkövető eszközei. A `lexikon/`-hoz, a `motivumok/`-hoz és az `eszkozok/lexikon_general.py` tartalmi részéhez nem nyúl (a HAMART javítókör és az F200 dolgozik rajtuk); a generátort csak hívja.

## A három hiba és a javítás
1. **A számkiosztás után a main bepirul (E28/E35).** A lap a DT-számból oldja fel a döntés dátumát, ezért a szám nélküli lap más szöveg volna; ezért a javítás az újragenerálás ugyanabban a commitban: `eszkozok/szamkiosztas_ujragen.py` (marker-blokkok, migrált lapok a saját `ts=` dátumukkal, nyílt mag). DT-F201a.
2. **Azonos F-szám párhuzamos ágakon.** `feladatok.py kovetkezo_szam --tavoli` (a távoli ágak briefjei és a foglalások is számítanak), `--foglal <ágnév>` (atomi push a `foglalas/F<nn>` ágra); a teljesült foglalást a workflow törli (`foglalas_takarit.py`). DT-F201b.
3. **Szétszórt gépi commitok.** A `szamkiosztas.yml` megszűnik; a `feladatok.yml` egy futásban végzi a számkiosztást, az újragenerálást, a FELADATOK.md-et és (ha érintett) a GERINC_TERKEP-et és az ELOSZURES-t, egyetlen commitban. DT-F201c.

## Garanciák
- G1: egy próba-helyőrzővel (a #182 számkiosztása előtti állapot) a workflow lépéseinek helyi szimulációja: újragenerálás nélkül E28/E35 piros, vele zöld (`naplok/F201_jelentes.md`).
- G2: a `szamkiosztas:` commit-üzenet első sora változatlan (E32).
- ⛔ A merge nem ennek a sessionnek a dolga; a workflow csak a main-en futtatható, a próbája `workflow_dispatch` a merge után.
