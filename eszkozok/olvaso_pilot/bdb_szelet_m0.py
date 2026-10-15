"""bdb_szelet_m0.py — F99 (BDB_SZELETELO) M0: aranyminta-összevetés és mérések. Csak olvas; a repóba nem ír (a naplót kézzel írom).

Módok (a repó gyökeréből):
  python eszkozok/olvaso_pilot/bdb_szelet_m0.py --dump H1242 [--nyelv en|hu] [--ki <könyvtár>]
        a szócikk szövege jelölő-jelöltek előtt sortöréssel + a mai szeletelő kimenete (az aranyminta kézi összeállításához)
  python eszkozok/olvaso_pilot/bdb_szelet_m0.py --arany
        az adat/bdb_aranyminta.tsv és a mai szeletelő (bdb_szelet.szeletel) összevetése: eltérések listája
  python eszkozok/olvaso_pilot/bdb_szelet_m0.py --hivatkozas
        igehely-hivatkozások mérése az angol BDB-n (kiírt / örökölt / feloldhatatlan könyv, álhivatkozás-jelöltek, MT ≠ Károli)
  python eszkozok/olvaso_pilot/bdb_szelet_m0.py --jelolo
        használati csoport-bevezetők mérése az angol BDB-n és a magyar fordításban

I/O: split('\\t') (csv modul nélkül).
"""
import argparse
import collections
import datetime
import hashlib
import os
import re
import subprocess
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, D)

import bdb_szelet as B  # noqa: E402

BDB_EN = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
FORD = os.path.join(REPO, 'adat', 'forditasok.tsv')
ARANY = os.path.join(REPO, 'adat', 'bdb_aranyminta.tsv')


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for d in iter(lambda: f.read(1 << 20), b''):
            h.update(d)
    return h.hexdigest()[:12]


def commit():
    try:
        return subprocess.check_output(['git', '-C', REPO, 'rev-parse', '--short', 'HEAD'], text=True).strip()
    except Exception:
        return '?'


def prov(scope, forras):
    return 'scope=%s | forras=%s | ts=%s' % (scope, forras, datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'))


def bdb_en():
    ki = {}
    with open(BDB_EN, encoding='utf-8', newline='') as f:
        for i, sor in enumerate(f):
            if i == 0:
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) >= 3:
                ki[m[0]] = m[2]
    return ki


def bdb_hu():
    """A szerver `bdb_magyar` szabálya: a Strong utolsó nem üres BDB-sora (fájlsorrendben)."""
    ki = {}
    with open(FORD, encoding='utf-8', newline='') as f:
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) > 6 and m[0] == 'BDB' and m[6].strip():
                ki[m[1]] = m[6].replace('\\n', '\n')
    return ki


def lemma_tabla():
    """Strong -> héber lemma (a szerver a Strong-szótár `Szótő` mezőjét adja a szeletelőnek, a pilot is)."""
    ki = {}
    ut = os.path.join(REPO, 'konkordancia', 'Strong_szotar.tsv')
    with open(ut, encoding='utf-8', newline='') as f:
        for i, sor in enumerate(f):
            if i == 0 or sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) > 1:
                ki.setdefault(m[0], m[1])
    return ki


# ---------------------------------------------------------------------------
# a szeletelő kimenete egységes csomópont-listaként
# ---------------------------------------------------------------------------

def _norm(s):
    return re.sub(r'\s+', ' ', (s or '').replace('\n', ' ')).strip(' ;,—')


def csomopontok(r):
    """A szeletel() kimenete -> [(szakasz, utvonal, szint, jel, szoveg)] (a fő szakasz: '')."""
    ki = []

    def torzsek(szak, tl):
        for t in tl:
            tn = t['nev'] or '-'
            if t['nev']:
                ki.append((szak, tn, 'torzs', t['nev'], ''))
            for j in t['jelentesek']:
                jp = '%s/%s' % (tn, j['jel'] or '-')
                ki.append((szak, jp, 'jelentes', j['jel'], j['szoveg']))
                for a in j['al']:
                    ki.append((szak, '%s/%s' % (jp, a['jel']), 'alpont', a['jel'], a['szoveg']))
    torzsek('', r['torzsek'])
    for x in r.get('szakaszok', []):
        sz = x['jel'] or x['szerep']
        ki.append((sz, '', 'szakasz', x['jel'], x['heber']))
        torzsek(sz, x['torzsek'])
    return ki


