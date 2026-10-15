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
      egyezik a névcímkével vagy a Névváltozat egyik nagybetűvel kezdődő névalakjával.
A két bizonyíték együtt adja a társ-tokenek listáját (nyelvtől függetlenül, egységesen). Egy találat
"gyenge", ha a token glosszája nem egyezik a névalakkal (az összetartozás csak a TIPNR névcímkén
alapul). Szabály, MINDKÉT nyelvre: ha a sorban nincs kiadás-/fordítás-jelölés, és a versen csak gyenge
társ van, az osztály "nem eldönthető" (így jelölés nélküli "szövegváltozat" vagy "alak-/névhasítás"
sem lehet gyenge találatból); jelölés mellett a glossz eltérése maga lehet a jelzés (pl. görög TR-jelölés).
Pusztán az, hogy a versen más nevű
token van, NEM bizonyíték (és az indoklás sem állítja azt): ez az „azonos nevű” hamis állítás hibája volt.

Osztályok:
  szövegváltozat      (CSAK görög) a névhez illő token `Kritikai kiadás` mezője a TR-t nem tartalmazza
                      (kiadás-jelölés a Névváltozatban: TR/Byz; jelölés nélkül is, ha a token TR nélküli)
  fordítási névalak   (CSAK héber, DT-F93b) a Névváltozat csak fordítás-jelölést (ESV/KJV/NIV/ASV)
                      hordoz, és a versen a névhez illő token áll
  ketiv/qere          (CSAK héber, DT-F93b) LK/LQ/Mss jelölés, ÉS a TAHOT az adott versen ketiv/qere-
                      jelölést hordoz (idézve); a kivonat ma nem hordoz, ezért ez az osztály üres, és az
                      LK/LQ/Mss sorok „nem eldönthető”-k: „az LK/LQ jelentését a repó nem rögzíti”
  alak-/névhasítás    nincs kiadás-/fordítás-jelölés, a névhez illő token a versen megvan
  számozási eltérés   a versen nincs token, de a szomszédos versben a névhez illő token megvan
  nincs Károli-vers   a TIPNR-sor igehelye üres (LXX.* hely)
  adathiány           nincs jelölés, és a versen nincs a névhez illő token
  nem eldönthető      minden más; explicit jelölve, nem kitöltve (CLAUDE.md 3. szabály)

Vegyes sorú alapszám (több TIPNR-sor): ha a sorok osztálya versenként eltér, az alapszám
„nem eldönthető” (az indoklás felsorolja a sorok osztályait); csak ha minden sor azonos osztályú,
kapja azt az alapszám. (Pl. H3482, H3159.)

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
            'forras=pardes.db (epites_ts=%s), konkordancia/TIPNR_kivonat.tsv, TAGNT_kivonat.tsv, '
            'TAHOT_kivonat.tsv | ts=%s' % (ts, ts))

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
                strongok.append('%s:%s' % (hely, '+'.join(e[0] for e in em[:3])))
                kiadasok_l.append(em[0][3] if ny == 'görög' else NINCS_KIADAS_MEZO)
            elter = elteres_megjegyzes(nev, nv, tag, em[0]) if em else ''
            if ny == 'görög':
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
                lack = [e for e in em if not (keres & kiadas_halmaz(e[3]))]
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
                        indok.append('%s: kiadás-jelölés (%s), de a versen nincs a névhez (%s) illő token' % (hely, tagszoveg, nev))
                    else:
                        osztalyok.append('adathiány')
                        indok.append('%s: nincs kiadás-jelölés, és a versen nincs a névhez (%s) illő token' % (hely, nev))
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
                    indok.append('%s: csak fordítás-jelölés (%s), de a versen nincs a névhez (%s) illő token' % (hely, tagszoveg, nev))
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
                    indok.append('%s: nincs jelölés, és a versen nincs a névhez (%s) illő token' % (hely, nev))
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
