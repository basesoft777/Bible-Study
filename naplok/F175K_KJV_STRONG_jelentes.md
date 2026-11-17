# F175.K: a Strong-réteg forrásoldali ellenőrzése a KJV-val, jelentés

*2026-11-17 · ág: `claude/sweet-mendeleev-515ab9` · végrehajtó: claude-sonnet-5-5 · gépi mérés, ellenőri idő nélkül · az 1.0-s adatot nem változtatja*

## 1. Kérdés és eredmény egy mondatban

A nyílt Károli–Strong adatkészletben a Strong-számot program rendeli a párhoz a STEPBible TAHOT/TAGNT forrásszavaiból. Egyeznek-e e forrás Strong-címkéi egy független tanúval, a KJV (eBible) Strong-címkéivel? **Igen: a KJV-ben címkézett 308 378 Strong-előfordulás 98,68%-a (ÓSZ 99,23%, ÚSZ 97,60%) megvan ugyanannak a versnek a TAHOT/TAGNT-címkéi között**, a dokumentált számozási konvenciók (ugyanaz a lexéma más számon) figyelembevételével. A mérés nem rendszerhibát, hanem a KJV-Strong néhány, külön számot adó alakváltozatát találta (l. 5. pont).

A mérés a **párosítást nem méri** (azt az emberi validáció méri); csak azt, hogy a programmal hozzárendelt Strong-számok *forrása* rendben van-e, és hogy a csomag pároknál álló Strong-halmaza mennyit tart meg ebből.

## 2. Módszer

Szkript: `eszkozok/karoli_strong/forras_kjv_ellenorzes.py` (a docstringben a teljes definíció), tesztek: `eszkozok/karoli_strong/teszt_forras_kjv_ellenorzes.py` (kitalált mini-adaton, 18 teszt). Futtatás: `python eszkozok/karoli_strong/forras_kjv_ellenorzes.py`; kimenet az `f175k/` mappában.

- **Egység:** egy Károli-vers (a csomag 31 158 verse) és a `konkordancia/Karoli_versmegfeleltetes.tsv` `igehely_kjv` oszlopa szerinti KJV-vers. Az ÚSZ-re a tábla nem terjed ki: ott a Károli- és a KJV-számozás azonosnak vett. Több Károli-vers egy KJV-versre képeződhet (2 eset: az egység az unió); az a KJV-vers, amelyre egyetlen Károli-vers sem képeződik („árva”), az ugyanabban a fejezetben előtte álló képezett KJV-vers egységéhez tartozik (a Károli összevonta őket); ugyanígy a Károli-vers nélküli TAHOT/TAGNT-vers (3 db az ÚSZ-ben) az előtte álló Károli-vers forráshalmazához. Ez utóbbi eredménye: **a csomag `szavak` táblájának `er` oldala mind a 31 158 versen pontosan egyezik a `TAHOT_kivonat`/`TAGNT_kivonat` Strong-halmazával** (nincs eltérő vers), vagyis a csomag forrásrétege és az itt mért forrás azonos.
- **Halmazok** (versenként, Strong-számonként egyszer, 4 jegyre nullázva): `T_all` = a kivonat összes Strong-címkéje (a „+”-os összetett címke tagjai külön; a H9001–H9049 morféma-kódok kiszűrve); `T_ref` = ÓSZ-ben `T_all`, ÚSZ-ben csak a TR-es tokenek (a repó definíciója: `TR`, `TR»N`, `TR«N`; a KJV a Textus Receptusból fordít); `P` = a csomag `parok/` tábláiban a pároknál álló Strongok (morféma-kód nélkül); `K` = a KJV Strong-címkéi (igealak-kódok, héber > 8674 és görög > 5624, valamint H9001–H9049 kiszűrve; ilyen a KJV-fájlban nem is fordul elő).
- **Konvenció:** a `pontossag_kulso.KONVENCIO` (ugyanaz a lexéma más számon; 2 héber és 5 görög csoport, ott dokumentálva) csoportjai a legkisebb számra képeződnek mindkét oldalon. A `_nyers` változat ezt nem alkalmazza.
- **Fő változat:** `forras_vs_kjv` = `T_all` ↔ `K`, konvencióval. Mellette: `forras_vs_kjv_nyers`, `forras_vs_kjv_tartalmi` (a grammatikai Strongok nélkül, `adat/grammatikai_strongok.tsv`), `forras_TR_vs_kjv` (`T_ref`), `csomag_parok_vs_kjv` (`P`). A fő változat a `T_all`, mert a `TR¹`-szerű (a TR eltérő olvasatát jelölő) tokenek a `T_ref`-ből kimaradnak, a KJV viszont rájuk is címkéz: a szigorúbb TR-változat ÚSZ-ben 96,41%-ot ad.
- **Mérőszámok:** egyező halmaz (T = K) · KJV ⊆ forrás (a KJV minden Strongja megvan a forrásban) · átlagos Jaccard · mikro: a KJV-címkék mekkora része van meg a forrásban, és a forráscímkék mekkora része van meg a KJV-ben. A mérés nem minta, hanem teljes körű (az egységek 99,5%-a), ezért nincs konfidenciaintervallum.

