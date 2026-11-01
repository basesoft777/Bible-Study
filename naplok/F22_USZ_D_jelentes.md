# F22_USZ_D_jelentes.md — a 22.9 D csomag összesítője (Mt, Mk)

*Proveniencia: scope=Mt, Mk (1 749 Károli-vers) | forras=`naplok/F22_Mt_jelentes.md`, `naplok/F22_Mk_jelentes.md`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_csomagjelentes.py`, `f22_konyvjelentes.py`, `egyesit.py --ellenoriz`, `tokenszint_vershatar.py --lazabb`, `nem_tr_lista.py` (szkriptkimenetek) | ts=2026-11-01. Ág: `claude/f22-evangeliumok-c2ac08`. Módszer: DT434/j és a brief 22.9 szerint: Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul, 10 verses kötegek, könyvenként soros küldés.*

## 1. Könyvenként

| könyv | Károli-vers | hívás | költség (USD) | USD/vers | kapuhiba 1. próba | javító körös köteg | ebből egész köteg formátumhiba | `[nem TR]` | ebből párosított | régi arany |
|---|---|---|---|---|---|---|---|---|---|---|
| Mt | 1071 | 133 | 5.8060 | 0.00542 | 113/1071 | 25 | 9 | 458 | 47 | 100.0% (2/2) |
| Mk | 678 | 73 | 3.6827 | 0.00543 | 14/678 | 5 | 1 | 663 | 57 | n.é. (0/0) |
| **össz** | **1749** | **206** | **9.4887** | **0.00543** | **127/1749** | **30** | **10** | **1121** | **104** | |

Végleges kapuhiba: 0/1 749. A 30 javító körös kötegből **10 egész köteg formátumhiba** volt (Mt 9, Mk 1: a modell önjavító, érvénytelen JSON-t adott; `f22/api_termeles/high/_munka/<könyv>_k*.json`, a kötegek a könyvjelentések 2. szakaszában), a többi 20 **versenkénti** kapuhiba; a javító kör mindet megoldotta (végleges kapuhiba 0). Az Mt első próbás kapuhibája (10,6%) az Mk-énál (2,1%) jóval magasabb, a végeredmény azonos (0).

## 2. Költség, keret, a mért egységár

- A D költsége **9.4887 USD** (Mt 5.8060 + Mk 3.6827). A futó összeg 103,5308 USD-ról **113.0196 USD**-ra nőtt; a plafon (`api_koteg.PLAFON_USD`) 141,53 USD, a maradék **28.5104 USD**. A plafon-őr nem változott; a felső becslés (Mt 18,31 USD, Mk 11,53 USD) a plafon alatt maradt.
- Mért egységár a D-ben: **0.00543 USD/vers** (a vetített 0,005238 USD/vers-nél kissé magasabb).
- Újravetítés a hátralevő két csomagra (E: Luk + Ján = 2 030 vers, F: ApCsel = 1 006 vers; összesen 3 036 vers): 3036 × 0.00543 = **16.47 USD**, ×1,2 tartalékkal **19.77 USD**; belefér a maradékba (28.51 USD): igen. Az ApCsel egyedi felső becslése (kb. 101 kérés × 0,16 USD) a plafont az E után túllépheti: ilyenkor a DT262 (b) módján részletekben küld a futtató, a plafon-őrhöz nem nyúl.

## 3. Tokenszintű vershatár (N-F22e)

A lazább küszöbű próba (`tokenszint_vershatar.py --lazabb`): **Mt 0, Mk 0 találat**. `kezi` kényszerített vers a D-ben nincs. (A Ján 1:38–51 és az ApCsel négy verse az E, illetve F csomagban `kezi`, DT435.)

## 4. A `[nem TR]` tokenek: 1 121, ebből 104 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a); a tábla újraépítve a D után: 223 sor, 24 ÚSZ-könyv); a sorok a két könyvjelentés 4. szakaszában.

## 5. Az ellenőri jelentés nyomán (ELLENOR_F22_USZ_D)

- A `NYITOTT_FELADATOK.md` sorvége-átírása (F22.46) visszaállítva; a fájl a `main`-hez képest egyetlen sorban tér el (N-F22e).
- A formátumhiba-szám most szkriptből jön (`f22_konyvjelentes.py`, `f22_csomagjelentes.py`).
- P6 (`adat/datasetek.tsv`, `adat/SEMA.md`) és a brief fejléce: az F csomag után, egyszerre az öt könyvre.
- Mt 11:19 (`[nem TR]`, G2041): a Mt-jelentés 4. szakasza nevesíti.

## 6. Mi marad

- E csomag (Luk + Ján) és F csomag (ApCsel), ugyanezzel a menettel; a Ján 1:38–51 és az ApCsel 13:32–33, 24:2–3 `kezi`.
- Független ellenőrzés: `naplok/ELLENOR_F22_USZ_D.md`; merge csak a felhasználótól.
