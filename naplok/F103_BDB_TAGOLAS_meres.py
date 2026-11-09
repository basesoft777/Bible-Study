"""F103_BDB_TAGOLAS_meres.py — F103 (BDB_TAGOLAS, FELADATOK #103): a használati csoportok mérése, előtte és utána ugyanazzal a
szkripttel. Csak olvas; a repóba csak a `--tsv` kapcsolóval ír (a régi magyar bevezető-alakok szócikkenkénti listája, naplok/).

Mérések (a repó gyökeréből: `python naplok/F103_BDB_TAGOLAS_meres.py [--tsv]`):
  1. aranyminta, angol: a várt csoportok (adat/bdb_aranyminta.tsv, szint=csoport) és a szeletelő csoportjai (bdb_szelet.csoport_bont)
     szülő-csomópontonként, a jelölő-sorozat leghosszabb közös részsorozatával illesztve: egyezik / hiányzik / hamis határ; az egyező
     csoportok horgonya (kezdet_en) a csoport szövegének elején (az első 25 karakteren belül) áll-e.
  2. aranyminta, magyar: a várt magyar bontás az aranyminta szerint ott, ahol a szülő minden angol csoportjának van magyar horgonya
     (kezdet_hu), különben bontás nélkül (DT167 (5) (a)); a szeletelő magyar bontása (bdb_szelet.csoport_magyar) ehhez mérve.
  3. teljes angol BDB: a bontott csoportok száma bevezetőnként (tájékoztató).
  4. teljes magyar BDB: a csoportos angol csomópontokból hányban bont a magyar (egyező jelölőszám és sorrend).
  5. terminológia (DT167 (2)): a kötelező magyar alak és a régi alakok előfordulása a magyar szócikkekben (mondatkezdő helyzetben és
     összesen), szócikkszámmal; `--tsv`: szócikkenként a naplok/F103_BDB_TAGOLAS_regi_alakok.tsv-be.
  6. jelentéspont (a #102 mércéje): m2_minta_osszevet.py --mai-tabla a seed-102 kulcsán és kitöltésein.
I/O: split('\\t') (csv modul nélkül).
"""
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

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'olvaso_szerver'))
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'bdb_jelolt'))

import bdb_szelet as B  # noqa: E402
import szakasz_bemenet as SZB  # noqa: E402

BDB_EN = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
FORD = os.path.join(REPO, 'adat', 'forditasok.tsv')
ARANY = os.path.join(REPO, 'adat', 'bdb_aranyminta.tsv')
STRONG_SZOTAR = os.path.join(REPO, 'konkordancia', 'Strong_szotar.tsv')
REGI_TSV = os.path.join(REPO, 'naplok', 'F103_BDB_TAGOLAS_regi_alakok.tsv')
RÓMAI = re.compile(r'^(?:I{1,3}|IV|V|VI)$')
HEB = '֐-׿יִ-ﭏ'


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for d in iter(lambda: f.read(1 << 20), b''):
            h.update(d)
    return h.hexdigest()[:12]


def commit():
    try:
        return subprocess.check_output(['git', '-C', REPO, 'rev-parse', '--short', 'HEAD'], text=True).strip()
    except Exception:  # noqa: BLE001
        return '?'


def tsv(path):
    fej, ki = None, []
    with open(path, encoding='utf-8', newline='') as f:
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\r\n').split('\t')
            if fej is None:
                fej = m
                continue
            ki.append(dict(zip(fej, m + [''] * (len(fej) - len(m)))))
    return ki


def bdb_en():
    ki = {}
    with open(BDB_EN, encoding='utf-8', newline='') as f:
        for i, sor in enumerate(f):
            if i == 0:
                continue
            m = sor.rstrip('\r\n').split('\t')
            if len(m) >= 3:
                ki[m[0]] = m[2]
    return ki


