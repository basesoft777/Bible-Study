"""A blokk-regiszter és a blokkok HTML-je (#76 M2, M0 3.4): a #60 pilot blokk-készlete a `pardes.db`-re átírva.

Minden blokk regiszter-bejegyzés: azonosító, oldal (`vers`, `szo_h`, `szo_g`), cím, **jelleg** (forrásadat / gépi
feldolgozás / modell-kimenet), a táblák (innen jön a licenc- és forrássor, és a kiadási kizárás), az adatlekérő és a
megjelenítő. A jelleg-címke és a forrás+licencsor a regiszterből generálódik (`blokk_html`), így nem maradhat ki;
hiány hibát dob.

Kimenet: a forrásokból jövő szöveg mindenütt escape-elt (`markupsafe`); `Markup` csak a saját, escape-elt elemekből
összeállított töredék. A 9. blokk (angol szavak) két regiszter-bejegyzés (BSB, KJV), mert a KJV-fél GPL miatt
kiadás szerint kimarad; így az M2-ben 40 azonosító állt a pilot 39 mért adatblokkjára. Az M2b a pilot kirajzolt készletéhez hozzáad hatot
(héber és LXX szócsempe, LXX versszintű együttelőfordulás, „Ebben a versben”, az adatréteg-blokk háromra bontása): 46 azonosító.
"""
import importlib.util
import os
import re
import unicodedata
from dataclasses import dataclass
from typing import Callable

from markupsafe import Markup, escape

import adatbazis
import lekerdezesek as q

def _pilot_modul(nev):
    """A #60 pilot meglévő modulja (kódmásolás nélkül, DT-F76g): csak a megadott fájl töltődik be, a pilot könyvtára nem kerül a `sys.path`-ra."""
    ut = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'olvaso_pilot', nev + '.py')
    spec = importlib.util.spec_from_file_location('pilot_' + nev, ut)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


import bdb_szelet  # noqa: E402  (élesben a szerver mellett, DT-F99c (a); a pilot ugyanezt tölti be)


def _eszkoz_modul(nev):
    """Az `eszkozok/` közös modulja (a lexikon-generátorral közös kód, N-F131x), fájlútvonalról, a `sys.path` változtatása nélkül."""
    ut = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), nev + '.py')
    spec = importlib.util.spec_from_file_location('eszkoz_' + nev, ut)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


bdb_rovidites = _eszkoz_modul('bdb_rovidites')

JELLEG = {
    'forras': ('forrásadat', 'jelleg-forras', 'változtatás nélkül egy adatkészletből'),
    'gepi': ('gépi feldolgozás', 'jelleg-gepi', 'determinisztikus szabály rendezi vagy párosítja a forrásadatot'),
    'modell': ('modell-kimenet', 'jelleg-modell', 'nyelvi modell állította elő; javaslat-értékű'),
}


class BlokkHiba(Exception):
    pass


@dataclass(frozen=True)
class Blokk:
    id: str
    oldal: str
    cim: str
    jelleg: object          # str vagy tuple: a pilot SUGO-listája szerinti jellegek (egy blokk több jellegű is lehet)
    tablak: tuple
    fetch: Callable
    render: Callable
    jelleg_megj: str = ''
    forras_szoveg: str = ''      # ha a blokk adata nincs a pardes.db-ben: a forrás- és licencsor szövege (tábla híján)
    kovet: tuple = ()            # azok a blokkok, amelyek láthatóságát követi (a bontott BDB ugyanazt a magyar szócikket mutatja, mint a szo.bdb_magyar)
    jelleg_fn: Callable = None   # az adatból függő jelleg (pl. a bontott BDB: modell-kimenet csak magyar bontásnál)
    vers_kell: bool = False      # csak vers-kontextussal jelenik meg (a szó-lap „Ebben a versben” blokkja)

    def __post_init__(self):
        j = (self.jelleg,) if isinstance(self.jelleg, str) else tuple(self.jelleg)
        object.__setattr__(self, 'jelleg', j)

    def kiadas_kizart(self, kiadas):
        ki = adatbazis.kizart_tablak(kiadas)
        return any(t in ki for t in self.tablak)


# ---------------------------------------------------------------------------------------------------------------------
# a megjelenítés segédei
# ---------------------------------------------------------------------------------------------------------------------
e = escape


def _szoveg(s):
    return Markup('<div class="szoveg gordul">%s</div>') % e(s or '')


def _tabla(fejlec, sorok, osztaly=''):
    """fejlec: [str]; sorok: [[cella]]; a cella str (escape-elve) vagy Markup (változatlanul)."""
    fh = Markup('').join(Markup('<th>%s</th>') % c for c in fejlec)
    sh = Markup('').join(
        Markup('<tr>%s</tr>') % Markup('').join(Markup('<td>%s</td>') % c for c in sor) for sor in sorok)
    return Markup('<table class="adat %s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>') % (osztaly, fh, sh)


def _lista(elemek):
    return Markup('<ul class="lista">%s</ul>') % Markup('').join(Markup('<li>%s</li>') % x for x in elemek)


def _ures():
    return Markup('<p class="ures">Nincs adat (üres eredmény, nem negatív lelet).</p>')


def _heb(s):
    return Markup('<span class="heb" lang="he" dir="rtl">%s</span>') % e(s or '')


def _gor(s):
    return Markup('<span class="gor" lang="grc">%s</span>') % e(s or '')


def strong_link(K, s):
    n = q.hnorm(s) if s else None
    if not n:
        return e(s or '')
    return Markup('<a class="strong" href="/szo/%s">%s</a>') % (n, n)


def _ctx_href(K, strong):
    """A Strong-szám hivatkozásának címe a vers-kontextusban: `/<könyv>/<fejezet>/<vers>?szo=H0430&ful=szo#v<vers>` (a szó-lap a vers mellett
    nyílik meg, így az „Ebben a versben” blokk is megjelenik); vers nélkül az önálló szó-lap."""
    n = q.hnorm(strong) if strong else None
    m = re.match(r'^(.+?) (\d+):(\d+)$', K.ig or '')
    slug = K.kozos.slug.get(m.group(1)) if m else None
    if slug and n:
        return '/%s/%s/%s?szo=%s&ful=szo#v%s' % (slug, m.group(2), m.group(3), n, m.group(3))
    return '/szo/%s' % n if n else '#'


def ctx_strong_link(K, strong, szoveg=None, osztaly='strong'):
    n = q.hnorm(strong) if strong else None
    if not n:
        return e(szoveg or strong or '')
    return Markup('<a class="%s" href="%s">%s</a>') % (osztaly, _ctx_href(K, n), szoveg or n)


def ig_link(K, szoveg):
    """`1Móz 1:4` (vagy `1Móz 1:4-6`, `Zsolt 22:1`) -> a versoldal hivatkozása, ha a könyv ismert; különben sima szöveg."""
    m = re.match(r'^(.+?) (\d+):(\d+)', szoveg or '')
    if m and m.group(1) in K.kozos.slug:
        return Markup('<a class="igehely" href="/%s/%s/%s">%s</a>') % (K.kozos.slug[m.group(1)], m.group(2), m.group(3), szoveg)
    return e(szoveg or '')


# ---------------------------------------------------------------------------------------------------------------------
# az igealak magyar feloldása (a pilot `MorfKulcs`-ának átirata a pardes.db táblájára)
# ---------------------------------------------------------------------------------------------------------------------
def morf_dekodol(kulcs, kod, nyelv='H'):
    """A Macula morfológiai kódjának magyar feloldása (`morf_kulcs_heber`); (szöveg, ismeretlen-e)."""
    if not kod:
        return '', False

    def k(poz, c):
        d = kulcs.get(poz, {})
        return d.get((nyelv, c)) or d.get(('*', c))

    sz, rest = kod[0], kod[1:]
    elso = k('szofaj', sz)
    if elso is None:
        return '', True
    ki, ism = [elso], False
    if sz == 'V':
        mezok = ['igetorzs', 'igetipus']
        tip = rest[1:2]
        if tip in ('r', 's'):
            mezok += ['nem', 'szam', 'allapot']
        elif tip in ('a', 'c'):
            mezok += ['allapot']
        else:
            mezok += ['szemely', 'nem', 'szam', 'allapot']
    elif sz in ('N', 'A'):
        mezok = ['tipus_' + sz, 'nem', 'szam', 'allapot']
    elif sz in ('P', 'S'):
        mezok = ['tipus_' + sz, 'szemely', 'nem', 'szam']
    elif sz in ('R', 'T'):
        mezok = ['tipus_' + sz]
    else:
        mezok = []
    for poz, c in zip(mezok, rest):
        if c == 'x':
            continue
        hu = k(poz, c)
        if hu is None:
            ism = True
            ki.append('[%s?]' % c)
            continue
        ki.append(hu + ' személy' if poz == 'szemely' else hu)
    if len(rest) > len(mezok):
        ism = True
    return ', '.join(ki), ism


# ---------------------------------------------------------------------------------------------------------------------
# vers-lap blokkok: fetch(K) és render(adat, K); K.ig = igehely, K.con = kapcsolat
# ---------------------------------------------------------------------------------------------------------------------
def _f_karoli(K):
    t = q.karoli_szoveg(K.con, K.ig)
    return t


def _r_karoli(d, K):
    return Markup('<p class="karoli-szoveg">%s</p>') % e(d)


def _f_par(K):
    return q.par_szavak(K.con, K.ig)


def _r_par(d, K):
    sorok = [[str(hs), hu, _heb(erszo), strong_link(K, st), bz or ''] for hs, hu, ers, erszo, st, bz in d]
    return _tabla(['Károli-szó (sorszám)', 'Szó', 'Eredeti', 'Strong', 'Bizonyosság'], sorok)


def _f_eredeti(K):
    return K.memo('eredeti', lambda: q.eredeti_szavak(K.con, K.ig))


def _r_eredeti(d, K):
    sorok = []
    for sz, ny, sn, alak, kiej, szoto, rovid, tukor in d:
        sorok.append([str(sz), _heb(alak) if ny == 'H' else _gor(alak), kiej or '', strong_link(K, sn), _heb(szoto) if ny == 'H' else _gor(szoto), rovid or '', tukor or ''])
    return _tabla(['#', 'Szó', 'Kiejtés', 'Strong', 'Szótő', 'Rövid jelentés', 'Angol tükörfordítás'], sorok)


def _f_macula(K):
    return K.memo('macula', lambda: q.macula(K.con, K.ig))


