"""A Kolofon (S8d; DT-F218y).

A HAMART-001 mai lapjával való egyezést (az engedélysorokkal) a regresszió méri; itt független számlálással: a
forrástábla sorai pontosan a számozott szakaszok olvasásai a jegyzék `irodalom` oszlopa szerint (GK-07, DT901), a
származtatott tábla CC BY-os bemenetei saját soron (F212); a licencszöveg és a kötelező megjelölés a licencleltárból;
a „Negatív kritérium” sor hivatkozás a lap elejére (DT874, 9. tétel); a jóváhagyás-mondat munka módban a korábbi
változatot mondja, kiadás módban a kapu a jóváhagyás frissességét méri (GK-27, T9, N221: egyező `lap_commit`;
csak generált változás; kézi próza vagy adat változása → BUKÁS); a közel-keleti és a Chain Lineage-mondat az állapotból jön
(GK-28); a licenckapu (N223, D14): a lap adatát adó minden kötelező megjelölésű forrás minden megjelölés-mondata a
Kolofonban, és minden forrás neve a forrástáblában, a tisztázatlan licencű a licencállapot mondatával. A táblákat a teszt maga olvassa (`split('\t')`), nem a generátor kódjával.
"""
import dataclasses
import datetime
import os
import unittest

import kozos
from lapgen import bemenet, fo, konfig
from lapgen.bemenet import alap as alap_be
from lapgen.bemenet import irodalom as irodalom_be
from lapgen.bemenet import jovahagyas as jovahagyas_be
from lapgen.bemenet import kolofon as kolofon_be
from lapgen.bemenet.jegyzek import BemenetHiba, JegyzekSor
from lapgen.ertekek import IrodLicenc
from lapgen.megjelenites.md import kolofon as MD
from lapgen.megjelenites.md.iro import Lapiro, lap_szoveg
from lapgen.szamitas import kolofon as SZ
from lapgen.szoveg import MotivumId, SablonHiba, SablonSor, kiiras, sablon

HAMART, ISTENTISZT = 'HAMART-001', 'ISTENTISZT-001'
DATUM = datetime.date(2026, 11, 13)


def kiir(lathato):
    return kiiras(lathato).szoveg


