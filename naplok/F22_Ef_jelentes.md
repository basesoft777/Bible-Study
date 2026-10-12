# F22_Ef_jelentes.md — Károli–Strong párosítás: Ef (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Ef`, `egyesit.py --konyv Ef` és `--ellenoriz`, `f22_elemzes.py --konyv Ef`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Ef-soraiból: `futas = api_termeles/high/Ef`, `cimke = ef`). Ág: `claude/f22-usz-b`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 B csomag (Gal, Ef, Zsid; a 2Kor visszatartva; D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „Gal, Ef, Zsid mehet. A 2Kor-t tartsd vissza …”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Ef'`).
- **Minta:** `f22/minta_Ef.tsv`, 155 vers a modellhez, 16 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_013nQhiKCXUYUy985YMz7pPe`, 16 kérés (2026-10-12T10:42:42+00:00); 2. kör `msgbatch_01DnJifCHLhQzvVVbFebyGps`, 2 kérés (2026-10-12T10:45:53+00:00).
- **Futásnapló** (Ef: 18 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 16 | 14 | 2 köteg | 0.7203 | 144 346 / 115 200 |
| 2. próba (javító) | 2 | 2 | 0 köteg | 0.0508 | 21 716 / 5 813 |
| **összesen** | 18 | | | **0.7711** | |

A javító körbe került köteg: k003 (10 vers); versenkénti kapuhiba: 3. ezek a magyar szavak sem a "parok" bal oldalán, sem a "betoldas"-ban nem szer. A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k012 (10 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

Költségplafon: a könyvplafon 155 vers × 0,0074 × 1,5 = 1.7205 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.72 USD); a könyv költsége 0.7711 USD (versenként 0.0050 USD, a modellhez ment 155 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó Ef-sora: 92.900461 USD, a 18 USD-s ÚSZ-keretből (D45: 86,3698 + 18; a kódbeli plafon `PLAFON_USD` = 104,36 USD).

## 1a. Szkriptkimenet

```
Sonnet: 16 köteg, 155 vers; kapuhiba első próbára 7.1% (11/155); végleg 0.0% (0/155)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Ef`: parok: 2201 sor {'alacsony': 2201}; szavak: 4885 sor {'alacsony': 4671, 'kezi': 214}; átnézési sor: 6 vers; ellenőrzés: rendben

A szavak bontása: hu 433 `betoldas`, 116 `fuggoben`, 1866 `parositva`; er 409 `forditatlan`, 98 `fuggoben`, 1963 `parositva`. Az átnézési sor (`naplok/F22_Ef_atnezes.tsv`): 6 vers.

`egyesit.py --konyv Ef --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

54 `[nem TR]` token; állapot szerint: 49 `forditatlan`, 3 `fuggoben`, 2 `parositva`. Eltérés az elvárttól (`forditatlan`): Ef 1:10 er 15 (ἐπὶ, G1909) → fuggoben; Ef 2:15 er 13 (αὐτῷ, G0846) → fuggoben; Ef 3:6 er 15 (Ἰησοῦ, G2424) → parositva; Ef 5:14 er 3 (ἔγειρε, G1453) → fuggoben; Ef 6:19 er 6 (δοθῇ, G1325) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Ef` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/2201), alacsony 100.0% (2201/2201), kezi 0.0% (0/2201); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/4885), alacsony 95.6% (4671/4885), kezi 4.4% (214/4885).

Link-forrás megoszlás (parok): S 2201. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 149 (Ef 1:1, Ef 1:12, Ef 1:13, Ef 1:14, Ef 1:15, Ef 1:16, Ef 1:17, Ef 1:18, Ef 1:19, Ef 1:2).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 346 | 0.0% (0/346) | 100.0% (346/346) | 0.0% (0/346) | 792 | 0.0% (0/792) | 89.4% (708/792) | 10.6% (84/792) |
| 2 | 304 | 0.0% (0/304) | 100.0% (304/304) | 0.0% (0/304) | 712 | 0.0% (0/712) | 89.5% (637/712) | 10.5% (75/712) |
| 3 | 304 | 0.0% (0/304) | 100.0% (304/304) | 0.0% (0/304) | 683 | 0.0% (0/683) | 100.0% (683/683) | 0.0% (0/683) |
| 4 | 462 | 0.0% (0/462) | 100.0% (462/462) | 0.0% (0/462) | 979 | 0.0% (0/979) | 100.0% (979/979) | 0.0% (0/979) |
| 5 | 406 | 0.0% (0/406) | 100.0% (406/406) | 0.0% (0/406) | 939 | 0.0% (0/939) | 94.1% (884/939) | 5.9% (55/939) |
| 6 | 379 | 0.0% (0/379) | 100.0% (379/379) | 0.0% (0/379) | 780 | 0.0% (0/780) | 100.0% (780/780) | 0.0% (0/780) |

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

- `Ef 1:10`: N-F22c: a nyers TAGNT `Eph.1.10{1.11}` sorai (2 szó) a kivonatból kimaradtak; a vers a NRSV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Ef 1:11`: N-F22c: a nyers TAGNT `Eph.1.10{1.11}` sorai (2 szó) a kivonatból kimaradtak; a vers a egyéb-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Ef 2:14`: N-F22c: a nyers TAGNT `Eph.2.14[2.15]` sorai (6 szó) a kivonatból kimaradtak; a vers a NRSV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Ef 2:15`: N-F22c: a nyers TAGNT `Eph.2.14[2.15]` sorai (6 szó) a kivonatból kimaradtak; a vers a KJV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Ef 5:13`: N-F22c: a nyers TAGNT `Eph.5.14[5.13]` sorai (6 szó) a kivonatból kimaradtak; a vers a KJV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Ef 5:14`: N-F22c: a nyers TAGNT `Eph.5.14[5.13]` sorai (6 szó) a kivonatból kimaradtak; a vers a NRSV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- Régi arany: a könyvben 0 hármas, az egyezés **nem mérhető** (kimondva, nem pótolva).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- A B csomag összesítője: `naplok/F22_USZ_B_jelentes.md`.

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a csomag után, közösen (`naplok/ELLENOR_F22_USZ_B.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
