# F84_jelentes.md — TAHOT_kivonat: a Jób 41 pótlása (F84.1 ellenőrzés)

*Feladat: FELADATOK #84 (`F84_TAHOT_JOB41_BRIEF.md`), ág: `claude/f84-tahot-job41`. Az F84.1 csak olvasott; táblát, generátort, CLAUDE.md-t nem írtam. Mérőszkriptek: a menet scratchpadjében (`f84_meres.py`, `f84_meres2.py`; nem verziózott, a számok a lenti lekérdezés-leírással reprodukálhatók). Olvasás `split('\t')`, `csv` nélkül.*

## 1. Nyitott sorok versenként és kulcsleképezés

`scope=TAHOT_kivonat_nyitott_esetek.tsv teljes, versenkénti bontás | forras=konkordancia/TAHOT_kivonat_nyitott_esetek.tsv, konkordancia/Konyv_normalizalo_tabla.tsv | ts=2026-10-09T06:12:14Z`

- 332 adatsor, mind 10 oszlopos, mind `ADATMINOSEGI_GYANU`, mind ugyanazzal az indoklással („lasd DONTES_FELULBIRALAS … Job fejezet 41”). Nem-Jób sor nincs: a fájl jelenleg **csak** ezt a 332 sort tartalmazza.
- 34 különböző `STEPBible_elsodleges` kulcs (`Job.41.1`–`Job.41.34`), 34 különböző `STEPBible_masodlagos` (`Job.40.25`–`Job.41.26`), 1:1 pár. A sorok versenként folytonos blokkban, a versek növekvő sorrendjében állnak (versen belül a szósorrendben).
- Sor/vers (Károli 41:n): 1 10 · 2 12 · 3 10 · 4 10 · 5 12 · 6 8 · 7 12 · 8 9 · 9 10 · 10 12 · 11 12 · 12 12 · 13 11 · 14 9 · 15 6 · 16 10 · 17 9 · 18 10 · 19 8 · 20 10 · 21 10 · 22 11 · 23 9 · 24 10 · 25 8 · 26 9 · 27 8 · 28 12 · 29 9 · 30 8 · 31 8 · 32 8 · 33 10 · 34 10 (összesen 332). A héber 40. / 41. fejezeti felosztás (83 / 249 sor) egyezik az F83-mal.
- Kulcsleképezés: `Konyv_normalizalo_tabla.tsv`: `Job` → `Jób`; `Job.41.n` → `Jób 41:n` (n = 1–34). MT-megfelelés (`STEPBible_masodlagos`): K 41:1–8 = MT 40:25–32, K 41:9–34 = MT 41:1–26; mind a 34 pár egyezik az F83 táblájával (0 eltérés).

## 2. Tartalmi ellenőrzés

`scope=34 vers, Strong-halmaz (H9xxx elöljárók nélkül) nyitott sor vs. Macula MT-vers; Károli-szöveg + angol glossz 6 versen | forras=konkordancia/TAHOT_kivonat_nyitott_esetek.tsv, konkordancia/Macula_heber_Job.tsv, konkordancia/Karoli_1908.tsv | ts=2026-10-09T06:12:14Z`

- **Strong-egyezés mind a 34 versre** (nem csak 5-re): Jaccard min 0,83, medián 1,00, max 1,00; mind ≥ 0,7. A különbség 4 versben (K 41:19, 20, 21, 25) egyetlen szám: a Macula H4480 (מִן, „-tól”), amelynek a nyitott sorokban nincs külön H4480-sora (értelmezés: a TAHOT a mem-elöljárót H9xxx-előtagként kezeli; külön nem ellenőriztem).
- **Versillesztés-próba:** mind a 34 versnél a megadott MT-vers adja a legjobb Strong-egyezést a Macula 40–41. fejezetének versei közül (34/34), tehát a 41. fejezet nincs eltolva.
- **Károli-szöveg tartalmi illeszkedése** (6 vers, a kért 5 helyett):
  - K 41:1 „Kihúzhatod-é a leviáthánt horoggal … nyelvét kötéllel?” = „will you draw out? Leviathan with a fish hook and with a cord … tongue” (H4900, H3882).
  - K 41:8 „megemlékezzél, hogy a harczot nem ismételed” = „remember [the] battle may not you repeat”.
  - K 41:9 „az ő reménykedése csalárd” = „hope his it is proved a lie”.
  - K 41:17 „Egyik a másikhoz tapad, egymást tartják” = „each on brother its they are joined together they grasp one another”.
  - **K 41:25 „Hogyha felkél, hősök is remegnek; ijedtökben veszteg állnak.” = „from uprising its they are afraid mighty ones from crashing they are bewildered”** (8 sor; MT 41:17): tartalmilag egyezik; a vers rendes, rövid (63 karakteres) Károli-vers.
  - K 41:34 „Lenéz minden nagy állatot, ő a király minden ragadozó felett.” = „[he] sees every exalted [one] … king over all [the] sons of pride”.
