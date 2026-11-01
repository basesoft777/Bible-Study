# BDB_FORDITAS — a 8. adag (sorrend 966–1388): tábla-Δ és commitonkénti bontás (E17, DT3)

*A #38 (BDB_FORDITAS) 8. adagának szakaszonkénti fordítása (4 szelet + 1 félkész köztes commit) és az ellenőrzés 1. javítóköre (`naplok/ELLENOR_F38_adag8.md` 3. tétel, DT362). Tartomány: `b64294ed` (a menet előtti alap) → `90e88881` (a javítókör utolsó adat- és döntés-commitja; az `adat/` utolsó változása a `c2f6ac59`). Minden szám saját méréssel készült; az adatsor a komment- (`#`) és a fejlécsor nélküli, nem üres sor. Minta: `naplok/BDB_FORDITAS_nf107b_bontas.md`.*

## 1. Tábla-Δ

| tábla | alap (`b64294ed`) | fej (`90e88881`) | Δ | `git diff --numstat` (+/−) |
|---|---|---|---|---|
| `adat/forditasok.tsv` | 5 360 | 7 996 | +2 636 | 2636 / 0 |
| minden más `adat/` tábla | — | — | 0 | — |
| `konkordancia/` (minden tábla) | — | — | 0 | — |

A 2 636 új sor mind `sz<n>` sor (423 Strong teljes szakaszszáma; a szakasztábla szerint 2 636). Módosított és törölt sor az alap és a fej között: 0 (a javítókör 14 sorának módosítása az ugyanebben a menetben hozzáadott sorokat érinti, ezért az alap–fej különbségben nem látszik). Más változott fájl: `naplok/EMELES_munka.tsv` (2636 / 0; munkatábla), `F38_BDB_FORDITAS_BRIEF.md` (fejléc), `DONTESEK.md` (DT361, DT362), `naplok/ELLENOR_F38_adag8.md`, és ez a napló.

