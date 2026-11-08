# -*- coding: utf-8 -*-
"""F123 HAMART-001: az „itzávón” átírás → „iccávón” (H6093) a HAMART-001 élő forrásaiban.
    python naplok/F123_HAMART3_iccavon.py [--ir]
A kiejtés-kivételtábla (adat/kiejtes_kivetelek.tsv) már „iccávón”-t ír elő, a generátor szótári blokkjai
ezt adják; a kézi szövegek őrizték a régi alakot. Csak a betűsor cserélődik. A nyilt_angol.tsv-ben a magyar
forrásszöveg és az angol fordítás ugyanazt a héber átírást hordozza: mindkettőben csere, a forras_hash
újraszámolva (a fordítás tartalma nem változik, újrafordítás nem kell).
Írás előtt soronként összevet: csak a cserét tartalmazó sorok változhatnak, a sorszám nem."""
import hashlib
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REGI, UJ = 'itzávón', 'iccávón'
FAJLOK = ['adat/elofordulasok.tsv', 'adat/jeloltek.tsv', 'adat/motivumok.tsv', 'motivumok/HAMART-001.md']
ANGOL = 'adat/nyilt_angol.tsv'


def csere(t):
    return t.replace(REGI, UJ).replace(REGI.capitalize(), UJ.capitalize())


def hash16(t):
    return hashlib.sha256((t or '').encode('utf-8')).hexdigest()[:16]


def ellenoriz(regi, uj, ut):
    assert len(regi) == len(uj), ut
    n = 0
    for a, b in zip(regi, uj):
        if a != b:
            assert REGI in a.lower(), (ut, a[:80])
            n += 1
    assert not any(REGI in s.lower() for s in uj), ut
    return n


def main(irj):
    for ut in FAJLOK:
        s = open(ut, encoding='utf-8', newline='').read().split('\n')
        u = [csere(l) for l in s]
        print('%s: %d sor' % (ut, ellenoriz(s, u, ut)))
        if irj:
            open(ut, 'w', encoding='utf-8', newline='').write('\n'.join(u))
    s = open(ANGOL, encoding='utf-8', newline='').read().split('\n')
    fej = next(l for l in s if l.startswith('tabla\t')).split('\t')
    ix = {k: i for i, k in enumerate(fej)}
    u = []
    for l in s:
        c = l.split('\t')
        if REGI in l.lower() and len(c) == len(fej):
            assert c[ix['forras_hash']] == hash16(c[ix['forras_hu']]), c[2]
            c[ix['forras_hu']] = csere(c[ix['forras_hu']])
            c[ix['angol']] = csere(c[ix['angol']])
            c[ix['forras_hash']] = hash16(c[ix['forras_hu']])
            l = '\t'.join(c)
        u.append(l)
    print('%s: %d sor' % (ANGOL, ellenoriz(s, u, ANGOL)))
    if irj:
        open(ANGOL, 'w', encoding='utf-8', newline='').write('\n'.join(u))


if __name__ == '__main__':
    main('--ir' in sys.argv)
