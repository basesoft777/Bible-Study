"""F131.3.14: a `adat/bdb_vers_jelentes.tsv` kinyerőjének tartomány-hibája — hatásmérés, csak olvas.

Hiba (DT-F131f 1. javítókör (b)): a `eszkozok/olvaso_szerver/bdb_szelet.py` `hivatkozasok()` a kiírt hivatkozás
utáni kötőjeles verstartományt („1Kin 18:24-25, 26”) nem kezeli: a `_FOLYTATAS` minta a token végén várja a
„, <vers>” folytatást, ezért a tartomány („-25”) után álló folytatás („, 26”) elvész, és a tartomány második
tagja sem kerül a táblába. A kinyerő és a tábla a #99 / #102 (BDB_SZELETELO_JAVITAS) tárgya, a #131 `ir`-én
kívül: ez a szkript NEM írja át őket; a javítás két változatát a memóriában méri a teljes táblán.

  A változat: a kiírt (vagy örökölt) hivatkozás utáni „-N” tartomány átlépése után a folytatás-keresés
              ugyanúgy fut, mint tartomány nélkül (a tartományt nem bontja ki; a „, 26” sor létrejön).
  B változat: A + a kötőjeles tartomány kibontása versenként (a hivatkozás és a folytatás tartománya is;
              „18:24-25” → 18:24, 18:25), azonos fejezeten belül.

Kimenet (stdout): soronként a régi és az új tábla összevetése (sorszámok a `general()` szerint), a hozzáadott
sorok száma, az érintett szócikkek és igehelyek száma, a sorszám-eltolódás; mintasorok; a H7121/H8034 eredménye.
TSV `split('\\t')`. Futásidő: a teljes tábla újragenerálása kétszer.

    python naplok/F131_bdb_tartomany_meres.py
"""
import collections
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok', 'olvaso_szerver'))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import bdb_szelet as B  # noqa: E402
import bdb_vers_jelentes as V  # noqa: E402

EREDETI = B.hivatkozasok
TARTOMANY = re.compile(r'\s*[-–]\s*(\d{1,3})(?![\d:])')
FOLYT_TART = re.compile(r'\s*,\s*(\d{1,3})\s*[-–]\s*(\d{1,3})(?=[\s,;.)\]]|$)(?!\s*:)')


def javitott(valtozat):
    def hivatkozasok(szoveg):
        s = B.lapit(szoveg)
        ki = EREDETI(szoveg)
        meglevo = {h['poz'] for h in ki}
        uj = []
        for h in ki:
            uj.append(h)
            if h['konyv_mod'] == 'folytatas':
                if valtozat == 'B':
                    m = FOLYT_TART.match(s, h['poz'] - (len(s[:h['poz']]) - len(s[:h['poz']].rstrip(' ,'))))
                    m2 = re.match(r'(\d{1,3})\s*[-–]\s*(\d{1,3})', s[h['poz']:])
                    if m2 and int(m2.group(2)) > h['v']:
                        for v in range(h['v'] + 1, int(m2.group(2)) + 1):
                            uj.append(dict(h, v=v, konyv_mod='tartomany', nyers='%s (tartomány)' % m2.group(0)))
                continue
            t = TARTOMANY.match(s, h['veg'])
            if not t:
                continue
            veg = int(t.group(1))
            if valtozat == 'B' and veg > h['v']:
                for v in range(h['v'] + 1, veg + 1):
                    uj.append(dict(h, v=v, konyv_mod='tartomany', nyers='%s%s (tartomány)' % (h['nyers'], t.group(0))))
            q = t.end()
            while True:
                f = B._FOLYTATAS.match(s, q)
                if not f or f.start(1) in meglevo:
                    break
                uj.append({'poz': f.start(1), 'veg': f.end(), 'nyers': f.group(0).strip(), 'konyv': h['konyv'],
                           'c': h['c'], 'v': int(f.group(1)), 'konyv_mod': 'folytatas', 'okkod': h['okkod']})
                if valtozat == 'B':
                    m2 = re.match(r'(\d{1,3})\s*[-–]\s*(\d{1,3})', s[f.start(1):])
                    if m2 and int(m2.group(2)) > int(f.group(1)):
                        for v in range(int(f.group(1)) + 1, int(m2.group(2)) + 1):
                            uj.append({'poz': f.start(1), 'veg': f.end(), 'nyers': '%s (tartomány)' % m2.group(0),
                                       'konyv': h['konyv'], 'c': h['c'], 'v': v, 'konyv_mod': 'tartomany',
                                       'okkod': h['okkod']})
                q = f.end()
        return uj
    return hivatkozasok


def kulcs(r):
    # strong, poz, nyers, karoli_vers, utvonal (sorszám nélkül)
    return (r[0], r[3], r[4], r[7], r[11])


def osszevet(cim, regi, uj):
    print('\n## %s' % cim)
    rc = collections.Counter(kulcs(r) for r in regi)
    uc = collections.Counter(kulcs(r) for r in uj)
    plusz = uc - rc
    minusz = rc - uc
    print('sorok: régi %d, új %d; hozzáadott %d, elveszett %d' % (len(regi), len(uj), sum(plusz.values()),
                                                                 sum(minusz.values())))
    strongok = sorted({k[0] for k in plusz} | {k[0] for k in minusz})
    print('érintett szócikk: %d; új Károli-igehely (nem üres): %d' % (
        len(strongok), len({(k[0], k[3]) for k in plusz if k[3]})))
    regi_sz = {}
    for r in regi:
        regi_sz.setdefault(r[0], []).append((kulcs(r), r[2]))
    eltolt = 0
    for r in uj:
        for k, sz in regi_sz.get(r[0], []):
            if k == kulcs(r) and sz != r[2]:
                eltolt += 1
                break
    print('a régi sorok közül más sorszámot kap: %d' % eltolt)
    for k in sorted(plusz)[:12]:
        print('  + %s poz=%s %r → %s (%s)' % (k[0], k[1], k[2], k[3] or '—', k[4]))
    for st in ('H7121', 'H8034'):
        for k in sorted(plusz):
            if k[0] == st:
                print('  [arany] + %s %r → %s (%s)' % (st, k[2], k[3], k[4]))
    return plusz


def main():
    ts = '2026-10-16'
    print('proveniencia: scope=adat/bdb_vers_jelentes.tsv teljes újragenerálása a memóriában (A, B változat) | '
          'forras=naplok/F131_bdb_tartomany_meres.py; eszkozok/olvaso_szerver/bdb_vers_jelentes.py general() | ts=%s'
          % datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    regi, _ = V.general(ts)
    with open(os.path.join(GYOKER, 'adat', 'bdb_vers_jelentes.tsv'), encoding='utf-8') as f:
        tabla = [s.split('\t') for s in f.read().split('\n')[3:] if s]
    print('a commitolt tábla és a mai kód kimenete: %s (%d / %d sor)' % (
        'azonos' if [r[:14] for r in tabla] == [r[:14] for r in regi] else 'ELTÉR', len(tabla), len(regi)))
    for valtozat in ('A', 'B'):
        B.hivatkozasok = javitott(valtozat)
        try:
            uj, _ = V.general(ts)
        finally:
            B.hivatkozasok = EREDETI
        osszevet('%s változat' % valtozat, regi, uj)


if __name__ == '__main__':
    main()
