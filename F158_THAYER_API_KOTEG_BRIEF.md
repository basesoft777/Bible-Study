---
feladat: 158
cim: "A Thayer szakaszos fordításának API-kötegelője (Message Batches) és a teljes Thayer futási listája"
kod: THAYER_API_KOTEG
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: fut
ad: "eszkozok/thayer_api_koteg.py: a #132 szakaszos láncának (thayer_jelolt/forditas.py, prompt v5.1, adatblokk, 14–16. kapu) Batch-kötegelője a bdb_api_koteg.py mintájára (szaraz / bekuld / allapot / begyujt / kapuz / javit / rogzit / beir), a teljes Thayer futási listájával; hálózat nélküli tesztekkel; valódi beküldés nélkül (az első a #27 M1-e)"
kovetkezo: "/kovetkezo; utána a #27 (FP3) M1-e ezzel fut"
olvas: [eszkozok/bdb_api_koteg.py, eszkozok/karoli_strong/api_koteg.py, eszkozok/thayer_jelolt/, eszkozok/emeles.py, eszkozok/forditas_kapuk.py, forditas/prompt_v5_1.md, adat/thayer_szakaszok.tsv, adat/forditasok.tsv, adat/SEMA.md, F132_THAYER_SZAKASZ_BRIEF.md, F142_THAYER_M3_BRIEF.md, F27_FP3_BRIEF.md, DONTESEK.md]
ir: [eszkozok/thayer_api_koteg.py, eszkozok/teszt_thayer_api_koteg.py, naplok/THAYER_API_KOTEG_naplo.md]
fugg: []
nem_fugg: [7, 12, 22, 27, 38, 121, 153, 154]
---

# F158_THAYER_API_KOTEG_BRIEF.md — a Thayer szakaszos fordításának API-kötegelője

