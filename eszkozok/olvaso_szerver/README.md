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
| `konfig/` | `szerver.toml` (kiadás, süti, gyorsítótár), `hozzaferes.toml`, `arculat.json` (az arculati token-fájl, #98), `elemek.toml` (az elem-regiszter és a kizárt osztályok, #98 M2) |
| `arculat.py` | a token-fájl betöltése és ellenőrzése, a token-blokk (`:root`, sötét téma) előállítása; a szerver a `/arculat.css?v=<hash>` címen adja (#98 M1, DT157) |
| `tervezo.py`, `tervezo_statikus/` | a tervező mód (#98 M2): a regiszter betöltése, a stíluslap szabálytérképe, a mentés értékszűrése, a mentési végpont; a kliens (`tervezo.js`, `tervezo.css`) a `/tervezo/…` címen, **csak a `belso` kiadásban** |
| `regiszter_or.py` | a regiszter-őr: a sablonok és a blokkok `class="…"` osztályai és a kliens (`olvaso.js`, `tervezo.js`) `classList.add/toggle/remove` literál-osztályai a regiszterben vagy a kizárt listán (`python regiszter_or.py`) |
| `arculat_szinkron.py` | a design system `tokens.json`-ja a token-fájlból (`--kimenet`, `--alap`; feltöltés nélkül) |
| `sablonok/`, `statikus/` | Jinja2 (autoescape), CSS, kis JS (nincs inline script/stílus: CSP); az `olvaso.css` token-értéket nem ismétel, csak `var(--…)`-hivatkozást |
| `gunicorn_conf.py`, `telepit.sh` | indítás (gthread, 1 worker, 4 szál), környezet, frissességi teszt |
| `frissesseg.py`, `manifest_pardes_db.tsv` | az épségi teszt (K4), M1 |
| `export.py` | statikus export váza |
| `teszt_olvaso_szerver.py` | tesztek (unittest) |
| `teszt_arculat.py` | a token-fájl, a token-blokk és az `/arculat.css` tesztjei (#98 M1) |
| `teszt_tervezo.py` | a tervező mód tesztjei (#98 M2): regiszter, regiszter-őr, szabálytérkép, értékszűrés, a végpont biztonsága kiadásonként, atomi írás, ETag, szinkron-kimenet, a szelektorok a valódi lapokon |
| `teszt_pilot_aranymintaval.py` | a kirajzolt blokk-készlet összevetése a #60 pilot aranymintájával (írásjeles szöveg, számlálók, szócsempék, „Ebben a versben”, Nave, blokk-címek); a döntések (DT148–i) tesztjei, az Interlineáris csempék |

## Útvonalak

`/` kezdőlap · `/<könyv>` · `/<könyv>/<fejezet>` · `/<könyv>/<fejezet>/<vers>` · `/szo/<H0216|G1504>` · `/nezet/<olvaso|interlinearis|munkaasztal>?vissza=` · `/ugras?q=` · `/r/szo/<strong>`, `/r/vers/…` (töredékek) · `/arculat.css?v=<hash>` (a token-blokk) · `/statusz` · `/robots.txt`. A könyvkód ASCII-sített (`1Moz`). `.db`/`.tsv` nincs kiszolgálva.

Csak a `belso` kiadásban (más kiadásban 404): `/tervezo/tervezo.js`, `/tervezo/tervezo.css`, `/tervezo/terkep.json` (a regiszter és a szabálytérkép), `/tervezo/kod` (egyszeri kód, csak helyi kérésre), `POST /tervezo/mentes`, `POST /tervezo/visszaallit`.

## Tervező mód (#98 M2)

A `belso` kiadásban a fejlécben, a szintváltó mellett a **Tervező** kapcsoló. Bekapcsolva a rámutatott elem keretet és címkét kap (a regiszterbeli magyar nevével; a regiszteren kívüli elem szaggatott keretet és „nem regisztrált elem” címkét), a kattintás nem navigál, hanem kiválaszt. A panel csak a kiválasztott elem regiszterbeli tulajdonságait mutatja (csúszka a méretekre, színválasztó és paletta a színekre; a szín a látott témában állítódik), és kiírja, hány szabályban és hány elemen hat a token a lapon. Minden állítás azonnal látszik (a `:root` CSS-változói, csak ebben a böngészőben); a változáslista egyenként és egészben visszavonható, és lapváltáskor megmarad (sessionStorage). A regisztrálatlan elem tokenjei gépi névvel állíthatók (előnézet), mellettük egy másolható `elemek.toml`-részlet.

**Küldés a szerverre:** a változások a `konfig/arculat.json`-ba íródnak (rendezett, determinisztikus JSON → kis git-diff); a szerver újraindítás nélkül az új arculattal adja a lapokat (új `arculat.css?v=` hash, új ETag, ürített lap-gyorsítótár). Az előző állapot a `konfig/arculat.json.elozo`-ban (git-ignorált); az **Előző mentés vissza** gomb ezt állítja vissza. A commitot a végrehajtó vagy a felhasználó készíti, nem a szerver.

**A mentés feltételei:** csak `belso` kiadás; csak helyi kérés (a forrás 127.0.0.1/::1, nincs `X-Forwarded-For`/`Forwarded`/`X-Real-IP` fejléc, a `Host` és az `Origin` helyi); csak `POST`; egyszeri kód a `GET /tervezo/kod`-ról (`X-Tervezo-Kod` fejléc); csak a regiszterben valamely elemhez rendelt token, érvényes értékkel (szín: `#rgb`, `#rrggbb`, `rgb()`, `hsl()`; betűméret px 8–64, rem/em 0.5–4; térköz px 0–128, rem/em 0–8 (DT158); lekerekítés px 0–999; sorköz 1.0–2.4); a betűcsalád nem írható. Hiba: 403 (helyi kérés/kód), 400 (érték; a lemezes token-fájlban nem létező token is), 415 (nem JSON), 500 (a lemezes token-fájl nem érvényes, külön üzenettel); a fájl ilyenkor változatlan. A token létezését a mentés a lemezes fájl szerint vizsgálja, mert arra ír. A CSP nem lazul (`script-src 'self'`, `style-src 'self'`). Fordított proxy mögött a feltétel csak akkor tartja távol a távoli kérést, ha a proxy továbbító fejlécet ad (`X-Forwarded-For`/`Forwarded`/`X-Real-IP`) vagy a külső `Host`-ot továbbítja: így a Caddy alapbeállítása. Az nginx alapbeállítása (`proxy_pass http://127.0.0.1:8000`, `proxy_set_header` nélkül) egyiket sem teszi: a kérés loopbackről, továbbító fejléc nélkül és `Host: 127.0.0.1:8000`-rel érkezik, így egy távoli, `Origin`/`Sec-Fetch-Site` nélküli kérés (pl. `curl`) átmegy a feltételen (a `GET /tervezo/kod` kódot ad, a `POST /tervezo/mentes` ír). A `belso` kiadást ezért proxy mögé csak továbbító fejlécet adó konfigurációval szabad tenni; a kérdés nyitott (DT159, a proxy-választás: N-F76d; az ellenőri napló: `naplok/ELLENOR_TERVEZO_MOD.md`). több workerrel futtatva a mentés csak az egyik worker arculatát töltené újra, ezért a tervező mód az egy workeres fejlesztői vagy gunicorn-indításhoz való.

**Regiszter-őr:** új CSS-osztály csak regisztrálva (`[[elem]]`) vagy indokkal kizárva (`[kizart]`) kerülhet a felületre: `python regiszter_or.py` (és a `teszt_tervezo.py`). Az őr a sablonok `class="…"` attribútumait, a `blokkok.py`/`oldalak.py` `class="…"`-literáljait és a kliens `classList.add/toggle/remove` literál-argumentumait olvassa; a nem olvasható alak (egyszeres idézőjeles vagy idézőjel nélküli `class=`, összefűzéssel le nem zárt attribútum, a Jinja-kifejezés nem literál ága, `className =`, nem literál `classList`-argumentum) hiba, nem marad ki némán. Nem olvassa a tervező saját panelének osztályait (`tz-…`, a `tervezo.css`-ből) és a csak a stíluslapban szereplő osztályokat. **Szinkron:** `python arculat_szinkron.py --kimenet /tmp/tokens.json --alap <a design system mostani tokens.json-ja>`.

## Futtatás

```bash
# fejlesztés (Flask kell: uv sync az olvaso_szerver könyvtárban, Python 3.12)
PARDES_DB=/út/pardes.db python eszkozok/olvaso_szerver/alkalmazas.py --port 8765
# éles jellegű
PARDES_DB=/út/pardes.db ./telepit.sh ellenorzes && PARDES_DB=/út/pardes.db ./telepit.sh indit
# tesztek
PARDES_DB=/út/pardes.db python eszkozok/olvaso_szerver/teszt_olvaso_szerver.py
PARDES_DB=/út/pardes.db python eszkozok/olvaso_szerver/teszt_tervezo.py
```

Kiadás: `PARDES_KIADAS=belso|nyilvanos|kereskedelmi` (vagy `konfig/szerver.toml`). Nyilvános kiadásban a KJV-Strong blokk, kereskedelmiben az MCGED is kimarad; az adatbázis-kapcsolat ezeket a táblákat olvasni sem engedi.

## Hozzáférési szintek és a szintváltó (F76.34)

A szintek és a blokk–szint hozzárendelés a `konfig/hozzaferes.toml`-ban vannak (éles: mindenki `kutato`). A fejléc **szintváltója** (`/szint/<nev>`, funkcionális süti `pardes_szint`, SameSite=Lax, HttpOnly, csak váltáskor jön létre) a próbaüzemhez van, a felhasználó kérésére (2026-10-14); **csak a `belso` kiadásban** jelenik meg és hat. `nyilvanos` és `kereskedelmi` kiadásban sem a vezérlő, sem a süti, sem a `?szint=` paraméter nem emelheti a szintet. A szint része a gyorsítótár-kulcsnak és az ETag-nek.

A `konfig/hozzaferes_proba.toml` a **tesztek** próba-konfigja; az éles szerver nem tölti be. A próba-konfig a MECHANIZMUST próbálja. A `kutato` szinthez kötött blokkok: a `forditasok`-ból olvasók (`szo.bdb_magyar`, `szo.bdb_apparatus`, `szo.magyar_gorog`), továbbá a Thayer, TBESH, TBESG, LSJ, UBS_DNTG szótárakhoz tartozó blokkok (`szo.thayer`, `szo.tbesh`, `szo.tbesg`, `szo.lsj`, `szo.ubs_dntg`), amelyek az eredeti angol forrástáblákat olvassák, nem a `forditasok`-at. NEM követi pontosan a DT-F86c fordítás-listáját: a DT-F86c szerint a BY-SA-eredetű tartalom (pl. UBS_DNTG) nem zárható, a próba mégis zárja, mert csak a szűrést próbálja. **Ez a #86 freemium/prémium határát nem dönti el**, csak a mechanizmust próbálja (`teszt_szintek.py`, a két pilot-szakasz valódi lapjain).
