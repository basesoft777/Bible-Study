# F22_1Kir_jelentes.md — Károli–Strong párosítás: 1Királyok (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 1Kir`, `egyesit.py --konyv 1Kir` és `--ellenoriz`, `f22_elemzes.py --konyv 1Kir`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 1Kir-sorainak összesítése (`futas = api_termeles/high/1Kir`, `cimke = 1kir`), a `f22/api_termeles/high/_munka/1Kir_k*.json` hibaüzenetei). Ág: `claude/f22-1kir`, a main `7789466` commitjáról. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a BDB-haszon mérése (`naplok/F22_konyvsorrend_meres.py`, 2026.10.09) szerint az 1Sám után a tiszta versbeosztású könyvek közül az 1Kir (509 előfordulás, 99 NINCS-szócikk) adja a legtöbbet. Indítás: felhasználó, chat, 2026.10.11; az előkészítés („1Királyok, csak az előkészítés”) után a futást is a chatben hagyta jóvá (utólagos megerősítés a független ellenőr J-pontjára, 2026.10.11: „igen, jóváhagytam a chatben”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint az 1Kir tiszta (817/817 vers, 22 fejezet), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'1Kir'`).
- **Minta:** `f22/minta_1Kir.tsv`, 817 vers (= a `Karoli_1908.tsv` `1Kir ` sorai), 82 köteg (10 vers/köteg, az utolsó 7).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01RJgdMzbpW5oGEwUNSeox85`, 82 kérés (2026-10-11T09:24Z); javító kör `msgbatch_01EoT7P2PY1VvPw9SL1GyawP`, 15 kérés (09:29Z).
- **Futásnapló** (1Kir: 97 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 82 | 67 | 15 köteg (27 vers) | 5,8552 | 957 085 / 979 631 |
| 2. próba (javító) | 15 | 15 | 0 | 0,3968 | 214 718 / 36 407 |
| **összesen** | 97 | | | **6,2520** | |

A javító körbe került kötegek: 8, 10, 13, 19, 23, 26, 31, 32, 48, 49, 51, 69, 73, 78, 80. Ebből **egy köteg egészében bukott** (k049, 10 vers), mert a válasz nem érvényes JSON; a többi 17 vers versszintű kapuhiba (k010 2, k023 3, a többi köteg 1-1 vers).

A könyvplafonból (817 × 0,0074 × 1,5 = 9,07 USD) 6,25 fogyott; a futásnapló futó összege 65,8812 USD (Ézs–1Sám 59,6292 + 1Kir 6,2520), a globális 110 USD-ből. Versenként 0,0077 USD (a plafon alapja 0,0074 fölött).

## 1a. Szkriptkimenet

```
Sonnet: 82 köteg, 817 vers; kapuhiba első próbára 3.3% (27/817); végleg 0.0% (0/817)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 1Kir`: `parok_1Kir.tsv` 19 827 link (mind `alacsony`, `S`; a fájl 19 829 sora a proveniencia- és a fejlécsorral), `szavak_1Kir.tsv` 39 945 token (39 947 sor). A szavak bontása: hu 19 796 (15 848 `parositva`, 3 948 `betoldas`), er 20 149 (18 005 `parositva`, 2 144 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `1Kir ` sorainak száma (20 149). Az átnézési sor (`naplok/F22_1Kir_atnezes.tsv`) üres (csak fejléc). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --ellenoriz --konyv 1Kir` (2026.10.11, ezen az ágon): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 1Kir` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/19827), alacsony 100.0% (19827/19827), kezi 0.0% (0/19827); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/39945), alacsony 100.0% (39945/39945), kezi 0.0% (0/39945).

Link-forrás megoszlás (parok): S 19827. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 817 (1Kir 10:1, 1Kir 10:10, 1Kir 10:11, 1Kir 10:12, 1Kir 10:13, 1Kir 10:14, 1Kir 10:15, 1Kir 10:16, 1Kir 10:17, 1Kir 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 1269 | 0.0% (0/1269) | 100.0% (1269/1269) | 0.0% (0/1269) | 2569 | 0.0% (0/2569) | 100.0% (2569/2569) | 0.0% (0/2569) |
| 2 | 1262 | 0.0% (0/1262) | 100.0% (1262/1262) | 0.0% (0/1262) | 2418 | 0.0% (0/2418) | 100.0% (2418/2418) | 0.0% (0/2418) |
| 3 | 727 | 0.0% (0/727) | 100.0% (727/727) | 0.0% (0/727) | 1494 | 0.0% (0/1494) | 100.0% (1494/1494) | 0.0% (0/1494) |
| 4 | 557 | 0.0% (0/557) | 100.0% (557/557) | 0.0% (0/557) | 1152 | 0.0% (0/1152) | 100.0% (1152/1152) | 0.0% (0/1152) |
| 5 | 464 | 0.0% (0/464) | 100.0% (464/464) | 0.0% (0/464) | 889 | 0.0% (0/889) | 100.0% (889/889) | 0.0% (0/889) |
| 6 | 710 | 0.0% (0/710) | 100.0% (710/710) | 0.0% (0/710) | 1548 | 0.0% (0/1548) | 100.0% (1548/1548) | 0.0% (0/1548) |
| 7 | 1035 | 0.0% (0/1035) | 100.0% (1035/1035) | 0.0% (0/1035) | 2370 | 0.0% (0/2370) | 100.0% (2370/2370) | 0.0% (0/2370) |
| 8 | 1842 | 0.0% (0/1842) | 100.0% (1842/1842) | 0.0% (0/1842) | 3579 | 0.0% (0/3579) | 100.0% (3579/3579) | 0.0% (0/3579) |
| 9 | 710 | 0.0% (0/710) | 100.0% (710/710) | 0.0% (0/710) | 1399 | 0.0% (0/1399) | 100.0% (1399/1399) | 0.0% (0/1399) |
| 10 | 670 | 0.0% (0/670) | 100.0% (670/670) | 0.0% (0/670) | 1383 | 0.0% (0/1383) | 100.0% (1383/1383) | 0.0% (0/1383) |
| 11 | 1042 | 0.0% (0/1042) | 100.0% (1042/1042) | 0.0% (0/1042) | 2065 | 0.0% (0/2065) | 100.0% (2065/2065) | 0.0% (0/2065) |
| 12 | 874 | 0.0% (0/874) | 100.0% (874/874) | 0.0% (0/874) | 1746 | 0.0% (0/1746) | 100.0% (1746/1746) | 0.0% (0/1746) |
| 13 | 904 | 0.0% (0/904) | 100.0% (904/904) | 0.0% (0/904) | 1877 | 0.0% (0/1877) | 100.0% (1877/1877) | 0.0% (0/1877) |
| 14 | 806 | 0.0% (0/806) | 100.0% (806/806) | 0.0% (0/806) | 1592 | 0.0% (0/1592) | 100.0% (1592/1592) | 0.0% (0/1592) |
| 15 | 753 | 0.0% (0/753) | 100.0% (753/753) | 0.0% (0/753) | 1505 | 0.0% (0/1505) | 100.0% (1505/1505) | 0.0% (0/1505) |
| 16 | 833 | 0.0% (0/833) | 100.0% (833/833) | 0.0% (0/833) | 1614 | 0.0% (0/1614) | 100.0% (1614/1614) | 0.0% (0/1614) |
| 17 | 557 | 0.0% (0/557) | 100.0% (557/557) | 0.0% (0/557) | 1097 | 0.0% (0/1097) | 100.0% (1097/1097) | 0.0% (0/1097) |
| 18 | 1122 | 0.0% (0/1122) | 100.0% (1122/1122) | 0.0% (0/1122) | 2303 | 0.0% (0/2303) | 100.0% (2303/2303) | 0.0% (0/2303) |
| 19 | 581 | 0.0% (0/581) | 100.0% (581/581) | 0.0% (0/581) | 1177 | 0.0% (0/1177) | 100.0% (1177/1177) | 0.0% (0/1177) |
| 20 | 1184 | 0.0% (0/1184) | 100.0% (1184/1184) | 0.0% (0/1184) | 2348 | 0.0% (0/2348) | 100.0% (2348/2348) | 0.0% (0/2348) |
| 21 | 742 | 0.0% (0/742) | 100.0% (742/742) | 0.0% (0/742) | 1457 | 0.0% (0/1457) | 100.0% (1457/1457) | 0.0% (0/1457) |
| 22 | 1183 | 0.0% (0/1183) | 100.0% (1183/1183) | 0.0% (0/1183) | 2363 | 0.0% (0/2363) | 100.0% (2363/2363) | 0.0% (0/2363) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 5; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (5/5).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/5).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (5/5).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- Nincs: az 1Királyokban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A régi arany (2.2) öt hármasa (1Kir 2:6, 2:9 H7585; 18:24, 18:25, 18:26 H7121 + H8034) egyezik (5/5); kis minta.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: az 1Kir bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `kovetkezo`, `ir`, D30, v2.24.
- Ez a jelentés az ellenőri kör (6.) után a 22.5 szerinti teljes alakra bővült (az első változat 13 soros összefoglaló volt).

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Kézi átnézés: 2Sám 23:16, Jób 16:22, 36:33, Péld 11:31; korábbról 1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1.
- A régi arany `Job.17.13` hármasa (`naplok/F22_Job_jelentes.md` 2.4): javasolt felvétel az `f21p/regi_arany_hibas.tsv`-be.
- PR és merge a felhasználóé.
- A következő könyv a felhasználó döntése; a mérés (2026.10.09) szerinti tiszta jelöltek: Neh (479 / 96), 2Kir (413 / 87); a Dán (1644 / 312) előtt versbeosztás-döntés kell (37 detektorsor).

## 6. Ellenőri kör (`naplok/ELLENOR_F22_1Kir.md`)

Az ellenőr 4 eltérést talált; a számszerű állításokat (817/817, 19 827 / 39 945, 27/817 → 0, 5/5, 6,252 USD, 65,88 USD) saját lekérdezéssel igazolta, a CI saját futásában a diffre HIBA nincs (az E25 3 és az E27 33 találata repószintű).

- **J (magas), a futtatási jóváhagyás:** a repóban csak az előkészítés jóváhagyása állt. A felhasználó megerősítette, hogy a futást a chatben jóváhagyta; rögzítve a D30-ban és e jelentés fejlécében.
- **Brief (közepes):** `kovetkezo`, `ir`, D30, v2.24 pótolva.
- **K9 (közepes):** `adat/datasetek.tsv` (8 sor) és `adat/SEMA.md` 2.20 pótolva.
- **K4 / 22.5 (közepes):** a fejezetenkénti arány (2.1), a szavak hu/er × állapot bontása (1a), a körönkénti tokenösszeg (1.) és a `/usage` n.a. jelölése pótolva.
- **Nem ellenőrizhető az ellenőrnek:** az `egyesit.py --ellenoriz` (az 1a szakasz saját futása igazolja) és a chat-idézet.
