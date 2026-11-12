#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tablajegyzet.py -- az új szerkezetű lexikonlap jegyzeteinek és forrássorainak olvasói alakja (lap-javit HAMART-001; a
felhasználó átnézése, 2. és 12. tétel, „Csak az A) csoport”).

A lap kész szövegén fut, a generálás végén, csak az új szerkezetű lapon. Blokk nem tűnik el, semmi nem kerül
mellékletbe. A táblák jegyzetei közvetlenül a tábla alá kerülnek, helyi számozott listába, az azonos jegyzet egyszer
(`tabla_ala`; a felhasználó v8-átnézése, 1.), és az önreferáló „lap” fordulat olvasói alakra vált (`onref_csere`, 4.).
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
    m = re.match(r'BDB-példa:\s*(.*?)(?:\s*\([^)]*(?:versenkénti jelentései|BDB-szótár|Thayer-szótár)\))?;\s*'
                 r'ez a szerkesztői hozzárendelés.*$', t)   # F212: a tábla „BDB-szótár” néven is
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
    # F212 (Kolofon-forrássor): a versenkénti jelentések táblája „BDB-szótár” néven fut; a jegyzetben nem ismétlődik
    return re.sub(r'\s*\(a [^)]*versenkénti jelentései\)|\s*\(a (?:BDB|Thayer)-szótár\)', '', t)


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
            m = re.search(r'(?:csoportos sor|blokk-sor)[^:]*:\s*([\d\s]+) vers', seg)   # F212: a „blokk-sor: N vers” is
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
            ki.append('[^%s]: %s%s' % (azon, olv or 'Forrás: a motívum adattáblái.', defs[azon][1]))
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
    return strong_szo_elol(onref_csere(_szam_link_nevelo(re.sub(r'\n{3,}', '\n\n', tabla_ala('\n'.join(ki))))))


_ALPONT_RX = re.compile(r'^#{3,5}\s+4\.(\d+)\.')
_HSOR_RX = re.compile(r'^\*\*([HG]\d{4,5}[a-z]?)\*\* · (.*)$')   # F212 (E2): a görög sor is a szóval kezd


def strong_szo_elol(szoveg):
    """A héber 4.5, 4.6 és 4.10 sorában elöl a szó, a Strong-szám hátul, a 4.1 mintájára (a v8-átnézés, kiadás előtti
    gyors kör, 4.): `**H0056** · …` → `**אָבַל (ával)** — … · H0056`; a 4.10-ben (ott a szó maga a tartalom)
    `**אָבַל (ával)** · H0056`. A szó a lap saját 4.10-es sorából (a szó és a magyaros kiejtése); ahol nincs, a sor
    változatlan. A görög sorok nem változnak."""
    sorok = szoveg.split('\n')
    szo, alpont = {}, None
    for s in sorok:
        m = _ALPONT_RX.match(s)
        if m:
            alpont = m.group(1)
        elif s.startswith('### '):
            alpont = None
        m = _HSOR_RX.match(s)
        if m and alpont == '10' and re.fullmatch(r'\S+ \([^()]+\)', m.group(2).strip()):
            szo[m.group(1)] = m.group(2).strip()
    if not szo:
        return szoveg
    ki, alpont = [], None
    for s in sorok:
        m = _ALPONT_RX.match(s)
        if m:
            alpont = m.group(1)
        elif s.startswith('### '):
            alpont = None
        m = _HSOR_RX.match(s)
        if m and alpont in ('5', '6', '10') and m.group(1) in szo:
            h, tobbi = m.group(1), m.group(2).rstrip()
            s = ('**%s** · %s' % (szo[h], h)) if alpont == '10' else ('**%s** — %s · %s' % (szo[h], tobbi, h))
        ki.append(s)
    return '\n'.join(ki)


