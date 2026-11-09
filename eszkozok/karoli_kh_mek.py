#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_kh_mek.py -- a Károli-kereszthivatkozások ellenőrzése a MEK 00161 kiadással (F177, KAROLI_KH_MEK).

A `konkordancia/Karoli_kereszthivatkozasok.tsv` (HunKar OSIS <- szentiras.hu KG) ismert hibája, hogy sok vers egy
másik vers KH-listáját hordozza (N-F156a). A MEK 00161 kiadás (*Szent Biblia*, Károli) versenként, a vers alatt adja
a KH-t, a HunKar-tól függetlenül: ez a második, független tanú. A nyers RTF NEM kerül a repóba.

Négy alparancs (a harmadik és negyedik: F181):

  kivonat <rtf> [--ki konkordancia/Karoli_KH_MEK.tsv] [--naplo <fájl>] [--sha256 <hex>] [--ts <dátum>]
      RTF-dekódolás (a `\\'xx` cp1250, a `\\uN`), könyvpárosítás a MEK saját tartalomjegyzéke szerint (66 cím,
      kánoni sorrend), fejezet-/versfelismerés, a KH-sor a vers után. Kimenet: igehely, kapcsolodo (STEPBible-alak),
      mek_alak (szó szerint), proveniencia. A MEK a tartományt két végponttal sorolja: ezt megőrzi.

  osszevet [--ki konkordancia/Karoli_KH_javitott.tsv] [--jelentes <fájl>]
      versellenőrzés (a hivatkozott vers létezik-e a Karoli_1908.tsv-ben), versenkénti összevetés a HunKar-táblával,
      TSK-támogatás; háromszintű tábla: megerositett / kiesik / jelolt. A `jelolt` sorokról NEM dönt (CLAUDE.md 2.).

  jelolt-bontas [--be konkordancia/Karoli_KH_javitott.tsv] [--jelentes <fájl>] [--modell <név>] [--ts <dátum>]
      a `jelolt` szint mérése és bontása (altípusok, a beemelési szabály soronkénti döntése, könyvenkénti eloszlás,
      a jelölt szint súlya; a TSK csak tájékoztatás). Csak olvas, a táblát nem módosítja.

  beemel [--be konkordancia/Karoli_KH_javitott.tsv] [--ki <fájl>] [--ts <dátum>]
      a beemelési szabály alkalmazása: a MEK-oldali jelölt sor megerositett lesz, kivéve a nem létező
      célvers és a gyanús ismétlődés; a MEK-listával ütköző HunKar-oldali jelölt sor kiesik. A sorok száma nem változik.

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
    sorok6 = [[v, c, sz, fo, ind, prov] for v, c, sz, fo, ind in sorok]
    if not a.nyers:
        # F181 (DT-F181d): az osszevet kimenete a beemelési szabállyal együtt áll elő, hogy az újragenerálás ne
        # veszítse el a J4 állapotát; a #177 háromszintű nyers állapota a --nyers kapcsolóval.
        bontas, _, _ = _bontas_sorokra(sorok6)
        sorok6 = beemel(sorok6, bontas, ts)
        sorok = [tuple(m[:5]) for m in sorok6]
        fej = FEJ_BEEMELT
    tsv_ir(a.ki, ['igehely', 'kapcsolodo', 'szint', 'forras', 'indok', 'proveniencia'], sorok6, fej)
    stat = osszegzes(sorok, hk, mek)
    print(stat)
    if a.jelentes:
        with open(a.jelentes, 'w', encoding='utf-8', newline='\n') as f:
            f.write(stat + '\n')
    return 0


def osszegzes(sorok, hk, mek):
    szamlalo = collections.Counter(s[2] for s in sorok)
    return '\n'.join('%s: %d' % (k, szamlalo.get(k, 0)) for k in SZINTEK) + '\nsor összesen: %d' % len(sorok)


# ----------------------------------------------------------------------------------------------------------------
# F181: a `jelolt` szint mérése (jelolt-bontas, J1), a beemelési szabály (J2) és alkalmazása (beemel, J4).
# DT-F181d (a felhasználó szava, 2026-11-09): „TSK külön rendszer, nem kell összevetni őket. Károlinak meg elfogadjuk a
# MEK-et, ha ott nem volt gyanús ismétlődő.” A TSK tehát NEM tanú és nem feltétel: a bontásban csak tájékoztató.
# ----------------------------------------------------------------------------------------------------------------

GYANUS_TSV = KONK + '/Karoli_kereszthivatkozasok_gyanus.tsv'
SZABALY_JEL = 'szabaly=F181'
FEJ_BEEMELT = ('# GENERÁLT: eszkozok/karoli_kh_mek.py osszevet + beemel — kézzel szerkeszteni tilos; a szintek: '
               'megerositett / kiesik / jelolt (a jelolt sorokról a döntés nélküli maradék: Karoli_KH_MEK_README.md 7.)')
ALTIPUSOK = ('tartomány/vershatár', 'könyv-elírás', 'fejezet-elírás', 'versszám-elírás', 'eltér (nem sorolható)',
             'csak MEK', 'egyéb (egyező, de nem létező hivatkozás)')
