# F22_API_VAKPROBA_jelentes.md — Károli–Strong párosítás API-n: vakpróba (#77)

*Végrehajtó: sonnet · 2026.10.08 · a brief: `F77_API_VAKPROBA_BRIEF.md`. A számok a `eszkozok/karoli_strong/api_vakproba_osszevet.py --konyv Józs --gondolkodas-becsles` kimenetéből jönnek (alább szó szerint), a költségek a `f22/vakproba/futasnaplo.tsv`-ből.*

## Egyeztetett eltérés

SDK helyett REST: az `api_koteg.py` az `anthropic` Python SDK helyett a Message Batches REST-et hívja a `requests`-szel (`POST /v1/messages/batches`, `GET .../batches/{id}`, `results_url`, `POST /v1/messages/count_tokens`), mert a `pypi.org` a környezet egress-policyje szerint tiltott (a `pip install anthropic` 403-at kapott). A kulcs a `PARDES_API_KEY`-ből jön, csak a fejlécbe kerül; a végső diffen a kulcs-grep (`sk-ant-` és a kulcs egy részlete) üres.

## Mi készült

- `eszkozok/karoli_strong/api_koteg.py` (F77.1): `bekuld` / `allapot` / `begyujt` / `javit` / `--onteszt`. A prompt a `sonnet_koteg.prompt_ir`-ből jön (hash-ellenőrzéssel), `custom_id` = `Jozs-k<köteg>-<effort>-p<próba>` (a `ó` miatt ASCII), az eredmény `custom_id` szerint dolgozódik fel. Modell `claude-sonnet-5-5`, `thinking: adaptive`, `output_config.effort`, `max_tokens` 32 000. Plafon-ellenőrzés beküldés előtt (a felső becslés a `max_tokens`-szel számol: az 1. batch 2,587 USD, a javító 1,750 USD; a kettő együtt a tényleges költséggel a plafon alatt maradt).
- `eszkozok/karoli_strong/api_vakproba_osszevet.py` (F77.3).
- Futtatás (F77.2): 1 batch × 15 kérés (kötegek 1, 6, 25, 45, 53 × low/medium/high), majd 1 javító batch × 10 kérés (a kapun bukott low/medium kötegek). Kimenet: `f22/vakproba/<effort>/Jozs.jsonl`, `batchek.tsv`, `futasnaplo.tsv`, `elteresek_minta.tsv` (20 sor).
- A `prompt_v3` hash-ét minden `prompt_ir` hívás ellenőrizte (a `BEFAGYASZTÁS HIBA` nem jelentkezett); a `f22/valaszok/`, `adat/karoli_strong/`, `f21p/` alatt a diff üres.

## Zajszint-alap

Az 5 köteg (1, 6, 25, 45, 53) `vegrehajto-sonnet` subagentekkel futott, sorban (D15), a Max-keretből, a `prompt_v3`-mal, a `prompt_ir` kimenetéből, vakon (a subagentek az `f22/valaszok/`, `f22/vakproba/`, `adat/karoli_strong/` fájlokat nem olvashatták). A mentés a `sonnet_koteg.mentes` logikájával, scratch `f22`-be ment, onnan `f22/vakproba/subagent/Jozs.jsonl`. A 25. köteg 1. próbája 1 kapuhibás verset adott (Józs 10:30), a 2. próba (javítás) rendben volt; a többi köteg elsőre átment.

## Mérések

## 1. Egyezés a meglévő futással

| változat | vers | link-egyezés (metszet/unió) | ref-link lefedés | betoldas-egyezés | forditatlan-egyezés |
|---|---|---|---|---|---|
| api-low | 45 | 77.96% (1008/1293) | 84.42% | 58.70% | 68.57% |
| api-medium | 49 | 82.21% (1174/1428) | 87.68% | 69.53% | 73.73% |
| api-high | 50 | 94.63% (1322/1397) | 96.78% | 90.75% | 89.19% |
| subagent (zajszint-alap) | 50 | 94.39% (1328/1407) | 97.22% | 91.03% | 90.11% |

*proveniencia: scope=f22/valaszok/sonnet/Jozs.jsonl vs f22/vakproba/<változat>/ | forras=api_vakproba_osszevet.py | ts=2026-10-08T08:41:47+00:00*

## 2. Kapuhiba (versszinten)

| változat | vers | első próbára hibás | végleges kapuhiba |
|---|---|---|---|
| api-low | 50 | 15 | 5 |
| api-medium | 50 | 28 | 1 |
| api-high | 50 | 0 | 0 |
| subagent (zajszint-alap) | 50 | 1 | 0 |

*proveniencia: scope=f22/valaszok/sonnet/Jozs.jsonl vs f22/vakproba/<változat>/ | forras=api_vakproba_osszevet.py | ts=2026-10-08T08:41:47+00:00*

## 3. Token és költség (Batch-áron, f22/vakproba/futasnaplo.tsv)

