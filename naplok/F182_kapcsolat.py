# -*- coding: utf-8 -*-
"""F182 HAMART-001, 1. fázis, F16 — a motívum kapcsolat-sorainak (adat/kapcsolatok.tsv) jelöltjei.

Két jelöltforrás, mindkettő a motívum mai beépített soraira (adat/elofordulasok.tsv, HAMART-001):
  (1) determinisztikus: a TSK és a Károli-KH minden beépített versre (`lekerdez.py tsk` / `karoli`,
      MUNKAMENET A5; a proveniencia-sorok `--naplo HAMART-001 --lepes A5` módon az adat/auditok.tsv-be,
      0 találatnál is); jelölt a pár, ha a célvers is a motívum beépített verse;
  (2) a motívum 1/a prózájának (kapcsolodas, funkcio; a próza szerzője, scope=manual) saját
      igehely-hivatkozásai, ha a hivatkozott vers a motívum beépített verse.
Minden jelölt mellé a mért lexikai bizonyíték: a két sor verseiben közösen álló lánc-szavak és
szópárok (TAHOT/TAGNT), split('\t').

Kimenet: naplok/F182_kapcsolat_jeloltek.tsv (a jelöltnapló; a döntés oszlopai a `donto` lépésben).
A kapcsolatok.tsv-be csak a `naplok/F182_kapcsolat_dontes.py` ír, döntéssel és indoklással
(CLAUDE.md 2. szabály: keresési találatból nincs közvetlen út).

Futtatás a repó gyökeréből: python naplok/F182_kapcsolat.py [--naplo]
(--naplo: a lekérdezések proveniencia-sorai az adat/auditok.tsv-be)"""
import io
import re
import sys
import contextlib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, 'eszkozok')
import lekerdez  # noqa: E402

ID = 'HAMART-001'
KI = 'naplok/F182_kapcsolat_jeloltek.tsv'
LANC_H = ['H0779', 'H0127', 'H6093', 'H2403', 'H2555', 'H7843', 'H6975', 'H1863']
LANC_G = ['G1944', 'G2671', 'G2672', 'G5351', 'G5356', 'G1311', 'G0173', 'G5146']
FORDULAT = {
    'föld színe (H6440+H0127)': ({'H6440', 'H0127'},),
    'málé+chámász': ({'H4390', 'H2555'}, {'H4393', 'H2555'}),
    'sámá+chámász': ({'H8085', 'H2555'},),
    'kóc+dardar': ({'H6975', 'H1863'},),
    'árar+adámá': ({'H0779', 'H0127'},),
    'ἄκανθα+τρίβολος': ({'G0173', 'G5146'},),
}
KONYV_RE = re.compile(r'(?<![\w:])((?:[1-5])?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,5}) (\d+):(\d+)(?:-(\d+))?')
CSUPASZ_RE = re.compile(r'(?<![\w:,])(\d+):(\d+)(?:-(\d+))?')


USZ = ('Mt', 'Mk', 'Róm', 'Gal', 'Zsid', 'Jel')
CSALAD = {
    'κατάρα-család (G1944/G2671/G2672)': {'G1944', 'G2671', 'G2672'},
    'φθείρω-család (G5351/G1311/G2704/G5356/G5349)': {'G5351', 'G1311', 'G2704', 'G5356', 'G5349'},
    'ἄκανθα/τρίβολος (G0173/G5146)': {'G0173', 'G5146'},
}
KONYVEK = ['1Móz', '2Móz', '3Móz', '4Móz', '5Móz', 'Zsolt', 'Ézs', 'Jer', 'Ez', 'Hós', 'Jóel', 'Ámós', 'Jón', 'Mik',
           'Hab', 'Sof', 'Mal', 'Mt', 'Mk', 'Róm', 'Gal', 'Zsid', 'Jel']


def kanoni(ige):
    m = re.match(r'^(.+?) (\d+):(\d+)', ige)
    return (KONYVEK.index(m.group(1)), int(m.group(2)), int(m.group(3)))


