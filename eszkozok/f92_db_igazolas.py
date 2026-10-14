#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/f92_db_igazolas.py -- F92: a pardes.db F92-es tartalmának CSAK-OLVASÓ igazolása (markdown kimenet).

Mindent a pardes.db-ből (mode=ro) és a forrás-TSV-kből SZÁMÍT; a zárójelentés (`naplok/PARDES_DB_OLVASOI_zaras.md`)
számait csak mint „várt” értéket veti össze, az eltérést `ELTÉRÉS` jelöli (nem simítja).

Szakaszok: K3 (meta-hash és forrás-sorszám), Macula kétértelmű csoportok, lxx_versszam, szövegformák
(Dán/Bír/Józs), Nave, a versifikációs térkép bontása, görög ÚSZ-előfordulás (kétirányú).

Futtatás: python eszkozok/f92_db_igazolas.py [--db pardes.db] > naplok/PARDES_DB_OLVASOI_db_igazolas.md
"""
import argparse
import datetime
import glob
import hashlib
import os
import re
import sqlite3
import subprocess
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'olvaso_pilot'))
import nave_bontas as NB  # noqa: E402
import zsolt_felirat_halmaz as ZFH  # noqa: E402

ELTERESEK = []


def tsv(rel):
    """(fejléc, sorok listák) -- split('\\t'), a #-sorok kihagyva."""
    fej, ki = None, []
    with open(os.path.join(ROOT, rel), encoding='utf-8', newline='') as f:
        for s in f.read().split('\n'):
            s = s.rstrip('\r')
            if not s.strip() or s.startswith('#'):
                continue
            m = s.split('\t')
            if fej is None:
                fej = m
            else:
                ki.append(m)
    return fej, ki


def hnorm(s):
    m = re.match(r'^([HG])0*(\d+)([A-Z]?)$', (s or '').strip().upper())
    return '%s%04d' % (m.group(1), int(m.group(2))) if m else None


def egyez(nev, kapott, vart):
    jel = 'egyezik' if kapott == vart else '**ELTÉRÉS**'
    if kapott != vart:
        ELTERESEK.append('%s: számított %s, várt %s' % (nev, kapott, vart))
    print('- %s: számított **%s**, várt (zaras.md) %s -- %s' % (nev, kapott, vart, jel))


def git(*a):
    return subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True, encoding='utf-8').stdout.strip()


def tabla_hash(con, n):
    k = len(con.execute('PRAGMA table_info("%s")' % n).fetchall())
    order = ','.join(str(i + 1) for i in range(k))
    h, db = hashlib.sha256(), 0
    for row in con.execute('SELECT * FROM "%s" ORDER BY %s' % (n, order)):
        h.update(('\t'.join('' if v is None else str(v) for v in row) + '\n').encode('utf-8'))
        db += 1
    return db, h.hexdigest()


