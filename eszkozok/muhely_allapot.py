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
    stash.json            a kesz (minden kapu zold) motivumok leirasa es statja

A "kesz" a 9 pontos kriteriumbol szamolodik (F156 brief 3.2; a 9. kapu, az olvasoi kapu: DT-F156k),
NEM a motivumok.tsv `statusz` mezojebol.
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
    (6, 'olvasói blokkok, kiejtés, fordítás, 1/a próza'),
    (7, 'a lektori kör lefutott'),
    (8, 'nincs nyitott DT / ⛔ feladat'),
    (9, 'olvasói kapu: 0 BUKÁS + a felhasználó vizuális átnézése'),
]
SZAMSZO = {8: 'nyolc', 9: 'kilenc', 10: 'tíz'}
KAPU_SZO = SZAMSZO[len(KRITERIUMOK)]

# a nyilvanos reteg feherlistaja: csak ezek a mezok mennek at
FEHERLISTA_MOTIVUM = ['id', 'cim', 'tema', 'pardes_szint', 'allasfokozat', 'lanc', 'teljesult_lepesek', 'zold_db',
                      'ossz_db', 'elvetett_jelolt_db', 'beepitett_jelolt_db', 'stash', 'olvasoi_mondat']
# a `nev` (belso kapunev) es az `allapot` (gepi kod) nem megy at; az `allapot` helyett az olvasoi szoveg
# a nyilvános rétegben csak a teljesült lépés szerepel (olvasói név és szöveg)
FEHERLISTA_KRITERIUM = ['sorszam', 'olvasoi_nev', 'olvasoi_szoveg']
FEHERLISTA_ESEMENY = ['datum', 'motivum', 'olvasoi_esemeny']
FEHERLISTA_STASH = ['cim', 'tema', 'pardes_szint', 'negativ_kriterium', 'folerendelt_fogalom', 'terjedelem_szo', 'kotet', 'elofordulas_osz', 'elofordulas_usz',
                    'kapcsolatok_db', 'forditasi_lefedettseg', 'utolso_generalas_commit',
                    'verzio', 'kotet_olvasoi', 'kiadas_allapot']
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
           8: 'Függő munka', 9: 'Olvasói átnézés'}
OLV_ALLAPOT = {ZOLD: 'rendben', PIROS: 'munka van hátra', NINCS: 'még nem vizsgáltuk',
               HIBA: 'az ellenőrzés nem futott le, újra próbáljuk'}
OLV_ZOLD = {1: 'Az adattáblák egymásnak megfelelnek.',
            2: 'A lap szövegei átmentek az ellenőrzésen.',
            3: 'A lap egyetlen szerkesztett forrásból készül, és újraépítve ugyanaz.',
            4: 'Minden vizsgált igehelyről döntöttünk.',
            5: 'A motívum határa tisztázott.',
            6: 'A lap minden része magyarázattal, kiejtéssel és fordítással áll, minden igehely alatt magyarázattal.',
            7: 'A lektori átolvasás lezárult.',
            8: 'A motívum körül minden kérdés rendezett.',
            9: 'A lapot gépi és emberi szemmel is átolvastuk.'}
OLV_NINCS = {1: 'Az adatellenőrzés még nem futott.', 2: 'Az ellenőrzés még nem futott.',
             3: 'A lap még nincs egy forrásba rendezve.', 4: 'Az igehelyek vizsgálata még nem indult el.',
             5: 'A határ vizsgálata még nem készült el.', 6: 'A lap még nem készült el.',
             7: 'A lektori átolvasás még nem indult el.', 8: 'A függő munka még nem vizsgált.',
             9: 'A lap olvasói átnézése még nem indult el.'}
OLV_ALLAS = {'jelölt': 'Felmerült', 'feldolgozás': 'Feldolgozás alatt',
             'ellenőrzés': 'Ellenőrzés alatt',
             'lezárt (stash)': 'Kész', 'kötetben': 'Megjelent a kötetben'}
OLV_KOTET = 'Kötetbe még nincs beosztva'