- **Jób 41:25 lelete.** A `Karoli_adatminosegi_anomaliak.tsv` 3. sora szerint a Jób 41:25 az eredeti Károli-szövegben 719 karakteres, összeolvadt vers volt, állapota viszont: **„JAVITVA — 10 versre bontva (Jób 41:25-34 …), a fejezet így 34 versre nőtt”** (MEK 00161). A `Karoli_1908.tsv` ma a javított állapotot tartalmazza (41:24–28 szövege ellenőrizve, a 41:25–34 mind önálló vers). A generátor indoklásának „Jób 41:25 összeolvadt vers” állítása tehát **elavult** (a javítás előtti állapotra szól), és a szúrópróba eltérést nem mutat.

## 3. Oszlopszerkezet (10 → 7)

`scope=fejlécek és mintasorok | forras=konkordancia/TAHOT_kivonat_nyitott_esetek.tsv, konkordancia/TAHOT_kivonat.tsv (Jób 40, 42 sorai) | ts=2026-10-09T06:12:34Z`

| nyitott (0-alapú oszlop) | fő kivonat (0-alapú) |
|---|---|
| 0 `STEPBible_elsodleges` (`Job.41.n`) | 0 `Igehely` = `Jób 41:n` (a normalizáló táblán át; a kulcs ez, nem a másodlagos) |
| 1 `STEPBible_masodlagos` | nem kerül át |
| 2 `Státusz` | nem kerül át |
| 3 `Indoklás` | nem kerül át |
| 4 `Strong-szám` | 1 `Strong-szám` |
| 5 `Ragozott alak` | 2 `Ragozott alak` |
| 6 `Kiejtés` | 3 `Kiejtés` |
| 7 `Szótő` | 4 `Szótő` |
| 8 `Rövid jelentés` | 5 `Rövid jelentés` |
| 9 `Angol tükörfordítás` | 6 `Angol tükörfordítás` |

Mintaegyezés: a fő kivonat Jób 40/42 sorai `Jób 40:6 · H9001 · וַ · va · ו · & · and` alakúak. A Strong-forma mindkét fájlban `Hnnnn` (négy számjegy; 332/332 és 950/950 sor azonos mintán), üres mező egyik oldalon sincs a 4–9. oszlopokban, CRLF egyik fájlban sincs, a fő kivonat újsorral végződik, és mind a 468 969 sora (fejléccel) 7 oszlopos. Az átvitel tehát tisztán oszlop-kiválasztás és kulcsátírás, adat-átalakítás nincs.

## 4. Más Jób-sor a nyitott esetek között

A 332 sor mind Jób 41 (elsődleges kulcs); a 40. fejezet csak másodlagos (MT) kulcsként szerepel (83 sor: MT 40:25–32 = Károli 41:1–8). Önálló Jób 40-es sor nincs, más könyv sora sincs. Nem nyúlok hozzá.

## 5. Beszúrási pont a fő kivonatban

