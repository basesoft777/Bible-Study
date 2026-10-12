# F22_2Jan_jelentes.md — Károli–Strong párosítás: 2Ján (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 2Ján`, `egyesit.py --konyv 2Ján` és `--ellenoriz`, `f22_elemzes.py --konyv 2Ján`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 2Ján-soraiból: `futas = api_termeles/high/2Jan`, `cimke = 2jan`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.8 ÚSZ-próbacsomag (Filem, 2Ján, 3Ján, Júd; 78 vers, D44) egyike; a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd itt a próbacsomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'2Ján'`).
- **Minta:** `f22/minta_2Jan.tsv`, 13 vers a modellhez, 2 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_014etARP3Sr8oKSnBif4Zg1r`, 2 kérés (2026-10-12T07:47:24+00:00); 2. kör `msgbatch_01Vq325ByRXc82aSJgckeQdy`, 1 kérés (2026-10-12T07:51:00+00:00).
- **Futásnapló** (2Ján: 3 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 2 | 1 | 1 köteg | 0.0651 | 16 107 / 9 804 |
| 2. próba (javító) | 1 | 1 | 0 köteg | 0.0181 | 6 708 / 2 270 |
| **összesen** | 3 | | | **0.0832** | |

A javító körbe került köteg: k002; egész köteg formátumhibás (nem érvényes JSON: „Extra data”; tömb nélküli versobjektumok prózai közbeszúrással), 3 vers; a javító kör 0-ra hozta. Versenkénti tartalmi kapuhiba a javító kör után nem maradt.

Költségplafon: a könyvplafon 13 vers × 0,0074 × 1,5 = 0.1443 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.00 USD); a könyv költsége 0.0832 USD (versenként 0.0064 USD, a modellhez ment 13 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó 2Ján-sora: 86.127785 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 2 köteg, 13 vers; kapuhiba első próbára 23.1% (3/13); végleg 0.0% (0/13)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 2Ján`: parok: 236 sor {'alacsony': 236}; szavak: 485 sor {'alacsony': 485}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 34 `betoldas`, 202 `parositva`; er 34 `forditatlan`, 215 `parositva`. Az átnézési sor (`naplok/F22_2Jan_atnezes.tsv`): 0 vers.

`egyesit.py --konyv 2Ján --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4)

5 `[nem TR]` token; állapot szerint: 5 `forditatlan`. Eltérés az elvárttól (`forditatlan`) nincs.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 2Ján` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/236), alacsony 100.0% (236/236), kezi 0.0% (0/236); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/485), alacsony 100.0% (485/485), kezi 0.0% (0/485).

Link-forrás megoszlás (parok): S 236. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 13 (2Ján 1:1, 2Ján 1:10, 2Ján 1:11, 2Ján 1:12, 2Ján 1:13, 2Ján 1:2, 2Ján 1:3, 2Ján 1:4, 2Ján 1:5, 2Ján 1:6).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 236 | 0.0% (0/236) | 100.0% (236/236) | 0.0% (0/236) | 485 | 0.0% (0/485) | 100.0% (485/485) | 0.0% (0/485) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1.

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
- Régi arany: a könyvben 0 hármas, az egyezés **nem mérhető** (a 22.8 szerint kimondva, nem pótolva).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- A 22.8 összesítő jelentése: `naplok/F22_USZ_proba_jelentes.md` (a négy könyv után).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a négy könyv után, közösen (`naplok/ELLENOR_F22_USZ_proba.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