def _r_macula_morf(d, K):
    sorok = [[_heb(m['szo']), _heb(m['lemma']), strong_link(K, m['strong']) if m['strong'] else '', m['morf'] or '', m['szofaj'] or '', m['gloss'] or ''] for m in d]
    return _tabla(['Szó', 'Lemma', 'Strong', 'Morfológiai kód', 'Szófaj', 'Gloss'], sorok)


def _macula_gor_cella(m):
    """A javított görög alak (F115, DT-F115a); ahol a Rahlfs-minősítés nem `rahlfs_igazolt` (és nem üres), jelölő áll mellette
    (`title`: az osztály és a forrásalak)."""
    cella = _gor(m['lxx'])
    r = m.get('lxx_rahlfs') or ''
    if r and r != 'rahlfs_igazolt':
        cim = '%s; forrásalak (upstream): %s' % (r, m.get('lxx_forras') or '')
        cella += Markup(' <sup title="%s">nem igazolt</sup>') % cim
    return cella


def _r_macula_gorog(d, K):
    sorok = [[_heb(m['szo']), m['gloss'] or '', _macula_gor_cella(m), strong_link(K, m['lxx_strong']) if m['lxx_strong'] else ''] for m in d if m['lxx'] or m['lxx_strong']]
    return _tabla(['Héber szó', 'Gloss', 'Görög (Macula)', 'Görög Strong'], sorok) if sorok else None


def _f_morf_hu(K):
    return K.memo('macula', lambda: q.macula(K.con, K.ig))


def _r_morf_hu(d, K):
    kulcs = K.kozos.morf_kulcs
    aramai = K.kozos.aramai_lekerdez(K.con, [m['xml_id'] for m in d])
    sorok = []
    for m in d:
        if not m['morf']:
            continue
        hu, ism = morf_dekodol(kulcs, m['morf'], aramai.get(m['xml_id'], 'H'))
        sorok.append([_heb(m['szo']), m['morf'], hu or '[ismeretlen kód]', aramai.get(m['xml_id'], 'H')])
    return _tabla(['Szó', 'Kód', 'Magyar feloldás', 'Nyelv'], sorok) if sorok else None


def _f_lxx_szavak(K):
    return q.lxx_szavak(K.con, K.ig)


def _r_lxx_szavak(d, K):
    csop = {}
    for x in d:
        csop.setdefault(x['szovegforma'] or '', []).append(x)
    ki = Markup('')
    for forma, lista in csop.items():
        if forma and len(csop) > 1:
            ki += Markup('<h4>%s</h4>') % forma
        ki += _tabla(['Szóalak', 'Lemma', 'Strong', 'Morf'], [[_gor(x['szoalak']), _gor(x['lemma']), strong_link(K, x['strong']) if x['strong'] else '', x['morf'] or ''] for x in lista])
    return ki


def _f_lxx_versszam(K):
    lxx, extra, terkep = q.lxx_versszam(K.con, K.ig)
    return (lxx, extra, terkep) if (lxx or extra or terkep) else None


def _r_lxx_versszam(d, K):
    lxx, extra, terkep = d
    sorok = [['LXX_OS', x] for x in lxx] + [[f, x] for f, x in extra] + [['térkép (KJV-kulcs)', x] for x in terkep]
    return _tabla(['Forrás', 'LXX-versszám'], sorok)


def _f_versszamozas(K):
    return q.versszamozas(K.con, K.ig)


def _r_versszamozas(d, K):
    osz, kjvi, mti, mf = d
    return _tabla(['Osztály', 'KJV-versszám', 'MT-versszám', 'A megfeleltetés forrása'], [[osz or '', kjvi or '', mti or kjvi or '', mf or '']])


def _f_bsb(K):
    return q.bsb(K.con, K.ig)


def _r_angol(d, K):
    """Szavankénti csempék (a pilot angol blokkjai): az angol szó és alatta a Strong-szám (kattintható); üres szó: —."""
    cs = Markup('').join(
        Markup('<span class="ang-csempe" title="%s"><span class="ang">%s</span><span class="st">%s</span></span>') % (
            x[3] or '', x[1] or '—', ctx_strong_link(K, x[2], x[2], 'st-link') if x[2] else '') for x in d)
    return Markup('<div class="angol-sor" lang="en">%s</div>') % cs


def _f_kjv(K):
    return q.kjv(K.con, K.ig)


def _f_nave(K):
    vers, fej = q.nave(K.con, K.ig), q.nave_fejezet(K.con, K.ig)
    return (vers, fej) if (vers or fej) else None


def _r_nave(d, K):
    d, fej = d
    ki = Markup('')
    if d:
        sorok = [[tema, cimke or '', ig_link(K, hely) if hely else '', 'tartomány (versekre bontva)' if t else 'vers'] for tema, cimke, hely, t, tid in d[:80]]
        ki += _tabla(['Téma', 'Cím', 'Nave-hely', 'Jelleg'], sorok)
        if len(d) > 80:
            ki += Markup('<p class="megj">Összesen %d sor; az első 80 látszik.</p>') % len(d)
    else:
        ki += Markup('<p class="ures">Nincs Nave-sor erre a vershez.</p>')
    if fej:
        ki += Markup('<details class="fejezet-nave" open><summary>Fejezet-szintű hivatkozások (%d)</summary>%s</details>') % (
            len(fej), _tabla(['Téma', 'Cím', 'Nave-hely'], [[tema, cimke or '', ig_link(K, hely)] for tema, cimke, hely, tid in fej]))
    return ki


def _f_tipnr(K):
    return q.tipnr(K.con, K.ig)


def _r_tipnr(d, K):
    return _tabla(['Név', 'Névváltozat', 'Strong', 'Nyelv'], [[n, v or '', strong_link(K, s) if s else '', ny or ''] for n, v, s, ny in d])


def _f_motivum(K):
    return q.motivum_elofordulasok(K.con, K.ig)


def _r_motivum(mot, K):
    return _tabla(['Azonosító', 'Motívum', 'Funkció', 'Strong', 'Károli-szó', 'Megbízhatóság', 'Proveniencia'],
                  [[a, cim or '', fk or '', strong_link(K, st) if st else '', kszo or '', mb or '', pr or ''] for a, ig, fk, st, kszo, mb, pr, cim in mot])


def _f_kapcsolat(K):
    return q.kapcsolatok(K.con, K.ig)


def _r_kapcsolat(kap, K):
    return _tabla(['Forrás', 'Cél', 'Azonosító', 'Típus', 'Funkció', 'Bizonyosság'],
                  [[ig_link(K, a), ig_link(K, b), c, t or '', f or '', bz or ''] for a, b, c, t, f, bz in kap])


def _f_lxx_dontes(K):
    return q.lxx_dontesek(K.con, K.ig)


def _r_lxx_dontes(lx, K):
    return _tabla(['Azonosító', 'LXX-hely', 'Héber', 'Görög', 'Típus', 'Megjegyzés', 'Bizonyosság', 'Proveniencia'],
                  [[a, c or '', strong_link(K, hs) if hs else '', Markup('%s %s') % (_gor(gl), strong_link(K, gs) if gs else ''), t or '', mj or '', bz or '', pv or ''] for a, ig, c, hs, gl, gs, t, mj, bz, pv in lx])


def _f_tsk(K):
    return q.tsk(K.con, K.ig)


def _r_tsk(d, K):
    sorok = [[ig_link(K, c), str(v)] for c, v in d[:15]]
    ki = _tabla(['Hivatkozás', 'Szavazat'], sorok)
    ki += Markup('<p class="megj">Összesen %d hivatkozás; az első %d látszik (szavazatszám szerint).</p>') % (len(d), min(len(d), 15))
    return ki


def _f_kh(K):
    return q.kh(K.con, K.ig)


def _r_kh(d, K):
    return _lista([ig_link(K, a) for a, b in d])


def _f_lxx_par(K):
    return q.lxx_versszintu(K.con, K.ig) or None


def _r_lxx_par(d, K):
    lem = K.kozos_szotar(list(d))
    sorok = Markup('').join(
        Markup('<div class="sor"><span class="fo">%s%s</span><span class="al">%s</span></div>') % (
            strong_link(K, h), Markup(' · %s') % _heb(lem[h][0]) if lem.get(h) and lem[h][0] else '',
            Markup(', ').join(strong_link(K, g) for g in gs)) for h, gs in d.items())
    return Markup('<details open><summary class="megj">%d héber szó, %d pár</summary><div class="sorok">%s</div></details>') % (
        len(d), sum(len(g) for g in d.values()), sorok)


# --- szócsempék: a héber szöveg és az LXX szavanként (a pilot `heber-sor` és `lxx-sor`)
def _csupasz(szo):
    """Görög szóalak ékezet és hehezet nélkül, kisbetűvel, végső szigma egységesítve (a pilot `csupasz`-a)."""
    t = unicodedata.normalize('NFD', szo or '')
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return t.lower().replace('ς', 'σ').strip('.,;·')


def _tavolsag(a, b):
    if a == b:
        return 0
    elozo = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        akt = [i]
        for j, cb in enumerate(b, 1):
            akt.append(min(elozo[j] + 1, akt[j - 1] + 1, elozo[j - 1] + (ca != cb)))
        elozo = akt
    return elozo[-1]


def _heber_csempek(K):
    """A vers héber szavai (TAHOT) a Macula-sorral párosítva (pozíció szerint, eltérő szegmentálásnál Strong szerint), a görög
    LXX-megfelelővel, a magyar alaktannal: a pilot `adat.py` párosítása. A memo-ban lévő Macula-sorokat nem módosítja."""
    def f():
        con, ig = K.con, K.ig
        th = [{'strong': q.hnorm(sn) or sn, 'heber': alak, 'atiras': kiej, 'tukor': tukor}
              for sz, ny, sn, alak, kiej, szoto, rovid, tukor in q.eredeti_szavak(con, ig) if ny == 'H']
        mac = [dict(m) for m in K.memo('macula', lambda: q.macula(con, ig))]
        if len(mac) == len(th):
            for w, m in zip(th, mac):
                w['macula'] = m
        else:
            hasznalt = set()
            for w in th:
                if w['strong'] and w['strong'].startswith('H9'):
                    jel = [i for i, m in enumerate(mac) if m['strong'] is None and i not in hasznalt]
                else:
                    jel = [i for i, m in enumerate(mac) if m['strong'] == w['strong'] and i not in hasznalt]
                w['macula'] = mac[jel[0]] if jel else None
                if jel:
                    hasznalt.add(jel[0])
        # a görög szóalak az LXX_OS-ből (Rahlfs) jön; a Macula csak a párosítást adja (szóalakja helyenként hibás)
        szabad = [dict(x) for x in q.lxx_szavak_sorrendben(con, ig)]
        for w in th:
            m = w['macula']
            if m and m.get('lxx_strong'):
                jelolt = [x for x in szabad if x['strong'] == m['lxx_strong'] and not x.get('_hasznalt')]
                mc = _csupasz(m['lxx'])
                cel = next((x for x in jelolt if _csupasz(x['szoalak']) == mc), None)
                if cel is None:
                    cel = next((x for x in jelolt if _tavolsag(_csupasz(x['szoalak']), mc) <= 1), None)
                if cel:
                    cel['_hasznalt'] = True
                    m['lxx'] = cel['szoalak']
        aramai = K.kozos.aramai_lekerdez(con, [m['xml_id'] for m in mac if m.get('xml_id')])
        for w in th:
            m = w['macula']
            w['nyelvtani'] = (not w['strong']) or w['strong'] in K.kozos.nyelvtani
            if m:
                m['nyelv'] = aramai.get(m['xml_id'], 'H')
                m['morf_hu'] = morf_dekodol(K.kozos.morf_kulcs, m['morf'], m['nyelv'])[0] if m['morf'] else ''
        return th
    return K.memo('heber_csempek', f)


