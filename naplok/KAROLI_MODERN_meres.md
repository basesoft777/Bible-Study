# KAROLI_MODERN_meres.md — a modernizált Károli-réteg mérési naplója (F96, FELADATOK #96)

*Brief: `F96_KAROLI_MODERN_BRIEF.md` v1.5 (a napló a v1.1-gyel indult). Végrehajtó: claude-opus-5-5 (a kért modell: opus). Ág: `ccr-a680d019-39s73e`.*

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
| `lemmavaltas` | 165 | 10 980 | a `szotari_alak_mai` nem csak helyesírás (*ki → aki*, *mely → amely*, *e → ez*, *oh → ó*, *férfiú → férfi*, *leány → lány*, *cselekedik → cselekszik*) — **döntési kérdés** (DT304), nem gépi csere |
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
| *reá*-család (*reá, reám, reátok, reánk …*) | 640 token | a DT128 nem nevezi; *reá → rá* helyesírás-e: DT304 |

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

A brief becslése (~0,05–0,2 M) az (1)-es változatban **túllépve** (0,44 M; a tokenszintű esetekkel együtt ~0,8 M), a teljes LLM-átírás ~3–3,5 M-jának így is kb. negyede. A brief .0/3 szerint itt megállás: ⛔ DT303.

**Minőségi megfigyelések a mintán (modell-kimenet, a felhasználó még nem ellenőrizte):** 194 sor `biztos`, 6 `bizonytalan`; a 41 `regies_gyanu` sorból 27-et írt át (*mondák*-típus → *-ták*, *-teték → -tetett*, *-vén → -ve*), 14-et hagyott változatlanul mai alakként (*elvesznek, hullák, karaván*) — a gyanú-heurisztika hamis pozitívjai. A jegyhibát elkapta (*követe*: főnév). **Szókincs- és alakhiba is van:** *megnevekedék → megszaporodott* (szókincscsere, a DT128 tiltja), *lennék → legyek* (a feltételes mód mai alak), *őrizénditek → őrizendőtök* (nem létező alak), *ráküldé → rákűldte* (helyesírási hiba), *keltének* változatlanul. Következmény: az LLM-kimenet elé determinisztikus **tő-őr** kell (a modern alaknak az igető, illetve a szótári alak mai alakjának betűsorát kell hordoznia; ami nem, az `bizonytalan`, felhasználói sorba), ez a .2 része.

## 3. Nyitott a .1 előtt — állapot a .1 indulásakor

- DT303 🟢: a keret emelve (≈ 0,45 M), az LLM-es maradék az előfizetésből (Claude Code), API nélkül; tő-őr kötelező. A .1 nem használ LLM-et (0 token).
- DT304 🟢: (a) a lemmaváltások maradnak; (b) *reá → rá* igen (.1); (c) *-ván/-vén* igen (.2); (d) *-jék*: a .1 mintája dönt (4.5).
- DT305 🟢: a réteg nem tárol Strongot; token-kulcs (vers-kulcs + `tokenizal`-sorszám).
- N-F96b: a *kivűl* és a további megfigyelt táblahibák a .1 kivételtáblájában (4.2); a *vévén* a .2-ben.
- A Hunspell hu_HU (DT301): 4.1 (a pótló menet: futott, 4.1.3–4.1.5).

## 4. F96.1 — helyesírási lépcső

`scope=a Károli 1908 minden verse (31 158) és tokenje (599 367) | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py | ts=2026-10-24T13:36Z` — `python eszkozok/karoli_modern/helyesiras.py --minta`; determinisztikus, LLM és API nélkül (**0 token**). Kimenet (generált, `# GENERÁLT:` fejléccel): `adat/karoli_modern/helyesiras_alakok.tsv` (a szövegkörnyezet nélkül változó alakok), `adat/karoli_modern/helyesiras_tokenek.tsv` (a változó, kieső vagy bizonytalan tokenek, vers-kulccsal és `tokenizal`-sorszámmal, DT305), `adat/karoli_modern/helyesiras_minta.tsv` (4.4). Ez a .1 köztes kimenete, nem a .3 kiadott rétege.

### 4.1 Hunspell hu_HU (DT301): fejlesztési mérce, futott

