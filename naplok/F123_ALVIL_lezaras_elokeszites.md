# F123 — az ALVIL-001 lezárásának előkészítése (X.Z, a felhasználótól független rész)

*2026-11-02 · modell: claude-opus-5-5 · ág: claude/f123-alvil-lezaras-099225 · menet: DT497 (1), `MUNKAMENET.md` C-h → C-l → C5*

A határ-ellenőrzést (C-h) a felhasználó indítja (DT-F151b), a lektor-felületen a döntések az övéi (C-l); ez a menet
egyiket sem indította. A C5 (1. kiadás sora, verzió-emelés, a brief lezárása) a határ- és a lektori kapu után jön, új
menetben.

## Feed kapunként (`python eszkozok/muhely_allapot.py --motivum ALVIL-001 --nincs-gh`)

| # | Kapu | Előtte | Utána | Mi történt / mire vár |
|---|---|---|---|---|
| 1 | szabály-ellenőrzés | zöld | zöld | — |
| 2 | CI-ellenőrzés | zöld (290 jelentés) | zöld (288 jelentés) | — |
| 3 | nulla-diff újragenerálás | zöld | zöld | — |
| 4 | nincs nyitott jelölt | zöld | zöld | — |
| 5 | határ: 0 nyitott kérdés | nincs mérő | nincs mérő | **a felhasználóra vár**: `naplok/HATAR_ALVIL-001.md` (C-h: `motivum_hatar.py` + `hatar-ellenor`) |
| 6 | olvasói blokkok, kiejtés, fordítás | piros (kiejtés-hiány 4) | **zöld** | F123.ALVIL.Z1: a kézi forrás négy görög szava kiejtéssel (ἄβυσσος *abüsszosz*; ᾍδης *hádész* ×3) |
| 7 | nincs nyitott lektori kérdés | nincs mérő | nincs mérő | **a felhasználóra vár**: a `naplok/LEKTOR_ALVIL-001.tsv` a `HATAR_ALVIL-001.md`-ből generálódik (`lektor_kerdesek.py`), tehát az 5. után; a döntések a lektor-felületen |
| 8 | nincs nyitott DT / ⛔ feladat | piros (#123 blokkoló) | **zöld** (0 blokkoló, 7 tájékoztató) | F123.ALVIL.Z2: DT498 (d), a `motivum_kesz` fejlécmező; a #121 megállt, de ⛔-je nem az ALVIL-001-ről szól (tájékoztató, mint eddig) |

Összesen: **4/8 → 6/8**.

## Az M4 hiánylista (`naplok/F123_M4_ALVIL-001.md`, 3. kör utáni állapot)

| Tétel | Állapot (mért, 2026-11-02) |
|---|---|
| TBESG G0086 2. szakaszának fordítása (#121) | **kész**: `adat/forditasok.tsv` `TBESG G0086 G0086 2 forditas_hu` (F121.18, 500855b6); a lapon „(fordításra vár)” 0 cella (a 6. kapu 0-t mér) |
| 2 „Seól” a `motivum_kapcsolatok.tsv` ISTENTISZT-001-gyel közös soraiban | **kész**: „Seolban” (358d0819, az ISTENTISZT-001 arany lap 12–14. szerepe, DT26); a lapon „Seól” 0 |
| a `jeloltek.tsv` régi ALVIL-001 sorainak „Seól”-ja | **teendő nincs**: 58 sor, mind az `indoklas` mezőben (+1 `cel_alpont`); a lapra nem renderelődik (a lapon 0 „Seól”), a DT422 hatóköre a lap adatmezői voltak; a döntési indoklás utólag nem írandó át |
| MCGED G0086 glossza | jelölt hiány marad (DT235), nem kapu |

*(proveniencia: scope=ALVIL-001 | forras=eszkozok/muhely_allapot.py --motivum ALVIL-001 --nincs-gh (repón kívüli kimenet, feed_belso.json), adat/jeloltek.tsv split('\t'), grep lexikon/ALVIL-001_TUDOMANYOS.md | ts=2026-11-02)*
