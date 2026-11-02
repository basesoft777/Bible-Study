"""F12.1 (DT-F12a (1), DT-F12f (1)): a TEREMT-002 három előfordulás-sorának szótári mezői és a két funkció-kapcsoló.

Négy tábla, írás előtti és utáni sorösszevetéssel (minta: naplok/F148_alvil_kitoltes.py, eszkozok/igazolas_migracio.py):
  - adat/elofordulasok.tsv: a 3 TEREMT-002-sor öt szótári mezője (`lexikon_szotar` = BDB, `lexikon_entry_id` = H8414,
    `jelentes_szam` = 1, `jelentes_en`, `jelentes_hu`) és a `proveniencia` `forras`-a („+ naplok/F12_kitoltes.tsv”);
    a `jelentes_en` a BDB H8414 -/1/- szakaszának (adat/bdb_szakaszok.tsv) definíciós feje, a `jelentes_hu`
    az adat/bdb_szakasz_hu.tsv azonos szakaszáé, mindkettő bájtra (DT272 (d): a szóról szól);
  - adat/lexikon_hivatkozasok.tsv: 2 új sor a végére: (H8414, BDB, H8414, 1) a -/1/- szakaszszöveggel, és
    (H0922, BDB, H0922, tagolatlan) a `fej` szakaszszöveggel (DT438: a tagolatlan Strong nem entry, a gerincen a `fej`);
  - adat/funkcio_kapcsolok.tsv: a `SZOTARI_GERINC TEREMT-002 kivetel` sor `aktiv` (DT437 sora szerint a #12 állítja),
    és új `KAROLI_MEGFELELOK TEREMT-002 aktiv` sor a TEREMT-002-sorok után.
A soronkénti gépi proveniencia: naplok/F12_kitoltes.tsv. Előfeltétel-ellenőrzés: a versen pontosan egy H8414- és
egy H0922-token (TAHOT), a H8414 BDB-példája pontosan egy út (-/1), a H0922-é `tagolatlan`; különben nincs írás.

    python naplok/F12_kitoltes.py            # száraz futás
    python naplok/F12_kitoltes.py --ir
"""
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import lexikon_general as LG  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

TS = '2026-11-02'
ID = 'TEREMT-002'
ELO = os.path.join(GYOKER, 'adat', 'elofordulasok.tsv')
LEX = os.path.join(GYOKER, 'adat', 'lexikon_hivatkozasok.tsv')
KAP = os.path.join(GYOKER, 'adat', 'funkcio_kapcsolok.tsv')
BDB_SZ = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')
BDB_HU = os.path.join(GYOKER, 'adat', 'bdb_szakasz_hu.tsv')
NAPLO_REL = 'naplok/F12_kitoltes.tsv'
NAPLO = os.path.join(GYOKER, NAPLO_REL)
MEZOK = ('lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam', 'jelentes_en', 'jelentes_hu')
FORRASFAJL = 'konkordancia/BDB_teljes_unabridged.tsv'

# A -/1/- szakasz definíciós feje a két nyelven (az ISTENTISZT-001 mintája: a jelentés minden során azonos, a versre
# szabott leírás a gerincen áll). A szakaszszövegnek ezzel kell kezdődnie (a magyarnak a jelölő után), különben megállás.
FEJ_EN, FEJ_HU = 'formlessness', 'formátlanság'
RESZLET = {v: (FEJ_EN, FEJ_HU) for v in ('1Móz 1:2', 'Jer 4:23', 'Ézs 34:11')}


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


def tabla(ut):
    sorok = olvas(ut)
    fej = next(s for s in sorok if not s.startswith('#')).split('\t')
    return fej, [dict(zip(fej, s.split('\t'))) for s in sorok if not s.startswith('#') and s.split('\t') != fej]


def szakasz(ut, strong, utvonal, mezo):
    _, t = tabla(ut)
    talalt = [r for r in t if r['strong'] == strong and r['utvonal'] == utvonal]
    if len(talalt) != 1:
        raise SystemExit('megállás: %s %s %s: %d sor' % (ut, strong, utvonal, len(talalt)))
    return talalt[0][mezo]


