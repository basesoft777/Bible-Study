#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21 P-K1 — sorrend-ellenőrzés a nyers TAHOT/TAGNT #01, #02... sorszámával.

Kérdés: a TAHOT/TAGNT-kivonat sorai egy versen belül a szórendben állnak-e,
vagyis a versen belüli sorszám (tokenek.betolt_eredeti) a sor helyéből
származtatható-e? (F22 22.0/3: ha nem, meg kell állni és jelezni.)

Módszer (két lépés):
  A) a nyers fájlban egy nyers vers (Gen.1.1, ill. a zárójeles kettős alak
     Gen.31.55(32.1) külön csoportként) #NN sorszámai a fájlsorrendben
     növekvők-e. A nyers fájl a változatsorokat (X, Q(K) stb.) tizedes-szerű
     sorszámmal szúrja be: a #501 az 5. szó utáni első beszúrt sor, a #0001
     a vers előtti változatblokk első sora. A #NN ezért a *szövegkörnyezet*
     alapján értelmezett: ha a 3+ jegyű szám előtagja (az utolsó két jegy
     nélkül) az utolsó szabályos sorszámmal egyezik, beszúrt sor (base, k);
     különben közönséges sorszám (pl. a 100. szó).
  B) a kivonat minden Károli-versének szósor-sorozata (ragozott alak, fájlsorrend)
     részsorozata-e a nyers fájlsorrendű morféma-sorozat legfeljebb három
     egymás utáni nyers csoportból álló ablakának (az ablak a vers fejezetéhez
     közeli — ±1 fejezet — csoportokból választódik). Az ablakos illesztés
     azért kell, mert a kivonat-generálás a zárójeles nyers sorokat Károli-
     kulcs szerint tette át, így a kivonat globális sorrendje nem egyezik a
     nyers fájlsorrenddel, a versen belüli sorrend viszont igen.
     A TAHOT-nál a héber morféma a '/' szerinti szegmens (a backslash utáni
     írásjel-kód elhagyva), a TAGNT-nál egy sor = egy szó.

Bemenet: a STEPBible-Data klón 'Translators Amalgamated OT+NT' könyvtára
(--nyers; a repón kívül). A nyers fájlok nem kerülnek a repóba.

Futtatás:
    python eszkozok/karoli_strong/sorrend_ellenoriz.py --nyers <könyvtár> [--jelentes <fájl>]
