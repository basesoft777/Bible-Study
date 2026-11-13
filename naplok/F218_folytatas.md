# F218a — folytatási fájl

*Kézi munkanapló (a brief 9. pontja szerint minden commitban frissül). Ebből indul a következő session; a régi generátorból visszafejtett mondatszabályok is itt állnak.*

Ág: `claude/f218-generator-uj-a` · PR: #729 (vázlat) · Brief: `F218_GENERATOR_UJ_A_BRIEF.md` · Alap: main `37f087cc`.

## Állás

| Tétel | Állapot | Megjegyzés |
|---|---|---|
| F218.0 | kész | modell-ellenőrzés, függések, keretmérés |
| F218.1 | kész, két halasztott résszel | referencia (bájtra azonos, 46,5 s), szimbólumtérkép, bemenet-hashek, alapmérés: `naplok/F218_jelentes.md`. **Halasztva:** a leltár `kovetelmeny` oszlopa (brief 7.4; a heti keret nullázása után, sonnet); az alias-sorok (GK-17) az S5 előttre |
| F218.2 (T) | kész | típusok és szerződések; GK-01, 02, 05, 08a–c, 12, 23, 29, 30 zöld |
| F218.4 (S1) | **kész: a szakasz-diff 0 az engedélyeken kívül** | „2. Előfordulások” + „2.1”: 437 sorból 432 bájtra egyezik, 5 engedélysor; festékpróba 0 szivárgás. Az S1 tesztjei (`teszt_elofordulas.py`): GK-13, GK-14, GK-17, GK-25, HN-01, HN-16, a sablonmódosítók, a jegyzet-összevonás |
| F218.3 | kész | tesztváz (`teszt_vaz.py`): 35 követelmény név + docstring + `skip` alakban, a szelet megnevezésével; a HN-03 a felhasználó döntésére vár; a mutációs próba (GK-26) az S9-ben. A tesztek állása: 121 teszt, 86 zöld, 35 kihagyva |
| ⛔ az S1 után | **ELTÉRÉS (11 tétel)**; megállt | 1. független ellenőrzés (`fuggetlen-ellenor`, opus) és a felhasználó első átnézése: a lista a `naplok/F218_jelentes.md` „Amit a felhasználónak látnia kell az S1 után” pontja |
| F218.5 (S2) | nem indult | 1. Döntési út + KIZARASOK |
| F218.6–F218.13 | nem indult | |

## Az 1. független ellenőrzés után: ELTÉRÉS, 11 tétel

A jelentés változtatás nélkül: `naplok/F218_jelentes.md` „Független ellenőrzés — 1. ellenőrzés”. A javítókör külön sessionben fut (`/elteres 218`; a brief szerint egy javítókör jár). Az alábbi besorolás az építő session javaslata, nem döntés.

