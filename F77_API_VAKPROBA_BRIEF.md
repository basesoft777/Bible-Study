---
feladat: 77
cim: Károli–Strong párosítás API-n — vakpróba a Józsué kész kötegein, Batch API-val, három effort-szinten
kod: API_VAKPROBA
tipus: feladat
fazis: 1
munka: folyamat
modell: sonnet
allapot: megallt
ag: claude/wonderful-einstein-ezr2pw
ad: mért válasz arra, hogy a #22 párosítása a Max-keret helyett az API-keretből (Batch API, claude-sonnet-5-5) ugyanazt adja-e, mint a mostani subagentes futás, és mennyibe kerül versenként
kovetkezo: "Te: merge (közös PR a #22 Ézs- és Jer-menetével). A DT73 (a) alkalmazva: F77.9–F77.11 (könyvenkénti plafon, futás-címke a --gyoker szerint); az Ézs és a Jer API-n lefutott (#22 D16, D17). Nyitva: `--koteg-meret` kapcsoló és 5 verses plafon-alap a következő prófétai könyv előtt (DT71 (b))."
olvas: [f21p/prompt_v3.md, f21p/prompt_v3.sha256, eszkozok/karoli_strong/sonnet_koteg.py, eszkozok/karoli_strong/bemenet.py, eszkozok/karoli_strong/kapu.py, eszkozok/karoli_strong/tokenek.py, eszkozok/karoli_strong/egyesit.py, f22/minta_Jozs.tsv, f22/valaszok/sonnet/Jozs.jsonl, adat/karoli_strong/parok_Jozs.tsv, naplok/F22_Jozs_jelentes.md, F22_KAROLI_STRONG_BRIEF.md]
ir: [eszkozok/karoli_strong/api_koteg.py, eszkozok/karoli_strong/api_vakproba_osszevet.py, f22/vakproba/, f22/api_termeles/futasnaplo.tsv, naplok/F22_API_VAKPROBA_jelentes.md]
fugg: []
nem_fugg: [22, 48]
helyi_gep: nem
---

# F77_API_VAKPROBA_BRIEF.md — Károli–Strong párosítás API-n: vakpróba

*FELADATOK #77 · Modell: sonnet · v1 · 2026.10.08 · a chatben készült (a 100 USD-s havi API-keret kihasználása)*

## 1. Cél

A #22 ma `vegrehajto-sonnet` subagentekkel fut, a Max-keretből. Ha ugyanaz a munka az Anthropic API-n (Batch API, fél áron) is ugyanolyan minőségű, a hátralévő könyvek a havi API-keretből futhatnak, a Max-keret és a heti 85%-os megállás nélkül.

A prompt ugyanaz marad (`prompt_v3`, befagyasztva), de három körülmény változik, és ezeket méri a próba:

1. **a környezet**: a subagent a Claude Code rendszerpromptjával kapja a promptot, az API-hívás nélküle;
2. **a gondolkodás**: az API-n az `effort`-ot nekünk kell beállítani (a pilotban a Sonnet nem tartotta a gondolkodási keretet: 11 144 token/hívás, `naplok/F21P_jelentes.md`);
3. **a költség**: a valós USD/vers érték, mert csak ebből látszik, hány könyv fér a havi keretbe.

## 2. Hatókör

**Benne van:**
- a Józsué 5 kész kötege (javaslat: 1., 6., 25., 45., 53.; a 6. és az 53. az eredeti futásban első próbára kapuhibás volt, így a javító kör is mérhető), összesen kb. 50 vers;
- három `effort`-szint: `low`, `medium`, `high` (a `claude-sonnet-5-5` alapértéke `high`); 3 × 5 = 15 kérés egyetlen batch-ben;
- **zajszint-alap**: ugyanaz az 5 köteg még egyszer `vegrehajto-sonnet` subagenttel (a Max-keretből, 5 subagent-hívás). E nélkül az egyezési szám nem értelmezhető: két subagentes futás sem egyezik 100%-ban;
- a javító kör: a kapun bukott válaszok egy második, kis batch-ben, a kapu hibaüzenetével (mint a `sonnet_koteg.py mentes` 2. próbája).

