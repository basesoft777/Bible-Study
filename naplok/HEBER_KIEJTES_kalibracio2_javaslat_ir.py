"""A 2. kalibráló minta kézi javaslat-táblájának megírása
(naplok/HEBER_KIEJTES_kalibracio2_javaslat.tsv). A héber kulcsot a mintából
(naplok/HEBER_KIEJTES_kalibracio2_minta.tsv) veszi sorszám szerint.

Proveniencia: manual — a session ítélete. A javaslat a DT-F131y konvencióit
követi (ס/שׂ = sz, ח = ch, kámec á a kivételekkel, R3 sevá torokhang előtt
kiejtett, R5 szókezdő begadkefat, Jahve, jerúsálajim); ahol ez eltér a
tibériási olvasattól, a megjegyzés jelzi.
TSV: split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINTA = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kalibracio2_minta.tsv')
KI = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kalibracio2_javaslat.tsv')

R3 = 'a DT-F131y R3 szerint kiejtett sevá (torokhang előtt); a tibériási olvasatban néma'
R5 = 'a DT-F131y R5 szerint kemény (a tő kezdőbetűje); a pontozás lágyat jelöl'

# sorszám: (gépi-ellenőrzés, javaslat, alternatíva, alternatíva2, megjegyzés)
J = {
    1: ('vajjisszácherú', 'vajjisszácherú', 'vajjisszochrú', 'vajjiszácherú', ''),
    2: ('rechullátchá', 'rechullátechá', 'rechulátechá', '', 'kámec után a sevá kiejtett (rəḵullāṯəḵā); a szövegben nincs meteg'),
    3: ('máleá', 'máleá', 'málá', 'molá', ''),
    4: ('jásevú', 'jásevú', 'jásvú', 'josvú', ''),
    5: ('cidkátechá', 'cidkátechá', 'cidkátchá', 'cidkatechá', ''),
    6: ('haccáhorajim', 'haccáhorajim', 'haccohorajim', 'hacáhorajim', 'hátef-kámec előtt a tibériási olvasat o (haccohorajim); a DT-F131y R2 szerint á'),
    7: ('jikrá', 'jikrá', 'jikerá', 'jikra', ''),
    8: ('biseól', 'biseól', 'bisól', 'biseol', R3),
    9: ('liseól', 'liseól', 'lisól', 'liseol', R3),
    10: ('ekrá', 'ekrá', 'ekerá', 'ekra', ''),
    11: ('kireú', 'kireú', 'kirú', 'kireu', R3),
    12: ('liseólá', 'liseólá', 'lisólá', 'liseóla', R3),
    13: ('póléach', 'póléach', 'fóléach', 'póleach', R5),
    14: ('úverúach', 'úverúach', 'úberúach', 'úvrúach', ''),
    15: ('rúach', 'rúach', 'rúcha', 'ruach', ''),
    16: ('úvókéa', 'úvókéa', 'úbókéa', 'úvókea', ''),
    17: ('hagbéah', 'hagbéah', 'hagbéa', 'hagebéah', ''),
    18: ('hannefilím', 'hannefilím', 'hanefilím', 'hannefílím', ''),
    19: ('vajjikreú', 'vajjikreú', 'vajikreú', 'vajjikrú', ''),
    20: ('iccevónéch', 'iccevónéch', 'icevónéch', 'iccevónech', ''),
    21: ('úméiccevón', 'úméiccevón', 'uméiccevón', 'úméicevón', ''),
    22: ('úmittehómót', 'úmittehómót', 'úmitehómót', 'umittehómót', ''),
    23: ('vajjiven', 'vajjiven', 'vajiven', 'vajjiben', ''),
    24: ('veim', 'veim', 'veím', 've-im', ''),
    25: ('gam', 'gam', 'gám', 'gam-', ''),
    26: ('avdé', 'avdé', 'abdé', 'avedé', ''),
    27: ('vejad', 'vejad', 'bejad', 'vejád', ''),
    28: ('kó', 'kó', 'chó', 'kóh', R5),
    29: ('kullám', 'kullám', 'chullám', 'kulám', R5),
    30: ('bór', 'bór', 'vór', 'bor', R5),
    31: ('vechá', 'vechá', 'bechá', 'vecha', ''),
    32: ('veappí', 'veappí', 'beappí', 'veapí', ''),
    33: ('ászón', 'ászón', 'ászon', 'ásón', ''),
    34: ('lemirmász', 'lemirmász', 'lemirmás', 'lemiremász', ''),
    35: ('jisszá', 'jisszá', 'jiszá', 'jissá', ''),
    36: ('jászúr', 'jászúr', 'jásúr', 'jaszúr', ''),
    37: ('tószéf', 'tószéf', 'tószef', 'tósef', ''),
    38: ('seól', 'seól', 'sól', 'seol', ''),
    39: ('seólá', 'seólá', 'seóla', 'seolá', ''),
    40: ('ráat', 'ráat', 'raat', 'ráát', ''),
    41: ('káráú', 'káráú', 'kárú', 'karaú', ''),
    42: ('refáím', 'refáím', 'refaím', 'rafáím', ''),
    43: ('semó', 'semó', 'smó', 'semo', ''),
    44: ('úvesém', 'úvesém', 'úbesém', 'uvsém', ''),
    45: ('leháráfá', 'leháráfá', 'leháráfa', 'leharáfá', ''),
    46: ('bené', 'bené', 'vené', 'bné', ''),
    47: ('háráfá', 'háráfá', 'hárafá', 'háráfa', ''),
    48: ('tehómót', 'tehómót', 'tehomot', 'thómót', ''),
    49: ('lesachét', 'lesachét', 'lesahét', 'lessachét', ''),
    50: ('seálá', 'seálá', 'sálá', 'seála', ''),
}


def main():
    sorok = [l.rstrip('\n').split('\t') for l in open(MINTA, encoding='utf-8') if not l.startswith('#')]
    fej, sorok = sorok[0], sorok[1:]
    ix = {k: i for i, k in enumerate(fej)}
    ki = ['# Kézi javaslat-tábla a 2. kalibráló mintához (HEBER_KIEJTES_kalibracio.py --menet 2).',
          '# scope=naplok/HEBER_KIEJTES_kalibracio2_minta.tsv | forras=manual (a session ítélete, DT-F131y konvenciói) | ts=2026-10-30',
          '\t'.join(['heber', 'sorszam', 'javaslat', 'alternativa', 'alternativa2', 'megjegyzes'])]
    for r in sorok:
        n = int(r[ix['sorszam']])
        gepi, jav, alt, alt2, megj = J[n]
        if r[ix['gepi']] != gepi:
            raise SystemExit(f'{n}. sor: a minta gépi alakja {r[ix["gepi"]]!r}, a táblában {gepi!r}')
        ki.append('\t'.join([r[ix['heber']], str(n), jav, alt, alt2, megj]))
    if len(sorok) != len(J):
        raise SystemExit(f'sorszám-eltérés: minta {len(sorok)}, tábla {len(J)}')
    with open(KI, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')
    print(f'{len(sorok)} sor -> {KI}')


if __name__ == '__main__':
    main()
