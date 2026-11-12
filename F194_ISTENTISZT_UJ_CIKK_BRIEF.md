---
feladat: 194
cim: Az ISTENTISZT-001 új cikke (2. kiadás) a HAMART-001 mércéjén — 1. fázis, adat
kod: ISTENTISZT_UJ_CIKK
tipus: feladat
fazis: lexikon
modell: opus
allapot: megallt
ag: claude/istentiszt-uj-cikk-992f57
pr: 709
ad: az ISTENTISZT-001 határa, jelöltjei, előfordulás-prózája, hiányzó fordításai és hatástörténet-anyaga a kész lap követelménylistája szerint, lépésenkénti méréssel
kovetkezo: "Az 1. fázis CS3-tól független adatlépései kész (F194.15–16: a main behozva, a kritérium és a meghatározás a motivumok.tsv-ben, a 14 LXX-sor és a Glossa két kézzel). Vár: a kapcsolat-lépés a CS3 C6-jára (N-F194a); a próza (U3), a lap újragenerálása (E28) és a nyílt mag angol rétege a CS3, az F202 és az F203 után, egyszer, külön jelre."
munka: adat
olvas: [sablonok/KESZ_LAP_KOVETELMENY.md, naplok/HATAR_ISTENTISZT-001.md, naplok/F123_teljesseg_ISTENTISZT-001.md, MUNKAMENET.md, adat/SEMA.md]
ir: [adat/jeloltek.tsv, adat/motivumok.tsv, adat/elofordulasok.tsv, adat/forditasok.tsv, adat/visszhang_megfelelok.tsv, adat/visszhang_tanuk.tsv, naplok/F194_meres.md, naplok/F194_naplo.md, naplok/HATAR_ISTENTISZT-001.md, naplok/F194_jelentes.md, adat/kapcsolatok.tsv, adat/elutasitasi_okok.tsv, adat/nyilt_kodkonyv.tsv, adat/tematikus_temak.tsv, naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv, dontesek/uj/istentiszt-uj-cikk-992f57.md, nyitott/uj/istentiszt-uj-cikk-992f57.md, F194_ISTENTISZT_UJ_CIKK_BRIEF.md]
fugg: []
---

# F194_ISTENTISZT_UJ_CIKK_BRIEF.md — Az ISTENTISZT-001 új cikke, 1. fázis

*FELADATOK #194 · Modell: opus (claude-opus-5-5), effort: a session alapértéke · v1 · 2026.11.11*

**Megbízás (az orkesztrátor-session, a felhasználó ütemezése szerint, 2026-11-11).** „az ISTENTISZT-001 új cikke a teljes eszköztárral, a HAMART-001 mércéjén. Ez a lap 2. kiadása. Ebben a sessionben egy kéz viszi végig: a határt, az adatot, és később a prózát is.” Az ütemezés (a felhasználó, 2026-11-11): HAMART arany → ISTENTISZT új cikk méréssel → nincs több új lap.

**Mérce.** `sablonok/KESZ_LAP_KOVETELMENY.md` (K01–K103). Ami nincs a listán, nem része a menetnek.

**Indok.** Az 1. kiadás (2026-11-02) foltozott; a HAMART-hoz mért próza-összevetés (közös jegyzetmappa, `ISTENTISZT_vs_HAMART_proza_2026-11-09.md`) új cikket indokol (memória: lap-menet-szintje).

## 1. fázis — adat (ez a menet)

1. **Határ (K93, K94):** a `naplok/HATAR_ISTENTISZT-001.md` K1–K8 kérdése. A K1–K5 szerkesztői döntéssel lezárt (DT476, DT478), nem nyílik újra. A K6–K8: értelmező ítélet a `jeloltek.tsv`-n át, indoklással; ahol a határ vagy a negatív kritérium szövege változna, ⛔ a felhasználó dönt.
2. **Scan és jelöltek:** a CLAUDE.md hét lépése, a teljesség-mérés újrafuttatása a mai adaton (K96).
3. **Előfordulások (K43, K40)** — *nem ebben a menetben: a 2026-11-12-i hatókör (az orkesztrátor) a prózát kizárta; a `kapcsolodas`/`funkcio` mezők a 2. fázis próza-lépésében íródnak (F194_naplo.md, F194.1; DT-F194b).* minden igehely alatt kerek `kapcsolodas`-mondat (a Károli-vers szó szerinti idézetével) és „Funkció:” sor („címke — magyarázat”), a HAMART-001 formájában (memória: 1a-kerek-proza).
4. **Hiányzó szótári fordítások (K59, C-y):** a `forditasok.tsv` `allapot` mezője szerint; ami érvényes, nem fordul újra.
5. **Hatástörténet-anyag (K67, K67a–K67f):** ÚSZ-ág (Vulgata, SBLGNT-apparátus, Targum az ÓSZ-helyeken); tanúréteg a `konkordancia/Tanu_atyak_index.tsv` és `Tanu_rabbinikus_index.tsv` fájlokból, a #183 HAMART-mintája szerint, két kézzel; a Glossánál kimondott hiány.

## 2. fázis — később, külön jelre

A próza (U3, a 10-es prompttal, nulláról) és a lap generálása a `szabalyhelyek` PR merge-e után (Alkalmazás nélkül, „9. Hatástörténet” főszakasszal).

## Ne nyúlj

`lexikon/HAMART-001*`, `eszkozok/lexikon_general.py`, `eszkozok/visszhang/`, `sablonok/`. Generátorhiba: N-tétel, nem javítás.

## Mérés (kötelező)

Lépésenként a `naplok/F194_meres.md`-ben: lépés, modell és effort, kezdő és záró idő, keret % előtte/utána (`get_usage`), futások és ellenőrzések száma, a lépés egysége (igehely-sor, Strong-szó, hiányzó fordítás, próza-szó). Cél: a többi lap arányosított becslése (lépés × egység).

## Garanciák és döntési napló

- G1: a három főszabály (proveniencia, nincs közvetlen út, memória vs. lekérdezés).
- G2: TSV-írás `split('\t')`/`'\t'.join()`, írás előtt soronkénti összevetés az eredetivel.
- G3: a generált lapot ez a fázis nem írja.
- D1: független ellenőrzés az 1. fázis végén (kód, adat, szabály), legfeljebb egy javítókör.
- ⛔ A határ- és kritériumváltozás és a merge a felhasználóé.
