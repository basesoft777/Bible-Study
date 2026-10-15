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
  python eszkozok/olvaso_pilot/bdb_szelet_m0.py --etym <LexicalIndex.xml> [--etym-minta 3915 …]
        az OSHL <etym> mérése (M0.4); a fájl a repón kívül, SHA-256-tal ellenőrizve

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


# ---------------------------------------------------------------------------
# --hivatkozas: igehely-hivatkozások mérése az angol BDB-n
# ---------------------------------------------------------------------------

def _bkj():
    sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
    import bdb_konyv_javit as K
    return K


# Irodalmi jel (sigla) a hivatkozás előtt: a hivatkozást megelőző legfeljebb két szó egyikében `^` áll, közben nincs mondat- vagy
# zárójelhatár („De^Job 2:598”, „Dr^Sm i. 24, 5”, „Kö^ii. 2:453”). Jelölt, nem ítélet: a szűrés szabálya a DT-F99a.
SIGLA_ELOTTE = re.compile(r'\S*\^\S*(?:\s+[^\s;()]+){0,2}\s*$')
FOLYTATAS = re.compile(r'\s*,\s*(\d{1,3})(?:\s*-\s*\d{1,3})?(?=[\s,;.)\]]|$)(?!\s*:)')


def hivatkozasok(szoveg, K):
    """Egy szócikk igehely-hivatkozásai sorrendben: dict(poz, nyers, konyv, c, v, mod, ok).
    mod: kiirt | orokolt | folytatas | feloldhatatlan; konyv=None, ha nem bibliai vagy nem dönthető el.
    ok: '' (bibliai, feloldott) | nem_bibliai (Talmud, Korán, apokrif, kommentár: a LANCTORO / APOKRIF_ALIAS alakjai, és az utánuk
    örökölt) | tobbertelmu (Kings, Sam, Chron …: a szám nélküli alak) | sigla_utan (álhivatkozás-jelölt) | nincs_elozmeny."""
    s = re.sub(r'\s+', ' ', szoveg.replace('\n', ' '))
    tok = []
    for m in K.TOKEN.finditer(s):
        tok.append((m.start(), m.end(), m.group(1), int(m.group(2)), int(m.group(3)), m.group(0)))
    for m in K.TAPADT_SZAM.finditer(s):
        tok.append((m.start(), m.end(), m.group(1) + m.group(2), int(m.group(3)), int(m.group(4)), m.group(0)))
    kiirt = {t[0]: t for t in tok}
    lefedett = set()
    for t in tok:
        lefedett.update(range(t[0], t[1]))
    for m in K.CSUPASZ.finditer(s):
        if m.start() in lefedett:
            continue
        kiirt.setdefault(m.start(), (m.start(), m.end(), None, int(m.group(1)), int(m.group(2)), m.group(0)))
    ki = []
    utolso = None          # (konyv | None, ok)
    for p in sorted(kiirt):
        a, e, alak, c, v, nyers = kiirt[p]
        sig = ''
        if a and s[a - 1] == '^':
            elotte = re.search(r'(\S*)\^$', s[max(0, a - 30):a]).group(1)
            sig = 'nem_tanu' if re.search(r'(?:masculine|feminine|plural|singular|hímnemű|nőnemű|főnév)$', elotte) else 'sigla_tapadt'
        elif SIGLA_ELOTTE.search(s[max(0, a - 40):a]):
            sig = 'sigla_kozel'
        if alak is not None:
            alak_n = alak.rstrip('.')
            if alak_n in K.LEK:
                konyv, ok = K.LEK[alak_n], ''
            elif alak_n in K.LANCTORO or alak_n in K.N.APOKRIF_ALIAS:
                konyv, ok = None, 'nem_bibliai'
            elif alak_n in K.TOBBERTELMU:
                konyv, ok = None, 'tobbertelmu'
            else:
                konyv, ok = None, 'ismeretlen_alak'
            mod = 'kiirt'
            utolso = (konyv, ok)
        else:
            if utolso is None:
                konyv, ok, mod = None, 'nincs_elozmeny', 'feloldhatatlan'
            else:
                konyv, ok = utolso
                mod = 'orokolt'
        ki.append({'poz': a, 'nyers': nyers, 'konyv': konyv, 'c': c, 'v': v, 'mod': mod, 'ok': ok, 'sig': sig})
        # vers-folytatás: „Gen 18:18, 25; 22:18” → 18:25 is hivatkozás
        q = e
        while True:
            f = FOLYTATAS.match(s, q)
            if not f:
                break
            ki.append({'poz': f.start(1), 'nyers': f.group(0).strip(), 'konyv': konyv, 'c': c, 'v': int(f.group(1)),
                       'mod': 'folytatas', 'ok': ok, 'sig': sig})
            q = f.end()
    return ki


