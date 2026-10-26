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
  (a) **Változatlan átvétel (műcím).** Egy besorolt sigla (amelynek `magyar_alak`-ja nem maga a `forrasalak`) *egy* előfordulása nem
      követeli meg a magyar alakot, ha *átvett*: (1) a sigla után legalább `ATVETEL_SZO` (3) szó áll, (2) az első ilyen szó nagybetűvel
      kezdődik (cím-jelleg; a kisbetűs folytatás — `Philo's use of …`, `Homer, under the word` — folyó angol szöveg, nem műcím), és (3) a
      sigla szavától az ablak végéig (a sigla szava + 3 szó, a záró írásjel nélkül) a szöveg szóközre normalizálva szó szerint megvan a
      fordításban (szóhatáron kezdődően). Példa: `Philo's Lehre von der Weltschöpfung` -> ablak `Philo's Lehre von der`. A sor csak a
      nem átvett előfordulásokra követeli meg a magyar alakot; ha minden előfordulás átvett, a sor nem ellenőrzött, és a részletben
      „N sigla változatlan átvételben, nem ellenőrzött” áll. Hamis negatív ellen: a folyó szövegbeli (nem átvett) előfordulás magyar
      alakját a kapu továbbra is megköveteli (az ablakot a fordítás körülötte lefordított szövege nem tartalmazza). Ismert határ: ha a
      fordító egy nagybetűs szóval induló, 3+ szavas angol mondatrészt a siglával együtt fordítatlanul hagy, a kapu ezt átvételnek veszi;
      ezt a 14. szakasz-, 6. hossz- és az egyéb kapuk, valamint a független ellenőrzés fogja.
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


def _atvett(forras, m, forditas_norm):
    """F145 (a): a `m` találat (a sigla a forrásban) változatlan átvétel-e a fordításban (l. a modul docstringjét)."""
    szavak = forras[m.start():].split()
    if len(szavak) < 1 + ATVETEL_SZO or not szavak[1][:1].isupper():
        return False
    ablak = re.sub(r'[^\w]+$', '', ' '.join(szavak[:1 + ATVETEL_SZO]))
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
        if cel != r['forrasalak'] and all(_atvett(forras, m, forditas_norm) for m in _re(r['forrasalak']).finditer(forras)):
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
