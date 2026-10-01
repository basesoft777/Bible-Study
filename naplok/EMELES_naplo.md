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
felvételének kérdése a `DONTESEK.md` E4a-tételébe került (az E4a első adagját nem
érinti, kivéve a „legrövidebb Thayer-szócikk” kiválasztását — l. az E4a szakaszt).
