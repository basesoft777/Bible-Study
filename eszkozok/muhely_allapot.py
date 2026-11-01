#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
muhely_allapot.py -- F156 (MUHELY_FEED_STASH): a muhely allapota, ket retegu Feed es Stash.

Uj merot NEM tartalmaz: a meglevo merokat csak olvasva futtatja (ellenoriz.py, ellenorzes/futtat.py,
general.py --cel lexikon a repon kivuli ideiglenes konyvtarba, motivum_hatar.py kimeneti fajlja,
naplok/OLVASOI_blokk_teljesseg_meres.py, kiejtes_szoveg.py, gh pr list), es a generalt/muhely/ ala
irja a harom JSON-t (kimenet reteg; kezzel szerkeszteni tilos):

    feed_belso.json       a muhely reszletesen (talalatok, hibaszovegek, nyitott DT-k, PR-ok)
    feed_nyilvanos.json   a belso FEHERLISTAS szurese (csak a nevesitett mezok mennek at)
    stash.json            a kesz (8/8 zold) motivumok leirasa es statja

A "kesz" a 8 pontos kriteriumbol szamolodik (F156 brief 3.2), NEM a motivumok.tsv `statusz` mezojebol.
Hianyzo vagy hibaval leallo mero soha nem zold ("nincs_mero" / "hiba").

Hasznalat:
    python eszkozok/muhely_allapot.py [--motivum ID ...] [--kimenet DIR] [--nincs-gh]
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
sys.path.insert(0, os.path.join(GYOKER, 'naplok'))

SCRIPT = 'eszkozok/muhely_allapot.py'
ZOLD, PIROS, NINCS, HIBA = 'zold', 'piros', 'nincs_mero', 'hiba'

KRITERIUMOK = [
    (1, 'szabály-ellenőrzés (ellenoriz.py 1–21)'),
    (2, 'CI-ellenőrzés (E2–E29)'),
    (3, 'egyforrású, nulla-diff újragenerálás'),
    (4, 'nincs nyitott jelölt'),
    (5, 'határ: 0 nyitott kérdés'),
    (6, 'olvasói blokkok, kiejtés, fordítás'),
    (7, 'nincs nyitott lektori kérdés'),
    (8, 'nincs nyitott DT / ⛔ feladat'),
]

# a nyilvanos reteg feherlistaja: csak ezek a mezok mennek at
FEHERLISTA_MOTIVUM = ['id', 'cim', 'tema', 'pardes_szint', 'allasfokozat', 'kriteriumok', 'zold_db', 'ossz_db',
                      'nyitott_jelolt_db', 'elvetett_jelolt_db', 'beepitett_jelolt_db', 'stash', 'olvasoi_mondat']
# a `nev` (belso kapunev) es az `allapot` (gepi kod) nem megy at; az `allapot` helyett az olvasoi szoveg
FEHERLISTA_KRITERIUM = ['sorszam', 'szin', 'olvasoi_nev', 'olvasoi_allapot', 'olvasoi_szoveg']
FEHERLISTA_ESEMENY = ['datum', 'motivum', 'olvasoi_esemeny']
FEHERLISTA_STASH = ['cim', 'tema', 'pardes_szint', 'terjedelem_szo', 'kotet', 'elofordulas_osz', 'elofordulas_usz',
                    'kapcsolatok_db', 'forditasi_lefedettseg', 'lektori_kerdes', 'utolso_generalas_commit',
                    'verzio', 'kotet_olvasoi']
FEHERLISTA_TOP = ['_generalt', 'generalva', 'commit', 'rendszer', 'motivumok', 'merok_osszesen', 'heti_tortenes',
                  'elvetett_jeloltek_osszesen']


# ----------------------------------------------------------------------------- segedek

def ido():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')


def prov(mero, motivum):
    return 'scope=motivum:%s | forras=%s | ts=%s' % (motivum, mero, ido())