def hivatkozas_meres():
    K = _bkj()
    en = bdb_en()
    biz_versek, _, mt2k_nyers = K.macula_betolt()
    mt2k = {kk: {(K.TAHOT_KONYV.get(x[0], x[0]), x[1], x[2]) for x in v} for kk, v in mt2k_nyers.items()}
    # a Károli-versmegfeleltetés: Károli-vers -> (osztaly, igehely_mt); az MT-osztályú sorok MT-száma = Károli-szám
    vm, vm_mt = {}, {}
    fej = None
    with open(os.path.join(REPO, 'konkordancia', 'Karoli_versmegfeleltetes.tsv'), encoding='utf-8', newline='') as f:
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            vm[d['igehely_karoli']] = d['osztaly']
            if d['igehely_mt']:
                kk = d['igehely_karoli'].rsplit(' ', 1)[0]
                vm_mt['%s %s' % (kk, d['igehely_mt'])] = d['igehely_karoli']
    osz = set(K.OSZ)
    c = collections.Counter()
    szocikk_ref = set()
    sig_minta = collections.defaultdict(list)
    ism, tobb, karoli_mas, karoli_nincs, nemletezo = collections.Counter(), collections.Counter(), [], [], []
    for strong, szoveg in en.items():
        hl = hivatkozasok(szoveg, K)
        if hl:
            szocikk_ref.add(strong)
        for h in hl:
            c['ossz'] += 1
            c['mod:' + h['mod']] += 1
            c['ok:' + (h['ok'] or 'bibliai')] += 1
            if h['sig']:
                c['sigla:' + h['sig']] += 1
                if len(sig_minta[h['sig']]) < 12:
                    sig_minta[h['sig']].append((strong, h['nyers'], re.sub(r'\s+', ' ', szoveg)[max(0, h['poz'] - 30):h['poz'] + 12]))
            if h['ok'] == 'ismeretlen_alak':
                ism[re.match(r'\S+', h['nyers']).group(0)] += 1
            if h['ok'] == 'tobbertelmu':
                tobb[re.match(r'\S+', h['nyers']).group(0)] += 1
            if h['ok'] == '' and h['konyv']:
                k = h['konyv']
                if k not in osz:
                    c['usz'] += 1
                    continue
                c['osz_bibliai'] += 1
                if h['v'] not in biz_versek.get(k, {}).get(h['c'], ()):
                    c['mt_nem_letezik'] += 1
                    c['mt_nem_letezik:' + h['mod']] += 1
                    if len(nemletezo) < 30:
                        nemletezo.append((strong, h['nyers'], '%s %d:%d' % (k, h['c'], h['v']), h['mod']))
                    continue
                ig = '%s %d:%d' % (k, h['c'], h['v'])
                # a Károli-versmegfeleltetés szerint (a brief forrása)
                if ig in vm_mt:
                    c['vm:MT_osztaly'] += 1
                    if vm_mt[ig] != ig:
                        c['vm:MT_osztaly_mas_karoli'] += 1
                elif vm.get(ig) == 'KJV':
                    c['vm:KJV_osztaly_mt_ismeretlen'] += 1
                elif ig in vm:
                    c['vm:%s_osztaly' % vm[ig]] += 1
                else:
                    c['vm:nincs_sor'] += 1
                kar = mt2k.get((k, h['c'], h['v']))
                if ig in vm_mt and kar and kar != {tuple([k] + [int(x) for x in vm_mt[ig].rsplit(' ', 1)[1].split(':')])}:
                    c['macula_ellentmond_vm_MT_osztaly'] += 1
                    c['macula_ellentmond_vm_MT_osztaly_konyv:' + k] += 1
                if not kar:
                    c['macula:karoli_nincs'] += 1
                    if len(karoli_nincs) < 15:
                        karoli_nincs.append((strong, ig))
                elif kar != {(k, h['c'], h['v'])}:
                    c['macula:karoli_mas'] += 1
                    c['macula:karoli_mas_konyv:' + k] += 1
                    if len(karoli_mas) < 20:
                        karoli_mas.append((strong, ig, sorted('%s %d:%d' % x for x in kar)))
                else:
                    c['macula:karoli_azonos'] += 1
    # független próba: az OSHL BDB-XML strukturált igehelyei (<ref r=…>) megvannak-e a mi feloldásunkban
    oshl = collections.defaultdict(set)
    for p in K.tsv(K.OSHL_REF)[1:]:
        if len(p) >= 6 and p[0].startswith('H'):
            oshl[p[0]].add((p[3], int(p[4]), int(p[5])))
    mi = collections.defaultdict(set)
    for strong, szoveg in en.items():
        if strong in oshl:
            for h in hivatkozasok(szoveg, K):
                if h['konyv']:
                    mi[strong].add((h['konyv'], h['c'], h['v']))
    o_ossz = sum(len(v) for v in oshl.values())
    o_van = sum(len(v & mi[s]) for s, v in oshl.items())
    c['oshl_proba:oshl_hely'] = o_ossz
    c['oshl_proba:megvan_a_feloldasban'] = o_van
    hiany = [(s, sorted(v - mi[s])[:3]) for s, v in sorted(oshl.items()) if v - mi[s]][:12]
    print(prov('angol BDB, minden szócikk (%d); hivatkozás = könyvvel kiírt vagy könyv nélküli fejezet:vers, és a vesszős vers-folytatás' % len(en),
               'BDB_teljes_unabridged.tsv@%s + bdb_konyv_javit.TOKEN/CSUPASZ/LEK/LANCTORO + Macula_heber_* (MT-versek, MT→Károli) + bdb_szelet_m0@%s'
               % (sha(BDB_EN), commit())))
    print('szócikk hivatkozással: %d / %d' % (len(szocikk_ref), len(en)))
    for k in sorted(c):
        print('%s\t%d' % (k, c[k]))
    print('\nismeretlen könyvalak (top 20):', ism.most_common(20))
    print('többértelmű alak:', tobb.most_common())
    for k, lst in sorted(sig_minta.items()):
        print('\nsigla minta (%s):' % k)
        for x in lst:
            print('  ', x)
    print('\nMT-ben nem létező vers (minta):')
    for x in nemletezo:
        print('  ', x)
    print('\nMT ≠ Károli (minta):')
    for x in karoli_mas:
        print('  ', x)
    print('\nMT-vers Károli-megfelelő nélkül (minta):')
    for x in karoli_nincs:
        print('  ', x)
    print('\nOSHL-hely, amely a feloldásban nincs (minta):')
    for x in hiany:
        print('  ', x)


