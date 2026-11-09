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

## 7. A jelölt szint feldolgozása — a beemelési szabály (F181; DT-F181d, DT-F181e, DT-F181f, DT-F181g, DT-F181h, DT-F181i)

**A szabály egy helyen (ez a szakasz); a megvalósítás: `eszkozok/karoli_kh_mek.py` (`jelolt_bontas`, `beemel`); tesztek: `eszkozok/teszt_karoli_kh_mek.py` (`JeloltSzabaly`, `RepoTablak`).**
Az alap a felhasználó szava (2026-11-09, szó szerint): „TSK külön rendszer, nem kell összevetni őket. Károlinak meg elfogadjuk a MEK-et, ha ott nem volt gyanús ismétlődő.” Módosításai: DT-F181e (orkesztrátori döntés, nem felhasználói: az elírás-gyanús osztály jelölt marad) és DT-F181f (a felhasználó: „beemeljük”: a HunKar-oldali gyanús-jelölés nem zár ki).

**1. A MEK-oldali `jelolt` sor (`forras=MEK`, azaz a MEK-ben áll, a HunKar-ban azon a versen nem) `megerositett` lesz**, kivéve, ha
* a hivatkozott vers vagy a forrásvers **nem létezik** (a versellenőrzés alapja a 4. szakasz: `Karoli_1908` ∪ MEK-versszerkezet) → `jelolt` marad (`hibas_hivatkozas`);
* a MEK-cél az **E2-hibaminta létező töredéke** (F181 javítókör 1; DT-F181h, ELLENOR_F181 E2): a MEK a HunKar `X a:b` (a: fejezet, b: vers) célját két töredékre bontva adja: `X c:a` és `X c:b`, ahol `c` az előző hivatkozás fejezete, és a két töredék egymás után áll a versen (Neh 1:5: HunKar 9:32, MEK `4,9` és `4,32`; Zsolt 35:12: HunKar 41:10, MEK `38,41` és `38,10`). A gépi felismerés (`karoli_kh_mek.e2_mintak`): két egymás utáni MEK-sor azonos könyvvel és fejezettel (`c`), versszámaik `a` és `b`, `a ≠ c`, az `X a:b` létező vers, és a két töredék közül legalább az egyik nem létezik. A **létező töredék** (Neh 4:9, Ján 9:12, ApCsel 11:13) nem emelődik be, `jelolt` marad; a nem létező társa a nem létező célok közt marad. Ha a forrásversen van HunKar-sor, amely `X a:b`-vel kezdődik (vers vagy tartomány), az a minta megfelelője: `megerositett` (a HunKar-tartomány további versei, `X a:b+1` …, ha a MEK-ben `X c:b+1` … következik, a mintához tartoznak: Zsolt 27:4 → 42:2–3, MEK `23,42` + `23,2` + `23,3`); indoka `…;mek_fejezet_minta=<a töredékek>;szabaly=F181`. A mintának nem kell HunKar-megfelelője legyen: HunKar-megfelelő nélkül is `jelolt` a létező töredék (hiányt nem töltünk ki; a helyes cél `X a:b` a HunKar-sor nélkül nem kerül a táblába);
* a forrásvers **MEK-oldali gyanús ismétlődő**: a forrásvers MEK-listája (legalább 2 különböző cél) szó szerint azonos egy másik forrásvers MEK-listájával → `jelolt` marad. (A `Karoli_kereszthivatkozasok_gyanus.tsv` HunKar-oldali jelölése **nem** zár ki: az a HunKar-lista másoltságát jelzi, a MEK-lista ilyenkor a javító tanú; DT-F181f.)
* a MEK-cél **egyetlen összetevőben** (könyv, fejezet vagy versszám) tér el a forrásvers egy jelölt HunKar-sorának céljától (**elírás-gyanús osztály**, DT-F181e: a végrehajtói olvasat szerint 15 sorból 4 valószínű MEK-elírás; a javítókörben az E2-szűrő 5 sort kiemelt, 10 marad) → `jelolt` marad.
A `megerositett` MEK-sor `forras=MEK`, indoka `csak_mek;mek_alak=…;tsk=…;szabaly=F181`.

