#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V — emberi validációs minta a Károli 1908 – Strong szópárosításhoz.

Két kimenet a `kozlemeny/data_paper/validacio/` alatt:
  * minta.tsv      — 300 szópár + 80 pár nélküli magyar szó, rétegzett véletlen minta;
  * ellenorzo.html — önálló, offline ellenőrző oldal, a mintával beágyazva
                     (a sablon: eszkozok/karoli_strong_validacio_sablon.html).

Mintavétel (rögzített mag; újrafuttatva ugyanazon a commiton bájtra azonos, a minta.tsv fejlécének git-hashe a commitot követi):
  * Párok: a #172 gépi mérés rétegzett mintájából (`f172/minta.tsv`, rétegenként
    200 véletlen pársor a teljes keretből) vett véletlen részminta, a keret
    pársúlya szerint arányosan (`f172/keret.tsv`, legnagyobb maradék). Egy egyszerű
    véletlen minta véletlen részmintája maga is egyszerű véletlen minta a rétegből,
    ezért a 300 pár a teljes keret (598 715 pár) arányosan rétegzett mintája; a
    hozadék, hogy a vak Opus-ellenőr ítélete (`f172/itelet_par.tsv`) erre a 300
    párra már megvan. A #172 nyolc rétegéből a két Mózes-réteg a közleményben
    egy könyvcsoport (`f172/reteg_osszevont.tsv`): hét könyvcsoport.
  * Pár nélküli magyar szavak: a `adat/karoli_strong/szavak_*.tsv` `hu` oldalának
    `betoldas` állapotú szavai (a `fuggoben` nem: az kézi, nem gépi döntés),
    könyvcsoportonként a betoldás-szám arányában, 80 darab.
Előtte ellenőrzi, hogy minden mintapár a mai `parok_*.tsv`-ben és a mai
bemenetben (Károli-token, TAHOT/TAGNT-token) is ugyanaz.

Tételenként: igehely, a teljes Károli-vers, a kiemelt szó és pozíciója
(sorszám + karakterhatár), a teljes eredeti vers (TAHOT/TAGNT, Károli-kulcson,
a párosítás bemenetével azonos sorszámozással), a forrásszó, Strong-szám,
szótő, rövid jelentés (TAHOT/TAGNT), alaktani kód és szófaj (Macula, CC BY 4.0;
illesztés versen belül Strong-számmal vagy mássalhangzó-vázzal; illesztés
nélkül üres), és a vers többi párja.

Olvasás split('\\t'), írás '\\t'.join() (a csv modul tilos, CLAUDE.md).
Az `adat/karoli_strong/` és a `konkordancia/` csak olvasott.

Használat (a repó gyökeréből):
    python eszkozok/karoli_strong_validacio_minta.py
    python eszkozok/karoli_strong_validacio_minta.py --csak-html   # a meglévő minta.tsv-ből
