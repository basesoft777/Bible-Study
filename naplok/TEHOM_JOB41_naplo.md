# TEHOM_JOB41_naplo.md — F109: a TEREMT-001 Jób 41:32 jelölt elbírálása

*2026.10.19 · modell: claude-sonnet-5-5 · forrás: DT184, F108 újrascan*

## Lekérdezés
- `python eszkozok/lekerdez.py scan H8415` → 35 igehely, 36 szó-előfordulás; a Jób 41:32 benne van.
  `proveniencia: scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H8415 | n=35 | ts=2026-10-19T09:56Z`
- `python eszkozok/lekerdez.py karoli "Jób 41:32"` → Károli 1908: „Maga után világos ösvényt hagy, azt hinné valaki, a tenger megőszült.”
  `proveniencia: scope=range:Jób 41:32 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=1 | ts=2026-10-19T09:57Z`
- TAHOT-sor: `H8415 תְּה֣וֹם te.Hom „abyss” / „[the] deep”` (a Jób 41:32 a Károli-vers kulcs; az MT-szám 41:24).

## Elbírálás
- **Negatív kritérium** (motivumok.tsv): az igehelynek a תְּהוֹם gyököt kell tartalmaznia. **Teljesül**: a lexéma szó szerint áll a versben (a gerinc-elem H8415), nem csak tematikus vízkép.
- **Hígulás-próba** (fölérendelt fogalom: vízi/kozmikus káosz-képzetek): a hely nem a fölérendelt fogalmon át tartozik ide, hanem lexikai alapon.
- **Funkció** (CLAUDE.md, 3. kérdés): a Leviatán nyomában „megőszülő” mélység, hasonlat; költői-leíró funkció, rokon a Jób 38:16, 38:30 és Ez 31:4 helyekkel. Nem tér el a motívum többi helyétől, így a brief 4. lépésének ⛔-je nem él; DT-F109a nem keletkezett.
- **Károli-szó:** „a tenger”. A Károli a tehómot tengernek fordítja (mint Zsolt 33:7 „hullámokat”, Zsolt 107:26 „fenékig”); a Károli-szóalak önmagában nem azonosítja a lexémát, a TAHOT igen. Azonosítás módja: `tartalom-alapú` (a Károli-szöveg olvasásával, nem #22 gépi párosításból), megbízhatóság `magas`.

## Döntés
`beépítve`. Írás:
- `adat/jeloltek.tsv`: a `TEREMT-001 | Jób 41:32` sor `dontes` = `beépítve`, indoklás, `karoli_szo`, `azonositas_modja`, `megbizhatosag`, `datum` kitöltve; a `forras_kereses` változatlan; minden más sor bájtra azonos.
- `adat/elofordulasok.tsv`: +1 sor (`gerinc_elem` = H8415, a scan proveniencia-sorával, `igazolas` = `TAHOT-igazolt`); minden más sor azonos.

## Nem része (külön `ertelmezo` tétel, DT-F32b szerinti modellel)
A `tematikus_lezart/Tehom_tematikus.md` 35-ös előfordulás-számot és a Jób-helyek táblázatát idézi; a Jób 41:32 felvétele után 36 szó-előfordulás / 35 igehely a mai scan szerint. A tanulmány és a lexikon nem módosult.