def _f_heber_csempe(K):
    return _heber_csempek(K) or None


def _r_heber_csempe(th, K):
    ki = Markup('')
    for w in th:
        m = w.get('macula') or {}
        mf = m.get('morf_hu') or m.get('szofaj') or ''
        cim = ('Nyelvtani elem (prefixum, névelő, tárgyjelölő): nincs szó-lapja' if w['nyelvtani'] else '%s szó-lapja' % w['strong']) + (' · morfológia: %s' % m['morf'] if m.get('morf') else '')
        fo = Markup('<span class="he" lang="he">%s</span><span class="at">%s</span><span class="gl">%s</span><span class="st">%s</span>%s') % (
            w['heber'], w['atiras'] or '', w['tukor'] or '', w['strong'] or '', Markup('<span class="mf">%s</span>') % mf if mf else '')
        if not w['nyelvtani']:
            fo = Markup('<a class="he-fo" href="%s" title="%s">%s</a>') % (_ctx_href(K, w['strong']), cim, fo)
        else:
            fo = Markup('<span class="he-fo" title="%s">%s</span>') % (cim, fo)
        if m.get('lxx'):
            if m.get('lxx_strong'):
                lx = Markup('<a class="lx kat" lang="grc" href="%s" title="%s görög szó-lapja">%s</a>') % (_ctx_href(K, m['lxx_strong']), m['lxx_strong'], m['lxx'])
            else:
                lx = Markup('<span class="lx" lang="grc" title="nincs Strong-szám">%s</span>') % m['lxx']
        else:
            lx = Markup('<span class="lx ures">LXX: —</span>')
        ki += Markup('<div class="he-szo%s" data-strong="%s">%s%s</div>') % (' nyelvtani' if w['nyelvtani'] else '', w['strong'] or '', fo, lx)
    return Markup('<p class="megj">Jobbról balra. Szavanként: átírás, angol tükörfordítás, Strong-szám, igealak (magyarul), alul a görög LXX-megfelelő (kattintható). '
                  'Szaggatott keret: nyelvtani elem, nincs szó-lapja.</p><div class="heber-sor" lang="he" dir="rtl">%s</div>') % ki


def _f_lxx_csempe(K):
    return q.lxx_szavak_sorrendben(K.con, K.ig) or None


def _r_lxx_csempe(d, K):
    cs = Markup('').join(
        (Markup('<a class="gk" href="%s" data-strong="%s" title="%s · %s · kattintásra görög szó-lap"><span class="gr" lang="grc">%s</span><small>%s</small></a>') % (
            _ctx_href(K, x['strong']), x['strong'], x['lemma'] or '', x['morf'] or '', x['szoalak'], x['strong'])
         if x['strong'] else
         Markup('<span class="nincs-st" title="%s · %s"><span class="gr" lang="grc">%s</span><small>nincs Strong</small></span>') % (x['lemma'] or '', x['morf'] or '', x['szoalak']))
        for x in d)
    return Markup('<p class="megj">A keretes, aláhúzott görög szavakra kattintva megnyílik a görög szó-lap (jelentés, újszövetségi előfordulások, héber háttér). '
                  'A szó alatt a Strong-szám; „nincs Strong”: a szónak nincs újszövetségi Strong-száma.</p><div class="lxx-sor" lang="grc">%s</div>') % cs


# --- „Ebben a versben”: a szó-lap vers-kontextusos blokkja (a pilot `ebbenAVersben`)
def _f_ebben(K):
    if not K.ig or not K.strong or K.strong[0] != 'H':
        return None
    talalat = [w for w in _heber_csempek(K) if w['strong'] == K.strong]
    ubs, lat = [], set()
    for st, lex, dom, df, gl in q.ubs_dbh(K.con, K.ig):
        if st == K.strong and lex not in lat:
            lat.add(lex)
            ubs.append((dom, df, gl))
    par = q.hu_par_szavak(K.con, K.ig)
    szofaj = q.szofajok(K.con, {p[2] for _, (hu, ps) in par.items() for p in ps})
    karoli = None
    for hs, (hu, ps) in sorted(par.items()):
        fo = q.fo_lista(ps, K.kozos.nyelvtani, szofaj)
        if fo and (fo[0][0] == K.strong or any(x[0] == K.strong for x in fo[1:])):
            karoli = (hu, fo)
            break
    return {'talalat': talalat, 'ubs': ubs, 'karoli': karoli}


def _r_ebben(d, K):
    if not d['talalat']:
        return Markup('<p class="megj">A szó nem fordul elő a %s versben.</p>') % K.ig
    w = d['talalat'][0]
    m = w.get('macula') or {}
    ki = Markup('<p class="megj">Vers: %s</p>') % K.ig
    if d['karoli']:
        hu, fo = d['karoli']
        sor = Markup('Károli itt: „%s”') % hu
        if len(fo) > 1:
            lem = K.kozos_szotar([x[0] for x in fo])
            reszek = []
            for st, bz in fo:
                lemma = _heb((lem.get(st) or (st,))[0] or st)
                cim = Markup('<b>%s</b>') % lemma if st == K.strong else Markup('<a href="%s">%s</a>') % (_ctx_href(K, st), lemma)
                reszek.append(Markup('%s (%s%s)') % (cim, st, ', %s bizonyosság' % bz if bz and bz != 'magas' else ''))
            sor += Markup(' — ez a magyar szó több héber szót ad vissza együtt: ') + Markup(' + ').join(reszek)
        ki += Markup('<p class="megj karoli-itt">%s</p>') % sor
    if m.get('morf'):
        ki += Markup('<p class="megj alak">Alak: %s (%s) · %s (%s)</p>') % (_heb(w['heber']), w['atiras'] or '', m.get('morf_hu') or m.get('szofaj') or '', m['morf'])
    if m.get('lxx'):
        if m.get('lxx_strong'):
            lx = Markup('<a class="gk" lang="grc" href="%s">%s</a>') % (_ctx_href(K, m['lxx_strong']), m['lxx'])
        else:
            lx = _gor(m['lxx'])
        ki += Markup('<p class="megj">Görögül ebben a versben (LXX): %s%s</p>') % (lx, Markup(' · %s') % m['lxx_strong'] if m.get('lxx_strong') else '')
    if d['ubs']:
        for dom, df, gl in d['ubs']:
            ki += Markup('<div class="ubs"><span class="dom">%s</span> <span class="def" lang="en">%s</span> <span class="gl" lang="en">Glosszák: %s</span></div>') % (dom or '', df or '', gl or '')
    else:
        ki += Markup('<p class="megj">A UBS-szótár ehhez az előforduláshoz nem ad jelentés-besorolást.</p>')
    return ki


def _f_ubs(K):
    return q.ubs_dbh(K.con, K.ig)


def _r_ubs(d, K):
    return _tabla(['Strong', 'Azonosító', 'Domén', 'Rövid definíció', 'Glosszák'], [[strong_link(K, st), lex, dom or '', df or '', gl or ''] for st, lex, dom, df, gl in d])


# ---------------------------------------------------------------------------------------------------------------------
# héber szó-lap blokkok: K.strong
# ---------------------------------------------------------------------------------------------------------------------
def _f_szotar(K):
    return q.strong_szotar(K.con, K.strong)


def _r_szotar(d, K):
    szoto, kiej, szofaj, jel, gyok = d
    return _tabla(['Szótő', 'Kiejtés', 'Szófaj', 'Rövid jelentés', 'Gyök / származtatás'], [[_heb(szoto) if K.strong[0] == 'H' else _gor(szoto), kiej or '', szofaj or '', jel or '', gyok or '']])


def _f_elofordulas(K):
    db, kony = q.elofordulas(K.con, K.strong)
    return (db, kony) if db else None


def _r_elofordulas(d, K):
    return Markup('<p><b>%d</b> előfordulás, <b>%d</b> könyvben.</p>') % d


def _f_karoli_alakok(K):
    ossz, magas, top = q.karoli_alakok(K.con, K.strong)
    return (ossz, magas, top) if ossz else None


def _r_karoli_alakok(d, K):
    ossz, magas, top = d
    ki = Markup('<p>%d Károli-előfordulás, ebből %d magas bizonyosságú.</p>') % (ossz, magas)
    ki += _tabla(['Károli-alak', 'Darab'], [[a, str(n)] for a, n in top])
    kv = K.kozos.karoli_strong_konyvek
    return ki + Markup('<p class="megj">A %d feldolgozott könyv (%s) szó szintű párjai alapján; a többi könyv még hiányzik.</p>') % (len(kv), ', '.join(kv))


def _bdb_adat(K):
    """A BDB-szócikk angol és magyar szövege (és az alias). A magyar fordítást (`forditasok`) csak akkor olvassa, ha a lap `magyar_ok`
    (a `szo.bdb_magyar` és `szo.bdb_apparatus` blokk szint és kiadás szerint látható): tiltott magyar BDB-t sem a szó-lap, sem a számláló nem olvas."""
    def f():
        mo = getattr(K, 'magyar_ok', True)
        en, hu = q.bdb_angol(K.con, K.strong), (q.bdb_magyar(K.con, K.strong) if mo else None)
        alias = None
        if not hu and not en:
            a = q.bdb_alias(K.con, K.strong)
            if a:
                en2, hu2 = q.bdb_angol(K.con, a[0]), (q.bdb_magyar(K.con, a[0]) if mo else None)
                if hu2 or en2:
                    alias, en, hu = {'tabla_strong': a[0], 'bdb_id': a[1], 'hasonlosag': a[2]}, en2, hu2
        return {'en': en, 'hu': hu, 'alias': alias}
    return K.memo('bdb', f)


