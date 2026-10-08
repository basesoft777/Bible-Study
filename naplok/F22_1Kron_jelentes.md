# F22_1Kron_jelentes.md — Károli–Strong párosítás: 1Krónika (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 1Kron`, `egyesit.py --ellenoriz --konyv <könyv>`, `f22_elemzes.py --konyv 1Krón`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 1Krón-sorainak összesítése, a `f22/api_termeles/high/_munka/1Kron_k*.json` hibaüzenetei). Ág: `claude/wonderful-einstein-ezr2pw`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT-F77 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Sorrend: DT57 (1), a BDB-haszon mérése szerint elsőként az 1Krón.*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.08, chat: „mehet”)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint az 1Krón tiszta (942/942 vers, 29 fejezet, K-hiány 0, E-hiány 0, eltolt 0), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'1Krón'`).
- **Minta:** `f22/minta_1Kron.tsv`, 942 vers (= a `Karoli_1908.tsv` `1Krón ` sorai), 95 köteg (10 vers/köteg, az utolsó 2).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_015RT7Wq1cMxJz16LnBU42QS`, 95 kérés (2026-10-08T13:06Z); javító kör `msgbatch_01KGN6V3b5KHWL3gFcKd1CEn`, 20 kérés (13:44Z).
- **Futásnapló** (1Krón: 115 sor, `futas=api_termeles/high/1Kron`): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb` (mint az Ézsnél és a Jeremiásnál).

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 95 | 75 | 20 köteg (70 vers) | 4,0943 | 935 103 / 631 833 |
| 2. próba (javító) | 20 | 19 | 1 köteg (1 vers) | 0,4609 | 218 743 / 48 441 |
| **összesen** | 115 | | | **4,5552** | |

A javító körbe került kötegek: 2, 4, 6, 7, 9, 12, 17, 30, 33, 34, 37, 52, 55, 66, 74, 75, 79, 82, 85, 90. Ebből **öt köteg egészében bukott** (12, 30, 66, 75, 82: 10–10 vers, együtt 50): a válasz formája volt hibás, nem a párosítás (pl. a k012-ben „a válasz nem érvényes JSON: Extra data”; a k030 és a k075 nyers válaszában az első versobjektum után zárócímke áll (`</parameter>`, ill. `</parok>`), utána önjavító szöveg és a teljes válasz újra; a k012 és a k082 válasza nem tömb, hanem soronkénti objektumok). A többi 20 vers versenkénti kapuhiba: üres partnerlista (`[n, []]`), kétszer vagy sehol sem szereplő sorszám.

A költség versenként 0,0048 USD (a plafon alapja 0,0074). A könyvplafonból (942 × 0,0074 × 1,5 = 10,46 USD) 4,56 fogyott; a futásnapló futó összege 20,6938 USD (Ézs 7,0834 + Jer 9,0552 + 1Krón 4,5552), a globális 110 USD-ből.

**Az első próbás kapuhiba-arány (7,4%) a Jeremiásénak (3,0%) több mint kétszerese.** A 70 versből 50 az öt formátumhibás kötegé, a párosítási kapuhiba 20 vers; a formátumhibás kötegek közül négy a javító körben átment, a k066-ban egy vers (19:2) végleg kapuhibás maradt.

## 1a. Szkriptkimenet

```
Sonnet: 95 köteg, 942 vers; kapuhiba első próbára 7.4% (70/942); végleg 0.1% (1/942)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 1Kron`: `parok_1Kron.tsv` 15 344 link (mind `alacsony`, `S`; a fájl 15 346 sora a proveniencia- és a fejlécsorral), `szavak_1Kron.tsv` 32 018 token (32 020 sor). A szavak bontása: hu 15 469 (12 393 `parositva`, 3 029 `betoldas`, 47 `fuggoben`), er 16 549 (14 451 `parositva`, 2 059 `forditatlan`, 39 `fuggoben`). Az er szám = a `TAHOT_kivonat.tsv` `1Krón ` sorainak száma (16 549). A 86 `fuggoben` token mind az **1Krón 19:2**-é (`kezi` bizonyosság, hu 47 + er 39), ez a vers az átnézési sorban (`naplok/F22_1Kron_atnezes.tsv`): `4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban nem szerepelnek: [17]` — a második próba után is egyetlen eredeti szó (17.) maradt gazdátlanul.

