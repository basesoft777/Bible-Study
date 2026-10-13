"""F91 M2 (A-oldal): a konkordancia/Karoli_versmegfeleltetes.tsv javítása a feliratos zsoltárokra.

Szabály (DT-F91a, A1): a feliratos zsoltárokban (62 zsoltár, d = Károli-max - KJV-max > 0, plusz Zsolt 13
kivétel) az `igehely_kjv` = a Karoli_1908-kulcsú LXX_OS-etalon KJV-értéke (v > d); v <= d (felirat): üres,
a megjegyzésben "felirat" / "felirat 2 vers". A d-szabály (c:(v-d)) csak ellenőrzés.
Írás: '\t'.join, olvasás split('\t') (a csv modul tilos). Idempotens. Nem érintett sor bájtra azonos.

Használat: python eszkozok/f91_versmegf_javit.py [--ir]   (--ir nélkül csak mér)
"""
import sys
import re
import os
import datetime
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'konkordancia')
TABLA = os.path.join(K, 'Karoli_versmegfeleltetes.tsv')
IR = '--ir' in sys.argv
TS = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        data = f.read()
    return data.split('\n')


# Károli / KJV maximumok -> d
kar = defaultdict(set)
for ln in rows(os.path.join(K, 'Karoli_1908.tsv')):
    m = re.match(r'Zsolt (\d+):(\d+)\t', ln)
    if m:
        kar[int(m.group(1))].add(int(m.group(2)))
kjv = defaultdict(set)
for ln in rows(os.path.join(K, 'KJV_Strongs_teljes.tsv')):
    m = re.match(r'Psa\.(\d+)\.(\d+)\t', ln)
    if m:
        kjv[int(m.group(1))].add(int(m.group(2)))
d = {c: max(kar[c]) - max(kjv[c]) for c in range(1, 151)}

# etalon: LXX_OS Károli-vers -> KJV-értékek (halmaz, 'c:v' alak)
et = defaultdict(lambda: defaultdict(set))
for ln in rows(os.path.join(K, 'LXX_OS', 'psalms-lxx.tsv')):
    p = ln.split('\t')
    if len(p) < 4:
        continue
    m = re.fullmatch(r'Zsolt (\d+):(\d+)', p[2])
    if m and p[1]:
        for x in p[1].split(';'):
            et[int(m.group(1))][int(m.group(2))].add(x)

# a kivétel-felismerés: az etalon legnagyobb eltolása (v - kjv_v)
def etalon_d(c):
    best = 0
    for v, s in et[c].items():
        if len(s) == 1:
            m = re.fullmatch(r'(\d+):(\d+)', next(iter(s)))
            if m and int(m.group(1)) == c:
                best = max(best, v - int(m.group(2)))
    return best

erintett = [c for c in range(1, 151) if d[c] > 0 or etalon_d(c) > 0]
dd = {c: (d[c] if d[c] > 0 else etalon_d(c)) for c in erintett}
print('érintett zsoltár:', len(erintett), '| d=1:', sum(1 for c in erintett if dd[c] == 1),
      '| d=2:', [c for c in erintett if dd[c] == 2], '| kivétel (d=0, etalon>0):', [c for c in erintett if d[c] == 0])


def kivalaszt(c, v):
    """-> (kjv_ertek, megjegyzes, forras_jelzo) a javított sorhoz."""
    dc = dd[c]
    if v <= dc:
        return '', ('felirat' if dc == 1 else 'felirat %d vers' % dc)
    s = et[c].get(v)
    if not s:
        return None, 'etalon_hiany'
    return ';'.join(sorted(s, key=lambda x: int(x.split(':')[1]))), ''


lines = rows(TABLA)
ujak = list(lines)
valt = 0
etalon_hiany = []
d_szabaly_elter = []
for i, ln in enumerate(lines):
    p = ln.split('\t')
    if len(p) < 6:
        continue
    m = re.fullmatch(r'Zsolt (\d+):(\d+)', p[0])
    if not m or int(m.group(1)) not in dd:
        continue
    c, v = int(m.group(1)), int(m.group(2))
    ertek, megj = kivalaszt(c, v)
    if ertek is None:
        etalon_hiany.append(p[0])
        continue
    if v > dd[c] and ertek != '%d:%d' % (c, v - dd[c]):
        d_szabaly_elter.append((p[0], ertek, '%d:%d' % (c, v - dd[c])))
    if p[1] != ertek or (megj and p[5] != megj):
        q = list(p)
        q[1] = ertek
        q[4] = 'lxx_os_etalon_f91'
        q[5] = megj
        ujak[i] = '\t'.join(q)
        valt += 1

print('módosuló sor:', valt, '| etalon-hiány:', len(etalon_hiany), etalon_hiany[:5],
      '| d-szabálytól eltérő etalon-sor:', len(d_szabaly_elter), d_szabaly_elter[:5])

# fejléc-jegyzet
JEGYZET = ('# F91 javítás (DT-F91a, A1): a feliratos zsoltárok (%d) igehely_kjv oszlopa az LXX_OS Károli-kulcsú etalonból; '
           'felirat-versek (v <= d) üres KJV, megjegyzés "felirat"; forras=lxx_os_etalon_f91 | forras=eszkozok/f91_versmegf_javit.py | ts=%s'
           % (len(erintett), TS))
if not any(l.startswith('# F91 javítás') for l in ujak):
    idx = max(i for i, l in enumerate(ujak) if l.startswith('#'))
    ujak.insert(idx + 1, JEGYZET)

# védőellenőrzés: minden nem érintett sor bájtra azonos
regi_nem = [l for l in lines if not l.startswith('# F91 javítás') and not (re.match(r'Zsolt (\d+):', l) and int(re.match(r'Zsolt (\d+):', l).group(1)) in dd)]
uj_nem = [l for l in ujak if not (re.match(r'Zsolt (\d+):', l) and int(re.match(r'Zsolt (\d+):', l).group(1)) in dd)
          and not l.startswith('# F91 javítás')]
assert regi_nem == uj_nem, 'nem érintett sor változott: megállok'
assert len([l for l in ujak if not l.startswith('# F91 javítás')]) == len([l for l in lines if not l.startswith('# F91 javítás')])

# ellenőrzés a javított tartalmon: 0 eltérés az etalonnal
def elteres(sorok):
    n = 0
    zs22 = 0
    for l in sorok:
        p = l.split('\t')
        if len(p) < 6:
            continue
        m = re.fullmatch(r'Zsolt (\d+):(\d+)', p[0])
        if not m or int(m.group(1)) not in dd:
            continue
        c, v = int(m.group(1)), int(m.group(2))
        if v <= dd[c]:
            ok = p[1] == ''
        else:
            ok = set(p[1].split(';')) == et[c].get(v, set()) if p[1] else False
        if not ok:
            n += 1
            if c == 22:
                zs22 += 1
    return n, zs22

print('eltérés az etalonnal ELŐTTE (összes érintett, ebből Zsolt 22):', elteres(lines))
print('eltérés az etalonnal UTÁNA:', elteres(ujak))

if IR:
    with open(TABLA, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(ujak))
    print('írva:', TABLA)