_RANG = {'tartomány/vershatár': 0, 'versszám-elírás': 1, 'fejezet-elírás': 2, 'könyv-elírás': 3}
ELIRAS = ('könyv-elírás', 'fejezet-elírás', 'versszám-elírás')
TSK_KATEGORIAK = ('mindkettő', 'csak a MEK-cél', 'csak a HunKar-cél', 'egyik sem')

# a döntés-kategóriák (a szabály kimenete soronként)
D_BEEMEL = 'beemel (MEK-sor -> megerositett)'
D_NEMLETEZO = 'marad: nem létező célvers'
D_GYANUS = 'marad: gyanús ismétlődő'
D_HK_KIESIK = 'HunKar-sor -> kiesik (a MEK-lista elfogadva a versen)'
D_HK_MARAD = 'HunKar-sor marad jelölt (a MEK-sor nem emelődik be)'
DONTESEK = (D_BEEMEL, D_GYANUS, D_NEMLETEZO, D_HK_KIESIK, D_HK_MARAD)


def gyanus_versek():
    """A #177 gyanús-jelölése (HunKar-oldali): a `Karoli_kereszthivatkozasok_gyanus.tsv` forrásversei (STEP-alak)."""
    return {m[0] for m in tsv_sorok(GYANUS_TSV) if m and m[0]}


def mek_ismetlodo(mek, min_elem=2):
    """A MEK-oldali gyanús ismétlődés: azok a forrásversek, amelyek MEK-listája (a nem üres célok halmaza, legalább
    `min_elem` elem) szó szerint azonos egy másik forrásvers MEK-listájával. Az egyelemű lista nem számít ismétlődésnek
    (a gyakori, pl. Róm 3:23, természetes egyezés)."""
    csop = collections.defaultdict(list)
    for v, lis in mek.items():
        halmaz = frozenset(c for c, _ in lis if c)
        if len(halmaz) >= min_elem:
            csop[halmaz].append(v)
    return {v for vs in csop.values() if len(vs) > 1 for v in vs}


def cel_vegpontok(cel):
    """A HunKar-cél (egy vers vagy 'A-B' tartomány) két végpontja (kezdet, vég) STEP-tuple-ként; hibás cél -> None."""
    r = cel.split('-')
    k = step_ref(r[0])
    e = step_ref(r[-1]) or k
    return (k, e) if k else None


def kapcsolat(mek_cel, hk_cel):
    """A MEK-cél (STEP-ref) és a HunKar-cél (vers vagy tartomány) viszonya: az `ALTIPUSOK` egyik típusa vagy None.
    tartomány/vershatár: a MEK-cél a HunKar-tartományban vagy annak végpontjától egy versnyire áll (azonos fejezet);
    könyv-/fejezet-/versszám-elírás: a MEK-cél egyetlen összetevőben (könyv / fejezet / vers) tér el valamelyik
    végponttól (az 1 verses eltérés vershatár, a versszám-elírás ennél nagyobb)."""
    m = step_ref(mek_cel)
    v = cel_vegpontok(hk_cel)
    if not m or not v:
        return None
    k, e = v
    if k[0] == m[0] and k <= m <= e:
        return 'tartomány/vershatár'
    for p in (k, e):
        if p[0] == m[0] and p[1] == m[1] and abs(p[2] - m[2]) == 1:
            return 'tartomány/vershatár'
    legjobb = None
    for p in (k, e):
        if p[0] != m[0] and p[1:] == m[1:]:
            t = 'könyv-elírás'
        elif p[0] == m[0] and p[1] != m[1] and p[2] == m[2]:
            t = 'fejezet-elírás'
        elif p[0] == m[0] and p[1] == m[1] and p[2] != m[2]:
            t = 'versszám-elírás'
        else:
            continue
        if legjobb is None or _RANG[t] < _RANG[legjobb]:
            legjobb = t
    return legjobb


def cel_letezik(cel, letezo):
    """Igaz, ha a cél (vers vagy tartomány) minden végpontja létező vers."""
    v = cel_vegpontok(cel)
    return bool(v) and all(ref_str(p) in letezo for p in v)


