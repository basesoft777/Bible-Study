# F22_1Tim_jelentes.md — Károli–Strong párosítás: 1Tim (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 1Tim`, `egyesit.py --konyv 1Tim` és `--ellenoriz`, `f22_elemzes.py --konyv 1Tim`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 1Tim-soraiból: `futas = api_termeles/high/1Tim`, `cimke = 1tim`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'1Tim'`).
- **Minta:** `f22/minta_1Tim.tsv`, 113 vers a modellhez, 12 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01DgnumiZzUS9jcSJpEmRisr`, 12 kérés (2026-10-12T09:51:54+00:00); 2. kör `msgbatch_01YNFQXCnXQLov7E6v69Ubqe`, 2 kérés (2026-10-12T09:56:07+00:00).
- **Futásnapló** (1Tim: 14 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 12 | 10 | 2 köteg | 0.4678 | 105 183 / 72 518 |
| 2. próba (javító) | 2 | 2 | 0 köteg | 0.0751 | 20 663 / 10 894 |
| **összesen** | 14 | | | **0.5429** | |

A javító körbe került köteg: k003 (10 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k004 (10 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

Költségplafon: a könyvplafon 113 vers × 0,0074 × 1,5 = 1.2543 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.25 USD); a könyv költsége 0.5429 USD (versenként 0.0048 USD, a modellhez ment 113 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó 1Tim-sora: 91.437851 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 12 köteg, 113 vers; kapuhiba első próbára 17.7% (20/113); végleg 0.0% (0/113)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 1Tim`: parok: 1643 sor {'alacsony': 1643}; szavak: 3409 sor {'alacsony': 3409}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 293 `betoldas`, 1493 `parositva`; er 157 `forditatlan`, 1466 `parositva`. Az átnézési sor (`naplok/F22_1Tim_atnezes.tsv`): 0 vers.

`egyesit.py --konyv 1Tim --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

21 `[nem TR]` token; állapot szerint: 19 `forditatlan`, 2 `parositva`. Eltérés az elvárttól (`forditatlan`): 1Tim 2:14 er 8 (ἐξαπατηθεῖσα, G1818) → parositva; 1Tim 6:11 er 16 (πραϋπαθίαν·, G6073) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 1Tim` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1643), alacsony 100.0% (1643/1643), kezi 0.0% (0/1643); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/3409), alacsony 100.0% (3409/3409), kezi 0.0% (0/3409).

Link-forrás megoszlás (parok): S 1643. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 113 (1Tim 1:1, 1Tim 1:10, 1Tim 1:11, 1Tim 1:12, 1Tim 1:13, 1Tim 1:14, 1Tim 1:15, 1Tim 1:16, 1Tim 1:17, 1Tim 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 313 | 0.0% (0/313) | 100.0% (313/313) | 0.0% (0/313) | 644 | 0.0% (0/644) | 100.0% (644/644) | 0.0% (0/644) |
| 2 | 191 | 0.0% (0/191) | 100.0% (191/191) | 0.0% (0/191) | 386 | 0.0% (0/386) | 100.0% (386/386) | 0.0% (0/386) |
| 3 | 209 | 0.0% (0/209) | 100.0% (209/209) | 0.0% (0/209) | 435 | 0.0% (0/435) | 100.0% (435/435) | 0.0% (0/435) |
| 4 | 222 | 0.0% (0/222) | 100.0% (222/222) | 0.0% (0/222) | 474 | 0.0% (0/474) | 100.0% (474/474) | 0.0% (0/474) |
| 5 | 354 | 0.0% (0/354) | 100.0% (354/354) | 0.0% (0/354) | 730 | 0.0% (0/730) | 100.0% (730/730) | 0.0% (0/730) |
| 6 | 354 | 0.0% (0/354) | 100.0% (354/354) | 0.0% (0/354) | 740 | 0.0% (0/740) | 100.0% (740/740) | 0.0% (0/740) |

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

- Nincs jelölt pont: az átnézési sorok száma 0 (nincs `kezi` vers).
- Régi arany: a könyvben 0 hármas, az egyezés **nem mérhető** (kimondva, nem pótolva).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- Az A csomag összesítője: `naplok/F22_USZ_A_jelentes.md` (a 11 könyv után).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a 11 könyv után, közösen (`naplok/ELLENOR_F22_USZ_A.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.

## 6. Utólagos javítás (N-F22c, 2026.10.12)

A felhasználó döntése szerint (chat, 2026.10.12) a 48 zárójeles csoport (`naplok/F22_TAGNT_zarojeles_sorok.md`: a nyers TAGNT `[..]`/`{..}` sorai a `TAGNT_kivonat.tsv`-ből kimaradtak) érintett versei `kezi` bizonyosságúak, `fuggoben` állapotúak, link nélkül, mert a részleges görög szöveg hamis `betoldas` jelölést adhatott. A Károli-kulcs (NRSV vagy KJV/egyéb) a kivonat javítása előtt nem dönthető el, ezért **mindkét kulcs** verse jelölt, ha a Károliban létezik. Eszköz: `f22/kezi_versek_1Tim.tsv` (az `egyesit.py` `kezi_felulir`-je; API nélkül újraépítve).

- Érintett versek: 1Tim 6:21.
- `parok_1Tim.tsv`: 1643 → 1636 link; `szavak_1Tim.tsv` (változott állapotok): er `forditatlan` 157 → 156; er `fuggoben` 0 → 7; er `parositva` 1466 → 1460; hu `betoldas` 293 → 289; hu `fuggoben` 0 → 11; hu `parositva` 1493 → 1486.
- Átnézési sor (`naplok/F22_1Tim_atnezes.tsv`): 1.
- `egyesit.py --konyv 1Tim --ellenoriz`: „rendben”. A fenti 1–5. szakasz számai a javítás előtti állapotot írják le.
