#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/olvaso_szerver/blokkfej.py -- F231.17: a lapon álló blokkok, jelleg-címkék és fejek kivonata láthatósággal (a main-összevetés
alapja; a kapu: `teszt_blokkfej.py`).

Miért kell: a #810 javítása közben a main-en látható adat került le a lapról vagy csukott lenyíló mögé (az „Apparátus és
szövegkritika” a szónézetről, a jelleg-címkék és a forrássor a blokkcím mellől, az üres eredményű blokkok), és ezt egyetlen teszt
sem fogta meg, mert a tesztek a javított alakot keresték, nem azt, ami közben eltűnt. A szerkesztő szabálya (2026-11-23): amit a
main a lapon mutatott, az maradjon látható. Ez a modul egy rögzített oldallistán kivonja, mi áll a lapon és milyen láthatósággal;
a `teszt_blokkfej.py` a main-ből generált alapfájlhoz (`merce/blokkfej_alap.tsv`) veti az ág állapotát.

A kivonat sorai (`fajta`, `blokk`, `szoveg`, `lathatosag`):
  * `blokk`        — egy `data-blokk` szakasz (a `szoveg` a címe, a h3 saját szövege);
  * `jelleg`       — jelleg-címke a blokk címsorában („forrásadat”, „gépi feldolgozás”, „modell-kimenet”);
  * `jelleg-mashol`— jelleg-címke a blokkon belül, de nem a címsorban (pl. egy lenyílóban);
  * `megj`         — a blokk rövid forrásmegjegyzése a címsorban (a jelleg-címke melletti `.megj`);
  * `forras`       — a blokk forrás- és licencsora (a `szoveg` üres: a jelenléte és a láthatósága számít);
  * `ures`         — üres eredmény jelzése (`.ures`, pl. „Nincs adat (üres eredmény, nem negatív lelet).”);
  * `fej`          — címsor (h1–h4), lenyíló-felirat (summary) és gomb (button) szövege;
  * `tabla`        — egy táblázat fejléce (a `th` cellák ` | `-vel; a fejléc nélküli táblázat nem áll a kivonatban).
A szövegben a számok `#`-re cserélve állnak (a darabszám változása nem eltűnés). A láthatóság: `lathato`, `csukott` (csukott
<details> tartalma, a saját feliratán kívül), `rejtett` (`hidden` attribútum alatt).

Használat (a `teszt_blokkfej.py --alap-ment` ezt hívja a main worktree-jére):
    python -I blokkfej.py --repo <a vizsgált repó gyökere> --ki <kimenet.tsv> [--fejlec "<sor>"]
