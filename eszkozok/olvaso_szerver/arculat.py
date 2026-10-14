"""Az arculati token-fájl (`konfig/arculat.json`) betöltése, ellenőrzése és a token-blokk előállítása (#98 M1, DT-F98e).

A token-fájl az arculat egyetlen forrása: a színek (világos és sötét téma), a betűcsaládok, a betűméretek, a sorközök, a
térközök és a lekerekítések értékei. A stíluslap (`statikus/olvaso.css`) egyetlen token-értéket sem ismétel, csak
`var(--…)`-hivatkozást tartalmaz. A token-blokk (`:root` és a két sötét téma-blokk) nem generált fájl a repóban: a szerver a
`/arculat.css?v=<hash>` útvonalon adja, a statikus export ugyanebből a függvényből (`css_blokk`) írja ki.

A CSS-változó neve a csoportból és a kulcsból áll: `szin.bg` → `--bg`, `betucsalad.ui` → `--font-ui`,
`betumeret.X` → `--fs-X`, `sorkoz.X` → `--lh-X`, `terkoz.X` → `--space-X`, `lekerekites.X` → `--radius-X`.

A betöltés csak a formát ellenőrzi (ismeretlen csoport, rossz név vagy rossz alakú érték: indulási hiba). A mentés
tartományai és a regiszterhez kötött írási jog az M2 mentési végpontjának dolga.
"""
import hashlib
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ALAP_UT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'konfig', 'arculat.json')
FAJLNEV = 'arculat.json'

# csoport → CSS-változó előtag; a sorrend a token-blokk sorrendje
ELOTAG = {'szin': '--', 'betucsalad': '--font-', 'betumeret': '--fs-', 'sorkoz': '--lh-', 'terkoz': '--space-', 'lekerekites': '--radius-'}
TEMAK = ('light', 'dark')

NEV = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
SZIN = re.compile(r'^(?:#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}'
                  r'|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)'
                  r'|hsl\(\s*\d{1,3}(?:\.\d+)?\s*,\s*\d{1,3}(?:\.\d+)?%\s*,\s*\d{1,3}(?:\.\d+)?%\s*\))$')
HOSSZ = re.compile(r'^\d+(?:\.\d+)?(?:px|rem|em)$')
PX = re.compile(r'^\d+(?:\.\d+)?px$')
SZAM = re.compile(r'^\d+(?:\.\d+)?$')
# betűcsalád: idézett és csupasz nevek vesszővel; CSS-t lezáró vagy HTML-be törő jel nem lehet benne
CSALAD = re.compile(r'^[A-Za-z0-9 ",\-]+$')

ERTEK_MINTA = {'betumeret': HOSSZ, 'terkoz': HOSSZ, 'lekerekites': PX, 'sorkoz': SZAM, 'betucsalad': CSALAD}


class ArculatHiba(ValueError):
    pass


def ellenoriz(adat):
    """A token-fájl formájának ellenőrzése; hibánál ArculatHiba, a hibás kulcs megnevezésével."""
    if not isinstance(adat, dict):
        raise ArculatHiba('arculat.json: a gyökér nem objektum')
    ismeretlen = set(adat) - set(ELOTAG) - {'verzio'}
    if ismeretlen:
        raise ArculatHiba('arculat.json: ismeretlen csoport: %s' % ', '.join(sorted(ismeretlen)))
    if adat.get('verzio') != 1:
        raise ArculatHiba('arculat.json: a verzio nem 1')
    for csop in ELOTAG:
        if not isinstance(adat.get(csop), dict) or not adat[csop]:
            raise ArculatHiba('arculat.json: hiányzó vagy üres csoport: %s' % csop)
        for nev, ertek in adat[csop].items():
            if not NEV.match(nev):
                raise ArculatHiba('arculat.json: rossz token-név: %s.%s' % (csop, nev))
            if csop == 'szin':
                if not isinstance(ertek, dict) or set(ertek) != set(TEMAK):
                    raise ArculatHiba('arculat.json: a szín tokenje két témát vár (light, dark): szin.%s' % nev)
                for t in TEMAK:
                    if not isinstance(ertek[t], str) or not SZIN.match(ertek[t]):
                        raise ArculatHiba('arculat.json: rossz színérték: szin.%s.%s = %r' % (nev, t, ertek[t]))
            elif not isinstance(ertek, str) or not ERTEK_MINTA[csop].match(ertek):
                raise ArculatHiba('arculat.json: rossz érték: %s.%s = %r' % (csop, nev, ertek))
    return adat


def valtozok(adat, tema='light'):
    """[(CSS-változó, érték)] a token-blokk sorrendjében; a színek a megadott téma értékével."""
    ki = []
    for csop, elo in ELOTAG.items():
        for nev in sorted(adat[csop]):
            ertek = adat[csop][nev][tema] if csop == 'szin' else adat[csop][nev]
            ki.append((elo + nev, ertek))
    return ki


def css_blokk(adat):
    """A token-blokk (CSS-szöveg): `:root` minden tokennel (a színek világos értékével), majd a sötét téma két blokkja
    (rendszer-beállítás, ha a felhasználó nem a világosat választotta; kifejezett sötét téma) csak a színekkel."""
    sotet = ' '.join('%s%s: %s;' % (ELOTAG['szin'], n, adat['szin'][n]['dark']) for n in sorted(adat['szin'])) + ' color-scheme: dark;'
    sorok = ['/* GENERÁLT: eszkozok/olvaso_szerver/konfig/arculat.json (arculat.py, css_blokk). Kézzel ne szerkeszd: a forrás a token-fájl. */',
             ':root {']
    sorok += ['  %s: %s;' % (v, e) for v, e in valtozok(adat, 'light')]
    sorok += ['}',
              '@media (prefers-color-scheme: dark) {',
              '  :root:not([data-tema="light"]) { %s }' % sotet,
              '}',
              ':root[data-tema="dark"] { %s }' % sotet,
              '']
    return '\n'.join(sorok)


def tartalom_hash(nyers):
    """A token-fájl tartalmának kivonata (a sorvég-különbség nem számít); a lap gyorsítótár-kulcsába, az ETag-be és a
    stíluslap címébe (`/arculat.css?v=`) kerül."""
    return hashlib.sha256(nyers.replace(b'\r\n', b'\n')).hexdigest()[:16]


class Arculat:
    """A betöltött token-fájl: `adat` (ellenőrzött szótár), `hash`, `css` (a token-blokk)."""

    def __init__(self, ut, nyers):
        self.ut = ut
        try:
            adat = json.loads(nyers.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as ex:
            raise ArculatHiba('arculat.json: nem olvasható JSON (%s): %s' % (ut, ex)) from ex
        self.adat = ellenoriz(adat)
        self.hash = tartalom_hash(nyers)
        self.css = css_blokk(self.adat)

    @classmethod
    def betolt(cls, ut=None):
        ut = ut or ALAP_UT
        with open(ut, 'rb') as f:
            return cls(ut, f.read())

    @classmethod
    def konfigbol(cls, konfig_dir):
        """A konfiguráció könyvtárának `arculat.json`-ja, ha van; különben a szerver alap token-fájlja."""
        ut = os.path.join(konfig_dir, FAJLNEV) if konfig_dir else None
        return cls.betolt(ut if ut and os.path.exists(ut) else None)

    def tokenek(self):
        """A CSS-változók halmaza (a regiszter és a stíluslap összevetéséhez)."""
        return {v for v, _ in valtozok(self.adat)}
