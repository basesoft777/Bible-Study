# F22_Abd_jelentes.md — Károli–Strong párosítás: Abdiás (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Abd`, `egyesit.py --konyv Abd` és `--ellenoriz`, `f22_elemzes.py --konyv Abd`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Abd-soraiból: `futas = api_termeles/high/Abd`, `cimke = abd`). Ág: `claude/f22-abd` (külön worktree, a main `88b2b8da` commitjáról, majd a Prédikátor PR #285 merge-ével frissítve; az 1Kir PR #274, a Neh PR #275, a 2Kir PR #277, a Dán PR #279, a Ruth PR #280, a Jón PR #281, a Náh PR #283, a régi-arany PR #284 és a Préd PR #285 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a hiányzó kis könyvek egyike (21 vers, a legkisebb hiányzó); a választás a felhasználóé. Indítás: felhasználó, chat, 2026.10.11 („mehet a következő könyv”, a pontosító kérdésre: „Abdiás”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint az Abd tiszta (21/21 vers, 1 fejezet, eltolt 0), a listában és a `versosszevonas.tsv`-ben nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Abd'`).
- **Minta:** `f22/minta_Abd.tsv`, 21 vers (= a `Karoli_1908.tsv` `Abd ` sorai), 3 köteg (10 + 10 + 1 vers).
- **Batch** (`f22/api_termeles/batchek.tsv`): `msgbatch_01F38hEJjnBm7qTwgpof9HMq`, 3 kérés (2026-10-11T16:51Z); javító kör nem kellett.
- **Futásnapló** (Abd: 3 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 3 | 3 | 0 | 0,1251 | 26 778 / 19 674 |
| **összesen** | 3 | | | **0,1251** | |

A könyvplafon a minimum (1,00 USD; 21 × 0,0074 × 1,5 = 0,23 alatt), ebből 0,13 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 79,2291 USD (Ézs–Préd 79,1039 + Abd 0,1251), a globális 110 USD-ből. Az Abd-sorok `futo_osszeg_usd` értékét a Prédikátor PR merge-ekor a Prédikátor utolsó sorához (79,103940) igazítottam (az Abd-sorok ezen az ágon saját sorok, régi sorhoz nem nyúltam); az utolsó sor értéke 79,229088, egyezik a soronkénti költségek összegével. Versenként 0,0060 USD (a plafon alapja 0,0074 alatt).

*Munkamódszer:* a menet saját worktree-ben (`C:\Users\bases\Desktop\Bible-Study-abd`) készült, ahogy a D36 előírja.

## 1a. Szkriptkimenet

```
Sonnet: 3 köteg, 21 vers; kapuhiba első próbára 0.0% (0/21); végleg 0.0% (0/21)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Abd`: `parok_Abd.tsv` 446 link (mind `alacsony`, `S`), `szavak_Abd.tsv` 867 token. A szavak bontása: hu 433 (348 `parositva`, 85 `betoldas`), er 434 (410 `parositva`, 24 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Abd ` sorainak száma (434). Az átnézési sor (`naplok/F22_Abd_atnezes.tsv`) üres (csak fejléc). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Abd --ellenoriz` (2026.10.11, a main beolvasztása után is): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Abd` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/446), alacsony 100.0% (446/446), kezi 0.0% (0/446); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/867), alacsony 100.0% (867/867), kezi 0.0% (0/867).

Link-forrás megoszlás (parok): S 446. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 21 (Abd 1:1, Abd 1:10, Abd 1:11, Abd 1:12, Abd 1:13, Abd 1:14, Abd 1:15, Abd 1:16, Abd 1:17, Abd 1:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 446 | 0.0% (0/446) | 100.0% (446/446) | 0.0% (0/446) | 867 | 0.0% (0/867) | 100.0% (867/867) | 0.0% (0/867) |

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

- Nincs: az Abdiásban nem volt kézi beolvasztás, és kapuhiba sem.
- A régi arany (2.2): a könyvben nincs hármas, ezért nincs mért érték.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: az Abd bejegyezve az `adat/datasetek.tsv`-be (8 sor, a jelentéslistával együtt) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D39, v2.33.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
- A következő könyv(ek) a felhasználó döntése: az ÓSZ-ből még 11 kis könyv hiányzik (Én, Sir, Hós, Jóel, Ámós, Mik, Hab, Sof, Hag, Zak, Mal; együtt 1 203 vers); a Hós (1:11, 11:11) jóváhagyott 2:1 beolvasztást tartalmaz (`f22/versosszevonas.tsv`, DT92), ott kézi átnézési pont várható; a többi 10 beolvasztás nélküli.

## 6. Ellenőri kör (`naplok/ELLENOR_F22_Abd.md`)

Az ellenőr a számszerű állításokat (21/21, 446 / 867, 0/21, 0,1251 USD, 79,2291 USD, az 1 203 vers a 11 megmaradt könyvben) saját lekérdezéssel igazolta; 2 eltérés:

- **DT72 / D19 (közepes), lezárva a D40-nel (a felhasználó döntése, 2026.10.11):** a main beolvasztásakor az Abd saját, még ki nem adott 3 futásnapló-sorának `futo_osszeg_usd` értékét a Préd utolsó sorához igazítottam (77,83… → 79,17…); a D19 szerint a futásnapló csak kifejezett jóváhagyással írható át, a saját ágon lévő új sorokra nincs kivétel. Az értékek számszerűen helyesek, a régi sorok érintetlenek. A felhasználó kivételt hagyott jóvá a D19 alól (brief D40, v2.34); az Abd-sorok igazítása ezzel a szabályon belül van.
- **D39 sor (alacsony), javítva:** a hiányzó könyvek felsorolása hibás volt (Náh és Jón már kész); helyesen: Hag 38, Sof 53, Mal 55, Hab 56.

