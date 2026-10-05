# Független ellenőrzés: F57 (BDB_STRONG_POTLAS)

*A jelentést a `fuggetlen-ellenor` ügynök állította össze (tartomány `bd39b91..60ce161`, 4 commit); a fájlba az orkesztrátor írta át (az ügynöknek nem volt Write eszköze). Verdikt: **ELTÉRÉS, 6 tétel, ebből 1 súlyos.** Az ügynök nem futtathatott szkriptet, tesztet és sha256-ot, ezek NEM ELLENŐRIZHETŐ minősítést kaptak.*

## Eredmény
- **OK:** a `BDB_teljes_unabridged.tsv` meglévő sorai bájtra változatlanok, csak +3 sor (H4725, H4123, H0747); a 3 `egyertelmu` pár 1:1 egyezéssel, indokkal és proveniencia-sorral dokumentált, `tobb_jelolt` 0, a tipp-sorok jelöltek maradtak; az alias külön fájl, a H0136/H0341 nincs a kanonikus táblában; DT-F57a 🟢 és DT-F57b (ir-bővítés) önálló tétel; nincs csv modul, az UTF-8 wrapper az importok után áll; E2–E16, E19, E12–E15: 0 találat; a ⛔ pont betartva (az írás a DT-F57a 🟢 után).
- **NEM ELLENŐRIZHETŐ:** a 11 teszt futása, a `--m2` idempotenciája futtatással, a README új SHA-256-ja, a CI-jelentés egyezése. (Kódolvasás szerint az `--m2` idempotens.)

## Eltérések súlyossági sorrendben
1. **(súlyos) Az alias-tábla 198 arámi BDB-szócikket héber testvérsorra old fel.** Példa: H0399 → H0398 (BDB9297, arámi `akal`), de a táblában a H0398 sora a héber szócikk. Az „igen” jelölés (513/529) a kódban csak azt jelenti, hogy a címszó mássalhangzói rész-sztringként előfordulnak a testvér-sor mássalhangzó-láncában, ez rövid gyököknél szinte mindig igaz, nem igazolás. A DT-F57a (c) döntés ezért hamis előfeltevésre épült az arámi csoportnál; sérül a 3. főszabály (hiányt nem töltünk ki gyenge anyaggal) és a brief arámi külön listára vonatkozó pontja. Az alias-generátor nem vizsgálja a nyelvet, holott a párosító igen. A valódi hiány (kb. 190+ arámi szócikk) nincs jelölve. *Tartalmi döntés a felhasználóé.*
2. **(közepes)** Az új táblasorok könyvnév-rövidítése és írásjel-szóközei eltérnek a meglévő soroktól (új: 1Kgs/Ps/Hos…, régi: 1Kin/Psa/Hosea…; szóköz az írásjel előtt), és ez nincs dokumentálva; a hivatkozás-feloldó fogyasztók nem oldják fel őket.
3. **(alacsony)** A README K7 SHA-256 mezője (15–16. sor) a régi értéket mutatja, ellentmond a „Pótlás” szakasz új hash-ének; az egyezés a fájllal nem ellenőrzött.
4. **(alacsony)** A README a BDB-licencet „közkincs”-ként írja, a `licencek.tsv` szerinti „tisztázatlan” státusz kimarad.
5. **(alacsony)** A zárójelentés neve (`F57_zaras.md`) eltér a brief M3 `BDB_STRONG_POTLAS_zaras.md` nevétől; a DT-F57b ezt pontatlanul „előírt”-nak nevezi.
6. **(alacsony)** A `bdb_strong_potlas.py` docstringje szerint a szkript nem írja a táblát, a `--m2` viszont írja.
