# F188 — A menetek könyvelési és ellenőrzési terhének csökkentése (TEHER_CSOKKENTES): jelentés

*Brief: `F188_TEHER_CSOKKENTES_BRIEF.md` · végrehajtó: `claude-opus-5-5` (a modell-ellenőrzés egyezett a brief `modell: opus` mezőjével) · 2026-11-10*

Két ág készült (DT-F188a). Az A ág, `claude/f188-t0-t3`, két új fájlt hoz tesztekkel, és nem élesít semmit. A B ág, `claude/f188-teher-csokkentes`, az A ág tetejére épül, ezért az A merge-e után a B diffje magától szűkül.

## T0 — mérés-alap

**Szkript:** `eszkozok/ellenorzes/teher_meres.py`. Hívás: `--pr <n…>` vagy `--utolso N`. A kimenet TSV, összesítés a célokkal és proveniencia-sor. A mezők meghatározása és korlátai a docstringben állnak:

- **Admin és tartalmi fájl:** a brief admin-meghatározása szerint.
- **Javítókör:** három jelből a legnagyobb:
  - az ELLENOR-fájl sorszáma − 1;
  - a `[elteres_kor k/K]` vagy „javítókör k/K” jelölő;
  - a `<tétel>: ellenőri jelentés` című commitok száma − 1.
- **Ellenőri idő:** az ELLENOR-fájlt létrehozó (vagy „ellenőri jelentés” című) commit és az előző commit közötti idő, a szerzői időbélyegből számolva.
  - A committer-dátum nem használható: a rebase átírja. A #664-ben hat commit egy másodpercre esett.
  - A mérték becslés, két irányban is torzíthat. Túlbecsül, mert benne van a mentés és a menet esetleges állása. Alulbecsül, ha a session az ellenőr futása közben commitolt.
- **CI:** az `ellenorzes` workflow futásai a PR ágán. A futás ideje `updatedAt − createdAt`, a sorban állással együtt.
- **Hibakezelés:** hálózati vagy git-hibánál a mező értéke „nem mért”, sosem üres.

**Kiindulás:** a #664, #665, #666, #668, és a legutóbbi 10 mergelt PR (átfedéssel: 10 PR).

| PR | tétel | commit (merge) | admin | tartalmi | javítókör (jel) | CI-javítás | ellenőr-futás | ellenőri perc | CI-futás (bukott) | CI perc átlag / össz. |
|---|---|---|---|---|---|---|---|---|---|---|
| #663 | F184 | 2 (1) | 1 | 0 | 0 | 0 | 0 | nem mérhető | 2 (0) | 2,2 / 4,4 |
| #664 | F102 | 26 (1) | 14 | 8 | 2 (ELLENOR-fájl, ellenőr-commit) | 0 | 3 | 12; 5; 5 | 3 (0) | 6,0 / 17,9 |
| #665 | F184 | 30 (1) | 11 | 20 | 2 (mindhárom jel) | 0 | 3 | 13; 13; 6 | 5 (1) | 4,6 / 22,9 |
| #666 | F103 | 19 (1) | 10 | 5 | 1 (mindhárom jel) | 0 | 2 | 12; 3 | 4 (0) | 5,8 / 23,3 |
| #667 | F185 | 4 (2) | 1 | 0 | 0 | 1 | 0 | nem mérhető | 4 (1) | 2,2 / 8,6 |
| #668 | HATAR | 8 (2) | 9 | 1 | 0 | 0 | 0 | nem mérhető | 3 (1) | 2,4 / 7,1 |
| #669 | – | 3 (1) | 0 | 2 | 0 | 0 | 0 | nem mérhető | 3 (1) | 2,0 / 6,1 |
| #670 | – | 1 (0) | 2 | 0 | 0 | 0 | 0 | nem mérhető | 1 (0) | 1,9 / 1,9 |
| #672 | F188 | 1 (0) | 1 | 0 | 0 | 0 | 0 | nem mérhető | 1 (0) | 1,4 / 1,4 |
| #673 | MAIN-ZOLD | 3 (2) | 0 | 3 | 0 | 0 | 0 | nem mérhető | 3 (0) | 1,7 / 5,2 |

`scope=PR #663, #664, #665, #666, #667, #668, #669, #670, #672, #673 | forras=gh+git (teher_meres.py @ f910d799) | ts=2026-11-10T09:02+0100`

**Összesítés a célokkal:**

