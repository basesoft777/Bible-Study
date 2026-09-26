# CI_alapallapot — CI.0 (alapállapot-mérés)

*Forrás: `CI_ELLENORZES_BRIEF.md`, CI.0 tétel. Futtatás: `python
eszkozok/ellenorzes/futtat.py --teljes`, teljes repóra, 2026.09.26.
Az E1-et (SEMA §3 1–12, Q1, Q7) a meglévő `eszkozok/ellenoriz.py` már
gépesíti — ez a mérés nem ismétli meg.*

`--teljes` módban minden szabály **JELENTÉS** szinten fut (a HIBA-besorolás
csak a diff-hatókörre, azaz `--valtozott FÁJL…` módra vonatkozik — l. brief
"Diff-hatókör" szakasz, D3). Az alábbi táblázat a brief javasolt szintjét
mutatja (`E2–E11`: HIBA-jelölt; `E12–E15`: FIGYELMEZTETÉS-jelölt, D4), a
tényleges besorolásról a felhasználó dönt ezen számok ismeretében.

## Összegzés

| Szabály | Javasolt szint | Találatszám (teljes repó) | Megjegyzés |
|---|---|---|---|
| E2 | HIBA | 140 | "ellenőrizve" jelölés proveniencia-sor nélkül a szakaszban |
| E3 | HIBA | 0 | `adat/elofordulasok.tsv` proveniencia-mezője mindenhol kitöltött, nem "ellenőrizve" |
| E4 | HIBA | 0 | minden `auditok.tsv`-beli teljes-scan (B3) motívumhoz van naplófájl és kitöltött döntés |
| E5 | HIBA | 0 (N/A) | diff-alapú szabály — `--teljes` módban nincs base/head, nem értelmezhető |
| E6 | HIBA | 1 | 1 tematikus study hiányzó "0. Forrás-összegyűjtés" szakasszal |
| E7 | HIBA | 0 | nincs "bekerült" jelölt, ami csak prózában szerepelne |
| E8 | HIBA | 0 | tiltott igehely-formátum egy fájlban sem |
| E9 | HIBA | 99 | angol "sense" szó study-/dokumentációs szövegben (ld. korlát lent) |
| E10 | HIBA | 0 | "spirit"/"lélek" tiltott fordítás-pár mintája nem talált |
| E11 | HIBA | 61 | Cremer/NIDNTTE/NIDOTTE említés (ld. korlát lent) |
| E12 | FIGYELMEZTETÉS | 4087 | proveniencia-szerű szöveg prózában, NAPLO-blokkon kívül |
| E13 | FIGYELMEZTETÉS | 3837 | héber/görög betűfutam 40 karakteren belüli átírás nélkül |
| E14 | FIGYELMEZTETÉS | 0 | tematikus sablon "Jelentés-szöveg" cellája nem angol túlsúlyú sehol |
| E15 | FIGYELMEZTETÉS | 0 | nincs 25 szónál hosszabb SzPA-idézet minta |
| E16 | HIBA | 0 (N/A) | önmódosítás-őr — csak PR-kontextusban (`--pr-cim`) értelmezhető, `--teljes` alatt üresen fut |

## Ismert korlátok — a felhasználónak a HIBA/FIGYELMEZTETÉS döntéshez

- **E2, E9, E11, E12, E13 a teljes repóra futott**, tehát a brief- és
  workflow-dokumentumokat (pl. `CREMER_OCR_BRIEF.md`, `ATALAKITASI_TERV.md.md`)
  is nézi, nem csak a tényleges study-/naplófájlokat. A diff-hatókörű
  (`--valtozott`) HIBA-mód ezt automatikusan szűkíti a PR-ben módosított
  fájlokra (D3), de a `--teljes` szám itt a *teljes* felületet mutatja —
  ezért ilyen magas az E12 (4087) és E13 (3837): ezek nagy része brief-
  és tervdokumentumokban van, ahol a szabály indoka (NAPLO-szétválasztás,
  kiejtés-szabály) nem is vonatkozik rájuk.
- **E9 (angol "sense")** és **E11 (Cremer/NIDNTTE/NIDOTTE)** találatai
  jelentős részben magukban a brief-dokumentumokban vannak, ahol a
  tiltás *tárgyaként* (pl. a Cremer-tiltás indoklásaként) szerepel a szó —
  ezek nem valódi szabálysértések, hanem a szabály saját dokumentációja.
- **Javaslat**: E12/E13 hatókörét a HIBA-besorolás bevezetésekor is csak a
  study-/napló-/lexikon-könyvtárakra kellene szűkíteni (`tematikus_lezart/`,
  `genezis/`, `ujszovetseg/`, `melyelemzesek/`, `motivumlog/`, `lexikon/`),
  kizárva a gyökérkönyvtár brief- és tervfájljait — ez a diff-hatókör miatt
  HIBA-módban amúgy is csak a ténylegesen módosított fájlokra szűkül.
