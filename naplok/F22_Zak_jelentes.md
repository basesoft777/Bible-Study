# F22_Zak_jelentes.md — Károli–Strong párosítás: Zakariás (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Zak`, `egyesit.py --konyv Zak` és `--ellenoriz`, `f22_elemzes.py --konyv Zak`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Zak-soraiból: `futas = api_termeles/high/Zak`, `cimke = zak`, a `f22/api_termeles/high/_munka/Zak_k*.json` hibaüzenetei). Ág: `claude/f22-zak` (külön worktree, a main `ebe8c417` commitjáról; az 1Kir PR #274, a Neh PR #275, a 2Kir PR #277, a Dán PR #279, a Ruth PR #280, a Jón PR #281, a Náh PR #283, a régi-arany PR #284, a Préd PR #285 és az Abd PR #286 már a main-en). Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a hiányzó kis könyvek egyike (211 vers); a választás a felhasználóé. Indítás: felhasználó, chat, 2026.10.11 („mehet a Zakariás”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint a Zak tiszta (211/211 vers, 14 fejezet, eltolt 0), a listában és a `versosszevonas.tsv`-ben nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Zak'`).
- **Minta:** `f22/minta_Zak.tsv`, 211 vers (= a `Karoli_1908.tsv` `Zak ` sorai), 22 köteg (10 vers/köteg, az utolsó 1).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01FbodRFAmmNPC2WSmvzV9Tp`, 22 kérés (2026-10-11T17:22Z); javító kör `msgbatch_01V7qiAksZXDvaeVMUEdJEiS`, 2 kérés (17:26Z).
- **Futásnapló** (Zak: 24 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 22 | 20 | 2 köteg (2 vers) | 1,2922 | 240 514 / 210 337 |
| 2. próba (javító) | 2 | 2 | 0 | 0,0423 | 26 987 / 3 064 |
| **összesen** | 24 | | | **1,3345** | |

A javító körbe került kötegek: 16 és 20 (1-1 vers); formátumhibás egész köteg nincs.

A könyvplafonból (211 × 0,0074 × 1,5 = 2,34 USD) 1,33 fogyott. A kumulatív összeg a futásnapló `api_termeles/` soraiból: 80,5636 USD (Ézs–Abd 79,2291 + Zak 1,3345), a globális 110 USD-ből; a `futo_osszeg_usd` oszlop utolsó sora is ennyi. Versenként 0,0063 USD (a plafon alapja 0,0074 alatt).

*Munkamódszer:* a menet saját worktree-ben (`C:\Users\bases\Desktop\Bible-Study-zak`) készült, ahogy a D36 előírja.

## 1a. Szkriptkimenet

```
Sonnet: 22 köteg, 211 vers; kapuhiba első próbára 0.9% (2/211); végleg 0.0% (0/211)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Zak`: `parok_Zak.tsv` 4 701 link (mind `alacsony`, `S`), `szavak_Zak.tsv` 9 510 token. A szavak bontása: hu 4 723 (3 855 `parositva`, 868 `betoldas`), er 4 787 (4 375 `parositva`, 412 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Zak ` sorainak száma (4 787). Az átnézési sor (`naplok/F22_Zak_atnezes.tsv`) üres (csak fejléc). A `/usage` nem mért (n.a.); a költség a futásnapló `batch_ar_szamolt` értéke.

