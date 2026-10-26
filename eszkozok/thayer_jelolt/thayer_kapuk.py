#!/usr/bin/env python
"""A Thayer szakaszonkénti fordításának kapui (F132; DT-F132d (1), brief 2a/5).

A közös kapusor (`eszkozok/forditas_kapuk.py` `kapuk_futtat_szakaszos`, benne a `14_szakasz` és a `15_tiltott`) változatlanul
fut, és egy Thayer-specifikus kapuval bővül:

  16_sigla   a sigla-tábla (`adat/thayer_sigla.tsv`, SEMA 2.37) **besorolt** soraira: ha a forrás tartalmazza a `forrasalak`-ot,
             a fordításban áll a tábla szerinti alak (`magyar_alak`; `változatlan` esetén maga a `forrasalak`). Hiánya SERTES
             (gátoló). Besorolatlan sor (`jelolt`, illetve a jóváhagyatlan `javaslat`, DT-F132j (3)) nem gátol: a kapu a számát
             JELZES-ként jelenti. A `besorolt`, `magyar_alak = nincs_egyseges` sor (nincs egységes alak, pl. `N.`, `e.`) nem
             ellenőrzött és nem besorolatlan: nem számít bele egyikbe sem. A `besorolt`, de **üres** `magyar_alak`-ú sor kitöltetlen
             besorolás (ELLENOR_F132 4. tétel): nem ellenőrzött, és a kapu JELZES-ként jelenti (nem gátol: a hiba a táblában van, nem
             a fordításban), hogy ne menjen át csendben.

  A kapu három tűrése (F145; DT-F142b/c, SEMA 2.37). A forrás-oldali keresés (`forrasalak`) mindháromnál változatlan: önálló szó.
  (a) **Változatlan átvétel (egyedi, soronkénti kivétel).** A sigla `magyar_alak`-ját a fordításnak minden előfordulásban tartalmaznia kell,
      **kivéve** az `ATVETEL_KIVETEL` állandó elemeit. Elem: (Strong, sigla, a változatlanul átvett ablak). Az ablak a sigla szava + a
      következő `ATVETEL_SZO` (3) szó, a záró írásjel nélkül; az előfordulás akkor mentesül, ha (1) a (sigla, ablak) pár szerepel a
      kivételek között, és (2) az ablak szóközre normalizálva, szóhatáron kezdődően szó szerint megvan a fordításban. Kezdetben egyetlen
      elem van: G0012, `Philo`, `Philo's Lehre von der` (J. G. Müller, *Philo's Lehre von der Weltschöpfung*, műcím). A sor csak a nem
      mentesülő előfordulásokra követeli meg a magyar alakot; ha minden előfordulás mentesül, a sor nem ellenőrzött, és a részletben
      „N sigla változatlan átvételben, nem ellenőrzött” áll. A hívó (`forditas.py`) a Strongot nem adja át a kapunak, ezért a kivételt
      a (sigla, ablak) egyezés azonosítja; a Strong a dokumentáció (és a kivétel eredetének nyoma).
      **Szűkítés indoka (DT-F145a (b), a felhasználó döntése, 2026-10-26; ELLENOR_F145 1.):** a korábbi általános szabály (a sigla utáni
      szó nagybetűs + az ablak szó szerint megvan) a `rövidítés` típusról az F145.9-ben, az `antik szerző` és `modern szerző` típusról
      itt kikerült, mert a fordítatlan szerző-sigla (`Xenophon, Cyril 3, 3`; G0282 `by Philo in de temul.`; G4151 `in Philo's use of`)
      is átment volna a kapun. A DT-F142b állítása (a műcím-kivétel) csak a G0012-re igazolt, ezért csak arra szól. Következmény: más
      szerző-típusú sigla (és a `cf. Winers Grammar` típusú rövidítés) fordítatlanul mindig SERTES; új kivétel csak döntéssel és
      ellenőrzött egyedi sorral vehető fel.
  (b) **Ragozás-tűrés.** A cél-alak (a `magyar_alak`, `változatlan` esetén a `forrasalak`) szó elején kezdődik, de toldalékot elfogad
      (`Homérosztól`, `Platónnál`, `Septuagintában`, `Gesenius-szal`): a cél-alak után nincs szóhatár-követelmény. Nem érvényes (a szóhatár
      marad): az egybetűs siglára (láncszabály), a legfeljebb 3 betűs cél-alakra (`Tr` ~ `Trench`, `WH`) és a `könyvrövidítés` típusra
      (`Bölcs` ~ `Bölcsesség`, `Sir` ~ `Sirály`; ott a 11. kapu alakja a mérték: `Makk-ban` a kötőjel miatt eleve találat). A pont
      végű cél-alaknak (`vö.`, `stb.`) eleve nincs záró határa. `TOLDALEK_MIN` = 4 betű.
  (c) **Számjegy-előtag.** A `könyvrövidítés` típusú sor cél-alakja számjegy mögött is találat (`4Makk`, `2Makk`, a 11. kapu alakja):
      a szó előtt betű nem állhat, számjegy igen. A szóvég-határ itt marad (`Makk-ban` találat, `Makkabeusok` nem).
  Az egybetűs sigla láncszabálya (F132.20) és szigorú szóhatára nem változik.

  from thayer_kapuk import kapuk_futtat_thayer, atment
TSV: split('\\t'), csv modul nélkül.
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(os.path.dirname(ITT))
ESZK = os.path.join(GYOKER, 'eszkozok')
if ESZK not in sys.path:
    sys.path.insert(0, ESZK)
import forditas_kapuk as K  # noqa: E402

SIGLA_UT = os.path.join(GYOKER, 'adat', 'thayer_sigla.tsv')
THAYER_GATOLO = ['16_sigla']
VALTOZATLAN = 'változatlan'
NINCS_EGYSEGES = 'nincs_egyseges'
ATVETEL_SZO = 3                                   # F145 (a): a változatlan átvétel ablaka: a sigla szava + ennyi szó
# F145.14 (DT-F145a (b)): a változatlan átvétel NEM általános kivétel; csak az itt felsorolt egyedi sorok mentesülnek.
# Elem: (Strong, sigla `forrasalak`, a változatlanul átvett ablak: a sigla szava + 3 szó, záró írásjel nélkül). A kapu hívása
# a Strongot nem adja át (forditas.py), ezért a kivételt a (sigla, ablak) szó szerinti egyezés azonosítja; a Strong dokumentáció.
ATVETEL_KIVETEL = (
    ('G0012', 'Philo', "Philo's Lehre von der"),     # J. G. Müller, Philo's Lehre von der Weltschöpfung (műcím; DT-F142b, Greppel igazolta)
)
KONYVROV = 'könyvrövidítés'                      # F145 (c): számjegy mögött is találat
TOLDALEK_MIN = 4                                  # F145 (b): ennél rövidebb cél-alaknál nincs toldalék-tűrés
_CACHE = {}


def sigla_betolt(ut=None):
    ut = ut or SIGLA_UT
    if ut not in _CACHE:
        with open(ut, encoding='utf-8', newline='') as f:
            sorok = [s.rstrip('\r') for s in f.read().split('\n')]
        sorok = [s for s in sorok if s and not s.startswith('#')]
        fej = sorok[0].split('\t')
        _CACHE[ut] = [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]
    return _CACHE[ut]


# Egybetűs sigla (`R`, `G`, `L`, `T`) többtagú rövidítésen belül nem találat (ELLENOR_F132 3. tétel): a betű-pont(-szóköz)-betű-pont
# láncban (`N. T.`, `O. T.`, `A. V.`, `R. V.`, `G. L. Hahn`, `N.T.`) a betű a rövidítés tagja, nem kiadás-sigla. A szomszéd betű maga
# is önálló kell legyen (`Gen. T` a `T`-t találja).
_LANC_ELOTT = r'(?<!(?<!\w)[^\W\d_]\.\s)(?<!(?<!\w)[^\W\d_]\.)'
_LANC_UTAN = r'(?!\.\s?[^\W\d_]\.)'


def _re(alak):
    egybetus = len(alak) == 1 and alak.isalpha()
    return re.compile(r'(?<![\w])' + (_LANC_ELOTT if egybetus else '') + re.escape(alak)
                      + (r'(?![\w])' if alak[-1:].isalnum() else '') + (_LANC_UTAN if egybetus else ''))


def _re_cel(alak, tipus=''):
    """A cél-oldali (fordítás-beli) keresés (F145 (b), (c)): `_re` + toldalék-tűrés (a legalább `TOLDALEK_MIN` betűs, nem könyvrövidítés cél-alaknál), számjegy-előtag a könyvrövidítésnél."""
    if len(alak) == 1 and alak.isalpha():
        return _re(alak)
    elotte = r'(?<![^\W\d_])' if tipus == KONYVROV else r'(?<![\w])'
    toldalekos = tipus != KONYVROV and len(alak) >= TOLDALEK_MIN
    veg = r'(?![\w])' if alak[-1:].isalnum() and not toldalekos else ''
    return re.compile(elotte + re.escape(alak) + veg)


def _atvett(forras, m, forditas_norm, sigla_alak):
    """F145.14 (DT-F145a (b)): a `m` találat egy `ATVETEL_KIVETEL`-sor változatlan átvétele-e a fordításban (l. a modul docstringjét)."""
    szavak = forras[m.start():].split()
    if len(szavak) < 1 + ATVETEL_SZO:
        return False
    ablak = re.sub(r'[^\w]+$', '', ' '.join(szavak[:1 + ATVETEL_SZO]))
    if not any(sigla_alak == sa and ablak == ab for _, sa, ab in ATVETEL_KIVETEL):
        return False
    return re.search(r'(?<![\w])' + re.escape(ablak), forditas_norm) is not None


def ellenoriz_sigla(forras, forditas, sigla=None):
    sigla = sigla_betolt() if sigla is None else sigla
    hibak, besorolatlan, kitoltetlen, n, atvetel = [], 0, [], 0, []
    forditas_norm = ' '.join(forditas.split())
    for r in sigla:
        if not r.get('forrasalak') or not _re(r['forrasalak']).search(forras):
            continue
        if r.get('allapot') == 'besorolt' and r.get('magyar_alak') == NINCS_EGYSEGES:
            continue
        if r.get('allapot') == 'besorolt' and not r.get('magyar_alak'):
            kitoltetlen.append(r['forrasalak'])
            continue
        if r.get('allapot') != 'besorolt':
            besorolatlan += 1
            continue
        cel = r['forrasalak'] if r['magyar_alak'] == VALTOZATLAN else r['magyar_alak']
        if cel != r['forrasalak'] and all(_atvett(forras, m, forditas_norm, r['forrasalak']) for m in _re(r['forrasalak']).finditer(forras)):
            atvetel.append(r['forrasalak'])      # minden előfordulás változatlan átvétel: a sor nem ellenőrzött
            continue
        n += 1
        if not _re_cel(cel, r.get('tipus', '')).search(forditas):
            hibak.append('%s -> %s hiányzik' % (r['forrasalak'], cel))
    if hibak:
        return 'SERTES', '; '.join(hibak[:8])
    atv = ('; %d sigla változatlan átvételben, nem ellenőrzött (%s)' % (len(atvetel), ', '.join(atvetel[:8]))) if atvetel else ''
    if besorolatlan or kitoltetlen:
        reszek = ['%d besorolt sigla rendben%s' % (n, atv)]
        if besorolatlan:
            reszek.append('%d besorolatlan sigla a forrásban (nem gátol)' % besorolatlan)
        if kitoltetlen:
            reszek.append('%d besorolt sigla üres magyar_alak-kal, kitöltetlen (alak vagy `%s` kell; nem gátol): %s'
                          % (len(kitoltetlen), NINCS_EGYSEGES, ', '.join(kitoltetlen[:8])))
        return 'JELZES', '; '.join(reszek)
    return 'RENDBEN', '%d besorolt sigla rendben%s' % (n, atv)


def kapuk_futtat_thayer(forras, forditas, bizonytalan=(), sigla=None):
    """forras / forditas: tokenes szöveg (`⟪n⟫`). -> [(nev, eredmeny, reszlet)]."""
    ki = K.kapuk_futtat_szakaszos('Thayer', forras, forditas, bizonytalan)
    ki.append(('16_sigla',) + ellenoriz_sigla(K.szakasz_nelkul(forras), K.szakasz_nelkul(forditas), sigla))
    return ki


def atment(eredmenyek):
    return K.atment(eredmenyek) and all(e != 'SERTES' for n, e, _ in eredmenyek if n in THAYER_GATOLO)