| # | Eltérés | Javasolt besorolás | Teendő |
|---|---|---|---|
| 1 | T3 (DT837) tárolása külön táblában, felhasználói megerősítés nélkül | döntés (a felhasználóé) | az orkesztrátor viszi a felhasználóhoz: külön tábla (DT-F218i) vagy az `elofordulasok.tsv` oszlopa; a megerősítésig a DT-F218i állapota nem ✅ |
| 2 | Az idézetbe mosás csatornája: a `gerinc.jel_szoveg` és az `idezet_szoveg` a számításból kapott szöveget burkolja; a B16–B22 nyers sorai festetlenül jutnak a számításba | mechanikus | a szakaszjel két alakja (cella, próza) és a példahely mezői a `bemenet/gerinc.py`-ban, betöltéskor kapjanak burkolót (a jel a kulcsból a bemeneti rétegen belül képződjön); a számítás típusos példahely-objektumot kapjon, nyers szótársort ne; a két általános burkoló metódus megszűnik; a festékpróba ezután a szótári ágat is fedi |
| 3 | A `cella` módosító prózát és idézetet ír át, szemben a 6-os sablon új szabályával („változatlanul”) | döntés + tervezés | két út: (a) a szabály szövege kimondott kivételt kap a cellakezdő alakra (tipográfiai átalakítás a sablon-konstruktorban, teszttel), a felhasználó jóváhagyásával; (b) a címkék cellakezdő alakja adatba kerül (a címketábla javítása), és a módosító csak sablonszövegre hat. Ugyanide tartozik az önreferencia („a lap”) kezelése: a kettő legyen következetes |
| 4 | A bemenet-hash őr nem veti össze az olvasási naplót a referencia-táblával; a B67 és a `dontesek/uj/*.md` nincs a táblában | mechanikus | a `regresszio.py` kapja meg az új generátor olvasási naplóját (a `fo.lap_keszit` eredményéből vagy a kimenet mellé írt naplófájlból), és bukjon, ha olvasott bemenet nincs a `F218_referencia.tsv`-ben; a tábla bővítése az új generátor bemeneteivel (külön commit, okkal) |
| 5 | Az S1-ONREF osztály előzetes darabszám nélkül, látható visszalépéssel; a T4 osztály 3 a rögzített 2 helyett | döntés (a felhasználóé) | a jelentés „Amit a felhasználónak látnia kell az S1 után” 1. és 2. pontja; a döntés után az engedélysorok igazítása |
| 6 | Az S1 hatóköréből halasztott tételek: HN-03, GK-13 (lemma), GK-14 (összevont versek), GK-03 (B18/B19/B21), 7.4, alias-sorok | részben döntés, részben mechanikus | a halasztást az orkesztrátor hagyja jóvá, vagy a javítókör pótolja; a GK-03 frissességi kapu a B18/B19/B21-re pótolható az S1-ben is |
| 7 | Tesztváz: hiányzik a GK-B9, a HN-szövegminták és a leltárleírások | mechanikus | GK-B9 a vázba (a tartalmát a `test_gk29_…` már méri); a HN-esetekhez lapszöveg-részlet mint tesztadat; a cím nélküli tételek leírása a 7.4 után |
| 8 | `general.py:1925`: az előjavító (E32) egy régi üzenetből törölte a „; DT-F09h” részt; a jelentés „additív”-nak mondja | mechanikus | a jelentés mondatának pontosítása (additív módosítás és egy E32-előjavítás); a régi generátor kimenete ettől bájtra azonos maradt |
| 9 | GK-07: `-` elem a blokkfejléc forráslistájában (a B13 szabálymodul útvonala) | mechanikus | a `fo._forrasok` a nem fájl-bemenetet hagyja ki (vagy a modul nevét írja); utána az S1-FORRAS engedélysor hash-e frissül |
| 10 | A 10 sornál nagyobb új táblákhoz nincs bontási napló | mechanikus | a három tábla sorainak bontása a jelentésbe (sablon: `eredet` szerint; névtábla: típus szerint; jegyzék: szeletenként) |
| 11 | A T4-táblázat „melyik felel meg a Károli-szónak” oszlopa jelöletlen értelmezés | mechanikus | értelmezésként jelölni, vagy a Károli–Strong párosítás lekérdezésével alátámasztani, proveniencia-sorral |

**A lassú tesztek.** Az ellenőr `teszt_futtat.py --diff` futása a `teszt_visszhang_kapu.py`-ban 2 bukást adott (a régi generátor 4.11 blokkja). A fő checkout (`1352ac3c`, a main egy korábbi állapota) ugyanezzel a 2 bukással áll (`python eszkozok/teszt_futtat.py --fajl teszt_visszhang_kapu`: 22 teszt, 2 bukás), tehát a hiba nem ebből a diffből jön. A `teszt_szintek.py` hibáját nem vizsgáltam.
*Proveniencia: `scope=python eszkozok/teszt_futtat.py --fajl teszt_visszhang_kapu | forras=1352ac3c (a fő checkout) | ts=2026-11-13`.*

## Következő lépés

**Az S2-t friss Fable-session kezdi ebből a fájlból** (az orkesztrátor döntése, 2026-11-13: szeletenként új session; az S2 effortja még xhigh, azt az orkesztrátor állítja be). Az első lépése a modell-ellenőrzés, a második a `get_usage`.

