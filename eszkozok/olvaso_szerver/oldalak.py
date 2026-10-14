"""Lapelőállítás (#76 M2): a lapok HTML-jét előállító függvények; **nem függnek a Flasktól**.

A Flask-réteg (`alkalmazas.py`) csak útvonalat, sütit, fejlécet és gyorsítótárat kezel; a tartalom itt készül, ezért
- a tesztek szerver nélkül is futnak,
- a statikus export később egy paranccsal előállítható (`export.py`: bejárja a `vers` táblát és kiírja a fájlokat).

A lap a kért blokkokat a `hozzaferes.py` szintje és a kiadás szerint szűrve állítja elő: a nem látható blokk függvénye
meg sem hívódik, és nem kerül a HTML-be (nem CSS-sel van elrejtve).
"""
import hashlib
import os
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

import adatbazis
import blokkok
import lekerdezesek as q

SABLON_VERZIO = 'm2-1'
NEZETEK = ('olvaso', 'interlinearis', 'munkaasztal')
NEZET_NEVEK = {'olvaso': 'Olvasópult', 'interlinearis': 'Interlineáris', 'munkaasztal': 'Munkaasztal'}
ALAP_NEZET = 'olvaso'
SABLON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sablonok')


class NemTalalhato(Exception):
    pass


def nezet_ervenyes(n):
    return n if n in NEZETEK else ALAP_NEZET


# ---------------------------------------------------------------------------------------------------------------------
# a kérésen átívelő, állandó adatok (egyszer töltődnek be)
# ---------------------------------------------------------------------------------------------------------------------
class Kozos:
    def __init__(self, con):
        self.konyvek = q.konyvek(con)                                   # [(kk, slug, nev, sorrend)]
        self.slug = {kk: sl for kk, sl, _, _ in self.konyvek}           # kk -> slug
        self.slug_kk = {sl: kk for kk, sl, _, _ in self.konyvek}        # slug -> kk
        if len(self.slug_kk) != len(self.konyvek):
            raise ValueError('a könyvkódok ASCII-sített alakja nem egyedi')
        self.nev = {kk: n for kk, _, n, _ in self.konyvek}
        self.licenc = q.tabla_licencek(con)
        self.share_alike = q.licenc_share_alike(con)
        self.morf_kulcs = q.morf_kulcs(con)
        self.nyelvtani = q.nyelvtani_strongok(con)
        self.meta = q.meta(con)
        self.fejezet_szam = {}
        for kk, _, _, _ in self.konyvek:
            self.fejezet_szam[kk] = q.fejezetek(con, kk)
        h = hashlib.sha256()
        for k, v in con.execute('SELECT kulcs, ertek FROM meta ORDER BY kulcs'):
            h.update(('%s=%s\n' % (k, v)).encode('utf-8'))
        self.adatbazis_kulcs = '%s-%s' % (self.meta.get('epites_ts', ''), h.hexdigest()[:12])

    def aramai_lekerdez(self, con, xml_idk):
        return q.aramai_xml(con, xml_idk) if xml_idk else {}


class Kontekst:
    """Egy lap előállításának környezete: kapcsolat, közös adatok, memo a blokkok közös lekérdezéseihez."""

    def __init__(self, con, kozos, ig=None, strong=None):
        self.con, self.kozos, self.ig, self.strong = con, kozos, ig, strong
        self._memo = {}

    def memo(self, kulcs, f):
        if kulcs not in self._memo:
            self._memo[kulcs] = f()
        return self._memo[kulcs]

    def kozos_szotar(self, strongok):
        return q.rovid_szotar(self.con, list(strongok))


def _ig_kulcs(kozos, slug, fej, vers):
    kk = kozos.slug_kk.get(slug)
    if kk is None:
        raise NemTalalhato('ismeretlen könyv')
    return kk, '%s %d:%d' % (kk, fej, vers)


