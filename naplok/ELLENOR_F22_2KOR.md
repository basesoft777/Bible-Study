# ELLENOR_F22_2KOR — F22_KAROLI_STRONG_BRIEF.md (22.9, D45, D43–D44), `7127e283..ab0240a` (ág: claude/f22-2kor)

*A független ellenőr (`fuggetlen-ellenor`) jelentése. A subagent a jelentésfájlt nem tudta kiírni (nincs Write eszköze), ezért a végrehajtó session mentette el a repóba, tartalmilag változtatás nélkül; az alábbi szöveg az ellenőr visszaadott jelentése. A javítókör és az újraellenőrzés: `naplok/ELLENOR_F22_2KOR_2.md` (ha készül).*

**Eredmény: ELTÉRÉS: 8 tétel**

**Modell-ellenőrzés:** a tényleges modell `claude-opus-5-5`, a kért modell `opus`, tehát egyezik. A menet `modell` mezői mind `claude-sonnet-5-5` értéket mutatnak (`f22/api_termeles/futasnaplo.tsv`, 41 új sor), és ez egyezik a brief `modell: sonnet` mezőjével és a commitok `Co-Authored-By: Claude Sonnet 5.5` sorával. Hogy a végrehajtó session valóban Sonnet volt-e, azt lekérdezéssel nem tudja igazolni.