# Használati csoport-bevezetők (szigorú jelöltlista; a végleges lista: DT-F99b). Csak mondatkezdő helyzetben (; . : — után).
_KEZD = r'(?:(?<=[;.:]\s)|(?<=—\s))'
CSOPORT_EN = re.compile(_KEZD + r'(absolute(?:ly)?\b|followed by\b|with\s+(?:accusative|infinitive|suffix|negative|(?=[֐-׿]))|figurative(?:ly)?\b|'
                        r'Inf(?:initive)?\.?\s+abs(?:olute)?\.?|in phrases?\b|opposed to\b|especially\b|also\b|so\b)')
CSOPORT_HU = re.compile(_KEZD + r'(abszolút\w*|utána\b|követi\b|\S+\s+követi|átvitt\w*|képletes\w*|infinitivus absolutus\w*|'
                        r'kifejezés\w*|szólás\w*|ellentéte\w*|ellentétben|különösen\b|továbbá\b|is\b|így\b)')


# ---------------------------------------------------------------------------
# --dump
# ---------------------------------------------------------------------------

def dump(strong, nyelv, kimenet):
    en, hu, lem = bdb_en(), bdb_hu(), lemma_tabla()
    szoveg = hu.get(strong) if nyelv == 'hu' else en.get(strong)
    if szoveg is None:
        print('nincs szöveg:', strong, nyelv)
        return
    r = B.szeletel(szoveg, lem.get(strong, ''))
    s = szoveg.replace('\n', ' ')
    t = re.sub(r'\s(—)\s', r'\n\1 ', s)
    t = re.sub(r'(?<=[\s.;:)])(' + B.TORZS + r')(?=[_\s,])', r'\n@@\1', t)
    t = re.sub(r'(?<=[\s])(\d{1,2})(\.?\s)(?=[^\d\s:,;.)])', r'\n##\1\2', t)
    t = re.sub(r'(?<=[\s])([a-l])\.\s', r'\n  ~~\1. ', t)
    t = re.sub(r'(?<=[\s.;—])((?:IV|VI|V|I{1,3}))\.\s+(?=\[?[֐-׿])', r'\n%%\1. ', t)
    sorok = ['# %s (%s), %d karakter' % (strong, nyelv, len(szoveg)), '', '## A mai szeletelő', '']
    sorok.append('fej: %s | elotag: %s' % (r['fej'], _norm(r.get('elotag'))[:80]))
    for sz, ut, szint, jel, sz2 in csomopontok(r):
        sorok.append('%-8s %-22s %-9s %-4s | %s' % (sz, ut, szint, jel, _norm(sz2)[:70]))
    sorok += ['', '## Csoport-bevezető jelöltek (mondatkezdő, ; . : — után)', '']
    for m in (CSOPORT_EN if nyelv == 'en' else CSOPORT_HU).finditer(s):
        sorok.append('  @%d %s | …%s' % (m.start(1), m.group(1), _norm(s[m.start(1):m.start(1) + 60])))
    sorok += ['', '## Szöveg (jelölő-jelöltek: — gondolatjel, @@ törzsnév, ## szám, ~~ betű, %% római címszó)', '', t]
    os.makedirs(kimenet, exist_ok=True)
    ut = os.path.join(kimenet, '%s_%s.txt' % (strong, nyelv))
    with open(ut, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorok) + '\n')
    print(ut)


# ---------------------------------------------------------------------------
# --arany: az aranyminta és a mai szeletelő összevetése
# ---------------------------------------------------------------------------

RÓMAI = re.compile(r'^(?:I{1,3}|IV|V|VI)$')
SZERKEZET = ('szakasz', 'torzs', 'jelentes', 'alpont')


def _kons(x):
    return re.sub(r'[֑-ׇ‎‏]', '', unicodedata.normalize('NFC', x or ''))


def _szak_kulcs(cimke):
    return cimke if (not cimke or RÓMAI.match(cimke)) else 'h:' + _kons(cimke)


