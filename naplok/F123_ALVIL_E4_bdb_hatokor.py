"""F123.ALVIL.J1 (ELLENOR_F123_ALVIL-001 E4): az F123.ALVIL.B1 (52919dfd) szeletelő-javításának hatóköre a H7585-ön kívül.

A B1 a `bdb_szelet._szam_minta`-ban a „] N” jelölőt is jelentés-sorszámnak fogadja el. Az `adat/bdb_vers_jelentes.tsv` diffje
a B1 szülője (52919dfd^) és a HEAD között a H7585 4 során kívül 6 szócikk 181 sorát érinti. A szkript minden ilyen sort párba
állít (kulcs: strong + sorszam + poz; régi ↔ új), és besorolja: javulás / semleges / rontás / eldontetlen.

Elsődleges mérce (a szeletelőtől független): a BDB eredeti angol szócikkszövege (`konkordancia/BDB_teljes_unabridged.tsv`, a
`bdb_szelet.lapit` alakjában, amelyre a `poz` vonatkozik; a `lapit` csak sortörés → szóköz és „1.a” → „1. a.” csere).
Láncolt jelölőkeresés: az 1., 2., … számjelölőt sorban keresi (az n. az n−1. után áll; jelölő: önálló 1–2 jegyű szám, előtte
szóköz vagy a szöveg eleje, utána „.”/szóköz és latin vagy héber betű, „>” vagy „(”), a számon belül az a., b., … betűjelölőket ugyanígy, a következő
számjelölőig. Törzs (Qal, …) esetén a keresés a törzsnév első előfordulásától a következő, mondathatár utáni törzsnévig fut.
Egy útvonal (`-/6`, `Qal/7/c`) szelete: a jelölőjétől a következő azonos vagy magasabb szintű jelölőig. A sor helyes, ha a `poz`
a hozzárendelt útvonal szeletében áll; a `tagolatlan` akkor helyes, ha a szócikkben nincs számjelölő.

Keresztpróba: az `adat/bdb_szakaszok.tsv` (bont.py, DictBDB.json — más forrás, más bontó). A hivatkozás előtti szövegrészt a
szakaszok szövegében keresi, és csak a talált szakasz útvonalának szám/betű részét veti össze (a törzset nem: a bdb_szakaszok a
H7200-ban a Qal 6/g-ben álló „compare … Niph`al” szöveget törzsfejnek veszi, és a Qal 7–8. pontját Niph'al alá teszi).

Besorolás: javulás (új helyes, régi nem); rontás (régi helyes, új nem); semleges (mindkettő helyes vagy mindkettő hibás, vagy
nem csak az `utvonal` változott); eldontetlen (a mérce nem talál jelölőt, vagy a keresztpróba ellentmond).

    python naplok/F123_ALVIL_E4_bdb_hatokor.py
"""
import os
import re
import subprocess
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'olvaso_szerver'))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))

import bdb_szelet as B  # noqa: E402  (csak a `lapit` normalizálás)

TABLA = 'adat/bdb_vers_jelentes.tsv'
B1 = '52919dfd'
KI_TSV = os.path.join(REPO, 'naplok', 'F123_ALVIL_E4_bdb_hatokor.tsv')
BDB_EN = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
SZAKASZOK = os.path.join(REPO, 'adat', 'bdb_szakaszok.tsv')
KIZART = {'H7585'}   # a B1 célpontja; a B1 és az ellenőr külön mérte
TORZSEK = ['Qal', 'Niph`al', 'Pi`el', 'Pu`al', 'Hiph`il', 'Hoph`al', 'Hithpa`el']
BESOROLASOK = ('javulás', 'semleges', 'rontás', 'eldontetlen')
# Kézi besorolás az `eldontetlen` sorokra (F123.ALVIL.J1, 2026-10-29, a BDB_teljes_unabridged H7200 szövegével): a H7200-ban a
# „Niph`al” szó ötször áll; a 8135. („compare v^b, Niph`al and Di”), 9855. („compare Niph`al Num 14:14”) és 10581. („read probably
# Niph`al”) pozíción szövegkritikai utalás a Qal 6/g-n, 8/a-n és 8/c-n belül, nem törzsfej; az első valódi törzsfej a 10654.
# („GASm. Niph`al Perfect …”). A 24 sor mind a Qal 6/g, 6/h, 8/a, 8/b, 8/c valódi szeletében áll (a sorok előtti szöveg kézzel
# átnézve); a régi `Qal/5/g` és `Qal/5/h` a BDB-ben nem létező pont (a Qal 5 csak a.–b.). A keresztpróba ellentmondása a
# bdb_szakaszok hibája, nem a B1-é.
JEGYZET = '— Corrupt is'
KEZI_H7200 ='javulás (kézi): a sor a BDB Qal %s pontjának szövegében áll; a bdb_szakaszok „Niph`al”-szakasza a 8135./9855. pozíciójú szövegközi utalásból ered, nem törzsfej'


