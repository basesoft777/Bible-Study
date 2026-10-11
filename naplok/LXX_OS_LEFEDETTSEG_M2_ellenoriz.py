"""F54 / M2 -- az LXX_OS Karoli-kulcsok ellenorzese (csak olvas).

  1. kettos kulcs: egy Karoli-vershez egy szovegvaltozaton (fajlon) belul tobb LXX-vers
  2. idegen kulcs: igehely_karoli, amely nincs a Karoli_1908.tsv-ben
  3. konyvenkenti lefedettseg: kulcsolt Karoli-versek / Karoli-versek (elsodleges fajl)

Hasznalat: python naplok/LXX_OS_LEFEDETTSEG_M2_ellenoriz.py
"""
import sys
import os
import re
import glob
import collections

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')).replace('\\', '/') + '/'
sys.path.insert(0, R + 'eszkozok')
import lxx_os_import as L  # noqa: E402

kar = set()
for l in open(R + 'konkordancia/Karoli_1908.tsv', encoding='utf-8'):
    kar.add(l.split('\t')[0])

dupl = []
idegen = []
kulcsolt_primary = collections.defaultdict(set)
for fn in sorted(glob.glob(R + 'konkordancia/LXX_OS/*.tsv')):
    slug = os.path.basename(fn)[:-4]
    if slug.startswith('karoli_') or slug == 'README':
        continue
    m = collections.defaultdict(set)
    for l in open(fn, encoding='utf-8'):
        if l.startswith('#') or l.startswith('igehely_lxx'):
            continue
        p = l.split('\t')
        if p[2]:
            m[p[2]].add(p[0])
            if p[2] not in kar:
                idegen.append((slug, p[2]))
    for k, v in m.items():
        if len(v) > 1:
            dupl.append((slug, k, sorted(v)))
    cim, bk, _t = L.BOOKS[slug]
    kb = L.BOOK_KEY_TO_KAROLI.get(bk)
    if kb and L.elsodleges_slug(kb) == slug:
        kulcsolt_primary[kb] |= set(m)

print('kettos kulcs:', len(dupl))
for d in dupl:
    print('  ', d)
print('idegen kulcs:', len(set(idegen)))
for d in sorted(set(idegen))[:20]:
    print('  ', d)
szam = collections.Counter()
for k in kar:
    szam[k.rsplit(' ', 1)[0]] += 1
print('konyvenkenti lefedettseg (kulcsolt / Karoli-vers):')
for kb in sorted(kulcsolt_primary):
    print('  %s %d / %d' % (kb, len([k for k in kulcsolt_primary[kb] if k in kar]), szam[kb]))
