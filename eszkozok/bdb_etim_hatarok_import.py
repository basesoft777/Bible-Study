"""BDB_etimologia_kezi_hatarok.tsv -- a 26 heber gerinc-token (D28) BDB-
szocikkeinek "nyelvi hatter" (etimologia/rokon-nyelvi anyag) hatar-
besorolasa harom kategoriaba (S9, D21, D28/D29 kiegeszitve).

- gepi: az em-dash + "1 " minta (regex) pontosan illeszkedik -- a
  hatarig tarto resz a nyelvi_hatter.
- javaslat: van erdemi rokon-nyelvi/etimologiai tartalom, de a gepi minta
  nem illeszkedik (eltero szamozasi/tagolasi forma) -- KEZZEL kijelolt
  hatar, JOVAHAGYASRA VAR (a menet vegi ⛔-nel).
- nem_targyalja: rovid szocikk, nincs kulon etimologiai/rokon-nyelvi
  bekezdes.

A "javaslat" sorokat ez a szkript NEM szamitja ki automatikusan -- a
JAVASLAT szoveget kezzel irt konstansok adjak (KEZI_JAVASLATOK), mert az
automatikus hatarfelismeres itt eppen azert bukik, mert a forras nem
kovetkezetes tagolasu; a kezi dontes indoklasat l. a SZOTAR_BRIEF.md §3
S1.4 soraban es az S1.4 jelenteseben.
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

BOUNDARY_RE = re.compile(r'—\s*1\s')  # em-dash + '1 '

# D21 (a regi 24 tokenen) + D28/D29 (H8414 uj gepi, H0922 uj javaslat).
NEM_TARGYALJA = {'H0779', 'H2555', 'H5303', 'H6093', 'H7496', 'H7497'}

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
        m = BOUNDARY_RE.search(entry) if entry else None
        if m:
            nyelvi_hatter = entry[:m.start()].strip()
            sorok.append((token, 'gepi', nyelvi_hatter, str(len(entry)), str(m.start())))
            continue
        if token in KEZI_JAVASLATOK:
            nyelvi_hatter = KEZI_JAVASLATOK[token]
            sorok.append((token, 'javaslat', nyelvi_hatter, str(len(entry)), str(len(nyelvi_hatter))))
            continue
        raise SystemExit('HIBA -- %s: nincs gepi hatar, nincs kezi javaslat, nincs '
                          'nem_targyalja besorolas sem -- dontes hianyzik' % token)

    header = ['strong', 'allapot', 'nyelvi_hatter', 'szocikk_hossz', 'hatar_pozicio']
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT (részben kézi javaslat) — eszkozok/bdb_etim_hatarok_import.py.\n')
        f.write('# allapot: gepi (regex-hatar) | javaslat (kezi, JOVAHAGYASRA VAR — l. menet '
                'vegi ⛔) | nem_targyalja (nincs erdemi etimologia). Dok.: konkordancia/'
                'BDB_teljes_unabridged_README.md\n')
        f.write('\t'.join(header) + '\n')
        for row in sorok:
            f.write('\t'.join(row) + '\n')

    print('sorok: %d' % len(sorok))
    for allapot in ('gepi', 'javaslat', 'nem_targyalja'):
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