## 3. Eredmények

Az összehasonlított egységek: 30 998 (ÓSZ 23 049, ÚSZ 7 949), ezek 31 000 Károli-versből állnak. Strong-előfordulások: forrás 373 902, KJV 308 378, közös 304 315.

| változat | csoport | egység | egyező halmaz | KJV ⊆ forrás | Jaccard | a KJV-címkék megvannak a forrásban | a forráscímkék megvannak a KJV-ben |
|---|---|---:|---:|---:|---:|---:|---:|
| **forras_vs_kjv** | **összes** | 30 998 | 13,45% | 89,90% | 0,812 | **98,68%** | 81,39% |
| | ÓSZ | 23 049 | 13,62% | 95,48% | 0,788 | **99,23%** | 77,73% |
| | ÚSZ | 7 949 | 12,95% | 73,71% | 0,880 | **97,60%** | 89,91% |
| | Mózes | 5 849 | 9,08% | 96,58% | 0,769 | 99,59% | 75,96% |
| | történeti | 6 962 | 11,81% | 94,53% | 0,788 | 98,98% | 77,69% |
| | költői | 4 924 | 26,81% | 96,47% | 0,822 | 99,19% | 81,27% |
| | próféták | 5 314 | 8,77% | 94,60% | 0,778 | 99,22% | 77,59% |
| | evangéliumok, ApCsel | 4 782 | 9,47% | 70,83% | 0,872 | 97,34% | 89,39% |
| | levelek | 2 763 | 19,07% | 78,75% | 0,891 | 98,02% | 90,59% |
| | Jelenések | 404 | 12,13% | 73,27% | 0,897 | 97,99% | 91,48% |
| forras_vs_kjv_nyers (konvenció nélkül) | összes / ÓSZ / ÚSZ | | 11,55% / 13,38% / 6,24% | 76,41% / 91,28% / 33,30% | | 96,05% / 98,72% / 90,84% | |
| forras_vs_kjv_tartalmi (grammatikai nélkül) | összes / ÓSZ / ÚSZ | | 43,67% / 35,57% / 67,14% | 90,56% / 95,48% / 76,29% | | 98,65% / 99,23% / 97,03% | |
| forras_TR_vs_kjv (ÚSZ: csak TR-es tokenek) | ÚSZ | | 12,68% | 64,74% | | 96,41% | |
| csomag_parok_vs_kjv (a pároknál álló Strongok) | összes / ÓSZ / ÚSZ | | 22,09% / 16,89% / 37,16% | 85,63% / 94,71% / 59,30% | | 97,82% / 99,10% / 95,30% | |

