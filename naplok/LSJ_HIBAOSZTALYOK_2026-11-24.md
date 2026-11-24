# LSJ: a két új hibaosztály mérése — hol látszik (2026-11-24)

**A kérdés:** a Perseus-összevetés (#858) két hibát talált az LSJ-adatban: (1) 894+ „szócikk” nem LSJ, hanem a modul készítőjének pótszövege; (2) néhány Strong-szám rossz szócikkhez kötődik. Hol látszik ez a három lapon (ISTENTISZT-001, TEREMT-001, HAMART-001) és az olvasóban?

**Válasz röviden.** Az olvasóban sok helyen: a görög szókártyák 942-én (az `LSJ` blokk 17,1%-án) nem LSJ-szöveg áll, további 52-n másik szó szócikke; az ÚSZ szóelőfordulásainak 5,9%-ánál (8 463 / 142 355) olyan szóra kattint az olvasó, amelynek „LSJ”-kártyája hibás. A három lapon a pótszöveg **szövege** csak az ISTENTISZT-001-en látszik (egy sor), de mindhárom lap **LSJ-ről szóló mondata hamis**, és ugyanaz a mechanizmus okozza: a lap abból következtet, hogy „az LSJ-nek nincs adata”, hogy a modul-sor pótszöveg, vagy hogy a lexikon-hivatkozástáblában nincs LSJ-sor — pedig a Perseus LSJ-jében van szócikk. Az ISTENTISZT-001 mondata („az ἐπικαλέω LSJ-szócikke csak átirányít, önálló tartalom nincs rá”) a téma szempontjából is hibás: a Perseus-szócikk a „megidéz egy istent áldozathoz vagy eskü tanújául, segítségül hív” (invoke) jelentéssel kezdődik.

```
proveniencia: scope=konkordancia/LSJ_teljes.tsv (5 522 szócikksor) × a #858 köztes eredménye (Perseus lexica @ 1c34cdf-párosítás) × konkordancia/TBESG.txt és Thayer_teljes.tsv (második Strong-tanú) × pardes.db (epites_ts 2026-11-22T17:57:40Z; lsj, token_strong) × adat/elofordulasok.tsv és a három lap | forras=PerseusDL/lexica 1c34cdf756c63cf37db61bd366d733431dbd7aa0; gépi besorolás, kézi átnézés a lapokra és a mintákra | ts=2026-11-24
```

A Strong-szintű lista: [LSJ_HIBAOSZTALYOK_2026-11-24_strongok.tsv](LSJ_HIBAOSZTALYOK_2026-11-24_strongok.tsv) (1 024 sor: osztály, TBESG-lemma, a modul-szöveg kezdete, ÚSZ-előfordulás, három-lap-jelölés, a Perseus-szócikk a Strong lemmájára). Gépi besorolás; kézzel nem szerkesztendő, a javítás-tábla (lent) a forrása a későbbi javításnak.

## 1. Az 1. osztály: nem LSJ-szöveg a „LSJ”-kártyán (942 Strong)

| alosztály | db | ÚSZ-előfordulás | mi áll a kártyán |
|---|---|---|---|
| A1 név-helyőrző | 468 | 2 964 | „This entry is a name, title, city… and is not Defined by LSJ (Note: there are some exceptions…)” |
| A2 Strong-utalás | 297 | 2 122 | „Probably emphatic of G5100” típusú Strong-mondat |
| A3 „no Definition found” | 43 | 2 258 | pl. G3165 μέ (2 035 előfordulás) |
| A4 rövid nyelvtani mondat | 32 | 28 | „Accusative plural of G1473” |
| A5 Strong-mondat + LSJ-szöveg | 102 | 475 | a Strong-mondat az LSJ-szöveg előtt áll |
| **összesen** | **942** | **7 847 (5,5%)** | |

(A #858 „894 + 41”-je ugyanez a halmaz; a különbség a besorolás szélein van: az A5-be kerültek a kevert és a Strong-mondattal kezdődő sorok.)

Két észrevétel a halmazról: (a) az A1 „név” besorolása nem mind név — a TBESG szófaja szerint kb. 35 sor ige, melléknév vagy határozó (pl. G1097 γινώσκω, 223 előfordulás; G1089 γεύω); (b) a Strong-lemmára **van** Perseus-szócikk az A2 297 sorából legalább 134-nél, az A5 102-ből 72-nél (alsó becslés: az ékezet- és helyesírás-változatokat — γινώσκω / γιγνώσκω — nem vettem), vagyis ezeknél nem a szócikk hiányzik, hanem a modul nem kötötte be.

### Fogyasztók

| fogyasztó | hogyan viszi tovább | mennyi érintett |
|---|---|---|
| `konkordancia/LSJ_teljes.tsv` | a forrás (a modulból) | 942 sor |
| `pardes.db` `lsj` tábla (`eszkozok/sqlite_epit.py:148`) → olvasó `szo.lsj` blokk (`eszkozok/olvaso_szerver/blokkok.py:2621–2628, 2763`; `lekerdezesek.py:1175`) | szűrés nélkül: minden görög szókártyán „LSJ” címmel, összecsukva, „CC BY-SA 4.0” licenc-sorral; a hozzáférési alapszint `nyilvanos` | mind a 942 sor a dbben; 849 olyan szóé, amely az ÚSZ-ben előfordul |
| lapgen B26 (`eszkozok/lapgen/bemenet/nyelvi_hatter.py:22, 55–69`) | a Strong-mondat regexe („… from G…”) „utaló csonk”-nak minősít, és az alapigére utal | 36 szó; 34-nél van saját Perseus-szócikk (l. a 4. pontot) |
| `adat/forditasok.tsv`, `adat/lexikon_hivatkozasok.tsv` | LSJ-sor: G2564 (részlet), G0086 | **nem érintett** (valódi LSJ-szócikkek, nincsenek a listán) |
| `eszkozok/cremer_ocr_javit.py`, `olvaso_pilot/*` | keresés a szövegben; pilot | nem lapon látható; a pilot nem az éles olvasó |
| `konkordancia/lexikonok_nyers/LXX.lexicon` | — | a kódban nincs fogyasztója |

**Az olvasóban** a pótszöveg az LSJ-kártyán áll, szűrés vagy jelzés nélkül (a dbben pl. G1941: „ἐπικαλεìομαι Middle voice from G1909 and G2564”; G0002: a név-helyőrző). A kártya címe és licenc-sora LSJ-t mond. Az olvasó-szervert nem indítottam; a leírás a kód és a `pardes.db` sorai alapján készült (a `meta.epites_ts` 2026-11-22; az LSJ-tábla azóta nem változott).

## 2. A 2. osztály: téves Strong → szócikk kötés

**A mérés módja.** A párosítás a #858-ban a modul-szöveg fejéből indult, ezért a Strong → szócikk hozzárendelést nem tudta ellenőrizni. A független tanú itt két másik Strong-forrás lemmája: a TBESG lemma-oszlopa és a Thayer-szócikk fejszava. Egy sor megfelelő, ha a tanúk egyike megegyezik (ékezet nélkül, kisbetűvel, a homográf-szám nélkül) a Perseus-szócikk lemmájával, a modul-szöveg fejével, vagy szerepel a szöveg első 600 karakterében. A hozzáfűzött szócikkeket (G1390 δῶμα, G1650 ἐν) külön futammal kerestem: a modul-szövegnek a Perseus-párban nem szereplő leghosszabb futamát vetettem össze a Perseus összes szócikkével.

Eredmény (4 578 párosított, nem-pótszöveg sorból):

| osztály | db | ÚSZ-előfordulás | példa |
|---|---|---|---|
| B1 másik szó szócikke áll a helyén | 28 | 316 | G3041 λίμνη (tó): a kártyán a λῐμήν (kikötő) szócikke; G3668 ὁμοίως: a ὁμοίωσις szócikke; G3176 μέγιστος: a μεγιστό-σωμος; G4057 περισσῶς: περίσσωσις |
| B2 Strong-mondat + az etimon szócikke | 19 | 289 | G998 βοηθός: „From G995 and θεω (to run)” + a θέω szócikke |
| B3 hozzáfűzött másik szócikk | 5 | 11 | G1390 δόμα + δῶμα; G1650 ἔλεγχος + ἐν (750 szó!); G838 αὔξησις + γάρ; G722; G2016 |
| **szigorúan téves** | **52** | **616 (0,43%)** | |
| V vizsgálandó | 30 | 1 812 | határesetek (a lemma-változatok többnyire rendben: G976 βίβλος/βύβλος; gyanús: G4511 ῥύσις → ῥύτις, G3305 μέντοι → μέντοινε); a nagy szám a G3778 οὗτος (1 425 előfordulás: a szócikk végére másik szócikk van hozzáfűzve, de azonosítani nem tudtam) és a G2041 ἔργον (177) tételéből jön |

A számok **alsó becslések**: csak azt fogja meg, ahol a modul-szöveg feje eltér a Strong lemmájától (vagy hosszú idegen futam van benne). Ahol a modul a *helyes lemma*, de a Strong-szám alatt rossz *homográfot* vagy rossz jelentés-ágat adja, azt nem látom. A 4 578 párosított, nem-pótszöveg sorból 4 501-ben a tanú és a Perseus-lemma egyezik.

Fogyasztók: ugyanazok, mint az 1. osztálynál (a `lsj` tábla → olvasó); a lapgen B26 csak a csonk-felismerést használja. Az `LSJ_teljes.tsv` mind az 52 + 30 sora az olvasóban jelenik meg a saját Strong-lapján.

## 3. A három lapon látható helyek

| lap | hol | mi látszik | osztály |
|---|---|---|---|
| ISTENTISZT-001 | `lexikon/ISTENTISZT-001_TUDOMANYOS.md` 672. sor (4.8 Nyelvi háttér) | a G1941 pótszövege idézve „a `konkordancia/LSJ_teljes.tsv` sora”-ként, torzult betűkkel: „ε (e)̓πικαλε (pikale)ìομαι (omai) Middle voice from G1909 and G2564”; a fájlnév is látszik | **1. (A2)** |
| ISTENTISZT-001 | ugyanott 1140. sor (a G2564-kártya végén) | „Az ἐπικαλέω LSJ-szócikke maga csak átirányít a καλέω alapigéhez… önálló LSJ-tartalom nincs rá.” — **hamis**: a Perseus LSJ-ben `e)pikale/w` 2 281 karakteres, önálló szócikk (n39550 az eng5 fájlban) | **1.** (következmény) |
| ISTENTISZT-001 | 1061–1067. sor (G2564 LSJ-részlet) | valódi LSJ (G2564 a „azonos tartalom, csak formázás” osztályban); a magyar részlet rendben | nem érintett |
| HAMART-001 | `lexikon/HAMART-001_TUDOMANYOS.md` 1289. sor | „A klasszikus görög nagyszótár (LSJ) a motívum szavaihoz és rokon szavaikhoz nem ad adatot.” — **hamis**: mind az 5 saját szónak (G1311, G1944, G2671, G5351, G5356) valódi, jó LSJ-szócikke van az `LSJ_teljes.tsv`-ben | nem a két osztály; ugyanaz a gyökér (l. 5. pont) |
| TEREMT-001 | `lexikon/TEREMT-001_TUDOMANYOS.md`, `_TORZSCIKK.md` | a jelenlegi lapon LSJ-szöveg vagy -mondat nincs (a törzscikk csak a szerepmátrixot idézi: „LSJ, ha releváns”); G0012 ἄβυσσος szócikke helyes | nem érintett ma |

A három lap többi G-száma (említett nevek, utalt szavak) nem jelenít meg LSJ-szöveget: a pótszöveg- vagy téves-halmazba eső említések (ISTENTISZT-001 14, HAMART-001 10, TEREMT-001 6 Strong-szám) csak számok, nem LSJ-idézetek.

**Az új generátor (218c) mit írna.** A `szocikkek.py:422–446` szerint a 4.8 görög pont csak a `lexikon_hivatkozasok.tsv` LSJ-sorából (egy sor: G2564) dönt, és a csonkot a Strong-mondat regexe ismeri fel; a tesztek (`teszt_szocikkek.py:268–308`) a „nem ad adatot” és az „LSJ-szócikke csak az alapigére utal” mondatot **elvárásként rögzítik**. A TEREMT-001-re (G0012-nek nincs LSJ-sora a hivatkozástáblában) a kód ugyanezt a „nem ad adatot” mondatot írná; futtatást nem végeztem, ez kódolvasás.

## 4. Közös gyök: a lap a pótszövegből és a hivatkozástábla hiányából következtet

- A **csonk-regex** (`… from G…`) 36 Strong-sort fog meg; 34-nél a Strong-lemmával azonos Perseus-szócikk létezik (kivétel: G1901 ἐπεκτείνομαι és G4132 πλήμμυρα). A lap szerint ezeknél „nincs önálló LSJ-tartalom” — hamis; a valódi, rövid szócikk a ἐπικαλέω-nál is megvan.
- A **„nem ad adatot”** mondat azt jelenti, hogy a `lexikon_hivatkozasok.tsv`-ben nincs LSJ-sor, nem azt, hogy az LSJ-nek nincs szócikke. A tábla egyetlen LSJ-sort tartalmaz.
- Az A1 „név”-besorolás ugyanilyen téves következtetést enged (kb. 35 sor nem név).

## 5. Nem a kérdés, de látható: a harmadik hiba (157 csonkolt szócikk)

A #858 a 157 csonkolt (T5a/T5b) szócikket is megtalálta; nem mértem, hol látszik. Az olvasóban a hosszú szócikkek (pl. G5259 ὑπό: 12 240 / 21 149 karakter) csonkán jelennek meg. Külön tétel, nem a két osztály része.

## 6. Javaslat (⛔ az integrátornak a javítás előtt)

**A kiadási minimum a látható hibákra:** a három lap hamis mondatai és az olvasó LSJ-kártyáján látható pótszöveg. Három kis PR, ebben a sorrendben:

1. **PR-C: a három lap mondatai** (nehéz kör: generátor és próza). A `NINCS` ág mondata a mai tábla hiányából következtet: igazzá kell tenni (pl. „az LSJ-szócikkek ehhez a laphoz nincsenek feldolgozva”), vagy a hivatkozástáblába kell felvenni a saját szavak LSJ-sorait — az utóbbi ma BemenetHibát ad (az LSJ-kártya nincs portolva, N-F218j), ezért a minimum a mondat. A csonk-ág („csak az alapigére utal”) a regex helyett a javítás-táblából (lent) döntsön; az ISTENTISZT-001 1140. sorának mondata szerepel az archivált tematikus tanulmányban (`archivum/ISTENTISZT-001/Segitsegul_hivni_az_Urat_tematikus.md`) és a pilot-jegyzetben is; a lap generálási forrását a PR-C-nek kell azonosítania, és ott javítani. A tesztek (`teszt_szocikkek.py:297–307`) a hamis mondatot rögzítik: a tesztet a mondattal együtt módosítani kell.
2. **PR-A: `adat/lsj_forras_javitas.tsv`** (adatforrás-javítás, mint a `bdb_forras_javitas.tsv` és a `thayer_forras_javitas.tsv`; a nyers `LSJ_teljes.tsv` érintetlen marad, kimeneti csere nincs). Oszlopok: `strong`, `tipus` (`nincs_szocikk` / `perseus_csere`), `perseus_kulcs` (és azonosító), `szoveg` (csak csere esetén), `indoklas`, proveniencia-sor (`scope=… | forras=PerseusDL/lexica@1c34cdf… | ts=`). Az `sqlite_epit.py` az `lsj` tábla építésekor alkalmazza (adatbázis-építés: nehéz kör). Az olvasó a `nincs_szocikk` sorra az üres-eredmény jelzést adja („az LSJ-ben nincs ilyen szócikk”). Gépi kiindulás: az A1–A4 (840) sor `nincs_szocikk`, kivéve ahol van Perseus-szócikk (az A2-ből ≥134, az A3-ból ≥7, az A1-ből ≥42: ezek `perseus_csere`-jelöltek, kézi átnézéssel).
3. **PR-B: a 2. osztály sorai ugyanabba a táblába** (52 szigorú + 30 vizsgálandó), **soronkénti kézi döntéssel és indoklással** (nincs közvetlen út: keresési találat nem lesz tábla-sor döntés nélkül). 25 szigorú sornál van Perseus-szócikk a Strong lemmájára; a többi (határozók: ὁμοίως, κακῶς, δικαίως…) a melléknév szócikkében van — ezeknél a javítás-tábla `perseus_csere` a *szülőszócikkre*, ez tartalmi döntés. Külön PR, mert más a döntés természete.

**A kiadás utáni listára:** a Perseus-csere az A5/A2/A1-jelöltek maradékára; a 157 csonkolt szócikk; a második osztály még nem látott alakjai (homográf-kötés); az LSJ-kártya portolása (N-F218j); a TBESG fejléce szerint a STEPBible adja a Strong-kulcsos teljes LSJ-t is (TFLSJ, CC BY) — a repóban nincs, a letöltés külső forrás, nem mértem; csak az átállás-döntéshez érdemes mérni.

## 7. Korlátok

- A mérés a Perseus-párosítás (#858) heurisztikájára épül; a második osztály alsó becslés (l. 2. pont), a besorolás gépi és csak a lapokra, a mintákra és a határesetekre néztem át kézzel.
- Az olvasót nem indítottam; a megjelenést a kód és a `pardes.db` sorai mutatják. A `pardes.db` az `epites_ts` szerint 2026-11-22-i; az LSJ-adat azóta nem változott.
- A „név-helyőrző” nem-név volta a TBESG szófaji kódjára épül (kb. 35 sor).
- A három lapnál a „látható” a main-en lévő lap szövege; az új generátor kimenetét nem futtattam (lapgen-futás nem kellett).
- Az ékezet- és helyesírás-változatok (γινώσκω / γιγνώσκω) miatt a „van Perseus-szócikk” számok alsó becslések.
