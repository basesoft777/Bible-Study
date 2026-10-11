"""F54 / M0 -- az 503 `csak_regi_vers` Karoli-vers osztalyozasa (csak olvas).

Kimenet: naplok/LXX_OS_LEFEDETTSEG_osztalyozas.tsv (versenkenti tabla) es
osszesites a stdout-ra. Nem ir semmilyen adattablat.

Bemenet (mind a repobol):
  - naplok/FORRASKIVEZETES_M5_eltereslista.tsv (kategoria = csak_regi_vers)
  - konkordancia/LXX_OS/<elsodleges slug>.tsv (karoli_ok, igehely_karoli, igehely_kjv)
  - konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/Karoli_1908.tsv
  - a regi LXX_kivonat (git: 0c2d1b44^, az F42.12 torles elotti allapot) -- CSAK
    osszehasonlitasi bizonyitek (regi_helyes), nem kulcsforras.

Modszer-korlat (CLAUDE.md 3. szabaly): a besorolas gepi mutatokra epul (tabla,
szoalak-Jaccard, szoszam-korrelacio); a proveniencia `manual` (osszevetes, nem
lekerdez.py-kimenet). Bizonytalan esetet nem sorol A-ba.
"""
import sys
import re
import math
import collections
import subprocess
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')).replace('\\', '/') + '/'
sys.path.insert(0, R + 'eszkozok')
import lxx_os_import as L  # noqa: E402

TS = '2026-10-11'
TORLES_ELOTT = '0c2d1b44^'
OLD = {'2Móz': 'Exodus', '4Móz': 'Numeri', 'Józs': 'Jozsue', '1Sám': 'Samuel_1', '1Kir': 'Kiralyok_1',
       'Jób': 'Job', 'Zsolt': 'Zsoltarok', 'Péld': 'Peldabeszedek', 'Én': 'Enekek_Eneke', 'Ézs': 'Ezsaias',
       'Jer': 'Jeremias', 'Dán': 'Daniel', 'Hós': 'Hoseas', 'Jón': 'Jonas'}


def nf(s):
    return s.replace('ς', 'σ').lower()


def jac(a, b):
    a = set(a)
    b = set(b)
    return len(a & b) / len(a | b) if (a | b) else 0.0


def pear(x, y):
    n = len(x)
    if n < 3:
        return None
    mx = sum(x) / n
    my = sum(y) / n
    sx = sum((a - mx) ** 2 for a in x)
    sy = sum((b - my) ** 2 for b in y)
    if sx == 0 or sy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sx * sy)


def split_ref(g):
    m = re.match(r'^(.+) (\d+):(\d+)$', g)
    return m.group(1), int(m.group(2)), int(m.group(3))


# --- betoltes -------------------------------------------------------------------------
gap = []
for l in open(R + 'naplok/FORRASKIVEZETES_M5_eltereslista.tsv', encoding='utf-8'):
    p = l.rstrip('\n').split('\t')
    if len(p) > 2 and p[1] == 'csak_regi_vers':
        gap.append((p[0], int(p[2])))

tab = {}
for l in open(R + 'konkordancia/Karoli_versmegfeleltetes.tsv', encoding='utf-8'):
    if l.startswith('#') or l.startswith('igehely_karoli'):
        continue
    p = l.rstrip('\n').split('\t')
    tab[p[0]] = p

kar = {}
for l in open(R + 'konkordancia/Karoli_1908.tsv', encoding='utf-8'):
    a, b = l.rstrip('\n').split('\t')
    kar[a] = len(b.split())

_old = {}


def old(book):
    if book in _old:
        return _old[book]
    txt = subprocess.run(['git', '-C', R, 'show', '%s:konkordancia/LXX_kivonat_%s.tsv' % (TORLES_ELOTT, OLD[book])],
                         capture_output=True, check=True).stdout.decode('utf-8')
    d = collections.defaultdict(list)
    for l in txt.split('\n'):
        p = l.split('\t')
        if len(p) >= 3:
            d[p[0]].append(nf(p[2]))
    _old[book] = d
    return d


_lx = {}


def lxx(slug):
    if slug in _lx:
        return _lx[slug]
    rows = {}
    for l in open(R + 'konkordancia/LXX_OS/%s.tsv' % slug, encoding='utf-8'):
        if l.startswith('#') or l.startswith('igehely_lxx'):
            continue
        p = l.rstrip('\n').split('\t')
        r = rows.setdefault(p[0], {'kjv': p[1], 'kar': p[2], 'ok': p[3], 'forms': []})
        r['forms'].append(nf(p[6]))
    _lx[slug] = rows
    return rows


