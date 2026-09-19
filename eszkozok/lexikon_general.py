#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lexikon_general.py — F6_BRIEF.md F6.4: a `lexikon/[ID]_TUDOMANYOS.md`
generátora.

A render-logika külön modulban (D13): a `general.py` a betöltést és a
CLI-t adja, ez a modul a hét generált blokk tartalmát építi fel az
`adat/` táblákból és a `konkordancia/` kivonatokból, a `lekerdez.py`
betöltőin keresztül (import, nem másolás).

Vegyes fájl (D1): a hét blokk `general.py --cel lexikon` alatt frissül;
a blokkokon kívüli (kézi) szakaszokat a `blokk_beilleszt` érintetlenül
hagyja. Új célfájlnál a teljes váz (fejléc + mind a 15 szakasz) íródik.

TSV-olvasás kizárólag split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import general as G
import lekerdez as L

ROOT = G.ROOT
ADAT = G.ADAT
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')

LEXIKON_HIVATKOZASOK_TSV = os.path.join(ADAT, 'lexikon_hivatkozasok.tsv')
OSHL_TSV = os.path.join(KONKORDANCIA, 'OSHL_lexikalis_index.tsv')
KAPCSOLATOK_TSV = os.path.join(ADAT, 'kapcsolatok.tsv')

STRONG_TOKEN_RE = re.compile(r'^[HG]\d{4}[A-Za-z]?$')
EM_DASH = '—'

# --- Licencek, §1.3 -------------------------------------------------------

LICENC = {
    'BDB': 'közkincs',
    'Karoli_KH': 'közkincs',
    'TBESH': 'CC BY 4.0',
    'TBESG': 'CC BY 4.0',
    'TSK': 'CC BY 4.0',
    'OSHL': 'CC BY 4.0',
    'SDBH': 'CC BY-SA 4.0',
    'SDGNT': 'CC BY-SA 4.0',
    'LXX': 'tisztazatlan',
    'Thayer': 'tisztazatlan',
    'LSJ': 'tisztazatlan',
    'SECE_G': 'tisztazatlan',
    'SECE_H': 'tisztazatlan',
    'MCGED': 'tisztazatlan',
    'projekt-adat': 'projekt-adat',
}

TISZTAZATLAN_SZOTARAK = {'Thayer', 'LSJ', 'SECE_G', 'SECE_H', 'MCGED'}


def _sorted_unique(seq):
    return sorted(set(seq))


# ---------------------------------------------------------------------------
# Segéd: motívum Strong-tokenjei
# ---------------------------------------------------------------------------

def motivum_strong_tokenek(sorai):
    """A motívum összes Strong-tokenje (a `strong` mező `+` mentén bontva,
    a ^[HG]\\d{4}[A-Za-z]?$ mintára illeszkedők), rendezve."""
    tokenek = set()
    for sor in sorai:
        for darab in (sor.get('strong') or '').split('+'):
            darab = darab.strip()
            if STRONG_TOKEN_RE.match(darab):
                tokenek.add(darab)
    return sorted(tokenek)


# ---------------------------------------------------------------------------
# 0. metaadat
# ---------------------------------------------------------------------------

def blokk_metaadat(m):
    forras_study_sorok = [s.strip() for s in (m.get('forras_study') or '').split(';') if s.strip()]
    forras_study_cella = '<br>'.join('`%s`' % s for s in forras_study_sorok) if forras_study_sorok else EM_DASH

    naplo_fajlnev = G.ID_NAPLO_TERKEP.get(m['id'])
    naplo_cella = (
        '`tematikus_lezart/naplok/%s`' % naplo_fajlnev if naplo_fajlnev else EM_DASH
    )

    statusz_cella = '%s (`%s`, %s)' % (m['statusz'], m.get('statusz_verzio', ''), m.get('statusz_datum', ''))

    sorok = [
        '| Mező | Érték |',
        '|---|---|',
        '| ID | `%s` |' % m['id'],
        '| Rövid UI-címke | %s |' % m.get('ui_cimke', EM_DASH),
        '| Teljes cím | %s |' % m.get('cim', EM_DASH),
        '| Téma | %s |' % m.get('tema', EM_DASH),
        '| PaRDeS-szint | %s |' % m.get('pardes_szint', EM_DASH),
        '| Státusz | %s |' % statusz_cella,
        '| Azonosság típusa | %s |' % m.get('azonossag_tipusa', EM_DASH),
        '| Negatív kritérium | %s |' % m.get('negativ_kriterium', EM_DASH),
        '| Fölérendelt fogalom | %s |' % m.get('folerendelt_fogalom', EM_DASH),
        '| Forrás-study | %s |' % forras_study_cella,
        '| Kereszthivatkozás-napló | %s |' % naplo_cella,
        '| Sablon-megfelelőség | %s |' % m.get('sablon_verzio', EM_DASH),
    ]
    hatokor = 'Ez a blokk a `[ID: %s]` motívum törzsadatait fedi a `motivumok.tsv`-ből.' % m['id']
    torzs = '\n'.join(sorok)
    blokk_szoveg = _lexikon_blokk(m['id'], 'metaadat', ['adat/motivumok.tsv'], ['projekt-adat'],
                                   hatokor, torzs)
    return blokk_szoveg, [('adat/motivumok.tsv', 'projekt-adat')]


