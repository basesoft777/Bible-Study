# F22_N-F22c_ujraparositas.md — az F90 által pótolt TAGNT-sorok miatt újrapárosítandó versek (az ÚSZ A/B csomag és a 22.8 próba)

*Proveniencia: scope=11 ÚSZ-könyv, 36 vers (21 újrapárosított + 15 kényszerkivezetett) | forras=`adat/karoli_strong/{parok,szavak}_<könyv>.tsv` (git `9f4fc06` ↔ `c0d1070`), `f22/api_termeles/futasnaplo.tsv`, `f22_nf22c_minta.py --lista` (szkriptkimenetek, split('\t')) | ts=2026-10-19.*

*Keletkezett: 2026.10.19, `claude/f22-2kor`. A számok szkriptkimenetből jönnek: `python eszkozok/karoli_strong/f22_nf22c_minta.py --lista`. Állapot: **lefutott és egyesítve** (2026.10.19; l. a 4–6. szakasz).*

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

## 4. Futtatás (2026.10.19)

Sonnet (`claude-sonnet-5-5`), Message Batches API, `effort=high`, `prompt_v3` változatlanul (`prompt_sha256_12 = 84f12ca7aafb`), könyvenként soros batch-ek (1 köteg/könyv), a 21 újrapárosítandó vers a `f22/minta_<könyv>_javito.tsv` mintákból; a válaszok `f22/valaszok/sonnet/<könyv>_javito.jsonl`.

| könyv | hívás | költség (USD) | első körben kapuhibás hívás |
|---|---|---|---|
| 3Ján | 2 | 0.0146 | 1 |
| 2Thessz | 1 | 0.0062 | 0 |
| 1Thessz | 1 | 0.0293 | 0 |
| Kol | 2 | 0.0228 | 1 |
| Fil | 2 | 0.0255 | 1 |
| 1Pét | 2 | 0.0219 | 1 |
| 1Ján | 1 | 0.0064 | 0 |
| 1Tim | 1 | 0.0060 | 0 |
| Gal | 1 | 0.0131 | 0 |
| Ef | 1 | 0.0228 | 0 |
| Zsid | 1 | 0.0204 | 0 |

Összesen **15 hívás, 0.1891 USD** (a becslés 0,3 USD alatt volt). Az első kör 4 könyvben (3Ján, Kol, Fil, 1Pét) egész köteg formátumhibás volt (a modell a JSON elé szöveget írt), a javító kör mindegyiknél rendben lett: **végleges kapuhiba 0**. A futó összeg a plafon (104.36 USD) alatt maradt: 96.0540 USD.

## 5. Kényszer kivezetése, egyesítés, összevetés

1. A 36 vers közül 33 sora törölve az `f22/kezi_versek_<könyv>.tsv`-ekből (10 fájl); a további 3 (3Ján 1:15, Fil 1:16, Fil 1:17) eredeti szöveg nélküli volt, kényszer alatt nem állt. Az `egyesit.py` az átnézési listákból (`naplok/F22_<könyv>_atnezes.tsv`) is kivette a 36 verset.
2. `egyesit.py --konyv <könyv>` mind a 11 könyvre, majd `--ellenoriz`: mindegyik „rendben”.
3. **Összevetés** (CLAUDE.md TSV-szabály: `split('\t')`, a régi a git `HEAD~1` verziója): a `parok_<könyv>.tsv` és a `szavak_<könyv>.tsv` versenkénti összevetése, 11 könyv × 2 tábla. **Csak a 36 célvers változott, kívüle egyetlen vers sorai sem** (versenként összevetve a sorok sorrendje és tartalma). A versek száma a `parok` táblákban nőtt (a 36 vers eddig link nélküli, `kezi` volt), a `szavak` táblákban változatlan; a `szavak` *sorainak* száma nőtt (l. a 7. szakasz).

## 6. Eredmény versenként

A 36 vers mindegyike eddig link nélkül állt (`kezi`, `fuggoben`); most mindegyik kapott linkeket (`alacsony`, forrás `S`), `fuggoben` szósor nincs.