def lxx_chapter(rows, c):
    """{vers: (igehely_lxx, szoszam)} az LXX-fejezetre (a fejezetszam az igehely_lxx szerint)."""
    d = {}
    for k, r in rows.items():
        m = re.match(r'^(.*) (\d+):(\d+)$', k)
        if m and int(m.group(2)) == c:
            d[int(m.group(3))] = (k, len(r['forms']))
    return d


def karoli_chapter(b, c):
    d = {}
    for k, n in kar.items():
        if k.startswith('%s %d:' % (b, c)):
            d[int(k.split(':')[1])] = n
    return d


def r_offset(kc, lc, s):
    xs, ys = [], []
    for v, n in kc.items():
        if v + s in lc:
            xs.append(n)
            ys.append(lc[v + s][1])
    return pear(xs, ys), len(xs)


def kjv_list(s):
    return [x for x in s.split(';') if x]



# --- sorrend-beagyazas: a nem kulcsolt Karoli-vers a kulcsolt szomszedai kozotti LXX-szakaszhoz parosul
_ord = {}
_kar_sorted = {}


def lxx_order(slug):
    """fajlsorrendu LXX-igehely lista + {Karoli-kulcs: [LXX-igehely]}"""
    if slug in _ord:
        return _ord[slug]
    rows = lxx(slug)
    order = list(rows.keys())
    idx = {k: i for i, k in enumerate(order)}
    of = collections.defaultdict(list)
    for k in order:
        if rows[k]['kar']:
            of[rows[k]['kar']].append(k)
    _ord[slug] = (order, idx, of)
    return _ord[slug]


def kar_sorted(b):
    if b not in _kar_sorted:
        lst = []
        for k in kar:
            m = re.match(r'^(.+) (\d+):(\d+)$', k)
            if m and m.group(1) == b:
                lst.append((int(m.group(2)), int(m.group(3)), k))
        lst.sort()
        _kar_sorted[b] = lst
    return _kar_sorted[b]


def beagyazas(b, c, v, slug):
    """-> (allapot, cel_lxx, reszlet). allapot: pair | ures | eltero_hossz | n/a"""
    order, idx, of = lxx_order(slug)
    ks = kar_sorted(b)
    pos = [i for i, (cc, vv, k) in enumerate(ks) if (cc, vv) == (c, v)]
    if not pos:
        return 'n/a', '', 'nincs Karoli-vers'
    i = pos[0]
    pred = succ = None
    for j in range(i - 1, -1, -1):
        if ks[j][2] in of:
            pred = j
            break
    for j in range(i + 1, len(ks)):
        if ks[j][2] in of:
            succ = j
            break
    if pred is None or succ is None:
        return 'n/a', '', 'nincs kulcsolt szomszed'
    if len(of[ks[pred][2]]) != 1 or len(of[ks[succ][2]]) != 1:
        return 'n/a', '', 'kettos kulcsu szomszed'
    P = of[ks[pred][2]][0]
    N = of[ks[succ][2]][0]
    if idx[P] >= idx[N]:
        return 'n/a', '', 'nem monoton szomszedok (%s -> %s)' % (P, N)
    s_lxx = order[idx[P] + 1:idx[N]]
    if any(lxx(slug)[k]['kar'] for k in s_lxx):
        return 'n/a', '', 'a szakaszban kulcsolt LXX-vers van'
    s_k = [ks[j][2] for j in range(pred + 1, succ)]
    det = 'szomszedok: %s=%s es %s=%s; LXX-szakasz %d vers, Karoli-szakasz %d vers' % (ks[pred][2], P, ks[succ][2], N, len(s_lxx), len(s_k))
    if len(s_lxx) == 0:
        return 'ures', '', det
    if len(s_lxx) != len(s_k):
        return 'eltero_hossz', '', det
    return 'pair', s_lxx[s_k.index(g_of(b, c, v))], det


def g_of(b, c, v):
    return '%s %d:%d' % (b, c, v)


_kjvi = {}


