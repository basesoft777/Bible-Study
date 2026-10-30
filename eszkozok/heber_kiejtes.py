"""Gépi magyaros héber kiejtés a pontozott szövegből (DT-F131y, N-F131w; 2026-10-30).

A lexikonlapon a héber szó kiejtése: a jóváhagyott kivétel (`adat/kiejtes_kivetelek.tsv`, SEMA 2.17) mindig
elsőbbséget élvez; ennek híján ez a modul adja, és a lapon „(…, gépi)” jelölés áll mellette. A szabályok a
felhasználó kalibrációjából (naplok/HEBER_KIEJTES_kalibracio*_ertekeles.md; a kísérleti előd:
naplok/HEBER_KIEJTES_meres.py `dt_f131y()`):

- R1: ס és שׂ = sz; שׁ = s.
- R2: a kámec á; o csak a kifejezett kámec kátán jelre (U+05C7), a hátef-kámecre és a kivétellistára
  (כָּל → kol, חָכְמ- → chochm-).
- R3: a sevá kiejtett (e), ha torokhang (א, ה, ע) követi.
- R4 (elutasítva, a régi szabály marad): a hosszú magánhangzó utáni sevá a meteg szerint.
- R5: szókezdő, dáges nélküli begadkefat: a tő kezdőbetűje és a כ-előtag kemény, a ב-előtag lágy (v);
  R5b: a tő kezdőbetűje előtag után is kemény (וּבֹקֵעַ → úbókéa).
- R6: a tetragramma Jahve; előtaggal kötőjellel (la-Jahve, ba-Jahve).
- R7: Jeruzsálem lexikai kivétel minden alakjával: jerúsálajim, irányjelölővel jerúsálajmá.
- R8: ח = ch.
- A teljes szóhoz: a szókezdő kötőszói וּ = ú (utána kiejtett sevá); a dáges forte kettőz; furtív patah
  a mássalhangzó elé; a szóvégi néma hé/álef és a matres lectionis nem ejtett.

Belépési pontok:
- `kiejt(alak, elotag_hossz=0, makkef=False)` -- egy pontozott szó (vagy szókapcsolat) gépi kiejtése; ''
  ha nincs pontozás (pontozatlan alakra nem generálunk).
- `teljes_szo(sorok, i)` -- a TAHOT egy versének sorai közül az i-edik tő-sor teljes szava (előtag + tő +
  toldalék; az előtag H9001-H9009, a toldalék H9010-től), az előtag betűszámával és a makkef-jelzéssel.
"""
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GEPI_JEL = 'gépi'

SEVA, HATAF_SZEGOL, HATAF_PATAH, HATAF_KAMEC = 'ְ', 'ֱ', 'ֲ', 'ֳ'
HIREK, CERE, SZEGOL, PATAH, KAMEC = 'ִ', 'ֵ', 'ֶ', 'ַ', 'ָ'
HOLAM, HOLAM_VAV, KUBBUC = 'ֹ', 'ֺ', 'ֻ'
DAGES, METEG, MAKKEF = 'ּ', 'ֽ', '־'
SIN_PONT, SZIN_PONT, KAMEC_KATAN = 'ׁ', 'ׂ', 'ׇ'
MAGANHANGZO = {HATAF_SZEGOL, HATAF_PATAH, HATAF_KAMEC, HIREK, CERE, SZEGOL,
               PATAH, KAMEC, HOLAM, HOLAM_VAV, KUBBUC, KAMEC_KATAN}
HOSSZU = {KAMEC, CERE, HOLAM, HOLAM_VAV}

ALEF, BET, GIMEL, DALET, HE, VAV, ZAJIN, CHET, TET, JOD = (
    'א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י')
KAF_V, KAF, LAMED, MEM_V, MEM, NUN_V, NUN, SZAMEH, AJIN = (
    'ך', 'כ', 'ל', 'ם', 'מ', 'ן', 'נ', 'ס', 'ע')