def olvasoi_kapu(k):
    """A kapu olvasói szövege a mérő számaiból (a belső szavak nélkül)."""
    sz, al, n = k['sorszam'], k['allapot'], k.get('szam', {})
    if al == ZOLD:
        if sz == 7 and n.get('kiadas2'):
            return OLV_ZOLD[7] + ' 2. kiadáshoz: %d kérdés.' % n['kiadas2']
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
        if n.get('proza1a'):
            reszek.append('%d igehely alatt hiányos a magyarázat' % n['proza1a'])
        return 'A lapon ' + ', '.join(reszek) + '.' if reszek else 'A lap még javításra vár.'
    if sz == 7:
        s = '%d lektori kérdés vár válaszra.' % n.get('n', 0)
        return s + ' 2. kiadáshoz: %d kérdés.' % n['kiadas2'] if n.get('kiadas2') else s
    if sz == 9:
        reszek = ['%d olvasói hiba van a lapon' % n['n']] if n.get('n') else []
        if not n.get('atnezes'):
            reszek.append('a lap emberi átnézése még hátravan')
        return (', '.join(reszek) + '.').capitalize() if reszek else 'A lap még javításra vár.'
    return '%d kapcsolódó munka vagy kérdés vár megoldásra.' % n.get('n', 0)


def olvasoi_mondat(feldolgozva, vizsgalat, kizarva, teljesul):
    """`N igehely feldolgozva, M vizsgálat alatt, K kizárva; a kilenc ellenőrzési lépésből Z teljesül.`"""
    reszek = ['%d igehely feldolgozva' % feldolgozva,
              '%d vizsgálat alatt' % vizsgalat if vizsgalat else 'nincs vizsgálat alatt álló igehely']
    if kizarva:
        reszek.append('%d kizárva' % kizarva)
    return ', '.join(reszek) + '; a %s ellenőrzési lépésből %d teljesül.' % (KAPU_SZO, teljesul)


LANC = ['Felmerült', 'Feldolgozás', 'Ellenőrzés', 'Kész', 'Kötetben']
LANC_FOK = {'jelölt': 0, 'feldolgozás': 1, 'ellenőrzés': 2, 'lezárt (stash)': 3, 'kötetben': 4}


def olvasoi_mondat_nyilvanos(feldolgozva, kizarva, teljesul):
    """Csak előrehaladás: `N igehely feldolgozva, K kizárva; a kilenc ellenőrzési lépésből Z teljesül.`"""
    reszek = ['%d igehely feldolgozva' % feldolgozva]
    if kizarva:
        reszek.append('%d kizárva' % kizarva)
    return ', '.join(reszek) + '; a %s ellenőrzési lépésből %d teljesül.' % (KAPU_SZO, teljesul)


def lanc(fok):
    """Az állapotlánc: a motívum melyik fokon áll (kész / aktuális / következő, semleges szavakkal)."""
    i = LANC_FOK[fok]
    return [{'nev': n, 'allapot': 'kesz' if k < i else 'aktualis' if k == i else 'kovetkezo'}
            for k, n in enumerate(LANC)]


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


def blokkolo_jelolt(j):
    """DT-F156b (a): csak a motívum saját előfordulás-jelöltje blokkol; a motívumközi nyitva marad, tájékoztatás."""
    return j['dontes'] == 'nyitva' and j.get('jelolt_tipus', '') != 'motivumkozi'


def kriterium_4(motivum, jeloltek):
    mero = 'jeloltek.tsv'
    sajat = [j for j in jeloltek if j['id'] == motivum and j['dontes'] == 'nyitva']
    nyitva = [j for j in sajat if blokkolo_jelolt(j)]
    kozi = [j for j in sajat if not blokkolo_jelolt(j)]
    # csak a hely: az indoklás adattábla-tartalom, nem kerül a Feedbe
    reszlet = [j['igehely'] for j in nyitva] + ['tájékoztató (motívumközi, nem blokkol): ' + j['igehely'] for j in kozi]
    e = uj(PIROS if nyitva else ZOLD, '%d nyitott jelölt, %d motívumközi (tájékoztató)' % (len(nyitva), len(kozi)),
           mero, motivum, reszlet, {'n': len(nyitva), 'kozi': len(kozi)})
    return e


def lektor_sorok(motivum):
    """naplok/LEKTOR_<ID>.tsv sorai (F157); None, ha a fájl nincs. Hiba esetén kivétel."""
    ut = os.path.join(GYOKER, 'naplok', 'LEKTOR_%s.tsv' % motivum)
    if not os.path.exists(ut):
        return None
    return tsv('naplok/LEKTOR_%s.tsv' % motivum)