def kjv_index(slug):
    """{kjv-hivatkozas: [nem kulcsolt es kulcsolt LXX-versek]} -- csak az egyertelmu (1 elemu) listak hasznosak"""
    if slug in _kjvi:
        return _kjvi[slug]
    d = collections.defaultdict(list)
    for k, r in lxx(slug).items():
        for x in kjv_list(r['kjv']):
            d[x].append(k)
    _kjvi[slug] = d
    return d


# --- osztalyozas ------------------------------------------------------------------------
rec = []
for g, regi_n in gap:
    b, c, v = split_ref(g)
    slug = L.elsodleges_slug(b)
    rows = lxx(slug)
    of = old(b).get(g, [])
    t = tab.get(g)
    kw = kar.get(g, 0)
    # a regi szoveg legjobb LXX-egyezese az egesz konyvben
    best = (0.0, '', '')
    for k, r in rows.items():
        j = jac(of, r['forms'])
        if j > best[0]:
            best = (j, k, r['kar'])
    cand = []
    if t:
        tk = t[1]
        cand = [k for k, r in rows.items() if tk in kjv_list(r['kjv']) and not r['kar']]
    rec.append(dict(g=g, b=b, c=c, v=v, regi_n=regi_n, kw=kw, slug=slug, t=t, cand=cand, best=best,
                    of=len(of)))

by_ch = collections.defaultdict(list)
for r in rec:
    by_ch[(r['b'], r['c'])].append(r)

