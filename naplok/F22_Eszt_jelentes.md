# F22_Eszt_jelentes.md — Károli–Strong párosítás: Eszter (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Eszt`, `egyesit.py --konyv Eszt` és `--ellenoriz`, `f22_elemzes.py --konyv Eszt`, `naplok/F22_konyvsorrend_meres.py`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Eszt-sorainak összesítése (`futas = api_termeles/high/Eszt`, `cimke = eszt`), a `f22/api_termeles/high/_munka/Eszt_k*.json` hibaüzenetei). Ág: `claude/peaceful-meitner-1vzy4m`, a Péld-, a Bír- és a Jób-menet után; a main (`1f420a7`, #263, #264) az `aee98c0` merge-dzsel bevonva. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek.*

*Sorrend: a DT57 (1) mért listája a Jóbbal elfogyott. A BDB-haszon mérése (`naplok/F22_konyvsorrend_meres.py`, 2026-10-09, a Péld, a Bír és a Jób után) szerint a 7. adag (649–969) 321 szócikkéből 317 már `van` (98,8%); a maradék NINCS/kevés szócikkek előfordulásából az Eszt adja a legtöbbet (148, 2 NINCS-szócikk; utána a Dán 40), a hátralévő sorban 443 / 77. A versbeosztás tiszta, a könyv kicsi. Indítás: felhasználó, chat, 2026.10.09: „mehet az eszter”.*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.09)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint az Eszt tiszta (167/167 vers, 10 fejezet), a listában nincs sora. Szimuláció: nyers 167 vers / 4 857 token = leképezett 167 vers / 4 857 token; Károli-vers pár nélkül és gazdátlan vers nincs; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Eszt'`).
- **Minta:** `f22/minta_Eszt.tsv`, 167 vers (= a `Karoli_1908.tsv` `Eszt ` sorai), 17 köteg (10 vers/köteg, az utolsó 7).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_015p7ZexYDEc6uZcBeVZUpEM`, 17 kérés (2026-10-09T07:32Z); javító kör `msgbatch_01T8W3jEA84zhadwqJpPfa7y`, 3 kérés (07:42Z).
- **Futásnapló** (Eszt: 20 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, minden sor `finish_reason=end_turn`, `koltseg_forras=batch_ar_szamolt`, `prompt_sha256_12` minden soron `84f12ca7aafb`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 17 | 14 | 3 köteg (3 vers) | 1,3002 | 212 034 / 217 638 |
| 2. próba (javító) | 3 | 3 | 0 | 0,0612 | 45 686 / 3 112 |
| **összesen** | 20 | | | **1,3614** | |

A javító körbe került kötegek: 3, 8, 12 (Eszt 2:8, 5:3, 8:2); mindhárom versszintű kapuhiba (gazdátlan eredeti sorszám), formátumhiba nincs.

A könyvplafonból (167 × 0,0074 × 1,5 = 1,85 USD) 1,36 fogyott; a futásnapló futó összege 48,4324 USD (Ézs–Jób 47,0709 + Eszt 1,3614), a globális 110 USD-ből. Versenként 0,0082 USD, a plafon alapja (0,0074) fölött: az Eszter hosszú elbeszélő versei (versenként 29,1 héber szó) miatt a kimenet nagy (217 638 token).

## 1a. Szkriptkimenet

```
Sonnet: 17 köteg, 167 vers; kapuhiba első próbára 1.8% (3/167); végleg 0.0% (0/167)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Eszt`: `parok_Eszt.tsv` 4 500 link (mind `alacsony`, `S`; a fájl 4 502 sora a proveniencia- és a fejlécsorral), `szavak_Eszt.tsv` 9 062 token (9 064 sor). A szavak bontása: hu 4 205 (3 586 `parositva`, 619 `betoldas`), er 4 857 (4 223 `parositva`, 634 `forditatlan`); `fuggoben` és `kezi` nincs. Az er szám = a `TAHOT_kivonat.tsv` `Eszt ` sorainak száma (4 857). Az átnézési sor (`naplok/F22_Eszt_atnezes.tsv`) üres (csak fejléc).

`egyesit.py --ellenoriz --konyv Eszt` (2026.10.09, ezen az ágon): „ellenőrzés: rendben”.

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Eszt` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/4500), alacsony 100.0% (4500/4500), kezi 0.0% (0/4500); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/9062), alacsony 100.0% (9062/9062), kezi 0.0% (0/9062).

