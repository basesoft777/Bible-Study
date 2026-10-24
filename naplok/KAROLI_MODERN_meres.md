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

## 3. Nyitott a .1 előtt

- ⛔ DT-F96d: a token-keret (az 1.–3. változat, a modell, a tokenszintű esetek kezelése).
- DT-F96e: a `lemmavaltas` osztály és a *reá → rá* — helyesírás vagy szókincs (a DT128 szintjén belül vagy kívül).
- N-F96b: a #94 `regies_jegy` értékkészletének tárgyas T/3-hiánya és a megfigyelt táblahibák (*vévén*, *kivűl*): a modernizálás saját szabállyal kezeli, a #94 lezárt.
- A Hunspell hu_HU (DT301, fejlesztési mérce) a .1/2-ben jön; a licenc-idézet ide kerül a használat előtt.