def git_tabla(rev):
    ki = subprocess.run(['git', 'show', '%s:%s' % (rev, TABLA)], cwd=REPO, capture_output=True, check=True).stdout
    return ki.decode('utf-8').split('\n')


def sorok(szoveg):
    fej, ki = None, {}
    for s in szoveg:
        s = s.rstrip('\r')
        if not s or s.startswith('#'):
            continue
        m = s.split('\t')
        if fej is None:
            fej = m
            continue
        d = dict(zip(fej, m))
        ki[(d['strong'], d['sorszam'], d['poz'])] = d
    return fej, ki


def bdb_szovegek(strongok):
    ki = {}
    with open(BDB_EN, encoding='utf-8', newline='') as f:
        for i, s in enumerate(f):
            m = s.rstrip('\r\n').split('\t')
            if i and m[0] in strongok:
                ki[m[0]] = B.lapit(m[2])
    return ki


def szam_jelolo(n):
    return re.compile(r'(?:(?<=\s)|^)%d(?:\.\s|\s)(?=[A-Za-z֐-׿>(])' % n)


def betu_jelolo(x):
    return re.compile(r'(?<=\s)%s\.\s' % x)


def tagolas(s, kezdet=0, veg=None):
    """[(kulcs, kezdet, vég)] láncolt kereséssel: számok 1-től, a számokon belül betűk a-tól."""
    veg = len(s) if veg is None else veg
    szamok = []
    p, n = kezdet, 1
    while True:
        m = szam_jelolo(n).search(s, p, veg)
        if not m:
            break
        szamok.append((n, m.start()))
        p, n = m.end(), n + 1
    ki = []
    for i, (n, a) in enumerate(szamok):
        b = szamok[i + 1][1] if i + 1 < len(szamok) else veg
        ki.append(('%d' % n, a, b))
        betuk, q = [], a
        for x in 'abcdefghijkl':
            m = betu_jelolo(x).search(s, q, b)
            if not m:
                break
            betuk.append((x, m.start()))
            q = m.end()
        for j, (x, c) in enumerate(betuk):
            d = betuk[j + 1][1] if j + 1 < len(betuk) else b
            ki.append(('%d/%s' % (n, x), c, d))
    return ki


def torzs_hatar(s, torzs):
    m = re.search(r'(?<![A-Za-z`])%s(?![A-Za-z`])' % re.escape(torzs), s)
    if not m:
        return None
    a = m.end()
    vegek = [a + x.start() for t in TORZSEK if t != torzs
             for x in re.finditer(r'(?<=[.\]]\s)%s(?![A-Za-z`])' % re.escape(t), s[a:])]
    return a, (min(vegek) if vegek else len(s))


def szelet(s, ut):
    reszek = ut.split('/')
    if reszek[0] == '-':
        a, b = 0, len(s)
    else:
        h = torzs_hatar(s, reszek[0].replace("'", '`'))
        if not h:
            return None
        a, b = h
    kulcs = '/'.join(x for x in reszek[1:] if x not in ('-', ''))
    for k, c, d in tagolas(s, a, b):
        if k == kulcs:
            return c, d
    return None