def _bdb_cimszo(K):
    """(„lemma (kiejtés)”, a lemma alapbetűje) a BDB-rövidítések feloldásához: a szócikk Strongjának (alias esetén a tábla-Strongnak)
    TBESH-lemmája, a jóváhagyott héber kiejtéssel (kiejtés-szabály: ha nincs, csak a lemma); ('', ''), ha nincs TBESH-sor."""
    def f():
        d = _bdb_adat(K)
        r = q.tbesh_lemma(K.con, d['alias']['tabla_strong'] if d['alias'] else K.strong)
        if not r:
            return '', ''
        return bdb_rovidites.cimszo_alak(r[0], bdb_rovidites.heber_kiejtes(*r)), bdb_rovidites.alapbetu(r[0])
    return K.memo('bdb_cimszo', f)


_CIMKE_RE = re.compile(r'(<[^>]*>)')


def _rovidites(K, html):
    """A BDB egybetűs rövidítései (׳י → י׳) <abbr class="rovidites">-ként a kész, escape-elt blokk-HTML szövegrészeiben (N-F131x; a jelölő
    közös a lexikon-generátorral: `eszkozok/bdb_rovidites.py`). A címkék (és attribútumaik) érintetlenek; a jelölő csak héber betűt és
    geres jelet fog meg, a cím escape-elve kerül be, így injekció nem lehet. `tabindex`: érintésre, fókuszra is megjelenik a feloldás;
    hivatkozáson (a vázlat <a>-ján) belül nincs, ott a koppintás a hivatkozásé, a feloldás a `title`."""
    cimszo, kezdo = _bdb_cimszo(K)
    ki, linkben = [], False
    for i, r in enumerate(_CIMKE_RE.split(str(html))):
        if i % 2:
            linkben = (r.startswith('<a ') or r == '<a>') or (linkben and r != '</a>')
            ki.append(r)
        else:
            ki.append(bdb_rovidites.jelol(r, cimszo, kezdo, cim_esc=lambda s: str(escape(s)), attr='' if linkben else ' tabindex="0"'))
    return Markup(''.join(ki))


def _alias_megj(a):
    return Markup('<p class="megj">A szócikk másik Strong-szám alatt áll (alias, gépi): %s, BDB-azonosító %s, szöveghasonlóság %s.</p>') % (a['tabla_strong'], a['bdb_id'], a['hasonlosag'])


def _bdb_bontas(K):
    """A BDB-szócikk gépi szeletelése a pilot `bdb_szelet.szeletel`-ével (DT-F76g): a magyar fordítás, ennek híján az angol eredeti szövegére;
    a lemma a Strong-szótár szótője. None, ha nincs szócikk."""
    def f():
        d = _bdb_adat(K)
        szoveg = d['hu'] or d['en']
        if not szoveg:
            return None
        sz = q.strong_szotar(K.con, K.strong)
        appar = bdb_szelet.szeletel(szoveg, sz[0] if sz else '')
        if not appar:
            return None
        hu = bool(d['hu'])
        forras_strong = d['alias']['tabla_strong'] if d['alias'] else K.strong
        return {'appar': appar, 'hu': hu, 'meta': q.bdb_magyar_meta(K.con, forras_strong) if hu else None, 'alias': d['alias'],
                'alap': bdb_szelet.alap_jelentes(appar['alap']) if hu else None}
    return K.memo('bdb_bontas', f)


def alapjelentes(K, magyar_ok=True, angol_ok=True):
    """A szó-lap fejlécének alapjelentése (DT-F76f): a magyar BDB-sor gépi tisztítása (`bdb_szelet.alap_jelentes`), ennek híján az angol
    Strong-glossza. {'szoveg', 'nyelv', 'tisztitott'} vagy None. `magyar_ok`/`angol_ok`: a hívó (OldalGyar) a blokk-szintű kiadási és
    hozzáférési szűrésen átengedte-e a magyar BDB-t, illetve a Strong-szótárat; ezek tiltása esetén a megfelelő forrást nem olvassa
    (a magyar BDB-hez a `K.magyar_ok` is kell: `_bdb_adat`)."""
    b = _bdb_bontas(K) if magyar_ok else None
    if b and b['hu'] and b['alap'] and b['alap'].get('szoveg'):
        return {'szoveg': b['alap']['szoveg'], 'nyelv': 'hu', 'tisztitott': b['alap']['tisztitott']}
    if not angol_ok:
        return None
    sz = q.strong_szotar(K.con, K.strong)
    return {'szoveg': sz[3], 'nyelv': 'en', 'tisztitott': False} if sz and sz[3] else None


_HIVATKOZAS_SUGO = ('a BDB ennél a jelentésnél kiírt igehely-hivatkozásainak gépi száma (minden „fejezet:vers” alak), '
                    'nem a szó előfordulásainak száma: a „vö.” helyek beleszámítanak, az „és máshol” nem')


def _helyek(n):
    return Markup('<span class="helyek" title="%s">%s hivatkozás</span>') % (_HIVATKOZAS_SUGO, n) if n else Markup('')


def _rovid(s, n):
    s = s or ''
    return s if len(s) <= n else re.sub(r'\s+\S*$', '', s[:n]) + ' …'


# A jelentés címe (gépi, a szócikk saját szavaiból, értelmezés nélkül): a szöveg eleje a zárójeles részek nélkül, az első
# igehely-hivatkozásig, pontosvesszőig, kettőspontig, egyenlőségjelig, gondolatjelig, vagy a magyar szöveg utáni első héber szóig
# (a vezető héber kifejezés marad). A vessző nem határ („rossz, kellemetlen, ártalmas”), csak ha a főjelentésnek nincs saját szövege
# (a BDB „1. a. …” szerkezete): ekkor a cím az első alpontéból képződik, annak első vesszőjéig (H0776: „föld”).
_CIM_REF = re.compile(r'(?:\b\d?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,5}\s+)?\d+:\d+')
_CIM_BETUK = re.compile(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2}')


def _zarojel_nelkul(s):
    """A felső szintű (…) és […] csoportok nélkül; a szó belsejében álló zárójel (héber `מַחֲשֶׁבֶת(ה)רָעָה`) marad."""
    ki, mely, i = [], 0, 0
    while i < len(s):
        c = s[i]
        if not mely and c in '([' and i and not s[i - 1].isspace():
            j = s.find(')' if c == '(' else ']', i)
            if j > 0:
                ki.append(s[i:j + 1])
                i = j + 1
                continue
        if c in '([':
            mely += 1
        elif c in ')]' and mely:
            mely -= 1
        elif not mely:
            ki.append(c)
        i += 1
    return ''.join(ki)


_CIM_IRASJEL = re.compile(r'[;:=]')
_CIM_HEBER = re.compile(r'[׳״]?[֐-׿יִ-ﭏ]')


def jelentes_cim(szoveg, vesszoig=False, max_hossz=48):
    nyers = re.sub(r'\s+', ' ', szoveg or '').strip()
    s = re.sub(r'\s+', ' ', _zarojel_nelkul(nyers)).strip().lstrip(' =:;,.—-')
    kp = _CIM_IRASJEL.search(s)
    if kp and s[kp.start()] == ':' and len(re.findall(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2,}', s[:kp.start()])) <= 1:
        kp = _CIM_IRASJEL.search(s, kp.end())        # „+ מִן comparativus: rosszabb, mint”: a jelentés a kettőspont után áll
    hatar = [m.start() for m in (_CIM_REF.search(s), kp, re.search(r'\s—\s', s),
                                 re.search(r',', s) if vesszoig else None) if m]
    b = _CIM_BETUK.search(s)
    if b:
        # a magyar szöveg utáni héber idézet határ, ha utána nem a magyar mondat folytatódik (hanem hivatkozás, írásjel, vége), és
        # előtte nem egyetlen szó áll vessző nélkül („ellentéte עֶרֶב”); a vezető héber kifejezés marad
        h = _CIM_HEBER.search(s, b.end())
        if h:
            vege = re.match(r'(?:[֐-׿יִ-ﭏ׳״\'־\-]+\s*)+', s[h.start():])
            folytatodik = re.match(r'\s*[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2}', s[h.start() + (vege.end() if vege else 0):])
            elotag = s[:h.start()].strip()
            egy_szo = ' ' not in elotag and ',' not in elotag
            if not folytatodik and not egy_szo:
                hatar.append(h.start())
    if hatar:
        s = s[:min(hatar)]
    s = re.sub(r'\s+', ' ', s).strip(' ,;:=—-.')
    if not _CIM_BETUK.search(s):
        if vesszoig:
            return ''
        s = nyers
    return _rovid(s, max_hossz)


# A BDB rövidítéseinek jelmagyarázata (konfig/bdb_jelek.tsv, kézi összeállítás): a jelentések szövegében <abbr>-ral jelölve, a blokk végén
# a szócikkben előforduló jelek listája. A forrásjelek (J, E, P …) csak zárójelben („(J)”, „(mind P)”, „(mindkettő J E)”) jelölők.
def _bdb_jelek_betolt():
    ut = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'konfig', 'bdb_jelek.tsv')
    jelek, fej = {}, None
    with open(ut, encoding='utf-8') as f:
        for sor in f:
            sor = sor.rstrip('\n')
            if not sor or sor.startswith('#'):
                continue
            mezok = sor.split('\t')
            if fej is None:
                fej = mezok
                continue
            d = dict(zip(fej, mezok))
            jelek[d['jel']] = (d['feloldas'], d['csoport'])
    return jelek


BDB_JELEK = _bdb_jelek_betolt()
_FORRASJEL = sorted((j for j, (_, cs) in BDB_JELEK.items() if cs == 'forrásjel'), key=len, reverse=True)
_SZOJEL = sorted((j for j, (_, cs) in BDB_JELEK.items() if cs != 'forrásjel'), key=len, reverse=True)
_HATAR = r'\w֐-׿יִ-ﭏ'
_SZOJEL_RE = re.compile(r'(?<![%s])(%s)(?![%s])' % (_HATAR, '|'.join(re.escape(j) for j in _SZOJEL), _HATAR))
_FJ = '|'.join(re.escape(j) for j in _FORRASJEL)
_FORRAS_ZAROJEL_RE = re.compile(r'\(((?:(?:mind|mindkettő|mindhárom)\s+)?(?:%s)(?:\s+(?:%s))*)\)' % (_FJ, _FJ))
_FORRAS_BETU_RE = re.compile(r'(?<![\w])(%s)(?![\w])' % _FJ)


