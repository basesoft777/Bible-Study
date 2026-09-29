"""BDB_etimologia_kezi_hatarok.tsv -- a 26 heber gerinc-token (D28) BDB-
szocikkeinek "nyelvi hatter" (etimologia/rokon-nyelvi anyag) hatar-
besorolasa negy kategoriaba (S9, D21, D28/D29 kiegeszitve; a hatarfelismero
regex F05b-ben javitva, l. lent a HATARJELOLTEK korul).

- gepi: a HATARJELOLTEK kozul a LEGKORABBAN illeszkedo minta hatarozza meg
  a vagast, ES a hatar a szocikk hosszanak legfeljebb 40%-anal van
  (BIZTONSAGI_KUSZOB). Ha egyik felteitel sem teljesul, a token NEM lehet
  gepi (l. lent).
- javaslat: nincs illeszkedo HATARJELOLT, VAGY a talalt hatar a szocikk
  40%-a utan van (tul bizonytalan ahhoz, hogy gepi legyen) -- KEZZEL
  kijelolt hatar, JOVAHAGYASRA VAR.
- jovahagyott: mint a `javaslat`, de a felhasznalo chat-dontessel mar
  jovahagyta (2026.09.29, l. naplok/SZOTAR_S1_7_jelentes.md) -- a
  JOVAHAGYOTT halmazban felsorolt Strongok. A H0430-at a felhasznalo
  eloszor ALLJ ala helyezte (a `Nes^l. c,)` hatarveg gyanus volt), majd
  a raw BDB.lexicon HTML-forras alapjan vegzett vizsgalat (a hatar
  teljes, nem csonka -- l. a jelentesben) utan kulon jova is hagyta.
- nem_targyalja: rovid szocikk, nincs kulon etimologiai/rokon-nyelvi
  bekezdes.

A "javaslat"/"jovahagyott" sorokat ez a szkript NEM szamitja ki
automatikusan -- a szoveget kezzel irt konstansok adjak (KEZI_JAVASLATOK),
mert az automatikus hatarfelismeres itt eppen azert bukik, mert a forras
nem kovetkezetes tagolasu; a kezi dontes indoklasat l. a SZOTAR_BRIEF.md
§3 S1.4 soraban es az S1.4 jelenteseben. A JOVAHAGYOTT halmaz csak azt
donti el, hogy a kimeneti allapot-cimke `javaslat` vagy `jovahagyott`
legyen -- a szoveg forrasa mindkettonel a KEZI_JAVASLATOK.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')
BDB_UT = os.path.join(KONKORDANCIA, 'BDB_teljes_unabridged.tsv')
KIMENET = os.path.join(KONKORDANCIA, 'BDB_etimologia_kezi_hatarok.tsv')

# F05b (2026.09.29) -- a fuggetlen-ellenor kimutatta, hogy a regi
# `—\s*1\s` minta (a) nem illeszkedik a "— 1." (pontos) alakra, ezert
# tobb tokennel (pl. H7121) az ELSO "— 1 " egyezes egy MELYEN a szocikk
# belsejeben levo, veletlenszeru "— 1 ..." reszre esett, nem a valodi
# hatarra; (b) nem veszi figyelembe, hogy sok ige-szocikknel az
# etimologia utan egy igealak-parad igma (Qal/Niph`al/Pi`el stb.) vagy
# egy igehelyes hasznalati/alak-felsorolas (pl. "— absolute ׳בּ Gen
# 4:25 +; construct ...") all, MIELOTT a szamozott "1." ertelem
# elkezdodne -- ez a resz sem etimologia, de a regi minta benne hagyta.
#
# HATARJELOLTEK: harom minta, a LEGKORABBAN (legkisebb pozicioban)
# illeszkedo szamit hatarnak, fuggetlenul attol, melyik minta talalta:
#   1) szamozott ertelem kezdete -- "— 1" vagy "— 1." (a pont opcionalis)
#   2) igealak-paradigma kezdete -- "— Qal" / "— Niph`al" / "— Pi`el" stb.
#   3) igehelyes hasznalati/alak-felsorolas kezdete -- "— [absolute/
#      construct] ׳X Gen ..." (a geresh-jelolt roevid Strong-utalas +
#      konyv-rovidites + versszam mintaja)
HATAR_SZAMOZOTT_RE = re.compile(r'—\s*1\.?\s')
HATAR_BINYAN_RE = re.compile(
    r'—\s*(?:Qal|Niph[`\']al|Pi[`\']el|Pu[`\']al|Hiph[`\']il|Hoph[`\']al|'
    r'Hithpa[`\']el|Hithpo[`\']el|Poel|Pilel|Hithpalpel)\b'
)
HATAR_HASZNALATI_RE = re.compile(
    r'—\s*(?:absolute\s+|construct\s+)?׳[֐-׿]{1,3}\s+[A-Z][a-z]{1,5}\.?\s*\d'
)
HATARJELOLTEK = (HATAR_SZAMOZOTT_RE, HATAR_BINYAN_RE, HATAR_HASZNALATI_RE)

# A gepi hatar csak akkor fogadhato el, ha a szocikk hosszanak legfeljebb
# ennyi szazalekanal van -- kulonben tul bizonytalan (pl. H7585-nel a
# valodi etimologia-bekezdes maga is hosszu, DE meg a kuszob alatt marad;
# ha egy jovobeli tokennel meg ez sem eleg, javaslat lesz belole, nem
# gepi -- l. hatar_keres()).
BIZTONSAGI_KUSZOB_SZAZALEK = 40.0


def hatar_keres(entry):
    """(pozicio, 'gepi'|'tul_hosszu'|'nincs_illeszkedes') -- a legkorabban
    illeszkedo HATARJELOLT pozicioja, es hogy a szocikk hosszanak
    BIZTONSAGI_KUSZOB_SZAZALEK-anal beluli-e."""
    pozicio = None
    for minta in HATARJELOLTEK:
        m = minta.search(entry)
        if m and (pozicio is None or m.start() < pozicio):
            pozicio = m.start()
    if pozicio is None:
        return None, 'nincs_illeszkedes'
    szazalek = 100.0 * pozicio / max(len(entry), 1)
    if szazalek > BIZTONSAGI_KUSZOB_SZAZALEK:
        return pozicio, 'tul_hosszu'
    return pozicio, 'gepi'

# D21 (a regi 24 tokenen) + D28/D29 (H8414 uj gepi, H0922 uj javaslat).
NEM_TARGYALJA = {'H0779', 'H2555', 'H5303', 'H6093', 'H7496', 'H7497'}

# Chat-dontessel jovahagyva 2026.09.29 (l. naplok/SZOTAR_S1_7_jelentes.md).
# A H0430-at kulon, utolagos vizsgalat utan hagyta jova a felhasznalo (a
# hatarveg "Nes^l. c,)" a nyers BDB.lexicon HTML-lel igazolva -- nem
# OCR-hiba/csonkolas).
JOVAHAGYOTT = {'H0430', 'H0922', 'H3678', 'H8004', 'H8034'}

# Kezi hatar-javaslatok -- a nyelvi_hatter szoveget a BDB_teljes_unabridged.tsv
# szocikkebol kezzel masoltuk ki, addig a pontig, ahol az erdemi etimologiai/
# rokon-nyelvi resz vegzodik es a hasznalati (usage) resz kezdodik. JOVAHAGYASRA
# VAR -- l. a menet vegi ⛔.
KEZI_JAVASLATOK = {
    'H0430': (
        'H430. elohim אֱלֹהִים noun masculine plural (feminine 1Kin 11:33; '
        'on number of occurrences of אֱלֹהִים אֱלוֺהַּ, אֵל, compare also Nes^l. c,)'
    ),
    'H3678': (
        'H3678. kisse or kisseh כִּסֵּה כִּסֵּא, noun masculine^2Sam 7:16 seat of '
        'honour, throne (Late Hebrew id.; Phoenician (plural) כרסים; Aramaic '
        'כּוּרְסְיָא, ; Biblical Aramaic כָּרְסֵא, Zinjirli כרסא DHM^Sendsch. 58. 44; '
        'Arabic ; but Assyrian kussu; perhaps Akkadian loan-word; ideogram '
        'iƒ GU. ZA, compare Dl^HWB 343)'
    ),
    'H8004': (
        'H8004. Shalem II. שָׁלֵם proper name, of a location abbreviated from '
        'יְרוּשָׁלַםִ (q. v.), and perhaps (Gunk Dr) intended as archaism Gen 14:18, '
        'compare (poetry) Psa 76:3 (|| צִיּוֺן); see Jos^Ant. i. 10, 2; ᵐ5 Σαλημ '
        'and (Psalms) εἰρήνη.'
    ),
    'H8034': (
        'H8034. shem I. שֵׁם noun masculine^2Sam 7:9 name (√ unknown; Thes '
        'שׁמה, compare Ba^ZMG xli (1887), 635; Lag^BN 160 ושׁם, Arabic brand, '
        'mark, compare RS^K 213, 303 ff. Kö^ii. 1. 104; Late Hebrew = '
        'Biblical Hebrew (especially הַשֵּׁם = יהוה); Phoenician שם Lzb^377; '
        'Assyrian šumu; Sabean סם Hom^Chr 124; Ethiopic Arabic ; Aramaic '
        'שְׁמָא שֵׁם, also שֻׁם שׁוּם, (Kö^ii. 1. 512), Old Aramaic, Palmyrene '
        'שם Lzb^377)'
    ),
    'H0922': (
        'H922. bohu בֹּהוּ noun [masculine] emptiness (on form see Ges^§ 84a, '
        '1 b Sta^§ 95, 198 a, on usage compare Lag^Or. ii. 60 f.) always '
        'with תֹּהוּ q. v.'
    ),
}


def read_tsv(path):
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    header = lines[0].split('\t')
    idx = {n: i for i, n in enumerate(header)}
    rows = {}
    for line in lines[1:]:
        if not line:
            continue
        cols = line.split('\t')
        rows[cols[idx['Strong_padded']]] = cols[idx['Teljes_szocikk']]
    return rows


def run(heber_tokenek):
    bdb = read_tsv(BDB_UT)
    sorok = []
    for token in heber_tokenek:
        entry = bdb.get(token, '')
        if token in NEM_TARGYALJA:
            sorok.append((token, 'nem_targyalja', '', str(len(entry)), '—'))
            continue
        pozicio, minosites = hatar_keres(entry) if entry else (None, 'nincs_illeszkedes')
        if minosites == 'gepi':
            nyelvi_hatter = entry[:pozicio].strip()
            sorok.append((token, 'gepi', nyelvi_hatter, str(len(entry)), str(pozicio)))
            continue
        if token in KEZI_JAVASLATOK:
            nyelvi_hatter = KEZI_JAVASLATOK[token]
            allapot = 'jovahagyott' if token in JOVAHAGYOTT else 'javaslat'
            sorok.append((token, allapot, nyelvi_hatter, str(len(entry)), str(len(nyelvi_hatter))))
            continue
        raise SystemExit(
            'HIBA -- %s: nincs biztonsagos gepi hatar (%s), nincs kezi javaslat a '
            'KEZI_JAVASLATOK-ban, nincs nem_targyalja besorolas sem -- dontes '
            'hianyzik (a token %s allapotban lenne, kezi hatart kell felvenni)'
            % (token, minosites, minosites))

    header = ['strong', 'allapot', 'nyelvi_hatter', 'szocikk_hossz', 'hatar_pozicio']
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT (részben kézi javaslat) — eszkozok/bdb_etim_hatarok_import.py.\n')
        f.write('# allapot: gepi (regex-hatar) | javaslat (kezi, JOVAHAGYASRA VAR — l. menet '
                'vegi ⛔) | jovahagyott (kezi, chat-dontessel jovahagyva, 2026.09.29 -- H0922, '
                'H3678, H8004, H8034, majd kulon vizsgalat utan H0430 is, l. naplok/'
                'SZOTAR_S1_7_jelentes.md) | nem_targyalja (nincs erdemi etimologia). Dok.: '
                'konkordancia/BDB_teljes_unabridged_README.md\n')
        f.write('\t'.join(header) + '\n')
        for row in sorok:
            f.write('\t'.join(row) + '\n')

    print('sorok: %d' % len(sorok))
    for allapot in ('gepi', 'javaslat', 'jovahagyott', 'nem_targyalja'):
        n = sum(1 for r in sorok if r[1] == allapot)
        print('  %s: %d' % (allapot, n))
    print('irva: %s' % KIMENET)


if __name__ == '__main__':
    HEBER_TOKENEK = [
        'H0127', 'H0430', 'H0779', 'H0922', 'H1121', 'H2403', 'H2416', 'H2555',
        'H3548', 'H3678', 'H4467', 'H5303', 'H5315', 'H6093', 'H6975', 'H7043',
        'H7121', 'H7451', 'H7496', 'H7497', 'H7585', 'H7843', 'H8004', 'H8034',
        'H8414', 'H8415',
    ]
    run(HEBER_TOKENEK)
