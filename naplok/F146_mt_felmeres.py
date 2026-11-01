"""F146.1 (VERSMEGF_MT_JAVITAS, brief 2.1–2.2): az `igehely_mt` mérése a Karoli_versmegfeleltetes.tsv minden
ÓSZ-beli `KJV` és `KEZI` osztályú, üres `igehely_mt`-jű sorára (a DT207 (c) módszerével, az F117-eszköz kiterjesztése).

Tanúk (a versmegfeleltető tábla `igehely_mt`-je és a Macula `karoli` oszlopa NÉLKÜL; a `karoli` oszlop csak a
fájl→könyv hozzárendelésre kell, tanúként nem):
  * Károli-oldal: konkordancia/TAHOT_kivonat.tsv (Károli-kulcs, F85) — a vers héber Strong-halmaza és szószáma;
  * MT-oldal: konkordancia/Macula_heber_<könyv>.tsv `ref` oszlopa (MT-számozás).
Igazítás: naplok/F117_mt_levezet.py `igazit` (Strong-Jaccard és Jaccard+szószám, monoton DP), blokk: Károli c-1..c+1 ↔
MT c-2..c+2. Független ellenőrzés: a KJV-versszám (KJV_Strongs_teljes.tsv) — az MT≠Károli eltérés gépileg csak ott
fogadható el, ahol a Macula-MT és a KJV fejezethossza eltér (± a szomszéd fejezet); máshol `KEZI_OLVASAS`.

Kimenet: naplok/F146_mt_felmeres.tsv — csak a mért eltérések (MT ≠ Károli) és a kétséges sorok, proveniencia-sorral;
összegzés a stdout-ra. Nem ír táblát. Futtatás: python naplok/F146_mt_felmeres.py
TSV-olvasás split('\\t'), írás '\\t'.join (a csv modul nélkül).
"""
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'naplok'))
import F117_mt_levezet as L  # noqa: E402  (igazit, jel, egyesit, strong, sorok)

K = os.path.join(ROOT, 'konkordancia')
TABLA = os.path.join(K, 'Karoli_versmegfeleltetes.tsv')
KIMENET = os.path.join(ROOT, 'naplok', 'F146_mt_felmeres.tsv')
VERS = L.VERS


def macula_fajlok():
    """-> {magyar könyvnév: fájlnév} (a `karoli` oszlop első értékéből; csak hozzárendelés, nem tanú)."""
    out = {}
    for fn in sorted(os.listdir(K)):
        if not (fn.startswith('Macula_heber_') and fn.endswith('.tsv')):
            continue
        fej = None
        for p in L.sorok(os.path.join(K, fn)):
            if fej is None:
                fej = p
                continue
            m = VERS.match(p[fej.index('karoli')].split(';')[0])
            if m:
                out[m.group(1)] = fn
                break
    return out


def macula(fn):
    d = {}
    fej = None
    for p in L.sorok(os.path.join(K, fn)):
        if fej is None:
            fej = p
            ir, ist = fej.index('ref'), fej.index('strong')
            continue
        m = re.match(r'^\S+ (\d+):(\d+)!', p[ir])
        if not m:
            continue
        x = L.strong(p[ist])
        e = d.setdefault((int(m.group(1)), int(m.group(2))), [set(), 0])
        if x:
            e[0].add(x)
            e[1] += 1
    return d


def tahot_mind():
    d = defaultdict(dict)
    for p in L.sorok(os.path.join(K, 'TAHOT_kivonat.tsv')):
        m = VERS.match(p[0])
        if m and len(p) > 1:
            x = L.strong(p[1])
            e = d[m.group(1)].setdefault((int(m.group(2)), int(m.group(3))), [set(), 0])
            if x:
                e[0].add(x)
                e[1] += 1
    return d


