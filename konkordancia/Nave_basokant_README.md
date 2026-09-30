# Nave_basokant.tsv — Nave's Topical Bible (1897), témák és igehely-hivatkozások

*F18 · 2026.09.30 · állapot: **javaslat** (l. `naplok/F18_import_naplo.md`, „Küszöb”). Generált fájl: `eszkozok/nave_import.py` — kézzel nem szerkesztendő.*

## Forrás és licenc

- **Forrás:** `github.com/basokant/nave`, commit `4f35c7d4ffd4933f4db1b9d5182db90dc04bd235`, a **nyers szövegfájl** (`data/nave.txt`, sha256 `560dcb1a9cdaccd8df50ed0b714f9d380203795970de8ef79b47d1819052f43a`).
- **Nem vettük át:** a basokant szkriptjeit (`bin/parse.ts`, `bin/scrape.ts`) és a `data/parsed-nave.json`-t; a parszoló saját (`eszkozok/nave_import.py`). A `theonize/bible_database`-t (GPLv3) a DT5 döntés szerint sem a repóba, sem elemzéshez nem használtuk.
- **Licenc:** a mű (Nave, 1897) közkincs a basokant README-je szerint; **licencfájl nincs**. A repó adatfájljára külön licenc nincs deklarálva; az adat a `naves-topical-bible.com` lekaparása. Részletek: `naplok/F18_licenc.md`.
- A nyers `nave.txt` **nincs a repóban** (4,5 MB): a commit-hash és a sha256 reprodukálhatóvá teszi; a generátor `--forras <nave.txt>` paramétert kér.

## Szerkezet

Egy sor = egy hivatkozás (`kapcsolat=vers`), egy „lásd” utalás (`lasd`), vagy egy hivatkozás nélküli szövegegység (`szoveg`). A `nave.txt` hierarchiája a lekaparáskor elveszett (behúzás nincs), ezért a tábla a **forrás sorszerkezetét** őrzi, nem tulajdonít altéma-fát:

| Oszlop | Tartalom |
|---|---|
| `tema_id` | `NAVE-0001`… a fájlbeli sorrend szerint (két cím ismétlődik: `REVERENCE`, `SIN` — külön entry, külön id) |
| `tema` | az entry címe (nagybetűs, ahogy a forrásban) |
| `sor` | a sor sorszáma az entry-n belül (1-től) |
| `sor_jel` | `→` (altéma-sor) · `szam:N` (számozott jelentés) · `folyt` (jel nélküli folytatósor) |
| `tetel` | `0` = a sor feje; `1..n` = a sorban álló `<list><item>` k-adik eleme |
| `cimke` | az egység hivatkozásokat megelőző szövege (a legutóbbi nem-elválasztó szöveg) |
| `kapcsolat` | `vers` · `lasd` · `szoveg` |
| `igehely` | repó-formátum, magyar könyvrövidítéssel, **KJV-számozással** (`2Móz 6:16-20`, `Mt 5:1-7:29`, fejezet: `1Krón 24`) |
| `igehely_osis` | az eredeti `osisRef` |
| `hely_tipus` | `vers` · `tartomany` · `fejezet` · `fejezettartomany` · `konyvhatar_tartomany` · `ismeretlen_konyv` · `hibas` |
| `karoli_allapot` | egyes versekre a `Karoli_versmegfeleltetes.tsv` szerint: `azonos` · `eltero` · `tobbes` · `nincs_a_tablaban` · `ujszovetseg_nincs_tabla` (a tábla ÓSZ-i); tartományra/fejezetre `tartomany`/`fejezet`; `n.a.` |
| `igehely_karoli` | csak `eltero`/`tobbes` esetén: a Károli-igehely(ek) |
| `cel_tema` | `lasd`-nál a `Nave:` cél (a forrás `target` attribútuma) |
| `megjegyzes` | `gyanus_kijelzes:…` (a kijelzett szöveg nem szabályos hivatkozás-alak), `utotag:…` (a hivatkozás utáni szöveg), `kijelzett:…` (a „lásd” kijelzett szövege eltér a céltól), `vegyes_veg…` |

Könyvnév-konverzió: OSIS → STEPBible-rövidítés (a parszolóban) → magyar rövidítés a `Konyv_normalizalo_tabla.tsv`-ből. A 13 `ismeretlen_konyv` sor (12 × `PrAzar.1.2`, 1 × `Wis.2`) nem valódi deuterokanonikus hivatkozás: a lekaparás a névvel összeolvadt „2Ch” / könyvrövidítést értelmezte rosszul (pl. „Azariah 2Ch 31:10” → `PrAzar.1.2`); a nyers osisRef marad. A `Wis.2` kijelzése szabályosnak látszik, ezért csak `ismeretlen_konyv` jelölést kap.

## Figyelmeztetések

- A Nave-hivatkozások **KJV-számozásúak**. Az `azonos`/`eltero` csak egyes versekre és csak az ÓSZ-re ítél; a `nincs_a_tablaban` **nem** „azonos”, hanem „a tábla nem tartalmazza” (proveniencia-szabály).
- A lekaparás hibái megmaradnak, jelölve: pl. a `Son of <ref osisRef="Mic.2">Micah 2</ref>Ch 34:20` alakú hibás `osisRef` a `gyanus_kijelzes` jelölést kapja (20 sor: 12 × `PrAzar`, 1 × `Jer`, 2 × `Obad`, 5 × `Zech`: a névvel összeolvadt hibás hivatkozás). A forrást nem javítjuk; a hibás sorok az `utotag:` megjegyzésben megőrzik az elnyelt hivatkozás-töredéket.
- A hivatkozás-sorok nem szó szerinti verslisták; a tartományokat nem bontjuk versekre.
- Ez **nem** a lexikai (Strong-alapú) gerinc része; nem mérőeszköz a motívum-azonosításhoz, hanem tematikus index, amelynek minden bejegyzése csak jelölt lehet (`adat/jeloltek.tsv`).

## Proveniencia

`scope=teljes-Nave | forras=basokant/nave@4f35c7d data/nave.txt | ts=2026-09-30`. Sorszámok: `naplok/F18_import_naplo.md`.
