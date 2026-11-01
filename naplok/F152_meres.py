"""F152 B0/B5 mérés: a lexikonlap mérete, az ismétlődő forrásmegjelölés, a „gerinc” szó, az ismétlődő kizárt sorok.

Futtatás: python naplok/F152_meres.py lexikon/ISTENTISZT-001_TUDOMANYOS.md [lexikon/ALVIL-001_TUDOMANYOS.md …]
A TSV-t nem olvas; csak a markdown-lapot, soronként (split('\n')).
"""
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# a generátor mintája (a lekérdezés strong= / n= / csatorna= mezőivel is; ELLENOR_F152 B.2)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'eszkozok'))
from szerep_kizart import PROV_HARMAS as PROV  # noqa: E402


def mer(utvonal):
    with open(utvonal, encoding='utf-8') as f:
        szoveg = f.read()
    sorok = szoveg.split('\n')
    print('== %s' % utvonal)
    print('méret: %d bájt (%.1f KB), %d sor' % (len(szoveg.encode('utf-8')), len(szoveg.encode('utf-8')) / 1024,
                                              len(sorok)))
    bajt = 0
    szakasz = '(eleje)'
    szakasz_prov = collections.Counter()
    for i, s in enumerate(sorok):
        if s.startswith('## 6. Értelmezés'):
            print('a 6. Értelmezés kezdete: %d. sor, a lap %.0f%%-ánál (bájt)' % (
                i + 1, 100 * bajt / len(szoveg.encode('utf-8'))))
        bajt += len(s.encode('utf-8')) + 1
        if s.startswith('## ') or s.startswith('### '):
            szakasz = s.strip('# ').strip()
        for m in PROV.finditer(s):
            szakasz_prov[(szakasz, m.group(0).replace('\\|', '|'))] += 1
    print('scope=manual összesen: %d' % szoveg.count('scope=manual'))
    for nev in ('forras=Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md',
                'forras=Segitsegul_hivni_az_Urat_tematikus.md'):
        print('%s: %d' % (nev, szoveg.count(nev)))
    print('proveniencia-sorok összesen (scope=…|forras=…|ts=…): %d; ebből ugyanabban a szakaszban ismétlődő: %d' % (
        sum(szakasz_prov.values()), sum(n - 1 for n in szakasz_prov.values() if n > 1)))
    for (sz, p), n in szakasz_prov.most_common(8):
        if n > 1:
            print('  %3d× | %s | %s' % (n, sz[:40], p[:110]))
    g = [(i + 1, s) for i, s in enumerate(sorok) if re.search(r'[Gg]erinc', s)]
    print('„gerinc” sor: %d' % len(g))
    olv = [x for x in g if not x[1].lstrip().startswith('*') and not x[1].lstrip().startswith('<!--')]
    print('  ebből nem dőlt üzemeltetői mondat / komment: %d' % len(olv))
    for i, s in olv[:30]:
        print('    %d: %s' % (i, s[:150]))
    # az 1/b. azonos indoklású egymást követő sorai
    tabla = [s for s in sorok if s.startswith('| 1Móz 25:')]
    print('1Móz 25:… sor a lapon: %d' % len(tabla))
    m = [s for s in sorok if 'Kereszthivatkozásból minősített jelöltek' in s]
    if m:
        k = sorok.index(m[0])
        v = k + 1
        while v < len(sorok) and (sorok[v].startswith('|') or not sorok[v].strip()):
            v += 1
        print('Minősítés jelölt-tábla: %d sor, %.1f KB' % (
            sum(1 for s in sorok[k:v] if s.startswith('| ') and not s.startswith('|---')) - 1,
            sum(len(s.encode('utf-8')) + 1 for s in sorok[k:v]) / 1024))


for u in sys.argv[1:]:
    mer(u)
