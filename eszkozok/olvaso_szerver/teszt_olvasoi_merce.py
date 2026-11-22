#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/olvaso_szerver/teszt_olvasoi_merce.py -- F232: az olvasó mércéje (olvasói pillanatkép) a szó-lapra és a versnézetre.

Miért kell: a #60 pilothoz mérő teszt (`teszt_pilot_aranymintaval.py`) csak a versnézetet nézi két szakaszon, a szó-lapot semmi; a
`blokkok.py` 17 tétel alatt, darabonként nőtt, és a teljes lapot senki nem olvasta olvasóként. A mérce a MAI állapotot rögzíti,
hibáival együtt (a hibák a saját tételükben javulnak, és a mércét azok frissítik). Nem képernyőkép: a lap blokksora (`data-blokk`),
a blokkcímek és a látható szöveg, normalizálva, lapranként egy szöveges fájl a `merce/` alatt, diffelhető.

A pillanatkép (`pillanatkep`):
  * a `<head>`, a `<script>`/`<style>`, a `hidden` elemek, az ugrás-link és a láblécek/figyelmeztető sávok (`labjegyzet`: ág, commit,
    építési idő) kimaradnak; az ISO időbélyeg (`2026-11-12T18:53:35Z`) és a `commit:` hash kiszűrve;
  * a blokk határa `## [<data-blokk>]` sor; a táblázat sora egy sor, a cellák ` | ` jellel;
  * a csukott `<details>` tartalma (a `<summary>` kivételével) minden sorában `▸ ` jelölővel áll: látszik, hogy alapból nem látható.

Futtatás (a DB-s rész Flask-et és `pardes.db`-t kér: `python eszkozok/teszt_futtat.py --fajl teszt_olvasoi_merce`; a normalizáló
egységtesztjei DB nélkül is futnak):
    python teszt_olvasoi_merce.py                  # tesztek
    python teszt_olvasoi_merce.py --merce-frissit  # a mérce újraírása (CSAK kifejezett parancsra; a PR leírása a felhasználó jóváhagyására hivatkozik)
Környezeti változók: PARDES_DB; PARDES_MERCE_SZIGORU=1: a mérce eltérése hiba (alapból figyelmeztetés, F232 2.5).