out = []
for r in rec:
    g, b, c, v, kw, slug, t, cand, best = r['g'], r['b'], r['c'], r['v'], r['kw'], r['slug'], r['t'], r['cand'], r['best']
    rows = lxx(slug)
    kc = karoli_chapter(b, c)
    emb, emb_cel, emb_det = beagyazas(b, c, v, slug) if kw else ('n/a', '', '')
    o = dict(igehely=g, konyv=b, regi_n=r['regi_n'], karoli_szo=kw, letezik_karoli='igen' if kw else 'nem',
             tabla_kjv=t[1] if t else '', tabla_osztaly=t[3] if t else '',
             cand_lxx=';'.join(cand), beagyazas=emb + (':' + emb_cel if emb_cel else ''),
             regi_legjobb_lxx=best[1], regi_jaccard='%.2f' % best[0],
             regi_legjobb_kulcs=best[2], regi_helyes='', fej_r='', fej_offset='',
             osztaly='', alosztaly='', javasolt_lxx='', kulcs_forras='', indok='')
    # --- C: nem letezo Karoli-vers
    if not kw:
        o.update(osztaly='C', alosztaly='nem_letezo_karoli_vers',
                 indok='a regi kivonat nem letezo Karoli-versre (%s) adott szoveget; a Karoli_1908.tsv-ben nincs ilyen vers, kulcs nem keletkezhet (K4 idegen kulcs)' % g,
                 kulcs_forras='-')
        o['regi_helyes'] = 'nem'
        out.append(o)
        continue

    def hossz_ok(lv):
        n = len(rows[lv]['forms'])
        ratio = n / kw
        return 0.4 <= ratio <= 2.5, ratio

    def fej_adat(lv):
        m = re.match(r'^(.*) (\d+):(\d+)$', lv)
        lc_ch, lv_n = int(m.group(2)), int(m.group(3))
        lcd = lxx_chapter(rows, lc_ch)
        s = lv_n - v
        rr, nn = r_offset(kc, lcd, s)
        o['fej_r'] = '' if rr is None else '%.2f' % rr
        o['fej_offset'] = str(s)
        return rr, s, lv_n

    # Zsolt: kettos feliratvers, sorrendi parositas
    if b == 'Zsolt' and v == 2 and not cand:
        prev = [x for x in rec if x['g'] == 'Zsolt %d:1' % c and len(x['cand']) == 2]
        if prev:
            lv = prev[0]['cand'][1]
            o.update(osztaly='A', alosztaly='A1_zsolt_cim', javasolt_lxx=lv, regi_helyes='nem',
                     kulcs_forras='Karoli_versmegfeleltetes.tsv (Zsolt %d:1 -> kjv %d:1 -> 2 jelolt: %s; sorrendi parositas)' % (c, c, ';'.join(prev[0]['cand'])),
                     indok='masodik feliratvers: a Karoli Zsolt %d:2 a %s-hoz tartozik (a regi szoveg a %s-ra mutat, a nem-cim versre: eltolt)' % (c, lv, best[1]))
            out.append(o)
            continue

    target_t = cand[0] if (len(cand) == 1 or (b == 'Zsolt' and v == 1 and len(cand) == 2)) else ''
    if target_t:
        rr, s, lv_n = fej_adat(target_t)
        regi_egyezik = (best[1] == target_t and best[0] >= 0.5)
        o['regi_helyes'] = 'igen' if regi_egyezik else 'nem'
        ok_h, ratio = hossz_ok(target_t)
        if emb == 'pair' and emb_cel != target_t:
            o.update(osztaly='bizonytalan', alosztaly='tabla_beagyazas_ellentmondas', javasolt_lxx=target_t,
                     kulcs_forras='Karoli_versmegfeleltetes.tsv',
                     indok='tabla-jelolt %s, de a sorrend-beagyazas %s-t adja (%s)' % (target_t, emb_cel, emb_det))
        elif b == 'Zsolt' and v in (1, 2) and lv_n in (1, 2):
            o.update(osztaly='A', alosztaly='A1_zsolt_cim', javasolt_lxx=target_t,
                     kulcs_forras='Karoli_versmegfeleltetes.tsv (%s -> kjv %s) + LXX %s igehely_kjv egyezes; dup-KJV-cel miatt nem kulcsolt' % (g, t[1], target_t),
                     indok='feliratvers: a Karoli %s es az LXX %s is a zsoltar elso (felirat)verse, a tobbi vers eltolasa azonos (d=%d)%s'
                           % (g, target_t, s, '; ket feliratvers: sorrendi parositas' if len(cand) == 2 else ''))
        elif regi_egyezik or (rr is not None and rr >= 0.6) or emb == 'pair':
            if not ok_h:
                o.update(osztaly='bizonytalan', alosztaly='szoszam_aranytalan', javasolt_lxx=target_t,
                         kulcs_forras='Karoli_versmegfeleltetes.tsv',
                         indok='tabla-jelolt %s, de a szoszam-arany (LXX/Karoli) %.2f kivul esik [0,4; 2,5]-on' % (target_t, ratio))
            else:
                tamasz = []
                if regi_egyezik:
                    tamasz.append('a regi szoveg szoalak-Jaccardja %.2f (egyezik)' % best[0])
                if emb == 'pair':
                    tamasz.append('sorrend-beagyazas ugyanezt adja')
                if rr is not None and rr >= 0.6:
                    tamasz.append('fejezet-szoszamkorrelacio r=%.2f' % rr)
                o.update(osztaly='A', alosztaly='A1_tabla', javasolt_lxx=target_t,
                         kulcs_forras='Karoli_versmegfeleltetes.tsv (%s -> kjv %s -> LXX %s)' % (g, t[1], target_t),
                         indok='tabla-jelolt egyedi, nem kulcsolt; ' + '; '.join(tamasz) + ('' if regi_egyezik else '; a regi szoveg mas versre mutat (%s)' % best[1]))
        else:
            o.update(osztaly='bizonytalan', alosztaly='tabla_jelolt_alatamasztas_nelkul', javasolt_lxx=target_t,
                     kulcs_forras='Karoli_versmegfeleltetes.tsv',
                     indok='tabla-jelolt %s, de sem a regi szoveg (Jaccard %.2f -> %s), sem a fejezet-szoszamkorrelacio (r=%s), sem a sorrend-beagyazas nem tamasztja ala'
                           % (target_t, best[0], best[1], o['fej_r'] or 'n/a'))
        out.append(o)
        continue

    # --- nincs egyertelmu tabla-jelolt: sorrend-beagyazas
    if emb == 'pair':
        lv = emb_cel
        rr, s, lv_n = fej_adat(lv)
        regi_egyezik = (best[1] == lv and best[0] >= 0.5)
        o['regi_helyes'] = 'igen' if regi_egyezik else 'nem'
        ok_h, ratio = hossz_ok(lv)
        if ok_h:
            o.update(osztaly='A', alosztaly='A3_sorrend_beagyazas', javasolt_lxx=lv,
                     kulcs_forras='NINCS egyertelmu tabla-jelolt (%s); a kulcsolt szomszedok adjak: %s' % (('kjv %s' % t[1]) if t else 'nincs tabla-sor', emb_det),
                     indok='sorrend-beagyazas: a nem kulcsolt LXX-szakasz es a nem kulcsolt Karoli-szakasz hossza egyezik; szoszam-arany %.2f; regi szoveg %s'
                           % (ratio, 'egyezik' if regi_egyezik else 'mas versre mutat (%s)' % best[1]))
        else:
            o.update(osztaly='bizonytalan', alosztaly='szoszam_aranytalan', javasolt_lxx=lv, kulcs_forras='-',
                     indok='sorrend-beagyazas %s-t adja, de a szoszam-arany %.2f kivul esik [0,4; 2,5]-on (%s)' % (lv, ratio, emb_det))
        out.append(o)
        continue
    if emb == 'ures':
        tk_van = bool(t) and any(t[1] in kjv_list(rr_['kjv']) for rr_ in rows.values())
        o.update(osztaly='B', alosztaly='B_ures_lxx_szakasz', kulcs_forras='-',
                 indok='a kulcsolt szomszedok kozott nincs LXX-vers, de van Karoli-vers: %s%s; a regi szoveg legjobb egyezese %s (Jaccard %.2f, kulcsa: %s) mas versre mutat'
                       % (emb_det, ('; a tabla kjv-je (%s) szerepel LXX-versnel' % t[1]) if tk_van else ('; egyetlen LXX-vers kjv-mezoje sem %s' % t[1] if t else ''),
                          best[1], best[0], best[2] or 'nincs'))
        o['regi_helyes'] = 'nem'
        out.append(o)
        continue

    # --- tabla-sor van, de nincs jelolt, nincs beagyazas
    if t:
        o.update(osztaly='bizonytalan', alosztaly='tabla_sor_jelolt_nelkul',
                 indok='a tabla sor (%s -> kjv %s) van, de nincs nem kulcsolt LXX-vers ezzel a kjv-vel, a sorrend-beagyazas sem dont (%s: %s); a regi szoveg legjobb egyezese: %s (Jaccard %.2f, kulcsa: %s)'
                       % (g, t[1], emb, emb_det, best[1], best[0], best[2] or 'nincs'))
        o['regi_helyes'] = 'ellentmondo' if best[2] else 'n/a'
        out.append(o)
        continue

    # --- nincs tabla-sor / jelolt: fuggetlen fejezetszintu eltolasteszt
    #     L-mod: az LXX-fejezet (= Karoli-fejezetszam) verse v+s
    #     K-mod: az az LXX-vers, amelynek igehely_kjv-je c:(v+t) (TVTMS-hivatkozas, bar melyik LXX-fejezetben)
    kjv_idx = kjv_index(slug)
    modok = []
    lcd = lxx_chapter(rows, c)
    for s in range(-4, 6):
        par = {}
        for vv in kc:
            if vv + s in lcd:
                par[vv] = lcd[vv + s][0]
        modok.append(('L%+d' % s, par))
    for tt in range(-3, 5):
        par = {}
        for vv in kc:
            lst = kjv_idx.get('%d:%d' % (c, vv + tt), [])
            if len(lst) == 1:
                par[vv] = lst[0]
        modok.append(('K%+d' % tt, par))
    ert = []
    for nev, par in modok:
        if len(par) < 5:
            continue
        xs = [kc[vv] for vv in par]
        ys = [len(rows[par[vv]]['forms']) for vv in par]
        rr = pear(xs, ys)
        if rr is not None:
            ert.append((rr, nev, par))
    ert.sort(key=lambda x: -x[0])
    if not ert:
        o.update(osztaly='bizonytalan', alosztaly='nincs_tabla_nincs_teszt', indok='nincs tabla-sor, a fejezetteszt nem ertelmezheto')
        out.append(o)
        continue
    r1, nev1, par1 = ert[0]
    r2 = -1
    for rr_, nev_, par_ in ert[1:]:
        if any(par_[x] != par1[x] for x in par_ if x in par1):
            r2 = rr_
            break
    jel = par1.get(v)
    if jel is None:
        for rr_, nev_, par_ in ert[1:]:
            if v in par_ and rr_ >= 0.7 and not any(par_[x] != par1[x] for x in par_ if x in par1):
                jel = par_[v]
                nev1 = nev1 + '+' + nev_
                break
    jel_ures = bool(jel) and not rows[jel]['kar']
    o['fej_r'] = '%.2f' % r1
    o['fej_offset'] = nev1
    regi_egyezik = bool(jel) and best[1] == jel and best[0] >= 0.5
    o['regi_helyes'] = 'igen' if regi_egyezik else 'nem'
    kjv_t = nev1.startswith('K')
    if r1 >= 0.7 and (r1 - r2) >= 0.15 and jel_ures:
        o.update(osztaly='A', alosztaly='A2_tabla_nelkul', javasolt_lxx=jel,
                 kulcs_forras='NINCS tabla-sor (Karoli_versmegfeleltetes.tsv-ben a fejezet hianyzik); %s; uj felulbiralasi sor kellene' % (
                     'LXX_OS igehely_kjv (TVTMS) hivatkozas szerinti parositas' if kjv_t else 'LXX-fejezeten beluli sorszam-eltolas'),
                 indok='fuggetlen fejezet-szoszamkorrelacio: legjobb parositas %s, r=%.2f (az ellentmondo parositasu 2. legjobb r=%.2f, n=%d); regi szoveg %s'
                       % (nev1, r1, r2, len(par1), 'egyezik' if regi_egyezik else 'mas versre mutat (%s)' % best[1]))
    else:
        o.update(osztaly='bizonytalan', alosztaly='nincs_tabla_gyenge_teszt', javasolt_lxx=(jel or ''),
                 kulcs_forras='-',
                 indok='nincs tabla-sor; a legjobb parositas %s r=%.2f (az ellentmondo parositasu 2.: %.2f, n=%d) nem eleri a kuszobot (r>=0,70, kulonbseg>=0,15, a jelolt letezik es nem kulcsolt: %s)'
                       % (nev1, r1, r2, len(par1), 'igen' if jel_ures else 'nem'))
    out.append(o)