def _abbr(jel):
    return Markup('<abbr title="%s">%s</abbr>') % (BDB_JELEK[jel][0], jel)


def _jeles(szoveg, talalt=None):
    """A szöveg escape-elve, a jelmagyarázat jelei <abbr>-ral; a `talalt` halmazba gyűjti a megjelölt jeleket."""
    ki, poz = [], 0
    s = szoveg or ''
    for m in _FORRAS_ZAROJEL_RE.finditer(s):
        ki.append(_jeles_szojel(s[poz:m.start()], talalt))
        belso = Markup('')
        bp = 0
        for b in _FORRAS_BETU_RE.finditer(m.group(1)):
            belso += escape(m.group(1)[bp:b.start()]) + _abbr(b.group(1))
            if talalt is not None:
                talalt.add(b.group(1))
            bp = b.end()
        ki.append(Markup('(') + belso + escape(m.group(1)[bp:]) + Markup(')'))
        poz = m.end()
    ki.append(_jeles_szojel(s[poz:], talalt))
    return Markup('').join(ki)


def _jeles_szojel(s, talalt):
    ki, poz = Markup(''), 0
    for m in _SZOJEL_RE.finditer(s):
        ki += escape(s[poz:m.start()]) + _abbr(m.group(1))
        if talalt is not None:
            talalt.add(m.group(1))
        poz = m.end()
    return ki + escape(s[poz:])


def _jelmagyarazat_html(talalt):
    if not talalt:
        return Markup('')
    rend = {'forrásjel': 0, 'szövegtanú': 1, 'rövidítés': 2, 'szerző': 3}
    sorok = sorted(talalt, key=lambda j: (rend.get(BDB_JELEK[j][1], 9), j))
    return Markup('<dl class="jelmagyarazat">%s</dl><p class="megj">A feloldás nem a BDB része; csak a fenti jelentésekben előforduló '
                  'jelek. A szövegben a pontozottan aláhúzott jelre mutatva is megjelenik.</p>') % Markup('').join(
        Markup('<dt>%s</dt><dd>%s</dd>') % (j, BDB_JELEK[j][0]) for j in sorok)


def _fo_cim(j):
    sajat = jelentes_cim(j['szoveg'], vesszoig=True) and jelentes_cim(j['szoveg'], max_hossz=70)
    return sajat or (jelentes_cim(j['al'][0]['szoveg'], vesszoig=True) if j['al'] else '')


def _fo_cim_html(j):
    """A főjelentés címe; ha a BDB-ben a főjelentésnek nincs saját meghatározása, a cím az első alpontból kölcsönzött: ezt a
    megjelenés jelzi (halvány, dőlt, súgóval), hogy ne tűnjön a BDB főjelentés-szövegének."""
    cim = _cim_html(_fo_cim(j))
    if jelentes_cim(j['szoveg'], vesszoig=True) or not j['al']:
        return cim
    return Markup('<span class="kolcsonzott" title="A BDB-ben ennek a jelentésnek nincs saját meghatározása; a cím az %s. alpontból '
                  'képződik (gépi).">%s</span>') % (j['al'][0]['jel'], cim)


# a címben a héber szavak (pontozott betűk, geres, maqqéf, szón belüli zárójel) futama
_HEB_SZO = r"[׳״']?[֐-׿יִ-ﭏ][֐-׿יִ-ﭏ׳״'־()\-]*"
_HEB_FUTAM = re.compile(r'%s(?:\s+%s)*' % (_HEB_SZO, _HEB_SZO))


def _cim_html(cim):
    """A cím megjelenítése: a vezető héber kifejezés a magyar szöveg mögé kerül („gonosz tervet kigondolni מַחֲשֶׁבֶת(ה)רָעָה חָשַׁב”), hogy a
    jelentés álljon elöl; minden héber futam lang="he"-vel, elkülönítve. A szavak nem változnak, csak a vezető héber helye."""
    m = _HEB_FUTAM.match(cim or '')
    if m and _CIM_BETUK.search(cim[m.end():]):
        cim = '%s %s' % (cim[m.end():].strip(' ,;:'), m.group(0))
    ki, poz = Markup(''), 0
    for h in _HEB_FUTAM.finditer(cim or ''):
        ki += escape(cim[poz:h.start()]) + Markup('<span class="he" lang="he">%s</span>') % h.group(0)
        poz = h.end()
    return ki + escape((cim or '')[poz:])


def _jel_id(elotag, ti, jel, al=''):
    return '%s-%d-%s%s' % (elotag, ti, jel or 'x', al)


def _vazlat_html(tl, elotag):
    """A jelentésszerkezet vázlata: főjelentésenként a jelölő, a cím és a helyszám, alatta az alpontok címe; minden sor a részletes
    jelentésre ugrik. A számozatlan előtag (igéknél az alak-lista) kimarad. Üres, ha egyetlen jelentés van alpontok nélkül."""
    torzsek = [(ti, t, [j for j in t['jelentesek'] if j['jel']]) for ti, t in enumerate(tl)]
    if not any(len(js) > 1 or any(j['al'] for j in js) for _, _, js in torzsek):
        return Markup('')
    ki = Markup('')
    for ti, t, js in torzsek:
        if not js:
            continue
        if t['nev']:
            ki += Markup('<p class="vz-torzs">%s</p>') % t['nev']
        sorok = Markup('')
        for j in js:
            al = Markup('')
            if j['al']:
                al = Markup('<span class="vz-al">%s</span>') % Markup(' · ').join(
                    Markup('<a href="#%s">%s. %s</a>') % (_jel_id(elotag, ti, j['jel'], s['jel']), s['jel'], _cim_html(jelentes_cim(s['szoveg']))) for s in j['al'])
            sorok += Markup('<li><a class="vz-fo" href="#%s"><span class="vz-jel">%s</span>%s</a>%s%s</li>') % (
                _jel_id(elotag, ti, j['jel']), j['jel'], _fo_cim_html(j), _helyek(j['ref']), al)
        ki += Markup('<ol>%s</ol>') % sorok
    return Markup('<nav class="jel-vazlat" aria-label="A jelentésszerkezet vázlata">%s</nav>') % ki


def _torzsek_html(tl, elotag='bdb', talalt=None):
    ki = Markup('')
    for ti, t in enumerate(tl):
        fej = Markup('')
        if t['nev']:
            fej = Markup('<h5>%s%s</h5>') % (t['nev'], Markup('<span class="helyek">%s előfordulás a BDB szerint</span>') % t['db'] if t['db'] else '')
        li = Markup('')
        for i, j in enumerate(t['jelentesek']):
            al = Markup('')
            if j['al']:
                al = Markup('<ol class="al">%s</ol>') % Markup('').join(
                    Markup('<li id="%s" data-jel="%s."><p class="jsz">%s</p>%s</li>') % (
                        _jel_id(elotag, ti, j['jel'], s['jel']), s['jel'] or '', _jeles(s['szoveg'], talalt), _helyek(s['ref'])) for s in j['al'])
            sajat = Markup('<p class="jsz">%s</p>') % _jeles(j['szoveg'], talalt) if j['szoveg'] else Markup('')
            li += Markup('<li id="%s" data-jel="%s"><details open><summary><span class="jcim">%s</span>%s</summary>%s%s</details></li>') % (
                _jel_id(elotag, ti, j['jel'] or 'x%d' % i), j['jel'] or '·', _fo_cim_html(j), _helyek(j['ref']), sajat, al)
        ki += Markup('<div class="torzs">%s<ol class="jel">%s</ol></div>') % (fej, li)
    return ki


# DT-F99l (c) (felhasználó, 2026-10-15): a BDB-szeletelő „próba” jelöléssel élesedik; a lapon a NYERS mért pontosság áll (a seed-101 vak
# minta, 200 véletlen igehely, jelentéspont: 184/200; Clopper–Pearson 95%), az ítélet utáni érték csak a naplóban (naplok/BDB_SZELETELO_M0.md 9.11)
BDB_MERT_PONTOSSAG = ('Mért pontosság (jelentéspont, 200 véletlen igehely vak ellenőrzéssel, 2026-10-15): 92,0% '
                      '(95%-os konfidencia-intervallum: 87,3–95,4%).')
SZAKASZ_CIM = {'elo': 'Zárójeles előszócikk (más gyök)', 'arámi': "Arámi (Pe'al) rész", 'azonos_lemma': 'További homonima ugyanezen a lemmán', 'masik_lemma': 'Másik szó (más lemma)',
               'tagolas': 'rész (a címszó fő tagolása)'}


def _f_bdb_apparatus(K):
    return _bdb_bontas(K)


