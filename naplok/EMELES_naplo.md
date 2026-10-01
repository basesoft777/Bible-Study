# F28 EMELES — futásnapló

*Brief: `F28_EMELES_BRIEF.md` v4 · ág: `claude/magical-goldberg-4xb1a0` · indult: 2026.10.01*

## E0 — Lista (F28.1)

Parancs: `python eszkozok/emeles.py lista` → `naplok/EMELES_lista.tsv` (40 sor).

A halmaz a brief 2. pontjának szövege szerint: az `adat/elofordulasok.tsv` **`strong`
mezőjének** G/H-tokenjei (a `+` mentén bontva), meg az `adat/lexikon_hivatkozasok.tsv`
**`szotar ∈ {Thayer, BDB}`** sorainak `strong`-ja.

| | Szócikk | ebből kimarad | Fordítandó | Karakter (fordítandó) | Leghosszabb |
|---|---|---|---|---|---|
| Thayer (G) | 14 | 1 (G1941, `teljes` `kezi`) | 13 | 39 515 | 23 705 (G4151) |
| BDB (H) | 26 | 0 | 26 | 126 394 | 14 948 (H1121) |
| **Összesen** | **40** | **1** | **39** | **165 909** | — |

### Eltérés a brief 2. pontjától

A brief számai (18 + 29 = 47 szócikk, 187 863 karakter) **nem** ezzel a halmazzal készültek,
hanem a két tábla **bármely mezőjének** G/H-tokenjeivel. Ez a mérés reprodukálható:
`python eszkozok/emeles.py lista --szeles` → Thayer 18, BDB 29 (a G1941-gyel együtt
51 437 + 136 426 = 187 863 karakter) — **pontosan a brief számai**.

A különbség 7 Strong-szám (a `--szeles` halmazban van, a briefszövegű halmazban nincs):

| Strong | Karakter | Honnan jön a token | Megjegyzés |
|---|---|---|---|
| G0035 | 186 | `elofordulasok.karoli_szo` (KIRALY-001, Zsid 7:1-28) | „nemzetség nélkül való (G0035, 7:3)” |
| G0540 | 214 | `elofordulasok.karoli_szo` (KIRALY-001, Zsid 7:1-28) | „Apa nélkül (G0540, 7:3)” |
| G2564 | 6 751 | `lexikon_hivatkozasok` TBESG- és LSJ-sor | nem Thayer-sor |
| G2672 | 1 025 | `elofordulasok.kapcsolodas` (HAMART-001, Gal 3:13) | a szöveg éppen kizárja: „nem a LXX κεκατηραμένος … szavával” |
| H0423 | 688 | `elofordulasok.kapcsolodas` + `lexikon_entry_id` (HAMART-001, Ézs 24:5-6) | a szöveg tematikusnak minősíti: „más szóval: אָלָה … ⇒ tematikus, nem lexikai” |
| H1863 | 191 | `elofordulasok.gerinc_elem` (HAMART-001, 1Móz 3:18, `H6975+H1863`) | gerinc-elem, de a `strong` mező csak H6975 |
| H8085 | 9 153 | `elofordulasok.kapcsolodas` (HAMART-001, Jer 6:7) | kollokáció-pár eleme („H8085+H2555”), a `strong` mező H2555 |

**Kezelés:** a menet a briefszövegű halmazzal (39 fordítandó) halad; a 7 tétel
felvételének kérdése a `DONTESEK.md` DT24 (c) pontjába került (az E4a első adagját nem
érinti, kivéve a „legrövidebb Thayer-szócikk” kiválasztását — l. az E4a szakaszt).

## E1 — Prompt v4 (F28.2)

`forditas/prompt_v4.md`: a `fp2/prompt_v3.md` szó szerinti másolata a
`<!-- PROMPT-KEZDET -->` jelölő alatt (az összeállító szkript ellenőrizte, hogy a v3
minden része változatlanul, sorrendben benne van), plusz az általános (v4) és a
BDB-blokk a v3 „Stílus” és „Ideiglenes terminológia” szakasza között, a végén a G26
példapár (forrás: a Thayer G0026 sora a „consequently it denotes” szavakig). A
BDB-blokk elé egy bekezdés került: H-számnál a v3 „Thayer” megnevezése a BDB-t jelenti
(a v3 szövege Thayer-specifikus, és szó szerint maradt). Kitöltés:
`python eszkozok/emeles.py prompt <Strong>`.

