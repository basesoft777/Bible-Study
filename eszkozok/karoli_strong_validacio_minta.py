#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V — emberi validációs minta a Károli 1908 – Strong szópárosításhoz.

Kimenetek. A repó nyilvános, ezért a válaszkulcs a validáció lezárásáig a repón kívüli letétben áll
(alapértelmezés: `~/Bible-Study-letet/`; DT-F175vh):
  * minta.tsv        — a valódi tételek a rétegjelöléssel (alapminta 300 pár, a #172 eltéréseiből a túlminta,
                       nehéz réteg 45, pár nélküli magyar szó 80, kimaradt pár 55);
  * F175V_csalik.tsv — a titkos mag és a 20 csali (elültetett hibás pár) listája;
  * ellenorzo.html   — önálló, offline ellenőrző oldal, minden tétellel (a csalikkal is), jelölés nélkül
                       (a sablon: eszkozok/karoli_strong_validacio_sablon.html); ezt kapják az ellenőrök.
A repóba csak a nyilvános lekötés kerül: `kozlemeny/data_paper/validacio/LEKOTES.md` (a három fájl SHA-256-ja és a
rétegenkénti tételszám).

Mintavétel: minden húzás (alapminta, rétegek, közös blokk, tétel-azonosítók, csalik) a letétben álló titkos
magból; a letétfájllal újrafuttatva bájtra azonos. Első előállítás: `--uj-csali` (új titkos mag).
  * Párok: a #172 gépi mérés rétegzett mintájából (`f172/minta.tsv`, rétegenként
    200 véletlen pársor a teljes keretből) vett véletlen részminta, a keret
    pársúlya szerint arányosan (`f172/keret.tsv`, legnagyobb maradék). Egy egyszerű
    véletlen minta véletlen részmintája maga is egyszerű véletlen minta a rétegből,
    ezért a 300 pár a teljes keret (598 715 pár) arányosan rétegzett mintája; a
    hozadék, hogy a vak Opus-ellenőr ítélete (`f172/itelet_par.tsv`) erre a 300
    párra már megvan. A #172 nyolc rétegéből a két Mózes-réteg a közleményben
    egy könyvcsoport (`f172/reteg_osszevont.tsv`): hét könyvcsoport.
  * Pár nélküli magyar szavak: a `adat/karoli_strong/szavak_*.tsv` `hu` oldalának
    `betoldas` állapotú szavai (a `fuggoben` nem: az kézi, nem gépi döntés), a párosítási szabály
    által eldöntött esetek nélkül (KIZART_SZABALY, `kizarasi_ok`: névelő, segédige, alanyi és tárgyi
    névmás, korrelatív „azért … hogy”; DT-F175vb),
    könyvcsoportonként a betoldás-szám arányában, 80 darab.
Előtte ellenőrzi, hogy minden mintapár a mai `parok_*.tsv`-ben és a mai
bemenetben (Károli-token, TAHOT/TAGNT-token) is ugyanaz.

Tételenként: igehely, a teljes Károli-vers, a kiemelt szó és pozíciója
(sorszám + karakterhatár), a teljes eredeti vers (TAHOT/TAGNT, Károli-kulcson,
a párosítás bemenetével azonos sorszámozással), a forrásszó, Strong-szám,
szótő, rövid jelentés (TAHOT/TAGNT), alaktani kód és szófaj (Macula, CC BY 4.0;
illesztés versen belül Strong-számmal vagy mássalhangzó-vázzal; illesztés
nélkül üres), és a vers többi párja.

Olvasás split('\\t'), írás '\\t'.join() (a csv modul tilos, CLAUDE.md).
Az `adat/karoli_strong/` és a `konkordancia/` csak olvasott.

Használat (a repó gyökeréből):
    python eszkozok/karoli_strong_validacio_minta.py
    python eszkozok/karoli_strong_validacio_minta.py --csak-html   # a meglévő minta.tsv-ből
