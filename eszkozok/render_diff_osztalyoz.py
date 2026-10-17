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
#
# DT-F09g: NINCS tartalék-kategória. Minden kategóriának explicit besorolási feltétele van; amelyik
# sor egyik feltételt sem teljesíti, az `ismeretlen` (ISMERETLEN), és a futás kilépési kódja 2 (ÁLLJ).
# A feltételek:
#   szerep_vaz     -- fejléc / ÜRES-jelölő / hivatkozás-sor / rokon-szavak sor a `szocikkek` blokkban, vagy
#                     (törölt, tartalmi sor esetén) a törölt sor tartalma az új kimenetben tovább él
#                     (`tovabb_el`: a normalizált sor vagy minden igehelye megvan a próba szövegében);
#   elavult_adat   -- a `elofordulasok`/`kizart`/`kapcsolatok`/`kereszthivatkozasok`/`tartalom`/`jelmagyarazat`
#                     blokk sora; a TÖRÖLT sorra csak akkor, ha a tartalma a próbában tovább él
#                     (különben `ismeretlen`: eltűnt tartalom, nem igazolt elavulás);
#   fordites_jelzo -- két, azonos normalizált kulcsú sor, amely CSAK a hiányzó fordítás jelzőjében különbözik;
#   kiejtes        -- két, azonos normalizált kulcsú sor, amely a latin betűs zárójeles kiejtésben különbözik,
#                     és a sor héber/görög írásjegyet hordoz;
#   tanulmany      -- generált blokkon KÍVÜLI sor (a 7 kézi rés törzse);
#   torzscikk_res  -- a törzscikk ismert szakaszainak sora (`TORZSCIKK_ISMERT_SZAKASZOK`).
# Besorolhatatlan sor / ismeretlen kategória, vagy változott éles fájl: kilépési kód 2 (ÁLLJ).
# ---------------------------------------------------------------------------

import collections
import hashlib

ISMERETLEN = 'ismeretlen'

PROBA_KATEGORIAK = (
    'kiejtes', 'tbesh', 'ubs_dbh', 'mounce_sece', 'teologiai', 'nyelvi_hatter', 'lxx_korpusz', 'licenc',
    'szerep', 'szerep_vaz', 'elavult_adat', 'fordites_jelzo', 'ismert_hiba_tsk_versszam', 'jeloles', 'tanulmany',
    'torzscikk_res')