A `TAHOT_kivonat.tsv` Jób 40 sorai folytonosak: fájlsor **288 901–289 098** (kulcsok 40:6–40:24, 198 sor; a Jób 40:1–5 TAHOT-kulcsa 39:34–38, az F83 szerint). Az utolsó Jób 40 sor `Jób 40:24 · H0639 · אָֽף …` (289 098.), a következő `Jób 42:1 · H9001 · וַ` (289 099.). **Beszúrás: a 289 098. és a 289 099. fájlsor közé** (az új sorok a mai 289 099. helyére). A fő kivonat Jób 41-es sorainak száma ma 0. Beszúrás után 468 968 + 332 = 469 300 adatsor. A Jób 40 kulcsai (MT-számozás) nem változnak. A `lekerdez.py scan H3882` ellenpróbájához: a H3882 (leviátán) a nyitott fájlban egyetlen sor (`Job.41.1`, לִוְיָתָ֣ן), a fő kivonat Jób 40-ében 0, tehát a pótlás előtt a Jób 41-re nincs találat, utána 1 kell legyen.

## Megjegyzések az F84.2-höz

- A `tahot_karoli_kulcs_generalas.py:227` a nyitott fájl előállítója (a `f4_0c_korut_ellenoriz.py` eredet-térképe is erre mutat); a fájl neve nem változik, csak a sorai.
- Az `adat/licencek.tsv` 49. sora és a TAGNT-README 241–244. sora a nyitott eseteket említi; a README-t az F84.3 javítja.

---

## ⛔ 1 — döntésre vár

**(a) A nyitott sorok sorsa.** Opciók:

1. **Törlés** a `TAHOT_kivonat_nyitott_esetek.tsv`-ből (a fájl csak a fejlécet tartja, a 332 sor átkerül a fő kivonatba).
2. **`ATVEVE_F84` státusz**: a 332 sor marad, `Státusz` = `ATVEVE_F84`, az `Indoklás` az F84-re hivatkozik.

*A végrehajtó javaslata: 1 (törlés).* Indok: a sorok a fő kivonatba azonos adattartalommal kerülnek át (csak a kulcs-oszlop alakja változik); a megmaradó második példány kétszeres számláláshoz vezethetne minden eszköznél, amely a kivonatot és a nyitott fájlt együtt olvassa (a `grep` szerint ma csak a generátor és a `f4_0c_korut_ellenoriz.py` eredet-térképe hivatkozza a fájlt, olvasó nincs), és a státusz-oszlop hamis „nyitott” benyomást keltene. A visszakereshetőséget a git-történet, az F83-jelentés és ez a jelentés adja. A 2. akkor jobb, ha a felhasználó az átvétel nyomát a nyitott-esetek fájlban akarja látni; ára a duplikált 332 sor.

**(b) A Jób 41:25 kezelése.** Opciók: 1. a vers a többi 33-mal együtt bekerül, jelölés nélkül · 2. kimarad · 3. bekerül, de külön `javaslat` jelöléssel.

*A végrehajtó javaslata: 1.* Indok: a mérés szerint a Strong-halmaz egyezik az MT 41:17-tel (Jaccard 0,83, az egyetlen különbség a H4480 elöljáró), a Károli-szöveg tartalmilag egyezik a 8 TAHOT-sorral, és az „összeolvadt vers” anomália a `Karoli_adatminosegi_anomaliak.tsv` szerint már javítva van (10 versre bontva), a `Karoli_1908.tsv` a javított állapotot tartalmazza. A kihagyás (2.) lyukat hagyna a 34 versnyi fejezetben és gyengítené a #22 Jób-futását; a `javaslat` jelölés (3.) olyan eltérést jelezne, amelyet a mérés nem talált.

Döntéstétel: `DONTESEK.md` DT-F84a.


---

## ⛔ 1 — a felhasználó döntése (2026-10-09) és F84.2 végrehajtása

DT-F84a: **(a) 1** — a 332 sor törlődik a nyitott fájlból (a fejléc marad); **(b) 1** — a Jób 41:25 jelölés nélkül bekerül. A 2. szakasz megjegyzése: a K 41:19–21 és 41:25 egyetlen H4480-különbsége a TAHOT előtag-kezelése (a מִן H9xxx-előtagként áll), nem megfeleltetési hiba.

### F84.2 — pótlás