"""

import argparse
import json
import os
import random
import re
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'karoli_strong'))
import bemenet  # noqa: E402
import pontossag_minta as pm  # noqa: E402
import tokenek  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karoli_strong_morf as morf  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = pm.GYOKER
KONK = os.path.join(GYOKER, 'konkordancia')
ADAT = pm.ADAT
KIMENET = os.path.join(GYOKER, 'kozlemeny', 'data_paper', 'validacio')
SABLON = os.path.join(GYOKER, 'eszkozok', 'karoli_strong_validacio_sablon.html')
MAG = 20261116   # a régi, nyilvános mag: az ezzel húzott (2026-11-16–17 között a repóban álló) minta érvénytelen (DT-F175vh); ma minden húzás a titkos magból jön
N_PAR = 300
N_NELKUL = 80

# a #172 nyolc rétege -> a közlemény hét könyvcsoportja
CSOPORTOK = ['OSZ_mozes', 'OSZ_tortenet', 'OSZ_koltoi', 'OSZ_profeta',
             'USZ_evangelium', 'USZ_level', 'USZ_jelenesek']


def csoport_of_reteg(rt):
    return 'OSZ_mozes' if rt.startswith('OSZ_mozes') else rt


MINTA_FEJ = ['tetel_id', 'tipus', 'reszminta', 'elteres', 'kozos', 'csoport', 'f172_reteg', 'f172_id', 'konyv', 'vers',
             'hu_vers', 'hu_sorszam', 'hu_szo', 'hu_kezdet', 'hu_veg',
             'er_nyelv', 'er_vers', 'er_sorszam', 'er_szo', 'strong', 'szoto', 'jelentes',
             'tukor', 'kiejtes', 'morf', 'szofaj', 'morf_hu', 'nem_tr', 'tobbszavas', 'tobbi_par', 'er_tokenek_json', 'parok_json']


# ---------------------------------------------------------------- segédek

def _tabla(ut):
    return pm._tabla(ut)


def legnagyobb_maradek(sulyok, n):
    """{kulcs: súly} -> {kulcs: darab}, összeg = n (Hamilton-módszer; döntetlennél a kulcs sorrendje)."""
    ossz = float(sum(sulyok.values()))
    nyers = {k: n * v / ossz for k, v in sulyok.items()}
    ki = {k: int(x) for k, x in nyers.items()}
    marad = n - sum(ki.values())
    sorrend = sorted(sulyok, key=lambda k: (-(nyers[k] - ki[k]), list(sulyok).index(k)))
    for k in sorrend[:marad]:
        ki[k] += 1
    return ki


def git_head():
    return pm.git_head()


def adat_head():
    """A felhasznált adat utolsó commitja (nem a pillanatnyi fej): a letétbe kerülő minta.tsv fejléce így csak akkor
    változik, ha az adat is, és a nyilvános lekötés (SHA-256) nem avul el egy újabb committól."""
    try:
        return subprocess.check_output(
            ['git', '-C', GYOKER, 'log', '-1', '--format=%h', '--', 'adat/karoli_strong', 'f172', 'konkordancia/Karoli_1908.tsv',
             'konkordancia/TAHOT_kivonat.tsv', 'konkordancia/TAGNT_kivonat.tsv', 'konkordancia/Strong_szotar.tsv',
             'konkordancia/Macula_gorog.tsv', 'f22'], text=True).strip()
    except Exception:  # noqa: BLE001
        return 'ismeretlen'


_HEB_JEL = re.compile('[֑-ׇ׳״‍‌͏]')


def vaz(s):
    """Héber mássalhangzó-váz / görög ékezet nélküli kisbetűs alak az illesztéshez."""
    s = _HEB_JEL.sub('', s)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = ''.join(c for c in s if c.isalpha())
    # héber végbetűk egységesítése
    s = s.translate(str.maketrans('ךםןףץ', 'כמנפצ'))
    return s.casefold()


# ---------------------------------------------------------------- források

def lex_tabla():
    """(strong, ragozott alak) -> (szótő, rövid jelentés, kiejtés), és strong -> ugyanez (tartalék)."""
    pontos, strongra = {}, {}
    for ut in (tokenek.TAHOT, tokenek.TAGNT):
        for r in tokenek._sorok(ut):
            if len(r) < 7:
                continue
            ertek = (r[4], r[5], r[3])
            pontos.setdefault((r[1], r[2]), ertek)
            strongra.setdefault(r[1], ertek)
    return pontos, strongra


def macula_versek(kell):
    """Károli-vers -> [(strong, váz, morf, szófaj, szó-azonosító)] a Macula-táblákból, csak a kért versekre.
    Görögben az N1904 és az SBLGNT sorai külön listán (kulcs: (vers, kiadás))."""
    ki = {}
    fajlok = sorted(f for f in os.listdir(KONK) if f.startswith('Macula_heber_') and f.endswith('.tsv'))
    for fn in fajlok:
        fej = None
        with open(os.path.join(KONK, fn), encoding='utf-8') as f:
            for sor in f:
                sor = sor.rstrip('\n').rstrip('\r')
                if not sor or sor.startswith('#'):
                    continue
                m = sor.split('\t')
                if fej is None:
                    fej = {k: i for i, k in enumerate(m)}
                    continue
                for v in m[fej['karoli']].split(';'):
                    v = v.strip()
                    if v in kell:
                        ki.setdefault((v, 'heb'), []).append(
                            (m[fej['strong']], vaz(m[fej['szo']]), m[fej['morf']], m[fej['szofaj']],
                             m[fej['ref']]))
    fej = None
    with open(os.path.join(KONK, 'Macula_gorog.tsv'), encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if not sor or sor.startswith('#'):
                continue
            m = sor.split('\t')
            if fej is None:
                fej = {k: i for i, k in enumerate(m)}
                continue
            v = m[fej['karoli']].strip()
            if v in kell:
                ki.setdefault((v, m[fej['kiadas']]), []).append(
                    (m[fej['strong']], vaz(m[fej['szo']]), m[fej['morf']], m[fej['szofaj']], m[fej['ref']]))
    return ki


def illeszt(er_lista, mac_lista, ablak=6):
    """Mohó illesztés versen belül: a TAHOT/TAGNT-token a Macula-sorhoz, ha a Strong-szám vagy a váz egyezik.
    Visszaad: {sorsz: (morf, szófaj, szó-azonosító)}."""
    ki = {}
    j = 0
    for w in er_lista:
        v = vaz(w['alak'])
        for k in range(j, min(j + ablak, len(mac_lista))):
            st, mv, morf, szf, ref = mac_lista[k]
            if (st and st == w['strong']) or (v and mv == v):
                ki[w['sorsz']] = (morf, szf, ref)
                j = k + 1
                break
    return ki


# ---------------------------------------------------------------- minta

def parok_versenkent(versek):
    """vers -> [(hu_sorszam, hu_szo, er_sorszam, er_szo, strong)] a mai parok_*.tsv-ből."""
    konyvek = {}
    for v in versek:
        konyvek.setdefault(_fajlkonyv(v), set()).add(v)
    ki = {}
    for k, vs in konyvek.items():
        _, sorok = _tabla(os.path.join(ADAT, 'parok_%s.tsv' % k))
        for r in sorok:
            if r['vers'] in vs:
                ki.setdefault(r['vers'], []).append(
                    (int(r['hu_sorszam']), r['hu_szo'], int(r['er_sorszam']), r['er_szo'], r['strong']))
    return ki


_FAJLKONYV = {}


def _fajlkonyv(vers):
    """'1Móz 3:16' -> '1Moz' (a parok_/szavak_ fájlnév könyve)."""
    if not _FAJLKONYV:
        for k in pm.konyvek():
            _, sorok = _tabla(os.path.join(ADAT, 'parok_%s.tsv' % k))
            if sorok:
                _FAJLKONYV[tokenek.igehely_bont(sorok[0]['vers'])[0]] = k
    return _FAJLKONYV[tokenek.igehely_bont(vers)[0]]


def f172_elteresek():
    """A #172 vak modell-ellenőrének eltérései: azok a mintapárok, amelyeket nem talált helyesnek (helyes=0)."""
    _, sorok = _tabla(os.path.join(GYOKER, 'f172', 'itelet_par.tsv'))
    return {r['minta_id'] for r in sorok if r['helyes'] == '0'}


def par_minta(mag):
    """Az alapminta (N_PAR pár, a keret pársúlya szerint arányos részminta) és a túlminta: a #172 összes
    eltérése, amely nincs az alapmintában (DT-F175vc). Minden sor `reszminta` (alap / tulminta) és `elteres`
    (1, ha a #172 modell-ellenőre nem értett egyet a párral) mezőt kap."""
    _, keret = _tabla(os.path.join(GYOKER, 'f172', 'keret.tsv'))
    sulyok = {r['reteg']: int(r['parsor']) for r in keret if r['reteg'] in pm.RETEGEK}
    db = legnagyobb_maradek(sulyok, N_PAR)
    _, f172 = _tabla(os.path.join(GYOKER, 'f172', 'minta.tsv'))
    elteres = f172_elteresek()
    ki = []
    for rt in pm.RETEGEK:
        sorok = [r for r in f172 if r['reteg'] == rt]
        rnd = random.Random('%s:par:%s' % (mag, rt))
        for x in sorted(rnd.sample(range(len(sorok)), db[rt])):
            ki.append(dict(sorok[x], reszminta='alap', elteres='1' if sorok[x]['minta_id'] in elteres else '0'))
    alap = {r['minta_id'] for r in ki}
    for r in f172:
        if r['minta_id'] in elteres and r['minta_id'] not in alap:
            ki.append(dict(r, reszminta='tulminta', elteres='1'))
    return ki, db


