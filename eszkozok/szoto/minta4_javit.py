"""F94.3 (FELADATOK #94): a felhasználó döntéseinek (2026-10-13) alkalmazása a 4. mintán: a hét [bizonytalan] sor
eldöntve, és (a teljes soronkénti átnézés után) mind a 113 sor `ellenorzes=felhasznalo`; a *felingereltessenek*
kategóriája a mintavételi réteg (ragos_nevszo) marad.

A hét sor `ellenorzes=felhasznalo` jelölést kap (a döntést a felhasználó hozta), a `[bizonytalan: …]` megjegyzés helyére
`[döntés: …]` kerül; a *mikre* `tovabbi_elfogadhato` mezője kiürül (azonos a szótári alakkal), a *felingereltessenek*
`kategoria`-ja `regies_ige`. A többi sor és mező változatlan (a szkript összeveti, eltérésnél megáll). Idempotens.

Használat: python eszkozok/szoto/minta4_javit.py"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(REPO, 'adat', 'szoto', 'szoto_minta_4_fuggetlen.tsv')
D = 'döntés: felhasználó, 2026-10-13'
DONTES = {
    'Filiszteusok': ({}, f'[{D}: a javaslat szerint — a népnév szótári alakja egyes számú (Filiszteus), a többes (Filiszteusok) további elfogadható alak: a kettős elfogadás a keresést védi]'),
    'Girzeusokat': ({}, f'[{D}: a javaslat szerint — Girzeus, további elfogadható: Girzeusok (mint a Filiszteusok)]'),
    'összegyűlekezének': ({}, f'[{D}: a javaslat szerint — régies összegyűlekezik, mai összegyülekezik, alapige gyülekezik]'),
    'elfeledték': ({}, f'[{D}: a javaslat szerint — elfeled / mai elfelejt, alapige feled; egy szó két alakja, DT130 (2)]'),
    'mikre': ({'tovabbi_elfogadhato': ''}, f'[{D}: szótári alak mi, mai ami (vonatkozó olvasat, Ján 13:29); a tovabbi_elfogadhato (mi) ürítve, mert azonos a szótári alakkal]'),
    'felingereltessenek': ({'kategoria': 'ragos_nevszo'}, f'[{D}: szenvedő olvasat, a javaslat szerint — felingereltetik, alapige ingerel; a kategória a mintavételi réteg (ragos_nevszo) marad: a korábbi regies_ige-átsorolás visszavonva]'),
    'bízott': ({}, f'[{D}: a javaslat szerint — bíz, további elfogadható bízik (H6680, „rábíz” olvasat)]'),
}
SZABAD = {'ellenorzes', 'indoklas', 'tovabbi_elfogadhato', 'kategoria'}


def main():
    sorok = open(P, encoding='utf-8').read().split('\n')
    if sorok[-1] == '':
        sorok = sorok[:-1]
    i = next(k for k, s in enumerate(sorok) if not s.startswith('#'))
    meta, fej, rek = sorok[:i], sorok[i].split('\t'), [s.split('\t') for s in sorok[i + 1:]]
    ix = {n: k for k, n in enumerate(fej)}
    eredeti = [list(r) for r in rek]
    talalt = set()
    for r in rek:
        a = r[ix['alak']]
        if a not in DONTES:
            continue
        talalt.add(a)
        mezok, megj = DONTES[a]
        for m, v in mezok.items():
            r[ix[m]] = v
        r[ix['ellenorzes']] = 'felhasznalo'
        ind = re.sub(r' ?\[bizonytalan: [^\]]*\]', '', r[ix['indoklas']])
        # a korábbi, azóta módosított döntés-szöveg cseréje (felingereltessenek: az átsorolás visszavonva)
        ind = re.sub(r' ?\[döntés: felhasználó, 2026-10-13: [^\]]*\]', '', ind) if megj not in ind else ind
        if megj not in ind:
            ind = ind + ' ' + megj
        r[ix['indoklas']] = ind
    if talalt != set(DONTES):
        sys.exit(f'HIBA: hiányzó sor: {set(DONTES) - talalt}')
    # 2. döntés (a felhasználó, 2026-10-13T15:10Z): mind a 113 sort soronként átnézte; a 106 sor változatlanul elfogadva
    for r in rek:
        r[ix['ellenorzes']] = 'felhasznalo'
    for r0, r1 in zip(eredeti, rek):
        for n in fej:
            if r0[ix[n]] != r1[ix[n]] and n != 'ellenorzes' and (n not in SZABAD or r0[ix['alak']] not in DONTES):
                sys.exit(f'HIBA: nem megengedett változás: {r0[0]} {n}')
    nf = sum(1 for r in rek if r[ix['ellenorzes']] == 'felhasznalo')
    meta = [('# allapot: független minta; mind a 113 sort a felhasználó soronként ellenőrizte (ellenorzes=felhasznalo); a mérés '
             '(meres.py --csak-felhasznalo --fuggetlen) mind a 113 soron. A strong a repó párosításából (5Móz, 1Sám, Péld, Ez); Mk, Ján, '
             'Róm, Jel nincs párosítva: üres. A kategoria a mintavételi réteg (SEMA 2.27)') if m.startswith('# allapot:') else m
            for m in meta]
    meta = [m for m in meta if not m.startswith('# dontes:') and not m.startswith('# ellenorzes-proveniencia:')] + [
        '# dontes: a 7 [bizonytalan] sor a felhasználó döntésével lezárva (2026-10-13), a további 106 sor változatlanul elfogadva; '
        f'felhasznalo {nf}, modell_ellenorizetlen {len(rek) - nf} (eszkozok/szoto/minta4_javit.py)',
        '# ellenorzes-proveniencia: scope=a 4. minta 113 sora és a K tábla 400 sora | forras=felhasználói átnézés, áttekintő oldal '
        '(https://claude.ai/artifact/PvJ8YFw3y561Nku1xwBdkr), 2026-10-13 | ts=2026-10-13T15:10Z']
    with open(P, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(meta + ['\t'.join(fej)] + ['\t'.join(r) for r in rek]) + '\n')
    print(f'felhasznalo {nf} / {len(rek)}')


if __name__ == '__main__':
    main()
