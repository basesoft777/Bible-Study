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
„sense” szót (H7121: *in this sense*) HIBA-nak vette; a blockquote a D11 szerint
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
