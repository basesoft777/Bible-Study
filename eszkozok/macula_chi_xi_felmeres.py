#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macula_chi_xi_felmeres.py -- a Macula heber `gorog_lxx` mezo chi<->xi csereje: felmeres (csak olvas).

Ket resz:
  (1) --upstream-xml <fajl>: egy letoltott macula-hebrew lowfat XML `greek` attributumaban
      megszamolja a megadott toveket (alapertelmezes: ἀρξ / ἀρχ, ψυξ / ψυχ).
  (2) a konkordancia/Macula_heber_*.tsv `gorog_lxx` mezoje vs. a Rahlfs-LXX
      (konkordancia/LXX_OS/*.tsv, `igehely_karoli` kulcs, minden szovegforma).

Illesztesi szabaly (2): a Macula-sor `karoli` versei (;-vel tagolva) -> az LXX_OS ugyanazon
Karoli-kulcsu tokenjei. Pozicio-mutato a Maculaban nincs (a `greek` attributum mellett nincs
LXX-tokenazonosito), ezert a "hely" = a Karoli-vers, a szo = beture (NFC) azonos szoalak.
  A valtozat: csak a szoalak egyezik egy tokennel a versben;
  B valtozat: a szoalak ES a Strong (gorog_strong = LXX_OS strong) is ugyanazon a tokenen.
Osztalyok soronkent (a `gorog_lxx` minden szavara kulon, a sor osztalya a szavak osszesitese):
  igazolt_csere     -- a csere-alak egyezik, az eredeti nem
  igazolt_eredeti   -- az eredeti egyezik, a csere-alak nem
  ketertelmu        -- mindketto megvan a versben (nem talalgatunk: nem igazolt)
  nem_igazolt:<ok>  -- egyik sem; ok: nincs_karoli | nincs_lxx_vers | csak_kisbetu | csak_ekezet | nincs_egyezes

Futtatas:
  python eszkozok/macula_chi_xi_felmeres.py [--upstream-xml <fajl>] [--naplo <md>] [--reszlet <tsv>]
A --reszlet a nem igazolt / ketertelmu sorokat irja (a repon kivulre ajanlott).
"""

import argparse
import glob
import os
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONK = os.path.join(GYOKER, 'konkordancia')
CSERE = str.maketrans({'χ': 'ξ', 'ξ': 'χ', 'Χ': 'Ξ', 'Ξ': 'Χ'})
CHIXI = set('χξΧΞ')


def ma():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d')


def nfc(s):
    return unicodedata.normalize('NFC', s or '')


def ekezettelen(s):
    s = unicodedata.normalize('NFD', s or '')
    return unicodedata.normalize('NFC', ''.join(c for c in s if unicodedata.category(c) != 'Mn')).lower()


def tsv(ut):
    """(fejlec, sorok) -- `#` megjegyzes-sorok nelkul; split('\\t') (CLAUDE.md: csv modul tilos)."""
    fej, sorok = None, []
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if not sor or sor.startswith('#'):
                continue
            mezok = sor.split('\t')
            if fej is None:
                fej = mezok
            else:
                sorok.append(mezok)
    return fej, sorok


def strong_norm(s):
    s = (s or '').strip().upper().lstrip('G')
    try:
        return str(int(s))
    except ValueError:
        return s


# ---------------------------------------------------------------- (1) upstream XML
def upstream(xml, tovek):
    import xml.etree.ElementTree as ET
    db = Counter()
    w_greek = 0
    for _, el in ET.iterparse(xml):
        if el.tag == 'w':
            g = nfc(el.get('greek', ''))
            if g:
                w_greek += 1
                for t in tovek:
                    db[t] += g.count(t)
            el.clear()
    return w_greek, db


# ---------------------------------------------------------------- (2) LXX_OS index
def lxx_index():
    """karoli-igehely -> [(szoalak_nfc, strong_norm, szovegforma)]"""
    ix = defaultdict(list)
    for ut in sorted(glob.glob(os.path.join(KONK, 'LXX_OS', '*.tsv'))):
        fej, sorok = tsv(ut)
        if not fej or not {'igehely_karoli', 'szoalak', 'strong'} <= set(fej):
            continue
        i_k, i_sz, i_st = fej.index('igehely_karoli'), fej.index('szoalak'), fej.index('strong')
        forma = os.path.splitext(os.path.basename(ut))[0]
        for s in sorok:
            if len(s) <= max(i_k, i_sz, i_st) or not s[i_k]:
                continue
            ix[s[i_k]].append((nfc(s[i_sz]), strong_norm(s[i_st]), forma))
    return ix


def szo_osztaly(eredeti, csere, strong, tokenek, B):
    """Egy gorog szo osztalya a vers tokenjein. B: Strong-egyezes is kell ugyanazon a tokenen."""
    def van(alak):
        hit = [t for t in tokenek if t[0] == alak and (not B or not strong or t[1] == strong)]
        return hit
    he, hc = van(eredeti), van(csere)
    if hc and not he:
        return 'igazolt_csere', hc
    if he and not hc:
        return 'igazolt_eredeti', he
    if he and hc:
        return 'ketertelmu', he + hc
    alakok = {t[0] for t in tokenek}

    def oldal(fn):
        # melyik alak illeszkedik lazan: (csere) / (eredeti) / (mindketto) -- csak diagnosztika
        c, e = any(fn(a) == fn(csere) for a in alakok), any(fn(a) == fn(eredeti) for a in alakok)
        return '(mindketto)' if c and e else '(csere)' if c else '(eredeti)' if e else None
    if B and (eredeti in alakok or csere in alakok):
        return 'nem_igazolt:strong_elteres' + oldal(lambda x: x), []
    o = oldal(str.lower)
    if o:
        return 'nem_igazolt:csak_kisbetu' + o, []
    o = oldal(ekezettelen)
    if o:
        return 'nem_igazolt:csak_ekezet' + o, []
    return 'nem_igazolt:nincs_egyezes', []


def sor_osztaly(osztalyok):
    """A sor szavainak osztalyabol: ha minden chi/xi-s szo igazolt es egyfele -> az; kulonben a legrosszabb."""
    s = set(osztalyok)
    if len(s) == 1:
        return osztalyok[0]
    if s <= {'igazolt_csere', 'igazolt_eredeti'}:
        return 'vegyes_igazolt'
    for o in ('ketertelmu',):
        if o in s:
            return o
    return sorted(x for x in s if x.startswith('nem_igazolt'))[0] if any(x.startswith('nem_igazolt') for x in s) else 'vegyes'


def felmeres(ix):
    eredm = {'A': Counter(), 'B': Counter()}
    konyv = {'A': defaultdict(Counter), 'B': defaultdict(Counter)}
    tovek = Counter()
    eredm_sor = {'A': {}, 'B': {}}
    alap = Counter()       # chi/xi nelkuli nem ures sorok: egyezik-e a Rahlfs-szal (kontroll)
    osszes = nem_ures = erintett = chi = xi = 0
    forma_hit = Counter()
    reszlet = []
    psy = []
    for ut in sorted(glob.glob(os.path.join(KONK, 'Macula_heber_*.tsv'))):
        knev = os.path.basename(ut)[len('Macula_heber_'):-4]
        fej, sorok = tsv(ut)
        i = {n: k for k, n in enumerate(fej)}
        for s in sorok:
            osszes += 1
            g = nfc(s[i['gorog_lxx']]).strip()
            if not g:
                continue
            nem_ures += 1
            karoli = [k for k in s[i['karoli']].split(';') if k]
            tokenek = [t for k in karoli for t in ix.get(k, [])]
            strong = strong_norm(s[i['gorog_strong']])
            if not (set(g) & CHIXI):
                if tokenek:
                    alap['van_lxx'] += 1
                    if all(any(t[0] == w for t in tokenek) for w in g.split()):
                        alap['egyezik'] += 1
                else:
                    alap['nincs_lxx'] += 1
                continue
            erintett += 1
            chi += any(c in 'χΧ' for c in g)
            xi += any(c in 'ξΞ' for c in g)
            if 'ψυχ' in g:
                psy.append((s[i['ref']], s[i['karoli']], g, g.translate(CSERE)))
            for w in g.split():
                for to in ('ψυχ', 'ψυξ', 'ἀρχ', 'ἀρξ', 'ξηρ', 'χηρ', 'ξύλ', 'χύλ'):
                    if to in w:
                        tovek[to] += 1
            for valt in ('A', 'B'):
                if not karoli:
                    o = 'nem_igazolt:nincs_karoli'
                elif not tokenek:
                    o = 'nem_igazolt:nincs_lxx_vers'
                else:
                    oszt = []
                    for w in g.split():
                        if set(w) & CHIXI:
                            ow, hit = szo_osztaly(w, w.translate(CSERE), strong, tokenek, valt == 'B')
                            oszt.append(ow)
                            if valt == 'B' and ow.startswith('igazolt'):
                                forma_hit[','.join(sorted({h[2] for h in hit}))] += 1
                    o = sor_osztaly(oszt)
                eredm[valt][o] += 1
                eredm_sor[valt][(s[i['ref']], g)] = o
                konyv[valt][knev][o] += 1
                if valt == 'B' and not o.startswith('igazolt'):
                    reszlet.append([knev, s[i['xml_id']], s[i['ref']], s[i['karoli']], g, g.translate(CSERE),
                                    s[i['gorog_strong']], o])
    return dict(osszes=osszes, nem_ures=nem_ures, erintett=erintett, chi=chi, xi=xi, eredm=eredm,
                konyv=konyv, tovek=tovek, alap=alap, forma_hit=forma_hit, reszlet=reszlet, psy=psy, eredm_sor=eredm_sor)


OSZTALYOK = ['igazolt_csere', 'igazolt_eredeti', 'vegyes_igazolt', 'ketertelmu', 'nem_igazolt:nincs_karoli',
             'nem_igazolt:nincs_lxx_vers', 'nem_igazolt:strong_elteres', 'nem_igazolt:csak_kisbetu', 'nem_igazolt:csak_ekezet',
             'nem_igazolt:nincs_egyezes', 'vegyes']


def pct(a, b):
    return '%.1f%%' % (100.0 * a / b) if b else '–'


def jelentes(r, up, prov):
    L = []
    if up:
        xml, w_greek, db = up
        L.append('## (1) Upstream XML\n')
        L.append('`%s`: `greek` attributummal bíró `<w>` elem: %d' % (os.path.basename(xml), w_greek))
        for t, n in db.items():
            L.append('- `%s`: %d' % (t, n))
        L.append('')
    L.append('## (2) Macula `gorog_lxx` vs. Rahlfs (LXX_OS)\n')
    L.append('- összes sor: %d; nem üres `gorog_lxx`: %d' % (r['osszes'], r['nem_ures']))
    L.append('- χ-t vagy ξ-t tartalmazó (érintett) sor: %d (χ-s: %d, ξ-s: %d)' % (r['erintett'], r['chi'], r['xi']))
    a = r['alap']
    L.append('- kontroll (χ/ξ nélküli nem üres sor): LXX-verssel %d, ebből betűre egyező %d (%s); LXX-vers nélkül %d'
             % (a['van_lxx'], a['egyezik'], pct(a['egyezik'], a['van_lxx']), a['nincs_lxx']))
    L.append('- tövek (szóelőfordulás): ' + ', '.join('`%s` %d' % (t, n) for t, n in sorted(r['tovek'].items())))
    L.append('')
    L.append('| osztály | A (alak) | A % | B (alak + Strong) | B % |')
    L.append('|---|---:|---:|---:|---:|')
    kulcsok = set(r['eredm']['A']) | set(r['eredm']['B'])
    rend = lambda k: (next((n for n, o in enumerate(OSZTALYOK) if k.startswith(o)), 99), k)
    for o in sorted(kulcsok, key=rend):
        na, nb = r['eredm']['A'][o], r['eredm']['B'][o]
        if na or nb:
            L.append('| `%s` | %d | %s | %d | %s |' % (o, na, pct(na, r['erintett']), nb, pct(nb, r['erintett'])))
    L.append('')
    L.append('Igazoló szövegforma (B, szavanként): ' + ', '.join('%s %d' % kv for kv in r['forma_hit'].most_common()))
    L.append('')
    L.append('### Könyvenként\n')
    L.append('| könyv | érintett | A igazolt_csere | A % | B % | A igazolt_eredeti | A kétértelmű | A csak kis/nagybetű | '
             'A csak ékezet | A nincs egyezés | nincs Károli/LXX-vers |')
    L.append('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for k in sorted(r['konyv']['A']):
        c, cb = r['konyv']['A'][k], r['konyv']['B'][k]
        ossz = sum(c.values())

        def kezd(cc, p):
            return sum(v for o, v in cc.items() if o.startswith(p))
        L.append('| %s | %d | %d | %s | %s | %d | %d | %d | %d | %d | %d |' % (
            k, ossz, c['igazolt_csere'], pct(c['igazolt_csere'], ossz), pct(cb['igazolt_csere'], ossz),
            c['igazolt_eredeti'], c['ketertelmu'], kezd(c, 'nem_igazolt:csak_kisbetu'), kezd(c, 'nem_igazolt:csak_ekezet'),
            c['nem_igazolt:nincs_egyezes'], c['nem_igazolt:nincs_karoli'] + c['nem_igazolt:nincs_lxx_vers']))
    L.append('')
    L.append('### A `ψυχ`-tövű sorok (a 2026-10-05-i mérés „5 helyes” sora)\n')
    L.append('| ref | Károli | gorog_lxx | csere | A osztály |')
    L.append('|---|---|---|---|---|')
    for ref, k, g, c in r['psy']:
        L.append('| %s | %s | %s | %s | `%s` |' % (ref, k, g, c, r['eredm_sor']['A'].get((ref, g), '')))
    L.append('')
    L.append('*(%s)*' % prov)
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--upstream-xml')
    ap.add_argument('--tovek', default='ἀρξ,ἀρχ,ψυξ,ψυχ')
    ap.add_argument('--naplo', help='a jelentés markdown-részlete ide (különben stdout)')
    ap.add_argument('--reszlet', help='nem igazolt / kétértelmű sorok TSV-je (B változat)')
    a = ap.parse_args()
    up = None
    if a.upstream_xml:
        tovek = [nfc(t) for t in a.tovek.split(',')]
        w, db = upstream(a.upstream_xml, tovek)
        up = (a.upstream_xml, w, db)
    ix = lxx_index()
    r = felmeres(ix)
    prov = ('proveniencia: scope=konkordancia/Macula_heber_*.tsv (gorog_lxx) × konkordancia/LXX_OS/*.tsv '
            '(igehely_karoli, minden szövegforma) | forras=eszkozok/macula_chi_xi_felmeres.py | ts=%s' % ma())
    szoveg = jelentes(r, up, prov)
    if a.naplo:
        with open(a.naplo, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg + '\n')
    print(szoveg)
    if a.reszlet:
        with open(a.reszlet, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\t'.join(['konyv', 'xml_id', 'ref', 'karoli', 'gorog_lxx', 'csere', 'gorog_strong', 'osztaly']) + '\n')
            for s in r['reszlet']:
                f.write('\t'.join(s) + '\n')


if __name__ == '__main__':
    main()
