# F22_1Sam_jelentes.md — Károli–Strong párosítás: 1Sámuel (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 1Sám`, `egyesit.py --konyv 1Sám` és `--ellenoriz`, `f22_elemzes.py --konyv 1Sám`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 1Sám-sorainak összesítése (`futas = api_termeles/high/1Sam`, `cimke = 1sam`), a `f22/api_termeles/high/_munka/1Sam_k*.json` hibaüzenetei). Ág: `claude/peaceful-meitner-1vzy4m`, a main `63d4f78` commitjáról (a #266 és a #267 merge után). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a BDB-haszon mérése (`naplok/F22_konyvsorrend_meres.py`, 2026.10.09) szerint a 2Sám után a tiszta versbeosztású könyvek közül az 1Sám (524 előfordulás, 86 NINCS-szócikk) és az 1Kir (509 / 99) adja a legtöbbet. Indítás: felhasználó, chat, 2026.10.09: „menjen 1sámuel”.*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.09)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint az 1Sám tiszta (811/811 vers, 31 fejezet), a listában nincs sora. Szimuláció: nyers 811 vers / 20 727 token = leképezett 811 vers / 20 727 token; Károli-vers pár nélkül és gazdátlan vers nincs; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. Az ismert 1Sám 20:43 (Károli önálló vers = MT 21:1) a `TAHOT_kivonat` kulcsgenerálásánál már Károli-kulcsot kapott (`eszkozok/tahot_karoli_kulcs_generalas.py`, `KULON_SOR_KIVETEL`), ezért itt nincs teendő. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'1Sám'`).
- **Minta:** `f22/minta_1Sam.tsv`, 811 vers (= a `Karoli_1908.tsv` `1Sám ` sorai), 82 köteg (10 vers/köteg, az utolsó 1).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_016NsEkvz89AQeVDRL6W7vqH`, 82 kérés (2026-10-09T08:35Z); javító kör `msgbatch_01Le9zujQYrNaBdUjtgai3Mt`, 17 kérés (08:47Z).
- **Futásnapló** (1Sám: 99 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 82 | 65 | 17 köteg (30 vers) | 5,6918 | 965 922 / 945 178 |
| 2. próba (javító) | 17 | 17 | 0 | 0,4610 | 245 262 / 43 148 |
| **összesen** | 99 | | | **6,1528** | |

A javító körbe került kötegek: 12, 13, 14, 22, 27, 37, 40, 50, 53, 54, 64, 67, 69, 70, 71, 78, 81. Ebből **egy köteg egészében bukott** (k013, 10 vers), mert a válasz nem érvényes JSON; a többi 20 vers versszintű kapuhiba (főleg gazdátlan eredeti vagy magyar sorszám, egy hibás pár-forma és egy többször szereplő magyar sorszám; egy versnél több hiba is lehet).

A könyvplafonból (811 × 0,0074 × 1,5 = 9,00 USD) 6,15 fogyott; a futásnapló futó összege 59,6292 USD (Ézs–2Sám 53,4764 + 1Sám 6,1528), a globális 110 USD-ből. Versenként 0,0076 USD (a plafon alapja 0,0074 fölött).

## 1a. Szkriptkimenet

```
Sonnet: 82 köteg, 811 vers; kapuhiba első próbára 3.7% (30/811); végleg 0.0% (0/811)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 1Sám`: `parok_1Sam.tsv` 20 152 link (mind `alacsony`, `S`; a fájl 20 154 sora a proveniencia- és a fejlécsorral), `szavak_1Sam.tsv` 40 376 token (40 378 sor). A szavak bontása: hu 19 649 (16 103 `parositva`, 3 546 `betoldas`), er 20 727 (18 799 `parositva`, 1 928 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `1Sám ` sorainak száma (20 727). Az átnézési sor (`naplok/F22_1Sam_atnezes.tsv`) üres (csak fejléc).

`egyesit.py --ellenoriz --konyv 1Sám` (2026.10.09, ezen az ágon): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 1Sám` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/20152), alacsony 100.0% (20152/20152), kezi 0.0% (0/20152); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/40376), alacsony 100.0% (40376/40376), kezi 0.0% (0/40376).

