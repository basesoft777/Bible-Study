#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tanulmany_ellenorzes.py -- F37 T4: a `fuggetlen-ellenor` tanulmany-ellenorzo
listajanak determinisztikus resze. Csak olvas, fajlt nem ir (a --kimenet
kivetelevel, amelyet csak a T5 egyszeri audit hasznal).

  1. a 2. pont kulcsszo-tablazatanak Strong-szama elofordul-e a megadott
     versben (versoszlop nelkul: a tanulmany igeszakaszaban) a Strong-jelolt
     eredeti szovegben: heber -> konkordancia/TAHOT_kivonat.tsv, gorog ->
     konkordancia/TAGNT_kivonat.tsv (T0 6. pont);
  2. a tablazat szava es kiejtese a szotari reteg (konkordancia/TBESH.txt,
     TBESG.txt) soraval: lemma, atiras egymas mellett + egyszeru egyezes-jelzes
     (a vegso itelet az ugynoke: ragozott alak, osszetett kifejezes);
  3. a tanulmanyban teljes alakban (konyv fejezet:vers) hivatkozott igehelyek
     leteznek-e a Karoli 1908-ban (konkordancia/Karoli_1908.tsv);
  6. a motivumnaplo (motivumlog/PaRDeS_motivumok.md) het szakaszanak melyike
     emliti a tanulmany igeszakaszat.
  A 4. (Sod levezethetosege) es 5. (⚠️ nevesitett kepviselo) pont itelet;
  a szkript csak kigyujti a ⚠️ es ⭐ sorokat, hogy az ugynok ne keresse.

CLI:
    python eszkozok/ellenorzes/tanulmany_ellenorzes.py genezis/1Moz_12v1-20_bovitett.md
    python eszkozok/ellenorzes/tanulmany_ellenorzes.py --mind [--kimenet FAJL]