# ---------------------------------------------------------------------------
# 1. elofordulasok
# ---------------------------------------------------------------------------

def lexikon_jelentes_cella(sor):
    szotar = sor.get('lexikon_szotar') or ''
    entry_id = sor.get('lexikon_entry_id') or ''
    if not szotar:
        return EM_DASH
    jsz = sor.get('jelentes_szam') or ''
    cella = ('%s %s %s' % (szotar, entry_id, jsz)).strip()
    jelentes_hu = sor.get('jelentes_hu') or ''
    if jelentes_hu:
        cella += ' — %s' % jelentes_hu
    return cella


def blokk_elofordulasok(m, sorai, konyv_sorrend, hianyzo_konyvek):
    sorai_rendezve = sorted(
        sorai, key=lambda s: G.igehely_rendezo_kulcs(s['igehely'], konyv_sorrend, hianyzo_konyvek))
    lexikon_jelentessel = sum(1 for s in sorai_rendezve if s.get('lexikon_szotar'))

    fejlec = ['| Igehely | Kapcsolódás | PaRDeS-szint | Funkció | Strong-szám(ok) | Lexikon-jelentés |',
              '|---|---|---|---|---|---|']
    sorok = list(fejlec)
    for s in sorai_rendezve:
        sorok.append('| %s | %s | %s | %s | %s | %s |' % (
            s['igehely'], s.get('kapcsolodas') or EM_DASH, s.get('pardes_szint') or EM_DASH,
            s.get('funkcio') or EM_DASH, s.get('strong') or EM_DASH,
            lexikon_jelentes_cella(s)))

    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d igehely-sorát fedi az `elofordulasok.tsv`-ből, '
               'kanonikus sorrendben, ebből %d lexikon-jelentéssel.'
               % (m['id'], len(sorai_rendezve), lexikon_jelentessel))
    torzs = '\n'.join(sorok)
    blokk_szoveg = _lexikon_blokk(m['id'], 'elofordulasok', ['adat/elofordulasok.tsv'], ['projekt-adat'],
                                   hatokor, torzs)
    return blokk_szoveg, [('adat/elofordulasok.tsv', 'projekt-adat')]


# ---------------------------------------------------------------------------
# 2. szocikkek
# ---------------------------------------------------------------------------

_oshl_cache = None


def oshl_sorok():
    global _oshl_cache
    if _oshl_cache is None:
        _oshl_cache = L.read_tsv_skip_comments(OSHL_TSV)
    return _oshl_cache


def oshl_twot_ehhez(strong):
    twotok = _sorted_unique(
        r['twot'] for r in oshl_sorok() if r['strong'] == strong and r['twot'] != EM_DASH
    )
    return twotok


_lexikon_hivatkozasok_cache = None


def lexikon_hivatkozasok_sorok():
    global _lexikon_hivatkozasok_cache
    if _lexikon_hivatkozasok_cache is None:
        _lexikon_hivatkozasok_cache = L.read_tsv_skip_comments(LEXIKON_HIVATKOZASOK_TSV)
    return _lexikon_hivatkozasok_cache


def lexikon_hivatkozasok_ehhez(strong):
    sorok = [r for r in lexikon_hivatkozasok_sorok() if r['strong'] == strong]
    return sorted(sorok, key=lambda r: (r['szotar'], r['jelentes_szam']))


