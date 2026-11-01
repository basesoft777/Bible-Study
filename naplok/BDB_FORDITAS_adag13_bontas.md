# BDB_FORDITAS — a 13. adag (sorrend 5671–7921) és a 14. adag (7922–8073): Batch API-út, tábla-Δ, költség, commitonkénti bontás (DT-F38y, DT-F38u, DT56)

*A #38 (BDB_FORDITAS) 13. adagja az Anthropic Message Batches API-n (`eszkozok/bdb_api_koteg.py`), próba nélkül (a felhasználó döntése, 2026-11-01, DT-F38y); `allapot=sonnet`, `modell=claude-sonnet-5-5` (a tényleges API-válasz modellneve), `effort=high`. A 14. adag (a sorrend utolsó 152 szócikke) a DT-F38u szerint a 13. adag maradékával együtt futott. Tartomány: `naplok/BDB_FORDITAS_sorrend.tsv` 13. adag 5671–7921 (2251 szócikk, 499 871 forráskarakter) és 14. adag 7922–8073 (152 szócikk, 71 439 karakter).*

*Az adag állapota: lezárva: a fordítás kész; a sorrendtábla mind a 8073 sora szerepel az `adat/forditasok.tsv`-ben (halmazkülönbség: 0). Független ellenőrzésre vár.*

## 0. Károli-lefedettség (DT56) — mérés a beküldés előtt

Proveniencia: `python naplok/BDB_FORDITAS_karoli_lefedettseg.py --tol 5671 --adagok 2` | scope=BDB-sorrend 5671– | forras=naplok/BDB_FORDITAS_sorrend.tsv x adat/karoli_strong/parok_*.tsv x konkordancia/TAHOT_kivonat.tsv x adat/forditasok.tsv | ts=2026-11-01 15:51.

| adag (sorrend) | szócikk | Károli-pár | % | indulhat |
|---|---|---|---|---|
| 13. (5671–7922 a script szerint; az adag 7921-ig tart) | 2252 | 2249 | 100% | igen |
| 14. (7923–8073) | 151 | 75 | 50% | nem (a DT-F38u előtt) |

**14. adag, DT-F38u (az orkesztrátor döntése a felhasználó megbízásából, 2026-11-01).** A script a 0 TAHOT-gyakoriságú Strongokat a nevezőből kihagyja és külön oszlopban mutatja (`--tol 7922 --adagok 1`, ts=2026-11-01 16:09): 152 szócikk, **87** nulla-gyakoriságú, nevező 65, Károli-pár 65, **100%**. (Az orkesztrátor üzenete 76 nulla-gyakoriságú Strongot említett; a script a 7922–8073 tartományban 87-et talál — a különbség okát nem vizsgáltam, a 100% mindkét számmal fennáll, mert a nem nulla-gyakoriságúak mind párosítottak.) A 13. adagban nulla-gyakoriságú Strong nincs.

## 1. Tábla-Δ

| tábla | alap (`18d0dcb9`, a `main` hegye az ág indulásakor) | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|
| `adat/forditasok.tsv` (adatsorok) | 23847 | **+6400** | 6400 / 0 |
| `naplok/EMELES_munka.tsv` | — | +6400 | 6400 / 0 |
| `naplok/FORDITAS_kisnagybetu_csere.tsv` | — | 0 | — |
| `naplok/BDB_FORDITAS_hibas.tsv` | — | 0 (nem került hibás-listára szócikk) | — |
| minden más `adat/` tábla | — | 0 | — |

A 6400 sor: 2401 szócikk szakaszos (`sz<n>` sorok, 6396 sor), 2 szócikk (H0747, H4123 — a szakasztáblán kívül) a régi `teljes` úton (2 sor), mind `sonnet` / `claude-sonnet-5-5` / 2026.11.01, `megjegyzes`: „API Batch (effort=high, <n>. próba)”. Törölt vagy módosított meglévő sor nincs (0 törlés). `kezi` sorhoz nem nyúltam. A régi `teljes` sor `elavult`-ra állítása nem volt szükséges (az adag Strongjainak nem volt korábbi sora).

## 2. A Batch API-út — mért költség és kapu-eredmény

Proveniencia: `forditas/bdb_api/adag13/futasnaplo.tsv` (kérésenként: bemeneti / cache / kimeneti token, `stop_reason`, USD Batch-áron: bemenet 1, kimenet 5, cache-olvasás 0,10, 1 órás cache-írás 2,00 USD/M token) | `eszkozok/bdb_api_koteg.py` | ts=2026-11-01.

