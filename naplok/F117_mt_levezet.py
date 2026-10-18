"""F117.3 (DT-F117d (c)): az `igehely_mt` versenkénti levezetése az A–D′ célhalmaz 346 Károli-versére.

Tanúk (a versmegfeleltető tábla és a Macula `karoli` oszlopa NÉLKÜL):
  * Károli-oldal: konkordancia/TAHOT_kivonat.tsv (Károli-kulcs, F85) — a vers héber Strong-halmaza és szószáma;
  * MT-oldal: konkordancia/Macula_heber_<könyv>.tsv `ref` oszlopa (MT-számozás, a Macula saját vershatára).
Jel: Strong-Jaccard (a grammatikai H9xxx nélkül); második igazítás: Jaccard + szószám-arány.
Szabály (DT-F117b (a), DT-F117d): a két igazítás egyezik, a lépés 1-1, az MT-ablak hézag- és átfedésmentesen lefedett.
KJV-ellenőrzés (DT-F117d kiegészítés): minden soron az MT-érték összevetése a kézi ítélet KJV-párjával
(naplok/F117_itelet.tsv; az Ézs 64:1-nél a DT-F117c (2) szerinti 64:1). Az MT≠KJV eltérés gépileg csak „ismert MT≠KJV
fejezeten” fogadható el; a listát az adatból számolja: azok a fejezetek, ahol a Macula-MT és a KJV_Strongs_teljes
versszáma eltér (± a szomszéd fejezet, mert a vershatár-eltolás átnyúlik). Máshol `KEZI_OLVASAS`.
Összevetés a KK1b-tervezet `igehely_mt`-jével (naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv): egyezik / javitott / uj.

Kimenet: naplok/F117_mt_levezetes.tsv (proveniencia-sorral). Futtatás: python naplok/F117_mt_levezet.py [--szoveg]
TSV-olvasás split('\\t'), a csv modul nélkül.
"""
import os
import re
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'konkordancia')
ITELET = os.path.join(ROOT, 'naplok', 'F117_itelet.tsv')
OSSZEVET = os.path.join(ROOT, 'naplok', 'F117_szoveg_osszevetes.tsv')
TERV = os.path.join(ROOT, 'naplok', 'KAROLI_KK1b_kulcstabla_tervezet.tsv')
KIMENET = os.path.join(ROOT, 'naplok', 'F117_mt_levezetes.tsv')

MACULA = {'2Móz': 'Exodus', 'Dán': 'Daniel', 'Hós': 'Hoseas', 'Jób': 'Job', 'Péld': 'Peldabeszedek',
          'Én': 'Enekek_Eneke', 'Ézs': 'Ezsaias', 'Préd': 'Predikator', '1Kir': 'Kiralyok_1', 'Jón': 'Jonas',
          '1Sám': 'Samuel_1'}
KJV_ERTEK_DONTES = {'Ézs 64:1': '64:1'}   # DT-F117c (2): az F91-szabály szerinti pár
P_URES, P_KIHAGY, P_OSSZEVON = 0.35, 0.35, 0.10
VERS = re.compile(r'^(.+) (\d+):(\d+)$')


def sorok(path):
    with open(path, encoding='utf-8') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if s and not s.startswith('#'):
                yield s.split('\t')


def strong(s):
    m = re.match(r'^H0*(\d+)', s.strip())
    return ('H' + m.group(1)) if m and int(m.group(1)) < 9000 else None


def konyv_tabla():
    return {p[1]: p[0] for p in sorok(os.path.join(K, 'Konyv_normalizalo_tabla.tsv')) if len(p) > 1}


def tahot(konyv):
    d = {}
    for p in sorok(os.path.join(K, 'TAHOT_kivonat.tsv')):
        m = VERS.match(p[0])
        if m and m.group(1) == konyv and len(p) > 1:
            x = strong(p[1])
            e = d.setdefault((int(m.group(2)), int(m.group(3))), [set(), 0])
            if x:
                e[0].add(x)
                e[1] += 1
    return d


def macula(konyv):
    d = {}
    fej = None
    for p in sorok(os.path.join(K, 'Macula_heber_%s.tsv' % MACULA[konyv])):
        if fej is None:
            fej = p
            ir, ist = fej.index('ref'), fej.index('strong')
            continue
        m = re.match(r'^\S+ (\d+):(\d+)!', p[ir])
        if not m:
            continue
        x = strong(p[ist])
        e = d.setdefault((int(m.group(1)), int(m.group(2))), [set(), 0])
        if x:
            e[0].add(x)
            e[1] += 1
    return d


def kjv_versszam(st):
    d = {}
    for p in sorok(os.path.join(K, 'KJV_Strongs_teljes.tsv')):
        m = re.match(r'^([^.]+)\.(\d+)\.(\d+)$', p[0])
        if m and m.group(1) == st:
            c, v = int(m.group(2)), int(m.group(3))
            d[c] = max(d.get(c, 0), v)
    return d


