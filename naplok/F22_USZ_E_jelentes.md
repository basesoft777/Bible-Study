# F22_USZ_E_jelentes.md — a 22.9 E csomag összesítője (Luk, Ján)

*Proveniencia: scope=Luk, Ján (2 030 Károli-vers) | forras=`naplok/F22_Luk_jelentes.md`, `naplok/F22_Jan_jelentes.md`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_csomagjelentes.py`, `f22_konyvjelentes.py`, `egyesit.py --ellenoriz`, `tokenszint_vershatar.py --lazabb`, `nem_tr_lista.py` (szkriptkimenetek) | ts=2026-11-01. Ág: `claude/f22-evangeliumok-c2ac08`. Módszer: DT-F22i/j/k és a brief 22.9 szerint: Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul, 10 verses kötegek, könyvenként soros küldés.*

## 1. Könyvenként

| könyv | Károli-vers | hívás | költség (USD) | USD/vers | kapuhiba 1. próba | javító körös köteg | ebből egész köteg formátumhiba | `[nem TR]` | ebből párosított | régi arany |
|---|---|---|---|---|---|---|---|---|---|---|
| Luk | 1151 | 127 | 6.2651 | 0.00544 | 40/1151 | 11 | 3 | 709 | 67 | 100.0% (5/5) |
| Ján | 879 | 102 | 4.7832 | 0.00544 | 32/879 | 14 | 2 | 423 | 42 | n.é. (0/0) |
| **össz** | **2030** | **229** | **11.0483** | **0.00544** | **72/2030** | **25** | **5** | **1132** | **109** | |

Végleges kapuhiba: **2/2 030**: a Luk 0/1 151, a Ján 2/879 (Ján 2:8: „többször szereplő magyar szó”; Ján 4:30: a 4:29–38 köteg mindkét próbán érvénytelen JSON; indokolt maradék, a két vers `kezi`, link nélkül). A 25 javító körös kötegből **5 egész köteg formátumhiba** (Luk 3, Ján 2), a többi versenkénti kapuhiba.

## 2. Költség, keret, a mért egységár

- Az E költsége **11.0483 USD** (Luk 6.2651 + Ján 4.7832). A futó összeg 113,0196 USD-ról **124.0678 USD**-ra nőtt; a plafon 141,53 USD, a maradék **17.4622 USD**. A felső becslés (Luk 19,66 USD, Ján 14,93 USD) a plafon alatt maradt.
- Mért egységár az E-ben: **0.00544 USD/vers**.
- Újravetítés az ApCsel-re (1 006 vers): 1006 × 0.00544 = **5.48 USD**, ×1,2 tartalékkal **6.57 USD**; belefér a maradékba (17.46 USD): igen. Az ApCsel egyedi felső becslése (17,17 USD) is a plafon alatt maradt (124,07 + 17,17 = 141,23 < 141,53), ezért egy beküldésben mehetett.

## 3. Tokenszintű vershatár (N-F22e, DT-F22k)

A lazább küszöbű próba (`tokenszint_vershatar.py --lazabb`): **Luk 0 találat; Ján 3 találat** (1:39→1:40, 1:42→1:43, 1:48→1:49: mind a Ján 1:38–1:51 tartományon belül). **Ján 1:38–1:51 (14 vers):** a Károli és a TAGNT vershatára végig egy verssel eltolt; `f22/kezi_versek_Jan.tsv`, az A út szerint `kezi` (link nélkül, `fuggoben`; `naplok/F22_Jan_atnezes.tsv`); a pótlás az N-F22e-é. Az egyező versszám nem bizonyítja az egyező vershatárt. A Jánban így összesen 16 `kezi` vers van (14 + Ján 2:8, 4:30).

## 4. A `[nem TR]` tokenek: 1 132, ebből 109 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a); a Luk után újraépítve: 290 sor, 25 ÚSZ-könyv; az F után 369 sor, 27 ÚSZ-könyv); a sorok a két könyvjelentés 4. szakaszában. A jelölés nem állítja, hogy a Strong a Károli forrásszövegéé (TR); l. a D-jelentés 5. szakaszát (Mt 11:19).

## 5. Mi marad

- Az F csomag (ApCsel); független ellenőrzés: `naplok/ELLENOR_F22_USZ_E.md`; merge csak a felhasználótól.
