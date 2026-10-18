"""F117.3 előtti próba: igazolható-e a KK1b-tervezet `igehely_mt` értéke a felülírandó D/D′ sorokon?

Független MT-tanú: a Macula héber `ref` oszlopa (MT-számozás, a Macula saját vershatára; a `karoli` oszlopot NEM
használjuk, mert az a versmegfeleltető táblából jön). Károli-oldal: a TAHOT_kivonat.tsv (Károli-kulcs, F85).
Jel: a két vers Strong-halmazának Jaccard-értéke (a grammatikai H9xxx nélkül). Csak olvas, kimenet a konzolra.
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'konkordancia')

PROBA = [  # (Károli-könyv, Macula-fájl, Macula-könyvkód, Károli-versek)
    ('Ézs', 'Macula_heber_Ezsaias.tsv', 'ISA', [(3, 1), (3, 2), (3, 27)]),
    ('1Sám', 'Macula_heber_Samuel_1.tsv', '1SA', [(20, 42), (20, 43), (24, 1), (24, 2)]),
    ('1Kir', 'Macula_heber_Kiralyok_1.tsv', '1KI', [(22, 43), (22, 44), (22, 45), (22, 54)]),
    ('Jón', 'Macula_heber_Jonas.tsv', 'JON', [(2, 1), (2, 11)]),
]


def strong(s):
    m = re.match(r'^H0*(\d+)', s.strip())
    return ('H' + m.group(1)) if m and int(m.group(1)) < 9000 else None


def tahot(konyv, kell):
    d = {}
    with open(os.path.join(K, 'TAHOT_kivonat.tsv'), encoding='utf-8') as f:
        for s in f:
            p = s.rstrip('\n').split('\t')
            m = re.match(r'^(.+) (\d+):(\d+)$', p[0])
            if m and m.group(1) == konyv and (int(m.group(2)), int(m.group(3))) in kell and len(p) > 1:
                x = strong(p[1])
                if x:
                    d.setdefault((int(m.group(2)), int(m.group(3))), set()).add(x)
    return d


def macula(fajl, kod, fejezetek):
    d = {}
    path = os.path.join(K, fajl)
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        fej = None
        for s in f:
            if s.startswith('#'):
                continue
            p = s.rstrip('\n').split('\t')
            if fej is None:
                fej = p
                ir, ist = fej.index('ref'), fej.index('strong')
                continue
            m = re.match(r'^(\w+) (\d+):(\d+)!', p[ir])
            if m and m.group(1) == kod and int(m.group(2)) in fejezetek:
                x = strong(p[ist])
                if x:
                    d.setdefault((int(m.group(2)), int(m.group(3))), set()).add(x)
    return d


for konyv, fajl, kod, versek in PROBA:
    t = tahot(konyv, set(versek))
    mc = macula(fajl, kod, {c for c, _ in versek} | {c - 1 for c, _ in versek} | {c + 1 for c, _ in versek})
    if mc is None:
        print(konyv, 'nincs Macula-fájl:', fajl)
        continue
    for c, v in versek:
        ks = t.get((c, v), set())
        jel = sorted(((len(ks & ms) / len(ks | ms)) if (ks | ms) else 0, '%d:%d' % mv) for mv, ms in mc.items())
        jel.reverse()
        print('%s %d:%d → MT legjobb: %s' % (konyv, c, v, ', '.join('%s (%.2f)' % (b, a) for a, b in jel[:3])))
