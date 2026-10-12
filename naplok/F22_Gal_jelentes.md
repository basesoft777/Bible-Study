# F22_Gal_jelentes.md — Károli–Strong párosítás: Gal (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Gal`, `egyesit.py --konyv Gal` és `--ellenoriz`, `f22_elemzes.py --konyv Gal`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Gal-soraiból: `futas = api_termeles/high/Gal`, `cimke = gal`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 B csomag (Gal, Ef, Zsid; a 2Kor visszatartva; D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „Gal, Ef, Zsid mehet. A 2Kor-t tartsd vissza …”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Gal'`).
- **Minta:** `f22/minta_Gal.tsv`, 149 vers a modellhez, 15 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01NMR5W5qYtY8Ar7g8j5MJge`, 15 kérés (2026-10-12T10:19:04+00:00); 2. kör `msgbatch_015Z6Bx1zW6H5byE8pLuLn6q`, 2 kérés (2026-10-12T10:39:20+00:00).
- **Futásnapló** (Gal: 17 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 15 | 13 | 2 köteg | 0.6244 | 135 801 / 97 726 |
| 2. próba (javító) | 2 | 1 | 1 köteg | 0.0671 | 22 057 / 8 999 |
| **összesen** | 17 | | | **0.6915** | |

A javító körbe került köteg: k002 (10 vers); versenkénti kapuhiba: 3. ezek a magyar szavak többször szerepelnek (a "parok" bal oldalán vagy a "beto. A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k007 (10 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 4 column 1 (”). A javító kör eredménye a fenti táblában.

Költségplafon: a könyvplafon 149 vers × 0,0074 × 1,5 = 1.6539 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.65 USD); a könyv költsége 0.6915 USD (versenként 0.0046 USD, a modellhez ment 149 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó Gal-sora: 92.129334 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 15 köteg, 149 vers; kapuhiba első próbára 7.4% (11/149); végleg 0.7% (1/149)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Gal`: parok: 2160 sor {'alacsony': 2160}; szavak: 4608 sor {'alacsony': 4493, 'kezi': 115}; átnézési sor: 3 vers; ellenőrzés: rendben

A szavak bontása: hu 361 `betoldas`, 58 `fuggoben`, 1921 `parositva`; er 256 `forditatlan`, 57 `fuggoben`, 1955 `parositva`. Az átnézési sor (`naplok/F22_Gal_atnezes.tsv`): 3 vers.

`egyesit.py --konyv Gal --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

40 `[nem TR]` token; állapot szerint: 36 `forditatlan`, 3 `fuggoben`, 1 `parositva`. Eltérés az elvárttól (`forditatlan`): Gal 2:20 er 24 (καὶ, G2532) → fuggoben; Gal 2:20 er 25 (Χριστοῦ, G5547) → fuggoben; Gal 3:23 er 10 (συγκλειόμενοι, G4788) → fuggoben; Gal 4:30 er 16 (κληρονομήσει, G2816) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Gal` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/2160), alacsony 100.0% (2160/2160), kezi 0.0% (0/2160); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/4608), alacsony 97.5% (4493/4608), kezi 2.5% (115/4608).

Link-forrás megoszlás (parok): S 2160. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 146 (Gal 1:1, Gal 1:10, Gal 1:11, Gal 1:12, Gal 1:13, Gal 1:14, Gal 1:15, Gal 1:16, Gal 1:17, Gal 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 355 | 0.0% (0/355) | 100.0% (355/355) | 0.0% (0/355) | 721 | 0.0% (0/721) | 100.0% (721/721) | 0.0% (0/721) |
| 2 | 341 | 0.0% (0/341) | 100.0% (341/341) | 0.0% (0/341) | 804 | 0.0% (0/804) | 89.2% (717/804) | 10.8% (87/804) |
| 3 | 447 | 0.0% (0/447) | 100.0% (447/447) | 0.0% (0/447) | 953 | 0.0% (0/953) | 97.1% (925/953) | 2.9% (28/953) |
| 4 | 429 | 0.0% (0/429) | 100.0% (429/429) | 0.0% (0/429) | 913 | 0.0% (0/913) | 100.0% (913/913) | 0.0% (0/913) |
| 5 | 305 | 0.0% (0/305) | 100.0% (305/305) | 0.0% (0/305) | 658 | 0.0% (0/658) | 100.0% (658/658) | 0.0% (0/658) |
| 6 | 283 | 0.0% (0/283) | 100.0% (283/283) | 0.0% (0/283) | 559 | 0.0% (0/559) | 100.0% (559/559) | 0.0% (0/559) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6.

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

- `Gal 2:19`: N-F22c: a nyers TAGNT `Gal.2.19[2.20]` sorai (2 szó) a kivonatból kimaradtak; a vers a NRSV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Gal 2:20`: N-F22c: a nyers TAGNT `Gal.2.19[2.20]` sorai (2 szó) a kivonatból kimaradtak; a vers a KJV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Gal 3:23`: 4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban nem szerepelnek: [5]
- Régi arany: a könyvben 0 hármas, az egyezés **nem mérhető** (kimondva, nem pótolva).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- A B csomag összesítője: `naplok/F22_USZ_B_jelentes.md`.

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a csomag után, közösen (`naplok/ELLENOR_F22_USZ_B.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
