#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bdb_psi_javit.py — F34 M2/M3: a BDB forras `psi` (Zsoltarok) hibas feloldasanak javitasa.

A nyers DictBDB.json nincs a repoban (a _convert_bdb.py a Temp-bol olvasna), tehat a
parser-javitas nem lehetseges: mezokulcsos csere a kesz TSV-n (DT-F34 1-4. pont).

Dontes soronkent (kulcs: szocikk-id + regi + uj):
  - A (fejezet>66 vagy Psalm-szo): javul, ha a szocikk Strong-szama a TAHOT szerint
    elofordul a Zsolt c:v-ben (+-1 vers); egyebkent marad (B).
  - B/R: javul, ha Zsolt c:v (+-1) talalat van, ES a TAHOT szerint SEMMILYEN mas
    konyv c:v (+-1) helyen nincs (egyertelmu); egyebkent marad (kezi nezet).
Lista: naplok/F34_M0_lista.tsv. Kimenet: naplok/F34_M2_csere.tsv, F34_M2_maradek.tsv.

Futtatas a repo gyokerebol:
    python eszkozok/bdb_psi_javit.py          # szarazon
    python eszkozok/bdb_psi_javit.py --ir     # forras + adat/forditasok.tsv iras
I/O: split('\\t') / '\\t'.join (csv modul nelkul); iras elott sor-osszevetes.
"""
import hashlib
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

FORRAS = 'konkordancia/BDB_teljes_unabridged.tsv'
LISTA = 'naplok/F34_M0_lista.tsv'
TAHOT = 'konkordancia/TAHOT_kivonat.tsv'
FORD = 'adat/forditasok.tsv'
MACULA_ZS = 'konkordancia/Macula_heber_Zsoltarok.tsv'   # MT-szamozas, a versszamozasi tabla forrasa
CSERE_TABLA = 'naplok/F34_M2_csere.tsv'
# DT-F34c (felhasznalo, 2026.10.01): a 81. (H7585) es 84. (H7843) sor token- es forras_hash-frissitese
# jovahagyva. Vedett (nem irjuk at) mezokulcsos: (szotar, strong, entry_id, jelentes_szam, mezo); a
# H8034 sor (Dan 22:14 forrashiba, N-F34c) valtozatlan marad.
VEDETT_KULCSOK = {('BDB', 'H8034', 'H8034', 'teljes', 'forditas_hu')}
KULCS_MEZOK = ('szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo')
# nem psi eredetu konyvfeloldasi hiba (Dt->Dan): a maradek-tablabol kimarad (DT-F34c 3. pont, N-F34c)
NEM_PSI_KONYV = ('Dan ',)


def vedett(sor):
    """sor: dict (a forditasok.tsv fejlec-mezoivel). Mezokulcsos, nem fajlsorszamos."""
    return tuple(sor[k] for k in KULCS_MEZOK) in VEDETT_KULCSOK

HU = {'Gen': '1Móz', 'Exod': '2Móz', 'Lev': '3Móz', 'Num': '4Móz', 'Deut': '5Móz', 'Josh': 'Józs',
      'Judg': 'Bír', 'Ruth': 'Ruth', '1Sam': '1Sám', '2Sam': '2Sám', '1Kin': '1Kir', '2Kin': '2Kir',
      '1Chr': '1Krón', '2Chr': '2Krón', 'Ezra': 'Ezsd', 'Neh': 'Neh', 'Esth': 'Eszt', 'Job': 'Jób',
      'Psa': 'Zsolt', 'Prov': 'Péld', 'Eccl': 'Préd', 'Song': 'Én', 'Isa': 'Ézs', 'Jer': 'Jer',
      'Lam': 'Sir', 'Ezek': 'Ez', 'Dan': 'Dán', 'Hos': 'Hós', 'Joel': 'Jóel', 'Amos': 'Ámós',
      'Obad': 'Abd', 'Jonah': 'Jón', 'Mic': 'Mik', 'Nah': 'Náh', 'Hab': 'Hab', 'Zeph': 'Sof',
      'Hag': 'Hag', 'Zech': 'Zak', 'Mal': 'Mal', '1Ki': '1Kir', '2Ki': '2Kir'}
# a fordito a Lam-ot JSir-nek irja; a TAHOT 'Sir'
HU_FORD = dict(HU)
HU_FORD['Lam'] = 'JSir'


def tahot_idx():
    idx = {}
    for l in open(TAHOT, encoding='utf-8').read().split('\n')[1:]:
        p = l.split('\t')
        if len(p) < 2:
            continue
        m = re.match(r'(.+) (\d+):(\d+)$', p[0])
        if not m:
            continue
        idx.setdefault(p[1], set()).add((m.group(1), int(m.group(2)), int(m.group(3))))
    return idx


def vers_tabla():
    """Zsolt (MT) fejezet -> a letezo versek halmaza, a Macula morfema-sorokbol (ref: PSA c:v!n)."""
    t = {}
    for l in open(MACULA_ZS, encoding='utf-8').read().split(chr(10)):
        if not l or l.startswith('#'):
            continue
        m = re.match(r'[^	]*	PSA (\d+):(\d+)!', l)
        if m:
            t.setdefault(int(m.group(1)), set()).add(int(m.group(2)))
    return t


def csere_forditason(hu, strong, csere):
    """A csere-tablat (naplok/F34_M2_csere.tsv, dontes=JAVIT sorok) a LEFORDITOTT szovegre alkalmazza.
    csere: [(szocikk_id, regi_angol_token, uj_angol_token), ...]; csak a helyhivatkozas tokenje
    valtozik (a forditas tobbi resze bajtazonos). Visszater: (uj_szoveg, [(regi_hu, uj_hu), ...])."""
    ki = []
    for st, regi, uj in csere:
        if st != strong:
            continue
        bk, rest = regi.split(' ', 1)
        hk = HU_FORD[bk]
        pat = re.compile(r'(?<![\wÀ-ɏ])' + re.escape(hk + ' ' + rest) + r'(?!\d)')
        if pat.search(hu):
            hu = pat.sub('Zsolt ' + rest, hu)
            ki.append((hk + ' ' + rest, 'Zsolt ' + rest))
    return hu, ki


def csere_beolvas():
    sor = open(CSERE_TABLA, encoding='utf-8').read().split(chr(10))[1:]
    return [(p[0], p[1], p[2]) for p in (l.split(chr(9)) for l in sor if l) if p[5] == 'JAVIT']


def talal(idx, strong, konyv, c, v):
    s = idx.get(strong[:5], set())
    return [x for x in ((konyv, c, v - 1), (konyv, c, v), (konyv, c, v + 1)) if x in s]


def masutt(idx, strong, c, v):
    """masik konyvben (nem Zsolt) c:v +-1 helyen elofordul-e"""
    s = idx.get(strong[:5], set())
    return sorted({k for (k, cc, vv) in s if k != 'Zsolt' and cc == c and abs(vv - v) <= 1})


def forditas_ujrafuttat(ir):
    """--forditas: a csere-tabla (JAVIT sorok) ujrafuttatasa a LEFORDITOTT BDB-szovegen (adat/forditasok.tsv).
    Csak a helyhivatkozas tokenje valtozik; a forras_hash-t NEM erinti (az a forrasbol szamolodik);
    a vedett (mezokulcsos) sorokat kihagyja. Igy a maradek kesobbi felbontasa nem igenyel ujrafordítast."""
    csere = csere_beolvas()
    fs = open(FORD, encoding='utf-8', newline='').read().split(chr(10))
    fej = fs[1].split(chr(9))
    ix = {k: i for i, k in enumerate(fej)}
    valt = []
    for n, l in enumerate(fs, 1):
        if n <= 2 or not l:
            continue
        p = l.split(chr(9))
        if vedett(dict(zip(fej, p))):
            continue
        if p[ix['szotar']] != 'BDB' or p[ix['mezo']] != 'forditas_hu':
            continue
        hu2, ki = csere_forditason(p[ix['forditas_hu']], p[ix['strong']], csere)
        if ki:
            p[ix['forditas_hu']] = hu2
            fs[n - 1] = chr(9).join(p)
            valt.append((n, p[ix['strong']], ki))
    print('forditas-ujrafuttatas: valtozo sorok:', valt)
    if ir and valt:
        open(FORD, 'w', encoding='utf-8', newline='').write(chr(10).join(fs))
        print('IRVA')


def hash_frissit(ir):
    """--hash-frissit: a nem vedett BDB `teljes` sorok, amelyek tarolt forras_hash-e elter az AKTUALIS forras
    SHA-1-jetol: a csere-tabla tokenjei + az uj hash. Kapu: a szodiffben csak helyhivatkozas-token
    es a forras_hash valtozhat; mas valtozas eseten megall (kilepesi kod 6)."""
    csere = csere_beolvas()
    forras = {}
    for l in open(FORRAS, encoding='utf-8', newline='').read().split(chr(10))[1:]:
        if l:
            q = l.split(chr(9))
            forras[q[0]] = q[2]
    fs = open(FORD, encoding='utf-8', newline='').read().split(chr(10))
    fej = fs[1].split(chr(9))
    ix = {k: i for i, k in enumerate(fej)}
    refh = re.compile(r'(?<![\wÀ-ɏ])(?:%s) \d+:\d+' % '|'.join(sorted(set(HU_FORD.values()) | {'Zsolt'}, key=len, reverse=True)))
    valt = []
    for n, l in enumerate(fs, 1):
        if n <= 2 or not l:
            continue
        p = l.split(chr(9))
        sor = dict(zip(fej, p))
        if sor['szotar'] != 'BDB' or sor['jelentes_szam'] != 'teljes' or vedett(sor):
            continue
        uj_hash = hashlib.sha1(forras[sor['strong']].encode('utf-8')).hexdigest()
        if uj_hash == sor['forras_hash']:
            continue
        hu2, ki = csere_forditason(sor['forditas_hu'], sor['strong'], csere)
        # szodiff-kapu: a ket szoveg szavai csak a helyhivatkozasban terhetnek el
        if refh.sub('<R>', sor['forditas_hu']) != refh.sub('<R>', hu2):
            print('SZODIFF KAPU BUKIK', n, sor['strong'])
            sys.exit(6)
        a, b = sor['forditas_hu'].split(), hu2.split()
        szodiff = [(x, y) for x, y in zip(a, b) if x != y]
        if len(a) != len(b):
            print('SZOSZAM VALTOZOTT', n)
            sys.exit(6)
        p[ix['forditas_hu']] = hu2
        p[ix['forras_hash']] = uj_hash
        fs[n - 1] = chr(9).join(p)
        valt.append((n, sor['strong'], sor['allapot'], sor['forras_hash'][:8], uj_hash[:8], szodiff))
    for v in valt:
        print('hash-frissites:', v)
    if ir and valt:
        open(FORD, 'w', encoding='utf-8', newline='').write(chr(10).join(fs))
        print('IRVA')


def meres_tahot():
    """--meres-tahot: a TAHOT-kivonat Zsolt-lefedettsege a Macula MT-tablahoz merve + fejezet-szintu rések.
    Kimenet: mereseredmeny + proveniencia-sor (SEMA: scope | forras | ts)."""
    import datetime
    vt = vers_tabla()
    th, fejezetek = {}, {}
    for l in open(TAHOT, encoding='utf-8').read().split(chr(10))[1:]:
        m = re.match(r'(.+) (\d+):(\d+)' + chr(9), l)
        if m:
            fejezetek.setdefault(m.group(1), set()).add(int(m.group(2)))
            if m.group(1) == 'Zsolt':
                th.setdefault(int(m.group(2)), set()).add(int(m.group(3)))
    van_fej = sum(1 for c in vt if c in th)
    van_vers = sum(len(vt[c] & th.get(c, set())) for c in vt)
    ossz_vers = sum(len(v) for v in vt.values())
    rest = {b: [c for c in range(1, max(cs) + 1) if c not in cs] for b, cs in fejezetek.items()}
    print('Zsolt fejezet: %d/%d; vers: %d/%d (TAHOT a Macula MT-tablahoz merve)' % (van_fej, len(vt), van_vers, ossz_vers))
    print('fejezet-szintu rések konyvenkent:', {b: c for b, c in rest.items() if c})
    print('scope=TAHOT_kivonat Zsolt-lefedettseg vs Macula MT-versek, fejezet-rések minden konyvben | forras=%s + %s | ts=%s' % (TAHOT, MACULA_ZS, datetime.date.today().isoformat()))


def main():
    ir = '--ir' in sys.argv
    if '--meres-tahot' in sys.argv:
        meres_tahot()
        return
    if '--hash-frissit' in sys.argv:
        hash_frissit(ir)
        return
    if '--forditas' in sys.argv:
        forditas_ujrafuttat(ir)
        return
    idx = tahot_idx()
    vt = vers_tabla()
    lista = [l.split('\t') for l in open(LISTA, encoding='utf-8').read().split('\n')[1:] if l]
    kulcsok = {}   # (strong, regi, uj) -> [osztalyok], darab
    for r in lista:
        if r[5] == 'KIZART' or r[3].startswith(NEM_PSI_KONYV):
            continue
        if r[4].startswith('('):
            uj = 'Psa ' + r[4][5:].rstrip('?)')
        else:
            uj = r[4]
        k = (r[1], r[3], uj)
        kulcsok.setdefault(k, []).append(r[5])

    dont = []  # kulcs, osztaly, dontes, ok
    for (st, regi, uj), osz in sorted(kulcsok.items()):
        m = re.match(r'Psa (\d+):(\d+)$', uj)
        c, v = int(m.group(1)), int(m.group(2))
        zs = talal(idx, st, 'Zsolt', c, v)
        o = 'A' if 'A' in osz else ('B' if 'B' in osz else 'R')
        if v > 176:
            d, ok = 'MARAD', 'szokatlan versszam (osszeolvadt alak)'
        elif o == 'A':
            if zs:
                d, ok = 'JAVIT', 'TAHOT Zsolt %d:%s' % (c, ','.join(str(x[2]) for x in zs))
            elif v in vt.get(c, ()):
                d, ok = 'JAVIT', 'DT-F34b: A-maradek, a vers letezik (Macula MT versszamozas Zsolt %d:%d); TAHOT nelkul' % (c, v)
            else:
                d, ok = 'MARAD', 'TAHOT: nincs Zsolt %d:%d+-1 talalat, a vers a Macula-tablaban sem letezik' % (c, v)
        else:
            if not zs:
                d, ok = 'MARAD', 'TAHOT: nincs Zsolt %d:%d+-1 talalat' % (c, v)
            else:
                mas = masutt(idx, st, c, v)
                bk = re.match(r'(\S+) ', regi).group(1)
                if mas:
                    d, ok = 'MARAD', 'Zsolt-talalat van, de mas konyvben is: ' + ','.join(mas)
                else:
                    d, ok = 'JAVIT', 'TAHOT Zsolt %d:%s, mas konyvben nincs' % (c, ','.join(str(x[2]) for x in zs))
        dont.append((st, regi, uj, o, len(osz), d, ok))

    with open('naplok/F34_M2_csere.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(['szocikk_id', 'regi', 'uj', 'osztaly_M0', 'elofordulas_a_listan', 'dontes', 'ok']) + '\n')
        for d in dont:
            f.write('\t'.join(str(x) for x in d) + '\n')
    with open('naplok/F34_M2_maradek.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write('\t'.join(['szocikk_id', 'regi', 'javasolt_uj', 'osztaly_M0', 'elofordulas_a_listan', 'dontes', 'ok']) + '\n')
        for d in dont:
            if d[5] == 'MARAD':
                f.write('\t'.join(str(x) for x in d) + '\n')
    javit = [d for d in dont if d[5] == 'JAVIT']
    from collections import Counter
    print('kulcs:', len(dont), 'JAVIT:', len(javit), 'MARAD:', len(dont) - len(javit))
    print('JAVIT osztaly:', Counter(d[3] for d in javit), 'MARAD osztaly:', Counter(d[3] for d in dont if d[5] == 'MARAD'))
    print('javitott helyek (elofordulas):', sum(d[4] for d in javit))

    # --- forras csere ---
    nyers = open(FORRAS, encoding='utf-8', newline='').read()
    sorok = nyers.split('\n')
    eredeti = list(sorok)
    ujak = {}
    csere_db = 0
    for st, regi, uj, o, n, d, ok in javit:
        talalt = False
        for i, l in enumerate(sorok):
            if not l.startswith(st + '\t'):
                continue
            p = l.split('\t')
            if p[0] != st:
                continue
            pat = re.compile(r'(?<![A-Za-z0-9])' + re.escape(regi) + r'(?!\d)')
            db = len(pat.findall(p[2]))
            if db == 0:
                talalt = True   # mar javitva (ujrafuttatas)
                continue
            if db != n:
                print('ELTERES: %s %s: %d elofordulas a szovegben, %d a listan' % (st, regi, db, n))
                sys.exit(2)
            p[2] = pat.sub(uj, p[2])
            sorok[i] = '\t'.join(p)
            talalt = True
            csere_db += db
        if not talalt:
            print('NINCS SZOCIKK', st)
            sys.exit(2)
    print('forras csere:', csere_db)

    # kapu: csak helyhivatkozas valtozhat
    ref = re.compile(r'(?<![A-Za-z0-9])(?:%s|Psa) \d+:\d+' % '|'.join(sorted(HU, key=len, reverse=True)))
    valt_sor = []
    assert len(sorok) == len(eredeti)
    for i, (a, b) in enumerate(zip(eredeti, sorok)):
        if a != b:
            if ref.sub('<R>', a) != ref.sub('<R>', b):
                print('KAPU BUKIK (nem csak helyhivatkozas valtozott):', i + 1)
                sys.exit(3)
            valt_sor.append(i + 1)
    print('valtozott forras-sor:', len(valt_sor))

    # --- forditasok.tsv ---
    fnyers = open(FORD, encoding='utf-8', newline='').read()
    fs = fnyers.split('\n')
    feje = fs[1].split('\t')
    ix = {k: i for i, k in enumerate(feje)}
    ujforras = {l.split('\t')[0]: l.split('\t')[2] for l in sorok[1:] if l}
    regiforras = {l.split('\t')[0]: l.split('\t')[2] for l in eredeti[1:] if l}
    ford_valt = []
    ford_hash = []
    vedett_hash_elter = []
    ford_eredeti = list(fs)
    for n, l in enumerate(fs, 1):
        if n <= 2 or not l:
            continue
        p = l.split('\t')
        if p[ix['szotar']] != 'BDB' or p[ix['jelentes_szam']] != 'teljes':
            continue
        st = p[ix['strong']]
        if st not in ujforras or ujforras[st] == regiforras[st]:
            continue
        if vedett(dict(zip(feje, p))):
            vedett_hash_elter.append((n, st, p[ix['allapot']]))
            continue
        # a hash a forrasszovegbol
        if hashlib.sha1(regiforras[st].encode('utf-8')).hexdigest() != p[ix['forras_hash']]:
            print('A TAROLT HASH MAR ELTER a regi forrastol:', n, st)
            sys.exit(4)
        hu = p[ix['forditas_hu']]
        hu2 = hu
        for (s2, regi, uj, o, nn, d, ok) in javit:
            if s2 != st:
                continue
            bk, rest = regi.split(' ', 1)
            hk = HU_FORD[bk]
            pat = re.compile(r'(?<![\wÀ-ɏ])' + re.escape(hk + ' ' + rest) + r'(?!\d)')
            db = len(pat.findall(hu2))
            if db:
                hu2 = pat.sub('Zsolt ' + rest, hu2)
                ford_valt.append((n, st, hk + ' ' + rest, 'Zsolt ' + rest, db))
            else:
                ford_valt.append((n, st, hk + ' ' + rest, '(nincs a forditasban)', 0))
        # bajtazonossag kapu: csak helyhivatkozas valtozhat
        refh = re.compile(r'(?<![\wÀ-ɏ])(?:%s) \d+:\d+' % '|'.join(sorted(set(HU_FORD.values()) | {'Zsolt'}, key=len, reverse=True)))
        if refh.sub('<R>', hu) != refh.sub('<R>', hu2):
            print('FORDITAS KAPU BUKIK', n)
            sys.exit(5)
        p[ix['forditas_hu']] = hu2
        p[ix['forras_hash']] = hashlib.sha1(ujforras[st].encode('utf-8')).hexdigest()
        fs[n - 1] = '\t'.join(p)
        ford_hash.append((n, st, p[ix['allapot']]))
    print('forditasok soraban csere:', [x for x in ford_valt if x[4]])
    print('forditasok: nem talalt token:', [x for x in ford_valt if not x[4]])
    print('forditasok hash-frissitett sorok (fajlsor, strong, allapot):', ford_hash)
    print('VEDETT sorok (nem irtam at; a forras valtozott, a tarolt forras_hash elavul -> allapot=elavult javasolt):', vedett_hash_elter)

    if ir and [x for x in ford_valt if x[4]]:
        # a naplo hozzafuzodik (az elozo futasok sorai megmaradnak)
        with open('naplok/F34_M3_forditasok_csere.tsv', 'a', encoding='utf-8', newline='') as f:
            for x in ford_valt:
                if x[4]:
                    f.write('\t'.join(str(y) for y in x) + '\n')

    if ir:
        open(FORRAS, 'w', encoding='utf-8', newline='').write('\n'.join(sorok))
        open(FORD, 'w', encoding='utf-8', newline='').write('\n'.join(fs))
        print('IRVA')
        print('forras sha256:', hashlib.sha256(open(FORRAS, 'rb').read()).hexdigest())


if __name__ == '__main__':
    main()