def jel(a, b, mod):
    ja = (len(a[0] & b[0]) / len(a[0] | b[0])) if (a[0] | b[0]) else 0.0
    if mod == 'jaccard':
        return ja
    import math
    r = max(1, a[1]) / max(1, b[1])
    return 0.7 * ja + 0.3 * math.exp(-abs(math.log(r)))


def egyesit(a, b):
    return [a[0] | b[0], a[1] + b[1]]


def igazit(kv, mv, mod):
    n, m = len(kv), len(mv)
    NEG = -1e9
    dp = [[NEG] * (m + 1) for _ in range(n + 1)]
    bt = [[None] * (m + 1) for _ in range(n + 1)]
    for j in range(m + 1):
        dp[0][j] = 0.0
    for i in range(1, n + 1):
        for j in range(m + 1):
            best, arg = dp[i - 1][j] - P_URES, '10'
            if j >= 1 and dp[i - 1][j - 1] > NEG:
                v = dp[i - 1][j - 1] + jel(kv[i - 1], mv[j - 1], mod)
                if v > best:
                    best, arg = v, '11'
            if j >= 2 and dp[i - 1][j - 2] > NEG:
                v = dp[i - 1][j - 2] + jel(kv[i - 1], egyesit(mv[j - 2], mv[j - 1]), mod) - P_OSSZEVON
                if v > best:
                    best, arg = v, '12'
            if i >= 2 and j >= 1 and dp[i - 2][j - 1] > NEG:
                v = dp[i - 2][j - 1] + jel(egyesit(kv[i - 2], kv[i - 1]), mv[j - 1], mod) - P_OSSZEVON
                if v > best:
                    best, arg = v, '21'
            if j >= 1 and dp[i][j - 1] > NEG:
                v = dp[i][j - 1] - P_KIHAGY
                if v > best:
                    best, arg = v, '01'
            dp[i][j], bt[i][j] = best, arg
    j = max(range(m + 1), key=lambda x: dp[n][x])
    i = n
    par = [None] * n
    kihagy = []
    while i > 0:
        op = bt[i][j]
        if op == '11':
            par[i - 1] = ((j - 1,), '1-1')
            i, j = i - 1, j - 1
        elif op == '12':
            par[i - 1] = ((j - 2, j - 1), '1-2')
            i, j = i - 1, j - 2
        elif op == '21':
            par[i - 1] = ((j - 1,), '2-1')
            par[i - 2] = ((j - 1,), '2-1')
            i, j = i - 2, j - 1
        elif op == '10':
            par[i - 1] = ((), 'nincs_par')
            i -= 1
        else:
            kihagy.append(j - 1)
            j -= 1
    return par, kihagy