def jelolt_bontas(javitott, letezo, tamogat_teljes, tamogat_tsk, gyanus_hk, gyanus_mek):
    """A `jelolt` sorok bontása és a J2 szabály döntése soronként.

    javitott: [(igehely, kapcsolodo, szint, forras, indok)] (a teljes tábla). A TSK-támogatás (tamogat_teljes: mai
    `tsk=` szabály; tamogat_tsk: tiszta TSK ±3) csak tájékoztató, a szabály nem használja (l. Karoli_KH_MEK_README.md 7.).
    gyanus_hk / gyanus_mek: a gyanús ismétlődő forrásversek két halmaza (HunKar-oldali jelölés / MEK-oldali ismétlődés).

    A szabály (README 7.): a MEK-oldali jelölt sor `megerositett`, kivéve ha (1) a hivatkozott vers vagy a forrásvers
    nem létezik (`Karoli_1908` ∪ MEK-versszerkezet), vagy (2) a forrásvers gyanús ismétlődő (a két halmaz uniója).
    A HunKar-oldali jelölt sor (a MEK a versen mást listáz) `kiesik`, ha a forrásverse MEK-listájából legalább egy sor
    beemelődik (a MEK-lista a versen irányadó, és a sor abban nincs); különben jelölt marad. Az `egyező, de nem létező
    hivatkozás` sor jelölt marad (nem létező célvers)."""
    csoport = collections.OrderedDict()
    for s in javitott:
        csoport.setdefault(s[0], []).append(s)
    ki = []
    for fv, sorok in csoport.items():
        jel = [s for s in sorok if s[2] == 'jelolt']
        if not jel:
            continue
        mek_sor = [s for s in jel if s[3] == 'MEK']
        hk_sor = [s for s in jel if s[3] == 'HunKar']
        par_mek = {}
        par_hk = {}
        for ms in mek_sor:
            lis = sorted(((_RANG[t], t, hs) for hs in hk_sor for t in [kapcsolat(ms[1], hs[1])] if t),
                         key=lambda x: x[0])
            par_mek[id(ms)] = lis
        for hs in hk_sor:
            lis = sorted(((_RANG[t], t, ms) for ms in mek_sor for t in [kapcsolat(ms[1], hs[1])] if t),
                         key=lambda x: x[0])
            par_hk[id(hs)] = lis
        van_beemel = False
        sv = []
        for s in jel:
            oldal = {'MEK': 'MEK', 'HunKar': 'HunKar'}.get(s[3], 'egyező')
            partner = None
            if oldal == 'egyező':
                alt = 'egyéb (egyező, de nem létező hivatkozás)'
            else:
                lis = (par_mek if oldal == 'MEK' else par_hk)[id(s)]
                if lis:
                    alt, partner = lis[0][1], lis[0][2]
                elif oldal == 'MEK' and not hk_sor:
                    alt = 'csak MEK'
                else:
                    alt = 'eltér (nem sorolható)'
            letezik = cel_letezik(s[1], letezo)
            forras_l = fv in letezo
            sajat = bool(tamogat_teljes(fv, s[1]))
            sajat_t = bool(tamogat_tsk(fv, s[1]))
            ptsk = pt = None
            if partner is not None:
                ptsk = bool(tamogat_teljes(fv, partner[1]))
                pt = bool(tamogat_tsk(fv, partner[1]))
            if oldal == 'egyező':
                kat = 'mindkettő' if sajat else 'egyik sem'
            else:
                mek_t = sajat if oldal == 'MEK' else bool(ptsk)
                hk_t = sajat if oldal == 'HunKar' else bool(ptsk)
                kat = ('mindkettő' if mek_t and hk_t else 'csak a MEK-cél' if mek_t else
                       'csak a HunKar-cél' if hk_t else 'egyik sem')
            gy_hk = fv in gyanus_hk
            gy_mek = fv in gyanus_mek
            dontes = None
            if oldal == 'egyező' or not letezik or not forras_l:
                dontes = D_NEMLETEZO if oldal != 'HunKar' else None
            if oldal == 'MEK':
                if dontes is None:
                    dontes = D_GYANUS if (gy_hk or gy_mek) else D_BEEMEL
                if dontes == D_BEEMEL:
                    van_beemel = True
            sv.append({'forras_vers': fv, 'cel': s[1], 'oldal': oldal, 'indok_kod': s[4].split(';')[0],
                       'altipus': alt, 'partner': partner[1] if partner is not None else None,
                       'sajat_tsk': sajat, 'partner_tsk': ptsk, 'sajat_tsk_tiszta': sajat_t,
                       'partner_tsk_tiszta': pt, 'tsk_kat': kat, 'cel_letezik': letezik, 'forras_letezik': forras_l,
                       'gyanus_hk': gy_hk, 'gyanus_mek': gy_mek, 'dontes': dontes,
                       'mek_alak': (s[4].split('mek_alak=')[1].split(';')[0] if 'mek_alak=' in s[4] else '')})
        for r in sv:
            if r['oldal'] == 'HunKar':
                r['dontes'] = D_HK_KIESIK if van_beemel else D_HK_MARAD
        ki.extend(sv)
    return ki


def jelolt_sulya(javitott, bontas):
    """A jelölt szint súlya: sorok, forrásversek, és hány versnek nem marad megerősített KH-ja a jelölt nélkül."""
    versek = {s[0] for s in javitott}
    meg_versek = {s[0] for s in javitott if s[2] == 'megerositett'}
    jel_versek = {r['forras_vers'] for r in bontas}
    nincs = jel_versek - meg_versek
    jel_kiesik = {s[0] for s in javitott if s[2] == 'kiesik'}
    be_versek = {r['forras_vers'] for r in bontas if r['dontes'] == D_BEEMEL}
    return {'sor_osszes': len(javitott), 'sor_jelolt': len(bontas), 'versek_osszes': len(versek),
            'versek_megerositettel': len(meg_versek), 'versek_jelolttel': len(jel_versek),
            'jelolt_vers_megerositett_nelkul': len(nincs), 'ebbol_kiesik_is': len(nincs & jel_kiesik),
            'ebbol_nincs_mas_sor': len(nincs - jel_kiesik), 'beemel_versek': len(be_versek),
            'beemel_uj_versek': len(nincs & be_versek)}


