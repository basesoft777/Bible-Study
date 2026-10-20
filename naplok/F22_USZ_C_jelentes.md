# F22_USZ_C_jelentes.md — a 22.9 C csomag összesítője (Róm, 1Kor, Jel)

*Proveniencia: scope=Róm, 1Kor, Jel (1 272 Károli-vers) | forras=a három könyvjelentés (`naplok/F22_Rom_jelentes.md`, `F22_1Kor_jelentes.md`, `F22_Jel_jelentes.md`), `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `egyesit.py --ellenoriz` (szkriptkimenetek) | ts=2026-10-20. Ág: `claude/f22-2kor` (a #433 merge-e után a main-ből). Módszer: D45, a brief 22.9 és a DT-F22h (b) szerint (a main-en: DT262): Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul, könyvenként soros, a plafon-őr érintetlen, a batch-ek a felső becslésnek megfelelő részletekben (Róm 1 batch, 1Kor 2, Jel 3).*

## 1. Könyvenként

| könyv | Károli-vers | hívás | költség (USD) | USD/vers | kapuhiba 1. próba | javító körös köteg | `[nem TR]` | ebből párosított | régi arany |
|---|---|---|---|---|---|---|---|---|---|
| Róm | 431 | 47 | 2.1407 | 0.00497 | 3/431 | 3 | 107 | 7 | 50,0% (1/2) |
| 1Kor | 436 | 50 | 2.0566 | 0.00472 | 7/436 | 6 | 180 | 23 | 50,0% (2/4) |
| Jel | 405 | 48 | 3.2796 | 0.00810 | 8/405 | 7 | 641 | 44 | 100,0% (11/11) |
| **össz** | **1272** | **145** | **7.4769** | **0.00588** | **18/1272** | **16** | **928** | **74** | |

Végleges kapuhiba: 0/1 272. Mind a 18 kapuhiba **versenkénti** kapuhiba volt (16 köteg; a `f22/api_termeles/high/_munka/*.json` szerint: nem lefedett eredeti vagy magyar szavak, hibás eredeti sorszám, üres pár, többször szereplő magyar szó), **egész köteg formátumhiba (érvénytelen JSON) egy sem**; a javító kör mindegyiket megoldotta (végleges kapuhiba 0). Az `egyesit.py --konyv <könyv> --ellenoriz` mind a háromra „rendben”. A futásnapló minden új sorában `prompt_sha256_12 = 84f12ca7aafb`.

## 2. Költség, keret, a mért egységár

- A C költsége **7.4769 USD** (a vetítés ×1,2 tartalékkal 7,995 USD volt: belefért; a Jel egységára, 0,0081 USD/vers, a legmagasabb az ÚSZ-ben). A futó összeg 96,0540 USD-ról **103.5308 USD**-ra nőtt; a plafon (`api_koteg.PLAFON_USD`) 104,36 USD, a **maradék 0.829 USD**. Az ÚSZ-keret (D45: 18 USD, 86,3698 + 18) **17.1610 USD**-ot használt fel (a 22.9 A, B, a 2Kor, az N-F22c és a C együtt).
- Mért egységár a 22.8, az A, a B, a 2Kor és a C együtt: **0.005495 USD/vers** ((0.005226 × 1638 + 1.36 + 7.4769) / 3166 vers).
- A DT-F22h (b) szerint a plafon-őr nem változott; a részletekben küldés miatt a legkisebb batch 6 kérés volt.

| hátralevő | vers | vetítés | ×1,2 tartalékkal | belefér a maradékba? |
|---|---|---|---|---|
| evangéliumok + ApCsel (Mt, Mk, Luk, Ján, ApCsel) | 4785 | 26.29 USD | 31.55 USD | **nem** (0.83 USD maradt): külön keretdöntés (D45) |

## 3. Az N-F22c versek útja a C-ben

- A három Károli-összevonás (Róm 3:30, Róm 8:38, 1Kor 3:22) a jóváhagyott `f22/versosszevonas.tsv`-sorok szerint `fuggoben`/`kezi` (hu 38 + er 34 a Rómában, 6 + 6 az 1Korban), link nélkül; átnézésre (`naplok/F22_{Rom,1Kor}_atnezes.tsv`).
- A Róm 16:25–27 és a Jel 12:18 görög szövege az F90 óta megvan: rendes versként mentek a modellhez.
- A tokenszintű vershatár-vizsgálat a három könyvben nem talált megerősített eltérést (a Róm 4:16–17 téves jelzés).

## 4. A `[nem TR]` tokenek: 928, ebből 74 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a); az újraépítés után 119 sor, 22 ÚSZ-könyv); a sorok a három könyvjelentés 4. szakaszában. A Jel `[nem TR]` aránya kiugró (641 / 10 185 = 6,3%), párosított belőle 44.

## 5. Mi marad

- Az **evangéliumok és az ApCsel** (4 785 vers) külön keretdöntés.
- **N-F22e:** a tokenszintű vershatár-mechanizmus (a nyolc `kezi` vers a mergelt könyvekben: 2Kor 2:12–13, 5:14–15, 8:13–14, Zsid 1:1–2, Fil 3:13–14); az ApCsel 13:32–33 és 24:2–3 a keretdöntésnél.
- Független ellenőrzés (`naplok/ELLENOR_F22_USZ_C.md`), draft PR, merge csak a felhasználótól.