def _tabla(rel):
    with open(os.path.join(kozos.GYOKER, *rel.split('/')), encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def _nevek(tipus):
    return {s['kulcs']: s['olvasoi_nev'] for s in _tabla('adat/olvasoi_nevtabla.tsv') if s['tipus'] == tipus}


class _Korny:
    def __init__(self, azonosito, mod=fo.Mod.MUNKA):
        self.b, self.motivum, self.mod = bemenet.Bemenet(kozos.GYOKER), MotivumId(azonosito), mod


def _elozo(korny):
    """A számozott szakaszok (és alrészeik) olvasásai, ahogy a `fo.lap_keszit` a gyűjtő szakasznak átadja."""
    elozo = {}
    for leiro in fo.szakaszrend().mind():
        if leiro.szamit is None or leiro.gyujto or leiro.nezet != konfig.NEZET_TUDOMANYOS:
            continue
        with korny.b.figyel() as f:
            leiro.szamit(korny)
        if leiro.szamozott or leiro.alresz:
            elozo[leiro.azonosito] = frozenset(f)
    return elozo


def _lap(korny, modell, datum=DATUM):
    b = korny.b
    keret = fo.Keret(bemenet.nyelv(b), korny.motivum, fo.szakaszrend(), 'ts=2026-11-13', korny.mod, b, datum)
    iro = Lapiro()
    MD.megjelenit(iro, modell, keret, fo._forrasok(b, bemenet.b01_licencek(b), frozenset()))
    return lap_szoveg(iro.kesz())


class _Alap(unittest.TestCase):
    AZONOSITO = HAMART
    _cache = {}

    @classmethod
    def setUpClass(cls):
        if cls.AZONOSITO not in _Alap._cache:
            korny = _Korny(cls.AZONOSITO)
            elozo = _elozo(korny)
            _Alap._cache[cls.AZONOSITO] = (korny, elozo, SZ.szamit(korny, elozo))
        cls.korny, cls.elozo, cls.modell = _Alap._cache[cls.AZONOSITO]
        cls.unio = frozenset().union(*cls.elozo.values())
        cls.lap = _lap(cls.korny, cls.modell)


class Forrastabla(_Alap):
    def test_gk07_a_sorok_az_olvasasokbol(self):
        """GK-07 (DT901): a forrástábla nevei pontosan a számozott szakaszok olvasott bemeneteinek fájlnevei (a jegyzék
        `irodalom` oszlopa szerint), a származtatott tábla bemenetei (F212) és a külső források."""
        jegyzek = {s['id']: s for s in _tabla('adat/lapgen_bemenetek.tsv')}
        szotar, kolofon, adat, kulso = (_nevek('irod_szotar'), _nevek('kolofon_szotar'), _nevek('irod_adat'),
                                        _nevek('irod_kulso'))

        def nevek(b_idk):
            ki = set()
            for b_id in b_idk:
                if jegyzek[b_id]['irodalom'] == '-':
                    continue
                for u in (x.strip() for x in jegyzek[b_id]['utvonal'].split(';')):
                    ki.add(kolofon[u] if u in szotar else adat[u])
            return ki
        vart = nevek(self.unio)
        for b_id, (jegyzekbeli, kulsok) in konfig.KOLOFON_SZARMAZTATOTT.items():
            if b_id in self.unio:
                vart |= nevek(jegyzekbeli) | {kulso[k] for k in kulsok}
        kapott = {s.nev.ertek: s for s in self.modell.forrasok}
        kapott_nevek = {_nevek(s.nev_tipus.value)[k] for k, s in kapott.items()}
        self.assertTrue(vart <= kapott_nevek, vart - kapott_nevek)
        self.assertTrue(kapott_nevek - vart <= set(kulso.values()), kapott_nevek - vart)
        # a MACULA (a BDB verstáblájának bemenete) saját soron áll (F212)
        self.assertIn(kulso['macula_heber'], kapott_nevek)

    def test_a_szakaszok_az_olvaso_szakaszok(self):
        """A „Szakasz” oszlop pontosan azok a szakaszok, amelyek a sor bemenetét olvasták (alrésznél a szülő)."""
        motivumtabla = [s for s in self.modell.forrasok if s.nev.ertek == 'adat/motivumok.tsv']
        self.assertEqual(len(motivumtabla), 1)
        rend = fo.szakaszrend()
        vart = {rend.sorszam(rend.szulo(a)) for a, olv in self.elozo.items() if 'B02' in olv}
        self.assertEqual(set(motivumtabla[0].szakaszok), vart)
        self.assertEqual(list(motivumtabla[0].szakaszok), sorted(vart))
        self.assertIn('3. Kizárt', self.lap)   # a 3. szakasz (S9a) is olvas: a szakaszlistákban áll

    def test_licenc_csak_a_licencleltarbol(self):
        """GK-07: a `licenc` alakú licenc a licencleltár címkéje szó szerint."""
        cimkek = {s['cimke'] for s in _tabla('adat/licencek.tsv')}
        for sor in self.modell.forrasok:
            for lic in sor.licencek:
                if lic.alak is IrodLicenc.LICENC:
                    self.assertIn(kiir(lic.cimke), cimkek)
        # a közlés DOI-ja a kiadási adatok egyetlen helyéről (a névtábla `kiadasi_adat` típusa, DT-F218y 1.)
        doi = _nevek('kiadasi_adat')['karoli_strong_doi']
        self.assertTrue(any(s.startswith('| Károli–Strong párosítás | CC BY 4.0, https://doi.org/%s |' % doi)
                            for s in self.lap.split('\n')))


class Megjeloles(_Alap):
    def test_a_megjelolesek_a_licencleltarbol(self):
        """A megjelölendő források a `konfig.KOLOFON_MEGJELOLES` kulcsai közül azok, amelyek a lapra adatot adnak (a
        bemenetet a lap olvasta, vagy külső forrásként áll; D14); a nem saját mondatú megjelölés a licencleltár `kotelezo_megjeloles` mezőjének mondata, szó szerint."""
        jegyzek = {s['id']: s for s in _tabla('adat/lapgen_bemenetek.tsv')}
        olvasott = {jegyzek[b]['licenc_kulcs'] for b in self.unio}
        # a több forrású bemenet társai és a külső források (D14: a MACULA, a Sefaria) is adatot adnak a lapra
        olvasott.update(*(t for b, t in konfig.LICENC_TARS.items() if b in self.unio))
        olvasott.update(konfig.IROD_KULSO_LICENC.values())
        mezo = {s['dataset']: s['kotelezo_megjeloles'] for s in _tabla('adat/licencek.tsv')}
        vart_sablon = [s for k, s in konfig.KOLOFON_MEGJELOLES if k in olvasott and s is not None]
        self.assertEqual([m.sablon.value for m in self.modell.megjelolesek if m.sablon], vart_sablon)
        for m in self.modell.megjelolesek:
            if m.sablon is None:
                self.assertTrue(any(m.szoveg is not None and kiir(m.szoveg) in mezo[k]
                                    for k, s in konfig.KOLOFON_MEGJELOLES if k in olvasott and s is None))
        self.assertNotIn('Mounce', self.lap)   # az új generátor a Mounce-szótárt nem olvassa
        self.assertIn('*LSJ forrás: Liddell-Scott-Jones', self.lap)


class Kriterium(_Alap):
    def test_ism_a_kolofon_nem_ismetli_a_kriteriumot(self):
        """DT-F218n, DT874 9. tétel: a „Negatív kritérium” sor a lap elejére hivatkozik, a kritériumot nem ismétli."""
        krit = [s['negativ_kriterium'] for s in _tabla('adat/motivumok.tsv') if s['id'] == HAMART][0]
        self.assertNotIn(krit[:60], self.lap)
        self.assertIn('| Negatív kritérium | a lap elején áll ([Mi tartozik ide, és mi nem](#mi-tartozik-ide)) |',
                      self.lap)


class Jovahagyas(_Alap):
    def test_gk27_munka_modban_a_korabbi_valtozat(self):
        """GK-27 (T9): munka módban a szerző a lap korábbi változatát hagyta jóvá, a legutóbbi átnézés (híján a
        legutóbbi kiadás) dátumával."""
        kiadasok = sorted((s for s in _tabla('adat/kiadasok.tsv') if s['id'] == HAMART), key=lambda s: int(s['kiadas']))
        atnezes = sorted(s['datum'] for s in _tabla('adat/lap_atnezesek.tsv')
                         if s['id'] == HAMART and s['ki'] == 'felhasználó')
        datum = (atnezes or [kiadasok[-1]['datum']])[-1]
        self.assertIn('; a szerző a lap korábbi változatát hagyta jóvá (%s). A többi szakasz' % datum, self.lap)
        self.assertNotIn('a szerző jóváhagyta', self.lap)
        self.assertIs(SZ.kapu(self.modell), self.modell)

    def test_gk27_kiadas_mod_kapuja(self):
        """GK-27 (T9, N221): kiadás módban a kézi résű lap csak kiadható frissességgel megy át; mérés nélkül,
        átnézés nélkül, a lap nélkül és elavult jóváhagyással BUKÁS; a generált lapnak nincs mit jóváhagyni."""
        F, J = jovahagyas_be.Frissesseg, jovahagyas_be.Jovahagyas
        with self.assertRaises(BemenetHiba):
            SZ.kapu(dataclasses.replace(self.modell, kiadas=True))
        for allapot in (F.NINCS_LAP, F.NINCS_ATNEZES, F.ELAVULT):
            with self.assertRaises(BemenetHiba, msg=allapot):
                SZ.kapu(dataclasses.replace(self.modell, kiadas=True,
                                            frissesseg=J(allapot, 'a' * 40, '2026.11.04', 'b' * 40)))
        for allapot in (F.FRISS, F.CSAK_GENERALT):
            m = dataclasses.replace(self.modell, kiadas=True, frissesseg=J(allapot, 'a' * 40, '2026.11.04', 'b' * 40))
            self.assertIs(SZ.kapu(m), m)
        generalt = dataclasses.replace(self.modell, kiadas=True, szerzoseg=SZ.Szerzoseg.GENERALT, resek=())
        self.assertIs(SZ.kapu(generalt), generalt)

    def test_gk27_kiadas_modban_a_mondat_friss(self):
        """T9: kiadás módban (a kapu után) a mondat „a szerző jóváhagyta”, a korábbi változat említése nélkül."""
        m = dataclasses.replace(self.modell, kiadas=True, frissesseg=jovahagyas_be.Jovahagyas(
            jovahagyas_be.Frissesseg.FRISS, 'a' * 40, '2026.11.04', 'a' * 40))
        lap = _lap(self.korny, m)
        self.assertIn('; a szerző jóváhagyta. A többi szakasz', lap)
        self.assertNotIn('korábbi változatát', lap)


    def test_kiadasi_adatok(self):
        adatok = kolofon_be.b48_kiadasi_adatok(self.korny.b, self.korny.motivum)
        kiadasok = [s for s in _tabla('adat/kiadasok.tsv') if s['id'] == HAMART]
        self.assertEqual([k.szam for k in adatok.kiadasok], sorted(int(s['kiadas']) for s in kiadasok))
        javitasok = {s['datum'] for s in _tabla('adat/lap_javitasok.tsv')
                     if s['id'] == HAMART and s['jovahagyta'] == 'felhasználó' and s['datum']}
        self.assertEqual([d.strftime('%Y.%m.%d') for d in adatok.javitasok], sorted(javitasok))
        self.assertIn('vetette el (2026.11.11–13) |', self.lap)   # a dátumok tartománya (azonos hónap)
        self.assertIn('| Kiadás | %d |' % adatok.kiadasok[-1].szam, self.lap)


class _HamisGit:
    """A `bemenet.jovahagyas.Git` helyett: a lap utolsó commitja rögzített, minden commit létezik és őse a HEAD-nek, a
    commitbeli tartalom a munkafáé, kivéve a `mas` szerinti fájlokat ({útvonal: szöveg})."""

    def __init__(self, utolso, mas=None):
        self.utolso, self.mas = utolso, dict(mas or {})

    def utolso_commit(self, _utvonal):
        return self.utolso

    def teljes(self, commit):
        return commit

    def ose_a_headnek(self, _commit):
        return True

    def tartalom(self, _commit, utvonal):
        if utvonal in self.mas:
            return self.mas[utvonal]
        teljes = os.path.join(kozos.GYOKER, *utvonal.split('/'))
        if not os.path.exists(teljes):
            return None
        with open(teljes, encoding='utf-8') as f:
            return f.read().replace('\r\n', '\n')


class Frissesseg(unittest.TestCase):
    """GK-27 (T9, N221, DT933 (1)) a frissesség három ágán, az ISTENTISZT-001 mai átnézés-sorával
    (`lap_atnezesek.tsv`; a teszt maga olvassa) és hamis git-olvasóval."""

    @classmethod
    def setUpClass(cls):
        cls.b, cls.motivum = bemenet.Bemenet(kozos.GYOKER), MotivumId(ISTENTISZT)
        sorok = [s for s in _tabla('adat/lap_atnezesek.tsv')
                 if s['id'] == ISTENTISZT and s['ki'] == 'felhasználó' and s['idezet'].strip()]
        cls.atnezes = sorok[-1]['lap_commit']

    def _f(self, git):
        return jovahagyas_be.frissesseg(self.b, self.motivum, git=git)

    def test_egyezo_lap_commit(self):
        j = self._f(_HamisGit(self.atnezes))
        self.assertIs(j.allapot, jovahagyas_be.Frissesseg.FRISS)
        self.assertTrue(j.kiadhato)

    def test_egyezo_lap_commit_de_valtozott_kezi_proza(self):
        """A lap még a jóváhagyott (egyező `lap_commit`), de a kézi próza azóta változott: elavult, nem friss (A1
        független ellenőrzés; DT933 (1))."""
        ut = 'motivumok/%s.md' % ISTENTISZT
        with open(os.path.join(kozos.GYOKER, *ut.split('/')), encoding='utf-8') as f:
            regi = f.read().replace('\r\n', '\n') + '\nRégi mondat.\n'
        j = self._f(_HamisGit(self.atnezes, {ut: regi}))
        self.assertIs(j.allapot, jovahagyas_be.Frissesseg.ELAVULT)
        self.assertFalse(j.kiadhato)

    def test_csak_generalt_valtozas(self):
        """A lap azóta változott, a kézi bemenetek nem: változásjegyzék-sor, új nézés nem."""
        j = self._f(_HamisGit('f' * 40))
        self.assertIs(j.allapot, jovahagyas_be.Frissesseg.CSAK_GENERALT)
        self.assertTrue(j.kiadhato)
        self.assertEqual(j.atnezes_commit, self.atnezes)

    def test_a_kozos_adat_mas_motivumanak_valtozasa_csak_generalt(self):
        """A közös tábla más motívumra eső sora nem a jóváhagyás tárgya."""
        with open(os.path.join(kozos.GYOKER, 'adat', 'jeloltek.tsv'), encoding='utf-8') as f:
            jeloltek = f.read().replace('\r\n', '\n')
        adatsorok = [s for s in jeloltek.split('\n') if s and not s.startswith('#')][1:]   # a fejléc nélkül
        sor = next(s for s in adatsorok if ISTENTISZT not in s.split('\t'))
        mas = jeloltek.replace(sor + '\n', '', 1)
        j = self._f(_HamisGit('f' * 40, {'adat/jeloltek.tsv': mas}))
        self.assertIs(j.allapot, jovahagyas_be.Frissesseg.CSAK_GENERALT)

    def test_kezi_proza_valtozasa(self):
        ut = 'motivumok/%s.md' % ISTENTISZT
        with open(os.path.join(kozos.GYOKER, *ut.split('/')), encoding='utf-8') as f:
            regi = f.read().replace('\r\n', '\n') + '\nRégi mondat.\n'
        j = self._f(_HamisGit('f' * 40, {ut: regi}))
        self.assertIs(j.allapot, jovahagyas_be.Frissesseg.ELAVULT)
        self.assertFalse(j.kiadhato)

    def test_adat_valtozasa(self):
        with open(os.path.join(kozos.GYOKER, 'adat', 'kapcsolatok.tsv'), encoding='utf-8') as f:
            kapcs = f.read().replace('\r\n', '\n')
        sor = next(s for s in kapcs.split('\n') if ISTENTISZT in s.split('\t'))
        j = self._f(_HamisGit('f' * 40, {'adat/kapcsolatok.tsv': kapcs.replace(sor, sor + 'x', 1)}))
        self.assertIs(j.allapot, jovahagyas_be.Frissesseg.ELAVULT)

    def test_nincs_lap_es_nincs_atnezes(self):
        self.assertIs(self._f(_HamisGit(None)).allapot, jovahagyas_be.Frissesseg.NINCS_LAP)
        j = jovahagyas_be.frissesseg(self.b, MotivumId(HAMART), git=_HamisGit('f' * 40))
        self.assertIs(j.allapot, jovahagyas_be.Frissesseg.NINCS_ATNEZES)

    def test_valodi_git(self):
        """A valódi olvasó: a lap utolsó commitja teljes hash, a commitbeli tartalom olvasható."""
        git = jovahagyas_be.Git(kozos.GYOKER)
        utolso = git.utolso_commit(jovahagyas_be.lap_utvonal(MotivumId(ISTENTISZT)))
        self.assertRegex(utolso, r'^[0-9a-f]{40}$')
        self.assertEqual(git.teljes(utolso[:12]), utolso)
        self.assertTrue(git.ose_a_headnek(utolso))
        self.assertIsNotNone(git.tartalom(utolso, jovahagyas_be.lap_utvonal(MotivumId(ISTENTISZT))))
        self.assertIsNone(git.teljes('0' * 40))


class Allapotmondat(_Alap):
    def test_gk28_kozel_keleti_csak_nem_vizsgalt_allapotban(self):
        """GK-28: a közel-keleti mondat csak „nem vizsgált” rétegállapotnál áll; más állapotnál a Kolofon megáll."""
        self.assertIn('összehasonlító réteg a munkában nincs', self.lap)
        b = bemenet.Bemenet(kozos.GYOKER)
        sor = b.jegyzek_sor('B75')
        b._jegyzek['B75'] = JegyzekSor(**dict({k: getattr(sor, k) for k in sor.__slots__}, allapot='aktiv'))
        with self.assertRaises(BemenetHiba):
            kolofon_be.b75_kozel_keleti_reteg(b)

    def test_gk28_chain_lineage_a_licencleltar_allapotabol(self):
        """GK-28: a Chain Lineage licencmondata a licencleltár állapotából (`tisztazatlan`) jön; tisztázott
        állapotnál a címke áll."""
        b = bemenet.Bemenet(kozos.GYOKER)
        k = {x.kulcs.ertek: x for x in irodalom_be.kulso_forrasok(b, MotivumId(HAMART), {'B39'})}
        self.assertIs(k['chain_lineage'].licenc, IrodLicenc.CHAIN_LINEAGE)
        eredeti = irodalom_be.b01_licencek

        def hamis(bb):
            lic = eredeti(bb)
            allapotok = dict(lic._allapotok, Chain_Lineage_Browser='tisztazott')
            return alap_be.Licencek(bb, lic._cimkek, allapotok, lic._megjelolesek)
        irodalom_be.b01_licencek = hamis
        try:
            k = {x.kulcs.ertek: x for x in irodalom_be.kulso_forrasok(b, MotivumId(HAMART), {'B39'})}
        finally:
            irodalom_be.b01_licencek = eredeti
        self.assertIs(k['chain_lineage'].licenc, IrodLicenc.LICENC)
        self.assertIsNotNone(k['chain_lineage'].cimke)


class Licenckapu(_Alap):
    """N223 (F241.4, D14): minden licencleltár-forrás, amelynek adata a lapra kerül és `kotelezo_megjeloles`-e nem üres,
    megjelölés-mondataival a Kolofonban áll (a saját mondatával, vagy a mező minden mondata idézetként); minden forrás
    neve a forrástáblában, a tisztázatlan licencű a licencállapot mondatával (GK-28)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.meres = SZ.licenc_meres(cls.korny, cls.elozo)

    def _mas(self, **csere):
        return dict(self.meres, **csere)

    def test_n223_a_merce_a_lapon_allo_forrasokbol(self):
        """A mérce forrásai a táblákból, független számlálással: a számozott szakaszok olvasott, forráslistára kerülő
        bemeneteinek licenckulcsa (a több forrású bemenet társaival), a MACULA (a B19 bemenete) és a tanúk külső
        forrásai."""
        jegyzek = {s['id']: s for s in _tabla('adat/lapgen_bemenetek.tsv')}
        mezo = {s['dataset']: s['kotelezo_megjeloles'] for s in _tabla('adat/licencek.tsv')}
        olvasott = {jegyzek[b]['licenc_kulcs'] for b in self.unio if jegyzek[b]['irodalom'] != '-'} - {'-'}
        for b_id, tarsak in konfig.LICENC_TARS.items():
            if b_id in self.unio:
                olvasott.update(tarsak)
        self.assertTrue(olvasott <= set(self.meres['lapon_allo']), olvasott - set(self.meres['lapon_allo']))
        vart = {k for k in olvasott if mezo.get(k)}
        self.assertTrue(vart <= set(self.meres['kotelezo']), vart - set(self.meres['kotelezo']))
        self.assertIn('Macula_heber', self.meres['kotelezo'])            # a származtatott tábla bemenete (F212)
        self.assertIn('Tanu_rabbinikus_index', self.meres['kotelezo'])   # a tanúk külső forrása (Sefaria)
        self.assertNotIn('BDB', self.meres['kotelezo'])                  # üres megjelölésű forrás nem tárgya

    def test_n223_a_lap_minden_kotelezo_megjelolest_hordoz(self):
        """A lap minden kötelező megjelölést hordoz: a kapu nem talál hiányt, és a mondatok a lapon állnak."""
        self.assertEqual(SZ.licenc_hianyok(self.meres), [])
        self.assertEqual(self.modell.licenc_hiany, ())
        self.assertIs(SZ.kapu(self.modell), self.modell)
        for kulcs, mondatok in self.meres['kotelezo'].items():
            if kulcs not in self.meres['sablonos']:
                for mondat in mondatok:
                    self.assertIn(mondat, self.lap, kulcs)

    def test_n223_hiany_bukas(self):
        """Ha egy kötelező megjelölés hiányzik, a hiány a forrást nevezi meg, és a kapu megáll; a saját mondatú forrás
        (LSJ) a sablonjával megjelölt."""
        hianyok = SZ.licenc_hianyok(self._mas(idezett=set()))
        self.assertIn('TAHOT', hianyok)
        self.assertIn('TBESH', hianyok)
        self.assertNotIn('LSJ', hianyok)
        hianyos = dataclasses.replace(self.modell, licenc_hiany=(self.korny.b.kulcs('B01', 'dataset', 'TAHOT'),))
        with self.assertRaises(BemenetHiba) as h:
            SZ.kapu(hianyos)
        self.assertIn('licenckapu', str(h.exception))
        self.assertIn('TAHOT', str(h.exception))

    def test_d14_a_forras_neve_a_kolofonban(self):
        """D14 (c): a lap adatát adó minden forrást a forrástábla megnevez; a tisztázatlan licencű forrást (Chain
        Lineage) a licencállapot mondatával (GK-28), és a mondat-kapu nem méri (a mezője leírás, nem előírt szöveg)."""
        self.assertIs(self.meres['lapon_allo']['Chain_Lineage_Browser'], True)
        self.assertNotIn('Chain_Lineage_Browser', self.meres['kotelezo'])
        self.assertIn(IrodLicenc.CHAIN_LINEAGE, self.meres['fedett']['Chain_Lineage_Browser'])
        nevtelen = {k: a for k, a in self.meres['fedett'].items() if k != 'TSK'}
        self.assertEqual(SZ.licenc_hianyok(self._mas(fedett=nevtelen)), ['TSK'])
        cimkes = dict(self.meres['fedett'], Chain_Lineage_Browser={IrodLicenc.LICENC})
        self.assertEqual(SZ.licenc_hianyok(self._mas(fedett=cimkes)), ['Chain_Lineage_Browser'])

    def test_n223_mondathatar(self):
        """A mező mondatokra bontása a „.; ” és a „); ” határon (a STEPBible-mondat zárójeles licenccel végződik):
        a TBESH első mondata azonos a TAHOT megjelölésével, így a lapon egyszer áll."""
        lic = alap_be.b01_licencek(bemenet.Bemenet(kozos.GYOKER))
        tahot, tbesh = lic.megjeloles_mondatok('TAHOT'), lic.megjeloles_mondatok('TBESH')
        self.assertEqual(len(tbesh), 3)
        self.assertEqual(tbesh[0], tahot[0])
        self.assertTrue(tbesh[1].startswith('Refer others'))
        self.assertEqual(lic.megjeloles_mondatok('BDB'), ())
        self.assertEqual(self.lap.count(tahot[0]), 1)


class Istentiszt(_Alap):
    AZONOSITO = ISTENTISZT

    def test_a_lap_elkeszul(self):
        self.assertIn('| Negatív kritérium | a lap elején áll', self.lap)
        self.assertIn('| ID | ISTENTISZT-001 |', self.lap)

    def test_n223_licenckapu(self):
        self.assertEqual(SZ.licenc_hianyok(SZ.licenc_meres(self.korny, self.elozo)), [])
        self.assertEqual(self.modell.licenc_hiany, ())


class Datumforma(unittest.TestCase):
    def test_datum_pont_es_nap(self):
        sor = SablonSor('x', '{a}–{b}', 'a:datum(pont), b:datum(nap)')
        self.assertEqual(kiir(sablon(sor, a=datetime.date(2026, 11, 1), b=datetime.date(2026, 11, 3))),
                         '2026.11.01–03')

    def test_ismeretlen_datumforma(self):
        with self.assertRaises(SablonHiba):
            SablonSor('x', '{a}', 'a:datum(ev)')


if __name__ == '__main__':
    unittest.main()
