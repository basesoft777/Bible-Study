#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
elojavit.py -- F188 T3: előzetes formai javító, a commit ELŐTT fut (a végrehajtó lépése,
F188_TEHER_CSOKKENTES_BRIEF.md T3). Három CI-szabály gépies esetét javítja, a többit
csak jelzi. A felismerés a CI saját kódja (`szabalyok.py`, import, nem másolat), ezért
ami itt tiszta, az a CI-ban is az.

- **E32** (kiosztott vagy kiosztásra váró helyőrző egy `eszkozok/**/*.py`
  string-literálban): a helyőrzőt számfüggetlen szövegre cseréli, ha az a literálban
  egy zárójeles hivatkozás eleme: `" (DT-F12a)"` -> `""`, `"(DT-F12a, N-F3b)"` ->
  `"(N-F3b)"`. Más helyzetben (a helyőrző a mondat része, vagy a sorban többször áll)
  csak jelez: a számfüggetlen megfogalmazás ott szövegezési döntés.
- **E5** (törölt `##`/`###` címsor vagy egy study-/sablonfájlból 30-nál több törölt sor
  `TÖRLÉS-SZÁNDÉKOS:` jelölés nélkül): a jelölés a commit-üzenetbe kerül, és a
  szándékot csak a végrehajtó tudja. Ezért alapból csak jelez, és kiírja a kész
  jelölősort; a `--e5-jelol --ir --commit-uzenet-fajl F` hármas fűzi az F
  üzenetfájlba (a `Co-Authored-By` sor elé).
- **E8** (tiltott igehely-formátum): a STEPBible-alak (`Gen.12.7`) a tanulmányfájlban
  adatformátum-idézet, ezért kódformázást kap (`` `Gen.12.7` ``); egy adatforrást
  megnevező sorban (`.tsv`, `adat/`, `konkordancia/`, `scope=`) az idézőjeles
  (`„…”`, `"…"`) igehely-idézet szintén. Más esetben (próza: `1 Móz 3:16`) csak jelez,
  a javasolt alakkal (`1Móz 3:16`).

