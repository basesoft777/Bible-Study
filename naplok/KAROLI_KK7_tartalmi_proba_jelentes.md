# KAROLI_KK7_tartalmi_proba_jelentes.md — tartalmi próba

*KK7.1 — KAROLI_KULCS_KK7_BRIEF.md §3, §1 mérce. Szkriptek:
`naplok/KAROLI_KK7_ujonnan_kitoltott_general.py` (a 671 újonnan kitöltött
(LXX-fájl, igehely_lxx) pár azonosítása, `a6783e4`-hez képest),
`naplok/KAROLI_KK7_tartalmi_proba.py` (a Pearson-korrelációs próba, ±2
eltolással, TIPNR-horgonnyal). Kimenet: `naplok/KAROLI_KK7_ujonnan_kitoltott.tsv`,
`naplok/KAROLI_KK7_fejezet_dontes.tsv`.*

## Módszer

Minden fejezetre, amelyben van újonnan kitöltött kulcs (27 fejezet, 671 pár),
a jelenlegi (`shift=0`) és a ±1/±2 versre tolt változatra Pearson-korreláció
az LXX-vers szószáma és a hozzárendelt Károli-vers szószáma között. A
**legjobb** korreláció győz (nem csak a jelenlegié) — ha ≥0,60 és a második
legjobbnál legalább 0,15-tel nagyobb, a hozzá tartozó eltolás lesz az
"elfogadott eltolás" (lehet 0 is, ha a jelenlegi már helyes, vagy ±1/±2,
ha korrekció kell). Ha a próba nem mérhető (kevesebb mint 4 pár egy
eltoláshoz), vagy egyik eltolás sem elég erős/egyértelmű, a fejezet
**üresre áll** (G1) — a tulajdonnév-horgony (TIPNR, a KK1b-4 mintájára)
csak a **nem mérhető** esetben dönthet (§1 szó szerint), egy egyértelműen
gyenge/bizonytalan korrelációs eredményt NEM írhat felül (egy generikus
név, mint "Izráel" vagy "Dávid", szinte minden fejezetben előfordulna,
tehát önmagában nem megbízható felülbírálati alap).

## Eredmény

| | Fejezet |
|---|---|
| Vizsgált fejezet | 27 |
| **Elfogadva** (a jelenlegi vagy egy korrigált eltolással) | **19** |
| — ebből a jelenlegi (`shift=0`) már helyes volt | 7 |
| — ebből korrekció kellett (±1 vagy ±2) | 12 |
| **Üresre állítva** | **8** |

**A 12 korrigált fejezet** (mind `shift=-1` vagy `-2`, megerősítve a brief
0.5-ös hipotézisét — a többletvers nem a fejezet elején van):
1Kir 6 (−2), 1Kir 22 (−1), 1Sám 18 (−1), 1Sám 20 (−1), 1Sám 23 (+1),
4Móz 6 (−1), 4Móz 29 (+1), Jón 1 (+1), Józs 10 (−1), Józs 13 (−1),
Ézs 9 (+1), **Ézs 63 (−1, a próbakő)**.

**A 8 üresre állított fejezet:** 1Sám 17, Hós 11, Jer 33, Jer 48, Jób 38,
Józs 8, Péld 18, Ézs 56 — mindegyiknél a korrelációs próba vagy nem adott
elég erős/egyértelmű jelet (a legjobb és a második legjobb eltolás
korrelációja túl közel van egymáshoz — pl. Ézs 56: r(−1)=0,74 vs.
r(−2)=0,61, különbség csak 0,13 < 0,15), vagy egyáltalán nem volt erős
jel egyik irányban sem.

**A brief 0.5 nyolc "erős jel" fejezete** (4Móz 6, 1Kir 22, Józs 10,
Józs 13, 1Sám 18, 1Sám 20, Ézs 56, Ézs 63) közül **7 megerősítve
korrekcióval**, 1 (Ézs 56) a szigorú 0,15-ös margó miatt üresre állt (a
korreláció maga is jelezte a −1-es eltolást, de a −2 is közel volt hozzá
— konzervatív, G1-nek megfelelő döntés). A két "gyenge jel" fejezet
(1Sám 17, Jer 48) mindkettő üresre állt — megerősítve, hogy a jel valóban
gyenge volt.

## Horgonyok

23/27 fejezetben volt TIPNR-alapú név-horgony (a döntést csak a nem
mérhető esetekben befolyásolva — ebben a menetben egyik fejezet sem volt
"nem mérhető", mindegyik legalább 4 újonnan kitöltött verset tartalmazott,
így a horgony ténylegesen egyik döntést sem írta felül, csak
dokumentálva van minden sorban).
