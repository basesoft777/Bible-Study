#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_diff_osztalyoz.py — RENDER_BRIEF.md R2.6: a 2. menetben újragenerált
`lexikon/*_TUDOMANYOS.md` és `lexikon/*_TORZSCIKK.md` fájlok git-diffjének
soronkénti osztályozása.

Minden változott (hozzáadott vagy törölt) sornak pontosan egy kategóriába
kell esnie -- a besorolás a sor TARTALMA szerint dől el, nem a mögöttes
forrásfájl útvonala szerint:
  - tanulmany      -- egy `tanulmany`-forrású rés törzse (akár a tematikus
                       tanulmányból, akár egy kereszthivatkozás-naplóból,
                       l. G14 `minosites`) -- rés-forrás, nem szerkesztői
                       megjegyzés
  - kivonat        -- a `## Kivonat` szakasz (G10, R2.2)
  - fejlec         -- egy rés fejléc-sorának szövege (G11, a 2/b-egységesítés)
  - naplo          -- kizárólag a 【NAPLO: ...】 folyamat-jelölő blokkok
                       sorai (akár egy tanulmányban, akár egy naplóban
                       állnak) -- l. G13/D24
  - jeloles        -- a fájl-szintű GENERÁLT gépi jelölés (R2.5)
  - torzscikk_res   -- bármely `_TORZSCIKK.md`-beli változás (a törzscikk
                       önálló forrás nélkül renderel, l. RENDER_BRIEF G7)
  - adat_res       -- a `forras=adat` rések (G16/D26 + KIRALY-001, D28)
                       generált sora, motívumonként egy (várt: 7)

Ismeretlen kategóriájú sor esetén a szkript kóddal (2) lép ki -- ez az R2.6
"ÁLLJ" jele; a hívó ilyenkor nem commitol.

TSV-olvasás kizárólag split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import difflib
import io
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lexikon_general as LG  # noqa: E402

ROOT = LG.ROOT
LEXIKON_DIR = os.path.join(ROOT, 'lexikon')

KATEGORIAK = ('tanulmany', 'kivonat', 'fejlec', 'naplo', 'jeloles', 'torzscikk_res', 'adat_res')

# D28 (RENDER_BRIEF.md v5): a forras=adat rések (G16/D26 + a KIRALY-001
# döntés, N19) generált sorai saját kategóriát kapnak -- ezek a G16
# alapértelmezés szerinti "A motívumhoz nincs rögzített kapcsolat." mondat
# (6 motívum) és a KIRALY-001 egyedi mondata, motívumonként egy sor.
ADAT_RES_VART_DARAB = 7

_UJ_2B_FEJLEC = '### 2/b. Kiegészítő szótári adatok *(kézi)*'
_LEGACY_2B_FEJLEC = '### 2/b *(kézi, ha van)*'
_NAPLO_BLOKK_RE = re.compile(r'【NAPLO.*?】', re.DOTALL)


def naplo_blokk_sorok(szoveg):
    """Minden sor, amely egy 【NAPLO...】 blokk RÉSZE (a blokk akár több
    soron át fut) -- ezek G13/D24 értelmében 'naplo' kategóriájú tartalom,
    függetlenül attól, hogy egy tanulmányban vagy egy kereszthivatkozás-
    naplóban élnek."""
    sorok = set()
    if not szoveg:
        return sorok
    for m in _NAPLO_BLOKK_RE.finditer(szoveg):
        for ln in m.group(0).splitlines():
            ln = ln.strip()
            if ln:
                sorok.add(ln)
    return sorok


def git_show_head(rel_path):
    rel = rel_path.replace('\\', '/')
    try:
        out = subprocess.run(['git', 'show', 'HEAD:%s' % rel], cwd=ROOT,
                              capture_output=True, check=True)
        return out.stdout.decode('utf-8')
    except subprocess.CalledProcessError:
        return None


def erintett_lexikon_fajlok():
    out = subprocess.run(['git', 'status', '--porcelain', '--', 'lexikon/'],
                          cwd=ROOT, capture_output=True, check=True)
    fajlok = []
    for sor in out.stdout.decode('utf-8').splitlines():
        sor = sor.rstrip('\n')
        if not sor.strip():
            continue
        ut = sor[3:].strip()
        if ut.endswith('.md'):
            fajlok.append(ut)
    return sorted(fajlok)