# A felhasználó v8-átnézése (4. szabály): a „lap” szó az oldal önmagára utalásaként nem áll az olvasói szövegben.
# Itt csak az a szöveg cserélődik, amelynek a forrása a régi lapokon is fut (közös generátormondat), vagy egy adattábla
# cellája, amelyhez a nyílt mag angol fordítása kötődik (a forras_hash miatt az adatcella a fordítás új körével
# változik, l. a jelentést). A csak új szerkezetű generátormondatok és a próza a forrásukban javultak. A rejtett
# megjegyzésekben (proveniencia) nincs csere.
ONREF_CSERE = (
    # közös generátormondatok (OLVASOI_SABLON, Jelmagyarázat)
    ('A lap szakaszai. Hogy melyik szakaszt', 'A szócikk szakaszai. Hogy melyik szakaszt'),
    ('A lapon használt rövidítések, jelek és forrásnevek feloldása. Ha a lap egy jelét nem érted, itt keresd.',
     'A szócikkben használt rövidítések, jelek és forrásnevek feloldása. Ha a szócikk egy jelét nem érted, itt keresd.'),
    ('mondat a lap készítőinek szól.', 'mondat a szócikk készítőinek szól.'),
    ('Hogyan hivatkozz erre a lapra,', 'Hogyan hivatkozz erre a szócikkre,'),
    # adatcellák (motivumok.tsv, elutasitasi_okok.tsv / jeloltek.tsv, elofordulasok.tsv, kapcsolatok.tsv)
    ('ezeket a lap egyenként, tematikus helyként veszi fel.', 'ezeket a vizsgálat egyenként, tematikus helyként veszi fel.'),
    ('amelyet a lap nem dönt el', 'amelyet ez a vizsgálat nem dönt el'),
    ('azt a lap vitatott pontként tárgyalja', 'azt a szócikk vitatott pontként tárgyalja'),
    ('amely a lánc szavai nélkül áll a lapon,', 'amely a lánc szavai nélkül áll a listán,'),
)


def onref_csere(szoveg):
    """Az ONREF_CSERE párjai a látható szövegben (a `<!-- … -->` megjegyzéseken kívül)."""
    reszek = re.split(r'(<!--.*?-->)', szoveg, flags=re.S)
    for i in range(0, len(reszek), 2):
        for a, b in ONREF_CSERE:
            reszek[i] = reszek[i].replace(a, b)
    return ''.join(reszek)


# az olvasói kapu figyelmeztetése (a felhasználó v8-átnézése, 4.): önreferáló „lap” az új szerkezetű lap látható
# szövegében; kivétel a Kolofon (technikai adatok) és a más motívum lapjára utaló fordulat
ONREF_RX = re.compile(r'(?<![\w-])(?:[Aa] lap|[Ee]rre a lapra|[Aa] lapon|[Aa] lapra|[Aa] lapról)(?![\w-])')
ONREF_KIVETEL_RX = re.compile(r'motívum lapján|\[[^\]]*lap\]\(')


def onref_talalatok(szoveg):
    """[(sorszám, szakasz, részlet)] az önreferáló „lap” fordulatokról, a Kolofonon és a megjegyzéseken kívül."""
    ki, szakasz = [], ''
    lathato = _KOMMENT_RX.sub(lambda m: '\n' * m.group(0).count('\n'), szoveg)   # a sorszám a forrásé marad
    for n, sor in enumerate(lathato.split('\n'), 1):
        if sor.startswith('## '):
            szakasz = sor[3:].strip()
        if szakasz.startswith('Kolofon') or ONREF_KIVETEL_RX.search(sor):
            continue
        for m in ONREF_RX.finditer(sor):
            ki.append((n, szakasz, sor[max(0, m.start() - 40):m.end() + 40]))
    return ki


def _szakasz_szam(cim):
    m = re.match(r'^##\s+(\d+)\.', cim)
    return m.group(1) if m else None


# F212 (I4, a felhasználó döntése: „javaslat szerint”): a 3. (kizárt helyek) és a 6. (minősítés) táblájában a jelölés
# forrását a „Miért lett jelölt” cella már kimondja; az a jegyzet, amely csak ezt ismétli, elmarad. Ismétlő az a
# jegyzet, amelynek kulcsadata (a TSK-ajánlás helye, a keresett szó, a csoportos kizárás versszáma) a sorban már áll.
ISMETLO_SZAKASZ = ('3', '6')
_ISMETLO_RX = (
    (re.compile(r'^Forrás: TSK-ajánlás \(([^)]*)\)((?:; a Károli-kereszthivatkozás is)?)\.$'),
     lambda m, sor: all(h.strip() in sor for h in re.split(r',\s*', m.group(1))) and (not m.group(2) or 'Károli' in sor)),
    (re.compile(r'^Forrás: (?:szókeresés|szócsalád-keresés): (.*)\.$'), lambda m, sor: m.group(1).strip() in sor),
    (re.compile(r'^Forrás: csoportos kizárás, (\d+) vers\.$'), lambda m, sor: (' %s vers' % m.group(1)) in sor),
)