def nem_letezo_pont(s, ut):
    """A számjelölő megvan, de a betűpont nincs a szám szeletében (pl. `Qal/5/c`, ahol a BDB 5. pontja csak a.–b.)."""
    reszek = [x for x in ut.split('/')[1:] if x not in ('-', '')]
    if len(reszek) != 2:
        return False
    return szelet(s, '/'.join([ut.split('/')[0], reszek[0], '-'])) is not None


def helyes(s, ut, poz):
    """(True / False / None, megjegyzés); None: a mérce nem dönt."""
    if ut == 'tagolatlan':
        return (not tagolas(s)), ('' if not tagolas(s) else 'tagolatlan, pedig a szócikkben van számjelölő')
    sz = szelet(s, ut)
    if sz is None:
        if nem_letezo_pont(s, ut):
            return False, 'a BDB-ben nem létező pont: %s' % ut
        return None, ''
    return sz[0] <= poz < sz[1], ''


def szakasz_index(strongok):
    ki = {}
    with open(SZAKASZOK, encoding='utf-8', newline='') as f:
        fej = None
        for s in f:
            if s.startswith('#'):
                continue
            m = s.rstrip('\r\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            if d['strong'] in strongok:
                ki.setdefault(d['strong'], []).append((d['utvonal'], re.sub(r'\s+', ' ', d['szoveg'])))
    return ki


def szamresz(ut):
    return '/'.join(x for x in ut.split('/')[1:] if x not in ('-', ''))


def keresztproba(szak, s, poz, nyers):
    """A hivatkozás előtti szövegrész melyik szakaszban áll (szám/betű rész); None, ha nem egyértelmű."""
    for hossz in (60, 40, 28, 18):
        minta = re.sub(r'\s+', ' ', s[max(0, poz - hossz):poz + len(nyers)]).strip()
        talal = {ut for ut, sz in szak if minta in sz}
        if len({szamresz(u) for u in talal}) == 1:
            return sorted(talal)[0]
    return None


def main():
    fej_r, regi = sorok(git_tabla(B1 + '^'))
    fej_u, uj = sorok(git_tabla('HEAD'))
    assert fej_r == fej_u, 'a fejléc eltér'
    assert set(regi) == set(uj), 'a kulcshalmaz eltér'
    valt = [k for k in sorted(regi) if regi[k] != uj[k] and k[0] not in KIZART]
    kizart = [k for k in sorted(regi) if regi[k] != uj[k] and k[0] in KIZART]
    strongok = sorted({k[0] for k in valt})
    szov = bdb_szovegek(set(strongok))
    szak = szakasz_index(set(strongok))
    ki = []
    for k in valt:
        r, u = regi[k], uj[k]
        mezok = [f for f in fej_r if r[f] != u[f]]
        s = szov[k[0]]
        poz = int(k[2])
        # a vers-folytatás nyers alakja „, 24”: a poz a számra mutat
        ny = r['nyers'].lstrip(', ')
        assert s[poz:poz + len(ny)] == ny, ('a poz nem a nyers hivatkozásra mutat', k)
        kp = keresztproba(szak.get(k[0], []), s, poz, r['nyers'])
        if mezok != ['utvonal']:
            bes, indok = 'semleges', 'nem csak az utvonal változott: ' + ','.join(mezok)
        else:
            (h_r, m_r), (h_u, m_u) = helyes(s, r['utvonal'], poz), helyes(s, u['utvonal'], poz)
            if h_r is None or h_u is None:
                bes, indok = 'eldontetlen', 'a mérce nem talál jelölőt (régi: %s, új: %s)' % (h_r, h_u)
            elif h_u and not h_r:
                bes, indok = 'javulás', 'a poz az új útvonal szeletében áll, a régiében nem'
            elif h_r and not h_u:
                bes, indok = 'rontás', 'a poz a régi útvonal szeletében áll, az újéban nem'
            else:
                bes, indok = 'semleges', 'mindkettő %s' % ('helyes' if h_u else 'hibás')
            for m in (m_r, m_u):
                if m:
                    indok += ' (%s)' % m
            kp_u = szamresz(u['utvonal']) if u['utvonal'] != 'tagolatlan' else ''
            if kp is None:
                indok += '; keresztpróba: nem egyértelmű'
            elif szamresz(kp) == kp_u:
                indok += '; keresztpróba (bdb_szakaszok, szám/betű) egyezik: %s' % kp
            else:
                indok += '; keresztpróba ELLENTMOND (bdb_szakaszok: %s)' % kp
                if k[0] == 'H7200' and kp.startswith("Niph'al") and u['utvonal'].startswith('Qal'):
                    indok += ' — a bdb_szakaszok ismert H7200-hibája: a Qal 6/g-ben álló „compare … Niph`al” szöveget törzsfejnek veszi'
                if bes == 'javulás':
                    bes = 'eldontetlen'
        sz = szelet(s, u['utvonal']) if u['utvonal'] != 'tagolatlan' else None
        kezi = ''
        if bes == 'eldontetlen' and k[0] == 'H7200' and 'ismert H7200-hibája' in indok:
            kezi = KEZI_H7200 % szamresz(u['utvonal'])
        # F123.ALVIL.J22 (ELLENOR_F123_ALVIL-001_2 ELTÉRÉS-5): a szelet végén álló „— Corrupt is …” szövegkritikai jegyzet sorai
        # nem a jelentéspont példái; a régi (nem létező) pontnál jobb helyen állnak, de nem a jelentésben: semleges, jelölt
        if sz is not None and JEGYZET in s[sz[0]:poz]:
            bes = 'semleges'
            indok += '; JELÖLT: a sor a BDB „%s …” szövegkritikai jegyzetében áll, nem a %s jelentésben' % (
                JEGYZET, szamresz(u['utvonal']))
            kezi = 'semleges, jelölt (kézi): szövegkritikai jegyzet, nem a %s jelentés' % szamresz(u['utvonal'])
        ki.append([k[0], k[1], k[2], r['nyers'], r['karoli_vers'], r['utvonal'], u['utvonal'], bes, indok,
                   '' if sz is None else '%d-%d' % sz, kezi])
    with open(KI_TSV, 'w', encoding='utf-8', newline='') as f:
        f.write('# F123.ALVIL.J1 (ELLENOR_F123_ALVIL-001 E4): a B1 (52919dfd) hatása a H7585-ön kívül; régi = 52919dfd^, új = 5fa4f291; '
                'készítő: naplok/F123_ALVIL_E4_bdb_hatokor.py; mérce: konkordancia/BDB_teljes_unabridged.tsv (lapit) láncolt '
                'jelölőkereséssel; keresztpróba: adat/bdb_szakaszok.tsv (csak szám/betű)\n')
        f.write('\t'.join(['strong', 'sorszam', 'poz', 'nyers', 'karoli_vers', 'utvonal_regi', 'utvonal_uj', 'besorolas', 'indok',
                           'uj_szelet', 'kezi_besorolas']) + '\n')
        for s in ki:
            f.write('\t'.join(s) + '\n')
    c = Counter((s[0], s[7]) for s in ki)
    vegso = Counter((s[0], 'javulás' if s[10].startswith('javulás') else s[7]) for s in ki)
    print('VÁLTOZÓ_SOR (H7585 nélkül)\t%d' % len(valt))
    print('H7585_SOR (kizárva)\t%d' % len(kizart))
    for st in strongok:
        print('%s\t%s' % (st, '  '.join('%s=%d' % (b, c[(st, b)]) for b in BESOROLASOK)))
    for b in BESOROLASOK:
        print('ÖSSZ_%s\t%d' % (b, sum(v for (st, bb), v in c.items() if bb == b)))
    print('A KÉZI BESOROLÁS UTÁN:')
    for st in strongok:
        print('%s\t%s' % (st, '  '.join('%s=%d' % (b, vegso[(st, b)]) for b in BESOROLASOK)))
    kpc = Counter('egyezik' in s[8] and 'egyezik' or ('ELLENTMOND' in s[8] and 'ellentmond' or 'nem_egyertelmu') for s in ki)
    print('KERESZTPRÓBA\t%s' % dict(kpc))


if __name__ == '__main__':
    main()
