# KAROLI_MODERN_meres.md — a modernizált Károli-réteg mérési naplója (F96, FELADATOK #96)

*Brief: `F96_KAROLI_MODERN_BRIEF.md` v1.1. Végrehajtó: claude-opus-5-5 (a kért modell: opus). Ág: `ccr-a680d019-39s73e`.*

## 1. F96.0 — előkészítés és fedettségi mérés

### 1.1 Bemenet

| bemenet | hash (sha256, első 12) | megjegyzés |
|---|---|---|
| `konkordancia/Karoli_1908.tsv` | 49335bbcc77d | 31 158 vers, 599 367 token |
| `adat/szoto/karoli_szotari_alak.tsv` | edba33e6d65a | a #94 kiadott táblája (C+K, simplemma nélkül, DT139), 66 824 sor |

A tokenizálás a `eszkozok/karoli_strong/tokenek.py` `tokenizal` függvénye (Unicode betű- és számjegysorozat), mert a Károli–Strong párosítás `hu_sorszam`-a ezen áll; a szóalak-szótár kulcsa így ugyanaz a token, amelyre a Strong-szám szavanként átvihető (K3). A #94 korpusz-lexikonja a kötőjeles alakot egy szónak veszi (*czédrus-deszkával*); a tokenizálás ezt két tokenre bontja, ezért 683 token-alak a táblában sincs (1.2, `tablan_kivul`).

**Szóalakszám:** 66 086 kis-/nagybetű-érzékeny, **62 109 kisbetűs** (a brief 62 109-es száma ez).

### 1.2 Fedettség alakonként

`scope=a Károli 1908 minden tokenizált szóalakja (66 086) | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) | ts=2026-10-24T11:31Z` — `python eszkozok/karoli_modern/fedettseg.py`; az alakonkénti osztályozás: `adat/karoli_modern/fedettseg_alakok.tsv` (generált mérőtábla, nem a kiadott réteg).