A mérce eltérése jóváhagyás nélkül FIGYELMEZTETÉS: a futás `MÉRCE-ELTÉRÉS` sorokban kiírja a diffet (a `teszt_futtat.py` és a
`push_elott.py` a sikeres futásnál is megmutatja). Hiba: ha egy mintaoldal nem 200, ha a mérce-fájl hiányzik, vagy ha a
normalizálás nem determinisztikus.
"""
import difflib
import os
import re
import sys
import unittest
from html.parser import HTMLParser

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
MERCE_KONYVTAR = os.path.join(D, 'merce')
DB = os.environ.get('PARDES_DB') or (os.path.dirname(os.path.dirname(D)).replace('\\', '/') + '/pardes.db')
VAN_DB = os.path.exists(DB)
try:
    import flask  # noqa: F401
    VAN_FLASK = True
except ImportError:
    VAN_FLASK = False

# --- a mintakészlet (a brief 2. 1.): a Károli-könyv kulcsa az útvonalban a Károli-rövidítés ékezet nélkül (`Jan` = Ján) -----------------
SZO_LAPOK = ('H1242', 'H7451', 'H3615', 'H0251', 'H7837', 'H2398', 'G0264', 'G3056', 'G1311', 'G2671')
VERSEK = ('/1Moz/1/1', '/1Moz/1/5', '/1Moz/3/6', '/1Moz/4/7', '/Zsolt/22/2', '/Jan/1/1')
FEJEZETEK = ('/1Moz/1', '/Zsolt/22')      # a két pilotszakasz (1Móz 1:1–2:3, Zsolt 22) fejezetnézete
MINTA = tuple('/szo/' + s for s in SZO_LAPOK) + VERSEK + FEJEZETEK

SZIGORU = os.environ.get('PARDES_MERCE_SZIGORU') == '1'
CSUKOTT_JEL = '▸ '

_VOID = frozenset('area base br col embed hr img input link meta param source track wbr'.split())
_BLOKK = frozenset('address article aside blockquote body dd details div dl dt fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 '
                   'header hr li main nav ol p pre section summary table tbody thead tfoot tr ul br'.split())
_KIHAGY = frozenset('head script style template noscript svg'.split())
_IDO = re.compile(r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?')
_COMMIT = re.compile(r'(commit:?\s*)[0-9a-f]{7,40}\b', re.I)


class _Kinyer(HTMLParser):
    """A látható szöveg sorokba rendezve (l. a modul leírását)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.verem = []        # (tag, kihagy, csukott_details, summary)
        self.sorok = []
        self.sor = ''

    def _kihagy(self):
        return any(e[1] for e in self.verem)

    def _csukott(self):
        # egy csukott <details> tartalma rejtett, kivéve a közvetlen gyermek <summary>-ját
        for i, e in enumerate(self.verem):
            if e[2]:
                kovetkezo = self.verem[i + 1] if i + 1 < len(self.verem) else None
                if not (kovetkezo and kovetkezo[3]):
                    return True
        return False

    def _flush(self):
        s = re.sub(r'\s+', ' ', self.sor).strip()
        self.sor = ''
        if s and not self._kihagy():
            self.sorok.append((CSUKOTT_JEL if self._csukott() else '') + s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in _VOID:
            if tag in _BLOKK and not self._kihagy():
                self._flush()
            return
        osztaly = (a.get('class') or '').split()
        kihagy = (tag in _KIHAGY or 'hidden' in a or 'labjegyzet' in osztaly or 'kihagy-link' in osztaly)
        if tag in _BLOKK:
            self._flush()
        csukott = tag == 'details' and 'open' not in a
        self.verem.append((tag, kihagy, csukott, tag == 'summary'))
        if kihagy:
            return
        if a.get('data-blokk'):
            self._flush()
            self.sorok.append('## [%s]' % a['data-blokk'])
        if tag in ('td', 'th') and self.sor.strip():
            self.sor += ' | '

    def handle_endtag(self, tag):
        if tag in _VOID:
            return
        for i in range(len(self.verem) - 1, -1, -1):
            if self.verem[i][0] == tag:
                if tag in _BLOKK:
                    self._flush()
                del self.verem[i:]
                return

    def handle_data(self, data):
        if not self._kihagy():
            self.sor += data

    def vege(self):
        self._flush()
        return self.sorok


def pillanatkep(html):
    """Az olvasói pillanatkép szövege (sorok `\\n`-nel összefűzve, a végén soremeléssel)."""
    k = _Kinyer()
    k.feed(html)
    k.close()
    sorok = [_COMMIT.sub(r'\1<hash>', _IDO.sub('<időbélyeg>', s)) for s in k.vege()]
    return '\n'.join(sorok) + '\n'


def merce_nev(url):
    """`/szo/H1242` -> `szo_H1242.txt`; `/1Moz/3/6` -> `vers_1Moz_3_6.txt`; `/Zsolt/22` -> `fejezet_Zsolt_22.txt`."""
    r = [x for x in url.split('/') if x]
    if r[0] == 'szo':
        return 'szo_%s.txt' % r[1]
    return '%s_%s.txt' % ('vers' if len(r) == 3 else 'fejezet', '_'.join(r))


def merce_ut(url):
    return os.path.join(MERCE_KONYVTAR, merce_nev(url))


def fejlec(url):
    return ('# F232 olvasói pillanatkép: %s\n'
            '# A mai állapot rögzítése, hibáival együtt; frissítés: teszt_olvasoi_merce.py --merce-frissit (csak jóváhagyással).\n'
            '# Jelölés: „## [blokk]” = data-blokk; „▸ ” = csukott <details> tartalma.\n' % url)


def merce_szoveg(url, html):
    return fejlec(url) + pillanatkep(html)


def beolvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read().replace('\r\n', '\n')


def app_kliens():
    import alkalmazas
    return alkalmazas.letrehoz(db_ut=DB, kiadas='belso').test_client()


def elteres_sorok(url, regi, uj, max_sor=60):
    """A `MÉRCE-ELTÉRÉS`-sorok (a diff első `max_sor` sora), a futás kimenetében is látszanak."""
    d = [x for x in difflib.unified_diff(regi.splitlines(), uj.splitlines(), 'merce/' + merce_nev(url), 'mostani', n=1, lineterm='')]
    ki = ['MÉRCE-ELTÉRÉS %s: %d változott sor (a mérce frissítése csak jóváhagyással: --merce-frissit)'
          % (url, sum(1 for x in d if x[:1] in '+-' and x[:3] not in ('+++', '---')))]
    ki += ['MÉRCE-ELTÉRÉS | ' + x[:300] for x in d[:max_sor]]
    if len(d) > max_sor:
        ki.append('MÉRCE-ELTÉRÉS | ... és további %d diff-sor' % (len(d) - max_sor))
    return ki


# =====================================================================================================================
class TestNormalizalo(unittest.TestCase):
    """A normalizáló (DB nélkül)."""

    def test_csukott_details_jelolve_summary_nem(self):
        h = ('<body><details><summary>Cím</summary><p>rejtett</p></details>'
             '<details open><summary>Nyitott</summary><p>látszik</p></details></body>')
        self.assertEqual(pillanatkep(h), 'Cím\n' + CSUKOTT_JEL + 'rejtett\nNyitott\nlátszik\n')

    def test_blokkcim_es_tablazat(self):
        h = ('<section data-blokk="szo.x"><h3>Cím <span>jel</span></h3><table><tr><td>a</td><td>b</td></tr>'
             '<tr><td>c</td></tr></table></section>')
        self.assertEqual(pillanatkep(h), '## [szo.x]\nCím jel\na | b\nc\n')

    def test_kiszurt_elemek(self):
        h = ('<head><title>T</title><script>x()</script></head><body><div class="labjegyzet">ág: x</div>'
             '<a class="kihagy-link">Ugrás</a><p hidden>rejtett</p><p>látható</p>'
             '<footer class="labjegyzet">commit: ea0a4414 · építve: 2026-11-12T18:53:35Z</footer>'
             '<p>ts 2026-11-12T18:53:35Z, commit: ea0a4414f</p></body>')
        self.assertEqual(pillanatkep(h), 'látható\nts <időbélyeg>, commit: <hash>\n')

    def test_szoveg_nem_valtozik_az_ures_ter_miatt(self):
        self.assertEqual(pillanatkep('<p>a\n   b\t<b>c</b>d</p>'), pillanatkep('<p>a b <b>c</b>d</p>'))

    def test_merce_nev(self):
        self.assertEqual(merce_nev('/szo/H1242'), 'szo_H1242.txt')
        self.assertEqual(merce_nev('/1Moz/3/6'), 'vers_1Moz_3_6.txt')
        self.assertEqual(merce_nev('/Zsolt/22'), 'fejezet_Zsolt_22.txt')

    def test_push_elott_az_olvaso_kodjat_ismeri_fel(self):
        # F232 (DT-F232a (b)): a push előtti kapu olvasó-tesztjei az olvasó kódjának változására indulnak, adatra és naplóra nem
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(D)), 'eszkozok'))
        import push_elott as P
        self.assertEqual(P.olvaso_erintett(['eszkozok/olvaso_szerver/blokkok.py', 'naplok/F232_jelentes.md', 'adat/jeloltek.tsv',
                                            'eszkozok/teszt_futtat.py', 'eszkozok\\olvaso_pilot\\adat.py', 'eszkozok/lexikon_general.py']),
                         ['eszkozok/olvaso_szerver/blokkok.py', 'eszkozok/teszt_futtat.py', 'eszkozok/olvaso_pilot/adat.py'])
        self.assertEqual(P.olvaso_erintett([]), [])

    def test_a_mintakeszlet_teljes(self):
        self.assertEqual(len(MINTA), 18)
        self.assertEqual(len({merce_nev(u) for u in MINTA}), 18)

    def test_elteres_diff_latszik(self):
        sorok = elteres_sorok('/szo/H1242', 'a\nb\n', 'a\nc\n')
        self.assertTrue(sorok[0].startswith('MÉRCE-ELTÉRÉS /szo/H1242: 2 változott sor'))
        self.assertTrue(any('-b' in s for s in sorok) and any('+c' in s for s in sorok))


