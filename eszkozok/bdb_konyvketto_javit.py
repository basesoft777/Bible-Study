#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bdb_konyvketto_javit.py — F240 (LXXBDB) L3: a kettőzött könyvnév a BDB-szövegben („angels Psalm Psa 97:7”).

A forrás (`konkordancia/BDB_teljes_unabridged.tsv`) a BDB könyvjelét (ψ, Jb, Ez …) szóként adja, utána a hivatkozás
saját könyvrövidítése áll; az F34 (`bdb_psi_javit.py`) a rossz könyvet `Psa`-ra javította, a „Psalm Psa …” kettőzést
nyitva hagyta (`naplok/F34_M0_felmeres.md`, „M1-es opció”). A fordítás ezt viszi tovább („angyalok Zsolt Zsolt 97:7”),
és a jelentés-fejléc a kettőzés első tagjánál vág („c. angyalok Zsolt”).

A javítás egy helyen, a forrásban történik (pozícióhoz kötött törlés), és onnan halad tovább:
  1. az angol forrás: a hivatkozás előtti kettőzött könyvszó törlése (a `MARAD` lista kivételével: személynév vagy
     tartalmi szó, pl. „friend of Job Job 2:11”, „in late Psalms Psa 149:1”);
  2. a szakasz-nézet javítótáblája (`adat/bdb_forras_javitas.tsv`) a `bdb_jelolt/forras_javit.py` újrafuttatásával
     magától követi (a `hivatkozas` sorok a TSV ↔ JSON eltérésből jönnek);
  3. a magyar fordítás (`adat/forditasok.tsv` BDB-sorai): ugyanazon a helyen a kettőzött könyvszó törlése, és a
     `forras_hash` frissítése a változott angol szövegre — fizetős újrafordítás nélkül (a minta: `bdb_psi_javit.py`,
     DT-F34c). Csak az a sor kap új hash-t, amelynek régi hash-e a régi angol szövegé volt (friss sor);
  4. `bdb_jelolt/hu_illeszt.py` → `adat/bdb_szakasz_hu.tsv` (a hívó futtatja).
Csere-napló: `naplok/LXXBDB_konyvketto_csere.tsv`. Kapu: `ellenoriz.py` 47. szabály (`kettozes_maradek`).

Futtatás a repó gyökeréből:
    python eszkozok/bdb_konyvketto_javit.py            # száraz: mit cserélne
    python eszkozok/bdb_konyvketto_javit.py --ir       # forrás + javítótábla + fordítás + napló
