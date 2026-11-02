"""F12.3: a TEREMT-002 nyolc rövid szótári egységének rögzítése az adat/forditasok.tsv-be a
naplok/F12_forditas_tervezet.tsv-ből (claude-sonnet-5-5, kapuk átmentek).

A session egy eltérése a tervezettől (indok: a nyelvközi egység, a Károli „kietlen” szava a tohu megfelelője):
  UBS_DBH H8414 007726001001000: „pusztaság; elpusztítottság; káosz” → „pusztaság; kietlenség; káosz”.
A kapuk az eltérő sorra újra lefutnak; SÉRTÉS esetén megállás.
A forras_hash a forrásszöveg SHA-1-e, a forrásszöveget a 13. szabály feloldója adja (glossza_lexikon_forditas:
tovabbi_forras / dbh_forras_idx), nem a tervezet oszlopa; eltérésnél megállás. Csak hozzáfűzés, sorösszevetéssel.

    python naplok/F12_forditas_rogzit.py        # száraz futás
    python naplok/F12_forditas_rogzit.py --ir
"""
import hashlib
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import glossza_lexikon_forditas as GLF  # noqa: E402
from forditas_kapuk import kapuk_futtat  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

TERV = os.path.join(GYOKER, 'naplok', 'F12_forditas_tervezet.tsv')
FORD = os.path.join(GYOKER, 'adat', 'forditasok.tsv')
MODELL = 'claude-sonnet-5-5'
DATUM = '2026.11.02'
ELTERES = {('UBS_DBH', 'H8414', '007726001001000'): 'pusztaság; kietlenség; káosz'}
FEJ = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'forditas_hu', 'allapot', 'modell',
       'datum', 'terminologia_verzio', 'megjegyzes']


def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read()
    if '\r\n' in nyers or not nyers.endswith('\n'):
        raise SystemExit('megállás: váratlan sorvég: %s' % ut)
    return nyers[:-1].split('\n')


def main():
    t = olvas(TERV)
    tfej = t[0].split('\t')
    terv = [dict(zip(tfej, s.split('\t'))) for s in t[1:] if s]
    if len(terv) != 8:
        raise SystemExit('megállás: a tervezet nem 8 sor')
    dbh = GLF.dbh_forras_idx()
    cache = {}
    sorok = olvas(FORD)
    if next(s for s in sorok if not s.startswith('#')).split('\t') != FEJ:
        raise SystemExit('megállás: a forditasok.tsv fejléce eltér')
    meglevo = {tuple(s.split('\t')[:5]) for s in sorok}
    uj = []
    for r in terv:
        kulcs = (r['szotar'], r['strong'], r['entry_id'], r['jelentes_szam'], r['mezo'])
        if kulcs in meglevo:
            raise SystemExit('megállás: már van sor: %s' % (kulcs,))
        if r['szotar'] == 'UBS_DBH':
            forras = GLF.forras_szoveg_dbh(dict(zip(FEJ, kulcs)), dbh)
        else:
            forras = GLF.tovabbi_forras(dict(zip(FEJ, kulcs)), cache=cache)
        if forras is None or forras != r['forras_szoveg']:
            raise SystemExit('megállás: a forrásszöveg eltér: %s (%r ≠ %r)' % (kulcs, forras, r['forras_szoveg']))
        hu = ELTERES.get(kulcs[:3], r['forditas_hu'])
        eredm = kapuk_futtat(r['szotar'], forras, hu, bizonytalan=[])
        if any(e[1] == 'SERTES' if isinstance(e, (list, tuple)) else False for e in eredm):
            raise SystemExit('megállás: kapu-sértés: %s %r' % (kulcs, eredm))
        megj = ('F12.3: TEREMT-002 (a #121 mintája); kapuk átmentek (naplok/F12_forditas_tervezet.tsv, '
                'naplok/F12_forditas_naplo.md); terminológia v4')
        if kulcs[:3] in ELTERES:
            megj += ('; a 2. tag („desolation”) a session (claude-opus-5-5) javítása a tervezet „elpusztítottság” '
                     'alakja helyett: a Károli „kietlen” szava a tohu megfelelője (nyelvközi egység)')
        megj += ' | scope=%s %s %s | forras=%s | ts=2026-11-02' % (
            r['szotar'], r['strong'], r['entry_id'],
            'konkordancia/UBS_DBH_jelentesek.tsv' if r['szotar'] == 'UBS_DBH' else 'konkordancia/TBESG.txt')
        uj.append('\t'.join([kulcs[0], kulcs[1], kulcs[2], kulcs[3], kulcs[4],
                             hashlib.sha1(forras.encode('utf-8')).hexdigest(), hu, 'sonnet', MODELL, DATUM, 'v4', megj]))
        print('%s → %s' % ('/'.join(kulcs), hu))
    if '--ir' not in sys.argv:
        print('száraz futás: nincs írás (--ir)')
        return
    uj_sorok = sorok + uj
    with open(FORD, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(uj_sorok) + '\n')
    if olvas(FORD) != uj_sorok:
        raise SystemExit('megállás: a visszaolvasott forditasok.tsv eltér')
    print('írva: +%d sor' % len(uj))


if __name__ == '__main__':
    main()
