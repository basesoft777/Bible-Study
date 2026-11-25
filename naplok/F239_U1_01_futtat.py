# -*- coding: utf-8 -*-
"""F239 U1 1., 3-6. pont: a hét lépés determinisztikus része (lekerdez.py, --naplo F239).
Kimenet (naplok/): F239_U1_TEREMT-001_lekerdezesek.txt (a nyers kimenetek), _scan.tsv, _igealak.tsv, _lxx_hid.tsv,
_kollokacio.tsv; a proveniencia-sorokat a lekerdez.py a naplok/F239_lekerdezesek.tsv-be naplózza.
Csak olvas (a naplo-fájl a naplok/ alatt). TSV: split('\\t'), '\\t'.join(); csv modul nélkül."""
import sys, os, re, subprocess
from collections import defaultdict, Counter
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L
MID = 'TEREMT-001'
PY = sys.executable
nyers = []

def fut(*arg, lepes='adhoc'):
    cmd = [PY, os.path.join(GY, 'eszkozok', 'lekerdez.py'), arg[0], '--naplo', 'F239', '--lepes', lepes] + list(arg[1:])
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', cwd=GY)
    nyers.append('$ lekerdez.py %s --naplo F239 --lepes %s %s\n%s%s' % (arg[0], lepes, ' '.join('"%s"' % a for a in arg[1:]), r.stdout, ('[stderr] ' + r.stderr) if r.stderr.strip() else ''))
    if r.returncode != 0:
        print('HIBA', cmd[2:], r.stderr.strip().split('\n')[0])
    return r.stdout

def tsv(path):
    return [l.rstrip('\n').split('\t') for l in open(path, encoding='utf-8') if l.strip() and not l.startswith('#')]

# --- adatállapot: E (elofordulasok.tsv) / J:döntés (jeloltek.tsv)
def kibont(ig):
    m = re.match(r'^(.+?) (\d+):(\d+)-(\d+)$', ig)
    if m:
        return ['%s %s:%d' % (m.group(1), m.group(2), v) for v in range(int(m.group(3)), int(m.group(4)) + 1)]
    return [ig]
E = defaultdict(list)
for r in tsv(os.path.join(GY, 'adat', 'elofordulasok.tsv'))[1:]:
    if r[0] == MID:
        for v in kibont(r[1]):
            E[v].append(r[5])
J = defaultdict(list)
for r in tsv(os.path.join(GY, 'adat', 'jeloltek.tsv'))[1:]:
    if r[0] == MID:
        for v in kibont(r[1]):
            J[v].append(r[3])

# --- 1. gerinc-metszet
h_versek = fut('scan', 'H8415', lepes='B2')
g_versek = fut('scan', 'G0012', lepes='B2')
HV = [l for l in h_versek.split('\n') if l and not l.startswith(('#', 'proveniencia'))]
GV = [l for l in g_versek.split('\n') if l and not l.startswith(('#', 'proveniencia'))]
fut('gerinc', '1Móz 1:2', '1Móz 7:11', '1Móz 8:2', lepes='B2')
fut('gerinc', *HV, lepes='B2')
fut('gerinc', *GV, lepes='B2')
fut('gerinc', 'Zsolt 33:7', 'Jób 38:16', 'Ézs 51:10', 'Jón 2:6', 'Hab 3:10', lepes='B2')
fut('gerinc', '1Móz 1:2', 'Jel 20:1', lepes='B2')

