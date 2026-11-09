#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_kh_mek.py -- a Károli-kereszthivatkozások ellenőrzése a MEK 00161 kiadással (F177, KAROLI_KH_MEK).

A `konkordancia/Karoli_kereszthivatkozasok.tsv` (HunKar OSIS <- szentiras.hu KG) ismert hibája, hogy sok vers egy
másik vers KH-listáját hordozza (N-F156a). A MEK 00161 kiadás (*Szent Biblia*, Károli) versenként, a vers alatt adja
a KH-t, a HunKar-tól függetlenül: ez a második, független tanú. A nyers RTF NEM kerül a repóba.

Két alparancs:

  kivonat <rtf> [--ki konkordancia/Karoli_KH_MEK.tsv] [--naplo <fájl>] [--sha256 <hex>] [--ts <dátum>]
      RTF-dekódolás (a `\\'xx` cp1250, a `\\uN`), könyvpárosítás a MEK saját tartalomjegyzéke szerint (66 cím,
      kánoni sorrend), fejezet-/versfelismerés, a KH-sor a vers után. Kimenet: igehely, kapcsolodo (STEPBible-alak),
      mek_alak (szó szerint), proveniencia. A MEK a tartományt két végponttal sorolja: ezt megőrzi.

  osszevet [--ki konkordancia/Karoli_KH_javitott.tsv] [--jelentes <fájl>]
      versellenőrzés (a hivatkozott vers létezik-e a Karoli_1908.tsv-ben), versenkénti összevetés a HunKar-táblával,
      TSK-támogatás; háromszintű tábla: megerositett / kiesik / jelolt. A `jelolt` sorokról NEM dönt (CLAUDE.md 2.).

