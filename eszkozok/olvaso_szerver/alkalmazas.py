"""Az olvasói szerver Flask-alkalmazása (#76 M2, DT146/1).

Csak útvonalat, sütit, fejlécet és gyorsítótárat kezel; a lapok tartalma az `oldalak.py`-ban készül, az SQL a
`lekerdezesek.py`-ban áll. Az adatbázis nem kerül ki a böngészőbe: a böngésző csak a kért lap HTML-jét kapja; nincs
`.db`/`.tsv` kiszolgálás (a `/pardes.db` ismeretlen könyvnek számít, 404).

Indítás (a célgépen): gunicorn -c gunicorn_conf.py "alkalmazas:letrehoz()"   (1 worker, 4 szál: gthread)
Fejlesztés:           python alkalmazas.py --port 8765
Kód-újratöltéssel:    python alkalmazas.py --port 8765 --ujratolt   (az `indit.sh` ezt használja; l. `figyelt_fajlok`)
"""
import json
import os
import re
import sys
import tomllib
from urllib.parse import urlencode

from flask import Flask, Response, abort, jsonify, make_response, redirect, request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import adatbazis
import allapot as allapot_modul
import arculat as arculat_modul
import hozzaferes as hozz_modul
import kereses as kereses_modul
import lekerdezesek
import oldalak
import tervezo as tervezo_modul
from gyorsitotar import Gyorsitotar

KONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'konfig')

CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"


def _konfig(konfig_dir=None):
    d = konfig_dir or os.environ.get('PARDES_KONFIG_DIR') or KONFIG_DIR
    with open(os.path.join(d, 'szerver.toml'), 'rb') as f:
        return tomllib.load(f), d