*FELADATOK #158 · Modell: sonnet · v1 · 2026.11.02 · készítette: `claude-opus-5-5` a `/befogad` menetében, a felhasználó döntése
szerint (DT-F27a, chat, 2026-11-02: „Mehet, külön #158”); a #27 (FP3) előfeltétele.*

## 1. Cél

A felhasználó döntése szerint (DT-F27a) a Thayer teljes magyar fordítása (#27 mérő adag, #7 éles) API-n, a Message Batches úton
fut, nem sessionből. A #132 szakaszos lánca (`eszkozok/thayer_jelolt/forditas.py`) **nem fordít**: a docstringje szerint a hívó
végzi a fordítást a kiírt promptokból. A BDB-nek van Batch-kötegelője (`eszkozok/bdb_api_koteg.py`, #38, a 13. adagtól), a Thayernek
nincs. Ez a feladat megírja: `eszkozok/thayer_api_koteg.py`.

Két hiányt pótol:

1. **A fordító út:** prompt → Batch-kérés → válasz → helyőrző-visszaállítás → javítóréteg és kapuk → munkatábla →
   `adat/forditasok.tsv`, a `forditas.py` függvényeivel, nem másolatukkal.
2. **A teljes Thayer futási listája:** a `thayer_jelolt/szolista.py` ma csak a motívumok gerincszavait listázza (DT332 (1)); a
   #27-nek és a #7-nek az 5 426 Strong kell, ugyanazzal a `kesz` / `forditando` állapotszabállyal.

## 2. Hatókör

**Benne van:** a kötegelő és a tesztje; hálózat nélküli `szaraz` futás és költségbecslés a teljes Thayerre és egy kb. 150 000
karakteres mintaadagra (a #27 M1 méretére); napló.

**Nincs benne:** **valódi beküldés vagy bármilyen hálózati hívás** (az első Batch a #27 M1-e, a felhasználó plafonjával); az
`adat/forditasok.tsv` írása; a #132 eszközeinek (`eszkozok/thayer_jelolt/`), az `emeles.py`-nak, a `forditas_kapuk.py`-nak, a
`bdb_api_koteg.py`-nak, az `api_koteg.py`-nak és a `prompt_v5_1.md`-nek a módosítása (ha a kötegelőhöz bármelyikhez hozzá kellene
nyúlni: megállás, tétel a `DONTESEK.md`-be); a sigla-tábla.

## 3. Követelmények

1. **Minta és újrahasználat.** A `bdb_api_koteg.py` szerkezete; a REST-hívó, a kulcskezelés (`PARDES_API_KEY`), a `tsv_olvas` /
   `tsv_hozzaad` és a git-mentés az `eszkozok/karoli_strong/api_koteg.py`-ból import, nem másolat. A prompt a
   `thayer_jelolt/forditas.prompt_epit`-ből épül, csoportonként (`thayer_bemenet.csoportok`); a görög/héber szakaszok a
   `emeles.helyorzo_bont` helyőrzőit kapják, mint a Code-os úton a `_szakasz_hely.txt` (a `bdb_api_koteg.kerelmek_strongra`
   mintájára); a visszaállítás betűhű (`emeles.helyorzo_visszaallit`).
2. **Alparancsok:**
   - `lista [--ki PATH] [--ts NAP]` — a teljes Thayer futási listája: minden `adat/thayer_szakaszok.tsv`-beli Strong a
     `szolista.allapot` szabályával (`kesz` / `nincs_szakaszos` / `hianyos` / `elavult_hash`), soronként proveniencia-sorral; a
     repóban fájlt nem ír;
   - `--adag N --strongok FÁJL szaraz` — a kérések összeállítása hálózat nélkül: kérés-, csoport- és karakterszám, token- és
     USD-becslés (a becslés jelölve, `manual`), csomagolási terv;
   - `bekuld`, `allapot`, `begyujt`, `kapuz`, `javit`, `rogzit`, `beir` — a `bdb_api_koteg.py` szerinti szerepben;
     a `kapuz` a `forditas.utofeldolgoz`-t hívja (javítóréteg + `kapuk_futtat_thayer`, benne `14_szakasz`, `15_tiltott`,
     `16_sigla`); a `rogzit` a `forditas.szakasz_sorok` szerint a munkatáblába (`naplok/F132_THAYER_SZAKASZ_munka.tsv`) ír,
     szakaszonként `jelentes_szam = sz<n>`; a `beir` a `forditas.beir`-t hívja (`--regi-elavult`, `--kezi-marad`, DT329);
   - `--onteszt` — a hálózat nélküli öntesztek.
3. **`custom_id`** = `<strong>-c<csoport>-p<próba>` (a BDB-vel azonos alak); a nagy szócikk csoportjai külön kérések.
4. **Modellnév:** a `rogzit` a `modell` mezőbe a válasz ténylegesen futott modellnevét írja (a Batch-válasz `model` mezője), nem
   konstansot.
5. **Plafon:** `PLAFON_USD` alapértéke **0** (beküldés tilos); a `bekuld` csak a felhasználó által megadott plafonnal
   (paraméter vagy konstans a #27 ⛔ M1 döntése szerint) indul, csomagonként ellenőrzi, és a plafon elérésekor megáll (kilépési kód
   3, a `bdb_api_koteg.py` szerint).
6. **Munkamappa:** `forditas/thayer_api/adag<N>/` (kérések, `valaszok.jsonl`, `kapu_eredmeny.jsonl`, `futasnaplo.tsv` USD-ben,
   `batchek.tsv`); `--munka PATH` felülírja (a száraz futás és a tesztek a repón kívülre írnak); a kulcs sehol nem íródik ki.
7. **Bukás:** a kétszer bukott Strong a `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`-be kerül (okkal), a futás továbbmegy.
8. **TSV:** `split('\t')` / `'\t'.join()`, a `csv` modul tilos; a táblát író lépés írás előtt összevet (minden más sor bájtra
   azonos). A szkript az importok után ráteszi a UTF-8 wrappert (CLAUDE.md).

## 4. Lépések

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév vs. `modell: sonnet`; eltérésnél nincs munka.
1. **Felmérés:** a `bdb_api_koteg.py` és a `forditas.py` összevetése — melyik függvény importálható változtatás nélkül, mi kell
   újonnan (a naplóba). Ha a `forditas.py` vagy az `emeles.py` módosítása nélkül nem megy: ⛔ megállás, tétel a `DONTESEK.md`-be.
2. **A kötegelő** megírása a 3. pont szerint.
3. **Tesztek** (`eszkozok/teszt_thayer_api_koteg.py`, hálózat nélkül):
   - a kötegelő promptja egy csoportra bájtra azonos a `forditas.prompt_epit` kimenetével (a helyőrzős forrásrésztől eltekintve), és
     a helyőrző-visszaállítás körútja betűhű;
   - egy kész `sonnet` szakaszos fordítás (pl. a G1941 sorai a `forditasok.tsv`-ből) hamis Batch-válaszként a `kapuz`-on átmegy, a
     `rogzit` (ideiglenes munkatáblába) a meglévő sorokkal azonos `forras_hash`-t és `jelentes_szam`-ot ad;
   - a `lista` minden Strongot lefed (5 426, a `thayer_szakaszok.tsv` szerint), és a kész Strongokat `kesz`-nek adja;
   - 0 plafonnal a `bekuld` nem indul; a `custom_id` oda-vissza bontható.
4. **Száraz futás:** `lista` a teljes Thayerre és `szaraz` egy kb. 150 000 karakteres mintaadagra (a lista első Strongjai Strong-szám
   szerint, mert a gyakorisági sorrend a #27 M0-é) és a teljes Thayerre; az eredmény a naplóba (`naplok/THAYER_API_KOTEG_naplo.md`),
   proveniencia-sorral, a becslés jelölve.
5. **Zárás:** `python eszkozok/teszt_thayer_api_koteg.py`, a `eszkozok/thayer_jelolt/teszt_*.py` (a `teszt_lanc.py` N66-tesztje
   ismert bukás) és `python eszkozok/feladatok.py ellenoriz`; `fuggetlen-ellenor`; draft PR.

## 5. Kész, ha

- K1: `eszkozok/thayer_api_koteg.py` a 3. pont alparancsaival; a #132 eszközei, az `emeles.py`, a `bdb_api_koteg.py` és az
  `api_koteg.py` bájtra változatlan.
- K2: a tesztek zöldek, hálózati hívás nélkül.
- K3: a napló a felméréssel, a teljes lista összesítésével (Strong, `kesz`, `forditando` okonként) és a két `szaraz` becsléssel.
- K4: az `adat/forditasok.tsv` változatlan; a `forditas/thayer_api/` nem jön létre (a száraz futás `--munka`-val a repón kívülre ír).
- K5: a `fuggetlen-ellenor` jelentése `TISZTA`.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.11.02 | Első változat: a Thayer Batch-kötegelője és a teljes Thayer futási listája, valódi beküldés nélkül | DT-F27a (felhasználó, 2026.11.02: „Mehet, külön #158”) |
