"""F148 (⛔ A, a felhasználó 2026-11-01: „A #148 gépileg”; „menjen a javaslatod szerint”): az ALVIL-001
59 H7585-sorának `lexikon_szotar` / `lexikon_entry_id` / `jelentes_szam` mezője a sor egyetlen BDB-példahelyéből.

Három tábla, írás előtti és utáni sorösszevetéssel (minta: eszkozok/igazolas_migracio.py):
  - adat/elofordulasok.tsv: csak az 59 sor három mezője, és a `proveniencia` `forras`-a
    („+ naplok/F148_alvil_kitoltes.tsv”, K1 (a)); minden más sor és mező bájtra változatlan;
  - adat/lexikon_hivatkozasok.tsv: 3 új sor (BDB H7585 2.b, 3.a, 3.b), a `szoveg_en` a bdb_szakaszok.tsv
    szakaszszövege bájtra (K2), a H7585-sorok közé, kulcsrendben;
  - adat/szotar_szakasz_cimke.tsv: a -/2/b, -/3/a, -/3/b meglévő kézi sorainak üres `lexikon_jelentes_szam`-ja
    (a címke nem változik; eszkozok/szakasz_cimke_levezet.py ir_tabla).
A soronkénti gépi proveniencia: naplok/F148_alvil_kitoltes.tsv.
Nem egyértelmű sornál (nem egy BDB-példaút, nem egy H7585-token, összetett Strong) semmit nem ír.

    python naplok/F148_alvil_kitoltes.py            # száraz futás
    python naplok/F148_alvil_kitoltes.py --ir
"""
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import lexikon_general as LG  # noqa: E402
import szakasz_cimke_levezet as SL  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

TS = '2026-11-01'
ID, STRONG = 'ALVIL-001', 'H7585'
ELO = os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')
LEX = os.path.join(GYOKER, 'adat', 'lexikon_hivatkozasok.tsv')
CIMKE = os.path.join(GYOKER, 'adat', 'szotar_szakasz_cimke.tsv')
BDB_SZ = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')
NAPLO_REL = 'naplok/F148_alvil_kitoltes.tsv'
NAPLO = os.path.join(GYOKER, NAPLO_REL)
MEZOK = ('lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam')


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read()
    if '\r\n' in nyers or not nyers.endswith('\n'):
        raise SystemExit('megállás: váratlan sorvég: %s' % ut)
    return nyers[:-1].split('\n')


def ir(ut, sorok):
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(sorok) + '\n')
    if olvas(ut) != sorok:
        raise SystemExit('megállás: a visszaolvasott %s eltér' % ut)


def kulcs_utbol(ut):
    return '.'.join(x for x in LG.gerinc_utvonal_vag(ut).split('/')[1:] if x != '-')


