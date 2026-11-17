# Az emberi validáció letétjének lekötése

GENERÁLT: eszkozok/karoli_strong_validacio_minta.py — kézzel szerkeszteni tilos.

**Állapot: IDEIGLENES** — nem kiküldhető; a végleges húzás a gépi bírálók fagyasztott táblája után készül (`--vegleges`).

A minta (`minta.tsv`, a rétegjelöléssel), a csalik listája (`F175V_csalik.tsv`, a titkos maggal) és az ellenőrző oldal (`ellenorzo.html`) a validáció lezárásáig a repón kívüli letétben áll, mert a repó nyilvános. Itt csak az SHA-256-juk szerepel, előzetes lekötésként; a lezárás után a fájlok a letétbe kerülnek, és ezzel ellenőrizhetők.

| fájl | SHA-256 |
|---|---|
| `minta.tsv` | `7a7ca9659ea3a8faee5320e30655864744afe535c1ad665fc859db008036414e` |
| `F175V_csalik.tsv` | `c5840b48602220e8b6604e982ae3627ab87bddd3689e02f21fc2eadababd3eff` |
| `ellenorzo.html` | `cdf71a07a7969a03836cf366fd349080adc8ba05512d2882e4e32df2a3c08d5e` |
| `ellenorzo_masodik.html` | `92dd30e1402344dac12e003f275ee1a36a960eea7215a20e46bfd3765bc59de1` |
| `UTMUTATO.md` (a repóban) | `1ccdf42911ff3b4fe25f7cd3309cb9bc22227f9df42823e85fa93cadfcd8d757` |
| `UTMUTATO.pdf` (a repóban) | `81a9efc7d28425e9c2279262d9782934ad062936cf24a6cb6c2224e0e4430347` |

Tételszám rétegenként: alapminta-pár 300, túlminta 56, nehéz réteg 45, pár nélküli magyar szó 80, kimaradt pár 55, csali 20, összesen 556, a második ítélő oldalán 443.

A minta alapja: a minta 401 valódi párjából 401 megvan a nyílt mag 1.0-s exportjában (`nyilt_karoli_strong/data/parok/`, a Zenodo 1.0 tartalma; kiadás: 2026-11-01-23fa739286662953).