**Hogyan olvasandó.** A „tiszta halmazegyezés” alacsony (13%), és ez *nem hiba*: az eBible KJV-Strong-táblája a szavak jelentős részét (kötőszavak, „minden” H3605, „lenni” H1961, tárgyjel H0853, névelő) egyáltalán nem címkézi, ezért a forrás-halmaz természetszerűen a KJV-halmaz felülhalmaza (89,9%-ban az is). Az érdemi mutató a **KJV-oldali Strongok megléte a forrásban** (98,68%) és a K\T (csak a KJV-ben álló) maradék (4 063 előfordulás, ebből ÓSZ 1 583, ÚSZ 2 480). A konvenció-normálás ÚSZ-ben döntő (a KJV-Strong külön számot ad a névmási és létige-alakoknak): a nyers 90,84% konvencióval 97,60%. A nem TR-es tokenek bevonása (T_all) a KJV-címkék 97,60%-át, a TR-szűrt halmaz 96,41%-át fedi.

A csomag pároknál álló Strong-halmaza a KJV-címkék 97,82%-át tartalmazza (ÓSZ 99,10%, ÚSZ 95,30%); a forrásnál kisebb értékét a párosítatlan (betoldás, fordítatlan, függőben) forrásszavak okozzák, tehát ez nem a párosítás hibaaránya, hanem a lefedettsége a KJV-címkék szempontjából.

### Nem illeszthető versek (okonként; `f175k/nem_illesztheto_versek.tsv`)

| ok | db | megjegyzés |
|---|---:|---|
| `nincs_kjv_megfeleles` | 144 | a tábla `igehely_kjv` oszlopa üres (Zsolt 67, 1Sám 38, Jer 16, Józs 11, 1Kir 7, egyéb 5: a tábla MT-osztályú sorai) |
| `nincs_versmegf_sor` | 9 | a Károli-versnek nincs sora a táblában (4Móz 13:1, Jób 39:1–3, Préd 2:1, 9:1–2, 12:1–2) |
| `kjv_vers_hianyzik` | 5 | a KJV-fájlban nincs ilyen vers (Mk 9:43, Luk 6:41, 17:36, Jel 12:18, 3Ján 1:15) |
| `kjv_vers_karoli_parja_nelkul` | 125 | KJV-oldali: a fejezet elején álló, Károli-pár nélküli KJV-vers (116 Zsolt: a zsoltárfeliratok eltérő számozása; 1Sám 18:1–5, Jób, Péld, Hós) |

A Károli-oldalon 158 vers (0,5%) nem illeszthető, 2 egység két Károli-versből áll; 39 egységhez 92 árva KJV-vers kapcsolódott. A kapcsolás javít: a forráscímkék KJV-ben megvolta 0,677-ről 0,793-ra nő a kiegészített egységeken. 17 egységben a KJV-címkék kevesebb mint fele van meg a forrásban (≥ 4 KJV-Strong; `f175k/alacsony_atfedesu_egysegek.tsv`: Józs 8:29, 1Sám 17:11, 18:9, 18:16, 1Kir 6:10, Jer 33:13, Mt 15:6 stb.), ezek a versösszevonás/számozás-táblabeli eltérések jelölt-helyei; **egyetlen fejezetben sem ≥ 40% az ilyen egységek aránya**, tehát versszámozási eltolásra nincs jel.

## 4. A „meglepően alacsony” feltétel

A brief 4. pontja szerint megállás kellene, ha az egyezés meglepően alacsony vagy rendszerhibára utal. A tiszta halmazegyezés (13%) első ránézésre alacsony, de a fenti ok miatt szerkezeti (a KJV-tábla részleges címkézése), és a 3. pont táblája mutatja a tényleges mérőszámot: 98,68%, a 30 998 egységből 27 866-ban (89,9%) a KJV minden Strongja megvan a forrásban, 28 073-ban (90,6%) legalább a 95%-uk. Rendszerhibára (eltolt versek, fordított könyvsorrend) nincs jel; ezért a mérés nem állt meg. Az adathoz nem nyúltam.

## 5. Gyanús forráscímkék (`f175k/gyanus_forrascimkek.tsv`)

