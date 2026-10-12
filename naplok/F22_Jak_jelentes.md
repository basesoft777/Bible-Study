# F22_Jak_jelentes.md — Károli–Strong párosítás: Jak (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Jak`, `egyesit.py --konyv Jak` és `--ellenoriz`, `f22_elemzes.py --konyv Jak`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Jak-soraiból: `futas = api_termeles/high/Jak`, `cimke = jak`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Jak'`).
- **Minta:** `f22/minta_Jak.tsv`, 108 vers a modellhez, 11 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01XdnUeJjQPAyr5c3v62T5SV`, 11 kérés (2026-10-12T09:48:35+00:00).
- **Futásnapló** (Jak: 11 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 11 | 11 | 0 köteg | 0.5162 | 102 428 / 82 755 |
| **összesen** | 11 | | | **0.5162** | |

Költségplafon: a könyvplafon 108 vers × 0,0074 × 1,5 = 1.1988 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.20 USD); a könyv költsége 0.5162 USD (versenként 0.0048 USD, a modellhez ment 108 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó Jak-sora: 90.894945 USD, a 18 USD-s ÚSZ-keretből (D45: 86,3698 + 18; a kódbeli plafon `PLAFON_USD` = 104,36 USD).

## 1a. Szkriptkimenet

```
Sonnet: 11 köteg, 108 vers; kapuhiba első próbára 0.0% (0/108); végleg 0.0% (0/108)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Jak`: parok: 1701 sor {'alacsony': 1701}; szavak: 3618 sor {'alacsony': 3618}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 345 `betoldas`, 1494 `parositva`; er 250 `forditatlan`, 1529 `parositva`. Az átnézési sor (`naplok/F22_Jak_atnezes.tsv`): 0 vers.

`egyesit.py --konyv Jak --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

52 `[nem TR]` token; állapot szerint: 45 `forditatlan`, 7 `parositva`. Eltérés az elvárttól (`forditatlan`): Jak 2:20 er 13 (ἀργή, G0692) → parositva; Jak 3:4 er 22 (βούλεται.¶, G1014) → parositva; Jak 3:8 er 8 (ἀκατάστατον, G0182) → parositva; Jak 4:5 er 14 (κατῴκισεν, G6052) → parositva; Jak 4:9 er 11 (μετατραπήτω, G6060) → parositva; Jak 4:12 er 17 (κρίνων, G2919) → parositva; Jak 4:12 er 19 (πλησίον;¶, G4139) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Jak` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/1701), alacsony 100.0% (1701/1701), kezi 0.0% (0/1701); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/3618), alacsony 100.0% (3618/3618), kezi 0.0% (0/3618).

Link-forrás megoszlás (parok): S 1701. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 108 (Jak 1:1, Jak 1:10, Jak 1:11, Jak 1:12, Jak 1:13, Jak 1:14, Jak 1:15, Jak 1:16, Jak 1:17, Jak 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 404 | 0.0% (0/404) | 100.0% (404/404) | 0.0% (0/404) | 834 | 0.0% (0/834) | 100.0% (834/834) | 0.0% (0/834) |
| 2 | 419 | 0.0% (0/419) | 100.0% (419/419) | 0.0% (0/419) | 899 | 0.0% (0/899) | 100.0% (899/899) | 0.0% (0/899) |
| 3 | 285 | 0.0% (0/285) | 100.0% (285/285) | 0.0% (0/285) | 610 | 0.0% (0/610) | 100.0% (610/610) | 0.0% (0/610) |
| 4 | 263 | 0.0% (0/263) | 100.0% (263/263) | 0.0% (0/263) | 579 | 0.0% (0/579) | 100.0% (579/579) | 0.0% (0/579) |
| 5 | 330 | 0.0% (0/330) | 100.0% (330/330) | 0.0% (0/330) | 696 | 0.0% (0/696) | 100.0% (696/696) | 0.0% (0/696) |

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
