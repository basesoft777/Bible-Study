"""A kalibráló minta kézi javaslat-táblájának megírása
(naplok/HEBER_KIEJTES_kalibracio_javaslat.tsv). A héber kulcsot a mintából
(naplok/HEBER_KIEJTES_kalibracio_minta.tsv) veszi sorszám szerint, így a
héber alakot nem kell begépelni.

Proveniencia: manual — a javaslat és az alternatívák a session héber
nyelvtani ítéletei (nem lekérdezés). Konvenció a javaslatban: ס és שׂ = sz,
a szókezdő begadkefatról a pontozás dönt, ח = ch; a ketiv/qere a qere szerint.
TSV: split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINTA = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kalibracio_minta.tsv')
KI = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kalibracio_javaslat.tsv')

# sorszám: (gépi-ellenőrzés, javaslat, alternatíva, alternatíva2, megjegyzés ha bizonytalan)
# A gépi-ellenőrzés a minta gépi oszlopa; ha eltér, a szkript megáll (a sorszámozás elcsúszott).
J = {
    1: ('horfáím', 'hárefáím', 'hárfáím', '', ''),
    2: ('vehárefáím', 'vehárefáím', 'vehárfáím', 'vehorfáím', ''),
    3: ('bechozká', 'bechozká', 'becházeká', 'becházká', ''),
    4: ('hojtá', 'hájetá', 'hájtá', '', ''),
    5: ('sibbolím', 'sibbolím', 'sibbólím', 'sibolím', ''),
    6: ('áháló', 'oholó', 'áholó', '', 'a hé alatt sevá és kámec együtt áll (a hátef-kámec szokatlan kódolása); az ohŏlô olvasat a valószínű'),
    7: ('nistárenú', 'nisztárnú', 'nisztárenú', '', 'pauzális alak: a hangsúlyos zárt szótag után a sevát némának tartom, a STEP kiejtettnek írja'),
    8: ('bisól', 'visól', 'viseól', '', ''),
    9: ('besimchá', 'vesimchá', 'vesimechá', '', ''),
    10: ('vekirú', 'vekirú', 'vekireú', 'vekiru', ''),
    11: ('nischátá', 'nischátá', 'nisechátá', 'nishátá', ''),
    12: ('kithómót', 'kithómót', 'kitehómót', 'kit-hómót', ''),
    13: ('hannefílím', 'hannefílím', 'hanefílím', 'hannefilím', ''),
    14: ('jehósua', 'jehósua', 'jehósúa', 'jehósuá', ''),
    15: ('hammizbéach', 'hammizbéach', 'hamizbéach', 'hammizbécha', ''),
    16: ('tacmíach', 'tacmíach', 'tacmícha', 'tacemíach', ''),
    17: ('mizbéach', 'mizbéach', 'mizbécha', 'mizebéach', ''),
    18: ('jánúach', 'jánúach', 'jánúcha', 'janúach', ''),
    19: ('réach', 'réach', 'récha', 'réjach', ''),
    20: ('úmittehóm', 'úmittehóm', 'umittehóm', 'úmitehóm', ''),
    21: ('chajjím', 'chajjím', 'chajím', 'hajjím', ''),
    22: ('vajjikrá', 'vajjikrá', 'vajikrá', 'vajjikerá', ''),
    23: ('chajjá', 'chajjá', 'chajá', 'hajjá', ''),
    24: ('misseól', 'misseól', 'miseól', 'missól', ''),
    25: ('chattát', 'chattát', 'chatát', 'hattát', ''),
    26: ('úvírúsálim', 'úvírúsálajim', 'úvírúsálém', '', 'ketiv/qere: a mássalhangzós szöveg (ketiv) „Jerúsálém”-et, a pontozás (qere) „Jerúsálajim”-ot ad'),
    27: ('jerúsálim', 'jerúsálajim', 'jerúsálém', '', 'ketiv/qere: l. az előző sort'),
    28: ('JHVH', 'JHVH', 'Elóhím', 'Jahve', 'az „Adonáj JHVH” kapcsolatban a pontozás (qere) Elóhímot olvastat; a lapon a JHVH-konvenció áll'),
    29: ('JHVH', 'JHVH', 'Adonáj', 'Jahve', ''),
    30: ('JHVH', 'JHVH', 'Adonáj', 'Jahve', ''),
    31: ('bené', 'vené', 'bné', '', ''),
    32: ('besém', 'vesém', 'vesem', '', ''),
    33: ('vachamas', 'vachamasz', 'vahamasz', '', 'a H2555 lemmája kézi kivétel („hámás”, D36: ח → h); kérdés, hogy ez a ragozott alakokra is vonatkozik-e'),
    34: ('att', 'at', 'atte', '', 'a szóvégi תְּ dágessel: a hagyományos olvasat „at”, a régebbi kiejtés „atte”'),
    35: ('af', 'af', 'ap', 'áf', ''),
    36: ('úfen', 'úfen', 'úpen', 'ufen', ''),
    37: ('kisól', 'chisól', 'chiseól', '', ''),
    38: ('kóhén', 'chóhén', 'kohén', '', ''),
    39: ('bismí', 'vismí', 'visemí', '', ''),
    40: ('bismó', 'vismó', 'visemó', '', ''),
    41: ('besálém', 'vesálém', 'vesalém', '', ''),
    42: ('becilló', 'vecilló', 'veciló', '', ''),
    43: ('berít', 'verít', 'brít', '', ''),
    44: ('vechámás', 'vechámász', 'vehámász', '', 'a H2555 kézi kivétele („hámás”, D36) a ragozott alakra is vonatkozhat'),
    45: ('hechámás', 'hechámász', 'hehámász', '', 'l. a 44. sort'),
    46: ('chámás', 'hámás', 'hámász', '', 'a jóváhagyott lemma-kiejtés „hámás” (D36); az sz-változat a ס-konvenciótól függ'),
    47: ('kisó', 'kiszó', 'kiszeó', '', ''),
    48: ('chamas', 'chamasz', 'hamasz', '', 'l. a 44. sort'),
    49: ('chasdechá', 'chaszdechá', 'haszdechá', '', ''),
    50: ('hakkesef', 'hakkeszef', 'hakeszef', '', ''),
}


def main():
    sorok = [l.rstrip('\n').split('\t') for l in open(MINTA, encoding='utf-8') if not l.startswith('#')]
    fej, sorok = sorok[0], sorok[1:]
    ix = {k: i for i, k in enumerate(fej)}
    ki = ['# Kézi javaslat-tábla a kalibráló mintához (HEBER_KIEJTES_kalibracio.py).',
          '# scope=naplok/HEBER_KIEJTES_kalibracio_minta.tsv | forras=manual (a session nyelvtani ítélete) | ts=2026-10-30',
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
