#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
olvasoi_kapu.py -- a gépi olvasói kapu egy generált lexikonlapon (`lexikon/[ID]_TUDOMANYOS.md`).

A lap-átvilágítás (2026-11-02) olvasói hibái átmentek a szerkezeti kapukon (Feed 1–8, ellenoriz.py, CI).
Ez az eszköz az átvilágítás „Mi gépesíthető” táblázatának pontjait méri azon, amit az olvasó lát: a lapon.
Csak olvas; lapot, prózát, adatot nem javít. A Feed 9. kapuja (`muhely_allapot.py`) erre épül (DT-F156k).

Ellenőrzések: a modulszintű `KAPUK` tábla (azonosító, súlyosság, leírás) és a VISSZHANG alszabályai
(`VISSZHANG_ALSZABALYOK`, V1–V7). A tábla az egyetlen leírás: belőle generálódik az `adat/SEMA.md` 3.11
„Gépi kapuk — szabálylista” blokkja (`python eszkozok/ellenorzes/szabalyok.py --kapulista --ir`), a CI E37
pedig ellenőrzi, hogy a tábla azonosítói egyeznek a kódban kibocsátott találatokéval (F184 D3).

Az olvasói szöveg: minden látható sor, kivéve a HTML-megjegyzést, a kódblokkot, a technikai dőlt sort (egész
sor `*…*`), a proveniencia-lábjegyzetet (`[^x]: proveniencia:` / `forrás:` / `scope=`), valamint a Tartalomjegyzék,
a Jelmagyarázat és a Kolofon szakaszát (ezek a lap készítőinek szóló, tervezett technikai részek; a Kolofont a
KOLOFON ellenőrzés külön méri). A küszöbök kalibrálása: `naplok/OLVASOI_KAPU_jelentes.md`.

Használat:
    python eszkozok/olvasoi_kapu.py ID [ID ...] [--reszletes] [--json FAJL]
    python eszkozok/olvasoi_kapu.py --osszes
