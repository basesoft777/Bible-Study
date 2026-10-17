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


# ---------------------------------------------------------------------------
# F09 S2.8: próbarender és az éles lexikon/ összevetése (--proba)
#
# A próba (pl. generalt_proba/F09_szotar_s2_proba) és az éles `lexikon/` MULTIHALMAZ-különbsége
# (a csak áthelyezett, változatlan szövegű sorok nem számítanak változásnak), soronként pontosan
# egy kategóriába. A kategória a sor TARTALMA és KONTEXTUSA (generált blokk, szerep-fejléc,
# törzscikk-szakasz) szerint dől el:
#   az F05 S2.8 kategóriái: kiejtes, tbesh, ubs_dbh, mounce_sece, teologiai, nyelvi_hatter,
#   lxx_korpusz, licenc, szerep (+ a meglévők közül: tanulmany, jeloles, torzscikk_res);
#   szerep_vaz (F09 brief S2.8 javaslata): a #78 váza miatti eltérés (az éles oldal még a régi,
#   Strong-sorrendű 2. szakaszt mutatja), hogy ne fedje el az adatváltozást;
#   két kiegészítő kategória, hogy minden sor besorolható legyen: elavult_adat (az éles oldal
#   adatrétege régebbi: előfordulások, kizárt helyek, kapcsolatok, kereszthivatkozások) és
#   fordites_jelzo (a hiányzó fordítás jelzője egységesült, K13f).
# Besorolhatatlan sor / ismeretlen kategória, vagy változott éles fájl: kilépési kód 2 (ÁLLJ).
# ---------------------------------------------------------------------------

import collections
import hashlib

PROBA_KATEGORIAK = (
    'kiejtes', 'tbesh', 'ubs_dbh', 'mounce_sece', 'teologiai', 'nyelvi_hatter', 'lxx_korpusz', 'licenc',
    'szerep', 'szerep_vaz', 'elavult_adat', 'fordites_jelzo', 'jeloles', 'tanulmany', 'torzscikk_res')

_BLOKK_KEZDET_RE = re.compile(r'<!-- GENERÁLT-KEZDET: general\.py --cel lexikon#[^#]+#(\w+)')
_SZEREP_FEJ_RE = re.compile(r'^#### (\d+)\. ')
_LATIN_ZAROJEL_RE = re.compile(r"\(([A-Za-zÀ-ɏḀ-ỿ.' \-]+)\)")
_FORDITAS_JELZO_RE = re.compile(r'\*?\(fordítás függőben\)\*?|\*?\(fordításra vár\)\*?|\*Fordítás függőben\.\*')
_FEJLEC_JEL_RE = re.compile(r'^#+ ')

# (nyelv, szerep sorszáma) -> kategória a próba-oldali sorokra a 2. szakaszban
_SZEREP_KATEGORIA = {
    ('heber', 1): 'tbesh', ('gorog', 3): 'teologiai', ('heber', 3): 'teologiai',
    ('gorog', 5): 'mounce_sece', ('heber', 5): 'ubs_dbh', ('heber', 9): 'ubs_dbh',
    ('gorog', 7): 'mounce_sece', ('heber', 7): 'mounce_sece', ('heber', 6): 'lxx_korpusz',
    ('heber', 8): 'nyelvi_hatter', ('gorog', 10): 'kiejtes', ('heber', 10): 'kiejtes',
}


def _tudomanyos_kontextusok(sorok):
    """Soronként (blokk, nyelv, szerep sorszáma, rokon-e): a generált blokk és a 2. szakasz kontextusa."""
    out = []
    blokk, nyelv, szerep, rokon = None, None, None, False
    for s in sorok:
        m = _BLOKK_KEZDET_RE.search(s)
        if m:
            blokk, nyelv, szerep, rokon = m.group(1), None, None, False
        if blokk == 'szocikkek':
            if s.startswith('### Görög szavak'):
                nyelv, szerep, rokon = 'gorog', None, False
            elif s.startswith('### Héber szavak'):
                nyelv, szerep, rokon = 'heber', None, False
            elif s.startswith('### Nyelvfüggetlen'):
                nyelv, szerep, rokon = 'kozos', None, False
            elif s.startswith('### Rokon szavak'):
                nyelv, szerep, rokon = None, None, True
            else:
                mm = _SZEREP_FEJ_RE.match(s)
                if mm:
                    szerep = int(mm.group(1))
        out.append((blokk, nyelv, szerep, rokon))
        if s.startswith('<!-- GENERÁLT-VÉGE'):
            blokk, nyelv, szerep, rokon = None, None, None, False
    return out


