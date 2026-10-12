# F22_Jud_jelentes.md — Károli–Strong párosítás: Júd (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Júd`, `egyesit.py --konyv Júd` és `--ellenoriz`, `f22_elemzes.py --konyv Júd`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Júd-soraiból: `futas = api_termeles/high/Jud`, `cimke = jud`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.8 ÚSZ-próbacsomag (Filem, 2Ján, 3Ján, Júd; 78 vers, D44) egyike; a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd itt a próbacsomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Júd'`).
- **Minta:** `f22/minta_Jud.tsv`, 25 vers a modellhez, 3 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01UtXAsZXYiZB4YQdHY5wYjL`, 3 kérés (2026-10-12T07:56:40+00:00); 2. kör `msgbatch_01SRKPyyYxCdE4Pt2ZhU8e2s`, 1 kérés (2026-10-12T08:00:13+00:00).
- **Futásnapló** (Júd: 4 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 3 | 2 | 1 köteg | 0.1385 | 27 814 / 22 145 |
| 2. próba (javító) | 1 | 1 | 0 köteg | 0.0271 | 7 715 / 3 878 |
| **összesen** | 4 | | | **0.1656** | |

Költségplafon: a könyvplafon 25 vers × 0,0074 × 1,5 = 0.2775 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.00 USD); a könyv költsége 0.1656 USD (versenként 0.0066 USD, a modellhez ment 25 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó Júd-sora: 86.369810 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 3 köteg, 25 vers; kapuhiba első próbára 20.0% (5/25); végleg 0.0% (0/25)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Júd`: parok: 426 sor {'alacsony': 426}; szavak: 954 sor {'alacsony': 954}; átnézési sor: 0 vers; ellenőrzés: rendben

A szavak bontása: hu 109 `betoldas`, 377 `parositva`; er 80 `forditatlan`, 388 `parositva`. Az átnézési sor (`naplok/F22_Jud_atnezes.tsv`): 0 vers.

`egyesit.py --konyv Júd --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4)

28 `[nem TR]` token; állapot szerint: 28 `forditatlan`. Eltérés az elvárttól (`forditatlan`) nincs.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Júd` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/426), alacsony 100.0% (426/426), kezi 0.0% (0/426); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/954), alacsony 100.0% (954/954), kezi 0.0% (0/954).

Link-forrás megoszlás (parok): S 426. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 25 (Júd 1:1, Júd 1:10, Júd 1:11, Júd 1:12, Júd 1:13, Júd 1:14, Júd 1:15, Júd 1:16, Júd 1:17, Júd 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 426 | 0.0% (0/426) | 100.0% (426/426) | 0.0% (0/426) | 954 | 0.0% (0/954) | 100.0% (954/954) | 0.0% (0/954) |

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
