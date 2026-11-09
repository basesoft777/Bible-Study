# F177 jelentés — a Károli-kereszthivatkozások javítása a MEK 00161 kiadással (KAROLI_KH_MEK)

*Végrehajtó: `claude-sonnet-5-5` (modell-ellenőrzés: a kért `sonnet`, egyezik). Ág: `claude/karoli-kh-mek`. 2026-11-09.*
*scope=konkordancia/Karoli_kereszthivatkozasok.tsv + konkordancia/Karoli_KH_MEK.tsv + konkordancia/Karoli_1908.tsv + konkordancia/TSK_kereszthivatkozasok.tsv | forras=eszkozok/karoli_kh_mek.py | ts=2026-11-09*

## 1. Egyeztetett eltérés a briefhez képest

* **A nyers RTF forrása:** nem a felhasználó gépéről (`E:\Letöltések\00161.rtf`), hanem közvetlenül a MEK-ről töltöttem le (a felhasználó jóváhagyta,
  2026-11-09): `https://mek.oszk.hu/00100/00161/00161.rtf`, letöltve 2026-11-09, 8 675 721 bájt, a repón kívülre (a menet scratch-könyvtárába), **nem része a repónak**.
  **SHA-256: `92130f2ae669402c38d2a0e13027fef86acd2fbd66d9a78b9b6d7a9800a7473a`.** A felhasználó a saját `E:\Letöltések\00161.rtf` fájljával
  összevetheti (`certutil -hashfile 00161.rtf SHA256`); egyezés esetén a kivonat onnan is ugyanígy áll elő.
* **Új fájlok az `ir` listán kívül (a briefben megkövetelt tartalomhoz):** `konkordancia/Karoli_KH_MEK_konyvaliasok.tsv` (a „könyv-aliasok a táblában rögzítve”),
  `konkordancia/Karoli_KH_MEK_versszerkezet.tsv` (a MEK vers-szerkezete a versellenőrzéshez); a döntési és nyitott fájlok: `dontesek/uj/karoli-kh-mek.md`,
  `nyitott/uj/karoli-kh-mek.md`; további fogyasztói átállítás: `eszkozok/lekerdez.py`, `sqlite_epit.py`, `olvaso_pilot/adat.py`, `olvaso_mockup/nav_kinyer.py`
  (a `karoli_kh_szuro.py` ezen át működik; a brief a szűrő átállítását írja elő, a fogyasztói a szűrő hívói).
* **A versellenőrzés alapja (DT-F177c):** a `Karoli_1908.tsv` ∪ a MEK vers-szerkezete (a brief a `Karoli_1908.tsv`-t írja; az 14 + 2 vers eltérése miatt, l. 3.).

## 2. Mérések (a próbaméréshez képest)

A MEK-kivonat: **31 170 vers, 1 189 fejezet, 29 987 KH-sor** (13 171 vers hordoz KH-t); a HunKar-tábla: 32 407 sor, 19 817 forrásvers.
Versenként (a `Karoli_kereszthivatkozasok_gyanus.tsv` gyanús halmazával):

| | próbamérés (orkesztrátor) | mért (F177) |
|---|---|---|
| a két forrás egyezik | 11 342 (+260 a gyanúsak közül) | **11 396 (+261 gyanús)** |
| gyanús, és a MEK-ben nincs KH | 4 769 / 5 078 | **4 773 / 5 078** |
| nem gyanús, és a MEK-ben nincs KH | 1 924 | **1 905** |
| eltér | 1 446 (+49) | **1 438 (+44)** |
| csak a MEK-ben | 74 | **32** |

A különbségek okát nem vizsgáltam (a próbamérés szkriptje nem áll rendelkezésemre); a mérés a `eszkozok/karoli_kh_mek.py` két futásából újraállítható. Egy ismert eltérő
kezelés: a három „1. 2.” elírású fejezetnél (Jób 24, Zsolt 102, Zak 11) a versszám nálam a sorrendből jön (DT-F177c), a `kapcsolodo` nélküli (nem értelmezhető) MEK-sor
pedig a „csak MEK” halmazban `jelolt` sorként szerepel.
Az **egyezés a nem gyanús verseken** (ahol van KH valamelyik forrásban): 11 396 / 14 771 = **77,1%**, a két oldalon is KH-t hordozóknál 11 396 / 12 834 = 88,8% — a ⛔ ③
küszöb (60%) fölött, megállás nem kellett.

**Sor-szinten** (`konkordancia/Karoli_KH_javitott.tsv`, 35 204 sor; a 32 407 HunKar-sor mindegyike pontosan egyszer):

