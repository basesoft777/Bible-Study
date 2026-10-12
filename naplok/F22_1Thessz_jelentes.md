# F22_1Thessz_jelentes.md — Károli–Strong párosítás: 1Thessz (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 1Thessz`, `egyesit.py --konyv 1Thessz` és `--ellenoriz`, `f22_elemzes.py --konyv 1Thessz`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 1Thessz-soraiból: `futas = api_termeles/high/1Thessz`, `cimke = 1thessz`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'1Thessz'`).
- **Minta:** `f22/minta_1Thessz.tsv`, 89 vers a modellhez, 9 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_017AKMhLwTh2Q4Dg56UUGPbe`, 9 kérés (2026-10-12T09:15:55+00:00); 2. kör `msgbatch_01GuhAepcPeG7B1EmEwJrC4j`, 4 kérés (2026-10-12T09:19:37+00:00).
- **Futásnapló** (1Thessz: 13 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 9 | 5 | 4 köteg | 0.4144 | 85 579 / 65 772 |
| 2. próba (javító) | 4 | 4 | 0 köteg | 0.0929 | 43 683 / 9 851 |
| **összesen** | 13 | | | **0.5074** | |

A javító körbe került köteg: k001 (10 vers); versenkénti kapuhiba: 4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban ne. A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k002 (10 vers); versenkénti kapuhiba: 4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban ne. A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k007 (10 vers); versenkénti kapuhiba: 1. hibás pár (kell: [magyar_sorszam, [eredeti_sorszam, ...]], nem üres): [4, []]. A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k009 (9 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

Költségplafon: a könyvplafon 89 vers × 0,0074 × 1,5 = 0.9879 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.00 USD); a könyv költsége 0.5074 USD (versenként 0.0057 USD, a modellhez ment 89 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó 1Thessz-sora: 88.145236 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 9 köteg, 89 vers; kapuhiba első próbára 13.5% (12/89); végleg 0.0% (0/89)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 1Thessz`: parok: 1478 sor {'alacsony': 1478}; szavak: 3063 sor {'alacsony': 3063}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 286 `betoldas`, 1275 `parositva`; er 209 `forditatlan`, 1293 `parositva`. Az átnézési sor (`naplok/F22_1Thessz_atnezes.tsv`): 0 vers.

`egyesit.py --konyv 1Thessz --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

36 `[nem TR]` token; állapot szerint: 34 `forditatlan`, 2 `parositva`. Eltérés az elvárttól (`forditatlan`): 1Thessz 1:7 er 4 (τύπον, G5179) → parositva; 1Thessz 2:3 er 11 (οὐδὲ, G3761) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 1Thessz` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1478), alacsony 100.0% (1478/1478), kezi 0.0% (0/1478); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/3063), alacsony 100.0% (3063/3063), kezi 0.0% (0/3063).

Link-forrás megoszlás (parok): S 1478. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 89 (1Thessz 1:1, 1Thessz 1:10, 1Thessz 1:2, 1Thessz 1:3, 1Thessz 1:4, 1Thessz 1:5, 1Thessz 1:6, 1Thessz 1:7, 1Thessz 1:8, 1Thessz 1:9).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 213 | 0.0% (0/213) | 100.0% (213/213) | 0.0% (0/213) | 435 | 0.0% (0/435) | 100.0% (435/435) | 0.0% (0/435) |
| 2 | 374 | 0.0% (0/374) | 100.0% (374/374) | 0.0% (0/374) | 794 | 0.0% (0/794) | 100.0% (794/794) | 0.0% (0/794) |
| 3 | 272 | 0.0% (0/272) | 100.0% (272/272) | 0.0% (0/272) | 527 | 0.0% (0/527) | 100.0% (527/527) | 0.0% (0/527) |
| 4 | 295 | 0.0% (0/295) | 100.0% (295/295) | 0.0% (0/295) | 631 | 0.0% (0/631) | 100.0% (631/631) | 0.0% (0/631) |
| 5 | 324 | 0.0% (0/324) | 100.0% (324/324) | 0.0% (0/324) | 676 | 0.0% (0/676) | 100.0% (676/676) | 0.0% (0/676) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 1; a Károli-szó/kifejezés nem található a vers tokenjei közt: 1.
- **Mért érték (kizárás nélkül, minden link):** 0.0% (0/1).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/1).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): n.é. (0/0).

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
