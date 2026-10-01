#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/forditas_kapuk.py -- F28_EMELES_BRIEF.md E3: a teljes szotari
szocikk-forditasok (Thayer, BDB) gepi kapui, az fp2/kapuk.py alapjan.

Az fp2/kapuk.py a naplok/FORDITAS_P4_ellenoriz.py fuggvenyeit importalja;
ez a modul ugyanigy tesz (1-6. ellenorzes), es hozzaadja a brief harom uj
kapujat:

  idezojel   az idezojel-parok szama egyezik (forras: ASCII " / 2 + “;
             forditas: „ + » nyito jelek)
  tagolas    a jelentesszamok es betujelek (1., 2., a., b., α., I., II.)
             sorozata azonos -- enelkul a render nem tud jelentest kivagni
  torzs      (csak BDB) az igetorzs-cimkek (Qal, Niph., Pi., Pu., Hiph.,
             Hoph., Hithp. es a ritkabbak) azonos sorrendben

Eredmeny: RENDBEN | SERTES | JELZES. A SERTES kapuhiba (E4: egy
onujraproba, utana naplok/EMELES_bukottak.tsv); a JELZES (hosszarany)
nem gatol.

Konyvtarkent:

    from forditas_kapuk import kapuk_futtat
    eredmenyek = kapuk_futtat('BDB', forras, forditas, bizonytalan=[])

Parancssorbol (fajlon at):

    python eszkozok/forditas_kapuk.py --szotar BDB --forras f.txt --forditas h.txt
