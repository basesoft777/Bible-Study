"""F91 M2 (A-oldal): a konkordancia/Karoli_versmegfeleltetes.tsv javítása a feliratos zsoltárokra.

Szabály (DT-F91a, A1; DT-F91c): a feliratos zsoltárokban (62 zsoltár, d = Károli-max - KJV-max > 0, plusz Zsolt 13
kivétel) az `igehely_kjv` = a Karoli_1908-kulcsú LXX_OS-etalon KJV-értéke (v > d); v <= d (felirat): üres,
a megjegyzésben "felirat" / "felirat 2 vers". A d-szabály (c:(v-d)) csak ellenőrzés.
Ha az etalon egy Károli-versre több KJV-verset ad (Zsolt 13:6 = KJV 13:5-6), az `igehely_kjv` az ELSŐ KJV-vers
(`;`-os érték a táblába nem kerülhet, DT-F91c), a megjegyzésben a teljes etalon-érték áll.
Írás: '\\t'.join, olvasás split('\\t') (a csv modul tilos). Idempotens. Nem érintett sor bájtra azonos.

Két használati mód (az eszközök egy helyen élnek):
  * a naplok/KAROLI_KK4_tabla_veglegesit.py generátor importálja és a `javit()`-ot hívja (a tábla forrása);
  * önállóan: python eszkozok/f91_versmegf_javit.py [--ir]   (--ir nélkül csak mér; a repó táblájára ír)
"""
import sys
import re
import os
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'konkordancia')
TABLA = os.path.join(K, 'Karoli_versmegfeleltetes.tsv')
# Rögzített időbélyeg: a SZABÁLY dátuma (az F91 A1-javítás időbélyege), nem a futásé; így a generátor kimenete determinisztikus.
TS = '2026-10-14'
JEGYZET_ELO = '# F91 javítás'


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        data = f.read()
    return data.split('\n')


def _kjv_sorrend(x):
    m = re.fullmatch(r'(\d+):(\d+)', x)
    return (int(m.group(1)), int(m.group(2)))


def etalon_betolt():
    """-> (dd, et, kivetel): dd = {zsoltár: d}, et = {zsoltár: {károli_vers: {KJV-értékek}}}."""
    kar = defaultdict(set)
    for ln in rows(os.path.join(K, 'Karoli_1908.tsv')):
        m = re.match(r'Zsolt (\d+):(\d+)\t', ln)
        if m:
            kar[int(m.group(1))].add(int(m.group(2)))
    kjv = defaultdict(set)
    for ln in rows(os.path.join(K, 'KJV_Strongs_teljes.tsv')):
        m = re.match(r'Psa\.(\d+)\.(\d+)\t', ln)
        if m:
            kjv[int(m.group(1))].add(int(m.group(2)))
    d = {c: max(kar[c]) - max(kjv[c]) for c in range(1, 151)}

    et = defaultdict(lambda: defaultdict(set))
    for ln in rows(os.path.join(K, 'LXX_OS', 'psalms-lxx.tsv')):
        p = ln.split('\t')
        if len(p) < 4:
            continue
        m = re.fullmatch(r'Zsolt (\d+):(\d+)', p[2])
        if m and p[1]:
            for x in p[1].split(';'):
                et[int(m.group(1))][int(m.group(2))].add(x)

    def etalon_d(c):
        best = 0
        for v, s in et[c].items():
            if len(s) == 1:
                m = re.fullmatch(r'(\d+):(\d+)', next(iter(s)))
                if m and int(m.group(1)) == c:
                    best = max(best, v - int(m.group(2)))
        return best

    erintett = [c for c in range(1, 151) if d[c] > 0 or etalon_d(c) > 0]
    dd = {c: (d[c] if d[c] > 0 else etalon_d(c)) for c in erintett}
    kivetel = [c for c in erintett if d[c] == 0]
    return dd, et, kivetel


def kivalaszt(dd, et, c, v):
    """-> (kjv_ertek, megjegyzes) a javított sorhoz; kjv_ertek None = etalon-hiány."""
    dc = dd[c]
    if v <= dc:
        return '', ('felirat' if dc == 1 else 'felirat %d vers' % dc)
    s = et[c].get(v)
    if not s:
        return None, 'etalon_hiany'
    tag = sorted(s, key=_kjv_sorrend)
    if len(tag) == 1:
        return tag[0], ''
    # DT-F91c: több KJV-vers egy Károli-versben -> az első; a teljes etalon-érték a megjegyzésben
    elso, utolso = tag[0], tag[-1]
    return elso, 'KJV %s–%s egy Károli-versben (etalon: %s)' % (elso, utolso.split(':')[1], ';'.join(tag))


