"""F43 LXX_BRIDGE: az adat/lxx_dontesek.tsv LD005-LD090 soranak osszevetese az
adat/kulso/lxx_bridge.tsv (heber->gorog Strong parok, CC BY 4.0) parjaival.

Kimenet: naplok/LXX_BRIDGE_egyezes.tsv (86 sor). A dontestablat NEM modositja.
Determinisztikus, halozatot nem hiv. TSV-olvasas split('\\t'), iras '\\t'.join()
(a csv modul tilos ezeken a tablakon).

Futtatas: python eszkozok/lxx_bridge_egyezes.py [--kimenet UT]
"""
import sys
import os
import re
import glob
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE = os.path.join(GYOKER, 'adat', 'kulso', 'lxx_bridge.tsv')
DONTESEK = os.path.join(GYOKER, 'adat', 'lxx_dontesek.tsv')
OS_MAPPA = os.path.join(GYOKER, 'konkordancia', 'LXX_OS')
SZOTAR = os.path.join(GYOKER, 'konkordancia', 'Strong_szotar.tsv')
GRAMM = os.path.join(GYOKER, 'adat', 'grammatikai_strongok.tsv')
KIMENET = os.path.join(GYOKER, 'naplok', 'LXX_BRIDGE_egyezes.tsv')

# A nyitott sorok jeloltjei: a megjegyzes szovegebol kezzel kiolvasva
# (lemma, LXX_OS-vers, ahol a lemma Strong-szama keresendo). A Strong-szamot
# a script a LXX_OS adott versenek tokenjeibol oldja fel (nem emlekezetbol).
NYITOTT_JELOLTEK = {
    'LD008': [('ᾅδης', 'Ecclesiastes 9:10')],
    'LD009': [('βάθος', 'Isaiah 7:11')],
    'LD058': [('Ραφα', '2 Samuel 21:22'), ('γίγας', '2 Samuel 21:22')],
    'LD064': [('γηγενής', 'Proverbs 2:18'), ('ᾅδης', 'Proverbs 2:18')],
}

FEJLEC = ['id', 'igehely', 'lxx_igehely', 'heber_strong', 'tipus', 'bizonyossag',
          'dontes_gorog_strong', 'dontes_gorog_lemma', 'bridge_jeloltek',
          'vers_strongok_forras', 'bridge_a_versben', 'bridge_lemma', 'kategoria',
          'megjegyzes', 'lefedettseg', 'vers_strong_hiany']

RE_STRONG = re.compile(r'^[HG]?0*(\d+)[a-z]?$')


def norm(s):
    """Strong-szam egesz szamma ('H1254', 'G4160', '4160', 'G0746' -> int); ures -> None."""
    s = (s or '').strip()
    if not s:
        return None
    m = RE_STRONG.match(s)
    if not m:
        return None
    return int(m.group(1))


def g(n):
    return 'G%04d' % n


def h(n):
    return 'H%04d' % n


def lemma_kulcs(s):
    """ekezet- es kisbetu-fuggetlen lemma-kulcs."""
    d = unicodedata.normalize('NFD', s or '')
    d = ''.join(c for c in d if not unicodedata.combining(c))
    return d.lower().replace('ς', 'σ')


def sorok(ut):
    """TSV sorai megjegyzes (#) es ures sor nelkul, tabbal vagva."""
    with open(ut, encoding='utf-8', newline='') as f:
        for sor in f:
            sor = sor.rstrip('\r\n')
            if not sor or sor.startswith('#'):
                continue
            yield sor.split('\t')


def bridge_betolt():
    it = sorok(BRIDGE)
    fejlec = next(it)
    parok = {}
    n = 0
    for r in it:
        hs, gs, c = norm(r[0]), norm(r[1]), int(r[2])
        parok.setdefault(hs, []).append((gs, c))
        n += 1
    for hs in parok:
        parok[hs].sort(key=lambda x: (-x[1], x[0]))
    return fejlec, parok, n


