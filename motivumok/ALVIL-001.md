# Hádész (Seol) — a halottak birodalma

<!-- FORRÁSRÉTEG (F4 G2) — kézzel írt, szabadon szerkeszthető. NEM generált fájl. -->

【NAPLO: F123 M3, 2026-10-29 — a forrás a régi tematikus tanulmány (`archivum/ALVIL-001/Hadesz_Seol_tematikus.md`), a kereszthivatkozás-napló és a régi forrásréteg szétválasztásával készült, a `naplok/F123_szetvalasztas_ALVIL-001.tsv` jóváhagyott leképezési táblája szerint (DT-F123g (a)); sablon: 9_ v0.3 (tervezet, az első 2. lépcsős motívum mint sablon-próba, DT-F123a).】

【NAPLO: Seol-egységesítés — orkesztrátori döntés, 2026-10-29 (DT26: `adat/terminologia.tsv` She'ôl → Seol), F123.ALVIL.J7. A kézi forrásban minden „Seól” „Seol”-ra változott, ragozott és összetett alakban is (17 hely). Az érintett mondatok bájtra-egyezése az archívummal (`archivum/ALVIL-001/Hadesz_Seol_tematikus.md`) ezen a ponton szándékosan megszűnt. A kisbetűs *seól* átírás (a héber szó transzliterációja, nem a magyar szakszó) nem változott. A J7 más fájlt nem érintett. **Kiegészítés (DT-F123k, F123.ALVIL.J17 és J24, ELLENOR_F123_ALVIL-001_2 ELTÉRÉS-2):** a csere kiterjed az `adat/motivumok.tsv` ALVIL-001 `cim` és `ui_cimke` mezőjére („Hádész (Seol)”, „Hádész/Seol”) és az `adat/szotar_szakasz_cimke.tsv` négy H7585-címkéjére (a G0086-címkékben „Seól” nem állt); a DT-F123d NAPLO-jában a felhasználói döntés idézete („kiáltás a Seól szorításából”) idézetként az eredeti „Seól” alakot hordozza. **Kiegészítés (DT-F123m, F123.ALVIL.J32, ELLENOR_F123_ALVIL-001_3 A):** a csere kiterjed az ALVIL-001 lapján megjelenő adatmezőkre is (`elofordulasok.tsv` `kapcsolodas`, a #123 saját 3 jelöltsora a `jeloltek.tsv`-ben), kivéve a szó szerinti idézetet; a `motivum_kapcsolatok.tsv` két, az ISTENTISZT-001 lapján is megjelenő sora kihagyva (lista és indok: `naplok/F123_ALVIL_seol_adat.tsv`).】

## Kivonat

<!-- RÉS-KEZDET: kivonat -->

A motívum lexikai azonosságú: a שְׁאוֹל (*seól*) és a görög ᾍδης (*hádész*) az egyéni halottak birodalmát jelöli — élesen elkülönülve a תְּהוֹם/ἄβυσσος kozmikus-mitológiai fogalomtól —, a teljes Ószövetségben 64 egyedi igehelyen, az Újszövetségben — teljes szövegvizsgálat szerint — tíz ᾍδης-előfordulásban. A legfontosabb lelet Hós 13:14, amelyet Pál explicit idéz/parafrazál 1Kor 15:55-ben ("Halál! hol a te fullánkod?"), és amely a study fő ívét (Krisztus legyőzi a hádészt, Jel 1:18, 20:13-14) egy második, páli hivatkozással erősíti meg. Önálló, ettől elkülönülő második használati minta is azonosítható: a "felmagasztalás→hádészig-taszítás" idióma (Luk 10:15/Mát 11:23), amely nem a halál/feltámadás-tipológiához, hanem a gőg isteni megalázásának mintázatához kapcsolódik.

<!-- RÉS-VÉGE: kivonat -->

<!-- ADAT-NÉZET: 0. Forrás-összegyűjtés a meglévő anyagból (örökölt motívum) | forrás: adat/jeloltek.tsv (forras_kereses), adat/auditok.tsv | cél: general.py --cel lexikon#ALVIL-001#kizart | SZINT: belso -->

## 1. Előfordulások összegyűjtése

<!-- ADAT-NÉZET: 1. pont, 7 oszlopos előfordulás-tábla | forrás: adat/elofordulasok.tsv | cél: general.py --cel study | SZINT: apparatus -->

A fenti egyetlen (Zsolt 16:10) genezisi-ívbeli előforduláson túl a *seól* még **63 egyedi igehelyen** fordul elő az Ószövetségben (a teljes H7585-mező 64 egyedi verset ad; a Hós 13:14-ben és a Zsolt 49:15-ben a szó kétszer szerepel egy versen belül, ez a nyers 66-os számlálást magyarázza: 64 + 2).

【NAPLO: örökölt mondat javítva (ELLENOR_F123_ALVIL-001 E2), F123.ALVIL.J5, 2026-10-29 — a régi mondat csak a Hós 13:14-et nevezte meg (64 + 1 = 65). Lekérdezés: `lekerdez.py scan H7585` → 64 igehely, 66 szó-előfordulás: scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H7585 | n=64 | ts=2026-10-29T12:58Z · `--szakasz "Hós 13:14"` → 1 igehely, 2 szó-előfordulás: scope=range:Hós 13:14 | forras=TAHOT_kivonat.tsv | strong=H7585 | n=1 | ts=2026-10-29T12:58Z · `--szakasz "Zsolt 49:15"` → 1 igehely, 2 szó-előfordulás: scope=range:Zsolt 49:15 | forras=TAHOT_kivonat.tsv | strong=H7585 | n=1 | ts=2026-10-29T12:58Z】

**Összegzés:** a 63 új igehely túlnyomó többsége személyes gyász, lament/könyörgés, bölcsességi figyelmeztetés vagy prófétai ítélet-gúnydal regiszterébe rendeződik — egyik sem mond ellent a study fő ívének (Krisztus legyőzi a Seolt/hádészt), sőt a Hós 13:14 lelet **közvetlenül megerősíti és kibővíti** azt egy második, páli idézettel.

<!-- INAKTÍV: Logikai kötőszó szerinti bontás — nincs adat: az egyetlen igehely-tartományú sor (Jel 20:13-14) bontását a régi tanulmány nem tárgyalta; a hiány nincs kitöltve -->

### Friss, teljes körű keresés (P1–P7)

【NAPLO: F123 M2, 2026-10-29 — a P-lépések nyoma az `adat/auditok.tsv` ALVIL-001-sorai (9 B4-lekérdezés, `naplok/F123_audit_ALVIL-001.py`); a régi tanulmány 2026.09.10-i scanjének leírása az archív példány Q2-jében.】

## 2. Eredeti nyelvi összevetés

<!-- ADAT-NÉZET: 2.S Szótári háttér — szerepmátrix | forrás: adat/lexikon_hivatkozasok.tsv, adat/szotar_szerepek.tsv | cél: general.py --cel lexikon#ALVIL-001#szocikkek | SZINT: apparatus -->

<!-- ADAT-NÉZET: 2/b Kiegészítő szótári adatok | forrás: adat/lexikon_hivatkozasok.tsv | cél: general.py --cel lexikon (2b rés, res_forras forras=adat) | SZINT: apparatus -->

<!-- RÉS-KEZDET: miert_fontos -->
**שְׁאוֹל — *seól*** (héber) és **ᾍδης — *hádész*** (görög, eredetileg az alvilág görög istenének neve, majd a LXX-ban a *seól* rendszeres fordítása). **Fontos megkülönböztetés a tehóm/abüsszosz-komplexumtól:** a seól/hádész **NEM azonos** a tehóm/abüsszosszal. A seól/hádész az **egyéni halottak** birodalma — minden halandó sorsa —, míg a tehóm/abüsszosz **kozmikus-mitológiai** fogalom, a teremtés előtti káosz. A két szócsalád eredetileg élesen elkülönül a héber gondolkodásban, és a Szentírás sosem azonosítja őket egymással.
<!-- RÉS-VÉGE: miert_fontos -->

## 3. A PaRDeS keretrendszer — a motívum egészére alkalmazva

<!-- RÉS-KEZDET: ertelmezes -->
**Peshat.** A hádész-vonal az egyéni halottak helye, ahonnan Krisztus feltámadása kiemeli Őt (ApCsel 2:27, 31, Zsolt 16:10 idézésével), és amelynek kulcsait Ő birtokolja (Jel 1:18), majd amelyet a végén magát a halált is a tűz tavába vetik (Jel 20:13-14). A gazdag ember és Lázár példázatában (Luk 16:23) a hádész a halál utáni, tudatos szenvedés helyeként jelenik meg. A Jelenések könyvében a Halál és a Hádész személyesített párosként lép fel (6:8), amely a végső ítéletben magával a hádésszel együtt semmisül meg (20:13-14).

**Remez.** A minta íve: a halál birodalma, amelybe minden halandó alászáll, de amelyben Krisztus nem maradt (ApCsel 2:31) — ez a győzelem adja az alapot ahhoz, hogy Ő birtokolja "a halál és a hádész kulcsait" (Jel 1:18), és hogy a történelem végén maga a hádész is megsemmisüljön (Jel 20:14) — egyfajta *"végső bezárás"*, amely tartalmilag rokon azzal, ahogyan a tehóm-motívumban a mélység forrásai bezárultak (1Móz 8:2) — de ez **csak tartalmi, nem lexikai** párhuzam a két motívum között.

【NAPLO: DT-F123j, 2026-10-29 (orkesztrátor, a felhasználó felhatalmazásával; ELLENOR_F123_ALVIL-001 E11) — a Remez és a következő („Második hádész-használati mintázat”) bekezdés bájtra az örökölt szöveg, és két jelöletlen következtetést tartalmaz. (1) A Remezben: „ez a győzelem adja az alapot ahhoz, hogy …” — Krisztus hádész fölötti győzelméből (ApCsel 2:31) vezeti le a kulcsok birtoklását (Jel 1:18) és a hádész megsemmisülését (Jel 20:14); az igehelyek egymás mellé állítása adat, a köztük lévő ok-okozati viszony értelmezés. (2) A következő bekezdésben: „tehát nem a jelen tanulmány fő ívéhez … kapcsolódik” — az idióma szerkezeti egyezéséből (Lk 10:15 / Mt 11:23 ~ Ézs 14:9-15) vont besorolás, szintén értelmezés. A szöveg nem változott.】

**Második hádész-használati mintázat — hübrisz és megaláztatás**. Luk 10:15 és párhuzamos helye, Mat 11:23, Jézus szájából ugyanazt a szót (ᾍδης) használja, de nem a halál/feltámadás-tipológia keretében: Kapernaum büszke "égig felmagasztaltatását" állítja szembe az eljövendő "hádészig" való megaláztatással. Ez a "felmagasztalás→Seol/Hádész-taszítás" idióma szerkezetileg megegyezik az Ézs 14:9-15 mintázattal (Babilon királyának bukása) — tehát nem a jelen tanulmány fő ívéhez (Krisztus legyőzi a halált) kapcsolódik, hanem egy **másik, önálló bibliai mintázathoz** (a gőg isteni megalázása). Jelzésre érdemes, de a fő tipológiai ívbe nem illesztendő bele.

**Drash.** A motívum tanítása: a halál — még a maga legfélelmetesebb, birodalom-szerű formájában is — Isten szuverén hatalma alatt áll. Krisztus nem "elkerülte" a hádészt, hanem belépett oda és győztesen távozott, ezért "birtokolja a kulcsait" — vagyis a nyitás-zárás jogát, amely korábban kizárólag Isten közvetlen előjoga volt. Ez a hívő számára azt jelenti, hogy a halál nem autonóm, félelmetes végállomás, hanem egy olyan hely, amely fölött Krisztusnak hatalma van.

**Sod** *(tömör)*. A hádész végső megsemmisítése (Jel 20:14, "a halál és a pokol/hádész pedig vettetének a tüzes tóba") azt a mintát fejezi be, amelyet Krisztus feltámadása nyitott meg: a halál birodalma maga is ideiglenes, Isten végső programjában felszámolandó valóság — nem örök ellenpólusa Isten uralmának, hanem annak alárendelt, végül megszüntetett intézménye.

### Új felismerés — Hós 13:14 → 1Kor 15:55

"Megváltom őket a Seol hatalmából... Hol van a te veszedelmed, oh Seol?" *(összevont saját alak, nem Károli-szöveg; a Károli 1908 alakja: „Megváltom őket a Seol hatalmából! Megmentem őket a haláltól! Hol van a te veszedelmed oh halál?! Hol van a te romlásod oh Seol?!”)* — ezt Pál explicit idézi/parafrazálja **1Kor 15:55**-ben: "Halál! hol a te fullánkod? Pokol! hol a te diadalmad?" A Károli 1908 (Textus Receptus-alapú) szöveg a második tagmondatot "Pokol"-lal (= hádész) adja vissza.

【NAPLO: ELLENOR_F123_ALVIL-001_2 ELTÉRÉS-4, F123.ALVIL.J21, 2026-10-29 — örökölt mondat jelölve: a Hós 13:14 idézőjeles alakja két tagmondat összevonása (a „veszedelmed” a Károliban a halálhoz, a Seolhoz a „romlásod” szól), nem Károli-szöveg; a J7 a Seol írásmódra hozta, ezért jelölés nélkül Károli-idézetnek látszott. A Károli-alak mellette. Lekérdezés: `lekerdez.py karoli "Hós 13:14"` — scope=range:Hós 13:14 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=1 | ts=2026-10-29T13:26Z】

### ↳ Alpont: kiáltás a Seol szorításából

【NAPLO: DT-F123d (2), felhasználó, 2026-10-19 (határdöntés, A4): a „kiáltás a Seól szorításából” az ALVIL-001 ↳ alpontja, nem új ID; a Seol nélküli scan küszöbe a DT-F123e szerint nem teljesült (1 minősített hely < 3, `naplok/F123_adat_ALVIL-001.md` 5c).】

**A motívum határa a halál szorításában kiáltónál.** A Seol nemcsak a halottak helye, hanem a még élőt is szorongató hatalom: „a Seol kötelei körülvettek” (2Sám 22:6 = Zsolt 18:6), „a Seol szorongatásai megragadtak” (Zsolt 116:3), „a Seol gyomrából kiáltottam” (Jón 2:3) — saját, szó szerinti fordítások, a héber *šᵉʾôl* megőrzésével; a Károli 1908 alakja: „A pokol kötelei vettek körül” (2Sám 22:6), „A Seol kötelei vettek körül” (Zsolt 18:6), „a pokol szorongattatásai támadtak meg engem” (Zsolt 116:3), „a Seol torkából sikolték” (Jón 2:3). Ezeken a helyeken a hívó a Seol fenyegetéséből az Úrhoz kiált, és meghallgatást nyer.

【NAPLO: ELLENOR_F123_ALVIL-001 E9, F123.ALVIL.J6, 2026-10-29 — az idézőjeles alakok az `elofordulasok.tsv` `kapcsolodas` mezőjéből jönnek, nem Károli-szövegek; saját fordításként jelölve, a Károli-alak mellettük. Lekérdezés: `lekerdez.py karoli`, a saját proveniencia-sorai szó szerint (újrafuttatva, F123.ALVIL.J20, ELLENOR_F123_ALVIL-001_2 ELTÉRÉS-3) — scope=range:2Sám 22:6 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=0 | ts=2026-10-29T13:26Z · scope=range:Zsolt 18:6 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=0 | ts=2026-10-29T13:26Z · scope=range:Zsolt 116:3 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=2 | ts=2026-10-29T13:26Z · scope=range:Jón 2:3 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=1 | ts=2026-10-29T13:26Z】

- **Minimális jegy:** a Seol a hívót szorongatja, és ő az Úrhoz kiált (meghallgatás). Mindkét elem nélkül a hely nem tartozik ide.
- **Kizárva:** a Seol mint az ellenségek sorsa (Zsolt 55:16; Zsolt 31:18) — ott nem a hívót szorongatja, hanem a hívó kéri, hogy az ellenség jusson oda.
- **A hígulás iránya:** az „ima bajban”. A halálveszélyből Istenhez kiáltó, de a Seolt nem nevező hely (például Zsolt 107:18–19: „a halál kapujához közelgetének … az Úrhoz kiáltának”) ezen a fölérendelt fogalmon keresztül tartozna ide, ezért az alpontból kimarad.
- **Viszony a név segítségül hívásához (ISTENTISZT-001):** a két motívum egyetlen közös helye a Zsolt 116:3–4 (a Seol szorongatása, majd „az Úr nevét hívtam segítségül”); a név nélküli kiáltás nem ISTENTISZT-001-előfordulás.
<!-- RÉS-VÉGE: ertelmezes -->

<!-- INAKTÍV: 4. Kapcsolódás a kutatási sablonhoz — nincs adat: dedikált, kifejezetten erre a lexikai komplexumra (seól/hádész) vonatkozó pünkösdi/karizmatikus szakirodalmi feldolgozás nem áll rendelkezésre elegendő mennyiségben ahhoz, hogy nevesített szerzőkkel idézhető legyen -->

## 5. Alkalmazás és tanítványság

<!-- INAKTÍV: 5.T Nevesített tanítói egyezés — a 7. lépés (B9) az ALVIL-001-re nem futott; a jóváhagyott listáról dedikáltan erre a témára szánt, ellenőrizhető forrás nem állt rendelkezésre; a hiány nincs kitöltve -->

<!-- RÉS-KEZDET: alkalmazas -->

A tanulmány saját megállapításaiból: a halál és a rá adott szellemi-lelki félelem nem végső hatalom a hívő élete fölött — Krisztus, aki "a halál és a hádész kulcsait" tartja, garantálja, hogy a halál sem jelenben (szorongás, gyász), sem véglegesen (a feltámadás reménye) nem az utolsó szó.

<!-- RÉS-VÉGE: alkalmazas -->

## 6. Napló-frissítés

<!-- ADAT-NÉZET: 6. Napló-frissítés (státusz) | forrás: adat/motivumok.tsv (statusz, statusz_verzio, statusz_datum) | cél: general.py --cel naplo | SZINT: belso -->

## 7. Módszertan és nyitott kérdések

<!-- ADAT-NÉZET: 7.K Kereszthivatkozások + Minősítés | forrás: adat/jeloltek.tsv (dontes, indoklas, forras_kereses), TSK/Károli-KH ∩ előfordulások | cél: general.py --cel lexikon (minosites rés, res_forras forras=adat) | SZINT: apparatus -->

<!-- ADAT-NÉZET: 7.A Kapcsolatok + Alátámasztás | forrás: adat/kapcsolatok.tsv (indoklas) | cél: general.py --cel lexikon (alatamasztas rés, res_forras forras=adat) | SZINT: apparatus -->

<!-- RÉS-KEZDET: modszertan -->

<!-- ADAT-NÉZET: 7.M Módszertan — ellenőrzési rétegek | forrás: adat/auditok.tsv | cél: general.py --cel lexikon | SZINT: belso -->

A TR/Byzantinus hagyomány eltérő olvasatáról szóló állítás nem a helyi TAHOT/TAGNT-kivonatból, hanem általános szövegkritikai ismeretből származik, 2026.09.10.

### Nyitott kérdések és séma-korlátok

1. **Mt 16:18** (ᾍδης, „a pokol kapui”, ekkleziológiai kontextus): külön motívumként kezelendő, ha valaha sorra kerül.

<!-- RÉS-VÉGE: modszertan -->

<!-- ADAT-NÉZET: 7.Q Minőségi kapu, verzió-címke | forrás: adat/motivumok.tsv (sablon_verzio), adat/auditok.tsv | cél: general.py --cel lexikon | SZINT: belso -->

## Proveniencia-sorok

【NAPLO: a Kivonat és az 1. szakasz számai (64 ÓSZ-vers, 66 szóelőfordulás, tíz ᾍδης-előfordulás) a ténylegesen lefutott lekérdezésekből, `adat/auditok.tsv` (F123.ALVIL.M2): scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H7585 | n=64 | ts=2026-10-29T10:48Z | csatorna=cli · scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H7585 | n=66 (igealak) | ts=2026-10-29T10:48Z | csatorna=cli · scope=TAGNT-teljes | forras=TAGNT_kivonat.tsv | strong=G0086 | n=10 | ts=2026-10-29T10:48Z | csatorna=cli】
