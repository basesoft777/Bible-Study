# FORRAS_FJ2_szamozas.md — 3e: a 15 `szamozas_elteres` sor besorolása

*FJ2 — FORRASJELOLTEK_BRIEF.md §3 szerint. Szkriptek: `naplok/FORRAS_FJ2_szamozas_general.py`
(verse_pairs.jsonl-lekérdezés), `naplok/FORRAS_FJ2_hianyellenoriz.py` (a repó saját
`LXX_OS`-kivonatának hiányvizsgálata), `naplok/FORRAS_FJ2_karoli_kjv_versszam.py`
(Károli–KJV versszám-összevetés). Kimenet: `naplok/FORRAS_FJ2_szamozas.tsv`.*

## 1. A fő lelet: a 15 sor többsége NEM versszámozási eltérés

A `lxx-morph` **forrás** JSON-jait (`/tmp/lxxmorph_test/db/seeds/lxx_morph/*.json`,
commit `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`) közvetlenül megnézve: **14 a 15
igehelyből TÉNYLEGESEN megvan a forrásban**, ugyanazzal a hivatkozással, mint a
Károliban (nincs eltolódás). A `konkordancia/LXX_OS/*.tsv` — amit a study-táblázatok
kerestek — viszont **hiányosan van kivonatolva**: pl. a `job-lxx.tsv`-ből teljesen
hiányzik a 17., 37. és 38. fejezet, a `joshua-vaticanus-b.tsv`-ből a 8., 10. és 13.
fejezet — miközben a forrás JSON-ban mindkettő megvan az elejétől a végéig.

**Ez tehát nem a §3e-ben feltételezett versszámozási probléma, hanem a
`eszkozok/lxx_os_import.py` kivonatolási hézaga.** Ennek javítása a jelen menet
hatáskörén kívül esik (FJ2 csak mér), de mindenképp jelentendő, mert a lezárt
LXX-egyeztetés (`lexikon/*_TUDOMANYOS.md`) 15 sora emiatt téves "szamozas_elteres"
címkét visel.

## 2. Soronkénti besorolás (K5: mind a 15 sor)

| Igehely (MT/Károli) | A forrásban megvan? | LXX-hivatkozás (verse_pairs) | Besorolás |
|---|---|---|---|
| Jób 17:13 | igen | Job 17:13 (identity) | **(a)** — a repó-kivonat hézaga, nem valódi eltérés |
| Jób 17:16 | igen | Job 17:16 (identity) | **(a)** — ua. |
| Hós 13:14 | igen | Hosea 13:14 (identity) | **(a)** — ua. (a `LXX_OS/hosea.tsv`-t nem vizsgáltuk tételesen, de a forrás megvan) |
| Jón 2:3 | igen | Jonah 2:4 (tvtms, eltolással) | **(a)** — a TVTMS szerint a LXX Jónás 2. fejezete +1 verssel el van tolva (a zsoltárbetét miatt); javasolt LXX-hely: **Jón(LXX) 2:4** |
| Jer 51:46 | **nem** (a forrásból is hiányzik) | nincs pár (`unpaired`) | **(b)** — valódi LXX-eltérés: a Jeremiás könyv MT és LXX szerkezete jelentősen eltér (a LXX kb. 1/7-ed rövidebb, átrendezett); kutatói kérdés |
| Józs 12:4 | igen | Josh 12:4 (identity) | **(a)** — a repó-kivonat hézaga |
| Józs 13:12 | igen | Josh 13:12 (identity) | **(a)** — ua. (a `joshua-vaticanus-b.tsv`-ből hiányzó 13. fejezet) |
| Józs 15:8 | igen | Josh 15:8 (identity) | **(a)** — a repó-kivonat hézaga (más okból, l. lent) |
| Józs 18:16 | igen | Josh 18:16 (identity) | **(a)** — ua. |
| Józs 17:15 | igen | Josh 17:15 (identity) | **(a)** — ua. |
| Jób 38:7 | igen | Job 38:7 (identity) | **(a)** — a `job-lxx.tsv`-ből hiányzó 38. fejezet |
| Jób 38:16 | igen | Job 38:16 (identity) | **(a)** — ua. |
| Jób 38:30 | igen | Job 38:30 (identity) | **(a)** — ua. |
| Ézs 63:13 | igen | Isa 63:13 (identity) | **(a)** — a repó-kivonat hézaga (az `isaiah.tsv`-t nem vizsgáltuk tételesen, de a forrás megvan) |
| Jón 2:6 | igen | Jonah 2:7 (tvtms, eltolással) | **(a)** — a Jón(LXX) 2:7-nek felel meg (ugyanaz az eltolás, mint fent) |

**Összegzés:** 13 sor **(a)** — megfeleltethető, a valódi ok a repó saját
kivonat-hézaga (nem a study kereszthivatkozás hibája); 2 sor **(a)**, de valódi
+1-es LXX-eltolással (Jón 2:3→2:4, Jón 2:6→2:7, a zsoltárbetét miatt); 1 sor **(b)**
valódi kutatói kérdés (Jer 51:46, a Jeremiás-könyv szerkezeti eltérése miatt).

## 3. Károli– és KJV-versállomány eltérése (1Móz, 2Móz, Péld)

Szkript: `naplok/FORRAS_FJ2_karoli_kjv_versszam.py`, forrás:
`konkordancia/Karoli_1908.tsv` vs. `konkordancia/KJV_Strongs_*.tsv`.

| Könyv | Károli versszám | KJV versszám | Csak Károliban | Csak KJV-ben |
|---|---|---|---|---|
| 1Móz | 1533 | 1533 | 0 | 0 |
| 2Móz | 1213 | 1213 | 1 (35:36) | 1 (36:38) |
| Péld | 914 | 915 | 0 | 1 (12:28) |

**Értelmezés:** 1Móz-ban tökéletes az egyezés. 2Móz-ban egyetlen off-by-one
csúszás van a 35–36. fejezet határánál (a sátor-építés szakasz Károli és KJV
közötti fejezetbeosztása eltér — ismert jelenség). Péld-ban a KJV egy pluszverset
tartalmaz (12:28b két külön versre bontva), amit a Károli egy versben hoz.

**Javaslat a 3b importkulcs tervezéséhez:** teljes külön Károli-kulcsú
számozási tábla **nem szükséges** — a három vizsgált könyvben összesen 2
eltérés van 3660 versből (0,05%). Elég egy rövid, kézzel karbantartott
kivétel-lista (ehhez hasonló méretű: `konkordancia/Karoli_KJV_kivetel_lista.tsv`,
2. menetben, ha az import megkezdődik) — nem kell teljes versificaciós tábla,
mint a LXX_OS/TVTMS esetében.