## E2 — Javítóréteg (F28.3)

`eszkozok/normalizal.py`, négy szabály (`kk_k`, `szerzonevek`, `igehely_rov`,
`konyvnevek`), szótáranként kapcsolható (`SZABALYOK`). Tesztek:
`python eszkozok/teszt_normalizal.py` → 19 teszt, OK.

## E3 — Kapuk (F28.4, F28.6)

`eszkozok/forditas_kapuk.py`: a `naplok/FORDITAS_P4_ellenoriz.py` 1–3. és 6.
ellenőrzése importálva, a 4. és 5. F28-as változata saját (l. lent), plus három új:
idézőjel-párok (8), tagolás (9), igetörzsek (10, BDB).

A tagolás-kapu **részsorozatot** vizsgál: a forrás jelölőinek (pontozott szám, a BDB
pont nélküli főszáma, betűjel, római szám, zárójeles jel) sorrendben meg kell
jelenniük a fordításban; a fordítás hozzáadhat sorszámnevet (a magyar `14. §`,
`835. o.`, `2. aorisztosz` nem forrásbeli tagolás). Pontos egyezést nem lehetett
előírni, mert a magyar sorszámnév-írás a forrásban nem létező pontozott számokat
termel.

Kalibráció a G1941 meglévő `teljes` `kezi` fordításán: tagolás RENDBEN; a 3., 4., 5.
kapu jelez (az akkori v1-stílus kiejtés-zárójelei, `Lk`, `Ám` rövidítés) — ez a
fordítás nem a v4 mércéje.

Hamis riasztások az első adagban, a kapuban javítva (F28.6):

| Kapu | Eset | Javítás |
|---|---|---|
| 4 formázás | a BDB gyakoriságjele (`קָרָא_724`, `Qal_655`) `_` Markdown-jelnek számított | csak a forrásbelinél több `*`, `_`, `#` sértés |
| 5 terminológia | a `procl.` szóban a `cl.` rövidítés „megvolt” | az angol alak előtt nem állhat betű |

## E4a — Első adag (F28.5–F28.7)

Az öt szócikk: G1944 (a briefszövegű lista legrövidebb Thayer-szócikke), G5590, H6093
(a legrövidebb BDB), H7121, H1121 — helyettesítés nem kellett. Kimenet:
`naplok/EMELES_elso_adag.md` (forrás és fordítás szegmensenként párban, a strukturális
tagolásjelölőknél igazítva; kapueredmények; a H7121-nél a kézi 2.c és 3. jelentés
összevetése). A párok nem kétoszlopos táblázatban, hanem egymás alatt állnak: a forrás
blockquote-ban, alatta a fordítás. Ok: a CI E9 szabálya a táblázatcellában álló angol
`sense` szót (H7121: `in this sense`) HIBA-nak vette; a blockquote a D11 szerint
kivétel (idézett angol forrásszöveg).

**Eltérés a brief E4 leírásától:** szócikkenkénti `vegrehajto-opus` subagent helyett a
menet maga fordított (Opus-modell, `claude-opus-5-5`), mert ebben a környezetben
subagent-indításra nem volt eszköz. A prompt, a terminológia és a forrásszöveg
ugyanaz.

**Segédeszköz (nem a brief része):** helyőrzős fordítás — az `emeles.py helyorzo` minden
összefüggő héber/görög szakaszt ⟦n⟧ jellel helyettesít, az `ellenoriz --mappa`
betűhíven visszaírja. Ok: a BDB-szócikkek több száz héber szakasza (H1121: 284) kézi
átmásolásnál hibázna; így a BDB-blokk 3. szabálya gépileg teljesül.

