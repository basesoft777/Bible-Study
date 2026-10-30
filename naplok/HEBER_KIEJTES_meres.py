"""Kísérleti mérés (N-F131w, DT426 utóhang): mennyire pontos egy
determinisztikus gépi magyaros héber kiejtés (átírás)?

NEM éles eszköz: nem az eszkozok/ alatt él, a lapokba nincs bekötve, adatot
(adat/) nem ír, lexikonlapot nem generál. Csak naplót ír:
  naplok/HEBER_KIEJTES_meres.tsv        -- soronkénti táblázat (A, B, C halmaz)
  naplok/HEBER_KIEJTES_meres_osszesito.txt -- összesítés (a jelentés ebből idéz)

Két átíró út:
  1. NIQQUD: pontozott héber szó -> magyaros kiejtés (saját szabályok, alább).
  2. STEP: STEPBible angolos átírás (TBESH 5. oszlop, TAHOT `Kiejtés`)
     -> magyaros kiejtés (betűcsere + hosszúság-heurisztika; a STEP nem
     jelöl magánhangzó-hosszúságot).
A meglévő OSHL-gépezet (eszkozok/heber_kiejtes_jeloltek.py) a B halmazon
is fut (régi konvencióval); az A halmazon körkörös, l. a jelentést.

Arany-halmazok:
  A: adat/kiejtes_kivetelek.tsv 26 héber sora (jóváhagyott, D34-D37 konvenció)
  B: naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv héber `arany`/`valodi`
     párjai (a régi, kézzel írt ISTENTISZT-001 lap, D34/D35 ELŐTTI konvenció:
     ח -> h, rafés כ -> k); csak pontozott, kommentár nélküli alakok
  C: 20 ragozott TAHOT-alak az ISTENTISZT-001 helyeiről -- nincs arany

Kalibrálás és keresztellenőrzés: mindkét út néhány bináris/többértékű
szabályparaméterrel fut (PARAM_TER). A paraméterek a) a priori (a mérés előtt
rögzített, szokásos konvenció), b) az A halmaz egészén kalibrálva,
c) leave-one-out (a kihagyott alakon mérve, a többi 25-ön kalibrálva),
d) kétfelé osztás (13/13, 200 véletlen felosztás átlaga) szerint mérve.

TSV: split('\\t') / '\\t'.join(), csv modul nélkül (CLAUDE.md).
"""

import itertools
import os
import random
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import heber_kiejtes_jeloltek as oshl_gep  # noqa: E402  (a meglévő S1.7 gépezet)

KIVETELEK = os.path.join(ROOT, 'adat', 'kiejtes_kivetelek.tsv')
TBESH = os.path.join(ROOT, 'konkordancia', 'TBESH.txt')
TAHOT = os.path.join(ROOT, 'konkordancia', 'TAHOT_kivonat.tsv')
OSHL = os.path.join(ROOT, 'konkordancia', 'OSHL_lexikalis_index.tsv')
TESZTKESZLET = os.path.join(ROOT, 'naplok', 'SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv')
ELOFORDULASOK = os.path.join(ROOT, 'adat', 'elofordulasok.tsv')
KI_TSV = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_meres.tsv')
KI_OSSZ = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_meres_osszesito.txt')

# --- Unicode-jelek ---------------------------------------------------------
SEVA, HATAF_SZEGOL, HATAF_PATAH, HATAF_KAMEC = 'ְ', 'ֱ', 'ֲ', 'ֳ'
HIREK, CERE, SZEGOL, PATAH, KAMEC = 'ִ', 'ֵ', 'ֶ', 'ַ', 'ָ'
HOLAM, HOLAM_VAV, KUBBUC = 'ֹ', 'ֺ', 'ֻ'
DAGES, METEG, MAKKEF, RAFE = 'ּ', 'ֽ', '־', 'ֿ'
SIN_PONT, SZIN_PONT, KAMEC_KATAN = 'ׁ', 'ׂ', 'ׇ'
MAGANHANGZO = {HATAF_SZEGOL, HATAF_PATAH, HATAF_KAMEC, HIREK, CERE, SZEGOL,
               PATAH, KAMEC, HOLAM, HOLAM_VAV, KUBBUC, KAMEC_KATAN}
HATAF = {HATAF_SZEGOL, HATAF_PATAH, HATAF_KAMEC}
HOSSZU = {KAMEC, CERE, HOLAM, HOLAM_VAV}  # a sevá-szabályhoz (mater nélkül)

ALEF, BET, GIMEL, DALET, HE, VAV, ZAJIN, CHET, TET, JOD = (
    'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז',
    'ח', 'ט', 'י')
KAF_V, KAF, LAMED, MEM_V, MEM, NUN_V, NUN, SZAMEH, AJIN = (
    'ך', 'כ', 'ל', 'ם', 'מ', 'ן', 'נ',
    'ס', 'ע')
PE_V, PE, CADE_V, CADE, KOF, RES, SIN, TAV = (
    'ף', 'פ', 'ץ', 'צ', 'ק', 'ר', 'ש', 'ת')
BEGADKEFAT = {BET, GIMEL, DALET, KAF, KAF_V, PE, PE_V, TAV}
TOROKHANG = {ALEF, HE, CHET, AJIN, RES}