1. **A ⛔ lezárása az S1 után.** Az 1. független ellenőrzés (`fuggetlen-ellenor`, opus) jelentése a `naplok/F218_jelentes.md` „Független ellenőrzés — 1. ellenőrzés” szakaszában áll (ha ez a szakasz hiányzik, az ellenőrzés még nem zárult le: a bemenete a brief, a `37f087cc..dfb4525a` tartomány, a szint `teljes`). `ELTÉRÉS` esetén egy javítókör jár. A felhasználó első átnézése az orkesztrátoron át megy: a lista a jelentés „Amit a felhasználónak látnia kell az S1 után” pontja (T4, önreferencia, 8 új sablonmondat). Az S2 ezekre nem vár, de a T4 döntése a kiejtés-szolgáltatást (`bemenet/szavak.py`, `Kiejtes.ragozott`) és három engedélysort érint.
2. **F218.5 (S2): „1. Döntési út” (1.1–1.5) és a `_KIZARASOK.md` melléklet.** Követelmények: GK-04 (teljesség minden hálóra: strong, karoli, szotar; melléklet-kapu), GK-09 (számegyezés a modellen), GK-21 (a Döntési út számai összeadódnak; döntés nélküli vers 0), HN-11 (a teljesség-mérés pillanatképe frissességi kapuval), GK-03 (B05, B06), GK-06.

### Az S2 terve

- **A mérce:** a referencia `## 1. Döntési út` szakasza (108–218. sor, 110 sor) és a teljes `HAMART-001_KIZARASOK.md` (431 sor). A melléklet a régi generátorban **nem megy át** az olvasói átíráson (csak az önreferencia-csere fut rajta), ezért várhatóan könnyebb; érdemes vele kezdeni. A Döntési út blokkja viszont a teljes utófeldolgozó láncon átmegy (olvasói átírás, névelő-levétel, könyvnév, idézőjel), a `<details>`/`<p>` HTML kivételével.
- **Első lépés: a lánc mérése.** A `lanc_meres.py` a régi generátor utófeldolgozó függvényeit burkolja, és minden lépés kimenetét fájlba menti; a `lanc_diff.py <könyvtár> dontesi_ut 330 6` megmutatja, melyik lépés mit változtat a blokkon. Így a mondatok szerkezetből írhatók meg, nem a cserék visszafejtéséből. A szkriptek a megosztott jegyzetmappában állnak: `side-session-notes/local_c8cc3610-84cb-4dc5-a316-803281316097/F218_eszkozok/` (a `lanc_meres.py`-ban a nyers blokk mentését a `blokk_dontesi_ut` függvényre kell átírni; a `nyers_blokk.py` ugyanezt adja befagyasztott motívumra is).
- **A régi kód helye** (a jelentés szimbólumtérképe, 2/a (ii); szimbólum szerint keresni): `blokk_dontesi_ut` (7648), `dontesi_ut_adat` (7434), `teljesseg_halok` (7377), `teljesseg_kapu` (7558), `kizarasok_melleklet` (7577), `kizarasok_adat` (7492, `MellekletHiba`), `_modszertan_nyitott` (7625); a `szerep_kizart.py`-ból: `okok`, `ok_megjegyzesek`, `csoport_versszam`, `jeloles_oka`, `elutasitas_oka`, `olvasoi_ok`, `versek`; a `nyilt_mag_export.py`-ból a `csoport_tagjai` (újraírandó a `szamitas/`-ban, a régi modul érintetlen marad).
- **Új bemenetek** (sor a jegyzékbe a függvénnyel együtt): B02 (`adat/motivumok.tsv`: negatív kritérium, fölérendelt fogalom, cím), B04 (`adat/jeloltek.tsv`; a csoportos kizárás versszáma **nem** a `forras_kereses` szövegéből, hanem a B06 mérésből, M13), B05 (`naplok/F123_teljesseg_<ID>.tsv`) és B06 (`…_blokkok.tsv`): pillanatképek, frissességi kapuval a mai Strong-halmazra; hiányuk kimondott hiány vagy BUKÁS a `kotelezo` szerint, B56 (`adat/elutasitasi_okok.tsv`), B47 (a motívum kézi forrása, `motivumok/<ID>.md`: az 1.5 nyitott kérdései rés-prózaként), B10 (TBESG/TBESH lemma és rövid glossza az 1.2-höz: ez a pontozatlan héber alak szótári kiejtését is megadja, amely az S1-ben kimondott hibával áll meg).
- **Kapuk a modellen:** a régi `teljesseg_kapu` és a `MellekletHiba` a kiírt szövegen, illetve összeadáson fut; az újban a `szamitas/` adjon kapufüggvényt a szakasz modelljére (a számok összeadódnak; a `strong`, a `karoli` és a `szotar` háló is mérve van; a melléklet taglistája egyezik a csoportszámmal), és a `fo.lap_keszit` a megjelenítés előtt futtassa. A `SzakaszLeiro` ehhez kapu-mezőt kap.
- **Két nézet:** a `KIZARASOK` nézet a szakaszrendben `kizarasok_melleklet` néven már szerepel; a `fo.lap_keszit` nézetenként ír. A regresszió a melléklet fájlját is méri (ott a szakasz a 2. szintű címsor; ha a mellékletben nincs ilyen, az egész fájl „(a lap eleje)”: ilyenkor a `regresszio.py` részleges módja ezt a szakaszt kihagyja, ezért a melléklethez `--teljes` vagy a szakaszolás finomítása kell).
- **Sablonmondatok:** az `e2.*` mintájára `d1.*` (Döntési út) és `kz.*` (melléklet) kulcsok; a betűre átvett mondat `eredet` mezője a régi szimbólum, az új mondaté `uj`, `dontes=var`. Táblasort magyar szöveggel csak fájlba írt szkripttel lehet hozzáadni (`tabla_bovit.py <repó> <sorfájl.py>`).
- **A szelet vége:** szakasz-diff 0 az engedélyeken kívül mindkét nézetre; az ISTENTISZT ugyanazon szakasza belső szöveg nélkül; festékpróba 0; tesztek zöldek; commit(ok) `F218.5: …`; `push_elott.py`; push; a folytatási fájl frissítve.

