# F22_3Jan_jelentes.md — Károli–Strong párosítás: 3Ján (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 3Ján`, `egyesit.py --konyv 3Ján` és `--ellenoriz`, `f22_elemzes.py --konyv 3Ján`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 3Ján-soraiból: `futas = api_termeles/high/3Jan`, `cimke = 3jan`). Ág: `claude/amazing-mayer-t276r0`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.8 ÚSZ-próbacsomag (Filem, 2Ján, 3Ján, Júd; 78 vers, D44) egyike; a futtatás soros. Indítás: felhasználói utasítás (chat, 2026.10.12: „mehet, indítsd itt a próbacsomagot”; a versbeosztás jóváhagyása: „mehet, jóváhagyom a versbeosztást”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'3Ján'`).
- **Minta:** `f22/minta_3Jan.tsv`, 14 vers a modellhez (+ 1 eredeti vers nélküli Károli-vers, nem kerül modellhez), 2 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01LK1p8EqXfj6Y5CvtTMyAJj`, 2 kérés (2026-10-12T07:53:08+00:00).
- **Futásnapló** (3Ján: 2 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 2 | 2 | 0 köteg | 0.0764 | 15 636 / 12 149 |
| **összesen** | 2 | | | **0.0764** | |

Költségplafon: a könyvplafon 15 vers × 0,0074 × 1,5 = 0.1665 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 1.00 USD); a könyv költsége 0.0764 USD (versenként 0.0055 USD, a modellhez ment 14 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó 3Ján-sora: 86.204166 USD, a globális 110 USD-ből.

## 1a. Szkriptkimenet

```
Sonnet: 2 köteg, 14 vers; kapuhiba első próbára 0.0% (0/14); végleg 0.0% (0/14)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 3Ján`: parok: 217 sor {'alacsony': 217}; szavak: 459 sor {'alacsony': 447, 'kezi': 12}; átnézési sor: 1 vers; ellenőrzés: rendben

A szavak bontása: hu 47 `betoldas`, 12 `fuggoben`, 190 `parositva`; er 30 `forditatlan`, 180 `parositva`. Az átnézési sor (`naplok/F22_3Jan_atnezes.tsv`): 1 vers.

`egyesit.py --konyv 3Ján --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4)

9 `[nem TR]` token; állapot szerint: 9 `forditatlan`. Eltérés az elvárttól (`forditatlan`) nincs.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 3Ján` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/217), alacsony 100.0% (217/217), kezi 0.0% (0/217); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/459), alacsony 97.4% (447/459), kezi 2.6% (12/459).

Link-forrás megoszlás (parok): S 217. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 14 (3Ján 1:1, 3Ján 1:10, 3Ján 1:11, 3Ján 1:12, 3Ján 1:13, 3Ján 1:14, 3Ján 1:2, 3Ján 1:3, 3Ján 1:4, 3Ján 1:5).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 217 | 0.0% (0/217) | 100.0% (217/217) | 0.0% (0/217) | 459 | 0.0% (0/459) | 97.4% (447/459) | 2.6% (12/459) |

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

- `3Ján 1:15`: nincs eredeti vers a TAGNT-ben (versszámozás-eltérés)
  - Pontosítás: az `egyesit.py` átnézési szövege általános („versszámozás-eltérés”); itt a valódi ok, hogy a vers görög szövege (εἰρήνη σοι …) a `TAGNT_kivonat.tsv`-ben sehol nem szerepel (az 1:14 a λαλήσομεν szóval zárul): a kivonat hiánya (N-F22c). A vers 12 Károli-szava `fuggoben`, link nélkül; a párosítás nem pótolja, a 22.8 4. pontja szerint.
- Régi arany: a könyvben 0 hármas, az egyezés **nem mérhető** (a 22.8 szerint kimondva, nem pótolva).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- A 22.8 összesítő jelentése: `naplok/F22_USZ_proba_jelentes.md` (a négy könyv után).

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a négy könyv után, közösen (`naplok/ELLENOR_F22_USZ_proba.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