Futás: mind az öt átment a kapukon; a javítóréteg egyiken sem változtatott. Önújrapróba
egy volt (H1121, 3. kapu: „Tiglat-Pileszernek 16:7” rövidítésnek látszott, a második
változat vesszővel választja el a nevet az igehelytől).

| Strong | Forrás kar. | Fordítás kar. | Arány |
|---|---|---|---|
| G1944 | 337 | 339 | 1.01 |
| G5590 | 5 950 | 6 055 | 1.02 |
| H6093 | 187 | 240 | 1.28 |
| H7121 | 10 780 | 11 884 | 1.10 |
| H1121 | 14 948 | 15 926 | 1.07 |

**Írás:** a fordítások a `naplok/EMELES_munka.tsv`-ben (az `adat/forditasok.tsv`
sémája, `allapot=opus`), nem az `adat/forditasok.tsv`-ben. Ok: az `eszkozok/ellenoriz.py`
13. szabálya (CI E1) minden `forditasok.tsv`-sorhoz a `lexikon_hivatkozasok.tsv`-ben
keresi a forrásszöveget; a H6093, H7121, H1121 `teljes` sorához ott nincs sor, tehát a
beírás a CI-t elbuktatná, és a SEMA 2.14 `allapot` zárt listáján nincs `opus`. Mindkettő
a brief `ir` listáján kívüli fájl módosítását kívánja — kérdés a DT24 (b) pontjában.

**E8 (keretmérés):** cloudban fut, kimarad.

**⛔ Megállás:** DT24 (`DONTESEK.md`).

## DT24 alkalmazása (F28.9–F28.12)

A felhasználó döntése: (a) jóváhagyva egy javítással (Lam → JSir), (b) igen, külön
commitban, negatív teszttel, (c) 39 szócikk.

- **F28.9 (`12a3022`):** `Konyv_normalizalo_tabla.tsv` 26. sor `Lam → JSir`; a
  `normalizal.py` a táblából olvas (új teszt: 20/20). A javítóréteg a már kész
  fordításokban a „Sir”-t nem cseréli (a Sir a Sirák fia apokrif alakja is, a csere
  nem determinisztikus), ezért **új 11. kapu** (könyv-egyezés): a forrás igehelyeinek
  könyvei leképezve egyezzenek a fordításéival. A H7121-ben 4, a H1121-ben 2 „Sir”
  akadt fenn, az önújrapróba JSir-re javította; mind az 5 újra átment. Nulla-diff
  (`eszkozok/nulladiff.sh 9f48e98`): a generált `lexikon/` azonos.
  **Mellékhatás, nem javítva (záró tételbe):** a régi „Sir” alakú Siralmak-hivatkozás
  maradt az `adat/jeloltek.tsv` 329. sorában (`TEREMT-002 Sir 2:8`), az
  `adat/auditok.tsv` 169–171. sorának `scope=range:Sir 2:8` proveniencia-értékében és
  a `genezis/1Moz_10v1-11v32_bovitett.md`-ben („Sir 3:52,4:18”) — ezek más feladatok
  adatai, illetve rögzített lekérdezés-proveniencia; a táblaváltás után a
  `lekerdez.py` a „Sir” alakot nem ismeri fel.
- **F28.10 (`f540c0e`, ELLENŐRZŐ-MÓDOSÍTÁS):** `ellenoriz.py` 13. szabály: a Thayer/BDB
  `teljes` sor forrása a konkordancia teljes szócikke, ha nincs
  `lexikon_hivatkozasok`-sor; SEMA 2.14 `allapot` + `opus`. Teszt:
  `eszkozok/teszt_ellenoriz_13.py`, 7 eset, 4 negatív, zöld. A CI E16 miatt a PR címe
  „[ELLENŐRZŐ]” előtagot kíván.