ALAP_MSH = {  # mássalhangzó -> magyaros betű (a paraméterfüggők külön)
    ALEF: '', BET: 'b', GIMEL: 'g', DALET: 'd', HE: 'h', VAV: 'v', ZAJIN: 'z',
    TET: 't', JOD: 'j', KAF: 'k', KAF_V: 'k', LAMED: 'l', MEM: 'm', MEM_V: 'm',
    NUN: 'n', NUN_V: 'n', AJIN: '', PE: 'p', PE_V: 'p', CADE: 'c', CADE_V: 'c',
    KOF: 'k', RES: 'r', TAV: 't', SIN: 's', SZAMEH: 's', CHET: 'ch',
}
LAGY = {BET: 'v', KAF: 'ch', KAF_V: 'ch', PE: 'f', PE_V: 'f'}

# --- Paramétertér ----------------------------------------------------------
# Minden paraméter első értéke az A PRIORI választás (a szokásos magyaros
# tudományos-népszerű konvenció, a mérés előtt rögzítve).
PARAM_TER_NIQQUD = {
    'chet': ['ch', 'h'],                 # ח
    'kaf_lagy': ['ch', 'k'],             # rafés כ
    'szamech': ['sz', 's'],              # ס
    'sin': ['sz', 's'],                  # שׂ
    'dages_forte_kettoz': [True, False], # kettőzés
    'seva_hosszu_utan': ['meteg', 'hangzo', 'nema'],  # sevá hosszú mgh. után
    'kamec_katan': [True, False],        # kámec zárt hangsúlytalan szótagban -> o
    'szegol_jod': ['é', 'e'],            # szegol + mater jod
    'hirek_jod': ['í', 'i'],             # hirek + mater jod
    'furtiv': [True, False],             # furtív patah a mássalhangzó elé
    'tetragramma': ['JHVH', 'gepi'],
    'szokezdo_begadkefat': ['kemeny', 'pont_szerint'],  # dáges nélküli szókezdő ב/כ/פ (D34: kemény)     # יהוה
}
PARAM_TER_STEP = {
    'a_nyilt': ['á', 'a'],     # nyílt szótagbeli a
    'a_zart': ['a', 'á'],      # zárt szótagbeli a
    'e_zart': ['e', 'é'],      # zárt szótagbeli e (cere vagy szegol?)
    'i': ['i', 'í'],
    'o': ['ó', 'o'],
    'u': ['ú', 'u'],
    'sz': ['sz', 's'],         # STEP s (számech és sin közös!)
    'ch': ['ch', 'h'],         # STEP ch (ח)
    'kh': ['ch', 'k'],         # STEP kh (rafés כ)
}


def a_priori(ter):
    return {k: v[0] for k, v in ter.items()}


# --- NIQQUD-átíró ----------------------------------------------------------
def tisztit(szo):
    """NFD, kantilláció (U+0591-U+05AF) és egyéb írásjel törlése; a meteg
    (U+05BD) megmarad, mert a sevá/kámec-döntéshez kell."""
    s = unicodedata.normalize('NFD', szo)
    ki = []
    for c in s:
        o = ord(c)
        if 0x0591 <= o <= 0x05AF or c in '׀׃ׅׄ׆׳״':
            continue
        ki.append(c)
    return ''.join(ki)


def betuk(szo):
    """[{'b': betű, 'j': set(jelek)}] -- egy szó (makkef nélkül)."""
    ls = []
    for c in szo:
        if ALEF <= c <= TAV:
            ls.append({'b': c, 'j': set(), 'jl': []})
        elif ls and 'ְ' <= c <= 'ׇ':
            ls[-1]['j'].add(c)
            ls[-1]['jl'].append(c)
    return ls


def mgh(bet):
    # determinisztikus: két magánhangzójelnél (pl. יְרוּשָׁלִַם) a szövegbeli első
    return next((c for c in bet['jl'] if c in MAGANHANGZO), None)