Link-forrás megoszlás (parok): S 4500. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 167 (Eszt 10:1, Eszt 10:2, Eszt 10:3, Eszt 1:1, Eszt 1:10, Eszt 1:11, Eszt 1:12, Eszt 1:13, Eszt 1:14, Eszt 1:15).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 547 | 0.0% (0/547) | 100.0% (547/547) | 0.0% (0/547) | 1113 | 0.0% (0/1113) | 100.0% (1113/1113) | 0.0% (0/1113) |
| 2 | 631 | 0.0% (0/631) | 100.0% (631/631) | 0.0% (0/631) | 1271 | 0.0% (0/1271) | 100.0% (1271/1271) | 0.0% (0/1271) |
| 3 | 455 | 0.0% (0/455) | 100.0% (455/455) | 0.0% (0/455) | 911 | 0.0% (0/911) | 100.0% (911/911) | 0.0% (0/911) |
| 4 | 427 | 0.0% (0/427) | 100.0% (427/427) | 0.0% (0/427) | 831 | 0.0% (0/831) | 100.0% (831/831) | 0.0% (0/831) |
| 5 | 380 | 0.0% (0/380) | 100.0% (380/380) | 0.0% (0/380) | 786 | 0.0% (0/786) | 100.0% (786/786) | 0.0% (0/786) |
| 6 | 402 | 0.0% (0/402) | 100.0% (402/402) | 0.0% (0/402) | 808 | 0.0% (0/808) | 100.0% (808/808) | 0.0% (0/808) |
| 7 | 277 | 0.0% (0/277) | 100.0% (277/277) | 0.0% (0/277) | 574 | 0.0% (0/574) | 100.0% (574/574) | 0.0% (0/574) |
| 8 | 526 | 0.0% (0/526) | 100.0% (526/526) | 0.0% (0/526) | 1054 | 0.0% (0/1054) | 100.0% (1054/1054) | 0.0% (0/1054) |
| 9 | 784 | 0.0% (0/784) | 100.0% (784/784) | 0.0% (0/784) | 1571 | 0.0% (0/1571) | 100.0% (1571/1571) | 0.0% (0/1571) |
| 10 | 71 | 0.0% (0/71) | 100.0% (71/71) | 0.0% (0/71) | 143 | 0.0% (0/143) | 100.0% (143/143) | 0.0% (0/143) |

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

- Nincs: az Eszterben nem volt kézi beolvasztás, és végleges kapuhiba sincs.
- **Régi arany nincs a könyvben** (0 hármas a `Karoli_Strong_kivonat.tsv`-ben): ezen a könyvön nincs külső pontossági támpont.
- Tájékoztató: a `forditatlan` er-tokenek aránya 13,1% (634/4 857), magasabb a Bír (9,4%) és a Jób (3,7%) értékénél. Ez a modell állítása (Károli nem fordította le a szót); hogy a próza tárgyjelölőiből és névelőiből adódik-e, azt ez a menet nem mérte.
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- A main bevonása (`aee98c0`): a brief `kovetkezo`-ütközése feloldva (az ág mezője maradt; a main-en lezárt #77-fejléc teendő kivéve).
- K9: az Eszt bejegyezve az `adat/datasetek.tsv`-be (8 sor) és az `adat/SEMA.md` 2.20-ba.
- A brief fejléce: `kovetkezo`, `ir`, D27, v2.21.

## 5. Nyitott (felhasználói) lépések

- ~~Független szúrópróba (22.6)~~: elmarad (DT70).
- Független ellenőr: `naplok/ELLENOR_F22_Eszt.md`.
- Kézi átnézés: Jób 16:22, 36:33, Péld 11:31; korábbról 1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1.
- A régi arany `Job.17.13` hármasa (`naplok/F22_Job_jelentes.md` 2.4): javasolt felvétel az `f21p/regi_arany_hibas.tsv`-be.
- PR és merge a felhasználóé (az ág a Péld-, a Bír-, a Jób- és az Eszt-menetet hordozza).
- A következő könyv a felhasználó döntése; a mérés szerinti tiszta jelöltek: 2Sám (577 / 86), 1Sám (524 / 86), 1Kir (509 / 99), Neh (479 / 96), 2Kir (413 / 87); a Dán (1644 / 312) előtt versbeosztás-döntés kell (37 detektorsor).