def k3(con, meta):
    print('\n## 1. K3 -- a meta-hash és a forrás-TSV állapota\n')
    ts = meta.get('epites_ts', '')
    ep = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    forras = {'token_macula': ['konkordancia/Macula_heber_*.tsv'], 'lxx_token': ['konkordancia/LXX_OS/'],
              'lxx_versszam': ['konkordancia/LXX_OS/'], 'bdb_alias': ['konkordancia/BDB_strong_alias.tsv'],
              'nave_vers': ['konkordancia/Nave_basokant.tsv', 'konkordancia/Karoli_versmegfeleltetes.tsv', 'konkordancia/LXX_OS/']}
    print('építés: `%s`, mód `%s`\n' % (ts, meta.get('mod')))
    print('| tábla | sor | meta-sor | meta-hash egyezik a tábla tartalmával | forrás-TSV: nem commitolt módosítás / commit az építés után |')
    print('|---|---:|---:|---|---|')
    rossz = 0
    for t in ('token_macula', 'lxx_token', 'lxx_versszam', 'bdb_alias', 'nave_vers', 'token_karoli', 'token_par'):
        db, hh = tabla_hash(con, t)
        m = meta.get('hash:' + t, '|')
        ok = (m == '%d|%s' % (db, hh))
        valt = []
        for rel in forras.get(t, []):
            if git('status', '--porcelain', '--', rel):
                valt.append('%s nem commitolt módosítás' % rel)
            ci = git('log', '-1', '--format=%cI', '--', rel)
            if ci and datetime.datetime.fromisoformat(ci) > ep:
                valt.append('%s commit %s > építés' % (rel, ci))
        if not ok or valt:
            rossz += 1
            ELTERESEK.append('K3 %s: hash %s, forrás %s' % (t, ok, valt))
        print('| `%s` | %d | %s | %s | %s |' % (t, db, m.split('|')[0], 'igen' if ok else '**NEM**', '; '.join(valt) or 'nincs'))
    # forrás-sorszámok
    macula = sum(len(tsv(os.path.relpath(f, ROOT).replace('\\', '/'))[1]) for f in sorted(glob.glob(os.path.join(ROOT, 'konkordancia', 'Macula_heber_*.tsv'))))
    lxx = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'konkordancia', 'LXX_OS', '*.tsv'))):
        fej, sorok = tsv(os.path.relpath(f, ROOT).replace('\\', '/'))
        if 'szoalak' in fej:
            lxx += len(sorok)
    nave = len(tsv('konkordancia/Nave_basokant.tsv')[1])
    alias = len(tsv('konkordancia/BDB_strong_alias.tsv')[1])
    print('')
    egyez('Macula forrás-sor (TSV most) = meta token_macula:forras_sor', macula, int(meta['token_macula:forras_sor']))
    egyez('LXX_OS forrás-sor (TSV most) = meta lxx_token:forras_sor', lxx, int(meta['lxx_token:forras_sor']))
    egyez('Nave forrás-sor (TSV most) = meta nave_vers:nave_basokant_sor', nave, int(meta['nave_vers:nave_basokant_sor']))
    egyez('bdb_alias sor = BDB_strong_alias.tsv sor', con.execute('SELECT COUNT(*) FROM bdb_alias').fetchone()[0], alias)
    return rossz


def macula(con, meta):
    print('\n## 2. Macula kétértelmű (vers, Strong) csoportok\n')
    cs = con.execute("SELECT COUNT(*), SUM(n) FROM (SELECT COUNT(*) n FROM token_macula WHERE strong IS NOT NULL AND igehely!='' "
                     "GROUP BY igehely, strong HAVING COUNT(*)>1)").fetchone()
    egyez('kétértelmű (vers, Strong) csoport a táblából', cs[0], 30541)
    egyez('meta token_macula:ketertelmu_vers_strong_csoport', int(meta['token_macula:ketertelmu_vers_strong_csoport']), cs[0])
    print('- ebben a csoportokban a Macula-tokenek száma: %s (meta: %s)' % (cs[1], meta['token_macula:ketertelmu_vers_strong_token']))
    ossz = con.execute("SELECT COUNT(DISTINCT igehely), COUNT(*) FROM token_macula WHERE igehely LIKE '%;%'").fetchone()
    egyez('összevont `A;B` Károli-kulcsú vers / sor', '%d / %d' % ossz, '7 / 132')
    # a pilot-kötés kétértelmű esetei a két szakaszon (db_meres.macula_kot)
    import db_meres as DM
    for nev, fejezetek, konyv, vart in (('1Móz 1–25', range(1, 26), '1Móz', '1256 / 14142 (116 vers)'),
                                        ('Zsolt 22', [22], 'Zsolt', '31 / 389 (6 vers)')):
        ketert = vers_ketert = osszes = 0
        for f in fejezetek:
            for (ig,) in con.execute("SELECT igehely FROM vers WHERE konyv=? AND fejezet=? ORDER BY vers", (konyv, f)):
                d = DM.db_vers(con, ig)
                th = [h[0] for h in d['heber']]
                _, k = DM.macula_kot(th, d['macula'], len(th))
                ketert += k
                vers_ketert += 1 if k else 0
                osszes += len(th)
        egyez('%s: kétértelmű kötés tokenre / összes TAHOT-token (vers)' % nev, '%d / %d (%d vers)' % (ketert, osszes, vers_ketert), vart)


