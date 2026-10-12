# F22_2Thessz_jelentes.md — Károli–Strong párosítás: 2Thessz (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 2Thessz`, `egyesit.py --konyv 2Thessz` és `--ellenoriz`, `f22_elemzes.py --konyv 2Thessz`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 2Thessz-soraiból: `futas = api_termeles/high/2Thessz`, `cimke = 2thessz`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 A csomag (Tit, 2Thessz, 2Pét, 2Tim, 1Thessz, Kol, Fil, 1Pét, 1Ján, Jak, 1Tim; 956 vers, D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd az A csomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'2Thessz'`).
- **Minta:** `f22/minta_2Thessz.tsv`, 47 vers a modellhez, 5 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_013r2oFX59PenE9oFEapVVjy`, 5 kérés (2026-10-12T08:58:04+00:00).
- **Futásnapló** (2Thessz: 5 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 5 | 5 | 0 köteg | 0.2809 | 47 413 / 46 692 |
| **összesen** | 5 | | | **0.2809** | |

Költségplafon: a könyvplafon 47 vers × 0,0074 × 1,5 = 0.5217 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.00 USD); a könyv költsége 0.2809 USD (versenként 0.0060 USD, a modellhez ment 47 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó 2Thessz-sora: 86.866842 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 5 köteg, 47 vers; kapuhiba első próbára 0.0% (0/47); végleg 0.0% (0/47)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 2Thessz`: parok: 823 sor {'alacsony': 823}; szavak: 1702 sor {'alacsony': 1702}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 163 `betoldas`, 700 `parositva`; er 123 `forditatlan`, 716 `parositva`. Az átnézési sor (`naplok/F22_2Thessz_atnezes.tsv`): 0 vers.

`egyesit.py --konyv 2Thessz --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

20 `[nem TR]` token; állapot szerint: 20 `forditatlan`. Eltérés az elvárttól (`forditatlan`) nincs.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 2Thessz` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/823), alacsony 100.0% (823/823), kezi 0.0% (0/823); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/1702), alacsony 100.0% (1702/1702), kezi 0.0% (0/1702).

Link-forrás megoszlás (parok): S 823. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 47 (2Thessz 1:1, 2Thessz 1:10, 2Thessz 1:11, 2Thessz 1:12, 2Thessz 1:2, 2Thessz 1:3, 2Thessz 1:4, 2Thessz 1:5, 2Thessz 1:6, 2Thessz 1:7).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 236 | 0.0% (0/236) | 100.0% (236/236) | 0.0% (0/236) | 480 | 0.0% (0/480) | 100.0% (480/480) | 0.0% (0/480) |
| 2 | 320 | 0.0% (0/320) | 100.0% (320/320) | 0.0% (0/320) | 656 | 0.0% (0/656) | 100.0% (656/656) | 0.0% (0/656) |
| 3 | 267 | 0.0% (0/267) | 100.0% (267/267) | 0.0% (0/267) | 566 | 0.0% (0/566) | 100.0% (566/566) | 0.0% (0/566) |

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