def mintak(sorok, n=5):
    """Egyenletesen elosztott, determinisztikus minta (a sorok sorrendjéből)."""
    if len(sorok) <= n:
        return list(sorok)
    lep = len(sorok) / n
    return [sorok[int(i * lep)] for i in range(n)]


def beemel(javitott, bontas, ts):
    """A szabály alkalmazása (J4). javitott: [(igehely, kapcsolodo, szint, forras, indok, proveniencia)]; a
    visszaadott lista ugyanilyen, ugyanabban a sorrendben, a sorok száma nem változik. Csak a `jelolt` sorok
    módosulhatnak: a beemelt MEK-sor `megerositett` lesz (indok + `;szabaly=F181`), a HunKar-oldali, MEK-listával
    ütköző sor `kiesik` (indok + `;szabaly=F181`); a többi változatlan. Idempotens (a már módosult sor nem jelolt)."""
    dont = {(r['forras_vers'], r['cel'], r['oldal']): r['dontes'] for r in bontas}
    prov = ('scope=konkordancia/Karoli_KH_javitott.tsv (szint=jelolt) + konkordancia/Karoli_KH_MEK_versszerkezet.tsv + '
            'konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv | forras=eszkozok/karoli_kh_mek.py beemel '
            '| ts=%s' % ts)
    ki = []
    for s in javitott:
        if s[2] != 'jelolt':
            ki.append(list(s))
            continue
        oldal = {'MEK': 'MEK', 'HunKar': 'HunKar'}.get(s[3], 'egyező')
        d = dont.get((s[0], s[1], oldal))
        if d == D_BEEMEL:
            ki.append([s[0], s[1], 'megerositett', s[3], s[4] + ';' + SZABALY_JEL, prov])
        elif d == D_HK_KIESIK:
            ki.append([s[0], s[1], 'kiesik', s[3], s[4] + ';' + SZABALY_JEL, prov])
        else:
            ki.append(list(s))
    return ki


def _db(rs, felt):
    return sum(1 for r in rs if felt(r))


