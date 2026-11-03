#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F123_ANTROP2_osztaly.py — az ANTROP-001 teljesség-mérésének (naplok/F123_teljesseg_ANTROP-001.tsv)
ELTÉRÉS-sorai lexémánként osztályozva, és a TR/kritikai szövegállás az újszövetségi E- és J-helyeken.

Csak olvas; két munkafájlt ír:
  naplok/F123_teljesseg_ANTROP-001_blokkok.tsv — versenként: háló(k), osztály, a versben álló Strongok
  naplok/F123_ANTROP2_tr_kritikai.tsv          — az ÚSZ E/J-helyek pneuma/pszükhé-szavainak szövegállása

Az osztály a vers Strongjaiból gépi (a sorrend az első egyező osztályt adja); döntés nem.
TSV-olvasás split('\\t') (CLAUDE.md). Futtatás: python naplok/F123_ANTROP2_osztaly.py
"""
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import lekerdez as L  # noqa: E402
import teljesseg_meres as T  # noqa: E402

GOROG = {'G4151', 'G4152', 'G5590', 'G5591'}
OSZTALYOK = [
    ('heber_par', 'a héber pár (nefes + chajjá) egy versben, a görög pár nélkül — a DT503 blokkja'),
    ('ruah_nefes', 'rúah (H7307) és nefes (H5315) egy versben — héber szópár, a negatív kritérium a görög szópárt kéri'),
    ('csak_pneuma', 'csak a πνεῦμα (G4151) áll a versben, a ψυχή nem'),
    ('csak_pszukhe', 'csak a ψυχή (G5590) áll a versben, a πνεῦμα nem'),
    ('csak_pneumatikosz', 'csak a πνευματικός (G4152) áll a versben, a ψυχή/ψυχικός nem'),
    ('csak_pszukhikosz', 'csak a ψυχικός (G5591) áll a versben, a πνεῦμα/πνευματικός nem'),
    ('nefes', 'csak a nefes (H5315) áll a versben (ÓSZ)'),
    ('ruah', 'csak a rúah (H7307) áll a versben (ÓSZ)'),
    ('chajja', 'csak a chaj/chajjá (H2416) áll a versben (ÓSZ)'),
    ('mas_heber', 'a Károli-szó más héber szót fordít (pl. nesámá, lév), a motívum szava nincs a versben'),
    ('mas_gorog', 'a Károli-szó más görög szót fordít, a motívum szava nincs a versben'),
]


def osztaly(vers, jelen, usz):
    if {'H5315', 'H2416'} <= jelen:
        return 'heber_par'
    if {'H7307', 'H5315'} <= jelen:
        return 'ruah_nefes'
    g = jelen & GOROG
    if g:
        if g == {'G4151'}:
            return 'csak_pneuma'
        if g == {'G5590'}:
            return 'csak_pszukhe'
        if g <= {'G4152'}:
            return 'csak_pneumatikosz'
        if g <= {'G5591'}:
            return 'csak_pszukhikosz'
        return 'csak_pneuma' if 'G4151' in g else 'csak_pszukhe'
    if 'H5315' in jelen:
        return 'nefes'
    if 'H7307' in jelen:
        return 'ruah'
    if 'H2416' in jelen:
        return 'chajja'
    return 'mas_gorog' if usz else 'mas_heber'


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    tahot, tagnt = L.load_tahot(), L.load_tagnt()
    usz_versek = {r['Igehely'] for r in tagnt}
    vs = T.vers_strongjai(GOROG | {'H5315', 'H2416', 'H7307'}, tahot, tagnt)
    sorok = T.olvas(os.path.join(GYOKER, 'naplok', 'F123_teljesseg_ANTROP-001.tsv'))
    elteres = defaultdict(set)
    for r in sorok:
        if r['allapot'] == 'ELTÉRÉS':
            elteres[r['igehely']].add(r['halo'])
    ki = []
    db = Counter()
    for vers in sorted(elteres, key=T.kulcs):
        jelen = vs.get(vers, set())
        o = osztaly(vers, jelen, vers in usz_versek)
        db[o] += 1
        ki.append((vers, '+'.join(sorted(elteres[vers])), o, ', '.join(sorted(jelen)) or '—'))
    prov = ('scope=naplok/F123_teljesseg_ANTROP-001.tsv ELTÉRÉS-sorai × TAHOT/TAGNT (G4151, G4152, G5590, G5591, '
            'H5315, H2416, H7307) | forras=naplok/F123_ANTROP2_osztaly.py, split(\'\\t\') | n=%d | ts=%s' % (len(ki), ts))
    with open(os.path.join(GYOKER, 'naplok', 'F123_teljesseg_ANTROP-001_blokkok.tsv'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/F123_ANTROP2_osztaly.py — az ELTÉRÉS-versek lexémánkénti osztálya (gépi, döntés nélkül)\n')
        f.write('# ' + prov + '\n')
        f.write('igehely\thalok\tosztaly\ta_versben\n')
        for s in ki:
            f.write('\t'.join(s) + '\n')
    print('ELTÉRÉS-vers összesen: %d' % len(ki))
    for o, leiras in OSZTALYOK:
        print('  %-18s %5d  %s' % (o, db[o], leiras))
    print('proveniencia: ' + prov)

    # TR / kritikai szövegállás az ÚSZ E- és J-helyeken
    e = {v for r in T.olvas(os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')) if r['id'] == 'ANTROP-001'
         for v in T.versekre(r['igehely'])}
    j = {v for r in T.olvas(os.path.join(GYOKER, 'adat', 'jeloltek.tsv')) if r['id'] == 'ANTROP-001'
         for v in T.versekre(r['igehely'])}
    tr = []
    for vers in sorted((e | j) & usz_versek, key=T.kulcs):
        for r in tagnt:
            if r['Igehely'] == vers and r['Strong-szám'] in GOROG:
                kiad = r.get('Kritikai kiadás', '')
                tagok = set(kiad.split('+'))
                allas = ('mindkettő' if {'TR', 'NA28'} <= tagok else 'csak TR' if 'TR' in tagok
                         else 'csak kritikai' if 'NA28' in tagok else 'egyik sem')
                tr.append((vers, 'E' if vers in e else 'J', r['Strong-szám'], r['Ragozott alak'], kiad, allas))
    with open(os.path.join(GYOKER, 'naplok', 'F123_ANTROP2_tr_kritikai.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/F123_ANTROP2_osztaly.py — a pneuma/pszükhé-szavak szövegállása (TAGNT „Kritikai kiadás”), ts=%s\n' % ts)
        f.write('igehely\tallapot\tstrong\talak\tkiadasok\tTR_NA28\n')
        for s in tr:
            f.write('\t'.join(s) + '\n')
    nem = [s for s in tr if s[5] != 'mindkettő']
    print('TR/NA28: %d szó, eltérés %d: %s' % (len(tr), len(nem), '; '.join('%s %s %s (%s)' % (s[0], s[2], s[3], s[5]) for s in nem)))


if __name__ == '__main__':
    main()
