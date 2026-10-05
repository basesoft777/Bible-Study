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

---

# 2. kör (a DT-F57c javítása után; tartomány `bd39b91..78eb180`)

*A jelentést a `fuggetlen-ellenor` ügynök állította össze, a fájlba az orkesztrátor írta át összefoglalva (az ügynöknek nem volt Write eszköze). Az ellenőr a `78eb180` állapotára ítélt; az ellenőrzés közben a végrehajtó a DT-F57e-t és a `kezi_ellenorzesre` indokot a `9f8a858`-ban vezette át (ezt az ellenőr nem ítélte meg). Verdikt: **ELTÉRÉS, 4 tétel.***

## Eredmény
- **OK:** az 1. kör súlyos hibája javítva. Az új alias 290 sora mind teljesíti a bdb_id-feltételt (az ellenőr a `BDB.lexicon` H-kulcs-fejléceit saját Greppel olvasta, mind a 290 pár illeszkedik, 74/74 a 2. menetben), a 14 arámi alias testvérsora arámi szócikk, a H0399→H0398 elvetve; az elvetett lista 239 sor (héber 66, arámi 173; 220 szócikk-eltérés, 19 küszöb alatti), 290+239=529; az arámi szám 187 (14+173) reprodukálható, a 198 nem; a 3 új táblasor könyvnév-stílusa igazodik, a többi 8090 sor és a fejléc változatlan; licenc „tisztázatlan” megnevezve; a zárójelentés neve és a docstring rendben; DT-F57c 🟢, DT-F57d 🟡; 3. főszabály rendben.
- **NEM ELLENŐRIZHETŐ:** a tesztek futása, a `--m2` idempotenciája futtatással, a README SHA-256-ja, a CI-jelentés egyezése. Az `origin/main` behúzása nélkül `--diff-alap origin/main` mellett E5 hibák jönnek (30, a main előrébb jár); ez a merge-ből eredő artefaktum.

## Eltérések és állapotuk
1. **(közepes)** A README és a DT-F57c a 19 kiesett sort „rövid törzs”/„stub-sor” indokkal írja le; a 22 testvérsorból csak 4 csonk (H0415, H0416, H7249, H8054), a többi teljes szócikk. Az elvetés valódi oka a szócikk-eltérés vagy a hozzáfűzött szöveg. — **Nyitott (dokumentáció pontosítása).**
2. **(közepes)** A küszöb hamis negatívjai: az 5 határsávos sor (H3292→H6130, H3347→H4169, H5761→H5757, H6978→H6979, H8284→H7791) és a H0532→H0526, H7485→H7480 a lekérdezett szöveg alapján valódi alias, **egyedi beemelésre javasolt (nem küszöbmódosítással)**; a H2753→H2752, H0868/H0869→H0866 kézi döntést igényel; a többi 9 kiesett sor helyesen esett ki (14 alacsony hasonlóságú sorból pl. H3606→H6903 „qobel”, H4078→H4100 „mah”). — **Nyitott, a felhasználó dönt.**
3. **(alacsony)** A 3 új táblasor feje diakritikus átírást használ (ʾărîsay, mahătallôt, māqôm), a meglévő sorok egyszerűsítettet (akal, mah, shur); a brief M2 „ugyanaz a fej” előírásától eltér. — **Nyitott.**
4. **(alacsony)** A DT-F57e a `78eb180`-ban nem volt rögzítve. — **Javítva** a `9f8a858`-ban (DT-F57e 🟢, az 5 határsávos sor `kezi_ellenorzesre`).