| effort | hívás | bemenet/hívás (átl.) | kimenet/hívás (átl.) | kimenet max. | gondolkodás becsült (átl./max.) | USD összesen | vers | USD/vers |
|---|---|---|---|---|---|---|---|---|
| low | 10 | 13664 | 1425 | 2215 | -6 / -6 | 0.2079 | 50 | 0.00416 |
| medium | 10 | 13757 | 3634 | 9081 | 1918 / 7020 | 0.3193 | 50 | 0.00639 |
| high | 5 | 12466 | 12234 | 14042 | 10073 / 11774 | 0.3682 | 50 | 0.00736 |

A teljes próba költsége: 0.8953 USD (plafon 3.00 USD).

*proveniencia: scope=f22/vakproba/futasnaplo.tsv | forras=api_koteg.py (Batch-ár: 1.00/5.00 USD/MTok be/ki) | ts=2026-10-08T08:41:47+00:00*

## 4. Kivetítés a hátralevő ÓSZ-versekre

ÓSZ-vers (eredeti-oldal, H-Strong): 23178; kész (f22/valaszok/sonnet): 9035; hátralevő: 14143.

| effort | USD/vers | hátralevő ÓSZ (USD) | hány ilyen mennyiség fér a havi 100 USD-be |
|---|---|---|---|
| low | 0.00416 | 58.80 | 1.7 |
| medium | 0.00639 | 90.31 | 1.1 |
| high | 0.00736 | 104.14 | 1.0 |

*proveniencia: scope=tokenek.betolt_eredeti + f22/valaszok/sonnet/*.jsonl | forras=api_vakproba_osszevet.py | ts=2026-10-08T08:41:47+00:00*

## 5. Eltérő linkek

Összes eltérő link (minden változat): 693; 20-as minta kézi átnézésre: /home/user/Bible-Study/f22/vakproba/elteresek_minta.tsv

*proveniencia: scope=/home/user/Bible-Study/f22/vakproba/elteresek_minta.tsv | forras=api_vakproba_osszevet.py (random.Random(77)) | ts=2026-10-08T08:41:47+00:00*

## Megjegyzések a számokhoz

- Egyezés = a Károli-token → eredeti-token linkek halmaza versenként, a meglévő `Jozs.jsonl` ugyanazon kötegeivel; "metszet/unió" a szimmetrikus szám, a "ref-link lefedés" a meglévő futás linkjeinek hányada. Csak azok a versek számítanak az egyezésbe, ahol mindkét oldalon kapun átment válasz van (low: 45, medium: 49, high: 50 vers az 50-ből).
- A "gondolkodás becsült" oszlop a kimeneti tokenből a válaszszöveg `count_tokens`-szel mért tokenjét vonja le (a batch usage-ben a gondolkodás nem külön mező). A low sora (-6) azt mutatja, hogy a szint gyakorlatilag nem gondolkodik, a becslés hibahatára néhány token.
- Az első batch kapuhibái leggyakrabban: nem teljes lefedés (az "eredeti szavak sem a parok jobb oldalán, sem a forditatlan-ban nem szerepel", 15 eset), érvénytelen JSON (10), üres eredeti-lista a párban (8).
- A bemenet ~13 000 token/hívás (a prompt), prompt-cache nem volt használatban; ez a költség kis része (high: ~17%), a költséget a kimenet adja.
- A kivetítés az ÓSZ-versek számát az eredeti-oldal H-Strongos versei adják (23 178), a "kész" a `f22/valaszok/sonnet/*.jsonl` igehelyei; a Józsué-minta (50 vers, 5 köteg) költségét tekinti reprezentatívnak, ami a hosszabb/nehezebb könyvekre (pl. Zsolt, próféták) eltérhet.

## Döntési kérdés (DT73)

A brief döntési szabály-javaslata: az API-változat akkor elfogadható, ha link-egyezése a meglévő futással nem kisebb, mint a zajszint-alapé mínusz 1 százalékpont, és a végleges kapuhiba 0. Állás (szkriptkimenetből, 1. és 2. tábla): a zajszint-alap link-egyezése 94,39%, az api-high-é 94,63%, vagyis a különbség +0,24 százalékpont, a küszöb (alap − 1 pp = 93,39%) fölött; a végleges kapuhiba 0 a `high` szinten teljesül (low: 5 vers, medium: 1 vers nem). A szabály szerint tehát csak a `high` szint felel meg. A minta kicsi (50 vers, egyetlen könyv).

Opciók:
- (a) a #22 hátralévő könyvei API-n futnak, a `high` szinten (~104 USD a hátralevő ~14 143 versre, vagyis egy havi 100 USD-keretnél kicsit több);
- (b) marad a subagentes futás;
- (c) további mérés: nagyobb minta és/vagy más könyvtípus (pl. próféta, Zsolt), esetleg `medium` + javító kör (~90 USD, de 1 végleges kapuhiba a mintában).

Javaslat: a döntési szabály alapján (a) `high` szinten teljesül, de a költsége (~104 USD) a havi keretet kissé meghaladja, a `medium` pedig a szabályon bukik; érdemes (a)-t egy nagyobb, más típusú mintán megerősíteni (c). A döntés a felhasználóé.
