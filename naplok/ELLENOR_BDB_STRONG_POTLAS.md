# Független ellenőrzés: F57 (BDB_STRONG_POTLAS)

*A jelentést a `fuggetlen-ellenor` ügynök állította össze (tartomány `bd39b91..60ce161`, 4 commit); a fájlba az orkesztrátor írta át (az ügynöknek nem volt Write eszköze). Verdikt: **ELTÉRÉS, 6 tétel, ebből 1 súlyos.** Az ügynök nem futtathatott szkriptet, tesztet és sha256-ot, ezek NEM ELLENŐRIZHETŐ minősítést kaptak.*

## Eredmény
- **OK:** a `BDB_teljes_unabridged.tsv` meglévő sorai bájtra változatlanok, csak +3 sor (H4725, H4123, H0747); a 3 `egyertelmu` pár 1:1 egyezéssel, indokkal és proveniencia-sorral dokumentált, `tobb_jelolt` 0, a tipp-sorok jelöltek maradtak; az alias külön fájl, a H0136/H0341 nincs a kanonikus táblában; DT37 🟢 és DT38 (ir-bővítés) önálló tétel; nincs csv modul, az UTF-8 wrapper az importok után áll; E2–E16, E19, E12–E15: 0 találat; a ⛔ pont betartva (az írás a DT37 🟢 után).
- **NEM ELLENŐRIZHETŐ:** a 11 teszt futása, a `--m2` idempotenciája futtatással, a README új SHA-256-ja, a CI-jelentés egyezése. (Kódolvasás szerint az `--m2` idempotens.)

## Eltérések súlyossági sorrendben
1. **(súlyos) Az alias-tábla 198 arámi BDB-szócikket héber testvérsorra old fel.** Példa: H0399 → H0398 (BDB9297, arámi `akal`), de a táblában a H0398 sora a héber szócikk. Az „igen” jelölés (513/529) a kódban csak azt jelenti, hogy a címszó mássalhangzói rész-sztringként előfordulnak a testvér-sor mássalhangzó-láncában, ez rövid gyököknél szinte mindig igaz, nem igazolás. A DT37 (c) döntés ezért hamis előfeltevésre épült az arámi csoportnál; sérül a 3. főszabály (hiányt nem töltünk ki gyenge anyaggal) és a brief arámi külön listára vonatkozó pontja. Az alias-generátor nem vizsgálja a nyelvet, holott a párosító igen. A valódi hiány (kb. 190+ arámi szócikk) nincs jelölve. *Tartalmi döntés a felhasználóé.*
2. **(közepes)** Az új táblasorok könyvnév-rövidítése és írásjel-szóközei eltérnek a meglévő soroktól (új: 1Kgs/Ps/Hos…, régi: 1Kin/Psa/Hosea…; szóköz az írásjel előtt), és ez nincs dokumentálva; a hivatkozás-feloldó fogyasztók nem oldják fel őket.
3. **(alacsony)** A README K7 SHA-256 mezője (15–16. sor) a régi értéket mutatja, ellentmond a „Pótlás” szakasz új hash-ének; az egyezés a fájllal nem ellenőrzött.
4. **(alacsony)** A README a BDB-licencet „közkincs”-ként írja, a `licencek.tsv` szerinti „tisztázatlan” státusz kimarad.
5. **(alacsony)** A zárójelentés neve (`F57_zaras.md`) eltér a brief M3 `BDB_STRONG_POTLAS_zaras.md` nevétől; a DT38 ezt pontatlanul „előírt”-nak nevezi.
6. **(alacsony)** A `bdb_strong_potlas.py` docstringje szerint a szkript nem írja a táblát, a `--m2` viszont írja.

---

# 2. kör (a DT39 javítása után; tartomány `bd39b91..78eb180`)

*A jelentést a `fuggetlen-ellenor` ügynök állította össze, a fájlba az orkesztrátor írta át összefoglalva (az ügynöknek nem volt Write eszköze). Az ellenőr a `78eb180` állapotára ítélt; az ellenőrzés közben a végrehajtó a DT41-t és a `kezi_ellenorzesre` indokot a `9f8a858`-ban vezette át (ezt az ellenőr nem ítélte meg). Verdikt: **ELTÉRÉS, 4 tétel.***