# DT-F09g (felhasználói döntés, 2026-10-17): megnevezett táblák, nem általános szabályok.
# 1. Az F87.3 (98f22fc6, DT-F87b) átkulcsolása, ALVIL-001: régi kulcs -> új kulcs (a Károli 1908 szövege szerint
#    a Seol a Préd 9:12-ben és a Jób 17:12-ben áll; a régi kulcs téves volt).
ATKULCSOLT_KULCS = {'Jób 17:13': 'Jób 17:12', 'Jób 17:16': 'Jób 17:15', 'Préd 9:10': 'Préd 9:12'}
# A régi kulcs alatt állt, törölt sorok (motívum, sor) -> a régi kulcs: ezek `elavult_adat`.
ATKULCSOLT_SOROK = {
    ('ALVIL-001', '*A sírnak mondom: Te vagy az én atyám; a férgeknek pedig: Ti vagytok az én anyám és néném.*'): 'Jób 17:13',
    ('ALVIL-001', '*A te ruháid mindenkor legyenek fejérek, és az olaj a te fejedről el ne fogyatkozzék.*'): 'Préd 9:10',
    ('ALVIL-001', '- Károli-KH: Jób 1:21'): 'Jób 17:13',
}
# 2. ISMERT HIBA (N-F09g): a TSK-tábla KJV-számozású, a tsk_index() átváltás nélkül Károli-kulccsal keres; a Préd 9:10
#    alatti 11 TSK-jelölt a KJV 9:10 = Károli 9:12 vershez tartozott, és emiatt veszett el. CSAK ez a 13 sor (12 TSK-jelölt a tudományos oldalon + a törzscikk-oldal összevont sora):
ISMERT_HIBA_TSK_VERSSZAM = {
    ('ALVIL-001', '- TSK: Kol 3:23 (Votes: 71)'), ('ALVIL-001', '- TSK: Ef 5:16 (Votes: 35)'),
    ('ALVIL-001', '- TSK: Róm 12:11 (Votes: 35)'), ('ALVIL-001', '- TSK: Zsolt 6:5 (Votes: 24)'),
    ('ALVIL-001', '- TSK: 1Kor 9:24 (Votes: 19)'), ('ALVIL-001', '- TSK: Préd 11:6 (Votes: 18)'),
    ('ALVIL-001', '- TSK: 2Krón 31:20 (Votes: 17)'), ('ALVIL-001', '- TSK: 2Krón 31:21 (Votes: 17)'),
    ('ALVIL-001', '- TSK: Jer 29:13 (Votes: 17)'), ('ALVIL-001', '- TSK: Mt 6:33 (Votes: 15)'),
    ('ALVIL-001', '- TSK: Ézs 38:19 (Votes: 15)'), ('ALVIL-001', '- TSK: Ézs 38:18 (Votes: 15)'),
    # a törzscikk-oldal ugyanezen 12 jelöltje egy sorban (lexikon/ALVIL-001_TORZSCIKK.md:676)
    ('ALVIL-001', '- **TSK-kereszthivatkozás** (szavazatszám): Kol 3:23 (71), Ef 5:16 (35), Róm 12:11 (35), Zsolt 6:5 (24), 1Kor 9:24 (19), Préd 11:6 (18), 2Krón 31:20 (17), 2Krón 31:21 (17), Jer 29:13 (17), Mt 6:33 (15), Ézs 38:18 (15), Ézs 38:19 (15)'),
}


_BLOKK_KEZDET_RE = re.compile(r'<!-- GENERÁLT-KEZDET: general\.py --cel lexikon#[^#]+#(\w+)')
_SZEREP_FEJ_RE = re.compile(r'^#### (\d+)\. ')
_LATIN_ZAROJEL_RE = re.compile(r"\(([A-Za-zÀ-ɏḀ-ỿ.' \-]+)\)")
_FORDITAS_JELZO_RE = re.compile(r'\*?\(fordítás függőben\)\*?|\*?\(fordításra vár\)\*?|\*Fordítás függőben\.\*')
_FEJLEC_JEL_RE = re.compile(r'^#+ ')

_FEJ_JEL_RE = re.compile(r'^\s*(?:#+\s+|>\s*|[-*]\s+)')
_LABJEGYZET_RE = re.compile(r'\[\^\w+\]')
_KOTTSZEG_RE = re.compile(r'<a id="[^"]*"></a>')
_IGEHELY_RE = re.compile(r'(?<![\w])(?:[1-5]\s?)?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,9}\.? \d{1,3}:\d{1,3}(?:[-–]\d{1,3})?')
_SCRIPT_RE = re.compile('[֐-׿Ͱ-Ͽἀ-῿]')
_VAZ_SOR_RE = re.compile(r'^\s*(?:#+ |<!-- ÜRES-|<!--|---+\s*$|\*\(üres blokk|\*Hivatkozás)')

_LEIRO_RE = re.compile(r'^\*Ez a blokk a `\[ID: [^\]]+\]` motívum')
_URES_ALLAPOT_RE = re.compile(
    r'^(?:Nincs jelentés-hivatkozás a |Nincs kizárt vagy nyitva maradt jelölt |\*A motívumnak nincs görög Strong-tokenje'
    r'|\*H\d+: nincs BDB-sor ehhez a szerephez\.\*)')
_URES_ERTEK_RE = re.compile(r'^\*\*[^*]+:\*\*\s*—\s*$')
_CIMKE_ERTEK_RE = re.compile(r'^\*\*[^*]+:\*\*\s*(.+?)\s*$')

