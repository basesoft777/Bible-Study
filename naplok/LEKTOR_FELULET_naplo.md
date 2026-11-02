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

## ALVIL-001 — a határ- és a lektori kör kérdései a felületen (MUNKAMENET C-h, C-l; 2026-11-02)

- Indítás: a felhasználó (DT-F151b) az orkesztrátornak, 2026-11-02: „inditsuk el”, az újraindításra: „Igen, indítsd”.
- Bemenet: `naplok/HATAR_ALVIL-001.md` (Gépi rész: 0 kérdés, a lexikai hordozón a negatív-kritérium próba nem fut; Modelles rész: a `hatar-ellenor`,
  `claude-fable-5-1`, 2 kérdés, hígulás 0) és `naplok/KIADAS_ALVIL-001_lektor.md` (a `lektor`, `claude-fable-5-1`, 28 kérdés). A `/kiadas` jelölt-listája
  (`naplok/KIADAS_ALVIL-001_lista.md`) üres volt, ezért a lektor a teljes kézi prózát kapta (DT515).
- `naplok/LEKTOR_ALVIL-001.tsv`: **30 kérdés** = 2 `hatar` (1. kiadás) + 28 `lektor` (2. kiadás), mind `nyitva`; kézi kártya-összefoglaló mind a 30-hoz
  (`eszkozok/lektor_felulet/osszefoglalo_ALVIL-001.tsv`, `manual`; egyiknél sem volt konkrét javítási javaslat, mind `nincs`).