# --- 3. scan állapottal
with open(os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_scan.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('# GENERÁLT: naplok/F239_U1_01_futtat.py | scope=TAHOT-teljes+TAGNT-teljes | forras=lekerdez.py scan H8415 / G0012, adat/elofordulasok.tsv, adat/jeloltek.tsv | ts=2026-11-23\n')
    f.write('strong\tigehely\tgerinc_elem\tadat_allapot\n')
    for s, lst in (('H8415', HV), ('G0012', GV)):
        for v in lst:
            al = []
            if v in E: al.append('E')
            for d in J.get(v, []): al.append('J:' + d)
            f.write('%s\t%s\t%s\t%s\n' % (s, v, s, ','.join(al) if al else 'NINCS'))

# --- 4. kollokáció
gr = L.load_grammatikai_strongok()
byv = defaultdict(set); gl = {}
for parsed, strong, src in L.combined_rows():
    byv[parsed].add(strong)
for r in L.load_tahot() + L.load_tagnt():
    gl.setdefault(r['Strong-szám'], r.get('Rövid jelentés', ''))
kol = []
for anchor, kuszob in (('H8415', 5), ('G0012', 3)):
    vs = [p for p, s in byv.items() if anchor in s]
    c = Counter(s for p in vs for s in byv[p] if s not in gr and s != anchor)
    for s, n in c.most_common():
        if n >= kuszob:
            kol.append((anchor, s, n))
with open(os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_kollokacio.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('# GENERÁLT: naplok/F239_U1_01_futtat.py | küszöb: H8415-versekben >=5, G0012-versekben >=3 tartalmi Strong; a mező-hipotézis az U2 dolga\n')
    f.write('gerinc_elem\tkollokalo_strong\tglossza\tversek_a_gerinc_versei_kozott\tkollokacios_versek_szama_egesz_korpuszban\n')
    for a, s, n in kol:
        out = fut('kollokacio', a, s, lepes='B4')
        m = re.search(r'— (\d+) vers', out)
        f.write('%s\t%s\t%s\t%d\t%s\n' % (a, s, gl.get(s, ''), n, m.group(1) if m else '?'))

# --- 5. igealak
with open(os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_igealak.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('# GENERÁLT: naplok/F239_U1_01_futtat.py | forras=lekerdez.py igealak H8415 / G0012 | a binyan/alak szerinti csoportosítás emberi döntés\n')
    f.write('gerinc_elem\tigehely\tragozott_alak\tkiejtes\trovid_jelentes\tangol_tukorforditas\n')
    for s in ('H8415', 'G0012'):
        out = fut('igealak', s, lepes='B4')
        for l in out.split('\n'):
            if l and not l.startswith(('#', 'proveniencia')):
                f.write('%s\t%s\n' % (s, l))

# --- 6. LXX-híd
with open(os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_lxx_hid.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('# GENERÁLT: naplok/F239_U1_01_futtat.py | forras=lekerdez.py lxx-hid (LXX_OS+TAGNT) a H8415 versein | a LXX-szó és a héber szó megfeleltetése nem gépi: a tartalmi LXX-szavak listája, G0012 jelölve\n')
    f.write('gerinc_elem\tigehely\tlxx_vers\tg0012_a_lxx_versben\ttartalmi_lxx_szavak\n')
    for v in HV:
        out = fut('lxx-hid', v, lepes='adhoc')
        lv = re.search(r'# LXX-vers: (.+)', out)
        szavak, van = [], False
        for l in out.split('\n'):
            m = re.match(r'^(G\d+)?\t(\S+)\t(noun|verb|adjective|adverb)', l)
            if m:
                szavak.append('%s %s' % (m.group(1) or '-', m.group(2)))
            if l.startswith('G0012\t'):
                van = True
        f.write('H8415\t%s\t%s\t%s\t%s\n' % (v, lv.group(1) if lv else 'NINCS LXX-vers', 'igen' if van else 'nem', ' | '.join(szavak)))
    for v in GV:
        out = fut('lxx-hid', v, lepes='adhoc')
        f.write('G0012\t%s\t(ÚSZ-hely; nem LXX-vers)\t-\t-\n' % v)

with open(os.path.join(GY, 'naplok', 'F239_U1_TEREMT-001_lekerdezesek.txt'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(nyers))
print('kész; kollokáció-pár:', len(kol))
