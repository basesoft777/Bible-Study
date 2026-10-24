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
- A Hunspell hu_HU (DT301): 4.1.

## 4. F96.1 — helyesírási lépcső

`scope=a Károli 1908 minden verse (31 158) és tokenje (599 367) | forras=konkordancia/Karoli_1908.tsv (sha256:49335bbcc77d) + adat/szoto/karoli_szotari_alak.tsv (sha256:edba33e6d65a) + eszkozok/karoli_modern/helyesiras.py | ts=2026-10-24T13:36Z` — `python eszkozok/karoli_modern/helyesiras.py --minta`; determinisztikus, LLM és API nélkül (**0 token**). Kimenet (generált, `# GENERÁLT:` fejléccel): `adat/karoli_modern/helyesiras_alakok.tsv` (a szövegkörnyezet nélkül változó alakok), `adat/karoli_modern/helyesiras_tokenek.tsv` (a változó, kieső vagy bizonytalan tokenek, vers-kulccsal és `tokenizal`-sorszámmal, DT-F96f), `adat/karoli_modern/helyesiras_minta.tsv` (4.4). Ez a .1 köztes kimenete, nem a .3 kiadott rétege.

### 4.1 Hunspell hu_HU (DT301) — nem futott

A futtató környezetben a Hunspell nem érhető el: nincs telepítve (sem `hunspell`, sem `/usr/share/hunspell`), a csomagforrás és a szótár forrása (GitHub, PyPI) a hálózati szabály miatt nem tölthető le (`connect_rejected`, 2026-10-24). A licencet így nem lehetett szó szerint idézni a forrásból, és a Hunspell nem futott. A brief .1/2 szerint, ahol sem a korpusz, sem a #94 tábla nem támasztja alá a modern alakot, a `tamasz` = `modell_ellenorizetlen`; a mérőszám a felhasználói minta. A Hunspell-mérés pótolható, ha a szótárfájl (és a licenc szövege) a repón kívül rendelkezésre áll: a felhasználó vagy egy hálózattal futó session dolga.

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

Összesen: **12 804 vers változik** (a 31 158-ból), **28 953 token** (ebből 11 212 kieső „a”), **1 377 alak** szövegkörnyezet nélkül. Az alakok `tamasz` oszlopa: `szoto_94` 177, `korpusz` 106 (a modern alak a Károliban is áll), `manual` 1, **`modell_ellenorizetlen` 1 093** (zömmel a `karakter` cseréi: a *cz*-s alakok modern párja a Károliban nem fordul elő; Hunspell nélkül ez a mintán mérhető).

**Nem változik a .1-ben (szándékosan):** a lemmaváltás (DT-F96e a: *e, oh, férfiú, leány, mostan, minekutánna*, az önálló *kik/mely*); minden igealak (*teremté, monda, -ván/-vén, vala, lőn, vagyon*: .2); a *-jék* és a *-jok/-jök* (4.5).

**Az „a mi” kezelése (heurisztika, manual).** Toldalékos *mi-* (*mit, minek, mire*) mindig összevonva. A puszta „a mi”: ha a következő szó *-nk* birtokos (*a mi Istenünk, a mi atyánk*) → birtokos, marad (`mi_birtokos_marad`); ha a következő szó nagybetűs, személyes névmás (*nékünk, minket*), vagy írásjel követi → `bizonytalan`, változatlan (**298 token**; ezek a mintában is szerepelnek); különben → *ami*. Egy „a Ki…” nagybetűs vers közbeni eset `nagybetu`, változatlan.

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
