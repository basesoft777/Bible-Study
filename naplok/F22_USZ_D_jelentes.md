# F22_USZ_D_jelentes.md — a 22.9 D csomag összesítője (Mt, Mk)

*Proveniencia: scope=Mt, Mk (1 749 Károli-vers) | forras=`naplok/F22_Mt_jelentes.md`, `naplok/F22_Mk_jelentes.md`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_csomagjelentes.py`, `f22_konyvjelentes.py`, `egyesit.py --ellenoriz`, `tokenszint_vershatar.py --lazabb`, `nem_tr_lista.py` (szkriptkimenetek) | ts=2026-11-01. Ág: `claude/f22-evangeliumok-c2ac08`. Módszer: DT-F22i/j és a brief 22.9 szerint: Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul, 10 verses kötegek, könyvenként soros küldés.*

## 1. Könyvenként

| könyv | Károli-vers | hívás | költség (USD) | USD/vers | kapuhiba 1. próba | javító körös köteg | `[nem TR]` | ebből párosított | régi arany |
|---|---|---|---|---|---|---|---|---|---|
| Mt | 1071 | 133 | 5.8060 | 0.00542 | 113/1071 | 25 | 458 | 47 | 100.0% (2/2) |
| Mk | 678 | 73 | 3.6827 | 0.00543 | 14/678 | 5 | 663 | 57 | n.é. (0/0) |
| **össz** | **1749** | **206** | **9.4887** | **0.00543** | **127/1749** | **30** | **1121** | **104** | |

Végleges kapuhiba: 0/1 749. A kapun első próbára bukott versek **versenkénti** kapuhibák voltak (a javító kör mindet megoldotta); egész köteg formátumhiba nem fordult elő. Az Mt első próbás kapuhibája (10,6%) az Mk-énál (2,1%) jóval magasabb, a végeredmény azonos (0).

## 2. Költség, keret, a mért egységár

- A D költsége **9.4887 USD** (Mt 5.8060 + Mk 3.6827). A futó összeg 103,5308 USD-ról **113.0196 USD**-ra nőtt; a plafon (`api_koteg.PLAFON_USD`) 141,53 USD, a maradék **28.5104 USD**. A plafon-őr nem változott; a felső becslés (Mt 18,31 USD, Mk 11,53 USD) a plafon alatt maradt.
- Mért egységár a D-ben: **0.00543 USD/vers** (a vetített 0,005238 USD/vers-nél kissé magasabb).
- Újravetítés a hátralevő két csomagra (E: Luk + Ján = 2 030 vers, F: ApCsel = 1 006 vers; összesen 3 036 vers): 3036 × 0.00543 = **16.47 USD**, ×1,2 tartalékkal **19.77 USD**; belefér a maradékba (28.51 USD): igen. Az ApCsel egyedi felső becslése (kb. 101 kérés × 0,16 USD) a plafont az E után túllépheti: ilyenkor a DT262 (b) módján részletekben küld a futtató, a plafon-őrhöz nem nyúl.

## 3. Tokenszintű vershatár (N-F22e)

A lazább küszöbű próba (`tokenszint_vershatar.py --lazabb`): **Mt 0, Mk 0 találat**. `kezi` kényszerített vers a D-ben nincs. (A Ján 1:38–51 és az ApCsel négy verse az E, illetve F csomagban `kezi`, DT-F22j.)

## 4. A `[nem TR]` tokenek: 1 121, ebből 104 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a); a tábla újraépítve: 223 sor, 24 ÚSZ-könyv); a sorok a két könyvjelentés 4. szakaszában.

## 5. Mi marad

- E csomag (Luk + Ján) és F csomag (ApCsel), ugyanezzel a menettel; a Ján 1:38–51 és az ApCsel 13:32–33, 24:2–3 `kezi`.
- Független ellenőrzés: `naplok/ELLENOR_F22_USZ_D.md`; merge csak a felhasználótól.
