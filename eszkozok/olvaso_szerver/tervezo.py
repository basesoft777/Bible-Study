"""Tervező mód (#98 M2): elem-regiszter, szabálytérkép, a mentés értékszűrése és a mentési végpont.

A tervező mód csak a `belso` kiadásban létezik: az útvonalakat (`/tervezo/*`) az `alkalmazas.letrehoz` csak ott jegyzi be,
más kiadásban mind 404, és a lap HTML-jében sincs nyoma (sem kapcsoló, sem szkript, sem stíluslap).

Részek:
- **Elem-regiszter** (`konfig/elemek.toml`, `Regiszter`): a kiválasztható elemek (CSS-szelektor), a magyar nevük, és elemenként
  az állítható tulajdonságok (magyar név → token). Mellette a kizárt osztályok listája indokkal (a regiszter-őr,
  `regiszter_or.py`, ezzel veti össze a felület osztályait). A regiszter induláskor ellenőrződik: ismeretlen vagy nem írható
  token (betűcsalád) indulási hiba.
- **Szabálytérkép** (`css_szabalyok`): a stíluslap (`statikus/olvaso.css`) szabályai szelektor → {tulajdonság → tokenek}.
  A kliens ebből számolja, hány szabályban és hány elemen hat egy token, és ebből kínálja a regisztrálatlan elem
  tokenjeit (tartalék). Útvonal: `/tervezo/terkep.json`.
- **Értékszűrés** (`ertek_szuro`, `valtozasok_ellenoriz`; a brief 3. pontja, az M0 2.2 és a DT-F98f (a)): csak a regiszterben
  valamely elemhez rendelt token írható, és csak érvényes értékkel. Szín: `#rgb`, `#rrggbb`, `rgb()`, `hsl()`; betűméret:
  px 8–64, rem/em 0.5–4; térköz: px 0–128, rem/em 0–8; lekerekítés: px 0–999; sorköz: szám 1.0–2.4. Szabad szöveg nem
  kerülhet a fájlba (a betűcsalád nem írható).
- **Mentés** (`Mento`): egyszeri kód (`GET /tervezo/kod`), csak helyi kérés (loopback, nincs továbbító fejléc, helyi `Host`,
  helyi `Origin`), csak `POST`, atomi írás (ideiglenes fájl ugyanabban a könyvtárban, majd `os.replace`), az előző állapot
  az `arculat.json.elozo`-ban (git-ignorált), a token-fájl és a lap-gyorsítótár újratöltése újraindítás nélkül.
"""
import copy
import hmac
import json
import os
import re
import secrets
import sys
import threading
import time
import tomllib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import arculat as arculat_modul

SZERVER_DIR = os.path.dirname(os.path.abspath(__file__))
ELEMEK_FAJL = 'elemek.toml'
ELEMEK_UT = os.path.join(SZERVER_DIR, 'konfig', ELEMEK_FAJL)
CSS_UT = os.path.join(SZERVER_DIR, 'statikus', 'olvaso.css')
STATIKUS_DIR = os.path.join(SZERVER_DIR, 'tervezo_statikus')
ELOZO_KITERJESZTES = '.elozo'

# token-előtag → a token-fájl csoportja (a CSS-változó neve: `--` + token); előtag nélkül szín
ELOTAG_CSOPORT = (('fs-', 'betumeret'), ('lh-', 'sorkoz'), ('space-', 'terkoz'), ('radius-', 'lekerekites'), ('font-', 'betucsalad'))
IRHATO_CSOPORT = ('szin', 'betumeret', 'sorkoz', 'terkoz', 'lekerekites')        # a betűcsalád szabad szöveg: nem írható
TIPUS = {'szin': 'szin', 'betumeret': 'hossz', 'terkoz': 'hossz', 'lekerekites': 'hossz', 'sorkoz': 'szam', 'betucsalad': 'csalad'}

# a mentés tartományai (M0 2.2; a térköz a DT-F98f (a) szerint 0–128px, rem/em 0–8)
TARTOMANY = {
    'betumeret': {'px': [8, 64], 'rem': [0.5, 4], 'em': [0.5, 4]},
    'terkoz': {'px': [0, 128], 'rem': [0, 8], 'em': [0, 8]},
    'lekerekites': {'px': [0, 999]},
    'sorkoz': {'': [1.0, 2.4]},
}