def niqqud_szo(szo, p, nyom, makkef_utan=False):
    """Egy szó átírása. `nyom`: a meghozott döntések kategóriái (lista)."""
    ls = betuk(szo)
    if not ls:
        return ''
    massal = ''.join(b['b'] for b in ls)
    if massal == JOD + HE + VAV + HE and p['tetragramma'] == 'JHVH':
        nyom.append('tetragramma')
        return 'JHVH'
    n = len(ls)
    # 1. matres lectionis és vav-magánhangzók előfeldolgozása
    for i, b in enumerate(ls):
        b['mater'] = False
        b['vok'] = mgh(b)          # a betű után ejtett magánhangzó
        b['seva'] = SEVA in b['j']
    for i, b in enumerate(ls):
        elo = ls[i - 1] if i else None
        if b['b'] == VAV and i > 0:
            if DAGES in b['j'] and b['vok'] is None and not b['seva'] and elo['vok'] is None:
                elo['vok'] = 'U'           # surek
                elo['seva'] = False
                b['mater'] = True
                continue
            if b['vok'] in (HOLAM, HOLAM_VAV) and elo['vok'] is None and not elo['seva']:
                elo['vok'] = HOLAM          # holam male
                b['mater'] = True
                continue
            if b['vok'] is None and not b['seva'] and elo['vok'] in (HOLAM, HOLAM_VAV):
                b['mater'] = True           # holam az előző betűn, néma vav
                nyom.append('mater')
                continue
        if b['b'] == JOD and i > 0 and b['vok'] is None and not b['seva'] and DAGES not in b['j']:
            if elo['vok'] == HIREK:
                elo['vok'] = 'I'
                b['mater'] = True
                nyom.append('mater_jod')
                continue
            if elo['vok'] == CERE:
                b['mater'] = True
                continue
            if elo['vok'] == SZEGOL:
                elo['vok'] = 'SZJ'
                b['mater'] = True
                nyom.append('mater_jod')
                continue
            if elo['vok'] == KAMEC and i + 1 < n and ls[i + 1]['b'] == VAV and i + 1 == n - 1:
                b['mater'] = True           # -áv végződés (-ָיו)
                continue
        if b['b'] in (HE, ALEF) and i == n - 1 and b['vok'] is None and DAGES not in b['j']:
            b['mater'] = True               # szóvégi néma hé / álef
    # 2. dágesek és sevák
    ki = []
    elozo_hangzo_seva = False
    for i, b in enumerate(ls):
        if b['mater']:
            continue
        if (i == 0 and p.get('kotoszo_u') and b['b'] == VAV and DAGES in b['j']
                and b['vok'] is None and not b['seva'] and n > 1):
            b['vok'] = 'U'                   # szókezdő kötőszói וּ (ú), utána hangzó sevá
            b['kotoszo'] = True
            nyom.append('kotoszo_u')
            ki.append(('ú', None))
            continue
        elo = None
        for k in range(i - 1, -1, -1):
            if not ls[k]['mater'] or ls[k]['b'] in (ALEF,):
                elo = ls[k]
                break
        else:
            elo = None
        # az előző (nem-mater) betű szótagja nyitott, ha ejtett magánhangzója van
        elozo_vok = None
        if i > 0:
            # a közvetlen előző betű, a mater figyelembevételével
            k = i - 1
            while k >= 0 and ls[k]['mater']:
                k -= 1
            if k >= 0:
                elozo_vok = ls[k]['vok'] if not ls[k].get('seva_hangzo') is False else ls[k]['vok']
                elozo_obj = ls[k]
            else:
                elozo_obj = None
        else:
            elozo_obj = None
        dages = DAGES in b['j'] and not (b['b'] == HE and i == n - 1)
        forte = False
        if dages and i > 0 and elozo_obj is not None and elozo_obj['vok'] is not None:
            forte = True
        msh = ALAP_MSH[b['b']]
        if b['b'] == SIN:
            msh = 's' if SIN_PONT in b['j'] or SZIN_PONT not in b['j'] else p['sin']
            if SZIN_PONT in b['j']:
                nyom.append('sin')
        if b['b'] == SZAMEH:
            msh = p['szamech']
            nyom.append('szamech')
        if b['b'] == CHET:
            msh = p['chet']
            nyom.append('chet')
        if b['b'] in LAGY:
            if dages or (i == 0 and p['szokezdo_begadkefat'] == 'kemeny'):
                msh = ALAP_MSH[b['b']]
            else:
                msh = LAGY[b['b']]
                if b['b'] in (KAF, KAF_V):
                    msh = p['kaf_lagy']
                    nyom.append('kaf_lagy')
                nyom.append('begadkefat')
        if b['b'] == HE and i == n - 1 and DAGES in b['j']:
            msh = 'h'                        # mappik
        if forte and msh and b['b'] not in TOROKHANG:
            nyom.append('dages_forte')
            if p['dages_forte_kettoz']:
                msh = msh[0] + msh if len(msh) == 1 else (msh[0] + msh if msh == 'sz' else msh)
        # sevá-döntés
        vok = b['vok']
        hangzo_seva = False
        if b['seva'] and vok is None:
            if i == 0:
                hangzo_seva = True           # szókezdő (egybetűs előtag is: בְּ)
            elif i == n - 1:
                hangzo_seva = False
            elif forte:
                hangzo_seva = True
            elif elozo_obj is not None and elozo_obj.get('kotoszo'):
                hangzo_seva = True
            elif elozo_hangzo_seva is False and elozo_obj is not None and elozo_obj['seva'] and elozo_obj['vok'] is None:
                hangzo_seva = True           # két sevá közül a második
            elif elozo_obj is not None and elozo_obj['vok'] in HOSSZU | {'I', 'U'}:
                nyom.append('seva_hosszu_utan')
                mod = p['seva_hosszu_utan']
                if mod == 'hangzo':
                    hangzo_seva = True
                elif mod == 'meteg':
                    hangzo_seva = METEG in elozo_obj['j']
                if elozo_obj['vok'] == KAMEC and p['kamec_katan'] and not hangzo_seva:
                    pass
            else:
                hangzo_seva = False
            nyom.append('seva')
        b['seva_hangzo'] = hangzo_seva
        elozo_hangzo_seva = hangzo_seva if b['seva'] else None
        # furtív patah
        if (p['furtiv'] and i == n - 1 and vok == PATAH and b['b'] in (CHET, AJIN, HE)
                and elozo_obj is not None and elozo_obj['vok'] not in (None, PATAH, KAMEC)):
            nyom.append('furtiv')
            ki.append(('a', None))
            ki.append((msh, None))
            continue
        ki.append((msh, b))
        if vok is not None:
            ki.append((vok, b))
        elif hangzo_seva:
            ki.append(('e', None))
    # 3. magánhangzók kiírása (kámec kátán: a következő mássalhangzó néma sevás)
    szoveg = []
    for idx, (t, b) in enumerate(ki):
        if b is None or t not in MAGANHANGZO | {'I', 'U', 'SZJ'}:
            szoveg.append(t)
            continue
        if t == KAMEC:
            katan = False
            if KAMEC_KATAN in b['j']:
                katan = True
            elif makkef_utan and p.get('makkef_katan') and METEG not in b['j']:
                # makkef előtt a szó hangsúlytalan: az utolsó, zárt szótagbeli kámec kátán
                pos = ls.index(b)
                kesobb = [x for x in ls[pos + 1:] if not x['mater']]
                if kesobb and not any(x['vok'] is not None or x['seva_hangzo'] for x in kesobb):
                    katan = True
            elif p['kamec_katan'] and METEG not in b['j']:
                # a következő ejtett mássalhangzó néma sevás (zárt szótag, nem szóvég)
                pos = ls.index(b)
                for k in range(pos + 1, len(ls)):
                    if ls[k]['mater']:
                        continue
                    if ls[k]['seva'] and ls[k]['vok'] is None and not ls[k]['seva_hangzo'] and k != len(ls) - 1:
                        katan = True
                    elif ls[k]['vok'] == HATAF_KAMEC:
                        katan = True
                    break
            if katan:
                nyom.append('kamec_katan')
            szoveg.append('o' if katan else 'á')
            continue
        szoveg.append({
            HATAF_SZEGOL: 'e', HATAF_PATAH: 'a', HATAF_KAMEC: 'o', HIREK: 'i',
            CERE: 'é', SZEGOL: 'e', PATAH: 'a', HOLAM: 'ó', HOLAM_VAV: 'ó',
            KUBBUC: 'u', KAMEC_KATAN: 'o', 'I': p['hirek_jod'], 'U': 'ú',
            'SZJ': p['szegol_jod'],
        }[t])
    return ''.join(szoveg)


