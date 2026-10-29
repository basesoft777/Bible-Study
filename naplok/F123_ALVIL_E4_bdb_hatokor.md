# F123.ALVIL.J1: a B1 szeletelő-javításának hatóköre (ELLENOR_F123_ALVIL-001 E4)

`scope=adat/bdb_vers_jelentes.tsv, 52919dfd^ ↔ 5fa4f291, a H7585-ön kívüli változó sorok | forras=naplok/F123_ALVIL_E4_bdb_hatokor.py (mérce: konkordancia/BDB_teljes_unabridged.tsv; keresztpróba: adat/bdb_szakaszok.tsv) | ts=2026-10-29`

Az ellenőr (E4) ezt kifogásolta: az F123.ALVIL.B1 (52919dfd) a `bdb_szelet._szam_minta`-ban a „] N” jelölőt is jelentés-sorszámnak fogadja el. Ennek a hatása a H7585-ön kívül nem volt sorszinten besorolva. A `adat/bdb_vers_jelentes.tsv` diffje a B1 szülője és a HEAD között **185 sort** érint: a H7585 4 sorát (ez a B1 célpontja) és 6 másik szócikk **181 sorát**. Mind a 185 sorban kizárólag az `utvonal` mező változik; a többi mező bájtra azonos.

## Eredmény

| Strong | sor | régi → új útvonal | javulás | semleges | rontás | eldöntetlen (gépi) | ebből kézzel: javulás |
|---|---:|---|---:|---:|---:|---:|---:|
| H0145 | 2 | tagolatlan → -/1, -/2 | 2 | 0 | 0 | 0 | — |
| H2811 | 7 | -/5 → -/6, -/7, -/8 | 7 | 0 | 0 | 0 | — |
| H6453 | 38 | -/2 → -/3 | 38 | 0 | 0 | 0 | — |
| H6563 | 2 | tagolatlan → -/1, -/2 | 2 | 0 | 0 | 0 | — |
| H6904 | 3 | tagolatlan → -/1, -/2 | 3 | 0 | 0 | 0 | — |
| H7200 | 129 | Qal/5/b–h → Qal/6/a–h, 7/a–f, 8/a–c | 104 | 4 | 0 | 21 | 21 |
| **össz.** | **181** | | **156** | **4** | **0** | **21** | **21** |

**A kézi besorolás után 177 javulás, 4 semleges (jelölt), 0 rontás és 0 eldöntetlen.** Rontó sor nincs.

