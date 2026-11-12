#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_strong_export.py -- a Károli 1908 – Strong szóillesztés nyílt mag (CC BY 4.0) generált exportja (F175,
FELADATOK #175).

A #22 gépi Károli–héber/görög párosítása (`adat/karoli_strong/parok_*.tsv`, `szavak_*.tsv`) a #172-ben mért
állapotban, változatlanul (1. változat): könyvenként egy pár- és egy szótábla OSIS-kulccsal, a Károli 1908
versszövege, és a #172 mérési eredménye (`meres.tsv`). A héber és görög szóalak (a TAHOT/TAGNT szövege) nem kerül
a csomagba: az eredeti szót a vers, a sorszáma és a Strong-száma azonosítja (az F174 mintája, a 2026-11-08-i
szerkesztői döntés: harmadik fél adata nem megy be). A külső összevetés forrásának adata sem: csak az összesített
egyezés.

Kimenet: `nyilt_karoli_strong/` — a mappa tartalma 1:1-ben a nyilvános adatrepó gyökere. Determinisztikus,
újrafuttatva bájtazonos. A `kozlemeny/` almappa (a rövid közlemény hu/en tervezete) generált, de nincs az ellenőrző
összegben, és a `.gitattributes` a kiadási archívumból kihagyja (export-ignore) a megjelenésig.

A nyilvános szövegek prózája itt áll; minden szám az adatból vagy a #172 mérőtábláiból számolódik (`szamok()`),
kézzel nem kerül a szövegbe. Ha egy szám nem olvasható ki, a szkript megáll.

TSV-olvasás `split('\\t')`, írás `'\\t'.join()` (nem `csv`).

Használat:
    python eszkozok/karoli_strong_export.py [--kimenet nyilt_karoli_strong]