**2. A HunKar-oldali `jelolt` sor** (`eltero_lista`: a HunKar-sor, amelyet a MEK a versen nem listáz, de más hivatkozást igen). A sorrend:
* **az E2-hibaminta megfelelője → `megerositett`** (az 1. pontban leírt minta; DT-F181h): indoka `eltero_lista;tsk=…;mek_fejezet_minta=<a töredékek>;szabaly=F181`;
* **a MEK a tartomány egyik végpontját adja → a tartomány megmarad** (F181 javítókör 1; DT-F181i, ELLENOR_F181 E3): ha a HunKar-sor rendezett tartomány (`A-B`, A < B, mindkét vég és a forrásvers létezik), és a forrásvers MEK-listájában a tartomány **egyik végpontja** áll (a másik végpont hiányzik, vagy értelmezhetetlen alakban áll, pl. `1 Sám. 12,.`: a megmaradt szám a tartomány végének versszáma), a MEK nem ellentmond a tartománynak, a tartomány vége nem veszhet el. A HunKar-sor `forras=HunKar+MEK`, `megerositett`, indoka `eltero_lista;tsk=…;mek_vegpont=<a végpont>[;mek_vege_elirt=<a MEK szó szerinti alakja>];szabaly=F181`. Hogy ne keletkezzen duplikáció, és a tábla többi tartománykezelésével összhangban (az `egyezik` tartománynál a MEK-végpontok sem önálló sorok), a MEK-végpontsor és az értelmezhetetlen társa `kiesik` (`forras=MEK`, indoka `…;tartomany_vegpont=<a tartomány>;szabaly=F181`): a lap/index a tartományt egyszer kapja. Fordított tartományra (a vég kisebb a kezdetnél, a HunKar-adat hibás) a szabály nem vonatkozik. **Szűkítés egyfejezetes könyvben (DT-F181n; Opus-szúrópróba, `naplok/F181_szuroproba.md` 131., 133–136.):** ha a könyv minden verse az 1. fejezetben áll (Abd, Filem, 2Ján, 3Ján, Júd; a létező versek halmazából), a HunKar-tartomány a könyv elejétől indul (`1:1-N`), és a MEK az `1:N` verset adja, a tartomány műtermék (a HunKar a levél elejétől az N. versig tartományt ad, a MEK a pontos verset): a MEK-vers `megerositett` (`forras=MEK`, indoka `…;egyfejezetes_tartomany=<a tartomány>;szabaly=F181`), a HunKar-tartomány `kiesik` (indoka `eltero_lista;tsk=…;egyfejezetes_tartomany_muterek=<a vég>;szabaly=F181`). Más tartományra (többfejezetes könyv, vagy nem a könyv elejéről induló tartomány, pl. Filem 1:5–7) az E3 változatlan. Példák: 2Kor 7:4 → Filem 1:8, Kol 1:7 → 1:23, Kol 4:9 → 1:10, Kol 4:14 → 1:24, Kol 4:15 → 1:2. Példák: 2Sám 7:8 → 1Sám 16:11–12 (MEK `16,11` + `12,.`), 2Kir 21:5 → 2Kir 23:11–12, 1Krón 6:14 → 2Kir 25:18–21; végpont-párral (a MEK csak a tartomány végét adja): Kol 4:9 → Filem 1:1–10 (MEK `1,10`);
* **a MEK-pár nem ellentmond neki → `megerositett`** (DT-F181g, ELLENOR_F181 E1): ha a HunKar-sor célverse létezik, és a MEK-oldali párja (a MEK-sor, amely egyetlen összetevőben tér el tőle: könyv/fejezet/versszám) **nem létező** célra mutat, a MEK-hiba nem ítélheti el a helyes HunKar-sort. A sor `forras=HunKar`, `megerositett`, az indoka `eltero_lista;tsk=…;mek_par_nem_letezik=<a MEK szó szerinti alakja>;szabaly=F181`. A döntés a sor saját párjától függ, nem attól, hogy a versen más, független MEK-sor beemelődik-e. Példák: Lev 23:17 → Lev 2:12 (MEK `2,17`), Józs 22:3 → 11:18 (MEK `11,28`), Zsolt 143:3 → 1Sám 23:7–8 (MEK `23,78`), ApCsel 21:8 → 8:26–40 (MEK `12,26`, `12,40`), Ef 2:20 → Ézs 28:16 (MEK `18,16`); a Neh 1:5, Ján 8:12 és ApCsel 14:22 az E2-megfelelő (az első pont);
* ha a sor egy elírás-gyanús MEK-sor párja → `jelolt` marad (a pár eldöntetlen: a HunKar-cél lehet a helyes);
* egyébként `kiesik`, ha a forrásvers MEK-listájából legalább egy sor beemelődik (a MEK-lista a versen irányadó, és a sor abban nincs); különben `jelolt` marad. A `kiesik` itt nem állítja, hogy a HunKar-sor hibás: a MEK-lista elfogadásának következménye.

