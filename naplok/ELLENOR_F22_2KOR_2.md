# ELLENOR_F22_2KOR_2 — újraellenőrzés, 1. kör

F22_KAROLI_STRONG_BRIEF.md (22.9, D45), `ab0240a..79cde01` (javítókör: `29f1dab..79cde01`; ág: claude/f22-2kor)

*A független ellenőr (`fuggetlen-ellenor`) jelentése. A subagent a jelentésfájlt nem tudta kiírni (nincs Write eszköze), ezért a végrehajtó session mentette a repóba; a táblázat sorai az ellenőr visszaadott szövegéből valók, a hosszú parancs-/idézetcellák rövidítve, a számok és az eredmények változatlanok. A javítókör az ellenőr 3 tételére: `F22.27` (l. lent „Javítás”).*

**Eredmény: ELTÉRÉS: 3 tétel** (az 1. kör 8 tételéből 7 megszűnt; a 4. tétel részben megmaradt, a 8. új alakban jelentkezik)

**Modell-ellenőrzés.** A tényleges modell `claude-opus-5-5`, a kért modell `opus`, egyezik. A javítókör nem írt új `modell` mezőt (`f22/api_termeles/futasnaplo.tsv` nem változott). Mind az öt commit `Co-Authored-By: Claude Sonnet 5.5`, egyezik a brief `modell: sonnet` mezőjével. Hogy a session valóban Sonnet volt-e, lekérdezéssel nem igazolható.

**Tanulmány-ellenőrzés (F37 T4):** nem alkalmazható (nincs `*_bovitett.md` / `*_tanulmany.md` a diffben).

