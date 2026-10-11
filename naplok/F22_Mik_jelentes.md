# F22_Mik_jelentes.md — Károli–Strong párosítás: Mik (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Mik`, `egyesit.py --konyv Mik` és `--ellenoriz`, `f22_elemzes.py --konyv Mik`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Mik-soraiból: `futas = api_termeles/high/Mik`, `cimke = mik`). Ág: `claude/youthful-clarke-5h6vk1` (a kilenc hiányzó kis könyv egy ágon, egy PR-ral; a main a Hós PR #291-et már tartalmazza). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a kilenc hiányzó kis könyv (797 vers) egyike (105 vers); a sorrend a felhasználó utasítása (Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir), a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.11: „mehet”, kilenc kis könyv egy ágon, egy PR-ral).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: **a felhasználó közvetlen ellenőrzése alapján** (nem a detektor alapján: a detektorlista az F85.6 óta az ÓSZ-ben üres); a Károli- és a TAHOT-kulcsok azonosak, a fejezetenkénti versszám egyezik, nincs versösszevonás és kézi leképezés. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Mik'`).
- **Minta:** `f22/minta_Mik.tsv`, 105 vers, 7 fejezet, 11 köteg (10 vers/köteg, az utolsó 5).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_017PFNMt9aHcwffMf2vZwYcP`, 11 kérés (2026-10-11T19:32:30Z); javító kör `msgbatch_01Gop3EXSqaEC4hMVGYAkXPp`, 1 kérés (2026-10-11T19:35:12Z).
- **Futásnapló** (Mik: 12 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 11 | 10 | 1 köteg (1 vers) | 0.5619 | 113 890 / 89 596 |
| 2. próba (javító) | 1 | 1 | 0 köteg (0 vers) | 0.0124 | 8 342 / 803 |
| **összesen** | 12 | | | **0.5742** | |

A javító körbe került kötegek: 11; formátumhibás egész köteg nincs.

Költségplafon: a megbízás szerinti könyvplafon vers × 0,0074 × 1,5 = 1.17 USD (az `api_koteg.py` beépített alsó határa 1,00 USD); a könyv költsége 0.5742 USD (versenként 0.0055 USD). A kumulatív összeg a futásnapló `api_termeles/` soraiból: 83.4110 USD (az előző állapot 82.8368 + 0.5742), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is 83.411022.

*Munkamódszer:* a menet a megbízott session saját ágán, soros futtatással készült (egy könyv egyszerre).

## 1a. Szkriptkimenet

```
Sonnet: 11 köteg, 105 vers; kapuhiba első próbára 1.0% (1/105); végleg 0.0% (0/105)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Mik`: parok: 2186 sor {'alacsony': 2186}; szavak: 4217 sor {'alacsony': 4217}; átnézési sor: 0 vers
ellenőrzés: rendben

A szavak bontása: hu 1741 `parositva`, 371 `betoldas`; er 2011 `parositva`, 94 `forditatlan`. A `kezi`/`fuggoben` tokenek száma: hu 0, er 0. Az átnézési sor (`naplok/F22_Mik_atnezes.tsv`): 0 vers. A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Mik --ellenoriz` (2026.10.11): „rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Mik` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/2186), alacsony 100.0% (2186/2186), kezi 0.0% (0/2186); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/4217), alacsony 100.0% (4217/4217), kezi 0.0% (0/4217).

Link-forrás megoszlás (parok): S 2186. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 105 (Mik 1:1, Mik 1:10, Mik 1:11, Mik 1:12, Mik 1:13, Mik 1:14, Mik 1:15, Mik 1:16, Mik 1:2, Mik 1:3).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 307 | 0.0% (0/307) | 100.0% (307/307) | 0.0% (0/307) | 586 | 0.0% (0/586) | 100.0% (586/586) | 0.0% (0/586) |
| 2 | 268 | 0.0% (0/268) | 100.0% (268/268) | 0.0% (0/268) | 539 | 0.0% (0/539) | 100.0% (539/539) | 0.0% (0/539) |
| 3 | 277 | 0.0% (0/277) | 100.0% (277/277) | 0.0% (0/277) | 521 | 0.0% (0/521) | 100.0% (521/521) | 0.0% (0/521) |
| 4 | 331 | 0.0% (0/331) | 100.0% (331/331) | 0.0% (0/331) | 632 | 0.0% (0/632) | 100.0% (632/632) | 0.0% (0/632) |
| 5 | 298 | 0.0% (0/298) | 100.0% (298/298) | 0.0% (0/298) | 568 | 0.0% (0/568) | 100.0% (568/568) | 0.0% (0/568) |
| 6 | 316 | 0.0% (0/316) | 100.0% (316/316) | 0.0% (0/316) | 614 | 0.0% (0/614) | 100.0% (614/614) | 0.0% (0/614) |
| 7 | 389 | 0.0% (0/389) | 100.0% (389/389) | 0.0% (0/389) | 757 | 0.0% (0/757) | 100.0% (757/757) | 0.0% (0/757) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7.

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