**Hatókör.** A `naplok/BDB_FORDITAS_sorrend.tsv` szerint a 8. adag a 966–1387 sorrend (422 szócikk); a záró szelet a 9. adag első szócikkét (sorrend 1388, H6297, 4 szakaszsor) is lefordította (DT362 (5): a H6297 marad, a #67 kapuját (DT55) elkészültekor rá is le kell futtatni). A fenti 423 Strong és 2 636 sor ezzel együtt értendő: 422 + 1.

*(proveniencia: scope=adat/forditasok.tsv @ b64294ed és @ 90e88881; adat/, konkordancia/ | forras=`git show <rev>:adat/forditasok.tsv`, `split('\t')`, megszámolt nem üres, nem `#` sor a fejléc nélkül (→ 5360 és 7996); `git diff --numstat b64294ed 90e88881 -- adat konkordancia naplok/EMELES_munka.tsv` (→ 2636 0 adat/forditasok.tsv; 2636 0 naplok/EMELES_munka.tsv; rögzített revízió, nem mozgó HEAD) | ts=2026-10-26T13:32Z)*

## 2. Commitonkénti bontás (`adat/forditasok.tsv`)

Új sor: a commit utáni sorok, amelyeknek az 5 elsődleges kulcsmezője (`szotar`, `strong`, `entry_id`, `jelentes_szam`, `mezo`) a szülőben nem szerepelt. Módosított: ugyanaz a kulcs, de a sor tartalma más.

| commit | tartalom | új sor (`sz<n>`) | módosított | törölt | érintett Strong |
|---|---|---|---|---|---|
| `db22c0f2` | 1. szelet (F38.387) | 729 | 0 | 0 | 116 |
| `cfed5c52` | 2. szelet félkész (F38.388; csak a munkatábla) | 0 | 0 | 0 | 0 |
| `a831e926` | 2. szelet (F38.389) | 825 | 0 | 0 | 127 |
| `866fbf88` | 3. szelet (F38.390) | 843 | 0 | 0 | 135 |
| `fb0b4e6a` | záró szelet (F38.391) | 239 | 0 | 0 | 45 |
| `de8d20a7` | javítókör: H1969 `megjegyzes` (F38.392; 1.) | 0 | 8 (`megjegyzes`) | 0 | 1 |
| `487e1272` | javítókör: H2574 sz2 jel + `megjegyzes` (F38.393; 2.) | 0 | 2 (1 `forditas_hu` + `megjegyzes`, 1 `megjegyzes`) | 0 | 1 |
| `c2f6ac59` | javítókör: H7621 sz4, sz6; H1032 sz2, sz4 (F38.394; 6.) | 0 | 4 (`forditas_hu`) | 0 | 2 |
| `90e88881` | javítókör: DONTESEK.md DT361 hivatkozás (F38.395; 7.; nem adat) | 0 | 0 | 0 | 0 |
| **összesen** | | **2 636** | (a javítókör 14 módosítása) | **0** | **423** |

Ellenőrzés: 729 + 825 + 843 + 239 = 2 636 = az 1. szakasz Δ-ja; 5 360 + 2 636 = 7 996. A `cfed5c52` csak a `naplok/EMELES_munka.tsv`-t érintette (a stop hook kényszerítette köztes commit, a H5126 kapu-megállása miatt), az `adat/`-ot nem.

*(proveniencia: scope=adat/forditasok.tsv @ <commit>^ és @ <commit>, kilenc commit: db22c0f2, cfed5c52, a831e926, 866fbf88, fb0b4e6a, de8d20a7, 487e1272, c2f6ac59, 90e88881 | forras=saját szkript (`git show <rev>:adat/forditasok.tsv`, `split('\t')`, kulcs = az első öt mező; módosított = azonos kulcs, eltérő sor) | ts=2026-10-26T13:32Z)*

## 3. Szeletenként a Strongok és a forráskarakterszám

**A mérés módja.** A szelet Strongjai: a 2. szakasz szerint az adott commitban hozzáadott `strong` értékek. (a) A `adat/bdb_szakaszok.tsv` `szoveg` oszlopának karakterhossza (Python `len`) összegezve a Strong minden szakaszán. (b) Ugyanez a fordító tényleges bemenetén: `eszkozok/bdb_jelolt/szakasz_bemenet.py` `szakaszok(strong)` → `nezet(...)` (csak a `hivatkozas` típusú javítások alkalmazva; token nélkül). (c) A commitüzenet, a jelentés és a brief szerinti szám.

| szelet | commit | Strong | szakaszsor | (a) szakasz-`szoveg` | (b) javított nézet | (c) a commitüzenet szerint |
|---|---|---|---|---|---|---|
| 1. | `db22c0f2` | 116 | 729 | 148 348 | 150 306 | 149 693 |
| 2. | `a831e926` | 127 | 825 | 146 395 | 148 698 | — (a jelentésben 139 751) |
| 3. | `866fbf88` | 135 | 843 | 147 926 | 150 261 | — (a brief-ben 140 278) |
| 4. (záró) | `fb0b4e6a` | 45 | 239 | 49 984 | 50 597 | — (a brief-ben 46 458) |
| **összesen** | | **423** | **2 636** | **492 653** | **499 862** | |

A 2.–4. szelet (c) számai a `szakasz_elokeszit` által írt `p/` fájlok hosszai, ahol a héber és görög szöveget ⟦n⟧ helyőrzők helyettesítik, ezért a (b)-nél kisebbek. Az 1. szelet 149 693-as számának mérési alapját a commit nem rögzíti. A (b) mérés a fordító tényleges bemenetének karakterszáma.

A szeletek Strongjai:

- 1. (116): H0197 H0212 H0325 H0423 H0591 H0676 H0748 H0759 H0816 H0860 H1361 H1416 H1436 H1530 H1653 H1661 H1993 H2236 H2244 H2280 H2370 H2377 H2399 H2474 H2518 H2563 H2574 H2600 H2623 H2859 H2876 H2898 H2919 H2934 H3051 H3123 H3233 H3243 H3409 H3563 H3577 H3582 H3611 H3612 H3618 H3629 H3715 H3812 H3816 H3830 H3876 H3972 H4219 H4283 H4318 H4436 H4578 H4603 H4643 H4676 H4847 H4900 H4932 H5116 H5236 H5254 H5358 H5401 H5514 H5518 H5592 H5643 H5678 H5680 H5695 H5705 H5941 H5980 H6040 H6187 H6189 H6203 H6212 H6231 H6241 H6442 H6486 H6524 H6643 H6654 H6779 H6822 H6845 H6883 H6884 H6955 H7045 H7065 H7098 H7107 H7186 H7414 H7416 H7440 H7561 H7622 H7832 H7887 H8184 H8227 H8328 H8398 H8426 H8615 H8643 H8668
- 2. (127): H0054 H0117 H0138 H0183 H0191 H0543 H0550 H0974 H1032 H1065 H1100 H1201 H1259 H1263 H1310 H1314 H1322 H1406 H1497 H1819 H1826 H1926 H1952 H2007 H2154 H2204 H2254 H2266 H2406 H2449 H2492 H2498 H2513 H2608 H2689 H2713 H2820 H2942 H3088 H3104 H3213 H3259 H3316 H3341 H3394 H3411 H3442 H3568 H3639 H3727 H3801 H3836 H3887 H3978 H4161 H4170 H4296 H4327 H4417 H4487 H4513 H4541 H4546 H4598 H4604 H5003 H5074 H5079 H5081 H5087 H5090 H5126 H5175 H5360 H5423 H5488 H5521 H5594 H5645 H5648 H5665 H5818 H5867 H5956 H6099 H6224 H6260 H6341 H6346 H6413 H6459 H6509 H6539 H6591 H6601 H6903 H7110 H7136 H7151 H7185 H7257 H7259 H7399 H7493 H7562 H7621 H7797 H7848 H7854 H7857 H7939 H7967 H8003 H8052 H8066 H8071 H8181 H8213 H8251 H8300 H8345 H8392 H8433 H8518 H8573 H8577 H8659
- 3. (135): H0029 H0052 H0060 H0188 H0200 H0281 H0343 H0606 H0644 H0697 H0769 H0906 H0957 H1162 H1215 H1290 H1319 H1396 H1478 H1548 H1722 H1777 H1823 H1832 H1840 H1897 H1935 H2143 H2146 H2340 H2344 H2347 H2371 H2435 H2483 H2530 H2637 H2664 H2672 H2833 H2856 H2905 H2963 H3003 H3021 H3147 H3276 H3323 H3390 H3474 H3489 H3518 H3547 H3569 H3595 H3708 H3805 H3867 H3923 H4046 H4334 H4350 H4406 H4410 H4522 H4539 H4599 H4601 H4641 H4692 H4744 H4775 H4805 H4888 H4918 H5006 H5028 H5034 H5065 H5071 H5110 H5137 H5145 H5258 H5397 H5404 H5410 H5526 H5591 H5688 H5699 H5713 H5774 H5787 H5794 H5833 H5850 H5949 H6214 H6223 H6227 H6342 H6372 H6403 H6412 H6456 H6490 H6504 H6510 H6522 H6532 H6597 H6672 H6685 H6810 H6870 H6923 H7270 H7287 H7326 H7337 H7605 H7614 H7699 H7701 H7761 H7810 H7837 H7845 H7860 H8025 H8032 H8446 H8467 H8559
- 4. (45): H0348 H0378 H0665 H1124 H1339 H1438 H1639 H1881 H1932 H1969 H2094 H2195 H2438 H2493 H2658 H2964 H3584 H3760 H3863 H3996 H4289 H4353 H4496 H4591 H4929 H4962 H5022 H5037 H5275 H5310 H5347 H5619 H5633 H5747 H5830 H6035 H6138 H6148 H6297 H7921 H7941 H8142 H8444 H8486 H8537

*(proveniencia: scope=adat/bdb_szakaszok.tsv (`szoveg` oszlop, 11. mező), `eszkozok/bdb_jelolt/szakasz_bemenet.py` `szakaszok()`/`nezet()` | forras=saját szkript (`split('\t')`, `len()` karakterekben, Strong-halmaz a 2. szakasz szerint) | ts=2026-10-26T13:32Z)*

## 4. A kapu-felülbírálások (DT361) tételesen

A felülbírálás a Strong minden szakaszsorának `megjegyzes`-ében jelölt. A kilenc tétel: nyolc a szeleteknél, a kilencedik (H2574) a javítókörben került rá (ELLENOR_F38_adag8 2.).

| # | Strong, szakasz | kapu | forrásidézet | fordítás |
|---|---|---|---|---|
| 1 | H5126 sz2 | 11_konyvek | „or Non נוּן and (1Chr 7:27) נוֺן proper name, masculine father of Joshua 7:27” | a „Joshua” személynév, a 7:27 az 1Krón 7:27 visszautalása |
| 2 | H1826 sz2 | 9_tagolas | „Ethiopic in II. stupefy; III., 1 & 2 be astounded” | „etióp II.-ben elbódít; III., 1 és 2 elképed” (igetörzs, nem tagolójel) |
| 3 | H7621 sz2 | 5_terminologia (`cl.`→klasszikus) | „(in rel.cl.) 5t.” | „(vonatkozó mondatban)”; a `cl.` = clause |
| 4 | H6903 sz14 | 5_terminologia (`see`→`l.`) | „because ye see” | „mivel látjátok” (ige, nem utalás) |
| 5 | H1032 sz8 | 8_idezojel | „modern Beit „anûn” | a „ (U+201E) OCR-maradvány megtartva |
| 6 | H6346 | 5_terminologia (`see`→`l.`) | „(strike out see, Sta and others)” | szövegkritikai utasítás, nem utalás |
| 7 | H7797 | 5_terminologia (`Heb.`→`héb.`) | „Da Toy^Heb.Hpt” | irodalmi szigla |
| 8 | H1969 sz2 | 5_terminologia (`accusative`→`tárgyeset`) | „= sextarius, accusative to Böckh^Metrol. Unters. 244” | „Böckh … szerint”; forráshiba (`accusative to` = acc. to), a fordítás a szándékolt olvasatot adja (DT362 (1); a `megjegyzes` jelzi) |
| 9 | H2574 sz2 | 8_idezojel | „„amaâ” (U+201E) | a „ (U+201E) jel vissza (előtte tévesen ‚ U+201A), csak ez a jel változott |

## 5. A javítókör módosításai

- 1.: H1969, a 8 sor `megjegyzes`-e kiegészült: „; forráshiba: „accusative to” = acc. to (according to); a fordítás a szándékolt olvasatot adja (DT362 (1))”. A szöveg nem változott.
- 2.: H2574 sz2 „mai ‚amaâ” → „mai „amaâ”; a két H2574-sor `megjegyzes`-ébe „kapu-felülbírálás: 8_idezojel (DT361)”.
- 6.: H7621 sz4 „eskü ... (׳י)” → „eskü -hoz -hoz (׳י)”, „az esküt” → „az eskü van”; H7621 sz6 „megteltél nyilakkal tegzed” → „nyilakkal töltötted meg tegzedet”; H1032 sz2 „vö.” → „vö. még”; H1032 sz4 „1 órányira nyugatra” → „1 órányira nyugatra -tól”.
- 7.: `DONTESEK.md` DT361: „(DT-F38o)” → „(DT339)”.
- A `naplok/EMELES_munka.tsv` megfelelő sorai ugyanígy módosultak (munkatábla; a forditasok.tsv-vel azonos tartalom).
- Nyitott: a 4. (hatókör) tétel — a H6297 a 9. adaghoz tartozik; a #67 kapuját elkészültekor rá is le kell futtatni (DT362 (5)).

## 6. A 2. javítókör (`naplok/ELLENOR_F38_adag8_2.md`, DT363; `54a1cd5a`, F38.398)

**Módszer.** Az 1. kör 14 kézzel cserélt cellája (H1969 sz1–8, H2574 sz1–2, H7621 sz4 és sz6, H1032 sz2 és sz4) újra rögzült az eszközláncon: a négy Strong tokenes szövege (a jelenlegi `forditasok.tsv`-sorokból, a kétféle tartalmi javítással) → `szakasz_ellenoriz` → `szakasz_rogzit` → `szakasz_beir --regi-elavult`. Kézi cellacsere nincs. A `datum` (2026.10.26) és a `modell` változatlan. A rögzítés a Strong minden szakaszsorát újraírja, ezért a `megjegyzes` a Strong mind a 24 során egységes (az eszköz csak Strong-szintű `--megjegyzes`-t tud); a `forditas_hu` az alábbi kettő kivételével bájtra változatlan.

**Kapu-felülbírálások** (mindegyiknél pontosan egy kapu bukott, a többi átment; `--kapu-felulir <kapu> --dontes DT361`):

| Strong | bukott kapu | forrásidézet | hű fordítás |
|---|---|---|---|
| H1969 | 5_terminologia (`accusative`→`tárgyeset`) | „= sextarius, accusative to Böckh^Metrol. Unters. 244” (sz2) | „Böckh … 244 szerint”; forráshiba, `megjegyzes` jelzi (DT362 (1)) |
| H2574 | 8_idezojel (forrás 0, fordítás 1 jelpár) | „modern „amaâ, on el-±A±ƒi” (sz2) | a „ (U+201E) OCR-maradvány megtartva |
| H7621 | 5_terminologia (`cl.`→`klasszikus`) | „(in rel.cl.) 5t.” (sz2) | „(vonatkozó mondatban)”; a `cl.` = clause |
| H1032 | 8_idezojel (forrás 0, fordítás 1 jelpár) | „modern Beit „anûn compare” (sz8) | a „ (U+201E) OCR-maradvány megtartva |

**Tartalmi változás** (a `forditas_hu`-ban, két cella):

- H7621 sz4, 1.: „megtartja, teljesíti az eskü van הַשּׁ ׳הֵקִים” → „megtartani, teljesíteni az esküt: הַשּׁ ׳הֵקִים” (forrás: „keep, discharge the oath is הַשּׁ ׳הֵקִים Gen 26:3 (J)”; az „is” kopula).
- H7621 sz4, 2.: „eskü -hoz -hoz (׳י)” → „a ׳י-nak tett eskü” (forrás: „oath to to (׳י)”; DT363 (1)(a)).
- H1032 sz4: a szöveg („b. 1 órányira nyugatra -tól”) változatlan; a `megjegyzes`-ben „forráshiba: csonka szakasz („from” tárgy nélkül)” (DT363 (2)).

**Megjegyzések a rögzítés után** (a Strong minden során): H1969: „forráshiba: „accusative to” … (DT362 (1)); kapu-felülbírálás: 5_terminologia (DT361)” (a sorrend az eszközé: előbb a forráshiba, utána a felülbírálás); H2574: „kapu-felülbírálás: 8_idezojel (DT361)”; H7621: „forráshiba: „to to” ismétlés; kapu-felülbírálás: 5_terminologia (DT361)”; H1032: „forráshiba: csonka szakasz („from” tárgy nélkül); kapu-felülbírálás: 8_idezojel (DT361)”. A „to to” és a csonka szakasz jelölése így a Strong többi során is áll, ahol nem releváns.

**Δ.** `git diff --numstat 54a1cd5a^ 54a1cd5a`: `adat/forditasok.tsv` 22 / 22 (a H2574 két sora bájtra azonos), `naplok/EMELES_munka.tsv` 24 / 24; sor hozzáadva vagy törölve: 0. Más tábla nem változott.

*(proveniencia: scope=adat/forditasok.tsv, naplok/EMELES_munka.tsv @ 54a1cd5a^ és @ 54a1cd5a; adat/bdb_szakaszok.tsv | forras=`emeles.py szakasz_ellenoriz/szakasz_rogzit/szakasz_beir`; `git diff --numstat`; a forrásidézetek az `adat/bdb_szakaszok.tsv` `szoveg` oszlopából | ts=2026-10-28)*