"""

import argparse
import json
import os
import random
import re
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'karoli_strong'))
import bemenet  # noqa: E402
import pontossag_minta as pm  # noqa: E402
import tokenek  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_strong_morf as morf  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = pm.GYOKER
KONK = os.path.join(GYOKER, 'konkordancia')
ADAT = pm.ADAT
KIMENET = os.path.join(GYOKER, 'kozlemeny', 'data_paper', 'validacio')
SABLON = os.path.join(GYOKER, 'eszkozok', 'karoli_strong_validacio_sablon.html')
MAG = 20261116
N_PAR = 300
N_NELKUL = 80

# a #172 nyolc rétege -> a közlemény hét könyvcsoportja
CSOPORTOK = ['OSZ_mozes', 'OSZ_tortenet', 'OSZ_koltoi', 'OSZ_profeta',
             'USZ_evangelium', 'USZ_level', 'USZ_jelenesek']


def csoport_of_reteg(rt):
    return 'OSZ_mozes' if rt.startswith('OSZ_mozes') else rt


MINTA_FEJ = ['tetel_id', 'tipus', 'csoport', 'f172_reteg', 'f172_id', 'konyv', 'vers',
             'hu_vers', 'hu_sorszam', 'hu_szo', 'hu_kezdet', 'hu_veg',
             'er_nyelv', 'er_vers', 'er_sorszam', 'er_szo', 'strong', 'szoto', 'jelentes',
             'tukor', 'kiejtes', 'morf', 'szofaj', 'morf_hu', 'nem_tr', 'tobbi_par', 'er_tokenek_json', 'parok_json']


# ---------------------------------------------------------------- segédek

def _tabla(ut):
    return pm._tabla(ut)


def legnagyobb_maradek(sulyok, n):
    """{kulcs: súly} -> {kulcs: darab}, összeg = n (Hamilton-módszer; döntetlennél a kulcs sorrendje)."""
    ossz = float(sum(sulyok.values()))
    nyers = {k: n * v / ossz for k, v in sulyok.items()}
    ki = {k: int(x) for k, x in nyers.items()}
    marad = n - sum(ki.values())
    sorrend = sorted(sulyok, key=lambda k: (-(nyers[k] - ki[k]), list(sulyok).index(k)))
    for k in sorrend[:marad]:
        ki[k] += 1
    return ki


def git_head():
    return pm.git_head()


_HEB_JEL = re.compile('[֑-ׇ׳״‍‌͏]')


def vaz(s):
    """Héber mássalhangzó-váz / görög ékezet nélküli kisbetűs alak az illesztéshez."""
    s = _HEB_JEL.sub('', s)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = ''.join(c for c in s if c.isalpha())
    # héber végbetűk egységesítése
    s = s.translate(str.maketrans('ךםןףץ', 'כמנפצ'))
    return s.casefold()


# ---------------------------------------------------------------- források

def lex_tabla():
    """(strong, ragozott alak) -> (szótő, rövid jelentés, kiejtés), és strong -> ugyanez (tartalék)."""
    pontos, strongra = {}, {}
    for ut in (tokenek.TAHOT, tokenek.TAGNT):
        for r in tokenek._sorok(ut):
            if len(r) < 7:
                continue
            ertek = (r[4], r[5], r[3])
            pontos.setdefault((r[1], r[2]), ertek)
            strongra.setdefault(r[1], ertek)
    return pontos, strongra


def macula_versek(kell):
    """Károli-vers -> [(strong, váz, morf, szófaj, szó-azonosító)] a Macula-táblákból, csak a kért versekre.
    Görögben az N1904 és az SBLGNT sorai külön listán (kulcs: (vers, kiadás))."""
    ki = {}
    fajlok = sorted(f for f in os.listdir(KONK) if f.startswith('Macula_heber_') and f.endswith('.tsv'))
    for fn in fajlok:
        fej = None
        with open(os.path.join(KONK, fn), encoding='utf-8') as f:
            for sor in f:
                sor = sor.rstrip('\n').rstrip('\r')
                if not sor or sor.startswith('#'):
                    continue
                m = sor.split('\t')
                if fej is None:
                    fej = {k: i for i, k in enumerate(m)}
                    continue
                for v in m[fej['karoli']].split(';'):
                    v = v.strip()
                    if v in kell:
                        ki.setdefault((v, 'heb'), []).append(
                            (m[fej['strong']], vaz(m[fej['szo']]), m[fej['morf']], m[fej['szofaj']],
                             m[fej['ref']]))
    fej = None
    with open(os.path.join(KONK, 'Macula_gorog.tsv'), encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if not sor or sor.startswith('#'):
                continue
            m = sor.split('\t')
            if fej is None:
                fej = {k: i for i, k in enumerate(m)}
                continue
            v = m[fej['karoli']].strip()
            if v in kell:
                ki.setdefault((v, m[fej['kiadas']]), []).append(
                    (m[fej['strong']], vaz(m[fej['szo']]), m[fej['morf']], m[fej['szofaj']], m[fej['ref']]))
    return ki


def illeszt(er_lista, mac_lista, ablak=6):
    """Mohó illesztés versen belül: a TAHOT/TAGNT-token a Macula-sorhoz, ha a Strong-szám vagy a váz egyezik.
    Visszaad: {sorsz: (morf, szófaj, szó-azonosító)}."""
    ki = {}
    j = 0
    for w in er_lista:
        v = vaz(w['alak'])
        for k in range(j, min(j + ablak, len(mac_lista))):
            st, mv, morf, szf, ref = mac_lista[k]
            if (st and st == w['strong']) or (v and mv == v):
                ki[w['sorsz']] = (morf, szf, ref)
                j = k + 1
                break
    return ki


# ---------------------------------------------------------------- minta

def parok_versenkent(versek):
    """vers -> [(hu_sorszam, hu_szo, er_sorszam, er_szo, strong)] a mai parok_*.tsv-ből."""
    konyvek = {}
    for v in versek:
        konyvek.setdefault(_fajlkonyv(v), set()).add(v)
    ki = {}
    for k, vs in konyvek.items():
        _, sorok = _tabla(os.path.join(ADAT, 'parok_%s.tsv' % k))
        for r in sorok:
            if r['vers'] in vs:
                ki.setdefault(r['vers'], []).append(
                    (int(r['hu_sorszam']), r['hu_szo'], int(r['er_sorszam']), r['er_szo'], r['strong']))
    return ki


_FAJLKONYV = {}


def _fajlkonyv(vers):
    """'1Móz 3:16' -> '1Moz' (a parok_/szavak_ fájlnév könyve)."""
    if not _FAJLKONYV:
        for k in pm.konyvek():
            _, sorok = _tabla(os.path.join(ADAT, 'parok_%s.tsv' % k))
            if sorok:
                _FAJLKONYV[tokenek.igehely_bont(sorok[0]['vers'])[0]] = k
    return _FAJLKONYV[tokenek.igehely_bont(vers)[0]]


def par_minta(mag):
    _, keret = _tabla(os.path.join(GYOKER, 'f172', 'keret.tsv'))
    sulyok = {r['reteg']: int(r['parsor']) for r in keret if r['reteg'] in pm.RETEGEK}
    db = legnagyobb_maradek(sulyok, N_PAR)
    _, f172 = _tabla(os.path.join(GYOKER, 'f172', 'minta.tsv'))
    ki = []
    for rt in pm.RETEGEK:
        sorok = [r for r in f172 if r['reteg'] == rt]
        rnd = random.Random('%d:par:%s' % (mag, rt))
        for x in sorted(rnd.sample(range(len(sorok)), db[rt])):
            ki.append(sorok[x])
    return ki, db


def nelkul_minta(mag):
    jeloltek = {cs: [] for cs in CSOPORTOK}
    for k in pm.konyvek():
        cs = pm.CSOPORT[k]
        _, sorok = _tabla(os.path.join(ADAT, 'szavak_%s.tsv' % k))
        for r in sorok:
            if r['oldal'] == 'hu' and r['allapot'] == 'betoldas':
                jeloltek[cs].append({'konyv': k, 'vers': r['vers'], 'hu_sorszam': r['sorszam'],
                                     'hu_szo': r['szo'], 'csoport': cs})
    db = legnagyobb_maradek({cs: len(jeloltek[cs]) for cs in CSOPORTOK}, N_NELKUL)
    ki = []
    for cs in CSOPORTOK:
        rnd = random.Random('%d:nelkul:%s' % (mag, cs))
        for x in sorted(rnd.sample(range(len(jeloltek[cs])), db[cs])):
            ki.append(jeloltek[cs][x])
    return ki, db, {cs: len(v) for cs, v in jeloltek.items()}


def epit(mag):
    parok, db_par = par_minta(mag)
    nelkul, db_nelkul, keret_nelkul = nelkul_minta(mag)
    karoli, ered = bemenet._adatok()
    versek = {r['vers'] for r in parok} | {r['vers'] for r in nelkul}
    pv = parok_versenkent(versek)
    lex_pontos, lex_strong = lex_tabla()
    mac = macula_versek(versek)
    hibak = []

    def alap(vers, hu_s):
        szoveg = karoli[vers]
        tl = list(re.finditer(r'[^\W_]+', szoveg, re.UNICODE))
        if [m.group(0) for m in tl] != tokenek.tokenizal(szoveg):
            hibak.append('%s: a tokenizálás eltér' % vers)
        m = tl[hu_s - 1]
        el = ered[vers]
        nt = vers.split(' ')[0] in _USZ_KONYVEK
        if nt:
            illesztes = {}
            for kiad in ('N1904', 'SBLGNT'):
                for s, x in illeszt(el, mac.get((vers, kiad), [])).items():
                    illesztes.setdefault(s, x)
        else:
            illesztes = illeszt(el, mac.get((vers, 'heb'), []))
        tok = []
        ar = None if nt else morf.arami_vers(vers)
        for w in el:
            il = illesztes.get(w['sorsz'])
            lx = lex_pontos.get((w['strong'], w['alak'])) or lex_strong.get(w['strong'], ('', '', ''))
            kod = il[0] if il else ''
            mh = (morf.gorog(kod) if nt else morf.heber(kod, ar)) if kod else None
            tok.append({'n': w['sorsz'], 'a': w['alak'], 's': w['strong'], 't': w['tukor'], 'k': lx[2],
                        'm': kod, 'mh': mh or '', 'w': il[2] if il else '', 'x': 1 if w['nem_tr'] else 0})
        return szoveg, m, el, illesztes, tok, nt

    tetelek = []
    for r in parok:
        v = r['vers']
        h, e = int(r['hu_sorszam']), int(r['er_sorszam'])
        szoveg, m, el, illesztes, tok, nt = alap(v, h)
        if m.group(0) != r['hu_szo']:
            hibak.append('%s hu %d: %s != %s' % (v, h, m.group(0), r['hu_szo']))
        w = el[e - 1]
        if w['alak'] != r['er_szo'] or w['strong'] != r['strong']:
            hibak.append('%s er %d: %s/%s != %s/%s' % (v, e, w['alak'], w['strong'], r['er_szo'], r['strong']))
        if (h, r['hu_szo'], e, r['er_szo'], r['strong']) not in pv.get(v, []):
            hibak.append('%s: a pár (%d→%d) nincs a mai parok-táblában' % (v, h, e))
        tetelek.append(dict(tipus='par', csoport=csoport_of_reteg(r['reteg']), f172_reteg=r['reteg'],
                            f172_id=r['minta_id'], konyv=r['konyv'], vers=v, h=h, e=e, szoveg=szoveg,
                            m=m, w=w, illesztes=illesztes, tok=tok, nt=nt))
    for r in nelkul:
        v = r['vers']
        h = int(r['hu_sorszam'])
        szoveg, m, el, illesztes, tok, nt = alap(v, h)
        if m.group(0) != r['hu_szo']:
            hibak.append('%s hu %d: %s != %s' % (v, h, m.group(0), r['hu_szo']))
        if any(p[0] == h for p in pv.get(v, [])):
            hibak.append('%s hu %d: betoldasnak jelölt szónak mégis van pára' % (v, h))
        tetelek.append(dict(tipus='parnelkuli', csoport=r['csoport'], f172_reteg='', f172_id='',
                            konyv=r['konyv'], vers=v, h=h, e=0, szoveg=szoveg, m=m, w=None,
                            illesztes=illesztes, tok=tok, nt=nt))
    if hibak:
        print('HIBA: a minta nem vezethető le a mai adatból (%d):' % len(hibak))
        for x in hibak[:30]:
            print('  ' + x)
        raise SystemExit(1)

    # tétel-azonosító: a csoportot és a típust nem árulja el (véletlen sorrend, rögzített mag)
    rnd = random.Random('%d:azonosito' % mag)
    sorrend = list(range(len(tetelek)))
    rnd.shuffle(sorrend)
    for uj, i in enumerate(sorrend, 1):
        tetelek[i]['tetel_id'] = 'V%03d' % uj

    sorok = []
    illesztett = 0
    for t in tetelek:
        v, h = t['vers'], t['h']
        vp = sorted(pv.get(v, []))
        tobbi = [p for p in vp if not (p[0] == h and p[2] == t['e'])]
        # ugyanahhoz a magyar szóhoz tartozó párok előre
        tobbi.sort(key=lambda p: (0 if p[0] == h else 1, p[0], p[2]))
        tobbi_szoveg = '; '.join('%d %s → %d %s %s' % p for p in tobbi)
        if t['w'] is not None:
            w = t['w']
            sz, jel, _ = lex_pontos.get((w['strong'], w['alak'])) or lex_strong.get(w['strong'], ('', '', ''))
            il = t['illesztes'].get(w['sorsz'])
            if il:
                illesztett += 1
            ct = t['tok'][t['e'] - 1]
            mkod, szofaj = (il[0], il[1]) if il else ('', '')
            er = [str(t['e']), w['alak'], w['strong'], sz, jel, w['tukor'], mkod, szofaj, '1' if w['nem_tr'] else '0',
                  ct['k'], ct['mh']]
        else:
            er = ['', '', '', '', '', '', '', '', '', '', '']
        er_vers = ' '.join(x['a'] for x in t['tok'])
        sorok.append({
            'tetel_id': t['tetel_id'], 'tipus': t['tipus'], 'csoport': t['csoport'],
            'f172_reteg': t['f172_reteg'], 'f172_id': t['f172_id'], 'konyv': t['konyv'], 'vers': v,
            'hu_vers': t['szoveg'], 'hu_sorszam': str(h), 'hu_szo': t['m'].group(0),
            'hu_kezdet': str(t['m'].start()), 'hu_veg': str(t['m'].end()),
            'er_nyelv': 'gorog' if t['nt'] else 'heber', 'er_vers': er_vers,
            'er_sorszam': er[0], 'er_szo': er[1], 'strong': er[2], 'szoto': er[3], 'jelentes': er[4],
            'tukor': er[5], 'morf': er[6], 'szofaj': er[7], 'nem_tr': er[8], 'kiejtes': er[9], 'morf_hu': er[10],
            'tobbi_par': tobbi_szoveg,
            'er_tokenek_json': json.dumps(t['tok'], ensure_ascii=False, separators=(',', ':')),
            'parok_json': json.dumps([list(p) for p in vp], ensure_ascii=False, separators=(',', ':')),
        })
    for s in sorok:
        for k in MINTA_FEJ:
            if '\t' in s[k] or '\n' in s[k]:
                raise SystemExit('tabulátor vagy sortörés a mezőben: %s %s' % (s['tetel_id'], k))
    sorok.sort(key=lambda s: s['tetel_id'])
    return sorok, db_par, db_nelkul, keret_nelkul, illesztett


_USZ_KONYVEK = None


def _usz_konyvek():
    hu = set()
    for k in pm.konyvek():
        if pm.CSOPORT[k].startswith('USZ'):
            _, sorok = _tabla(os.path.join(ADAT, 'parok_%s.tsv' % k))
            if sorok:
                hu.add(tokenek.igehely_bont(sorok[0]['vers'])[0])
    return hu


# ---------------------------------------------------------------- írás

def minta_ir(sorok, db_par, db_nelkul, keret_nelkul, mag, head):
    ut = os.path.join(KIMENET, 'minta.tsv')
    par_cs = {}
    for rt, n in db_par.items():
        par_cs[csoport_of_reteg(rt)] = par_cs.get(csoport_of_reteg(rt), 0) + n
    prov = ('# MANUAL: scope=F175.V emberi validációs minta (%d szópár a #172 rétegzett mintájának arányos '
            'részmintájaként + %d pár nélküli magyar szó, könyvcsoportonként arányosan; mag=%d) | '
            'forras=f172/minta.tsv, f172/keret.tsv, adat/karoli_strong/parok_*.tsv, szavak_*.tsv, '
            'konkordancia/Karoli_1908.tsv, TAHOT_kivonat.tsv, TAGNT_kivonat.tsv, Macula_*.tsv @ %s | ts=git:%s | '
            'manual (determinisztikus mintavétel: eszkozok/karoli_strong_validacio_minta.py; a párok '
            'modell-kimenet, javaslat) | párok: %s | pár nélkül: %s'
            % (N_PAR, N_NELKUL, mag, head, head,
               ', '.join('%s %d' % (cs, par_cs[cs]) for cs in CSOPORTOK),
               ', '.join('%s %d/%d' % (cs, db_nelkul[cs], keret_nelkul[cs]) for cs in CSOPORTOK)))
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(prov + '\n')
        f.write('\t'.join(MINTA_FEJ) + '\n')
        for s in sorok:
            f.write('\t'.join(s[k] for k in MINTA_FEJ) + '\n')
    return par_cs


def minta_olvas():
    _, sorok = _tabla(os.path.join(KIMENET, 'minta.tsv'))
    return sorok


def html_ir(sorok):
    """Az ellenőrző oldal: a sablon `/*MINTA_ADAT*/null` helyére a minta JSON-ja."""
    adat = []
    for s in sorok:
        adat.append({
            'id': s['tetel_id'], 'tipus': s['tipus'], 'vers': s['vers'], 'hu': s['hu_vers'],
            'hn': int(s['hu_sorszam']), 'hk': int(s['hu_kezdet']), 'hv': int(s['hu_veg']), 'hs': s['hu_szo'],
            'nyelv': s['er_nyelv'], 'en': int(s['er_sorszam']) if s['er_sorszam'] else 0,
            'strong': s['strong'], 'szoto': s['szoto'], 'jel': s['jelentes'], 'tukor': s['tukor'],
            'morf': s['morf'], 'mh': s['morf_hu'], 'kiej': s['kiejtes'], 'ntr': s['nem_tr'] == '1',
            'tok': json.loads(s['er_tokenek_json']), 'parok': json.loads(s['parok_json']),
        })
    js = json.dumps(adat, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    with open(SABLON, encoding='utf-8') as f:
        sablon = f.read()
    if sablon.count('/*MINTA_ADAT*/null') != 1:
        raise SystemExit('a sablonban pontosan egy /*MINTA_ADAT*/null helyőrző kell')
    ki = sablon.replace('/*MINTA_ADAT*/null', js)
    with open(os.path.join(KIMENET, 'ellenorzo.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(ki)
    return len(ki)


def main():
    global _USZ_KONYVEK
    ap = argparse.ArgumentParser()
    ap.add_argument('--mag', type=int, default=MAG)
    ap.add_argument('--csak-html', action='store_true')
    a = ap.parse_args()
    os.makedirs(KIMENET, exist_ok=True)
    if not a.csak_html:
        _USZ_KONYVEK = _usz_konyvek()
        sorok, db_par, db_nelkul, keret_nelkul, illesztett = epit(a.mag)
        par_cs = minta_ir(sorok, db_par, db_nelkul, keret_nelkul, a.mag, git_head())
        print('minta: %d tétel -> kozlemeny/data_paper/validacio/minta.tsv' % len(sorok))
        print('  párok (%d):' % N_PAR)
        for cs in CSOPORTOK:
            print('    %-15s %3d' % (cs, par_cs[cs]))
        print('    (#172-rétegenként: %s)' % ', '.join('%s %d' % (k, v) for k, v in db_par.items()))
        print('  pár nélküli szavak (%d, a betoldás-keretből):' % N_NELKUL)
        for cs in CSOPORTOK:
            print('    %-15s %3d / %d' % (cs, db_nelkul[cs], keret_nelkul[cs]))
        print('  alaktani adat (Macula-illesztés) a párok forrásszavánál: %d / %d' % (illesztett, N_PAR))
        tk = [x for s in sorok for x in json.loads(s['er_tokenek_json'])]
        print('  a minta verseinek forrásszavai: %d; alaktan nélkül %d, átírás nélkül %d'
              % (len(tk), sum(1 for x in tk if not x['mh']), sum(1 for x in tk if not x['k'])))
    meret = html_ir(minta_olvas())
    print('ellenőrző oldal: %d bájt -> kozlemeny/data_paper/validacio/ellenorzo.html' % meret)


if __name__ == '__main__':
    main()
