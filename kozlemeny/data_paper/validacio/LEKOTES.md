# Az emberi validáció letétjének lekötése

GENERÁLT: eszkozok/karoli_strong_validacio_minta.py — kézzel szerkeszteni tilos.

**Állapot: VÉGLEGES** — ez a kiküldött minta.

A minta (`minta.tsv`, a rétegjelöléssel), a csalik listája (`F175V_csalik.tsv`, a titkos maggal) és az ellenőrző oldal (`ellenorzo.html`) a validáció lezárásáig a repón kívüli letétben áll, mert a repó nyilvános. Itt csak az SHA-256-juk szerepel, előzetes lekötésként; a lezárás után a fájlok a letétbe kerülnek, és ezzel ellenőrizhetők.

| fájl | SHA-256 |
|---|---|
| `minta.tsv` | `03178b5a57312d7f3dcdcb7d0f8038643600d214e4faa051ff0926e27c75868e` |
| `F175V_csalik.tsv` | `0ac4c70c02d63986c6492756f6f895ecf8fb09aad81ce9e8a904a86167de3538` |
| `ellenorzo.html` | `16ee1d16a0b710b3986c5c31a61664e5f7511b0eea57dd09b590333f6de5128d` |
| `ellenorzo_masodik.html` | `1d42beee3bc1d318d39a6b031617315f10557c872df07b677c6ecbea3f0fba7b` |
| `harom_biralo_itelet.tsv` | `e236146d9f13a08e31427f95ccdbb692bfb3f102964f53184517fc8f083f28b7` |
| `proba.tsv` | `8c794b379f30e568289c70c43318a98eb988a41619ba338d0edb5939aaefe736` |
| `UTMUTATO.md` (a repóban) | `4775a7a84e57585d918bf4aae7e908d49000ab7235d0729169a05c44c708c21c` |
| `UTMUTATO.pdf` (a repóban) | `d553175579dc3445ece777fe80e44942d99db24e2402571676aa9d339a496f28` |

**Az online felület (F175.V21).** A kiküldött felület a Cloudflare Worker: a tételeket a linkbeli tokenre a D1 adatbázisból adja, minden választ azonnal ment (append-only napló). A Worker kódja és a tétel nélküli oldal a repóban áll; a tételek a letétből töltődnek a D1-be (`eszkozok/karoli_strong_validacio_d1.py`), és a betöltő a tételek kanonikus JSON-ját az itt lekötött SHA-256-tal veti össze. A próbatételek (`proba.tsv`) a mintán kívüli párok, a próba ítéletei a kiértékelésbe nem kerülnek.

| online felület | SHA-256 |
|---|---|
| `public/index.html` (a tétel nélküli oldal, a repóban) | `6ecb95e823ce2449c0b02087074d77b98770e31571e52a88cc3a9e973a46eaa1` |
| `src/logika.js` (a Worker, a repóban) | `ac0c1a0fd0202fb981bfde975585d8297aae96b53dcc661d301c10cc28a982b4` |
| `schema.sql` (a D1 sémája, a repóban) | `216b27a0020599993e82a5755c67fd62d6ef10ede10242d3ee8c35c6496ac7e1` |
| a külső ellenőr tételei (568; az `oldal_adat` kanonikus JSON-ja) | `6be449ec093c2e0db603ef12952ea284fa6b79f1520ad1c66c4a41dbae7b33dd` |
| a második ítélő tételei (311) | `073132d6015bc8654f6260067a019078d6ecb6054c0593414e3257ffde81e1cc` |
| a próbatételek (10) | `2aab6e57b0567a85cfd97752b6b51fd138eb018e4236142f2e24141964626b9a` |

Tételszám rétegenként: alapminta-pár 300, túlminta 68, nehéz réteg 45, pár nélküli magyar szó 80, kimaradt pár 55, csali 20, összesen 568, a második ítélő oldalán 311.

A minta alapja: a minta 413 valódi párjából 413 megvan a nyílt mag 1.0-s exportjában (`nyilt_karoli_strong/data/parok/`, a Zenodo 1.0 tartalma; kiadás: 2026-11-01-23fa739286662953; verzió-DOI: 10.5281/zenodo.24141884, concept DOI: 10.5281/zenodo.24141883).

*Proveniencia (verzió-DOI): scope=Zenodo-rekord lekérdezése (version 1.0, publikálva 2026-11-15) | forras=zenodo.org/api/records/24141884 | ts=2026-11-17.*
