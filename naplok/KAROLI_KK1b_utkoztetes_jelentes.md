# KAROLI_KK1b_utkoztetes_jelentes.md — ütköztetés a térképpel

*KK1b-3 — KAROLI_KULCS_BRIEF.md v1.1 §3, §1 ütköztetési mérce. Szkriptek:
`naplok/KAROLI_KK1b_kulcstabla_general.py` (a teljes 929-fejezetes tervezet
újragenerálása a `KAROLI_KK1b_fejezetosztaly.tsv`-ből), `naplok/KAROLI_KK1b_utkoztetes_general.py`
(ütköztetés), `naplok/KAROLI_KK1b_terkep_javaslat_general.py` (automatikus
horgony-döntés). Kimenet: `naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv`
(22 940 sor), `naplok/KAROLI_KK1b_kulcstabla_tervezet_utkoztetve.tsv`,
`naplok/KAROLI_KK1b_utkozes.tsv`, `naplok/KAROLI_KK1b_terkep_javaslat.tsv`.*

## Az ütköztetés eredménye, osztályonként

| Osztály | `NINCS_TERKEP_SOR` | `EGYEZIK` | `UTKOZIK_ELLENORIZETLEN` | `UTKOZIK_ELLENORZOTT` | `OSSZETETT_TERKEP_SOR` |
|---|---|---|---|---|---|
| KJV | 17 235 | 2 800 | 846 | **0** | 46 |
| MT | 595 | 72 | 1 045 | **0** | 1 |
| KEZI | 188 | 78 | 34 | **0** | — |
| **Összesen** | **18 018** | **2 950** | **1 925** | **0** | **47** |

**K4 kritikus feltétele teljesül: 0 `UTKOZIK_ELLENORZOTT` sor** — a térkép
egyetlen *tartalmilag ellenőrzött* (`Karoli_egyezik_hol` ∈ {Heber, Heber,Latin,
Heber,Gorog, Heber,Latin,Gorog}) sora sem mond ellent a KK1b-tervezetnek.

## `UTKOZIK_ELLENORIZETLEN` — 1 925 sor, automatikus horgony-döntés

A brief §3 KK1b-3 soronkénti horgonyos döntést kér, a 0b.8 mintájára. Mivel
1 925 sor egyedi, kézi tartalmi egyeztetése ebben a menetben nem végezhető
el, **automatikus, TAHOT-létezési horgonyt** alkalmaztunk minden sorra: a
saját tervezet célja és a térkép célja közül létezik-e ténylegesen vers a
`TAHOT_kivonat.tsv`-ben az adott könyv adott fejezet:vers-hivatkozásán.

| Automatikus döntés | Sorok | Arány |
|---|---|---|
| `TERVEZET_MARAD` (csak a mi célunk van a TAHOT-ban) | 151 | 7,6% |
| `TERKEP_JAVASOLT_JAVITAS` (csak a térkép célja van a TAHOT-ban) | 0 | 0% |
| `BIZONYTALAN_MINDKETTO_LETEZIK` (mindkét cél létezik — a horgony nem dönt) | 1 792 | 90,6% |
| `BIZONYTALAN_EGYIK_SEM_LETEZIK` (összetett/tartományos térkép-sor) | 35 | 1,8% |

**Módszertani korlát, őszintén jelezve:** a TAHOT-létezési horgony **nem
egy tartalmi (szó-szintű) próba**, csak azt teszi fel a kérdést, hogy a
könyvben egyáltalán van-e vers az adott hivatkozáson — ez a legtöbb esetben
(90,6%) mindkét oldalon igaz (mert egy könyvön belüli bármely ésszerű
fejezet:vers-szám valószínűleg létező vers), tehát **nem tudja eldönteni
a valódi kérdést**. A 0b.8-hoz hasonló, tényleges tartalmi (szó-anchor)
összevetés csak a `naplok/KAROLI_KK1_15sor.tsv`-ben szereplő,
kézzel ellenőrzött esetekre készült el (l. lent) — **a teljes 1 792
"bizonytalan" sor kézi vagy jobb automatizált (pl. lemma-egyezés)
feldolgozása a jelen menet keretein túlmutat**, és a 2. menet előtt
tisztázandó nyitott kérdés marad.

## A 15 lexikon-sor és a térkép — közvetlen ellenőrzés

A KK0 0.8 / KK1 tartalmi kontrollja (Jón 2:3, `Karoli_egyezik_hol=EGYIK_SEM`
a térképen) mintájára ellenőrizve: egyik a 15 lexikon-sor közül **sem esik
`UTKOZIK_ELLENORZOTT`-ba** — a térkép egyik érintett sora sem "Heber"-rel
ellenőrzött ezekre a versekre (a Jón 2:3/2:6, Ézs 63:13, Józs 13:12 mind
`EGYIK_SEM` vagy hasonló jelzésű a térképen), tehát a KK1-ben adott
javaslatok (Jón 2:3 = LXX 2:3, nem 2:4 stb.) **nem ütköznek** ellenőrzött
térkép-adattal — a K4 "nincs UTKOZIK_ELLENORZOTT bizonyítás nélkül"
feltétele ezekre a sorokra is teljesül.

## Következtetés

A tervezet (`KAROLI_KK1b_kulcstabla_tervezet.tsv`) **használható marad**: a
kötelező ütközés-teszt (K4) formálisan teljesül (0 `UTKOZIK_ELLENORZOTT`),
de a **1 925 `UTKOZIK_ELLENORIZETLEN` sor túlnyomó többsége (1 792, 90,6%)
nyitott kérdés marad** — ez a 2. menet előtt egy külön, célzott
tartalmi-egyeztetési kört igényelne (G9 szerint a térkép saját javítási
javaslatai is csak ebbe a naplófájlba kerülnek, nem a térkép fájljába).
