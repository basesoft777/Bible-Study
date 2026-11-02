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

## M1 — mérő adag (API, Batch)

*Menetrend: 2026-11-02. Modell a Batch-válaszból: claude-sonnet-5-5 (a `forditasok.tsv` `modell` mezője ezt viseli).*

### Az adag összetétele (az orkesztrátor döntése, 2026-11-02: a brief egyeztetett bővítése)

A brief szerinti első ~150 000 karakter (a sorrend első 9 Strongja, a „funkciószavak”: καί, αὐτός, ὁ, σύ, ἐν, δέ, ὅς, εἰμί, εἰς; 159 666 kar.) mellé **rétegzett minta**: `naplok/FP3_M0.py minta`, `random.Random(27)`, hosszkategóriák a Strong forráskarakterszáma szerint (kicsi <500, közepes 500–2 999, nagy ≥3 000), a sorrend többi Strongjából, kategóriánként keverve; célszám 11 / 9 / 5, a pótlás összesen legfeljebb 30 000 karakter (a „nagy” kategóriából 3 Strong fért bele). Lista és kategória: `naplok/FP3_m1_strongok.tsv` (a kötegelő bemenete: `FP3_m1_strongok.txt`). Eredmény: **32 Strong** (9 funkciószó + 11 kicsi + 9 közepes + 3 nagy), **44 kérés**, 191 414 tokenes forráskarakter. Az aranyminta külön batch-ben fut (`FP3_arany_strongok.txt`: G0282, G1941, G1944, G4151, G5590; 7 kérés, 34 640 kar.; adagszám 99); a munkatáblába és a `forditasok.tsv`-be nem írtam.

### Költségmérés (a kötegelő `futasnaplo.tsv`-je, USD, Batch-ár, cache nélkül; mért érték)

| | kérés | forráskar. | bemenet token | kimenet token | USD | becslés (manual) |
|---|---|---|---|---|---|---|
| M1 1. kör | 44 | 191 414 | 1 456 418 | 364 994 | 3,2814 | 1,73 (**+90%**) |
| M1 javító kör | 25 | — | 1 162 380 | 252 332 | 2,4240 | — |
| **M1 összesen** | 69 | | 2 618 798 | 617 326 | **5,7054** | |
| aranyminta 1. kör | 7 | 34 640 | 258 653 | 66 700 | 0,5922 | 0,30 (+97%) |
| aranyminta javító kör | 7 | — | 282 394 | 46 477 | 0,5148 | — |
| **aranyminta összesen** | 14 | | | | **1,1069** | |

**Plafon (M1: 5 USD, aranyminta: 2 USD):** az M1 összköltsége **5,7054 USD: a plafont 0,71 USD-vel (14%-kal) átlépte**. A kötegelő a plafont a beküldés előtt a saját becslésével ellenőrzi (ez kb. 40–50%-kal alacsonyabb a mértnél), ezért a javító batch átment; a mért költség csak utólag ismert. Az orkesztrátornak jelezve; további költség nincs. Aranyminta: 1,11 USD, a plafonon belül.

**Hiba, őszintén:** a begyűjtés és kapuzás parancsláncához tévedésből hozzáfűztem a `javit --plafon 5` hívást, így az M1 javító batch (25 kérés) a költségeltérés jelzése előtt elindult. Az orkesztrátor utólag jóváhagyta a folytatást; a batch-et nem szakítottam meg. Az aranyminta javító körét már csak az engedélye után indítottam.

### Kapu-eredmények (M1; a kötegelő `kapu_eredmeny.jsonl`-je)

| | Strong |
|---|---|
| 1. próba: átment | 19 |
| 1. próba: javítandó | 13 |
| javító kör után átment | 9 (a 13-ból) |
| **kétszer bukott** (nem rögzítve; `bukottak.tsv`) | **4**: G3588, G1722, G1510, G1519 |
| **rögzítve és beírva** | **28 Strong, 185 szakaszsor** |

1. próbán jelzett kapuk (Strongok száma; egy Strong több kaput is sérthet): `8_idezojel` 8 (G2532 G0846 G3588 G4771 G1722 G1161 G1510 G4594) · `11_konyvek` 5 (G0846 G3588 G1161 G1519 G1632) · `16_sigla` 5 (G2532 Homer; G0846 G2281 G1131 G1097 Sept.) · `9_tagolas` 4 (G0846 G1722 G1510 G1519) · `5_terminologia` 2 (G0846 „the Spirit”, G1131 „Heb.”) · `4_formazas` 1 (G1510).