Link-forrás megoszlás (parok): S 20152. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 811 (1Sám 10:1, 1Sám 10:10, 1Sám 10:11, 1Sám 10:12, 1Sám 10:13, 1Sám 10:14, 1Sám 10:15, 1Sám 10:16, 1Sám 10:17, 1Sám 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 643 | 0.0% (0/643) | 100.0% (643/643) | 0.0% (0/643) | 1259 | 0.0% (0/1259) | 100.0% (1259/1259) | 0.0% (0/1259) |
| 2 | 843 | 0.0% (0/843) | 100.0% (843/843) | 0.0% (0/843) | 1672 | 0.0% (0/1672) | 100.0% (1672/1672) | 0.0% (0/1672) |
| 3 | 449 | 0.0% (0/449) | 100.0% (449/449) | 0.0% (0/449) | 885 | 0.0% (0/885) | 100.0% (885/885) | 0.0% (0/885) |
| 4 | 534 | 0.0% (0/534) | 100.0% (534/534) | 0.0% (0/534) | 1107 | 0.0% (0/1107) | 100.0% (1107/1107) | 0.0% (0/1107) |
| 5 | 306 | 0.0% (0/306) | 100.0% (306/306) | 0.0% (0/306) | 625 | 0.0% (0/625) | 100.0% (625/625) | 0.0% (0/625) |
| 6 | 561 | 0.0% (0/561) | 100.0% (561/561) | 0.0% (0/561) | 1165 | 0.0% (0/1165) | 100.0% (1165/1165) | 0.0% (0/1165) |
| 7 | 411 | 0.0% (0/411) | 100.0% (411/411) | 0.0% (0/411) | 833 | 0.0% (0/833) | 100.0% (833/833) | 0.0% (0/833) |
| 8 | 444 | 0.0% (0/444) | 100.0% (444/444) | 0.0% (0/444) | 846 | 0.0% (0/846) | 100.0% (846/846) | 0.0% (0/846) |
| 9 | 769 | 0.0% (0/769) | 100.0% (769/769) | 0.0% (0/769) | 1550 | 0.0% (0/1550) | 100.0% (1550/1550) | 0.0% (0/1550) |
| 10 | 675 | 0.0% (0/675) | 100.0% (675/675) | 0.0% (0/675) | 1395 | 0.0% (0/1395) | 100.0% (1395/1395) | 0.0% (0/1395) |
| 11 | 374 | 0.0% (0/374) | 100.0% (374/374) | 0.0% (0/374) | 749 | 0.0% (0/749) | 100.0% (749/749) | 0.0% (0/749) |
| 12 | 632 | 0.0% (0/632) | 100.0% (632/632) | 0.0% (0/632) | 1252 | 0.0% (0/1252) | 100.0% (1252/1252) | 0.0% (0/1252) |
| 13 | 519 | 0.0% (0/519) | 100.0% (519/519) | 0.0% (0/519) | 1108 | 0.0% (0/1108) | 100.0% (1108/1108) | 0.0% (0/1108) |
| 14 | 1263 | 0.0% (0/1263) | 100.0% (1263/1263) | 0.0% (0/1263) | 2625 | 0.0% (0/2625) | 100.0% (2625/2625) | 0.0% (0/2625) |
| 15 | 782 | 0.0% (0/782) | 100.0% (782/782) | 0.0% (0/782) | 1567 | 0.0% (0/1567) | 100.0% (1567/1567) | 0.0% (0/1567) |
| 16 | 563 | 0.0% (0/563) | 100.0% (563/563) | 0.0% (0/563) | 1147 | 0.0% (0/1147) | 100.0% (1147/1147) | 0.0% (0/1147) |
| 17 | 1398 | 0.0% (0/1398) | 100.0% (1398/1398) | 0.0% (0/1398) | 2853 | 0.0% (0/2853) | 100.0% (2853/2853) | 0.0% (0/2853) |
| 18 | 687 | 0.0% (0/687) | 100.0% (687/687) | 0.0% (0/687) | 1376 | 0.0% (0/1376) | 100.0% (1376/1376) | 0.0% (0/1376) |
| 19 | 600 | 0.0% (0/600) | 100.0% (600/600) | 0.0% (0/600) | 1194 | 0.0% (0/1194) | 100.0% (1194/1194) | 0.0% (0/1194) |
| 20 | 1025 | 0.0% (0/1025) | 100.0% (1025/1025) | 0.0% (0/1025) | 2079 | 0.0% (0/2079) | 100.0% (2079/2079) | 0.0% (0/2079) |
| 21 | 416 | 0.0% (0/416) | 100.0% (416/416) | 0.0% (0/416) | 810 | 0.0% (0/810) | 100.0% (810/810) | 0.0% (0/810) |
| 22 | 632 | 0.0% (0/632) | 100.0% (632/632) | 0.0% (0/632) | 1253 | 0.0% (0/1253) | 100.0% (1253/1253) | 0.0% (0/1253) |
| 23 | 700 | 0.0% (0/700) | 100.0% (700/700) | 0.0% (0/700) | 1343 | 0.0% (0/1343) | 100.0% (1343/1343) | 0.0% (0/1343) |
| 24 | 591 | 0.0% (0/591) | 100.0% (591/591) | 0.0% (0/591) | 1137 | 0.0% (0/1137) | 100.0% (1137/1137) | 0.0% (0/1137) |
| 25 | 1218 | 0.0% (0/1218) | 100.0% (1218/1218) | 0.0% (0/1218) | 2369 | 0.0% (0/2369) | 100.0% (2369/2369) | 0.0% (0/2369) |
| 26 | 705 | 0.0% (0/705) | 100.0% (705/705) | 0.0% (0/705) | 1417 | 0.0% (0/1417) | 100.0% (1417/1417) | 0.0% (0/1417) |
| 27 | 319 | 0.0% (0/319) | 100.0% (319/319) | 0.0% (0/319) | 622 | 0.0% (0/622) | 100.0% (622/622) | 0.0% (0/622) |
| 28 | 674 | 0.0% (0/674) | 100.0% (674/674) | 0.0% (0/674) | 1316 | 0.0% (0/1316) | 100.0% (1316/1316) | 0.0% (0/1316) |
| 29 | 355 | 0.0% (0/355) | 100.0% (355/355) | 0.0% (0/355) | 671 | 0.0% (0/671) | 100.0% (671/671) | 0.0% (0/671) |
| 30 | 767 | 0.0% (0/767) | 100.0% (767/767) | 0.0% (0/767) | 1543 | 0.0% (0/1543) | 100.0% (1543/1543) | 0.0% (0/1543) |
| 31 | 297 | 0.0% (0/297) | 100.0% (297/297) | 0.0% (0/297) | 608 | 0.0% (0/608) | 100.0% (608/608) | 0.0% (0/608) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 1; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (1/1).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/1).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (1/1).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- Nincs: az 1Sámuelben nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- A régi arany (2.2) egyetlen hármasa (1Sám 2:6, H7585) egyezik (1/1); kis minta.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: az 1Sám bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `kovetkezo`, `ir`, D29, v2.23.

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_1Sam.md`.
- Kézi átnézés: 2Sám 23:16, Jób 16:22, 36:33, Péld 11:31; korábbról 1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1.
- A régi arany `Job.17.13` hármasa (`naplok/F22_Job_jelentes.md` 2.4): javasolt felvétel az `f21p/regi_arany_hibas.tsv`-be.
- PR és merge a felhasználóé.
- A következő könyv a felhasználó döntése; a mérés (2026.10.09) szerinti tiszta jelöltek: 1Kir (509 / 99), Neh (479 / 96), 2Kir (413 / 87); a Dán (1644 / 312) előtt versbeosztás-döntés kell (37 detektorsor).

## 6. Ellenőri kör (`naplok/ELLENOR_F22_1Sam.md`)

Az ellenőr eltérést nem talált (TISZTA). A számokat pontos könyvegyezéssel (`api_termeles/high/1Sam`, `cimke=1sam`, `^1Sám `, `1Sam_k*.json`) és `lekerdez.py`-jal igazolta; a CI saját futásában HIBA nincs (az E25 3 és az E27 92 találata előzményi).

- **Versbeosztás:** a detektorban és a kézi táblákban nincs 1Sám-sor; 811/811 kulcs mindkét oldalon; az 1Sám 20:43 Károli-kulcsa a TAHOT-ban (`KULON_SOR_KIVETEL`) igazolva; 1:1, 20:43, 31:13 és 24:1 tartalmilag egyezik.
- **Strong a TAHOT-ból:** 1:1, 17:4, 20:43, 31:13 (69 er-token) tokenről tokenre egyezik. Régi arany 1/1 igazolva.
- **Nem ellenőrizhető az ellenőrnek:** az `egyesit.py --ellenoriz` (az 1a szakasz saját futása igazolja) és a chat-idézet. Az indító feladatleírás tévesen `840f6f8` head-et adott meg; a helyes tartomány (`63d4f78..b884bcb`) utólagos javítással ment.