def lektor_zart(sor):
    return sor.get('allapot', '').strip() == 'megvalaszolva'


def masodik_kiadas(sor):
    """A `/kiadas` kimenetéből jövő kérdések (forras=lektor és proza_lefedettseg) a következő kiadáshoz tartoznak: nem blokkolnak."""
    return sor.get('forras', '').strip() in ('lektor', 'proza_lefedettseg')


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
    # a modelles K-kérdések a lektori táblában is szerepelnek (kerdes_id: hatar:<ID>:mK<n>); a megválaszolt zárt
    try:
        sorok = lektor_sorok(motivum) or []
    except Exception as ex:  # noqa: BLE001
        return uj(HIBA, 'a lektori tábla nem olvasható', mero, motivum, [repr(ex)[:300]])
    zart = {s['kerdes_id'].rsplit(':m', 1)[-1] for s in sorok if s.get('kerdes_id', '').startswith('hatar:%s:m' % motivum)
            and lektor_zart(s)}
    megvalaszolt = [c for c in cimek if c in zart]
    n -= len(megvalaszolt)
    cimek = [c for c in cimek if c not in zart]
    # F178.1: a határ-frissesség kapuja (HIBA) — a modelles rész a mai beépített sorokon készült-e
    # (`ellenoriz.hatar_frissesseg`, SORÁLLAPOT-jel). Nem friss modelles résszel a lap nem adható ki.
    import ellenoriz as ELL
    friss, friss_szoveg = ELL.hatar_frissesseg(os.path.join(GYOKER, 'adat'), motivum)
    if friss != 'friss':
        return uj(PIROS, 'a határ-ellenőrzés nem a mai adaton készült (%s)' % friss_szoveg, mero, motivum, cimek,
                  {'n': n, 'frissesseg': friss})
    return uj(PIROS if n else ZOLD, '%d nyitott kérdés' % n, mero, motivum, cimek, {'n': n})


def kiejtes_szuro(hianyok):
    """DT-F156b (b): a generált Jelmagyarázat szótári rövidítései nem kiejtés-kötelesek."""
    return [h for h in hianyok if not str(h[1]).startswith('Jelmagyarázat')]


def kriterium_6(motivum):
    mero = 'OLVASOI_blokk_teljesseg_meres.py + kiejtes_szoveg.py + proza_1a.py'
    ut = os.path.join(GYOKER, 'lexikon', motivum + '_TUDOMANYOS.md')
    if not os.path.exists(ut):
        return uj(NINCS, 'nincs lexikon-lap', mero, motivum)
    try:
        import OLVASOI_blokk_teljesseg_meres as OB
        import kiejtes_szoveg as KSZ
        import proza_1a as P1A
        ki, _ = OB.meres(ut)
        blokk_hiany = [(i, s) for i, s, van, ok in ki if van == 'nincs' and ok == 'HIÁNY']
        with open(ut, encoding='utf-8') as f:
            szoveg = f.read()
        kiejtes_hiany = kiejtes_szuro(KSZ.elemez(szoveg))
        # DT-F1Aa (b): az 1/a minden igehelye alatt kerek próza és „Funkció:” sor (mérce: az arany lap)
        proza_hiany = [x for x in P1A.meres(szoveg) if not (x[1] == 'kerek' and x[2] == 'van')]
    except Exception as ex:  # noqa: BLE001 -- a mero hibaja "hiba", nem nulla
        return uj(HIBA, 'a mérő hibával állt le', mero, motivum, [repr(ex)[:300]])
    fordit = szoveg.replace('\r', '').count('*(fordításra vár)*')
    n_blokk = len(ki)
    van = sum(1 for x in ki if x[2] == 'van')
    reszlet = ['blokk-hiány: sor %d %s' % (i, s[:80]) for i, s in blokk_hiany]
    reszlet += ['kiejtés-hiány: sor %s — %s' % (k[0], k[3]) for k in kiejtes_hiany]
    reszlet += ['1/a: %s — próza %s, Funkció %s' % (x[0], x[1], x[2]) for x in proza_hiany]
    zold = not blokk_hiany and not kiejtes_hiany and fordit == 0 and not proza_hiany
    ertek = '%d/%d blokk fedett (%d bevezetővel), kiejtés-hiány %d, fordításra vár %d, 1/a hiányos igehely %d' % (
        n_blokk - len(blokk_hiany), n_blokk, van, len(kiejtes_hiany), fordit, len(proza_hiany))
    e = uj(ZOLD if zold else PIROS, ertek, mero, motivum, reszlet)
    e['szam'] = {'kiejtes': len(kiejtes_hiany), 'fordit': fordit, 'blokk': len(blokk_hiany),
                 'proza1a': len(proza_hiany)}
    e['mertek'] = {'blokk_osszes': n_blokk, 'blokk_hiany': len(blokk_hiany), 'kiejtes_hiany': len(kiejtes_hiany),
                   'fordításra_var': fordit, 'proza_1a_hiany': len(proza_hiany)}
    return e


