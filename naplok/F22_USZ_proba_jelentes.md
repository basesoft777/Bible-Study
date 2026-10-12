# F22_USZ_proba_jelentes.md — a 22.8 ÚSZ-próbacsomag összesítője (Filem, 2Ján, 3Ján, Júd)

*A számok szkriptkimenetből jönnek: a négy könyvjelentés (`naplok/F22_Filem_jelentes.md`, `F22_2Jan_jelentes.md`, `F22_3Jan_jelentes.md`, `F22_Jud_jelentes.md`), a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` (`futas = api_termeles/high/<könyv>`; `cimke = filem, 2jan, 3jan, jud`), valamint a `konkordancia/Karoli_1908.tsv` és `konkordancia/TAGNT_kivonat.tsv` versenkénti számlálása. Ág: `claude/amazing-mayer-t276r0`. Módszer: D44 (csak Sonnet, Message Batches API, `effort=high`, `prompt_v3`, 10 verses kötegek, soros futtatás). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd itt a próbacsomagot”).*

## 1. A görög egységár és a vetítés (22.8 7. pont, a)

| könyv | Károli-vers | a modellhez | hívás | költség (USD) | USD/vers |
|---|---|---|---|---|---|
| Filem | 25 | 25 | 3 | 0.0999 | 0.0040 |
| 2Ján | 13 | 13 | 3 | 0.0832 | 0.0064 |
| 3Ján | 15 | 14 | 2 | 0.0764 | 0.0055 |
| Júd | 25 | 25 | 4 | 0.1656 | 0.0066 |
| **össz** | **78** | **77** | **12** | **0.4251** | **0.0055** |

A próba a könyvplafonok alatt maradt (mind a négy könyvnél az `api_koteg.py` alsó határa, 1,00 USD a tényleges plafon). A futásnapló `futo_osszeg_usd` utolsó sora: **86,3698 USD** a 110 USD-ből (a kiindulás 85,9447, D43); a **maradék keret 23,6302 USD**.

**Vetítés a teljes ÚSZ-re.** Módszer: egyszerű arány, nem illesztés; az alap a próba összköltsége (0,425133 USD) a modellhez ment 77 versre, illetve 1 311 Károli-szóra (a 3Ján 1:15 12 szava nélkül). A teljes ÚSZ a `Karoli_1908.tsv` szerint 7 954 vers, 142 048 Károli-szó (17,9 szó/vers; a próbáé 17,0).

| alap | teljes ÚSZ (7 954 vers) | a hátralevő 23 könyv (7 876 vers) |
|---|---|---|
| versarányos (0,005521 USD/vers) | 43,92 USD | 43,49 USD |
| szóarányos (0,0003243 USD/Károli-szó) | 46,06 USD | 45,63 USD |

A hátralevő 23 könyv vetített költsége (43,5–45,6 USD) **kb. a kétszerese a maradék keretnek** (23,63 USD). A vetítés bizonytalansága nagy: a négy könyv egységára 0,0040 és 0,0066 USD/vers között szór, a javító kör aránya könyvenként 0 és 1 köteg között; a próba négy rövid levél, elbeszélő próza (evangéliumok, ApCsel) nincs benne. A keretből a maradék kb. a hátralevő versek felére elég (versarányosan 4 280 vers).

## 2. Kapuhiba (b)

| könyv | első próbára | végleg | javító kör |
|---|---|---|---|
| Filem | 0/25 | 0 | nem kellett |
| 2Ján | 3/13 | 0 | 1 köteg (k002) |
| 3Ján | 0/14 | 0 | nem kellett |
| Júd | 5/25 | 0 | 1 köteg (k003) |
| **össz** | **8/77 (10,4%)** | **0** | 2 köteg |

**Mind a 8 első próbás hiba formátumhiba:** a két javító körös köteg egésze érvénytelen JSON volt az 1. próbán (2Ján k002, 3 vers, és Júd k003, 5 vers; a hiba mindkettőnél „Extra data: line 3 column 1”, vagyis a JSON-tömb után további szöveg; `f22/api_termeles/high/_munka/2Jan_k002.json`, `Jud_k003.json`). Versenkénti tartalmi kapuhiba (érvényes JSON, hibás párosítás) **0** volt. Ugyanez a minta a kilenc kis ÓSZ-könyvben is előfordult (négy egész formátumhibás köteg, 33 vers; első próbás kapuhiba ott 47/797, 5,9%, D43).

## 3. A `[nem TR]` tokenek (c, P4)

| könyv | `[nem TR]` | `forditatlan` | párosított |
|---|---|---|---|
| Filem | 9 | 9 | 0 |
| 2Ján | 5 | 5 | 0 |
| 3Ján | 9 | 9 | 0 |
| Júd | 28 | 28 | 0 |
| **össz** | **51** | **51** | **0** |

Mind az 51 a várt módon `forditatlan` (a `prompt_v3` K szabálya); a száraz próba előre mért száma (9/5/9/28) egyezik.

## 4. A 3Ján 1:15 útja (d)

- **Minta:** a `sonnet_koteg.py minta` az eredeti vers nélküli versek közé sorolja, a modellhez nem kerül (`f22/minta_3Jan.tsv`: 14 vers + 1 kimaradt).
- **Kapu:** nem érinti (nincs kérés).
- **Egyesítés:** az `egyesit.py` a 12 Károli-szavát `fuggoben` állapotban, link nélkül írja a `szavak_3Jan.tsv`-be; a `parok_3Jan.tsv`-ben nincs sora.
- **Átnézés:** `naplok/F22_3Jan_atnezes.tsv` 1 sor („nincs eredeti vers a TAGNT-ben (versszámozás-eltérés)”). A szöveg általános; a valódi ok a kivonat hiánya (a görög szöveg, εἰρήνη σοι …, a `TAGNT_kivonat.tsv`-ben sehol nincs), l. N-F22b és a 3Ján-jelentés 3. szakasza.

## 5. Régi arany (e)

A négy könyvben a `Karoli_Strong_kivonat.tsv`-nek 0 hármasa van: az egyezés **nem mérhető**. Nem pótoltuk.

## 6. Egyéb

- **P2:** a `strong` a TAGNT-ből, gépi ellenőrzéssel (`egyesit.py --konyv <könyv> --ellenoriz`: „rendben” mind a négyben); a proveniencia-sor a `konkordancia/TAGNT_kivonat.tsv`-t és „a TAGNT-ből” szöveget hordozza (az `egyesit.py` F22.8.1 javítása; az ÓSZ-kimenet bájtra változatlan: Sir, Mal, Hós újraépítve).
- **P3:** a `f21p/prompt_v3.md` SHA-256-ja a futás végén `5937e6ab…`, egyezik a `f21p/prompt_v3.sha256`-tal; a fájl a menetben nem változott; a futásnapló mind a 12 sorában `prompt_sha256_12 = 84f12ca7aafb`, ugyanaz, mint a korábbi API-menetekben.
- **Batch-várakozás:** a Filem batch-e (05:47 UTC) kb. 2 óráig `in_progress` volt, kérés nélküli hibával nem; egy közben indított szinkron próbahívás 1,6 mp alatt válaszolt (a modell és a kulcs rendben). A többi hat batch 2–3 perc alatt végzett. A próbahívás költsége (5 kimeneti token) nem került a futásnaplóba.
- **Mellékes lelet (nem e tétel dolga):** a main-en a `parok_2Moz.tsv`, `szavak_2Moz.tsv`, `parok_Job.tsv`, `szavak_Job.tsv` proveniencia-fejléce eltér attól, amit az `egyesit.py` ma írna (a `forras` listában a már üres versmegfeleltetési táblák); az adatsorok azonosak. A módosítás nélkül is így van (ellenőrizve).

## 7. ⛔ Megállás — a felhasználó döntése

1. Indul-e a többi 23 ÚSZ-könyv (7 876 vers), milyen sorrendben és csomagokban.
2. A keret: a vetítés (43,5–45,6 USD) a maradék 23,63 USD kb. kétszerese. Lehetőség: keretemelés, vagy egy részcsomag a maradékból. Példa: a levelek és a Jel (a pilot `naplok/F21P_jelentes.md` „levél+Jel” csoportja, 3 169 vers) a négy próbakönyv nélkül 3 091 vers, versarányosan kb. 17,1 USD; ez belefér a maradékba, az evangéliumok és az ApCsel (4 785 vers, kb. 26,4 USD) nem.
3. N-F22b (az ÚSZ-verskulcs eltérései) rendezése a teljes ÚSZ előtt, vagy menet közben `kezi`-be téve.