### A felhasználó megállási küszöbe

A felhasználó (az orkesztrátoron át, 2026-11-13, szó szerint): „megállási köszüb 96% legyen”. Minden commit előtt `get_usage`. Ha a heti keret („Weekly · all models”) eléri a 96%-ot: az épp futó lépés zöld állapotban lezárul (commit, folytatási fájl, push), megállás, a pontos százalék jelzése az orkesztrátornak. Új szelet 96% fölött nem indul. Ez a brief megállási szabálya mellett érvényes.

## Hogyan futtatható

- Tesztek: `python eszkozok/lapgen/tesztek/futtat.py` (minden), `… futtat.py szoveg szerkezet` (megnevezett fájlok).
- Új lap: `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon2 --id HAMART-001 --kimenet <repón kívüli könyvtár>`; a fájlok a `<kimenet>/lexikon/` alá kerülnek.
- Regresszió: `python eszkozok/lapgen/regresszio.py --id HAMART-001 --uj <kimenet>/lexikon --reszletes <fájl>`.
- Festékpróba: `python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001`.
- A régi generátor egyezése: `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon --id HAMART-001 --kimenet <ideiglenes>`, majd `cmp` a `git show HEAD:lexikon/HAMART-001_TUDOMANYOS.md` tartalmával (a munkafa CRLF-es, a blob LF-es).
- Push előtt: `python eszkozok/push_elott.py --pr-cim "F218: a lapgenerátor újraírása, 1. rész — építés a regresszióig"` (kb. 7 perc, a háttérben), csak 0 HIBA-val.
- Táblasor hozzáadása: magyar szöveget tartalmazó kódot heredocból futtatni tilos (és el is romlik); a sorokat Python-fájlba kell írni, és úgy futtatni.

## Tervezési döntések