`scope=Jób 41:1-34 átvétele a nyitott esetekből a fő kivonatba; előtte/utána sorszám, bájtazonosság, lefedettség, H3882-scan | forras=eszkozok/tahot_job41_potlas.py --ir, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAHOT_kivonat_nyitott_esetek.tsv | ts=2026-10-09T06:18:00Z`

- **Beszúrt sorok: 332** a `TAHOT_kivonat.tsv`-be, a 289 098. fájlsor (`Jób 40:24`) után, a `Jób 42:1` elé; a fő kivonat 468 968 → 469 300 adatsor. **Törölt sorok: 332** a nyitott fájlból (csak a fejléc marad).
- Írás előtti őrök (a szkript leáll, ha bármelyik sérül): a fő kivonat meglévő sorai bájtazonosak (`git diff --numstat`: fő kivonat +332 / −0, nyitott fájl +0 / −332); a sorvég mindkét fájlban LF (a szkript CR-t elutasít, megőrzi); a nyitott fájl 332 sora mind `Job.41.n` (n = 1–34, növekvő, teljes) és `ADATMINOSEGI_GYANU`; a fő kivonatban előtte 0 Jób 41-sor volt.
- `python eszkozok/tahot_lefedettseg_ellenoriz.py`: „Fejezet-szinten nincs hiány”, hiányzó fejezet 0 (ts=2026-10-09T06:18:00Z).
- `python eszkozok/lekerdez.py scan H3882 --szakasz "Jób 41:1-41:34"`: **1 igehely, 1 szó-előfordulás (Jób 41:1)**; `proveniencia: scope=range:Jób 41:1-41:34 | forras=TAHOT_kivonat.tsv | strong=H3882 | n=1 | ts=2026-10-09T06:18Z`.

### F84.3 — generátor és dokumentáció

- `eszkozok/tahot_karoli_kulcs_generalas.py`: a `("Job", (40, 41))` bejegyzés fölé megjegyzés került (mért Károli-szám 40 = 19, 41 = 34; az angol 41. fejezet hossza egyezik; a 41:25 „összeolvadt” állítás elavult, a vers javított; hivatkozás az F84-re). A döntés-érték és az indoklás-szöveg **változatlan** (a generátor a repóból nem futtatható). **[javaslat]** újrafuttatás esetén: `ELSODLEGES` a 41-re.
- `CLAUDE.md`: a TAHOT-mondat a mért állapotra javítva (nincs fejezet-hiány; a Jób 40:1–5 nem hiányzik; a Jób 41 az F84 után megvan; maradó korlát: a Jób 40 MT-kulcsú számozása).
- `konkordancia/TAHOT_TAGNT_README.md`: az eset-táblázat Jób 40/41 sora, a nyitott esetek mondata és a „Jób 40:1-5 és Jób 41 hiányzik” bekezdés a mért állapotra javítva.
- `NYITOTT_FELADATOK.md`: N-F83a felvéve és lezárva, N-F34b lezárva (helyőrzők; a végleges számot az Action osztja), mindkettő a „Lezárva” szakaszban.
- **N-F41g / #41 megjegyzés:** a BSB `Számozás` oszlopa a Jób 41-et `kjv`-nek jelöli, mert a TAHOT-ban nem volt; az F84 ezt nem írta át, a következmény (a jelölés viszonya a mostani Jób 41 TAHOT-sorokhoz) az N-F41g-hez tartozik (megjegyzésként a `NYITOTT_FELADATOK.md` lezárási blokkjában).

### Következmény a #22-re

A `f22/versmegfeleltetes.tsv` (gépi lista, a `versbeosztas.py` kimenete) a Jób 41-re a pótlás előtti állapotot rögzíti: 26 Jób 41-es vers ma `nincs_eredeti` (F83 jelentés, 3. szakasz). A fájl a #22 tulajdona, az F84 `ir`-jében nincs, ezért nem módosítottam. A `versbeosztas.py`-t a Jób-menet (#22) előtt újra kell generálni, hogy a Jób 41 az új TAHOT-sorokra párosuljon.
