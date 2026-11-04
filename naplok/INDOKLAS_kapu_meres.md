# Az olvasói kapu BELSO-találatai előtte és utána (F123.INDOKLAS, 4. lépés)

*Mérve: `python naplok/INDOKLAS_belso_meres.py --rev origin/main` (előtte: a main lapjai) és
`python naplok/INDOKLAS_belso_meres.py` (utána). A mérce mindkét oldalon a mai kapu (`eszkozok/olvasoi_kapu.py`
`ell_belso`, a Strong-szabállyal együtt), a találatok csoportosítás előtt.*

*Proveniencia: `scope=lexikon/*_TUDOMANYOS.md (9 lap) | forras=naplok/INDOKLAS_belso_meres.py (olvasoi_kapu.ell_belso) | ts=2026-11-04`*

## A négy migrált lap (újragenerálva)

| Lap | BELSO előtte | utána | Strong előtte | utána | 1/b. + Minősítés előtte | utána |
|---|---|---|---|---|---|---|
| ALVIL-001 | 60 | 0 | 60 | 0 | 0 | 0 |
| ANTROP-001 | 3 | 0 | 3 | 0 | 0 | 0 |
| ISTENTISZT-001 | 45 | 14 | 33 | 2 | 14 | 0 |
| TEREMT-002 | 10 | 6 | 4 | 0 | 0 | 0 |
| **Összesen** | **118** | **20** | **100** | **2** | **14** | **0** |

A maradék Strong (2) az ISTENTISZT-001 kézi részében áll („Két oltár”, „Mindaz, a ki”): a generátor a kézi részt nem írja
(DT569, a kiejtés-szabály mintája), a forrásban javítandó (kiadott lap: átnézés kell). A többi BELSO a kézi próza
(Értelmezés, Alkalmazás, Módszertan); nem ennek a tételnek a tárgya.

## Az öt nem migrált lap (a main változatán marad)

HAMART-001 72 / 35 / 3, HODIT-001 30 / 0 / 10, KIRALY-001 26 / 4 / 2, MENNY-001 22 / 0 / 2, TEREMT-001 45 / 27 / 2
(BELSO / Strong / 1/b. + Minősítés; előtte = utána).

A main e lapjai korábbi generátor-változások óta nincsenek újragenerálva, ezért az újragenerálás nem csak ennek a
tételnek a változását hozná: a BDB-gerinc szócikkenkénti szerkezete régi címsorokat töröl (CI E5: HAMART-001 29,
HODIT-001 és a többi 8), a KIRALY-001 és a HAMART-001 régi kézi tartalma az E9-et (angol „sense”, 12 sor) buktatja.
Egy korábbi, mind a 9 lapot újrageneráló állapoton mérve a jelöltekből jövő belső jel ezeken is 0 volt (HAMART-001
32 / 8 / 1, KIRALY-001 19 / 3 / 0, HODIT-001 17 / 0 / 2, MENNY-001 16 / 0 / 1, TEREMT-001 13 / 0 / 0). Az
újragenerálásuk a saját migrációs menetükre vár (#123).

A main behozása (#609, HAMART-001 U1: 77 új jelölt-sor, ebből 66 belső jelű indoklással, szétválasztva) után mérve.

## A kiadott lapok (DT569)

`python naplok/INDOKLAS_dt569_igazolas.py`: minden megváltozott sor a régi és az új oldalon is generált részben áll
(a #617 merge-e utáni main-hez képest).

| Lap | Megváltozott sor | Ebből kézi részben |
|---|---|---|
| ISTENTISZT-001 | 239 | 0 |
| ALVIL-001 | 60 | 0 |
| ANTROP-001 | 4 | 0 |