NEV = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
OSZTALY = re.compile(r'^[A-Za-z_][A-Za-z0-9_-]*$')
HEX = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')
RGB = re.compile(r'^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$')
HSL = re.compile(r'^hsl\(\s*(\d{1,3}(?:\.\d{1,2})?)\s*,\s*(\d{1,3}(?:\.\d{1,2})?)%\s*,\s*(\d{1,3}(?:\.\d{1,2})?)%\s*\)$')
HOSSZ = re.compile(r'^(\d{1,3}(?:\.\d{1,3})?)(px|rem|em)$')
SZAM = re.compile(r'^(\d(?:\.\d{1,3})?)$')

MAX_TORZS = 64 * 1024              # a mentési kérés legnagyobb törzse (bájt)
MAX_VALTOZAS = 400                 # egy mentésben legfeljebb ennyi token
KOD_ELETTARTAM = 30 * 60           # az egyszeri kód érvényessége (mp)
KOD_MAX = 16                       # egyszerre érvényes kódok

HELYI_CIM = ('127.0.0.1', '::1', '::ffff:127.0.0.1')
HELYI_HOST = re.compile(r'^(?:localhost|127\.0\.0\.1|\[::1\])(?::\d{1,5})?$')
HELYI_ORIGIN = re.compile(r'^https?://((?:localhost|127\.0\.0\.1|\[::1\])(?::\d{1,5})?)$')
TOVABBITO_FEJLEC = ('X-Forwarded-For', 'Forwarded', 'X-Real-IP', 'X-Forwarded-Host')


class TervezoHiba(ValueError):
    """Érvénytelen kérés (400) vagy érvénytelen regiszter (indulási hiba)."""


def token_csoport(token):
    """`fs-torzs` → ('betumeret', 'torzs'); előtag nélkül szín: `bg` → ('szin', 'bg')."""
    for elo, csop in ELOTAG_CSOPORT:
        if token.startswith(elo):
            return csop, token[len(elo):]
    return 'szin', token


def token_letezik(token, adat):
    csop, kulcs = token_csoport(token)
    return kulcs in adat.get(csop, {})


# =====================================================================================================================
# a regiszter
# =====================================================================================================================
def szelektor_reszek(szelektor):
    """A szelektorlista vesszőnként, a zárójeleken (`:not(…)`) és az attribútum-szögletes zárójeleken belüli vesszőt kihagyva."""
    reszek, mely, akt, idezet = [], 0, [], None
    for ch in szelektor:
        if idezet:
            akt.append(ch)
            if ch == idezet:
                idezet = None
            continue
        if ch in '"\'':
            idezet = ch
        elif ch in '([':
            mely += 1
        elif ch in ')]':
            mely -= 1
        elif ch == ',' and mely == 0:
            reszek.append(''.join(akt).strip())
            akt = []
            continue
        akt.append(ch)
    if ''.join(akt).strip():
        reszek.append(''.join(akt).strip())
    return reszek


def specifitas(resz):
    """Közelítő CSS-specifitás (a, b, c) egyetlen összetett szelektorra; a `:not(x)` az argumentuma szerint számít."""
    s = re.sub(r':not\(', ' ', resz)
    s = re.sub(r'"[^"]*"|\'[^\']*\'', '""', s)
    a = len(re.findall(r'#[A-Za-z_][\w-]*', s))
    b = len(re.findall(r'\.[A-Za-z_][\w-]*', s)) + len(re.findall(r'\[[^\]]*\]', s)) + len(re.findall(r'(?<!:):[A-Za-z][\w-]*', s))
    c = len(re.findall(r'(?:^|[\s>+~(])([a-z][a-z0-9]*)', s)) + len(re.findall(r'::[A-Za-z][\w-]*', s))
    return [a, b, c]


def szelektor_osztalyok(szelektor):
    """A szelektorban szereplő CSS-osztályok (a regiszter-őr ezeket tekinti regisztráltnak)."""
    s = re.sub(r'"[^"]*"|\'[^\']*\'', '""', szelektor)
    return set(re.findall(r'\.([A-Za-z_][\w-]*)', s))


