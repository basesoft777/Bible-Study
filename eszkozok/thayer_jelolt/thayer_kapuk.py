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


def ellenoriz_sigla(forras, forditas, sigla=None):
    sigla = sigla_betolt() if sigla is None else sigla
    hibak, besorolatlan, kitoltetlen, n = [], 0, [], 0
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
        n += 1
        cel = r['forrasalak'] if r['magyar_alak'] == VALTOZATLAN else r['magyar_alak']
        if not _re(cel).search(forditas):
            hibak.append('%s -> %s hiányzik' % (r['forrasalak'], cel))
    if hibak:
        return 'SERTES', '; '.join(hibak[:8])
    if besorolatlan or kitoltetlen:
        reszek = ['%d besorolt sigla rendben' % n]
        if besorolatlan:
            reszek.append('%d besorolatlan sigla a forrásban (nem gátol)' % besorolatlan)
        if kitoltetlen:
            reszek.append('%d besorolt sigla üres magyar_alak-kal, kitöltetlen (alak vagy `%s` kell; nem gátol): %s'
                          % (len(kitoltetlen), NINCS_EGYSEGES, ', '.join(kitoltetlen[:8])))
        return 'JELZES', '; '.join(reszek)
    return 'RENDBEN', '%d besorolt sigla rendben' % n


def kapuk_futtat_thayer(forras, forditas, bizonytalan=(), sigla=None):
    """forras / forditas: tokenes szöveg (`⟪n⟫`). -> [(nev, eredmeny, reszlet)]."""
    ki = K.kapuk_futtat_szakaszos('Thayer', forras, forditas, bizonytalan)
    ki.append(('16_sigla',) + ellenoriz_sigla(K.szakasz_nelkul(forras), K.szakasz_nelkul(forditas), sigla))
    return ki


def atment(eredmenyek):
    return K.atment(eredmenyek) and all(e != 'SERTES' for n, e, _ in eredmenyek if n in THAYER_GATOLO)
