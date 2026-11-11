#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""proza_allitas.py -- F200: a lexikonlap értelmező prózájának versre hivatkozó állításai a vers és az adat mellett.

A kézi forrás (`motivumok/<ID>.md`) értelmező réseiből (`<!-- RÉS-KEZDET: … -->` … `<!-- RÉS-VÉGE: … -->`) és a
motívum `adat/elofordulasok.tsv`-sorainak `kapcsolodas` prózájából kigyűjti a versre hivatkozó mondatokat
(igehely-felismerés a `konkordancia/Konyv_normalizalo_tabla.tsv` szerint), és ahol lehet, gépileg ellenőrzi őket:

- **szójelenlét** („a föld szava nélkül”, „a föld szava … áll”, „más héber szóval”): a vers TAHOT/TAGNT Strong-sorai;
- **szópár** (a forrásban a „szópárja (…; …)” felsorolás, a feloldás a `gerinc_elem` + a vers Strong-sorai):
  mindkét szó a versben áll-e;
- **szám** („47 helyet”, „hat újszövetségi helyén”, „a szó 211 versben áll”): az `adat/elofordulasok.tsv` sorai,
  illetve a TAHOT/TAGNT versszáma;
- **idézet** (`„…”`, legalább három szó): a Károli 1908 szövege, az olvasói kapu egyeztetésével
  (`olvasoi_kapu.karoli_egyezik`, az E34-gyel azonos tűréssel).

Ahol az állítás nem gépies (ki az alany, mi telik meg mivel, mire utal vissza), az ellenőrzési listára kerül: az
állítás, a Károli-vers és a héber/görög sor egymás mellett, a gépi jelzésekkel (⚑: a magyar szó a versben más
héber/görög szót fordít, mint a lánc szava; a szó nincs a versben). A listát olcsó modell vagy ember nézi át;
az eszköz modellt nem hív.

Kimenet: `naplok/ALLITAS_<ID>.md` (soronként: állítás | vers | gépi ítélet: egyezik / ELTÉR / kézi | bizonyíték).
Kapu-szint: JELENTÉS (a kilépőkód 0; `--szigoru`: 1, ha van ELTÉR-sor).

`--lektor <fájl>`: összevetés egy lektori kérdéslistával (`naplok/KIADAS_<ID>_lektor.md` szerkezet): a pontossági
tételek (a „Mi a gond” sor az 1. vagy a 4. kérdést nevezi) közül hányat fog meg gépileg, hányat tesz kézi listára,
hányat nem lát. Ez a jelentés első sora.

A TSV-k olvasása `split('\t')` (CLAUDE.md); a `karoli_strong/parok_<könyv>.tsv` párosítás modell-kimenet (javaslat,
SEMA 2.20): csak bizonyítékként és jelzésként áll, ítélet nem épül rá.

CLI:
    python eszkozok/proza_allitas.py HAMART-001
    python eszkozok/proza_allitas.py HAMART-001 --lektor naplok/KIADAS_HAMART-001_lektor.md
    python eszkozok/proza_allitas.py HAMART-001 --kimenet <fájl> --szigoru