def niqqud(alak, p):
    nyom = []
    alak = tisztit(alak)
    szavak = []
    for szo in alak.split():
        reszek = szo.split(MAKKEF)
        szavak.append('-'.join(niqqud_szo(r, p, nyom, makkef_utan=(k < len(reszek) - 1))
                               for k, r in enumerate(reszek)))
    return ' '.join(szavak), nyom


# --- STEP-átíró ------------------------------------------------------------
def step(atiras, p):
    """STEP angolos átírás -> magyaros. A STEP nagybetűje a hangsúlyt jelöli
    (elhagyjuk); a pont szótaghatár; az aposztróf álef/ajin (elesik)."""
    s = atiras.strip().strip('-').lower()
    if s in ('yah.weh',):
        return 'JHVH'
    szotagok = [x for x in s.split('.') if x]
    ki = []
    for szt in szotagok:
        szt = szt.replace("'", '')
        # mássalhangzó-digráfok előbb
        csere = [('sh', 'S'), ('ts', 'C'), ('tz', 'C'), ('ch', 'H'), ('kh', 'K'),
                 ('ph', 'F'), ('th', 't'), ('bh', 'v'), ('gh', 'g'), ('dh', 'd')]
        for a, b in csere:
            szt = szt.replace(a, b)
        szt = szt.replace('ei', 'É')
        # nyitott-e a szótag (magánhangzóra végződik)?
        nyilt = bool(szt) and szt[-1] in 'aeiouÉ'
        out = []
        for c in szt:
            if c == 'a':
                out.append(p['a_nyilt'] if nyilt else p['a_zart'])
            elif c == 'e':
                out.append('e' if nyilt else p['e_zart'])
            elif c == 'É':
                out.append('é')
            elif c == 'i':
                out.append(p['i'])
            elif c == 'o':
                out.append(p['o'])
            elif c == 'u':
                out.append(p['u'])
            elif c == 'S':
                out.append('s')
            elif c == 's':
                out.append(p['sz'])
            elif c == 'C':
                out.append('c')
            elif c == 'H':
                out.append(p['ch'])
            elif c == 'K':
                out.append(p['kh'])
            elif c == 'F':
                out.append('f')
            elif c == 'q':
                out.append('k')
            elif c == 'y':
                out.append('j')
            elif c == 'w':
                out.append('v')
            else:
                out.append(c)
        ki.append(''.join(out))
    szo = ''.join(ki).replace('szsz', 'ssz')
    if szo.endswith('aj') is False and (szo.endswith('ai') or szo.endswith('ái')):
        szo = szo[:-1] + 'j'                 # STEP "chai"/"'Ai" -> -aj
    # szóvégi néma h (mater): STEP "mah" -> má
    if szo.endswith('h') and len(szo) > 1 and szo[-2] in 'aáeéoó' and not szo.endswith('ch'):
        szo = szo[:-1]
    return szo


# --- Összevetés ------------------------------------------------------------
EKEZET = str.maketrans('áéíóúÁÉÍÓÚ', 'aeiouAEIOU')


def ekezet_nelkul(s):
    return s.translate(EKEZET).lower()


def hossz_nelkul(s):
    s = ekezet_nelkul(s)
    ki = []
    for c in s:
        if ki and ki[-1] == c and c not in 'aeiou':
            continue
        ki.append(c)
    return ''.join(ki).replace('ssz', 'sz')


def szintek(gepi, arany):
    return (gepi == arany, ekezet_nelkul(gepi) == ekezet_nelkul(arany),
            hossz_nelkul(gepi) == hossz_nelkul(arany))


# --- Hibaok-besorolás (melyik döntés átfordítása adná az egyezést?) -------
HIBA_PARAM_NIQQUD = [
    ('chet', 'ḥ (ח) ch/h'), ('kaf_lagy', 'begadkefat (rafés כ ch/k)'),
    ('szamech', 'számech s/sz'), ('sin', 'sin s/sz'),
    ('dages_forte_kettoz', 'dáges forte (kettőzés)'),
    ('seva_hosszu_utan', 'sevá (néma/kiejtett)'),
    ('kamec_katan', 'kámec gádol / kátán'),
    ('szegol_jod', 'mater jod (szegol)'), ('hirek_jod', 'mater jod (hirek)'),
    ('furtiv', 'furtív patah'), ('tetragramma', 'tetragramma'),
]


