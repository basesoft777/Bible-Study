"""F146.1 (brief 2.1, független ellenőrzés): a Jóel Károli 2:28–3:21 ↔ MT 3:1–4:21 megfeleltetés KJV-tanúja.

A KJV_Strongs_teljes.tsv (KJV-számozás, a Károli Jóel-számozása azonos vele) versenkénti Strong-halmaza vs a Macula
`ref` MT-versének Strong-halmaza (Jaccard): a mért MT-vers (Károli c:v → MT c+1:v-27 / c+1:v) és az azonos számú MT-vers.
Csak olvas; stdout. Futtatás: python naplok/F146_joel_kjv_tanu.py
"""
import os
import re
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'naplok'))
import F117_mt_levezet as L  # noqa: E402
import F146_mt_felmeres as F  # noqa: E402


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    kjv = {}
    for p in L.sorok(os.path.join(F.K, 'KJV_Strongs_teljes.tsv')):
        m = re.match(r'^Jol\.(\d+)\.(\d+)$', p[0])
        if m:
            for x in re.findall(r'H\d+', '\t'.join(p[1:])):
                s = L.strong(x)
                if s:
                    kjv.setdefault((int(m.group(1)), int(m.group(2))), set()).add(s)
    mc = F.macula('Macula_heber_Joel.tsv')
    jo = 0
    sorok = [(2, v) for v in range(28, 33)] + [(3, v) for v in range(1, 22)]
    for c, v in sorok:
        mt = (3, v - 27) if c == 2 else (4, v)
        k = kjv.get((c, v), set())
        a = mc[mt][0]
        b = mc.get((c, v), [set(), 0])[0]
        ja = len(k & a) / len(k | a) if k | a else 0
        jb = len(k & b) / len(k | b) if k | b else 0
        jo += ja > jb
        print('KJV/Károli Jóel %d:%d | MT %d:%d J=%.2f | azonos számú MT %d:%d J=%.2f' % (c, v, mt[0], mt[1], ja, c, v, jb))
    print('a mért MT-vers erősebb: %d/%d' % (jo, len(sorok)))
    print('proveniencia: scope=Jóel 2:28–3:21 (26 vers) | forras=KJV_Strongs_teljes.tsv+Macula_heber_Joel.tsv(ref) '
          '| eszkoz=naplok/F146_joel_kjv_tanu.py | ts=%s' % ts)


if __name__ == '__main__':
    main()