- Artifact: ugyanaz a link (https://claude.ai/artifact/GqczbTiP918WHpRVnzxZZv), 10. verzió; `epit.py` az összes `LEKTOR_*.tsv`-ből, `--lap-url` változatlan.
  Az élő változattal összevetve: a sablon azonos, a meglévő 53 kártya bájtra egyező adatú, új a 30 ALVIL-001 kártya (összesen 83). A kérdésekre ez a menet
  nem válaszolt, és semmit nem vezetett át.

## Lapnézet motívumonként (hibajelzés, a felhasználó szavaival: „minden lapnézet az istentisztelet artifactra mutat”; 2026-11-02)

- Ok: a `sablon.html` egyetlen `LAP_URL`-t használt (az ISTENTISZT-001 arany lapja), így minden kártya, az ALVIL-001 és a döntés-kártyák is, oda vitt.
- Javítás: kézi tábla `eszkozok/lektor_felulet/lapnezetek.tsv` (`motivum`, `url`, `megjegyzes`); az `epit.py` ebből tölti a `LAP_URLOK`-at (a `--lap-url` kapcsoló megszűnt),
  a kártya a saját motívumának nézetére mutat; ami nincs a táblában (más motívum, döntés-kártya), annak nincs linkje. 2 új teszt (`teszt_lektor_kerdesek.py`, 27 OK).
- Az ALVIL-001 nézete ugyanazzal az eszközzel, ahogy az arany lapé (`C:\Users\bases\pardes_eszkozok\epit_nezet.py lexikon/ALVIL-001_TUDOMANYOS.md … 6edf842d`), új privát
  artifactként: https://claude.ai/artifact/44gJuUTb1cu5ewgupXmyAQ. Az eszköz sablonfeliratai az ISTENTISZT-001-re vannak drótozva (cím, fejléc, forrásmegjelölés): a kimenetben ez a négy
  felirat ALVIL-001-re cserélve, a beágyazott lapszöveg érintetlen.
- Lektor-felület: ugyanaz a link, 11. verzió (a 12. a törlés-gombbal együtt); az élő változattal összevetve csak a link-logika változott (a 83 kártya adata azonos, a db-beli válaszok érintetlenek).
- Ellenőrzés böngészőben (a claude.ai a beépített böngészőben bejelentkezést kér, ezért a publikált HTML helyi kiszolgálásával): 67 megjelenő kártyán az ALVIL-001-é (30) az ALVIL-001
  nézetére, az ISTENTISZT-001-é (22) az arany lapra mutat, a 15 döntés-kártyán nincs link; az ALVIL-001 nézet renderel.

## Válasz törlése (a felhasználó kérése: „kellene egy válasz törlése gomb is. ahol egy megadott választ törlők”; 2026-11-02)

- `sablon.html`: a megválaszolt kártya alján „Válasz törlése”; kattintásra helyben megerősítés („Biztosan törlöd a válaszod? …” — Igen, törlöm / Mégse; a böngésző `confirm()` ablaka a
  beágyazott lapon tiltott lehet). Az „Igen” a `valaszok/<kerdes_id>` dokumentumot törli a db-ből (`doc().delete()`), majd a helyi tartalékból (localStorage) is, és a kártya újra megválaszolatlan.
  Ha a db-törlés nem sikerül, a felület kiírja („A válasz törlése nem sikerült (…): a válaszod megmaradt.”), és a válasz marad. Az átvezetett (`atvezetve`) kártyán nincs törlés-gomb.
- A máshol (másik eszközön) törölt válasz sem tér vissza: a válaszok `db` jelölést kapnak, ha az adatbázisban is megvannak; a snapshot `removed` változása és a szerver-nézetből hiányzó,
  korábban adatbázisbeli válasz törlődik a helyi másolatból; a csak helyben (adatbázis nélkül) mentett válasz marad.
- Próba (helyben, memóriabeli db-utánzattal, mert a claude.ai a beépített böngészőben bejelentkezést kér): válasz → törlés-gomb → Mégse (marad) → sikertelen törlés (marad, hibaüzenet) →
  törlés (db-ből és localStorage-ból eltűnik, kártya megválaszolatlan) → újra válasz (db-be kerül) → máshol törölt (eltűnik); a többi válasz érintetlen. Az élő oldalon gombnyomásos próba nem
  futott; az élő db `valaszok` gyűjteménye (3 dokumentum) a publikálás előtt és után bájtra azonos (ArtifactData list).
- Lektor-felület: ugyanaz a link, 12. verzió (a lapnézet-javítással együtt).

## Határ-kártya: „A jelenlegi határ” és „Ha így döntesz…” (a felhasználó kérése: „lektor határellenőrzéskor jó lenne bent lenni mi a jelenlegi határ . és a döntés következményei”; 2026-11-02)

- „A jelenlegi határ” (csak `forras=hatar`, általánosan): a `lektor_kerdesek.py` új `hatar_jelenlegi` mezője, gépileg az adatból — a motívum negatív kritériuma és fölérendelt fogalma szó szerint
  az `adat/motivumok.tsv`-ből (a kanonikus helyük; a `motivumok/<ID>.md` ezeket nem tartalmazza), és a kártya igehelyeinek (a cím és az (a) rész igehelyei + a `hely` mező) mai állapota:
  `elofordulasok.tsv` = bent van, `jeloltek.tsv` = döntés + indoklás, `fájl:sor` hivatkozással; saját proveniencia-sor. Ami nem olvasható ki (nincs motívum-sor, nincs igehely, nincs sor),
  azt a kártya kimondja, nem tölti ki.
- „Ha így döntesz…”: gombonként egy mondat. Az első két gombé a kézi összefoglalóból (`osszefoglalo_<ID>.tsv` új, elhagyható oszlopai: `kov_elfogadom`, `kov_elvetem`; csak határ-kártyán,
  csak párban), a számok az adatból (ALVIL-001: 8 újszövetségi sor / 9 vers, 10 hádész-vers; ISTENTISZT-001: 22 előfordulás, az 1. kiadás az `adat/kiadasok.tsv`-ben); a Visszakérdezek és
  a Saját megoldás mondata minden határ-kártyán ugyanaz (a sablonban). Kitöltve: az ALVIL-001 2 és az ISTENTISZT-001 5 határ-kártyáján.
- A `LEKTOR_ALVIL-001.tsv` és a `LEKTOR_ISTENTISZT-001.tsv` újragenerálva: csak a három új oszlop változott (a válasz-mezők soronként azonosak); a többi `LEKTOR_*.tsv` régi fejléccel is
  beolvasható. 4 új teszt (31 OK).
- Lektor-felület: ugyanaz a link, 13. verzió; az élő db `valaszok` gyűjteménye változatlan (3 dokumentum, ArtifactData list). Helyben, db-utánzattal megnézve: a két blokk csak a határ-kártyán
  jelenik meg, a lektori kártyán nem. Az élő oldalon a beépített böngésző bejelentkezést kér, ott a felhasználónak kell kipróbálnia.

## A felület új neve: Kiadó (DT516; a felhasználó: „A lektor kereszteljük át: Kiadó-ra”, pontosítva: „Csak a felület nevét”; 2026-11-02)

- A felület címe (`<title>`) és fejléce „Kiadó” (`eszkozok/lektor_felulet/sablon.html`); az `epit.py` leírása „a Kiadó (felület)”.
- Dokumentáció, ahol a felület mint hely szerepel: „Kiadó (felület)” — `MUNKAMENET.md` (C-h, C-l, C-k sora és a lezárás menete; 5 hely), `F10_LEXIKON_LEZARAS_BRIEF.md` (1),
  `F123_MIGRACIO2_BRIEF.md` (3), `sablonok/4_PaRDeS_tematikus_sablon.md` (1).
- Nem változik: a fájl- és eszköznevek (`naplok/LEKTOR_*.tsv`, `eszkozok/lektor_kerdesek.py`, `eszkozok/lektor_felulet/`), a `lektor` subagent, a „lektori kérdés / lektori kör”,
  a `CLAUDE.md`, a generált `FELADATOK.md`, a korábbi döntések, naplók (ez a napló is) és idézetek szövege, a #156/#157 briefjében a feladat neve.
- Az artifact ugyanazon a linken (https://claude.ai/artifact/GqczbTiP918WHpRVnzxZZv), 14. verzió; a db válaszai érintetlenek.

## Reszponzív elrendezés és élő próba Chrome-ban (a felhasználó: „böngészőben nagyon keskeny az oldal”; 2026-11-02)

- `sablon.html`: 1100 px fölött a tartalom legfeljebb 1240 px széles; a lektori kártyák két hasábban, a határ-kártya teljes szélességben, benne balra a kérdés és a gombok,
  jobbra a „Jelenlegi határ” és a „Ha így döntesz…”; a szűrősorok két hasábban. Telefonon egy hasáb marad (kérdés → határ-blokk → nagy gombok). A folyó szöveg sorhossza em-alapú
  korláttal ~70–75 karakter (mérve 1400 px-en: bevezető 75, „Mi a gond” 75, a határ-blokk 69–72; a nyers „Részletek” sorai a hosszú kód-azonosítók miatt 79-ig).
- Élő próba a felhasználó Chrome-jában (Claude in Chrome, saját fülön; az ablak maximalizált, ezért a szélességet a beágyazó keret szélességével állítottam: 1400 és 390 px):
  cím „Kiadó”; 1400 px-en két hasábos lektori kártyák és kettéosztott határ-kártya; 390 px-en egy hasáb, vízszintes görgetés nélkül; a határ-blokk megjelenik; törlés-próba
  (az ALVIL-001:mK1-en próbaválasz → „Válasz törlése” → „Igen, törlöm”): a kártya visszaállt nyitottra, a próbaválasz nincs a db-ben, a felhasználó 3 válasza bájtra azonos;
  konzolhiba nincs. A lapnézet-link célját kattintással nem lehetett igazolni (az új fül a próba fülcsoportján kívül nyílik); a közzétett oldal motívum → nézet táblája helyes.
- Artifact: ugyanaz a link, 15. verzió.
