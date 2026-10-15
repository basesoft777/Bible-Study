#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/f93_tipnr_token_hiany.py -- F93: a TIPNR token nélküli alapszámainak osztályozása.

Bemenet: a kész pardes.db (CSAK OLVASÁS; argumentum, vagy PARDES_DB, vagy ./pardes.db).
A `tipnr` táblának azok az utótag nélküli sorai, amelyek `strong` értéke a `token_strong`-ban
nem szerepel (a #88 levágott utótagos sora nem tartozik ide). Kimenet: naplok/F93_alapszamok.tsv
(alapszámonként egy sor). Jelölés, nem javítás: a TIPNR/TAGNT/TAHOT és a pardes.db nem változik.

Névegyeztetés (a versen lévő token megkeresése) -- a repó adatából, kétféle bizonyíték:
  (1) TIPNR-azonosság: ugyanazon a versen ugyanazzal a névcímkével (`nev`) van másik TIPNR-sor,
      amelynek Strong-száma a vers tokenjei között megvan (utótagos TIPNR-sor is számít);
  (2) glossz-egyezés: a vers valamely tokenének `Rövid jelentés` vagy `Angol tükörfordítás` mezője
      egyezik a névcímkével vagy a Névváltozat egyik nagybetűvel kezdődő névalakjával;
  (3) több tokenre bontott név: a versen EGYMÁST KÖVETŐ tokenek (legfeljebb 5) azonos nevű glosszái
      (mind Rövid jelentés, vagy mind Angol tükörfordítás; a [..] és <..> betoldások nélkül, írásjel-
      és kisbetű-különbség figyelmen kívül hagyva) együtt SZIGORÚAN egyenlők a névcímkével vagy a
      Névváltozat valamelyik névalakjával (pl. Nea+Polis = Neapolis, Ben-+Hesed = Ben-hesed). Asszociatív
      vagy jelentésbeli egyezés nem elég; minden tokennek ki kell tennie a névalak egy részét. Az
      egyetlen tokenes, kisbetűs névalak (pl. „villages”) is ide tartozik (pontos egyenlőség).
A három bizonyíték együtt adja a társ-tokenek listáját (nyelvtől függetlenül, egységesen). Egy találat
"gyenge", ha a token glosszája nem egyezik a névalakkal (az összetartozás csak a TIPNR névcímkén
alapul). Szabály, MINDKÉT nyelvre: ha a sorban nincs kiadás-/fordítás-jelölés, és a versen csak gyenge
társ van, az osztály "nem eldönthető" (így jelölés nélküli "szövegváltozat" vagy "alak-/névhasítás"
sem lehet gyenge találatból); jelölés mellett a glossz eltérése maga lehet a jelzés (pl. görög TR-jelölés).
Pusztán az, hogy a versen más nevű
token van, NEM bizonyíték (és az indoklás sem állítja azt): ez az „azonos nevű” hamis állítás hibája volt.

Osztályok:
  szövegváltozat      (CSAK görög) a névhez illő token `Kritikai kiadás` mezője a TR-t nem tartalmazza.
                      Kiadás-jelölés (TR/Byz) a Névváltozatban: a névhez illő bármely token számít.
                      Jelölés nélkül (DT-F93c) CSAK olyan token, amelynek glosszája egyezik a névvel
                      (nem „gyenge”, csak névcímke-alapú társ); vegyes találatnál (gyenge és erős token
                      ugyanazon a versen) a gyenge token nem választható, a jelölés nélküli sor
                      szövegváltozat-besorolását csak az erős, TR nélküli token adhatja.
  fordítási névalak   (CSAK héber, DT-F93b) a Névváltozat csak fordítás-jelölést (ESV/KJV/NIV/ASV)
                      hordoz, és a versen a névhez illő token áll
  ketiv/qere          (CSAK héber, DT-F93b) LK/LQ/Mss jelölés, ÉS a TAHOT az adott versen ketiv/qere-
                      jelölést hordoz (idézve); a kivonat ma nem hordoz, ezért ez az osztály üres, és az
                      LK/LQ/Mss sorok „nem eldönthető”-k: „az LK/LQ jelentését a repó nem rögzíti”
  alak-/névhasítás    nincs kiadás-/fordítás-jelölés, a névhez illő token a versen megvan
  számozási eltérés   a versen nincs token, de a szomszédos versben a névhez illő token megvan
  nincs Károli-vers   a TIPNR-sor igehelye üres (LXX.* hely), vagy nem létező Károli-vers (nincs a
                      Karoli_1908.tsv-ben, N-F79b/DT114; a vers-átváltást a Karoli_versmegfeleltetes.tsv
                      sora igazolná, ennek hiányában nincs átváltás, emlékezetből sem képezünk)
  (Egy Károli-vers görög találatánál a Kritikai kiadás mező nem-alapkiadás jelölése -- pl. TR»1 --
   „nem eldönthető”: a »N jelentését a repó nem rögzíti, N-F93c.)
  adathiány           nincs jelölés, és a versen nincs a névhez illő token
  nem eldönthető      minden más; explicit jelölve, nem kitöltve (CLAUDE.md 3. szabály)

Vegyes sorú alapszám (több TIPNR-sor): ha a sorok osztálya versenként eltér, az alapszám
„nem eldönthető” (az indoklás felsorolja a sorok osztályait); csak ha minden sor azonos osztályú,
kapja azt az alapszám. A mostani listában nincs ilyen alapszám (a H3482 és a H3159 sorai is azonos
osztályúak), a szabály tehát jelenleg nem érvényesül, de a kód tartalmazza.

A görög `Kritikai kiadás` alapkiadásai: NA28, NA27, Tyn, SBL, WH, Treg, TR, Byz. A TAHOT-kivonatnak
nincs ilyen mezője (DT-F93b), ezért a G3 (Kritikai kiadás mező) csak a görög szövegváltozat-sorokra áll.

Két futás kimenete bájtazonos: a ts a pardes.db meta.epites_ts értéke, a rendezés kulcsos.
TSV-írás '\\t'.join()-nal (a csv modul tilos).
"""
import collections
import os
import re
import sqlite3
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIMENET = os.path.join(GYOKER, 'naplok', 'F93_alapszamok.tsv')
OSZLOPOK = ['strong', 'nev', 'nevvaltozat', 'igehely', 'osztaly', 'tagnt_strong_a_versen',
            'tagnt_kiadas', 'indoklas', 'proveniencia', 'nyelv', 'tipnr_sorok']
KIADAS_RE = re.compile(r'=([A-Za-z]+(?:,[A-Za-z]+)*)')
# a TAGNT `Kritikai kiadás` mező alapkiadásai (a ritka kéziratjelölések, KJV/NIV maradványok nélkül)
TAGNT_KIADASOK = {'NA28', 'NA27', 'Tyn', 'SBL', 'WH', 'Treg', 'TR', 'Byz'}
FORDITAS_JELOLES = {'ESV', 'KJV', 'NIV', 'ASV'}
KETIV_QERE_JELOLES = {'LK', 'LQ', 'Mss'}
NINCS_KIADAS_MEZO = 'n/a (a TAHOT-kivonat nem hordoz kiadás-mezőt)'
KQ_RE = re.compile(r'\((?:K|Q)\)|\b(?:ketiv|qere|kethib)\b', re.I)


def kiadasok(nevvaltozat):
    t = set()
    for m in KIADAS_RE.finditer(nevvaltozat or ''):
        t.update(m.group(1).split(','))
    return t


def nev_alakok(nev, nevvaltozat):
    """A névcímke és a Névváltozat nagybetűvel kezdődő névalakjai (a '=' előtti rész)."""
    alakok = [(nev, 'névcímke')]
    for szegmens in (nevvaltozat or '').split(';'):
        resz = szegmens.split('=')[0].strip().rstrip(':').strip()
        if resz and resz[0].isupper() and resz != nev:
            alakok.append((resz, 'a Névváltozat névalakja'))
    return alakok


def norm(szoveg):
    szoveg = (szoveg or '').lower().replace('_', ' ')
    szoveg = re.sub(r'[^\w\s\-]', ' ', szoveg)
    return ' '.join(szoveg.split())


def squash(szoveg):
    return re.sub(r'[\W_]+', '', (szoveg or '').lower())


def tisztit(gloss):
    """A glosszából a szögletes/hegyes zárójeles betoldások kihagyva ([the], <obj.>)."""
    return re.sub(r'\[[^\]]*\]|<[^>]*>', ' ', gloss or '')


def osszes_alak(nev, nevvaltozat):
    """A névcímke és a Névváltozat összes névalakja (a '=' előtti rész), kisbetűs és többszavas is."""
    alakok = [(nev.replace('_', ' '), 'névcímke')]
    for szegmens in (nevvaltozat or '').split(';'):
        resz = szegmens.split('=')[0].strip().rstrip(':').strip()
        if resz and all(resz != a[0] for a in alakok):
            alakok.append((resz, 'a Névváltozat névalakja'))
    return alakok


def nincs_egyezes(nev, nevvaltozat):
    alakok = ' | '.join(a[0] for a in osszes_alak(nev, nevvaltozat))
    return ("a versen egyetlen token, és egymást követő tokenek sora sem adja glosszáival (Rövid jelentés vagy "
            "Angol tükörfordítás) együtt a névcímkét vagy a Névváltozat valamelyik névalakját (%s): szigorú egyenlőség" % alakok)


def egyedi_strongok(em):
    ki = []
    for e in em[:3]:
        for st in e[0].split('+'):
            if st not in ki:
                ki.append(st)
    return '+'.join(ki)


def kiadas_tiszta(kiadas):
    """Igaz, ha a Kritikai kiadás mező minden eleme az alapkiadások közül való (nincs »1-szerű jelölés)."""
    return all(e in TAGNT_KIADASOK for e in kiadas.replace('/', '+').replace(' ', '').split('+') if e)


def vers_parse(ig):
    m = re.match(r'^(.+) (\d+):(\d+)$', ig or '')
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def kiadas_halmaz(szoveg):
    return set(szoveg.replace('/', '+').replace(' ', '').split('+'))


def main(argv):
    db = argv[1] if len(argv) > 1 else os.environ.get('PARDES_DB') or os.path.join(GYOKER, 'pardes.db')
    kim = argv[2] if len(argv) > 2 else KIMENET
    c = sqlite3.connect('file:%s?mode=ro' % db.replace('\\', '/'), uri=True)
    r = c.execute("select ertek from meta where kulcs='epites_ts'").fetchone()
    ts = r[0] if r else 'ismeretlen'
    prov = ('scope=tipnr(utótag nélkül) ∖ token_strong; token_eredeti (TAGNT/TAHOT) | '
            'forras=pardes.db (tipnr, token_strong, token_eredeti, meta; epites_ts=%s), '
            'konkordancia/Karoli_1908.tsv, konkordancia/Karoli_versmegfeleltetes.tsv | ts=%s' % (ts, ts))

    karoli_versek = set()
    with open(os.path.join(GYOKER, 'konkordancia', 'Karoli_1908.tsv'), encoding='utf-8') as f:
        for sor in f:
            karoli_versek.add(sor.split('\t')[0])
    versmegf = {}
    with open(os.path.join(GYOKER, 'konkordancia', 'Karoli_versmegfeleltetes.tsv'), encoding='utf-8') as f:
        for sor in f:
            if sor.startswith('#') or sor.startswith('igehely_karoli'):
                continue
            mezok = sor.rstrip('\n').split('\t')
            versmegf[mezok[0]] = mezok

    rows = c.execute("select nev,nevvaltozat,strong,nyelv,igehely,step_nyers from tipnr "
                     "where utotag='' and strong not in (select strong from token_strong) "
                     "order by strong, igehely, step_nyers, nev, nevvaltozat").fetchall()

    tokenek_cache = {}

    def tokenek(ig, ny):
        kulcs = (ig, ny)
        if kulcs not in tokenek_cache:
            kod = 'G' if ny == 'görög' else 'H'
            tokenek_cache[kulcs] = c.execute(
                "select strong_lanc, rovid_jelentes, angol_tukorford, kritikai_kiadas, alak from token_eredeti "
                "where igehely=? and nyelv=? order by sorszam", (ig, kod)).fetchall()
        return tokenek_cache[kulcs]

    def egyezesek(ig, nev, nv, ny, s):
        """A versen a névhez illő tokenek: (strong, tipus, megjegyzes, kiadas)."""
        tok = tokenek(ig, ny)
        if not tok:
            return []
        van = {t[0] for t in tok}
        kk = {}
        for t in tok:
            kk.setdefault(t[0], t[3])
        ered = []
        # (1) TIPNR-azonosság: azonos névcímkéjű másik TIPNR-sor, amelynek Strong-száma token a versen
        for (st,) in c.execute("select distinct strong from tipnr where igehely=? and nyelv=? and nev=? "
                               "and strong<>? order by strong", (ig, ny, nev, s)).fetchall():
            if st in van:
                gl = [t for t in tok if t[0] == st][0]
                tamogat = any(norm(gl[1]) == norm(a)
                              or re.search(r'(?<![\w\-])%s(?![\w\-])' % re.escape(norm(a)), norm(gl[2]))
                              for (a, _) in nev_alakok(nev, nv) if norm(a))
                megj = 'azonos névcímkéjű (%s) TIPNR-sor Strong-száma a versen token' % nev
                if not tamogat:
                    megj += (" (a token glosszája '%s' / '%s' nem egyezik a névalakkal: az összetartozás csak a TIPNR "
                             "névcímkén alapul, amely összetett nevek részeit is csoportosítja)" % (gl[1], gl[2]))
                ered.append((st, 'tipnr', megj, kk[st]))
        # (2) glossz-egyezés (az (1) mellett is: a társ-tokenek listája egységes)
        for (alak, honnan) in nev_alakok(nev, nv):
            n = norm(alak)
            if not n:
                continue
            for (st, rj, at, kiad, _) in tok:
                if st == s or ',' in st:
                    continue
                if norm(rj) == n or re.search(r'(?<![\w\-])%s(?![\w\-])' % re.escape(n), norm(at)):
                    ered.append((st, 'glossz', "a token glosszája (Rövid jelentés: '%s'; Angol tükörfordítás: '%s') egyezik a(z) '%s' névvel (%s)"
                                 % (rj, at, alak, honnan), kiad))
        # (3) egymást követő tokenek glosszái együtt adják a nevet / a Névváltozat egy névalakját (szigorú egyenlőség)
        for (alak, honnan) in osszes_alak(nev, nv):
            cel = squash(alak)
            if not cel:
                continue
            for i0 in range(len(tok)):
                for hossz in range(1, 6):
                    ablak = tok[i0:i0 + hossz]
                    if len(ablak) < hossz:
                        break
                    if hossz == 1 and not alak[:1].islower():
                        continue          # az egyetlen tokenes, nagybetűs névalakot a (2) kezeli
                    if any(t[0] == s or ',' in t[0] for t in ablak):
                        continue
                    for (mezo, ix) in (('Rövid jelentés', 1), ('Angol tükörfordítás', 2)):
                        if any(not squash(tisztit(t[ix])) for t in ablak):
                            continue      # minden token glosszájának ki kell tennie a névalak egy részét
                        egyben = ''.join(squash(tisztit(t[ix])) for t in ablak)
                        if egyben == cel:
                            ered.append(('+'.join(t[0] for t in ablak), 'ablak',
                                         "%d egymást követő token (%s) %s mezői együtt a(z) '%s' névalakot adják (%s)"
                                         % (hossz, '+'.join(t[0] for t in ablak), mezo, alak, honnan),
                                         ' / '.join(sorted({t[3] for t in ablak}))))
                            break
        seen = set()
        egyedi = []
        for e in ered:
            if e[0] not in seen:
                seen.add(e[0])
                egyedi.append(e)
        return egyedi

    def gyenge(em):
        """Igaz, ha van találat, de mind csak névcímkén alapul (a token glosszája nem egyezik a névalakkal)."""
        return bool(em) and all('nem egyezik a névalakkal' in e[2] for e in em)

    def emtxt(em):
        return '; '.join('%s token: %s' % (e[0], e[2]) for e in em[:3])

    def kq_jeloles(ig, ny):
        for t in tokenek(ig, ny):
            m = KQ_RE.search(t[4] or '')
            if m:
                return "%s (alak: %s)" % (m.group(0), t[4])
        return None

    def szomszedok(ig):
        p = vers_parse(ig)
        if not p:
            return []
        k, f, v = p
        lista = []
        if v > 1:
            lista.append('%s %d:%d' % (k, f, v - 1))
        lista.append('%s %d:%d' % (k, f, v + 1))
        lista.append('%s %d:1' % (k, f + 1))
        return lista

    def elteres_megjegyzes(nev, nv, tag, e):
        """Ha a Névváltozat jelölt névalakja eltér a talált tokentől, de ugyanarra az entitásra mutat."""
        if not tag or 'nem egyezik a névalakkal' in e[2]:
            return ''
        ered = []
        for szegmens in (nv or '').split(';'):
            if '=' in szegmens:
                resz = szegmens.split('=')[0].strip().rstrip(':').strip()
                if resz and resz != nev and resz[0].isupper() and resz not in e[2]:
                    ered.append(resz)
        if not ered:
            return ''
        return ("; a Névváltozat jelölt névalakja (%s) a tokenétől eltér, de ugyanarra az entitásra mutat a TIPNR-sor szerint"
                % ', '.join(ered))

    alap = {}
    for (nev, nv, s, ny, ig, step) in rows:
        alap.setdefault(s, []).append((nev, nv, ny, ig, step))

    kim_sorok = []
    for s in sorted(alap):
        sorok = alap[s]
        osztalyok, strongok, kiadasok_l, indok, igek = [], [], [], [], []
        for (nev, nv, ny, ig, step) in sorok:
            hely = ig if ig else step
            igek.append(hely)
            tag = kiadasok(nv)
            tagszoveg = ','.join(sorted(tag))
            if ig is None:
                osztalyok.append('nincs Károli-vers')
                indok.append('%s: a TIPNR-sor igehelye üres, nincs Károli-vers, tehát TAGNT/TAHOT-vers sem' % hely)
                continue
            tok = tokenek(ig, ny)
            if not tok and ig not in karoli_versek:
                osztalyok.append('nincs Károli-vers')
                indok.append("%s: a TIPNR-sor igehelye nem létező Károli-vers (N-F79b, DT114): a Karoli_1908.tsv-ben nincs ilyen sor; a Karoli_versmegfeleltetes.tsv-ben %s; ezért a vers-átváltás (pl. a név elemeinek más versben álló tokenjei) a repó adatából nem igazolt"
                             % (hely, ('sor: ' + ' | '.join(versmegf[ig])) if ig in versmegf else 'nincs igehely_karoli sor erre a versre'))
                continue
            if not tok:
                megvan = None
                for z in szomszedok(ig):
                    e = egyezesek(z, nev, nv, ny, s)
                    if e:
                        megvan = (z, e[0])
                        break
                if megvan:
                    osztalyok.append('számozási eltérés')
                    strongok.append('%s:%s' % (megvan[0], megvan[1][0]))
                    kiadasok_l.append(megvan[1][3] if ny == 'görög' else NINCS_KIADAS_MEZO)
                    indok.append('%s: a versen nincs token; a szomszédos %s versben %s: %s'
                                 % (hely, megvan[0], megvan[1][0], megvan[1][2]))
                else:
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: a versen nincs token, és a szomszédos versben sincs a névhez (%s) illő token' % (hely, nev))
                continue
            em = egyezesek(ig, nev, nv, ny, s)
            if em:
                strongok.append('%s:%s' % (hely, egyedi_strongok(em)))
                kiadasok_l.append(em[0][3] if ny == 'görög' else NINCS_KIADAS_MEZO)
            elter = elteres_megjegyzes(nev, nv, tag, em[0]) if em else ''
            if ny == 'görög':
                if em and not any(kiadas_tiszta(e[3]) for e in em):
                    osztalyok.append('nem eldönthető')
                    indok.append("%s: a névhez illő token(ek) (%s) Kritikai kiadás mezője nem alapkiadás-jelölés ('%s'): a »N jelölés jelentését a repó nem rögzíti (N-F93c)"
                                 % (hely, '; '.join(e[0] for e in em[:3]), em[0][3]))
                    continue
                if tag and not (tag & {'TR', 'Byz'}):
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: kiadás-jelölés (%s), de nincs köztük a TAGNT Kritikai kiadás mezőjének összevethető kiadása (TR/Byz)'
                                 % (hely, tagszoveg))
                    continue
                if not tag and gyenge(em):
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: nincs jelölés; a versen csak névcímke-alapú társ van, a token glosszája nem egyezik a névalakkal, ezért az azonosság a repó adatából nem dönthető el: %s'
                                 % (hely, emtxt(em)))
                    continue
                keres = (tag & {'TR', 'Byz'}) or {'TR'}
                # DT-F93c: jelölés nélkül csak egyező glosszájú (nem gyenge) token lehet szövegváltozat
                jeloltek = em if tag else [e for e in em if 'nem egyezik a névalakkal' not in e[2]]
                lack = [e for e in jeloltek if not (keres & kiadas_halmaz(e[3]))]
                if lack:
                    e = lack[0]
                    strongok[-1:] = ['%s:%s' % (hely, e[0])]
                    kiadasok_l[-1:] = [e[3]]
                    jelol = ('kiadás-jelölés a Névváltozatban (%s)' % tagszoveg) if tag else \
                        'a Névváltozat nem hordoz kiadás-jelölést'
                    osztalyok.append('szövegváltozat')
                    indok.append('%s: %s; a versen %s; Kritikai kiadás (%s): %s (a %s kiadást nem tartalmazza)%s'
                                 % (hely, jelol, emtxt([e]), e[0], e[3], '+'.join(sorted(keres)), elter))
                elif em:
                    if tag:
                        osztalyok.append('nem eldönthető')
                        indok.append('%s: kiadás-jelölés (%s), de a névhez illő %s token Kritikai kiadás mezője (%s) tartalmazza a jelölt kiadást'
                                     % (hely, tagszoveg, em[0][0], em[0][3]))
                    else:
                        osztalyok.append('alak-/névhasítás')
                        indok.append('%s: nincs kiadás-jelölés; a versen %s (Kritikai kiadás: %s, tartalmazza a TR-t); a TIPNR a névalaknak külön Strong-számot ad'
                                     % (hely, emtxt(em), em[0][3]))
                else:
                    if tag:
                        osztalyok.append('nem eldönthető')
                        indok.append('%s: kiadás-jelölés (%s), de %s' % (hely, tagszoveg, nincs_egyezes(nev, nv)))
                    else:
                        osztalyok.append('adathiány')
                        indok.append('%s: nincs kiadás-jelölés, és %s' % (hely, nincs_egyezes(nev, nv)))
                continue
            # héber
            if tag & KETIV_QERE_JELOLES:
                kq = kq_jeloles(ig, ny)
                if kq:
                    osztalyok.append('ketiv/qere')
                    indok.append('%s: jelölés (%s); a TAHOT a versen ketiv/qere-jelölést hordoz: %s' % (hely, tagszoveg, kq))
                else:
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: jelölés (%s): az LK/LQ jelentését a repó nem rögzíti, és a TAHOT-kivonat a versen nem hordoz ketiv/qere-jelölést%s'
                                 % (hely, tagszoveg, ('; névhez illő: %s' % emtxt(em)) if em else ''))
            elif tag and tag <= FORDITAS_JELOLES:
                if em:
                    osztalyok.append('fordítási névalak')
                    indok.append('%s: csak fordítás-jelölés (%s); a versen %s%s'
                                 % (hely, tagszoveg, emtxt(em), elter))
                else:
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: csak fordítás-jelölés (%s), de %s' % (hely, tagszoveg, nincs_egyezes(nev, nv)))
            elif tag:
                osztalyok.append('nem eldönthető')
                indok.append('%s: ismeretlen jelölés (%s)' % (hely, tagszoveg))
            else:
                if gyenge(em):
                    osztalyok.append('nem eldönthető')
                    indok.append('%s: nincs jelölés (Névváltozat: %s); a versen csak névcímke-alapú társ van, a token glosszája nem egyezik a névalakkal, ezért az azonosság a repó adatából nem dönthető el: %s'
                                 % (hely, nv, emtxt(em)))
                elif em:
                    osztalyok.append('alak-/névhasítás')
                    indok.append('%s: nincs kiadás-/fordítás-jelölés (Névváltozat: %s); a versen %s; a TIPNR a névalaknak külön Strong-számot ad'
                                 % (hely, nv, emtxt(em)))
                else:
                    osztalyok.append('adathiány')
                    indok.append('%s: nincs jelölés, és %s' % (hely, nincs_egyezes(nev, nv)))
        egyedi = sorted(set(osztalyok))
        if len(egyedi) == 1:
            osz = egyedi[0]
        else:
            osz = 'nem eldönthető'
            indok.append('az alapszám sorai több osztályba esnek (%s)' % ', '.join(egyedi))
        kim_sorok.append([s, sorok[0][0], ' || '.join(sorted({x[1] for x in sorok})), ' ; '.join(igek),
                          osz, ' ; '.join(strongok) or '-', ' ; '.join(kiadasok_l) or '-',
                          ' | '.join(indok), prov, sorok[0][2], str(len(sorok))])

    for sor in kim_sorok:
        for m in sor:
            assert '\t' not in m and '\n' not in m
    szoveg = '\t'.join(OSZLOPOK) + '\n' + ''.join('\t'.join(x) + '\n' for x in kim_sorok)
    with open(kim, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    ossz = collections.Counter()
    sor_ossz = collections.Counter()
    for x in kim_sorok:
        ossz[(x[9], x[4])] += 1
        sor_ossz[(x[9], x[4])] += int(x[10])
    print('alapszám: %d, sor: %d' % (len(kim_sorok), sum(int(x[10]) for x in kim_sorok)))
    for k in sorted(ossz):
        print(k, 'alapszám', ossz[k], 'sor', sor_ossz[k])


if __name__ == '__main__':
    main(sys.argv)