A kódot a `--repo` útjáról tölti (a `-I` kapcsolóval a szkript könyvtára nem kerül a modulútra), a `PARDES_DB` adatbázisán.
"""
import argparse
import os
import re
import sys
import unicodedata
from html.parser import HTMLParser

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))

# A rögzített oldallista: (URL, hozzáférési szint). A verslap fülei külön állnak, mert a lap csak a kiválasztott fül tartalmát adja.
# Az oldalak: verssor és szónézet (köztük a H4325 és a H8415, amelyről az apparátus eltűnt), egy újszövetségi vers és szónézet, a
# kereszthivatkozás- és motívumfül kutatói szinten, valamint az F232 pillanatképeinek szó-lapjai.
OLDALAK = (
    ('/1Moz/1/7', None), ('/1Moz/1/7?ful=kh', 'kutato'), ('/1Moz/1/7?ful=temak', None), ('/1Moz/1/7?ful=motivum', 'kutato'),
    ('/1Moz/1/7?szo=H4325&ful=szo', None), ('/1Moz/1/2?szo=H8415&ful=szo', None),
    ('/1Moz/1/1', None), ('/1Moz/1/1?ful=kh', 'kutato'), ('/1Moz/1/5?szo=H1242&ful=szo', None),
    ('/Zsolt/22/2', None), ('/Zsolt/22', None),
    ('/Jan/1/1', None), ('/Jan/1/1?ful=kh', 'kutato'), ('/Jan/1/1?szo=G3056&ful=szo', None),
    ('/Rom/3/23?szo=G0264&ful=szo', None),
    ('/szo/H1242', None), ('/szo/H0430', None), ('/szo/H7451', None), ('/szo/G0264', None), ('/szo/G3056', None),
)
KUTATO = 'kutato'

LATHATO, CSUKOTT, REJTETT = 'lathato', 'csukott', 'rejtett'
RANG = {LATHATO: 2, CSUKOTT: 1, REJTETT: 0}

_FEJ = frozenset('h1 h2 h3 h4 summary button'.split())
_KIHAGY = frozenset('head script style template noscript svg'.split())
_VOID = frozenset('area base br col embed hr img input link meta param source track wbr'.split())


def norm(s):
    """Az összevetési alak: NFC, egy szóköz, a számok `#`-re cserélve."""
    s = unicodedata.normalize('NFC', s or '')
    s = re.sub(r'\d+(?:[.,]\d+)?', '#', s)
    return re.sub(r'\s+', ' ', s).strip()


def betuk(s):
    """A tartalmazás-próba alakja: csak a betűk, kisbetűvel (írásjel, szám, szóköz és tagolás nélkül)."""
    return ''.join(c for c in unicodedata.normalize('NFC', s or '').lower() if c.isalpha())


class Kivonat(HTMLParser):
    """A lap elemei láthatósággal (l. a modul leírását)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.verem = []          # [tag, attrs, gyűjtő vagy None]
        self.elemek = []         # [fajta, blokk, szoveg, lathatosag]
        self.cim = None          # (elem-index, szöveg-lista): a blokk h3-jának saját szövege

    def _lathatosag(self):
        rejtett, csukott = False, False
        for i, (tag, a, _g) in enumerate(self.verem):
            if 'hidden' in a:
                rejtett = True
            if tag == 'details' and 'open' not in a:
                kov = self.verem[i + 1] if i + 1 < len(self.verem) else None
                if not (kov and kov[0] == 'summary'):
                    csukott = True
        return REJTETT if rejtett else (CSUKOTT if csukott else LATHATO)

    def _blokk(self):
        for tag, a, _g in reversed(self.verem):
            if a.get('data-blokk'):
                return a['data-blokk']
        return ''

    def _benne(self, tag):
        return any(t == tag for t, _a, _g in self.verem)

    def _kihagy(self):
        return any(t in _KIHAGY for t, _a, _g in self.verem)

    def handle_starttag(self, tag, attrs):
        if tag in _VOID:
            return
        a = {k: (v if v is not None else '') for k, v in attrs}
        gy = None
        if not self._kihagy() and tag not in _KIHAGY:
            osztaly = a.get('class', '').split()
            lat = self._lathatosag() if 'hidden' not in a else REJTETT
            blokk = a.get('data-blokk') or self._blokk()
            if a.get('data-blokk'):
                self.elemek.append(['blokk', blokk, '', lat])
            elif tag == 'h3' and blokk and self.elemek and self.elemek[-1][0] == 'blokk' and self.elemek[-1][1] == blokk \
                    and not self.elemek[-1][2] and self.cim is None:
                self.cim = (len(self.elemek) - 1, [])
            elif 'jelleg' in osztaly:
                gy = ['jelleg' if self._benne('h3') else 'jelleg-mashol', blokk, [], lat]
            elif blokk and 'megj' in osztaly and self._benne('h3'):
                gy = ['megj', blokk, [], lat]
            elif 'forras' in osztaly:
                self.elemek.append(['forras', blokk, '', lat])
            elif 'ures' in osztaly:
                gy = ['ures', blokk, [], lat]
            elif tag == 'table':
                gy = ['tabla', blokk, [], lat]
            elif tag in _FEJ:
                gy = ['fej', blokk, [], lat]
            if tag == 'th':
                for _t, _a, g in reversed(self.verem):
                    if g is not None and g[0] == 'tabla':
                        if g[2]:
                            g[2].append(' | ')
                        break
        self.verem.append([tag, a, gy])

    def handle_endtag(self, tag):
        if tag in _VOID:
            return
        for i in range(len(self.verem) - 1, -1, -1):
            if self.verem[i][0] == tag:
                for t, _a, gy in reversed(self.verem[i:]):
                    if gy is not None:
                        sz = norm(''.join(gy[2]))
                        if sz:
                            self.elemek.append([gy[0], gy[1], sz, gy[3]])
                    if t == 'h3' and self.cim is not None:
                        self.elemek[self.cim[0]][2] = norm(''.join(self.cim[1]))
                        self.cim = None
                del self.verem[i:]
                return

    def handle_data(self, data):
        if self._kihagy():
            return
        nyitott = [g for _t, _a, g in self.verem if g is not None]
        th = self._benne('th')
        for g in nyitott:
            if g[0] != 'tabla' or th:           # a táblázatból csak a fejléc (th) szövege
                g[2].append(data)
        if self.cim is not None and not any(g[0] in ('jelleg', 'megj') for g in nyitott):
            self.cim[1].append(data)

    def vege(self):
        self.close()
        return [tuple(e) for e in self.elemek]


