# BDB magyar szakasz-illesztés — „csak a jelölő” sorok (jelentés)

*Csak olvasás, adatot nem módosít. Tétel nincs hozzárendelve; javításhoz új tétel kell (az F107 lezárt, `naplok/BDB_JELOLT_SZOVEG_zaras.md`). A jelentés heurisztikus mérés, nem soronkénti átnézés.*

proveniencia: `scope=adat/bdb_szakasz_hu.tsv (674 Strong, 9 664 sor) | forras=ad hoc szűrés (a leírt feltétellel), nem repó-eszköz | ts=2026-10-25`
bemenet: `adat/bdb_szakasz_hu.tsv` sha1 `2dcfad3cea24`; repó-HEAD `c454c4d43d7d`

## 1. Kiváltó eset

H0001 (אָב, BDB17): a `-/1/-` sor (1. jelölő) szövege csak „1.”. Az 1. pont tényleges magyar szövege („— 1 az egyén atyja 1Móz 2:24 …”) a következő, `-/2/-` sorban áll, amely 2 181 karakteres, és a fejléc folytatását, az 1. és a 2. pontot együtt tartalmazza.

Ok: a forrás fejlécében (`BDB_teljes_unabridged.tsv`, H0001) a „Sabean אב CIS^iv, 1, 37 **1.** **2** and others, Ethiopic…” töredék szám-szerű szövegrészt tartalmaz. A magyarban ez „1, 37 1. 2 és mások”. Az illesztő (`hu_illeszt.py`) a jelölőket számmal, sorrendben keresi, ezért az 1. jelölőt az „1.”-hez, a 2.-at a „2 és mások”-hoz kötötte; mindkét sor `illeszkedik` kategóriát kapott, vagyis a kategória itt hamis egyezést takar.

A szakasztábla (`bdb_szakaszok.tsv`, 3. sor) az angol szövegben az 1. pontot helyesen elkülöníti, és az igehely-tábla (`bdb_vers_jelentes.tsv`, `-/1`: 49 hely) is helyes csoportban van. A hiba csak a magyar illesztés rétegében van.

## 2. Mérés

Feltétel (A): `kategoria = illeszkedik`, `jel` nem üres, és a `szoveg_hu` rövidebb vagy egyenlő, mint a jelölő + 3 karakter (azaz gyakorlatilag csak a jelölő).

Eredmény: **26 sor, 26 szócikk** a 674-ből (3,9%). A jelölő-eloszlás: „3” 6, „1” 5, „Hiph`il” 3, „Niph`al” 3, „2” 3, „Pi`el” 2, „5” 1, „Qal.” 1.

Tágabb kör (B): `illeszkedik`, jelölővel, a szöveg 12 karakternél rövidebb és nem A-beli: 79 sor, 70 szócikk (nem vizsgált).

A tábla kategóriái: `illeszkedik` 6 395, `jelolo_nelkul` 2 461, `elakad` 606, `horgonnyal` 202. Az `elakad` a #38 / N-F107b ismert hiánya, ez nem azonos az itt vizsgált hibával.

## 3. Az A-csoport három típusa

Besorolás a következő sor és az előző sor vége alapján, kézi átnézés nélkül.

| Típus | Db | Szócikkek |
|---|---|---|
| (a) szerkezeti: a jelölő után „a.”, „b.” alpontok jönnek, az „1.” csoportcím | 6 | H1129, H1980, H3499, H4519, H6965, H7130 |
| (b) a jelölő a szöveg végére esett, utána üres vagy nincs sor; az előző sor vége szövegközi említés („…Hiph`il imperfectum”, „…1. látnia adatik”) | 13 | H3423, H3603, H5324, H5826, H6299, H7122, H7200, H7218, H7378, H7650, H7725, H7896, H7971 |
| (c) fejléc-töredékhez kötött vagy bizonytalan | 7 | H0001, H2199, H3381, H5027, H5060, H6499, H7043 |

Megjegyzések:
- (a): valószínűleg nem hiba; a `horgony`-ellenőrzés tartalmilag nem igazolt.
- (b): a jelölő szövegközi számhoz vagy törzsnévhez kötődött; a valódi szakasz tartalma ilyenkor feltehetően az előző sor szövegében van. A H5324, H7218, H7650, H7971 előző sora üres, itt a jelölő a szakasz első sora; ezekre külön vizsgálat kell.
- (c): a H0001 igazolt (1. pont). A H2199, H3381, H5027, H5060 törzsnév-sorok, amelyeknek a tartalma a következő sorban áll; a H6499 („b. és”) és a H7043 folytatásnak látszik. Mindegyik soronkénti ellenőrzést kér.
- A H0001-féle „1. 2” töredék szövegkereséssel (`\s1\.\s+2\s` a `fej` szövegében) a teljes táblában csak a H0001-ben van.

## 4. Következtetés és javaslat

A tényleges, javítandó kör mintegy 20 szócikk (13 + 7), nem a teljes 674. A hibatípus nem egyetlen forráshibára vezethető vissza: a (b) csoport az illesztő jelölőkeresésének (szövegközi szám- és törzsnév-említések) hibája, a H0001 pedig a forrás hibás számtöredéke.

Javaslat új tételre (az F107 lezárása miatt):
1. a 13 + 7 szócikk soronkénti átnézése, pontos okok rögzítése;
2. a `hu_illeszt.py` jelölőkeresésében a szövegközi említés kizárása (pl. mondatvégi vagy zárójelen belüli szám/törzsnév nem jelölő), vagy a fejléc-töredék („szám + 1, 37 1. 2”) kezelése;
3. újragenerálás és a `kategoria` újramérése; a B csoport (70 szócikk) szúrópróbás átnézése;
4. a H0001-nél a HTML-nézet (`H0001_bdb.html` a scratchpadben) mutatja a következményt: az „1.” szakasz alatt csak a jelölő áll, a hozzá tartozó szöveg a 2. alatt.

Nem érinti az igehely-feloldást (`bdb_vers_jelentes.tsv`), amely az angol szakasztáblára épül.