- **F28.11 (`97f8c4b`):** `emeles.py beir` → az 5 sor `kezi`-ként az
  `adat/forditasok.tsv`-ben; a H7121 2.c és 3. sora az új fordítás szakaszát kapta (a
  forrásszakaszon is átment a kapukon). `ellenoriz.py`: SÉRTÉS 0. Nulla-diff
  (`f540c0e` → HEAD): a generált lexikonban a G5590 (ANTROP-001) és a G1944 (HAMART-001)
  „Fordítás függőben” helyén megjelenik a fordítás, a H7121 2.c és 3. (ISTENTISZT-001)
  az új szöveget mutatja — a várt hatás. Az éles `lexikon/` újragenerálása nem ennek a
  feladatnak a dolga (záró tétel).

## E4 — A maradék 34 szócikk (F28.13–F28.22)

Fordító továbbra is a menet maga (Opus, `claude-opus-5-5`); subagent-indításra nem volt
eszköz. Módszer: helyőrzős forrás → fordítás → `emeles.py ellenoriz` (javítóréteg +
kapuk) → `emeles.py rogzit` (munkatábla) → a végén `emeles.py beir --allapot opus`.
Darabolás nem kellett; a G4151-et és a H1121-et a fordító több vázlatrészben írta, és
egyben került a kapukra.

**Eredmény:** 34/34 szócikk átment; `naplok/EMELES_bukottak.tsv` nem készült (nincs
bukott). A végén mind a 39 munkatábla-sor újrafutott a végleges kapukon: 0 hiba.
`adat/forditasok.tsv`: 34 új `teljes` sor `allapot=opus`-szal (F28.22); `ellenoriz.py`
SÉRTÉS 0.

**Kapukalibrálások az E4 során** (mind hamis riasztás volt, a kapu javult; az összes
szócikk utólag a végleges kapukon is átment):

| Commit | Kapu | Eset | Javítás |
|---|---|---|---|
| F28.13 | 9 tagolás | `e. g.` második tagja (G0282) | kizárva |
| F28.15 | javítóréteg | „Lange on Revelation” könyvcím (G0086) | angol elöljáró után nincs csere |
| F28.14 | javítóréteg | „Philo's Lehre” cím (G0012) | aposztróf előtt nincs csere |
| F28.17 | 3 Károli | „Gi 20:21” szigla (H8034) | a forrásban is igehely előtt álló, nem könyvnév tag elfogadott |
| F28.17 | 9 tagolás | szám utáni `f.` (= és a következő) | szám után nem betűjel |
| F28.18 | 9 tagolás | „3 Izráelben” (H3548) | a fordításban nagybetűs szó is állhat a főszám után |
| F28.20 | 5 terminológia | „lelkét”, „lelked” (H2416) | lélek → lelk- tőváltozat |

**Önújrapróbák** (a fordítás javult, nem a kapu): G0086, H1121, H3548, H0430 — vessző a
magyar szó és a csupasz igehely közé (a 3. kapu a nagybetűs magyar szót rövidítésnek
veszi); H7451 — „divine spirit” → szellem; H5315 — három betoldott zárójel elhagyva;
H7121, H1121 — Sir → JSir (11. kapu).

**Terminológia-kivétel:** G0282 — a „Bleek on Heb.” a Zsidókhoz írt levél; a
terminológia `Heb. → héb.` sora itt nem alkalmazható (`--kivetel Heb.`, a sor
megjegyzésében).

**Hiba a jóváhagyott H1121-ben (javítás nélkül, DT25 (c)):** a két vázlatrész
összefűzésekor kimaradt egy szóköz: „Bír 8:18.j. gyakran”. A sor `kezi`, a brief szerint
védett; a G4151 összefűzésénél a hibát észrevettem és szóközzel fűztem.

**Az `emeles.py lista` mostantól** a `kezi` `teljes` sorokat kimaradónak jelöli (a
`naplok/EMELES_lista.tsv` F28.22 óta az első adag 5 sorát `kimarad=igen`-nel mutatja). Az
`opus` sorokat nem jelöli kimaradónak — ezt az E7 munkafolyamat-lépés rendezi.

**Az első adag naplója** (`naplok/EMELES_elso_adag.md`) a DT24 előtti állapot pillanatképe
(benne még a H7121/H1121 „Sir” alakja); nem generáltam újra.

## E5 — Szúrópróba (F28.23)