def kriterium_7(motivum):
    mero = 'lektori kérdések (naplok/LEKTOR_<ID>.tsv)'
    try:
        sorok = lektor_sorok(motivum)
    except Exception as ex:  # noqa: BLE001
        return uj(HIBA, 'a lektori tábla nem olvasható', mero, motivum, [repr(ex)[:300]])
    if sorok is None:
        return uj(NINCS, 'nincs naplok/LEKTOR_%s.tsv (a lektori kérdések még nincsenek generálva)' % motivum, mero,
                  motivum)
    # DT-F123j (a lépésszám-szabály): a kapu azt mondja ki, hogy a lektori kör lefutott; a megválaszolatlan lektori
    # kérdés a 2. kiadás bemenete, nem gátol
    nyitott = [s for s in sorok if not lektor_zart(s)]
    kiadas2 = [s for s in nyitott if masodik_kiadas(s)]
    return uj(ZOLD, 'a lektori kör lefutott: %d megválaszolt, a 2. kiadás bemenete %d' % (
              len(sorok) - len(nyitott), len(nyitott)), mero, motivum,
              ['2. kiadáshoz: ' + s.get('kerdes_id', '') for s in nyitott],
              {'n': 0, 'kiadas2': len(nyitott)})


ATNEZES_TABLA = 'adat/lap_atnezesek.tsv'


def lap_commit(motivum):
    """A lap utolsó változásának commitja (teljes hash); None, ha nincs a git-történetben."""
    rc, o, _ = futtat(['git', 'log', '-1', '--format=%H', '--', 'lexikon/%s_TUDOMANYOS.md' % motivum])
    return o.strip() or None if rc == 0 else None


def atnezes_ervenyes(sor, motivum, commit):
    """SEMA 2.48, DT-F156l: a sor a lap mai commitjáról szól (legalább 7 jegyű előtag), a `ki` a felhasználó, és az
    `idezet` a felhasználó szavai (nem üres). Session vagy modell nem írhat érvényes sort a felhasználó idézete nélkül."""
    lc = (sor.get('lap_commit') or '').strip()
    return (sor.get('id') == motivum and len(lc) >= 7 and commit.startswith(lc)
            and (sor.get('ki') or '').strip() == 'felhasználó' and bool((sor.get('idezet') or '').strip()))


def vizualis_atnezes(motivum):
    """A felhasználó vizuális átnézése a lap MAI változatáról: a tábla érvényes sora, vagy None.
    Az átnézés a lap commitjához kötött: ha a lap azóta újragenerálódott, a régi átnézés nem érvényes."""
    if not os.path.exists(os.path.join(GYOKER, ATNEZES_TABLA)):
        return None
    commit = lap_commit(motivum)
    if not commit:
        return None
    sorok = tsv(ATNEZES_TABLA)
    for s in sorok:
        if atnezes_ervenyes(s, motivum, commit):
            return s
    # F203 (N-F184a, DT665): egy korábbi lapváltozat átnézése érvényes marad, ha azóta csak a generált szótári/KH blokk (és a
    # kolofon) változott — blokkszintű lapdiff (`lapdiff_blokk.py`); a legutóbbi ilyen sor számít
    import lapdiff_blokk as LB
    for s in reversed(sorok):
        lc = (s.get('lap_commit') or '').strip()
        if not (s.get('id') == motivum and len(lc) >= 7 and (s.get('ki') or '').strip() == 'felhasználó'
                and (s.get('idezet') or '').strip()):
            continue
        d = LB.atnezes_dt665(motivum, lc, commit, GYOKER)
        if d['ervenyes']:
            return dict(s, dt665=d)
    return None


