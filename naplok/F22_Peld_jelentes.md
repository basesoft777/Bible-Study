# F22_Peld_jelentes.md — Károli–Strong párosítás: Példabeszédek (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Péld`, `egyesit.py --konyv Péld` és `--ellenoriz`, `f22_elemzes.py --konyv Péld`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Péld-sorainak összesítése (`futas = api_termeles/high/Peld`, `cimke = peld`), a `f22/api_termeles/high/_munka/Peld_k*.json` hibaüzenetei). Ág: `claude/peaceful-meitner-1vzy4m`, a main `51c8655` commitjáról. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a DT57 (1) mért listájából a Jób (159) és a Péld (145) maradt. A felhasználó először a Jóbot indította („mehet a jób”), majd a Jób versbeosztás-javaslata után a Példabeszédekre váltott (chat, 2026.10.09: „menjen helyette a példabeszédek”). A Jób-javaslat az 5. szakaszban áll, a repóba nem került.*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.09)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor csak a `nincs_karoli` Péld 12:28 sort jelezte; ez hibás. A versszám Károli 11/12 = 31/27, TAHOT 31/28; a többi fejezet egyezik. A Károli 11:31 második mondata („A ki szereti a dorgálást … oktalan az”, 15–30. szó) = TAHOT 12:1 (2:1, kézi beolvasztás, `f22/versosszevonas.tsv`); Károli 12:n → TAHOT 12:(n+1), n = 1–27 (`f22/versmegfeleltetes_kezi.tsv`, 27 `eltolt` + 1 `nincs_karoli` sor). Szimuláció: nyers 915 vers / 9 703 token = leképezett 914 vers / 9 695 token + 8 beolvasztott token; Károli-vers pár nélkül és gazdátlan (+1000) vers nincs. Jóváhagyta a felhasználó (chat, 2026.10.09: „Mehet a Péld. Jóváhagyom a versbeosztás-javítást”). A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Péld'`).
- **Minta:** `f22/minta_Peld.tsv`, 914 vers (= a `Karoli_1908.tsv` `Péld ` sorai), 92 köteg (10 vers/köteg, az utolsó 4).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01EoXLWjH6w22nok6AGcRUEx`, 92 kérés (2026-10-09T05:56Z); javító kör `msgbatch_01LsVC1RPD5PbHKMiZXqgcrs`, 15 kérés (06:00Z).
- **Futásnapló** (Péld: 107 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb` (mint az Ézs–Ez soraiban).

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 92 | 77 | 15 köteg (56 vers) | 2,2944 | 755 771 / 307 726 |
| 2. próba (javító) | 15 | 15 | 0 | 0,3183 | 141 328 / 35 390 |
| **összesen** | 107 | | | **2,6127** | |

A javító körbe került kötegek: 4, 13, 38, 46, 47, 50, 51, 54, 60, 67, 68, 77, 84, 85, 92. Ebből **öt köteg egészében bukott**, mert a válasz nem érvényes JSON (k038, k051, k054, k077 egyenként 10 vers, k092 4 vers; összesen 44 vers), tehát a forma volt hibás, nem a párosítás. A többi 12 vers versszintű kapuhiba (10 hibás pár-forma, 1 gazdátlan eredeti sorszám, 1 többször szereplő magyar sorszám).

A könyvplafonból (914 × 0,0074 × 1,5 = 10,15 USD) 2,61 fogyott; a futásnapló futó összege 39,0687 USD (Ézs–Ez 36,4560 + Péld 2,6127), a globális 110 USD-ből. Versenként 0,0029 USD (a plafon alapja 0,0074): a Péld rövid versei miatt a kimenet kicsi.

## 1a. Szkriptkimenet

