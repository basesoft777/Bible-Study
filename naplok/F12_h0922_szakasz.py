"""F12.7c: a BDB H0922 `tagolatlan` sor fordítása (E19) — új fordítás nélkül, a meglévő Opus-teljesfordításból.

A H0922 szócikke tagolatlan (DT438): a `lexikon_hivatkozasok.tsv` (H0922, BDB, H0922, tagolatlan) sora a `fej` szakasz
szövege. A magyar a `adat/bdb_szakasz_hu.tsv` H0922 `fej` sora: ez a `forditasok.tsv` (BDB, H0922, H922, teljes) sorának
(opus, claude-opus-5-5, 2026.10.01) horgony szerint kivágott része, a „H922. bohu ” címsor-előtaggal, amely az angol
`fej` szövegben nincs (az a `cim` sor); az előtag nélkül kerül át. A forras_hash a lexikon_hivatkozasok `szoveg_en`-jének
SHA-1-e (13. szabály). Kapuk: forditas_kapuk.kapuk_futtat('BDB', …); SÉRTÉS esetén megállás.

    python naplok/F12_h0922_szakasz.py        # száraz futás
    python naplok/F12_h0922_szakasz.py --ir
"""
import hashlib
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
from forditas_kapuk import kapuk_futtat  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

FORD = os.path.join(GYOKER, 'adat', 'forditasok.tsv')
LEX = os.path.join(GYOKER, 'adat', 'lexikon_hivatkozasok.tsv')
HU = os.path.join(GYOKER, 'adat', 'bdb_szakasz_hu.tsv')
ELOTAG = 'H922. bohu '


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read()
    if '\r\n' in nyers or not nyers.endswith('\n'):
        raise SystemExit('megállás: váratlan sorvég: %s' % ut)
    return nyers[:-1].split('\n')


def tabla(ut):
    s = olvas(ut)
    fej = next(x for x in s if not x.startswith('#')).split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s if not x.startswith('#') and x.split('\t') != fej]


def main():
    en = [r for r in tabla(LEX) if (r['strong'], r['szotar'], r['entry_id'], r['jelentes_szam']) == ('H0922', 'BDB', 'H0922', 'tagolatlan')]
    hu = [r for r in tabla(HU) if r['strong'] == 'H0922' and r['utvonal'] == 'fej']
    if len(en) != 1 or len(hu) != 1:
        raise SystemExit('megállás: forrás- vagy magyar sor nem egy (%d, %d)' % (len(en), len(hu)))
    szoveg_hu = hu[0]['szoveg_hu']
    if not szoveg_hu.startswith(ELOTAG):
        raise SystemExit('megállás: a magyar fej nem a várt előtaggal kezdődik')
    szoveg_hu = szoveg_hu[len(ELOTAG):]
    forras = en[0]['szoveg_en']
    teljes = [r for r in tabla(FORD) if (r['szotar'], r['strong'], r['jelentes_szam'], r['mezo']) == ('BDB', 'H0922', 'teljes', 'forditas_hu')]
    if len(teljes) != 1 or szoveg_hu not in teljes[0]['forditas_hu']:
        raise SystemExit('megállás: a magyar fej nem része a H0922 teljes fordításának')
    eredm = kapuk_futtat('BDB', forras, szoveg_hu, bizonytalan=[], strong='H0922')
    for nev, all_, megj in eredm:
        print('  %-22s %s %s' % (nev, all_, megj[:80]))
    if any(e[1] == 'SERTES' for e in eredm):
        raise SystemExit('megállás: kapu-sértés')
    sor = ['BDB', 'H0922', 'H0922', 'tagolatlan', 'forditas_hu', hashlib.sha1(forras.encode('utf-8')).hexdigest(), szoveg_hu,
           teljes[0]['allapot'], teljes[0]['modell'], teljes[0]['datum'], teljes[0]['terminologia_verzio'],
           'F12.7c (E19, DT438): a H0922 teljes fordításának (BDB H922 teljes, opus) fej-szakasza a bdb_szakasz_hu.tsv-ből, '
           'a „H922. bohu” címsor-előtag nélkül; új fordítás nincs; kapuk átmentek | scope=BDB H0922 fej | '
           'forras=adat/bdb_szakasz_hu.tsv+adat/lexikon_hivatkozasok.tsv | ts=2026-11-02']
    sorok = olvas(FORD)
    if any(tuple(x.split('\t')[:5]) == tuple(sor[:5]) for x in sorok):
        raise SystemExit('megállás: a sor már létezik')
    print('új sor: %s' % ' | '.join(sor[:5] + [sor[6][:60] + '…']))
    if '--ir' not in sys.argv:
        print('száraz futás: nincs írás (--ir)')
        return
    uj = sorok + ['\t'.join(sor)]
    with open(FORD, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(uj) + '\n')
    if olvas(FORD) != uj:
        raise SystemExit('megállás: a visszaolvasott forditasok.tsv eltér')
    print('írva')


if __name__ == '__main__':
    main()
