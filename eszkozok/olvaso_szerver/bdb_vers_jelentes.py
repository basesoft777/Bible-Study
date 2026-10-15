"""bdb_vers_jelentes.py — F99 M2: a BDB igehely-hivatkozásai feloldva és jelentésponthoz kötve → adat/bdb_vers_jelentes.tsv.

Minden angol BDB-szócikk (konkordancia/BDB_teljes_unabridged.tsv) minden hivatkozására egy sor: a könyv feloldása (kiírt / örökölt /
vers-folytatás), az MT-vers, a Károli-vers (MT → Károli átkulcsolás), a jelentéspont (szakasz + törzs/jelentés/alpont, a szeletelő
csomópontjai szerint), okkóddal. A szabályok a DT-F99a döntése szerint (felhasználó, 2026-10-15):
  (1) a nem bibliai mű és a `^`-hoz tapadt kommentár-hely okkóddal kiszűrve (`szurt=1`, Károli-vers nélkül); a közeli sigla és a többértelmű
      könyvalak a táblában marad, `bizonytalan` jelöléssel (okkód); a nemi tanú („noun masculine^Gen 1:27”) bibliai hivatkozás;
  (2) MT → Károli: a Macula `karoli` oszlopa (konkordancia/Macula_heber_*.tsv), az F85-ben elvetett régiókban (naplok/F85_macula_elvetve.tsv)
      az azonos kulcs; a Károli-versmegfeleltetés MT-osztályú soraival ellenőrizve, ellentmondásnál `atkulcsolt_bizonytalan`;
  (3) a Károliban vagy az MT-ben nem létező vers a táblában marad, üres Károli-verssel és okkóddal, kitöltés nélkül;
  (4) egyfejezetes könyv fejezetszám nélkül („Obad 8”) az 1. fejezetre oldódik.

Használat (a repó gyökeréből):
  python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts 2026-10-15        # írja az adat/bdb_vers_jelentes.tsv-t
  python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts 2026-10-15 --ellenoriz   # újragenerál a memóriába, bájtra összeveti
Azonos bemenettel és --ts-sel bájtra azonos. I/O: split('\\t') / '\\t'.join (csv modul nélkül).
"""
import argparse
import collections
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, D)
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))

import bdb_szelet as B  # noqa: E402

