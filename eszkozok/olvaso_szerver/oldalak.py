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
import arculat as arculat_modul
import blokkok
import kereses as kereses_modul
import lekerdezesek as q

SABLON_VERZIO = 'f134-m3k'
# nézetek helyett rétegek (#134, DT294, DT-F134f (b), DT-F134g (c)): egyetlen réteg, az interlineáris sor (`il`); az alap a folyó
# Károli-szöveg réteg nélkül. A réteg-állapot szöveg: a bekapcsolt rétegek vesszővel, a RETEGEK sorrendjében ('' = nincs réteg).
RETEGEK = ('il',)
RETEG_NEVEK = {'il': 'Interlineáris sor'}
ALAP_RETEG = ''
# a régi nézetnevek álnevek (a könyvjelzők és a naplók mérési címei ne törjenek): `?nezet=` és `/nezet/<nev>`
NEZET_ALNEVEK = {'olvaso': '', 'interlinearis': 'il', 'munkaasztal': ''}
# a részletek lapja (#134 M1, DT293): a versmód fülei és a blokkok kiosztása (a mockup 9. változatának FULBLOKK-ja, M0 2.1);
# a ki nem osztott vers-blokk a „Vers” fülre kerül
VERS_FULEK = (('vers', 'Vers'), ('kh', 'Kereszthiv.'), ('temak', 'Témák'), ('motivum', 'Motívum'))
FULBLOKK = {'vers.kh': 'kh', 'vers.tsk': 'kh', 'vers.nave': 'temak', 'vers.tipnr': 'temak', 'vers.motivum': 'motivum', 'vers.kapcsolat': 'motivum'}
# a lap `?ful=` értékei: a szómód, a versmód fülei, és az üres állapot nyitott lapon (kis képernyőn a forrás és a számlálók)
FUL_ERTEKEK = ('szo', 'info') + tuple(k for k, _ in VERS_FULEK)
# a navigáció (#134 M2): a könyvválasztó és a kánon-sáv műfaji csoportjai a kánon sorrendjében (a mockup 9. változatának MUFAJ-a);
# (kód, név, könyvek száma, szín-kód). A szín-kód a kánon-sáv `data-mufaj` attribútuma (a műfajszínek az M3-ban, `--g-*`).
# Csak 66 könyvnél érvényes; más könyvlistánál két csoport: Ószövetség / Újszövetség.
MUFAJOK = (('tor', 'Törvény', 5, 'tor'), ('tort', 'Történeti könyvek', 12, 'tort'), ('bolcs', 'Költői és bölcsességi könyvek', 5, 'bolcs'),
           ('prof', 'Nagypróféták', 5, 'prof'), ('kis', 'Kispróféták', 12, 'kis'), ('ev', 'Evangéliumok és Apostolok Cselekedetei', 5, 'ev'),
           ('pal', 'Pál levelei', 13, 'lev'), ('alt', 'Általános levelek', 8, 'lev'), ('apok', 'Jelenések', 1, 'apok'))
SABLON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sablonok')
SZERVER_DIR = os.path.dirname(os.path.abspath(__file__))
PILOT_DIR = os.path.join(os.path.dirname(SZERVER_DIR), 'olvaso_pilot')