Téves riasztás / valódi hiba (a nyers válaszok elolvasása nélkül, a hibaüzenetekből; jelölve: manual): a `8_idezojel` üzenetei („forrás 0 pár, fordítás n pár”) a forrás ASCII-idézőjel-számolásából adódnak, téves riasztás gyanú; a `11_konyvek` hibái (`Makk`, `Tób`, `Bölcs`) az apokrif könyvek hiányos leképezéséhez köthetők (l. M0 3. pont), kapu-/normalizálóhiba gyanú; valódi fordítási hiba a `16_sigla` („Sept.”, „Wis.” kibontatlan), a `5_terminologia` („Heb.” → „héb.”) és a `9_tagolas`.

Kétszer bukottak: G3588: `8_idezojel` + `11_konyvek` (1Makk/2Makk); G1722 és G1510: **max_tokens**, a kérés nem adott használható választ (a nagy, sok szakaszos szócikkek kimenete a limit fölé nőtt, a javító körben is); G1519: `11_konyvek` (Bölcs.) + `16_sigla` (Wis.).

### Beírás

`beir --regi-elavult --kezi-marad --allapot sonnet` a 28 Strongra: `adat/forditasok.tsv` +185 sor, 0 törölt vagy módosított sor; minden új sor `allapot=sonnet`, `modell=claude-sonnet-5-5`, `datum=2026.11.02`, `jelentes_szam=sz<n>`. Beírás előtt `origin/main`-nel összevetve: az `adat/forditasok.tsv` a main-en nem változott (bájtazonos a merge előtt és után); #38 és #154 nem fut (orkesztrátor).