# ---------------------------------------------------------------------------------------------------------------------
# az oldalgyár
# ---------------------------------------------------------------------------------------------------------------------
class OldalGyar:
    def __init__(self, db, hozzaferes, sablon_dir=SABLON_DIR):
        self.db = db
        self.hozz = hozzaferes
        self.kiadas = db.kiadas
        con = db.kapcsolat()
        self.kozos = Kozos(con)
        self.jinja = Environment(loader=FileSystemLoader(sablon_dir), autoescape=select_autoescape(['html']),
                                 trim_blocks=True, lstrip_blocks=True)
        # a regisztert egyszer ellenőrzi: minden tábla licencsora megvan (hiány indulási hiba)
        for b in blokkok.REGISZTER:
            blokkok.forras_sor(b, self.kozos)

    # -- belső ---------------------------------------------------------------------------------------------------------
    def _blokkok(self, oldal, K, szint):
        ki = []
        for b in blokkok.blokkok_oldalra(oldal):
            if b.kiadas_kizart(self.kiadas):
                continue
            if not self.hozz.lathato(b.id, szint):
                continue
            ki.append(blokkok.blokk_html(b, K))
        return Markup('').join(ki)

    def _render(self, sablon, **ctx):
        ctx.setdefault('nezetek', [(n, NEZET_NEVEK[n]) for n in NEZETEK])
        ctx.setdefault('kiadas', self.kiadas)
        ctx.setdefault('epites_ts', self.kozos.meta.get('epites_ts', ''))
        ctx.setdefault('nezet', ALAP_NEZET)
        return self.jinja.get_template(sablon).render(**ctx)

    def con(self):
        return self.db.kapcsolat()

    # -- töredékek (a `/r/...` útvonalak és a lapok panelei) --------------------------------------------------------------
    def szo_torzs(self, strong, szint):
        """A szó-lap blokkjai (HTML-töredék); NemTalalhato, ha a Strong-szám ismeretlen."""
        s = q.hnorm(strong)
        if not s:
            raise NemTalalhato('érvénytelen Strong-szám')
        con = self.con()
        if not q.strong_van(con, s):
            raise NemTalalhato('ismeretlen Strong-szám')
        K = Kontekst(con, self.kozos, strong=s)
        oldal = 'szo_h' if s[0] == 'H' else 'szo_g'
        sz = q.strong_szotar(con, s)
        if s[0] == 'G':
            tb = q.tbesg(con, s)
            fej = (tb[0], tb[1], tb[2]) if tb else ('', '', '')
        else:
            fej = (sz[0], sz[1], sz[3]) if sz else ('', '', '')
        return s, fej, self._blokkok(oldal, K, szint)

    def szo_fragment(self, strong, szint):
        s, fej, torzs = self.szo_torzs(strong, szint)
        return self.jinja.get_template('_szo_panel.html').render(strong=s, lemma=fej[0], atiras=fej[1], jelentes=fej[2], blokkok=torzs, gorog=s[0] == 'G')

    def vers_fragment(self, slug, fej, vers, szint):
        kk, ig = _ig_kulcs(self.kozos, slug, fej, vers)
        con = self.con()
        if not q.vers_van(con, ig):
            raise NemTalalhato('ismeretlen vers')
        K = Kontekst(con, self.kozos, ig=ig)
        return self.jinja.get_template('_vers_panel.html').render(igehely=ig, blokkok=self._blokkok('vers', K, szint))

    # -- lapok ---------------------------------------------------------------------------------------------------------
    def kezdolap(self, nezet, ut):
        konyvek = []
        for kk, sl, nev, sor in self.kozos.konyvek:
            konyvek.append({'kk': kk, 'slug': sl, 'nev': nev, 'ot': sor < 39, 'fejezetek': [f for f, _ in self.kozos.fejezet_szam[kk]]})
        return self._render('kezdolap.html', konyvek=konyvek, nezet=nezet, ut=ut, cim='Károli-bibliaszöveg')

    def konyv_lap(self, slug, nezet, ut):
        kk = self.kozos.slug_kk.get(slug)
        if kk is None:
            raise NemTalalhato('ismeretlen könyv')
        return self._render('konyv.html', kk=kk, slug=slug, nev=self.kozos.nev[kk], fejezetek=self.kozos.fejezet_szam[kk], nezet=nezet, ut=ut, cim=self.kozos.nev[kk])

    def fejezet_lap(self, slug, fej, vers, nezet, szint, szo, ful, ut):
        kk = self.kozos.slug_kk.get(slug)
        if kk is None:
            raise NemTalalhato('ismeretlen könyv')
        con = self.con()
        fejezetek = dict(self.kozos.fejezet_szam[kk])
        if fej not in fejezetek:
            raise NemTalalhato('ismeretlen fejezet')
        versek = q.fejezet_versek(con, kk, fej)
        if vers is not None and vers not in {v for _, v, _ in versek}:
            raise NemTalalhato('ismeretlen vers')
        szavak = q.fejezet_szavak(con, kk, fej)
        strongok = {st for lista in szavak.values() for _, _, parok in lista for _, _, st, _ in parok}
        szofaj = q.szofajok(con, strongok)
        vlista = []
        for ig, v, szoveg in versek:
            ws = []
            van_par = False
            for sz, szo_, parok in szavak.get(ig, []):
                fo = q.fo_szo(parok, self.kozos.nyelvtani, szofaj)
                van_par = van_par or bool(parok)
                ws.append({'sz': sz, 'szo': szo_, 'fo': fo[0] if fo else None, 'biz': fo[1] if fo else None, 'parok': parok})
            vlista.append({'ig': ig, 'vers': v, 'szoveg': szoveg, 'szavak': ws, 'van_par': van_par})
        parositatlan = q.fejezet_parositatlan(con, kk, fej) if nezet == 'interlinearis' else {}
        for v in vlista:
            v['parositatlan'] = parositatlan.get(v['ig'], [])
        szo_html = vers_html = None
        szo_n = None
        if szo:
            szo_n = q.hnorm(szo)
        if szo_n:
            try:
                szo_html = self.szo_fragment(szo_n, szint)
            except NemTalalhato:
                szo_n, szo_html = None, None
        if vers is not None:
            vers_html = self.vers_fragment(slug, fej, vers, szint)
        if ful not in ('szo', 'vers'):
            ful = 'szo' if (szo_html and not vers_html) else 'vers'
        fl = [f for f, _ in self.kozos.fejezet_szam[kk]]
        elozo = fl[fl.index(fej) - 1] if fl.index(fej) > 0 else None
        kovetkezo = fl[fl.index(fej) + 1] if fl.index(fej) + 1 < len(fl) else None
        return self._render('fejezet.html', kk=kk, slug=slug, nev=self.kozos.nev[kk], fej=fej, vers=vers, versek=vlista, nezet=nezet,
                            szo=szo_n, szo_html=szo_html, vers_html=vers_html, ful=ful, ut=ut, elozo=elozo, kovetkezo=kovetkezo,
                            cim='%s %d' % (self.kozos.nev[kk], fej))

    def szo_lap(self, strong, nezet, szint, ut):
        s, fej, torzs = self.szo_torzs(strong, szint)
        return self._render('szo.html', strong=s, lemma=fej[0], atiras=fej[1], jelentes=fej[2], blokkok=torzs, gorog=s[0] == 'G', nezet=nezet, ut=ut,
                            cim=s)

    def hiba_lap(self, kod, uzenet, nezet, ut):
        return self._render('hiba.html', kod=kod, uzenet=uzenet, nezet=nezet, ut=ut, cim='Hiba')

    # -- az állapot (`/statusz`) ---------------------------------------------------------------------------------------
    def statusz(self):
        con = self.con()
        return {'epites_ts': self.kozos.meta.get('epites_ts', ''), 'meta_hash_sorok': q.meta_hashek_db(con),
                'kiadas': self.kiadas, 'adatbazis_kulcs': self.kozos.adatbazis_kulcs, 'sablon_verzio': SABLON_VERZIO}