def _r_bdb_apparatus(d, K):
    """A pilot `apparatus()` átirata: a `bdb_szelet.szeletel` kimenete, minden szöveg escape-elve (csak a saját, escape-elt elemek Markup)."""
    a, hu = d['appar'], d['hu']
    forras = 'BDB (Brown–Driver–Briggs), magyar fordítás · gépi bontás' if hu else 'BDB (Brown–Driver–Briggs), angol eredeti · gépi bontás'

    def resz(cim, tartalom):
        return Markup('<div class="app"><h4>%s</h4><p class="forrasnev"><span class="fcim">Forrás</span> %s</p>%s</div>') % (cim, forras, tartalom)

    ki = Markup('<span class="allapot%s">%s</span>') % ('' if hu else ' folyamat', ('Lefordítva · %s' % d['meta']) if hu else 'Magyar fordítás nincs · az angol eredeti áll')
    if d['alias']:
        al = d['alias']
        ki += Markup('<p class="megj">A szócikk a(z) %s Strong-szám alatt áll (%s, szövegi hasonlóság %s; a BDB_strong_alias.tsv alias-párosítása).</p>') % (al['tabla_strong'], al['bdb_id'], al['hasonlosag'])
    ki += Markup('<p class="megj">Gépi szeletelés (próba): a határokat a szócikk saját jelölői adják (gondolatjel, sorszámok, törzsnevek); hibás határ előfordulhat. A szöveg nem változik. %s</p>') % BDB_MERT_PONTOSSAG
    fej = a['fej']
    ki += resz('Címszó', Markup('<div class="cimszo"><span class="he" lang="he">%s</span><span>%s</span>%s<span class="helyek">%s igehely-hivatkozás a szócikkben</span></div>') % (
        fej.get('heber') or '', ' · '.join(x for x in (fej.get('atiras'), ('%s. címszó' % fej['homonima']) if fej.get('homonima') else '') if x),
        Markup('<span class="helyek">%s előfordulás (BDB)</span>') % fej['ossz'] if fej.get('ossz') else '', a['ref_ossz']))
    ki += resz('Alapjelentés és szófaj', Markup('<p class="jsz">%s</p>') % (a['alap'] or '—'))
    if a.get('szakaszok'):
        # F99 M2: a `tagolas` szerepű szakasz a címszó saját római számos fő tagolása (H1961, H1285), nem más szócikk
        for tag_e, cimsor in ((False, 'Ugyanabban a BDB-sorban további szakaszok (%d) — nem ennek a címszónak a szerkezete'),
                              (True, 'A címszó fő tagolása (%d rész, római számmal)')):
            reszek, db = Markup(''), 0
            for k, x in enumerate(a['szakaszok']):
                if (x['szerep'] == 'tagolas') != tag_e:
                    continue
                db += 1
                cim = SZAKASZ_CIM['elo'] if x['szerep'] == 'elo' else (SZAKASZ_CIM['arámi'] if x['nyelv'] == 'arámi' else SZAKASZ_CIM[x['szerep']])
                if x['szerep'] != 'elo' and x.get('jel'):
                    cim = '%s. %s' % (x['jel'], cim)
                ny = Markup('<ul class="lista">%s</ul>') % Markup('').join(Markup('<li>%s</li>') % n for n in x['nyelvi']) if x['nyelvi'] else Markup('')
                reszek += Markup('<details open><summary class="megj">%s · <span class="he" lang="he">%s</span> · %s%s</summary>%s%s</details>') % (
                    cim, x['heber'] or '', _rovid(x['alap'] or '—', 80), _helyek(x.get('ref')), ny, _torzsek_html(x['torzsek'], 'bdb-s%d' % k))
            if db:
                ki += resz(cimsor % db, reszek)
    if a.get('nyelvi'):
        ki += resz('Nyelvi háttér (etimológia, rokon nyelvek)', Markup('<ul class="lista">%s</ul>') % Markup('').join(Markup('<li>%s</li>') % n for n in a['nyelvi']))
    if a.get('alaktan'):
        ki += resz('Alakok (alaktani apparátus)', Markup('<details open><summary class="megj">%s</summary><p class="jsz">%s</p></details>') % (_rovid(a['alaktan'], 120), a['alaktan']))
    talalt = set()
    ki += resz('Jelentésszerkezet törzsenként' if any(t['nev'] for t in a['torzsek']) else 'Jelentésszerkezet',
               _vazlat_html(a['torzsek'], 'bdb') + _torzsek_html(a['torzsek'], 'bdb', talalt))
    if talalt:
        ki += Markup('<div class="app"><h4>Jelmagyarázat</h4><p class="forrasnev"><span class="fcim">Forrás</span> projekt_adat '
                     '(konfig/bdb_jelek.tsv), kézi összeállítás · proveniencia: manual</p>%s</div>') % _jelmagyarazat_html(talalt)
    if a.get('irodalom') or a.get('krit'):
        ki += resz('Irodalmi és szövegkritikai jelek', Markup('<div class="jelek">%s%s</div>') % (
            Markup('').join(Markup('<span class="jel-cimke" title="BDB irodalmi hivatkozás (szerző^mű)">%s</span>') % x for x in a.get('irodalom') or []),
            Markup('').join(Markup('<span class="jel-cimke krit" title="a BDB jele">%s</span>') % x for x in a.get('krit') or [])))
    return _rovidites(K, ki)


def _f_lxx_tobblet(K):
    return {'hiany': True}


def _r_lxx_tobblet(d, K):
    return Markup('<p class="ures">Az adat még nincs a DB-ben: a LXX_tobblet_szakaszok.tsv és a Verzifikacios_elteres_tabla.tsv a pardes.db következő újraépítésekor '
                  'kerül be (N-F76j). Üres eredmény itt nem jelenti azt, hogy a versnek nincs LXX-többlete vagy számozási eltérése.</p>')


def _f_bdb_angol(K):
    d = _bdb_adat(K)
    return d if d['en'] else None


def _r_bdb_angol(d, K):
    return (_alias_megj(d['alias']) if d['alias'] else Markup('')) + _rovidites(K, _szoveg(d['en']))


def _f_bdb_magyar(K):
    d = _bdb_adat(K)
    return d if d['hu'] else None


def _r_bdb_magyar(d, K):
    return (_alias_megj(d['alias']) if d['alias'] else Markup('')) + _rovidites(K, _szoveg(d['hu']))


def _f_lxx_bridge(K):
    return q.lxx_bridge_h(K.con, K.strong)[:10] or None


def _r_lxx_bridge(d, K, irany='h'):
    cimk = K.kozos_szotar([g for _, g in d])
    return _tabla(['Görög Strong', 'Szótő', 'Jelentés', 'Darab'], [[strong_link(K, g), _gor(cimk.get(g, ('', ''))[0]), cimk.get(g, ('', ''))[1] or '', str(c)] for c, g in d])


def _r_sdbh(d, K):
    return _tabla(['Domén kód', 'Domén', 'Glossza', 'Hivatkozás'], [[a or '', b or '', c or '', str(n or '')] for a, b, c, n in d])


def _f_sdbh(K):
    return q.sdbh(K.con, K.strong)


def _f_sece_h(K):
    return q.sece_h(K.con, K.strong)


def _r_szoveg(d, K):
    return _szoveg(d)


def _f_oshl(K):
    lex, hely = q.oshl(K.con, K.strong)
    return (lex, hely) if (lex or hely) else None


def _r_oshl(d, K):
    lex, hely = d
    ki = _tabla(['TWOT', 'BDB-azonosító', 'Nyelv', 'OSHL-azonosító', 'Lemma', 'Átírás', 'Szófaj', 'Angol meghatározás'],
                [[a or '', b or '', c or '', f or '', _heb(g), h or '', i or '', j or ''] for a, b, c, f, g, h, i, j in lex])
    if hely:
        ki += Markup('<h4>BDB-helyek (az első %d)</h4>') % len(hely)
        ki += _lista([Markup('%s %s:%s (%s)') % (k, f, v, b) for b, k, f, v in hely])
    return ki


def _f_oshl_csalad(K):
    d = q.oshl_csalad(K.con, K.strong)
    return d if d is not None else {'nincs_oszlop': True}


def _r_oshl_csalad(d, K):
    """„Rokon szavak” (F99 M1): a gyök és a származékai Strong-linkkel; ha nincs család, kifejezett felirat (nem negatív lelet)."""
    if d.get('nincs_oszlop'):
        return Markup('<p class="ures">Az adatbázisban még nincs OSHL-gyökcsalád adat (a pardes.db újraépítése után jelenik meg).</p>')
    if not d['csaladok']:
        if 'single' in d['tipusok']:
            return Markup('<p class="ures">Nincs OSHL-gyökcsalád: az OSHL a szót családon kívüliként jelöli (single). Nem negatív lelet.</p>')
        return Markup('<p class="ures">Nincs OSHL-gyökcsalád (az OSHL-ben ehhez a szóhoz nincs gyökcsalád-adat). Nem negatív lelet.</p>')
    ki = Markup('')
    for cs in d['csaladok']:
        oid, st, lemma, atiras, szofaj, def_en, gyok = cs['gyok']
        nev = gyok if gyok and gyok != '—' else lemma
        ki += Markup('<h4>Gyök: %s %s</h4>') % (_heb(nev), strong_link(K, st) if st and st != '—' else Markup('(Strong-szám nélküli gyök-bejegyzés)'))
        sorok = []
        for t_oid, t_st, t_lemma, t_atiras, t_szofaj, t_def in cs['tagok']:
            sorok.append([strong_link(K, t_st) if t_st and t_st != '—' else '—', _heb(t_lemma), t_atiras or '', t_szofaj or '', t_def or ''])
        if sorok:
            ki += _tabla(['Strong', 'Lemma', 'Átírás', 'Szófaj', 'Angol meghatározás'], sorok)
        else:
            ki += Markup('<p class="ures">A gyök-bejegyzésnek nincs felsorolt származéka.</p>')
    return ki


def _f_tbesh(K):
    return q.tbesh(K.con, K.strong)


def _r_tbesh(d, K):
    return _tabla(['Szó', 'Átírás', 'Morf', 'Gloss', 'Jelentés'], [[_heb(a), b or '', c or '', dd or '', f or ''] for a, b, c, dd, f in d])


def _f_tw(K):
    return q.tw(K.con, K.strong)


def _r_tw(d, K):
    return Markup('').join(Markup('<h4>%s <span class="megj">(%s, %s)</span></h4>') % (cim, kat or '', twid) + _szoveg(sz) for twid, kat, cim, sz in d)


def _f_nyelvtani(K):
    return q.nyelvtani(K.con, K.strong) or ('', '', '')


def _r_nyelvtani(d, K):
    if not d[0] and not d[1]:
        return Markup('<p class="megj">Nem szerepel a nyelvtani Strong-számok szűrésében (tartalmas szó).</p>')
    return Markup('<p>Nyelvtani Strong-szám (%s): %s. %s</p>') % (d[0] or '', d[1] or '', d[2] or '')


# ---------------------------------------------------------------------------------------------------------------------
# görög szó-lap blokkok: K.strong
# ---------------------------------------------------------------------------------------------------------------------
def _f_tbesg(K):
    return q.tbesg(K.con, K.strong)


def _r_tbesg(d, K):
    szo, atiras, gloss, jel = d
    return _tabla(['Szó', 'Átírás', 'Gloss'], [[_gor(szo), atiras or '', gloss or '']]) + _szoveg(jel)


def _f_thayer(K):
    return q.thayer(K.con, K.strong)


def _f_magyar_gorog(K):
    return q.magyar_gorog(K.con, K.strong)


def _r_magyar_gorog(d, K):
    cimke = {'glosszak_hu': ' · glossza', 'definicio_hu': ' · definíció'}
    return Markup('').join(Markup('<h4>%s, %s. jelentés%s</h4>') % (sz, jsz or '', cimke.get(mezo, '')) + _szoveg(fh) for sz, jsz, fh, mezo in d)


def _f_ubs_dbh(K):
    if not K.strong or K.strong[0] != 'H':
        return None
    return q.ubs_dbh_szo(K.con, K.strong) or None


def _r_ubs_dbh(d, K):
    return _tabla(['Azonosító', 'Domén', 'Glossza (magyar)', 'Definíció (magyar)', 'Glossza (angol)', 'Definíció (angol)'],
                  [[lex, dom or '', gh or '(fordításra vár)', dh or '(fordításra vár)', ge or '', de or ''] for lex, dom, de, ge, dh, gh in d])


