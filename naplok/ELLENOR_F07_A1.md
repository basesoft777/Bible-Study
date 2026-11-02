# ELLENOR_F07_A1 — a #7 A1 független ellenőrzése

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`), tartomány: `origin/main` (`ec12f054`)..`c39ae073`/`3a37c93a`. Az ellenőr nem tudott fájlt írni és tesztet futtatni; a jelentést a végrehajtó mentette, a javításokat az F7.A1.9 commit vezette át (a tesztek, `ellenoriz.py`, `feladatok.py ellenoriz` a végrehajtónál futottak).*

**Eredmény: ELTÉRÉS 8 tétel, mind javítva.**

| # | Súly | Eltérés | Javítás |
|---|---|---|---|
| 1 | közepes–magas | A G0282 7 korábbi gépi (`sonnet`, v3) sora helyben felülíródott, nem `elavult`-ra került; a napló az ellenkezőjét állította; a bontás 666 új + 7 felülírt | napló A1 6. és 9.: pontosítva (410 új + 7 felülírt; `--regi-elavult` csak a `teljes` sorokat érinti; a `kezi teljes` sor marad) |
| 2 | közepes | A `9_tagolas` maszk lezáratlan mintái valódi alpontot nyelhetnek el (`cf. below, 2. a. of persons`) | `_UTAL_LEZAR` (az utalás nem folytatódhat szabad kisbetűs szóval; a jelölő pontja nem hagyható el), 2 új negatív teszt; az A1 8 újrakapuzott Strongja továbbra is átmegy |
| 3 | alacsony | `kovetkezo`: „eredeti A2” 85 / 611 808 | 79 Strong / 498 937 kar., a 6 bukottal együtt 85 / 611 808 |
| 4 | alacsony | napló: DT537 „visszaigazolásra vár” | átírva (visszaigazolva) |
| 5 | alacsony | DT535/j proveniencia scratchpadre mutatott | `naplok/THAYER_ELES_A1.py` + `kapu_eredmeny_1_kor.jsonl`, `kapu_eredmeny_2_kor.jsonl` |
| 6 | alacsony | `Esdr`/`Bel`/`Manasseh` nem lett N-F tétel | N-F07a (`NYITOTT_FELADATOK.md`) |
| 7 | alacsony | koltseg-tábla: `becsles_usd` 13,62 és `plafon_usd` 16,87 nem egy bázison | `becsles_usd` 12,98 (a sorrendterv, amelynek 1,3×-a a 16,87); a `szaraz` 13,62-je a naplóban |
| 8 | alacsony | `kapu_eredmeny.jsonl` 35 → 14 sorra íródott felül | a két korábbi állapot külön fájlban |

Nem ellenőrzött az ellenőr oldalán (a végrehajtó futtatta): tesztek (kapuk 126, kötegelő 35, normalizáló 70, `Lanc` 6 zöld), `ellenoriz.py` SÉRTÉS 0, `feladatok.py ellenoriz` 0 hiba.