Kilépési kód: 1, ha bármely lapon van BUKÁS; 0 egyébként.
"""
import argparse
import difflib
import json
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

BUKAS, FIGY = 'BUKÁS', 'FIGYELMEZTETÉS'

# Az olvasói kapu ellenőrzései (F184 D3): ez az egyetlen leírásuk. Ebből generálódik az `adat/SEMA.md` 3.11 blokkja
# (`python eszkozok/ellenorzes/szabalyok.py --kapulista --ir`); a CI E37 ellenőrzi, hogy az azonosítók egyeznek a
# kódban kibocsátott `talalat('<AZON>', …)` hívásokéval, és a V-alszabályok a VISSZHANG üzeneteivel.
KAPUK = (
    ('BELSO', BUKAS, 'belső jelölés az olvasói szövegben (DT/N/F-tétel, #nnn, P1–P7, ELLENOR_, orkesztrátor, gerinc, '
                     '.tsv, manual, belső fájl; a csupasz Strong-szám, ahol mellette ott a héber/görög szó és a kiejtése — '
                     'a jelölt alak (hivatkozás + felső index, DT602) és a táblázat „Strong” oszlopa nem hiba; a „(kézi)” / '
                     '„(generált)” szerzőségi jelölés a lap bármely látható sorában, a Tartalomjegyzékben is, DT603)'),
    ('MOTIVUM_ID', FIGY, 'más motívum azonosítója link nélkül'),
    ('ONREF', FIGY, 'önreferáló „a lap” fordulat az új szerkezetű lap látható szövegében (a lap az oldal önmagára utalva: '
                    'helyette a valódi alany, a motívum, a vizsgálat, a keresés vagy a szócikk); kivétel a Kolofon és a '
                    'más motívum lapjára utaló fordulat (a felhasználó v8-átnézése, 4.)'),
    ('PONT', BUKAS, '„N. pont” hivatkozás: nem létező szakaszra vagy rossz névvel BUKÁS, egyébként FIGYELMEZTETÉS'),
    ('ANGOL', BUKAS, 'angol maradék és munkazsargon a szólistából'),
    ('ANGOL_SOR', FIGY, '≥3 angol funkciószó egy sorban'),
    ('IDEZOJEL', BUKAS, 'egyenes " a magyar szövegben'),
    ('ATIRAS', BUKAS, 'ugyanaz a héber/görög szó két kiejtéssel'),
    ('ATIRAS_VALT', FIGY, 'a lapon álló kiejtés ékezet-eltérő változata dőlt/zárójeles helyen'),
    ('KONYV', BUKAS, 'könyvrövidítés nem a `Konyv_normalizalo_tabla.tsv` alakjával'),
    ('BDB_JEL', BUKAS, 'torzult jel a szövegben (^, ®, °, a BDB átírási betűkészletének ¹ µ £ ¥ ‰ ƒ ‡ ¢ jele, rafe, '
                       'latin betű héber szóhoz tapadva, ,,)'),
    ('ZAROJEL', BUKAS, 'nyitva maradt zárójel (a 2. Szótári háttérben BUKÁS, máshol FIGYELMEZTETÉS)'),
    ('FUNKCIO_URES', BUKAS, 'az 1. tábla „Funkció” oszlopában üres cella'),
    ('IDEZET', BUKAS, 'az 1/a jegyzet idézete nem a fölötte álló Károli-vers szövege, és nincs „saját fordítás” jelölés'),
    ('KIVONAT_SZAM', FIGY, 'a Kivonat darabszáma eltér a tábla összesítőjétől'),
    ('KOLOFON', BUKAS, 'hiányzó Kiadás / Változásjegyzék / Próza modellje, üres törzsadat-mező'),
    ('HIANYJEL', FIGY, 'belső hiányjelzés az olvasói cellában („(nincs …)”)'),
    ('SZINT_ALATT', FIGY, 'üres vagy az arany laphoz mérve szint alatti blokk'),
    ('KH_MASOLT', FIGY, 'a Károli-KH lista más vers listájának teljes vagy részleges másolata (`karoli_kh_epseg.py`; '
                        'javítás: N-F156a); az új szerkezetű lapon BUKÁS (lap-javit HAMART-001, lektor 15.)'),
    ('LABJEGYZET', BUKAS, 'definíció nélküli lábjegyzet (átvett: `ellenoriz.lap_labjegyzet_hianyok`, ha a main-en van)'),
    ('PROZA_1A', BUKAS, 'az 1/a igehely alatt nincs kerek próza vagy „Funkció:” sor (átvett: `proza_1a.meres`)'),
    ('CELLA_ISMETLES', BUKAS, 'egy táblacellában ugyanaz a hivatkozott elem („… [ⓘ](…)”) többször áll (F123.HAMART3)'),
    ('VISSZHANG', BUKAS, 'a visszhang-blokk szabályai (a 9. Hatástörténet ószövetségi táblája, korábban 4.11; F178.5, DT645, DT646): a `VISSZHANG_ALSZABALYOK` V1–V7'),
    ('NAVE_ANGOL', BUKAS, 'a Nave-blokkban angol témanév az olvasói szövegben (nem `title`-ben), vagy bárhol nyers '
                          'HTML-karakterkód (`&#8221`) (F123.HAMART3 javítókör)'),
    ('MUNKASZO', BUKAS, 'munkaszó vagy munkajelölő az olvasói szövegben (a `MUNKASZAVAK` lista: „próba”, „javaslat”, '
                        '„ellenőrzendő”, „függőben”, „nincs bekötve”, „kutatói jelölés”, „azonosításra vár”, „D-minta”, '
                        '„Q3-fegyelem”, „study”, „audit”, „token”, „↳ Alpont:”, „független keresés”, „mért pontosság”); '
                        'az új szerkezetű lapon BUKÁS (a /kiadas jelölő-kapuja is), a régin FIGYELMEZTETÉS (F182: F22, H4, '
                        'F24, F35)'),
    ('HELYORZO', BUKAS, 'nyers helyőrző a lapon („<KANONIKUS_FORRAS_URL>”, „[HELYŐRZŐ…]”, „<DOI>”, üres „DOI: .”); '
                        'csak az új szerkezetű lapon (a felhasználó döntései, 2026-11-11: a szerző, a lexikon címe és a '
                        'kanonikus cím a generátor beállításából, hiányuk olvasói mondattal)'),
    ('SZAKASZ_HIV', BUKAS, 'a lap „N. szakasz” / „N. (Név)” hivatkozása nem létező szakaszra vagy más nevű szakaszra mutat '
                           '(a BDB és a szócikk saját szakaszai nem); csak az új szerkezetű lapon (F182: F22 (b))'),
    ('NYERS_JEL', BUKAS, 'nyers mezőnév vagy belső jel az olvasói szövegben, a lábjegyzetben is („proveniencia:”, '
                         '„igazolas:”, `jelentes_szam`, „sorszám N”, „napló: …”, „(4/b. rész)”, `halo=`, `blokk=`, „lanc ±1”, '
                         '„csalad H…”, „indoklás (nyers)”, „szónézet: /szo/…”, tW-azonosító `kt/…`, `other/…`, `karoli_szo`, a '
                         'címszó belső számlálója `_226`); csak az új szerkezetű lapon (F182: A08, A11, A17, KH-lábjegyzet)'),
    ('MI_HANG', BUKAS, '„mi”-hangú (első személyű többes számú) igealak az olvasói szövegben, a Károli-idézeten és a „…” '
                       'idézeten kívül („átnéztük”, „vizsgáltunk”, „döntöttünk”); csak az új szerkezetű lapon (F182: A07, '
                       'B07, K12)'),
    ('NEVELO', BUKAS, '„a” névelő magánhangzóval kezdődő szó előtt („a adamá”, „A arar”), az idézeten kívül; csak az új '
                      'szerkezetű lapon (F182: A06, F4 (c), K48)'),
    ('MEGHATAROZAS', BUKAS, 'a lap elején „A motívum.” bekezdés üres, a címet ismétli vagy csak az azonosság típusát mondja, '
                            'vagy a Kolofonban nincs „Meghatározás” sor; csak az új szerkezetű lapon (lap-javit HAMART-001)'),
    ('LISTA_NEVELO', BUKAS, 'lista- vagy táblaelem kisbetűs „a”/„az” névelővel kezdődik („a BDB-szótár (közkincs)”): a név '
                            'és a leíró elem névelő nélkül áll, a névelőt csak a folyó szöveg teszi elé; csak az új '
                            'szerkezetű lapon (lap-javit HAMART-001, orkesztrátori tétel)'),
    ('KOV_ISM', BUKAS, 'ugyanaz a „Következtetés:” mondat legalább háromszor egy szakaszban (a V6 kiterjesztése minden '
                       'pontra); csak az új szerkezetű lapon (F182: A14, A16, F12, K10)'),
    ('INDOKLAS', BUKAS, 'a döntés indoklásában (a „**elutasítva**”, „**beépítve**”, „**nyitva**” cella) héber vagy görög '
                        'írás zárójeles kiejtés nélkül, más sorra hivatkozás („… sorának folytatása”) vagy munkajavaslat '
                        '(„érdemes lehet külön vizsgálatra”); csak az új szerkezetű lapon (F182 javítókör: A05, A06, B08, '
                        'K47, K48)'),
    ('BDB_OLVASOI', BUKAS, 'a 4.2 BDB- és Thayer-kártyájának olvasói rétegében (a szótári apparátus előtt) feloldatlan '
                           'rövidítés, belső címke vagy nyers sorszám (a szócikk sorszáma is), a szócikk feje mint '
                           'jelentéspont, kétszer álló vers a motívum helyei között, a Thayer-kártyán nyers görög alak; csak '
                           'az új szerkezetű lapon (F104, F187)'),
)

# A VISSZHANG alszabályai (DT639, DT645, DT646, DT-F184a); a szabályok szövege: `sablonok/6_PaRDeS_lexikon_oldal_sablon.md`,
# „A 4.11 visszhang-blokk szabályai”.
VISSZHANG_ALSZABALYOK = (
    ('V1', 'angol maradék a blokkban (BDB-fordulat, angol glossza, „fordításra vár”)'),
    ('V2', 'nem rokon nyelvi sor a BDB-háttérben (újhéber, targumi arámi, Sirák)'),
    ('V3', '„nincs rokon nyelvi adat”, holott a BDB-szócikk nem azonosítható (bdb_szócikk=0): a kettő nem vonható össze'),
    ('V4', '„ugyanaz a szó”, holott a cellában két lemma áll (helyesen: „ugyanaz a szócsalád”)'),
    ('V5', 'kiemelt (félkövér) következtetés alapvonal nélkül: kiemelt csak a láncon kívüli alapvonallal (a LXX sávja szerint), '
           'két héber lánc-szó egyesítése is csak így; a Targumnál és a Vulgatánál nem (DT645, pontosítva)'),
    ('V6', 'ugyanaz a tagmondat (a számok és a fordítók neve nélkül) legalább háromszor a táblán'),
    ('V7', 'az alapvonal-mondat nem a sávja (≥ 80% / 40–80% / < 40%) szerinti, a zárójeles versszám nevezőként áll, '
           'vagy a három szám nem egyezik'),
)
ARANY = 'ISTENTISZT-001'

KIZART_SZAKASZ_REGI = ('Tartalomjegyzék', 'Jelmagyarázat', 'Kolofon')
KIZART_SZAKASZ = KIZART_SZAKASZ_REGI
IRODALOM = '8. Irodalom'
# F178.4: az új szerkezetű lapon (1. Döntési út … 12. Irodalom) az olvasói kapu kivétel nélkül mér: a Tartalomjegyzék,
# a Jelmagyarázat, a Kolofon és az Irodalom is olvasói szöveg, a technikai dőlt sor és a lábjegyzet is (a nyers
# proveniencia-sor a lap forrásában HTML-megjegyzésben áll). A régi szerkezetű lapon a régi mérce, amíg a lap az új
# körben újra nem generálódik (a felhasználó: „Előbb csak a hamart”, 2026-11-08).
UJ_SZERKEZET_RX = re.compile(r'(?m)^## 1\. Döntési út[ \t]*$')
KIVETEL_NELKUL = False
ELOFORDULAS_SZAKASZ = ('1. Előfordulások', '2. Előfordulások')
SZOTARI_SZAKASZ = ('2. Szótári', '4. Szótári')

# --- BELSO: belső jelölések (az átvilágítás A4, A21, T3, T14, G4, G5, G7)
BELSO = [
    (re.compile(r'(?<![\w-])DT-?F?\d+[a-z]?\b'), 'döntés-azonosító'),
    (re.compile(r'(?<![\w-])N-F\d+[a-z]?\b|(?<![\w-])N\d{1,3}\b'), 'N-tétel'),
    (re.compile(r'(?<![\w/.#-])F\d{1,3}(?:\.\d+)?\b'), 'F-tétel'),
    (re.compile(r'(?<![\w&/])#\d{2,3}\b'), 'feladatszám'),
    (re.compile(r'(?<![\w-])P[1-7]\b'), 'munkalépés-jel'),
    (re.compile(r'ELLENOR_'), 'ellenőri napló'),
    (re.compile(r'orkesztrátor', re.I), 'munkafolyamat-szereplő'),
    (re.compile(r'\bgerinc', re.I), 'belső szó (gerinc)'),
    (re.compile(r'\.tsv\b|\.py\b|[\w/]+\.md\b|NYITOTT_FELADATOK'), 'belső fájl'),
    (re.compile(r'\bmanual\b'), 'proveniencia-érték (manual)'),
    (re.compile(r'\b(?:tanítói|forrás)\s?fájl\w*|\bfájl(?:ban|ból|ja|jában)\b', re.I), 'belső fájl'),
]
MOTIVUM_ID = re.compile(r'(?<![\w\[/#`-])([A-ZÁÉÍÓÖŐÚÜŰ]{3,}-\d{3})\b(?![\]`])')

# --- ANGOL: szólista (A22, T11, G4) és funkciószó-küszöb
ANGOL_SZO = re.compile(r'\bgap\b|\bstudy\b|\bwas called\b|\bhaving been\b|\bscan\w*|LXX_OS|'
                       r'\bpipeline\b|\bworkflow\b|\bbatch\w*|\bverdict\b|(?<![\w.])[1-3]?[A-Z][a-z]{1,3}\.\d+\.\d+\b',
                       re.I)
# az „is” és a „be” magyar szó is, ezért nincs a listában
ANGOL_FUNKCIO = re.compile(r'\b(the|and|of|with|which|from|that|this|are|was|were|by|to|in|for|not|or|as|an|it|'
                           r'its|his|her|their|who|whom|into|upon|unto)\b')
ANGOL_SOR_MIN = 3

# --- BDB_JEL (A12, A23, T8)
BDB_JEL = [
    (re.compile(r'(?<!\[)\^'), 'nyers ^ elválasztó'),
    (re.compile(r'[®°]'), 'torzult jel (® / °)'),
    # F123.GENKOR: a DictBDB.json átírási betűkészletének többi torz jele (N89); a † (Abbott-Smith) és a ± (±1) jogos jel
    (re.compile(r'[¹µ£¥‰ƒ‡¢]'), 'torzult jel (a BDB átírási betűkészlete: ¹ µ £ ¥ ‰ ƒ ‡ ¢)'),
    (re.compile('ֿ'), 'rafe (ֿ) pontjel a héber szóban'),
    (re.compile(r'[א-ת][֑-ׇ]*[A-Za-z]|[A-Za-z][א-ת]'), 'latin betű héber szóhoz tapadva'),
    (re.compile(r'[^\s,],,'), 'dupla vessző'),
]

# számnevek a Kivonat-összevetéshez
SZAMNEV = {'egy': 1, 'két': 2, 'kettő': 2, 'három': 3, 'négy': 4, 'öt': 5, 'hat': 6, 'hét': 7, 'nyolc': 8,
           'kilenc': 9, 'tíz': 10, 'tizenegy': 11, 'tizenkét': 12, 'tizenkettő': 12, 'tizenhárom': 13,
           'tizennégy': 14, 'tizenöt': 15, 'tizenhat': 16, 'tizenhét': 17, 'tizennyolc': 18, 'tizenkilenc': 19,
           'húsz': 20, 'mindkét': 2, 'mindhárom': 3, 'mind a négy': 4, 'mind az öt': 5}
SZAM_FONEV = r'(?:igehely|hely|előfordulás|vers|ószövetségi|újszövetségi)'


# ----------------------------------------------------------------------------- segédek

def tsv(rel):
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f]
    sorok = [s for s in sorok if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t') + [''] * (len(fej) - len(s.split('\t'))))) for s in sorok[1:]]


_KONYV = None


def konyvek():
    """(magyar rövidítések halmaza, magyar -> STEPBible, ÚSZ-rövidítések halmaza)."""
    global _KONYV
    if _KONYV is None:
        sorok = tsv('konkordancia/Konyv_normalizalo_tabla.tsv')
        hu = [s['Magyar rövidítés'] for s in sorok]
        step = {s['Magyar rövidítés']: s['STEPBible-rövidítés'] for s in sorok}
        i = next(k for k, s in enumerate(sorok) if s['STEPBible-rövidítés'] == 'Mat')
        _KONYV = (set(hu), step, set(hu[i:]))
    return _KONYV


def ekezet_nelkul(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))


def normal_szoveg(s):
    """Idézet-összevetéshez: kisbetű, ékezet és írásjel nélkül, egyszeres szóközzel."""
    s = ekezet_nelkul(s.lower())
    s = re.sub(r'[^\w\s]', ' ', s)
    return ' '.join(s.split())


def lathato(s):
    """A sor látható szövege: megjegyzés, horgony, link-cél és lábjegyzet-hivatkozás nélkül."""
    s = re.sub(r'<!--.*?-->', '', s)
    s = re.sub(r'<a id="[^"]*"></a>', '', s)
    s = re.sub(r'<a href="[^"]*">', '<a>', s)   # F182: a HTML-link célja nem látható szöveg (a kizárt helyek melléklete)
    # a jelölt Strong-szám (DT-F181b): „[mizbéah](/szo/H4196)<sup class="strong" …>H4196</sup>” → „mizbéah H4196”
    s = re.sub(r'\[([^\]]*)\]\((/szo/[^)]*)\)(?=<sup class="strong")', r'\1', s)
    s = re.sub(r'<sup class="strong"[^>]*>([^<]*)</sup>', r' \1', s)
    s = re.sub(r'\]\([^)]*\)', ']', s)
    s = re.sub(r'\[\^[^\]]+\]', '', s)
    # a cellába vagy sorba ágyazott proveniencia (`scope=… | forras=… | ts=…`, „forrás: `fájl`”) nem olvasói próza
    s = re.sub(r'(?:\\?\|\s*)?scope=.*?ts=[\dT:Z.-]+', '', s)
    s = re.sub(r'forrás:\s*`[^`]*`', '', s)
    return s


def kod_nelkul(s):
    return re.sub(r'`[^`]*`', ' ', s)


class Sor:
    __slots__ = ('n', 'nyers', 'szoveg', 'fajta', 'szakasz', 'alszakasz')

    def __init__(self, n, nyers, szoveg, fajta, szakasz, alszakasz):
        self.n, self.nyers, self.szoveg, self.fajta = n, nyers, szoveg, fajta
        self.szakasz, self.alszakasz = szakasz, alszakasz

    @property
    def olvasoi(self):
        """Olvasói próza-e (az ellenőrzések nagy része csak ezeken fut)."""
        if KIVETEL_NELKUL:
            return self.fajta in ('proza', 'tabla', 'cim', 'labjegyzet', 'dolt', 'proveniencia')
        if self.fajta not in ('proza', 'tabla', 'cim', 'labjegyzet'):
            return False
        return not self.szakasz.startswith(KIZART_SZAKASZ)


def tagol(szoveg):
    """A lap soraira bontása fajtával és szakasszal."""
    ki = []
    komment = kod = False
    szakasz = alszakasz = ''
    elozo = ''
    tabla_fej = None
    for n, nyers in enumerate(szoveg.replace('\r', '').split('\n'), 1):
        s = nyers
        if kod:
            if s.strip().startswith('```'):
                kod = False
            ki.append(Sor(n, nyers, '', 'kod', szakasz, alszakasz))
            continue
        if s.strip().startswith('```'):
            kod = True
            ki.append(Sor(n, nyers, '', 'kod', szakasz, alszakasz))
            continue
        if komment:
            if '-->' in s:
                komment = False
                s = s.split('-->', 1)[1]
            else:
                ki.append(Sor(n, nyers, '', 'komment', szakasz, alszakasz))
                continue
        if '<!--' in s and '-->' not in s.split('<!--', 1)[1]:
            komment = True
            s = s.split('<!--', 1)[0]
        lat = lathato(s)
        t = lat.strip()
        m = re.match(r'^(#{1,6})\s+(.*)', t)
        if m:
            if len(m.group(1)) <= 2:
                szakasz, alszakasz = m.group(2).strip(), ''
            else:
                alszakasz = m.group(2).strip()
            fajta = 'cim'
        elif not t:
            fajta = 'ures'
        elif re.match(r'^\[\^[^\]]+\]:', nyers.strip()):
            def_szoveg = nyers.split(':', 1)[1].strip()
            fajta = 'proveniencia' if re.match(r'(proveniencia|forrás)\s*:', def_szoveg) or 'scope=' in def_szoveg \
                else 'labjegyzet'
            lat = re.sub(r'<!--.*?-->', '', def_szoveg)   # F178.4: a nyers proveniencia megjegyzésben áll
        elif t.startswith('|'):
            fajta = 'tabla'
            cellak = re.split(r'(?<!\\)\|', t.strip('|'))
            if tabla_fej is None:
                tabla_fej = [c.strip() for c in cellak]
            elif len(cellak) == len(tabla_fej):
                # a „Forrás” oszlop proveniencia (fájlnév, dataset-név): nem olvasói próza
                lat = '|' + '|'.join('' if tabla_fej[i] == 'Forrás' else c for i, c in enumerate(cellak)) + '|'
        elif t.startswith('>'):
            fajta = 'idezetblokk'  # a szótár angol eredetijének szó szerinti idézete
        elif re.match(r'^\*[^*].*\*$', t) or t in ('*', '**'):
            fajta = 'karoli' if re.match(r'^\*\*[^*]+\d+:\d+[^*]*\*\*$', elozo.strip()) else 'dolt'
        else:
            fajta = 'proza'
        if fajta != 'tabla':
            tabla_fej = None
        ki.append(Sor(n, nyers, lat, fajta, szakasz, alszakasz))
        if fajta != 'ures':
            elozo = lat
    return ki


def bekezdesek(sorok):
    """Az egymást követő prózasorok bekezdésekké fűzve (a lap kézi sortöréssel tördel): [(első sor, szöveg)].
    Listaelem (`- `, `1. `) új bekezdést kezd."""
    ki, akt = [], None
    for s in sorok:
        if s.fajta == 'proza' and not (akt and re.match(r'^\s*(?:[-*]|\d+\.)\s', s.szoveg)):
            if akt is None:
                akt = [s, [s.szoveg.strip()]]
            else:
                akt[1].append(s.szoveg.strip())
            continue
        if akt:
            ki.append((akt[0], ' '.join(akt[1])))
            akt = None
        if s.fajta == 'proza':
            akt = [s, [s.szoveg.strip()]]
    if akt:
        ki.append((akt[0], ' '.join(akt[1])))
    return ki


def talalat(azon, suly, sor, idezet, uzenet, kulcs=None):
    """Egy találat. A `kulcs` a csoportosítás alapja: az azonos azonosítójú, súlyosságú és kulcsú találatok egy
    szakaszon belül egy tételbe olvadnak (`db`, `sorok`), mert ugyanaz a hiba sokszor ismétlődik (pl. tábla-oszlop)."""
    return {'azonosito': azon, 'sulyossag': suly, 'sor': sor, 'idezet': (idezet or '').strip()[:160],
            'uzenet': uzenet, 'kulcs': kulcs}


def csoportosit(talalatok, sorok):
    szakasz = {s.n: s.szakasz for s in sorok}
    ki, index = [], {}
    for t in sorted(talalatok, key=lambda x: (x['sor'], x['azonosito'])):
        if t['kulcs'] is None:
            t = dict(t, db=1, sorok=[t['sor']])
            t.pop('kulcs')
            ki.append(t)
            continue
        k = (t['azonosito'], t['sulyossag'], t['kulcs'], szakasz.get(t['sor'], ''))
        if k in index:
            index[k]['db'] += 1
            index[k]['sorok'].append(t['sor'])
            continue
        t = dict(t, db=1, sorok=[t['sor']])
        t.pop('kulcs')
        index[k] = t
        ki.append(t)
    return ki


def kornyezet(s, m, szel=50):
    return s[max(0, m.start() - szel):m.end() + szel]


# ----------------------------------------------------------------------------- ellenőrzések

# F178.6: a „felhasználó” mint munkafolyamat-szereplő az új szerkezetű lapon BUKÁS (olvasói név: szerkesztői
# döntés); a régi szerkezetű lapon a következő körben javul, a belső adat (`jeloltek.tsv` indoklása) nem változik —
# ezért a minta nem a BELSO listában áll (azt az `ellenoriz.py` 29. szabálya és a `szerep_kizart` is használja)
FELHASZNALO_RX = re.compile(r'(?<!\w)[Ff]elhasználó\w*')


def ell_belso(sorok):
    ki = []
    for s in sorok:
        if not s.olvasoi:
            continue
        if KIVETEL_NELKUL:
            m = FELHASZNALO_RX.search(s.szoveg)
            if m:
                ki.append(talalat('BELSO', BUKAS, s.n, kornyezet(s.szoveg, m), 'munkafolyamat-szereplő: ' + m.group(0),
                                  'felhasznalo'))
        for rx, nev in BELSO:
            if nev == 'belső fájl' and s.szakasz.startswith(IRODALOM) and not KIVETEL_NELKUL:
                continue  # az Irodalom a lapot és a forrásfájlt idézhetőként nevezi meg
            m = rx.search(s.szoveg)
            if m:
                ki.append(talalat('BELSO', BUKAS, s.n, kornyezet(s.szoveg, m), nev + ': ' + m.group(0),
                                  nev + m.group(0)))
        if s.fajta != 'cim':
            for m in MOTIVUM_ID.finditer(s.szoveg):
                ki.append(talalat('MOTIVUM_ID', FIGY, s.n, kornyezet(s.szoveg, m),
                                  'motívum-azonosító link nélkül: ' + m.group(1), m.group(1)))
    ki += ell_belso_strong(sorok)
    ki += ell_belso_szerzoseg(sorok)
    return ki


# F123.GENKOR (DT-F181c): a régi „(kézi)” / „(generált)” jelölés a prózát hamisan a kutatónak tulajdonította; a szerzőséget a
# Kolofon mondata adja. A jelölés a lap bármely látható sorában hiba, a Tartalomjegyzékben is (ott állt a hamis magyarázat).
SZERZOSEG_JEL = re.compile(r'\((?:kézi|generált)(?:, ha van)?\)')


def ell_belso_szerzoseg(sorok):
    ki = []
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures', 'proveniencia') or s.szakasz.startswith('Kolofon'):
            continue
        m = SZERZOSEG_JEL.search(kod_nelkul(s.szoveg))
        if m:
            ki.append(talalat('BELSO', BUKAS, s.n, kornyezet(s.szoveg, m), 'szerzőségi jelölés: ' + m.group(0),
                              'szerzoseg'))
    return ki


def ell_belso_strong(sorok):
    """BELSO, Strong-szám (F123.INDOKLAS): a Strong-szám az olvasói prózában, ahol mellette ott a héber/görög szó és a
    kiejtése, jelöletlenül (csupaszon). A mérce az utófeldolgozó `strong_valtozas`-a (amit itt megfog, azt a generátor
    jelölt alakra írja, DT-F181b; a jelölt alak védett, nem hiba); kivétel a táblázat „Strong” oszlopa, a címsor, az
    egyedül vagy láncban álló Strong-szám."""
    import olvasoi_utofeldolg as OU
    olvasoi = {s.n for s in sorok if s.olvasoi and s.fajta != 'cim'}
    ki = []
    for n, regi, uj, generalt in OU.strong_valtozas('\n'.join(s.nyers for s in sorok)):
        if n + 1 not in olvasoi:
            continue
        csupasz_uj = OU.csupasz_strongok(uj)
        for m in re.finditer(OU._STRONG, regi):
            if OU.csupasz_strongok(regi).count(m.group(0)) > csupasz_uj.count(m.group(0)):
                ki.append(talalat('BELSO', BUKAS, n + 1, kornyezet(regi, m),
                                  'Strong-szám a szó és a kiejtése mellett, jelöletlenül: ' + m.group(0)
                                  + ' (a generátor jelölt alakra írja: a lap elavult)', 'strong'))
                break
    return ki


def szakasz_cimek(sorok):
    """{'3': '3. LXX-fordítói döntések', ...} a `## N.` fejlécekből."""
    ki = {}
    for s in sorok:
        if s.fajta == 'cim' and s.szoveg.startswith('## '):
            m = re.match(r'##\s+(\d+)\.\s*(.*)', s.szoveg.strip())
            if m:
                ki.setdefault(m.group(1), m.group(2))
    return ki


def alcimek(sorok):
    """{(`##` szakasz, szám)}: a szakaszon belüli számozott alcímek (`#### 2. Mélységi szócikk`)."""
    ki = set()
    for s in sorok:
        if s.fajta == 'cim' and not s.szoveg.startswith('## '):
            m = re.match(r'#{3,6}\s+(\d+)\.', s.szoveg.strip())
            if m:
                ki.add((s.szakasz, m.group(1)))
    return ki


def ell_pont(sorok):
    cimek = szakasz_cimek(sorok)
    alc = alcimek(sorok)
    ki = []
    rx = re.compile(r'(?<![\d.])(\d+)\.\s*pont\w*\b(?:\s*,\s*[„"]?([A-ZÁÉÍÓÖŐÚÜŰ][\w-]+))?')
    for s in sorok:
        if not s.olvasoi:
            continue
        for m in rx.finditer(s.szoveg):
            szam, nev = m.group(1), m.group(2)
            if (s.szakasz, szam) in alc and not nev:
                continue  # a szakasz saját számozott alpontja (pl. a Szótári háttér „2. pont”-ja)
            if szam not in cimek:
                ki.append(talalat('PONT', BUKAS, s.n, kornyezet(s.szoveg, m),
                                  '„%s. pont”: a lapon nincs %s. szakasz' % (szam, szam)))
            elif nev and nev.lower() not in cimek[szam].lower():
                ki.append(talalat('PONT', BUKAS, s.n, kornyezet(s.szoveg, m),
                                  '„%s. pont, %s”: a lap %s. szakasza „%s”' % (szam, nev, szam, cimek[szam])))
            else:
                ki.append(talalat('PONT', FIGY, s.n, kornyezet(s.szoveg, m),
                                  '„%s. pont”: a lap szakaszait nem pontnak hívja; a forrás saját számozása?' % szam))
    return ki


# F182 (2. fázis; F22 (a), H4 (a), F24 (a)(c), F35): a munkaszavak és munkajelölők listája EGY helyen. A „próba” csak önálló
# szóként („próbatétel” nem); a „független” csak a közös bemenetű keresésről (F24 (a)); a mért BDB-pontosság csak a
# módszertani dokumentációban áll (F35, DT733). A generátor új szerkezetű lapon olvasói alakra írja át ezeket
# (`lexikon_general.UJ_OLVASOI_MUNKASZO`); a régi lapok a saját teljes folyamatukban.
MUNKASZAVAK = [
    (re.compile(r'\bpróba(?:ként|jelleg\w*|i)?\b', re.I), 'munkajelölő (próba)'),
    (re.compile(r'\bjavaslat\w*', re.I), 'munkajelölő (javaslat)'),
    (re.compile(r'ellenőrzendő', re.I), 'munkajelölő (ellenőrzendő)'),
    (re.compile(r'függőben', re.I), 'munkajelölő (függőben)'),
    (re.compile(r'nincs bekötve', re.I), 'munkajelölő (nincs bekötve)'),
    (re.compile(r'kutatói jelölés', re.I), 'munkajelölő (kutatói jelölés)'),
    (re.compile(r'azonosításra vár', re.I), 'munkajelölő (azonosításra vár)'),
    (re.compile(r'\bD-minta'), 'munkaszó (D-minta)'),
    (re.compile(r'\bQ\d-fegyelem'), 'munkaszó (Q-fegyelem)'),
    (re.compile(r'\bstudy\b', re.I), 'munkaszó (study)'),
    (re.compile(r'\baudit\w*', re.I), 'munkaszó (audit)'),
    (re.compile(r'\btoken\w*', re.I), 'munkaszó (token)'),
    (re.compile(r'↳\s*Alpont:'), 'belső címke (↳ Alpont:)'),
    (re.compile(r'független\w*\s+keresés\w*', re.I), 'közös bemenetű keresések „független”-ként (F24 (a))'),
    (re.compile(r'[Mm]ért pontosság'), 'mért BDB-pontosság a lapon (F35: csak a módszertani dokumentációban)'),
    # F212 (N-F206a; a sablonmondat-lista M1–M14, A1 osztálya, a felhasználó döntése: „javaslat szerint”): a generált
    # műhelyszavak — második előfordulás, gépi védelem
    (re.compile(r'\bhígul\w*', re.I), 'munkaszó (hígul…)'),
    (re.compile(r'séma-korlát\w*', re.I), 'munkaszó (séma-korlát)'),
    (re.compile(r'Strong-keresés|\bmintakeresés'), 'munkaszó (keresés neve)'),
    (re.compile(r'\blánc-?vers\w*'), 'munkaszó (láncvers)'),
    (re.compile(r'Peshat-mag'), 'munkaszó (Peshat-mag)'),
    (re.compile(r'\balapvonal\w*'), 'munkaszó (alapvonal)'),
    (re.compile(r'\b[Cc]ell(?:a|ája|ában|ák|ákban)\b|-cella\b'), 'munkaszó (cella)'),
    (re.compile(r'kinyerő tábl\w*'), 'munkaszó (kinyerő tábla)'),
    (re.compile(r'\bVotes\b'), 'munkaszó (Votes)'),
    (re.compile(r'versenkénti kereséssel'), 'munkaszó (versenkénti keresés)'),
    (re.compile(r'modell emeli ki|másik kéz'), 'munkaszó (munkamenet)'),
    (re.compile(r'még nem történt meg'), 'munkaszó (munkaállapot)'),
    (re.compile(r'renderidej\w*'), 'munkaszó (renderidejű)'),
    (re.compile(r'Dice-társulás\w*|\bszóillesztés\w*'), 'munkaszó (mérési zsargon)'),
    (re.compile(r'teljesség-mérés\w*'), 'munkaszó (teljesség-mérés)'),
    (re.compile(r'\w+-háló\b|szó háló\b'), 'munkaszó (háló)'),
    (re.compile(r'\bProveniencia\b'), 'munkaszó (Proveniencia)'),
    (re.compile(r'Kutatói megjegyzés'), 'munkaszó (Kutatói megjegyzés)'),
    (re.compile(r'\*Generált:'), 'munkaszó (Generált:)'),
    (re.compile(r'\bEz a blokk\b|\b(?:sorát|jelöltjét|tokenjét) fedi\b'), 'munkaszó (blokk-hatókör)'),
    (re.compile(r'\(HCF: \d+\)'), 'munkaszó (adatbázis-azonosító)'),
    (re.compile(r'Összesítő sor \d+'), 'munkaszó (összesítő sor)'),
    (re.compile(r'LSJ-sor|jelölt hiány'), 'munkaszó (szerepmátrix)'),
    (re.compile(r'[Cc]sak megjelenítés'), 'munkaszó (csak megjelenítés)'),
    (re.compile(r'gépi (?:Strong-|lánc-|szópár-|frázis-)?keresés|gépi teljesség|gépi illesztés'), 'munkaszó (gépi …)'),
]


# F182 (3. menet): a nyers mezőnév és a belső jel mintái egy helyen (a generátor olvasói átírása:
# `lexikon_general.jelolt_labjegyzet_olvasoi`, `_olvasoi_resz`, `kesz_lap_utana`)
NYERS_JELEK = [
    (re.compile(r'\bproveniencia\s*:', re.I), 'nyers mezőnév (proveniencia:)'),
    (re.compile(r'\bigazolas\s*:'), 'nyers mezőnév (igazolas:)'),
    (re.compile(r'\bjelentes_szam\b'), 'nyers mezőnév (jelentes_szam)'),
    (re.compile(r'\bkaroli_szo\b'), 'nyers mezőnév (karoli_szo)'),
    (re.compile(r'\bsorszám \d+(?:, \d+)*\)'), 'nyers sorszám a forrásmegjelölésben'),
    (re.compile(r'\bnapló:\s'), 'napló-hivatkozás'),
    (re.compile(r'\(\d+(?:/[a-z])?\. rész\)'), 'napló-szakasz utalása („(7. rész)”, „(4/b. rész)”)'),
    (re.compile(r'\bcsatorna='), 'nyers mezőnév (csatorna=)'),
    (re.compile(r'\bszamozas_elteres\b'), 'nyers mezőérték (szamozas_elteres)'),
    (re.compile(r'\bforras_kereses\b'), 'nyers mezőnév (forras_kereses)'),
    (re.compile(r'\b(?:halo|blokk|osztaly)='), 'belső keresési jel'),
    (re.compile(r'\blanc ±\d'), 'belső keresési jel (lanc)'),
    (re.compile(r'\bcsalad [HG]\d{4}'), 'belső keresési jel (csalad)'),
    (re.compile(r'indoklás \(nyers\)'), 'nyers indoklás'),
    (re.compile(r'szónézet: /szo/'), 'nyers szónézet-útvonal'),
    (re.compile(r'(?<![\w/])(?:kt|other|names)/[a-z]'), 'tW-azonosító'),
    (re.compile(r'(?<=[֐-׿יִ-ﭏ\]])\u200e?_\d+\b'), 'a címszó belső számlálója'),
    (re.compile(r'(?<![\w./-])(?:adat|konkordancia|naplok|eszkozok)/\w'), 'a repó belső útvonala'),
]


def ell_nyers_jel(sorok):
    if not KIVETEL_NELKUL:
        return []
    ki = []
    for s in sorok:
        if not s.olvasoi:
            continue
        for rx, nev in NYERS_JELEK:
            for m in rx.finditer(s.szoveg):
                ki.append(talalat('NYERS_JEL', BUKAS, s.n, kornyezet(s.szoveg, m), nev + ': ' + m.group(0),
                                  nev + m.group(0)))
    return ki


# első személyű többes számú múlt idejű igealak (a névutós személyragos alakok nélkül: alattuk, közöttük …)
MI_HANG_RX = re.compile(r'(?<![\w-])([a-záéíóöőúüű]+(?:[lnrsztv]t|tt)(?:ük|uk|ünk|unk))(?![\w-])')
MI_HANG_KIVETEL = {'alattuk', 'felettük', 'fölöttük', 'közöttük', 'között', 'mellettük', 'előttük', 'mögöttük',
                   'körülöttük', 'helyettük', 'miattuk', 'értük', 'velük', 'nélkülük', 'rajtuk', 'bennük', 'tőlük'}
IDEZET_KI_RX = re.compile(r'„[^”]*”|"[^"]*"|\*[^*]+\*')


def ell_mi_hang(sorok):
    if not KIVETEL_NELKUL:
        return []
    ki = []
    for s in sorok:
        if not s.olvasoi:
            continue
        t = IDEZET_KI_RX.sub(' ', s.szoveg)
        # F182 javítókör (DT760): az 1.2 alcím névszói („A keresés forrásai”), kivétel nincs
        for m in MI_HANG_RX.finditer(t):
            if m.group(1).lower() in MI_HANG_KIVETEL:
                continue
            ki.append(talalat('MI_HANG', BUKAS, s.n, kornyezet(t, m), '„mi”-hangú igealak: ' + m.group(1), m.group(1)))
    return ki


NEVELO_RX = re.compile(r'(?<![\w.-])[Aa] (?=[aáeéiíoóöőuúüű][a-záéíóöőúüű])')


def ell_nevelo(sorok):
    if not KIVETEL_NELKUL:
        return []
    ki = []
    for s in sorok:
        if not s.olvasoi:
            continue
        t = IDEZET_KI_RX.sub(' ', s.szoveg)
        for m in NEVELO_RX.finditer(t):
            ki.append(talalat('NEVELO', BUKAS, s.n, kornyezet(t, m), '„a” magánhangzó előtt', t[m.start():m.start() + 12]))
    return ki


KOV_RX = re.compile(r'\*\*Következtetés:\*\*\s*([^.]*\.)')
KOV_ISM_MAX = 2


def ell_kov_ism(sorok):
    if not KIVETEL_NELKUL:
        return []
    ki, db = [], {}
    for s in sorok:
        if not s.olvasoi:
            continue
        for m in KOV_RX.finditer(s.szoveg):
            kulcs = (s.szakasz, re.sub(r'\d+', 'N', m.group(1)))
            db.setdefault(kulcs, []).append(s.n)
    for (szak, mondat), nn in db.items():
        if len(nn) > KOV_ISM_MAX:
            ki.append(talalat('KOV_ISM', BUKAS, nn[0], mondat[:120],
                              'ugyanaz a következtetés %d-szor a(z) „%s” szakaszban' % (len(nn), szak), mondat))
    return ki


# F182 javítókör (ELLENOR_F182 #8; A05, A06, B08): az indoklás-cella olvasói alakja. Egy írásfutam (héber vagy görög
# szó, szókapcsolat; „A + B”, „A, B”, „A … B” egy csoport) után zárójeles vagy vesszős kiejtés áll („(chámász)”,
# „(φθορά, fthora)”, „(adámá: föld)”); a jelölt Strong-szám („עֶצֶב H6089 (ecev)”) közbeállhat.
INDOKLAS_CELLA_RX = re.compile(r'\*\*(?:elutasítva|beépítve|nyitva)\*\*')
INDOK_FEJLEC_RX = re.compile(r'^\|\s*Igehely\s*\|\s*Miért lett jelölt\s*\|\s*(?:Döntés és indok|Indok)\s*\|')
_IRAS_BETU = '\u0590-\u05FF\uFB1D-\uFB4F\u0370-\u03FF\u1F00-\u1FFF'
IRAS_FUTAM_RX = re.compile(r'[%s](?:[%s\u05BE׳״]|[ ](?=[%s]))*' % (_IRAS_BETU, _IRAS_BETU, _IRAS_BETU))
IRAS_LANC_RX = re.compile(r'\s*(?:\+|,|/|\.\.\.|…)\s*(?=[%s])' % _IRAS_BETU)
IRAS_KIEJTES_RX = re.compile(r'(?: [HG]\d{4}[a-z]?)?\s*(?:\(|,|:)\s*[a-zA-ZáéíóöőúüűÁÉÍÓÖŐÚÜŰ\'’]')
INDOKLAS_TILOS = (
    (re.compile(r'sorának folytatása|[Uu]gyanaz az indok,? mint'), 'más sorra hivatkozik'),
    (re.compile(r'érdemes lehet|külön vizsgálatra'), 'munkajavaslat az olvasói szövegben'),
)


def iras_kiejtes_nelkul(t):
    """[írásfutam]: a szövegben kiejtés nélkül álló héber/görög szó vagy szókapcsolat."""
    ki, i = [], 0
    while True:
        m = IRAS_FUTAM_RX.search(t, i)
        if not m:
            return ki
        v = m.end()
        while True:
            lanc = IRAS_LANC_RX.match(t, v)
            m2 = IRAS_FUTAM_RX.match(t, lanc.end()) if lanc else None
            if not m2:
                break
            v = m2.end()
        if not IRAS_KIEJTES_RX.match(t, v):
            ki.append(t[m.start():v])
        i = v


def ell_indoklas(sorok):
    if not KIVETEL_NELKUL:
        return []
    ki = []
    indok_tabla = False
    for s in sorok:
        # F212 (I5): az elutasított sor cellája jel nélkül áll („| Igehely | Miért lett jelölt | Indok |” tábla); az
        # indoklás-cella a fejlécről is megtalálható, így a kapu a jel elhagyásával nem gyengül
        if INDOK_FEJLEC_RX.match(s.szoveg):
            indok_tabla = True
            continue
        if not s.szoveg.startswith('|'):
            indok_tabla = False
        if not s.olvasoi:
            continue
        m = INDOKLAS_CELLA_RX.search(s.szoveg)
        if m:
            t = s.szoveg[m.end():]
        elif indok_tabla and not s.szoveg.startswith('|---'):
            cellak = s.szoveg.strip().strip('|').split('|')
            if len(cellak) < 3:
                continue
            t = '|'.join(cellak[2:])
        else:
            continue
        for f in iras_kiejtes_nelkul(t):
            ki.append(talalat('INDOKLAS', BUKAS, s.n, f, 'írás kiejtés nélkül az indoklásban', f))
        for rx, nev in INDOKLAS_TILOS:
            for mm in rx.finditer(t):
                ki.append(talalat('INDOKLAS', BUKAS, s.n, kornyezet(t, mm), nev, mm.group(0)))
    return ki


def ell_munkaszo(sorok):
    ki = []
    suly = BUKAS if KIVETEL_NELKUL else FIGY
    for s in sorok:
        if not s.olvasoi:
            continue
        for rx, nev in MUNKASZAVAK:
            for m in rx.finditer(s.szoveg):
                ki.append(talalat('MUNKASZO', suly, s.n, kornyezet(s.szoveg, m), nev + ': ' + m.group(0),
                                  nev + m.group(0).lower()))
    return ki


# F203 (orkesztrátori hatókör-bővítés, 2026-11-12; DT-F203b): a hivatkozás-rövidítés („c.” caput, „p.” pagina, „§”) utáni szám
# forrás-hivatkozás, nem a lap szakasza (G2671: „Protevangelium Jacobi, c. 3. (Aiszkhülosz, …)” — hamis BUKÁS volt)
SZAKASZ_HIV_NEV = re.compile(r'(?<![\d.:])(?<!\bc\. )(?<!\bp\. )(?<!§ )(\d{1,2})\.\s*\(([A-ZÁÉÍÓÖŐÚÜŰ][^)]{1,60})\)')
SZAKASZ_HIV_SZO = re.compile(r'(?<![\d.:])(\d{1,2})\.\s*szakasz\w*(?:\s*\(([A-ZÁÉÍÓÖŐÚÜŰ][^)]{1,60})\))?')
SZAKASZ_HIV_CIMSZO = re.compile(r'(?<![\d.:])(\d{1,2})\.\s+([A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{3,})')
SZAKASZ_HIV_IDEGEN = re.compile(r'(?:BDB|Thayer|szócikk\w*|szótár\w*)[^.;]{0,25}$')


HELYORZO_RX = re.compile(r'<KANONIKUS_FORRAS_URL>|\[HELYŐRZŐ[^\]]*\]|<DOI>|DOI:\s*[.`]?\s*$|DOI:\s*\.')


def ell_helyorzo(sorok):
    """A felhasználó döntései (2026-11-11): az új szerkezetű lapon nyers helyőrző nem állhat (a megjegyzés kivétel)."""
    if not KIVETEL_NELKUL:
        return []
    ki = []
    for s in sorok:
        if s.fajta in ('komment', 'kod'):
            continue
        m = HELYORZO_RX.search(s.szoveg)
        if m:
            ki.append(talalat('HELYORZO', BUKAS, s.n, kornyezet(s.szoveg, m), 'nyers helyőrző a lapon: „%s”' % m.group(0)))
    return ki


# Névelő a lista- és táblaelem elején (lap-javit HAMART-001, orkesztrátori tétel, a felhasználó: „pedig ezt külön
# megjelöltük” — második előfordulás; LISTA_NEVELO): a forrásnév a listában és a táblacellában névelő nélkül áll („BDB-szótár
# (közkincs)”, nem „a BDB-szótár (közkincs)”); a névelőt csak a folyó szöveg teszi elé. A kisbetűs „a”/„az” a
# névtöredék jele; a nagybetűs „A”/„Az” mondatkezdő listaelem (pl. a Nyitott kérdések pontjai), az megengedett.
NEVELO_ELEM_RX = re.compile(r'^(?:\*\*|\*|\[|`)?(?:a|az)\s')
NEVELO_LISTA_RX = re.compile(r'^\s*(?:[-*]|\d+\.)\s+(.*)$')


def ell_lista_nevelo(sorok):
    if not KIVETEL_NELKUL:
        return []
    ki = []
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures', 'cim'):
            continue
        t = re.sub(r'<!--.*?-->', '', s.nyers).strip()
        elemek = []
        if t.startswith('|'):
            if re.match(r'^\|[\s:|-]+\|$', t):
                continue
            elemek = [c.strip() for c in re.split(r'(?<!\\)\|', t.strip('|'))]
        else:
            m = NEVELO_LISTA_RX.match(t)
            if m:
                elemek = [m.group(1).strip()]
        for e in elemek:
            if NEVELO_ELEM_RX.match(e):
                ki.append(talalat('LISTA_NEVELO', BUKAS, s.n, e[:80], 'a lista- vagy táblaelem névelővel kezdődik: a név '
                                  'névelő nélkül álljon, a névelőt csak a folyó szöveg teszi elé'))
    return ki


# A motívum meghatározása (a felhasználó, 2026-11-11: „hiányolom a motívum definíciót … a kolofonban is és az elején”):
# az új szerkezetű lapon a „**A motívum.**” bekezdés nem üres, nem a cím, és nem csak az azonosság típusának mondata;
# a Kolofonban „Meghatározás” sor áll, értékkel.
AZONOSSAG_MONDAT_RX = re.compile(r'(?:Szavas|Fordulat-|Utalás-|Fogalmi|Szerkezeti) ?motívum: [^.]*\.')
MEGHATAROZAS_MIN_SZO = 8


def ell_meghatarozas(sorok):
    if not KIVETEL_NELKUL:
        return []
    ki = []
    cim = next((re.sub(r'^#\s+(?:\S+\s+)?[\w-]+\s+—\s+', '', s.nyers.strip()) for s in sorok
                if s.nyers.startswith('# ')), '')
    bek = next((s for s in sorok if s.nyers.strip().startswith('**A motívum.**')), None)
    if bek is None:
        ki.append(talalat('MEGHATAROZAS', BUKAS, 1, '', 'a lap elején nincs „A motívum.” bekezdés'))
    else:
        t = bek.nyers.strip()[len('**A motívum.**'):].strip()
        marad = AZONOSSAG_MONDAT_RX.sub('', t).strip()
        if not t or t.rstrip('.') == cim.rstrip('.') or len(marad.split()) < MEGHATAROZAS_MIN_SZO \
                or marad.rstrip('.') == cim.rstrip('.'):
            ki.append(talalat('MEGHATAROZAS', BUKAS, bek.n, t[:80], '„A motívum.” bekezdés üres, a címet ismétli, vagy '
                              'csak az azonosság típusát mondja: a motívum meghatározása hiányzik'))
    kol = [s for s in sorok if s.szakasz.startswith('Kolofon') and re.match(r'^\|\s*Meghatározás\s*\|', s.nyers.strip())]
    if not kol or not re.sub(r'[\s|—-]', '', kol[0].nyers.strip()[len('| Meghatározás'):]):
        ki.append(talalat('MEGHATAROZAS', BUKAS, kol[0].n if kol else 1, '', 'a Kolofonban nincs „Meghatározás” sor értékkel'))
    return ki


def ell_szakasz_hiv(sorok):
    """F22 (b): az új szerkezetű lap „N. szakasz” és „N. (Név)” hivatkozása a lap tényleges szakaszára mutat."""
    if not KIVETEL_NELKUL:
        return []
    cimek = szakasz_cimek(sorok)
    elso_szavak = {re.split(r'[\s-]', c)[0].lower()[:6] for c in cimek.values() if c}
    ki = []
    for s in sorok:
        if not s.olvasoi or s.fajta == 'cim':
            continue
        # „a 6. Értelmezésben”: szám + a lap valamelyik szakaszcímének első szava (zárójel nélkül)
        for m in SZAKASZ_HIV_CIMSZO.finditer(s.szoveg):
            szo = m.group(2).lower()[:6]
            if szo not in elso_szavak or SZAKASZ_HIV_IDEGEN.search(s.szoveg[:m.start()]):
                continue
            if m.group(1) not in cimek or not cimek[m.group(1)].lower().startswith(szo):
                ki.append(talalat('SZAKASZ_HIV', BUKAS, s.n, kornyezet(s.szoveg, m),
                                  '„%s”: a lap %s. szakasza „%s”' % (m.group(0).strip(), m.group(1),
                                                                     cimek.get(m.group(1), '—'))))
        for rx in (SZAKASZ_HIV_NEV, SZAKASZ_HIV_SZO):
            for m in rx.finditer(s.szoveg):
                szam, nev = m.group(1), m.group(2)
                if SZAKASZ_HIV_IDEGEN.search(s.szoveg[:m.start()]):
                    continue    # a BDB vagy a szócikk saját szakasza
                if szam not in cimek:
                    ki.append(talalat('SZAKASZ_HIV', BUKAS, s.n, kornyezet(s.szoveg, m),
                                      '„%s”: a lapon nincs %s. szakasz' % (m.group(0).strip(), szam)))
                elif nev and not cimek[szam].lower().startswith(nev.split(' ')[0].lower()[:6]):
                    ki.append(talalat('SZAKASZ_HIV', BUKAS, s.n, kornyezet(s.szoveg, m),
                                      '„%s”: a lap %s. szakasza „%s”' % (m.group(0).strip(), szam, cimek[szam])))
    return ki


def ell_angol(sorok):
    ki = []
    for s in sorok:
        if not s.olvasoi or s.szakasz.startswith(IRODALOM):
            continue
        t = kod_nelkul(s.szoveg)
        m = ANGOL_SZO.search(t)
        if m:
            ki.append(talalat('ANGOL', BUKAS, s.n, kornyezet(t, m), 'angol maradék / zsargon: ' + m.group(0),
                              m.group(0).lower()))
        fsz = ANGOL_FUNKCIO.findall(t)
        if len(fsz) >= ANGOL_SOR_MIN:
            ki.append(talalat('ANGOL_SOR', FIGY, s.n, t[:140], '%d angol funkciószó (%s)' % (
                len(fsz), ', '.join(sorted(set(fsz))))))
    return ki


def ell_idezojel(sorok):
    ki = []
    for s in sorok:
        if not s.olvasoi:
            continue
        t = re.sub(r'<[^>]+>', '', kod_nelkul(s.szoveg))
        if '"' in t:
            i = t.index('"')
            ki.append(talalat('IDEZOJEL', BUKAS, s.n, t[max(0, i - 50):i + 60],
                              'egyenes " a magyar szövegben (a „…” helyett)', 'egyenes'))
    return ki


HEBER_SZO = r'[א-תיִ-ﭏ][֑-ׇא-תיִ-ﭏ]*'
GOROG_SZO = r'[Ͱ-Ͽἀ-῿]+'
PAR_RX = re.compile(r'((?:%s|%s)(?:[\s־]+(?:%s|%s))*)\s*\(([^()]{1,80})\)' % (
    HEBER_SZO, GOROG_SZO, HEBER_SZO, GOROG_SZO))


def heber_kulcs(szo):
    if re.search(r'[֐-׿]', szo):
        return re.sub('[֑-ֽ֯׀׃]', '', szo)
    return ekezet_nelkul(szo.lower())


def kiejtes_parok(sorok):
    """[(héber/görög kulcs, kiejtés, sor)] a lapon álló „szó (kiejtés)” párokból."""
    egy, tobb = [], []
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures'):
            continue
        for m in PAR_RX.finditer(s.szoveg):
            szavak = [heber_kulcs(w) for w in re.split(r'[\s־]+', m.group(1)) if w]
            belso = re.sub(r'\b[HG]\d{3,5}[a-z]?\b', ' ', m.group(2))
            belso = re.sub(r'[*_;,]', ' ', belso.split(':')[0])
            kiejt = [w.lower().strip("-'’") for w in re.split(r'[\s]+', belso) if w]
            if len(szavak) != len(kiejt) or not all(re.match(r"^[A-Za-zÁ-ž'’ʼ-]+$", w) for w in kiejt):
                continue
            (egy if len(szavak) == 1 else tobb).append((szavak, kiejt, s.n, m.group(0)))
    ki = [(sz[0], k[0], n, idez) for sz, k, n, idez in egy]
    ismert = {(sz[0], k[0]) for sz, k, _, _ in egy}
    for szavak, kiejt, n, idez in tobb:
        # a szótárak angol szövegében a héber szócsoport fordított (vizuális) sorrendben is állhat: azt az
        # irányt fogadjuk el, amelyik több egyszavas párral egyezik
        elore = sum((h, k) in ismert for h, k in zip(szavak, kiejt))
        hatra = sum((h, k) in ismert for h, k in zip(reversed(szavak), kiejt))
        if hatra > elore:
            szavak = list(reversed(szavak))
        ki += [(h, k, n, idez) for h, k in zip(szavak, kiejt)]
    return ki


def ell_atiras(sorok):
    ki = []
    parok = kiejtes_parok(sorok)
    by = {}
    for kulcs, k, n, idez in parok:
        by.setdefault(kulcs, {}).setdefault(k, []).append((n, idez))
    for kulcs, valt in by.items():
        if len(valt) > 1:
            elso = sorted((v[0][0], k, v[0][1]) for k, v in valt.items())
            ki.append(talalat('ATIRAS', BUKAS, elso[1][0], ' · '.join(x[2] for x in elso[:3]),
                              'egy szó %d kiejtéssel: %s' % (len(valt), ', '.join(
                                  '%s (sor %d)' % (k, n) for n, k, _ in elso))))
    # a lapon álló kiejtések ékezet-eltérő változata dőlt vagy zárójeles helyen (pl. hádész / hadész, tohu)
    ismert = {}
    for kulcs, k, n, _ in parok:
        if len(ekezet_nelkul(k)) >= 4 and k != ekezet_nelkul(k):
            ismert.setdefault(ekezet_nelkul(k), set()).add(k)
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures', 'karoli') or s.szakasz.startswith(KIZART_SZAKASZ):
            continue  # a Károli-vers alakja („Seol”) nem a lap kiejtése
        if s.alszakasz.startswith('Háttér: rokon nyelvek'):
            continue  # F182 (A22): a rokon nyelvi alak (arab, arámi) más szó, saját kiejtéssel; nem a héber szó változata
        reszek = re.findall(r'(?<!\*)\*([^*]+)\*(?!\*)|\(([^()]*)\)', s.szoveg)
        for dolt, zar in reszek:
            for w in re.findall(r'[A-Za-zÁ-ž]+', dolt or zar):
                wk = w.lower()
                alap = ekezet_nelkul(wk)
                if alap in ismert and wk not in ismert[alap]:
                    ki.append(talalat('ATIRAS_VALT', FIGY, s.n, s.szoveg[:140],
                                      '„%s” — a lapon máshol: %s' % (w, ', '.join(sorted(ismert[alap]))), wk))
    return ki


# a magyar rövidítés pont nélküli; a ponttal álló alak (Lob. Path. Element. 2:6) bibliográfia
KONYV_RX = re.compile(r'(?<![\w./#-])((?:[1-5]\s?)?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,6})\s(\d{1,3})[:,](\d{1,3})')
SZOTAR_ALAK = re.compile(r'(?:BDB|Thayer|szótár)-?(?:ben|ban)?:\s*„$')  # a szótár saját alakját szó szerint idézi


# a normalizáló tábla csak a 66 könyvet tartja; a deuterokanonikus és pszeudepigráf könyvek rövidítése nem hiba
DEUTERO = {'Tób', 'Jud', 'Bölcs', 'Sir', 'Bár', '1Makk', '2Makk', '3Makk', '4Makk', 'Énokh', '1Énokh', 'Jub'}
NEM_KONYV = {'Az', 'A', 'Lásd', 'Vö'}  # mondatkezdő névelő/utalószó egy könyv nélküli fejezet:vers előtt


def ell_konyv(sorok):
    hu = konyvek()[0] | DEUTERO | NEM_KONYV
    ki = []
    for s in sorok:
        if not s.olvasoi and s.fajta != 'dolt':
            continue
        if s.szakasz.startswith(KIZART_SZAKASZ):
            continue
        t = kod_nelkul(s.szoveg)
        # F183 (K67f): a szakirodalom bibliográfiai címe az eredeti alakjában áll (pl. „(Gen 6:5–9:17)”), nem olvasói
        # igehely-hivatkozás; a 12. Irodalom „Szakirodalom” listájának DOI-s sorai kivételek
        if s.szakasz.startswith('12. Irodalom') and 'DOI: 10.' in t:
            continue
        for m in KONYV_RX.finditer(t):
            if m.group(1) not in hu and not SZOTAR_ALAK.search(t[max(0, m.start() - 20):m.start()]):
                ki.append(talalat('KONYV', BUKAS, s.n, kornyezet(s.szoveg, m, 30),
                                  'könyvrövidítés nem a normalizáló tábla alakjával: „%s”' % m.group(1), m.group(1)))
    return ki


def ell_bdb(sorok):
    ki = []
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures', 'proveniencia') or s.szakasz.startswith(KIZART_SZAKASZ):
            continue
        t = kod_nelkul(s.szoveg)
        for rx, nev in BDB_JEL:
            m = rx.search(t)
            if m:
                ki.append(talalat('BDB_JEL', BUKAS, s.n, kornyezet(t, m, 40), nev, nev))
        if s.fajta in ('labjegyzet', 'dolt', 'tabla'):
            for r in (t.split('|') if s.fajta == 'tabla' else [t]):
                if zarojel_nyitva(r):
                    ki.append(zarojel_talalat(s, r))
                    break
    for s, b in bekezdesek(sorok):
        if not s.szakasz.startswith(KIZART_SZAKASZ) and zarojel_nyitva(kod_nelkul(b)):
            ki.append(zarojel_talalat(s, kod_nelkul(b)))
    return ki


def zarojel_nyitva(r):
    return r.count('(') > r.count(')')


def zarojel_talalat(s, r):
    i = r.rfind('(')
    szotar = s.szakasz.startswith(SZOTARI_SZAKASZ)
    return talalat('ZAROJEL', BUKAS if szotar else FIGY, s.n, r[max(0, i - 60):i + 60], 'nyitva maradt zárójel')


def elso_tabla(sorok, szakasz_kezd):
    """Az adott szakasz első táblája: (fejléc-cellák, [(sor, cellák)])."""
    fej, ki = None, []
    for s in sorok:
        if not s.szakasz.startswith(szakasz_kezd):
            if fej:
                break
            continue
        if s.fajta == 'tabla':
            cellak = [c.strip() for c in s.szoveg.strip().strip('|').split('|')]
            if fej is None:
                fej = cellak
            elif not all(re.match(r'^:?-+:?$', c) for c in cellak if c):
                ki.append((s.n, cellak))
        elif fej is not None and s.fajta != 'ures':
            break
    return fej, ki


def ell_funkcio(sorok):
    fej, tabla = elso_tabla(sorok, ELOFORDULAS_SZAKASZ)
    if not fej:
        return []
    oszl = next((i for i, c in enumerate(fej) if c.startswith('Funkció')), None)
    if oszl is None:
        return [talalat('FUNKCIO_URES', BUKAS, 0, ' | '.join(fej), 'az 1. táblában nincs „Funkció” oszlop')]
    ki = []
    for n, cellak in tabla:
        if oszl >= len(cellak) or cellak[oszl].strip(' *') in ('', '—', '-', '–'):
            ki.append(talalat('FUNKCIO_URES', BUKAS, n, cellak[0], 'üres „Funkció” cella', 'ures'))
    return ki


IDEZET_RX = re.compile(r'(\(?)\s*(?:„([^”"]+)[”"]|"([^"]+)")')


def blokkok_1a(sorok):
    """[(igehely, sor, Károli-vers, [prózasorok])] az 1/a részből."""
    ki, akt = [], None
    for s in sorok:
        if not s.alszakasz.startswith('1/a') and not s.szakasz.startswith('1/a'):
            if akt:
                ki.append(akt)
                akt = None
            continue
        m = re.match(r'^\*\*([^*]+\d+:\d+[^*]*)\*\*\s*$', s.szoveg.strip())
        if m:
            if akt:
                ki.append(akt)
            akt = [m.group(1).strip(), s.n, '', []]
        elif akt is not None and s.fajta in ('karoli', 'dolt') and not akt[3]:
            # a tartomány-sor (pl. 1Móz 4:2-3) minden verse külön dőlt Károli-sor (a második már 'dolt' fajtájú):
            # az idézet bármelyikből jöhet
            akt[2] = (akt[2] + ' ' + s.szoveg.strip().strip('*')).strip()
        elif akt is not None and s.fajta == 'proza':
            akt[3].append(s)
    if akt:
        ki.append(akt)
    return ki


IDEZET_SZO_HASONLOSAG = 0.75  # szavanként: a modernizált helyesírás (setétség → sötétség) még egyezik
# darabonként a kihagyott versszavak legfeljebb ennyiszerese az idézett szavaknak (pl. „felfakadának [ezen a napon]
# a nagy mélység [minden] forrásai”); minden idézett szónak sorrendben egyeznie kell, ezért ez nem enged át parafrázist
IDEZET_KIHAGYAS = 1


def szo_egyezik(a, b):
    return a == b or difflib.SequenceMatcher(None, a, b).ratio() >= IDEZET_SZO_HASONLOSAG


def karoli_egyezik(idez, karoli_normal):
    """Az idézet a Károli-vers szövege-e: minden „…”-tal elválasztott darabja a vers szavait sorrendben követi,
    szavanként tűréssel (a Károli régies helyesírása), a darab szószámával arányos kihagyással.
    A más igealak vagy más szó (kihirdetem ↔ kiáltom) saját fordítás."""
    vers = karoli_normal.split()
    for darab in re.split(r'\.\.\.|…|\[[^\]]*\]', idez):
        szavak = normal_szoveg(darab).split()
        if not szavak:
            continue
        keret = IDEZET_KIHAGYAS * len(szavak)
        if not any(illeszt(szavak, vers, 0, k, 0, keret) for k in range(len(vers))):
            return False
    return True


def illeszt(q, v, qi, vi, kihagy, keret):
    """A q[qi:] szavai a v[vi:]-ben sorrendben, összesen legfeljebb `keret` kihagyott versszóval."""
    if qi == len(q):
        return True
    if vi == len(v):
        return False
    if szo_egyezik(q[qi], v[vi]) and illeszt(q, v, qi + 1, vi + 1, kihagy, keret):
        return True
    return qi > 0 and kihagy < keret and illeszt(q, v, qi, vi + 1, kihagy + 1, keret)


def ell_idezet(sorok):
    ki = []
    for ige, _, karoli, proza in blokkok_1a(sorok):
        if not karoli:
            continue
        kn = normal_szoveg(karoli)
        for s in proza:
            if re.match(r'^Funkció\s*:', s.szoveg.strip()):
                continue
            for m in IDEZET_RX.finditer(s.szoveg):
                if m.group(1):  # zárójeles glossza egy héber szó után: nem versidézet
                    continue
                idez = m.group(2) or m.group(3)
                if len(normal_szoveg(idez).split()) < 3:
                    continue
                if karoli_egyezik(idez, kn):
                    continue
                if re.search(r'saját fordítás|sajat forditas|szó szerint:|ford\.\s*:', s.szoveg, re.I):
                    continue
                ki.append(talalat('IDEZET', BUKAS, s.n, '%s: „%s”' % (ige, idez),
                                  'az idézet nem a fölötte álló Károli-vers szövege, és nincs „saját fordítás” jelölés'))
    return ki


def elofordulas_szamok(sorok):
    """Az 1. tábla sorai: (összes, ÓSZ, ÚSZ)."""
    _, tabla = elso_tabla(sorok, ELOFORDULAS_SZAKASZ)
    _, _, usz = konyvek()
    ossz = len(tabla)
    u = 0
    for _, c in tabla:
        m = re.match(r'\[?((?:[1-5])?[^\s\]]+)\s', c[0])
        if m and m.group(1) in usz:
            u += 1
    return ossz, ossz - u, u


def lxx_osszesites(sorok):
    for s in sorok:
        if s.szakasz.startswith('3. LXX') and 'Összesítés:' in s.szoveg:
            return {k.strip(): int(v) for k, v in re.findall(r'([\wáéíóöőúüű -]+)=(\d+)', s.szoveg)}
    return None


def szam_ertek(szo):
    szo = szo.lower()
    if szo.isdigit():
        return int(szo)
    return SZAMNEV.get(szo)


def ell_kivonat(sorok):
    ossz, osz, usz = elofordulas_szamok(sorok)
    if not ossz:
        return []
    lxx = lxx_osszesites(sorok)
    ki = []
    szam = r'(\d+|%s)' % '|'.join(sorted((re.escape(k) for k in SZAMNEV), key=len, reverse=True))
    for s in sorok:
        if not s.szakasz.startswith('Kivonat') or s.fajta != 'proza' or s.nyers.rstrip().endswith('<!-- olvasói -->'):
            continue
        for mondat in re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÖŐÚÜŰ„])', s.szoveg):
            lxx_m = re.search(r'Septuaginta|LXX|görög fordítás', mondat)
            for m in re.finditer(r'\b%s\s+(?:\S+\s+){0,2}?[\w-]*?%s' % (szam, SZAM_FONEV), mondat, re.I):
                n = szam_ertek(m.group(1))
                if n is None:
                    continue
                fonev = m.group(0).lower()
                # a testamentum: a darabszó saját jelzője, vagy a mondatban előtte álló utolsó testamentum-szó
                # csak a főnév („az Újszövetségben”); a jelzői „újszövetségi folytatás” nem szűkít
                elotte = re.findall(r'Újszövetség(?!i)|Ószövetség(?!i)', mondat[:m.start()])
                testamentum = 'ú' if 'újszövetségi' in fonev else 'ó' if 'ószövetségi' in fonev else \
                    (elotte[-1][0].lower() if elotte else '')
                if testamentum == 'ú':
                    vart, mi = usz, 'újszövetségi'
                elif testamentum == 'ó':
                    vart, mi = osz, 'ószövetségi'
                else:
                    vart, mi = ossz, 'összes'
                if lxx_m and lxx and n in lxx.values():
                    continue
                if n != vart and (testamentum or n not in (ossz, osz, usz)):
                    ki.append(talalat('KIVONAT_SZAM', FIGY, s.n, mondat[max(0, m.start() - 60):m.end() + 40],
                                      'a Kivonat „%s” darabszáma (%d) ≠ az 1. tábla %s helyeinek száma (%d)' % (
                                          m.group(0), n, mi, vart)))
            if lxx_m and lxx and lxx.get('kutatói azonosítás függőben') and re.search(
                    r'\bmind(?:három|két|en| a \w+)\b', mondat):
                ki.append(talalat('KIVONAT_SZAM', FIGY, s.n, mondat[:160],
                                  'a Kivonat minden LXX-helyről állít, de a 3. szakasz összesítője szerint %d hely '
                                  '„kutatói azonosítás függőben”' % lxx['kutatói azonosítás függőben']))
    return ki


KOLOFON_KOTELEZO = ('Kiadás', 'Próza modellje')
KOLOFON_NEM_URES = ('Státusz', 'Kereszthivatkozás-napló', 'Sablon-megfelelőség', 'Forrás-study')


def ell_kolofon(sorok):
    kol = [s for s in sorok if s.szakasz.startswith('Kolofon')]
    if not kol:
        return [talalat('KOLOFON', BUKAS, 0, '', 'a lapon nincs Kolofon')]
    mezok = {}
    for s in kol:
        if s.fajta == 'tabla':
            c = [x.strip() for x in s.szoveg.strip().strip('|').split('|')]
            if len(c) >= 2:
                mezok.setdefault(c[0], (s.n, c[1]))
    ki = []
    for k in KOLOFON_KOTELEZO:
        if k not in mezok:
            ki.append(talalat('KOLOFON', BUKAS, kol[0].n, '', 'a Kolofonban nincs „%s” sor' % k))
    if not any('Változásjegyzék' in s.szoveg for s in kol):
        ki.append(talalat('KOLOFON', BUKAS, kol[0].n, '', 'a Kolofonban nincs Változásjegyzék'))
    for k in KOLOFON_NEM_URES:
        if k in mezok and mezok[k][1].strip(' `') in ('', '—', '-'):
            ki.append(talalat('KOLOFON', BUKAS, mezok[k][0], '| %s | %s |' % (k, mezok[k][1]),
                              'üres törzsadat-mező: %s' % k))
    return ki


HIANYJEL_RX = re.compile(r'\*\((nincs [^)]*)\)\*|nincs a szakasztáblában')


def ell_hianyjel(sorok):
    ki = []
    for s in sorok:
        if s.fajta in ('komment', 'kod', 'ures', 'proveniencia') or s.szakasz.startswith(KIZART_SZAKASZ):
            continue
        for m in HIANYJEL_RX.finditer(s.szoveg):
            ki.append(talalat('HIANYJEL', FIGY, s.n, kornyezet(s.szoveg, m, 30),
                              'belső hiányjelzés az olvasói szövegben: ' + m.group(0), m.group(0)))
            break
    return ki


SZINT_ALATT_RX = re.compile(r'ennél a motívumnál még nincs|nem futott|üres blokk|egyikéhez sincs rögzített indoklás|'
                            r'még nincs (?:ilyen|kapcsolat)', re.I)
SZINT_ARANY = 0.25      # a szakasz szószáma az arany lap azonos szakaszáénak ennyi része alatt: figyelmeztetés
SZINT_MIN_ARANY = 150   # csak az arany lapon legalább ennyi szavas szakaszokat mérjük
# csak az értelmező (kézi) és a kapcsolati szakaszokat: az 1., 1/b., 2–4. hossza az előfordulások számával arányos
SZINT_SZAKASZ = ('5. Kapcsolatok', '5/b.', '6. Értelmezés', '6/b.', '7. Módszertan',
                 '7. Kapcsolatok', '8. Kapcsolódó', '9. Értelmezés', '10. Alkalmazás', '11. Módszertan',
                 '10. Módszertan', '10. Értelmezés')   # F182 (A21); F183: a 9. a Hatástörténet, az Értelmezés a 10.


def szakasz_szoszam(sorok):
    ki = {}
    for s in sorok:
        if s.fajta in ('proza', 'tabla', 'dolt', 'karoli', 'labjegyzet') and s.szakasz:
            kulcs = re.sub(r'\s*\*\(.*\)\*\s*$', '', s.szakasz)
            ki[kulcs] = ki.get(kulcs, 0) + len(s.szoveg.split())
    return ki


_ARANY_SZOSZAM = None


def ell_szint(sorok, arany_szoszam=None):
    ki = []
    for s in sorok:
        if s.olvasoi and SZINT_ALATT_RX.search(s.szoveg):
            m = SZINT_ALATT_RX.search(s.szoveg)
            ki.append(talalat('SZINT_ALATT', FIGY, s.n, kornyezet(s.szoveg, m), 'üres vagy hiányt jelző blokk'))
    if arany_szoszam:
        sajat = szakasz_szoszam(sorok)
        elso = {}
        for s in sorok:
            if s.fajta == 'cim' and s.szoveg.startswith('## '):
                elso.setdefault(re.sub(r'\s*\*\(.*\)\*\s*$', '', s.szakasz), s.n)
        for k, a in arany_szoszam.items():
            if a < SZINT_MIN_ARANY or not k.startswith(SZINT_SZAKASZ) or k not in elso:
                continue
            if sajat.get(k, 0) < SZINT_ARANY * a:
                ki.append(talalat('SZINT_ALATT', FIGY, elso[k], k, 'a szakasz %d szó, az arany lapon %d (< %d%%)' % (
                    sajat.get(k, 0), a, int(SZINT_ARANY * 100))))
    return ki


_KH_GYANUS = None


def ell_kh(sorok):
    global _KH_GYANUS
    if _KH_GYANUS is None:
        import karoli_kh_epseg as KH
        _KH_GYANUS = KH.gyanus_forrasok()
    _, step, _ = konyvek()
    ki, jelzett = [], set()
    for s in sorok:
        # a szakasz száma a lapszerkezettől függ (régi lap: 4., új szerkezet: 6.); lap-javit HAMART-001, lektor 15.:
        # a „4.” rögzítése miatt az új szerkezetű lapon az ellenőrzés nem futott
        if not re.match(r'\d+\. Kereszthivatkoz', s.szakasz) or not s.szoveg.strip().startswith('- Károli-KH'):
            continue
        m = re.match(r'(\S+)\s+(\d+):(\d+)', s.alszakasz)
        if not m or m.group(1) not in step:
            continue
        forras = '%s.%s.%s' % (step[m.group(1)], m.group(2), m.group(3))
        if forras in _KH_GYANUS and forras not in jelzett:
            jelzett.add(forras)
            # új szerkezetű lapon (KIVETEL_NELKUL) a másolt lista BUKÁS: a generátor kiszűri, a lapra nem kerülhet
            ki.append(talalat('KH_MASOLT', BUKAS if KIVETEL_NELKUL else FIGY, s.n,
                              '%s → %s' % (s.alszakasz, s.szoveg.strip()[2:]),
                              'a Károli-KH lista feltehetően más vers listájának (teljes vagy részleges) másolata (gazdája: '
                              '%s); javítás: N-F156a' % ', '.join(_KH_GYANUS[forras][:3])))
    return ki


def ell_atvett(szoveg):
    """A párhuzamos szabályok (lábjegyzet: ellenoriz.py 24.; 1/a próza: proza_1a.py) — ha a main-en vannak."""
    ki, megj = [], []
    try:
        import ellenoriz as E
        f = getattr(E, 'lap_labjegyzet_hianyok', None)
    except Exception:  # noqa: BLE001
        f = None
    if f is None:
        megj.append('LABJEGYZET: az ellenoriz.lap_labjegyzet_hianyok még nincs a main-en (PR #595) — nem mérve')
    else:
        for k in f(szoveg):
            ki.append(talalat('LABJEGYZET', BUKAS, 0, '[^%s]' % k, 'definíció nélküli lábjegyzet'))
    try:
        import proza_1a as P
    except ImportError:
        P = None
    if P is None or not hasattr(P, 'meres'):
        megj.append('PROZA_1A: a proza_1a.py még nincs a main-en (PR #593) — nem mérve')
    else:
        for x in P.meres(szoveg):
            if not (x[1] == 'kerek' and x[2] == 'van'):
                ki.append(talalat('PROZA_1A', BUKAS, 0, x[0], '1/a: próza %s, Funkció %s' % (x[1], x[2])))
    return ki, megj


# CELLA_ISMETLES (F123.HAMART3, 2026-11-05): a tartomány-sor versenként ugyanazt a jelentést írta a cellába
# (5Móz 27:15-26: tizenkétszer). Elem: a cellában egy „… [ⓘ](…)” link a szövegével, az előző link (vagy a cella
# eleje) után; ugyanaz az elem kétszer egy cellában hiba.
CELLA_ELEM_RX = re.compile(r'([^|;]*?(?:;[^|;]*?)*?\[ⓘ\](?:\([^)]*\))?)')  # a tagolt sorban a link célja már levágva


def ell_cella_ismetles(sorok):
    ki = []
    for s in sorok:
        if s.fajta != 'tabla':
            continue
        for cella in s.szoveg.split('|'):
            elemek = [e.strip(' ;') for e in CELLA_ELEM_RX.findall(cella)]
            latott = set()
            for e in elemek:
                if e in latott:
                    ki.append(talalat('CELLA_ISMETLES', BUKAS, s.n, e[:80],
                                      'a táblacellában ugyanaz az elem többször áll (tartomány-sor ismétlése?)'))
                    break
                latott.add(e)
    return ki


# NAVE_ANGOL (F123.HAMART3 javítókör, 2026-11-08): a Nave-blokk angol témaneve nem áll az olvasói szövegben (csak a
# `title` attribútumban), és nyers HTML-karakterkód (`&#8221`, pontosvessző nélkül is) sehol sem áll benne.
NYERS_KOD_RX = re.compile(r'&#x?[0-9A-Fa-f]+;?')
TITLE_RX = re.compile(r'\stitle="[^"]*"')
NAVE_ANGOL_RX = re.compile(r'\(\*[A-Z][^*]*\*\)|\*\(fordításra vár\)\*')


def ell_nave_angol(sorok):
    ki = []
    for s in sorok:
        if not s.olvasoi:
            continue
        t = TITLE_RX.sub('', s.szoveg)
        m = NYERS_KOD_RX.search(t)
        if m:
            ki.append(talalat('NAVE_ANGOL', BUKAS, s.n, kornyezet(t, m), 'nyers HTML-karakterkód: ' + m.group(0),
                              m.group(0)))
        if s.alszakasz.startswith('12. Tematikus index') or 'Tematikus index' in s.alszakasz:
            m = NAVE_ANGOL_RX.search(t)
            if m:
                ki.append(talalat('NAVE_ANGOL', BUKAS, s.n, kornyezet(t, m),
                                  'angol témanév az olvasói szövegben: ' + m.group(0), m.group(0)))
    return ki


# VISSZHANG (F178.5, DT639, DT-F178d; a felhasználó: „Legyen biztosítva, hogy ezt át tudjuk vinni, ne legyen
# visszaesés”, 2026-11-08): a 4.11 visszhang-blokk szabályai minden lapon, ahol a blokk áll — BUKÁS. Az alszabályok
# (V1–V7) leírása a `VISSZHANG_ALSZABALYOK` táblában (fent) áll, egy helyen (F184 D3, DT-F184a).
VH_ANGOL_RX = re.compile(r"\b(?:see|so|cf|Assyrian|Arabic|Syriac|Ethiopic|Aramaic|Late Hebrew|Hiph'?il|Ecclus|"
                         r"cursed|curse|grief|corruption)\b|fordításra vár")
VH_NEM_ROKON_RX = re.compile(r'^\s*(?:újhéber|targumi|Sirák|késői héber)', re.I)
VH_KIEMELT_JO_RX = re.compile(r'láncon kívül.*\d+%')   # kiemelt csak alapvonallal (DT-F178d, pontosítva)
VH_FORDITASOK = ((1, 'Targum'), (2, 'Vulgata'), (3, 'LXX'))
_VH_NEM_AZONOSITOTT = None


def _niqqud_nelkul(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not ('֑' <= c <= 'ׇ'))


def vh_nem_azonositott():
    """A rokon írások gyorsítótárában bdb_szócikk=0 Strongok próbált alakjai (pontozatlan héber)."""
    global _VH_NEM_AZONOSITOTT
    if _VH_NEM_AZONOSITOTT is None:
        _VH_NEM_AZONOSITOTT = set()
        ut = os.path.join(GYOKER, 'konkordancia', 'BDB_rokon_irasok.tsv')
        if os.path.exists(ut):
            with open(ut, encoding='utf-8') as f:
                for sor in f:
                    m = re.match(r'# lekérdezve: H\d+ \| próbált_alakok=([^|]+)\|.*bdb_szócikk=0\b', sor)
                    if m:
                        _VH_NEM_AZONOSITOTT.update(x.strip() for x in m.group(1).split(','))
    return _VH_NEM_AZONOSITOTT


def _vh_cellak(t):
    return [c.strip() for c in t.strip().strip('|').split('|')]


def ell_visszhang(sorok):
    ki = []
    mondatok = {}
    for s in sorok:
        # F183: a visszhang-blokk a 9. Hatástörténet „Ókori fordítások: Ószövetség” alcíme alatt áll (a 4.11 helyén mutató)
        if s.fajta not in ('tabla', 'proza') or not (s.alszakasz.startswith('4.11.') or
                                                    s.alszakasz.startswith('Ókori fordítások: Ószövetség') or
                                                    s.alszakasz.startswith('Háttér: rokon nyelvek')):
            continue
        t = s.szoveg
        m = VH_ANGOL_RX.search(t)
        if m:
            ki.append(talalat('VISSZHANG', BUKAS, s.n, kornyezet(t, m), 'V1 angol maradék a visszhang-blokkban: ' +
                              m.group(0), 'V1' + m.group(0)))
        if s.fajta != 'tabla':
            continue
        c = _vh_cellak(t)
        if s.alszakasz.startswith('Háttér') and len(c) == 4 and not set(c[0]) <= set('-: '):
            if VH_NEM_ROKON_RX.search(c[1]):
                ki.append(talalat('VISSZHANG', BUKAS, s.n, t, 'V2 nem rokon nyelvi sor a BDB-háttérben: ' + c[1][:40]))
            if 'nincs rokon nyelvi adat' in c[1]:
                szo = re.findall('[֐-׿]+', c[0])
                if szo and _niqqud_nelkul(szo[0]) in vh_nem_azonositott():
                    ki.append(talalat('VISSZHANG', BUKAS, s.n, t, 'V3 „nincs rokon nyelvi adat”, holott a BDB-szócikk '
                                                                  'nem azonosított (nem azonosítható ≠ nincs)'))
        elif s.alszakasz.startswith('4.11.') and len(c) == 5 and c[0] != 'Lánc-szó · versek' \
                and not set(c[0]) <= set('-: '):
            mit = c[4]
            for i, nev in VH_FORDITASOK:
                cella = c[i].replace('**', '')
                mm = re.match(r'^(.*?) · (\d+)/(\d+)\b', cella)
                if mm and len(mm.group(1).split(' · ')) >= 2 and re.search(r'\b%s: ugyanaz a szó\b' % nev, mit):
                    ki.append(talalat('VISSZHANG', BUKAS, s.n, mit[:120], 'V4 „ugyanaz a szó” két lemmánál (%s): '
                                                                         'helyesen „ugyanaz a szócsalád”' % nev))
            for b in re.findall(r'\*\*(.+?)\*\*', mit):
                if not VH_KIEMELT_JO_RX.search(b):
                    ki.append(talalat('VISSZHANG', BUKAS, s.n, b[:120], 'V5 kiemelt következtetés alapvonal nélkül'))
            # V6: tagmondatonként (pont és pontosvessző), a számok és a fordítók neve nélkül, a teljes táblán és a
            # cellán belül is számolva
            for mondat in re.split(r'(?<=[.;])\s+', mit.replace('**', '')):
                kulcs = re.sub(r'\d+', '#', re.sub(r'\b(?:A|a) (?:Targum|Vulgata|LXX)\b:?', '', mondat)).strip(' .;')
                if len(kulcs) > 25:
                    mondatok.setdefault(kulcs, []).append(s.n)
            # V7: a LXX alapvonal-mondata a sávja szerinti: ≥ 80% „szokásos”, 40–80% „gyakori, de nem kizárólagos”,
            # < 40% kiemelt „más szót választ”
            for mondat in re.split(r'(?<=\.)\s+', mit.replace('**', '')):
                pcts = [int(x) for x in re.findall(r'(\d+)%', mondat)] if 'láncon kívül' in mondat else []
                if not pcts:
                    continue
                pct, kor = min(pcts), mondat
                egyesit = 'mindkét héber szót' in mondat
                kell = (('így van' if egyesit else 'szokásos fordítása') if pct >= 80 else
                        ('gyakran, de nem kizárólag' if egyesit else 'gyakori, de nem kizárólag') if pct >= 40 else
                        ('nem így' if egyesit else 'más szót választ'))
                if kell not in kor:
                    ki.append(talalat('VISSZHANG', BUKAS, s.n, kor[:120], 'V7 az alapvonal (%d%%) mondata nem a sávja '
                                                                          'szerinti („%s”)' % (pct, kell)))
                # ELLENOR_F178 5.: a nevező nem állhat találatszámként („a versek 98%-ában (97 vers)”); a helyes alak
                # „a láncon kívüli N versből x versben (y%)”, és a három szám egymással egyezik
                if re.search(r'%-[aá]ban \(\d+ vers\)', kor):
                    ki.append(talalat('VISSZHANG', BUKAS, s.n, kor[:120], 'V7 a zárójeles versszám a nevező, az olvasó '
                                                                          'találatnak érti: helyesen „a láncon kívüli N '
                                                                          'versből x versben (y%)”'))
                for nn, xx, yy in re.findall(r'kívüli (\d+) versből (?:csak )?(\d+) versben \((\d+)%\)', kor):
                    nn, xx, yy = int(nn), int(xx), int(yy)
                    if not nn or xx > nn or int(round(100.0 * xx / nn)) != yy:
                        ki.append(talalat('VISSZHANG', BUKAS, s.n, kor[:120], 'V7 az alapvonal számai nem egyeznek: '
                                                                              '%d versből %d (%d%%)' % (nn, xx, yy)))
    for mondat, ns in mondatok.items():
        if len(ns) >= 3:
            ki.append(talalat('VISSZHANG', BUKAS, ns[0], mondat[:120], 'V6 sablonmondat-ismétlés: %d sorban' % len(ns)))
    return ki


# --- BDB_OLVASOI (F104, DT-F104b): a 4.2 kétrétegű BDB-kártyájának olvasói rétege. A kutatói réteg (apparátus) határa a
# generátor jelölője (`lexikon_general.APPARATUS_RX`, egy helyen definiálva); a feloldatlan jelek: a gyakoriság-számláló, a
# zárójeles forrásjel, a szövegtanú- és gyökjel, az egybetűs rövidítés, a `konfig/bdb_jelek.tsv` szerző- és szövegtanú-jelei
# (3+ betű), a „szerző mű szám” alakú irodalmi hivatkozás; belső címke: sorszám, BDB-azonosító, „nincs címke”, kutatói jel.
BDB_OLVASOI_MINTA = [
    (re.compile(r'(?<=\S)_\d+'), 'nyers gyakoriság-számláló (_N)'),
    (re.compile(r'\((?:mind\s+|mindkettő\s+)?(?:J|E|P|D|H|R|JE)(?:\s+(?:J|E|P|D|H|R))*\)'), 'feloldatlan forrásjel'),
    (re.compile('[ᵐᵑ⅏√]'), 'feloldatlan szövegtanú- vagy gyökjel'),
    (re.compile('[א-ת][\u0591-\u05C7]*׳'), 'feloldatlan egybetűs rövidítés'),
    (re.compile(r'\b[A-Z][a-zö]{0,3}\s[A-Z][A-Za-z]{0,3}\s\d{2,4}\b'), 'irodalmi hivatkozás (szerző mű szám)'),
    (re.compile(r'\bsorsz[aá]m\w*|\bBDB\d+|nincs címke|ⓘ|[Kk]utatói (?:megjegyzés|jelölés)|\bhorgony'), 'belső címke vagy sorszám'),
    # F187 / F29 (c): a szócikk sorszáma („1. szócikk”, „II. szócikk”) belső tagolás, nem olvasói név
    (re.compile(r'(?<![\w.])(?:\d+|[IVX]+)\.\s+szócikk'), 'belső címke vagy sorszám'),
    # F187 / F29 (b): a szócikk feje nem jelentéspont
    (re.compile(r'a szócikk feje'), 'a szócikk feje jelentéspontként'),
]
# F187: a görög kártya olvasói rétegében nyers görög alak sem állhat (az alakjegyzék az apparátusé)
THAYER_OLVASOI_MINTA = [(re.compile('[Ͱ-Ͽἀ-῿]'), 'nyers görög alak az olvasói rétegben')]
_HELY_RX = re.compile(r'((?:[1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,6}\s+)?)(\d+):(\d+)')


def helyek_ismetlese(sor):
    """F29 (b): „A motívum helyein:” sorban kétszer álló versek (a rövidített felsorolás — „1Móz 3:17, 3:23” — könyvnevét
    örökítve); csak a „→” előtti versek számítanak."""
    t = re.sub(r'^\s*\*\*A motívum helyein:\*\*\s*', '', sor)
    lat, ketszer, konyv = set(), [], ''
    for resz in t.split(' · '):
        if ' → ' not in resz:
            continue
        for m in _HELY_RX.finditer(resz.split(' → ', 1)[0]):
            konyv = m.group(1).strip() or konyv
            v = '%s %s:%s' % (konyv, m.group(2), m.group(3))
            if v in lat and v not in ketszer:
                ketszer.append(v)
            lat.add(v)
    return ketszer
_BDB_JELEK_RX = None


def _bdb_jelek_rx():
    global _BDB_JELEK_RX
    if _BDB_JELEK_RX is None:
        jelek = []
        ut = os.path.join(GYOKER, 'eszkozok', 'olvaso_szerver', 'konfig', 'bdb_jelek.tsv')
        if os.path.exists(ut):
            fej = None
            with open(ut, encoding='utf-8') as f:
                for sor in f:
                    sor = sor.rstrip('\n')
                    if not sor or sor.startswith('#'):
                        continue
                    m = sor.split('\t')
                    if fej is None:
                        fej = m
                        continue
                    d = dict(zip(fej, m))
                    if d.get('csoport') in ('szerző', 'szövegtanú') and len(d.get('jel', '')) >= 3:
                        jelek.append(d['jel'])
        _BDB_JELEK_RX = re.compile(r'(?<![\w])(%s)(?![\w])' % '|'.join(re.escape(j) for j in sorted(jelek, key=len, reverse=True))) \
            if jelek else None
    return _BDB_JELEK_RX


def ell_bdb_olvasoi(sorok):
    """Az új szerkezetű lap 4.2-es szakaszában a BDB-kártyák olvasói rétege (a `##### … · BDB` címtől az apparátus
    kezdetéig) nem hordozhat feloldatlan rövidítést, belső címkét vagy nyers sorszámot. A régi lapon nem fut."""
    if not KIVETEL_NELKUL:
        return []
    from lexikon_general import APPARATUS_RX
    # a kétrétegű kártyát nem hordozó új szerkezetű lapon sem fut (a generátor kapcsolója, `lexikon_general.KETRETEGU_BDB_KARTYA`,
    # ki van kapcsolva, vagy a lap még a régi alakú): a kapu a lap jelölőjéhez igazodik, mint az F178.4-nél a lapszerkezethez
    if not any(APPARATUS_RX.search(s.nyers) for s in sorok):
        return []
    ki, in42, kartya = [], False, False
    jelek = _bdb_jelek_rx()
    for s in sorok:
        if s.fajta == 'cim':
            t = s.szoveg.strip()
            if re.match(r'^#{1,4}\s', t):
                in42 = bool(re.match(r'^#{4}\s+4\.2\.', t))
                kartya = False
            elif in42 and re.match(r'^#{5}\s', t):
                # F187: a görög (Thayer) kártya olvasói rétegét ugyanez a kapu védi
                kartya = 'BDB' if t.rstrip().endswith('· BDB') else ('Thayer' if t.rstrip().endswith('· Thayer') else False)
            continue
        m = APPARATUS_RX.search(s.nyers)
        if m:
            if m.group(1) == 'KEZDET':
                kartya = False
            continue
        if not (in42 and kartya) or s.fajta in ('komment', 'kod', 'ures'):
            continue
        t = kod_nelkul(s.szoveg)
        for rx, nev in BDB_OLVASOI_MINTA + ([(jelek, 'feloldatlan szerző- vagy szövegtanú-jel')] if jelek else []) + \
                (THAYER_OLVASOI_MINTA if kartya == 'Thayer' else []):
            mm = rx.search(t)
            if mm:
                ki.append(talalat('BDB_OLVASOI', BUKAS, s.n, kornyezet(t, mm, 40), nev, nev))
        if t.lstrip().startswith('**A motívum helyein:**'):
            dupla = helyek_ismetlese(t.strip())
            if dupla:
                nev = 'egy vers kétszer a motívum helyei között'
                ki.append(talalat('BDB_OLVASOI', BUKAS, s.n, ', '.join(dupla), nev, nev))
    return ki


ELLENORZESEK = [ell_belso, ell_pont, ell_angol, ell_idezojel, ell_atiras, ell_konyv, ell_bdb, ell_funkcio,
                ell_idezet, ell_kivonat, ell_kolofon, ell_hianyjel, ell_kh, ell_cella_ismetles, ell_nave_angol,
                ell_visszhang, ell_bdb_olvasoi, ell_munkaszo, ell_szakasz_hiv, ell_helyorzo, ell_lista_nevelo, ell_meghatarozas, ell_nyers_jel, ell_mi_hang,
                ell_nevelo, ell_kov_ism, ell_indoklas]


def arany_szoszam():
    global _ARANY_SZOSZAM
    if _ARANY_SZOSZAM is None:
        ut = os.path.join(GYOKER, 'lexikon', ARANY + '_TUDOMANYOS.md')
        if os.path.exists(ut):
            with open(ut, encoding='utf-8') as f:
                _ARANY_SZOSZAM = szakasz_szoszam(tagol(f.read()))
        else:
            _ARANY_SZOSZAM = {}
    return _ARANY_SZOSZAM


def lap_meres(szoveg, kh=True, atvett=True, arany=True):
    """Egy lap szövegének mérése: (találatok, megjegyzések). Az új szerkezetű lapon kivétel nélkül (F178.4)."""
    global KIVETEL_NELKUL, KIZART_SZAKASZ
    KIVETEL_NELKUL = bool(UJ_SZERKEZET_RX.search(szoveg))
    KIZART_SZAKASZ = () if KIVETEL_NELKUL else KIZART_SZAKASZ_REGI
    sorok = tagol(szoveg)
    ki = []
    for f in ELLENORZESEK:
        if f is ell_kh and not kh:
            continue
        ki += f(sorok)
    ki += ell_szint(sorok, arany_szoszam() if arany else None)
    if KIVETEL_NELKUL:
        import tablajegyzet as TJ
        for n, _sz, reszlet in TJ.onref_talalatok(szoveg):
            ki.append(talalat('ONREF', FIGY, n, reszlet, 'önreferáló „lap”: a valódi alany kell (motívum, vizsgálat, '
                                                          'keresés, szócikk)'))
    megj = []
    if atvett:
        a, megj = ell_atvett(szoveg)
        ki += a
    return csoportosit(ki, sorok), megj


LEXIKON_KONYVTAR = os.path.join(GYOKER, 'lexikon')


def motivum_meres(mid):
    ut = os.path.join(LEXIKON_KONYVTAR, mid + '_TUDOMANYOS.md')
    if not os.path.exists(ut):
        return None, ['nincs lexikon/%s_TUDOMANYOS.md' % mid]
    with open(ut, encoding='utf-8') as f:
        return lap_meres(f.read())


def osszesit(talalatok):
    """{azonosító: {BUKÁS: n, FIGYELMEZTETÉS: n}} és a két összeg."""
    by = {}
    for t in talalatok:
        by.setdefault(t['azonosito'], {BUKAS: 0, FIGY: 0})[t['sulyossag']] += 1
    return by, sum(1 for t in talalatok if t['sulyossag'] == BUKAS), sum(1 for t in talalatok if t['sulyossag'] == FIGY)


def main():
    ap = argparse.ArgumentParser(description='Gépi olvasói kapu egy lexikonlapon')
    ap.add_argument('id', nargs='*')
    ap.add_argument('--osszes', action='store_true', help='minden lexikon/*_TUDOMANYOS.md')
    ap.add_argument('--reszletes', action='store_true', help='minden találat soronként')
    ap.add_argument('--json', help='a teljes kimenet JSON-fájlba')
    ap.add_argument('--lexikon-konyvtar', help='a lapok könyvtára (alapból lexikon/; pl. egy --kimenet próba lexikon/ mappája)')
    ap.add_argument('--markdown', help='motívumonkénti javítandó lista Markdown-fájlba (generált napló)')
    a = ap.parse_args()
    global LEXIKON_KONYVTAR
    if a.lexikon_konyvtar:
        LEXIKON_KONYVTAR = os.path.abspath(a.lexikon_konyvtar)
    ids = a.id
    if a.osszes:
        ids = sorted(n[:-len('_TUDOMANYOS.md')] for n in os.listdir(LEXIKON_KONYVTAR)
                     if n.endswith('_TUDOMANYOS.md'))
    if not ids:
        ap.error('adj meg motívum-ID-t vagy --osszes')
    ossz, buk_ossz = {}, 0
    for mid in ids:
        tal, megj = motivum_meres(mid)
        if tal is None:
            print('## %s: %s' % (mid, megj[0]))
            continue
        by, b, fi = osszesit(tal)
        buk_ossz += b
        ossz[mid] = {'bukas': b, 'figyelmeztetes': fi, 'kapunkent': by, 'megjegyzes': megj, 'talalatok': tal}
        print('## %s: %d BUKÁS, %d FIGYELMEZTETÉS' % (mid, b, fi))
        for k in sorted(by):
            print('   %-13s BUKÁS %3d · FIGY %3d' % (k, by[k][BUKAS], by[k][FIGY]))
        for x in megj:
            print('   (%s)' % x)
        if a.reszletes:
            for t in tal:
                print('   %5s %-13s %-14s %s — %s' % (t['sor'], t['azonosito'], t['sulyossag'], t['uzenet'], t['idezet']))
        print()
    if a.json:
        with open(a.json, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(ossz, f, ensure_ascii=False, indent=1)
    if a.markdown:
        with open(a.markdown, 'w', encoding='utf-8', newline='\n') as f:
            f.write(markdown(ossz))
    return 1 if buk_ossz else 0


def cella(s):
    return (s or '').replace('|', '\\|').replace('\n', ' ')


def markdown(ossz):
    """A mérés generált naplója: összesítő és motívumonként a javítandó lista."""
    ki = ['# GENERÁLT: eszkozok/olvasoi_kapu.py --markdown — kézzel szerkeszteni tilos', '',
          '# Olvasói kapu — mérés a lexikonlapokon', '',
          '*scope=lexikon/*_TUDOMANYOS.md | forras=eszkozok/olvasoi_kapu.py | ts=%s*' % os.environ.get(
              'PARDES_DATUM', 'futáskor'), '',
          'Egy tétel = egy hiba egy szakaszban; a `db` az ismétlődések száma (pl. ugyanaz a belső jel egy tábla '
          'több sorában). A sorszám a lap Markdown-sora.', '',
          '| Motívum | BUKÁS | FIGYELMEZTETÉS | Kapunként (B/F) |', '|---|---|---|---|']
    for mid, d in ossz.items():
        ki.append('| %s | %d | %d | %s |' % (mid, d['bukas'], d['figyelmeztetes'], ', '.join(
            '%s %d/%d' % (k, v[BUKAS], v[FIGY]) for k, v in sorted(d['kapunkent'].items()))))
    for mid, d in ossz.items():
        ki += ['', '## %s — %d BUKÁS, %d FIGYELMEZTETÉS' % (mid, d['bukas'], d['figyelmeztetes']), '']
        for m in d['megjegyzes']:
            ki.append('*%s*' % m)
        ki += ['', '| Sor | Ellenőrzés | Súlyosság | db | Mi a hiba | Idézet |', '|---|---|---|---|---|---|']
        for t in sorted(d['talalatok'], key=lambda x: (x['sulyossag'] != BUKAS, x['sor'])):
            ki.append('| %s | %s | %s | %d | %s | %s |' % (t['sor'], t['azonosito'], t['sulyossag'], t['db'],
                                                          cella(t['uzenet']), cella(t['idezet'])))
    return '\n'.join(ki) + '\n'


if __name__ == '__main__':
    sys.exit(main())
