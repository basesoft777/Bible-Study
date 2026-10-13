"""F94.1 (FELADATOK #94): a hibrid szótövező korpusz-lexikona a Károli 1908-ból (`konkordancia/Karoli_1908.tsv`;
nem a `pardes.db`-ből, mert az generált index, nem forrás — DT28).

Kimenet: `adat/szoto/karoli_lexikon.tsv` (generált, kézzel nem szerkeszthető; SEMA 2.27):
    alak<TAB>kisbetus<TAB>nagy_belul<TAB>nagy_kezdo
- kisbetus: kisbetűs előfordulás;
- nagy_belul: nagybetűs előfordulás mondat belsejében;
- nagy_kezdo: nagybetűs előfordulás mondatkezdő helyzetben (a vers első szava, vagy . ! ? : után).
A tokenizálás és a számlálás az előmérés `lexikon_epit.py`-jával azonos (az ott a `pardes.db` `vers.karoli_szoveg`-éből olvasott).

Használat: python eszkozok/szoto/lexikon_epit.py [--ts 2026-10-13T00:00Z] [--kimenet <fájl>]"""
import argparse
import collections
import datetime
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KAROLI = os.path.join(REPO, 'konkordancia', 'Karoli_1908.tsv')
KIMENET = os.path.join(REPO, 'adat', 'szoto', 'karoli_lexikon.tsv')
SZO = re.compile(r"[\wÁÉÍÓÖŐÚÜŰáéíóöőúüű-]+|[.!?:]")
FEJLEC = ['alak', 'kisbetus', 'nagy_belul', 'nagy_kezdo']


def szamol(versszovegek):
    kis, nagy_belul, nagy_kezdo = collections.Counter(), collections.Counter(), collections.Counter()
    for sz in versszovegek:
        kezdo = True
        for t in SZO.findall(sz or ''):
            if t in '.!?:':
                kezdo = True
                continue
            if t[:1].isdigit():
                continue
            if t[:1].isupper():
                (nagy_kezdo if kezdo else nagy_belul)[t] += 1
            else:
                kis[t] += 1
            kezdo = False
    return kis, nagy_belul, nagy_kezdo


def versek():
    for s in open(KAROLI, encoding='utf-8').read().split('\n')[1:]:
        if '\t' in s:
            yield s.split('\t', 1)[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts', default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'))
    ap.add_argument('--kimenet', default=KIMENET)
    a = ap.parse_args()
    kis, nb, nk = szamol(versek())
    alakok = sorted(set(kis) | set(nb) | set(nk))
    h = hashlib.sha256(open(KAROLI, 'rb').read()).hexdigest()
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# GENERÁLT: eszkozok/szoto/lexikon_epit.py (F94.1) — kézzel nem szerkeszthető | scope=OT+NT-full | '
                f'forras=konkordancia/Karoli_1908.tsv (sha256:{h}) | ts={a.ts}\n')
        f.write('\t'.join(FEJLEC) + '\n')
        for w in alakok:
            f.write(f'{w}\t{kis[w]}\t{nb[w]}\t{nk[w]}\n')
    print(f'alak: {len(alakok)}; token: {sum(kis.values()) + sum(nb.values()) + sum(nk.values())}')


if __name__ == '__main__':
    main()