```
Sonnet: 92 köteg, 914 vers; kapuhiba első próbára 6.1% (56/914); végleg 0.0% (0/914)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Péld`: `parok_Peld.tsv` 10 761 link (mind `alacsony`, `S`; a fájl 10 763 sora a proveniencia- és a fejlécsorral), `szavak_Peld.tsv` 21 781 token (21 783 sor). A szavak bontása: hu 12 078 (9 076 `parositva`, 2 986 `betoldas`, 16 `fuggoben`), er 9 703 (9 513 `parositva`, 182 `forditatlan`, 8 `fuggoben`); az er szám = a `TAHOT_kivonat.tsv` `Péld ` sorainak száma (9 703). A 24 `fuggoben` (`kezi`) token a beolvasztott rész: a Károli 11:31 15–30. szava és a TAHOT 12:1 8 szava, link nélkül. Az átnézési sor (`naplok/F22_Peld_atnezes.tsv`) ezt az egy verset tartalmazza (Péld 11:31).

`egyesit.py --ellenoriz --konyv Péld` (2026.10.09, ezen az ágon): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Péld` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/10761), alacsony 100.0% (10761/10761), kezi 0.0% (0/10761); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/21781), alacsony 99.9% (21757/21781), kezi 0.1% (24/21781).

Link-forrás megoszlás (parok): S 10761. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 914 (Péld 10:1, Péld 10:10, Péld 10:11, Péld 10:12, Péld 10:13, Péld 10:14, Péld 10:15, Péld 10:16, Péld 10:17, Péld 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 394 | 0.0% (0/394) | 100.0% (394/394) | 0.0% (0/394) | 747 | 0.0% (0/747) | 100.0% (747/747) | 0.0% (0/747) |
| 2 | 242 | 0.0% (0/242) | 100.0% (242/242) | 0.0% (0/242) | 469 | 0.0% (0/469) | 100.0% (469/469) | 0.0% (0/469) |
| 3 | 447 | 0.0% (0/447) | 100.0% (447/447) | 0.0% (0/447) | 839 | 0.0% (0/839) | 100.0% (839/839) | 0.0% (0/839) |
| 4 | 363 | 0.0% (0/363) | 100.0% (363/363) | 0.0% (0/363) | 651 | 0.0% (0/651) | 100.0% (651/651) | 0.0% (0/651) |
| 5 | 298 | 0.0% (0/298) | 100.0% (298/298) | 0.0% (0/298) | 551 | 0.0% (0/551) | 100.0% (551/551) | 0.0% (0/551) |
| 6 | 438 | 0.0% (0/438) | 100.0% (438/438) | 0.0% (0/438) | 817 | 0.0% (0/817) | 100.0% (817/817) | 0.0% (0/817) |
| 7 | 323 | 0.0% (0/323) | 100.0% (323/323) | 0.0% (0/323) | 602 | 0.0% (0/602) | 100.0% (602/602) | 0.0% (0/602) |
| 8 | 418 | 0.0% (0/418) | 100.0% (418/418) | 0.0% (0/418) | 838 | 0.0% (0/838) | 100.0% (838/838) | 0.0% (0/838) |
| 9 | 198 | 0.0% (0/198) | 100.0% (198/198) | 0.0% (0/198) | 385 | 0.0% (0/385) | 100.0% (385/385) | 0.0% (0/385) |
| 10 | 323 | 0.0% (0/323) | 100.0% (323/323) | 0.0% (0/323) | 696 | 0.0% (0/696) | 100.0% (696/696) | 0.0% (0/696) |
| 11 | 314 | 0.0% (0/314) | 100.0% (314/314) | 0.0% (0/314) | 732 | 0.0% (0/732) | 96.7% (708/732) | 3.3% (24/732) |
| 12 | 284 | 0.0% (0/284) | 100.0% (284/284) | 0.0% (0/284) | 612 | 0.0% (0/612) | 100.0% (612/612) | 0.0% (0/612) |
| 13 | 258 | 0.0% (0/258) | 100.0% (258/258) | 0.0% (0/258) | 565 | 0.0% (0/565) | 100.0% (565/565) | 0.0% (0/565) |
| 14 | 362 | 0.0% (0/362) | 100.0% (362/362) | 0.0% (0/362) | 794 | 0.0% (0/794) | 100.0% (794/794) | 0.0% (0/794) |
| 15 | 324 | 0.0% (0/324) | 100.0% (324/324) | 0.0% (0/324) | 744 | 0.0% (0/744) | 100.0% (744/744) | 0.0% (0/744) |
| 16 | 382 | 0.0% (0/382) | 100.0% (382/382) | 0.0% (0/382) | 786 | 0.0% (0/786) | 100.0% (786/786) | 0.0% (0/786) |
| 17 | 325 | 0.0% (0/325) | 100.0% (325/325) | 0.0% (0/325) | 685 | 0.0% (0/685) | 100.0% (685/685) | 0.0% (0/685) |
| 18 | 269 | 0.0% (0/269) | 100.0% (269/269) | 0.0% (0/269) | 563 | 0.0% (0/563) | 100.0% (563/563) | 0.0% (0/563) |
| 19 | 331 | 0.0% (0/331) | 100.0% (331/331) | 0.0% (0/331) | 708 | 0.0% (0/708) | 100.0% (708/708) | 0.0% (0/708) |
| 20 | 349 | 0.0% (0/349) | 100.0% (349/349) | 0.0% (0/349) | 699 | 0.0% (0/699) | 100.0% (699/699) | 0.0% (0/699) |
| 21 | 344 | 0.0% (0/344) | 100.0% (344/344) | 0.0% (0/344) | 711 | 0.0% (0/711) | 100.0% (711/711) | 0.0% (0/711) |
| 22 | 349 | 0.0% (0/349) | 100.0% (349/349) | 0.0% (0/349) | 695 | 0.0% (0/695) | 100.0% (695/695) | 0.0% (0/695) |
| 23 | 457 | 0.0% (0/457) | 100.0% (457/457) | 0.0% (0/457) | 879 | 0.0% (0/879) | 100.0% (879/879) | 0.0% (0/879) |
| 24 | 447 | 0.0% (0/447) | 100.0% (447/447) | 0.0% (0/447) | 859 | 0.0% (0/859) | 100.0% (859/859) | 0.0% (0/859) |
| 25 | 357 | 0.0% (0/357) | 100.0% (357/357) | 0.0% (0/357) | 741 | 0.0% (0/741) | 100.0% (741/741) | 0.0% (0/741) |
| 26 | 336 | 0.0% (0/336) | 100.0% (336/336) | 0.0% (0/336) | 713 | 0.0% (0/713) | 100.0% (713/713) | 0.0% (0/713) |
| 27 | 351 | 0.0% (0/351) | 100.0% (351/351) | 0.0% (0/351) | 712 | 0.0% (0/712) | 100.0% (712/712) | 0.0% (0/712) |
| 28 | 350 | 0.0% (0/350) | 100.0% (350/350) | 0.0% (0/350) | 732 | 0.0% (0/732) | 100.0% (732/732) | 0.0% (0/732) |
| 29 | 300 | 0.0% (0/300) | 100.0% (300/300) | 0.0% (0/300) | 626 | 0.0% (0/626) | 100.0% (626/626) | 0.0% (0/626) |
| 30 | 456 | 0.0% (0/456) | 100.0% (456/456) | 0.0% (0/456) | 924 | 0.0% (0/924) | 100.0% (924/924) | 0.0% (0/924) |
| 31 | 372 | 0.0% (0/372) | 100.0% (372/372) | 0.0% (0/372) | 706 | 0.0% (0/706) | 100.0% (706/706) | 0.0% (0/706) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 16; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (16/16).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/16).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (16/16).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- **Péld 11:31** (`naplok/F22_Peld_atnezes.tsv`): a beolvasztott rész (hu 15–30 = TAHOT 12:1) link nélkül, `kezi`; a kézi párosítás a felhasználóé, mint az Ézs 9:20 és 64:1 esetén.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs (mint a 3Móz–Ez menetekben).
- A régi arany (2.2) 16 hármasa mind egyezik (16/16); kis minta.

## 4. Kiegészítések ebben a menetben

- K9: a Péld bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba (a kézi megfeleltetés és a Péld 11:31 beolvasztás is).
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D24, v2.18.

## 5. A Jób versbeosztása: javaslat, nem alkalmazva

A menet a Jóbbal indult; a felhasználó a javaslat láttán a Példabeszédekre váltott, ezért a Jób-módosítás visszavonva, a repóba nem került. A megállapítások a következő Jób-menethez:

- **Jób 16:22 / 17:** a Károli 16:22 = TAHOT 16:22 + **TAHOT 17:1** („Lelkem meghanyatlott … vár rám a sír”, a Károli 16:22 14–21. szava, 2:1); Károli 17:n → TAHOT 17:(n+1), n = 1–15. A detektor csak a fejezet végét (17:10–15) jelzi, a 17:1–9-et nem, tehát a listája itt hibás.
- **Jób 36:33 / 37:** a Károli 36:33 = TAHOT 36:33 + **TAHOT 37:1** („Ezért remeg az én szívem … helyéből”, 13–21. szó, 2:1); Károli 37:n → TAHOT 37:(n+1), n = 1–23. A detektor itt is csak a 37:21–23-at jelzi.
- **Jób 38–42:** a #83 kézi táblája (Károli 40:1–19 → TAHOT 40:6–24) a main-ben van; a **Jób 41-hez (34 vers) nincs `TAHOT_kivonat`-adat** (N-F83a, kulcsgenerátor-javítás).
- Szimuláció a fenti javításokkal: a Jób 1068 Károli-verséből 1034 párosítható, nyers 1036 TAHOT-vers / 12 150 token = leképezett 1034 vers / 12 130 token + 20 beolvasztott token; gazdátlan vers nincs; pár nélkül csak a Jób 41 34 verse.
- Döntés kell: a Jób a 41. fejezet nélkül fusson most, vagy előbb az N-F83a.

## 6. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_Peld.md`.
- Kézi átnézés: Péld 11:31; a korábbiak (1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1) továbbra is a felhasználóé.
- PR és merge a felhasználóé.
- A következő könyv: a DT57 (1) mért listájából csak a Jób maradt (5. szakasz); az indítás a felhasználó döntése.

