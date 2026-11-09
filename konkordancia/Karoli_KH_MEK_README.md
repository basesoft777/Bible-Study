# Karoli_KH_MEK — a MEK 00161 kiadás Károli-kereszthivatkozásai (F177, KAROLI_KH_MEK)

A `Karoli_kereszthivatkozasok.tsv` (HunKar OSIS ← szentiras.hu KG) ismert hibája, hogy sok vers egy másik vers
KH-listáját hordozza (N-F156a). A MEK 00161 kiadás (*Szent Biblia*, Károli) versenként, a vers alatt adja a KH-t,
a HunKar-tól függetlenül: **ez a második, független tanú**. A MEK Károli-kiadása a kimenet szempontjából **közkincs**
(DT-F177b, a felhasználó döntése, 2026-11-09: „(a) közkincs”; l. „Licenc”): a MEK-ből származó sor a kimenetbe
(lap, nyílt mag) kerülhet.

## 1. Forrás és ellenőrizhetőség

| | |
|---|---|
| forrás-URL | https://mek.oszk.hu/00100/00161/ (oldal); a letöltött fájl: https://mek.oszk.hu/00100/00161/00161.rtf |
| letöltve | 2026-11-09 (az F177 menet; a nyers fájl a repón kívülre, a menet scratch-könyvtárába került, **nem része a repónak**) |
| fájl | `00161.rtf`, 8 675 721 bájt |
| **SHA-256** | `92130f2ae669402c38d2a0e13027fef86acd2fbd66d9a78b9b6d7a9800a7473a` |
| RTF-fejléc | cím: *Szent Biblia*; létrehozás: 2004-04-08; a fájl eredeti neve `Biblia.lit`; 1 495 oldal, 625 880 szó |
| MEK-oldal dátuma | 2002-10-01 (a MEK oldalán a tétel dátuma) |

**Összevetés a felhasználó saját fájljával.** A felhasználó gépén lévő `E:\Letöltések\00161.rtf` ugyanennek a
kiadásnak az RTF-je lehet; az egyezés a SHA-256 összevetésével ellenőrizhető (`certutil -hashfile 00161.rtf SHA256`
Windowson). Egyezés esetén a kivonat a felhasználó fájljából is ugyanígy áll elő
(`python eszkozok/karoli_kh_mek.py kivonat <rtf>`).

**A kiadás azonosítása.** A fájlban nincs impresszum. A MEK katalóguscédulája (https://mek.oszk.hu/00100/00161/cedula.html,
lekérve 2026-11-09) szó szerint: „*Szent Biblia : Azaz Istennek Ó és Új Testamentomában foglaltatott egész Szent Irás /
fordító Károli Gáspár*”; „*eredeti kiadvány: Biblia [elektronikus dok.] : Károli; katolikus, King James teljes
szövegekkel. 3.0 ver. Budapest : Arcanum, 1995*”; „*MEK-be került: 1995-06-14*”. Azaz az **elektronikus kiadás
azonosított** (Arcanum, Biblia 3.0, 1995), a **nyomtatott kiadás, amelyre a KH-margó visszamegy, nem azonosított**. A
szöveg helyesírása az 1908-as revízióé (a `Karoli_1908.tsv`-vel egyező szövegváltozat).

## 2. Fájlok

| Fájl | Tartalom |
|---|---|
| `Karoli_KH_MEK.tsv` | a MEK KH-sorai: `igehely` (a forrásvers, STEPBible-alak, pl. `Gen.1.1`), `kapcsolodo` (a hivatkozott vers, STEPBible-alak; **üres**, ha a MEK sora nem értelmezhető, pl. `1 Sám. 12,.`), `mek_alak` (a MEK szó szerinti alakja, pl. `1 Móz. 2,4.`), `proveniencia` |
| `Karoli_KH_MEK_konyvaliasok.tsv` | a könyvrövidítések megfeleltetése: `mek` (a MEK KH-sorainak 66+1 rövidítése) és `karoli_1908` (a `Karoli_1908.tsv` eltérése: `Sir` = Jeremiás siralmai) → STEP-kód |
| `Karoli_KH_MEK_versszerkezet.tsv` | a MEK vers-szerkezete (könyv, fejezet, versszám): a versellenőrzéshez (l. 4.) |
| `Karoli_KH_javitott.tsv` | az összevetés eredménye, háromszintű (l. 5.) |
| `eszkozok/karoli_kh_mek.py` | `kivonat` (RTF → a három első fájl) és `osszevet` (→ `Karoli_KH_javitott.tsv`) |