def hibaok_niqqud(alak, p, arany):
    okok = []
    for kulcs, nev in HIBA_PARAM_NIQQUD:
        for ertek in PARAM_TER_NIQQUD[kulcs]:
            if ertek == p[kulcs]:
                continue
            q = dict(p)
            q[kulcs] = ertek
            if niqqud(alak, q)[0] == arany:
                okok.append(nev)
    if okok:
        return '; '.join(okok)
    g = niqqud(alak, p)[0]
    if hossz_nelkul(g) == hossz_nelkul(arany):
        return 'hosszúság (magánhangzó/kettőzés)'
    return 'egyéb (szabályon kívüli)'


def hibaok_step(atiras, p, arany):
    okok = []
    for kulcs, vals in PARAM_TER_STEP.items():
        for ertek in vals:
            if ertek == p[kulcs]:
                continue
            q = dict(p)
            q[kulcs] = ertek
            if step(atiras, q) == arany:
                okok.append(kulcs)
    g = step(atiras, p)
    if okok:
        return 'hosszúság-heurisztika/konvenció: ' + ', '.join(okok)
    if ekezet_nelkul(g) == ekezet_nelkul(arany):
        return 'hosszúság (a STEP nem jelöli)'
    if hossz_nelkul(g) == hossz_nelkul(arany):
        return 'hosszúság + kettőzés'
    return 'forrás-eltérés vagy átírási hiba'


# --- Beolvasás -------------------------------------------------------------
def tsv_sorok(ut, fejlec_kulcs):
    with open(ut, encoding='utf-8') as f:
        nyers = [l.rstrip('\n\r') for l in f]
    fej = None
    sorok = []
    for l in nyers:
        if not l or l.startswith('#'):
            continue
        if fej is None:
            if l.split('\t')[0] == fejlec_kulcs:
                fej = l.split('\t')
            continue
        r = l.split('\t')
        sorok.append(dict(zip(fej, r + [''] * (len(fej) - len(r)))))
    return sorok


def nfc(s):
    return unicodedata.normalize('NFC', s)


def tbesh_index():
    """{(strong4, lemma_nfc): step}, {strong4: [(lemma_nfc, step)]}"""
    pontos, strongonkent = {}, {}
    with open(TBESH, encoding='utf-8') as f:
        for l in f:
            r = l.rstrip('\n').split('\t')
            if len(r) < 5 or not r[0].startswith('H') or not r[0][1:5].isdigit():
                continue
            s4 = r[0][:5]
            lem = nfc(r[3])
            pontos.setdefault((s4, lem), r[4])
            pontos.setdefault(('*', lem), r[4])
            strongonkent.setdefault(s4, []).append((lem, r[4]))
    return pontos, strongonkent


def a_halmaz():
    """A 26 jóváhagyott héber sor: (strong, lemma, arany)."""
    sorok = tsv_sorok(KIVETELEK, 'nyelv')
    migr = {'qa.ra': ('H7121', None), 'shem': ('H8034', None)}
    oshl = {}
    for r in tsv_sorok(OSHL, 'strong'):
        oshl.setdefault(r['strong'], r)
    ki = []
    for r in sorok:
        if r['nyelv'] != 'heber':
            continue
        if r['alak'] in migr:
            st = migr[r['alak']][0]
            lemma = nfc(oshl[st]['lemma'])
        else:
            st = r['megjegyzes'].split('H', 1)[1][:4]
            st = 'H' + st
            lemma = nfc(r['alak'])
        ki.append({'strong': st, 'lemma': lemma, 'arany': r['kiejtes']})
    return ki


def pontozott(s):
    """Van-e magánhangzó-pont (a csak sin/sin-pontos alak mássalhangzó-átírás)."""
    return any(c in MAGANHANGZO or c in (SEVA, DAGES) for c in unicodedata.normalize('NFD', s))


def b_halmaz():
    """A régi ISTENTISZT-001 kézi lap héber párjai (egyedi szó+kiejtés)."""
    ki, kihagyott, latott = [], [], set()
    for r in tsv_sorok(TESZTKESZLET, 'nyelv'):
        if r['nyelv'] != 'heber' or r['besorolas'] not in ('arany', 'valodi'):
            continue
        szo, kiejt = nfc(r['szo']), r['kiejtes'].strip()
        kulcs = (szo, kiejt)
        if kulcs in latott:
            continue
        latott.add(kulcs)
        if not pontozott(szo):
            kihagyott.append((szo, kiejt, 'pontozatlan'))
            continue
        if any(x in kiejt for x in ('…', '+', ';', 'azaz', ',')) or '׳' in szo:
            kihagyott.append((szo, kiejt, 'kommentár/rövidítés a párban'))
            continue
        if len(szo.split()) != len(kiejt.split()):
            kihagyott.append((szo, kiejt, 'szószám-eltérés'))
            continue
        ki.append({'lemma': szo, 'arany': kiejt})
    return ki, kihagyott


# --- Kalibrálás ------------------------------------------------------------
def osszes_param(ter):
    kulcsok = list(ter)
    for ertekek in itertools.product(*(ter[k] for k in kulcsok)):
        yield dict(zip(kulcsok, ertekek))


def kalibral(elemek, fn, ter, apriori):
    """A legtöbb pontos egyezést adó paraméterkészlet; holtversenynél az
    a priorihoz legközelebbi (legkevesebb eltérő paraméter)."""
    legjobb, legjobb_kulcs = None, None
    for p in osszes_param(ter):
        talalat = sum(fn(e, p) == e['arany'] for e in elemek)
        elteres = sum(p[k] != apriori[k] for k in p)
        kulcs = (talalat, -elteres)
        if legjobb_kulcs is None or kulcs > legjobb_kulcs:
            legjobb, legjobb_kulcs = p, kulcs
    return legjobb