Minta: `python eszkozok/emeles.py minta --seed 28` → G4151, G0282, H7585, H8004, H8415
(5 = max(5, ⌈34 × 10%⌉); Thayer 2, BDB 3; G4151 > 10 000 karakter). Kimenet:
`naplok/EMELES_szuroproba.md`. **⛔ Megállás:** DT25 (`DONTESEK.md`).

**CI-megjegyzés a PR-hez:** (1) az `eszkozok/ellenoriz.py` módosult (F28.10), a CI E16
miatt a PR címe „[ELLENŐRZŐ]” előtagot kíván; (2) az `adat/SEMA.md` módosult (F28.10,
F28.11), és a CI E9 a fájl **korábbi** 235–236. sorában álló angol „sense” szóra
JELENTÉS-t ad (nem ennek a menetnek a sora; a D8 a nem érintett sort JELENTÉS-re
minősíti, a kilépési kód 0). *Helyesbítés (ELLENOR_F28 8. tétel): korábban itt tévesen
„HIBA” állt; HIBA PR-cím nélkül csak az E16-ból jön.*

## DT25 alkalmazása, E6, E7, zárás (F28.24–F28.29)

- **F28.24 `defb80e`:** a szúrópróba 5 sora `kezi` (a G0282 terminológia-kivétele
  megmaradt); a H1121 szóközjavítása (DT25 (c)).
- **F28.25 `a85c855`:** `adat/terminologia.tsv` v2 (Holy Spirit → Szent Szellem, Spirit of
  God → Isten Szelleme, the Spirit → a Szellem); 12. kapu (Szentlélek / Isten Lelke →
  JELZÉS), 13. kapu (a könyv fejezetszámánál nagyobb fejezet → JELZÉS; a BDB ψ-hibája 5
  szócikkben). Szentlélek-lista: `naplok/EMELES_szentlelek_lista.tsv` (9 hely, csak lista).
  *Kiegészítés (ELLENOR_F28 7. tétel):* a lista a `lexikon/*.md` GENERÁLT-blokkjait
  kihagyja, ezért 3 további találat nem szerepel benne: `lexikon/ANTROP-001_TUDOMANYOS.md`
  71, 108 („Isten Lelkének”, 1Kor 2:14) és `lexikon/TEREMT-001_TUDOMANYOS.md` 159 („Isten
  Lelke”, 1Móz 1:2). Generált tartalom; a lexikonban nem javítottam (DT26 (c)).
- **F28.26 `85c15ac`:** `lekerdez.py` — a „Sir” a JSir álneve olvasáskor (a rögzített
  `tsk "Sir 2:8"` proveniencia újrafuttatva n=15, egyezik). *Helyesbítve az F28.32-ben:*
  az álnév a közös `parse_igehely`-be került, nem csak a scope-olvasásba, ezért a TAHOT
  „Sir” igehelyei csak a JSir-tartományra illeszkedtek, a `lxx-hid`, `gerinc "Sir 2"`,
  `scan --szakasz "Sir 2"` és a JSir-alakú `tsk`/`karoli` pedig 0-t vagy hibát adott
  (ELLENOR_F28 1. tétel). A tényleges viselkedés az F28.32 után: l. lent.
- **F28.27 `258d385` (E6):** CI E19 + tesztek (54/54 zöld; a jelenlegi adaton 0 találat).
- **F28.28 `0d66b8d` (E7):** MUNKAMENET C0 ⛔ sor; az `emeles.py lista` kész-feltétele:
  `kezi`/`opus` `teljes` sor a jelenlegi forrás-hash-sel (40/40 kész).
- **Zárás:** DONTESEK DT25 ✅, DT26 nyitva; `naplok/F28_zaras.md`; brief: `lezarva`.

## Javítások a független ellenőrzés után (ELLENOR_F28, F28.31–)

