"""F239 U3 — a TEREMT-001 döntésnaplójának alakja az új lapgenerátorhoz (B04, B56); csak forma, tartalom nem.

1. A csoportos elutasító sorok (a forrás „blokk-sor …: N vers”) indoklása az „Összesítő sor N versre (a sor igehelye
   a blokk egy verse áll): …” alakra (a lapgen `_OSSZESITO_ELEJE_RX`); a két egyverses blokk-sor, amelynek az oka más
   (Ézs 44:27: a Septuaginta többlete; Jób 42:8: adathiba), ugyanezt az előtagot kapja, az ok szövege változatlan.
2. A két Septuaginta-sor (Jób 36:16, Zsolt 71:21) forrás-megnevezése az elfogadott hálónévre: „teljesség-mérés,
   LXX-többlet háló” (az ALVIL-001 mintája; a lapgen `_HALOK`), a forrássor többi része változatlan.
3. A 2Pét 2:4 elutasító indoklásában az egyenes idézőjel magyar idézőjelre („…”) cserélve (a lap olvasói kapuja).
4. `adat/elutasitasi_okok.tsv` +2 TEREMT-001 sor, a meglévő okok kulcsával (a HAMART-001 98–99. sorának mintája): az
   összesítő előtagú Septuaginta- és adathiba-sor ugyanabba az okba kerül, mint eddig.

Írás előtt: csak a megnevezett mezők változnak (összevetés a régi sorokkal); a `csv` modult nem használja.
Futtatás a repó gyökeréből: python naplok/F239_U3_jelolt_alak.py [--ir]"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

MOT = 'TEREMT-001'
ELOTAG = 'Összesítő sor %d versre (a sor igehelye a blokk egy verse áll): '
OSSZ_RX = re.compile(r'^Összesítő sor (\d+) versre: ')
BLOKK_RX = re.compile(r'blokk-(?:kizárás|sor)[^:|]*:\s*(\d+) vers')
LXX_REGI = 'F239 U1 LXX-híd: '
LXX_UJ = 'F239 U1 teljesség-mérés, LXX-többlet háló: '
PROV = 'scope=manual | forras=F239 U3, a döntésnapló alakja az új generátorhoz (naplok/F239_U3_jelolt_alak.py; claude-opus-5-5) | ts=2026-11-23'


def olvas(ut):
    nyers = open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    return nyers, nl, nyers.split(nl)


def jeloltek(ir):
    ut = 'adat/jeloltek.tsv'
    nyers, nl, sorok = olvas(ut)
    fej_i = next(i for i, l in enumerate(sorok) if l and not l.startswith('#'))
    ix = {k: i for i, k in enumerate(sorok[fej_i].split('\t'))}
    valt = []
    for i in range(fej_i + 1, len(sorok)):
        if not sorok[i]:
            continue
        m = sorok[i].split('\t')
        if m[ix['id']] != MOT or m[ix['jelolt_tipus']] != 'elofordulas':
            continue
        regi = list(m)
        forras, ind = m[ix['forras_kereses']], m[ix['indoklas']]
        blokk = BLOKK_RX.search(forras.split(' | ')[0])
        if m[ix['dontes']] == 'elutasítva' and blokk:
            n = int(blokk.group(1))
            o = OSSZ_RX.match(ind)
            if o:
                if int(o.group(1)) != n:
                    sys.exit('HIBA: %s: az indoklás %s verset mond, a forrás %d-et' % (m[1], o.group(1), n))
                ind = ELOTAG % n + ind[o.end():]
            elif not ind.startswith('Összesítő sor'):
                ind = ELOTAG % n + ind[0].lower() + ind[1:]
            m[ix['indoklas']] = ind
        if m[ix['dontes']] == 'elutasítva' and '"' in ind:
            ind = re.sub(r'"([^"]*)"', lambda x: '„' + x.group(1) + '”', ind)
            m[ix['indoklas']] = ind
        if forras.startswith(LXX_REGI):
            m[ix['forras_kereses']] = LXX_UJ + forras[len(LXX_REGI):]
        if m != regi:
            for k in ix:
                if m[ix[k]] != regi[ix[k]] and k not in ('indoklas', 'forras_kereses'):
                    sys.exit('HIBA: más mező változna: %s %s' % (m[1], k))
            valt.append((m[1], [k for k in ('indoklas', 'forras_kereses') if m[ix[k]] != regi[ix[k]]]))
            sorok[i] = '\t'.join(m)
    for ih, mezok in valt:
        print('  %s: %s' % (ih, ', '.join(mezok)))
    print('%s: %d sor változik' % (ut, len(valt)))
    if ir:
        open(ut, 'w', encoding='utf-8', newline='').write(nl.join(sorok))


def okok(ir):
    ut = 'adat/elutasitasi_okok.tsv'
    nyers, nl, sorok = olvas(ut)
    uj = [
        ['99', MOT, r'^összesítő sor \d+ versre \([^)]*\): a septuaginta többlete',
         'a Septuaginta többlete, a héberben nincs tehóm (összesítő sor)',
         'a görög fordítás ἄβυσσος-t hoz, a héber versben viszont más szó áll, vagy a görög szöveg a héberen túl ismétel',
         PROV],
        ['100', MOT, r'^összesítő sor \d+ versre \([^)]*\): adathiba',
         'a szótár hivatkozása hibás, a versben a szó nem áll (összesítő sor)',
         'a szótár egy másik könyv azonos számú versét idézi; a feldolgozás a könyv nevét elhagyta, a versben a motívum '
         'szava nem áll', PROV],
    ]
    meglevo = {(s.split('\t')[0], s.split('\t')[1]) for s in sorok if s and not s.startswith('#')}
    uj = [u for u in uj if (u[0], u[1]) not in meglevo]
    while sorok and sorok[-1] == '':
        sorok.pop()
    sorok += ['\t'.join(u) for u in uj] + ['']
    print('%s: +%d sor' % (ut, len(uj)))
    if ir:
        open(ut, 'w', encoding='utf-8', newline='').write(nl.join(sorok))


if __name__ == '__main__':
    ir = '--ir' in sys.argv
    jeloltek(ir)
    okok(ir)
    print('ÍRVA' if ir else '(próba; írás: --ir)')
