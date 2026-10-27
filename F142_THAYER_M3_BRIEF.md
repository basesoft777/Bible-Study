---
feladat: 142
cim: A motívumok aktuális görög gerincszavainak szakaszonkénti Thayer-fordítása (a #132 M3-a, újrafuttatható, Sonnet)
kod: THAYER_M3
tipus: feladat
fazis: 2
modell: sonnet
munka: adat
allapot: megallt
ad: a motívumok aktuális görög gerincszavai (a futás pillanatában, DT332 (1)) szakaszonként magyarul a forditasok.tsv-ben (`szotar = Thayer`, `jelentes_szam = sz<n>`), a gátoló kapukon (köztük 14_szakasz, 15_tiltott, 16_sigla) átengedve; a régi `teljes` sorok a DT329 szerint jelölve; újrafuttatható
ag: ccr-676ffb53-9qo1to
kovetkezo: "Te: /elteres 142"
olvas: [adat/thayer_szakaszok.tsv, adat/thayer_forras_javitas.tsv, adat/thayer_vers_jelentes.tsv, adat/thayer_sigla.tsv, adat/tiltott_fordulatok.tsv, adat/terminologia.tsv, adat/elofordulasok.tsv, adat/karoli_strong/, konkordancia/Karoli_1908.tsv, konkordancia/Strong_szotar.tsv, konkordancia/lexikonok_nyers/Thayer.lexicon, forditas/prompt_v5_1.md, eszkozok/thayer_jelolt/, eszkozok/forditas_kapuk.py, eszkozok/emeles.py, eszkozok/bdb_jelolt/szakasz_bemenet.py, F132_THAYER_SZAKASZ_BRIEF.md]
ir: [adat/forditasok.tsv, adat/thayer_sigla.tsv, naplok/F132_THAYER_SZAKASZ_munka.tsv, naplok/F132_THAYER_SZAKASZ_bukottak.tsv, naplok/F132_THAYER_SZAKASZ_naplo.md, naplok/F142_zaras.md]
fugg: [132]
nem_fugg: [38, 123, 138]
---

# Fnn_THAYER_M3_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

*FELADATOK #nn · Modell: sonnet · v0 (tervezet) · 2026.10.25 · készítette: a #132 végrehajtója (`claude-opus-5-5`), a DT334 (1)
szerint; befogadás: `/befogad`, a felhasználó jóváhagyásával.*

## 1. Cél

A #132 (`F132_THAYER_SZAKASZ_BRIEF.md`) M3-a külön, Sonnet-modellű feladatként (DT334 (1), felhasználó, 2026-10-25): a motívumok
aktuális görög gerincszavainak szakaszonkénti magyar Thayer-fordítása a #132 által épített közös láncon. A #132 az M0–M2-t, az
M3 előfeltételeit (betöltő, szólista, javítótábla, adatblokk, kapuk, prompt v5.1, sigla-javaslat) és az Mz-t adja; a fordítás itt fut.

Kötelező döntések (mind eldöntve, `DONTESEK.md`):

- **DT332 (1):** a lista a futás pillanatában az `adat/elofordulasok.tsv` görög Strongjai (`Strong_padded`); kimarad, aminek már
  van érvényes (nem `elavult`, `forras_hash`-egyező) szakaszos fordítása. Újrafuttatható: új motívum görög szava a következő futásban
  kerül sorra.
- **DT329 (a)+(i)+(ii):** szakaszonkénti újrafordítás; a régi nem `kezi` `teljes` sor `elavult` (felváltás jelölésével); a `kezi`
  `teljes` sor a DT290 (3) szerint érvényes marad, amíg a felhasználó az új szakaszsorokat jóvá nem hagyja; a G0994 (gerincen kívül)
  változatlan.
- **DT330 (1)+(S):** a közös lánc (a #128 fájljai nem változnak), Sonnet.
- **DT335 (3):** a sigla-tábla gépi javaslatát (`allapot = javaslat`) a felhasználó hagyja jóvá; csak a `besorolt` sor kötelező
  (16. kapu).
- **DT336 (2):** prompt `forditas/prompt_v5_1.md` (a `thayer_jelolt/forditas.py` `PROMPT_UT`-ja).
- **DT333 (2):** a forrásszöveg a javított nézet (`thayer_bemenet.szakaszok`, `adat/thayer_forras_javitas.tsv`).

## 2. Hatókör

**Benne van:** a sigla-jóváhagyás átvezetése (1. lépés); a futás listája; a lista Strongjainak szakaszonkénti fordítása, kapuzása,
rögzítése és beírása; a régi `teljes` sorok jelölése; mérés és napló.

**Nincs benne:** a teljes Thayer (#7, D46); a #132 eszközeinek, tábláinak és a `prompt_v5_1.md`-nek a módosítása (hiba esetén
megállás, tétel a `DONTESEK.md`-be); a `kezi` jóváhagyás (a felhasználóé, DT290 (3)); a #131 render.

## 3. Lépések (⛔ a kötelező megállások)

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév vs. `modell: sonnet`; eltérésnél nincs munka.
1. **⛔ Előfeltétel — a sigla-jóváhagyás.** Ha a felhasználó a `adat/thayer_sigla.tsv` `javaslat` sorait (a jóváhagyási lista:
   `naplok/F132_THAYER_SZAKASZ_naplo.md` F132.13) még nem hagyta jóvá, megállás (`dontesre_var`). A jóváhagyott sorok `allapot =
   besorolt`, a `besorolas_proveniencia` a jóváhagyás forrásával (`forras=manual — felhasználói jóváhagyás (chat, <dátum>)`); a
   módosított sorok átvezetése írás előtt összevetve (csak a kézi oszlopok változnak), utána `sigla_gyujt.py --ellenoriz` azonos.
2. **A futás listája** (DT332): `python eszkozok/thayer_jelolt/forditas.py lista --ki <scratchpad>/m3_lista.tsv` — a lista és a
   kihagyottak okkal a naplóba (proveniencia-sorral).
3. **Strongonként** (a lista `forditando` sorai; egy Strong = egy adag = egy commit):

   ```
   python eszkozok/thayer_jelolt/forditas.py elokeszit <STRONG> --mappa <scratchpad>/m3
   #   a <STRONG>_c<i>_prompt.md fordítása (csoportonként), a helyőrzős vázlat: <scratchpad>/m3/<STRONG>_vazlat.txt
   python eszkozok/thayer_jelolt/forditas.py ellenoriz <STRONG> --be <vázlat> --mappa <scratchpad>/m3 --ki <végleges>
   python eszkozok/thayer_jelolt/forditas.py rogzit <STRONG> --be <végleges> --allapot sonnet --modell <a saját tényleges modellnév>
   python eszkozok/thayer_jelolt/forditas.py beir <STRONG> --allapot sonnet --regi-elavult      # nem kezi régi sor (DT329 (i))
   python eszkozok/thayer_jelolt/forditas.py beir <STRONG> --allapot sonnet --kezi-marad        # kezi régi sor (DT329 (ii))
   ```

   Kapubukásnál egy önújrapróba, utána a Strong a `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`-be kerül (okkal), és a futás a következő
   Stronggal folytatódik. A `modell` mező a saját környezetből vett tényleges név. A `beir` írás előtt összevet: csak új sor, a régi
   `teljes` sor jelölése a fenti szerint, minden más sor bájtra azonos.
4. **Mz:** a lista újrafuttatása (a fordított Strongok `kesz`); mérés a naplóba (Strongonként szakasz, csoport, kapueredmény,
   önújrapróba, bukott; a G1941 motívumhelyeinek jelentéspontja a magyar szövegben); `python eszkozok/ellenoriz.py` (SÉRTÉS 0),
   `python eszkozok/feladatok.py ellenoriz` (0 hiba), a `eszkozok/thayer_jelolt/teszt_*.py` és a `eszkozok/teszt_forditas_kapuk.py`.

⛔ Megállás minden tartalmi kérdésnél (pl. a 16. kapu tartós bukása egy jóváhagyott sigla miatt; a lánc hibája): tétel a
`DONTESEK.md`-be, a #132 eszközei nem módosulnak e feladatban.

## 4. Elfogadási feltételek

1. A futás listájának minden `forditando` Strongja vagy a `forditasok.tsv`-ben (minden szakasza `sz<n>` sorral, a gátoló kapukon
   átment), vagy a `bukottak.tsv`-ben okkal; a kihagyottak okkal a naplóban.
2. A régi `teljes` sorok a DT329 (i)/(ii) szerint; minden más `forditasok.tsv`-sor bájtra változatlan.
3. A `modell` mező a tényleges modellnév; proveniencia minden lekérdezésből származó állítás mellett; hiány explicit.
4. A TSV-ket `split('\t')` olvassa és `'\t'.join()` írja (a `csv` modul tilos).
5. `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba; a tesztek zöldek.

## 5. Döntésnapló

| Azonosító | Kérdés | Állapot |
|---|---|---|
| DT334 | az M3 indítása | eldöntve: (1) külön brief, `modell: sonnet` (felhasználó, 2026-10-25) |
| DT329, d, h, i, j, k | l. 1. | eldöntve (felhasználó, 2026-10-25; `DONTESEK.md`) |
| sigla-jóváhagyás | a 91 `javaslat` sor | eldöntve: jóváhagyva, `Sir.` → `Sirák` (felhasználó, chat, 2026-10-26); átvezetés: F142.1 |