"""
import argparse
import glob
import hashlib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nyilt_mag_export as NM  # noqa: E402  (OSIS-kulcs, közös azonosítók)
import karoli_strong_szovegek as SZ  # noqa: E402  (a nyilvános szövegek prózája)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = NM.GYOKER
KIMENET = 'nyilt_karoli_strong'
DOI = NM.DOI_KAROLI_STRONG                       # 10.5281/zenodo.24141884 (lefoglalt)
DOI_MODERN = '10.5281/zenodo.24141950'
DOI_MAG = NM.DOI_MAG
KANONIKUS_HELY = 'https://doi.org/' + DOI
CIM_HU = 'Károli 1908 – Strong szóillesztés'
CIM_EN = 'Károli 1908 – Strong word alignment'
KOZLEMENY_DIR = 'kozlemeny/'

PAROK = 'adat/karoli_strong/parok_*.tsv'
SZAVAK = 'adat/karoli_strong/szavak_*.tsv'
NEM_TR = 'adat/karoli_strong/nem_tr_parositott.tsv'
KAROLI = 'konkordancia/Karoli_1908.tsv'
F172_MERES = 'f172/meres_eredmeny.tsv'
F172_KULSO = 'f172/kulso/kulso_eredmeny.tsv'
F172_KERET = 'f172/keret.tsv'

PAR_FEJ = ['osis', 'token', 'alak_1908', 'eredeti_token', 'strong', 'kapcsolat', 'bizonyossag', 'allapot', 'nem_tr']
SZO_FEJ = ['osis', 'oldal', 'token', 'alak_1908', 'allapot', 'partner_token', 'strong', 'bizonyossag']
VERS_FEJ = ['osis', 'szoveg_1908']
MERES_FEJ = ['szakasz', 'cimke', 'n', 'x', 'p', 'also95', 'felso95', 'modszer']
FEJLEC_HU = ('# GENERÁLT: a %s – %s nyílt magjának exportja (CC BY 4.0), a projekt adataiból generálva — kézzel '
             'nem szerkesztendő; a „#” kezdetű sor megjegyzés.' % (NM.LEXIKON_CIM_HU, CIM_HU))
FEJLEC_EN = ('# GENERATED: export of the %s – %s open core (CC BY 4.0), generated from the project data — do not '
             'edit by hand; a line starting with "#" is a comment.' % (NM.LEXIKON_CIM_EN, CIM_EN))
STEP_ATTRIB = 'Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0)'
MORFEMA_RX = re.compile(r'^H90(0[1-9]|[1-4]\d)$')       # H9001–H9049: a TAHOT előtag-/rag-morfémái

SZO_ALLAPOT = {'parositva': 'parositva', 'betoldas': 'betoldas', 'forditatlan': 'forditatlan', 'fuggoben': 'fuggoben'}
BIZONYOSSAG = {'magas': 'magas', 'alacsony': 'alacsony', 'kezi': ''}

# a #172 mérőtáblájának címkéi -> a csomag kódjai (a kódkönyv írja le őket); ismeretlen címke -> megáll
RETEG = {'OSZ_mozes_magas': 'OSZ_mozes_magas', 'OSZ_mozes': 'OSZ_mozes_alacsony', 'OSZ_tortenet': 'OSZ_tortenet',
         'OSZ_koltoi': 'OSZ_koltoi', 'OSZ_profeta': 'OSZ_profeta', 'USZ_evangelium': 'USZ_evangelium',
         'USZ_level': 'USZ_level', 'USZ_jelenesek': 'USZ_jelenesek'}
HIBATIPUS = {'fölös pár': 'folos_par', 'azonos lexéma, más előfordulás': 'azonos_lexema_mas_elofordulas',
             'szomszédos token': 'szomszedos_token', 'rossz szó a versben': 'rossz_szo_a_versben'}
SULYOZOTT = {'OSZ (súlyozott)': 'OSZ', 'USZ (súlyozott)': 'USZ', 'OSSZES (súlyozott)': 'OSSZES'}
BONTAS = {'OSZ · tartalmi szó': 'OSZ_tartalmi_szo', 'OSSZES · tartalmi szó': 'OSSZES_tartalmi_szo',
          'OSZ · morféma (H9001–H9049)': 'OSZ_morfema', 'OSSZES · morféma (H9001–H9049)': 'OSSZES_morfema'}
KALIBRACIO = {'vak Opus-ellenőr = régi arany': 'ellenor_kezi_minta',
              'gépi pár (#22) = régi arany': 'gepi_kezi_minta',
              'vak Opus-ellenőr = régi arany (a hibás hármasok nélkül)': 'ellenor_kezi_minta_javitott',
              'gépi pár (#22) = régi arany (a hibás hármasok nélkül)': 'gepi_kezi_minta_javitott',
              'kimaradt arany-hármas (nincs vers / a kifejezés nincs a versben)': 'kezi_minta_nem_merheto'}
LEIRO = {'cél Károli-szó, amelyhez az ellenőr a gépinél több eredeti tokent jelölt': 'hianyzo_par'}
MODSZER_KOD = {'reteg': 'wilson95', 'sulyozott': 'retegzett_normal95', 'bontas': 'retegzett_leiro',
               'hibatipus': 'darab', 'leiro': 'darab', 'kalibracio': 'wilson95'}


# ----------------------------------------------------------------------------- olvasás

def tsv(rel):
    return NM.tsv(rel)


def fejsorok(rel):
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        return [s.rstrip('\n') for s in f if s.startswith('#')]


def relglob(minta):
    return sorted(os.path.relpath(p, GYOKER).replace('\\', '/') for p in glob.glob(os.path.join(GYOKER, minta)))


def kapcsolat(strong):
    reszek = strong.split('+')
    return 'morfema' if all(MORFEMA_RX.match(r) for r in reszek) else 'szo'


_OSIS = {}


def osis(ig):
    if ig not in _OSIS:
        _OSIS[ig] = NM.osis(ig)
    return _OSIS[ig]


def beolvas():
    _, versek = tsv(KAROLI)
    parok, szavak = [], []
    for rel in relglob(PAROK):
        parok += tsv(rel)[1]
    for rel in relglob(SZAVAK):
        szavak += tsv(rel)[1]
    _, nt = tsv(NEM_TR)
    return versek, parok, szavak, nt


# ----------------------------------------------------------------------------- átalakítás

def atalakit(versek, parok, szavak, nt):
    """Könyvenként a pár- és a szósorok. A sorrend a Károli-versek sorrendje, azon belül a sorszám. Megáll, ha
    egy sor verse nincs a Károli-szövegben, vagy egy pár magyar szava eltér a szótábla alakjától (nem találgat)."""
    vsor = {}
    konyvsor = []
    for i, v in enumerate(versek):
        ig = v['Igehely']
        if ig in vsor:
            raise SystemExit('átalakítás: kétszer álló Károli-vers: %s' % ig)
        vsor[ig] = i
        kk = osis(ig).split('.')[0]
        if kk not in konyvsor:
            konyvsor.append(kk)
    nem_tr = {(s['vers'], s['er_sorszam']) for s in nt}
    hu_alak = {}
    szo_ki = {}
    for s in szavak:
        if s['vers'] not in vsor:
            raise SystemExit('átalakítás: a szótábla verse nincs a Károli-szövegben: %s' % s['vers'])
        if s['allapot'] not in SZO_ALLAPOT or s['bizonyossag'] not in BIZONYOSSAG:
            raise SystemExit('átalakítás: ismeretlen állapot vagy bizonyosság: %s %s %s' % (
                s['vers'], s['allapot'], s['bizonyossag']))
        if s['oldal'] == 'hu':
            hu_alak[(s['vers'], s['sorszam'])] = s['szo']
        elif s['oldal'] != 'er':
            raise SystemExit('átalakítás: ismeretlen oldal: %r' % s['oldal'])
        o = osis(s['vers'])
        kulcs = (vsor[s['vers']], 0 if s['oldal'] == 'hu' else 1, int(s['sorszam']))
        sor = [o, s['oldal'], s['sorszam'], s['szo'] if s['oldal'] == 'hu' else '', SZO_ALLAPOT[s['allapot']],
               s['partner_sorszam'], s['strong'], BIZONYOSSAG[s['bizonyossag']]]
        szo_ki.setdefault(o.split('.')[0], []).append((kulcs, sor))
    par_ki = {}
    for p in parok:
        if p['vers'] not in vsor:
            raise SystemExit('átalakítás: a pártábla verse nincs a Károli-szövegben: %s' % p['vers'])
        if hu_alak.get((p['vers'], p['hu_sorszam'])) != p['hu_szo']:
            raise SystemExit('átalakítás: a pár magyar szava eltér a szótábláétól: %s %s' % (p['vers'], p['hu_sorszam']))
        o = osis(p['vers'])
        kulcs = (vsor[p['vers']], int(p['hu_sorszam']), int(p['er_sorszam']), p['strong'])
        sor = [o, p['hu_sorszam'], p['hu_szo'], p['er_sorszam'], p['strong'], kapcsolat(p['strong']),
               BIZONYOSSAG[p['bizonyossag']], 'javaslat', 'igen' if (p['vers'], p['er_sorszam']) in nem_tr else '']
        par_ki.setdefault(o.split('.')[0], []).append((kulcs, sor))
    konyvek = []
    for kk in konyvsor:
        konyvek.append((kk, [s for _, s in sorted(par_ki.get(kk, []))], [s for _, s in sorted(szo_ki.get(kk, []))]))
    vsorok = [[osis(v['Igehely']), v['Károli-szöveg (teljes vers)']] for v in versek]
    return konyvek, vsorok


def meres_sorok():
    """A #172 mérőtáblájának sorai a csomag kódjaival, és a külső összevetés összesítése (csak arányok)."""
    _, ss = tsv(F172_MERES)
    ki = []
    for s in ss:
        sz, c = s['szakasz'], s['cimke']
        if sz == 'reteg':
            kod = RETEG[c]
        elif sz == 'sulyozott':
            kod = SULYOZOTT[c]
        elif sz == 'bontas':
            kod = BONTAS[c]
        elif sz == 'hibatipus':
            reszek = [r.strip() for r in c.split('·')]
            alap = RETEG.get(reszek[0], reszek[0])
            if alap not in set(RETEG.values()) | {'OSSZES'}:
                raise SystemExit('mérés: ismeretlen hibatípus-réteg: %r' % c)
            if len(reszek) == 3:
                alap += {'tartalmi': '_tartalmi_szo', 'morféma': '_morfema'}[reszek[1]]
            kod = alap + ':' + HIBATIPUS[reszek[-1]]
        elif sz == 'kalibracio':
            kod = KALIBRACIO[c]
        elif sz == 'leiro':
            kod = LEIRO[c]
        else:
            raise SystemExit('mérés: ismeretlen szakasz: %r' % sz)
        ki.append([sz, kod, s['n'], s['x'], s['p'], s['also95'], s['felso95'],
                   MODSZER_KOD[sz] if s['p'] or sz in ('hibatipus', 'leiro') else 'darab'])
    for c in ('OSSZES', 'OSZ', 'USZ'):
        o = _f172(F172_KULSO, 'csoport', c)
        n = int(o['n_fo'])
        x = int(o['egyezik']) + int(o['konvencio'])
        if abs(x / n - float(o['forras_szerint'])) > 5e-5:
            raise SystemExit('mérés: a külső összevetés aránya nem jön ki a darabszámokból (%s)' % c)
        ki.append(['kulso', c + '_fo_szo', str(n), str(x), o['forras_szerint'], o['fs_also95'], o['fs_felso95'],
                   'wilson95'])
        x3 = n - int(o['elter_mi_hibank'])
        ki.append(['kulso', c + '_fo_szo_haromutas', str(n), str(x3), o['haromutas'], o['h3_also95'],
                   o['h3_felso95'], 'wilson95'])
    return ki


