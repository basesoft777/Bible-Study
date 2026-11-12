#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tablajegyzet.py -- az új szerkezetű lexikonlap jegyzeteinek és forrássorainak olvasói alakja (lap-javit HAMART-001; a
felhasználó átnézése, 2. és 12. tétel, „Csak az A) csoport”).

A lap kész szövegén fut, a generálás végén, csak az új szerkezetű lapon. A lap szerkezete nem változik: blokk nem
tűnik el, semmi nem kerül mellékletbe, a jegyzetek a helyükön maradnak.
  - A jegyzet látható szövegéből kikerül a közös forrásmegjelölés jele (‹E1›, ‹K1›), a hozzárendelés mechanikája („a
    szerkesztői hozzárendelés (X → Y) alá esik …”), a szavazatszám, a döntés dátuma, a felmérés-rész és a munkamenet-
    jel (U2:). A rejtett `<!-- eredeti: … -->` megjegyzés marad: a proveniencia ott áll (CLAUDE.md 1. szabály).
  - A közös forrásmegjelölések feloldása (‹E1› = …) rejtett megjegyzésbe kerül (a jel a jegyzetekben már nem áll).
  - A szakaszvégi „Forrás:” sorban csak a forrásművek neve áll, dátum és munkaanyag nélkül; a teljes sor a rejtett
    megjegyzésben marad.