| könyv | vers | típus | régi: pár / bizonyosság | új: pár / bizonyosság | új szavak: betoldas / forditatlan / fuggoben |
|---|---|---|---|---|---|
| 3Ján | 3Ján 1:15 | újrapárosított | 0 / – | 9 / alacsony 9 | 3 / 2 / 0 |
| 2Thessz | 2Thessz 1:7 | kényszer kivezetve | 0 / – | 19 / alacsony 19 | 6 / 2 / 0 |
| 2Thessz | 2Thessz 1:8 | újrapárosított | 0 / – | 20 / alacsony 20 | 4 / 2 / 0 |
| 1Thessz | 1Thessz 1:2 | kényszer kivezetve | 0 / – | 14 / alacsony 14 | 2 / 2 / 0 |
| 1Thessz | 1Thessz 1:3 | újrapárosított | 0 / – | 26 / alacsony 26 | 7 / 9 / 0 |
| 1Thessz | 1Thessz 2:6 | újrapárosított | 0 / – | 18 / alacsony 18 | 3 / 0 / 0 |
| 1Thessz | 1Thessz 2:7 | kényszer kivezetve | 0 / – | 13 / alacsony 13 | 3 / 3 / 0 |
| 1Thessz | 1Thessz 2:11 | újrapárosított | 0 / – | 15 / alacsony 15 | 2 / 0 / 0 |
| 1Thessz | 1Thessz 2:12 | újrapárosított | 0 / – | 15 / alacsony 15 | 4 / 5 / 0 |
| Kol | Kol 1:11 | újrapárosított | 0 / – | 15 / alacsony 15 | 1 / 2 / 0 |
| Kol | Kol 1:12 | kényszer kivezetve | 0 / – | 11 / alacsony 11 | 6 / 7 / 0 |
| Kol | Kol 1:21 | újrapárosított | 0 / – | 15 / alacsony 15 | 2 / 2 / 0 |
| Kol | Kol 1:22 | kényszer kivezetve | 0 / – | 16 / alacsony 16 | 3 / 4 / 0 |
| Fil | Fil 1:16 | újrapárosított | 0 / – | 11 / alacsony 11 | 6 / 4 / 0 |
| Fil | Fil 1:17 | újrapárosított | 0 / – | 11 / alacsony 11 | 2 / 0 / 0 |
| Fil | Fil 2:7 | kényszer kivezetve | 0 / – | 11 / alacsony 11 | 0 / 0 / 0 |
| Fil | Fil 2:8 | újrapárosított | 0 / – | 14 / alacsony 14 | 4 / 0 / 0 |
| 1Pét | 1Pét 3:15 | újrapárosított | 0 / – | 27 / alacsony 27 | 6 / 5 / 0 |
| 1Pét | 1Pét 3:16 | kényszer kivezetve | 0 / – | 19 / alacsony 19 | 5 / 3 / 0 |
| 1Ján | 1Ján 2:13 | újrapárosított | 0 / – | 26 / alacsony 26 | 3 / 0 / 0 |
| 1Ján | 1Ján 2:14 | kényszer kivezetve | 0 / – | 27 / alacsony 27 | 3 / 3 / 0 |
| 1Tim | 1Tim 6:21 | újrapárosított | 0 / – | 10 / alacsony 10 | 1 / 15 / 0 |
| Gal | Gal 2:19 | kényszer kivezetve | 0 / – | 9 / alacsony 9 | 2 / 0 / 0 |
| Gal | Gal 2:20 | újrapárosított | 0 / – | 35 / alacsony 35 | 3 / 4 / 0 |
| Ef | Ef 1:10 | kényszer kivezetve | 0 / – | 20 / alacsony 20 | 8 / 5 / 0 |
| Ef | Ef 1:11 | újrapárosított | 0 / – | 22 / alacsony 22 | 2 / 3 / 0 |
| Ef | Ef 2:14 | kényszer kivezetve | 0 / – | 17 / alacsony 17 | 3 / 4 / 0 |
| Ef | Ef 2:15 | újrapárosított | 0 / – | 21 / alacsony 21 | 5 / 5 / 0 |
| Ef | Ef 5:13 | újrapárosított | 0 / – | 15 / alacsony 15 | 2 / 1 / 0 |
| Ef | Ef 5:14 | kényszer kivezetve | 0 / – | 14 / alacsony 14 | 4 / 3 / 0 |
| Zsid | Zsid 3:9 | újrapárosított | 0 / – | 15 / alacsony 15 | 4 / 4 / 0 |
| Zsid | Zsid 3:10 | kényszer kivezetve | 0 / – | 18 / alacsony 18 | 2 / 2 / 0 |
| Zsid | Zsid 7:20 | újrapárosított | 0 / – | 14 / alacsony 14 | 2 / 0 / 0 |
| Zsid | Zsid 7:21 | kényszer kivezetve | 0 / – | 25 / alacsony 25 | 3 / 1 / 0 |
| Zsid | Zsid 12:22 | kényszer kivezetve | 0 / – | 13 / alacsony 13 | 3 / 0 / 0 |
| Zsid | Zsid 12:23 | újrapárosított | 0 / – | 17 / alacsony 17 | 5 / 0 / 0 |

*Megjegyzés:* a kényszerkivezetett 15 vers a régi, teljes görög szöveggel kapott modellválaszból épül (az eredeti szövegük nem változott); az újrapárosított 21 vers az F90 utáni teljes tokenlistával kapott új választ. A `nem_tr_lista.py` újrafutott (`adat/karoli_strong/nem_tr_parositott.tsv`, 45 sor). Az A/B könyvek `F22_<könyv>_jelentes.md` fájljainak számait ez a napló korrigálja: a 36 vers `kezi`/`fuggoben` jelölése megszűnt.

## 7. Sorszám-változás (E17/DT3) és magyarázata

A `parok` +617 sor a 36 vers új linkjeinek összege (a napló 6. táblája versenként bontja). A `szavak` +120 sora az F90 által pótolt, korábban hiányzó eredeti tokenek: az újrapárosított versek eredeti tokenlistája teljes lett (a kényszerkivezetett 15 versé nem változott, ott a Δ 0), a 3Ján 1:15 és a Fil 1:16–17 eddig eredeti nélküli volt (a korábban csak Károli-szavas sorokhoz most eredeti sorok jönnek). A Δ könyvenként (`git` `9f4fc06` → `c0d1070`, adatsorok, fejléc nélkül):

| könyv | `parok` sorok Δ | `szavak` sorok Δ |
|---|---|---|
| 3Jan | +9 | +11 |
| 2Thessz | +39 | +3 |
| 1Thessz | +101 | +14 |
| Kol | +57 | +5 |
| Fil | +47 | +31 |
| 1Pet | +46 | +5 |
| 1Jan | +53 | +7 |
| 1Tim | +10 | +17 |
| Gal | +44 | +2 |
| Ef | +109 | +14 |
| Zsid | +102 | +11 |
| **összesen** | **+617** | **+120** |

A független ellenőr a Fil 1:16–17 (TAGNT 37 sor = a `szavak_Fil.tsv` 11 + 26 eredeti sora), a 3Ján 1:15 és az 1Tim 6:21 (24 = 24) számát külön megerősítette (`naplok/ELLENOR_F22_2KOR.md`). Az E17 a `futtat.py`-ban nincs megvalósítva; ez a szakasz a kézi bontás.
