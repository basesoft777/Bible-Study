# KAROLI_ELLENORZES M3 — ISTENTISZT-001 minta (F65.3)

*2026-10-11 · szárazon: az adatsorok még NEM változtak · proveniencia: scope=manual | forras=adat/karoli_strong/parok_1Moz.tsv, parok_2Moz.tsv, adat/elofordulasok.tsv | ts=manual (nem lekérdezés) · eszköz: `eszkozok/karoli_ellenorzes.py`*

A mintát a DT104 (4) szerint az ISTENTISZT-001 adja (az ANTROP-001-nek az 1Móz/2Móz-ben egyetlen sora van). Teljes eltéréslista: `naplok/KAROLI_ELLENORZES_elteresek.tsv`.

## 1. Az ISTENTISZT-001 mind a 32 sorának ítélete

| ítélet | bizonyossag | sor | megjegyzés |
|---|---|---|---|
| egyezik | alacsony | 12 | egyezik, de csak `alacsony` párokon (1Kir, 2Kir, Zsolt, 1Krón, Ézs, Jer): nem frissül |
| egyezik | magas | 7 | **frissíthető** (1Móz 4:26, 12:8, 13:4, 21:33, 26:25; 2Móz 33:19, 34:5) |
| nincs_par | — | 13 | Sof, Zak, Jóel (a #22 még nem párosította) és 7 NT-sor (G1941; a #22 csak az ÓSZ-t párosítja) |

Eltérő (`elter`) sor az ISTENTISZT-001-ben: **0**.

## 2. A hét frissítendő sor (azonositas_modja: `tartalom-alapú` → `szó-szintű-gépi`)

| igehely | régi karoli_szo | Strong | illesztett szavak | nem illesztett szavak | részleges |
|---|---|---|---|---|---|
| 1Móz 4:26 | segítségül hívni az Úrnak nevét | H7121+H8034 | hívni,nevét | segítségül,az,úrnak | igen |
| 1Móz 12:8 | segítségűl hívá az Úr nevét | H7121+H8034 | hívá,nevét | segítségűl,az,úr | igen |
| 1Móz 13:4 | segítségűl hívá ott Ábrám az Úrnak nevét | H7121+H8034 | hívá,nevét | segítségűl,ott,ábrám,az,úrnak | igen |
| 1Móz 21:33 | segítségűl hívá ott az örökkévaló Úr Istennek nevét | H7121+H8034 | hívá,nevét | segítségűl,ott,az,örökkévaló,úr,istennek | igen |
| 1Móz 26:25 | segítségűl hívá az Úrnak nevét | H7121+H8034 | hívá,nevét | segítségűl,az,úrnak | igen |
| 2Móz 33:19 | kiáltom előtted az Úr nevét | H7121+H8034 | kiáltom,nevét | előtted,az,úr | igen |
| 2Móz 34:5 | nevén kiáltá az Urat | H7121+H8034 | nevén,kiáltá | az,urat | igen |

Minden sorban **csak az `azonositas_modja`** változik; a `karoli_szo`, `megbizhatosag` és `proveniencia` marad (DT104 (2)). A soronkénti proveniencia-sor az `adat/karoli_variancia.tsv` `megerosites` sorában áll (`tipus=megerosites`, `id=ISTENTISZT-001`).

## 3. Amit a mintán látni kell

- Mind a 7 sor **részleges** (laza illesztés): a H7121 és a H8034 a gépi párosítás szerint a fenti két-két szóhoz tartozik; a `nem illesztett` szavaknak ezen a versen nincs H7121/H8034 párjuk. A `szó-szintű-gépi` mód így azt jelenti: *mindkét Strong megvan a vers gépi párjai között a `karoli_szo` szavain*, nem azt, hogy a teljes idézet minden szava Strong-igazolt.
- A névelők (`a`, `az`) a héberben nincsenek, ezért a legtöbb sorban a `nem_illesztett` listán állnak; ez zaj, a döntés (laza szabály) szerint listázzuk őket. Ha a névelők kihagyása kívánatos, az a `nem_illesztett` lista szűrése, nem az ítélet változása.
- 2Móz 33:19 és 34:5: a régi `karoli_szo` más szavakat tartalmaz, mint az 1Móz-i sorok (`kiáltom`, `kiáltá` a H7121 gépi párja); az ítélet itt is csak a két Strong meglétét igazolja a versben, a formula-azonosság értelmezése (a motívum-besorolás) nem tárgya ennek a tételnek.
- A 12 `egyezik`+`alacsony` sor (Zsolt 116:4, 116:13, 116:17 stb.) a #22 kétmodelles futása után ugyanezzel az eszközzel újrafuttatható.

## 4. Megjegyzés a TEREMT-001 / KIRALY-001 két eltérésére

A 2Móz 19:6 (`papok`, KIRALY-001) és a 2Móz 15:5 (`a mélységbe`, TEREMT-001) sorok `elter` ítéletűek: **nem változnak**, csak az eltéréslistán állnak kézi ítéletre (`naplok/KAROLI_ELLENORZES_elteresek.tsv`). A gépi javítás nincs.

