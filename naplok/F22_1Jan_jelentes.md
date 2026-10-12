# F22_1Jan_jelentes.md — Károli–Strong párosítás: 1Ján (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 1Ján`, `egyesit.py --konyv 1Ján` és `--ellenoriz`, `f22_elemzes.py --konyv 1Ján`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 1Ján-soraiból: `futas = api_termeles/high/1Jan`, `cimke = 1jan`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'1Ján'`).
- **Minta:** `f22/minta_1Jan.tsv`, 105 vers a modellhez, 11 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_019N11W1PGnCV7XFs1GQUGoW`, 11 kérés (2026-10-12T09:45:17+00:00).
- **Futásnapló** (1Ján: 11 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 11 | 11 | 0 köteg | 0.6526 | 110 427 / 108 432 |
| **összesen** | 11 | | | **0.6526** | |

Költségplafon: a könyvplafon 105 vers × 0,0074 × 1,5 = 1.1655 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.17 USD); a könyv költsége 0.6526 USD (versenként 0.0062 USD, a modellhez ment 105 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó 1Ján-sora: 90.378742 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 11 köteg, 105 vers; kapuhiba első próbára 0.0% (0/105); végleg 0.0% (0/105)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 1Ján`: parok: 2072 sor {'alacsony': 2072}; szavak: 4343 sor {'alacsony': 4343}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 376 `betoldas`, 1776 `parositva`; er 365 `forditatlan`, 1826 `parositva`. Az átnézési sor (`naplok/F22_1Jan_atnezes.tsv`): 0 vers.

`egyesit.py --konyv 1Ján --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

43 `[nem TR]` token; állapot szerint: 42 `forditatlan`, 1 `parositva`. Eltérés az elvárttól (`forditatlan`): 1Ján 1:5 er 5 (ἀγγελία, G0031) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 1Ján` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/2072), alacsony 100.0% (2072/2072), kezi 0.0% (0/2072); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/4343), alacsony 100.0% (4343/4343), kezi 0.0% (0/4343).

Link-forrás megoszlás (parok): S 2072. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 105 (1Ján 1:1, 1Ján 1:10, 1Ján 1:2, 1Ján 1:3, 1Ján 1:4, 1Ján 1:5, 1Ján 1:6, 1Ján 1:7, 1Ján 1:8, 1Ján 1:9).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 203 | 0.0% (0/203) | 100.0% (203/203) | 0.0% (0/203) | 399 | 0.0% (0/399) | 100.0% (399/399) | 0.0% (0/399) |
| 2 | 551 | 0.0% (0/551) | 100.0% (551/551) | 0.0% (0/551) | 1184 | 0.0% (0/1184) | 100.0% (1184/1184) | 0.0% (0/1184) |
| 3 | 478 | 0.0% (0/478) | 100.0% (478/478) | 0.0% (0/478) | 962 | 0.0% (0/962) | 100.0% (962/962) | 0.0% (0/962) |
| 4 | 421 | 0.0% (0/421) | 100.0% (421/421) | 0.0% (0/421) | 881 | 0.0% (0/881) | 100.0% (881/881) | 0.0% (0/881) |
| 5 | 419 | 0.0% (0/419) | 100.0% (419/419) | 0.0% (0/419) | 917 | 0.0% (0/917) | 100.0% (917/917) | 0.0% (0/917) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5.

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

A felhasználó döntése szerint (chat, 2026.10.12) a 48 zárójeles csoport (`naplok/F22_TAGNT_zarojeles_sorok.md`: a nyers TAGNT `[..]`/`{..}` sorai a `TAGNT_kivonat.tsv`-ből kimaradtak) érintett versei `kezi` bizonyosságúak, `fuggoben` állapotúak, link nélkül, mert a részleges görög szöveg hamis `betoldas` jelölést adhatott. A Károli-kulcs (NRSV vagy KJV/egyéb) a kivonat javítása előtt nem dönthető el, ezért **mindkét kulcs** verse jelölt, ha a Károliban létezik. Eszköz: `f22/kezi_versek_1Jan.tsv` (az `egyesit.py` `kezi_felulir`-je; API nélkül újraépítve).

- Érintett versek: 1Ján 2:14, 1Ján 2:13.
- `parok_1Jan.tsv`: 2072 → 2027 link; `szavak_1Jan.tsv` (változott állapotok): er `forditatlan` 365 → 361; er `fuggoben` 0 → 41; er `parositva` 1826 → 1789; hu `betoldas` 376 → 364; hu `fuggoben` 0 → 52; hu `parositva` 1776 → 1736.
- Átnézési sor (`naplok/F22_1Jan_atnezes.tsv`): 2.
- `egyesit.py --konyv 1Ján --ellenoriz`: „rendben”. A fenti 1–5. szakasz számai a javítás előtti állapotot írják le.
