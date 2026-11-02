#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jelolt_eloszures.py -- F150 (DT432): a dontesre varo (`dontes=nyitva`) elofordulas-jeloltek gepi
elo-szurese: atnezesi sorrend, NEM dontes. Kimenet: `naplok/ELOSZURES_<ID>.tsv` (munkalista, nem adat;
a `jeloltek.tsv`-t ez a szkript nem irja, CLAUDE.md 2. szabaly).

Szabaly (determinisztikus, modell es API nelkul): ha a jelolt versenek (tartomanynal az osszes versenek,
`lexikon_general.igehely_lista`) Strong-halmazaban (`szerep_karoli.vers_strongok`: TAHOT+TAGNT) egyetlen
gerinc-kombinacio sincs meg TELJESEN egy versben -- a kombinaciok a motivum `elofordulasok.tsv` `strong`
mezoi, a nyelvtani Strongok (`szerep_karoli.nyelvtani`) kiszuerve --, a javaslat `valoszinu_ki`.

HORDOZO (DT432, 2026-11-01): `valoszinu_ki` CSAK `azonossag_tipusa=formulaikus` motivumon lehet; minden mas
hordozon `vizsgalando` ("a hordozo nem formulaikus: a gepi szabaly nem dont").

LEXIKAI KITERJESZTES (N-F150a, DT432 (d)): a `LEXIKAI_BEKAPCSOLT` motivumain (alapertelmezetten ures: a
bevezetes a meres utan a felhasznalo/orkesztrator dontese) a lexikai hordozo is dont, de KITERJESZTETT
szaballyal (`vizsgal_lexikai`): (1) szomszedos versek: a jelolt versei +-1 vers egyutt adja az ablakot
(versen atnyulo parok: Luk 1:46-47); (2) rokon alakok: a kombinacio egy tagja a verssel kielegitett, ha az
ablakban van egy belole SZARMAZTATOTT szo (`Strong_szotar.tsv` "Gyok/Szarmaztatas": psuchikos <- G5590);
(3) nyelv: csak a jelolt nyelvu (G/H) kombinaciok szamitanak; ha a motivumnak nincs ilyen kombinacioja,
a gep nem dont (MENNY-001 ujszovetsegi helyei: a kombinaciok mind hebereek).

Oszlopok: igehely, javaslat, ok, hordozo, proveniencia. Rendezes: `vizsgalando` elol, `valoszinu_ki` a vegen,
azon belul kanonikus versrend. Fajl keszul MINDEN motivumra, amelynek van elofordulas-jeloltje (a nyitott
jelolt nelkulire fejlec-csak fajl): igy a mar eldontott jeloltek sora nem marad elavult.

Idempotens: a `ts` a bemeneti fajlok utolso git-commitjanak ideje (nem a futase), a `bemenet` a fajlok
HEAD-blobjai (a `gerinc_terkep.py` mintaja) -- ugyanarra a bemenetre bajtra azonos kimenet.

`--meres`: az eldontott (beepitve / elutasitva) jeloltekre is lefut, es a stdout-ra osszesitot ir
(hamis kizaras, felismert elutasitas); a vegleges kimenetbe NEM kerul.

    python eszkozok/jelolt_eloszures.py [--kimenet naplok] [--adat adat] [--meres]

