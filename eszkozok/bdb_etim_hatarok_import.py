"""BDB_etimologia_kezi_hatarok.tsv -- a 26 heber gerinc-token (D28) BDB-
szocikkeinek "nyelvi hatter" (etimologia/rokon-nyelvi anyag) hatar-
besorolasa negy kategoriaba (S9, D21, D28/D29 kiegeszitve; a hatarfelismero
szabaly F05b-ben javitva ketszer -- l. D41 es hatar_keres()).

- gepi: a nyelvi_hatter az ELSO ZARojelen KIVULI (nulla melysegu) em-dash
  (—) ELOTT er veget (D41) -- a szocikk zarojel-melyseget karakterenkent
  szamolva, az elso "—" karakter, amelynel a melyseg <=0. ES a hatar a
  szocikk hosszanak legfeljebb 40%-anal van (BIZTONSAGI_KUSZOB). Ha
  egyik feltetel sem teljesul, a token NEM lehet gepi (l. lent).
- javaslat: nincs nulla-melysegu em-dash, VAGY a talalt hatar a szocikk
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')
BDB_UT = os.path.join(KONKORDANCIA, 'BDB_teljes_unabridged.tsv')
KIMENET = os.path.join(KONKORDANCIA, 'BDB_etimologia_kezi_hatarok.tsv')

# D41 (F05b, 2026.09.29, felhasznaloi dontes a 0eeb885 reszleges
# jovahagyasa utan): a korabbi harom-mintás (HATARJELOLTEK) megkozelites
# tul specifikus volt -- a helyes altalanos szabaly egyszerubb: a
# nyelvi_hatter az ELSO ZAROJELEN KIVULI (nulla melysegu) em-dash (—)
# elott er veget. A legtobb BDB-szocikk etimologiaja egyetlen, esetleg
# beagyazott zarojeleket tartalmazo "(...)" blokkban all; ami e blokk
# UTAN, a legkulso zarojel-melysegen (0) all es "—"-sel kezdodik, az mar
# nem etimologia (akar szamozott ertelem, akar igealak-paradigma, akar
# igehelyes hasznalati lista). A regi `—\s*1\s` minta ezt csak
# esetlegesen talalta el (l. a 0eeb885 commit indoklasat).
BIZTONSAGI_KUSZOB_SZAZALEK = 40.0


def zero_melysegu_emdash(entry):
    """Az elso '—' (em-dash) pozicioja, amelynel a zarojel-melyseg <=0,
    vagy None, ha nincs ilyen. A melyseg '(' -nal no, ')' -nal csokken."""
    melyseg = 0
    for i, ch in enumerate(entry):
        if ch == '(':
            melyseg += 1
        elif ch == ')':
            melyseg -= 1
        elif ch == '—':  # em-dash
            if melyseg <= 0:
                return i
    return None


def hatar_keres(entry):
    """(pozicio, 'gepi'|'tul_hosszu'|'nincs_illeszkedes') -- a D41 szerinti
    elso nulla-melysegu em-dash pozicioja, es hogy a szocikk hosszanak
    BIZTONSAGI_KUSZOB_SZAZALEK-anal beluli-e."""
    pozicio = zero_melysegu_emdash(entry)
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
# OCR-hiba/csonkolas). A H2403-at a D41-es javitokor soran hagyta jova,
# kezi hatarral. FONTOS: a H2403-nal VAN nulla-melysegu em-dash (pozicio
# 556, "...+ 40 t. suffix; -- 1 sin..."), a D41 szabaly tehat magat a
# 40%-os kuszobot at is engedne (5.8%) -- DE addig a pontig egy hosszu,
# em-dash nelkuli inflektalt-alak/citacios lista all (construct/suffix/
# plural alakok versekkel), ami NEM etimologia. A D41 szabaly ISMERT
# GYENGESEGE: csak az em-dash-hatarolt hasznalati/alak-blokkokat ismeri
# fel, az em-dash nelkuli, vesszovel csatolt inflekcios listat nem --
# ezert kellett kezi felulbiralas, nem azert, mert nincs automatikus
# talalat.

JOVAHAGYOTT = {'H0430', 'H0922', 'H2403', 'H3678', 'H8004', 'H8034'}

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
    'H2403': (
        "H2403. chatta 'ah חַטָּאת noun feminine^1Sam 14:38 (Gen 4:7 no "
        'exception for רֹבֵץ is noun = crouching beast) sin, sin-offering'
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
        # A kezi javaslat/jovahagyott tokeneknel a kezi hatar MINDIG elsobbseget
        # elvez az automatikus felismeressel szemben -- ezeket eppen azert
        # veszik fel a KEZI_JAVASLATOK-ba, mert a szocikk szerkezete miatt a
        # gepi szabaly nem ad jo hatart (vagy adna valamit, de nem azt, amit a
        # felhasznalo jovahagyott); az automatikus utat itt meg sem probaljuk.
        if token in KEZI_JAVASLATOK:
            nyelvi_hatter = KEZI_JAVASLATOK[token]
            allapot = 'jovahagyott' if token in JOVAHAGYOTT else 'javaslat'
            sorok.append((token, allapot, nyelvi_hatter, str(len(entry)), str(len(nyelvi_hatter))))
            continue
        pozicio, minosites = hatar_keres(entry) if entry else (None, 'nincs_illeszkedes')
        if minosites == 'gepi':
            nyelvi_hatter = entry[:pozicio].strip()
            sorok.append((token, 'gepi', nyelvi_hatter, str(len(entry)), str(pozicio)))
            continue
        raise SystemExit(
            'HIBA -- %s: nincs biztonsagos gepi hatar (%s), nincs kezi javaslat a '
            'KEZI_JAVASLATOK-ban, nincs nem_targyalja besorolas sem -- dontes '
            'hianyzik (a token %s allapotban lenne, kezi hatart kell felvenni)'
            % (token, minosites, minosites))

    header = ['strong', 'allapot', 'nyelvi_hatter', 'szocikk_hossz', 'hatar_pozicio']
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT (részben kézi javaslat) — eszkozok/bdb_etim_hatarok_import.py.\n')
        f.write('# allapot: gepi (D41-hatar, l. eszkozok/bdb_etim_hatarok_import.py) | '
                'javaslat (kezi, JOVAHAGYASRA VAR — l. menet vegi ⛔) | jovahagyott (kezi, '
                'chat-dontessel jovahagyva, 2026.09.29 -- H0922, H3678, H8004, H8034, majd '
                'kulon vizsgalat utan H0430, majd a D41 javitokor soran H2403 is, l. naplok/'
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