# A pár nélküli szavak keretéből kizárt, a párosítási szabály (f21p/prompt_v3.md) által eldöntött esetek
# (DT-F175vb): ezeknél a „nincs megfelelője” a konvenció következménye, nem a modell ítélete, így az ember
# a konvenciót bírálná, nem az alkalmazását. Felszíni alak szerint (kis-nagybetű nélkül):
#   A  önálló névelő: a, az (az így kiszűrt, párosítatlan mutató „az” is kiesik; ismert korlát);
#   G  segédige, ha nincs külön eredeti ige (párosítatlanul): vala, volt, fog, van, volna, lészen és ragozott alakjaik
#      (a többértelmű „vagy” nem: kötőszó is);
#   F  külön kitett alanyi névmás: én, te, ő, mi, ti, ők;
#   C  tárgyi névmás eredeti megfelelő nélkül: azt, ezt, őt, őket;
#   L  korrelatív mutató névmás a „hogy” előtt: azért (ha a versben utána „hogy” áll; az „azt” a C-ben).
# A vonatkozó névmás (B) nem esik ki: ott a szabály az eredeti szerkezetétől függ, és a kimaradás valódi hiba lehet.
KIZART_SZABALY = {
    'A': {'a', 'az'},
    'G': {'vala', 'valának', 'valék', 'valál', 'valánk', 'valátok', 'volt', 'voltak', 'volna', 'volnának', 'volnék',
          'volnál', 'volnánk', 'volnátok', 'fog', 'fogok', 'fogsz', 'fogunk', 'fogtok', 'fognak', 'van', 'vannak', 'vagyok', 'vagyunk', 'vagytok',
          'lészen', 'lésznek'},
    'F': {'én', 'te', 'ő', 'mi', 'ti', 'ők'},
    'C': {'azt', 'ezt', 'őt', 'őket'},
}


def kizarasi_ok(szo, utana):
    """A pár nélküli szó kizárási oka (A/G/F/C/L), vagy None. utana: a versben utána álló tokenek (kisbetűsen)."""
    x = szo.casefold()
    for ok, alakok in KIZART_SZABALY.items():
        if x in alakok:
            return ok
    if x == 'azért' and 'hogy' in utana:
        return 'L'
    return None


def nelkul_minta(mag, szur=True):
    """A pár nélküli szavak mintája. Visszaad: (minta, darab csoportonként, keret csoportonként,
    kizárt csoportonként és okonként)."""
    jeloltek = {cs: [] for cs in CSOPORTOK}
    kizart = {cs: {} for cs in CSOPORTOK}
    for k in pm.konyvek():
        cs = pm.CSOPORT[k]
        _, sorok = _tabla(os.path.join(ADAT, 'szavak_%s.tsv' % k))
        versenkent = {}
        for r in sorok:
            if r['oldal'] == 'hu':
                versenkent.setdefault(r['vers'], []).append(r)
        for v, hu in versenkent.items():
            for i, r in enumerate(hu):
                if r['allapot'] != 'betoldas':
                    continue
                ok = kizarasi_ok(r['szo'], [y['szo'].casefold() for y in hu[i + 1:]]) if szur else None
                if ok:
                    kizart[cs][ok] = kizart[cs].get(ok, 0) + 1
                    continue
                jeloltek[cs].append({'konyv': k, 'vers': r['vers'], 'hu_sorszam': r['sorszam'],
                                     'hu_szo': r['szo'], 'csoport': cs})
    db = legnagyobb_maradek({cs: len(jeloltek[cs]) for cs in CSOPORTOK}, N_NELKUL)
    ki = []
    for cs in CSOPORTOK:
        rnd = random.Random('%s:nelkul:%s' % (mag, cs))
        for x in sorted(rnd.sample(range(len(jeloltek[cs])), db[cs])):
            ki.append(jeloltek[cs][x])
    return ki, db, {cs: len(v) for cs, v in jeloltek.items()}, kizart


N_NEHEZ = 45
N_KOZOS = 300   # a két ellenőr közös blokkja: minden ellenőrnél ez áll elöl (DT-F175ve)
N_KIMARADT = 55

# A kimaradt-pár réteg keretéből kizárt, a párosítási szabály szerint fordítatlan forrásszavak (f21p/prompt_v3.md):
#   A  névelő: H9009, G3588;  C  tárgyjelölő ʾet: H0853;  H  nyomatékos -āh, paragogikus nun: H9012, H9013;
#   I  ve-/καί (a szabály szerint fordítatlan, ha a magyarban nincs a helyén kötőszó): H9001, H9002, G2532 —
#      csak ha a versben nincs párosítatlan magyar kötőszó (KOTOSZOK); különben a keretben marad;
#   K  a [nem TR] szó (a Textus Receptusban nincs).
KOTOSZOK = {'és', 's', 'pedig', 'is', 'de', 'hogy'}   # a prompt_v3 I pontjának magyar kötőszavai
KIMARADT_KIZART_STRONG = {'H9009': 'A', 'G3588': 'A', 'H0853': 'C', 'H9012': 'H', 'H9013': 'H',
                          'H9001': 'I', 'H9002': 'I', 'G2532': 'I'}


def nehez_minta(mag, mar_benne):
    """Nehéz réteg: az 1–2Móz azon párjai, ahol a két párosító modell nem egyezett (`bizonyossag` ≠ magas);
    egyszerű véletlen minta (N_NEHEZ), a mintában már szereplő párok nélkül."""
    keret = []
    for k in ('1Moz', '2Moz'):
        _, sorok = _tabla(os.path.join(ADAT, 'parok_%s.tsv' % k))
        for r in sorok:
            if r['bizonyossag'] != 'magas' and (r['vers'], r['hu_sorszam'], r['er_sorszam']) not in mar_benne:
                keret.append(dict(r, konyv=k, reteg='OSZ_mozes', minta_id='', reszminta='nehez', elteres=''))
    rnd = random.Random('%s:nehez' % mag)
    return [keret[x] for x in sorted(rnd.sample(range(len(keret)), N_NEHEZ))], len(keret)


def kimaradt_minta(mag, ered):
    """Kimaradt-pár réteg: a `forditatlan` forrásszavak a szabály szerinti esetek nélkül, könyvcsoportonként a
    keret arányában (N_KIMARADT). Visszaad: (minta, darab csoportonként, keret csoportonként, kizárt okonként)."""
    jeloltek = {cs: [] for cs in CSOPORTOK}
    kizart = {}
    for k in pm.konyvek():
        cs = pm.CSOPORT[k]
        _, sorok = _tabla(os.path.join(ADAT, 'szavak_%s.tsv' % k))
        # az I-szabály (ve-/καί fordítatlan) csak akkor dönt, ha a magyarban nincs a helyén kötőszó: ha a versben
        # párosítatlan magyar kötőszó áll, a fordítatlan ve-/καί lehet kimaradt pár, tehát a keretben marad
        kotoszos = {r['vers'] for r in sorok
                    if r['oldal'] == 'hu' and r['allapot'] == 'betoldas' and r['szo'].casefold() in KOTOSZOK}
        for r in sorok:
            if r['oldal'] != 'er' or r['allapot'] != 'forditatlan':
                continue
            ok = KIMARADT_KIZART_STRONG.get(r['strong'])
            if ok == 'I' and r['vers'] in kotoszos:
                ok = None
            if not ok:
                lista = ered.get(r['vers']) or []
                n = int(r['sorszam'])
                if 1 <= n <= len(lista) and lista[n - 1]['nem_tr']:
                    ok = 'K'
            if ok:
                kizart[ok] = kizart.get(ok, 0) + 1
                continue
            jeloltek[cs].append({'konyv': k, 'vers': r['vers'], 'er_sorszam': r['sorszam'], 'er_szo': r['szo'],
                                 'strong': r['strong'], 'csoport': cs})
    db = legnagyobb_maradek({cs: len(jeloltek[cs]) for cs in CSOPORTOK}, N_KIMARADT)
    ki = []
    for cs in CSOPORTOK:
        rnd = random.Random('%s:kimaradt:%s' % (mag, cs))
        for x in sorted(rnd.sample(range(len(jeloltek[cs])), db[cs])):
            ki.append(jeloltek[cs][x])
    return ki, db, {cs: len(v) for cs, v in jeloltek.items()}, kizart