def bdb_hu():
    """A szerver `bdb_magyar` szabálya: a Strong BDB-sorai a táblasorrendben, a közös összefűzőn át (szakasz_bemenet.strong_magyar_sorok)."""
    sorok = collections.defaultdict(list)
    for r in tsv(FORD):
        if r['szotar'] == 'BDB':
            sorok[r['strong']].append(r)
    ki = {}
    for s, rs in sorok.items():
        szoveg = SZB.strong_magyar_sorok(rs)[0]
        if szoveg:
            ki[s] = szoveg.replace('\\n', '\n')
    return ki


def lemma_tabla():
    ki = {}
    for r in tsv(STRONG_SZOTAR):
        vals = list(r.values())
        if len(vals) > 1:
            ki.setdefault(vals[0], vals[1])
    return ki


def _kons(x):
    return re.sub(r'[֑-ׇ‎‏]', '', unicodedata.normalize('NFC', x or ''))


def szak_kulcs(cimke, resz=''):
    k = cimke if (not cimke or RÓMAI.match(cimke) or cimke.startswith('h:')) else 'h:' + _kons(cimke)
    return '%s r:%s' % (k, resz) if resz else k


def szulo_norm(ut):
    """Az aranyminta csoport-útvonalának szülője a szeletelő alakjában: a jelentés nélküli alpont („X/a”) „X/-/a”."""
    r = ut.split('/')
    if len(r) == 2 and re.fullmatch(r'[a-l]', r[1]):
        return '%s/-/%s' % (r[0], r[1])
    return ut