@unittest.skipUnless(VAN_DB and VAN_FLASK, 'nincs pardes.db vagy Flask')
class TestMerce(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = app_kliens()

    def test_minta_oldalai_a_merce_szerint(self):
        eltert = []
        for url in MINTA:
            with self.subTest(url=url):
                r = self.c.get(url)
                self.assertEqual(r.status_code, 200, '%s: %s (a mintakészlet oldala nem érhető el)' % (url, r.status_code))
                uj = merce_szoveg(url, r.get_data(as_text=True))
                ut = merce_ut(url)
                self.assertTrue(os.path.exists(ut), '%s: nincs mérce-fájl (%s); rögzítés: teszt_olvasoi_merce.py --merce-frissit' % (url, ut))
                regi = beolvas(ut)
                if regi != uj:
                    eltert.append(url)
                    for s in elteres_sorok(url, regi, uj):
                        print(s)
                    if SZIGORU:
                        self.fail('%s: a mérce eltér (PARDES_MERCE_SZIGORU=1)' % url)
        if eltert:
            print('MÉRCE-ELTÉRÉS ÖSSZESEN: %d/%d oldal: %s' % (len(eltert), len(MINTA), ', '.join(eltert)))

    def test_a_pillanatkep_determinisztikus(self):
        for url in ('/szo/H7837', '/1Moz/1/5'):
            a = merce_szoveg(url, self.c.get(url).get_data(as_text=True))
            b = merce_szoveg(url, self.c.get(url).get_data(as_text=True))
            self.assertEqual(a, b, '%s: két egymás utáni lekérés eltér' % url)

    def test_a_szo_lap_blokksora_nem_ures(self):
        for s in SZO_LAPOK:
            sz = merce_szoveg('/szo/' + s, self.c.get('/szo/' + s).get_data(as_text=True))
            self.assertIn('## [szo.', sz, '%s: a lapon nincs szó-blokk' % s)


def frissit():
    if not (VAN_DB and VAN_FLASK):
        print('HIBA: a mérce frissítéséhez pardes.db (PARDES_DB) és Flask kell.', file=sys.stderr)
        return 2
    c = app_kliens()
    os.makedirs(MERCE_KONYVTAR, exist_ok=True)
    for url in MINTA:
        r = c.get(url)
        if r.status_code != 200:
            print('HIBA: %s: %s' % (url, r.status_code), file=sys.stderr)
            return 1
        szoveg = merce_szoveg(url, r.get_data(as_text=True))
        with open(merce_ut(url), 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('mérce: %-18s %6d sor, %7d bájt' % (url, szoveg.count('\n'), len(szoveg.encode('utf-8'))))
    return 0


if __name__ == '__main__':
    if '--merce-frissit' in sys.argv:
        sys.exit(frissit())
    unittest.main()
