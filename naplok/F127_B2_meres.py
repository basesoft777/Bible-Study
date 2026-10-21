"""F127 B2: a pilot motívumközi jelöltjeinek mért alapja (saját lekérdezés).

A felmérés (naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md, 3-5.) számai nem
források; ez a szkript újra méri:
  1. a két oldal igehelyei előfordulás-e a saját motívumukban
     (adat/elofordulasok.tsv, split('\\t'));
  2. a fejezeten belüli versszomszédság (a vers sorszáma a fejezetben,
     konkordancia/Karoli_1908.tsv sorrendje szerint) -- a távolság versekben;
  3. mindkét oldal Károli-szövege és Károli-KH-ja: eszkozok/lekerdez.py karoli
     --naplo F127 --lepes adhoc (a proveniencia-sor naplok/F127_lekerdezesek.tsv-be).

A „beszéd”-szomszédság (pl. Péter pünkösdi beszéde) nem adat: a szkript csak
a fejezetet és a versek távolságát méri; a beszéd határa értelmezés.

Kimenet: naplok/F127_B2_szomszedsag.tsv (+ a lekerdez.py kimenete a
naplok/F127_B2_karoli.txt-be).

    python naplok/F127_B2_meres.py
"""
import datetime
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (jelölt-azonosító, saját motívum, saját igehely(ek), célmotívum, cél-igehely(ek))
PAROK = [
    ('a', 'ISTENTISZT-001', ['Zsolt 116:4'], 'ALVIL-001', ['Zsolt 116:3']),
    ('b', 'ISTENTISZT-001', ['ApCsel 2:21'], 'ALVIL-001', ['ApCsel 2:27', 'ApCsel 2:31']),
    ('c', 'ISTENTISZT-001', ['1Móz 4:26'], 'HAMART-001',
     ['1Móz 4:2-3', '1Móz 4:7', '1Móz 4:10-11', '1Móz 4:12', '1Móz 4:14']),
    ('d', 'ISTENTISZT-001', ['1Móz 12:8'], 'HAMART-001', ['1Móz 12:3']),
    ('e', 'ISTENTISZT-001', ['Róm 10:12', 'Róm 10:13', 'Róm 10:14'], 'TEREMT-001', ['Róm 10:7']),
]

_IG = re.compile(r'^(.+?) (\d+):(\d+)(?:-(\d+))?$')


def tsv(path):
    with open(path, encoding='utf-8', newline='') as f:
        sorok = [s.rstrip('\r') for s in f.read().split('\n')]
    sorok = [s for s in sorok if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def bont(igehely):
    m = _IG.match(igehely)
    if not m:
        raise ValueError('nem értelmezhető igehely: %r' % igehely)
    k, f, v1, v2 = m.groups()
    return k, int(f), int(v1), int(v2 or v1)


def main():
    elof = tsv(os.path.join(ROOT, 'adat', 'elofordulasok.tsv'))
    elof_kulcs = {(r['id'], r['igehely']) for r in elof}
    karoli = tsv(os.path.join(ROOT, 'konkordancia', 'Karoli_1908.tsv'))
    # vers sorszáma a fejezeten belül (a Károli-tábla saját sorrendje)
    fej_versek = {}
    for r in karoli:
        k, f, v, _ = bont(r['Igehely'])
        fej_versek.setdefault((k, f), []).append(v)

    ts = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ')
    ki = ['\t'.join(['jelolt', 'id', 'igehely', 'id_elofordulas', 'cel_id', 'cel_igehely',
                     'cel_elofordulas', 'fejezet_azonos', 'tavolsag_vers', 'proveniencia'])]
    lekerdezendo = []
    for jel, mid, sajat, cel, celok in PAROK:
        for s in sajat:
            for c in celok:
                sk, sf, sv1, sv2 = bont(s)
                ck, cf, cv1, cv2 = bont(c)
                azonos = (sk, sf) == (ck, cf)
                if azonos:
                    # a két vers(tartomány) közti legkisebb távolság a fejezet versrendjében
                    rend = fej_versek[(sk, sf)]
                    poz = {v: i for i, v in enumerate(rend)}
                    tav = min(abs(poz[a] - poz[b]) for a in range(sv1, sv2 + 1) for b in range(cv1, cv2 + 1))
                else:
                    tav = ''
                prov = ('scope=%s %s ↔ %s %s | forras=elofordulasok.tsv+Karoli_1908.tsv | ts=%s'
                        % (mid, s, cel, c, ts))
                ki.append('\t'.join([jel, mid, s, 'igen' if (mid, s) in elof_kulcs else 'NEM',
                                     cel, c, 'igen' if (cel, c) in elof_kulcs else 'NEM',
                                     'igen' if azonos else 'nem', str(tav), prov]))
                lekerdezendo += [s, c]
    with open(os.path.join(ROOT, 'naplok', 'F127_B2_szomszedsag.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# F127 B2: a pilot motívumközi jelöltjeinek mért szomszédsága (naplok/F127_B2_meres.py)\n')
        f.write('\n'.join(ki) + '\n')
    print('\n'.join(ki))

    # Károli-szöveg + KH, proveniencia-naplóval
    lattuk = []
    kimenet = []
    for ig in lekerdezendo:
        for v in ([ig] if '-' not in ig else ['%s %d:%d' % (bont(ig)[0], bont(ig)[1], x)
                                               for x in range(bont(ig)[2], bont(ig)[3] + 1)]):
            if v in lattuk:
                continue
            lattuk.append(v)
            p = subprocess.run([sys.executable, os.path.join(ROOT, 'eszkozok', 'lekerdez.py'),
                                '--naplo', 'F127', '--lepes', 'adhoc', 'karoli', v],
                               capture_output=True, text=True, encoding='utf-8',
                               env=dict(os.environ, PYTHONIOENCODING='utf-8'))
            if p.returncode:
                print('HIBA: lekerdez.py karoli %s: %s' % (v, p.stderr.strip()), file=sys.stderr)
                return 1
            kimenet.append(p.stdout.rstrip('\n'))
    with open(os.path.join(ROOT, 'naplok', 'F127_B2_karoli.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n\n'.join(kimenet) + '\n')
    print('lekérdezett vers: %d (naplok/F127_B2_karoli.txt, naplok/F127_lekerdezesek.tsv)' % len(lattuk))
    return 0


if __name__ == '__main__':
    sys.exit(main())