def _f_usz(K):
    n, v, versek = q.usz(K.con, K.strong)
    return (n, v, versek, q.usz_lanc(K.con, K.strong)) if n else None


def _r_usz(d, K):
    n, v, versek, lanc = d
    ki = Markup('<p><b>%d</b> előfordulás <b>%d</b> versben.</p>') % (n, v)
    if lanc:
        ki += Markup('<p class="megj">A számlálás bontása: <b>%d</b> előfordulás, ebből <b>%d</b> láncelemként (a TAGNT „+” Strong-láncában, pl. krázis-alaknál); '
                     'az egész mezős előfordulás %d. A <code>token_strong</code> a láncelemeket is számolja (DT-F76d).</p>') % (n, lanc, n - lanc)
    return ki + _tabla(['Igehely', 'Károli-szöveg'], [[ig_link(K, ig), t] for ig, t in versek])


def _f_heber_hatter(K):
    return q.lxx_bridge_g(K.con, K.strong)[:10] or None


def _r_heber_hatter(d, K):
    cimk = K.kozos_szotar([h for _, h in d])
    return _tabla(['Héber Strong', 'Szótő', 'Jelentés', 'Darab'], [[strong_link(K, h), _heb(cimk.get(h, ('', ''))[0]), cimk.get(h, ('', ''))[1] or '', str(c)] for c, h in d])


def _f_sdgnt(K):
    return q.sdgnt(K.con, K.strong)


def _f_sece_g(K):
    return q.sece_g(K.con, K.strong)


def _f_lsj(K):
    return q.lsj(K.con, K.strong)


def _f_mcged(K):
    return q.mcged(K.con, K.strong)


def _r_mcged(d, K):
    return _tabla(['GK-szám', 'Lemma', 'Átírat', 'Gyakoriság', 'Glossza'], [[a or '', _gor(b), c or '', str(dd or ''), f or ''] for a, b, c, dd, f in d])


def _f_ubs_dntg(K):
    jel, ref = q.ubs_dntg(K.con, K.strong)
    return (jel, ref) if (jel or ref) else None


def _r_ubs_dntg(d, K):
    jel, ref = d
    ki = _tabla(['Azonosító', 'Domén', 'Rövid definíció', 'Glosszák'], [[a, b or '', c or '', dd or ''] for a, b, c, dd in jel])
    if ref:
        ki += Markup('<h4>Előfordulások (az első %d)</h4>') % len(ref)
        ki += _lista([Markup('%s: %s') % (lex, ig_link(K, ig)) for lex, ig in ref])
    return ki


# ---------------------------------------------------------------------------------------------------------------------
# a regiszter
# ---------------------------------------------------------------------------------------------------------------------
B = Blokk
REGISZTER = [
    # vers-lap
    B('vers.karoli', 'vers', 'Károli-szöveg', 'forras', ('vers',), _f_karoli, _r_karoli),
    B('vers.heber_csempe', 'vers', 'Héber szöveg', ('forras', 'gepi'), ('token_eredeti', 'token_macula', 'lxx_token', 'morf_kulcs_heber', 'morf_nyelv_aramai'), _f_heber_csempe, _r_heber_csempe,
      'szavankénti csempék; a táblázatos nézet alább'),
    B('vers.lxx_csempe', 'vers', 'Septuaginta (LXX, Rahlfs)', 'forras', ('lxx_token',), _f_lxx_csempe, _r_lxx_csempe, 'szavankénti csempék; a táblázatos nézet alább'),
    B('vers.par', 'vers', 'Károli–Strong párosítás', 'modell', ('token_par',), _f_par, _r_par, 'a pontozott aláhúzás a szövegben is modell-kimenet'),
    B('vers.eredeti', 'vers', 'Eredeti szavak (TAHOT / TAGNT)', 'forras', ('token_eredeti',), _f_eredeti, _r_eredeti),
    B('vers.macula_morf', 'vers', 'Igealak-kód és szófaj (Macula)', 'forras', ('token_macula',), _f_macula, _r_macula_morf),
    B('vers.macula_gorog', 'vers', 'Héber–görög párosítás szavanként (Macula)', 'forras', ('token_macula',), _f_macula, _r_macula_gorog),
    B('vers.lxx_szavak', 'vers', 'Görög szóalak és LXX-vers szavai (LXX_OS)', 'forras', ('lxx_token',), _f_lxx_szavak, _r_lxx_szavak),
    B('vers.lxx_versszam', 'vers', 'LXX-versszám', 'forras', ('lxx_versszam',), _f_lxx_versszam, _r_lxx_versszam),
    B('vers.versszamozas', 'vers', 'Versszámozás (MT / KJV)', 'forras', ('vers_szamozas',), _f_versszamozas, _r_versszamozas),
    B('vers.bsb', 'vers', 'Angol szavak szavanként (BSB)', ('forras', 'gepi'), ('bsb',), _f_bsb, _r_angol),
    B('vers.kjv', 'vers', 'Angol szavak szavanként (KJV + Strong)', ('forras', 'gepi'), ('kjv',), _f_kjv, _r_angol, 'a Strong-címkék GPL-eredetűek: nyilvános kiadásból kimarad'),
    B('vers.nave', 'vers', 'Témák (Nave, versekre bontva)', ('forras', 'gepi'), ('nave_vers', 'nave_basokant'), _f_nave, _r_nave),
    B('vers.tipnr', 'vers', 'Tulajdonnevek (TIPNR)', ('forras', 'gepi'), ('tipnr',), _f_tipnr, _r_tipnr),
    B('vers.morf_hu', 'vers', 'Az igealak magyar feloldása', 'gepi', ('morf_kulcs_heber', 'token_macula', 'morf_nyelv_aramai'), _f_morf_hu, _r_morf_hu),
    B('vers.motivum', 'vers', 'Motívumadat (adatréteg)', 'forras', ('elofordulasok', 'motivumok'), _f_motivum, _r_motivum, 'soronként saját proveniencia-mező'),
    B('vers.kapcsolat', 'vers', 'Igehely-kapcsolatok (adatréteg)', 'forras', ('kapcsolatok',), _f_kapcsolat, _r_kapcsolat),
    B('vers.lxx_dontes', 'vers', 'LXX-fordítói döntések (adatréteg)', 'forras', ('lxx_dontesek',), _f_lxx_dontes, _r_lxx_dontes, 'soronként saját proveniencia-mező'),
    B('vers.lxx_par', 'vers', 'LXX versszintű együttelőfordulás', 'forras', ('lxx_versszintu_parok',), _f_lxx_par, _r_lxx_par, 'együttelőfordulás a versben, nem szóillesztés'),
    B('vers.lxx_tobblet', 'vers', 'LXX többlet és számozási eltérés', 'forras', (), _f_lxx_tobblet, _r_lxx_tobblet, 'az adat még nincs a DB-ben (N-F76j)',
      forras_szoveg='LXX_tobblet_szakaszok.tsv, Verzifikacios_elteres_tabla.tsv (Versifikacios_tablak; licenc: adat/licencek.tsv; a pardes.db-ben még nincsenek)'),
    B('vers.tsk', 'vers', 'Kereszthivatkozások (TSK)', 'forras', ('tsk',), _f_tsk, _r_tsk),
    B('vers.kh', 'vers', 'Károli-kereszthivatkozások', 'forras', ('kh',), _f_kh, _r_kh),
    B('vers.ubs', 'vers', 'UBS-jelentés az előfordulásra', 'forras', ('ubs_dbh_referenciak', 'ubs_dbh_jelentesek'), _f_ubs, _r_ubs),
    # héber szó-lap
    B('szo.szotar', 'szo_h', 'Strong-szótár', 'forras', ('strong_szotar',), _f_szotar, _r_szotar),
    B('szo.elofordulas', 'szo_h', 'Előfordulás, könyvek száma', 'gepi', ('token_strong',), _f_elofordulas, _r_elofordulas),
    B('szo.ebben', 'szo_h', 'Ebben a versben', ('forras', 'gepi', 'modell'), ('token_par', 'token_eredeti', 'token_macula', 'lxx_token', 'ubs_dbh_referenciak', 'ubs_dbh_jelentesek', 'morf_kulcs_heber', 'morf_nyelv_aramai'), _f_ebben, _r_ebben, vers_kell=True,
      kovet=('vers.ubs', 'vers.heber_csempe', 'vers.par')),     # az UBS DBH-, a héber csempe- és a párosítás-adat blokkjainak láthatóságát követi
    B('szo.karoli_alakok', 'szo_h', 'Károli-alakok és bizonyosság', 'modell', ('token_par',), _f_karoli_alakok, _r_karoli_alakok),
    B('szo.bdb_apparatus', 'szo_h', 'BDB-szócikk apparátusokra bontva', ('forras', 'modell', 'gepi'), ('bdb', 'bdb_alias', 'forditasok'), _f_bdb_apparatus, _r_bdb_apparatus,
      'a pilot gépi szeletelése (bdb_szelet.py); hibás határ előfordulhat',
      kovet=('szo.bdb_magyar',), jelleg_fn=lambda d: ('forras', 'modell', 'gepi') if d['hu'] else ('forras', 'gepi')),     # modell-kimenet csak a magyar fordításból készült bontásnál
    B('szo.bdb_angol', 'szo_h', 'BDB-szócikk (angol)', 'forras', ('bdb', 'bdb_alias'), _f_bdb_angol, _r_bdb_angol, 'az alias gépi feldolgozás'),
    B('szo.bdb_magyar', 'szo_h', 'BDB-szócikk (magyar fordítás)', 'modell', ('forditasok',), _f_bdb_magyar, _r_bdb_magyar),
    B('szo.lxx_bridge', 'szo_h', 'Görög megfelelő (lxx_bridge)', 'forras', ('lxx_bridge',), _f_lxx_bridge, _r_lxx_bridge),
    B('szo.ubs_dbh', 'szo_h', 'UBS DBH jelentések (a teljes szócikk, magyar fordítással)', ('forras', 'modell'), ('ubs_dbh_jelentesek', 'forditasok'), _f_ubs_dbh, _r_ubs_dbh,
      'CC BY-SA 4.0 (UBS); a magyar glossza és definíció modell-kimenet (#121)'),
    B('szo.sdbh', 'szo_h', 'Szemantikai domén (SDBH)', 'forras', ('sdbh_domenek',), _f_sdbh, _r_sdbh, 'üres eredmény nem negatív lelet'),
    B('szo.sece_h', 'szo_h', 'SECE-szócikk (héber)', 'forras', ('sece_h',), _f_sece_h, _r_szoveg),
    B('szo.oshl', 'szo_h', 'OSHL: TWOT- és BDB-azonosító, BDB-helyek', 'forras', ('oshl_lexikalis_index', 'oshl_bdb_igehelyek'), _f_oshl, _r_oshl),
    B('szo.oshl_csalad', 'szo_h', 'Rokon szavak (OSHL-gyökcsalád)', 'forras', ('oshl_lexikalis_index',), _f_oshl_csalad, _r_oshl_csalad,
      'az OSHL <etym> eleme: a gyök és a származékai; üres család nem negatív lelet'),
    B('szo.tbesh', 'szo_h', 'Bővített Strong-szócikk (TBESH)', ('forras', 'gepi'), ('tbesh',), _f_tbesh, _r_tbesh),
    B('szo.tw_h', 'szo_h', 'translationWords', 'forras', ('tw_szocikkek',), _f_tw, _r_tw),
    B('szo.nyelvtani', 'szo_h', 'Nyelvtani Strong-számok szűrése', 'gepi', ('grammatikai_strongok',), _f_nyelvtani, _r_nyelvtani),
    # görög szó-lap
    B('szo.tbesg', 'szo_g', 'TBESG', 'forras', ('tbesg',), _f_tbesg, _r_tbesg),
    B('szo.thayer', 'szo_g', 'Thayer (angol)', 'forras', ('thayer',), _f_thayer, _r_szoveg),
    B('szo.magyar_gorog', 'szo_g', 'Magyar jelentés (Thayer, UBS DNTG)', 'modell', ('forditasok',), _f_magyar_gorog, _r_magyar_gorog),
    B('szo.usz', 'szo_g', 'ÚSZ-előfordulás és versek', 'forras', ('token_strong', 'vers'), _f_usz, _r_usz),
    B('szo.heber_hatter', 'szo_g', 'Héber háttér (lxx_bridge)', 'forras', ('lxx_bridge',), _f_heber_hatter, _r_heber_hatter),
    B('szo.sdgnt', 'szo_g', 'Szemantikai domén (SDGNT)', 'forras', ('sdgnt_domenek',), _f_sdgnt, _r_sdbh, 'üres eredmény nem negatív lelet'),
    B('szo.sece_g', 'szo_g', 'SECE-szócikk (görög)', 'forras', ('sece_g',), _f_sece_g, _r_szoveg),
    B('szo.lsj', 'szo_g', 'LSJ', 'forras', ('lsj',), _f_lsj, _r_szoveg),
    B('szo.mcged', 'szo_g', 'MCGED (Mounce)', 'forras', ('mcged',), _f_mcged, _r_mcged, 'nem kereskedelmi: kereskedelmi kiadásból kimarad'),
    B('szo.ubs_dntg', 'szo_g', 'UBS DNTG jelentés', 'forras', ('ubs_dntg_jelentesek', 'ubs_dntg_referenciak'), _f_ubs_dntg, _r_ubs_dntg),
    B('szo.tw_g', 'szo_g', 'translationWords', 'forras', ('tw_szocikkek',), _f_tw, _r_tw),
]
BLOKK_ID = {b.id: b for b in REGISZTER}
assert len(BLOKK_ID) == len(REGISZTER), 'ismétlődő blokk-azonosító'
OLDALAK = ('vers', 'szo_h', 'szo_g')


