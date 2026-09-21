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

Nem létező eszköz (`jelolt.py`, `_tanitoi_kereses.md` minta, a
`lexikai-scan`/tanítói/audit subagentek) **kizárólag** az `F8 — nincs eszköz`
jelöléssel szerepel — futtathatóként sehol nem áll.

## A) szakasz — bővített tanulmány: a motívum felismerése

| # | Lépés | Ki | Kimenet | Ma mivel fut | Megjegyzés |
|---|---|---|---|---|---|
| A1 💎 | a szakasz feldolgozása, PaRDeS-kifejtés | kutató | bővített tanulmány prózája | kézi | drága modell (l. lent) |
| A2 💎 | 2. pont kulcsszó-táblázata | kutató | kulcsszavak, Strong-számmal | kézi | drága modell |
| A3 | a kulcsszó-táblázat sorainak kiírása a táblába | végrehajtó | `jeloltek.tsv` sorok | `F8 — nincs eszköz` | nincs általános study→`jeloltek.tsv` betöltő; a történeti F3-betöltők (`f3_1_betoltes.py`, `f3_2_betoltes.py` stb.) egyediek, egy adott retroaktív menethez kötve, nem újrafelhasználhatók |
| A3b | jelölt-generálás meglévő motívumokhoz | végrehajtó (`jelolt.py`) | automatikus jelöltlista | `eszkozok/jelolt.py --szakasz "…"` | formulaikus motívumnál a sorok `pozicionális ellenőrzés kell` jelzést kapnak; `beépítve`/`elutasítva` soha nem íródik |
| A4 💎 ⛔ | motívum-felismerés: új ID vagy meglévő ID új előfordulása | kutató javasol + **ember dönt** | `motivumok.tsv` + `elofordulasok.tsv` | kézi | **kötelező megállási pont — l. lent** |
| A5 | 3/b pont kereszthivatkozásai | kutató + végrehajtó | `kapcsolatok.tsv` | `eszkozok/lekerdez.py tsk` / `eszkozok/lekerdez.py karoli` | a lekérdezés fut; a `kapcsolatok.tsv`-be írás kézi |
| A6 💎 | előrejelzett motívum rögzítése (státusz = *előrejelzett*) | kutató | `motivumok.tsv` | kézi | drága modell |
| A6b | új ID esetén a 4.6 gate négy kérdésének megválaszolása | kutató + ember | `motivumok.tsv` mezői | kézi | `eszkozok/gate.py` az ütközés-/részhalmaz-jelentést adja (4. kérdés támpontja), a döntést nem helyettesíti |
| A7 | motívumnapló, index, sorozat-tábla újragenerálása | végrehajtó | generált fájlok | `eszkozok/general.py --cel naplo --ir` és `--cel index --ir` | a sorozat-tábla = a napló „Feldolgozott igeszakaszok listája", kézi (l. N10, N11, `ATALAKITASI_TERV.md.md` A7); csak a napló és az index rész generált |

## B) szakasz — küszöbátlépés és tematikus study

| # | Lépés | Ki | Kimenet | Ma mivel fut | Megjegyzés |
|---|---|---|---|---|---|
| B1 | küszöbfigyelő jelzi a ⭐ 3+ átlépést | audit | jelentés | `eszkozok/kuszob.py` | a ⭐ számítás a `general.py`-ban marad, a `kuszob.py` importálja; átlépés = ≥ 3 és üres `forras_study`; kód 1 = van átlépés |
| B2 | gerinc-metszet + grammatikai szűrés | végrehajtó | kivonat | `eszkozok/lekerdez.py gerinc` | a grammatikai szűrés (`adat/grammatikai_strongok.tsv`) be van építve |
| B3 💎 | szemantikai mező-hipotézis | kutató | mező-szavak listája | kézi | drága modell — a menet egyetlen generatív lépése |
| B4 | teljes scan + kollokáció + igealak + LXX-híd | végrehajtó | jelölt-halmaz provenienciával | `eszkozok/lekerdez.py scan` / `kollokacio` / `igealak` / `lxx-hid` | mind a négy parancs fut, mindegyik saját provenienciát ír |
| B5 💎 ⛔ | jelöltek minősítése | **ember** + kutató javaslattal | `jeloltek.tsv` kitöltve | kézi | **kötelező megállási pont — l. lent** |
| B6 | beépített sorok átvezetése | végrehajtó | `elofordulasok` + `kapcsolatok` | `F8 — nincs eszköz` | nincs általános beépítő; a történeti betöltők egyediek (l. A3) |
| B7 | study 1. pont, kereszthivatkozás-napló, index generálása | végrehajtó | generált fájlok | `eszkozok/general.py --cel study`; `--cel naplok`; `--cel index --ir` | a `study` és a `naplok` cél **nem élesíthető** — csak `--kimenet` alá termel próbát; kizárólag az `index` írható közvetlenül élesen |
| B8 💎 | 2-5. pont megírása | kutató | PaRDeS-próza | kézi | drága modell |
| B9 | nevesített tanítói menet | tanítói-agent | `_tanitoi_kereses.md` | `F8 — nincs eszköz` | sem a subagent, sem a minta-fájl nem létezik |
| B10 | Q-kapu + konzisztencia-ellenőrzés | audit | jelentés | `eszkozok/ellenoriz.py [--study …]` | Q2–Q6 és a `felteteles` datasetek kézi; hook nincs (F8 §3) |

