# F22_2Tim_jelentes.md — Károli–Strong párosítás: 2Tim (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 2Tim`, `egyesit.py --konyv 2Tim` és `--ellenoriz`, `f22_elemzes.py --konyv 2Tim`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 2Tim-soraiból: `futas = api_termeles/high/2Tim`, `cimke = 2tim`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'2Tim'`).
- **Minta:** `f22/minta_2Tim.tsv`, 83 vers a modellhez, 9 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01JNVmeA3Ro56fVhZJt8QZB6`, 9 kérés (2026-10-12T09:08:55+00:00); 2. kör `msgbatch_01DyNK64Nz9P3e2rK6AMcgQf`, 4 kérés (2026-10-12T09:12:07+00:00).
- **Futásnapló** (2Tim: 13 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 9 | 5 | 4 köteg | 0.2720 | 79 295 / 38 542 |
| 2. próba (javító) | 4 | 4 | 0 köteg | 0.1398 | 39 348 / 20 081 |
| **összesen** | 13 | | | **0.4118** | |

A javító körbe került köteg: k003 (10 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k007 (10 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k008 (10 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k009 (3 vers); versenkénti kapuhiba: 4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban ne. A javító kör eredménye a fenti táblában.

Költségplafon: a könyvplafon 83 vers × 0,0074 × 1,5 = 0.9213 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.00 USD); a könyv költsége 0.4118 USD (versenként 0.0050 USD, a modellhez ment 83 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó 2Tim-sora: 87.637859 USD, a 18 USD-s ÚSZ-keretből (D45: 86,3698 + 18; a kódbeli plafon `PLAFON_USD` = 104,36 USD).

## 1a. Szkriptkimenet

```
Sonnet: 9 köteg, 83 vers; kapuhiba első próbára 37.3% (31/83); végleg 0.0% (0/83)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 2Tim`: parok: 1220 sor {'alacsony': 1220}; szavak: 2568 sor {'alacsony': 2568}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 228 `betoldas`, 1067 `parositva`; er 174 `forditatlan`, 1099 `parositva`. Az átnézési sor (`naplok/F22_2Tim_atnezes.tsv`): 0 vers.

`egyesit.py --konyv 2Tim --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

21 `[nem TR]` token; állapot szerint: 21 `forditatlan`. Eltérés az elvárttól (`forditatlan`) nincs.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 2Tim` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1220), alacsony 100.0% (1220/1220), kezi 0.0% (0/1220); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/2568), alacsony 100.0% (2568/2568), kezi 0.0% (0/2568).

Link-forrás megoszlás (parok): S 1220. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 83 (2Tim 1:1, 2Tim 1:10, 2Tim 1:11, 2Tim 1:12, 2Tim 1:13, 2Tim 1:14, 2Tim 1:15, 2Tim 1:16, 2Tim 1:17, 2Tim 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 322 | 0.0% (0/322) | 100.0% (322/322) | 0.0% (0/322) | 645 | 0.0% (0/645) | 100.0% (645/645) | 0.0% (0/645) |
| 2 | 359 | 0.0% (0/359) | 100.0% (359/359) | 0.0% (0/359) | 768 | 0.0% (0/768) | 100.0% (768/768) | 0.0% (0/768) |
| 3 | 238 | 0.0% (0/238) | 100.0% (238/238) | 0.0% (0/238) | 485 | 0.0% (0/485) | 100.0% (485/485) | 0.0% (0/485) |
| 4 | 301 | 0.0% (0/301) | 100.0% (301/301) | 0.0% (0/301) | 670 | 0.0% (0/670) | 100.0% (670/670) | 0.0% (0/670) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4.

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

- Nincs jelölt pont: az átnézési sorok száma 0 (nincs `kezi` vers).
- Régi arany: l. a 2.2-t; az eltérő hármasok tartalmi ítélete a felhasználóé (nem e menet dolga).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- Az A csomag összesítője: `naplok/F22_USZ_A_jelentes.md` (a 11 könyv után).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a 11 könyv után, közösen (`naplok/ELLENOR_F22_USZ_A.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
