# F22_2Pet_jelentes.md — Károli–Strong párosítás: 2Pét (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 2Pét`, `egyesit.py --konyv 2Pét` és `--ellenoriz`, `f22_elemzes.py --konyv 2Pét`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 2Pét-soraiból: `futas = api_termeles/high/2Pet`, `cimke = 2pet`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'2Pét'`).
- **Minta:** `f22/minta_2Pet.tsv`, 61 vers a modellhez, 7 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01Awv6C58oGeLc5eMwL8Jru9`, 7 kérés (2026-10-12T09:02:26+00:00); 2. kör `msgbatch_012B6XxzcyP4frWFQgAtvhEt`, 1 kérés (2026-10-12T09:06:08+00:00).
- **Futásnapló** (2Pét: 8 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 7 | 6 | 1 köteg | 0.3416 | 65 480 / 55 222 |
| 2. próba (javító) | 1 | 1 | 0 köteg | 0.0177 | 11 899 / 1 154 |
| **összesen** | 8 | | | **0.3593** | |

A javító körbe került köteg: k005 (10 vers); versenkénti kapuhiba: 4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban ne. A javító kör eredménye a fenti táblában.

Költségplafon: a könyvplafon 61 vers × 0,0074 × 1,5 = 0.6771 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.00 USD); a könyv költsége 0.3593 USD (versenként 0.0059 USD, a modellhez ment 61 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó 2Pét-sora: 87.226101 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 7 köteg, 61 vers; kapuhiba első próbára 1.6% (1/61); végleg 0.0% (0/61)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 2Pét`: parok: 1052 sor {'alacsony': 1052}; szavak: 2315 sor {'alacsony': 2315}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 262 `betoldas`, 941 `parositva`; er 164 `forditatlan`, 948 `parositva`. Az átnézési sor (`naplok/F22_2Pet_atnezes.tsv`): 0 vers.

`egyesit.py --konyv 2Pét --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

36 `[nem TR]` token; állapot szerint: 34 `forditatlan`, 2 `parositva`. Eltérés az elvárttól (`forditatlan`): 2Pét 2:21 er 13 (ὑποστρέψαι, G5290) → parositva; 2Pét 2:22 er 18 (κυλισμὸν, G2946) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 2Pét` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1052), alacsony 100.0% (1052/1052), kezi 0.0% (0/1052); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/2315), alacsony 100.0% (2315/2315), kezi 0.0% (0/2315).

Link-forrás megoszlás (parok): S 1052. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 61 (2Pét 1:1, 2Pét 1:10, 2Pét 1:11, 2Pét 1:12, 2Pét 1:13, 2Pét 1:14, 2Pét 1:15, 2Pét 1:16, 2Pét 1:17, 2Pét 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 362 | 0.0% (0/362) | 100.0% (362/362) | 0.0% (0/362) | 786 | 0.0% (0/786) | 100.0% (786/786) | 0.0% (0/786) |
| 2 | 357 | 0.0% (0/357) | 100.0% (357/357) | 0.0% (0/357) | 821 | 0.0% (0/821) | 100.0% (821/821) | 0.0% (0/821) |
| 3 | 333 | 0.0% (0/333) | 100.0% (333/333) | 0.0% (0/333) | 708 | 0.0% (0/708) | 100.0% (708/708) | 0.0% (0/708) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3.

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

- Nincs jelölt pont: az átnézési sorok száma 0 (nincs `kezi` vers).
- Régi arany: l. a 2.2-t; az eltérő hármasok tartalmi ítélete a felhasználóé (nem e menet dolga).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- Az A csomag összesítője: `naplok/F22_USZ_A_jelentes.md` (a 11 könyv után).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a 11 könyv után, közösen (`naplok/ELLENOR_F22_USZ_A.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