PE_V, PE, CADE_V, CADE, KOF, RES, SIN, TAV = (
    'ף', 'פ', 'ץ', 'צ', 'ק', 'ר', 'ש', 'ת')
TOROKHANG = {ALEF, HE, CHET, AJIN, RES}
TETRAGRAMMA = JOD + HE + VAV + HE
JERUZSALEM = JOD + RES + VAV + SIN + LAMED

ALAP_MSH = {
    ALEF: '', BET: 'b', GIMEL: 'g', DALET: 'd', HE: 'h', VAV: 'v', ZAJIN: 'z',
    CHET: 'ch', TET: 't', JOD: 'j', KAF: 'k', KAF_V: 'k', LAMED: 'l', MEM: 'm', MEM_V: 'm',
    NUN: 'n', NUN_V: 'n', SZAMEH: 'sz', AJIN: '', PE: 'p', PE_V: 'p', CADE: 'c', CADE_V: 'c',
    KOF: 'k', RES: 'r', SIN: 's', TAV: 't',
}
LAGY = {BET: 'v', KAF: 'ch', KAF_V: 'ch', PE: 'f', PE_V: 'f'}
MAGANHANGZO_KI = {
    HATAF_SZEGOL: 'e', HATAF_PATAH: 'a', HATAF_KAMEC: 'o', HIREK: 'i', CERE: 'é', SZEGOL: 'e',
    PATAH: 'a', HOLAM: 'ó', HOLAM_VAV: 'ó', KUBBUC: 'u', KAMEC_KATAN: 'o',
    'I': 'í', 'U': 'ú', 'SZJ': 'é',
}
ELOTAG_STRONGOK = {'H900%d' % i for i in range(1, 10)}


def tisztit(szo):
    """NFD; a kantilláció (U+0591-U+05AF) és az egyéb írásjel törölve, a meteg megmarad (a sevá-döntéshez)."""
    s = unicodedata.normalize('NFD', szo)
    return ''.join(c for c in s if not (0x0591 <= ord(c) <= 0x05AF or c in '׀׃ׅׄ׆׳״'))


def pontozott(alak):
    """Van-e magánhangzó-, sevá- vagy dágespont (a pontozatlan alakra nincs gépi kiejtés)."""
    return any(c in MAGANHANGZO or c in (SEVA, DAGES) for c in unicodedata.normalize('NFD', alak))


def _betuk(szo):
    ls = []
    for c in szo:
        if ALEF <= c <= TAV:
            ls.append({'b': c, 'j': set(), 'jl': []})
        elif ls and 'ְ' <= c <= 'ׇ':
            ls[-1]['j'].add(c)
            ls[-1]['jl'].append(c)
    return ls


def _betu_kezdet(szo, k):
    """A k-adik betű kezdőindexe a szóban (a jelekkel együtt vágáshoz)."""
    poz = [i for i, c in enumerate(szo) if ALEF <= c <= TAV]
    return poz[k] if k < len(poz) else len(szo)


