# Az emberi validáció letétjének lekötése

GENERÁLT: eszkozok/karoli_strong_validacio_minta.py — kézzel szerkeszteni tilos.

**Állapot: VÉGLEGES** — ez a kiküldött minta.

A minta (`minta.tsv`, a rétegjelöléssel), a csalik listája (`F175V_csalik.tsv`, a titkos maggal) és az ellenőrző oldal (`ellenorzo.html`) a validáció lezárásáig a repón kívüli letétben áll, mert a repó nyilvános. Itt csak az SHA-256-juk szerepel, előzetes lekötésként; a lezárás után a fájlok a letétbe kerülnek, és ezzel ellenőrizhetők.

| fájl | SHA-256 |
|---|---|
| `minta.tsv` | `03178b5a57312d7f3dcdcb7d0f8038643600d214e4faa051ff0926e27c75868e` |
| `F175V_csalik.tsv` | `0ac4c70c02d63986c6492756f6f895ecf8fb09aad81ce9e8a904a86167de3538` |
| `ellenorzo.html` | `4fdc9863d9541f8ed176da426ec567c3fcf050ed54e0f38066791d5ceeba75f8` |
| `ellenorzo_masodik.html` | `d32bc4db7adef54f3d2aa4c50e80283ba3e0a461eeb547668f978a375b04251c` |
| `harom_biralo_itelet.tsv` | `e236146d9f13a08e31427f95ccdbb692bfb3f102964f53184517fc8f083f28b7` |
| `proba.tsv` | `8c794b379f30e568289c70c43318a98eb988a41619ba338d0edb5939aaefe736` |
| `UTMUTATO.md` (a repóban) | `eb354eeebf639fec373e40738f95a45bd8b0d7dac05c5033e768b3770055ce8c` |
| `UTMUTATO.pdf` (a repóban) | `20db107047b14433c5cc3d6b64163131d27a4493ddc7ef9abfddda46d550f38f` |

**Az online felület (F175.V21).** A kiküldött felület a Cloudflare Worker: a tételeket a linkbeli tokenre a D1 adatbázisból adja, minden választ azonnal ment (append-only napló). A Worker kódja és a tétel nélküli oldal a repóban áll; a tételek a letétből töltődnek a D1-be (`eszkozok/karoli_strong_validacio_d1.py`), és a betöltő a tételek kanonikus JSON-ját az itt lekötött SHA-256-tal veti össze. A próbatételek (`proba.tsv`) a mintán kívüli párok, a próba ítéletei a kiértékelésbe nem kerülnek.

| online felület | SHA-256 |
|---|---|
| `public/index.html` (a tétel nélküli oldal, a repóban) | `1d5282de1d7451d84aea9a01ba7fbfe5e08cacf2064ec5db10a3d7f22ccc01ff` |
| `src/logika.js` (a Worker, a repóban) | `098e8187f80a1a83e79f66418afba92cd816a4f23ec0d22ce4418393096d734d` |
| `schema.sql` (a D1 sémája, a repóban) | `216b27a0020599993e82a5755c67fd62d6ef10ede10242d3ee8c35c6496ac7e1` |
| a külső ellenőr tételei (568; az `oldal_adat` kanonikus JSON-ja) | `e9130179028440f255cc40d0f49c74d1c5475fdb3057e61e0fa80017d64fefd2` |
| a második ítélő tételei (311) | `c83984bc9d28451068abf2e72bf837b632abac4230fc0fac162172c90c14c3d0` |
| a próbatételek (10) | `47260a1168fa53136da9594198809f16a3820043d76855e941e3d56d6199b77e` |

Tételszám rétegenként: alapminta-pár 300, túlminta 68, nehéz réteg 45, pár nélküli magyar szó 80, kimaradt pár 55, csali 20, összesen 568, a második ítélő oldalán 311.

A minta alapja: a minta 413 valódi párjából 413 megvan a nyílt mag 1.0-s exportjában (`nyilt_karoli_strong/data/parok/`, a Zenodo 1.0 tartalma; kiadás: 2026-11-01-23fa739286662953; verzió-DOI: 10.5281/zenodo.24141884, concept DOI: 10.5281/zenodo.24141883).

*Proveniencia (verzió-DOI): scope=Zenodo-rekord lekérdezése (version 1.0, publikálva 2026-11-15) | forras=zenodo.org/api/records/24141884 | ts=2026-11-17.*