TSV-olvasás/írás: `split('\\t')` / `'\\t'.join()`, a `csv` modul nem használható (CLAUDE.md).
"""
import argparse
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HELY = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(HELY)
sys.path.insert(0, HELY)

KONK = 'konkordancia'
MEK_TSV = KONK + '/Karoli_KH_MEK.tsv'
JAVITOTT = KONK + '/Karoli_KH_javitott.tsv'
HUNKAR = KONK + '/Karoli_kereszthivatkozasok.tsv'
ALIAS = KONK + '/Karoli_KH_MEK_konyvaliasok.tsv'
KAROLI = KONK + '/Karoli_1908.tsv'
NORM = KONK + '/Konyv_normalizalo_tabla.tsv'
MEK_URL = 'https://mek.oszk.hu/00100/00161/00161.rtf'
SZERKEZET = KONK + '/Karoli_KH_MEK_versszerkezet.tsv'
SZINTEK = ('megerositett', 'kiesik', 'jelolt')


# ----------------------------------------------------------------------------------------------------------------
# közös segédek
# ----------------------------------------------------------------------------------------------------------------

def tsv_sorok(rel, fejlec=True):
    """TSV beolvasása `split('\\t')`-tel; a `#` kezdetű (generált) fejsorokat átugorja."""
    ut = rel if os.path.isabs(rel) else os.path.join(GYOKER, rel)
    ki = []
    with open(ut, encoding='utf-8', newline='') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if s.startswith('#'):
                continue
            ki.append(s.split('\t'))
    return ki[1:] if fejlec else ki


def tsv_ir(rel, fejsor, sorok, megjegyzes=None):
    ut = rel if os.path.isabs(rel) else os.path.join(GYOKER, rel)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        if megjegyzes:
            f.write(megjegyzes.rstrip('\n') + '\n')
        f.write('\t'.join(fejsor) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')


def hu_step():
    """Magyar rövidítés -> STEPBible-rövidítés (a normalizáló táblából)."""
    return {m[1]: m[0] for m in tsv_sorok(NORM) if len(m) > 1}


def step_konyvek():
    """A 66 STEP-kód kánoni sorrendben (a normalizáló tábla sorrendje)."""
    return [m[0] for m in tsv_sorok(NORM) if m and m[0]]


def aliasok(forras):
    """Rövidítés -> STEP-kód a `konkordancia/Karoli_KH_MEK_konyvaliasok.tsv`-ből (nem kódba szórva); `forras`:
    'mek' (a MEK KH-sorainak rövidítései, pl. 'Mát.') vagy 'karoli_1908' (a Karoli_1908.tsv eltérései, pl. 'Sir')."""
    ki = {}
    for m in tsv_sorok(ALIAS):
        if len(m) >= 3 and m[0] == forras and m[1]:
            ki[m[1]] = m[2]
    return ki


def mek_aliasok():
    return aliasok('mek')


def step_ref(ref):
    m = re.match(r'(\w+)\.(\d+)\.(\d+)$', ref or '')
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def ref_str(t):
    return '%s.%d.%d' % t


# ----------------------------------------------------------------------------------------------------------------
# RTF -> bekezdések (stílus, szöveg)
# ----------------------------------------------------------------------------------------------------------------

_TOK = re.compile(r"\\'([0-9a-fA-F]{2})|\\([a-zA-Z]+)(-?\d+)? ?|\\([^a-zA-Z])|([{}])|([^\\{}]+)")
_KIHAGY = {'fonttbl', 'colortbl', 'stylesheet', 'info', 'fldinst', 'datafield', 'pntext', 'pnseclvl', 'userprops',
           'revtbl', 'template', 'listtable', 'listoverridetable', 'bkmkstart', 'bkmkend', 'generator', 'header',
           'footer'}


def rtf_bekezdesek(adat):
    """A nyers RTF (bytes) -> [(bekezdésstílus-szám vagy None, szöveg)]. A `\\sN` a bekezdés-stílus (1: könyvcím,
    2: fejezetcím, 3: KH-sor; a törzsszöveg stílus nélküli). A célcsoportok (betűtípus-, stílus-, mezőutasítás-,
    könyvjelző-táblák) kimaradnak; a mező eredménye (`fldrslt`) megmarad."""
    s = adat.decode('latin-1')
    verem = []
    kihagy = 0
    sor = []
    stilus = None
    ki = []
    atugr = 0
    for m in _TOK.finditer(s):
        h, w, n, sym, br, txt = m.groups()
        if br == '{':
            verem.append(kihagy)
            continue
        if br == '}':
            kihagy = verem.pop() if verem else 0
            continue
        if kihagy:
            continue
        if h:
            if atugr:
                atugr -= 1
                continue
            sor.append(bytes([int(h, 16)]).decode('cp1250'))
            continue
        if w:
            if w == 'par':
                ki.append((stilus, ''.join(sor)))
                sor = []
            elif w == 'pard':
                stilus = None
            elif w == 's' and n is not None:
                stilus = int(n)
            elif w == 'u' and n is not None:
                sor.append(chr(int(n) % 65536))
                atugr = 1
            elif w == 'tab':
                sor.append('\t')
            elif w == 'line':
                sor.append(' ')
            elif w in _KIHAGY:
                kihagy = 1
            continue
        if sym:
            if sym == '*':
                kihagy = 1
            elif sym in '\\{}':
                sor.append(sym)
            elif sym == '~':
                sor.append(' ')
            continue
        if txt:
            if atugr:
                txt = txt[1:]
                atugr = 0
            sor.append(txt.replace('\r', '').replace('\n', ''))
    if sor:
        ki.append((stilus, ''.join(sor)))
    return ki


# ----------------------------------------------------------------------------------------------------------------
# kivonat
# ----------------------------------------------------------------------------------------------------------------

_VERS = re.compile(r'^\s*(\d+)\.\s*(.*)$')
_FEJEZET = re.compile(r'^\s*(\d+)\.?\s*$')
_KH_TAG = re.compile(r'^\s*((?:\d\s)?[^\d,.\s][^\d,]*?\.)\s*(\d+),(\d+)\.?\s*$')
_TESTAMENTUM = re.compile(r'^\s*AZ\s+(ÓTESTAMENTOM|ÚJ\s+TESTAMENTOM)', re.I)


def kh_tagok(szoveg):
    """A KH-bekezdés szétvágása hivatkozásokra: 'A. 1,2. , B. 3,4.' -> ['A. 1,2.', 'B. 3,4.'] (mek_alak)."""
    return [p.strip() for p in re.split(r'(?<=\.)\s*,\s+(?=\S)', szoveg.strip()) if p.strip()]


def mek_kivonat(adat, aliasok, konyvek):
    """(sorok, naplo). sorok: [(igehely STEP, kapcsolodo STEP, mek_alak)], a MEK forrássorrendjében.
    naplo: dict a diagnosztikával (könyvcímek, szám, eltérések)."""
    par = rtf_bekezdesek(adat)
    cimek = []
    for st, t in par:
        t = t.strip()
        if st == 1 and t and not _TESTAMENTUM.match(t):
            cimek.append(t)
    nap = {'cimek': cimek, 'fejezet_nelkul_uj': [], 'fejezet_eltero': [], 'vers_ugras': [], 'ismeretlen_bekezdes': [],
           'kh_vers_elott': [], 'ismeretlen_konyv': [], 'ertelmezhetetlen_kh': [], 'versek': 0, 'fejezetek': 0,
           'szerkezet': collections.OrderedDict()}
    if len(cimek) != len(konyvek):
        nap['hiba'] = 'a MEK könyvcímeinek száma %d, a kánoné %d' % (len(cimek), len(konyvek))
        return [], nap
    sorok = []
    kon = -1
    fej = 0
    vers = 0
    utolso = None  # az utolsó vers STEP-kulcsa
    fejezetsor_jott = False
    kezdett = False
    for st, t in par:
        t = t.strip()
        if st == 1 and t and not _TESTAMENTUM.match(t):
            kon += 1
            fej = 0
            vers = 0
            utolso = None
            kezdett = True
            continue
        if not kezdett or not t:
            continue
        if st == 2:
            m = _FEJEZET.match(t)
            if m:
                fej_uj = int(m.group(1))
                if fej_uj != fej + 1:
                    nap['fejezet_eltero'].append((konyvek[kon], fej, fej_uj))
                fej = fej_uj
                vers = 0
                utolso = None
                fejezetsor_jott = True
                nap['fejezetek'] += 1
            else:
                nap['ismeretlen_bekezdes'].append((konyvek[kon], fej, 's2', t[:60]))
            continue
        if st == 3:
            if utolso is None:
                nap['kh_vers_elott'].append((konyvek[kon], fej, t[:60]))
                continue
            for tag in kh_tagok(t):
                m = _KH_TAG.match(tag)
                if not m:
                    nap['ertelmezhetetlen_kh'].append((utolso, tag))
                    sorok.append((utolso, '', tag))  # a MEK-elírás szó szerint megmarad; kapcsolodo üres
                    continue
                ab = m.group(1).strip()
                if ab not in aliasok:
                    nap['ismeretlen_konyv'].append((utolso, ab))
                    sorok.append((utolso, '', tag))
                    continue
                cel = '%s.%d.%d' % (aliasok[ab], int(m.group(2)), int(m.group(3)))
                sorok.append((utolso, cel, tag))
            continue
        if st is None:
            m = _VERS.match(t)
            if not m:
                nap['ismeretlen_bekezdes'].append((konyvek[kon], fej, 'torzs', t[:60]))
                continue
            nyomtatott = int(m.group(1))
            if nyomtatott == 1 and vers >= 1 and not fejezetsor_jott:
                fej += 1  # fejezetsor nélkül 1-re ugró vers: új fejezet
                nap['fejezet_nelkul_uj'].append((konyvek[kon], fej))
                nap['fejezetek'] += 1
                vers = 0
            fejezetsor_jott = False
            vers += 1  # a versszám a sorrendből jön; a nyomtatott szám eltérése naplóba kerül (MEK-számozási hiba)
            if nyomtatott != vers:
                nap['vers_ugras'].append((konyvek[kon], fej, vers, nyomtatott))
            utolso = '%s.%d.%d' % (konyvek[kon], fej, vers)
            nap['versek'] += 1
            nap['szerkezet'][(konyvek[kon], fej)] = vers
    return sorok, nap


def proveniencia_mek(sha, ts):
    return ('scope=MEK 00161 Szent Biblia (Károli) sha256=%s (URL, letöltés: konkordancia/Karoli_KH_MEK_README.md) | '
            'forras=eszkozok/karoli_kh_mek.py kivonat | ts=%s' % (sha[:12], ts))


def kivonat_main(a):
    import hashlib
    adat = open(a.rtf, 'rb').read()
    sha = a.sha256 or hashlib.sha256(adat).hexdigest()
    ts = a.ts or os.environ.get('PARDES_DATUM', '2026-11-09')
    konyvek = step_konyvek()
    sorok, nap = mek_kivonat(adat, mek_aliasok(), konyvek)
    if 'hiba' in nap:
        print('HIBA: ' + nap['hiba'], file=sys.stderr)
        return 1
    prov = proveniencia_mek(sha, ts)
    tsv_ir(a.ki, ['igehely', 'kapcsolodo', 'mek_alak', 'proveniencia'], [[v, c, al, prov] for v, c, al in sorok])
    tsv_ir(a.szerkezet, ['konyv', 'fejezet', 'versszam'],
           [[k, str(f), str(n)] for (k, f), n in nap['szerkezet'].items()])
    nap['sor'] = len(sorok)
    nap['sha256'] = sha
    szoveg = naplo_szoveg(nap, konyvek)
    print(szoveg)
    if a.naplo:
        with open(a.naplo, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg + '\n')
    return 0


def naplo_szoveg(nap, konyvek):
    ki = ['MEK-kivonat: %d vers, %d fejezet, %d KH-sor; SHA-256 %s' % (
        nap['versek'], nap['fejezetek'], nap.get('sor', 0), nap.get('sha256', '?'))]
    ki.append('könyvcímek (%d): ' % len(nap['cimek']) + ' | '.join('%s=%s' % (k, c) for k, c in zip(konyvek, nap['cimek'])))
    for kulcs in ('fejezet_nelkul_uj', 'fejezet_eltero', 'vers_ugras', 'ismeretlen_bekezdes', 'kh_vers_elott',
                  'ismeretlen_konyv', 'ertelmezhetetlen_kh'):
        ki.append('%s: %d %s' % (kulcs, len(nap[kulcs]), repr(nap[kulcs][:15]) if nap[kulcs] else ''))
    return '\n'.join(ki)


# ----------------------------------------------------------------------------------------------------------------
# összevetés
# ----------------------------------------------------------------------------------------------------------------

def karoli_versek():
    """A Karoli_1908.tsv versei STEP-kulccsal (halmaz)."""
    norm = dict(hu_step())
    norm.update(aliasok('karoli_1908'))
    ki = set()
    for m in tsv_sorok(KAROLI):
        r = re.match(r'(\S+) (\d+):(\d+)$', m[0])
        if r and r.group(1) in norm:
            ki.add('%s.%s.%s' % (norm[r.group(1)], r.group(2), r.group(3)))
    return ki | mek_versek()


def mek_versek():
    """A MEK saját vers-szerkezete (STEP-kulcsok) a Karoli_KH_MEK_versszerkezet.tsv-ből. A Karoli_1908.tsv
    néhány versben két MEK-verset hordoz egyben (pl. Ján 1:51 = a MEK 1:51 és 1:52), ezért a MEK külön versei hiányoznak belőle."""
    ki = set()
    for m in tsv_sorok(SZERKEZET):
        if len(m) >= 3:
            for v in range(1, int(m[2]) + 1):
                ki.add('%s.%s.%d' % (m[0], m[1], v))
    return ki


def hunkar_sorok():
    """[(forras, cel_nyers, kezdet, veg)] a HunKar-táblából; a tartomány 'A-B' egy sor (kezdet != veg)."""
    ki = []
    for m in tsv_sorok(HUNKAR):
        if len(m) < 2 or not m[0]:
            continue
        reszek = m[1].split('-')
        ki.append((m[0], m[1], reszek[0], reszek[-1]))
    return ki


def mek_sorok_betolt():
    """{forras: [(cel, mek_alak)]} a Karoli_KH_MEK.tsv-ből, forrássorrendben."""
    ki = collections.OrderedDict()
    for m in tsv_sorok(MEK_TSV):
        if len(m) >= 3:
            ki.setdefault(m[0], []).append((m[1], m[2]))
    return ki


def vers_letezik(ref, letezo):
    return ref in letezo


def hibas_lista(refek, letezo):
    """A nem létező (vagy nem értelmezhető) hivatkozások: üres kapcsolodo = a MEK-elírás szó szerinti sora."""
    return ['ertelmezhetetlen' if not r else r for r in refek if not r or r not in letezo]


def osszevet(hk, mek, letezo, tamogat_):
    def tamogat(f, c):
        return bool(c) and tamogat_(f, c)

    """A háromszintű tábla sorai: [(igehely, kapcsolodo, szint, forras, indok)].

    hk: [(forras, cel_nyers, kezdet, veg)] a HunKar-sorok; mek: {forras: [(cel, mek_alak)]}.
    letezo: a Karoli_1908 versei (STEP). tamogat(forras, cel) -> bool (TSK / visszautalás).
    Szabály (sor-szinten):
      - a HunKar-sor és a MEK ugyanarra a versre mind a végpontjait listázza -> egyezik;
      - egyező sor: `megerositett`, ha a forrásvers és minden végpont létezik a Károli-szövegben, különben `jelolt`
        (hibas_hivatkozas);
      - HunKar-sor, ha a MEK a versen semmit nem ad -> `kiesik` (az indokban tsk=igen|nem is);
      - HunKar-sor, ha a MEK a versen mást ad -> `jelolt` (eltér); a MEK-sor, amelyet a HunKar a versen nem ad
        -> `jelolt` (csak MEK). A versellenőrzés és a TSK-támogatás az indokban."""
    ki = []
    hk_verseken = collections.OrderedDict()
    for sor in hk:
        hk_verseken.setdefault(sor[0], []).append(sor)
    for forras, sorok in hk_verseken.items():
        mek_cel = mek.get(forras, [])
        felhasznalt = [False] * len(mek_cel)
        for _, cel_nyers, kezdet, veg in sorok:
            vegpontok = [kezdet] if kezdet == veg else [kezdet, veg]
            egyezik = bool(mek_cel)
            idx = []
            if mek_cel:
                for vp in vegpontok:
                    j = next((i for i, (c, _) in enumerate(mek_cel) if c == vp), None)
                    if j is None:
                        egyezik = False
                        break
                    idx.append(j)
            hibas = hibas_lista([forras] + vegpontok, letezo)
            if egyezik:
                for j in idx:
                    felhasznalt[j] = True
                if hibas:
                    ki.append((forras, cel_nyers, 'jelolt', 'HunKar+MEK',
                               'egyezik;hibas_hivatkozas=' + ','.join(hibas)))
                else:
                    ki.append((forras, cel_nyers, 'megerositett', 'HunKar+MEK', 'egyezik'))
            elif not mek_cel:
                ki.append((forras, cel_nyers, 'kiesik', 'HunKar', 'mek_ures_vers;tsk=' + (
                    'igen' if tamogat(forras, kezdet) else 'nem') + (
                    ';hibas_hivatkozas=' + ','.join(hibas) if hibas else '')))
            else:
                ind = 'eltero_lista;tsk=' + ('igen' if tamogat(forras, kezdet) else 'nem')
                if hibas:
                    ind += ';hibas_hivatkozas=' + ','.join(hibas)
                ki.append((forras, cel_nyers, 'jelolt', 'HunKar', ind))
        for i, (c, al) in enumerate(mek_cel):
            if felhasznalt[i]:
                continue
            hibas = hibas_lista([forras, c], letezo)
            ind = 'csak_mek;mek_alak=%s;tsk=%s' % (al, 'igen' if tamogat(forras, c) else 'nem')
            if hibas:
                ind += ';hibas_hivatkozas=' + ','.join(hibas)
            ki.append((forras, c, 'jelolt', 'MEK', ind))
    for forras, mek_cel in mek.items():
        if forras in hk_verseken:
            continue
        for c, al in mek_cel:
            hibas = hibas_lista([forras, c], letezo)
            ind = 'csak_mek;mek_alak=%s;tsk=%s' % (al, 'igen' if tamogat(forras, c) else 'nem')
            if hibas:
                ind += ';hibas_hivatkozas=' + ','.join(hibas)
            ki.append((forras, c, 'jelolt', 'MEK', ind))
    return ki


def tamogato():
    """tamogat(forras, cel) a karoli_kh_epseg.tamogatott szabályával (TSK ±3 vers; a visszautalás a HunKar- ÉS a
    MEK-listán)."""
    import karoli_kh_epseg as E
    kh, tsk = E.betolt()
    for forras, tagok in mek_sorok_betolt().items():
        for c, _ in tagok:
            if c not in kh.get(forras, []):
                kh.setdefault(forras, []).append(c)
    return lambda forras, cel: E.tamogatott(forras, cel, kh, tsk)


def proveniencia_javitott(ts):
    return ('scope=konkordancia/Karoli_kereszthivatkozasok.tsv + konkordancia/Karoli_KH_MEK.tsv + '
            'konkordancia/Karoli_1908.tsv + konkordancia/TSK_kereszthivatkozasok.tsv | '
            'forras=eszkozok/karoli_kh_mek.py osszevet | ts=%s' % ts)


def osszevet_main(a):
    ts = a.ts or os.environ.get('PARDES_DATUM', '2026-11-09')
    hk = hunkar_sorok()
    mek = mek_sorok_betolt()
    sorok = osszevet(hk, mek, karoli_versek(), tamogato())
    prov = proveniencia_javitott(ts)
    fej = '# GENERÁLT: eszkozok/karoli_kh_mek.py osszevet — kézzel szerkeszteni tilos; a szintek: megerositett / ' \
          'kiesik / jelolt (a jelolt sorokról nincs döntés, CLAUDE.md 2. szabály)'
    tsv_ir(a.ki, ['igehely', 'kapcsolodo', 'szint', 'forras', 'indok', 'proveniencia'],
           [[v, c, sz, fo, ind, prov] for v, c, sz, fo, ind in sorok], fej)
    stat = osszegzes(sorok, hk, mek)
    print(stat)
    if a.jelentes:
        with open(a.jelentes, 'w', encoding='utf-8', newline='\n') as f:
            f.write(stat + '\n')
    return 0


def osszegzes(sorok, hk, mek):
    szamlalo = collections.Counter(s[2] for s in sorok)
    return '\n'.join('%s: %d' % (k, szamlalo.get(k, 0)) for k in SZINTEK) + '\nsor összesen: %d' % len(sorok)


def main():
    ap = argparse.ArgumentParser(description='Károli-KH ellenőrzés a MEK 00161 kiadással (F177)')
    sp = ap.add_subparsers(dest='parancs', required=True)
    k = sp.add_parser('kivonat')
    k.add_argument('rtf')
    k.add_argument('--ki', default=os.path.join(GYOKER, MEK_TSV))
    k.add_argument('--naplo')
    k.add_argument('--szerkezet', default=os.path.join(GYOKER, SZERKEZET))
    k.add_argument('--sha256')
    k.add_argument('--ts')
    o = sp.add_parser('osszevet')
    o.add_argument('--ki', default=os.path.join(GYOKER, JAVITOTT))
    o.add_argument('--jelentes')
    o.add_argument('--ts')
    a = ap.parse_args()
    return kivonat_main(a) if a.parancs == 'kivonat' else osszevet_main(a)


if __name__ == '__main__':
    sys.exit(main())