# ---------------------------------------------------------------------------------------------------------------------
# a keresődoboz / gyorsugrás értelmezése (M2: csak navigáció; a keresés az M3)
# ---------------------------------------------------------------------------------------------------------------------
def ugras_celpont(kozos, szoveg):
    """`1Móz 1:4`, `1Moz 1:4`, `Zsolt 22` vagy `H216` -> belső útvonal; különben None."""
    t = (szoveg or '').strip()
    if not t or len(t) > 60:
        return None
    s = q.hnorm(t)
    if s:
        return '/szo/' + s
    m = re.match(r'^(.+?)\s+(\d{1,3})(?:\s*[:,.]\s*(\d{1,3}))?$', t)
    nev = m.group(1).strip() if m else t
    mind = {sl.lower(): sl for sl in kozos.slug_kk}
    for kk, sl in kozos.slug.items():
        mind[kk.lower()] = sl
    sl = mind.get(nev.lower().replace(' ', ''))
    if not sl:
        return None
    if not m:
        return '/' + sl
    return '/%s/%d' % (sl, int(m.group(2))) + ('/%d' % int(m.group(3)) if m.group(3) else '')


def biztonsagos_vissza(v):
    """A `vissza` paraméter: csak `/`-rel kezdődő belső út; `//`, `\\`, `:` és vezérlőkarakter nem lehet benne."""
    if not v or not v.startswith('/') or v.startswith('//') or '\\' in v or re.search(r'[\x00-\x1f\x7f]', v):
        return '/'
    elso = v.split('?', 1)[0]
    if ':' in elso:
        return '/'
    return v
