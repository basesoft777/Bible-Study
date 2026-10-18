"""F117.6: kivonat a repón kívüli próbagenerálásból (E5) és a független referencia a TSK nyers soraiból.

Használat: python naplok/F117_proba_kivonat.py <proba_lexikon_konyvtar>
  * a próbalexikon (`general.py --cel lexikon --id <ID> --kimenet <repón kívül>`) `#### <vers>` blokkjainak `- TSK:` sorai
    az ALVIL-001 Jón 2:3, a TEREMT-001 Jón 2:6 és a TEREMT-001 Zsolt 42:8 alatt;
  * referencia (a táblától független): a TSK nyers sorai a KJV-kulcson (Jón 2:2, Jón 2:5; a Zsolt 42:7 = Károli 42:8
    célja KJV Jón 2:3 = Károli Jón 2:4, naplok/F117_itelet.tsv), Votes ≥ 15 (a generátor küszöbe).
Csak olvas; TSV split('\\t').
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def blokk(path, vers):
    with open(path, encoding='utf-8') as f:
        s = f.read()
    m = re.search(r'^#### %s\s*$(.*?)(?=^#{1,4} )' % re.escape(vers), s, re.S | re.M)
    if not m:
        return None
    return [l.strip() for l in m.group(1).splitlines() if l.strip().startswith('- TSK:')]


def tsk(forras, kuszob=15):
    out = []
    with open(os.path.join(ROOT, 'konkordancia', 'TSK_kereszthivatkozasok.tsv'), encoding='utf-8') as f:
        for s in f:
            p = s.rstrip('\n').split('\t')
            if p[0] == forras and len(p) > 3 and p[3].isdigit() and int(p[3]) >= kuszob:
                out.append((p[1], int(p[3])))
    return sorted(out, key=lambda x: -x[1])


def main():
    d = sys.argv[1]
    alvil = os.path.join(d, 'ALVIL-001_TUDOMANYOS.md')
    teremt = os.path.join(d, 'TEREMT-001_TUDOMANYOS.md')
    for nev, path, vers, kjv in (('ALVIL-001', alvil, 'Jón 2:3', 'Jón 2:2'), ('TEREMT-001', teremt, 'Jón 2:6', 'Jón 2:5')):
        b = blokk(path, vers)
        ref = tsk(kjv)
        print('%s %s: próbalexikon TSK-sor: %s | referencia (KJV %s, Votes>=15): %d' % (
            nev, vers, 'nincs blokk' if b is None else len(b), kjv, len(ref)))
        for l in (b or [])[:30]:
            print('   ', l)
        print('    ref:', '; '.join('%s (%d)' % x for x in ref))
    b = blokk(teremt, 'Zsolt 42:8')
    ref = [x for x in tsk('Zsolt 42:7') if x[0].startswith('Jón ')]
    print('TEREMT-001 Zsolt 42:8: Jón-célú TSK-sor a próbában: %s | referencia (KJV Zsolt 42:7 -> %s)' % (
        [l for l in (b or []) if 'Jón' in l], ref))
    print('    a teljes Zsolt 42:8 blokk TSK-sorainak száma: %s' % (len(b) if b is not None else 'nincs blokk'))
    print('proveniencia: scope=ALVIL-001, TEREMT-001 próbalexikon (repón kívül) + TSK_kereszthivatkozasok.tsv | '
          'forras=eszkozok/general.py --cel lexikon --kimenet <repón kívül> | eszkoz=naplok/F117_proba_kivonat.py | ts=2026-10-18')


if __name__ == '__main__':
    main()