# ---------------------------------------------------------------------------
# --jelolo: használati csoport-bevezetők mérése
# ---------------------------------------------------------------------------

# Mérési jelöltlista (tágabb, mint az aranyminta szigorú listája): kulcs -> minta. A „with”-et a szerkezet szerint bontjuk.
BEVEZETO_EN = [
    ('absolute', r'absolute(?:ly)?\b'),
    ('followed by', r'followed by\b'),
    ('with + héber', r'with\s+(?=[֐-׿׳])'),
    ('with accusative', r'with\s+accusative\b'),
    ('with infinitive', r'with\s+infinitive\b'),
    ('with suffix', r'with\s+suffix\b'),
    ('Inf. abs. (as adverb)', r'(?:Inf(?:initive)?\.?\s+abs(?:olute)?\.?|infinitive absolute)(?:\s+(?:as\s+)?adverb\.?)?'),
    ('in phrase(s)', r'in\s+phrases?\b'),
    ('figurative', r'figurative(?:ly)?\b'),
    ('opposed to', r'opposed to\b'),
    ('especially', r'especially\b'),
    ('also', r'also\b'),
    ('so', r'so\b'),
    ('often', r'often\b'),
    ('rarely', r'rarely\b'),
    ('(n) zárójeles szám', r'\(\d\)'),
    ('(a) zárójeles betű', r'\([a-h]\)'),
]
BEVEZETO_HU = [
    ('abszolút használatban', r'abszolút használat\w*'),
    ('abszolút (egyéb)', r'abszolút(?! használat)\w*'),
    ('status absolutus', r'status absolutus'),
    ('utána', r'utána\b'),
    ('követi', r'\S+\s+követi\b|követi\b'),
    ('+ ragos héber (-val/-vel)', r'[֐-׿׳]+-(?:val|vel|lal|lel|ral|rel)\b'),
    ('tárgyesetével', r'\w*\s?tárgyesetével'),
    ('infinitivus absolutus', r'infinitivus absolutus\w*(?:\s+határozószóként)?'),
    ('kifejezésekben/fordulatokban', r'(?:kifejezés|fordulat)\w*ban\b|(?:kifejezés|fordulat)\w*ben\b'),
    ('átvitt értelemben', r'átvitt értelem\w*'),
    ('képletesen', r'képletes\w*'),
    ('ellentéte', r'ellentét\w*'),
    ('szemben', r'\w+\s+szemben\b'),
    ('különösen', r'különösen\b'),
    ('továbbá', r'továbbá\b'),
    ('így', r'így\b'),
    ('gyakran', r'gyakran\b'),
    ('ritkán', r'ritkán\b'),
    ('(n) zárójeles szám', r'\(\d\)'),
    ('(a) zárójeles betű', r'\([a-h]\)'),
]


