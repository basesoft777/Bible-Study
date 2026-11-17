# Az emberi validáció letétjének lekötése

GENERÁLT: eszkozok/karoli_strong_validacio_minta.py — kézzel szerkeszteni tilos.

**Állapot: IDEIGLENES** — nem kiküldhető; a végleges húzás a gépi bírálók fagyasztott táblája után készül (`--vegleges`).

A minta (`minta.tsv`, a rétegjelöléssel), a csalik listája (`F175V_csalik.tsv`, a titkos maggal) és az ellenőrző oldal (`ellenorzo.html`) a validáció lezárásáig a repón kívüli letétben áll, mert a repó nyilvános. Itt csak az SHA-256-juk szerepel, előzetes lekötésként; a lezárás után a fájlok a letétbe kerülnek, és ezzel ellenőrizhetők.

| fájl | SHA-256 |
|---|---|
| `minta.tsv` | `203fd845a15b3ce9e7f2795b3125c8f6417d656f388d2db7639ad659762c60f3` |
| `F175V_csalik.tsv` | `c5840b48602220e8b6604e982ae3627ab87bddd3689e02f21fc2eadababd3eff` |
| `ellenorzo.html` | `daac854c872660931b06b3f547df658eb57e0dc6f571c7781776ee411584e70b` |
| `ellenorzo_masodik.html` | `e8fa636a1de4b0c69abfb4b8979727f2ecc834fcb37cc449d89e6ccd7253ddc0` |
| `UTMUTATO.md` (a repóban) | `1e73d3a90822623997adf6ad3ccfaf18f704d63ea6c6113aa146c1959dbe9637` |
| `UTMUTATO.pdf` (a repóban) | `00e12270e5e2fdedfc4fca21b0bd0c3bc0bd8a9edad5d949174fc8c8df4a0e4b` |

Tételszám rétegenként: alapminta-pár 300, túlminta 56, nehéz réteg 45, pár nélküli magyar szó 80, kimaradt pár 55, csali 20, összesen 556, a második ítélő oldalán 311.

A minta alapja: a minta 401 valódi párjából 401 megvan a nyílt mag 1.0-s exportjában (`nyilt_karoli_strong/data/parok/`, a Zenodo 1.0 tartalma; kiadás: 2026-11-01-23fa739286662953).