def domen_talalatok(strong):
    """[(domen_kod, domen)] ehhez a Stronghoz, a lekerdez.py domen parancsával
    azonos illesztéssel (K13: a darabszám egyezik a `domen <strong>` n
    értékével)."""
    if strong.startswith('H'):
        rows = L.load_sdbh_domenek()
    else:
        rows = L.load_sdgnt_domenek()
    hits = [r for r in rows if r['strong'] == strong]
    domenkodok = _sorted_unique(r['domen_kod'] for r in hits if r['domen_kod'] != EM_DASH)
    talalatok = []
    for kod in domenkodok:
        label = next(r['domen'] for r in hits if r['domen_kod'] == kod)
        talalatok.append((kod, label))
    return talalatok


def domen_anomalia_figyelmeztetes(strong):
    dataset_name = 'SDBH' if strong.startswith('H') else 'SDGNT'
    anom_rows = L.load_sdbh_sdgnt_anomaliak()
    matches = L._matching_jelentes_nelkul(anom_rows, dataset_name, strong)
    return matches


def blokk_szocikkek(m, tokenek):
    reszek = []
    # fajl -> licenc-kulcsok halmaza -- FÁJLONKÉNTI granularitás (a 9. szakasz
    # táblájának ne legyen minden Strong-token licence-e ráragasztva minden
    # fájlra, csak a ténylegesen hozzá tartozó).
    fajl_licenc_kulcsok = {'adat/lexikon_hivatkozasok.tsv': set()}
    van_hivatkozas_barmelyikhez = False
    tisztazatlan_erintve = False

    for strong in tokenek:
        alszakasz = ['### %s' % strong]

        if strong.startswith('H'):
            twotok = oshl_twot_ehhez(strong)
            alszakasz.append('**TWOT:** %s' % (', '.join(twotok) if twotok else EM_DASH))
            fajl_licenc_kulcsok.setdefault('konkordancia/OSHL_lexikalis_index.tsv', set()).add('OSHL')
        else:
            alszakasz.append('**TWOT:** %s' % EM_DASH)

        domenek = domen_talalatok(strong)
        if domenek:
            domen_szoveg = ', '.join('%s %s' % (kod, label) for kod, label in domenek)
        else:
            domen_szoveg = EM_DASH
        alszakasz.append('**Szemantikai domén:** %s' % domen_szoveg)
        domen_fajl = 'konkordancia/SDBH_domenek.tsv' if strong.startswith('H') else 'konkordancia/SDGNT_domenek.tsv'
        domen_licenc_kulcs = 'SDBH' if strong.startswith('H') else 'SDGNT'
        fajl_licenc_kulcsok.setdefault(domen_fajl, set()).add(domen_licenc_kulcs)

        for anom in domen_anomalia_figyelmeztetes(strong):
            alszakasz.append('*Figyelem: elemzetlen bejegyzés illeszkedik — %s %s %s*'
                              % (anom['entry_id'], anom['lemma'], anom['nyers_ertek']))

        hiv_sorok = lexikon_hivatkozasok_ehhez(strong)
        if hiv_sorok:
            van_hivatkozas_barmelyikhez = True
            for r in hiv_sorok:
                fajl_licenc_kulcsok['adat/lexikon_hivatkozasok.tsv'].add(r['szotar'])
                if r['szotar'] in TISZTAZATLAN_SZOTARAK:
                    tisztazatlan_erintve = True
                alszakasz.append('#### %s %s — %s. jelentés' % (r['szotar'], r['entry_id'], r['jelentes_szam']))
                alszakasz.append('> %s' % r['szoveg_en'])
                if r['forditas_hu']:
                    alszakasz.append('**🇭🇺** %s' % r['forditas_hu'])
                else:
                    alszakasz.append('Fordítás nincs (a `forditas_hu` üres).')
                alszakasz.append('*Forrás: %s*' % r['forrasfajl'])
        else:
            alszakasz.append('Nincs jelentés-hivatkozás a `lexikon_hivatkozasok.tsv`-ben.')

        reszek.append('\n\n'.join(alszakasz))

    if not fajl_licenc_kulcsok['adat/lexikon_hivatkozasok.tsv']:
        del fajl_licenc_kulcsok['adat/lexikon_hivatkozasok.tsv']

    torzs = '\n\n'.join(reszek)
    licenc_lista = _sorted_unique(
        LICENC[k] for kulcsok in fajl_licenc_kulcsok.values() for k in kulcsok
    )
    forras_licenc_parok = [
        (fajl, licenc)
        for fajl, kulcsok in fajl_licenc_kulcsok.items()
        for licenc in _sorted_unique(LICENC[k] for k in kulcsok)
    ]
    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d Strong-tokenjét fedi, %s jelentés-hivatkozással '
               'a `lexikon_hivatkozasok.tsv`-ből.'
               % (m['id'], len(tokenek), 'van' if van_hivatkozas_barmelyikhez else 'nincs'))
    blokk_szoveg = _lexikon_blokk(m['id'], 'szocikkek', sorted(fajl_licenc_kulcsok), licenc_lista, hatokor, torzs)
    return blokk_szoveg, tisztazatlan_erintve, forras_licenc_parok