# --- mar kulcsolt Karoli-vers nem kaphat masodik kulcsot
for o in out:
    if o['osztaly'] == 'A':
        of_ = lxx_order(L.elsodleges_slug(o['konyv']))[2]
        if o['igehely'] in of_:
            o['osztaly'] = 'bizonytalan'
            o['alosztaly'] = 'mar_kulcsolt_karoli_vers'
            o['indok'] += ' | a Karoli-vers mar kulcsolt (%s): kettos kulcs lenne' % ';'.join(of_[o['igehely']])

# --- kettos jeloltek: ket Karoli-vers ugyanarra az LXX-versre
cnt = collections.Counter(o['javasolt_lxx'] for o in out if o['osztaly'] == 'A' and o['javasolt_lxx'])
for o in out:
    if o['osztaly'] == 'A' and cnt[o['javasolt_lxx']] > 1:
        o['osztaly'] = 'bizonytalan'
        o['alosztaly'] = 'kettos_jelolt'
        o['indok'] += ' | tobb Karoli-vers is ugyanerre az LXX-versre mutat: %s' % o['javasolt_lxx']

cols = ['igehely', 'konyv', 'regi_n', 'karoli_szo', 'letezik_karoli', 'tabla_kjv', 'tabla_osztaly', 'cand_lxx', 'beagyazas',
        'regi_legjobb_lxx', 'regi_jaccard', 'regi_legjobb_kulcs', 'regi_helyes', 'fej_r', 'fej_offset',
        'osztaly', 'alosztaly', 'javasolt_lxx', 'kulcs_forras', 'indok']
with open(R + 'naplok/LXX_OS_LEFEDETTSEG_osztalyozas.tsv', 'w', encoding='utf-8', newline='\n') as f:
    f.write('# GENERÁLT: naplok/LXX_OS_LEFEDETTSEG_M0_general.py — kézzel nem szerkesztendő.\n')
    f.write('# proveniencia: scope=naplok/FORRASKIVEZETES_M5_eltereslista.tsv (kategoria=csak_regi_vers, 503 vers) | forras=manual (gépi összevetés: Karoli_versmegfeleltetes.tsv, LXX_OS, Karoli_1908.tsv, a törölt LXX_kivonat git %s; nem lekerdez.py-kimenet) | ts=%s\n' % (TORLES_ELOTT, TS))
    f.write('\t'.join(cols) + '\n')
    for o in out:
        f.write('\t'.join(str(o[c]).replace('\t', ' ') for c in cols) + '\n')

# --- osszesites
print('osszes', len(out))
tot = collections.Counter(o['osztaly'] for o in out)
print(dict(tot))
print(collections.Counter((o['osztaly'], o['alosztaly']) for o in out))
bk = collections.Counter((o['konyv'], o['osztaly']) for o in out)
for k in sorted(bk):
    print(k, bk[k])