def elteres(dd, et, sorok):
    """Az etalonnal való eltérések száma (összes, ebből Zsolt 22). Pontosvesszős érték mindig hiba."""
    n = 0
    zs22 = 0
    for l in sorok:
        p = l.split('\t')
        if len(p) < 6:
            continue
        m = re.fullmatch(r'Zsolt (\d+):(\d+)', p[0])
        if not m or int(m.group(1)) not in dd:
            continue
        c, v = int(m.group(1)), int(m.group(2))
        if v <= dd[c]:
            ok = p[1] == ''
        else:
            s = et[c].get(v)
            ok = bool(s) and ';' not in p[1] and p[1] == sorted(s, key=_kjv_sorrend)[0]
        if not ok:
            n += 1
            if c == 22:
                zs22 += 1
    return n, zs22


def _zsolt_erintett(dd, l):
    m = re.match(r'Zsolt (\d+):', l)
    return bool(m) and int(m.group(1)) in dd


def javit(lines, ts=TS, naplo=print):
    """A tábla sorainak (sorvég nélkül) javítása -> az új sorok listája. Védőellenőrzésekkel."""
    dd, et, kivetel = etalon_betolt()
    erintett = sorted(dd)
    naplo('érintett zsoltár: %d | d=1: %d | d=2: %s | kivétel (d=0, etalon>0): %s' % (
        len(erintett), sum(1 for c in erintett if dd[c] == 1),
        [c for c in erintett if dd[c] == 2], kivetel))

    ujak = list(lines)
    valt = 0
    etalon_hiany = []
    d_szabaly_elter = []
    for i, ln in enumerate(lines):
        p = ln.split('\t')
        if len(p) < 6:
            continue
        m = re.fullmatch(r'Zsolt (\d+):(\d+)', p[0])
        if not m or int(m.group(1)) not in dd:
            continue
        c, v = int(m.group(1)), int(m.group(2))
        ertek, megj = kivalaszt(dd, et, c, v)
        if ertek is None:
            etalon_hiany.append(p[0])
            continue
        if v > dd[c] and ertek != '%d:%d' % (c, v - dd[c]):
            d_szabaly_elter.append((p[0], ertek, '%d:%d' % (c, v - dd[c])))
        if p[1] != ertek or p[5] != megj or p[4] != 'lxx_os_etalon_f91':
            q = list(p)
            q[1] = ertek
            q[4] = 'lxx_os_etalon_f91'
            q[5] = megj
            ujak[i] = '\t'.join(q)
            valt += 1

    naplo('módosuló sor: %d | etalon-hiány: %d %s | d-szabálytól eltérő sor: %d %s' % (
        valt, len(etalon_hiany), etalon_hiany[:5], len(d_szabaly_elter), d_szabaly_elter[:5]))
    assert not etalon_hiany, 'etalon-hiány: megállok'

    jegyzet = (JEGYZET_ELO + ' (DT-F91a, A1; DT-F91c): a feliratos zsoltárok (%d) igehely_kjv oszlopa az LXX_OS '
               'Károli-kulcsú etalonból; felirat-versek (v <= d) üres KJV, megjegyzés "felirat"; ahol egy Károli-versben '
               'több KJV-vers áll (Zsolt 13:6), az első KJV-vers, `;`-os érték nincs; '
               'forras=lxx_os_etalon_f91 | forras=eszkozok/f91_versmegf_javit.py | ts=%s (a szabály dátuma, nem a futásé)' % (len(erintett), ts))
    ujak = [l for l in ujak if not l.startswith(JEGYZET_ELO)]
    idx = max(i for i, l in enumerate(ujak) if l.startswith('#'))
    ujak.insert(idx + 1, jegyzet)

    # védőellenőrzés: minden nem érintett sor bájtra azonos, a sorszám nem változik
    def nem_erintett(sorok):
        return [l for l in sorok if not l.startswith(JEGYZET_ELO) and not _zsolt_erintett(dd, l)]
    assert nem_erintett(lines) == nem_erintett(ujak), 'nem érintett sor változott: megállok'
    assert len([l for l in lines if not l.startswith(JEGYZET_ELO)]) == len([l for l in ujak if not l.startswith(JEGYZET_ELO)])

    e_elo, e_utan = elteres(dd, et, lines), elteres(dd, et, ujak)
    naplo('eltérés az etalonnal ELŐTTE (összes érintett, ebből Zsolt 22): %s' % (e_elo,))
    naplo('eltérés az etalonnal UTÁNA: %s' % (e_utan,))
    assert e_utan == (0, 0), 'etalon-eltérés a javítás után: megállok'
    pontosvesszo = [l for l in ujak if not l.startswith('#') and len(l.split('\t')) > 1 and ';' in l.split('\t')[1]]
    assert not pontosvesszo, '`;`-os igehely_kjv érték a táblában: %s' % pontosvesszo[:3]
    return ujak


if __name__ == '__main__':
    ir = '--ir' in sys.argv
    sorok = rows(TABLA)
    uj = javit(sorok)
    if ir:
        with open(TABLA, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(uj))
        print('írva:', TABLA)