def kriterium_9(motivum):
    """DT-F156k: az olvasói kapu. Zöld, ha a lapon 0 BUKÁS (`olvasoi_kapu.py`) ÉS a lap mai változatáról
    rögzített a felhasználó vizuális átnézése. A FIGYELMEZTETÉS nem blokkol."""
    mero = 'olvasoi_kapu.py + vizuális átnézés (%s)' % ATNEZES_TABLA
    if not os.path.exists(os.path.join(GYOKER, 'lexikon', motivum + '_TUDOMANYOS.md')):
        return uj(NINCS, 'nincs lexikon-lap', mero, motivum)
    try:
        import olvasoi_kapu as OK
        tal, megj = OK.motivum_meres(motivum)
        kapunkent, buk, figy = OK.osszesit(tal)
        atnez = vizualis_atnezes(motivum)
    except Exception as ex:  # noqa: BLE001 -- a mero hibaja "hiba", nem nulla
        return uj(HIBA, 'a mérő hibával állt le', mero, motivum, [repr(ex)[:300]])
    reszlet = ['%s: BUKÁS %d, FIGYELMEZTETÉS %d' % (k, v[OK.BUKAS], v[OK.FIGY]) for k, v in sorted(kapunkent.items())]
    reszlet += megj
    reszlet.append('vizuális átnézés: %s' % ('%s, %s' % (atnez.get('datum', ''), atnez.get('ki', '')) if atnez
                                             else 'nincs a lap mai változatáról'))
    if atnez and atnez.get('dt665'):
        reszlet.append('DT665 kivétel (a %s változat átnézése): %s%s' % (
            atnez['lap_commit'][:12], atnez['dt665']['ok'],
            '' if atnez['dt665']['kolofon'] else '; a kolofon nem változott — a (c) a jelentésben ellenőrizendő'))
    e = uj(ZOLD if buk == 0 and atnez else PIROS, '%d BUKÁS, %d FIGYELMEZTETÉS, átnézés: %s' % (
        buk, figy, 'van' if atnez else 'nincs'), mero, motivum, reszlet, {'n': buk, 'figy': figy, 'atnezes': int(bool(atnez))})
    return e


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
    import dontes_nezet as DN   # egyesitett nezet: a dontesek/uj/*.md sorai is
    if True:
        for s in DN.dontesek_szoveg(GYOKER).splitlines():
            if not s.startswith('| DT'):
                continue
            m = [x.strip() for x in s.split('|')]
            if len(m) < 8:
                continue
            szam = re.match(r'#(\d+)', m[2])
            ki.append({'id': m[1], 'feladat': int(szam.group(1)) if szam else None, 'cim': m[2],
                       'kerdes': m[3][:300], 'nyitott': '🟡' in m[6]})
    return ki


def sajat_fajl(motivum, ir):
    """A brief `ir` listájában a motívum valamelyik fájlja áll (nem csak a neve valamelyik naplóban)."""
    return any(x % motivum in ir for x in ('motivumok/%s.md', 'lexikon/%s_', 'motivumlog/%s'))


def pont_a_motivumrol(szoveg, motivum):
    """A brief valamelyik ⛔ pontja a motívumról szól."""
    return any('⛔' in s and motivum in s for s in szoveg.splitlines())


def lista_mezo(ertek):
    """A fejléc `[a, b]` listája elemekre bontva."""
    return [x.strip().strip('"\'') for x in (ertek or '').strip().strip('[]').split(',') if x.strip()]


def motivum_kesz(fej, motivum, dt_lista=()):
    """DT-F123n: több motívumot író briefben a `motivum_kesz` fejlécmezőben álló motívum része kész — a brief erről a
    motívumról már nem hoz ⛔-t, a fájljait csak a lezárás (C5) írja. A feladat nyitott 🟡 DT-je, amely a motívumot
    megnevezi, ettől még blokkol."""
    if motivum not in lista_mezo(fej.get('motivum_kesz')):
        return False
    return not any(d['nyitott'] and d['feladat'] == int(fej.get('feladat', -1)) and motivum in d['kerdes']
                   for d in dt_lista)