def letrehoz(db_ut=None, kiadas=None, konfig_dir=None, hozzaferes=None):
    """Az alkalmazás-gyár. Paraméter > környezeti változó > konfiguráció."""
    konf, kdir = _konfig(konfig_dir)
    db_ut = db_ut or os.environ.get('PARDES_DB') or konf.get('db') or (adatbazis.GY + 'pardes.db')
    kiadas = kiadas or os.environ.get('PARDES_KIADAS') or konf.get('kiadas', 'belso')
    hozz = hozzaferes or hozz_modul.Hozzaferes.betolt(kdir)
    db = adatbazis.Adatbazis(db_ut, kiadas, mmap_bajt=int(konf.get('mmap_bajt', 0)))
    gyar = oldalak.OldalGyar(db, hozz, arculat=arculat_modul.Arculat.konfigbol(kdir))
    # a lábléc indítási állapota (#100): ág, commit, építési idő, figyelmeztetések; a statikus exportban nincs (ott a lábléc változatlan)
    gyar.lablec = allapot_modul.LablecFigyelo(kiadas, gyar.kozos.meta.get('epites_ts', ''))
    # az elem-regiszter (#98 M2): induláskor ellenőrzött (ismeretlen vagy nem állítható token indulási hiba), minden kiadásban
    regiszter = tervezo_modul.Regiszter.konfigbol(kdir, gyar.arculat.adat)
    suti = konf.get('suti', {})
    suti_nev = suti.get('nev', 'pardes_reteg')
    szint_suti_nev = suti.get('szint_nev', 'pardes_szint')
    gy = konf.get('gyorsitotar', {})
    cache = Gyorsitotar(gy.get('max_lap', 512), gy.get('max_bajt', 64 * 1024 * 1024))
    nyilvanos_mod = kiadas != 'belso'

    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statikus'), static_url_path='/statikus')
    app.config['JSON_AS_ASCII'] = False
    app.extensions['pardes'] = {'db': db, 'gyar': gyar, 'cache': cache, 'hozz': hozz, 'regiszter': regiszter}

    # -- a tervező mód (#98 M2): CSAK a belso kiadásban; más kiadásban a /tervezo/* útvonalak nem léteznek (404), és a lapon
    #    nincs kapcsoló, szkript és stíluslap. A mentés feltételei (helyi kérés, egyszeri kód, értékszűrés): tervezo.py.
    if kiadas == 'belso':
        gyar.tervezo = True
        tervezo_modul.utvonalak(app, gyar, cache, regiszter)

    # -- réteg és szint ---------------------------------------------------------------------------------------------------
    def reteg_kerese():
        """A rétegek (#134, DT-F134f (b)): `?reteg=` > a régi `?nezet=` (álnév) > a `pardes_reteg` süti > réteg nélkül. A süti itt
        NEM jön létre (csak a /reteg/<nev>/<be|ki> és a /nezet/<nev> útvonalon). A régi `pardes_nezet` sütit nem olvassuk."""
        if 'reteg' in request.args:
            return oldalak.reteg_ervenyes(request.args.get('reteg'))
        if 'nezet' in request.args:
            return oldalak.reteg_ervenyes(request.args.get('nezet'))
        return oldalak.reteg_ervenyes(request.cookies.get(suti_nev))

    def reteg_suti(r, ertek):
        r.set_cookie(suti_nev, ertek, max_age=int(suti.get('max_kor_mp', 31536000)), samesite='Lax', httponly=True, secure=bool(suti.get('secure', False)), path='/')

    def aktualis_ut():
        return request.path

    def szint_kerese():
        """A kérés szintje (rang). CSAK a `belso` kiadásban választható (a `pardes_szint` süti); `nyilvanos` és `kereskedelmi` kiadásban a süti és
        minden paraméter (`?szint=`) figyelmen kívül marad: az alapértelmezett szint érvényes, azt semmi nem emelheti (F76.34)."""
        if kiadas != 'belso':
            return hozz.szint(request)
        r = hozz.szint_nevbol(request.cookies.get(szint_suti_nev))
        return r if r is not None else hozz.szint(request)

    # -- közös lap-kiszolgálás gyorsítótárral és ETaggel ---------------------------------------------------------------------
    def kiszolgal(kulcs_reszek, elo, fragment=False):
        szint = szint_kerese()
        reteg = reteg_kerese()
        # az arculat hash-e külön tag (#98): a token-fájl változása után nincs 304 és nincs régi lap a gyorsítótárból
        kulcs = (request.path, tuple(sorted(kulcs_reszek.items())), reteg, szint, kiadas, gyar.kozos.adatbazis_kulcs, oldalak.SABLON_VERZIO, gyar.kod_verzio,
                 gyar.arculat.hash, fragment, gyar.lablec.kap().kulcs() if gyar.lablec else None)
        etag = Gyorsitotar.etag(kulcs)
        hit = cache.kap(kulcs)
        if hit is None:
            try:
                hit = elo(reteg, szint)
            except oldalak.NemTalalhato as ex:
                return hiba(404, str(ex))
            cache.tesz(kulcs, hit)
            allapot = 'MISS'
        else:
            allapot = 'HIT'
        if request.headers.get('If-None-Match') == etag:
            r = make_response('', 304)
        else:
            r = make_response(hit)
            r.headers['Content-Type'] = 'text/html; charset=utf-8'
        r.headers['ETag'] = etag
        r.headers['Cache-Control'] = 'public, max-age=300' if nyilvanos_mod else 'no-cache'
        r.headers['X-Cache'] = allapot
        # a réteg a sütitől függ: a közbenső gyorsítótárak ne keverjék
        r.headers['Vary'] = 'Cookie'
        return r

    def hiba(kod, uzenet):
        reteg = reteg_kerese()
        try:
            html = gyar.hiba_lap(kod, uzenet, reteg, request.path, szint_kerese())
        except Exception:
            html = '<!doctype html><title>%s</title><p>%s</p>' % (kod, 'hiba')
        r = make_response(html, kod)
        r.headers['Content-Type'] = 'text/html; charset=utf-8'
        r.headers['Cache-Control'] = 'no-store'
        return r

    @app.errorhandler(404)
    def _404(_):
        return hiba(404, 'A keresett oldal nem található.')

    @app.errorhandler(405)
    def _405(_):
        return hiba(405, 'Ez a művelet nem engedélyezett.')

    @app.errorhandler(500)
    def _500(_):
        return hiba(500, 'Belső hiba.')

    # -- fejlécek -----------------------------------------------------------------------------------------------------------
    @app.after_request
    def _fejlecek(r):
        r.headers.setdefault('Content-Security-Policy', CSP)
        r.headers.setdefault('X-Content-Type-Options', 'nosniff')
        r.headers.setdefault('Referrer-Policy', 'same-origin')
        return r

    # -- útvonalak -----------------------------------------------------------------------------------------------------------
    @app.get('/')
    def kezdolap():
        ut = aktualis_ut()
        return kiszolgal({}, lambda reteg, szint: gyar.kezdolap(reteg, ut, szint))

    @app.get('/<konyv>')
    def konyv_lap(konyv):
        ut = aktualis_ut()
        return kiszolgal({}, lambda reteg, szint: gyar.konyv_lap(konyv, reteg, ut, szint))

    def _fejezet(konyv, fej, vers):
        szo = lekerdezesek.hnorm(request.args.get('szo', '')[:12]) or ''
        # a lap módja és a versmód füle (#134 M1): szo | info | vers | kh | temak | motivum
        ful = request.args.get('ful', '') if request.args.get('ful') in oldalak.FUL_ERTEKEK else ''
        ut = request.path + ('?' + urlencode([(k, v) for k, v in (('szo', szo), ('ful', ful)) if v]) if (szo or ful) else '')
        return kiszolgal({'szo': szo, 'ful': ful}, lambda reteg, szint: gyar.fejezet_lap(konyv, fej, vers, reteg, szint, szo, ful, ut))

    @app.get('/<konyv>/<int:fej>')
    def fejezet_lap(konyv, fej):
        return _fejezet(konyv, fej, None)

    @app.get('/<konyv>/<int:fej>/<int:vers>')
    def vers_lap(konyv, fej, vers):
        return _fejezet(konyv, fej, vers)

    @app.get('/szo/<strong>')
    def szo_lap(strong):
        ut = aktualis_ut()
        return kiszolgal({}, lambda reteg, szint: gyar.szo_lap(strong, reteg, szint, ut))

    @app.get('/r/szo/<strong>')
    def szo_toredek(strong):
        # `?ig=1Moz/1/2`: a vers-kontextus (az „Ebben a versben” blokkhoz); csak szigorúan ellenőrzött alakban
        m = re.match(r'^([A-Za-z0-9]{1,12})/([0-9]{1,3})/([0-9]{1,3})$', request.args.get('ig', ''))
        kk = gyar.kozos.slug_kk.get(m.group(1)) if m else None
        ig = '%s %d:%d' % (kk, int(m.group(2)), int(m.group(3))) if kk else None
        return kiszolgal({'ig': ig or ''}, lambda reteg, szint: gyar.szo_fragment(strong, szint, ig), fragment=True)

    @app.get('/r/vers/<konyv>/<int:fej>/<int:vers>')
    def vers_toredek(konyv, fej, vers):
        return kiszolgal({}, lambda reteg, szint: gyar.vers_fragment(konyv, fej, vers, szint), fragment=True)

    @app.get('/reteg/<nev>/<allas>')
    def reteg_valtas(nev, allas):
        """Egy réteg be- vagy kikapcsolása (#134, DT-F134f (b)): itt (és a /nezet/<nev> álnéven) jön létre a funkcionális süti
        (DT146/4). A többi réteg a süti szerinti állapotában marad."""
        if nev not in oldalak.RETEGEK or allas not in ('be', 'ki'):
            return hiba(404, 'Ismeretlen réteg.')
        most = set(x for x in oldalak.reteg_ervenyes(request.cookies.get(suti_nev)).split(',') if x)
        most = most | {nev} if allas == 'be' else most - {nev}
        r = redirect(oldalak.biztonsagos_vissza(request.args.get('vissza')), 302)
        reteg_suti(r, oldalak.reteg_ervenyes(','.join(most)))
        r.headers['Cache-Control'] = 'no-store'
        return r

    @app.get('/nezet/<nev>')
    def nezet_valtas(nev):
        """A régi nézetváltó címe álnévként (DT-F134f (b)): 302 a `vissza` címre, a nézetnek megfelelő réteggel
        (`interlinearis` → `il`, `olvaso` és `munkaasztal` → réteg nélkül). Ismeretlen név: 404, süti nélkül."""
        if nev not in oldalak.NEZET_ALNEVEK:
            return hiba(404, 'Ismeretlen nézet.')
        r = redirect(oldalak.biztonsagos_vissza(request.args.get('vissza')), 302)
        reteg_suti(r, oldalak.NEZET_ALNEVEK[nev])
        r.headers['Cache-Control'] = 'no-store'
        return r

    @app.get('/szint/<nev>')
    def szint_valtas(nev):
        """A hozzáférési szint próbaüzemi választása (F76.34, a felhasználó kérésére): funkcionális süti, csak váltáskor, csak a `belso` kiadásban.
        Más kiadásban az útvonal nem létezik (404, süti nélkül)."""
        if kiadas != 'belso' or hozz.szint_nevbol(nev) is None:
            return hiba(404, 'Ismeretlen szint.')
        r = redirect(oldalak.biztonsagos_vissza(request.args.get('vissza')), 302)
        r.set_cookie(szint_suti_nev, nev, max_age=int(suti.get('max_kor_mp', 31536000)), samesite='Lax', httponly=True, secure=bool(suti.get('secure', False)), path='/')
        r.headers['Cache-Control'] = 'no-store'
        return r

    @app.get('/ugras')
    def ugras():
        """Navigáció: az `?q=` (igehely vagy Strong-szám) vagy a `konyv`/`fej`/`vers` űrlapmezők alapján átirányít."""
        q = request.args.get('q')
        if q is None and request.args.get('konyv'):
            q = '%s %s%s' % (request.args.get('konyv', ''), request.args.get('fej', '1') or '1', (':' + request.args['vers']) if request.args.get('vers') else '')
        cel = oldalak.ugras_celpont(gyar.kozos, q)
        if not cel:
            return hiba(404, 'Nem értelmezhető cél. Adj meg igehelyet (pl. 1Móz 1:4) vagy Strong-számot (pl. H0216); szóra és frázisra a /kereses lap keres.')
        r = redirect(cel, 302)
        r.headers['Cache-Control'] = 'no-store'
        return r

    @app.get('/kereses')
    def kereses():
        """A keresés (M3): `?q=` (+ `tipus`, `mod`) vagy a típusos állandó alak (`?strong=`, `?szo=` + `mod`, `?frazis=`, `?heber=`), `tol`: lapozás.
        Igehelyre (pl. `1Móz 1:4`) a `q` ugrik. A paraméterek csak a `kereses.ertelmez` normalizálásán át jutnak a lekérdezésbe (paraméterként)."""
        ut = request.full_path.rstrip('?') if request.query_string else request.path
        urlap = {'q': request.args.get('q') or next((request.args.get(t) for t in kereses_modul.TIPUSOK if request.args.get(t)), ''),
                 'tipus': next((t for t in kereses_modul.TIPUSOK if request.args.get(t)), request.args.get('tipus') or 'auto'),
                 'mod': request.args.get('mod') or kereses_modul.ALAP_MOD}
        try:
            k = kereses_modul.ertelmez(request.args, gyar.kozos)
        except kereses_modul.KeresesHiba as ex:
            html = gyar.kereses_lap(None, reteg_kerese(), szint_kerese(), ut, hiba=str(ex), urlap=urlap)
            r = make_response(html, 400)
            r.headers['Content-Type'] = 'text/html; charset=utf-8'
            r.headers['Cache-Control'] = 'no-store'
            return r
        if isinstance(k, tuple):
            r = redirect(k[1], 302)
            r.headers['Cache-Control'] = 'no-store'
            return r
        kulcs = {'urlap': tuple(sorted(urlap.items()))}
        if k is not None:
            kulcs.update({'tipus': k.tipus, 'szavak': tuple(k.szavak), 'szoveg': k.szoveg, 'mod': k.mod, 'tol': k.tol})
        return kiszolgal(kulcs, lambda reteg, szint: gyar.kereses_lap(k, reteg, szint, ut, urlap=urlap))

    @app.get('/statusz')
    def statusz():
        s = gyar.statusz()
        ut = os.environ.get('PARDES_FRISSESSEG_FAJL')
        fr = 'nem futott'
        if ut and os.path.exists(ut):
            with open(ut, encoding='utf-8') as f:
                sorok = [l.strip() for l in f if l.strip()]
            fr = sorok[-1] if sorok else 'üres'
        s['frissesseg'] = fr
        n, b = cache.meret()
        s['gyorsitotar'] = {'lap': n, 'bajt': b, 'talalat': cache.talalat, 'melle': cache.melle}
        s['allapot'] = 'ok'
        r = Response(json.dumps(s, ensure_ascii=False), mimetype='application/json')
        r.headers['Cache-Control'] = 'no-store'
        return r

    @app.get('/arculat.css')
    def arculat_css():
        """A token-blokk (#98, DT-F98e): a `konfig/arculat.json`-ból generálva, nem fájlból. A lap `?v=<hash>`-sel linkeli;
        a jelenlegi hash-sel kért változat sokáig gyorsítótárazható, minden más kérés újraellenőrzendő."""
        a = gyar.arculat
        etag = '"arculat-%s"' % a.hash
        if request.headers.get('If-None-Match') == etag:
            r = make_response('', 304)
        else:
            r = Response(a.css, mimetype='text/css')
            r.headers['Content-Type'] = 'text/css; charset=utf-8'
        r.headers['ETag'] = etag
        r.headers['Cache-Control'] = 'public, max-age=31536000, immutable' if request.args.get('v') == a.hash else 'no-cache'
        return r

    @app.get('/robots.txt')
    def robots():
        return Response('User-agent: *\nDisallow: /\n', mimetype='text/plain')

    return app