def main():
    szoveg = '--szoveg' in sys.argv
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    hu2st = konyv_tabla()
    itelet = {p[0]: p[1] for p in sorok(ITELET) if p[0] != 'igehely_karoli'}
    osztaly = {p[0]: p[1] for p in sorok(OSSZEVET) if p[0] != 'igehely_karoli' and p[1] != 'kontextus'}
    assert len(itelet) == 346 and set(itelet) == set(osztaly)
    terv = {}
    for p in sorok(TERV):
        if p[0] != 'igehely_karoli':
            terv.setdefault(p[0], []).append(p[2] if len(p) > 2 else '')
    cel_fej = sorted({VERS.match(k).group(1) + ' ' + VERS.match(k).group(2) for k in itelet},
                     key=lambda x: (x.rsplit(' ', 1)[0], int(x.rsplit(' ', 1)[1])))
    cache = {}
    ki, ketseges, arva_ossz, elteres_lista = [], [], [], {}
    for fj in cel_fej:
        konyv, c = fj.rsplit(' ', 1)[0], int(fj.rsplit(' ', 1)[1])
        if konyv not in cache:
            st = hu2st[konyv]
            mc = macula(konyv)
            mt_db = {}
            for (cc, vv) in mc:
                mt_db[cc] = max(mt_db.get(cc, 0), vv)
            kj_db = kjv_versszam(st)
            elter = {cc for cc in set(mt_db) | set(kj_db) if mt_db.get(cc) != kj_db.get(cc)}
            elteres_lista[konyv] = (sorted(elter), mt_db, kj_db)
            cache[konyv] = (tahot(konyv), mc, elter)
        th, mc, elter = cache[konyv]
        kar_keys = [(cc, vv) for (cc, vv) in sorted(th) if c - 1 <= cc <= c + 1]
        mt_keys = [(cc, vv) for (cc, vv) in sorted(mc) if c - 2 <= cc <= c + 2]
        kv = [th[k] for k in kar_keys]
        mv = [mc[k] for k in mt_keys]
        pj, kih = igazit(kv, mv, 'jaccard')
        ph, _ = igazit(kv, mv, 'hossz')
        for x in kih:
            arva_ossz.append('%s: MT %d:%d' % (fj, mt_keys[x][0], mt_keys[x][1]))
        for i, (cc, vv) in enumerate(kar_keys):
            if cc != c:
                continue
            kk = '%s %d:%d' % (konyv, cc, vv)
            if kk not in itelet:
                continue
            idx_j, lep_j = pj[i]
            idx_h, lep_h = ph[i]
            mt_j = ';'.join('%d:%d' % mt_keys[x] for x in idx_j)
            mt_h = ';'.join('%d:%d' % mt_keys[x] for x in idx_h)
            if idx_j:
                ref = mv[idx_j[0]] if len(idx_j) == 1 else egyesit(mv[idx_j[0]], mv[idx_j[1]])
                ja = jel(kv[i], ref, 'jaccard')
            else:
                ja = 0.0
            kjv = KJV_ERTEK_DONTES.get(kk, itelet[kk])
            tv = [x for x in terv.get(kk, []) if x]
            tervezet = tv[0] if tv else ''
            if not tervezet:
                tviszony = 'uj'
            else:
                tviszony = 'egyezik' if tervezet == mt_j else 'javitott'
            ok = []
            if mt_j != mt_h:
                ok.append('a két igazítás eltér (jaccard=%s, hossz=%s)' % (mt_j or '-', mt_h or '-'))
            if lep_j != '1-1':
                ok.append('lépés %s' % lep_j)
            if mt_j == kjv:
                kviszony = 'mt=kjv'
            else:
                mt_c = int(mt_j.split(';')[0].split(':')[0]) if mt_j else None
                kj_c = int(kjv.split(';')[0].split(':')[0])
                ismert = any(x in elter for x in {mt_c, kj_c} | {kj_c - 1, kj_c + 1} | ({mt_c - 1, mt_c + 1} if mt_c else set()) if x)
                kviszony = 'ismert_elteres' if ismert else 'KEZI_OLVASAS'
                if not ismert:
                    ok.append('MT≠KJV ismert eltérés-fejezeten kívül')
            if ok:
                ketseges.append((kk, mt_j, mt_h, kjv, tervezet, '; '.join(ok)))
            ki.append('\t'.join([kk, osztaly[kk], kjv, mt_j, mt_h, lep_j, '%.2f' % ja, tervezet, tviszony, kviszony,
                                 '; '.join(ok) or 'rendben',
                                 'scope=gepi:%s (blokk) | forras=TAHOT_kivonat.tsv+Macula_heber_%s.tsv(ref)+naplok/F117_itelet.tsv '
                                 '| eszkoz=naplok/F117_mt_levezet.py | ts=%s' % (fj, MACULA[konyv], ts)]))
            if szoveg and (ok or kviszony != 'mt=kjv' or tviszony == 'javitott'):
                print('%s [%s] MT=%s (hossz: %s, %s, J=%.2f) | KJV=%s | tervezet=%s (%s) | %s | %s' % (
                    kk, osztaly[kk], mt_j, mt_h, lep_j, ja, kjv, tervezet or '-', tviszony, kviszony, '; '.join(ok) or 'rendben'))
    assert len(ki) == 346, len(ki)
    elt_leiras = '; '.join('%s: %s' % (k, ','.join(str(x) for x in v[0])) for k, v in sorted(elteres_lista.items()))
    fejlec = [
        '# F117.3 (DT-F117d (c)): az igehely_mt levezetése az A–D′ célhalmaz 346 Károli-versére (a Karoli_versmegfeleltetes.tsv és a Macula `karoli` oszlopa nélkül)',
        '# proveniencia: scope=A–D′ (346 Károli-vers, %d fejezet, blokk: Károli c-1..c+1 ↔ MT c-2..c+2) | forras=TAHOT_kivonat.tsv + '
        'Macula_heber_*.tsv (ref) + KJV_Strongs_teljes.tsv (versszám) + naplok/F117_itelet.tsv (KJV-pár) + naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv '
        '(összevetés) | eszkoz=naplok/F117_mt_levezet.py | n=346 | ts=%s' % (len(cel_fej), ts),
        '# ismert MT≠KJV fejezetek (a Macula-MT és a KJV versszáma eltér; adatból számolva): %s' % elt_leiras,
        '# árva MT-vers a blokkokban: %s' % ('; '.join(arva_ossz) or 'nincs'),
        '\t'.join(['igehely_karoli', 'osztaly', 'kjv_par', 'mt_jaccard', 'mt_hossz', 'lepes', 'jaccard', 'tervezet_mt',
                   'tervezet_viszony', 'kjv_viszony', 'ketseg', 'proveniencia']),
    ]
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(fejlec + ki) + '\n')
    from collections import Counter
    print('írva: %s (%d sor)' % (KIMENET, len(ki)))
    print('tervezet:', dict(Counter(s.split('\t')[8] for s in ki)))
    print('KJV-viszony:', dict(Counter(s.split('\t')[9] for s in ki)))
    print('lépés:', dict(Counter(s.split('\t')[5] for s in ki)))
    print('árva MT:', arva_ossz or 'nincs')
    print('kétséges: %d' % len(ketseges))
    for k in ketseges:
        print('  ', ' | '.join(k))


if __name__ == '__main__':
    main()
