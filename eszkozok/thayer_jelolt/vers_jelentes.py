#!/usr/bin/env python
"""A Thayer igehely-hivatkozásai jelentésponthoz kötve (F132 M2; FELADATOK #132; DT-F132b (2)).

Minden `<ref onclick="bcv(k,f,v)">` egy sor, a szócikkön belüli sorrendben: a könyvszám (1–66) a
`konkordancia/Konyv_normalizalo_tabla.tsv` k-adik adatsorán át Károli-rövidítés; a `karoli_vers` a `Karoli_1908.tsv`
`Igehely` kulcsa, ha ilyen vers van (különben üres: kitöltés nélkül); a `szakasz` és az `utvonal` a hivatkozást tartalmazó
bekezdésé (`thayer_jelolt/bont.py` szerkezete, a `thayer_szakaszok.tsv` `strong` + `sorszam` kulcsa). ÚSZ-helyen a számozás
egyezik; az ÓSZ-hivatkozások (LXX-utalás) Károli-megfelelője csak a vers létezését méri, átkulcsolás nincs (a naplóban mérve).

A `bcv`-jelölt hivatkozás mellett a közvetlenül utána (`</ref>` után) álló, a forrásban jelöletlen folytatás is sor
(„Act 9:14</ref>,21; 22:16”: a 9:21 és a 22:16; ELLENOR_SZOTARI_GERINC 2., a BDB-s DT-F131l (A) mintájára): `,v` ugyanabban a
fejezetben, `; c:v` ugyanabban a könyvben, amíg a lánc tart; a verstartomány (`-v`) nincs kibontva. A lánc csak közvetlenül a
`</ref>` után indulhat, és megszakad, ha a szám után könyvnév jön („, 2 Esdr. 10:2”) vagy a szám után kettőspont áll
(„, 34:”). Az ilyen sor proveniencia-forrása `(fejléc, folytatas)`.

Módok: (alap) írás · --meres · --ellenoriz (a fájl fejlécének --ts-ével újragenerál és bájtra összevet).
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
if ITT not in sys.path:
    sys.path.insert(0, ITT)
import bont  # noqa: E402

GYOKER = bont.GYOKER
KONYV_UT = os.path.join(GYOKER, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
KAROLI_UT = os.path.join(GYOKER, 'konkordancia', 'Karoli_1908.tsv')
KI_UT = os.path.join(GYOKER, 'adat', 'thayer_vers_jelentes.tsv')

FEJLEC = ['strong', 'sorszam', 'szakasz', 'konyv', 'fejezet', 'vers', 'karoli_vers', 'utvonal', 'proveniencia']
# A Karoli_1908.tsv a Siralmakat „Sir”-nek írja, a könyvtábla „JSir”-nek (a bdb_vers_jelentes.py KAROLI_KONYV mintája):
# a `konyv` a könyvtábla alakja, a `karoli_vers` a Károli-szöveg kulcsa.
KAROLI_KONYV = {'JSir': 'Sir'}
BCV = re.compile(r'<ref\b[^>]*\bonclick="bcv\((\d+),(\d+),(\d+)\)"[^>]*>')
REF = re.compile(r'<ref\b')
REF_VEG = re.compile(r'</ref>')
# a jelöletlen folytatás (ELLENOR_SZOTARI_GERINC 2.): a lánc közvetlenül a `</ref>` után; a szám után nem állhat számjegy,
# kettőspont (a „34:” fejezetszám vagy írásjel, kétértelmű) vagy könyvnév + szám („2 Esdr. 10:2”, „1 Samuel 21”)
_UTANA = r'(?![\d:])(?!\s*[A-Za-z][A-Za-z.]*\s*\d)'
FOLYT_VERS = re.compile(r'\s*,\s*(\d{1,3})' + _UTANA)
FOLYT_FEJEZET = re.compile(r'\s*;\s*(\d{1,3}):(\d{1,3})' + _UTANA)
FOLYT_TARTOMANY = re.compile(r'\s*[-–]\s*\d{1,3}' + _UTANA)


def folytatasok(raw, poz, fejezet):
    """[(fejezet, vers)]: a `poz`-on (a `</ref>` vége) induló jelöletlen folytatás-lánc; tartomány-kibontás nélkül."""
    ki, q, f = [], poz, fejezet
    t = FOLYT_TARTOMANY.match(raw, q)
    if t:
        q = t.end()
    while True:
        m = FOLYT_VERS.match(raw, q)
        if m:
            ki.append((f, int(m.group(1))))
        else:
            m = FOLYT_FEJEZET.match(raw, q)
            if not m:
                break
            f = int(m.group(1))
            ki.append((f, int(m.group(2))))
        q = m.end()
        t = FOLYT_TARTOMANY.match(raw, q)
        if t:
            q = t.end()
    return ki


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return [s.rstrip('\r').split('\t') for s in f.read().split('\n') if s.rstrip('\r')]


def konyvek(ut=KONYV_UT):
    """könyvszám (1-től, a tábla adatsorainak sorrendje) -> Károli-rövidítés."""
    s = tsv_sorok(ut)
    i = s[0].index('Magyar rövidítés')
    return {n: r[i] for n, r in enumerate(s[1:], 1)}


def karoli_kulcsok(ut=KAROLI_UT):
    s = tsv_sorok(ut)
    i = s[0].index('Igehely')
    return {r[i] for r in s[1:]}


def kod_hash():
    h = hashlib.sha256()
    for ut in (os.path.abspath(__file__), os.path.join(ITT, 'bont.py'), os.path.join(ITT, 'kulcs.py')):
        with open(ut, 'rb') as f:
            h.update(f.read().replace(b'\r\n', b'\n'))
    return h.hexdigest()


def general(ts):
    lex = bont.lexikon_beolvas()
    kv = konyvek()
    kk = karoli_kulcsok()
    sorok, stat = [], collections.Counter()
    for sp, (topic, d) in lex.items():
        n = 0
        stat['ref_nem_bcv'] += len(REF.findall(d)) - len(BCV.findall(d))
        for sz_i, x in enumerate(bont.szerkezet(d), 1):
            for m in BCV.finditer(x['raw']):
                k, f0, v0 = (int(g) for g in m.groups())
                konyv = kv.get(k, '')
                vege = REF_VEG.search(x['raw'], m.end())
                lanc = folytatasok(x['raw'], vege.end(), f0) if vege else []
                for i, (f, v) in enumerate([(f0, v0)] + lanc):
                    n += 1
                    kar = '%s %d:%d' % (KAROLI_KONYV.get(konyv, konyv), f, v) if konyv else ''
                    if kar not in kk:
                        kar = ''
                    resz = 'usz' if k >= 40 else 'osz'
                    stat[resz] += 1
                    if i:
                        stat['folytatas'] += 1
                    if not konyv:
                        stat['ismeretlen_konyv'] += 1
                    elif not kar:
                        stat['nincs_karoli_' + resz] += 1
                    sorok.append([sp, str(n), str(sz_i), konyv or str(k), str(f), str(v), kar, x['utvonal'],
                                  'scope=%s | forras=thayer_jelolt/vers_jelentes.py (fejléc%s) | ts=%s'
                                  % (sp, ', folytatas' if i else '', ts)])
        # a szerkezeten kívüli (üres bekezdésbe eső) bcv nem lehet: a teszt a teljes számot a nyers HTML-lel veti össze
    stat['sor'] = len(sorok)
    return sorok, stat


def fajl_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/thayer_jelolt/vers_jelentes.py --ts %s — kézzel nem szerkesztendő (F132; séma: adat/SEMA.md, thayer_vers_jelentes.tsv).' % ts,
           '# forras: konkordancia/lexikonok_nyers/Thayer.lexicon@%s (a bcv-koordináta, a szerkezet és a `</ref>` utáni '
           'jelöletlen folytatás, DT-F131n) + '
           'konkordancia/Konyv_normalizalo_tabla.tsv@%s + konkordancia/Karoli_1908.tsv@%s + kód@%s'
           % (bont.sha256_fajl(bont.LEX_UT)[:12], bont.sha256_fajl(KONYV_UT)[:12], bont.sha256_fajl(KAROLI_UT)[:12],
              kod_hash()[:12]),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(s) for s in sorok]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts')
    ap.add_argument('--meres', action='store_true')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    ts = a.ts or (bont.fajl_ts(KI_UT) if a.ellenoriz and os.path.exists(KI_UT) else None) or datetime.date.today().isoformat()
    sorok, stat = general(ts)
    print('sor: %d (ebből jelöletlen folytatás %d); ÚSZ %d, ÓSZ %d; Károli-vers nélkül: ÚSZ %d, ÓSZ %d; ismeretlen könyv %d; '
          'bcv nélküli <ref>: %d'
          % (stat['sor'], stat['folytatas'], stat['usz'], stat['osz'], stat['nincs_karoli_usz'], stat['nincs_karoli_osz'],
             stat['ismeretlen_konyv'], stat['ref_nem_bcv']))
    if a.meres:
        return 0
    szoveg = fajl_szoveg(sorok, ts)
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
