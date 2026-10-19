# F22_N-F22c_ujraparositas.md — az F90 által pótolt TAGNT-sorok miatt újrapárosítandó versek (az ÚSZ A/B csomag és a 22.8 próba)

*Keletkezett: 2026.10.19, `claude/f22-2kor`. A számok szkriptkimenetből jönnek: `python eszkozok/karoli_strong/f22_nf22c_minta.py --lista`. Állapot: **előkészítve, a modellhívás még nem futott** (a `PARDES_API_KEY` ebben a sessionben nincs beállítva).*

## 1. Besorolás (mért)

A mérce: a vers `szavak_<könyv>.tsv`-beli `er` sorainak szövege (a párosításkor használt eredeti tokenlista) összevetve a mai `betolt_eredeti()` tokenlistával (TAGNT-kivonat az F90 után). A Károli-kulcsot az F90 csoportonként döntötte el (DT120), ezért a mért lista **a Károli-kulcsok szerint** áll, és eltér az N-F22c NRSV-kulcsos felsorolásától (pl. Gal 2:20, nem 2:19).

| | vers |
|---|---|
| újrapárosítandó (az eredeti tokenlista változott, vagy a vers eddig eredeti nélküli volt) | **21** |
| a `f22/kezi_versek_<könyv>.tsv` kényszere alatt áll, de az eredeti szövege változatlan | 15 |

Újrapárosítandó: 3Ján 1:15; 2Thessz 1:8; 1Thessz 1:3, 2:6, 2:11, 2:12; Kol 1:11, 1:21; Fil 1:16, 1:17, 2:8; 1Pét 3:15; 1Ján 2:13; 1Tim 6:21; Gal 2:20; Ef 1:11, 2:15, 5:13; Zsid 3:9, 7:20, 12:23.

Változatlan eredetijű, kényszerített `kezi` (a régi, teljes görög szöveggel kapott modellválasz érvényes, a kényszer kivezethető): 2Thessz 1:7; 1Thessz 1:2, 2:7; Kol 1:12, 1:22; Fil 2:7; 1Pét 3:16; 1Ján 2:14; Gal 2:19; Ef 1:10, 2:14, 5:14; Zsid 3:10, 7:21, 12:22.

## 2. Módszer (terv)

1. `f22/minta_<könyv>_javito.tsv` (11 könyv, a 21 vers): `f22_nf22c_minta.py --ir`. Az `egyesit.py` a javító menet válaszát felülírásként olvassa (`modell_versek`), a mintát kiegészítésként (`minta_sorok`).
2. Futtatás: Message Batches API, `effort=high`, `prompt_v3` változatlanul, csak Sonnet (DT-F22c). A javító mintanevek (`<könyv>_javito`) az `api_koteg.py`-ban támogatottak (F22.10: a custom_id és a `konyv_nev` kiterjesztése).
3. Átvezetés (`api_koteg.py atvezet`): `f22/valaszok/sonnet/<könyv>_javito.jsonl`.
4. A kényszer kivezetése: az érintett sorok törlése az `f22/kezi_versek_<könyv>.tsv`-ből (a 21 + 15 vers), majd `egyesit.py --konyv <könyv>` és `--ellenoriz`.
5. **Felülírás előtt összevetés** (CLAUDE.md TSV-szabály): a régi és az új `parok_<könyv>.tsv` versenkénti különbsége ebbe a naplóba; eltérésnél megállás.

## 3. Költség (becslés)

21 vers × 0,0066 USD/vers (a 22.8 rossz esete) = 0,14 USD, a javító körrel is 0,3 USD alatt; a futó összeg 94,5049 USD, a plafon 104,36 USD.
