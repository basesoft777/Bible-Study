# F22_Jon_jelentes.md — Károli–Strong párosítás: Jónás (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Jón`, `egyesit.py --konyv Jón` és `--ellenoriz`, `f22_elemzes.py --konyv Jón`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Jon-soraiból: `futas = api_termeles/high/Jon`, `cimke = jon`, a `f22/api_termeles/high/_munka/Jon_k*.json` hibaüzenetei). Ág: `claude/f22-jon` (külön worktree, a main `7be3977a` commitjáról; az 1Kir PR #274, a Neh PR #275, a 2Kir PR #277, a Dán PR #279 és a Ruth PR #280 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a Ruth után a hiányzó kis könyvek egyike (48 vers), a detektor szerint beolvasztás nélküli; a választás a felhasználóé. Indítás: felhasználó, chat, 2026.10.11 („mehet a Jónás”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Jón tiszta (48/48 vers, 4 fejezet, eltolt 0), a listában és a `versosszevonas.tsv`-ben nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Jón'`).
- **Minta:** `f22/minta_Jon.tsv`, 48 vers (= a `Karoli_1908.tsv` `Jón ` sorai), 5 köteg (10 vers/köteg, az utolsó 8).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01T2d3F8ZP5WxciiNxLGPYKv`, 5 kérés (2026-10-11T15:06Z); javító kör `msgbatch_01G7kEqAMqKvoDQCAGVXjwAs`, 2 kérés (15:09Z).
- **Futásnapló** (Jon: 7 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 5 | 3 | 2 köteg (2 vers) | 0,2357 | 53 371 / 36 465 |
| 2. próba (javító) | 2 | 2 | 0 | 0,0485 | 27 684 / 4 157 |
| **összesen** | 7 | | | **0,2842** | |

A javító körbe került kötegek: 1 (1 vers) és 4 (1 vers); formátumhibás egész köteg nincs.

A könyvplafon a minimum (1,00 USD; 48 × 0,0074 × 1,5 = 0,53 alatt), ebből 0,28 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 77,5074 USD (Ézs–Ruth 77,2232 + Jón 0,2842), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is ennyi. Versenként 0,0059 USD (a plafon alapja 0,0074 alatt).

*Munkamódszer-megjegyzés:* a menet külön worktree-ben (`C:\Users\bases\Desktop\Bible-Study-jon`) készült, mert a közös munkakönyvtárban más session ágat váltogat.

## 1a. Szkriptkimenet

```
Sonnet: 5 köteg, 48 vers; kapuhiba első próbára 4.2% (2/48); végleg 0.0% (0/48)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Jón`: `parok_Jon.tsv` 1 052 link (mind `alacsony`, `S`), `szavak_Jon.tsv` 2 071 token. A szavak bontása: hu 991 (827 `parositva`, 164 `betoldas`), er 1 080 (1 000 `parositva`, 80 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Jón ` sorainak száma (1 080). Az átnézési sor (`naplok/F22_Jon_atnezes.tsv`) üres (csak fejléc). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Jón --ellenoriz` (2026.10.11): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Jón` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1052), alacsony 100.0% (1052/1052), kezi 0.0% (0/1052); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/2071), alacsony 100.0% (2071/2071), kezi 0.0% (0/2071).

Link-forrás megoszlás (parok): S 1052. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 48 (Jón 1:1, Jón 1:10, Jón 1:11, Jón 1:12, Jón 1:13, Jón 1:14, Jón 1:15, Jón 1:16, Jón 1:2, Jón 1:3).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 391 | 0.0% (0/391) | 100.0% (391/391) | 0.0% (0/391) | 771 | 0.0% (0/771) | 100.0% (771/771) | 0.0% (0/771) |
| 2 | 177 | 0.0% (0/177) | 100.0% (177/177) | 0.0% (0/177) | 336 | 0.0% (0/336) | 100.0% (336/336) | 0.0% (0/336) |
| 3 | 216 | 0.0% (0/216) | 100.0% (216/216) | 0.0% (0/216) | 430 | 0.0% (0/430) | 100.0% (430/430) | 0.0% (0/430) |
| 4 | 268 | 0.0% (0/268) | 100.0% (268/268) | 0.0% (0/268) | 534 | 0.0% (0/534) | 100.0% (534/534) | 0.0% (0/534) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 2; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (2/2).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/2).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (2/2).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- Nincs: a Jónásban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A régi arany (2.2) két hármasa egyezik (2/2); kis minta.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: a Jón bejegyezve az `adat/datasetek.tsv`-be (8 sor, a jelentéslistával együtt) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D35, v2.29.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
- A következő könyv(ek) a felhasználó döntése: az ÓSZ-ből még 14 kis könyv hiányzik (Préd, Én, Sir, Hós, Jóel, Ámós, Abd, Mik, Náh, Hab, Sof, Hag, Zak, Mal; együtt 1 492 vers); a Hós (1:11, 11:11) és a Préd (2:26) jóváhagyott 2:1 beolvasztást tartalmaz (`f22/versosszevonas.tsv`, DT92), ezeknél kézi átnézési pont várható; a többi 12 tiszta.