def kod_verzio(gyokerek=None):
    """A kód, a sablonok, a statikus fájlok és a konfiguráció tartalom-hash-e (a lap ETag-jébe és a gyorsítótár kulcsába kerül): kódváltozás után
    a szerver nem adhat 304-et vagy gyorsítótárból régi lapot. `gyokerek`: [(könyvtár, [kiterjesztések])]; alap: a szerver könyvtára
    (.py a tesztek nélkül, .html, .css, .js, .toml, .json — a token-fájl, #98) és a pilot `bdb_szelet.py`-ja (a BDB-bontás ezt hívja).
    A token-fájl futás közbeni változását (#98 M2, mentés) nem ez követi, hanem az `arculat.hash` (a kulcsban külön tag)."""
    h = hashlib.sha256()
    if gyokerek is None:
        gyokerek = [(SZERVER_DIR, ('.py', '.html', '.css', '.js', '.toml', '.json')), (PILOT_DIR, ('bdb_szelet.py',))]
        if os.environ.get('PARDES_KONFIG_DIR'):                      # külső konfiguráció (kiadás, hozzáférési szintek) is a verzió része
            gyokerek.append((os.environ['PARDES_KONFIG_DIR'], ('.toml',)))
    for gyoker, kit in gyokerek:
        for ut, _, nevek in sorted(os.walk(gyoker)):
            if '.venv' in ut or '__pycache__' in ut:
                continue
            for n in sorted(nevek):
                if n.startswith('teszt_') or not (n.endswith(tuple(kit))):
                    continue
                with open(os.path.join(ut, n), 'rb') as f:
                    tartalom = f.read().replace(b'\r\n', b'\n')
                h.update(os.path.relpath(os.path.join(ut, n), gyoker).replace(os.sep, '/').encode('utf-8') + b'\x00' + tartalom + b'\x00')
    return h.hexdigest()[:16]


class NemTalalhato(Exception):
    pass


def reteg_ervenyes(r):
    """A réteg-állapot normalizálása: a bekapcsolt ismert rétegek vesszővel, a RETEGEK sorrendjében; a régi nézetnév álnévként
    (`interlinearis` → `il`, `olvaso`, `munkaasztal` → réteg nélkül). Ismeretlen vagy hibás érték: réteg nélkül."""
    be = set()
    for d in re.split(r'[,\s]+', (r or '')[:60]):
        d = NEZET_ALNEVEK.get(d, d)
        if d in RETEGEK:
            be.add(d)
    return ','.join(x for x in RETEGEK if x in be)


def reteg_be(reteg, nev):
    return nev in (reteg or '').split(',')


def _vers_eleje(szoveg, n=60):
    """A vers eleje a lap fejsorába: legfeljebb `n` karakter, szóhatáron vágva, „…” jellel."""
    s = ' '.join((szoveg or '').split())
    if len(s) <= n:
        return s
    v = s[:n].rsplit(' ', 1)[0]
    return (v or s[:n]).rstrip(',;:') + '…'


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
        self.karoli_strong_konyvek = q.karoli_strong_konyvek(con)       # a Károli–Strong párosítású könyvek (fejléc-számláló, szó-lap jelzés)
        self.meta = q.meta(con)
        self.vers_sorrend = q.vers_sorrendek(con)                      # {igehely: sorrend}: a keresés rendezése (M3)
        self.fejezet_szam = {}
        for kk, _, _, _ in self.konyvek:
            self.fejezet_szam[kk] = q.fejezetek(con, kk)
        h = hashlib.sha256()
        for k, v in q.meta_sorok(con):
            h.update(('%s=%s\n' % (k, v)).encode('utf-8'))
        self.adatbazis_kulcs = '%s-%s' % (self.meta.get('epites_ts', ''), h.hexdigest()[:12])

    def aramai_lekerdez(self, con, xml_idk):
        return q.aramai_xml(con, xml_idk) if xml_idk else {}