**Nincs benne:**
- új könyv futtatása (az a próba eredménye után külön döntés);
- a `prompt_v3` bármilyen módosítása, structured output vagy prefill (ez a mért körülményt változtatná meg);
- a `f22/valaszok/sonnet/Jozs.jsonl` és az `adat/karoli_strong/*_Jozs.tsv` módosítása: **a kész adat nem íródik felül**, minden kimenet a `f22/vakproba/` alá kerül;
- GitHub Actions: a szkript egy felhős Claude Code-sessionben (claude.ai/code) fut, helyi gép nélkül.

## 3. Lépések

### ⛔ 0. Előfeltételek (a felhasználóé)

1. API-kulcs a Console-ból, a felhős Claude Code-környezet beállításaiban környezeti változóként: `ANTHROPIC_API_KEY`. Fájlba (a `.env`-et is beleértve) nem kerül, mert a felhős klón a gitignore-olt fájlokat nem látja, és a kulcs így a repó közelébe sem jut. A környezet hálózati beállítása engedje az `api.anthropic.com`-ot. A végrehajtó a kulcsot nem kéri, nem írja és nem jeleníti meg; a menet elején csak azt ellenőrzi, hogy a változó be van-e állítva, és hiányánál megáll.
2. **Jóváhagyás a D15 szerint**: a batch párhuzamos futás (DT60: csak kifejezett jóváhagyással).
3. Költségplafon a próbára: **3,00 USD** (a becslés kb. 1 USD; a plafon a `high` szint esetleges gondolkodás-túlfutására ad tartalékot).

### 1. Eszköz (`eszkozok/karoli_strong/api_koteg.py`)

- `pip install anthropic` (ha hiányzik).
- A köteg promptja **ugyanabból a kódból** jön, mint ma: `sonnet_koteg.prompt_ir` (a `prompt_v3` hash-ellenőrzésével). Saját promptépítés tilos.
- Alparancsok:
  - `bekuld --konyv Józs --kotegek 1,6,25,45,53 --effort low,medium,high --cimke vakproba`: egy batch, `custom_id` = `<könyv>-k<köteg>-<effort>-p<próba>`; a batch-azonosító a `f22/vakproba/batchek.tsv`-be;
  - `allapot`: a batch állapota;
  - `begyujt`: az eredmények letöltése **`custom_id` szerint** (soha nem pozíció szerint), kapuellenőrzés a `sonnet_koteg.mentes` logikájával, de a kimenet a `f22/vakproba/<effort>/` alá; a bukott kötegek listája a javító körhöz;
  - `javit`: a bukott kötegek második batch-e a kapu hibaüzenetével; ami másodszor is bukik, `kapuhiba`.
- Hívásonként naplózza: modell, effort, bemeneti/kimeneti/gondolkodási token, cache-olvasás, `stop_reason`, költség (a Batch API árán), a `f22/vakproba/futasnaplo.tsv`-be (a `f22/futasnaplo.tsv` oszlopsorrendjével).
- Modell: `claude-sonnet-5-5`, `thinking: {type: "adaptive"}`, `max_tokens` 32 000. Ha a modell `refusal`-lal áll meg, a köteg `kapuhiba`, nem újrapróbálandó.
- Plafon: a beküldés előtt becslés a `count_tokens`-szel; ha a becslés felső értéke a plafon fölött van, megállás.
- Önteszt (`--onteszt`), hálózat és kulcs nélkül, a `sonnet_koteg.py --onteszt` mintájára.

**Commit:** `F<nn>.1: api_koteg.py …`. Commit előtt kulcs-grep (`sk-ant-` minta) a teljes diffen; találatnál megállás.

