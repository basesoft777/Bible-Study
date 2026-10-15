"""m2_minta_osszevet.py — F99 M2 ⛔: a vakon kitöltött minta-munkalap(ok) összevetése a kulccsal.

Az összevetés szabálya (a felhasználó döntése, 2026-10-15; rögzítve a KÖVETKEZŐ mérés előtt, naplok/BDB_SZELETELO_M0.md 9.5):
  * a római szakasz (I., II., III. …) a kulcs része: a fő szakasz is a saját római számával áll (a tábla `szakasz` mezője); a jelöletlen
    al-címszó (`h:…`) szakasza római szám nélküli, ahogy a vak lap is írja;
  * normálható CSAK: (1) a backtick és az aposztróf a törzsnévben („Pi`el” = „Pi'el”); (2) a „fej”, a „tagolatlan” és a „<törzs>/-”
    („<törzs>/fej”, „<törzs>”) egyenértékű: egyik sem nevez meg számozott jelentést vagy alpontot;
  * a zárójeles szint („(2)”, „(c)”, „(β)”) külön mutató: a fő mutató a zárójeles szegmensek nélkül hasonlít, a második azt méri, hogy
    a kulcs (durvább) útvonala előtagja-e a kitöltött útvonalnak (helyes-e előtagként);
  * DT-F99i (felhasználó, 2026-10-15; a seed-101 mérés ELŐTT rögzítve): két római szint, két mező — a címszó homonima-száma a
    jelentéspont elején (a kulcsban a `szakasz`), a szócikk római számos fő tagolása (rész) külön (a kulcsban és az új vak lapon a `resz`
    oszlop). Mindkettő pontosan egyezzen. A régi (seed-99/100) kitöltésekben nincs `resz` oszlop: ott a jelentéspont második római száma a
    rész („III I/3”), egy római szám a homonima-szám;
  * könyv és MT-vers: pontos egyezés (a vak lap Károli-könyvrövidítést ír); a Károli-oszlopot nem a vak lap bírálja, hanem a gépi
    összevetés (`karoli_ellenoriz.py`).
Csak olvas. Használat (a repó gyökeréből):
  python eszkozok/olvaso_szerver/m2_minta_osszevet.py --kulcs naplok/BDB_SZELETELO_M2_minta_kulcs.tsv \
      --kitoltott naplok/BDB_SZELETELO_M2_minta_kitoltott_A.tsv naplok/BDB_SZELETELO_M2_minta_kitoltott_B.tsv [--mai-tabla]
A `--mai-tabla` a kulcs szeletelő-oszlopait a mai `adat/bdb_vers_jelentes.tsv` megfelelő soraival (strong + poz) cseréli: így mérhető, hogy a
javítás után a szeletelő mit adna ugyanarra a mintára (tájékoztató, nem új mérés).
"""
import argparse
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROMAI = re.compile(r'^(?:I{1,3}|IV|V|VI)$')
ZAROJEL = re.compile(r'^\([^)]*\)$')


def olvas(p):
    L = [l.rstrip('\n').split('\t') for l in open(p, encoding='utf-8') if l.strip() and not l.startswith('#')]
    h = L[0]
    return [dict(zip(h, r + [''] * (len(h) - len(r)))) for r in L[1:]]


def bont(szakasz, ut):
    """-> (római szakasz vagy '', [szegmensek]) — a kulcs mezőiből."""
    sz = szakasz if ROMAI.match(szakasz or '') else ''
    return sz, [x for x in (ut or '').split('/') if x != '']


def bont_kitoltott(jp, resz_oszlop=None):
    """A vak lap jelentéspontja: „II Qal/2/a”, „I -/2”, „Qal I/2/b”, „II/6/b”, „II fej”, „-/3/(2)/a” → (szakasz, rész, [szegmensek]).
    Ha a lapnak van `resz` oszlopa (seed-101-től), a rész onnan jön; különben a jelentéspont második római száma a rész (DT-F99i)."""
    t = (jp or '').strip()
    sz = ''
    resz = ''
    szavak = re.split(r'\s+', t)
    maradek = []
    for w in szavak:
        if ROMAI.match(w) and not sz:
            sz = w
        elif ROMAI.match(w) and resz_oszlop is None and not resz:
            resz = w
        else:
            maradek.append(w)
    t = ' '.join(maradek)
    reszek = [x for x in re.split(r'[/\s]+', t) if x != '']
    if reszek and ROMAI.match(reszek[0]) and not sz:
        sz = reszek.pop(0)
    # „Qal I/2/b”: a törzs utáni római szám
    for i, x in enumerate(reszek):
        if ROMAI.match(x) and (i > 0 or sz) and (not sz or (resz_oszlop is None and not resz)):
            if not sz:
                sz = reszek.pop(i)
            else:
                resz = reszek.pop(i)
            break
    if resz_oszlop is not None:
        resz = resz_oszlop.strip()
    return sz, resz, reszek