I/O: split('\\t') / '\\t'.join (csv modul nélkül); írás előtt sor-összevetés.
"""
import argparse
import collections
import hashlib
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORRAS = os.path.join(GYOKER, 'konkordancia', 'BDB_teljes_unabridged.tsv')
FORD = os.path.join(GYOKER, 'adat', 'forditasok.tsv')
NAPLO = os.path.join(GYOKER, 'naplok', 'LXXBDB_konyvketto_csere.tsv')
FJ_ARGS = ['--ts', '2026-10-18', '--ts-heber-sorrend', '2026-11-01', '--ts-atiras', '2026-11-03',
           '--ts-hivatkozott-vers', '2026-11-10', '--ts-tanu', '2026-11-10']

REF = ('Gen|Exod|Lev|Num|Deut|Josh|Judg|Ruth|1Sam|2Sam|1Kin|2Kin|1Chr|2Chr|Ezra|Neh|Esth?|Job|Psa|Prov|Eccl|Song|Isa|'
       'Jer|Lam|Ezek|Dan|Hosea|Joel|Amos|Obad|Jonah|Mic|Nah|Hab|Zeph|Hag|Zech|Mal')
# a könyvjel szóként (a BDB rövidítésének feloldása); a ref előtt a kettőzés első tagja
KONYVSZO = {'Psa': ('Psalm', 'Psalms', 'Paslm', 'Psalmist'), 'Gen': ('Genesis',), 'Ezek': ('Ez',)}
EN_RX = re.compile(r'(?<![\w`^])((?:Psalms?|Paslm|Psalmist|Genesis|Ez|' + REF + r')) (' + REF + r') (\d+:\d+)')
EN_RX_FORDITOTT = re.compile(r'(?<![\w`^])(' + REF + r') (Genesis) (\d+:\d+)')    # „Gen Genesis 32:33”

HU = {'Gen': '1Móz', 'Exod': '2Móz', 'Lev': '3Móz', 'Num': '4Móz', 'Deut': '5Móz', 'Josh': 'Józs', 'Judg': 'Bír', 'Ruth': 'Ruth',
      '1Sam': '1Sám', '2Sam': '2Sám', '1Kin': '1Kir', '2Kin': '2Kir', '1Chr': '1Krón', '2Chr': '2Krón', 'Ezra': 'Ezsd',
      'Neh': 'Neh', 'Est': 'Eszt', 'Esth': 'Eszt', 'Job': 'Jób', 'Psa': 'Zsolt', 'Prov': 'Péld', 'Eccl': 'Préd', 'Song': 'Én',
      'Isa': 'Ézs', 'Jer': 'Jer', 'Lam': 'JSir', 'Ezek': 'Ez', 'Dan': 'Dán', 'Hosea': 'Hós', 'Joel': 'Jóel', 'Amos': 'Ámós',
      'Obad': 'Abd', 'Jonah': 'Jón', 'Mic': 'Mik', 'Nah': 'Náh', 'Hab': 'Hab', 'Zeph': 'Sof', 'Hag': 'Hag', 'Zech': 'Zak',
      'Mal': 'Mal'}
HU_KONYVSZO = {'Zsolt': ('Zsoltár', 'Zsoltárok', 'Zsolt')}

# (Strong, könyv, fejezet:vers) → indok: a hivatkozás előtti szó itt személynév vagy tartalmi szó, nem kettőzés (marad)
MARAD = {
    ('H0453', 'Job', '32:2'): 'személynév: „the young friend of Job” + hivatkozás',
    ('H0464', 'Job', '2:11'): 'személynév: „friend of Job”',
    ('H1419', 'Job', '1:3'): 'személynév a felsorolásban: „Moses …, David …, Job”',
    ('H2344', 'Job', '29:18'): 'személynév: „of days of Job”',
    ('H3224', 'Job', '42:14'): 'személynév: „daughter of Job”',
    ('H3519', 'Job', '19:9'): 'személynév: „of Job”',
    ('H4598', 'Job', '1:20'): 'személynév a felsorolásban (Sámuel, Ezsdrás, a tenger fejedelmei, Jób köntöse)',
    ('H5650', 'Job', '1:8'): 'személynév a felsorolásban („my servant” … Caleb, Job)',
    ('H5707', 'Job', '16:19'): 'személynév: „for Job”',
    ('H6942', 'Job', '1:5'): 'személynév: „sons of Job”',
    ('H1162', 'Ruth', '2:1'): 'személynév: „who married Ruth”',
    ('H5744', 'Ruth', '4:17'): 'személynév: „son of Boaz and Ruth”',
    ('H1954', 'Hosea', '1:1'): 'személynév: „the prophet Hosea”',
    ('H4578', 'Jonah', '2:1'): 'személynév: „fish that swallowed Jonah”',
    ('H2374', 'Amos', '7:12'): 'személynév a látók felsorolásában',
    ('H6602', 'Joel', '1:1'): 'személynév: „father of prophet Joel”',
    ('H2623', 'Psa', '149:1'): 'tartalmi szó: „in late Psalms” (késői zsoltárokban)',
    ('H1420', 'Psa', '71:21'): 'tartalmi szó: „of Psalmist” (a zsoltáríróé)',
}
EZRA_SZEMELY = 'személynév: Ezsdrás (a kortársa, társa, kódexe, ideje)'


def tsv(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = f.read().split('\n')
    return sorok


def sha1(t):
    return hashlib.sha1(t.encode('utf-8')).hexdigest()


def en_jeloltek(strong, t):
    """[(pozíció, régi, új, könyv, c:v, döntés, ok)] egy angol szócikkben."""
    ki = []
    for rx, forditott in ((EN_RX, False), (EN_RX_FORDITOTT, True)):
        for m in rx.finditer(t):
            a, b, cv = m.group(1), m.group(2), m.group(3)
            if forditott:
                konyv, torlendo, poz = a, b, m.start(2) - 1           # „Gen Genesis 32:33” → „Gen 32:33”
                regi = m.group(0)
                uj = '%s %s' % (a, cv)
            else:
                if not (a == b or a in KONYVSZO.get(b, ())):
                    continue
                konyv, torlendo, poz = b, a, m.start(1)
                regi = m.group(0)
                uj = '%s %s' % (b, cv)
            k = (strong, konyv, cv)
            if k in MARAD:
                ki.append((m.start(), regi, uj, konyv, cv, 'marad', MARAD[k]))
            elif konyv == 'Ezra' and a == 'Ezra':
                ki.append((m.start(), regi, uj, konyv, cv, 'marad', EZRA_SZEMELY))
            else:
                ki.append((m.start(), regi, uj, konyv, cv, 'javit',
                           'a könyvjel szóként maradt a hivatkozás előtt (ψ → „Psalm”, „Jb” → „Job” …; F34 M1)'))
    return sorted(ki)


def en_javit(t, jel):
    """A javítandó helyek cseréje hátulról előre."""
    for poz, regi, uj, *_r, d, _ok in sorted(jel, reverse=True):
        if d != 'javit':
            continue
        assert t[poz:poz + len(regi)] == regi, (poz, regi)
        t = t[:poz] + uj + t[poz + len(regi):]
    return t


def hu_rx(konyv_hu):
    szavak = HU_KONYVSZO.get(konyv_hu, (konyv_hu,))
    return re.compile(r'(?<![\w])(%s) (%s) ' % ('|'.join(map(re.escape, szavak)), re.escape(konyv_hu)))


def hu_javit(szoveg, javitando, marad_versek):
    """A magyar szöveg kettőzéseinek törlése. `javitando`: {(HU könyv, c:v)} az angol javítás helyei; ezen felül minden
    „Zsoltár(ok) Zsolt c:v” (a fordító az angol „Psalm 40:18”-ból is kettőzött), a `marad_versek` kivételével."""
    db = 0
    konyvek = {k for k, _ in javitando} | {'Zsolt'}
    for kh in sorted(konyvek):
        rx = re.compile(hu_rx(kh).pattern + r'(\d+:\d+)')
        def csere(m):
            nonlocal db
            cv = m.group(3)
            if (kh, cv) in marad_versek:
                return m.group(0)
            if (kh, cv) in javitando or (kh == 'Zsolt' and m.group(1) in ('Zsoltár', 'Zsoltárok')):
                db += 1
                return '%s %s' % (m.group(2), cv)
            return m.group(0)
        szoveg = rx.sub(csere, szoveg)
    return szoveg, db


def szakasz_hashek(strongok):
    """{(strong, 'sz<n>'): hash} a szakasz-nézet szerint (a bdb_jelolt/szakasz_bemenet.py aktuális állapotából)."""
    sys.path.insert(0, os.path.join(GYOKER, 'eszkozok', 'bdb_jelolt'))
    import importlib
    import szakasz_bemenet as sb
    importlib.reload(sb)
    ki = {}
    for s in strongs_rendezve(strongok):
        szak = sb.szakaszok(s)
        for x in szak or []:
            ki[(s, 'sz%d' % x['sorszam'])] = x['hash']
    return ki


def strongs_rendezve(x):
    return sorted(set(x))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--ir', action='store_true')
    a = ap.parse_args()

    f_sorok = tsv(FORRAS)
    en_uj, naplo, erintett = {}, [], set()
    for i, sor in enumerate(f_sorok):
        if not sor or sor.startswith('Strong_padded'):
            continue
        p = sor.split('\t')
        jel = en_jeloltek(p[0], p[-1])
        for poz, regi, uj, konyv, cv, d, ok in jel:
            naplo.append([p[0], str(poz), regi, uj, d, ok])
        if any(x[5] == 'javit' for x in jel):
            en_uj[i] = (p, en_javit(p[-1], jel), jel)
            erintett.add(p[0])
    nj = sum(1 for x in naplo if x[4] == 'javit')
    print('angol: %d kettőzés javítandó %d szócikkben; marad: %d' % (nj, len(erintett), len(naplo) - nj))

    # a magyar oldal: minden BDB-sor, amelyben kettőzés áll (az angol javítás helyei + a „Zsoltár Zsolt”)
    javitando, marad_versek = collections.defaultdict(set), collections.defaultdict(set)
    for s, poz, regi, uj, d, ok in naplo:
        m = re.search(r'(' + REF + r')\s+(\d+:\d+)$', uj)
        (javitando if d == 'javit' else marad_versek)[s].add((HU[m.group(1)], m.group(2)))
    fsor = tsv(FORD)
    fej = fsor[[i for i, x in enumerate(fsor) if x.startswith('szotar\t')][0]].split('\t')
    ix = {n: i for i, n in enumerate(fej)}
    hu_db, hu_sor = 0, {}
    for i, sor in enumerate(fsor):
        if not sor.startswith('BDB\t'):
            continue
        p = sor.split('\t')
        s = p[ix['strong']]
        uj, db = hu_javit(p[ix['forditas_hu']], javitando.get(s, set()), marad_versek.get(s, set()))
        if db:
            hu_sor[i] = (p, uj)
            hu_db += db
            erintett.add(s)
    print('magyar: %d kettőzés javítandó %d fordítássorban' % (hu_db, len(hu_sor)))
    if not a.ir:
        return

    # hash-ek a csere előtt
    regi_sz = szakasz_hashek(erintett)
    regi_en = {f_sorok[i].split('\t')[0]: sha1(f_sorok[i].split('\t')[-1]) for i in en_uj}
    # 1. angol forrás
    for i, (p, t, _jel) in en_uj.items():
        f_sorok[i] = '\t'.join(p[:-1] + [t])
    with open(FORRAS, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(f_sorok))
    # 2. a szakasz-nézet javítótáblája
    r = subprocess.run([sys.executable, os.path.join(GYOKER, 'eszkozok', 'bdb_jelolt', 'forras_javit.py')] + FJ_ARGS,
                       cwd=GYOKER, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        sys.exit('forras_javit.py hiba:\n' + r.stderr[-2000:])
    uj_sz = szakasz_hashek(erintett)
    uj_en = {p[0]: sha1(t) for p, t, _j in en_uj.values()}
    # 3. fordítás + hash
    hash_db = 0
    for i, sor in enumerate(fsor):
        if not sor.startswith('BDB\t'):
            continue
        p = sor.split('\t')
        s, jsz, h = p[ix['strong']], p[ix['jelentes_szam']], p[ix['forras_hash']]
        if i in hu_sor:
            p[ix['forditas_hu']] = hu_sor[i][1]
        if jsz == 'teljes' and s in regi_en and h == regi_en[s]:
            p[ix['forras_hash']] = uj_en[s]
            hash_db += 1
        elif (s, jsz) in regi_sz and h == regi_sz[(s, jsz)] and uj_sz.get((s, jsz)) not in (None, h):
            p[ix['forras_hash']] = uj_sz[(s, jsz)]
            hash_db += 1
        fsor[i] = '\t'.join(p)
    eredeti = tsv(FORD)
    if len(eredeti) != len(fsor):
        sys.exit('sorszám-eltérés a fordítási táblában; nem írom')
    for x, y in zip(eredeti, fsor):
        if x != y and x.split('\t')[:5] != y.split('\t')[:5]:
            sys.exit('kulcs-eltérés a fordítási táblában; nem írom: %s' % x[:80])
    with open(FORD, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(fsor))
    with open(NAPLO, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/bdb_konyvketto_javit.py --ir (F240 L3) — a kettőzött könyvnév csere-naplója; '
                'dontes: javit (törölve) / marad (személynév vagy tartalmi szó).\n')
        f.write('\t'.join(['strong', 'pozicio', 'regi', 'uj', 'dontes', 'ok']) + '\n')
        for x in naplo:
            f.write('\t'.join(x) + '\n')
    print('kiírva: forrás (%d szócikk), javítótábla, fordítás (%d szöveg, %d hash), napló' % (len(en_uj), len(hu_sor), hash_db))


if __name__ == '__main__':
    main()
