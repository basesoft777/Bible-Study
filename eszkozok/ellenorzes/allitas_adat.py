#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
allitas_adat.py -- F196.1: az állítás–adat kapu (JELENTÉS szint).

Mit mér: a generált lexikonlap (`lexikon/[ID]_TUDOMANYOS.md`) és a mellékletlapja (`lexikon/[ID]_KIZARASOK.md`)
látható szövegében álló számokat és „nincs …” mondatokat a saját adatukhoz méri. A kapuk eddig a formát nézték
(szakaszrend, átírás, angol szó), az igazságot nem; a gyökérok-példa: a lapon „A motívumhoz nincs rögzített
kapcsolat.” állt, miközben a `kapcsolatok.tsv` 56 sort tartalmazott (memória: hiba-oka-es-javitasi-szint).

Hogyan: az állítás-katalógus (`ALLITASOK`) minden eleme egy mintát ad a lap mondatára és a mondat számaihoz egy-egy
adatkulcsot. Az adatkulcs értékét az `Adat` osztály számolja, ahol lehet, a generátor saját függvényével
(`lexikon_general.dontesi_ut_adat`, `kizarasok_adat`, `lxx_osszevetes`, `karoli_szavankent`, `kapcsolatok_sorok`,
`szerep_kizart.vizsgalt_versek`, `szerep_karoli.*`), tehát a kapu nem másol logikát. Ahol a generátor a számot egy
blokkfüggvényen belül számolja, és nincs önálló függvénye, ott a kapu a blokkfüggvény számolását ismétli, a forrással
jelölve (`SAJAT_SZAMOLAS`); ezek kiemelése a generátorba külön tétel (N-F196a), mert a `lexikon_general.py`-t ez a
menet nem írja.

A lap hiányzó mondata nem hiba: a kapu csak azt méri, ami a lapon áll. Az egyező és az eltérő állítás egyaránt
listázódik; a nem mérhető állítás (az adat nem számolható) „nem mérhető” jelölést kap, nem egyezést.

Szint: JELENTÉS. A kilépési kód 0, akármit talál; a `--szigoru` kapcsolóval 1, ha van eltérés (a HIBA-szintre emelés a
HAMART-001 kiadása után, külön döntéssel jön: DT-F196a).

CLI:
    python eszkozok/ellenorzes/allitas_adat.py HAMART-001 ISTENTISZT-001
    python eszkozok/ellenorzes/allitas_adat.py --minden            # minden lap, amelynek van előfordulás-sora
    python eszkozok/ellenorzes/allitas_adat.py HAMART-001 --reszletes   # az egyező állítások is
    python eszkozok/ellenorzes/allitas_adat.py --minden --szigoru  # (később) eltérésnél 1-es kilépési kód