def normal(seg):
    """(1) backtick = aposztróf; (2) a fej / tagolatlan / törzs/- egy alak: 'NINCS_PONT'."""
    s = [x.replace('`', "'") for x in seg if x != '-']           # a hiányzó szint („-”) nem szegmens
    while s and s[-1] == 'fej':
        s.pop()
    if not s or s == ['tagolatlan'] or (len(s) == 1 and not re.match(r'^\d', s[0]) and not re.match(r'^[a-z]$', s[0])):
        return ['NINCS_PONT']
    return s


def fo(seg):
    return normal([x for x in seg if not ZAROJEL.match(x)])


def elotag(kulcs, kit):
    k, e = normal(kulcs), normal(kit)
    return e[:len(k)] == k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kulcs', required=True)
    ap.add_argument('--kitoltott', nargs='+', required=True)
    ap.add_argument('--mai-tabla', action='store_true')
    a = ap.parse_args()
    kulcs = {r['azon']: r for r in olvas(a.kulcs)}
    if a.mai_tabla:
        mai = {}
        for r in olvas(os.path.join(REPO, 'adat', 'bdb_vers_jelentes.tsv')):
            mai[(r['strong'], r['poz'])] = r
        for k in kulcs.values():
            m = mai.get((k['strong'], k['poz']))
            if m:
                for o in ('konyv_feloldas', 'mt_vers', 'karoli_vers', 'vers_feloldas', 'szakasz', 'resz', 'utvonal', 'okkod', 'szurt'):
                    k[o] = m.get(o, '')
            else:
                k['utvonal'] = '?nincs a mai táblában'
    kit = {}
    for f in a.kitoltott:
        for r in olvas(f):
            kit[r['azon']] = r
    sorok = []
    for azon, k in sorted(kulcs.items()):
        e = kit[azon]
        mt_e = e['konyv_mt'].split(' (')[0].strip()
        ok_vers = k['mt_vers'] == mt_e or (not k['mt_vers'] and k['szurt'] == '1')
        ksz, kseg = bont(k['szakasz'], k['utvonal'])
        kresz = k.get('resz', '') or ''
        esz, eresz, eseg = bont_kitoltott(e['jelentespont'], e.get('resz') if 'resz' in e else None)
        ok_jp = (ksz == esz) and (kresz == eresz) and fo(kseg) == fo(eseg)
        ok_elotag = (ksz == esz) and (kresz == eresz) and elotag(kseg, eseg)
        szk = 'kiszurt' if k['szurt'] == '1' else ('bizonytalan' if any(o in k['okkod'].split(',') for o in ('sigla_kozel', 'tobbertelmu', 'ismeretlen_alak', 'nincs_elozmeny', 'orokles_hibas')) else 'bibliai')
        sze = 'kiszurt' if e['szures'].startswith('alhiv') else ('bizonytalan' if e['szures'].startswith('bizony') else 'bibliai')
        sorok.append((azon, k, e, ok_vers, ok_jp, ok_elotag, szk, sze))
    v = [x for x in sorok if x[1]['reteg'] == 'veletlen']
    print('# M2 minta-összevetés: kulcs=%s%s; kitöltött: %s' % (a.kulcs, ' (a mai tábla szerint)' if a.mai_tabla else '', ', '.join(a.kitoltott)))
    print('veletlen\t%d' % len(v))
    print('konyv_vers_egyezik\t%d' % sum(x[3] for x in v))
    print('jelentespont_egyezik\t%d' % sum(x[4] for x in v))
    print('jelentespont_elotagkent_helyes\t%d' % sum(x[5] for x in v))
    for x in v:
        if not x[3]:
            print('VERS\t%s\t%s\t%s\tkulcs: %s\tkitoltott: %s' % (x[0], x[1]['strong'], x[1]['nyers'], x[1]['mt_vers'], x[2]['konyv_mt']))
    for x in v:
        if not x[4]:
            print('JP\t%s\t%s\tkulcs: %s %s %s\tkitoltott: %s%s\t%s' % (
                x[0], x[1]['strong'], x[1]['szakasz'], ('r:' + x[1]['resz']) if x[1].get('resz') else '', x[1]['utvonal'],
                x[2]['jelentespont'], (' r:' + x[2]['resz']) if x[2].get('resz') else '', 'előtagként helyes' if x[5] else ''))
    for reteg in ('veletlen', 'kiszurt', 'szurt', 'bizonytalan'):
        s = [x for x in sorok if x[1]['reteg'] == reteg]
        if not s:
            continue
        print('szures_%s\t%d\tegyezik %d' % (reteg, len(s), sum(x[6] == x[7] for x in s)))
        for x in s:
            if x[6] != x[7]:
                print('SZ\t%s\t%s\tkulcs: %s %s\tkitoltott: %s' % (x[0], x[1]['nyers'], x[6], x[1]['okkod'], x[2]['szures'][:80]))


if __name__ == '__main__':
    main()