"""
import re

_KOMMENT_RX = re.compile(r'<!--.*?-->', re.S)
_LABJ_DEF_RX = re.compile(r'^\[\^([\w.-]+)\]:\s?(.*)$')
_LABJ_REF_RX = re.compile(r'\[\^([\w.-]+)\]')
_DATUM_RX = re.compile(r',?\s*\b20\d\d[-.]\d\d[-.]\d\d\b(?:\s*\([a-z]\))?')
_KOD_RX = re.compile(r'‹[A-Z]\d+›')
_FORRAS_SOR_RX = re.compile(r'^\*(\(?)(Forrás|forrás):\s*(.*?)(\)?)\*(\s*<!--.*)?$', re.S)
_JELMAGYARAZAT_RX = re.compile(r'^\*(?:A közös forrásmegjelölések|Minden sor forrásmegjelölése)')
_MUNKA_NEVEK = ('a lap munkaanyaga', 'a lap munkanaplója', 'kézi szerkesztés', 'a lap adattáblája')


def _jelentes_olvasoi(t):
    """A „jelentés címkéje” rész olvasói alakja: mi a jelentés, a hozzárendelés mechanikája nélkül."""
    t = t.strip()
    m = re.match(r'BDB-példa:\s*(.*?)(?:\s*\([^)]*versenkénti jelentései\))?;\s*ez a szerkesztői hozzárendelés.*$', t)
    if m:
        return m.group(1).strip()
    m = re.match(r'BDB-példa:\s*(.*?)(?:\s*\([^)]*\))?\s*$', t)
    if m:
        return m.group(1).strip()
    m = re.search(r'jelentésszám „([^”]+)” → ([^,)]+)', t)
    if m and 'tagolása szerint' in t:
        szotar = 'Thayer' if 'Thayer' in t else 'BDB'
        cel = m.group(2).strip()
        if cel.lower().startswith(szotar.lower()):
            cel = cel[len(szotar):].strip()
        return ('a %s szócikkfeje' % szotar) if cel == 'fej' else 'a %s %s szakasza' % (szotar, cel)
    if 'nincs leképezve' in t and 'tagolatlan' in t:
        return 'a szócikk egésze (a szótár nem tagolja számozott jelentésekre)'
    m = re.match(r'(.*?)(?:;\s*(?:ez )?a szerkesztői hozzárendelés.*)$', t)
    if m:
        t = m.group(1).strip()
    return re.sub(r'\s*\(a [^)]*versenkénti jelentései\)', '', t)


def olvasoi_jegyzet(lathato, ujszov=False):
    """Egy lábjegyzet látható szövegéből az olvasói jegyzet: forrás és jelentés, műhelyszöveg nélkül."""
    t = _KOMMENT_RX.sub('', lathato).strip()
    if 'a sornak nincs Strong-száma' in t:
        return 'Tematikus hely: a versben a lánc szava nem áll.'
    # a vers saját (nem lánc-) szava a tematikus sorban (Jel 22:3): a címke maga az olvasói jegyzet
    m = re.search(r'a jelentés címkéje:\s*(Tematikus hely:[^·]*)', t)
    if m:
        s = m.group(1).strip()
        return s + ('' if s.endswith('.') else '.')
    forras_elotag = t.startswith('forrás:')
    t = re.sub(r'^(?:Forrás|forrás):\s*', '', t)
    ki = []
    for seg in [x.strip() for x in t.split(' · ')]:
        seg = re.sub(r'^(?:Forrás|forrás):\s*', '', seg).strip()
        if not seg or _KOD_RX.fullmatch(seg) or seg.startswith(('döntés:', 'lap-javit')) \
                or 'versszám-felmérése' in seg or re.match(r'U\d:', seg):
            continue
        seg = _KOD_RX.sub('', seg)
        seg = re.sub(r';\s*szavazat:\s*[\d,– -]+\)', ')', seg)
        seg = re.sub(r'\s*\(szavazat:\s*[\d, –-]+\)', '', seg)
        seg = _DATUM_RX.sub('', seg)
        if seg.startswith('a jelentés címkéje:'):
            seg = 'a jelentés: ' + _jelentes_olvasoi(seg[len('a jelentés címkéje:'):])
        if seg == 'a héber szöveg (TAHOT) hatókörén kívül':
            seg = 'újszövetségi hely: a szó a görög szövegből (TAGNT)' if ujszov else \
                'a héber szöveg-igazolás itt nem alkalmazható'
        if seg.startswith('teljesség-mérés'):
            m = re.search(r'csoportos sor:\s*([\d\s]+) vers', seg)
            seg = 'csoportos kizárás, %s vers' % m.group(1).strip() if m else 'a teljességi keresés csoportos kizárása'
        if seg.startswith('négy forrás összevetése'):
            seg = 'a motívum korábbi kereszthivatkozás-naplója'
        seg = re.sub(r'^Strong-keresés:', 'szókeresés:', seg)
        seg = seg.replace('a jelöltek döntésnaplója', 'a jelöltek döntései')
        for nev in _MUNKA_NEVEK:
            seg = re.sub(r';?\s*' + re.escape(nev), '', seg)
        seg = re.sub(r'\s+', ' ', seg).strip(' ;,')
        if seg and seg not in ki:
            ki.append(seg)
    if not ki:
        return ''
    s = '; '.join(ki)
    s = ('Forrás: ' + s) if forras_elotag else (s[:1].upper() + s[1:])
    return s + ('' if s.endswith('.') else '.')


def olvasoi_forrasnevek(t):
    """A „Forrás:” sor forrásművei: dátum, munkaanyag, állítás-címke és ismétlés nélkül."""
    t = _KOMMENT_RX.sub('', t)
    nevek = []
    for resz in re.split(r'\s·\s|;\s*', t):
        resz = re.sub(r'^.*?:\s*forrás:\s*', '', resz)          # „az X: forrás: Y” → Y
        resz = re.sub(r'^(?:Forrás|forrás):\s*', '', resz).strip()
        resz = _DATUM_RX.sub('', resz).strip(' ,.')
        if not resz or resz in _MUNKA_NEVEK or ':' in resz:
            continue
        if resz not in nevek:
            nevek.append(resz)
    return nevek


_USZ_RX = re.compile(r'\]\(#ige-(?:mt|mk|luk|ján|apcsel|róm|1kor|2kor|gal|ef|fil|kol|1thessz|2thessz|1tim|2tim|tit|'
                     r'filem|zsid|jak|1pét|2pét|1ján|2ján|3ján|júd|jel)-')


def alkalmaz(szoveg):
    """A lap olvasói jegyzet- és forrássorai (a modul leírása szerint)."""
    sorok = szoveg.split('\n')
    defs = {}                       # azonosító -> (látható szöveg, a rejtett megjegyzések)
    for s in sorok:
        m = _LABJ_DEF_RX.match(s)
        if m:
            defs[m.group(1)] = (m.group(2), ''.join(_KOMMENT_RX.findall(m.group(2))))
    ujszov_ref = {x for s in sorok if s.startswith('|') and _USZ_RX.search(s) for x in _LABJ_REF_RX.findall(s)}

    ki, i = [], 0
    while i < len(sorok):
        s = sorok[i]
        md = _LABJ_DEF_RX.match(s)
        if md:
            azon = md.group(1)
            olv = olvasoi_jegyzet(defs[azon][0], ujszov=azon in ujszov_ref)
            ki.append('[^%s]: %s%s' % (azon, olv or 'Forrás: a lap adatai.', defs[azon][1]))
            i += 1
            continue
        t = s.strip()
        # a közös forrásmegjelölések feloldása: rejtett megjegyzésbe (a jel a jegyzetekben nem áll)
        if _JELMAGYARAZAT_RX.match(t):
            lathato = _KOMMENT_RX.sub('', t).strip('*').replace('--', '—')
            ki.append('<!-- közös forrásmegjelölés: %s -->%s' % (lathato, ''.join(_KOMMENT_RX.findall(t))))
            i += 1
            continue
        # a szakaszvégi „Forrás:” sor: a forrásművek neve, dátum és munkaanyag nélkül
        m = _FORRAS_SOR_RX.match(t)
        if m and (_DATUM_RX.search(m.group(3)) or any(n in m.group(3) for n in _MUNKA_NEVEK)):
            nevek = olvasoi_forrasnevek(m.group(3))
            if nevek:
                rejtett = ''.join(_KOMMENT_RX.findall(t))
                if not rejtett:
                    rejtett = '<!-- eredeti: %s -->' % _KOMMENT_RX.sub('', t).replace('--', '—')
                ki.append('*%s%s: %s%s%s*%s' % (m.group(1), m.group(2), '; '.join(nevek),
                                                '' if m.group(4) else '.', m.group(4), rejtett))
                i += 1
                continue
        ki.append(s)
        i += 1
    return _szam_link_nevelo(re.sub(r'\n{3,}', '\n\n', '\n'.join(ki)))


_SZAM_LINK_RX = re.compile(r'(?<![\w-])([Aa]z?) \[(\d+)\.')


def _szam_link_nevelo(szoveg):
    """A számozott szakaszra mutató link előtti névelő a számhoz igazodik (a lektor és a Fable közös véleménye, 5.: „az
    [2. Előfordulások]” → „a [2. Előfordulások]”; a link a szakaszok átszámozásakor kapja az új számot)."""
    def csere(m):
        n = int(m.group(2))
        jo = 'az' if n == 1 or str(n)[0] == '5' or 1000 <= n < 2000 else 'a'
        if m.group(1)[0] == 'A':
            jo = jo.capitalize()
        return '%s [%s.' % (jo, m.group(2))
    return _SZAM_LINK_RX.sub(csere, szoveg)
