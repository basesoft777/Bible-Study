"""F239 U3 — a TEREMT-001 elutasítási okainak cellakezdő alakja az olvasói névtáblában (adat/olvasoi_nevtabla.tsv,
`ok_cella`, és a megjegyzésé: `ok_leiras_cella`; az új generátor B65 bemenete). Az ok kulcsa a címke „(összesítő sor)” jelölő nélkül; az olvasói név a
címke nagy kezdőbetűvel (a meglévő sorok mintája). Csak a TEREMT-001 elutasított sorainak ténylegesen illesztett
okai (a mintaszótár `sorrend` szerinti első egyezése), és csak a hiányzó sor; a meglévőt nem érinti.
Futtatás a repó gyökeréből: python naplok/F239_U3_nevtabla.py [--ir]"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
MOT = 'TEREMT-001'
EREDET_LEIRAS = ('az elutasítási ok megjegyzése (adat/elutasitasi_okok.tsv) cellakezdő alakban, a 3. szakasz okainak '
                 'táblájában (S9a; a régi lap a cella elején nagybetűsített)')
EREDET = ('az elutasítási ok címkéje (adat/elutasitasi_okok.tsv) cellakezdő alakban, a Minősítés és a 3. szakasz '
          'táblájának „Indok” cellájában; a lapon így áll (a régi lap nagybetűsítése); DT869: a cella értéke az adatban '
          'a végleges alak')
JELOLO = re.compile(r'\s*\(összesítő sor\)\s*$')


def sorok(ut):
    nyers = open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    return nyers, nl, nyers.split(nl)


def tabla(ut):
    fej, ki = None, []
    for s in sorok(ut)[2]:
        if not s or s.startswith('#'):
            continue
        m = s.split('\t')
        if fej is None:
            fej = m
            continue
        ki.append(dict(zip(fej, m + [''] * (len(fej) - len(m)))))
    return ki


def main(ir):
    mintak = sorted((r for r in tabla('adat/elutasitasi_okok.tsv') if r['id'] in (MOT, '*')),
                    key=lambda r: int(r['sorrend']))
    kulcsok, leiras = [], {}
    for j in tabla('adat/jeloltek.tsv'):
        if j['id'] != MOT or j['jelolt_tipus'] != 'elofordulas' or j['dontes'] != 'elutasítva':
            continue
        for r in mintak:
            if re.search(r['minta'], j['indoklas'], re.IGNORECASE):
                k = JELOLO.sub('', r['cimke'])
                print('  %s → %s' % (j['igehely'], k))
                if k not in kulcsok:
                    kulcsok.append(k)
                if k not in leiras and r['megjegyzes'].strip():
                    leiras[k] = r['megjegyzes'].strip()
                break
        else:
            sys.exit('HIBA: be nem sorolt indoklás: %s' % j['igehely'])
    ut = 'adat/olvasoi_nevtabla.tsv'
    _, nl, nt = sorok(ut)
    meglevo = {tuple(s.split('\t')[:2]) for s in nt if s and not s.startswith('#') and '\t' in s}
    uj = ['\t'.join(['ok_cella', k, k[0].upper() + k[1:], EREDET]) for k in kulcsok if ('ok_cella', k) not in meglevo]
    uj += ['\t'.join(['ok_leiras_cella', k, leiras[k][0].upper() + leiras[k][1:], EREDET_LEIRAS]) for k in kulcsok
           if k in leiras and ('ok_leiras_cella', k) not in meglevo]
    for u in uj:
        print('  +', u.split('\t')[2])
    while nt and nt[-1] == '':
        nt.pop()
    if ir and uj:
        open(ut, 'w', encoding='utf-8', newline='').write(nl.join(nt + uj + ['']))
    print('%s: +%d sor %s' % (ut, len(uj), 'ÍRVA' if ir else '(próba)'))


if __name__ == '__main__':
    main('--ir' in sys.argv)
