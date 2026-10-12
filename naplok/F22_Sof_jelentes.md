# F22_Sof_jelentes.md — Károli–Strong párosítás: Sof (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Sof`, `egyesit.py --konyv Sof` és `--ellenoriz`, `f22_elemzes.py --konyv Sof`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Sof-soraiból: `futas = api_termeles/high/Sof`, `cimke = sof`). Ág: `claude/youthful-clarke-5h6vk1` (a kilenc hiányzó kis könyv egy ágon, egy PR-ral; a main a Hós PR #291-et már tartalmazza). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a kilenc hiányzó kis könyv (797 vers) egyike (53 vers); a sorrend a felhasználó utasítása (Mal, Hag, Sof, Hab, Mik, Ámós, Jóel, Én, Sir), a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.11: „mehet”, kilenc kis könyv egy ágon, egy PR-ral).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: **a felhasználó közvetlen ellenőrzése alapján** (nem a detektor alapján: a detektorlista az F85.6 óta az ÓSZ-ben üres); a Károli- és a TAHOT-kulcsok azonosak, a fejezetenkénti versszám egyezik, nincs versösszevonás és kézi leképezés. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Sof'`).
- **Minta:** `f22/minta_Sof.tsv`, 53 vers, 3 fejezet, 6 köteg (10 vers/köteg, az utolsó 3).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_017e2yXWaL5H1BTaiN1XQrE8`, 6 kérés (2026-10-11T19:20:29Z).
- **Futásnapló** (Sof: 6 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 6 | 6 | 0 köteg (0 vers) | 0.3111 | 61 278 / 49 961 |
| **összesen** | 6 | | | **0.3111** | |

Javító kör nem kellett.

Költségplafon: a megbízás szerinti könyvplafon vers × 0,0074 × 1,5 = 0.59 USD (az `api_koteg.py` beépített alsó határa 1,00 USD); a könyv költsége 0.3111 USD (versenként 0.0059 USD). A kumulatív összeg a futásnapló `api_termeles/` soraiból: 82.5083 USD (az előző állapot 82.1972 + 0.3111), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is 82.508294.

*Munkamódszer:* a menet a megbízott session saját ágán, soros futtatással készült (egy könyv egyszerre).

## 1a. Szkriptkimenet

```
Sonnet: 6 köteg, 53 vers; kapuhiba első próbára 0.0% (0/53); végleg 0.0% (0/53)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Sof`: parok: 1108 sor {'alacsony': 1108}; szavak: 2228 sor {'alacsony': 2228}; átnézési sor: 0 vers
ellenőrzés: rendben

A szavak bontása: hu 912 `parositva`, 196 `betoldas`; er 1037 `parositva`, 83 `forditatlan`. A `kezi`/`fuggoben` tokenek száma: hu 0, er 0. Az átnézési sor (`naplok/F22_Sof_atnezes.tsv`): 0 vers. A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Sof --ellenoriz` (2026.10.11): „rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Sof` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1108), alacsony 100.0% (1108/1108), kezi 0.0% (0/1108); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/2228), alacsony 100.0% (2228/2228), kezi 0.0% (0/2228).

Link-forrás megoszlás (parok): S 1108. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 53 (Sof 1:1, Sof 1:10, Sof 1:11, Sof 1:12, Sof 1:13, Sof 1:14, Sof 1:15, Sof 1:16, Sof 1:17, Sof 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 378 | 0.0% (0/378) | 100.0% (378/378) | 0.0% (0/378) | 799 | 0.0% (0/799) | 100.0% (799/799) | 0.0% (0/799) |
| 2 | 311 | 0.0% (0/311) | 100.0% (311/311) | 0.0% (0/311) | 622 | 0.0% (0/622) | 100.0% (622/622) | 0.0% (0/622) |
| 3 | 419 | 0.0% (0/419) | 100.0% (419/419) | 0.0% (0/419) | 807 | 0.0% (0/807) | 100.0% (807/807) | 0.0% (0/807) |

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

- **Régi arany (2.2): 1/1, a `Zep.3.9 H7121+H8034` hármas** („segítségül hívják az Úr nevét”). A párosítás (`Sof 3:9`) a „segítségül” (hu 10) és a „hívják” (hu 11) szót a 9. eredeti tokenre köti (קְרֹ֤א, H7121), a „nevét” (hu 14) szót a 13. tokenre (שֵׁ֣ם, H8034); mindkét összetevő megvan, a hármas a várt tokenekre párosult. A hármas nem szerepel az `f21p/regi_arany_hibas.tsv`-ben.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9 (`adat/datasetek.tsv`, `adat/SEMA.md` 2.20) és a brief fejléce/D43/v2.37: a kilenc könyv után, közös tételben (l. a brief D43).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: az orkesztrátor hívja (nem e menet dolga); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.