| szint | sor | ebből |
|---|---|---|
| `megerositett` | **21 314** | gyanús versen 317, nem gyanús versen 20 997 |
| `kiesik` | **11 027** | gyanús versen 7 654, nem gyanús versen 3 373 |
| `jelolt` | **2 863** | 2 797 `csak_mek` (2 018 TSK-támogatással, 779 nélkül), 44 `eltero_lista` (22 TSK-val), 22 `egyezik`, de nem létező hivatkozott verssel |

**Hibás hivatkozás** (`hibas_hivatkozas`): 161 sor, 142 különböző nem létező vers; 117 csak-MEK sor (köztük a 3 nem értelmezhető MEK-sor), 22 egyező sor, 22 `kiesik` HunKar-sor.

## 3. Versellenőrzés alapja

A MEK-nek 14 verse nincs a `Karoli_1908.tsv`-ben (1Kor 3:23, Préd 2:27, Hós 1:12, Hós 11:12, Ézs 3:28, Ézs 9:21, Ján 1:52, Jób 16:23, Jób 36:34, Luk 23:57,
4Móz 29:40, Péld 11:32, Róm 3:31, Róm 8:39), és a `Karoli_1908.tsv`-nek 2 verse nincs a MEK-ben (Ézs 4:6, Zak 9:17); az eltérés a `Karoli_1908.tsv` KJV-számozású
összevonásából jön (pl. Ján 1:51–52 egy vers). A `Karoli_1908.tsv` Jeremiás siralmait `Sir`-ként adja (alias a táblában). A létezés a két forrás uniója (DT-F177c).

## 4. A MEK-elírások (a nem létező hivatkozott vers; a javítás nem történt meg)

117 csak-MEK sor, köztük a brief példái: 2Móz 6:20 → „2 Móz. 26,59.” (helyesen valószínűleg 4Móz 26,59), 5Móz 7:15 → „1 Móz. 15,26.”; az 5Móz 21:23 → „Gal. 2,13.”
létező vers (Gal 2:13), ezért nem `hibas_hivatkozas`, hanem `csak_mek` jelölt (`tsk=nem`) — a MEK-elírás itt egy létező vers, a helyes Gal 3:13 nincs a HunKar-táblában azon a versen.
További példák: Ámós 7:8 → „Ámós. 8,28.”, Zsolt 37:37 → „Zsolt. 20,44.”, Zsolt 27:4 → „Zsolt. 23,42.”, 1Sám 31:11 → „2 Sám. 2,45.”. Nem értelmezhető (hiányzó versszám):
2Sám 7:8 (`1 Sám. 12,.`), 2Kir 21:5 (`2 Kir. 12,.`), 1Krón 6:14 (`2 Kir. 21,.`). A teljes lista: `grep hibas_hivatkozas konkordancia/Karoli_KH_javitott.tsv`.
Kétforrású hibás hivatkozások (mindkét forrás ugyanazt hordozza): pl. 1Krón 28:8 → 4Móz 28:1–68, Józs 8:34 → 5Móz 27:15–28 (a hivatkozott tartomány vége nem létező vers).

## 5. A MEK-kivonat naplója

