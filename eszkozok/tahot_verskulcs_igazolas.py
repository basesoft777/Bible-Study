#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F85.8 — az átkulcsolás (F85.6) és a #22 kézi táblák kivezetése (F85.8) utólagos, csak olvasó igazolása.

(a) Soronkénti bájt-összevetés az átkulcsolás előtti állapot (`8ce6e95c~1`) és a mostani
    `konkordancia/TAHOT_kivonat.tsv` között a `naplok/F85_kulcsvaltas.tsv` sorszámai alapján: pontosan a napló
    sorai különböznek, csak az Igehely (első) mezőben, a régi/új kulcs a naplóéval egyezik, minden más sor és mező
    bájtazonos.
(b) A már futott (VERSBEOSZTAS_JOVAHAGYOTT) könyvek vers -> héber szavak bemenete: a régi pipeline (az átkulcsolás
    előtti TAHOT + f22 táblák, `tokenek.betolt_eredeti()` + `osszevont_extra()`) és az új pipeline (a mostani
    TAHOT + a kivezetett f22 táblák) versenként azonos-e (sorszám, strong, alak, tükörfordítás, TR-jelző).
(c) A már futott könyvek `parok_*` / `szavak_*` tábláinak SOR-tartalma: az `egyesit.epit()` a régi és az új
    bemeneti pipeline-nal, a repóbeli táblák adatsoraival összevetve (a táblákat nem írja; a proveniencia-sor
    `forras=` mezője az f22 táblák kivezetése miatt eltérne egy újraíráskor — ezt külön jelzi).

