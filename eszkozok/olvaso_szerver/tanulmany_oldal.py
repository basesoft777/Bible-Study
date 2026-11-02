"""A tanulmány-oldal megjelenítője (F149 M3): a kézi markdownból generált nézet (kézzel nem szerkeszthető).

A tanulmány szövege a `pardes.db` `tanulmany_szoveg` táblájából jön (a szerver csak az adatbázist látja); itt csak megjelenik:
a címsorok horgonyt kapnak (ugyanazt, amelyet a vers → szakasz index használ), és minden igehely-hivatkozás az olvasó versére
mutat (`/<könyv>/<fej>/<vers>#v<vers>`, a visszahorgony). A hivatkozás-felismerés ugyanaz a függvény, mint az indexé
(`eszkozok/tanulmany_regiszter.py`: `talalatok`), tehát ami az indexben szerepel, az az oldalon is link.

Kimenet: biztonságos HTML (minden szöveg escape-elt; nyers HTML a forrásban nem érvényesül, nincs link-szintaxis).
Támogatott: címsorok, bekezdés, felsorolás (egy szint beágyazással), számozott lista, táblázat, idézet, vízszintes vonal,
kód-blokk, **félkövér**, *dőlt*, `kód`.
"""
import re

from markupsafe import Markup, escape

_FEJ_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
_LISTA_RE = re.compile(r'^(\s*)([-*+]|\d+\.)\s+(.*)$')
_HR_RE = re.compile(r'^\s*([-*_])(\s*\1){2,}\s*$')
_TABLA_ELV_RE = re.compile(r'^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$')
_KOD_RE = re.compile(r'`([^`]+)`')
_FELKOVER_RE = re.compile(r'\*\*(?=\S)(.+?)(?<=\S)\*\*')
_DOLT_RE = re.compile(r'(?<![\*\w])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\*\w])')
_TAG_RE = re.compile(r'<[^>]*>')


