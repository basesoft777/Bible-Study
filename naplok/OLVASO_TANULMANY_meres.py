"""F149 M0 — a tanulmány-regiszter kinyerhetőségének mérése (csak olvas).

Méri: tartomány-kinyerés a fájlnevekből, sorozat-folytonosság, Károli-számozás
egyezése a 2. szakasz versei és a fájlnév között, a finom szint sűrűsége
(név szerinti szakasz-hivatkozás a tartomány verseire), átfedések,
a forras_tanulmany lefedettsége.

Proveniencia: scope=genezis/, ujszovetseg/, melyelemzesek/ | forras=manual
(eseti mérőszkript) | ts=2026-11-02
Használat: python naplok/OLVASO_TANULMANY_meres.py [kimenet.md]
"""
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KONYVEK = ('genezis', 'ujszovetseg', 'melyelemzesek')


def strip(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').lower()


def olvas_tsv(p):
    with open(p, encoding='utf-8') as f:
        return [l.rstrip('\r\n').split('\t') for l in f]


# --- Károli: versek könyv/fejezet szerint ---
karoli = {}      # (konyv, fej, vers) -> sorszam
sorrend = []
for r in olvas_tsv(ROOT / 'konkordancia/Karoli_1908.tsv')[1:]:
    m = re.match(r'^(\S+) (\d+):(\d+)$', r[0])
    if m:
        k = (m.group(1), int(m.group(2)), int(m.group(3)))
        karoli[k] = len(sorrend)
        sorrend.append(k)
verslista = defaultdict(list)
for k in sorrend:
    verslista[k[0]].append(k)

# --- könyvnevek ---
alias = {}
for r in olvas_tsv(ROOT / 'konkordancia/Konyv_normalizalo_tabla.tsv')[1:]:
    if len(r) >= 2 and r[1]:
        alias[strip(r[1])] = r[1]
        if len(r) >= 4:
            for a in r[3].split(','):
                if a.strip():
                    alias[strip(a.strip())] = r[1]
for a, k in (('rom', 'Róm'), ('zsolt', 'Zsolt'), ('zsoltarok', 'Zsolt'), ('mozes', None),
             ('romabeliekhez', 'Róm'), ('zsidokhoz', 'Zsid'), ('rom', 'Róm'),
             ('zsidok', 'Zsid'), ('roma', 'Róm'), ('1moz', '1Móz'), ('1mozes', '1Móz'),
             ('1thessz', '1Thessz'), ('lk', 'Luk'), ('jn', 'Ján'), ('apcsel', 'ApCsel')):
    if k:
        alias[a] = k
KONYV_TAR = {k for k in verslista}


def konyv_fajlnevbol(nev):
    return alias.get(strip(nev))


def tartomany_fajlnevbol(fn):
    """('genezis'|...) fájlnévből -> (könyv, kezdő(fej,vers), vég(fej,vers)) vagy None."""
    stem = fn.replace('_bovitett.md', '')
    m = re.match(r'^(\d?[A-Za-z]+)_(\d+)(?:v(\d+))?(?:-(?:(\d+)v)?(\d+))?$', stem)
    if not m:
        return None
    konyv = konyv_fajlnevbol(m.group(1))
    if not konyv:
        return None
    f1, v1, f2, v2 = m.group(2), m.group(3), m.group(4), m.group(5)
    f1 = int(f1)
    if v1 is None:                       # egész fejezet
        vs = [k for k in verslista[konyv] if k[1] == f1]
        if not vs:
            return None
        return konyv, (f1, vs[0][2]), (f1, vs[-1][2])
    v1 = int(v1)
    if v2 is None:                       # egy vers
        return konyv, (f1, v1), (f1, v1)
    if f2 is None:
        return konyv, (f1, v1), (f1, int(v2))
    return konyv, (f1, v1), (int(f2), int(v2))


def verskeszlet(konyv, kez, veg):
    a = karoli.get((konyv, kez[0], kez[1]))
    b = karoli.get((konyv, veg[0], veg[1]))
    if a is None or b is None:
        return None
    return sorrend[a:b + 1]


# --- igehely-hivatkozás kinyerése szövegből ---
KONYV_RE = r'(?:[123]\s?)?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]+\.?'
REF_RE = re.compile(
    r'(?:(?P<k>' + KONYV_RE + r')\s+)?(?P<f>\d{1,3}):(?P<v>\d{1,3})'
    r'(?:\s?[–-]\s?(?:(?P<f2>\d{1,3}):)?(?P<v2>\d{1,3}))?'
    r'(?P<lista>(?:\s?,\s?\d{1,3}(?!\d|:)(?:\s?[–-]\s?\d{1,3}(?!:))?)*)')


def hivatkozasok(szoveg, alap_konyv, kiterjeszt=True):
    """Generátor: (poz, könyv, fej, vers) minden megnevezett versre."""
    akt = alap_konyv
    kozos = []
    for m in REF_RE.finditer(szoveg):
        if m.group('k'):
            k = konyv_fajlnevbol(m.group('k').rstrip('.'))
            if k:
                akt = k
            else:
                kozos.append(m.group('k'))
                continue
        f, v = int(m.group('f')), int(m.group('v'))
        v2 = int(m.group('v2')) if m.group('v2') else None
        f2 = int(m.group('f2')) if m.group('f2') else f
        if v2 is None:
            vege = (f, v)
        else:
            vege = (f2, v2)
        a = karoli.get((akt, f, v))
        b = karoli.get((akt, vege[0], vege[1]))
        if a is not None and b is not None and a <= b <= a + 200:
            for k in (sorrend[a:b + 1] if kiterjeszt else {sorrend[a], sorrend[b]}):
                yield m.start(), k
        for x in re.findall(r'\d{1,3}(?:\s?[–-]\s?\d{1,3})?', m.group('lista') or ''):
            p = re.split(r'\s?[–-]\s?', x)
            lo, hi = int(p[0]), int(p[-1])
            for vv in (range(lo, hi + 1) if kiterjeszt else {lo, hi}):
                if (akt, f, vv) in karoli:
                    yield m.start(), (akt, f, vv)


def szakaszok(szoveg):
    """[(horgony_szint, cim, szoveg)] a ##/### címsorok szerint."""
    ki, cim, buf = [], None, []
    fo = [None]
    for sor in szoveg.split('\n'):
        m = re.match(r'^(#{2,3}) (.*)$', sor)
        if m:
            if cim is not None:
                ki.append((cim, '\n'.join(buf)))
            cim, buf = m.group(2).strip(), []
        elif cim is not None:
            buf.append(sor)
    if cim is not None:
        ki.append((cim, '\n'.join(buf)))
    return ki


def jel(k):
    return f'{k[0]} {k[1]}:{k[2]}'


def main():
    ki = []
    out = ki.append
    out('# F149 M0 — a tanulmány-regiszter mérése\n')
    out('*proveniencia: scope=genezis/, ujszovetseg/, melyelemzesek/, konkordancia/Karoli_1908.tsv, '
        'adat/elofordulasok.tsv | forras=manual (naplok/OLVASO_TANULMANY_meres.py, csak olvas) | ts=2026-11-02*\n')

    tanulmanyok = []   # dict
    hibak = []
    for d in ('genezis', 'ujszovetseg'):
        for p in sorted((ROOT / d).glob('*_bovitett.md')):
            t = tartomany_fajlnevbol(p.name)
            if not t:
                hibak.append(f'{d}/{p.name}: fájlnévből nem kinyerhető tartomány')
                continue
            konyv, kez, veg = t
            vs = verskeszlet(konyv, kez, veg)
            if vs is None:
                hibak.append(f'{d}/{p.name}: a tartomány vége/kezdete nincs a Károliban ({konyv} {kez}-{veg})')
                continue
            tanulmanyok.append(dict(fajl=f'{d}/{p.name}', tipus='bovitett', konyv=konyv, kez=kez, veg=veg, versek=vs, p=p))
    mely = sorted((ROOT / 'melyelemzesek').glob('*.md'))

    out('## 1. Kinyerhetőség (bővített, a fájlnévből)\n')
    out(f'- Bővített tanulmány: {len(tanulmanyok)} kinyerve, {len(hibak)} hibás.')
    for h in hibak:
        out(f'  - HIBA: {h}')
    out('\n| fájl | tartomány | versek |\n|---|---|---|')
    for t in tanulmanyok:
        k0, k1 = t['versek'][0], t['versek'][-1]
        out(f"| {t['fajl']} | {jel(k0)} – {jel(k1)} | {len(t['versek'])} |")

    # sorozat-folytonosság
    out('\n## 2. Sorozat-folytonosság (könyvenként)\n')
    for konyv in sorted({t['konyv'] for t in tanulmanyok}):
        ts = sorted((t for t in tanulmanyok if t['konyv'] == konyv),
                    key=lambda t: karoli[(konyv,) + t['kez']])
        hez = []
        for a, b in zip(ts, ts[1:]):
            ia = karoli[(konyv,) + a['veg']]
            ib = karoli[(konyv,) + b['kez']]
            if ib == ia + 1:
                continue
            if ib <= ia:
                hez.append(f"átfedés: {a['fajl']} ↔ {b['fajl']}")
            else:
                hez.append(f"hézag: {jel(sorrend[ia + 1])} – {jel(sorrend[ib - 1])} ({ib - ia - 1} vers) a {a['fajl']} és {b['fajl']} között")
        out(f'- **{konyv}**: {len(ts)} tanulmány; ' + ('hézag/átfedés nincs.' if not hez else ''))
        for h in hez:
            out(f'  - {h}')

    # 2. szakasz számozás-egyezés + finom szint
    out('\n## 3. Károli-számozás és a finom szint sűrűsége\n')
    out('A „2. szakasz” táblázatának `Vers` oszlopa a fájlnév tartományában van-e; és hány tartomány-vers kap név szerinti hivatkozást valamely szakaszban (a 2. szakasz táblázata nélkül, mert az nem szakasz-hivatkozás, hanem lexikai tábla).\n')
    out('| tanulmány | tartomány-versek | 2. szakasz tábla-verse | ebből tartományon kívül | hivatkozott (tartománnyal) | csak egyedi/végpont | arány (egyedi) | szakasz-szám |\n|---|---|---|---|---|---|---|')
    atfedes = defaultdict(list)
    for t in tanulmanyok:
        szov = t['p'].read_text(encoding='utf-8')
        szak = szakaszok(szov)
        halmaz = set(t['versek'])
        for k in halmaz:
            atfedes[k].append(t['fajl'])
        tabla_versek, kivul = 0, 0
        m2 = re.search(r'^## 2\..*?(?=^## 3\.)', szov, re.S | re.M)
        for sor in (m2.group(0).splitlines() if m2 else []):
            m = re.match(r'^\|\s*(?:(\d+):)?(\d+)(?:\s?[–-]\s?(?:(\d+):)?(\d+))?\s*\|', sor)
            if m:
                fej = int(m.group(1)) if m.group(1) else t['kez'][0]
                tabla_versek += 1
                if (t['konyv'], fej, int(m.group(2))) not in halmaz:
                    kivul += 1
        nevezett, szigoru = set(), set()
        for cim, sz in szak:
            if cim.startswith('2.'):
                continue
            for _, k in hivatkozasok(sz, t['konyv']):
                if k in halmaz:
                    nevezett.add(k)
            for _, k in hivatkozasok(sz, t['konyv'], False):
                if k in halmaz:
                    szigoru.add(k)
        out(f"| {t['fajl']} | {len(halmaz)} | {tabla_versek} | {kivul} | {len(nevezett)} | {len(szigoru)} | "
            f"{100 * len(szigoru) // max(1, len(halmaz))}% | {len(szak)} |")

    # mélyelemzés
    out('\n## 4. Mélyelemzés (⛔ DT-F149a)\n')
    for p in mely:
        szov = p.read_text(encoding='utf-8')
        elso = szov.split('\n')[0]
        out(f'- `melyelemzesek/{p.name}`; első címsor: „{elso}”')
        out('  - fájlnévből az általános minta nem illik (több szétszórt tartomány: 1Móz 14:18–20; Zsolt 110:4; Zsid 5–7).')
        out('  - a címsorban a tartományok megvannak, de szabadszöveges alakban (`Zsidók 5-7` = három egész fejezet).')
        vs = []
        for kn, ke, ve in (('1Móz', (14, 18), (14, 20)), ('Zsolt', (110, 4), (110, 4))):
            vs += verskeszlet(kn, ke, ve) or []
        zs = [k for k in verslista['Zsid'] if 5 <= k[1] <= 7]
        out(f'  - (b) kézi tartomány: 1Móz 14:18–20 = 3 vers, Zsolt 110:4 = 1 vers, Zsid 5–7 = {len(zs)} vers (összesen {len(vs) + len(zs)}).')
        halmaz = set(vs) | set(zs)
        for k in halmaz:
            atfedes[k].append(f'melyelemzesek/{p.name}')
        nev = set()
        for cim, sz in szakaszok(szov):
            for _, k in hivatkozasok(sz, '1Móz'):
                if k in halmaz:
                    nev.add(k)
        out(f'  - név szerint hivatkozott vers a tartományokból: {len(nev)} / {len(halmaz)}.')

    out('\n## 5. Átfedések (vers több tanulmányban)\n')
    tobb = {k: v for k, v in atfedes.items() if len(v) > 1}
    out(f'- {len(tobb)} vers tartozik legalább két tanulmányhoz.')
    csoport = defaultdict(list)
    for k, v in sorted(tobb.items(), key=lambda kv: karoli[kv[0]]):
        csoport[tuple(v)].append(k)
    for v, ks in csoport.items():
        out(f'  - {" + ".join(v)}: {len(ks)} vers ({jel(ks[0])} – {jel(ks[-1])})')

    # forras_tanulmany
    out('\n## 6. A `forras_tanulmany` lefedettsége\n')
    rows = [r for r in olvas_tsv(ROOT / 'adat/elofordulasok.tsv') if r and not r[0].startswith('#')]
    hdr = rows[0]
    i = hdr.index('forras_tanulmany')
    adat = rows[1:]
    tolt = [r for r in adat if len(r) > i and r[i]]
    out(f'- {len(adat)} sorból {len(tolt)} kitöltött.')
    ervenytelen = [r[i] for r in tolt if not (ROOT / r[i]).exists()]
    out(f'- nem létező fájlra mutat: {len(ervenytelen)}')
    print('\n'.join(ki))
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text('\n'.join(ki) + '\n', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
