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
import unicodedata

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
    'szerep', 'szerep_vaz', 'elavult_adat', 'fordites_jelzo', 'ismert_hiba_tsk_versszam', 'felhasznalo_elfogadva', 'jeloles', 'tanulmany',
    'torzscikk_res')

# DT-F09g (felhasználói döntés, 2026-10-17): megnevezett táblák, nem általános szabályok.
# 1. Az F87.3 (98f22fc6, DT-F87b) átkulcsolása, ALVIL-001: régi kulcs -> új kulcs (a Károli 1908 szövege szerint
#    a Seol a Préd 9:12-ben és a Jób 17:12-ben áll; a régi kulcs téves volt).
ATKULCSOLT_KULCS = {'Jób 17:13': 'Jób 17:12', 'Jób 17:16': 'Jób 17:15', 'Préd 9:10': 'Préd 9:12'}
# A régi kulcs alatt állt, törölt sorok (motívum, sor) -> a régi kulcs: ezek `elavult_adat`. NÉV SZERINTI lista (3. javító menet:
# az ALVIL-001 három régi kulcsának összes sora a tudományos és a törzscikk-oldalon), csak törölt irány, csak ALVIL-001.
ATKULCSOLT_SOROK = {
    ('ALVIL-001', '| [Jób 17:13](#v-jób-17-13) | — | Remez | magas · tartalom-alapú |'): 'Jób 17:13',
    ('ALVIL-001', '| [Jób 17:16](#v-jób-17-16) | — | Remez | közepes · tartalom-alapú |'): 'Jób 17:16',
    ('ALVIL-001', '| [Préd 9:10](#v-préd-9-10) | — | Remez | közepes · tartalom-alapú |'): 'Préd 9:10',
    ('ALVIL-001', '### Jób 17:13'): 'Jób 17:13',
    ('ALVIL-001', '> *A sírnak mondom: Te vagy az én atyám; a férgeknek pedig: Ti vagytok az én anyám és néném.*'): 'Jób 17:13',
    ('ALVIL-001', "- **Kulcsszó:** A sírnak — שְׁא֣וֹל (she.'ol)"): 'Jób 17:13',
    ('ALVIL-001', '- **Károli-kereszthivatkozás:** Jób 1:21'): 'Jób 17:13',
    ('ALVIL-001', '### Jób 17:16'): 'Jób 17:16',
    ('ALVIL-001', '> *(Jób 17:16: nincs Károli-szöveg)*'): 'Jób 17:16',
    ('ALVIL-001', '### Préd 9:10'): 'Préd 9:10',
    ('ALVIL-001', '> *A te ruháid mindenkor legyenek fejérek, és az olaj a te fejedről el ne fogyatkozzék.*'): 'Préd 9:10',
    ('ALVIL-001', '- **LXX:** Préd(LXX) 9:8 — — — kutatói azonosítás függőben'): 'Préd 9:10',
    ('ALVIL-001', "| [Jób 17:13](#v-jób-17-13) | — | שְׁא֣וֹל (she.'ol) | — | szamozas_elteres |"): 'Jób 17:13',
    ('ALVIL-001', "| [Jób 17:16](#v-jób-17-16) | — | שְׁאֹ֣ל (she.'Ol) | — | szamozas_elteres |"): 'Jób 17:16',
    ('ALVIL-001', "| [Préd 9:10](#v-préd-9-10) | Préd(LXX) 9:8 | שְׁא֕וֹל (sh.'ol) | — | kutatói azonosítás függőben |"): 'Préd 9:10',
    ('ALVIL-001', "| [Jób 17:13](#ige-jób-17-13) | A sírnak — שְׁא֣וֹל (she.'ol) | — | Remez | H7585 | — | — *(ÓSZ)* | magas · tartalom-alapú[^15] |"): 'Jób 17:13',
    ('ALVIL-001', "| [Jób 17:16](#ige-jób-17-16) | a sír üregébe — שְׁאֹ֣ל (she.'Ol) | — | Remez | H7585 | — | — *(ÓSZ)* | közepes · tartalom-alapú[^16] |"): 'Jób 17:16',
    ('ALVIL-001', "| [Préd 9:10](#ige-préd-9-10) | a Seolban — שְׁא֕וֹל (sh.'ol) | — | Remez | H7585 | — | — *(ÓSZ)* | közepes · tartalom-alapú[^44] |"): 'Préd 9:10',
    ('ALVIL-001', '**Jób 17:13**'): 'Jób 17:13',
    ('ALVIL-001', '**Jób 17:16**'): 'Jób 17:16',
    ('ALVIL-001', '*(Jób 17:16: nincs Károli-szöveg)*'): 'Jób 17:16',
    ('ALVIL-001', '**Préd 9:10**'): 'Préd 9:10',
    ('ALVIL-001', '#### Jób 17:13'): 'Jób 17:13',
    ('ALVIL-001', '#### Préd 9:10'): 'Préd 9:10',
    ('ALVIL-001', '*A sírnak mondom: Te vagy az én atyám; a férgeknek pedig: Ti vagytok az én anyám és néném.*'): 'Jób 17:13',
    ('ALVIL-001', '*A te ruháid mindenkor legyenek fejérek, és az olaj a te fejedről el ne fogyatkozzék.*'): 'Préd 9:10',
    ('ALVIL-001', '- Károli-KH: Jób 1:21'): 'Jób 17:13',
}
# DT-F09g (felhasználó, 2026-10-17, chat): a 32 elfogadott `ismeretlen` sor NÉV SZERINT (fájl + pontos sorszöveg), csak törölt irány.
# Csoportok: forditas_ubs_forras_elavult 14 · joshua_forrasvaltas 2 · bdb_formatumvaltozas 2 · lsj_licencverzio_valtas 1 ·
# szamozas_elteres_fuggobe_valt 6 (kutatói azonosítás függőben lett) · szamozas_elteres_helyorzo_feloldodott 4 (tartalomra oldódott) ·
# kutatoi_azonositas_feloldodott 3 · (2026-10-18) leiro_mondat_bovult 8 · f87_glossza_javitas 4 · (DT-F113b) jelmagyarazat_mondat 8 ·
# kezi_2b_lefedettseg_sece 3. Általános szabály nincs.
FELHASZNALO_ELFOGADOTT = {
    ('ALVIL-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 'forditas_ubs_forras_elavult',
    ('ALVIL-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 'forditas_ubs_forras_elavult',
    ('ANTROP-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 'forditas_ubs_forras_elavult',
    ('ANTROP-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 'forditas_ubs_forras_elavult',
    ('HAMART-001_TORZSCIKK.md', '- **LXX:** Zsolt(LXX) 73:20 — — — kutatói azonosítás függőben'): 'kutatoi_azonositas_feloldodott',
    ('HAMART-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 'forditas_ubs_forras_elavult',
    ('HAMART-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 'forditas_ubs_forras_elavult',
    ('HODIT-001_TORZSCIKK.md', '- **LXX:** — — — — szamozas_elteres'): 'szamozas_elteres_fuggobe_valt',
    ('HODIT-001_TORZSCIKK.md', '- **LXX:** Zsolt(LXX) 87:11 — — — kutatói azonosítás függőben'): 'kutatoi_azonositas_feloldodott',
    ('HODIT-001_TUDOMANYOS.md', '- LXX (Septuaginta — lxx-morph + GreekWordList szövegkorpusz) (`konkordancia/LXX_OS/1-chronicles.tsv`, `konkordancia/LXX_OS/2-samuel.tsv`, `konkordancia/LXX_OS/deuteronomy.tsv`, `konkordancia/LXX_OS/genesis.tsv`, `konkordancia/LXX_OS/isaiah.tsv`, `konkordancia/LXX_OS/job-lxx.tsv`, `konkordancia/LXX_OS/joshua.tsv`, `konkordancia/LXX_OS/numbers.tsv`, `konkordancia/LXX_OS/proverbs.tsv`, `konkordancia/LXX_OS/psalms-lxx.tsv`, CC BY 4.0)'): 'joshua_forrasvaltas',
    ('HODIT-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 'forditas_ubs_forras_elavult',
    ('HODIT-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 'forditas_ubs_forras_elavult',
    ('HODIT-001_TUDOMANYOS.md', '| `joshua.tsv` | `konkordancia/LXX_OS/joshua.tsv` | CC BY 4.0 | lxx |'): 'joshua_forrasvaltas',
    ('ISTENTISZT-001_TORZSCIKK.md', '- LSJ (Liddell-Scott-Jones, A Greek-English Lexicon) — CC BY-SA 3.0'): 'lsj_licencverzio_valtas',
    ('ISTENTISZT-001_TUDOMANYOS.md', '- BDB (Brown–Driver–Briggs, A Hebrew and English Lexicon of the Old Testament, 1906) (`konkordancia/BDB_teljes_unabridged.tsv`, közkincs)'): 'bdb_formatumvaltozas',
    ('KIRALY-001_TORZSCIKK.md', '- **LXX:** Zsolt(LXX) 75:3 — — — kutatói azonosítás függőben'): 'kutatoi_azonositas_feloldodott',
    ('KIRALY-001_TUDOMANYOS.md', '- BDB (Brown–Driver–Briggs, A Hebrew and English Lexicon of the Old Testament, 1906) (`konkordancia/BDB_teljes_unabridged.tsv`, közkincs)'): 'bdb_formatumvaltozas',
    ('KIRALY-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 'forditas_ubs_forras_elavult',
    ('KIRALY-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 'forditas_ubs_forras_elavult',
    ('MENNY-001_TORZSCIKK.md', '- **LXX:** — — — — szamozas_elteres'): 'szamozas_elteres_fuggobe_valt',
    ('MENNY-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 'forditas_ubs_forras_elavult',
    ('MENNY-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 'forditas_ubs_forras_elavult',
    ('TEREMT-001_TORZSCIKK.md', '- **LXX:** — — — — szamozas_elteres'): 'szamozas_elteres_helyorzo_feloldodott',
    ('TEREMT-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 'forditas_ubs_forras_elavult',
    ('TEREMT-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 'forditas_ubs_forras_elavult',
    # felhasználó, 2026-10-18 (chat): a cellánkénti összevetés utáni 12 pár törölt sora (8 leíró mondat bővült; 4 glossza az F87.3 adatjavítása)
    ('ALVIL-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: ALVIL-001]` motívum 2 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 'leiro_mondat_bovult',
    ('ANTROP-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: ANTROP-001]` motívum 4 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 'leiro_mondat_bovult',
    ('HAMART-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: HAMART-001]` motívum 14 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 'leiro_mondat_bovult',
    ('HODIT-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: HODIT-001]` motívum 3 Strong-tokenjét fedi, nincs jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 'leiro_mondat_bovult',
    ('ISTENTISZT-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: ISTENTISZT-001]` motívum 3 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 'leiro_mondat_bovult',
    ('KIRALY-001_TORZSCIKK.md', '- **Kulcsszó:** papok — כֹּהֲנִ֖ים (ko.ha.Nim); מַמְלֶ֥כֶת (mam.Le.khet)'): 'f87_glossza_javitas',
    ('KIRALY-001_TUDOMANYOS.md', '| [2Móz 19:6](#ige-2móz-19-6) | papok — כֹּהֲנִ֖ים (ko.ha.Nim); מַמְלֶ֥כֶת (mam.Le.khet) | egyéni → kollektív szintre emelve | Remez | H3548+H4467 | BDB H3548 1 — egyszerre papok és királyok a nemzetekhez való viszonyukban | — *(ÓSZ)* | magas · tartalom-alapú[^2] |'): 'f87_glossza_javitas',
    ('KIRALY-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: KIRALY-001]` motívum 7 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 'leiro_mondat_bovult',
    ('MENNY-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: MENNY-001]` motívum 3 Strong-tokenjét fedi, nincs jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 'leiro_mondat_bovult',
    ('TEREMT-001_TORZSCIKK.md', '- **Kulcsszó:** a mélységbe — תְּהֹמֹ֖ת (te.ho.Mot)'): 'f87_glossza_javitas',
    ('TEREMT-001_TUDOMANYOS.md', '| [2Móz 15:5](#ige-2móz-15-5) | a mélységbe — תְּהֹמֹ֖ת (te.ho.Mot) | — | Remez | H8415 | — | — *(ÓSZ)* | magas · tartalom-alapú[^5] |'): 'f87_glossza_javitas',
    ('TEREMT-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: TEREMT-001]` motívum 2 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 'leiro_mondat_bovult',
    # felhasználó, 2026-10-18 (DT-F113b (2), #113): a szűkítés után a régi mátrixból sem igazolható 11 törölt sor -- a 3 `kézi (2/b)` lefedettségsor (ISTENTISZT-001) és a 8 jelmagyarázat-mondat
    ('ALVIL-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 'jelmagyarazat_mondat',
    ('ANTROP-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 'jelmagyarazat_mondat',
    ('HAMART-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 'jelmagyarazat_mondat',
    ('HODIT-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 'jelmagyarazat_mondat',
    ('ISTENTISZT-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 'jelmagyarazat_mondat',
    ('ISTENTISZT-001_TORZSCIKK.md', '| G1941 | TBESG | Thayer | nincs adatosítva | UBS DNTG (Louw–Nida) | UBS DNTG glossza + referencia-szám; Mounce kiegészítő | az ÚSZ-szó LXX-háttere: mely héber szavakat ad vissza, mely versekben (lekerdez.py lxx-hid, LXX_OS) | kézi (2/b) | LSJ, ha releváns | UBS DNTG (szópozícióig) | nincs adatosítva |'): 'kezi_2b_lefedettseg_sece',
    ('ISTENTISZT-001_TORZSCIKK.md', '| H7121 | TBESH | BDB | nincs adatosítva | UBS DBH (SDBH) | nincs adatosítva | LXX-fordítói döntés versenként: mely görög szó adja vissza (LXX_OS + adat/lxx_dontesek.tsv; a lexikonoldal 3. szakasza) | kézi (2/b) | nincs adatosítva | nincs adatosítva | nincs adatosítva |'): 'kezi_2b_lefedettseg_sece',
    ('ISTENTISZT-001_TORZSCIKK.md', '| H8034 | TBESH | BDB | nincs adatosítva | UBS DBH (SDBH) | nincs adatosítva | LXX-fordítói döntés versenként: mely görög szó adja vissza (LXX_OS + adat/lxx_dontesek.tsv; a lexikonoldal 3. szakasza) | kézi (2/b) | nincs adatosítva | nincs adatosítva | nincs adatosítva |'): 'kezi_2b_lefedettseg_sece',
    ('KIRALY-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 'jelmagyarazat_mondat',
    ('MENNY-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 'jelmagyarazat_mondat',
    ('TEREMT-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 'jelmagyarazat_mondat',
}
# Az elfogadott sorok ELVÁRT darabszáma kulcsonként (4. ellenőrzés 3. eltérése): fájlonként és kulcsonként legfeljebb ennyi
# törölt sort fogad el az osztályozó, a többlet `ismeretlen`. Az összeg 55 = 32 + 12 + 11 (DT-F113b).
FELHASZNALO_DARAB = {
    ('ALVIL-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: ALVIL-001]` motívum 2 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 1,
    ('ALVIL-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 1,
    ('ALVIL-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 1,
    ('ANTROP-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: ANTROP-001]` motívum 4 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 1,
    ('ANTROP-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 1,
    ('ANTROP-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 1,
    ('HAMART-001_TORZSCIKK.md', '- **LXX:** Zsolt(LXX) 73:20 — — — kutatói azonosítás függőben'): 1,
    ('HAMART-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: HAMART-001]` motívum 14 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 1,
    ('HAMART-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 1,
    ('HAMART-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 1,
    ('HODIT-001_TORZSCIKK.md', '- **LXX:** — — — — szamozas_elteres'): 5,
    ('HODIT-001_TORZSCIKK.md', '- **LXX:** Zsolt(LXX) 87:11 — — — kutatói azonosítás függőben'): 1,
    ('HODIT-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: HODIT-001]` motívum 3 Strong-tokenjét fedi, nincs jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 1,
    ('HODIT-001_TUDOMANYOS.md', '- LXX (Septuaginta — lxx-morph + GreekWordList szövegkorpusz) (`konkordancia/LXX_OS/1-chronicles.tsv`, `konkordancia/LXX_OS/2-samuel.tsv`, `konkordancia/LXX_OS/deuteronomy.tsv`, `konkordancia/LXX_OS/genesis.tsv`, `konkordancia/LXX_OS/isaiah.tsv`, `konkordancia/LXX_OS/job-lxx.tsv`, `konkordancia/LXX_OS/joshua.tsv`, `konkordancia/LXX_OS/numbers.tsv`, `konkordancia/LXX_OS/proverbs.tsv`, `konkordancia/LXX_OS/psalms-lxx.tsv`, CC BY 4.0)'): 1,
    ('HODIT-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 1,
    ('HODIT-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 1,
    ('HODIT-001_TUDOMANYOS.md', '| `joshua.tsv` | `konkordancia/LXX_OS/joshua.tsv` | CC BY 4.0 | lxx |'): 1,
    ('ISTENTISZT-001_TORZSCIKK.md', '- LSJ (Liddell-Scott-Jones, A Greek-English Lexicon) — CC BY-SA 3.0'): 1,
    ('ISTENTISZT-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: ISTENTISZT-001]` motívum 3 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 1,
    ('ISTENTISZT-001_TUDOMANYOS.md', '- BDB (Brown–Driver–Briggs, A Hebrew and English Lexicon of the Old Testament, 1906) (`konkordancia/BDB_teljes_unabridged.tsv`, közkincs)'): 1,
    ('KIRALY-001_TORZSCIKK.md', '- **Kulcsszó:** papok — כֹּהֲנִ֖ים (ko.ha.Nim); מַמְלֶ֥כֶת (mam.Le.khet)'): 1,
    ('KIRALY-001_TORZSCIKK.md', '- **LXX:** Zsolt(LXX) 75:3 — — — kutatói azonosítás függőben'): 1,
    ('KIRALY-001_TUDOMANYOS.md', '| [2Móz 19:6](#ige-2móz-19-6) | papok — כֹּהֲנִ֖ים (ko.ha.Nim); מַמְלֶ֥כֶת (mam.Le.khet) | egyéni → kollektív szintre emelve | Remez | H3548+H4467 | BDB H3548 1 — egyszerre papok és királyok a nemzetekhez való viszonyukban | — *(ÓSZ)* | magas · tartalom-alapú[^2] |'): 1,
    ('KIRALY-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: KIRALY-001]` motívum 7 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 1,
    ('KIRALY-001_TUDOMANYOS.md', '- BDB (Brown–Driver–Briggs, A Hebrew and English Lexicon of the Old Testament, 1906) (`konkordancia/BDB_teljes_unabridged.tsv`, közkincs)'): 1,
    ('KIRALY-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 1,
    ('KIRALY-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 1,
    ('MENNY-001_TORZSCIKK.md', '- **LXX:** — — — — szamozas_elteres'): 1,
    ('MENNY-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: MENNY-001]` motívum 3 Strong-tokenjét fedi, nincs jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 1,
    ('MENNY-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 1,
    ('MENNY-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 1,
    ('TEREMT-001_TORZSCIKK.md', '- **Kulcsszó:** a mélységbe — תְּהֹמֹ֖ת (te.ho.Mot)'): 1,
    ('TEREMT-001_TORZSCIKK.md', '- **LXX:** — — — — szamozas_elteres'): 4,
    ('TEREMT-001_TUDOMANYOS.md', '| [2Móz 15:5](#ige-2móz-15-5) | a mélységbe — תְּהֹמֹ֖ת (te.ho.Mot) | — | Remez | H8415 | — | — *(ÓSZ)* | magas · tartalom-alapú[^5] |'): 1,
    ('TEREMT-001_TUDOMANYOS.md', '*Ez a blokk a `[ID: TEREMT-001]` motívum 2 Strong-tokenjét fedi, van jelentés-hivatkozással a `lexikon_hivatkozasok.tsv`-ből.*'): 1,
    ('TEREMT-001_TUDOMANYOS.md', '- `adat/forditas_ubs.tsv` (projekt-adat)'): 1,
    ('TEREMT-001_TUDOMANYOS.md', '| `forditas_ubs.tsv` | `adat/forditas_ubs.tsv` | projekt-adat | elofordulasok |'): 1,
    # felhasználó, 2026-10-18 (DT-F113b (2), #113): a szűkítés után a régi mátrixból sem igazolható 11 törölt sor -- a 3 `kézi (2/b)` lefedettségsor (ISTENTISZT-001) és a 8 jelmagyarázat-mondat
    ('ALVIL-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 1,
    ('ANTROP-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 1,
    ('HAMART-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 1,
    ('HODIT-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 1,
    ('ISTENTISZT-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 1,
    ('ISTENTISZT-001_TORZSCIKK.md', '| G1941 | TBESG | Thayer | nincs adatosítva | UBS DNTG (Louw–Nida) | UBS DNTG glossza + referencia-szám; Mounce kiegészítő | az ÚSZ-szó LXX-háttere: mely héber szavakat ad vissza, mely versekben (lekerdez.py lxx-hid, LXX_OS) | kézi (2/b) | LSJ, ha releváns | UBS DNTG (szópozícióig) | nincs adatosítva |'): 1,
    ('ISTENTISZT-001_TORZSCIKK.md', '| H7121 | TBESH | BDB | nincs adatosítva | UBS DBH (SDBH) | nincs adatosítva | LXX-fordítói döntés versenként: mely görög szó adja vissza (LXX_OS + adat/lxx_dontesek.tsv; a lexikonoldal 3. szakasza) | kézi (2/b) | nincs adatosítva | nincs adatosítva | nincs adatosítva |'): 1,
    ('ISTENTISZT-001_TORZSCIKK.md', '| H8034 | TBESH | BDB | nincs adatosítva | UBS DBH (SDBH) | nincs adatosítva | LXX-fordítói döntés versenként: mely görög szó adja vissza (LXX_OS + adat/lxx_dontesek.tsv; a lexikonoldal 3. szakasza) | kézi (2/b) | nincs adatosítva | nincs adatosítva | nincs adatosítva |'): 1,
    ('KIRALY-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 1,
    ('MENNY-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 1,
    ('TEREMT-001_TORZSCIKK.md', 'A cella értéke: forrás-hivatkozás (a szerep ma adatosítva), `kézi (2/b)` (a 2/b résben kézzel rögzítve), vagy `nincs adatosítva` (RENDER_BRIEF.md G7).'): 1,
}
# 2. ISMERT HIBA (N-F09g): a TSK-tábla KJV-számozású, a tsk_index() átváltás nélkül Károli-kulccsal keres; a Préd 9:10
#    alatti 12 TSK-jelölt a KJV 9:10 = Károli 9:12 vershez tartozott, és emiatt veszett el. CSAK ez a 13 sor (12 TSK-jelölt a tudományos oldalon + a törzscikk-oldal összevont sora):
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
    # #113 (5. hely): a zárójeles rész cseréje csak akkor kiejtés, ha a változás maga átírás (adatalapú próba,
    # `_kiejtes_kulonbseg`); ugyanaz a függvény, mint a cellánkénti ágon. Különben None: cellánkénti összevetés.
    if _kiejtes_kulonbseg(a, b):
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
            # törölt sablonmondat adatblokkban csak ellenőrzött csere (párosítás / valódi tartalom) után elszámolt
            return ISMERETLEN if irany == 'torolt' else 'elavult_adat'
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
    if irany == 'torolt' and ATKULCSOLT_KULCS.get(ATKULCSOLT_SOROK.get((motivum, s))):
        return 'elavult_adat'  # F87.3 átkulcsolás: a régi kulcs sora
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


_FEJ_SOR_RE = re.compile(r'^#{3,6} ')
_META_RE = re.compile(r'^- Generálva: \d{4}-\d{2}-\d{2}\s*$')
_CAND_RE = re.compile(r'^- (TSK|Károli-KH): (.+?)(?: \(Votes: \d+\))?$')
_ITEM_RE = re.compile(r'^- \*\*([^*]+):\*\*\s*(.*)$')
_LXXIGE_RE = re.compile(r'(?:[1-5]\s?)?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,9}(?:\(LXX\))?\.? \d{1,3}:\d{1,3}')
_STRONG_RE = re.compile(r'\b[HG]\d{4}\b')
_LINK_RE = re.compile(r'\[([^\]]*)\]\([^)]*\)')


def _fejek(sorok):
    """Soronként a legközelebbi megelőző (3–6 szintű) fejléc a generált blokkon / `##` szakaszon belül."""
    cur, out = '', []
    for s in sorok:
        if s.startswith('## ') or s.startswith('<!-- GENERÁLT-KEZDET'):
            cur = ''
        if _FEJ_SOR_RE.match(s):
            cur = s.strip()
        out.append(cur)
    return out


def _cellak(sor):
    return [c.strip() for c in re.split(r'(?<!\\)\|', sor.strip().strip('|'))]


def teljes_kulcs(sor, szakasz, fej):
    """DT-F09g (3. javító menet): a sor TELJES kulcsa a párosításhoz: forráscímke + igehely + célpont/Strong, a
    szakasz (blokk + alszakasz) mellett. Csak az igehely egyezése NEM elég. None, ha a sorhoz nincs kulcs."""
    s = sor.strip()
    m = _CAND_RE.match(s)
    if m:
        return ('jelolt', szakasz, m.group(1), fej, m.group(2).strip())
    if s.startswith('|'):
        c = _cellak(s)
        if not c or not c[0]:
            return None
        c0 = re.sub(r'\s+', ' ', _LINK_RE.sub(r'\1', c[0]).replace('`', '').replace('**', '')).strip()
        if not c0 or set(c0) <= set('-: '):
            return None
        return ('sor', szakasz, c0, frozenset(_STRONG_RE.findall(s)))
    m = _ITEM_RE.match(s)
    if m:
        return ('tetel', szakasz, m.group(1), fej, frozenset(_LXXIGE_RE.findall(m.group(2))),
                frozenset(_STRONG_RE.findall(s)))
    if _LEIRO_RE.match(s):
        return ('leiro', szakasz)
    if s.startswith('*Összesítés:'):
        return ('osszesites', szakasz)
    if s.startswith('A cella értéke:'):
        return ('jelmagyarazat', szakasz)
    return None


def _jeloles_kulonbseg(a, b):
    """Csak jelölés (kiemelés, táblaszegély, fejléc-jel, idézőjel) különbözik."""
    def tiszta(x):
        return re.sub(r'[\s*_#>|\\`]', '', x)
    return tiszta(a) == tiszta(b)


# #113 (5. hely): adatalapú átírás-próba. A zárójeles csere csak akkor kiejtés, ha mindkét oldal latin átírási
# karakterkészletű, ÉS az új oldal ugyanannak a szónak a mai kiejtése: görögül a `kiejtes.atir()` a régi (SBL-)
# átírásból, héberül az `adat/kiejtes_kivetelek.tsv` héber lemma-kiejtése a mező valamelyik héber szavára.
_ATIRAS_KESZLET_RE = re.compile(r"^[A-Za-zÀ-ɏḀ-ỿʾʿ.' \-]+$")
_STRONG_UTOTAG_RE = re.compile(r',?\s*[HG]\d{4}[a-z]?\s*$')
_HEBER_SZO_RE = re.compile('[֐-׿]+')
_kiejtes_cache = {}


def _kiejtes_adat():
    """(görög szabályok, görög kivételek, héber lemma-kiejtések) -- a kiejtes.py betöltőivel, egyszer."""
    if not _kiejtes_cache:
        import kiejtes as KJ
        _kiejtes_cache['k'] = (KJ, KJ.szabalyok_betolt(), KJ.kivetelek_betolt(), KJ.kivetelek_betolt(nyelv='heber'))
    return _kiejtes_cache['k']


def _atirasnak_tunik(x):
    """Latin átírási karakterkészlet (betű, ékezet, SBL-diakritika, pont, aposztróf, kötőjel, szóköz)."""
    return bool(x) and bool(_ATIRAS_KESZLET_RE.match(x))


def _atiras_par(x, y, mezo):
    """Egy eltérő zárójeles pár (x régi, y új) átírás-csere-e: a lemma / Strong-utótag azonos, csak az átírás
    (a vesszővel tagolt utolsó tag) változott, és az új átírás a régi mai kiejtése (adatalapú próba)."""
    sx, sy = _STRONG_UTOTAG_RE.search(x), _STRONG_UTOTAG_RE.search(y)
    if (sx.group(0).strip(' ,') if sx else '') != (sy.group(0).strip(' ,') if sy else ''):
        return False
    tx = x[:sx.start()] if sx else x
    ty = y[:sy.start()] if sy else y
    px, py = tx.rsplit(', ', 1), ty.rsplit(', ', 1)
    if len(px) != len(py) or (len(px) == 2 and px[0] != py[0]):
        return False
    regi, uj = px[-1].strip(), py[-1].strip()
    if regi == uj or not (_atirasnak_tunik(regi) and _atirasnak_tunik(uj)):
        return False
    KJ, szab, kiv, kiv_h = _kiejtes_adat()
    if KJ.atir(regi, szab, kiv) == uj:
        return True
    return any(kiv_h.get(unicodedata.normalize('NFC', w)) == uj for w in _HEBER_SZO_RE.findall(mezo))


def _kiejtes_kulonbseg(a, b):
    """Csak a zárójelezett latin betűs átírás / kiejtés különbözik, héber/görög írásjegyes mezőben: a zárójelen
    kívüli szöveg (pl. a magyar glossza) azonos, és minden eltérő zárójeles pár adatalapúan igazolt átírás-csere
    (#113, 5. hely: magyar szó cseréje -- `(pap)` -> `(király)` -- nem az)."""
    if not _SCRIPT_RE.search(a + b):
        return False
    kivul = lambda x: re.sub(r'\s+', ' ', re.sub(r'\([^()]*\)', '()', x)).strip()
    if kivul(a) != kivul(b):
        return False
    ga, gb = re.findall(r'\(([^()]*)\)', a), re.findall(r'\(([^()]*)\)', b)
    if ga == gb or len(ga) != len(gb):
        return False
    return all(_atiras_par(x, y, a) for x, y in zip(ga, gb) if x != y)


# DT-F09g (4. javító menet): cellánkénti összevetés. A sor kategóriája az eltérő mezők kategóriáiból adódik; a
# legkockázatosabb nyer (a sorrend: elöl a legkockázatosabb).
KOCKAZAT_SORREND = (ISMERETLEN, 'szerep', 'licenc', 'lxx_korpusz', 'elavult_adat', 'tbesh', 'ubs_dbh', 'mounce_sece',
                    'teologiai', 'nyelvi_hatter', 'ismert_hiba_tsk_versszam', 'felhasznalo_elfogadva', 'fordites_jelzo',
                    'kiejtes', 'jeloles', 'szerep_vaz', 'torzscikk_res', 'tanulmany')
_HELYORZO = ('', '—', '-', '–')
_LXX_ALLAPOT = ('egyező', 'eltérő', 'LXX-minusz', 'kutatói azonosítás függőben', 'szamozas_elteres')
_VOTES_RE = re.compile(r'\s*\(Votes: (\d+)\)\s*$')


def _legkockazatosabb(kats):
    return min(kats, key=lambda k: KOCKAZAT_SORREND.index(k) if k in KOCKAZAT_SORREND else 0)


def _mezok(fajta, sor):
    """A sor mezőkre bontása a kulcs fajtája szerint: táblasor: cellák; tétel: címke + ` — ` tagolt érték;
    jelölt: a szavazatszám; egyéb (leíró, összesítés, jelmagyarázat, sima sor): a teljes szöveg."""
    s = sor.strip()
    if fajta == 'sor':
        return _cellak(s)
    if fajta == 'tetel':
        m = _ITEM_RE.match(s)
        if m:
            return [m.group(1)] + [x.strip() for x in m.group(2).split(' — ')]
    if fajta == 'jelolt':
        m = _VOTES_RE.search(s)
        return [m.group(1) if m else '']
    return [s]


def _kanon(x):
    """Módszerjelző, fordítás-jelző és lábjegyzet normalizálása. Az LXX-állapotszavakat NEM olvasztja össze
    (#113, 4. hely): az állapotváltás iránya a `_lxx_allapot_kat`-ban dől el."""
    x = _FORDITAS_JELZO_RE.sub('(F)', x)
    x = _LABJEGYZET_RE.sub('', x)
    x = re.sub(r'tartalom-alapú|szó-szintű-gépi', 'MODSZER', x)
    return x.strip()


# #113 (4. hely, DT-F113a (b)): az LXX-állapot iránya. Csak a helyőrző / függő vagy számozási állapot -> előrébb
# lévő állapot fogadható el (pl. `kutatói azonosítás függőben` -> `eltérő`, `szamozas_elteres` -> `kutatói azonosítás
# függőben`); azonos fokú állapotok cseréje (`egyező` <-> `eltérő`), visszalépés és állapot -> helyőrző: `ismeretlen`.
_LXX_ALLAPOT_FOK = {'szamozas_elteres': 0, 'kutatói azonosítás függőben': 1, 'egyező': 2, 'eltérő': 2, 'LXX-minusz': 2}


def _lxx_allapot_elore(a, b):
    return a in _LXX_ALLAPOT_FOK and b in _LXX_ALLAPOT_FOK and _LXX_ALLAPOT_FOK[b] > _LXX_ALLAPOT_FOK[a]


# #113 (3. hely, DT-F113a (d)): csak a darabszám-, szavazatszám- és sorszám-jellegű szám frissülése elfogadott.
# A megváltozott számjegy-futam környezete (előtte / utána) egyike: `=N`, `Votes: N`, `(N)`, `N <főnév>`, a
# szerep-fejléc `#### N.` sorszáma, vagy önálló szám a mezőben. Igehely (`N:N`), jelentésszám (`2.c`, `BDB N`,
# `LSJ N`) és minden más számcsere nem ismert fajta.
_SZAM_ELO_OK_RE = re.compile(r'(?:=\s*|Votes:\s*)$')
_SZAM_FONEV_RE = re.compile(r'^ [a-záéíóöőúüű]')


def _darabszam_frissules(a, b):
    ta, tb = re.split(r'(\d+)', a), re.split(r'(\d+)', b)
    if len(ta) != len(tb):
        return False
    for k in range(1, len(ta), 2):
        if ta[k] == tb[k]:
            continue
        elo, uto = ta[k - 1], ta[k + 1]
        if elo.endswith(':') or uto.startswith(':') or re.match(r'^\.[a-z]', uto) \
                or re.search(r'(?:BDB|LSJ)\s*$', elo):
            return False                         # igehely / verzifikáció / jelentésszám
        if elo == '' and uto == '':
            continue                             # önálló szám a mezőben
        if _SZAM_ELO_OK_RE.search(elo) or (elo.endswith('(') and uto.startswith(')')):
            continue                             # `=N`, `Votes: N`, `(N)`
        if _SZAM_FONEV_RE.match(uto) and (elo == '' or elo[-1] in ' ('):
            continue                             # `N <főnév>` (darabszám)
        if re.match(r'^#{3,6} $', elo) and uto.startswith('. '):
            continue                             # a szerep-fejléc `#### N.` sorszáma
        return False
    return True


# #113 (2. hely, DT-F113a (c)): a licenc-blokkban csak licencszöveg / licencjelző cseréje, vagy bővült lista
# (az új listaérték a régi minden tételét tartalmazza) elszámolt. A licencértékek az `adat/licencek.tsv` `licenc`
# oszlopából (a teljes érték és a ` (`, ` — `, `;` előtti vezető része), a licencjelzők az alábbi mintából.
_LICENC_JELZO_RE = re.compile(r'^(?:projekt-adat|minden jog fenntartva|CC0(?: \d\.\d)?|CC BY(?:-SA|-NC|-ND)*(?: \d\.\d)?)$')
_licenc_cache = []


def _licenc_ertekek():
    if not _licenc_cache:
        ertekek = set()
        with io.open(os.path.join(ROOT, 'adat', 'licencek.tsv'), encoding='utf-8') as fh:
            sorok = [s for s in fh.read().split('\n') if s and not s.startswith('#')]
        fej = sorok[0].split('\t')
        i = fej.index('licenc')
        for s in sorok[1:]:
            m = s.split('\t')
            if len(m) > i and m[i].strip():
                v = m[i].strip()
                ertekek.add(v)
                ertekek.add(re.split(r' \(| — |;', v)[0].strip())
        _licenc_cache.append(ertekek)
    return _licenc_cache[0]


def _licencnek_tunik(x):
    x = x.strip()
    return bool(x) and (bool(_LICENC_JELZO_RE.match(x)) or x in _licenc_ertekek())


def _licenc_csere(a, b):
    if _licencnek_tunik(a) and _licencnek_tunik(b):
        return True
    kivul = lambda x: re.sub(r'\s+', ' ', re.sub(r'\([^()]*\)', '()', x)).strip()
    ga, gb = re.findall(r'\(([^()]*)\)', a), re.findall(r'\(([^()]*)\)', b)
    if kivul(a) == kivul(b) and len(ga) == len(gb) and ga != gb:
        return all(_licencnek_tunik(x) and _licencnek_tunik(y) for x, y in zip(ga, gb) if x != y)
    return False


def _bovult_lista(a, b):
    ra = [t.strip() for t in a.split(',') if t.strip()]
    rb = [t.strip() for t in b.split(',') if t.strip()]
    return len(rb) > len(ra) and all(t in rb for t in ra)


# #113 (1. hely, DT-F113a (a), DT-F113b (1)): az éles lexikon/ 8 törzscikkét renderelő szerepmátrix
# (`git show d9b80b37:adat/szotar_szerepek.tsv`, blob bce21db8) egyszeri, rögzített kivonata, unió nélkül:
# (nyelv, sorrend) -> (szerep, forrás, állapot). A kód futás közben NEM olvassa a git-történetet.
REGI_SZEREPMATRIX_D9B80B37 = {
    ('gorog', 1): ('Alapjelentés', 'TBESG', 'adatosítva'),
    ('gorog', 2): ('Mélységi szócikk', 'Thayer', 'adatosítva'),
    ('gorog', 3): ('Teológiai szócikk', 'Cremer (1895)', 'nincs adatosítva'),
    ('gorog', 4): ('Jelentésszerkezet, szemantikai mező', 'UBS DNTG (Louw–Nida)', 'adatosítva'),
    ('gorog', 5): ('Tömör jelentés, előfordulás', 'UBS DNTG glossza + referencia-szám; Mounce kiegészítő', 'adatosítva'),
    ('gorog', 6): ('LXX-híd', 'az ÚSZ-szó LXX-háttere: mely héber szavakat ad vissza, mely versekben (lekerdez.py lxx-hid, LXX_OS)', 'adatosítva'),
    ('gorog', 7): ('Megfelelők a másik nyelven', 'SECE (héber)', 'nincs adatosítva'),
    ('gorog', 8): ('Nyelvi háttér', 'LSJ, ha releváns', 'adatosítva'),
    ('gorog', 9): ('Versenkénti jelentés', 'UBS DNTG (szópozícióig)', 'adatosítva'),
    ('gorog', 10): ('Kiejtés (magyaros)', 'kiejtes.py szabálytábla', 'nincs adatosítva'),
    ('heber', 1): ('Alapjelentés', 'TBESH', 'adatosítva'),
    ('heber', 2): ('Mélységi szócikk', 'BDB', 'adatosítva'),
    ('heber', 3): ('Teológiai szócikk', 'Girdlestone (1897) + Cremer héber mutatója; TWOT-szám hivatkozásként', 'nincs adatosítva'),
    ('heber', 4): ('Jelentésszerkezet, szemantikai mező', 'UBS DBH (SDBH)', 'adatosítva'),
    ('heber', 5): ('Tömör jelentés, előfordulás', 'UBS DBH glossza + referencia-szám', 'nincs adatosítva'),
    ('heber', 6): ('LXX-híd', 'LXX-fordítói döntés versenként: mely görög szó adja vissza (LXX_OS + adat/lxx_dontesek.tsv; a lexikonoldal 3. szakasza)', 'adatosítva'),
    ('heber', 7): ('Megfelelők a másik nyelven', 'SECE (görög)', 'nincs adatosítva'),
    ('heber', 8): ('Nyelvi háttér', 'BDB etimológia', 'nincs adatosítva'),
    ('heber', 9): ('Versenkénti jelentés', 'UBS DBH', 'nincs adatosítva'),
    ('heber', 10): ('Kiejtés (magyaros)', 'lemma: kiejtes_kivetelek.tsv (kézi, OSHL-alapú jelöltekből); alak: STEP-átírás, változatlanul', 'nincs adatosítva'),
}
_TOKEN_RE = re.compile(r'^[HG]\d{4}[a-z]?$')
_matrix_cache = []


def _mai_matrix():
    """[(nyelv, sorrend, szerep, forrás, állapot)] -- a mai `adat/szotar_szerepek.tsv` (split('\\t'))."""
    if not _matrix_cache:
        out = []
        with io.open(os.path.join(ROOT, 'adat', 'szotar_szerepek.tsv'), encoding='utf-8') as fh:
            for s in fh.read().split('\n'):
                if not s or s.startswith('#') or s.startswith('nyelv\t'):
                    continue
                m = s.split('\t')
                out.append((m[0], int(m[1]), m[2], m[3], m[4]))
        _matrix_cache.append(out)
    return _matrix_cache[0]


def _olvaso_forras(x):
    import torzscikk_general as TG
    return TG.olvaso_forras(x)


def _szerep_csere(a, b, sor_kulcs, oszlop):
    """Az `5. Szótári` szakasz egy cellájának cseréje szerep-változás-e (DT-F113a (a)):
      szerep-táblasor (`| <szerep> | <görög forrás> | <héber forrás> |`): az új érték a cella szerepének MAI
        forrása vagy annak renderelt alakja (`olvaso_forras`), a régi érték ugyanennek a szerepnek a forrása a régi
        mátrixban (`REGI_SZEREPMATRIX_D9B80B37`) vagy a maiban;
      lefedettség-sor (`| <token> | ... |`, az oszlopok a mai görög szerepsorrendben): az új érték a renderfüggvény
        (`szerep_lefedettseg_cella`) értéke a cellára, a régi a szerep régi forrása vagy állapota.
    Minden más csere: nem szerep-változás (`ismeretlen`). Ez zárja ki pl. a `UBS DNTG` -> `Mounce` cserét egy
    olyan cellában, amelynek szerepéhez a mátrix nem a Mounce-ot rendeli."""
    cella = _szerep_cella(sor_kulcs, oszlop)
    if cella is None:
        return False
    vart, regi_ok = cella
    return b == vart and a in regi_ok


def _szerep_cella(sor_kulcs, oszlop):
    """Az `5. Szótári` szakasz azonosított cellájának (várt mai érték, elfogadható régi értékek) párja, vagy None,
    ha a cella nem azonosítható (nem szerep-tábla- vagy lefedettség-sor, ismeretlen szerep)."""
    if sor_kulcs is None or oszlop is None or oszlop < 1:
        return None
    mai = _mai_matrix()
    gorog = sorted((r for r in mai if r[0] == 'gorog'), key=lambda r: r[1])
    if _TOKEN_RE.match(sor_kulcs):
        if oszlop > len(gorog):
            return None
        nyelv = 'gorog' if sor_kulcs.startswith('G') else 'heber'
        szerep = gorog[oszlop - 1][2]
    elif oszlop in (1, 2):
        nyelv, szerep = ('gorog', 'heber')[oszlop - 1], sor_kulcs
    else:
        return None
    sor = next((r for r in mai if r[0] == nyelv and r[2] == szerep), None)
    if sor is None:
        return None
    regi = next((v for (ny, _n), v in REGI_SZEREPMATRIX_D9B80B37.items() if ny == nyelv and v[0] == szerep), None)
    if _TOKEN_RE.match(sor_kulcs):
        vart = _olvaso_forras(LG.szerep_lefedettseg_cella(
            nyelv, {'sorrend': str(sor[1]), 'szerep': sor[2], 'forras': sor[3], 'allapot': sor[4]}, sor_kulcs))
        regi_ok = {regi[1], regi[2]} if regi else set()
    else:
        vart = _olvaso_forras(sor[3])
        regi_ok = ({regi[1]} if regi else set()) | {sor[3], vart}
    return vart, regi_ok


_SZEREP_ALLAPOTJELZOK = ('nincs adatosítva', 'nincs forrás', 'a forrás nem tárgyalja')


def _szerep_uj_igazolt(b, sor_kulcs, oszlop):
    """#113 1. hely (ellenőri 1. eltérés): helyőrző / `nincs adatosítva` régi oldal után az új oldal csak akkor
    szerep, ha az azonosított cellában a várt mai érték (a szerep mai forrása / renderelt alakja, lefedettség-sorban
    a `szerep_lefedettseg_cella` értéke), vagy állapotjelző (a mai mátrix `allapot` értékei és a fenti jelzők)."""
    cella = _szerep_cella(sor_kulcs, oszlop)
    if cella is None:
        return False
    return b == cella[0] or b in _SZEREP_ALLAPOTJELZOK or b in set(r[4] for r in _mai_matrix())


def _mezo_kat(a, b, alap, szakasz, sor_kulcs=None, oszlop=None):
    """Egy eltérő mezőpár kategóriája az ismert változásfajták alapján; tartalom eltűnése vagy ismeretlen fajta:
    `ismeretlen`. `alap`: az új sor blokk szerinti kategóriája (maga is lehet `ismeretlen`); a kategória NEVÉT
    adhatja, az elfogadást nem (#113): minden elfogadó ág a régi -> új érték viszonyán múlik.
    `sor_kulcs`, `oszlop`: táblasornál az első cella és a mező sorszáma (a szerep-cella azonosításához)."""
    a, b = a.strip(), b.strip()
    if a not in _HELYORZO and b in _HELYORZO:
        return ISMERETLEN                       # a mező tartalma eltűnt (állapot -> helyőrző is, #113 4. hely)
    if a in _HELYORZO or a == 'nincs adatosítva':
        if szakasz.startswith('5. Szótári'):    # #113 1. hely: az új oldal is igazolandó (ellenőri 1. eltérés)
            return 'szerep' if _szerep_uj_igazolt(b, sor_kulcs, oszlop) else ISMERETLEN
        return alap                             # helyőrző / `nincs adatosítva` -> tartalom vagy állapot
    if a in _LXX_ALLAPOT or b in _LXX_ALLAPOT:
        return alap if _lxx_allapot_elore(a, b) else ISMERETLEN   # #113 4. hely: csak előre lépő állapot
    if _kiejtes_kulonbseg(a, b):
        return 'kiejtes'                        # átírás / kiejtés (adatalapú próba, #113 5. hely)
    if _jeloles_kulonbseg(a, b):
        return 'jeloles'
    ca, cb = _kanon(a), _kanon(b)
    if ca == cb:                                # módszerjelző, fordítás-jelző, lábjegyzet
        return 'fordites_jelzo' if (_FORDITAS_JELZO_RE.search(a) or _FORDITAS_JELZO_RE.search(b)) else alap
    if re.sub(r'\d+', '#', a) == re.sub(r'\d+', '#', b):
        return alap if _darabszam_frissules(a, b) else ISMERETLEN  # #113 3. hely: csak darab-/szavazat-/sorszám
    if alap == 'licenc':
        # #113 2. hely: licencszöveg / -jelző cseréje vagy bővült lista; más csere a licenc-blokkban sem ismert
        return 'licenc' if (_licenc_csere(a, b) or _bovult_lista(a, b)) else ISMERETLEN
    azon = r'^[A-Za-z0-9_./\-]*[._/][A-Za-z0-9_./\-]*$'   # fájlnév / forrás-azonosító (. _ vagy / van benne)
    if re.match(azon, a) and re.match(azon, b):
        return alap                             # fájlnév / forrás-azonosító cseréje (N-F113a: a #113-on kívül)
    if szakasz.startswith('5. Szótári'):
        # #113 1. hely: csak a szerepmátrix szerinti forrás- / állapotváltás (cellára azonosítva)
        return 'szerep' if _szerep_csere(a, b, sor_kulcs, oszlop) else ISMERETLEN
    return ISMERETLEN


def par_mezo_kategoria(regi, uj, fajta, alap, szakasz):
    """Pár esetén a régi és az új sor mezőnkénti összevetése; az eltérő mezők kategóriáiból a legkockázatosabb."""
    fa, fb = _mezok(fajta, regi), _mezok(fajta, uj)
    if len(fb) < len(fa):
        return ISMERETLEN                       # mező(k) eltűntek
    sor_kulcs = fa[0].strip() if fajta == 'sor' and fa else None
    kats = [_mezo_kat(x, y, alap, szakasz, sor_kulcs, i if fajta == 'sor' else None)
            for i, (x, y) in enumerate(zip(fa, fb)) if x.strip() != y.strip()]
    if len(fb) > len(fa):
        kats.append(alap)                       # új (hozzáfűzött) mezők: nem veszteség
    if not kats:
        return 'jeloles'
    return _legkockazatosabb(kats)


def _akcio_sect(torzscikk, k):
    return k if torzscikk else (k[0] or '')


def proba_osztalyoz(fajl_nev, eles_szoveg, proba_szoveg, parok=None):
    """{kategória: {'hozzaadott': [sor], 'torolt': [sor]}} a multihalmaz-különbségre.

    Sorrend (DT-F09g, 3. javító menet): (0) megnevezett táblák és metaadat; (1) kizárólagos párosítás azonos
    szakaszban a normalizált kulccsal (kiejtés / jelző / fejléc-mélység); (2) kizárólagos párosítás a TELJES kulccsal
    (`teljes_kulcs`); (3) üres-állapot mondat ellenőrzött cseréje valódi tartalomra; (4) a többi sor a blokkja szerint,
    a törölt sor a `tovabb_el` próbával; ami így sem fér sehova: `ismeretlen` (tartalék nincs)."""
    eles = eles_szoveg.replace('\r\n', '\n').split('\n')
    proba = proba_szoveg.replace('\r\n', '\n').split('\n')
    ce, cp = collections.Counter(eles), collections.Counter(proba)
    torzscikk = fajl_nev.endswith('_TORZSCIKK.md')
    motivum = fajl_nev.split('_')[0]
    if torzscikk:
        ke, kp = _torzscikk_kontextusok(eles), _torzscikk_kontextusok(proba)
    else:
        ke, kp = _tudomanyos_kontextusok(eles), _tudomanyos_kontextusok(proba)
    fe, fp = _fejek(eles), _fejek(proba)

    def feleslegek(sorok, kont, fej, sajat, masik):
        latott, ki = collections.Counter(), []
        for s, k, f in zip(sorok, kont, fej):
            if not s.strip():
                continue
            latott[s] += 1
            if latott[s] <= sajat[s] - masik[s]:
                ki.append((s, k, f))
        return ki

    torolt = feleslegek(eles, ke, fe, ce, cp)
    hozzaadott = feleslegek(proba, kp, fp, cp, ce)
    proba_sz = ProbaSzoveg(proba)
    eredmeny = collections.defaultdict(lambda: {'hozzaadott': [], 'torolt': []})
    kat_t, kat_h = {}, {}          # index -> kategória
    hasznalt_h = set()

    def sajat_kat(s, k, irany, tovabb=True):
        """A sor besorolása a blokkja / szakasza szerint (a megnevezett táblák és a túlélés-próba nélkül is)."""
        if torzscikk:
            return _torzscikk_kategoria(s, k, irany, proba_sz if tovabb else None, motivum)
        return _tudomanyos_kategoria(s, k, irany, proba_sz if tovabb else None, motivum)

    # (0) metaadat
    for idx, (s, k, f) in enumerate(torolt):
        if _META_RE.match(s.strip()) or s.strip().startswith('<!-- GENERÁLT'):
            kat_t[idx] = 'jeloles'
    for idx, (s, k, f) in enumerate(hozzaadott):
        if _META_RE.match(s.strip()) or s.strip().startswith('<!-- GENERÁLT'):
            kat_h[idx] = 'jeloles'
    # (0) a felhasználó által név szerint elfogadott sorok (csak törölt irány)
    elfogadva_db = collections.Counter()
    for idx, (s, k, f) in enumerate(torolt):
        kulcs_ = (fajl_nev, s.strip())
        if idx not in kat_t and kulcs_ in FELHASZNALO_ELFOGADOTT and elfogadva_db[kulcs_] < FELHASZNALO_DARAB[kulcs_]:
            elfogadva_db[kulcs_] += 1
            kat_t[idx] = 'felhasznalo_elfogadva'   # a darabszámon felüli azonos sor nem elfogadott
    # (0) megnevezett táblák (F87.3-lábnyom, ismert TSK-hiba): nem párosítjuk
    nevesitett = set()
    for idx, (s, k, f) in enumerate(torolt):
        if idx in kat_t:
            continue
        if (motivum, s.strip()) in ISMERT_HIBA_TSK_VERSSZAM or (motivum, s.strip()) in ATKULCSOLT_SOROK:
            nevesitett.add(idx)

    # (1) kizárólagos párosítás a normalizált kulccsal, azonos szakaszban
    hmap = collections.defaultdict(list)
    for j, (s, k, f) in enumerate(hozzaadott):
        if j not in kat_h:
            hmap[(_akcio_sect(torzscikk, k), _kulcs(s))].append(j)
    for idx, (s, k, f) in enumerate(torolt):
        if idx in kat_t or idx in nevesitett:
            continue
        lst = [j for j in hmap.get((_akcio_sect(torzscikk, k), _kulcs(s)), []) if j not in hasznalt_h]
        if not lst:
            continue
        j = lst[0]
        hasznalt_h.add(j)
        pk = _par_kategoria(s, hozzaadott[j][0])
        if pk is None:   # a szerkezeti / jelző / kiejtés-feltétel nem illik: cellánkénti összevetés (4. javító menet)
            kk0 = teljes_kulcs(s, _akcio_sect(torzscikk, k), f)
            alap = sajat_kat(hozzaadott[j][0], hozzaadott[j][1], 'hozzaadott', tovabb=False)
            kat_t[idx] = kat_h[j] = par_mezo_kategoria(s, hozzaadott[j][0], kk0[0] if kk0 else None, alap,
                                                       _akcio_sect(torzscikk, k))
        else:
            kat_t[idx] = kat_h[j] = pk
        if parok is not None:
            parok.append(('normalizált kulcs', s, hozzaadott[j][0], _kulcs(s), kat_t[idx]))

    # (2) kizárólagos párosítás a TELJES kulccsal
    hk = collections.defaultdict(list)
    for j, (s, k, f) in enumerate(hozzaadott):
        if j in hasznalt_h or j in kat_h:
            continue
        kk = teljes_kulcs(s, _akcio_sect(torzscikk, k), f)
        if kk is not None:
            hk[kk].append(j)
    for idx, (s, k, f) in enumerate(torolt):
        if idx in kat_t or idx in nevesitett:
            continue
        kk = teljes_kulcs(s, _akcio_sect(torzscikk, k), f)
        if kk is None:
            continue
        lst = [j for j in hk.get(kk, []) if j not in hasznalt_h]
        if not lst:
            continue
        j = lst[0]
        hasznalt_h.add(j)
        uj_sor, uj_k = hozzaadott[j][0], hozzaadott[j][1]
        alap = sajat_kat(uj_sor, uj_k, 'hozzaadott', tovabb=False)
        kat = par_mezo_kategoria(s, uj_sor, kk[0], alap, _akcio_sect(torzscikk, k))
        kat_t[idx] = kat_h[j] = kat
        if parok is not None:
            parok.append(('teljes kulcs', s, uj_sor, kk, kat))

    # (3) üres-állapot mondat ellenőrzött cseréje: ugyanabban a szakaszban (blokk + alszakasz) valódi tartalom áll
    for idx, (s, k, f) in enumerate(torolt):
        if idx in kat_t or idx in nevesitett or not _URES_ALLAPOT_RE.match(s.strip()):
            continue
        if not torzscikk and k[0] == 'szocikkek':
            continue   # a szocikkek váz-sorait a blokk-szabály kezeli
        for j, (hs, hk_, hf) in enumerate(hozzaadott):
            if hf != f or _akcio_sect(torzscikk, hk_) != _akcio_sect(torzscikk, k):
                continue
            if _URES_ALLAPOT_RE.match(hs.strip()) or _LEIRO_RE.match(hs.strip()) or _FEJ_SOR_RE.match(hs):
                continue
            kat_t[idx] = sajat_kat(hs, hk_, 'hozzaadott', tovabb=False)
            break

    # (4) a többi: saját besorolás (a törölt sorra túlélés-próbával); a megnevezett táblák a saját kategóriájukba
    for idx, (s, k, f) in enumerate(torolt):
        if idx in kat_t:
            continue
        if torzscikk:
            kat_t[idx] = _torzscikk_kategoria(s, k, 'torolt', proba_sz, motivum)
        else:
            kat_t[idx] = _tudomanyos_kategoria(s, k, 'torolt', proba_sz, motivum)
    for j, (s, k, f) in enumerate(hozzaadott):
        if j in kat_h:
            continue
        if s.strip().startswith('<!-- GENERÁLT'):
            kat_h[j] = 'jeloles'
        else:
            kat_h[j] = sajat_kat(s, k, 'hozzaadott', tovabb=False)
    for idx, (s, k, f) in enumerate(torolt):
        kat = kat_t[idx]
        if s.strip().startswith('<!-- GENERÁLT') and kat == ISMERETLEN:
            kat = 'jeloles'
        eredmeny[kat]['torolt'].append(s)
    for j, (s, k, f) in enumerate(hozzaadott):
        eredmeny[kat_h[j]]['hozzaadott'].append(s)
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
    ismeretlen_sorok = ['\t'.join(['fajl', 'irany', 'sor', 'felhasznaloi_besorolas', 'uj_sor_a_parbol'])]
    elfogadott_db = collections.Counter()
    for f in fajlok:
        with io.open(os.path.join(a.eles, f), encoding='utf-8', newline='') as fh:
            eles = fh.read()
        with io.open(os.path.join(proba_lex, f), encoding='utf-8', newline='') as fh:
            proba = fh.read()
        parok = []
        eredmeny = proba_osztalyoz(f, eles, proba, parok)
        par_uj = {}
        for _mod, regi_, uj_, _kk, _kat in parok:
            par_uj.setdefault(regi_.strip(), uj_.strip())
        for kat in sorted(eredmeny):
            h, t = len(eredmeny[kat]['hozzaadott']), len(eredmeny[kat]['torolt'])
            sorok.append('\t'.join([f, kat, str(h), str(t)]))
            osszes[kat] += h + t
            if kat not in PROBA_KATEGORIAK:
                ismeretlen = True
                print('ISMERETLEN KATEGÓRIA: %s %s (%d sor)' % (f, kat, h + t), file=sys.stderr)
                for irany in ('hozzaadott', 'torolt'):
                    for s in eredmeny[kat][irany]:
                        ismeretlen_sorok.append('\t'.join([f, irany, s.strip(), '', par_uj.get(s.strip(), '') if irany == 'torolt' else '']))
            elif kat == 'felhasznalo_elfogadva':
                for s in eredmeny[kat]['torolt']:
                    g = FELHASZNALO_ELFOGADOTT[(f, s.strip())]
                    elfogadott_db[g] += 1
                    ismeretlen_sorok.append('\t'.join([f, 'torolt', s.strip(), g, '']))
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
    if ismeretlen or elfogadott_db:
        ism_ut = os.path.splitext(a.tsv)[0].replace('_diff', '') + '_ismeretlen.tsv'
        ismeretlen_sorok.append('# felhasznaloi_besorolas: a felhasználó (chat) által név szerint elfogadott sorok (FELHASZNALO_ELFOGADOTT; 2026-10-17: 32 sor, 2026-10-18: 12 sor, DT-F113b: 11 sor); az üres besorolású sor `ismeretlen`, a felhasználó elé kerül. Elfogadott csoportok: %s' % ', '.join('%s=%d' % kv for kv in sorted(elfogadott_db.items())))
        ismeretlen_sorok.append('# proveniencia: scope=%s vs %s | forras=eszkozok/render_diff_osztalyoz.py --proba | ts=%s' % (os.path.relpath(a.proba, ROOT).replace(os.sep, '/'), os.path.relpath(a.eles, ROOT).replace(os.sep, '/'), os.environ.get('PARDES_DATUM', '')))
        with io.open(ism_ut, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(ismeretlen_sorok) + '\n')
        print('ismeretlen / elfogadott sorok: %s' % os.path.relpath(ism_ut, ROOT).replace(os.sep, '/'), file=sys.stderr)
    print('\n'.join(sorok))
    if valtozott:
        print('ÁLLJ: az éles lexikon/ fájlja változott: %s' % ', '.join(valtozott), file=sys.stderr)
        return 2
    return 2 if ismeretlen else 0


if __name__ == '__main__':
    if '--proba' in sys.argv:
        sys.exit(proba_main(sys.argv[1:]))
    sys.exit(main())
