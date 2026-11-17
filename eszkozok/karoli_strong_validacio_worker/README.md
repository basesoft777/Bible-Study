# Az emberi validáció online felülete (F175.V21, DT-F175vp)

Cloudflare Worker statikus tartalommal és D1 adatbázissal: az ellenőr a levélben kapott személyes linken
(`https://<worker>/?t=<token>`) dolgozik, minden válasz azonnal a szerverre mentődik, és bármely eszközön folytatható.

| fájl | szerep |
|---|---|
| `src/logika.js`, `src/index.js` | a Worker: tételek tokenre, mentés append-only naplóba, „Kész”, admin-haladás és -export |
| `schema.sql` | a D1 sémája (a `naplo` táblán UPDATE és DELETE tiltva; `utolso` nézet: az utolsó érvényes válasz) |
| `public/index.html` | az ellenőrző oldal online változata, **generált** a `karoli_strong_validacio_sablon.html`-ből, tétel nélkül |
| `public/admin.html` | a szervező haladás-oldala (`/admin`): csak haladás, ítélet nem |
| `teszt/*.mjs` | Node-próbák kitalált adattal (D1 helyett `node:sqlite`); a `teszt_karoli_strong_validacio.py` futtatja |
| `wrangler.toml` | a Worker beállítása; titok nincs benne |

**Titok a repóban nincs.** A tételek (a minta, a csalik), a tokenek és az admin-kulcs csak a letétben
(`~/Bible-Study-letet/`) és a Cloudflare-ben állnak. A D1-ben a tokennek csak az SHA-256-ja van. A rendszerben név
nincs: a token–ellenőr megfeleltetést a felhasználó a letétbeli `tokenek.tsv` `megjegyzes` oszlopába írja.

## Végpontok

| végpont | jogosultság | mit ad |
|---|---|---|
| `GET /api/tetelek` | ellenőri token (`Authorization: Bearer`) | az ellenőr tételei, a minta-azonosító, az utolsó érvényes válaszai |
| `POST /api/valaszok` | ellenőri token | 1–100 válasz-pillanatkép; a `kliens_azon` szerint idempotens; idegen tételnél az egész köteg 403 |
| `POST /api/kesz` | ellenőri token | lezárás, ha minden tételnél van ítélet; utána a mentés 409 |
| `GET /api/admin/haladas` | admin-kulcs | ellenőrönként: ítéletszám, utolsó mentés, kész-e |
| `GET /api/admin/export?formatum=json\|csv` | admin-kulcs | JSON: ellenőrönként az utolsó érvényes válaszok és a teljes napló (a kiértékelő `--szerver-export`-ja ezt olvassa); CSV: a napló |

Minden válasz `X-Robots-Tag: noindex`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store` fejléccel megy, a
`/robots.txt` mindent tilt, a HTML-en szigorú CSP áll.

## Helyi próba (fiók nélkül)

```
npm install wrangler@4.164.0          # a repón kívüli mappában
python eszkozok/karoli_strong_validacio_minta.py --csak-html --vegleges
python eszkozok/karoli_strong_validacio_d1.py
npx wrangler d1 execute karoli-strong-validacio --local --persist-to <ideiglenes mappa> --config eszkozok/karoli_strong_validacio_worker/wrangler.toml --file %USERPROFILE%/Bible-Study-letet/d1_betoltes.sql
npx wrangler dev --config eszkozok/karoli_strong_validacio_worker/wrangler.toml --persist-to <ideiglenes mappa> --var ADMIN_KULCS:<helyi próbakulcs, legalább 32 karakter>
```

## Telepítés (a felhasználó fiókjával)

1. A felhasználó létrehozza a Cloudflare-fiókot és egy API tokent (jogosultság: *Workers Scripts: Edit*,
   *D1: Edit*), és környezeti változóba teszi: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`. A tokent chatbe,
   fájlba vagy naplóba írni tilos.
2. Adatbázis EU-jurisdikcióval: `npx wrangler d1 create karoli-strong-validacio --jurisdiction eu`; a kiírt
   `database_id` a `wrangler.toml`-ba kerül (nem titok; commit).
3. Betöltés: `python eszkozok/karoli_strong_validacio_d1.py` (a letétbeli tokenekkel), majd
   `npx wrangler d1 execute karoli-strong-validacio --remote --config … --file %USERPROFILE%/Bible-Study-letet/d1_betoltes.sql`.
   A betöltő a tételeket a LEKOTES.md-vel veti össze; a sima INSERT miatt kétszeri betöltés hibával áll meg.
4. Admin-kulcs secretként (PowerShell): `Get-Content $env:USERPROFILE\Bible-Study-letet\admin_kulcs.txt | npx wrangler secret put ADMIN_KULCS --config …`
5. `npx wrangler deploy --config …` (első alkalommal a workers.dev aldomain regisztrálását kérheti), majd a linkek a
   tokenfájlba: `python eszkozok/karoli_strong_validacio_d1.py --alap-url https://karoli-strong-validacio.<aldomain>.workers.dev`.

## Élesítés előtt: kétfős próba

A `P1` és `P2` token a mintán kívüli 10 próbapárt kapja (`proba.tsv`; a próba semmit nem mutat meg a mintából, és a
kiértékelésbe nem kerül). Két ember, két eszköz: mindketten kitöltik a 10 tételt; közben az egyik eszközön a hálózat
megszakad (repülőgép-üzemmód), és a válaszok a kapcsolat visszatértével felmennek; az egyik ellenőr a munkát a másik
eszközén folytatja ugyanazzal a linkkel; végül „Kész, beküldöm”. Utána az admin-export teljességének ellenőrzése: a
`P1`/`P2` minden ítélete benne van, a napló sorszáma folytonos, a kiértékelő `naplobol_utolso` szabálya ugyanazt adja.

## Export és kiértékelés

```
curl -H "Authorization: Bearer <admin-kulcs>" "https://…/api/admin/export?formatum=json" -o %USERPROFILE%/Bible-Study-letet/szerver_export.json
python eszkozok/karoli_strong_validacio_kiertekel.py --szerver-export %USERPROFILE%/Bible-Study-letet/szerver_export.json
```

A kiértékelő a próba-ellenőröket kihagyja, az utolsó érvényes válaszokat a naplóból újraszámolja, és eltérésnél megáll.
