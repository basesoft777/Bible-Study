# -*- coding: utf-8 -*-
"""F123 ANTROP-001 új cikk, U2 — az orkesztrátor döntésének (2026-11-03) átvezetése két indoklásba
(a nem érintett sorok bájtra egyezésének kontrolljával, split('\\t'), CLAUDE.md):

  - Luk 9:55-56: az elutasítás oka, hogy a két szó nem egy mondatban áll; a csak-TR állás külön megjegyzés,
    a TR-mérce szerint önmagában nem kizáró ok;
  - Fil 1:27: az ok a Thayer G4151 2. és G5590 2. szakasza alapján, határesetként (a határkártya:
    naplok/HATAR_ANTROP-001.md K1, a felhasználóé).
Forrás: az orkesztrátor döntése a felhasználó felhatalmazásával: »az orkesztrátor vegye magához a döntéseket
és hozza is meg« (2026-11-03).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import F123_ANTROP2_u3_adat as U  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

INDOK = {
    'Luk 9:55-56': ('A két szó nem egy mondatban áll: a „minémű lélek van ti bennetek” és az „emberek lelkét” két külön '
                    'mondat, és a lélek az egyikben indulat, a másikban élet. Megjegyzés: a két szó csak a Károli '
                    'alapszövegében (Textus Receptus) áll, a kritikai kiadásokban nincs; a Textus Receptus mércéje '
                    'szerint ez önmagában nem kizáró ok.'),
    'Fil 1:27': ('A két szó nem megkülönböztető szerepben áll: az „egy lélekben, egy érzéssel” két párhuzamos tagja a '
                 'közösség egységét fejezi ki, nem az ember két belső rétegét különbözteti meg. A Thayer-szótár a '
                 'πνεῦμα második jelentésénél megjegyzi, hogy itt a ψυχή helyén „szív” is állhatna, a ψυχή-t pedig az '
                 'érzelmek székhelye jelentés alá, az ApCsel 4:32 mellé sorolja (adat/thayer_szakaszok.tsv, G4151 -/2/-, '
                 'G5590 -/2/-). Határeset: a Mária-ének (Luk 1:46–47) mellérendelt tagjai bent vannak.'),
}


def mod(m, ix):
    m[ix['indoklas']] = INDOK[m[ix['igehely']]]


if __name__ == '__main__':
    U.egy_sor('jeloltek.tsv', 'id\t', lambda m, ix: m[0] == U.ID and m[ix['igehely']] in INDOK
              and m[ix['jelolt_tipus']] == 'elofordulas', mod, varhato=2)
