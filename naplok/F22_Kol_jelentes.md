# F22_Kol_jelentes.md — Károli–Strong párosítás: Kol (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Kol`, `egyesit.py --konyv Kol` és `--ellenoriz`, `f22_elemzes.py --konyv Kol`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Kol-soraiból: `futas = api_termeles/high/Kol`, `cimke = kol`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Kol'`).
- **Minta:** `f22/minta_Kol.tsv`, 95 vers a modellhez, 10 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01DSVwwhLb3S1h5sKmjRUbV4`, 10 kérés (2026-10-12T09:22:23+00:00); 2. kör `msgbatch_01WBGA3yZSqMrf4Zqdeep3JA`, 1 kérés (2026-10-12T09:32:42+00:00).
- **Futásnapló** (Kol: 11 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 10 | 9 | 1 köteg | 0.4536 | 93 059 / 72 107 |
| 2. próba (javító) | 1 | 1 | 0 köteg | 0.0571 | 10 588 / 9 297 |
| **összesen** | 11 | | | **0.5107** | |

A javító körbe került köteg: k007 (10 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”); a válasz csak a Kol 3:9-et hozza (kétszer), a Kol 3:10–18 (9 vers) hiányzik (a független ellenőr jelzése nyomán pontosítva). A javító kör mind a 10 verset hozta.

Költségplafon: a könyvplafon 95 vers × 0,0074 × 1,5 = 1.0545 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.05 USD); a könyv költsége 0.5107 USD (versenként 0.0054 USD, a modellhez ment 95 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó Kol-sora: 88.655903 USD, a 18 USD-s ÚSZ-keretből (D45: 86,3698 + 18; a kódbeli plafon `PLAFON_USD` = 104,36 USD).

## 1a. Szkriptkimenet

```
Sonnet: 10 köteg, 95 vers; kapuhiba első próbára 10.5% (10/95); végleg 0.0% (0/95)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Kol`: parok: 1579 sor {'alacsony': 1579}; szavak: 3290 sor {'alacsony': 3290}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 316 `betoldas`, 1343 `parositva`; er 254 `forditatlan`, 1377 `parositva`. Az átnézési sor (`naplok/F22_Kol_atnezes.tsv`): 0 vers.

`egyesit.py --konyv Kol --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

45 `[nem TR]` token; állapot szerint: 35 `forditatlan`, 10 `parositva`. Eltérés az elvárttól (`forditatlan`): Kol 2:2 er 6 (συμβιβασθέντες, G4822) → parositva; Kol 2:2 er 13 (πλοῦτος, G4149) → parositva; Kol 2:12 er 5 (βαπτισμῷ, G0909) → parositva; Kol 3:22 er 12 (ὀφθαλμοδουλίᾳ, G3787) → parositva; Kol 3:22 er 21 (κύριον., G2962) → parositva; Kol 4:1 er 18 (οὐρανῷ.¶, G3772) → parositva; Kol 4:12 er 18 (σταθῆτε, G2476) → parositva; Kol 4:12 er 21 (πεπληροφορημένοι, G4135) → parositva; Kol 4:15 er 7 (Νύμφαν, G3564) → parositva; Kol 4:15 er 12 (αὐτῆς, G0846) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Kol` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1579), alacsony 100.0% (1579/1579), kezi 0.0% (0/1579); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/3290), alacsony 100.0% (3290/3290), kezi 0.0% (0/3290).

Link-forrás megoszlás (parok): S 1579. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 95 (Kol 1:1, Kol 1:10, Kol 1:11, Kol 1:12, Kol 1:13, Kol 1:14, Kol 1:15, Kol 1:16, Kol 1:17, Kol 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 521 | 0.0% (0/521) | 100.0% (521/521) | 0.0% (0/521) | 1097 | 0.0% (0/1097) | 100.0% (1097/1097) | 0.0% (0/1097) |
| 2 | 410 | 0.0% (0/410) | 100.0% (410/410) | 0.0% (0/410) | 835 | 0.0% (0/835) | 100.0% (835/835) | 0.0% (0/835) |
| 3 | 361 | 0.0% (0/361) | 100.0% (361/361) | 0.0% (0/361) | 758 | 0.0% (0/758) | 100.0% (758/758) | 0.0% (0/758) |
| 4 | 287 | 0.0% (0/287) | 100.0% (287/287) | 0.0% (0/287) | 600 | 0.0% (0/600) | 100.0% (600/600) | 0.0% (0/600) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4.

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

A felhasználó döntése szerint (chat, 2026.10.12) a 48 zárójeles csoport (`naplok/F22_TAGNT_zarojeles_sorok.md`: a nyers TAGNT `[..]`/`{..}` sorai a `TAGNT_kivonat.tsv`-ből kimaradtak) érintett versei `kezi` bizonyosságúak, `fuggoben` állapotúak, link nélkül, mert a részleges görög szöveg hamis `betoldas` jelölést adhatott. A Károli-kulcs (NRSV vagy KJV/egyéb) a kivonat javítása előtt nem dönthető el, ezért **mindkét kulcs** verse jelölt, ha a Károliban létezik. Eszköz: `f22/kezi_versek_Kol.tsv` (az `egyesit.py` `kezi_felulir`-je; API nélkül újraépítve).

- Érintett versek: Kol 1:11, Kol 1:12, Kol 1:22, Kol 1:21.
- `parok_Kol.tsv`: 1579 → 1526 link; `szavak_Kol.tsv` (változott állapotok): er `forditatlan` 254 → 238; er `fuggoben` 0 → 63; er `parositva` 1377 → 1330; hu `betoldas` 316 → 300; hu `fuggoben` 0 → 62; hu `parositva` 1343 → 1297.
- Átnézési sor (`naplok/F22_Kol_atnezes.tsv`): 4.
- `egyesit.py --konyv Kol --ellenoriz`: „rendben”. A fenti 1–5. szakasz számai a javítás előtti állapotot írják le.