A lista **jelölt-lista kézi ellenőrzésre**, nem hibalista. Típusok: `csak_forras` (T\K), `csak_kjv` (K\T), `csere` (a tartalmi halmazokból: az egységben pontosan egy csak-forrás és egy csak-KJV elem). Szabály: ≥ 5 vers, ≥ 50% arány, nem grammatikai Strong; a `csak_forras` csak akkor gyanús, ha van csere-partnere; a `csere` akkor, ha nem ismert konvenció. Az 50 + 50 + 50 legnagyobb tétel és minden gyanús jelölt benne van (124 gyanús: 63 csak_kjv, 21 csak_forras, 40 csere).

A K\T 4 063 előfordulásából 1 301 a gyanús `csak_kjv` Strongokon áll. A jelöltek javarésze **a KJV-Strong külön számot adó alakváltozata**, nem a TAHOT/TAGNT hibája: ugyanaz a lexéma a forrásban az egyik, a KJV-ben a másik számon (fokozás, igető, névmási alak, névvariáns). Az 1.2-be javasolt konvenció-bővítés legerősebb jelöltjei (a csere-pár: TAHOT/TAGNT → KJV, vers-darabszám): G0757→G0756 (ἄρχω/ἄρχομαι, 56), G3441→G3440 (μόνος/μόνον, 44), G4413→G4412 (πρῶτος, 37), G4483↔G2046 (ἐρῶ/εἶπον igetövek, 29 + 21), G2089→G3765 (οὐκέτι, 27), G0681→G0680 (ἅπτω, 25), H5117→H3240 (נוּחַ, 23), G4218→G3379 (μήποτε, 19), G3403→G3415 (μιμνήσκω, 18), G2396→G1492 (ἴδε/ἰδού, 17), G3173→G3187 (μέγας fokozás, 17), G4571→G4572 (σεαυτόν, 16), H2396→H3169 (Ezékiás neve, 15), H2895→H2896 (טוֹב, 12). További 8 pár 10–12 vers. A `csak_kjv` jelöltek közül külön figyelmet kér a G2504 (καγώ, 67 vers: a TAGNT crasist két szóra bontja), a G1699 (ἐμός, 63) és a G5126 (τοῦτο, 63): ezek kézi megnézése dönti el, hogy konvenció vagy valódi hiány.

Ezek a számok az 1.0-s adatban nem változnak; a konvenció-bővítés a mérést javítaná (a K\T a jelöltek 1 301 előfordulásával csökkenne ~32%-kal), de a mérés itt szándékosan a meglévő, dokumentált `KONVENCIO`-val készült, hogy ne a mért adatból építsünk mércét.

## 6. Korlátok

- **A KJV-tábla részleges tanú.** Az eBible KJV-Strong-tábla (`KJV_Strongs_teljes.tsv`) a szavaknak csak egy részét címkézi, és az „angol szó” néha frázis. Ezért csak a K\T iránya érdemi; a T\K nem hibajel (a `csak_forras` lista informatív).
- **KJV = Textus Receptus.** A TAGNT kritikai szövegű, a TR-eltérő olvasatok csak részben szerepelnek soraiként; a TR-ben lévő, a TAGNT-ban nincs sorral bíró szó K\T-ként jelenik meg (ez szövegvariáns, nem címkehiba). A T_all/T_ref különbség (97,60% / 96,41%) ennek a mértéke.
- **A konvenció-tábla szűk** (2 + 5 csoport); a további konvenció-jelöltek a 5. pontban. A számok ezeket nem alkalmazzák.
- **Versleképezés:** az ÚSZ-ben azonos számozás feltételezett; a tábla 144 + 9 ÓSZ-versre nem ad KJV-megfelelőt; a Zsolt-feliratok és az 1Sám 17–18 számozása eltérő (116 + 5 árva KJV-vers). Az árva-kapcsolás feltevés (a Károli összevont), ezért a K_alap/K_ext különbség külön áll a diagnosztikában.
- **Nem független a TAHOT/TAGNT és a KJV Strong-rendszere teljesen:** mindkettő a Strong-számozásból indul, így a mérés a *szövegazonosítás* hibáit (rossz lexéma) jól, a közös Strong-rendszer *szisztematikus* hibáit nem látja.
- **A STEPBible-commit** (`efe428a0047b`) itt nem ellenőrizhető; a mérés a repó `TAHOT_kivonat.tsv`/`TAGNT_kivonat.tsv` fájljait használja (letöltve 2026-08-24), amelyekkel a csomag `er` oldala mind a 31 158 versen egyezik.

