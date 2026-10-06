#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
naplok/F56_minta.py -- F56 M3: a 20 mintablokk eloállítása és szúrópróbája.

A szúrópróba a blokk kódjától FÜGGETLEN útvonalon, a nyers fájlokból (split('\t'))
számolja újra szocikkenként legalább 2 adatot (az 1. Károli-szóalak darabszáma; az 1.
példavers; az 1. LXX-sor), és a nyers forrássort kiírja.

    python naplok/F56_minta.py            # naplok/BDB_ADATBLOKK_minta.md
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import bdb_adatblokk as B  # noqa: E402

TS = '2026-10-06T12:00:00Z'
KI = os.path.join(REPO, 'naplok', 'BDB_ADATBLOKK_minta.md')


def sorrend():
    d = {}
    for m in B.tsv_sorok(B.SORREND_UT):
        if m[0] == 'sorszam':
            continue
        d[int(m[0])] = m[1]
    return d


def nyers_karoli_darab(szam, alak):
    """Nyers fajlokbol: (magas, alacsony, elso nyers sor)."""
    mag = alc = 0
    elso = None
    for fn in sorted(os.listdir(B.PAROK_MAPPA)):
        if not fn.startswith('parok_'):
            continue
        with open(os.path.join(B.PAROK_MAPPA, fn), encoding='utf-8') as fh:
            for sor in fh.read().split('\n'):
                if not sor or sor.startswith('#'):
                    continue
                m = sor.split('\t')
                if re.match(r'^H0*%d$' % szam, m[5]) and m[2].lower() == alak:
                    if m[6] == 'magas':
                        mag += 1
                    else:
                        alc += 1
                    if elso is None:
                        elso = (fn, sor)
    return mag, alc, elso


def ellenorzes(strong, blokk):
    szam = B.strong_szam(strong)
    sorok = []
    ok = True
    # 1. az elso Károli-szóalak darabszáma (magas-sor, ha van; különben az alacsony)
    m = re.search(r'magas bizonyosságú pár: (?:—|([^\n]*))', blokk)
    sor1 = re.search(r'- magas bizonyosságú pár: ([^\n]+)', blokk).group(1)
    sor2 = re.search(r'- alacsonyabb bizonyosságú pár \(`alacsony`\): ([^\n]+)', blokk)
    if '[NINCS KÁROLI-ALAK]' in blokk:
        sorok.append('- 1. Károli: `[NINCS KÁROLI-ALAK]`; nyers ellenőrzés: a `parok_*.tsv`-ben `H%d` sora: %d'
                     % (szam, len(B.parok().get(szam, []))))
        ok = ok and not B.parok().get(szam)
    else:
        cel = sor1 if sor1 != '—' else sor2.group(1)
        elso = re.match(r'(\S+) ×(\d+)', cel)
        alak, n = elso.group(1), int(elso.group(2))
        mag, alc, nyers = nyers_karoli_darab(szam, alak)
        egyezik = (mag if sor1 != '—' else alc) == n
        ok = ok and egyezik
        sorok.append('- 1. Károli: `%s` ×%d → nyers `parok_*.tsv` számlálás: magas %d, alacsony %d (%s); első nyers sor: `%s: %s`'
                     % (alak, n, mag, alc, 'EGYEZIK' if egyezik else 'ELTÉR', nyers[0], nyers[1]))
    # 2. az első példavers a Károli_1908.tsv-ben
    pm = re.search(r'\n- \*\*(\S+)\*\*: (\S+ \d+:\d+) „([^”]+)”', blokk)
    if pm:
        vers = pm.group(2)
        idez = pm.group(3).replace('**', '').strip('.').replace('...', '').strip()
        nyers_vers = None
        with open(B.KAROLI_UT, encoding='utf-8') as fh:
            for sor in fh.read().split('\n'):
                if sor.startswith(vers + '\t'):
                    nyers_vers = sor.split('\t', 1)[1]
                    break
        bent = bool(nyers_vers) and idez in nyers_vers
        ok = ok and bent
        sorok.append('- 2. Példavers: `%s` „%s” → a `Karoli_1908.tsv`-ben a vers: „%s” (%s)'
                     % (vers, pm.group(3), (nyers_vers or '')[:160], 'szakasz BENNE VAN' if bent else 'NINCS BENNE'))
    else:
        sorok.append('- 2. Példavers: nincs (a blokkban nincs példa)')
    # 3. LXX
    lm = re.search(r'\*\*3\. LXX-megfelelő\*\*\n(G\d+) (\S+) ×(\d+)', blokk)
    nyers_lxx = [s for s in open(B.LXX_UT, encoding='utf-8').read().split('\n') if s.startswith('H%04d\t' % szam)]
    if lm:
        keres = '\t'.join(['H%04d' % szam, 'G%04d' % int(lm.group(1)[1:]), lm.group(3)])
        bent = keres in nyers_lxx
        ok = ok and bent
        sorok.append('- 3. LXX: `%s %s ×%s` → nyers `lxx_bridge.tsv`-sor: `%s` (%s)'
                     % (lm.group(1), lm.group(2), lm.group(3), keres.replace('\t', ' | '), 'BENNE VAN' if bent else 'NINCS'))
    else:
        ok = ok and not nyers_lxx
        sorok.append('- 3. LXX: „—” → nyers `lxx_bridge.tsv`-ben a `H%04d` sorai: %d' % (szam, len(nyers_lxx)))
    return ok, sorok


def main():
    srt = sorrend()
    k1 = [srt[i] for i in range(177, 187)]
    k2 = [srt[i] for i in range(407, 417)]
    kiv = []
    kiv.append('# F56 M3 — Mintablokk (20 szocikk) · elfogadási próba\n')
    kiv.append('*Generálja: `python naplok/F56_minta.py` (a blokkok: `python eszkozok/bdb_adatblokk.py --minta ...`, '
               'ts=%s). Minta: a H2617 körüli 10 szócikk (`BDB_FORDITAS_sorrend.tsv` 177–186) és a 6. adag első 10 szócikke '
               '(407–416). A szúrópróba a nyers fájlokból, a blokk kódjától függetlenül számol (szocikkenként 3 adat).*\n' % TS)
    osszes = 0
    jo = 0
    for cim, lista in (('A. A H2617 körül (177–186)', k1), ('B. A 6. adag első 10 szocikke (407–416)', k2)):
        kiv.append('## %s\n' % cim)
        for s in lista:
            blokk = B.blokk_epit(s, TS)
            ok, sorok = ellenorzes(s, blokk)
            osszes += 1
            jo += ok
            kiv.append('### %s\n' % s)
            kiv.append(blokk)
            kiv.append('**Szúrópróba (%s):**\n' % ('MIND EGYEZIK' if ok else 'ELTÉRÉS'))
            kiv.extend(sorok)
            kiv.append('')
    kiv.append('## Összegzés\n')
    kiv.append('- Blokkok: %d; szúrópróba mind egyezik: %d/%d.' % (osszes, jo, osszes))
    with open(KI, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(kiv) + '\n')
    print('irva: %s; %d/%d' % (KI, jo, osszes))


if __name__ == '__main__':
    main()