# ----------------------------------------------------------------------------- számok (generált)

def _f172(rel, oszlop, ertek):
    _, ss = tsv(rel)
    for s in ss:
        if s.get(oszlop) == ertek:
            return s
    raise SystemExit('szám: hiányzó sor %s=%s (%s)' % (oszlop, ertek, rel))


def _meres(msorok, szakasz, cimke):
    for s in msorok:
        if s[0] == szakasz and s[1] == cimke:
            return s
    raise SystemExit('szám: hiányzó mérési sor %s/%s' % (szakasz, cimke))


def _ts_datumok(rels):
    d = []
    for rel in rels:
        for s in fejsorok(rel):
            d += re.findall(r'\bts=(\d{4}-\d{2}-\d{2})', s)
    return d


def szamok(konyvek, vsorok, msorok):
    N = {}
    N['konyv'] = len(konyvek)
    N['vers'] = len(vsorok)
    psor = [s for _, ps, _ in konyvek for s in ps]
    ssor = [s for _, _, ss in konyvek for s in ss]
    N['par'] = len(psor)
    N['magas'] = sum(1 for s in psor if s[6] == 'magas')
    N['alacsony'] = sum(1 for s in psor if s[6] == 'alacsony')
    N['morfema'] = sum(1 for s in psor if s[5] == 'morfema')
    N['heber_par'] = sum(1 for s in psor if s[4].startswith('H'))
    N['gorog_par'] = sum(1 for s in psor if s[4].startswith('G'))
    N['nem_tr'] = sum(1 for s in psor if s[8] == 'igen')
    N['nem_tr_token'] = len({(s[0], s[3]) for s in psor if s[8] == 'igen'})
    hu = [s for s in ssor if s[1] == 'hu']
    er = [s for s in ssor if s[1] == 'er']
    N['hu_token'] = len(hu)
    N['er_token'] = len(er)
    for nev, lista in (('hu', hu), ('er', er)):
        for a in ('parositva', 'betoldas', 'forditatlan', 'fuggoben'):
            N['%s_%s' % (nev, a)] = sum(1 for s in lista if s[4] == a)
    N['fuggoben_vers'] = len({s[0] for s in hu if s[4] == 'fuggoben'})
    N['heber_morfema_arany'] = N['morfema'] / N['heber_par']
    # a #172 mérése
    for kod, kulcs in (('OSSZES', 'osszes'), ('OSZ', 'osz'), ('USZ', 'usz')):
        s = _meres(msorok, 'sulyozott', kod)
        N['p_' + kulcs], N['p_%s_a' % kulcs], N['p_%s_f' % kulcs] = s[4], s[5], s[6]
        N['n_' + kulcs] = int(s[2])
    for kod, kulcs in (('OSSZES_tartalmi_szo', 'tartalmi'), ('OSSZES_morfema', 'morf')):
        s = _meres(msorok, 'bontas', kod)
        N['p_' + kulcs], N['p_%s_a' % kulcs], N['p_%s_f' % kulcs] = s[4], s[5], s[6]
        N['n_' + kulcs] = int(s[2])
    for kod in RETEG.values():
        s = _meres(msorok, 'reteg', kod)
        N['r_' + kod], N['r_%s_a' % kod], N['r_%s_f' % kod] = s[4], s[5], s[6]
        N['rn_' + kod], N['rx_' + kod] = int(s[2]), int(s[3])
    N['reteg_n'] = int(_meres(msorok, 'reteg', 'OSZ_profeta')[2])
    N['minta'] = N['n_osszes']
    N['elteres'] = N['minta'] - int(_meres(msorok, 'sulyozott', 'OSSZES')[3])
    for t in HIBATIPUS.values():
        N['h_' + t] = int(_meres(msorok, 'hibatipus', 'OSSZES:' + t)[3])
        N['ht_' + t] = int(_meres(msorok, 'hibatipus', 'OSSZES_tartalmi_szo:' + t)[3])
        N['hm_' + t] = int(_meres(msorok, 'hibatipus', 'OSSZES_morfema:' + t)[3])
    if sum(N['h_' + t] for t in HIBATIPUS.values()) != N['elteres']:
        raise SystemExit('szám: a hibatípusok összege nem az eltérések száma')
    N['hianyzo_par'] = int(_meres(msorok, 'leiro', 'hianyzo_par')[3])
    for kod, kulcs in (('ellenor_kezi_minta', 'kal_ell'), ('gepi_kezi_minta', 'kal_gep')):
        s = _meres(msorok, 'kalibracio', kod)
        N[kulcs], N[kulcs + '_a'], N[kulcs + '_f'], N[kulcs + '_n'] = s[4], s[5], s[6], int(s[2])
    for c, kulcs in (('OSSZES', 'k'), ('OSZ', 'ko'), ('USZ', 'ku')):
        s = _meres(msorok, 'kulso', c + '_fo_szo')
        N[kulcs + '_n'], N[kulcs + '_fs'], N[kulcs + '_fs_a'], N[kulcs + '_fs_f'] = int(s[2]), s[4], s[5], s[6]
        N[kulcs + '_elter'] = int(s[2]) - int(s[3])
        s = _meres(msorok, 'kulso', c + '_fo_szo_haromutas')
        N[kulcs + '_h3'], N[kulcs + '_h3_a'], N[kulcs + '_h3_f'] = s[4], s[5], s[6]
        N[kulcs + '_mi'] = int(s[2]) - int(s[3])
    N['kulso_fejezet'] = len([s for s in tsv(F172_KULSO)[1] if re.match(r'^\S+ \d+$', s.get('csoport', ''))])
    # a keret: a mért párkészlet egyezik a csomagéval
    N['keret'] = int(_f172(F172_KERET, 'reteg', 'OSSZES')['parsor'])
    if N['keret'] != N['par']:
        raise SystemExit('szám: a #172 keretének párszáma (%d) nem a csomagé (%d): a mért állapot változott'
                         % (N['keret'], N['par']))
    # adatállapot: a forrástáblák fejlécének ts-dátuma és utolsó commitja közül a későbbi
    datumok = _ts_datumok(relglob(PAROK) + relglob(SZAVAK) + [NEM_TR])
    try:
        g = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', 'adat/karoli_strong'],
                           cwd=GYOKER, capture_output=True, text=True, encoding='utf-8')
        if re.match(r'^\d{4}-\d{2}-\d{2}$', g.stdout.strip()):
            datumok.append(g.stdout.strip())
    except OSError:
        pass
    N['adatallapot'] = max(datumok)
    return N


