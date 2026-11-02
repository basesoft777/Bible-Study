# FP3 napló — F27 (Thayer mérő adag, API Batch)

*Modell: claude-sonnet-5-5 (a brief `modell: sonnet`-jével egyezik). Ág: `claude/f27-thayer-fp3-2d0652` (main `841d7a20`). Számok forrása: `naplok/FP3_M0.py` futásai; proveniencia: scope=teljes Thayer | forras=naplok/FP3_M0.py, eszkozok/thayer_api_koteg.py szaraz/lista | ts=2026-11-02.*

## M0 — felmérés

### 1. Előfeltételek (E1–E6)

| # | Állapot (mért) |
|---|---|
| E1 | `thayer_api_koteg.py` a main-en (`841d7a20`), `--onteszt` lefut; `lista`: 5 426 Strong, 5 413 fordítandó, 13 `kesz` |
| E2 | `grep -c DT329 eszkozok/thayer_jelolt/forditas.py` = 1 — teljesült |
| E3 | sigla: 91 `besorolt`, 164 `jelolt` sor (l. 4. pont) |
| E4 | `teszt_lanc.py`: 40 teszt, 1 bukás (N66, ismert) |
| E5 | `Sir c:v` előfordulás a forrásban: 536 |
| E6 | `feladatok.py fuggesek`: `KIZAR 27↔38`, `KIZAR 154 27`, `FUGGES 27 154` — a `beir` előtt a #38/#154 adag nem futhat |

### 2. Lánc-próba szárazon a teljes Thayeren

| Lépés | Fut-e | Eltérés |
|---|---|---|
| `lista` | igen | 5 413 fordítandó / 13 kesz |
| kérések összeállítása (`kerelmek_strongra`, minden fordítandó Strong) | igen, **0 hiba** | 5 437 kérés, 9 többcsoportos Strong; forrás 4 470 001 karakter (tokenes); prompt összesen 188 641 492 karakter (átlag 34 695), 92 mp |
| csomagolás | igen | 13 csomag × ≤450 kérés |
| teljes dry-becslés (manual) | — | 119,32 USD (Batch-ár, cache nélkül; a brief 119,81-e a 17 093 szakaszra) |
| kész sorok újrakapuzása (`kapu`) | igen | 13 szakaszos `sonnet` Strong: 12 átment, 1 bukott: **G0282 `5_terminologia` SÉRTÉS** („Heb. -> héb. hiányzik”). `kezi` / `opus` sor nincs a szakaszos (`sz<n>`) sorok között, ezeket a menet nem is kapuzta |

Az újrakapuzás G0282-jelzése a kész sorokat érinti (nem az M1 adagját); a kapu azóta szigorodott vagy a sor régi. Nem javítom (a kész `sonnet` sorhoz a menet nem nyúl).

### 3. Könyv- és hivatkozásfedés

c:v előtti szó a forrásban: 70 058 előfordulás, 420 különböző alak; leképezett könyvnevek találata 66 576. **Nem leképezett: 311 alak, 3 489 előfordulás** (első 15): Antiquities 534, Polybius 328, Herodotus 254, Diodorus 229, Iliad 179, Cyril 146, Thucydides 142, **1 Cor. 112**, Odyssey 106, 3Macc. 103, 1 Esdr. 59, Apion 58, Barnabas 58, Hell. 52, Antoninus 41. Ezek javarészt klasszikus szerzők/művek (nem bibliai könyv); a `11_konyvek` kapu a leképezettekre vonatkozik, a többi szó szerint marad. Külön sorok: `Sir c:v` 536 (E5); Kelemen-hivatkozás: a „1 Cor. c, v” vessző-alak 0, a pontos alakú `1 Cor.` 112, `2 Cor.` 7 a nem leképezettek között (kérdés a DT-F27b-be); klasszikus szerzők: Josephus 838, Philo 426, Lucian 262, Antoninus 47.

### 4. Sigla-fedés (E3)

| Tábla-állapot | Előfordulás a teljes Thayerben | Az M1 adagban (9 Strong) |
|---|---|---|
| `besorolt` | 69 835 | 2 352 |
| `jelolt` | **5 758** | **79** (38 sigla-sor) |

A `jelolt` sziglákat a `16_sigla` kapu nem védi; a jóváhagyás a felhasználóé (DT335 (3)).

### 5. Terminológia

`adat/terminologia.tsv`: 84 sor (Thayer-relevánsak: spirit, soul, cf., cl., pass., sc., Sept., Heb., i. e., etc. …). Az egyszerű szógyakoriság alapján sor nélküli leggyakoribb angol szavak (javaslatlista; a fájl nem változik): grammar 2 938, aorist 1 821, passive 1 378, genitive 937, infinitive 659, participle 600, dative 548, plural 716, future 723, present 713, middle 577, metaphorically 391, absolutely 359. A „Sept.” mint pont nélküli szó a keresésben „sept” (1 664) — a sor megvan, a mérés durva.

### 6. Sorrend

`naplok/FP3_sorrend.tsv`: 5 413 sor (kesz kihagyva), Károli ÚSZ Strong-gyakoriság (a `parok_<ÚSZ-könyv>.tsv` sorai a Strongra) csökkenő, egyenlőségnél Strong-szám; 163 Strong ÚSZ-gyakorisága 0 (a végén).

### 7. Adagterv

| Adag | Strong | Karakter | Szakasz |
|---|---|---|---|
| 1 (M1) | 9 | 159 666 | 307 |
| 2 | 45 | 502 920 | 905 |
| 3 | 91 | 501 235 | 849 |
| 4 | 170 | 501 475 | 983 |
| 5 | 303 | 501 587 | 1 372 |
| 6 | 546 | 500 466 | 1 888 |
| 7 | 803 | 500 655 | 2 378 |
| 8 | 1 239 | 500 150 | 3 101 |
| 9 | 1 515 | 500 064 | 3 581 |
| 10 | 692 | 232 680 | 1 658 |

*Megfigyelés (mérés, nem ítélet):* az M1-adag a 9 leggyakoribb görög szó (καί, αὐτός, ὁ, σύ, ἐν, δέ, ὅς, εἰμί, εἰς): nagy, kevés Strongos szócikkek (4 többcsoportos), tehát a **hosszkategóriás kivetítés** a kisebb szócikkek tartományában (a Strongok zöme) az M1-ből nem fedhető le jól. Ezt a ⛔ M1 jelentésben jelzem.

### M0 összegzés

Blokkoló hiány nincs: az előkészítés a 5 413 Strongra hibátlan, a kötegelő száraz futása lefut. Megállás az M0 után nem kell.

### M1 száraz becslés (manual, Batch-ár, cache nélkül)

- M1 adag (9 Strong, 21 kérés, 161 115 tokenes forráskarakter): **1,17 USD**
- aranyminta (5 Strong, 7 kérés, 34 640 karakter): **0,30 USD**
