# F22_Mal_jelentes.md — Károli–Strong párosítás: Mal (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Mal`, `egyesit.py --konyv Mal` és `--ellenoriz`, `f22_elemzes.py --konyv Mal`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Mal-soraiból: `futas = api_termeles/high/Mal`, `cimke = mal`). Ág: `claude/youthful-clarke-5h6vk1` (a kilenc hiányzó kis könyv egy ágon, egy PR-ral; a main a Hós PR #291-et már tartalmazza). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a kilenc hiányzó kis könyv (797 vers) egyike (55 vers); a sorrend a felhasználó utasítása (Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir), a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.11: „mehet”, kilenc kis könyv egy ágon, egy PR-ral).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: **a felhasználó közvetlen ellenőrzése alapján** (nem a detektor alapján: a detektorlista az F85.6 óta az ÓSZ-ben üres); a Károli- és a TAHOT-kulcsok azonosak, a fejezetenkénti versszám egyezik, nincs versösszevonás és kézi leképezés. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Mal'`).
- **Minta:** `f22/minta_Mal.tsv`, 55 vers, 4 fejezet, 6 köteg (10 vers/köteg, az utolsó 5).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_0136sLRaPqtSRHP9LaR4AWtU`, 6 kérés (2026-10-11T19:07:01Z); javító kör `msgbatch_012Tjvw1qTTFaFawq5S4RPdk`, 2 kérés (2026-10-11T19:10:59Z).
- **Futásnapló** (Mal: 8 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 6 | 4 | 2 köteg (11 vers) | 0.3600 | 66 545 / 58 687 |
| 2. próba (javító) | 2 | 2 | 0 köteg (0 vers) | 0.0931 | 28 621 / 12 890 |
| **összesen** | 8 | | | **0.4531** | |

A javító körbe került kötegek: 1, 2; egész köteg formátumhibás (nem érvényes JSON): k001, 10 vers; a javító kör 0-ra hozta.

Költségplafon: a megbízás szerinti könyvplafon vers × 0,0074 × 1,5 = 0.61 USD (az `api_koteg.py` beépített alsó határa 1,00 USD); a könyv költsége 0.4531 USD (versenként 0.0082 USD). A kumulatív összeg a futásnapló `api_termeles/` soraiból: 81.9476 USD (az előző állapot 81.4946 + 0.4531), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is 81.947640.

*Munkamódszer:* a menet a megbízott session saját ágán, soros futtatással készült (egy könyv egyszerre).

## 1a. Szkriptkimenet

```
Sonnet: 6 köteg, 55 vers; kapuhiba első próbára 20.0% (11/55); végleg 0.0% (0/55)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Mal`: parok: 1340 sor {'alacsony': 1340}; szavak: 2679 sor {'alacsony': 2679}; átnézési sor: 0 vers
ellenőrzés: rendben

A szavak bontása: hu 1113 `parositva`, 264 `betoldas`; er 1226 `parositva`, 76 `forditatlan`. A `kezi`/`fuggoben` tokenek száma: hu 0, er 0. Az átnézési sor (`naplok/F22_Mal_atnezes.tsv`): 0 vers. A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Mal --ellenoriz` (2026.10.11): „rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Mal` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1340), alacsony 100.0% (1340/1340), kezi 0.0% (0/1340); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/2679), alacsony 100.0% (2679/2679), kezi 0.0% (0/2679).

Link-forrás megoszlás (parok): S 1340. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 55 (Mal 1:1, Mal 1:10, Mal 1:11, Mal 1:12, Mal 1:13, Mal 1:14, Mal 1:2, Mal 1:3, Mal 1:4, Mal 1:5).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 359 | 0.0% (0/359) | 100.0% (359/359) | 0.0% (0/359) | 739 | 0.0% (0/739) | 100.0% (739/739) | 0.0% (0/739) |
| 2 | 420 | 0.0% (0/420) | 100.0% (420/420) | 0.0% (0/420) | 812 | 0.0% (0/812) | 100.0% (812/812) | 0.0% (0/812) |
| 3 | 426 | 0.0% (0/426) | 100.0% (426/426) | 0.0% (0/426) | 849 | 0.0% (0/849) | 100.0% (849/849) | 0.0% (0/849) |
| 4 | 135 | 0.0% (0/135) | 100.0% (135/135) | 0.0% (0/135) | 279 | 0.0% (0/279) | 100.0% (279/279) | 0.0% (0/279) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4.

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

