# F22_Tit_jelentes.md — Károli–Strong párosítás: Tit (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Tit`, `egyesit.py --konyv Tit` és `--ellenoriz`, `f22_elemzes.py --konyv Tit`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Tit-soraiból: `futas = api_termeles/high/Tit`, `cimke = tit`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Tit'`).
- **Minta:** `f22/minta_Tit.tsv`, 46 vers a modellhez, 5 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_011fhDoGQ8jMCAx8wcK9CYBE`, 5 kérés (2026-10-12T08:34:15+00:00); 2. kör `msgbatch_01ENTc8o4CxF23TZXoz8JA1w`, 1 kérés (2026-10-12T08:55:14+00:00).
- **Futásnapló** (Tit: 6 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 5 | 4 | 1 köteg | 0.1910 | 43 733 / 29 446 |
| 2. próba (javító) | 1 | 1 | 0 köteg | 0.0252 | 8 501 / 3 339 |
| **összesen** | 6 | | | **0.2162** | |

A javító körbe került köteg: k005 (6 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

Költségplafon: a könyvplafon 46 vers × 0,0074 × 1,5 = 0.5106 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.00 USD); a könyv költsége 0.2162 USD (versenként 0.0047 USD, a modellhez ment 46 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó Tit-sora: 86.585969 USD, a 18 USD-s ÚSZ-keretből (D45: 86,3698 + 18; a kódbeli plafon `PLAFON_USD` = 104,36 USD).

## 1a. Szkriptkimenet

```
Sonnet: 5 köteg, 46 vers; kapuhiba első próbára 13.0% (6/46); végleg 0.0% (0/46)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Tit`: parok: 657 sor {'alacsony': 657}; szavak: 1384 sor {'alacsony': 1384}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 109 `betoldas`, 595 `parositva`; er 85 `forditatlan`, 595 `parositva`. Az átnézési sor (`naplok/F22_Tit_atnezes.tsv`): 0 vers.

`egyesit.py --konyv Tit --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

11 `[nem TR]` token; állapot szerint: 11 `forditatlan`. Eltérés az elvárttól (`forditatlan`) nincs.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Tit` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/657), alacsony 100.0% (657/657), kezi 0.0% (0/657); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/1384), alacsony 100.0% (1384/1384), kezi 0.0% (0/1384).

Link-forrás megoszlás (parok): S 657. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 46 (Tit 1:1, Tit 1:10, Tit 1:11, Tit 1:12, Tit 1:13, Tit 1:14, Tit 1:15, Tit 1:16, Tit 1:2, Tit 1:3).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 246 | 0.0% (0/246) | 100.0% (246/246) | 0.0% (0/246) | 520 | 0.0% (0/520) | 100.0% (520/520) | 0.0% (0/520) |
| 2 | 181 | 0.0% (0/181) | 100.0% (181/181) | 0.0% (0/181) | 389 | 0.0% (0/389) | 100.0% (389/389) | 0.0% (0/389) |
| 3 | 230 | 0.0% (0/230) | 100.0% (230/230) | 0.0% (0/230) | 475 | 0.0% (0/475) | 100.0% (475/475) | 0.0% (0/475) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3.

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

- Nincs jelölt pont: az átnézési sorok száma 0 (nincs `kezi` vers).
- Régi arany: a könyvben 0 hármas, az egyezés **nem mérhető** (kimondva, nem pótolva).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- Az A csomag összesítője: `naplok/F22_USZ_A_jelentes.md` (a 11 könyv után).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a 11 könyv után, közösen (`naplok/ELLENOR_F22_USZ_A.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
