# F22_Hag_jelentes.md — Károli–Strong párosítás: Hag (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Hag`, `egyesit.py --konyv Hag` és `--ellenoriz`, `f22_elemzes.py --konyv Hag`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Hag-soraiból: `futas = api_termeles/high/Hag`, `cimke = hag`). Ág: `claude/youthful-clarke-5h6vk1` (a kilenc hiányzó kis könyv egy ágon, egy PR-ral; a main a Hós PR #291-et már tartalmazza). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a kilenc hiányzó kis könyv (797 vers) egyike (38 vers); a sorrend a felhasználó utasítása (Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir), a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.11: „mehet”, kilenc kis könyv egy ágon, egy PR-ral).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: **a felhasználó közvetlen ellenőrzése alapján** (nem a detektor alapján: a detektorlista az F85.6 óta az ÓSZ-ben üres); a Károli- és a TAHOT-kulcsok azonosak, a fejezetenkénti versszám egyezik, nincs versösszevonás és kézi leképezés. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Hag'`).
- **Minta:** `f22/minta_Hag.tsv`, 38 vers, 2 fejezet, 4 köteg (10 vers/köteg, az utolsó 8).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01PYWb9y1eCytkL6AR6j6ZBQ`, 4 kérés (2026-10-11T19:16:02Z).
- **Futásnapló** (Hag: 4 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 4 | 4 | 0 köteg (0 vers) | 0.2496 | 44 326 / 41 049 |
| **összesen** | 4 | | | **0.2496** | |

Javító kör nem kellett.

Költségplafon: a megbízás szerinti könyvplafon vers × 0,0074 × 1,5 = 0.42 USD (az `api_koteg.py` beépített alsó határa 1,00 USD); a könyv költsége 0.2496 USD (versenként 0.0066 USD). A kumulatív összeg a futásnapló `api_termeles/` soraiból: 82.1972 USD (az előző állapot 81.9476 + 0.2496), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is 82.197211.

*Munkamódszer:* a menet a megbízott session saját ágán, soros futtatással készült (egy könyv egyszerre).

## 1a. Szkriptkimenet

```
Sonnet: 4 köteg, 38 vers; kapuhiba első próbára 0.0% (0/38); végleg 0.0% (0/38)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Hag`: parok: 872 sor {'alacsony': 872}; szavak: 1770 sor {'alacsony': 1770}; átnézési sor: 0 vers
ellenőrzés: rendben

A szavak bontása: hu 685 `parositva`, 174 `betoldas`; er 810 `parositva`, 101 `forditatlan`. A `kezi`/`fuggoben` tokenek száma: hu 0, er 0. Az átnézési sor (`naplok/F22_Hag_atnezes.tsv`): 0 vers. A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Hag --ellenoriz` (2026.10.11): „rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Hag` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/872), alacsony 100.0% (872/872), kezi 0.0% (0/872); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/1770), alacsony 100.0% (1770/1770), kezi 0.0% (0/1770).

Link-forrás megoszlás (parok): S 872. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 38 (Hag 1:1, Hag 1:10, Hag 1:11, Hag 1:12, Hag 1:13, Hag 1:14, Hag 1:15, Hag 1:2, Hag 1:3, Hag 1:4).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 348 | 0.0% (0/348) | 100.0% (348/348) | 0.0% (0/348) | 698 | 0.0% (0/698) | 100.0% (698/698) | 0.0% (0/698) |
| 2 | 524 | 0.0% (0/524) | 100.0% (524/524) | 0.0% (0/524) | 1072 | 0.0% (0/1072) | 100.0% (1072/1072) | 0.0% (0/1072) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 0; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** n.é. (0/0).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): n.é. (0/0).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): n.é. (0/0).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- Nincs jelölt pont: az átnézési sorok száma 0 (nincs `kezi` vers), régi-arany hármas a könyvben nincs.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9 (`adat/datasetek.tsv`, `adat/SEMA.md` 2.20) és a brief fejléce/D43/v2.37: a kilenc könyv után, közös tételben (l. a brief D43).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: az orkesztrátor hívja (nem e menet dolga); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.

