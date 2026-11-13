---
feladat: 194
cim: Az ISTENTISZT-001 új cikke (2. kiadás) a HAMART-001 mércéjén — 1. fázis (adat) és 2. fázis (lap, próza)
kod: ISTENTISZT_UJ_CIKK
tipus: feladat
fazis: folyamat
modell: opus
allapot: dontesre_var
ag: claude/istentiszt-uj-cikk-992f57
pr: 709
ad: az ISTENTISZT-001 határa, jelöltjei, előfordulás-prózája, hiányzó fordításai és hatástörténet-anyaga a kész lap követelménylistája szerint, lépésenkénti méréssel
kovetkezo: "A 2. fázis kész (F194.19–F194.32): a lap az új szerkezetben, a próza nulláról, a lektor és a független ellenőr javítókörével. Vár: az N-F194h (a lap elején álló, jóváhagyott kritérium és meghatározás három pontja) a felhasználó döntésére; utána a 2. kiadás `kiadasok.tsv`-sora a felhasználó lapátnézése után. Nyitott: N-F194a (a kapcsolat-lépés), N-F194d, N-F194e, N-F194f, N-F194g, N-F194i."
munka: adat
olvas: [sablonok/KESZ_LAP_KOVETELMENY.md, "tematikus_lezart/HAMART-001*", "tematikus_lezart/naplok/HAMART-001*", sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, "tematikus_lezart/ISTENTISZT-001*", "tematikus_lezart/naplok/ISTENTISZT-001*", naplok/HATAR_ISTENTISZT-001.md, naplok/F123_teljesseg_ISTENTISZT-001.md, MUNKAMENET.md, adat/SEMA.md]
ir: [adat/res_forras.tsv, eszkozok/tablajegyzet.py, eszkozok/kiejtes_szoveg.py, eszkozok/olvasoi_kapu.py, eszkozok/bdb_rovidites.py, lexikon/HAMART-001_TUDOMANYOS.md, adat/lap_javitasok.tsv, adat/kiadasok.tsv, archivum/ISTENTISZT-001/, eszkozok/teszt_szotari_gerinc.py, eszkozok/teszt_ellenoriz_31.py, eszkozok/teszt_ellenoriz_32.py, eszkozok/teszt_ellenoriz_35.py, eszkozok/teszt_olvasoi_kapu.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, motivumok/ISTENTISZT-001.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, naplok/F123_teljesseg_ISTENTISZT-001.tsv, eszkozok/lexikon_general.py, eszkozok/teszt_f194_szopar.py, eszkozok/teszt_kesz_lap_hamart.py, adat/jeloltek.tsv, adat/motivumok.tsv, adat/elofordulasok.tsv, adat/forditasok.tsv, adat/visszhang_megfelelok.tsv, adat/visszhang_tanuk.tsv, naplok/F194_meres.md, naplok/F194_naplo.md, naplok/F194_jelentes.md, adat/kapcsolatok.tsv, adat/elutasitasi_okok.tsv, adat/nyilt_kodkonyv.tsv, adat/tematikus_temak.tsv, naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv, dontesek/uj/istentiszt-uj-cikk-992f57.md, nyitott/uj/istentiszt-uj-cikk-992f57.md, F194_ISTENTISZT_UJ_CIKK_BRIEF.md]
fugg: []
nem_fugg: [151, 123, 178, 179, 70, 203, 212]
---

# F194_ISTENTISZT_UJ_CIKK_BRIEF.md — Az ISTENTISZT-001 új cikke, 1. és 2. fázis

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

## 2. fázis — az orkesztrátor indítása (2026-11-12, a felhasználó: „vidd végig ezeket: ISTENTISZT prózája …”)

A próza (U3, a 10-es prompttal, nulláról) és a lap generálása a CS3 (F212), az F202 és az F203 után (Alkalmazás nélkül, „9. Hatástörténet” főszakasszal): 1) a main behozása; 2) a teljesség-mérés a mai Strong-halmazzal (új jelöltvers esetén megállás); 3) a lap újragenerálása a CS3-generátorral, a HAMART-001 2. kiadásának mintájára; 4) a próza egy kézben; 5) kapuk, lektor, egy javítókör, független ellenőrzés; 6) a teljes helyi ellenőrzés 0 HIBA-ig, push. A kiadás sora csak a felhasználó lapátnézése után.

## Ne nyúlj

`lexikon/HAMART-001*`, `eszkozok/lexikon_general.py`, `eszkozok/visszhang/`, `sablonok/`. Generátorhiba: N-tétel, nem javítás.

*A 2. fázisban az orkesztrátor jóváhagyásával (2026-11-12) a generátor és a kapuk az ISTENTISZT-001 új szerkezetéhez igazodnak (`UJ_LAPSZERKEZET`, DT-F194h, a „Jahve” és a pontozatlan rokon alak), a HAMART-001 lapja legfeljebb a jóváhagyott három sorral változik (`adat/lap_javitasok.tsv`); az `eszkozok/visszhang/` és a `sablonok/` változatlan.*

## Mérés (kötelező)

Lépésenként a `naplok/F194_meres.md`-ben: lépés, modell és effort, kezdő és záró idő, keret % előtte/utána (`get_usage`), futások és ellenőrzések száma, a lépés egysége (igehely-sor, Strong-szó, hiányzó fordítás, próza-szó). Cél: a többi lap arányosított becslése (lépés × egység).

## Garanciák és döntési napló

- G1: a három főszabály (proveniencia, nincs közvetlen út, memória vs. lekérdezés).
- G2: TSV-írás `split('\t')`/`'\t'.join()`, írás előtt soronkénti összevetés az eredetivel.
- G3: a generált lapot az 1. fázis nem írja; a 2. fázis a generátorral írja újra (kézi szerkesztés nincs).
- D1: független ellenőrzés mindkét fázis végén (kód, adat, szabály), fázisonként legfeljebb egy javítókör (1. fázis: `naplok/F194_jelentes.md`; 2. fázis: `naplok/ELLENOR_F194_2.md`).
- ⛔ A határ- és kritériumváltozás és a merge a felhasználóé.
