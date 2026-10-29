# ELLENŐR — F146_VERSMEGF_MT_JAVITAS_BRIEF.md · `dababe2c..c8b5b19f`

*A `fuggetlen-ellenor` subagent jelentése (modell: `claude-opus-5-5`, a kért `opus`; egyezik). Az ellenőr csak olvasó szerepű, a fájlt nem tudta megírni; a jelentést a végrehajtó session tette át szó szerint, a táblázatot tömörítve (a parancsok és az eredmények változatlanok). A végén a javítókör.*

Saját commitok: F146.0 fa4475d6, F146.1 86698e26, F146.2 fd5da52e, F146.3 c8b5b19f; 7347b950 = a main beolvasztása. A merge-base az origin/main-nel `dababe2c` (= base).

```
ELTÉRÉS: 1 tétel
```

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | `naplok/VERSMEGF_MT_JAVITAS_naplo.md:3` | session `claude-opus-5-5`, kért `opus`; a napló `modell` értéke a tényleges modell |
| 1 Jóel Károli 2:28–32 = MT 3:1–5 | OK | `Karoli_versmegfeleltetes.tsv:16139-16143` | `lekerdez.py scan H7121 --szakasz "Jóel 2:32"` → 2 előfordulás; `scan H8034` → 1 (`scope=range:Jóel 2:32 \| forras=TAHOT_kivonat.tsv \| ts=2026-10-29T07:18Z`). Macula `ref`: `JOL 3:5!4/!20` H7121, `!5` H8034. `scan H2472/H2492` → Jóel 2:28; Macula `JOL 3:1!14/15`. Maculában nincs `JOL 2:28–32` |
| 1 Jóel Károli 3:1–21 = MT 4:1–21 | OK | Jóel 3:x sorok | `scan H7622` → Jóel 3:1, Macula `JOL 4:1!11`; `scan H5352` → Jóel 3:21, Macula `JOL 4:21!1/!4`; versszám mindkét oldalon 73. A Macula `karoli` oszlopa nem tanú |
| 1 Jóel 1:1–2:27 azonosság | OK (szúrópróba) / teljes: NEM ELLENŐRIZHETŐ | — | `scan H6165/H8628/H0954`: 1:20, 2:1, 2:15, 1:11, 1:12, 2:26, 2:27 a Maculában azonos `ref`-en |
| 2 halmaz-őr a táblán | OK | `Karoli_versmegfeleltetes.tsv:7`, Jóel-blokk | `git diff --numstat` 27/26: a 26 Jóel-sor + 1 `# F146 javítás` jegyzet; más sor nem változott |
| 2 KK4 kétszeri futás / egyezés | NEM ELLENŐRIZHETŐ (szerepkorlát) | napló 6. | a KK4 futtatása kívül esik az ellenőr parancsain |
| 2 a javító bemenet 350 sora változatlan | OK | `Karoli_versmegfeleltetes_javitas.tsv` | `git diff --numstat` 27/0 |
| 3 az F117-szabály nem lazult | OK | `eszkozok/versmegf_javitas.py:132-135` | az F117 KEZI-ága változatlan; az új ág csak `forras == FORRAS_F146`; új negatív teszt |
| 3 `teszt_versmegf_javitas.py` fut | NEM ELLENŐRIZHETŐ (szerepkorlát) | — | |
| 3 fejléc-jegyzet szűrése | OK | `versmegf_javitas.py:68,150` | megjegyzés: a jegyzetszöveg rögzítetten a Jóelről szól; ha az N-F146a újabb `macula_mt_f146` sort hoz, hamis lesz |
| 4 ISTENTISZT-001: csak időbélyeg + Jóel 2:32 | OK | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:89` | `--word-diff=porcelain`: 15 `ts=`, 1 `Generálva:`, 1 Jóel 2:32 |
| 4 a Jóel 2:32 DBH-oszlopa | OK | `…:89` | `UBS_DBH_referenciak.tsv` `Jóel 3:5`: H7121 `006562001006000`, `006562001011000`, H8034 `007442001001000`; `Jóel 2:32`-re 0 sor; a lap mindhármat `(MT: Jóel 3:5)`-tel hozza |
| 4 a többi 7 lap | NEM ELLENŐRIZHETŐ (szerepkorlát) | napló 7. | a diff más lexikonfájlt nem érint |
| 5 proveniencia az új adatsorokon | OK | javító bemenet, 26 sor | mind `scope=gepi:Jóel N … \| dontes=DT398 \| ts=2026-10-28` |
| 5 TSV `split('\t')`, kód fájlból | OK | `naplok/F146_*.py` | `csv` 0 találat; `reconfigure`-őr megvan |
| 6 felmérés | OK (szúrópróba) | `F146_mt_felmeres.tsv:792,821,1012,1091` | Jób 41:32 → MT 41:24 (`scan H7872`, Macula `JOB 41:24!6`); Mal 4:1 → MT 3:19 (`scan H8574/H6057`); 1106 adatsor = 982+9+93+19+3 |
| 6 a 12 vers ítéletei | OK (szúrópróba) | napló 4. | Préd 9:12 → MT 9:10 (`scan H2808/H7585`, Macula `ECC 9:10`); Jób 38:7 = MT 38:7 (`scan H3556`) |
| brief 2.3 / Kész 3 soronkénti proveniencia | **ELTÉRÉS** | napló 4. | egyetlen közös proveniencia-sor a táblázat fölött |
| brief 2.2 a halmazt nem javították | OK | `Karoli_versmegfeleltetes.tsv:16927,23184` | Mal 4:1 és Ézs 9:1 változatlan |
| ⛔ 3.1 | OK | fa4475d6, fd5da52e | a DT398 az F146.0-ban nyitott, a javítás az F146.2-ben |
| G 3.3 fogyasztók | OK / részben NEM ELLENŐRIZHETŐ | `lexikon_general.py:1123-1126`; `sqlite_epit.py:192` | jelzetlen fogyasztó: `eszkozok/f17/macula_kk.py:100-101` (a kitöltött `igehely_mt` elsőbbsége; a Macula újragenerálásakor a Jóel-sorok `forras`-a változhat) |
| 7 szó szerinti idézet | OK formailag / tartalmilag NEM ELLENŐRIZHETŐ | `DONTESEK.md:459-460` | az idézetek a szülő sessionön át érkeztek |
| 7 nincs végleges DT-szám | OK | — | E26: 0 |
| A1 | OK | napló 2–7. | |
| A2 | OK | `NYITOTT_FELADATOK.md` | megjegyzés: az N-F146a a Jób 38:7/16/30-at „táblahibának” nevezi (valójában osztály-anomália), a Jób 41:32 kétszer számolódik |
| A3–A5 | NEM ALKALMAZHATÓ | — | |
| A6 (E12–E15) | OK | lexikonlap | E12 357 J, E13 120 J, E14/E15 0; HIBA nincs |
| CI | NEM ELLENŐRIZHETŐ (nem volt CI-jelentés) | — | saját `futtat.py`: E2–E11, E14–E16, E19, E20, E26, E28–E31 0; E12 357 J, E13 120 J, E25 4 J, E27 41 J (FELADATOK.md), E32 3 J (a DT-F117a/e literál a base-ben is) |
| 1–5. ellenőrzőpont (törölt sorok, kulcstartomány, nulladiff hatóköre, sorszám-Δ, ⛔) | OK / a nulladiff NEM ELLENŐRIZHETŐ | — | a javító bemenet +26 adatsor egy kategóriában (KEZI, Jóel 2:28–3:21), a bontás a napló 6.-ban |

ELTÉRÉS súlyossági sorrendben:
1. (alacsony) A brief 2.3 / Kész 3 soronkénti proveniencia-sort kér a #131 12 versére; a naplóban egy közös sor áll.

Merge előtt fontos lehet: (a) a KK4 bájtazonossága, a teszt és a 7 lap nulladiffje az ellenőr számára nem futtatható; (b) az origin/main előreszaladt (F38 11. adag, `adat/forditasok.tsv`), a lap merge után elavult lehet; (c) a Jóel 2:32 sorában egy angol „fordításra vár” DBH-definíció (N-F146b).

## Javítókör (F146.4, a végrehajtó session)

1. **ELTÉRÉS 1 — javítva:** a napló 4. szakaszának táblázata soronkénti `proveniencia` oszlopot kapott (`scope=vers:<igehely> | forras=… | eszkoz=naplok/F146_131_versek.py | ts=2026-10-28T21:24Z`).
2. **A2 megjegyzés — javítva:** az N-F146a szövege a Jób 38:7/16/30-at osztály-anomáliaként (Károli = KJV = MT, `KEZI` üres `igehely_mt`-vel) írja le, a Jób 41:32-nél jelzi, hogy a 956 között is szerepel.
3. **`macula_kk` fogyasztó és a jegyzetszöveg — naplózva** (napló 6.); a Macula-import nem tartozik e tétel hatókörébe.
4. **NEM ELLENŐRIZHETŐ pontok — a végrehajtó saját futása (bizonyíték csak ez):** KK4 kétszer a repón kívülre, bájtazonos (sha256 `a16e9572…d2a3`) és azonos a commitolt táblával; `naplok/F146_tabla_osszevet.py` OK; `python eszkozok/teszt_versmegf_javitas.py` 23/23 OK; 8 lap nulladiffje (régi/új tábla): 7 bájtra azonos, az ISTENTISZT-001-ben csak a Jóel 2:32 sora (napló 7.).
5. **A main előreszaladt — kezelve:** a main újra beolvasztva, a lap újragenerálva és összevetve (napló 8.).
