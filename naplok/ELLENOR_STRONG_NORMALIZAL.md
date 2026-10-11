# ELLENŐR — F62_STRONG_NORMALIZAL_BRIEF.md · origin/main...HEAD (F62.0–F62.4, 1d2d4641)

*A jelentést a `fuggetlen-ellenor` subagent adta (nem volt fájlíró eszköze); a fő session írta ki, tartalmilag változatlanul, tömörítve. A subagent nem futtathatta a teszteket, a `ellenoriz.py`-t és a `betolt.py`-t: ezek NEM ELLENŐRIZHETŐ eredményt kaptak. Az ág le van maradva a main mögött (közös ős 77894663); az ág saját munkája a hárompontos diff, 8 fájl.*

**Összegzés: ELTÉRÉS: 6 tétel**

## Eltérések (súlyossági sorrendben)

1. **K2 / DT-F62a — érvényes ötjegyű TAGNT-kulcsok lekérdezhetetlenek.** `lekerdez.py scan G20447` és `igealak G20833` hibával (exit=1) áll meg ("négynél több érvényes számjegyet …"; a javasolt H0779 alak G-kódnál nem elérhető). A `TAGNT_kivonat.tsv`-ben ezek valódi kulcsok: ApCsel 24:12 és 2Kor 11:28 (`G20447`), 1Thessz 2:8 (`G20833`). A régi kód ezekre 2, ill. 1 találatot adott. Érvényes adatkulcson bekövetkezett viselkedésváltozás, amelyet a DT-F62a kivétele nem fed; a zárás nem említi. (`eszkozok/lekerdez.py:40-60`, `eszkozok/strong_util.py:57-58`)
2. **K2 / DT-F62a — `domen`.** `domen H779` hiba nélkül `n=0`-t ad (néma nem-találat marad), `domen H0779` 2 egységet. A `_anomaly_part_matches` saját Strong-normalizálást végez (`lekerdez.py:561-606, 631`), ami ütközik a „csak a közös függvény” kitétellel.
3. **K4** — a független ellenőr nem zár eltérés nélkül (ez a jelentés).
4. **K3 / A1 — az M0 mérése nem reprodukálható.** A mérőszkript a scratchpadről futott, nincs a repóban, proveniencia-sor nélkül; a „0 eltérés” hatóköre (csak a SEMA-Strong-oszlopok; a forditasok/lexikon_hivatkozasok forrásalakot tartó oszlopaiban 113 nullázatlan találat áll) nincs kimondva (`naplok/STRONG_NORMALIZAL_M0.md:3, 62-66`).
5. **K2 / `betolt.py` stderr-figyelmeztetés** (nem SEMA-alakú study-érték, `betolt.py:110-115`) a DT-F62a-ban nem szerepel; jóváhagyandó vagy a K2-be veendő. Valós eset: `genezis/1Moz_16_bovitett.md` 52–53. sor (`H410+H7210`, `H883`).
6. **M3 / zárás** pontatlan és hiányos: nem említi az 1. és 2. tételt; „49 Strong-oszlop” ≠ az M0 „11 oszlop + 38 fájl” megfogalmazása.

## OK

K2 (`scan`/`igealak`/`kollokacio` nullázatlan bemenet: hiba a helyes alakkal; `scan H0779` 52 igehely, az M0-val egyező); `lxx_hid` strong_alak (a `LXX_OS/`-ban 0 kimenet-eltérés); `betolt.py` csak a közös függvényt hívja; K1 alaklefedés (21 teszt, idempotencia); kódolási őr az importok után; K3 (adattábla nem változott, minden `adat/`/`konkordancia/` TSV Δ=0); DT-F62a helyőrző-alakú; nincs végleges DT/N szám az ágon; ⛔ betartva (F62.1 megállás → F62.2 elfogadás → F62.3); E2–E26 CI a közös ősből EXIT=0 (a `--diff-alap origin/main` E5 hibája az ág lemaradásából ered).

## NEM ELLENŐRIZHETŐ

`teszt_strong_util.py`, `teszt_lekerdez_sir.py`, `ellenoriz.py` futtatása; `betolt.py` bájtazonosság (a 24 lekérdezés a végrehajtó jelentésére támaszkodik).
