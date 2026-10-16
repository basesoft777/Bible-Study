"""m2_karoli_ellenoriz.py — F99 M2: a vers → jelentés tábla Károli-oszlopának gépi összevetése a repó Károli-szövegével.

A felhasználó döntése (2026-10-15): a Károli-oszlopot nem a vak ellenőr bírálja, hanem gépi összevetés. A próba: a TAHOT_kivonat.tsv
`Igehely` kulcsa maga a Károli-vers, amelynek a héber szövegét a sor hordozza (F85.6); ha a szócikk Strong-száma a táblában álló
Károli-vers TAHOT-sorai között szerepel, a Károli-kulcs a héber szöveg szerint helyes. Ha nem, a ±3 versnyi környezetben keresi, és
kiírja, hol áll. A Karoli_1908.tsv a vers létezését, a Karoli_versmegfeleltetes.tsv az MT↔Károli besorolást (osztály) adja.

Korlátok (a jelentésben is): a BDB szócikk és a TAHOT Strong-címkézése eltérhet (pl. héber–arámi pár, H5920/H5921, homonimák), ezért
a „nincs TAHOT-találat” nem bizonyítja a hibát; a mért arány a kulcsolás felső hibabecslése.

Kimenet: naplok/BDB_SZELETELO_M2_karoli.md (felülírja). Csak olvas, a táblát nem módosítja.
Használat: python eszkozok/olvaso_szerver/m2_karoli_ellenoriz.py [--kulcs …] [--kitoltott A B] [--ki naplok/…md]
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TABLA = os.path.join(REPO, 'adat', 'bdb_vers_jelentes.tsv')
TAHOT = os.path.join(REPO, 'konkordancia', 'TAHOT_kivonat.tsv')
KAROLI = os.path.join(REPO, 'konkordancia', 'Karoli_1908.tsv')
VERSMEGF = os.path.join(REPO, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')
# a vak minta külön megnevezett sorai (a felhasználó döntése, 5. pont): kulcs-üres Károli, Jób 37, Zsolt 45:3/45:4 és a többi eltérés
KIEMELT = ['M098', 'M045', 'M102', 'M112', 'M029', 'M145', 'M014', 'M027', 'M106', 'M119', 'M230']
VERS = re.compile(r'^(.+?) (\d+):(\d+)$')


def tsv(p):
    for l in open(p, encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        yield l.rstrip('\n').split('\t')


def strong_n(x):
    m = re.match(r'^H0*(\d+)', x or '')
    return int(m.group(1)) if m else None


def olvas_lap(p):
    L = list(tsv(p))
    return {r[0]: dict(zip(L[0], r + [''] * (len(L[0]) - len(r)))) for r in L[1:]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kulcs', default='naplok/BDB_SZELETELO_M2_minta_kulcs.tsv')
    ap.add_argument('--kitoltott', nargs='*', default=['naplok/BDB_SZELETELO_M2_minta_kitoltott_A.tsv',
                                                         'naplok/BDB_SZELETELO_M2_minta_kitoltott_B.tsv'])
    ap.add_argument('--ki', default='naplok/BDB_SZELETELO_M2_karoli.md')
    a = ap.parse_args()

    tahot = defaultdict(set)
    for r in tsv(TAHOT):
        if r[0] == 'Igehely':
            continue
        n = strong_n(r[1])
        if n is not None:
            tahot[r[0]].add(n)
    karoli = {}
    for r in tsv(KAROLI):
        if r[0] != 'Igehely':
            karoli[r[0]] = r[1] if len(r) > 1 else ''
    osztaly = {}
    for r in tsv(VERSMEGF):
        if r[0] != 'igehely_karoli':
            osztaly[r[0]] = r[3] if len(r) > 3 else ''

    def kozel(konyv, c, v, n, sugar=3):
        """A ±sugar versnyi környezetben a Strong TAHOT-helyei; ha ott nincs, a fejezet többi helye „(fejezet)” jelöléssel."""
        ki = ['%s %d:%d' % (konyv, c, vv) for vv in range(max(1, v - sugar), v + sugar + 1)
              if n in tahot.get('%s %d:%d' % (konyv, c, vv), ())]
        if not ki:
            ki = ['%s %d:%d (fejezet)' % (konyv, c, vv) for vv in range(1, 200) if n in tahot.get('%s %d:%d' % (konyv, c, vv), ())][:4]
        return ki

    def proba(vers, n):
        m = VERS.match(vers or '')
        if not m:
            return 'nincs vers', []
        if vers not in karoli:
            return 'a Károliban nincs ilyen vers', []
        if n in tahot.get(vers, ()):
            return 'igen', [vers]
        return 'nem', kozel(m.group(1), int(m.group(2)), int(m.group(3)), n)

    # 1. a teljes tábla
    h = None
    stat = Counter()
    nk = Counter()
    fejezet = defaultdict(Counter)
    for r in tsv(TABLA):
        if h is None:
            h = {k: i for i, k in enumerate(r)}
            continue
        if r[h['okkod']] == 'nincs_karoli' and r[h['szurt']] != '1':
            # a Károli-megfelelő nélküli sor: létezik-e azonos számú Károli-vers, és a TAHOT ott hordozza-e a szót
            mt = r[h['mt_vers']]
            n = strong_n(r[h['strong']])
            if mt not in karoli:
                nk['nincs azonos számú Károli-vers'] += 1
            elif n in tahot.get(mt, ()):
                nk['azonos számú Károli-versen a TAHOT-ban'] += 1
            elif any('(fejezet)' not in x for x in kozel(VERS.match(mt).group(1), int(VERS.match(mt).group(2)),
                                                          int(VERS.match(mt).group(3)), n)):
                nk['a ±3 versnyi környezetben a TAHOT-ban'] += 1
            else:
                nk['a környezetben sincs'] += 1
        if r[h['szurt']] == '1' or not r[h['karoli_vers']]:
            continue
        n = strong_n(r[h['strong']])
        ok = n in tahot.get(r[h['karoli_vers']], ())
        stat[(r[h['vers_feloldas']], ok)] += 1
        if not ok:
            m = VERS.match(r[h['karoli_vers']])
            b, c, v = m.group(1), int(m.group(2)), int(m.group(3))
            d = next((dd for dd in (-1, 1, -2, 2, -3, 3) if n in tahot.get('%s %d:%d' % (b, c, v + dd), ())), None)
            fejezet[(r[h['vers_feloldas']], '%s %d' % (b, c))][d] += 1

    # 2. a vak minta sorai
    kulcs = olvas_lap(os.path.join(REPO, a.kulcs))
    lapok = [olvas_lap(os.path.join(REPO, p)) for p in a.kitoltott]
    mai = {}
    for r in tsv(TABLA):
        if r[0] == 'strong':
            continue
        mai[(r[h['strong']], r[h['poz']])] = r

    def ell_vers(lap_sor, mt):
        x = (lap_sor or {}).get('karoli_vers', '').strip()
        if not x or x == '?':
            return x or ''
        if x == '=':
            return mt
        m = VERS.match(mt or '')
        if re.match(r'^\d+:\d+$', x) and m:
            return '%s %s' % (m.group(1), x)
        return x

    sorok = []
    veletlen = [k for k, v in kulcs.items() if v['reteg'] == 'veletlen']
    egyezik = elter = 0
    for az in veletlen:
        k = kulcs[az]
        t = mai.get((k['strong'], k['poz']))
        kv = t[h['karoli_vers']] if t else k['karoli_vers']
        mt = t[h['mt_vers']] if t else k['mt_vers']
        e = [ell_vers(l.get(az), mt) for l in lapok]
        if all(x == kv for x in e if x):
            egyezik += 1
        else:
            elter += 1
        if az in KIEMELT or any(x and x != kv for x in e):
            n = strong_n(k['strong'])
            tp = proba(kv, n)
            ep = [(x, proba(x, n)) for x in sorted(set(x for x in e if x and x != kv))]
            mtp = proba(mt, n) if mt != kv else None
            sorok.append((az, k['strong'], k['nyers'], mt, kv, t[h['vers_feloldas']] if t else k['vers_feloldas'],
                          t[h['okkod']] if t else '', e, tp, ep, mtp, osztaly.get(kv, '')))

    ki = []
    ki.append('# F99 M2 — a Károli-oszlop gépi összevetése (vak minta, seed 99)')
    ki.append('')
    ki.append('*Generálta: `eszkozok/olvaso_szerver/m2_karoli_ellenoriz.py` (csak olvas). A felhasználó döntése (2026-10-15, 5. pont): a '
              'Károli-oszlopot nem a vak ellenőr bírálja, hanem gépi összevetés a repó Károli-adatával. Proveniencia: '
              '`scope=adat/bdb_vers_jelentes.tsv + vak minta seed 99 | forras=TAHOT_kivonat.tsv (Igehely = Károli-vers, F85.6), '
              'Karoli_1908.tsv, Karoli_versmegfeleltetes.tsv | ts=2026-10-15`.*')
    ki.append('')
    ki.append('## 1. A próba')
    ki.append('')
    ki.append('A TAHOT `Igehely` kulcsa a Károli-vers, amelynek a héber szövegét a sor hordozza. Ha a szócikk Strong-száma a táblában álló '
              'Károli-vers TAHOT-sorai között van, a Károli-kulcs a héber szöveg szerint helyes („igen”). Ha nincs, a ±3 versnyi környezet '
              'TAHOT-találatai jelzik, hová kerülne. **Korlát:** a BDB szócikk és a TAHOT Strong-címkéje eltérhet (héber–arámi pár, '
              'homonima, H5920/H5921), ezért a „nem” nem bizonyított hiba, hanem vizsgálandó jel.')
    ki.append('')
    ki.append('## 2. A teljes tábla (szűretlen, Károli-verses sorok)')
    ki.append('')
    ki.append('| feloldás | TAHOT-ban a Strong a Károli-versen | nincs | arány |')
    ki.append('|---|---:|---:|---:|')
    for fm in sorted({x for x, _ in stat}):
        i, n = stat[(fm, True)], stat[(fm, False)]
        ki.append('| %s | %d | %d | %.2f%% |' % (fm, i, n, 100.0 * i / max(1, i + n)))
    i, n = sum(v for (f, o), v in stat.items() if o), sum(v for (f, o), v in stat.items() if not o)
    ki.append('| **összesen** | %d | %d | %.2f%% |' % (i, n, 100.0 * i / max(1, i + n)))
    ki.append('')
    ki.append('Fejezetenként rendszeres eltolás (a TAHOT-találat nélküli sorok közül legalább 20, amelyeknél a szomszédos vers hordozza '
              'a szót, egyirányú eltolással; ez a kulcsolás rendszerhibájának jele, nem a Strong-címkézésé):')
    ki.append('')
    ki.append('| feloldás | fejezet | eltolás (Károli-vers + d) | sor | a fejezet találat nélküli sorai |')
    ki.append('|---|---|---:|---:|---:|')
    for (fm, fj), cnt in sorted(fejezet.items(), key=lambda t: -max(v for k, v in t[1].items() if k is not None) if any(
            k is not None for k in t[1]) else 0):
        d, v = max(((k, v) for k, v in cnt.items() if k is not None), key=lambda t: t[1], default=(None, 0))
        if v >= 20:
            ki.append('| %s | %s | %+d | %d | %d |' % (fm, fj, d, v, sum(cnt.values())))
    ki.append('')
    ki.append('A `nincs_karoli` okkódú (Károli-megfelelő nélküli, DT-F99a (3) a) szűretlen sorok, a TAHOT szerint:')
    ki.append('')
    ki.append('| eset | sor |')
    ki.append('|---|---:|')
    for x, v in sorted(nk.items(), key=lambda t: -t[1]):
        ki.append('| %s | %d |' % (x, v))
    ki.append('')
    ki.append('## 3. A vak minta (200 véletlen sor)')
    ki.append('')
    ki.append('A mai tábla Károli-verse és a két kitöltés Károli-értéke („=” = az MT-vers) %d sorban egyezik, %d sorban tér el (a kulcs-üres '
              'sorokat is beleértve).' % (egyezik, elter))
    ki.append('')
    ki.append('| azon | Strong | nyers | MT-vers | tábla Károli | feloldás | okkód | ellenőrök | TAHOT a táblai versen | TAHOT az ellenőri versen | '
              'TAHOT az MT-számon | versmegf. osztály |')
    ki.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for (az, st, ny, mt, kv, fm, ok, e, tp, ep, mtp, oszt) in sorok:
        def f(p):
            return '%s%s' % (p[0], (' → ' + ', '.join(p[1])) if p[0] == 'nem' and p[1] else '')
        ki.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            az, st, ny, mt, kv or '—', fm, ok or '', ' / '.join(x or '—' for x in e), f(tp),
            '; '.join('%s: %s' % (x, f(p)) for x, p in ep) or '—', f(mtp) if mtp else '(= tábla)', oszt or '—'))
    ki.append('')
    with open(os.path.join(REPO, a.ki), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(ki))
    print('kiírva:', a.ki, '| sorok:', len(sorok), '| minta egyezik/eltér:', egyezik, elter)
    for x in sorted({x for x, _ in stat}):
        print(x, stat[(x, True)], stat[(x, False)])


if __name__ == '__main__':
    main()