def valtozott_sorok(regi_szoveg, uj_szoveg):
    """(hozzáadott sorszövegek, törölt sorszövegek) -- csak a ténylegesen
    változott (nem közös) sorok, üres sorok nélkül."""
    regi_sorok = regi_szoveg.splitlines() if regi_szoveg is not None else []
    uj_sorok = uj_szoveg.splitlines()
    sm = difflib.SequenceMatcher(a=regi_sorok, b=uj_sorok, autojunk=False)
    hozzaadott, torolt = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('replace', 'insert'):
            hozzaadott.extend(uj_sorok[j1:j2])
        if tag in ('replace', 'delete'):
            torolt.extend(regi_sorok[i1:i2])
    hozzaadott = [s for s in hozzaadott if s.strip()]
    torolt = [s for s in torolt if s.strip()]
    return hozzaadott, torolt


def res_hatarok(motivum_id, szoveg):
    """{res: (kezdő sorszám, végző sorszám)} -- 1-indexelt, a res_forras.tsv
    _BOUNDARY_SLOTS sorrendje szerint, a JELEN (regenerált) szövegben."""
    sorok = LG.res_forras_sorok()
    sorok_szoveg = szoveg.splitlines()

    def sor_szama(char_offset):
        return szoveg.count('\n', 0, char_offset) + 1

    offsets = []
    search_from = 0
    for kind, ertek in LG._BOUNDARY_SLOTS:
        if kind == 'lit':
            i, _ = LG._boundary_index(szoveg, ertek, search_from, None)
        else:
            masik_sor = sorok.get((motivum_id, ertek))
            i, _ = LG._boundary_index(szoveg, masik_sor['fejlec'], search_from, ertek)
        offsets.append(i)
        search_from = i
    hatarok = {}
    for idx, (kind, ertek) in enumerate(LG._BOUNDARY_SLOTS):
        if kind == 'res':
            hatarok[ertek] = (sor_szama(offsets[idx]), sor_szama(offsets[idx + 1]))
    return hatarok, sorok_szoveg


def _forras_szoveg_cache():
    cache = {}

    def get(relativ_ut):
        if relativ_ut not in cache:
            teljes = os.path.join(ROOT, relativ_ut)
            if os.path.exists(teljes):
                with io.open(teljes, encoding='utf-8', newline='') as f:
                    cache[relativ_ut] = f.read()
            else:
                cache[relativ_ut] = ''
        return cache[relativ_ut]
    return get


_forras_get = _forras_szoveg_cache()


