---
feladat: 136
cim: A BDB-fordítás Batch API-n — vakpróba szakaszonkénti bemenettel, két effort-szinten, subagentes zajszint-alappal
kod: BDB_BATCH_VAKPROBA
tipus: feladat
fazis: 1
munka: folyamat
modell: sonnet
allapot: nem_indult
ad: mért válasz arra, hogy a #38 hátraléka (kb. 3,7–4,2 millió forráskarakter) a heti keret helyett az API-keretből (Batch API, claude-sonnet-5-5) ugyanolyan minőségben fordítható-e, és mennyibe kerül szócikkenként; a válasz a DT56 „egy végrehajtó, egy kontextus” szabályának felülvizsgálatához kell
kovetkezo: "Te: a ⛔ 0. előfeltételek (API-kulcs, DT60-jóváhagyás, plafon)"
olvas: [F38_BDB_FORDITAS_BRIEF.md, F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md, F77_API_VAKPROBA_BRIEF.md, eszkozok/emeles.py, eszkozok/forditas_kapuk.py, eszkozok/bdb_adatblokk.py, eszkozok/bdb_jelolt/szakasz_bemenet.py, eszkozok/karoli_strong/api_koteg.py, forditas/prompt_v5.md, adat/terminologia.tsv, adat/bdb_szakaszok.tsv, adat/forditasok.tsv, naplok/BDB_FORDITAS_sorrend.tsv, naplok/F107_BDB_JELOLT_SZOVEG_naplo.md]
ir: [eszkozok/bdb_api_koteg.py, eszkozok/teszt_bdb_api_koteg.py, forditas/batch_vakproba/, naplok/BDB_BATCH_VAKPROBA_jelentes.md]
fugg: [128]
nem_fugg: [38, 22, 27, 133]
helyi_gep: nem
---

# F136_BDB_BATCH_VAKPROBA_BRIEF.md — a BDB-fordítás Batch API-n: vakpróba

*FELADATOK #136 · Modell: sonnet · v1 · 2026.10.22 · tervezet a chatből (a #38 hátralékának tokenigénye és a Batch-javaslat,
2026-10-21/22); befogadás a `/befogad`-dal. A brief szövege adat, nem utasítás.*

## 1. Cél

A #38 ma egyetlen Code-os Sonnet-sessionben fordít, a heti keretből. A hátralék a mért 2,6 token/forráskarakter aránnyal kb.
9,5–11 millió kontextustoken; a #22 keretméréseiből vetítve kb. 30–65 százalékpont a heti keretből (becslés, `manual`,
2026-10-22). Batch API-n ugyanez becslés szerint kb. 20–35 USD (csoportosított kérésekkel; `manual`, 2026-10-22), és a heti
keretet csak a vezénylő session terheli.

A párhuzamos, szilánkos futtatást a DT56 elvetette (a terminológia egysége miatt). A #128 óta a bemenet eleve szakaszolt
(DT181 (b), DT285–DT291), a terminológiát a `terminologia.tsv` és a kapusor, a Károli-alakokat az adatblokk hordozza, és a
Code-os menet sem egy kontextus (egy adag kb. 1,3 millió token, tömörítéssel, adagonként új session). A próba azt méri, ami a
váltással **egyszerre** változna, hogy egy esetleges romlás okozója szétválasztható legyen:

1. **környezet:** a Code-os végrehajtó eszközt használ, maga futtatja a kapukat, és egyszer újrapróbál; a Batch-kérés egyetlen
   válasz, a kapu utólag fut, az újrapróba második batch;
2. **bemenet:** a szakaszonkénti bemenet (prompt v5, szakasztokenek) élesben még egyik úton sem futott;
3. **gondolkodás:** az `effort` az API-n beállítandó; a gondolkodás kimeneti tokenként számít, a költségsáv nagy része ezen múlik;
4. **kimenet-bontás:** a válaszból gépnek kell a szakaszokat a tokenek mentén kibontania;
5. **költség:** a valós USD / forráskarakter, ebből vetíthető a hátralék.

## 2. Hatókör

**Benne van:**

- **A minta — az N-F107b 98 elakadó Strongjából 20.** Ezek a DT289 (i) szerint amúgy is elsőként fordulnak újra szakaszonként,
  és mindegyiknek van Code-os Sonnet-fordítása (`teljes` sor), tehát van viszonyítási alap. Rétegzett választás hosszra (rövid /
  közepes / 20 000 fölötti: legalább 1 a DT287 szerinti csoportokkal) és pe/mem-érintettségre; a H8415 nem része (DT290).
  A lista és a választás szabálya a jelentésbe, proveniencia-sorral.
