#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F170_kodkonyv_cimke.py -- a kódkönyv (`adat/nyilt_kodkonyv.tsv`) `cimke_en` mezője (F170.2, DT-F170a). Egyszeri,
idempotens szerkesztő-segéd (a kódkönyv kézi forrás; ez a szkript a szerkesztett címkéket viszi be):

1. a fejlécbe a `leiras_en` után a `cimke_en` oszlop (a meglévő sorokba üres mező);
2. az értéksorok `cimke_en`-je a `naplok/F170_cimkek.tsv` szerkesztett címke-szótárából (magyar érték -> angol címke);
3. a zárt oszlopok (`nyilt_mag_export.ZART`) hiányzó értéksorai (a kizárás oka, a licencszűrés oka, a forrás
   megnevezése), leírással és címkével;
4. minden zárt oszlop `<oszlop>_en` párjának oszlopsora.

Írás előtt a régi sorokat összeveti az újakkal: a meglévő sor mezői a `cimke_en` beszúrásán kívül nem változnak.
Használat: python naplok/F170_kodkonyv_cimke.py
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import nyilt_mag_export as E  # noqa: E402

KK = os.path.join(GY, 'adat', 'nyilt_kodkonyv.tsv')
PROV = 'scope=manual | forras=F170 NYILT_MAG_ANGOL: a zárt értékek angol címkéje (F170.2, DT-F170a) | ts=2026-11-05'

UJ_LEIRAS = {
    'kizaras_oka': ('Kizárási ok: %s.', 'Reason for exclusion: %s.'),
    'ok': ('A licenc szerinti besorolás oka: %s.', 'Reason for the licence classification: %s.'),
    'forras_megnevezes': ('A sor forrásának megnevezése: %s.', 'Name of the source of the row: %s.'),
    'lekerdezes_tipusa': ('A lekérdezés típusa: %s.', 'Type of query: %s.'),
}


def main():
    with open(os.path.join(GY, 'naplok', 'F170_cimkek.tsv'), encoding='utf-8') as f:
        cimke = dict(s.rstrip('\n').split('\t') for s in f if s.strip())
    with open(KK, encoding='utf-8') as f:
        sorok = f.read().split('\n')
    if sorok[-1] == '':
        sorok = sorok[:-1]
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fej = sorok[fej_i].split('\t')
    if 'cimke_en' not in fej:
        hely = fej.index('leiras_en') + 1
        regi = list(sorok)
        for i in range(fej_i, len(sorok)):
            if sorok[i].startswith('#') or not sorok[i]:
                continue
            m = sorok[i].split('\t')
            m.insert(hely, 'cimke_en' if i == fej_i else '')
            sorok[i] = '\t'.join(m)
        for a, b in zip(regi, sorok):     # a régi mezők nem változhatnak
            ma, mb = a.split('\t'), b.split('\t')
            if ma != mb[:hely] + mb[hely + 1:]:
                raise SystemExit('eltérés a beszúráson kívül: %r' % a[:80])
        fej = sorok[fej_i].split('\t')
    ci = fej.index('cimke_en')
    kulcsok = set()
    hiany = []
    for i in range(fej_i + 1, len(sorok)):
        if sorok[i].startswith('#') or not sorok[i]:
            continue
        m = sorok[i].split('\t')
        kulcsok.add((m[0], m[1], m[2]))
        if m[2]:
            c = cimke.get(m[2], '')
            if not c:
                hiany.append(m[2])
            m[ci] = c
            sorok[i] = '\t'.join(m)
    # a csomag mai zárt értékei (az OSIS-szal bővített export, címke nélkül)
    E.cimkek()
    fajlok = None
    try:
        fajlok, _ = E.export('nyilt_mag')
    except SystemExit:
        pass
    if fajlok is None:      # a címkék még hiányoznak: a zárt értékeket a nyers soradatból gyűjtjük
        E._CIMKE = {}
        E.cimke_bovit_eredeti = E.cimke_bovit
        E.cimke_bovit = lambda t, f, s: (f, s)
        fajlok, _ = E.export('nyilt_mag')
        E.cimke_bovit = E.cimke_bovit_eredeti
    uj = []
    for tabla, oszlopok in sorted(E.ZART.items()):
        _, ds = E.tsv_szoveg(fajlok[tabla])
        for o in oszlopok:
            for r in sorted({r for d in ds for r in E.ertek_reszek(d.get(o, ''))}):
                if (tabla, o, r) in kulcsok:
                    continue
                c = cimke.get(r, '')
                if not c:
                    hiany.append(r)
                hu, en = UJ_LEIRAS[o]
                m = [tabla, o, r, hu % r, en % c, c, PROV]
                uj.append('\t'.join(m))
                kulcsok.add((tabla, o, r))
            if (tabla, o + '_en', '') not in kulcsok:
                m = [tabla, o + '_en', '',
                     'Az előző oszlop (%s) értékének rövid angol címkéje a kódkönyvből (szerkesztett címke, nem '
                     'gépi fordítás); a `;`-vel összetett érték részenként.' % o,
                     'Short English label of the value in the preceding column (%s), taken from the codebook (an '
                     'edited label, not a machine translation); a compound value separated by `;` is labelled part by '
                     'part.' % o, '', PROV]
                uj.append('\t'.join(m))
                kulcsok.add((tabla, o + '_en', ''))
    if hiany:
        raise SystemExit('nincs címke: %s' % sorted(set(hiany)))
    with open(KK, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(sorok + uj) + '\n')
    print('cimke_en kitöltve; új sor: %d' % len(uj))


if __name__ == '__main__':
    main()