## Eredmény
- **OK:** az 1. kör súlyos hibája javítva. Az új alias 290 sora mind teljesíti a bdb_id-feltételt (az ellenőr a `BDB.lexicon` H-kulcs-fejléceit saját Greppel olvasta, mind a 290 pár illeszkedik, 74/74 a 2. menetben), a 14 arámi alias testvérsora arámi szócikk, a H0399→H0398 elvetve; az elvetett lista 239 sor (héber 66, arámi 173; 220 szócikk-eltérés, 19 küszöb alatti), 290+239=529; az arámi szám 187 (14+173) reprodukálható, a 198 nem; a 3 új táblasor könyvnév-stílusa igazodik, a többi 8090 sor és a fejléc változatlan; licenc „tisztázatlan” megnevezve; a zárójelentés neve és a docstring rendben; DT39 🟢, DT40 🟡; 3. főszabály rendben.
- **NEM ELLENŐRIZHETŐ:** a tesztek futása, a `--m2` idempotenciája futtatással, a README SHA-256-ja, a CI-jelentés egyezése. Az `origin/main` behúzása nélkül `--diff-alap origin/main` mellett E5 hibák jönnek (30, a main előrébb jár); ez a merge-ből eredő artefaktum.

## Eltérések és állapotuk
1. **(közepes)** A README és a DT39 a 19 kiesett sort „rövid törzs”/„stub-sor” indokkal írja le; a 22 testvérsorból csak 4 csonk (H0415, H0416, H7249, H8054), a többi teljes szócikk. Az elvetés valódi oka a szócikk-eltérés vagy a hozzáfűzött szöveg. — **Nyitott (dokumentáció pontosítása).**
2. **(közepes)** A küszöb hamis negatívjai: az 5 határsávos sor (H3292→H6130, H3347→H4169, H5761→H5757, H6978→H6979, H8284→H7791) és a H0532→H0526, H7485→H7480 a lekérdezett szöveg alapján valódi alias, **egyedi beemelésre javasolt (nem küszöbmódosítással)**; a H2753→H2752, H0868/H0869→H0866 kézi döntést igényel; a többi 9 kiesett sor helyesen esett ki (14 alacsony hasonlóságú sorból pl. H3606→H6903 „qobel”, H4078→H4100 „mah”). — **Nyitott, a felhasználó dönt.**
3. **(alacsony)** A 3 új táblasor feje diakritikus átírást használ (ʾărîsay, mahătallôt, māqôm), a meglévő sorok egyszerűsítettet (akal, mah, shur); a brief M2 „ugyanaz a fej” előírásától eltér. — **Nyitott.**
4. **(alacsony)** A DT41 a `78eb180`-ban nem volt rögzítve. — **Javítva** a `9f8a858`-ban (DT41 🟢, az 5 határsávos sor `kezi_ellenorzesre`).

---

# 3.–5. kör (a DT42/g/h/i szabályfejlődés alatt)

*A jelentéseket a `fuggetlen-ellenor` ügynök állította össze (3. kör: `e754e6b`, 4. kör: `b08f936`, 5. záró kör: `30a9378`); a fájlba az orkesztrátor írta át összefoglalva, az ügynöknek nem volt Write eszköze. Az ügynök nem futtathatott tesztet és sha256-ot; minden lexikon-állítást a `BDB.lexicon` H-kulcs-fejléceiből és a TSV-sorokból olvasott.*

