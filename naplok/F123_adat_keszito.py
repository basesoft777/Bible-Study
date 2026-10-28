#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F123_adat_keszito.py — a #123 X.A adat-előkészítésének munkaszkriptje (motívumfüggetlen, ID-paraméterrel).

Csak olvas a repó tábláiból, és csak `naplok/F123_*` munkafájlt ír (a lekérdezések proveniencia-sorai a
`lekerdez.py --naplo F123` útján a `naplok/F123_lekerdezesek.tsv`-be kerülnek). Adattáblát nem ír.

Alparancsok:
  f108    <ID>  — a törzs (elofordulasok + jeloltek) összevetése a #108 eltérés-táblájával és a mai scannel
  szotar  <ID>  — szótári sorok a motívum Strongjaihoz, szerepenként (adat/szotar_szerepek.tsv), és a
                  hiányzó fordítások listája (a generátor forditasok.tsv-kulcsai szerint)
  proza   <ID>  — próza-lefedettség: az előfordulások megnevezése a kézi forrásban és a lexikonoldal réseiben
  seol    —       az ALVIL-001 2e. 4. scanje: halál/sír + kiáltás az Úrhoz, H7585 nélkül

TSV-olvasás split('\\t') (lekerdez.read_tsv); a csv modul tilos (CLAUDE.md).
Futtatás: python naplok/F123_adat_keszito.py <alparancs> [ID]
"""

import hashlib
import re
import subprocess
import sys
from collections import defaultdict, Counter
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'eszkozok'))
import lekerdez as L  # noqa: E402

NAPLOK = ROOT / 'naplok'
TS = L.ts()


def ir_tsv(nev, fejlec, sorok, megj):
    p = NAPLOK / nev
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/F123_adat_keszito.py | %s | %s\n' % (megj, TS))
        f.write('\t'.join(fejlec) + '\n')
        for s in sorok:
            s = [str(x).replace('\t', ' ').replace('\r', ' ').replace('\n', ' \\n ') for x in s]
            f.write('\t'.join(s) + '\n')
    return p


def motivum_sorok(mid):
    E = [r for r in L.read_tsv_skip_comments(ROOT / 'adat' / 'elofordulasok.tsv') if r['id'] == mid]
    J = [r for r in L.read_tsv_skip_comments(ROOT / 'adat' / 'jeloltek.tsv') if r['id'] == mid]
    return E, J


def motivum_strongok(E):
    s = set()
    for r in E:
        for t in (r['strong'] or '').split('+'):
            if t.strip():
                s.add(t.strip())
    return sorted(s)


def lekerdez_futtat(argv):
    """lekerdez.py futtatása --naplo F123 --lepes B4 naplózással; (kimenet-sorok, proveniencia)."""
    cmd = [sys.executable, str(ROOT / 'eszkozok' / 'lekerdez.py'), '--naplo', 'F123', '--lepes', 'B4'] + argv
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', cwd=str(ROOT))
    if p.returncode != 0:
        sys.exit('lekerdez hiba: %s\n%s' % (' '.join(argv), p.stderr))
    sorok = [s for s in p.stdout.splitlines() if s.strip()]
    prov = [s for s in sorok if s.startswith('proveniencia:')]
    return sorok, (prov[-1][len('proveniencia:'):].strip() if prov else 'manual')


def versre(igehely):
    if '-' not in igehely:
        return [igehely]
    rng = L.parse_range(igehely)
    if rng[0] == 'verse':
        return [igehely]
    ki = []
    for k in L.load_karoli_1908():
        try:
            p = L.parse_igehely(k)
        except ValueError:
            continue
        if L.in_range(rng, *p):
            ki.append((p[1], p[2], k))
    return [x[2] for x in sorted(ki)] or [igehely]


# ---------------------------------------------------------------------------
def cmd_f108(mid):
    E, J = motivum_sorok(mid)
    f108 = [r for r in L.read_tsv_skip_comments(NAPLOK / 'F108_ujrascan_elteresek.tsv') if r['id'] == mid]
    f108_E = {(r['igehely'], r['strong']): r for r in f108 if r['tabla'] == 'elofordulasok'}
    f108_J = {}
    for r in f108:
        if r['tabla'].startswith('jeloltek:'):
            f108_J.setdefault(r['igehely'], []).append(r)
    f108_U = [r for r in f108 if r['tabla'] == 'ujrascan']

    sorok = []
    valt = Counter()
    # E-sorok
    ma_E = {(r['igehely'], r['strong']) for r in E}
    for r in E:
        k = (r['igehely'], r['strong'])
        f = f108_E.get(k)
        if f is None:
            v = 'uj_E_sor_a_108_ota'
        else:
            v = 'nincs'
        valt[('E', v)] += 1
        sorok.append(['elofordulasok', r['igehely'], r['strong'], r['gerinc_elem'],
                      f['osztaly'] if f else '—', f['megjegyzes'] if f else '—', v])
    for k, f in f108_E.items():
        if k not in ma_E:
            valt[('E', 'eltunt_E_sor_a_108_ota')] += 1
            sorok.append(['elofordulasok', k[0], k[1], '—', f['osztaly'], f['megjegyzes'], 'eltunt_E_sor_a_108_ota'])
    # J-sorok
    ma_J = Counter(r['igehely'] for r in J)
    for r in J:
        fl = f108_J.get(r['igehely'], [])
        d108 = sorted({x['tabla'].split(':', 1)[1] for x in fl})
        if not fl:
            v = 'uj_J_sor_a_108_ota'
        elif r['dontes'] not in d108:
            v = 'dontes_valtozott (F108: %s)' % ', '.join(d108)
        else:
            v = 'nincs'
        valt[('J', v.split(' ')[0])] += 1
        sorok.append(['jeloltek:' + r['dontes'], r['igehely'], '—', '—',
                      ', '.join(sorted({x['osztaly'] for x in fl})) or '—',
                      ' | '.join(sorted({x['megjegyzes'] for x in fl if x['megjegyzes']})) or '—', v])
    for ig, fl in f108_J.items():
        if ig not in ma_J:
            valt[('J', 'eltunt_J_sor_a_108_ota')] += 1
            sorok.append([fl[0]['tabla'], ig, '—', '—', fl[0]['osztaly'], fl[0]['megjegyzes'], 'eltunt_J_sor_a_108_ota'])

    # mai scan a motívum Strongjaira
    E_versek = set()
    for r in E:
        E_versek.update(versre(r['igehely']))
    J_versek = set()
    for r in J:
        try:
            J_versek.update(versre(r['igehely']))
        except ValueError:
            J_versek.add(r['igehely'])
    scan_prov = []
    scan_db = {}
    for s in motivum_strongok(E):
        ki, prov = lekerdez_futtat(['scan', s])
        scan_prov.append(prov)
        hits = [x for x in ki if not x.startswith('#') and not x.startswith('proveniencia:')]
        uj = [h for h in hits if h not in E_versek and h not in J_versek]
        csakJ = [h for h in hits if h not in E_versek and h in J_versek]
        nincs_scanben = sorted(v for v in E_versek if any(r['strong'] == s and v in versre(r['igehely'])
                                                          for r in E) and v not in hits)
        scan_db[s] = (len(hits), len(hits) - len(uj) - len(csakJ), len(csakJ), len(uj), nincs_scanben)
        for h in uj:
            sorok.append(['ujrascan', h, s, '—', '—', '—', 'UJ_HELY (nincs E-ben/J-ben)'])
            valt[('scan', 'uj_hely')] += 1
        for h in csakJ:
            sorok.append(['ujrascan', h, s, '—', '—', 'csak J-ben', 'nincs (már jelölt)'])
        for v in nincs_scanben:
            sorok.append(['ujrascan', v, s, s, '—', 'E-sor, de a mai scan nem adja', 'KULCS_ELTERES'])
            valt[('scan', 'kulcs_elteres')] += 1
        f108_ref = [r for r in f108_U if r['strong'] == s]
        scan_db[s] = scan_db[s] + (len(f108_ref),)

    fej = ['tabla', 'igehely', 'strong', 'gerinc_elem', 'f108_osztaly', 'f108_megjegyzes', 'valtozas', 'proveniencia']
    prov = ('scope=%s: adat/elofordulasok.tsv (%d sor) + adat/jeloltek.tsv (%d sor) × naplok/F108_ujrascan_elteresek.tsv '
            '(%d sor) | forras=split(\'\\t\'), ág claude/f123-alvil-adat | ts=%s' % (mid, len(E), len(J), len(f108), TS))
    ir_tsv('F123_adat_%s_f108_osszevetes.tsv' % mid, fej, [s + [prov] for s in sorok], 'F123 X.A #108-összevetés %s' % mid)
    print('PROV\t' + prov)
    for p in scan_prov:
        print('PROV\t' + p)
    for k, v in sorted(valt.items()):
        print('VALT\t%s\t%s\t%d' % (k[0], k[1], v))
    for s, d in scan_db.items():
        print('SCAN\t%s\ttalalat=%d\tE-ben=%d\tcsak_J=%d\tuj=%d\tE-sor_scan_nelkul=%s\tF108_ujrascan_sor=%d'
              % (s, d[0], d[1], d[2], d[3], ','.join(d[4]) or '—', d[5]))
    osztaly = Counter((r['tabla'].split(':')[0], r['osztaly']) for r in f108)
    for k, v in sorted(osztaly.items()):
        print('F108\t%s\t%s\t%d' % (k[0], k[1], v))


# ---------------------------------------------------------------------------
def tbes_blokkok(fajl, strong):
    """TBESH/TBESG.txt: a Strongra (és alszócikkeire) illeszkedő sorok (a fájl tabos sorai)."""
    ki = []
    pat = re.compile(r'^%s[A-Za-z]?\t' % re.escape(strong))
    pat2 = re.compile(r'\t%s[A-Za-z]?\t' % re.escape(strong))
    with open(ROOT / 'konkordancia' / fajl, encoding='utf-8', errors='replace') as f:
        for i, l in enumerate(f, 1):
            if pat.search(l) or pat2.search(l):
                ki.append((i, l.rstrip('\n')))
    return ki


def sorok_strongra(path, oszlop, strong, kiegeszito=None, skip=True):
    rows = L.read_tsv_skip_comments(path) if skip else L.read_tsv(path)
    return [r for r in rows if r.get(oszlop, '') == strong or (kiegeszito and r.get(oszlop, '') in kiegeszito)]


def h(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:10]


def cmd_szotar(mid):
    E, _ = motivum_sorok(mid)
    strongok = motivum_strongok(E)
    K = ROOT / 'konkordancia'
    A = ROOT / 'adat'
    ford = {(r['szotar'], r['strong'], r['entry_id'], r['jelentes_szam'], r['mezo']): r
            for r in L.read_tsv_skip_comments(A / 'forditasok.tsv')}
    szerepek = L.read_tsv_skip_comments(A / 'szotar_szerepek.tsv')
    sorok = []     # szotari sorok
    hiany = []     # hiányzó fordítások
    lefed = []     # szerep-kínálat
    latott = set()

    def fkulcs(szotar, strong, entry, jsz, mezo):
        r = ford.get((szotar, strong, entry, jsz, mezo))
        return (r['allapot'] if r else None)

    def add(szerep_n, nyelv, forras, strong, kulcs, tartalom, prov, ford_kulcs=None, ford_allapot=None):
        sorok.append([nyelv, szerep_n, forras, strong, kulcs, len(tartalom), h(tartalom),
                      tartalom[:160].replace('\t', ' '),
                      '|'.join(ford_kulcs) if ford_kulcs else '—',
                      ford_allapot or ('HIÁNYZIK' if ford_kulcs else '—'), prov])
        if ford_kulcs and not ford_allapot and tuple(ford_kulcs) not in latott:
            latott.add(tuple(ford_kulcs))
            hiany.append([nyelv, szerep_n, forras, strong] + list(ford_kulcs) + [prov])

    for s in strongok:
        ny = 'heber' if s.startswith('H') else 'gorog'
        num = str(int(s[1:]))
        if ny == 'heber':
            # 1 TBESH
            for i, l in tbes_blokkok('TBESH.txt', s):
                add(1, ny, 'TBESH.txt', s, 'sor %d' % i, l,
                    'scope=TBESH.txt %s | forras=konkordancia/TBESH.txt (sorillesztés) | ts=%s' % (s, TS),
                    ('TBESH', s, s, 'teljes', 'forditas_hu'), fkulcs('TBESH', s, s, 'teljes', 'forditas_hu'))
            # 2 BDB szakaszok + teljes
            szak = sorok_strongra(A / 'bdb_szakaszok.tsv', 'strong', s)
            teljes = fkulcs('BDB', s, s, 'teljes', 'forditas_hu')
            for r in szak:
                st = fkulcs('BDB', s, s, 'sz' + r['sorszam'], 'forditas_hu')
                add(2, ny, 'adat/bdb_szakaszok.tsv', s, 'sz%s %s' % (r['sorszam'], r['utvonal']), r['szoveg'],
                    r['proveniencia'] or 'scope=adat/bdb_szakaszok.tsv | forras=split | ts=%s' % TS,
                    ('BDB', s, s, 'sz' + r['sorszam'], 'forditas_hu'),
                    st or (('nincs sz-sor; a kezi `teljes` érvényes (DT290 (3))') if teljes == 'kezi' else None))
            for r in sorok_strongra(K / 'BDB_teljes_unabridged.tsv', 'Strong_padded', s, skip=False):
                add(2, ny, 'konkordancia/BDB_teljes_unabridged.tsv', s, 'teljes', r['Teljes_szocikk'],
                    'scope=BDB_teljes_unabridged %s | forras=konkordancia/BDB_teljes_unabridged.tsv | ts=%s' % (s, TS),
                    ('BDB', s, s, 'teljes', 'forditas_hu'), teljes)
            # 3 tW
            for r in L.read_tsv_skip_comments(K / 'tW_szocikkek.tsv'):
                if s in r['strong'].split('+'):
                    first = r['strong'].split('+')[0]
                    add(3, ny, 'konkordancia/tW_szocikkek.tsv', s, r['tw_id'], r['szoveg'],
                        'scope=tW_szocikkek %s | forras=konkordancia/tW_szocikkek.tsv (commit %s) | ts=%s' % (s, r['forras_commit'][:10], TS),
                        ('tW_szocikkek', first, r['tw_id'], '—', 'forditas_hu'),
                        fkulcs('tW_szocikkek', first, r['tw_id'], '—', 'forditas_hu'))
            # 4-5 UBS DBH / SDBH
            for r in sorok_strongra(K / 'UBS_DBH_jelentesek.tsv', 'strong', s):
                for mezo, src in (('glosszak_hu', 'glosszak'), ('definicio_hu', 'definicio_rovid')):
                    add(5 if mezo == 'glosszak_hu' else 4, ny, 'konkordancia/UBS_DBH_jelentesek.tsv', s,
                        '%s %s' % (r['lexid'], r['entry_kod']), r[src],
                        'scope=UBS_DBH_jelentesek %s | forras=konkordancia/UBS_DBH_jelentesek.tsv | ts=%s' % (s, TS),
                        ('UBS_DBH', s, r['lexid'], '—', mezo), fkulcs('UBS_DBH', s, r['lexid'], '—', mezo))
            for r in sorok_strongra(K / 'SDBH_domenek.tsv', 'strong', s):
                add(4, ny, 'konkordancia/SDBH_domenek.tsv', s, r['domen_kod'], '%s — %s' % (r['domen'], r['glossza']),
                    'scope=SDBH_domenek %s | forras=konkordancia/SDBH_domenek.tsv | ts=%s' % (s, TS))
            refs = sorok_strongra(K / 'UBS_DBH_referenciak.tsv', 'strong', s)
            add(9, ny, 'konkordancia/UBS_DBH_referenciak.tsv', s, '%d referencia' % len(refs),
                '; '.join(r['igehely'] for r in refs),
                'scope=UBS_DBH_referenciak %s | forras=konkordancia/UBS_DBH_referenciak.tsv | ts=%s' % (s, TS))
            # 6 LXX
            lxx = sorok_strongra(A / 'lxx_dontesek.tsv', 'heber_strong', s)
            for r in lxx:
                add(6, ny, 'adat/lxx_dontesek.tsv', s, r['igehely'], '%s %s %s' % (r['gorog_lemma'], r['gorog_strong'], r['tipus']),
                    r['proveniencia'] or 'manual')
            parok = Counter(r['gorog_strong'] for r in sorok_strongra(K / 'LXX_versszintu_parok.tsv', 'heber_strong', s))
            add(6, ny, 'konkordancia/LXX_versszintu_parok.tsv', s, '%d pár' % sum(parok.values()),
                ', '.join('%s×%d' % kv for kv in parok.most_common(12)),
                'scope=LXX_versszintu_parok %s | forras=konkordancia/LXX_versszintu_parok.tsv | ts=%s' % (s, TS))
            # 7 SECE
            for r in sorok_strongra(K / 'SECE_H_teljes.tsv', 'Strong_padded', s, skip=False):
                add(7, ny, 'konkordancia/SECE_H_teljes.tsv', s, r['Strong_eredeti'], r['Teljes_szocikk'],
                    'scope=SECE_H %s | forras=konkordancia/SECE_H_teljes.tsv | ts=%s' % (s, TS))
            # 8 BDB etimológia
            for r in sorok_strongra(K / 'BDB_etimologia_kezi_hatarok.tsv', 'strong', s):
                add(8, ny, 'konkordancia/BDB_etimologia_kezi_hatarok.tsv', s, r.get('allapot', ''),
                    r.get('nyelvi_hatter', ''),
                    'scope=BDB_etimologia_kezi_hatarok %s | forras=konkordancia/BDB_etimologia_kezi_hatarok.tsv | ts=%s' % (s, TS),
                    ('BDB', s, s, 'nyelvi_hatter', 'forditas_hu'), fkulcs('BDB', s, s, 'nyelvi_hatter', 'forditas_hu'))
            # 9 BDB vers-jelentés, BSB
            bv = sorok_strongra(A / 'bdb_vers_jelentes.tsv', 'strong', s)
            add(9, ny, 'adat/bdb_vers_jelentes.tsv', s, '%d sor' % len(bv),
                '; '.join('%s→%s' % (r['karoli_vers'], r['utvonal']) for r in bv[:40]),
                (bv[0]['proveniencia'] if bv and bv[0]['proveniencia'] else 'scope=adat/bdb_vers_jelentes.tsv | ts=%s' % TS))
            # 10 kiejtés
            for r in sorok_strongra(A / 'kiejtes_kivetelek.tsv', 'strong', s):
                add(10, ny, 'adat/kiejtes_kivetelek.tsv', s, '—', ' '.join(r.values()),
                    'scope=kiejtes_kivetelek %s | ts=%s' % (s, TS))
            # 13 Károli
            for r in sorok_strongra(A / 'bdb_karoli.tsv', 'strong', s):
                add(13, ny, 'adat/bdb_karoli.tsv', s, '%s %s' % (r['tipus'], r['karoli_alak']),
                    '%s (%s)' % (r['pelda_versek'], r['tahot_elofordulas']), r['proveniencia'] or 'manual')
            # glossza
            for r in sorok_strongra(A / 'glosszak_heber_hu.tsv', 'strong', s):
                add(5, ny, 'adat/glosszak_heber_hu.tsv', s, r['entry_id'], '%s → %s' % (r['glossza_en'], r['glossza_hu']),
                    'scope=glosszak_heber_hu %s | forras=adat/glosszak_heber_hu.tsv (%s, %s) | ts=%s' % (s, r['allapot'], r['modell'], TS))
            # OSHL / TWOT
            for r in sorok_strongra(K / 'OSHL_lexikalis_index.tsv', 'strong', s):
                add(3, ny, 'konkordancia/OSHL_lexikalis_index.tsv', s, 'TWOT %s' % r['twot'], r['def_en'],
                    'scope=OSHL_lexikalis_index %s | forras=konkordancia/OSHL_lexikalis_index.tsv | ts=%s' % (s, TS))
        else:
            # 1 TBESG
            for i, l in tbes_blokkok('TBESG.txt', s):
                add(1, ny, 'TBESG.txt', s, 'sor %d' % i, l,
                    'scope=TBESG.txt %s | forras=konkordancia/TBESG.txt (sorillesztés) | ts=%s' % (s, TS),
                    ('TBESG', s, s, 'teljes', 'forditas_hu'), fkulcs('TBESG', s, s, 'teljes', 'forditas_hu'))
            # 2 Thayer
            eid = 'G' + num
            szak = sorok_strongra(A / 'thayer_szakaszok.tsv', 'strong', s)
            for r in szak:
                add(2, ny, 'adat/thayer_szakaszok.tsv', s, 'sz%s %s' % (r['sorszam'], r['utvonal']), r['szoveg'],
                    r['proveniencia'] or 'manual', ('Thayer', s, eid, 'sz' + r['sorszam'], 'forditas_hu'),
                    fkulcs('Thayer', s, eid, 'sz' + r['sorszam'], 'forditas_hu'))
            tv = sorok_strongra(A / 'thayer_vers_jelentes.tsv', 'strong', s)
            add(9, ny, 'adat/thayer_vers_jelentes.tsv', s, '%d sor' % len(tv),
                '; '.join('%s→sz%s' % (r['karoli_vers'], r['szakasz']) for r in tv),
                tv[0]['proveniencia'] if tv else 'manual')
            # 3 tW
            for r in L.read_tsv_skip_comments(K / 'tW_szocikkek.tsv'):
                if s in r['strong'].split('+'):
                    first = r['strong'].split('+')[0]
                    add(3, ny, 'konkordancia/tW_szocikkek.tsv', s, r['tw_id'], r['szoveg'],
                        'scope=tW_szocikkek %s | forras=konkordancia/tW_szocikkek.tsv (commit %s) | ts=%s' % (s, r['forras_commit'][:10], TS),
                        ('tW_szocikkek', first, r['tw_id'], '—', 'forditas_hu'),
                        fkulcs('tW_szocikkek', first, r['tw_id'], '—', 'forditas_hu'))
            # 4-5 UBS DNTG, SDGNT, MCGED
            for r in sorok_strongra(K / 'UBS_DNTG_jelentesek.tsv', 'strong', s):
                for mezo, src, n in (('definicio_hu', 'definicio_rovid', 4), ('glosszak_hu', 'glosszak', 5)):
                    add(n, ny, 'konkordancia/UBS_DNTG_jelentesek.tsv', s, '%s %s' % (r['lexid'], r['entry_kod']), r[src],
                        'scope=UBS_DNTG_jelentesek %s | forras=konkordancia/UBS_DNTG_jelentesek.tsv | ts=%s' % (s, TS),
                        ('UBS_DNTG', s, r['lexid'], r['entry_kod'], mezo), fkulcs('UBS_DNTG', s, r['lexid'], r['entry_kod'], mezo))
            for r in sorok_strongra(K / 'SDGNT_domenek.tsv', 'strong', s):
                add(4, ny, 'konkordancia/SDGNT_domenek.tsv', s, r['domen_kod'], '%s — %s' % (r['domen'], r['glossza']),
                    'scope=SDGNT_domenek %s | forras=konkordancia/SDGNT_domenek.tsv | ts=%s' % (s, TS))
            for r in sorok_strongra(K / 'MCGED_teljes.tsv', 'strong', s):
                add(5, ny, 'konkordancia/MCGED_teljes.tsv', s, r['gk_szam'], r['glossza'],
                    'scope=MCGED %s | forras=konkordancia/MCGED_teljes.tsv | ts=%s' % (s, TS),
                    ('MCGED', s, r['gk_szam'], '—', 'glosszak_hu'), fkulcs('MCGED', s, r['gk_szam'], '—', 'glosszak_hu'))
            refs = sorok_strongra(K / 'UBS_DNTG_referenciak.tsv', 'strong', s)
            add(9, ny, 'konkordancia/UBS_DNTG_referenciak.tsv', s, '%d referencia' % len(refs),
                '; '.join(r['igehely'] for r in refs),
                'scope=UBS_DNTG_referenciak %s | forras=konkordancia/UBS_DNTG_referenciak.tsv | ts=%s' % (s, TS))
            # 6 LXX-híd (görög → héber)
            parok = Counter(r['heber_strong'] for r in sorok_strongra(K / 'LXX_versszintu_parok.tsv', 'gorog_strong', s))
            add(6, ny, 'konkordancia/LXX_versszintu_parok.tsv', s, '%d pár' % sum(parok.values()),
                ', '.join('%s×%d' % kv for kv in parok.most_common(12)),
                'scope=LXX_versszintu_parok %s | forras=konkordancia/LXX_versszintu_parok.tsv | ts=%s' % (s, TS))
            # 7 SECE_G
            for r in sorok_strongra(K / 'SECE_G_teljes.tsv', 'Strong_padded', s, skip=False):
                add(7, ny, 'konkordancia/SECE_G_teljes.tsv', s, r['Strong_eredeti'], r['Teljes_szocikk'],
                    'scope=SECE_G %s | forras=konkordancia/SECE_G_teljes.tsv | ts=%s' % (s, TS))
            # 8 LSJ
            for r in sorok_strongra(K / 'LSJ_teljes.tsv', 'Strong_padded', s, skip=False):
                add(8, ny, 'konkordancia/LSJ_teljes.tsv', s, r['Strong_eredeti'], r['Teljes_szocikk'],
                    'scope=LSJ %s | forras=konkordancia/LSJ_teljes.tsv | ts=%s' % (s, TS),
                    ('LSJ', s, s, 'teljes', 'forditas_hu'), fkulcs('LSJ', s, s, 'teljes', 'forditas_hu'))
        # 10 kiejtés: nem szótári sor; a forrás állapota
        if ny == 'heber':
            kiv = [r for r in L.read_tsv_skip_comments(A / 'kiejtes_heber_kivetelek.tsv') if r['strong'] == s]
            add(10, ny, 'adat/kiejtes_heber_kivetelek.tsv + TBESH STEP-átírás', s, '%d kivétel-sor' % len(kiv),
                (kiv[0]['ertek'] if kiv else 'nincs jóváhagyott héber kivétel-sor: a render a STEP-átírást adja (lexikon_general.lemma_kiejtes)'),
                'scope=kiejtes_heber_kivetelek %s | forras=adat/kiejtes_heber_kivetelek.tsv | ts=%s' % (s, TS))
        else:
            add(10, ny, 'kiejtes.py szabálytábla (TBESG-átírásból)', s, 'számolt',
                'a kiejtés a render-időben számolt (lexikon_general.gorog_magyaros), nem szótári sor',
                'scope=kiejtes %s | forras=manual (a generátor kódja) | ts=%s' % (s, TS))
        # 13 Károli-megfelelők: adat/karoli_strong/szavak_*.tsv (hu oldal, a Strongra párosított szavak)
        alak = Counter()
        for fp in sorted((A / 'karoli_strong').glob('szavak_*.tsv')):
            for r in L.read_tsv_skip_comments(fp):
                if r['strong'] == s and r['oldal'] == 'hu':
                    alak[r['szo']] += 1
        add(13, ny, 'adat/karoli_strong/szavak_*.tsv', s, '%d alak, %d szó' % (len(alak), sum(alak.values())),
            ', '.join('%s×%d' % kv for kv in alak.most_common(25)),
            'scope=adat/karoli_strong/szavak_*.tsv (oldal=hu, strong=%s) | forras=split | ts=%s' % (s, TS))
        # 14 rejtett/hamis párhuzam: a 13. szerepből származtatott lekérdezés, itt nem gyűjtve
        add(14, ny, 'származtatott (13. szerep)', s, '—',
            'nem gyűjtve: a 13. szerepből a render-időben származtatott lekérdezés (nem új forrás)',
            'scope=— | forras=manual | ts=%s' % TS)
    # 12 Nave: nyelvfüggetlen, a motívum verseire (nem Strong-kulcsú)
    E_versek = set()
    for r in E:
        E_versek.update(versre(r['igehely']))
    tema = Counter()
    for r in L.read_tsv_skip_comments(K / 'Nave_basokant.tsv'):
        if r['igehely_karoli'] in E_versek:
            tema[r['tema']] += 1
    for ny in ('heber', 'gorog'):
        add(12, ny, 'konkordancia/Nave_basokant.tsv', '+'.join(strongok), '%d téma, %d hivatkozás' % (len(tema), sum(tema.values())),
            ', '.join('%s×%d' % kv for kv in tema.most_common(25)),
            'scope=Nave_basokant × %s versei (%d vers, igehely_karoli) | forras=konkordancia/Nave_basokant.tsv | ts=%s' % (mid, len(E_versek), TS))

    # szerep-kínálat
    for sz in szerepek:
        ny = sz['nyelv']
        n = int(sz['sorrend'])
        db = [r for r in sorok if r[0] == ny and r[1] == n]
        lefed.append([ny, n, sz['szerep'], sz['allapot'], len(db),
                      ', '.join(sorted({'%s:%s' % (r[3], r[2]) for r in db})) or 'ÜRES (a kínálat nem tartalmaz sort)',
                      'scope=adat/szotar_szerepek.tsv × %s Strongjai (%s) | forras=F123_adat_%s_szotar.tsv | ts=%s'
                      % (mid, '+'.join(strongok), mid, TS)])

    ir_tsv('F123_adat_%s_szotar.tsv' % mid,
           ['nyelv', 'szerep_sorrend', 'forras', 'strong', 'kulcs', 'hossz', 'sha1_10', 'kivonat_160',
            'forditas_kulcs', 'forditas_allapot', 'proveniencia'],
           sorted(sorok, key=lambda r: (r[3], r[1])), 'F123 X.A szótári sorok %s' % mid)
    ir_tsv('F123_adat_%s_forditas_hiany.tsv' % mid,
           ['nyelv', 'szerep_sorrend', 'forras', 'strong', 'szotar', 'strong_kulcs', 'entry_id', 'jelentes_szam', 'mezo',
            'proveniencia'], hiany, 'F123 X.A hiányzó fordítások %s (a forditasok.tsv-be NEM írva)' % mid)
    ir_tsv('F123_adat_%s_szerepkinalat.tsv' % mid,
           ['nyelv', 'sorrend', 'szerep', 'matrix_allapot', 'sor_db', 'forrasok', 'proveniencia'],
           sorted(lefed, key=lambda r: (r[0], r[1])), 'F123 X.A szerepenkénti nyers kínálat %s' % mid)
    print('STRONGOK\t' + ','.join(strongok))
    print('SOROK\t%d' % len(sorok))
    print('HIANY\t%d' % len(hiany))
    for r in hiany:
        print('H\t' + '\t'.join(str(x) for x in r[:9]))
    for r in sorted(lefed, key=lambda r: (r[0], r[1])):
        print('SZ\t%s\t%d\t%s\t%d\t%s' % (r[0], r[1], r[2][:30], r[4], r[5][:120]))


# ---------------------------------------------------------------------------
IGEHELY_RE = None


def igehely_re():
    """Igehely-említések: 'Könyv f:v' és a folytatólagos ', v' / '; f:v' alakok a könyvnév öröklésével."""
    _, hu2step = L.book_tables()
    konyvek = sorted(hu2step, key=len, reverse=True)
    kp = '|'.join(re.escape(k) for k in konyvek)
    return re.compile(r'(?<![\w])(%s)\.?\s*(\d+)\s*[:,]\s*(\d+)((?:\s*[-–]\s*\d+)?(?:\s*[,.]\s*\d+(?![:\d]))*)' % kp)


def emlitesek(szoveg, rx):
    ki = Counter()
    for m in rx.finditer(szoveg):
        konyv, f, v, tobb = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4) or ''
        ki['%s %d:%d' % (konyv, f, v)] += 1
        for t in re.findall(r'[,.]\s*(\d+)', tobb):
            ki['%s %d:%d' % (konyv, f, int(t))] += 1
        rm = re.match(r'\s*[-–]\s*(\d+)', tobb)
        if rm:
            for x in range(v + 1, int(rm.group(1)) + 1):
                ki['%s %d:%d' % (konyv, f, x)] += 1
    return ki


def cmd_proza(mid):
    E, _ = motivum_sorok(mid)
    m = {r['id']: r for r in L.read_tsv_skip_comments(ROOT / 'adat' / 'motivumok.tsv')}[mid]
    forras = m.get('forras_fajl') or ''
    # a motívumtábla utolsó oszlopa a tanulmány útvonala
    utvonal = [v for v in m.values() if isinstance(v, str) and v.endswith('.md')]
    tan = ROOT / utvonal[-1]
    lex = ROOT / 'lexikon' / ('%s_TUDOMANYOS.md' % mid)
    rx = igehely_re()
    t_szoveg = tan.read_text(encoding='utf-8')
    l_szoveg = lex.read_text(encoding='utf-8')
    # lexikonoldal: kézi rések (RÉS-KEZDET/VÉGE) vs a többi
    res_rx = re.compile(r'<!-- RÉS-KEZDET: (\w+) -->(.*?)<!-- RÉS-VÉGE: \1 -->', re.S)
    resek = {}
    for mm in res_rx.finditer(l_szoveg):
        resek.setdefault(mm.group(1), '')
        resek[mm.group(1)] += mm.group(2)
    nem_res = res_rx.sub(' ', l_szoveg)
    res_eml = {k: emlitesek(v, rx) for k, v in resek.items()}
    tan_eml = emlitesek(t_szoveg, rx)
    nem_res_eml = emlitesek(nem_res, rx)
    # előfordulás-sor adatmezői (kapcsolodas + funkcio) — mint az adatmező-réteg
    sorok = []
    for r in E:
        versek = versre(r['igehely'])
        def db(c):
            return sum(c.get(v, 0) for v in versek)
        res_db = {k: db(c) for k, c in res_eml.items()}
        proza_ossz = sum(res_db.values())
        kat = 'nem nevezi meg' if proza_ossz == 0 else ('érinti (1–3)' if proza_ossz <= 3 else 'tárgyalja (4+)')
        sorok.append([r['igehely'], r['strong'], db(tan_eml), proza_ossz,
                      '; '.join('%s:%d' % (k, v) for k, v in sorted(res_db.items()) if v) or '—',
                      db(nem_res_eml), kat, (r['kapcsolodas'] + ' // ' + r['funkcio']).strip(' /')])
    prov = ('scope=%s: adat/elofordulasok.tsv (%d sor) × %s (%d bájt) + %s (%d bájt; RÉS-KEZDET/VÉGE rések: %s) | '
            'forras=saját számláló (naplok/F123_adat_keszito.py proza; „Könyv f:v” + folytatólagos versszám, tartomány versre) | ts=%s'
            % (mid, len(E), tan.relative_to(ROOT).as_posix(), len(t_szoveg.encode('utf-8')),
               lex.relative_to(ROOT).as_posix(), len(l_szoveg.encode('utf-8')), ','.join(sorted(resek)), TS))
    ir_tsv('F123_adat_%s_proza_lefedettseg.tsv' % mid,
           ['igehely', 'strong', 'tanulmany_emlites', 'lexikon_res_emlites', 'resenkent', 'lexikon_nem_res_emlites',
            'kategoria', 'adatmezo_kapcsolodas_funkcio', 'proveniencia'],
           [s + [prov] for s in sorok], 'F123 X.A próza-lefedettség %s — az értelmező menet viszi át a motivumok/naplok/-ba' % mid)
    print('PROV\t' + prov)
    c = Counter(s[6] for s in sorok)
    for k, v in sorted(c.items()):
        print('KAT\t%s\t%d' % (k, v))
    print('TAN_0\t%d' % sum(1 for s in sorok if s[2] == 0))
    print('NEM_NEVEZI\t' + ', '.join(s[0] for s in sorok if s[6] == 'nem nevezi meg'))
    for k in sorted(resek):
        print('RES\t%s\t%d bájt\t%d említés' % (k, len(resek[k].encode('utf-8')), sum(res_eml[k].values())))


# ---------------------------------------------------------------------------
SEOL_FENYEGETES = ['H4194', 'H8179', 'H0953', 'H7845']
SEOL_KIALTAS = ['H7121', 'H2199', 'H6817', 'H7768']


def cmd_seol():
    """2e. 4.: (halál/sír-fenyegetés) ∩ (kiáltás) egy versben, H7585 nélkül; a H8179 csak H4194-gyel együtt
    („halál kapui”). A szabadulás-elem és a „az Úrhoz” megszorítás nem determinisztikusan szűrhető: a kimenet
    jelöli a versben álló H3068 / H0410 / H0430 és a szabadulás-igék (H5337, H3467, H4422, H6403, H2502, H1350,
    H6299, H5927) jelenlétét, mért mezőként, ítélet nélkül."""
    tahot = L.load_tahot()
    versek = defaultdict(set)
    for r in tahot:
        for s in r['Strong-szám'].split('+'):
            versek[r['_parsed']].add(s.strip())
    prov_sorok = []
    # a determinisztikus lekérdezések naplózása (kollokáció párok)
    for f in SEOL_FENYEGETES:
        for k in SEOL_KIALTAS:
            _, prov = lekerdez_futtat(['kollokacio', f, k])
            prov_sorok.append(prov)
    _, prov7585 = lekerdez_futtat(['scan', 'H7585'])
    prov_sorok.append(prov7585)
    SZAB = ['H5337', 'H3467', 'H4422', 'H6403', 'H2502', 'H1350', 'H6299', 'H5927']
    ISTEN = ['H3068', 'H0410', 'H0430']
    talalat = []
    for p, ss in versek.items():
        if 'H7585' in ss:
            continue
        fen = [s for s in SEOL_FENYEGETES if s in ss]
        if 'H8179' in fen and 'H4194' not in ss:
            fen.remove('H8179')
        kia = [s for s in SEOL_KIALTAS if s in ss]
        if fen and kia:
            talalat.append((p, fen, kia, [s for s in ISTEN if s in ss], [s for s in SZAB if s in ss]))
    # rendezés kánon szerint: a TAHOT fájlsorrend helyett könyv-sorrend a Károli-kulcsok elsőbbségével
    sorrend = {}
    for i, k in enumerate(L.load_karoli_1908()):
        try:
            sorrend[L.parse_igehely(k)] = i
        except ValueError:
            pass
    talalat.sort(key=lambda t: sorrend.get(t[0], 10 ** 9))
    E, _ = motivum_sorok('ALVIL-001')
    E_versek = set()
    for r in E:
        E_versek.update(versre(r['igehely']))
    dublett = {('2Sám', 22): ('Zsolt', 18), ('Zsolt', 18): ('2Sám', 22)}
    sorok = []
    onallo = set()
    for p, fen, kia, ist, sza in talalat:
        ig = '%s %d:%d' % p
        kulcs = (p[0], p[1])
        if kulcs in dublett:
            hely = '2Sám 22 = Zsolt 18 (dublett)'
        else:
            hely = ig
        onallo.add(hely)
        sorok.append([ig, '+'.join(fen), '+'.join(kia), '+'.join(ist) or '—', '+'.join(sza) or '—',
                      'igen' if ig in E_versek else 'nem', hely])
    prov = ('scope=TAHOT-teljes: (H4194 | H8179[+H4194] | H0953 | H7845) ∩ (H7121 | H2199 | H6817 | H7768) egy versben, '
            'H7585 nélkül; dublett: 2Sám 22 = Zsolt 18 egy hely | forras=konkordancia/TAHOT_kivonat.tsv (lekerdez.load_tahot) | '
            'ts=%s' % TS)
    ir_tsv('F123_adat_ALVIL-001_seol_nelkul.tsv',
           ['igehely', 'fenyegetes_strong', 'kialtas_strong', 'isten_nev_a_versben', 'szabadulas_ige_a_versben',
            'alvil001_elofordulas', 'onallo_hely', 'proveniencia'],
           [s + [prov] for s in sorok], 'F123 X.A 2e. 4. Seól nélküli scan (mért mezők, ítélet nélkül)')
    print('PROV\t' + prov)
    for p in prov_sorok:
        print('PROVQ\t' + p)
    print('VERSEK\t%d' % len(sorok))
    print('ONALLO\t%d' % len(onallo))
    isten = {s[6] for s in sorok if s[3] != '—'}
    isten_szab = {s[6] for s in sorok if s[3] != '—' and s[4] != '—'}
    print('ONALLO_ISTENNEVVEL\t%d' % len(isten))
    print('ONALLO_ISTENNEV_ES_SZABADULAS\t%d' % len(isten_szab))
    for s in sorok:
        print('T\t' + '\t'.join(s))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == 'f108':
        cmd_f108(sys.argv[2])
    elif cmd == 'szotar':
        cmd_szotar(sys.argv[2])
    elif cmd == 'proza':
        cmd_proza(sys.argv[2])
    elif cmd == 'seol':
        cmd_seol()
    else:
        sys.exit('ismeretlen alparancs: %s' % cmd)


if __name__ == '__main__':
    main()