## 7. Ellenőri kör (`naplok/ELLENOR_F22_Peld.md`)

Az ellenőr eltérést nem talált (TISZTA). A számokat pontos könyvegyezéssel (`\tapi_termeles/high/Peld\t`, `cimke=peld`, `^Péld `, `Peld_k*.json`) és `lekerdez.py`-jal igazolta. A szkripteket (`egyesit.py --ellenoriz`) nem futtathatta; ezt az 1a szakasz saját futása igazolja. A saját CI-futásában HIBA szintű találat nincs (az E27 92 találata repószintű, a main-en is ugyanannyi).

- **Versbeosztás:** a Károli 11:31 15–30. szava = TAHOT 12:1, a Károli 12:1, 12:14, 12:27 = TAHOT 12:2, 12:15, 12:28 (tartalmi összevetés a tükörfordítással); a TAHOT 12:1 8 tokenje `kezi`-ként a 11:31 er-soraiban, a Strong egyezik.
- **Strong a TAHOT-ból:** 67 er-token mintavétele (1:1, 11:31, 12:1, 12:14, 12:27, 31:31) 67/67 egyezik.
- **Régi arany:** a 16 `Pro.` hármas mind a várt Károli-szónál és Strongnál áll (16/16).
- **Javítva az ellenőr tájékoztatója nyomán:** a brief `ir` mezőjében az `f22/versosszevonas.tsv` kétszer szerepelt; a duplikátum kikerült.
- **Tájékoztató, nem javítva:** a `datasetek.tsv` szavak-sorai a kézi beolvasztásból csak a 4Móz 29:39-et nevezik meg (az Ézs és a Péld nincs benne); a SEMA 2.20 a teljes listát tartalmazza. A korábbi menetek óta így áll, külön tétel lehet.
