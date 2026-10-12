# F22_1Pet_jelentes.md — Károli–Strong párosítás: 1Pét (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 1Pét`, `egyesit.py --konyv 1Pét` és `--ellenoriz`, `f22_elemzes.py --konyv 1Pét`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 1Pét-soraiból: `futas = api_termeles/high/1Pet`, `cimke = 1pet`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'1Pét'`).
- **Minta:** `f22/minta_1Pet.tsv`, 105 vers a modellhez, 11 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01DeXvQVr8St6UUAAx1sNMdT`, 11 kérés (2026-10-12T09:42:00+00:00).
- **Futásnapló** (1Pét: 11 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 11 | 11 | 0 köteg | 0.5728 | 102 829 / 93 988 |
| **összesen** | 11 | | | **0.5728** | |

Költségplafon: a könyvplafon 105 vers × 0,0074 × 1,5 = 1.1655 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.17 USD); a könyv költsége 0.5728 USD (versenként 0.0055 USD, a modellhez ment 105 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó 1Pét-sora: 89.726155 USD, a 18 USD-s ÚSZ-keretből (D45: 86,3698 + 18; a kódbeli plafon `PLAFON_USD` = 104,36 USD).

## 1a. Szkriptkimenet

```
Sonnet: 11 köteg, 105 vers; kapuhiba első próbára 0.0% (0/105); végleg 0.0% (0/105)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 1Pét`: parok: 1677 sor {'alacsony': 1677}; szavak: 3585 sor {'alacsony': 3585}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 372 `betoldas`, 1484 `parositva`; er 240 `forditatlan`, 1489 `parositva`. Az átnézési sor (`naplok/F22_1Pet_atnezes.tsv`): 0 vers.

`egyesit.py --konyv 1Pét --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

53 `[nem TR]` token; állapot szerint: 52 `forditatlan`, 1 `parositva`. Eltérés az elvárttól (`forditatlan`): 1Pét 3:1 er 22 (κερδηθήσονται,, G2770) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 1Pét` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1677), alacsony 100.0% (1677/1677), kezi 0.0% (0/1677); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/3585), alacsony 100.0% (3585/3585), kezi 0.0% (0/3585).

Link-forrás megoszlás (parok): S 1677. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 105 (1Pét 1:1, 1Pét 1:10, 1Pét 1:11, 1Pét 1:12, 1Pét 1:13, 1Pét 1:14, 1Pét 1:15, 1Pét 1:16, 1Pét 1:17, 1Pét 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 426 | 0.0% (0/426) | 100.0% (426/426) | 0.0% (0/426) | 888 | 0.0% (0/888) | 100.0% (888/888) | 0.0% (0/888) |
| 2 | 383 | 0.0% (0/383) | 100.0% (383/383) | 0.0% (0/383) | 812 | 0.0% (0/812) | 100.0% (812/812) | 0.0% (0/812) |
| 3 | 363 | 0.0% (0/363) | 100.0% (363/363) | 0.0% (0/363) | 782 | 0.0% (0/782) | 100.0% (782/782) | 0.0% (0/782) |
| 4 | 304 | 0.0% (0/304) | 100.0% (304/304) | 0.0% (0/304) | 654 | 0.0% (0/654) | 100.0% (654/654) | 0.0% (0/654) |
| 5 | 201 | 0.0% (0/201) | 100.0% (201/201) | 0.0% (0/201) | 449 | 0.0% (0/449) | 100.0% (449/449) | 0.0% (0/449) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5.

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

## 6. Utólagos javítás (N-F22c, 2026.10.12)

A felhasználó döntése szerint (chat, 2026.10.12) a 48 zárójeles csoport (`naplok/F22_TAGNT_zarojeles_sorok.md`: a nyers TAGNT `[..]`/`{..}` sorai a `TAGNT_kivonat.tsv`-ből kimaradtak) érintett versei `kezi` bizonyosságúak, `fuggoben` állapotúak, link nélkül, mert a részleges görög szöveg hamis `betoldas` jelölést adhatott. A Károli-kulcs (NRSV vagy KJV/egyéb) a kivonat javítása előtt nem dönthető el, ezért **mindkét kulcs** verse jelölt, ha a Károliban létezik. Eszköz: `f22/kezi_versek_1Pet.tsv` (az `egyesit.py` `kezi_felulir`-je; API nélkül újraépítve).

- Érintett versek: 1Pét 3:16, 1Pét 3:15.
- `parok_1Pet.tsv`: 1677 → 1638 link; `szavak_1Pet.tsv` (változott állapotok): er `forditatlan` 240 → 231; er `fuggoben` 0 → 43; er `parositva` 1489 → 1455; hu `betoldas` 372 → 356; hu `fuggoben` 0 → 46; hu `parositva` 1484 → 1454.
- Átnézési sor (`naplok/F22_1Pet_atnezes.tsv`): 2.
- `egyesit.py --konyv 1Pét --ellenoriz`: „rendben”. A fenti 1–5. szakasz számai a javítás előtti állapotot írják le.
