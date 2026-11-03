# B3 — a BDB forrás-átírási hibája: `atiras` hibaosztály (DT581), mérés

2026-11-03 · modell: claude-opus-5-5 · ág: `claude/optimistic-wozniak-ac2f08` (a main 410e59fa-ről, a #611 után)
Szkript: `python naplok/B3_ATIRAS_meres.py` (csak olvas).

## 0. Kiinduló helyzet

A KEZI_FOLTOK felmérés B3 pontja: a DictBDB.json latin betűs átírásaiban a „®” és a „°” torz kód; a H7585-nél
(4e2cfc27) a jóváhagyott fordítás megjegyzésébe és szövegébe ment kézi javítás, mert a `bdb_forras_javitas.tsv`-nek
nem volt átírás-osztálya.

A torz jelek jelentése: a „®” a redukált magánhangzó (ᵉ), a „°” az álef (ʾ). A BDB.lexicon ugyanezt a szöveget
nagyrészt ugyanígy torzan hordozza, két szócikkben viszont tisztán: H7496 és (máshol, 18-szor) „She'ôl”, H7218 „ra'š”.

## 1. A forrás (`adat/bdb_szakaszok.tsv`) „®”-alakjai → `atiras` sorok

40 sor, 33 Strong.

- **`javitva`** — 37 sor, 30 Strong, mind a Seól-család (`Sh®°ôl` / `sh®°ôl` / `She®°ôl` → `Sheʾôl` / `sheʾôl`):
  H0011, H0734, H0776, H0953, H1004, H1086, H1097, H1323, H1802, H2670, H2706, H3331, H3344, H5117, H5181, H5315,
  H5971, H6009, H6174, H6310, H6931, H6986, H7496, H7585, H7646, H7845, H7901, H8371, H8482, H8551.
- **`jelolt_marad`** — 3 sor: H2609 `néns®`, H6573 `s®nhana`, H7848 `šond®t` (a szabály szerinti alak a lexikonban
  nem áll; N91).

Szabály: „e?®” → „e”, „°” → „ʾ”; igazolás: a szabály szerinti alak (ʾ → ') tiszta latin szóként áll a BDB.lexicon
valamely BDB-szócikkében. A tábla többi sora (pe_mem, hivatkozas, kezi, heber_sorrend) bájtra változatlan; a
fejléc a `--ts-atiras 2026-11-03` kapcsolóval és az új kód-hash-sel módosul.

## 2. A torz alakot hordozó fordítások (`adat/forditasok.tsv`, BDB, `forditas_hu`)

A megjelenítés (`bdb_rovidites.atiras_javit`) részszöveg szerint cserél, ezért a toldalékos magyar alak is javul. A
magyar szövegben a tár alakja áll (DT581 🟢, felhasználó, 2026-11-03: „Seól álljon”): „Sh®°ôlban” → „Seólban”;
az angol szövegben a helyreállított átírás: „Sh®°ôl” → „Sheʾôl”. A fordítássorokat nem írtam át.

| Strong | jelentes_szam | allapot | „®” előtte | utána | teendő |
|---|---|---|---|---|---|
| H0011 | sz3 | sonnet | 2 | 0 | nincs |
| H0776 | teljes | sonnet | 1 | 0 | nincs |
| H1004 | sz8 | sonnet | 1 | 0 | nincs |
| H1086 | sz5 | sonnet | 1 | 0 | nincs |
| H1097 | sz3 | sonnet | 1 | 0 | nincs |
| H1323 | teljes | sonnet | 1 | 0 | nincs |
| H1802 | sz4 | sonnet | 1 | 0 | nincs |
| H2706 | teljes | sonnet | 1 | 0 | nincs |
| H3331 | sz3 | sonnet | 1 | 0 | nincs |
| H5117 | teljes | sonnet | 2 | 0 | nincs |
| H5971 | sz11, sz23 | sonnet | 1 + 1 | 0 | nincs |
| H6174 | sz2 | sonnet | 1 | 0 | nincs |
| H6310 | teljes | sonnet | 2 | 0 | nincs |
| H7646 | teljes | sonnet | 1 | 0 | nincs |
| H7845 | sz4 | sonnet | 1 | 0 | nincs |
| H7901 | sz17 | sonnet | 1 | 0 | nincs |
| H8371 | sz3 | sonnet | 1 | 0 | nincs |
| **H2609** | sz2 | sonnet | 1 | 1 | forrásdöntés (N91), utána esetleg új fordítás |
| **H6573** | sz2 | sonnet | 1 | 1 | forrásdöntés (N91), utána esetleg új fordítás |
| **H7848** | sz2 | sonnet | 1 | 1 | forrásdöntés (N91), utána esetleg új fordítás |
| H1004, H5971, H7901 | teljes | elavult | 1, 2, 1 | 0 | nincs (elavult sor) |

**Új fordítás nem kell:** a „Seól” alakot is a megjelenítés adja (`ATIRAS_MAGYAR`), a fordítássorokhoz nem nyúl.
A terminológia (`adat/terminologia.tsv`) viszont „Seol”-t ír; az eltérés: N90.

A H7585 `kezi` sorai (teljes, nyelvi_hatter) a fordítás szövegében már „Seól”-t hordoznak (4e2cfc27), a „She®°ôl”
csak a megjegyzésükben áll; a csere ezekhez nem nyúl. A kézi foltot ez a PR nem vonja vissza: a sor jóváhagyott `kezi`
fordítás, és a megjegyzés pontosan rögzíti az okát; a forrásoldali hibát mostantól az `atiras` sor viseli.

## 3. Lapok — laponkénti diff

Módszer: mind a 9 lexikonlap generálása (`general.py --cel lexikon --kimenet <repón kívül>`) kétszer, ugyanazon a
kódon és adaton: az alapvonalban az `atiras_javitasok` üresre cserélve, a másodikban a javítással.

| Lap | diff (sor) |
|---|---|
| ALVIL-001_TUDOMANYOS.md (kiadott) | 0 |
| ANTROP-001_TUDOMANYOS.md | 0 |
| HAMART-001_TUDOMANYOS.md | 0 |
| HODIT-001_TUDOMANYOS.md | 0 |
| ISTENTISZT-001_TUDOMANYOS.md (kiadott) | 0 |
| KIRALY-001_TUDOMANYOS.md | 0 |
| MENNY-001_TUDOMANYOS.md | 0 |
| TEREMT-001_TUDOMANYOS.md | 0 |
| TEREMT-002_TUDOMANYOS.md | 0 |

Egyetlen generált lap sem hordoz „®”-t (az alapvonalban sem): a 30 javított Strong BDB-blokkja egyik lapon sem
renderel a torz szakaszból (a H7585 a `kezi` úton megy). A `TORZSCIKK` a lapból renderel, így az sem változik. A
lapokat ezért nem commitoltam. A hatás az olvasó szónézetében (`/szo/<Strong>`, `olvaso_szerver/blokkok.py`) látszik,
amely futásidőben renderel.

**Második kör (DT581 🟢, „Seól” a magyar szövegben, 2026-11-03):** ugyanez a módszer az új kóddal: mind a 9 lap
alapvonal ↔ javított 0 sor, és az első kör javított lapjaihoz képest is 0 sor. A „Seól” a lapokon eddig is csak a
kézi forrásból áll (ALVIL-001 2, HODIT-001 6 előfordulás), „Sheʾôl” és „®” egyik lapon sincs. Az olvasóban
(`blokkok._rovidites`, a WSL venv-ben ellenőrizve): magyar blokk „a Sh®°ôlban” → „a Seólban”, angol blokk
„in Sh®°ôl” → „in Sheʾôl”.

## 4. Kapuk

A 26. szabály (`bdb_szakasz_hu.tsv` naprakész): 0 eltérés az új javítótáblával (a `szakasz_bemenet.py` csak a
`hivatkozas` sorokat olvassa, az `sz<n>` hash nem változik).