# ---------------------------------------------------------------------------
# 3. lxx
# ---------------------------------------------------------------------------

_lxx_cache = {}


def lxx_sorok(fname):
    if fname not in _lxx_cache:
        path = os.path.join(KONKORDANCIA, 'LXX_kivonat_%s.tsv' % fname)
        _lxx_cache[fname] = L.read_tsv(path) if os.path.exists(path) else []
    return _lxx_cache[fname]


def blokk_lxx(m, sorai, tokenek):
    gorog_tokenek = {t for t in tokenek if t.startswith('G')}
    if not gorog_tokenek:
        hatokor = ('Ez a blokk a `[ID: %s]` motívum görög Strong-tokenjeit keresné az '
                    'LXX-kivonatban.' % m['id'])
        torzs = 'A motívum előfordulásaiban nincs görög Strong-szám, ezért az LXX-szűrés nem végezhető.'
        return _lexikon_blokk(m['id'], 'lxx', [], [], hatokor, torzs), []

    talalatsorok = []
    forras_fajlok = set()
    osz_igehelyek = 0
    for s in sorai:
        token = G.konyv_token(s['igehely'])
        if G.konyv_teszamentum(token) != 'ÓSZ':
            continue
        osz_igehelyek += 1
        fname = L._lxx_filename(token)
        if fname is None:
            continue
        forras_fajlok.add('konkordancia/LXX_kivonat_%s.tsv' % fname)
        for r in lxx_sorok(fname):
            if r['Igehely'] == s['igehely'] and r['Strong-szám'] in gorog_tokenek:
                talalatsorok.append(r)

    fejlec = ['| Igehely | Görög szóalak | Morfológiai kód | Strong | Forrás-jelzés |',
              '|---|---|---|---|---|']
    sorok = list(fejlec)
    for r in talalatsorok:
        sorok.append('| %s | %s | %s | %s | %s |' % (
            r['Igehely'], r['Görög szóalak'], r['Morfológiai kód'], r['Strong-szám'], r['Forrás']))
    if not talalatsorok:
        sorok.append('| — | — | — | — | — |')

    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d görög Strong-tokenjét keresi %d ÓSZ igehelyen '
               'az LXX-kivonatban, és %d találatot ad.'
               % (m['id'], len(gorog_tokenek), osz_igehelyek, len(talalatsorok)))
    torzs = '\n'.join(sorok)
    blokk_szoveg = _lexikon_blokk(m['id'], 'lxx', sorted(forras_fajlok), ['tisztazatlan'], hatokor, torzs)
    forras_licenc_parok = [(fajl, 'tisztazatlan') for fajl in sorted(forras_fajlok)]
    return blokk_szoveg, forras_licenc_parok


# ---------------------------------------------------------------------------
# 4. tsk_kh
# ---------------------------------------------------------------------------

_tsk_by_igehely = None
_kh_by_step = None


def tsk_index():
    global _tsk_by_igehely
    if _tsk_by_igehely is None:
        idx = {}
        for r in L.load_tsk():
            idx.setdefault(r['Igehely'], []).append(r)
        _tsk_by_igehely = idx
    return _tsk_by_igehely


def kh_index():
    global _kh_by_step
    if _kh_by_step is None:
        idx = {}
        for r in L.load_karoli_kh():
            idx.setdefault(r['Igehely'], []).append(r)
        _kh_by_step = idx
    return _kh_by_step