class Regiszter:
    """A betöltött `elemek.toml`: `elemek` ([{id, nev, csoport, szelektor, tulajdonsag: [{nev, token}]}]), `kizart` ({osztály: indok})."""

    def __init__(self, ut, adat, arculat_adat):
        self.ut = ut
        if not isinstance(adat, dict) or set(adat) - {'elem', 'kizart'}:
            raise TervezoHiba('%s: ismeretlen kulcs a gyökérben (elem, kizart várt)' % ELEMEK_FAJL)
        elemek = adat.get('elem')
        if not isinstance(elemek, list) or not elemek:
            raise TervezoHiba('%s: nincs [[elem]]' % ELEMEK_FAJL)
        ids = set()
        for i, e in enumerate(elemek, 1):
            hely = '%s [[elem]] #%d' % (ELEMEK_FAJL, i)
            if not isinstance(e, dict) or set(e) != {'id', 'nev', 'csoport', 'szelektor', 'tulajdonsag'}:
                raise TervezoHiba('%s: a kulcsok: id, nev, csoport, szelektor, tulajdonsag' % hely)
            if not isinstance(e['id'], str) or not NEV.match(e['id']) or e['id'] in ids:
                raise TervezoHiba('%s: rossz vagy ismétlődő id: %r' % (hely, e['id']))
            ids.add(e['id'])
            for k in ('nev', 'csoport', 'szelektor'):
                if not isinstance(e[k], str) or not e[k].strip() or len(e[k]) > 200:
                    raise TervezoHiba('%s (%s): üres vagy túl hosszú %s' % (hely, e['id'], k))
            if not szelektor_reszek(e['szelektor']):
                raise TervezoHiba('%s (%s): üres szelektor' % (hely, e['id']))
            if not isinstance(e['tulajdonsag'], list) or not e['tulajdonsag']:
                raise TervezoHiba('%s (%s): nincs tulajdonság' % (hely, e['id']))
            for t in e['tulajdonsag']:
                if not isinstance(t, dict) or set(t) != {'nev', 'token'} or not isinstance(t['nev'], str) or not t['nev'].strip():
                    raise TervezoHiba('%s (%s): a tulajdonság kulcsai: nev, token' % (hely, e['id']))
                tok = t['token']
                if not isinstance(tok, str) or not token_letezik(tok, arculat_adat):
                    raise TervezoHiba('%s (%s): ismeretlen token: %r (nincs az arculat.json-ban)' % (hely, e['id'], tok))
                if token_csoport(tok)[0] not in IRHATO_CSOPORT:
                    raise TervezoHiba('%s (%s): a token nem állítható (betűcsalád): %s' % (hely, e['id'], tok))
        kizart = adat.get('kizart', {})
        if not isinstance(kizart, dict):
            raise TervezoHiba('%s: a [kizart] tábla osztály = "indok" párokból áll' % ELEMEK_FAJL)
        for o, indok in kizart.items():
            if not OSZTALY.match(o) or not isinstance(indok, str) or not indok.strip():
                raise TervezoHiba('%s [kizart]: rossz osztálynév vagy hiányzó indok: %r' % (ELEMEK_FAJL, o))
        self.elemek = elemek
        self.kizart = dict(kizart)

    @classmethod
    def betolt(cls, arculat_adat, ut=None):
        ut = ut or ELEMEK_UT
        with open(ut, 'rb') as f:
            try:
                adat = tomllib.load(f)
            except tomllib.TOMLDecodeError as ex:
                raise TervezoHiba('%s: nem olvasható TOML: %s' % (ELEMEK_FAJL, ex)) from ex
        return cls(ut, adat, arculat_adat)

    @classmethod
    def konfigbol(cls, konfig_dir, arculat_adat):
        """A konfiguráció könyvtárának `elemek.toml`-ja, ha van; különben a szerver alap regisztere."""
        ut = os.path.join(konfig_dir, ELEMEK_FAJL) if konfig_dir else None
        return cls.betolt(arculat_adat, ut if ut and os.path.exists(ut) else None)

    def tokenek(self):
        """A regiszterben valamely elemhez rendelt tokenek: csak ezek írhatók a mentési végponton."""
        return {t['token'] for e in self.elemek for t in e['tulajdonsag']}

    def osztalyok(self):
        """A regiszter szelektoraiban szereplő CSS-osztályok."""
        ki = set()
        for e in self.elemek:
            ki |= szelektor_osztalyok(e['szelektor'])
        return ki