BDB_EN = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
STRONG_SZOTAR = os.path.join(REPO, 'konkordancia', 'Strong_szotar.tsv')
OSHL_INDEX = os.path.join(REPO, 'konkordancia', 'OSHL_lexikalis_index.tsv')
VERSMEGF = os.path.join(REPO, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')
KAROLI = os.path.join(REPO, 'konkordancia', 'Karoli_1908.tsv')
F85_ELVETVE = os.path.join(REPO, 'naplok', 'F85_macula_elvetve.tsv')
KI = os.path.join(REPO, 'adat', 'bdb_vers_jelentes.tsv')

FEJ = ['strong', 'bdb_id', 'sorszam', 'poz', 'nyers', 'konyv_feloldas', 'mt_vers', 'karoli_vers', 'vers_feloldas', 'szakasz', 'utvonal',
       'okkod', 'szurt', 'proveniencia']
SZURENDO = {'nem_bibliai', 'sigla_tapadt'}


def fajl_hash(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for d in iter(lambda: f.read(1 << 20), b''):
            h.update(d)
    return h.hexdigest()[:12]


def tsv_sorok(ut):
    fej, ki = None, []
    with open(ut, encoding='utf-8', newline='') as f:
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            ki.append(dict(zip(fej, m)))
    return ki


def betolt():
    en = {d['Strong_padded']: d['Teljes_szocikk'] for d in tsv_sorok(BDB_EN)}
    lem = {}
    with open(STRONG_SZOTAR, encoding='utf-8', newline='') as f:
        for i, sor in enumerate(f):
            if i == 0 or sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) > 1:
                lem.setdefault(m[0], m[1])
    bdb_id = collections.defaultdict(list)
    for d in tsv_sorok(OSHL_INDEX):
        if d['strong'] != '—' and d['bdb_id'] != '—' and d['bdb_id'] not in bdb_id[d['strong']]:
            bdb_id[d['strong']].append(d['bdb_id'])
    vm_karoli, vm_mt = set(), {}
    for d in tsv_sorok(KAROLI):
        vm_karoli.add(d['Igehely'])
    for d in tsv_sorok(VERSMEGF):
        if d['igehely_mt']:
            k = d['igehely_karoli'].rsplit(' ', 1)[0]
            vm_mt['%s %s' % (k, d['igehely_mt'])] = d['igehely_karoli']
    elvetett = set()
    for d in tsv_sorok(F85_ELVETVE):
        elvetett.add((d['konyv'], int(d['fejezet'])))
    return en, lem, bdb_id, vm_karoli, vm_mt, elvetett


# A Károli-szöveg (Karoli_1908.tsv) és a versmegfeleltetés a Siralmakat „Sir”-nek írja, a könyvalak-tábla (LEK) „JSir”-nek: a Károli-vers
# a Karoli_1908 kulcsa (link a szerverre), az MT-vers a LEK alakja.
KAROLI_KONYV = {'JSir': 'Sir'}


def mt_karoli(K, versek, mt2k, vm_karoli, vm_mt, elvetett, konyv, c, v):
    """-> (mt_vers, karoli_vers, vers_feloldas, okkod_kieg)"""
    mt = '%s %d:%d' % (konyv, c, v)
    kk = KAROLI_KONYV.get(konyv, konyv)
    if v not in versek.get(konyv, {}).get(c, ()):
        return mt, '', 'nem_letezo_vers', 'nem_letezo_vers'
    if (konyv, c) in elvetett:
        kar = {(kk, c, v)}
        mod = 'azonos_f85'
    else:
        kar = set(mt2k.get((konyv, c, v), set()))
        mod = None
    if not kar:
        return mt, '', 'nincs_karoli', 'nincs_karoli'
    jel = sorted(kar, key=lambda x: (x[1], x[2]))
    karoli = '%s %d:%d' % jel[0]
    kieg = 'tobb_karoli_vers' if len(jel) > 1 else ''
    if mod is None:
        mod = 'azonos' if karoli == '%s %d:%d' % (kk, c, v) else 'atkulcsolt'
    mtk = '%s %d:%d' % (kk, c, v)
    if mtk in vm_mt and vm_mt[mtk] != karoli:
        mod = 'atkulcsolt_bizonytalan'
    if karoli not in vm_karoli:
        return mt, '', 'nincs_karoli', 'karoli_vers_nem_letezik'
    return mt, karoli, mod, kieg


def general(ts, strongok=None):
    """A tábla sorai (és a kód-hash); `strongok`: csak ezek a szócikkek (tesztekhez)."""
    K = B._konyvtabla()
    en, lem, bdb_id, vm_karoli, vm_mt, elvetett = betolt()
    versek, _, mt2k = K.macula_betolt()
    osz = set(K.OSZ)
    modhash = '%s+%s' % (fajl_hash(os.path.join(D, 'bdb_szelet.py')), fajl_hash(os.path.abspath(__file__)))
    sorok = []
    for strong in sorted(strongok if strongok is not None else en):
        szoveg = en[strong]
        r = B.szeletel(szoveg, lem.get(strong, ''))
        savok = B.csomopont_savok(szoveg, r)
        # tagolatlan szócikk (nincs számozott jelentés, alpont, törzs): a hivatkozás az egész szócikkhez tartozik
        tagolt = any(not ut.endswith('/-') or szint == 'alpont' or not ut.startswith('-/') for _, _, _, ut, szint in savok)
        prov = 'scope=%s | forras=bdb_vers_jelentes@%s | ts=%s' % (strong, modhash, ts)
        for n, h in enumerate(B.hivatkozasok(szoveg), 1):
            szak, ut = B.jelentespont(h['poz'], savok)
            if not tagolt:
                szak, ut = '', 'tagolatlan'
            ok = h['okkod']
            mt = kar = ''
            vmod = ''
            if h['konyv'] and ok not in SZURENDO:
                if h['konyv'] in osz:
                    mt, kar, vmod, kieg = mt_karoli(K, versek, mt2k, vm_karoli, vm_mt, elvetett, h['konyv'], h['c'], h['v'])
                    if kieg:
                        ok = ok + ',' + kieg if ok else kieg
                else:
                    mt, vmod = '%s %d:%d' % (h['konyv'], h['c'], h['v']), 'usz'
                    ok = ok + ',usz' if ok else 'usz'
            sorok.append([strong, ','.join(bdb_id.get(strong, [])), str(n), str(h['poz']), h['nyers'], h['konyv_mod'], mt, kar, vmod,
                          szak, ut, ok, '1' if h['okkod'] in SZURENDO else '0', prov])
    return sorok, modhash


def kiir(sorok, modhash, ts):
    fej = ['# GENERÁLT: eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts %s — kézzel nem szerkesztendő (F99 M2; séma: adat/SEMA.md 2.29).' % ts,
           '# forras: konkordancia/BDB_teljes_unabridged.tsv@%s + Macula_heber_* (MT-versek, MT→Károli) + Karoli_versmegfeleltetes.tsv@%s + '
           'Karoli_1908.tsv@%s (Károli-versek) + naplok/F85_macula_elvetve.tsv + OSHL_lexikalis_index.tsv (bdb_id); '
           'kód: bdb_szelet.py+bdb_vers_jelentes.py@%s (a sorok proveniencia-mezője erre hivatkozik); szabály: DT-F99a'
           % (fajl_hash(BDB_EN), fajl_hash(VERSMEGF), fajl_hash(KAROLI), modhash),
           '\t'.join(FEJ)]
    for s in sorok:
        for x in s:
            if '\t' in x or '\n' in x:
                raise SystemExit('HIBA: tab vagy sortörés a mezőben: %r' % s)
    return '\n'.join(fej + ['\t'.join(s) for s in sorok]) + '\n'


def minta(seed, n, kieg, ki_ut):
    """Az M2 ⛔ minta-ellenőrzésének munkalapja (javaslat: naplok/BDB_SZELETELO_M0.md 9.4): a meglévő táblából `n` egyszerű véletlen sor
    (random.Random(seed)), és rétegenként `kieg` további sor a kiszűrt (szurt=1) és a bizonytalan (sigla_kozel, tobbertelmu) hivatkozásokból.
    Soronként a forrás-környezet (±70 karakter) és a jelentéspont csomópontjának eleje, kitöltendő ítélet-oszlopokkal. Csak olvas, a
    munkalapot a megadott útra írja (a repón kívülre vagy a naplok/ alá)."""
    import random
    fej, sorok = None, []
    with open(KI, encoding='utf-8', newline='') as f:
        for s in f:
            if s.startswith('#'):
                continue
            m = s.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            sorok.append(dict(zip(fej, m)))
    rnd = random.Random(seed)
    valasztott = [('veletlen', s) for s in rnd.sample(sorok, n)]
    for nev, felt in (('szurt', lambda s: s['szurt'] == '1'),
                      ('bizonytalan', lambda s: any(o in s['okkod'].split(',') for o in ('sigla_kozel', 'tobbertelmu')))):
        pool = [s for s in sorok if felt(s)]
        valasztott += [(nev, s) for s in rnd.sample(pool, min(kieg, len(pool)))]
    en, lem, _, _, _, _ = betolt()
    ki = ['# M2 ⛔ minta-munkalap: seed=%d, %d véletlen + %d/réteg kiegészítő; forrás: adat/bdb_vers_jelentes.tsv' % (seed, n, kieg),
          '\t'.join(['reteg', 'strong', 'sorszam', 'nyers', 'kornyezet', 'konyv_feloldas', 'mt_vers', 'karoli_vers', 'vers_feloldas',
                     'szakasz', 'utvonal', 'csomopont_eleje', 'okkod', 'szurt', 'itelet_konyv_vers', 'itelet_jelentespont', 'itelet_szures', 'megjegyzes'])]
    cache = {}
    for reteg, s in valasztott:
        szoveg = en[s['strong']]
        if s['strong'] not in cache:
            r = B.szeletel(szoveg, lem.get(s['strong'], ''))
            cache[s['strong']] = (B.lapit(szoveg), B.csomopont_savok(szoveg, r))
        flat, savok = cache[s['strong']]
        p = int(s['poz'])
        korny = flat[max(0, p - 70):p] + '⟦' + flat[p:p + len(s['nyers'])] + '⟧' + flat[p + len(s['nyers']):p + len(s['nyers']) + 70]
        csp = next((flat[a:min(b, a + 50)] for a, b, sz, ut, _ in savok if sz == s['szakasz'] and ut == s['utvonal']), '')
        ki.append('\t'.join([reteg, s['strong'], s['sorszam'], s['nyers'], korny.replace('\t', ' '), s['konyv_feloldas'], s['mt_vers'], s['karoli_vers'],
                             s['vers_feloldas'], s['szakasz'], s['utvonal'], csp.replace('\t', ' '), s['okkod'], s['szurt'], '', '', '', '']))
    with open(ki_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')
    print('munkalap: %s (%d sor)' % (ki_ut, len(valasztott)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--minta', type=int, metavar='SEED', help='az M2 ⛔ minta-munkalapja (nem írja a táblát)')
    ap.add_argument('--minta-n', type=int, default=200)
    ap.add_argument('--minta-kieg', type=int, default=25)
    ap.add_argument('--minta-ki', default=None)
    ap.add_argument('--ts', help='a proveniencia ts mezője (a futás napja); azonos ts-sel bájtra azonos a kimenet')
    ap.add_argument('--ellenoriz', action='store_true', help='nem ír: újragenerál és összeveti a meglévő táblával')
    a = ap.parse_args()
    if a.minta is not None:
        minta(a.minta, a.minta_n, a.minta_kieg, a.minta_ki or os.path.join(REPO, 'naplok', 'BDB_SZELETELO_M2_minta.tsv'))
        return
    if not a.ts:
        ap.error('--ts kell')
    sorok, modhash = general(a.ts)
    szoveg = kiir(sorok, modhash, a.ts)
    if a.ellenoriz:
        regi = open(KI, encoding='utf-8', newline='').read() if os.path.exists(KI) else ''
        print('bájtra azonos' if regi == szoveg else 'ELTÉR')
        sys.exit(0 if regi == szoveg else 1)
    with open(KI, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    c = collections.Counter()
    for s in sorok:
        c['sor'] += 1
        c['szurt=' + s[12]] += 1
        c['konyv:' + s[5]] += 1
        c['vers:' + (s[8] or '—')] += 1
        c['karoli_vers_van' if s[7] else 'karoli_vers_nincs'] += 1
        c['jelentespont:' + (s[10] if s[10] in ('fej', 'tagolatlan') else 'csomopont')] += 1
        for o in s[11].split(','):
            if o:
                c['okkod:' + o] += 1
    for k in sorted(c):
        print('%s\t%d' % (k, c[k]))


if __name__ == '__main__':
    main()
