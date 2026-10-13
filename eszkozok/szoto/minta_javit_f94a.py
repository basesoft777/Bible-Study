"""F94.0f (FELADATOK #94): a felhasználó DT-F94a/DT-F94b döntésének (2026-10-13) alkalmazása az 1. és 2. mintán.

Csak a döntésben megnevezett mezőket írja; minden más mező bájtra változatlan (a szkript a változás előtt és után
összeveti a sorokat, és eltérésnél megáll). Idempotens: a már javított sort nem írja újra.
Az `ellenorzes` csak a döntésben felsorolt hét sornál lesz `felhasznalo` (vettetének, születének, helyezteté,
tudatá, ki, elvesznek, seregeknek); az E-7 és E-8 formai javítása az `ellenorzes`-t nem változtatja.

Használat: python eszkozok/szoto/minta_javit_f94a.py"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
M1 = os.path.join(REPO, 'adat', 'szoto', 'szoto_minta_1_fejlesztes.tsv')
M2 = os.path.join(REPO, 'adat', 'szoto', 'szoto_minta_2_fejlesztes.tsv')
D = 'döntés 2026-10-13 (DT-F94a)'

# Soronkénti döntések: alak -> {mező: érték}; az 'indoklas+' a meglévő indoklás végére kerül.
JAVIT = {
    M1: {
        'születének': {'ellenorzes': 'felhasznalo', 'indoklas+': f'[{D}: változatlan, önálló -ik-es ige, nem szenvedő képzés]'},
        'helyezteté': {'szotari_alak': 'helyeztet', 'szotari_alak_mai': 'helyez', 'alapige': 'helyez', 'ellenorzes': 'felhasznalo',
                       'indoklas+': f'[{D}: nem műveltető (H5414 Qal); mai alak és alapige: helyez; a -tat/-tet nem általános szabály, alakonként dől el]'},
        'ki': {'tovabbi_elfogadhato': 'aki', 'ellenorzes': 'felhasznalo',
               'indoklas+': f'[{D}: három olvasat — igekötő (1Móz 2:5 „hajtott ki”), kérdő névmás (Ézs 41:26 „Ki jelenté meg”), '
                            f'vonatkozó névmás (1Móz 2:5 „ki a földet művelje”, mai alakja: aki)]'},
    },
    M2: {
        'vettetének': {'alapige': 'vet', 'ellenorzes': 'felhasznalo', 'indoklas+': f'[{D}: szenvedő képzett igealak, a C) szerint; alapige: vet]'},
        'tudatá': {'alapige': 'tud', 'ellenorzes': 'felhasznalo', 'indoklas+': f'[{D}: valódi műveltető (H8085 Hif’íl), a C) szerint; alapige: tud]'},
        'elvesznek': {'tovabbi_elfogadhato': 'elvesz', 'alapige': 'vész',
                      'indoklas+': f'[{D}: a sor elvész marad (Ézs 41:11, H0006); a kétértelmű alak másik olvasata: elvesz]'},
        'seregeknek': {'tovabbi_elfogadhato': 'Seregek', 'ellenorzes': 'felhasznalo',
                       'indoklas+': '[döntés 2026-10-13 (DT-F94b): sereg, további elfogadható Seregek; a kisbetűs alak a Károliban mindkét '
                                    'jelentésben áll (a 85 kisbetűs seregek…-tokenből 64 Ur-/Isten- előtt); manual megfigyelés: Ézs 44:6 '
                                    '„a seregeknek … Ura” — a szó köznév, a cím a szókapcsolat]'},
    },
}
# E-7: az igekötős igék alapigéje (a napló 5. szakaszának javaslat-oszlopa szerint), az ellenorzes változatlan
E7 = {'kiterjeszté': 'terjeszt', 'megváltá': 'vált', 'megvígasztalá': 'vígasztal', 'kifeszíté': 'feszít', 'megerősíté': 'erősít',
      'megalapítá': 'alapít', 'elszéleszté': 'széleszt', 'megrémülének': 'rémül', 'elhamvadának': 'hamvad',
      'bekövetkezének': 'következik', 'meglennének': 'lesz', 'elhagynának': 'hagy', 'megszégyenülnek': 'szégyenül',
      'elvesznek': 'vész', 'leborulnak': 'borul', 'megértsék': 'ért'}
IGEKAT = {'regies_ige', 'ige_mai_alak'}


def olvas(p):
    sorok = open(p, encoding='utf-8').read().split('\n')
    if sorok[-1] == '':
        sorok = sorok[:-1]
    fejsor = next(i for i, s in enumerate(sorok) if not s.startswith('#'))
    return sorok[:fejsor], sorok[fejsor].split('\t'), [s.split('\t') for s in sorok[fejsor + 1:]]


def main():
    osszes = []
    for p in (M1, M2):
        meta, fej, rek = olvas(p)
        ix = {n: i for i, n in enumerate(fej)}
        eredeti = [list(r) for r in rek]
        valtozas = []
        for r in rek:
            a = r[ix['alak']]
            # E-8 (csak az 1. minta): az alapige ürítése, ha azonos a mai szótári alakkal (nem ige / igekötő nélküli ige)
            if p == M1 and r[ix['alapige']] and r[ix['alapige']] == r[ix['szotari_alak_mai']]:
                if a == 'helyezteté':
                    pass  # a döntés külön adja (alapige: helyez)
                else:
                    valtozas.append((a, 'alapige', r[ix['alapige']], ''))
                    r[ix['alapige']] = ''
            if p == M2 and a in E7 and r[ix['alapige']] != E7[a]:
                valtozas.append((a, 'alapige', r[ix['alapige']], E7[a]))
                r[ix['alapige']] = E7[a]
            for mezo, ertek in JAVIT[p].get(a, {}).items():
                if mezo == 'indoklas+':
                    if ertek not in r[ix['indoklas']]:
                        uj = (r[ix['indoklas']] + ' ' if r[ix['indoklas']] else '') + ertek
                        valtozas.append((a, 'indoklas', '…', '+' + ertek[:40] + '…'))
                        r[ix['indoklas']] = uj
                elif r[ix[mezo]] != ertek:
                    valtozas.append((a, mezo, r[ix[mezo]], ertek))
                    r[ix[mezo]] = ertek
        # ellenőrzés: csak a megengedett mezők változtak, a sorrend és a sorszám azonos
        for r0, r1 in zip(eredeti, rek):
            for n in fej:
                if r0[ix[n]] != r1[ix[n]] and n not in ('alapige', 'szotari_alak', 'szotari_alak_mai', 'tovabbi_elfogadhato', 'ellenorzes', 'indoklas'):
                    sys.exit(f'HIBA: nem megengedett mező változott: {r0[0]} {n}')
            if '\t' in ''.join(r1):
                sys.exit('HIBA: tab a mezőben')
        assert len(eredeti) == len(rek)
        nf = sum(1 for r in rek if r[ix['ellenorzes']] == 'felhasznalo')
        for i, m in enumerate(meta):
            if m.startswith('# allapot:'):
                elotag = m.split('; felhasznalo ')[0]
                if 'DT-F94a' not in elotag:
                    elotag += '; javítva a DT-F94a/b szerint (F94.0f, eszkozok/szoto/minta_javit_f94a.py)'
                meta[i] = f'{elotag}; felhasznalo {nf}, modell_ellenorizetlen {len(rek) - nf}'
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(meta + ['\t'.join(fej)] + ['\t'.join(r) for r in rek]) + '\n')
        print(f'{os.path.basename(p)}: {len(valtozas)} mezőváltozás, felhasznalo {nf}')
        osszes += [(os.path.basename(p),) + v for v in valtozas]
    for v in osszes:
        if v[2] != 'alapige' or v[1] in ('helyezteté', 'vettetének', 'tudatá'):
            print('  ', ' | '.join(v))


if __name__ == '__main__':
    main()
