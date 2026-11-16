#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V — az emberi validáció kiértékelése (Károli 1908 – Strong szópárosítás).

Bemenet:
  * a két ellenőr exportja (`<ellenor>_valaszok.json`, az `ellenorzo.html` írja);
  * a minta: kozlemeny/data_paper/validacio/minta.tsv (a JSON `minta_hash`-ének egyeznie kell);
  * opcionálisan a harmadik döntés (`--dontes`): az előző futás `eltero_tetelek.tsv`-je
    kitöltött `dontes` oszloppal (helyes | hibas | bizonytalan);
  * opcionálisan a modell-ellenőr ítéletei:
      --modell-f172      a párokra a #172 vak Opus-ellenőr meglévő ítélete (f172/itelet_par.tsv,
                         a minta `f172_id` oszlopán át; a 300 pár mind a #172 mintájából való);
      --modell-valasz D  a pár nélküli szavakra az új vak futás válaszai (D/koteg_NNN.json, a
                         #172 formájában; a szó ítélete `helyes`, ha a modell üres listát jelölt);
      --modell TSV       általános alak: `tetel_id<TAB>modell_itelet` (helyes | hibas) soronként.
    A modell-ellenőr bemenetét a `--modell-bemenet D` írja (a pár nélküli 80 szó, a #172
    utasításával és versblokk-formájával); a futtatás nem ennek a szkriptnek a dolga.

Kimenet (`--kimenet`, alapértelmezés: kozlemeny/data_paper/validacio/eredmeny/):
  * kiertekeles.md     — emberi pontosság Wilson 95%-kal (párok; pár nélküli szavak: kimaradási
                          arány), ellenőrönként és a döntött mintán; Cohen-kappa a két ember között;
                          a modell és az ember egyezése;
  * eltero_tetelek.tsv — a két ember eltérő tételei a harmadik döntéshez (`dontes` oszlop üres).

Az ítélet jelentése mindkét típusnál: helyes-e a gép döntése (pár: a pár helyes; pár nélküli szó:
valóban nincs eredetije). A `bizonytalan` a pontosság nevezőjéből kimarad, külön számoljuk, és a
konzervatív alsó becslés hibásnak veszi.

Olvasás split('\\t'), írás '\\t'.join() (a csv modul tilos, CLAUDE.md).

Használat (a repó gyökeréből):
    python eszkozok/karoli_strong_validacio_kiertekel.py A_valaszok.json B_valaszok.json
    python eszkozok/karoli_strong_validacio_kiertekel.py A.json B.json --dontes eltero_tetelek.tsv --modell-f172
    python eszkozok/karoli_strong_validacio_kiertekel.py --modell-bemenet <könyvtár>
"""

import argparse
import json
import math
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
VALIDACIO = os.path.join(GYOKER, 'kozlemeny', 'data_paper', 'validacio')
MINTA = os.path.join(VALIDACIO, 'minta.tsv')
F172_ITELET = os.path.join(GYOKER, 'f172', 'itelet_par.tsv')
Z95 = 1.959963984540054
ITELETEK = ('helyes', 'hibas', 'bizonytalan')
ELTERO_FEJ = ['tetel_id', 'tipus', 'vers', 'hu_szo', 'er_szo', 'strong',
              'A_itelet', 'A_hibatipus', 'A_helyes_forras', 'A_megjegyzes',
              'B_itelet', 'B_hibatipus', 'B_helyes_forras', 'B_megjegyzes', 'dontes', 'dontes_indok']


# ---------------------------------------------------------------- beolvasás

def tabla(ut):
    fej, sorok = None, []
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if not sor or sor.startswith('#'):
                continue
            m = sor.split('\t')
            if fej is None:
                fej = m
            else:
                sorok.append(dict(zip(fej, m)))
    return fej, sorok


def minta_hash(sorok):
    """Az ellenorzo.html MINTA_HASH-e (32 bites FNV-1a az UTF-16 kódegységeken, hexában)."""
    s = ';'.join('%s|%s|%s|%s' % (r['tetel_id'], r['vers'], int(r['hu_sorszam']),
                                  int(r['er_sorszam']) if r['er_sorszam'] else 0) for r in sorok)
    h = 0x811c9dc5
    b = s.encode('utf-16-le')
    for i in range(0, len(b), 2):
        h ^= b[i] | (b[i + 1] << 8)
        h = (h * 0x01000193) & 0xffffffff
    return '%x' % h


def valaszok_olvas(ut, minta, hash_):
    with open(ut, encoding='utf-8') as f:
        d = json.load(f)
    if d.get('minta_hash') != hash_:
        raise SystemExit('%s: a minta_hash (%s) nem ezé a mintáé (%s)' % (ut, d.get('minta_hash'), hash_))
    ids = {r['tetel_id'] for r in minta}
    ki = {}
    for k, v in (d.get('valaszok') or {}).items():
        if k not in ids:
            raise SystemExit('%s: ismeretlen tétel: %s' % (ut, k))
        it = v.get('itelet', '')
        if it and it not in ITELETEK:
            raise SystemExit('%s: ismeretlen ítélet %r (%s)' % (ut, it, k))
        if it:
            ki[k] = v
    return d.get('ellenor') or os.path.basename(ut), ki


# ---------------------------------------------------------------- statisztika

def wilson(x, n, z=Z95):
    if n == 0:
        return (float('nan'), float('nan'), float('nan'))
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def kappa(parok, kategoriak):
    """Cohen-kappa a (a, b) címkepárokon; (kappa, megfigyelt egyezés, n)."""
    n = len(parok)
    if n == 0:
        return (float('nan'), float('nan'), 0)
    po = sum(a == b for a, b in parok) / n
    pe = sum((sum(a == k for a, _ in parok) / n) * (sum(b == k for _, b in parok) / n) for k in kategoriak)
    k = float('nan') if pe == 1 else (po - pe) / (1 - pe)
    return (k, po, n)


def szazalek(x):
    return '–' if x != x else '%.2f%%' % (100 * x)


def szam(x):
    return '–' if x != x else '%.3f' % x


# ---------------------------------------------------------------- kiértékelés

def pontossag_sor(cimke, itelet_lista):
    """itelet_lista: ['helyes'|'hibas'|'bizonytalan', ...] -> táblasor."""
    h = itelet_lista.count('helyes')
    b = itelet_lista.count('hibas')
    u = itelet_lista.count('bizonytalan')
    p, lo, hi = wilson(h, h + b)
    pk, _, _ = wilson(h, h + b + u)
    return '| %s | %d | %d | %d | %d | %s | %s–%s | %s |' % (
        cimke, h + b + u, h, b, u, szazalek(p), szazalek(lo), szazalek(hi), szazalek(pk))


def kimaradas_sor(cimke, itelet_lista):
    h = itelet_lista.count('helyes')
    b = itelet_lista.count('hibas')
    u = itelet_lista.count('bizonytalan')
    p, lo, hi = wilson(b, h + b)
    return '| %s | %d | %d | %d | %d | %s | %s–%s |' % (
        cimke, h + b + u, h, b, u, szazalek(p), szazalek(lo), szazalek(hi))


def dontott(minta, a, b, dontes):
    """A döntött minta: egyező ítéletnél a közös, eltérőnél a harmadik döntés (ha van)."""
    ki, hianyzo = {}, []
    for r in minta:
        t = r['tetel_id']
        if t not in a or t not in b:
            continue
        ia, ib = a[t]['itelet'], b[t]['itelet']
        if ia == ib:
            ki[t] = ia
        elif dontes.get(t):
            ki[t] = dontes[t]
        else:
            hianyzo.append(t)
    return ki, hianyzo


def modell_osszevet(minta, emberi, modell, tipus):
    """Modell vs. döntött emberi ítélet (a bizonytalan emberi ítélet kimarad)."""
    parok = []
    for r in minta:
        t = r['tetel_id']
        if r['tipus'] != tipus or t not in modell or emberi.get(t) not in ('helyes', 'hibas'):
            continue
        parok.append((modell[t], emberi[t]))
    k, po, n = kappa(parok, ('helyes', 'hibas'))
    m = {(x, y): sum(1 for p in parok if p == (x, y)) for x in ('helyes', 'hibas') for y in ('helyes', 'hibas')}
    return k, po, n, m


def modell_f172(minta):
    _, sorok = tabla(F172_ITELET)
    by = {r['minta_id']: r for r in sorok}
    ki = {}
    for r in minta:
        if r['tipus'] == 'par' and r['f172_id'] in by:
            ki[r['tetel_id']] = 'helyes' if by[r['f172_id']]['helyes'] == '1' else 'hibas'
    return ki


def modell_valasz(minta, konyvtar):
    """A pár nélküli szavak vak modell-ítélete a koteg_*.json válaszokból (a #172 formája)."""
    cel = {}
    for r in minta:
        if r['tipus'] == 'parnelkuli':
            cel[(r['vers'], int(r['hu_sorszam']))] = r['tetel_id']
    ki = {}
    for fn in sorted(os.listdir(konyvtar)):
        if not (fn.startswith('koteg_') and fn.endswith('.json')):
            continue
        with open(os.path.join(konyvtar, fn), encoding='utf-8') as f:
            d = json.load(f)
        for v in d.get('versek', []):
            for hu, er in v.get('jeloles', []):
                t = cel.get((v.get('vers'), hu))
                if t:
                    ki[t] = 'helyes' if not er else 'hibas'
    return ki


def modell_tsv(ut):
    _, sorok = tabla(ut)
    ki = {}
    for r in sorok:
        if r.get('modell_itelet') not in ('helyes', 'hibas'):
            raise SystemExit('%s: ismeretlen modell_itelet %r (%s)' % (ut, r.get('modell_itelet'), r.get('tetel_id')))
        ki[r['tetel_id']] = r['modell_itelet']
    return ki


def kiertekel(minta, nev_a, a, nev_b, b, dontes, modell):
    """A jelentés szövege és az eltérő tételek sorai."""
    tip = {r['tetel_id']: r['tipus'] for r in minta}
    csop = {r['tetel_id']: r['csoport'] for r in minta}
    sor = []
    sor.append('## 1. Kitöltöttség\n')
    for nev, v in ((nev_a, a), (nev_b, b)):
        sor.append('- %s: %d / %d tétel (pár %d, pár nélküli %d)' % (
            nev, len(v), len(minta), sum(tip[t] == 'par' for t in v), sum(tip[t] == 'parnelkuli' for t in v)))
    kozos = [r['tetel_id'] for r in minta if r['tetel_id'] in a and r['tetel_id'] in b]
    sor.append('- mindkettő: %d tétel\n' % len(kozos))

    dont, hianyzo = dontott(minta, a, b, dontes)
    fej_p = ('| | n | helyes | hibás | bizonytalan | pontosság | Wilson 95% | konzervatív (bizonytalan = hibás) |\n'
             '|---|---|---|---|---|---|---|---|')
    sor.append('## 2. Párok: emberi pontosság\n')
    sor.append(fej_p)
    for nev, v in ((nev_a, a), (nev_b, b)):
        sor.append(pontossag_sor(nev, [v[t]['itelet'] for t in v if tip[t] == 'par']))
    sor.append(pontossag_sor('**döntött minta**', [dont[t] for t in dont if tip[t] == 'par']))
    sor.append('')
    sor.append('Könyvcsoportonként (döntött minta; a minta arányos, a csoportbecslések kis n-en állnak):\n')
    sor.append(fej_p)
    for cs in sorted({csop[t] for t in dont}, key=_csoport_sorrend):
        sor.append(pontossag_sor(cs, [dont[t] for t in dont if tip[t] == 'par' and csop[t] == cs]))
    sor.append('')
    tsz = {r['tetel_id']: (r.get('tobbszavas') or '') for r in minta}
    sor.append('Többszavas megfelelés szerint (döntött minta; 1:n = a magyar szónak több eredetije van, n:1 = a '
               'forrásszónak több magyar párja, n:m = mindkettő):\n')
    sor.append(fej_p)
    for cimke, felt in (('egyszavas (1:1)', lambda x: x == ''), ('többszavas, összesen', lambda x: x != ''),
                        ('· 1:n', lambda x: x == '1:n'), ('· n:1', lambda x: x == 'n:1'), ('· n:m', lambda x: x == 'n:m')):
        sor.append(pontossag_sor(cimke, [dont[t] for t in dont if tip[t] == 'par' and felt(tsz.get(t, ''))]))
    sor.append('')
    sor.append('Hibatípusok (a hibás páron, ellenőrönként): ' + '; '.join(
        '%s: %s' % (nev, ', '.join('%s %d' % (k, n) for k, n in sorted(_szamlal(
            v[t].get('hibatipus') or '(nincs megadva)' for t in v if tip[t] == 'par' and v[t]['itelet'] == 'hibas').items())) or '–')
        for nev, v in ((nev_a, a), (nev_b, b))) + '\n')

    fej_k = ('| | n | nincs eredetije (helyes) | van eredetije (kimaradt) | bizonytalan | kimaradási arány | Wilson 95% |\n'
             '|---|---|---|---|---|---|---|')
    sor.append('## 3. Pár nélküli szavak: kimaradási arány\n')
    sor.append('A keret: a párosítatlan magyar szavak a szabály által eldöntött esetek nélkül (önálló névelő, segédige, '
               'alanyi és tárgyi névmás, korrelatív „azért … hogy”); az arány erre a keretre szól.\n')
    sor.append(fej_k)
    for nev, v in ((nev_a, a), (nev_b, b)):
        sor.append(kimaradas_sor(nev, [v[t]['itelet'] for t in v if tip[t] == 'parnelkuli']))
    sor.append(kimaradas_sor('**döntött minta**', [dont[t] for t in dont if tip[t] == 'parnelkuli']))
    sor.append('')

    sor.append('## 4. A két ember egyezése (Cohen-kappa)\n')
    sor.append('| tételek | n | megfigyelt egyezés | kappa (3 kategória) | kappa (helyes/hibás; bizonytalan nélkül) | PABAK (helyes/hibás) |')
    sor.append('|---|---|---|---|---|---|')
    for cimke, szuro in (('összes', None), ('párok', 'par'), ('pár nélküli szavak', 'parnelkuli')):
        ts = [t for t in kozos if szuro is None or tip[t] == szuro]
        p3 = [(a[t]['itelet'], b[t]['itelet']) for t in ts]
        k3, po3, n3 = kappa(p3, ITELETEK)
        p2 = [x for x in p3 if 'bizonytalan' not in x]
        k2, po2, n2 = kappa(p2, ('helyes', 'hibas'))
        sor.append('| %s | %d | %s | %s | %s (n=%d) | %s |' % (cimke, n3, szazalek(po3), szam(k3), szam(k2), n2,
                                                              szam(2 * po2 - 1 if n2 else float('nan'))))
    sor.append('')
    elt = [t for t in kozos if a[t]['itelet'] != b[t]['itelet']]
    sor.append('Eltérő tétel: %d; harmadik döntéssel lezárva: %d; döntésre vár: %d (`eltero_tetelek.tsv`).\n' % (
        len(elt), sum(1 for t in elt if dontes.get(t)), len(hianyzo)))

    sor.append('## 5. A modell-ellenőr és az ember egyezése\n')
    if not modell:
        sor.append('Nincs modell-ítélet megadva (`--modell-f172`, `--modell-valasz`, `--modell`).\n')
    else:
        sor.append('A döntött emberi ítélethez mérve; a bizonytalan emberi ítélet kimarad.\n')
        sor.append('| tételek | n | egyezés | kappa | modell helyes / ember helyes | modell helyes / ember hibás | modell hibás / ember helyes | modell hibás / ember hibás |')
        sor.append('|---|---|---|---|---|---|---|---|')
        for cimke, tp in (('párok', 'par'), ('pár nélküli szavak', 'parnelkuli')):
            k, po, n, m = modell_osszevet(minta, dont, modell, tp)
            sor.append('| %s | %d | %s | %s | %d | %d | %d | %d |' % (
                cimke, n, szazalek(po), szam(k), m[('helyes', 'helyes')], m[('helyes', 'hibas')],
                m[('hibas', 'helyes')], m[('hibas', 'hibas')]))
        sor.append('')

    minta_by = {r['tetel_id']: r for r in minta}
    eltero = []
    for t in sorted(elt):
        r = minta_by[t]
        eltero.append([t, r['tipus'], r['vers'], r['hu_szo'], r['er_szo'], r['strong'],
                       a[t]['itelet'], a[t].get('hibatipus', ''), ','.join(map(str, a[t].get('helyes_forras') or [])),
                       _egysor(a[t].get('megjegyzes', '')),
                       b[t]['itelet'], b[t].get('hibatipus', ''), ','.join(map(str, b[t].get('helyes_forras') or [])),
                       _egysor(b[t].get('megjegyzes', '')), dontes.get(t, ''), ''])
    return '\n'.join(sor), eltero


def _szamlal(it):
    d = {}
    for x in it:
        d[x] = d.get(x, 0) + 1
    return d


def _egysor(s):
    return ' '.join((s or '').replace('\t', ' ').split())


_SORREND = ['OSZ_mozes', 'OSZ_tortenet', 'OSZ_koltoi', 'OSZ_profeta', 'USZ_evangelium', 'USZ_level', 'USZ_jelenesek']


def _csoport_sorrend(cs):
    return _SORREND.index(cs) if cs in _SORREND else len(_SORREND)


def dontes_olvas(ut):
    _, sorok = tabla(ut)
    ki = {}
    for r in sorok:
        d = (r.get('dontes') or '').strip()
        if d and d not in ITELETEK:
            raise SystemExit('%s: ismeretlen döntés %r (%s)' % (ut, d, r.get('tetel_id')))
        if d:
            ki[r['tetel_id']] = d
    return ki


def git_head():
    try:
        return subprocess.check_output(['git', '-C', GYOKER, 'rev-parse', '--short', 'HEAD'], text=True).strip()
    except Exception:  # noqa: BLE001
        return 'ismeretlen'


# ---------------------------------------------------------------- modell-bemenet

def modell_bemenet(minta, konyvtar, koteg=25):
    """A pár nélküli szavak vak modell-ellenőrzésének bemenete, a #172 formájában
    (utasitas.md + koteg_NNN.txt; a CÉL a pár nélküli szó sorszáma)."""
    sys.path.insert(0, os.path.join(GYOKER, 'eszkozok', 'karoli_strong'))
    import bemenet  # noqa: E402
    import pontossag_ellenor as pe  # noqa: E402
    cel = {}
    for r in minta:
        if r['tipus'] == 'parnelkuli':
            cel.setdefault(r['vers'], set()).add(int(r['hu_sorszam']))
    versek = sorted(cel)
    os.makedirs(konyvtar, exist_ok=True)
    with open(os.path.join(konyvtar, 'utasitas.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(pe.FELADAT.replace('{SZABALYOK}', pe.utasitas()))
    n = 0
    for k in range(0, len(versek), koteg):
        n += 1
        blokk = [bemenet.versblokk(v, kjv=False) + '\nCÉL (Károli-sorszámok): ' + ', '.join(map(str, sorted(cel[v])))
                 for v in versek[k:k + koteg]]
        with open(os.path.join(konyvtar, 'koteg_%03d.txt' % n), 'w', encoding='utf-8', newline='\n') as f:
            f.write('KÖTEG: %d\n\n' % n + '\n\n'.join(blokk) + '\n')
    return len(versek), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('valaszok', nargs='*', help='a két ellenőr JSON-exportja')
    ap.add_argument('--minta', default=MINTA)
    ap.add_argument('--dontes')
    ap.add_argument('--modell-f172', action='store_true')
    ap.add_argument('--modell-valasz')
    ap.add_argument('--modell')
    ap.add_argument('--modell-bemenet')
    ap.add_argument('--kimenet', default=os.path.join(VALIDACIO, 'eredmeny'))
    a = ap.parse_args()

    _, minta = tabla(a.minta)
    if a.modell_bemenet:
        nv, nk = modell_bemenet(minta, a.modell_bemenet)
        print('modell-bemenet: %d vers, %d köteg -> %s' % (nv, nk, a.modell_bemenet))
        if not a.valaszok:
            return
    if len(a.valaszok) != 2:
        raise SystemExit('pontosan két válaszfájl kell')
    h = minta_hash(minta)
    nev_a, va = valaszok_olvas(a.valaszok[0], minta, h)
    nev_b, vb = valaszok_olvas(a.valaszok[1], minta, h)
    if nev_a == nev_b:
        raise SystemExit('a két válaszfájl ugyanattól az ellenőrtől való: %s' % nev_a)
    dontes = dontes_olvas(a.dontes) if a.dontes else {}
    modell = {}
    if a.modell_f172:
        modell.update(modell_f172(minta))
    if a.modell_valasz:
        modell.update(modell_valasz(minta, a.modell_valasz))
    if a.modell:
        modell.update(modell_tsv(a.modell))

    szoveg, eltero = kiertekel(minta, 'A (%s)' % nev_a, va, 'B (%s)' % nev_b, vb, dontes, modell)
    head = git_head()
    forras = [os.path.relpath(x, GYOKER).replace(os.sep, '/') if os.path.abspath(x).startswith(GYOKER) else os.path.basename(x)
              for x in [a.minta] + a.valaszok + ([a.dontes] if a.dontes else [])]
    prov = ('# MANUAL: scope=F175.V emberi validáció kiértékelése | forras=%s%s @ %s | ts=git:%s | manual '
            '(determinisztikus számítás: eszkozok/karoli_strong_validacio_kiertekel.py; az ítéletek emberi ellenőröké)'
            % (', '.join(forras), ', f172/itelet_par.tsv' if a.modell_f172 else '', head, head))
    os.makedirs(a.kimenet, exist_ok=True)
    with open(os.path.join(a.kimenet, 'kiertekeles.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('<!-- %s -->\n\n# Emberi validáció — kiértékelés\n\n' % prov[2:] + szoveg + '\n')
    with open(os.path.join(a.kimenet, 'eltero_tetelek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(prov + '\n')
        f.write('\t'.join(ELTERO_FEJ) + '\n')
        for s in eltero:
            f.write('\t'.join(s) + '\n')
    print(szoveg)
    print('\n-> %s' % os.path.join(a.kimenet, 'kiertekeles.md'))


if __name__ == '__main__':
    main()
