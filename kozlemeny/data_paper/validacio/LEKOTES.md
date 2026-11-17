# Az emberi validáció letétjének lekötése

GENERÁLT: eszkozok/karoli_strong_validacio_minta.py — kézzel szerkeszteni tilos.

**Állapot: VÉGLEGES** — ez a kiküldött minta.

A minta (`minta.tsv`, a rétegjelöléssel), a csalik listája (`F175V_csalik.tsv`, a titkos maggal) és az ellenőrző oldal (`ellenorzo.html`) a validáció lezárásáig a repón kívüli letétben áll, mert a repó nyilvános. Itt csak az SHA-256-juk szerepel, előzetes lekötésként; a lezárás után a fájlok a letétbe kerülnek, és ezzel ellenőrizhetők.

| fájl | SHA-256 |
|---|---|
| `minta.tsv` | `03178b5a57312d7f3dcdcb7d0f8038643600d214e4faa051ff0926e27c75868e` |
| `F175V_csalik.tsv` | `0ac4c70c02d63986c6492756f6f895ecf8fb09aad81ce9e8a904a86167de3538` |
| `ellenorzo.html` | `941346053d606a8e2010abc02bc9b5782a39905cf719b7236f0e031e255cf6e9` |
| `ellenorzo_masodik.html` | `2323c4c02104be47f097c1748e32885928dc864ecb2bec86da99e9a06b589532` |
| `harom_biralo_itelet.tsv` | `e236146d9f13a08e31427f95ccdbb692bfb3f102964f53184517fc8f083f28b7` |
| `proba.tsv` | `8c794b379f30e568289c70c43318a98eb988a41619ba338d0edb5939aaefe736` |
| `UTMUTATO.md` (a repóban) | `76fd33418066ff766c5bdb9a8a8b33a4f2611b3cb395f1677ac92b6fbd9b1e41` |
| `UTMUTATO.pdf` (a repóban) | `775e8eaab3423d28f217c553426da759b47a1f4b96b65c93a95fa3d0670945c5` |

**Az online felület (F175.V21).** A kiküldött felület a Cloudflare Worker: a tételeket a linkbeli tokenre a D1 adatbázisból adja, minden választ azonnal ment (append-only napló). A Worker kódja és a tétel nélküli oldal a repóban áll; a tételek a letétből töltődnek a D1-be (`eszkozok/karoli_strong_validacio_d1.py`), és a betöltő a tételek kanonikus JSON-ját az itt lekötött SHA-256-tal veti össze. A próbatételek (`proba.tsv`) a mintán kívüli párok, a próba ítéletei a kiértékelésbe nem kerülnek.

| online felület | SHA-256 |
|---|---|
| `public/index.html` (a tétel nélküli oldal, a repóban) | `54d5e9d01fba4a5cbe75d9c6b6b10447461a5a509b9e4dfcff31f4d2a10a4ae6` |
| `src/logika.js` (a Worker, a repóban) | `ef6fc8e159ca06f7d6172ee124073335f896df4f9333a7a7a784221b4d9c82f2` |
| `schema.sql` (a D1 sémája, a repóban) | `216b27a0020599993e82a5755c67fd62d6ef10ede10242d3ee8c35c6496ac7e1` |
| a külső ellenőr tételei (568; az `oldal_adat` kanonikus JSON-ja) | `e9130179028440f255cc40d0f49c74d1c5475fdb3057e61e0fa80017d64fefd2` |
| a második ítélő tételei (311) | `c83984bc9d28451068abf2e72bf837b632abac4230fc0fac162172c90c14c3d0` |
| a próbatételek (10) | `47260a1168fa53136da9594198809f16a3820043d76855e941e3d56d6199b77e` |

Tételszám rétegenként: alapminta-pár 300, túlminta 68, nehéz réteg 45, pár nélküli magyar szó 80, kimaradt pár 55, csali 20, összesen 568, a második ítélő oldalán 311.

A minta alapja: a minta 413 valódi párjából 413 megvan a nyílt mag 1.0-s exportjában (`nyilt_karoli_strong/data/parok/`, a Zenodo 1.0 tartalma; kiadás: 2026-11-01-23fa739286662953; verzió-DOI: 10.5281/zenodo.24141884, concept DOI: 10.5281/zenodo.24141883).

*Proveniencia (verzió-DOI): scope=Zenodo-rekord lekérdezése (version 1.0, publikálva 2026-11-15) | forras=zenodo.org/api/records/24141884 | ts=2026-11-17.*