`egyesit.py --konyv Zak --ellenoriz` (2026.10.11): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Zak` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/4701), alacsony 100.0% (4701/4701), kezi 0.0% (0/4701); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/9510), alacsony 100.0% (9510/9510), kezi 0.0% (0/9510).

Link-forrás megoszlás (parok): S 4701. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 211 (Zak 10:1, Zak 10:10, Zak 10:11, Zak 10:12, Zak 10:2, Zak 10:3, Zak 10:4, Zak 10:5, Zak 10:6, Zak 10:7).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 484 | 0.0% (0/484) | 100.0% (484/484) | 0.0% (0/484) | 972 | 0.0% (0/972) | 100.0% (972/972) | 0.0% (0/972) |
| 2 | 243 | 0.0% (0/243) | 100.0% (243/243) | 0.0% (0/243) | 472 | 0.0% (0/472) | 100.0% (472/472) | 0.0% (0/472) |
| 3 | 248 | 0.0% (0/248) | 100.0% (248/248) | 0.0% (0/248) | 488 | 0.0% (0/488) | 100.0% (488/488) | 0.0% (0/488) |
| 4 | 285 | 0.0% (0/285) | 100.0% (285/285) | 0.0% (0/285) | 575 | 0.0% (0/575) | 100.0% (575/575) | 0.0% (0/575) |
| 5 | 246 | 0.0% (0/246) | 100.0% (246/246) | 0.0% (0/246) | 506 | 0.0% (0/506) | 100.0% (506/506) | 0.0% (0/506) |
| 6 | 309 | 0.0% (0/309) | 100.0% (309/309) | 0.0% (0/309) | 612 | 0.0% (0/612) | 100.0% (612/612) | 0.0% (0/612) |
| 7 | 289 | 0.0% (0/289) | 100.0% (289/289) | 0.0% (0/289) | 591 | 0.0% (0/591) | 100.0% (591/591) | 0.0% (0/591) |
| 8 | 514 | 0.0% (0/514) | 100.0% (514/514) | 0.0% (0/514) | 1035 | 0.0% (0/1035) | 100.0% (1035/1035) | 0.0% (0/1035) |
| 9 | 358 | 0.0% (0/358) | 100.0% (358/358) | 0.0% (0/358) | 703 | 0.0% (0/703) | 100.0% (703/703) | 0.0% (0/703) |
| 10 | 251 | 0.0% (0/251) | 100.0% (251/251) | 0.0% (0/251) | 527 | 0.0% (0/527) | 100.0% (527/527) | 0.0% (0/527) |
| 11 | 362 | 0.0% (0/362) | 100.0% (362/362) | 0.0% (0/362) | 752 | 0.0% (0/752) | 100.0% (752/752) | 0.0% (0/752) |
| 12 | 333 | 0.0% (0/333) | 100.0% (333/333) | 0.0% (0/333) | 672 | 0.0% (0/672) | 100.0% (672/672) | 0.0% (0/672) |
| 13 | 240 | 0.0% (0/240) | 100.0% (240/240) | 0.0% (0/240) | 495 | 0.0% (0/495) | 100.0% (495/495) | 0.0% (0/495) |
| 14 | 539 | 0.0% (0/539) | 100.0% (539/539) | 0.0% (0/539) | 1110 | 0.0% (0/1110) | 100.0% (1110/1110) | 0.0% (0/1110) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 3; a Károli-szó/kifejezés nem található a vers tokenjei közt: 1.
- **Mért érték (kizárás nélkül, minden link):** 66.7% (2/3).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/3).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (2/2).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- Nincs: a Zakariásban nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- **Régi arany (2.2): 2/3, a kifejezés-egyeztetés műterméke.** A három hármas: `Zec.6.13 H3548 „pap”`, `Zec.6.13 H3678 „székében”`, `Zec.13.9 H7121+H8034 „segítségül hívja ... nevemet”`. A harmadik kifejezés-alakú, és a „...” a kihagyott szavakat jelöli (a Károli-szövegben „segítségül hívja **az én** nevemet” áll), ezért az `f22_elemzes.py` `kifejezes_helyek` függvénye (szó szerinti, egybefüggő tokensorozat-egyeztetés) nem találja a vers tokenjei közt. A párosítás viszont mindkét linket tartalmazza: `Zak 13:9` „segítségül” és „hívja” → H7121, „nevemet” → H9003+H8034+H9020 (`parok_Zak.tsv`, `szavak_Zak.tsv`). A 66,7% (2/3) tehát nem párosítási hiba; a „tájékoztató” sor 100,0% (2/2) a nem található hármast a nevezőből kihagyja. A „...” kezelése **nem lesz külön tétel** (a felhasználó döntése, 2026.10.11: 1 érintett hármas a teljes datasetben); az `f22_elemzes.py` változatlan marad.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- K9: a Zak bejegyezve az `adat/datasetek.tsv`-be (8 sor, a jelentéslistával együtt) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `ag`, `kovetkezo`, `ir`, D41, v2.35.

## 5. Nyitott (felhasználói) lépések

- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.
- A következő könyv(ek) a felhasználó döntése: az ÓSZ-ből még 10 kis könyv hiányzik (Én, Sir, Hós, Jóel, Ámós, Mik, Hab, Sof, Hag, Mal; együtt 992 vers); a Hós (1:11, 11:11) jóváhagyott 2:1 beolvasztást tartalmaz (`f22/versosszevonas.tsv`, DT92), ott kézi átnézési pont várható; a többi 9 beolvasztás nélküli.

## 6. Ellenőri kör (`naplok/ELLENOR_F22_Zak.md`)

Az ellenőr a számszerű állításokat (211/211, 4 701 / 9 510, 2/211 → 0, 1,3345 USD, 80,5636 USD, a futó összeg folytonossága, a 992 vers a 10 megmaradt könyvben) és a régi arany „műtermék” indoklását saját lekérdezéssel és a kód olvasásával igazolta; 2 eltérés:

- **A „külön tétel” nincs nyilvántartva (alacsony), lezárva (a felhasználó döntése, 2026.10.11):** az `f22_elemzes.py` „...” (kihagyásos kifejezés) kezelése nem lesz külön tétel, mert a teljes datasetben 1 hármast érint; ezért nincs N-F helyőrző sem, és a `NYITOTT_FELADATOK.md` nem változik.
- **Kozmetikai, javítva:** a `SEMA.md` 2.20 felsorolásából hiányzott egy vessző; pótolva. A jelentés 3. szakasza is pontosítva (nem a „...” token, hanem a vele jelölt kihagyás, „az én”, rontja az egyeztetést).