**3. Az `egyezik`, de nem létező hivatkozású sor (`HunKar+MEK`) `jelolt` marad.**

**4. A TSK nem tanú és nem feltétel.** A `tsk=igen|nem` jelölés az indokban tájékoztatás marad (ELLENOR_F177 1.), a szabály nem használja.

**5. A döntés nélküli maradék `jelolt` marad** (hiányt nem töltünk ki, CLAUDE.md 3. szabály; a lapra/indexbe nem jut). **Minden ilyen sor a saját indokában hordozza a maradás okát**: `…;marad=<kód>` (F181 javítókör 1; DT-F181k, ELLENOR_F181 E8; új oszlop nélkül; egy sor pontosan egy kódot kap). A kódok és a sorok száma:

| kód | sor | jelentés |
|---|---|---|
| `marad=nem_letezo_cel` | 136 | a hivatkozott vers vagy a forrásvers nem létezik (a `Karoli_1908` ∪ MEK-versszerkezet szerint), vagy a MEK-sor értelmezhetetlen; ide tartozik az `egyezik;hibas_hivatkozas=…` sor is (tételesen: `naplok/F181_jelentes.md` A. függelék) |
| `marad=gyanus_ismetlodo` | 6 | MEK-oldali gyanús ismétlődő: a forrásvers MEK-listája szó szerint azonos egy másik vers MEK-listájával |
| `marad=eliras_gyanus` | 10 | a MEK-cél egyetlen összetevőben tér el a forrásvers egy jelölt HunKar-sorának céljától, és létezik (DT-F181e) |
| `marad=mek_fejezet_minta` | 9 | az E2-hibaminta létező töredéke (DT-F181h) |
| `marad=eliras_gyanus_par` | 10 | HunKar-oldali sor, amelynek MEK-párja elírás-gyanús vagy E2-töredék sor: a pár eldöntetlen |
| `marad=mek_lista_nincs_elfogadva` | 11 | HunKar-oldali sor, amelynek forrásversén a MEK-lista egyik sora sem emelődik be (nem létező cél, gyanús ismétlődő), tehát a HunKar-sor sorsáról nincs mi alapján dönteni |

Összesen **182** sor. A maradékról nincs döntés; a szúrópróba és a mért hibaarány: `naplok/F181_jelentes.md` 7. szakasz, az új minta tételei: `naplok/F181_szuroproba.md`.

**6. A fogyasztók.** A `karoli_kh_szuro.mek_sorok()` a csak a MEK-ben álló, `megerositett` sorokat adja (a HunKar-tábla kulcsaival és magyar megjelenítéssel); a `lekerdez.py` (`karoli`), a `sqlite_epit.py` (`kh` tábla), az `olvaso_pilot/adat.py` és az `olvaso_mockup/nav_kinyer.py` a HunKar-sorok mellé ezeket is olvassa, ugyanazzal az `elfogad` szűrővel. A `kiesik` és a `jelolt` sor nem jut át. A lapokat és a `pardes.db`-t ez a menet nem építette újra (N-F177a).

**Előállítás.** `python eszkozok/karoli_kh_mek.py osszevet` a #177 összevetése **és** a beemelési szabály együtt (a tábla fejléce: `osszevet + beemel`); `osszevet --nyers` a #177 háromszintű nyers állapotát adja; `beemel` a kész táblán alkalmazza a szabályt (idempotens); `jelolt-bontas` a `jelolt` szintet méri; `e2-meres` az E2-hibaminta teljes mérése; `szuroproba` a rétegzett mintát veszi (`--md`: tételes táblázat üres ítélet-oszloppal). A sorok száma a szabály alkalmazásakor nem változik.

**Mért eredmény (2026-11-09; a javítókör 1 után, ELLENOR_F181 E1–E3 és E8).**