"""
import argparse
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ESZKOZOK = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(ESZKOZOK)
if ESZKOZOK not in sys.path:
    sys.path.insert(0, ESZKOZOK)

import lekerdez as L  # noqa: E402  (parse_range, in_range)
import olvasoi_kapu as OK  # noqa: E402  (normal_szoveg, karoli_egyezik, IDEZET_RX)
import heber_kiejtes as HK  # noqa: E402  (kiejt: az átírás feloldása)
import strong_util as SU  # noqa: E402  (F62: az egyetlen Strong-normalizáló)

KONK = os.path.join(ROOT, 'konkordancia')
ADAT = os.path.join(ROOT, 'adat')
T_NORMAL = os.path.join(KONK, 'Konyv_normalizalo_tabla.tsv')
T_KAROLI = os.path.join(KONK, 'Karoli_1908.tsv')
T_TAHOT = os.path.join(KONK, 'TAHOT_kivonat.tsv')
T_TAGNT = os.path.join(KONK, 'TAGNT_kivonat.tsv')
T_ELOF = os.path.join(ADAT, 'elofordulasok.tsv')
T_GRAMM = os.path.join(ADAT, 'grammatikai_strongok.tsv')
D_PAROK = os.path.join(ADAT, 'karoli_strong')

UJSZ_KONYVEK = ('Mt', 'Mk', 'Luk', 'Ján', 'ApCsel', 'Róm', '1Kor', '2Kor', 'Gal', 'Ef', 'Fil', 'Kol', '1Thessz',
                '2Thessz', '1Tim', '2Tim', 'Tit', 'Filem', 'Zsid', 'Jak', '1Pét', '2Pét', '1Ján', '2Ján', '3Ján',
                'Júd', 'Jel')
ADAT_KONYV = {'JSir': 'Sir'}  # a magyar kulcsú konkordancia-táblák a „Sir” alakot használják (lekerdez.py, DT25)

SZAMSZAVAK = {'egy': 1, 'két': 2, 'kettő': 2, 'három': 3, 'négy': 4, 'öt': 5, 'hat': 6, 'hét': 7, 'nyolc': 8,
              'kilenc': 9, 'tíz': 10, 'tizenegy': 11, 'tizenkét': 12, 'tizenkettő': 12, 'tizenhárom': 13,
              'tizennégy': 14, 'tizenöt': 15, 'húsz': 20}
BETU = 'a-zA-ZáéíóöőúüűÁÉÍÓÖŐÚÜŰ'
GOROG = 'Ͱ-Ͽἀ-῿'


# ---------------------------------------------------------------------------
# TSV (split('\t'), nem csv)
# ---------------------------------------------------------------------------
def tsv_dict(ut):
    """A '#' kezdetű megjegyzéssorok után a fejléc, majd a sorok dictként."""
    fej = None
    with open(ut, 'r', encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n').rstrip('\r')
            if fej is None:
                if sor.startswith('#') or not sor.strip():
                    continue
                fej = sor.split('\t')
                continue
            if not sor or sor.startswith('#'):
                continue
            mezok = sor.split('\t')
            yield dict(zip(fej, mezok + [''] * (len(fej) - len(mezok))))


def strong_norm(s):
    """A Strong-szám SEMA 1.2 alakja az F62 normalizálóval (`strong_util`), a betűutótag nélkül (a motívum adata
    utótag nélküli); a G-kiegészítő kód (G + öt számjegy) megmarad. Nem Strong-szám (átírás, „tematikus:”): ''."""
    try:
        n = SU.strong_normalizal((s or '').split('+')[0].strip(), utotag='megtart')
    except ValueError:
        return ''
    return re.sub(r'(?<=\d)[A-Za-z]+$', '', n)


def ascii_konyv(konyv):
    """A karoli_strong fájlnevek könyvalakja: ékezet nélkül, kis-nagybetű megtartva (1Móz → 1Moz)."""
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', konyv) if not unicodedata.combining(c))


def nfc(s):
    import unicodedata
    return unicodedata.normalize('NFC', s or '')


def ekezet_nelkul(s):
    return OK.ekezet_nelkul(s.lower())


# ---------------------------------------------------------------------------
# Igehely-felismerés
# ---------------------------------------------------------------------------
def konyv_alakok():
    """{forrás-alak: magyar rövidítés} a normalizáló táblából (a magyar rövidítés maga is alak)."""
    alakok = {}
    for d in tsv_dict(T_NORMAL):
        hu = d.get('Magyar rövidítés', '').strip()
        if not hu:
            continue
        alakok[hu] = hu
        for a in d.get('Forrás-alakok', '').split(','):
            a = a.strip()
            if a and re.match(r'^[0-9]?[%s]+$' % BETU, a):
                alakok[a] = hu
    alakok.setdefault('Sir', 'JSir')
    return alakok


class Igehelyek:
    def __init__(self):
        self.alakok = konyv_alakok()
        konyv_rx = '|'.join(sorted((re.escape(a) for a in self.alakok), key=len, reverse=True))
        self.fo = re.compile(r'(?<![%s0-9])(%s)\s+(\d+):(\d+)(?:\s*[-–]\s*(\d+)(?::(\d+))?)?(?![0-9:])'
                             % (BETU, konyv_rx))
        self.folyt = re.compile(r'^(\s*(?:,|;|\s+és)\s*)(?:(%s)\s+)?(\d+):(\d+)'
                                r'(?:\s*[-–]\s*(\d+)(?::(\d+))?)?(?![0-9:])' % konyv_rx)

    @staticmethod
    def _alak(konyv, c, v, v2, c2v):
        if v2 and c2v:
            return '%s %s:%s-%s:%s' % (konyv, c, v, v2, c2v)
        if v2:
            return '%s %s:%s-%s' % (konyv, c, v, v2)
        return '%s %s:%s' % (konyv, c, v)

    def csoportok(self, szoveg):
        """[(kezdet, vég, [igehely, ...])]: egy csoport egy felsorolás („Ez 7:23, 8:17, 12:19”)."""
        ki, poz = [], 0
        while True:
            m = self.fo.search(szoveg, poz)
            if not m:
                break
            konyv = self.alakok[m.group(1)]
            refek = [self._alak(konyv, m.group(2), m.group(3), m.group(4), m.group(5))]
            veg = m.end()
            while True:
                f = self.folyt.match(szoveg[veg:])
                if not f:
                    break
                if f.group(2):
                    konyv = self.alakok[f.group(2)]
                refek.append(self._alak(konyv, f.group(3), f.group(4), f.group(5), f.group(6)))
                veg += f.end()
            ki.append((m.start(), veg, refek))
            poz = veg
        return ki


# ---------------------------------------------------------------------------
# Adatforrások
# ---------------------------------------------------------------------------
class Adat:
    def __init__(self):
        self.karoli = {}          # 'Ez 7:23' -> szöveg
        self.konyv_versek = {}    # 'Ez' -> [(fej, vers, kulcs)]
        for d in tsv_dict(T_KAROLI):
            k = d.get('Igehely', '')
            try:
                konyv, fej, vers = L.parse_igehely(k)
            except ValueError:
                continue
            self.karoli[k] = d.get('Károli-szöveg (teljes vers)', '')
            self.konyv_versek.setdefault(konyv, []).append((fej, vers, k))
        self.gramm = {strong_norm(d.get('strong', '')) for d in tsv_dict(T_GRAMM)}
        self.szavak = {}          # vers -> [(strong, szótő, jelentés)]
        self.parok = {}           # vers -> [(hu_szo, strong)]
        self.parok_poz = {}       # vers -> [(hu_sorszam, hu_szo, strong)]
        self.strong_versszam = {}

    def versek(self, igehely):
        """Az igehely (vers vagy tartomány) Károli-kulcsai sorrendben; [] ha nem oldható fel."""
        try:
            rng = L.parse_range(igehely)
        except ValueError:
            return []
        konyv = rng[1]
        adat_konyv = ADAT_KONYV.get(konyv, konyv)
        rng = (rng[0], adat_konyv) + tuple(rng[2:])
        return [k for fej, vers, k in self.konyv_versek.get(adat_konyv, []) if L.in_range(rng, adat_konyv, fej, vers)]

    def betolt_szavak(self, versek, strongok_szamlalasra=()):
        """A TAHOT/TAGNT sorai a kért versekre; a megadott Strong-számok versszáma a teljes táblán."""
        kell = set(versek)
        szamlalt = set(strongok_szamlalasra)
        for ut in (T_TAHOT, T_TAGNT):
            if not os.path.exists(ut):
                continue
            versek_strong = {}
            for d in tsv_dict(ut):
                k = d.get('Igehely', '')
                s = strong_norm(d.get('Strong-szám', ''))
                if s in szamlalt:
                    versek_strong.setdefault(s, set()).add(k)
                if k in kell:
                    self.szavak.setdefault(k, []).append((s, d.get('Szótő', ''), d.get('Rövid jelentés', '')))
            for s, vs in versek_strong.items():
                self.strong_versszam[s] = len(vs)

    def betolt_parok(self, versek):
        konyvek = {}
        for k in versek:
            konyvek.setdefault(k.rsplit(' ', 1)[0], set()).add(k)
        for konyv, vs in konyvek.items():
            ut = os.path.join(D_PAROK, 'parok_%s.tsv' % ascii_konyv(konyv.replace('JSir', 'Sir')))
            if not os.path.exists(ut):
                continue
            for d in tsv_dict(ut):
                k = d.get('vers', '')
                if k in vs:
                    self.parok.setdefault(k, []).append((d.get('hu_szo', ''), strong_norm(d.get('strong', ''))))
                    self.parok_poz.setdefault(k, []).append((d.get('hu_sorszam', ''), d.get('hu_szo', ''),
                                                             strong_norm(d.get('strong', ''))))

    def strongok(self, versek):
        return {s for k in versek for s, _, _ in self.szavak.get(k, [])}

    def karoli_szoveg(self, versek):
        return ' '.join(self.karoli.get(k, '') for k in versek)

    def heber_sor(self, versek):
        """Tartalmi szavak: átírás (szótő) Strong 'jelentés' — a grammatikai Strong-számok nélkül."""
        darabok = []
        for k in versek:
            for s, szoto, jel in self.szavak.get(k, []):
                if not s or s in self.gramm or s.startswith('H90') or s.startswith('H99'):
                    continue
                # héberül a magyaros kiejtés (a héber írás nélkül, a jelentés rövidebb), görögül a szótő
                nev = (HK.kiejt(szoto) or szoto) if s.startswith('H') else szoto
                darabok.append('%s %s ‘%s’' % (nev, s, jel))
        return ' · '.join(darabok)


# ---------------------------------------------------------------------------
# A motívum szókészlete: magyar szó -> Strong (a forrás saját megnevezéseiből)
# ---------------------------------------------------------------------------
def tovek(szo):
    """Egyszerű magyar tövek a mondatbeli kereséshez (föld → föld; átok → átok, átk; romlás → roml)."""
    szo = szo.lower()
    t = {szo}
    if len(szo) > 5:
        t.add(szo[:-2])
    for ve in ('ság', 'ség'):
        if szo.endswith(ve) and len(szo) > 6:
            t.add(szo[:-3])
            t.add(szo[:-4])
    m = re.match(r'^(.*[^aáeéiíoóöőuúüű])([aáeéoóöő])([^aáeéiíoóöőuúüű])$', szo)
    if m and len(szo) >= 4:
        t.add(m.group(1) + m.group(3))   # átok → átk
    return {x for x in t if len(x) >= 3}


def to_rx(tovek_):
    return re.compile(r'(?<![%s])(?:meg|el)?(?:%s)' % (BETU, '|'.join(sorted(map(re.escape, tovek_), key=len,
                                                                                    reverse=True))), re.I)


class Szokeszlet:
    """A lánc szavai: {magyar_szo: {'strong', 'atiras', 'rx'}}; a szópárok: [(kifejezés, [strong, strong], rx-ek)]."""

    def __init__(self, forras, elof_sorok, adat):
        self.atiras = {}   # átírás (ékezet nélkül) -> Strong
        for m in re.finditer(r'\b([HG]\d{4})\s+—\s+[^\s(]+\s+\(([^)]+)\)', forras):
            self.atiras[ekezet_nelkul(m.group(2).strip())] = m.group(1)
        # a motívum verseinek héber szavai: kiejtés -> Strong (az átírás feloldása, ha a fejléc nem adja)
        self.vers_kiejtes = {}
        for d in elof_sorok:
            for k in adat.versek(d.get('igehely', '')):
                for s2, szoto, _ in adat.szavak.get(k, []):
                    if s2.startswith('H') and not s2.startswith('H90'):
                        self.vers_kiejtes.setdefault(ekezet_nelkul(HK.kiejt(szoto)), s2)
        self.szavak = {}
        rx = re.compile(r'(?<![%s])(?:a|az)\s+([%s]+(?:\s+és\s+[%s]+)?)(?:\s+(?:igéje|szava))?\s+\(([%s\']+)\)'
                        % (BETU, BETU, BETU, BETU))
        for m in rx.finditer(forras):
            s = self.atiras.get(ekezet_nelkul(m.group(2))) or self.vers_kiejtes.get(ekezet_nelkul(m.group(2)))
            if not s:
                continue
            for hu in re.split(r'\s+és\s+', m.group(1)):
                self._felvesz(hu, {s}, m.group(2))
        # görög: „az átkozott (ἐπikatáratos, …)”, „a romlás szócsaládja (φθείρω, …)” -> a motívum sorainak G-számai
        g_lemma = {}
        for d in elof_sorok:
            for s in re.findall(r'G\d{4}', d.get('strong', '') + ' ' + d.get('gerinc_elem', '')):
                for k in adat.versek(d.get('igehely', '')):
                    for s2, szoto, _ in adat.szavak.get(k, []):
                        if s2 == s:
                            g_lemma[nfc(szoto)] = s
        grx = re.compile(r'(?<![%s])(?:a|az)\s+([%s]+)(\s+szócsaládja)?\s+\(([%s]+),\s*([%s]+)\)'
                         % (BETU, BETU, GOROG, BETU))
        for m in grx.finditer(nfc(forras)):
            lemma = m.group(3)
            ss = {g_lemma[lemma]} if lemma in g_lemma else set()
            if m.group(2):   # szócsalád: az előtag nélküli tő első két betűje
                to = _gorog_to(lemma)[:2]
                ss |= {v for k, v in g_lemma.items() if _gorog_to(k).startswith(to)}
            if ss:
                self._felvesz(m.group(1), ss, m.group(4))
        self.szoparok = self._szoparok(forras, elof_sorok, adat)

    def _felvesz(self, hu, strongok, atiras):
        hu = hu.strip().lower()
        if not hu:
            return
        if hu in self.szavak:
            self.szavak[hu]['strongok'] |= set(strongok)
            self.szavak[hu]['atiras'] += ', ' + atiras
        else:
            self.szavak[hu] = {'strongok': set(strongok), 'atiras': atiras, 'rx': to_rx(tovek(hu))}

    def _szoparok(self, forras, elof_sorok, adat):
        m = re.search(r'szópárja\s+\(([^)]+)\)', forras)
        if not m:
            return []
        # a gerinc_elem szópárjai: 'H6975+H1863', 'málé+chámász' -> Strong-párok (átírás a vers szavaiból)
        jeloltek = {}
        for d in elof_sorok:
            g = d.get('gerinc_elem', '')
            if '+' not in g or g.startswith('tematikus'):
                continue
            versek = adat.versek(d.get('igehely', ''))
            par = []
            for tag in g.split('+'):
                s = strong_norm(tag)
                if not s:
                    s = self.atiras.get(ekezet_nelkul(tag))
                if not s:
                    for k in versek:
                        for s2, szoto, _ in adat.szavak.get(k, []):
                            if s2.startswith('H') and ekezet_nelkul(HK.kiejt(szoto)) == ekezet_nelkul(tag):
                                s = s2
                if s:
                    par.append(s)
            if len(par) == 2:
                hu_szavak = {}
                for k in versek:
                    for hu, s2 in adat.parok.get(k, []):
                        if s2 in par:
                            hu_szavak.setdefault(s2, set()).add(hu.lower())
                jeloltek.setdefault(tuple(par), {}).update(
                    {s: jeloltek.get(tuple(par), {}).get(s, set()) | v for s, v in hu_szavak.items()})
        ki = []
        for kif in m.group(1).split(';'):
            kif = kif.strip()
            szavak = [w for w in re.findall(r'[%s]+' % BETU, kif.lower()) if w not in ('és', 'a', 'az')]
            if len(szavak) != 2:
                continue
            legjobb, pont = None, 0
            for par, hu in jeloltek.items():
                p = 0
                for w in szavak:
                    p += max([_kozos_elotag(w, h) for s in par for h in hu.get(s, set())] or [0])
                    lex = self.lanc_szo(w)
                    if lex and lex['strongok'] & set(par):
                        p += 5
                if p > pont:
                    legjobb, pont = par, p
            if legjobb:
                ki.append((kif, list(legjobb), [to_rx(tovek(w)) for w in szavak]))
        return ki

    def lanc_szo(self, szo):
        for hu, d in self.szavak.items():
            if d['rx'].match(szo):
                return d
        return None


def sj(d):
    return '+'.join(sorted(d['strongok']))


def _gorog_to(lemma):
    import unicodedata
    s = ''.join(c for c in unicodedata.normalize('NFD', lemma.lower()) if not unicodedata.combining(c))
    for elo in ('δια', 'κατα', 'επι', 'απο', 'συν'):
        if s.startswith(elo) and len(s) > len(elo) + 3:
            return s[len(elo):]
    return s


def _kozos_elotag(a, b):
    a, b = re.sub(r'^meg', '', a), re.sub(r'^meg', '', b)
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]:
        n += 1
    return n if n >= 3 else 0


# ---------------------------------------------------------------------------
# Kinyerés: rések és a kapcsolodas
# ---------------------------------------------------------------------------
class Egyseg:
    """Egy ellenőrzési egység: egy mondat (rés) vagy egy adatsor kapcsolodas-prózája."""

    def __init__(self, forras, hely, szoveg, alap_ref=None, fejezet_strong=None):
        self.forras, self.hely, self.szoveg = forras, hely, szoveg
        self.alap_ref, self.fejezet_strong = alap_ref, fejezet_strong


MONDATHATAR = re.compile(r'(?<=[.!?])\s+(?=[„(*]?[A-ZÁÉÍÓÖŐÚÜŰ0-9])')


def mondatok(bekezdes):
    reszek, akt = [], ''
    for darab in MONDATHATAR.split(bekezdes):
        akt = (akt + ' ' + darab).strip() if akt else darab
        # rövidítés vagy igehely-szám után nem zárunk („vö.”, „1Móz 3:17.” után nagybetűs mondat igen)
        if re.search(r'(?:\bvö|\bkb|\bpl|\bi\.e|\bi\.sz)\.$', akt):
            continue
        reszek.append(akt)
        akt = ''
    if akt:
        reszek.append(akt)
    return reszek


def res_egysegek(md_ut):
    with open(md_ut, 'r', encoding='utf-8') as f:
        sorok = f.read().split('\n')
    egysegek, res, fejezet_strong = [], None, None
    for i, sor in enumerate(sorok, 1):
        m = re.match(r'<!--\s*RÉS-KEZDET:\s*([\w]+)\s*-->', sor.strip())
        if m:
            res, fejezet_strong = m.group(1), None
            continue
        if re.match(r'<!--\s*RÉS-VÉGE', sor.strip()):
            res = None
            continue
        if res is None:
            continue
        s = sor.strip()
        if s.startswith('#'):
            fs = re.findall(r'\b([HG]\d{4})\b', s)
            fejezet_strong = fs[0] if len(fs) == 1 else None
            continue
        if not s or s.startswith('<!--') or s.startswith('*Proveniencia') or s.startswith('【') or s.startswith('|'):
            continue
        s = re.sub(r'<!--.*?-->', '', s)
        for mo in mondatok(s):
            egysegek.append(Egyseg('rés:' + res, '%s:%d' % (os.path.basename(md_ut), i), mo,
                                   fejezet_strong=fejezet_strong))
    return egysegek


def kapcsolodas_egysegek(elof_sorok, elof_sorszam):
    ki = []
    for d in elof_sorok:
        szoveg = d.get('kapcsolodas', '').strip()
        if szoveg:
            ki.append(Egyseg('adat:kapcsolodas', 'elofordulasok.tsv:%d' % elof_sorszam[d['igehely']], szoveg,
                             alap_ref=d.get('igehely', '')))
    return ki


# ---------------------------------------------------------------------------
# Ellenőrzés
# ---------------------------------------------------------------------------
class Sor:
    def __init__(self, egyseg, vers, allitas, itelet, bizonyitek, tipus, jelzes=''):
        self.egyseg, self.vers, self.allitas = egyseg, vers, allitas
        self.itelet, self.bizonyitek, self.tipus, self.jelzes = itelet, bizonyitek, tipus, jelzes
        self.kezi_id = None


SZOPAR_ALANY_TAV = 2   # a szópár mellett megnevezett szó legfeljebb ennyi szóra áll a szópártól
FORDULAT_TAV = 80      # a rövid idézett fordulat és a hozzá tartozó igehely-csoport legnagyobb távolsága

ABSZOLUT = re.compile(r'(?<![%s])(?:először|elsőként|egyetlen|mindig|soha|sehol|kizárólag|mindhárom'
                      r'|mind a (?:két|három|négy|öt|hat)|minden előfordulás\w*)(?![%s])' % (BETU, BETU), re.I)
IDEZET_KI = re.compile(r'„[^”]*”|"[^"]*"')


VONATKOZO = re.compile(r'^[\s),]*(?:ahol|amely\w*|ami\w*|aki\w*|mely\w*)(?![%s])[^,;]*[,;]?' % BETU, re.I)


def zaradek_sajat(zaradek):
    """Az előző igehely-csoportra visszautaló vonatkozó mellékmondat („…(Ézs 24:5-6), ahol az átok más héber szóval
    …, a”) nem a következő csoport állítása: a záradék eleje a mellékmondat végéig levágva."""
    m = VONATKOZO.match(zaradek)
    return zaradek[m.end():] if m else zaradek


def zaradek_vege(zaradek):
    """A záradék utolsó tagmondata (a ; : — utáni rész), legfeljebb 120 karakter: az implicit szó-jelzés ablaka."""
    vege = re.split(r'[;:—]', zaradek)[-1]
    return vege[-120:]


NEGALT = re.compile(r'(?:a|az)\s+([%s]+)\s+szav(?:a|ai)\s+nélkül' % BETU, re.I)
MAS_SZO = re.compile(r'\bmás\s+(?:héber\s+|görög\s+)?(?:kulcs)?szó(?:val|t)?\b', re.I)
POZITIV = re.compile(r'(?:a|az)\s+([%s]+)\s+szava\b(?!\s+nélkül)' % BETU, re.I)
SZAM_RX = re.compile(r'(?<![%s0-9])(\d{1,3}(?:[  ]\d{3})+|\d+|%s)(?:-[aoeö]t)?\s+((?:[%s-]+\s+){0,2}?)'
                     r'(hely\w*|vers\w*|igehely\w*)\b' % (BETU, '|'.join(sorted(SZAMSZAVAK, key=len, reverse=True)),
                                                           BETU), re.I)
SAJAT_FORDITAS = re.compile(r'saját fordítás|sajat forditas|szó szerint:|ford\.\s*:', re.I)   # = E34_JELOLES
JELENTES_GLOSSZA = re.compile(r'(?<![%s])(?:jelentés\w*|jelenti|értelemben|glossz\w*|BDB|Thayer|LSJ|UBS)(?![%s])'
                              % (BETU, BETU), re.I)
RESZHALMAZ = re.compile(r'(?<![%s])(?:közül|csak|ebben|ezekben|amely\w*|ahol)(?![%s])' % (BETU, BETU), re.I)
SZAM_ELIDALT = re.compile(r'(\d+)-[aoeö]t\s+(?:a|az)\s+(Genezisből|Ószövetség többi könyvéből|Újszövetségből)')
STRONG_SZAM = re.compile(r'\b(?:szó|ige)\b[^.;]*?\b(\d{1,3}(?:[  ]\d{3})*|\d+)\s+versben\s+áll')


def neg_ervenyes(szoveg, neg, kezdet, zaradek):
    """A „X szava nélkül” tagadás erre a csoportra szól-e: a záradékban áll, vagy előtte, és a kettő között
    (a zárójeles igehely-csoportokat leszámítva) nincs vessző és záró zárójel (más tagmondat, zárójeles betét)."""
    if neg.end() > kezdet:
        return False
    kozte = re.sub(r'\([^()]*\)', '', szoveg[neg.end():kezdet])
    return ',' not in kozte and ')' not in kozte


def szam_ertek(s):
    s = s.lower().replace(' ', '').replace(' ', '')
    return int(s) if s.isdigit() else SZAMSZAVAK.get(s)


class Ellenor:
    def __init__(self, mid, adat, szk, elof_sorok, igeh):
        self.mid, self.adat, self.szk, self.elof, self.igeh = mid, adat, szk, elof_sorok, igeh
        self.sorok = []
        self.szamok = self._szamok()
        self.motivum_versek = [k for d in elof_sorok for k in adat.versek(d['igehely'])]

    def _szamok(self):
        def versszam(sorok):
            return len({k for d in sorok for k in self.adat.versek(d['igehely'])})

        def konyv(d):
            return d['igehely'].rsplit(' ', 1)[0]
        osszes = self.elof
        csop = {
            'összes': osszes,
            'Genezis': [d for d in osszes if konyv(d) == '1Móz'],
            'Ószövetség többi': [d for d in osszes if konyv(d) != '1Móz' and konyv(d) not in UJSZ_KONYVEK],
            'ószövetségi': [d for d in osszes if konyv(d) not in UJSZ_KONYVEK],
            'újszövetségi': [d for d in osszes if konyv(d) in UJSZ_KONYVEK],
            'tematikus': [d for d in osszes if d.get('gerinc_elem', '').startswith('tematikus')],
        }
        return {k: (len(v), versszam(v)) for k, v in csop.items()}

    def _szam_csoport(self, kornyezet):
        k = kornyezet.lower()
        if 'tematikus' in k or 'szavai nélkül' in k:
            return 'tematikus'
        if 'genezis' in k:
            return 'Genezis'
        if 'többi' in k and 'ószövetség' in k:
            return 'Ószövetség többi'
        if 'újszövetség' in k:
            return 'újszövetségi'
        if 'ószövetség' in k:
            return 'ószövetségi'
        return None

    # --- egység feldolgozása
    def egyseg(self, e):
        szoveg = e.szoveg
        csoportok = self.igeh.csoportok(szoveg)
        szoveg_refek = [r for _, _, rs in csoportok for r in rs]
        if e.alap_ref:
            # az adatsor prózája a sor saját versére szól; a benne említett más versek csak az idézethez jelöltek
            idezet_refek = [e.alap_ref] + [r for r in szoveg_refek if r != e.alap_ref]
            vizsgalt = [(len(szoveg), len(szoveg), [e.alap_ref], szoveg)]
        else:
            idezet_refek = szoveg_refek
            vizsgalt, elozo = [], 0
            for kezdet, veg, refek in csoportok:
                zaradek = szoveg[elozo:kezdet] if kezdet > elozo else szoveg[max(0, kezdet - 200):kezdet]
                if elozo:
                    zaradek = zaradek_sajat(zaradek)
                vizsgalt.append((kezdet, veg, refek, zaradek))
                elozo = veg
        lefedett = set()   # a vers, amelyre az egész állítás egy idézet (gépi ítélet született)
        self._idezetek(e, szoveg, idezet_refek, lefedett)
        if not e.alap_ref:
            self._fordulat(e, szoveg, csoportok, self.motivum_versek)
        self._szamok_ell(e, szoveg, [(k, v) for k, v, _ in csoportok])
        abszolut = ABSZOLUT.search(IDEZET_KI.sub(' ', szoveg))
        if not vizsgalt:
            if abszolut and e.forras.startswith('rés:'):
                self.sorok.append(Sor(e, '–', szoveg, 'kézi', '⚑ kizárólagos vagy egyetemes állítás („%s”) '
                                      'igehely nélkül: lekérdezéssel igazolandó, vagy olvasatként jelölendő'
                                      % abszolut.group(0), 'kézi', jelzes='⚑'))
            return
        neg = NEGALT.search(szoveg)
        mas = MAS_SZO.search(szoveg)
        mas_csoport = None
        if mas:
            elotte = [c for c in vizsgalt if c[1] <= mas.start() and mas.start() - c[1] < 80]
            mas_csoport = elotte[-1][0] if elotte else None
        for kezdet, veg, refek, zaradek in vizsgalt:
            for ref in refek:
                versek = self.adat.versek(ref)
                if not versek:
                    self.sorok.append(Sor(e, ref, szoveg, 'kézi', 'az igehely nem oldható fel a Károli-táblán',
                                          'feloldás'))
                    continue
                strongok = self.adat.strongok(versek)
                jelzesek = []
                n0 = len(self.sorok)
                # negatív szójelenlét: a tagadás a záradékban, vagy előtte, tagmondat-határ nélkül
                if neg and (e.alap_ref or neg_ervenyes(szoveg, neg, kezdet, zaradek)):
                    self._negalt(e, ref, versek, strongok, neg.group(1), szoveg)
                if mas and (e.alap_ref or mas_csoport == kezdet or mas.group(0) in zaradek_vege(zaradek)):
                    mas_zaradek = zaradek + ' ' + szoveg[veg:mas.end()] if mas.start() >= veg else zaradek
                    self._mas_szo(e, ref, versek, strongok, mas_zaradek, szoveg, idezet_refek)
                # pozitív szójelenlét a záradékban
                for m in POZITIV.finditer(zaradek):
                    d = self.szk.lanc_szo(m.group(1))
                    if not d or (neg and neg.group(1) == m.group(1)):
                        continue
                    van = bool(d['strongok'] & strongok)
                    self.sorok.append(Sor(e, ref, szoveg, 'egyezik' if van else 'ELTÉR',
                                          'a mondat szerint a %s szava (%s, %s) a versben áll; TAHOT/TAGNT: %s'
                                          % (m.group(1), d['atiras'], sj(d), 'áll' if van else 'NEM áll'),
                                          'szójelenlét'))
                # szópár
                for kif, par, rxek in self.szk.szoparok:
                    if all(rx.search(zaradek) for rx in rxek):
                        hiany = [s for s in par if s not in strongok]
                        if hiany:
                            self.sorok.append(Sor(e, ref, szoveg, 'ELTÉR', 'szópár „%s” (%s): a versből hiányzik: %s'
                                                  % (kif, '+'.join(par), ', '.join(hiany)), 'szópár'))
                            continue
                        alany = self._szopar_alany(zaradek, rxek, versek, par)
                        if alany is None:
                            self.sorok.append(Sor(e, ref, szoveg, 'egyezik', 'szópár „%s” (%s): mindkét szó a versben '
                                                  'áll' % (kif, '+'.join(par)), 'szópár'))
                        else:
                            hu, elfogadott, jeloltek, talalt = alany
                            self.sorok.append(Sor(
                                e, ref, szoveg, 'egyezik' if talalt else 'ELTÉR',
                                'szópár „%s” (%s) a „%s” szóval: a versben a szópár mellett álló szavak: %s; a „%s” '
                                '(%s) %s' % (kif, '+'.join(par), hu, ', '.join(
                                    '%s (%s)' % (x, self._atiras(versek, x)) for x in jeloltek) or '–', hu,
                                    ', '.join(sorted(elfogadott)), 'köztük áll' if talalt else 'NEM áll köztük'),
                                'szópár'))
                # implicit lánc-szó: a záradék végének magyar szava a versben más szót fordít, vagy nincs a versben
                jelzesek += self._implicit(zaradek if e.alap_ref else zaradek_vege(zaradek), versek, strongok, ref)
                if abszolut and (e.alap_ref or abszolut.group(0) in zaradek):
                    jelzesek.append('⚑ kizárólagos vagy egyetemes állítás („%s”): lekérdezéssel igazolandó, vagy '
                                    'olvasatként jelölendő' % abszolut.group(0))
                uj = self.sorok[n0:]
                if any(s.itelet == 'ELTÉR' for s in uj) and not jelzesek:
                    continue   # a gépi ELTÉR már javítást kér
                if ref in lefedett and not jelzesek:
                    continue   # az állítás maga a (megegyező) Károli-idézet
                egyezo = [s.tipus + ': ' + s.bizonyitek for s in uj if s.itelet == 'egyezik']
                self.sorok.append(Sor(e, ref, szoveg, 'kézi', '; '.join(jelzesek + [
                    'gépileg egyezik, de az állítás ennél több — ' + x for x in egyezo]), 'kézi',
                    jelzes='⚑' if jelzesek else ''))

    def _tartalmi(self, s):
        return bool(s) and s not in self.adat.gramm and not s.startswith('H90') and not s.startswith('H99')

    def tartalmi_sor(self, versek):
        """A versek Strong-sorai sorrendben, a grammatikai és az előtag-/toldalék-számok nélkül."""
        return [s for k in versek for s, _, _ in self.adat.szavak.get(k, [])
                if s and s not in self.adat.gramm and not s.startswith('H90') and not s.startswith('H99')]

    def _elfogadott(self, d, hu_rx_lista, versek):
        """Egy magyar szó elfogadott Strong-számai a versben: a lánc szava és a Károli-párosítás szerinti szó."""
        elf = set(d['strongok'])
        for k in versek:
            for husz, s in self.adat.parok.get(k, []):
                if s and self._tartalmi(s) and any(rx.match(husz.lower()) for rx in hu_rx_lista):
                    elf.add(s)
        return elf

    def _szopar_alany(self, zaradek, szopar_rxek, versek, par):
        """A szópár mellett megnevezett lánc-szó (pl. „a föld megtelt erőszakkal”): a héber szórendben a szópár két
        szava mellett (előttük és utánuk két-két szó, köztük) áll-e. None, ha a záradék ilyen szót nem nevez meg."""
        lanc = {x for d in self.szk.szavak.values() for x in d['strongok']}
        if not (set(par) & lanc):
            return None   # névszói szópár (tövis és bogáncs): nincs alanya, a próba az igei szópárra szól
        nev = None
        tokok = [t.lower() for t in re.findall(r'[%s]+' % BETU, zaradek)]
        par_poz = [i for i, t in enumerate(tokok) if any(rx.match(t) for rx in szopar_rxek)]
        for i, t in enumerate(tokok):
            if i in par_poz or not any(abs(i - j) <= SZOPAR_ALANY_TAV for j in par_poz):
                continue
            for hu, d in self.szk.szavak.items():
                if d['rx'].match(t) and not (d['strongok'] & set(par)):
                    nev = (hu, d)
                    break
            if nev:
                break
        if not nev:
            return None
        hu, d = nev
        elfogadott = self._elfogadott(d, [d['rx']], versek)
        sor = self.tartalmi_sor(versek)
        jeloltek, talalt = [], False
        for i, s2 in enumerate(sor):
            if s2 != par[1]:
                continue
            js = [j for j in range(max(0, i - 3), min(len(sor), i + 4)) if sor[j] == par[0] and j != i]
            if not js:
                continue
            j = min(js, key=lambda x: abs(x - i))
            lo, hi = min(i, j), max(i, j)
            kor = [sor[x] for x in range(max(0, lo - 2), min(len(sor), hi + 3)) if x not in (i, j)]
            jeloltek += [x for x in kor if x not in jeloltek]
            talalt = talalt or bool(set(kor) & elfogadott)
        if not jeloltek:
            return None
        return hu, elfogadott, jeloltek, talalt

    def _fordulat(self, e, szoveg, csoportok, motivum_versek):
        """Kétszavas idézett fordulat („föld színéről”): a motívum versei közül abban, ahol a Károli egymás mellett
        hozza, a Károli-párosítás adja a két szó tartalmi Strong-számát; a fordulathoz tartozó igehely-csoport (utána, vagy
        előtte, legfeljebb FORDULAT_TAV karakterre) verseiben ezek szomszédosak-e a héber szórendben."""
        for m in OK.IDEZET_RX.finditer(szoveg):
            idez = m.group(2) or m.group(3)
            szavak = OK.normal_szoveg(idez or '').split()
            if len(szavak) != 2:
                continue
            utana = [c for c in csoportok if 0 <= c[0] - m.end() <= FORDULAT_TAV]
            elotte = [c for c in csoportok if 0 <= m.start() - c[1] <= FORDULAT_TAV]
            csop = utana[0] if utana else (elotte[-1] if elotte else None)
            if not csop:
                continue
            minta = self._fordulat_minta(szavak, motivum_versek)
            if not minta:
                continue
            # „… is áll (A, B, C)”: minden versre szól; különben (pl. „… kerül a következmény alá (A, B, C)”)
            # a felsorolás tagonként értendő, és elég, ha a fordulat a csoport egyik versében áll
            koztes = szoveg[m.end():csop[0]] if csop[0] >= m.end() else ''
            mindre = bool(re.search(r'(?<![%s])(?:áll|állnak|szerepel|szerepelnek|visszatér|olvasható)(?![%s])'
                                    % (BETU, BETU), koztes))
            eredm = []
            for ref in csop[2]:
                versek = self.adat.versek(ref)
                if not versek:
                    continue
                sor = self.tartalmi_sor(versek)
                van = any(set(sor[x:x + 2]) == set(minta) for x in range(len(sor) - 1))
                eredm.append((ref, sor, van))
            if not mindre and any(v for _, _, v in eredm):
                eredm = [x for x in eredm if x[2]]
            for ref, sor, van in eredm:
                hiany = [x for x in minta if x not in sor]
                self.sorok.append(Sor(e, ref, '„%s”' % idez, 'egyezik' if van else 'ELTÉR',
                                      'a „%s” szavai (%s) a héber szórendben %s' % (
                                          idez, '+'.join('%s (%s)' % (x, self._atiras(motivum_versek, x))
                                                         for x in minta),
                                          'egymás mellett állnak' if van else 'NEM állnak egymás mellett' + (
                                              ' (a versből hiányzik: %s)' % ', '.join(hiany) if hiany else '')),
                                      'fordulat'))

    def _fordulat_minta(self, szavak, motivum_versek):
        elotag = [w[:4] for w in szavak]
        for k in motivum_versek:
            szavankent = {}
            for poz, hu, s in self.adat.parok_poz.get(k, []):
                szavankent.setdefault(poz, [OK.normal_szoveg(hu), []])[1].append(s)
            rend = [szavankent[p] for p in sorted(szavankent, key=lambda x: int(x) if x.isdigit() else 0)]
            for x in range(len(rend) - 1):
                if rend[x][0].startswith(elotag[0]) and rend[x + 1][0].startswith(elotag[1]):
                    a = [s for s in rend[x][1] if self._tartalmi(s)]
                    b = [s for s in rend[x + 1][1] if self._tartalmi(s)]
                    if a and b and a[0] != b[0]:
                        return [a[0], b[0]]
        return None

    def _implicit(self, zaradek, versek, strongok, ref):
        """A záradék lánc-szavai (magyar alak szerint) a vers Strong-sorai mellett: ⚑ jelzések."""
        nyelv = 'G' if ref.rsplit(' ', 1)[0] in UJSZ_KONYVEK else 'H'
        jelzesek, latott = [], set()
        parok = [p for k in versek for p in self.adat.parok.get(k, [])]
        for tok in re.findall(r'[%s]+' % BETU, zaradek):
            tok_l = tok.lower()
            illo = [(hu, d) for hu, d in self.szk.szavak.items() if d['rx'].match(tok_l)]
            if not illo:
                continue
            elfogadott = {s for _, d in illo for s in d['strongok'] if s.startswith(nyelv)}
            if not elfogadott:
                continue   # a lánc szava ezen a nyelven nincs megnevezve (pl. a „föld” az Újszövetségben)
            hu = illo[0][0]
            if hu in latott or elfogadott & strongok:
                latott.add(hu)
                continue
            latott.add(hu)
            nev = ', '.join(sorted(elfogadott))
            masik = sorted({s for husz, s in parok if s and s not in self.adat.gramm and not s.startswith('H90')
                            and any(d['rx'].match(husz.lower()) for _, d in illo)})
            if masik:
                jelzesek.append('⚑ a „%s” itt %s, nem a lánc szava (%s)'
                                % (hu, ', '.join('%s (%s)' % (s, self._atiras(versek, s)) for s in masik), nev))
            else:
                jelzesek.append('⚑ a lánc „%s” szava (%s) nincs a versben' % (hu, nev))
        return jelzesek

    def _atiras(self, versek, s):
        for k in versek:
            for s2, szoto, _ in self.adat.szavak.get(k, []):
                if s2 == s:
                    return HK.kiejt(szoto) if s.startswith('H') else szoto
        return '?'

    def _negalt(self, e, ref, versek, strongok, szo, szoveg):
        if szo.lower() == 'lánc':
            van = sorted({s for d in self.szk.szavak.values() for s in d['strongok'] & strongok})
            self.sorok.append(Sor(e, ref, szoveg, 'ELTÉR' if van else 'egyezik',
                                  'a mondat szerint a lánc szavai nincsenek a versben; TAHOT/TAGNT: %s'
                                  % (('áll: ' + ', '.join(van)) if van else 'egyik sem áll'), 'szójelenlét'))
            return True
        d = self.szk.lanc_szo(szo)
        if not d:
            return False
        van = bool(d['strongok'] & strongok)
        self.sorok.append(Sor(e, ref, szoveg, 'ELTÉR' if van else 'egyezik',
                              'a mondat szerint a %s szava (%s, %s) nincs a versben; TAHOT/TAGNT: %s'
                              % (szo, d['atiras'], sj(d), 'ÁLL' if van else 'nem áll'), 'szójelenlét'))
        return True

    def _mas_szo(self, e, ref, versek, strongok, zaradek, szoveg, osszes_ref):
        """„más (héber) szóval”: (a) a záradék lánc-szava nem áll a versben; (b) idézett mondat szavai más versben."""
        for hu, d in self.szk.szavak.items():
            if d['rx'].search(zaradek):
                van = bool(d['strongok'] & strongok)
                self.sorok.append(Sor(e, ref, szoveg, 'ELTÉR' if van else 'egyezik',
                                      'a mondat szerint itt más szó áll, nem a %s (%s, %s); TAHOT/TAGNT: %s'
                                      % (hu, d['atiras'], sj(d), 'a lánc szava ÁLL' if van else 'nem áll'),
                                      'szójelenlét'))
                return True
        # (b): az idézett mondat (más vers) tartalmi szavai: ha mind a versben állnak, a „más szó” nem igaz
        for m in OK.IDEZET_RX.finditer(szoveg):
            idez = m.group(2) or m.group(3)
            if not idez or len(OK.normal_szoveg(idez).split()) < 3:
                continue
            for forras_ref in osszes_ref:
                fv = self.adat.versek(forras_ref)
                if forras_ref == ref or not OK.karoli_egyezik(idez, OK.normal_szoveg(self.adat.karoli_szoveg(fv))):
                    continue
                idez_szavak = set(OK.normal_szoveg(idez).split())
                tart = sorted({s for k in fv for hu, s in self.adat.parok.get(k, [])
                               if s and s not in self.adat.gramm and not s.startswith('H90')
                               and set(OK.normal_szoveg(hu).split()) & idez_szavak})
                kozos = [s for s in tart if s in strongok]
                if tart and 2 * len(kozos) >= len(tart):   # az idézet tartalmi szavainak legalább fele közös
                    self.sorok.append(Sor(e, ref, szoveg, 'ELTÉR',
                                          'a mondat szerint itt más szó áll, mint a(z) %s idézetében; a(z) %s idézett '
                                          'szavai közül itt is áll: %s' % (forras_ref, forras_ref,
                                                                           ', '.join('%s (%s)' % (s, self._atiras(
                                                                               fv, s)) for s in kozos)),
                                          'szójelenlét'))
                    return True
        return False

    def _idezetek(self, e, szoveg, refek, lefedett):
        if SAJAT_FORDITAS.search(szoveg):
            return   # az E34 jelölése (DT614): a mondat idézete saját fordítás
        for m in OK.IDEZET_RX.finditer(szoveg):
            if m.group(1):
                continue   # zárójeles glossza: nem versidézet (E34)
            if JELENTES_GLOSSZA.search(szoveg[max(0, m.start() - 40):m.start()] + ' ' + szoveg[m.end():m.end() + 25]):
                continue   # szótári jelentés idézőjelben („néven nevezni” jelentésben): nem versidézet
            idez = m.group(2) or m.group(3)
            if not idez or len(OK.normal_szoveg(idez).split()) < 3:
                continue
            if not refek:
                continue
            talalt = None
            for ref in refek:
                versek = self.adat.versek(ref)
                if versek and OK.karoli_egyezik(idez, OK.normal_szoveg(self.adat.karoli_szoveg(versek))):
                    talalt = ref
                    break
            if talalt:
                self.sorok.append(Sor(e, talalt, '„%s”' % idez, 'egyezik', 'Károli 1908: az idézet a vers szövege',
                                      'idézet'))
                if len(refek) == 1:
                    lefedett.add(talalt)
            else:
                self.sorok.append(Sor(e, ', '.join(refek), '„%s”' % idez, 'ELTÉR',
                                      'Károli 1908: az idézet a mondat egyik versének szövegével sem egyezik '
                                      '(a mondat versei: %s)' % ', '.join(refek), 'idézet'))

    def _szamok_ell(self, e, szoveg, ref_szakaszok=()):
        for m in SZAM_ELIDALT.finditer(szoveg):
            csop = {'Genezisből': 'Genezis', 'Ószövetség többi könyvéből': 'Ószövetség többi',
                    'Újszövetségből': 'újszövetségi'}[m.group(2)]
            self._szam_sor(e, szoveg, int(m.group(1)), 'hely', csop, m.group(0))
        for m in SZAM_RX.finditer(szoveg):
            ertek = szam_ertek(m.group(1))
            if ertek is None or any(k <= m.start() < v for k, v in ref_szakaszok):
                continue
            fonev = 'vers' if m.group(3).lower().startswith('vers') else 'hely'
            # gépi ítélet csak a motívum egészére vagy egy minősített részére szóló számra: a „lap”/„motívum” alany
            # legfeljebb négy szóval előtte, részhalmazt jelző szó nélkül („A motívum hat újszövetségi helyén”);
            # minden más szám kézi (pl. „a motívum helyei közül csak ebben a két versben”, „a motívum ívét két … vers”)
            elotte = szoveg[max(0, m.start() - 60):m.start()]
            alany = re.search(r'\b(?:a lap|a motívum)((?:\s+[^\s.;:,]+){0,4})\s*$', elotte, re.I)
            if alany and RESZHALMAZ.search(alany.group(1)):
                alany = None
            if alany and alany.group(1).strip() and not re.match(r'^\s*\d', alany.group(1)) and \
                    not re.search(r'(?<![%s])(?:sorol|ad|áll|tartalmaz)' % BETU, alany.group(1)):
                alany = None   # a szám és az alany között más bővítmény áll („a motívum ívét két … vers”)
            csop = self._szam_csoport(m.group(2)) if alany else None
            if csop is None and alany:
                kovet = re.split(r'[,;:.(]', szoveg[m.end():m.end() + 80])[0]
                csop = self._szam_csoport(kovet) or 'összes'
            if csop is None:
                if e.fejezet_strong and fonev == 'vers':
                    continue   # a Strong-szám versszáma külön (STRONG_SZAM)
                self.sorok.append(Sor(e, '–', m.group(0), 'kézi',
                                      'szám; a viszonyítási alap a mondatból nem állapítható meg (a motívum adata: '
                                      '%d hely, %d vers)' % self.szamok['összes'], 'szám'))
                continue
            self._szam_sor(e, szoveg, ertek, fonev, csop, m.group(0))
        if e.fejezet_strong:
            for m in STRONG_SZAM.finditer(szoveg):
                ertek = szam_ertek(m.group(1))
                n = self.adat.strong_versszam.get(e.fejezet_strong)
                if ertek is None or n is None:
                    continue
                self.sorok.append(Sor(e, '–', m.group(0), 'egyezik' if n == ertek else 'ELTÉR',
                                      '%s a TAHOT/TAGNT teljes táblán %d versben áll' % (e.fejezet_strong, n),
                                      'szám'))

    def _szam_sor(self, e, szoveg, ertek, fonev, csop, allitas):
        hely, vers = self.szamok[csop]
        valos = vers if fonev == 'vers' else hely
        self.sorok.append(Sor(e, '–', allitas, 'egyezik' if valos == ertek else 'ELTÉR',
                              'adat/elofordulasok.tsv (id=%s), %s: %d hely, %d vers' % (self.mid, csop, hely, vers),
                              'szám'))


# ---------------------------------------------------------------------------
# Lektori összevetés
# ---------------------------------------------------------------------------
def lektor_tetelek(ut):
    with open(ut, 'r', encoding='utf-8') as f:
        szoveg = f.read()
    tetelek = []
    for m in re.finditer(r'^\*\*(\d+)\.\s+(.*?)\*\*\s*$(.*?)(?=^\*\*\d+\.|^## |\Z)', szoveg, re.M | re.S):
        test = m.group(3)
        vonatkozik = re.search(r'Erre vonatkozik:(.*)', test)
        gond = re.search(r'Mi a gond:(.*)', test)
        tetelek.append({'szam': int(m.group(1)), 'cim': m.group(2).strip(),
                        'vonatkozik': vonatkozik.group(1) if vonatkozik else '',
                        'gond': gond.group(1) if gond else ''})
    return tetelek


def lektor_pontossagi(t):
    return bool(re.search(r'\b[14]\.\s+(?:és\s+\d\.\s+)?kérdés|\b\d\.\s+és\s+[14]\.\s+kérdés', t['gond']))


NEM_LATJA_FORRAS = 'nem látja (a forrásban van, gépi tétel nélkül)'
NEM_LATJA_GENERALT = 'nem látja (nem a forrás prózája: generált blokk)'


def lektor_darabok(t):
    """A tétel „Erre vonatkozik” idézetei (a beágyazott „…” idézőjelekkel együtt), normalizált darabokra bontva."""
    darabok = []
    for idez in re.split(r'”\s*/\s*„', t['vonatkozik']):
        m = re.search(r'„(.*)”', idez)
        if not m:
            continue
        for d in re.split(r'…|\.\.\.', m.group(1)):
            n = OK.normal_szoveg(d)
            if len(n) >= 20:   # rövid darab (egy fordulat) sok egységre illene: csak a mondatnyi idézet azonosít
                darabok.append(n[:60])
    return darabok


def lektor_illeszt(t, sorok, egysegek):
    """A tétel idézett szövegrészeit tartalmazó egységek ítéletei -> (eredmény, sorok)."""
    darabok = lektor_darabok(t)
    if not darabok:
        return NEM_LATJA_GENERALT, []
    talalat = [s for s in sorok if any(d in OK.normal_szoveg(s.egyseg.szoveg) for d in darabok)]
    if not talalat:
        if any(any(d in OK.normal_szoveg(e.szoveg) for d in darabok) for e in egysegek):
            return NEM_LATJA_FORRAS, []
        return NEM_LATJA_GENERALT, []
    if any(s.itelet == 'ELTÉR' for s in talalat):
        return 'gépi', talalat
    if any(s.itelet == 'kézi' and s.jelzes for s in talalat):
        return 'kézi ⚑', talalat
    if any(s.itelet == 'kézi' for s in talalat):
        return 'kézi', talalat
    return 'nem látja (gépileg egyezik)', talalat


# ---------------------------------------------------------------------------
# Jelentés
# ---------------------------------------------------------------------------
def rovid(s, n=240):
    """A gépi tábla állítás-cellája: a hosszú mondat eleje (a teljes mondat a forrás során, a hely oszlop szerint)."""
    s = (s or '').replace('\n', ' ')
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + ' …'


def cella(s):
    return (s or '').replace('|', '¦').replace('\n', ' ')


def jelentes(mid, ell, adat, lektor=None, scope_forras='', egysegek=()):
    sorok = ell.sorok
    kezi = [s for s in sorok if s.itelet == 'kézi']
    # kézi azonosító: egységenként és versenként egy
    kulcsok = {}
    for s in kezi:
        k = id(s.egyseg)   # egységenként egy tétel: a mondat egyszer, alatta versenként a bizonyíték
        if k not in kulcsok:
            kulcsok[k] = 'K%d' % (len(kulcsok) + 1)
        s.kezi_id = kulcsok[k]
    elter = [s for s in sorok if s.itelet == 'ELTÉR']
    egyez = [s for s in sorok if s.itelet == 'egyezik']
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    ki = []
    if lektor:
        tet = [t for t in lektor_tetelek(lektor) if lektor_pontossagi(t)]
        eredm = [(t, *lektor_illeszt(t, sorok, egysegek)) for t in tet]
        def db(x):
            return sum(1 for _, r, _ in eredm if r == x)
        nem = db(NEM_LATJA_FORRAS) + db(NEM_LATJA_GENERALT) + db('nem látja (gépileg egyezik)')
        ki.append('**Próba a lektor %d pontossági tételén (%s): gépileg megfogja %d, kézi listára teszi %d '
                  '(ebből ⚑ jelzéssel %d), nem látja %d (ebből %d generált blokkban áll, nem a forrás prózájában; '
                  '%d a forrásban gépi tétel nélkül; %d-nál a gépi ítélet „egyezik”).**'
                  % (len(tet), os.path.basename(lektor), db('gépi'), db('kézi') + db('kézi ⚑'), db('kézi ⚑'),
                     nem, db(NEM_LATJA_GENERALT), db(NEM_LATJA_FORRAS), db('nem látja (gépileg egyezik)')))
        ki.append('')
    ki.append('# ALLITAS %s — a próza versre hivatkozó állításai' % mid)
    ki.append('')
    ki.append('<!-- GENERÁLT: eszkozok/proza_allitas.py — kézzel nem szerkesztendő; újrafuttatással frissül. -->')
    ki.append('')
    ki.append('Forrás: `motivumok/%s.md` értelmező rései és az `adat/elofordulasok.tsv` `kapcsolodas` mezője '
              '(id=%s). Kapu-szint: JELENTÉS. Gépi ítélet: **egyezik** / **ELTÉR** / **kézi** (az ellenőrzési '
              'listán, `K<n>`). A ⚑ gépi jelzés a kézi sorban: a magyar szó a versben más héber/görög szót fordít, '
              'mint a lánc szava, vagy a lánc szava nincs a versben.' % (mid, mid))
    ki.append('')
    ki.append('Összesen: %d gépi sor (ELTÉR %d, egyezik %d), %d kézi tétel (ebből ⚑ %d).'
              % (len(elter) + len(egyez), len(elter), len(egyez), len(kulcsok),
                 len({s.kezi_id for s in kezi if s.jelzes})))
    ki.append('')
    if lektor:
        ki.append('## Összevetés a lektorral')
        ki.append('')
        ki.append('A pontossági tétel: a lektor „Mi a gond” sora az 1. (az igehely maga) vagy a 4. kérdést nevezi. '
                  'Illesztés: a tétel idézett szövegrésze az ellenőrzési egység szövegében.')
        ki.append('')
        ki.append('| Lektor | Hely | Eredmény | Sorok |')
        ki.append('|---|---|---|---|')
        for t, r, ts_ in eredm:
            hiv = ', '.join(sorted({(s.kezi_id or s.itelet) + ('⚑' if s.jelzes else '') for s in ts_
                                    if s.itelet != 'egyezik'}))
            ki.append('| %d | %s | %s | %s |' % (t['szam'], cella(t['cim'][:70]),
                                                 r, cella(hiv)))
        ki.append('')
    ki.append('## Gépi ítéletek')
    ki.append('')
    ki.append('| # | Hely | Állítás | Vers | Gépi ítélet | Bizonyíték |')
    ki.append('|---|---|---|---|---|---|')
    n = 0
    for s in elter + egyez:
        n += 1
        ki.append('| %d | %s (%s) | %s | %s | %s | %s: %s |'
                  % (n, s.egyseg.hely, s.egyseg.forras, cella(rovid(s.allitas)), cella(s.vers),
                     '**ELTÉR**' if s.itelet == 'ELTÉR' else 'egyezik', s.tipus, cella(s.bizonyitek)))
    ki.append('')
    ki.append('## Ellenőrzési lista (kézi)')
    ki.append('')
    ki.append('Minden tételnél a kérdés: azt mondja-e a vers (a Károli és a héber/görög sor szerint), amit az '
              'állítás neki tulajdonít — az alany, a tárgy, a szó és a kapcsolat. A ⚑ tételek elöl.')
    ki.append('')
    rendezett = sorted(kulcsok.items(), key=lambda kv: (0 if any(s.jelzes for s in kezi if s.kezi_id == kv[1])
                                                        else 1, int(kv[1][1:])))
    for eid, kid in rendezett:
        tag = [s for s in kezi if s.kezi_id == kid]
        e = tag[0].egyseg
        versek_rendben = []
        for s in tag:
            if s.vers not in versek_rendben:
                versek_rendben.append(s.vers)
        ki.append('### %s%s · %s (%s) · %s' % (kid, ' ⚑' if any(s.jelzes for s in tag) else '', e.hely, e.forras,
                                                 ', '.join(versek_rendben)))
        ki.append('')
        ki.append('> %s' % e.szoveg.replace('\n', ' '))
        ki.append('')
        for vers in versek_rendben:
            versek = adat.versek(vers) if vers != '–' else []
            bizonyitek = [s.bizonyitek for s in tag if s.vers == vers and s.bizonyitek]
            if not versek and not bizonyitek:
                continue
            ki.append('- **%s**' % vers)
            if versek:
                ki.append('  - Károli: %s' % adat.karoli_szoveg(versek))
                ki.append('  - Héber/görög: %s' % (adat.heber_sor(versek) or '–'))
            for b in bizonyitek:
                ki.append('  - Gépi: %s' % b)
        ki.append('')
    ki.append('(proveniencia: scope=%s | forras=eszkozok/proza_allitas.py; TAHOT_kivonat.tsv, TAGNT_kivonat.tsv, '
              'Karoli_1908.tsv, adat/elofordulasok.tsv, adat/karoli_strong/parok_*.tsv (modell-kimenet, javaslat: '
              'csak jelzés) | ts=%s)' % (scope_forras, ts))
    return '\n'.join(ki) + '\n'


def futtat(mid, md_ut=None, elof_ut=T_ELOF):
    md_ut = md_ut or os.path.join(ROOT, 'motivumok', '%s.md' % mid)
    with open(md_ut, 'r', encoding='utf-8') as f:
        forras = f.read()
    elof_sorok, elof_sorszam = [], {}
    sorszam = 0
    with open(elof_ut, 'r', encoding='utf-8') as f:
        fej = None
        for sor in f:
            sorszam += 1
            sor = sor.rstrip('\n').rstrip('\r')
            if sor.startswith('#') or not sor:
                continue
            if fej is None:
                fej = sor.split('\t')
                continue
            d = dict(zip(fej, sor.split('\t')))
            if d.get('id') == mid:
                elof_sorok.append(d)
                elof_sorszam[d['igehely']] = sorszam
    adat = Adat()
    igeh = Igehelyek()
    egysegek = res_egysegek(md_ut) + kapcsolodas_egysegek(elof_sorok, elof_sorszam)
    versek = set()
    for e in egysegek:
        for _, _, refek in igeh.csoportok(e.szoveg):
            for r in refek:
                versek.update(adat.versek(r))
        if e.alap_ref:
            versek.update(adat.versek(e.alap_ref))
    for d in elof_sorok:
        versek.update(adat.versek(d['igehely']))
    fej_strongok = {e.fejezet_strong for e in egysegek if e.fejezet_strong}
    adat.betolt_szavak(versek, fej_strongok)
    adat.betolt_parok(versek)
    szk = Szokeszlet(forras, elof_sorok, adat)
    ell = Ellenor(mid, adat, szk, elof_sorok, igeh)
    for e in egysegek:
        ell.egyseg(e)
    ell.egysegek = egysegek
    return ell, adat, szk, len(egysegek)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('id', help='motívum-azonosító, pl. HAMART-001')
    ap.add_argument('--forras', help='a kézi forrás útja (alapértelmezés: motivumok/<ID>.md)')
    ap.add_argument('--lektor', help='lektori kérdéslista az összevetéshez (naplok/KIADAS_<ID>_lektor.md szerkezet)')
    ap.add_argument('--kimenet', help='a jelentés útja (alapértelmezés: naplok/ALLITAS_<ID>.md)')
    ap.add_argument('--szigoru', action='store_true', help='1-es kilépőkód, ha van ELTÉR-sor')
    a = ap.parse_args()
    ell, adat, szk, n_egyseg = futtat(a.id, a.forras)
    kimenet = a.kimenet or os.path.join(ROOT, 'naplok', 'ALLITAS_%s.md' % a.id)
    scope = 'motivumok/%s.md (rések) + adat/elofordulasok.tsv kapcsolodas (id=%s), %d egység' % (a.id, a.id, n_egyseg)
    szoveg = jelentes(a.id, ell, adat, a.lektor, scope, ell.egysegek)
    with open(kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    elter = sum(1 for s in ell.sorok if s.itelet == 'ELTÉR')
    print('%s: %d egység; lánc-szavak: %s; szópárok: %s' % (
        a.id, n_egyseg, ', '.join('%s=%s' % (k, sj(v)) for k, v in szk.szavak.items()),
        '; '.join('%s=%s' % (k, '+'.join(p)) for k, p, _ in szk.szoparok)))
    print('ELTÉR: %d, egyezik: %d, kézi sor: %d -> %s' % (
        elter, sum(1 for s in ell.sorok if s.itelet == 'egyezik'), sum(1 for s in ell.sorok if s.itelet == 'kézi'),
        kimenet))
    if szoveg.startswith('**Próba'):
        print(szoveg.split('\n', 1)[0])
    return 1 if (a.szigoru and elter) else 0


if __name__ == '__main__':
    sys.exit(main())