def osztalyoz(fajl_rel, hozzaadott, torolt, uj_szoveg, regi_szoveg, motivum_id):
    fajl_nev = os.path.basename(fajl_rel)
    kategoriak = {}

    if fajl_nev.endswith('_TORZSCIKK.md'):
        for sor in hozzaadott + torolt:
            kategoriak.setdefault('torzscikk_res', []).append(sor)
        return kategoriak

    # ## Kivonat szakasz sorai (a szakasz-fejléc utáni, a Tartalomjegyzékig)
    _, sorok_szoveg = res_hatarok(motivum_id, uj_szoveg)
    kivonat_sorok = set()
    try:
        i_kiv = sorok_szoveg.index('## Kivonat *(kézi)*')
        i_toc = next(i for i in range(i_kiv, len(sorok_szoveg))
                     if sorok_szoveg[i].startswith('## Tartalomjegyzék'))
        kivonat_sorok = set(s for s in sorok_szoveg[i_kiv:i_toc] if s.strip())
    except (ValueError, StopIteration):
        pass

    res_fejlec_szovegek = set()
    forras_lista = []  # [(res, forras, ut_vagy_mondat)]
    for (mid, res), sor in LG.res_forras_sorok().items():
        if mid == motivum_id:
            res_fejlec_szovegek.add(sor['fejlec'])
            forras_lista.append((res, sor['forras'], sor.get('tanulmany')))

    # G13/D24: 【NAPLO...】 blokkok -- akár a lexikonoldal régi/új
    # állapotában, akár a mögöttes tanulmány/napló-fájl aktuális
    # szövegében állnak, 'naplo' kategóriájúak (nem csak a napló-FÁJL-ból
    # jövő tartalom).
    naplo_sorok = naplo_blokk_sorok(uj_szoveg) | naplo_blokk_sorok(regi_szoveg)
    for res, forras, ut in forras_lista:
        if forras == 'tanulmany' and ut:
            naplo_sorok |= naplo_blokk_sorok(_forras_get(ut))

    def egy_sor_kategoria(sor_szoveg):
        s = sor_szoveg.strip()
        if s.startswith('<!-- GENERÁLT: general.py --cel lexikon | rések:'):
            return 'jeloles'
        if s in (_UJ_2B_FEJLEC, _LEGACY_2B_FEJLEC) or s in res_fejlec_szovegek:
            return 'fejlec'
        if s in kivonat_sorok:
            return 'kivonat'
        if s in naplo_sorok:
            return 'naplo'

        # rés-törzs: a forrás (tanulmány- vagy kereszthivatkozás-napló fájl,
        # vagy adatból írt mondat) ténylegesen tartalmazza-e ezt a sort?
        # A 'naplo' kategória a TARTALOM szerint dől el (【NAPLO: ...】
        # blokk-e, fent már ellenőrizve), NEM a forrásfájl útvonala szerint
        # -- a kereszthivatkozás-napló `minosites` rés-tartalma G14 szerint
        # rés-forrás, tehát 'tanulmany' kategóriájú, akkor is, ha maga a
        # forrásfájl egy .../naplok/ alatti napló.
        for res, forras, ut in forras_lista:
            if forras == 'tanulmany' and ut:
                forras_szoveg = _forras_get(ut)
                if s and s in forras_szoveg:
                    return 'tanulmany'
            elif forras == 'adat' and ut and s == ut.strip():
                return 'adat_res'
        # nem azonosítható forrás-fájlban szó szerint (jellemzően a RÉGI,
        # felülírt tartalom: "*Kézzel írandó*" helyőrző-próza vagy elavult
        # al-fejléc) -- ez a rés-törzs cseréjének RÉGI oldala, tehát
        # 'tanulmany' kategória.
        return 'tanulmany'

    for sor in hozzaadott + torolt:
        kat = egy_sor_kategoria(sor)
        kategoriak.setdefault(kat if kat is not None else '(azonosítatlan)', []).append(sor)

    return kategoriak


def main():
    fajlok = erintett_lexikon_fajlok()
    if not fajlok:
        print('Nincs változott lexikon/*.md fájl.')
        return 0

    osszesito = {k: 0 for k in KATEGORIAK}
    ismeretlen_talalt = False
    adat_res_motivumok = set()

    for fajl_rel in fajlok:
        fajl_ut = os.path.join(ROOT, fajl_rel)
        motivum_id = os.path.basename(fajl_rel).split('_')[0]
        with io.open(fajl_ut, encoding='utf-8', newline='') as f:
            uj_szoveg = f.read()
        regi_szoveg = git_show_head(fajl_rel)
        hozzaadott, torolt = valtozott_sorok(regi_szoveg, uj_szoveg)
        if not hozzaadott and not torolt:
            continue
        kategoriak = osztalyoz(fajl_rel, hozzaadott, torolt, uj_szoveg, regi_szoveg, motivum_id)
        sor_darab = {k: len(v) for k, v in kategoriak.items()}
        print('%s: %s' % (fajl_rel, ', '.join(
            '%s=%d' % (k, v) for k, v in sorted(sor_darab.items()))))
        for k, v in sor_darab.items():
            if k not in KATEGORIAK:
                ismeretlen_talalt = True
                print('  ISMERETLEN KATEGÓRIA: %s (%d sor)' % (k, v), file=sys.stderr)
            else:
                osszesito[k] += v
                if k == 'adat_res':
                    adat_res_motivumok.add(motivum_id)

    print()
    print('Összesítő kategóriánként: %s'
          % ', '.join('%s=%d' % (k, osszesito[k]) for k in KATEGORIAK))

    if osszesito['adat_res'] != ADAT_RES_VART_DARAB:
        print('ÁLLJ: adat_res sorszám %d, várt %d (motívumok: %s).'
              % (osszesito['adat_res'], ADAT_RES_VART_DARAB,
                 ', '.join(sorted(adat_res_motivumok))), file=sys.stderr)
        return 2

    if ismeretlen_talalt:
        print('ÁLLJ: ismeretlen kategóriájú sor(ok) a diffben.', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