## 7. Javaslat a kéziratba

**Magyarul.** „A Strong-réteg forrásoldalának független ellenőrzéseként versenként összevetettük a STEPBible TAHOT/TAGNT forrásszavainak Strong-számait a KJV (eBible) Strong-címkézésével, 30 998 összehasonlított versegységen (a versek 99,5%-án). A KJV-ben címkézett 308 378 Strong-előfordulás 98,7%-a megtalálható az azonos vers forráscímkéi között (ÓSZ 99,2%, ÚSZ 97,6%), a dokumentált számozási konvenciók (ugyanaz a lexéma más számon) egyenértékűnek véve. A KJV nem címkéz minden forrásszót, ezért az ellenőrzés a forráscímkéket vizsgálja, a párosítást nem; ez utóbbi pontosságát külön mérjük. A fennmaradó eltéréseket a KJV-Strong külön számot adó alakváltozatai (pl. G0756/G0757) magyarázzák; a jelölt-lista a kiegészítő anyagban áll.”

**English.** “As an independent check on the source-side Strong's layer, we compared, verse by verse, the Strong's numbers of the STEPBible TAHOT/TAGNT source words with the Strong's tagging of the King James Version (eBible) over 30,998 aligned verse units (99.5% of verses). 98.7% of the 308,378 Strong's occurrences tagged in the KJV are present among the source labels of the same verse (OT 99.2%, NT 97.6%), treating documented numbering conventions (one lexeme, two numbers) as equivalent. The KJV does not tag every source word, so this check tests the source labels, not the alignment, whose accuracy is measured separately. The residual differences are explained mostly by KJV Strong's numbers that split a lexeme into separate numbers (e.g. G0756/G0757); the candidate list is in the supplementary material.”

## 8. Mi menjen a letétbe

Javaslat a következő adatverzióhoz (1.2) vagy a kézirat kiegészítő anyagához (a Zenodo-rekord a mért 1.0-t nem érinti): **`f175k/meres_osszesites.tsv`** (az összesítő számok, könyvenként is) és **`f175k/gyanus_forrascimkek.tsv`** (a jelölt-lista Strong-számokkal, STEPBible-lemmával és -jelentéssel, KJV-szóval, példaversekkel). A `diagnosztika.tsv` (számlálók) opcionális, a `nem_illesztheto_versek.tsv` és az `alacsony_atfedesu_egysegek.tsv` a repóban marad (belső munkaanyag; bennük csak igehely és szám van). **A szkript nem megy a letétbe** (a kód nem nyílt, csak az adat); a TSV-k fejlécének `forras=` mezője belső útvonalakat sorol, a letét előtt a csomag-szintű proveniencia-sorra cserélendő. Licenc: a TAHOT/TAGNT-adatra (CC BY 4.0, Tyndale House Cambridge / STEPBible.org) a csomag meglévő attribúciója vonatkozik; a KJV (eBible) public domain. A kimenetben nincs Károli-szöveg és nincs zárt (Bible-Discovery) forrásból való adat.

## 9. Proveniencia és reprodukálás

`scope=F175K forrásoldali Strong-ellenőrzés (TAHOT/TAGNT vs KJV, versenként, szóhalmaz-szinten) | forras=konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/KJV_Strongs_teljes.tsv (eBible, sha256 a fájl fejlécében), konkordancia/Karoli_versmegfeleltetes.tsv, nyilt_karoli_strong/data (Zenodo 1.0, DOI 10.5281/zenodo.24141883) | ts=git:<a kimenet fejében> | manual (determinisztikus szkript, nincs lekérdezés és nincs modellhívás)`

Reprodukálás: `python eszkozok/karoli_strong/forras_kjv_ellenorzes.py` (kb. 15 s, hálózat nélkül); a számok minden sora a `f175k/meres_osszesites.tsv`-ben és a `f175k/diagnosztika.tsv`-ben áll.