- **E5** és **E16** `--teljes` módban szerkezetileg nem futtatható
  (nincs mihez viszonyítani egy diffet, illetve nincs PR-cím) — ezeket a
  CI.2 GitHub Actions workflow gyakorolja élesben, PR-kontextusban.

## Minta-találatok szabályonként (max. 3)

### E2 — "ellenőrizve" proveniencia nélkül (140)
- `Atadasi_dokumentum_2026_09_11.md:143` -- "még nem történt meg"-ként jelöli — ez **igaz állítás**, ellenőrizve.
- `Atadasi_dokumentum_2026_09_11.md:189` -- memóriából, de jelölni kell. *Incidens: egy "🔍 STEPBible-ellenőrizve"
- `CREMER_OCR_BRIEF.md:126` -- - **O3.1** Szócikkhatárok: a szócikkfej görög címszava (a lap élőfejével és a görög szómutatóval keresztellenőrizve), fő- és Supplement-rész külön.

### E6 — hiányzó "0. Forrás-összegyűjtés" (1)
- `tematikus_lezart/Pneuma_pszukhe_megkulonboztetes_tematikus.md:0` -- hiányzik a "0. Forrás-összegyűjtés" szakasz

### E9 — angol "sense" (99)
- `Atadasi_dokumentum_2026_09_11.md:145` -- ### 3.8 ⚠️ Sense-szám mező nem-numerikus értékei — indoklás nélkül
- `Atadasi_dokumentum_2026_09_11.md:149` -- igegyököket binyan szerint tagolja, nem számozott sense-ekkel. Ez
- `F4_GENERATOR_BRIEF.md:576` -- Strong-szám(ok) | BDB-entry-id | Sense-szám | Jelentés-szöveg (EN + HU).

### E11 — Cremer/NIDNTTE/NIDOTTE (61)
- `CREMER_OCR_BRIEF.md:1` -- Cremer említve: # CREMER_OCR_BRIEF.md — a Cremer teljes szövegének javítása külső képolvasó modellekkel
- `CREMER_OCR_BRIEF.md:5` -- Cremer említve: **Cél.** Hermann Cremer *Biblico-Theological Lexicon of New Testament Greek* (3. angol kiadás,
- `CREMER_OCR_BRIEF.md:11` -- Cremer említve: **Viszony a `SZOTAR_BRIEF.md`-hez.** Független tőle: csak a `konkordancia/_nyers/cremer/` alól

### E12 — proveniencia prózában (4087)
- `.claude/agents/tanito-kereso.md:8` -- A `sablonok/7_PaRDeS_tanitoi_kereses_sablon.md` szerint dolgozol. Bemeneted egy
- `.claude/agents/tanito-kereso.md:9` -- motívum-ID és a hozzá tartozó study-fájl. A `sablonok/PaRDeS_tanitok_lista.md`
- `.claude/agents/tanito-kereso.md:19` -- Kizárólag a `[study-mappa]/naplok/[motívum]_tanitoi_kereses.md` fájlt írod —

### E13 — kiejtés hiánya (3837)
- `ATALAKITASI_TERV.md.md:170` -- **Az 1. lépés szabálya nem az, hogy „mindig kezdd metszettel", hanem hogy a gerincet mindig le kell vezetni, és a levezetést dokumentálni kell — akkor
- `ATALAKITASI_TERV.md.md:267` -- | ISTENTISZT-001 | formulaikus (קָרָא בְשֵׁם יְהוָה) |
- `ATALAKITASI_TERV.md.md:278` -- 2. **Mi az a minimális jegy, amely nélkül egy igehely NEM tartozik ide?** → `negativ_kriterium` mező. Minta: az ISTENTISZT-001-ből kizárt D-minta (נִק

## Teljes szabálylista, találatszámmal

E2: 140 · E3: 0 · E4: 0 · E5: 0 (N/A, diff-alapú) · E6: 1 · E7: 0 · E8: 0 ·
E9: 99 · E10: 0 · E11: 61 · E12: 4087 · E13: 3837 · E14: 0 · E15: 0 ·
E16: 0 (N/A, PR-alapú)

## Megállás — jóváhagyás a CI.2 előtt

A brief (nyitó prompt) szerint itt áll meg a munka: a felhasználó dönti el,
melyik HIBA-jelölt szabály maradjon ténylegesen HIBA szinten (a fenti
korlátok, főleg az E12/E13 magas száma miatt), mielőtt a CI.2 (GitHub
Actions workflow) ezekre épülne.
