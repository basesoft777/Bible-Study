# F22_Ezsd_jelentes.md — Károli–Strong párosítás: Ezsdrás (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Ezsd`, `egyesit.py --ellenoriz --konyv <könyv>`, `f22_elemzes.py --konyv Ezsd`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Ezsd-sorainak összesítése, a `f22/api_termeles/high/_munka/Ezsd_k*.json` hibaüzenetei). Ág: `claude/f22-ezsd`, a 2Krón-ág utolsó commitjáról (`ebc590d`) indítva; a 2Krón azóta a PR #255-tel a main-be olvadt. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Sorrend: DT57 (1), a BDB-haszon mérése szerint a 2Krón után az Ezsd.*

*A könyvnév (`Ezsd`) ASCII és magyar alakja azonos, ezért az `f22_elemzes.py` régi-arany szűrése itt nem csúszhat el (l. `naplok/ELLENOR_F22_1Kron.md` 1. eltérés).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.08, chat: „mehet az ezsdrás”)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint az Ezsd tiszta (280/280 vers, 10 fejezet, K-hiány 0, E-hiány 0, eltolt 0), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Ezsd'`).
- **Minta:** `f22/minta_Ezsd.tsv`, 280 vers (= a `Karoli_1908.tsv` `Ezsd ` sorai), 28 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01XTCpyxBw1vSL8r5nvNgUEA`, 28 kérés (2026-10-08T16:30Z); javító kör `msgbatch_01ViEfPt4GQmhvRvWSUoLBLZ`, 5 kérés (16:35Z).
- **Futásnapló** (Ezsd: 33 sor, `futas=api_termeles/high/Ezsd`): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb` (mint az Ézs–2Krón soraiban).

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 28 | 23 | 5 köteg (16 vers) | 1,4824 | 299 658 / 236 552 |
| 2. próba (javító) | 5 | 5 | 0 | 0,1603 | 59 240 / 20 219 |
| **összesen** | 33 | | | **1,6428** | |

A javító körbe került kötegek: 2, 6, 9, 22, 28. Ebből **egy köteg egészében bukott**: a k009 (Ezsd 2:70–3:9, 10 vers), mert a válasz nem érvényes JSON („Extra data: line 12 column 1”), tehát a forma volt hibás, nem a párosítás. A többi 6 vers versszintű kapuhiba (gazdátlan eredeti sorszám, hiányzó magyar sorszám, üres partnerlista).

A könyvplafonból (280 × 0,0074 × 1,5 = 3,11 USD) 1,64 fogyott; a futásnapló futó összege 28,6549 USD (Ézs 7,0834 + Jer 9,0552 + 1Krón 4,5552 + 2Krón 6,3183 + Ezsd 1,6428), a globális 110 USD-ből. Versenként 0,0059 USD (a plafon alapja 0,0074; a 2Krón 0,0077 volt).

**Az arámi szakaszok** (Ezsd 4:8–6:18, 7:12–26) ugyanazzal a prompttal és ugyanabban a kötegezésben futottak; külön mérés rájuk nem készült.

## 1a. Szkriptkimenet

```
Sonnet: 28 köteg, 280 vers; kapuhiba első próbára 5.7% (16/280); végleg 0.0% (0/280)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Ezsd`: `parok_Ezsd.tsv` 5 533 link (mind `alacsony`, `S`; a fájl 5 535 sora a proveniencia- és a fejlécsorral), `szavak_Ezsd.tsv` 10 989 token (10 991 sor). A szavak bontása: hu 5 183 (4 284 `parositva`, 899 `betoldas`), er 5 806 (5 275 `parositva`, 531 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Ezsd ` sorainak száma (5 806). Az átnézési sor (`naplok/F22_Ezsd_atnezes.tsv`) üres (csak fejléc).

`egyesit.py --ellenoriz --konyv <könyv>` (2026.10.08, ezen az ágon): 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs, Zsolt, Ézs, Jer, 1Krón, 2Krón, Ezsd — mind „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Ezsd` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/5533), alacsony 100.0% (5533/5533), kezi 0.0% (0/5533); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/10989), alacsony 100.0% (10989/10989), kezi 0.0% (0/10989).

Link-forrás megoszlás (parok): S 5533. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 280 (Ezsd 10:1, Ezsd 10:10, Ezsd 10:11, Ezsd 10:12, Ezsd 10:13, Ezsd 10:14, Ezsd 10:15, Ezsd 10:16, Ezsd 10:17, Ezsd 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 275 | 0.0% (0/275) | 100.0% (275/275) | 0.0% (0/275) | 541 | 0.0% (0/541) | 100.0% (541/541) | 0.0% (0/541) |
| 2 | 677 | 0.0% (0/677) | 100.0% (677/677) | 0.0% (0/677) | 1211 | 0.0% (0/1211) | 100.0% (1211/1211) | 0.0% (0/1211) |
| 3 | 395 | 0.0% (0/395) | 100.0% (395/395) | 0.0% (0/395) | 833 | 0.0% (0/833) | 100.0% (833/833) | 0.0% (0/833) |
| 4 | 567 | 0.0% (0/567) | 100.0% (567/567) | 0.0% (0/567) | 1165 | 0.0% (0/1165) | 100.0% (1165/1165) | 0.0% (0/1165) |
| 5 | 487 | 0.0% (0/487) | 100.0% (487/487) | 0.0% (0/487) | 952 | 0.0% (0/952) | 100.0% (952/952) | 0.0% (0/952) |
| 6 | 585 | 0.0% (0/585) | 100.0% (585/585) | 0.0% (0/585) | 1132 | 0.0% (0/1132) | 100.0% (1132/1132) | 0.0% (0/1132) |
| 7 | 630 | 0.0% (0/630) | 100.0% (630/630) | 0.0% (0/630) | 1280 | 0.0% (0/1280) | 100.0% (1280/1280) | 0.0% (0/1280) |
| 8 | 716 | 0.0% (0/716) | 100.0% (716/716) | 0.0% (0/716) | 1473 | 0.0% (0/1473) | 100.0% (1473/1473) | 0.0% (0/1473) |
| 9 | 506 | 0.0% (0/506) | 100.0% (506/506) | 0.0% (0/506) | 981 | 0.0% (0/981) | 100.0% (981/981) | 0.0% (0/981) |
| 10 | 695 | 0.0% (0/695) | 100.0% (695/695) | 0.0% (0/695) | 1421 | 0.0% (0/1421) | 100.0% (1421/1421) | 0.0% (0/1421) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.

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

- Nincs: az Ezsdrásban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs (mint a 3Móz–2Krón menetekben); a versbeosztás a detektor szerint tiszta.
- A régi arany (2.2) az Ezsdrásban üres: a `Karoli_Strong_kivonat.tsv`-ben nincs `Ezr` sor, ez valódi üres eredmény, nem szűrési hiba.

## 4. Kiegészítések ebben a menetben

- K9: az Ezsd bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag` (`claude/f22-ezsd`), `kovetkezo`, `ir`, D22, v2.16.

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_Ezsd.md`.
- A korábbi kézi átnézések (1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1) továbbra is a felhasználóé.
- A következő könyv indítása a felhasználó döntése (⛔ 2.). A DT57 (1) mérése szerint a sorrend: Jób 159, Ez 147, Péld 145 szócikk; a Jób előtt TAHOT-hiány (Jób 40:1–5, 41) és döntés az 1:2 / 2:1 támogatásról.