Ellenőrzések: `eszkozok/ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba; `teszt_forditas_kapuk.py` OK; `teszt_lanc.py` 39/40 (N66). **Bukó tesztek:** `teszt_bont.py` 2 (`test_ellenoriz`, `test_forras_javit_ellenoriz`: a forrás-javítás 15 lyuka miatt a vizsgált parancs kilépési kódja 1) és `teszt_vers_jelentes.py` 1 (`test_ellenoriz`: Károli-vers nélküli sor ÚSZ 29, ÓSZ 12). A menet ezeket a táblákat nem módosította (a diffben csak a `forditasok.tsv`, a munkatábla, a bukottak tábla és `naplok/`, `forditas/thayer_api/` szerepel), tehát a bukás előzetes; a main-en külön nem futtattam (jelölve: manual).

### 5 véletlen Strong

`naplok/FP3_veletlen.md` (seed = 27, a beírt nem funkciószó Strongok hossz szerinti harmadaiból: 2 rövid, 1 közepes, 2 hosszú): G4978, G4018, G4309, G1248, G2281. Forrás és fordítás egymás alatt, szakaszonként.

### Aranyminta-összevetés

`naplok/FP3_arany.md` (generálja: `naplok/FP3_arany.py`); a három szöveg (forrás, `kezi`, Sonnet) teljes terjedelemben egymás alatt. Mérhető jellemzők, ítélet nélkül:

| Strong | szakasz | forrás kar. | `kezi` kar. | Sonnet kar. (token nélkül) | c:v forrás / `kezi` / Sonnet | kapu |
|---|---|---|---|---|---|---|
| G0282 | 7 | 702 | 736 | 740 | 1 / 1 / 1 | átment (2. próba) |
| G1941 | 7 | 3 746 | 4 601 | 3 991 | 44 / 44 / 44 | átment (2. próba) |
| G1944 | 2 | 337 | 339 | 342 | 9 / 9 / 9 | átment (2. próba) |
| G4151 | 17 | 23 726 | 24 473 | — | 517 / 515 / — | **javítandó** (max_tokens, nincs válasz) |
| G5590 | 10 | 5 950 | 6 055 | 6 112 | 121 / 121 / 121 | átment (2. próba) |

Feltűnő eltérések (felsorolva, ítélet nélkül): a G4151-re az API nem adott használható választ (17 szakasz, 23 726 karakter, mindkét körben max_tokens); a G1941 `kezi` szövege 23%-kal hosszabb a forrásnál, a Sonnet-é 6,5%-kal; a G4151 `kezi` sora 515 igehelyalakot visz a forrás 517-éből. A tartalmi összevetés (szóválasztás, terminológia) a felhasználóé.

### Kivetítés a teljes Thayerre (mért tokenekből; `naplok/FP3_koltseg.py`)

*A kötegelő becslője (`TOKEN_KARAKTER` 2,8; gondolkodási token 1 500/kérés) a mérthez képest alulbecsül; nem írtam át (nincs az `ir` mezőben; N-F27a).*

Illesztés az 51 első körös kérésre (M1 + aranyminta), legkisebb négyzetekkel: **bemenet = 17 136 token/kérés + 3,721 token/forráskarakter**; **kimenet = 1 134 token/kérés + 1,654 token/forráskarakter**. A kérésenkénti 17 136 bemeneti token a prompt állandó része (terminológia, Károli-tábla, szabályok).

| Hosszkategória (a teljes listán) | kérés | forráskar. | 1. kör, USD (mért modell) | javító/1. kör USD-arány a mintában |
|---|---|---|---|---|
| kicsi (<500 kar.) | 3 353 | 894 315 | 87,19 | 0,00 (11 Strong, javítás nem kellett) |
| közepes (500–2 999) | 1 845 | 1 983 756 | 65,86 | 0,30 (9 Strong; 3 kérés javítva) |
| nagy (≥3 000) | 239 | 1 522 827 | 23,71 | 0,43 (3 Strong; 2 kérés javítva) |
| funkciószó (a 9 M1-Strong; külön kategória, a teljes listán a 3 kategória részei) | 21 | 161 115 | 2,41 (mért) | 0,92 |
| **1. kör összesen** | 5 437 | 4 400 898 | **176,76** | |

A javító kör kategóriánként mért arányával: 87,19 + 65,86 × 1,30 + 23,71 × 1,43 = **206,7 USD** (alsó becslés). Az M1 egészére mért javító/1. kör arány (0,74 USD, 0,57 kérés) alkalmazásával: **310,9 USD** (felső becslés; a két max_tokens-hibás nagy Strong újrapróbái is benne vannak).

**A teljes Thayer kivetített költsége: kb. 207–311 USD (a nagy kategóriára 3, a kicsire 11 Strong a minta: kis minta).** A kötegelő 119,32 USD-s becslése ennek a fele sem. Becslés, nem mért érték; jelölve. A költség ~86%-a a kérésenkénti állandó (prompt) rész: 5 437 kérés × 17 136 bemeneti token ≈ 93 millió token. A kicsi Strongok fajlagosan ötszörösen drágábbak a funkciószavaknál (0,071 vs 0,015 USD / 1000 forráskarakter).

### Megfigyelések (a DT-F27b és az N-F27a… tételek bemenete)

1. A kötegelő költségbecslője kalibrálatlan (N-F27a); a plafon beküldés előtti becslésre épül, a mért költség átléphette (N-F27b).
2. A max_tokens-hiba a nagy szócikkeknél a javító körben is megismétlődött (G1722, G1510; aranyminta: G4151): a nagy szócikkek csoportosítása, max_tokens (N-F27c).
3. Prompt-gyorsítótár: a kérésenkénti 17 136 bemeneti token a legnagyobb megtakarítási lehetőség; a Batch-úton a kötegelőben ki van kapcsolva (BDB-tapasztalat); a #7 előtt mérendő (N-F27d).
4. `11_konyvek`: az apokrif könyvek leképezése hiányos; a `1 Cor.` (112) és `Sir` (536) a #7 bemenete (N-F27e).
5. `16_sigla`: 5 758 `jelolt` sigla-előfordulás a teljes Thayerben (79 az M1-ben); a „Sept.” és „Wis.” kibontása gyakran hiányzik; jóváhagyás a felhasználóé.
6. A G0282 kész `sonnet` soránál az újrakapuzás `5_terminologia` SÉRTÉST ad („Heb. → héb. hiányzik”); ebben a feladatban nem javítottam, csak listázom.

## Javaslat a #7 (Thayer éles) briefjéhez (nem brief; futtatni nem kezdtem)

- **Hatókör:** a `naplok/FP3_sorrend.tsv` 5 413 − 28 (beírt) − 9 (az M1-ben kétszer bukott Strongok közül 4) = a még hátralévő Strongok; adagok a sorrend szerint, kb. 500 000 forráskarakter; adagonként új session.
- **Előfeltételek a #7 előtt (a DT-F27b (b) döntésétől függően):** N-F27a (becslő kalibrálása a mért modellre), N-F27b (mért futó összeg a plafon-ellenőrzésben), N-F27c (max_tokens a nagy szócikkeknél), N-F27d (gyorsítótár mérése), N-F27e (apokrif-könyvek, `1 Cor.`, `Sir`, sigla-jóváhagyás).
- **Költség:** mért kivetítés 207–311 USD a teljes Thayerre (l. fent); adagonként plafon = az adag mért-modell szerinti becslésének 1,5-szerese, mért futó összeggel.
- **Lépések adagonként:** `szaraz` → plafon → `bekuld` → `allapot` (5 perces ciklus) → `begyujt` → `kapuz` → `javit` (1 kör) → `rogzit` → `beir --regi-elavult --kezi-marad` → adagjelentés; a kétszer bukottak a `bukottak.tsv`-be.
- **Nyitott a felhasználóra:** DT-F27b (a)–(c).