### 2. Futtatás

1. `bekuld` → `allapot` (a legtöbb batch egy órán belül kész, a felső határ 24 óra) → `begyujt` → szükség esetén `javit` → `begyujt`.
2. A zajszint-alap: az 5 köteg `vegrehajto-sonnet` subagenttel, sorban, a mai menettel azonos módon, a kimenet a `f22/vakproba/subagent/` alá.

**Commit:** `F<nn>.2: vakpróba-futás …` (csak a `f22/vakproba/` és a napló).

### 3. Összevetés (`eszkozok/karoli_strong/api_vakproba_osszevet.py`)

Mindhárom effort-szintre és a zajszint-alapra, a **meglévő `Jozs.jsonl`** ugyanazon kötegeihez képest:

| Mérőszám | Mit mutat |
|---|---|
| link-szintű egyezés (Károli-token → eredeti token) | a fő minőségi szám |
| `betoldas` / `forditatlan` egyezés | a nem párosított tokenek kezelése |
| kapuhiba első próbára / végleg | a kimenet formai megbízhatósága |
| gondolkodási token / köteg (átlag, max.) | a túlfutás mértéke |
| USD / vers (Batch-áron) és kivetítés a hátralévő ÓSZ-könyvekre | hány könyv fér a havi 100 USD-be |

Az eltérő linkekből 20-as minta kézi átnézésre (`f22/vakproba/elteresek_minta.tsv`, vers, Károli-szó, a két változat).

Minden szám szkriptkimenetből jön; a jelentés minden táblája alatt proveniencia-sor.

### ⛔ 4. Jelentés és döntés

`naplok/F22_API_VAKPROBA_jelentes.md`, a végén a döntési kérdés `DT-F<nn>` helyőrzővel:

- (a) a #22 hátralévő könyvei API-n futnak, a(z) `[effort]` szinten;
- (b) marad a subagentes futás;
- (c) további mérés (pl. nagyobb minta).

A döntési szabály javaslata (a felhasználó módosíthatja): az API-változat akkor elfogadható, ha a link-egyezése a meglévő futással **nem kisebb, mint a zajszint-alapé mínusz 1 százalékpont**, és a végleges kapuhiba 0. Az eredményt a végrehajtó csak leírja, nem dönt.

## 4. Elfogadási feltételek

- `git diff` a `f22/valaszok/`, az `adat/karoli_strong/` és a `f21p/` alatt üres.
- A `prompt_v3` hash-e a futás elején és végén egyezik.
- A teljes költség a plafon alatt, a futásnaplóból összegezve.
- Kulcs sehol a repóban (kulcs-grep a végső diffen).
- A jelentés minden száma szkriptkimenetből jön, proveniencia-sorral.

## 5. Döntésnapló

| # | Döntés | Indok | Elvetett |
|---|---|---|---|
| D1 | Józsué kötegek, nem új könyv | csak kész kötegen van mihez hasonlítani | új könyv előfutása (nincs viszonyítási alap) |
| D2 | zajszint-alap subagenttel | e nélkül az egyezési szám nem értelmezhető | csak API-futás |
| D3 | a kész adat nem íródik felül | a próba mérés, nem csere | a Józs újrafuttatása a helyén |
| D4 | felhős Code-session, Actions nélkül (a felhasználó kérése, 2026.10.08) | helyi gép nem kell; a #22 is Code-sessionben fut | helyi futás; GitHub Actions (külön workflow-munka) |
| D5 | F77.11: könyvenkénti költségplafon (vers × 0,0074 × 1,5, min. 1 USD) és a futásnapló `futas` címkéje a `--gyoker` szerint; az Ézs 145 sora átcímkézve (DT72: utólag elfogadva) | a DT73 (a) „a plafon a könyv méretére állítandó” pontja; az Ézs-ellenőr 3. és 8. eltérése | egyetlen 110 USD-s plafon; a régi címke megtartása |
