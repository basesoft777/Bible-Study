"""Nehéz esetek mintája a gépi magyaros héber kiejtés bekötése előtt
(DT-F131y ⛔ feltétele; N-F131w). Kísérleti, csak naplót ír:
  naplok/HEBER_KIEJTES_nehez_minta.tsv

A lexikonlapok (lexikon/*_TUDOMANYOS.md) motívumainak héber előfordulásaiból
(adat/elofordulasok.tsv) veszi a verseket, a TAHOT-ból (konkordancia/
TAHOT_kivonat.tsv) TELJES szót rak össze (előtag + tő + toldalék, DT-F131y (5)),
és a motívum Strongján álló szavakból rögzített seed-del (20261030) mintát vesz
hat nehéz kategóriából: kámec kátán gyanú, nem szókezdő sevá, furtív patah,
dáges forte, ketiv/qere, makkef.

A gépi kiejtés a naplok/HEBER_KIEJTES_meres.py NIQQUD-átírójával készül, a
DT-F131y konvencióival: ס és שׂ = sz, a szókezdő begadkefatról a pontozás dönt,
szókezdő kötőszói וּ = ú, makkef előtti zárt szótag kámece = o.

TSV: split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import os
import random
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'naplok'))
import HEBER_KIEJTES_meres as m  # noqa: E402

KIMENET = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_nehez_minta.tsv')
SEED = 20261030
KVOTA = [('kamec_katan_gyanu', 10), ('nem_szokezdo_seva', 10), ('furtiv_patah', 8),
         ('dages_forte', 8), ('ketiv_qere', 6), ('makkef', 8)]

P = m.a_priori(m.PARAM_TER_NIQQUD)
P.update({'szamech': 'sz', 'sin': 'sz', 'szokezdo_begadkefat': 'pont_szerint',
          'kotoszo_u': True, 'makkef_katan': True})
# Alternatíva (összevetésre): a kámec alapból gádol, kátán csak pozitív jelre
# (U+05C7, makkef előtti zárt szótag); a hosszú magánhangzó utáni sevá kiejtett.
P_ALT = dict(P)
P_ALT.update({'kamec_katan': False, 'seva_hosszu_utan': 'hangzo'})


ELOTAGOK = {'H900%d' % i for i in range(1, 10)}


def heber(s):
    return any(m.ALEF <= c <= m.TAV for c in s)


def lexikon_motivumok():
    d = os.path.join(ROOT, 'lexikon')
    return sorted(f[:-len('_TUDOMANYOS.md')] for f in os.listdir(d) if f.endswith('_TUDOMANYOS.md'))


def celhelyek(motivumok):
    """{igehely: {strong4: set(motivum)}} -- a lexikon-motívumok héber előfordulásai."""
    ki = {}
    for r in m.tsv_sorok(m.ELOFORDULASOK, 'id'):
        if r['id'] not in motivumok:
            continue
        for st in r['strong'].split('+'):
            st = st.strip()
            if st.startswith('H') and st[1:5].isdigit():
                ki.setdefault(r['igehely'], {}).setdefault(st[:5], set()).add(r['id'])
    return ki


def szavak(helyek):
    """A TAHOT sorainak összerakása teljes szóvá a célversekben.
    Előtag: H9001-H9009 (vav, elöljárók, -ש, kérdő hé, névelő); toldalék: H9010-től
    (irányjelölő hé, paragogikus nun, névmási toldalékok, pl. Ps3m). Makkef: a szó utolsó elemének STEP-átírása '-'-re végződik."""
    soronkent = {}
    with open(m.TAHOT, encoding='utf-8') as f:
        next(f)
        for l in f:
            r = l.rstrip('\n').split('\t')
            if len(r) < 5 or r[0] not in helyek:
                continue
            soronkent.setdefault(r[0], []).append(r)
    ki = []
    for hely, sorok in soronkent.items():
        elotag = []
        aktualis = None
        for r in sorok:
            st, alak, step, szoto = r[1], r[2], r[3], r[4]
            if st[:5] in ELOTAGOK:
                if aktualis:
                    ki.append(aktualis)
                    aktualis = None
                elotag.append(r)
                continue
            if st.startswith('H9') and aktualis:
                aktualis['reszek'].append(r)
                continue
            if aktualis:
                ki.append(aktualis)
            aktualis = {'igehely': hely, 'strong': st[:5], 'reszek': elotag + [r],
                        'elotag_db': len(elotag)}
            elotag = []
        if aktualis:
            ki.append(aktualis)
    for w in ki:
        w['alak'] = unicodedata.normalize('NFC', ''.join(x[2] for x in w['reszek']))
        w['step'] = ' + '.join(x[3] for x in w['reszek'])
        w['makkef'] = w['reszek'][-1][3].strip().endswith('-')
        w['tiszta'] = unicodedata.normalize('NFC', m.tisztit(w['alak']).replace(m.METEG, ''))
    return ki


def jegyek(w):
    """Szerkezeti jegyek a pontozott alakból + az átíró döntésnyomai."""
    alak = m.tisztit(w['alak']) + (m.MAKKEF if w['makkef'] else '')
    gepi, nyom = m.niqqud(alak, P)
    ls = m.betuk(alak.replace(m.MAKKEF, ''))
    j = set()
    for i, b in enumerate(ls):
        if m.KAMEC_KATAN in b['j'] or m.HATAF_KAMEC in b['j']:
            j.add('kamec_katan_gyanu')
        if m.KAMEC in b['j']:
            for k in range(i + 1, len(ls)):
                if ls[k]['b'] in (m.VAV, m.JOD, m.HE, m.ALEF) and not (ls[k]['j'] & (m.MAGANHANGZO | {m.SEVA, m.DAGES})):
                    continue
                if m.SEVA in ls[k]['j'] and k != len(ls) - 1:
                    j.add('kamec_katan_gyanu')
                break
        if m.SEVA in b['j'] and 0 < i < len(ls) - 1 and i >= w['elotag_db']:
            j.add('nem_szokezdo_seva')
    if 'kamec_katan' in nyom:
        j.add('kamec_katan_gyanu')
    if 'furtiv' in nyom:
        j.add('furtiv_patah')
    if 'dages_forte' in nyom:
        j.add('dages_forte')
    if 'tetragramma' in nyom or 'ירושל' in ''.join(c for c in unicodedata.normalize('NFD', w['alak']) if m.ALEF <= c <= m.TAV):
        j.add('ketiv_qere')
    if w['makkef']:
        j.add('makkef')
        if any(m.KAMEC in b['j'] for b in ls):
            j.add('kamec_katan_gyanu')
    w['gepi_alt'] = m.niqqud(alak, P_ALT)[0].rstrip('-')
    return gepi.rstrip('-'), nyom, j


def main():
    motivumok = lexikon_motivumok()
    helyek = celhelyek(set(motivumok))
    jeloltek = []
    for w in szavak(helyek):
        mot = helyek[w['igehely']].get(w['strong'])
        w['motivum_szo'] = 'igen' if mot else 'nem'
        w['motivum'] = ', '.join(sorted(mot or set().union(*helyek[w['igehely']].values())))
        w['gepi'], w['nyom'], w['jegyek'] = jegyek(w)
        jeloltek.append(w)
    # egyedi alakok (a pontozás szerint), a vers szerinti első előfordulással
    latott, egyedi = set(), []
    for w in sorted(jeloltek, key=lambda x: (x['motivum_szo'] != 'igen', x['igehely'], x['tiszta'])):
        if w['tiszta'] in latott:
            continue
        latott.add(w['tiszta'])
        egyedi.append(w)
    rnd = random.Random(SEED)
    valasztott, vett = [], set()
    for kat, db in KVOTA:
        jel = [w for w in egyedi if kat in w['jegyek'] and w['tiszta'] not in vett]
        rnd.shuffle(jel)
        jel.sort(key=lambda w: w['motivum_szo'] != 'igen')  # stabil: a motívumszavak előre
        for w in jel[:db]:
            w['kategoria'] = kat
            valasztott.append(w)
            vett.add(w['tiszta'])
    stat = {kat: (sum(kat in w['jegyek'] and w['motivum_szo'] == 'igen' for w in egyedi),
                  sum(kat in w['jegyek'] for w in egyedi)) for kat, _ in KVOTA}
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# HEBER_KIEJTES_nehez_minta.py kimenete (DT-F131y ⛔ feltétele; kísérleti, nem adat).\n')
        f.write(f'# scope=adat/elofordulasok.tsv ({", ".join(motivumok)}; héber Strongok) + konkordancia/TAHOT_kivonat.tsv '
                f'| forras=naplok/HEBER_KIEJTES_nehez_minta.py (seed={SEED}) | ts=2026-10-30\n')
        f.write(f'# jelölt szavak: {len(jeloltek)}, egyedi alak: {len(egyedi)}; kategóriánként (egyedi; motívumszó, összes): {stat}\n')
        f.write('\t'.join(['sorszam', 'kategoria', 'osszes_jegy', 'motivum_szo', 'motivum', 'igehely', 'strong',
                           'alak', 'step', 'gepi', 'gepi_alt']) + '\n')
        for i, w in enumerate(valasztott, 1):
            f.write('\t'.join([str(i), w['kategoria'], ','.join(sorted(w['jegyek'])), w['motivum_szo'], w['motivum'],
                               w['igehely'], w['strong'], w['tiszta'], w['step'], w['gepi'], w['gepi_alt']]) + '\n')
    print(len(jeloltek), len(egyedi), stat, len(valasztott))


if __name__ == '__main__':
    main()