def _torzscikk_kontextusok(sorok):
    cur, out = '', []
    for s in sorok:
        if s.startswith('## '):
            cur = s[3:]
        out.append(cur)
    return out


def _feleslegek(sorok, kontextusok, sajat, masik):
    """A multihalmaz-többlet sorai (sor, kontextus), az oldal sorrendjében."""
    latott, ki = collections.Counter(), []
    for s, k in zip(sorok, kontextusok):
        if not s.strip():
            continue
        latott[s] += 1
        if latott[s] <= sajat[s] - masik[s]:
            ki.append((s, k))
    return ki


def _kulcs(sor):
    """Normalizált kulcs: a fejléc-# jelek, a latin betűs zárójeles kiejtés és a fordítás-jelző nélkül."""
    s = _FORDITAS_JELZO_RE.sub('(F)', _FEJLEC_JEL_RE.sub('', sor.strip()))
    return _LATIN_ZAROJEL_RE.sub('(K)', s)


def _par_kategoria(egyik, masik):
    """Két, azonos normalizált kulcsú sor eltérésének oka."""
    a, b = _FEJLEC_JEL_RE.sub('', egyik.strip()), _FEJLEC_JEL_RE.sub('', masik.strip())
    if a == b:
        return 'szerep_vaz'  # csak a fejléc mélysége
    if _FORDITAS_JELZO_RE.sub('(F)', a) == _FORDITAS_JELZO_RE.sub('(F)', b):
        return 'fordites_jelzo'
    return 'kiejtes'


def _tudomanyos_kategoria(sor, kontextus, irany):
    s = sor.strip()
    blokk, nyelv, szerep, rokon = kontextus
    if blokk in ('idezes', 'kolofon'):
        return 'licenc'
    if blokk == 'lxx':
        return 'lxx_korpusz'
    if blokk in ('elofordulasok', 'kizart', 'kapcsolatok', 'kereszthivatkozasok', 'tartalom', 'jelmagyarazat'):
        return 'elavult_adat'
    if blokk == 'szocikkek':
        if irany == 'torolt':
            return 'szerep_vaz'  # az éles oldal régi, Strong-sorrendű 2. szakasza
        if s.startswith('### ') or _SZEREP_FEJ_RE.match(s) or s.startswith('<!-- ÜRES-') \
                or s.startswith('*(üres blokk') or s.startswith('*Hivatkozás') or rokon:
            return 'szerep_vaz'
        return _SZEREP_KATEGORIA.get((nyelv, szerep), 'szerep_vaz')
    return 'tanulmany'  # a 7 kézi rés törzse (forrása: tanulmány/napló), a meglévő szabály szerint


def _torzscikk_kategoria(sor, szakasz):
    if sor.strip().startswith('| **Fő szavak**'):
        return 'kiejtes'
    if szakasz.startswith('5. Szótári'):
        return 'szerep'
    if szakasz.startswith('Források és licenc'):
        return 'licenc'
    if szakasz.startswith('4. LXX'):
        return 'lxx_korpusz'
    return 'torzscikk_res'


def proba_osztalyoz(fajl_nev, eles_szoveg, proba_szoveg):
    """{kategória: {'hozzaadott': [sor], 'torolt': [sor]}} a multihalmaz-különbségre."""
    eles = eles_szoveg.replace('\r\n', '\n').split('\n')
    proba = proba_szoveg.replace('\r\n', '\n').split('\n')
    ce, cp = collections.Counter(eles), collections.Counter(proba)
    torzscikk = fajl_nev.endswith('_TORZSCIKK.md')
    if torzscikk:
        ke, kp = _torzscikk_kontextusok(eles), _torzscikk_kontextusok(proba)
    else:
        ke, kp = _tudomanyos_kontextusok(eles), _tudomanyos_kontextusok(proba)
    torolt = _feleslegek(eles, ke, ce, cp)
    hozzaadott = _feleslegek(proba, kp, cp, ce)

    # párosítás: azonos normalizált kulcs => csak kiejtés / jelző / fejléc-mélység változott
    par = collections.defaultdict(list)       # kulcs -> hozzáadott sorok
    par_t = collections.defaultdict(list)     # kulcs -> törölt sorok
    for s, _k in hozzaadott:
        par[_kulcs(s)].append(s)
    for s, _k in torolt:
        par_t[_kulcs(s)].append(s)
    eredmeny = collections.defaultdict(lambda: {'hozzaadott': [], 'torolt': []})

    def kategoria(s, k, irany):
        if s.strip().startswith('<!-- GENERÁLT'):
            return 'jeloles'
        partner = (par if irany == 'torolt' else par_t).get(_kulcs(s))
        if partner:
            return _par_kategoria(s, partner[0])
        if torzscikk:
            return _torzscikk_kategoria(s, k)
        return _tudomanyos_kategoria(s, k, irany)

    for s, k in torolt:
        eredmeny[kategoria(s, k, 'torolt')]['torolt'].append(s)
    for s, k in hozzaadott:
        eredmeny[kategoria(s, k, 'hozzaadott')]['hozzaadott'].append(s)
    return eredmeny