def feladat_blokkol(fej, szoveg, motivum, dt_lista=()):
    """DT-F156b (c): megállt/döntésre váró feladat, `ir`-ben a motívum fájlja ÉS a ⛔ pontja róla szól — kivéve, ha a
    motívum része a briefben kész (`motivum_kesz`, DT-F123n)."""
    return fej.get('allapot') in ('megallt', 'dontesre_var') and sajat_fajl(motivum, fej.get('ir', '')) \
        and pont_a_motivumrol(szoveg, motivum) and not motivum_kesz(fej, motivum, dt_lista)


def kriterium_8(motivum, fejlecek, dt_lista):
    mero = 'feladatok.py + DONTESEK.md'
    erintett = {n: f for n, f in fejlecek.items() if motivum in f.get('ir', '')}
    blokkolo = {}
    for n, f in erintett.items():
        try:
            with open(os.path.join(GYOKER, f['_fajl']), encoding='utf-8') as fh:
                szoveg = fh.read()
        except OSError:
            continue
        if feladat_blokkol(f, szoveg, motivum, dt_lista):
            blokkolo[n] = f
    reszlet, info = [], []
    for n, f in sorted(erintett.items()):
        if f.get('allapot') in ('megallt', 'dontesre_var'):
            kesz = ' (a motívum része kész: motivum_kesz)' if motivum_kesz(f, motivum, dt_lista) else ''
            (reszlet if n in blokkolo else info).append('#%d ⛔ megállt feladat%s' % (n, kesz))
    for d in dt_lista:
        if d['nyitott'] and d['feladat'] in erintett:
            (reszlet if d['feladat'] in blokkolo else info).append('%s 🟡 (#%d)' % (d['id'], d['feladat']))
    e = uj(PIROS if reszlet else ZOLD, '%d blokkoló, %d tájékoztató ⛔/🟡' % (len(reszlet), len(info)), mero, motivum,
           reszlet + ['tájékoztató: ' + x for x in info], {'n': len(reszlet), 'info': len(info)})
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


def kiadas_szam(motivum):
    """A motívum legnagyobb kiadásszáma az `adat/kiadasok.tsv`-ből (SEMA 2.46); 0, ha nincs kiadása."""
    try:
        return max((int(s['kiadas']) for s in tsv('adat/kiadasok.tsv') if s.get('id') == motivum), default=0)
    except (OSError, ValueError):
        return 0


def kiadas_allapot(kiadas, minden_zold):
    """DT-F156m: a kiadott lap a Stash-ben marad; ha egy kapu (pl. a 9.) azóta piros, ezt kimondja."""
    if not kiadas:
        return None
    elso = '%s %d. kiadás érvényes' % (nevelo(kiadas).capitalize(), kiadas)
    if minden_zold:
        return elso + '.'
    return '%s; %s %d. kiadás javítandói nyitottak.' % (elso, nevelo(kiadas + 1), kiadas + 1)


def nevelo(n):
    """A számnév előtti névelő: az 1., 5., 50. … előtt „az” (egy, öt, ötven), egyébként „a”."""
    return 'az' if str(n)[0] in '15' else 'a'


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
        'negativ_kriterium': m['negativ_kriterium'], 'folerendelt_fogalom': m['folerendelt_fogalom'],  # DT-F156e
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


def allasfokozat(m, zold_db, ossz_db, kriteriumok, kiadas=0):
    if zold_db == ossz_db or kiadas:  # DT-F156m: a kiadott lap kész marad, a következő kiadás javítandóival
        return 'lezárt (stash)'
    if m['statusz'] == 'feldolgozás alatt':
        return 'feldolgozás'
    return 'ellenőrzés'


# ----------------------------------------------------------------------------- fo

def feherlista(d, kulcsok):
    return {k: d[k] for k in kulcsok if k in d}


