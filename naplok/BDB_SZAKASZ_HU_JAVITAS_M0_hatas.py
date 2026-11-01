r"""F144 M0: a javítási szabályváltozatok hatásbecslése (csak olvas, memóriában; adatot nem ír). A `hu_illeszt.py` illesztőjének
másolata, kapcsolható szabályokkal; az alap (minden kapcsoló ki) a `hu_illeszt.strong_illeszt`-tel azonos eredményt ad.
  R1  : a törzsnév csak tagolásjel után jelölő (a szöveg eleje, „. ”, „; ”, „: ”, „— ”, „) ”) — elvetve (241 sor, ép sorokat ront);
  R1e : R1 kivétellel: a forrássor saját angol szövege legfeljebb 8 karakter — elvetve;
  R2  : a vesszős kötetszámú siglum („CIS^iv, 1, 37 ”) utáni számsor nem jelölő (`\^[ivx]+,(?:\s?\d+[.,]?)+\s$`);
  R3  : előretekintés: a jelölő nem köthető olyan helyre, amely előtt (a kurzortól) a következő jelölős sor első jelölője áll — elvetve;
  R3t : R3, csak ha a következő jelölő törzsnév és a mostani nem — elvetve (a következő törzsnév korábbi említése miatt ép sort ront);
  R3x : R3t, de a következő törzsnév a forrás szerinti előfordulás-indexével (l. R4);
  R4  : a törzsnév-jelölő a magyarban annyiadik előfordulásához kötődik, ahány azonos törzsnév áll előtte az angol forrásban
        (a forrás sorainak `jel` + `szoveg` mezője, címkék nélkül); ha ilyen nincs vagy a kurzor előtt van, a mai viselkedés.
Használat: python naplok/BDB_SZAKASZ_HU_JAVITAS_M0_hatas.py [kimenet.txt]  (a soronkénti lista a kimeneti fájlba)
TSV: split('\t'), csv modul nélkül."""
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KI = sys.argv[1] if len(sys.argv) > 1 else os.devnull
sys.path.insert(0, os.path.join(GY, 'eszkozok', 'bdb_jelolt'))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import hu_illeszt as hi  # noqa
import szakasz_bemenet as sb  # noqa

TAGOLAS_ELOTT = re.compile(r'(?:^|[.;:—)]\s)$')
SIGLUM_SOR = re.compile(r'\^[ivx]+,(?:\s?\d+[.,]?)+\s$')


def mj_valtozat(hu, r1, r2):
    ki = []
    for p, j in hi.magyar_jelolok(hu):
        if r1 and j.startswith('T:') and not TAGOLAS_ELOTT.search(hu[max(0, p - 3):p]):
            ki.append((p, j, 'r1'))
            continue
        if r2 and not j.startswith('T:') and SIGLUM_SOR.search(hu[max(0, p - 40):p]):
            continue
        ki.append((p, j, ''))
    return ki


def illeszt(sorok, hu, r1=False, r1e=False, r2=False, r3=False, r3t=False, r4=False, r3x=False):
    mj = mj_valtozat(hu, r1, r2)
    en_elotte = []
    acc = ''
    for x in sorok:
        en_elotte.append(acc)
        acc += ' ' + x['jel'] + ' ' + re.sub(r'<[^>]+>', '', x['szoveg'])
    jelek_l = [hi.forras_jelolok(x['jel']) if x['jelolo'] in ('point', 'section', 'remarks') else [] for x in sorok]
    kurzor = 0
    ered = []
    for i, x in enumerate(sorok):
        jelek = jelek_l[i]
        if not jelek:
            ered.append(['jelolo_nelkul', '', None])
            continue
        ures = len(re.sub(r'<[^>]+>', '', x['szoveg']).strip()) <= 8
        engedett = lambda m: m[2] == '' or (r1e and ures)  # noqa
        kov = next((jl[0] for jl in jelek_l[i + 1:] if jl), None)
        kovi = next((t for t in range(i + 1, len(sorok)) if jelek_l[t]), None)
        poz, k = [], kurzor
        for j in jelek:
            hol = next((t for t in range(k, len(mj)) if mj[t][1] == j and engedett(mj[t])), None)
            if r4 and j.startswith('T:') and hol is not None:
                kk = sum(1 for m in hi.TORZS_HU.finditer(en_elotte[i]) if 'T:' + hi.torzs_kulcs(m.group(1)) == j)
                elof = [t for t in range(len(mj)) if mj[t][1] == j]
                if kk < len(elof) and elof[kk] >= k:
                    hol = elof[kk]
            if hol is None:
                poz = None
                break
            if r3x and not poz and kov and kov.startswith('T:') and not j.startswith('T:'):
                kk = sum(1 for m in hi.TORZS_HU.finditer(en_elotte[kovi]) if 'T:' + hi.torzs_kulcs(m.group(1)) == kov)
                elof = [t for t in range(len(mj)) if mj[t][1] == kov]
                if kk < len(elof) and k <= elof[kk] < hol:
                    poz = None
                    break
            if (r3 or (r3t and kov and kov.startswith('T:') and not j.startswith('T:'))) and not poz and kov and kov != j:
                elotte = next((t for t in range(k, hol) if mj[t][1] == kov and mj[t][2] == ''), None)
                if elotte is not None:
                    poz = None
                    break
            poz.append(mj[hol][0])
            k = hol + 1
        if poz:
            ered.append(['illeszkedik', ' '.join(jelek), poz[0]])
            kurzor = k
        else:
            ered.append(['elakad', ' '.join(jelek), None])
    # a horgony-lépés az eredetiből (változatlan kód, szövegesen másolva)
    for i, (x, e) in enumerate(zip(sorok, ered)):
        if e[0] != 'elakad':
            continue
        also = max([r[2] for r in ered[:i] if r[2] is not None] or [0])
        felso = min([r[2] for r in ered[i + 1:] if r[2] is not None and r[0] == 'illeszkedik'] or [len(hu)])
        m = hi.REF.search(x['szoveg'])
        if not m:
            continue
        p = hu.find(m.group(0), also + 1 if also else 0)
        if 0 <= p < felso and p > also:
            jel0 = next((j for j in hi.forras_jelolok(x['jel']) if not j.startswith('T:')), None)
            eleje = None
            if jel0:
                talalat = [t.start() for t in re.finditer(r'(?<!\S)' + re.escape(jel0) + r'\.?(?=\s)', hu[also:p])]
                if talalat:
                    eleje = also + talalat[-1]
            if eleje is None:
                hatar = max(hu.rfind('. ', also, p), hu.rfind('; ', also, p), hu.rfind('— ', also, p))
                eleje = (hatar + 2) if hatar > also else p
            e[:] = ['horgonnyal', m.group(0), eleje]
    return ered


