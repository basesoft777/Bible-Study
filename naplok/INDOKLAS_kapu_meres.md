# Az olvasói kapu BELSO-találatai előtte és utána (F123.INDOKLAS, 4. lépés)

*Mérve: `python naplok/INDOKLAS_belso_meres.py --rev origin/main` (előtte: a main lapjai) és
`python naplok/INDOKLAS_belso_meres.py` (utána: az újragenerált lapok). A mérce mindkét oldalon a mai kapu
(`eszkozok/olvasoi_kapu.py` `ell_belso`, a Strong-szabállyal együtt), a találatok csoportosítás előtt.*

*Proveniencia: `scope=lexikon/*_TUDOMANYOS.md (9 lap) | forras=naplok/INDOKLAS_belso_meres.py (olvasoi_kapu.ell_belso) | ts=2026-11-04`*

| Lap | BELSO előtte | utána | Strong előtte | utána | 1/b. + Minősítés előtte | utána |
|---|---|---|---|---|---|---|
| ALVIL-001 | 60 | 0 | 60 | 0 | 0 | 0 |
| ANTROP-001 | 3 | 0 | 3 | 0 | 0 | 0 |
| HAMART-001 ⚠ | 72 | 72 | 35 | 35 | 3 | 3 |
| HODIT-001 | 30 | 17 | 0 | 0 | 10 | 2 |
| ISTENTISZT-001 | 45 | 14 | 33 | 2 | 14 | 0 |
| KIRALY-001 ⚠ | 26 | 26 | 4 | 4 | 2 | 2 |
| MENNY-001 | 22 | 16 | 0 | 0 | 2 | 1 |
| TEREMT-001 | 45 | 13 | 27 | 0 | 2 | 0 |
| TEREMT-002 | 10 | 6 | 4 | 0 | 0 | 0 |
| **Összesen** | **313** | **164** | **166** | **41** | **33** | **8** |

⚠ **A HAMART-001 és a KIRALY-001 lapja ebben a PR-ben nem újragenerált** (a main változata maradt). A main e két lapja
korábbi generátor-változások óta sincs újragenerálva; az újragenerálás a régi kézi tartalom miatt a CI-t buktatja:
a KIRALY-001-en az E9 (angol „sense”, 11 sor, a régi kézi táblákban és a jelölt-indoklásokban), a HAMART-001-en az
E5 (a BDB-gerinc szócikkenkénti szerkezete 29 régi címsort töröl) és az E9 (1 sor). Az újragenerált változatukon
mérve (a PR egy korábbi állapotán): HAMART-001 32 / 8 / 1, KIRALY-001 19 / 3 / 0 — a jelöltekből jövő belső jel
ott is 0. Az újragenerálás a két lap saját menetéé (HAMART-001: a #123 U-lépései; KIRALY-001: migráció).

A main behozása (#609, HAMART-001 U1: 77 új jelölt-sor, ebből 66 belső jelű indoklással, szétválasztva) után mérve.

## A maradék (az újragenerált 7 lapon)

- **Strong (2):** ISTENTISZT-001, kézi részben („Két oltár”, „Mindaz, a ki”). A generátor a kézi részt nem írja
  (DT569, a kiejtés-szabály mintája); a forrásban javítandó (kiadott lap: átnézés kell).
- **1/b. + Minősítés (3):** egyik sem a `jeloltek.tsv`-ből jön: a HODIT-001 2 és a MENNY-001 1 a régi lapok kézi
  „Minősítés *(kézi)*” résének fájlnevei.
- **A többi BELSO:** a kézi próza (Értelmezés, Alkalmazás, Módszertan) és a régi lapok kézi táblái; nem ennek a
  tételnek a tárgya.

## A kiadott lapok (DT569)

`python naplok/INDOKLAS_dt569_igazolas.py`: minden megváltozott sor a régi és az új oldalon is generált részben áll
(a ts-sorokkal együtt).

| Lap | Megváltozott sor | Ebből kézi részben |
|---|---|---|
| ISTENTISZT-001 | 257 | 0 |
| ALVIL-001 | 101 | 0 |
| ANTROP-001 | 64 | 0 |