**Eljárási közlés.** Az ellenőr három parancsban a `git diff` kimenetét `grep`/`awk`/`sort`/`uniq`/`cut`/`head`/`tail` csővel szűrte (csak olvasás, fájlt nem írt). Az `egyesit.py --onteszt` és a `feladatok.py ellenoriz` nincs a megengedett körében, ezért nem futtatta.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 1. DT262 opciók, javaslat | OK | `DONTESEK.md:324` | egyetlen sor; az „a” kimondja a D45 belefér-ágat; a „c” a D45 nem-fér-bele ága, „önmagában nem futtatható”; a javaslat „a (vagy b)”; végleges DT-szám nincs (E26 = 0) |
| 1. DT262 kerekítés | OK | `DONTESEK.md:324` | 7,995 USD; (0,005226×1638+1,36)/1894 = 0,0052377; ×1272 = 6,6627; ×1,2 = 7,99528; Róm+1Kor 867 vers: 4,54 / 5,45 USD |
| 2. `kezi_versek_2Kor.tsv` | OK | `f22/kezi_versek_2Kor.tsv:3–5` | új fájl, fejléc `igehely ok`, két sor (2Kor 8:13, 8:14) |
| 2. szavak: a két vers `fuggoben`/`kezi` | OK | `szavak_2Kor.tsv:5058–5126` | 69 sor, mind `fuggoben … kezi`; más versben nincs `fuggoben` |
| 2. parok: nincs link a két versben | OK | `parok_2Kor.tsv` | 0 sor; a javítókör 22 törölt sora mind 8:13/8:14 |
| 2. nulla-diff a két versen kívül | OK | `szavak_2Kor.tsv`, `parok_2Kor.tsv` | 69−/69+, minden ± sor 8:13 vagy 8:14 (törölt: 8:13 22 parositva + 11 betoldas, 8:14 21 parositva + 2 betoldas + 13 forditatlan; hozzáadott: 33 + 36 `fuggoben/kezi`); a fejléc nem változott |
| 2. K1 a két versben | OK | `TAGNT_kivonat.tsv:102784–102818`; `Karoli_1908.tsv:29002–29003` | 8:13: hu 1–22, er 1–11; 8:14: hu 1–12, er 1–24; a TAGNT 11 + 24 tokenje sorrendben és Strongban azonos |
| 2. helyesbítő sor | OK | `naplok/F22_versbeosztas_jovahagyas.md:65` | „2Kor 8:13–14 (helyesbítés a 64. sorra)”, 9 / 11 számmal, N-F22e |
| 3. N-F22c, N-F22d lezárva | OK | `NYITOTT_FELADATOK.md:109, 110` | „LEZÁRVA” szöveg mindkettőben |
| 3. N-F22e helyőrző | OK | `NYITOTT_FELADATOK.md:111` | végleges `N<n>` szám nincs; a 69 szósor egyezik |
| 4. brief fejléc `kovetkezo` | OK (részben NEM ELLENŐRIZHETŐ) | `F22_KAROLI_STRONG_BRIEF.md:11` | DT262, a C jóváhagyása, 96,0540 USD, N-F22e; a „draft PR #433” `gh` nélkül nem ellenőrizhető |
| **4. 22.9 C-sor és a hiányzó görög szöveg listája** | **ELTÉRÉS** | `F22_KAROLI_STRONG_BRIEF.md:182, 195` | a brief szerint a Róm 16:25–27 és a Jel 12:18 „nincs görög szövegük”, `fuggoben` maradna; a `TAGNT_kivonat.tsv`-ben az F90 óta megvan (73 sor; Róm 16:27: 26). `lekerdez.py scan G1391 --szakasz "Róm 16:25-27"` → Róm 16:27 (`scope=range:Róm 16:25-27 \| forras=TAGNT_kivonat.tsv \| strong=G1391 \| n=1 \| ts=2026-10-19T16:06Z`); `scan G2476 --szakasz "Jel 12:18"` → Jel 12:18 (`… n=1 \| ts=2026-10-19T16:06Z`). A javítás csak a Fil és a 2Kor állítását írta át. A C tervét érinti |
| **4. brief `ir` mező** | **ELTÉRÉS** (alacsony) | `F22_KAROLI_STRONG_BRIEF.md:15` | `kezi_versek_2Kor` 0 találat; az új fájl nincs az `ir` listában |
| 4. D45 eredmény | OK (megjegyzéssel) | `F22_KAROLI_STRONG_BRIEF.md:266` | 2Kor 256 vers, 1,36 USD, N-F22c 36 vers, 0,1891 USD, 96,0540 / 8,31 / 7,995, DT262; a bejegyzés a sor utolsó cellájában áll, nem a döntés-cellában, mint az A és B eredménye |
| 4. v2.45 sor | OK | `F22_KAROLI_STRONG_BRIEF.md` (Döntésnapló) | új sor, 2026.10.19, csökkenő sorrend |
| 4. `feladatok.py ellenoriz` | NEM ELLENŐRIZHETŐ | — | a megengedett körön kívül; `futtat.py` E18, E26: 0 |
| 5. N-F22c napló 7. szakasz Δ | OK | `naplok/F22_N-F22c_ujraparositas.md:105–120` | parok +617, szavak +120, könyvenként egyezik a `git diff --numstat 9f4fc06..c0d1070`-nel; Gal szúrópróba: 2:19 er 9→9 (Δ0), 2:20 er 33→35 (+2) |
| 6. táblafejléc `forras` | OK | 11 könyv + 2Kor `parok_/szavak_*.tsv:1` | minden megnevezett `sonnet/<k>.jsonl` és `sonnet/<k>_javito.jsonl` létezik; `c/*_javito` sehol sem szerepel |
| 6. a 11 könyvben csak az első sor változott | OK | ugyanott | a 11 könyv 22 táblája 1/1, csak a `f22/valaszok/c/<k>_javito.jsonl,` tűnt el |
| 6. `egyesit.py` változtatás | OK (kódolvasás) | `eszkozok/karoli_strong/egyesit.py:328–329` | csak a létező javító-fájlt nevezi meg; a 2Móz kimenete nem változik; `egyesit.py --onteszt` nem ellenőrizhető |
| 7. proveniencia-sor a naplókban | OK | `naplok/F22_2Kor_jelentes.md:5`; `naplok/F22_N-F22c_ujraparositas.md:3` | mindkettőben `scope=… \| forras=… \| ts=2026-10-19` |
| 8. 2Kor-jelentés új számai | OK | `naplok/F22_2Kor_jelentes.md:22–29` | parok_2Kor 4332 = 2 fejlécsor + 4330; hu 3727 + 756 + 34 = 4517; er 3880 + 632 + 35 = 4547; `fuggoben` 34 + 35 = 69 |
| **8. 4. szakasz aritmetikája** | **ELTÉRÉS** (alacsony) | `naplok/F22_2Kor_jelentes.md:61, 62` | a táblázat helyes (7.995); a :61 „7.99 USD ≤ 8.31 USD” helyesen 7,995 (két tizedesre 8,00); a :62 „a Róm után kb. 98.4 USD” a mért egységárral 96,054 + 431×0,005238 = 98,31; a következtetést egyik sem dönti meg |
| Regresszió: a 36 vers nulla-diffje | OK | 11 könyv | `git diff --numstat c0d1070..HEAD`: a 11 könyv mind 1/1; a ± sorok száma a 2Kor nélkül 44 = 22 tábla × 2 (csak a proveniencia-sor) |
| Regresszió: FELADATOK.md | OK | — | a `69f6a67..HEAD` és az `origin/main...HEAD` szerint változatlan |
| Regresszió: commit-üzenetek | OK | `git log ab0240a..HEAD --first-parent` | F22.22–F22.26, magyarul, `F22.<n>` előtaggal; E30: 1 FIGYELMEZTETÉS (`3f8b959`: „kezi”, technikai állapotnév) |
| Regresszió: a C nem indult | OK | — | `git log 69f6a67..HEAD -- f22/api_termeles/ f22/valaszok/ eszkozok/karoli_strong/api_koteg.py` üres |
| A1 | OK | `F22_2Kor_jelentes.md:31, 35` | az állítások a táblákból és a TAGNT-ből igazolódnak |
| A2 | OK (megjegyzéssel) | `NYITOTT_FELADATOK.md:109–111` | az N-F22c(3), N-F22d kész, az N-F22e nyitott; megjegyzés: a `:3` „Utolsó frissítés” sora nem frissült |
| A3, A4, A5 | nem értelmezett | — | nincs tanulmány, PaRDeS-réteg vagy tanító a diffben |
| A6 / CI (3.) | OK | — | `futtat.py` a változott fájlokra: exit 1; E2–E16, E19, E20, E26, E28, E29, E31: 0; E12–E15: 0; E25 4 JELENTÉS; E27 HIBA 1: `FELADATOK.md:56`, `1f420a7c` (F52-brief generált blokkja, nem a diff fájlja); E30 1 FIGYELMEZTETÉS; az első kör E28-hibái a main-beolvasztással megszűntek |
| Lista 1: törölt sorok | OK | — | javítókör: parok_2Kor −22 link; szavak_2Kor 69 sor állapotcserével; a 11 könyv 22 táblájában csak az első sor cserélődött |
| Lista 2: kulcslefedettség | OK | — | 2Kor 256/256 vers; link 254 versben, a két `kezi` versben szándékosan nincs |
| Lista 3: a nulla-diff hatóköre | OK | — | a 11 könyv adatsoraira és a 2Kor 254 versére; nem vonatkozik a 22 + 2 proveniencia-fejlécre és a 2Kor 8:13–14-re |
| Lista 4: sorszám-Δ a main-hez (E17/DT3) | OK | `F22_N-F22c_ujraparositas.md` 6–7.; `F22_2Kor_jelentes.md` 2. | nem_tr_parositott +6; parok 1Jan +53, 1Pet +46, 1Thessz +101, 1Tim +10, 2Kor új 4330, 2Thessz +39, 3Jan +9, Ef +109, Fil +47, Gal +44, Kol +57, Zsid +102; szavak 1Jan +7, 1Pet +5, 1Thessz +14, 1Tim +17, 2Kor új 9064, 2Thessz +3, 3Jan +11, Ef +14, Fil +31, Gal +2, Kol +5, Zsid +11; minden ≥10-es Δ-ra van bontás |
| Lista 5: ⛔ pontok | OK | — | a C nem indult; a Károli-összevonás három sora nem került be; megállás ellenőrre |

