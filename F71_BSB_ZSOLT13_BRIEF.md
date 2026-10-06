---
feladat: 71
cim: Zsolt 13 kézi versmegfeleltetése a BSB-importban (DT-F41a)
kod: BSB_ZSOLT13
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: lezarva
pr: 226
lezarva_osszegzes: "Zsolt 13 MT 3–6 importálva kézi kivétellel (41 sor, nulladiff 0); MT 1–2 forráshiány, N50"
ad: a Zsolt 13 importálva a BSB_Strongs.tsv-be a DT-F41a listája szerint (felirat → MT 1, 1 → 2, 2 → 3, 3 → 4, 4 → 5, 5+6 → 6); a sorok `manual` provenienciával, kézi kivételként jelölve; az `illesztetlen` állapot `kezi`
kovetkezo: "független ellenőrzés (fuggetlen-ellenor), majd merge a felhasználótól; a Zsolt 13 MT 1–2 (felirat, BSB 13:1) a display-JSON hiánya miatt nem importálható"
ag: claude/bsb-zsolt13
olvas: [naplok/F16_bsb_zsolt_megfeleltetes.tsv, konkordancia/TAHOT_kivonat.tsv, eszkozok/fj2/]
ir: [naplok/ELLENOR_F71.md, naplok/F71_zaras.md, adat/datasetek.tsv, adat/SEMA.md, NYITOTT_FELADATOK.md, konkordancia/BSB_Strongs.tsv, konkordancia/README.md, eszkozok/fj2/bsb_import.py, naplok/F16_bsb_zsolt_megfeleltetes.tsv, naplok/F16_bsb_lefedettseg.tsv, naplok/F41_bsb_megfeleltetes.tsv, naplok/F41_nem_egyezo_versek.tsv, naplok/F71_nulladiff.txt]
fugg: [41]
---

# F71_BSB_ZSOLT13_BRIEF.md

*v1 · 2026.10.06 · FELADATOK #71 · forrás: `DONTESEK.md` DT-F41a 🟢; KONZISZTENCIA_20261006 1.6 (a döntés alkalmazása lezárt feladatra, a #41-re volt bízva)*

## Cél

A #41 a Zsolt 13-at belső versosztás-eltérés miatt kihagyta a mérésből és az importból (DT6 (g), „Belső versosztás-eltérés (F16.11)”). A DT-F41a eldöntötte: kézi megfeleltetés, a teljes listával. Ez a feladat alkalmazza a döntést.

## A döntés (DT-F41a, szó szerint alkalmazandó)

| BSB | MT |
|---|---|
| felirat (`bsb_d_cim`) | 1 |
| 1 | 2 |
| 2 | 3 |
| 3 | 4 |
| 4 | 5 |
| 5 + 6 | 6 |

Az új sorok `manual` provenienciát kapnak, kézi kivételként jelölve. A fejezet `illesztetlen` állapota `kezi` lesz. Precedens: az 1Kir 22:43 kézi osztása (F41).

## Lépések

- **M0 — felmérés (csak olvas).** A `naplok/F16_bsb_zsolt_megfeleltetes.tsv` és az `illesztetlen_ok` Strong-illeszkedése alapján ellenőrizd, hogy a lista minden sora alátámasztott-e. Pontosítsd az `ir` listáját (melyik fájl hordozza az `illesztetlen` → `kezi` állapotot). ⛔, ha bármelyik sor ellentmond a mérésnek: ilyenkor `DT-F<nn>` tétel, megállás.
- **M1 — megfeleltetés.** A kézi megfeleltetés felvétele a `bsb_import.py` kézi kivételei közé, az 1Kir 22:43 mintájára.
- **M2 — import.** A `BSB_Strongs.tsv` kiegészítése a Zsolt 13 soraival; a 7. oszlop (`Számozás`) `mt`.
- **M3 — nulladiff.** A Zsolt 13-on kívül a `BSB_Strongs.tsv` bájtra változatlan (a `bsb_nulladiff.py` mintájára).
- **M4 — lezárás.** `naplok/F16_bsb_lefedettseg.tsv` és `konkordancia/README.md` frissítése; a saját fejléc lezárása.

## Nem tartozik ide

- A 2Sám, Ezsd, Dán kimaradása (DT6 (c), (d)).
- A #41 újranyitása.

## Elfogadási feltételek

- A Zsolt 13 hat MT-verse a `BSB_Strongs.tsv`-ben, `manual` provenienciával és kézi kivétel jelöléssel.
- A nulladiff a többi sorra 0.
- `python eszkozok/feladatok.py ellenoriz` 0.
