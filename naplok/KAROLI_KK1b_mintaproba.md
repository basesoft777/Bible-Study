# KAROLI_KK1b_mintaproba.md — K4 mintapróba

*KK1b-4 — KAROLI_KULCS_BRIEF.md v1.1 §3, §1 mérce ("A K4 mintapróba
horgonya: a Károli-vers és a jelölt MT-vers között a `TAHOT_kivonat.tsv`
tulajdonnév- (TIPNR) Strongja; KJV-szöveg nem kell hozzá."). Szkript:
`naplok/KAROLI_KK1b_mintaproba_general.py`. Kimenet:
`naplok/KAROLI_KK1b_mintaproba.tsv`.*

## Módszer

10%-os véletlen minta (Python `random.seed(42)`), külön a `KJV`- és
`MT`-osztályú fejezetekből (`naplok/KAROLI_KK1b_fejezetosztaly.tsv`),
fejezetenként az első és az utolsó vers. Minden mintavershez: a
`TAHOT_kivonat.tsv` Strong-listájából megkeressük, van-e a
`TIPNR_kivonat.tsv`-ben szereplő tulajdonnév (mind a "Név (normalizált)",
mind a "Névváltozat" oszlopot figyelembe véve — pl. H3290 normalizált neve
"Israel", de a szó szerinti korai igehelyeken "Jacob" a névváltozat, és a
Károli-szöveg ilyenkor "Jákób"-ot ír), és egy kézzel épített, ~30 elemes
héber–magyar tulajdonnév-táblával ellenőrizzük, hogy a Károli-szöveg
tartalmazza-e a névalakot.

## Eredmény

| | Fejezet a mintában | Versminta (első+utolsó) |
|---|---|---|
| KJV-osztály (819 fejezetből 10%) | 82 | 164 |
| MT-osztály (84 fejezetből 10%) | 8 | 16 |
| **Összesen** | **90** | **180** |

| Állapot | Darab |
|---|---|
| `EGYEZIK` | 70 |
| `NEM_EGYEZIK` | 0 |
| `NINCS_ELLENORIZHETO_HORGONY` (a versben nincs a kis táblánkban szereplő tulajdonnév) | 110 |

**Az ellenőrizhető (névhorgonyos) mintán: 70/70 = 100,0%.**

Ez **meghaladja a §1 ≥98%-os küszöböt**. A 110 "nincs ellenőrizhető horgony"
sor nem számít bele a próbába (nem hamis egyezés vagy hiba, hanem hiányzó
tulajdonnév az adott versben — a kis, kézzel épített ~30 elemes névtábla
korlátja, nem a fejezetosztályozásé).

**Módszertani megjegyzés (javítási kör közben derült ki, dokumentálva):**
az első futásban 4 sor `NEM_EGYEZIK`-ként jelentkezett (1Móz 31:1, 33:1,
Jer 10:25 — H3290 "Israel"-ként keresve, de a szövegben "Jákób" áll; Ézs
35:10 — H6726 "Jerusalem"-ként keresve, de a szövegben "Sion" áll). Ezek
**nem valódi eltérések**, hanem a TIPNR "Név (normalizált)" oszlopának
kanonikus névhasználatából adódó hamis negatívok (a normalizált név a
személy/hely végleges neve, a tényleges igehelyen viszont gyakran a
korábbi név szerepel — pl. Jákób/Izráel, Sion/Jeruzsálem). A javítás után
(mindkét TIPNR-oszlop figyelembevétele) mind a 4 sor `EGYEZIK`-re változott.
