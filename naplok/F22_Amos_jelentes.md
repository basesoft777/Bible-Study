# F22_Amos_jelentes.md — Károli–Strong párosítás: Ámós (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Ámós`, `egyesit.py --konyv Ámós` és `--ellenoriz`, `f22_elemzes.py --konyv Ámós`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Amos-soraiból: `futas = api_termeles/high/Amos`, `cimke = amos`). Ág: `claude/youthful-clarke-5h6vk1` (a kilenc hiányzó kis könyv egy ágon, egy PR-ral; a main a Hós PR #291-et már tartalmazza). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a kilenc hiányzó kis könyv (797 vers) egyike (146 vers); a sorrend a felhasználó utasítása (Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir), a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.11: „mehet”, kilenc kis könyv egy ágon, egy PR-ral).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: **a felhasználó közvetlen ellenőrzése alapján** (nem a detektor alapján: a detektorlista az F85.6 óta az ÓSZ-ben üres); a Károli- és a TAHOT-kulcsok azonosak, a fejezetenkénti versszám egyezik, nincs versösszevonás és kézi leképezés. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Ámós'`).
- **Minta:** `f22/minta_Amos.tsv`, 146 vers, 9 fejezet, 15 köteg (10 vers/köteg, az utolsó 6).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01VuhK3uVQxVzcFNmatisdfD`, 15 kérés (2026-10-11T19:38:42Z); javító kör `msgbatch_01CQySZdfShzYWu9KBazh21v`, 1 kérés (2026-10-11T19:48:01Z).
- **Futásnapló** (Amos: 16 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 15 | 14 | 1 köteg (10 vers) | 0.8462 | 159 365 / 137 370 |
| 2. próba (javító) | 1 | 1 | 0 köteg (0 vers) | 0.0623 | 14 624 / 9 540 |
| **összesen** | 16 | | | **0.9085** | |

A javító körbe került kötegek: 6; egész köteg formátumhibás (nem érvényes JSON): k006, 10 vers; a javító kör 0-ra hozta.

Költségplafon: a megbízás szerinti könyvplafon vers × 0,0074 × 1,5 = 1.62 USD (az `api_koteg.py` beépített alsó határa 1,00 USD); a könyv költsége 0.9085 USD (versenként 0.0062 USD). A kumulatív összeg a futásnapló `api_termeles/` soraiból: 84.3196 USD (az előző állapot 83.4110 + 0.9085), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is 84.319561.

*Munkamódszer:* a menet a megbízott session saját ágán, soros futtatással készült (egy könyv egyszerre).

## 1a. Szkriptkimenet

```
Sonnet: 15 köteg, 146 vers; kapuhiba első próbára 6.8% (10/146); végleg 0.0% (0/146)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Ámós`: parok: 3061 sor {'alacsony': 3061}; szavak: 6137 sor {'alacsony': 6137}; átnézési sor: 0 vers
ellenőrzés: rendben

A szavak bontása: hu 2544 `parositva`, 615 `betoldas`; er 2785 `parositva`, 193 `forditatlan`. A `kezi`/`fuggoben` tokenek száma: hu 0, er 0. Az átnézési sor (`naplok/F22_Amos_atnezes.tsv`): 0 vers. A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Ámós --ellenoriz` (2026.10.11): „rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Ámós` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/3061), alacsony 100.0% (3061/3061), kezi 0.0% (0/3061); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/6137), alacsony 100.0% (6137/6137), kezi 0.0% (0/6137).

Link-forrás megoszlás (parok): S 3061. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 146 (Ámós 1:1, Ámós 1:10, Ámós 1:11, Ámós 1:12, Ámós 1:13, Ámós 1:14, Ámós 1:15, Ámós 1:2, Ámós 1:3, Ámós 1:4).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 323 | 0.0% (0/323) | 100.0% (323/323) | 0.0% (0/323) | 629 | 0.0% (0/629) | 100.0% (629/629) | 0.0% (0/629) |
| 2 | 322 | 0.0% (0/322) | 100.0% (322/322) | 0.0% (0/322) | 649 | 0.0% (0/649) | 100.0% (649/649) | 0.0% (0/649) |
| 3 | 309 | 0.0% (0/309) | 100.0% (309/309) | 0.0% (0/309) | 606 | 0.0% (0/606) | 100.0% (606/606) | 0.0% (0/606) |
| 4 | 335 | 0.0% (0/335) | 100.0% (335/335) | 0.0% (0/335) | 643 | 0.0% (0/643) | 100.0% (643/643) | 0.0% (0/643) |
| 5 | 464 | 0.0% (0/464) | 100.0% (464/464) | 0.0% (0/464) | 952 | 0.0% (0/952) | 100.0% (952/952) | 0.0% (0/952) |
| 6 | 277 | 0.0% (0/277) | 100.0% (277/277) | 0.0% (0/277) | 578 | 0.0% (0/578) | 100.0% (578/578) | 0.0% (0/578) |
| 7 | 347 | 0.0% (0/347) | 100.0% (347/347) | 0.0% (0/347) | 680 | 0.0% (0/680) | 100.0% (680/680) | 0.0% (0/680) |
| 8 | 283 | 0.0% (0/283) | 100.0% (283/283) | 0.0% (0/283) | 588 | 0.0% (0/588) | 100.0% (588/588) | 0.0% (0/588) |
| 9 | 401 | 0.0% (0/401) | 100.0% (401/401) | 0.0% (0/401) | 812 | 0.0% (0/812) | 100.0% (812/812) | 0.0% (0/812) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9.

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

- **Régi arany (2.2): 2/2** (kizárás nélkül; egyik hármas sincs az `f21p/regi_arany_hibas.tsv`-ben).
  - `Amo.7.4 H8415` („mélységet”): `Ámós 7:4` hu 21 „mélységet” → er 18 תְּהוֹם (H8415): egyezik.
  - `Amo.9.2 H7585` („a Seolba”): `Ámós 9:2` hu 3 „Seolba” → er 4 שְׁאוֹל (H7585): egyezik.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9 (`adat/datasetek.tsv`, `adat/SEMA.md` 2.20) és a brief fejléce/D43/v2.37: a kilenc könyv után, közös tételben (l. a brief D43).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: az orkesztrátor hívja (nem e menet dolga); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.

