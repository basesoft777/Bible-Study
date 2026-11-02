# LEKTOR_FELULET_naplo.md — F157 (#157) végrehajtási napló

*Modell-ellenőrzés: kért `sonnet`, tényleges `claude-sonnet-5-5` — egyezik.*

## 0. Ellenőrzés (2026-11-01)

- **DT-F157a–c** a brief 6. szakaszában eldöntve (egy felület; tároló: artifact-adatbázis; beolvasás kérésre) — átvéve.
- **db capability:** az `artifact-capabilities` szolgáltatás a fiók élő jogosultság-listáján a `db`-t kínálja (`artifact`, `assets`,
  `comments`, `db`, `downloads`, … ; runtime contract 0.2.96). A publikálás utáni működési próba eredménye lent (M1).
- **Tartalék:** a felület a db hiányában (`claude.use("db") === null`, vagy elutasított írás) a válaszokat a lapon tartja
  (kényelmi `localStorage`), és másolható összesítő sort ad; ez a tartalék a db mellett is ott van.

## M0 — kérdés-séma és generátor

- `eszkozok/lektor_kerdesek.py` (+ `eszkozok/teszt_lektor_kerdesek.py`, 8 teszt): a `naplok/HATAR_<ID>.md` Gépi rész K/N pontjaiból
  és a Modelles rész K pontjaiból `naplok/LEKTOR_<ID>.tsv`. A „Felhasználói besorolás” K-sorai a `valasz` mezőbe, az `allapot`
  `megvalaszolva`-ra kerülnek (DT-F151c, szó szerint); a már kitöltött `valasz`/`allapot`/`atvezetes` megmarad.
- `LEKTOR_ISTENTISZT-001.tsv`: 5 kérdés (K1–K5, mind a #151 felhasználói besorolásával); `LEKTOR_HAMART-001.tsv`: 0 kérdés (gépi
  rész 0 kérdés, modelles rész „nem futott”) — üres eredmény, jelölve, nem hiba.
- A CRLF-es forrásfájl (Windows) kezelve; a `hely` a kérdés első `jeloltek.tsv:<sor>` hivatkozásának igehelye.

## M1 — felület és artifact

- `eszkozok/lektor_felulet/sablon.html` + `epit.py`: a `naplok/LEKTOR_*.tsv` kérdéseiből építi az oldalt (csak kérdés-mezők és a
  repóban már rögzített döntés; a felhasználó artifact-beli válasza soha nem kerül az oldalba). Gombok: Elfogadom / Elvetem /
  Visszakérdezek / Saját szöveg; szűrő forrás, motívum, állapot szerint; egy hasáb, 48 px-es gombok (telefon); „lapnézet” link.
- Artifact (privát, `db` capability): https://claude.ai/artifact/GqczbTiP918WHpRVnzxZZv — a válaszok a `valaszok/<kerdes_id>`
  dokumentumokban; tartalék: kényelmi `localStorage` + másolható `LEKTOR-VALASZ | <kerdes_id> | <típus> | <szöveg>` összesítő.
- **Működési próba (db):** a `valaszok` gyűjtemény `ArtifactData` `list`-je a publikálás után üres (nem töltöttem fel), `as_level: view`
  szerint is üres. Amit nem tudtam kipróbálni: a gombok és az írás a böngészőben, telefonon (⛔ a felhasználó próbája, brief 2. lépés).
- Az artifact „lapnézet” linkje az arany lap nézetére mutat (1d9WcUQDkSLgEwopYXtFKq); horgony-ugrás nincs, a `hely` a kártyán áll.

## M2 — `proza_javaslat` kérdés-típus (orkesztrátor-kérés, felhasználó: „mehet”)

- Felhasználói felvetés: a lektor ne csak a meglévő próza hibáit találja meg, hanem olvasás közben is kérdezhessen: „az adatból ez
  következik, de a lap nem mondja ki — legyen róla mondat?”.
- Séma: új `forras` érték `proza_javaslat` (`FORRASOK`); `proza_javaslat_sor()` kötelezően kér adatsort (`fájl:sor`) és az adat saját
  proveniencia-sorát; a kérdés csak kérdez, mondatot nem javasol. Válaszlehetőségek: legyen mondat; nem kell; később.