class Megjelenito:
    """Egy tanulmány megjelenítése. `T`: a `tanulmany_regiszter` modul; `kar`: `T.Karoli` (a hivatkozás-felismeréshez);
    `href(kulcs)`: az igehely-kulcs (`1Móz 3:8`) olvasó-hivatkozása vagy None; `alap_konyv`, `egy_fejezet`: mint az indexnél."""

    def __init__(self, T, kar, href, alap_konyv, egy_fejezet):
        self.T, self.kar, self.href = T, kar, href
        self.alap_konyv, self.egy_fejezet = alap_konyv, egy_fejezet

    # -- soron belüli ----------------------------------------------------------------------------------------------
    def _horgonyoz(self, h):
        """A már escape-elt soron belüli HTML szövegcsomópontjaiban az igehely-hivatkozásokat linkké alakítja (meglévő linken belül nem)."""
        if not any(c.isdigit() for c in h):
            return h
        ures = _TAG_RE.sub(lambda m: '\x00' * len(m.group()), h)          # a címkék helyén nem illeszkedő jel: a pozíciók megmaradnak
        linkben, mely = [], None
        for m in re.finditer(r'<(/?)a\b[^>]*>', h):
            if not m.group(1):
                mely = m.start()
            elif mely is not None:
                linkben.append((mely, m.end()))
                mely = None
        beszur = []
        for kezd, veg, kulcsok, _ in self.T.talalatok(ures, self.alap_konyv, self.egy_fejezet, self.kar):
            if any(kezd < b and veg > a for a, b in linkben):
                continue
            ut = self.href(kulcsok[0][0])
            if ut:
                beszur.append((kezd, veg, ut))
        for kezd, veg, ut in sorted(beszur, reverse=True):
            h = h[:kezd] + '<a class="igehely" href="%s">%s</a>' % (escape(ut), h[kezd:veg]) + h[veg:]
        return h

    def inline(self, szoveg, horgony=True):
        h = str(escape(szoveg))
        kodok = []

        def kod(m):
            kodok.append('<code>%s</code>' % m.group(1))
            return '\x01%d\x01' % (len(kodok) - 1)
        h = _KOD_RE.sub(kod, h)
        h = _FELKOVER_RE.sub(r'<strong>\1</strong>', h)
        h = _DOLT_RE.sub(r'<em>\1</em>', h)
        if horgony:
            h = self._horgonyoz(h)
        h = re.sub('\x01(\\d+)\x01', lambda m: kodok[int(m.group(1))], h)
        return h

    # -- blokkok ---------------------------------------------------------------------------------------------------
    def megjelenit(self, szoveg):
        """-> (Markup html, [(horgony, cim, szint)]). A `##`/`###` címsorok horgonya a `szakaszok()` horgonya."""
        horgonyok = [h for h, c, _ in self.T.szakaszok(szoveg) if not (h == 'eleje' and c == 'A tanulmány eleje')]
        self._horgonyok = iter(horgonyok)
        self.toc = []
        html = self._blokkok(szoveg.replace('\r\n', '\n').split('\n'))
        return Markup(html), self.toc

    def _tabla_cellak(self, sor):
        sor = sor.strip()
        if sor.startswith('|'):
            sor = sor[1:]
        if sor.endswith('|') and not sor.endswith('\\|'):
            sor = sor[:-1]
        return [c.strip().replace('\\|', '|') for c in re.split(r'(?<!\\)\|', sor)]

    def _tabla(self, sorok):
        fej, test = None, sorok
        if len(sorok) >= 2 and _TABLA_ELV_RE.match(sorok[1].strip()):
            fej, test = self._tabla_cellak(sorok[0]), sorok[2:]
        ki = ['<div class="tabla-gordul"><table class="tan-tabla">']
        if fej is not None:
            ki.append('<thead><tr>%s</tr></thead>' % ''.join('<th>%s</th>' % self.inline(c) for c in fej))
        ki.append('<tbody>')
        for sor in test:
            cellak = self._tabla_cellak(sor)
            tds = []
            for i, c in enumerate(cellak):
                if i == 0 and self.egy_fejezet and re.match(r'^\**\d{1,3}(?:\s?[–-]\s?\d{1,3})?\**$', c):
                    # az első cella versszám (egyfejezetes tanulmány): a sor eleje mint hivatkozás-szöveg
                    tds.append('<td>%s</td>' % self._horgonyoz_cella(c))
                else:
                    tds.append('<td>%s</td>' % self.inline(c))
            ki.append('<tr>%s</tr>' % ''.join(tds))
        ki.append('</tbody></table></div>')
        return '\n'.join(ki)

    def _horgonyoz_cella(self, c):
        h = self.inline(c, horgony=False)
        tal = self.T.talalatok('| ' + c + ' |', self.alap_konyv, self.egy_fejezet, self.kar)
        for kezd, veg, kulcsok, _ in tal:
            ut = self.href(kulcsok[0][0])
            if ut:
                return '<a class="igehely" href="%s">%s</a>' % (escape(ut), h)
        return h

    def _lista(self, sorok):
        """Egymást követő lista-sorok (és folytatásaik) -> beágyazott ul/ol."""
        elemek = []                       # (behuzas, rendezett, szoveg)
        for sor in sorok:
            m = _LISTA_RE.match(sor)
            if m:
                elemek.append([len(m.group(1).expandtabs(4)), m.group(2)[0].isdigit(), m.group(3)])
            elif elemek:
                elemek[-1][2] += ' ' + sor.strip()

        def epit(i, behuzas):
            if i >= len(elemek):
                return '', i
            rend = elemek[i][1]
            ki = ['<%s>' % ('ol' if rend else 'ul')]
            while i < len(elemek) and elemek[i][0] >= behuzas:
                if elemek[i][0] > behuzas:
                    bel, i = epit(i, elemek[i][0])
                    ki.append(bel)
                    continue
                szoveg = self.inline(elemek[i][2])
                i += 1
                if i < len(elemek) and elemek[i][0] > behuzas:
                    bel, i = epit(i, elemek[i][0])
                    szoveg += bel
                ki.append('<li>%s</li>' % szoveg)
            ki.append('</%s>' % ('ol' if rend else 'ul'))
            return ''.join(ki), i
        html, _ = epit(0, elemek[0][0] if elemek else 0)
        return html

    def _blokkok(self, sorok):
        ki, i, n = [], 0, len(sorok)
        while i < n:
            sor = sorok[i]
            if not sor.strip():
                i += 1
                continue
            if sor.lstrip().startswith('```'):
                j = i + 1
                while j < n and not sorok[j].lstrip().startswith('```'):
                    j += 1
                ki.append('<pre><code>%s</code></pre>' % escape('\n'.join(sorok[i + 1:j])))
                i = j + 1
                continue
            m = _FEJ_RE.match(sor)
            if m:
                szint = len(m.group(1))
                cim = m.group(2)
                if szint in (2, 3):
                    hor = next(self._horgonyok, None)
                    if hor:
                        self.toc.append((hor, re.sub(r'[*_`]', '', cim), szint))
                        ki.append('<h%d id="%s">%s</h%d>' % (szint, hor, self.inline(cim, False), szint))
                        i += 1
                        continue
                ki.append('<h%d>%s</h%d>' % (szint, self.inline(cim, False), szint))
                i += 1
                continue
            if _HR_RE.match(sor):
                ki.append('<hr>')
                i += 1
                continue
            if sor.lstrip().startswith('|'):
                j = i
                while j < n and sorok[j].lstrip().startswith('|'):
                    j += 1
                ki.append(self._tabla(sorok[i:j]))
                i = j
                continue
            if sor.lstrip().startswith('>'):
                j = i
                while j < n and sorok[j].lstrip().startswith('>'):
                    j += 1
                bel = [re.sub(r'^\s*>\s?', '', x) for x in sorok[i:j]]
                ki.append('<blockquote>%s</blockquote>' % self._blokkok(bel))
                i = j
                continue
            if _LISTA_RE.match(sor):
                j = i
                while j < n and sorok[j].strip() and (_LISTA_RE.match(sorok[j]) or sorok[j].startswith((' ', '\t'))):
                    j += 1
                ki.append(self._lista(sorok[i:j]))
                i = j
                continue
            j = i
            while j < n and sorok[j].strip() and not (
                    _FEJ_RE.match(sorok[j]) or _HR_RE.match(sorok[j]) or sorok[j].lstrip().startswith(('|', '>', '```'))
                    or _LISTA_RE.match(sorok[j])):
                j += 1
            ki.append('<p>%s</p>' % self.inline(' '.join(x.strip() for x in sorok[i:j])))
            i = j
        return '\n'.join(ki)
