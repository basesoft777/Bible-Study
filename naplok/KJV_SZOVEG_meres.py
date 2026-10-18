#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KJV_SZOVEG_meres.py -- #118 M2 mérése (brief 4. pont, M2.2): M-a vershalmaz, M-b szóegyezés, M-c épség, és a
mellékes F19-kérdés (érinti-e a KJV_Strongs_teljes.tsv-t, hogy az F19-parse a \\s1-sort az előző vershez fűzi).
A mérőkód nem a generátorban van: a táblákat split('\\t')-tel olvassa, a nyers zipet közvetlenül (zipfile), a jelölő-
számokat a generátortól függetlenül számolja, és a tábla fejlécének veszteség-sorával veti össze. Csak olvas, kivéve:
  naplok/KJV_SZOVEG_szoegyezes_hiany.tsv   csak ha az M-b nem illeszkedő szót talál

Futtatás:  python -I naplok/KJV_SZOVEG_meres.py --zip C:/Users/bases/Desktop/kjv_munka/kjv.zip
"""

import argparse
import collections
import datetime
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BS = chr(92)
E = re.escape(BS)
UJ = os.path.join(REPO, 'konkordancia', 'KJV_teljes_szoveg.tsv')
REGI = os.path.join(REPO, 'konkordancia', 'KJV_Strongs_teljes.tsv')
HIANY = os.path.join(REPO, 'naplok', 'F19_hianyok.tsv')
KONYVTABLA = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
WJ = '\u2039\u203a'
PILCROW = '\u00b6'


def tabla(fajl):
    fej, fejlec, sorok = [], None, []
    for s in open(fajl, encoding='utf-8').read().split('\n'):
        if not s:
            continue
        if s.startswith('#'):
            fej.append(s)
        elif fejlec is None:
            fejlec = s.split('\t')
        else:
            sorok.append(s.split('\t'))
    return fej, fejlec, sorok


def kulcs(ih):
    b, f, v = ih.split('.')
    return (b, int(f), int(v))


def norm_tokenek(szoveg):
    t = szoveg.lower().replace('\u2019', "'").replace('\u2018', "'")
    t = re.sub(r"[^a-z0-9\u00e6']+", ' ', t)
    return [w.strip("'") for w in t.split() if w.strip("'")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--zip', required=True)
    a = ap.parse_args()
    zsha = hashlib.sha256(open(a.zip, 'rb').read()).hexdigest()
    usha = hashlib.sha256(open(UJ, 'rb').read()).hexdigest()
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    print('# proveniencia: scope=KJV_SZOVEG M2 mérés (M-a, M-b, M-c, F19-kérdés) | forras=konkordancia/KJV_teljes_szoveg.tsv sha256=%s + '
          'konkordancia/KJV_Strongs_teljes.tsv + naplok/F19_hianyok.tsv + kjv.zip sha256=%s | ts=%s' % (usha, zsha, ts))
    konyvek = [s.split('\t')[0] for s in open(KONYVTABLA, encoding='utf-8').read().split('\n')[1:] if s.strip()]
    ufej, ufejlec, usorok = tabla(UJ)
    rfej, _rf, rsorok = tabla(REGI)
    print('fejléc:', ufejlec, '| fejlécsorok:', len(ufej), '| első sor GENERÁLT:', ufej[0].startswith('# GENERÁLT:'))
    T = {kulcs(r[0]): r for r in usorok}
    assert len(T) == len(usorok), 'ismétlődő Igehely'
    S = collections.OrderedDict()
    for r in rsorok:
        S.setdefault(kulcs(r[0]), []).append((int(r[1]), r[2], r[3]))

    # ---- M-a
    kan = [k for k in T if k[2] > 0]
    print('M-a: |T|=%d (v>0: %d, v=0: %d); |S|=%d; S ⊆ T: %s; |S - T|=%d' % (
        len(T), len(kan), len(T) - len(kan), len(S), set(S) <= set(T), len(set(S) - set(T))))
    ts_ = sorted(set(T) - set(S))
    hianyok = set()
    for s in open(HIANY, encoding='utf-8').read().split('\n'):
        c = s.split('\t')
        if len(c) > 1 and c[0] == 'KJV':
            hianyok.add(kulcs(c[1]))
    print('M-a: T - S = %s; F19_hianyok KJV címke nélküli = %s; azonos: %s' % (
        ['%s.%d.%d' % k for k in ts_], ['%s.%d.%d' % k for k in sorted(hianyok)], set(ts_) == hianyok))
    sorrend = [kulcs(r[0]) for r in usorok]
    rend = {b: i for i, b in enumerate(konyvek)}
    print('M-a: a sorok kanonikus sorrendben (könyv, fejezet, vers): %s; könyvek: %d' % (
        sorrend == sorted(sorrend, key=lambda k: (rend[k[0]], k[1], k[2])), len({k[0] for k in T})))

    # ---- M-b
    # Sorrendtarto reszsorozat-illesztes, ket megmagyarazott osztallyal (az M2 elso futasa 90 nem illeszkedo szoelemet
    # adott, mind a forras szohataron beluli cimkezese miatt):
    #   osszetett_szo -- egy irott szot tobb cimkes resz alkot (where+in = wherein, can+not = cannot, bold+ly = boldly,
    #                    day+s = day's): a kovetkezo szoelemek osszefuzve adjak a tokent (aposztrof nelkul osszevetve)
    #   szoreszlet    -- a cimke csak a szo elejet fedi, a maradek cimke nelkuli (afrai|..+d, give|..+n): a token a szoelemmel kezdodik
    # Minden mas: nincs_a_szovegben / sorrend (megmagyarazatlan).
    hiany_sorok = []
    osszes = 0
    oszt = collections.Counter()

    def ap(x):
        return x.replace("'", '')

    for k, szavak in S.items():
        tok = norm_tokenek(T[k][1])
        elemek = [(sorsz, st, szo, w) for sorsz, st, szo in sorted(szavak) for w in norm_tokenek(szo)]
        i = 0
        e = 0
        while e < len(elemek):
            sorsz, st, szo, w = elemek[e]
            jx = next((j for j in range(i, len(tok)) if tok[j] == w), None)
            jo = None
            for j in range(i, len(tok) if jx is None else jx):
                if ap(tok[j]).startswith(ap(w)) and ap(tok[j]) != ap(w):
                    osszefuz, n = ap(w), 1
                    while len(osszefuz) < len(ap(tok[j])) and e + n < len(elemek):
                        osszefuz += ap(elemek[e + n][3])
                        n += 1
                    if osszefuz == ap(tok[j]) and n > 1:
                        jo = (j, n)
                        break
            if jo is not None:
                j, n = jo
                for d in range(n):
                    s2, st2, szo2, w2 = elemek[e + d]
                    osszes += 1
                    oszt['osszetett_szo'] += 1
                    hiany_sorok.append(('%s.%d.%d' % k, str(s2), st2, szo2, w2, 'osszetett_szo', tok[j]))
                i = j + 1
                e += n
                continue
            osszes += 1
            if jx is not None:
                oszt['pontos'] += 1
                i = jx + 1
                e += 1
                continue
            jr = next((j for j in range(i, len(tok)) if ap(tok[j]).startswith(ap(w))), None)
            if jr is not None:
                oszt['szoreszlet'] += 1
                hiany_sorok.append(('%s.%d.%d' % k, str(sorsz), st, szo, w, 'szoreszlet', tok[jr]))
                i = jr + 1
            else:
                ok = 'nincs_a_szovegben' if w not in tok else 'sorrend'
                oszt[ok] += 1
                hiany_sorok.append(('%s.%d.%d' % k, str(sorsz), st, szo, w, ok, ''))
            e += 1
    megmagy = oszt['nincs_a_szovegben'] + oszt['sorrend']
    print('M-b: szóelem %d; osztályok: %s; megmagyarázatlan: %d' % (osszes, dict(oszt), megmagy))
    if hiany_sorok:
        with open(os.path.join(REPO, 'naplok', 'KJV_SZOVEG_szoegyezes_hiany.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('# proveniencia: scope=KJV_SZOVEG M-b (a KJV_Strongs_teljes.tsv Angol szó-elemei a KJV_teljes_szoveg.tsv Szöveg-tokenjeiben) | forras=KJV_teljes_szoveg.tsv sha256=%s | ts=%s\n' % (usha, ts))
            fh.write('# ok: osszetett_szo = több címkés rész egy írott szóban (token); szoreszlet = a címke csak a szó elejét fedi; nincs_a_szovegben / sorrend = megmagyarázatlan\n')
            fh.write('\t'.join(['Igehely', 'Szósorszám', 'Strong-szám', 'Angol szó', 'szóelem', 'ok', 'token_a_szövegben']) + '\n')
            for h in hiany_sorok:
                fh.write('\t'.join(h) + '\n')
        for h in [h for h in hiany_sorok if h[5] in ('nincs_a_szovegben', 'sorrend')][:20]:
            print('   ', h)
    hiany_sorok = [h for h in hiany_sorok if h[5] in ('nincs_a_szovegben', 'sorrend')]

    # ---- M-c
    ures = [r[0] for r in usorok if not r[1].strip()]
    print('M-c: üres Szöveg: %d %s; üres Szöveg_jelolt: %d' % (len(ures), ures[:5], sum(1 for r in usorok if not r[2].strip())))
    pk = collections.Counter(k[0] for k in T)
    print('M-c: versek könyvenként: ' + ' '.join('%s=%d' % (b, pk[b]) for b in konyvek))
    hibak = collections.Counter()
    for r in usorok:
        if len(r) != 5:
            hibak['oszlopszam'] += 1
        for i, ert in enumerate(r[1:], 1):
            if BS in ert:
                hibak['backslash_%d' % i] += 1
            if re.search(r' [,.;:?!)]', ert):
                hibak['szokoz_irasjel_elott_%d' % i] += 1
            if '  ' in ert or ert != ert.strip():
                hibak['szokoz_%d' % i] += 1
        if any(c in r[1] for c in WJ + PILCROW):
            hibak['jel_a_Szovegben'] += 1
        if re.sub('[\\[\\]' + WJ + PILCROW + ']', '', r[2]).split() != r[1].split():
            hibak['Szoveg_jelolt_szavai_elternek:' + r[0]] += 1
        if r[2].count('[') != r[2].count(']') or r[2].count(WJ[0]) != r[2].count(WJ[1]):
            hibak['paratlan_jel:' + r[0]] += 1
        if any(c in (r[3] + r[4]) for c in WJ + PILCROW + '[]'):
            hibak['jel_az_Elotte_Utoirat_ban'] += 1
    print('M-c: formai ellenőrzés:', dict(hibak) or 0)
    print('M-c: Elotte nem üres: %s; Utoirat nem üres: %s' % (
        ' '.join(r[0] for r in usorok if r[3]), ' '.join(r[0] for r in usorok if r[4])))
    print('M-c: ‹…› sorok: %d; [..] sorok: %d; ¶ sorok (Szöveg_jelolt): %d' % (
        sum(1 for r in usorok if WJ[0] in r[2]), sum(1 for r in usorok if '[' in r[2]), sum(1 for r in usorok if PILCROW in r[2])))

    # nyers zip: független jelölőszámok (66 kanonikus könyv) és a vershidak; az F19-kérdés
    z = zipfile.ZipFile(a.zip)
    kan_usfm = {b.upper() for b in konyvek}
    nyit = collections.Counter()
    hid = 0
    s1_sor = 0
    s1_strong = 0
    for n in z.namelist():
        m = re.match(r'^[0-9]+-([0-9A-Z]{3})eng-kjv\.usfm$', n)
        if not m or m.group(1) not in kan_usfm:
            continue
        t = z.read(n).decode('utf-8-sig')
        nyit['f'] += len(re.findall(E + r'f ', t))
        tf = re.sub(E + r'f .*?' + E + r'f\*', '', t, flags=re.S)  # a labjegyzeten beluli jelolo nem szamit (az importalo is eldobja)
        for mj in re.finditer(E + r'\+?([a-z]+[0-9]*)(\*?)', tf):
            if not mj.group(2):
                nyit[mj.group(1)] += 1
        nyit['strong='] += t.count('strong="')
        hid += len(re.findall(E + r'v [0-9]+-[0-9]+', t))
        for sor in t.split('\n'):
            if re.match(E + r's1( |$)', sor):
                s1_sor += 1
                s1_strong += sor.count('strong="')
    print('M-c: vershíd (\\v n-m) a nyers forrásban: %d' % hid)
    vesz = ufej[4]
    minta = {'strong=': r'strong=\) ([0-9]+)', 'f': r'\(\\f\) ([0-9]+)', 'p': r'\\p ([0-9]+)', 'q1': r'\\q1 ([0-9]+)',
             'b': r'\\b ([0-9]+)', 'nd': r'\\nd ([0-9]+)', 'tl': r'\\tl ([0-9]+)', 'wj': r'\\wj ([0-9]+)', 'add': r'\\add-jelölés ([0-9]+)'}
    egyez = {}
    for k, mi in minta.items():
        mm = re.search(mi, vesz)
        egyez[k] = (int(mm.group(1)) if mm else None, nyit[k])
    print('M-c: veszteség-sor (generátor) vs nyers jelölőszám (független): ' + ' '.join(
        '%s=%s/%s%s' % (k, g, n, '' if g == n else ' ELTÉR') for k, (g, n) in egyez.items()))
    print('M-c: ‹…› lezárás (versen átnyúló \\wj): ' + (re.search(r'lezárása ([0-9]+)', vesz).group(1)))
    # F19-kerdes: a \s1-sorban van-e Strong-cimke (ha nincs, az F19-parse nem fuz szot a tablaba), es az erintett versek M-b-je
    erintett = {kulcs('Psa.119.%d' % v) for v in range(8, 169, 8)} | {kulcs(r[0]) for r in usorok if r[4]}
    erintett_hiany = [h for h in hiany_sorok if kulcs(h[0]) in erintett]
    print('F19: \\s1-sor a 66 kanonikus könyvben: %d; strong= bennük: %d' % (s1_sor, s1_strong))
    print('F19: az érintett %d vers (Zsolt 119:8, 16 … 168 és a 14 utóiratos vers) táblabeli szavai: %d, ebből a versszövegben nem illeszkedő: %d' % (
        len(erintett), sum(len(S.get(k, [])) for k in erintett), len(erintett_hiany)))
    # reprodukalhatosag: a generator ujrafuttatva bajtra ugyanaz (ideiglenes konyvtarba, repon kivul)
    tmp = tempfile.mkdtemp(prefix='kjv_m2_')
    ki = os.path.join(tmp, 'KJV_teljes_szoveg.tsv')
    subprocess.run([sys.executable, '-I', os.path.join(REPO, 'eszkozok', 'kjv_szoveg_import.py'), '--munka', os.path.dirname(a.zip),
                    '--kimenet', ki], check=True, capture_output=True)
    ujra = hashlib.sha256(open(ki, 'rb').read()).hexdigest()
    os.remove(ki)
    os.rmdir(tmp)
    print('reprodukálhatóság: újragenerálva bájtra azonos: %s (%s)' % (ujra == usha, ujra[:16]))


if __name__ == '__main__':
    main()