- Felület: ennél a típusnál a gombok „Legyen mondat / Nem kell / Visszakérdezek / Saját szöveg”.
- A lektor prózát NEM ír (DT-F32b). Az „igen” a forrásfájl prózai feladata (`/befogad`-dal, jóváhagyással); a mondatot a próza írója
  írja az egészet olvasva. Az `eszkozok/lektor_kerdesek.py` ehhez nem generál sort: a forrás (a lektor-futás) a #125 után jön.
- **Függő:** a brief 3.1/3.4 szakasza és a `DONTESEK.md` DT-F157 helyőrző az `ir` listán kívül esik; írásuk jóváhagyásra vár.

## M3 — felmérés: döntés-kártyák és talált, kidolgozatlan motívumok (építés előtt, 2026-11-01)

*Felhasználói felvetés: „a lektor felület /reviewer felült is / pl döntések / már csak tartalmi / kidolgozatlan de talált motivumok?”; a javaslatra: „mehet”. Csak olvasás; egy fájl sem módosult az adatrétegben. Az építés a felmérés megmutatása után.*

### (1) Döntés-kártyák — forrás: `DONTESEK.md`

- A táblázat 514 `| DT…` sora: 475 szabályos (8 oszlop), **39 „furcsa”** (a kérdés/döntés szövegében ` | ` áll, így az oszlopszám 9–23). A kártya-generátornak
  ezért az oszlopokat a sor **elejéről (id, feladat) és végéről (napló, döntés, állapot)** kell vennie, nem a ` | ` szétvágásból.
- Az állapotok jelmagyarázata szerint 🟡 = nyitott; 🟢 = eldöntve, alkalmazásra vár; ✅ = alkalmazva. **Valóban nyitott (🟡) csak 14 tétel van**: DT90, DT106, DT126,
  DT133, DT134, DT169, DT190, DT235, DT236, DT237, DT338, DT359, DT365 és a „végrehajtó dönt” DT388. A 319 🟢 sor döntött, nem kártya.
