"""F239 U3 — a TEREMT-001 adatának olvasói alakja (az olvasói kapu tételei az új generátor előnézetén); csak forma.

1. `adat/elofordulasok.tsv` `karoli_szo`: a kezdő névelő („a ”, „A ”, „az ”) nélkül — a lap 1. táblájának Kulcsszó
   oszlopa táblaelem, névelővel nem kezdődhet (olvasói kapu LISTA_NEVELO); a szó maga változatlan.
2. `adat/motivumok.tsv` `negativ_kriterium`: az egyenes idézőjel („"tenger"”) magyar idézőjelre („„tenger”") —
   a szabály szövege nem változik (DT-F239c).
3. `adat/jeloltek.tsv` Jób 41:31 indoklása: „köztük” → „például” (a kapu MI_HANG osztálya a „köztük” szót
   többes szám első személynek méri; a mondat tartalma azonos).
4. `adat/motivum_kapcsolatok.tsv` Ez 31:15 `funkcio`: a mondat nem kezdődik névelővel (LISTA_NEVELO); a tartalma
   azonos.
Írás előtt csak a megnevezett mezők változnak (összevetés). Futtatás: python naplok/F239_U3_olvasoi_alak.py [--ir]"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
MOT = 'TEREMT-001'
NEVELO = re.compile(r'^(?:a|A|az|Az) ')


def nyit(ut):
    n = open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in n else '\n'
    s = n.split(nl)
    fi = next(i for i, l in enumerate(s) if l and not l.startswith('#'))
    return s, nl, fi, {k: i for i, k in enumerate(s[fi].split('\t'))}


def main(ir):
    valt = 0
    # 1. karoli_szo
    s, nl, fi, ix = nyit('adat/elofordulasok.tsv')
    for i in range(fi + 1, len(s)):
        m = s[i].split('\t')
        if len(m) > 1 and m[0] == MOT and NEVELO.match(m[ix['karoli_szo']]):
            regi = m[ix['karoli_szo']]
            m[ix['karoli_szo']] = NEVELO.sub('', regi)
            print('  %s karoli_szo: %r → %r' % (m[1], regi, m[ix['karoli_szo']]))
            s[i] = '\t'.join(m)
            valt += 1
    if ir:
        open('adat/elofordulasok.tsv', 'w', encoding='utf-8', newline='').write(nl.join(s))
    # 2. negativ_kriterium
    s, nl, fi, ix = nyit('adat/motivumok.tsv')
    for i in range(fi + 1, len(s)):
        m = s[i].split('\t')
        if m[0] == MOT and '"tenger"' in m[ix['negativ_kriterium']]:
            m[ix['negativ_kriterium']] = m[ix['negativ_kriterium']].replace('"tenger"', '„tenger”')
            s[i] = '\t'.join(m)
            valt += 1
            print('  motivumok negativ_kriterium: idézőjel')
    if ir:
        open('adat/motivumok.tsv', 'w', encoding='utf-8', newline='').write(nl.join(s))
    # 3. jeloltek Jób 41:31
    s, nl, fi, ix = nyit('adat/jeloltek.tsv')
    for i in range(fi + 1, len(s)):
        m = s[i].split('\t')
        if len(m) > 9 and m[0] == MOT and m[1] == 'Jób 41:31' and m[ix['jelolt_tipus']] == 'elofordulas':
            if '(köztük a Jón 2:4' in m[ix['indoklas']]:
                m[ix['indoklas']] = m[ix['indoklas']].replace('(köztük a Jón 2:4', '(például a Jón 2:4')
                s[i] = '\t'.join(m)
                valt += 1
                print('  jeloltek Jób 41:31: köztük → például')
    if ir:
        open('adat/jeloltek.tsv', 'w', encoding='utf-8', newline='').write(nl.join(s))
    # 4. motivum_kapcsolatok Ez 31:15 funkcio
    REGI = ('a cédrus a seólba száll, Isten miatta gyászba borítja és visszatartja a mélységet: a holtak helye és a '
            'kozmikus víz egy versben')
    UJ = ('Isten gyászba borítja és visszatartja a mélységet, amikor a cédrus a seólba száll: a holtak helye és a '
          'kozmikus víz egy versben')
    s, nl, fi, ix = nyit('adat/motivum_kapcsolatok.tsv')
    for i in range(fi + 1, len(s)):
        m = s[i].split('\t')
        if len(m) > 7 and m[0] == 'ALVIL-001' and m[3] == MOT and m[ix['funkcio']] == REGI:
            m[ix['funkcio']] = UJ
            s[i] = '\t'.join(m)
            valt += 1
            print('  motivum_kapcsolatok Ez 31:15 funkcio')
    if ir:
        open('adat/motivum_kapcsolatok.tsv', 'w', encoding='utf-8', newline='').write(nl.join(s))
    print('%d változás; %s' % (valt, 'ÍRVA' if ir else '(próba)'))


if __name__ == '__main__':
    main('--ir' in sys.argv)
