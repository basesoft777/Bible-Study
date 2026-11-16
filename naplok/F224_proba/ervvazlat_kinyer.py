#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ervvazlat_kinyer.py -- F224.13: a bíráló-próba bemenete gépileg, értelmezés nélkül.

Egy javítás előtti motívumforrásból kiveszi a „Vitatott pontok” bekezdéseit szó szerint, és pontonként a lap minden
más rés-mondatát, amely ugyanazokra a versekre támaszkodik (a `proza_allitas.py` F224.4-es bekezdés-igehely
felismerésével). Így az érvvázlat-bemenet nem hordoz a végrehajtó tudásából semmit (a végrehajtó látta a lektori
listát; a vakság ezért nem az ő megfogalmazásán múlik). A bizonyítéklap a pontok verseire készül.

Használat:
    python naplok/F224_proba/ervvazlat_kinyer.py <ID> <forras.md> <elof.tsv> <jeloltek.tsv> <ki_ervvazlat.md> <ki_bizonyitek.md> [lanc]
"""
import os
import re
import sys

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ITT, '..', '..', 'eszkozok'))
import proza_allitas as P  # noqa: E402
import bizonyiteklap as B  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    mid, forras, elof, jelolt, ki_e, ki_b = sys.argv[1:7]
    lanc = sys.argv[7].split(',') if len(sys.argv) > 7 else B.lanc_motivumbol(mid, elof)
    sorok = open(forras, encoding='utf-8').read().split('\n')
    # a Vitatott pontok szakasz bekezdései (a címsortól a következő címsorig)
    kezd = next(i for i, s in enumerate(sorok) if re.match(r'#+ .*Vitatott pontok', s))
    pontok = []
    for i in range(kezd + 1, len(sorok)):
        s = sorok[i].strip()
        if s.startswith('#'):
            break
        if s.startswith('**') and not s.startswith('*Proveniencia'):
            pontok.append((i + 1, s))
    egysegek = P.res_egysegek(forras)
    adat = P.Adat()
    igeh = P.Igehelyek()
    ell = P.Ellenor(mid, adat, None, [], igeh)
    ell.egysegek = egysegek
    ki = ['# Érvvázlat — %s, a vitatott pontok (C lépés, gépi kivonat a javítás előtti forrásból)' % mid, '',
          '*Minden tétel vizsgálandó állítás, nem tény. A pontok szövege szó szerint a forrásból; alattuk a lap más '
          'mondatai, amelyek ugyanazokra a versekre támaszkodnak (gépi kiválasztás, ítélet nélkül). Igeszakasz-'
          'tanulmány blokkjai: a motívumhoz ebben az állapotban nincsenek.*', '',
          '*(proveniencia: scope=%s „Vitatott pontok” szakasza és a rés-mondatok | forras=naplok/F224_proba/'
          'ervvazlat_kinyer.py | ts=2026-11-15)*' % os.path.basename(forras), '']
    minden_vers = []
    for n, (sorszam, szoveg) in enumerate(pontok, 1):
        e = P.Egyseg('rés:ertelmezes', 'x:%d' % sorszam, szoveg)
        refek = ell._refek_lazan(szoveg)
        versek = {k for r in refek for k in adat.versek(r)}
        for r in refek:
            if r not in minden_vers:
                minden_vers.append(r)
        cim = re.match(r'\*\*([^*]+)\*\*', szoveg)
        ki += ['## %d. vitatott pont: %s' % (n, cim.group(1) if cim else '–'), '',
               '> %s' % szoveg, '', '*(forrás: %s:%d)*' % (os.path.basename(forras), sorszam), '',
               '### A lap más mondatai ugyanezekre a versekre (%s)' % ', '.join(refek), '']
        db = 0
        for x in egysegek:
            if x.hely.endswith(':%d' % sorszam):
                continue
            xv = {k for r in ell._refek_lazan(x.szoveg) for k in adat.versek(r)}
            if versek & xv:
                ki.append('- %s (%s): %s' % (x.hely, x.forras, x.szoveg))
                db += 1
        if not db:
            ki.append('- nincs')
        ki.append('')
    with open(ki_e, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki))
    with open(ki_b, 'w', encoding='utf-8', newline='\n') as f:
        f.write(B.keszit(mid, minden_vers, lanc, elof_ut=elof, jelolt_ut=jelolt))
    print('%s: %d vitatott pont, %d vers, lánc: %s' % (mid, len(pontok), len(minden_vers), ', '.join(lanc)))


if __name__ == '__main__':
    main()
