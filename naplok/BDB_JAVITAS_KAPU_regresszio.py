#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/BDB_JAVITAS_KAPU_regresszio.py -- F67 M4: a 17_bdb_javitas kapu futtatasa az
adat/forditasok.tsv minden BDB `teljes` es `sz<n>` soran, a Strong megadasaval.
Csak olvas (adat/ es konkordancia/ valtozatlan); kimenet: naplok/BDB_JAVITAS_KAPU_naplo.md

    python naplok/BDB_JAVITAS_KAPU_regresszio.py
"""
import datetime
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import emeles as E  # noqa: E402
import forditas_kapuk as K  # noqa: E402

JELOLT = ['H5002', 'H5046', 'H4427', 'H7223']
KULON = ['H6297']
KI = os.path.join(REPO, 'naplok', 'BDB_JAVITAS_KAPU_naplo.md')


def main():
    SB = E._sb()
    tabla = K.javitas_betolt()
    sorok = [r for r in E.tsv_dict_sorok(E.FORDITASOK_UT) if r['szotar'] == 'BDB']
    szak_cache = {}
    ered = []   # (strong, jelentes_szam, eredmeny, reszlet, marker_db, forras_hossz)
    kihagyott = 0
    for r in sorok:
        jsz, sp = r['jelentes_szam'], r['strong']
        if jsz == 'teljes':
            forras = E.forras_szoveg(sp)[1]
        else:
            n = SB.sorszam_jelentesbol(jsz)
            if n is None:
                kihagyott += 1
                continue
            if sp not in szak_cache:
                szak_cache[sp] = {x['sorszam']: x['szoveg'] for x in SB.szakaszok(sp) or []}
            forras = szak_cache[sp].get(n)
            if forras is None:
                kihagyott += 1
                continue
        e, d = K.ellenoriz_bdb_javitas('BDB', forras, r['forditas_hu'], sp)
        ered.append((sp, jsz, e, d, r['forditas_hu'].count('[BDB:'), len(forras)))
    teljes = sum(1 for x in ered if x[1] == 'teljes')
    szak = len(ered) - teljes
    rendben = [x for x in ered if x[2] == 'RENDBEN']
    sertes = [x for x in ered if x[2] == 'SERTES']
    ts = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    prov = ('scope=BDB-sorok (teljes + sz<n>) adat/forditasok.tsv x adat/bdb_igehely_javitas.tsv | '
            'forras=eszkozok/forditas_kapuk.py ellenoriz_bdb_javitas (naplok/BDB_JAVITAS_KAPU_regresszio.py) | ts=%s' % ts)
    L = ['# BDB_JAVITAS_KAPU — regresszió a meglévő BDB-soron (F67 M4)', '',
         '*proveniencia: %s*' % prov, '',
         '## Összegzés', '',
         '- vizsgált sor: %d (teljes %d, szakaszsor %d); kihagyott (nem teljes/sz<n> jelentésszám vagy szakasz nélkül): %d' % (len(ered), teljes, szak, kihagyott),
         '- RENDBEN: %d · SERTES: %d' % (len(rendben), len(sertes)),
         '- nem üres `[BDB:` jelölés a sorokban: %d sor' % sum(1 for x in ered if x[4]), '']
    L += ['## Szócikkenként (a javítótáblában szereplő vagy jelölést hordozó Strongok)', '',
          '| Strong | sorok | RENDBEN | SERTES | jelölés (db) | javitva sor a táblában |', '|---|---|---|---|---|---|']
    strongok = sorted({x[0] for x in ered})
    for sp in strongok:
        xs = [x for x in ered if x[0] == sp]
        jel = sum(x[4] for x in xs)
        tj = sum(1 for t in tabla.get(sp, []) if t['allapot'] == 'javitva')
        if sp in JELOLT + KULON or jel or tj:
            L.append('| %s | %d | %d | %d | %d | %d |' % (sp, len(xs), sum(1 for x in xs if x[2] == 'RENDBEN'),
                                                      sum(1 for x in xs if x[2] == 'SERTES'), jel, tj))
    L += ['', '## A 4 már jelölt szócikk és a H6297 külön', '']
    for sp in JELOLT + KULON:
        xs = [x for x in ered if x[0] == sp]
        L.append('### %s — %d sor; RENDBEN %d, SERTES %d' % (sp, len(xs), sum(1 for x in xs if x[2] == 'RENDBEN'),
                                                       sum(1 for x in xs if x[2] == 'SERTES')))
        L.append('*proveniencia: %s*' % prov)
        for x in xs:
            if x[4] or x[2] == 'SERTES' or x[3].startswith('1 javítva') or 'javítva' in x[3]:
                L.append('- %s: %s — %s' % (x[1], x[2], x[3]))
        L.append('')
    L += ['## SERTES sorok', '']
    if sertes:
        for x in sertes:
            L.append('- %s %s: %s' % (x[0], x[1], x[3]))
    else:
        L.append('nincs.')
    with open(KI, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(L) + '\n')
    print('sorok %d (teljes %d, sz %d), kihagyott %d, RENDBEN %d, SERTES %d' % (len(ered), teljes, szak, kihagyott, len(rendben), len(sertes)))
    for sp in JELOLT + KULON:
        xs = [x for x in ered if x[0] == sp]
        print(sp, len(xs), 'sor', 'SERTES', sum(1 for x in xs if x[2] == 'SERTES'))
    for x in sertes[:30]:
        print('SERTES', x[0], x[1], x[3][:300])


main()
