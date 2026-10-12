# F22_Fil_jelentes.md — Károli–Strong párosítás: Fil (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Fil`, `egyesit.py --konyv Fil` és `--ellenoriz`, `f22_elemzes.py --konyv Fil`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Fil-soraiból: `futas = api_termeles/high/Fil`, `cimke = fil`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Fil'`).
- **Minta:** `f22/minta_Fil.tsv`, 102 vers a modellhez (+ 2 eredeti vers nélküli Károli-vers, nem kerül modellhez), 11 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_016ZpGS7qWorjotjXpdwEbv1`, 11 kérés (2026-10-12T09:36:01+00:00); 2. kör `msgbatch_01BWDLYVZfTamcfLv9P6FaMr`, 2 kérés (2026-10-12T09:38:42+00:00).
- **Futásnapló** (Fil: 13 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 11 | 9 | 2 köteg | 0.4355 | 98 493 / 67 394 |
| 2. próba (javító) | 2 | 2 | 0 köteg | 0.0620 | 16 790 / 9 046 |
| **összesen** | 13 | | | **0.4975** | |

A javító körbe került köteg: k006 (10 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 5 column 1 (”); a válasz csak a Fil 2:23–25-öt hozza (kétszer), a Fil 2:26–3:2 (7 vers) hiányzik (a független ellenőr jelzése nyomán pontosítva). A javító kör mind a 10 verset hozta.

A javító körbe került köteg: k011 (2 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

Költségplafon: a könyvplafon 104 vers × 0,0074 × 1,5 = 1.1544 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.15 USD); a könyv költsége 0.4975 USD (versenként 0.0049 USD, a modellhez ment 102 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó Fil-sora: 89.153386 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 11 köteg, 102 vers; kapuhiba első próbára 11.8% (12/102); végleg 0.0% (0/102)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Fil`: parok: 1638 sor {'alacsony': 1638}; szavak: 3356 sor {'alacsony': 3331, 'kezi': 25}; átnézési sor: 2 vers; ellenőrzés: rendben

A szavak bontása: hu 308 `betoldas`, 25 `fuggoben`, 1395 `parositva`; er 194 `forditatlan`, 1434 `parositva`. Az átnézési sor (`naplok/F22_Fil_atnezes.tsv`): 2 vers.

`egyesit.py --konyv Fil --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

37 `[nem TR]` token; állapot szerint: 35 `forditatlan`, 2 `parositva`. Eltérés az elvárttól (`forditatlan`): Fil 1:11 er 2 (καρπὸν, G2590) → parositva; Fil 3:21 er 26 (αὐτῷ, G0846) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Fil` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1638), alacsony 100.0% (1638/1638), kezi 0.0% (0/1638); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/3356), alacsony 99.3% (3331/3356), kezi 0.7% (25/3356).

Link-forrás megoszlás (parok): S 1638. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 102 (Fil 1:1, Fil 1:10, Fil 1:11, Fil 1:12, Fil 1:13, Fil 1:14, Fil 1:15, Fil 1:18, Fil 1:19, Fil 1:2).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 476 | 0.0% (0/476) | 100.0% (476/476) | 0.0% (0/476) | 977 | 0.0% (0/977) | 97.4% (952/977) | 2.6% (25/977) |
| 2 | 451 | 0.0% (0/451) | 100.0% (451/451) | 0.0% (0/451) | 903 | 0.0% (0/903) | 100.0% (903/903) | 0.0% (0/903) |
| 3 | 325 | 0.0% (0/325) | 100.0% (325/325) | 0.0% (0/325) | 720 | 0.0% (0/720) | 100.0% (720/720) | 0.0% (0/720) |
| 4 | 386 | 0.0% (0/386) | 100.0% (386/386) | 0.0% (0/386) | 756 | 0.0% (0/756) | 100.0% (756/756) | 0.0% (0/756) |

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

- `Fil 1:16`: nincs eredeti vers a TAGNT-ben (versszámozás-eltérés)
  - Pontosítás: a címke általános; a valódi ok, hogy a vers görög szövege a `TAGNT_kivonat.tsv`-ben nincs meg (N-F22c). A vers Károli-szavai `fuggoben` állapotúak, link nélkül; a párosítás nem pótolja.
- `Fil 1:17`: nincs eredeti vers a TAGNT-ben (versszámozás-eltérés)
  - Pontosítás: a címke általános; a valódi ok, hogy a vers görög szövege a `TAGNT_kivonat.tsv`-ben nincs meg (N-F22c). A vers Károli-szavai `fuggoben` állapotúak, link nélkül; a párosítás nem pótolja.
- Régi arany: a könyvben 0 hármas, az egyezés **nem mérhető** (kimondva, nem pótolva).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- Az A csomag összesítője: `naplok/F22_USZ_A_jelentes.md` (a 11 könyv után).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a 11 könyv után, közösen (`naplok/ELLENOR_F22_USZ_A.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