TSV: split('\\t'), '\\t'.join; csv modul nelkul.
"""
import argparse
import collections
import datetime
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import szerep_karoli as SZK  # noqa: E402
import lexikon_general as LG  # noqa: E402  (csak importalva: igehely_lista)

ALAPERTELMEZETT_ADAT = os.path.join(ROOT, 'adat')
ALAPERTELMEZETT_KIMENET = os.path.join(ROOT, 'naplok')
DONTO_HORDOZO = 'formulaikus'
LEXIKAI_HORDOZO = 'lexikai'
# A lexikai motivumok, amelyeken a kiterjesztett szabaly dont (N-F150a). Ures: a bevezetes ⛔ a meres utan.
LEXIKAI_BEKAPCSOLT = frozenset()
STRONG_SZOTAR = os.path.join(ROOT, 'konkordancia', 'Strong_szotar.tsv')
VERS_RE = re.compile(r'^(.+) (\d+):(\d+)$')
STRONG_RE = re.compile(r'[GH]\d{1,4}')
OK_NEM_DONT = 'a hordozó nem formulaikus: a gépi szabály nem dönt'
FEJLEC = ['igehely', 'javaslat', 'ok', 'hordozo', 'proveniencia']
BEMENETI_FAJLOK = [
    'adat/jeloltek.tsv', 'adat/elofordulasok.tsv', 'adat/motivumok.tsv', 'adat/grammatikai_strongok.tsv',
    'konkordancia/TAHOT_kivonat.tsv', 'konkordancia/TAGNT_kivonat.tsv', 'konkordancia/Karoli_1908.tsv',
]
SCOPE = 'jeloltek.tsv (jelolt_tipus=elofordulas, dontes=nyitva) + elofordulasok.tsv (strong) + motivumok.tsv (azonossag_tipusa)'
FORRAS = 'TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (szerep_karoli.vers_strongok)'


def beolvas(ut):
    """[dict] -- split('\\t'), a '#' kommentsorok kihagyva; hiányzó fájl: üres."""
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n') if x.strip() and not x.startswith('#')]
    if not s:
        return []
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def kombinaciok(elofordulasok):
    """{motivum_id: [frozenset(nem nyelvtani Strongok)]} az `elofordulasok.tsv` sorainak `strong` mezőjéből."""
    ki = collections.defaultdict(set)
    for s in elofordulasok:
        if not s.get('strong'):
            continue
        k = frozenset(x for x in s['strong'].split('+') if x and not SZK.nyelvtani(x))
        if k:
            ki[s['id']].add(k)
    return {m: sorted(v, key=lambda k: sorted(k)) for m, v in ki.items()}


def vizsgal(igehely, kombok, vers_st):
    """(megvan: bool|None, ok): None, ha a versre nincs szöveg (TAHOT/TAGNT) vagy a motívumnak nincs kombinációja."""
    if not kombok:
        return None, 'nincs gerinc-kombináció a motívumhoz (elofordulasok.tsv strong)'
    versek = LG.igehely_lista(igehely.replace('–', '-'))
    halmazok = [h for h in (vers_st.get(v) for v in versek) if h]
    if not halmazok:
        return None, 'nincs szövegadat a TAHOT/TAGNT-ban ehhez az igehelyhez'
    megvan = [k for k in kombok if any(k <= h for h in halmazok)]
    if megvan:
        return True, 'a gerinc-szókapcsolat megvan: %s' % ', '.join('+'.join(sorted(k)) for k in megvan)
    uni = set().union(*halmazok)
    gerinc = set().union(*kombok)
    return False, 'a gerinc-szókapcsolat hiányzik: %s; a versben a gerincből: %s' % (
        ', '.join('+'.join(sorted(k)) for k in kombok), ', '.join(sorted(gerinc & uni)) or 'semmi')


def szarmazas(ut=STRONG_SZOTAR):
    """{Strong: frozenset(Strongok, amelyekből származtatott)} a `Strong_szotar.tsv` 5. oszlopából
    (Gyök/Származtatás, pl. 'πνεῦμα (G4151)', 'from H5307'); a számok 4 jegyre kiegészítve."""
    ki = {}
    if not os.path.exists(ut):
        return ki
    with open(ut, encoding='utf-8', newline='') as f:
        for sor in f.read().split('\n')[1:]:
            m = sor.rstrip('\r').split('\t')
            if len(m) < 5 or not m[0]:
                continue
            refs = frozenset(x[0] + x[1:].zfill(4) for x in STRONG_RE.findall(m[4]))
            if refs:
                ki[m[0]] = refs
    return ki


def ablak_versei(versek, vers_st):
    """A jelölt versei és a szomszédos (-1, +1) versek, amelyekre van szövegadat; kanonikus sorrendben."""
    ki = []
    for v in versek:
        m = VERS_RE.match(v)
        for x in ([v] if not m else ['%s %s:%d' % (m.group(1), m.group(2), int(m.group(3)) + d) for d in (-1, 0, 1)]):
            if x not in ki and vers_st.get(x):
                ki.append(x)
    return ki


def vizsgal_lexikai(igehely, kombok, vers_st, szarm=None, szomszed=True, rokon=True, nyelv=True):
    """Mint a `vizsgal`, de a lexikai kiterjesztett szabállyal (l. a modul docstringje).
    (megvan: bool|None, ok)."""
    if not kombok:
        return None, 'nincs gerinc-kombináció a motívumhoz (elofordulasok.tsv strong)'
    versek = LG.igehely_lista(igehely.replace('–', '-'))
    sajat = [vers_st.get(v) for v in versek if vers_st.get(v)]
    if not sajat:
        return None, 'nincs szövegadat a TAHOT/TAGNT-ban ehhez az igehelyhez'
    ablak = ablak_versei(versek, vers_st) if szomszed else [v for v in versek if vers_st.get(v)]
    uni = set().union(*(vers_st[v] for v in ablak))
    if nyelv:
        ny = 'G' if any(x.startswith('G') for x in set().union(*sajat)) else 'H'
        kombok = [k for k in kombok if all(x.startswith(ny) for x in k)]
        if not kombok:
            return None, 'a motívumnak nincs %s-nyelvű gerinc-kombinációja: a gépi szabály nem dönt' % ny
    szarm = szarm or {}

    def kielegit(s):
        return s in uni or (rokon and any(s in szarm.get(y, ()) for y in uni))

    megvan = [k for k in kombok if all(kielegit(s) for s in k)]
    if megvan:
        return True, 'a gerinc-szókapcsolat megvan: %s' % ', '.join('+'.join(sorted(k)) for k in megvan)
    gerinc = set().union(*kombok)
    return False, 'a gerinc-szókapcsolat hiányzik: %s; az ablakban a gerincből: %s' % (
        ', '.join('+'.join(sorted(k)) for k in kombok), ', '.join(sorted(gerinc & uni)) or 'semmi')


def javaslat(motivum, hordozo, igehely, komb, vers_st, szarm=None, lexikai_be=None):
    """(javaslat, ok) egy jelöltre. `lexikai_be`: a lexikai motívumok, ahol a kiterjesztett szabály dönt
    (alapértelmezés: LEXIKAI_BEKAPCSOLT)."""
    lexikai_be = LEXIKAI_BEKAPCSOLT if lexikai_be is None else lexikai_be
    if hordozo == LEXIKAI_HORDOZO and motivum in lexikai_be:
        megvan, ok = vizsgal_lexikai(igehely, komb.get(motivum, []), vers_st, szarm)
        return ('valoszinu_ki' if megvan is False else 'vizsgalando'), ok
    if hordozo != DONTO_HORDOZO:
        return 'vizsgalando', OK_NEM_DONT
    megvan, ok = vizsgal(igehely, komb.get(motivum, []), vers_st)
    return ('valoszinu_ki' if megvan is False else 'vizsgalando'), ok


def jeloltek_elofordulas(jeloltek):
    """[sor] az `elofordulas` típusúakból; (id, igehely) szerint az utolsó sor a mérvadó."""
    d = collections.OrderedDict()
    for r in jeloltek:
        if r.get('jelolt_tipus') == 'elofordulas':
            d[(r['id'], r['igehely'])] = r
    return list(d.values())


def sorok_szamit(adat_dir, dontesek=('nyitva',), vers_st=None, lexikai_be=None):
    """{motivum_id: [(igehely, javaslat, ok, hordozo, dontes)]} a megadott döntésű jelöltekre; minden
    előfordulás-jelöltes motívum szerepel (esetleg üres listával)."""
    vers_st = vers_st if vers_st is not None else SZK.vers_strongok()
    mot = {r['id']: r for r in beolvas(os.path.join(adat_dir, 'motivumok.tsv'))}
    komb = kombinaciok(beolvas(os.path.join(adat_dir, 'elofordulasok.tsv')))
    szarm = szarmazas()
    jel = jeloltek_elofordulas(beolvas(os.path.join(adat_dir, 'jeloltek.tsv')))
    ki = collections.OrderedDict((m, []) for m in sorted({r['id'] for r in jel}))
    for r in jel:
        if r['dontes'] not in dontesek:
            continue
        m = r['id']
        hordozo = mot.get(m, {}).get('azonossag_tipusa', '?')
        j, ok = javaslat(m, hordozo, r['igehely'], komb, vers_st, szarm, lexikai_be)
        ki[m].append((r['igehely'], j, ok, hordozo, r['dontes']))
    for m in ki:
        ki[m].sort(key=lambda x: (x[1] == 'valoszinu_ki', SZK.vers_kulcs(x[0])))
    return ki


def _git(args, root):
    try:
        r = subprocess.run(['git', '-C', root] + args, capture_output=True, text=True, encoding='utf-8')
    except OSError:
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def bemenet_azonosito(root):
    """(bemenet-szöveg, ts): a bemeneti fájlok HEAD-blobjai és utolsó commitjuk ideje (nem a futásé)."""
    resz = []
    for f in BEMENETI_FAJLOK:
        h = _git(['rev-parse', 'HEAD:%s' % f], root)
        resz.append('%s@%s' % (f, h[:10] if h else 'nincs-git'))
    ep = _git(['log', '-1', '--format=%ct', '--'] + BEMENETI_FAJLOK, root)
    ts = (datetime.datetime.fromtimestamp(int(ep), datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
          if ep and ep.isdigit() else 'ismeretlen')
    return ','.join(resz), ts


def tsv_szoveg(motivum, sorok, bemenet, ts):
    fej = ('# GENERÁLT: jelolt_eloszures.py | átnézési sorrend, NEM döntés (a döntés a jeloltek.tsv-ben, a felhasználóé) | '
           'motivum=%s | n=%d | bemenet=%s | ts=%s' % (motivum, len(sorok), bemenet, ts))
    ki = [fej, '\t'.join(FEJLEC)]
    for igehely, j, ok, hordozo, _d in sorok:
        prov = 'scope=%s | forras=%s | motivum=%s | ts=%s' % (SCOPE, FORRAS, motivum, ts)
        ki.append('\t'.join([igehely, j, ok, hordozo, prov]))
    return '\n'.join(ki) + '\n'


def futtat(adat_dir=ALAPERTELMEZETT_ADAT, root=ROOT, kimenet_dir=None, bemenet_fn=None, vers_st=None):
    """{motivum_id: tsv-szöveg}; ha `kimenet_dir` van, a fájlokat (LF) ki is írja."""
    bemenet, ts = (bemenet_fn or bemenet_azonosito)(root)
    szovegek = collections.OrderedDict()
    for m, sorok in sorok_szamit(adat_dir, vers_st=vers_st).items():
        szovegek[m] = tsv_szoveg(m, sorok, bemenet, ts)
    if kimenet_dir:
        os.makedirs(kimenet_dir, exist_ok=True)
        for m, sz in szovegek.items():
            with open(os.path.join(kimenet_dir, 'ELOSZURES_%s.tsv' % m), 'w', encoding='utf-8', newline='\n') as f:
                f.write(sz)
    return szovegek


def meres(adat_dir=ALAPERTELMEZETT_ADAT, vers_st=None, lexikai_be=None):
    """Az eldöntött jelöltekre: motívumonként (beépítve, hamis kizárás, elutasítva, felismert). Csak stdout."""
    ki = sorok_szamit(adat_dir, dontesek=('beépítve', 'elutasítva'), vers_st=vers_st, lexikai_be=lexikai_be)
    mot = {r['id']: r for r in beolvas(os.path.join(adat_dir, 'motivumok.tsv'))}
    ossz = collections.OrderedDict()
    for m, sorok in ki.items():
        be = [s for s in sorok if s[4] == 'beépítve']
        el = [s for s in sorok if s[4] == 'elutasítva']
        ossz[m] = {
            'hordozo': mot.get(m, {}).get('azonossag_tipusa', '?'),
            'beepitve': len(be), 'hamis_kizaras': [s[0] for s in be if s[1] == 'valoszinu_ki'],
            'elutasitva': len(el), 'felismert': sum(1 for s in el if s[1] == 'valoszinu_ki'),
        }
    return ossz


def main():
    ap = argparse.ArgumentParser(description='F150 -- a jelöltek gépi elő-szűrése (átnézési sorrend)')
    ap.add_argument('--kimenet', default=ALAPERTELMEZETT_KIMENET, help='kimeneti könyvtár (alapértelmezés: naplok/)')
    ap.add_argument('--adat', default=ALAPERTELMEZETT_ADAT, help='az adat/ könyvtár')
    ap.add_argument('--meres', action='store_true',
                    help='az eldöntött jelöltekre is: összesítő a stdout-ra (hamis kizárás, felismert elutasítás); nem ír fájlt')
    args = ap.parse_args()
    if args.meres:
        print('motivum\thordozo\tbeepitve\thamis_kizaras\telutasitva\tfelismert')
        for m, d in meres(args.adat).items():
            print('\t'.join([m, d['hordozo'], str(d['beepitve']), str(len(d['hamis_kizaras'])),
                             str(d['elutasitva']), str(d['felismert'])]))
        return 0
    szovegek = futtat(args.adat, kimenet_dir=args.kimenet)
    for m, sz in szovegek.items():
        sorok = [l for l in sz.split('\n')[2:] if l]
        ki_db = sum(1 for l in sorok if l.split('\t')[1] == 'valoszinu_ki')
        print('  ELOSZURES_%s.tsv: %d sor, valoszinu_ki %d, vizsgalando %d' % (m, len(sorok), ki_db, len(sorok) - ki_db),
              file=sys.stderr)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