**Tanulmány-ellenőrzés (F37 T4):** nem él, mert a diff nem hoz `*_bovitett.md` / `*_tanulmany.md` fájlt.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | `f22/api_termeles/futasnaplo.tsv:1869–1909` | 41 sor, `modell=claude-sonnet-5-5`, `prompt_sha256_12=84f12ca7aafb` mindenhol |
| 1. állítás: 2Kor 256 vers, 26 köteg | OK | `f22/minta_2Kor.tsv`, futásnapló | `Karoli_1908.tsv`-ben `^2Kor \d+:\d+\t`: 256. 26 köteg, igehely 25×10 + 6 = 256. Batch `msgbatch_01B2fhTDU7FZsH4GrHsvhQGr`, 26 kérés |
| 1. állítás: kapuhiba 0 | OK | futásnapló | mind a 26 sorban `kapuhiba_db=0`, `ok=igen` |
| 1. állítás: 4352 link, mind alacsony/S | OK | `adat/karoli_strong/parok_2Kor.tsv` | `\talacsony\tS$` = 4352 |
| 1. állítás: 9064 = 4517 + 4547 | OK | `szavak_2Kor.tsv` | `\thu\t` = 4517, `\ter\t` = 4547; TAGNT_kivonat `^2Kor ` = 4547 |
| 1. állítás: összetétel 3748/769/0 és 3902/0/645 | OK | `szavak_2Kor.tsv` | hu parositva 3748, hu betoldas 769, er parositva 3902, er forditatlan 645 |
| 1. állítás: költség 1,36 USD, tokenösszeg | OK | futásnapló | 95,864905 − 94,504948 = 1,359957 USD; bemenet 250 872, kimenet 221 817 token |
| 1. állítás: K1 (minden token egyszer) | NEM ELLENŐRIZHETŐ (részben OK) | `szavak_2Kor.tsv` | az er-oldal darabszáma egyezik a TAGNT-vel; a Károli-oldal duplikációmentességét a megengedett parancsokkal nem tudta összegezni. Szúrópróba (2Kor 13:13, 8:13–14, 5:12) rendben |
| 1. állítás: K2 (Strong a TAGNT-ből) | NEM ELLENŐRIZHETŐ (szúrópróba OK) | `parok_2Kor.tsv` | nincs nem `G\d{4}` Strong; a szúrópróba pozíciója és Strongja a TAGNT-tel egyezik |
| 1. állítás: 2Kor 13:13 #22–33 TR-utóirat, fordítatlan | OK | `szavak_2Kor.tsv:9055–9066` | 12 sor, mind `forditatlan`; a Károliban nincs utóirat |
| 2. állítás: VERSBEOSZTAS_JOVAHAGYOTT + napló | OK / NEM ELLENŐRIZHETŐ | `eszkozok/karoli_strong/tokenek.py:56`, `naplok/F22_versbeosztas_jovahagyas.md:64` | a `'2Kor'` hozzáadva, a naplósor megvan, a batch előtt. A chates „mehet” nem ellenőrizhető |
| **2Kor 8:13/8:14 vershatár** | **ELTÉRÉS** | `szavak_2Kor.tsv:5071–5079, 5103–5113`; `naplok/F22_versbeosztas_jovahagyas.md:64` | A Károli 8:13 „… e mostani időben a ti bőségtek pótolja amazoknak fogyatkozását” a TAGNT 2Kor 8:14 1–11. tokenje („ἐν τῷ νῦν καιρῷ τὸ ὑμῶν περίσσευμα εἰς τὸ ἐκείνων ὑστέρημα”). Következmény: 9 Károli-szó hamisan `betoldas` (8:13 hu 14–22), 11 eredeti token hamisan `forditatlan` (8:14 er 1–11). A jóváhagyási sor és a jelentés „nincs … kézi leképezés”, a 8. fejezet jelzése „nem eltolódás” állítását ez cáfolja |
| 3. állítás: csak a 36 vers változott | OK | 11 könyv `parok_`/`szavak_` | az összes ± adatsor 3087, a 36 vers mintájára illeszkedő ± sor szintén 3087; a 36 versen kívül 0 sor változott |
| 3. állítás: törölt sorok csak függőben-sorok | OK | ugyanott | törölt `parositva/betoldas/forditatlan` = 0; hozzáadott `fuggoben/kezi` = 0 |
| 3. állítás: kezi_versek 33 sor + 3 vers | OK | `f22/kezi_versek_*.tsv` | törlések 2+2+6+1+2+6+2+2+4+6 = 33; a 3Ján 1:15 és a Fil 1:16–17 korábban `nincs_eredeti` sor volt, nem kényszer. Az átnézési listákból 36 sor tűnt el |
| 3. állítás: nincs függőben a 36 versben | OK | `szavak_*.tsv` | `fuggoben/kezi` az ÚSZ-ben csak `szavak_Gal.tsv` 28 sor, mind Gal 3:23 (nem célvers) |
| 3. állítás: K1 a 3 korábban eredeti nélküli versben | OK | `szavak_3Jan.tsv`, `szavak_Fil.tsv` | TAGNT 37 sor = szavak er-sorai 11 + 26; 1Tim 6:21: 24 = 24 |
| 3. állítás: a 15 kényszerkivezetett vers eredetije változatlan | OK (szúrópróba) | 1Thessz 1:2 | a 14 er-token alakja és Strongja azonos, csak az állapot változott |
| 3. állítás: a napló 6. táblájának párszámai | OK | `naplok/F22_N-F22c_ujraparositas.md:62–97` | könyvenkénti párösszeg = a parok-Δ (3Ján 9, 1Tim 10, 2Thessz 39, 1Thessz 101, Kol 57, Fil 47, 1Pét 46, 1Ján 53, Gal 44, Ef 109, Zsid 102) |
| 4. állítás: [nem TR] 103, ebből 5 párosított | OK | `adat/karoli_strong/nem_tr_parositott.tsv` | TAGNT TR = 4444, 4547 − 4444 = 103; az 5 sor pozíciója és Strongja egyezik; a tábla 45 sora |
| 5. állítás: futó összeg, N-F22c 15 hívás | OK | futásnapló | utolsó sor 96,053973; N-F22c: 0,189068; 15 sor |
| 5. állítás: plafon, újravetítés | OK | `api_koteg.py:54, 61, 116–118, 258–264`; `naplok/F22_2Kor_jelentes.md:48–57` | PLAFON 104,36, maradék 8,306. Egységár 0,005238; C: 1272 vers (Róm 431 + 1Kor 436 + Jel 405), ×0,005238 = 6,66, ×1,2 = 7,995. Felső becslés 0,16 USD/kérés; 2Kor-ra 4,41 |
| 5. állítás: DT262 szám | **ELTÉRÉS** (alacsony) | `DONTESEK.md:324` | 7,996 USD szerepel, a helyes érték 7,995 (6,662736 × 1,2 = 7,99528) |
| **5. állítás / D45: DT262 opciói** | **ELTÉRÉS** | `DONTESEK.md:324`; `naplok/F22_2Kor_jelentes.md:57` | A „c” opció (Róm + 1Kor) a jelenlegi őr mellett sem futtatható (a Róm után kb. 98,3 + 7,1 > 104,36, az 1Kor beküldését az őr elutasítja). A „c vagy b” javaslat félrevezető. A D45 szerint a ×1,2-es belefér-feltétel teljesül, tehát a C-nek egészben kellene indulnia; a „c” a D45-ben a nem-fér-bele ág |
| 5. állítás: DT262 helyőrző | OK | `DONTESEK.md:324` | E26 = 0 találat; `DT262` egyedi, végleges DT-szám nincs |
| 6. állítás: FELADATOK.md generált blokkja | OK | — | a `FELADATOK.md` nem szerepel a diffben |
| 6. állítás: GENERÁLT fájl kézzel | OK / NEM ELLENŐRIZHETŐ | `nem_tr_parositott.tsv:1`, `f22/versmegfeleltetes.tsv:1` | fejléc és tartalom konzisztens a TAGNT-tel; hogy szkript írta-e, futtatás nélkül nem igazolható |
| 6. állítás: proveniencia (táblafejlécek) | **ELTÉRÉS** (alacsony) | 11 könyv `parok_*.tsv:1`, `szavak_*.tsv:1` | a `forras` nem létező fájlt nevez meg: `f22/valaszok/c/<könyv>_javito.jsonl`; a `f22/valaszok/c/*_javito*` közül csak `2Moz_javito.jsonl` létezik |
| 6. állítás: proveniencia (naplók) | **ELTÉRÉS** (alacsony) | `naplok/F22_2Kor_jelentes.md:3`, `naplok/F22_N-F22c_ujraparositas.md:3` | a lekérdezésből származó számok mellett csak szkriptnév áll; nincs `scope=… \| forras=… \| ts=…` sor (CLAUDE.md 1. szabály) |
| 6. állítás: commit-üzenetek | OK | `git log 7127e283..ab0240a` | mind magyar, `F22.<n>` előtaggal (F22.10 … F22.21). E30 jelzés: „kezi” a cf5d43c-ben (technikai állapotnév). A b4464a8-ban nincs Co-Authored trailer |
| G: 22.9/2 soros futás (D15, DT60) | OK | `batchek.tsv:93–108` | a batch-időbélyegek sorosak, átfedés nincs |
| G: 22.9/3 jelentés, nem_tr_lista | OK | — | `F22_2Kor_jelentes.md` és `nem_tr_parositott.tsv` frissült; a B-összesítő nem, helyette a 2Kor-jelentés „B csomag zárása” szakasza áll (tűrhető) |
| G: 22.9 kész-ha (plafon alatt, újravetítés) | OK | — | 96,05 < 104,36; az újravetítés a 4. szakaszban |
| **D45 / brief-fejléc** | **ELTÉRÉS** | `F22_KAROLI_STRONG_BRIEF.md:11, 180, 195`; D45 sor (266) | a fejléc `kovetkezo` mezője az F22.10.3 állapotát írja; a DT262, az ellenőr és a PR nem szerepel; a Döntésnapló nem kapta meg a 2Kor / N-F22c eredményt; a 22.9 szövege szerint a 2Kor 13:13 „nincs görög szövege”, ami elavult |
| A1 memória vs. lekérdezés | OK | `F22_2Kor_jelentes.md:31` | a TR-utóirat állítást a TAGNT igazolja (12 TR-only sor) |
| **A2 nyitott tételek** | **ELTÉRÉS** | `NYITOTT_FELADATOK.md:109–110` | az N-F22c (3) és az N-F22d („Nyitva marad: a Fil 1:16–17 újrapárosítása”) ezen az ágon elkészült (Fil 1:16–17: 11+11 pár), a `NYITOTT_FELADATOK.md` mégsem frissült |
| A3, A4, A5 | nem értelmezett | — | nincs tanulmány, tematikus párhuzam, PaRDeS-réteg vagy nevesített tanító a diffben |
| A6 E12–E15 | OK | — | `futtat.py`: E12–E15 0 találat |
| CI (3.) | NEM ELLENŐRIZHETŐ | — | saját futtatás: exit 1. E27 HIBA 1 (`FELADATOK.md:56`, `1f420a7c`), E28 HIBA 5 (`motivumlog/PaRDeS_motivumok.md:36, 494`, `Lezart_tematikus_tanulmanyok_index.md:24` …; `elofordulasok.tsv` 259 vs. 260), E25 4 jelentés, E30 1 figyelmeztetés. A HIBÁ-k egyike sem a diff fájljaiban van; hogy az alapon is fennállnak-e, azt nem tudta futtatni |
| Lista 1: törölt sorok | OK | — | 11 könyv szavak: −1186 sor, mind `fuggoben`/`kezi` (36 vers). parok: −11 (proveniencia-fejléc). kezi_versek: −33. Átnézési listák: −36. versmegfeleltetes: −8 `nincs_eredeti` sor (mind megvan a TAGNT-ben) |
| Lista 2: kulcslefedettség | OK | — | 2Kor: 256/256 vers (Károli = minta = TAGNT-kulcs) |
| Lista 3: „nulla-diff” hatóköre | OK | — | a „csak a 36 vers változott” a 11 könyv adatsoraira vonatkozik; nem vonatkozik a proveniencia-fejlécre, a 2Kor-ra (új tábla) és a `nem_tr_parositott.tsv`-re (+6) |
| Lista 4: sorszám-Δ (E17/DT3) | **ELTÉRÉS** (alacsony) | `naplok/F22_N-F22c_ujraparositas.md:54` | a parok-Δ-t a napló 6. táblája bontja, a 2Kor-t a jelentés; a szavak-táblák ≥10-es Δ-ját (1Thessz +14, 1Tim +17, 3Ján +11, Ef +14, Fil +31, Zsid +11: az F90 új er-tokenjei) a napló nem bontja. Az E17 a `futtat.py`-ban nincs megvalósítva |
| Lista 5: ⛔ pontok | OK | — | a versbeosztás-jóváhagyás megelőzte a bővítést és a batch-et; a C nem indult; párhuzamos futás nem volt; megállás ellenőrre és PR-re |