def kjv_mind():
    d = defaultdict(dict)
    for p in L.sorok(os.path.join(K, 'KJV_Strongs_teljes.tsv')):
        m = re.match(r'^([^.]+)\.(\d+)\.(\d+)$', p[0])
        if m:
            c, v = int(m.group(2)), int(m.group(3))
            d[m.group(1)][c] = max(d[m.group(1)].get(c, 0), v)
    return d


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    hu2st = L.konyv_tabla()
    hu2st.setdefault('Sir', hu2st.get('JSir'))   # a Károli-tábla és a TAHOT `Sir`, a normalizáló `JSir`
    mfaj = macula_fajlok()
    tabla = {}
    for p in L.sorok(TABLA):
        if p[0] == 'igehely_karoli':
            continue
        tabla[p[0]] = p
    cel = {k: p for k, p in tabla.items()
           if p[3] in ('KJV', 'KEZI') and p[2] == '' and VERS.match(k) and VERS.match(k).group(1) in mfaj}
    # a kitöltött igehely_mt-jű sorok (MT, és a KEZI kitöltve): csak jelentés (brief 2.2: „ide tartozik az Ézs 9”)
    kit = {k: p for k, p in tabla.items()
           if p[2] != '' and VERS.match(k) and VERS.match(k).group(1) in mfaj}
    th_all = tahot_mind()
    kj_all = kjv_mind()
    fejezetek = sorted({(VERS.match(k).group(1), int(VERS.match(k).group(2))) for k in list(cel) + list(kit)})
    print('célhalmaz: %d sor (KJV %d, KEZI %d), %d fejezet, %d könyv' % (
        len(cel), sum(1 for p in cel.values() if p[3] == 'KJV'), sum(1 for p in cel.values() if p[3] == 'KEZI'),
        len(fejezetek), len({f[0] for f in fejezetek})))
    cache = {}
    ki, stat, konyv_stat = [], Counter(), Counter()
    for konyv, c in fejezetek:
        if konyv not in cache:
            mc = macula(mfaj[konyv])
            mt_db = {}
            for (cc, vv) in mc:
                mt_db[cc] = max(mt_db.get(cc, 0), vv)
            kj_db = kj_all.get(hu2st[konyv], {})
            elter = {cc for cc in set(mt_db) | set(kj_db) if mt_db.get(cc) != kj_db.get(cc)}
            cache = {konyv: (th_all[konyv], mc, elter)}
        th, mc, elter = cache[konyv]
        kar_keys = [k for k in sorted(th) if c - 1 <= k[0] <= c + 1]
        mt_keys = [k for k in sorted(mc) if c - 2 <= k[0] <= c + 2]
        kv = [th[k] for k in kar_keys]
        mv = [mc[k] for k in mt_keys]
        pj, _ = L.igazit(kv, mv, 'jaccard')
        ph, _ = L.igazit(kv, mv, 'hossz')
        for i, (cc, vv) in enumerate(kar_keys):
            kk = '%s %d:%d' % (konyv, cc, vv)
            if cc != c or (kk not in cel and kk not in kit):
                continue
            kar = '%d:%d' % (cc, vv)
            idx_j, lep_j = pj[i]
            idx_h, _ = ph[i]
            mt_j = ';'.join('%d:%d' % mt_keys[x] for x in idx_j)
            mt_h = ';'.join('%d:%d' % mt_keys[x] for x in idx_h)
            if kk in kit:
                row = kit[kk]
                stat['kitoltott_mert'] += 1
                if mt_j == row[2] and mt_h == row[2] and lep_j == '1-1':
                    continue
                a = 'kitoltott_elteres' if (mt_j == mt_h and lep_j == '1-1') else 'kitoltott_ketseges'
                stat[a] += 1
                konyv_stat[(konyv, a)] += 1
                ja = 0.0
                if idx_j:
                    ref = mv[idx_j[0]] if len(idx_j) == 1 else L.egyesit(mv[idx_j[0]], mv[idx_j[1]])
                    ja = L.jel(kv[i], ref, 'jaccard')
                ki.append('	'.join([konyv, str(cc), str(vv), kk, row[3], row[1], mt_j, mt_h, lep_j, '%.2f' % ja, '',
                                     a, 'csak jelent (a tábla igehely_mt-je: %s; a 2.2 hatókörén kívül)' % row[2],
                                     'lépés %s' % lep_j if lep_j != '1-1' else 'rendben',
                                     'scope=gepi:%s %d | forras=TAHOT_kivonat.tsv+%s(ref) | eszkoz=naplok/F146_mt_felmeres.py | ts=%s'
                                     % (konyv, c, mfaj[konyv], ts)]))
                continue
            stat['mert'] += 1
            if idx_j:
                ref = mv[idx_j[0]] if len(idx_j) == 1 else L.egyesit(mv[idx_j[0]], mv[idx_j[1]])
                ja = L.jel(kv[i], ref, 'jaccard')
            else:
                ja = 0.0
            ja_id = L.jel(kv[i], mc[(cc, vv)], 'jaccard') if (cc, vv) in mc else None
            ok = []
            if mt_j != mt_h:
                ok.append('a két igazítás eltér (jaccard=%s, hossz=%s)' % (mt_j or '-', mt_h or '-'))
            if lep_j != '1-1':
                ok.append('lépés %s' % lep_j)
            row = cel[kk]
            kjv = row[1]
            if mt_j == kar and not ok:
                stat['egyezik'] += 1
                if row[3] == 'KEZI' and kjv == kar:
                    # KEZI-sor, amelyben Károli = KJV = mért MT: a render nem párosítja (üres igehely_mt) — csak jelent
                    stat['kezi_azonos'] += 1
                    konyv_stat[(konyv, 'kezi_azonos')] += 1
                    ki.append('\t'.join([konyv, str(cc), str(vv), kk, row[3], kjv, mt_j, mt_h, lep_j, '%.2f' % ja,
                                         '' if ja_id is None else '%.2f' % ja_id, 'kezi_azonos',
                                         'csak jelent (KEZI, Károli = KJV = MT; a 2.2 hatókörén kívül)', 'rendben',
                                         'scope=gepi:%s %d | forras=TAHOT_kivonat.tsv+%s(ref) | eszkoz=naplok/F146_mt_felmeres.py | ts=%s'
                                         % (konyv, c, mfaj[konyv], ts)]))
                continue
            # a KJV-pár (a tábla igehely_kjv-je) független tanú: ha a mért MT azonos vele, az eltérés igazolt
            if mt_j and mt_j != kar and mt_j != kjv:
                mt_c = int(mt_j.split(';')[0].split(':')[0])
                ismert = any(x in elter for x in {mt_c - 1, mt_c, mt_c + 1, cc - 1, cc, cc + 1})
                if not ismert:
                    ok.append('MT≠Károli ismert MT≠KJV fejezeten kívül (KEZI_OLVASAS)')
            if mt_j == kar:
                javaslat = 'marad (kétséges igazítás, MT=Károli)'
            elif not ok:
                if kjv == kar:
                    javaslat = 'KEZI + igehely_mt (Károli = KJV ≠ MT; új kombináció)'
                elif mt_j == kjv:
                    javaslat = 'KEZI + igehely_mt (Károli ≠ KJV = MT)'
                else:
                    javaslat = 'KEZI + igehely_mt (Károli ≠ KJV ≠ MT)'
            else:
                javaslat = 'kétséges: tételes lista'
            allapot = 'elteres' if (mt_j != kar and not ok) else 'ketseges'
            stat[allapot] += 1
            konyv_stat[(konyv, allapot)] += 1
            ki.append('\t'.join([konyv, str(cc), str(vv), kk, row[3], kjv, mt_j, mt_h, lep_j, '%.2f' % ja,
                                 '' if ja_id is None else '%.2f' % ja_id, allapot, javaslat, '; '.join(ok) or 'rendben',
                                 'scope=gepi:%s %d (blokk: Károli c-1..c+1 ↔ MT c-2..c+2) | forras=TAHOT_kivonat.tsv+%s(ref)'
                                 '+KJV_Strongs_teljes.tsv(versszám) | eszkoz=naplok/F146_mt_felmeres.py | ts=%s'
                                 % (konyv, c, mfaj[konyv], ts)]))
    fejlec = [
        '# F146.1 (DT207 (c) módszer): az igehely_mt mérése a Karoli_versmegfeleltetes.tsv ÓSZ-beli KJV/KEZI, üres igehely_mt-jű '
        'soraira; csak az MT≠Károli eltérések és a kétséges sorok (a Macula `karoli` oszlopa tanúként kizárva)',
        '# proveniencia: scope=%d sor, %d fejezet | forras=TAHOT_kivonat.tsv + Macula_heber_*.tsv (ref) + KJV_Strongs_teljes.tsv '
        '| eszkoz=naplok/F146_mt_felmeres.py | ts=%s' % (stat['mert'], len(fejezetek), ts),
        '# jaccard = a mért pár Strong-Jaccardja; jaccard_azonos = a Károli-vers és az azonos számú MT-vers Jaccardja',
        '\t'.join(['konyv', 'fejezet', 'vers', 'igehely_karoli', 'osztaly', 'igehely_kjv', 'mt_jaccard', 'mt_hossz', 'lepes',
                   'jaccard', 'jaccard_azonos', 'allapot', 'osztaly_javaslat', 'ketseg', 'proveniencia']),
    ]
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(fejlec + ki) + '\n')
    print('írva: %s (%d sor)' % (KIMENET, len(ki)))
    print('összesen:', dict(stat))
    for (kv_, a), n in sorted(konyv_stat.items()):
        print('  %s %s: %d' % (kv_, a, n))


if __name__ == '__main__':
    main()