def nyilvanos(belso):
    """A nyilvános réteg: CSAK előrehaladás (DT-F156j). Fehérlista, nem feketelista: piros kapu, hibaszám, nyitott
    jelölt, megállt feladat és bármely akadályt jelző mező nem megy át."""
    ki = feherlista(belso, FEHERLISTA_TOP)
    ki['_generalt'] = belso['_generalt'].replace('feed_belso', 'feed_nyilvanos') + ' (a belső réteg fehérlistás szűrése)'
    o = belso['merok_osszesen']
    ki['merok_osszesen'] = {k: o[k] for k in ('motivum_db', 'kesz_db', 'kapu_zold', 'kapu_ossz')}
    ki['heti_tortenes'] = [feherlista(x, FEHERLISTA_ESEMENY) for x in belso['heti_tortenes']]
    ki['motivumok'] = []
    for m in belso['motivumok']:
        e = feherlista(m, FEHERLISTA_MOTIVUM)
        e['allasfokozat'] = m['allasfokozat_olvasoi']
        e['lanc'] = lanc(m['allasfokozat'])
        e['teljesult_lepesek'] = [feherlista(k, FEHERLISTA_KRITERIUM) for k in m['kriteriumok'] if k['allapot'] == ZOLD]
        e['olvasoi_mondat'] = m['olvasoi_mondat_nyilvanos']
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
            '7': kriterium_7(mid), '8': kriterium_8(mid, fejlecek, dt_lista), '9': kriterium_9(mid),
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
        kiadas = kiadas_szam(mid)
        st['kiadas_allapot'] = kiadas_allapot(kiadas, zold_db == len(lista))
        stashben = zold_db == len(lista) or bool(kiadas)
        e = {
            'id': mid, 'cim': m['ui_cimke'] or m['cim'], 'tema': m['tema'], 'pardes_szint': m['pardes_szint'],
            'allasfokozat': allasfokozat(m, zold_db, len(lista), krit, kiadas),
            'allasfokozat_olvasoi': OLV_ALLAS[allasfokozat(m, zold_db, len(lista), krit, kiadas)],
            'olvasoi_mondat_nyilvanos': olvasoi_mondat_nyilvanos(st['elofordulas_osz'] + st['elofordulas_usz'], len(elv), zold_db),
            'olvasoi_mondat': olvasoi_mondat(st['elofordulas_osz'] + st['elofordulas_usz'],
                                             sum(1 for j in sajat_j if blokkolo_jelolt(j)), len(elv), zold_db),
            'tsv_statusz': m['statusz'], 'tsv_statusz_eltérés': (m['statusz'] == 'publikálható') != (zold_db == len(KRITERIUMOK)),
            'kriteriumok': lista, 'zold_db': zold_db, 'ossz_db': len(lista),
            'nyitott_jelolt_db': sum(1 for j in sajat_j if blokkolo_jelolt(j)),
            'nyitott_motivumkozi_db': sum(1 for j in sajat_j if j['dontes'] == 'nyitva' and not blokkolo_jelolt(j)),
            'elvetett_jelolt_db': len(elv),
            'beepitett_jelolt_db': sum(1 for j in sajat_j if j['dontes'].startswith('beépít')),
            'stash': st if stashben else None,
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
        'kritérium': 'mind a %d pont zöld (F156 3.2; a 9.: DT-F156k), vagy a lapnak van kiadása (DT-F156m: a '
                     '`kiadas_allapot` mondja ki a következő kiadás nyitott javítandóit); a kötet-hozzárendelés nincs '
                     'adatban (DT-F156d)' % len(KRITERIUMOK),
        'tetelek': [dict(feherlista(x['stash'], FEHERLISTA_STASH), id=x['id']) for x in ki if x['stash']],
        'kesz_db': sum(1 for x in ki if x['stash']),
    }

    os.makedirs(a.kimenet, exist_ok=True)
    for nev, tartalom in (('feed_belso.json', belso), ('feed_nyilvanos.json', ny), ('stash.json', stash)):
        with open(os.path.join(a.kimenet, nev), 'w', encoding='utf-8', newline='\n') as f:
            json.dump(tartalom, f, ensure_ascii=False, indent=1, sort_keys=False)
            f.write('\n')
    print('kész: %d motívum, %d a Stash-ben (%d/%d vagy kiadott); kimenet: %s' % (len(ki), stash['kesz_db'], len(KRITERIUMOK),
                                                               len(KRITERIUMOK), a.kimenet))


if __name__ == '__main__':
    main()
