# F34 M2–M4 — futásnapló és proveniencia

*Ág: `claude/bdb-psi` · eszköz: `eszkozok/bdb_psi_javit.py` · dátum: 2026.10.01 · dontés: DT-F34 (felhasználó, 2026.10.01)*

## Proveniencia

`scope=manual | forras=eszkozok/bdb_psi_javit.py + konkordancia/TAHOT_kivonat.tsv + naplok/F34_M0_lista.tsv | ts=2026-10-01`
A javítás kulcsa: szócikk-id + régi + új token (`naplok/F34_M2_csere.tsv`), nem sorszám.

## 0. pont: parser-javítás nem elérhető

A nyers `DictBDB.json` nincs a repóban (a `konkordancia/_convert_bdb.py` a `%TEMP%`-ből olvasna); a `konkordancia/lexikonok_nyers/BDB.lexicon` más szerkezetű (18 642 tétel, más jelölés), nem ennek a datasetnek a nyers forrása. Ezért az 1–4. pont szerint mezőkulcsos csere a kész TSV-n.

## Szabály és eredmény

- A (fejezet>66 / „Psalm” jelző): javul, ha a szócikk Strong-száma a TAHOT szerint előfordul a Zsolt c:v ±1 versben.
- B/R: javul, ha Zsolt c:v ±1 találat van, és a TAHOT szerint más könyvben ugyanott (c:v ±1) nincs.

| | Javítva (hely) | Maradék (hely) |
|---|---|---|
| A | 85 | 19 |
| B | 57 | 144 |
| R | 2 (köztük H7585 `Ezek 16:10` → `Psa 16:10`) | 15 |
| Összesen | **144 hely, 48 szócikk** | **178 hely, 104 szócikk** |

A maradék oka: 167 kulcsnál a TAHOT-kivonatban nincs Zsolt c:v ±1 találat (a kivonat nem teljes: Zsolt 88/89/140/142 hiányzik, és a Strong-szám nem mindig szerepel az idézett versben), 7-nél más könyvben is van találat (nem egyértelmű), 1 összeolvadt alak (`2Sam 132:1132`). Listája: `naplok/F34_M2_maradek.tsv` — **kézi nézet, nem javítva**. `Dan 22:14` forráshiba, nem hatókör.

## Diff-kapu

Forrás: 144 csere, 48 sor változott; minden változott sorban a `Könyv c:v` helyhivatkozások `<R>`-re cserélve a két szöveg bájtazonos (más eltérés nincs). Sorszám változatlan, a sorvégek megmaradtak. Új SHA-256: `e9ee0b724dcb86f40370734b142d17863fe204c764966911f72b042e0ddf666d`.

## M3 — adat/forditasok.tsv

Csak a helyhivatkozás tokenje változott (a fordítás szövege egyébként bájtazonos; kapu a szkriptben), a `forras_hash` az új forrásból újraszámolva (SHA-1):

| Fájlsor | Szócikk | Állapot | Csere |
|---|---|---|---|
| 78 | H8415 | kezi | Ézs 106:9 → Zsolt 106:9; Ézs 71:20 → Zsolt 71:20 |
| 81 | H7585 | kezi | Ez 16:10 → Zsolt 16:10; Ez 49:16 → Zsolt 49:16 (Ez 73:23, 73:25 marad: a TAHOT nem igazolja) |
| 89 | H0430 | opus | Jób 97:7 → Zsolt 97:7 |

A 84. és 85. sor forrása nem változott (nincs javítható találat), ezért érintetlen. `eszkozok/ellenoriz.py`: 13. szabály (forras_hash) **RENDBEN**, kilépési kód 0.

## M4 — kapu

`eszkozok/teszt_forditas_kapuk.py`: 20 teszt OK (3 új: javított hely nem jelez; hibás ψ-feloldás jelez; a 78. és 89. sor RENDBEN). A 13. kapu a 78. és 89. soron **0**; a 81., 84., 85. soron a jelzés a **maradék miatt** marad (Ez 73; Péld 57–59, 75 és `2Kir 36:10`; Dán 22) — ez a ⛔ kézi nézet.
