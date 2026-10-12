# F22_En_jelentes.md — Károli–Strong párosítás: Én (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Én`, `egyesit.py --konyv Én` és `--ellenoriz`, `f22_elemzes.py --konyv Én`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` En-soraiból: `futas = api_termeles/high/En`, `cimke = en`). Ág: `claude/youthful-clarke-5h6vk1` (a kilenc hiányzó kis könyv egy ágon, egy PR-ral; a main a Hós PR #291-et már tartalmazza). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a kilenc hiányzó kis könyv (797 vers) egyike (117 vers); a sorrend a felhasználó utasítása (Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir), a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.11: „mehet”, kilenc kis könyv egy ágon, egy PR-ral).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: **a felhasználó közvetlen ellenőrzése alapján** (nem a detektor alapján: a detektorlista az F85.6 óta az ÓSZ-ben üres); a Károli- és a TAHOT-kulcsok azonosak, a fejezetenkénti versszám egyezik, nincs versösszevonás és kézi leképezés. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Én'`).
- **Minta:** `f22/minta_En.tsv`, 117 vers, 8 fejezet, 12 köteg (10 vers/köteg, az utolsó 7).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_017YL9yjKnZGGW9u6CoFNECm`, 12 kérés (2026-10-11T20:05:21Z); javító kör `msgbatch_01AwCWXWhjwEafASPtEKyqB6`, 3 kérés (2026-10-11T20:08:04Z).
- **Futásnapló** (En: 15 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 12 | 9 | 3 köteg (3 vers) | 0.5378 | 116 257 / 84 306 |
| 2. próba (javító) | 3 | 3 | 0 köteg (0 vers) | 0.0592 | 37 235 / 4 399 |
| **összesen** | 15 | | | **0.5970** | |

A javító körbe került kötegek: 1, 4, 7; formátumhibás egész köteg nincs.

Költségplafon: a megbízás szerinti könyvplafon vers × 0,0074 × 1,5 = 1.30 USD (az `api_koteg.py` beépített alsó határa 1,00 USD); a könyv költsége 0.5970 USD (versenként 0.0051 USD). A kumulatív összeg a futásnapló `api_termeles/` soraiból: 85.2909 USD (az előző állapot 84.6939 + 0.5970), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is 85.290949.

*Munkamódszer:* a menet a megbízott session saját ágán, soros futtatással készült (egy könyv egyszerre).

## 1a. Szkriptkimenet

```
Sonnet: 12 köteg, 117 vers; kapuhiba első próbára 2.6% (3/117); végleg 0.0% (0/117)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Én`: parok: 2138 sor {'alacsony': 2138}; szavak: 4138 sor {'alacsony': 4138}; átnézési sor: 0 vers
ellenőrzés: rendben

A szavak bontása: hu 1692 `parositva`, 474 `betoldas`; er 1826 `parositva`, 146 `forditatlan`. A `kezi`/`fuggoben` tokenek száma: hu 0, er 0. Az átnézési sor (`naplok/F22_En_atnezes.tsv`): 0 vers. A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Én --ellenoriz` (2026.10.11): „rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Én` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/2138), alacsony 100.0% (2138/2138), kezi 0.0% (0/2138); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/4138), alacsony 100.0% (4138/4138), kezi 0.0% (0/4138).

Link-forrás megoszlás (parok): S 2138. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 117 (Én 1:1, Én 1:10, Én 1:11, Én 1:12, Én 1:13, Én 1:14, Én 1:15, Én 1:16, Én 1:17, Én 1:2).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 252 | 0.0% (0/252) | 100.0% (252/252) | 0.0% (0/252) | 492 | 0.0% (0/492) | 100.0% (492/492) | 0.0% (0/492) |
| 2 | 282 | 0.0% (0/282) | 100.0% (282/282) | 0.0% (0/282) | 579 | 0.0% (0/579) | 100.0% (579/579) | 0.0% (0/579) |
| 3 | 223 | 0.0% (0/223) | 100.0% (223/223) | 0.0% (0/223) | 420 | 0.0% (0/420) | 100.0% (420/420) | 0.0% (0/420) |
| 4 | 321 | 0.0% (0/321) | 100.0% (321/321) | 0.0% (0/321) | 596 | 0.0% (0/596) | 100.0% (596/596) | 0.0% (0/596) |
| 5 | 384 | 0.0% (0/384) | 100.0% (384/384) | 0.0% (0/384) | 718 | 0.0% (0/718) | 100.0% (718/718) | 0.0% (0/718) |
| 6 | 177 | 0.0% (0/177) | 100.0% (177/177) | 0.0% (0/177) | 351 | 0.0% (0/351) | 100.0% (351/351) | 0.0% (0/351) |
| 7 | 213 | 0.0% (0/213) | 100.0% (213/213) | 0.0% (0/213) | 432 | 0.0% (0/432) | 100.0% (432/432) | 0.0% (0/432) |
| 8 | 286 | 0.0% (0/286) | 100.0% (286/286) | 0.0% (0/286) | 550 | 0.0% (0/550) | 100.0% (550/550) | 0.0% (0/550) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 1; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (1/1).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/1).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (1/1).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- **Régi arany (2.2): 1/1, a `Sng.8.6 H7585` hármas** („a sír”; nincs az `f21p/regi_arany_hibas.tsv`-ben). Az `Én 8:6`-ban a „sír” (hu 23) → er 20 שְׁאוֹל (H7585): egyezik.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9 (`adat/datasetek.tsv`, `adat/SEMA.md` 2.20) és a brief fejléce/D43/v2.37: a kilenc könyv után, közös tételben (l. a brief D43).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: az orkesztrátor hívja (nem e menet dolga); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.

