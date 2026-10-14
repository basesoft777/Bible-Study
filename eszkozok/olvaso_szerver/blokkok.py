"""A blokk-regiszter és a blokkok HTML-je (#76 M2, M0 3.4): a #60 pilot blokk-készlete a `pardes.db`-re átírva.

Minden blokk regiszter-bejegyzés: azonosító, oldal (`vers`, `szo_h`, `szo_g`), cím, **jelleg** (forrásadat / gépi
feldolgozás / modell-kimenet), a táblák (innen jön a licenc- és forrássor, és a kiadási kizárás), az adatlekérő és a
megjelenítő. A jelleg-címke és a forrás+licencsor a regiszterből generálódik (`blokk_html`), így nem maradhat ki;
hiány hibát dob.

Kimenet: a forrásokból jövő szöveg mindenütt escape-elt (`markupsafe`); `Markup` csak a saját, escape-elt elemekből
összeállított töredék. A 9. blokk (angol szavak) két regiszter-bejegyzés (BSB, KJV), mert a KJV-fél GPL miatt
kiadás szerint kimarad; így a regiszterben 40 azonosító áll a pilot 39 blokkjára.
"""
import re
from dataclasses import dataclass
from typing import Callable

from markupsafe import Markup, escape

import adatbazis
import lekerdezesek as q

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


def _r_macula_gorog(d, K):
    sorok = [[_heb(m['szo']), m['gloss'] or '', _gor(m['lxx']), strong_link(K, m['lxx_strong']) if m['lxx_strong'] else ''] for m in d if m['lxx'] or m['lxx_strong']]
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
    return _tabla(['#', 'Angol szó', 'Strong', 'Morf'], [[str(x[0]), x[1] or '', strong_link(K, x[2]) if x[2] else '', x[3] or ''] for x in d])


def _f_kjv(K):
    return q.kjv(K.con, K.ig)


def _f_nave(K):
    return q.nave(K.con, K.ig)


def _r_nave(d, K):
    sorok = [[tema, cimke or '', ig_link(K, hely) if hely else '', 'tartomány (versekre bontva)' if t else 'vers'] for tema, cimke, hely, t, tid in d[:80]]
    ki = _tabla(['Téma', 'Cím', 'Nave-hely', 'Jelleg'], sorok)
    if len(d) > 80:
        ki += Markup('<p class="megj">Összesen %d sor; az első 80 látszik.</p>') % len(d)
    return ki


def _f_tipnr(K):
    return q.tipnr(K.con, K.ig)


def _r_tipnr(d, K):
    return _tabla(['Név', 'Névváltozat', 'Strong', 'Nyelv'], [[n, v or '', strong_link(K, s) if s else '', ny or ''] for n, v, s, ny in d])


def _f_adatreteg(K):
    lx = q.lxx_dontesek(K.con, K.ig)
    kap = q.kapcsolatok(K.con, K.ig)
    mot = q.motivum_elofordulasok(K.con, K.ig)
    return (lx, kap, mot) if (lx or kap or mot) else None


def _r_adatreteg(d, K):
    lx, kap, mot = d
    ki = Markup('')
    if mot:
        ki += Markup('<h4>Motívum-előfordulások</h4>')
        ki += _tabla(['Azonosító', 'Motívum', 'Funkció', 'Strong', 'Károli-szó', 'Megbízhatóság', 'Proveniencia'],
                     [[a, cim or '', fk or '', strong_link(K, st) if st else '', kszo or '', mb or '', pr or ''] for a, ig, fk, st, kszo, mb, pr, cim in mot])
    if kap:
        ki += Markup('<h4>Igehely-kapcsolatok</h4>')
        ki += _tabla(['Forrás', 'Cél', 'Azonosító', 'Típus', 'Funkció', 'Bizonyosság'],
                     [[ig_link(K, a), ig_link(K, b), c, t or '', f or '', bz or ''] for a, b, c, t, f, bz in kap])
    if lx:
        ki += Markup('<h4>LXX-fordítói döntések</h4>')
        ki += _tabla(['Azonosító', 'LXX-hely', 'Héber', 'Görög', 'Típus', 'Megjegyzés', 'Bizonyosság', 'Proveniencia'],
                     [[a, c or '', strong_link(K, hs) if hs else '', Markup('%s %s') % (_gor(gl), strong_link(K, gs) if gs else ''), t or '', mj or '', bz or '', pv or ''] for a, ig, c, hs, gl, gs, t, mj, bz, pv in lx])
    return ki


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
    return ki + _tabla(['Károli-alak', 'Darab'], [[a, str(n)] for a, n in top])


def _bdb_adat(K):
    def f():
        en, hu = q.bdb_angol(K.con, K.strong), q.bdb_magyar(K.con, K.strong)
        alias = None
        if not hu and not en:
            a = q.bdb_alias(K.con, K.strong)
            if a:
                en2, hu2 = q.bdb_angol(K.con, a[0]), q.bdb_magyar(K.con, a[0])
                if hu2 or en2:
                    alias, en, hu = {'tabla_strong': a[0], 'bdb_id': a[1], 'hasonlosag': a[2]}, en2, hu2
        return {'en': en, 'hu': hu, 'alias': alias}
    return K.memo('bdb', f)


def _alias_megj(a):
    return Markup('<p class="megj">A szócikk másik Strong-szám alatt áll (alias, gépi): %s, BDB-azonosító %s, szöveghasonlóság %s.</p>') % (a['tabla_strong'], a['bdb_id'], a['hasonlosag'])


def _f_bdb_angol(K):
    d = _bdb_adat(K)
    return d if d['en'] else None