`egyesit.py --ellenoriz --konyv <könyv>` (2026.10.08, ezen az ágon): 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs, Zsolt, Ézs, Jer, 1Krón — mind „ellenőrzés: rendben”. A proveniencia-sor: `scope=manual | forras=f22/valaszok/sonnet/1Kron.jsonl, konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv | ts=manual (csak Sonnet, DT-F22c: nincs C futásnapló; az API (Batch)-futásnak nincs lekérdezés-időbélyege) | …`.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 1Krón` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/15344), alacsony 100.0% (15344/15344), kezi 0.0% (0/15344); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/32018), alacsony 99.7% (31932/32018), kezi 0.3% (86/32018).

Link-forrás megoszlás (parok): S 15344. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 941 (1Krón 10:1, 1Krón 10:10, 1Krón 10:11, 1Krón 10:12, 1Krón 10:13, 1Krón 10:14, 1Krón 10:2, 1Krón 10:3, 1Krón 10:4, 1Krón 10:5).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 520 | 0.0% (0/520) | 100.0% (520/520) | 0.0% (0/520) | 1123 | 0.0% (0/1123) | 100.0% (1123/1123) | 0.0% (0/1123) |
| 2 | 621 | 0.0% (0/621) | 100.0% (621/621) | 0.0% (0/621) | 1371 | 0.0% (0/1371) | 100.0% (1371/1371) | 0.0% (0/1371) |
| 3 | 278 | 0.0% (0/278) | 100.0% (278/278) | 0.0% (0/278) | 564 | 0.0% (0/564) | 100.0% (564/564) | 0.0% (0/564) |
| 4 | 641 | 0.0% (0/641) | 100.0% (641/641) | 0.0% (0/641) | 1345 | 0.0% (0/1345) | 100.0% (1345/1345) | 0.0% (0/1345) |
| 5 | 500 | 0.0% (0/500) | 100.0% (500/500) | 0.0% (0/500) | 1004 | 0.0% (0/1004) | 100.0% (1004/1004) | 0.0% (0/1004) |
| 6 | 959 | 0.0% (0/959) | 100.0% (959/959) | 0.0% (0/959) | 2145 | 0.0% (0/2145) | 100.0% (2145/2145) | 0.0% (0/2145) |
| 7 | 595 | 0.0% (0/595) | 100.0% (595/595) | 0.0% (0/595) | 1233 | 0.0% (0/1233) | 100.0% (1233/1233) | 0.0% (0/1233) |
| 8 | 367 | 0.0% (0/367) | 100.0% (367/367) | 0.0% (0/367) | 809 | 0.0% (0/809) | 100.0% (809/809) | 0.0% (0/809) |
| 9 | 672 | 0.0% (0/672) | 100.0% (672/672) | 0.0% (0/672) | 1436 | 0.0% (0/1436) | 100.0% (1436/1436) | 0.0% (0/1436) |
| 10 | 299 | 0.0% (0/299) | 100.0% (299/299) | 0.0% (0/299) | 619 | 0.0% (0/619) | 100.0% (619/619) | 0.0% (0/619) |
| 11 | 716 | 0.0% (0/716) | 100.0% (716/716) | 0.0% (0/716) | 1511 | 0.0% (0/1511) | 100.0% (1511/1511) | 0.0% (0/1511) |
| 12 | 715 | 0.0% (0/715) | 100.0% (715/715) | 0.0% (0/715) | 1501 | 0.0% (0/1501) | 100.0% (1501/1501) | 0.0% (0/1501) |
| 13 | 295 | 0.0% (0/295) | 100.0% (295/295) | 0.0% (0/295) | 629 | 0.0% (0/629) | 100.0% (629/629) | 0.0% (0/629) |
| 14 | 296 | 0.0% (0/296) | 100.0% (296/296) | 0.0% (0/296) | 591 | 0.0% (0/591) | 100.0% (591/591) | 0.0% (0/591) |
| 15 | 527 | 0.0% (0/527) | 100.0% (527/527) | 0.0% (0/527) | 1142 | 0.0% (0/1142) | 100.0% (1142/1142) | 0.0% (0/1142) |
| 16 | 665 | 0.0% (0/665) | 100.0% (665/665) | 0.0% (0/665) | 1335 | 0.0% (0/1335) | 100.0% (1335/1335) | 0.0% (0/1335) |
| 17 | 666 | 0.0% (0/666) | 100.0% (666/666) | 0.0% (0/666) | 1266 | 0.0% (0/1266) | 100.0% (1266/1266) | 0.0% (0/1266) |
| 18 | 324 | 0.0% (0/324) | 100.0% (324/324) | 0.0% (0/324) | 695 | 0.0% (0/695) | 100.0% (695/695) | 0.0% (0/695) |
| 19 | 437 | 0.0% (0/437) | 100.0% (437/437) | 0.0% (0/437) | 980 | 0.0% (0/980) | 91.2% (894/980) | 8.8% (86/980) |
| 20 | 202 | 0.0% (0/202) | 100.0% (202/202) | 0.0% (0/202) | 419 | 0.0% (0/419) | 100.0% (419/419) | 0.0% (0/419) |
| 21 | 717 | 0.0% (0/717) | 100.0% (717/717) | 0.0% (0/717) | 1445 | 0.0% (0/1445) | 100.0% (1445/1445) | 0.0% (0/1445) |
| 22 | 494 | 0.0% (0/494) | 100.0% (494/494) | 0.0% (0/494) | 946 | 0.0% (0/946) | 100.0% (946/946) | 0.0% (0/946) |
| 23 | 493 | 0.0% (0/493) | 100.0% (493/493) | 0.0% (0/493) | 1022 | 0.0% (0/1022) | 100.0% (1022/1022) | 0.0% (0/1022) |
| 24 | 406 | 0.0% (0/406) | 100.0% (406/406) | 0.0% (0/406) | 833 | 0.0% (0/833) | 100.0% (833/833) | 0.0% (0/833) |
| 25 | 462 | 0.0% (0/462) | 100.0% (462/462) | 0.0% (0/462) | 853 | 0.0% (0/853) | 100.0% (853/853) | 0.0% (0/853) |
| 26 | 546 | 0.0% (0/546) | 100.0% (546/546) | 0.0% (0/546) | 1151 | 0.0% (0/1151) | 100.0% (1151/1151) | 0.0% (0/1151) |
| 27 | 554 | 0.0% (0/554) | 100.0% (554/554) | 0.0% (0/554) | 1249 | 0.0% (0/1249) | 100.0% (1249/1249) | 0.0% (0/1249) |
| 28 | 601 | 0.0% (0/601) | 100.0% (601/601) | 0.0% (0/601) | 1226 | 0.0% (0/1226) | 100.0% (1226/1226) | 0.0% (0/1226) |
| 29 | 776 | 0.0% (0/776) | 100.0% (776/776) | 0.0% (0/776) | 1575 | 0.0% (0/1575) | 100.0% (1575/1575) | 0.0% (0/1575) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 6; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (6/6).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/6).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (6/6).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- **1Krón 19:2** (végleges kapuhiba, `kezi`, linkek nélkül; `naplok/F22_1Kron_atnezes.tsv`): a felhasználóé. Kézi párosítás vagy újrafuttatás nélkül a vers 86 tokenje `fuggoben` marad.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs (mint a 3Móz–Jer menetekben); a versbeosztás a detektor szerint tiszta.
- A régi arany (2.2) 6 hármasa (1Krón 11:15, 14:9, 16:8, 20:4, 20:6, 20:8) mind egyezik (6/6); kis minta.

## 4. Kiegészítések ebben a menetben

- K9: az 1Krón bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `kovetkezo`, `ir`, D20, v2.14 (az `ag` nem változott).

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_1Kron.md`.
- Kézi átnézés: 1Krón 19:2.
- A következő könyv indítása a felhasználó döntése (⛔ 2.). A DT57 (1) mérése szerint a sorrend: 2Krón 169, Ezsd 162, Jób 159, Ez 147, Péld 145 szócikk; a Jób előtt TAHOT-hiány (Jób 40:1–5, 41) és döntés az 1:2 / 2:1 támogatásról.

