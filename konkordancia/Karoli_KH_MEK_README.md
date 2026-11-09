# Karoli_KH_MEK — a MEK 00161 kiadás Károli-kereszthivatkozásai (F177, KAROLI_KH_MEK)

A `Karoli_kereszthivatkozasok.tsv` (HunKar OSIS ← szentiras.hu KG) ismert hibája, hogy sok vers egy másik vers
KH-listáját hordozza (N-F156a). A MEK 00161 kiadás (*Szent Biblia*, Károli) versenként, a vers alatt adja a KH-t,
a HunKar-tól függetlenül: **ez a második, független tanú**. A MEK-ből származó tartalom **belső tanú**: a nyílt
magba, a lapokra és bármely kimenetbe addig semmi nem kerül belőle, amíg a felhasználó a licencet nem erősíti meg
(l. „Licenc”).

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
vers-szerkezetében. A `Karoli_1908.tsv` KJV-számozású, és néhány fejezetben összevon (pl. Ján 1:51–52 egy versként), míg
a MEK és a HunKar a Károli-számozást követi; a kettős alap miatt a valódi Károli-versek nem esnek ki. A nem létező vers
`hibas_hivatkozas` jelöléssel marad a táblában. Mért: 14 MEK-vers nincs a `Karoli_1908.tsv`-ben (1Kor 3:23, Préd 2:27, Hós 1:12,
Hós 11:12, Ézs 3:28, Ézs 9:21, Ján 1:52, Jób 16:23, Jób 36:34, Luk 23:57, 4Móz 29:40, Péld 11:32, Róm 3:31, Róm 8:39), és 2
`Karoli_1908`-vers nincs a MEK-ben (Ézs 4:6, Zak 9:17); a MEK összesen 31 170 verse a `Karoli_1908.tsv` 31 158 versével szemben.

## 5. Licenc

A MEK szerzői jogi oldala (https://mek.oszk.hu/html/allando/copyright.htm, lekérve 2026-11-09): „*Digitális formában
szabadon másolható, de csak saját célokra, nem-kereskedelmi jellegű felhasználásra, változtatások nélkül és a forrásra
való megfelelő hivatkozással: "Országos Széchényi Könyvtár, Magyar Elektronikus Könyvtár".*” A dokumentum a szerzői
jogról szóló 1999. évi LXXVI. törvény IV/B. fejezete (kereskedelmi forgalomban nem elérhető művek) alapján került
fel. A tétel katalóguscédulája ugyanakkor: „*Jogi közlemény: Nem jogvédett*”. **A felhasználónak külön meg kell
erősítenie** (a Sefaria-döntés elve szerint: közkincs tartalomnál a szerzői jog az irányadó), mielőtt a MEK-ből
származó bármi a kimenetbe (lap, nyílt mag) kerül. Addig a `licencek.tsv` sora `kereskedelmi=feltetelesen`, `allapot=tisztazatlan`,
és a MEK belső tanú. A javított tábla a saját döntésünk; a MEK szövege (a versszöveg) nem került át, csak a
hivatkozás-tény és a szó szerinti hivatkozás-alak (`mek_alak`).

## 6. Mért eredmény (2026-11-09; részletek: `naplok/F177_jelentes.md`)

A `Karoli_KH_javitott.tsv` 35 204 sora: **megerositett 21 314**, **kiesik 11 027**, **jelolt 2 863** (ebből 2 797 csak a MEK-ben
szereplő hivatkozás, 44 eltérő lista, 22 egyező, de nem létező hivatkozott verssel). A 32 407 HunKar-sor mindegyike pontosan egyszer szerepel.
A MEK 13 171 versén áll KH (29 987 sor); a HunKar-táblában 19 817 forrásvers.

Versenként (a HunKar `Karoli_kereszthivatkozasok_gyanus.tsv`-vel): a 5 078 gyanús vers közül 4 773-nak a MEK-ben nincs KH-ja,
261 teljesen egyezik, 44 eltér; a nem gyanús versek közül 11 396 egyezik, 1 438 eltér, 1 905-nek a MEK-ben nincs KH-ja, 32 csak a
MEK-ben szerepel. **Hibás hivatkozás** (nem létező hivatkozott vers) 161 sorban van (142 különböző nem létező vers): 117 csak MEK-sor
(114 nem létező hivatkozott vers, a MEK-elírások, pl. `2 Móz. 26,59` a 2Móz 6:20-nál, `1 Móz. 15,26` az 5Móz 7:15-nél), 22 egyező sor (mindkét forrás ugyanazt a hibás
hivatkozást hordozza, pl. 1Krón 28:8 → 4Móz 28:68), 22 `kiesik` HunKar-sor. A 117 csak MEK-sor között 3 nem értelmezhető MEK-sor van (`1 Sám. 12,.`, `2 Kir. 12,.`, `2 Kir. 21,.`:
a versszám hiányzik; `indok`: `hibas_hivatkozas=ertelmezhetetlen`).
**Korlát:** a MEK a tartományt két végponttal adja, ezért a `csak_mek` sorok között tartomány-végpontpárok is lehetnek; a sorok eldöntése
(N-F177b) nem része a menetnek.