def blokk_tsk_kh(m, sorai, konyv_sorrend, hianyzo_konyvek):
    sorai_rendezve = sorted(
        sorai, key=lambda s: G.igehely_rendezo_kulcs(s['igehely'], konyv_sorrend, hianyzo_konyvek))

    bekezdesek = []
    nem_vizsgalhato = []
    talalat_szam = 0

    for s in sorai_rendezve:
        igehely = s['igehely']
        try:
            step = L.to_step(igehely)
        except ValueError:
            nem_vizsgalhato.append(igehely)
            continue

        tsk_talalatok = sorted(
            [r for r in tsk_index().get(igehely, []) if int(r['Votes']) >= 15],
            key=lambda r: -int(r['Votes'])
        )
        kh_talalatok = kh_index().get(step, [])

        if not tsk_talalatok and not kh_talalatok:
            continue

        sorok = ['#### %s' % igehely]
        for r in tsk_talalatok:
            sorok.append('- TSK: %s (Votes: %s)' % (r['Kapcsolódó igehely magyar megjelenítése'], r['Votes']))
            talalat_szam += 1
        for r in kh_talalatok:
            sorok.append('- Károli-KH: %s' % r['Kapcsolódó igehely magyar megjelenítése'])
            talalat_szam += 1
        bekezdesek.append('\n'.join(sorok))

    torzs_reszek = list(bekezdesek)
    if nem_vizsgalhato:
        torzs_reszek.append('*Versenkénti kereséssel nem vizsgálható: %s.*' % ', '.join(nem_vizsgalhato))
    torzs = '\n\n'.join(torzs_reszek) if torzs_reszek else 'Nincs TSK/Károli-KH találat ehhez a motívumhoz.'

    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d igehelyét veti össze a TSK (Votes ≥ 15) és a '
               'Károli-KH táblával; %d igehely ad legalább egy találatot (%d találat összesen), '
               '%d igehely versenkénti kereséssel nem vizsgálható.'
               % (m['id'], len(sorai_rendezve), len(bekezdesek), talalat_szam, len(nem_vizsgalhato)))
    blokk_szoveg = _lexikon_blokk(
        m['id'], 'tsk_kh',
        ['konkordancia/TSK_kereszthivatkozasok.tsv', 'konkordancia/Karoli_kereszthivatkozasok.tsv'],
        ['CC BY 4.0', 'közkincs'], hatokor, torzs
    )
    forras_licenc_parok = [
        ('konkordancia/TSK_kereszthivatkozasok.tsv', 'CC BY 4.0'),
        ('konkordancia/Karoli_kereszthivatkozasok.tsv', 'közkincs'),
    ]
    return blokk_szoveg, forras_licenc_parok


# ---------------------------------------------------------------------------
# 5. kapcsolatok
# ---------------------------------------------------------------------------

_kapcsolatok_cache = None


def kapcsolatok_sorok():
    global _kapcsolatok_cache
    if _kapcsolatok_cache is None:
        _, sorok = G.tsv_beolvas(KAPCSOLATOK_TSV)
        _kapcsolatok_cache = sorok
    return _kapcsolatok_cache


def blokk_kapcsolatok(m, konyv_sorrend, hianyzo_konyvek):
    sorok_ehhez = [r for r in kapcsolatok_sorok() if r['id'] == m['id']]

    if not sorok_ehhez:
        torzs = 'Nincs kapcsolat-sor a `kapcsolatok.tsv`-ben ehhez a motívumhoz.'
        hatokor = 'Ez a blokk a `[ID: %s]` motívum kapcsolat-sorait fedné a `kapcsolatok.tsv`-ből; 0 sor.' % m['id']
        return _lexikon_blokk(m['id'], 'kapcsolatok', ['adat/kapcsolatok.tsv'], ['projekt-adat'], hatokor, torzs), \
            [('adat/kapcsolatok.tsv', 'projekt-adat')]

    igehelyek = _sorted_unique(list(
        {r['forras_igehely'] for r in sorok_ehhez} | {r['cel_igehely'] for r in sorok_ehhez}
    ))
    igehelyek.sort(key=lambda ige: G.igehely_rendezo_kulcs(ige, konyv_sorrend, hianyzo_konyvek))
    node_id = {ige: 'n%d' % (i + 1) for i, ige in enumerate(igehelyek)}

    mermaid = ['```mermaid', 'graph LR']
    for ige in igehelyek:
        mermaid.append('    %s["%s"]' % (node_id[ige], ige))
    for r in sorok_ehhez:
        mermaid.append('    %s -->|%s| %s' % (
            node_id[r['forras_igehely']], r['tipus'], node_id[r['cel_igehely']]))
    mermaid.append('```')

    fejlec = ['| Forrás | Cél | Típus | Funkció | Bizonyosság | PaRDeS-szint |',
              '|---|---|---|---|---|---|']
    tabla_sorok = list(fejlec)
    for r in sorok_ehhez:
        tabla_sorok.append('| %s | %s | %s | %s | %s | %s |' % (
            r['forras_igehely'], r['cel_igehely'], r['tipus'], r['funkcio'],
            r['bizonyossag'], r['pardes_szint']))

    torzs = '\n'.join(mermaid) + '\n\n' + '\n'.join(tabla_sorok)
    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d kapcsolat-sorát fedi a `kapcsolatok.tsv`-ből, '
               '%d igehely-csomóponttal.' % (m['id'], len(sorok_ehhez), len(igehelyek)))
    blokk_szoveg = _lexikon_blokk(m['id'], 'kapcsolatok', ['adat/kapcsolatok.tsv'], ['projekt-adat'], hatokor, torzs)
    return blokk_szoveg, [('adat/kapcsolatok.tsv', 'projekt-adat')]


