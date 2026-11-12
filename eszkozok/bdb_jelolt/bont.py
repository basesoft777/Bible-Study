#!/usr/bin/env python
"""A BDB szakasztáblája (F107, 2. lépés; FELADATOK #107; DT-F107a (c) hibrid).

Forrás (DT-F107a, felhasználó, 2026-10-18):
  - szöveg és bekezdés-tagolás: konkordancia/lexikonok_nyers/DictBDB.json (közkincs, DT-F107a (i));
  - BDB-azonosító, szócikkhatár, section/remarks osztály: konkordancia/lexikonok_nyers/BDB.lexicon
    (licence tisztázatlan: csak azonosító és szerkezeti metaadat, szöveget NEM ad).

Kimenet: adat/bdb_szakaszok.tsv (séma: adat/SEMA.md, „bdb_szakaszok.tsv”). Soronként egy szakasz = a JSON
egy bekezdése (<p>, <p style="sub1"> vagy a bekezdésen kívüli szövegdarab), a szócikkhez illesztve.

Az illesztés (Strongonként, bekezdésszinten): a JSON Strong-eleme több BDB-szócikket is összefűzhet, és olyat is
tartalmazhat, amely a lexikonban nem ennek a Strongnak a címkéjével áll (pl. H1 végén BDB1, BDB2). Ezért minden
bekezdést a lexikon ÖSSZES szócikkének elejéhez mérünk (ujjlenyomat: latin szavak + héber mássalhangzó-váz, a
hivatkozások nélkül); ahol egy bekezdés egy szócikk elejével egyezik, ott új szócikk kezdődik.

Sikerfeltétel Strongonként (rögzítve a mérés előtt):
  (a) az első tartalmi bekezdés szócikk-kezdethez illeszkedik (minden bekezdés kap bdb_id-t), és
  (b) minden szegmens latin+héber szavainak lefedése a hozzárendelt lexikon-szócikkel MINDKÉT irányban >= 0,90.
  A (b) nélküli, de (a)-t teljesítő Strong `reszleges`, az (a)-t sem teljesítő `sikertelen`.

Módok:
  (alap)        a tábla írása (adat/bdb_szakaszok.tsv)
  --meres       csak az illesztési statisztika, írás nélkül
  --ellenoriz   újragenerálás memóriában és bájtos összevetés a fájllal (kilépési kód 1, ha eltér)

TSV: '\\t'.join írás, csv modul nélkül. A szöveg tabot nem tartalmaz (a tab szóközre cserélve).
"""
import argparse
import collections
import datetime
import difflib
import hashlib
import html
import json
import os
import re
import sqlite3
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_UT = os.path.join(GYOKER, 'konkordancia', 'lexikonok_nyers', 'DictBDB.json')
LEX_UT = os.path.join(GYOKER, 'konkordancia', 'lexikonok_nyers', 'BDB.lexicon')
KI_UT = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')
JSON_HASH = '5d826c580a4dd06f54a53d1e19b5e8c354aab0180e200849e3148b89f370e33d'

# A törzsnevek listája a szeletelőéből indult (eszkozok/olvaso_szerver/bdb_szelet.py TORZS, TORZS_KANON; csak olvasva).
# F185 (N106, seed-102 M223/M233 H7812 „Hithpa`lel”): a forrás félkövér törzsfejei közül a szeletelő listáján nem álló teljes
# nevek is törzsek (a korpuszon: Hithpo`lel 9, Hithpolel 7, Po`lel 8, Hothpa`al 4, Pi`lel 4, Po`lal 2, Pu`lal 2, Pol`el 2,
# Pa`lel 1, Hithpa`lel 1); a rövidítés („Hithpa.”, „Po`l.”) nem, az a hivatkozásban áll. A hosszabb név előbb áll (alternáció).
TORZS = (r"Qal|Niph`al|Pi`el|Pu`al|Hiph`il|Hoph`al|Hithpa`lel|Hithpo`lel|Hithpolel|Hothpa`al|Hithpa`el|Hithpe`el|Hithpo`el|"
         r"Hithpalpel|Pilpel|Polpal|Po`lel|Po`lal|Pol`el|Pi`lel|Pu`lal|Pa`lel|"
         r"Polel|Polal|Po`el|Po`al|Pil`el|Pul`al|Pual|Piel|Hiphil|Niphal|Hophal|Ishtaphel|Tiph`el|"
         r"Pe`al|Pa`el|Aph`el|Haph`el|Shaph`el|Ithpe`el|Ithpa`al|Ithpa`el|Ithpo`el|Hithpa`al|Pe`il|Ishtaph`al")
TORZS_KANON = {'Pual': "Pu'al", 'Piel': "Pi'el", 'Hiphil': "Hiph'il", 'Niphal': "Niph'al", 'Hophal': "Hoph'al",
               'Ishtaphel': "Ishtaph'el"}

FEJ_TOKEN = re.compile(
    r'(?P<romai>(?:VIII|VII|VI|IV|IX|III|II|V|X|I)\.)(?=\s|$)'
    r'|(?P<torzs>(?:' + TORZS + r'))\.?(?=\s|$)'
    r'|(?P<nagy>[A-H]\.)(?=\s|$)'
    # a szóköz nélküli kombinált fej („1.a.”, H7626) is két token (F107.22: a tokenizáló hibája volt)
    r'|(?P<szam>\d{1,2}\.?)(?=\s|$|[a-z]\.)'
    r'|(?P<betu>[a-z]\.)(?=\s|$)'
    r'|(?P<zaro>\((?:\d{1,2}|[a-z]|[α-ω])\))(?=\s|$)')

MINDEN_SZINT = ('resz', 'torzs', 'nagy', 'szam', 'betu', 'zaro')
# melyik szint melyiket törli (a mélyebbeket); a törzs a részt is (aranyminta 2.28: a rákövetkező törzs már a címszóé)
TOROL = {
    'romai': ('nagy', 'szam', 'betu', 'zaro'),
    'torzs': ('resz', 'nagy', 'szam', 'betu', 'zaro'),
    'nagy': ('szam', 'betu', 'zaro'),
    'szam': ('betu', 'zaro'),
    'betu': ('zaro',),
    'zaro': (),
}

FEJLEC = ['strong', 'bdb_id', 'sorszam', 'alszocikk', 'szakasz', 'resz', 'utvonal', 'jelolo', 'jel', 'gyakorisag', 'szoveg',
          'illesztes', 'forras', 'forras_hash', 'proveniencia', 'belso_fejek']
JAVITAS_UT = os.path.join(GYOKER, 'adat', 'bdb_forras_javitas.tsv')

# Az illesztési ujjlenyomatban a pe (és a pe sofit) a memmel egy vázbetű: a DictBDB.json a dagesses pét dagesses
# memként írja (0 dagesses pe, l. naplok/F107_BDB_JELOLT_SZOVEG_naplo.md 2.2); a SZÖVEG ezt nem javítja (DT-F107f).
PE_MEM = {'פ': 'מ', 'ף': 'מ'}
ROMAI_TOKEN = {'ii', 'iii', 'iv', 'vi', 'vii', 'viii', 'ix'}
VEGSO = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}