Kilépési kód 1, ha bármely vers sorrendje vagy részsorozat-illeszkedése hibás.
"""

import argparse
import glob
import os
import re
import subprocess
import sys
from collections import OrderedDict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenek  # noqa: E402

BS = chr(92)
SOR = re.compile(r'^([A-Za-z0-9]+)\.(\d+)\.(\d+)(?:\((\d+)\.(\d+)\))?#(\d+)=(\S*)\t')
HIANYZO_NORM = {}


def nyers_csoportok(fajlok, gorog):
    """[(kulcs, (konyv, ch, v, ch2, v2), [(nn, morfema), ...]), ...] fájlsorrendben."""
    csoportok = OrderedDict()
    for fn in fajlok:
        with open(fn, encoding='utf-8') as f:
            for ln in f:
                m = SOR.match(ln)
                if not m:
                    continue
                c = ln.rstrip('\n').split('\t')
                k, ch, v, ch2, v2, nn = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6)
                if gorog:
                    morf = [c[1].split(' (')[0].strip()]
                else:
                    morf = [x.strip() for x in c[1].split(BS)[0].split('/')]
                kulcs = (k, ch, v, ch2, v2)
                csoportok.setdefault(kulcs, []).extend((nn, x) for x in morf if x)
    return csoportok


def nn_kulcsok(nn_lista):
    """A nyers #NN sorszámok (sztring) rendezhető kulcsai, a beszúrt sorokkal.

    Egy nyers sor több morfémát ad (ugyanaz a #NN ismétlődik), ezt egyszerűsítjük.
    """
    ki = []
    utolso = 0
    elozo = None
    for nn in nn_lista:
        if nn == elozo:
            continue
        elozo = nn
        if len(nn) >= 3 and (int(nn[:-2]) == utolso or (utolso == 0 and not ki and int(nn[:-2]) > 0)):
            # a csoport elején álló 3+ jegyű szám (pl. Neh.7.68: #1401) egy
            # másik csoport sorszámterének beszúrt sora: a bázist átvesszük
            utolso = int(nn[:-2])
            ki.append((utolso, int(nn[-2:])))
        else:
            utolso = int(nn)
            ki.append((utolso, 0))
    return ki


def kulcs_hu(konyv_step, ch, v, step_hu):
    return '%s %s:%s' % (step_hu[konyv_step], int(ch), int(v))


def reszsorozat(kis, nagy):
    """kis részsorozata-e nagy-nak; az első nem illeszkedő kis-index vagy None."""
    i = 0
    for elem in nagy:
        if i < len(kis) and kis[i] == elem:
            i += 1
    return None if i == len(kis) else i


def ablakos_reszsorozat(lista, idxek, lista_cs):
    """True, ha a lista részsorozata az idxek (fájlsorrendű csoportindexek)
    valamelyik legfeljebb 3 egymás utáni csoportból álló ablakának úgy, hogy
    az ablak első és utolsó csoportja is ad legalább egy illeszkedést; False, ha
    egyik ablak sem jó. Üres lista: True."""
    if not lista:
        return True
    elso = lista[0]
    for p, i in enumerate(idxek):
        if elso not in lista_cs[i][2]:
            continue
        for w in (1, 2, 3):
            ablak = idxek[p:p + w]
            if len(ablak) < w:
                break
            # a csoportindexeknek a nyers fájlban egymás után kell állniuk
            if any(ablak[j + 1] != ablak[j] + 1 for j in range(w - 1)):
                break
            j = 0
            hasznalt = set()
            for gi, g in enumerate(ablak):
                for szo in lista_cs[g][2]:
                    if j < len(lista) and lista[j] == szo:
                        j += 1
                        hasznalt.add(gi)
            if j == len(lista) and 0 in hasznalt and (w - 1) in hasznalt:
                return True
    return False


def ellenoriz(nyers_konyvtar, gorog):
    if gorog:
        fajlok = sorted(glob.glob(os.path.join(nyers_konyvtar, 'TAGNT*.txt')))
        kiv_ut = tokenek.TAGNT
    else:
        fajlok = sorted(glob.glob(os.path.join(nyers_konyvtar, 'TAHOT*.txt')))
        kiv_ut = tokenek.TAHOT
    if not fajlok:
        raise SystemExit('nincs nyers fájl: %s' % nyers_konyvtar)
    step_hu = tokenek.konyv_step_to_hu()
    cs = nyers_csoportok(fajlok, gorog)

    # A) #NN szigorúan növekvő a fájlsorrendben
    nn_hibak = []
    for kulcs, sorok in cs.items():
        kulcsok = nn_kulcsok([nn for nn, _ in sorok])
        if any(b <= a for a, b in zip(kulcsok, kulcsok[1:])):
            nn_hibak.append((kulcs, kulcsok[:12]))

    # B) kivonat-vers részsorozata a nyers csoportok fájlsorrendű sorozatának
    lista_cs = []          # (könyv_step, fejezetek halmaza, szavak) fájlsorrendben
    konyvenkent = {}       # könyv -> [csoportindex, ...]
    for kulcs, sorok in cs.items():
        k, ch, v, ch2, v2 = kulcs
        if k not in step_hu:
            continue
        fej = {int(ch)} | ({int(ch2)} if ch2 else set())
        lista_cs.append((k, fej, [m for _, m in sorok]))
        konyvenkent.setdefault(k, []).append(len(lista_cs) - 1)
    hu_step = {v: k for k, v in step_hu.items()}
    kiv = OrderedDict()
    for r in tokenek._sorok(kiv_ut):
        kiv.setdefault(r[0], []).append(r[2].strip() if not gorog else r[2].split(' (')[0].strip())
    reszs_hibak = []
    nincs_jelolt = []
    for ig, lista in kiv.items():
        konyv_hu, ch, _v = tokenek.igehely_bont(ig)
        k = hu_step.get(konyv_hu)
        if k is None or k not in konyvenkent:
            nincs_jelolt.append(ig)
            continue
        kozel = [i for i in konyvenkent[k] if any(abs(f - ch) <= 1 for f in lista_cs[i][1])]
        if ablakos_reszsorozat(lista, kozel, lista_cs) is False:
            # csoportsorrend-csere: a vers két szomszédos nyers csoport szavainak
            # FORDÍTOTT sorrendű összefűzése (a cím vagy az áthozott vers vége a
            # kivonatban a vers végére került, a nyers fájlban az elejére áll)
            fordit = False
            for p in range(len(kozel) - 1):
                a, b = kozel[p], kozel[p + 1]
                if b == a + 1 and lista == lista_cs[b][2] + lista_cs[a][2]:
                    fordit = True
                    break
            reszs_hibak.append((ig, 'csoportsorrend-csere' if fordit else 'egyéb'))
    return {
        'nyers_csoport': len(cs),
        'nyers_morfema': sum(len(s) for s in cs.values()),
        'nn_hibak': nn_hibak,
        'kivonat_versek': len(kiv),
        'kivonat_sorok': sum(len(v) for v in kiv.values()),
        'nincs_jelolt': nincs_jelolt,
        'reszs_hibak': reszs_hibak,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nyers', required=True)
    ap.add_argument('--jelentes')
    ap.add_argument('--eltero', help='a sorrend-eltérő versek TSV-je (igehely, dataset, osztály)')
    a = ap.parse_args()
    try:
        commit = subprocess.run(['git', '-C', os.path.dirname(a.nyers.rstrip('/' + BS)), 'rev-parse', 'HEAD'],
                                capture_output=True, text=True).stdout.strip()
    except Exception:
        commit = '?'
    sorok = ['# F21 P-K1 sorrend-ellenőrzés', '',
             'nyers forrás: STEPBible-Data commit %s' % (commit or '?'), '']
    rossz = False
    eltero = []
    for nev, gorog in (('TAHOT', False), ('TAGNT', True)):
        e = ellenoriz(a.nyers, gorog)
        sorok.append('## %s' % nev)
        sorok.append('- nyers vers-csoport: %d, morféma: %d' % (e['nyers_csoport'], e['nyers_morfema']))
        sorok.append('- #NN nem szigorúan növekvő csoport: %d' % len(e['nn_hibak']))
        for k, n in e['nn_hibak'][:10]:
            sorok.append('  - %s %s' % ('.'.join(x for x in k if x), n))
        sorok.append('- kivonat: %d vers, %d sor' % (e['kivonat_versek'], e['kivonat_sorok']))
        sorok.append('- kivonat-vers nyers megfelelő nélkül: %d %s' % (len(e['nincs_jelolt']), e['nincs_jelolt'][:10]))
        sorok.append('- kivonat-vers, amely NEM részsorozata a nyers fájlsorrendnek: %d'
                     % len(e['reszs_hibak']))
        osztaly = {}
        for ig, o in e['reszs_hibak']:
            osztaly.setdefault(o, []).append(ig)
        for o, l in sorted(osztaly.items()):
            sorok.append('  - %s: %d — %s' % (o, len(l), ', '.join(l)))
        sorok.append('')
        for ig, o in e['reszs_hibak']:
            eltero.append('%s\t%s\t%s' % (ig, nev, o))
        if e['nn_hibak'] or e['reszs_hibak'] or e['nincs_jelolt']:
            rossz = True
    szoveg = '\n'.join(sorok)
    print(szoveg)
    if a.jelentes:
        with open(a.jelentes, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg + '\n')
    if a.eltero:
        with open(a.eltero, 'w', encoding='utf-8', newline='\n') as f:
            f.write('igehely\tdataset\tosztaly\n' + '\n'.join(eltero) + ('\n' if eltero else ''))
    sys.exit(1 if rossz else 0)


if __name__ == '__main__':
    main()