```
MEK-kivonat: 31170 vers, 1189 fejezet, 29987 KH-sor; SHA-256 92130f2ae669402c38d2a0e13027fef86acd2fbd66d9a78b9b6d7a9800a7473a
fejezet_nelkul_uj: 0 
fejezet_eltero: 0 
vers_ugras: 68 [('Job', 24, 2, 3), ('Job', 24, 3, 4), ('Job', 24, 4, 5), ('Job', 24, 5, 6), ('Job', 24, 6, 7), ('Job', 24, 7, 8), ('Job', 24, 8, 9), ('Job', 24, 9, 10), ('Job', 24, 10, 11), ('Job', 24, 11, 12), ('Job', 24, 12, 13), ('Job', 24, 13, 14), ('Job', 24, 14, 15), ('Job', 24, 15, 16), ('Job', 24, 16, 17)]
ismeretlen_bekezdes: 0 
kh_vers_elott: 0 
ismeretlen_konyv: 0 
ertelmezhetetlen_kh: 3 [('2Sa.7.8', '1 Sám. 12,.'), ('2Ki.21.5', '2 Kir. 12,.'), ('1Ch.6.14', '2 Kir. 21,.')]

```
A könyvcímek (a MEK tartalomjegyzéke, a kánoni sorrendben a normalizáló tábla STEP-kódjaival párosítva):
Gen=Mózes első könyve a teremtésről
  * Exo=Mózes második könyve a zsidóknak Égyiptomból kijöveteléről
  * Lev=Mózes harmadik könyve a léviták egyházi szolgálatáról
  * Num=Mózes negyedik könyve az izráeliták megszámlálásáról való könyv
  * Deu=Mózes ötödik könyve a törvény summája
  * Jos=Józsué könyve
  * Jdg=Bírák könyve
  * Rut=Ruth könyve
  * 1Sa=Sámuel első könyve
  * 2Sa=Sámuel második könyve
  * 1Ki=A királyokról írt I. könyv
  * 2Ki=A királyokról írt II. könyv
  * 1Ch=Krónika I. könyve
  * 2Ch=Krónika II. könyve
  * Ezr=Ezsdrás könyve
  * Neh=Nehémiás könyve
  * Est=Eszter könyve
  * Job=Jób könyve
  * Psa=Zsoltárok könyve
  * Pro=Bölcs Salamonnak példabeszédei
  * Ecc=A prédikátor Salamon könyve
  * Sng=Salamon Énekek éneke
  * Isa=Ésaiás próféta könyve
  * Jer=Jeremiás próféta könyve
  * Lam=Jeremiás siralmai
  * Ezk=Ezékiel próféta könyve
  * Dan=Dániel próféta könyve
  * Hos=Hóseás próféta könyve
  * Jol=Jóel próféta könyve
  * Amo=Ámós próféta könyve
  * Oba=Abdiás próféta könyve
  * Jon=Jónás próféta könyve
  * Mic=Mikeás próféta könyve
  * Nam=Náhum próféta könyve
  * Hab=Habakuk próféta könyve
  * Zep=Sofóniás próféta könyve
  * Hag=Aggeus próféta könyve
  * Zec=Zakariás próféta könyve
  * Mal=Malakiás próféta könyve
  * Mat=A Máté írása szerint való szent evangyéliom
  * Mrk=A Márk írása szerint való szent evangyéliom
  * Luk=A Lukács írása szerint való szent evangyéliom
  * Jhn=A János írása szerint való szent evangyéliom
  * Act=Az apostolok cselekedetei
  * Rom=Pál apostolnak a rómabeliekhez írt levele
  * 1Co=Pál apostolnak a korinthusbeliekhez írt első levele
  * 2Co=Pál apostolnak a korinthusbeliekhez írt második levele
  * Gal=Pál apostolnak a galátziabeliekhez írt levele
  * Eph=Pál apostolnak az efézusbeliekhez írt levele
  * Php=Pál apostolnak a filippibeliekhez írt levele
  * Col=Pál apostolnak a kolossébeliekhez írt levele
  * 1Th=Pál apostolnak a thessalonikabeliekhez írott első levele
  * 2Th=Pál apostolnak a thessalonikabeliekhez írott második levele
  * 1Ti=Pál apostolnak Timótheushoz írt első levele
  * 2Ti=Pál apostolnak Timótheushoz írt második levele
  * Tit=Pál apostolnak Titushoz írt levele
  * Phm=Pál apostolnak Filemonhoz írt levele
  * Heb=A zsidókhoz írt levél
  * Jas=Jakab apostolnak közönséges levele
  * 1Pe=Péter apostolnak közönséges első levele
  * 2Pe=Péter apostolnak közönséges második levele
  * 1Jn=János apostolnak közönséges első levele
  * 2Jn=János apostolnak közönséges második levele
  * 3Jn=János apostolnak közönséges harmadik levele
  * Jud=Júdás apostolnak közönséges levele
  * Rev=János apostolnak mennyei jelenésekről való könyve

A „vers_ugras” 68 sora a három „1. 2.” fejezet (Jób 24, Zsolt 102, Zak 11) nyomtatott számozásának egyel előrébb járása; a versszám a sorrendből jön.

## 6. A kiadás azonosítása