# ----------------------------------------------------------------------------- névelő (a/az)

# névelő + szám (ezres tagolással vagy anélkül, sorszámnévvel is: „az 1. kiadás”); a szám után nem állhat betű
NEVELO_SZAM_RX = re.compile(r'(?<![\w(])([Aa]z?) (\d{1,3}(?: \d{3})+|\d+)(?![\w(])')
MAGANHANGZO = 'aáeéiíoóöőuúüűAÁEÉIÍOÓÖŐUÚÜŰ'


def szam_nevelo(szam):
    """A szám elé illő névelő a kiejtés szerint: „az”, ha a kiejtés magánhangzóval kezdődik (egy, öt, ezer, ötven,
    ötszáz, egymillió…; sorszámnévként első, ötödik, ezredik…), egyébként „a”. A vezető számcsoport dönt: az 5-tel
    kezdődő csoport mindig „öt…”; az egyjegyű 1-es csoport „egy/ezer/egymillió/első”; a 1x és 1xx „tíz/tizen/száz”."""
    vezeto = szam.split(' ')[0]
    return 'az' if vezeto[0] == '5' or vezeto == '1' else 'a'


def szo_nevelo(szo):
    """A szó (vagy szám) elé illő névelő."""
    if szo[:1].isdigit():
        return szam_nevelo(szo)
    return 'az' if szo[:1] in MAGANHANGZO else 'a'


