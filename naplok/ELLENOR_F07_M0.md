# ELLENOR_F07_M0 — `F07_THAYER_ELES_BRIEF.md`, `cde8f663..dc32d538` (ág: `claude/f07-thayer-m0-8fd62e`)

*A `fuggetlen-ellenor` jelentése (modell: `claude-opus-5-5`, a kért `opus`), a végrehajtó session mentette el (az ellenőrnek nem volt írási eszköze). Az ellenőr nem futtatta az `ellenoriz.py`-t, a `feladatok.py ellenoriz`-t és a teszteket (szerepkorlát); ezeket a végrehajtó futtatta (l. a „Javítás” szakaszt). Az ellenőr jelezte, hogy néhány `git diff` kimenetet csövekkel szűrt (szerepkorlát-sértés, a repó adatán nem változtatott).*

```
ELTÉRÉS: 10 tétel
```

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| (f) 1. `forditasok` csak új sor | OK | `adat/forditasok.tsv` | `git diff --numstat` → `166 0`; 0 törölt sor; hunk `@@ -30434,0 +30435,166` |
| (f) 59 Strong, megjegyzés, batch | OK | `adat/forditasok.tsv:30435…30599` | 59 `sz1` sor a „a #159 mérő batchéből (adag1591” szöveggel; minden sor `claude-sonnet-5-5`; a 8 „2. próba” Strong 29 sora a `msgbatch_011JLtF14rip7TAyfMz67WBe` azonosítót is hordozza |
| (f) 59/1 | OK | `adag7904/kapu_eredmeny.jsonl` | 59 `kesz`, 8 `proba: 2`; az adag1591-hez képest egyetlen eltérés a G1187 (`16_sigla: Vulg. -> Vulgáta hiányzik`) |
| (f) terminológia-verzió | **ELTÉRÉS** | `adat/forditasok.tsv:30435–30600` (11. mező) | mind a 166 sorban `v5`; a fordítás a #159 batchében készült, a v5 előtt; a SEMA 807. sora: „…verziója, amellyel a fordítás készült” |
| (d1) `thayer_sigla.tsv` oszlopai | OK | `adat/thayer_sigla.tsv` | az egyetlen törölt token `jelolt` (164×); a forrásalak, a számoszlopok, a `pelda`, az utolsó `proveniencia` érintetlen |
| (d1) jóváhagyás módja | **ELTÉRÉS** | `DONTESEK.md` DT-F07e; brief 4.(d) | a brief „soronként”, a DT-F07e „egy tömbben” |
| (d2) `terminologia.tsv` csak új sor | OK | `adat/terminologia.tsv:87–116` | `--numstat` → `30 0`; mind `v5`, `nem` |
| (3) költség = futásnapló | OK | `naplok/THAYER_ELES_koltseg.tsv:2–4` | adag7901 2,509892, adag7902 1,025732, adag7903 0,751389; összesen 4,287013 ≤ 5 |
| (3) becslés-oszlop | **ELTÉRÉS** | `THAYER_ELES_koltseg.tsv:3` | a 7902 becslése 1,18, a `becsles_*.txt` fájlok összege 1,2050 |
| (3) M0-plafon | **ELTÉRÉS** | `THAYER_ELES_koltseg.tsv` `plafon_usd`; `thayer_api_koteg.py:146–169` | a plafonok összege 2,90 + 1,25 + 1,05 = 5,20 > 5 USD; a `futo_osszeg()` csak a saját adagot olvassa, `--elozo-kiadas` nélkül az 5 USD-t semmi nem kényszerítette ki; két sorban a becslés a plafon fölött van |
| (b) B-javító kör, kód | OK | `thayer_api_koteg.py` | kettős beküldés ellen a `csomag_javito.txt`; plafon `javito_becsles × 1,3`-mal; mellékes: a `javito_kerelmek` `strongok` paramétere nincs használva |
| (5) HOSSZULO, CV_ELOTT_NEM | OK | `thayer_kapuk.py:98–110`, `forditas_kapuk.py:358–368` | hiányzó siglát nem enged át; pozitív és negatív teszt van |
| (5) `apokrif` és a BDB | OK | `normalizal.py:66` | `'apokrif': {'Thayer'}`; a BDB-ben a bővített alakok 0 találat |
| (e) ⛔ sorrend: G4151 a (c) döntése után | **ELTÉRÉS** | `adag7902/batchek.tsv:3`, `adag7903/batchek.tsv:3`, `adag7901/batchek.tsv:2` | a G4151 egyenkénti batchei 11:48:31Z / 11:48:45Z, a (c) batch 11:48:58Z |
| (6) A1 = 35, A2 = 79, A8 = 1505, A9 = 918, összesen 5327 | OK | `naplok/THAYER_ELES_sorrend.tsv` | G1187 → adag 8 |
| (6) becslő-illesztés, adagbecslések | NEM ELLENŐRIZHETŐ | `THAYER_ELES_naplo.md` | a `THAYER_ELES_M0.py` futtatása nem megengedett; a medium/high kimenet 33 660 / 66 300 egyezik |
| (6) javító-arány módszere | **ELTÉRÉS** | `THAYER_ELES_naplo.md`; `JAVITO_ARANY` | 7901: 0,9140 / 0,8956 = 1,02 (csak a javított G1722, G1510 1. körével osztva); 7902: 0,84 és 7903: 0,95 (az összes egyenkénti 1. körrel osztva): következetlen, az A = 0,90 az A1–A3 becslés kb. felét adja |
| (6) 8_idezojel 20/10 | **ELTÉRÉS** | `DONTESEK.md` DT-F07g; napló | az arány az 50%-os küszöbön van, nincs hozzá futtatható parancs a `THAYER_ELES_M0.py`-ban; a proveniencia körkörös és rossz pontra mutat (6. helyett 9.) |
| (6) 60 Strong, high 0/60 | **ELTÉRÉS** | napló; DT-F07d | „javító kör után 0/60”, a végleges kapuval 1/60 (G1187): a két szám más kapuállapotra vonatkozik, jelöletlenül |
| (c) max_tokens | OK | `adag7901/futasnaplo.tsv` | 25 sor mind `end_turn`; legnagyobb kimenet 18 873 / 20 227 |
| (e) aranyminta-bukások | OK | `adag7902`, `adag7903/kapu_eredmeny.jsonl` | high 5 `kesz`; medium G4151, G5590 `javitando` (2/5) |
| DT-F07c `Sir` 813, `1 Cor` 119/124 | NEM ELLENŐRIZHETŐ | DONTESEK | az „egyszeri regex-számolás” nem reprodukálható |
| N68/N69 lezárás | OK | `NYITOTT_FELADATOK.md` | a kód megfelel a szövegnek |
| A2 nyitott tételek | **ELTÉRÉS** | `NYITOTT_FELADATOK.md` N70, N72 | az N70-et a DT-F07b megválaszolta, az N72 apokrif / `1 Cor` / sigla-része kész; a szöveg nincs frissítve |
| `ir`-fegyelem | **ELTÉRÉS** | `naplok/THAYER_ELES_M0_{arany,beirt,maxtokens,maxtokens_javito}_strongok.txt` | 4 új fájl nincs a brief `ir` listájában |
| 3. CI | OK, részben | — | a `futtat.py --valtozott …` E2–E20, E26, E28, E29, E31, E32: 0 találat; E25 3 (nem a diffből), E27 40 (régi hivatkozások), E30 4 figyelmeztetés |
| 7. `ellenoriz.py`, `feladatok.py ellenoriz`, tesztek | NEM ELLENŐRIZHETŐ | — | szerepkorlát |
| L1–L4 | OK | — | `forditasok` 0 törölt; `terminologia` 0; `thayer_sigla` 164 módosított; sorszám-Δ: `forditasok` +166, `terminologia` +30 |