def lxx_versszam(con, meta):
    print('\n## 3. lxx_versszam\n')
    sor = dict(con.execute('SELECT forras, COUNT(*) FROM lxx_versszam GROUP BY forras').fetchall())
    egyez('forrás-értékek halmaza', sorted(sor), ['LXX_OS', 'nincs'])
    egyez('sor forras=LXX_OS', sor.get('LXX_OS'), 23849)
    egyez('sor forras=nincs', sor.get('nincs'), 383)
    egyez('összes sor', sum(sor.values()), 24232)
    ot = {x for (x,) in con.execute("SELECT DISTINCT igehely FROM token_eredeti WHERE nyelv='H' AND van_vers=1")}
    van = {x for (x,) in con.execute('SELECT DISTINCT karoli_igehely FROM lxx_versszam')}
    egyez('ÓSZ-vers (TAHOT héber token, Károli-vers)', len(ot), 23204)
    egyez('ÓSZ-vers, amelyhez nincs lxx_versszam-sor', len(ot - van), 0)
    egyez('lxx_versszam-sor nem ÓSZ-versre', len(van - ot), 0)
    egyez('forras=nincs sor nem üres lxx_igehely-vel', con.execute("SELECT COUNT(*) FROM lxx_versszam WHERE forras='nincs' AND IFNULL(lxx_igehely,'')!=''").fetchone()[0], 0)
    egyez('forras=nincs, de a terkep_ertek nem üres (vers)', con.execute("SELECT COUNT(*) FROM lxx_versszam WHERE forras='nincs' AND IFNULL(terkep_ertek,'')!=''").fetchone()[0], 95)
    egyez('forras=nincs vers (terkep_ertek nélkül)', con.execute("SELECT COUNT(*) FROM lxx_versszam WHERE forras='nincs' AND IFNULL(terkep_ertek,'')=''").fetchone()[0], 288)


def szovegformak(con):
    print('\n## 4. Párhuzamos LXX-szövegformák (Dán, Bír, Józs)\n')
    print('| könyv | Károli-vers, amelyen ≥2 szövegforma áll | lxx_token sor formánként | lxx_versszam (LXX_OS) sor formánként |')
    print('|---|---:|---|---|')
    for pre in ('Dán', 'Bír', 'Józs'):
        tobb = con.execute("SELECT COUNT(*) FROM (SELECT karoli_igehely FROM lxx_token WHERE karoli_igehely LIKE ? "
                           "GROUP BY karoli_igehely HAVING COUNT(DISTINCT szovegforma)>1)", (pre + ' %',)).fetchone()[0]
        tok = dict(con.execute("SELECT szovegforma, COUNT(*) FROM lxx_token WHERE karoli_igehely LIKE ? GROUP BY szovegforma", (pre + ' %',)).fetchall())
        vsz = dict(con.execute("SELECT szovegforma, COUNT(*) FROM lxx_versszam WHERE karoli_igehely LIKE ? AND forras='LXX_OS' GROUP BY szovegforma", (pre + ' %',)).fetchall())
        print('| %s | %d | %s | %s |' % (pre, tobb, tok, vsz))
        if tobb == 0 or len(tok) < 2:
            ELTERESEK.append('szövegforma %s: nincs párhuzamos forma a táblában' % pre)
    print('')
    egyez('lxx_token / lxx_versszam(LXX_OS) sor üres szövegformával', con.execute("SELECT (SELECT COUNT(*) FROM lxx_token WHERE IFNULL(szovegforma,'')='') + (SELECT COUNT(*) FROM lxx_versszam WHERE forras='LXX_OS' AND IFNULL(szovegforma,'')='')").fetchone()[0], 0)


def nave(con, meta):
    print('\n## 5. Nave\n')
    nv = con.execute('SELECT COUNT(*), COUNT(DISTINCT forras_sor) FROM nave_vers').fetchone()
    egyez('nave_vers sor', nv[0], 156214)
    egyez('nave_vers különböző forrás-sor (bontott)', nv[1], 75856)
    fej, sorok = tsv('konkordancia/Nave_basokant.tsv')
    ix = fej.index('igehely')
    uresek = fejezet = nemert = 0
    for r in sorok:
        h = NB.hely_elemez(r[ix])
        if not r[ix].strip():
            uresek += 1
        elif h is None:
            nemert += 1
        elif h[0] == 'fejezet':
            fejezet += 1
    egyez('Nave-sor a TSV-ben', len(sorok), 85246)
    egyez('kihagyott: igehely nélküli (TSV-ből számolva)', uresek, 7122)
    egyez('kihagyott: fejezet-szintű (TSV-ből számolva)', fejezet, 2212)
    egyez('kihagyott: nem értelmezhető hely (TSV-ből számolva)', nemert, 13)
    nincs_vers = len(sorok) - nv[1] - uresek - fejezet - nemert
    egyez('kihagyott: nincs Károli-vers a tartományban (a maradék)', nincs_vers, 43)
    egyez('kihagyott összesen = 2212 + 7122 + 13 + 43', len(sorok) - nv[1], 9390)
    egyez('meta nave_vers:kihagyott_osszes', int(meta['nave_vers:kihagyott_osszes']), len(sorok) - nv[1])
    egyez('bontott + kihagyott = Nave-sor', nv[1] + (len(sorok) - nv[1]), len(sorok))
    egyez('nave_vers sor igehely nélkül/üres nave_hellyel', con.execute("SELECT COUNT(*) FROM nave_vers WHERE IFNULL(igehely,'')='' OR IFNULL(nave_hely,'')=''").fetchone()[0], 0)