def nevelo_javit(szoveg):
    """Magyar szövegben a szám előtti névelőt a kiejtéshez igazítja (a nagybetűt megtartja)."""
    def csere(m):
        uj = szam_nevelo(m.group(2))
        return (uj.capitalize() if m.group(1)[0] == 'A' else uj) + ' ' + m.group(2)
    return NEVELO_SZAM_RX.sub(csere, szoveg)


def nevelo_hibak(szoveg):
    """A szám előtti hibás névelők listája (a kapu használja), és a kiejtés szerint el nem döntött „a(z)” alak."""
    ki = ['%s %s' % (m.group(1), m.group(2)) for m in NEVELO_SZAM_RX.finditer(szoveg)
          if m.group(1).lower() != szam_nevelo(m.group(2))]
    ki += ['a(z)' for _ in re.finditer(r'\b[Aa]\(z\)', szoveg)]
    return ki


def ezres(n, nyelv='hu'):
    s = '{:,}'.format(int(n))
    return s.replace(',', ' ' if nyelv == 'hu' else ',')


def szazalek(p, nyelv='hu', jegy=2):
    s = ('%.' + str(jegy) + 'f') % (float(p) * 100)
    return s.replace('.', ',') if nyelv == 'hu' else s


def fmt(N, nyelv):
    """A szövegek behelyettesítő szótára: ezres tagolás, százalék."""
    F = {}
    for k, v in N.items():
        if isinstance(v, int):
            F[k] = ezres(v, nyelv)
        elif isinstance(v, str) and re.match(r'^0\.\d+$|^1\.0+$', v):
            F[k] = szazalek(v, nyelv)
    F['heber_morfema_arany'] = szazalek(N['heber_morfema_arany'], nyelv, 1)
    F['morfema_arany'] = szazalek(N['morfema'] / N['par'], nyelv, 1)
    F['doi'] = DOI
    F['doi_modern'] = DOI_MODERN
    F['doi_mag'] = DOI_MAG
    F['lex_hu'] = NM.LEXIKON_CIM_HU
    F['lex_en'] = NM.LEXIKON_CIM_EN
    F['szerzo'] = NM.SZERZO
    F['orcid'] = NM.ORCID
    F['adatallapot'] = N['adatallapot']
    F['cim'] = CIM_HU
    F['cim_en'] = CIM_EN
    F['step'] = STEP_ATTRIB
    F['cim_modern_hu'] = 'Modernizált Károli – Strong'
    F['cim_modern_en'] = 'Modernised Károli – Strong'
    return F


