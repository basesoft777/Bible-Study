# F22_Zsid_jelentes.md — Károli–Strong párosítás: Zsid (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Zsid`, `egyesit.py --konyv Zsid` és `--ellenoriz`, `f22_elemzes.py --konyv Zsid`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Zsid-soraiból: `futas = api_termeles/high/Zsid`, `cimke = zsid`). Ág: `claude/f22-usz-b`. Módszer: `prompt_v3` változatlanul, **Sonnet a Message Batches API-n, `effort=high`** (DT73 (a)), **a C (Gemini) kimarad** (DT-F22c), 10 verses kötegek. Eredeti szöveg: `konkordancia/TAGNT_kivonat.tsv` (TR-szűrés: a `[nem TR]` szó a `prompt_v3` K szabálya szerint `forditatlan`).*

*Sorrend: a 22.9 B csomag (Gal, Ef, Zsid; a 2Kor visszatartva; D45) egyike; a futtatás soros, ebben a sorrendben. Keret: 18 USD az ÚSZ-re (`api_koteg.PLAFON_USD` 104,36). Indítás: felhasználói utasítás (chat, 2026.10.12: „Gal, Ef, Zsid mehet. A 2Kor-t tartsd vissza …”).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.12)**, `naplok/F22_versbeosztas_jovahagyas.md`: a felhasználó közvetlen ellenőrzése alapján. `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Zsid'`).
- **Minta:** `f22/minta_Zsid.tsv`, 303 vers a modellhez, 31 köteg (10 vers/köteg).
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01K45BvmGezRZCzwNAXgyJrX`, 31 kérés (2026-10-12T10:49:15+00:00); 2. kör `msgbatch_013g4itBGmvNdggSzv4TPfJG`, 4 kérés (2026-10-12T10:52:58+00:00).
- **Futásnapló** (Zsid: 35 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

| kör | kérés | kapun átment | kapun bukott | költség (USD) | bemenet / kimenet token |
|---|---|---|---|---|---|
| 1. próba | 31 | 27 | 4 köteg | 1.5332 | 289 779 / 248 680 |
| 2. próba (javító) | 4 | 4 | 0 köteg | 0.0713 | 39 953 / 6 271 |
| **összesen** | 35 | | | **1.6045** | |

A javító körbe került köteg: k016 (10 vers); versenkénti kapuhiba: 4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban ne. A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k028 (10 vers); versenkénti kapuhiba: 4. ezek az eredeti szavak sem a "parok" jobb oldalán, sem a "forditatlan"-ban ne. A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k030 (10 vers); versenkénti kapuhiba: 3. ezek a magyar szavak sem a "parok" bal oldalán, sem a "betoldas"-ban nem szer. A javító kör eredménye a fenti táblában.

A javító körbe került köteg: k031 (3 vers); egész köteg formátumhibás (az 1. próba nyers válasza nem érvényes JSON: „1. a válasz nem érvényes JSON: Extra data: line 3 column 1 (”). A javító kör eredménye a fenti táblában.

Költségplafon: a könyvplafon 303 vers × 0,0074 × 1,5 = 3.3633 USD (az `api_koteg.py` beépített alsó határa 1,00 USD, tehát a tényleges plafon 3.36 USD); a könyv költsége 1.6045 USD (versenként 0.0053 USD, a modellhez ment 303 versre). A futásnapló `futo_osszeg_usd` oszlopának utolsó Zsid-sora: 94.504948 USD, a 18 USD-s ÚSZ-keretből (D45: 86,3698 + 18; a kódbeli plafon `PLAFON_USD` = 104,36 USD).

## 1a. Szkriptkimenet

```
Sonnet: 31 köteg, 303 vers; kapuhiba első próbára 2.0% (6/303); végleg 0.0% (0/303)
C: 0 köteg, 0 vers; kapuhiba első próbára n.é. (0/0); végleg n.é. (0/0)
C költség: 0.000000 USD, 0 hívás, bemenet 0, kimenet 0 (ebből gondolkodás 0) token
```

`egyesit.py --konyv Zsid`: parok: 4765 sor {'alacsony': 4765}; szavak: 10241 sor {'alacsony': 10045, 'kezi': 196}; átnézési sor: 6 vers; ellenőrzés: rendben

A szavak bontása: hu 913 `betoldas`, 108 `fuggoben`, 4194 `parositva`; er 695 `forditatlan`, 88 `fuggoben`, 4243 `parositva`. Az átnézési sor (`naplok/F22_Zsid_atnezes.tsv`): 6 vers.

`egyesit.py --konyv Zsid --ellenoriz` (2026.10.12): „rendben”.

### 1b. A `[nem TR]` eredeti szavak (22.8 P4, 22.9)

92 `[nem TR]` token; állapot szerint: 80 `forditatlan`, 3 `fuggoben`, 9 `parositva`. Eltérés az elvárttól (`forditatlan`): Zsid 2:1 er 10 (παραρυῶμεν.¶, G3901) → parositva; Zsid 3:9 er 7 (ἐν, G1722) → fuggoben; Zsid 3:9 er 8 (δοκιμασίᾳ, G6020) → fuggoben; Zsid 3:10 er 5 (ταύτῃ, G3778) → fuggoben; Zsid 4:2 er 16 (συγκεκερασμένους, G4786) → parositva; Zsid 4:7 er 13 (προείρηται,, G4280) → parositva; Zsid 9:14 er 19 (ἡμῶν, G3165) → parositva; Zsid 10:2 er 16 (κεκαθαρισμένους., G2511) → parositva; Zsid 11:12 er 18 (ἡ, G3588) → parositva; Zsid 13:15 er 8 (παντὸς, G3956) → parositva; Zsid 13:18 er 4 (πειθόμεθα, G3982) → parositva; Zsid 13:21 er 15 (ἡμῖν, G3165) → parositva

## 2. Ellenőrzés a könyvön (22.5)

*Minden szám az `eszkozok/karoli_strong/f22_elemzes.py --konyv Zsid` kimenetéből.*

### 2.1 Arányok

Összesen: linkek (parok): magas 0.0% (0/4765), alacsony 100.0% (4765/4765), kezi 0.0% (0/4765); szavak (tokenek, Károli és eredeti együtt): magas 0.0% (0/10241), alacsony 98.1% (10045/10241), kezi 1.9% (196/10241).

Link-forrás megoszlás (parok): S 4765. Csak egy modell által átjutott (a másik kapuhibás) versek, amelyekben nincs S+C sor: 297 (Zsid 10:1, Zsid 10:10, Zsid 10:11, Zsid 10:12, Zsid 10:13, Zsid 10:14, Zsid 10:15, Zsid 10:16, Zsid 10:17, Zsid 10:18).

| fejezet | linkek | magas | alacsony | kezi | szavak | magas | alacsony | kezi |
|---|---|---|---|---|---|---|---|---|
| 1 | 227 | 0.0% (0/227) | 100.0% (227/227) | 0.0% (0/227) | 504 | 0.0% (0/504) | 100.0% (504/504) | 0.0% (0/504) |
| 2 | 331 | 0.0% (0/331) | 100.0% (331/331) | 0.0% (0/331) | 668 | 0.0% (0/668) | 100.0% (668/668) | 0.0% (0/668) |
| 3 | 263 | 0.0% (0/263) | 100.0% (263/263) | 0.0% (0/263) | 580 | 0.0% (0/580) | 88.6% (514/580) | 11.4% (66/580) |
| 4 | 290 | 0.0% (0/290) | 100.0% (290/290) | 0.0% (0/290) | 591 | 0.0% (0/591) | 100.0% (591/591) | 0.0% (0/591) |
| 5 | 229 | 0.0% (0/229) | 100.0% (229/229) | 0.0% (0/229) | 472 | 0.0% (0/472) | 100.0% (472/472) | 0.0% (0/472) |
| 6 | 286 | 0.0% (0/286) | 100.0% (286/286) | 0.0% (0/286) | 618 | 0.0% (0/618) | 100.0% (618/618) | 0.0% (0/618) |
| 7 | 402 | 0.0% (0/402) | 100.0% (402/402) | 0.0% (0/402) | 925 | 0.0% (0/925) | 92.9% (859/925) | 7.1% (66/925) |
| 8 | 278 | 0.0% (0/278) | 100.0% (278/278) | 0.0% (0/278) | 575 | 0.0% (0/575) | 100.0% (575/575) | 0.0% (0/575) |
| 9 | 471 | 0.0% (0/471) | 100.0% (471/471) | 0.0% (0/471) | 1029 | 0.0% (0/1029) | 100.0% (1029/1029) | 0.0% (0/1029) |
| 10 | 528 | 0.0% (0/528) | 100.0% (528/528) | 0.0% (0/528) | 1154 | 0.0% (0/1154) | 100.0% (1154/1154) | 0.0% (0/1154) |
| 11 | 639 | 0.0% (0/639) | 100.0% (639/639) | 0.0% (0/639) | 1336 | 0.0% (0/1336) | 100.0% (1336/1336) | 0.0% (0/1336) |
| 12 | 453 | 0.0% (0/453) | 100.0% (453/453) | 0.0% (0/453) | 1007 | 0.0% (0/1007) | 93.6% (943/1007) | 6.4% (64/1007) |
| 13 | 368 | 0.0% (0/368) | 100.0% (368/368) | 0.0% (0/368) | 782 | 0.0% (0/782) | 100.0% (782/782) | 0.0% (0/782) |

Gyanús fejezetek (nincs link, vagy a linkek `magas` aránya < 70%; versszámozás-eltolódás vagy más rendszerhiba jele): 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13.

### 2.2 Régi arany (konkordancia/Karoli_Strong_kivonat.tsv)

- Minden régi-arany hármas a könyvben: 8; a Károli-szó/kifejezés nem található a vers tokenjei közt: 2.
- **Mért érték (kizárás nélkül, minden link):** 75.0% (6/8).
- Csak a `magas` linkekkel (a nevező ugyanaz, tehát alsó becslés): 0.0% (0/8).
- A `magas` tokenekre korlátozva (azok a hármasok, amelyeknél a Károli-token(ek) mind `magas` bizonyosságúak; a találat a `magas` token linkjein): n.é. (0/0).
- Tájékoztató (az `f21p/regi_arany_hibas.tsv` hibásnak jelölt hármasai kizárva; nem a mért érték): 100.0% (6/6).

### 2.3 A 20 leggyakoribb eltérés-típus az alacsony tokenekből

Eltérő Károli-token (két modell partnerhalmaza különbözik) összesen: 0; különböző típus (magyar szó, Sonnet-jelölt, C-jelölt): 0. A jelölt a partnerek TAHOT-Strongja; `betoldas` = nincs link.

| # | magyar szó | Sonnet (táblába kerül) | C | db | mintapélda |
|---|---|---|---|---|---|

## 3. Kézi átnézésre jelölt pontok

- `Zsid 3:9`: N-F22c: a nyers TAGNT `Heb.3.10[3.9]` sorai (2 szó) a kivonatból kimaradtak; a vers a KJV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Zsid 3:10`: N-F22c: a nyers TAGNT `Heb.3.10[3.9]` sorai (2 szó) a kivonatból kimaradtak; a vers a NRSV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Zsid 7:20`: N-F22c: a nyers TAGNT `Heb.7.20[7.21]` sorai (8 szó) a kivonatból kimaradtak; a vers a NRSV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Zsid 7:21`: N-F22c: a nyers TAGNT `Heb.7.20[7.21]` sorai (8 szó) a kivonatból kimaradtak; a vers a KJV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Zsid 12:22`: N-F22c: a nyers TAGNT `Heb.12.22[12.23]` sorai (1 szó) a kivonatból kimaradtak; a vers a NRSV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- `Zsid 12:23`: N-F22c: a nyers TAGNT `Heb.12.22[12.23]` sorai (1 szó) a kivonatból kimaradtak; a vers a KJV-kulcs szerint érintett, a görög szöveg részleges lehet; a Károli-kulcs a kivonat javítása után dől el (a felhasználó döntése, 2026.10.12)
- Régi arany: l. a 2.2-t; az eltérő hármasok tartalmi ítélete a felhasználóé (nem e menet dolga).
- A „gyanús fejezetek” listája a 2.1-ben formális: egy modell fut, `magas` nincs.

## 4. Kiegészítések ebben a menetben

- A B csomag összesítője: `naplok/F22_USZ_B_jelentes.md`.

## 5. Nyitott (felhasználói) lépések

- Független ellenőrzés: a csomag után, közösen (`naplok/ELLENOR_F22_USZ_B.md`); ez a jelentés nem „ellenőrzött”.
- Független szúrópróba (22.6): elmarad (DT70).
- PR és merge a felhasználóé.

## Utólagos javítás (2026.10.19)

A Zsid 1:1–2 tokenszintű vershatár-eltérés (a Károli 1:1 vége „ez utolsó időkben szólott nékünk Fia által” = a TAGNT 1:2 1–9. tokenje): a két vers `kezi` kényszerbe került (`f22/kezi_versek_Zsid.tsv`), `parok_Zsid.tsv` 4 844 link, `szavak_Zsid.tsv` 64 `fuggoben` sor. Részletek: `naplok/F22_C_elokeszites.md` 3.
