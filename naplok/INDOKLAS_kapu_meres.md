# Az olvasói kapu BELSO-találatai előtte és utána (F123.INDOKLAS, 4. lépés)

*Mérve: `python naplok/INDOKLAS_belso_meres.py --rev origin/main` (előtte: a main 7c6ec946 lapjai) és
`python naplok/INDOKLAS_belso_meres.py` (utána: az újragenerált lapok). A mérce mindkét oldalon a mai kapu
(`eszkozok/olvasoi_kapu.py` `ell_belso`, a Strong-szabállyal együtt), a találatok csoportosítás előtt.*

*Proveniencia: `scope=lexikon/*_TUDOMANYOS.md (9 lap) | forras=naplok/INDOKLAS_belso_meres.py (olvasoi_kapu.ell_belso) | ts=2026-11-04`*

| Lap | BELSO előtte | utána | Strong előtte | utána | 1/b. + Minősítés előtte | utána |
|---|---|---|---|---|---|---|
| ALVIL-001 | 60 | 0 | 60 | 0 | 0 | 0 |
| ANTROP-001 | 3 | 0 | 3 | 0 | 0 | 0 |
| HAMART-001 | 72 | 32 | 35 | 8 | 3 | 1 |
| HODIT-001 | 30 | 17 | 0 | 0 | 10 | 2 |
| ISTENTISZT-001 | 45 | 14 | 33 | 2 | 14 | 0 |
| KIRALY-001 | 26 | 19 | 4 | 3 | 2 | 0 |
| MENNY-001 | 22 | 16 | 0 | 0 | 2 | 1 |
| TEREMT-001 | 45 | 13 | 27 | 0 | 2 | 0 |
| TEREMT-002 | 10 | 6 | 4 | 0 | 0 | 0 |
| **Összesen** | **313** | **117** | **166** | **13** | **33** | **4** |

## A maradék

- **Strong (13):** mind kézi részben (HAMART-001 8, KIRALY-001 3, ISTENTISZT-001 2: a „Két oltár” és a „Mindaz, a ki”
  bekezdés). A generátor a kézi részt nem írja (DT569, a kiejtés-szabály mintája); a forrásban javítandó.
- **1/b. + Minősítés (4):** egyik sem a `jeloltek.tsv`-ből jön. A HAMART-001 a negatív kritérium sora
  („a gerinc valamelyik elemén”, `motivumok.tsv` `negativ_kriterium`); a HODIT-001 2 és a MENNY-001 1 a régi lapok kézi
  „Minősítés *(kézi)*” résének fájlnevei.
- **A többi BELSO (100):** a kézi próza (Értelmezés, Alkalmazás, Módszertan) és a régi lapok kézi táblái; nem ennek a
  tételnek a tárgya.

## A kiadott lapok (DT569)

`python naplok/INDOKLAS_dt569_igazolas.py`: minden megváltozott sor a régi és az új oldalon is generált részben áll.

| Lap | Megváltozott sor | Ebből kézi részben |
|---|---|---|
| ISTENTISZT-001 | 257 | 0 |
| ALVIL-001 | 74 | 0 |
| ANTROP-001 | 15 | 0 |