**Az ELTÉRÉS-ek súlyosság szerint:** 1. ⛔ (e) sorrend (G4151 a DT-F07b előtt ment be); 2. `terminologia_verzio=v5` a 166 sorban; 3. a DT-F07g 50%-os küszöbdöntése nem reprodukálható; 4. az M0-plafonok összege 5,20 > 5 USD; 5. a javító-arány módszere következetlen; 6. „high 0/60” vs végleges 1/60 jelöletlen; 7. a 7902 becslése (1,18 vs 1,2050); 8. N70/N72 elavult szövege; 9. négy `ir`-en kívüli fájl; 10. (d1) „soronként” helyett „egy tömbben”.

## Javítás (végrehajtó, F07.8)

1. **Sorrend (e):** a G4151 beküldése tényleg megelőzte a DT-F07b-t. Hatástalan: a (c) döntése „nincs változás”, a G4151 kérései ugyanazzal a képlettel mentek volna. A naplóban rögzítve.
2. **`terminologia_verzio`:** a 166 sorban `v5` → `v4` (a fordítás a v4 tábla alatt készült; a `rogzit` a beíráskori verziót írja, ezért kézzel javítva, a naplóban).
3. **8_idezojel:** a számolás bekerült a `naplok/THAYER_ELES_M0.py idezojel` parancsba; a proveniencia a napló 9. pontjára és erre a parancsra mutat.
4. **M0-plafon:** a napló rögzíti, hogy a három adag külön plafonnal futott, a közös 5 USD-t a végrehajtó kézzel, a futásnaplók összegével tartotta (mért 4,2870 USD); a `--elozo-kiadas` nem volt használva. A 7902 becslése 1,2050-re javítva.
5. **Javító-arány:** egységes definíció (a javító kör költsége / az ugyanabban a futásban lévő összes nagy kérés 1. körének költsége, csak a teljesen lefutott javító körű futások): adag1 0,867, adag99 0,883, adag7902 0,84, adag7903 0,95 → pooled 0,873; a 7901 (részleges javító kör) kimarad. `JAVITO_ARANY['A'] = 0,87`; az adagterv újraszámolva.
6. **60 Strong:** a naplóban és a DT-F07d-ben jelölve: a „0/60” a #159 mérésének (régi kapuk) számát jelenti, a végleges kapukkal 1/60 (G1187).
7. N70 és N72 frissítve a `NYITOTT_FELADATOK.md`-ben.
8. A négy `*_strongok.txt` fájl az `ir` mezőben (`naplok/THAYER_ELES_M0_*_strongok.txt`).
9. (d1): a „soronként” helyett az orkesztrátor a táblát egy tömbben hagyta jóvá (DT-F07e); ez az orkesztrátor döntése, nem a végrehajtó eltérése.