def kivonat(html):
    k = Kivonat()
    k.feed(html)
    return k.vege()


def kliens_gyar(repo, db=None):
    """A `repo` olvasó-szerverének Flask teszt-kliense (a kódot a `repo` útjáról tölti)."""
    szerver = os.path.join(os.path.abspath(repo), 'eszkozok', 'olvaso_szerver')
    if szerver not in sys.path:
        sys.path.insert(0, szerver)
    import alkalmazas
    if os.path.normcase(os.path.dirname(os.path.abspath(alkalmazas.__file__))) != os.path.normcase(szerver):
        raise RuntimeError('az alkalmazas modul nem a megadott repóból jött: %s' % alkalmazas.__file__)
    db = db or os.environ.get('PARDES_DB') or os.path.join(os.path.abspath(repo), 'pardes.db')
    return lambda: alkalmazas.letrehoz(db_ut=db, kiadas='belso').test_client()


def lapok(uj_kliens, oldalak=OLDALAK):
    """{(url, szint): html} a rögzített oldallistán (szint: 'alap' vagy 'kutato')."""
    k = {None: uj_kliens(), KUTATO: uj_kliens()}
    k[KUTATO].get('/szint/kutato?vissza=/')
    ki = {}
    for url, szint in oldalak:
        r = k[szint].get(url)
        if r.status_code != 200:
            raise RuntimeError('%s (%s): HTTP %s' % (url, szint or 'alap', r.status_code))
        ki[(url, szint or 'alap')] = unicodedata.normalize('NFC', r.get_data(as_text=True))
    return ki


def sorok(lapok_html):
    """[(url, szint, fajta, blokk, szoveg, lathatosag)]."""
    return [k + e for k, h in lapok_html.items() for e in kivonat(h)]


FEJLEC_OSZLOPOK = ('url', 'szint', 'fajta', 'blokk', 'szoveg', 'lathatosag')


def tsv_ir(sorok_, ut, fejlec=()):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        for s in fejlec:
            f.write('# %s\n' % s)
        f.write('\t'.join(FEJLEC_OSZLOPOK) + '\n')
        for s in sorok_:
            f.write('\t'.join(x.replace('\t', ' ').replace('\n', ' ') for x in s) + '\n')


def tsv_olvas(ut):
    ki, fej = [], None
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n')
            if not sor or sor.startswith('#'):
                continue
            m = sor.split('\t')
            if fej is None:
                fej = m
                continue
            ki.append(tuple(m))
    return ki


def main():
    ap = argparse.ArgumentParser(description='a lapon álló blokkok, jelleg-címkék és fejek kivonata (F231.17)')
    ap.add_argument('--repo', default=os.path.dirname(os.path.dirname(D)))
    ap.add_argument('--ki', required=True)
    ap.add_argument('--fejlec', action='append', default=[])
    a = ap.parse_args()
    s = sorok(lapok(kliens_gyar(a.repo)))
    tsv_ir(s, a.ki, a.fejlec)
    print('%d elem, %d lap -> %s' % (len(s), len(OLDALAK), a.ki))


if __name__ == '__main__':
    main()
