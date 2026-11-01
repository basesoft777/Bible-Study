"""F131 M0: a brief 2. szakaszának újramérése (a #127, #110, #132 utáni main-en).

Csak olvas. Minden TSV `split('\\t')`-tel, a `csv` modul nélkül (CLAUDE.md).
A kimenet a stdout; a napló (naplok/F131_SZOTARI_GERINC_naplo.md 1. szakasz)
ebből készül.

    python naplok/F131_M0_meres.py
"""
import collections
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTIVUM = 'ISTENTISZT-001'
LAP = os.path.join(GYOKER, 'lexikon', MOTIVUM + '_TUDOMANYOS.md')
JEL = '(fordításra vár)'


def tabla(rel):
    """Fejléc + sorok (dict-ek); a '#' kezdetű sorok kimaradnak."""
    fejlec = None
    sorok = []
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        for nyers in f:
            sor = nyers.rstrip('\n').rstrip('\r')
            if not sor or sor.startswith('#'):
                continue
            mezok = sor.split('\t')
            if fejlec is None:
                fejlec = mezok
                continue
            mezok += [''] * (len(fejlec) - len(mezok))
            sorok.append(dict(zip(fejlec, mezok)))
    return sorok


def cim(s):
    print()
    print('=' * 70)
    print(s)
    print('=' * 70)


def vag(utvonal):
    """A záró '/-' levágása (2.29 ↔ 2.30 összevetéshez)."""
    while utvonal.endswith('/-'):
        utvonal = utvonal[:-2]
    return utvonal


def kutatoi_ut(jsz):
    """'2.c (tagadva)' → ('2.c', 'tagadva'); a minősítő levágva."""
    m = re.match(r'^\s*([^\s(]+)\s*(?:\((.*)\))?\s*$', jsz)
    if not m:
        return jsz, ''
    return m.group(1), (m.group(2) or '')


def ala_esik(bdb_ut, kut_kulcs):
    """Igaz, ha a BDB-útvonal (pl. 'Qal/3/b') a kutatói kulcs (pl. '3') alá esik.
    A kutatói kulcs törzs nélküli: '2.c' → szám 2, betű c; '3' → szám 3."""
    reszek = vag(bdb_ut).split('/')
    if len(reszek) < 2:
        return False
    szam = reszek[1] if len(reszek) > 1 else '-'
    betu = reszek[2] if len(reszek) > 2 else '-'
    k = kut_kulcs.split('.')
    if k[0] != szam:
        return False
    if len(k) > 1 and k[1] != betu:
        return False
    return True


