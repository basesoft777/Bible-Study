#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORDITAS_P4_ellenoriz.py -- FORDITAS_PILOT_BRIEF.md v1, FP4: a brief SS1. het
gepi ellenorzese a naplok/FORDITAS_P3_kimenet.tsv minden (szocikk, modell)
soran.

Ellenorzesek (SS1):
  1. gorog/heber betus szakaszok multihalmaza == a forrase
  2. fejezet:vers szampar multihalmaza == a forrase
  3. minden konyvroviditess a forditasban szerepel a Karoli-roviditeslistaban
     (az apokrif/deuterokanonikus konyvek -- amelyeknek nincs Karoli-alakjuk --
     kulon megengedett listan vannak, l. APOKRIF_KIVETEL)
  4. nincs Markdown-formazas (*, _, #) es nincs UJ zarojeles betoldas
     (a zarojel-parok szama a forditasban <= a forraseval)
  5. a G5 ideiglenes terminologia serulese (a forrasban szereplo angol
     rovidites/szo sem a vart magyar megfelelovel nem szerepel a forditasban,
     SEM a bizonytalan_feloldasok listajan nem all)
  6. hosszarany (forditas/forras karakterszam) 0.8-1.6 kozott -- CSAK JELZES,
     nem szamit a RENDBEN/SERTES aranyba
  7. JSON-sema ervenyes -- a FORDITAS_P3_kimenet.tsv "HIBA:" -kezdetu sorai
     ezen elbuknak, a tobbi mar a fordit.py-ban ervenyesitve volt

Kimenet: naplok/FORDITAS_P4_ellenorzes.tsv (strong, csoport, modell,
ellenorzes, eredmeny, reszlet) -- eredmeny: RENDBEN | SERTES | JELZES | HIBA.

    python naplok/FORDITAS_P4_ellenoriz.py
"""

import os
import re
import sys
import unicodedata
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAPLOK = os.path.join(REPO, 'naplok')

KIMENET_UT = os.path.join(NAPLOK, 'FORDITAS_P3_kimenet.tsv')
BIZONYTALAN_UT = os.path.join(NAPLOK, 'FORDITAS_P3_bizonytalan.tsv')
MINTA_UT = os.path.join(NAPLOK, 'FORDITAS_P1_minta.tsv')
TERMINOLOGIA_UT = os.path.join(NAPLOK, 'FORDITAS_P_terminologia.tsv')
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
KAROLI_UT = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')

ELLENORZES_UT = os.path.join(NAPLOK, 'FORDITAS_P4_ellenorzes.tsv')
ELLENORZES_FEJLEC = ['strong', 'csoport', 'modell', 'ellenorzes', 'eredmeny', 'reszlet']

# A Karoli-Biblia nem tartalmazza az apokrif/deuterokanonikus konyveket, ezert
# ezeknek nincs Karoli-roviditesuk -- a forditas jogosan hagyja valtozatlanul
# az angol/latin alaku roviditest (l. a Thayer-forras sajat hivatkozasai:
# Wis., Sir., Macc., Baruch stb.). Ez a lista NEM a forrasban elofordulo
# osszes nem-STEPBible-alak roviditest sorolja fel (azok tobbsege csak a
# Thayer sajat, STEPBible-tol elutero konyvrovidites-stilusa -- pl. "Joh"
# "Jhn" helyett -- ami az 1-3. ellenorzest NEM erinti, mert az a FORDITAS,
# nem a forras roviditeseit vizsgalja), csak azokat, amelyeknek valoban
# nincs Karoli-megfeleloje.
APOKRIF_KIVETEL = {
    'Wis', 'Wisdom', 'Sir', 'Sirach', 'Macc', 'Baruch', 'Bar', 'Tob', 'Tobit',
    'Jdt', 'Judith', 'Sap',
    # magyar forditasban megjeleno alakjaik (a modellek nemelyike ezeket is
    # leforditotta, nem csak atemelte -- mindket valasztas elfogadhato, mert
    # egyiknek sincs hivatalos Karoli-roviditese)
    'Bölcs', 'Bölcsesség', 'Báruk', 'Makk', '1Makk', '2Makk', 'Sirák', 'Tóbiás', 'Judit',
}

GOROG_HEBER_MINTA = re.compile(
    r'[Ͱ-Ͽἀ-῿̀-ͯ]+|[֐-׿]+'
)
VERS_MINTA = re.compile(r'\d{1,3}:\d{1,3}')
KONYV_ROVIDITES_MINTA = re.compile(
    r'\b([1-3]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüűA-Za-z]*)\.?\s+\d{1,3}:\d{1,3}'
)
MARKDOWN_MINTA = re.compile(r'[*_#]')


def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def tsv_dict_sorok(ut):
    fejlec = None
    for m in tsv_sorok(ut):
        if m[0].startswith('#'):
            continue
        if fejlec is None:
            fejlec = m
            continue
        yield dict(zip(fejlec, m))


def tsv_ir(ut, fejlec, sorok):
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(fejlec) + '\n')
        for sor in sorok:
            fh.write('\t'.join(str(sor.get(mezo, '')) for mezo in fejlec) + '\n')


def betolt():
    thayer = {r['Strong_padded']: r['Teljes_szocikk'] for r in tsv_dict_sorok(THAYER_UT)}
    karoli_halmaz = {r['Magyar rövidítés'] for r in tsv_dict_sorok(KAROLI_UT)}
    terminologia = list(tsv_dict_sorok(TERMINOLOGIA_UT))
    csoport = {r['strong']: r['csoport'] for r in tsv_dict_sorok(MINTA_UT)}

    bizonytalan = {}  # (strong, modell) -> [rovidites, ...]
    if os.path.exists(BIZONYTALAN_UT):
        for r in tsv_dict_sorok(BIZONYTALAN_UT):
            kulcs = (r['strong'], r['modell'])
            bizonytalan[kulcs] = [x.strip() for x in r['bizonytalan_feloldasok'].split(';') if x.strip()]

    kimenet = list(tsv_dict_sorok(KIMENET_UT))
    return thayer, karoli_halmaz, terminologia, csoport, bizonytalan, kimenet


def _ekezet_nelkul(token):
    """A gorog ekezet a mondatbeli helyzettol fuggoen valtozhat (pl. mondat
    vegen oxeia -> baria, l. τό/τὸ), es a forras/forditas ugyanazt a szot
    mas mondatpoziciobol idezheti -- ez NEM tartalmi elteres. NFD-bontas
    utan az osszes nemszavas (Mn kategoriaju) jelolot -- ekezetet, lehelet-
    jelet -- levesszuk, csak az alapbetuket hasonlitjuk."""
    return ''.join(ch for ch in unicodedata.normalize('NFD', token)
                    if unicodedata.category(ch) != 'Mn')


def ellenoriz_1_gorog_heber(forras, forditas):
    f_forras = Counter(_ekezet_nelkul(t) for t in GOROG_HEBER_MINTA.findall(forras))
    f_forditas = Counter(_ekezet_nelkul(t) for t in GOROG_HEBER_MINTA.findall(forditas))
    if f_forras == f_forditas:
        return 'RENDBEN', ''
    hianyzik = f_forras - f_forditas
    tobblet = f_forditas - f_forras
    reszlet = []
    if hianyzik:
        reszlet.append('hianyzik: ' + ', '.join('%s×%d' % (k, v) for k, v in hianyzik.items()))
    if tobblet:
        reszlet.append('tobblet: ' + ', '.join('%s×%d' % (k, v) for k, v in tobblet.items()))
    return 'SERTES', '; '.join(reszlet)


def ellenoriz_2_versszam(forras, forditas):
    f_forras = Counter(VERS_MINTA.findall(forras))
    f_forditas = Counter(VERS_MINTA.findall(forditas))
    if f_forras == f_forditas:
        return 'RENDBEN', ''
    hianyzik = f_forras - f_forditas
    tobblet = f_forditas - f_forras
    reszlet = []
    if hianyzik:
        reszlet.append('hianyzik: ' + ', '.join('%s×%d' % (k, v) for k, v in hianyzik.items()))
    if tobblet:
        reszlet.append('tobblet: ' + ', '.join('%s×%d' % (k, v) for k, v in tobblet.items()))
    return 'SERTES', '; '.join(reszlet)


def ellenoriz_3_karoli_roviditesek(forditas, karoli_halmaz):
    talalatok = {m.group(1) for m in KONYV_ROVIDITES_MINTA.finditer(forditas)}
    ismeretlen = sorted(t for t in talalatok if t not in karoli_halmaz and t not in APOKRIF_KIVETEL)
    if not ismeretlen:
        return 'RENDBEN', ''
    return 'SERTES', 'ismeretlen roviditesek: ' + ', '.join(ismeretlen)


def ellenoriz_4_formazas(forras, forditas):
    hibak = []
    md_talalat = MARKDOWN_MINTA.findall(forditas)
    if md_talalat:
        hibak.append('Markdown-jel: ' + ''.join(sorted(set(md_talalat))))
    if forditas.count('(') > forras.count('('):
        hibak.append('tobb nyito zarojel a forditasban (%d) mint a forrasban (%d) -- lehetseges betoldas'
                      % (forditas.count('('), forras.count('(')))
    if not hibak:
        return 'RENDBEN', ''
    return 'SERTES', '; '.join(hibak)


def _magyar_alak_mintaja(magyar):
    """A magyar toldalekolas a rovid vegzo maganhangzot megnyujtja
    (Septuaginta -> Septuagintaban/Septuagintat), ezert az egyszeru
    reszlanc-egyezes hamis SERTES-t adna: a torzs vegen levo 'a'/'e'
    betut karakterosztallyal ('[aá]'/'[eé]') helyettesitjuk, a tobbi
    betut szo szerint vesszuk."""
    if magyar and magyar[-1] in 'ae':
        csere = {'a': '[aá]', 'e': '[eé]'}[magyar[-1]]
        return re.compile(re.escape(magyar[:-1]) + csere)
    return re.compile(re.escape(magyar))


def ellenoriz_5_terminologia(forras, forditas, terminologia, bizonytalan_lista):
    serult = []
    for t in terminologia:
        angol = t['angol']
        if angol not in forras:
            continue
        if _magyar_alak_mintaja(t['magyar']).search(forditas):
            continue
        if any(angol.rstrip('.') == b.rstrip('.') for b in bizonytalan_lista):
            continue
        serult.append('%s -> %s hianyzik' % (angol, t['magyar']))
    if not serult:
        return 'RENDBEN', ''
    return 'SERTES', '; '.join(serult)


def ellenoriz_6_hosszarany(forras, forditas):
    if not forras:
        return 'JELZES', 'ures forras'
    arany = len(forditas) / len(forras)
    if 0.8 <= arany <= 1.6:
        return 'RENDBEN', '%.2f' % arany
    return 'JELZES', '%.2f (a 0.8-1.6 savon kivul)' % arany


def main():
    thayer, karoli_halmaz, terminologia, csoport, bizonytalan, kimenet = betolt()

    sorok = []
    for r in kimenet:
        strong = r['strong']
        modell = r['modell']
        forras = thayer.get(strong, '')
        forditas = r['forditas_hu']
        cs = csoport.get(strong, '?')

        if forditas.startswith('HIBA:'):
            for nev in ('1_gorog_heber', '2_versszam', '3_karoli_roviditesek',
                        '4_formazas', '5_terminologia', '6_hosszarany', '7_json_sema'):
                sorok.append({'strong': strong, 'csoport': cs, 'modell': modell,
                              'ellenorzes': nev, 'eredmeny': 'HIBA', 'reszlet': forditas})
            continue

        sorok.append({'strong': strong, 'csoport': cs, 'modell': modell,
                      'ellenorzes': '7_json_sema', 'eredmeny': 'RENDBEN', 'reszlet': ''})

        bizonytalan_lista = bizonytalan.get((strong, modell), [])

        for nev, fv in (
            ('1_gorog_heber', lambda: ellenoriz_1_gorog_heber(forras, forditas)),
            ('2_versszam', lambda: ellenoriz_2_versszam(forras, forditas)),
            ('3_karoli_roviditesek', lambda: ellenoriz_3_karoli_roviditesek(forditas, karoli_halmaz)),
            ('4_formazas', lambda: ellenoriz_4_formazas(forras, forditas)),
            ('5_terminologia', lambda: ellenoriz_5_terminologia(forras, forditas, terminologia, bizonytalan_lista)),
            ('6_hosszarany', lambda: ellenoriz_6_hosszarany(forras, forditas)),
        ):
            eredmeny, reszlet = fv()
            sorok.append({'strong': strong, 'csoport': cs, 'modell': modell,
                          'ellenorzes': nev, 'eredmeny': eredmeny, 'reszlet': reszlet})

    tsv_ir(ELLENORZES_UT, ELLENORZES_FEJLEC, sorok)
    print('irva: %s (%d sor)' % (ELLENORZES_UT, len(sorok)))

    # Osszesito: atmenesi arany a PASS/FAIL ellenorzeseken (1,2,3,4,5,7) --
    # a 6 (hosszarany) csak jelzes, es a HIBA sorok kulon szamitanak.
    pass_fail_nevek = {'1_gorog_heber', '2_versszam', '3_karoli_roviditesek',
                        '4_formazas', '5_terminologia', '7_json_sema'}
    modellenkent = {}
    for s in sorok:
        if s['ellenorzes'] not in pass_fail_nevek:
            continue
        m = s['modell']
        d = modellenkent.setdefault(m, {'RENDBEN': 0, 'SERTES': 0, 'HIBA': 0})
        d[s['eredmeny']] = d.get(s['eredmeny'], 0) + 1

    print('\n=== atmenesi arany modellenkent (1,2,3,4,5,7 ellenorzes egyutt) ===')
    for m in sorted(modellenkent):
        d = modellenkent[m]
        osszes = d['RENDBEN'] + d['SERTES'] + d['HIBA']
        print('  %-32s RENDBEN %3d | SERTES %3d | HIBA %3d | atmeneti arany (RENDBEN a nem-HIBA felett) %.1f%%'
              % (m, d['RENDBEN'], d['SERTES'], d['HIBA'],
                 100.0 * d['RENDBEN'] / (d['RENDBEN'] + d['SERTES']) if (d['RENDBEN'] + d['SERTES']) else 0.0))


if __name__ == '__main__':
    main()