def _csomopont_kezdetek(szoveg, r):
    """A szeletelő csomópontjainak kezdőpozíciói a lapított szövegben, és a jelentésrégió kezdete (első törzs vagy jelentés)."""
    flat = re.sub(r'\s+', ' ', szoveg.replace('\n', ' '))
    kezd, start = [], 0
    for sz, ut, szint, jel, sz2 in csomopontok(r):
        k = re.sub(r'\s+', ' ', sz2 or '').strip()[:30]
        if not k or szint == 'szakasz':
            continue
        i = flat.find(k, start)
        if i >= 0:
            kezd.append(i)
            start = i
    return flat, sorted(set(kezd))


def _helyzet(flat, poz, kezd, zaro):
    if kezd and poz < kezd[0]:
        return 'alaktan_elotag'
    if zaro[poz]:
        return 'zarojelben'
    if any(0 <= poz - k <= 2 for k in kezd):
        return 'csomopont_eleje'
    elotte = flat[max(0, poz - 3):poz]
    if re.search(r'[;.:—]\s*$', elotte):
        return 'mondatkezdo'
    if re.search(r',\s*$', elotte):
        return 'vesszo_utan'
    return 'mondat_kozben'


def jelolo_meres():
    en, hu, lem = bdb_en(), bdb_hu(), lemma_tabla()
    eredmeny = {}
    for nyelv, korpusz, lista in (('en', en, BEVEZETO_EN), ('hu', hu, BEVEZETO_HU)):
        c = collections.defaultdict(collections.Counter)
        szocikk = collections.defaultdict(set)
        for strong, szoveg in korpusz.items():
            r = B.szeletel(szoveg, lem.get(strong, ''))
            flat, kezd = _csomopont_kezdetek(szoveg, r)
            zaro = B._zarojelben(flat)
            for kulcs, minta in lista:
                for m in re.finditer(r'(?<![\w-])(?:%s)' % minta, flat):
                    h = _helyzet(flat, m.start(), kezd, zaro)
                    c[kulcs][h] += 1
                    c[kulcs]['ossz'] += 1
                    szocikk[kulcs].add(strong)
        eredmeny[nyelv] = (c, szocikk, len(korpusz))
    print(prov('angol BDB (%d szócikk) és magyar BDB (%d szócikk, a szerver bdb_magyar-szabálya); helyzet a mai szeletelő csomópontjaihoz képest'
               % (len(en), len(hu)), 'BDB_teljes_unabridged.tsv@%s + forditasok.tsv@%s + bdb_szelet@%s' % (sha(BDB_EN), sha(FORD), commit())))
    oszl = ['ossz', 'csomopont_eleje', 'mondatkezdo', 'vesszo_utan', 'mondat_kozben', 'zarojelben', 'alaktan_elotag']
    for nyelv in ('en', 'hu'):
        c, szocikk, n = eredmeny[nyelv]
        print('\n## %s (%d szócikk)' % (nyelv, n))
        print('| bevezető | szócikk | ' + ' | '.join(oszl) + ' |')
        print('|---|---|' + '---|' * len(oszl))
        for kulcs, _ in (BEVEZETO_EN if nyelv == 'en' else BEVEZETO_HU):
            print('| %s | %d | %s |' % (kulcs, len(szocikk[kulcs]), ' | '.join(str(c[kulcs][o]) for o in oszl)))
    # a kész magyar szócikkeken: angol bevezető-szám vs. magyar megfelelő-szám szócikkenként (csak a jelentésrégióban, zárójelen kívül)
    print('\n## A kész magyar szócikkek (%d): angol–magyar bevezetőszám szócikkenként (jelentésrégió, zárójelen kívül)' % len(hu))
    parok = [('absolute', ['abszolút használatban', 'abszolút (egyéb)']), ('followed by', ['utána', 'követi']),
             ('figurative', ['átvitt értelemben', 'képletesen']), ('opposed to', ['ellentéte', 'szemben']),
             ('especially', ['különösen']), ('in phrase(s)', ['kifejezésekben/fordulatokban']),
             ('Inf. abs. (as adverb)', ['infinitivus absolutus'])]
    for ek, hks in parok:
        egyezik = kulonbozik = mindketto0 = 0
        for strong in hu:
            def db(szoveg, lista, kulcsok):
                r = B.szeletel(szoveg, lem.get(strong, ''))
                flat, kezd = _csomopont_kezdetek(szoveg, r)
                zaro = B._zarojelben(flat)
                n = 0
                for kulcs, minta in lista:
                    if kulcs not in kulcsok:
                        continue
                    for m in re.finditer(r'(?<![\w-])(?:%s)' % minta, flat):
                        if _helyzet(flat, m.start(), kezd, zaro) not in ('zarojelben', 'alaktan_elotag'):
                            n += 1
                return n
            a, b = db(en.get(strong, ''), BEVEZETO_EN, [ek]), db(hu[strong], BEVEZETO_HU, hks)
            if a == 0 and b == 0:
                mindketto0 += 1
            elif a == b:
                egyezik += 1
            else:
                kulonbozik += 1
        print('- %s ↔ %s: azonos szám %d szócikkben, eltérő %d, egyik sem %d' % (ek, ' / '.join(hks), egyezik, kulonbozik, mindketto0))