"""

import argparse
import importlib.util
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_spec = importlib.util.spec_from_file_location(
    'forditas_p4_ellenoriz', os.path.join(REPO, 'naplok', 'FORDITAS_P4_ellenoriz.py'))
_p4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_p4)

TERMINOLOGIA_UT = os.path.join(REPO, 'adat', 'terminologia.tsv')
KAROLI_UT = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')

GATOLO = ['1_gorog_heber', '2_versszam', '3_karoli_roviditesek', '4_formazas',
          '5_terminologia', '8_idezojel', '9_tagolas', '10_torzs', '11_konyvek']


# ---------------------------------------------------------------------------
# idezojel
# ---------------------------------------------------------------------------

def idezojel_parok_forras(szoveg):
    return szoveg.count('"') // 2 + szoveg.count('“')


def idezojel_parok_forditas(szoveg):
    return szoveg.count('„') + szoveg.count('»')


def ellenoriz_idezojel(forras, forditas):
    a, b = idezojel_parok_forras(forras), idezojel_parok_forditas(forditas)
    if a == b:
        return 'RENDBEN', '%d par' % a
    reszlet = 'forras %d par, forditas %d par' % (a, b)
    if forras.count('"') % 2:
        reszlet += ' (a forras ASCII-idezojeleinek szama paratlan: %d)' % forras.count('"')
    return 'SERTES', reszlet


# ---------------------------------------------------------------------------
# tagolas
# ---------------------------------------------------------------------------

# Tagolas-jelolok. A forras oldalon szukebb, a forditas oldalon tagabb a
# kinyeres, es a kapu RESZSOROZATOT vizsgal: a forras minden jelolojenek
# a forras sorrendjeben meg kell jelennie a forditasban. A forditas
# hozzaadhat sorszamneveket (a magyar `14. §`, `835. o.`, `VIII. kötet`,
# `1. aorisztosz` nem forrasbeli tagolas), de forrasjelolot nem hagyhat el
# es nem cserelhet fel -- a render ezekre vag.
#
#   pontozott szam:    1.  2.          (elotte szokoz/sorkezdet/—/( , utana szokoz)
#   pont nelkuli szam: 3 proclaim      (BDB; elotte `. `, `; `, `: `, `— `, `) `,
#                                       utana kisbetus szo, de nem nyelvtani cimke)
#   betujel:           a.  b.          (a-i; elotte szokoz; nem `i. e.`, `e. g.`,
#                                       nem `c. 100` = circa)
#   romai:             I.  II.         (nem `A. V.` / `R. V.`)
#   zarojeles:         (1) (α) (I)

_PONT_SZAM = re.compile(r'(?:(?<=^)|(?<=[\s(—]))(\d{1,2})\.(?=\s)')
_SZAM_PONT_NELKUL = re.compile(r'(?<=[.;:—)] )(\d{1,2})(?= ([a-zá-ű]\w*))')
# a forditas oldalan a jelolo utan nagybetus szo is allhat (`3 Izráelben`)
_SZAM_PONT_NELKUL_HU = re.compile(r'(?<=[.;:—)] )(\d{1,2})(?= ([^\W\d_]\w*))')
_BETU = re.compile(r'(?:(?<=^)|(?<=\s))([a-i])\.(?=\s)')
_ROMAI = re.compile(r'(?:(?<=^)|(?<=[\s(—]))([IVX]{1,4})\.(?=[\s,;)])')
_ZAROJELES = re.compile(r'\(([α-ω]|\d{1,2}|[IVX]{1,4})\)')

# a pont nelkuli szam utan allo nyelvtani cimkek (a forras BDB-alakjai): ezek
# nem tagolas (`3 feminine singular`, `2 accusative`)
_NYELVTANI = {'masculine', 'feminine', 'singular', 'plural', 'accusative', 'person',
              'common', 'dual', 'times', 't'}
_HIVATKOZAS_ELOTAG = re.compile(r'(?:\bp|\bpp|\bvol|\bNo|\bed|§)\.? $')


def _jelolok(szoveg, forras_oldal):
    return [j for _, j in jelolok_pozicioval(szoveg, forras_oldal)]


def tagolas_igazitas(forras, forditas):
    """A forras jeloloinek pozicioja es a forditasban megfelelo jelolo
    pozicioja (moho reszsorozat-illesztes) -- a naplo egymas melletti
    nezetehez. [(jel, forras_poz, forditas_poz | None), ...]"""
    a = jelolok_pozicioval(forras, True)
    b = jelolok_pozicioval(forditas, False)
    ki, j = [], 0
    for poz, jel in a:
        while j < len(b) and b[j][1] != jel:
            j += 1
        if j == len(b):
            ki.append((jel, poz, None))
            continue
        ki.append((jel, poz, b[j][0]))
        j += 1
    return ki


def jelolok_pozicioval(szoveg, forras_oldal):
    talalat = []  # (pozicio, jel)
    for m in _PONT_SZAM.finditer(szoveg):
        talalat.append((m.start(), m.group(1)))
    for m in (_SZAM_PONT_NELKUL if forras_oldal else _SZAM_PONT_NELKUL_HU).finditer(szoveg):
        if forras_oldal and m.group(2).lower() in _NYELVTANI:
            continue
        if forras_oldal and _HIVATKOZAS_ELOTAG.search(szoveg[max(0, m.start() - 6):m.start()]):
            continue  # p. 27 c., vol. 2 -- oldal-/kotetszam, nem tagolas
        talalat.append((m.start(), m.group(1)))
    for m in _BETU.finditer(szoveg):
        jel = m.group(1)
        utana = szoveg[m.end():m.end() + 4].lstrip()
        elotte = szoveg[max(0, m.start() - 3):m.start()]
        if jel == 'e' and (elotte.endswith('i. ') or utana.startswith('g.')):
            continue  # i. e. / e. g.
        if jel == 'i' and utana.startswith('e.'):
            continue  # i. e.
        if jel == 'g' and elotte.endswith('e. '):
            continue  # e. g. (masodik tagja)
        if jel == 'f' and re.search(r'\d\s?$', elotte):
            continue  # `273 f.` = es a kovetkezo (magyarul `k.`), nem betujel
        if jel == 'c' and utana[:1].isdigit():
            continue  # c. 100 = circa
        talalat.append((m.start(), jel))
    for m in _ROMAI.finditer(szoveg):
        elotte = szoveg[max(0, m.start() - 3):m.start()]
        if m.group(1) == 'V' and elotte in ('A. ', 'R. '):
            continue  # A. V. / R. V.
        talalat.append((m.start(), m.group(1)))
    for m in _ZAROJELES.finditer(szoveg):
        talalat.append((m.start(), '(%s)' % m.group(1)))
    return sorted(talalat)


def tagolas_sorozat(szoveg):
    """A forras tagolas-jeloloi, sorrendben."""
    return _jelolok(szoveg, forras_oldal=True)


def tagolas_sorozat_forditas(szoveg):
    return _jelolok(szoveg, forras_oldal=False)


def ellenoriz_tagolas(forras, forditas):
    a = tagolas_sorozat(forras)
    b = tagolas_sorozat_forditas(forditas)
    j = 0
    for i, jel in enumerate(a):
        while j < len(b) and b[j] != jel:
            j += 1
        if j == len(b):
            return 'SERTES', ('a forras %d jelolojebol a(z) %d. (%s) nem talalhato a forditasban a helyen; '
                              'kornyezet a forrasban: %s'
                              % (len(a), i + 1, jel, ' '.join(a[max(0, i - 3):i + 3])))
        j += 1
    return 'RENDBEN', '%d forrasjelolo (forditas %d)' % (len(a), len(b))


# ---------------------------------------------------------------------------
# torzs (BDB)
# ---------------------------------------------------------------------------

TORZS_MINTA = re.compile(
    r'(?<![A-Za-z])'
    r'(Qal|Niph(?:al)?|Pi(?:el)?|Pu(?:al)?|Hiph(?:il)?|Hoph(?:al)?|Hithp(?:a(?:el|lpel)|o(?:lel|el)|eel|ael)?'
    r'|Hithpo|Hishtaph(?:el)?|Pilp(?:el)?|Pilel|Pulal|Pol(?:el|al)?|Po(?:el|al)?|Pōʿ(?:ēl|al)|Pōl(?:ēl|al)'
    r'|Palp(?:al)?|Pealal|Tiph(?:el)?|Nithp(?:ael)?)'
    r'(?![A-Za-z])')


def torzs_sorozat(szoveg):
    return [m.group(1)[:4] for m in TORZS_MINTA.finditer(szoveg)]


def ellenoriz_torzs(forras, forditas):
    a, b = torzs_sorozat(forras), torzs_sorozat(forditas)
    if a == b:
        return 'RENDBEN', ' '.join(a)
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return 'SERTES', ('forras %d cimke, forditas %d cimke; elso elteres a %d. cimkenel: forras %s | forditas %s'
                      % (len(a), len(b), i + 1,
                         ' '.join(a[i:i + 6]) or '-', ' '.join(b[i:i + 6]) or '-'))


# ---------------------------------------------------------------------------
# osszes kapu
# ---------------------------------------------------------------------------

_KAROLI = None
_TERM = None


def _betolt():
    global _KAROLI, _TERM
    if _KAROLI is None:
        _KAROLI = {r['Magyar rövidítés'] for r in _p4.tsv_dict_sorok(KAROLI_UT)}
        _TERM = list(_p4.tsv_dict_sorok(TERMINOLOGIA_UT))
    return _KAROLI, _TERM


# A P4 4. es 5. ellenorzesenek F28-as valtozata. Ok (E4a kalibracio, H7121):
#  - a BDB a gyakorisagot `_` jellel kozli (`קָרָא_724`, `Qal_655`), a P4 4.
#    ellenorzese viszont MINDEN `_`-t Markdown-jelnek vesz -> itt csak a
#    forrasbelinel TOBB jel serules;
#  - a P4 5. ellenorzese reszlanc-egyezest keres, igy a `procl.` szoban
#    megtalalja a `cl.` roviditest -> itt az angol alak elott nem allhat betu.

def ellenoriz_formazas(forras, forditas):
    hibak = []
    for jel in '*_#':
        if forditas.count(jel) > forras.count(jel):
            hibak.append('Markdown-jel: %s (forras %d, forditas %d)'
                         % (jel, forras.count(jel), forditas.count(jel)))
    if forditas.count('(') > forras.count('('):
        hibak.append('tobb nyito zarojel a forditasban (%d) mint a forrasban (%d) -- lehetseges betoldas'
                     % (forditas.count('('), forras.count('(')))
    if not hibak:
        return 'RENDBEN', ''
    return 'SERTES', '; '.join(hibak)


def _angol_minta(angol):
    vege = r'(?![A-Za-z])' if angol[-1:].isalpha() else ''
    return re.compile(r'(?<![A-Za-z])' + re.escape(angol) + vege)


# a magyar toldalekolas tovaltozasai (lélek -> lelkét, lelked; H2416), regex-
# mintakent: a „lelk” to UTAN a fonev toldalekanak magánhangzoja all
# (lelke, lelkét, lelkünk, lelkük, lelkű ...). ELLENOR_F28 3. tetel: a puszta
# „lelk” elotag a „lelkiismeret”, „lelkész”, „lelkes”, „lelkület” szora is
# illeszkedett; ezek nem a „lélek” fonev alakjai.
HU_TOVALTOZAT = {'lélek': (r'lelk(?!es|ész|esz|ület)[eéüű]\w*',)}


def ellenoriz_terminologia(forras, forditas, terminologia, bizonytalan_lista):
    serult = []
    for t in terminologia:
        angol = t['angol']
        if not _angol_minta(angol).search(forras):
            continue
        if _p4._magyar_alak_mintaja(t['magyar']).search(forditas):
            continue
        if any(re.search(r'\b' + tov, forditas, re.IGNORECASE)
               for tov in HU_TOVALTOZAT.get(t['magyar'], ())):
            continue
        if any(angol.rstrip('.') == b.rstrip('.') for b in bizonytalan_lista):
            continue
        serult.append('%s -> %s hianyzik' % (angol, t['magyar']))
    if not serult:
        return 'RENDBEN', ''
    return 'SERTES', '; '.join(serult)


# ---------------------------------------------------------------------------
# 11. konyv-egyezes (DT24 (a) utan): az igehelyek konyvei a forras
# rovidítesebol a normalizal.py lekepezesevel (Thayer/BDB/STEPBible ->
# Karoli; apokrif -> magyar alak) szamolva egyezzenek a forditas
# konyveivel. Ok: a Jeremiás siralmai (Lam) JSir, a Sirák fia (Sir.) Sir --
# a 3. kapu ezt nem latja, mert mindket alak megengedett.
# ---------------------------------------------------------------------------

def _konyv_mintak():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import normalizal as N
    lek = {}
    for rov, _ in N.KAROLI.values():
        lek[rov] = rov
    for step, (rov, _) in N.KAROLI.items():
        lek.setdefault(step, rov)
    for alias, step in N.FORRAS_ALIAS.items():
        if step in N.KAROLI:
            lek.setdefault(alias, N.KAROLI[step][0])
    for alias, hu in N.APOKRIF_ALIAS.items():
        lek.setdefault(alias, hu)
    betu = r'A-Za-zÀ-ɏ'

    def minta(kulcsok):
        k = sorted(set(kulcsok), key=len, reverse=True)
        return re.compile(r'(?<![%s0-9])(%s)\.?\s+(?=\d{1,3}:\d)' % (betu, '|'.join(re.escape(x) for x in k)))
    return lek, minta(lek), minta(set(lek.values()))


_KONYV = None


def ellenoriz_konyvek(forras, forditas):
    global _KONYV
    if _KONYV is None:
        _KONYV = _konyv_mintak()
    lek, f_minta, h_minta = _KONYV
    from collections import Counter
    a = Counter(lek[m.group(1)] for m in f_minta.finditer(forras))
    b = Counter(m.group(1) for m in h_minta.finditer(forditas))
    if a == b:
        return 'RENDBEN', '%d konyvnevvel jelolt igehely' % sum(a.values())
    hiany = a - b
    tobb = b - a
    return 'SERTES', '; '.join(x for x in (
        'a forditasbol hianyzik: ' + ', '.join('%s×%d' % kv for kv in sorted(hiany.items())) if hiany else '',
        'a forditasban tobb: ' + ', '.join('%s×%d' % kv for kv in sorted(tobb.items())) if tobb else '') if x)


# A P4 3. ellenorzesenek F28-as valtozata: az ismeretlen "rovidites" elfogadott,
# ha a FORRASBAN is szo szerint ugyanigy all igehely elott, es nem konyvnev
# (nem kulcsa a konyv-lekepezesnek). Ok: a BDB sziglai (`Gi 20:21` =
# Ginsburg-kiadas, `Element. 2:6`) nem konyvrovidítesek. A konyvnev-hibat a
# 11. kapu fogja meg.
def ellenoriz_karoli(forras, forditas, karoli):
    global _KONYV
    if _KONYV is None:
        _KONYV = _konyv_mintak()
    lek = _KONYV[0]
    eredm, reszlet = _p4.ellenoriz_3_karoli_roviditesek(forditas, karoli)
    if eredm == 'RENDBEN':
        return eredm, reszlet
    tokenek = [t.strip() for t in reszlet.split(':', 1)[1].split(',')]
    forras_tokenek = {m.group(1) for m in _p4.KONYV_ROVIDITES_MINTA.finditer(forras)}
    maradek = [t for t in tokenek if not (t in forras_tokenek and t not in lek)]
    if not maradek:
        return 'RENDBEN', 'forrasbeli szigla igehely elott: ' + ', '.join(tokenek)
    return 'SERTES', 'ismeretlen roviditesek: ' + ', '.join(maradek)


# ---------------------------------------------------------------------------
# 12. Szentlélek / Isten Lelke (DT25 (a), JELZES): a jóváhagyott terminológia
# Szent Szellem, Isten Szelleme, a Szellem; a régi alak jelzést kap.
# ---------------------------------------------------------------------------

SZENTLELEK_MINTA = re.compile(r'Szent ?l[ée]l|Isten Lelk', re.IGNORECASE)


def ellenoriz_szentlelek(forditas):
    t = sorted({m.group(0) for m in SZENTLELEK_MINTA.finditer(forditas)})
    if not t:
        return 'RENDBEN', ''
    return 'JELZES', 'a terminológia Szent Szellem / Isten Szelleme; talált: ' + ', '.join(t)


# ---------------------------------------------------------------------------
# 13. Fejezetszám (DT25 uj feladatjelolt, JELZES): a konyvnevvel jelolt
# igehely fejezetszama nem lehet nagyobb a konyv fejezeteinel. Ok: a BDB a
# Zsoltarok `ψ` jelet nehol mas konyvnek oldotta fel (Ez 73:23, Ézs 106:9).
# Az OSZ-ben a nagyobbik a Karoli- es a heber (MT) fejezetszam kozul (Jóel 4,
# Mal 4), mert a BDB a heber szamozast koveti.
# ---------------------------------------------------------------------------

FEJEZETSZAM = {
    "1Móz": 50, "2Móz": 40, "3Móz": 27, "4Móz": 36, "5Móz": 34, "Józs": 24, "Bír": 21,
    "Ruth": 4, "1Sám": 31, "2Sám": 24, "1Kir": 22, "2Kir": 25, "1Krón": 29, "2Krón": 36,
    "Ezsd": 10, "Neh": 13, "Eszt": 10, "Jób": 42, "Zsolt": 150, "Péld": 31, "Préd": 12,
    "Én": 8, "Ézs": 66, "Jer": 52, "JSir": 5, "Ez": 48, "Dán": 12, "Hós": 14, "Jóel": 4,
    "Ámós": 9, "Abd": 1, "Jón": 4, "Mik": 7, "Náh": 3, "Hab": 3, "Sof": 3, "Hag": 2,
    "Zak": 14, "Mal": 4,
    "Mt": 28, "Mk": 16, "Luk": 24, "Ján": 21, "ApCsel": 28, "Róm": 16, "1Kor": 16,
    "2Kor": 13, "Gal": 6, "Ef": 6, "Fil": 4, "Kol": 4, "1Thessz": 5, "2Thessz": 3,
    "1Tim": 6, "2Tim": 4, "Tit": 3, "Filem": 1, "Zsid": 13, "Jak": 5, "1Pét": 5,
    "2Pét": 3, "1Ján": 5, "2Ján": 1, "3Ján": 1, "Júd": 1, "Jel": 22,
}


def ellenoriz_fejezetszam(forditas):
    rossz = []
    for m in re.finditer(r'(?<![A-Za-zÀ-ɏ0-9])(%s) (\d{1,3}):\d'
                         % '|'.join(sorted(map(re.escape, FEJEZETSZAM), key=len, reverse=True)), forditas):
        if int(m.group(2)) > FEJEZETSZAM[m.group(1)]:
            rossz.append('%s %s' % (m.group(1), m.group(2)))
    if not rossz:
        return 'RENDBEN', ''
    return 'JELZES', 'a könyv fejezetszámánál nagyobb fejezet: ' + ', '.join(sorted(set(rossz)))


def kapuk_futtat(szotar, forras, forditas, bizonytalan=()):
    """[(nev, eredmeny, reszlet), ...]"""
    karoli, term = _betolt()
    ki = [
        ('1_gorog_heber',) + _p4.ellenoriz_1_gorog_heber(forras, forditas),
        ('2_versszam',) + _p4.ellenoriz_2_versszam(forras, forditas),
        ('3_karoli_roviditesek',) + ellenoriz_karoli(forras, forditas, karoli),
        ('4_formazas',) + ellenoriz_formazas(forras, forditas),
        ('5_terminologia',) + ellenoriz_terminologia(forras, forditas, term, list(bizonytalan)),
        ('6_hosszarany',) + _p4.ellenoriz_6_hosszarany(forras, forditas),
        ('8_idezojel',) + ellenoriz_idezojel(forras, forditas),
        ('9_tagolas',) + ellenoriz_tagolas(forras, forditas),
    ]
    if szotar == 'BDB':
        ki.append(('10_torzs',) + ellenoriz_torzs(forras, forditas))
    ki.append(('11_konyvek',) + ellenoriz_konyvek(forras, forditas))
    ki.append(('12_szentlelek',) + ellenoriz_szentlelek(forditas))
    ki.append(('13_fejezetszam',) + ellenoriz_fejezetszam(forditas))
    return ki


def atment(eredmenyek):
    return all(e != 'SERTES' for n, e, _ in eredmenyek if n in GATOLO)


def main():
    ap = argparse.ArgumentParser(description='F28 E3 forditasi kapuk')
    ap.add_argument('--szotar', required=True, choices=['Thayer', 'BDB'])
    ap.add_argument('--forras', required=True)
    ap.add_argument('--forditas', required=True)
    args = ap.parse_args()
    with open(args.forras, encoding='utf-8') as fh:
        forras = fh.read()
    with open(args.forditas, encoding='utf-8') as fh:
        forditas = fh.read()
    eredm = kapuk_futtat(args.szotar, forras, forditas)
    for n, e, r in eredm:
        print('%-22s %-8s %s' % (n, e, r))
    print('ATMENT' if atment(eredm) else 'BUKOTT')
    sys.exit(0 if atment(eredm) else 1)


if __name__ == '__main__':
    main()