**Az ELTÉRÉS-ek súlyossági sorrendben**

1. A DT262 opciói (`DONTESEK.md:324`): a javasolt „c” a saját plafon-őr-elemzés szerint nem futtatható, és ellentmond a D45 belefér-ágának.
2. A 2Kor 8:13/8:14 részleges vershatár-eltérése (`szavak_2Kor.tsv:5071–5079, 5103–5113`): 9 Károli-szó hamis `betoldas`, 11 görög token hamis `forditatlan`, és a jóváhagyási napló „nincs kézi leképezés” állítása ezt nem fedi.
3. A2: az N-F22c (3) és az N-F22d a `NYITOTT_FELADATOK.md:109–110`-ben nyitottként áll, pedig elkészült.
4. A brief fejléce, Döntésnaplója és 22.9-szövege elavult (`F22_KAROLI_STRONG_BRIEF.md:11, 180, 195, 266`).
5. E17/DT3: a szavak-táblák ≥10-es Δ-jához nincs bontás.
6. A táblafejlécek proveniencia-`forras` mezője nem létező `f22/valaszok/c/*_javito.jsonl` fájlt nevez meg.
7. A naplókból hiányzik a `scope | forras | ts` proveniencia-sor.
8. Kerekítési hiba: a DT262 7,996 USD-t ír 7,995 helyett.