A fájlban nincs impresszum. A MEK katalóguscédulája (https://mek.oszk.hu/00100/00161/cedula.html, lekérve 2026-11-09): „eredeti kiadvány: Biblia [elektronikus dok.] :
Károli; katolikus, King James teljes szövegekkel. 3.0 ver. Budapest : Arcanum, 1995”; MEK-be került 1995-06-14; az oldal dátuma 2002-10-01. **Az elektronikus kiadás azonosított
(Arcanum, Biblia 3.0, 1995), a nyomtatott kiadás, amelyre a margó visszamegy, nem azonosított.** A szöveg helyesírása az 1908-as revízióé.

## 7. Licenc-állapot (⛔ ② — a munka belső tanúként folyt)

A `licencek.tsv` `Karoli_KH_MEK` sora: `kereskedelmi=feltetelesen`, `allapot=tisztazatlan`, `cimke=tisztázatlan`; a MEK copyright-szövege személyes, nem kereskedelmi másolást enged,
forrásmegjelöléssel („Országos Széchényi Könyvtár, Magyar Elektronikus Könyvtár”); a katalóguscédula ugyanakkor „Jogi közlemény: Nem jogvédett”. **A felhasználónak külön meg kell
erősítenie (DT-F177b), mielőtt a MEK-ből származó bármi a kimenetbe (lap, nyílt mag) kerül.** A munka során semmi MEK-eredetű nem került kimenetbe: a lapok újragenerálása nem történt
meg, a `megerositett` szintű sorok közkincs HunKar-sorok, a `csak_mek` sorok `jelolt` szintűek és nem jutnak a szűrőn át. A `Karoli_KH_javitott` licencsora szintén `feltetelesen` / `tisztazatlan`.

## 8. Mi változott a rendszerben

* `karoli_kh_szuro.py`: `elfogad(forras, cel)` / `szint(forras, cel)` a javított táblából; a `gyanus_forrasok()` archív (szűrésre nem használt).
* Átállított fogyasztók: `lekerdez.py`, `sqlite_epit.py`, `olvaso_pilot/adat.py`, `olvaso_mockup/nav_kinyer.py`. **Nem módosítva** (kizárt): `lexikon_general.py` (`kh_index`), a lapok;
  az `olvasoi_kapu.py` `KH_MASOLT` szabálya a `karoli_kh_epseg.gyanus_forrasok()`-t használja (N-F177a).
* A `Karoli_kereszthivatkozasok_gyanus.tsv` ARCHÍV fejlécet kapott (a generátorból újragenerálva; az adat változatlan, csak a `ts=` és a fejléc), a generátor megjegyzést.
* N-F156a és N-F156c lezárva (`NYITOTT_FELADATOK.md`, helyben); új: N-F177a, N-F177b (`nyitott/uj/karoli-kh-mek.md`); új döntések: DT-F177a, b, c (`dontesek/uj/karoli-kh-mek.md`).

## 9. Ellenőrzések kimenete

* `python eszkozok/ellenoriz.py`: `RENDBEN: 26 | SÉRTÉS: 1 | KÉZI: 2 | JELENTÉS: 14` (a kilépési kód 1 az ág indulása előtt is: a HAMART-001 `minosites` rés-forrás egyezési SÉRTÉSe, a 11. szabály; a `git stash`-sel mért alapállapot azonos kimenetű, az F177 nem érinti).
* `python eszkozok/feladatok.py ellenoriz`: `197 brief, 0 hiba, 0 figyelmeztetés`.
* `python eszkozok/teszt_karoli_kh_mek.py` (új, 25 teszt): `Ran 25 tests in 0.282s  OK`.
* Meglévő érintett tesztek: `teszt_karoli_kh_gyanus` (`Ran 3 tests in 6.027s  OK`), `teszt_lekerdez_naplo` (`Ran 8 tests in 1.501s  OK`), `teszt_lekerdez_sir` (`Ran 11 tests in 12.446s  OK`), `teszt_karoli_ellenorzes` (`Ran 10 tests in 0.010s  OK`), `teszt_feladatok` (`Ran 119 tests in 3.150s  OK`).
* `eszkozok/teszt_sqlite_epit.py`: 3 FAIL + 1 ERROR (`Integracio` setUpClass, `FeliratHalmaz`, `Negativ.baseline`, `Pozitiv.mai_adat`) — **ugyanaz az alapállapoton** (`git stash`-sel mérve: azonos 3 + 1); a `Pozitiv` / `Negativ` hibaüzenete a HAMART-001 11. szabály-sértését idézi; a másik kettő okát nem vizsgáltam, az F177 egyiket sem okozza (azonos az alapállapoton).
* Az olvasó-szerver tesztjei (`teszt_futtat.py`, WSL-venv és natív `pardes.db` kell) ebben a környezetben nem futtathatók; a `karoli_kh_szuro.elfogad` hívó oldalai (`olvaso_pilot/adat.py`, `nav_kinyer.py`) szintaktikailag és a szűrő tesztjén át ellenőrzöttek, a teljes lefutás a CI-re vár.

## 10. Megállási pontok

⛔ ① nem (a modell egyezett, a #176 a `main`-ben); ⛔ ② a licenc: a munka belső tanúként folytatódott, a megerősítés nyitva (DT-F177b); ⛔ ③ nem (77,1% a nem gyanús verseken);
⛔ ④ nem (egyetlen KH-t sem javítottam kézzel; a `jelolt` sorok eldöntetlenek, N-F177b).