# ---------------------------------------------------------------------------
# 6. forrasok (9. szakasz)
# ---------------------------------------------------------------------------

def blokk_forrasok(m, fajl_licenc_blokk_lista):
    """fajl_licenc_blokk_lista: [(fajl, licenc, blokk_nev)] -- a ténylegesen
    felhasznált forrásfájlok, FÁJLONKÉNTI licenc-hozzárendeléssel (nem az
    egész blokk licenc-halmazát ráragasztva minden fájljára)."""
    per_fajl = {}
    for fajl, licenc, blokk_nev in fajl_licenc_blokk_lista:
        rekord = per_fajl.setdefault(fajl, {'licenc': set(), 'blokkok': set()})
        rekord['licenc'].add(licenc)
        rekord['blokkok'].add(blokk_nev)

    fejlec = ['| Forrás | Fájl | Licenc | Blokk |', '|---|---|---|---|']
    sorok = list(fejlec)
    tabla_licencek = set()
    for fajl in sorted(per_fajl):
        rekord = per_fajl[fajl]
        licenc = ', '.join(sorted(rekord['licenc']))
        blokkok = ', '.join(sorted(rekord['blokkok']))
        tabla_licencek.update(rekord['licenc'])
        sorok.append('| `%s` | `%s` | %s | %s |' % (
            os.path.basename(fajl), fajl, licenc, blokkok))

    hatokor = 'Ez a blokk a `[ID: %s]` motívum lexikon-oldalán ténylegesen felhasznált forrásokat sorolja fel.' % m['id']
    torzs = '\n'.join(sorok)
    return _lexikon_blokk(m['id'], 'forrasok', sorted(per_fajl), sorted(tabla_licencek), hatokor, torzs)


# ---------------------------------------------------------------------------
# Marker-blokk (a general.blokk() mintájára, licenc-mezővel bővítve)
# ---------------------------------------------------------------------------

def _cel_kulcs(motivum_id, blokk_nev):
    return 'lexikon#%s#%s' % (motivum_id, blokk_nev)


def _lexikon_blokk(motivum_id, blokk_nev, forras_lista, licenc_lista, hatokor_sor, torzs):
    cel_kulcs = _cel_kulcs(motivum_id, blokk_nev)
    fejl = '<!-- GENERÁLT-KEZDET: general.py --cel %s | forrás: %s | licenc: %s | ts=%s -->' % (
        cel_kulcs, ', '.join(forras_lista), ', '.join(licenc_lista), G.TS)
    veg = '<!-- GENERÁLT-VÉGE: %s -->' % cel_kulcs
    return '\n\n'.join([fejl, '*%s*' % hatokor_sor, torzs, veg])


# ---------------------------------------------------------------------------
# Teljes fájlváz (D2)
# ---------------------------------------------------------------------------

