"""A DT-F131y R2 kivétellistájának (כָּל, חָכְמָה) és R7-ének (Jeruzsálem) próbája
a teljes TAHOT-on (N-F131w). A két kalibráló mintában ezek nem (vagy alig)
fordultak elő, ezért itt a TAHOT minden H3605 (כֹּל), H2451 (חָכְמָה) és H3389
(יְרוּשָׁלַםִ) tőalakját átírja a dt_f131y() szabályaival, és alakonként
kiírja a gépi kiejtést és a gyakoriságot. Csak naplót ír:
naplok/HEBER_KIEJTES_kivetel_proba.md. Adatot nem ír.
TSV: split('\\t') (CLAUDE.md).
"""

import collections
import os
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'naplok'))
import HEBER_KIEJTES_meres as m  # noqa: E402

KIMENET = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kivetel_proba.md')
CEL = {'H3605': 'כֹּל (kol)', 'H2451': 'חָכְמָה (chochmá)', 'H3389': 'Jeruzsálem (jerúsálajim)'}


def main():
    p = m.dt_f131y()
    szamlalo = {k: collections.Counter() for k in CEL}
    with open(m.TAHOT, encoding='utf-8') as f:
        next(f)
        for l in f:
            r = l.rstrip('\n').split('\t')
            if len(r) < 4 or r[1][:5] not in CEL:
                continue
            alak = unicodedata.normalize('NFC', m.tisztit(r[2]).replace(m.METEG, ''))
            makkef = r[3].strip().endswith('-')
            g = m.niqqud(alak + (m.MAKKEF if makkef else ''), p)[0].rstrip('-')
            szamlalo[r[1][:5]][(alak, r[3].strip(), g)] += 1
    L = ['# A DT-F131y kivételeinek próbája a teljes TAHOT-on (N-F131w)', '',
         '- **Proveniencia:** `scope=konkordancia/TAHOT_kivonat.tsv (H3605, H2451, H3389 tőalakjai) '
         '| forras=naplok/HEBER_KIEJTES_kivetel_proba.py | ts=2026-10-30`',
         '- A tőalak a TAHOT-sor (előtag és toldalék nélkül). A gépi kiejtés a `dt_f131y()` szabályaival készült.', '']
    for st, nev in CEL.items():
        c = szamlalo[st]
        L += [f'## {st} — {nev}: {sum(c.values())} előfordulás, {len(c)} alak', '',
              '| alak | STEP | gépi (DT-F131y) | db |', '|---|---|---|---|']
        for (alak, step, g), db in c.most_common():
            L.append(f'| {alak} | `{step}` | {g} | {db} |')
        L.append('')
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    for st in CEL:
        c = szamlalo[st]
        print(st, sum(c.values()), len(c), [(a, g, db) for (a, _, g), db in c.most_common(8)])


if __name__ == '__main__':
    main()