def tsv(ut):
    sorok = [l for l in open(ut, encoding='utf-8').read().split('\n') if l and not l.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, l.split('\t'))) for l in sorok[1:]]


def kibont(ige):
    m = re.match(r'^(.+?) (\d+):(\d+)(?:-(\d+))?$', ige)
    k, f, a, v = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    return ['%s %s:%d' % (k, f, i) for i in range(a, (int(v) if v else a) + 1)]


def strongok():
    vs = {}
    for ut in ('konkordancia/TAHOT_kivonat.tsv', 'konkordancia/TAGNT_kivonat.tsv'):
        for l in open(ut, encoding='utf-8').read().split('\n')[1:]:
            c = l.split('\t')
            if len(c) > 1:
                vs.setdefault(c[0], set()).add(c[1])
    return vs


def futtat(argv):
    p = lekerdez.build_parser()
    args = p.parse_args(argv)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        lekerdez.futtat_naplozva(args)
    return buf.getvalue()


def main():
    naploz = '--naplo' in sys.argv
    sorok = [r for r in tsv('adat/elofordulasok.tsv') if r['id'] == ID]
    vers2sor = {}
    for r in sorok:
        for v in kibont(r['igehely']):
            vers2sor[v] = r['igehely']
    vs = strongok()
    sor_strong = {r['igehely']: set().union(*[vs.get(v, set()) for v in kibont(r['igehely'])]) for r in sorok}
    sorrend = {r['igehely']: kanoni(r['igehely']) for r in sorok}

    jelolt = {}  # (a, b) rendezett -> {forras: [..]}

    def ad(a, b, forras):
        if a == b or a not in sorrend or b not in sorrend:
            return
        kulcs = tuple(sorted((a, b), key=lambda x: sorrend[x]))
        jelolt.setdefault(kulcs, []).append(forras)

    elo = ['--naplo', ID, '--lepes', 'A5'] if naploz else []
    n_tsk = n_kh = 0
    for v in sorted(vers2sor, key=lambda x: (sorrend[vers2sor[x]], x)):
        ki = futtat(elo + ['tsk', v])
        for l in ki.split('\n'):
            m = re.match(r'^(.+?) (\d+),(\d+)\tVotes=(\d+)$', l)
            if m:
                cel = '%s %s:%s' % (m.group(1), m.group(2), m.group(3))
                if cel in vers2sor:
                    n_tsk += 1
                    ad(vers2sor[v], vers2sor[cel], 'TSK %s→%s Votes=%s' % (v, cel, m.group(4)))
        ki = futtat(elo + ['karoli', v])
        bent = False
        for l in ki.split('\n'):
            if l.startswith('# Károli-KH'):
                bent = True
                continue
            if bent and not l.startswith('proveniencia') and not l.startswith('#') and l.strip():
                m = re.match(r'^(.+?) (\d+),(\d+)', l.strip())
                if m:
                    cel = '%s %s:%s' % (m.group(1), m.group(2), m.group(3))
                    if cel in vers2sor:
                        n_kh += 1
                        ad(vers2sor[v], vers2sor[cel], 'Károli-KH %s→%s' % (v, cel))
    # a próza saját hivatkozásai
    n_proza = 0
    for r in sorok:
        konyv = r['igehely'].rsplit(' ', 1)[0]
        szoveg = r['kapcsolodas'] + ' ¦ ' + r['funkcio']
        talalt = set()
        for m in KONYV_RE.finditer(szoveg):
            for v in kibont('%s %s:%s%s' % (m.group(1), m.group(2), m.group(3), '-' + m.group(4) if m.group(4) else '')):
                talalt.add(v)
        maradek = KONYV_RE.sub(' ', szoveg)
        for m in CSUPASZ_RE.finditer(maradek):
            for v in kibont('%s %s:%s%s' % (konyv, m.group(1), m.group(2), '-' + m.group(3) if m.group(3) else '')):
                talalt.add(v)
        for v in sorted(talalt):
            if v in vers2sor and vers2sor[v] != r['igehely']:
                n_proza += 1
                ad(r['igehely'], vers2sor[v], 'próza %s → %s' % (r['igehely'], v))

    # (3) az adat saját mutatója: a tematikus sor gerinc-eleme a láncvers nevét hordozza
    n_gerinc = 0
    for r in sorok:
        if r['gerinc_elem'].startswith('tematikus:'):
            cel = r['gerinc_elem'].split(':', 1)[1].strip()
            if cel in vers2sor and vers2sor[cel] != r['igehely']:
                n_gerinc += 1
                ad(r['igehely'], vers2sor[cel], 'gerinc_elem %s → %s' % (r['igehely'], r['gerinc_elem']))
    # LXX a nyelvközi párokhoz (az ÓSZ-sor a görög Ószövetségben)
    gram = {l.split('\t')[0] for l in open('adat/grammatikai_strongok.tsv', encoding='utf-8').read().split('\n')[1:]
            if l and not l.startswith('#')}
    lxx = {}
    for r in sorok:
        if r['igehely'].split(' ')[0] in USZ:
            continue
        g = set()
        for v in kibont(r['igehely']):
            for l in futtat(elo + ['lxx-hid', v]).split('\n'):
                c = l.split('\t')
                if len(c) == 3 and re.match(r'^G\d{4}$', c[0]):
                    g.add(c[0])
        lxx[r['igehely']] = g
    lanc_g_lxx = LANC_G + ['G2704', 'G1093']

    fej = ['forras_sor', 'cel_sor', 'jelolt_forras', 'kozos_lanc_strong', 'kozos_fordulat', 'lxx_hid',
           'kozos_tartalmi_strong', 'gorog_szocsalad']
    ki = ['# GENERÁLT: naplok/F182_kapcsolat.py | scope=adat/elofordulasok.tsv (HAMART-001, %d sor, %d vers) × '
          'TSK_kereszthivatkozasok.tsv + Karoli_KH_javitott.tsv (lekerdez.py tsk/karoli, MUNKAMENET A5) + a 1/a próza '
          'igehely-hivatkozásai (scope=manual) + a tematikus sorok gerinc_elem-je | bizonyíték: TAHOT_kivonat.tsv+'
          'TAGNT_kivonat.tsv, LXX (lekerdez.py lxx-hid), split(\'\\t\') | '
          'ts=%s' % (len(sorok), len(vers2sor), lekerdez.ts()),
          '\t'.join(fej)]
    for (a, b), forr in sorted(jelolt.items(), key=lambda kv: (sorrend[kv[0][0]], sorrend[kv[0][1]])):
        sa, sb = sor_strong[a], sor_strong[b]
        kozos = [s for s in LANC_H + LANC_G if s in sa and s in sb]
        ford = [n for n, alt in FORDULAT.items() if any(x <= sa for x in alt) and any(x <= sb for x in alt)]
        hid = ''
        if (a in lxx) != (b in lxx):
            osz, usz = (a, b) if a in lxx else (b, a)
            hid = ','.join(s for s in lanc_g_lxx if s in lxx[osz] and s in sor_strong[usz])
        tart = ','.join(sorted(s for s in (sa & sb) if s not in gram and not s.startswith('H9')))
        # görög szócsalád (a negatív kritérium szerint): az ÓSZ-oldalon a LXX, az ÚSZ-oldalon a TAGNT
        ga = lxx.get(a, sa) if a in lxx else sa
        gb = lxx.get(b, sb) if b in lxx else sb
        csal = ','.join(n for n, cs in CSALAD.items() if (ga & cs) and (gb & cs)) if (a not in lxx or b not in lxx) else ''
        ki.append('\t'.join([a, b, ' · '.join(forr), ','.join(kozos), ','.join(ford), hid, tart, csal]))
    open(KI, 'w', encoding='utf-8', newline='').write('\n'.join(ki) + '\n')
    print('TSK-találat a motívumon belül: %d, Károli-KH: %d, próza-hivatkozás: %d, gerinc-mutató: %d; '
          'jelölt pár: %d -> %s' % (n_tsk, n_kh, n_proza, n_gerinc, len(jelolt), KI))


if __name__ == '__main__':
    main()
