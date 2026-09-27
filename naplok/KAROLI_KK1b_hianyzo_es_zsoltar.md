# KAROLI_KK1b_hianyzo_es_zsoltar.md — hiányzó könyvek és a Zsoltárok

*KK1b-2 — KAROLI_KULCS_BRIEF.md v1.1 §3. Szkriptek:
`naplok/KAROLI_KK1b_fejezetosztaly_general.py` (teljes 929-fejezetes
osztálytábla), `naplok/KAROLI_KK1b_zsoltar_ok_general.py` (Zsoltár
ok-besorolás). Kimenet: `naplok/KAROLI_KK1b_fejezetosztaly.tsv` (929
fejezet, 39 könyv), `naplok/KAROLI_KK1b_ok_besorolas.tsv`.*

## (a) Ezsdrás, Nehémiás, Eszter

A `verse_pairs.jsonl`-ben a `2-esdras` grk_book **mind Ezsdrást, mind
Nehémiást** fedi (`mt_book` "ezra" ill. "nehemiah"), az `esther-greek`
pedig Esztert (néhány `mt_book=None` sorral — ezek a görög Eszter-toldalékok,
amiknek nincs héber megfelelője, `nincs_mt_parositas` marad). A három könyv
mind a 33 fejezete a KK1 módszerével osztályozva:

| Könyv | Fejezet | KJV | MT | KEZI | EGYIK_SEM |
|---|---|---|---|---|---|
| Ezsdrás | 10 | 10 | 0 | 0 | 0 |
| Nehémiás | 13 | 13 | 0 | 0 | 0 |
| Eszter | 10 | 10 | 0 | 0 | 0 |
| **Összesen** | **33** | **33** | 0 | 0 | 0 |

Mind a 33 fejezet tisztán `KJV`-osztályú (Károli = KJV versszám minden
fejezetben) — ez a három könyv nem hordoz numerálási problémát.

## (b) Zsoltárok

150 fejezet, a KK1 módszerével osztályozva (egy új, próbaként bevezetett
`ZSOLT_CIM_ELTOLAS` osztály nem lépett életbe — l. lent):

| Osztály | Fejezet |
|---|---|
| KJV | 88 |
| MT | 62 |
| ZSOLT_CIM_ELTOLAS (próba-osztály, üres) | 0 |
| EGYIK_SEM | 0 |

**Fontos módszertani megfigyelés:** a jelenlegi `resolve_karoli` külön,
kézzel írt "Zsoltár cím-eltolás" logikát tartalmaz (`d∈{1,2}` speciális
eset). A KK1-módszerű egyszerű `MT`-osztályozás (Károli max = TAHOT max)
**önmagában lefedi a 62 cím-eltolásos zsoltárfejezetet** — vagyis egy
általános, MT-tudatos `resolve_karoli` (G4) a jelenlegi speciális
Zsoltár-cím-ágat feleslegessé tenné, mert a Zsoltárok többsége egyszerűen
"MT-osztályú fejezet", ugyanúgy, mint Jónás vagy Ézsaiás 63 — nem kell
külön eset.

**Zsoltárok szósor-szinten** (`psalms-lxx.tsv`): kitöltött 20 071 ·
`zsolt_felirat_eltolas` 14 065 · `szamozas_elteres` 699 · `nincs_mt_parositas` 116.

**Zsoltárok `szamozas_elteres` — egyedi LXX-vers szinten: 67** (a szósorok
699-ből, sok szó/vers). Ok-besorolás:

| Ok | Versek | Arány |
|---|---|---|
| H2 (Károli MT-számozást követ, importer nem ismeri) | 48 | 71,6% |
| H5 (valódi vers-tartalmi eltérés) | 19 | 28,4% |
| H1 (KEZI) | 0 | — |
| H3 (EGYIK_SEM) | 0 | — |

A Zsoltárokban nincs `KEZI_ELTOLASOK`-függvény és nincs `EGYIK_SEM`
fejezet — a 67 érintett vers mindegyike H2 vagy H5.

## Teljes 929-fejezetes osztálytábla (a 39 könyv összesítve)

| Osztály | Fejezet | Arány |
|---|---|---|
| KJV | 819 | 88,2% |
| MT | 84 | 9,0% |
| KEZI | 13 | 1,4% |
| EGYIK_SEM | 13 | 1,4% |
| **Összesen** | **929** | **100%** |

(A KK1-hez képest +33 KJV-fejezet Ezsdrás/Nehémiás/Eszterből.)

## Mért hatás a Zsoltárokkal együtt

| | Nem-Zsoltár (KK1) | Zsoltár (KK1b) | Összesen |
|---|---|---|---|
| Mért érintett vers | 985 | 67 | **1 052** |
| Megoldódna (H1+H2) | 666 | 48 | **714 (67,9%)** |
| Nem oldódik meg (H3+H5) | 319 | 19 | **338 (32,1%)** |

**Megjegyzés a `0.2`-höz képesti eltérésről:** a brief §0.2 1 015 érintett
verset mondott ki (chat-alapú mérés); a jelen menet szkriptes mérése
**1 052-t** ad (985+67). A 37 vers eltérés valószínűleg a könyv-szintű
lefedettségi különbségből ered (pl. a `judges`/`judges-vaticanus-b` kettős
szöveg-változat egyikének esetleges ki/bemaradása a számlálásban) — **ez
egy mérési eltérés, nem extrapoláció** (G10): mindkét szám tényleges
szkript-futásból származik, csak eltérő könyv-halmazon. A pontos ok
feltárása a 2. menet előtt tisztázandó.