def _ut_norm(ut, szint):
    """Az aranyminta útvonala a szeletelőével azonos alakra: a jelentés nélküli alpont („-/a”) a „-/-/a”."""
    r = ut.split('/')
    if szint == 'alpont' and len(r) == 2:
        return '%s/-/%s' % (r[0], r[1])
    return ut


def _szoveg_norm(s):
    """Összevetési alak: NFC, a héber pontozás nélkül (a kézi horgony és a forrás pontozási sorrendje eltérhet), szóközök egységesítve."""
    s = unicodedata.normalize('NFC', (s or '').replace('\n', ' '))
    s = re.sub(r'[֑-ׇ‎‏]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.lstrip(' —;,.:')


def _cim_norm(s):
    s = (s or '').replace('…', ' ')
    s = re.sub(r'[֐-׿יִ-ﭏ]', ' ', s)
    s = re.sub(r'[^\w\s]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip().lower()


def _szeletelo_csomopontok(r):
    """{(szakasz_kulcs, utvonal, szint): (szoveg, cim_forras)} a szeletelő kimenetéből. A számozatlan jelentés ('…/-') csak akkor
    csomópont, ha alpontja van (ekkor az alpontok '…/-/a' úton állnak); maga nem számít (az aranyminta nem rögzíti)."""
    ki = {}

    def torzsek(szk, tl):
        for t in tl:
            tn = t['nev'] or '-'
            if t['nev']:
                ki[(szk, tn, 'torzs')] = ('', None)
            for j in t['jelentesek']:
                jp = '%s/%s' % (tn, j['jel'] or '-')
                if j['jel']:
                    ki[(szk, jp, 'jelentes')] = (j['szoveg'], ('fo', j))
                for a in j['al']:
                    ki[(szk, '%s/%s' % (jp, a['jel']), 'alpont')] = (a['szoveg'], ('al', a))
    torzsek('', r['torzsek'])
    for x in r.get('szakaszok', []):
        szk = _szak_kulcs(x['jel']) if x['jel'] else 'h:' + _kons(x['heber'])
        ki[(szk, '', 'szakasz')] = (x['heber'], None)
        torzsek(szk, x['torzsek'])
    return ki


def _cim_fuggvenyek():
    """A szerver címképzése (blokkok._fo_cim, blokkok.jelentes_cim); None, ha a szerver modulja nem tölthető be (markupsafe nélkül)."""
    try:
        sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'olvaso_szerver'))
        import blokkok  # noqa: F401
        return blokkok._fo_cim, blokkok.jelentes_cim
    except Exception as e:  # noqa: BLE001
        print('[figyelem] a címek összevetése kimarad: a szerver blokkok modulja nem tölthető be (%s)' % e.__class__.__name__)
        return None


