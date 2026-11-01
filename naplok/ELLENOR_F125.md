ELTÉRÉS: 7 tétel
# ELLENOR_F125 — F125_GERINC_KARTYA_SZOVEG_BRIEF.md · `9ad99898..HEAD` (PR #554)

*A `fuggetlen-ellenor` jelentése (2026-11-01), összefoglalva; a subagentnek nincs íróeszköze, a fájlt az orkesztrátor-menet írta. Az ág saját változása 15 fájl; az `origin/main..HEAD` kétpontos diff a main előrehaladása miatt többet mutat.*

## ELTÉRÉS-ek (súlyossági sorrendben)

| # | Tétel | Hely | Mi az eltérés |
|---|---|---|---|
| 1 | Csoportos kategória túl tág (DT471) | `eszkozok/proza_lefedettseg.py:121,133,160`; `teszt_proza_lefedettseg.py:68-71` | `csoportos = any(CSOPORTOS.search(p) …)`: ha a prózában bárhol szerepel „N igehely”, az összes név nélküli előfordulás „csoportosan fedett”, a számot semmi nem veti össze az előfordulások számával. A `TEREMT-002.md:235` („3 igehelyen … 1Móz 1:2, Jer 4:23, Ézs 34:11”) is kiváltja. A napló „darabszám szerint kezeli” állítása (`naplo:152`) nem felel meg a kódnak. |
| 2 | A sablonok a 22. szabályról mást állítanak | `sablonok/1_:69`, `2_:306`, `4_:436`, `5_:73` | A K-sor szerint a 22. szabály „jelzi, ha egy szó egy szakaszban egyszer sem kap kiejtést”; a `szabaly22_kiejtes_hiany` csak a `lexikon/*_TUDOMANYOS.md`-t olvassa (tanulmányt nem), és az első előfordulás hiányát jelzi (a későbbi kiejtés nem pótolja). |
| 3 | A `/kiadas` 3. lépése nem hajtható végre | `.claude/commands/kiadas.md:21,26` | Nincs lektor-subagent fájl (`.claude/agents/`: nincs lektor; a `hatar-ellenor` `model: fable`), így a „ne adj meg model paramétert” utasításnak nincs alanya; az „eltérő modell” nem biztosítható, mert a próza készítő modelljét a repó nem rögzíti (DT443). |
| 4 | A kolofon kiadás-sorának nyitott tétele nincs nyilvántartva | brief `kovetkezo`, `naplo:164` | Csak a `kovetkezo` mezőben és a naplóban áll; az `F152` briefben nincs, N-F helyőrző sincs, a kiadásszámnak nincs adatforrása (`kiadas.md:28`). |
| 5 | Ellentmondó kiejtés-sorok | `1_:68`, `2_:305`, `4_:435`, `5_:72`, `6_:366`, `gyorsref:30` | Az új K-sor fölött a régi „Minden görög/héber szótári szó mellett feltüntetve a kiejtés” sor bent maradt; ellentmond az újnak (bekezdésen belül nem ismétlendő, idézetben nincs). |
| 6 | Hiányzó proveniencia-sor | `DONTESEK.md` DT471, `naplo:11,153` | Az 57, 4, 192, 77 mért szám `scope=… \| forras=… \| ts=…` nélkül áll. |
| 7 | `ir` mező eltérése | brief fejléc | A `naplok/F125_SZOVEGJAVASLAT.md` megíródott, de nincs az `ir`-ben; a `teszt_ellenoriz_proza.py` az `ir`-ben van, de nem készült el (egy fájlban a `teszt_proza_lefedettseg.py`); az e6e7955d két tételt (F125.2 és F125.1) visz egy commitban. |

## Rendben (szó szerinti egyezés)

A3b, A3c, a prioritási-térkép mondata, a 2_ v22, C-x, C-y, C-z, C-w, K (a 6 beírt sor betűre azonos a javaslattal), L, O: egyezik a jóváhagyott szöveggel. A két JELENTÉS-szabály csak `JELENTÉS`/`RENDBEN`/`KÉZI` verdiktet ad, nem SÉRTÉS. A #152 fájljai (`lexikon_general.py`, ISTENTISZT-001 forrás, `lexikon/`) érintetlenek; az `adat/` és `konkordancia/` diffje nulla. A ⛔ sorrend betartva (a sablonok csak az F125.3-ban változnak).

## NEM ELLENŐRIZHETŐ

- A 22 → 192 és 23 → 77 mért szám (az `ellenoriz.py` nem futtatható az ellenőr parancskészletével).
- A jóváhagyás eredete („a javaslatod szerint”, orkesztrátor-idézet).
- A PR-cím `[ELLENŐRZŐ]` előtagja (a `futtat.py` `--pr-cim` nélkül E16 HIBA).
- A kiejtés „jelölés nélkül” ↔ kód: a `kiejtes_szoveg.py:10,92` és a `lexikon_general.py` docstringjében még „…, gépi” jelölés áll; a diff ezekhez nem nyúl.
- Hogy a végrehajtó ténylegesen Sonnet volt-e (a repóból nem igazolható).
