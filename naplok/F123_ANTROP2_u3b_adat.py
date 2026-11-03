# -*- coding: utf-8 -*-
"""F123 ANTROP-001 új cikk, U3 — a lap saját átnézése utáni két adatjavítás (a nem érintett sorok bájtra
egyezésének kontrolljával, split('\\t'), CLAUDE.md):

  - adat/elofordulasok.tsv: a `megbizhatosag` `közepes` → `magas` az 1Thessz 5:23, a Zsid 4:12 és az 1Kor 2:14
    során: a 2026-08-i érték a TAHOT-hatókörön kívüli, kézi azonosításé volt; az U1 szópár-hálója a TAGNT-ben
    mindhárom versben igazolja a pár mindkét tagját (naplok/F123_teljesseg_ANTROP-001.md 1.). Az 1Kor 2:15
    `közepes` marad: a versben csak a melléknév áll, a pár a két vers ellentétében;
  - adat/jeloltek.tsv: az 1Pét 1:22 indoklása zárójelek nélkül (a generált kiejtés kettős zárójelet adott).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import F123_ANTROP2_u3_adat as U  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

MAGAS = {'1Thessz 5:23', 'Zsid 4:12', '1Kor 2:14'}
PET = ('A két szó nem megkülönböztető szerepben áll: a lelket Isten Lelke tisztítja meg, a görögben a ψυχή a '
       'megtisztított lélek, a πνεῦμα a tisztító Lélek, nem az ember két belső összetevője. A „Lélek által” szavak '
       'csak a Károli alapszövegében (Textus Receptus) állnak, a kritikai kiadásokban nincsenek.')


def mod_e(m, ix):
    assert m[ix['megbizhatosag']] == 'közepes'
    m[ix['megbizhatosag']] = 'magas'


def mod_j(m, ix):
    m[ix['indoklas']] = PET


if __name__ == '__main__':
    U.egy_sor('elofordulasok.tsv', 'id\t', lambda m, ix: m[0] == U.ID and m[ix['igehely']] in MAGAS, mod_e, varhato=3)
    U.egy_sor('jeloltek.tsv', 'id\t', lambda m, ix: m[0] == U.ID and m[ix['igehely']] == '1Pét 1:22'
              and m[ix['jelolt_tipus']] == 'elofordulas', mod_j)