def _szo(szo, elotag_hossz=0, makkef_utan=False):
    ls = _betuk(szo)
    if not ls:
        return ''
    massal = ''.join(b['b'] for b in ls)
    n = len(ls)
    # R6: tetragramma (előtaggal kötőjellel)
    if massal.endswith(TETRAGRAMMA):
        if n == 4:
            return 'Jahve'
        return _szo(szo[:_betu_kezdet(szo, n - 4)], min(elotag_hossz, n - 4)) + '-Jahve'
    # R7: Jeruzsálem, minden alakjával (sinnel/sinnel írt, jodos/jod nélküli, irányjelölős)
    j = massal.find(JERUZSALEM)
    if j >= 0:
        vege = 'jerúsálajmá' if massal.endswith(MEM + HE) else 'jerúsálajim'
        if j == 0:
            return vege
        elotag = _szo(szo[:_betu_kezdet(szo, j)], min(elotag_hossz, j))
        jod = ls[j]
        if not (jod['j'] & (MAGANHANGZO | {SEVA})) and elotag.endswith('i'):
            return elotag[:-1] + 'í' + vege[2:]  # a jod az előtag hirekjének hordozója (בִּירוּשָׁלִַם → bírúsálajim)
        return elotag + vege
    # 1. matres lectionis, vav-magánhangzók, kivétellista
    for i, b in enumerate(ls):
        b['mater'] = False
        b['vok'] = next((c for c in b['jl'] if c in MAGANHANGZO), None)
        b['seva'] = SEVA in b['j']
        if KAMEC in b['j'] and ((b['b'] == KAF and i + 1 == n - 1 and ls[i + 1]['b'] == LAMED) or
                                (b['b'] == CHET and i + 2 < n and ls[i + 1]['b'] in (KAF, KAF_V)
                                 and ls[i + 2]['b'] in (MEM, MEM_V))):
            b['kivetel_katan'] = True  # R2 kivétellista: כָּל, חָכְמ-
    for i, b in enumerate(ls):
        elo = ls[i - 1] if i else None
        if b['b'] == VAV and i > 0:
            if DAGES in b['j'] and b['vok'] is None and not b['seva'] and elo['vok'] is None:
                elo['vok'], elo['seva'], b['mater'] = 'U', False, True       # surek
                continue
            if b['vok'] in (HOLAM, HOLAM_VAV) and elo['vok'] is None and not elo['seva']:
                elo['vok'], b['mater'] = HOLAM, True                          # holam male
                continue
            if b['vok'] is None and not b['seva'] and elo['vok'] in (HOLAM, HOLAM_VAV):
                b['mater'] = True                                             # néma vav holam után
                continue
        if b['b'] == JOD and i > 0 and b['vok'] is None and not b['seva'] and DAGES not in b['j']:
            if elo['vok'] == HIREK:
                elo['vok'], b['mater'] = 'I', True
                continue
            if elo['vok'] == CERE:
                b['mater'] = True
                continue
            if elo['vok'] == SZEGOL:
                elo['vok'], b['mater'] = 'SZJ', True
                continue
            if elo['vok'] == KAMEC and i + 1 == n - 1 and ls[i + 1]['b'] == VAV:
                b['mater'] = True                                             # -ָיו: -áv
                continue
        if b['b'] in (HE, ALEF) and i == n - 1 and b['vok'] is None and DAGES not in b['j']:
            b['mater'] = True                                                 # szóvégi néma hé/álef
    # 2. mássalhangzók, dágesek, sevák
    ki = []
    elozo_hangzo_seva = False
    for i, b in enumerate(ls):
        if b['mater']:
            continue
        if i == 0 and b['b'] == VAV and DAGES in b['j'] and b['vok'] is None and not b['seva'] and n > 1:
            b['vok'], b['kotoszo'] = 'U', True                               # kötőszói וּ
            ki.append(('ú', None))
            continue
        k = i - 1
        while k >= 0 and ls[k]['mater']:
            k -= 1
        elozo = ls[k] if k >= 0 else None
        dages = DAGES in b['j'] and not (b['b'] == HE and i == n - 1)
        forte = dages and elozo is not None and elozo['vok'] is not None
        msh = ALAP_MSH[b['b']]
        if b['b'] == SIN:
            msh = 'sz' if SZIN_PONT in b['j'] and SIN_PONT not in b['j'] else 's'   # R1
        if b['b'] in LAGY:
            kemeny = dages
            if i == 0:
                kemeny = kemeny or not (elotag_hossz > 0 and b['b'] == BET)     # R5
            elif i == elotag_hossz and i < n - 1:
                kemeny = True                    # R5b (a szóvégi betű nem tő-kezdet: בְךָ = előtag + toldalék)
            if not kemeny:
                msh = LAGY[b['b']]
        if b['b'] == HE and i == n - 1 and DAGES in b['j']:
            msh = 'h'                                                            # mappik
        if forte and msh and b['b'] not in TOROKHANG:
            if len(msh) == 1 or msh == 'sz':
                msh = msh[0] + msh                                               # kettőzés (ss, ssz, cc; a ch nem)
        vok = b['vok']
        hangzo_seva = False
        if b['seva'] and vok is None:
            if i == 0:
                hangzo_seva = True
            elif i == n - 1:
                hangzo_seva = False
            elif ls[i + 1]['b'] in (ALEF, HE, AJIN) and not ls[i + 1]['mater']:
                hangzo_seva = True                                               # R3
            elif forte or (elozo is not None and elozo.get('kotoszo')):
                hangzo_seva = True
            elif elozo_hangzo_seva is False and elozo is not None and elozo['seva'] and elozo['vok'] is None:
                hangzo_seva = True                                               # két sevá közül a második
            elif elozo is not None and elozo['vok'] in HOSSZU | {'I', 'U'}:
                hangzo_seva = METEG in elozo['j']                                # R4 elutasítva: a meteg szerint
        b['seva_hangzo'] = hangzo_seva
        elozo_hangzo_seva = hangzo_seva if b['seva'] else None
        if (i == n - 1 and vok == PATAH and b['b'] in (CHET, AJIN, HE)
                and elozo is not None and elozo['vok'] not in (None, PATAH, KAMEC)):
            ki.append(('a', None))                                               # furtív patah
            ki.append((msh, None))
            continue
        ki.append((msh, b))
        if vok is not None:
            ki.append((vok, b))
        elif hangzo_seva:
            ki.append(('e', None))
    # 3. magánhangzók (R2: a kámec á, o csak U+05C7-re és a kivétellistára)
    szoveg = []
    for t, b in ki:
        if b is None or t not in MAGANHANGZO | {'I', 'U', 'SZJ'}:
            szoveg.append(t)
        elif t == KAMEC:
            szoveg.append('o' if KAMEC_KATAN in b['j'] or b.get('kivetel_katan') else 'á')
        else:
            szoveg.append(MAGANHANGZO_KI[t])
    return ''.join(szoveg)


