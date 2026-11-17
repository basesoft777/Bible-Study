#!/usr/bin/env python
"""bdb_sefaria_proba.py — N-F197a (DT776): a Sefaria-tanú bekapcsolása előtti független, mintán kívüli kézi szúrópróba előkészítése és értékelése.

A tanút NEM kapcsolja be; csak megméri, hogy a `biztos` → `ketes:jp_tanu_sefaria` váltások közül hányat okoz a tábla, és hányat a Sefaria hibája.

Alparancsok (mind a repó gyökeréből; a nagy fájlok a REPÓN KÍVÜL, a `--ut` / `--tabla` mappában):
  valtasok  a teljes tanú-táblán a `biztos` sorok közül azok, amelyeket a tanú `elter`-nek ítél (szám, szint, szócikk-eloszlás).
  minta     rögzített seeddel N sor, szócikkenként legfeljebb egy (rétegezés); kizárva: a seed-103 minta, a korábbi 40 soros próba és a
            két kézi próba (H8081 Ez 23:41, H3847 3Móz 6:4). Kimenet: `--ut`/bir/NNN.txt (a vak bírálati lapok: a tábla és a Sefaria
            pontja véletlen sorrendben, A/B névvel, azonos alakban) + `--ut`/kulcs.tsv (a forrás–betű megfeleltetés; a bírálónak NEM adandó).
  ertekel   a bírálat (`--valasz`: soronként azon<TAB>A|B|mindketto|egyik_sem|eldonthetetlen) + kulcs → hibaarányok, 95%-os Clopper–Pearson
            konfidencia-intervallummal, hibatípusok.

TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import math
import os
import random
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, D)
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))

import bdb_sefaria_tanu as ST  # noqa: E402
from bdb_konyv_javit import MACULA_KOD  # noqa: E402

NAPLO = os.path.join(REPO, 'naplok')
MANUALIS = {('H8081', 'Ez 23:41'), ('H3847', '3Móz 6:4')}      # a két kézi próba (naplok/F197_jelentes.md 4.)
SEED = 20261116
ABLAK_EL, ABLAK_UT = 7000, 1200


def sorok_tsv(ut):
    return ST.tsv_sorok(ut)


def kizart_kulcsok():
    """A mintán kívüliség: a seed-103 mintája (a 40 soros próba ennek része) → {(strong, sorszam)}."""
    ki = set()
    for r in sorok_tsv(os.path.join(NAPLO, 'BDB_SZELETELO_M2_minta_seed103_kulcs.tsv')):
        ki.add((r['strong'], r['sorszam']))
    return ki


def valtas_sorok(tabla_ut):
    """→ (a vizsgált `biztos` sorok száma, [az eltérést kapó sorok])."""
    tanu = ST.tanu_betolt(tabla_ut)
    osszes, valt = 0, []
    for r in sorok_tsv(ST.VJ):
        if r['szurt'] != '0' or not r['mt_vers'] or r['vers_feloldas'] == 'usz':
            continue
        if r['bizonyossag'] != 'biztos' or 'jp_kezi' in r['okkod'].split(','):
            continue
        osszes += 1
        if ST.itelet(tanu, r['strong'], r['sorszam'], r['mt_vers'], r['szakasz'], r['resz'], r['utvonal']) == 'elter':
            r['_tanu'] = tanu[(r['strong'], r['sorszam'])]
            valt.append(r)
    return osszes, valt


def szint(r):
    """Az eltérés szintje: törzs, szám, betű (a tábla és a Sefaria pontjából)."""
    tp = ST.tabla_pont(r['szakasz'], r['resz'], r['utvonal'])
    _, _, tt, tsz, tb = tp
    ki = []
    for s in r['_tanu'][2].split(';'):
        _, sres, st, ssz, sb = ST.ut_bont(s)
        k = []
        if not ST._torzs_egyezik(tt, st):
            k.append('torzs')
        if tsz != ssz:
            k.append('szam')
        if tb and sb and tb != sb:
            k.append('betu')
        ki.append('+'.join(k) or 'resz')
    return ki[0]


def parancs_valtasok(a):
    osszes, valt = valtas_sorok(a.tabla)
    st = collections.Counter(r['strong'] for r in valt)
    print('vizsgált `biztos` sor: %d; váltás (biztos → ketes): %d, %d szócikken' % (osszes, len(valt), len(st)))
    print('illesztés: ' + ', '.join('%s %d' % kv for kv in sorted(collections.Counter(r['_tanu'][1] for r in valt).items())))
    print('szint: ' + ', '.join('%s %d' % kv for kv in sorted(collections.Counter(szint(r) for r in valt).items())))
    print('a 10 legtöbb váltású szócikk: ' + ', '.join('%s %d' % kv for kv in st.most_common(10)))


# ------------------------------------------------------------------ a vak lap

def kanon_pont(szakasz, resz, utvonal):
    """A tábla pontja → azonos megjelenítési alak a Sefaria-pontéval."""
    _, rsz, t, sz, b = ST.tabla_pont(szakasz, resz, utvonal)
    return rsz, ('' if t == '-' else t), sz, b


TORZSEK = ['qal', 'niphal', 'piel', 'pual', 'hiphil', 'hophal', 'hithpael', 'polel', 'poel', 'pilpel', 'polal', 'pealal', 'hithpolel',
           'hithpalpel', 'hishtaphel', 'shaphel', 'hithpoel', 'hothpaal', 'poal', 'pulal', 'hithpael']


def torzs_kanon(t):
    """A törzsnév azonos megjelenítési alakra (a Sefaria „Pōʿlēl” és a tábla „Po'el” forrás-jegyei nem árulkodnak): teljes névre."""
    k = ST._torzs_kulcs(t)
    if not k:
        return ''
    for c in TORZSEK:
        if c.startswith(k) or k.startswith(c):
            return c.capitalize()
    return k.capitalize()


def pont_szoveg(resz, torzs, szam, betu):
    if not (torzs or szam or betu):
        return 'a szócikk fejrésze: nincs számozott jelentéspont' + (' (rész: %s)' % resz if resz else '')
    t = torzs_kanon(torzs)
    return '%storzs: %s; szám: %s; betű: %s' % ('rész: %s; ' % resz if resz else '', t or '(nincs)', szam or '(nincs)', betu or '(nincs)')


def macula_vers(versek):
    """{mt_vers: [(szo, strong_szam)]} csak a kért versekre."""
    ki = {}
    kdir = os.path.join(REPO, 'konkordancia')
    kerdezett = set(versek)
    for fn in sorted(os.listdir(kdir)):
        if not (fn.startswith('Macula_heber_') and fn.endswith('.tsv')):
            continue
        fej = None
        for sor in open(os.path.join(kdir, fn), encoding='utf-8', newline=''):
            if sor.startswith('#'):
                continue
            p = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = {k: i for i, k in enumerate(p)}
                continue
            m = re.match(r'(\w+) (\d+):(\d+)', p[fej['ref']])
            if not m or m.group(1) not in MACULA_KOD:
                continue
            v = '%s %s:%s' % (MACULA_KOD[m.group(1)], m.group(2), m.group(3))
            if v not in kerdezett:
                continue
            s = (p[fej['strong_x']] or p[fej['strong']] or '').strip()
            ki.setdefault(v, []).append((p[fej['szo']], re.sub(r'^H0*', '', s.split('/')[0]) if s else ''))
    return ki


def parancs_minta(a):
    osszes, valt = valtas_sorok(a.tabla)
    kiz = kizart_kulcsok()
    jelolt = [r for r in valt if (r['strong'], r['sorszam']) not in kiz and (r['strong'], r['mt_vers']) not in MANUALIS
              and r['_tanu'][1].startswith('pontos')]
    n_hom = sum(1 for r in valt if r['_tanu'][1].startswith('barmely'))
    st = collections.defaultdict(list)
    for r in jelolt:
        st[r['strong']].append(r)
    print('váltás: %d (ebből „bármely” illesztésű, a mintából kizárva: %d); mintázható: %d sor, %d szócikken' % (
        len(valt), n_hom, len(jelolt), len(st)))
    rnd = random.Random(a.seed)
    szocikkek = rnd.sample(sorted(st), a.n)
    en = {d['Strong_padded']: d['Teljes_szocikk'] for d in sorok_tsv(ST.BDB_EN)}
    valasztott = [(s, rnd.choice(st[s])) for s in szocikkek]
    mt_versek = macula_vers({r['mt_vers'] for _, r in valasztott})
    ids = list(range(1, a.n + 1))
    rnd.shuffle(ids)
    os.makedirs(os.path.join(a.ut, 'bir'), exist_ok=True)
    kulcs = []
    for (s, r), azon in zip(valasztott, ids):
        azon = 'P%02d' % azon
        tab = pont_szoveg(*kanon_pont(r['szakasz'], r['resz'], r['utvonal']))
        sefp = ST.ut_bont(r['_tanu'][2])
        sef = pont_szoveg(sefp[1], sefp[2], sefp[3], sefp[4])
        tabla_a = rnd.random() < 0.5
        A, B = (tab, sef) if tabla_a else (sef, tab)
        szoveg = en[s]
        poz = int(r['poz'])
        nyers = r['nyers']
        jel = szoveg[:poz] + ' ⟦►' + nyers + '◄⟧ ' + szoveg[poz + len(nyers):]
        # az ablak: a szócikk eleje (szócím, jelentés) + a hivatkozás előtti ABLAK_EL és utáni ABLAK_UT karakter; a teljes szöveg külön fájlban
        m_ = len(szoveg[:poz]) + 1
        if len(jel) > ABLAK_EL + ABLAK_UT + 600:
            kezd = max(600, m_ - ABLAK_EL)
            ablak = jel[:600] + (' […] ' if kezd > 600 else '') + jel[kezd:m_ + ABLAK_UT] + (' […]' if m_ + ABLAK_UT < len(jel) else '')
        else:
            ablak = jel
        os.makedirs(os.path.join(a.ut, 'teljes'), exist_ok=True)
        with open(os.path.join(a.ut, 'teljes', azon + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(jel)
        ige = ' '.join(('«%s»' % w if sz == s.lstrip('H').lstrip('0') else w) for w, sz in mt_versek.get(r['mt_vers'], [])) or '(nincs)'
        with open(os.path.join(a.ut, 'bir', azon + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('BÍRÁLATI LAP %s\n\n' % azon)
            f.write('Szócikk (Strong-szám): %s\nIgehely (a hivatkozás feloldása, MT-számozás): %s\n' % (s, r['mt_vers']))
            f.write('A BDB-ben a hivatkozás szövege: %s (a szócikkben ⟦►…◄⟧ jelöli)\n' % nyers)
            f.write('A vers héber szövege (a szócikk szava «…» között, ha azonosítható):\n%s\n\n' % ige)
            f.write('KÉT JELÖLT jelentéspont ugyanarra a hivatkozásra (a BDB 1906-os tagolásában: törzs → szám → betű):\n')
            f.write('  A: %s\n  B: %s\n\n' % (A, B))
            f.write('A BDB-szócikk szövege (Brown–Driver–Briggs, 1906): a szócikk eleje és a hivatkozás környéke, a hivatkozás helyén '
                    'megjelölve ( […] = kihagyott rész). A teljes szócikk, ha az ablak nem elég: %s\n\n%s\n'
                    % (os.path.join(a.ut, 'teljes', azon + '.txt'), ablak))
        kulcs.append([azon, s, r['sorszam'], r['mt_vers'], nyers, tab, sef, 'A=tabla,B=sefaria' if tabla_a else 'A=sefaria,B=tabla',
                      r['_tanu'][1], szint(r), str(len(st[s]))])
    kulcs.sort()
    with open(os.path.join(a.ut, 'kulcs.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['azon', 'strong', 'sorszam', 'mt_vers', 'nyers', 'tabla_pont', 'sefaria_pont', 'hozzarendeles', 'illesztes',
                           'szint', 'szocikk_valtasa']) + '\n')
        for k in kulcs:
            f.write('\t'.join(k) + '\n')
    print('%d lap: %s' % (len(kulcs), os.path.join(a.ut, 'bir')))


# ------------------------------------------------------------------ értékelés

def cp_ci(k, n, alfa=0.05):
    """Clopper–Pearson (egzakt) konfidencia-intervallum; bináris keresés a binomiális eloszlás-függvényen."""
    if n == 0:
        return (0.0, 1.0)

    def cdf(x, p):          # P(X <= x)
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, x + 1))

    def keres(f):
        lo, hi = 0.0, 1.0
        for _ in range(80):
            mid = (lo + hi) / 2
            if f(mid):
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    also = 0.0 if k == 0 else keres(lambda p: (1 - cdf(k - 1, p)) < alfa / 2)       # P(X >= k | p) csökkenő a p alatt
    felso = 1.0 if k == n else keres(lambda p: cdf(k, p) > alfa / 2)
    return also, felso


def parancs_ertekel(a):
    kulcs = {r['azon']: r for r in sorok_tsv(os.path.join(a.ut, 'kulcs.tsv'))}
    valasz = {}
    for sor in open(a.valasz, encoding='utf-8'):
        sor = sor.rstrip('\n')
        if sor and not sor.startswith('#') and not sor.startswith('azon'):
            m = sor.split('\t')
            valasz[m[0]] = m[1]
    hianyzik = sorted(set(kulcs) - set(valasz))
    if hianyzik:
        sys.exit('hiányzó válasz: %s' % ', '.join(hianyzik))
    c = collections.Counter()
    sulyozott = collections.Counter()
    tipus = collections.defaultdict(collections.Counter)
    for az, k in kulcs.items():
        v = valasz[az]
        tabla_a = k['hozzarendeles'].startswith('A=tabla')
        if v in ('A', 'B'):
            helyes = 'tabla' if (v == 'A') == tabla_a else 'sefaria'
        else:
            helyes = v
        c[helyes] += 1
        sulyozott[helyes] += int(k['szocikk_valtasa'])
        tipus[helyes][k['szint']] += 1
    n = len(kulcs)
    dont = n - c['eldonthetetlen']
    tabla_hiba = c['sefaria'] + c['egyik_sem']
    sef_hiba = c['tabla'] + c['egyik_sem']
    print('sorok: %d; eldönthetetlen: %d; eldönthető: %d' % (n, c['eldonthetetlen'], dont))
    print('a bírálat szerint helyes: tábla %d, Sefaria %d, mindkettő %d, egyik sem %d' % (c['tabla'], c['sefaria'], c['mindketto'], c['egyik_sem']))
    for nev, k in (('a TÁBLA téved (tehát a váltás jogos)', tabla_hiba), ('a SEFARIA téved (tehát téves riasztás)', sef_hiba)):
        lo, hi = cp_ci(k, dont)
        print('%s: %d / %d = %.1f%%, 95%% CI [%.1f%%, %.1f%%]' % (nev, k, dont, 100.0 * k / max(dont, 1), 100 * lo, 100 * hi))
    sw = sum(sulyozott[x] for x in ('tabla', 'sefaria', 'mindketto', 'egyik_sem'))
    print('szócikk-súlyozott (a szócikk váltásainak számával): a tábla téved %.1f%%, a Sefaria téved %.1f%%' % (
        100.0 * (sulyozott['sefaria'] + sulyozott['egyik_sem']) / max(sw, 1), 100.0 * (sulyozott['tabla'] + sulyozott['egyik_sem']) / max(sw, 1)))
    for h in ('tabla', 'sefaria', 'mindketto', 'egyik_sem', 'eldonthetetlen'):
        print('  %s: szint szerint %s' % (h, dict(tipus[h])))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    for nev in ('valtasok', 'minta', 'ertekel'):
        p = sub.add_parser(nev)
        p.add_argument('--tabla', default=ST.KI, help='a teljes tanú-tábla (SEMA 2.29.1); a teljes letöltésből a repón kívül generálva')
        p.add_argument('--ut', default=r'D:\pardes_tanu\bdb\proba', help='a lapok és a kulcs mappája (a repón kívül)')
        if nev == 'minta':
            p.add_argument('--seed', type=int, default=SEED)
            p.add_argument('--n', type=int, default=40)
        if nev == 'ertekel':
            p.add_argument('--valasz', required=True)
    a = ap.parse_args()
    {'valtasok': parancs_valtasok, 'minta': parancs_minta, 'ertekel': parancs_ertekel}[a.cmd](a)


if __name__ == '__main__':
    main()