VAZ_SABLON = """# 📖 %(id)s — %(cim)s

## TUDOMÁNYOS REFERENCIA-VÁLTOZAT

*Vegyes fájl. A GENERÁLT-blokkok az `adat/` táblákból állnak elő (`python eszkozok/general.py --cel lexikon`), kézzel nem szerkeszthetők. A blokkokon kívüli szakaszok kézzel írandók; a generátor nem írja felül őket.*

## 0. Metaadatok

%(metaadat)s

## 1. Előfordulások

%(elofordulasok)s

## 1/b. PaRDeS keretrendszer *(kézi)*

*Kézzel írandó — a forrás-study 3. pontja alapján, a 2. szakasz lexikai adataival bővítve.*

## 2. Lexikon-szócikkek

%(szocikkek)s

### Miért fontos ez a lelet *(kézi)*

*Kézzel írandó.*

## 3. LXX-híd — nyers adat

%(lxx)s

## 4. TSK és Károli-KH — nyers eredmény

%(tsk_kh)s

### Minősítés *(kézi)*

*Kézzel írandó: független megerősítés / új találat / nem releváns.*

## 5. Kapcsolatok

%(kapcsolatok)s

### Alátámasztás *(kézi)*

*Kézzel írandó.*

## 6. Módszertani napló *(kézi)*

*Kézzel írandó.*

## 7. ÚJ FELISMERÉS *(kézi, ha van)*

## 8. Nyitott kérdések és séma-korlátok *(kézi)*

*Kézzel írandó.*

## 9. Források és licencek

%(forrasok)s
"""

BLOKK_NEVEK = ('metaadat', 'elofordulasok', 'szocikkek', 'lxx', 'tsk_kh', 'kapcsolatok', 'forrasok')


def render_lexikon_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek):
    """({blokk_nev: szoveg}, tisztazatlan_erintve) -- a hét blokk, teljes
    új-fájl vázhoz vagy meglévő fájlba blokk_beilleszt-tel való cseréhez
    (l. run()). A forrás/licenc pár-lista FÁJLONKÉNTI, nem a blokk egész
    licenc-halmazát ráragasztva minden fájlra."""
    tokenek = motivum_strong_tokenek(sorai)

    blokk_metaadat_szov, fl_metaadat = blokk_metaadat(m)
    blokk_elofordulasok_szov, fl_elofordulasok = blokk_elofordulasok(m, sorai, konyv_sorrend, hianyzo_konyvek)
    blokk_szocikkek_szov, tisztazatlan_erintve, fl_szocikkek = blokk_szocikkek(m, tokenek)
    blokk_lxx_szov, fl_lxx = blokk_lxx(m, sorai, tokenek)
    blokk_tsk_kh_szov, fl_tsk_kh = blokk_tsk_kh(m, sorai, konyv_sorrend, hianyzo_konyvek)
    blokk_kapcsolatok_szov, fl_kapcsolatok = blokk_kapcsolatok(m, konyv_sorrend, hianyzo_konyvek)

    fajl_licenc_blokk_lista = (
        [(fajl, licenc, 'metaadat') for fajl, licenc in fl_metaadat]
        + [(fajl, licenc, 'elofordulasok') for fajl, licenc in fl_elofordulasok]
        + [(fajl, licenc, 'szocikkek') for fajl, licenc in fl_szocikkek]
        + [(fajl, licenc, 'lxx') for fajl, licenc in fl_lxx]
        + [(fajl, licenc, 'tsk_kh') for fajl, licenc in fl_tsk_kh]
        + [(fajl, licenc, 'kapcsolatok') for fajl, licenc in fl_kapcsolatok]
    )
    blokk_forrasok_szov = blokk_forrasok(m, fajl_licenc_blokk_lista)

    blokkok = {
        'metaadat': blokk_metaadat_szov,
        'elofordulasok': blokk_elofordulasok_szov,
        'szocikkek': blokk_szocikkek_szov,
        'lxx': blokk_lxx_szov,
        'tsk_kh': blokk_tsk_kh_szov,
        'kapcsolatok': blokk_kapcsolatok_szov,
        'forrasok': blokk_forrasok_szov,
    }

    return blokkok, tisztazatlan_erintve


def epit_uj_fajl(m, blokkok):
    return VAZ_SABLON % {
        'id': m['id'],
        'cim': m.get('cim', ''),
        'metaadat': blokkok['metaadat'],
        'elofordulasok': blokkok['elofordulasok'],
        'szocikkek': blokkok['szocikkek'],
        'lxx': blokkok['lxx'],
        'tsk_kh': blokkok['tsk_kh'],
        'kapcsolatok': blokkok['kapcsolatok'],
        'forrasok': blokkok['forrasok'],
    }


_TS_LEVAGVA_RE = re.compile(r'\| ts=\S+ -->$')


def _fejlec_ts_nelkul(fejlec):
    return _TS_LEVAGVA_RE.sub('-->', fejlec)


