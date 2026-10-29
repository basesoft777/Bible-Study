#!/usr/bin/env python
"""A kész magyar BDB-fordítás illesztése a szakasztáblához (F107, 7. lépés; DT-F107c (d) után).

Bemenet: adat/bdb_szakaszok.tsv (a szakaszok, a `jel` fejekkel), adat/forditasok.tsv (csak olvasva: a BDB-sorok Strongonként a
közös összefűzőn át, `szakasz_bemenet.strong_magyar_sorok`; F128, DT-F128g (a)), eszkozok/forditas_kapuk.py (a magyar oldali jelölő- és törzsnév-felismerés, csak importálva).
Kimenet: adat/bdb_szakasz_hu.tsv (séma: adat/SEMA.md „bdb_szakasz_hu.tsv”). Az adat/forditasok.tsv nem íródik.

Illesztés Strongonként:
  1. a forrás jelölői: a szakasztábla sorainak `jel`-tokenjei — szám, betű, római, zárójeles (a tagolás-kapu jelei), és a törzsnév
     (`T:<az első 4 betű>`, a kapu `torzs_sorozat`-ának alakjában); a magyar oldal jelölői pozícióval (`jelolok_pozicioval`, a
     `TORZS_MINTA` a rag-szabállyal);
  2. mohó, sorrendtartó illesztés: a forrás minden jelölőjét a magyarban a kurzortól keresem; ha nincs meg, a jelölő kimarad (a kurzor
     nem mozdul) — a sor `illeszkedik`, ha a sor összes jelölője megvan;
  3. horgony (a jelölő nem illeszkedett): a sor `szoveg`-ének első fejezet:verse (`\\d+:\\d+`) a magyarban az előző és a következő
     illesztett horgony között — a sor `horgonnyal`; különben `elakad`;
  4. a magyar szakasz a sor horgonyától a következő horgonyig tart; a jelölő nélküli sor (fej utáni bekezdés, cím, fej, alcímszó)
     `jelolo_nelkul`: a szövege az előző szakaszban van (`szoveg_hu` üres), a cím és a fej a magyar szöveg elejét kapja.

A Strong-szintű mérés a kiinduló számhoz (355 / 89 / 230, 2026-10-16, `manual`) a kapu szigorú illesztőjével (`_illeszt`, az első nem
talált kötelező jelölőnél megáll) a tábla jelölősorozatán: `illeszkedik` / `tagolatlan` (nincs jelölő) / `elakad`; és a horgonnyal
kiegészítve: `illeszkedik` / `horgonnyal` (minden jelölős sor illeszkedik vagy horgonnyal) / `elakad` / `tagolatlan`.

  (alap) írás · --meres csak számok · --ellenoriz bájtos összevetés · --ts NAP
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import datetime
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(os.path.dirname(ITT))
sys.path.insert(0, ITT)
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import bont  # noqa: E402
import forditas_kapuk as kapu  # noqa: E402

TABLA = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')
FORD = os.path.join(GYOKER, 'adat', 'forditasok.tsv')
KI_UT = os.path.join(GYOKER, 'adat', 'bdb_szakasz_hu.tsv')
FEJLEC = ['strong', 'sorszam', 'bdb_id', 'szakasz', 'resz', 'utvonal', 'jel', 'kategoria', 'horgony', 'hu_kezdet', 'hu_hossz',
          'szoveg_hu', 'forditas_forras_hash', 'proveniencia']
REF = re.compile(r'\d+:\d+')


def sha256_bajtok(darabok):
    """Sorvég-független SHA-256 (F128.21, ELLENOR_F128 1.): a `kod_hash` konvenciója szerint \\r\\n → \\n, így a CRLF- és az
    LF-checkout ugyanazt a hash-t adja. A darabhatáron kettévágott \\r\\n-t a visszatartott záró \\r kezeli."""
    h = hashlib.sha256()
    maradek = b''
    for b in darabok:
        b = maradek + b
        if b.endswith(b'\r'):
            b, maradek = b[:-1], b'\r'
        else:
            maradek = b''
        h.update(b.replace(b'\r\n', b'\n'))
    h.update(maradek)
    return h.hexdigest()


def sha256_fajl(ut):
    with open(ut, 'rb') as f:
        return sha256_bajtok(iter(lambda: f.read(1 << 20), b''))


def kod_hash():
    with open(os.path.abspath(__file__), 'rb') as f:
        return hashlib.sha256(f.read().replace(b'\r\n', b'\n')).hexdigest()


# ---------------------------------------------------------------- DT-F107b (d), felhasználó, 2026-10-18: a magyar jelölő-felismerés
# bővítése (a kapu regexei érintetlenek — a forditas_kapuk.py nincs a brief `ir` mezőjében —, a bővítés itt, az illesztőben):
#  (1) törzsnév MINDKÉT oldalon a bontó törzslistájából (a szeletelőével azonos), a forrás alakjában (` ' ʿ ‘ ’), a magyaros alakokkal
#      (Nifal, Hifil, Hofal, Hitpael) és a magyar raggal (kötőjellel is): a kapu `Hithp(?:a(?:el|...))?` mintája a „Hithpa`el”-t nem fogja,
#      az arámi törzseket (Pe`al, Pa`el, Haph`el, Aph`el …) egyáltalán nem; kulcs: a kanonikus név (`Hithpa'el`);
#  (2) betű j-től: csak tagolásjel után („. ”, „; ”, „: ”, „— ”, „) ” vagy a szöveg elején), mert szövegközben rövidítés („l. ott”,
#      „vö.”); a „k.” szám után nem jelölő („632 k.” = és a következő);
#  (3) a kérdőjel utáni szám („+? 1 Gerár”, H0040).
_APO = "[`'ʿ‘’]"
_MAGYAROS = {'Nifal': "Niph'al", 'Hifil': "Hiph'il", 'Hofal': "Hoph'al", 'Hitpael': "Hithpa'el"}
_TORZS_NEVEK = sorted(set(bont.TORZS.split('|')), key=len, reverse=True)
_RAG = sorted(set(kapu._TORZS_RAG_HOSSZU + kapu._TORZS_RAG_ROVID), key=len, reverse=True)
TORZS_HU = re.compile(
    r'(?<![A-Za-zÀ-ž])(' + '|'.join(re.escape(n).replace('`', _APO) for n in _TORZS_NEVEK) + '|' + '|'.join(_MAGYAROS) + r')'
    r'(?:-?(?:' + '|'.join(_RAG) + r'))?(?![A-Za-zÀ-ž])')
BETU_J = re.compile(r'(?:(?<=^)|(?<=[.;:—)] ))([j-z])\.(?=\s)')
KERDO_SZAM = re.compile(r'(?<=\? )(\d{1,2})(?= [^\W\d_])')
#  (4) a kötetszámos siglum (`^` + kis római szám + pont: „Kö^ii.”, „Bö^ii.”) utáni jel a kötet lapszáma, nem jelölő
#      („Kö^ii. 1. 104”, H8034; ISTENTISZT-001 arany lap, 2026-10-29): a forrásoldalon nem félkövér, a magyarban viszont a kapu
#      számjelnek veszi. Csak ez az alak: a szerzői siglum után („Che^Hpt. 2 nyomorúságban”, „So^Kau. 2”, „Dr^Sm. b.”) és a záró
#      zárójel után („RS^149). 5”) a jel valódi jelölő lehet (naplok/ISTENTISZT001_siglum_hatas.py).
SIGLUM_ELOTT = re.compile(r'\^[ivx]+\.\s?$')


def torzs_kulcs(nev):
    """A törzsnév kanonikus kulcsa (a forrás és a magyar oldalon azonos): `Hithpa'el`, `Qal`, `Pe'al`."""
    nev = re.sub(_APO, "'", nev)
    if nev in _MAGYAROS:
        return _MAGYAROS[nev]
    return bont.TORZS_KANON.get(nev.replace("'", '`'), nev)


def forras_jelolok(jel):
    """A sor `jel`-ének illeszthető jelölői, sorrendben: '1', 'a', 'II', '(1)', 'T:Qal'."""
    if not jel:
        return []
    tok, _ = bont.fej_bont('<b>' + jel + '</b>')
    ki = []
    for sz, v in tok:
        if sz == 'szam':
            ki.append(v.rstrip('.'))
        elif sz == 'betu':
            ki.append(v.rstrip('.'))
        elif sz == 'romai':
            ki.append(v.rstrip('.'))
        elif sz == 'zaro':
            ki.append(v)
        elif sz == 'torzs':
            ki.append('T:' + torzs_kulcs(v.rstrip('.')))
    return ki


def magyar_jelolok(hu):
    """A magyar szöveg jelölői pozícióval (a tagolás-kapu jelei + a törzsnevek)."""
    ki = list(kapu.jelolok_pozicioval(hu, False))
    for m in TORZS_HU.finditer(hu):
        ki.append((m.start(), 'T:' + torzs_kulcs(m.group(1))))
    for m in BETU_J.finditer(hu):
        if m.group(1) == 'k' and re.search(r'\d\s?$', hu[max(0, m.start() - 3):m.start()]):
            continue
        ki.append((m.start(), m.group(1)))
    for m in KERDO_SZAM.finditer(hu):
        ki.append((m.start(), m.group(1)))
    ki = [(p, j) for p, j in ki if j.startswith('T:') or not SIGLUM_ELOTT.search(hu[max(0, p - 12):p])]
    return sorted(set(ki))


def forditasok(ut=None):
    """{Strong: {'forditas_hu', 'forras_hash'}} a BDB-sorokból, a közös összefűzőn át (F128, DT-F128a (a), DT-F128g (a):
    `szakasz_bemenet.strong_magyar_sorok`): a szakaszonként fordított Strong szövege a `sz<sorszam>` sorok összefűzése, a
    `forras_hash` ilyenkor a token nélküli forrásnézet (`szakasz_bemenet.nezet`) SHA-1-e; különben a `teljes` sor és a saját
    `forras_hash`-e (a jóváhagyott `kezi` sor elsőbbségével, DT-F128f (3))."""
    import szakasz_bemenet as sb
    with open(ut or FORD, encoding='utf-8', newline='') as f:
        sorok = [s.rstrip('\r') for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    strongonkent = collections.OrderedDict()
    for s in sorok[1:]:
        d = dict(zip(fej, s.split('\t')))
        if d['szotar'] == 'BDB':
            strongonkent.setdefault('H%04d' % int(re.sub(r'\D', '', d['strong'])), []).append(d)
    ki = {}
    for st, ds in strongonkent.items():
        szoveg, tipus, hasznalt = sb.strong_magyar_sorok(ds)
        if not szoveg:
            continue
        if tipus == 'szakasz':
            szak = sb.szakaszok(st)
            h = sb.sha1(sb.nezet(szak)) if szak else ''
        else:
            h = hasznalt[0].get('forras_hash', '')
        ki[st] = {'forditas_hu': szoveg, 'forras_hash': h}
    return ki


def strong_illeszt(sorok, hu):
    """Soronként (kategória, horgony, hu_kezdet) és a Strong-szintű szigorú / horgonyos kategória."""
    mj = magyar_jelolok(hu)
    kurzor = 0
    eredmeny = []
    for x in sorok:
        jelek = forras_jelolok(x['jel']) if x['jelolo'] in ('point', 'section', 'remarks') else []
        if not jelek:
            eredmeny.append(['jelolo_nelkul', '', None])
            continue
        poz, k = [], kurzor
        for j in jelek:
            hol = next((i for i in range(k, len(mj)) if mj[i][1] == j), None)
            if hol is None:
                poz = None
                break
            poz.append(mj[hol][0])
            k = hol + 1
        if poz:
            eredmeny.append(['illeszkedik', ' '.join(jelek), poz[0]])
            kurzor = k
        else:
            eredmeny.append(['elakad', ' '.join(jelek), None])
    # horgony a nem illesztett jelölős sorokra: az első fejezet:vers az előző és a következő illesztett pozíció között
    for i, (x, e) in enumerate(zip(sorok, eredmeny)):
        if e[0] != 'elakad':
            continue
        also = max([r[2] for r in eredmeny[:i] if r[2] is not None] or [0])
        felso = min([r[2] for r in eredmeny[i + 1:] if r[2] is not None and r[0] == 'illeszkedik'] or [len(hu)])
        m = REF.search(x['szoveg'])
        if not m:
            continue
        p = hu.find(m.group(0), also + 1 if also else 0)
        if 0 <= p < felso and p > also:
            # a szakasz kezdete: a sor saját jelölőjének utolsó előfordulása az előző szakasz és a horgony között (a kapu
            # regexe nem minden helyzetben ismeri fel, pl. „+? 1 Gerár”, H0040); ha nincs, a mondat- vagy tagolásjel után
            jel0 = next((j for j in forras_jelolok(x['jel']) if not j.startswith('T:')), None)
            eleje = None
            if jel0:
                talalat = [t.start() for t in re.finditer(r'(?<!\S)' + re.escape(jel0) + r'\.?(?=\s)', hu[also:p])]
                if talalat:
                    eleje = also + talalat[-1]
            if eleje is None:
                hatar = max(hu.rfind('. ', also, p), hu.rfind('; ', also, p), hu.rfind('— ', also, p))
                eleje = (hatar + 2) if hatar > also else p
            e[:] = ['horgonnyal', m.group(0), eleje]
    # Strong-szint, szigorú (a kapu _illeszt-je a tábla jelölősorozatán, törzsnév nélkül, mint a kiinduló mérés)
    a = [j for x in sorok if x['jelolo'] in ('point', 'section', 'remarks')
         for j in forras_jelolok(x['jel']) if not j.startswith('T:')]
    b = kapu.tagolas_sorozat_forditas(hu)
    if not a:
        szigoru = 'tagolatlan'
    else:
        _, hiba = kapu._illeszt(a, b)
        szigoru = 'illeszkedik' if hiba is None else 'elakad'
    kat = [e[0] for e in eredmeny if e[0] != 'jelolo_nelkul']
    if not kat:
        horgonyos = 'tagolatlan'
    elif all(k == 'illeszkedik' for k in kat):
        horgonyos = 'illeszkedik'
    elif all(k in ('illeszkedik', 'horgonnyal') for k in kat):
        horgonyos = 'horgonnyal'
    else:
        horgonyos = 'elakad'
    return eredmeny, szigoru, horgonyos


def general(ts):
    tab = collections.OrderedDict()
    with open(TABLA, encoding='utf-8', newline='') as f:
        s = f.read().split('\n')
    fej = s[2].split('\t')
    for x in s[3:]:
        if x:
            d = dict(zip(fej, x.split('\t')))
            tab.setdefault(d['strong'], []).append(d)
    ford = forditasok()
    ki, stat, sor_stat = [], collections.Counter(), collections.Counter()
    nincs = []
    for st in sorted(ford):
        if st not in tab:
            nincs.append(st)
            continue
        sorok, hu = tab[st], ford[st]['forditas_hu']
        eredmeny, szigoru, horgonyos = strong_illeszt(sorok, hu)
        stat[('szigoru', szigoru)] += 1
        stat[('horgonyos', horgonyos)] += 1
        poziciok = sorted(set([0] + [e[2] for e in eredmeny if e[2] is not None]))
        for x, e in zip(sorok, eredmeny):
            kat, horgony, p = e
            if x['sorszam'] in ('1', '2') and kat == 'jelolo_nelkul' and x['utvonal'] in ('cim', 'fej'):
                p = 0 if x['sorszam'] == '1' or x['utvonal'] == 'fej' else None
            if x['sorszam'] == '1':
                p = None                               # a cím: a magyar szövegben nincs külön része
            if x['sorszam'] == '2' and p is None and x['utvonal'] == 'fej':
                p = 0
            if p is not None:
                kov = next((q for q in poziciok if q > p), len(hu))
                szoveg_hu = hu[p:kov].strip()
            else:
                szoveg_hu = ''
            sor_stat[kat] += 1
            ki.append([st, x['sorszam'], x['bdb_id'], x.get('szakasz', ''), x['resz'], x['utvonal'], x['jel'], kat, horgony,
                       '' if p is None else str(p), '' if p is None else str(len(szoveg_hu)),
                       szoveg_hu.replace('\t', ' ').replace('\n', ' '), ford[st]['forras_hash'],
                       'scope=%s | forras=bdb_jelolt/hu_illeszt.py (fejléc) | ts=%s' % (st, ts)])
    return ki, stat, sor_stat, nincs, len(ford)


def fajl_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/bdb_jelolt/hu_illeszt.py --ts %s — kézzel nem szerkesztendő (F107, 7. lépés; séma: adat/SEMA.md, bdb_szakasz_hu.tsv).' % ts,
           '# forras: adat/bdb_szakaszok.tsv@%s + adat/forditasok.tsv@%s (csak olvasva) + eszkozok/forditas_kapuk.py@%s + kód@%s'
           % (sha256_fajl(TABLA)[:12], sha256_fajl(FORD)[:12],
              sha256_fajl(os.path.join(GYOKER, 'eszkozok', 'forditas_kapuk.py'))[:12], kod_hash()[:12]),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(s) for s in sorok]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    ap.add_argument('--meres', action='store_true')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    sorok, stat, sor_stat, nincs, n = general(a.ts)
    print('Strong (fordítással): %d; a táblában nincs: %d %s' % (n, len(nincs), nincs))
    print('Strong-szint, szigorú (_illeszt, mint a kiinduló 355/89/230): %s' % {k[1]: v for k, v in stat.items() if k[0] == 'szigoru'})
    print('Strong-szint, horgonnyal: %s' % {k[1]: v for k, v in stat.items() if k[0] == 'horgonyos'})
    print('sor: %d; %s' % (len(sorok), dict(sor_stat)))
    if a.meres:
        return 0
    szoveg = fajl_szoveg(sorok, a.ts)
    if a.ellenoriz:
        with open(KI_UT, encoding='utf-8', newline='') as f:
            if f.read() != szoveg:
                print('ELTÉR: %s' % KI_UT)
                return 1
        print('azonos: %s' % KI_UT)
        return 0
    with open(KI_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('írva: %s' % KI_UT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