- **Tartalmi vagy technikai** ítélet kell: a 14-ből tartalminak látszik a DT106 (a *tohu–bohu* pár szótári szerepe), a DT235–DT237 (mit fordítsunk: Mounce, TBESH
  forrásszöveg, tW-szócikk), a DT133–DT134 (ÚSZ-számlálás, versifikációs térkép) és a DT169 (modell-magyarázat a teljes BDB-re); üzleti: DT359, DT365 (#86);
  licenc/folyamat: DT126, DT90, DT190, DT338, DT388. Ezt a besorolást gép nem tudja megbízhatóan levezetni (a „Feladat” oszlop szövege nem hordozza), ezért
  **kézi szűrőlista kell** (az orkesztrátor/felhasználó jelöli „tartalmi”-nak), a generátor csak a jelöltek közül képez kártyát.
- Következmény: a **mai állapotban kevés (kb. 5–9) tartalmi nyitott kártya** lesz; a felhasználó előtt álló döntések nagy része a briefek ⛔ pontjain és az
  orkesztrátor chatjében van, nem a `DONTESEK.md` 🟡 soraiban. Ha a cél „minden, ami rám vár”, akkor a briefek `allapot: megallt` (10 db) és `dontesre_var` (1 db)
  fejléce is forrás lehetne — ez külön döntés.
- Visszaút változatlan: a kártya `dontes:<DT-azonosító>` (`forras=dontes`), a válasz a felhasználó idézetével a `DONTESEK.md`-be (session írja át); a lektor nem ír.

### (2) Talált, kidolgozatlan motívumok — honnan gyűjthető

| Forrás | Mi van benne | Használható? |
|---|---|---|
| `motivumlog/PaRDeS_motivumok.md` (655 sor) | Az egyetlen hely, ahol az **ID-t még nem kapott** motívumok állnak: 183 felsorolás-sor, ebből csak 11-nek van `[ID: …]`; „A blokkon kívüli, kézi tételek” (44., 181., 261. sor), „Előrejelzett, konkrét igehelyen megerősítendő” (215–240.), 14 „közel a küszöbhöz” sor (pl. *mély álom / tardémá* 1Móz 2:21 ↔ 15:12; *Ádám mint szövetségszegő*) | **Igen, fő forrás** — de **kézzel írt próza**: az igehelyek és a „küszöb” állítás nem gépi lekérdezés, a kártya proveniencia-sora `manual` |
| `NYITOTT_FELADATOK.md` 3. tétel | „Én vagyok” (2Móz 3:14 ↔ ἐγώ εἰμι; Ézs *Ani Hu*): 6 pozíció-alapon megerősített előfordulás, „még sehol nincs repóban dokumentálva” | **Igen**, egy nevesített jelölt |
| `adat/jeloltek.tsv` `nyitva` (34 sor) | HODIT-001 14, HAMART-001 8, ISTENTISZT-001 6, ANTROP-001 3, MENNY-001 2, KIRALY-001 1 — **meglévő** motívumok jelöltjei | **Nem (2)**; ezek a `hatar`/jelölt-kártya forrásai |
| `jeloltek.tsv` `motivumkozi` (7 sor), `motivum_kapcsolatok.tsv` | motívumok közti kapcsolat | Nem új motívum |
| `naplok/F108_*`, `JELOLT_ELOSZURES_*` | meglévő 9 motívum soraira | Nem új motívum |
| `motivumlog/Alap_bejegyzes_kigyujtes_v1_PISZKOZAT.tsv` | archív, hibás Strong-párosítás | **Kizárva** (a README szerint emberi felülvizsgálat nélkül nem használható) |
| `adat/motivumok.tsv` | csak a 9 kidolgozott motívum, jelölt-állapot oszlop **nincs** | Nem forrás |

- Nincs gépi „jelölt-motívum” tábla: a (2) kártyáinak forrása a `PaRDeS_motivumok.md` próza + a `NYITOTT_FELADATOK.md`. Hiányt ne töltsünk ki (CLAUDE.md 3. szabály): ahol a
  tételnek nincs igehelye vagy gerince, a kártya ezt mondja ki.
- A kártya kérdése („érdemes-e kidolgozni?”) és a **CLAUDE.md négy kötelező kérdésének előre kitöltött javaslata** értelmező munka: a javaslatot egy session írja
  (a próza-szabály szerint egy kéz, Opus; DT-F32b), a generátor csak a jelöltlistát és a forrás-hivatkozásokat adja. A „igen” `/befogad`-javaslat; **ID közvetlenül nem keletkezik**.
- Becslés: a (2) első lépcsőben 15–25 jelölt-kártya (a 14 „küszöb” sor + az „Én vagyok” + a blokkon kívüli kézi tételek közül a nevesíthetők); pontos szám a
  kézi tételek átnézése után mondható.

### Nyitott kérdések az építés előtt

1. A (1)-hez: a tartalmi-nyitott lista kézi szűrőből (javaslat) vagy a briefek `megallt`/`dontesre_var` fejlécéből is?
2. A (2)-höz: a javaslat-szöveget (négy kérdés) ki és mikor írja — a lektor-futás (#125 után), vagy egy külön kör?
3. Az `ir` lista szűk-e: a kártyák `naplok/LEKTOR_DONTESEK.tsv` és `naplok/LEKTOR_JELOLT_MOTIVUM.tsv` fájlba mennének (illeszkednek a `naplok/LEKTOR_*.tsv` mintához; az építő a fájlnévből veszi a „motívum” mezőt), ezért nem szűk; a **kézi szűrőlista** helye (pl. `adat/` vagy `naplok/`) új fájl, amelyet jóváhagyás nélkül nem hozok létre.

## M4 — arculat: A. Olvasó (a felhasználó választása, 2026-11-01)

- A `sablon.html` tokenjei és betűi a `KOZOS_TOKENEK.md` A változatára cserélve (világos és sötét mód a szabványos három blokkban): Source Serif 4 (cím),
  IBM Plex Sans (szöveg), IBM Plex Mono (adat), sugár 4px; méretskála 12/13/14/16/28 px. Tokennevek változatlanok, kiegészítve `--cim`, `--sugar`-ral
  (a #156 dashboarddal közös). Az artifact ugyanazon a linken frissítve (3. verzió). Nem ellenőrizve: a megjelenés böngészőben/telefonon (ArtifactCheck nem érhető el).

### M3 kiegészítés — a forrás-tanulmány megtalálhatósága (a felhasználó pontosítása: „eddig csak a igeszakasz tanulmányok következtében megjelent egy fájlban. és talan a tanulmány is utal rá”)

- A `motivumlog/PaRDeS_motivumok.md` valóban a tanulmányokból gyűjt (7. sor: a tanulmány 3/b. pontja, „Ismétlődő motívum korábbi tanulmányodból”); saját
  küszöb-jelölése van (⭐ küszöb elérve / közel a küszöbhöz / megerősítve). A bejegyzésekben **fájlhivatkozás nincs** (egyetlen `genezis/…` vagy `ujszovetseg/…` út sem
  szerepel), a forrás-tanulmány tehát az igehelyből **levezetve** keresendő.
- Módszer (heurisztika, nem lekérdezés): a bejegyzés igehelyeit (1Móz, Róm, Zsid, 1Thessz) összevetve a `genezis/` és `ujszovetseg/` fájlnevekbe kódolt vers-tartományokkal
  (23 igeszakasz-tanulmány; a `melyelemzesek/` és `tematikus_lezart/` fájlok témára épülnek, nem vers-tartományra, ezeket nem vettem be).
- Eredmény: a kézi kulcsszó-index 81 sorából **77-nél** (95%) van legalább egy igehely, amely egy igeszakasz-tanulmány tartományába esik; a „Kulcsszavak részletesen”
  31 `###` bejegyzéséből **28-nál**. Forrás nélkül marad (nincs lefedő tanulmány az idézett igehelyeken): *Ádám mint szövetségszegő* (csoport), *Nimród — történelmi
  azonosítási kísérletek*, *Hágár mint tipológiai alak*. A 23 tanulmányból **19-ben** van „Ismétlődő motívum” jelzés (a 3/b szerinti visszautalás).
- **Fenntartás:** a levezetés azt mondja meg, melyik tanulmány *tartalmazza* az idézett verset, nem azt, hogy a motívum *melyikből indult*. Egy bejegyzés több tanulmányra
  is illeszkedhet (az „előfordulás-pár” két oldala két tanulmány). A kártyán ezért „tanulmány(ok), amely(ek) az igehelyet tárgyalja/tárgyalják” szerepeljen, linkkel, és a
  3/b sor idézete, ha van; ahol a levezetés nem ad találatot, a kártya ezt kimondja (nem töltjük ki).
- Küszöb-állapot szerinti sorrend: a kézi index soraiban **nincs** küszöb-jelölés (csak az „Emlékeztető küszöb” kézi blokkjában és a `###` bejegyzések fejében: 1 „küszöb elérve”,
  2 „közel a küszöbhöz”, 1 „megerősítve” a fejekben; a 14 küszöb-közeli sor a blokkban). A sorrend tehát csak a küszöb-jelölt tételeknél (kb. 14–18) adható meg, a többi
  „jelöletlen” csoport.

## M5 — döntés-kártyák (`dontes` forrás; DT483: „mindkettő”)

- `eszkozok/lektor_kerdesek.py --dontes` → `naplok/LEKTOR_DONTESEK.tsv`: **31 kártya** = 14 nyitott (🟡) `DONTESEK.md`-tétel + 17 megállt (`megallt` / `dontesre_var`) brief.
  A táblázat soraiban az állapot az első emojis cella (a 39 „furcsa” sor miatt nem az oszlopszám); a briefeknél a fejléc `kovetkezo` mezője (karbantartott) és a ⛔ sorok
  gépi, nem szűrt kivonata (a lezárt pontokat a kulcsszavak alapján kihagyja) áll a kártyán. A proveniencia: `scope=DONTESEK.md:<sor>` illetve `scope=<brief> (fejléc + ⛔ sorok)`
  | `forras=lektor_kerdesek.py` | `ts=<futás napja>`.
- Új séma-oszlop: `cimke` (tartalmi / uzleti / technikai / osztalyozatlan). A nem-döntés források tartalmiak. A régi fejlécű TSV-t a beolvasás elfogadja.
- **Kézi szűrő:** `eszkozok/lektor_felulet/dontes_szuro.tsv` (azonosító → címke). A kezdeti tartalom *javaslat* (Sonnet), a felhasználó módosíthatja; ami nincs benne, `osztalyozatlan`.
  A felület típus-szűrője alapból a „tartalmi”-t mutatja.
- Életciklus: a lezárult kártya (a tétel ✅ lett, a brief már nem megállt) elhagyható, ha az állapota `atvezetve`; a megválaszolt, de át nem vezetett kártya eltűnése megállítja az írást.
- **Ismert hiányosság:** a briefek ⛔ kivonata zajos (pl. szakaszcímek, általános szabálymondatok is bekerülhetnek); a döntő információ a `kovetkezo` sor. A `kod` nélküli brief (F22) „#22 F22”-ként jelenik meg.
- A talált motívumok kártyái (`motivum_jelolt`) **nincsenek építve** (a javaslat-író még eldöntetlen).

## M6 — mindig világos (DT484)

- A felhasználó döntése: a lektor-felület mindig az A. Olvasó világos változatát mutatja, a témától függetlenül (a Feedre: „Igen, mindig világos”; a lektor-felületre: „igen”).
- A `sablon.html`-ből kikerült a sötét token-készlet, a `prefers-color-scheme` blokk és a `[data-theme]` kapcsolás; a `:root` a világos tokeneket adja (`--papir: #f6f6f3`),
  a `color-scheme: light` az Artifact-váz alapja. A többi (betűk, méretek, sugár) változatlan. Az artifact újrapublikálva (6. verzió).


## M7 — a /kiadas kimenete a felületen (`lektor` és `proza_lefedettseg` forrás)

- Bemenet (a fő checkoutból, változatlanul átmásolva; a bájtazonosságot `cmp` igazolta): `naplok/KIADAS_ISTENTISZT-001_lektor.md` (a `lektor` subagent, Fable 5.1 kimenete, 15 kérdés) és
  `naplok/KIADAS_ISTENTISZT-001_lista.md` (a próza-lefedettség mérőjének kimenete). Az ISTENTISZT-001 `/kiadas` menetét az orkesztrátor-session indította a felhasználó
  „csináljuk” kérésére; az átolvasás része volt, hogy „a kérdések a lektor-felületre kerülnek”.
- `eszkozok/lektor_kerdesek.py`: `lektor_kerdesek()` (számozott tétel = kérdés, a `## ` szakasz a `hely`, a szöveg változatlan, a proveniencia a fájl záró sora) és `lista_hianyok()` („Név nélküli
  elemek” → `forras=proza_lefedettseg`, `hely` az igehely; a lista nem hordoz proveniencia-sort, ezért `manual`). Az egyenetlenség-tábla nem kérdés, nem kerül be. 18 teszt.
- `naplok/LEKTOR_ISTENTISZT-001.tsv`: **22 kérdés** = 5 `hatar` + 15 `lektor` + 2 `proza_lefedettseg`. Átfedés: a lektor 1. és 2. kérdése ugyanaz a két hiány, mint a lista két sora
  (1Móz 4:26 → Sof 3:9; Ézs 41:25); a kártyák külön azonosítóval külön válaszolhatók, ez szándékos (a két forrás egymástól független).

## M8 — érthető kártyák (felhasználói visszajelzés: „egyáltalán nem világos”)

- Ok: a kártya a lektor nyers szövegét mutatta (sorszámok, proveniencia), és a gombok nem mondták meg, mit jelentenek. A kártya most: **Mi a gond** (egy egyszerű mondat) →
  **Mit javasol a lektor** (egy mondat; „a lektor nem javasolt konkrét javítást”, ha a lektor-fájlból konkrét javítás nem vezethető le) → a nyers szöveg a lenyitható **Részletek** alatt.
- A gombfeliratok a kérdés fajtájához igazodnak (`javaslat_tipus`): `konkret` (Elfogadom — javítsuk így), `nincs` (Javítandó — a próza írója megoldja / Maradjon így), `hiany` (Legyen róla mondat /
  Szándékos, maradjon így), `dontott` (Marad a rögzített döntésem / Mégis másképp). Mind a négy: Visszakérdezek — nem értem / kérdésem van; Saját megoldás — én írom le. A tárolt válasz típusa
  változatlan (`elfogadom` / `elvetem` / `visszakerdezek` / `sajat`). Mindig látható súgósor a lap tetején.
- Az összefoglaló mondatok **kézzel írt, értelmező összefoglalók** (`eszkozok/lektor_felulet/osszefoglalo_ISTENTISZT-001.tsv`, `manual` proveniencia): a lektor/forrás állítását adják vissza, újat nem tesznek
  hozzá. A `lektor_kerdesek.py` kerdes_id szerint olvassa be (ismeretlen kerdes_id és ismeretlen típus hiba); az ISTENTISZT-001 mind a 22 kérdéséhez van összefoglaló (teszt).
  A lektor 15 kérdése közül egyiknél sem volt konkrét javítási javaslat, ezért mind `nincs` (vagy `hiany`).
- A 31 döntés-kártya (`dontes`) még a régi formában van (nincs összefoglalójuk).
- Felület: az ISTENTISZT-001 kártyái elöl, a döntés-kártyák utána; a motívum-szűrő nem sorolja fel a döntés-kártyák feladatait.

## M9 — kiadás-jelölés (felhasználó: „melyik ügyek tartoznak már az új kiadásra / melyik az iniciál kiadásra”)

- A döntés (az orkesztrátor közvetítésével): a `/kiadas` kimenetéből jövő kérdések (`forras=lektor`, `proza_lefedettseg`, és a `proza_javaslat`) a következő, **2. kiadás** bemenetei; a határ-kérdések (`hatar`)
  a mostani, **1. kiadáshoz** tartoznak. A besorolás a forrásból következik (`KIADAS_FORRASONKENT`), nem kézi mező; új séma-oszlop: `kiadas` (`1` | `2` | üres).
- A döntés-kártyák (`dontes`) nem kiadás-kérdések: `kiadas` üres, a felületen „kiadáson kívül”.
- Felület: minden kártyán kiadás-jelvény; a lap tetején kiadás-szűrő darabszámokkal: mind (53) · 1. kiadás (5) · 2. kiadás (17) · kiadáson kívül (31). A régebbi fejlécű TSV beolvasható.
- Nincs `DONTESEK.md` tétel a besorolásról (nem kérték); ha kell, DT-F157 helyőrzővel rögzíthető.

## 7. Döntés-kártyák három kategóriája (DT-F161a, 2026-11-02, „mehet”)

*Besorolás: mit változtat meg a döntés? négy kategória (tartalmi · kiadói · üzleti · fejlesztői), ütközésnél tartalmi > kiadói > üzleti > fejlesztői; a felhasználó szó szerint (2026-11-02, az orkesztrátoron át): „egy új kategória is lesz: üzleti / ahol ügyfélszolgálat / számlázás/ megrendelés stb”; az üzleti kártyák a felhasználóéi, a fejlesztőieket az orkesztrátor dönti; a gépi jel a forrás-brief `ir` és `munka` mezője (`lektor_kerdesek.gepi_kategoria`); a `dontes_szuro.tsv` kézi címkéje elsőbbséget élvez. A „kézi” oszlop a mai (régi) címke. Mért: 28 mai kártya (a korábbi 31-ből az F131, F148, F152 lezárult).*

| kártya | kézi (mai) | gépi | eltér | indok |
|---|---|---|---|---|
| DT90 | fejlesztoi | fejlesztoi |  | gépi: a #52 brief csak ír: CLAUDE.md; munka: folyamat (eszköz, séma, munkafolyamat) |
| DT106 | tartalmi | osztalyozatlan | igen | nincs F5_*_BRIEF.md, és kézi besorolás sincs |
| DT126 | fejlesztoi | fejlesztoi |  | gépi: a #60 brief csak ír: eszkozok/olvaso_pilot/adat.py, eszkozok/olvaso_pilot/bdb_szelet.py; munka: adat (eszköz, séma, munkafolyamat) |
| DT133 | tartalmi | fejlesztoi | igen | gépi: a #92 brief csak ír: eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py; munka: adat (eszköz, séma, munkafolyamat) |
| DT134 | tartalmi | fejlesztoi | igen | gépi: a #92 brief csak ír: eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py; munka: adat (eszköz, séma, munkafolyamat) |
| DT169 | tartalmi | kiadoi | igen | gépi: a #99 brief ír: eszkozok/olvaso_szerver/, eszkozok/olvaso_szerver/bdb_vers_jelentes.py (megjelenés, licenc, felület) |
| DT190 | fejlesztoi | osztalyozatlan | igen | nincs F9_*_BRIEF.md, és kézi besorolás sincs |
| DT235 | tartalmi | tartalmi |  | gépi: a #121 brief ír: adat/forditasok.tsv, adat/terminologia.tsv (a lexikon állítását érinti) |
| DT236 | tartalmi | tartalmi |  | gépi: a #121 brief ír: adat/forditasok.tsv, adat/terminologia.tsv (a lexikon állítását érinti) |
| DT237 | tartalmi | tartalmi |  | gépi: a #121 brief ír: adat/forditasok.tsv, adat/terminologia.tsv (a lexikon állítását érinti) |
| DT338 | fejlesztoi | tartalmi | igen | gépi: a #121 brief ír: adat/forditasok.tsv, adat/terminologia.tsv (a lexikon állítását érinti) |
| DT388 | fejlesztoi | tartalmi | igen | gépi: a #121 brief ír: adat/forditasok.tsv, adat/terminologia.tsv (a lexikon állítását érinti) |
| DT359 | uzleti | uzleti |  | gépi: a #86 brief ír: eszkozok/feed_epit.py (ügyfél, számlázás, megrendelés, árazás) |
| DT365 | uzleti | uzleti |  | gépi: a #86 brief ír: eszkozok/feed_epit.py (ügyfél, számlázás, megrendelés, árazás) |
| F111 | fejlesztoi | fejlesztoi |  | gépi: a #111 brief csak ír: .claude/commands/elteres.md, .claude/commands/kovetkezo.md; munka: folyamat (eszköz, séma, munkafolyamat) |
| F121 | tartalmi | tartalmi |  | gépi: a #121 brief ír: adat/forditasok.tsv, adat/terminologia.tsv (a lexikon állítását érinti) |
| F123 | tartalmi | tartalmi |  | gépi: a #123 brief ír: motivumok/ALVIL-001.md, motivumok/ANTROP-001.md; munka: ertelmezo (a lexikon állítását érinti) |
| F125 | tartalmi | fejlesztoi | igen | gépi: a #125 brief csak ír: MUNKAMENET.md, eszkozok/proza_lefedettseg.py; munka: folyamat (eszköz, séma, munkafolyamat) |
| F134 | fejlesztoi | kiadoi | igen | gépi: a #134 brief ír: eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/statikus/ (megjelenés, licenc, felület) |
| F140 | tartalmi | tartalmi |  | gépi: a #140 brief ír: adat/glosszak_heber_hu.tsv (a lexikon állítását érinti) |
| F146 | fejlesztoi | tartalmi | igen | gépi: a #146 brief ír: lexikon/ISTENTISZT-001_TUDOMANYOS.md (a lexikon állítását érinti) |
| F151 | tartalmi | fejlesztoi | igen | gépi: a #151 brief csak ír: eszkozok/motivum_hatar.py, eszkozok/teszt_motivum_hatar.py; munka: adat (eszköz, séma, munkafolyamat) |
| F153 | fejlesztoi | tartalmi | igen | gépi: a #153 brief ír: adat/forditasok.tsv (a lexikon állítását érinti) |
| F157 | fejlesztoi | kiadoi | igen | gépi: a #157 brief ír: eszkozok/lektor_felulet/ (megjelenés, licenc, felület) |
| F22 | fejlesztoi | fejlesztoi |  | gépi: a #22 brief csak ír: eszkozok/karoli_strong/tokenszint_vershatar.py, eszkozok/karoli_strong/nem_tr_lista.py (eszköz, séma, munkafolyamat) |
| F38 | tartalmi | tartalmi |  | gépi: a #38 brief ír: adat/forditasok.tsv (a lexikon állítását érinti) |
| F52 | fejlesztoi | fejlesztoi |  | gépi: a #52 brief csak ír: CLAUDE.md; munka: folyamat (eszköz, séma, munkafolyamat) |
| F86 | uzleti | uzleti |  | gépi: a #86 brief ír: eszkozok/feed_epit.py (ügyfél, számlázás, megrendelés, árazás) |

Eltér: 13 / 28.

### 7.1 Végleges besorolás (orkesztrátori döntés a felhasználó felhatalmazásával, 2026-11-02; DT-F161a)

A 13 eltérésből a kézi marad: DT106, DT133, DT134, DT169, F125, F151 (tartalmi), DT190 (fejlesztői); a gépi érvényes: DT338, DT388, F146, F153 → tartalmi, F134, F157 → kiadói (a `dontes_szuro.tsv`-ben frissítve). Lefelé-védelem: a gépi jel nem sorol lejjebb kézzel tartalminak/kiadóinak/üzletinek jelölt kártyát (az indokban jelezve). Szűk bővítés: `naplok/HATAR_` az `ir`-ben tartalmi jel.

| kártya | régi kézi | gépi | végleges | indok |
|---|---|---|---|---|
| DT90 | fejlesztoi | fejlesztoi | fejlesztoi | kézi besorolás (dontes_szuro.tsv) |
| DT106 | tartalmi | osztalyozatlan | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| DT126 | fejlesztoi | fejlesztoi | fejlesztoi | kézi besorolás (dontes_szuro.tsv) |
| DT133 | tartalmi | fejlesztoi | tartalmi | kézi besorolás (dontes_szuro.tsv); a gépi jel alacsonyabbat (fejlesztoi) mondana, a kézi marad |
| DT134 | tartalmi | fejlesztoi | tartalmi | kézi besorolás (dontes_szuro.tsv); a gépi jel alacsonyabbat (fejlesztoi) mondana, a kézi marad |
| DT169 | tartalmi | kiadoi | tartalmi | kézi besorolás (dontes_szuro.tsv); a gépi jel alacsonyabbat (kiadoi) mondana, a kézi marad |
| DT190 | fejlesztoi | osztalyozatlan | fejlesztoi | kézi besorolás (dontes_szuro.tsv) |
| DT235 | tartalmi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| DT236 | tartalmi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| DT237 | tartalmi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| DT338 | fejlesztoi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| DT388 | fejlesztoi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| DT359 | uzleti | uzleti | uzleti | kézi besorolás (dontes_szuro.tsv) |
| DT365 | uzleti | uzleti | uzleti | kézi besorolás (dontes_szuro.tsv) |
| F111 | fejlesztoi | fejlesztoi | fejlesztoi | kézi besorolás (dontes_szuro.tsv) |
| F121 | tartalmi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| F123 | tartalmi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| F125 | tartalmi | fejlesztoi | tartalmi | kézi besorolás (dontes_szuro.tsv); a gépi jel alacsonyabbat (fejlesztoi) mondana, a kézi marad |
| F134 | fejlesztoi | kiadoi | kiadoi | kézi besorolás (dontes_szuro.tsv) |
| F140 | tartalmi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| F146 | fejlesztoi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| F151 | tartalmi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| F153 | fejlesztoi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| F157 | fejlesztoi | kiadoi | kiadoi | kézi besorolás (dontes_szuro.tsv) |
| F22 | fejlesztoi | fejlesztoi | fejlesztoi | kézi besorolás (dontes_szuro.tsv) |
| F38 | tartalmi | tartalmi | tartalmi | kézi besorolás (dontes_szuro.tsv) |
| F52 | fejlesztoi | fejlesztoi | fejlesztoi | kézi besorolás (dontes_szuro.tsv) |
| F86 | uzleti | uzleti | uzleti | kézi besorolás (dontes_szuro.tsv) |

Darabszám: fejlesztoi 6, kiadoi 2, tartalmi 17, uzleti 3 (összesen 28).