"""

import argparse
import collections
import io
import os
import re
import sys

ESZKOZOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ESZKOZOK not in sys.path:
    sys.path.insert(0, ESZKOZOK)
GYOKER = os.path.dirname(ESZKOZOK)
LEXIKON = os.path.join(GYOKER, 'lexikon')

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------------------
# Szám és látható szöveg
# ---------------------------------------------------------------------------

# a generátor ezres tagolása nem törő szóközzel (OK._ezres); a próza sima szóközt is írhat
SZ = r'(\d{1,3}(?:[\u00a0\u202f ]\d{3})+|\d+)'
_MEGJEGYZES = re.compile(r'<!--.*?-->', re.S)


def szam(s):
    return int(re.sub(r'[\u00a0\u202f ]', '', s))


def lathato(szoveg):
    """A HTML-megjegyzések nélküli szöveg, a sorszámok megtartásával (a megjegyzés újsorai megmaradnak)."""
    return _MEGJEGYZES.sub(lambda m: '\n' * m.group(0).count('\n'), szoveg.replace('\r\n', '\n'))


def sorszam(szoveg, poz):
    return szoveg.count('\n', 0, poz) + 1


# ---------------------------------------------------------------------------
# Az adat: egy motívum értékei, lustán számolva
# ---------------------------------------------------------------------------

class NemMerheto(Exception):
    """Az adat nem számolható (hiányzó tábla, a generátor függvénye hibát dob): az állítás „nem mérhető”."""


class Adat(object):
    """Egy motívum adatkulcsai. `ertek(kulcs)` a kulcs értékét adja (int), vagy `NemMerheto`-t dob. A kulcs vagy
    egyszerű név (`hely`), vagy pár (`('csoport_ok', ok)`)."""

    def __init__(self, mid):
        import general as G
        import lexikon_general as LG
        import szerep_karoli as SZK
        import szerep_kizart as SZKZ
        self.G, self.LG, self.SZK, self.SZKZ = G, LG, SZK, SZKZ
        self.mid = mid
        _, motivumok = G.tsv_beolvas(G.MOTIVUMOK_TSV)
        talalt = [m for m in motivumok if m['id'] == mid]
        if not talalt:
            raise NemMerheto('%s: nincs sora a motivumok.tsv-ben' % mid)
        self.m = talalt[0]
        _, elof = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
        self.sorai = G.elofordulasok_id_szerint(elof).get(mid, [])
        self.uj = bool(LG.uj_szerkezet(mid))
        if self.uj:
            LG.lemma_valtozat_beallit(self.sorai)   # a generátor főciklusa is így hívja (lexikon_general.run)
        else:
            LG.LEMMA_VALTOZAT.clear()
        self._cache = {}

    # -- a kulcsok -----------------------------------------------------------
    def ertek(self, kulcs):
        if kulcs in self._cache:
            v = self._cache[kulcs]
        else:
            try:
                v = self._szamol(kulcs)
            except NemMerheto as e:
                v = e
            except Exception as e:  # noqa: BLE001 -- a generátor függvénye hibát dobott: nem mérhető, nem egyezés
                v = NemMerheto('%s: %s' % (type(e).__name__, e))
            self._cache[kulcs] = v
        if isinstance(v, NemMerheto):
            raise v
        return v

    def _szamol(self, kulcs):
        G, LG, SZK, SZKZ = self.G, self.LG, self.SZK, self.SZKZ
        if isinstance(kulcs, tuple):
            nev, arg = kulcs
            if nev == 'csoport_ok':
                return self._dontesi()['csoport_ok'].get(arg, 0)
            if nev == 'egyen_ok':
                return len(self._dontesi()['egyen_ok'].get(arg, []))
            if nev == 'ok':     # az 1.3 lenyitható sora: az ok vagy csoportos, vagy egyenkénti
                d = self._dontesi()
                if arg in d['csoport_ok']:
                    return d['csoport_ok'][arg]
                return len(d['egyen_ok'].get(arg, []))
            if nev == 'kapcs_tipus':
                return sum(1 for r in self._kapcs() if (r.get('tipus') or '').lower() == arg.lower())
            if nev == 'nyelv_szo':
                elo = 'H' if arg == 'héber' else 'G'
                return sum(1 for t in LG.motivum_strong_tokenek(self.sorai) if t.startswith(elo))
            if nev == 'mell_ok':
                return len(self._melleklet()[arg[0]].get(arg[1], []))
            raise NemMerheto('ismeretlen kulcs: %r' % (kulcs,))
        # 2. Előfordulások (lexikon_general.blokk_elofordulasok számolása; SAJAT_SZAMOLAS['elof'])
        s = self.sorai
        tesz = [G.konyv_teszamentum(G.konyv_token(r['igehely'])) for r in s]
        if kulcs == 'hely':
            return len(s)
        if kulcs == 'vers':
            return len(LG._versek_halmaz(r['igehely'] for r in s))
        if kulcs == 'osz':
            return tesz.count('ÓSZ')
        if kulcs == 'usz':
            return tesz.count('ÚSZ')
        if kulcs == 'konyv':
            return len({G.konyv_token(r['igehely']) for r in s})
        if kulcs == 'top_konyv':
            db = collections.Counter(G.konyv_token(r['igehely']) for r in s)
            return max(db.values()) if db else 0
        if kulcs == 'genezis':
            return sum(1 for r in s if G.konyv_token(r['igehely']) == '1Móz')
        if kulcs == 'osz_tobbi':
            return tesz.count('ÓSZ') - sum(1 for r in s if G.konyv_token(r['igehely']) == '1Móz')
        if kulcs == 'magas':
            return sum(1 for r in s if (r.get('megbizhatosag') or '').strip() == 'magas')
        # 1. Döntési út (lexikon_general.dontesi_ut_adat)
        if kulcs in ('bent', 'egyen', 'csoport', 'nyitva', 'osszes'):
            return self._dontesi()[kulcs]
        if kulcs == 'kizart_osszes':
            d = self._dontesi()
            return d['csoport'] + d['egyen']
        if kulcs == 'csoport_ok_db':
            return len(self._dontesi()['csoport_ok'])
        if kulcs == 'egyen_ok_db':
            return len(self._dontesi()['egyen_ok'])
        # 3. Kizárt és vizsgált helyek (szerep_kizart.vizsgalt_versek, ahogy a blokk_kizart hívja)
        if kulcs == 'kizart_sor':
            return len(self._kizart_sorok())
        if kulcs in ('k_egyenkent', 'k_csoport_vers', 'k_osszes', 'k_elutasitva', 'k_nyitva'):
            v = self._vizsgalt()
            return v[{'k_egyenkent': 'egyenkent', 'k_csoport_vers': 'csoport_vers', 'k_osszes': 'osszes',
                      'k_elutasitva': 'elutasitva', 'k_nyitva': 'nyitva'}[kulcs]]
        # 7. Kapcsolatok (lexikon_general.kapcsolatok_sorok; a csomópont és a magas a blokk_kapcsolatok szerint)
        if kulcs == 'kapcs':
            return len(self._kapcs())
        if kulcs == 'kapcs_csomopont':
            return len({r['forras_igehely'] for r in self._kapcs()} | {r['cel_igehely'] for r in self._kapcs()})
        if kulcs == 'kapcs_magas':
            return sum(1 for r in self._kapcs() if r['bizonyossag'] == 'magas')
        if kulcs == 'kapcs_alacsonyabb':
            return sum(1 for r in self._kapcs() if r['bizonyossag'] != 'magas')
        # 8. Kapcsolódó motívumok (lexikon_general.kapcsolodo_olvasoi számolása)
        if kulcs in ('kapcsolodo', 'kapcsolodo_masik', 'kapcsolodo_nyitott'):
            mk = LG.motivum_kapcsolatok_sorok()
            sajat = [r for r in mk if self.mid in (r['id_a'], r['id_b'])]
            if kulcs == 'kapcsolodo':
                return len(sajat)
            if kulcs == 'kapcsolodo_masik':
                return len({r['id_b'] if r['id_a'] == self.mid else r['id_a'] for r in sajat})
            return sum(1 for j in LG.motivumkozi_jeloltek() if j.get('dontes') == 'nyitva'
                       and self.mid in (j['id'], j.get('cel_id')))
        # 5. LXX (lexikon_general.lxx_osszevetes; a mondat összege és kategóriái a lxx_olvasoi szerint)
        if kulcs in ('lxx_n', 'lxx_egyezo', 'lxx_eltero', 'lxx_minusz', 'lxx_egyeb', 'lxx_fuggoben', 'lxx_szamozas'):
            sz = self._lxx()
            return {'lxx_n': sum(sz.values()), 'lxx_egyezo': sz.get('egyező', 0), 'lxx_eltero': sz.get('eltérő', 0),
                    'lxx_minusz': sz.get('LXX-minusz', 0),
                    'lxx_egyeb': sz.get('kutatói azonosítás függőben', 0) + sz.get('szamozas_elteres', 0),
                    'lxx_fuggoben': sz.get('kutatói azonosítás függőben', 0),
                    'lxx_szamozas': sz.get('szamozas_elteres', 0)}[kulcs]
        if kulcs == 'osz_hely':
            return tesz.count('ÓSZ')
        if kulcs == 'gorog_szo':
            return sum(1 for t in LG.motivum_strong_tokenek(s) if t.startswith('G'))
        # 4.13 (lexikon_general.olvasoi_13 / olvasoi_13_szavankent számai)
        if kulcs == 'k13_n':
            return sum(1 for r in s if r.get('karoli_szo'))
        if kulcs == 'k13_szo_csalad':
            return len(SZK.szocsalad(SZK.karoli_megfelelok(s)))
        if kulcs == 'k13_szo':
            return len(SZK.karoli_megfelelok(s))
        if kulcs == 'k13_keves':
            szavak = LG.karoli_szavankent(s)
            return len(szavak) - sum(1 for _k, db, _c in szavak if db >= LG.KAROLI_MIN_HELY)
        # 4.14 (szerep_karoli.kulcsszavak / rejtett_parhuzamok / hamis_parhuzamok, ahogy az olvasoi_14_szavankent hívja)
        if kulcs == 'k14_osszes':
            return len(SZK.gerinc_kombinaciok(s))
        if kulcs == 'k14_kulcs':
            return len(self._kulcs())
        if kulcs == 'k14_rejtett':
            return len(SZK.rejtett_parhuzamok(s, kulcs=self._kulcs())) if self._kulcs() else 0
        if kulcs == 'k14_hamis':
            return len(SZK.hamis_parhuzamok(s, kulcs=self._kulcs())) if self._kulcs() else 0
        # melléklet (lexikon_general.kizarasok_adat)
        if kulcs == 'mell_osszes':
            d = self._melleklet()
            return sum(len(v) for v in d['csoport'].values()) + sum(len(v) for v in d['egyen'].values())
        raise NemMerheto('ismeretlen kulcs: %r' % (kulcs,))

    # -- a generátor függvényei, egyszer hívva -------------------------------------
    def _dontesi(self):
        if '_d' not in self._cache:
            self._cache['_d'] = self.LG.dontesi_ut_adat(self.m, self.sorai)
        return self._cache['_d']

    def _kizart_sorok(self):
        return [r for r in self.LG.jeloltek_sorok() if r['id'] == self.mid and r.get('dontes') in ('elutasítva', 'nyitva')]

    def _vizsgalt(self):
        if '_v' not in self._cache:
            cs_n = self.LG.csoport_n(self.mid) if self.uj else None
            self._cache['_v'] = self.SZKZ.vizsgalt_versek(self._kizart_sorok(), csoport_n=cs_n)
        return self._cache['_v']

    def _kapcs(self):
        if '_k' not in self._cache:
            self._cache['_k'] = [r for r in self.LG.kapcsolatok_sorok() if r['id'] == self.mid]
        return self._cache['_k']

    def _lxx(self):
        if '_lxx' not in self._cache:
            tok = self.LG.motivum_strong_tokenek(self.sorai)
            osz = [r for r in self.sorai if self.G.konyv_teszamentum(self.G.konyv_token(r['igehely'])) == 'ÓSZ']
            if not osz:
                self._cache['_lxx'] = collections.Counter()
            else:
                _sorok, szamlalo, _f, _h = self.LG.lxx_osszevetes(self.sorai, tok)
                self._cache['_lxx'] = szamlalo
        return self._cache['_lxx']

    def _kulcs(self):
        if '_kulcs' not in self._cache:
            self._cache['_kulcs'] = collections.OrderedDict(
                (k, v) for k, v in self.SZK.kulcsszavak(self.sorai).items() if v)
        return self._cache['_kulcs']

    def _melleklet(self):
        if '_mell' not in self._cache:
            self._cache['_mell'] = self.LG.kizarasok_adat(self.m, self.sorai)
        return self._cache['_mell']


# Ahol a kapu nem a generátor önálló függvényét hívja, hanem a blokkfüggvény számolását ismétli (N-F196a): a kulcs és a
# generátor helye. A kiemelés után ezek a kulcsok a kiemelt függvényt hívják.
SAJAT_SZAMOLAS = {
    'elof': 'lexikon_general.blokk_elofordulasok (a tesz/konyv_db/magas számolása az OK.elofordulasok* hívása előtt)',
    'kapcs': 'lexikon_general.blokk_kapcsolatok (a csomópont és a magas bizonyosság számolása)',
    'kapcsolodo': 'lexikon_general.kapcsolodo_olvasoi (a sajat/nyitott számolása)',
    'kizart_sor': 'lexikon_general.blokk_kizart (a sorok_ehhez szűrése)',
    'k13': 'lexikon_general.olvasoi_13_szavankent (az n és a szócsalád-szám)',
    'k14': 'lexikon_general.olvasoi_14_szavankent (a kulcs szűrése)',
}


# ---------------------------------------------------------------------------
# Az állítás-katalógus
# ---------------------------------------------------------------------------
# Elem: (azonosító, leírás, minta, [(csoportnév, adatkulcs), …], fájl). A minta nevesített csoportjai számok; a
# hiányzó (opcionális) csoport nem mér. A `fajl` 'lap' vagy 'melleklet'. A „nincs” mondatoknál a kulcs értékének 0-nak
# kell lennie: (csoportnév None, kulcs) — a lapon az állítás „0”.

def _n(nev):
    return r'(?P<%s>\d{1,3}(?:[\u00a0\u202f ]\d{3})+|\d+)' % nev


ALLITASOK = [
    # --- 2. Előfordulások (az olvasói összegzés, régi és új szerkezet) ---
    ('ELOF', 'az előfordulás-összegzés: hely, könyv, ÓSZ/ÚSZ, magas megbízhatóság',
     r'A motívum %s igehelyen fordul elő, %s bibliai könyvben(?: \((?:%s ószövetségi)?(?:, )?(?:%s újszövetségi)? hely\))?'
     r'(?:; a legtöbb hely: [^.]*?)?\. %s hely azonosítása magas'
     % (_n('hely'), _n('konyv'), _n('osz'), _n('usz'), _n('magas')),
     [('hely', 'hely'), ('konyv', 'konyv'), ('osz', 'osz'), ('usz', 'usz'), ('magas', 'magas')], 'lap'),
    ('ELOF_ALACSONY', 'az alacsonyabb megbízhatóságú helyek száma',
     r'%s hely azonosítása magas megbízhatóságú, %s alacsonyabb' % (_n('magas'), _n('alacsony')),
     [('magas', 'magas')], 'lap'),
    ('ELOF_SULYPONT', 'a súlypont-könyv helyeinek száma',
     r'súlypontja [^(]{1,80}\(%s helyből %s\)' % (_n('hely'), _n('top')),
     [('hely', 'hely'), ('top', 'top_konyv')], 'lap'),
    ('ELOF_HATOKOR', 'a 2. blokk hatókör-sora: igehely-sorok száma',
     r'Ez a blokk a motívum %s igehely-sorát fedi' % _n('hely'), [('hely', 'hely')], 'lap'),
    ('KIVONAT_HELY_VERS', 'a Kivonat: hely és vers',
     r'%s helyet sorol fel %s versben' % (_n('hely'), _n('vers')), [('hely', 'hely'), ('vers', 'vers')], 'lap'),
    ('KIVONAT_BONTAS', 'a Kivonat: Genezis / többi ÓSZ / ÚSZ helyei',
     r'%s-?[a-zéáöő]* a Genezisből, %s-?[a-zéáöő]* az Ószövetség többi könyvéből és %s-?[a-zéáöő]* az Újszövetségből'
     % (_n('gen'), _n('tobbi'), _n('usz')), [('gen', 'genezis'), ('tobbi', 'osz_tobbi'), ('usz', 'usz')], 'lap'),
    # --- 1. Döntési út ---
    ('DONTES_ELSO', 'a Döntési út bevezetője: megvizsgált és beépült vers',
     r'%s megvizsgált versből %s tartozik a motívumhoz' % (_n('osszes'), _n('bent')),
     [('osszes', 'osszes'), ('bent', 'bent')], 'lap'),
    ('DONTES_OSSZES', 'az 1.3 tábla: megvizsgált versek összesen',
     r'\*\*Megvizsgált versek összesen\*\* \| \*\*%s\*\*' % _n('osszes'), [('osszes', 'osszes')], 'lap'),
    ('DONTES_CSOPORT', 'az 1.3 tábla: csoportosan kizárt versek és okok száma',
     r'\*\*Csoportosan kizárva\*\* \| \*\*%s\*\* \|[^|]*\(%s ok' % (_n('csoport'), _n('okdb')),
     [('csoport', 'csoport'), ('okdb', 'csoport_ok_db')], 'lap'),
    ('DONTES_EGYEN', 'az 1.3 tábla: egyenként elutasított versek és okok száma',
     r'\*\*Egyenként elbírálva és elutasítva\*\* \| \*\*%s\*\* \|[^|]*\(%s ok' % (_n('egyen'), _n('okdb')),
     [('egyen', 'egyen'), ('okdb', 'egyen_ok_db')], 'lap'),
    ('DONTES_BENT', 'az 1.3 tábla: a motívumhoz tartozó versek és helyek',
     r'\*\*A motívumhoz tartozik\*\* \| \*\*%s\*\* \| %s hely' % (_n('bent'), _n('hely')),
     [('bent', 'bent'), ('hely', 'hely')], 'lap'),
    ('DONTES_NYITVA', 'az 1.3 tábla: döntésre váró versek',
     r'\*\*Döntésre vár\*\* \| \*\*%s\*\*' % _n('nyitva'), [('nyitva', 'nyitva')], 'lap'),
    ('DONTES_OSSZEADAS', 'az 1.3 összeadása',
     r'\*\*Összeadás:\*\* %s \(a motívumhoz tartozik\) \+ %s \(csoportosan kizárva\) \+ %s \(egyenként elutasítva\)'
     r'(?: \+ %s \(döntésre vár\))? = %s megvizsgált vers' % (_n('bent'), _n('csoport'), _n('egyen'), _n('nyitva'),
                                                              _n('osszes')),
     [('bent', 'bent'), ('csoport', 'csoport'), ('egyen', 'egyen'), ('nyitva', 'nyitva'), ('osszes', 'osszes')], 'lap'),
    ('DONTES_DONTES_NELKUL', 'az 1.3: döntés nélkül maradt vers',
     r'Döntés nélkül maradt vers: %s' % _n('nyitva'), [('nyitva', 'nyitva')], 'lap'),
    # --- 3. Kizárt és vizsgált helyek ---
    ('KIZART_VIZSGALT', 'a 3. szakasz: a motívum helyein túl vizsgált versek',
     r'A motívum %s helyén túl további %s ver' % (_n('hely'), _n('vizsgalt')),
     [('hely', 'hely'), ('vizsgalt', 'k_osszes')], 'lap'),
    ('KIZART_EGYEN_CSOPORT', 'a 3. szakasz: egyenként és csoportosan döntött versek',
     r'%s versről egyenként [^,]{1,40}, %s versről közös ok' % (_n('egyen'), _n('csoport')),
     [('egyen', 'k_egyenkent'), ('csoport', 'k_csoport_vers')], 'lap'),
    ('KIZART_NYITOTT', 'a 3. szakasz: elutasított és döntésre váró versek',
     r'Ezek közül %s nem tartozik a motívumhoz, %s döntésre vár' % (_n('elut'), _n('nyitva')),
     [('elut', 'k_elutasitva'), ('nyitva', 'k_nyitva')], 'lap'),
    ('KIZART_HATOKOR', 'a 3. blokk hatókör-sora: elutasított/nyitva maradt jelölt-sorok',
     r'motívum %s elutasított/nyitva maradt jelöltjét fedi' % _n('sor'), [('sor', 'kizart_sor')], 'lap'),
    # --- 5. LXX ---
    ('LXX', 'az LXX-összegzés (versben): összes, egyező, eltérő, hiányzó, nem megállapított',
     r'ószövetségi helyei %s versre terjednek; ezek közül %s versben a görög fordítás \(Septuaginta\) ugyanazt a szót '
     r'használja, mint az Újszövetség(?:; (?:%s versben mást)?(?:, )?(?:%s versben a görögből hiányzik)?(?:, )?'
     r'(?:%s versben a megfelelő nincs megállapítva)?)?\.'
     % (_n('n'), _n('egyezo'), _n('eltero'), _n('minusz'), _n('egyeb')),
     [('n', 'lxx_n'), ('egyezo', 'lxx_egyezo'), ('eltero', 'lxx_eltero'), ('minusz', 'lxx_minusz'),
      ('egyeb', 'lxx_egyeb')], 'lap'),
    ('LXX_REGI', 'az LXX-összegzés (helyben, régi szerkezet): összes, egyező, eltérő, hiányzó, függőben',
     r'A motívum %s ószövetségi helyéből %s helyen a görög fordítás \(Septuaginta\) ugyanazt a szót használja'
     r'(?: \([^)]*\))?, mint az Újszövetség(?:; (?:%s helyen mást)?(?:, )?(?:%s helyen a görögből hiányzik)?(?:, )?'
     r'(?:%s helyen az azonosítás függőben)?)?\.'
     % (_n('n'), _n('egyezo'), _n('eltero'), _n('minusz'), _n('egyeb')),
     [('n', 'lxx_n'), ('egyezo', 'lxx_egyezo'), ('eltero', 'lxx_eltero'), ('minusz', 'lxx_minusz'),
      ('egyeb', 'lxx_egyeb')], 'lap'),
    ('LXX_OSSZESITES', 'az 5. tábla összesítő sora',
     # a régi lapon a tábla-címkék, az új szerkezetűn az olvasói utófeldolgozás címkéi (olvasoi_utofeldolg)
     r'Összesítés: egyező=%s, eltérő=%s, LXX-minusz=%s, (?:kutatói azonosítás függőben|a megfelelő nincs megállapítva)=%s, '
     r'(?:szamozas_elteres|versszámozás miatt nem párosítva)=%s'
     % (_n('egyezo'), _n('eltero'), _n('minusz'), _n('fugg'), _n('szam')),
     [('egyezo', 'lxx_egyezo'), ('eltero', 'lxx_eltero'), ('minusz', 'lxx_minusz'), ('fugg', 'lxx_fuggoben'),
      ('szam', 'lxx_szamozas')], 'lap'),
    # --- 7. Kapcsolatok ---
    ('KAPCS', 'a 7. szakasz összegzése: kapcsolat, csomópont, magas bizonyosság',
     r'%s kapcsolat %s helyet köt össze: (?P<tipusok>[^;]+); %s magas(?:, %s alacsonyabb)?'
     % (_n('n'), _n('csomopont'), _n('magas'), _n('alacsony')),
     [('n', 'kapcs'), ('csomopont', 'kapcs_csomopont'), ('magas', 'kapcs_magas'), ('alacsony', 'kapcs_alacsonyabb')],
     'lap'),
    ('KAPCS_HATOKOR', 'a 7. blokk hatókör-sora: kapcsolat-sorok és csomópontok',
     r'motívum %s kapcsolat-sorát fedi[^,]*, %s igehely-csomóponttal' % (_n('n'), _n('csomopont')),
     [('n', 'kapcs'), ('csomopont', 'kapcs_csomopont')], 'lap'),
    # --- 8. Kapcsolódó motívumok ---
    ('KAPCSOLODO', 'a 8. szakasz: motívumközi kapcsolatok és másik motívumok',
     r'%s kapcsolat %s másik motívummal' % (_n('n'), _n('masik')),
     [('n', 'kapcsolodo'), ('masik', 'kapcsolodo_masik')], 'lap'),
    ('KAPCSOLODO_NYITOTT', 'a 8. szakasz: döntésre váró motívumközi jelöltek',
     r'másik motívummal \([^)]*\), [^;.]*; további %s döntésre vár' % _n('nyitott'),
     [('nyitott', 'kapcsolodo_nyitott')], 'lap'),
    # --- 4.13 / 4.14 ---
    ('K13_UJ', 'a 4.13: Károli-szóval álló helyek és szócsaládok',
     r'A motívum %s igehelyén a Károli %s különböző magyar szót használ \(szócsaládonként\)' % (_n('n'), _n('k')),
     [('n', 'k13_n'), ('k', 'k13_szo_csalad')], 'lap'),
    ('K13_REGI', 'a 4.13 (régi): Károli-szóval álló helyek és szótári alakok',
     r'A motívum %s igehelyén a Károli %s különböző magyar szót használ\. ' % (_n('n'), _n('k')),
     [('n', 'k13_n'), ('k', 'k13_szo')], 'lap'),
    ('K13_KEVES', 'a 4.13: a következtetéshez kevés helyen álló szavak',
     r'A többi %s szó \d+ helynél kevesebben áll' % _n('n'), [('n', 'k13_keves')], 'lap'),
    ('K14_KULCS', 'a 4.14: a motívum szavai és a kulcsszavas szavak',
     r'Ilyen kulcsszava a motívum %s szava közül %s-' % (_n('osszes'), _n('kulcs')),
     [('osszes', 'k14_osszes'), ('kulcs', 'k14_kulcs')], 'lap'),
    ('K14_REJTETT', 'a 4.14: rejtett párhuzamok',
     r'\*\*Rejtett párhuzam\*\* \([^)]*\)[^.\n]{0,200}?(?: —|:) %s hely' % _n('n'), [('n', 'k14_rejtett')], 'lap'),
    ('K14_HAMIS', 'a 4.14: hamis párhuzamok',
     r'\*\*Hamis párhuzam\*\* \([^)]*\)[^.\n]{0,200}?(?: —|:) %s vers' % _n('n'), [('n', 'k14_hamis')], 'lap'),
    # --- a „nincs …” mondatok: az adatkulcsnak 0-nak kell lennie ---
    ('NINCS_KAPCS', '„nincs rögzített kapcsolat”', r'otívumhoz nincs rögzített kapcsolat\.', [(None, 'kapcs')], 'lap'),
    ('NINCS_KAPCS_OLV', '„a kapcsolatok … még nincs ilyen”',
     r'igehelyei közötti kapcsolatok; ennél a motívumnál még nincs ilyen', [(None, 'kapcs')], 'lap'),
    ('NINCS_KIZART', '„nincs kizárt vagy nyitva maradt jelölt”',
     r'nincs kizárt vagy nyitva maradt jelölt', [(None, 'kizart_sor')], 'lap'),
    ('NINCS_KIZART_OLV', '„a kizárt helyek … nincs ilyen”',
     r'kizárt helyek; ennél a motívumnál nincs ilyen', [(None, 'kizart_sor')], 'lap'),
    ('NINCS_KAPCSOLODO', '„nincs rögzített motívumközi kapcsolat”',
     r'nincs rögzített motívumközi kapcsolat', [(None, 'kapcsolodo')], 'lap'),
    ('NINCS_KAPCSOLODO_OLV', '„még nincs rögzített kapcsolata más motívummal”',
     r'még nincs rögzített kapcsolata más motívummal', [(None, 'kapcsolodo')], 'lap'),
    ('NINCS_OSZ', '„nincs ószövetségi előfordulása”',
     r'nincs (?:ÓSZ-i|ószövetségi) előfordulása', [(None, 'osz_hely')], 'lap'),
    ('NINCS_GOROG', '„a motívumnak nincs görög szava”',
     r'A motívumnak nincs görög szava', [(None, 'gorog_szo')], 'lap'),
    ('NINCS_NYELV', '„ezen a nyelven nincs saját szava”',
     r'A motívum (?P<nyelv>héber|görög) szavainak szótári anyaga\. A motívumnak ezen a nyelven nincs saját szava',
     [(None, ('nyelv_szo', None))], 'lap'),
    ('NINCS_REJTETT', '„Rejtett párhuzam nincs”', r'\*\*Rejtett párhuzam\*\* nincs', [(None, 'k14_rejtett')], 'lap'),
    ('NINCS_HAMIS', '„Hamis párhuzam nincs”', r'\*\*Hamis párhuzam\*\* nincs', [(None, 'k14_hamis')], 'lap'),
    ('NINCS_KULCSSZO', '„egyik szavának sincs ilyen kulcsszava”',
     r'A motívum egyik szavának sincs ilyen kulcsszava', [(None, 'k14_kulcs')], 'lap'),
    # --- melléklet (lexikon/[ID]_KIZARASOK.md) ---
    ('MELL_BENT', 'a melléklet: a motívum versei', r'a motívum %s versén túl' % _n('bent'), [('bent', 'bent')],
     'melleklet'),
    ('MELL_OSSZES', 'a melléklet: a kizárt versek összesen',
     r'nem tartozó mind (?:az? )?%s vers' % _n('n'), [('n', 'mell_osszes')], 'melleklet'),
    ('MELL_OSSZEADAS', 'a melléklet összeadása',
     r'\*\*Összeadás:\*\* %s \(csoportosan kizárva\) \+ %s \(egyenként elutasítva\) = %s vers'
     % (_n('csoport'), _n('egyen'), _n('n')),
     [('csoport', 'csoport'), ('egyen', 'egyen'), ('n', 'kizart_osszes')], 'melleklet'),
]

_LENYITHATO = re.compile(r'<summary><strong>(?P<ok>[^<]+)</strong> — %s vers</summary>' % _n('n'))
_KAPCS_TIPUS = re.compile(r'%s (?P<tipus>[^\s,;]+)' % _n('n'))
_MELL_CIM = re.compile(r'^### (?P<ok>.+) — %s vers$' % _n('n'))
_MELL_SZAKASZ = re.compile(r'^## (?P<cim>.+)$')
_MELL_LISTA = re.compile(r'^- \*\*(?P<konyv>[^*]+)\*\* \((?P<n>\d+)\): (?P<helyek>.+)$')


Eredmeny = collections.namedtuple('Eredmeny', 'azonosito leiras fajl sor lapon adatban allapot megjegyzes')
EGYEZIK, ELTER, NEM_MERHETO = 'egyezik', 'ELTÉR', 'nem mérhető'


def _osszevet(adat, azon, leiras, fajl, sor, lapon, kulcs, megj=''):
    try:
        v = adat.ertek(kulcs)
    except NemMerheto as e:
        return Eredmeny(azon, leiras, fajl, sor, lapon, None, NEM_MERHETO, str(e))
    return Eredmeny(azon, leiras, fajl, sor, lapon, v, EGYEZIK if v == lapon else ELTER, megj)


def _kulcs_nev(kulcs):
    return kulcs if isinstance(kulcs, str) else '%s:%s' % kulcs


def meres_szoveg(szoveg, adat, fajl='lap'):
    """Egy szöveg (lap vagy melléklet) állításai: [Eredmeny]. A szöveg a nyers fájltartalom."""
    lat = lathato(szoveg)
    ki = []
    for azon, leiras, minta, mezok, hol in ALLITASOK:
        if hol != fajl:
            continue
        for m in re.finditer(minta, lat):
            sor = sorszam(lat, m.start())
            for csop, kulcs in mezok:
                if csop is None:   # „nincs” mondat: az adat 0
                    if isinstance(kulcs, tuple) and kulcs[1] is None:
                        kulcs = (kulcs[0], m.group('nyelv'))
                    ki.append(_osszevet(adat, azon, leiras, fajl, sor, 0, kulcs, _kulcs_nev(kulcs)))
                    continue
                if m.group(csop) is None:
                    continue
                ki.append(_osszevet(adat, azon, '%s [%s]' % (leiras, csop), fajl, sor, szam(m.group(csop)), kulcs,
                                    _kulcs_nev(kulcs)))
            if azon == 'KAPCS':   # a típusonkénti szám: „43 párhuzam, 7 kontraszt, 6 variáns”
                for t in _KAPCS_TIPUS.finditer(m.group('tipusok')):
                    ki.append(_osszevet(adat, 'KAPCS_TIPUS', 'a 7. összegzés: típusonként [%s]' % t.group('tipus'),
                                        fajl, sor, szam(t.group('n')), ('kapcs_tipus', t.group('tipus'))))
    if fajl == 'lap':
        # az 1.3 lenyitható okai: „<ok> — N vers”; ugyanaz az ok csoportos és egyenkénti is lehet, ezért az alcím dönt
        for m in _LENYITHATO.finditer(lat):
            ok = m.group('ok').strip()
            elotte = '\n' + lat[:m.start()]
            cs, eg = elotte.rfind('\n#### Csoportosan'), elotte.rfind('\n#### Egyenként')
            kulcs = ('csoport_ok', ok) if cs > eg else ('egyen_ok', ok) if eg > cs else ('ok', ok)
            ki.append(_osszevet(adat, 'DONTES_OK', 'az 1.3 lenyitható ok-sora [%s]' % ok, fajl, sorszam(lat, m.start()),
                                szam(m.group('n')), kulcs, _kulcs_nev(kulcs)))
    else:
        ki += _melleklet_listak(lat, adat)
    return ki


def _melleklet_listak(lat, adat):
    """A melléklet okonkénti címsora (`### <ok> — N vers`) és a felsorolt versek az adathoz mérve."""
    ki = []
    szakasz = None
    aktualis = None   # (ok, sor, [versek])

    def lezar():
        if aktualis is None:
            return []
        ok, sor, versek, n_cim = aktualis
        if not versek:
            return []
        tipus = 'csoport' if szakasz == 'csoport' else 'egyen'
        e = [_osszevet(adat, 'MELL_LISTA', 'a melléklet felsorolt versei [%s]' % ok, 'melleklet', sor, len(versek),
                       ('mell_ok', (tipus, ok)))]
        try:
            vart = set(adat._melleklet()[tipus].get(ok, []))
            kulonbseg = len(set(versek) ^ vart)
            if kulonbseg:
                e.append(Eredmeny('MELL_LISTA_TAG', 'a melléklet felsorolt versei, tagonként [%s]' % ok, 'melleklet',
                                  sor, len(set(versek) - vart), 0, ELTER,
                                  '%d vers csak a mellékletben, %d csak az adatban'
                                  % (len(set(versek) - vart), len(vart - set(versek)))))
        except Exception as ex:  # noqa: BLE001
            e.append(Eredmeny('MELL_LISTA_TAG', 'a melléklet felsorolt versei, tagonként [%s]' % ok, 'melleklet', sor,
                              len(versek), None, NEM_MERHETO, str(ex)))
        return e

    for i, s in enumerate(lat.split('\n'), start=1):
        sz = _MELL_SZAKASZ.match(s)
        if sz:
            ki += lezar()
            aktualis = None
            szakasz = 'csoport' if 'Csoportosan' in sz.group('cim') else 'egyen' if 'Egyenként' in sz.group('cim') else None
            continue
        c = _MELL_CIM.match(s)
        if c and szakasz:
            ki += lezar()
            ok = c.group('ok').strip()
            aktualis = (ok, i, [], szam(c.group('n')))
            ki.append(_osszevet(adat, 'MELL_OK', 'a melléklet ok-címsora [%s]' % ok, 'melleklet', i, szam(c.group('n')),
                                (('csoport_ok', ok) if szakasz == 'csoport' else ('egyen_ok', ok))))
            continue
        lm = _MELL_LISTA.match(s)
        if lm and aktualis is not None:
            konyv = lm.group('konyv').strip()
            for h in lm.group('helyek').split(','):
                h = h.strip()
                if h:
                    aktualis[2].append('%s %s' % (konyv, h))
    ki += lezar()
    return ki


def _olvas(ut):
    with io.open(ut, encoding='utf-8') as f:
        return f.read()


def meres(mid):
    """{'lap': [Eredmeny], 'melleklet': [Eredmeny], 'hiba': str|None} egy motívumra."""
    lap_ut = os.path.join(LEXIKON, '%s_TUDOMANYOS.md' % mid)
    mell_ut = os.path.join(LEXIKON, '%s_KIZARASOK.md' % mid)
    if not os.path.exists(lap_ut):
        return {'lap': [], 'melleklet': [], 'hiba': 'nincs lexikon/%s_TUDOMANYOS.md' % mid}
    try:
        adat = Adat(mid)
    except NemMerheto as e:
        return {'lap': [], 'melleklet': [], 'hiba': str(e)}
    ki = {'lap': meres_szoveg(_olvas(lap_ut), adat, 'lap'), 'melleklet': [], 'hiba': None}
    if os.path.exists(mell_ut):
        ki['melleklet'] = meres_szoveg(_olvas(mell_ut), adat, 'melleklet')
    return ki


def osszes_lap_id():
    ki = []
    for nev in sorted(os.listdir(LEXIKON)):
        if nev.endswith('_TUDOMANYOS.md'):
            ki.append(nev[:-len('_TUDOMANYOS.md')])
    return ki


# ---------------------------------------------------------------------------
# Jelentés
# ---------------------------------------------------------------------------

def _cella(x):
    return '—' if x is None else str(x).replace('|', '\\|')


def jelentes(eredmenyek, reszletes=False):
    """Markdown jelentés: {mid: meres(mid)} → szöveg."""
    ki = ['# Állítás–adat kapu (F196, JELENTÉS)', '',
          '*A lap számai és „nincs …” mondatai a saját adatukhoz mérve. Szint: JELENTÉS, nem gátol (a HIBA-szint külön döntés).*', '']
    for mid, e in eredmenyek.items():
        if e['hiba']:
            ki += ['## %s' % mid, '', 'Nem mérhető: %s' % e['hiba'], '']
            continue
        minden = e['lap'] + e['melleklet']
        szamlalo = collections.Counter(r.allapot for r in minden)
        ki += ['## %s' % mid, '',
               '%d állítás: %d egyezik, %d eltér, %d nem mérhető.' % (
                   len(minden), szamlalo[EGYEZIK], szamlalo[ELTER], szamlalo[NEM_MERHETO]), '']
        elter = [r for r in minden if r.allapot != EGYEZIK]
        if elter:
            ki += ['| Fájl | Sor | Állítás | Lapon | Adatban | Állapot | Adatkulcs / ok |', '|---|---|---|---|---|---|---|']
            for r in elter:
                ki.append('| %s | %d | %s | %s | %s | %s | %s |' % (
                    r.fajl, r.sor, _cella(r.leiras), _cella(r.lapon), _cella(r.adatban), r.allapot,
                    _cella(r.megjegyzes)))
            ki.append('')
        if reszletes:
            egyez = [r for r in minden if r.allapot == EGYEZIK]
            if egyez:
                ki += ['<details><summary>Egyező állítások (%d)</summary>' % len(egyez), '',
                       '| Fájl | Sor | Állítás | Érték |', '|---|---|---|---|']
                for r in egyez:
                    ki.append('| %s | %d | %s | %s |' % (r.fajl, r.sor, _cella(r.leiras), r.lapon))
                ki += ['', '</details>', '']
    return '\n'.join(ki) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Állítás–adat kapu (F196): a lap számai az adathoz mérve, JELENTÉS.')
    ap.add_argument('id', nargs='*', help='motívum-azonosító(k), pl. HAMART-001')
    ap.add_argument('--minden', action='store_true', help='minden lexikon/*_TUDOMANYOS.md lap')
    ap.add_argument('--reszletes', action='store_true', help='az egyező állítások is')
    ap.add_argument('--szigoru', action='store_true', help='eltérésnél 1-es kilépési kód (a HIBA-szintre emelés után)')
    args = ap.parse_args(argv)
    idk = osszes_lap_id() if args.minden or not args.id else args.id
    eredmenyek = collections.OrderedDict((mid, meres(mid)) for mid in idk)
    print(jelentes(eredmenyek, args.reszletes), end='')
    elteres = sum(1 for e in eredmenyek.values() for r in e['lap'] + e['melleklet'] if r.allapot == ELTER)
    return 1 if (args.szigoru and elteres) else 0


if __name__ == '__main__':
    sys.exit(main())