N_CSALI = 20
IGEKOTOK = {'meg', 'el', 'ki', 'be', 'le', 'fel', 'föl', 'át', 'által', 'oda', 'ide', 'alá', 'elő', 'vissza', 'össze',
            'rá', 'reá', 'hozzá', 'utána', 'végig', 'fenn', 'benn', 'ki'}
CSALI_TARTALMI = ('főnév', 'ige', 'melléknév')   # a Strong_szotar Szófaj mezőjének eleje (a tulajdonnév nem)
LETET_ALAP = os.path.join(os.path.expanduser('~'), 'Bible-Study-letet', 'F175V_csalik.tsv')
LETET_FEJ = MINTA_FEJ + ['csali_ok', 'eredeti_er_sorszam', 'eredeti_er_szo', 'eredeti_strong']
_SZOFAJ = {}


def tartalmi(strong):
    """Tartalmas szó-e a Strong-szám (főnév, ige, melléknév a Strong_szotar szerint; a tulajdonnév nem)."""
    if not _SZOFAJ:
        for r in tokenek._sorok(os.path.join(KONK, 'Strong_szotar.tsv')):
            if len(r) > 3:
                _SZOFAJ[r[0]] = r[3]
    return _SZOFAJ.get(strong, '').startswith(CSALI_TARTALMI)


def csali_jelolt(vp, el, rnd, tartalmi_e=None):
    """Egy vers lehetséges csalija: (h, e_eredeti, e_csali) vagy None.

    vp: a vers párjai [(hu_sorszam, hu_szo, er_sorszam, er_szo, strong)], el: az eredeti tokenek.
    Feltételek: a magyar szónak pontosan egy párja van, és az tartalmas szó; a csali egy szomszédos (±1, ±2)
    tartalmas forrásszó, más Strong-számmal, amelynek pontosan egy, másik magyar szó a párja, és az a magyar szó
    is csak ezt az egy párt kapta, és nem áll közvetlenül a vizsgált szó mellett (így a kettő nem olvasható egy
    szerkezetnek, pl. „nagy irgalmasságú”); nem rokon tő (a Strong-szám legalább 4-gyel eltér) és nincs közös
    szókezdet a két magyar szóban; a vizsgált magyar szó legalább hárombetűs, és nem igekötő. A csali
    így hihető (szomszédos tartalmas szó), de egyértelműen rossz (a mondatban egy másik magyar szó fordítja)."""
    tartalmi_e = tartalmi_e or tartalmi
    h2e, e2h = {}, {}
    for p in vp:
        h2e.setdefault(p[0], []).append(p)
        e2h.setdefault(p[2], []).append(p)
    jeloltek = []
    for h, ps in sorted(h2e.items()):
        if len(ps) != 1:
            continue
        e = ps[0][2]
        if not tartalmi_e(ps[0][4]) or len(ps[0][1]) < 3 or ps[0][1].casefold() in IGEKOTOK:
            continue
        for d in (-1, 1, -2, 2):
            e2 = e + d
            if e2 < 1 or e2 > len(el) or len(e2h.get(e2, [])) != 1:
                continue
            p2 = e2h[e2][0]
            if p2[0] == h or abs(p2[0] - h) <= 1 or len(h2e.get(p2[0], [])) != 1 or p2[1].casefold() == ps[0][1].casefold():
                continue
            s1, s2 = ps[0][4], el[e2 - 1]['strong']
            if s1 == s2 or not tartalmi_e(s2):
                continue
            # rokon tő (közeli Strong-szám, pl. H5358 ~ H5359) vagy közös szókezdet („minden” ~ „mindenkinek”):
            # a csali ilyenkor egy szerkezet tagjának látszhat, nem egyértelműen rossz
            if s1[0] == s2[0] and abs(int(s1[1:]) - int(s2[1:])) <= 3:
                continue
            if p2[1].casefold()[:4] == ps[0][1].casefold()[:4]:
                continue
            jeloltek.append((h, e, e2))
            break
    return rnd.choice(jeloltek) if jeloltek else None


def csali_minta(csali_mag, kizart_versek, ered):
    """N_CSALI csali könyvcsoportonként a keret pársúlya szerint (legnagyobb maradék); a titkos maggal
    determinisztikus. Visszaad: [(konyv, csoport, vers, h, e_eredeti, e_csali, vp)]."""
    _, keret = _tabla(os.path.join(GYOKER, 'f172', 'keret.tsv'))
    suly = {}
    for r in keret:
        if r['reteg'] in pm.RETEGEK:
            cs = csoport_of_reteg(r['reteg'])
            suly[cs] = suly.get(cs, 0) + int(r['parsor'])
    db = legnagyobb_maradek({cs: suly[cs] for cs in CSOPORTOK}, N_CSALI)
    ki = []
    for cs in CSOPORTOK:
        versek = []
        for k in pm.konyvek():
            if pm.CSOPORT[k] != cs:
                continue
            _, sorok = _tabla(os.path.join(ADAT, 'parok_%s.tsv' % k))
            vv = {}
            for r in sorok:
                vv.setdefault(r['vers'], []).append(
                    (int(r['hu_sorszam']), r['hu_szo'], int(r['er_sorszam']), r['er_szo'], r['strong']))
            versek.extend((k, v, sorted(p)) for v, p in vv.items() if v not in kizart_versek and v in ered)
        rnd = random.Random('%s:csali:%s' % (csali_mag, cs))
        rnd.shuffle(versek)
        n = 0
        for k, v, vp in versek:
            if n >= db[cs]:
                break
            j = csali_jelolt(vp, ered[v], rnd)
            if j:
                ki.append((k, cs, v, j[0], j[1], j[2], vp))
                n += 1
    return ki


def letet_olvas(ut):
    """(mag, sorok) a letétfájlból; a `# csali_mag=` sor adja a titkos magot."""
    mag = None
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            if sor.startswith('# csali_mag='):
                mag = sor.strip().split('=', 1)[1]
    _, sorok = _tabla(ut)
    return mag, sorok