| szakasz | kérés | Strong | bemenet (M token) | kimenet (M token) | USD |
|---|---|---|---|---|---|
| 1. csomag: egy Strong/kérés, 1 órás cache | 450 | 450 | 7,01 | 0,34 | 11,674 |
| javító batch (1. csomag) | 8 | 8 | — | — | 0,06 |
| B-próba (3 kérés, ~25 Strong/kérés) | 3 | 75 | 0,16 | 0,057 | 0,451 |
| B-fő (63 kérés) | 63 | 1878 | 3,85 | 1,22 | 9,955 |
| javító batch (B + próba, A-stílusú, cache nélkül) | 43 | 43 | — | — | 1,08 |
| **összesen** | **567** | **2403** | | | **23,22 USD** |

(A tábla a futásnapló összegei: A-p1 450 kérés 11,674; p2 51 kérés 1,140; B 66 kérés 10,406; összesen 23,2201 USD. A javító sorok bontása a két javító batch között kerekített.)

- **USD / forráskarakter:** 23,22 USD / 571 310 karakter (a sorrendtábla `karakter` oszlopa, 13.+14. adag) = **0,0000406 USD/karakter**; csak a 13. adagra (499 871 karakter, a 14. adag aránya nélkül) ugyanez az arány ~20,3 USD. Szócikkenként átlag 0,0097 USD.
- **Hátralék:** nincs. A sorrendtábla 8073 sorából mind kész (a halmazkülönbség 0); a 14. adag volt az utolsó. Hátralékra vetítés ezért nem értelmezhető; a 14. adag költsége 1,2 USD körüli becslés volt (A: 3,0–3,3 USD).
- **A/B összevetés (becslés ↔ mért):** a hálózat nélküli vetítés (`naplok/BDB_API_koltseg_valtozatok.py`, becslés, `manual`) a 13. adagra A: 43,7–48,4 USD, B: 17,3–17,6 USD volt; a mért B-út a 13. adag maradékára + a 14. adagra (1953 Strong) 10,41 USD, a teljes futás (A-csomag + javítók + B) 23,22 USD. A B-út Strongonként ~0,0053 USD, az A-csomag (cache-sel) 0,0259 USD/kérés: a kérésenkénti állandó prompt (~15 ezer token) felosztása ~5-szörös megtakarítás. A cache az A-úton rontott: 4,23 M token cache-írás (8,5 USD) mellett csak 1,41 M token olvasás.
- **Plafon:** az 1. csomag után a plafon 15 USD volt (11,67 USD mért); a felhasználó a B-útra +20 USD-t hagyott jóvá (31,67 USD összesen, DT-F38y utáni jóváhagyás, 2026-11-01). A tényleges költség 23,22 USD, a plafon alatt.
- **Kapuhiba az 1. próbán:** 54 / 2403 Strong = **2,2%** (1. csomag 8/450 = 1,8%; B-próba 3/75 = 4,0%; B-fő 43/1878 = 2,3%). A 2. próbán (javító batch a kapu hibaüzenetével) 49 / 54 átment; **5 Strong másodszor is bukott**, mind kapu-hamis pozitív (l. 3.). `naplok/BDB_FORDITAS_hibas.tsv`-be egyik sem került (mind felülbírálva).
- **Strong-határ a B-úton:** a 66 B-kérés 1953 Strongjából 0 hiányzott a válaszból; egy B-kérés ért `max_tokens`-hez (B064, egyetlen Strong: H4984, 20 055 gondolkodási token a 27 295 kimeneti tokenből), az A-stílusú javító kérésben fordult le. A `⟦n⟧` helyőrzők az egy Strongon belüli számozással tartottak; egy esetben ismeretlen sorszám („ismeretlen helyőrző”) került a válaszba (a kapu hibaüzenetet adott, az eszköz javítva: IndexError helyett javítandó).

## 3. Kapu-felülbírálások (DT361, a 12. adag mintájára)

Öt Strongot érintett, mindegyiknél a másodszori bukás hamis pozitív, hű fordítással, a forrásidézet megadásával; a `--kapu-felulir <kapu> --dontes DT361` mintát az `emeles.kapu_felulir` kapuellenőrzése (pontosan egy bukott kapu, DT-sor létezik) engedi át, a `megjegyzes` mezőbe kerül.