- **admin ≤ tartalmi:** 3 PR teljesíti a 10-ből. Nem teljesül.
- **Átlagos javítókör:** 0,50 a 10 PR-on (teljesül). A 3 ellenőrzött feladat-PR-on (#664, #665, #666) viszont 1,67, ami nem teljesül.
- **Ellenőri futás:** 8 futás mérhető, a leghosszabb 13 perc; a 15 perces célt egyik sem lépi át (becslés).
- **CI:** 29 futás, átlagosan 3,0 perc futásonként.

A brief táblájának számait (#664, #665, #666, #668: commit, admin, tartalmi) a mérés hiánytalanul visszaadta.

**Orkesztrátori közlés (mért adat, nem a szkriptből):** `manual (orkesztrátori közlés, 2026-11-10)`

1. A `teszt_arculat.py` egymagában kb. 30 percig fut; ezt a #104 javítókörében mérték. A végrehajtók minden körben lefuttatják.
2. A #181 végrehajtójának helyi CI-futása kb. 1 óráig tartott, mert a gépen egyszerre 5–6 session futtatott ellenőrzést.

**Amit a mérés nem fed le:** a brief „20–60 perc” ellenőri ideje a #104-ből jön, amely még nincs mergelve, ezért nincs a mintában. A commit-rés módszer a mért PR-okon legfeljebb 13 percet ad.

A teher ezért nem a CI egyes futásaiban van (1–6 perc), hanem három helyen:

- a helyi tesztekben (a `teszt_arculat` kb. 30 perc);
- a párhuzamos helyi futásokban (kb. 1 óra);
- a feladat-PR-ok admin-túlsúlyában.

## T3 — előzetes formai javító (A ág)

`eszkozok/ellenorzes/elojavit.py`. A felismerés a CI saját kódja: a `szabalyok.py`-t importálja, nem másolja.

- **E32:** a zárójeles hivatkozás eleme helyőrzőt törli, így a szöveg számfüggetlen lesz.
- **E8:** a tanulmányfájl STEPBible-alakját és az adatforrást megnevező sor idézőjeles igehely-idézetét kódformázza. A prózai tiltott alakot csak jelzi, a javasolt alakkal.
- **E5:** a törölt címsort csak jelzi, a kész jelölősorral, mert a szándékot csak a végrehajtó tudja. A `--e5-jelol --ir --commit-uzenet-fajl` hármas beírja a sort az üzenetfájlba.
- **Működés:** alapból száraz futás (a diff a stdout-ra kerül), `--ir`-rel ír. Kilépési kód: 0, ha nincs teendő; 1, ha van; 2 futási hibánál.
- **Próba a repón:** a `eszkozok/general.py` egy E32-helye javítható; két további helyet csak jelez, mert ott a helyőrző a mondat része.
- **Tesztek:** `tesztek/test_elojavit.py`, 20 teszt (a T2-jelzés tesztjeivel együtt).

## T1 — egy jelentésfájl feladatonként

- **`BRIEF_SABLON.md` „Jelentés”** (a kanonikus hely, F184 D4):
  - a napló, a „Független ellenőrzés — <n>. ellenőrzés” szakasz(ok) és a Zárás egy fájlban áll;
  - az ellenőr jelentését a session menti, szó szerint, külön commitban, `F<nn>.<t>: ellenőri jelentés (…)` címmel (ezt méri a T0);
  - a régi `ELLENOR_*` és `_zaras.md` fájlok változatlanok.
- **`fuggetlen-ellenor`:** fájlt nem ír, a jelentést válaszként adja. Eddig sem volt Write eszköze.
- **`/kovetkezo`:** a 9. és a 10. lépés a jelentésfájlba ment.
- **`/elteres`:** a legutóbbi jelentés a legnagyobb sorszámú szakasz. A függő újraellenőrzés jelölője: `újraellenőrzés függ: <n+1>. ellenőrzés`.
  - **Visszafelé kompatibilis:** a régi `ELLENOR_F<nn>*` sorozatú feladatnál a régi forma folytatódik.
- **`feladatok.py`:** kivétel-módosítás nem kellett, mert a jelentésfájl a feladat saját `naplok/F<nn>_*` fájlja (`_kozos`). Új teszt rögzíti.
- **Korlát:** a CI D14-kizárása (`kozos.py`) a jelentésfájlra nem vonatkozik. Mért kockázat: a 361 régi ELLENOR-fájlon a nem adattáblás szabályok 1 találatot adnának (E2). Teendő: N-F188c.

## T2 — számot csak egy helyen

- **Felismerés:** a `szabalyok.py` `szamismetles` függvénye, JELENTES szinten. Ezt jelzi:
  - hatókör: nyitott tétel, README, jelentés;
  - a sor `.tsv` táblát nevez meg és darabszámot mond;
  - nincs mellette proveniencia, és nem generált blokkban, kódblokkban vagy backtickes kódban áll.
- **Mért kiindulás:** 133 fájl, 366 találat, 103 fájlban. `scope=NYITOTT_FELADATOK.md, nyitott/uj/, naplok/*_jelentes.md, **/README.md | forras=szabalyok.szamismetles @ de9d34ed | ts=2026-11-10`
- **Ami most működik:** az `elojavit.py` a hozzáadott sorokon tájékoztatóként jelez; a kilépési kódba nem számít.
- **Ami kimaradt, és miért:** a CI-szabállyá emelés (E38) és a szabály szövege. Mindkettő a SEMA 3.11 generált kapulistáját és a SEMA szövegét írná, azt pedig a #104 előtt nem írjuk. A pontos teendő: N-F188a.

## T4 — ellenőr-diéta, lassú tesztek

- **`fuggetlen-ellenor`** bemenete a szint és a head-re szóló CI-jelentés.
  - A CI által lefuttatott vizsgálatot nem futtatja újra. A `futtat.py`-t csak akkor futtatja, ha a head-re nincs befejezett futás.
  - Az E28-at az érintett lapokra szűkíti (`PARDES_E28_CSAK`, csak helyben; a CI-ben a teljes E28 fut).
  - Tesztet csak kódot érintő diffnél futtat.
- **`szabalyok.py` `e28_csak_szures`:** új CI-szabály nincs, a `SZINT` és a 3.11 változatlan.
- **`teszt_futtat.py`** (orkesztrátori kiegészítés):
  - `LASSU_LEFEDETT`: a lassú tesztek lefedett fájljainak listája, egy helyen;
  - `--diff ALAP`: a `teszt_arculat` és a `teszt_szintek` csak akkor fut, ha a diff az `eszkozok/olvaso_szerver/` alatti fájlt érint;
  - a `teszt_arculat` bekerült a `--gyors` által kihagyott lassú fájlok közé.
- **Végrehajtók:** a `vegrehajto-*.md` ugyanezt írja elő.

## T5 — kockázat szerinti ellenőrzési szint

- **Levezetés:** a `feladatok.py szint <nn>` (vagy `--extra`) a meglévő `munka` és `ir` mezőből vezeti le a szintet, új mező nélkül (DT-F188b).
- **A szabály kanonikus helye:** `MUNKAMENET.md` „Menet-ellenőrzés” (DT-F188c).
- **A mai briefeken:** #181, #184, #186, #188: `teljes`; #104: `konnyitett` (DT-F188b (c) kérdés; a javítókör után `teljes`, l. „Javítókör 1/2”, 1.).
- **Minden szinten megmarad:**
  - a PR teljes CI-je, E1–E37;
  - a modell-ellenőrzés;
  - a brief G/D és ⛔ pontjai;
  - az E17 sorszám-változás;
  - az A1 proveniencia;
  - a `teves` besorolás csak saját lekérdezéssel.
- **Amit a könnyített szint elhagy:** csak az A3–A6-ot és a második javítókört.
- **Formai kör:** a tisztán formai javítókör nem nyit újraellenőrzést; a zöld CI zárja.
- **Ahol átvezetve:** `/elteres` (korlát `K`, jelölő `[elteres_kor k/K]`), `/kovetkezo` 9. lépés, `/befogad`.

**Helyi zár** (orkesztrátori kiegészítés): a `futtat.py` `HelyiZar` osztálya. Ugyanezt a zárat veszi a `teszt_futtat.py` is.

- A zár helye: `~/.pardes/ellenorzes.zar`. Windowson ez `C:\Users\<név>\.pardes\ellenorzes.zar`, WSL-ben a WSL saját home-ja.
- A `teszt_futtat.py` a zárat a Windows-oldalon veszi, mielőtt a WSL-be lép.
- A hely felülírható: `PARDES_ZAR_KONYVTAR`.
- Foglalt zárnál a futás kiírja, ki tartja, és vár.
- A zár feloldódik, ha a tartó folyamat ugyanazon a gépen már nem él, vagy ha a zár a korlátnál régebbi (120 perc, `PARDES_ZAR_KORLAT_PERC`).
- GitHub alatt nincs zár.
- Teszt: `tesztek/test_zar.py`, 10 teszt.

## T6 — main-őr

A `/kovetkezo` 1. lépése: `gh run list --branch main --workflow ellenorzes --limit 1`. Ha a main utolsó futása piros, a javaslat első sora jelzi, a futás azonosítójával, a commit-sha-val és a bukott lépéssel. A jelzés nem blokkol.

- **Próba:** 42775641047 (`904c52da`), failure. A bukott lépés az E2–E37 és az E1. Ez nem a #188 diffjéből ered; nem javítottam.
- **Feed/Stash:** az ottani jelzés N-F188b.

## T7 — mérés utána

Ebben az ágban nem végezhető el: a merge utáni első 3 PR-on fut, pontos hívással (N-F188e).

## Javítókör 1/2 (`naplok/ELLENOR_F188.md`, 5 ELTÉRÉS-tétel)

**Egyeztetett eltérés:** a javítókör az orkesztrátor döntésére ebben a sessionben fut, nem külön sessionben, mert az asztali alkalmazás túlterhelt (749 session). Mind az 5 tétel döntése az orkesztrátoré; a besorolás mind az 5 tételnél `mechanikus`, mert a döntés megvan, és minden érintett fájl benne van az `ir`-ben. A javítókör alapja: `df7a658b` (az ELLENOR_F188 rögzítése).

1. **T5, fordított logika** (F188.4; DT-F188b (c), kiterjesztve; DT-F188c): a szint alapból `teljes`. `konnyitett` csak akkor lehet, ha az `ir` minden eleme a `feladatok.py` `SZINT_KONNYITETT_*` listájára esik: dokumentáció, koordináció, teszt, CI vagy parancs.
   - Az olvasói kimenetet előállító kód (`SZINT_OLVASOI_*`) mindig teljes.
   - Ugyancsak teljes: üres `ir`, ismeretlen elem, glob, perjel nélküli könyvtárnév.
   - A mai briefeken 174 teljes és 11 könnyített: #26, #29, #32, #39, #40, #45, #47, #49, #50, #111, #112. A #104, #159, #172 és #174 teljes.
   - Teszt: SzintTest, 8 teszt.
2. **T4** (F188.5): a `LASSU_LEFEDETT` kiegészült az importfüggésekkel: `olvaso_pilot/`, `bdb_jelolt/`, `bdb_rovidites` és `kiejtes`, `tanulmany_regiszter`, `bdb_konyv_javit`, `normalizal`, `forditas_kapuk`, `tsk_kulcs`, `karoli_kh_szuro`. A `teszt_szintek`-nél az `adat/` és a `konkordancia/` is a listán van, mert a pilot JSON a TSV-kből épül.
   - A kihagyási üzenet most azt mondja meg, mit nem futtatott és miért. A „CI a mérvadó” kikerült belőle, mert a CI ezeket a teszteket nem futtatja.
   - Teszt: `test_zar.py`, köztük statikus őr: az olvasó-szerver fájlútról betöltött moduljai a listán állnak.
3. **T3, az A ágon** (F188.6, `28ccd53b`; beolvasztva `7eec99b1`, `--no-ff`): az előjavító generált fájlba nem ír. Generált a `lexikon/`, `nyilt_mag/`, `generalt_proba/` alatti fájl és a `# GENERÁLT` / `<!-- GENERÁLT:` fejlécű fájl; a kézi fájl `GENERÁLT-KEZDET` blokkjába sem ír.
   - Az E8 csak táblacellában és rövid (60 karakteres vagy rövidebb), egysoros adatidézetben formáz; prózában csak jelez.
   - Teszt: `test_elojavit.py`, 27 teszt a B ágon (25 az A ágon).
4. **Zár** (F188.7): a zár létrehozása `O_EXCL`-lel történik; az elavult zárat a váró átnevezéssel veszi át, és utána tartalmi összevetéssel ellenőrzi, hogy nem friss zárat nevezett-e át.
   - A tartót a zár egyedi azonosítója (`azon`) jelöli, nem a pid.
   - Kilépéskor a tartó a saját átnevezett példányát is törli.
   - Windowson a PermissionError-t rövid ideig újrapróbálja.
   - Teszt: két szál egy elavult zárra, 20 kör; egyszerre legfeljebb egy tartó, a végén nem marad zárfájl.
5. **Eszkaláció** (F188.8): ha az ellenőr könnyített szintről teljesre vált, a jelentés második sora ezt írja: `SZINT-ESZKALÁCIÓ: konnyitett → teljes — …`. A `/elteres` a K kört ebből veszi: K = a levezetett szint és az eszkaláció nagyobbika.

## Javítókör 2/2 (`naplok/ELLENOR_F188_2.md`, 3 ELTÉRÉS-tétel)

A kör alapja `2d1baf31` (az ELLENOR_F188_2 rögzítése; a B ág ebben a #674-es main-t is tartalmazza). Mindhárom tétel `mechanikus`, a már meghozott döntések alkalmazása (orkesztrátor). A gépen több session dolgozik, ezért csak célzott teszteket futtattam; a lassú teszteket és a teljes tesztsort nem.

1. **Zár** (F188.13; ELLENOR_F188_2 1.): az átnevezés és a visszatevés megszűnt, helyette a javasolt minta, átvételi zárral (`<ut>.atvetel`, `O_CREAT|O_EXCL`).
   - **Miért helyes.** A fő zár csak `O_EXCL`-lel jön létre. A fő zárat csak az átvételi zár tartója törli: az elavultat újraolvasás után, a sajátját kilépéskor. Így az újraolvasás és a törlés között senki más nem törölheti a fő zárat, és amíg az létezik, újat sem hozhat létre senki: a törölt fájl pontosan az elavultnak ítélt. Átvétel után az átvevő is `O_EXCL`-lel próbál, és ha más nyert, tovább vár.
   - **Időkorlátok:** az átvételi zár 60 s után (mtime) elavult. Az olvashatatlan vagy üres fő zár (a létrehozó még írja) 60 s türelmi időn belül nem elavult.
   - **Maradék kockázat:** ha egy folyamat az átvételi zár ezredmásodperces kritikus szakaszában omlik össze, és a 60 s után két váró egyszerre törli az elavult átvételi zárat, ketten lehetnek a kritikus szakaszban. Két fő zár ekkor sem létezhet egyszerre, mert az `O_EXCL` kizárja.
   - **Teszt:** `test_zar.py`, 17 teszt. A verseny 3 szállal és egy újonnan érkezővel fut, 40 körben; mindenki lefut, egyszerre legfeljebb egy tartó, a végén nem marad fájl. Ötször futtatva zöld.
2. **T5** (F188.14; ELLENOR_F188_2 2.): a `naplok/` közül csak a szöveges `*.md` könnyített; a `naplok/*.py`, `*.tsv`, `*.txt` és a puszta `naplok/` teljes.
   - A `LASSU_LEFEDETT` és a `SZINT_*` ellentmondását egy teszt fogja meg: a `LASSU_LEFEDETT` minden kódeleme a szint szerint teljes. Egyik lista nem származik a másikból, mert a kettő más kérdésre felel (olvasói kimenet, illetve tesztlefedés); a teszt köti össze őket.
   - A mai briefeken a szám változatlan: 174 teljes, 11 könnyített.
3. **Eszkaláció** (F188.15; ELLENOR_F188_2 3.): az eszkalációt egy önálló, sor eleji `SZINT-ESZKALÁCIÓ: konnyitett → teljes` sor jelzi, bárhol a jelentésben.
   - Gépi olvasás: `feladatok.py szint <nn> --jelentes <fájl>`, amely a tényleges kör-korlátot adja.
   - Teszt: `EszkalacioTest`, 3 teszt (⛔ első sor, szakaszos jelentés, CRLF; nem illeszkedik idézetre és behúzásra).

**Tesztek ebben a körben** (célzott): `test_zar.py` 17 OK; `teszt_feladatok.py` `SzintTest` 10 és `EszkalacioTest` 3 OK; `feladatok.py ellenoriz` 0 hiba; a `futtat.py` PR-módban, `[ELLENŐRZŐ]` címmel, a merge-base-hez (`99763405`) mérve: kilépési kód 0, HIBA nincs; csak jelentés (E25: 3, E27: 43, E30: 7, E34: 41). `scope=99763405..940927d2 | forras=futtat.py | ts=2026-11-10`. Megjegyzés: az `origin/main..HEAD` kétpontos diffje 11 hamis E5-HIBA-t adott, mert a main közben 22 commitot lépett (a #104 is bekerült); a CI a merge-base-t használja.

## Korlát fölötti javítás (engedéllyel) (`naplok/ELLENOR_F188_3.md`, 2 ELTÉRÉS-tétel)

A javítókör-korlát (2/2) betelt; a korlát fölött, engedéllyel javítva: a felhasználó a sessionök döntéseit az orkesztrátorra bízta, és ő ezt a javítást engedélyezte (2026-11-10). A döntések: DT-F188d = (b)+(c), DT-F188e = (a). Alap: `85eae013`. Csak célzott tesztek futottak.

1. **Zár: OS-szintű átvételi zár** (F188.20; ELLENOR_F188_3 1.; DT-F188d (b)+(c)).
   - Az átvételi zár az állandó `<ut>.atvetel` fájlon álló OS-zár: Windowson `msvcrt.locking`, POSIX/WSL-en `fcntl.flock`, nyitott fájlleíróval. Összeomláskor a rendszer magától feloldja, ezért az elavult átvételi zár és a 60 s-os mtime-törlés megszűnt. Ezzel megszűnt a 2/2-es kör maradék kockázata is: két tartó nem kerülhet a kritikus szakaszba.
   - Az OS-zár alatt marad az újraolvasás, az elavult fő zár törlése, és kilépéskor a saját zár törlése.
   - A pörgés helyére rövid alvás került (0,02 s). Ha a kilépő 60 s alatt sem kapja meg az OS-zárat, a saját zárát nem törli; a halott pid miatt a következő váró elavultként átveszi.
   - Teszt: `test_zar.py`, 19 teszt. Az OS-zár kizárja a második átvevőt. Az átvételi zár birtokában `os._exit`-tel kilépő alfolyamat után a zár felszabadul. A váró nem pörög. A korábbi versenytesztek is zöldek. Háromszor futtatva zöld.
2. **T5: az olvasói kód `naplok/`-bemenetei teljesek** (F188.21; ELLENOR_F188_3 2.; DT-F188e (a)).
   - Gépi gyűjtés egy helyen (`feladatok.py` `olvasoi_naplok()`): a `SZINT_OLVASOI_*` fájlok `naplok/` útvonal-literáljai. Ma 16 minta, köztük a `naplok/KAROLI_KH_EPSEG_jelentes.md`.
   - Teszt: ez a fájl teljes, a `naplok/F188_jelentes.md` könnyített.
   - Korlát: a literál nélkül, futásidőben összerakott utat a gyűjtés nem látja.

## Folytatás a #104 merge-e után

1. A T2 CI-szabállyá emelése és a szabály szövege a SEMA-ban, egy commitban (N-F188a): `SZINT`, `SZABALY_LEIRAS`, `SZABALYOK_FUGGVENYEI`, `szabalyok.py --kapulista --ir`.
2. Más SEMA-változás nem kell: a T5 nem hozott új fejlécmezőt.

## Zárás

**Egyeztetett eltérés** (orkesztrátor, 2026-11-10):

- két ág, és a PR-t nem a végrehajtó nyitja;
- a SEMA-t a #104 merge-éig nem írjuk, ezért a T2 CI-része kimaradt;
- a `.github/workflows/` nincs az `ir`-ben (N-F188d: az új tesztek a CI-ben);
- a T7 a merge után fut;
- kiegészítés:
  - a lassú tesztek csak érintettség esetén futnak;
  - egyszerre egy helyi teljes ellenőrzés fut (zár);
  - a T0-ba az orkesztrátor két mért adata került;
  - az `ir` kiegészült az `eszkozok/ellenorzes/futtat.py`-jal és az `eszkozok/teszt_futtat.py`-jal.

**Mi készült:** T0, T1, T3, T4, T5, T6 kész. A T2 részben készült: a felismerés kész, a CI-szabály a #104 után jön. A T7 a merge után fut.

**Döntések:** DT-F188a 🟢; DT-F188b 🟢 (c), kiterjesztve; DT-F188c 🟢 (orkesztrátor, 2026-11-10).

**Nyitott tételek:** N-F188a–e.

**Megjegyzés a PR-hoz:** a PR címe `[ELLENŐRZŐ]` előtagú legyen, mert a diff az `eszkozok/ellenorzes/`-t és a `fuggetlen-ellenor.md`-t érinti (E16). A brief fejléce `fut` marad; a lezárás az orkesztrátoré.
