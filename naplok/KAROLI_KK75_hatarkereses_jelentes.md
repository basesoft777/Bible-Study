# KAROLI_KK75_hatarkereses_jelentes.md — korpuszszintű keresés

*KK7.5.1 — KAROLI_KULCS_KK75_BRIEF.md §3, §1 (a)–(c). Szkriptek:
`naplok/KAROLI_KK75_hatarkereses_general.py` (nyers, feltáró keresés),
`naplok/KAROLI_KK75_hatarkereses2_general.py` (pontos, `verse_pairs.jsonl`-alapú
fejezethatár-átlépő duplikáció-keresés). Kimenetek:
`naplok/KAROLI_KK75_hatarkereses.tsv` (999 sor, feltáró),
`naplok/KAROLI_KK75_hatarkereses2.tsv` (1 sor, pontos),
`naplok/KAROLI_KK75_hatarkereses_vegleges.tsv` (a végleges, 2 soros
felülbírálási javaslat).

## Módszer és a zaj kiszűrése

A nyers keresés (a)–(c) tesztjei önmagukban **erősen zajosak**, mert nem
különböztetik meg a valódi hibákat a **szándékos, dokumentált**
mechanizmusoktól:

- **(a) többes hivatkozás:** ha a keresést nem szűkítjük ugyanarra az
  LXX-fájlra (slugra), **minden** olyan vers hamis találat lenne, ahol két
  **független szöveghagyomány** (pl. `daniel` és `daniel-theodotion`,
  `joshua` és `joshua-vaticanus-b`) ugyanarra a Károli-célra mutat — ez
  nem hiba, két tanú egyezése. Fájlon belülre szűkítve **0 találat**.
- **(b) fejezethatár-átlépés:** a nyers teszt (raw LXX-fejezet ≠ Károli-
  fejezet) **920 találatot** ad, de ezek túlnyomó többsége a
  `KEZI_ELTOLASOK` **szándékosan** fejezethatárt átlépő, dokumentált
  eltolása (pl. Jób 38:39–41→Jób 39:1–3, 4Móz 12:16→13:1, Préd 11:9–10→12:1–2),
  vagy a Zsoltárok jól ismert, rendszeres LXX/MT fejezet-eltolása (pl.
  Zsolt(LXX) 11→Zsolt 12) — egyik sem hiba. Egy **pontos, `verse_pairs.jsonl`-
  alapú** teszttel (`hatarkereses2`): csak azokat a KJV-célokat nézve,
  amelyekre **két különböző fejezetből** mutat forrás **ugyanabban az
  elfogadott fejezetben**, **pontosan 1 találat**: `1Sám 20:42` (a brief
  0. pontjában leírt eset).
- **(c) hiányzó Károli-vers a sorozatból:** 78 találat, ebből a legtöbb
  egyetlen vers (jellemzően a fejezet 1. verse — Zsoltár-cím-ambiguitás,
  már ismert és szándékosan üres, l. KK6/KK7), vagy egy teljes `EGYIK_SEM`-
  fejezet (pl. Dán 3, mind a 30 vers hiányzik — a fejezet szándékosan
  érintetlen). **Két többes hiányt mintaellenőriztünk**: 1Kir 6:11–14 és
  1Sám 18:1–5,10–11,17–19,30 — mindkettő **jól dokumentált, valódi
  LXX-minusz** (a görög szöveghagyomány e helyeken rövidebb, mint a héber/
  Károli — 1Kir 6:11–14 klasszikus LXX-kihagyás, 1Sám 17–18 a Vaticanus-
  szöveg híres nagy kihagyása) — **nem importer-hiba**.

## Az egyetlen megerősített, valódi hiba

| LXX-vers | Most | Javasolt | Típus | Bizonyíték |
|---|---|---|---|---|
| `1-samuel 20:42` | üres | `1Sám 20:42` | fejezethatár-átlépő többes hivatkozás | `verse_pairs.jsonl`: `1-samuel 20:42` és `1-samuel 21:1` mindkettő KJV `20:42`-re hivatkozik; a görög "καὶ εἶπεν Ιωναθαν πορεύου εἰς εἰρήνην" = Károli "Monda azért Jonathán… Eredj el békességgel" |
| `1-samuel 21:1` | `1Sám 20:42` (hibás) | `1Sám 20:43` | ugyanaz | ugyanaz a KJV-cél; a görög "καὶ ἀνέστη Δαυιδ καὶ ἀπῆλθεν" = Károli "Felkele ezután és elméne" — a fejezet záró (43.) verse |

**K2 (a keresés utáni nyitott találatok):** a fenti egyetlen valódi eset
a KK7.5.2-ben javítva (l. `naplok/KAROLI_KK75_jelentes.md`); minden más
(a)/(b)/(c) találat vagy strukturálisan szándékos (KEZI-eltolás, Zsoltár-
fejezet-eltolás, cím-ambiguitás, `EGYIK_SEM`), vagy dokumentált valódi
LXX-minusz — egyik sem igényel további beavatkozást.