A kimenet utolso sora a lekerdezes proveniencia-sora (CLAUDE.md 1. szabaly).
Kilepesi kod: 0 (az eltérés is adat, nem futasi hiba), 2 = futasi hiba.
"""

import argparse
import datetime
import difflib
import os
import re
import subprocess
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos as K

KONK = 'konkordancia'
NAPLO = 'motivumlog/PaRDeS_motivumok.md'
NAPLO_SZAKASZOK = (
    'Tematikus áttekintés', 'Kulcsszó-index', 'Kulcsszavak részletesen',
    'Könyv szerinti index', '⭐ Emlékeztető küszöb', 'Még nem feldolgozott',
    'Feldolgozott igeszakaszok',
)


# ---------------------------------------------------------------- segédek

def _ut(*r):
    return os.path.join(K.ROOT, *r)


def _tsv(relut):
    """(fejlec, sorok) split('\\t')-tel, a '#' sorok nelkul (CLAUDE.md TSV-olvasas)."""
    fej, ki = None, []
    with open(_ut(*relut.split('/')), encoding='utf-8-sig') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if not s.strip() or s.startswith('#'):
                continue
            m = s.split('\t')
            if fej is None:
                fej = m
                continue
            ki.append(m)
    return fej, ki


def _ekezet_nelkul(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def _massalhangzok(s):
    """Heber/gorog szo pontozas, ekezet, kantillacio nelkul (osszevetesi kulcs)."""
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.replace('־', '').replace('׃', '')
    return re.sub(r'[\s,./()*\[\]\'"“”„|-]', '', s).lower().replace('ς', 'σ')


_KONYVEK = None


def konyvek():
    """{ekezet nelkuli rovidites: magyar rovidites} a normalizalo tablabol (+ Sir)."""
    global _KONYVEK
    if _KONYVEK is None:
        _fej, sorok = _tsv(KONK + '/Konyv_normalizalo_tabla.tsv')
        _KONYVEK = {}
        for m in sorok:
            if len(m) > 1 and m[1].strip():
                _KONYVEK[_ekezet_nelkul(m[1].strip())] = m[1].strip()
        _KONYVEK.setdefault('Sir', 'Sir')
    return _KONYVEK


def tanulmany_szakasz(relut):
    """(konyv, (fej1, vers1), (fej2, vers2|None)) a fajlnevbol: 1Moz_12v1-20,
    1Moz_10v1-11v32, 1Moz_14, Rom_8v10."""
    nev = os.path.basename(relut)
    m = re.match(r'^([1-3]?[A-Za-z]+)_(\d+)(?:v(\d+))?(?:-(\d+)(?:v(\d+))?)?_', nev)
    if not m:
        return None
    konyv = konyvek().get(m.group(1), m.group(1))
    f1 = int(m.group(2))
    v1 = int(m.group(3)) if m.group(3) else 1
    if m.group(4) is None:
        veg = (f1, int(m.group(3)) if m.group(3) else None)
    elif m.group(5) is None:
        veg = (f1, int(m.group(4))) if m.group(3) else (int(m.group(4)), None)
    else:
        veg = (int(m.group(4)), int(m.group(5)))
    return konyv, (f1, v1), veg


def _szakaszban(szak, fej, vers):
    _k, (f1, v1), (f2, v2) = szak
    if (fej, vers) < (f1, v1):
        return False
    if fej < f2:
        return True
    return fej == f2 and (v2 is None or vers <= v2)


# ---------------------------------------------------------------- adatforrás

class Forras(object):
    def __init__(self):
        self._vers_strong = None
        self._karoli = None
        self._szotar = {}

    def vers_strong(self):
        """{igehely: set(Strong)} a TAHOT es a TAGNT kivonatbol."""
        if self._vers_strong is None:
            d = {}
            for f in ('TAHOT_kivonat.tsv', 'TAGNT_kivonat.tsv'):
                fej, sorok = _tsv(KONK + '/' + f)
                ii, si = fej.index('Igehely'), fej.index('Strong-szám')
                for m in sorok:
                    if len(m) > si:
                        for s in m[si].split('+'):
                            if s.strip():
                                d.setdefault(m[ii], set()).add(s.strip())
            self._vers_strong = d
        return self._vers_strong

    def karoli(self):
        if self._karoli is None:
            _fej, sorok = _tsv(KONK + '/Karoli_1908.tsv')
            self._karoli = {m[0] for m in sorok if m}
        return self._karoli

    def szotar(self, strong):
        """[(kulcs, lemma, atiras, glossza)] a TBESH/TBESG-bol (H1254 -> H1254a, H1254b is)."""
        if strong in self._szotar:
            return self._szotar[strong]
        fajl = 'TBESH.txt' if strong.startswith('H') else 'TBESG.txt'
        ki = []
        minta = re.compile(r'^%s[a-z]?$' % re.escape(strong))
        with open(_ut(KONK, fajl), encoding='utf-8-sig') as f:
            for s in f:
                m = s.rstrip('\n').split('\t')
                if len(m) > 6 and minta.match(m[0]):
                    sor = (m[0], m[3], m[4], m[6])
                    if sor not in ki:
                        ki.append(sor)
        self._szotar[strong] = ki
        return ki


def strong_norm(s):
    m = re.match(r'^([GH])0*(\d{1,4})([a-zA-Z]?)$', s.strip())
    if not m:
        return None
    return '%s%04d' % (m.group(1), int(m.group(2)))


# ---------------------------------------------------------------- 2. pont táblázata

def kulcsszo_sorok(sorok):
    """[(sorszam, versek_szoveg|None, szo, kiejtes, [strong])] a ## 2. szakasz
    kulcsszo-tablazataibol (fejlec: van Strong- es szo-oszlop)."""
    ki = []
    a2 = False
    i = 0
    while i < len(sorok):
        s = sorok[i]
        if s.startswith('## '):
            a2 = bool(re.match(r'^##\s+2\.', s))
        if a2 and s.strip().startswith('|') and 'Strong' in s and re.search(r'[Ss]zó', s) \
                and 'Kulcsszó (Strong)' not in s:
            fej = [c.strip().lower() for c in s.strip().strip('|').split('|')]
            def idx(*kulcs):
                for j, c in enumerate(fej):
                    if any(k in c for k in kulcs):
                        return j
                return None
            iv, isz, ik, ist = idx('vers'), idx('szó'), idx('kiejtés'), idx('strong')
            j = i + 2
            while j < len(sorok) and sorok[j].strip().startswith('|'):
                c = [x.strip() for x in sorok[j].strip().strip('|').split('|')]
                def cel(k):
                    return c[k] if k is not None and k < len(c) else ''
                strongok = [strong_norm(x) for x in re.findall(r'[GH]\d{1,4}[a-zA-Z]?', cel(ist))]
                ki.append((j + 1, cel(iv) or None, cel(isz), cel(ik).strip('*_ '), [x for x in strongok if x]))
                j += 1
            i = j
            continue
        i += 1
    return ki


def versek(szak, vers_szoveg):
    """A vers-cella igehelyei (konyv fej:vers listaja); None -> az egesz szakasz."""
    konyv = szak[0]
    if not vers_szoveg:
        return None
    ki = []
    for m in re.finditer(r'(\d+):(\d+)(?:[-–](\d+))?', vers_szoveg):
        f, v1 = int(m.group(1)), int(m.group(2))
        v2 = int(m.group(3)) if m.group(3) else v1
        ki.extend('%s %d:%d' % (konyv, f, v) for v in range(v1, v2 + 1))
    # csupasz versszam ("17", "v.7", "14-15") egyfejezetes tanulmanyban: a fejezet a szakaszbol
    if not ki and szak[1][0] == szak[2][0]:
        for m in re.finditer(r'(?<![\d:])(\d+)(?:[-–](\d+))?(?![\d:])', vers_szoveg):
            v1 = int(m.group(1))
            v2 = int(m.group(2)) if m.group(2) else v1
            ki.extend('%s %d:%d' % (konyv, szak[1][0], v) for v in range(v1, v2 + 1))
    return ki or None


def _szakasz_versei(forras, szak):
    konyv = szak[0]
    ki = []
    for ig in forras.vers_strong():
        if not ig.startswith(konyv + ' '):
            continue
        m = re.match(r'^.+ (\d+):(\d+)$', ig)
        if m and _szakaszban(szak, int(m.group(1)), int(m.group(2))):
            ki.append(ig)
    return ki


def pont1_es_2(forras, relut, sorok, szak):
    p1, p2 = [], []
    for sorszam, vszov, szo, kiejt, strongok in kulcsszo_sorok(sorok):
        ighelyek = versek(szak, vszov) if szak else None
        hatokor = 'vers: ' + ', '.join(ighelyek) if ighelyek else 'a tanulmány szakasza'
        if ighelyek is None and szak:
            ighelyek = _szakasz_versei(forras, szak)
        for st in strongok or [None]:
            if st is None:
                p1.append((sorszam, szo, '—', hatokor, 'NEM ELLENŐRIZHETŐ', 'nincs értelmezhető Strong-szám'))
                continue
            if not ighelyek:
                p1.append((sorszam, szo, st, hatokor, 'NEM ELLENŐRIZHETŐ', 'a vers nem állapítható meg'))
                continue
            talalt = [ig for ig in ighelyek if st in forras.vers_strong().get(ig, ())]
            if talalt:
                p1.append((sorszam, szo, st, hatokor, 'OK', ', '.join(talalt[:3])))
            else:
                p1.append((sorszam, szo, st, hatokor, 'ELTÉRÉS', 'a Strong-szám nincs a vers(ek)ben'))
        # 2. pont: szótári alak, kiejtés
        if len(strongok) != 1:
            p2.append((sorszam, szo, '+'.join(strongok) or '—', '—', '—', kiejt, 'KÉZI',
                       'összetett kifejezés vagy nincs Strong' if strongok else 'nincs Strong'))
            continue
        st = strongok[0]
        szt = forras.szotar(st)
        if not szt:
            p2.append((sorszam, szo, st, '—', '—', kiejt, 'ELTÉRÉS', 'nincs szótári sor'))
            continue
        lemma, atiras = szt[0][1], szt[0][2]
        alak_egyezik = any(_massalhangzok(l) == _massalhangzok(szo)
                           for x in szt for l in x[1].split(','))
        k1 = re.sub(r'[^a-z]', '', _ekezet_nelkul(kiejt.lower()))
        k2 = re.sub(r'[^a-z]', '', _ekezet_nelkul(atiras.lower()))
        hasonlo = difflib.SequenceMatcher(None, k1, k2).ratio() if k1 and k2 else 0.0
        if alak_egyezik and hasonlo >= 0.5:
            itelet, ok = 'OK', 'szótári alak egyezik, kiejtés hasonló (%.2f)' % hasonlo
        elif alak_egyezik:
            itelet, ok = 'KÉZI', 'szótári alak egyezik, kiejtés eltér (%.2f)' % hasonlo
        else:
            itelet, ok = 'KÉZI', 'nem szótári alak (ragozott?), kiejtés-hasonlóság %.2f' % hasonlo
        p2.append((sorszam, szo, st, lemma, atiras, kiejt, itelet, ok))
    return p1, p2


# ---------------------------------------------------------------- 3. pont

def pont3(forras, sorok):
    nevek = sorted(set(konyvek().values()), key=len, reverse=True)
    minta = re.compile(r'(?<![\wÁ-ű])(%s) (\d+):(\d+)(?:[-–](\d+))?' % '|'.join(re.escape(n) for n in nevek))
    hiba, db = [], 0
    for i, s in enumerate(sorok, 1):
        for m in minta.finditer(s):
            db += 1
            konyv, f = m.group(1), int(m.group(2))
            for v in {int(m.group(3)), int(m.group(4) or m.group(3))}:
                # a Karoli 1908 a Siralmakat `Sir`-kent kulcsolja (T0 6. pont)
                ig = '%s %d:%d' % ('Sir' if konyv == 'JSir' else konyv, f, v)
                if ig not in forras.karoli():
                    hiba.append((i, ig, m.group(0)))
    return db, hiba


# ---------------------------------------------------------------- 6. pont

def pont6(relut, szak):
    try:
        sorok = K.md_olvasas(_ut(*NAPLO.split('/')))
    except (IOError, OSError):
        return None
    tores = os.path.basename(relut)[:-3]
    keresett = [tores]
    if szak:
        konyv, (f1, v1), (f2, v2) = szak
        # a naplo a hosszabb alakot is hasznalja: "1Mózes 12:1-20", "Róma 8:10"
        for alak in (konyv, konyv + 'es', konyv + 'a'):
            keresett.append('%s %d:%d' % (alak, f1, v1))
            if v1 == 1 and v2 is None:
                keresett.append('%s %d' % (alak, f1))
    ki = []
    for nev in NAPLO_SZAKASZOK:
        eleje = next((i for i, s in enumerate(sorok) if s.startswith('## ') and nev in s), None)
        if eleje is None:
            ki.append((nev, 'NINCS SZAKASZ', ''))
            continue
        vege = next((j for j in range(eleje + 1, len(sorok)) if sorok[j].startswith('## ')), len(sorok))
        szoveg = '\n'.join(sorok[eleje:vege])
        talalt = [k for k in keresett if k in szoveg]
        if szak and not talalt:
            # barmely, a szakaszba eso versre mutato hivatkozas ("1Móz 2:7", "1Mózes 2:7")
            konyv = szak[0]
            for m in re.finditer(r'(?<![\wÁ-ű])%s(?:es|a)? (\d+):(\d+)' % re.escape(konyv), szoveg):
                if _szakaszban(szak, int(m.group(1)), int(m.group(2))):
                    talalt.append(m.group(0))
                    break
        ki.append((nev, 'említi' if talalt else 'nem említi', ', '.join(talalt)))
    return ki


# ---------------------------------------------------------------- 4–5. pont kigyűjtés

def jel_sorok(sorok, jel):
    return [(i, s.strip()) for i, s in enumerate(sorok, 1) if jel in s]


# ---------------------------------------------------------------- jelentés

def _c(s, n=90):
    s = (s or '').replace('|', '\\|').replace('`', "'")
    return s if len(s) <= n else s[:n - 1] + '…'


def ellenoriz(forras, relut):
    sorok = K.md_olvasas(_ut(*relut.split('/')))
    szak = tanulmany_szakasz(relut)
    p1, p2 = pont1_es_2(forras, relut, sorok, szak)
    db3, hiba3 = pont3(forras, sorok)
    p6 = pont6(relut, szak)
    return {'relut': relut, 'szak': szak, 'p1': p1, 'p2': p2, 'db3': db3, 'hiba3': hiba3,
            'p6': p6, 'figy': jel_sorok(sorok, '⚠️'), 'csillag': jel_sorok(sorok, '⭐')}


def jelentes_md(e, reszletes=True):
    s = []
    s.append('### `%s`' % e['relut'])
    s.append('')
    if e['szak']:
        k, (f1, v1), (f2, v2) = e['szak']
        s.append('Igeszakasz (fájlnévből): %s %d:%d – %d:%s' % (k, f1, v1, f2, v2 if v2 else 'vége'))
        s.append('')
    def szamol(lista, idx):
        c = {}
        for x in lista:
            c[x[idx]] = c.get(x[idx], 0) + 1
        return ', '.join('%s %d' % kv for kv in sorted(c.items())) or '—'
    s.append('- **1. Strong a versben:** %s' % szamol(e['p1'], 4))
    s.append('- **2. szótári alak / kiejtés:** %s' % szamol(e['p2'], 6))
    s.append('- **3. igehelyek:** %d teljes alakú hivatkozás, nem létező: %d' % (e['db3'], len(e['hiba3'])))
    if e['p6'] is not None:
        s.append('- **6. motívumnapló:** ' + '; '.join('%s: %s' % (n, a) for n, a, _t in e['p6']))
    s.append('- **4–5. kigyűjtve:** ⚠️ %d sor, ⭐ %d sor' % (len(e['figy']), len(e['csillag'])))
    if not reszletes:
        return '\n'.join(s)
    elteres1 = [x for x in e['p1'] if x[4] != 'OK']
    if elteres1:
        s.append('')
        s.append('| sor | szó | Strong | hatókör | 1. pont | indok |')
        s.append('|---|---|---|---|---|---|')
        for x in elteres1:
            s.append('| %d | %s | %s | %s | %s | %s |' % (x[0], _c(x[1], 30), x[2], _c(x[3], 40), x[4], _c(x[5])))
    nem_ok2 = [x for x in e['p2'] if x[6] != 'OK']
    if nem_ok2:
        s.append('')
        s.append('| sor | szó (tanulmány) | Strong | lemma (TBESH/G) | átírás (TBESH/G) | kiejtés (tanulmány) | 2. pont | megjegyzés |')
        s.append('|---|---|---|---|---|---|---|---|')
        for x in nem_ok2:
            s.append('| %d | %s | %s | %s | %s | %s | %s | %s |' % (
                x[0], _c(x[1], 30), x[2], _c(x[3], 20), _c(x[4], 20), _c(x[5], 25), x[6], _c(x[7], 60)))
    if e['hiba3']:
        s.append('')
        s.append('Nincs a Károli 1908 számozásában (nem létező igehely vagy verzifikációs eltérés, '
                 'l. `konkordancia/Karoli_versmegfeleltetes.tsv`): '
                 + '; '.join('%d. sor `%s`' % (i, ig) for i, ig, _m in e['hiba3']))
    return '\n'.join(s)


def proveniencia(n):
    return ('proveniencia: scope=%d tanulmány | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv+TBESH.txt+'
            'TBESG.txt+Karoli_1908.tsv+motivumlog/PaRDeS_motivumok.md | ts=%s'
            % (n, datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')))


def mind():
    try:
        ki = subprocess.check_output(['git', 'ls-files', '*.md'], cwd=K.ROOT,
                                     stderr=subprocess.DEVNULL).decode('utf-8').splitlines()
    except (subprocess.CalledProcessError, OSError):
        ki = K.md_fajlok()
    return sorted(f for f in ki if not f.startswith('.') and K.tanulmany_fajl_e(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tanulmany', nargs='*')
    ap.add_argument('--mind', action='store_true', help='minden verziozott tanulmanyfajl')
    ap.add_argument('--kimenet', default=None)
    args = ap.parse_args()
    fajlok = mind() if args.mind else [os.path.relpath(os.path.abspath(f), K.ROOT).replace(os.sep, '/')
                                       for f in args.tanulmany]
    if not fajlok:
        print('Hiba: tanulmanyfajl vagy --mind kell.', file=sys.stderr)
        return 2
    forras = Forras()
    reszek = [jelentes_md(ellenoriz(forras, f)) for f in fajlok]
    szoveg = '\n\n'.join(reszek) + '\n\n' + proveniencia(len(fajlok)) + '\n'
    if args.kimenet:
        with open(_ut(*args.kimenet.split('/')), 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('irva: %s' % args.kimenet)
    else:
        print(szoveg)
    return 0


if __name__ == '__main__':
    sys.exit(main())