# ---------------------------------------------------------------------------
# --etym: az OSHL LexicalIndex.xml <etym> elemének mérése (M0.4)
# ---------------------------------------------------------------------------

OSHL_LEXINDEX_SHA256 = '8f7a605c58899d2f44430149c143c00903976e1e91232476677972a69e5bc85f'


def etym_meres(ut, minta=('3915',)):
    import xml.etree.ElementTree as ET
    h = hashlib.sha256(open(ut, 'rb').read()).hexdigest()
    if h != OSHL_LEXINDEX_SHA256:
        sys.exit('HIBA: a LexicalIndex.xml SHA-256-ja eltér: %s' % h)
    ns = '{http://openscriptures.github.com/morphhb/namespace}'
    bejegyzes = {}
    for part in ET.parse(ut).getroot().iter(ns + 'part'):
        nyelv = part.get('{http://www.w3.org/XML/1998/namespace}lang')
        for e in part.findall(ns + 'entry'):
            w = e.find(ns + 'w')
            x = e.find(ns + 'xref')
            et = e.find(ns + 'etym')
            st = x.get('strong') if x is not None else None
            bejegyzes[e.get('id')] = {
                'nyelv': nyelv, 'lemma': ''.join(w.itertext()) if w is not None else '', 'xlit': w.get('xlit') if w is not None else '',
                'strong': ('H%04d' % int(st)) if st and st.isdigit() else None,
                'tipus': et.get('type') if et is not None else None, 'gyok': et.get('root') if et is not None else None,
                'cel': [t.strip() for t in (et.text or '').split(',') if t.strip()] if et is not None else []}
    bdb = set(bdb_en())
    c = collections.Counter()
    for i, b in bejegyzes.items():
        t = b['tipus'] or 'nincs_etym'
        c['%s:%s' % (b['nyelv'], t)] += 1
        c['ossz:' + t] += 1
        if t == 'main':
            c['main:gyok_attributummal' if b['gyok'] else 'main:gyok_nelkul'] += 1
            c['main:szarmazek_nelkul' if not b['cel'] else 'main:szarmazekkal'] += 1
            for x in b['cel']:
                c['main_lista_elem'] += 1
                y = bejegyzes.get(x)
                if not y:
                    c['main_lista_elem:nem_letezo_id'] += 1
                elif y['tipus'] != 'sub' or i not in y['cel']:
                    c['main_lista_elem:nem_kolcsonos'] += 1
        if t == 'sub':
            cel = b['cel'][0] if b['cel'] else None
            y = bejegyzes.get(cel)
            if len(b['cel']) != 1:
                c['sub:nem_egy_cel'] += 1
            if not y:
                c['sub_cel:nem_letezo_id'] += 1
            else:
                c['sub_cel:tipus_' + (y['tipus'] or 'nincs')] += 1
                c['sub_cel:strong_' + ('van' if y['strong'] else 'nincs')] += 1
                if y['strong']:
                    c['sub_cel:strong_a_bdb_tablaban' if y['strong'] in bdb else 'sub_cel:strong_nincs_a_bdb_tablaban'] += 1
                if y['tipus'] == 'main' and i not in y['cel']:
                    c['sub:a_cel_listaja_nem_tartalmazza'] += 1
        if b['strong']:
            c['strong_bejegyzes:' + t] += 1
    # Strong-szintű lefedettség: a BDB-tábla Strongjai közül hánynak van (legalább egy) családja az OSHL-ben
    strong_tipus = collections.defaultdict(set)
    for b in bejegyzes.values():
        if b['strong']:
            strong_tipus[b['strong']].add(b['tipus'] or 'nincs_etym')
    for s in bdb:
        tl = strong_tipus.get(s)
        if not tl:
            c['bdb_strong:nincs_oshl_bejegyzes'] += 1
        elif tl & {'main', 'sub'}:
            c['bdb_strong:van_csalad'] += 1
        elif 'single' in tl:
            c['bdb_strong:single'] += 1
        else:
            c['bdb_strong:etym_nelkul'] += 1
    print(prov('OSHL LexicalIndex.xml <etym> (minden <entry>); a BDB-tábla Strongjai: %d' % len(bdb),
               'openscriptures/HebrewLexicon@21c9add13bc727d3a951361778e97e3ff7afd1ce LexicalIndex.xml sha256=%s… + BDB_teljes_unabridged.tsv@%s + bdb_szelet_m0@%s'
               % (h[:12], sha(BDB_EN), commit())))
    for k in sorted(c):
        print('%s\t%d' % (k, c[k]))
    for st in minta:
        print('\n## Minta: H%04d' % int(st))
        for i, b in bejegyzes.items():
            if b['strong'] == 'H%04d' % int(st):
                print('  %s %s %s %s etym=%s gyok=%s cel=%s' % (i, b['nyelv'], b['lemma'], b['xlit'], b['tipus'], b['gyok'], b['cel']))
                csal = []
                if b['tipus'] == 'sub' and b['cel']:
                    m = bejegyzes.get(b['cel'][0], {})
                    csal = [b['cel'][0]] + m.get('cel', [])
                elif b['tipus'] == 'main':
                    csal = [i] + b['cel']
                for x in csal:
                    y = bejegyzes.get(x, {})
                    print('    család: %s %s %s %s %s' % (x, y.get('strong'), y.get('lemma'), y.get('xlit'), y.get('tipus')))
                if not csal:
                    print('    nincs OSHL-gyökcsalád (etym=%s)' % b['tipus'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dump', nargs='+')
    ap.add_argument('--nyelv', default='auto')
    ap.add_argument('--ki', default=os.path.join(os.environ.get('TEMP', '/tmp'), 'f99_dump'))
    ap.add_argument('--arany', action='store_true')
    ap.add_argument('--hivatkozas', action='store_true')
    ap.add_argument('--jelolo', action='store_true')
    ap.add_argument('--etym', metavar='LEXICALINDEX_XML')
    ap.add_argument('--etym-minta', nargs='*', default=['3915', '1242', '7307'])
    a = ap.parse_args()
    if a.dump:
        hu = bdb_hu()
        for s in a.dump:
            ny = a.nyelv if a.nyelv != 'auto' else ('hu' if s in hu else 'en')
            dump(s, ny, a.ki)
    if a.arany:
        arany()
    if a.hivatkozas:
        hivatkozas_meres()
    if a.jelolo:
        jelolo_meres()
    if a.etym:
        etym_meres(a.etym, a.etym_minta)


if __name__ == '__main__':
    main()