def szovegek(sorok, hu, ered):
    poz = sorted(set([0] + [e[2] for e in ered if e[2] is not None]))
    ki = []
    for x, e in zip(sorok, ered):
        kat, _, p = e
        if x['sorszam'] in ('1', '2') and kat == 'jelolo_nelkul' and x['utvonal'] in ('cim', 'fej'):
            p = 0 if x['sorszam'] == '1' or x['utvonal'] == 'fej' else None
        if x['sorszam'] == '1':
            p = None
        if x['sorszam'] == '2' and p is None and x['utvonal'] == 'fej':
            p = 0
        if p is not None:
            kov = next((q for q in poz if q > p), len(hu))
            ki.append((kat, hu[p:kov].strip()))
        else:
            ki.append((kat, ''))
    return ki


def A(kat, jel, sz):
    return kat == 'illeszkedik' and jel and len(sz) <= len(jel) + 3


ford = hi.forditasok()
with open(hi.FORD, encoding='utf-8', newline='') as f:
    fs = [x.rstrip('\r') for x in f.read().split('\n') if x and not x.startswith('#')]
ff = fs[0].split('\t')
bdb = collections.defaultdict(list)
for x in fs[1:]:
    d = dict(zip(ff, x.split('\t')))
    if d['szotar'] == 'BDB':
        bdb['H%04d' % int(re.sub(r'\D', '', d['strong']))].append(d)
tipus = {st: sb.strong_magyar_sorok(ds)[1] for st, ds in bdb.items()}
with open(hi.TABLA, encoding='utf-8', newline='') as f:
    s = f.read().split('\n')
tf = s[2].split('\t')
tab = collections.OrderedDict()
for x in s[3:]:
    if x:
        d = dict(zip(tf, x.split('\t')))
        tab.setdefault(d['strong'], []).append(d)

VALT = collections.OrderedDict([
    ('R1', dict(r1=True)), ('R1+R1e', dict(r1=True, r1e=True)), ('R2', dict(r2=True)), ('R3', dict(r3=True)),
    ('R3t', dict(r3t=True)), ('R3x', dict(r3x=True)), ('R4', dict(r4=True)), ('R2+R4+R3x', dict(r2=True, r4=True, r3x=True))])
ki = []
p = ki.append
reszlet = {}
for nev, opc in VALT.items():
    for tip in ('teljes', 'szakasz'):
        valt_sor, valt_str, kat_elotte, kat_utana = 0, set(), collections.Counter(), collections.Counter()
        a_e = a_u = 0
        lista = []
        for st in sorted(ford):
            if st not in tab or tipus.get(st) != tip:
                continue
            sorok, hu = tab[st], ford[st]['forditas_hu']
            e0 = illeszt(sorok, hu)
            e1 = illeszt(sorok, hu, **opc)
            s0, s1 = szovegek(sorok, hu, e0), szovegek(sorok, hu, e1)
            for x, a, b in zip(sorok, s0, s1):
                kat_elotte[a[0]] += 1
                kat_utana[b[0]] += 1
                a_e += A(a[0], x['jel'], a[1])
                a_u += A(b[0], x['jel'], b[1])
                if a != b:
                    valt_sor += 1
                    valt_str.add(st)
                    lista.append('%s %s (%s): %s %d → %s %d' % (st, x['sorszam'], x['jel'] or '-', a[0], len(a[1]), b[0], len(b[1])))
        p('## %s · típus=%s: változó sor %d, Strong %d; A-sor %d → %d' % (nev, tip, valt_sor, len(valt_str), a_e, a_u))
        p('   kategória előtte %s' % dict(kat_elotte))
        p('   kategória utána  %s' % dict(kat_utana))
        p('   Strongok: ' + ' '.join(sorted(valt_str)))
        reszlet[(nev, tip)] = lista
p('')
for (nev, tip), lista in reszlet.items():
    if tip == 'teljes':
        p('### %s · teljes — változó sorok' % nev)
        ki.extend('   ' + x for x in lista)
with open(KI, 'w', encoding='utf-8') as f:
    f.write('\n'.join(ki) + '\n')
print('\n'.join(x for x in ki if x.startswith('##') or x.startswith('   kat') or x.startswith('   Str')))