*Előzmény: a .1 első menetében (2026-10-24, 13:36Z előtt) a Hunspell nem futhatott, mert a GitHub és a PyPI felé a hálózati szabály `connect_rejected` választ adott; a `helyesiras_alakok.tsv` fejléce és a DT307 szövege ezt az állapotot rögzíti. A mérést ugyanazon a napon, egy hálózattal futó menet pótolta (4.1.1–4.1.5).*

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
- **Régi helyesírású vagy alakú közszó, amelyet a szabály nem fed le** (*cerimóniákat → ceremóniákat, kálcédon → kalcedon, skárlátcikkeket → skarlát-, pőröllyel → pöröllyel, sudarcédrussal → sudár-, köröskörül → körös-körül, kívánatosb*): a karaktercsere után maradó eltérés. Lemma- vagy alakváltás, a DT304 (a) szerint nem e lépcső dolga. A *körös-körül* kötőjeles, tehát tokenváltozás volna.
- **A semleges eset a Hunspell korlátja.** A szótár sok régies alakot elfogad: *néki* (1 734 token), *reá, reám, reád*, *setétség* és ragozott alakjai, *arczára, válaszszák, harmincz* (*Harmincz*), *paizsos*. Ezeken a Hunspell nem dönt. A régi alak elfogadása nem cáfolja a szabályt, de alá sem támasztja. A *néki → neki* és a *reá → rá* forrása a DT128 és a DT304 (b), tehát felhasználói döntés.
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
| `rea` | DT304 b | 661 | *reá → rá*, *reájok → rájok*, *reáköltesz → ráköltesz* |
| `szotag` | manual | 160 | *dícsér- → dicsér-*, *paizs → pajzs* |
| `kivetel` | N-F96b | 4 csere | *kivűl → kívül* (a #94 tábla: *kivül*); változatlan marad a *gyűl-*, *egybegyűl-*, *összegyűl-*, *dűl-*, *ledűle*, *jóhiszeműleg* (a tábla mai alakja ott hibás: *gyül*, *dül*) |

Összesen: **12 804 vers változik** (a 31 158-ból), **28 953 token** (ebből 11 212 kieső „a”), **1 377 alak** szövegkörnyezet nélkül. Az alakok `tamasz` oszlopa: `szoto_94` 177, `korpusz` 106 (a modern alak a Károliban is áll), `manual` 1, **`modell_ellenorizetlen` 1 093** (zömmel a `karakter` cseréi: a *cz*-s alakok modern párja a Károliban nem fordul elő; Hunspell nélkül ez a mintán mérhető; a Hunspell-ítélet: 4.1.3).

**Nem változik a .1-ben (szándékosan):** a lemmaváltás (DT304 a: *e, oh, férfiú, leány, mostan, minekutánna*, az önálló *kik/mely*); minden igealak (*teremté, monda, -ván/-vén, vala, lőn, vagyon*: .2); a *-jék* és a *-jok/-jök* (4.5).

**Az „a mi” kezelése (heurisztika, manual; a DT308 előtti állapot, felváltotta a 4.6).** Toldalékos *mi-* (*mit, minek, mire*) mindig összevonva. A puszta „a mi”: ha a következő szó *-nk* birtokos (*a mi Istenünk, a mi atyánk*) → birtokos, marad (`mi_birtokos_marad`); ha a következő szó nagybetűs, személyes névmás (*nékünk, minket*), vagy írásjel követi → `bizonytalan`, változatlan (**298 token**; ezek a mintában is szerepelnek); különben → *ami*. Egy „a Ki…” nagybetűs vers közbeni eset `nagybetu`, változatlan.

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
| `jek` | 8 | a *-jék* felszólító E/3: az `alternativa` oszlop a *-jon/-jen/-jön* változat (DT304 d) |
| `jok` | 6 | a *-jok/-jök* birtokos T/3: az `alternativa` oszlop a *-juk/-jük* változat (DT306) |
| `valtozatlan` | 6 | nem maradt-e ki régi helyesírás (a Hunspell helyett) |

Oszlopok: `szoveg_1908`, `szoveg_modern` (a .1 kimenete), `valtozasok` (`sorszám:régi→új`; `(összevonva)` = kieső „a”; `?(…)` = bizonytalan, változatlan; `=(…)` = szándékosan marad), `alternativa` (csak a `jek`/`jok` sorokon). **Az `ellenorzes` és a `megjegyzes` oszlopot a felhasználó tölti** (javasolt értékek: `jó` / `hibás`; a `jek`/`jok` sorokon `A` = a `szoveg_modern`, `B` = az `alternativa`); a mérés csak a kitöltött sorokon fut. Az igealak (*monda, vala, lőn*) e lépcsőben szándékosan régi: nem hiba.

**A K1 küszöbe** (brief .1/3, K1) a mérés előtt rögzítendő: DT307.

### 4.5 Döntésre váró, a mintán eldöntendő

- **DT304 (d)** *-jék* felszólító E/3 az *-ik*-es igéken (*cselekedjék, uralkodjék, lakozzék, igyék*): **93 alak, 417 token** (heurisztika: a szótári alak *-ik*-re végződik, a tő önálló szóként nem áll a korpuszban, így a tárgyas T/3 *megismerjék* kimarad). Az alternatíva hangrendje: *-jon/-jen/-jön*; csak *i/í* magánhangzós tőnél *-on* (*igyék → igyon*).
- **DT306** (új) *-jok/-jök* birtokos T/3 (*atyjok, reájok, hozzájok, útjokat, erejök*): **212 alak, 714 token** a *j*-s változaton (kizárva a többes számú *tolvajok, bajok, tutajok-*). A *j* nélküli változat (*kezöket, szívök, közöttök*) a .1-ben nem mért: a *-ok/-ök* többes számmal egybeesik, gépi szétválasztása szövegkörnyezetfüggő.

### 4.6 Az „a mi”-szabály (DT308; a 4.6.1–4.6.3 a kísérleti mérés, a 4.6.4 az alkalmazás)

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

#### 4.6.4 Alkalmazva (DT308 🟢, 1. opció)

**A felhasználó döntése:** 2026-10-24, chat: „Mehet a javaslat”. A 4.6.1 szabálya a kiadott .1 része lett, a `szabaly` oszlopban `ami:<kritérium>` címkével. A `--ami-proba` futás a DT308 előtti és a DT308 szerinti döntést veti össze, a kiadott réteget nem írja.

`scope=a Károli 1908 minden verse (31 158) és tokenje (599 367) | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py (sha256:555cf301c07a) | ts=2026-10-24` — `python eszkozok/karoli_modern/helyesiras.py --minta-frissit`, majd `--ami-proba`; 0 token.

| | DT308 előtt (4.2) | DT308 szerint |
|---|---:|---:|
| változó vers | 12 804 | **12 760** |
| változó token | 28 953 | **28 785** |
| kieső (összevont „a”) | 11 212 | **11 128** (−93 + 9) |
| `bizonytalan` „a mi” | 298 | **7** (és 1 `nagybetu`, változatlan) |
| változó alak (`helyesiras_alakok.tsv`) | 1 377 | 1 377 (a törzs bájtra azonos) |

A `helyesiras_tokenek.tsv`-ben csak a puszta „a mi” tokenjeinek sorai változtak: a döntés és a `szabaly` címke. Más sor nem változott (diff a futás előtti változattal).

**A minta (`helyesiras_minta.tsv`)** az új `--minta-frissit` kapcsolóval frissült. Ez megtartja a kiválasztást (`minta_id`, `reteg`, `igehely`) és a felhasználói oszlopokat (`ellenorzes`, `megjegyzes`; most üresek), és csak a `szoveg_modern`, `valtozasok`, `alternativa` oszlopot számolja újra. A régi `--minta` kapcsoló a DT308 óta más verseket választana, mert a `bizonytalan` réteg jelöltjei 298-ról 7-re fogytak. Ezért a minta így nem generálódott újra. Változott 5 sor, a `bizonytalan` réteg 4 sora és az M076:
- M076, M077, M078, M080: a bizonytalan „a mi” birtokosként jelölve (`=(birtokos, marad)`), a szöveg változatlan;
- M079 (2Móz 9:4): *mindabból, a mi Izráel fiaié → mindabból, ami Izráel fiaié*.

A `bizonytalan` réteg 4 sora így a DT308 döntéseit méri.

**Külön felhasználói ellenőrzés: `adat/karoli_modern/helyesiras_ami_ellenorzes.tsv`**, generált, 109 token:

| `tipus` | token | ellenőrizendő |
|---|---:|---|
| `osszevonas_visszavonva` | 93 | a DT308 előtt *ami* lett, most birtokos, marad *a mi* (*a mi atyáinknak, a mi mindennapi kenyerünket*) |
| `osszevonas_uj` | 9 | a DT308 előtt bizonytalan volt, most *ami* |
| `bizonytalan` | 7 | támpont nélkül, változatlan (a modell olvasata: 4.6.2) |

Oszlopok: `szoveg_1908`, `szoveg_modern_dt_f96i_elott`, `szoveg_modern`, `kriterium`. Az `ellenorzes` és a `megjegyzes` oszlopot a felhasználó tölti (`jó` / `hibás`; a `bizonytalan` sorokon `vonatkozó` / `birtokos`). Újragenerálásnál a kitöltött értékek megmaradnak (`igehely` + `sorszam` kulcson). Ezt a 112 soros minta nem fedi: a K1 küszöbét (DT307) erre a fájlra is alkalmazni kell.

**Hunspell (DT301).** A `helyesiras_hunspell.tsv` fejléce a régi `helyesiras_tokenek.tsv` sha256-ját hordozza (`49fbf5d191c5`). Tartalmilag nem avult el: új alakpár nem keletkezett, a *mi → ami* pár benne van (`semleges`), és csak a darabszáma kisebb. Újrafuttatás nem volt, a futtató ebben a sessionben nincs meg.

**A 4.2 „Az „a mi” kezelése” bekezdése a DT308 előtti állapotot írja le; a kiadott réteg a 4.6.1 szerint jár el.**

### 4.7 Döntések a .1 ⛔ mérése előtt (felhasználó, 2026-10-24)

A felhasználó a modell javaslatát hagyta jóvá (chat: „Mehet”). A K1 küszöbe így **a mérés előtt** rögzült (brief K1). A minta és a generált táblák ebben a menetben nem változtak.

- **DT307 (K1) 🟢.**
  - **Egység:** a csere, vagyis a minta `valtozasok` tétele.
  - **Küszöb:** ≥ 98% helyes csere két külön halmazon: a 112 soros mintán (`helyesiras_minta.tsv`) és a `helyesiras_ami_ellenorzes.tsv` 102 szövegváltozó során (`osszevonas_visszavonva` + `osszevonas_uj`; legfeljebb 2 hibás).
  - **`valtozatlan` réteg:** 0 kihagyott régi helyesírás.
  - **Nem hiba:** a `jek`/`jok` sorok A/B választása és a 7 bizonytalan „a mi” besorolása (döntés).
  - **Küszöb alatt:** a hibás szabály javul, és csak az érintett sorok mérődnek újra.
- **DT304 (d) 🟢.** A *-jék* felszólító E/3 (93 alak, 417 token) **marad**. Élő, választékos alak (4.1.4: a Hunspell elfogadja), a DT304 (a) logikája szerint. A minta `jek` rétegén eltérő ítélet felülírja.
- **DT306 🟢.**
  - **Változik:** a *j*-s *-jok/-jök → -juk/-jük* (212 alak, 714 token) a .1 szabálya. Gépileg egyértelmű, és a Hunspell a régi alakot elutasítja (4.1.4: *rájok*, *orcájok-*).
  - **Marad:** a *j* nélküli változat (*kezöket, szívök*).
  - A minta `jok` rétegén eltérő ítélet felülírja.
  - **Hátra van:** az alkalmazás (generátor-szabály, újragenerálás, a minta `--minta-frissit`-tel).

### 4.8 A DT306 alkalmazása, az átnézés és a K1 mérése

`scope=a Károli 1908 minden verse és tokenje; a minta 112 sora; a helyesiras_ami_ellenorzes.tsv 109 sora | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py | ts=2026-10-24` — `python eszkozok/karoli_modern/helyesiras.py --minta-frissit`, majd `--ami-proba`. Az átnézés és a mérés a scratchpadben futott, 0 token.

#### 4.8.1 DT306 alkalmazva

Új szabály, `jok` (`szabaly_forras`: DT306): a *j*-s birtokos T/3 *-jok/-jök → -juk/-jük*, **212 alak, 714 token**. A szabály az alak minden más cseréje után fut, így a *reájok → rájok → rájuk* sor is teljesül. A 212 alakot egyenként átnéztem. A többes számra gyanús hat alak (*hajokat, ganéjokat, nyájok, nyájokat, zárjok, ujjokkal*) a versben mind birtokos (*a saját ganéjokat*, *az ő nyájok mellett*), többes számú főnév nincs köztük.

Új állapot: változó vers 12 760 → **13 083**, változó token 28 785 → **29 396**, változó alak 1 377 → **1 580**; a kieső tokenek száma 11 128, változatlan. A minta 9 sora frissült a `--minta-frissit` kapcsolóval (M039, M042, M061, M101–M106). A *j* nélküli változat (*kezöket, szívök*) marad.

#### 4.8.2 Az átnézés — a felhasználó a modellre bízta

**A felhasználó döntése** (chat, 2026-10-24): „Nézd át te. Elfogadom a döntést”. A két fájl `ellenorzes` oszlopát ezért a modell (claude-opus-5-5) töltötte ki. Minden sor `megjegyzes`-e így kezdődik: *modell-ellenőrzés (claude-opus-5-5), a felhasználó elfogadta (chat, 2026-10-24)*.

**A K1 így nem független felhasználói mérés.** A szabályokat író modell ellenőrizte a saját kimenetét, és ezt a felhasználó fogadta el. A független ellenőr (K5) ezt külön mérheti.

A beíró szkript csak ezt a két oszlopot írta. Előtte soronként összevetette a többi oszlopot az eredetivel, és üres oszlopot nem írt felül.

- **Minta (112 sor):** 104 `jó`, 8 `A` (a `jek` réteg; DT304 d: marad), 0 `hibás`. A `jok` réteg 6 sora `jó`, mert a DT306 már a `szoveg_modern`-ben van.
- **`helyesiras_ami_ellenorzes.tsv` (109 sor):** 101 `jó`, 1 `hibás`, 3 `birtokos`, 4 `vonatkozó`.
  - A hibás sor az A089 (Ef 3:20): *elgondoljuk, a mi bennünk munkálkodó erő → ami bennünk …*. Ez személyes névmás és igenév, nem vonatkozó; a V1 (vessző előtte) itt téved.
  - Ugyanez a szerkezet áll a bizonytalan A077-ben (Róm 5:8, *a mi hozzánk való szerelmét*), ezt a modell birtokosnak jelölte.

#### 4.8.3 A K1 mérése (DT307)

| halmaz | eredmény | küszöb | |
|---|---:|---:|---|
| minta, cserék (`→`) | **230 / 230 (100%)** | ≥ 98% | ✓ |
| minta, szándékos *marad* (`=`) | 15 / 15 | — | |
| minta, `valtozatlan` réteg | **0** kihagyás (6 sor) | 0 | ✓ |
| `helyesiras_ami_ellenorzes.tsv`, szövegváltozó sorok | **101 / 102 (99,0%)** | ≥ 98% | ✓ |

A K1 teljesül; az A089 hibája a küszöbön belül van, a szabály nem változott.

#### 4.8.4 Megfigyelések: kimaradt régi írásmód (nem csere-hiba, a K1-be nem számít)

A minta nem `valtozatlan` rétegű soraiban kimaradt régi írásmód, amelyre nincs szabály. A `megjegyzes` oszlop soronként jelzi.

1. **A *nék-* család** (*néked, nékem, nékik, nékünk, néktek*): **3 919 token** a korpuszban (*nékik* 1 146, *nékem* 892, *néktek* 802, *néked* 784, *nékünk* 295). A minta 14 sorában fordul elő. A `neki` szabály csak a *néki*-t cseréli, mert a DT128 példája ez. → **DT309** 🟡.
2. **Egyedi ékezet- és betűhibák** (M024 *irígy*, M035 *akképen*, M054 *husvét*, M056 *bölcseség*, M058 *nyilásának*, M062 *hizelkedő*, M094 *sujts*). A #94 táblája és a karakterszabály nem fedi őket, korpusz-szintű számuk nem mért. → **N-F96c**.
3. **Különírás:** *a felől, az által* (M065). Ez tokenváltozás volna (K2), ezért a .1 nem kezeli.
4. **Az *atyjokfiai* összetétel** (M089): a DT306 szabálya csak szóvégen fut, az *atyánkfia*-típusú összetételben nem. Számuk nem mért.

### 4.9 A DT309 alkalmazása és a .1 lezárása

`scope=a Károli 1908 minden verse és tokenje; a minta 112 sora | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py | ts=2026-10-24` — `python eszkozok/karoli_modern/helyesiras.py --minta-frissit`, majd `--ami-proba`; 0 token.

**A felhasználó döntése** (chat, 2026-10-24: „Mehet”): a DT309 1. opciója. A `neki` szabály zárt halmazra fut (`NEK_CSALAD`): *néki, néked, nékem, nékik, nékünk, néktek → neki, neked, nekem, nekik, nekünk, nektek*, nagybetűvel is. A korpusz *nék-* kezdetű tokenjei közül három kimarad: a *Nékó* és a *Nékhusta-* (tulajdonnév), valamint az egyszeri *nékie* (1Móz 15:5), mert az alakváltozat, nem csak ékezet. Ez utóbbi az N-F96c-hez tartozik.

**Eredmény.** A DT309 **3 919 tokent** cserél, 10 alakon; a `neki` szabály összesen 5 657 tokenen fut (a *néki* 1 738-a és az új 3 919). Változó vers 13 083 → **14 733**, változó token 29 396 → **33 315**, változó alak 1 580 → **1 590**; a kieső tokenek száma 11 128, változatlan. A modern szövegben nem maradt *nék-* alak.

**A minta.** A `--minta-frissit` 13 sort frissített (M015, M021, M034, M037, M049, M055, M057, M066, M075, M077, M085, M088, M101). Az új cseréket a modell átnézte, mind helyes. A `megjegyzes` oszlopban a korábbi „kimaradt (nincs rá szabály)” helyett ez áll: „DT309: a nék- csere átnézve (jó)”. A csere csak ezt az oszlopot érintette; a többit a szkript soronként összevetette. Az `ellenorzes` értékei megmaradtak. Az „a mi” ellenőrző fájl 109 kitöltött sora a `--ami-proba` újrafuttatása után is megmaradt.

**A K1 a DT309 után** (DT307; modell-ellenőrzés, a felhasználó elfogadta):

| halmaz | eredmény | küszöb | |
|---|---:|---:|---|
| minta, cserék (`→`) | **246 / 246 (100%)** | ≥ 98% | ✓ |
| minta, `valtozatlan` réteg | **0** kihagyás | 0 | ✓ |
| `helyesiras_ami_ellenorzes.tsv`, szövegváltozó sorok | **101 / 102 (99,0%)** | ≥ 98% | ✓ |

**A .1 lezárva.** A K1 teljesül; a .1 ⛔ döntései (DT304 d, DT306, DT307, DT308, DT309) mind 🟢 és alkalmazva. Nyitva marad az N-F96c: az egyedi régi írásmódok (4.8.4) és a *nékie*. A K1 egyedül ezt a lépést nem tartja vissza.

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
| felszólító E/2 *-jál/-jél* (*cselekedjél → cselekedj*) | 92 | 319 | **nem automatikus**, jelölt: DT310 |
| kötőhangzós régi múlt (*mondotta → mondta*, *szólott → szólt*) | 89 | 658 | **nem automatikus**, jelölt: DT310 |
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

**A Strong a kieső tokeneken (DT314).** `scope=a kieső tokenek a #22 párosított könyveiben | forras=adat/karoli_modern/igealak_tokenek.tsv + adat/karoli_strong/szavak_*.tsv | ts=2026-10-24` — a réteg Strongot nem tárol (DT305); a mérés azt nézi, elveszhet-e Strong-illesztés.

| kieső token | Strongos | a Strong a gazdaszón is ott van | csak a kieső tokenen | Strong nélkül (betoldás, függőben) | a könyv nincs párosítva |
|---|---:|---:|---:|---:|---:|
| összevont „a” | 5 572 | 5 315 | **257** (főleg H0834) | 3 865 | 1 691 |
| segédigei *vala* | 38 | 1 | **37** (mind H1961) | 1 688 | 721 |

A kieső sor a táblában megmarad (kulcs + `kieso`), ezért egy Strong-illesztés sem vész el. A modern szövegben a 294 tokennek nincs saját szava: a `kieso_gazda` oszlop a gazdaszó sorszámát adja (az összevont „a”-é a következő token, a segédigei *vala*-é az előző). A kereső (#137) ide köti a Strongot. A kulcs-lefedettség gépi igazolása a .3-ban (K3b).

### 5.3 LLM-ellenőrzés és tő-őr (DT303)

A nem automatikus igealak-jelöltek (ritka jegyes és régies gyanús alakok; **3 174 kisbetűs alak**) LLM-kérdésként mentek: alak, szótári alak, jegy és az első előfordulás versrészlete, a szabály jelöltje nélkül (vak ellenőrzés). Előfizetésből futott (Claude Code subagent, **claude-sonnet-5-5**, a .0 mérésének modellje), API és `PARDES_API_KEY` nélkül. Öt köteg: az elsőben 420 alak, ±8 szavas versrészlettel; a többi négyben 689 alak, ±5 szóval. Minden kérdésre jött válasz, 3 174 / 3 174 (`adat/karoli_modern/igealak_llm.tsv`, modell-kimenet, `modell_ellenorizetlen`).

| osztály | tő-őr | szabály = LLM | alak |
|---|---|---|---:|
| ritka jegyes | ok | egyezik | 2 400 |
| ritka jegyes | ok | eltér | 296 |
| ritka jegyes | bukott | — | 75 |
| régies gyanú | ok | nincs szabály-jelölt | 426 |
| régies gyanú | ok | egyezik / eltér | 133 / 34 |
| régies gyanú | bukott | — | 86 |

A ritka jegyes alakokon a szabály és az LLM **2 400 / 2 771 alakon egyezik (86,6%)**. Az eltérések (modell-átnézés, 30 elemes szúrópróba) főként jegyhibák, és ott az LLM-nek van igaza: nem ige (*félénk, felirata, haladék, erősebbé*), a mai alak hibás E/2 jeggyel (*elmentél, elvesztél*), a magas hangrendű *-ék* E/3-a (*elutazék → elutazott*). A szenvedő *-taték/-teték* (*kiadaték → kiadatott*) és az *-ik*-es *-ék* E/3-a erre szabályjavítást kapott. Az LLM is hibázik: *játszék → játsszon*, *keltének* változatlan, a tárgyas/alanyi választás. A tő-őr főként két esetben bukik: a helyesírási ékezetnél (*kinyujtá → kinyújtotta*: a tő-őr a .1 utáni alakot nézi), és ott, ahol az LLM a *-nd-* jövő időt jelenre írta (*mondándom → mondom*, *leendesz → leszel*). Ez utóbbi helyes kiszűrés: igeidő-váltás. A jelölt a modern szövegbe nem kerül be; az alkalmazás a DT311 döntése.

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

A becslés (a brief 0,05–0,2 M-ja, illetve a DT303 ≈ 0,45 M-os kerete, a .0 API-mérése alapján, alakonként 132,5 token) **a teljes számítás szerint kb. háromszorosan túllépve: 1,42 M**, alakonként 447 token. A cache-olvasás nélkül (új bemenet + kimenet) **0,60 M**, ez is a keret felett. Az ok a subagent saját rendszerpromptja és eszközleírása (hívásonként kb. 57 ezer token), amely minden hívásnál újra beolvasódik; a .0 API-mérésében ez nem volt. Az első köteg (fájlba író beállítás) után a többi kötegnél csak egy olvasás és a válasz a hand-back üzenetben: alakonként 382 token. A keret kérdése: DT312.

**Az opus-ellenőrzés** (5.3b; `adat/karoli_modern/igealak_llm_opus_hivasok.jsonl`):

| köteg | alak | hívás | bemenet (új + cache-írás) | cache-olvasás | kimenet | összesen |
|---|---:|---:|---:|---:|---:|---:|
| opus 1 | 430 | 2 | 87 053 | 57 300 | 12 735 | 157 088 |
| opus 2 | 430 | 2 | 87 025 | 57 300 | 10 972 | 155 297 |
| **összesen** | **860** | 4 | **174 078** | **114 600** | **23 707** | **312 385** |

Alakonként 363 token. **A .2 LLM-felhasználása összesen 1 732 172 token** (sonnet 1 419 787 + opus 312 385); cache-olvasás nélkül 0,80 M. Az opus-futás a DT312 nyitott kérdése mellett, a felhasználó külön kérésére ment.

A .2 determinisztikus része (szabályok, *vala*, minta) 0 token.

### 5.5 Lefedettség — maradt-e régies igealak

A modern szövegben maradó régies igealak, tokenben: ritka jegyes **6 734** (ebből jelölttel 6 706), régies gyanú **3 685** (jelölttel 3 592), gyakori jegyes **241** (a felszólító *-jál* és a jelölt nélküli 5 alak), a *vala*-család 34 (a bizonytalan segédige), *lőnek* 2, *vagyon* 1. Összesen **10 697 token** régies igealak marad, ebből 10 439 jelölttel. Ha a DT311 szerint a szabály + LLM egyező, tő-őrön átment ritka jelöltjei bekerülnek, ez 5 771 tokennel csökken (a 2 400 alak tokenje). A gyanú-heurisztika alsó becslés (napló 1.2): a jegy nélküli, a heurisztikán kívül eső régies alak nem számolódik. A *-nd-* jövő (*mondándok, leend*) egy tokenben nem írható át (a mai alak két szó: *mondani fogok*); jelöltként marad.

### 5.6 A minta (⛔ felhasználói ellenőrzés)

`adat/karoli_modern/igealak_minta.tsv`: rögzített magú (20261024), rétegzett minta, **120 vers**, 20 réteg. A rétegek: jegyenként a gyakori igealak; a tárgyas/alanyi heurisztika; az *-ék* E/1/T/3; *lőn*, *vagyon*, a gyanú kézi listája; a *vala* négy esete; a ritka és a gyanús jelölt; a felszólító *-jál*; a kötőhangzós múlt; és változatlan vers. Oszlopok: `szoveg_1908`, `szoveg_modern` (a .1 + .2 után), `valtozasok` (a `[.2]` jelű a .2 cseréje, a `?(…)` a bizonytalan jelölés), `jelolt` (a nem automatikus jelöltek: `szabaly:` és `llm:` a tő-őr eredményével), `ellenorzes` és `megjegyzes`. Az utolsó kettőt a felhasználó tölti: *jó* / *hibás*, a jelölt soron *A* = a jelölt jó, *B* = maradjon. A modell nem tölti ki őket. A K1 küszöbét és mérési egységét a felhasználó adja a mérés előtt (a .1 DT-F96h-ja a .1-re szólt; a delegálás a .2-re nem érvényes).

### 5.7 A döntések alkalmazása és a K1 (DT310, l, m, n)

`scope=a Károli 1908 minden verse és tokenje; a minta 120 sora | forras=mint 5., + adat/karoli_modern/igealak_llm_opus.tsv | ts=2026-10-24` — `python eszkozok/karoli_modern/igealak.py --minta-frissit`; 0 token.

**A felhasználó döntése** (chat, 2026-10-24: „Mehet” a javaslatokra): DT312 1. (a túllépés elfogadva; a keret a teljes számítással, cache-olvasással mérve; minden további LLM-futás előtt kötegszám és becslés, jóváhagyással); DT310 (b) igen, (a) marad; DT311 2. opció; DT313 1. opció, a minta modell-ellenőrzéssel, a felhasználó elfogadására.

**Alkalmazva.**
- **DT310 (b):** a kötőhangzós régi múlt automatikus csere, korpusz-támasszal. Ez **620 token**: *szólott → szólt* 144, *mondotta → mondta* 91, *állott → állt* 58, *megmondotta → megmondta* 46 …
  - Kimarad a melléknévi igenév (*halott*, *törött*, *elbizakodottak*, *megölöttek*): az E/3 és a T/3 alanyi csak a `KOTOHANG_IGE` listán cserél.
  - Kimarad a más igéhez tartozó alak (*születtél*: születik; *elveszett*: elvész; *küldettem*, *kiűzettek*: szenvedő) és a *körülött-* névutó.
- **DT310 (a):** a felszólító *-jál* (319 token) változatlan; a jelölt a mintában marad.
- **DT311, 2. opció:** a ritka és a gyanús jelölt cserél, ha a szabály, a sonnet és az opus közül legalább kettő egyezik, és a tő-őr átengedi. Ez **6 866 token**: szabály + sonnet 6 041, sonnet + opus 663, szabály + opus 160 …
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

**A K1** (DT313; modell-ellenőrzés, claude-opus-5-5; **a felhasználó elfogadására vár**):

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

**A .2 lezárva** (felhasználó, chat, 2026-10-25: „Mehet” a K1 elfogadására): a K1 a modell-ellenőrzés alapján teljesül (313 / 316, 99,1%), a DT310, l, m, n, o mind 🟢 és alkalmazva.

## 6. F96.3 — a kiadott tábla

`scope=a Károli 1908 minden verse és tokenje (31 158 vers, 599 367 token) + a #22 párosítás 61 könyvének Strongos magyar tokenjei | forras=konkordancia/Karoli_1908.tsv + adat/szoto/karoli_szotari_alak.tsv + adat/karoli_modern/helyesiras_tokenek.tsv + igealak_tokenek.tsv + igealak_llm.tsv + igealak_llm_opus.tsv + adat/karoli_strong/szavak_*.tsv; a teljes sha256 a táblák fejlécében | ts=2026-10-25` — `python eszkozok/karoli_modern/karoli_modern.py`; 0 token.

**Kimenet** (SEMA 2.34):
- `adat/karoli_modern/karoli_modern.tsv`: token-soronként a teljes szöveg (599 367 sor, 19,6 MB).
- `adat/karoli_modern/karoli_modern_versek.tsv`: versenként a modern szöveg (31 158 sor, 4,6 MB).

A brief .3 egy táblát írt le, „token-soronként, a vers-kulccsal és a modern vers-szöveggel együtt”. A versszöveg minden tokensorban ismétlődne (kb. 90 MB, a GitHub 100 MB-os fájlkorlátja közelében), ezért a tokensor és a versszöveg két táblába került, közös vers-kulccsal. A K4b (keresésre alkalmas, token-szintű tábla) így teljesül.

**Ellenőrzések** (mind lefutott, eltérésnél a szkript megáll):

| | eredmény |
|---|---|
| a .1 újraszámolása = `helyesiras_tokenek.tsv` | 33 323 / 33 323 sor egyezik |
| a .2 újraszámolása = `igealak_tokenek.tsv` | 65 195 / 65 195 sor egyezik |
| K2 (a modern versszöveg újratokenizálva = a nem kieső tokenek modern alakja; írásjel-váz) | minden versen átment |
| K3 (versenként a tokenek száma és sorrendje = a `tokenizal` 1908-as kimenete) | minden versen átment |
| **K3b** (DT314: a #22 minden Strongos magyar tokenjének kulcsa a táblában, azonos 1908-as alakkal) | **418 633 / 418 633** (61 könyv); ebből kieső, a `kieso_gazda`-n át illeszthető: 5 572 összevont „a” és 38 segédigei *vala* |

**Számok:** 48 121 token változik (.1 + .2, a kieső tokenek nélkül), 13 578 kiesik (11 128 összevont „a”, 2 450 segédigei *vala*), és 21 255 vers változik. A Strong egy tokenen sem vész el és nem változik: a réteg Strongot nem tárol, a kulcs változatlan.

**Licenc:** `adat/licencek.tsv` `karoli_modern` sor. A projekt saját adata, a Károli 1908 közkincs. Strong-oszlop nincs, ezért TAHOT/TAGNT-összetevő sincs; a Hunspellből alak nem került be (DT301).

**Nyitott, a #96-on kívül:** N-F96c (egyedi régi írásmódok: *Pezsdűljenek, eledelűl, nékie*), N-F96a / #137 (a `pardes.db`-be töltés és a kereső; a DT314 kötelező pontja). A K5-ből hátravan a CI és a független ellenőr.

## 7. A független ellenőr első köre és a javítások

`scope=a #96 diffje (61714f36..b21871f) és a javítás után a teljes réteg | forras=naplok/ELLENOR_F96.md (1. kör, ELTÉRÉS: 11 tétel) + a 6. szakasz bemenetei | ts=2026-10-25` — `python eszkozok/karoli_modern/helyesiras.py --minta-frissit`, `--ami-proba`, `python eszkozok/karoli_modern/igealak.py --minta-frissit`, `python eszkozok/karoli_modern/karoli_modern.py`; 0 token.

**A felhasználó döntése** (chat, 2026-10-25: „Mehet”): a javasolt besorolás szerinti javítás, és a DT315 1. opciója.

| tétel | javítás | ellenőrzés |
|---|---|---|
| **ELT-1** „-ik ige + volt” (32 eset) | `igealak.py` `VALA_ELOTT_KEZI`: a 37 „-ik + vala” esetből a 29 igei alak (32 token; a 34 a 8. szakasz előtti elírás) kézzel átnézett múlt idejű alakja, a *vala* kiesik (*szégyenlik vala → szégyenlették*, *igyekszik vala → igyekezett*, *kínlódik vala → kínlódott*). A *kik, második, kisebbik, betegeik, kérdéseik, mellvértjeik* nem ige, marad. | a versek táblán `\w+ik volt`: csak *második* (3), *hetedik*, *kisebbik* |
| **ELT-2** a .1 nyitott hibái (napló 4.1.5) | `helyesiras.py` `ALAK_KIVETEL`: *keménynyakú(ak)* változatlan (összetételi határ), *paizszsal → pajzzsal*, *strucz → strucc*, *struczok → struccok*, *struczmadarak → struccmadarak* | 22 `kivetel` sor: 17 csere (*pajzzsal* 7, *strucc-* 10), 5 változatlan (*keménynyakú(ak)*) |
| **ELT-3** tárgyas-heurisztika | `targyrag()`: az „a/az + -t” csak akkor tárgy, ha a *-t* (*-at, -et* …) nélküli tő szó a korpuszban (*a kárpit* nem tárgy) | 2Móz 36:16: *Csináltak ötven hurkot … csináltak* |
| **ELT-4** a K1 három hibája | `igealak.py` `TOKEN_KIVETEL`: igehely + sorszám szerinti kivétel, az *evék* és a *tevék* minden előfordulásán átnézve. 7 token: a *tevék* főnév (1Móz 24:63, Ez 25:5) változatlan; *ették* (Ján 6:58, 2Móz 16:35); *tettem* (Neh 13:21, Dán 9:4, Jer 35:5). A Jel 12:2 az ELT-1-gyel javult. | a minta G020, G046, G084 sora jó |
| **ELT-5** DONTESEK DT303/e | az oszlopcsúszás javítva (Állapot 🟢, Döntés, Napló) | 8 oszlop |
| **ELT-6** bontás | l. lent (`igealak_alakok.tsv`) | |
| **ELT-7** elavult fejlécek | a minták fejléce: „a felhasználó tölti, vagy a felhasználó által elfogadott modell-ellenőrzés”; az `igealak_alakok.tsv` fejléce a DT311 szerint; a .2 mintájának `megjegyzes`-e: „a felhasználó elfogadta (chat, 2026-10-25)” | |
| **ELT-8** `ir` lista | a brief `ir` mezője kiegészítve: `naplok/ELLENOR_F96.md`, `adat/SEMA.md`, `adat/licencek.tsv`, `DONTESEK.md`, `F137_KAROLI_MODERN_DB_BRIEF.md` | |
| **ELT-9** token-keret | nincs teendő: dokumentált, utólag jóváhagyva (DT312) | |
| **ELT-10** verziószámok | a brief címsora v1.5; a napló fejléce; a DT312 szövege a sonnet- és az opus-számot szétválasztja | |
| **ELT-11** bemeneti hash | a `karoli_modern.py` `BEMENETEK`-je kiegészül: `tokenek.py`, `fedettseg.py`, és a K3b bemenete (`adat/karoli_strong/szavak_*.tsv`, 61 fájl, összesített sha256) | a táblák fejléce |

**DT315** (a *j* nélküli birtokos T/3, alkalmazva):
- A szabály: *-ök → -ük* (ragokkal is: *kezökbe → kezükbe*), ahol a tő többese a korpuszban *-ek* (*szív → szívek*), és nem *j* előzi meg. A *nemök* kézi listából jön (a *nemek* nem áll a korpuszban).
- Kizárva a ragtalan *-tök* *t*-végű tövön, mert az múlt idejű T/2 ige (*ültök, jöttök, megöltök, készültök*; 17 alak). Kivétel: *érettök, értök* (névmás).
- A 195 kisbetűs jelöltalakot a modell átnézte (17 igealak kizárva); a táblában **182 alak** (kis- és nagybetűsen külön számolva: *Istenök, istenök*) és **911 token** cserél: *velök → velük* 220, *ellenök → ellenük* 66, *szívök → szívük* 42, *Istenök → Istenük* 37, *nemzetségök* 19, *lelkök* 18, *szemök* 17 …
- A névelő utáni alak is cserél (*a kezökbe*): a névelő-próba csak az igealak-jelöltekre fut.
- A mély hangrendű *-ok* (*házok*) nem cserél, mert a próba ott hamis találatot ad (*gonoszok, akartok*).

**ELT-6, az `igealak_alakok.tsv` bontása** (4 221 adatsor a javítás után; az 1. körben 4 039):

| osztály × alkalmazás | alak |
|---|---:|
| `igealak_ritka` × jelolt (a többségi csere tokenszinten, DT311) | 2 879 |
| `regies_gyanu` × jelolt | 678 |
| `igealak_gyakori` × szabaly | 318 |
| `valtozatlan` × szabaly (kötőhangzós múlt, DT315, kézi gyanúlista) | 235 |
| `regies_gyanu` × szabaly (kézi lista, kötőhangzós múlt) | 76 |
| `regies_lista` (vala 10, lőn 3, vagyon 1, egyéb 1) | 15 |
| `igealak_ritka` × valtozatlan (igenév-kivétel) | 8 |
| `igealak_gyakori` × jelolt (felszólító *-jál*) | 6 |
| `igealak_gyakori` × valtozatlan (KEZI: jegyhiba, igenév-kivétel) | 5 |
| `tablan_kivul` × szabaly | 1 |

**A K1 a javítás után** (modell-ellenőrzés, a felhasználó elfogadta):
- A minta automatikus cseréi: **319 / 319 (100%)**, a változatlan rétegben 0 kihagyás.
- A minta 6 sora változott; mind átnézve, jó: a G020, G046 és G084 javult, a G071 és G113 a DT315, a G091 az ELT-3 miatt változott.

**Az újragenerálás igazolása** (a független ellenőr szerepköre a futtatást nem engedte, ezért itt):
- A .3 generátora a .1-et és a .2-t újraszámolja, és soronként összeveti a kiadott táblákkal: `helyesiras_tokenek.tsv` 33 318 sor, `igealak_tokenek.tsv` 66 131 sor, egyezik. A K2 és a K3 minden versen átment.
- A K3b: 418 633 / 418 633 Strongos token a táblában, azonos 1908-as alakkal. A K3b 61 könyvre igazol: a #22 párosításában nincs még **Mt, Mk, Lk, Ján, ApCsel** (`adat/karoli_strong/szavak_*.tsv`); ezeken a Strong-illesztés a #22 dolga.
- A réteg számai: 49 025 token változik, 13 610 kiesik (11 128 összevont „a”, 2 482 segédigei *vala*), 21 454 vers változik.

**Mérési melléktábla, nem frissítve:** a `helyesiras_hunspell.tsv` (DT301, csak mérce) az ELT-2 előtti alakpárokra szól. A Hunspell-futtató a sessionben nem fut újra; a kiadott rétegbe Hunspell-alak nem kerül, ezért a tábla a 4.1 mérés lenyomata marad.

**Lefedettség:** a modern szövegben maradó régies igealak 1 146 token (az ELT-1 a létigeinek vett *vala* előtti igét javította, ezért a számot nem változtatja): felszólító *-jál* 319 (marad), *-nd-* jövő 147, régies gyanú 294, ritka jegyes 214, gyakori jegyes 135, *vala*-család bizonytalan 34, egyéb 3.

## 8. A független ellenőr második köre és a javítások

`scope=a #96 diffje (61714f36..ca95eb3) és a javítás után a teljes réteg | forras=naplok/ELLENOR_F96.md (2. kör, ELTÉRÉS: 6 tétel) + a 6. szakasz bemenetei | ts=2026-10-25` — `python eszkozok/karoli_modern/igealak.py --minta-frissit`, `python eszkozok/karoli_modern/karoli_modern.py`; 0 token.

**A felhasználó döntése** (chat, 2026-10-25: „Mehet”): mind a hat tétel javítása, a jelöltek teljes átnézésével. Ez a javítókörök szabálya szerinti utolsó újraellenőrzés előtti kör.

| tétel | javítás | ellenőrzés |
|---|---|---|
| **ELT-1 maradéka** (nem *-ik* végű jelen idejű ige + *vala → volt*) | A létigeinek vett *vala* előtt álló, jelen idejű végződésű szavak (255 alak–vala pár) mind átnézve. A 37 igei alak a `VALA_ELOTT_KEZI`-be került (*ásnak vala → ástak*, *járkálnak vala → járkáltak*, *vigasztalják vala → vigasztalták*, *meri vala → merte*, *gyötri vala → gyötörte*, *lőnek vala → lőttek* (1Krón 12:2, nyíllal), *vész vala → veszett*). 4 már múlt idejű alak után (*tusakodtatok, etettelek, tévelyegtem, vendégeskedtek*) csak a *vala* esik ki (`VALA_ELOTT_MULT_KEZI`). A többi szó névszó (*fiai, olyanok, velük, embernek* …), ott a *vala* helyesen *volt*. | a lista újrafuttatva: csak névszó maradt |
| **N-1** E/1 tárgyas elbeszélő múlt *-ám/-ém* | Új szabály (`mult_E1_targyas`): az *-ám/-ém* alak, ha az E/3 tárgyas párja (*mondá*) a #94 táblában `mult.targyas.E3` jegyű. A mai alak a jegy szerinti E/1 (*mondám → mondtam*, *látám → láttam*, *hallám → hallottam*). A 131 alakot a modell átnézte; az `E1_TARGYAS_KEZI` felülbírálja az *elvégzém → elvégeztem*, *kérdém → kérdeztem* alakot, az *értém* kimarad (*értem* 'miattam' is). A névutók (*elém, felém, alám*) nem esnek a szabály alá: nincs jegyes E/3 párjuk. **430 token.** A hangrend javítva: a csak *i/í* hangú *-ít* ige mély (*megtisztítám → megtisztítottam*). | a versek táblán *mondám, látám, hallám, adám*: 0 |
| **N-2** *ellenek vala → ellentem* | `VALA_ELOTT_KEZI`: *ellenek → elltek* (1Móz 30:39, 31:8; 3 token) | |
| **ELT-7** fejlécek | Az `igealak_minta.tsv` fejlécéből kikerült az önellentmondó „a modell nem”. Az `igealak_tokenek.tsv`, az `igealak_alakok.tsv` és a minta fejléce a DT311 szerinti cserét írja le. A `karoli_modern.tsv` fejléce minden kivételtáblát felsorol (`ALAK_KIVETEL`, `VALA_ELOTT_KEZI`, `VALA_ELOTT_MULT_KEZI`, `TOKEN_KIVETEL`, `E1_TARGYAS_KEZI`, `OK_KEZI`), és a K1-et a 8. szakaszra hivatkozza. Az `igealak.py` docstringje is a DT-F96l-et írja. | |
| **N-3** a 7. szakasz számai | javítva a 7. szakaszban: 32 token (nem 34); 22 `kivetel` sor (17 csere, 5 változatlan); 182 alak (kis- és nagybetűsen külön) | |
| **N-4** az `igealak_tokenek.tsv` bontása | l. lent | |

**N-4, az `igealak_tokenek.tsv` változásának bontása** (új / eltűnt kulcs, a csere szabálya szerint):

| kör | sorok | Δ | bontás |
|---|---:|---:|---|
| 1. javítókör (`73b16a1 → 8aa3799`) | 65 195 → 66 131 | +936 | +911 `ok_birtokos` (DT315), +32 `jelen_mult_vala` (ELT-1: a *vala* előtti ige; a *vala* sora már bent volt), −5 `karakter` (a *keménynyakú(ak)* változatlan, ELT-2), −2 `token_kivetel` (a *tevék* főnév, ELT-4) |
| 2. javítókör (`8aa3799 → 8.`) | 66 131 → 66 601 | +470 | +430 `mult_E1_targyas` (N-1), +40 `jelen_mult_vala` (az ELT-1 maradéka és az N-2; a *vala* sora már bent volt) |

**A K1 a javítás után** (modell-ellenőrzés, a felhasználó elfogadta): a minta automatikus cseréi **322 / 322 (100%)**, a változatlan rétegben 0 kihagyás. A 2. körben 3 sor változott (G050 *mondtam*; G051 az *etettelek vala* *vala*-ja kiesik; G068 *megöltem, elhoztam*), mind átnézve, jó. A korlát marad: a mintahibák egy részét a mintatokenekre is ható kézi kivétel javította, így a 100% ugyanazon a mintán nem független becslés (DT307).

**Az újragenerálás igazolása:** a .3 generátora a .1-et és a .2-t újraszámolja, és soronként összeveti a kiadott táblákkal: `helyesiras_tokenek.tsv` 33 318 sor, `igealak_tokenek.tsv` 66 601 sor, egyezik. A K2 és a K3 minden versen átment. A K3b: 418 633 / 418 633 (61 könyv; a kieső, Strongos tokenek: 5 572 összevont „a”, 40 segédigei *vala*). A réteg: 49 449 token változik, 13 657 kiesik (11 128 összevont „a”, 2 529 segédigei *vala*), 21 516 vers változik.

**Lefedettség:** a régies igealak a modern szövegben 1 145 token (felszólító *-jál* 319 marad; *-nd-* jövő 147; régies gyanú 294; ritka jegyes 214; gyakori jegyes 135; a *vala*-család 34 bizonytalan esete; egyéb 2). A számláló a fedettség osztályain fut (`igealak_gyakori`, `igealak_ritka`, `regies_gyanu`, a *vala/lőn/vagyon*). A `valtozatlan` osztályú régies alakot, amilyen az N-1 *mondám*-ja volt, nem látja. A 2. kör ezért külön kereséssel ellenőrizte az ismert osztályokat (*-ám/-ém*, „ige + volt”).

## 9. A független ellenőr harmadik köre — megállás

`naplok/ELLENOR_F96.md` 3. kör: **ELTÉRÉS, 7 tétel**. Ez a javítókörök szabálya szerinti utolsó újraellenőrzés volt, ezért a végrehajtó nem javít tovább: a tételek nyitott tételként (helyőrzővel) kerülnek a briefbe, és a folytatás a felhasználó döntése.

**Saját hibák, amelyeket a 3. kör kimutatott:**
- A 8. szakasz „a lista újrafuttatva: csak névszó maradt” állítása hamis. Az ellenőrző lista végződésszűrője a ragtalan E/3 jelen időt és a régmúltat (múlt + *vala*) nem fedte.
- Az N-1 ellenőrzése csak négy szót nézett (*mondám, látám, hallám, adám*). A szabály csak azokat az *-ám/-ém* alakokat fogta meg, amelyeknek az E/3 tárgyas párja a #94 táblában jegyes; a többi (*imádkozám, evém, megérkezém*) maradt.
- A 8. szakasz lefedettség-száma (1 145 token) nagyságrenddel alábecsül, mert a számláló a fedettségi mérés `valtozatlan` osztályát nem látja. A 8. szakasz ezt kimondta, de tételt nem nyitott.
- A K1 eljárása (DT307/n) a minta változatlanul maradt régies alakját nem számolta kihagyásnak.

**Nyitott tételek** (a brief döntésnaplójában): **N-F96d** (a `valtozatlan` osztály régies igealakjai), **N-F96e** (a *vala* előtti ragtalan E/3 jelen és a régmúlt), **N-F96f** (az `ek_E1_T3`), **N-F96g** (a K1 mérési eljárása). A 6. (E17: az `igealak_alakok.tsv` +143-as Δ-ja: 143 `mult_E1_targyas` alak, kis- és nagybetűsen külön, kisbetűsítve 129; a 8. szakasz 131-e a felülbírálás előtti jelöltszám) és a 7. tétel (a brief `kovetkezo` mezője) itt és a brief fejlécében javítva.

**A kiadott réteg állapota:** a K2, K3 és K3b teljesül; a Strong változatlan. A cserék a mintán pontosak. A lefedettség hiányos: a fenti osztályok régies alakja a modern szövegben maradt, és egyes mondatokban régi és mai igealak keveredik (Neh 1:4 „bőjtöltem és imádkozám”).

## 10. A 3. kör maradéka: szisztematikus újramérés (DT316) — megállás a DT-F96r-en

**A felhasználó döntése** (chat, 2026-10-25): „1” (szisztematikus újramérés), majd a javaslatra „Mehet a javaslattal” (DT316).

### 10.1 A régies-szken (N-F96d, N-F96e)

`eszkozok/karoli_modern/regies_szken.py` a kiadott `karoli_modern.tsv`-n (a 3. ellenőri kör előtti réteg, `8b858b3`) fut, a #94 jegyétől és a fedettségi osztálytól függetlenül, a már LLM-kérdezett alakok nélkül. Kimenet: `adat/karoli_modern/regies_szken.tsv`.

| Jelöltkör | Kérdés | Token |
|---|---|---|
| `alak`: változatlan, nem kieső token régies végződéssel (minden *-á/-é*, a névutók és a mondatbelseji nagybetűs nevek nélkül; *-ának/-ének, -ánk/-énk, -átok/-étek, -aték/-eték, -ád/-éd, -ám/-ém, -ál/-él, -ák/-ék, -ván/-vén*, ha a tő igei) | 1 354 | 3 702 |
| `vala`: a létigeinek vett *vala* előtti szó, ha ő maga vagy a töve igei | 162 | 342 |

A szabály-jelölt a végződés szerinti mai alak (`igeragozas.mult`). Szövegkörnyezetfüggő:
- az *-ék*-en `E1=…|T3=…`; az *-ik*-es igén E/3 alanyi; ha a T/3 tárgyas alak a korpuszban nem áll, csak E/1 (*elájulék → elájultam*);
- az *-ának/-ének*-en `alanyi=…|targyas=…`, ha a tárgyas alak a korpuszban áll.

### 10.2 Az opus-futás (K4)

Vak, versrészlettel (±6 szó), 4 köteg (380/380/380/376), Claude Code subagent, előfizetésből, API nélkül. A modell mind a négy átiratban `claude-opus-5-5`. Az utasítás a kérdésekkel együtt a repón kívül maradt; az eredmény az `adat/karoli_modern/igealak_llm_kor3.tsv` és a hívásnapló.

| | Token |
|---|---|
| összesen (8 hívás) | **595 232** (becslés: 0,55 M; +8%) |
| kötegenként | 148 137 – 149 815 |
| ebből cache-írás / cache-olvasás / kimenet kötegenként | kb. 83 000 / 56 900 / 8 300–9 800 |

Az opus 514 alakot változtatna. A *vala*-párokból 67-et segédigeinek ítélt, 95-öt létigeinek (`-`).

### 10.3 Alkalmazás (`igealak.py`, DT316)

| | Token | Alak |
|---|---|---|
| csere: az opus és a szabály-jelölt egyezik, a tő-őr átengedi (`kor3:szabaly+opus`) | 690 | 420 |
| jelölt marad (eltérés vagy bukott tő-őr; a `jelolt` oszlopban `kor3_szabaly`, `kor3_opus`) | 129 | 86 |
| csak opus, szabály-jelölt nélkül (`kor3:opus`) | 0 | 0 |
| *vala* kiesik (`vala_segedige_kor3`, `bizonytalan=kor3_csak_opus`) | 71 | — |
| ebből az előtte álló ige múlt időbe kerül (*háborog → háborgott, szakadoz → szakadozott, fér → fért*) | 13 | 9 |

A jelölt maradt alakok két csoportja:
- a szabály a hibás: *bévevé → bévevte*, *átköltözteté → átköltöztetta*, *felfegyverzé → felfegyverzette*; az opus jó;
- a tő-őr a régi tövön bukik: *evém → ettem*, *ivám → ittam*, *felűlének → felültek*; itt a két forrás egyezik.

A DT316 szerint ezek nem cserélnek.

A szabály-jelölt nélküli alakok (főnév *-vá/-vé*, birtokos *-é*, igenév) mind változatlan választ kaptak. Ezért csak opus-csere alakon nincs, csak a *vala*-n.

A homográf-őrhöz (`KOR3_VALA_HOMOGRAF`) egy próbahiba vezetett. A *vala*-párok alakszintűek, és a *mert vala* a Luk 8:42-ben kötőszó („Mert vala néki egy egyetlen leánya”). A *mert* ezért csak tagadószó után ige (Mt 2:22: *nem mert vala* → *nem mert*).

### 10.4 Az `ek_E1_T3` (N-F96f)

Új szabály: E/1, ha a token mondatszakaszában (a `.;:!?` jelek között) E/1 igealak áll. Ilyen az *-ám/-ém* E/1 tárgyas elbeszélő múlt (*mondám*, N-1, vagy a szken E/1-jelöltje), a *valék*, a *vagyok* és a *leszek*. E/1 akkor is, ha a token előtt E/1 névmás áll, a birtokos *az én* nélkül. A tárgyatlan *felelék* és *-jövék* mindig E/1 (`E1_MINDIG_VEG`).

A próbák három tágabb változatot elvetettek:
1. **Versszintű E/1** (igealak és névmás az egész versben): hibás E/1 az idézett beszéd miatt (Mt 26:22 *kezdék …: Én vagyok-é*, Ján 9:15, 1Móz 25:30 *fáradt vagyok. Ezért nevezék*), és más mondat E/1-e miatt (Dán 7:13 *Látám …; eleibe vivék őt*).
2. **Igealak a mondatszakaszban, névmás a vers elbeszélő részében:** hibás E/1 az 1Móz 41:24 (*elnyelék a … gabonafejek … nékem*), a Neh 2:18, a Jób 1:15, az Ez 9:6 és az Ez 23:38 (*az én szent helyemet*) versben.
3. **Igealak és névmás is a mondatszakaszban, a token után is:** hibás E/1 a Jób 1:17-ben (*ölék meg, csak én magam*).

A kiadott változatban **17 token** került T/3-ról E/1-re, és mind helyes. Ide tartozik a *felelék* (1Móz 31:11, 2Sám 1:8, Neh 2:20, Jer 1:13, 11:5, Zak 4:4, 4:11, 4:12), az *eljövék* (ApCsel 24:17), az *elküldék* (1Thessz 3:5), a *gyűjték* (Ezsd 7:28), a *rendelék* (Neh 12:31, 13:19), a *megverék* (Neh 13:25), a *Körültekinték* (Ézs 63:5) és a *vevék* (5Móz 1:23, 1Sám 13:12).

Ami a szűkítés miatt T/3 maradt: az 1Móz 39:15 *kezdék* (helyesen E/1), a Dán 7:16 *kérék* és az Ez 22:30 *keresék*. Ezek `ek_E1_T3` jelölésűek, mint korábban; a jelölés összesen 681 tokenen áll.

### 10.5 Újragenerálás

- **`igealak_tokenek.tsv`:** 66 601 → 67 432 sor (+831). Egy sor sem tűnt el.
- **A régi minta:** a `--minta-frissit` négy sort változtatott (G022 *összefoglalák*, G051 *rakád*, G083 *vévén*, G097 *kirántá*). Mind a négy kihagyás volt a 3. kör előtt, most helyes csere; átnézve.
- **.3 (`karoli_modern.py`):** a .1 és a .2 újraszámolva egyezik; a K2 és a K3 minden versen, a K3b mind a 418 633 Strongos tokenen teljesül. A Strongos kieső *vala* 38 → 40 (a gazdaszón át illeszthető, DT314).
- **Változó token:** 50 078. A 9. szakasz keveredés-példája (Neh 1:4 „bőjtöltem és imádkozám”) most: „bőjtöltem és imádkoztam”.

### 10.6 Az új K1 (N-F96g): a lefedettséget is mérő minta

`adat/karoli_modern/igealak_minta2.tsv`, rögzített mag 20261025, 140 vers. A rétegek: 100 egyenletes véletlen vers (a lefedettség mércéje), 20 kor3-csere, 10 kor3-*vala*, 10 `ek_E1_T3`.

Az ellenőrzés vak opus-subagent (`claude-opus-5-5`, 150 065 token) volt. A szöveget ismerte, a szabályokat és a kiválasztás okát nem. A vers minden régies igealakját számolta, a *vala*-t és az *-ök* birtokost is: a rossz csere hiba, a változatlanul maradt régies alak kihagyás.

| Réteg | Csere | Hiba | Kihagyás |
|---|---|---|---|
| véletlen (100) | 89 | 0 | 10 |
| kor3 (20) | 67 | 0 | 6 |
| kor3-*vala* (10) | 25 | 0 | 0 |
| `ek_E1_T3` (10) | 25 | 0 | 2 |
| **összesen** | **206** | **0** | **18** |

- **A cserék pontossága:** 206/206 (a DT313 ≥ 98%-a teljesül).
- **A lefedettség a véletlen rétegen:**
  - igealak: 89 / (89 + 7) = **92,7%**;
  - az *-ök/-ok* birtokossal együtt: 89 / 99 = 89,9%.
- **Korpuszbecslés:** 7 igealak-kihagyás 100 versben, 31 158 versre kb. 2 200 token. A 95%-os Poisson-sáv kb. 900–4 500.

**A kihagyások** (18):
- **8 token *-ok/-ök* birtokos:** *előttök, közülök, rajtok, szivökben, szomjúságokban, szavoknak, uroknak, magoknak*. A DT315 (1. opció) a mély hangrendű *-ok*-ot és a *-ek* többes nélküli tövet szándékosan kihagyta.
- **10 token igealak:**
  - v-tövű *-ék*: *megnyugovék, körülvevék* (a szken igei próbája nem ismerte fel a tövet);
  - *-a/-e* E/3 alanyi elbeszélő múlt: *megfullada, felüle* (a szken végződéslistájában nincs, mert névszóval egybeesik);
  - ható ige régies raggal: *késhetének, tűrhetém*;
  - *felzúdíták* és *cselekedik vala* (a szken nem jelölte);
  - jelöltként maradt: *hivék* (a szabály, a sonnet és az opus három különböző alakot ad) és *dícsérvén* (csak szabály-jelölt van).

**A maradék-szken** (`regies_szken.py --kimenet`, a repón kívül) az újragenerált rétegen 9 új alakot (11 token: *begöngyölék, eloszlatám, felhalmozák, megnyergelék, vehetének* …) és 3 új *vala*-párt (*csépel, felakasztották, hajigál vala*) talál. Ezeket a szken most azért ismeri fel, mert a 3. kör cseréi a tő igei alakját a korpuszba hozták (*begöngyölte*). A DT316 jóváhagyása egyetlen futásra szólt, ezért ezek nem kerültek újra LLM-re.

**Megállás:** a lefedettségre nincs elfogadott küszöb, ezért a folytatás tartalmi döntés. Helyőrzője a **DT317** (🟡, `DONTESEK.md`).

## 11. A 4. kör (DT317, 2. opció) — megállás a DT-F96s-en

**A felhasználó döntése** (chat, 2026-10-25): „2” — még egy kör a 10.6 maradék osztályaira, opus-futással (becslés kb. 0,2–0,3 M token), majd a minta2 újramérése.

### 11.1 A szken (`regies_szken.py --kor 4`)

Bemenet: a 3. kör utáni réteg pillanatképe (`karoli_modern.tsv` és `igealak_alakok.tsv` a `9fd137f`-nél). A kérdésekből a már kérdezett alak és *vala*-pár kimarad (minden LLM-tábla, a kor3 is). Kimenet: `adat/karoli_modern/regies_szken_kor4.tsv`, `S%04d` azonosítókkal.

| Jelöltkör | A 10.6 kihagyása | Kérdés |
|---|---|---|
| igei próba: igekötő + régi tő; v-tő → *-d* (*megnyugov → megnyugod*); ható ige; igeképzős tő (*-ít, -oz, -gat, -ad* …) | *körülvevék, megnyugovék, késhetének, tűrhetém, felzúdíták* | 291 alak (728 token), a következő két kör alakjaival együtt |
| *-a/-e* E/3 alanyi elbeszélő múlt; névszószűrő: kimarad, ha a korpuszban *-ában/-ához/-ával …* esetragos alakja áll | *megfullada, felüle* | (az előző sorban) |
| a csak a .1 által változtatott token, a modern alakján | *dícsérvén* | (az előző sorban) |
| a `vala_nem_elemezheto` *vala* | *cselekedik vala* | 33 pár (42 token) |
| `jelolt`: változatlan (vagy csak a .1-ben változott) jelölt alak, amelyre opus-szavazat még nincs | *dícsérvén* | 161 alak |

A szabály-jelölt a v-tövön *-dik* igét ad (*megnyugovék → megnyugodott*), az igekötő + régi tövön pedig a régi tő mai igéjét (*körülvevék → E1=körülvettem|T3=körülvették*). Ez a javítás a futás után került be: a kérdések és a válaszok változatlanok, csak a szabály-jelölt oszlop számolódott újra ugyanabból a pillanatképből (a `regies_szken_kor4.tsv` 1–4., 6–7. oszlopa azonos).

### 11.2 Az opus-futás (K4)

2 köteg (243 + 242), vak, versrészlettel. A modell mindkét átiratban `claude-opus-5-5`. Összesen **282 897 token** (4 hívás; kötegenként 140 741 és 142 156; a keret 0,2–0,3 M). Eredmény: `igealak_llm_kor4.tsv` és a hívásnapló.

### 11.3 Alkalmazás (`igealak.py`)

| | Token | Alak |
|---|---|---|
| csere, a szabály és az opus egyezik, a tő-őr átengedi (`kor4:szabaly+opus`) | 184 | 119 |
| jelölt marad (`kor4_szabaly`, `kor4_opus` a `jelolt` oszlopban) | 83 | 59 |
| a `jelolt` típus: a DT311 többsége az új opus-szavazattal; valódi szövegváltozás | 10 | — |
| ugyanez, csak a címke bővül (a szabály és a sonnet már egyezett) | 319 | — |
| *vala* kiesik (`vala_segedige_kor4`; az ige múlt időbe kerül: 12 token, *sátoroz → sátorozott, cselekedik → cselekedett, hintenek → hintettek*) | 16 | — |
| a `vala_nem_elemezheto` *vala* létige (`vala_letige_kor4`: Ez 27:8, Ján 3:26) | 2 | — |

Mind a 184 csere igei alak; átnézve egyedi alakonként (119), névszó nem cserélt. A *vive → vitt* a Károliban E/3 elbeszélő múlt.

**Két javítás a próbák alapján:**
- **A .1 cseréje a .2 eredményén** (`h1_atvisz`): a szavazat az 1908-as alakra jött, és a *reáveté → reávetette* visszacsinálta volna a .1 *reá → rá* cseréjét. Ez 3 tokent érintett (3Móz 8:7, Luk 4:40, ApCsel 18:12), a régebbi rétegekben egyet sem.
- **A tő-őr a .1-ben változott tokenen:** a 4. körben a .1 utáni alakon is mér (*harczolának → harcoltak, reáadá → ráadta, körűlvevék → körülvették*).

**Újragenerálás:**
- `igealak_tokenek.tsv`: 67 432 → 67 685 sor, a változó token 50 078 → 50 246;
- .3: K2, K3 és K3b teljesül, a Strong nem változott;
- az `ek_E1_T3` 692 tokenen áll (+7: *körülvevék*, a tagmondat dönt);
- a 4. kör osztályaiban a maradék-szken 0 új jelöltet talál.

**A régi minta:** a G008 (*rávetette, ráadta*), a G044 (*táncoltak*) és a G083 (*felháborították*) korábbi kihagyása javult, átnézve. A G106 *üle* (helyesen *ült*) kihagyás maradt, mert a szken a háromgyűs alakot nem nézi.

### 11.4 A minta2 újramérése

A 140 versből 7 sor modern szövege változott (H001, H025, H047, H078, H110, H120, H135). Ezeket a végrehajtó session (`claude-opus-5-5`) a 10.6 szabályával újraellenőrizte: mind a 7 javítás helyes, új hiba nincs. A többi 133 sor szövege nem változott, ott a vak K1 ítélete érvényes.

| Réteg | Csere | Hiba | Kihagyás |
|---|---|---|---|
| véletlen (100) | 93 | 0 | 6 |
| kor3 (20) | 69 | 0 | 4 |
| kor3-*vala* (10) | 25 | 0 | 0 |
| `ek_E1_T3` (10) | 26 | 0 | 1 |
| **összesen** | **213** | **0** | **11** |

- **A cserék pontossága:** 213/213.
- **A lefedettség a véletlen rétegen:**
  - igealak: 93 / (93 + 3) = **96,9%** (a 3. kör után 92,7%);
  - az *-ök/-ok* birtokossal együtt: 93 / 99 = 93,9%.
- **Korpuszbecslés:** 3 igealak-kihagyás 100 versben, kb. 930 token. A 95%-os Poisson-sáv kb. 200–2 700.
- **Torzítás:** a véletlen réteg 10.6-os kihagyásai jelölték ki a 4. kör osztályait, ezért ezen a rétegen a 96,9% a valódi lefedettséget felülbecsli. Torzítatlan mérés új véletlen mintából lehetséges.

**A maradék kihagyások:**
- **igealak (3):**
  - *hivék*: a szabály, a sonnet és az opus három különböző alakot ad, mert a T/3 alanyi és a tárgyas között a szövegkörnyezet dönt;
  - *megfullada*: a szabály *megfulladott*, az opus *megfulladt*, ezért jelölt marad;
  - *dícsérvén*: az opus *dicsérve*, a szabály *dícsérve*; a .1 ékezetcseréje miatt nincs egyezés;
- **a DT315 hatókörén kívüli *-ök/-ok* birtokos (8):** *előttök, közülök, rajtok, szivökben, szomjúságokban, szavoknak, uroknak, magoknak*.

**Megállás:** a 2. opció végrehajtva, a folytatás (lezárás, ellenőrzés, újabb kör) a felhasználó döntése: **DT318** (🟡, `DONTESEK.md`).

## 12. A jelöltként maradt alakok köre (DT318, 3. opció) — megállás a DT-F96t-n

**A felhasználó döntése** (chat, 2026-10-25): „3” — további kör a jelöltként maradt alakokra. A DT318 ehhez példaként a DT316 eltérés-szabályának lazítását adta ott, ahol a szabály-jelölt bizonyítottan gyenge. Új LLM-futás nem volt: a kör a meglévő szavazatokon dolgozik.

### 12.1 A szabályok (`igealak.py`)

1. **Nem tanúsított szabály-jelölt** (`…:opus_tanusitott`, `bizonytalan=szabaly_nem_tanusitott`):
   - Ha a szabály-jelölt egyetlen értéke sem áll a Károli 1908 korpuszában, az opus-alak viszont igen, és a tő-őr átengedi, akkor az opus-alak cserél. A régi rétegben feltétel még, hogy a sonnet ne adjon más, tanúsított alakot.
   - Nem cserél:
     - ha az alak változatlan;
     - ha az E/3 tárgyas *-á/-é* mai alakja nem *-a/-e* végű: *rombolá → rombolt* hibás, *rombolta* a helyes;
     - ha az *-ék* opus-alakja nem E/1, de a mondatszakaszban E/1 jelző áll;
     - az *-nd-* jövő idő (*adánd*).
2. **A .1 cseréje a szavazatokon:** a szabály-jelöltre és az LLM-alakra (`h1_atvisz`), mielőtt szavaznak (*dícsérve = dicsérve*). Az LLM-jelölt tő-őre a .1-ben változott alakon a .1 utáni alakon is mér.
3. **Alanyi–tárgyas pár** (`tobbseg:alanyi_targyas`, `bizonytalan=targyas_heur`): ha a sonnet és az opus csak a T/3 alanyi és tárgyas ragban tér el (*hittek / hitték*), a tagmondat tárgya dönt.

### 12.2 A próbák hibái

- **Az első próba 95 tokent változtatott.** Ebből:
  - 27 token csak címkét kapott (*higyjetek, csepüvé*);
  - a *rombolá → rombolt* rossz ragozás volt;
  - az *-nd-* jövő idő 100 tokenje cserélt volna, a jelölt-maradék 147 → 47-re esett volna;
  - a 3 *reá*-tokennél (3Móz 8:7, Luk 4:40, ApCsel 18:12) visszalépett a .1, mert az LLM-szavazatot nem normalizáltam.
- Mind a négyet a fenti kizárások javítják.

### 12.3 Eredmény

| Szabály | Token |
|---|---|
| `kor3:opus_tanusitott` (*cselekvé → cselekedte, eltörlé → eltörölte, megszünék → megszűnt, válék → vált, kijövél → kijöttél* …) | 29 |
| `tobbseg:opus_tanusitott` (*megvereték → megveretett, tulajdoníttaték → tulajdoníttatott, aluvék → aludt* (Bír 16:3), *érteté → értette* …) | 22 |
| `kor4:opus_tanusitott` (*felgyullada → felgyulladt, megvirrada → megvirradt, elbágyada → elbágyadt* …) | 7 |
| `tobbseg:alanyi_targyas` (*hivék*: Mk 16:11, Ján 9:18 → *hittek*; Luk 24:37 *azt hivék* → *hitték*) | 3 |
| a normalizálás és a tő-őr tartalékpróbája (*dícsérvén → dicsérve* 6, *dícséré → dicsérte* 2, *körűlmetéltetvén → körülmetéltetve* 1) | 9 |
| **összesen** | **70** |

Mind a 70 csere átnézve, mind helyes.

**Újragenerálás:**
- .2 és .3 újragenerálva; a K2, K3 és K3b teljesül, a Strong nem változott;
- `szabaly_nem_tanusitott` 58 tokenen áll; a változó token 50 307.

### 12.4 A minta2

Két sor modern szövege változott (H024 *hivék → hitték*, H051 *dícsérvén → dicsérve*). Mindkettő korábbi kihagyás volt, mindkettő helyes; a végrehajtó session (`claude-opus-5-5`) ellenőrizte.

| Réteg | Csere | Hiba | Kihagyás |
|---|---|---|---|
| véletlen (100) | 95 | 0 | 4 (1 igealak + 3 *-ök/-ok*) |
| kor3 (20) | 69 | 0 | 4 |
| kor3-*vala* (10) | 25 | 0 | 0 |
| `ek_E1_T3` (10) | 26 | 0 | 1 |

- **A lefedettség a véletlen rétegen:** igealak 95/96 = **99,0%**; az *-ök/-ok*-kal együtt 95/99 = 96,0%.
- **A maradék igealak a *megfullada*:** sem a szabály-jelölt (*megfulladott*), sem az opus-alak (*megfulladt*) nem áll a korpuszban, ezért a 12.1 szerint jelölt marad.
- **Torzítás:** a 11.4 szerint a 99,0% erre a mintára hangolt kör eredménye, a valódi lefedettséget felülbecsli.

**Megállás:** a folytatás a felhasználó döntése, **DT319** (🟡).

## 13. A tokenszintű kör felmérése (DT319, 3. opció) — megállás a DT-F96u-n

**A felhasználó döntése** (chat, 2026-10-25): „3” — további kör, tokenszintű LLM-kérdéssel. A DT312 szerint minden további LLM-futás előtt a keret jóváhagyása kell, ezért a futás előtt felmérés készült.

**A maradék** (`igealak_tokenek.tsv`; a modern szövegben változatlan, `jelolt` oszlopos, nem kieső tokenek, a felszólító *-jál/-jél* és a *-nd-* jövő nélkül):

| Csoport | Token | Alak | Példák |
|---|---|---|---|
| minden LLM-szavazat „változatlan” (nem régies) | 2 747 | 232 | *tett, elment, leszek, tőled, halál, rajtad, egyék* |
| legalább egy LLM-szavazat változtatna, nincs egyezés | 357 | 205 | *higyjetek, egybegyűle, vevén, gyűlölte, megszomorodék, gyűle, tevének, törlé, megnyugovának* |
| csak szabály-jelölt | 13 | 6 | *leűle, űle, felgyűle, könyörűle, megréműle* |

A második és a harmadik csoport (370 token) a tokenszintű kör tárgya. A korábbi körök alakonként kérdeztek, az első előfordulás ±6 (±8) szavas részletével, így a szövegkörnyezetfüggő alakban az egy válasz nem illik minden előfordulásra. Ilyen az alanyi/tárgyas, az E/1/T/3 és az igenév/múlt (*vevén*) különbsége.

**Javaslat** (DT320, 1. opció):
- A kérdés tokenenként szól, a teljes vers szövegével, vakon, 2 opus-kötegben.
- A becslés a 4. kör mért kötegtokenje alapján kb. 0,3 M token: kötegenként kb. 140 ezer a rögzített rész, a teljes vers miatt nagyobb kérdésfájllal.
- Csere akkor van, ha az új válasz egy meglévő forrással egyezik, és a tő-őr átengedi; ez a DT311 kettő-egyezése tokenszinten.
- Utána a minta2 változott sorainak ellenőrzése jön.

**Megállás:** a keret és a cserélési szabály a felhasználó döntése (**DT320**, 🟡).

## 14. Az 5. kör: tokenszintű opus-kérdés (DT320, 1. opció) — megállás a DT-F96v-n

**A felhasználó döntése** (chat, 2026-10-25): „1” — tokenenként, a teljes verssel, vak opus-futás. Csere akkor van, ha a válasz egy meglévő jelölttel egyezik, és a tő-őr átengedi.

### 14.1 A kérdések (`regies_szken.py --kor 5`)

Bemenet: a 4. kör és a jelölt-kör utáni `igealak_tokenek.tsv` (`0dda8b3`). A hatókör a DT320 szerint a modern szövegben változatlan, `jelolt` oszlopos, nem kieső token, a felszólító és a *-nd-* jövő nélkül. Két csoport:
- ahol legalább egy LLM-szavazat változtatna: 357 token;
- ahol LLM-szavazat nincs, és a szabály-jelölt változtatna: 13 token.

Ez **370 kérdés**, `T%04d` azonosítóval, a meglévő jelöltekkel (`regies_szken_kor5.tsv`).

Egy próbahiba: az első változat a csak szabály szerint változó, de minden LLM szerint változatlan tokeneket is felvette (*vége → végett*). Ez 743 kérdés lett volna, ezért szűkítve.

A kérdés a teljes modern vers, a token [szögletes zárójelben]. A helyét a K2 garantálja: a nem kieső tokenek sorrendje a modern szöveg szavaié, eltérésnél a szkript megáll.

### 14.2 A futás (K4)

2 köteg (185 + 185), vak, `claude-opus-5-5` mindkét átiratban. Összesen **285 418 token** (4 hívás; kötegenként 144 936 és 140 482; a keret 0,25–0,35 M). Eredmény: `igealak_llm_kor5.tsv` és a hívásnapló.

### 14.3 Alkalmazás

- **Csere** (`kor5:token_opus+meglevo`, `bizonytalan=token_opus`): **205 token**.
  - A válasz a .1 cseréjével normalizálva egyezik egy meglévő jelölttel, és a tő-őr átengedi (a .1-ben változott tokenen a .1 utáni alakon is mér).
  - Kizárva a *jövén/jővén/lévén* igenév (`IGENEV_KIVETEL`): ez 4 tokent tartott vissza (*eljővén, kijővén* …).
- **Jelölt marad** (`kor5_token_opus` a `jelolt` oszlopban): 106 token. A válasz itt nem egyezik meglévő jelölttel, vagy a tő-őr bukik. A többi kérdésre az opus változatlan alakot adott.
- **Átnézés:** a 147 egyedi alak–eredmény pár mind átnézve, a kétes helyeken a verssel:
  - *aluva találta őket → alva* (igenév);
  - *szerzék → szereztem* (2Sám 7:10, Neh 5:7: E/1);
  - *nevekedének → növekedtek* (a #94 mai lemmája; a réteg korábban is 42 tokenen így cserél);
  - *rombolá → rombolta*, *megfullada → megfulladt*, *űle → ült*.
- **Újragenerálás:**
  - .2 és .3 újragenerálva; a K2, K3 és K3b teljesül, a Strong nem változott;
  - a változó token 50 491, a változó vers 21 620;
  - a .1-visszalépés 0 tokenen.

### 14.4 A minták

- **A minta2:** a H046 (*megfullada → megfulladt*) változott, korábbi kihagyás volt, most jó.
- **A régi minta:** a G106 (*űle → ült*) változott, korábbi kihagyás volt, most jó.

| A minta2 rétege | Csere | Hiba | Kihagyás |
|---|---|---|---|
| véletlen (100) | 96 | 0 | 3 (mind *-ök/-ok*, a DT315 hatókörén kívül) |
| kor3 (20) | 69 | 0 | 4 |
| kor3-*vala* (10) | 25 | 0 | 0 |
| `ek_E1_T3` (10) | 26 | 0 | 1 |

- **Lefedettség a véletlen rétegen:** igealak 96/96 = **100%**; az *-ök/-ok*-kal együtt 96/99 = 97,0%.
- **Torzítás:** a 11.4 és a 12.4 szerint a szám erre a mintára hangolt körök után áll elő, ezért felülbecsül. Torzítatlan mérés csak friss véletlen mintán lehetséges.

**Megállás:** a folytatás a felhasználó döntése, **DT321** (🟡).

## 15. Javítókör (`/elteres`, 1. kör): a független ellenőr 4. körének 5 tétele

**Bemenet:** `naplok/ELLENOR_F96.md` 4. kör (ELTÉRÉS: 5 tétel); a besorolás (mind az 5 tétel `mechanikus`) a felhasználó jóváhagyása. A végrehajtó session modellje `claude-opus-5-5`. Minden kódváltozás előtt `--kimenet`-próba a repón kívülre, tokenenkénti összevetés a kiadott `igealak_tokenek.tsv`-vel, és minden megváltozott token átnézése a versével (`konkordancia/Karoli_1908.tsv`). A számok a végrehajtó session mérései (`manual`), független ellenőrzésük az újraellenőrzés dolga.

### 15.1 Az `ek_E1_T3` és a visszaható E/1 névmás (4. kör, 1.)

**A hiba:** Salamon E/1 beszédében (Préd 2:5–9) a *magamnak* mellett az *-ék* T/3-ra fordult: *építék → építették*, *ülteték → ültették* (2:5, 2:6), *Gyűjték → Gyűjtötték*. Két külön ok:
- az `E1_JEL` nem ismerte a visszaható E/1 névmás ragos alakjait (*építék*, *Gyűjték*: a szabály-jelölt E1/T3, a `valaszt` dönt);
- az *ülteték* elemezetlen alak, szabály-jelölt nélkül; a sonnet és az opus egyező *ültették* alakja a `tobbseg` ágon közvetlenül cserélt, az E/1 heurisztika nélkül.

**A javítás (`igealak.py`):**
1. Az `E1_JEL` bővül: *magamnak, magamban, magamba, magamra, magamhoz, magammal, magamtól, magamért, magamról, magamnál, magamon, magamból* (a *magam, magamat* már benne volt). Hatás: 2 token (Préd 2:5 *építettem*, 2:9 *Gyűjtöttem*).
2. Új lépés (`ek_e1_fordit`) a `tobbseg` ágon, ha a többségi érték nem szövegkörnyezetfüggő: az *-ék* token *-ták/-ték* végű, változtató többségi alakja E/1-re fordul (*-tam/-tem*), `ek_E1_T3` jelöléssel, ha a mondatszakaszban (`.;:!?` között) visszaható E/1 névmás (`MAGAM_E1`) áll. Hatás: 2 token (Préd 2:5, 2:6 *ültettem*).

**A szűkítés (próba):** az első változat a 2. lépésben a tágabb E/1 jelzőt (`e1_e`, `e1_ige`) használta. A próbán 9 token változott, ebből 5 hibásan: T/3 helyett E/1 lett az 1Móz 47:9 *érték* (változatlan alakon), az Ez 20:13 *megveték* (az *ellenem* miatt), az Ez 23:38 *megfertézteték* (*az én szent helyemet*), a Józs 24:12 *űzék* (a darázsok űzték) és a Zak 5:9 *felemelék* (a két asszony). A kiadott változat ezért csak a *magam-* névmásra és csak változtató alakra fordít.

**Eredmény:** 4 token változott (Préd 2:5 ×2, 2:6, 2:9), mind átnézve a versével, mind helyes; más token nem változott. Az `ek_E1_T3` jelölés 692 → 694 tokenen áll. A minták modern szövege nem változott (a két mintában nincs Préd 2). A .3 újragenerálva: K2, K3, K3b teljesül, a Strong nem változott.

**Az N-F96f állapota:** részben megoldva. Ismert, nyitott maradék a 10.4 szerint 3 token, ahol E/1 helyén T/3 maradt (1Móz 39:15 *kezdék*, Dán 7:16 *kérék*, Ez 22:30 *keresék*); az `ek_E1_T3` heurisztika a teljes osztályon nem igazolt.

### 15.2 A `nevelo_utan` kizárás (4. kör, 2.) és a friss lefedettség-mérés

**A kizárás leírása (a 10.3 óta működött, ott nem írtam le).** A `nevelo_utan` (`igealak.py`) a névelő után, egy szóközzel álló igealak-jelöltet főnévnek veszi (*a tevék*, *egy tevének*, *a küldöttek*, *a megmaradottak*). Ilyenkor nem cserél:
- a .2 szabálya (`alk == 'szabaly'`, az *-ok* birtokos kivételével; `bizonytalan=nevelo_utan`);
- a DT311 többségi szavazása (`jelolt` ág);
- a 3. és a 4. kör alkalmazása (`kor3_alkalmaz`: a `nevelo_utan` jelölésű tokent mindkét körben kihagyja).

A DT316/r ezt a feltételt nem nevezte meg; a 10.3 és a 11.3 csere-számai ezzel a kizárással értendők.

**A hiba:** a Károli névmási *az*-a (*az monda*, *az felele*, *az méne*: ő mondta) is névelőnek számított, ezért 31 valódi igealak régies maradt (ellenőr: 47 `nevelo_utan` token, ebből 31 igealak). Ide tartozik az S0072 *felele* (1Móz 22:1, 1Kir 13:16): a 4. körben a szabály és az opus egyezett (*felelt*), mégsem lett csere.

**A javítás:** a névelő *a* csak mássalhangzóval, az *az* csak magánhangzóval kezdődő szó előtt áll. A mássalhangzós szó előtti *az* névmás, a magánhangzós szó előtti *a* nem névelő: ott a kizárás nem érvényes. Az *egy* mindkét esetben névelő marad. A függvény egy helyen dönt, a hívásai (a .2 szabálya, a `jelolt` ág, a kor3/kor4 `kor3_alkalmaz`) ugyanezt használják.

**Eredmény (próba, majd élesítés):** 39 token sora változott, ebből 27 token modern alakja. Mind a 27 átnézve a versével, mind helyes:
- *az monda → mondta* ×14 (1Móz 16:8, 27:18, 38:17; 1Kir 2:13; 2Kir 4:23, 8:14; Ruth 2:2, 3:9, 3:16, 4:4; Luk 7:40; Ján 13:6; ApCsel 26:15), *az mondá → mondta* ×2 (Ján 1:33, 5:11);
- *az felele → felelt* ×2 (1Móz 22:1, 1Kir 13:16);
- *az fogada → fogadott* ×2 (1Móz 16:4, 38:3; a korpusz többi *fogada*-ja is így cserél), *az szűle → szült* (1Móz 4:25), *az szűlé → szülte* (1Móz 25:2);
- *az beméne → bement* (Ez 10:6), *az méne → ment* (Luk 22:47), *az jöve → jött* (Jób 3:25);
- *az felkelvén → felkelve* ×2 (Mt 9:7, 9:9), *az letöretteték → letöretett* (Dán 8:22).

A többi 12 sor csak címkét kapott (a szabálycímke és a bizonytalan jelölés), a modern alak azonos:
- *felnövekedék, felemelkedék, feltekinte, fölkele, megfordulván, megosztá, bevádoltaték* (7 token): eddig az 5. kör cseréje volt (`kor5:token_opus+meglevo`), most a DT311 többségi ága cseréli ugyanarra az alakra: a címke `…+tobbseg:szabaly+sonnet+opus` (1Móz 7:17, 1Móz 21:20, 4Móz 21:9, Mk 9:27, Luk 15:12, Ján 20:16), a Luk 16:1 *bevádoltaték* sorában `…+tobbseg:sonnet+opus`, szabály nélkül (a szabály-jelölt itt *bevádoltaott*, a `jelolt` oszlop szerint). A szabály-jelölt tehát legfeljebb a szavazat egyik tagja, a cserét a többség adja. *(Pontosítva a 2. javítókörben, `ELLENOR_F96_2` 2.: a korábbi szöveg a .2 szabályának tulajdonította a cserét.)* Ezért a `token_opus` jelölés 205 → 198 tokenen áll (a 14.3 205-je a javítókör előtti szám);
- *tőled, vigye, vette, lenne, leszek* (5 token): változatlan, csak a szabálycímkét kapták meg. A minták modern szövege nem változott. A .3: K2, K3, K3b teljesül, a Strong nem változott; a változó token 50 491 → 50 516, a változó vers 21 620 → 21 621.

**Ami a kizárásban marad (21 token):** 14 névszó vagy melléknévi igenév, helyesen (*tevék* ×4, *küldöttek* ×3, *megmaradott(ak)* ×5, *megfáradott* ×2), és 7 kihagyás: a magánhangzós ige a névmási *az* után, amelyet a hangtani próba nem választ el a névelős főnévtől: *az elfuta* (1Móz 16:6), *az elbeszélé* (2Kir 8:6), *az esék* (Jób 3:25), *az elküldé* (Luk 15:15), *az eljő* ×2 (Préd 9:14, Ján 4:25; határeset); valamint az *egy monda* (Jel 6:1: „egy monda”, számnévi névmás), mert az *egy* marad. Ezek kihagyások, nem hibák.

**A friss lefedettség-mérés (a független ellenőr helyettesítő mintája).** A független ellenőr a 4. körben (`ELLENOR_F96.md` 4. kör, 2. rész) a kért véletlen minta helyett determinisztikus, egyenletes, szisztematikus mintát vett: a `karoli_modern_versek.tsv` 160 + 311·k sora (k = 0…99), 100 vers, a két meglévő mintával egy közös vers cserélve.

| | Csere | Hiba | Kihagyás |
|---|---|---|---|
| igealak | 92 | 0 | 5 |
| *-ök/-ok* birtokos | 9 | 0 | 2 magas hangrendű + 2 mély (*-ok*) |

- **Lefedettség igealakra: 92 / (92 + 5) = 94,8%.** A korpuszbecslés kb. 1 560 token (Poisson 95%-os sáv kb. 500–3 600).
- **Az 5 kihagyás:** *egybegyűle* (Bír 6:35; a tő-őr az ű/ü eltérésen bukik), *sétála* (Dán 4:26; egyik szkenben sincs), *az méne* (Luk 22:47; `nevelo_utan`), *Helybenhagyák* (ApCsel 24:9; egyik szkenben sincs), *lőnek* (Jel 11:19; `lonek_lo` téves találat, 15.3).
- **A 14.4 „100%”-a** (96/96) a minta2 véletlen rétegére vonatkozik, amelynek kihagyásai jelölték ki a 4.–5. kör osztályait: torzított, a valódi lefedettséget felülbecsli. Ennél a mérésnél 5 várt kihagyás mellett 0 kihagyás valószínűsége kb. 0,7% (ellenőr).
- **A javítókör után** az *az méne* (15.2) és a *lőnek* (15.3) javult; az *egybegyűle, sétála, Helybenhagyák* maradt. Új mérést nem végeztem: a minta kihagyásaira hangolt javítás után a számot ugyanez a torzítás érné.
- A mintán kívüli szúrópróba (ellenőr) további kihagyásai: 1Móz 7:17 *felveheték*, 1Móz 16:4 *béméne*, 2Sám 7:10 *elplántálám*, 2Krón 35:23 *lövének*.

A DT321 (🟡) leírása ezzel a számmal frissült; a döntés a felhasználóé.

### 15.3 A `lonek_lo` kivétel szóhatárhoz kötve (4. kör, 3.)

**A hiba:** a *lőnek* „nyíllal lőnek” kivétele (`lonek_lo`: a *lő* ige, nem *lőn → lettek*) részszót keresett a versben (`nyil|nyíl|íj`), ezért a Jel 11:19 *megnyilatkozék* szavára is illeszkedett, és a „lőnek villámlások” régies maradt.

**A javítás (`igealak.py`, `NYIL_IJ`):** a vers egy szava egész szóként a nyíl/íj szócsaládba tartozik: *nyíl/nyil* + (*a, ai, aid, aidat, aim, aimat, ait, aival, ak, akat, akba, akkal, aknak, at, át, lal, lá, tól, okat, azók, asok, lövésnyi*), illetve *íj/íjj/ijj* + (*at, ját, aim, im, dal, ász, ászok, ászai, ászokhoz, ászszá*). A szólistát a Károli 1908 *nyil-/nyíl-/íj-/ijj-* kezdetű szavaiból állítottam össze. Kimarad a *nyílik, nyilt, nyílott, nyilván-, nyílás-* és a *megnyilatkoz-*.

**Eredmény:** 1 token változott, a Jel 11:19 *lőnek → lettek*; átnézve a versével, helyes. Az 1Krón 12:2 „nyíllal lőnek vala” `lonek_lo` maradt (*lőttek*). A minták modern szövege nem változott. A .3: K2, K3, K3b teljesül, a Strong nem változott; a változó token 50 517.

### 15.4 Proveniencia: a `ts=` mező és a szken-fejlécek (4. kör, 4.)

**A hiba:** a három szken-tábla (`regies_szken.tsv`, `regies_szken_kor4.tsv`, `regies_szken_kor5.tsv`) és az `igealak.py` táblái (`igealak_tokenek.tsv`, `igealak_alakok.tsv`, `igealak_minta.tsv`, `igealak_minta2.tsv`) fejlécéből hiányzott a `ts=` (CLAUDE.md 1. szabály: `scope | forras | ts`). A `regies_szken_kor4.tsv` fejléce a 3. kör címkéjét viselte („N-F96d/e, DT316”), `--kor 4` nélkül.

**A javítás:**
- `regies_szken.py`: minden szken-fejléc `ts=`-t kap. A címke a kör szerint: 3. kör „(F96.3, 3. kör: N-F96d/e, DT316)”, 4. kör „--kor 4 (F96.3, 4. kör: DT317, 2. opció; a 3. kör utáni kihagyás-osztályok)”, 5. kör „--kor 5 (F96.3, 5. kör: DT320, 1. opció)”. A 4. kör `forras` mezője a tényleges bemenetet sorolja: `karoli_modern.tsv`, `igealak_alakok.tsv`, valamint a kérdezett alakokat kizáró LLM-táblák, a kor3-tábla is (a `volt` halmaz). A scope-ban szerepel a `jelolt` kérdések száma is (161).
- Az LLM-táblák (`--llm-valasz`) fejlécében a kör neve egységes („3. kör: DT316”, „--kor 4, 4. kör: DT317”, „5. kör: DT320”). Új kapcsoló: `--futas-ts`. Ezzel a meglévő válaszfájlokból újraírt táblán a `futas_ts` az LLM-futás eredeti ideje marad (kor3 `2026-10-25T08:31Z`, kor4 `10:09Z`, kor5 `10:42Z`, a korábbi fejlécekből); a `ts` az újraírás ideje.
- `igealak.py`: a közös fejléc `ts=`-t kap (`igealak_tokenek`, `igealak_alakok`, a két minta).

**Az újragenerálás menete:** a szken-táblák pillanatképek (a kérdésazonosítók és a válaszok rájuk épülnek), ezért mindegyik a saját pillanatkép-bemenetéből készült újra. A segédszkript a repón kívül volt. Lépései: a mostani bemenet mentése, a pillanatkép visszaállítása (`git show <commit>:<út>`), a szken futtatása, majd a mostani bemenet visszaállítása (utána `git status`: a bemenetek változatlanok).

| Tábla | Pillanatkép | A futás idejére eltéve |
|---|---|---|
| `regies_szken.tsv` | `karoli_modern.tsv` @ `8b858b3` | `igealak_llm_kor3.tsv`, `igealak_llm_kor4.tsv` (akkor még nem léteztek) |
| `regies_szken_kor4.tsv` | `karoli_modern.tsv`, `igealak_alakok.tsv` @ `9fd137f` | `igealak_llm_kor4.tsv` (a `volt` halmazt bővítené) |
| `regies_szken_kor5.tsv` | `igealak_tokenek.tsv`, `karoli_modern_versek.tsv`, `karoli_modern.tsv` @ `0dda8b3` | — |

**Az ellenőrzés:**
1. Előbb a régi kóddal, `--kimenet`-tel futott próba: mindhárom tábla a fejléccel együtt bájtra azonos lett a kiadottal, vagyis a pillanatkép reprodukálható.
2. Az új fejléces futás után mindhárom tábla a fejlécen kívül bájtra azonos a korábbival.
3. Az LLM-táblák a meglévő válaszfájlokból (scratchpad: `llm_kor3/`, `llm_kor4/`, `llm_kor5/`; `--modell claude-opus-5-5`, a hívásnaplók szerint) újraírva: a fejlécen kívül minden sor azonos, a három hívásnapló bájtra azonos. A sorrend: kor3-szken → kor3-LLM → kor4-szken (a végleges kor3-tábla sha-jával) → kor4-LLM → kor5-szken → kor5-LLM.
4. Az `igealak.py` (`--minta-frissit`) és a `karoli_modern.py` újragenerálva: a 4 + 2 tábla a fejlécen kívül azonos. A K2, K3 és K3b teljesül, a Strong nem változott.

Nem változott: a `karoli_modern.py` saját fejléce. Ebben a `ts=` már a javítókör előtt is megvolt (`eszkozok/karoli_modern/karoli_modern.py:166`; a `karoli_modern.tsv:1` és a `karoli_modern_versek.tsv:1` fejlécében a javítókör előtt `ts=2026-10-25T10:45Z`, az újragenerálás után `ts=2026-10-25T12:10Z`), ezért a tételhez nem kellett hozzányúlni. *(Javítva a 2. javítókörben, `ELLENOR_F96_2` 1.: a korábbi szöveg tévesen hiányzónak írta.)*

### 15.5 E17: az `igealak_tokenek.tsv` sorszám-változásának bontása (4. kör, 5.)

**Mérés:** a `8b858b3` és a javítókör 4. tétele utáni HEAD (`ccc555b4`) táblájának kulcsonkénti (igehely, sorszám) összevetése, `split('\t')`-tel. A számítás szkriptje a repón kívül van. A szabálycímke a `szabaly`, a `bizonytalan` és a `jelolt` oszlop változásából adódik. A sorok a 10.–15. szakasz összes körét együtt mutatják.

| | Sor |
|---|---|
| `8b858b3` (fájlsor 66 603, ebből 2 fejléc) | 66 601 |
| HEAD (fájlsor 67 687) | 67 685 |
| **Δ** | **+1 084** |
| új sor | 1 084 |
| eltűnt sor | 0 |
| **Δ = új − eltűnt** | **+1 084** |
| módosult sor (a Δ-t nem érinti) | 679 |
| változatlan sor | 65 922 |

A `git diff --numstat` −680 sora (a 4. körben −646) ennek megfelelően nem törlés: 679 módosult sor és a fejléc.

**Az új sorok (1 084) szabálycímke szerint:**

| Címke | Sor |
|---|---|
| `kor3:szabaly+opus` (DT316, 10.3) | 690 |
| `kor4:szabaly+opus` (DT317, 11.3) | 162 |
| `kor5:token_opus+meglevo` (DT320, 14.3) | 131 |
| csak jelölt: `kor5_token_opus` a `jelolt` oszlopban (DT320) | 41 |
| `kor3:opus_tanusitott` (DT318, 12.3) | 29 |
| `jelen_mult_vala`, `kor3_csak_opus` (a kieső *vala* előtti ige múlt időbe, 10.3) | 12 |
| `jelen_mult_vala`, `kor4_csak_opus` (ugyanez a 4. körben, 11.3) | 11 |
| `kor4:opus_tanusitott` (DT318, 12.3) | 7 |
| `kivetel`, `kor4_csak_opus` | 1 |
| **összesen** | **1 084** |

Ebből 1 043 sor modern alakja eltér a .1-étől; 41 csak jelölt.

**A módosult sorok (679) a változás oka szerint:**

| Ok | Sor |
|---|---|
| **csak címke vagy jelölt (a modern alak azonos)** | **398** |
| a 4. kör opus-szavazata a DT311 címkéjében és a `jelolt` oszlopban (11.3, `jelolt` típus) | 331 |
| az 5. kör jelöltje (`kor5_token_opus`) a `jelolt` oszlopban | 64 |
| a 4. kör jelöltje (`kor4_opus`) a `jelolt` oszlopban | 3 |
| **a modern alak változott** | **281** |
| *vala* kiesik, `vala_segedige_kor3` (10.3) | 71 |
| az 5. kör cseréje, `kor5:token_opus+meglevo` (14.3) | 67 |
| a DT311 többsége a 4. kör opus-szavazatával (`…+opus`, `tobbseg:sonnet+opus`; 11.3; ide tartozik a Dán 8:22 *letöretteték* is, 15.2) | 30 |
| a `nevelo_utan` feloldása (15.2; a 27 tokenből 26, a 27. az előző sorban) | 26 |
| `kor4:szabaly+opus` (11.3) | 22 |
| `tobbseg:opus_tanusitott` (DT318, 12.3) | 22 |
| az `ek_E1_T3` E/1-re fordul: a 10.4 mondatszakasz-szabálya (16) és a 15.1 *ülteték* ×2 | 18 |
| *vala* kiesik vagy létige a 4. körben: `vala_segedige_kor4` 16, `vala_letige_kor4` 2 | 18 |
| `tobbseg:alanyi_targyas` (DT318, 12.3) | 3 |
| `vala_segedige_mult` (a régmúlt *vala*-ja) | 2 |
| `jelen_mult_vala`, `kor3_csak_opus` | 1 |
| *lőnek → lettek* (15.3) | 1 |
| **összesen** | **679** |

A 4. körben jelzett állapot (`8b858b3..b8334a64`): ugyanaz a +1 084 (1 084 új, 0 eltűnt), 645 módosult sor. A javítókör sort nem adott és nem vett el. Az 1.–3. tétel 44 sort módosított (4 + 39 + 1), a 4. tétel csak a fejlécet. A 44 sorból:
- 34 a 4. körig a `8b858b3` óta változatlan volt; ezek adják a módosult sorok 645 → 679 növekedését;
- 10 már korábban is módosult sor volt: a 7 volt `token_opus` sor (15.2), a Préd 2:5 *építék*, a Préd 2:9 *Gyűjték* (15.1) és a Dán 8:22 *letöretteték* (15.2).

### 15.6 Összegzés és megállás

| Tétel | Változás | Token (modern alak) |
|---|---|---|
| 1. `ek_E1_T3` + visszaható E/1 névmás | `E1_JEL` bővítés, `ek_e1_fordit` (`MAGAM_E1`) | 4 (Préd 2:5 ×2, 2:6, 2:9) |
| 2. `nevelo_utan` | hangtani névelő-próba, az *egy* marad; leírás a kódban és a 15.2-ben; friss mérés: 94,8% | 27 (+12 sor csak címke) |
| 3. `lonek_lo` | egész szavas nyíl/íj szólista (`NYIL_IJ`) | 1 (Jel 11:19) |
| 4. proveniencia | `ts=` a szken- és az igealak-fejlécekben, kör-címke, `--futas-ts`; a szken-táblák a pillanatképből | 0 (csak fejléc) |
| 5. E17 | a +1 084 bontása (15.5) | — |

A javítókör után:
- az `igealak_tokenek.tsv` 67 685 adatsor (változatlan);
- a változó token 50 491 → 50 517, a változó vers 21 620 → 21 621;
- K2, K3 és K3b minden lépés után teljesült; a 418 633 Strongos token kulcsa mind a táblában, a Strong nem változott;
- a két minta (`igealak_minta.tsv`, `igealak_minta2.tsv`) modern szövege egyetlen soron sem változott, csak a fejlécük.

**Nyitva marad (nem a javítókör tárgya):**
- 3 ismert E/1 → T/3 hiba (1Móz 39:15, Dán 7:16, Ez 22:30; 15.1);
- a magánhangzós ige a névmási *az* után (7 kihagyás, 15.2);
- az ellenőr mintájának *egybegyűle, sétála, Helybenhagyák* kihagyása és a mintán kívüli szúrópróba alakjai (15.2).

**Megállás:** az 1. javítókör a független újraellenőrzésen állt meg (`naplok/ELLENOR_F96_2.md`: ELTÉRÉS: 2 tétel, dokumentációs). A 2. javítókör ezt a két tételt javította (15.2, 15.4, 15.6), majd szintén az újraellenőrzésen állt meg (`naplok/ELLENOR_F96_3.md`: ELTÉRÉS: 1 tétel, ez a megállás-mutató). A javítókör-korlát (2/2) ezzel betelt; ezt a tételt a zárócommit javítja (16.). *(Javítva a zárásban, `ELLENOR_F96_3` 1.: a korábbi szöveg az `ELLENOR_F96_2.md`-re várónak írta a munkát.)*

## 16. Zárás (DT321, 1. opció)

**A felhasználó döntése** (chat, 2026-10-25): „1, zárd le a hivatkozás javításával”.

- **A független ellenőr** a 3. kör óta végzett változásokon (`8b858b3..d5f6607`, `naplok/ELLENOR_F96.md` 4. kör) friss, egyenletes mintán mért. A mintát szisztematikusan vette, mert a kért magú véletlen mintát nem futtathatta. A lefedettség igealakra 94,8% (92 csere, 0 hiba, 5 kihagyás).
- **A két javítókör** (`naplok/ELLENOR_F96_2.md`, `naplok/ELLENOR_F96_3.md`) mind az öt 4. körös tételt javította. Ebből a minta két kihagyását pótolta: *az méne*, *lőnek*. A korlát betelt, a maradék egyetlen dokumentációs tétel (a 15.6 megállás-mutatója) a zárásban javítva.
- **A kiadott réteg:** `adat/karoli_modern/karoli_modern.tsv` (599 367 token, 50 517 változó) és `karoli_modern_versek.tsv` (31 158 vers, 21 621 változó). A K2, K3 és K3b teljesül, a Strong nem változott (DT314).
- **A maradék** (N-F96h, nyitott tétel a briefben; utófeladat a `/befogad`-dal, a felhasználó jóváhagyásával):
  - a jelöltként maradt tokenek (`igealak_tokenek.tsv` `jelolt` oszlop);
  - a magánhangzós ige a névmási *az* után (7 token);
  - 3 E/1 → T/3 hiba (1Móz 39:15, Dán 7:16, Ez 22:30);
  - az ellenőr mintájának és szúrópróbájának kihagyásai (*egybegyűle, sétála, Helybenhagyák, felveheték, béméne, elplántálám, lövének, megszerzém*);
  - a mély hangrendű *-ok* birtokos (DT315, 3. opció);
  - az N-F96c.