def os_betolt(kellenek):
    """LXX_OS: igehely_lxx -> [(pozicio, lemma, strong|None, strong_ok)]; csak a kert versek."""
    idx = {}
    for ut in sorted(glob.glob(os.path.join(OS_MAPPA, '*.tsv'))):
        nev = os.path.basename(ut)
        if nev in ('karoli_fejezet_dontes.tsv', 'karoli_vers_felulbiralas.tsv'):
            continue
        it = sorok(ut)
        fejlec = next(it)
        if fejlec[0] != 'igehely_lxx':
            continue
        i_poz, i_lemma = fejlec.index('pozicio'), fejlec.index('lemma')
        i_str, i_ok = fejlec.index('strong'), fejlec.index('strong_ok')
        for r in it:
            if r[0] in kellenek:
                idx.setdefault(r[0], []).append(
                    (int(r[i_poz]), r[i_lemma], norm(r[i_str]), r[i_ok]))
    return idx


def szotar_betolt():
    d = {}
    for r in sorok(SZOTAR):
        s = r[0]
        if s.startswith('G'):
            d[norm(s)] = r[1] if len(r) > 1 else ''
    return d


def gramm_betolt():
    return {norm(r[0]) for r in sorok(GRAMM) if r[0].startswith('G')}


def fmt_parok(lista):
    return ' '.join('%s:%d' % (g(s), c) for s, c in lista)


