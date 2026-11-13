# F218a — folytatási fájl

*Kézi munkanapló (a brief 9. pontja szerint minden commitban frissül). Ebből indul a következő session; a régi generátorból visszafejtett mondatszabályok is itt állnak.*

Ág: `claude/f218-generator-uj-a` · Brief: `F218_GENERATOR_UJ_A_BRIEF.md` · Alap: main `37f087cc`.

## Állás

| Tétel | Állapot | Megjegyzés |
|---|---|---|
| F218.0 | kész | modell-ellenőrzés, függések, keretmérés |
| F218.1 | fut (sonnet, háttérben) | referencia, alapmérés, szimbólumtérkép; a leltár `kovetelmeny` oszlopa a heti keret nullázása utánra halasztva |
| F218.2 (T) | fut | típusok és szerződések |
| F218.3 | nem indult | tesztváz |
| F218.4 (S1) | nem indult | 2. Előfordulások + 2.1 |
| F218.5 (S2) | nem indult | 1. Döntési út + KIZARASOK |
| F218.6–F218.13 | nem indult | |

## Következő lépés

F218.2: `eszkozok/lapgen/szoveg.py` (a `Lathato` típus három konstruktorral, `Proveniencia`, `Nev`, `Igehely`, `Kulcs`), a bemeneti réteg váza és a három tábla, a `regresszio.py`, a `festek.py`.

## Megállási küszöb

A brief megállási szabálya: az építő session indulásakor mért maradék heti keret felének elfogyásáig az S1 szakasz-diffje legyen 0. Induló érték: heti 83% → a küszöb **91,5%** (heti, minden modell). Ha ezt eléri a keret, és az S1 diffje nem 0: megállás és jelzés.

## Mérőszámok

| Pont | Dátum (UTC) | Heti · minden modell | Heti · Fable | 5 órás | Megjegyzés |
|---|---|---|---|---|---|
| F218.0 (indulás) | 2026-11-13 09:05 | 83% | 15% | 19% | `get_usage`; nullázás: 2026-11-14 14:00 UTC |

Diff-görbe (engedélyen kívüli diff-sorok szakaszonként, commitonként): még nincs mérés.

## Nyitott diff-sorok szakaszonként

Még nincs mérés.

## A régi generátorból visszafejtett szabályok

Még nincs bejegyzés.

## Session-váltások, kompaktálások

- 1. session (2026-11-13): az indulás `claude-opus-5-5` modellen modell-eltérés miatt megállt; a felhasználó a sessiont `claude-fable-5-2`-re állította, a munka innen indul.