def futtat(args, env=None, timeout=900):
    e = dict(os.environ)
    e['PYTHONIOENCODING'] = 'utf-8'
    if env:
        e.update(env)
    p = subprocess.run(args, cwd=GYOKER, env=e, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def tsv(utvonal):
    """Fejlecsoros TSV beolvasasa `split('\\t')`-tel (a csv modul nem hasznalhato, CLAUDE.md)."""
    with open(os.path.join(GYOKER, utvonal), encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f]
    sorok = [s for s in sorok if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    ki = []
    for s in sorok[1:]:
        m = s.split('\t')
        m += [''] * (len(fej) - len(m))
        ki.append(dict(zip(fej, m)))
    return ki


def git_commit():
    rc, o, _ = futtat(['git', 'rev-parse', '--short', 'HEAD'])
    return o.strip() if rc == 0 else None


def datum_iso(s):
    """'2026.09.13' vagy '2026-09-13T...' -> '2026-09-13'; egyebkent None."""
    m = re.match(r'(\d{4})[.\-](\d{2})[.\-](\d{2})', (s or '').strip())
    return '%s-%s-%s' % m.groups() if m else None


def uj(allapot, ertek, mero, motivum, reszlet=None, szam=None):
    return {'allapot': allapot, 'ertek': ertek, 'proveniencia': prov(mero, motivum), 'reszlet': reszlet or [],
            'szam': szam or {}}


# --- olvasói megfogalmazás (DT-F156f, jóváhagyva: "Igen, így"); a nyilvános réteg csak ezeket mutatja ---
OLV_NEV = {1: 'Az adatok összhangja', 2: 'A szövegek ellenőrzése', 3: 'Egy szerkesztett forrásból épül',
           4: 'Eldöntendő igehelyek', 5: 'A motívum határa', 6: 'Olvasható lap', 7: 'Lektori átolvasás',
           8: 'Függő munka'}
OLV_ALLAPOT = {ZOLD: 'rendben', PIROS: 'munka van hátra', NINCS: 'még nem vizsgáltuk',
               HIBA: 'az ellenőrzés nem futott le, újra próbáljuk'}
OLV_ZOLD = {1: 'Az adattáblák egymásnak megfelelnek, ellentmondás nincs.',
            2: 'A lap szövegei hibátlanul átmentek az ellenőrzésen.',
            3: 'A lap egyetlen szerkesztett forrásból készül, és újraépítve ugyanaz.',
            4: 'Minden vizsgált igehelyről döntöttünk.',
            5: 'A motívum határáról szóló kérdések megválaszoltak.',
            6: 'A lap minden része magyarázattal, kiejtéssel és fordítással áll.',
            7: 'A lektor minden kérdése lezárult.',
            8: 'Nincs a motívumot érintő megoldatlan kérdés vagy megállt munka.'}
OLV_NINCS = {1: 'Az adatellenőrzés még nem futott.', 2: 'Az ellenőrzés még nem futott.',
             3: 'A lap még nincs egy forrásba rendezve.', 4: 'Az igehelyek vizsgálata még nem indult el.',
             5: 'A határ vizsgálata még nem készült el.', 6: 'A lap még nem készült el.',
             7: 'A lektori átolvasás még nem indult el.', 8: 'A függő munka még nem vizsgált.'}
OLV_ALLAS = {'jelölt': 'Felmerült: igehelyeket gyűjtünk hozzá', 'feldolgozás': 'Feldolgozás alatt',
             'ellenőrzés': 'Ellenőrzés alatt: a lap megvan, a kapuk egy része még nem teljesül',
             'lezárt (stash)': 'Kész, megjelenésre vár', 'kötetben': 'Megjelent a kötetben'}
OLV_KOTET = 'Kötetbe még nincs beosztva'


def olvasoi_kapu(k):
    """A kapu olvasói szövege a mérő számaiból (a belső szavak nélkül)."""
    sz, al, n = k['sorszam'], k['allapot'], k.get('szam', {})
    if al == ZOLD:
        return OLV_ZOLD[sz]
    if al == NINCS:
        return OLV_NINCS[sz]
    if al == HIBA:
        return OLV_ALLAPOT[HIBA] + '.'
    if sz == 1:
        return 'Az adatokban ellentmondás van, javítás alatt.'
    if sz == 2:
        return 'Az ellenőrzés %d hibát talált a szövegekben.' % n.get('n', 0)
    if sz == 3:
        return 'A lap még átállításra vár az új szerkesztési rendre.'
    if sz == 4:
        return '%d igehely vizsgálata folyamatban van.' % n.get('n', 0)
    if sz == 5:
        return '%d kérdés van nyitva arról, mi tartozik a motívumhoz.' % n.get('n', 0)
    if sz == 6:
        reszek = []
        if n.get('kiejtes'):
            reszek.append('%d kiejtés hiányzik' % n['kiejtes'])
        if n.get('fordit'):
            reszek.append('%d rész fordításra vár' % n['fordit'])
        if n.get('blokk'):
            reszek.append('%d rész magyarázat nélkül áll' % n['blokk'])
        return 'A lapon ' + ', '.join(reszek) + '.' if reszek else 'A lap még javításra vár.'
    if sz == 7:
        return '%d lektori kérdés vár válaszra.' % n.get('n', 0)
    return '%d kapcsolódó munka vagy kérdés vár megoldásra.' % n.get('n', 0)


def olvasoi_mondat(feldolgozva, vizsgalat, kizarva, teljesul):
    """`N igehely feldolgozva, M vizsgálat alatt, K kizárva; a nyolc ellenőrzési lépésből Z teljesül.`"""
    reszek = ['%d igehely feldolgozva' % feldolgozva,
              '%d vizsgálat alatt' % vizsgalat if vizsgalat else 'nincs vizsgálat alatt álló igehely']
    if kizarva:
        reszek.append('%d kizárva' % kizarva)
    return ', '.join(reszek) + '; a nyolc ellenőrzési lépésből %d teljesül.' % teljesul


def olvasoi_esemeny(e):
    if e['esemeny'].endswith('beépítve'):
        return '%d igehely bekerült a motívumba' % e['db']
    if e['esemeny'].endswith('elutasítva'):
        return '%d igehelyet kizártunk, mert nem illik a motívum határába' % e['db']
    m = re.search(r'\((v\d+)\)', e['esemeny'])
    return 'A motívum lapja új változatot kapott (%s. változat)' % m.group(1)[1:] if m else 'A motívum lapja frissült'


# ----------------------------------------------------------------------------- mero-futtatasok (egyszer)

def ellenoriz_futas():
    """ellenoriz.py egyszer; blokkokra bontva. Visszaad: (rc, blokkok, hibaszoveg)."""
    rc, o, e = futtat([sys.executable, 'eszkozok/ellenoriz.py'], timeout=600)
    if not o.strip():
        return rc, None, e.strip()[:500]
    blokkok = []
    akt = None
    for sor in o.split('\n'):
        m = re.match(r'\*\*([^*]+)\*\*: (\S+)', sor)
        if m:
            akt = {'nev': m.group(1), 'verdikt': m.group(2), 'szoveg': [sor]}
            blokkok.append(akt)
        elif akt is not None and not sor.startswith('## '):
            akt['szoveg'].append(sor)
    return rc, blokkok, e.strip()[:500]


def kriterium_1(motivum, blokkok, rc, hiba):
    mero = 'ellenoriz.py'
    if blokkok is None:
        return uj(HIBA, 'a mérő nem futott', mero, motivum, [hiba])
    sertesek = [b for b in blokkok if b['verdikt'] not in ('RENDBEN', 'JELENTÉS', 'KÉZI')]
    sajat = [b for b in sertesek if motivum in '\n'.join(b['szoveg'])]
    nem_levezetheto = [b for b in sertesek if not re.search(r'[A-ZÁÉÍÓÖŐÚÜŰ]+-\d{3}', '\n'.join(b['szoveg']))]
    jelentes = [b['nev'] + ': ' + b['verdikt'] for b in blokkok
                if b['verdikt'] in ('JELENTÉS', 'KÉZI') and motivum in '\n'.join(b['szoveg'])]
    if sajat:
        return uj(PIROS, '%d szabály sérül' % len(sajat), mero, motivum, [b['nev'] for b in sajat])
    if nem_levezetheto:
        return uj(PIROS, 'globális sérülés, motívumra nem bontható', mero, motivum,
                  [b['nev'] for b in nem_levezetheto])
    e = uj(ZOLD, '0 HIBA', mero, motivum, jelentes)
    return e


def kriterium_2(motivum):
    mero = 'ellenorzes/futtat.py'
    fajlok = [f for f in ('motivumok/%s.md' % motivum, 'lexikon/%s_TUDOMANYOS.md' % motivum,
                          'lexikon/%s_TORZSCIKK.md' % motivum, 'motivumlog/%s.md' % motivum)
              if os.path.exists(os.path.join(GYOKER, f))]
    if not fajlok:
        return uj(NINCS, 'nincs vizsgálható fájl', mero, motivum)
    rc, o, e = futtat([sys.executable, 'eszkozok/ellenorzes/futtat.py', '--valtozott'] + fajlok)
    if rc == 2 or not o.strip():
        return uj(HIBA, 'futási hiba', mero, motivum, [(e or o).strip()[:500]])
    hiba = 0
    jelentes = 0
    for m in re.finditer(r'^## (E\d+) \(([^)]*)\)', o, re.M):
        h = re.search(r'HIBA: (\d+)', m.group(2))
        j = re.search(r'JELENTES: (\d+)', m.group(2))
        hiba += int(h.group(1)) if h else 0
        jelentes += int(j.group(1)) if j else 0
    allapot = ZOLD if rc == 0 and hiba == 0 else PIROS
    return uj(allapot, '%d HIBA, %d jelentés' % (hiba, jelentes), mero, motivum,
              ['jelentés: %d (nem blokkol)' % jelentes] if jelentes else [], {'n': hiba})


def kriterium_3(motivum):
    mero = 'general.py --cel lexikon (nulla-diff)'
    forras = os.path.join(GYOKER, 'motivumok', motivum + '.md')
    lap = os.path.join(GYOKER, 'lexikon', motivum + '_TUDOMANYOS.md')
    if not os.path.exists(forras):
        return uj(PIROS, 'nincs egyforrású motivumok/%s.md (migrációra vár)' % motivum, mero, motivum)
    if not os.path.exists(lap):
        return uj(PIROS, 'nincs lexikon/%s_TUDOMANYOS.md' % motivum, mero, motivum)
    with open(lap, encoding='utf-8') as f:
        eredeti = f.read().replace('\r', '')
    m = re.search(r'\bts=(\d{4}-\d{2}-\d{2})', eredeti)
    env = {'PARDES_DATUM': m.group(1)} if m else {}
    with tempfile.TemporaryDirectory(prefix='muhely_nulladiff_') as tmp:
        rc, o, e = futtat([sys.executable, 'eszkozok/general.py', '--cel', 'lexikon', '--id', motivum,
                           '--kimenet', tmp], env=env)
        ujlap = os.path.join(tmp, 'lexikon', motivum + '_TUDOMANYOS.md')
        if rc != 0 or not os.path.exists(ujlap):
            return uj(HIBA, 'az újragenerálás nem futott', mero, motivum, [(e or o).strip()[-500:]])
        with open(ujlap, encoding='utf-8') as f:
            uj_szoveg = f.read().replace('\r', '')
    if uj_szoveg == eredeti:
        return uj(ZOLD, 'nulla-diff', mero, motivum)
    a, b = uj_szoveg.split('\n'), eredeti.split('\n')
    eltero = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
    return uj(PIROS, '%d eltérő sor' % eltero, mero, motivum, None, {'n': eltero})


def kriterium_4(motivum, jeloltek):
    mero = 'jeloltek.tsv'
    nyitva = [j for j in jeloltek if j['id'] == motivum and j['dontes'] == 'nyitva']
    reszlet = [j['igehely'] for j in nyitva]  # csak a hely: az indoklás adattábla-tartalom, nem kerül a Feedbe
    return uj(PIROS if nyitva else ZOLD, '%d nyitott jelölt' % len(nyitva), mero, motivum, reszlet, {'n': len(nyitva)})


def kriterium_5(motivum):
    mero = 'motivum_hatar.py'
    ut = os.path.join(GYOKER, 'naplok', 'HATAR_%s.md' % motivum)
    if not os.path.exists(ut):
        return uj(NINCS, 'nincs naplok/HATAR_%s.md' % motivum, mero, motivum)
    with open(ut, encoding='utf-8') as f:
        t = f.read()
    szamok = [int(x) for x in re.findall(r'\*\*(\d+) kérdés\.\*\*', t)]
    if not szamok:
        return uj(HIBA, 'a határ-fájlban nincs kérdésszám', mero, motivum)
    cimek = re.findall(r'^\*\*(K\d+) — ', t, re.M)  # csak a jelölők: a kérdés szövege nem kerül a Feedbe
    n = sum(szamok)
    return uj(PIROS if n else ZOLD, '%d nyitott kérdés' % n, mero, motivum, cimek, {'n': n})


def kriterium_6(motivum):
    mero = 'OLVASOI_blokk_teljesseg_meres.py + kiejtes_szoveg.py'
    ut = os.path.join(GYOKER, 'lexikon', motivum + '_TUDOMANYOS.md')
    if not os.path.exists(ut):
        return uj(NINCS, 'nincs lexikon-lap', mero, motivum)
    try:
        import OLVASOI_blokk_teljesseg_meres as OB
        import kiejtes_szoveg as KSZ
        ki, _ = OB.meres(ut)
        blokk_hiany = [(i, s) for i, s, van, ok in ki if van == 'nincs' and ok == 'HIÁNY']
        with open(ut, encoding='utf-8') as f:
            szoveg = f.read()
        kiejtes_hiany = KSZ.elemez(szoveg)
    except Exception as ex:  # noqa: BLE001 -- a mero hibaja "hiba", nem nulla
        return uj(HIBA, 'a mérő hibával állt le', mero, motivum, [repr(ex)[:300]])
    fordit = szoveg.replace('\r', '').count('*(fordításra vár)*')
    n_blokk = len(ki)
    van = sum(1 for x in ki if x[2] == 'van')
    reszlet = ['blokk-hiány: sor %d %s' % (i, s[:80]) for i, s in blokk_hiany]
    reszlet += ['kiejtés-hiány: sor %s — %s' % (k[0], k[3]) for k in kiejtes_hiany]
    zold = not blokk_hiany and not kiejtes_hiany and fordit == 0
    ertek = '%d/%d blokk fedett (%d bevezetővel), kiejtés-hiány %d, fordításra vár %d' % (
        n_blokk - len(blokk_hiany), n_blokk, van, len(kiejtes_hiany), fordit)
    e = uj(ZOLD if zold else PIROS, ertek, mero, motivum, reszlet)
    e['szam'] = {'kiejtes': len(kiejtes_hiany), 'fordit': fordit, 'blokk': len(blokk_hiany)}
    e['mertek'] = {'blokk_osszes': n_blokk, 'blokk_hiany': len(blokk_hiany), 'kiejtes_hiany': len(kiejtes_hiany),
                   'fordításra_var': fordit}
    return e


def kriterium_7(motivum):
    mero = 'lektori kérdések (naplok/LEKTOR_<ID>.tsv)'
    ut = os.path.join(GYOKER, 'naplok', 'LEKTOR_%s.tsv' % motivum)
    if not os.path.exists(ut):
        return uj(NINCS, 'nincs mérő (a lektor-felület tárolója még nem létezik; DT-F156c)', mero, motivum)
    try:
        sorok = tsv('naplok/LEKTOR_%s.tsv' % motivum)
    except Exception as ex:  # noqa: BLE001
        return uj(HIBA, 'a lektori tábla nem olvasható', mero, motivum, [repr(ex)[:300]])
    nyitott = [s for s in sorok if s.get('allapot', 'nyitva') in ('nyitva', 'nyitott')]
    return uj(PIROS if nyitott else ZOLD, '%d nyitott lektori kérdés' % len(nyitott), mero, motivum, None,
              {'n': len(nyitott)})


# ----------------------------------------------------------------------------- feladatok, DT-k

def feladat_fejlecek():
    """A gyoker *_BRIEF.md fajlok elso blokkja (`---` kozott) -> {szam: {kulcs: ertek}}."""
    ki = {}
    for nev in sorted(os.listdir(GYOKER)):
        if not nev.endswith('_BRIEF.md'):
            continue
        with open(os.path.join(GYOKER, nev), encoding='utf-8') as f:
            sorok = f.read().split('\n')
        if not sorok or sorok[0].strip() != '---':
            continue
        fej = {}
        for s in sorok[1:]:
            if s.strip() == '---':
                break
            k, _, v = s.partition(':')
            fej[k.strip()] = v.strip()
        if fej.get('feladat', '').isdigit():
            fej['_fajl'] = nev
            ki[int(fej['feladat'])] = fej
    return ki


def nyitott_dt():
    """DONTESEK.md tablasorai: azonosito, feladatszam, allapot (🟡 nyitott), kerdes eleje."""
    ki = []
    with open(os.path.join(GYOKER, 'DONTESEK.md'), encoding='utf-8') as f:
        for s in f:
            if not s.startswith('| DT'):
                continue
            m = [x.strip() for x in s.split('|')]
            if len(m) < 8:
                continue
            szam = re.match(r'#(\d+)', m[2])
            ki.append({'id': m[1], 'feladat': int(szam.group(1)) if szam else None, 'cim': m[2],
                       'kerdes': m[3][:300], 'nyitott': '🟡' in m[6]})
    return ki


def kriterium_8(motivum, fejlecek, dt_lista):
    mero = 'feladatok.py + DONTESEK.md'
    erintett = {n: f for n, f in fejlecek.items() if motivum in f.get('ir', '')}
    reszlet = []
    for n, f in sorted(erintett.items()):
        if f.get('allapot') == 'megallt':
            reszlet.append('#%d ⛔ megállt feladat' % n)
    for d in dt_lista:
        if d['nyitott'] and d['feladat'] in erintett:
            reszlet.append('%s 🟡 (#%d)' % (d['id'], d['feladat']))
    e = uj(PIROS if reszlet else ZOLD, '%d nyitott ⛔/🟡' % len(reszlet), mero, motivum, reszlet, {'n': len(reszlet)})
    e['feladatok'] = [{'feladat': n, 'allapot': f.get('allapot', ''), 'cim': f.get('cim', '')[:120]}
                      for n, f in sorted(erintett.items())]
    return e


def nyitott_prok(motivumok, nincs_gh):
    """gh pr list (csak olvasas): motivum -> [PR]. Hiba eseten (None, hibaszoveg)."""
    if nincs_gh:
        return None, 'kihagyva (--nincs-gh)'
    try:
        rc, o, e = futtat(['gh', 'pr', 'list', '--state', 'open', '--limit', '100', '--json',
                           'number,title,url,files'], timeout=120)
        if rc != 0:
            return None, (e or o).strip()[:300]
        prok = json.loads(o)
    except Exception as ex:  # noqa: BLE001
        return None, repr(ex)[:300]
    ki = {m: [] for m in motivumok}
    for p in prok:
        utak = ' '.join(f.get('path', '') for f in p.get('files', []))
        for m in motivumok:
            if m in utak:
                ki[m].append({'szam': p['number'], 'cim': p['title'], 'url': p['url']})
    return ki, None


# ----------------------------------------------------------------------------- stash, tortenes

def usz_konyvek():
    sorok = tsv('konkordancia/Konyv_normalizalo_tabla.tsv')
    lista = [s['Magyar rövidítés'] for s in sorok]
    for i, s in enumerate(sorok):
        if s['STEPBible-rövidítés'] == 'Mat':
            return set(lista[i:])
    return set()


def stash_adat(m, kriteriumok, elofordulasok, kapcsolatok, usz, commit_lapon):
    sajat = [e for e in elofordulasok if e['id'] == m['id']]
    osz = sum(1 for e in sajat if e['igehely'].split(' ')[0] not in usz)
    fordit = sum(1 for e in sajat if e['jelentes_hu'].strip())
    szavak = None
    lap = os.path.join(GYOKER, 'lexikon', m['id'] + '_TUDOMANYOS.md')
    if os.path.exists(lap):
        with open(lap, encoding='utf-8') as f:
            szavak = len(f.read().split())
    k6 = kriteriumok['6']
    return {
        'cim': m['cim'], 'tema': m['tema'], 'pardes_szint': m['pardes_szint'],
        'terjedelem_szo': szavak,
        'kotet': None, 'kotet_megjegyzes': 'nincs kötet-adat (DT-F156d)', 'kotet_olvasoi': OLV_KOTET,
        'elofordulas_osz': osz, 'elofordulas_usz': len(sajat) - osz,
        'kapcsolatok_db': sum(1 for k in kapcsolatok if m['id'] in (k['id_a'], k['id_b'])),
        'forditasi_lefedettseg': round(fordit / len(sajat), 3) if sajat else None,
        'forditasra_var_jeloles': (k6.get('mertek') or {}).get('fordításra_var'),
        'lektori_kerdes': None if kriteriumok['7']['allapot'] == NINCS else kriteriumok['7']['ertek'],
        'utolso_generalas_commit': commit_lapon,
        'verzio': m['statusz_verzio'],
    }


def heti_tortenes(jeloltek, motivumok, nap=7):
    ma = datetime.date.today()
    tol = ma - datetime.timedelta(days=nap)
    esemenyek = {}
    for j in jeloltek:
        d = datum_iso(j.get('datum'))
        if d and tol.isoformat() <= d <= ma.isoformat():
            kulcs = (d, j['id'], j['dontes'])
            esemenyek[kulcs] = esemenyek.get(kulcs, 0) + 1
    ki = [{'datum': d, 'motivum': mid, 'esemeny': 'jelölt-döntés: %s' % dontes, 'db': n}
          for (d, mid, dontes), n in esemenyek.items()]
    for m in motivumok:
        d = datum_iso(m.get('statusz_datum'))
        if d and tol.isoformat() <= d <= ma.isoformat():
            ki.append({'datum': d, 'motivum': m['id'], 'esemeny': 'állapot: %s (%s)' % (m['statusz'],
                                                                                         m['statusz_verzio']),
                       'db': 1})
    return sorted(ki, key=lambda x: x['datum'], reverse=True)


def allasfokozat(m, zold_db, ossz_db, kriteriumok):
    if zold_db == ossz_db:
        return 'lezárt (stash)'
    if m['statusz'] == 'feldolgozás alatt':
        return 'feldolgozás'
    return 'ellenőrzés'


# ----------------------------------------------------------------------------- fo

def feherlista(d, kulcsok):
    return {k: d[k] for k in kulcsok if k in d}


def nyilvanos(belso):
    ki = feherlista(belso, FEHERLISTA_TOP)
    ki['_generalt'] = belso['_generalt'].replace('feed_belso', 'feed_nyilvanos') + ' (a belső réteg fehérlistás szűrése)'
    ki['heti_tortenes'] = [feherlista(x, FEHERLISTA_ESEMENY) for x in belso['heti_tortenes']]
    ki['motivumok'] = []
    for m in belso['motivumok']:
        e = feherlista(m, FEHERLISTA_MOTIVUM)
        e['allasfokozat'] = m['allasfokozat_olvasoi']
        e['kriteriumok'] = [feherlista(k, FEHERLISTA_KRITERIUM) for k in m['kriteriumok']]
        if m.get('stash'):
            e['stash'] = feherlista(m['stash'], FEHERLISTA_STASH)
        ki['motivumok'].append(e)
    return ki


def main():
    ap = argparse.ArgumentParser(description='F156: a műhely állapota (Feed/Stash)')
    ap.add_argument('--motivum', nargs='+', help='motívum-ID-k (alapból mind)')
    ap.add_argument('--kimenet', default=os.path.join(GYOKER, 'generalt', 'muhely'))
    ap.add_argument('--nincs-gh', action='store_true', help='a gh pr list kihagyása')
    a = ap.parse_args()

    motivumok = tsv('adat/motivumok.tsv')
    if a.motivum:
        motivumok = [m for m in motivumok if m['id'] in a.motivum]
    ids = [m['id'] for m in motivumok]
    jeloltek = tsv('adat/jeloltek.tsv')
    elofordulasok = tsv('adat/elofordulasok.tsv')
    kapcsolatok = tsv('adat/motivum_kapcsolatok.tsv')
    usz = usz_konyvek()
    fejlecek = feladat_fejlecek()
    dt_lista = nyitott_dt()
    rc1, blokkok, hiba1 = ellenoriz_futas()
    prok, pr_hiba = nyitott_prok(ids, a.nincs_gh)

    ki = []
    for m in motivumok:
        mid = m['id']
        print('mérés: %s' % mid, file=sys.stderr)
        krit = {
            '1': kriterium_1(mid, blokkok, rc1, hiba1), '2': kriterium_2(mid), '3': kriterium_3(mid),
            '4': kriterium_4(mid, jeloltek), '5': kriterium_5(mid), '6': kriterium_6(mid),
            '7': kriterium_7(mid), '8': kriterium_8(mid, fejlecek, dt_lista),
        }
        lista = []
        for sz, nev in KRITERIUMOK:
            k = dict(krit[str(sz)])
            k['sorszam'], k['nev'] = sz, nev
            k['szin'] = {ZOLD: 'zold', PIROS: 'piros', NINCS: 'szurke', HIBA: 'hiba'}[k['allapot']]  # csak a szinezeshez
            k['olvasoi_nev'] = OLV_NEV[sz]
            k['olvasoi_allapot'] = OLV_ALLAPOT[k['allapot']]
            k['olvasoi_szoveg'] = olvasoi_kapu(k)
            lista.append(k)
        zold_db = sum(1 for k in lista if k['allapot'] == ZOLD)
        sajat_j = [j for j in jeloltek if j['id'] == mid]
        elv = [j for j in sajat_j if j['dontes'].startswith('elutas')]
        rc, o, _ = futtat(['git', 'log', '-1', '--format=%h', '--', 'lexikon/%s_TUDOMANYOS.md' % mid])
        lapon = o.strip() if rc == 0 and o.strip() else None
        st = stash_adat(m, krit, elofordulasok, kapcsolatok, usz, lapon)
        e = {
            'id': mid, 'cim': m['ui_cimke'] or m['cim'], 'tema': m['tema'], 'pardes_szint': m['pardes_szint'],
            'allasfokozat': allasfokozat(m, zold_db, len(lista), krit),
            'allasfokozat_olvasoi': OLV_ALLAS[allasfokozat(m, zold_db, len(lista), krit)],
            'olvasoi_mondat': olvasoi_mondat(st['elofordulas_osz'] + st['elofordulas_usz'],
                                             sum(1 for j in sajat_j if j['dontes'] == 'nyitva'), len(elv), zold_db),
            'tsv_statusz': m['statusz'], 'tsv_statusz_eltérés': (m['statusz'] == 'publikálható') != (zold_db == 8),
            'kriteriumok': lista, 'zold_db': zold_db, 'ossz_db': len(lista),
            'nyitott_jelolt_db': sum(1 for j in sajat_j if j['dontes'] == 'nyitva'),
            'elvetett_jelolt_db': len(elv),
            'beepitett_jelolt_db': sum(1 for j in sajat_j if j['dontes'].startswith('beépít')),
            'stash': st if zold_db == len(lista) else None,
            # --- csak belso ---
            'stash_jelolt': st,
            'elvetett_jeloltek': [j['igehely'] for j in elv],
            'nyitott_pr': (prok or {}).get(mid) if prok is not None else None,
        }
        ki.append(e)

    commit = git_commit()
    belso = {
        '_generalt': '%s — GENERÁLT, kézzel szerkeszteni tilos; feed_belso.json (belső réteg)' % SCRIPT,
        'generalva': ido(), 'commit': commit, 'rendszer': 'PaRDeS műhely — Feed/Stash (F156)',
        'merok_osszesen': {
            'motivum_db': len(ki),
            'kesz_db': sum(1 for x in ki if x['zold_db'] == x['ossz_db']),
            'kapu_zold': sum(x['zold_db'] for x in ki), 'kapu_ossz': sum(x['ossz_db'] for x in ki),
            'nyitott_jelolt': sum(x['nyitott_jelolt_db'] for x in ki),
        },
        'elvetett_jeloltek_osszesen': sum(x['elvetett_jelolt_db'] for x in ki),
        'heti_tortenes': [dict(x, olvasoi_esemeny=olvasoi_esemeny(x)) for x in heti_tortenes(jeloltek, motivumok)],
        'pr_hiba': pr_hiba,
        'ellenoriz_hiba': hiba1 or None,
        'motivumok': ki,
    }
    ny = nyilvanos(belso)
    stash = {
        '_generalt': '%s — GENERÁLT, kézzel szerkeszteni tilos; stash.json' % SCRIPT,
        'generalva': belso['generalva'], 'commit': commit,
        'kritérium': 'mind a 8 pont zöld (F156 3.2); a kötet-hozzárendelés nincs adatban (DT-F156d)',
        'tetelek': [dict(feherlista(x['stash_jelolt'], FEHERLISTA_STASH), id=x['id']) for x in ki
                    if x['zold_db'] == x['ossz_db']],
        'kesz_db': belso['merok_osszesen']['kesz_db'],
    }

    os.makedirs(a.kimenet, exist_ok=True)
    for nev, tartalom in (('feed_belso.json', belso), ('feed_nyilvanos.json', ny), ('stash.json', stash)):
        with open(os.path.join(a.kimenet, nev), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(tartalom, f, ensure_ascii=False, indent=1, sort_keys=False)
            f.write('\n')
    print('kész: %d motívum, %d kész (8/8); kimenet: %s' % (len(ki), stash['kesz_db'], a.kimenet))


if __name__ == '__main__':
    main()
