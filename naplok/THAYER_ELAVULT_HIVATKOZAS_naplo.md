# THAYER_ELAVULT_HIVATKOZAS (#155) — napló

*Végrehajtó: `claude-sonnet-5-5` · ág: `claude/f155-thayer-elavult-hivatkozas` · 2026.11.02 · a brief: `F155_THAYER_ELAVULT_HIVATKOZAS_BRIEF.md`*

## 1. Mért kiindulás

scope=adat/forditasok.tsv | forras=`grep -c "DT-F132c" adat/forditasok.tsv`; `awk -F'\t' '/DT-F132c/{n++; if($1=="Thayer"&&$8=="elavult")e++}'` | ts=2026-11-02

- `DT-F132c`-t tartalmazó sor: **7**; mind `Thayer … teljes … elavult` sor (a találatok = az `elavult` Thayer-sorok).
- A 7 sor Strongja (fájlsorrendben, sorszám): G1311 (66), G2671 (67), G5010 (69), G5356 (70), G0012 (71), G5351 (73), G0086 (79).

## 2. Lépések

- **F155.0** (`0b815caa`): a brief fejléce `allapot: fut`, `ag` mező. A `FELADATOK.md`-hez nem nyúltam.
- **F155.1** (`615c1cc8`): `eszkozok/thayer_jelolt/forditas.py:219` — a `beir()` megjegyzése `…(%s; DT-F132c)` helyett `…(%s; DT329)`. A docstring és a 211./216. sor hibaüzenetei (`DT-F132c (i)`, `(ii)`) a briefe szerint nem hatókör, nem módosultak. Teszt: `teszt_lanc.py` `Lanc.test_beir_opus_regi_elavul` — a `beir` által beírt megjegyzés tartalmazza a `felváltva: szakaszonkénti fordítás (2026.10.25; DT329)` szöveget, és nem tartalmaz `DT-F132c`-t. A teszt a `forditasok.tsv` ideiglenes másolatán dolgozik (`tempfile.mkdtemp`), a valódi táblához nem nyúl.
- Az `adat/forditasok.tsv`-hez **nem** nyúltam (a 2. lépés ⛔, DT-F155a).

## 3. Egyeztetett eltérés (a felhasználó kérése, chat 2026-11-02: „#155 és a teszt”)

A `teszt_lanc.py` `Szolista.test_gerinc_halmaz_normalizalt` állítása `g['G1941'] == 10` elavult volt.

scope=szolista.gerinc_strongok()['G1941'] | forras=`python -I` + `szolista.gerinc_strongok()` a worktree-n (main a95a1db9) | ts=2026-11-02

- Mért érték: **6**.
- Ok: a DT476 / F152.14 (K1–K5 átvezetés) szándékosan vette ki a Róm 10:12, 10:14, 2Tim 2:22, 1Pét 1:17 helyet az ISTENTISZT-001-ből (10 − 4 = 6).
- A teszt állítása 6-ra javítva, megjegyzéssel.

## 4. Teszteredmény (szó szerint)

`python eszkozok/thayer_jelolt/teszt_lanc.py`:

```
Ran 40 tests in 24.263s
FAILED (failures=1)
FAIL: test_tabla_determinisztikus_es_kezi_vedett (__main__.Sigla.test_tabla_determinisztikus_es_kezi_vedett)
AssertionError: 1 != 0 : jelölt: 255 ({'minta': 31, 'kiadas_sigla': 6, 'rovidites': 218}); a gerincszavakban előforduló: 90
ELTÉR: …\adat\thayer_sigla.tsv
```

Az egyetlen hiba az ismert N66 sigla-teszt; a többi 39 zöld (a `Szolista` és a `Lanc.test_beir_opus_regi_elavul` is).

- `python eszkozok/ellenoriz.py`: `RENDBEN: 17 | SÉRTÉS: 0 | KÉZI: 2 | JELENTÉS: 7`.
- `python eszkozok/feladatok.py ellenoriz`: `177 brief, 0 hiba, 0 figyelmeztetés`.

## 5. Nyitott: ⛔ DT-F155a

A 7 `elavult` Thayer-sor megjegyzése: (a) bájt-szintű csere `DT-F132c` → `DT329`, vagy (b) a történeti szöveg marad. Lásd `DONTESEK.md` DT-F155a. Az (a) elfogadási feltétele: `grep -c "DT-F132c" adat/forditasok.tsv` = 0, minden más sor bájtra azonos; a (b)-é: 7, dokumentálva.
