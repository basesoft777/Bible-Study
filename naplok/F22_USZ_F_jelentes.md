# F22_USZ_F_jelentes.md — a 22.9 F csomag összesítője (ApCsel) és az evangéliumok + ApCsel keretének zárása

*Proveniencia: scope=ApCsel (1 006 Károli-vers); a keretösszesítés: Mt, Mk, Luk, Ján, ApCsel (4 785 vers) | forras=`naplok/F22_ApCsel_jelentes.md`, `naplok/F22_USZ_D_jelentes.md`, `naplok/F22_USZ_E_jelentes.md`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_csomagjelentes.py`, `f22_konyvjelentes.py`, `egyesit.py --ellenoriz`, `tokenszint_vershatar.py --lazabb`, `nem_tr_lista.py` (szkriptkimenetek) | ts=2026-11-01. Ág: `claude/f22-evangeliumok-c2ac08`. Módszer: DT434/j/k és a brief 22.9 szerint (l. a D, E jelentés).*

## 1. Az ApCsel

| könyv | Károli-vers | hívás | költség (USD) | USD/vers | kapuhiba 1. próba | javító körös köteg | ebből egész köteg formátumhiba | `[nem TR]` | ebből párosított | régi arany |
|---|---|---|---|---|---|---|---|---|---|---|
| ApCsel | 1006 | 118 | 6.0141 | 0.00598 | 27/1006 | 17 | 1 | 634 | 37 | 60.0% (3/5) |
| **össz** | **1006** | **118** | **6.0141** | **0.00598** | **27/1006** | **17** | **1** | **634** | **37** | |

Végleges kapuhiba: 0/1 006. A 17 javító körös kötegből 1 egész köteg formátumhiba (k025), a többi versenkénti kapuhiba. A plafon-őr az ApCsel egyedi felső becslését (17,17 USD) átengedte (124,07 + 17,17 = 141,23 < 141,53), részletekben küldés nem kellett.

## 2. Tokenszintű vershatár (N-F22e, DT436)

A lazább küszöbű próba: **ApCsel 2 találat** (13:32→13:33, 24:2→24:3), mindkettő szövegen igazolt; `f22/kezi_versek_ApCsel.tsv`: ApCsel 13:32, 13:33, 24:2, 24:3 `kezi` (link nélkül, `fuggoben`; `naplok/F22_ApCsel_atnezes.tsv`); a pótlás az N-F22e-é.

## 3. A teljes keret (DT434: 38 USD)

| csomag | könyvek | vers | költség (USD) | USD/vers | végleges kapuhiba |
|---|---|---|---|---|---|
| D | Mt, Mk | 1 749 | 9.4887 | 0.00543 | 0/1 749 |
| E | Luk, Ján | 2 030 | 11.0483 | 0.00544 | 2/2 030 (Ján 2:8, 4:30) |
| F | ApCsel | 1 006 | 6.0141 | 0.00598 | 0/1 006 |
| **össz** | | **4 785** | **26.5511** | **0.00555** | **2/4 785** |

- A futó összeg 103,5308 USD-ról **130.0820 USD**-ra nőtt; a plafon (`api_koteg.PLAFON_USD`) 141,53 USD, a maradék **11.4480 USD**. A keret 38 USD-jából **26.5511 USD** fogyott el (a vetítés ×1,2 tartalékkal 30,1 USD volt).
- A `kezi` versek: Ján 1:38–51 (14) + Ján 2:8, 4:30 + ApCsel 13:32–33, 24:2–3 (4) = 20 vers; mind a tokenszintű vershatár (N-F22e) vagy a végleges kapuhiba miatt, link nélkül.
- Mért egységár a 22.8, az A, a B, a 2Kor, a C (3 166 vers, 0,005495 USD/vers, l. a C-jelentést) és a D + E + F (4 785 vers, 26.5511 USD) együtt: **0.005527 USD/vers** (7 951 vers).

## 4. A `[nem TR]` tokenek: 2 887, ebből 250 párosított

Mt 458 / 47, Mk 663 / 57, Luk 709 / 67, Ján 423 / 42, ApCsel 634 / 37 (a két szám: `[nem TR]` token / ebből párosított; a könyvjelentések 4. szakasza). A jelölőtábla (`adat/karoli_strong/nem_tr_parositott.tsv`) az F után 369 sor, 27 ÚSZ-könyv.

## 5. Az ellenőri jelentés nyomán (ELLENOR_F22_USZ_F)

- A keret 26.5511 USD (a futásnaplóból: 130.081958 − 103.530839); a korábbi 26,5512 két kerekített futó összeg különbsége volt.
- Az N-F22e pótlandó köre 30 vers (10 + 20), nem 28.
- P4: az ApCsel 634 `[nem TR]` tokenjéből 596 `forditatlan`, 37 párosított, 1 `fuggoben` (ApCsel 24:2 er 15, διορθωμάτων, G1357, a `kezi` vers tokenje).
- ApCsel 2:27, 2:31 (Hádész, G0086 `forditatlan`): l. az ApCsel-jelentés végén.

## 6. Mi marad

- N-F22e: az általános tokenszintű vershatár-mechanizmus (a `kezi` versek pótlása: a meglévő 10 vers (2Kor 8:13–14, 2:12–13, 5:14–15, Zsid 1:1–2, Fil 3:13–14) + a 20 vers = 30 vers).
- Független ellenőrzés: `naplok/ELLENOR_F22_USZ_F.md`; merge csak a felhasználótól.
