# F22_2Sam_jelentes.md — Károli–Strong párosítás: 2Sámuel (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 2Sám`, `egyesit.py --konyv 2Sám` és `--ellenoriz`, `f22_elemzes.py --konyv 2Sám`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 2Sám-sorainak összesítése (`futas = api_termeles/high/2Sam`, `cimke = 2sam`), a `f22/api_termeles/high/_munka/2Sam_k*.json` hibaüzenetei). Ág: `claude/peaceful-meitner-1vzy4m`, az Eszt-menet után; a main (`4435a17`, #265) az `53f57b9` merge-dzsel bevonva (ütközés nélkül). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a BDB-haszon mérése (`naplok/F22_konyvsorrend_meres.py`, 2026.10.09, a Jób után) szerint a tiszta versbeosztású könyvek közül a 2Sám adja a legtöbbet a hátralévő sornak (577 előfordulás, 86 NINCS-szócikk). Indítás: felhasználó, chat, 2026.10.09: „mehet” (a 2Sámuel javaslatára).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.09)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a 2Sám tiszta (695/695 vers, 24 fejezet), a listában nincs sora. Szimuláció: nyers 695 vers / 17 018 token = leképezett 695 vers / 17 018 token; Károli-vers pár nélkül és gazdátlan vers nincs; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'2Sám'`).
- **Minta:** `f22/minta_2Sam.tsv`, 695 vers (= a `Karoli_1908.tsv` `2Sám ` sorai), 70 köteg (10 vers/köteg, az utolsó 5).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01QK6hWwX7ECkYyWNyUbiaJY`, 70 kérés (2026-10-09T08:02Z); javító kör `msgbatch_01QyCxwcvj3GT5oRyi7wnvAJ`, 11 kérés (08:12Z).
- **Futásnapló** (2Sám: 81 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 70 | 59 | 11 köteg (28 vers) | 4,7020 | 807 455 / 778 917 |
| 2. próba (javító) | 11 | 10 | 1 köteg (1 vers) | 0,3420 | 152 498 / 37 899 |
| **összesen** | 81 | | | **5,0440** | |

A javító körbe került kötegek: 12, 15, 24, 35, 38, 39, 47, 54, 60, 65, 69. Egész köteg formátumhiba miatt nem bukott; a k054-ben 9 vers hiányzott a válaszból (a kapu „a válaszból hiányzik ez a vers” hibája), a többi versszintű kapuhiba (gazdátlan eredeti vagy magyar sorszám, többször szereplő magyar sorszám, hibás pár-forma, nem létező magyar sorszám; egy versnél több hiba is lehet).

**Végleges kapuhiba: 1 vers, 2Sám 23:16** (a k065 javító próbája is bukott: „4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban nem szerepelnek: [21]”). A vers 34 Károli- és 36 eredeti tokenje `fuggoben` / `kezi`, link nélkül; átnézési sor: `naplok/F22_2Sam_atnezes.tsv` (az 1Krón 19:2 mintájára).

A könyvplafonból (695 × 0,0074 × 1,5 = 7,71 USD) 5,04 fogyott; a futásnapló futó összege 53,4764 USD (Ézs–Eszt 48,4324 + 2Sám 5,0440), a globális 110 USD-ből. Versenként 0,0073 USD.

## 1a. Szkriptkimenet

```
Sonnet: 70 köteg, 695 vers; kapuhiba első próbára 4.0% (28/695); végleg 0.1% (1/695)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv 2Sám`: `parok_2Sam.tsv` 16 499 link (mind `alacsony`, `S`; a fájl 16 501 sora a proveniencia- és a fejlécsorral), `szavak_2Sam.tsv` 33 213 token (33 215 sor). A szavak bontása: hu 16 195 (13 025 `parositva`, 3 136 `betoldas`, 34 `fuggoben`), er 17 018 (15 296 `parositva`, 1 686 `forditatlan`, 36 `fuggoben`); az er szám = a `TAHOT_kivonat.tsv` `2Sám ` sorainak száma (17 018). A 70 `fuggoben` (`kezi`) token a 2Sám 23:16 verse.

`egyesit.py --ellenoriz --konyv 2Sám` (2026.10.09, ezen az ágon): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv 2Sám` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/16499), alacsony 100.0% (16499/16499), kezi 0.0% (0/16499); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/33213), alacsony 99.8% (33143/33213), kezi 0.2% (70/33213).

