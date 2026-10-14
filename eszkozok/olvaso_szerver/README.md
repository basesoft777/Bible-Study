# Olvasói szerver (#76 OLVASOI_KONKORDANCIA, M2)

Szerveroldali Flask-alkalmazás, amely a `pardes.db`-ből (csak olvasásra) állítja elő a Károli-bibliaszöveg lapjait, három váltható nézettel. Terv: `naplok/OLVASOI_KONKORDANCIA_M0.md`; zárónapló: ugyanott 4.4, és `naplok/OLVASOI_KONKORDANCIA_zaras.md`.

## Szerkezet

| Fájl | Szerep |
|---|---|
| `alkalmazas.py` | Flask-gyár: útvonalak, süti, fejlécek, gyorsítótár/ETag; SQL nincs benne |
| `oldalak.py` | a lapelőállítás (HTML-szöveg), **nem függ a Flasktól**; a statikus export erre épül |
| `blokkok.py` | a blokk-regiszter (46 azonosító: az M2 40-e a pilot 39 mért adatblokkjára + az M2b 6 új blokkja a pilot kirajzolt készletéhez), jelleg-címke, forrás- és licencsor |
| `lekerdezesek.py` | az összes SQL, paraméterezve (N-F76c) |
| `adatbazis.py` | csak olvasó kapcsolat, `set_authorizer` a kiadás szerint kizárt táblákra |
| `hozzaferes.py` | hozzáférési szintek a `konfig/hozzaferes.toml`-ból |
| `gyorsitotar.py` | korlátos LRU a kész lapokra |
| `konfig/` | `szerver.toml` (kiadás, süti, gyorsítótár), `hozzaferes.toml` |
| `sablonok/`, `statikus/` | Jinja2 (autoescape), CSS, kis JS (nincs inline script/stílus: CSP) |
| `gunicorn_conf.py`, `telepit.sh` | indítás (gthread, 1 worker, 4 szál), környezet, frissességi teszt |
| `frissesseg.py`, `manifest_pardes_db.tsv` | az épségi teszt (K4), M1 |
| `export.py` | statikus export váza |
| `teszt_olvaso_szerver.py` | tesztek (unittest) |
| `teszt_pilot_aranymintaval.py` | a kirajzolt blokk-készlet összevetése a #60 pilot aranymintájával (írásjeles szöveg, számlálók, szócsempék, „Ebben a versben”, Nave, blokk-címek); a döntésre váró hiányok `expectedFailure` (DT-F76e–i) |

## Útvonalak

`/` kezdőlap · `/<könyv>` · `/<könyv>/<fejezet>` · `/<könyv>/<fejezet>/<vers>` · `/szo/<H0216|G1504>` · `/nezet/<olvaso|interlinearis|munkaasztal>?vissza=` · `/ugras?q=` · `/r/szo/<strong>`, `/r/vers/…` (töredékek) · `/statusz` · `/robots.txt`. A könyvkód ASCII-sített (`1Moz`). `.db`/`.tsv` nincs kiszolgálva.

## Futtatás

```bash
# fejlesztés (Flask kell: uv sync az olvaso_szerver könyvtárban, Python 3.12)
PARDES_DB=/út/pardes.db python eszkozok/olvaso_szerver/alkalmazas.py --port 8765
# éles jellegű
PARDES_DB=/út/pardes.db ./telepit.sh ellenorzes && PARDES_DB=/út/pardes.db ./telepit.sh indit
# tesztek
PARDES_DB=/út/pardes.db python eszkozok/olvaso_szerver/teszt_olvaso_szerver.py
```

Kiadás: `PARDES_KIADAS=belso|nyilvanos|kereskedelmi` (vagy `konfig/szerver.toml`). Nyilvános kiadásban a KJV-Strong blokk, kereskedelmiben az MCGED is kimarad; az adatbázis-kapcsolat ezeket a táblákat olvasni sem engedi.
