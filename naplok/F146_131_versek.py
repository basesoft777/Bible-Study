"""F146.1 (brief 2.3): a #131 DBH-mérésének 12 ÓSZ-verse — a táblabeli MT-megfeleltetés helyes-e (Macula `ref` mint tanú).

Versenként: a tábla sora; a `lexikon_general.karoli_mt_vers` MT-verse (ahogy a render látja); a Macula-`ref` szerinti
legjobb MT-vers (Strong-Jaccard a TAHOT Károli-versével, a Károli-fejezet ±1 fejezetének MT-versei közül; a Macula
`karoli` oszlopa nélkül); a DBH-hivatkozások száma a táblabeli és a mért MT-versen. Csak olvas; stdout.
Futtatás: python naplok/F146_131_versek.py
"""
import os
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'naplok'))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import F117_mt_levezet as L  # noqa: E402
import F146_mt_felmeres as F  # noqa: E402
import lexikon_general as LG  # noqa: E402

VERSEK = ['Ézs 7:11', '1Móz 4:10', '1Krón 20:6', '1Krón 20:8', '1Móz 14:19', '1Móz 14:20', 'Jób 41:32',
          'Préd 9:12', '4Móz 13:34', 'Jób 38:7', 'Jób 38:16', 'Jób 38:30']


def main():
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    tabla = {p[0]: p for p in L.sorok(F.TABLA)}
    mfaj = F.macula_fajlok()
    th_all = F.tahot_mind()
    dbh = {}
    for p in L.sorok(os.path.join(F.K, 'UBS_DBH_referenciak.tsv')):
        if p[0] != 'lexid':
            dbh.setdefault(p[2], []).append(p[1])
    mc_cache = {}
    for kk in VERSEK:
        m = F.VERS.match(kk)
        konyv, c, v = m.group(1), int(m.group(2)), int(m.group(3))
        if konyv not in mc_cache:
            mc_cache[konyv] = F.macula(mfaj[konyv])
        mc = mc_cache[konyv]
        kv = th_all[konyv].get((c, v))
        sor = tabla.get(kk)
        mt_tabla, ok = LG.karoli_mt_vers(kk)
        jel = sorted(((L.jel(kv, e, 'jaccard'), k) for k, e in mc.items() if abs(k[0] - c) <= 1),
                     reverse=True)[:2] if kv else []
        legjobb = '%s %d:%d' % (konyv, jel[0][1][0], jel[0][1][1]) if jel else '-'
        print('%s | tábla: %s | render-MT: %s %s | mért MT: %s (J=%.2f; 2.: %s J=%.2f) | DBH@render-MT: %d | DBH@mért: %d' % (
            kk, '|'.join(sor[1:5]) if sor else 'NINCS SOR', mt_tabla or '-', ('(' + ok + ')') if ok else '',
            legjobb, jel[0][0] if jel else 0, ('%d:%d' % jel[1][1]) if len(jel) > 1 else '-', jel[1][0] if len(jel) > 1 else 0,
            len(dbh.get(mt_tabla, [])) if mt_tabla else 0, len(dbh.get(legjobb, []))))
    print('proveniencia: scope=12 vers (#131 DBH-mérés, brief 2.3) | forras=Karoli_versmegfeleltetes.tsv+TAHOT_kivonat.tsv'
          '+Macula_heber_*.tsv(ref)+UBS_DBH_referenciak.tsv | eszkoz=naplok/F146_131_versek.py | ts=%s' % ts)


if __name__ == '__main__':
    main()