def _sha256(ut):
    with open(ut, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def proba_main(argv):
    import argparse
    p = argparse.ArgumentParser(description='F09 S2.8: próbarender vs. éles lexikon/ diff-osztályozás')
    p.add_argument('--proba', required=True, help='a próba gyökere (alatta lexikon/*.md)')
    p.add_argument('--eles', default=LEXIKON_DIR, help='az éles lexikon/ könyvtár')
    p.add_argument('--tsv', default=os.path.join(ROOT, 'naplok', 'SZOTAR_S2_diff.tsv'))
    p.add_argument('--hash', default=os.path.join(ROOT, 'naplok', 'F09_S0_lexikon_hash.tsv'),
                   help='az éles lexikon/ S0-ban mért hash-ei (változatlansági ellenőrzés)')
    a = p.parse_args(argv)
    proba_lex = os.path.join(a.proba, 'lexikon')
    fajlok = sorted(f for f in os.listdir(proba_lex) if f.endswith('.md'))
    sorok = ['fajl\tkategoria\thozzaadott\ttorolt']
    osszes = collections.Counter()
    ismeretlen = False
    for f in fajlok:
        with io.open(os.path.join(a.eles, f), encoding='utf-8', newline='') as fh:
            eles = fh.read()
        with io.open(os.path.join(proba_lex, f), encoding='utf-8', newline='') as fh:
            proba = fh.read()
        eredmeny = proba_osztalyoz(f, eles, proba)
        for kat in sorted(eredmeny):
            h, t = len(eredmeny[kat]['hozzaadott']), len(eredmeny[kat]['torolt'])
            sorok.append('\t'.join([f, kat, str(h), str(t)]))
            osszes[kat] += h + t
            if kat not in PROBA_KATEGORIAK:
                ismeretlen = True
                print('ISMERETLEN KATEGÓRIA: %s %s' % (f, kat), file=sys.stderr)
    sorok.append('# összesítő (hozzáadott + törölt sor): ' + ', '.join(
        '%s=%d' % (k, osszes[k]) for k in PROBA_KATEGORIAK if osszes[k]))
    sorok.append('# proveniencia: scope=%s vs %s | forras=eszkozok/render_diff_osztalyoz.py --proba | ts=%s'
                 % (os.path.relpath(a.proba, ROOT).replace(os.sep, '/'),
                    os.path.relpath(a.eles, ROOT).replace(os.sep, '/'), os.environ.get('PARDES_DATUM', '')))
    # az éles lexikon/ bájtra változatlan-e (S0.2/7 hash-ei)
    valtozott = []
    with io.open(a.hash, encoding='utf-8') as fh:
        for sor in fh.read().split('\n'):
            m = sor.split('\t')
            if len(m) == 2 and _sha256(os.path.join(a.eles, m[0])) != m[1]:
                valtozott.append(m[0])
    sorok.append('# az éles lexikon/ hash-ellenőrzése (naplok/F09_S0_lexikon_hash.tsv): %s'
                 % ('VÁLTOZOTT: ' + ', '.join(valtozott) if valtozott else '16 fájl bájtra változatlan'))
    with io.open(a.tsv, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(sorok) + '\n')
    print('\n'.join(sorok))
    if valtozott:
        print('ÁLLJ: az éles lexikon/ fájlja változott: %s' % ', '.join(valtozott), file=sys.stderr)
        return 2
    return 2 if ismeretlen else 0


if __name__ == '__main__':
    if '--proba' in sys.argv:
        sys.exit(proba_main(sys.argv[1:]))
    sys.exit(main())