def jelolt_bontas_szoveg(bontas, suly, modell, ts, gy_hk_db, gy_mek_db):
    ki = []
    w = ki.append
    n = len(bontas)
    prov = ('scope=konkordancia/Karoli_KH_javitott.tsv (szint=jelolt) + konkordancia/Karoli_KH_MEK.tsv + '
            'konkordancia/Karoli_kereszthivatkozasok.tsv + konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv + '
            'konkordancia/Karoli_1908.tsv + konkordancia/Karoli_KH_MEK_versszerkezet.tsv + '
            'konkordancia/TSK_kereszthivatkozasok.tsv | forras=eszkozok/karoli_kh_mek.py jelolt-bontas | ts=%s' % ts)
    w('# F181 jelentés — a Károli-KH jelölt szintjének mérése, a beemelési szabály és alkalmazása\n')
    w('*Végrehajtó: `%s`. Ág: `claude/f181-karoli-kh-jeloltek`. %s.*' % (modell, ts))
    w('*%s*\n' % prov)
    w('## 1. A jelölt sorok és az altípusok (J1; mért: %d sor)\n' % n)
    w('| altípus | sor | MEK-oldali | HunKar-oldali | egyező |')
    w('|---|---|---|---|---|')
    sz = collections.Counter((r['altipus'], r['oldal']) for r in bontas)
    for a in ALTIPUSOK:
        m, h, e = sz[(a, 'MEK')], sz[(a, 'HunKar')], sz[(a, 'egyező')]
        w('| %s | %d | %d | %d | %d |' % (a, m + h + e, m, h, e))
    w('| **összesen** | **%d** | %d | %d | %d |\n' % (
        n, sum(v for (a, o), v in sz.items() if o == 'MEK'), sum(v for (a, o), v in sz.items() if o == 'HunKar'),
        sum(v for (a, o), v in sz.items() if o == 'egyező')))
    w('Indok-kódok: ' + ', '.join('`%s` %d' % (k, v) for k, v in sorted(
        collections.Counter(r['indok_kod'] for r in bontas).items())) + '.')
    w('Az altípus a másik oldal **jelölt** soraihoz viszonyít (azonos forrásvers): a MEK-cél és a HunKar-cél egyetlen '
      'összetevőben tér el (könyv-/fejezet-/versszám-elírás), vagy a MEK-cél a HunKar-tartományban / egy versnyire '
      'áll (tartomány/vershatár). `csak MEK`: a forrásversen nincs jelölt HunKar-sor. `eltér (nem sorolható)`: van '
      'másik oldali jelölt sor, de a pár nem áll közel.\n')
    hibas = _db(bontas, lambda r: not r['cel_letezik'] or not r['forras_letezik'])
    w('Nem létező cél vagy forrásvers (`Karoli_1908` ∪ MEK-versszerkezet szerint): **%d** sor.\n' % hibas)

    w('## 2. A szabály (J2) kimenete, soronként\n')
    w('A szabály: a MEK-oldali jelölt sor `megerositett`, **kivéve** (1) a hivatkozott vers vagy a forrásvers nem létezik, '
      '(2) a forrásvers gyanús ismétlődő. A HunKar-oldali jelölt sor `kiesik`, ha a forrásverse MEK-listájából legalább '
      'egy sor beemelődik; különben jelölt marad. A TSK nem szerepel a szabályban.\n')
    w('| döntés | sor |')
    w('|---|---|')
    dk = collections.Counter(r['dontes'] for r in bontas)
    for d in DONTESEK:
        w('| %s | %d |' % (d, dk[d]))
    w('| **összesen** | **%d** |\n' % n)
    mek_db = _db(bontas, lambda r: r['oldal'] == 'MEK')
    w('**A három szám (MEK-oldali jelölt sorok: %d):** bekerül **%d**; gyanús ismétlődésként marad **%d**; a nem létező '
      'célvers miatt marad **%d** (+ %d egyező-de-nem-létező sor, összesen %d nem létező célvers).\n' % (
          mek_db, dk[D_BEEMEL], dk[D_GYANUS],
          _db(bontas, lambda r: r['oldal'] == 'MEK' and r['dontes'] == D_NEMLETEZO),
          _db(bontas, lambda r: r['oldal'] == 'egyező'), dk[D_NEMLETEZO]))
    w('A gyanús ismétlődés két forrása (a MEK-oldali jelölt sorokon): HunKar-oldali jelölés (a #177 gyanús halmaza, '
      '%d forrásvers) %d sor; MEK-oldali ismétlődés (a MEK-lista szó szerint azonos egy másik vers MEK-listájával, ≥2 '
      'elem, %d forrásvers) %d sor; mindkettő %d sor. **Figyelem:** a HunKar-oldali jelölés a *HunKar-lista* '
      'másoltságát jelzi, nem a MEK-listáét; a szabály (a koordinátori előírás szerint) mégis jelöltben tartja ezeket.' % (
          gy_hk_db, _db(bontas, lambda r: r['oldal'] == 'MEK' and r['dontes'] == D_GYANUS and r['gyanus_hk']),
          gy_mek_db, _db(bontas, lambda r: r['oldal'] == 'MEK' and r['dontes'] == D_GYANUS and r['gyanus_mek']),
          _db(bontas, lambda r: r['oldal'] == 'MEK' and r['dontes'] == D_GYANUS and r['gyanus_hk'] and r['gyanus_mek'])))
    w('A **nem létező célvers** és a gyanús ismétlődés átfedése: %d MEK-oldali sor mindkettő; a táblázatban a nem '
      'létező célvers az elsőbbségű.\n' % _db(bontas, lambda r: r['oldal'] == 'MEK' and
                                                 (not r['cel_letezik'] or not r['forras_letezik']) and
                                                 (r['gyanus_hk'] or r['gyanus_mek'])))
    w('**A HunKar-oldali jelölt sor sorsa (mit választottam és miért).** A #177 `eltero_lista` sora: a HunKar-sor, '
      'amelyet a MEK a versen nem listáz, de más hivatkozást igen. Ha a MEK-lista a versen irányadó (a MEK-sor '
      'beemelődik), akkor a HunKar-sor a MEK-lista szerint nincs ott: ugyanaz a helyzet, mint a `kiesik` szinten (a '
      'MEK a versen nem listázza), ezért `kiesik` lesz (indok: `eltero_lista;tsk=…;szabaly=F181`). Ha a verse egyik '
      'MEK-sora sem emelődik be (nem létező cél, gyanús), a HunKar-sor jelölt marad: a verse MEK-listája nincs elfogadva, '
      'tehát a HunKar-sor sorsáról sincs mi alapján dönteni (hiányt nem töltünk ki, CLAUDE.md 3. szabály). A `kiesik` '
      'itt **nem** jelent hibás HunKar-sort: a sor a MEK-lista elfogadásának következménye (l. 4. az elírás-gyanús '
      'párokat). HunKar-oldali jelölt sor: %d; ebből `kiesik`: %d, jelölt marad: %d.\n' % (
          _db(bontas, lambda r: r['oldal'] == 'HunKar'), dk[D_HK_KIESIK], dk[D_HK_MARAD]))

    w('## 3. Keresztábla és könyvenkénti eloszlás\n')
    w('**Altípus × döntés:**\n')
    w('| altípus | ' + ' | '.join(DONTESEK) + ' |')
    w('|---|' + '---|' * len(DONTESEK))
    kt = collections.Counter((r['altipus'], r['dontes']) for r in bontas)
    for a in ALTIPUSOK:
        if any(kt[(a, d)] for d in DONTESEK):
            w('| %s | ' % a + ' | '.join(str(kt[(a, d)]) for d in DONTESEK) + ' |')
    w('')
    w('**TSK-támogatás (csak tájékoztatás, nem szabály-feltétel)** — a mai `tsk=` szabály szerint (TSK ±3 vagy '
      'visszautalás); „tiszta TSK”: csak a TSK ±3. Kategória: melyik oldal célját támogatja (a sor és a párosított '
      'másik oldali sor célja; párosítás nélkül a hiányzó oldal „nem támogatott”).\n')
    w('| altípus | TSK-kategória | cél létezik | cél nem létezik |')
    w('|---|---|---|---|')
    kt2 = collections.Counter((r['altipus'], r['tsk_kat'], r['cel_letezik']) for r in bontas)
    for a in ALTIPUSOK:
        for k in TSK_KATEGORIAK:
            i, nem = kt2[(a, k, True)], kt2[(a, k, False)]
            if i or nem:
                w('| %s | %s | %d | %d |' % (a, k, i, nem))
    w('')
    tisz = _db(bontas, lambda r: r['sajat_tsk_tiszta'])
    teljes = _db(bontas, lambda r: r['sajat_tsk'])
    w('A sor saját céljára mutató TSK-támogatás: mai szabály szerint %d sor, ebből tiszta TSK ±3-mal %d, csak '
      'visszautalással %d.\n' % (teljes, tisz, teljes - tisz))
    w('**Könyvenként (a forrásvers könyve szerint):**\n')
    w('| könyv | jelölt | beemel | gyanús | nem létező | HunKar→kiesik | HunKar marad |')
    w('|---|---|---|---|---|---|---|')
    konyv = collections.OrderedDict()
    for r in bontas:
        konyv.setdefault(r['forras_vers'].split('.')[0], []).append(r)
    for k in step_konyvek():
        rs = konyv.get(k)
        if rs:
            w('| %s | %d | %d | %d | %d | %d | %d |' % (
                k, len(rs), _db(rs, lambda r: r['dontes'] == D_BEEMEL), _db(rs, lambda r: r['dontes'] == D_GYANUS),
                _db(rs, lambda r: r['dontes'] == D_NEMLETEZO), _db(rs, lambda r: r['dontes'] == D_HK_KIESIK),
                _db(rs, lambda r: r['dontes'] == D_HK_MARAD)))
    w('')

    w('## 4. Mire kell figyelni a szabály alkalmazásakor\n')
    elir = [r for r in bontas if r['oldal'] == 'MEK' and r['dontes'] == D_BEEMEL and r['altipus'] in ELIRAS]
    w('* **Elírás-gyanús beemelés:** %d beemelt MEK-sor áll olyan HunKar-sorral párban, amelytől egyetlen összetevőben '
      '(könyv/fejezet/versszám) tér el, és a MEK-cél létezik. Ezekben a MEK-elírás is lehet (pl. 5Móz 21:23 → Gal 2:13 '
      'a Gal 3:13 helyett); a szabály a MEK-et fogadja el (a felhasználó előírása), a HunKar-párja `kiesik` lesz. Bontás: %s. Ez a '
      'szabály tudott ára; a J3 szúrópróba ezt méri.' % (
          len(elir), ', '.join('%s %d' % (a, _db(elir, lambda r: r['altipus'] == a)) for a in ELIRAS)))
    tart = _db(bontas, lambda r: r['oldal'] == 'MEK' and r['dontes'] == D_BEEMEL and r['altipus'] == 'tartomány/vershatár')
    w('* **Tartomány-végpontok:** %d beemelt MEK-sor a HunKar-tartomány végpontja vagy annak szomszédja; a HunKar a '
      'tartományt egy sorban adja, a MEK két végponttal, ezért a beemelt végpontsor és a `kiesik` tartománysor együtt '
      'azonos tartalmat hordozhat (a lap/index oldalán összevonandó).' % tart)
    w('* **A fogyasztók nem látják a MEK-oldali megerősített sort.** A `karoli_kh_szuro.elfogad(forras, cel)` és a hívói '
      '(`lekerdez.py`, `sqlite_epit.py`, `olvaso_pilot/adat.py`, `nav_kinyer.py`) a `Karoli_kereszthivatkozasok.tsv` '
      'sorait szűrik; a csak a MEK-ben álló, most `megerositett` sorok nincsenek abban a táblában, ezért a lapra/'
      'indexbe csak a fogyasztók bővítésével jutnának (N-F177a körébe tartozik; ez a menet nem módosítja őket).\n')

    w('## 5. A jelölt szint súlya\n')
    s = suly
    w('* A tábla sorai: %d; ebből `jelolt`: **%d** (%.1f%%).' % (s['sor_osszes'], s['sor_jelolt'],
                                                              100 * s['sor_jelolt'] / s['sor_osszes']))
    w('* Forrásversek a táblában: %d; legalább egy `megerositett` sora van: %d; legalább egy `jelolt` sora van: '
      '**%d**.' % (s['versek_osszes'], s['versek_megerositettel'], s['versek_jelolttel']))
    w('* **Jelölt nélkül nem marad megerősített KH-ja: %d vers** (a jelölt versek %.1f%%-a); ezek közül %d versnek van '
      '`kiesik` sora is, %d versnek csak jelölt sora van.' % (
          s['jelolt_vers_megerositett_nelkul'],
          100 * s['jelolt_vers_megerositett_nelkul'] / max(1, s['versek_jelolttel']), s['ebbol_kiesik_is'],
          s['ebbol_nincs_mas_sor']))
    w('* A szabály %d forrásversen emel be sort; ebből %d versnek ezzel lesz először megerősített KH-ja (a '
      '`megerositett` szint %d forrásversét %.1f%%-kal bővíti).\n' % (
          s['beemel_versek'], s['beemel_uj_versek'], s['versek_megerositettel'],
          100 * s['beemel_uj_versek'] / max(1, s['versek_megerositettel'])))

    w('## 6. Példák (kategóriánként legfeljebb 8, egyenletes minta a tábla sorrendjéből)\n')
    w('Jelölés: `forrásvers → cél`; partner: a másik oldal párosított sora; TSK: a saját cél '
      '(mai szabály / tiszta; csak tájékoztatás); L: a cél létezik; gy: gyanús (H: HunKar-oldali, M: MEK-oldali).\n')
    for d in DONTESEK:
        rs = [r for r in bontas if r['dontes'] == d]
        if not rs:
            continue
        w('### %s (%d sor)\n' % (d, len(rs)))
        for r in mintak(rs, 8):
            w('* %s → %s %s| %s | altípus: %s | TSK %s/%s | L: %s%s%s' % (
                r['forras_vers'], r['cel'],
                '| partner: %s ' % r['partner'] if r['partner'] else '', r['oldal'], r['altipus'],
                'igen' if r['sajat_tsk'] else 'nem', 'igen' if r['sajat_tsk_tiszta'] else 'nem',
                'igen' if r['cel_letezik'] else 'nem', '' if r['forras_letezik'] else ' | forrásvers nem létezik',
                ' | gy: %s%s' % ('H' if r['gyanus_hk'] else '', 'M' if r['gyanus_mek'] else '')
                if (r['gyanus_hk'] or r['gyanus_mek']) else ''))
        w('')
    return '\n'.join(ki) + '\n'


