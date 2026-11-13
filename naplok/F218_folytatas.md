# F218a — folytatási fájl

*Kézi munkanapló (a brief 9. pontja szerint minden commitban frissül). Ebből indul a következő session; a régi generátorból visszafejtett mondatszabályok is itt állnak.*

Ág: `claude/f218-generator-uj-a` · PR: #729 (vázlat) · Brief: `F218_GENERATOR_UJ_A_BRIEF.md` · Alap: main `37f087cc`.

## Állás

| Tétel | Állapot | Megjegyzés |
|---|---|---|
| F218.0 | kész | modell-ellenőrzés, függések, keretmérés |
| F218.1 | kész, két halasztott résszel | referencia (bájtra azonos, 46,5 s), szimbólumtérkép, bemenet-hashek, alapmérés: `naplok/F218_jelentes.md`. **Halasztva:** a leltár `kovetelmeny` oszlopa (brief 7.4; a heti keret nullázása után, sonnet); az alias-sorok (GK-17) az S5 előttre |
| F218.2 (T) | kész | típusok és szerződések; GK-01, 02, 05, 08a–c, 12, 23, 29, 30 zöld |
| F218.4 (S1) | **a szakasz-diff 0 az engedélyeken kívül** | „2. Előfordulások” + „2.1”: 437 sorból 432 bájtra egyezik, 5 engedélysor; festékpróba 0 szivárgás; 69 teszt zöld. Hátra van: az S1 saját tesztjei (GK-13, 14, 17, 25, HN-01, HN-03, HN-16, a mutációs próba váza) |
| F218.3 | következik | tesztváz (`skip`) a 7. pont még meg nem írt követelményeire |
| ⛔ az S1 után | következik | 1. független ellenőrzés (`fuggetlen-ellenor`, opus) és a felhasználó első átnézése: a lista a `naplok/F218_jelentes.md` „Amit a felhasználónak látnia kell az S1 után” pontja |
| F218.5 (S2) | nem indult | 1. Döntési út + KIZARASOK |
| F218.6–F218.13 | nem indult | |

## Következő lépés

1. Az S1 tesztjei a `lapgen/tesztek/`-ben: GK-13 (egy kiejtési út: H2403a/b, H2398, H7121), GK-14 (T4: az első előfordulás, nevesített szabály), GK-17 (0 kódba írt könyvnév-alias), GK-25 (pozitív szerkezeti kapu: minden igehely alatt teljes mondat + „Funkció:”; a jegyzet a tábla alatt, rövid, egysoros, a cellát nem ismétli), HN-01, HN-03, HN-16 (szövegminták), a mutációs próba váza (GK-26), és a `cella` módosító, az összevont jegyzet, a közös forrásmegjelölés egységtesztjei.
2. F218.3: `teszt_vaz.py` a hátralévő követelményekre (név + docstring + `skip`).
3. ⛔: `fuggetlen-ellenor` (bemenet: a brief, `37f087cc..HEAD`, szint `teljes`, a CI-állapot a head-re); a jelentése változtatás nélkül a `naplok/F218_jelentes.md`-be, külön commitban. Egy javítókör. Ugyanekkor megy a felhasználónak az S1 listája (T4, önreferencia, új sablonmondatok).
4. F218.5 (S2): „1. Döntési út” és a KIZARASOK-melléklet. A régi kód helye: a jelentés szimbólumtérképe, 2/a (ii). Új bemenetek: B02 (motívumok), B04 (jelöltek), B05/B06 (teljesség-mérés, frissességi kapuval), B56 (elutasítási okok), B47 (a kézi forrás rései).

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

Diff-görbe (engedélyen kívüli diff-sorok, commitonként):

| Commit | 2. Előfordulások (437 sor) | Megjegyzés |
|---|---|---|
| F218.4 (1) | 76 | az összegző mondat, a hatókör-sor és a 2.1 pont egyezik |
| F218.4 (2) | 0 (5 engedélysor) | a tábla, a 17 jegyzet, a közös forrásmegjelölés, az UBS-magyarázat |

Festékpróba: HAMART-001 0 szivárgás (belső 137, idézet 326, kézi 180 látott jelzőszó); ISTENTISZT-001 0 (86, 180, 85). Mutációs próba: még nincs. Átszökési arány: még nincs mérés (az 1. ellenőrzés és a felhasználó átnézése után).

## Session-váltások, kompaktálások

- 1. session (2026-11-13): az indulás `claude-opus-5-5` modellen modell-eltérés miatt megállt; a felhasználó a sessiont `claude-fable-5-2`-re állította. Egy megszakadás (hitelesítési hiba) az S1 közben, adatvesztés nélkül. Kompaktálás eddig: 0; a kontextus az S1 végén 76%.