def main():
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print('proveniencia: scope=%s (adat/elofordulasok.tsv); H7121, H8034, G1941 | '
          'forras=naplok/F131_M0_meres.py | ts=%s' % (MOTIVUM, ts))

    # ---------------------------------------------------------------- 1
    cim('1. Az előfordulások szótári hivatkozása (adat/elofordulasok.tsv)')
    elo = [s for s in tabla('adat/elofordulasok.tsv') if s['id'] == MOTIVUM]
    print('sorok:', len(elo))
    szotar = collections.Counter((s['lexikon_szotar'], s['lexikon_entry_id']) for s in elo)
    for k, v in sorted(szotar.items()):
        print('  %s %s: %d' % (k[0], k[1], v))
    jsz = collections.Counter((s['lexikon_entry_id'], s['jelentes_szam']) for s in elo)
    for k, v in sorted(jsz.items()):
        print('  jelentes_szam %s %r: %d' % (k[0], k[1], v))
    print('  H8034-re mutató sor (lexikon_entry_id):',
          sum(1 for s in elo if s['lexikon_entry_id'] == 'H8034'))
    print('  strong-mező értékek:', dict(collections.Counter(s['strong'] for s in elo)))
    print('  minősítős jelentes_szam:')
    for s in elo:
        if '(' in s['jelentes_szam']:
            print('    %s: %r' % (s['igehely'], s['jelentes_szam']))
    jhu = collections.Counter(s['jelentes_hu'] for s in elo if s['lexikon_szotar'] == 'BDB')
    print('  jelentes_hu (ÓSZ/BDB) értékek:')
    for k, v in jhu.most_common():
        print('    %r: %d' % (k, v))
    jhu_g = collections.Counter(s['jelentes_hu'] for s in elo if s['lexikon_szotar'] != 'BDB')
    print('  jelentes_hu (ÚSZ) értékek:', dict(jhu_g))
    osz = [s for s in elo if s['lexikon_szotar'] == 'BDB']
    usz = [s for s in elo if s['lexikon_szotar'] != 'BDB']
    osz_versek = {s['igehely'] for s in osz}
    usz_versek = {s['igehely'] for s in usz}

    # ---------------------------------------------------------------- 2
    cim('2. A BDB-tagolás három helyen (lexikon_hivatkozasok / 2.30 / 2.29)')
    lh = tabla('adat/lexikon_hivatkozasok.tsv')
    lh_bdb = [s for s in lh if s['szotar'] == 'BDB']
    print('lexikon_hivatkozasok BDB-sorok:', len(lh_bdb))
    for s in lh_bdb:
        print('  %s %r (forrasfajl=%s)' % (s['strong'], s['jelentes_szam'], s['forrasfajl']))
    lh_g = [s for s in lh if s['strong'] in ('G1941',)]
    print('lexikon_hivatkozasok G1941-sorok:')
    for s in lh_g:
        print('  %s %s %r' % (s['szotar'], s['strong'], s['jelentes_szam']))
    bsz = tabla('adat/bdb_szakaszok.tsv')
    for strong in ('H7121', 'H8034'):
        ut = [s['utvonal'] for s in bsz if s['strong'] == strong]
        print('bdb_szakaszok %s: %d sor; Niph\'al/2/c jelen: %s; Qal/2/c jelen: %s' % (
            strong, len(ut), "Niph'al/2/c" in ut, 'Qal/2/c' in ut))

    # ---------------------------------------------------------------- 3
    cim('3. A magyar BDB szakaszolása (adat/bdb_szakasz_hu.tsv)')
    bhu = tabla('adat/bdb_szakasz_hu.tsv')
    for strong in ('H7121', 'H8034'):
        sorok = [s for s in bhu if s['strong'] == strong]
        print('%s: %d sor; kategoria: %s' % (
            strong, len(sorok), dict(collections.Counter(s['kategoria'] for s in sorok))))
        for s in sorok:
            if s['kategoria'] in ('horgonnyal', 'elakad'):
                print('   %s %s horgony=%s' % (s['kategoria'], s['utvonal'], s['horgony']))
    for strong, ut in (('H7121', 'Qal/3/-'), ('H7121', 'Qal/2/c'), ('H7121', 'Qal/3/b'),
                       ('H8034', '-/3/-'), ('H8034', '-/4/-'), ('H7121', 'fej'), ('H8034', 'fej')):
        for s in bhu:
            if s['strong'] == strong and s['utvonal'] == ut and s['szoveg_hu']:
                print('  %s %s eleje: %s' % (strong, ut, s['szoveg_hu'][:110].replace('\n', ' ')))
                break
        else:
            print('  %s %s: nincs magyar szöveg' % (strong, ut))
    # a #144 tárgya: `illeszkedik` sor, amelynek magyar szövege csak a jelölő
    for strong in ('H7121', 'H8034'):
        csak = [s['utvonal'] for s in bhu if s['strong'] == strong
                and s['kategoria'] == 'illeszkedik'
                and re.sub(r'[\s.:]', '', s['szoveg_hu']) == re.sub(r'[\s.:]', '', s['jel'])]
        print('%s: csak a jelölőt hordozó illeszkedik-sor (a #144 tárgya): %d %s' % (
            strong, len(csak), csak))
    print('elakad-sorok a teljes táblában:',
          sum(1 for s in bhu if s['kategoria'] == 'elakad'),
          '; Strongok:', sorted({s['strong'] for s in bhu if s['kategoria'] == 'elakad'})[:10])

    # ---------------------------------------------------------------- 4
    cim('4. A BDB saját példahelyei a motívumhelyek között (bdb_vers_jelentes, szurt≠1)')
    bvj = tabla('adat/bdb_vers_jelentes.tsv')
    kut = {s['igehely']: kutatoi_ut(s['jelentes_szam'])[0] for s in osz}
    for strong in ('H7121', 'H8034'):
        talalt = [s for s in bvj if s['strong'] == strong and s['szurt'] != '1'
                  and s['karoli_vers'] in osz_versek]
        versek = {s['karoli_vers'] for s in talalt}
        print('%s: %d hivatkozás %d versre' % (strong, len(talalt), len(versek)))
        for s in talalt:
            megj = ''
            if strong == 'H7121':
                kk = kut.get(s['karoli_vers'], '')
                megj = '  kutatói=%s  ala_esik=%s' % (kk, ala_esik(s['utvonal'], kk))
            print('   sorszam=%s %s %s%s' % (s['sorszam'], s['karoli_vers'], s['utvonal'], megj))
    ellent = 0
    for s in bvj:
        if s['strong'] == 'H7121' and s['szurt'] != '1' and s['karoli_vers'] in osz_versek:
            if not ala_esik(s['utvonal'], kut.get(s['karoli_vers'], '')):
                ellent += 1
    print('H7121 ellentmondás (BDB-példa nem esik a kutatói út alá):', ellent)

    # ---------------------------------------------------------------- 5
    cim('5. A Thayer G1941 (forditasok.tsv, thayer_szakaszok, thayer_vers_jelentes)')
    ford = tabla('adat/forditasok.tsv')
    for s in ford:
        if s['strong'] == 'G1941':
            print('  forditasok: %s %s %s %s hossz=%d allapot=%s modell=%s' % (
                s['szotar'], s['entry_id'], s['jelentes_szam'], s['mezo'],
                len(s['forditas_hu']), s['allapot'], s['modell']))
    th_sz = [s for s in ford if s['szotar'] == 'Thayer' and s['jelentes_szam'].startswith('sz')]
    print('forditasok Thayer sz<n> sorok (összes Strong):', len(th_sz))
    tsz = [s for s in tabla('adat/thayer_szakaszok.tsv') if s['strong'] == 'G1941']
    print('thayer_szakaszok G1941: %d szakasz: %s' % (
        len(tsz), ', '.join('%s:%s' % (s['sorszam'], s['utvonal']) for s in tsz)))
    tvj = [s for s in tabla('adat/thayer_vers_jelentes.tsv') if s['strong'] == 'G1941']
    print('thayer_vers_jelentes G1941: %d sor' % len(tvj))
    tal = [s for s in tvj if s['karoli_vers'] in usz_versek]
    print('  ebből motívumhelyen: %d sor, %d vers' % (len(tal), len({s['karoli_vers'] for s in tal})))
    for s in tal:
        print('   sorszam=%s %s %s' % (s['sorszam'], s['karoli_vers'], s['utvonal']))
    print('  motívumhely Thayer-hivatkozás nélkül:',
          sorted(usz_versek - {s['karoli_vers'] for s in tal}))
    teljes = [s for s in ford if s['szotar'] == 'Thayer' and s['strong'] == 'G1941'
              and s['jelentes_szam'] == 'teljes']
    if teljes:
        t = teljes[0]['forditas_hu']
        hamis = re.findall(r'(?<!\w)(\d)\. (\w+)', t)
        print('  a teljes magyar Thayer egyszerű számmintája (n. szó):',
              ', '.join('%s. %s' % h for h in hamis))
    ubs = [s for s in ford if s['szotar'] == 'UBS_DNTG' and s['strong'] == 'G1941']
    print('UBS_DNTG G1941 sorok:', len(ubs), '; Louw–Nida:',
          sorted({s['jelentes_szam'] for s in ubs}))

    # ---------------------------------------------------------------- 6
    cim('6. A mai lap (lexikon/ISTENTISZT-001_TUDOMANYOS.md): (fordításra vár) egységenként')
    with open(LAP, encoding='utf-8') as f:
        sorok = f.read().split('\n')
    print('jelölés-előfordulás összesen:', sum(s.count(JEL) for s in sorok),
          '; jelölést tartalmazó sor:', sum(1 for s in sorok if JEL in s))
    h2 = h3 = h4 = h5 = summ = ''
    egysegek = collections.OrderedDict()
    for s in sorok:
        if s.startswith('## '):
            h2, h3, h4, h5, summ = s[3:], '', '', '', ''
        elif s.startswith('### '):
            h3, h4, h5, summ = s[4:], '', '', ''
        elif s.startswith('#### '):
            h4, h5, summ = s[5:], '', ''
        elif s.startswith('##### '):
            h5, summ = s[6:], ''
        elif s.startswith('<summary>'):
            summ = re.sub(r'<.*?>', '', s).split(' — ')[0]
        if JEL not in s:
            continue
        if s.startswith('|'):
            m = re.match(r'\|\s*`?([^`|]+?)`?\s*\|', s)
            kulcs = 'sor ' + (m.group(1) if m else '?')
        elif summ:
            kulcs = 'tW ' + summ
        elif h5:
            kulcs = h5
        elif s.startswith('*Mounce'):
            kulcs = 'Mounce'
        else:
            kulcs = '(blokkszint)'
        k = (h3, h4, kulcs)
        egysegek[k] = egysegek.get(k, 0) + s.count(JEL)
    print('egység (nyelv | szerep | kulcs): jelölésszám')
    for (h3, h4, kulcs), n in egysegek.items():
        print('  %s | %s | %s: %d' % (h3, h4, kulcs, n))
    print('egységek száma:', len(egysegek))


if __name__ == '__main__':
    main()