## C) szakasz — lexikon-oldal

| # | Lépés | Ki | Kimenet | Ma mivel fut | Megjegyzés |
|---|---|---|---|---|---|
| C1 | lexikon TUDOMÁNYOS szakaszainak generálása | végrehajtó | generált fájl | `eszkozok/general.py --cel lexikon --ir` | a generált szakaszok: **0, 1, 2, 3, 4, 5, 9** — nem 0-8 (l. lent) |
| C2 💎 | a kézi részek megírása | kutató | kézi blokkok | kézi | drága modell — hét kézi rész, l. lent |
| C3 💎 | lexikon OLVASHATÓ megírása | kutató | kézi fájl | kézi | drága modell; ma egyetlen `_OLVASHATO.md` sem létezik |
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
Ma egyik subagent sincs definiálva: a `.claude/` alatt nincs `agents/`
könyvtár és nincs `settings.json`. A három érintett szerep ma:

- **audit (B1, B10)** — nem subagent, hanem szkript-szerep: a B1-hez a
  `kuszob.py`, a B10-hez az `ellenoriz.py`.
- **`lexikai-scan` (B2, B4)** — ma nem burkolt subagent, hanem közvetlen
  `lekerdez.py`-hívás a fő szálon.
- **tanítói (B9)** — a tervben valódi subagent-szerep; ma nincs eszköz, sem
  minta-fájl.

## Generátor-tények

- `ELESITHETO = {naplo, index, nyitott, lexikon}` — ez a négy `general.py
  --cel` érték írható közvetlenül éles fájlba (`--ir`).
- A `naplok` és a `study` cél **nem élesíthető** ebben a fázisban — csak a
  `--kimenet` könyvtár alá termel próbát, `--ellenoriz`-nél PIROS marad.
- A ⭐ 3+ küszöb-számítás a `general.py`-ban él (`fo_elofordulas_csoportok()`
  + `render_naplo_kuszob()`), nem a `gate.py`-ban és nem a `lekerdez.py`-ban.
  A küszöb-összevetést és a kilépési kódot a `kuszob.py` adja (F8.4).

## C) szakasz — a lexikon-generálás tényleges hatóköre

A terv 462. sora (F6-szakasz) és a C1/C2 sor korábban „0-8. szakasz
generálva"-t és „9. szakasz = Nyitott kérdések"-et állított. Ez az F6 óta nem
igaz (l. `ATALAKITASI_TERV.md.md` F7.4 javítása):

- **generált** szakaszok: 0 (Metaadatok), 1 (Előfordulások), 2
  (Lexikon-szócikkek), 3 (LXX-híd — nyers adat), 4 (TSK és Károli-KH — nyers
  eredmény), 5 (Kapcsolatok), 9 (Források és licencek).
- **kézi** részek (hét): 1/b (PaRDeS keretrendszer), „Miért fontos ez a
  lelet" (a 2. szakasz minden többforrásos szócikke után), „Minősítés" (a 4.
  szakasz után), „Alátámasztás" (az 5. szakasz után), 6 (Módszertani napló),
  7 (ÚJ FELISMERÉS, ha van), 8 (Nyitott kérdések és séma-korlátok).

## Mi hiányzik az üzemmenetből ma

Hét tétel, mindegyik `F8` (l. `F8_BRIEF.md` §0):

1. **`jelolt.py`** (A3b) — jelölt-generálás meglévő motívumokhoz.
2. **A B1 küszöbfigyelő önálló eszköze** (`kuszob.py`) — ma a `general.py`
   csak számol, küszöböt nem hasonlít, kilépési kódot nem ad.
3. **`ellenoriz.py`** (B10) — az `adat/SEMA.md` §3 szabályai és a Q-kapu gépi
   része (Q1, Q7).
4. **`betolt.py`** (A3, B6) — study→adat átjáró; csak `beépítve` sort léptet elő.
5. **A tanítói keresés sablonja** (B9).
6. **Két subagent** (B4, B9) — `lexikai-scan` és `tanito-kereso`; az audit (B1,
   B10) és a C1 szkript marad (F7 D3).
7. **A „sorozat-tábla"** (A7) — definiálva az F8.2-ben, l. `NYITOTT_FELADATOK.md` N10.