## 3. A kivonat módszere

* **RTF-dekódolás.** A `\'xx` escape cp1250, a `\uN` Unicode; a betűtípus-, stílus-, mezőutasítás- és könyvjelző-csoportok
  kimaradnak. A bekezdés-stílus dönt: `\s1` könyvcím, `\s2` fejezetszám, `\s3` KH-sor, a stílus nélküli bekezdés a vers.
* **Könyvpárosítás a MEK saját tartalomjegyzéke szerint.** A 66 könyvcím (stílus 1, a két testamentum-címen kívül) kánoni
  sorrendben áll; az i-edik cím a `Konyv_normalizalo_tabla.tsv` i-edik sora (STEP-kód). A címek a futás naplójában.
* **Fejezet, vers.** A `N.` sor új fejezet; ha a vers 1-re ugrik fejezetsor nélkül, új fejezet. A KH-sor a **megelőző**
  vers alatt áll, és ahhoz tartozik. **A versszám a sorrendből jön**, a nyomtatott szám eltérése naplóba kerül: a MEK-ben
  három fejezet első bekezdése „1. 2.” (Jób 24, Zsolt 102, Zak 11), ahol a „2.” elírás; a nyomtatott számozás ezeken a
  fejezeteken a fejezet végéig egyel előrébb jár. A Gen 42 fejezetsora pont nélküli („42”).
* **A tartomány két végponttal.** A MEK a tartományt két külön hivatkozásként adja (a két végpont); a kivonat ezt
  megőrzi (két sor), és az összevetés is így kezeli (a HunKar-tartomány megfelel, ha mindkét végpontját listázza a MEK).
* **MEK-elírások.** A MEK néhány KH-sora nem értelmezhető (pl. `1 Sám. 12,.`, `2 Kir. 12,.`, `2 Kir. 21,.`: a versszám
  hiányzik), ezek `kapcsolodo` nélküli sorként megmaradnak; a nem létező vershez mutatók (pl. `2 Móz. 26,59.`) a
  versellenőrzésen bukik ki, **nem javítjuk találgatással**.

## 4. A versellenőrzés alapja

