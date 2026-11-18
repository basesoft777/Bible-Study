# Az emberi validáció letétjének lekötése

GENERÁLT: eszkozok/karoli_strong_validacio_minta.py — kézzel szerkeszteni tilos.

**Állapot: VÉGLEGES** — ez a kiküldött minta.

A minta (`minta.tsv`, a rétegjelöléssel), a csalik listája (`F175V_csalik.tsv`, a titkos maggal) és az ellenőrző oldal (`ellenorzo.html`) a validáció lezárásáig a repón kívüli letétben áll, mert a repó nyilvános. Itt csak az SHA-256-juk szerepel, előzetes lekötésként; a lezárás után a fájlok a letétbe kerülnek, és ezzel ellenőrizhetők.

| fájl | SHA-256 |
|---|---|
| `minta.tsv` | `03178b5a57312d7f3dcdcb7d0f8038643600d214e4faa051ff0926e27c75868e` |
| `F175V_csalik.tsv` | `0ac4c70c02d63986c6492756f6f895ecf8fb09aad81ce9e8a904a86167de3538` |
| `ellenorzo.html` | `bd6a73151014388969658dee68e17d266a490d826a2100b23cb8e7a0cb3b1eb4` |
| `ellenorzo_masodik.html` | `c6de39ebea7f2ef0d3c0053e876b963c4fe1ecaf4a1c480aa1ced6f59b96c155` |
| `harom_biralo_itelet.tsv` | `e236146d9f13a08e31427f95ccdbb692bfb3f102964f53184517fc8f083f28b7` |
| `proba.tsv` | `8c794b379f30e568289c70c43318a98eb988a41619ba338d0edb5939aaefe736` |
| `UTMUTATO.md` (a repóban) | `36fd0a1e004f0b97b4ee3a7ebdcd2aa28120e396259782d925ce2f9b2aeffc0c` |
| `UTMUTATO.pdf` (a repóban) | `4817549fe872e0cbee5e04946fcfe5c6e18f6d20f8bdbeaa23fb3b3f477d04fc` |

**Az online felület (F175.V21).** A kiküldött felület a Cloudflare Worker: a tételeket a linkbeli tokenre a D1 adatbázisból adja, minden választ azonnal ment (append-only napló). A Worker kódja és a tétel nélküli oldal a repóban áll; a tételek a letétből töltődnek a D1-be (`eszkozok/karoli_strong_validacio_d1.py`), és a betöltő a tételek kanonikus JSON-ját az itt lekötött SHA-256-tal veti össze. A próbatételek (`proba.tsv`) a mintán kívüli párok, a próba ítéletei a kiértékelésbe nem kerülnek.

| online felület | SHA-256 |
|---|---|
| `public/index.html` (a tétel nélküli oldal, a repóban) | `2cf5fd71a7cb9e4c8ebd66302365fc2a32399cd2c1a75b0709b19b8207b081dc` |
| `src/logika.js` (a Worker, a repóban) | `ef6fc8e159ca06f7d6172ee124073335f896df4f9333a7a7a784221b4d9c82f2` |
| `schema.sql` (a D1 sémája, a repóban) | `216b27a0020599993e82a5755c67fd62d6ef10ede10242d3ee8c35c6496ac7e1` |
| a külső ellenőr tételei (568; az `oldal_adat` kanonikus JSON-ja) | `6be449ec093c2e0db603ef12952ea284fa6b79f1520ad1c66c4a41dbae7b33dd` |
| a második ítélő tételei (311) | `073132d6015bc8654f6260067a019078d6ecb6054c0593414e3257ffde81e1cc` |
| a próbatételek (10) | `2aab6e57b0567a85cfd97752b6b51fd138eb018e4236142f2e24141964626b9a` |

Tételszám rétegenként: alapminta-pár 300, túlminta 68, nehéz réteg 45, pár nélküli magyar szó 80, kimaradt pár 55, csali 20, összesen 568, a második ítélő oldalán 311.

A minta alapja: a minta 413 valódi párjából 413 megvan a nyílt mag 1.0-s exportjában (`nyilt_karoli_strong/data/parok/`, a Zenodo 1.0 tartalma; kiadás: 2026-11-01-23fa739286662953; verzió-DOI: 10.5281/zenodo.24141884, concept DOI: 10.5281/zenodo.24141883).

*Proveniencia (verzió-DOI): scope=Zenodo-rekord lekérdezése (version 1.0, publikálva 2026-11-15) | forras=zenodo.org/api/records/24141884 | ts=2026-11-17.*