def main():
    iras = '--ir' in sys.argv
    adat = LG.gerinc_adat()
    en_1 = szakasz(BDB_SZ, 'H8414', '-/1/-', 'szoveg')
    hu_1 = szakasz(BDB_HU, 'H8414', '-/1/-', 'szoveg_hu')
    en_fej_0922 = szakasz(BDB_SZ, 'H0922', 'fej', 'szoveg')

    # 1. elofordulasok.tsv
    sorok = olvas(ELO)
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fej = sorok[fej_i].split('\t')
    ix = {k: i for i, k in enumerate(fej)}
    uj = list(sorok)
    naplo, gond = [], []
    for i in range(fej_i + 1, len(sorok)):
        m = sorok[i].split('\t')
        if m[ix['id']] != ID:
            continue
        vers = m[ix['igehely']]
        if m[ix['strong']] != 'H8414+H0922' or any(m[ix[k]] for k in MEZOK) or vers not in RESZLET:
            gond.append((vers, 'strong/mező/vers'))
            continue
        utak = sorted({LG.gerinc_utvonal_vag(p['utvonal']) for p in LG.bdb_peldak(adat, 'H8414', vers)})
        utak_0922 = sorted({p['utvonal'] for p in LG.bdb_peldak(adat, 'H0922', vers)})
        tok = [(adat.get('token_szam') or {}).get((vers, s), 0) for s in ('H8414', 'H0922')]
        if utak != ['-/1'] or utak_0922 != ['tagolatlan'] or tok != [1, 1]:
            gond.append((vers, utak, utak_0922, tok))
            continue
        r_en, r_hu = RESZLET[vers]
        if not en_1.startswith(FEJ_EN + ',') or not hu_1.startswith('1 ' + FEJ_HU + ','):
            gond.append((vers, 'a részlet nincs a szakaszszövegben'))
            continue
        for k, v in zip(MEZOK, ('BDB', 'H8414', '1', r_en, r_hu)):
            m[ix[k]] = v
        prov = m[ix['proveniencia']]
        if ' | ts=' not in prov or NAPLO_REL in prov:
            gond.append((vers, 'proveniencia', prov))
            continue
        eleje, vege = prov.rsplit(' | ts=', 1)
        m[ix['proveniencia']] = '%s + %s | ts=%s' % (eleje, NAPLO_REL, vege)
        uj[i] = '\t'.join(m)
        naplo.append([ID, vers, 'BDB', 'H8414', '1', '-/1/-', 'H0922=tagolatlan', r_en, r_hu,
                      'scope=H8414+H0922 %s (adat/bdb_vers_jelentes.tsv: H8414 -/1, H0922 tagolatlan; TAHOT 1+1 token) | '
                      'forras=adat/bdb_szakaszok.tsv + adat/bdb_szakasz_hu.tsv (H8414 -/1/-, részlet bájtra) | ts=%s'
                      % (vers, TS)])
    if gond:
        raise SystemExit('⛔ nem egyértelmű sor(ok), nincs írás: %s' % gond)
    if len(naplo) != 3:
        raise SystemExit('megállás: %d sor (várt: 3)' % len(naplo))
    for i, (a, b) in enumerate(zip(sorok, uj)):
        if a == b:
            continue
        ma, mb = a.split('\t'), b.split('\t')
        elter = {fej[j] for j in range(len(ma)) if ma[j] != mb[j]}
        if len(ma) != len(mb) or not elter <= set(MEZOK) | {'proveniencia'} or ma[ix['id']] != ID:
            raise SystemExit('megállás: a %d. sorban más is változott volna: %s' % (i, elter))
    print('elofordulasok.tsv: %d sor változik' % sum(1 for a, b in zip(sorok, uj) if a != b))

    # 2. lexikon_hivatkozasok.tsv
    lsorok = olvas(LEX)
    lfej = next(s for s in lsorok if not s.startswith('#')).split('\t')
    if lfej != ['strong', 'szotar', 'entry_id', 'jelentes_szam', 'szoveg_en', 'forrasfajl']:
        raise SystemExit('megállás: a lexikon_hivatkozasok.tsv fejléce eltér')
    meglevo = {tuple(s.split('\t')[:4]) for s in lsorok}
    uj_lex = []
    for st, js, szov in (('H8414', '1', en_1), ('H0922', 'tagolatlan', en_fej_0922)):
        if (st, 'BDB', st, js) in meglevo:
            raise SystemExit('megállás: már létezik: %s %s' % (st, js))
        uj_lex.append('\t'.join([st, 'BDB', st, js, szov, FORRASFAJL]))
    lex_uj = lsorok + uj_lex
    print('lexikon_hivatkozasok.tsv: +%d sor (H8414 1, H0922 tagolatlan)' % len(uj_lex))

    # 3. funkcio_kapcsolok.tsv
    ksorok = olvas(KAP)
    k_uj = list(ksorok)
    gerinc = [i for i, s in enumerate(ksorok) if s.startswith('SZOTARI_GERINC\t%s\t' % ID)]
    if len(gerinc) != 1:
        raise SystemExit('megállás: a SZOTARI_GERINC TEREMT-002 sor nem egy')
    m = ksorok[gerinc[0]].split('\t')
    if m[2] != 'kivetel':
        raise SystemExit('megállás: a SZOTARI_GERINC TEREMT-002 állapota nem kivetel: %s' % m[2])
    m[2] = 'aktiv'
    m[4] = 'a szótári gerinc a motívumon kész: a #12 adatcommitja (F12.1) kitöltötte a szótári mezőket (DT-F12f)'
    m[5] = 'scope=manual | forras=DT437 + DT-F12f (az orkesztrátor döntése a felhasználó 2026-11-02-i felhatalmazásával) | ts=%s' % TS
    k_uj[gerinc[0]] = '\t'.join(m)
    if any(s.startswith('KAROLI_MEGFELELOK\t%s\t' % ID) for s in ksorok):
        raise SystemExit('megállás: a KAROLI_MEGFELELOK TEREMT-002 sor már létezik')
    k_uj.insert(gerinc[0] + 1, '\t'.join([
        'KAROLI_MEGFELELOK', ID, 'aktiv', '',
        'a 13–14. szerep (Károli-megfelelők, rejtett / hamis párhuzam) a motívumon: az arany lap mércéje (DT-F12f)',
        'scope=manual | forras=DT-F12f (az orkesztrátor döntése a felhasználó 2026-11-02-i felhatalmazásával) | ts=%s' % TS]))
    if [s for i, s in enumerate(k_uj) if i != gerinc[0] and i != gerinc[0] + 1] != \
            [s for i, s in enumerate(ksorok) if i != gerinc[0]]:
        raise SystemExit('megállás: a funkcio_kapcsolok.tsv más sora is változna')
    print('funkcio_kapcsolok.tsv: SZOTARI_GERINC kivetel→aktiv, +1 KAROLI_MEGFELELOK sor')

    if not iras:
        print('száraz futás: nincs írás (--ir)')
        return
    ir(ELO, uj)
    ir(LEX, lex_uj)
    ir(KAP, k_uj)
    with open(NAPLO, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# F12.1: a TEREMT-002 három sorának szótári mezői (naplok/F12_kitoltes.py); DT-F12a (1), az orkesztrátor '
                'döntése a felhasználó 2026-11-02-i felhatalmazásával\n')
        f.write('\t'.join(['id', 'igehely', 'lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam', 'bdb_utvonal',
                           'tarsszo', 'jelentes_en', 'jelentes_hu', 'proveniencia']) + '\n')
        for r in naplo:
            f.write('\t'.join(r) + '\n')
    print('napló: %s (%d sor)' % (NAPLO_REL, len(naplo)))


if __name__ == '__main__':
    main()