def main():
    iras = '--ir' in sys.argv
    adat = LG.gerinc_adat()

    # 1. elofordulasok.tsv
    sorok = olvas(ELO)
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fej = sorok[fej_i].split('\t')
    ix = {k: i for i, k in enumerate(fej)}
    uj = list(sorok)
    naplo, kulcsok, gond = [], {}, []
    for i in range(fej_i + 1, len(sorok)):
        m = sorok[i].split('\t')
        if m[ix['id']] != ID or any(m[ix[k]] for k in MEZOK):
            continue
        vers = m[ix['igehely']]
        pl = LG.bdb_peldak(adat, STRONG, vers)
        utak = sorted({LG.gerinc_utvonal_vag(p['utvonal']) for p in pl})
        n_tok = (adat.get('token_szam') or {}).get((vers, STRONG), 0)
        if m[ix['strong']] != STRONG or len(utak) != 1 or n_tok != 1:
            gond.append((vers, m[ix['strong']], utak, n_tok))
            continue
        kulcs = kulcs_utbol(utak[0])
        teljes_ut = next(p['utvonal'] for p in pl)
        sorszam = ','.join(sorted({p['sorszam'] for p in pl}))
        m[ix['lexikon_szotar']], m[ix['lexikon_entry_id']], m[ix['jelentes_szam']] = 'BDB', STRONG, kulcs
        prov = m[ix['proveniencia']]
        if ' | forras=' not in prov or NAPLO_REL in prov:
            gond.append((vers, 'proveniencia', prov))
            continue
        eleje, vege = prov.split(' | ts=')
        m[ix['proveniencia']] = '%s + %s | ts=%s' % (eleje, NAPLO_REL, vege)
        uj[i] = '\t'.join(m)
        kulcsok[kulcs] = kulcsok.get(kulcs, 0) + 1
        naplo.append([ID, vers, 'BDB', STRONG, kulcs, teljes_ut, sorszam,
                      'scope=%s %s (adat/bdb_vers_jelentes.tsv, sorszam %s, út %s) | forras=szakasz_cimke_levezet.py + '
                      'adat/bdb_vers_jelentes.tsv | ts=%s' % (STRONG, vers, sorszam, teljes_ut, TS)])
    if gond:
        raise SystemExit('⛔ nem egyértelmű sor(ok), nincs írás: %s' % gond)
    if len(naplo) != 59:
        raise SystemExit('megállás: %d sor (várt: 59)' % len(naplo))
    # összevetés: csak a kitöltött sorok, és bennük csak a három mező + a proveniencia
    valtozott = 0
    for i, (a, b) in enumerate(zip(sorok, uj)):
        if a == b:
            continue
        ma, mb = a.split('\t'), b.split('\t')
        elter = {fej[j] for j in range(len(ma)) if ma[j] != mb[j]}
        if len(ma) != len(mb) or not elter <= set(MEZOK) | {'proveniencia'} or ma[ix['id']] != ID:
            raise SystemExit('megállás: a %d. sorban más is változott volna: %s' % (i, elter))
        valtozott += 1
    print('elofordulasok.tsv: %d sor változik; kulcsok: %s' % (valtozott, dict(sorted(kulcsok.items()))))

    # 2. lexikon_hivatkozasok.tsv
    bdb = {}
    for s in olvas(BDB_SZ):
        m = s.split('\t')
        if m[0] == STRONG:
            bdb[m[6]] = m
    bdb_fej = next(s for s in olvas(BDB_SZ) if not s.startswith('#')).split('\t')
    bix = {k: i for i, k in enumerate(bdb_fej)}
    lsorok = olvas(LEX)
    lfej = next(s for s in lsorok if not s.startswith('#')).split('\t')
    meglevo = {tuple(s.split('\t')[:4]) for s in lsorok}
    uj_lex = []
    for kulcs, ut in (('2.b', '-/2/b'), ('3.a', '-/3/a'), ('3.b', '-/3/b')):
        k = (STRONG, 'BDB', STRONG, kulcs)
        if k in meglevo:
            raise SystemExit('megállás: már létezik: %s' % (k,))
        sor = dict(zip(lfej, [STRONG, 'BDB', STRONG, kulcs, bdb[ut][bix['szoveg']],
                              'konkordancia/BDB_teljes_unabridged.tsv']))
        uj_lex.append('\t'.join(sor[c] for c in lfej))
    utolso_2a = max(i for i, s in enumerate(lsorok) if s.startswith('%s\tBDB\t%s\t2.a\t' % (STRONG, STRONG)))
    if not lsorok[utolso_2a + 1].startswith('%s\tBDB\t%s\t4\t' % (STRONG, STRONG)):
        raise SystemExit('megállás: a H7585 2.a után nem a 4 áll')
    lex_uj = lsorok[:utolso_2a + 1] + uj_lex + lsorok[utolso_2a + 1:]
    if [s for s in lex_uj if s not in uj_lex] != lsorok:
        raise SystemExit('megállás: a lexikon_hivatkozasok.tsv eredeti sorai változnának')
    print('lexikon_hivatkozasok.tsv: +%d sor (2.b, 3.a, 3.b)' % len(uj_lex))

    # 3. szotar_szakasz_cimke.tsv: kulcspótlás
    irando = {('BDB', STRONG, ut): ('kulcs_potlas', kulcs, '')
              for kulcs, ut in (('2.b', '-/2/b'), ('3.a', '-/3/a'), ('3.b', '-/3/b'))}

    if not iras:
        print('száraz futás: nincs írás (--ir)')
        return
    ir(ELO, uj)
    ir(LEX, lex_uj)
    p, u = SL.ir_tabla(CIMKE, irando, TS)
    print('szotar_szakasz_cimke.tsv: %d kulcspótlás, %d új sor' % (p, u))
    with open(NAPLO, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# F148: az ALVIL-001 59 H7585-sorának gépi kitöltése (naplok/F148_alvil_kitoltes.py); '
                'a felhasználó 2026-11-01: „A #148 gépileg”, „menjen a javaslatod szerint”\n')
        f.write('\t'.join(['id', 'igehely', 'lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam', 'bdb_utvonal',
                           'bdb_vers_jelentes_sorszam', 'proveniencia']) + '\n')
        for r in naplo:
            f.write('\t'.join(r) + '\n')
    print('napló: %s (%d sor)' % (NAPLO_REL, len(naplo)))


if __name__ == '__main__':
    main()