def fajl_sha256(ut):
    import hashlib
    with open(ut, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def epit(mag, csali_mag=None):
    parok, db_par = par_minta(mag)
    nehez, keret_nehez = nehez_minta(mag, {(r['vers'], r['hu_sorszam'], r['er_sorszam']) for r in parok})
    parok = parok + nehez
    nelkul, db_nelkul, keret_nelkul, kizart = nelkul_minta(mag)
    # a szabály nélküli (F175.V1–V4) minta: hány tétele esett volna a kizárt esetek közé
    regi, _, _, _ = nelkul_minta(mag, szur=False)
    regi_kizart = {}
    for r in regi:
        sorok_v = [r2 for r2 in _hu_versszavak(r['konyv'], r['vers'])]
        idx = [i for i, r2 in enumerate(sorok_v) if r2['sorszam'] == r['hu_sorszam']][0]
        ok = kizarasi_ok(r['hu_szo'], [y['szo'].casefold() for y in sorok_v[idx + 1:]])
        if ok:
            regi_kizart[ok] = regi_kizart.get(ok, 0) + 1
    karoli, ered = bemenet._adatok()
    kimaradt, db_kim, keret_kim, kizart_kim = kimaradt_minta(mag, ered)
    versek = {r['vers'] for r in parok} | {r['vers'] for r in nelkul} | {r['vers'] for r in kimaradt}
    csalik = csali_minta(csali_mag, versek, ered) if csali_mag else []
    versek |= {c[2] for c in csalik}
    pv = parok_versenkent(versek)
    lex_pontos, lex_strong = lex_tabla()
    mac = macula_versek(versek)
    hibak = []

    def alap(vers, hu_s):
        szoveg = karoli[vers]
        tl = list(re.finditer(r'[^\W_]+', szoveg, re.UNICODE))
        if [m.group(0) for m in tl] != tokenek.tokenizal(szoveg):
            hibak.append('%s: a tokenizálás eltér' % vers)
        m = tl[hu_s - 1] if hu_s else None
        el = ered[vers]
        nt = vers.split(' ')[0] in _USZ_KONYVEK
        if nt:
            illesztes = {}
            for kiad in ('N1904', 'SBLGNT'):
                for s, x in illeszt(el, mac.get((vers, kiad), [])).items():
                    illesztes.setdefault(s, x)
        else:
            illesztes = illeszt(el, mac.get((vers, 'heb'), []))
        tok = []
        ar = None if nt else morf.arami_vers(vers)
        for w in el:
            il = illesztes.get(w['sorsz'])
            lx = lex_pontos.get((w['strong'], w['alak'])) or lex_strong.get(w['strong'], ('', '', ''))
            kod = il[0] if il else ''
            mh = (morf.gorog(kod) if nt else morf.heber(kod, ar)) if kod else None
            tok.append({'n': w['sorsz'], 'a': w['alak'], 's': w['strong'], 't': w['tukor'], 'k': lx[2],
                        'm': kod, 'mh': mh or '', 'w': il[2] if il else '', 'x': 1 if w['nem_tr'] else 0})
        return szoveg, m, el, illesztes, tok, nt

    tetelek = []
    for r in parok:
        v = r['vers']
        h, e = int(r['hu_sorszam']), int(r['er_sorszam'])
        szoveg, m, el, illesztes, tok, nt = alap(v, h)
        if m.group(0) != r['hu_szo']:
            hibak.append('%s hu %d: %s != %s' % (v, h, m.group(0), r['hu_szo']))
        w = el[e - 1]
        if w['alak'] != r['er_szo'] or w['strong'] != r['strong']:
            hibak.append('%s er %d: %s/%s != %s/%s' % (v, e, w['alak'], w['strong'], r['er_szo'], r['strong']))
        if (h, r['hu_szo'], e, r['er_szo'], r['strong']) not in pv.get(v, []):
            hibak.append('%s: a pár (%d→%d) nincs a mai parok-táblában' % (v, h, e))
        tetelek.append(dict(tipus='par', reszminta=r['reszminta'], elteres=r['elteres'],
                            csoport=csoport_of_reteg(r['reteg']), f172_reteg=r['reteg'],
                            f172_id=r['minta_id'], konyv=r['konyv'], vers=v, h=h, e=e, szoveg=szoveg,
                            m=m, w=w, illesztes=illesztes, tok=tok, nt=nt))
    for r in nelkul:
        v = r['vers']
        h = int(r['hu_sorszam'])
        szoveg, m, el, illesztes, tok, nt = alap(v, h)
        if m.group(0) != r['hu_szo']:
            hibak.append('%s hu %d: %s != %s' % (v, h, m.group(0), r['hu_szo']))
        if any(p[0] == h for p in pv.get(v, [])):
            hibak.append('%s hu %d: betoldasnak jelölt szónak mégis van pára' % (v, h))
        tetelek.append(dict(tipus='parnelkuli', reszminta='alap', elteres='', csoport=r['csoport'], f172_reteg='', f172_id='',
                            konyv=r['konyv'], vers=v, h=h, e=0, szoveg=szoveg, m=m, w=None,
                            illesztes=illesztes, tok=tok, nt=nt))
    for r in kimaradt:
        v = r['vers']
        e = int(r['er_sorszam'])
        szoveg, m, el, illesztes, tok, nt = alap(v, None)
        w = el[e - 1]
        if w['alak'] != r['er_szo'] or w['strong'] != r['strong']:
            hibak.append('%s er %d: %s/%s != %s/%s' % (v, e, w['alak'], w['strong'], r['er_szo'], r['strong']))
        if any(p[2] == e for p in pv.get(v, [])):
            hibak.append('%s er %d: fordítatlannak jelölt szónak mégis van pára' % (v, e))
        tetelek.append(dict(tipus='kimaradt', reszminta='kimaradt', elteres='', csoport=r['csoport'], f172_reteg='',
                            f172_id='', konyv=r['konyv'], vers=v, h=-1, e=e, szoveg=szoveg, m=None, w=w,
                            illesztes=illesztes, tok=tok, nt=nt))
    for k, cs, v, h, e0, e1, vp in csalik:
        szoveg, m, el, illesztes, tok, nt = alap(v, h)
        p0 = [p for p in vp if p[0] == h and p[2] == e0][0]
        w = el[e1 - 1]
        uj_vp = sorted([p for p in vp if p != p0] + [(h, p0[1], e1, w['alak'], w['strong'])])
        masik = [p for p in vp if p[2] == e1][0]
        ok = ('a „%s” valójában a(z) %s (%s, %d. szó) párja; a csali a szomszédos %s (%s, %d. szó), amelyet a „%s” fordít'
              % (p0[1], p0[3], p0[4], e0, w['alak'], w['strong'], e1, masik[1]))
        tetelek.append(dict(tipus='par', reszminta='csali', elteres='', csoport=cs, f172_reteg='', f172_id='',
                            konyv=k, vers=v, h=h, e=e1, szoveg=szoveg, m=m, w=w, illesztes=illesztes, tok=tok,
                            nt=nt, vp=uj_vp, csali_ok=ok, eredeti=(str(e0), p0[3], p0[4])))
    if hibak:
        print('HIBA: a minta nem vezethető le a mai adatból (%d):' % len(hibak))
        for x in hibak[:30]:
            print('  ' + x)
        raise SystemExit(1)

    # közös blokk: N_KOZOS tétel a rétegek arányában (legnagyobb maradék, rögzített mag); az oldal minden
    # ellenőrnél ezeket teszi előre, így a kappa akkor is mérhető, ha a második ítélő csak ennyit néz át.
    # A rétegjelölést az oldal nem kapja meg, és a közös blokk minden rétegből vegyesen áll.
    retegek = {}
    for i, t in enumerate(tetelek):
        if t['reszminta'] != 'csali':
            retegek.setdefault((t['tipus'], t['reszminta']), []).append(i)
    n_valodi = sum(len(v) for v in retegek.values())
    db_kozos = legnagyobb_maradek({k: len(v) for k, v in sorted(retegek.items())}, min(N_KOZOS, n_valodi))
    for k, idx in sorted(retegek.items()):
        rnd_k = random.Random('%s:kozos:%s:%s' % (mag, k[0], k[1]))
        valasztott = set(rnd_k.sample(idx, db_kozos[k]))
        for i in idx:
            tetelek[i]['kozos'] = '1' if i in valasztott else '0'
    # a csalik a közös blokkban is arányosan (a titkos maggal): mindkét ellenőr ugyanazokat kapja
    cs_idx = [i for i, t in enumerate(tetelek) if t['reszminta'] == 'csali']
    if cs_idx:
        n_kb = round(len(cs_idx) * min(N_KOZOS, n_valodi) / n_valodi)
        valasztott = set(random.Random('%s:csali:kozos' % csali_mag).sample(cs_idx, n_kb))
        for i in cs_idx:
            tetelek[i]['kozos'] = '1' if i in valasztott else '0'

    # tétel-azonosító: a csoportot és a típust nem árulja el (véletlen sorrend, rögzített mag)
    rnd = random.Random('%s:azonosito' % mag)
    sorrend = list(range(len(tetelek)))
    rnd.shuffle(sorrend)
    for uj, i in enumerate(sorrend, 1):
        tetelek[i]['tetel_id'] = 'V%03d' % uj

    sorok = []
    illesztett = 0
    for t in tetelek:
        v, h = t['vers'], t['h']
        vp = t.get('vp') or sorted(pv.get(v, []))
        tobbi = [p for p in vp if not (p[0] == h and p[2] == t['e'])]
        # ugyanahhoz a magyar szóhoz tartozó párok előre
        tobbi.sort(key=lambda p: (0 if p[0] == h else 1, p[0], p[2]))
        tobbi_szoveg = '; '.join('%d %s → %d %s %s' % p for p in tobbi)
        if t['w'] is not None:
            w = t['w']
            sz, jel, _ = lex_pontos.get((w['strong'], w['alak'])) or lex_strong.get(w['strong'], ('', '', ''))
            il = t['illesztes'].get(w['sorsz'])
            if il and t['tipus'] == 'par' and t['reszminta'] == 'alap':
                illesztett += 1
            ct = t['tok'][t['e'] - 1]
            mkod, szofaj = (il[0], il[1]) if il else ('', '')
            er = [str(t['e']), w['alak'], w['strong'], sz, jel, w['tukor'], mkod, szofaj, '1' if w['nem_tr'] else '0',
                  ct['k'], ct['mh']]
        else:
            er = ['', '', '', '', '', '', '', '', '', '', '']
        er_vers = ' '.join(x['a'] for x in t['tok'])
        # többszavas megfelelés (csak párnál): 1:n = a magyar szónak több eredetije van; n:1 = a forrásszónak több
        # magyar párja; n:m = mindkettő
        tobbsz = ''
        if t['w'] is not None and t['tipus'] == 'par':
            n_er = sum(1 for p in vp if p[0] == h)
            n_hu = sum(1 for p in vp if p[2] == t['e'])
            tobbsz = {(True, True): 'n:m', (True, False): '1:n', (False, True): 'n:1'}.get((n_er > 1, n_hu > 1), '')
        sorok.append({
            'tetel_id': t['tetel_id'], 'tipus': t['tipus'], 'reszminta': t['reszminta'], 'elteres': t['elteres'],
            'kozos': t['kozos'],
            'csoport': t['csoport'],
            'f172_reteg': t['f172_reteg'], 'f172_id': t['f172_id'], 'konyv': t['konyv'], 'vers': v,
            'hu_vers': t['szoveg'], 'hu_sorszam': str(h), 'hu_szo': t['m'].group(0) if t['m'] else '',
            'hu_kezdet': str(t['m'].start()) if t['m'] else '-1', 'hu_veg': str(t['m'].end()) if t['m'] else '-1',
            'er_nyelv': 'gorog' if t['nt'] else 'heber', 'er_vers': er_vers,
            'er_sorszam': er[0], 'er_szo': er[1], 'strong': er[2], 'szoto': er[3], 'jelentes': er[4],
            'tukor': er[5], 'morf': er[6], 'szofaj': er[7], 'nem_tr': er[8], 'kiejtes': er[9], 'morf_hu': er[10],
            'tobbszavas': tobbsz,
            'tobbi_par': tobbi_szoveg,
            'er_tokenek_json': json.dumps(t['tok'], ensure_ascii=False, separators=(',', ':')),
            'parok_json': json.dumps([list(p) for p in vp], ensure_ascii=False, separators=(',', ':')),
            'csali_ok': t.get('csali_ok', ''), 'eredeti_er_sorszam': (t.get('eredeti') or ('', '', ''))[0],
            'eredeti_er_szo': (t.get('eredeti') or ('', '', ''))[1], 'eredeti_strong': (t.get('eredeti') or ('', '', ''))[2],
        })
    for s in sorok:
        for k in MINTA_FEJ:
            if '\t' in s[k] or '\n' in s[k]:
                raise SystemExit('tabulátor vagy sortörés a mezőben: %s %s' % (s['tetel_id'], k))
    sorok.sort(key=lambda s: s['tetel_id'])
    reteg_info = {'nehez': (len(nehez), keret_nehez), 'kimaradt': (db_kim, keret_kim, kizart_kim)}
    return sorok, db_par, db_nelkul, keret_nelkul, illesztett, kizart, regi_kizart, reteg_info


_HU_CACHE = {}


def _hu_versszavak(konyv, vers):
    if konyv not in _HU_CACHE:
        d = {}
        _, sorok = _tabla(os.path.join(ADAT, 'szavak_%s.tsv' % konyv))
        for r in sorok:
            if r['oldal'] == 'hu':
                d.setdefault(r['vers'], []).append(r)
        _HU_CACHE[konyv] = d
    return _HU_CACHE[konyv][vers]


_USZ_KONYVEK = None


def _usz_konyvek():
    hu = set()
    for k in pm.konyvek():
        if pm.CSOPORT[k].startswith('USZ'):
            _, sorok = _tabla(os.path.join(ADAT, 'parok_%s.tsv' % k))
            if sorok:
                hu.add(tokenek.igehely_bont(sorok[0]['vers'])[0])
    return hu


# ---------------------------------------------------------------- írás

def letet_ir(ut, csalis, csali_mag):
    """A csalik letétfájlja (a repón kívül; a validáció lezárásáig az ellenőröknek nem adható ki). Determinisztikus
    tartalom (időbélyeg nélkül), hogy az SHA-256-ja, amely a minta.tsv fejlécébe kerül, újrafuttatáskor ne változzon."""
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# LETÉT — F175.V emberi validáció: a csalik (elültetett hibás párok) listája. A validáció lezárásáig '
                'az ellenőröknek NEM adható ki; utána a letétbe kerül | előállítás: eszkozok/karoli_strong_validacio_minta.py\n')
        f.write('# csali_mag=%s\n' % csali_mag)
        f.write('\t'.join(LETET_FEJ) + '\n')
        for r in sorted(csalis, key=lambda x: x['tetel_id']):
            f.write('\t'.join(r[k] for k in LETET_FEJ) + '\n')