def fo():
    kimenet = KIMENET
    if '--kimenet' in sys.argv:
        kimenet = sys.argv[sys.argv.index('--kimenet') + 1]

    # --- 1. lepes: bridge
    b_fejlec, parok, b_sorok = bridge_betolt()
    egyedi_g = {s for lst in parok.values() for s, _ in lst}
    print('BRIDGE fejlec=%s' % '|'.join(b_fejlec))
    print('BRIDGE sorok=%d egyedi_heber=%d egyedi_gorog=%d' % (b_sorok, len(parok), len(egyedi_g)))

    # --- dontesek
    it = sorok(DONTESEK)
    d_fejlec = next(it)
    dontesek = []
    for r in it:
        rec = dict(zip(d_fejlec, r + [''] * (len(d_fejlec) - len(r))))
        if rec['id'] in ('LD001', 'LD002', 'LD003', 'LD004'):
            continue  # a #6 pilot sorai, nem az F08 86 sora
        dontesek.append(rec)
    print('DONTESEK sorok=%d (LD005-LD090)' % len(dontesek))

    kellenek = {d['lxx_igehely'] for d in dontesek}
    for lst in NYITOTT_JELOLTEK.values():
        for _, v in lst:
            kellenek.add(v)
    os_idx = os_betolt(kellenek)
    szotar = szotar_betolt()
    gramm = gramm_betolt()

    kimeno = []
    for d in dontesek:
        vers = d['lxx_igehely']
        hs = norm(d['heber_strong'])
        dg = norm(d['gorog_strong'])
        tipus, biz = d['tipus'], d['bizonyossag']
        tokenek = os_idx.get(vers)
        if tokenek:
            forras = 'LXX_OS'
            vers_g = {s for _, _, s, _ in tokenek if s is not None}
            hiany = sum(1 for _, _, s, _ in tokenek if s is None)
            lemma_g = {}
            for _, lm, s, _ in tokenek:
                if s is not None and s not in lemma_g:
                    lemma_g[s] = lm
        else:
            forras, vers_g, hiany, lemma_g = 'nincs', set(), '', {}
        # F42 / DT-F42f: a régi LXX_kivonat kivezetve; a lefedettség csak az LXX_OS-ből áll.
        lefed = 'csak_OS' if tokenek else 'egyik_sem'

        jeloltek = parok.get(hs, []) if hs is not None else []
        bridge_gs = {s for s, _ in jeloltek}
        verszben = [(s, c) for s, c in jeloltek if s in vers_g] if forras != 'nincs' else []
        lemmak = []
        for s, _ in verszben:
            lm = lemma_g.get(s) or szotar.get(s, '')
            lemmak.append('%s=%s' % (g(s), lm))
        non_funkcio = [s for s, _ in verszben if s not in gramm]
        megj = []
        kat = ''

        if tipus == 'nincs_heber_kulcsszo' or biz == 'nem_alkalmazhato':
            kat = 'nem_alkalmazhato'
        elif biz == 'nyitott':
            allapotok = []
            for lm, v in NYITOTT_JELOLTEK[d['id']]:
                tok = os_idx.get(v, [])
                kulcs = lemma_kulcs(lm)
                sz = {s for _, l, s, _ in tok if lemma_kulcs(l) == kulcs}
                sz_ok = {ok for _, l, s, ok in tok if lemma_kulcs(l) == kulcs}
                sz = {x for x in sz if x is not None}
                if not sz:
                    ok = next(iter(sz_ok), None)
                    allapotok.append('%s: nincs Strong a LXX_OS-ben (%s)' % (
                        lm, ok if ok else 'a lemma nem all a %s versben' % v))
                    continue
                for s in sorted(sz):
                    if hs is None or hs not in parok:
                        st = 'nincs_adat'
                    elif s in bridge_gs:
                        c = dict(jeloltek)[s]
                        st = 'egyezik (%s:%d)' % (g(s), c)
                    else:
                        st = 'elter'
                    allapotok.append('%s %s: %s; a sor versében (%s) %s' % (
                        lm, g(s), st, vers, 'all' if s in vers_g else 'nem all'))
            kat = 'nyitott_jelolt'
            megj.append('jelolt-bridge-statusz: ' + ' | '.join(allapotok))
        elif tipus == 'lxx_minusz':
            if hs is None or hs not in parok:
                kat = 'nincs_adat'
                megj.append('a heber Strong nincs a bridge-ben (>=3 szures)')
            elif forras == 'nincs':
                kat = 'nincs_adat'
                megj.append('a vers Strong-halmaza nem elerheto')
            elif verszben:
                kat = 'lxx_minusz_ellentmond'
                megj.append('a bridge versben allo jeloltje: ' + ' '.join(lemmak))
                if not non_funkcio:
                    megj.append('csak funkciószó a metszetben')
            else:
                kat = 'lxx_minusz_osszhang'
        else:  # eltero_forditas
            if hs is None or hs not in parok:
                kat = 'nincs_adat'
                megj.append('a heber Strong nincs a bridge-ben (>=3 szures)')
            elif dg is None:
                kat = 'nincs_adat'
                megj.append('a dontesnek nincs gorog Strong-ja')
            elif dg in bridge_gs:
                if forras == 'nincs':
                    kat = 'egyezik_lexema'
                elif dg in vers_g:
                    kat = 'egyezik'
                else:
                    kat = 'egyezik_lexema'
                    megj.append('a dontes Strong-ja a bridge-ben van, de a vers Strong-halmazaban nem all')
            elif verszben:
                kat = 'elter'
                megj.append('a dontes %s nincs a bridge-parok kozt (a >=3 szures miatt hianyozhat); '
                            'versben allo bridge-jelolt: %s' % (g(dg), ' '.join(lemmak)))
                if not non_funkcio:
                    megj.append('csak funkciószó a metszetben')
            else:
                kat = 'nincs_adat'
                megj.append('nincs versben allo bridge-jelolt')
                if dg not in bridge_gs:
                    megj.append('a dontes %s sincs a bridge-parok kozt' % g(dg))

        kimeno.append([
            d['id'], d['igehely'], vers, d['heber_strong'], tipus, biz,
            d['gorog_strong'], d['gorog_lemma'],
            fmt_parok(jeloltek), forras, fmt_parok(verszben), ' '.join(lemmak),
            kat, '; '.join(megj), lefed, str(hiany)])

    if len(kimeno) != 86:
        print('HIBA: nem 86 sor: %d' % len(kimeno))
        sys.exit(1)
    for r in kimeno:
        for x in r:
            if '\t' in x or '\n' in x:
                print('HIBA: tab/ujsor a mezoben: %s' % r[0])
                sys.exit(1)

    os.makedirs(os.path.dirname(kimenet) or '.', exist_ok=True)
    with open(kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/lxx_bridge_egyezes.py — kézzel nem szerkesztendő. '
                'forras=adat/kulso/lxx_bridge.tsv (CC BY 4.0) + adat/lxx_dontesek.tsv + konkordancia/LXX_OS\n')
        f.write('\t'.join(FEJLEC) + '\n')
        for r in kimeno:
            f.write('\t'.join(r) + '\n')

    # --- osszesites
    from collections import Counter
    print('KIMENET sorok=%d -> %s' % (len(kimeno), kimenet))
    print('LEFEDETTSEG ' + str(sorted(Counter(r[14] for r in kimeno).items())))
    print('VERS_FORRAS ' + str(sorted(Counter(r[9] for r in kimeno).items())))
    print('KATEGORIA ' + str(sorted(Counter(r[12] for r in kimeno).items())))
    ker = Counter((r[5] or 'ures', r[12]) for r in kimeno)
    for k in sorted(ker):
        print('BIZONYOSSAG_X_KATEGORIA %s %s %d' % (k[0], k[1], ker[k]))


if __name__ == '__main__':
    fo()