# ----------------------------------------------------------------------------- összeállítás

def tsv_szoveg(fej, sorok):
    ki = [FEJLEC_HU, FEJLEC_EN, '\t'.join(fej)]
    ki += ['\t'.join(s) for s in sorok]
    return '\n'.join(ki) + '\n'


def kodkonyv_md():
    ki = ['# Kódkönyv / Codebook', '', '*%s / %s*' % (CIM_HU, CIM_EN), '']
    for fajl, cim in SZ.KODKONYV_FAJLOK:
        ki += ['## %s' % cim, '', '| oszlop / column | érték / value | leírás | description |', '|---|---|---|---|']
        for f, o, e, hu, en in SZ.KODKONYV_SOROK:
            if f == fajl:
                ki.append('| `%s` | %s | %s | %s |' % (o, ('`%s`' % e) if e else '', hu, en))
        ki.append('')
    return '\n'.join(ki)


def export():
    versek, parok, szavak, nt = beolvas()
    konyvek, vsorok = atalakit(versek, parok, szavak, nt)
    msorok = meres_sorok()
    N = szamok(konyvek, vsorok, msorok)
    hu, en = fmt(N, 'hu'), fmt(N, 'en')
    fajlok = {}
    for i, (kk, ps, ss) in enumerate(konyvek, 1):
        fajlok['parok/%02d_%s.tsv' % (i, kk)] = tsv_szoveg(PAR_FEJ, ps)
        fajlok['szavak/%02d_%s.tsv' % (i, kk)] = tsv_szoveg(SZO_FEJ, ss)
    fajlok['versek.tsv'] = tsv_szoveg(VERS_FEJ, vsorok)
    fajlok['meres.tsv'] = tsv_szoveg(MERES_FEJ, msorok)
    fajlok['kodkonyv.tsv'] = tsv_szoveg(['fajl', 'oszlop', 'ertek', 'leiras_hu', 'leiras_en'],
                                        [list(s) for s in SZ.KODKONYV_SOROK])
    fajlok['KODKONYV.md'] = kodkonyv_md()
    for nev, sablon, d in SZ.SZOVEGEK:
        fajlok[nev] = nevelo_javit(sablon.format(**hu)) if d == 'hu' else sablon.format(**en)
    fajlok['.gitattributes'] = SZ.GITATTRIBUTES
    # ellenőrző összeg: minden kiadott fájl, a közlemény-tervezet nélkül
    sor = ['%s  %s' % (hashlib.sha256(fajlok[rel].encode('utf-8')).hexdigest(), rel) for rel in sorted(fajlok)]
    fajlok['ELLENORZO_OSSZEG.sha256'] = '\n'.join(sor) + '\n'
    hash_ = hashlib.sha256(fajlok['ELLENORZO_OSSZEG.sha256'].encode('utf-8')).hexdigest()
    datum = N['adatallapot']
    fajlok['KIADAS.txt'] = ('kiadas_azonosito: %s-%s\nadatallapot_datuma: %s\ntartalmi_hash_sha256: %s\n'
                            'kozzeteteli_hely: %s\n' % (datum, hash_[:16], datum, hash_, KANONIKUS_HELY))
    fajlok['RELEASE.txt'] = ('release_id: %s-%s\ndata_state_date: %s\ncontent_hash_sha256: %s\n'
                             'publication_place: %s\n' % (datum, hash_[:16], datum, hash_, KANONIKUS_HELY))
    # a közlemény-tervezet (export-ignore; nincs az ellenőrző összegben)
    for nev, sablon, d in SZ.KOZLEMENY:
        fajlok[KOZLEMENY_DIR + nev] = nevelo_javit(sablon.format(**hu)) if d == 'hu' else sablon.format(**en)
    return fajlok, N