def blokkok_oldalra(oldal):
    return [b for b in REGISZTER if b.oldal == oldal]


# ---------------------------------------------------------------------------------------------------------------------
# a blokk HTML-je: jelleg-címke + tartalom + forrás- és licencsor (a regiszterből, kihagyhatatlanul)
# ---------------------------------------------------------------------------------------------------------------------
def forras_sor(b, kozos):
    """Forrás- és licencsor a `tabla_licenc`/`licencek` táblákból: dataset, licenc-címke, jelzések."""
    if b.forras_szoveg:
        return 'Forrás és licenc: ' + b.forras_szoveg
    reszek, lat = [], set()
    for t in b.tablak:
        l = kozos.licenc.get(t)
        if not l:
            raise BlokkHiba('a(z) %s blokk %s táblájának nincs licencsora a tabla_licenc táblában' % (b.id, t))
        kulcs = (l['dataset'], l['cimke'])
        if kulcs in lat:
            continue
        lat.add(kulcs)
        jel = []
        if l['allapot'] == 'tisztazatlan':
            jel.append('tisztázatlan')
        if l['kereskedelmi'] == 'nem':
            jel.append('nem kereskedelmi')
        elif l['kereskedelmi'] == 'feltetelesen':
            jel.append('feltételesen kereskedelmi')
        sa = any(kozos.share_alike.get(d) == 'igen' for d in l['dataset'].split('+')) or 'BY-SA' in (l['cimke'] or '')
        if sa:
            jel.append('share-alike')
        reszek.append('%s (%s): %s%s' % (l['dataset'], t, l['cimke'], ' [' + ', '.join(jel) + ']' if jel else ''))
    return 'Forrás és licenc: ' + ' · '.join(reszek)


def jelleg_cimkek(jellegek):
    """A jelleg-címkék HTML-je (egy vagy több)."""
    for j in jellegek:
        if j not in JELLEG:
            raise BlokkHiba('ismeretlen jelleg: %s' % j)
    return Markup(' ').join(Markup('<span class="jelleg %s" title="%s">%s</span>') % (JELLEG[j][1], JELLEG[j][2], JELLEG[j][0]) for j in jellegek)


def blokk_html(b, K):
    """A blokk teljes HTML-je. Hibát dob, ha a jelleg- vagy a forrássor hiányozna."""
    forras = forras_sor(b, K.kozos)
    adat = b.fetch(K)
    cimkek = jelleg_cimkek(b.jelleg_fn(adat) if (b.jelleg_fn and adat) else b.jelleg)
    torzs = None
    if adat:
        torzs = b.render(adat, K)
    if not torzs:
        torzs = _ures()
    megj = Markup('<span class="megj">%s</span>') % b.jelleg_megj if b.jelleg_megj else Markup('')
    html = Markup(
        '<section class="blokk" id="b-%s" data-blokk="%s"><h3>%s %s %s</h3>%s<p class="forras">%s</p></section>') % (
            b.id.replace('.', '-'), b.id, b.cim, cimkek, megj, torzs, forras)
    if 'class="jelleg ' not in html or 'class="forras"' not in html:
        raise BlokkHiba('hiányzó jelleg-címke vagy forrássor: %s' % b.id)
    return html


# a szövegoszlop jelölése (Olvasópult, Interlineáris, Munkaasztal): a Károli-szöveg forrásadat, az aláhúzás és a
# szópárok a `token_par` modell-kimenete; a párosítatlan eredeti szavak a `token_karoli`-ból jönnek
SZOVEG_FORRAS = B('szoveg.karoli', 'vers', 'szövegoszlop', 'forras', ('vers',), None, None)
SZOVEG_PAR = B('szoveg.par', 'vers', 'szövegoszlop', 'modell', ('token_par', 'token_karoli'), None, None)


def szoveg_jegy_html(kozos, nezet):
    """Jelleg-címke és forrássor a szövegoszlop fölé; hibát dob, ha a licencsor hiányzik."""
    if nezet == 'interlinearis':
        par = 'A szavak alatti szópárok és a párosítatlan eredeti szavak sora:'
    else:
        par = 'A szavak pontozott aláhúzása (a kattintható szó):'
    return Markup(
        '<div class="szoveg-jegy"><p><b>Károli-szöveg</b> %s<br><span class="forras">%s</span></p>'
        '<p><b>%s</b> Károli–Strong párosítás %s<br><span class="forras">%s</span></p></div>') % (
            jelleg_cimkek(SZOVEG_FORRAS.jelleg), forras_sor(SZOVEG_FORRAS, kozos), par, jelleg_cimkek(SZOVEG_PAR.jelleg), forras_sor(SZOVEG_PAR, kozos))


# a keresés (M3) találatlistáinak jelölése: jelleg-címke, forrás- és licencsor (a regiszterből, mint a blokkoké). A lapon nem blokkként
# jelennek meg, hanem a találatlista fölött; az azonosítójuk a hozzáférési konfigban szintet kaphat (`hozzaferes.toml`, `[blokk]`).
# A (c) mód Strong-ága és a találatok kiemelése a `token_par` párosításán át a `vers.par` blokk láthatóságát követi (kereses.py).
KERESES = {
    'strong': B('kereses.strong', 'kereses', 'Strong-szám', ('forras', 'modell'), ('token_strong', 'vers', 'token_par'), None, None,
                'a versek a TAHOT/TAGNT Strong-címkéiből; a magyar szavak kiemelése a Károli–Strong párosításból (modell-kimenet)'),
    'szo': B('kereses.szo', 'kereses', 'magyar szó', ('gepi', 'modell'),
             ('token_karoli', 'vers', 'szotari_kereso', 'szotari_alak', 'szotari_token_kotojeles', 'token_par'), None, None,
             'a szótokenek gépi bontás; a szótári alak gépi szabály és részben modell-javaslat (DT130 (13)); a Strong-lista és a (c) mód a párosításból (modell-kimenet)'),
    'frazis': B('kereses.frazis', 'kereses', 'magyar frázis', 'gepi', ('token_karoli', 'vers'), None, None,
                'egymást követő szótokenek egy Károli-versen belül'),
    'heber': B('kereses.heber', 'kereses', 'héber frázis', ('gepi', 'modell'), ('token_karoli', 'vers', 'token_par'), None, None,
               'a héber tokenek mássalhangzós alakja (TAHOT); a magyar szavak kiemelése a párosításból (modell-kimenet)'),
}
KERESES_ID = {b.id: b for b in KERESES.values()}


def ismert_azonositok():
    """A hozzáférési konfigban megengedett azonosítók: a blokkok és a keresési módok."""
    return set(BLOKK_ID) | set(KERESES_ID)


def kereses_jegy_html(b, kozos):
    """A találatlista jelleg- és forrássora (a blokkok szabálya: hiányzó licencsor hiba)."""
    html = Markup('<div class="szoveg-jegy"><p><b>Találatlista (%s)</b> %s <span class="megj">%s</span><br><span class="forras">%s</span></p></div>') % (
        b.cim, jelleg_cimkek(b.jelleg), b.jelleg_megj, forras_sor(b, kozos))
    if 'class="jelleg ' not in html or 'class="forras"' not in html:
        raise BlokkHiba('hiányzó jelleg-címke vagy forrássor: %s' % b.id)
    return html
