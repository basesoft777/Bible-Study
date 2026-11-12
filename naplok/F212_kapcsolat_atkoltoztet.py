"""F212 (C6, N151, DT759): a HAMART-001 kapcsolat-jelöltjeinek átköltöztetése a kivételfájlból a jelölttáblába.

Forrás: `naplok/F182_kapcsolat_jeloltek.tsv` (103 jelölt: 56 beépítve, 47 elutasítva). Cél: `adat/jeloltek.tsv`, új
`jelolt_tipus=kapcsolat` sorok (SEMA 2.4): `igehely` = a kapcsolat forrás-igehelye, `cel_igehely` = a cél-igehely,
`cel_id` üres (a pár a motívumon belül áll), `megbizhatosag` = a jelölt bizonyossága, a mérés bizonyítékai és a
kapcsolat típusa a `dontes_ref`-ben. A `kapcsolatok.tsv` proveniencia-forrása a jelölttáblára mutat.

Írás előtt összevetés (CLAUDE.md, TSV-írás): a jelölttábla meglévő sorai bájtra változatlanok; az új sorok mezői
visszaolvasva egyeznek a forrással; a `kapcsolatok.tsv`-ben csak a forrás-hivatkozás változik. Eltérésnél megáll.
Ismételt futás: ha a sorok már bent vannak és egyeznek, nem ír.

Futtatás: python naplok/F212_kapcsolat_atkoltoztet.py [--ir]
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORRAS = os.path.join(GYOKER, 'naplok', 'F182_kapcsolat_jeloltek.tsv')
JELOLTEK = os.path.join(GYOKER, 'adat', 'jeloltek.tsv')
KAPCSOLATOK = os.path.join(GYOKER, 'adat', 'kapcsolatok.tsv')
MOTIVUM = 'HAMART-001'
DATUM = '2026.11.10'          # a kivételfájl ts-e (2026-11-10T07:05Z)
REGI_HIV = 'forras=naplok/F182_kapcsolat_jeloltek.tsv'
UJ_HIV = 'forras=adat/jeloltek.tsv (jelolt_tipus=kapcsolat)'
BIZONYITEK = (('kozos_lanc_strong', 'közös lánc-szó'), ('kozos_fordulat', 'közös fordulat'), ('lxx_hid', 'LXX-híd'),
              ('kozos_tartalmi_strong', 'közös tartalmi szó'), ('gorog_szocsalad', 'görög szócsalád'))
PROV = 'scope=adat/elofordulasok.tsv (HAMART-001) | forras=naplok/F182_kapcsolat.py | ts=2026-11-10T07:05Z'


def nyers_sorok(ut):
    with io.open(ut, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def forras_sorok():
    sorok = [s for s in nyers_sorok(FORRAS) if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def dontes_ref(r):
    reszek = ['kapcsolat-típus: %s' % r['tipus']] if r['tipus'] else []
    reszek += ['%s: %s' % (nev, r[k]) for k, nev in BIZONYITEK if r.get(k)]
    return ' · '.join(reszek + ['DT759', PROV])


def uj_sor(r, fej):
    d = {'id': MOTIVUM, 'igehely': r['forras_sor'], 'forras_kereses': r['jelolt_forras'], 'dontes': r['dontes'],
         'indoklas': r['indoklas'], 'karoli_szo': '', 'azonositas_modja': '', 'megbizhatosag': r['bizonyossag'],
         'datum': DATUM, 'jelolt_tipus': 'kapcsolat', 'cel_id': '', 'cel_igehely': r['cel_sor'], 'cel_alpont': '',
         'dontes_ref': dontes_ref(r)}
    for k, v in d.items():
        if '\t' in v or '\n' in v:
            raise SystemExit('MEGÁLLÁS: tabulátor vagy sortörés a(z) %s mezőben: %r' % (k, v[:60]))
    return '\t'.join(d[k] for k in fej)


def main():
    ir = '--ir' in sys.argv
    forras = forras_sorok()
    if len(forras) != 103 or sum(r['dontes'] == 'beépítve' for r in forras) != 56:
        raise SystemExit('MEGÁLLÁS: a forrás nem a várt 103 sor / 56 beépítve (%d)' % len(forras))

    jel = nyers_sorok(JELOLTEK)
    fej_i = next(i for i, s in enumerate(jel) if s and not s.startswith('#'))
    fej = jel[fej_i].split('\t')
    meglevo = [s for s in jel[fej_i + 1:] if s]
    mar_bent = [s for s in meglevo if s.split('\t')[fej.index('jelolt_tipus')] == 'kapcsolat']
    ujak = [uj_sor(r, fej) for r in forras]
    kulcsok = {(MOTIVUM, r['forras_sor'], 'kapcsolat', r['cel_sor']) for r in forras}
    if len(kulcsok) != len(forras):
        raise SystemExit('MEGÁLLÁS: ismétlődő kapcsolat-kulcs a forrásban')
    if mar_bent:
        if mar_bent != ujak:
            raise SystemExit('MEGÁLLÁS: a jelölttáblában már vannak kapcsolat-sorok, és eltérnek a forrástól')
        print('A 103 kapcsolat-jelölt már a jelölttáblában van, egyezik a forrással; nincs írás.')
        uj_jel = jel
    else:
        veg = jel[-1] == ''
        uj_jel = (jel[:-1] if veg else jel) + ujak + ([''] if veg else [])

    # visszaolvasás: a régi sorok bájtra azonosak, az új sorok a forrás mezőit adják vissza
    if uj_jel[:len(jel) - 1] != jel[:len(jel) - 1]:
        raise SystemExit('MEGÁLLÁS: a jelölttábla meglévő sorai változnának')
    vissza = [dict(zip(fej, s.split('\t'))) for s in uj_jel if s and not s.startswith('#')
              and s.split('\t')[fej.index('jelolt_tipus')] == 'kapcsolat']
    for r, v in zip(forras, vissza):
        if (v['igehely'], v['cel_igehely'], v['forras_kereses'], v['dontes'], v['indoklas'], v['megbizhatosag']) != \
                (r['forras_sor'], r['cel_sor'], r['jelolt_forras'], r['dontes'], r['indoklas'], r['bizonyossag']):
            raise SystemExit('MEGÁLLÁS: visszaolvasási eltérés: %s → %s' % (r['forras_sor'], r['cel_sor']))
    if len(vissza) != 103:
        raise SystemExit('MEGÁLLÁS: %d kapcsolat-sor a jelölttáblában, várt 103' % len(vissza))

    kap = nyers_sorok(KAPCSOLATOK)
    uj_kap = [s.replace(REGI_HIV, UJ_HIV) for s in kap]
    valtozott = [(a, b) for a, b in zip(kap, uj_kap) if a != b]
    for a, b in valtozott:
        if a.split('\t')[:-1] != b.split('\t')[:-1]:
            raise SystemExit('MEGÁLLÁS: a kapcsolatok.tsv-ben nem csak az indoklás mező változna')
    beepitve = {(r['forras_sor'], r['cel_sor']) for r in forras if r['dontes'] == 'beépítve'}
    hivatkozo = [s.split('\t') for s in uj_kap if UJ_HIV in s]
    hianyzo = [(c[0], c[1]) for c in hivatkozo if (c[0], c[1]) not in beepitve]
    if hianyzo:
        raise SystemExit('MEGÁLLÁS: kapcsolat-sor beépített jelölt nélkül: %s' % hianyzo[:5])
    print('jelölttábla: %d meglévő sor változatlan, %d kapcsolat-sor (%d beépítve, %d elutasítva)'
          % (len(meglevo) - len(mar_bent), len(vissza), sum(v['dontes'] == 'beépítve' for v in vissza),
             sum(v['dontes'] == 'elutasítva' for v in vissza)))
    print('kapcsolatok.tsv: %d sor forrás-hivatkozása a jelölttáblára mutat (mindegyik mögött beépített jelölt)'
          % len(valtozott or hivatkozo))
    if not ir:
        print('(próba: --ir nélkül nincs írás)')
        return
    for ut, sorok in ((JELOLTEK, uj_jel), (KAPCSOLATOK, uj_kap)):
        with io.open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(sorok))
    print('írva: adat/jeloltek.tsv, adat/kapcsolatok.tsv')


if __name__ == '__main__':
    main()