| osztály | alak | token | ki adja a modern alakot |
|---|---:|---:|---|
| `valtozatlan` | 59 979 | 551 464 | nincs változás (sem jegy, sem helyesírási eltérés, sem régies gyanú) |
| `helyesiras_szabaly` | 1 111 | 4 713 | karakterszabály: *cz → c*, *czcz → cc*, *nyny → nny*, *lyly → lly* … és *néki → neki* (DT128) — **szabály** |
| `helyesiras_tabla` | 163 | 1 062 | a #94 `szotari_alak_mai` helyesírási eltérése az alak elejére vihető (*setétségben → sötétségben*, *kivül → kívül*, *vajjon → vajon*, *miképen → miképpen*) — **a tábla egyértelmű** |
| `igealak_gyakori` | 329 | 12 806 | régies jegy, a 200 leggyakoribb kisbetűs jegyes alak (DT140: itt a jegy megbízható) — **szabály** |
| `regies_lista` | 15 | 5 589 | *vala*-, *lőn*-család, *vagyon* (a #94-ben jegy nélkül) — **szabály** (a *vala* tokenszinten, 1.3) |
| `lemmavaltas` | 165 | 10 980 | a `szotari_alak_mai` nem csak helyesírás (*ki → aki*, *mely → amely*, *e → ez*, *oh → ó*, *férfiú → férfi*, *leány → lány*, *cselekedik → cselekszik*) — **döntési kérdés** (DT-F96e), nem gépi csere |
| `regies_gyanu` | 754 | 4 975 | jegy nélküli, régiesnek látszó igealak — **LLM-jelölt** |
| `igealak_ritka` | 2 887 | 6 734 | régies jegy a ritka alakon (N-F94h: a jegy ~6%-ban hibás) — **LLM-jelölt** (brief .2/1) |
| `nem_elotag` | 0 | 0 | (helyesírási eltérés tőváltó alakon; a karakterszabály után nem maradt) |
| `tablan_kivul` | 683 | 1 044 | a token kisbetűsen sincs a táblában (kötőjeles alak része, tulajdonnév) — változatlan, a karakterszabály után |

**Összesítve (alak / token):**
- a #94 tábla vagy a determinisztikus szabály adja: 1 618 alak / 24 170 token (helyesírási osztályok, gyakori jegyes, régies lista);
- változatlan: 60 662 alak / 552 508 token (a `tablan_kivul`-lal);
- **LLM-jelölt: 3 641 alak (kisbetűsen 3 303) / 11 709 token** (`igealak_ritka` + `regies_gyanu`);
- döntési kérdés: 165 alak / 10 980 token (`lemmavaltas`).

A `regies_gyanu` bontása: a #94 által elemezetlen (szótári alak = alak) sor régies végződéssel és igei tővel 392 (*mondák, adák, találák, veték, találtaték, megharaguvék*), a kivételtábla jegy nélküli, a szótári alaktól eltérő sora 228 (*tőn, vőn, jőnek*), *-nd-* jövő 101 (*mondándok*), igei tő + régies végződés 32 (*állának*), *jő* 1. A gyanú-heurisztika (igei tő: a tő + *-ni/-ani/-eni/-tt/-ott/-ett/-ött* a korpuszban, vagy a szótári alaknak van jegyes sora) **alsó becslés**: a maradék régies igealak aránya a .2 lefedettségi mérésében mérendő; a hamis pozitívok (*halál, hajlék, nyilván, követe*) az LLM-en mennek át változatlanként.

**Megfigyelés a #94 értékkészletéről (manual, javítás nélkül):** a `regies_jegy` értékkészletében (SEMA 2.27) nincs tárgyas T/3 (*-ák/-ék*: *mondák, adák, találák, elhozák*): ezek a táblában elemezetlenül, jegy nélkül állnak (`modszer=lexikon`, szótári alak = alak), és csak a gyanú-heurisztika fogja meg őket. A *vévén* szótári alakja *véve*, a *kivűl* mai alakja *kivül* (a #94 tábla hibái; a #94 lezárt, a modernizálás a saját szabályával kezeli). Tétel: N-F96b.

### 1.3 Tokenszintű, szövegkörnyezetfüggő esetek

Ugyanabból a futásból (`fedettseg.py`), heurisztika (manual):

| eset | darab | megjegyzés |
|---|---:|---|
| *vala / valának* segédigei (előtte igei alak) | 2 239 | → elhagyva, a kieső token jelölve; az előtte álló ige múlt időbe (*lebeg vala → lebegett*) |
| *vala / valának* létigei | 2 509 | → *volt / voltak* |
| „a” + *ki-* különírt vonatkozó névmás | 5 267 | → *aki-* (két token egy szóvá: az „a” kieső tokenként jelölve) |
| „a” + *mely-* | 2 831 | → *amely-* |
| „a” + *mi-* | 1 260 | → *ami-*; további 543 eset a birtokos „a mi (Istenünk)” gyanúja (a következő szó nagybetűs vagy -nk végű): bizonytalan |
| jegyes *-ék/-ák* alak (mult.E1 / mult.T3 tárgyas alakilag egyezik, napló 16.) | 549 alak / 2 207 token | a modern alak versenként más lehet (*láték → láttam* vagy *látták*): szövegkörnyezetfüggő |
| *reá*-család (*reá, reám, reátok, reánk …*) | 640 token | a DT128 nem nevezi; *reá → rá* helyesírás-e: DT-F96e |

A *vala* segédigei / létigei aránya a DT128-ban idézett `pardes.db`-mérés (2 874 segédigei) közelében, de a heurisztika itt az előző token igeiségét nézi, a szórend (*vala* az ige előtt) nincs benne; a pontosság a .2 felhasználói mintáján mérendő.

### 1.4 Korpusz-támasz a jegyes alakokra (döntési opcióhoz)

`python eszkozok/karoli_modern/korpusz_tamasz.py` (`scope=a jegyes kisbetűs alakok (2 816) | forras=adat/karoli_modern/fedettseg_alakok.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-24T11:36Z`): a jegy szerinti szabályos mai alak-jelöltek (a szótári alak tövéből, *-ta/-tta/-otta*, *-t/-ott*, *-tak/-ták* …; kézi lista) közül hány szerepel magában a Károliban.

| osztály | pontosan egy jelölt a korpuszban | több | egy sem |
|---|---:|---:|---:|
| `igealak_gyakori` (195 kisbetűs) | 119 | 36 | 40 |
| `igealak_ritka` (2 621 kisbetűs) | 1 087 | 177 | 1 357 |

A korpusz-támasz a jegyhibát nem szűri: a főnévi *követe* (követ ’küldött’ birtokos) szabályos „mai alakja” *követte*, és ez szerepel a korpuszban. Ezért a korpusz-támasz a -t/-tt választást segíti, a jegy helyességét nem igazolja.

## 2. F96.0/3 — token-mérés a ~200 alakos mintán

`scope=200 alakos rétegzett minta az LLM-jelölt maradékból (3 303 kisbetűs alak: igealak_ritka 2 621, regies_gyanu 682; mag 20261024) | forras=adat/karoli_modern/fedettseg_alakok.tsv + konkordancia/Karoli_1908.tsv; modell: claude-sonnet-5-5 (Anthropic API, nem Batch, adaptive thinking, effort=low) | ts=2026-10-24T11:32:48Z–2026-10-24T11:33:14Z` — `python eszkozok/karoli_modern/token_minta.py --futtat`; a hívásnapló (usage mezők): `adat/karoli_modern/token_minta_hivasok.jsonl`; a válaszok: `adat/karoli_modern/token_minta.tsv` (modell-kimenet, `modell_ellenorizetlen`; mérési melléktermék, nem a kiadott réteg).

A prompt alakonként: alak, a #94 szótári alakja, és az első vers, amelyben az alak áll (szövegkörnyezet a tárgyas/alanyi döntéshez); 4 kérés × 50 alak; az utasítás a DT128 szintjét írja le (a promptszöveg a szkriptben).

| köteg | bemenet | kimenet |
|---|---:|---:|
| 1 | 5 011 | 1 137 |
| 2 | 5 365 | 1 233 |
| 3 | 5 615 | 1 369 |
| 4 | 5 326 | 1 442 |
| **összesen** | **21 317** | **5 181** |

**Alakonként 132,5 token** (106,6 bemenet + 25,9 kimenet; a gondolkodás tokenje 0). A kérés költsége a normál áron (2 / 10 USD/MTok, a `eszkozok/karoli_strong/api_koteg.py` szerint) kb. 0,09 USD.

**Vetítés:**

| változat | alak | token | a 0,2 M-hoz |
|---|---:|---:|---|
| (1) minden LLM-jelölt alak, verssel (a mért beállítás) | 3 303 | **≈ 437 600** | **meghaladja** |
| (2) a korpusz-támaszú (pontosan egy jelölt) ritka jegyes alak szabállyal; LLM a többire (177 + 1 357 + 682) | 2 216 | ≈ 293 600 | meghaladja |
| (3) minden jegyes alak szabállyal; LLM csak a `regies_gyanu` és a „több jelölt” ritka alak | 859 | ≈ 113 800 | alatta |
| + a tokenszintű, szövegkörnyezetfüggő esetek LLM-mel (2 207 *-ék/-ák* + 543 „a mi” token, ugyanilyen alakonkénti költséggel) | 2 750 | ≈ 364 000 | — |

A brief becslése (~0,05–0,2 M) az (1)-es változatban **túllépve** (0,44 M; a tokenszintű esetekkel együtt ~0,8 M), a teljes LLM-átírás ~3–3,5 M-jának így is kb. negyede. A brief .0/3 szerint itt megállás: ⛔ DT-F96d.

**Minőségi megfigyelések a mintán (modell-kimenet, a felhasználó még nem ellenőrizte):** 194 sor `biztos`, 6 `bizonytalan`; a 41 `regies_gyanu` sorból 27-et írt át (*mondák*-típus → *-ták*, *-teték → -tetett*, *-vén → -ve*), 14-et hagyott változatlanul mai alakként (*elvesznek, hullák, karaván*) — a gyanú-heurisztika hamis pozitívjai. A jegyhibát elkapta (*követe*: főnév). **Szókincs- és alakhiba is van:** *megnevekedék → megszaporodott* (szókincscsere, a DT128 tiltja), *lennék → legyek* (a feltételes mód mai alak), *őrizénditek → őrizendőtök* (nem létező alak), *ráküldé → rákűldte* (helyesírási hiba), *keltének* változatlanul. Következmény: az LLM-kimenet elé determinisztikus **tő-őr** kell (a modern alaknak az igető, illetve a szótári alak mai alakjának betűsorát kell hordoznia; ami nem, az `bizonytalan`, felhasználói sorba), ez a .2 része.

## 3. Nyitott a .1 előtt — állapot a .1 indulásakor

- DT-F96d 🟢: a keret emelve (≈ 0,45 M), az LLM-es maradék az előfizetésből (Claude Code), API nélkül; tő-őr kötelező. A .1 nem használ LLM-et (0 token).
- DT-F96e 🟢: (a) a lemmaváltások maradnak; (b) *reá → rá* igen (.1); (c) *-ván/-vén* igen (.2); (d) *-jék*: a .1 mintája dönt (4.5).
- DT-F96f 🟢: a réteg nem tárol Strongot; token-kulcs (vers-kulcs + `tokenizal`-sorszám).
- N-F96b: a *kivűl* és a további megfigyelt táblahibák a .1 kivételtáblájában (4.2); a *vévén* a .2-ben.
- A Hunspell hu_HU (DT301): 4.1 (a pótló menet: futott, 4.1.3–4.1.5).

## 4. F96.1 — helyesírási lépcső

`scope=a Károli 1908 minden verse (31 158) és tokenje (599 367) | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py | ts=2026-10-24T13:36Z` — `python eszkozok/karoli_modern/helyesiras.py --minta`; determinisztikus, LLM és API nélkül (**0 token**). Kimenet (generált, `# GENERÁLT:` fejléccel): `adat/karoli_modern/helyesiras_alakok.tsv` (a szövegkörnyezet nélkül változó alakok), `adat/karoli_modern/helyesiras_tokenek.tsv` (a változó, kieső vagy bizonytalan tokenek, vers-kulccsal és `tokenizal`-sorszámmal, DT-F96f), `adat/karoli_modern/helyesiras_minta.tsv` (4.4). Ez a .1 köztes kimenete, nem a .3 kiadott rétege.

### 4.1 Hunspell hu_HU (DT301): fejlesztési mérce, futott

*Előzmény: a .1 első menetében (2026-10-24, 13:36Z előtt) a Hunspell nem futhatott, mert a GitHub és a PyPI felé a hálózati szabály `connect_rejected` választ adott; a `helyesiras_alakok.tsv` fejléce és a DT-F96h szövege ezt az állapotot rögzíti. A mérést ugyanazon a napon, egy hálózattal futó menet pótolta (4.1.1–4.1.5).*

**A DT301 szerint csak fejlesztési mérce.** A Hunspell-ítélet a szabályok ellenőrzésére szolgál. A `helyesiras_alakok.tsv`, a `helyesiras_tokenek.tsv` és a `helyesiras_minta.tsv` alakjai és `tamasz` oszlopa **nem változtak**. A szótárfájlok nem kerültek a repóba: a repón kívül, a session scratchpadjében vannak, a kimenet csak a sha256-jukat és a forrás-URL-t rögzíti.

#### 4.1.1 Forrás és licenc (playbook 2. pont)

`scope=LibreOffice/dictionaries, hu_HU/ (hu_HU.aff, hu_HU.dic, README_hu_HU.txt, description.xml) | forras=https://raw.githubusercontent.com/LibreOffice/dictionaries/67032ee957631908098a72edf48dc81cac27e369/hu_HU/<fájl> (a master HEAD-je a lekéréskor, `git ls-remote`) | ts=2026-10-24T15:57:55Z`

| fájl | bájt | sha256 |
|---|---:|---|
| `hu_HU.aff` | 2 316 267 | `f3a2748dd535cfde2142ab17d0f7f8e4787b03fb25a60829c69ac8d493db4802` |
| `hu_HU.dic` | 1 786 144 | `97293d670ad4a3b8e7eebef7e25c6e8e939b914c64b6b4672b2bf416b768f990` |
| `README_hu_HU.txt` | 1 190 | `52b17fc3d53b6935eab747a71894507d702f7f0fde379c819c16cc803005fc84` |
| `description.xml` | 839 | `049d1c6cac167cce2fe18638c35ecfacea72c78337803bae2aede146a879c6ee` |

A `hu_HU/` könyvtárban külön licencfájl nincs: a `LICENSE`, a `COPYING` és a `license.txt` lekérése 404-et adott. A README a `COPYING.LGPL`-re és a `COPYING.MPL`-re a forrásfa gyökerében hivatkozik; ezeket ez a menet nem kérte le.

A licenc **szó szerint**, a `README_hu_HU.txt`-ből (UTF-8):

> Magyar Ispell helyesírási szótár – 1.9 szótárállományok morfológiai adatokkal
>
> A szótárállományok a LibreOffice projekt részeként a következő nyílt forráskódú
> licencek bármelyike alapján szabadon felhasználhatóak, de mindenféle garancia nélkül:
>
> MPLv2 vagy LesserGPLv3+
>
> (c) Németh László és Godó Ferenc, 2025
>
> Honlap: http://magyarispell.sf.net
>
> ------------------------------------------------------------------------------
>
> Hungarian Hunspell dictionaries version 1.9 with morphological data
>
> These files are part of the LibreOffice project.
>
> License: MPLv2 and LesserGPLv3+
>
> The contents of this software may be used under the terms of
> the GNU Lesser General Public License Version 3 or later (the "LGPL",
> see COPYING.LGPL) or the Mozilla Public License Version 2.0 or later
> (the "MPL", see COPYING.MPL in the root folder of the source tree).
>
> Software distributed under these licenses is distributed on an "AS IS" basis,
> WITHOUT WARRANTY OF ANY KIND, either express or implied. See the licences
> for the specific language governing rights and limitations under the licenses.
>
> 2025 (c) László Németh & Ferenc Godó
>
> Home: http://magyarispell.sf.net

A `hu_HU.aff` fejlécéből szó szerint (a megjegyzéssorok ISO-8859-2 kódolásúak, a szótár maga `SET UTF-8`):

> \# This dictionary is based on the Hungarian wordlist and affixes created
> \# by László Németh and Ferenc Godó, and it is covered by their original
> \# GPL/LGPL/MPL license as published by the FSF and Mozilla Foundation.
> \#
> \# Version: December 2025, 1.9

**Két eltérés a korábbi feltevéshez képest, jelzésként; nem jogi vélemény:**
1. A DT301 kérdése emlékezetből „MPL 1.1 / LGPL / GPL hármas licencet” feltételezett. A README szerint a licenc **MPLv2 vagy LGPLv3+** (a magyar szöveg szerint „bármelyike”), GPL nélkül.
2. A `hu_HU.aff` fejléce régebbi megfogalmazással „GPL/LGPL/MPL” licencet említ. A két fájl tehát nem egyezik. A fejlesztési mércét (DT301) ez nem érinti, mert a kiadott rétegbe semmi nem kerül a szótárból, ezért `licencek.tsv`-sor sem kell. A brief 2. szakasza szerint a kiadásba vételhez új licencdöntés kellene.

`description.xml`: `version value="2023.05.22"`, kiadó: FSF.hu Alapítvány. A verziója eltér a README-ben és az `.aff`-ban álló 1.9-es verziótól (2025-12); ezt a mérés nem vizsgálta.

#### 4.1.2 A futtató

- **Hunspell 1.7.2** (`https://github.com/hunspell/hunspell`, tag `v1.7.2`, commit `2969be996acad84b91ab3875b1816636fe61a40e`, klón: 2026-10-24). A könyvtár licence MPL 1.1 / GPL 2.0 / LGPL 2.1. A forrás nem került a repóba.
- Az `apt` nem érte el a csomagtárat (DNS). A `pip install hunspell` / `cyhunspell` csomagot nem lehetett telepíteni (a PyPI a `no_proxy`-n áll, DNS nélkül; a proxyn át letöltött `cyhunspell` buildje elbukott). Az `autoreconf`-hoz hiányzik az `autopoint`, ezért a CLI nem fordult le. Helyette a könyvtár forrásából egy saját, kis futtató fordult: `eszkozok/karoli_modern/hunspell_driver.cxx`. Ez soronként egy szót olvas, a `Hunspell::spell` ítéletét adja vissza, és csak mérési célra, `--suggest` kapcsolóval, legfeljebb 3 javaslatot is. Fordítás:
  `g++ -O2 -std=c++11 -DHUNSPELL_STATIC -I<hunspell>/src/hunspell eszkozok/karoli_modern/hunspell_driver.cxx <hunspell>/src/hunspell/{affentry,affixmgr,csutil,filemgr,hashmgr,hunspell,hunzip,phonet,replist,suggestmgr}.cxx -o hs_check`
- A mérő szkript: `python eszkozok/karoli_modern/hunspell_meres.py --futtato <hs_check> --aff <hu_HU.aff> --dic <hu_HU.dic>`. Az útvonalak a repón kívül vannak, és csak argumentumként mennek át. A kimenet: `adat/karoli_modern/helyesiras_hunspell.tsv`, generált, `# GENERÁLT:` fejléccel. Alakpáronként rögzíti a `hunspell_1908`, a `hunspell_modern` (`elfogad`/`elutasit`) és a `hunspell_itelet` oszlopot. **Ez az ítélet-oszlop a `modell_ellenorizetlen` jelölés frissítése; a `tamasz` oszlop maga nem változik.**
- Próba: *harminc, királlyal, sötétség, neki, akik, amellyel* elfogadva; *harmincz, királylyal, melylyel, atyjok* elutasítva. A *setétség* viszont elfogadva: a szótár a régies alakot is ismeri (4.1.4).

#### 4.1.3 Eredmény

`scope=a helyesiras_alakok.tsv mind az 1 377 alakja + a helyesiras_tokenek.tsv 146 további, szövegkörnyezetfüggő alakpárja (nem kieső, változó; zömmel nevmas) = 1 523 alakpár, 2 988 szó | forras=adat/karoli_modern/helyesiras_alakok.tsv + helyesiras_tokenek.tsv; Hunspell 1.7.2 + LibreOffice hu_HU 1.9 (67032ee9) | ts=2026-10-24T16:01Z` — determinisztikus, LLM nélkül (**0 token**).

Ítélet a pár két alakjából. `megerosit`: a modern alak elfogadva, az 1908-as elutasítva. `semleges`: mindkettő elfogadva. `cafol`: a modern elutasítva, az 1908-as elfogadva. `ismeretlen`: mindkettő elutasítva. Az alábbi számok alak / token formában értendők, a token az 1908-as alak korpuszgyakorisága.

| `tamasz` | alak | megerősít | semleges | ismeretlen | cáfol |
|---|---:|---:|---:|---:|---:|
| `modell_ellenorizetlen` | **1 093** | **824 / 2 348** | 20 / 39 | 246 / 442 | **3 / 5** |
| `szoto_94` | 177 | 138 / 1 018 | 13 / 51 | 26 / 65 | 0 |
| `korpusz` | 106 | 84 / 424 | 13 / 2 295 | 9 / 107 | 0 |
| `manual` | 1 | 1 / 4 | 0 | 0 | 0 |
| **alakok összesen** | 1 377 | 1 047 / 3 794 | 46 / 2 385 | 281 / 614 | 3 / 5 |
| tokenek (szövegkörnyezetfüggő) | 146 | 4 / 269 | 141 / 10 942 | 0 | 1 / 1 |

Szabályonként, az alakok táblájában:

| szabály | megerősít | semleges | ismeretlen | cáfol |
|---|---:|---:|---:|---:|
| `karakter` | 847 | 16 | 244 | 3 |
| `szoto_94` | 138 | 13 | 26 | 0 |
| `szotag` | 52 | 5 | 4 | 0 |
| `rea` | 9 | 10 | 7 | 0 |
| `neki` | 0 | 2 | 0 | 0 |
| `kivetel` | 1 | 0 | 0 | 0 |

A `modell_ellenorizetlen` 1 093 alakjából tehát **824 alakot (2 348 token) a Hunspell alátámaszt**. 20 alakon nem dönt, mert a régi alakot is elfogadja; 246 alakon nem dönt, mert a modernt sem ismeri; 3 alakon cáfol.

#### 4.1.4 A tipikus elutasítások és a Hunspell korlátai

A 285 elutasított modern alakot (`ismeretlen` + `cafol`) heurisztika sorolta be, mérési célra, a scratchpadben. A javaslat (`suggest`) csak itt, a naplóban szerepel, és nem kimeneti alak.

- **Nagybetűs, zömmel tulajdonnév: 182 alak** (*Acmonig, Bocra, Cefon, Ciklág, Cilicia …*). A kisbetűsítve újrapróbált alakok egyikét sem fogadja el a Hunspell, tehát nem mondatkezdő közszavakról van szó. A *cz → c* a tulajdonneveken a Hunspellel nem ellenőrizhető.
- **Régies igealak, a .2 dolga: kb. 32 alak** (*harcola, harcolának, szülé, leüle, körülmetélé, növekedének, ráveté*). A helyesírási csere maga helyes, az elutasítás oka az igealak. Hasonló a *-jok/-jök* birtokos T/3 (8 alak, 101 token: *rájok* 88, *orcájok-*, *utcájokon*): a Hunspell csak a *-juk/-jük* alakot ismeri (*rájuk, orcájukat*). Ez a DT-F96g-hez adat, nem döntés.
- **Összetett számnevek: kb. 18 alak** (*harmincezeret, kétezernyolcszáztizenkettő, száznyolcvanötezeret*). A Hunspell a hosszú számnév-összetételt nem ismeri, ez a szótár korlátja. Megfigyelés: a mai helyesírás (AkH. 12., 2000 fölött kötőjel: *kétezer-nyolcszáztizenkettő*) kötőjelet kívánna, ez azonban tokenváltozás (K2), és a .1 nem kezeli.
- **Régi helyesírású vagy alakú közszó, amelyet a szabály nem fed le** (*cerimóniákat → ceremóniákat, kálcédon → kalcedon, skárlátcikkeket → skarlát-, pőröllyel → pöröllyel, sudarcédrussal → sudár-, köröskörül → körös-körül, kívánatosb*): a karaktercsere után maradó eltérés. Lemma- vagy alakváltás, a DT-F96e (a) szerint nem e lépcső dolga. A *körös-körül* kötőjeles, tehát tokenváltozás volna.
- **A semleges eset a Hunspell korlátja.** A szótár sok régies alakot elfogad: *néki* (1 734 token), *reá, reám, reád*, *setétség* és ragozott alakjai, *arczára, válaszszák, harmincz* (*Harmincz*), *paizsos*. Ezeken a Hunspell nem dönt. A régi alak elfogadása nem cáfolja a szabályt, de alá sem támasztja. A *néki → neki* és a *reá → rá* forrása a DT128 és a DT-F96e (b), tehát felhasználói döntés.
- **A szövegkörnyezetfüggő összevonás** (`nevmas`: *a kik → akik*) szóalakon nem mérhető. A *kik* és az *akik* is helyes szó, ezért a pár 141 esetben semleges; a döntést a minta hozza.

#### 4.1.5 Amit a Hunspell cáfol vagy hibának mutat (nem javítva, jelzés)

A szabályok és a kimeneti táblák **nem változtak**. A javítás szabálydöntés, a .1 ⛔ mintája után.

1. **`karakter` (nyny → nny) összetételi határon: cáfolat.** *keménynyakú → keménnyakú* (3 token), *Keménynyakú* (1), *keménynyakúak* (1): összesen 3 alak, 5 token. A Hunspell a régi alakot elfogadja, a modernt elutasítja, első javaslata *keménynyakú*. Az AkH. szerint az összetételben a kettős betű nem egyszerűsödik (*kemény + nyakú*). A szabály tehát az összetételi határon hibás: a modern alak a változatlan *keménynyakú*. A többi *nyny/gygy/cscs/lyly/szsz* csere (201 alak) a Hunspell szerint helyes (*aranynyal → arannyal, egygyé → eggyé, öcscse → öccse*).
2. **Szabálysorrend-hiba: `karakter` a `szotag` előtt.** *paizszsal → paizzsal* (7 token): a *zszs → zzs* csere után a *paizs → pajzs* szabály már nem illeszkedik, így félig modern alak jön létre. A Hunspell mindkét alakot elutasítja, és a *pajzzsal*-t javasolja. Nem cáfolat (`ismeretlen`), de valódi generátorhiba.
3. **`karakter` (cz → c) szóvégi kettőzéssel: cáfolat jellegű.** *strucz → struc* (3), *struczok → strucok* (3), *struczmadarak, struczmadár, struczmadárnak* (4): 5 alak, 10 token. A Hunspell a *struc*-ot elutasítja, és a *strucc*-ot javasolja. A mai alak *strucc* (AkH.), a mechanikus *cz → c* itt rossz modern alakot ad. A régit sem fogadja el, ezért a besorolás `ismeretlen`.
4. **`nevmas:hatarozo`, *a minemű → aminemű* (1Krón 17:8, 1 token).** A Hunspell az *aminemű*-t nem ismeri, a *minemű*-t igen (`cafol`). Gyenge jelzés: az *aminemű* régies, de létező vonatkozó névmás, így a hiány valószínűleg a szótár korlátja. A mintán dönthető.
5. **`szotag`, *paizst → pajzst* (18 token) és *dícséréd → dicséréd*.** A Hunspell elutasítja őket: a mai alak *pajzsot*, illetve *dicséred*. A helyesírási csere helyes, az eltérés alaktani, tehát nem a .1 dolga.

**Összegzés a szabályokra:** a Hunspell a `modell_ellenorizetlen` alakok 75%-át (824 / 1 093) alátámasztja. Egy szabályt cáfol egy szűk esetben: a `karakter` nyny → nny cseréje összetételi határon (5 token). Egy szabálysorrend-hibát (7 token) és egy szóvégi *cz → cc* esetet (10 token) mutat meg. A többi elutasítás a tulajdonnév, a .2-es igealak, a *-jok* és a szótár korlátja. A javítás (kivétel a *keménynyakú*-ra, a *paizs* sorrendje, *strucc*) a .1 ⛔ után, a felhasználói mintával együtt dönthető.

### 4.2 Szabályok és darabszámok

| szabály (`szabaly`) | forrás (`szabaly_forras`) | token | példa |
|---|---|---:|---|
| `nevmas` — „a” + vonatkozó névmás / határozószó egybe | DT128, N-F94f | 11 212 összevonás | *a kik → akik*, *a melylyel → amellyel*, *a mint → amint*, *a hol → ahol*, *a hogy → ahogy* |
| ebből `nevmas:ki` / `:mely` / `:mi` / `:hatarozo` | | 5 311 / 2 903 / 1 338 / 1 660 | |
| `karakter` | manual (helyesírás-történet) | 3 101 | *harmincz → harminc*, *királylyal → királlyal*, *gonoszszal → gonosszal* |
| `neki` | DT128 | 1 738 | *néki → neki* |
| `szoto_94` — a #94 mai szótári alakjának helyesírási eltérése | #94 | 1 134 | *miképen → miképpen*, *kivül → kívül*, *vajjon → vajon*, *közűl → közül*, *nevekedik → növekedik* |
| `rea` | DT-F96e b | 661 | *reá → rá*, *reájok → rájok*, *reáköltesz → ráköltesz* |
| `szotag` | manual | 160 | *dícsér- → dicsér-*, *paizs → pajzs* |
| `kivetel` | N-F96b | 4 csere | *kivűl → kívül* (a #94 tábla: *kivül*); változatlan marad a *gyűl-*, *egybegyűl-*, *összegyűl-*, *dűl-*, *ledűle*, *jóhiszeműleg* (a tábla mai alakja ott hibás: *gyül*, *dül*) |

Összesen: **12 804 vers változik** (a 31 158-ból), **28 953 token** (ebből 11 212 kieső „a”), **1 377 alak** szövegkörnyezet nélkül. Az alakok `tamasz` oszlopa: `szoto_94` 177, `korpusz` 106 (a modern alak a Károliban is áll), `manual` 1, **`modell_ellenorizetlen` 1 093** (zömmel a `karakter` cseréi: a *cz*-s alakok modern párja a Károliban nem fordul elő; Hunspell nélkül ez a mintán mérhető; a Hunspell-ítélet: 4.1.3).

**Nem változik a .1-ben (szándékosan):** a lemmaváltás (DT-F96e a: *e, oh, férfiú, leány, mostan, minekutánna*, az önálló *kik/mely*); minden igealak (*teremté, monda, -ván/-vén, vala, lőn, vagyon*: .2); a *-jék* és a *-jok/-jök* (4.5).

**Az „a mi” kezelése (heurisztika, manual; a DT-F96i előtti állapot, felváltotta a 4.6).** Toldalékos *mi-* (*mit, minek, mire*) mindig összevonva. A puszta „a mi”: ha a következő szó *-nk* birtokos (*a mi Istenünk, a mi atyánk*) → birtokos, marad (`mi_birtokos_marad`); ha a következő szó nagybetűs, személyes névmás (*nékünk, minket*), vagy írásjel követi → `bizonytalan`, változatlan (**298 token**; ezek a mintában is szerepelnek); különben → *ami*. Egy „a Ki…” nagybetűs vers közbeni eset `nagybetu`, változatlan.

### 4.3 K2 önellenőrzés

A generátor minden versen ellenőrzi, és eltérésnél megáll: a modern versszöveg újratokenizálva pontosan a nem kieső tokenek modern alakjait adja, sorrendben; a nem-betű váz (írásjel, szóköz) csak az összevonások egy-egy szóközével rövidebb. A futás 31 158 versen hiba nélkül ment át. (Ez a generátor saját ellenőrzése, nem a független ellenőré.)

### 4.4 A minta (⛔ felhasználói ellenőrzés)

`adat/karoli_modern/helyesiras_minta.tsv` — rögzített mag (20261024), rétegzett, **112 vers**, egy vers egy rétegben:

| réteg | vers | mit ellenőrizz |
|---|---:|---|
| `karakter` | 14 | a *cz/lyly/szsz …* csere |
| `neki` | 8 | *néki → neki* |
| `szoto_94` | 14 | a #94 tábla átvitele (*kívül, vajon, miképpen, sötétség, növekedik*) |
| `rea` | 8 | *reá → rá* |
| `nevmas:ki`, `nevmas:mely`, `nevmas:mi`, `nevmas:hatarozo` | 10 + 10 + 8 + 8 | az összevonás (*akik, amely, ami, amint, ahol, ahogy*) |
| `mi_birtokos_marad` | 4 | a „mi” birtokosként jogosan maradt-e |
| `bizonytalan` | 4 | a változatlanul hagyott „a mi”: *ami* vagy birtokos |
| `kivetel_szotag` | 4 | az N-F96b kivétel és a *dics-/pajzs* |
| `jek` | 8 | a *-jék* felszólító E/3: az `alternativa` oszlop a *-jon/-jen/-jön* változat (DT-F96e d) |
| `jok` | 6 | a *-jok/-jök* birtokos T/3: az `alternativa` oszlop a *-juk/-jük* változat (DT-F96g) |
| `valtozatlan` | 6 | nem maradt-e ki régi helyesírás (a Hunspell helyett) |

Oszlopok: `szoveg_1908`, `szoveg_modern` (a .1 kimenete), `valtozasok` (`sorszám:régi→új`; `(összevonva)` = kieső „a”; `?(…)` = bizonytalan, változatlan; `=(…)` = szándékosan marad), `alternativa` (csak a `jek`/`jok` sorokon). **Az `ellenorzes` és a `megjegyzes` oszlopot a felhasználó tölti** (javasolt értékek: `jó` / `hibás`; a `jek`/`jok` sorokon `A` = a `szoveg_modern`, `B` = az `alternativa`); a mérés csak a kitöltött sorokon fut. Az igealak (*monda, vala, lőn*) e lépcsőben szándékosan régi: nem hiba.

**A K1 küszöbe** (brief .1/3, K1) a mérés előtt rögzítendő: DT-F96h.

### 4.5 Döntésre váró, a mintán eldöntendő

- **DT-F96e (d)** *-jék* felszólító E/3 az *-ik*-es igéken (*cselekedjék, uralkodjék, lakozzék, igyék*): **93 alak, 417 token** (heurisztika: a szótári alak *-ik*-re végződik, a tő önálló szóként nem áll a korpuszban, így a tárgyas T/3 *megismerjék* kimarad). Az alternatíva hangrendje: *-jon/-jen/-jön*; csak *i/í* magánhangzós tőnél *-on* (*igyék → igyon*).
- **DT-F96g** (új) *-jok/-jök* birtokos T/3 (*atyjok, reájok, hozzájok, útjokat, erejök*): **212 alak, 714 token** a *j*-s változaton (kizárva a többes számú *tolvajok, bajok, tutajok-*). A *j* nélküli változat (*kezöket, szívök, közöttök*) a .1-ben nem mért: a *-ok/-ök* többes számmal egybeesik, gépi szétválasztása szövegkörnyezetfüggő.

### 4.6 Az „a mi”-szabály (DT-F96i; a 4.6.1–4.6.3 a kísérleti mérés, a 4.6.4 az alkalmazás)

`scope=a Károli 1908 minden puszta „a mi” tokenje (1 164: „a” + „mi”, szóközzel, toldalék nélkül) | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py (sha256:7295d5569705) | ts=2026-10-24T17:46Z`. A futtatás: `python eszkozok/karoli_modern/helyesiras.py --ami-proba`. Determinisztikus, LLM és API nélkül (**0 token**). Kimenet: `adat/karoli_modern/helyesiras_ami_proba.tsv`, generált, `# GENERÁLT:` fejléccel. Soronként egy token: `igehely`, `sorszam` (a „mi” `tokenizal`-sorszáma), `elozo`, `kovetkezo`, `dontes_regi`, `dontes_kiserleti`, `kriterium`, `valtozik`. **Ez nem a kiadott réteg.** A `helyesiras_alakok.tsv`, a `helyesiras_tokenek.tsv` és a `helyesiras_minta.tsv` nem változott. Ellenőrzés: a kapcsoló nélküli futás a repón kívülre generálva, a fejlécsor nélkül, bájtra azonos a három táblával. A három tábla fejléce viszont a szkript előző sha256-ját hordozza (`c0b30137c31b`), mert a kiadott réteget a döntés előtt nem generáltam újra.

**Előzmény.** A felhasználó vizsgálata (chat, 2026-10-24, az orkesztrátoron át; ezeket a darabszámokat nem ez a menet kérdezte le): a Károli 1908-ban a vonatkozó névmás különírt alakban áll (*a mi* 1 164, *a ki* 2 592, *a kik* 1 756, *a mely-* 2 909). Egybeírva csak *ami* 2, *akik* 6 és *amely-* 13 fordul elő. A puszta *a mi* 1 164-es darabszámát ez a menet is megkapta. A felhasználó példái: vonatkozó a 3Móz 11:42, az 1Thessz 5:21, a Neh 9:6 és a 2Móz 23:11; birtokos a Sir 5:2, a 4Móz 36:3, az 5Móz 21:7 és a Róm 5:21. A javasolt támpontokat a felhasználó még nem hagyta jóvá: birtokos, ha a *mi* után *-ünk/-unk/-ink/-eink* végű birtokos főnév áll; vonatkozó, ha előtte vessző, *mindazt/mindent/semmit* vagy ige áll, utána ige vagy melléknév.

#### 4.6.1 A kísérleti szabály

Sorrend: az első illeszkedő támpont dönt. A kód: `ami_proba_keszit`.

| kritérium | feltétel |
|---|---|
| `B1_nk_utana` → birtokos | a következő szó *-nk* birtokos főnév, minden esetraggal (`NK_PROBA`), az összetett *atyánkfia-* család is; nagybetűs főnéven is (*Istenünk, Urunk*). Nem az a ragos személyes névmás (*nékünk, velünk, minket*). A *magunk*-család igen (*a mi magunk lelkét*). |
| `B2_nk_masodik` → birtokos | a második szó ilyen, szóközzel, és az első nem ige (*a mi mindennapi kenyerünket, megtartó Istenünknek*) |
| `V1_irasjel_elotte` → vonatkozó | az „a” előtt vessző, pontosvessző vagy kettőspont áll |
| `V2_mindazt_elotte` → vonatkozó | előtte *mindazt/mindent/semmit* áll, írásjel nélkül |
| `V3_ige_elotte` → vonatkozó | előtte ige áll, írásjel nélkül |
| `V4_ige_utana` → vonatkozó | utána ige áll |
| `nincs_tampont` | a régi `bizonytalan` marad (változatlan) |
| `regi_szabaly` | a régi döntés marad (a régi vonatkozó *ami* lesz) |

Az ige: a #94 tábla `regies_jegy`-e vagy a `fedettseg.igei_tovek` próbája a szótári alakon (manual heurisztika).

**Eltérések a javaslattól, mind a mért adatból:**
1. **A birtokos-támpont a vessző elé került.** A kísérleti birtokosok közül **179** előtt írásjel áll (*az Úr, a mi Istenünk*; 44 a régi birtokosokból, 120 a régi bizonytalanokból, 15 a régi vonatkozókból). Fordított sorrendben a vessző-támpont mind a 179-et *ami*-vé vonná össze.
2. **A *-nk* minden birtokos személyjelre áll**, a *-ánk/-énk/-ónk* alakra is (*Atyánk, Kősziklánk, Megtartónk*), nem csak az *-ünk/-unk/-ink/-eink* alakra.
3. **Új támpont a második szón álló *-nk* (B2).** A javaslat „utána melléknév → vonatkozó” támpontja éppen ezeken az eseteken hibázna (*a mi mindennapi kenyerünket*).
4. **A melléknév-támpont nem fut.** A repó adata szófajt nem hordoz, ezért a melléknév nem ismerhető fel. Melléknév-találgatást nem tettem a helyére.

#### 4.6.2 Eredmény

| régi döntés → kísérleti | token | kritérium |
|---|---:|---|
| birtokos → birtokos | 377 | B1 377 |
| **bizonytalan → birtokos** | **282** | B1 281, B2 1 (*Jak 2:1 a mi Jézus Krisztusunkban*) |
| **bizonytalan → vonatkozó** | **9** | V1 9 (*mindabból, a mi Izráel fiaié*; *mindent, a mi Eliméleké volt*; *az, a mi velünk történt*) |
| **bizonytalan → bizonytalan** | **7** | nincs támpont |
| **vonatkozó → birtokos** | **93** | B1 71, B2 22 |
| vonatkozó → vonatkozó | 396 | V1 276, V2 2, V3 9, V4 14, régi szabály 95 |
| **összesen** | 1 164 | |

**A bizonytalan „a mi” 298-ról 7-re csökken.** 98 vers modern szövege változik: 102 token, 9 új összevonás és 93 visszavont összevonás. A 282 bizonytalan → birtokos csere a szöveget nem változtatja, csak a jelölést.

**A mai kiadott szabály hibái (a 93 „vonatkozó → birtokos”).** Ezeket a kísérlet tárta fel. A mai `NK` minta nem ismeri a *-nknak* (37), *-nkba/-nkbe* (10), *-nknál/-nknél* (4) végződést és az *atyánkfia-* összetételt (20). Az ilyen esetekben ma *ami*-t ad: *a mi atyáinknak → ami atyáinknak*, *a mi atyánkfiait → ami atyánkfiait*, *a mi szívünkbe → ami szívünkbe*. A második szón álló birtokost sem ismeri (22): *a mi mindennapi kenyerünket → ami mindennapi kenyerünket* (Mt 6:11, Luk 11:3). Mind a 93 sort egyenként átnéztem, és birtokosnak olvastam. **Ez modell-olvasat (`modell_ellenorizetlen`), nem felhasználói ellenőrzés.** A sorok a `helyesiras_ami_proba.tsv`-ben vannak, `valtozik=igen` értékkel.

**A 7 megmaradt bizonytalan** és a modell olvasata (értelmezés, nem döntés):

| igehely | | olvasat |
|---|---|---|
| 1Krón 24:20 | *A mi Lévi többi fiait illeti* | vonatkozó |
| Ján 3:6 | *és a mi Lélektől született* | vonatkozó |
| Róm 1:20 | *Mert a mi Istenben láthatatlan* | vonatkozó |
| 1Pét 3:21 | *A mi minket is megtart* | vonatkozó |
| 2Kor 7:14 | *a mi Titus előtt való dicsekvésünk* | birtokos |
| Józs 22:27 | *a mi utánunk való nemzetségeink* | birtokos |
| Róm 5:8 | *a mi hozzánk való szerelmét* | nem dönthető a sorból |

**Ismert maradék hiba a kísérleti vonatkozókban** (szkenneléssel: *-nk* szó 2–4 szón belül, írásjel nélkül; a scratchpadben, nem kimenet), ≈ 11 token birtokosnak olvasva. *Filem 1:1 a mi szeretett munkatársunknak* és *2Pét 3:15 a mi szeretett atyánkfia*: a *szeretett* igei alak, ezért a B2 nem fut. *2Kor 4:17 a mi pillanatnyi könnyű szenvedésünk*, *2Kor 7:12, 2Kor 9:3, 1Thessz 1:9, 1Thessz 2:1 a mi (ti) hozzátok való menetelünk*, *2Thessz 2:1*, *2Thessz 3:14*, *Tit 3:6*: a *-nk* a harmadik vagy negyedik szón áll, *való* szerkezettel. Ezek a mai kiadott rétegben is hibásak, a kísérlet nem rontja őket. Javításuk a B2 kiterjesztése volna (*való*, melléknévi igenév), ehhez új mérés kell.

#### 4.6.3 A minta és a Hunspell

- **A 112 soros minta** (`helyesiras_minta.tsv`, a fájl nem változott). A kísérlet **egy sor** modern szövegét változtatja: M079 (2Móz 9:4, `bizonytalan` réteg), *mindabból, a mi Izráel fiaié → mindabból, ami Izráel fiaié*. Ez a felhasználó vonatkozó példáinak (*mindent, a mi …*) mintája. Az M076, M077, M078 és M080 bizonytalan tokenje birtokosra vált; a szövegük nem változik. A `nevmas:mi` és a `mi_birtokos_marad` réteg sorai nem változnak. **Az `ellenorzes` oszlop üres**, ezért pontosság nem mérhető. A „nem ront” itt csak annyit jelent, hogy a minta egyetlen sora sem változik a felhasználói példák ellenében. A 93 visszavont összevonás közül egy sem esik a mintába, így azokat a minta nem méri.
- **Hunspell (DT301, csak mérce).** A kísérlet nem hoz létre új szóalakot. Az egyetlen szövegváltozó alakpár a *mi → ami* (9 token). Ez a `helyesiras_hunspell.tsv`-ben már `semleges`, mert a Hunspell mindkét alakot elfogadja. A visszavont összevonás a régi alakot (*a*, *mi*) adja vissza. A Hunspell a *mi* és az *ami* között szóalakon nem dönt, mert a különbség szövegkörnyezeti (4.1.4). Ezért nem futott újra; a szótárfájlok és a futtató ebben a sessionben nincsenek meg.

#### 4.6.4 Alkalmazva (DT-F96i 🟢, 1. opció)

**A felhasználó döntése:** 2026-10-24, chat: „Mehet a javaslat”. A 4.6.1 szabálya a kiadott .1 része lett, a `szabaly` oszlopban `ami:<kritérium>` címkével. A `--ami-proba` futás a DT-F96i előtti és a DT-F96i szerinti döntést veti össze, a kiadott réteget nem írja.

`scope=a Károli 1908 minden verse (31 158) és tokenje (599 367) | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py (sha256:555cf301c07a) | ts=2026-10-24` — `python eszkozok/karoli_modern/helyesiras.py --minta-frissit`, majd `--ami-proba`; 0 token.

| | DT-F96i előtt (4.2) | DT-F96i szerint |
|---|---:|---:|
| változó vers | 12 804 | **12 760** |
| változó token | 28 953 | **28 785** |
| kieső (összevont „a”) | 11 212 | **11 128** (−93 + 9) |
| `bizonytalan` „a mi” | 298 | **7** (és 1 `nagybetu`, változatlan) |
| változó alak (`helyesiras_alakok.tsv`) | 1 377 | 1 377 (a törzs bájtra azonos) |

A `helyesiras_tokenek.tsv`-ben csak a puszta „a mi” tokenjeinek sorai változtak: a döntés és a `szabaly` címke. Más sor nem változott (diff a futás előtti változattal).

**A minta (`helyesiras_minta.tsv`)** az új `--minta-frissit` kapcsolóval frissült. Ez megtartja a kiválasztást (`minta_id`, `reteg`, `igehely`) és a felhasználói oszlopokat (`ellenorzes`, `megjegyzes`; most üresek), és csak a `szoveg_modern`, `valtozasok`, `alternativa` oszlopot számolja újra. A régi `--minta` kapcsoló a DT-F96i óta más verseket választana, mert a `bizonytalan` réteg jelöltjei 298-ról 7-re fogytak. Ezért a minta így nem generálódott újra. Változott 5 sor, a `bizonytalan` réteg 4 sora és az M076:
- M076, M077, M078, M080: a bizonytalan „a mi” birtokosként jelölve (`=(birtokos, marad)`), a szöveg változatlan;
- M079 (2Móz 9:4): *mindabból, a mi Izráel fiaié → mindabból, ami Izráel fiaié*.

A `bizonytalan` réteg 4 sora így a DT-F96i döntéseit méri.

**Külön felhasználói ellenőrzés: `adat/karoli_modern/helyesiras_ami_ellenorzes.tsv`**, generált, 109 token:

| `tipus` | token | ellenőrizendő |
|---|---:|---|
| `osszevonas_visszavonva` | 93 | a DT-F96i előtt *ami* lett, most birtokos, marad *a mi* (*a mi atyáinknak, a mi mindennapi kenyerünket*) |
| `osszevonas_uj` | 9 | a DT-F96i előtt bizonytalan volt, most *ami* |
| `bizonytalan` | 7 | támpont nélkül, változatlan (a modell olvasata: 4.6.2) |

Oszlopok: `szoveg_1908`, `szoveg_modern_dt_f96i_elott`, `szoveg_modern`, `kriterium`. Az `ellenorzes` és a `megjegyzes` oszlopot a felhasználó tölti (`jó` / `hibás`; a `bizonytalan` sorokon `vonatkozó` / `birtokos`). Újragenerálásnál a kitöltött értékek megmaradnak (`igehely` + `sorszam` kulcson). Ezt a 112 soros minta nem fedi: a K1 küszöbét (DT-F96h) erre a fájlra is alkalmazni kell.

**Hunspell (DT301).** A `helyesiras_hunspell.tsv` fejléce a régi `helyesiras_tokenek.tsv` sha256-ját hordozza (`49fbf5d191c5`). Tartalmilag nem avult el: új alakpár nem keletkezett, a *mi → ami* pár benne van (`semleges`), és csak a darabszáma kisebb. Újrafuttatás nem volt, a futtató ebben a sessionben nincs meg.

**A 4.2 „Az „a mi” kezelése” bekezdése a DT-F96i előtti állapotot írja le; a kiadott réteg a 4.6.1 szerint jár el.**

### 4.7 Döntések a .1 ⛔ mérése előtt (felhasználó, 2026-10-24)

A felhasználó a modell javaslatát hagyta jóvá (chat: „Mehet”). A K1 küszöbe így **a mérés előtt** rögzült (brief K1). A minta és a generált táblák ebben a menetben nem változtak.

- **DT-F96h (K1) 🟢.**
  - **Egység:** a csere, vagyis a minta `valtozasok` tétele.
  - **Küszöb:** ≥ 98% helyes csere két külön halmazon: a 112 soros mintán (`helyesiras_minta.tsv`) és a `helyesiras_ami_ellenorzes.tsv` 102 szövegváltozó során (`osszevonas_visszavonva` + `osszevonas_uj`; legfeljebb 2 hibás).
  - **`valtozatlan` réteg:** 0 kihagyott régi helyesírás.
  - **Nem hiba:** a `jek`/`jok` sorok A/B választása és a 7 bizonytalan „a mi” besorolása (döntés).
  - **Küszöb alatt:** a hibás szabály javul, és csak az érintett sorok mérődnek újra.
- **DT-F96e (d) 🟢.** A *-jék* felszólító E/3 (93 alak, 417 token) **marad**. Élő, választékos alak (4.1.4: a Hunspell elfogadja), a DT-F96e (a) logikája szerint. A minta `jek` rétegén eltérő ítélet felülírja.
- **DT-F96g 🟢.**
  - **Változik:** a *j*-s *-jok/-jök → -juk/-jük* (212 alak, 714 token) a .1 szabálya. Gépileg egyértelmű, és a Hunspell a régi alakot elutasítja (4.1.4: *rájok*, *orcájok-*).
  - **Marad:** a *j* nélküli változat (*kezöket, szívök*).
  - A minta `jok` rétegén eltérő ítélet felülírja.
  - **Hátra van:** az alkalmazás (generátor-szabály, újragenerálás, a minta `--minta-frissit`-tel).

### 4.8 A DT-F96g alkalmazása, az átnézés és a K1 mérése

`scope=a Károli 1908 minden verse és tokenje; a minta 112 sora; a helyesiras_ami_ellenorzes.tsv 109 sora | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py | ts=2026-10-24` — `python eszkozok/karoli_modern/helyesiras.py --minta-frissit`, majd `--ami-proba`. Az átnézés és a mérés a scratchpadben futott, 0 token.

#### 4.8.1 DT-F96g alkalmazva

Új szabály, `jok` (`szabaly_forras`: DT-F96g): a *j*-s birtokos T/3 *-jok/-jök → -juk/-jük*, **212 alak, 714 token**. A szabály az alak minden más cseréje után fut, így a *reájok → rájok → rájuk* sor is teljesül. A 212 alakot egyenként átnéztem. A többes számra gyanús hat alak (*hajokat, ganéjokat, nyájok, nyájokat, zárjok, ujjokkal*) a versben mind birtokos (*a saját ganéjokat*, *az ő nyájok mellett*), többes számú főnév nincs köztük.

Új állapot: változó vers 12 760 → **13 083**, változó token 28 785 → **29 396**, változó alak 1 377 → **1 580**; a kieső tokenek száma 11 128, változatlan. A minta 9 sora frissült a `--minta-frissit` kapcsolóval (M039, M042, M061, M101–M106). A *j* nélküli változat (*kezöket, szívök*) marad.

#### 4.8.2 Az átnézés — a felhasználó a modellre bízta

**A felhasználó döntése** (chat, 2026-10-24): „Nézd át te. Elfogadom a döntést”. A két fájl `ellenorzes` oszlopát ezért a modell (claude-opus-5-5) töltötte ki. Minden sor `megjegyzes`-e így kezdődik: *modell-ellenőrzés (claude-opus-5-5), a felhasználó elfogadta (chat, 2026-10-24)*.

**A K1 így nem független felhasználói mérés.** A szabályokat író modell ellenőrizte a saját kimenetét, és ezt a felhasználó fogadta el. A független ellenőr (K5) ezt külön mérheti.

A beíró szkript csak ezt a két oszlopot írta. Előtte soronként összevetette a többi oszlopot az eredetivel, és üres oszlopot nem írt felül.

- **Minta (112 sor):** 104 `jó`, 8 `A` (a `jek` réteg; DT-F96e d: marad), 0 `hibás`. A `jok` réteg 6 sora `jó`, mert a DT-F96g már a `szoveg_modern`-ben van.
- **`helyesiras_ami_ellenorzes.tsv` (109 sor):** 101 `jó`, 1 `hibás`, 3 `birtokos`, 4 `vonatkozó`.
  - A hibás sor az A089 (Ef 3:20): *elgondoljuk, a mi bennünk munkálkodó erő → ami bennünk …*. Ez személyes névmás és igenév, nem vonatkozó; a V1 (vessző előtte) itt téved.
  - Ugyanez a szerkezet áll a bizonytalan A077-ben (Róm 5:8, *a mi hozzánk való szerelmét*), ezt a modell birtokosnak jelölte.

#### 4.8.3 A K1 mérése (DT-F96h)

| halmaz | eredmény | küszöb | |
|---|---:|---:|---|
| minta, cserék (`→`) | **230 / 230 (100%)** | ≥ 98% | ✓ |
| minta, szándékos *marad* (`=`) | 15 / 15 | — | |
| minta, `valtozatlan` réteg | **0** kihagyás (6 sor) | 0 | ✓ |
| `helyesiras_ami_ellenorzes.tsv`, szövegváltozó sorok | **101 / 102 (99,0%)** | ≥ 98% | ✓ |

A K1 teljesül; az A089 hibája a küszöbön belül van, a szabály nem változott.

#### 4.8.4 Megfigyelések: kimaradt régi írásmód (nem csere-hiba, a K1-be nem számít)

A minta nem `valtozatlan` rétegű soraiban kimaradt régi írásmód, amelyre nincs szabály. A `megjegyzes` oszlop soronként jelzi.

1. **A *nék-* család** (*néked, nékem, nékik, nékünk, néktek*): **3 919 token** a korpuszban (*nékik* 1 146, *nékem* 892, *néktek* 802, *néked* 784, *nékünk* 295). A minta 14 sorában fordul elő. A `neki` szabály csak a *néki*-t cseréli, mert a DT128 példája ez. → **DT-F96j** 🟡.
2. **Egyedi ékezet- és betűhibák** (M024 *irígy*, M035 *akképen*, M054 *husvét*, M056 *bölcseség*, M058 *nyilásának*, M062 *hizelkedő*, M094 *sujts*). A #94 táblája és a karakterszabály nem fedi őket, korpusz-szintű számuk nem mért. → **N-F96c**.
3. **Különírás:** *a felől, az által* (M065). Ez tokenváltozás volna (K2), ezért a .1 nem kezeli.
4. **Az *atyjokfiai* összetétel** (M089): a DT-F96g szabálya csak szóvégen fut, az *atyánkfia*-típusú összetételben nem. Számuk nem mért.

### 4.9 A DT-F96j alkalmazása és a .1 lezárása

`scope=a Károli 1908 minden verse és tokenje; a minta 112 sora | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py | ts=2026-10-24` — `python eszkozok/karoli_modern/helyesiras.py --minta-frissit`, majd `--ami-proba`; 0 token.

**A felhasználó döntése** (chat, 2026-10-24: „Mehet”): a DT-F96j 1. opciója. A `neki` szabály zárt halmazra fut (`NEK_CSALAD`): *néki, néked, nékem, nékik, nékünk, néktek → neki, neked, nekem, nekik, nekünk, nektek*, nagybetűvel is. A korpusz *nék-* kezdetű tokenjei közül három kimarad: a *Nékó* és a *Nékhusta-* (tulajdonnév), valamint az egyszeri *nékie* (1Móz 15:5), mert az alakváltozat, nem csak ékezet. Ez utóbbi az N-F96c-hez tartozik.

**Eredmény.** A DT-F96j **3 919 tokent** cserél, 10 alakon; a `neki` szabály összesen 5 657 tokenen fut (a *néki* 1 738-a és az új 3 919). Változó vers 13 083 → **14 733**, változó token 29 396 → **33 315**, változó alak 1 580 → **1 590**; a kieső tokenek száma 11 128, változatlan. A modern szövegben nem maradt *nék-* alak.

**A minta.** A `--minta-frissit` 13 sort frissített (M015, M021, M034, M037, M049, M055, M057, M066, M075, M077, M085, M088, M101). Az új cseréket a modell átnézte, mind helyes. A `megjegyzes` oszlopban a korábbi „kimaradt (nincs rá szabály)” helyett ez áll: „DT-F96j: a nék- csere átnézve (jó)”. A csere csak ezt az oszlopot érintette; a többit a szkript soronként összevetette. Az `ellenorzes` értékei megmaradtak. Az „a mi” ellenőrző fájl 109 kitöltött sora a `--ami-proba` újrafuttatása után is megmaradt.

**A K1 a DT-F96j után** (DT-F96h; modell-ellenőrzés, a felhasználó elfogadta):

| halmaz | eredmény | küszöb | |
|---|---:|---:|---|
| minta, cserék (`→`) | **246 / 246 (100%)** | ≥ 98% | ✓ |
| minta, `valtozatlan` réteg | **0** kihagyás | 0 | ✓ |
| `helyesiras_ami_ellenorzes.tsv`, szövegváltozó sorok | **101 / 102 (99,0%)** | ≥ 98% | ✓ |

**A .1 lezárva.** A K1 teljesül; a .1 ⛔ döntései (DT-F96e d, DT-F96g, DT-F96h, DT-F96i, DT-F96j) mind 🟢 és alkalmazva. Nyitva marad az N-F96c: az egyedi régi írásmódok (4.8.4) és a *nékie*. A K1 egyedül ezt a lépést nem tartja vissza.

## 5. F96.2 — igealak-lépcső és *vala*

`scope=a Károli 1908 minden verse és tokenje (31 158 vers, 599 367 token) | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + adat/karoli_modern/helyesiras_tokenek.tsv (sha256:4759bd24957f, a .1 kimenete) + eszkozok/karoli_modern/igealak.py + igeragozas.py + adat/karoli_modern/igealak_llm.tsv | ts=2026-10-24` — `python eszkozok/karoli_modern/igealak.py --minta`.

### 5.1 A generátor

A .2 a .1 kimenetére épül: az `igealak.py` a .1-et a `helyesiras.py` függvényeivel újraszámolja, és összeveti a kiadott `helyesiras_tokenek.tsv`-vel. Mind a **33 323 sor egyezik**, eltérésnél a szkript megáll. A múlt idő képzése és a jelen idő elemzése az `igeragozas.py`-ban van (kézi szabálykészlet, manual; rendhagyó tövek, hangkivetés, *-ad/-ed* tövek, az *i*-hangú igék hangrendje kézi listában). Hunspell és API nélkül fut.

| döntés | alak | token | |
|---|---:|---:|---|
| gyakori jegyes alak (DT140, a 200 leggyakoribb) | 318 | 12 565 | automatikus; a 329 alakot a modell átnézte, 7 hibás jegyű vagy rosszul képzett alak a `KEZI` táblában (*érte*: névutós névmás; *megjelenék → megjelent*; *eltemeték → eltemették*) |
| a jegy nélküli régies alakok kézi listája (`GYANU_KEZI`, N-F96b) | 74 | 1 496 | automatikus: *jő → jön*, *vőn → vett*, *mondák → mondták*, *álla → állt* … (a gyanús alakok 6+ gyakoriságú, átnézett része) |
| *lőn → lett*, *lőnek → lettek*, *vagyon → van* | 4 | 752 | automatikus; a névelő utáni *vagyon* (főnév) és a nyíllal álló *lőnek* (lő) marad |
| ritka jegyes alak (`igealak_ritka`) | 2 793 | 6 528 | **nem automatikus** (N-F94h): a szabály és az LLM jelöltje a `jelolt` oszlopban |
| jegy nélküli régies gyanú (`regies_gyanu`) | 682 | 3 701 | **nem automatikus**: jelölt |
| felszólító E/2 *-jál/-jél* (*cselekedjél → cselekedj*) | 92 | 319 | **nem automatikus**, jelölt: DT-F96k |
| kötőhangzós régi múlt (*mondotta → mondta*, *szólott → szólt*) | 89 | 658 | **nem automatikus**, jelölt: DT-F96k |
| határozói igenév kivétele (*lévén*, *jövén*-család) | 13 | — | változatlan: a mai alak is *-vén* |

A .2 a modern szövegben **18 566 tokent cserél**, és **2 447 tokent ejt ki** (segédigei *vala*). A .1-gyel együtt **20 134 vers** változik.

A tárgyas/alanyi választás a T/3, E/2, T/1 és T/2 régies alakján heurisztikus (határozott tárgy a tagmondatban): 583 token, `bizonytalan=targyas_heur`. A tárgyas alakot csak akkor kínálja, ha az ige tárgyas alakja a korpuszban áll (*bemenének → bementek*, nem *bementék*). A magas hangrendű *-ék* E/1 vagy T/3 tárgyas: 272 token, `bizonytalan=ek_E1_T3`; E/1 akkor, ha a versben egyes szám első személyű névmás áll.

### 5.2 A *vala* (K2, K3)

| eset | token | a modern szövegben |
|---|---:|---|
| létigei | 2 332 | *volt / voltak / voltam …* |
| létigei, igenév után (*írva vala*) | 20 | *volt* |
| segédigei, múlt idejű ige után (*mondotta vala*, *parancsolt vala*) | 1 014 | kiesik |
| segédigei, jelen idejű ige után (*mondja vala*, *megy vala*, *ülnek vala*) | 1 433 | kiesik; az ige múlt időbe: *mondta*, *ment*, *ültek* (1 417 alakcsere; ebből 165 a korpuszban nem álló alak, `bizonytalan=mult_korpuszban_nincs`) |
| segédigei, az ige nem elemezhető | 34 | mindkettő változatlan, `bizonytalan=vala_segedige` |

A #94 tábla sok igealakot elemezetlenül hagy (*ülnek, jöttek, hallotta, szeret → szer*). Ilyenkor a *vala* előtti szóra saját tőkeresés fut: igekötő, rendhagyó múlt tő, vagy tő + múlt idő jele, ahol a tő igeneve a korpuszban áll. A határozószók (*előtt, mellett, között*) így nem számítanak igének. A heurisztika a szórendet nem nézi (*vala* az ige előtt): ez létigei *volt* lesz.

**K2 önellenőrzés:** minden versen a modern szöveg újratokenizálva pontosan a nem kieső tokenek modern alakjait adja, sorrendben. A nem-betű váz a kieső tokenek egy-egy szóközén kívül változatlan; eltérésnél a szkript megáll. **K3:** minden sor az 1908-as token vers-kulcsán és `tokenizal`-sorszámán áll (`igealak_tokenek.tsv`). A kieső tokenek: **2 447 segédigei** (`kieso=segedige`) és a .1 11 128 összevont „a”-ja (`kieso=osszevonva`).

**A Strong a kieső tokeneken (DT-F96o).** `scope=a kieső tokenek a #22 párosított könyveiben | forras=adat/karoli_modern/igealak_tokenek.tsv + adat/karoli_strong/szavak_*.tsv | ts=2026-10-24` — a réteg Strongot nem tárol (DT-F96f); a mérés azt nézi, elveszhet-e Strong-illesztés.

| kieső token | Strongos | a Strong a gazdaszón is ott van | csak a kieső tokenen | Strong nélkül (betoldás, függőben) | a könyv nincs párosítva |
|---|---:|---:|---:|---:|---:|
| összevont „a” | 5 572 | 5 315 | **257** (főleg H0834) | 3 865 | 1 691 |
| segédigei *vala* | 38 | 1 | **37** (mind H1961) | 1 688 | 721 |

A kieső sor a táblában megmarad (kulcs + `kieso`), ezért egy Strong-illesztés sem vész el. A modern szövegben a 294 tokennek nincs saját szava: a `kieso_gazda` oszlop a gazdaszó sorszámát adja (az összevont „a”-é a következő token, a segédigei *vala*-é az előző). A kereső (#137) ide köti a Strongot. A kulcs-lefedettség gépi igazolása a .3-ban (K3b).

### 5.3 LLM-ellenőrzés és tő-őr (DT-F96d)

A nem automatikus igealak-jelöltek (ritka jegyes és régies gyanús alakok; **3 174 kisbetűs alak**) LLM-kérdésként mentek: alak, szótári alak, jegy és az első előfordulás versrészlete, a szabály jelöltje nélkül (vak ellenőrzés). Előfizetésből futott (Claude Code subagent, **claude-sonnet-5-5**, a .0 mérésének modellje), API és `PARDES_API_KEY` nélkül. Öt köteg: az elsőben 420 alak, ±8 szavas versrészlettel; a többi négyben 689 alak, ±5 szóval. Minden kérdésre jött válasz, 3 174 / 3 174 (`adat/karoli_modern/igealak_llm.tsv`, modell-kimenet, `modell_ellenorizetlen`).

| osztály | tő-őr | szabály = LLM | alak |
|---|---|---|---:|
| ritka jegyes | ok | egyezik | 2 400 |
| ritka jegyes | ok | eltér | 296 |
| ritka jegyes | bukott | — | 75 |
| régies gyanú | ok | nincs szabály-jelölt | 426 |
| régies gyanú | ok | egyezik / eltér | 133 / 34 |
| régies gyanú | bukott | — | 86 |

A ritka jegyes alakokon a szabály és az LLM **2 400 / 2 771 alakon egyezik (86,6%)**. Az eltérések (modell-átnézés, 30 elemes szúrópróba) főként jegyhibák, és ott az LLM-nek van igaza: nem ige (*félénk, felirata, haladék, erősebbé*), a mai alak hibás E/2 jeggyel (*elmentél, elvesztél*), a magas hangrendű *-ék* E/3-a (*elutazék → elutazott*). A szenvedő *-taték/-teték* (*kiadaték → kiadatott*) és az *-ik*-es *-ék* E/3-a erre szabályjavítást kapott. Az LLM is hibázik: *játszék → játsszon*, *keltének* változatlan, a tárgyas/alanyi választás. A tő-őr főként két esetben bukik: a helyesírási ékezetnél (*kinyujtá → kinyújtotta*: a tő-őr a .1 utáni alakot nézi), és ott, ahol az LLM a *-nd-* jövő időt jelenre írta (*mondándom → mondom*, *leendesz → leszel*). Ez utóbbi helyes kiszűrés: igeidő-váltás. A jelölt a modern szövegbe nem kerül be; az alkalmazás a DT-F96l döntése.

### 5.3b Második ellenőrzés opusszal a vitatott alakokon

**A felhasználó kérésére** (chat, 2026-10-24: „Mehet, futtasd opusszal a vitatott 880 alakot”) a vitatott jelöltek második, vak LLM-ellenőrzést kaptak. Vitatott az a ritka jegyes vagy régies gyanús alak, ahol a szabály és a sonnet nem egyezik, vagy a tő-őr bukott: **860 kérdés** (858 kisbetűs alak). A futtató Claude Code subagent volt, **claude-opus-5-5** modellel, két 430-as kötegben, előfizetésből, API nélkül. A versrészlet ±6 szó volt, a szótári alakkal. **Eltérés a sonnet-utasítástól:** az opus utasítása külön kimondta, hogy a *-nd-* jövő idő egy szóban nem írható át, ezért változatlanul adandó vissza. A sonnet ezeket jelen időre írta, a tő-őr pedig nagyrészt kiszűrte őket (5.3). Az opus válasza: `adat/karoli_modern/igealak_llm_opus.tsv` (modell-kimenet, `modell_ellenorizetlen`). A második köteg a választ id helyett sorszámmal adta vissza; a kérdésfájl sorrendje szerint lett visszarendelve, a sorszám-egyezés ellenőrzésével.

| osztály | opus tő-őr | az opus kivel egyezik | alak | token |
|---|---|---|---:|---:|
| ritka jegyes | ok | a sonnettel | 257 | 454 |
| ritka jegyes | ok | a szabállyal | 61 | 132 |
| ritka jegyes | ok | egyikkel sem | 20 | 50 |
| ritka jegyes | bukott | — | 33 | 82 |
| régies gyanú | ok | a sonnettel | 414 | 2 972 |
| régies gyanú | ok | a szabállyal | 3 | 28 |
| régies gyanú | ok | egyikkel sem | 121 | 325 |
| régies gyanú | bukott | — | 8 | 13 |

**Megfigyelések** (modell-átnézés, szúrópróba):
- Az „egyikkel sem” sorok zöme (104 alak, 286 token) *-nd-* jövő idő, amelyet az opus az utasítása szerint változatlanul hagyott (*mondándok, leend, teendi*).
- Ahol az opus a szabállyal egyezik, ott a sonnet jellemzően **a szókincsbe nyúlt**, ami a DT128 szerint tilos: *általmenének → átmentek* (opus: *általmentek*), *helyheztete → helyeztetett* (opus: *helyheztetett*), *eltapodá → eltaposta* (opus: *eltapodta*), *eltelé → eltöltötte*. A tárgyas/alanyi és a személy választásában is az opus a pontosabb: *lakozátok → lakoztatok*, nem *laktatok*; *átronték → átrontottam*, nem *átrontottak*.
- Az opus a .1 helyesírását nem pótolja: *Kinyujtá → Kinyujtotta*, nem *Kinyújtotta*. Ez a .1 dolga (N-F96c).
- Az opus és a sonnet egyezése nem teljesen független megerősítés: a két utasítás közös, csak a *-nd-* mondatban tér el.

### 5.4 Token-felhasználás (K4)

`scope=az 5 LLM-köteg | forras=a subagentek átirata (usage mezők), adat/karoli_modern/igealak_llm_hivasok.jsonl | ts=2026-10-24`

| köteg | alak | hívás | bemenet (új + cache-írás) | cache-olvasás | kimenet | összesen |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 420 | 4 | 108 561 | 247 864 | 12 653 | 369 078 |
| 2 | 689 | 3 | 97 798 | 142 869 | 22 608 | 263 275 |
| 3 | 689 | 3 | 97 507 | 142 843 | 23 434 | 263 784 |
| 4 | 689 | 3 | 98 802 | 142 924 | 21 756 | 263 482 |
| 5 | 687 | 3 | 97 070 | 142 884 | 20 214 | 260 168 |
| **összesen** | **3 174** | 16 | **499 738** | **819 384** | **100 665** | **1 419 787** |

A becslés (a brief 0,05–0,2 M-ja, illetve a DT-F96d ≈ 0,45 M-os kerete, a .0 API-mérése alapján, alakonként 132,5 token) **a teljes számítás szerint kb. háromszorosan túllépve: 1,42 M**, alakonként 447 token. A cache-olvasás nélkül (új bemenet + kimenet) **0,60 M**, ez is a keret felett. Az ok a subagent saját rendszerpromptja és eszközleírása (hívásonként kb. 57 ezer token), amely minden hívásnál újra beolvasódik; a .0 API-mérésében ez nem volt. Az első köteg (fájlba író beállítás) után a többi kötegnél csak egy olvasás és a válasz a hand-back üzenetben: alakonként 382 token. A keret kérdése: DT-F96m.

**Az opus-ellenőrzés** (5.3b; `adat/karoli_modern/igealak_llm_opus_hivasok.jsonl`):

| köteg | alak | hívás | bemenet (új + cache-írás) | cache-olvasás | kimenet | összesen |
|---|---:|---:|---:|---:|---:|---:|
| opus 1 | 430 | 2 | 87 053 | 57 300 | 12 735 | 157 088 |
| opus 2 | 430 | 2 | 87 025 | 57 300 | 10 972 | 155 297 |
| **összesen** | **860** | 4 | **174 078** | **114 600** | **23 707** | **312 385** |

Alakonként 363 token. **A .2 LLM-felhasználása összesen 1 732 172 token** (sonnet 1 419 787 + opus 312 385); cache-olvasás nélkül 0,80 M. Az opus-futás a DT-F96m nyitott kérdése mellett, a felhasználó külön kérésére ment.

A .2 determinisztikus része (szabályok, *vala*, minta) 0 token.

### 5.5 Lefedettség — maradt-e régies igealak

A modern szövegben maradó régies igealak, tokenben: ritka jegyes **6 734** (ebből jelölttel 6 706), régies gyanú **3 685** (jelölttel 3 592), gyakori jegyes **241** (a felszólító *-jál* és a jelölt nélküli 5 alak), a *vala*-család 34 (a bizonytalan segédige), *lőnek* 2, *vagyon* 1. Összesen **10 697 token** régies igealak marad, ebből 10 439 jelölttel. Ha a DT-F96l szerint a szabály + LLM egyező, tő-őrön átment ritka jelöltjei bekerülnek, ez 5 771 tokennel csökken (a 2 400 alak tokenje). A gyanú-heurisztika alsó becslés (napló 1.2): a jegy nélküli, a heurisztikán kívül eső régies alak nem számolódik. A *-nd-* jövő (*mondándok, leend*) egy tokenben nem írható át (a mai alak két szó: *mondani fogok*); jelöltként marad.

### 5.6 A minta (⛔ felhasználói ellenőrzés)

`adat/karoli_modern/igealak_minta.tsv`: rögzített magú (20261024), rétegzett minta, **120 vers**, 20 réteg. A rétegek: jegyenként a gyakori igealak; a tárgyas/alanyi heurisztika; az *-ék* E/1/T/3; *lőn*, *vagyon*, a gyanú kézi listája; a *vala* négy esete; a ritka és a gyanús jelölt; a felszólító *-jál*; a kötőhangzós múlt; és változatlan vers. Oszlopok: `szoveg_1908`, `szoveg_modern` (a .1 + .2 után), `valtozasok` (a `[.2]` jelű a .2 cseréje, a `?(…)` a bizonytalan jelölés), `jelolt` (a nem automatikus jelöltek: `szabaly:` és `llm:` a tő-őr eredményével), `ellenorzes` és `megjegyzes`. Az utolsó kettőt a felhasználó tölti: *jó* / *hibás*, a jelölt soron *A* = a jelölt jó, *B* = maradjon. A modell nem tölti ki őket. A K1 küszöbét és mérési egységét a felhasználó adja a mérés előtt (a .1 DT-F96h-ja a .1-re szólt; a delegálás a .2-re nem érvényes).

### 5.7 A döntések alkalmazása és a K1 (DT-F96k, l, m, n)

`scope=a Károli 1908 minden verse és tokenje; a minta 120 sora | forras=mint 5., + adat/karoli_modern/igealak_llm_opus.tsv | ts=2026-10-24` — `python eszkozok/karoli_modern/igealak.py --minta-frissit`; 0 token.

**A felhasználó döntése** (chat, 2026-10-24: „Mehet” a javaslatokra): DT-F96m 1. (a túllépés elfogadva; a keret a teljes számítással, cache-olvasással mérve; minden további LLM-futás előtt kötegszám és becslés, jóváhagyással); DT-F96k (b) igen, (a) marad; DT-F96l 2. opció; DT-F96n 1. opció, a minta modell-ellenőrzéssel, a felhasználó elfogadására.

**Alkalmazva.**
- **DT-F96k (b):** a kötőhangzós régi múlt automatikus csere, korpusz-támasszal. Ez **620 token**: *szólott → szólt* 144, *mondotta → mondta* 91, *állott → állt* 58, *megmondotta → megmondta* 46 …
  - Kimarad a melléknévi igenév (*halott*, *törött*, *elbizakodottak*, *megölöttek*): az E/3 és a T/3 alanyi csak a `KOTOHANG_IGE` listán cserél.
  - Kimarad a más igéhez tartozó alak (*születtél*: születik; *elveszett*: elvész; *küldettem*, *kiűzettek*: szenvedő) és a *körülött-* névutó.
- **DT-F96k (a):** a felszólító *-jál* (319 token) változatlan; a jelölt a mintában marad.
- **DT-F96l, 2. opció:** a ritka és a gyanús jelölt cserél, ha a szabály, a sonnet és az opus közül legalább kettő egyezik, és a tő-őr átengedi. Ez **6 866 token**: szabály + sonnet 6 041, sonnet + opus 663, szabály + opus 160 …
  - A szövegkörnyezetfüggő szabály-jelölt (alanyi/tárgyas, E/1/T/3) tokenenként a heurisztikával dönt.
  - A felszólító *-jál* és a névelő utáni alak kimarad.
  - Ahol a többség a változatlan alakot adja, ott az alak nem régies igealak (*tett, leszek, halál*; 2 596 token).

**Javítások a minta modell-átnézése után** (a mérés előtt, a küszöb rögzítése után):
1. **A névelő utáni igealak-jelölt főnév, változatlan marad:** *a tevék*, *egy tevének*, *a küldöttek*; 47 token, `bizonytalan=nevelo_utan`.
2. **A kötőhangzós szabály szűkítése:** l. fent.
3. **A segédigei *vala* a .2 által múltba tett ige után is kiesik:** *illeték vala → illették*. Az *-lak/-lek* E/1 (*etettelek*) múltnak számít.
4. **A tárgyas/alanyi heurisztika finomítása:**
   - a vonatkozó névmás tárgya alanyit kér: *amelyeket adtak*, *amelyet hoztak*;
   - az 1./2. személyű tárgy alanyit kér: *hagytál el engemet*;
   - a tagmondat a vesszőig és az „és”-ig tart;
   - az idézet előtti kettőspont már nem tárgyas jel: *feleltek*;
   - a puszta *-át/-ét* nem birtokos tárgy: *ötven horgocskát* → *csináltak*;
   - az E/1 próbája is tagmondaton belül fut.
5. **A régies gyanús osztályban is a kötőhangzós szabály dönt** (*mondotta*).

**A .2 együtt:**
- A .2 a modern szövegben **25 996 tokent cserél**, és **2 450 segédigei *vala*-t ejt ki**. A .1-gyel együtt **21 255 vers** változik.
- A K2 minden versen átmegy, a .1 újraszámolása egyezik.
- **Lefedettség:** a modern szövegben 1 146 token régies igealak marad. Ebből döntés szerint marad 319 (felszólító *-jál*), egy szóban nem írható át 147 (*-nd-* jövő). A többi 680 token:
  - régies gyanú 294 és ritka jegyes 214, ahol nincs többségi jelölt;
  - gyakori jegyes 135: a névelő utáni és a jelölt nélküli alakok;
  - a *vala*-család 34 bizonytalan esete és egyéb, 37.

**A K1** (DT-F96n; modell-ellenőrzés, claude-opus-5-5; **a felhasználó elfogadására vár**):

| halmaz | eredmény | küszöb | |
|---|---:|---:|---|
| a minta automatikus cseréi (`[.2]` és a kieső *vala*) | **313 / 316 (99,1%)** | ≥ 98% | ✓ |
| ebből bizonytalan nélkül | 275 / 277 (99,3%) | — | |
| bizonytalan jelölésű cserék (`targyas_heur`, `ek_E1_T3`, `mult_korpuszban_nincs`; mellékmérés) | 38 / 39 (97,4%) | külön kiírva | |
| `valtozatlan` réteg | **0** kihagyás | 0 | ✓ |

**A három hibás csere** (a minta `megjegyzes` oszlopában):
- **G020, Jn 6:58:** *atyáitok evék a mannát → evett*; helyesen *ették*. A gyakori *evék* jegye mult.E3, a T/3-at a szabály nem látja.
- **G046, Ez 25:5:** *tevék legelőjévé → tették*. A *tevék* itt főnév; névelő nincs előtte, ezért a próba nem fogja meg.
- **G084, Jel 12:2:** *kínlódik vala → kínlódik volt*; helyesen *kínlódott*. A #94 elemezetlen *kínlódik*-ja a korpuszban nem igazolható igének.

Mindhárom egyedi eset. Szabállyal csak az utolsó javítható általánosan (az *-ik* végű, elemezetlen alak igeként a *vala* előtt), ez a .3-ban vagy a felhasználó döntése szerint.

**Megfigyelés a mintán kívül (nem javítva, a K1-be nem számít):** a minta nem automatikus rétegeiben maradt régies alakok (*összefoglalák, agyonverék, táncolának, megölém, elhozám, kirántá, felháboríták, rakád, mondám, általméne*) a többségi jelölt hiánya vagy a #94 jegyhiánya miatt maradtak. A lefedettségbe beleszámítanak.