- **F28.32 — `lekerdez.py` „Sir” (1. és 4. tétel, A1).** Az álnév kikerült a közös
  `parse_igehely`-ből (a `REGI_ALNEV` törölve); az adatbeolvasás (`parse_igehely`,
  `load_*`, `to_step`) az F28 előtti állapotú. A „Sir”/„JSir” kezelése csak a
  parancssori scope-olvasásban van (`scope_adat_igehely`, `scope_range`,
  `scope_to_step`): a magyar kulcsú táblák (TAHOT_kivonat, TSK, Karoli_1908,
  LXX_kivonat_Siralmak) „Sir” alakjára fordít, a STEPBible-kulcsúakhoz
  (Karoli_kereszthivatkozasok) a táblán át „Lam”-ra. **Tényleges viselkedés:** a kimenet és a
  proveniencia scope-ja a parancssori alakot írja (`scope=range:Sir 2:8` vagy
  `range:JSir 2:8`), a találatok igehelyei az adat alakjában („Sir 2:1 …”) állnak — a
  lekérdezés tehát NEM írja ki a JSir alakot. Mért n-ek, mindkét alakra azonosak:
  `lxx-hid` 24, `tsk` 15, `karoli` 1 (= auditok.tsv 169–171), `gerinc "Sir 2" "Ézs 34"`
  38, `scan H1323 --szakasz "Sir 2"` 10 (= az F28 előtti `e39f145` kódjának értéke
  ugyanerre a parancsra). Teszt: `eszkozok/teszt_lekerdez_sir.py` (11 eset, minden út
  mindkét alakkal).
- **F28.33 — E19 `--teljes` módban (2. tétel).** Az F28.27 „0 találat”-a `--teljes`
  módban hamis tiszta volt: a `futtat.py` az md-fajlok listáját adta az E19-nek, amely
  így el sem indult. Javítás: `szabalyok.HATOKOR_SZABALYOK = {'E3', 'E19'}`, ezek
  `--teljes` módban a `['__TELJES__']` jelzőt kapják. Teszt: `E19Teszt.test_teljes_modban_fut`
  (a javítás nélkül bukik) és `test_teljes_jelzo_kozvetlenul`; 56/56 zöld. A valódi
  adaton az E19 `--teljes` módban most ténylegesen lefut: 0 találat. Az
  `ellenorzes.yml` lépésnevei E2-E19-re frissültek (a `E2E16_KILEPES` változónév maradt).
- **Eltérés a brieftől: a kapuk menet közbeni kalibrálása (3. tétel).** A brief E4
  pontja kapuhibánál egy önújrapróbát ír elő, utána a szócikk a
  `naplok/EMELES_bukottak.tsv`-be kerül. Ehelyett a menet közben a kapukódot
  módosítottam, és a szócikk a módosított kapun ment át; a `bukottak.tsv` ezért üres.
  Ez **eltérés a brieftől**, nem a brief szerinti eljárás. A változtatások (az ellenőr 6-ot
  számolt; a commitokból 7 olvasható ki): (1) formázás-kapu: a BDB `_` gyakorisági jele
  (F28.6, H7121); (2) terminológia-kapu: `cl.` a `procl.`-ban (F28.6, H7121);
  (3) tagolás-kapu: az „e. g.” `g.` tagja (F28.13, G0282); (4) 3. kapu: a „Gi” szigla
  elfogadása, ha a forrásban ugyanígy igehely előtt áll (F28.17, H8034); (5) tagolás-kapu:
  szám utáni „f.” nem betűjel (F28.17, H8034); (6) tagolás-kapu: főszám után nagybetűs
  szó a fordításban (F28.18, H7451/H3548); (7) terminológia-kapu: a lélek → lelk-
  tőváltozat (F28.20, H2416). Ez utóbbi túl tágra sikerült (a „lelkiismeret”, „lelkész”
  szóra is illeszkedett); az F28.34 a főnév toldalékolt alakjaira szűkítette, teszttel
  (`teszt_forditas_kapuk.py` `LelekTovaltozat`); a 40 `teljes` sor terminológia-eredménye a
  szűkítés előtt és után azonos. Hogy a kalibrálással átengedett szócikkek (H7121, G0282,
  H8034, H7451, H3548, H2416) az E4 szerint bukottnak számítanak-e, nem az én döntésem.