- **Három konstruktor:** `proza(kezi)`, `sablon(sor, **p)`, `idezet(forrasszoveg)`. Az `idezet` egyetlen argumentumot kap: a forrást (B-azonosító) és a helyet maga a `Forrasszoveg` érték hordozza (a brief `idezet(forras, hely, szoveg)` alakjának szigorítása).
- **A `Lathato` nem `str`:** nincs rajta szövegművelet, `str()`/formázás kivételt dob; szöveggé csak a `kiiras()` alakítja, amelyet csak a `megjelenites/md/iro.py` hív (statikus teszt).
- **Burkolók a bemeneti rétegből:** `Kezi` → `proza`; `Forrasszoveg` → `idezet`; `Belso`, `Kulcs`, `Utvonal` → csak `Proveniencia` vagy (kulcsnál) névtábla. A burkolót csak a `bemenet/` hozhatja létre.
- **Nyilvános azonosító-típusok** (a brief felsorolásán túl): `Strong`, `MotivumId`, `Horgony` az `Igehely` mellett; szigorú alakjuk miatt megjeleníthetők.
- **Sablonmondat:** `{nev}`; skalárnál `{nev|a}` / `{nev|A}` névelőt tesz elé (a/az; számnál a kiejtés szerint), `{nev|a:masik}` a névelőt a megnevezett másik paraméter szövege szerint választja (pl. a görög szó kiejtése), `{nev|cella}` a cellakezdő alak (l. lent); listánál `{elemek|; }`, illetve `{elemek|, | és }`. A mondatban Markdown-jelölés állhat. A megjelenítő saját literálja csak szerkezeti jelölés (`Jel`, zárt készlet az író modulban).
- **Fajta-térkép:** az író minden kiírt sorhoz tartományokat ad (próza / sablon / idézet / megjegyzés / jelölés); ezt használja a festékpróba, és ezt fogja használni az alakosztály-kapu (GK-24).
- **Festés:** a burkoló `szoveg` alakja festett futásban jelzőszót hordoz (`ZZQ<B-azonosító>_<mező>ZZ`); az `ertek` változatlan. Belső jelzőszó csak megjegyzésben állhat, kézi csak prózában, idézeté csak idézetben.
- **Blokkjelölő:** a lapon `general.py --cel lexikon#…` áll (a termék célneve), nem `lexikon2`.
- **Hash:** sorvég-normalizált tartalomból (`\r\n` → `\n`), a bemeneti rétegben és a regresszióban is.
- **`ts=`:** `PARDES_DATUM`-ból vagy a `--datum` paraméterből; nélkülük `ts=b:<12 jegy>` az olvasási napló hash-éből.
- **Jegyzék:** a sor a bemeneti függvénnyel együtt kerül a táblába (statikus teszt: sor ↔ `b<nn>_…` függvény, egy az egyhez). Több fájlos bemenetnél az `utvonal` `;`-vel sorol fel; nem fájl-bemenet (szabálymodul) útvonala `-`.
- **Regresszió:** szakasz = 2. szintű címsor; soronkénti diff; az engedélyfájl `regi`/`uj` oszlopa `sor` kötésnél a sor sha256-ának első 16 jegye. Részleges lapnál a még nem kész szakasz „nincs kész”, és az engedélysora nem számít.
- **A megjegyzések is bájtra egyeznek:** a régi lap `<!-- eredeti: … -->` megjegyzéseit az új generátor `Proveniencia`-ként, ugyanabból a szerkezetből állítja elő, mint a látható mondatot (két párhuzamos megjelenítés, nem egymásból képzett szöveg).
- **A szótári gerinc megosztása:** a forrás szerkezetének feloldása (melyik példahely melyik szócikké, szakaszjel, címke, glossza) a `bemenet/gerinc.py`; a döntés (melyik címke áll a soron, és miért) a `szamitas/szotari_gerinc.py`, szerkezetként (`Indok` fajtával); a mondat a megjelenítőben, a sablontáblából.
- **Újrahasznosított régi segédmodulok** (tiszta függvények, az útvonalat a jegyzékből kapják): `heber_kiejtes`, `kiejtes`, `bdb_tagolas`, `bdb_rovidites`, `szotari_glossza`. A `lexikon_general.py`-ból az új kód semmit nem importál.
- **T3:** a tematikus hely saját szava külön kézi táblában (`adat/tematikus_sajat_szo.tsv`, B67, SEMA 2.63; DT-F218i), nem az `elofordulasok.tsv` új oszlopában.

## A régi generátorból visszafejtett szabályok (S1)