## 6. Ellenőri kör (`naplok/ELLENOR_F22_1Kron.md`)

Az ellenőr 5 eltérést talált; a párosítási adatban hibát nem. A számokat Grep-számlálással igazolta, a szkripteket nem futtathatta.

| # | eltérés | kezelés |
|---|---|---|
| 1 | a régi arany némán 0: az `f22_elemzes.py` `--konyv 1Kron` (ASCII) névvel futott, a `regi_arany` szűrése (`startswith(konyv + ' ')`) így egy verset sem talált | javítva: újrafuttatás `--konyv 1Krón`-nal, a 2. szakasz cserélve; mért érték 100.0% (6/6). A 2.1 és 2.3 kimenete változatlan. Az eszköz ismeretlen könyvnévre nem jelez — nyitva (javaslat:az `f22_elemzes.py` álljon meg, ha a könyvnévre 0 Károli-vers jön) |
| 2 | az ág elavult a main-hez képest: a main-en a `szamkiosztas` már kiosztotta a DT70–DT73-at, az ág új szövegei a helyőrzőket (DT-F22e, DT-F77 …) használják; a brief fejléce és a SEMA 2.20 mindkét oldalon módosult, ütközés várható; a PR #249 már merge-elt | nyitva, felhasználói döntésre: a main beolvasztása és a helyőrzők cseréje, új PR |
| 3 | SEMA 2.20: a „minden link és szó `alacsony`” mondat nem igaz a `kezi` versekre (1Krón 19:2, Ézs 9:20, 64:1); a csak-Sonnet felsorolásból hiányoznak a Zsolt-fájlok és -jelentés | javítva |
| 4 | a k030 és a k075 hibájának leírása pontatlan (1. szakasz) | javítva |
| 5 | a 4. szakasz szerint az `ag` is változott, pedig nem | javítva |
