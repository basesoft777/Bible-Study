# F22_Nah_jelentes.md — Károli–Strong párosítás: Náhum (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Náh`, `egyesit.py --konyv Náh` és `--ellenoriz`, `f22_elemzes.py --konyv Náh`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Nah-soraiból: `futas = api_termeles/high/Nah`, `cimke = nah`, a `f22/api_termeles/high/_munka/Nah_k*.json` hibaüzenetei). Ág: `claude/f22-nah` (külön worktree, a main `85fa874c` commitjáról; az 1Kir PR #274, a Neh PR #275, a 2Kir PR #277, a Dán PR #279, a Ruth PR #280 és a Jón PR #281 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a hiányzó kis könyvek egyike (47 vers), a detektor szerint beolvasztás nélküli; a választás a felhasználóé. Indítás: felhasználó, chat, 2026.10.11 („mehet a Nehémiás”, a pontosító kérdésre a válasz: „Náhum”; a Nehémiás már kész, PR #275).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Náh tiszta (47/47 vers, 3 fejezet, eltolt 0), a listában és a `versosszevonas.tsv`-ben nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Náh'`).
- **Minta:** `f22/minta_Nah.tsv`, 47 vers (= a `Karoli_1908.tsv` `Náh ` sorai), 5 köteg (10 vers/köteg, az utolsó 7).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_018YV7SykB2aV6RGqdTN9u9v`, 5 kérés (2026-10-11T15:56Z); javító kör `msgbatch_01RRaYZcd4CTLXdnssmHxnt6`, 1 kérés (15:58Z).
- **Futásnapló** (Nah: 6 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 5 | 4 | 1 köteg (1 vers) | 0,2356 | 48 516 / 37 424 |
| 2. próba (javító) | 1 | 1 | 0 | 0,0146 | 11 687 / 590 |
| **összesen** | 6 | | | **0,2503** | |

A javító körbe került köteg: 2 (1 vers); formátumhibás egész köteg nincs.

A könyvplafon a minimum (1,00 USD; 47 × 0,0074 × 1,5 = 0,52 alatt), ebből 0,25 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 77,7576 USD (Ézs–Jón 77,5074 + Náh 0,2503), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is ennyi. Versenként 0,0053 USD (a plafon alapja 0,0074 alatt).

*Munkamódszer:* a menet saját worktree-ben (`C:\Users\bases\Desktop\Bible-Study-nah`) készült, ahogy a D36 előírja (az „egyedül fut” szabály alól API Batch módban ezzel a feltétellel felmentés van).

## 1a. Szkriptkimenet

```
Sonnet: 5 köteg, 47 vers; kapuhiba első próbára 2.1% (1/47); végleg 0.0% (0/47)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Náh`: `parok_Nah.tsv` 850 link (mind `alacsony`, `S`), `szavak_Nah.tsv` 1 641 token. A szavak bontása: hu 813 (679 `parositva`, 134 `betoldas`), er 828 (792 `parositva`, 36 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Náh ` sorainak száma (828). Az átnézési sor (`naplok/F22_Nah_atnezes.tsv`) üres (csak fejléc). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Náh --ellenoriz` (2026.10.11): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Náh` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/850), alacsony 100.0% (850/850), kezi 0.0% (0/850); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/1641), alacsony 100.0% (1641/1641), kezi 0.0% (0/1641).

Link-forrás megoszlás (parok): S 850. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 47 (Náh 1:1, Náh 1:10, Náh 1:11, Náh 1:12, Náh 1:13, Náh 1:14, Náh 1:15, Náh 1:2, Náh 1:3, Náh 1:4).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 268 | 0.0% (0/268) | 100.0% (268/268) | 0.0% (0/268) | 524 | 0.0% (0/524) | 100.0% (524/524) | 0.0% (0/524) |
| 2 | 226 | 0.0% (0/226) | 100.0% (226/226) | 0.0% (0/226) | 443 | 0.0% (0/443) | 100.0% (443/443) | 0.0% (0/443) |
| 3 | 356 | 0.0% (0/356) | 100.0% (356/356) | 0.0% (0/356) | 674 | 0.0% (0/674) | 100.0% (674/674) | 0.0% (0/674) |

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

- Nincs: a Náhumban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A régi arany (2.2): a könyvben nincs hármas, ezért nincs mért érték.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: a Náh bejegyezve az `adat/datasetek.tsv`-be (8 sor, a jelentéslistával együtt) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D37, v2.31.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
- A következő könyv(ek) a felhasználó döntése: az ÓSZ-ből még 13 kis könyv hiányzik (Préd, Én, Sir, Hós, Jóel, Ámós, Abd, Mik, Hab, Sof, Hag, Zak, Mal; együtt 1 445 vers); a Hós (1:11, 11:11) és a Préd (2:26) jóváhagyott 2:1 beolvasztást tartalmaz (`f22/versosszevonas.tsv`, DT92), ezeknél kézi átnézési pont várható; a többi 11 tiszta.

## 6. Ellenőri kör (`naplok/ELLENOR_F22_Nah.md`)

Az ellenőr TISZTA jelentést adott, eltérés nélkül: a számszerű állításokat (47/47, 850 / 1 641, 1/47 → 0, 0,2503 USD, 77,7576 USD, a futó összeg folytonossága, az 1 445 vers a 13 megmaradt könyvben) saját lekérdezéssel igazolta. Nem ellenőrizhető a szerepkörből: a K3 hash viszonya a `prompt_v3.sha256`-hoz (a korábbi könyvekkel azonos), a chat-jóváhagyás, a K2/K7 teljes köre, a detektor ítélete, a régi arany hiánya és a CI-jelentés összevetése.

