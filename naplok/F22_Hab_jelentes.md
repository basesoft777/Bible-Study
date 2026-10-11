# F22_Hab_jelentes.md — Károli–Strong párosítás: Hab (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Hab`, `egyesit.py --konyv Hab` és `--ellenoriz`, `f22_elemzes.py --konyv Hab`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Hab-soraiból: `futas = api_termeles/high/Hab`, `cimke = hab`). Ág: `claude/youthful-clarke-5h6vk1` (a kilenc hiányzó kis könyv egy ágon, egy PR-ral; a main a Hós PR #291-et már tartalmazza). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a kilenc hiányzó kis könyv (797 vers) egyike (56 vers); a sorrend a felhasználó utasítása (Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir), a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.11: „mehet”, kilenc kis könyv egy ágon, egy PR-ral).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: **a felhasználó közvetlen ellenőrzése alapján** (nem a detektor alapján: a detektorlista az F85.6 óta az ÓSZ-ben üres); a Károli- és a TAHOT-kulcsok azonosak, a fejezetenkénti versszám egyezik, nincs versösszevonás és kézi leképezés. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Hab'`).
- **Minta:** `f22/minta_Hab.tsv`, 56 vers, 3 fejezet, 6 köteg (10 vers/köteg, az utolsó 6).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_015DQH1xeE3hTFHDg6VBEtoa`, 6 kérés (2026-10-11T19:25:09Z); javító kör `msgbatch_01UMETntYpEaV9dJZPbEu3xy`, 2 kérés (2026-10-11T19:28:52Z).
- **Futásnapló** (Hab: 8 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 6 | 4 | 2 köteg (2 vers) | 0.2961 | 58 109 / 47 597 |
| 2. próba (javító) | 2 | 2 | 0 köteg (0 vers) | 0.0324 | 20 997 / 2 282 |
| **összesen** | 8 | | | **0.3285** | |

A javító körbe került kötegek: 1, 6; formátumhibás egész köteg nincs.

Költségplafon: a megbízás szerinti könyvplafon vers × 0,0074 × 1,5 = 0.62 USD (az `api_koteg.py` beépített alsó határa 1,00 USD); a könyv költsége 0.3285 USD (versenként 0.0059 USD). A kumulatív összeg a futásnapló `api_termeles/` soraiból: 82.8368 USD (az előző állapot 82.5083 + 0.3285), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is 82.836795.

*Munkamódszer:* a menet a megbízott session saját ágán, soros futtatással készült (egy könyv egyszerre).

## 1a. Szkriptkimenet

```
Sonnet: 6 köteg, 56 vers; kapuhiba első próbára 3.6% (2/56); végleg 0.0% (0/56)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Hab`: parok: 1038 sor {'alacsony': 1038}; szavak: 2048 sor {'alacsony': 2048}; átnézési sor: 0 vers
ellenőrzés: rendben

A szavak bontása: hu 829 `parositva`, 219 `betoldas`; er 958 `parositva`, 42 `forditatlan`. A `kezi`/`fuggoben` tokenek száma: hu 0, er 0. Az átnézési sor (`naplok/F22_Hab_atnezes.tsv`): 0 vers. A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Hab --ellenoriz` (2026.10.11): „rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Hab` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1038), alacsony 100.0% (1038/1038), kezi 0.0% (0/1038); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/2048), alacsony 100.0% (2048/2048), kezi 0.0% (0/2048).

Link-forrás megoszlás (parok): S 1038. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 56 (Hab 1:1, Hab 1:10, Hab 1:11, Hab 1:12, Hab 1:13, Hab 1:14, Hab 1:15, Hab 1:16, Hab 1:17, Hab 1:2).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 317 | 0.0% (0/317) | 100.0% (317/317) | 0.0% (0/317) | 610 | 0.0% (0/610) | 100.0% (610/610) | 0.0% (0/610) |
| 2 | 397 | 0.0% (0/397) | 100.0% (397/397) | 0.0% (0/397) | 804 | 0.0% (0/804) | 100.0% (804/804) | 0.0% (0/804) |
| 3 | 324 | 0.0% (0/324) | 100.0% (324/324) | 0.0% (0/324) | 634 | 0.0% (0/634) | 100.0% (634/634) | 0.0% (0/634) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 2; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 50.0% (1/2).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/2).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 50.0% (1/2).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- **Régi arany (2.2): 1/2** (a `Hab.2.5 H7585` hármas egyezik, a `Hab.3.10 H8415` nem; a kizárás nélkül mért érték 50,0%, mindkettő a `regi_arany_hibas.tsv`-n kívül áll).
  - `Hab.2.5 H7585` („a Seol”): a `Hab 2:5` hu 20 „Seol” az er 15 שְׁאוֹל-ra (H7585) párosult: egyezik.
  - `Hab.3.10 H8415` („víz-ár”): a `Hab 3:10`-ben a „víz” (hu 10) → er 6 מַיִם (H4325), az „ár” (hu 11) → er 5 זֶרֶם (H2230); a H8415 (תְּהוֹם, er 9) a „hullám” (hu 14) szóhoz kötött. A régi arany tehát más Károli-szóhoz (a „víz-ár”-hoz) rendelte a H8415-öt, mint a párosítás; a TAHOT-glosszák (H4325 „water”, H2230 „storm”, H8415 „abyss”) a párosítás tokenkiosztását támogatják, de hogy a régi arany hármasa hibás-e, az **tartalmi ítélet, nem e menet dolga**: az `f21p/regi_arany_hibas.tsv`-be felvétel a felhasználó/orkesztrátor döntése (javaslat: vizsgálandó, mint a `Job.17.13` és az `Ecc.9.10` esete).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9 (`adat/datasetek.tsv`, `adat/SEMA.md` 2.20) és a brief fejléce/D43/v2.37: a kilenc könyv után, közös tételben (l. a brief D43).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: az orkesztrátor hívja (nem e menet dolga); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.