def arany():
    en, hu, lem = bdb_en(), bdb_hu(), lemma_tabla()
    fej, sorok = None, []
    with open(ARANY, encoding='utf-8', newline='') as f:
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            sorok.append(dict(zip(fej, m)))
    cimf = _cim_fuggvenyek()
    szocikkek = []
    for s in sorok:
        if s['strong'] not in szocikkek:
            szocikkek.append(s['strong'])
    ossz = collections.Counter()
    reszlet = []
    for strong in szocikkek:
        gs = [g for g in sorok if g['strong'] == strong]
        kihagy = [(_szak_kulcs(g['szakasz']), g['utvonal']) for g in gs if g['szint'] == 'kihagy']
        for nyelv, szoveg in (('en', en.get(strong)), ('hu', hu.get(strong))):
            if szoveg is None:
                continue
            r = B.szeletel(szoveg, lem.get(strong, ''))
            sz = _szeletelo_csomopontok(r)
            vart = {}
            for g in gs:
                if g['szint'] in SZERKEZET:
                    vart[(_szak_kulcs(g['szakasz']), _ut_norm(g['utvonal'], g['szint']), g['szint'])] = g
            elteres = []
            szocikk = next(g for g in gs if g['szint'] == 'szocikk')
            if _kons(r['fej'].get('heber')) != _kons(szocikk['kezdet_en']):
                elteres.append(('címszó', '', 'várt %s, kapott %s' % (szocikk['kezdet_en'] or '—', r['fej'].get('heber') or '—')))
            if (r['fej'].get('homonima') or '') != szocikk['jel']:
                elteres.append(('homonima', '', 'várt %s, kapott %s' % (szocikk['jel'] or '—', r['fej'].get('homonima') or '—')))

            def kihagyott(k):
                return any(k[0] == ksz and k[1].startswith(kut + '/') for ksz, kut in kihagy)
            for k in sorted(set(vart) - set(sz)):
                elteres.append(('hiányzik', '%s %s' % (k[0], k[1]), k[2]))
            for k in sorted(set(sz) - set(vart)):
                if not kihagyott(k):
                    elteres.append(('fölösleges', '%s %s' % (k[0], k[1]), k[2]))
            cim_db = cim_ok = 0
            for k in sorted(set(sz) & set(vart)):
                g = vart[k]
                kezdet = g['kezdet_hu' if nyelv == 'hu' else 'kezdet_en']
                if kezdet and not _szoveg_norm(sz[k][0]).startswith(_szoveg_norm(kezdet)):
                    elteres.append(('rossz kezdet', '%s %s' % (k[0], k[1]), 'várt „%s”, kapott „%s”' % (kezdet, _szoveg_norm(sz[k][0])[:50])))
                if cimf and g['cim'] and nyelv == ('hu' if hu.get(strong) else 'en') and sz[k][1]:
                    tipus, obj = sz[k][1]
                    kapott = cimf[0](obj) if tipus == 'fo' else cimf[1](obj['szoveg'])
                    cim_db += 1
                    a, b = _cim_norm(g['cim']), _cim_norm(kapott)
                    if a == b or (kapott.endswith('…') and b and a.startswith(b)):
                        cim_ok += 1
                    else:
                        elteres.append(('cím', '%s %s' % (k[0], k[1]), 'várt „%s”, kapott „%s”' % (g['cim'], kapott)))
            csop = sum(1 for g in gs if g['szint'] == 'csoport')
            ossz['szocikk_' + nyelv] += 1
            ossz['elteres_' + nyelv] += len(elteres)
            ossz['hibas_szocikk_' + nyelv] += bool([e for e in elteres if e[0] != 'cím'])
            ossz['cim_' + nyelv] += cim_db
            ossz['cim_ok_' + nyelv] += cim_ok
            ossz['csoport_vart'] += csop if nyelv == 'en' else 0
            reszlet.append((strong, nyelv, len(vart), elteres, csop))
    print('# Aranyminta-összevetés: %s' % prov('adat/bdb_aranyminta.tsv (%d szócikk) × bdb_szelet.szeletel' % len(szocikkek),
                                              'BDB_teljes_unabridged.tsv@%s + forditasok.tsv@%s + bdb_szelet@%s' % (sha(BDB_EN), sha(FORD), commit())))
    for strong, nyelv, n, el, csop in reszlet:
        szerk = [e for e in el if e[0] != 'cím']
        print('\n## %s (%s) — várt szerkezeti csomópont %d, szerkezeti eltérés %d, cím-eltérés %d, várt csoport %d (a szeletelő nem bont csoportra)'
              % (strong, nyelv, n, len(szerk), len(el) - len(szerk), csop))
        for e in el:
            print('- %s: %s %s' % e)
    print('\n# Összesen')
    for k in sorted(ossz):
        print('%s\t%d' % (k, ossz[k]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dump', nargs='+')
    ap.add_argument('--nyelv', default='auto')
    ap.add_argument('--ki', default=os.path.join(os.environ.get('TEMP', '/tmp'), 'f99_dump'))
    ap.add_argument('--arany', action='store_true')
    ap.add_argument('--hivatkozas', action='store_true')
    ap.add_argument('--jelolo', action='store_true')
    a = ap.parse_args()
    if a.dump:
        hu = bdb_hu()
        for s in a.dump:
            ny = a.nyelv if a.nyelv != 'auto' else ('hu' if s in hu else 'en')
            dump(s, ny, a.ki)
    if a.arany:
        arany()


if __name__ == '__main__':
    main()