def keresztellenorzes(elemek, fn, ter):
    apr = a_priori(ter)
    # leave-one-out
    loo = 0
    for i, e in enumerate(elemek):
        p = kalibral(elemek[:i] + elemek[i + 1:], fn, ter, apr)
        loo += fn(e, p) == e['arany']
    # kétfelé osztás, 200 véletlen felosztás
    rnd = random.Random(20261030)
    aranyok = []
    for _ in range(200):
        idx = list(range(len(elemek)))
        rnd.shuffle(idx)
        fel = len(idx) // 2
        tan = [elemek[i] for i in idx[:fel]]
        teszt = [elemek[i] for i in idx[fel:]]
        p = kalibral(tan, fn, ter, apr)
        aranyok.append(sum(fn(e, p) == e['arany'] for e in teszt) / len(teszt))
    return loo, sum(aranyok) / len(aranyok), min(aranyok), max(aranyok)


_CACHE = {}


def fn_niqqud(e, p):
    k = ('n', e['lemma'], tuple(p.values()))
    if k not in _CACHE:
        _CACHE[k] = niqqud(e['lemma'], p)[0]
    return _CACHE[k]


def fn_step(e, p):
    if not e.get('step'):
        return ''
    k = ('s', e['step'], tuple(p.values()))
    if k not in _CACHE:
        _CACHE[k] = step(e['step'], p)
    return _CACHE[k]


# --- C halmaz: 20 ragozott TAHOT-alak az ISTENTISZT-001 helyeiről ----------
def c_halmaz():
    helyek = {}
    for r in tsv_sorok(ELOFORDULASOK, 'id'):
        if r['id'] != 'ISTENTISZT-001':
            continue
        for st in r['strong'].split('+'):
            if st.startswith('H'):
                helyek.setdefault(r['igehely'], set()).add(st)
    ki, latott = [], set()
    with open(TAHOT, encoding='utf-8') as f:
        next(f)
        for l in f:
            r = l.rstrip('\n').split('\t')
            if len(r) < 4 or r[0] not in helyek:
                continue
            alak = nfc(''.join(c for c in unicodedata.normalize('NFD', r[2])
                               if not 0x0591 <= ord(c) <= 0x05AF))
            if alak in latott or len(alak) < 2:
                continue
            latott.add(alak)
            ki.append({'igehely': r[0], 'strong': r[1], 'lemma': alak, 'step': r[3],
                       'nyers': r[2]})
    # a motívum Strongjai elöl, aztán a többi (a minta legyen vegyes)
    sajat = [e for e in ki if e['strong'] in ('H7121', 'H8034')]
    tobbi = [e for e in ki if e['strong'] not in ('H7121', 'H8034')
             and not e['strong'].startswith('H9')]
    return (sajat[:8] + tobbi[:12])[:20]


# --- STEP-proxy a nehéz esetekre: a TAHOT összes ISTENTISZT-001-versén ----
def step_proxy(p=None):
    """A niqqud-út és a STEP-átírás egyezése a mássalhangzó+magánhangzó
    vázon (ékezet és kettőzés nélkül, ch/k/h összevonva). NEM arany: a STEP
    maga is téved/következetlen; csak a nehéz esetek nagyságrendjét mutatja."""
    helyek = set()
    for r in tsv_sorok(ELOFORDULASOK, 'id'):
        if r['id'] == 'ISTENTISZT-001':
            helyek.add(r['igehely'])
    p = p or a_priori(PARAM_TER_NIQQUD)
    q = a_priori(PARAM_TER_STEP)
    ossz = egyez = 0
    elteresek = []

    def vaz(s):
        s = hossz_nelkul(s).replace('ch', 'h').replace('sz', 's')
        return s.replace('-', '')

    with open(TAHOT, encoding='utf-8') as f:
        next(f)
        for l in f:
            r = l.rstrip('\n').split('\t')
            if len(r) < 4 or r[0] not in helyek or r[1].startswith('H9'):
                continue
            st = r[3].strip().rstrip('-')
            utolso = st.rstrip('.').split('.')[-1].lower()
            if st.endswith('.') or not any(c in 'aeiou' for c in utolso):
                continue  # morféma-csonk (a STEP a toldalékot külön sorba vágja)
            if st.lower().startswith('i.y'):
                st = st[2:]  # STEP vajjiqtol-jelölés: a kettőzött jod "i." előtagja
            g = niqqud(r[2], p)[0]
            s = step(st, q)
            ossz += 1
            if vaz(g) == vaz(s):
                egyez += 1
            else:
                elteresek.append((r[0], nfc(r[2]), st, g, s))
    return ossz, egyez, elteresek