## 3. kör (`e754e6b`, DT42): ELTÉRÉS, 6 tétel
- **OK:** az alias-sorok bdb_id-egyezése és a szöveg a testvérsor elején (37 + 27 soros minta, a 6 beemelt és a 3 kérdéses sor); H3606→H6903 helyesen elvetve; az alias nem tartalmaz több testvéres sort; a 3 új táblasor és a meglévő 8090 sor.
- **Eltérések:** (1) a 52 sávbeli (0,79–0,90) elvetett sor indoka („a testvérsor más szócikk”) a 48 egytestvéres sorra címszó-szinten hamis (a DictBDB megfordítja a többszavas héber kifejezések szórendjét); a H3347→H4169 valódi alias; a H2088 ne kerüljön be (kifejezés-társcímke); a H3071/3073/3074 kézi döntés. — **Javítva a DT43-vel** (csak latin betűk az összevetésben). (2) A mérőszám jellege (aszimmetrikus, +60 ablak, 1500 korlát) nem volt leírva a döntésben. — **Javítva** (DT43). (3) 173 helyett 172 arámi sor a „nem ebből” kategóriában. — **Javítva.** (4) A H0747 feje „arisay”. — **Javítva** („Arisay”). (5) A DT39 elavult számai; (6) a proveniencia-sor és a docstring a régi feltételre hivatkozott. — **Javítva.**

## 4. kör (`b08f936`, DT43): ELTÉRÉS, 5 tétel
- **OK:** 36 alias-sor bdb_id-egyezése és szöveg-elöl-állása; a 37 `tobb_testveres` sorban tényleg több azonos szócikkbeli testvér van; H3606 elvetve, H2088 és H3071/3073/3074 kint, listázva; a 3 új sor feje, a 8090 sor bájtra azonos, az `--m2` idempotens (kódolvasás); darabszámok (256+273=529).
- **Eltérések:** (1) 3 hamis „más szócikk” címke (H0706 0,832; H6737 0,858; H8112 0,873): a testvérsor ugyanazzal a szócikkel kezdődik. — **Javítva** (`kuszob_alatt` kód, jelölt marad). (2) Nyitott tartalmi döntés (37 többtestvéres sor szűkítése, H3071/3073/3074) tétel nélkül, `lezarva` briefnél. — **Javítva** (DT44, DT45). (3) A `testver_strong` oszlop más szócikkhez tartozó Strongokat is felsorolt. — **Javítva.** (4) A DT40 elavult száma. — **Javítva.** (5) Az indok-kódok a táblában és a README/M1-ben nem egyeztek. — **Javítva** (`indok_kod` és `indok` oszlop).

## 5. (záró) kör (`30a9378`, DT44/i): ELTÉRÉS, 6 tétel; súlyos nincs, közepes 1
- **OK:** a +40 új alias sor (37 korábbi `tobb_testveres`, 3 korábbi `kezi_dontes`): bdb_id-egyezés és szöveg-elöl-állás 25 + 17 soron, csak egy testvér felel meg; H3071/3073/3074 aliasban; H2088 kint, indok kimondva; `kuszob_alatt` 3 sor ugyanazzal a címszóval kezd; `a_testversor_mas_szocikk` 9 sor valóban más szócikk; `indok_kod`/`indok`/`testver_strong` oszlopok; a meglévő 8090 sor bájtra azonos (`3 0`); darabszámok (296+233=529; arámi 14+173; héber 282+60); PR-szinten E2–E16, E19, E26: 0 HIBA.
- **Közepes (nyitott, a felhasználó dönt):** a H5853 és H5855 → H5852 alias lett (0,981), pedig a felhasználó saját mérése 0,86 volt, és kint tartani kívánta. Az ellenőr szerint a H5852 sora szó szerint a BDB5999 szócikke (Ataroth), a másik testvér (H5854) csonk, a két sor a BDB5999 alpontja, tehát az alias a szabály és az Abel-elv szerint helyes; a 0,86–0,981 eltérés oka nem ellenőrizhető. A végrehajtó a döntést a 🟢 DT44 szövegébe írta, nem külön 🟡 tételbe.
- **Alacsony — javítva a c87ac04-ben:** a DT39/f elavult számai; a H3070 csendben alias lett (most megnevezve a DT45-ben); a `kuszob_alatt` indokszövege („egyedi beemelésre javasolt”) ütközött a DT45 (c)-vel; a „0 több testvéres alias” ellenőrzés tautológia volt (most a „megfelelő testvérek száma = 1” feltételt méri; a README korlátként jelzi, hogy a címszó-heurisztika csak a legjobb testvért nézi és homonímára vak, pl. H5875/83/86 → H5871).
- **Nem javítandó:** a kör szintű CI E5 jelzése az M1-jelentés címsor-átnevezésére (PR-szinten 0 hiba).