*Javítás (F123.ALVIL.J22, ELLENOR_F123_ALVIL-001_2 ELTÉRÉS-5): az első változat 181 javulást adott. A H7200 341–344. sora (1Krón 17:17, 2Sám 7:19, Ez 12:12, Mik 6:9) a BDB Qal 8/c szeletének végén, a „— Corrupt is …” szövegkritikai jegyzetben áll („1Chr 17:17 … 2Sam 7:19 …; Ezek 12:12 read probably Niph`al …; Micah 6:9 read probably …”), nem a „c. with …” jelentés példájaként. Az új útvonal (`Qal/8/c`) a nem létező régi `Qal/5/h`-nál jobb helyen áll, de hamis jelentéspont alatt; ezért „semleges, jelölt” (a szkript `JEGYZET` szabálya: ha a szelet eleje és a sor között „— Corrupt is” áll).*

Soronkénti adat: `naplok/F123_ALVIL_E4_bdb_hatokor.tsv`. Oszlopai: strong, sorszam, poz, nyers, karoli_vers, régi és új útvonal, gépi besorolás, indok, az új útvonal szelete a `lapit`-szövegben, valamint a kézi besorolás.

## Módszer

- **Párosítás.** A szkript a `git show 52919dfd^:adat/bdb_vers_jelentes.tsv` és a `HEAD` tábláját olvassa be (`split('\t')`). A párosítás kulcsa a `strong + sorszam + poz`; a kulcshalmaz és a fejléc a két változatban azonos. A szkript minden sornál ellenőrzi, hogy a `poz` a `lapit` szövegben a `nyers` hivatkozásra mutat. Vers-folytatásnál (`, 24`) a `poz` a számra mutat.
- **Elsődleges mérce.** Ez a BDB angol szócikkszövege (`konkordancia/BDB_teljes_unabridged.tsv`), a `bdb_szelet.lapit` alakjában. A `poz` erre az alakra vonatkozik; a `lapit` csak a sortörést cseréli szóközre, és az „1.a” alakot „1. a.”-ra. A szeletelőt a mérce nem használja. Láncolt jelölőkeresés:
  - A számjelölőket (1., 2., …) sorban keresi, mindegyiket az előző után. Jelölőnek számít az önálló 1–2 jegyű szám, amely előtt szóköz vagy a szöveg eleje áll, utána pedig pont vagy szóköz, majd latin vagy héber betű, „>” vagy „(”.
  - A számon belül a betűjelölőket (a., b., …) ugyanígy keresi, a következő számjelölőig.
  - Törzsnél (Qal) a keresés a törzsnév első előfordulásától a következő, mondathatár után álló törzsnévig tart.
  - Egy útvonal szelete a jelölőjétől a következő, azonos vagy magasabb szintű jelölőig tart. A sor akkor helyes, ha a `poz` ebben a szeletben áll.
  - A `tagolatlan` csak akkor helyes, ha a szócikkben nincs számjelölő.
  - Ha egy útvonal számjelölője megvan, de a betűpontja a szám szeletében nincs, az a BDB-ben nem létező pont (példa: `Qal/5/c`, holott a Qal 5. pontja csak a.–b.). Ilyenkor a besorolás hibás.
- **Keresztpróba.** Az `adat/bdb_szakaszok.tsv` a `bont.py` kimenete a DictBDB.json-ból: más forrás és más bontó. A szkript a hivatkozás előtti 60/40/28/18 karakteres szövegrészt a szakaszok szövegében keresi, és csak a talált szakasz szám/betű részét veti össze az új útvonallal; a törzset nem. Eredmény: 153 sorban egyezik, 4 sorban nem egyértelmű, 24 sorban ellentmond.
- **Besorolás.**
  - javulás: az új útvonal helyes, a régi nem;
  - rontás: a régi helyes, az új nem;
  - semleges: mindkettő helyes, mindkettő hibás, vagy nem csak az `utvonal` változott;
  - eldöntetlen: a mérce nem talál jelölőt, vagy a keresztpróba ellentmond egy gépi javulásnak.

## A gépileg eldöntetlen sorok (H7200), kézzel

A keresztpróba ellentmondása 24 sort tett eldöntetlenné; ebből 3 (8/c: 1Krón 17:17, 2Sám 7:19, Ez 12:12) a J22 óta a fenti jegyzet-szabály szerint semleges, jelölt. A maradék 21 az elsődleges mérce szerint javulás. A régi útvonal (`Qal/5/g`, `Qal/5/h`) a BDB-ben nem létező pont, az új (`Qal/6/g`, `6/h`, `8/a`, `8/b`, `8/c`) a sort tartalmazó szelet.

A BDB-szöveget néztem meg (H7200, `lapit`). A „Niph`al” szó ötször fordul elő benne: a 8135., 9855., 10581., 10654. és 14001. pozíción. Ebből csak a 10654. törzsfej („GASm. Niph`al Perfect …”), ez zárja a Qal-t. A többi szövegközi utalás:

- 8135.: „compare v^b, Niph`al and Di”, a Qal 6/g-ben;
- 9855.: „compare Niph`al Num 14:14”, a Qal 8/a-ban;
- 10581.: „read probably Niph`al”, a Qal 8/c-ben.

A **`bdb_szakaszok.tsv` a 8135. és a 9855. pozíciót törzsfejnek veszi.** Ezért a Qal 6/g második felét, a 6/h-t és a 7. pontot Niph'al alá teszi (`Niph'al/-/-`, `Niph'al/-/h`, `Niph'al/7/a`…), a 8/a második felét, a 8/b-t és a 8/c-t pedig `Niph'al/-/-`, `Niph'al/-/b`, `Niph'al/-/c` alá. **A keresztpróba ellentmondása tehát a `bdb_szakaszok` hibája, nem a B1-é.** Ugyanez a hiba okozza, hogy a 7. pont sorai a szám/betű-összevetésben egyeznek: ott a szám helyes, csak a törzs hamis.

Mit láttam a sorok előtt (kivonat):

- a 6/g sor (Est 2:9) a „g. look out, find out” pont végén áll, a „compare … Niph`al and Di” utalás után, a „h.” előtt;
- a 6/h sor (1Móz 39:23) a „h. look at = concern oneself about” pontban áll;
- a 15 db 8/a sor a „8. a. with ב, literally, look into”, majd „look upon, sometimes gloat over” részben áll (Jób 33:28 … Zsolt 118:7);
- a 2 db 8/b sor a „b. with אֶל person” részben áll;
- az 5 db 8/c sorból 2 (1Sám 16:7, Zsolt 64:6) a „c. with … לַלֵּבָב” részben áll; 3 (1Krón 17:17, 2Sám 7:19, Ez 12:12) a „— Corrupt is …” jegyzetben, a valódi Niph`al-fej (10654.) előtt.

**Kézi besorolás: 21 javulás, 3 semleges, jelölt** (a negyedik jegyzet-sor, a Mik 6:9, gépileg sem volt eldöntetlen). A TSV `kezi_besorolas` oszlopa rögzíti.

## Tudnivaló, nem a B1 hatóköre

A `adat/bdb_szakaszok.tsv` H7200-tagolása (F107, `bont.py`) a fenti szövegközi „Niph`al” utalásokat törzsfejnek veszi. Ezt a hibát a B1 nem érinti és nem javítja. Itt csak rögzítem; a javítása nem e kör feladata.
