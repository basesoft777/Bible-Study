#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
muhelynaplo.py -- az új szerkezetű lexikonlap műhelyszövegének kiválasztása és a műhelynapló-melléklet
(`lexikon/[ID]_MUHELYNAPLO.md`) előállítása (lap-javit HAMART-001, a felhasználó átnézése, S1–S2; a felhasználó:
„ezért kellene ott lennie minden ilyen naplónak”).

A lap olvasói helyén (táblajegyzet, dőlt bevezető, „Forrás:” sor) műhelyszöveg nem áll. A lap kész szövegén fut, a
generálás legvégén, csak az új szerkezetű lapon:
  - a táblák Markdown-lábjegyzetei (`[^x]`) helyi jegyzetlistává válnak a tábla alatt; a jegyzet látható szövege
    olvasói (forrásnév, a jelentés rövid megnevezése), dátum, belső kód (‹E1›), szavazatszám, felmérés-rész nélkül; az
    azonos olvasói szövegű jegyzetek egyszer állnak (S2), helyi számmal (`2.5`), a cellában hivatkozással;
  - a jegyzet száma a melléklet sorazonosítója (`#j-2-5`): ott áll a jegyzet minden eredeti lábjegyzete a teljes,
    nyers proveniencia-sorral (CLAUDE.md 1. szabály: a sor nem tűnik el, a mellékletbe költözik, a lapról linkkel);
  - a szakaszvégi „*Forrás: …*” sor a forrásművek nevére rövidül, dátum és munkaanyag nélkül, linkkel a melléklet
    soráig (`#f-…`), ahol a teljes sor áll;
  - a közös forrásmegjelölések jelmagyarázata (‹E1› = …) és a lap rejtett `<!-- eredeti: … -->` megjegyzései a
    mellékletbe költöznek.
