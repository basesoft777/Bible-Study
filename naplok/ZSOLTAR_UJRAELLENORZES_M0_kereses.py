"""F55 M0 — a zsoltárhivatkozások keresése a kézi forrásrétegben, és a régi
LXX_kivonat_Zsoltarok.tsv (a git-történetből: 0c2d1b44^, az F42.12 törlés előtti állapot)
újra-összevetése a mai LXX_OS-sel (a #54 után), az eszkozok/lxx_osszevetes.py kategóriáival.

    python naplok/ZSOLTAR_UJRAELLENORZES_M0_kereses.py

Kimenet: naplok/ZSOLTAR_UJRAELLENORZES_M0_talalatok.tsv (a forrás-, archív- és adatréteg
minden zsoltárhivatkozása, kategóriával), a kategória-változások a stdout-on.
A generált és próba-fájlok (lexikon/, generalt_proba/, motivumlog/lexikon_pilot/) csak számolva.
Proveniencia: manual (összevetés és szövegkeresés, nem lekerdez.py-lekérdezés)."""
import collections
import glob
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import lxx_osszevetes as LO  # noqa: E402

# --- 1. fájlkör ---
KOR = {
    'forras': ['tematikus_lezart/**/*.md', 'genezis/**/*.md', 'ujszovetseg/**/*.md',
               'melyelemzesek/**/*.md', 'motivumok/**/*.md', 'motivumlog/*.md'],
    'archiv': ['archivum/ISTENTISZT-001/*.md'],
    'adat': ['adat/jeloltek.tsv', 'adat/auditok.tsv', 'adat/elofordulasok.tsv', 'adat/lxx_dontesek.tsv',
             'adat/kapcsolatok.tsv'],
    'kizart_jelolt': ['motivumlog/lexikon_pilot/**/*', 'generalt_proba/**/*', 'lexikon/*.md'],
}
GOROG = re.compile(r'[Ͱ-Ͽἀ-῿]')
GSTRONG = re.compile(r'\bG\d{3,4}\b')
LXXSZO = re.compile(r'LXX|Septuaginta|ἐπικαλ|görög', re.I)
ZS = re.compile(r'(Zsolt(?:ár)?\.?|Psalm|Ps)\s*(\d+)\s*[:,.]\s*(\d+)((?:\s*[–\-]\s*\d+(?![\d:])|\s*,\s*\d+(?![\d:]))*)')
FOLYT = re.compile(r'^\s*(?:/|;|,|és)\s*(\d+):(\d+)((?:\s*[–\-]\s*\d+(?![\d:]))?)')


def versek(fej, vers, tobb):
    out = [(int(fej), int(vers))]
    for m in re.finditer(r'([–\-,])\s*(\d+)', tobb or ''):
        v = int(m.group(2))
        if m.group(1) in '–-':
            out += [(int(fej), x) for x in range(out[-1][1] + 1, v + 1)]
        else:
            out.append((int(fej), v))
    return out


def keres(sor):
    talalt = []
    for m in ZS.finditer(sor):
        talalt += versek(m.group(2), m.group(3), m.group(4))
        rest = sor[m.end():]
        while True:
            f = FOLYT.match(rest)
            if not f:
                break
            talalt += versek(f.group(1), f.group(2), f.group(3))
            rest = rest[f.end():]
    return talalt


# --- 2. régi vs új index (Zsoltárok) ---
uj = LO.uj_index()
regi = collections.defaultdict(list)
_regi = subprocess.run(['git', 'show', '0c2d1b44^:konkordancia/LXX_kivonat_Zsoltarok.tsv'],
                       capture_output=True, check=True).stdout.decode('utf-8').split('\n')
fej = _regi[0].rstrip('\r').split('\t')
for ln in _regi[1:]:
    if not ln.strip():
        continue
    p = ln.rstrip('\r').split('\t')
    r = dict(zip(fej, p))
    regi[r['Igehely']].append(r)


def kat(vers):
    rr = regi.get(vers, [])
    ur = uj.get(vers, [])
    if not rr:
        return 'csak_uj_vers' if ur else 'nincs_egyikben'
    if not ur:
        return 'csak_regi_vers'
    rs = {k: v for k, v in collections.Counter(LO.norm_strong(r['Strong-szám']) for r in rr).items() if k}
    us = {k: v for k, v in collections.Counter(LO.norm_strong(r['strong']) for r in ur).items() if k}
    if rs == us:
        return 'azonos'
    j = LO.jaccard(collections.Counter(rs), collections.Counter(us))
    k = 'strong_eltero' if j >= 0.8 else 'nagy_eltero'
    if k == 'nagy_eltero':
        kov = uj.get(LO.kovetkezo_vers(vers), [])
        if kov:
            ks = {k2: v for k2, v in collections.Counter(LO.norm_strong(r['strong']) for r in kov).items() if k2}
            if LO.jaccard(collections.Counter(rs), collections.Counter(ks)) >= 0.8:
                k = 'zsoltar_eltolas'
    return k