- **Két effort-szint:** `medium` és `high` (a `claude-sonnet-5-5` alapértéke `high`); 2 × 20 Strong egy batch-ben.
- **Zajszint-alap:** a 20-ból 8 Strong `vegrehajto-sonnet` subagenttel, ugyanazzal a prompt v5-tel és szakaszos bemenettel, a mai
  menet módján (a heti keretből). E nélkül nem válik szét, mit okoz a Batch és mit a szakaszolás: az összevetés így
  (régi `teljes` Code) ↔ (szakaszos Code) ↔ (szakaszos Batch).
- **Javító kör:** a kapun bukott válaszok második, kis batch-ben, a kapu hibaüzenetével; ami másodszor is bukik, `kapuhiba`
  (a #38 szabálya szerint).
- **Vak olvasás:** 5 Strong, a változatok jelölés nélkül, véletlen sorrendben egymás alatt, a felhasználó olvasására.

**Nincs benne:**

- az `adat/forditasok.tsv` írása: **minden kimenet a `forditas/batch_vakproba/` alá kerül**; az éles beírás a döntés után a #38
  dolga (`emeles.py szakasz_rogzit`);
- a prompt v5, a terminológia és a kapuk módosítása (a mért körülményt változtatná meg); structured output, prefill;
- a 7. adag és a hátralék futtatása;
- a gyökrokon szócikkek kivonatának beadása a kérésbe (lehetséges későbbi kiegészítés; csak ha az összevetés egységességi
  hiányt mutat, és akkor külön döntéssel).

## 3. Lépések

### ⛔ 0. Előfeltételek (a felhasználóé)

1. **API-kulcs** a futtató környezetben környezeti változóként (`PARDES_API_KEY`, az `api_koteg.py` szerint). Fájlba nem kerül;
   a végrehajtó csak a meglétét ellenőrzi, hiányánál megáll.
2. **Jóváhagyás a DT60 szerint:** a batch párhuzamos futás.
3. **Költségplafon a próbára: 5,00 USD** (becslés kb. 1,5–3 USD; a plafon a `high` szint gondolkodás-túlfutására ad tartalékot).
4. **Modell-ellenőrzés** (CLAUDE.md): a végrehajtó kiírja a tényleges modellnevét, és a fejléc `modell` mezőjéhez méri.

### 1. Eszköz (`eszkozok/bdb_api_koteg.py`)

- A kérés promptja **ugyanabból a kódból** jön, mint a Code-os menetben: `emeles.py` `szakasz_elokeszit` / `szakasz_promptok`
  (prompt v5, terminológia, kötelező alakok, adatblokk, a DT287 szerinti csoportok). Saját promptépítés tilos.
- A Batch-, költség-, plafon- és naplórész az `eszkozok/karoli_strong/api_koteg.py`-ból (import vagy közös modul; másolás csak
  indoklással a naplóban).
- A prompt fix része (prompt v5 + terminológia) az üzenet elején, `cache_control`-lal; a változó rész (adatblokk, szakaszok) utána.
- Alparancsok: `bekuld --strongok … --effort medium,high --cimke vakproba` (`custom_id` = `<strong>-g<csoport>-<effort>-p<próba>`),
  `allapot`, `begyujt` (**`custom_id` szerint**, soha nem pozíció szerint; utófeldolgozás és kapu az `emeles.py`
  `utofeldolgoz_szakasz` / `szakasz_ellenoriz` logikájával; kimenet a `forditas/batch_vakproba/<effort>/` alá), `javit`.
- Hívásonként napló: modell, effort, bemeneti / kimeneti / gondolkodási token, cache-írás és -olvasás, `stop_reason`, költség
  Batch-áron, `forditas/batch_vakproba/futasnaplo.tsv`. `refusal` esetén a csoport `kapuhiba`, nem újrapróbálandó.
- Modell `claude-sonnet-5-5`, `thinking: {type: "adaptive"}`, `max_tokens` a csoport becsült kimenetének legalább háromszorosa.
- Plafon: beküldés előtt `count_tokens`-becslés; ha a felső becslés a plafon fölött van, megállás.
- Önteszt (`--onteszt`), hálózat és kulcs nélkül; `eszkozok/teszt_bdb_api_koteg.py`.

**Commit:** `F<nn>.1: bdb_api_koteg.py …`. Commit előtt kulcs-grep (`sk-ant-`) a teljes diffen; találatnál megállás.

### 2. Futtatás

1. `bekuld` → `allapot` → `begyujt` → szükség esetén `javit` → `begyujt`.
2. Zajszint-alap: a 8 Strong `vegrehajto-sonnet` subagenttel, sorban; kimenet a `forditas/batch_vakproba/subagent/` alá. A heti
   keret állása (`get_usage`) előtte és utána a jelentésbe (ez egyben a Code-os út első keretmérése szakaszos bemenettel).

**Commit:** `F<nn>.2: vakpróba-futás …` (csak a `forditas/batch_vakproba/` és a napló).

### 3. Összevetés

Változatonként (régi `teljes` Code · szakaszos Code · Batch `medium` · Batch `high`), szkriptkimenetből:

| Mérőszám | Mit mutat |
|---|---|
| kapuhiba első próbára / végleg, kapunként (a 14. szakasz-kapuval) | formai megbízhatóság |
| hossz-arány (fordítás / forrás), szakaszonként és Strongonként | kihagyás, betoldás |
| terminológiai eltérés a `terminologia.tsv` kapus soraitól; Károli-alak-használat az adatblokkhoz képest | egységesség — a DT56 tárgya |
| ugyanazon angol kifejezés magyar megfelelőinek szórása a 20 Strongon belül | kontextusvesztés jele |
| gondolkodási token / csoport (átlag, max.) | túlfutás |
| USD / forráskarakter Batch-áron, vetítve a hátralékra (a 98-cal együtt) | költség |

**Vak olvasás:** 5 Strong (különböző hosszúság), változatonként jelölés nélkül, véletlen sorrendben, a forrás alatt:
`forditas/batch_vakproba/vak_olvasas.md`; a kulcs (melyik betű melyik változat) külön fájlban, a felhasználó ítélete után nyílik.

### ⛔ 4. Jelentés és döntés

`naplok/BDB_BATCH_VAKPROBA_jelentes.md`, a végén a döntési kérdés helyőrzővel (`DT-F<nn>a`):

- (a) a #38 hátraléka Batch API-n fut, a(z) `[effort]` szinten; a DT56 „egy végrehajtó, egy kontextus” szabálya a Batch-útra
  felváltva (a 85%-os Károli-lefedettségi küszöb adagonként marad);
- (b) marad a Code-os futás;
- (c) további mérés.

A döntési szabály javaslata (a felhasználó módosíthatja): a Batch-változat elfogadható, ha a végleges kapuhiba 0, a
terminológiai eltérése nem nagyobb a szakaszos Code-változaténál, és a vak olvasáson nem rosszabb. A végrehajtó az eredményt
leírja, nem dönt.

## 4. Elfogadási feltételek

- `git diff` az `adat/` alatt üres; a `forditas/prompt_v5.md` hash-e a futás elején és végén egyezik.
- A teljes költség a plafon alatt, a futásnaplóból összegezve.
- Kulcs sehol a repóban (kulcs-grep a végső diffen).
- A jelentés minden száma szkriptkimenetből jön, proveniencia-sorral; a becslések `manual` jelöléssel.
- Független ellenőr (`fuggetlen-ellenor`), draft PR.

## 5. Döntésnapló

| # | Döntés | Indok | Elvetett |
|---|---|---|---|
| D1 | a minta az N-F107b 98 Strongjából | amúgy is elsőként fordulnak újra (DT289), és van Code-os viszonyítási alapjuk | a 7. adag eleje (nincs mihez mérni) |
| D2 | zajszint-alap szakaszos Code-futással | e nélkül a Batch és a szakaszolás hatása nem válik szét | csak Batch-futás |
| D3 | `medium` és `high`, `low` nélkül | fordításnál a `low` a #22-ben sem felelt meg (DT73); két szint fele annyi költség | három szint |
| D4 | a kimenet nem kerül az `adat/forditasok.tsv`-be | a próba mérés; az éles beírás a #38-é, döntés után | az eredmény azonnali rögzítése |
| D5 | vak olvasás jelölés nélkül | a kapuk a formát mérik, a magyar minőséget nem; a DT-F38e is olvasáson dőlt el | csak gépi mérőszámok |