Link-forrás megoszlás (parok): S 16499. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 694 (2Sám 10:1, 2Sám 10:10, 2Sám 10:11, 2Sám 10:12, 2Sám 10:13, 2Sám 10:14, 2Sám 10:15, 2Sám 10:16, 2Sám 10:17, 2Sám 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 563 | 0.0% (0/563) | 100.0% (563/563) | 0.0% (0/563) | 1090 | 0.0% (0/1090) | 100.0% (1090/1090) | 0.0% (0/1090) |
| 2 | 748 | 0.0% (0/748) | 100.0% (748/748) | 0.0% (0/748) | 1487 | 0.0% (0/1487) | 100.0% (1487/1487) | 0.0% (0/1487) |
| 3 | 975 | 0.0% (0/975) | 100.0% (975/975) | 0.0% (0/975) | 1945 | 0.0% (0/1945) | 100.0% (1945/1945) | 0.0% (0/1945) |
| 4 | 359 | 0.0% (0/359) | 100.0% (359/359) | 0.0% (0/359) | 715 | 0.0% (0/715) | 100.0% (715/715) | 0.0% (0/715) |
| 5 | 514 | 0.0% (0/514) | 100.0% (514/514) | 0.0% (0/514) | 1024 | 0.0% (0/1024) | 100.0% (1024/1024) | 0.0% (0/1024) |
| 6 | 548 | 0.0% (0/548) | 100.0% (548/548) | 0.0% (0/548) | 1096 | 0.0% (0/1096) | 100.0% (1096/1096) | 0.0% (0/1096) |
| 7 | 744 | 0.0% (0/744) | 100.0% (744/744) | 0.0% (0/744) | 1393 | 0.0% (0/1393) | 100.0% (1393/1393) | 0.0% (0/1393) |
| 8 | 366 | 0.0% (0/366) | 100.0% (366/366) | 0.0% (0/366) | 747 | 0.0% (0/747) | 100.0% (747/747) | 0.0% (0/747) |
| 9 | 339 | 0.0% (0/339) | 100.0% (339/339) | 0.0% (0/339) | 655 | 0.0% (0/655) | 100.0% (655/655) | 0.0% (0/655) |
| 10 | 463 | 0.0% (0/463) | 100.0% (463/463) | 0.0% (0/463) | 936 | 0.0% (0/936) | 100.0% (936/936) | 0.0% (0/936) |
| 11 | 673 | 0.0% (0/673) | 100.0% (673/673) | 0.0% (0/673) | 1344 | 0.0% (0/1344) | 100.0% (1344/1344) | 0.0% (0/1344) |
| 12 | 797 | 0.0% (0/797) | 100.0% (797/797) | 0.0% (0/797) | 1627 | 0.0% (0/1627) | 100.0% (1627/1627) | 0.0% (0/1627) |
| 13 | 996 | 0.0% (0/996) | 100.0% (996/996) | 0.0% (0/996) | 1956 | 0.0% (0/1956) | 100.0% (1956/1956) | 0.0% (0/1956) |
| 14 | 925 | 0.0% (0/925) | 100.0% (925/925) | 0.0% (0/925) | 1924 | 0.0% (0/1924) | 100.0% (1924/1924) | 0.0% (0/1924) |
| 15 | 900 | 0.0% (0/900) | 100.0% (900/900) | 0.0% (0/900) | 1833 | 0.0% (0/1833) | 100.0% (1833/1833) | 0.0% (0/1833) |
| 16 | 577 | 0.0% (0/577) | 100.0% (577/577) | 0.0% (0/577) | 1159 | 0.0% (0/1159) | 100.0% (1159/1159) | 0.0% (0/1159) |
| 17 | 758 | 0.0% (0/758) | 100.0% (758/758) | 0.0% (0/758) | 1544 | 0.0% (0/1544) | 100.0% (1544/1544) | 0.0% (0/1544) |
| 18 | 885 | 0.0% (0/885) | 100.0% (885/885) | 0.0% (0/885) | 1837 | 0.0% (0/1837) | 100.0% (1837/1837) | 0.0% (0/1837) |
| 19 | 1236 | 0.0% (0/1236) | 100.0% (1236/1236) | 0.0% (0/1236) | 2457 | 0.0% (0/2457) | 100.0% (2457/2457) | 0.0% (0/2457) |
| 20 | 646 | 0.0% (0/646) | 100.0% (646/646) | 0.0% (0/646) | 1324 | 0.0% (0/1324) | 100.0% (1324/1324) | 0.0% (0/1324) |
| 21 | 580 | 0.0% (0/580) | 100.0% (580/580) | 0.0% (0/580) | 1210 | 0.0% (0/1210) | 100.0% (1210/1210) | 0.0% (0/1210) |
| 22 | 656 | 0.0% (0/656) | 100.0% (656/656) | 0.0% (0/656) | 1230 | 0.0% (0/1230) | 100.0% (1230/1230) | 0.0% (0/1230) |
| 23 | 583 | 0.0% (0/583) | 100.0% (583/583) | 0.0% (0/583) | 1307 | 0.0% (0/1307) | 94.6% (1237/1307) | 5.4% (70/1307) |
| 24 | 668 | 0.0% (0/668) | 100.0% (668/668) | 0.0% (0/668) | 1373 | 0.0% (0/1373) | 100.0% (1373/1373) | 0.0% (0/1373) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 8; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (8/8).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/8).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (8/8).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- **2Sám 23:16** (végleges kapuhiba, `kezi`, linkek nélkül; `naplok/F22_2Sam_atnezes.tsv`): a felhasználóé. Kézi párosítás vagy újrafuttatás nélkül a vers 70 tokenje `fuggoben` marad.
- A régi arany (2.2) 8 hármasa mind egyezik (8/8); kis minta.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- A main bevonása (`53f57b9`, #265), ütközés nélkül.
- K9: a 2Sám bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba (a 2Sám 23:16 a `kezi` példák között).
- A brief fejléce: `kovetkezo`, `ir`, D28, v2.22.

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_2Sam.md`.
- Kézi átnézés: 2Sám 23:16, Jób 16:22, 36:33, Péld 11:31; korábbról 1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1.
- A régi arany `Job.17.13` hármasa (`naplok/F22_Job_jelentes.md` 2.4): javasolt felvétel az `f21p/regi_arany_hibas.tsv`-be.
- PR és merge a felhasználóé (az ág a Péld-, a Bír-, a Jób-, az Eszt- és a 2Sám-menetet hordozza).
- A következő könyv a felhasználó döntése; a mérés (2026.10.09) szerinti tiszta jelöltek: 1Sám (524 / 86), 1Kir (509 / 99), Neh (479 / 96), 2Kir (413 / 87); a Dán (1644 / 312) előtt versbeosztás-döntés kell (37 detektorsor).

## 6. Ellenőri kör (`naplok/ELLENOR_F22_2Sam.md`)

Az ellenőr egy alacsony súlyú eltérést talált, adatot nem érint. A számokat pontos könyvegyezéssel (`\tapi_termeles/high/2Sam\t`, `cimke=2sam`, `^2Sám `, `2Sam_k*.json`) és `lekerdez.py`-jal igazolta; a merge pontosan a main változásait hozta. A PR valódi alapjával (`4435a17`) futtatott CI-ben HIBA nincs.

- **Végleges kapuhiba:** a 2Sám 23:16 átnézési sora, 34 + 36 `fuggoben`/`kezi` tokenje és a k065 2. próbájának hibája igazolva; link nincs.
- **Versbeosztás:** a detektorban és a kézi táblákban nincs 2Sám-sor; 695/695 kulcs; 1:1, 12:7, 24:25 tartalmilag egyezik.
- **Strong a TAHOT-ból:** 71 er-token mintavétele egyezik; minden nem-`fuggoben` er-sor egyetlen H-Strongot visel. Régi arany 8/8 igazolva.
- **Eltérés (M2, alacsony) — javítva:** a jelentés a main bevonását az `aa7ff55` commitnak tulajdonította; ez a merge üzenetének módosítása (`--amend`) előtti azonosító, a head-ben a merge `53f57b9` (azonos fa és szülők). A két hivatkozás ebben a commitban `53f57b9`-re javítva.
- **Nem ellenőrizhető az ellenőrnek:** a BDB-mérés számai (a mérést az orkesztrátor futtatta, 2026.10.09) és az `egyesit.py --ellenoriz` (az 1a szakasz saját futása igazolja).