Kimenet: naplok/F85_igazolas.tsv és naplok/F85_igazolas.md. Más fájlt nem ír. split / join, a csv modul tilos.
Futtatás a repó gyökeréből:  python eszkozok/tahot_verskulcs_igazolas.py
"""
import collections
import datetime
import glob
import hashlib
import os
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
import tokenek  # noqa: E402
import egyesit  # noqa: E402

IDOPONT = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
BASE = '8ce6e95c~1'     # az átkulcsolás előtti állapot (a4a09ba9)
VALT = os.path.join(ROOT, 'naplok', 'F85_kulcsvaltas.tsv')
TAHOT = os.path.join(ROOT, 'konkordancia', 'TAHOT_kivonat.tsv')
KI_TSV = os.path.join(ROOT, 'naplok', 'F85_igazolas.tsv')
KI_MD = os.path.join(ROOT, 'naplok', 'F85_igazolas.md')
ASCII = {'Móz': 'Moz'}
sor_ki = []        # (pont, tárgy, eredmény, részlet)


def jelent(pont, targy, eredmeny, reszlet=''):
    sor_ki.append((pont, targy, eredmeny, reszlet))
    print('%s | %s | %s | %s' % (pont, targy, eredmeny, reszlet))


def git_show(ut):
    r = subprocess.run(['git', 'show', '%s:%s' % (BASE, ut)], capture_output=True, cwd=ROOT)
    if r.returncode:
        raise SystemExit('git show hiba: %s' % ut)
    return r.stdout


def a_pont():
    regi = git_show('konkordancia/TAHOT_kivonat.tsv').split(b'\n')
    uj = open(TAHOT, 'rb').read().split(b'\n')
    jelent('a', 'sorszám (régi/új)', 'OK' if len(regi) == len(uj) else 'HIBA', '%d / %d' % (len(regi), len(uj)))
    naplo = {}
    with open(VALT, encoding='utf-8') as fh:
        for s in fh:
            if s.startswith('#') or s.startswith('sorszam\t'):
                continue
            p = s.rstrip('\n').split('\t')
            naplo[int(p[0])] = (p[1], p[2])
    elteres = {}
    csak_elso_mezo = True
    for i, (a, b) in enumerate(zip(regi, uj), 1):
        if a != b:
            ma, mb = a.split(b'\t'), b.split(b'\t')
            if len(ma) != len(mb) or ma[1:] != mb[1:]:
                csak_elso_mezo = False
            elteres[i] = (ma[0].decode('utf-8'), mb[0].decode('utf-8'))
    jelent('a', 'eltérő sorok = a napló sorai (sorszám szerint)', 'OK' if elteres == naplo else 'HIBA',
           '%d eltérő sor, %d naplósor' % (len(elteres), len(naplo)))
    jelent('a', 'az eltérés csak az Igehely mezőben', 'OK' if csak_elso_mezo else 'HIBA', '')
    kulcs_ok = all(regi[i - 1].split(b'\t')[0].decode('utf-8') == naplo[i][0] and uj[i - 1].split(b'\t')[0].decode('utf-8') == naplo[i][1] for i in naplo)
    jelent('a', 'a napló régi/új kulcsa a két fájl kulcsaival egyezik minden sorban', 'OK' if kulcs_ok else 'HIBA', '')
    erintetlen = sum(1 for i, (a, b) in enumerate(zip(regi, uj), 1) if i not in naplo and a == b)
    jelent('a', 'nem érintett sorok bájtazonosak', 'OK' if erintetlen == len(regi) - len(naplo) else 'HIBA', '%d sor' % erintetlen)
    return regi


def beallit(tahot, vm, kezi, ossz):
    tokenek.TAHOT, tokenek.VERSBEOSZTAS_MEGF, tokenek.VERSMEGF_KEZI, tokenek.VERSOSSZEVONAS = tahot, vm, kezi, ossz


def pipeline():
    ered = tokenek.betolt_eredeti()
    extra = tokenek.osszevont_extra()
    return ered, extra


def teljes(ered, extra, ig):
    return [tuple(sorted(w.items())) for w in ered.get(ig, []) + extra.get(ig, [])]


def b_pont(regi_tmp):
    jov = tokenek.VERSBEOSZTAS_JOVAHAGYOTT
    mai = (tokenek.TAHOT, tokenek.VERSBEOSZTAS_MEGF, tokenek.VERSMEGF_KEZI, tokenek.VERSOSSZEVONAS)
    beallit(*regi_tmp)
    e_regi, x_regi = pipeline()
    beallit(*mai)
    e_uj, x_uj = pipeline()
    jelent('b', 'a mai pipeline betölt (KeyError nélkül)', 'OK', 'versmegfeleltetes sorok: %d, osszevonas sorok: %d' % (len(tokenek.versmegfeleltetes()), len(tokenek.versosszevonasok())))
    konyvek = collections.OrderedDict()
    for ig in sorted(set(e_regi) | set(e_uj), key=lambda x: (x.split(' ')[0], tokenek.igehely_bont(x)[1:])):
        b = tokenek.igehely_bont(ig)[0]
        if b not in jov:
            continue
        d = konyvek.setdefault(b, [0, 0])
        d[0] += 1
        if teljes(e_regi, x_regi, ig) != teljes(e_uj, x_uj, ig):
            d[1] += 1
    ossz = sum(d[0] for d in konyvek.values())
    elt = sum(d[1] for d in konyvek.values())
    jelent('b', 'jóváhagyott könyvek vers -> héber szavak (régi vs. új pipeline)', 'OK' if elt == 0 else 'HIBA', '%d vers, %d eltérő' % (ossz, elt))
    for b, d in konyvek.items():
        jelent('b', 'könyv ' + b, 'OK' if d[1] == 0 else 'HIBA', '%d vers, %d eltérő' % tuple(d))
    return e_regi, x_regi, e_uj, x_uj


def tabla_sorok(ut):
    with open(ut, encoding='utf-8') as fh:
        sorok = [s.rstrip('\n') for s in fh if not s.startswith('#')]
    return sorok


def c_pont(regi_tmp):
    mai = (tokenek.TAHOT, tokenek.VERSBEOSZTAS_MEGF, tokenek.VERSMEGF_KEZI, tokenek.VERSOSSZEVONAS)
    jov = tokenek.VERSBEOSZTAS_JOVAHAGYOTT
    karoli = tokenek.betolt_karoli()
    futott = sorted({os.path.basename(p)[len('parok_'):-4] for p in glob.glob(os.path.join(ROOT, 'adat', 'karoli_strong', 'parok_*.tsv'))})
    ascii_konyv = {egyesit.sonnet_koteg.ascii_nev(b): b for b in tuple(jov) + ('1Móz',)}
    for n in futott:
        konyv = ascii_konyv.get(n)
        if konyv is None:
            jelent('c', 'parok_' + n, 'KIHAGYVA', 'nincs a jóváhagyott könyvek közt (nem hasonlítható)')
            continue
        u = egyesit.utak(konyv)
        fajl_p = tabla_sorok(u['parok'])[1:]
        fajl_s = tabla_sorok(u['szavak'])[1:]
        eredmeny, szovegek = {}, {}
        for cim, cfg in (('régi', regi_tmp), ('új', mai)):
            beallit(*cfg)
            p, s, a = egyesit.epit(konyv, None, karoli, None)
            eredmeny[cim] = (['\t'.join(str(x) for x in r) for r in p], ['\t'.join(str(x) for x in r) for r in s])
            prov = egyesit.proveniencia_sor(konyv)
            szovegek[cim] = {'parok': egyesit.tsv_szoveg(egyesit.PAROK_FEJ, p, prov), 'szavak': egyesit.tsv_szoveg(egyesit.SZAVAK_FEJ, s, prov),
                             'atnezes': egyesit.tsv_szoveg(egyesit.ATNEZES_FEJ, a, None)}
        beallit(*mai)
        reg_ok = eredmeny['régi'] == (fajl_p, fajl_s)
        uj_ok = eredmeny['új'] == (fajl_p, fajl_s)
        reszlet = 'repó %d/%d sor; régi pipeline = repó: %s; új pipeline = repó: %s' % (len(fajl_p), len(fajl_s), reg_ok, uj_ok)
        # teljes fájl-bájtok (a proveniencia-sorral együtt), parok / szavak / átnézési napló
        bajt, csak_prov = {}, True
        for kulcs in ('parok', 'szavak', 'atnezes'):
            ut = u[kulcs]
            if not os.path.exists(ut):
                bajt[kulcs] = {'régi': None, 'új': None}
                continue
            fb = open(ut, 'rb').read()
            bajt[kulcs] = {cim: szovegek[cim][kulcs].encode('utf-8') == fb for cim in ('régi', 'új')}
            if not bajt[kulcs]['új']:
                # csak az első (proveniencia-)sor tér-e el
                fs, us = fb.decode('utf-8').split(chr(10)), szovegek['új'][kulcs].split(chr(10))
                csak_prov = csak_prov and fs[1:] == us[1:] and kulcs != 'atnezes'
        reszlet += '; teljes fájl bájtra (régi/új): ' + ', '.join('%s %s/%s' % (k, v['régi'], v['új']) for k, v in bajt.items())
        mind_bajt = all(v['új'] is not False for v in bajt.values())
        if uj_ok and not mind_bajt and csak_prov:
            allapot = 'RÉSZBEN'
            reszlet += '; a sorok és az átnézési napló bájtazonosak, CSAK a proveniencia-sor (forras=) tér el (az f22/versmegfeleltetes*.tsv már nem forrás)'
        else:
            allapot = 'OK' if (uj_ok and mind_bajt) else 'HIBA'
        if not uj_ok:
            kul = set()
            for uj_l, f_l in ((eredmeny['új'][0], fajl_p), (eredmeny['új'][1], fajl_s)):
                cu, cf = collections.Counter(uj_l), collections.Counter(f_l)
                for sor in list((cu - cf).keys()) + list((cf - cu).keys()):
                    kul.add(sor.split(chr(9))[0])
            reszlet += '; eltérő versek (%d): %s' % (len(kul), ', '.join(sorted(kul)))
        jelent('c', 'parok/szavak sorai: ' + konyv, allapot, reszlet)
    beallit(*mai)


def sig(lista):
    return [(w['strong'], w['alak'], w['tukor']) for w in lista]


# a 9 összevonás: (közös Károli-kulcs, a fő vers régi TAHOT-címkéje, a beolvasztott vers régi TAHOT-címkéje)
OSSZEVONASOK = [('4Móz 29:39', '4Móz 29:39', '4Móz 30:1'), ('Jób 16:22', 'Jób 16:22', 'Jób 17:1'), ('Jób 36:33', 'Jób 36:33', 'Jób 37:1'),
                ('Péld 11:31', 'Péld 11:31', 'Péld 12:1'), ('Ézs 9:20', 'Ézs 9:19', 'Ézs 9:20'), ('Ézs 64:1', 'Ézs 64:1', 'Ézs 64:2'),
                ('Hós 1:11', 'Hós 1:11', 'Hós 2:1'), ('Hós 11:11', 'Hós 11:11', 'Hós 12:1'), ('Préd 2:26', 'Préd 2:26', 'Préd 2:25')]


def e_pont(regi_tmp):
    """A 9 összevonás szétválasztása: a közös kulcson a fő vers (betolt_eredeti) és az extra (osszevont_extra) tokenjei
    megegyeznek az átkulcsolás előtti nyers TAHOT megfelelő verseivel (a 6 futott és a 3 még nem futott összevonás)."""
    mai = (tokenek.TAHOT, tokenek.VERSBEOSZTAS_MEGF, tokenek.VERSMEGF_KEZI, tokenek.VERSOSSZEVONAS)
    beallit(*regi_tmp)
    regi_nyers = tokenek._nyers_eredeti()
    beallit(*mai)
    fo, extra = tokenek.betolt_eredeti(), tokenek.osszevont_extra()
    for k, f, e in OSSZEVONASOK:
        fo_ok = sig(fo[k]) == sig(regi_nyers[f]) and [w['sorsz'] for w in fo[k]] == list(range(1, len(fo[k]) + 1))
        ex_ok = sig(extra.get(k, [])) == sig(regi_nyers[e]) and [w['sorsz'] for w in extra.get(k, [])] == list(range(len(fo[k]) + 1, len(fo[k]) + 1 + len(regi_nyers[e])))
        jelent('e', 'összevonás szétválasztása: %s (fő: %s, extra: %s)' % (k, f, e), 'OK' if fo_ok and ex_ok else 'HIBA',
               'fő %d token, extra %d token' % (len(fo[k]), len(extra.get(k, []))))


def d_pont():
    """Kontroll: a F85.8-ban kivezetett 4 'nem átkulcsolt vers' kézi sor visszaállítva sem változtatná a betöltést (tehát inertek voltak)."""
    alap = tokenek.betolt_eredeti()
    mai = tokenek.VERSMEGF_KEZI
    tmp = os.path.join(tempfile.mkdtemp(prefix='f85_kezi4_'), 'kezi.tsv')
    szoveg = 'karoli' + chr(9) + 'eredeti' + chr(9) + 'tipus' + chr(10) + chr(9) + 'Ézs 9:20' + chr(9) + 'nincs_karoli' + chr(10)
    szoveg += 'Ézs 64:1' + chr(9) + chr(9) + 'torol' + chr(10) + chr(9) + 'Ézs 64:1' + chr(9) + 'torol' + chr(10)
    open(tmp, 'wb').write(szoveg.encode('utf-8'))
    tokenek.VERSMEGF_KEZI = tmp
    try:
        e = tokenek.betolt_eredeti()
    except SystemExit as ex:
        tokenek.VERSMEGF_KEZI = mai
        jelent('d', 'a kivezetett 4 sor visszaállítva: a betöltés megszakad (nem inert; nem állítható vissza)', 'OK', str(ex)[:160])
        return
    finally:
        tokenek.VERSMEGF_KEZI = mai
    kul = [k for k in set(alap) | set(e) if alap.get(k) != e.get(k)]
    jelent('d', 'a kivezetett 4 sor (Ézs 9:20 nincs_karoli, Ézs 64:1 torol x2) visszaállítva: a betöltés változatlan', 'OK' if not kul else 'HIBA', '%d eltérő kulcs' % len(kul))


def f_pont():
    """Az `egyesit.ellenoriz()` (a `egyesit.py --ellenoriz` függvénye) mind a 19 meglévő táblapárra, az új pipeline-nal."""
    futott = sorted({os.path.basename(p)[len('parok_'):-4] for p in glob.glob(os.path.join(ROOT, 'adat', 'karoli_strong', 'parok_*.tsv'))})
    ascii_konyv = {egyesit.sonnet_koteg.ascii_nev(b): b for b in tuple(tokenek.VERSBEOSZTAS_JOVAHAGYOTT) + ('1Móz',)}
    ossz = 0
    for n in futott:
        konyv = ascii_konyv.get(n)
        if konyv is None:
            continue
        hk = egyesit.ellenoriz(konyv)
        ossz += 1
        jelent('f', 'egyesit.ellenoriz: ' + konyv, 'OK' if not hk else 'HIBA', 'rendben' if not hk else '%d hiba: %s' % (len(hk), '; '.join(hk[:3])))
    jelent('f', 'egyesit.ellenoriz összesen', 'OK' if ossz == 19 else 'HIBA', '%d könyv' % ossz)


def sha_ellenorzes():
    ki = {}
    for p in sorted(glob.glob(os.path.join(ROOT, 'adat', 'karoli_strong', '*.tsv'))):
        ki[os.path.basename(p)] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    r = subprocess.run(['git', 'diff', '--quiet', BASE, '--', 'adat'], cwd=ROOT)
    jelent('c', 'adat/ (benne parok_*/szavak_*) a git szerint változatlan az átkulcsolás előtti állapothoz képest', 'OK' if r.returncode == 0 else 'HIBA', '%d adat/karoli_strong fájl' % len(ki))


def main():
    regi = a_pont()
    tmp = tempfile.mkdtemp(prefix='f85_regi_')
    ut = {}
    for nev in ('konkordancia/TAHOT_kivonat.tsv', 'f22/versmegfeleltetes.tsv', 'f22/versmegfeleltetes_kezi.tsv', 'f22/versosszevonas.tsv'):
        p = os.path.join(tmp, os.path.basename(nev))
        open(p, 'wb').write(git_show(nev))
        ut[nev] = p
    regi_tmp = (ut['konkordancia/TAHOT_kivonat.tsv'], ut['f22/versmegfeleltetes.tsv'], ut['f22/versmegfeleltetes_kezi.tsv'], ut['f22/versosszevonas.tsv'])
    b_pont(regi_tmp)
    c_pont(regi_tmp)
    e_pont(regi_tmp)
    f_pont()
    d_pont()
    sha_ellenorzes()
    with open(KI_TSV, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# GENERÁLT: eszkozok/tahot_verskulcs_igazolas.py | a(z) %s (átkulcsolás előtti) állapot és a mostani fa összevetése | ts=2026-10-09\n' % BASE)
        fh.write('# proveniencia: scope=manual (a repó saját fájljainak csak-olvasó összevetése: git show %s vs. a mostani fa; egyesit.epit/ellenoriz memóriában) | forras=konkordancia/TAHOT_kivonat.tsv, naplok/F85_kulcsvaltas.tsv, f22/*.tsv, adat/karoli_strong/parok_*.tsv, szavak_*.tsv, f22/valaszok/ | ts=%s\n' % (BASE, IDOPONT))
        fh.write('pont\ttargy\teredmeny\treszlet\n')
        for r in sor_ki:
            fh.write('\t'.join(x.replace('\t', ' ') for x in r) + '\n')
    hibak = [r for r in sor_ki if r[2] == 'HIBA']
    with open(KI_MD, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# F85_igazolas.md — az átkulcsolás és a kivezetés utólagos igazolása\n\n')
        fh.write('*Generálta: `eszkozok/tahot_verskulcs_igazolas.py` (csak olvas). Alap: `%s` (az átkulcsolás előtti állapot). Összesen %d vizsgálat, %d HIBA.*\n\n' % (BASE, len(sor_ki), len(hibak)))
        fh.write('*proveniencia: scope=manual (csak-olvasó összevetés: git show %s vs. a mostani fa; egyesit.epit/ellenoriz memóriában) | forras=konkordancia/TAHOT_kivonat.tsv, naplok/F85_kulcsvaltas.tsv, f22/*.tsv, adat/karoli_strong/*.tsv, f22/valaszok/ | ts=%s*' % (BASE, IDOPONT) + chr(10) * 2)
        fh.write('| pont | tárgy | eredmény | részlet |\n|---|---|---|---|\n')
        for r in sor_ki:
            fh.write('| %s | %s | %s | %s |\n' % tuple(x.replace('|', '/') for x in r))
    print('írva: %s, %s; HIBA: %d' % (KI_TSV, KI_MD, len(hibak)))
    return 1 if hibak else 0


if __name__ == '__main__':
    sys.exit(main())