def kezirat(N):
    """A második data paper kézirata (hu/en): a repó gyökeréhez viszonyított út -> (törzs, teljes szöveg). A törzs
    a nyilvános szöveg (a kapu ezt ellenőrzi), a teljes szöveg a GENERÁLT-jelöléssel kezdődik."""
    hu, en = fmt(N, 'hu'), fmt(N, 'en')
    ki = {}
    for rel, sablon, d in SZ.KEZIRAT:
        torzs = nevelo_javit(sablon.format(**hu)) if d == 'hu' else sablon.format(**en)
        ki[rel] = (torzs, SZ.KEZIRAT_FEJ + torzs)
    return ki


def kezirat_kiir(N):
    for rel, (_, szoveg) in kezirat(N).items():
        with open(os.path.join(GYOKER, rel), 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)


def kiir(fajlok, kimenet):
    abs_ki = os.path.join(GYOKER, kimenet) if not os.path.isabs(kimenet) else kimenet
    if os.path.isdir(abs_ki):
        for gy, _, nevek in os.walk(abs_ki):
            for n in nevek:
                rel = os.path.relpath(os.path.join(gy, n), abs_ki).replace('\\', '/')
                if rel not in fajlok:
                    os.remove(os.path.join(gy, n))
    for rel, tartalom in fajlok.items():
        ut = os.path.join(abs_ki, rel)
        os.makedirs(os.path.dirname(ut), exist_ok=True)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(tartalom)
    return abs_ki


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--kimenet', default=KIMENET)
    a = ap.parse_args()
    fajlok, N = export()
    ut = kiir(fajlok, a.kimenet)
    if a.kimenet == KIMENET:
        kezirat_kiir(N)          # a kézirat csak a kanonikus futáskor (a --kimenet próba a repón kívül marad)
    print('Károli 1908 – Strong szóillesztés exportálva: %s (%d fájl)' % (ut, len(fajlok)))
    for k in ('konyv', 'vers', 'par', 'hu_token', 'er_token', 'hu_parositva', 'hu_betoldas', 'hu_fuggoben',
              'er_parositva', 'er_forditatlan', 'er_fuggoben', 'morfema', 'nem_tr', 'keret'):
        print('  %-16s %9d' % (k, N[k]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