ILL_KUSZOB = 0.80     # bekezdés-eleje ↔ szócikk-eleje (az első K token)
LEFED_KUSZOB = 0.90   # szegmens ↔ szócikk szólefedés, mindkét irány
K = 12


def sha256_fajl(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def kod_hash():
    with open(os.path.abspath(__file__), 'rb') as f:
        return hashlib.sha256(f.read().replace(b'\r\n', b'\n')).hexdigest()


# ---------------------------------------------------------------- szöveg

def sima(htmltxt):
    """A _convert_bdb.py (142ad625) tisztítása, egy eltéréssel: a <sub> nem `_N` lesz, hanem kimarad
    (a gyakoriságszám a `gyakorisag` oszlopba kerül, l. bekezdes_bont)."""
    t = htmltxt
    t = re.sub(r'<a [^>]*>(.*?)</a>', r'\1', t, flags=re.S)
    t = re.sub(r'<ref0[^>]*>(.*?)</ref0>', r'\1', t, flags=re.S)
    t = re.sub(r'<font[^>]*>(.*?)</font>', r'\1', t, flags=re.S)
    t = re.sub(r'<heb>|</heb>', '', t)
    t = re.sub(r'<grk>|</grk>', '', t)
    t = re.sub(r'<sup>(.*?)</sup>', r'^\1', t, flags=re.S)
    t = re.sub(r'<sub>(.*?)</sub>', '', t, flags=re.S)
    t = re.sub(r'<i>|</i>', '', t)
    t = re.sub(r'<b>|</b>', '', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    t = t.replace('‎', '')
    t = re.sub(r'\s+', ' ', t).strip()
    return t.replace('\t', ' ')


def heber_vaz(szo):
    s = ''.join(c for c in unicodedata.normalize('NFD', szo) if 'א' <= c <= 'ת')
    return ''.join(PE_MEM.get(VEGSO.get(c, c), VEGSO.get(c, c)) for c in s)


def ujjlenyomat(htmltxt, lexikon):
    """Latin szavak (kisbetűs, >= 2 betű) és héber mássalhangzó-vázak, sorrendben; hivatkozások nélkül."""
    t = htmltxt
    if lexikon:
        t = re.sub(r'<ref [^>]*>.*?</ref>', ' ', t, flags=re.S)
    else:
        t = re.sub(r"<a href='bible:[^']*'>.*?</a>", ' ', t, flags=re.S)
    t = re.sub(r'<sub>.*?</sub>|<sup>.*?</sup>', ' ', t, flags=re.S)
    t = unicodedata.normalize('NFD', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
    ki = []
    for m in re.finditer(r'[A-Za-z]{2,}|[֐-׿]+', t):
        w = m.group(0)
        if '֐' <= w[0] <= '׿':
            v = heber_vaz(w)
            if v:
                ki.append('h:' + v)
        else:
            w = w.lower()
            if w not in ROMAI_TOKEN:
                ki.append(w)
    return ki


def lefedes(a, b):
    """a tokenjainak hányada, amely b-ben megvan: latin tokenekre sorrendben; ha a latin tokenek száma < 5
    (csonk szócikk), az összes tokenre, sorrend nélkül (a DictBDB a héber kifejezések szórendjét megfordítja)."""
    la = [x for x in a if not x.startswith('h:')]
    lb = [x for x in b if not x.startswith('h:')]
    if len(la) < 5 or len(lb) < 5:
        if not a:
            return 1.0
        cb = collections.Counter(b)
        return sum(min(n, cb[x]) for x, n in collections.Counter(a).items()) / len(a)
    a, b = la, lb
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sum(x.size for x in sm.get_matching_blocks()) / len(a)


def eleje_hasonlo(a, b):
    """Két kezdet (első K token) hasonlósága; a rövidebbhez mérve (csonk szócikk)."""
    a, b = a[:K], b[:K]
    if not a or not b:
        return 0.0
    n = min(len(a), len(b))
    if n < 2:
        return 1.0 if a[0] == b[0] else 0.0
    # sorrend nélkül (multihalmaz): a DictBDB a többszavas héber kifejezések szórendjét megfordítja
    def atfed(x, y):
        cy = collections.Counter(y)
        return sum(min(k, cy[t]) for t, k in collections.Counter(x).items()) / n
    # szimmetrikus: mindkét irányban a közös hossz (+1 token tűrés a szórend-csere határán)
    return min(atfed(a[:n], b[:n + 1]), atfed(b[:n], a[:n + 1]))


# ---------------------------------------------------------------- JSON

def json_blokkok(defhtml):
    """A def HTML-je bekezdésekre: (nyers_html, sub1). A <div> burok nélkül; a bekezdésen kívüli szöveg is blokk."""
    belso = defhtml
    if belso.startswith('<div>') and belso.endswith('</div>'):
        belso = belso[5:-6]
    ki = []
    poz, sub1 = 0, False
    for m in re.finditer(r'<p(?:\s[^>]*)?>|</p>', belso):
        darab = belso[poz:m.start()]
        if darab.strip() and sima(darab):
            ki.append((darab, sub1))
        if m.group(0) == '</p>':
            sub1 = False
        else:
            sub1 = 'sub1' in m.group(0)
        poz = m.end()
    darab = belso[poz:]
    if darab.strip() and sima(darab):
        ki.append((darab, sub1))
    # DT-F107g (a) (3): a bekezdés közepén álló valódi félkövér fej új blokkot nyit
    bontott = []
    for k, (darab, s1) in enumerate(ki):
        kovetkezo = ki[k + 1][0] if k + 1 < len(ki) else ''
        for i, resz in enumerate(kozepfej_bont(darab, kovetkezo)):
            bontott.append((resz, s1 if i == 0 else False))
    return bontott


HAMIS_FEJ_UTAN = (')', ',', ';', ']')
KOZEPFEJ_ELOTT = ('.', '—', ':', ';', ',')


def fej_valodi(tokenek, maradek_html):
    """DT-F107g (a) (1): a fej után közvetlenül „)”, „,”, „;”, „]” álló félkövér nem fej, hanem hivatkozás, amelyet a JSON
    bekezdéstörése vitt bekezdés elejére (H7121 „(compare Pu`al)”, H3615 „2 );”, H0068 „below 3 );”)."""
    return bool(tokenek) and not sima(maradek_html).startswith(HAMIS_FEJ_UTAN)


def kozepfej_bont(blokk_html, kovetkezo_html=''):
    """DT-F107g (a) (3): a blokk szétvágása a bekezdés közepén álló valódi félkövér fejeknél (M243 H1129 „— build, <b>1</b>
    (literal)”). Valódi, ha a félkövér tartalma csupa fej-token; előtte (a sima szövegben) „.”, „—”, „:”, „;” vagy „,” áll; utána
    nem „)”, „,”, „;”, „.”, „]” áll; és törzsnév után nem szám áll (hivatkozás: „compare Qal 42:10, Pi`el 38:7”). A bekezdés
    VÉGÉN álló fej (utána semmi) akkor valódi, ha a következő blokk fejjel nyit (H3615 „— <b>1</b> </p><p><b>a.</b>”; a
    BDB.lexicon ugyanitt „<b>1.</b> <br> <b>a.</b>”)."""
    _, maradek = fej_bont(blokk_html)
    kezd = len(blokk_html) - len(maradek)
    vagasok = []
    for m in re.finditer(r'<b>(.*?)</b>', blokk_html, re.S):
        if m.start() <= kezd:
            continue
        tartalom = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
        tok, rest = fej_bont('<b>' + tartalom + '</b>')
        if not tok or sima(rest):
            continue
        elotte = sima(blokk_html[:m.start()])
        utana = sima(blokk_html[m.end():])
        if not elotte.endswith(KOZEPFEJ_ELOTT) or utana.startswith(HAMIS_FEJ_UTAN + ('.',)):
            continue
        if not utana:
            ktok, kmar = fej_bont(kovetkezo_html)
            if not fej_valodi(ktok, kmar):
                continue
        if tok[-1][0] == 'torzs' and re.match(r'\d', utana):
            continue
        vagasok.append(m.start())
    if not vagasok:
        return [blokk_html]
    reszek, elozo = [], 0
    for v in vagasok:
        reszek.append(blokk_html[elozo:v])
        elozo = v
    reszek.append(blokk_html[elozo:])
    return [r for r in reszek if sima(r)]


def fej_bont(blokk_html):
    """A bekezdés elején álló félkövér szerkezeti fej(ek): (tokenek [(szint, szöveg)], maradék_html)."""
    tokenek = []
    maradek = blokk_html
    while True:
        m = re.match(r'\s*<b>(.*?)</b>', maradek, re.S)
        if not m:
            break
        tartalom = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
        poz, sajat = 0, []
        while poz < len(tartalom):
            t = FEJ_TOKEN.match(tartalom, poz)
            if not t:
                break
            sajat.append((t.lastgroup, t.group(0)))
            poz = t.end()
            while poz < len(tartalom) and tartalom[poz] == ' ':
                poz += 1
        if not sajat:
            break
        tokenek.extend(sajat)
        if poz < len(tartalom):
            # a félkövér maradéka (pl. „1. proper name”) a szöveg része
            maradek = '<b>' + tartalom[poz:] + '</b>' + maradek[m.end():]
            break
        maradek = maradek[m.end():]
    return tokenek, maradek


def gyakorisag_kivesz(maradek_html, van_fej):
    """A <sub> számok listája (a szövegből a sima() úgyis kihagyja)."""
    return [html.unescape(re.sub(r'<[^>]+>', '', s)).strip() for s in re.findall(r'<sub>(.*?)</sub>', maradek_html, re.S)]


# ---------------------------------------------------------------- lexikon

LEX_BLOKKNYITO = re.compile(r'(?:<div class="(?:point|section|remarks)">|<p>|<br\s*/?>|</div>|</p>|<hr\s*/?>)(?:\s|&emsp;)*$')


def fej_kulcs(tokenek):
    """A fej összevetési kulcsa: (szint, érték pont nélkül) sorozat."""
    return tuple((sz, v.rstrip('.')) for sz, v in tokenek)


def lexikon_fejek(torzs_html):
    """DT-F107h (a): a lexikon-szócikk félkövér fejei — (kulcs, a szövegen belül áll-e, az utána álló szöveg ujjlenyomata).
    A lexikon itt csak szerkezeti metaadat (DT-F107a (i)): hol nyit blokkot a fej, szöveget nem ad."""
    ki = []
    for m in re.finditer(r'<b>(.*?)</b>', torzs_html, re.S):
        tok, rest = fej_bont('<b>' + html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip() + '</b>')
        if not tok or sima(rest):
            continue
        elotte_html = torzs_html[max(0, m.start() - 80):m.start()]
        belso = not LEX_BLOKKNYITO.search(elotte_html)
        # a fej előtti utolsó szó a lexikonban (a hivatkozó szó: „pointed as <b>Niph`al</b>”, „compare <b>Qal</b>”)
        elozo = re.findall(r'[A-Za-z]+', html.unescape(re.sub(r'<[^>]+>', ' ', elotte_html)))
        hivatkozo = belso and bool(elozo) and elozo[-1].lower() in HIVATKOZO_SZO \
            and re.search(r'[A-Za-z]\s*$', html.unescape(re.sub(r'<[^>]+>', ' ', elotte_html))) is not None
        ki.append((fej_kulcs(tok), hivatkozo, ujjlenyomat(torzs_html[m.end():m.end() + 600], True)[:8]))
    return ki


# a lexikonban a fej előtt közvetlenül álló hivatkozó szavak (DT-F107h (a) szűkítése, F107.29: a „szövegen belül” jel
# önmagában a valódi törzsfejeket is elvetette — „— <b>Qal</b> Perfect” —, l. napló 4.8)
HIVATKOZO_SZO = {'as', 'see', 'compare', 'cf', 'read', 'like', 'than', 'under', 'also'}


def lexikon_szerint_hivatkozas(szocikk_adat, tokenek, maradek_html):
    """DT-F107h (a): a JSON blokk eleji feje hivatkozás, ha a lexikon ugyanazon szócikkében ugyanez a fej (ugyanazzal a
    követő szöveggel) a szövegen belül áll (előtte nincs <div class="point|section|remarks">, <p>, <br>). Ha a lexikonban nincs
    megfelelő hely (a követő szöveg kezdete < 0,6 hasonló), nincs bizonyíték: a fej marad. (H6440 „pointed as </p><p><b>Niph`al</b>
    to avoid”; a lexikonban „pointed as <b>Niph`al</b> to avoid”.)"""
    kulcs = fej_kulcs(tokenek)
    fp = ujjlenyomat(maradek_html, False)[:8]
    if len(fp) < 3:
        return False
    legjobb = None
    for k, belso, lfp in szocikk_adat.get('fejek', ()):
        if k != kulcs:
            continue
        p = eleje_hasonlo(fp, lfp)
        # holtversenyben a blokkot nyitó (valódi fej) előfordulás nyer (F107.29: H0430 „3”)
        if p >= 0.6 and (legjobb is None or (p, not belso) > legjobb[:2]):
            legjobb = (p, not belso, belso)
    return bool(legjobb and legjobb[2])


# F185 (N103 (2), a Thayer K2-jének megfelelője): a JSON a kereszthivatkozás vagy a zárójeles megjegyzés KÖZEPÉN tör bekezdést,
# és a hivatkozott jelölő („see 1 above”, „(compare Pi`el as Ezek 30:24)”, „(see Zech 14:7 below 3 below)”) félkövéren a következő
# bekezdés elejére kerül. Ilyenkor a bekezdés-eleji fej NEM fej (a szöveg része, az útvonal öröklődik; a sor nem vágódik, a `sorszam`
# nem változik). Négy, egymástól független jel (bármelyik elég):
#   (a) zárójel: az előző bekezdésben lezáratlan „(” áll, és ennek a bekezdésnek az eleje (120 karakteren belül) nyitás nélkül zár
#       „)”-t — a fej a zárójeles megjegyzés belsejében áll (seed-102 M002/M221 H2388, M198/M201 H3117, M004 H3588, seed-101 M184 H9004);
#   (b) „above” / „below” követi a fejet: visszautalás (H2403 „see 1 above”, N99; H1004 „2 below”, seed-101 M237);
#   (c) az előző bekezdés utaló szóval végződik („see”, „compare”, „cf.”, „read”, „reads”), és a fej egyetlen törzsnév („compare
#       Qal”, „read Hiph`il”); szám- vagy betűfejnél nem, mert ott a JSON az utaló szó tárgyát gyakran elhagyja, és a fej valódi
#       (a korpuszon: H1518 „compare | 2 transitive”, H3205 „yet see | 2 less often beget:”, H4601 „see | 3. b. father of”);
#   (d) sorrendsértés mondat közepén: az előző bekezdés betűvel végződik (nincs mondatzáró jel), és a fej egyetlen, „a”-nál későbbi,
#       a már elért alpontnál nem későbbi betű (seed-101 M154 H2471 „burnt on the altar with c. Lev 8:26”: a „c.” a c. pontra
#       utal; H6499 „— both b. and c.”). Az „a.” újrakezdés lehet (H2850 „usually a. collective”), az nem hamis.
HAMIS_UTAN_SZO = {'see', 'compare', 'cf', 'read', 'reads'}


def _nyitott_zarojel(t):
    m = 0
    for c in t:
        if c == '(':
            m += 1
        elif c == ')' and m:
            m -= 1
    return m


def _elol_zar(t, n=120):
    m = 0
    for c in t[:n]:
        if c == '(':
            m += 1
        elif c == ')':
            if m == 0:
                return True
            m -= 1
    return False


def zarojel_folytatas(elozo_sima, sima_szoveg):
    """F202.2: a bekezdés az előző bekezdés nyitva maradt zárójelét zárja (a JSON a zárójel közepén tört bekezdést)."""
    return bool(_nyitott_zarojel(elozo_sima)) and _elol_zar(sima_szoveg)


def hamis_fej_kornyezet(elozo_sima, maradek_sima, tokenek, allapot):
    """F185: a bekezdés-eleji fej a környezete szerint hivatkozás (l. fent (a)–(d)); visszaadja a jel betűjelét vagy ''."""
    if _nyitott_zarojel(elozo_sima) and _elol_zar(maradek_sima):
        return 'a'
    if re.match(r'(?:above|below)\b', maradek_sima):
        return 'b'
    w = re.findall(r'(?:^|[^A-Za-z])([A-Za-z]+)\.?$', elozo_sima)
    if w and w[0].lower() in HAMIS_UTAN_SZO and len(tokenek) == 1 and tokenek[0][0] == 'torzs':
        return 'c'
    if (len(tokenek) == 1 and tokenek[0][0] == 'betu' and allapot.get('betu')
            and re.search(r'[A-Za-z֐-׿]$', elozo_sima)
            and 'a' < tokenek[0][1].rstrip('.') <= allapot['betu']):
        return 'd'
    return ''


# F185 (seed-101 M238 H5608): a jelöletlen alcímszó a JSON-ban `sub1` nélkül is állhat — a bekezdés héber címszóval (egy-két alak,
# vesszővel) kezdődik, és utána félkövér szófaj áll („<p> סוֺפֵר סֹפֵר, <b>noun masculine</b>”); a tagolás-állapot ilyenkor is nullázódik.
ALCIMSZO_SZOFAJ = r'(?:noun|adjective|verb|proper name|adverb|preposition|particle|pronoun|conjunction|interjection)'
ALCIMSZO_NYITO = re.compile(r'^\[?[֐-׿][֐-׿־\[\] ]{0,40},?\s*' + ALCIMSZO_SZOFAJ + r'\b')


def alcimszo_nyito(blokk_html):
    t = sima(blokk_html)
    if not ALCIMSZO_NYITO.match(t):
        return False
    return re.search(r'<b>\s*' + ALCIMSZO_SZOFAJ + r'\b', blokk_html[:600]) is not None


# F185 (N103, seed-101 M184 H9004 „(see יוֺם 7h), … see <b>3b. b.</b> qualitatively”; M057 H4994 „see above <b>3b, c. c.</b>”): a
# félkövér a kereszthivatkozás jelölőjét („3b,”, „3b.”) és a valódi betűfejet együtt fogja; a valódi fej az utolsó betű, ha a
# sorrendben a várt (a következő betű, vagy szám után „a”). A `jel` a teljes félkövér marad (a szakasz szövege így nem változik).
HIVATKOZAS_FEJ = re.compile(r'^(\d{1,2}[a-z](?:[.,]\s*[a-z])*[.,]?)\s+([a-z])\.$')


HOMONIMA_NYITO = re.compile(r'^((?:VI|IV|V|I{1,3}))\.\s+\[?[\u0590-\u05ff\ufb1d-\ufb4f]')


def hivatkozas_fej(blokk_html, allapot):
    """-> (jel, betű, maradék_html) vagy None."""
    m = re.match(r'\s*<b>(.*?)</b>', blokk_html, re.S)
    if not m:
        return None
    tartalom = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
    h = HIVATKOZAS_FEJ.match(tartalom)
    if not h:
        return None
    var = chr(ord(allapot['betu']) + 1) if allapot.get('betu') else 'a'
    if h.group(2) != var:
        return None
    return tartalom, h.group(2), blokk_html[m.end():]


# ---------------------------------------------------------------- sorbelső fejek (F185, DT-F185b (a))
# A bekezdés KÖZEPÉN álló, félkövér nélküli fej (N103 (1), a Thayer K1-ének megfelelője) a sort nem vágja (a `sorszam`-ra kulcsolódó
# fordítások és a 2.31 horgonyai miatt), hanem a `belso_fejek` oszlopba kerül: `<eltolás a szoveg-ben>|<jel>|<útvonal>`, `;`-vel
# elválasztva; az útvonal a fej utáni állapot, és a következő sorok ebből az állapotból öröklődnek. A sor `utvonal`-a a sor eleji
# állapot marad. Csak a sorrendben VÁRT fej számít (a következő betű; a következő szám; az „1” csak törzsállapotban, az „a” csak
# számállapotban):
#   betű: írásjel („.;:)]”, „—”, „,”) után „x.” + szó (seed-102 M056/M194 H3452 „… elsewhere) b. without article”);
#   szám: írásjel vagy pont után „n” vagy „n.” + kisbetűs szó (H0539 „Deut 28:59. 1.carried”); vessző után csak az „1”
#         (H5066 „come near, 1 human subject”, a forrásban dőlt);
#   törzsnév: mondatvég vagy „—” után, héber alak vagy alaktani szó előtt (H0539 „see אֵמֻן. Niph`al נֶאֱמַן”);
#   hivatkozással tapadt betűfej: „3b, c. c.” (seed-101 M057 H4994; a bekezdés-eleji alak: `hivatkozas_fej`).
# Kizárva: utaló vagy rövidítő szó előtte (see, compare, cf., p., comp., ib., in, under, and, or, of, to, above, below …), betű
# után egybetűs rövidítés („a. d.”, „i. e.”), szám, „)”, „,” vagy „;”; szám után személyszám („3 masculine”), „t.”, „times”.
# A 2.31 `jelolo_hianyzik` kézi sorai (a forrásban hiányzó jelölő, DT-F107g (b)) ugyanígy, a horgony-`sorszam` sorában álló
# `forras_alak` helyén; a sor eleji jelölőhöz tartozó („</p>”-t tartalmazó) alak a sor eleji állapotot javítja (H3318 „Qal”).
BELSO_TILT_ELOTTE = {'see', 'compare', 'cf', 'p', 'pp', 'comp', 'ib', 'id', 'in', 'under', 'and', 'or', 'of', 'to', 'above',
                     'below', 'also', 'so', 'as', 'with', 'from', 'on', 'vid', 'sq', 'ff', 'l', 'c', 'e', 'i', 'v', 'vs', 'ch', 'col'}
_IRASJEL_UTAN = r'(?:(?<=[.;:)\]]\s)|(?<=—\s)|(?<=,\s))'
_SZEMELY = r'(?:masculine|feminine|common|singular|plural|pers|person|t\.|times|ed\b|st\b|nd\b|rd\b|th\b|end\b|near\b|above\b|below\b)'


def _elozo_szo(s, poz):
    m = re.search(r'([A-Za-z]+)\.?[,;:)\]]?\s*(?:—\s*)?$', s[max(0, poz - 20):poz])
    return m.group(1).lower() if m else ''


def kezi_jelolok():
    """{(strong, sorszam): [(forras_alak, javitott_alak)]} a 2.31 `jelolo_hianyzik` kézi soraiból (ha a tábla még nincs, üres)."""
    ki = collections.defaultdict(list)
    if not os.path.exists(JAVITAS_UT):
        return ki
    fej = None
    with open(JAVITAS_UT, encoding='utf-8', newline='') as f:
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            if d.get('hiba') == 'jelolo_hianyzik':
                ki[(d['strong'], d['sorszam'])].append((d['forras_alak'], d['javitott_alak']))
    return ki


def _javitott_allapot(allapot, javitott):
    r = javitott.split('/')
    torzs = r[0] if r[0] not in ('', '-') else ''
    if torzs and torzs != allapot['torzs']:
        for x in TOROL['torzs']:
            allapot[x] = ''
        allapot['torzs'] = torzs
    if len(r) > 1 and r[1] not in ('', '-'):
        for x in TOROL['szam']:
            allapot[x] = ''
        allapot['szam'] = r[1]
    if len(r) > 2 and r[2] not in ('', '-'):
        allapot['betu'] = r[2]


def belso_fejek(szoveg, allapot, kezi=()):
    """A sor szövegének sorbelső fejei sorrendben: [(eltolás, jel, útvonal)]; az `allapot`-ot helyben lépteti."""
    ki, poz = [], 0
    kezi_hely = []
    for forras_alak, javitott in kezi:
        if '</p>' in forras_alak:
            continue
        frag = html.unescape(re.sub(r'<[^>]+>', '', forras_alak))
        k = szoveg.find(frag)
        if k < 0:
            continue
        utolso = javitott.split('/')[-1]
        if re.match(r'\d', utolso):
            j = [m.start() for m in re.finditer(r'(?<!\d)%s(?!\d)' % re.escape(utolso), frag)]
        else:
            j = [m.start() for m in re.finditer(re.escape(utolso.replace("'", '`')), frag)]
        if j:
            kezi_hely.append((k + j[-1], javitott))
    while True:
        jeloltek = []
        var_b = chr(ord(allapot['betu']) + 1) if allapot['betu'] else ('a' if allapot['szam'] else '')
        var_sz = str(int(allapot['szam']) + 1) if allapot['szam'].isdigit() else ('1' if allapot['torzs'] and not allapot['szam'] else '')
        if var_b:
            for m in re.finditer(_IRASJEL_UTAN + r'(%s)[.:]\s(?=[^\d\s),;])(?!end\b|near\b|above\b|below\b)' % var_b, szoveg[poz:]):
                a = poz + m.start(1)
                if re.match(r'[a-z]\.\s', szoveg[a + 3:a + 6]) or _elozo_szo(szoveg, a) in BELSO_TILT_ELOTTE:
                    continue
                jeloltek.append((a, '%s.' % var_b, ('betu', var_b)))
                break
            for m in re.finditer(r'(?<=\s)(\d{1,2}[a-z](?:[.,]\s*[a-z])*[.,]?)\s+(%s)\.\s' % var_b, szoveg[poz:]):
                jeloltek.append((poz + m.start(1), '%s %s.' % (m.group(1), var_b), ('betu', var_b)))
                break
        if var_sz:
            for m in re.finditer(r'(?:' + _IRASJEL_UTAN + r'|(?<=\.))(%s)(?:\.\s?|\s)(?=[a-z]{2})(?!%s)' % (var_sz, _SZEMELY),
                                 szoveg[poz:]):
                a = poz + m.start(1)
                elotte = szoveg[max(0, a - 2):a]
                if elotte.endswith(', ') and var_sz != '1':
                    continue
                if elotte.endswith('.') and not re.search(r'[a-z\d)]\.$', elotte):
                    continue
                if _elozo_szo(szoveg, a) in BELSO_TILT_ELOTTE:
                    continue
                pont = szoveg[a + len(var_sz):a + len(var_sz) + 1] == '.'
                jeloltek.append((a, var_sz + ('.' if pont else ''), ('szam', var_sz)))
                break
        for m in re.finditer(r'(?:(?<=[.;]\s)|(?<=—\s))(' + TORZS + r')(?=\s+(?:[\u0590-\u05ff]|Perfect|Imperfect|Participle|'
                             r'Infinitive|Imperative))', szoveg[poz:]):
            a = poz + m.start(1)
            nev = TORZS_KANON.get(m.group(1), m.group(1)).replace('`', "'")
            if nev == allapot['torzs'] or _elozo_szo(szoveg, a) in BELSO_TILT_ELOTTE:
                continue
            jeloltek.append((a, m.group(1), ('torzs', nev)))
            break
        for a, javitott in kezi_hely:
            if a >= poz:
                jeloltek.append((a, szoveg[a:a + 12].split(' ')[0], ('kezi', javitott)))
        if not jeloltek:
            return ki
        a, jel, (szint, ertek) = min(jeloltek, key=lambda x: x[0])
        if szint == 'kezi':
            kezi_hely = [x for x in kezi_hely if x[0] != a]
            _javitott_allapot(allapot, ertek)
        else:
            for x in TOROL[szint]:
                allapot[x] = ''
            allapot[szint] = ertek
        ki.append((a, jel, utvonal(allapot)))
        poz = a + max(1, len(jel))


def lexikon_beolvas():
    con = sqlite3.connect('file:' + LEX_UT.replace('\\', '/') + '?mode=ro', uri=True)
    szocikk = {}
    for t, d in con.execute("select Topic, Definition from Lexicon where Topic like 'BDB%'"):
        h = re.match(r'<h1>(.*?)</h1>', d, re.S)
        cimkek = re.findall(r"lex\('(H\d+[a-z]?)'\)", h.group(1) if h else '')
        torzs = d[h.end():] if h else d
        torzs = re.sub(r'<div class="navigation">.*?</div>', '', torzs, count=1, flags=re.S)
        blokkok = []
        for m in re.finditer(r'<div class="(section|remarks)">', torzs):
            blokkok.append((m.group(1), ujjlenyomat(torzs[m.end():m.end() + 1500], True)[:8]))
        fp = ujjlenyomat(torzs, True)
        szocikk[t] = {'id': t, 'cimkek': cimkek, 'fp': fp, 'blokkok': blokkok, 'fejek': lexikon_fejek(torzs)}
    con.close()
    index = collections.defaultdict(list)
    for e in szocikk.values():
        for tok in set(e['fp'][:3]):
            index[tok].append(e['id'])
    return szocikk, index


def unpad(s):
    m = re.match(r'^H0*(\d+)([a-z]?)$', s)
    return 'H%s%s' % (m.group(1), m.group(2))


# ---------------------------------------------------------------- illesztés

def kezdet_jeloltek(fp, szocikk, index, sajat):
    """A bekezdés-eleje (fp) lehetséges szócikk-kezdetei: (pontszám, bdb_id), csökkenő sorrendben."""
    jel = set(sajat)
    for tok in set(fp[:3]):
        lista = index.get(tok, [])
        if len(lista) <= 300:      # a nagyon gyakori kezdő token (pl. „noun”) nem jelöltképző
            jel |= set(lista)
    ki = []
    for b in jel:
        e = szocikk[b]
        p = eleje_hasonlo(fp, e['fp'])
        if p >= ILL_KUSZOB:
            ki.append((p + (0.001 if b in sajat else 0), b))
    return sorted(ki, reverse=True)


def cimfolytatas_nelkul(fp):
    """Az első tartalmi blokk elején a cím átírásának folytatása állhat (pl. H3512 „<b>H3512. ka</b>” + „ah [כָּאָה]
    verb”, H8147 „or shettayim …”): az első héber token előtti legfeljebb 6 latin token nem része a szócikk-kezdetnek."""
    for i, t in enumerate(fp[:7]):
        if t.startswith('h:'):
            return fp[i:] if 0 < i <= 6 else fp
    return fp


def strong_illeszt(strong_eredeti, blokkok, szocikk, index, cimke_szerint):
    """bdb_id blokkonként (a 0. a cím); (hozzarendeles, kategoria, reszletek)."""
    sajat = cimke_szerint.get(strong_eredeti, [])
    fps = [ujjlenyomat(b, False) for b, _ in blokkok]
    hozz = [''] * len(blokkok)
    if len(fps) > 1:
        fps[1] = cimfolytatas_nelkul(fps[1])
    if len(blokkok) < 2:
        return hozz, 'sikertelen', 'nincs tartalmi blokk'

    def kezdo_fp(i):
        # kettévágott szócikk-kezdet (F107, DT-F107e (b)): a címszó egy rövid blokkban (< 4 token), a szöveg a
        # következőben (pl. H108 „I. אוה” + „1Arabic …”, H176 „אוֺ , , ),” + „conjunction or”): együtt mérjük
        if len(fps[i]) < 4 and i + 1 < len(fps):
            return fps[i] + fps[i + 1]
        return fps[i]

    elso = kezdet_jeloltek(kezdo_fp(1), szocikk, index, sajat)
    if not elso:
        tartalom = sum(len(f) for f in fps[1:])
        if tartalom < 8:
            # JSON-csonk: a címsor folytatása vagy utaló (pl. H381 „ish-chayil”, H358 „Elon Beth Chanan”), szócikk-szöveg nélkül
            return hozz, 'csonk', 'a tartalmi blokk nem szócikk-kezdet, %d token' % tartalom
        return hozz, 'sikertelen', 'az első tartalmi blokk nem szócikk-kezdet'
    aktualis = elso[0][1]
    hasznalt = {aktualis}
    hozz[0] = hozz[1] = aktualis
    for i in range(2, len(blokkok)):
        tokenek, mar = fej_bont(blokkok[i][0])
        if fej_valodi(tokenek, mar) and any(sz != 'romai' for sz, _ in tokenek):
            # számozott / betűs / törzs-fejű bekezdés nem nyit új szócikket
            hozz[i] = aktualis
            continue
        if len(fps[i]) < 4 and zarojel_folytatas(sima(blokkok[i - 1][0]), sima(blokkok[i][0])):
            # F202.2 (C1/C2, N147): a rövid blokk az előző bekezdés nyitott zárójelét zárja („compare Niph`al )”, H3988;
            # „(compare מַלְכוּת 2, מַמְלָכוּת 3).”, H4467): az előző szócikk vége, nem a következő szócikk-kezdet része (a
            # `kezdo_fp` a rövid blokkot a következővel együtt mérte, és a töredék a következő szócikkhez került)
            hozz[i] = aktualis
            continue
        # a későbbi szócikk-kezdet küszöbe azonos az elsőével (ILL_KUSZOB; F107.14: a 0,85 a H1817 BDB1943-at elvétette)
        uj = [x for x in kezdet_jeloltek(kezdo_fp(i), szocikk, index, sajat) if x[1] not in hasznalt]
        if uj:
            aktualis = uj[0][1]
            hasznalt.add(aktualis)
        hozz[i] = aktualis
    # szegmensek lefedése
    szegm = collections.OrderedDict()
    for i in range(1, len(blokkok)):
        szegm.setdefault(hozz[i], []).extend(fps[i])
    rossz, resz = [], []
    for b, fp in szegm.items():
        e = szocikk[b]['fp']
        a1, a2 = lefedes(fp, e), lefedes(e, fp)
        if a1 < LEFED_KUSZOB:
            rossz.append('%s %.2f/%.2f' % (b, a1, a2))
        elif a2 < LEFED_KUSZOB:
            resz.append('%s %.2f/%.2f' % (b, a1, a2))
    if rossz:
        return hozz, 'reszleges', '; '.join(rossz + resz)
    if resz:
        # a JSON-szegmens a szócikkben benne van, de a szócikk több (más Strongok alá eső) részt is tartalmaz
        return hozz, 'szocikk_resze', '; '.join(resz)
    return hozz, 'egyezik', ''


# ---------------------------------------------------------------- tagolás

def utvonal(allapot):
    t = allapot['torzs'] or '-'
    if allapot['nagy']:
        t += '.' + allapot['nagy'].rstrip('.')
    u = '%s/%s/%s' % (t, allapot['szam'] or '-', allapot['betu'] or '-')
    if allapot['zaro']:
        u += '/' + allapot['zaro']
    return u


# DT-F107e (a), felhasználó, 2026-10-18: a nem egyező Strong sorai a JSON szövegével és tagolásával, de bdb_id és
# section/remarks nélkül (explicit hiány; a kategória az `illesztes` oszlopban). A szocikk_resze bdb_id-je kitöltve.
BDB_NELKUL = {'reszleges', 'sikertelen', 'csonk'}


def strong_sorok(strong_pad, strong_eredeti, blokkok, hozz, kategoria, szocikk, ts, kezi=None):
    sorok = []
    kezi = kezi or {}
    allapot = dict.fromkeys(MINDEN_SZINT, '')
    alsz = 0
    szakasz, szakasz_mod, volt_fej = '', None, False
    nagy_szam_alatt = False
    kiir_bdb = kategoria not in BDB_NELKUL
    section_jel = {}
    if kiir_bdb:
        for b in set(hozz):
            if b:
                section_jel[b] = list(szocikk[b]['blokkok'])
    for i, (bh, sub1) in enumerate(blokkok):
        bdb = hozz[i]
        # szócikk eleje: az első tartalmi blokk, vagy ahol az illesztett szócikk váltott (a belső szegmentálás a
        # tagolás-állapotot akkor is nullázza, ha a bdb_id nem íródik ki)
        szocikk_eleje = i == 1 or (i > 1 and hozz[i] != hozz[i - 1])
        if szocikk_eleje:
            allapot = dict.fromkeys(MINDEN_SZINT, '')
            alsz = 0
            szakasz, szakasz_mod, volt_fej = '', None, False
            nagy_szam_alatt = False
        if i == 0:
            jelolo, jel, gy, szoveg, ut = 'cim', '', '', sima(bh), 'cim'
        else:
            if sub1 and not szocikk_eleje:
                alsz += 1
                allapot = dict.fromkeys(MINDEN_SZINT, '')
                szakasz, szakasz_mod, volt_fej = '', None, False
                nagy_szam_alatt = False
            tokenek, maradek = fej_bont(bh)
            if tokenek and not fej_valodi(tokenek, maradek):
                # DT-F107g (a) (1): hamis fej (hivatkozás a bekezdéstörés után) — a szöveg része, nem jelölő
                tokenek, maradek = [], bh
            hiv_jel = None
            demotalt = ''
            if i > 1 and not szocikk_eleje:
                hf = hivatkozas_fej(bh, allapot)
                if hf:
                    hiv_jel, betu, maradek = hf
                    tokenek = [('betu', betu + '.')]
            if (tokenek and i > 1 and not szocikk_eleje and not sub1 and not hiv_jel
                    and hamis_fej_kornyezet(sima(blokkok[i - 1][0]), sima(maradek), tokenek, allapot)):
                # F185 (N103 (2)): a környezet szerint hivatkozás (zárójel, „above/below”, „see …”, sorrendsértés)
                # a `jel` + `szoveg` összefűzve változatlan marad (a fordítások `forras_hash`-e erre a nézetre számol)
                demotalt = ' '.join(y for y in (' '.join(x for _, x in tokenek), sima(maradek)) if y)
                tokenek, maradek = [], bh
            hm = HOMONIMA_NYITO.match(sima(bh)) if not tokenek and i else None
            if hm:
                # F185 (seed-101 M009 H4428 „I. מֶ֫לֶךְ noun”, H1390 „II. גִּבְעָה proper name”): a félkövér nélküli római szám a
                # héber címszó előtt a homonima száma (a 2.29 `szakasz`-a); a szócikk belsejében új címszó-szakaszt nyit (DT229 (a) (2))
                if not szocikk_eleje:
                    allapot = dict.fromkeys(MINDEN_SZINT, '')
                    szakasz_mod, volt_fej, nagy_szam_alatt = None, False, False
                szakasz = hm.group(1)
            if not tokenek and i > 1 and not szocikk_eleje and not sub1 and not hm and alcimszo_nyito(bh):
                # F185: jelöletlen alcímszó `sub1` nélkül (seed-101 M238)
                alsz += 1
                allapot = dict.fromkeys(MINDEN_SZINT, '')
                szakasz, szakasz_mod, volt_fej, nagy_szam_alatt = '', None, False, False
                alcimszo_uj = True
            else:
                alcimszo_uj = False
            if (tokenek and kiir_bdb and bdb and not szocikk_eleje and not hiv_jel
                    and lexikon_szerint_hivatkozas(szocikk[bdb], tokenek, maradek)):
                # DT-F107h (a): a lexikonban ugyanez a fej a szövegen belül áll — hivatkozás a JSON bekezdéstörése után
                tokenek, maradek = [], bh
            # DT-F107h (a): a fejsorbeli törzsnév („<b>verb Pa`el</b>”, H2939) a szócikk törzsállapota a fej után
            fejsor_torzs = None
            if szocikk_eleje or sub1:
                m_t = re.search(r'<b>\s*verb\s+(' + TORZS + r')\.?\s*</b>', bh)
                if m_t:
                    fejsor_torzs = TORZS_KANON.get(m_t.group(1), m_t.group(1)).replace('`', "'")
            gy = ','.join(gyakorisag_kivesz(bh, bool(tokenek)))
            if tokenek and szocikk_eleje and all(sz == 'romai' for sz, _ in tokenek):
                # a szócikk-eleji római szám a homonima száma (aranyminta 2.28 `szakasz`), nem fő tagolás
                jelolo, jel, szoveg, ut = 'fej', ' '.join(x for _, x in tokenek), sima(maradek), 'fej'
                szakasz = tokenek[-1][1].rstrip('.')
            elif tokenek:
                for szint, szov in tokenek:
                    if szint == 'romai':
                        if szakasz_mod is None:
                            # DT-F107g (a) (2): ha a szócikk első római feje „I.”, és előtte nem volt szám-, betű- vagy
                            # törzsfej, a római fejek homonima-szakaszok (H6440), különben fő tagolás (`resz`; H3068, H8478)
                            # F185 (seed-101 M062 H3824 „I. seldom of things”): homonima-szakasz csak héber címszó előtt;
                            # glossza előtt a fő tagolás (`resz`), mint a szeletelő TAGOLAS-a
                            # (a „II. פְּנֵי with prepositions” is, ha nem „I.” az első: seed-101 M029, seed-102 M024 H6440)
                            szakasz_mod = (not volt_fej
                                           and re.match(r'\[?[\u0590-\u05ff]', sima(maradek)) is not None)
                        nagy_szam_alatt = False
                        if szakasz_mod:
                            allapot = dict.fromkeys(MINDEN_SZINT, '')
                            szakasz = szov.rstrip('.')
                        else:
                            for x in ('nagy', 'szam', 'betu', 'zaro'):
                                allapot[x] = ''
                            allapot['resz'] = szov.rstrip('.')
                    else:
                        volt_fej = True
                        torol = TOROL[szint]
                        if szint == 'nagy' and (nagy_szam_alatt or (allapot['szam'] and not allapot['nagy'])):
                            # F185 (seed-102 M226 H5676 „1 … A. east Jordan … B. West Jordan … 2”): a számozott pont ALATT álló
                            # nagybetűs csoport a számot nem törli; a következő szám a csoportot zárja (lent)
                            nagy_szam_alatt = True
                            torol = ('betu', 'zaro')
                        elif szint == 'szam' and nagy_szam_alatt:
                            nagy_szam_alatt = False
                            torol = ('nagy',) + TOROL['szam']
                        elif szint in ('torzs', 'nagy'):
                            nagy_szam_alatt = False
                        for x in torol:
                            allapot[x] = ''
                        if szint == 'torzs':
                            nev = szov.rstrip('.')
                            allapot['torzs'] = TORZS_KANON.get(nev, nev).replace('`', "'")
                        elif szint == 'szam':
                            allapot['szam'] = szov.rstrip('.')
                        elif szint == 'betu':
                            allapot['betu'] = szov.rstrip('.')
                        else:
                            allapot[szint] = szov
                jelolo = 'point'
                jel = hiv_jel or ' '.join(s for _, s in tokenek)
                szoveg = sima(maradek)
                ut = utvonal(allapot)
                if ut == '-/-/-' and not allapot['resz']:
                    ut = 'fej'      # csak homonima-szakasz fej (pl. „II.”), jelentésszint nélkül
            else:
                jel = ''
                szoveg = demotalt or sima(bh)
                if szocikk_eleje or ((sub1 or alcimszo_uj) and not any(allapot[x] for x in MINDEN_SZINT)):
                    jelolo, ut = ('alcimszo' if (sub1 or alcimszo_uj) and not szocikk_eleje else 'fej'), 'fej'
                elif not any(allapot[x] for x in MINDEN_SZINT):
                    jelolo, ut = 'bekezdes', 'fej'
                else:
                    jelolo, ut = 'bekezdes', utvonal(allapot)
            # section / remarks a lexikonból (csak metaadat): a blokk eleje a lexikon-blokk elejével egyezik
            if bdb and section_jel.get(bdb):
                fp = ujjlenyomat(maradek if tokenek else bh, False)[:8]
                for j, (osztaly, lfp) in enumerate(section_jel[bdb]):
                    if lfp and eleje_hasonlo(fp, lfp) >= 0.9:
                        jelolo = osztaly
                        del section_jel[bdb][j]
                        break
        belso = []
        if i == 0:
            ut = 'cim'
        else:
            kz = kezi.get((strong_pad, str(i + 1)), [])
            if any('</p>' in f for f, _ in kz):
                # a sor eleji jelölőhöz hiányzó törzsnév (2.31 kézi, H3318 „Qal”)
                for f, jav in kz:
                    if '</p>' in f:
                        _javitott_allapot(allapot, jav)
                ut = utvonal(allapot)
            if any(allapot[x] for x in ('torzs', 'szam', 'betu')) or kz:
                belso = belso_fejek(szoveg, allapot, kz)
        sorok.append([strong_pad, bdb if kiir_bdb else '', str(i + 1), str(alsz), szakasz if i else '',
                      allapot['resz'] if i else '', ut, jelolo, jel, gy, szoveg,
                      kategoria, 'DictBDB.json:%s#%d' % (strong_eredeti, i),
                      hashlib.sha256(bh.encode('utf-8')).hexdigest()[:16],
                      'scope=%s | forras=bdb_jelolt/bont.py (fejléc) | ts=%s' % (strong_pad, ts),
                      ';'.join('%d|%s|%s' % x for x in belso)])
        if i and fejsor_torzs and ut == 'fej':
            allapot['torzs'] = fejsor_torzs
    return sorok


# ---------------------------------------------------------------- fő

def general(ts, json_ut=JSON_UT):
    with open(json_ut, encoding='utf-8') as f:
        data = json.load(f)
    szocikk, index = lexikon_beolvas()
    cimke_szerint = collections.defaultdict(list)
    for e in szocikk.values():
        for c in e['cimkek']:
            cimke_szerint[c].append(e['id'])
    sorok, stat, reszlet = [], collections.Counter(), {}
    kezi = kezi_jelolok()
    for item in data:
        top = item.get('top', '')
        m = re.match(r'^H(\d+)', top)
        if not m:
            continue
        pad = 'H%04d' % int(m.group(1)) + top[len(m.group(0)):]
        blokkok = json_blokkok(item.get('def', ''))
        hozz, kat, r = strong_illeszt(top, blokkok, szocikk, index, cimke_szerint)
        stat[kat] += 1
        if kat != 'egyezik':
            reszlet[pad] = (kat, r)
        sorok.extend(strong_sorok(pad, top, blokkok, hozz, kat, szocikk, ts, kezi))
    return sorok, stat, reszlet


def fajl_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/bdb_jelolt/bont.py --ts %s — kézzel nem szerkesztendő (F107; séma: adat/SEMA.md, bdb_szakaszok.tsv).' % ts,
           '# forras: konkordancia/lexikonok_nyers/DictBDB.json@%s (szöveg, tagolás) + konkordancia/lexikonok_nyers/BDB.lexicon@%s '
           '(csak bdb_id, szócikkhatár, section/remarks; DT225) + kód@%s' % (sha256_fajl(JSON_UT)[:12], sha256_fajl(LEX_UT)[:12], kod_hash()[:12]),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(s) for s in sorok]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    ap.add_argument('--meres', action='store_true')
    ap.add_argument('--ellenoriz', action='store_true')
    ap.add_argument('--lista', type=int, default=30, help='a nem egyező Strongokból ennyit ír ki')
    a = ap.parse_args()
    if sha256_fajl(JSON_UT) != JSON_HASH:
        print('HIBA: a DictBDB.json hash-e eltér a rögzítettől', file=sys.stderr)
        return 2
    sorok, stat, reszlet = general(a.ts)
    ossz = sum(stat.values())
    print('Strong: %d; %s; nem egyező arány: %.2f%% (a csonk nélkül: %.2f%%)' % (ossz, dict(stat), 100.0 * (ossz - stat['egyezik']) / max(1, ossz), 100.0 * (ossz - stat['egyezik'] - stat['csonk']) / max(1, ossz)))
    print('sor: %d; jelolo: %s' % (len(sorok), dict(collections.Counter(s[FEJLEC.index('jelolo')] for s in sorok))))
    for k, (kat, r) in list(sorted(reszlet.items()))[:a.lista]:
        print('  %s %s %s' % (k, kat, r[:160]))
    if a.meres:
        return 0
    szoveg = fajl_szoveg(sorok, a.ts)
    if a.ellenoriz:
        with open(KI_UT, encoding='utf-8', newline='') as f:
            regi = f.read()
        if regi != szoveg:
            print('ELTÉR: %s' % KI_UT)
            return 1
        print('azonos: %s' % KI_UT)
        return 0
    with open(KI_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('írva: %s' % KI_UT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