def terkep(con):
    print('\n## 6. A versifikációs térkép bontása (nem forrás, DT-F92b; a kulcs KJV-kulcs, F91 DT-F91b)\n')
    kulcsok, nm = Counter(), 0
    fej, sorok = tsv('konkordancia/LXX_versificacios_terkep.tsv')
    for r in sorok:
        if r[0] == 'NEM_MEGHATAROZHATO':
            nm += 1
        else:
            kulcsok[r[0]] += 1
    # KJV-kulcs -> Károli-vers(ek): az lxx_versszam.kjv_vers (LXX_OS; a felirat-vers nélkül) és a Karoli_versmegfeleltetes.tsv (igehely_kjv)
    kjv_karoli = {}

    def hozzaad(ig, cv):
        if re.fullmatch(r'\d+:\d+', cv):
            kjv_karoli.setdefault('%s %s' % (ig.rsplit(' ', 1)[0], cv), set()).add(ig)
    felirat = ZFH.felirat_versek()    # F91 E2: a közös felirat-halmaz (nem a `karoli_ok` jelölés)
    for ig, kjv in con.execute("SELECT DISTINCT karoli_igehely, kjv_vers FROM lxx_versszam WHERE IFNULL(kjv_vers,'')!=''"):
        if ig in felirat:
            continue
        for cv in kjv.split(';'):
            hozzaad(ig, cv)
    vers = {x for (x,) in con.execute('SELECT igehely FROM vers')}
    af, asor = tsv('konkordancia/Karoli_versmegfeleltetes.tsv')
    for r in asor:
        if r[0] in vers:
            hozzaad(r[0], r[1])
    ot = {x for (x,) in con.execute('SELECT DISTINCT karoli_igehely FROM lxx_versszam')}
    van_os = {x for (x,) in con.execute("SELECT DISTINCT karoli_igehely FROM lxx_versszam WHERE forras='LXX_OS'")}
    csak = {x for (x,) in con.execute("SELECT DISTINCT karoli_igehely FROM lxx_versszam WHERE forras='nincs' AND IFNULL(terkep_ertek,'')!=''")}
    atvalt = {k for k in kulcsok if k in kjv_karoli}
    karoli_vers = set().union(*[kjv_karoli[k] for k in atvalt]) if atvalt else set()
    egyez('NEM_MEGHATAROZHATO sor', nm, 39)
    egyez('KJV-kulcs a térképben (különböző)', len(kulcsok), 5204)
    egyez('  ebből Károli-versre átváltható (LXX_OS kjv_vers + A-tábla)', len(atvalt), 5001)
    egyez('  ebből nincs Károli-vers (karoli_nelkul)', len(set(kulcsok) - atvalt), 203)
    egyez('Károli-vers, amelyhez a térkép értéke kerül (KJV→Károli után)', len(karoli_vers), 5001)
    egyez('  ebből ÓSZ-vers az lxx_versszam-ban', len(karoli_vers & ot), 5001)
    egyez('  ebből LXX_OS-sal is', len(karoli_vers & van_os), 4906)
    egyez('  ebből csak térkép (forras=nincs, terkep_ertek)', len(karoli_vers & csak), 95)
    egyez('  ebből Károli-vers, de nem ÓSZ-vers az lxx_versszam-ban', len((karoli_vers - ot) & vers), 0)
    egyez('nem üres terkep_ertek (Károli-vers, lxx_versszam)', len({x for (x,) in con.execute("SELECT DISTINCT karoli_igehely FROM lxx_versszam WHERE IFNULL(terkep_ertek,'')!=''")}), 5001)
    zs22 = con.execute("SELECT COUNT(*), SUM(terkep_ertek!='') FROM lxx_versszam WHERE karoli_igehely LIKE 'Zsolt 22:%' AND forras='LXX_OS'").fetchone()
    egyez('Zsolt 22: LXX_OS-sor / ebből nem üres terkep_ertek (F91: KJV-kulcson illesztve; a felirat-versnek nincs KJV-kulcsa)', '%d / %d' % zs22, '32 / 31')
    # F91 E2: a közös felirat-halmaz (67 vers, Zsolt 13:1 is) egyetlen versének sincs terkep_ertek-e
    fe = [ig for (ig, t) in con.execute("SELECT karoli_igehely, terkep_ertek FROM lxx_versszam") if ig in felirat and t]
    egyez('felirat-halmaz (%d vers) verse, amelynek van terkep_ertek-e' % len(felirat), len(fe), 0)