- **Lánc.** A régi lap nyers blokkokból épül, majd tíz utófeldolgozó lépés írja át (címcsere → olvasói átírás → névelő-levétel → kiejtés-pótlás → Strong/BDB/könyvnév/idézőjel → lábjegyzet a tábla alá → közös forrásmegjelölés → önreferencia-csere). A lánc táblája: `naplok/F218_jelentes.md` „F218.1 — szimbólumtérkép”. A közbenső állapotok mérésére a régi generátor függvényei burkolhatók (repón kívüli szkripttel), így látszik, melyik lépés mit változtat egy szakaszon.
- **Cellakezdet (`nevelo_le`).** Minden tábla- és listaelem: ha kisbetűs „a ”/„az ” névelővel kezdődik, és utána hatnál kevesebb szó áll, a névelő elmarad, és az elem nagy kezdőbetűt kap („a szócikk egésze — fájdalom” → „Szócikk egésze — fájdalom”); hat vagy több szónál a névelő marad, nagy kezdőbetűvel („a megművelt föld, amely táplál · 1” → „A megművelt…”). A szószám a cella egészére értendő (a szakaszjel és a „·” is szó). Az új generátorban ez a `cella` sablonmódosító; minden táblacella a `tabla.cella` sablonon megy át.
- **Kulcsszó-cella.** `Károli-szó — alak (kiejtés)`; több Strongnál az alakok „; ”-vel. Héberül a teljes szó (előtag + tő + toldalék a szöveg soraiból, `heber_kiejtes.teljes_szo`) és a gépi kiejtése; görögül a ragozott alak és a magyaros átírása. A záró írásjel (`,.;·`) lemarad az alakról. A régi az utolsó előfordulást vette (a szótárindex felülírása miatt), az új a T4 szerint az elsőt.
- **Jelentés-cella.** Címkével: `címke · jel`; címke nélkül, BDB-jellel: `a szakasz olvasói glosszája · jel`; jel nélküli héber szónál, ha a szócikk tagolatlan: `a szócikk egésze — a fej glosszája`; különben `*(nincs címke: jel)*`, illetve `*(nincs hozzárendelés)*`. Több szónál `H…: …; H…: …`. A nem BDB-jel a szótár nevével áll („Thayer 1”, „Thayer fej”).
- **A címke elsőbbsége.** Ha a BDB maga idézi a verset, és az útja a szerkesztői hozzárendelés alá esik, a finomabb út címkéje áll; ha a szerkesztői út esik a példa alá, a szerkesztői; ha egyik sem, a futás megáll. Ha a Strong többször áll a versben, a versszintű BDB-példa nem kerül a szóra. Több útvonalú példánál a szerkesztői hozzárendelés dönt, ha pontosan egy esik alá.
- **Jegyzet (egyszavas sor).** `Igazolás; a jelentés: indok.` Az igazolás: „A héber szöveg (TAHOT) igazolja” / „Újszövetségi hely: a szó a görög szövegben áll” (hatókörön kívül, újszövetségi sor) / „A héber szöveg-igazolás itt nem alkalmazható” / „Szövegigazolás nélkül”. Az indok az első indok fajtája szerint: BDB-példa → „a BDB a(z) X szakaszban maga idézi a helyet” (a puszta szám ponttal: „az 1.”); más szakaszban is → „a BDB a helyet a(z) X is idézi”; szerkesztői hozzárendelés → „a BDB X szakasza” / „a Thayer szócikkfeje”; tagolatlan → „a szócikk egésze (a szótár nem tagolja számozott jelentésekre)”. A tematikus sor jegyzete egyetlen mondat, igazolás nélkül.
- **Jegyzet (többszavas, szópáros sor).** Mondatonként: az igazolás, majd szavanként `H…: rövid mondat` (a cella tartalmát nem ismétli); a „nincs hozzárendelés” szóról nem szól mondat.
- **Összevonás.** Az azonos látható mondatú jegyzet egyszer áll; a szám az első hivatkozás sorrendje; a sor jelentés- és megbízhatóság-cellája is hivatkozik rá (a tematikus sornál csak az utóbbi). Az összevont sor végén minden eredeti lábjegyzet `<!-- eredeti: [^n]: proveniencia: … | igazolas: … | jelentés-címke: … -->` megjegyzésként áll.
- **Közös forrásmegjelölés.** A legalább két jegyzetben álló `scope=… | forras=… | ts=…` hármas jelet kap (‹E1›, ‹E2› …, gyakoriság, majd szöveg szerint); a tábla alatt egy megjegyzéspár áll: `<!-- közös forrásmegjelölés: … -->` (olvasói alak: „forrás: kézi szerkesztés, dátum”) és `<!-- eredeti: … -->`.
- **UBS-cella.** Újszövetségi sor: a görög UBS-szótár versre hivatkozott jelentései, `glossza [ⓘ](/szo/Strong)`, több jelentésnél vagy tartománynál `*(lehetséges, nem egyértelmű)*`. Ószövetségi sor: a héber UBS-szótár a Károli-vers masszoréta megfelelőjén; eltérő versnél `*(MT: vers)*`. A glossza a fordítástáblából (`glosszak_hu`), híján az angol `*(fordításra vár)*` jelöléssel.
- **Önreferencia-csere.** A régi kód nyolc rögzített szövegpárral cserélte a „lap” szót (`tablajegyzet.ONREF_CSERE`), adatcellákban is; az új generátor prózát nem ír át (l. „Nyitott kérdések”).