**Az ELTÉRÉS-ek súlyossági sorrendben**

1. A brief 22.9 C-sora (`:182`) és a „Hiányzó görög szöveg” pont (`:195`): a Róm 16:25–27 és a Jel 12:18 az F90 óta megvan (73 sor), az állítás elavult. A C tervét érinti.
2. `F22_2Kor_jelentes.md:61–62`: „7.99 USD” → 7,995; „kb. 98.4 USD” → 98,31.
3. A brief `ir` mezőjéből hiányzik az `f22/kezi_versek_2Kor.tsv`.

**Megjegyzések (nem eltérések):**
- A táblafejlécek `forras` mezője a `f22/kezi_versek_<könyv>.tsv`-t sehol nem nevezi meg, pedig a 2Kor 8:13–14 állapotát ez a fájl határozza meg. Ez az `egyesit.py` korábbi viselkedése, a javítókör nem okozta.
- A `NYITOTT_FELADATOK.md` „Utolsó frissítés” sora nem frissült.
- A D45 EREDMÉNY bejegyzése más cellában áll, mint az A és B eredménye.

## Javítás (F22.27, 2026.10.19)

1. A brief 22.9 C-sora és a „Hiányzó görög szöveg” pont átírva: a Róm 16:25–27 és a Jel 12:18 görög szövege az F90 óta megvan; új előírás: a C versbeosztás-jóváhagyása tokenszintű vershatár-vizsgálatot is kér (GYENGE fejezetek; N-F22e).
2. A 2Kor-jelentés 4. szakasza: 7,995 USD ≤ 8,306 USD (különbség 0,311 USD); a Róm után kb. 98.3 USD.
3. A brief `ir` mezője kibővítve (`f22/kezi_versek_2Kor.tsv`, `naplok/ELLENOR_F22_2KOR.md`, `naplok/ELLENOR_F22_2KOR_2.md`).
4. A megjegyzések közül a `NYITOTT_FELADATOK.md` „Utolsó frissítés” sora frissítve; a másik kettő nem eltérés (a `forras` mező `kezi_versek` említése az `egyesit.py` külön fejlesztése; a D45 bejegyzés cellája formai).

Következő lépés: 2. újraellenőrzés (az `elteres` szabály szerint legfeljebb 2).
