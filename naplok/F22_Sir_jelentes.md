# F22_Sir_jelentes.md — Károli–Strong párosítás: Sir (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Sir`, `egyesit.py --konyv Sir` és `--ellenoriz`, `f22_elemzes.py --konyv Sir`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Sir-soraiból: `futas = api_termeles/high/Sir`, `cimke = sir`). Ág: `claude/youthful-clarke-5h6vk1` (a kilenc hiányzó kis könyv egy ágon, egy PR-ral; a main a Hós PR #291-et már tartalmazza). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a kilenc hiányzó kis könyv (797 vers) egyike (154 vers); a sorrend a felhasználó utasítása (Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir), a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.11: „mehet”, kilenc kis könyv egy ágon, egy PR-ral).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: **a felhasználó közvetlen ellenőrzése alapján** (nem a detektor alapján: a detektorlista az F85.6 óta az ÓSZ-ben üres); a Károli- és a TAHOT-kulcsok azonosak, a fejezetenkénti versszám egyezik, nincs versösszevonás és kézi leképezés. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Sir'`).
- **Minta:** `f22/minta_Sir.tsv`, 154 vers, 5 fejezet, 16 köteg (10 vers/köteg, az utolsó 4).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_015BjsNyDfSvtG2fmqF4cumv`, 16 kérés (2026-10-11T20:11:40Z); javító kör `msgbatch_01XBhNxXCnNTH1ZU8F5yx7MP`, 4 kérés (2026-10-11T20:14:54Z).
- **Futásnapló** (Sir: 20 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 16 | 12 | 4 köteg (15 vers) | 0.5874 | 143 874 / 88 696 |
| 2. próba (javító) | 4 | 4 | 0 köteg (0 vers) | 0.0664 | 34 874 / 6 300 |
| **összesen** | 20 | | | **0.6537** | |

A javító körbe került kötegek: 6, 8, 9, 10; formátumhibás egész köteg nincs.

Költségplafon: a megbízás szerinti könyvplafon vers × 0,0074 × 1,5 = 1.71 USD (az `api_koteg.py` beépített alsó határa 1,00 USD); a könyv költsége 0.6537 USD (versenként 0.0042 USD). A kumulatív összeg a futásnapló `api_termeles/` soraiból: 85.9447 USD (az előző állapot 85.2909 + 0.6537), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is 85.944677.

*Munkamódszer:* a menet a megbízott session saját ágán, soros futtatással készült (egy könyv egyszerre).

## 1a. Szkriptkimenet

```
Sonnet: 16 köteg, 154 vers; kapuhiba első próbára 9.7% (15/154); végleg 0.0% (0/154)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Sir`: parok: 2410 sor {'alacsony': 2410}; szavak: 4539 sor {'alacsony': 4539}; átnézési sor: 0 vers
ellenőrzés: rendben

A szavak bontása: hu 1892 `parositva`, 409 `betoldas`; er 2181 `parositva`, 57 `forditatlan`. A `kezi`/`fuggoben` tokenek száma: hu 0, er 0. Az átnézési sor (`naplok/F22_Sir_atnezes.tsv`): 0 vers. A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Sir --ellenoriz` (2026.10.11): „rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Sir` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/2410), alacsony 100.0% (2410/2410), kezi 0.0% (0/2410); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/4539), alacsony 100.0% (4539/4539), kezi 0.0% (0/4539).

Link-forrás megoszlás (parok): S 2410. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 154 (Sir 1:1, Sir 1:10, Sir 1:11, Sir 1:12, Sir 1:13, Sir 1:14, Sir 1:15, Sir 1:16, Sir 1:17, Sir 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 584 | 0.0% (0/584) | 100.0% (584/584) | 0.0% (0/584) | 1070 | 0.0% (0/1070) | 100.0% (1070/1070) | 0.0% (0/1070) |
| 2 | 580 | 0.0% (0/580) | 100.0% (580/580) | 0.0% (0/580) | 1101 | 0.0% (0/1101) | 100.0% (1101/1101) | 0.0% (0/1101) |
| 3 | 615 | 0.0% (0/615) | 100.0% (615/615) | 0.0% (0/615) | 1172 | 0.0% (0/1172) | 100.0% (1172/1172) | 0.0% (0/1172) |
| 4 | 400 | 0.0% (0/400) | 100.0% (400/400) | 0.0% (0/400) | 779 | 0.0% (0/779) | 100.0% (779/779) | 0.0% (0/779) |
| 5 | 231 | 0.0% (0/231) | 100.0% (231/231) | 0.0% (0/231) | 417 | 0.0% (0/417) | 100.0% (417/417) | 0.0% (0/417) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5.

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