Egy hivatkozott (és egy forrás-) vers akkor létezik, ha benne van a `Karoli_1908.tsv`-ben **vagy** a MEK saját
vers-szerkezetében. A `Karoli_1908.tsv` egyes versekben két MEK-verset hordoz egyben (a Károli két versét egy versként adja), ezért a MEK külön versei hiányoznak belőle. Mérve (`python eszkozok/lekerdez.py karoli "<vers>"`; scope=range:<vers> | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv+Karoli_KH_javitott.tsv | ts=2026-11-09): a 4Móz 29:39, a Róm 3:30, az 1Kor 3:22 és a Ján 1:51 egy-egy Károli-versben adja a MEK két versét; a 29:40, 3:31, 3:23 és 1:52 ezért „Nincs Károli-szöveg”. A 14 hiányzó MEK-vers közül ilyen a Róm 8:39, a Hós 11:12, az Ézs 9:21 és a Préd 2:27 is (az előző Károli-vers szövege a két MEK-verset együtt hordozza; a Préd 2:26 kétvers-egység: a Károli Préd 2:26 „Mert kicsoda ehetnék…” + „Mert az embernek, a ki jó…” a KJV 2:25–26-nak felel meg, a `KJV_Strongs_teljes.tsv` Ecc.2.25 [H398 eat, H2363 hasten, H2351 more] és Ecc.2.26 sorai szerint; `python eszkozok/lekerdez.py karoli "Préd 2:26"`, scope=range:Préd 2:26 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv+Karoli_KH_javitott.tsv | n=1 | ts=2026-11-09T11:09Z; „Préd 2:27” → „Nincs Károli-szöveg”). Összevonásos eset tehát 8 van. A Jób 16:23, a Jób 36:34, a Péld 11:32 és a Hós 1:12 esetén pedig az utolsó Károli-vers a következő fejezet első versének megfelelő szöveget is tartalmazza (4 fejezetvégi eset; a megfelelés a KJV-számozás szerint áll, a forrás a repóbeli `KJV_Strongs_teljes.tsv`; a `Karoli_1908.tsv` saját következő fejezeti 1. verse mást hordoz). Az Ézs 3:28 és a Luk 23:57 esetén a fejezet utolsó Károli-verse egyetlen versnyi szöveg, ott az eltérés a fejezeten belül van (a MEK szövege nélkül nem jelölhető ki; 2 vizsgálatlan eset). Bontás: 8 + 4 + 2 = 14. Az Ézs 4:6 és a Zak 9:17 fordított irányú: a `Karoli_1908.tsv`-ben külön vers, a MEK-ben nincs.
A kettős alap miatt a MEK valódi versei nem esnek ki. A nem létező vers
`hibas_hivatkozas` jelöléssel marad a táblában. Mért: 14 MEK-vers nincs a `Karoli_1908.tsv`-ben (1Kor 3:23, Préd 2:27, Hós 1:12,
Hós 11:12, Ézs 3:28, Ézs 9:21, Ján 1:52, Jób 16:23, Jób 36:34, Luk 23:57, 4Móz 29:40, Péld 11:32, Róm 3:31, Róm 8:39), és 2
`Karoli_1908`-vers nincs a MEK-ben (Ézs 4:6, Zak 9:17); a MEK összesen 31 170 verse a `Karoli_1908.tsv` 31 158 versével szemben.

## 5. Licenc