# --- Fő -------------------------------------------------------------------
def main():
    tb_pontos, tb_strong = tbesh_index()
    A = a_halmaz()
    for e in A:
        e['step'] = tb_pontos.get((e['strong'], e['lemma'])) or \
            (tb_strong.get(e['strong'], [(None, '')])[0][1])
    B, B_kihagyott = b_halmaz()
    for e in B:
        if len(e['lemma'].split()) == 1:
            e['step'] = tb_pontos.get(('*', e['lemma']), '')
    oshl_lemma = {}
    for r in tsv_sorok(OSHL, 'strong'):
        oshl_lemma.setdefault(nfc(r['lemma']), r)
    oshl_szab = oshl_gep.szabalytabla_betolt()

    sorok_ki = []
    out = []
    pn_apr = a_priori(PARAM_TER_NIQQUD)
    ps_apr = a_priori(PARAM_TER_STEP)
    pn_kal = kalibral(A, fn_niqqud, PARAM_TER_NIQQUD, pn_apr)
    ps_kal = kalibral(A, fn_step, PARAM_TER_STEP, ps_apr)

    def eredmeny(nev, elemek, fn, p):
        s = [szintek(fn(e, p), e['arany']) for e in elemek]
        return (nev, sum(x[0] for x in s), sum(x[1] for x in s), sum(x[2] for x in s), len(elemek))

    ossz = []
    ossz.append(eredmeny('A / NIQQUD / a priori', A, fn_niqqud, pn_apr))
    ossz.append(eredmeny('A / NIQQUD / kalibrált (mind a 26-on)', A, fn_niqqud, pn_kal))
    ossz.append(eredmeny('A / STEP / a priori', A, fn_step, ps_apr))
    ossz.append(eredmeny('A / STEP / kalibrált (mind a 26-on)', A, fn_step, ps_kal))
    loo_n, fel_n, fel_n_min, fel_n_max = keresztellenorzes(A, fn_niqqud, PARAM_TER_NIQQUD)
    loo_s, fel_s, fel_s_min, fel_s_max = keresztellenorzes(A, fn_step, PARAM_TER_STEP)

    # B: a régi konvencióra állított (nem kalibrált!) paraméterekkel
    pn_B = dict(pn_kal)
    pn_B.update({'chet': 'h', 'kaf_lagy': 'k', 'sin': 'sz', 'szamech': 'sz'})
    ps_B = dict(ps_kal)
    ps_B.update({'ch': 'h', 'kh': 'k', 'sz': 'sz'})

    def szorend(e, p):
        """RTL-kinyerési hiba: a többszavas pároknál a héber szórend fordított
        lehet; azt a sorrendet adja, amelyben több szó egyezik (hossz nélkül)."""
        h = e['lemma'].split()
        a = e['arany'].split()
        def egyezo(hs):
            return sum(hossz_nelkul(niqqud(x, p)[0]) == hossz_nelkul(y) for x, y in zip(hs, a))
        return list(reversed(h)) if egyezo(list(reversed(h))) > egyezo(h) else h

    def b_fn_niqqud(e, p):
        if len(e['lemma'].split()) == 1:
            return niqqud(e['lemma'], p)[0]
        return ' '.join(niqqud(x, p)[0] for x in szorend(e, p))

    ossz.append(eredmeny('B / NIQQUD / régi konvenció (nem kalibrált B-n)', B, b_fn_niqqud, pn_B))
    B_step = [e for e in B if e.get('step')]
    ossz.append(eredmeny('B / STEP / régi konvenció (csak TBESH-lemmás egyszavasak)', B_step, fn_step, ps_B))
    # meglévő OSHL-gépezet a B-n (ahol a pontozott alak OSHL-lemma)
    B_oshl = []
    for e in B:
        r = oshl_lemma.get(e['lemma'])
        if r is None:
            continue
        g = oshl_gep.atir(oshl_gep.spirantize(r['lemma'], r['atiras']), oshl_szab)
        g_regi = g.replace('ch', '\x00')
        # régi konvenció: ח -> h, rafés כ -> k (a ch kétféle eredetét a lemma dönti el)
        g_regi = g_regi.replace('\x00', 'h') if CHET in unicodedata.normalize('NFD', r['lemma']) else g_regi.replace('\x00', 'k')
        B_oshl.append({'lemma': e['lemma'], 'arany': e['arany'], 'gep': g_regi, 'oshl': r['atiras']})
    s = [szintek(x['gep'], x['arany']) for x in B_oshl]
    ossz.append(('B / OSHL-gépezet (S1.7) / régi konvenció', sum(x[0] for x in s),
                 sum(x[1] for x in s), sum(x[2] for x in s), len(B_oshl)))
    # meglévő OSHL-gépezet az A-n (körkörös!)
    A_oshl_tal = 0
    oshl_by_strong = oshl_gep.oshl_index()
    hkiv = oshl_gep.heber_kivetelek_betolt()
    for e in A:
        rr = [x for x in oshl_by_strong.get(e['strong'], []) if nfc(x['lemma']) == e['lemma']] or oshl_by_strong.get(e['strong'], [])
        g = hkiv.get(e['strong']) or oshl_gep.atir(oshl_gep.spirantize(rr[0]['lemma'], rr[0]['atiras']), oshl_szab)
        e['oshl_gep'] = g
        A_oshl_tal += g == e['arany']

    # soronkénti táblázat
    fej = ['halmaz', 'strong', 'lemma', 'step_atiras', 'arany', 'gepi_niqqud',
           'pontos', 'ekezet_nelkul', 'hossz_nelkul', 'hibaok_niqqud',
           'gepi_step', 's_pontos', 's_ekezet_nelkul', 's_hossz_nelkul', 'hibaok_step',
           'loo_niqqud', 'loo_step']
    sorok_ki.append(fej)
    apr = a_priori(PARAM_TER_NIQQUD)
    aprs = a_priori(PARAM_TER_STEP)
    hibaszam_n, hibaszam_s = {}, {}
    for i, e in enumerate(A):
        g = fn_niqqud(e, pn_kal)
        sz = szintek(g, e['arany'])
        ok = '' if sz[0] else hibaok_niqqud(e['lemma'], pn_kal, e['arany'])
        if ok:
            hibaszam_n[ok] = hibaszam_n.get(ok, 0) + 1
        gs = fn_step(e, ps_kal)
        szs = szintek(gs, e['arany'])
        oks = '' if szs[0] else hibaok_step(e['step'], ps_kal, e['arany'])
        if oks:
            hibaszam_s[oks] = hibaszam_s.get(oks, 0) + 1
        maradek = A[:i] + A[i + 1:]
        loo_n_e = fn_niqqud(e, kalibral(maradek, fn_niqqud, PARAM_TER_NIQQUD, apr))
        loo_s_e = fn_step(e, kalibral(maradek, fn_step, PARAM_TER_STEP, aprs))
        sorok_ki.append(['A', e['strong'], e['lemma'], e['step'], e['arany'], g,
                         *['igen' if x else 'nem' for x in sz], ok,
                         gs, *['igen' if x else 'nem' for x in szs], oks,
                         loo_n_e, loo_s_e])
    hibaszam_b = {}
    for e in B:
        g = b_fn_niqqud(e, pn_B)
        sz = szintek(g, e['arany'])
        ok = '' if sz[0] else (hibaok_niqqud(e['lemma'], pn_B, e['arany'])
                               if len(e['lemma'].split()) == 1 else 'többszavas: ' +
                               '; '.join(hibaok_niqqud(h, pn_B, a) for h, a in
                                         zip(szorend(e, pn_B), e['arany'].split())
                                         if niqqud(h, pn_B)[0] != a))
        if ok:
            hibaszam_b[ok] = hibaszam_b.get(ok, 0) + 1
        gs = fn_step(e, ps_B) if e.get('step') else ''
        szs = szintek(gs, e['arany']) if gs else None
        sorok_ki.append(['B', '', e['lemma'], e.get('step', ''), e['arany'], g,
                         *['igen' if x else 'nem' for x in sz], ok,
                         gs, *(['igen' if x else 'nem' for x in szs] if szs else ['', '', '']),
                         '' if not szs or szs[0] else hibaok_step(e['step'], ps_B, e['arany']), '', ''])
    C = c_halmaz()
    for e in C:
        g = niqqud(e['lemma'], pn_kal)[0]
        sorok_ki.append(['C', e['strong'], e['lemma'], e['step'], '', g, '', '', '',
                         'nincs arany: ' + e['igehely'], step(e['step'], ps_kal),
                         '', '', '', '', '', ''])
    with open(KI_TSV, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# HEBER_KIEJTES_meres.py kimenete (N-F131w mérés; kísérleti, nem adat).\n')
        f.write('# scope=adat/kiejtes_kivetelek.tsv (26 heber sor) + naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv '
                '(heber arany/valodi) + konkordancia/TAHOT_kivonat.tsv (ISTENTISZT-001 helyek) '
                '| forras=naplok/HEBER_KIEJTES_meres.py | ts=2026-10-30\n')
        for s in sorok_ki:
            f.write('\t'.join(s) + '\n')

    # összesítő
    px_ossz, px_egyez, px_elt = step_proxy()
    p_pont = dict(pn_kal)
    p_pont['szokezdo_begadkefat'] = 'pont_szerint'
    px2_ossz, px2_egyez, px2_elt = step_proxy(p_pont)
    L = []
    L.append('scope=A26 + B + C20 + STEP-proxy | forras=naplok/HEBER_KIEJTES_meres.py | ts=2026-10-30')
    L.append('')
    L.append('halmaz / út / paraméterek\tpontos\tékezet nélkül\thossz nélkül\tn')
    for nev, a, b, c, n in ossz:
        L.append(f'{nev}\t{a}/{n} ({a/n:.0%})\t{b}/{n} ({b/n:.0%})\t{c}/{n} ({c/n:.0%})\t{n}')
    n = len(A)
    L.append(f'A / NIQQUD / leave-one-out\t{loo_n}/{n} ({loo_n/n:.0%})')
    L.append(f'A / NIQQUD / kétfelé osztás (200x)\tátlag {fel_n:.0%} (min {fel_n_min:.0%}, max {fel_n_max:.0%})')
    L.append(f'A / STEP / leave-one-out\t{loo_s}/{n} ({loo_s/n:.0%})')
    L.append(f'A / STEP / kétfelé osztás (200x)\tátlag {fel_s:.0%} (min {fel_s_min:.0%}, max {fel_s_max:.0%})')
    L.append(f'A / OSHL-gépezet (S1.7, körkörös: az A ennek a kimenetéből lett jóváhagyva)\t{A_oshl_tal}/{n}')
    L.append('')
    L.append('kalibrált NIQQUD-paraméterek: ' + ', '.join(f'{k}={v}' for k, v in pn_kal.items() if v != pn_apr[k]) + ' (a többi = a priori)')
    L.append('kalibrált STEP-paraméterek: ' + ', '.join(f'{k}={v}' for k, v in ps_kal.items() if v != ps_apr[k]) + ' (a többi = a priori)')
    L.append('')
    L.append('A / NIQQUD hibaokok (kalibrált): ' + repr(hibaszam_n))
    L.append('A / STEP hibaokok (kalibrált): ' + repr(hibaszam_s))
    L.append('B / NIQQUD hibaokok: ' + repr(hibaszam_b))
    L.append('B kihagyott párok: ' + repr(B_kihagyott))
    L.append('B / OSHL-gépezet eltérések: ' + repr([(x['lemma'], x['oshl'], x['gep'], x['arany']) for x in B_oshl if x['gep'] != x['arany']]))
    L.append('')
    L.append(f'STEP-proxy (ISTENTISZT-001 versek, TAHOT, nem arany): {px_egyez}/{px_ossz} ({px_egyez/max(px_ossz,1):.0%}) váz-egyezés')
    for x in px_elt[:40]:
        L.append('  ' + '\t'.join(x))
    L.append(f'STEP-proxy, szokezdo_begadkefat=pont_szerint: {px2_egyez}/{px2_ossz} ({px2_egyez/max(px2_ossz,1):.0%})')
    for x in px2_elt[:40]:
        L.append('  ' + '\t'.join(x))
    with open(KI_OSSZ, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L[:20]))


if __name__ == '__main__':
    main()
