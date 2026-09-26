# KAROLI_KK75_kiindulas.md — kiindulás

*KK7.5.0 — KAROLI_KULCS_KK75_BRIEF.md §3.*

## §0 újramérése

| LXX-vers | Görög szöveg (eleje) | Most | Helyesen |
|---|---|---|---|
| 1Sám 20:41 | καὶ ὡς εἰσῆλθεν τὸ παιδάριον | `1Sám 20:41` ✓ | `1Sám 20:41` |
| 1Sám 20:42 | καὶ εἶπεν Ιωναθαν πορεύου εἰς εἰρήνην | üres (`szamozas_elteres`) | `1Sám 20:42` |
| 1Sám 21:1 | καὶ ἀνέστη Δαυιδ καὶ ἀπῆλθεν | `1Sám 20:42` — **hibás** | `1Sám 20:43` |
| 1Sám 21:2 | καὶ ἔρχεται Δαυιδ εἰς Νομβα | `1Sám 21:1` ✓ | `1Sám 21:1` |

Megerősítve, közvetlenül a `konkordancia/LXX_OS/1-samuel.tsv` és a
`konkordancia/Karoli_1908.tsv` tartalmán.

**A gyökér ok** (`verse_pairs.jsonl` közvetlen vizsgálatával): a raw LXX
`1-samuel 20:42` ÉS `1-samuel 21:1` **mindkettő** a KJV `20:42`-re
hivatkozik (`method=tvtms`) — ez egy fejezethatárt átlépő, kétszeres
KJV-célú eset (hasonló a Zsoltár-cím-duplikációhoz, de itt a két forrás
**két különböző LXX-fejezetben** van, nem egyben). A KK7 döntéstáblája
1Sám 20-ra `elfogad, -1` — ez a `21:1` forrásra (ami a "legmagasabb", tehát
az ellenpróba szerint ő kapja meg az eltolást) `20:42`-t ad (kjv_v=42,
d=1, korrekció=-1 → 42), miközben a `20:42` forrás üresen marad (az
ellenpróba elutasítja, mert nem ő a "legmagasabb"). A valódi Károli-cél
viszont fordított: `20:42`-höz a `20:42` forrás tartozik, `21:1`-hez pedig
a fejezet-záró `20:43`.