# =====================================================================================================================
# a stíluslap szabálytérképe
# =====================================================================================================================
DINAMIKUS_ALLAPOT = re.compile(r'::[A-Za-z-]+(?:\([^)]*\))?|:(?:hover|focus-visible|focus-within|focus|active|visited|target)\b')


def css_szabalyok(css):
    """[{szelektor, reszek: [{alap, allapot, sp}], media, deklaraciok: [[tulajdonság, [token, …]]]}] — csak a tokent
    (`var(--x)`) használó deklarációk. Az `alap` a dinamikus állapot (`:hover`, `::before` …) nélküli szelektor (a kliens ezzel
    keres elemet), az `allapot` a levágott rész; a csak ál-elemből álló rész (pl. `::selection`) kimarad."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    ki = []

    def blokk(szoveg, media):
        poz = 0
        while True:
            j = szoveg.find('{', poz)
            if j < 0:
                return
            fej = szoveg[poz:j].strip()
            if fej.startswith('@'):
                mely, k = 1, j + 1
                while mely:
                    if szoveg[k] == '{':
                        mely += 1
                    elif szoveg[k] == '}':
                        mely -= 1
                    k += 1
                blokk(szoveg[j + 1:k - 1], fej)
                poz = k
                continue
            k = szoveg.index('}', j)
            torzs = szoveg[j + 1:k]
            poz = k + 1
            dekl = []
            for d in torzs.split(';'):
                if ':' not in d:
                    continue
                p, v = d.split(':', 1)
                tok = re.findall(r'var\(--([a-z0-9-]+)\)', v)
                if tok:
                    dekl.append([p.strip(), tok])
            if not dekl:
                continue
            reszek = []
            for r in szelektor_reszek(fej):
                alap = DINAMIKUS_ALLAPOT.sub('', r).strip()
                alap = re.sub(r'\s*>\s*$', '', alap).strip()
                if not alap:
                    continue
                allapot = ' '.join(m.group(0) for m in DINAMIKUS_ALLAPOT.finditer(r))
                reszek.append({'alap': alap, 'allapot': allapot, 'sp': specifitas(r)})
            if reszek:
                ki.append({'szelektor': ' '.join(fej.split()), 'reszek': reszek, 'media': media, 'deklaraciok': dekl})

    blokk(css, '')
    return ki


def css_beolvas(ut=None):
    with open(ut or CSS_UT, encoding='utf-8') as f:
        return f.read()


# =====================================================================================================================
# az értékszűrés
# =====================================================================================================================
def _szam(s):
    return float(s)


def ertek_szuro(csop, ertek):
    """Egy érték ellenőrzése a csoport szerint; jó értéknél maga az érték (változatlanul), rossznál TervezoHiba."""
    if not isinstance(ertek, str) or len(ertek) > 40:
        raise TervezoHiba('az érték nem szöveg, vagy túl hosszú')
    if csop == 'szin':
        if HEX.match(ertek):
            pass
        elif RGB.match(ertek):
            if any(int(x) > 255 for x in RGB.match(ertek).groups()):
                raise TervezoHiba('rgb(): 0–255')
        elif HSL.match(ertek):
            h, s, l = (float(x) for x in HSL.match(ertek).groups())
            if h > 360 or s > 100 or l > 100:
                raise TervezoHiba('hsl(): árnyalat 0–360, telítettség és világosság 0–100%')
        else:
            raise TervezoHiba('szín: #rgb, #rrggbb, rgb(r, g, b) vagy hsl(h, s%, l%)')
        if not arculat_modul.SZIN.match(ertek):
            raise TervezoHiba('szín: a token-fájl formája nem fogadja el')
        return ertek
    if csop in ('betumeret', 'terkoz', 'lekerekites'):
        m = HOSSZ.match(ertek)
        if not m or m.group(2) not in TARTOMANY[csop]:
            raise TervezoHiba('hossz: %s' % ', '.join(TARTOMANY[csop]))
        lo, hi = TARTOMANY[csop][m.group(2)]
        if not lo <= _szam(m.group(1)) <= hi:
            raise TervezoHiba('tartományon kívül: %s–%s%s' % (lo, hi, m.group(2)))
        return ertek
    if csop == 'sorkoz':
        m = SZAM.match(ertek)
        lo, hi = TARTOMANY['sorkoz']['']
        if not m or not lo <= _szam(m.group(1)) <= hi:
            raise TervezoHiba('sorköz: szám %s–%s, mértékegység nélkül' % (lo, hi))
        return ertek
    raise TervezoHiba('nem írható csoport: %s' % csop)


def valtozasok_ellenoriz(torzs, irhato_tokenek, arculat_adat):
    """A mentési kérés törzse: `{"tokenek": {token: érték}}`, színnél az érték `{"light": …}` és/vagy `{"dark": …}`.
    Visszaad: [(csoport, kulcs, téma vagy None, érték)]; bármely hibánál TervezoHiba (a fájl nem változik)."""
    if not isinstance(torzs, dict) or set(torzs) != {'tokenek'} or not isinstance(torzs['tokenek'], dict):
        raise TervezoHiba('a törzs: {"tokenek": {token: érték}}')
    tok = torzs['tokenek']
    if not tok or len(tok) > MAX_VALTOZAS:
        raise TervezoHiba('üres vagy túl nagy változáslista')
    ki = []
    for token, ertek in tok.items():
        if not isinstance(token, str) or not NEV.match(token) or token not in irhato_tokenek or not token_letezik(token, arculat_adat):
            raise TervezoHiba('nem regisztrált token: %r' % (token[:40] if isinstance(token, str) else token))
        csop, kulcs = token_csoport(token)
        if csop not in IRHATO_CSOPORT:
            raise TervezoHiba('nem írható token: %s' % token)
        if csop == 'szin':
            if not isinstance(ertek, dict) or not ertek or set(ertek) - set(arculat_modul.TEMAK):
                raise TervezoHiba('%s: a szín értéke {"light": …, "dark": …} (legalább az egyik)' % token)
            for tema in sorted(ertek):
                try:
                    ki.append((csop, kulcs, tema, ertek_szuro(csop, ertek[tema])))
                except TervezoHiba as ex:
                    raise TervezoHiba('%s (%s): %s' % (token, tema, ex)) from ex
        else:
            try:
                ki.append((csop, kulcs, None, ertek_szuro(csop, ertek)))
            except TervezoHiba as ex:
                raise TervezoHiba('%s: %s' % (token, ex)) from ex
    return ki


# =====================================================================================================================
# a helyi kérés és a mentés
# =====================================================================================================================
def helyi_keres(req):
    """Igaz, ha a kérés helyi: a forrás loopback, nincs továbbító (proxy) fejléc, a `Host` helyi név (DNS-rebinding ellen), az
    `Origin` (ha van) ugyanaz a helyi cím, és a `Sec-Fetch-Site` (ha van) azonos eredetű."""
    if req.remote_addr not in HELYI_CIM:
        return False
    if any(h in req.headers for h in TOVABBITO_FEJLEC):
        return False
    host = (req.host or '').lower()
    if not HELYI_HOST.match(host):
        return False
    origin = req.headers.get('Origin')
    if origin is not None:
        m = HELYI_ORIGIN.match(origin.lower())
        if not m or m.group(1) != host:
            return False
    sfs = req.headers.get('Sec-Fetch-Site')
    if sfs is not None and sfs not in ('same-origin', 'none'):
        return False
    return True


def atomi_ir(ut, bajtok):
    """Ideiglenes fájlba írás ugyanabban a könyvtárban, majd átnevezés (`os.replace`); hibánál az ideiglenes fájl törlődik,
    a cél változatlan."""
    d, n = os.path.split(ut)
    tmp = os.path.join(d, '.%s.%d.%s.tmp' % (n, os.getpid(), secrets.token_hex(4)))
    try:
        with open(tmp, 'wb') as f:
            f.write(bajtok)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, ut)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def szerializal(adat, crlf=False):
    """A token-fájl determinisztikus alakja: rendezett kulcsok, 2 szóközös behúzás, záró újsor (kis git-diff)."""
    s = json.dumps(adat, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if crlf:
        s = s.replace('\n', '\r\n')
    return s.encode('utf-8')


class Mento:
    """Az egyszeri kódok és a token-fájl írása; a sikeres írás után a szerver az új token-fájllal dolgozik (a lap-gyorsítótár ürül,
    a gyorsítótár-kulcs és az ETag az `arculat.hash`-sel együtt változik)."""

    def __init__(self, gyar, cache, regiszter):
        self.gyar = gyar
        self.cache = cache
        self.regiszter = regiszter
        self._kodok = {}
        self._kodzar = threading.Lock()
        self._irzar = threading.Lock()

    # -- kódok ---------------------------------------------------------------------------------------------------------
    def _takarit(self):
        most = time.monotonic()
        for k in [k for k, lejar in self._kodok.items() if lejar < most]:
            del self._kodok[k]

    def uj_kod(self):
        with self._kodzar:
            self._takarit()
            while len(self._kodok) >= KOD_MAX:
                del self._kodok[min(self._kodok, key=self._kodok.get)]
            k = secrets.token_urlsafe(32)
            self._kodok[k] = time.monotonic() + KOD_ELETTARTAM
            return k

    def kod_felhasznal(self, kod):
        """Igaz, ha a kód érvényes; a kód ezzel elhasználódik (egyszeri)."""
        if not isinstance(kod, str) or not kod or len(kod) > 100:
            return False
        with self._kodzar:
            self._takarit()
            for k in list(self._kodok):
                if hmac.compare_digest(k.encode('utf-8'), kod.encode('utf-8')):
                    del self._kodok[k]
                    return True
        return False

    # -- írás ----------------------------------------------------------------------------------------------------------
    def _beir(self, uj_bajtok, regi_bajtok):
        """Az új token-fájl ellenőrzése, az előző állapot mentése, atomi írás, újratöltés."""
        ut = self.gyar.arculat.ut
        uj_arculat = arculat_modul.Arculat(ut, uj_bajtok)              # ellenőriz (ArculatHiba → nem ír)
        atomi_ir(ut + ELOZO_KITERJESZTES, regi_bajtok)
        atomi_ir(ut, uj_bajtok)
        self.gyar.arculat = uj_arculat
        self.cache.urit()
        return uj_arculat

    def mentes(self, valtozasok):
        with self._irzar:
            ut = self.gyar.arculat.ut
            with open(ut, 'rb') as f:
                regi = f.read()
            adat = copy.deepcopy(json.loads(regi.decode('utf-8')))
            for csop, kulcs, tema, ertek in valtozasok:
                if tema:
                    adat[csop][kulcs][tema] = ertek
                else:
                    adat[csop][kulcs] = ertek
            return self._beir(szerializal(adat, b'\r\n' in regi), regi)

    def visszaallit(self):
        """Az előző állapot (`arculat.json.elozo`) visszaírása; a mostani állapot lesz az új előző (a visszaállítás is visszavonható)."""
        with self._irzar:
            ut = self.gyar.arculat.ut
            if not os.path.exists(ut + ELOZO_KITERJESZTES):
                raise FileNotFoundError('nincs előző állapot')
            with open(ut + ELOZO_KITERJESZTES, 'rb') as f:
                elozo = f.read()
            with open(ut, 'rb') as f:
                regi = f.read()
            return self._beir(elozo, regi)


# =====================================================================================================================
# a szabálytérkép a kliensnek
# =====================================================================================================================
def terkep(regiszter, arculat, css_szoveg):
    """A `/tervezo/terkep.json` tartalma: a regiszter (szelektor-részekkel és specifitással), a tokenek (érték, csoport, típus,
    írható-e), a mentés tartományai és a stíluslap szabálytérképe."""
    irhato = regiszter.tokenek()
    tokenek = {}
    for csop, elo in arculat_modul.ELOTAG.items():
        for kulcs, ertek in arculat.adat[csop].items():
            tok = elo[2:] + kulcs
            tokenek[tok] = {'csoport': csop, 'tipus': TIPUS[csop], 'ertek': ertek, 'irhato': tok in irhato and csop in IRHATO_CSOPORT}
    elemek = []
    for e in regiszter.elemek:
        elemek.append({'id': e['id'], 'nev': e['nev'], 'csoport': e['csoport'], 'szelektor': e['szelektor'],
                       'reszek': [{'alap': r, 'sp': specifitas(r)} for r in szelektor_reszek(e['szelektor'])],
                       'tulajdonsag': [{'nev': t['nev'], 'token': t['token']} for t in e['tulajdonsag']]})
    return {'verzio': 1, 'arculat_hash': arculat.hash, 'regiszter': elemek, 'tokenek': tokenek, 'tartomany': TARTOMANY,
            'temak': list(arculat_modul.TEMAK), 'szabalyok': css_szabalyok(css_szoveg)}


# =====================================================================================================================
# az útvonalak (csak a belso kiadásban jegyzi be az alkalmazas.letrehoz)
# =====================================================================================================================
def utvonalak(app, gyar, cache, regiszter):
    from flask import Response, jsonify, make_response, request, send_from_directory

    mento = Mento(gyar, cache, regiszter)
    app.extensions['pardes']['tervezo'] = mento
    css_szoveg = css_beolvas()

    def valasz(adat, kod=200):
        r = make_response(jsonify(adat), kod)
        r.headers['Cache-Control'] = 'no-store'
        return r

    def tiltott():
        return valasz({'hiba': 'tiltott: a tervező mód mentése csak helyi kérésre és érvényes egyszeri kóddal működik'}, 403)

    @app.get('/tervezo/tervezo.js')
    def tervezo_js():
        r = send_from_directory(STATIKUS_DIR, 'tervezo.js', mimetype='text/javascript', max_age=0)
        r.headers['Cache-Control'] = 'no-cache'
        return r

    @app.get('/tervezo/tervezo.css')
    def tervezo_css():
        r = send_from_directory(STATIKUS_DIR, 'tervezo.css', mimetype='text/css', max_age=0)
        r.headers['Cache-Control'] = 'no-cache'
        return r

    @app.get('/tervezo/terkep.json')
    def tervezo_terkep():
        etag = '"terkep-%s-%s"' % (gyar.arculat.hash, gyar.kod_verzio)
        if request.headers.get('If-None-Match') == etag:
            r = make_response('', 304)
        else:
            r = Response(json.dumps(terkep(regiszter, gyar.arculat, css_szoveg), ensure_ascii=False, sort_keys=True), mimetype='application/json')
        r.headers['ETag'] = etag
        r.headers['Cache-Control'] = 'no-cache'
        return r

    @app.get('/tervezo/kod')
    def tervezo_kod():
        if not helyi_keres(request):
            return tiltott()
        return valasz({'kod': mento.uj_kod()})

    def post_elofeltetel():
        """None, ha a kérés helyi és a kód érvényes (a kód ezzel elhasználódik); különben a 403-as válasz."""
        if not helyi_keres(request):
            return tiltott()
        if not mento.kod_felhasznal(request.headers.get('X-Tervezo-Kod')):
            return tiltott()
        return None

    @app.post('/tervezo/mentes')
    def tervezo_mentes():
        hiba = post_elofeltetel()
        if hiba is not None:
            return hiba
        if (request.mimetype or '') != 'application/json':
            return valasz({'hiba': 'a törzs application/json'}, 415)
        if request.content_length is None or request.content_length > MAX_TORZS:
            return valasz({'hiba': 'hiányzó vagy túl nagy törzs'}, 400)
        try:
            torzs = json.loads(request.get_data(cache=False).decode('utf-8'))
            valtozasok = valtozasok_ellenoriz(torzs, regiszter.tokenek(), gyar.arculat.adat)
            uj = mento.mentes(valtozasok)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return valasz({'hiba': 'a törzs nem érvényes JSON'}, 400)
        except (TervezoHiba, arculat_modul.ArculatHiba) as ex:
            return valasz({'hiba': str(ex)}, 400)
        return valasz({'ok': True, 'arculat_hash': uj.hash, 'valtozas': len(valtozasok), 'uj_kod': mento.uj_kod()})

    @app.post('/tervezo/visszaallit')
    def tervezo_visszaallit():
        hiba = post_elofeltetel()
        if hiba is not None:
            return hiba
        try:
            uj = mento.visszaallit()
        except FileNotFoundError:
            return valasz({'hiba': 'nincs előző mentés'}, 409)
        except arculat_modul.ArculatHiba as ex:
            return valasz({'hiba': str(ex)}, 400)
        return valasz({'ok': True, 'arculat_hash': uj.hash, 'uj_kod': mento.uj_kod()})

    return mento
