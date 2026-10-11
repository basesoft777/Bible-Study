# F22_Joel_jelentes.md — Károli–Strong párosítás: Jóel (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Jóel`, `egyesit.py --konyv Jóel` és `--ellenoriz`, `f22_elemzes.py --konyv Jóel`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Joel-soraiból: `futas = api_termeles/high/Joel`, `cimke = joel`). Ág: `claude/youthful-clarke-5h6vk1` (a kilenc hiányzó kis könyv egy ágon, egy PR-ral; a main a Hós PR #291-et már tartalmazza). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a kilenc hiányzó kis könyv (797 vers) egyike (73 vers); a sorrend a felhasználó utasítása (Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir), a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.11: „mehet”, kilenc kis könyv egy ágon, egy PR-ral).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: **a felhasználó közvetlen ellenőrzése alapján** (nem a detektor alapján: a detektorlista az F85.6 óta az ÓSZ-ben üres); a Károli- és a TAHOT-kulcsok azonosak, a fejezetenkénti versszám egyezik, nincs versösszevonás és kézi leképezés. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Jóel'`).
- **Minta:** `f22/minta_Joel.tsv`, 73 vers, 3 fejezet, 8 köteg (10 vers/köteg, az utolsó 3).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_011gGRvzetHyzn7HPgriNGqz`, 8 kérés (2026-10-11T19:59:08Z); javító kör `msgbatch_01P4mtG1aSRiCyLHjsohVn54`, 2 kérés (2026-10-11T20:01:49Z).
- **Futásnapló** (Joel: 10 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 8 | 6 | 2 köteg (5 vers) | 0.3382 | 80 272 / 51 577 |
| 2. próba (javító) | 2 | 2 | 0 köteg (0 vers) | 0.0362 | 18 554 / 3 532 |
| **összesen** | 10 | | | **0.3744** | |

A javító körbe került kötegek: 2, 8; formátumhibás egész köteg nincs.

Költségplafon: a megbízás szerinti könyvplafon vers × 0,0074 × 1,5 = 0.81 USD (az `api_koteg.py` beépített alsó határa 1,00 USD); a könyv költsége 0.3744 USD (versenként 0.0051 USD). A kumulatív összeg a futásnapló `api_termeles/` soraiból: 84.6939 USD (az előző állapot 84.3196 + 0.3744), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is 84.693932.

*Munkamódszer:* a menet a megbízott session saját ágán, soros futtatással készült (egy könyv egyszerre).

## 1a. Szkriptkimenet

```
Sonnet: 8 köteg, 73 vers; kapuhiba első próbára 6.8% (5/73); végleg 0.0% (0/73)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Jóel`: parok: 1445 sor {'alacsony': 1445}; szavak: 2913 sor {'alacsony': 2913}; átnézési sor: 0 vers
ellenőrzés: rendben

A szavak bontása: hu 1184 `parositva`, 291 `betoldas`; er 1322 `parositva`, 116 `forditatlan`. A `kezi`/`fuggoben` tokenek száma: hu 0, er 0. Az átnézési sor (`naplok/F22_Joel_atnezes.tsv`): 0 vers. A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Jóel --ellenoriz` (2026.10.11): „rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Jóel` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1445), alacsony 100.0% (1445/1445), kezi 0.0% (0/1445); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/2913), alacsony 100.0% (2913/2913), kezi 0.0% (0/2913).

Link-forrás megoszlás (parok): S 1445. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 73 (Jóel 1:1, Jóel 1:10, Jóel 1:11, Jóel 1:12, Jóel 1:13, Jóel 1:14, Jóel 1:15, Jóel 1:16, Jóel 1:17, Jóel 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 328 | 0.0% (0/328) | 100.0% (328/328) | 0.0% (0/328) | 678 | 0.0% (0/678) | 100.0% (678/678) | 0.0% (0/678) |
| 2 | 707 | 0.0% (0/707) | 100.0% (707/707) | 0.0% (0/707) | 1414 | 0.0% (0/1414) | 100.0% (1414/1414) | 0.0% (0/1414) |
| 3 | 410 | 0.0% (0/410) | 100.0% (410/410) | 0.0% (0/410) | 821 | 0.0% (0/821) | 100.0% (821/821) | 0.0% (0/821) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3.

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

- **Régi arany (2.2): 1/1, a `Jol.2.32 H7121+H8034` hármas** („az Úrnak nevét hívja segítségül”; nincs az `f21p/regi_arany_hibas.tsv`-ben). A `Jóel 2:32`-ben a „nevét” (hu 7) → er 7 שֵׁם (H8034), a „hívja” (hu 8) → er 5 יִקְרָא (H7121); mindkét összetevő megvan, a hármas a várt tokenekre párosult.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9 (`adat/datasetek.tsv`, `adat/SEMA.md` 2.20) és a brief fejléce/D43/v2.37: a kilenc könyv után, közös tételben (l. a brief D43).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: az orkesztrátor hívja (nem e menet dolga); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.