A melléklet új adatforrást nem hoz: ugyanazt az adatot mutatja, mint az adattáblák proveniencia-mezői.
"""
import collections
import re

MUHELYNAPLO_UTOTAG = '_MUHELYNAPLO.md'

_KOMMENT_RX = re.compile(r'<!--.*?-->', re.S)
_EREDETI_RX = re.compile(r'<!-- eredeti: (.*?) -->', re.S)
_LABJ_DEF_RX = re.compile(r'^\[\^([\w.-]+)\]:\s?(.*)$')
_LABJ_REF_RX = re.compile(r'\[\^([\w.-]+)\]')
_DATUM_RX = re.compile(r',?\s*\b20\d\d[-.]\d\d[-.]\d\d\b(?:\s*\([a-z]\))?')
_KOD_RX = re.compile(r'‹[A-Z]\d+›')
_FORRAS_SOR_RX = re.compile(r'^\*Forrás:\s*(.*?)\*\s*$')
_JELMAGYARAZAT_RX = re.compile(r'^\*(?:A közös forrásmegjelölések|Minden sor forrásmegjelölése)')

# a nevekből kimaradó munka-megnevezések (S1)
_MUNKA_NEVEK = ('a lap munkaanyaga', 'a lap munkanaplója', 'kézi szerkesztés', 'a lap adattáblája')


def _szakasz_azon(cim):
    m = re.match(r'^#{2}\s+(\d+)\.', cim)
    if m:
        return m.group(1)
    t = re.sub(r'^#+\s+', '', cim).lower()
    return re.sub(r'[^a-z0-9áéíóöőúüű]+', '-', t).strip('-')[:20] or 'lap'


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
    """Egy lábjegyzet látható szövegéből az olvasói jegyzet (S1): forrás és jelentés, műhelyszöveg nélkül."""
    t = _KOMMENT_RX.sub('', lathato).strip()
    if 'a sornak nincs Strong-száma' in t:
        return 'Tematikus hely: a versben a lánc szava nem áll.'
    t = re.sub(r'^(?:Forrás|forrás):\s*', '', t)
    ki = []
    for seg in [s.strip() for s in t.split(' · ')]:
        seg = re.sub(r'^(?:Forrás|forrás):\s*', '', seg).strip()
        if not seg or _KOD_RX.fullmatch(seg) or seg.startswith(('döntés:', 'lap-javit')) or 'versszám-felmérése' in seg \
                or re.match(r'U\d:', seg):
            continue
        seg = _KOD_RX.sub('', seg)
        seg = re.sub(r';\s*szavazat:\s*[\d,– -]+\)', ')', seg)
        seg = re.sub(r'\s*\(szavazat:\s*[\d, ]+\)', '', seg)
        seg = _DATUM_RX.sub('', seg)
        if seg.startswith('a jelentés címkéje:'):
            seg = 'a jelentés: ' + _jelentes_olvasoi(seg[len('a jelentés címkéje:'):])
        if seg == 'a héber szöveg (TAHOT) hatókörén kívül':
            seg = 'újszövetségi hely: a szó a görög szövegből (TAGNT)' if ujszov else 'a héber szöveg-igazolás itt nem alkalmazható'
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
    return s[:1].upper() + s[1:] + ('' if s.endswith('.') else '.')


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


# Dőlt bevezető sorok, amelyek műhelyszöveget hordoznak (S1): (minta, olvasói csere vagy None = csak a mellékletbe,
# beolvasztandó mondat az előző olvasói bevezetőbe vagy None). A teljes eredeti sor a mellékletbe kerül.
DOLT_SZABALYOK = (
    (r'^\*Ez a blokk a lexikon-oldal \d+ szakaszának tartalomjegyzékét adja', None, None),
    (r'^\*Ez a blokk közös, minden lexikon-oldalon szó szerint azonos szöveg', None, None),
    (r'^\*Ez a blokk a motívum \d+ igehely-sorát fedi',
     '*A „Jelentés (a szó)” oszlop a szó jelentését mutatja a szótár tagolásában, a „Funkció (a motívumban)” oszlop a '
     'hely szerepét a motívumban; az „UBS-jelentés” egy másik szótár (az UBS ószövetségi és újszövetségi szótára) '
     'versenkénti jelentése, az ⓘ a szónézetre mutat. A jegyzetek a tábla alatt állnak.*', None),
    (r'^\*Az UBS-jelentés az újszövetségi soroknál', None, None),
    (r'^\*Ez a blokk a motívum (\d+) Strong-számát fedi', r'*A szakasz a motívum \1 szavát mutatja, szótári '
     r'szempontonként (a szempontok rendje a Jelmagyarázatban).*', None),
    (r'^\*Az LXX-megfelelő versszintű együtt-előfordulás',
     '*Az LXX-megfelelő az a görög szó, amely a héber szó ószövetségi verseiben a görög Bibliában a leggyakrabban '
     'áll mellette (versenkénti, nem szavankénti összevetés); a motívum saját helyein álló görög szót a 9. szakasz '
     'mutatja, ezért a kettő eltérhet.*', None),
    (r'^\*Szótári tagolás \(szerkesztői döntés', None,
     ' Ahol a szótár a helyet nem idézi, ott jelentéspont sincs; a szótári blokk a szóról szól, a hely szerepét a '
     'motívumban a 2. szakasz adja.'),
    (r'^\*Összesítés: egyező=(\d+), eltérő=(\d+), LXX-minusz=(\d+), a megfelelő nincs megállapítva=(\d+), '
     r'versszámozás miatt nem párosítva=(\d+)\.\*$',
     r'*Összesítés: \1 egyező, \2 eltérő, \3 helyen hiányzik a görög szövegből, \4 helyen a megfelelő nincs '
     r'megállapítva, \5 vers a versszámozás miatt nem párosítható.*', None),
    (r'^\*Ez a blokk a motívum motívumközi kapcsolatait adja',
     '*A motívum kapcsolatai más motívumokkal; minden sor mögött szerkesztői döntés áll, és a sor mindkét motívum '
     'lapján megjelenik.*', None),
    (r'^\*Döntésre váró motívumközi jelölt \([^)]*\): (\d+) — ([\w-]+): \d+\.\*$',
     r'*Döntésre vár még \1 motívumközi kapcsolat (\2).*', None),
    (r'^\*Generált a kapcsolat-tábla indoklás mezőjéből', None, None),
    (r'^\*A magyar szöveg a szakaszonkénti (?:Thayer|BDB)-fordításból', None, None),
    (r'^\*ⓘ Kutatói megjegyzés:', None, None),
    (r'^\*Hivatkozás: a motívum saját szavaihoz nincs LSJ-sor',
     '*A klasszikus görög nagyszótár (LSJ) adata a motívum szavaihoz a lap forrásaiban nem áll rendelkezésre.*', None),
    (r'^\*Ez a blokk a motívum (\d+) kapcsolat-sorát fedi \(forrás: a kapcsolat-tábla\), (\d+) igehely-csomóponttal\.',
     r'*A blokk a motívum \1 kapcsolatát mutatja, \2 helyet összekötve.', None),
)


def s1_tisztit(s):
    """Az olvasói sor műhely-maradékai (S1): a TSK-szavazat és a „Votes” jelölés."""
    s = re.sub(r',\s*szavazat:\s*\d[\d,–-]*(?:\s*,\s*\d[\d–-]*)*', '', s)
    s = re.sub(r'\s*\(Votes:?\s*\d+\)', '', s)
    s = re.sub(r'TSK \(Votes (\d+)\)', 'TSK', s)
    s = s.replace('(Votes ≥ 15)', '(legalább 15 olvasói szavazat)')
    return s


def kivalaszt(szoveg, mid):
    """(lap, melléklet). A lap olvasói alakja és a műhelynapló-melléklet szövege."""
    sorok = szoveg.split('\n')
    mell_link = '%s%s' % (mid, MUHELYNAPLO_UTOTAG)
    # 1. a lábjegyzet-definíciók begyűjtése
    defs = {}
    szakasz, szak_ut = 'lap', {}
    for s in sorok:
        if re.match(r'^#{2,3}\s', s):
            szakasz = _szakasz_azon(s) if s.startswith('## ') else szakasz
        m = _LABJ_DEF_RX.match(s)
        if m:
            defs[m.group(1)] = (m.group(2), szakasz)
    # csak a táblában hivatkozott lábjegyzet válik helyi jegyzetté; a többi Markdown-lábjegyzet marad
    tabla_ref = {x for s in sorok if s.startswith('|') for x in _LABJ_REF_RX.findall(s)}
    # 2. bejárás
    ki, mell = [], collections.OrderedDict()   # mell: szakasz -> [md-sor]
    jegyz_sz = collections.Counter()
    szakasz, szak_cim = 'lap', 'A lap eleje'
    i = 0
    forras_sz = collections.Counter()

    def mell_add(sz, cim, sor):
        mell.setdefault((sz, cim), []).append(sor)

    while i < len(sorok):
        s = sorok[i]
        if s.startswith('## '):
            szakasz, szak_cim = _szakasz_azon(s), s[3:].strip()
        md = _LABJ_DEF_RX.match(s)
        if md and md.group(1) in tabla_ref:
            i += 1
            if i < len(sorok) and not sorok[i].strip() and ki and not ki[-1].strip():
                i += 1
            continue
        # táblablokk
        if s.startswith('|'):
            blokk = []
            while i < len(sorok) and sorok[i].startswith('|'):
                blokk.append(sorok[i])
                i += 1
            helyi = collections.OrderedDict()   # olvasói szöveg -> (szám, [eredeti azonosítók])
            uj_blokk = []
            for b in blokk:
                ujszov = bool(re.search(r'\]\(#ige-(?:mt|mk|luk|ján|apcsel|róm|1kor|2kor|gal|ef|fil|kol|1thessz|2thessz|'
                                        r'1tim|2tim|tit|filem|zsid|jak|1pét|2pét|1ján|2ján|3ján|júd|jel)-', b))

                def csere(mm):
                    azon = mm.group(1)
                    if azon not in defs:
                        return mm.group(0)
                    olv = olvasoi_jegyzet(defs[azon][0], ujszov=ujszov) or 'Forrás: a lap adatai.'
                    if olv not in helyi:
                        jegyz_sz[szakasz] += 1
                        helyi[olv] = ('%s.%d' % (szakasz, jegyz_sz[szakasz]), [])
                    szam, lista = helyi[olv]
                    if azon not in lista:
                        lista.append(azon)
                    return '<sup>[%s](#j-%s)</sup>' % (szam, szam.replace('.', '-'))
                b2 = _LABJ_REF_RX.sub(csere, b)
                for e in _EREDETI_RX.findall(b2):
                    mell_add(szakasz, szak_cim, '- táblasor: `%s`' % e.replace('`', "'")[:400])
                uj_blokk.append(_EREDETI_RX.sub('', b2))
            ki.extend(s1_tisztit(x) for x in uj_blokk)
            if helyi:
                ki.append('')
                for olv, (szam, lista) in helyi.items():
                    a = szam.replace('.', '-')
                    ki.append('- <a id="j-%s"></a><sup>[%s](%s#j-%s)</sup> %s' % (a, szam, mell_link, a, olv))
                    sor = ['### <a id="j-%s"></a>Jegyzet %s' % (a, szam), '', 'A lapon: %s' % olv, '']
                    for azon in lista:
                        lath, _sz = defs[azon]
                        nyers = _EREDETI_RX.findall(lath)
                        sor.append('- `[^%s]` %s' % (azon, _KOMMENT_RX.sub('', lath).strip()))
                        for n in nyers:
                            sor.append('  - nyers: `%s`' % n.replace('`', "'"))
                    sor.append('')
                    mell_add(szakasz, szak_cim, '\n'.join(sor))
            continue
        t = s.strip()
        # műhelyszöveget hordozó dőlt bevezető (S1)
        tk = _KOMMENT_RX.sub('', t)
        szab = next(((rx, cs, be) for rx, cs, be in DOLT_SZABALYOK if re.match(rx, tk)), None)
        if szab:
            rx, cs, be = szab
            mell_add(szakasz, szak_cim, '- dőlt bevezető: %s' % tk.strip('*'))
            if cs:
                ki.append(re.sub(rx + r'.*$', cs, tk) if cs.endswith('*') else re.sub(rx, cs, tk))
            if be:
                for k in range(len(ki) - 1, -1, -1):
                    if ki[k].strip():
                        if '<!-- olvasói -->' in ki[k]:
                            ki[k] = ki[k].replace('<!-- olvasói -->', be + '<!-- olvasói -->')
                        break
            i += 1
            if not cs and i < len(sorok) and not sorok[i].strip() and ki and not ki[-1].strip():
                i += 1
            continue
        # közös forrásmegjelölések jelmagyarázata
        if _JELMAGYARAZAT_RX.match(t):
            mell_add(szakasz, szak_cim, '- jelmagyarázat: %s' % _KOMMENT_RX.sub('', t).strip('*'))
            i += 1
            if i < len(sorok) and not sorok[i].strip() and ki and not ki[-1].strip():
                i += 1
            continue
        # a szakaszvégi „Forrás:” sor
        m = _FORRAS_SOR_RX.match(_KOMMENT_RX.sub('', t))
        if m and '_MUHELYNAPLO' not in t:
            forras_sz[szakasz] += 1
            a = 'f-%s-%d' % (szakasz, forras_sz[szakasz])
            nevek = olvasoi_forrasnevek(m.group(1))
            mell_add(szakasz, szak_cim, '### <a id="%s"></a>Forrás (%s)\n\n- a lapon: %s\n- teljes sor: %s%s\n' % (
                a, szak_cim, '; '.join(nevek) or '—', m.group(1),
                ''.join('\n- nyers: `%s`' % e.replace('`', "'") for e in _EREDETI_RX.findall(s))))
            ki.append('*Forrás: %s.* [részletek](%s#%s)' % ('; '.join(nevek) if nevek else 'a lap adatai', mell_link, a))
            i += 1
            continue
        # a lap többi rejtett „eredeti” megjegyzése
        if '<!-- eredeti:' in s:
            for e in _EREDETI_RX.findall(s):
                mell_add(szakasz, szak_cim, '- sor (%s): `%s`' % (_KOMMENT_RX.sub('', s).strip()[:80],
                                                                   e.replace('`', "'")[:600]))
            s = _EREDETI_RX.sub('', s)
        ki.append(s if s.startswith('#') else s1_tisztit(s))
        i += 1
    lap = '\n'.join(ki)
    lap = re.sub(r'\n{3,}', '\n\n', lap)
    return lap, melleklet(mid, mell)


def melleklet(mid, mell):
    ki = ['<!-- GENERÁLT: general.py --cel lexikon | melléklet: %s (műhelynapló) -->' % mid, '',
          '# 📎 %s — Műhelynapló (melléklet)' % mid, '',
          'A [%s lap](%s_TUDOMANYOS.md) műhelyadatai: a lap jegyzeteinek és forrássorainak teljes, nyers '
          'proveniencia-sora, a közös forrásmegjelölések, a döntések dátuma. A lap jegyzetszáma (pl. 2.5) ennek a '
          'mellékletnek a sorazonosítója. Új adatot nem hoz: ugyanazt mutatja, mint az adattáblák proveniencia-mezői.'
          % (mid, mid), '']
    for (sz, cim), sorok in mell.items():
        ki += ['## %s' % cim, '']
        ki += sorok
        ki.append('')
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(ki)).rstrip('\n') + '\n'