class Kontekst:
    """Egy lap előállításának környezete: kapcsolat, közös adatok, memo a blokkok közös lekérdezéseihez."""

    def __init__(self, con, kozos, ig=None, strong=None):
        self.con, self.kozos, self.ig, self.strong = con, kozos, ig, strong
        self._memo = {}
        self.magyar_ok = True        # a magyar BDB (`forditasok`) olvasható-e ezen a lapon (szint és kiadás szerint); a hívó állítja

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
    def __init__(self, db, hozzaferes, sablon_dir=SABLON_DIR, arculat=None):
        self.db = db
        self.hozz = hozzaferes
        # az arculati token-fájl (#98): a lap a token-blokkot a `/arculat.css?v=<hash>` címen linkeli
        self.arculat = arculat or arculat_modul.Arculat.betolt()
        self.kod_verzio = kod_verzio()           # induláskor számolt; a gyorsítótár kulcsában és az ETag-ben
        self.kiadas = db.kiadas
        # a tervező mód (#98 M2): a kapcsoló, a szkript és a stíluslap a lapon; csak a szerver kapcsolja be, a belso kiadásban
        # (alkalmazas.letrehoz); a statikus export és más kiadás lapján nincs nyoma
        self.tervezo = False
        # a lábléc élő állapota (#100, `allapot.LablecFigyelo`): az `alkalmazas.letrehoz` állítja be; a statikus export lapján None (a lábléc ott változatlan)
        self.lablec = None
        con = db.kapcsolat()
        self.kozos = Kozos(con)
        self.jinja = Environment(loader=FileSystemLoader(sablon_dir), autoescape=select_autoescape(['html']),
                                 trim_blocks=True, lstrip_blocks=True)
        # a regisztert egyszer ellenőrzi: minden tábla licencsora megvan (hiány indulási hiba)
        for b in blokkok.REGISZTER + [blokkok.SZOVEG_FORRAS, blokkok.SZOVEG_PAR] + list(blokkok.KERESES.values()):
            blokkok.forras_sor(b, self.kozos)
        # elgépelt blokk-azonosító a hozzáférési konfigban indulási hiba (ne maradjon csendben nyitva); a keresési módok azonosítói is ismertek
        self.hozz.ellenoriz_blokkok(blokkok.ismert_azonositok())
        # a magyar szótokenek nélküli könyvek (a 9 párosítatlan ÚSZ-könyv): a magyar keresés ott nem talál, a keresőlap kiírja
        self.token_nelkuli_konyvek = [kk for kk, sl, _, _ in self.kozos.konyvek if sl not in set(self.kozos.karoli_strong_konyvek)]

    # -- belső ---------------------------------------------------------------------------------------------------------
    def _latszik(self, blokk_id, szint):
        b = blokkok.BLOKK_ID[blokk_id]
        return (not b.kiadas_kizart(self.kiadas) and self.hozz.lathato(b.id, szint)
                and all(self._latszik(k, szint) for k in b.kovet))

    def _blokk_lista(self, oldal, K, szint):
        """[(blokk, html)] a látható blokkokra, a regiszter sorrendjében."""
        ki = []
        for b in blokkok.blokkok_oldalra(oldal):
            if b.kiadas_kizart(self.kiadas):
                continue
            if b.vers_kell and not K.ig:
                continue                                  # vers-kontextus nélkül nincs értelme (pl. „Ebben a versben”)
            if not self.hozz.lathato(b.id, szint) or not all(self._latszik(k, szint) for k in b.kovet):
                continue
            ki.append((b, blokkok.blokk_html(b, K)))
        return ki

    def _blokkok(self, oldal, K, szint):
        return Markup('').join(h for _, h in self._blokk_lista(oldal, K, szint))

    def _render(self, sablon, **ctx):
        ctx.setdefault('kiadas', self.kiadas)
        ctx.setdefault('epites_ts', self.kozos.meta.get('epites_ts', ''))
        ctx['reteg'] = reteg_ervenyes(ctx.get('reteg'))
        ctx['il'] = reteg_be(ctx['reteg'], 'il')
        ctx.setdefault('lap_nyitva', False)
        ctx.setdefault('nav', None)                 # a fejezet-lap navigációja (#134 M2); a többi lapon a fejléc a régi
        ctx.setdefault('arculat_hash', self.arculat.hash)
        ctx.setdefault('lablec', self.lablec.kap() if self.lablec else None)
        ctx['tervezo'] = bool(self.tervezo) and self.kiadas == 'belso'
        if ctx['tervezo']:
            ctx['tervezo_v'] = self.kod_verzio
        sz = ctx.pop('szint', None)
        # a szintváltó vezérlő CSAK a belső kiadásban (próbaüzem): máshol a szint nem választható
        ctx['szint_vezerlo'] = self.kiadas == 'belso'
        if ctx['szint_vezerlo']:
            ctx['szintek'] = self.hozz.szintek
            ctx['szint_nev'] = self.hozz.szint_neve(sz if sz is not None else self.hozz.szint())
        return self.jinja.get_template(sablon).render(**ctx)

    def con(self):
        return self.db.kapcsolat()

    # -- töredékek (a `/r/...` útvonalak és a lapok panelei) --------------------------------------------------------------
    def szo_torzs(self, strong, szint, ig=None):
        """A szó-lap blokkjai (HTML-töredék); NemTalalhato, ha a Strong-szám ismeretlen. `ig`: az igehely, amelyben a szót
        olvassák (az „Ebben a versben” blokk csak vers-kontextussal jelenik meg)."""
        s = q.hnorm(strong)
        if not s:
            raise NemTalalhato('érvénytelen Strong-szám')
        con = self.con()
        if not q.strong_van(con, s):
            raise NemTalalhato('ismeretlen Strong-szám')
        K = Kontekst(con, self.kozos, ig=ig, strong=s)
        K.magyar_ok = self._latszik('szo.bdb_magyar', szint) and self._latszik('szo.bdb_apparatus', szint)
        oldal = 'szo_h' if s[0] == 'H' else 'szo_g'
        sz = q.strong_szotar(con, s)
        alapjel = None
        if s[0] == 'G':
            tb = q.tbesg(con, s) if self._latszik('szo.tbesg', szint) else None
            if tb:
                fej = (tb[0], tb[1], tb[2])
            else:                                                      # tiltott TBESG: a Strong-szótár (szótő, kiejtés, rövid jelentés), ha az látszik
                fej = (sz[0], sz[1], sz[3]) if (sz and self._latszik('szo.szotar', szint)) else ('', '', '')
        else:
            # szótő, kiejtés, szófaj (a Strong-szótár blokk láthatóságát követi, mint a görög ág); az alapjelentés külön sor (DT-F76f)
            fej = (sz[0], sz[1], sz[2]) if (sz and self._latszik('szo.szotar', szint)) else ('', '', '')
            # az alapjelentés is átmegy a blokk-szűrésen (kiadás és hozzáférési szint): tiltott BDB/Strong-szótár esetén nem olvas és nem szivárog
            alapjel = blokkok.alapjelentes(K, K.magyar_ok, self._latszik('szo.szotar', szint))
        return s, fej, self._blokkok(oldal, K, szint), alapjel

    def szo_resz(self, strong, szint, ig=None):
        """A szómód töredéke és a lap fejsora: (html, cím, alcím). A cím a Strong-szám és a héber/görög alak, az alcím az
        alapjelentés (héber szónál), különben a szótár rövid jelentése. Vers-kontextussal (`ig`) a töredék alján „A vers: … →”
        hivatkozás áll: a versmódra vált bezárás nélkül (DT293)."""
        s, fej, torzs, alapjel = self.szo_torzs(strong, szint, ig)
        vers_ut = vers_cim = None
        if ig:
            kk, hely = ig.rsplit(' ', 1)
            f, v = hely.split(':')
            if kk in self.kozos.slug:
                vers_ut, vers_cim = '/%s/%s/%s?ful=vers#v%s' % (self.kozos.slug[kk], f, v, v), ig
        cim = ('%s %s' % (s, fej[0])).strip()
        al = (alapjel or {}).get('szoveg') or fej[2] or ''
        html = self.jinja.get_template('_szo_panel.html').render(strong=s, lemma=fej[0], atiras=fej[1], jelentes=fej[2], alapjel=alapjel, blokkok=torzs,
                                                               gorog=s[0] == 'G', lapcim=cim, lapal=_vers_eleje(al, 90), vers_ut=vers_ut, vers_cim=vers_cim)
        return html, cim, _vers_eleje(al, 90)

    def szo_fragment(self, strong, szint, ig=None):
        return self.szo_resz(strong, szint, ig)[0]

    def vers_resz(self, slug, fej, vers, szint, ful='vers'):
        """A versmód töredéke és a lap fejsora: (html, cím, alcím). A blokkok a fülekre a FULBLOKK szerint oszlanak; a látható
        blokk nélküli fül kimarad (hozzáférési szint, DT129). A cím az igehely, az alcím a vers eleje."""
        kk, ig = _ig_kulcs(self.kozos, slug, fej, vers)
        con = self.con()
        if not q.vers_van(con, ig):
            raise NemTalalhato('ismeretlen vers')
        K = Kontekst(con, self.kozos, ig=ig)
        lista = self._blokk_lista('vers', K, szint)
        fulek = []
        for kod, nev in VERS_FULEK:
            bl = [h for b, h in lista if FULBLOKK.get(b.id, 'vers') == kod]
            if bl:
                fulek.append({'kod': kod, 'nev': nev, 'html': Markup('').join(bl)})
        kodok = [f['kod'] for f in fulek]
        if ful not in kodok:
            ful = kodok[0] if kodok else 'vers'
        eleje = _vers_eleje(q.karoli_szoveg(con, ig) or '') if self._latszik('vers.karoli', szint) else ''
        html = self.jinja.get_template('_vers_panel.html').render(igehely=ig, slug=slug, fej=fej, vers=vers, fulek=fulek, ful=ful, lapcim=ig, lapal=eleje)
        return html, ig, eleje

    def vers_fragment(self, slug, fej, vers, szint, ful='vers'):
        return self.vers_resz(slug, fej, vers, szint, ful)[0]

    # -- lapok ---------------------------------------------------------------------------------------------------------
    def kezdolap(self, reteg, ut, szint=None):
        konyvek = []
        for kk, sl, nev, sor in self.kozos.konyvek:
            konyvek.append({'kk': kk, 'slug': sl, 'nev': nev, 'ot': sor < 39, 'fejezetek': [f for f, _ in self.kozos.fejezet_szam[kk]]})
        return self._render('kezdolap.html', konyvek=konyvek, reteg=reteg, ut=ut, szint=szint, cim='Károli-bibliaszöveg')

    def konyv_lap(self, slug, reteg, ut, szint=None):
        kk = self.kozos.slug_kk.get(slug)
        if kk is None:
            raise NemTalalhato('ismeretlen könyv')
        return self._render('konyv.html', kk=kk, slug=slug, nev=self.kozos.nev[kk], fejezetek=self.kozos.fejezet_szam[kk], reteg=reteg, ut=ut, szint=szint, cim=self.kozos.nev[kk])

    def navigacio(self, kk, fej, elozo, kovetkezo, jeloles):
        """A fejezet-lap navigációja (#134 M2): 900 px alatt a fejezetcímre nyíló navigációs lap, fölötte a fejléc. A könyvválasztó
        (műfaji csoportok, a könyv fejezetei), a kánon-sáv (a könyvek szélessége a fejezetszámukkal arányos, SVG-téglalapok: a CSP
        miatt `style=""` nélkül) és a kereső kliensoldali javaslatának könyvlistája (DT-F134k (b)) ugyanabból a meglévő
        könyvlistából (`Kozos.konyvek`, `Kozos.fejezet_szam`); új adat és új végpont nincs."""
        konyvek = self.kozos.konyvek
        if len(konyvek) == sum(n for _, _, n, _ in MUFAJOK):
            csop, i = [], 0
            for kod, nev, n, szin in MUFAJOK:
                csop.append((kod, nev, szin, konyvek[i:i + n]))
                i += n
        else:
            csop = [('osz', 'Ószövetség', 'osz', [k for k in konyvek if k[3] < 39]), ('usz', 'Újszövetség', 'usz', [k for k in konyvek if k[3] >= 39])]
        mufajok, kanon, x = [], [], 0.0
        for kod, nev, szin, kl in csop:
            sor = []
            for kk_, sl, kn, srd in kl:
                fl = [f for f, _ in self.kozos.fejezet_szam[kk_]]
                # a fejezetrácsot a JS csak folytonos (1..n) fejezetszámozásnál rajzolja helyben; különben a könyv lapja nyílik
                fejszam = len(fl) if fl == list(range(1, len(fl) + 1)) else ''
                sor.append({'kk': kk_, 'slug': sl, 'nev': kn, 'nf': len(fl), 'fejszam': fejszam, 'itt': kk_ == kk})
                if kanon and srd >= 39 and kanon[-1]['srd'] < 39:
                    x += 6                                                # az Ó- és az Újszövetség határa
                w = max(len(fl), 3)
                kanon.append({'kk': kk_, 'slug': sl, 'nev': kn, 'nf': len(fl), 'szin': szin, 'itt': kk_ == kk, 'x': '%g' % x, 'w': '%g' % w, 'srd': srd})
                x += w + 1
            mufajok.append({'kod': kod, 'nev': nev, 'konyvek': sor})
        return {'kk': kk, 'slug': self.kozos.slug[kk], 'nev': self.kozos.nev[kk], 'fej': fej, 'elozo': elozo, 'kovetkezo': kovetkezo,
                'fejezetek': [f for f, _ in self.kozos.fejezet_szam[kk]], 'mufajok': mufajok, 'kanon': kanon, 'kanon_w': '%g' % max(x - 1, 1),
                'jeloles': jeloles}

    def fejezet_lap(self, slug, fej, vers, reteg, szint, szo, ful, ut):
        """A fejezet-lap: a Károli-szöveg (réteg nélkül folyó szöveg, az `il` réteggel versenkénti interlineáris csempék) és a
        részletek lapja (#134 M1). `reteg`: a réteg-állapot (a régi nézetnév is, álnévként). A lap módja: `ful=szo` és ismert
        szó → szómód; vers a címben → versmód (a `ful` a versmód füle); csak szó → szómód; különben üres állapot (útmutató,
        forrás, számlálók; DT-F134l). `ful=info`: üres állapot nyitott lapon (kis képernyőn)."""
        il = reteg_be(reteg_ervenyes(reteg), 'il')
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
            tokenek = szavak.get(ig, [])
            irasjel = q.szovegbe_igazit(szoveg, [t[1] for t in tokenek])      # a szavak írásjellel (a `vers.karoli_szoveg`-ből)
            for (sz, szo_, parok), (kiir, szokoz) in zip(tokenek, irasjel):
                fo = q.fo_szo(parok, self.kozos.nyelvtani, szofaj)
                van_par = van_par or bool(parok)
                ws.append({'sz': sz, 'szo': szo_, 'kiir': kiir, 'szokoz': szokoz, 'fo': fo[0] if fo else None, 'biz': fo[1] if fo else None, 'parok': parok})
            vlista.append({'ig': ig, 'vers': v, 'szoveg': szoveg, 'szavak': ws, 'van_par': van_par})
        # az Interlineáris csempék az eredeti szavak és a párosítás blokkjainak láthatóságát követik (zárt blokknál nem jelennek meg)
        csempe_ok = self._latszik('vers.eredeti', szint) and self._latszik('vers.par', szint)
        parositatlan = q.fejezet_parositatlan(con, kk, fej) if (il and csempe_ok) else {}
        for v in vlista:
            v['parositatlan'] = parositatlan.get(v['ig'], [])
        if il:
            # szócsempék: a magyar szó alatt az eredeti szó, átírás, angol tükörfordítás, Strong (a #60 pilot csempéinek mintájára)
            ered = q.fejezet_eredeti(con, kk, fej) if csempe_ok else {}
            for v in vlista:
                for w in v['szavak']:
                    w['er'] = None if not csempe_ok else [{'szo': erszo, 'st': st, 'gor': st[:1] == 'G', 'at': ered.get((v['ig'], ers), ('', '', ''))[0], 'tukor': ered.get((v['ig'], ers), ('', '', ''))[1],
                                'nyt': st in self.kozos.nyelvtani} for ers, erszo, st, bz in w['parok']]
        ful = ful if ful in FUL_ERTEKEK else ''
        szo_n = q.hnorm(szo) if szo else None
        lap_html, lap_cim, lap_al, mod = None, '', '', 'ures'
        if szo_n and (ful == 'szo' or vers is None):
            try:
                lap_html, lap_cim, lap_al = self.szo_resz(szo_n, szint, ('%s %d:%d' % (kk, fej, vers)) if vers is not None else None)
                mod = 'szo'
            except NemTalalhato:
                szo_n = None
        if mod == 'ures' and vers is not None and ful != 'info':
            lap_html, lap_cim, lap_al = self.vers_resz(slug, fej, vers, szint, ful if ful in dict(VERS_FULEK) else 'vers')
            mod = 'vers'
        vers_ful = ful if (mod == 'vers' and ful in dict(VERS_FULEK)) else 'vers'
        lap_html = Markup(lap_html) if lap_html else None            # a saját sablonunkból, autoescape-pel renderelt töredék
        cimkek = self.cimkek(self.szamlalok([v['ig'] for v in vlista], szint))
        fl = [f for f, _ in self.kozos.fejezet_szam[kk]]
        elozo = fl[fl.index(fej) - 1] if fl.index(fej) > 0 else None
        kovetkezo = fl[fl.index(fej) + 1] if fl.index(fej) + 1 < len(fl) else None
        cim = '%s %d' % (self.kozos.nev[kk], fej)
        return self._render('fejezet.html', kk=kk, slug=slug, nev=self.kozos.nev[kk], fej=fej, vers=vers, versek=vlista, reteg=reteg,
                            szo=szo_n if mod == 'szo' else None, lap_html=lap_html, lap_cim=lap_cim, lap_al=lap_al, mod=mod, vers_ful=vers_ful,
                            lap_nyitva=(mod != 'ures' or ful == 'info'), ures_fo=cim, ures_al='Útmutató, forrás és számlálók',
                            ut=ut, elozo=elozo, kovetkezo=kovetkezo, cimkek=cimkek, nav=self.navigacio(kk, fej, elozo, kovetkezo, not il),
                            szint=szint, cim=cim, szoveg_jegy=blokkok.szoveg_jegy_html(self.kozos, il))

    def szamlalok(self, igehelyek, szint=None):
        """A fejléc-számlálók a versek halmazára (a #60 pilot szabálya): héber szó-lapok (a versek héber szavai, nyelvtani nélkül), görög
        szó-lapok (az LXX-szavak, a Macula-párok és a héber lapok lxx_bridge első három sora), ezek közül a magyar BDB-szócikkel bírók
        (a hiányzót az alias pótolja, mint a lapon), a Károli–Strong párosítású könyvek száma."""
        con = self.con()
        szint = self.hozz.szint() if szint is None else szint
        magyar_ok = self._latszik('szo.bdb_magyar', szint) and self._latszik('szo.bdb_apparatus', szint)
        heber = [s for s in q.heber_strongok_versekre(con, igehelyek) if s not in self.kozos.nyelvtani]
        gorog = set(q.gorog_strongok_versekre(con, igehelyek))
        for ig in igehelyek:                                            # a Macula-párok: csak a TAHOT-szóhoz párosított sorok (a héber csempék szabálya)
            for w in blokkok._heber_csempek(Kontekst(con, self.kozos, ig=ig)):
                if (w.get('macula') or {}).get('lxx_strong'):
                    gorog.add(w['macula']['lxx_strong'])
        hu_db = 0
        for s in heber:
            gorog.update(g for _, g in q.lxx_bridge_h(con, s)[:3])
            if magyar_ok and blokkok._bdb_adat(Kontekst(con, self.kozos, strong=s))['hu']:
                hu_db += 1
        # tiltott magyar BDB (szint vagy kiadás): a számláló nem jelenik meg (None), a tiltott táblát nem olvassuk
        return {'vers': len(igehelyek), 'heber': len(heber), 'gorog': len(gorog), 'bdb_hu': hu_db if magyar_ok else None, 'konyv': len(self.kozos.karoli_strong_konyvek)}

    @staticmethod
    def cimkek(sz):
        """A számlálók címkéi: [(szöveg, arany)]; arany, ha a magyar BDB nem teljes."""
        ki = [('%d vers' % sz['vers'], False), ('%d héber + %d görög szó-lap' % (sz['heber'], sz['gorog']), False)]
        if sz['bdb_hu'] is not None:
            ki.append(('BDB magyarul: %d/%d' % (sz['bdb_hu'], sz['heber']), sz['bdb_hu'] < sz['heber']))
        return ki + [('Károli–Strong: %d könyv' % sz['konyv'], False)]

    def szo_lap(self, strong, reteg, szint, ut):
        s, fej, torzs, alapjel = self.szo_torzs(strong, szint)
        return self._render('szo.html', strong=s, lemma=fej[0], atiras=fej[1], jelentes=fej[2], alapjel=alapjel, blokkok=torzs, gorog=s[0] == 'G', reteg=reteg, ut=ut, szint=szint,
                            cim=s)

    # -- keresés (M3) ----------------------------------------------------------------------------------------------------
    def kereses_lap(self, kerdes, reteg, szint, ut, hiba=None, urlap=None):
        """A keresőlap: űrlap, és ha van `kerdes` (kereses.Kerdes), a találatlista lapozva. `hiba`: érvénytelen bemenet üzenete;
        `urlap`: az űrlap kitöltése ({'q', 'tipus', 'mod'}). A keresési mód a hozzáférési szint szerint zárható (a `kereses.*`
        azonosító, `hozzaferes.toml`): zárt módban a lekérdezés nem fut."""
        szint = self.hozz.szint() if szint is None else szint
        ctx = dict(reteg=reteg, ut=ut, szint=szint, cim='Keresés', hiba=hiba, tipusok=list(kereses_modul.TIPUS_NEVEK.items()),
                   modok=list(kereses_modul.MOD_NEVEK.items()), token_nelkuli=self.token_nelkuli_konyvek, urlap=urlap or {}, k=None)
        if kerdes is None:
            return self._render('kereses.html', **ctx)
        b = blokkok.KERESES[kerdes.tipus]
        ctx.update(k=kerdes, tipus_nev=kereses_modul.TIPUS_NEVEK[kerdes.tipus], mod_nev=kereses_modul.MOD_NEVEK.get(kerdes.mod), cim='Keresés: %s' % kerdes.szoveg)
        if not self.hozz.lathato(b.id, szint):
            ctx['zart'] = True
            return self._render('kereses.html', **ctx)
        con = self.con()
        par_ok = self._latszik('vers.par', szint)
        t = kereses_modul.keres(con, kerdes, self.kozos.vers_sorrend, par_lathato=par_ok)
        oldal, kov = kereses_modul.lap(t, kerdes.tol)
        ctx.update(t=t, sorok=kereses_modul.lap_sorai(con, self.kozos, t, oldal, kerdes, par_lathato=par_ok), jegy=blokkok.kereses_jegy_html(b, self.kozos),
                   kovetkezo_url=kereses_modul.kereses_url(kerdes, kov) if kov is not None else None,
                   elso_url=kereses_modul.kereses_url(kerdes) if kerdes.tol >= 0 else None,
                   sorszam_tol=sum(1 for v in t.versek if v[0] <= kerdes.tol) + 1, par_ok=par_ok,
                   mod_url={m: kereses_modul.kereses_url(kereses_modul.Kerdes(kerdes.tipus, kerdes.szoveg, kerdes.szavak, m)) for m in kereses_modul.MODOK})
        return self._render('kereses.html', **ctx)

    def hiba_lap(self, kod, uzenet, reteg, ut, szint=None):
        return self._render('hiba.html', kod=kod, uzenet=uzenet, reteg=reteg, ut=ut, szint=szint, cim='Hiba')

    # -- az állapot (`/statusz`) ---------------------------------------------------------------------------------------
    def statusz(self):
        con = self.con()
        return {'epites_ts': self.kozos.meta.get('epites_ts', ''), 'meta_hash_sorok': q.meta_hashek_db(con),
                'kiadas': self.kiadas, 'adatbazis_kulcs': self.kozos.adatbazis_kulcs, 'sablon_verzio': SABLON_VERZIO, 'kod_verzio': self.kod_verzio, 'arculat_hash': self.arculat.hash}


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