def minta_ir(ut, sorok, db_par, db_nelkul, keret_nelkul, head, csali_info=None):
    par_cs = {}
    for rt, n in db_par.items():
        par_cs[csoport_of_reteg(rt)] = par_cs.get(csoport_of_reteg(rt), 0) + n
    n_tul = sum(1 for r in sorok if r['reszminta'] == 'tulminta')
    n_elt = sum(1 for r in sorok if r['elteres'] == '1')
    prov = ('# MANUAL: scope=F175.V emberi validációs minta (%d szópár a #172 rétegzett mintájának arányos '
            'részmintájaként + %d szópár túlmintaként: a #172 modell-ellenőrének az alapmintán kívüli eltérései, '
            'összesen %d eltérés + %d szópár a nehéz rétegből (1–2Móz, a két párosító modell nem egyezett) + '
            '%d fordítatlannak jelölt forrásszó a szabály szerinti esetek nélkül (kimaradt-pár réteg) + %d pár nélküli magyar szó a szabály által eldöntött esetek nélkül, könyvcsoportonként arányosan; minden húzás a letétben álló titkos magból) | '
            'forras=f172/minta.tsv, f172/keret.tsv, adat/karoli_strong/parok_*.tsv, szavak_*.tsv, '
            'konkordancia/Karoli_1908.tsv, TAHOT_kivonat.tsv, TAGNT_kivonat.tsv, Macula_*.tsv @ %s | ts=git:%s | '
            'manual (determinisztikus mintavétel: eszkozok/karoli_strong_validacio_minta.py; a párok '
            'modell-kimenet, javaslat) | párok: %s | pár nélkül: %s'
            % (N_PAR, n_tul, n_elt, sum(1 for r in sorok if r['reszminta'] == 'nehez'),
               sum(1 for r in sorok if r['tipus'] == 'kimaradt'), N_NELKUL, head, head,
               ', '.join('%s %d' % (cs, par_cs[cs]) for cs in CSOPORTOK),
               ', '.join('%s %d/%d' % (cs, db_nelkul[cs], keret_nelkul[cs]) for cs in CSOPORTOK)))
    if csali_info:
        prov += (' | csali: %d tétel a repón kívüli letétben (csali_sha256=%s); az ellenőrző oldal jelölés nélkül '
                 'tartalmazza, ez a tábla nem' % csali_info)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(prov + '\n')
        f.write('\t'.join(MINTA_FEJ) + '\n')
        for s in sorok:
            f.write('\t'.join(s[k] for k in MINTA_FEJ) + '\n')
    return par_cs


