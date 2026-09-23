# Munkamenet — a bővített tanulmánytól a lexikon-oldalig

*Készült: F7 (chat-menet, Sonnet), 2026-09-20, a mérés forrása `F7_BRIEF.md` §1.*

## Mire való, mire nem

Ez a fájl az `ATALAKITASI_TERV.md.md` 7. pontjának („Az új munkamenet") 23
lépését rögzíti egy táblában, lépésenként: ki végzi, mi a kimenete, és **ma**
mivel fut. Nem specifikáció-forrás — a lépések tartalmát és sorrendjét a terv
7. pontja adja, ez a fájl csak a mai üzemi állapotot vetíti rá.

**Ami itt NEM szerepel, csak hivatkozásként:**
- a hét lépéses determinisztikus kutatási protokoll (gerinc-metszet →
  szemantikai mező-hipotézis → teljes scan → kollokáció → igealak-ellenőrzés
  → LXX-híd → nevesített tanító) — l. `CLAUDE.md`, „Kutatási menet — a hét
  lépés";
- a 4.6 motívum-gate négy kérdése (azonosság hordozója, negatív kritérium,
  funkció-különbség, részhalmaz) — l. `CLAUDE.md`, „Új motívum-ID kiosztása —
  négy kérdés, kötelezően".

Mindkettő egy igazság-forrásból él; ez a fájl nem másolja őket.

## A „ma mivel fut" oszlop értékei

Az oszlop kizárólag három alakot vehet fel:
1. **konkrét, ma létező parancs** — a hivatkozott szkript/cél ma is fut, `test -f`-fel ellenőrizve;
2. **kézi** — a lépés emberi/kutatói munka, nincs is szüksége eszközre;
3. **`F8 — nincs eszköz`** — a terv „végrehajtó" szerepet ír elő, de a hozzá tartozó eszköz (script, subagent, minta) ma nem létezik.

Nem létező eszköz **kizárólag** az `F8 — nincs eszköz`
jelöléssel szerepel — futtathatóként sehol nem áll.

## A) szakasz — bővített tanulmány: a motívum felismerése

| # | Lépés | Ki | Kimenet | Ma mivel fut | Megjegyzés |
|---|---|---|---|---|---|
| A1 💎 | a szakasz feldolgozása, PaRDeS-kifejtés | kutató | bővített tanulmány prózája | kézi | drága modell (l. lent) |
| A2 💎 | 2. pont kulcsszó-táblázata | kutató | kulcsszavak, Strong-számmal | kézi | drága modell |
| A3 | a kulcsszó-táblázat sorainak kiírása a táblába | végrehajtó | `kulcsszavak.tsv` sorok | `eszkozok/betolt.py kulcsszo --study … --konyv …` | átmeneti tábla, `id` nélkül (SEMA 2.8); a motívum-ID az A4-ben, a `jeloltek.tsv`-ben születik |
| A3b | jelölt-generálás meglévő motívumokhoz | végrehajtó (`jelolt.py`) | automatikus jelöltlista | `eszkozok/jelolt.py --szakasz "…"` | formulaikus motívumnál a sorok `pozicionális ellenőrzés kell` jelzést kapnak; `beépítve`/`elutasítva` soha nem íródik |
| A4 💎 ⛔ | motívum-felismerés: új ID vagy meglévő ID új előfordulása | kutató javasol + **ember dönt** | `motivumok.tsv` + `elofordulasok.tsv` | kézi | **kötelező megállási pont — l. lent** |
| A5 | 3/b pont kereszthivatkozásai | kutató + végrehajtó | `kapcsolatok.tsv` | `eszkozok/lekerdez.py tsk` / `eszkozok/lekerdez.py karoli` | a lekérdezés fut; a `kapcsolatok.tsv`-be írás kézi; minden futás proveniencia-sora → `adat/auditok.tsv` (`id`, `lepes`, `proveniencia`, `datum`), 0 találatnál is; a `lexikai-scan` által visszaadott sor ugyanígy |
| A6 💎 | előrejelzett motívum rögzítése (státusz = *előrejelzett*) | kutató | `motivumok.tsv` | kézi | drága modell |
| A6b | új ID esetén a 4.6 gate négy kérdésének megválaszolása | kutató + ember | `motivumok.tsv` mezői | kézi | `eszkozok/gate.py` az ütközés-/részhalmaz-jelentést adja (4. kérdés támpontja), a döntést nem helyettesíti |
| A7 | motívumnapló, index, sorozat-tábla újragenerálása | végrehajtó | generált fájlok | `eszkozok/general.py --cel naplo --ir` és `--cel index --ir` | a sorozat-tábla = a napló „Feldolgozott igeszakaszok listája", kézi (l. N10, N11, `ATALAKITASI_TERV.md.md` A7); csak a napló és az index rész generált |

## B) szakasz — küszöbátlépés és tematikus study

| # | Lépés | Ki | Kimenet | Ma mivel fut | Megjegyzés |
|---|---|---|---|---|---|
| B1 | küszöbfigyelő jelzi a ⭐ 3+ átlépést | audit | jelentés | `eszkozok/kuszob.py` | a ⭐ számítás a `general.py`-ban marad, a `kuszob.py` importálja; átlépés = ≥ 3 és üres `forras_study`; kód 1 = van átlépés |
| B2 | gerinc-metszet + grammatikai szűrés | végrehajtó | kivonat | `eszkozok/lekerdez.py gerinc` | a grammatikai szűrés (`adat/grammatikai_strongok.tsv`) be van építve; minden futás proveniencia-sora → `adat/auditok.tsv` (`id`, `lepes`, `proveniencia`, `datum`), 0 találatnál is; a `lexikai-scan` által visszaadott sor ugyanígy |
| B3 💎 | szemantikai mező-hipotézis | kutató | mező-szavak listája | kézi | drága modell — a menet egyetlen generatív lépése |
| B4 | teljes scan + kollokáció + igealak + LXX-híd | végrehajtó | jelölt-halmaz provenienciával | `eszkozok/lekerdez.py scan` / `kollokacio` / `igealak` / `lxx-hid` | mind a négy parancs fut, mindegyik saját provenienciát ír; burkoltan a `lexikai-scan` subagent (`.claude/agents/lexikai-scan.md`) is futtathatja; minden futás proveniencia-sora → `adat/auditok.tsv` (`id`, `lepes`, `proveniencia`, `datum`), 0 találatnál is; a `lexikai-scan` által visszaadott sor ugyanígy |
| B5 💎 ⛔ | jelöltek minősítése | **ember** + kutató javaslattal | `jeloltek.tsv` kitöltve | kézi | **kötelező megállási pont — l. lent** |
| B6 | beépített sorok átvezetése | végrehajtó | `elofordulasok` + `kapcsolatok` | `eszkozok/betolt.py beepit --munkalap …` | csak `beépítve` sort léptet elő; a `kapcsolatok` kézi (G10) |
| B7 | study 1. pont, kereszthivatkozás-napló, index generálása | végrehajtó | generált fájlok | `eszkozok/general.py --cel study`; `--cel naplok`; `--cel index --ir` | a `study` és a `naplok` cél **nem élesíthető** — csak `--kimenet` alá termel próbát; kizárólag az `index` írható közvetlenül élesen |
| B8 💎 | 2-5. pont megírása | kutató | PaRDeS-próza | kézi | drága modell |
| B9 | nevesített tanítói menet | tanítói-agent | `_tanitoi_kereses.md` | `tanito-kereso` subagent (`.claude/agents/tanito-kereso.md`) | a sablon: `sablonok/7_PaRDeS_tanitoi_kereses_sablon.md` |
| B10 | Q-kapu + konzisztencia-ellenőrzés | audit | jelentés | `eszkozok/ellenoriz.py [--study …]` | Q2–Q6 és a `felteteles` datasetek és a 8/c kézi; hook nincs (F8 §3) |

## C) szakasz — lexikon-oldal

| # | Lépés | Ki | Kimenet | Ma mivel fut | Megjegyzés |
|---|---|---|---|---|---|
| C1 | lexikon TUDOMÁNYOS szakaszainak + a törzscikk generálása (render) | végrehajtó | generált fájlok | `eszkozok/general.py --cel lexikon --ir`; `eszkozok/general.py --cel torzscikk --ir` | RENDER_BRIEF.md v5 (2. menet, R2.3) óta mind a 8 motívum lexikonoldalán a 10 generált blokk MELLETT a hét rés (`kivonat`, `2b`, `miert_fontos`, `minosites`, `alatamasztas`, `ertelmezes`, `modszertan`) is generált: `adat/res_forras.tsv` + a tanulmány/napló `<!-- RÉS-KEZDET/VÉGE -->` jelölői közötti törzse, vagy (`alatamasztas`-nál, 0-kapcsolatú motívumoknál és KIRALY-001-nél) egy adatból vezetett mondat alapján (G1/G2/G16). A `_TORZSCIKK.md` a lexikonoldalból renderel ("render a renderből", G7) — nem önálló lépés |
| C2 💎 | a rések megírása **a tanulmányban**, nem a lexikonoldalon | kutató | tanulmány-rés (a tematikus tanulmány vagy a kereszthivatkozás-napló `<!-- RÉS-KEZDET/VÉGE -->` jelölői között) | kézi | drága modell — hét rés, l. lent. **A lexikonoldal kézzel nem szerkeszthető** (RENDER_BRIEF.md G4); a `ellenoriz.py` 11. szakasza SÉRTÉSnek jelzi az eltérést |
| C3 💎 | ~~lexikon OLVASHATÓ megírása~~ — MEGSZŰNT (2026.09.21, felhasználói döntés): a lexikon-oldal egyetlen változata a _TUDOMANYOS.md | kutató | kézi fájl | kézi | drága modell; az első (ISTENTISZT-001) átemelve a pilotból, a többi a célvonal-döntéstől függ |
| C4 | commit/push, `main` merge | végrehajtó + ember | — | kézi | git-parancsok a `CLAUDE.md` szabálya szerint; nincs önálló script |

💎 = a kilenc, drága modellt igénylő lépés (A1, A2, A4, A5 — a kutatói rész, A6, B3, B8, C2, C3). ⛔ = kötelező emberi megállási pont.

## A4 és B5 — kötelező megállási pont

**A4** és **B5** nem azért állási pont, mert az ügynök autonóm, hanem mert a
2026.09.11-i modell-összehasonlításban *mindkét* ág átlépett egy besorolási
döntési ponton anélkül, hogy jelezte volna: a Sonnet-ág némán követte a
motívumnapló 5:29-re vonatkozó döntését, az Opus-ág némán felülírta — egyik
sem kérdezett (`ATALAKITASI_TERV.md.md` 520. sor). A menet ezen a két ponton
**megáll és kérdez**, akkor is, ha a válasz nyilvánvalónak látszik.

## Szereposztás — a mai valóság

A terv 5.1 pontja hat szerepet ír le (fő szál, `lexikai-scan` subagent,
`tanito-kereso` subagent, `szerkeszto` subagent, `ellenor` subagent, ember).
Az F8.9 óta két subagent van definiálva a `.claude/agents/` alatt
(`settings.json` továbbra sincs); a `szerkeszto` és az `ellenor` subagent
nem F8-tárgy (`F8_BRIEF.md` §3). A négy érintett szerep ma:

- **audit (B1, B10)** — nem subagent, hanem szkript-szerep: a B1-hez a
  `kuszob.py`, a B10-hez az `ellenoriz.py` (F7 D3 — az audit determinisztikus,
  a modell csak hibaforrás volna).
- **`lexikai-scan` (B2, B4)** — `.claude/agents/lexikai-scan.md`, haiku;
  kizárólag `lekerdez.py`/`jelolt.py` futtatása, fájlt nem ír.
- **`tanito-kereso` (B9)** — `.claude/agents/tanito-kereso.md`, sonnet; a
  `sablonok/7_PaRDeS_tanitoi_kereses_sablon.md` szerint dolgozik, kizárólag a
  `[study-mappa]/naplok/[motívum]_tanitoi_kereses.md` fájlt írja.

## Generátor-tények

- `ELESITHETO = {naplo, index, nyitott, lexikon, torzscikk}` — ez az öt
  `general.py --cel` érték írható közvetlenül éles fájlba (`--ir`).
- A `naplok` és a `study` cél **nem élesíthető** ebben a fázisban — csak a
  `--kimenet` könyvtár alá termel próbát, `--ellenoriz`-nél PIROS marad.
- A ⭐ 3+ küszöb-számítás a `general.py`-ban él (`fo_elofordulas_csoportok()`
  + `render_naplo_kuszob()`), nem a `gate.py`-ban és nem a `lekerdez.py`-ban.
  A küszöb-összevetést és a kilépési kódot a `kuszob.py` adja (F8.4).

## C) szakasz — a lexikon-generálás tényleges hatóköre

A terv 462. sora (F6-szakasz) és a C1/C2 sor korábban „0-8. szakasz
generálva"-t és „9. szakasz = Nyitott kérdések"-et állított — ez azóta a
LEXV2_2 (v2 oldalszerkezet) és a RENDER_BRIEF.md v4 (1. menet) miatt kétszer
is módosult. **Ma érvényes állapot** (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`
v3, `eszkozok/lexikon_general.py`):

- **generált** szakaszok (10 blokk, `general.py --cel lexikon`): Tartalomjegyzék,
  Jelmagyarázat, 1. Előfordulások, 1/b. Kizárt és vizsgált helyek, 2. Szótári
  háttér, 3. LXX-fordítói döntések, 4. Kereszthivatkozások, 5. Kapcsolatok,
  8. Irodalom és idézés, Kolofon.
- **rés** (hét, `res_blokkok_alkalmaz()`, RENDER_BRIEF.md G1–G4): `kivonat`,
  `2b`, `miert_fontos`, `minosites`, `alatamasztas`, `ertelmezes`,
  `modszertan` — fejlécsoruk a `adat/res_forras.tsv`-ből, törzsük vagy a
  motívum tematikus tanulmányából/kereszthivatkozás-naplójából
  (`forras=tanulmany`), vagy — csak a 0-kapcsolatú motívumok
  `alatamasztas` résénél, és a KIRALY-001 `alatamasztas` résénél —
  a `res_forras.tsv`-be előre rögzített, adatból vezetett mondatból
  (`forras=adat`, G16/D26, RENDER_BRIEF.md D28). A `forras=lap` a
  RENDER_BRIEF.md 2. menetének végére (R2.3) megszűnt: mind az 56 sor
  `tanulmany` vagy `adat` forrású (`adat/res_forras.tsv`). A lexikonoldal
  ezeket a szakaszokat is a generátorral kapja; **kézzel csak a
  tanulmányban szerkeszthetők** (G4). A lexikonoldal első sora fájl-szintű
  gépi jelölést hordoz (`<!-- GENERÁLT: general.py --cel lexikon | rések:
  [forras_study] -->`, R2.5) — nem tévesztendő össze a 10 blokk saját
  GENERÁLT-KEZDET/VÉGE jelölésével.
- a **törzscikk** (`lexikon/[ID]_TORZSCIKK.md`, `general.py --cel torzscikk`)
  a lexikonoldalból renderel, önálló kézi rész nélkül (G7); a törzscikk
  a 【NAPLO...】 folyamat-jelölő blokkokat és a fájl-szintű GENERÁLT-sort
  is eltávolítja (K9: egyik sem jelenhet meg a törzscikkben).

## Mi hiányzik az üzemmenetből ma

Az F8 óta nincs `F8`-jelölt hiány. Nyitva: `NYITOTT_FELADATOK.md` N11, N13, N15 és
az `F8_BRIEF.md` §3 tételei. (N14 lezárva, 2026.09.21.)
