# F117.6 — próbagenerálás (ALVIL-001, TEREMT-001), E5

*FELADATOK #117 · ág: `claude/f117-versmegf-javitas` · végrehajtó: claude-opus-5-5 · 2026-10-18*

proveniencia: scope=ALVIL-001, TEREMT-001 (TUDOMANYOS) | forras=`python eszkozok/general.py --cel lexikon --id <ID> --kimenet <scratchpad>/f117_proba` (repón kívül; a `lexikon/` és a `generalt_proba/` érintetlen) + TSK_kereszthivatkozasok.tsv + lexikon_general.tsk_index | eszkoz=naplok/F117_proba_kivonat.py, naplok/F117_tsk_index_proba.py | ts=2026-10-18

A próbakimenet a repón kívül maradt; ide csak a kivonat került.

## E5 — a három hely

| Hely | #114 utáni állapot (`naplok/TSK_VERSSZAM_jelentes.md`) | F117 után: TSK-index (minden Votes) | F117 után: próbalexikon (Votes ≥ 15) | Referencia (KJV-kulcs, a táblától független) |
|---|---|---|---|---|
| ALVIL-001 `Jón 2:3` | 0 TSK-sor (a Jón 2:2–10 kivétel miatt) | **26 sor**, mind a KJV `Jón 2:2`-ből | **3 sor**: Zsolt 18:5 (22), Zsolt 18:7 (22), Zsolt 120:1 (21) | KJV Jón 2:2, Votes ≥ 15: Zsolt 18:4, 18:6, 120:1 (KJV-számozás) = Károli 18:5, 18:7, 120:1 |
| TEREMT-001 `Jón 2:6` | 0 TSK-sor | **4 sor**, mind a KJV `Jón 2:5`-ből: Zsolt 69:2 (11), 69:3 (11), Sir 3:54 (7), Zsolt 40:3 (5) | **0 sor**: mind Votes < 15 | KJV Jón 2:5: 4 sor, Votes 5–11; Votes ≥ 15-ös nincs |
| TEREMT-001 `Zsolt 42:8` → Jón-cél | a `Jón 2:3 (Votes: 15)` sor megszűnt | 13 sor a KJV `Zsolt 42:7`-ből, köztük **Jón 2:4 (15)** | **`- TSK: Jón 2:4 (Votes: 15)`** (a blokk egyetlen TSK-sora) | KJV Zsolt 42:7 → KJV Jón 2:3 (15) = Károli Jón 2:4 (`naplok/F117_itelet.tsv`) |

## Értékelés

- **ALVIL-001 `Jón 2:3` — teljesül.** A KJV 2:2 sorai visszatértek, és a célok is Károli-kulcsra váltódtak (Zsolt 18:4 → 18:5).
- **TEREMT-001 `Zsolt 42:8` — teljesül.** A TSK-cél a `Jón 2:4`-en áll.
- **TEREMT-001 `Jón 2:6` — az átváltás szintjén teljesül.** A fogyasztói index a KJV 2:5 mind a 4 sorát a Jón 2:6-ra adja.
  - A próbalexikonban viszont TSK-sor nem jelenik meg, mert mind a 4 sor a generátor Votes ≥ 15 küszöbe alatt van (`lexikon_general.py:1953`).
  - A brief E5-öt („a próbalexikonban TSK-sorokat kap”) ezen a helyen a küszöb miatt nem lehet szó szerint teljesíteni. Ez nem az F117 hibája; jelzem.

## Mellékes megfigyelés (nem vizsgált)

A próbalexikon `#### Jón 2:6` blokkjában két Károli-KH sor áll: `Jer 23:11-32` és `Hós 9:7`. A tartalmuk alapján meglepőek a Jónás 2:6-hoz. A forrásuk a `Karoli_kereszthivatkozasok.tsv` (STEPBible-kulcs), nem a TSK és nem a versmegfeleltető tábla; az F117 nem érinti, és nem vizsgáltam.