## Nyitott kérdések (a felhasználóhoz, illetve az orkesztrátorhoz)

- **T4:** az „első előfordulás” a mért sorok többségén nem a sor Károli-szavának megfelelő alakot adja (táblázat a jelentésben). Javaslat: a Károli–Strong párosítás szerinti előfordulás, és csak annak híján az első.
- **Önreferencia a kézi prózában:** adatcella javítása vagy prózajavító tábla; addig az S1-ONREF engedélysor áll.
- **Új sablonmondatok jóváhagyása:** 8 sor (`dontes=var` a sablontáblában).
- **A T3 szócikke:** az orkesztrátor üzenete szerint a saját szó „a 4. szakaszban szócikket kap”, a brief 12. pontja (T3) és a DT837 szerint „szócikk nélkül”. A generátor a brief szerint készül (nem kap szócikket), megerősítésig.
- **Alias-sorok (GK-17, B63):** a normalizáló tábla 4. oszlopát több eszköz olvassa; döntés az S5 előtt kell.
- **A CI nem futtatja a `lapgen/tesztek`-et:** a bekötés a 218c N-tételébe kerül.
- **Függések:** a `feladatok.py fuggesek` a 194 és a 212 tétellel is `KIZAR` sort ad (l. a jelentés F218.0 szakaszát).

## Megállási küszöb

Az S1 szakasz-diffje a heti keret 89%-ánál lett 0 (az engedélyeken kívül); a küszöb 91,5% volt. A megállási szabály első feltétele teljesült. A T4 osztály tényleges száma (3) az előre rögzítettől (2) 20%-nál jobban eltér: az ok a mérés hatóköre (csak a héber szöveg), a jelentés kimondja; a ⛔ megállás az S1 után amúgy is esedékes.

## Mérőszámok

| Pont | Dátum (UTC) | Heti · minden modell | Heti · Fable | 5 órás | Megjegyzés |
|---|---|---|---|---|---|
| F218.0 (indulás) | 2026-11-13 09:05 | 83% | 15% | 19% | `get_usage`; nullázás: 2026-11-14 14:00 UTC |
| F218.2 után | 2026-11-13 09:35 | 85% | 20% | 38% | az F218.1 (sonnet) és az F218.2 együtt 2 százalékpont |
| S1 első fele után | 2026-11-13 09:55 | 87% | 22% | 48% | a régi kód olvasása és a 2.1 pont: 2 százalékpont |
| S1 diff 0 | 2026-11-13 10:35 | 89% | 27% | 66% | a tábla, a jelentés-oszlop és a jegyzetek: 2 százalékpont |
| S1 tesztek, push | 2026-11-13 11:00 | 90% | 28% | 71% | a tesztek és a tesztváz: 1 százalékpont; a kontextus 80% |

Diff-görbe (engedélyen kívüli diff-sorok, commitonként):

| Commit | 2. Előfordulások (437 sor) | Megjegyzés |
|---|---|---|
| F218.4 (1) | 76 | az összegző mondat, a hatókör-sor és a 2.1 pont egyezik |
| F218.4 (2) | 0 (5 engedélysor) | a tábla, a 17 jegyzet, a közös forrásmegjelölés, az UBS-magyarázat |

Festékpróba: HAMART-001 0 szivárgás (belső 137, idézet 326, kézi 180 látott jelzőszó); ISTENTISZT-001 0 (86, 180, 85). Mutációs próba: még nincs. Átszökési arány: még nincs mérés (az 1. ellenőrzés és a felhasználó átnézése után).

## Session-váltások, kompaktálások

- 1. session (2026-11-13): az indulás `claude-opus-5-5` modellen modell-eltérés miatt megállt; a felhasználó a sessiont `claude-fable-5-2`-re állította. Egy megszakadás (hitelesítési hiba) az S1 közben, adatvesztés nélkül. Kompaktálás eddig: 0; a kontextus az S1 végén 76%.