# eltéréslista (F42, 2026-10-05)
elt = {}
with open('naplok/FORRASKIVEZETES_M5_eltereslista.tsv', encoding='utf-8') as f:
    for ln in f:
        if ln.startswith('#') or ln.startswith('igehely'):
            continue
        p = ln.rstrip('\r\n').split('\t')
        if p[0].startswith('Zsolt '):
            elt[p[0]] = p[1]

# teljes újraszámítás a Zsoltárokra
uj_kat = {}
for v in set(regi) | {k for k in uj if k.startswith('Zsolt ')}:
    uj_kat[v] = kat(v)
cnt_ma = collections.Counter(uj_kat.values())
cnt_f42 = collections.Counter(elt.values())
valt = [(v, elt.get(v, 'azonos'), uj_kat[v]) for v in sorted(uj_kat) if elt.get(v, 'azonos') != uj_kat[v]]
print('F42 kategóriák (Zsolt):', dict(cnt_f42))
print('ma (a #54 után):', dict(cnt_ma))
print('kategória-változás F42 -> ma:', len(valt))
vc = collections.Counter((a, b) for _, a, b in valt)
for k, n in vc.most_common():
    print('   ', k, n)
for v, a, b in valt:
    print('   valtozas\t%s\t%s\t%s' % (v, a, b))

ERINTETT = {'zsoltar_eltolas', 'csak_regi_vers'}

# --- 3. keresés ---
ki = []
stat = collections.Counter()
for reteg, minták in KOR.items():
    fajlok = sorted({p for m in minták for p in glob.glob(m, recursive=True) if os.path.isfile(p)})
    stat[reteg + '_fajl'] = len(fajlok)
    for p in fajlok:
        try:
            sorok = open(p, encoding='utf-8').read().split('\n')
        except UnicodeDecodeError:
            continue
        for i, s in enumerate(sorok, 1):
            vv = keres(s)
            if not vv:
                continue
            gor = bool(GOROG.search(s)) or bool(GSTRONG.search(s)) or bool(LXXSZO.search(s))
            for (c, v) in vv:
                vers = 'Zsolt %d:%d' % (c, v)
                stat[reteg + '_hiv'] += 1
                if gor:
                    stat[reteg + '_hiv_gorog'] += 1
                k42 = elt.get(vers, 'azonos' if vers in regi else 'nincs_regiben')
                kma = uj_kat.get(vers, 'nincs_egyikben')
                ki.append([reteg, p.replace('\\', '/'), str(i), vers, 'igen' if gor else 'nem', k42, kma,
                           s.strip()[:160].replace('\t', ' ')])
print(dict(stat))
with open('naplok/ZSOLTAR_UJRAELLENORZES_M0_talalatok.tsv', 'w', encoding='utf-8', newline='\n') as f:
    f.write('# GENERÁLT: naplok/ZSOLTAR_UJRAELLENORZES_M0_kereses.py — kézzel nem szerkesztendő.\n')
    f.write('# proveniencia: scope=zsoltárhivatkozás-keresés (forras, archiv, adat réteg) + '
            'LXX_kivonat_Zsoltarok@0c2d1b44^ vs LXX_OS | forras=manual | ts=2026-10-19\n')
    f.write('reteg\tfajl\tsor\tvers\tgorog_kontextus\tkat_F42\tkat_ma\tszoveg\n')
    for r in ki:
        if r[0] != 'kizart_jelolt':
            f.write('\t'.join(r) + '\n')
er = [r for r in ki if r[4] == 'igen' and (r[5] in ERINTETT or r[6] in ERINTETT)]
print('szűrt (görög kontextus + zsoltar_eltolas/csak_regi_vers, F42 vagy ma):', len(er),
      '— ebből nem generált/próba:', sum(1 for r in er if r[0] != 'kizart_jelolt'))
for r in sorted({tuple(r[:7]) for r in er if r[0] != 'kizart_jelolt'}):
    print('   szurt\t' + '\t'.join(r))