def _r_bdb_angol(d, K):
    return (_alias_megj(d['alias']) if d['alias'] else Markup('')) + _szoveg(d['en'])


def _f_bdb_magyar(K):
    d = _bdb_adat(K)
    return d if d['hu'] else None


def _r_bdb_magyar(d, K):
    return (_alias_megj(d['alias']) if d['alias'] else Markup('')) + _szoveg(d['hu'])


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
    return Markup('').join(Markup('<h4>%s, %s. jelentés</h4>') % (sz, jsz or '') + _szoveg(fh) for sz, jsz, fh in d)


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
    B('vers.par', 'vers', 'Károli–Strong párosítás', 'modell', ('token_par',), _f_par, _r_par, 'a pontozott aláhúzás a szövegben is modell-kimenet'),
    B('vers.eredeti', 'vers', 'Eredeti szavak (TAHOT / TAGNT)', 'forras', ('token_eredeti',), _f_eredeti, _r_eredeti),
    B('vers.macula_morf', 'vers', 'Igealak-kód és szófaj (Macula)', 'forras', ('token_macula',), _f_macula, _r_macula_morf),
    B('vers.macula_gorog', 'vers', 'Héber–görög párosítás szavanként (Macula)', 'forras', ('token_macula',), _f_macula, _r_macula_gorog),
    B('vers.lxx_szavak', 'vers', 'Görög szóalak és LXX-vers szavai (LXX_OS)', 'forras', ('lxx_token',), _f_lxx_szavak, _r_lxx_szavak),
    B('vers.lxx_versszam', 'vers', 'LXX-versszám', 'forras', ('lxx_versszam',), _f_lxx_versszam, _r_lxx_versszam),
    B('vers.versszamozas', 'vers', 'Versszámozás (MT / KJV)', 'forras', ('vers_szamozas',), _f_versszamozas, _r_versszamozas),
    B('vers.bsb', 'vers', 'Angol szavak szavanként (BSB)', ('forras', 'gepi'), ('bsb',), _f_bsb, _r_angol),
    B('vers.kjv', 'vers', 'Angol szavak szavanként (KJV + Strong)', ('forras', 'gepi'), ('kjv',), _f_kjv, _r_angol, 'a Strong-címkék GPL-eredetűek: nyilvános kiadásból kimarad'),
    B('vers.nave', 'vers', 'Témák (Nave, versekre bontva)', ('forras', 'gepi'), ('nave_vers',), _f_nave, _r_nave),
    B('vers.tipnr', 'vers', 'Tulajdonnevek (TIPNR)', ('forras', 'gepi'), ('tipnr',), _f_tipnr, _r_tipnr),
    B('vers.morf_hu', 'vers', 'Az igealak magyar feloldása', 'gepi', ('morf_kulcs_heber', 'token_macula', 'morf_nyelv_aramai'), _f_morf_hu, _r_morf_hu),
    B('vers.adatreteg', 'vers', 'LXX-döntés, kapcsolat, motívum (adatréteg)', 'forras', ('lxx_dontesek', 'kapcsolatok', 'elofordulasok', 'motivumok'), _f_adatreteg, _r_adatreteg, 'soronként saját proveniencia-mező'),
    B('vers.tsk', 'vers', 'Kereszthivatkozások (TSK)', 'forras', ('tsk',), _f_tsk, _r_tsk),
    B('vers.kh', 'vers', 'Károli-kereszthivatkozások', 'forras', ('kh',), _f_kh, _r_kh),
    B('vers.ubs', 'vers', 'UBS-jelentés az előfordulásra', 'forras', ('ubs_dbh_referenciak', 'ubs_dbh_jelentesek'), _f_ubs, _r_ubs),
    # héber szó-lap
    B('szo.szotar', 'szo_h', 'Strong-szótár', 'forras', ('strong_szotar',), _f_szotar, _r_szotar),
    B('szo.elofordulas', 'szo_h', 'Előfordulás, könyvek száma', 'gepi', ('token_strong',), _f_elofordulas, _r_elofordulas),
    B('szo.karoli_alakok', 'szo_h', 'Károli-alakok és bizonyosság', 'modell', ('token_par',), _f_karoli_alakok, _r_karoli_alakok),
    B('szo.bdb_angol', 'szo_h', 'BDB-szócikk (angol)', 'forras', ('bdb', 'bdb_alias'), _f_bdb_angol, _r_bdb_angol, 'az alias gépi feldolgozás'),
    B('szo.bdb_magyar', 'szo_h', 'BDB-szócikk (magyar fordítás)', 'modell', ('forditasok',), _f_bdb_magyar, _r_bdb_magyar),
    B('szo.lxx_bridge', 'szo_h', 'Görög megfelelő (lxx_bridge)', 'forras', ('lxx_bridge',), _f_lxx_bridge, _r_lxx_bridge),
    B('szo.sdbh', 'szo_h', 'Szemantikai domén (SDBH)', 'forras', ('sdbh_domenek',), _f_sdbh, _r_sdbh, 'üres eredmény nem negatív lelet'),
    B('szo.sece_h', 'szo_h', 'SECE-szócikk (héber)', 'forras', ('sece_h',), _f_sece_h, _r_szoveg),
    B('szo.oshl', 'szo_h', 'OSHL: TWOT- és BDB-azonosító, BDB-helyek', 'forras', ('oshl_lexikalis_index', 'oshl_bdb_igehelyek'), _f_oshl, _r_oshl),
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
    cimkek = jelleg_cimkek(b.jelleg)
    forras = forras_sor(b, K.kozos)
    adat = b.fetch(K)
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