def _blokk_beilleszt_fejleccel(fajl_szoveg, cel_kulcs, uj_blokk):
    """Mint a G.blokk_beilleszt, de a fejlécet (forrás/licenc) IS cseréli,
    ha az — a ts mezőt figyelmen kívül hagyva — eltér a régitől; a `ts=` a
    G.blokk_beilleszt-nél a törzzsel együtt fagyott be, ezért a fejlécben
    ténylegesen felhasznált forrás/licenc soha nem frissült (F6.5a L1). Ha
    sem a fejléc (ts nélkül), sem a törzs nem változott, a régi fejléc (a
    régi ts-sel) marad — így a nem érintett blokkok ts-e sem mozdul (K22)."""
    talalat = G.marker_par_keres(fajl_szoveg, cel_kulcs)
    if not talalat:
        raise ValueError('nincs marker-pár: %s' % cel_kulcs)
    kezd_idx, torzs_kezd, torzs_veg, _veg_idx = talalat
    regi_fejlec = fajl_szoveg[kezd_idx:torzs_kezd]
    regi_torzs = fajl_szoveg[torzs_kezd:torzs_veg]

    uj_fejlec_vege = uj_blokk.index('-->') + len('-->')
    uj_fejlec = uj_blokk[:uj_fejlec_vege]
    uj_torzs = G.blokk_torzs(uj_blokk, cel_kulcs)

    if _fejlec_ts_nelkul(regi_fejlec) == _fejlec_ts_nelkul(uj_fejlec) and regi_torzs == uj_torzs:
        return fajl_szoveg, 'változatlan'
    return fajl_szoveg[:kezd_idx] + uj_fejlec + uj_torzs + fajl_szoveg[torzs_veg:], 'frissítve'


def frissit_meglevo_fajlt(meglevo_szoveg, m, blokkok):
    szoveg = meglevo_szoveg
    for blokk_nev in BLOKK_NEVEK:
        cel_kulcs = _cel_kulcs(m['id'], blokk_nev)
        szoveg, _ = _blokk_beilleszt_fejleccel(szoveg, cel_kulcs, blokkok[blokk_nev])
    return szoveg


def run(args, motivumok, elofordulasok, konyv_sorrend, hianyzo_konyvek):
    """--ir/--ellenoriz: éles célfájl `lexikon/‹ID›_TUDOMANYOS.md` (F6.5,
    ELESITHETO). Egyébként (próba) a --kimenet (alapértelmezésben
    generalt_proba/) alá."""
    elof_id_szerint = G.elofordulasok_id_szerint(elofordulasok)
    kimenet_gyoker = (
        os.path.join(G.ROOT, 'lexikon') if (args.ir or args.ellenoriz)
        else os.path.join(args.kimenet, 'lexikon')
    )

    osszesitett_tisztazatlan = {}

    for m in motivumok:
        sorai = elof_id_szerint.get(m['id'], [])
        if not sorai:
            continue

        blokkok, tisztazatlan_erintve_szocikkek = render_lexikon_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek)
        osszesitett_tisztazatlan[m['id']] = (
            tisztazatlan_erintve_szocikkek or '| licenc: tisztazatlan |' in blokkok['lxx']
        )

        cel_ut = os.path.join(kimenet_gyoker, '%s_TUDOMANYOS.md' % m['id'])

        if os.path.exists(cel_ut):
            with io.open(cel_ut, encoding='utf-8', newline='') as f:
                meglevo = f.read()
            uj_szoveg = frissit_meglevo_fajlt(meglevo, m, blokkok)
            allapot = 'változatlan' if uj_szoveg == meglevo else 'frissítve'
        else:
            uj_szoveg = epit_uj_fajl(m, blokkok)
            allapot = 'új fájl'

        if args.ellenoriz:
            print('  %s: --ellenoriz, nincs írás (%s lenne)' % (m['id'], allapot))
            continue

        os.makedirs(kimenet_gyoker, exist_ok=True)
        with io.open(cel_ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(uj_szoveg)
        print('  %s: %s (%s, %d bájt)'
              % (m['id'], os.path.relpath(cel_ut, ROOT), allapot, os.path.getsize(cel_ut)))

    print('  tisztázatlan licencű forrás érintett-e (motívumonként): %s'
          % ', '.join('%s=%s' % (k, 'igen' if v else 'nem') for k, v in osszesitett_tisztazatlan.items()))
    return 0