def minta_olvas(ut):
    _, sorok = _tabla(ut)
    return sorok


LEKOTES = os.path.join(KIMENET, 'LEKOTES.md')


def masodik_resz(sorok):
    """A második ítélő tételei: a közös blokk és az összes alapminta-pár."""
    return [r for r in sorok if r['kozos'] == '1' or (r['tipus'] == 'par' and r['reszminta'] == 'alap')]


def lekotes_ir(letet_dir, retegszam, vegleges=False):
    """A nyilvános lekötés: a letétfájlok SHA-256-ja és a rétegenkénti tételszám (a tételek és a rétegjelölés
    nélkül). A validáció lezárása után a letétfájlok nyilvánosságra kerülnek, és ezzel ellenőrizhetők."""
    sorok = ['# Az emberi validáció letétjének lekötése', '',
             'GENERÁLT: eszkozok/karoli_strong_validacio_minta.py — kézzel szerkeszteni tilos.', '',
             ('**Állapot: VÉGLEGES** — ez a kiküldött minta.' if vegleges else
              '**Állapot: IDEIGLENES** — nem kiküldhető; a végleges húzás a gépi bírálók fagyasztott táblája után '
              'készül (`--vegleges`).'), '',
             'A minta (`minta.tsv`, a rétegjelöléssel), a csalik listája (`F175V_csalik.tsv`, a titkos maggal) és az '
             'ellenőrző oldal (`ellenorzo.html`) a validáció lezárásáig a repón kívüli letétben áll, mert a repó '
             'nyilvános. Itt csak az SHA-256-juk szerepel, előzetes lekötésként; a lezárás után a fájlok a letétbe '
             'kerülnek, és ezzel ellenőrizhetők.', '',
             '| fájl | SHA-256 |', '|---|---|']
    for fn in ('minta.tsv', 'F175V_csalik.tsv', 'ellenorzo.html', 'ellenorzo_masodik.html'):
        sorok.append('| `%s` | `%s` |' % (fn, fajl_sha256(os.path.join(letet_dir, fn))))
    sorok += ['', 'Tételszám rétegenként: ' + ', '.join('%s %d' % kv for kv in retegszam) + '.', '']
    with open(LEKOTES, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(sorok))


def lekotes_sha(fn):
    """A nyilvános lekötésben álló SHA-256 egy letétfájlra (vagy None)."""
    if not os.path.exists(LEKOTES):
        return None
    with open(LEKOTES, encoding='utf-8') as f:
        for sor in f:
            m = re.match(r'^\| `([^`]+)` \| `([0-9a-f]{64})` \|', sor)
            if m and m.group(1) == fn:
                return m.group(2)
    return None