def figyelt_fajlok(szerver_dir=None):
    """Az újratöltő által figyelt, nem Python-modul fájlok (#100): a Werkzeug alapból csak a betöltött modulokat nézi, a sablonokat,
    a konfigurációt és a statikus fájlokat nem. A BDB-szeletelő (`bdb_szelet.py`) a DT-F99c óta a szerver könyvtárában él, a Werkzeug
    modulként figyeli. A tervező mód által futás közben írt `arculat.json` és `.elozo`-ja KIMARAD: a mentés újraindítás nélkül hat (a szerver
    az `arculat.hash`-ből követi), a figyelése minden mentésnél újraindítaná a szervert."""
    d = szerver_dir or os.path.dirname(os.path.abspath(__file__))
    ki = []
    for alk in ('sablonok', 'konfig', 'statikus'):
        for gyoker, _, nevek in os.walk(os.path.join(d, alk)):
            for n in sorted(nevek):
                if n.startswith('arculat.json') or n.endswith('.pyc'):
                    continue
                ki.append(os.path.join(gyoker, n))
    return sorted(f for f in ki if os.path.isfile(f))


def main():
    import argparse
    ap = argparse.ArgumentParser(description='PaRDeS olvasó (fejlesztői szerver; élesben gunicorn)')
    ap.add_argument('--db')
    ap.add_argument('--kiadas', choices=adatbazis.KIADASOK)
    ap.add_argument('--port', type=int, default=8765)
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--ujratolt', action='store_true', help='kódváltozáskor magától újraindul (Werkzeug stat-újratöltő: a /mnt/c-n az inotify nem működik)')
    a = ap.parse_args()
    if not a.ujratolt:
        letrehoz(a.db, a.kiadas).run(host=a.host, port=a.port, threaded=True)
        return
    # az újratöltővel a szülő-folyamat csak a figyelő: az alkalmazást (adatbázis, regiszter) csak a gyerek építi fel, így a mért indulás nem duplázódik
    from werkzeug.serving import is_running_from_reloader, run_simple
    app = letrehoz(a.db, a.kiadas) if is_running_from_reloader() else (lambda environ, start: [])
    if is_running_from_reloader():
        L = app.extensions['pardes']['gyar'].lablec.kap()
        print('[indítás] kiadás=%s ág=%s commit=%s kod_verzio=%s epites_ts=%s%s' % (
            L.kiadas, L.ag, L.commit, app.extensions['pardes']['gyar'].kod_verzio, L.epites_ts,
            ''.join(' FIGYELEM: ' + f for f in L.figyelmeztetesek)), flush=True)
    run_simple(a.host, a.port, app, threaded=True, use_reloader=True, reloader_type='stat', reloader_interval=1, extra_files=figyelt_fajlok())


if __name__ == '__main__':
    main()