def szoveg_norm(s):
    s = unicodedata.normalize('NFC', (s or '').replace('\n', ' '))
    s = re.sub(r'[֑-ׇ‎‏]', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def lcs(a, b):
    """A két jelölő-sorozat leghosszabb közös részsorozata: [(i, j)] index-párok."""
    n, m = len(a), len(b)
    t = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            t[i][j] = t[i + 1][j + 1] + 1 if a[i] == b[j] else max(t[i + 1][j], t[i][j + 1])
    i = j = 0
    ki = []
    while i < n and j < m:
        if a[i] == b[j]:
            ki.append((i, j))
            i += 1
            j += 1
        elif t[i + 1][j] >= t[i][j + 1]:
            i += 1
        else:
            j += 1
    return ki


def szeletelo_csoportok(r):
    """{(szakasz_kulcs, szülő-útvonal): [csoport-dict]} a szeletelő kimenetéből; üres, ha a szeletelőben nincs csoportbontás."""
    if not hasattr(B, 'csoport_bejar'):
        return {}
    ki = collections.defaultdict(list)
    for szak, ut, node in B.csoport_bejar(r):
        cs = node.get('csop') or []
        if cs:
            ki[(szak_kulcs(*B.szakasz_bont(szak)), ut)].extend(cs)
    return ki


def csoport_bont(r, nyelv):
    if hasattr(B, 'csoport_bont'):
        B.csoport_bont(r, nyelv)
    return r


def arany(en, hu, lem):
    sorok = tsv(ARANY)
    vart_en = collections.defaultdict(list)
    kihagy = []
    for g in sorok:
        if g['szint'] == 'kihagy':
            kihagy.append((g['strong'], szak_kulcs(g['szakasz'], g.get('resz', '')), g['utvonal']))
        if g['szint'] != 'csoport':
            continue
        szulo = szulo_norm(g['utvonal'].rsplit('/', 1)[0])
        vart_en[(g['strong'], szak_kulcs(g['szakasz'], g.get('resz', '')), szulo)].append(g)
    szocikkek = []
    for g in sorok:
        if g['strong'] not in szocikkek:
            szocikkek.append(g['strong'])
    ossz = collections.Counter()
    hibak = []
    hu_hibak = []
    for strong in szocikkek:
        r = csoport_bont(B.szeletel(en[strong], lem.get(strong, '')), 'en')
        kapott = szeletelo_csoportok(r)
        kulcsok = {k[1:] for k in vart_en if k[0] == strong} | set(kapott)
        for k in sorted(kulcsok):
            vg = vart_en.get((strong,) + k, [])
            kg = kapott.get(k, [])
            if not vg and any(kst == strong and k[0] == ksz and (k[1] == kut or k[1].startswith(kut + '/'))
                              for kst, ksz, kut in kihagy):
                continue
            par = lcs([g['jel'] for g in vg], [c['jel'] for c in kg])
            ossz['en_vart'] += len(vg)
            ossz['en_kapott'] += len(kg)
            ossz['en_egyezik'] += len(par)
            ossz['en_hianyzik'] += len(vg) - len(par)
            ossz['en_hamis_hatar'] += len(kg) - len(par)
            for i, j in par:
                kezdet = szoveg_norm(vg[i]['kezdet_en'])
                if kezdet and kezdet not in szoveg_norm(kg[j]['szoveg'])[:len(kezdet) + 25]:
                    ossz['en_rossz_kezdet'] += 1
                    hibak.append('rossz kezdet\t%s\t%s %s\t%s\tvárt „%s”, kapott „%s”' % (
                        strong, k[0], k[1], vg[i]['jel'], vg[i]['kezdet_en'], szoveg_norm(kg[j]['szoveg'])[:50]))
            pi = {i for i, _ in par}
            pj = {j for _, j in par}
            for i, g in enumerate(vg):
                if i not in pi:
                    hibak.append('hiányzik\t%s\t%s %s\t%s\t„%s”%s' % (strong, k[0], k[1], g['jel'], g['kezdet_en'],
                                                                   '' if k in kapott or not kapott else ''))
            for j, c in enumerate(kg):
                if j not in pj:
                    hibak.append('hamis határ\t%s\t%s %s\t%s\t„%s”' % (strong, k[0], k[1], c['jel'], szoveg_norm(c['szoveg'])[:50]))
        # magyar: várt bontás ott, ahol a szülő minden angol csoportjának van magyar horgonya
        if strong in hu:
            rh = csoport_bont(B.szeletel(hu[strong], lem.get(strong, '')), 'hu')
            if hasattr(B, 'csoport_magyar'):
                B.csoport_magyar(rh, r)
            kh = szeletelo_csoportok(rh)
            for k in sorted({k[1:] for k in vart_en if k[0] == strong} | set(kh)):
                vg = vart_en.get((strong,) + k, [])
                vart_bont = bool(vg) and all(g['kezdet_hu'] for g in vg)
                kg = kh.get(k, [])
                ossz['hu_szulo'] += 1
                ossz['hu_vart_bontas'] += vart_bont
                ossz['hu_bontott'] += bool(kg)
                if kg and vart_bont:
                    ossz['hu_bontott_es_vart'] += 1
                    if [c['jel'] for c in kg] != [g['jel'] for g in vg]:
                        ossz['hu_bontott_mas_jelolokkel'] += 1
                        hu_hibak.append('más jelölők\t%s\t%s %s\tvárt %s, kapott %s' % (
                            strong, k[0], k[1], [g['jel'] for g in vg], [c['jel'] for c in kg]))
                elif kg and not vart_bont:
                    ossz['hu_bontott_nem_vart'] += 1
                    hu_hibak.append('nem várt bontás\t%s\t%s %s\tkapott %s' % (strong, k[0], k[1], [c['jel'] for c in kg]))
                elif vart_bont and not kg:
                    ossz['hu_vart_nem_bontott'] += 1
                    hu_hibak.append('várt, nem bontott\t%s\t%s %s\tvárt %s' % (strong, k[0], k[1], [g['jel'] for g in vg]))
    return ossz, hibak, hu_hibak


# DT167 (2): angol bevezető → kötelező magyar alak, és a régi (más) alakok a kész fordításban
TERMINOLOGIA = [
    ('followed by', 'utána', r'utána', [('követi', r'\S+\s+követi'), ('ragos héber (-val/-vel)', r'[' + HEB + r'][^\s,;]*-(?:val|vel)\b')]),
    ('Inf. abs. as adverb', 'infinitivus absolutus határozószóként', r'infinitivus absolutus határozószóként',
     [('infinitivus absolutus (más folytatással)', r'infinitivus absolutus(?!\s+határozószóként)\w*'), ('inf. abs.', r'[Ii]nf\.\s*abs\.')]),
    ('in phrase(s)', 'kifejezésekben', r'kifejezésekben', [('kifejezésben', r'kifejezésben'), ('fordulat(ok)ban', r'fordulat(?:ok)?ban'),
                                                           ('szólás(ok)ban', r'szólás(?:ok)?ban')]),
    ('figurative', 'átvitt értelemben', r'átvitt értelemben', [('képletesen', r'képletes(?:en)?\b'), ('átvitt (más alakban)', r'átvitt(?!\s+értelemben)\w*')]),
    ('opposed to', 'ellentéte', r'ellentéte\b', [('szemben', r'szemben\b'), ('ellentétben', r'ellentétben\b')]),
    ('especially', 'különösen', r'különösen\b', [('főként', r'főként\b'), ('kiváltképp', r'kiváltképp(?:en)?\b'), ('főleg', r'főleg\b')]),
    ('absolute', 'abszolút használatban', r'abszolút használatban', [('abszolút (más alakban)', r'abszolút(?!\s+használatban)\w*')]),
]
MONDATKEZDO = r'(?:(?<=[;.:]\s)|(?<=—\s))'


def terminologia(hu, tsv_ir):
    ossz = collections.Counter()
    szocikk = collections.Counter()
    lista = []
    for strong in sorted(hu):
        s = hu[strong].replace('\n', ' ')
        for angol, kotelezo, kminta, regiek in TERMINOLOGIA:
            for nev, minta in [('kötelező: ' + kotelezo, kminta)] + [('régi: ' + n, m) for n, m in regiek]:
                osszes = len(re.findall(minta, s))
                mk = len(re.findall(MONDATKEZDO + '(?:' + minta + ')', s))
                if osszes:
                    ossz[(angol, nev, 'osszes')] += osszes
                    ossz[(angol, nev, 'mondatkezdo')] += mk
                    szocikk[(angol, nev)] += 1
                    if nev.startswith('régi'):
                        lista.append((strong, angol, kotelezo, nev[6:], str(osszes), str(mk)))
    if tsv_ir:
        with open(REGI_TSV, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# F103 (N-F103a): a DT167 (2) kötelező magyar alakjától eltérő (régi) bevezető-alakok a magyar BDB-szócikkekben, '
                    'szócikkenként. %s\n' % prov('magyar BDB (%d szócikk, a szerver bdb_magyar-szabálya)' % len(hu),
                                                 'forditasok.tsv@%s + naplok/F103_BDB_TAGOLAS_meres.py' % sha(FORD)))
            f.write('# A régi alak nem hiba a kész szövegben (DT167 (5) (a): csak mérés és lista, csere nincs); a mondatkezdő oszlop a '
                    'csoportot nyitó helyzet (; . : — után).\n')
            f.write('\t'.join(['strong', 'angol_bevezeto', 'kotelezo_alak', 'regi_alak', 'elofordulas', 'mondatkezdo']) + '\n')
            for sor in lista:
                f.write('\t'.join(sor) + '\n')
    return ossz, szocikk


def prov(scope, forras):
    return 'scope=%s | forras=%s | ts=%s' % (scope, forras, datetime.datetime.now().strftime('%Y-%m-%dT%H:%M'))


def teljes(en, hu, lem):
    ossz = collections.Counter()
    for strong, szoveg in en.items():
        r = B.szeletel(szoveg, lem.get(strong, ''))
        if not r:
            continue
        csoport_bont(r, 'en')
        cs = szeletelo_csoportok(r)
        for lst in cs.values():
            for c in lst:
                ossz['en_csoport'] += 1
                ossz['en_bev:' + (c['jel'] if not c['jel'].startswith('(') else '(zárójeles)')] += 1
        ossz['en_csoportos_szulo'] += len(cs)
        if strong in hu:
            ossz['hu_szocikk'] += 1
            rh = B.szeletel(hu[strong], lem.get(strong, ''))
            if not rh:
                continue
            csoport_bont(rh, 'hu')
            if hasattr(B, 'csoport_magyar'):
                B.csoport_magyar(rh, r)
            ch = szeletelo_csoportok(rh)
            ossz['hu_angol_csoportos_szulo'] += len(cs)
            ossz['hu_bontott_szulo'] += sum(1 for k in ch if k in cs)
            ossz['hu_bontott_csoport'] += sum(len(v) for k, v in ch.items() if k in cs)
            ossz['hu_bontott_angol_nelkul'] += sum(1 for k in ch if k not in cs)
    return ossz


def jelentespont():
    ki = subprocess.run([sys.executable, os.path.join(REPO, 'eszkozok', 'olvaso_szerver', 'm2_minta_osszevet.py'),
                         '--kulcs', os.path.join(REPO, 'naplok', 'BDB_SZELETELO_M2_minta_seed102_kulcs.tsv'),
                         '--kitoltott', os.path.join(REPO, 'naplok', 'BDB_SZELETELO_M2_seed102_kitoltott_A.tsv'),
                         os.path.join(REPO, 'naplok', 'BDB_SZELETELO_M2_seed102_kitoltott_B.tsv'), '--mai-tabla'],
                        capture_output=True, text=True, encoding='utf-8')
    return [s for s in ki.stdout.splitlines() if re.match(r'^(veletlen|konyv_vers_egyezik|jelentespont_egyezik|jelentespont_elotagkent_helyes)\t', s)]


def main():
    tsv_ir = '--tsv' in sys.argv
    en, hu, lem = bdb_en(), bdb_hu(), lemma_tabla()
    print('# F103 mérés: %s' % prov('aranyminta (adat/bdb_aranyminta.tsv) + teljes angol BDB (%d) + magyar BDB (%d)' % (len(en), len(hu)),
                                  'BDB_teljes_unabridged.tsv@%s + forditasok.tsv@%s + bdb_aranyminta.tsv@%s + bdb_szelet.py@%s (HEAD %s) '
                                  '+ naplok/F103_BDB_TAGOLAS_meres.py' % (sha(BDB_EN), sha(FORD), sha(ARANY),
                                                                          sha(B.__file__), commit())))
    print('# csoportbontás a szeletelőben: %s' % ('van' if hasattr(B, 'csoport_bont') else 'NINCS (bdb_szelet.csoport_bont hiányzik)'))
    ossz, hibak, hu_hibak = arany(en, hu, lem)
    print('\n## 1–2. Aranyminta')
    for k in sorted(ossz):
        print('%s\t%d' % (k, ossz[k]))
    print('\n### Angol eltérések (%d)' % len(hibak))
    for h in hibak:
        print(h)
    print('\n### Magyar eltérések (%d)' % len(hu_hibak))
    for h in hu_hibak:
        print(h)
    print('\n## 3–4. Teljes BDB')
    t = teljes(en, hu, lem)
    for k in sorted(t):
        print('%s\t%d' % (k, t[k]))
    print('\n## 5. Terminológia (DT167 (2)), magyar BDB')
    o, sz = terminologia(hu, tsv_ir)
    print('angol\talak\tszócikk\tösszes\tmondatkezdő')
    for angol, kotelezo, _, regiek in TERMINOLOGIA:
        for nev in ['kötelező: ' + kotelezo] + ['régi: ' + n for n, _ in regiek]:
            print('%s\t%s\t%d\t%d\t%d' % (angol, nev, sz[(angol, nev)], o[(angol, nev, 'osszes')], o[(angol, nev, 'mondatkezdo')]))
    print('\n## 6. Jelentéspont (seed-102, m2_minta_osszevet.py --mai-tabla)')
    for s in jelentespont():
        print(s)


if __name__ == '__main__':
    main()