TORZSCIKK_ISMERT_SZAKASZOK = (
    'Kivonat', 'Tartalom', '1. Igehelyek', '2. Kapcsolatok', '3. A kereszthivatkozások',
    '6. Értelmezés', '7. Módszertan', 'Jelmagyarázat')

# (nyelv, szerep sorszáma) -> kategória a próba-oldali sorokra a 2. szakaszban
_SZEREP_KATEGORIA = {
    # a szerepmátrix (adat/szotar_szerepek.tsv) forrás-oszlopa szerint; a nem felsorolt (nyelv, szerep) `ismeretlen`
    ('gorog', 1): 'tbesh', ('heber', 1): 'tbesh',
    ('gorog', 2): 'szerep', ('heber', 2): 'szerep',          # Thayer / BDB mélységi szócikk
    ('gorog', 3): 'teologiai', ('heber', 3): 'teologiai',
    ('gorog', 4): 'ubs_dbh', ('heber', 4): 'ubs_dbh',        # UBS DNTG / DBH szemantikai domén
    ('gorog', 5): 'mounce_sece', ('heber', 5): 'ubs_dbh',
    ('gorog', 6): 'lxx_korpusz', ('heber', 6): 'lxx_korpusz',
    ('gorog', 7): 'mounce_sece', ('heber', 7): 'mounce_sece',
    ('gorog', 8): 'nyelvi_hatter', ('heber', 8): 'nyelvi_hatter',
    ('gorog', 9): 'ubs_dbh', ('heber', 9): 'ubs_dbh',
    ('gorog', 10): 'kiejtes', ('heber', 10): 'kiejtes',
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


def _norm(sor):
    """Tartalmi normalizálás a `tovabb_el` összevetéséhez: fejléc-/idézet-/lista-jel, kiemelés, lábjegyzet,
    horgony és a táblázat-szegélyek nélkül, összevont szóközökkel."""
    s = _KOTTSZEG_RE.sub('', sor)
    s = _FEJ_JEL_RE.sub('', s)
    s = _LABJEGYZET_RE.sub('', s)
    s = s.replace('**', '').replace('*', '').replace('`', '').replace('|', ' ')
    return re.sub(r'\s+', ' ', s).strip()


def _forrascimke(n):
    """A normalizált sor forráscímkéje: az első igehely előtti szöveg (pl. `TSK:`, `Károli-KH:`, `[`)."""
    m = _IGEHELY_RE.search(n)
    return n[:m.start()].strip() if m else ''


class ProbaSzoveg(object):
    """A próba normalizált sorai a `tovabb_el` kereséséhez."""

    def __init__(self, sorok):
        self.sorok = []   # (nyers sor első jele, normalizált sor)
        for s in sorok:
            if s.strip():
                self.sorok.append((s.strip()[:1], _norm(s)))
        self.halmaz = set(n for _, n in self.sorok)

    def tovabb_el(self, sor):
        """Hol él tovább a (törölt) sor tartalma a próbában? Szigorú (3. javító menet): ugyanaz a JELÖLT-SOR kell
        a forráscímkéjével együtt --
          'sor'          a normalizált sor egy próba-sorral egyezik;
          'cimke_igehely' ugyanabban a próba-sorban (azonos kezdőjellel) megvan a sor forráscímkéje ÉS minden igehelye;
          'reszlet'      a normalizált sor (legalább 20 jegy) egyetlen próba-sor része;
          'ertek'        `**Címke:** érték` sor: ugyanabban a próba-sorban a címke ÉS az érték is megvan;
        vagy None. Az igehely önmagában (más sorban, címke nélkül) NEM elég."""
        n = _norm(sor)
        if not n:
            return 'sor'
        if n in self.halmaz:
            return 'sor'
        jel = sor.strip()[:1]
        ige = _IGEHELY_RE.findall(n)
        cimke = _forrascimke(n)
        if ige:
            for j, pn in self.sorok:
                if j == jel and cimke in pn and all(i in pn for i in ige):
                    return 'cimke_igehely'
        if len(n) >= 20 and any(n in pn for _, pn in self.sorok):
            return 'reszlet'
        m = _CIMKE_ERTEK_RE.match(sor.strip())
        if m and len(m.group(1)) >= 2 and m.group(1) != '—':
            c = re.match(r'^\*\*([^*]+:)\*\*', sor.strip())
            if c and any(c.group(1) in pn and m.group(1) in pn for _, pn in self.sorok):
                return 'ertek'
        return None


def _par_kategoria(egyik, masik):
    """Két, azonos normalizált kulcsú sor eltérésének oka; ha a szerkezeti / jelző / kiejtés-feltétel egyike
    sem teljesül, None (a hívó a sor saját blokkja szerint osztályoz, tartalék nélkül: DT-F09g)."""
    a, b = _FEJLEC_JEL_RE.sub('', egyik.strip()), _FEJLEC_JEL_RE.sub('', masik.strip())
    if a == b:
        return 'szerep_vaz'  # csak a fejléc mélysége
    if _FORDITAS_JELZO_RE.sub('(F)', a) == _FORDITAS_JELZO_RE.sub('(F)', b):
        return 'fordites_jelzo'
    ga, gb = _LATIN_ZAROJEL_RE.findall(a), _LATIN_ZAROJEL_RE.findall(b)
    if ga != gb and _SCRIPT_RE.search(a + b):
        return 'kiejtes'
    return None


_ADAT_BLOKKOK = ('elofordulasok', 'kizart', 'kapcsolatok', 'kereszthivatkozasok', 'tartalom', 'jelmagyarazat')


def _tudomanyos_kategoria(sor, kontextus, irany, proba=None, motivum=None):
    s = sor.strip()
    if irany == 'torolt' and (motivum, s) in ISMERT_HIBA_TSK_VERSSZAM:
        return 'ismert_hiba_tsk_versszam'
    if irany == 'torolt' and ATKULCSOLT_KULCS.get(ATKULCSOLT_SOROK.get((motivum, s))):
        return 'elavult_adat'  # F87.3 átkulcsolás: a régi kulcs sora
    blokk, nyelv, szerep, rokon = kontextus
    if blokk in ('idezes', 'kolofon', 'lxx'):
        # a törölt sor csak akkor besorolt, ha a tartalma tovább él (3. javító menet); különben ismeretlen
        if irany == 'torolt' and proba is not None and proba.tovabb_el(s) is None:
            return ISMERETLEN
        return 'licenc' if blokk != 'lxx' else 'lxx_korpusz'
    if _LEIRO_RE.match(s) or _URES_ALLAPOT_RE.match(s) or (irany == 'torolt' and _URES_ERTEK_RE.match(s)):
        # blokk-leíró mondat / üres-állapot jelzés / értéktelen címkesor: sablonmondat, amely a blokk adatából
        # számolt számot vagy az üresség tényét hordozza -- a blokk szerint besorolva (adatot nem hordoz)
        if blokk == 'szocikkek':
            return 'szerep_vaz'
        if blokk in _ADAT_BLOKKOK:
            return 'elavult_adat'
    if blokk in _ADAT_BLOKKOK:
        # az éles oldal adatrétege régebbi; törölt sor csak akkor elavult, ha a tartalma tovább él
        if irany == 'torolt' and proba is not None and proba.tovabb_el(s) is None:
            return ISMERETLEN
        return 'elavult_adat'
    if blokk == 'szocikkek':
        if irany == 'torolt':
            if _VAZ_SOR_RE.match(s):
                return 'szerep_vaz'  # az éles oldal régi, Strong-sorrendű 2. szakaszának váz-sora
            # tartalmi sor: csak akkor váz-áthelyezés, ha a tartalma az új kimenetben tovább él
            if proba is not None and proba.tovabb_el(s) is not None:
                return 'szerep_vaz'
            return ISMERETLEN
        if s.startswith('### ') or _SZEREP_FEJ_RE.match(s) or s.startswith('<!-- ÜRES-') \
                or s.startswith('*(üres blokk') or s.startswith('*Hivatkozás') or rokon:
            return 'szerep_vaz'
        return _SZEREP_KATEGORIA.get((nyelv, szerep), ISMERETLEN)
    if blokk is None:
        return 'tanulmany'  # generált blokkon kívüli sor: a 7 kézi rés törzse
    return ISMERETLEN  # ismeretlen generált blokk


def _torzscikk_kategoria(sor, szakasz, irany='hozzaadott', proba=None, motivum=None):
    s = sor.strip()
    if irany == 'torolt' and (motivum, s) in ISMERT_HIBA_TSK_VERSSZAM:
        return 'ismert_hiba_tsk_versszam'
    kat = _torzscikk_kat(sor, szakasz)
    if irany == 'torolt' and kat != ISMERETLEN and proba is not None and proba.tovabb_el(s) is None:
        return ISMERETLEN   # a törölt sor tartalma sehol nem él tovább
    return kat


def _torzscikk_kat(sor, szakasz):
    if sor.strip().startswith('| **Fő szavak**'):
        return 'kiejtes'
    if szakasz.startswith('5. Szótári'):
        return 'szerep'
    if szakasz.startswith('Források és licenc'):
        return 'licenc'
    if szakasz.startswith('4. LXX'):
        return 'lxx_korpusz'
    if szakasz == '' or szakasz.startswith(TORZSCIKK_ISMERT_SZAKASZOK):  # '' = az első ## előtti fejléc
        return 'torzscikk_res'
    return ISMERETLEN


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
    proba_sz = ProbaSzoveg(proba)

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
            pk = _par_kategoria(s, partner[0])
            if pk is not None:
                return pk
        # azonos normalizált kulcsú partner: a sor tartalma a partnerben él tovább, a túlélés-próba felesleges
        pv = None if partner else proba_sz
        if torzscikk:
            return _torzscikk_kategoria(s, k, irany, pv, fajl_nev.split('_')[0])
        return _tudomanyos_kategoria(s, k, irany, pv, fajl_nev.split('_')[0])

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
    ismeretlen_sorok = ['fajl\tirany\tsor']
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
                print('ISMERETLEN KATEGÓRIA: %s %s (%d sor)' % (f, kat, h + t), file=sys.stderr)
                for irany in ('hozzaadott', 'torolt'):
                    for s in eredmeny[kat][irany]:
                        ismeretlen_sorok.append('\t'.join([f, irany, s.strip()]))
    sorok.append('# összesítő (hozzáadott + törölt sor): ' + ', '.join(
        '%s=%d' % (k, osszes[k]) for k in PROBA_KATEGORIAK if osszes[k])
        + ', %s=%d' % (ISMERETLEN, sum(v for k, v in osszes.items() if k not in PROBA_KATEGORIAK)))
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
    if ismeretlen:
        ism_ut = os.path.splitext(a.tsv)[0].replace('_diff', '') + '_ismeretlen.tsv'
        with io.open(ism_ut, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(ismeretlen_sorok) + '\n')
        print('ismeretlen sorok: %s' % os.path.relpath(ism_ut, ROOT).replace(os.sep, '/'), file=sys.stderr)
    print('\n'.join(sorok))
    if valtozott:
        print('ÁLLJ: az éles lexikon/ fájlja változott: %s' % ', '.join(valtozott), file=sys.stderr)
        return 2
    return 2 if ismeretlen else 0


if __name__ == '__main__':
    if '--proba' in sys.argv:
        sys.exit(proba_main(sys.argv[1:]))
    sys.exit(main())