def _bontas_futtat(be, ts):
    jav = [m[:6] for m in tsv_sorok(be) if len(m) >= 6]
    return (jav,) + _bontas_sorokra(jav)


def _bontas_sorokra(jav):
    letezo = karoli_versek()
    import karoli_kh_epseg as E
    _, tsk = E.betolt()
    teljes = tamogato()
    mek = mek_sorok_betolt()
    gy_hk = gyanus_versek()
    gy_mek = mek_ismetlodo(mek)
    bontas = jelolt_bontas([m[:5] for m in jav], letezo, teljes, lambda f, c: bool(c) and E.tamogatott(f, c, {}, tsk),
                           gy_hk, gy_mek)
    return bontas, gy_hk, gy_mek


def jelolt_bontas_main(a):
    ts = a.ts or os.environ.get('PARDES_DATUM', '2026-11-09')
    jav, bontas, gy_hk, gy_mek = _bontas_futtat(a.be, ts)
    suly = jelolt_sulya([m[:5] for m in jav], bontas)
    szoveg = jelolt_bontas_szoveg(bontas, suly, a.modell, ts, len(gy_hk), len(gy_mek))
    print(szoveg)
    if a.jelentes:
        with open(a.jelentes, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
    return 0


def beemel_main(a):
    """A szabály alkalmazása a táblán (J4): a sorok száma nem változik; a Δ-napló a kimeneten."""
    ts = a.ts or os.environ.get('PARDES_DATUM', '2026-11-09')
    jav, bontas, _, _ = _bontas_futtat(a.be, ts)
    uj = beemel(jav, bontas, ts)
    assert len(uj) == len(jav)
    elo = collections.Counter(s[2] for s in jav)
    utan = collections.Counter(s[2] for s in uj)
    valt = collections.Counter((j[2], u[2]) for j, u in zip(jav, uj) if j[2] != u[2])
    fej = FEJ_BEEMELT
    tsv_ir(a.ki or a.be, ['igehely', 'kapcsolodo', 'szint', 'forras', 'indok', 'proveniencia'], uj, fej)
    szoveg = ['sorok: %d -> %d' % (len(jav), len(uj))]
    for k in SZINTEK:
        szoveg.append('%s: %d -> %d (Δ %+d)' % (k, elo[k], utan[k], utan[k] - elo[k]))
    for (x, y), v in sorted(valt.items()):
        szoveg.append('átment %s -> %s: %d' % (x, y, v))
    print('\n'.join(szoveg))
    return 0


# ----------------------------------------------------------------------------------------------------------------
# szuroproba (F181, J3): rétegzett (könyvenkénti, arányos) szúrópróba-minta a döntés nélküli maradékból és a
# beemelt sorokból (kontroll). Csak mintát vesz és kiírja a két vers szövegét; az ítéletet nem adja (az emberi/
# végrehajtói olvasás, a jelentésben).
# ----------------------------------------------------------------------------------------------------------------

def karoli_szoveg():
    """{STEP-kulcs: Károli-vers szövege} a Karoli_1908.tsv-ből."""
    norm = dict(hu_step())
    norm.update(aliasok('karoli_1908'))
    ki = {}
    for m in tsv_sorok(KAROLI):
        r = re.match(r'(\S+) (\d+):(\d+)$', m[0])
        if r and r.group(1) in norm and len(m) > 1:
            ki['%s.%s.%s' % (norm[r.group(1)], r.group(2), r.group(3))] = m[1]
    return ki


def retegzett_minta(sorok, kulcs, n, mag):
    """Könyvenkénti arányos (legnagyobb maradék) minta: a `kulcs(sor)` a könyv; a mag rögzített, ezért ismételhető.
    Visszaadja (minta, {könyv: (populáció, mintaszám)})."""
    import random
    rnd = random.Random(mag)
    csop = collections.OrderedDict()
    for k in step_konyvek():
        csop[k] = []
    for r in sorok:
        csop.setdefault(kulcs(r), []).append(r)
    ossz = sum(len(v) for v in csop.values())
    n = min(n, ossz)
    alap = {k: (len(v) * n) // ossz for k, v in csop.items()}
    maradek = sorted(csop, key=lambda k: -((len(csop[k]) * n) % ossz))
    for k in maradek[:n - sum(alap.values())]:
        alap[k] += 1
    minta = []
    for k, v in csop.items():
        if alap[k]:
            minta.extend(rnd.sample(v, alap[k]))
    return minta, {k: (len(v), alap[k]) for k, v in csop.items() if v}


def szuroproba_main(a):
    ts = a.ts or os.environ.get('PARDES_DATUM', '2026-11-09')
    jav = [m[:6] for m in tsv_sorok(a.be) if len(m) >= 6]
    bontas, _, _ = _bontas_sorokra(jav)
    szov = karoli_szoveg()
    kon = lambda fv: fv.split('.')[0]  # noqa: E731
    sorok = []
    gy = [r for r in bontas if r['dontes'] == D_GYANUS]
    hkm = [r for r in bontas if r['dontes'] == D_HK_MARAD]
    kontroll = [m for m in jav if m[2] == 'megerositett' and m[3] == 'MEK' and SZABALY_JEL in m[4]]
    m1, e1 = retegzett_minta(gy, lambda r: kon(r['forras_vers']), a.maradek, a.mag)
    m3, e3 = retegzett_minta(kontroll, lambda r: kon(r[0]), a.kontroll, a.mag)
    for r in m1:
        sorok.append(('maradék: gyanús ismétlődő', r['forras_vers'], r['cel'], r['mek_alak'], r['oldal']))
    for r in hkm:
        sorok.append(('maradék: HunKar-sor jelölt marad (mind)', r['forras_vers'], r['cel'], '', r['oldal']))
    for r in m3:
        sorok.append(('kontroll: beemelt MEK-sor', r[0], r[1], (r[4].split('mek_alak=')[1].split(';')[0]
                                                                if 'mek_alak=' in r[4] else ''), 'MEK'))
    ki = ['ts=%s | mag=%d | maradék-gyanús: %d sor -> %d minta; HunKar-marad: %d (mind); kontroll: %d beemelt -> %d minta' % (
        ts, a.mag, len(gy), len(m1), len(hkm), len(kontroll), len(m3))]
    ki.append('allokáció (gyanús, könyv: populáció/minta): ' + ', '.join('%s %d/%d' % (k, v[0], v[1]) for k, v in e1.items()))
    ki.append('allokáció (kontroll, könyv: populáció/minta): ' + ', '.join('%s %d/%d' % (k, v[0], v[1]) for k, v in e3.items()))
    for i, (ret, fv, cel, al, oldal) in enumerate(sorok, 1):
        c0 = cel.split('-')[0]
        ki.append('#%d [%s] %s -> %s %s' % (i, ret, fv, cel, '[%s]' % al if al else ''))
        ki.append('   F: ' + szov.get(fv, '(nincs Károli-szöveg)')[:a.hossz])
        ki.append('   C: ' + szov.get(c0, '(nincs Károli-szöveg)')[:a.hossz])
    szoveg = '\n'.join(ki) + '\n'
    if a.ki:
        with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
    print(szoveg)
    return 0


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
    o.add_argument('--nyers', action='store_true', help='a #177 háromszintű nyers állapota, a beemelési szabály nélkül')
    j = sp.add_parser('jelolt-bontas', help='a jelolt szint mérése és bontása (F181, J1); nem módosítja a táblát')
    j.add_argument('--be', default=os.path.join(GYOKER, JAVITOTT))
    j.add_argument('--jelentes')
    j.add_argument('--modell', default='?')
    j.add_argument('--ts')
    b = sp.add_parser('beemel', help='a beemelési szabály alkalmazása a táblán (F181, J4)')
    b.add_argument('--be', default=os.path.join(GYOKER, JAVITOTT))
    b.add_argument('--ki')
    b.add_argument('--ts')
    z = sp.add_parser('szuroproba', help='rétegzett szúrópróba-minta a maradékból és a beemeltekből (F181, J3)')
    z.add_argument('--be', default=os.path.join(GYOKER, JAVITOTT))
    z.add_argument('--ki')
    z.add_argument('--maradek', type=int, default=30)
    z.add_argument('--kontroll', type=int, default=40)
    z.add_argument('--mag', type=int, default=181)
    z.add_argument('--hossz', type=int, default=140)
    z.add_argument('--ts')
    a = ap.parse_args()
    if a.parancs == 'szuroproba':
        return szuroproba_main(a)
    if a.parancs == 'jelolt-bontas':
        return jelolt_bontas_main(a)
    if a.parancs == 'beemel':
        return beemel_main(a)
    return kivonat_main(a) if a.parancs == 'kivonat' else osszevet_main(a)


if __name__ == '__main__':
    sys.exit(main())