def html_ir(sorok, cel):
    """Az ellenőrző oldal: a sablon `/*MINTA_ADAT*/null` helyére a minta JSON-ja."""
    adat = []
    for s in sorok:
        adat.append({
            'id': s['tetel_id'], 'tipus': s['tipus'], 'kb': 1 if s['kozos'] == '1' else 0, 'vers': s['vers'], 'hu': s['hu_vers'],
            'hn': int(s['hu_sorszam']), 'hk': int(s['hu_kezdet']), 'hv': int(s['hu_veg']), 'hs': s['hu_szo'],
            'nyelv': s['er_nyelv'], 'en': int(s['er_sorszam']) if s['er_sorszam'] else 0,
            'strong': s['strong'], 'szoto': s['szoto'], 'jel': s['jelentes'], 'tukor': s['tukor'],
            'morf': s['morf'], 'mh': s['morf_hu'], 'kiej': s['kiejtes'], 'ntr': s['nem_tr'] == '1', 'tsz': s['tobbszavas'],
            'tok': json.loads(s['er_tokenek_json']), 'parok': json.loads(s['parok_json']),
        })
    js = json.dumps(adat, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    with open(SABLON, encoding='utf-8') as f:
        sablon = f.read()
    if sablon.count('/*MINTA_ADAT*/null') != 1:
        raise SystemExit('a sablonban pontosan egy /*MINTA_ADAT*/null helyőrző kell')
    ki = sablon.replace('/*MINTA_ADAT*/null', js)
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    with open(cel, 'w', encoding='utf-8', newline='\n') as f:
        f.write(ki)
    return len(ki)


def main():
    global _USZ_KONYVEK
    ap = argparse.ArgumentParser()
    ap.add_argument('--csak-html', action='store_true')
    ap.add_argument('--vegleges', action='store_true',
                    help='a végleges húzás (a gépi bírálók fagyasztott táblája után); enélkül a lekötés IDEIGLENES')
    ap.add_argument('--letet', default=LETET_ALAP, help='a csalik letétfájlja (a repón kívül)')
    ap.add_argument('--uj-csali', action='store_true', help='új titkos csali-mag (csak ha még nincs letétfájl)')
    a = ap.parse_args()
    os.makedirs(KIMENET, exist_ok=True)
    minta_ut = os.path.join(os.path.dirname(a.letet), 'minta.tsv')
    if not a.csak_html:
        if os.path.exists(a.letet):
            if a.uj_csali:
                raise SystemExit('a letétfájl már létezik (%s); új csalikhoz előbb kézzel kell félretenni' % a.letet)
            csali_mag, _ = letet_olvas(a.letet)
        elif a.uj_csali:
            import secrets
            csali_mag = secrets.token_hex(16)
        else:
            raise SystemExit('nincs letétfájl (%s): a csalik titkos magja ebben áll. Első előállításhoz: --uj-csali'
                             % a.letet)
        _USZ_KONYVEK = _usz_konyvek()
        # minden húzás (alapminta, rétegek, közös blokk, azonosítók, csalik) a titkos magból: a nyilvános
        # kódból és adatból nem vezethető le, melyik tétel melyik réteg (DT-F175vh)
        osszes, db_par, db_nelkul, keret_nelkul, illesztett, kizart, regi_kizart, reteg_info = epit(csali_mag, csali_mag)
        sorok = [r for r in osszes if r['reszminta'] != 'csali']
        csalis = [r for r in osszes if r['reszminta'] == 'csali']
        letet_ir(a.letet, csalis, csali_mag)
        par_cs = minta_ir(minta_ut, sorok, db_par, db_nelkul, keret_nelkul, adat_head(), (len(csalis), fajl_sha256(a.letet)))
        print('minta: %d tétel -> %s; csali: %d -> %s (letét, a repón kívül)' % (len(sorok), minta_ut, len(csalis), a.letet))
        print('  párok: alapminta %d + túlminta %d (a #172 eltérései közül az alapmintán kívüliek; eltérés összesen %d)' % (
            N_PAR, sum(1 for r in sorok if r['reszminta'] == 'tulminta'), sum(1 for r in sorok if r['elteres'] == '1')))
        print('  az alapminta könyvcsoportonként:')
        for cs in CSOPORTOK:
            print('    %-15s %3d' % (cs, par_cs[cs]))
        print('    (#172-rétegenként: %s)' % ', '.join('%s %d' % (k, v) for k, v in db_par.items()))
        print('  pár nélküli szavak (%d, a szabály által eldöntött esetek nélküli betoldás-keretből):' % N_NELKUL)
        for cs in CSOPORTOK:
            print('    %-15s %3d / %d' % (cs, db_nelkul[cs], keret_nelkul[cs]))
        osszes = {}
        for cs in CSOPORTOK:
            for ok, n in kizart[cs].items():
                osszes[ok] = osszes.get(ok, 0) + n
        print('  a betoldás-keretből szabály szerint kizárva: %d (%s)' % (
            sum(osszes.values()), ', '.join('%s %d' % (k, osszes[k]) for k in sorted(osszes))))
        print('  a szabály nélküli 80-as mintából ennyi esett volna ki: %d (%s)' % (
            sum(regi_kizart.values()), ', '.join('%s %d' % (k, regi_kizart[k]) for k in sorted(regi_kizart))))
        n_neh, k_neh = reteg_info['nehez']
        print('  nehéz réteg (1–2Móz, a két párosító modell nem egyezett): %d / %d pár' % (n_neh, k_neh))
        db_k, keret_k, kiz_k = reteg_info['kimaradt']
        print('  kimaradt-pár réteg (fordítatlannak jelölt forrásszavak, szabály szerinti esetek nélkül): %d / %d; '
              'kizárva %d (%s)' % (sum(db_k.values()), sum(keret_k.values()), sum(kiz_k.values()),
                                   ', '.join('%s %d' % (k, kiz_k[k]) for k in sorted(kiz_k))))
        print('    könyvcsoportonként: %s' % ', '.join('%s %d/%d' % (cs, db_k[cs], keret_k[cs]) for cs in CSOPORTOK))
        print('  alaktani adat (Macula-illesztés) az alapminta párjainak forrásszavánál: %d / %d' % (illesztett, N_PAR))
        tk = [x for s in sorok for x in json.loads(s['er_tokenek_json'])]
        print('  a minta verseinek forrásszavai: %d; alaktan nélkül %d, átírás nélkül %d'
              % (len(tk), sum(1 for x in tk if not x['mh']), sum(1 for x in tk if not x['k'])))
    valodi = minta_olvas(minta_ut)
    with open(minta_ut, encoding='utf-8') as f:
        fej = f.readline()
    csalis = []
    if 'csali_sha256=' in fej:
        if not os.path.exists(a.letet):
            raise SystemExit('a minta csalit vár, de nincs letétfájl: %s' % a.letet)
        if 'csali_sha256=%s' % fajl_sha256(a.letet) not in fej:
            raise SystemExit('a letétfájl SHA-256-ja nem egyezik a minta.tsv fejlécével: %s' % a.letet)
        _, csalis = letet_olvas(a.letet)
    osszes = sorted(valodi + csalis, key=lambda r: r['tetel_id'])
    cel = os.path.join(os.path.dirname(a.letet), 'ellenorzo.html')
    meret = html_ir(osszes, cel)
    print('ellenőrző oldal: %d bájt -> %s (a repón kívül; a külső ellenőré)' % (meret, cel))
    # a második ítélő oldala: a közös blokk és az összes alapminta-pár (a kappa 300 alappáron); külön fájl, hogy a
    # külső ellenőr sorrendjéből ne derüljön ki, melyik tétel alappár
    cel2 = os.path.join(os.path.dirname(a.letet), 'ellenorzo_masodik.html')
    meret2 = html_ir(masodik_resz(osszes), cel2)
    print('a második ítélő oldala: %d bájt, %d tétel -> %s' % (meret2, len(masodik_resz(osszes)), cel2))
    retegszam = {}
    for r in valodi + csalis:
        k = {'alap': 'alapminta-pár' if r['tipus'] == 'par' else 'pár nélküli magyar szó', 'tulminta': 'túlminta',
             'nehez': 'nehéz réteg', 'kimaradt': 'kimaradt pár', 'csali': 'csali'}[r['reszminta']]
        retegszam[k] = retegszam.get(k, 0) + 1
    rend = ['alapminta-pár', 'túlminta', 'nehéz réteg', 'pár nélküli magyar szó', 'kimaradt pár', 'csali']
    lekotes_ir(os.path.dirname(a.letet), [(k, retegszam[k]) for k in rend if k in retegszam] +
               [('összesen', len(valodi) + len(csalis)), ('a második ítélő oldalán', len(masodik_resz(osszes)))],
               a.vegleges)
    print('lekötés: %s' % LEKOTES)


if __name__ == '__main__':
    main()