| szint | #177 | F181 után | Δ |
|---|---|---|---|
| `megerositett` | 21 314 | 23 981 | +2 667 |
| `kiesik` | 11 027 | 11 041 | +14 |
| `jelolt` | 2 863 | 182 | −2 681 |
| összesen | 35 204 | 35 204 | 0 |

A +2 667 `megerositett`: 2 647 MEK-sor, 12 HunKar-sor (5: a MEK-pár célja nem létezik; 7: az E2-hibaminta megfelelője), 8 HunKar-tartomány (a MEK az egyik végpontot adja). A +14 `kiesik`: 3 HunKar-sor (a MEK-lista elfogadva a versen) és 11 MEK-végpontsor (a megerősített HunKar-tartományba olvad). A `megerositett` sorok forrása: `HunKar+MEK` (egyező; a tartomány), `MEK` (beemelt), `HunKar` (a MEK-pár nem ellentmond).

**Figyelmeztetések (részletek: a jelentés 4., 7., 9. és 10. szakasza).**
* A tartomány-végpontok duplikációját az E3 szabály kezeli: a megerősített HunKar-tartomány mellett a MEK-végpontsor `kiesik` (nem önálló sor).
* A szúrópróbát az első körben a végrehajtó olvasta, nem független ellenőr (alsó becslés: olyan MEK-elírást, amely véletlenül értelmes helyre mutat, nem fog meg). A javítókör utáni új minta tételei ítélet nélkül: `naplok/F181_szuroproba.md`; az ítéletet Opus hozza (DT-F181j).
* Az E2-hibaminta HunKar-megfelelő nélküli esete (1Kir 2:26 → 1Sám 22:20) tartalmilag helyesnek látszik, de a szabály szerint `jelolt` (N-F181f, az orkesztrátor döntésére vár).

## 8. A beemelt sorok maradék hibája (adatleírás; F181, DT-F181o)

A `Karoli_KH_javitott.tsv` `megerositett` szintje a MEK-ben álló, beemelt sorokat (`forras=MEK`) is hordozza. **A MEK irányadó; a maradék hiba a MEK saját elírása.** A hibát az Opus-szúrópróba mérte (`naplok/F181_szuroproba.md`, 136 tétel, mag=181; ítélet: `claude-opus-5-5`, a két vers Károli-szövege alapján; részletek és az összes réteg: `naplok/F181_jelentes.md` 7.1). Rétegenként (n, hibás, arány, 95% Wilson-intervallum, score-módszer, z = 1,96):

| réteg | n | hibás | hibaarány | 95% Wilson-intervallum |
|---|---|---|---|---|
| kontroll: beemelt MEK-sor | 40 | 1 | 2,5% | 0,4% – 12,9% |
| HunKar-gyanús forrásversen beemelt MEK-sor | 30 | 1 | 3,3% | 0,6% – 16,7% |
| E1/E2/E3: megerősített HunKar-sor (az E3-szűkítés után, levezetve) | 15 | 0 | 0,0% | 0,0% – 20,4% |

* A két hibás beemelt sor `csak_mek` és `tsk=nem` (létező, de idegen versre mutató MEK-elírás: 5Móz 14:21 → 4Móz 22:28; 2Kor 3:5 → Ján 15:15). A hibaarány alsó becslés: egyetlen modell olvasata, a véletlenül értelmes helyre mutató elírást nem fogja meg. A két beemelt réteg mintája átfed (egy közös táblasor).
* A TSK külön, egyenrangú rendszer, nem tanú és nem feltétel (DT-F181o), ezért a sorban TSK-alapú kockázati jel nincs.
* A jelöltben maradt és az E-szabályokkal döntött többi réteg (gyanús ismétlődő 0/6, elírás-gyanús 4/10, HunKar-sor jelölt marad 9/20, E2-szűrt 7/9) a lapra/indexbe nem jut; a magas arányuk a jelölt szint indokoltságát mutatja.
* Az E3-szűkítés (DT-F181n) előtt az E1/E2/E3 réteg 4/20 hibás volt (20,0%, 8,1% – 41,6%); mind a 4 az 5 Filem-tartományból, amelyek a szűkítés után `kiesik`-ek. A helyükre emelt 5 MEK-vers a mintában nem szerepelt.