def ismetlo_jegyzet(lathato, sor):
    """Igaz, ha a jegyzet csak a sor cellájában már álló jelölési forrást ismétli (I4)."""
    for rx, feltetel in _ISMETLO_RX:
        m = rx.match(lathato)
        if m:
            return feltetel(m, sor)
    return False


def tabla_ala(szoveg):
    """A táblák jegyzetei a tábla alá, helyi számozott listába (a felhasználó v8-átnézése, 1.; a lektor javaslata).

    A táblasorban csak a jel áll (`2.5`); közvetlenül a tábla alatt a jegyzetlista. Az azonos szövegű jegyzet egyszer
    áll, több sor is mutathat rá. A szám a szakaszon belül folyamatos (egy szakasz több táblája nem ütközik). A rejtett
    `<!-- eredeti: … -->` megjegyzések a lista sorában maradnak (CLAUDE.md 1. szabály); mellékletbe semmi nem kerül.
    Számozott szakaszon kívüli tábla és táblán kívüli lábjegyzet változatlan marad."""
    sorok = szoveg.split('\n')
    defs = {}
    for s in sorok:
        m = _LABJ_DEF_RX.match(s)
        if m:
            defs[m.group(1)] = m.group(2)
    # a tábla alá kerülő lábjegyzetek: számozott szakasz táblájában hivatkozottak
    szakasz, tabla_ref = None, set()
    for s in sorok:
        if s.startswith('## '):
            szakasz = _szakasz_szam(s)
        if szakasz and s.startswith('|'):
            tabla_ref.update(x for x in _LABJ_REF_RX.findall(s) if x in defs)
    if not tabla_ref:
        return szoveg
    ki, i, szakasz, sorszam = [], 0, None, {}
    while i < len(sorok):
        s = sorok[i]
        if s.startswith('## '):
            szakasz = _szakasz_szam(s)
        md = _LABJ_DEF_RX.match(s)
        if md and md.group(1) in tabla_ref:
            i += 1
            continue
        if not (szakasz and s.startswith('|')):
            ki.append(s)
            i += 1
            continue
        blokk = []
        while i < len(sorok) and sorok[i].startswith('|'):
            blokk.append(sorok[i])
            i += 1
        helyi = {}                     # látható olvasói szöveg -> [szám, [rejtett megjegyzések]]
        sor_most = ['']

        def csere(mm):
            azon = mm.group(1)
            if azon not in tabla_ref:
                return mm.group(0)
            lathato = _KOMMENT_RX.sub('', defs[azon]).strip()
            if szakasz in ISMETLO_SZAKASZ and ismetlo_jegyzet(lathato, sor_most[0]):
                return ''               # F212 (I4): a jegyzet a cellát ismétli; a jel és a jegyzet elmarad
            if lathato not in helyi:
                sorszam[szakasz] = sorszam.get(szakasz, 0) + 1
                helyi[lathato] = ['%s.%d' % (szakasz, sorszam[szakasz]), []]
            szam, rejtett = helyi[lathato]
            for k in _KOMMENT_RX.findall(defs[azon]):
                if k not in rejtett:
                    rejtett.append(k)
            return '<sup class="lj"><a href="#j-%s">%s</a></sup>' % (szam.replace('.', '-'), szam)
        for b in blokk:
            sor_most[0] = _LABJ_REF_RX.sub('', b)
            ki.append(_LABJ_REF_RX.sub(csere, b))
        if helyi:
            ki.append('')
            for lathato, (szam, rejtett) in helyi.items():
                ki.append('- <span class="lj-szam" id="j-%s">%s</span>%s%s' % (szam.replace('.', '-'), szam, lathato,
                                                                             ''.join(rejtett)))
            ki.append('')
    return '\n'.join(ki)


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