def kiejt(alak, elotag_hossz=0, makkef=False):
    """Egy pontozott szó vagy szókapcsolat gépi magyaros kiejtése (DT-F131y); '' pontozatlan alakra.
    `elotag_hossz`: az első szó előtagjának betűszáma (a TAHOT H9001-H9009 sorai; R5, R5b); `makkef`: a szó
    után makkef áll (a TAHOT STEP-átírásának „-” végződése; a kiejtésen nem látszik)."""
    if not pontozott(alak):
        return ''
    szavak = []
    for si, szo in enumerate(tisztit(alak).split()):
        reszek = [r for r in szo.split(MAKKEF) if r]
        szavak.append('-'.join(_szo(r, elotag_hossz if si == 0 and k == 0 else 0, k < len(reszek) - 1)
                               for k, r in enumerate(reszek)))
    return ' '.join(s for s in szavak if s)


def teljes_szo(sorok, i):
    """(teljes_alak, elotag_hossz, makkef) a TAHOT egy versének soraiból (dict-ek, `Strong-szám`, `Ragozott alak`,
    `Kiejtés` kulccsal, a fájl sorrendjében) az i-edik (tő-)sor köré: az előtte álló előtag-sorok (H9001-H9009) és az
    utána álló toldaléksorok (H9010-től)."""
    eleje = i
    while eleje > 0 and sorok[eleje - 1]['Strong-szám'][:5] in ELOTAG_STRONGOK:
        eleje -= 1
    vege = i + 1
    while (vege < len(sorok) and sorok[vege]['Strong-szám'].startswith('H9')
           and sorok[vege]['Strong-szám'][:5] not in ELOTAG_STRONGOK):
        vege += 1
    elotag = ''.join(s['Ragozott alak'] for s in sorok[eleje:i])
    alak = ''.join(s['Ragozott alak'] for s in sorok[eleje:vege])
    makkef = sorok[vege - 1].get('Kiejtés', '').strip().endswith('-')
    return alak, len(_betuk(tisztit(elotag))), makkef
