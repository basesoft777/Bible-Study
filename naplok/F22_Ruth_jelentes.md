# F22_Ruth_jelentes.md — Károli–Strong párosítás: Ruth (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Ruth`, `egyesit.py --konyv Ruth` és `--ellenoriz`, `f22_elemzes.py --konyv Ruth`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Ruth-soraiból: `futas = api_termeles/high/Ruth`, `cimke = ruth`, a `f22/api_termeles/high/_munka/Ruth_k*.json` hibaüzenetei). Ág: `claude/f22-ruth` (a main `3ceddf0a` commitjáról; az 1Kir PR #274, a Neh PR #275, a 2Kir PR #277 és a Dán PR #279 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a Dán után a hiányzó kis könyvek közül a Ruth a legkisebb (85 vers), a detektor szerint beolvasztás nélküli. Indítás: felhasználó, chat, 2026.10.11 („mehet a Ruth”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Ruth tiszta (85/85 vers, 4 fejezet, eltolt 0), a listában és a `versosszevonas.tsv`-ben nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Ruth'`).
- **Minta:** `f22/minta_Ruth.tsv`, 85 vers (= a `Karoli_1908.tsv` `Ruth ` sorai), 9 köteg (10 vers/köteg, az utolsó 5).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01Q5ojFpzh4SynJG4Pdrc1Yk`, 9 kérés (2026-10-11T14:47Z); javító kör `msgbatch_01CPLoEUVeoDDL4qgxemsN7P`, 1 kérés (14:51Z).
- **Futásnapló** (Ruth: 10 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 9 | 8 | 1 köteg (1 vers) | 0,5610 | 99 812 / 92 228 |
| 2. próba (javító) | 1 | 1 | 0 | 0,0214 | 13 491 / 1 583 |
| **összesen** | 10 | | | **0,5824** | |

A javító körbe került köteg: 3 (1 vers); formátumhibás egész köteg nincs.

A könyvplafon a minimum (1,00 USD; 85 × 0,0074 × 1,5 = 0,94 alatt), ebből 0,58 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 77,2232 USD (Ézs–Dán 76,6408 + Ruth 0,5824), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is ennyi. Versenként 0,0069 USD (a plafon alapja 0,0074 alatt).

*Munkamódszer-megjegyzés:* a menet közben a közös munkakönyvtárban egy másik session másik ágra váltott (`claude/f61-lekerdez-naplo`); a Ruth-adat ezért a `claude/f22-ruth` ág saját worktree-jében készült el, a közös könyvtárba kerülő, nem commitolt Ruth-fájlokat eltávolítottam.

## 1a. Szkriptkimenet

```
Sonnet: 9 köteg, 85 vers; kapuhiba első próbára 1.2% (1/85); végleg 0.0% (0/85)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Ruth`: `parok_Ruth.tsv` 2 078 link (mind `alacsony`, `S`), `szavak_Ruth.tsv` 4 071 token. A szavak bontása: hu 2 045 (1 663 `parositva`, 382 `betoldas`), er 2 026 (1 884 `parositva`, 142 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Ruth ` sorainak száma (2 026). Az átnézési sor (`naplok/F22_Ruth_atnezes.tsv`) üres (csak fejléc). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Ruth --ellenoriz` (2026.10.11): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Ruth` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/2078), alacsony 100.0% (2078/2078), kezi 0.0% (0/2078); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/4071), alacsony 100.0% (4071/4071), kezi 0.0% (0/4071).

Link-forrás megoszlás (parok): S 2078. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 85 (Ruth 1:1, Ruth 1:10, Ruth 1:11, Ruth 1:12, Ruth 1:13, Ruth 1:14, Ruth 1:15, Ruth 1:16, Ruth 1:17, Ruth 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 541 | 0.0% (0/541) | 100.0% (541/541) | 0.0% (0/541) | 1025 | 0.0% (0/1025) | 100.0% (1025/1025) | 0.0% (0/1025) |
| 2 | 614 | 0.0% (0/614) | 100.0% (614/614) | 0.0% (0/614) | 1209 | 0.0% (0/1209) | 100.0% (1209/1209) | 0.0% (0/1209) |
| 3 | 411 | 0.0% (0/411) | 100.0% (411/411) | 0.0% (0/411) | 808 | 0.0% (0/808) | 100.0% (808/808) | 0.0% (0/808) |
| 4 | 512 | 0.0% (0/512) | 100.0% (512/512) | 0.0% (0/512) | 1029 | 0.0% (0/1029) | 100.0% (1029/1029) | 0.0% (0/1029) |

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

- Nincs: a Ruthban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A régi arany (2.2): a könyvben nincs hármas, ezért nincs mért érték.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: a Ruth bejegyezve az `adat/datasetek.tsv`-be (8 sor, a jelentéslistával együtt) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D34, v2.28.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
- A következő könyv(ek) a felhasználó döntése: az ÓSZ-ből még 15 kis könyv hiányzik (Préd, Én, Sir, Hós, Jóel, Ámós, Abd, Jón, Mik, Náh, Hab, Sof, Hag, Zak, Mal; együtt 1 540 vers); a Hós (1:11, 11:11) és a Préd (2:26) jóváhagyott 2:1 beolvasztást tartalmaz (`f22/versosszevonas.tsv`, DT92), ezeknél kézi átnézési pont várható; a többi 13 tiszta.