A MEK szerzői jogi oldala (https://mek.oszk.hu/html/allando/copyright.htm, lekérve 2026-11-09): „*Digitális formában
szabadon másolható, de csak saját célokra, nem-kereskedelmi jellegű felhasználásra, változtatások nélkül és a forrásra
való megfelelő hivatkozással: "Országos Széchényi Könyvtár, Magyar Elektronikus Könyvtár".*” A dokumentum a szerzői
jogról szóló 1999. évi LXXVI. törvény IV/B. fejezete (kereskedelmi forgalomban nem elérhető művek) alapján került
fel. A tétel katalóguscédulája ugyanakkor: „*Jogi közlemény: Nem jogvédett*”. A mű kora miatt a kiadás
közkincs: **DT-F177b (a felhasználó döntése, 2026-11-09, szó szerint: „(a) közkincs”)**, a Sefaria-döntés elve szerint
(DT-F176b): közkincs tartalomnál a szerzői jog az irányadó. A `licencek.tsv` sora ezért `közkincs` / `kereskedelmi=igen` /
`allapot=kozkincs`; a MEK-ből származó sor a kimenetbe (lap, nyílt mag) kerülhet. A két fenti MEK-állítás (a copyright-szöveg
és a cédula) idézete a döntés alapja, nem nyitott kérdés. A forrásmegjelölés („Országos Széchényi Könyvtár, Magyar
Elektronikus Könyvtár”, MEK 00161) udvariasságból a forrásleírásban marad. A javított tábla a saját döntésünk; a MEK szövege (a versszöveg) nem került át, csak a
hivatkozás-tény és a szó szerinti hivatkozás-alak (`mek_alak`).

## 6. Mért eredmény (2026-11-09; részletek: `naplok/F177_jelentes.md`)

A `Karoli_KH_javitott.tsv` 35 204 sora: **megerositett 21 314**, **kiesik 11 027**, **jelolt 2 863** (ebből 2 797 csak a MEK-ben
szereplő hivatkozás, 44 eltérő lista, 22 egyező, de nem létező hivatkozott verssel). A 32 407 HunKar-sor mindegyike pontosan egyszer szerepel.
A MEK 13 171 versén áll KH (29 987 sor); a HunKar-táblában 19 817 forrásvers.

Versenként (a HunKar `Karoli_kereszthivatkozasok_gyanus.tsv`-vel): a 5 078 gyanús vers közül 4 773-nak a MEK-ben nincs KH-ja,
261 teljesen egyezik, 44 eltér; a nem gyanús versek közül 11 396 egyezik, 1 438 eltér, 1 905-nek a MEK-ben nincs KH-ja, 32 csak a
MEK-ben szerepel. **Hibás hivatkozás** (nem létező hivatkozott vers) 161 sorban van (142 különböző nem létező vers): 117 csak MEK-sor
(114 nem létező hivatkozott vers, a MEK-elírások, pl. `2 Móz. 26,59` a 2Móz 6:20-nál, `1 Móz. 15,26` az 5Móz 7:15-nél), 22 egyező sor (mindkét forrás ugyanazt a hibás
hivatkozást hordozza, pl. 1Krón 28:8 → 4Móz 28:1–68, a tartomány vége, a 28:68 nem létező vers), 22 `kiesik` HunKar-sor. A 117 csak MEK-sor között 3 nem értelmezhető MEK-sor van (`1 Sám. 12,.`, `2 Kir. 12,.`, `2 Kir. 21,.`:
a versszám hiányzik; `indok`: `hibas_hivatkozas=ertelmezhetetlen`). Mindhárom a HunKar-tartomány második végpontjának helyén áll (2Sám 7:8: `1Sám 16:11–12`; 2Kir 21:5: `2Kir 23:11–12`; 1Krón 6:14: `2Kir 25:18–21`), de a MEK-alak fejezetszáma is eltér (12 / 12 / 21 a 16 / 23 / 25 helyett); ez megfigyelés, az adatot nem javítottuk.
**TSK-jelölés a `kiesik` soron is** (ELLENOR_F177 1.): minden `kiesik` sor indoka `mek_ures_vers;tsk=igen|nem` (+ esetleg `hibas_hivatkozas`), ugyanazzal a szabállyal, mint a `jelolt` soroké. A 11 027 `kiesik` sorból `tsk=igen` 321, `tsk=nem` 10 706; a nem gyanús versekre eső 3 373 sorból `tsk=igen` 318, `tsk=nem` 3 055. A szint nem változik, a jelölés csak támasz.
**Korlát:** a MEK a tartományt két végponttal adja, ezért a `csak_mek` sorok között tartomány-végpontpárok is lehetnek; a sorok eldöntése
(N-F177b) nem része a menetnek.

## 7. A jelölt szint feldolgozása — a beemelési szabály (F181; DT-F181d, DT-F181e, DT-F181f)

**A szabály egy helyen (ez a szakasz); a megvalósítás: `eszkozok/karoli_kh_mek.py` (`jelolt_bontas`, `beemel`); tesztek: `eszkozok/teszt_karoli_kh_mek.py` (`JeloltSzabaly`, `RepoTablak`).**
Az alap a felhasználó szava (2026-11-09, szó szerint): „TSK külön rendszer, nem kell összevetni őket. Károlinak meg elfogadjuk a MEK-et, ha ott nem volt gyanús ismétlődő.” Módosításai: DT-F181e (orkesztrátori döntés, nem felhasználói: az elírás-gyanús osztály jelölt marad) és DT-F181f (a felhasználó: „beemeljük”: a HunKar-oldali gyanús-jelölés nem zár ki).

**1. A MEK-oldali `jelolt` sor (`forras=MEK`, azaz a MEK-ben áll, a HunKar-ban azon a versen nem) `megerositett` lesz**, kivéve, ha
* a hivatkozott vers vagy a forrásvers **nem létezik** (a versellenőrzés alapja a 4. szakasz: `Karoli_1908` ∪ MEK-versszerkezet) → `jelolt` marad (`hibas_hivatkozas`);
* a forrásvers **MEK-oldali gyanús ismétlődő**: a forrásvers MEK-listája (legalább 2 különböző cél) szó szerint azonos egy másik forrásvers MEK-listájával → `jelolt` marad. (A `Karoli_kereszthivatkozasok_gyanus.tsv` HunKar-oldali jelölése **nem** zár ki: az a HunKar-lista másoltságát jelzi, a MEK-lista ilyenkor a javító tanú; DT-F181f.)
* a MEK-cél **egyetlen összetevőben** (könyv, fejezet vagy versszám) tér el a forrásvers egy jelölt HunKar-sorának céljától (**elírás-gyanús osztály**, DT-F181e: a végrehajtói olvasat szerint 15 sorból 4 valószínű MEK-elírás) → `jelolt` marad.
A `megerositett` MEK-sor `forras=MEK`, indoka `csak_mek;mek_alak=…;tsk=…;szabaly=F181`.

**2. A HunKar-oldali `jelolt` sor** (`eltero_lista`: a HunKar-sor, amelyet a MEK a versen nem listáz, de más hivatkozást igen): `kiesik`, ha a forrásvers MEK-listájából legalább egy sor beemelődik (a MEK-lista a versen irányadó, és a sor abban nincs), **kivéve** ha egy elírás-gyanús MEK-sor párja (a pár eldöntetlen: a HunKar-cél lehet a helyes); különben `jelolt` marad. A `kiesik` itt nem állítja, hogy a HunKar-sor hibás: a MEK-lista elfogadásának következménye.

**3. Az `egyezik`, de nem létező hivatkozású sor (`HunKar+MEK`) `jelolt` marad.**

**4. A TSK nem tanú és nem feltétel.** A `tsk=igen|nem` jelölés az indokban tájékoztatás marad (ELLENOR_F177 1.), a szabály nem használja.

**5. A döntés nélküli maradék `jelolt` marad** (hiányt nem töltünk ki, CLAUDE.md 3. szabály; a lapra/indexbe nem jut): a nem létező célvers (139 sor, tételesen a `naplok/F181_jelentes.md` A. függelékében), a MEK-oldali gyanús ismétlődő (6), az elírás-gyanús osztály (15), és a jelöltben maradt HunKar-oldali sorok (30). Összesen **190** sor. A maradékról nincs döntés; a szúrópróba és a mért hibaarány: `naplok/F181_jelentes.md` 7. szakasz.

**6. A fogyasztók.** A `karoli_kh_szuro.mek_sorok()` a csak a MEK-ben álló, `megerositett` sorokat adja (a HunKar-tábla kulcsaival és magyar megjelenítéssel); a `lekerdez.py` (`karoli`), a `sqlite_epit.py` (`kh` tábla), az `olvaso_pilot/adat.py` és az `olvaso_mockup/nav_kinyer.py` a HunKar-sorok mellé ezeket is olvassa, ugyanazzal az `elfogad` szűrővel. A `kiesik` és a `jelolt` sor nem jut át. A lapokat és a `pardes.db`-t ez a menet nem építette újra (N-F177a).

**Előállítás.** `python eszkozok/karoli_kh_mek.py osszevet` a #177 összevetése **és** a beemelési szabály együtt (a tábla fejléce: `osszevet + beemel`); `osszevet --nyers` a #177 háromszintű nyers állapotát adja; `beemel` a kész táblán alkalmazza a szabályt (idempotens); `jelolt-bontas` a `jelolt` szintet méri; `szuroproba` a rétegzett mintát veszi. A sorok száma a szabály alkalmazásakor nem változik.

**Mért eredmény (2026-11-09).**

| szint | #177 | F181 után | Δ |
|---|---|---|---|
| `megerositett` | 21 314 | 23 973 | +2 659 |
| `kiesik` | 11 027 | 11 041 | +14 |
| `jelolt` | 2 863 | 190 | −2 673 |
| összesen | 35 204 | 35 204 | 0 |

**Figyelmeztetések (részletek: a jelentés 4., 7. és 9. szakasza).**
* A tartomány-végpontok miatt a beemelt MEK-végpontsor és a `kiesik` HunKar-tartománysor azonos tartalmat hordozhat.
* A szúrópróbát a végrehajtó olvasta, nem független ellenőr; olyan MEK-elírást, amely véletlenül értelmes helyre mutat, nem fog meg (alsó becslés).