Tájékoztató jelzés (F188 T2, nem gátol, a kilépési kódba nem számít): a nyitott tételben, a README-ben és a
jelentésben a hozzáadott sor, amely egy `.tsv` tábla darabszámát ismétli proveniencia-sor nélkül
(`szabalyok.szamismetles`; a CI-szabállyá emelése a #104 merge-e után, N-F188a).

Hatókör: a megadott fájlok, ennek hiányában a diff által érintettek (a munkafa a
`git merge-base <alap> HEAD`-hez képest, a nem követett új fájlokkal együtt).
Alapból száraz futás: kiírja a diffet, nem ír. `--ir`: a javítást a fájlba írja.

Kilépési kód: 0 = nincs teendő; 1 = van javítandó (száraz futás) vagy jelzés maradt;
2 = futási hiba.

CLI:
    python eszkozok/ellenorzes/elojavit.py                      # diff-érintett fájlok, száraz futás
    python eszkozok/ellenorzes/elojavit.py --ir
    python eszkozok/ellenorzes/elojavit.py a.md eszkozok/x.py --ir
    python eszkozok/ellenorzes/elojavit.py --e5-jelol --ir --commit-uzenet-fajl uzenet.txt
"""

import argparse
import ast
import difflib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos as K  # noqa: E402
import szabalyok as SZ  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

_HELYORZO_RESZLETBEN = re.compile(r'`((?:DT|N|D)-F\d+[a-z]*)`')
E8_ADATFORRAS = re.compile(r'\.tsv\b|\badat/|\bkonkordancia/|\bscope\s*=')
_E8_IDEZET = re.compile(r'„[^”\n]*”|"[^"\n]*"')
_E8_STEP = SZ.TANULMANY_TILTOTT_IGEHELY_MINTAK[1]
# javasolt alak a prózai esethez (csak jelzésben; nem írja)
_E8_JAVASLAT = (
    (re.compile(r'\b(\d)\.?\s+Móz\b'), r'\1Móz'),
    (re.compile(r'\b(\d)\.\s*(Sám|Kir|Krón|Kor|Thessz|Tim|Pét|Jn)\b'), r'\1\2'),
    (re.compile(r'\bApCsel\.\s'), 'ApCsel '),
    (re.compile(r'\b([1-5])\.?\s?Mózes\s+(\d+[:,.]\d)'), r'\1Móz \2'),
)


class Lelet(object):
    """Egy javítás vagy jelzés: (szabály, fájl, sor, szöveg, javított-e)."""

    __slots__ = ('szabaly', 'fajl', 'sor', 'szoveg', 'javitott')

    def __init__(self, szabaly, fajl, sor, szoveg, javitott):
        self.szabaly, self.fajl, self.sor, self.szoveg, self.javitott = szabaly, fajl, sor, szoveg, javitott

    def __repr__(self):
        return '%s %s:%s %s %r' % (self.szabaly, self.fajl, self.sor, 'JAVÍT' if self.javitott else 'JELEZ',
                                   self.szoveg)


# --------------------------------------------------------------------------
# fájlkezelés (a sorvég megmarad)
# --------------------------------------------------------------------------

def _olvas_sorok(relut):
    with open(os.path.join(K.ROOT, *relut.split('/')), encoding='utf-8', newline='') as f:
        return f.read().splitlines(True)


def _sor_torzs(sor):
    """(törzs, sorvég)."""
    for veg in ('\r\n', '\n', '\r'):
        if sor.endswith(veg):
            return sor[:-len(veg)], veg
    return sor, ''


def _ir_sorok(relut, sorok):
    with open(os.path.join(K.ROOT, *relut.split('/')), 'w', encoding='utf-8', newline='') as f:
        f.write(''.join(sorok))


def _git(args):
    try:
        return subprocess.check_output(['git'] + args, cwd=K.ROOT, stderr=subprocess.DEVNULL).decode(
            'utf-8', errors='replace')
    except (subprocess.CalledProcessError, OSError):
        return None


def merge_base(alap):
    ki = _git(['merge-base', alap, 'HEAD'])
    return ki.strip() if ki else None


def erintett_fajlok(alap):
    """A munkafa változott és új (nem követett) fájljai a merge-base-hez képest, repó-relatív, létezők."""
    mb = merge_base(alap)
    if mb is None:
        return None
    lista = (_git(['diff', '--name-only', mb]) or '').splitlines()
    lista += (_git(['ls-files', '--others', '--exclude-standard']) or '').splitlines()
    ki = []
    for f in lista:
        f = f.strip().replace('\\', '/')
        if f and f not in ki and os.path.isfile(os.path.join(K.ROOT, *f.split('/'))):
            ki.append(f)
    return ki


# --------------------------------------------------------------------------
# E32
# --------------------------------------------------------------------------

def e32_sor_javitas(sor, helyorzo):
    """A sor számfüggetlen alakja, ha a helyőrző egyszer áll benne, egy zárójeles hivatkozás elemeként; különben
    None."""
    h = re.escape(helyorzo)
    if len(re.findall(r'(?<![A-Za-z0-9-])' + h + r'(?![A-Za-z0-9-])', sor)) != 1:
        return None
    for minta, csere in (
        (r' ?\(\s*' + h + r'\s*\)', ''),              # " (DT-F12a)"  -> ""
        (r'\(\s*' + h + r'\s*[,;]\s*', '('),           # "(DT-F12a, X)" -> "(X)"
        (r'\s*[,;]\s*' + h + r'(?=\s*\))', ''),        # "(X, DT-F12a)" -> "(X)"
    ):
        uj, n = re.subn(minta, csere, sor, count=1)
        if n:
            return uj
    return None


def e32_javitasok(fajlok, ir):
    leletek = []
    talalatok = SZ.e32_kiosztott_helyorzo_literalban(fajlok)
    fajlonkent = {}
    for t in talalatok:
        fajlonkent.setdefault(t.fajl, []).append(t)
    for relut, ts in sorted(fajlonkent.items()):
        sorok = _olvas_sorok(relut)
        eredeti = list(sorok)
        for t in sorted(ts, key=lambda x: x.sor):
            m = _HELYORZO_RESZLETBEN.search(t.reszlet)
            idx = t.sor - 1
            uj = None
            if m and 0 <= idx < len(sorok):
                torzs, veg = _sor_torzs(sorok[idx])
                uj_torzs = e32_sor_javitas(torzs, m.group(1))
                if uj_torzs is not None:
                    uj = uj_torzs + veg
            if uj is None:
                leletek.append(Lelet('E32', relut, t.sor, t.reszlet, False))
                continue
            sorok[idx] = uj
            leletek.append(Lelet('E32', relut, t.sor, '`%s` törölve a zárójeles hivatkozásból' % m.group(1), True))
        if sorok == eredeti:
            continue
        try:
            ast.parse(''.join(sorok))
        except SyntaxError as e:
            for le in leletek:
                if le.fajl == relut and le.javitott:
                    le.javitott = False
                    le.szoveg += ' (a javítás után a fájl nem értelmezhető: %s; nem írtam)' % e
            continue
        _kiir_diff(relut, eredeti, sorok)
        if ir:
            _ir_sorok(relut, sorok)
    return leletek


# --------------------------------------------------------------------------
# E8
# --------------------------------------------------------------------------

def _kodon_kivul(sor):
    """[(kezd, veg)] a sor backtickes inline kódon kívüli szakaszai."""
    szakaszok, poz = [], 0
    for m in re.finditer(r'`[^`]*`', sor):
        szakaszok.append((poz, m.start()))
        poz = m.end()
    szakaszok.append((poz, len(sor)))
    return szakaszok


def _becsomagol(sor, kezd, veg):
    return sor[:kezd] + '`' + sor[kezd:veg] + '`' + sor[veg:]


def e8_sor_javitas(sor, tanulmany):
    """(új_sor, maradék_jelzések). A STEPBible-alakot (tanulmányfájlban), és adatforrást megnevező sorban az
    idézőjeles igehely-idézetet kódformázza; a többi tiltott alakra jelzést ad a javasolt alakkal."""
    mintak = SZ.TILTOTT_IGEHELY_MINTAK + (SZ.TANULMANY_TILTOTT_IGEHELY_MINTAK if tanulmany else [])
    adatsor = bool(E8_ADATFORRAS.search(sor))
    for _ in range(50):  # minden kör legfeljebb egy cserét tesz; a sor véges
        csere = None
        for kezd, veg in _kodon_kivul(sor):
            resz = sor[kezd:veg]
            if tanulmany:
                m = _E8_STEP.search(resz)
                if m:
                    csere = (kezd + m.start(), kezd + m.end())
                    break
            if adatsor:
                for idez in _E8_IDEZET.finditer(resz):
                    if any(mt.search(idez.group(0)) for mt in mintak):
                        csere = (kezd + idez.start(), kezd + idez.end())
                        break
                if csere:
                    break
        if not csere:
            break
        sor = _becsomagol(sor, *csere)
    jelzesek = []
    tisztitott = re.sub(r'`[^`]*`', '', sor)
    for minta in mintak:
        for m in minta.finditer(tisztitott):
            javaslat = m.group(0)
            for jm, jcs in _E8_JAVASLAT:
                javaslat = jm.sub(jcs, javaslat)
            jelzesek.append('tiltott igehely-formátum: "%s"%s' % (
                m.group(0), (' -> javasolt: "%s"' % javaslat) if javaslat != m.group(0) else ''))
    return sor, jelzesek


def e8_javitasok(fajlok, ir):
    leletek = []
    md = [f for f in fajlok if f.endswith('.md') and not K.kizart_e(f)]
    talalatok = SZ.e8_igehely_format(md)
    sorszamok = {}
    for t in talalatok:
        sorszamok.setdefault(t.fajl, set()).add(t.sor)
    for relut in sorted(sorszamok):
        sorok = _olvas_sorok(relut)
        eredeti = list(sorok)
        tanulmany = K.tanulmany_fajl_e(relut)
        for n in sorted(sorszamok[relut]):
            torzs, veg = _sor_torzs(sorok[n - 1])
            uj, jelzesek = e8_sor_javitas(torzs, tanulmany)
            if uj != torzs:
                sorok[n - 1] = uj + veg
                leletek.append(Lelet('E8', relut, n, 'adatidézet kódformázva', True))
            for j in jelzesek:
                leletek.append(Lelet('E8', relut, n, j, False))
        if sorok != eredeti:
            _kiir_diff(relut, eredeti, sorok)
            if ir:
                _ir_sorok(relut, sorok)
    return leletek


# --------------------------------------------------------------------------
# E5
# --------------------------------------------------------------------------

def e5_torlesek(diff_szoveg, study_halmaz):
    """[(fájl, leírás)] a `git diff --unified=0` szövegéből: a megfeleltetés nélkül törölt címsorok, illetve a
    study-/sablonfájlból törölt 30-nál több sor (ugyanaz a szabály, mint a CI E5-je: `SZ.CIMSOR_MINTA`,
    `SZ._tenylegesen_torolt_cimsorok`, `SZ._study_vagy_sablon_fajl`)."""
    ki = []
    allapot = {'fajl': None, 'torolt': 0, 'tc': [], 'hc': []}

    def lezar():
        f = allapot['fajl']
        if f is None:
            return
        torolt = SZ._tenylegesen_torolt_cimsorok(allapot['tc'], allapot['hc'])
        if torolt:
            for c in torolt:
                ki.append((f, 'törölt címsor: %s' % c))
        elif allapot['torolt'] > 30 and SZ._study_vagy_sablon_fajl(f, study_halmaz):
            ki.append((f, '%d törölt sor (study-/sablonfájl)' % allapot['torolt']))

    for sor in diff_szoveg.splitlines():
        if sor.startswith('+++ ') or sor.startswith('--- '):
            continue
        if sor.startswith('diff --git'):
            lezar()
            m = re.search(r' b/(\S+)$', sor)
            f = m.group(1) if m else None
            allapot.update(fajl=None if (f is None or f.startswith('beerkezo/')) else f, torolt=0, tc=[], hc=[])
            continue
        if sor.startswith('+') and not sor.startswith('++'):
            if SZ.CIMSOR_MINTA.match(sor[1:]):
                allapot['hc'].append(sor[1:].strip())
            continue
        if sor.startswith('-') and not sor.startswith('--'):
            allapot['torolt'] += 1
            if SZ.CIMSOR_MINTA.match(sor[1:]):
                allapot['tc'].append(sor[1:].strip())
    lezar()
    return ki


def e5_jelolo_sor(torlesek):
    """A commit-üzenetbe illeszthető jelölősor (a szándékot a végrehajtó erősíti meg)."""
    return 'TÖRLÉS-SZÁNDÉKOS: ' + '; '.join('%s — %s' % (f, le) for f, le in torlesek)


def commit_uzenetbe(szoveg, jelolo):
    """A jelölősor az üzenetbe, a `Co-Authored-By` sor(ok) elé (ha nincs ilyen, a végére)."""
    sorok = szoveg.rstrip('\n').split('\n')
    for i, s in enumerate(sorok):
        if s.startswith('Co-Authored-By:'):
            elotte = sorok[:i]
            while elotte and not elotte[-1].strip():
                elotte.pop()
            return '\n'.join(elotte + ['', jelolo, ''] + sorok[i:]) + '\n'
    return '\n'.join(sorok + ['', jelolo]) + '\n'


def e5_ellenoriz(alap, uzenet_fajl, e5_jelol, ir):
    mb = merge_base(alap)
    if mb is None:
        return [Lelet('E5', '-', 0, 'a merge-base nem állapítható meg (%s); az E5 nem vizsgálható' % alap, False)]
    diff = _git(['diff', '--unified=0', mb])
    if diff is None:
        return [Lelet('E5', '-', 0, 'a git diff nem futott; az E5 nem vizsgálható', False)]
    study = SZ._study_fajlok_halmaza_ref(mb) | SZ._study_fajlok_halmaza_ref('HEAD')
    torlesek = e5_torlesek(diff, study)
    if not torlesek:
        return []
    uzenetek = _git(['log', '--format=%B', '%s..HEAD' % mb]) or ''
    uzenet = ''
    if uzenet_fajl and os.path.exists(uzenet_fajl):
        with open(uzenet_fajl, encoding='utf-8') as f:
            uzenet = f.read()
    if SZ.SZANDEKOS_JELOLES_MINTA.search(uzenetek + '\n' + uzenet):
        return []
    jelolo = e5_jelolo_sor(torlesek)
    if e5_jelol and ir and uzenet_fajl:
        with open(uzenet_fajl, 'w', encoding='utf-8', newline='\n') as f:
            f.write(commit_uzenetbe(uzenet, jelolo))
        return [Lelet('E5', uzenet_fajl, 0, 'jelölősor beírva: %s' % jelolo, True)]
    return [Lelet('E5', f, 0, '%s; ha szándékos, a commit-üzenetbe: %s' % (le, jelolo), False)
            for f, le in torlesek]


# --------------------------------------------------------------------------
# futtatás
# --------------------------------------------------------------------------

def _kiir_diff(relut, regi, uj):
    for sor in difflib.unified_diff([_sor_torzs(s)[0] + '\n' for s in regi],
                                    [_sor_torzs(s)[0] + '\n' for s in uj],
                                    'a/' + relut, 'b/' + relut, n=0):
        sys.stdout.write(sor)


def munkafa_hozzaadott_sorok(mb, relut):
    """A munkafa `relut` fájljának a merge-base-hez képest hozzáadott/módosított sorai (halmaz); None: a fájl
    egésze új (nincs a merge-base-ben), vagy a diff nem állapítható meg."""
    if mb is None or _git(['cat-file', '-e', '%s:%s' % (mb, relut)]) is None:
        return None
    ki = _git(['diff', '--unified=0', mb, '--', relut])
    if ki is None:
        return None
    sorok = set()
    for sor in ki.splitlines():
        m = K._HUNK_FEJLEC.match(sor)
        if m:
            kezdo, hossz = int(m.group(1)), int(m.group(2)) if m.group(2) is not None else 1
            sorok.update(range(kezdo, kezdo + hossz))
    return sorok


def t2_szures(talalatok, hozzaadott):
    """Csak a hozzáadott sorok találatai (`hozzaadott` None: mind)."""
    return [t for t in talalatok if hozzaadott is None or t.sor in hozzaadott]


def t2_jelzesek(fajlok, alap):
    mb = merge_base(alap)
    leletek = []
    for f in fajlok:
        if not SZ.szamismetles_hatokor(f):
            continue
        for t in t2_szures(SZ.szamismetles([f]), munkafa_hozzaadott_sorok(mb, f)):
            leletek.append(Lelet('T2', t.fajl, t.sor, t.reszlet, False))
    return leletek


def fut(fajlok, alap, ir, uzenet_fajl=None, e5_jelol=False):
    leletek = []
    leletek += e32_javitasok(fajlok, ir)
    leletek += e8_javitasok(fajlok, ir)
    leletek += e5_ellenoriz(alap, uzenet_fajl, e5_jelol, ir)
    leletek += t2_jelzesek(fajlok, alap)
    return leletek


def main(argv=None):
    ap = argparse.ArgumentParser(description='F188 T3: előzetes formai javító (E32, E5, E8) a commit előtt.')
    ap.add_argument('fajlok', nargs='*', help='a vizsgált fájlok (alapból: a diff által érintettek)')
    ap.add_argument('--alap', default='origin/main', help='a diff alapja (merge-base ezzel; alap: origin/main)')
    ap.add_argument('--ir', action='store_true', help='a javítás a fájlba (alapból száraz futás)')
    ap.add_argument('--commit-uzenet-fajl', default=None, help='a készülő commit üzenetfájlja (E5)')
    ap.add_argument('--e5-jelol', action='store_true',
                    help='a TÖRLÉS-SZÁNDÉKOS jelölősor beírása az üzenetfájlba (--ir-rel és --commit-uzenet-fajl-lal)')
    args = ap.parse_args(argv)
    if args.fajlok:
        fajlok = [os.path.relpath(os.path.abspath(f), K.ROOT).replace(os.sep, '/') for f in args.fajlok]
    else:
        fajlok = erintett_fajlok(args.alap)
        if fajlok is None:
            print('Hiba: a merge-base nem állapítható meg (%s).' % args.alap, file=sys.stderr)
            return 2
    leletek = fut(fajlok, args.alap, args.ir, args.commit_uzenet_fajl, args.e5_jelol)
    javitott = [le for le in leletek if le.javitott]
    jelzett = [le for le in leletek if not le.javitott]
    mod = 'írás' if args.ir else 'száraz futás'
    print('\n# elojavit.py (%s): %d fájl, %d javítás%s, %d jelzés' % (
        mod, len(fajlok), len(javitott), '' if args.ir else ' (nem írva)', len(jelzett)))
    for le in javitott:
        print('- JAVÍT %s `%s:%s` — %s' % (le.szabaly, le.fajl, le.sor, le.szoveg))
    for le in jelzett:
        print('- JELEZ %s `%s:%s` — %s' % (le.szabaly, le.fajl, le.sor, le.szoveg))
    if any(le.szabaly != 'T2' for le in jelzett) or (javitott and not args.ir):  # a T2 tájékoztató
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