def usz(con):
    print('\n## 7. Görög ÚSZ-előfordulás (kétirányú: TAGNT ↔ token_strong)\n')
    egesz, lanc = Counter(), Counter()
    fej, sorok = tsv('konkordancia/TAGNT_kivonat.tsv')
    for r in sorok:
        if len(r) < 2:
            continue
        n = hnorm(r[1])
        if n:
            egesz[n] += 1
        elif '+' in r[1]:
            for x in r[1].split('+'):
                h = hnorm(x)
                if h:
                    lanc[h] += 1
    db = Counter({g: n for g, n in con.execute("SELECT strong, COUNT(*) FROM token_strong WHERE strong LIKE 'G%' GROUP BY strong")})
    tagnt = Counter()
    for g in set(egesz) | set(lanc):
        tagnt[g] = egesz[g] + lanc[g]
    egyez('G-Strong a token_strong-ban', len(db), 5420)
    print('- G-Strong a TAGNT-ban (egész mező ∪ láncelem): %d' % len(tagnt))
    hianyzik = sorted(g for g in tagnt if g not in db)
    tobblet = sorted(g for g in db if g not in tagnt)
    elter = sorted(g for g in db if g in tagnt and db[g] != tagnt[g])
    print('- a TAGNT-ban van, a DB-ből hiányzik: %d %s' % (len(hianyzik), hianyzik[:10]))
    print('- a DB-ben van, a TAGNT-ban nincs: %d %s' % (len(tobblet), tobblet[:10]))
    print('- mindkettőben van, de a darabszám eltér: %d %s' % (len(elter), elter[:10]))
    if hianyzik or tobblet or elter:
        ELTERESEK.append('ÚSZ: hiányzik %d, többlet %d, eltérő darab %d' % (len(hianyzik), len(tobblet), len(elter)))
    reszeg = sum(1 for g in db if db[g] != egesz[g])
    print('- a DB-szám eltér az egész-mezős (pilot TSV-út / lekerdez.py scan) számtól: %d G-Strongon (ezek a láncelemet is hordozó Strongok)' % reszeg)
    for g in ('G4218',):
        print('- példa %s: egész mező %d, láncelem %d, DB %d' % (g, egesz[g], lanc[g], db.get(g, 0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--db', default=os.path.join(ROOT, 'pardes.db'))
    a = ap.parse_args()
    con = sqlite3.connect('file:%s?mode=ro' % a.db.replace('\\', '/'), uri=True)
    meta = dict(con.execute('SELECT kulcs, ertek FROM meta'))
    print('# PARDES_DB_OLVASOI (#92) -- a pardes.db csak-olvasó igazolása\n')
    print('*Proveniencia: `scope=a #92 F92-es táblái, a zaras.md számai + K3 | forras=%s (mode=ro) meta.epites_ts=%s meta.mod=%s + a konkordancia/ forrás-TSV-k; eszkozok/f92_db_igazolas.py | ts=%s`*'
          % (os.path.basename(a.db), meta.get('epites_ts'), meta.get('mod'),
             datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')))
    k3(con, meta)
    macula(con, meta)
    lxx_versszam(con, meta)
    szovegformak(con)
    nave(con, meta)
    terkep(con)
    usz(con)
    print('\n## Összegzés\n')
    if ELTERESEK:
        print('**ELTÉRÉS %d tétel:**' % len(ELTERESEK))
        for e in ELTERESEK:
            print('- ' + e)
    else:
        print('Minden számított érték egyezik a várttal.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
