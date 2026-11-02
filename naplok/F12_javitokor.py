"""F12.10 (javítókör, naplok/ELLENOR_F12_TEREMT002_LEXIKON.md): két adatmező pontosítása, írás előtti és utáni
összevetéssel (csak a megnevezett mező változik).

  - adat/elofordulasok.tsv, TEREMT-002 / Ézs 34:11, `kapcsolodas`: a héber pár mellé a kiejtés („(tóhú vávóhú)”),
    mint az 1Móz 1:2 sorában (az ellenőr A6/E13 tétele);
  - adat/forditasok.tsv, UBS_DBH / H8414 / 007726001001000 / glosszak_hu, `modell`: a végső szöveg mindkét szerzője
    („claude-sonnet-5-5; claude-opus-5-5 (2. tag)”; az ellenőr 0c tétele).

    python naplok/F12_javitokor.py        # száraz futás
    python naplok/F12_javitokor.py --ir
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELO = os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')
FORD = os.path.join(GYOKER, 'adat', 'forditasok.tsv')
REGI_K, UJ_K = 'a תֹהוּ וָבֹהוּ pár Edom', 'a תֹהוּ וָבֹהוּ (tóhú vávóhú) pár Edom'


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read()
    if '\r\n' in nyers or not nyers.endswith('\n'):
        raise SystemExit('megállás: váratlan sorvég: %s' % ut)
    return nyers[:-1].split('\n')


def modosit(ut, kulcs_fv, mezo, uj_fv):
    sorok = olvas(ut)
    fej = next(s for s in sorok if not s.startswith('#')).split('\t')
    ix = fej.index(mezo)
    talalt = [i for i, s in enumerate(sorok) if not s.startswith('#') and kulcs_fv(dict(zip(fej, s.split('\t'))))]
    if len(talalt) != 1:
        raise SystemExit('megállás: %s: %d egyező sor' % (ut, len(talalt)))
    m = sorok[talalt[0]].split('\t')
    regi = m[ix]
    m[ix] = uj_fv(regi)
    if m[ix] == regi:
        raise SystemExit('megállás: %s: nincs változás' % ut)
    uj = list(sorok)
    uj[talalt[0]] = '\t'.join(m)
    if [s for i, s in enumerate(uj) if i != talalt[0]] != [s for i, s in enumerate(sorok) if i != talalt[0]]:
        raise SystemExit('megállás: más sor is változna')
    print('%s: %s\n  régi: %s\n  új:   %s' % (os.path.basename(ut), mezo, regi[:120], m[ix][:120]))
    return uj


def main():
    def k_uj(v):
        if v.count(REGI_K) != 1:
            raise SystemExit('megállás: a kapcsolodas mintája nem egyszer áll')
        return v.replace(REGI_K, UJ_K)
    e = modosit(ELO, lambda r: r['id'] == 'TEREMT-002' and r['igehely'] == 'Ézs 34:11', 'kapcsolodas', k_uj)
    f = modosit(FORD, lambda r: (r['szotar'], r['strong'], r['entry_id'], r['mezo']) ==
                ('UBS_DBH', 'H8414', '007726001001000', 'glosszak_hu'), 'modell',
                lambda v: 'claude-sonnet-5-5; claude-opus-5-5 (2. tag)' if v == 'claude-sonnet-5-5' else v)
    if '--ir' not in sys.argv:
        print('száraz futás: nincs írás (--ir)')
        return
    for ut, sorok in ((ELO, e), (FORD, f)):
        with open(ut, 'w', encoding='utf-8', newline='') as fh:
            fh.write('\n'.join(sorok) + '\n')
        if olvas(ut) != sorok:
            raise SystemExit('megállás: a visszaolvasott %s eltér' % ut)
    print('írva')


if __name__ == '__main__':
    main()
