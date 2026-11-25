"""F239 U3b — a Róm 10:7 görög ószövetségi háttere: a LXX_OS azon versei, amelyekben az ἄβυσσος
a καταβαίνω (leszáll), az ἀνάγω (felhoz) vagy az ἀναβαίνω (felmegy) igével együtt áll (D2.1 ellenőrzése).
Kimenet: vers, Károli-kulcs, a talált igék szóalakkal."""
import sys, glob, os

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

IGEK = {'καταβαίνω', 'ἀνάγω', 'ἀναβαίνω'}
talalat = {}
for ut in sorted(glob.glob('konkordancia/LXX_OS/*.tsv')):
    fejlec = None
    for s in open(ut, encoding='utf-8'):
        if s.startswith('#'):
            continue
        m = s.rstrip('\r\n').split('\t')
        if fejlec is None:
            fejlec = {n: i for i, n in enumerate(m)}
            if 'igehely_lxx' not in fejlec:
                print('kihagyva (más fejléc): %s' % os.path.basename(ut))
                break
            continue
        v = m[fejlec['igehely_lxx']]
        d = talalat.setdefault((os.path.basename(ut), v), {'karoli': m[fejlec['igehely_karoli']], 'szavak': []})
        d['szavak'].append((m[fejlec['lemma']], m[fejlec['szoalak']]))
n = 0
for (f, v), d in talalat.items():
    lemmak = {l for l, _ in d['szavak']}
    if 'ἄβυσσος' in lemmak and lemmak & IGEK:
        n += 1
        alakok = [a for l, a in d['szavak'] if l in IGEK or l == 'ἄβυσσος']
        print('%s\t%s\t%s' % (v, d['karoli'], ' '.join(alakok)))
print('n=%d' % n)