| Strong | kapu | forrásidézet és indok |
|---|---|---|
| H2202 | 8_idezojel | forrás: „Za±ferâne, „umƒ and Hamath” — az OCR-maradvány „ (U+201E) pár nélkül áll; a fordítás hűen hordozza: „Za±ferâne, „umƒ és Hamát között”; a ` (' perhaps ')` zárójeles idézet a fordításban „(talán)”. |
| H3901 | 9_tagolas | forrás: „A ᵐ5^L read is ⟦4⟧, whence Bu^RS 103 ⟦5⟧” — az „5” a ᵐ5^L sziglum része, nem jelentéssorszám; a fordításban „A ᵐ5^L olv.” változatlanul. |
| H0435 | 5_terminologia | forrás: „proper name of 6th month, Aug.—Sept. Neh 6:15” — a „Sept.” a szeptember rövidítése, nem a Septuaginta. |
| H2954 | 5_terminologia | forrás: „Guy^JAS 1883, Août-Sept. 189” — a „Sept.” folyóirat-hivatkozásban szeptember. |
| H1306 | 5_terminologia | forrás: „Vog^JAs 1883, Août. Sept. 153” — a „Sept.” folyóirat-hivatkozásban szeptember. |

A felülbírálás-lista: `forditas/bdb_api/adag13/felulir.tsv`.

## 4. Commitonkénti bontás

| commit | tartalom | `forditasok.tsv` új sor |
|---|---|---|
| F38.454 | `eszkozok/bdb_api_koteg.py`, `eszkozok/teszt_bdb_api_koteg.py`, DT-F38y, brief-jelölések (#38 API-út, #136 okafogyott) | 0 |
| F38.455 | az 1. csomag (450 kérés) beküldve | 0 |
| F38.456 | az 1. csomag begyűjtve és kapuzva (11,67 USD, 8 javítandó) | 0 |
| F38.457 | az 1. csomag 442 átment Strongja rögzítve; javító batch; költségvetítés | +931 |
| F38.458 | a javító batch 8 Strongja rögzítve | +19 |
| F38.459 | B-út az eszközben; DT56 nulla-gyakoriságúak külön oszlopban; DT-F38u | 0 |
| F38.460 | B-próbacsomag (3 kérés, 75 Strong) beküldve | 0 |
| F38.461 | B-próba begyűjtve (0,45 USD) | 0 |
| F38.462 | a B-út maradéka (63 kérés) beküldve | 0 |
| F38.463 | B-fő begyűjtve és kapuzva; javító batch (43) | 0 |
| F38.464 | rögzítés: 2403 Strong, 5 felülbírálás | +5450 |
| **össz.** | | **+6400** |

(A rögzítő lépések a munkatáblát és az `adat/forditasok.tsv`-t újraírták az addig rögzített sorokkal azonos tartalommal; a „+” a `git diff --numstat` alapja szerinti új sor, a törlés 0.)

## 5. Ellenőrzések

- `python eszkozok/ellenoriz.py`: 0 SÉRTÉS (RENDBEN 18 | SÉRTÉS 0 | KÉZI 2 | JELENTÉS 4), a rögzítés után.
- `python eszkozok/teszt_bdb_api_koteg.py`: 16 teszt OK (hamis hívós folyamat, plafon, B-prompt, B-szétbontás).
- Lefedettség: a `naplok/BDB_FORDITAS_sorrend.tsv` mind a 8073 Strongja szerepel az `adat/forditasok.tsv`-ben `sonnet` állapottal (halmazkülönbség: 0; ebből 13. adag 2251, 14. adag 152).
- A `forditas/bdb_api/adag13/` mappa: batch-azonosítók (`batchek.tsv`), nyers válaszok (`valaszok.jsonl`), kapu-eredmény (`kapu_eredmeny.jsonl`), költségnapló (`futasnaplo.tsv`), felülbírálások (`felulir.tsv`); a prompt-hash-ek a `csomag_*.txt` fájlokban.
- A prompt a kérésenkénti állandó szabály-részt (prompt v5, terminológia, Károli-tábla) a B-úton egyszer tartalmazza; a Strongonkénti rész az adatblokk és a tokenes forrás; a **szabálytartalom változatlan** (`emeles.prompt_epit`), a kimenet-szakasz JSON-tömbre módosult. A héber–görög szakaszok `⟦n⟧` helyőrzővel mentek (a Code-os út `_szakasz_hely.txt` mintája), visszaállításuk betűhű.

## 6. Nyitott kérdések

- Az adatblokk proveniencia-sora időbélyeget hordoz, ezért a prompt két felépítése között a szöveg ts-ben eltér; ezért az eszköz a felépített tervet a repón kívüli gyorsítótárba teszi (`PARDES_BDB_CACHE`, alapérték `%TEMP%/bdb_api_cache`), és a prompt SHA-256 előtagját a `csomag_*.txt` rögzíti.
- Az orkesztrátor 76, a script 87 nulla-gyakoriságú Strongot talál a 14. adagban (l. 0.) — nem vizsgáltam.
- A BDB-fordítás a sorrendtábla szerint kész; az Mz zárás (terminológiai javaslatok, szúrópróba, hibás-lista összesítés) a felhasználó jelzésére indul.
