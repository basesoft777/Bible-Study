"""
zaro2_kiejtes_potlas.py — ISTENTISZT_V3_ZARO2.md W1-W3: kiejtés-pótlás az
adattáblák szövegmezőiben.

Minden csere előtt ellenőrzi, hogy a "régi" minta a megjelölt mező
szövegében PONTOSAN EGYSZER fordul elő; ha nem, megáll (semmit nem ír).
Csak akkor ír, ha MINDEN csere érvényesíthető.

TSV-olvasás/írás kizárólag split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT = os.path.join(ROOT, 'adat')

# ---------------------------------------------------------------------------
# W1 -- adat/elofordulasok.tsv (kulcs: id + igehely)
# ---------------------------------------------------------------------------
W1 = [
    dict(id='ISTENTISZT-001', igehely='1Móz 21:33', mezo='kapcsolodas',
         regi='אֵל עוֹלָם,', uj='אֵל עוֹלָם (él olám),'),
]

# ---------------------------------------------------------------------------
# W2 -- adat/motivumok.tsv (kulcs: id)
# ---------------------------------------------------------------------------
W2 = [
    dict(id='ISTENTISZT-001', mezo='negativ_kriterium',
         regi='a קָרָא + בְּ (aktív', uj='a קָרָא (kárá) + בְּ (be) (aktív'),
    dict(id='ISTENTISZT-001', mezo='negativ_kriterium',
         regi='passzív נִקְרָא...עַל szerkezet', uj='passzív נִקְרָא...עַל (nikrá … al) szerkezet'),
    dict(id='ISTENTISZT-001', mezo='folerendelt_fogalom',
         regi='a קָרָא בְשֵׁם formulán', uj='a קָרָא בְשֵׁם (kárá besém) formulán'),
    dict(id='TEREMT-001', mezo='negativ_kriterium',
         regi='a תְּהוֹם gyököt', uj='a תְּהוֹם (tehóm) gyököt'),
    dict(id='TEREMT-001', mezo='negativ_kriterium',
         regi='ἄβυσσος megfelelőjét)', uj='ἄβυσσος (abüsszosz) megfelelőjét)'),
    dict(id='TEREMT-001', mezo='negativ_kriterium',
         regi='(pl. יָם, "tenger")', uj='(pl. יָם – jám, "tenger")'),
    dict(id='TEREMT-001', mezo='folerendelt_fogalom',
         regi='a תְּהוֹם/ἄβυσσος lexémán', uj='a תְּהוֹם (tehóm) / ἄβυσσος (abüsszosz) lexémán'),
    dict(id='ALVIL-001', mezo='negativ_kriterium',
         regi='a שְׁאוֹל gyököt', uj='a שְׁאוֹל (seól) gyököt'),
    dict(id='ALVIL-001', mezo='negativ_kriterium',
         regi='ᾍδης megfelelőjét) kell', uj='ᾍδης (hadész) megfelelőjét) kell'),
    dict(id='ALVIL-001', mezo='negativ_kriterium',
         regi='a תְּהוֹם/ἄβυσσος szócsalád', uj='a תְּהוֹם (tehóm) / ἄβυσσος (abüsszosz) szócsalád'),
    dict(id='ALVIL-001', mezo='folerendelt_fogalom',
         regi='a שְׁאוֹל/ᾍδης lexémán', uj='a שְׁאוֹל (seól) / ᾍδης (hadész) lexémán'),
    dict(id='MENNY-001', mezo='negativ_kriterium',
         regi='a בְּנֵי (הָ)אֱלֹהִים szórendi', uj='a בְּנֵי (הָ)אֱלֹהִים (bené (há)elóhím) szórendi'),
    dict(id='MENNY-001', mezo='negativ_kriterium',
         regi='a נְפִלִים szót', uj='a נְפִלִים (nefilím) szót'),
    dict(id='MENNY-001', mezo='negativ_kriterium',
         regi='a רְפָאִים szócsalád', uj='a רְפָאִים (refáím) szócsalád'),
    dict(id='MENNY-001', mezo='folerendelt_fogalom',
         regi='a בְּנֵי (הָ)אֱלֹהִים/נְפִלִים lexémákon', uj='a בְּנֵי (הָ)אֱלֹהִים (bené (há)elóhím) / נְפִלִים (nefilím) lexémákon'),
    dict(id='ANTROP-001', mezo='negativ_kriterium',
         regi='a πνεῦμα és ψυχή szavakat', uj='a πνεῦμα (pneuma) és ψυχή (pszükhé) szavakat'),
    dict(id='HODIT-001', mezo='negativ_kriterium',
         regi='a רְפָאִים gyököt', uj='a רְפָאִים (refáím) gyököt'),
    dict(id='HODIT-001', mezo='negativ_kriterium',
         regi='זוּזִים, אֵימִים, זַמְזֻמִּים)', uj='זוּזִים – zúzím, אֵימִים – émím, זַמְזֻמִּים – zamzummím)'),
    dict(id='HODIT-001', mezo='negativ_kriterium',
         regi='a נְפִלִים/גִּבּוֹר szócsalád', uj='a נְפִלִים (nefilím) / גִּבּוֹר (gibbór) szócsalád'),
    dict(id='HODIT-001', mezo='folerendelt_fogalom',
         regi='a רְפָאִים lexémán', uj='a רְפָאִים (refáím) lexémán'),
    dict(id='HAMART-001', mezo='negativ_kriterium',
         regi='ἐπικατάρατος, κατάρα, φθείρω-család)', uj='ἐπικατάρατος – epikataratosz, κατάρα – katara, φθείρω-család – ftheiró)'),
]

# ---------------------------------------------------------------------------
# W3 -- adat/kapcsolatok.tsv (kulcs: id + forras_igehely + cel_igehely)
# ---------------------------------------------------------------------------
W3 = [
    dict(id='ISTENTISZT-001', forras_igehely='Róm 10:14', cel_igehely='1Kor 1:2', mezo='funkcio',
         regi='(ἐπικαλέομαι),', uj='(ἐπικαλέομαι, epikaleomai),'),
    dict(id='ISTENTISZT-001', forras_igehely='1Móz 4:26', cel_igehely='2Móz 33:19', mezo='funkcio',
         regi='(קָרָא+שֵׁם),', uj='(קָרָא+שֵׁם – kárá + sém),'),
    dict(id='KIRALY-001', forras_igehely='2Móz 19:6', cel_igehely='1Pét 2:9', mezo='funkcio',
         regi='(βασίλειον ἱεράτευμα);', uj='(βασίλειον ἱεράτευμα – baszileion hierateuma);'),
]


def read_tsv_raw(path):
    with open(path, encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f]
    comment_lines = []
    i = 0
    while i < len(lines) and lines[i].startswith('#'):
        comment_lines.append(lines[i])
        i += 1
    header = lines[i].split('\t')
    data_lines = lines[i + 1:]
    return comment_lines, header, data_lines


def write_tsv_raw(path, comment_lines, header, data_lines):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        for c in comment_lines:
            f.write(c + '\n')
        f.write('\t'.join(header) + '\n')
        for line in data_lines:
            f.write(line + '\n')


def apply_replacements(path, key_fields, replacements, report_label):
    comment_lines, header, data_lines = read_tsv_raw(path)
    idx = {name: i for i, name in enumerate(header)}

    rows = []
    for line in data_lines:
        if not line:
            rows.append(None)
            continue
        rows.append(line.split('\t'))

    hibak = []
    tervezett = []  # (row_index, mezo_idx, uj_ertek, regi, uj, key_desc)

    for spec in replacements:
        mezo_idx = idx[spec['mezo']]
        talalt_sorok = []
        for i, cols in enumerate(rows):
            if cols is None:
                continue
            if all(cols[idx[k]] == v for k, v in spec.items() if k in key_fields):
                talalt_sorok.append(i)

        key_desc = ' / '.join('%s=%s' % (k, spec[k]) for k in key_fields)
        if len(talalt_sorok) == 0:
            hibak.append('%s: nincs sor ehhez a kulcshoz: %s' % (key_desc, key_desc))
            continue
        if len(talalt_sorok) > 1:
            hibak.append('%s: %d sor illeszkedik a kulcsra (egyértelműnek kellene lennie)'
                          % (key_desc, len(talalt_sorok)))
            continue

        i = talalt_sorok[0]
        cella = rows[i][mezo_idx]
        n = cella.count(spec['regi'])
        if n != 1:
            hibak.append("%s (%s): a régi minta %d alkalommal fordul elő (1 helyett): %r"
                          % (key_desc, spec['mezo'], n, spec['regi']))
            continue

        uj_cella = cella.replace(spec['regi'], spec['uj'], 1)
        tervezett.append((i, mezo_idx, uj_cella, spec['regi'], spec['uj'], key_desc, spec['mezo']))

    if hibak:
        print('%s: MEGALLAS -- %d hiba, iras nem tortent:' % (report_label, len(hibak)))
        for h in hibak:
            print('  - %s' % h)
        return False, []

    for i, mezo_idx, uj_cella, _regi, _uj, _key_desc, _mezo in tervezett:
        rows[i][mezo_idx] = uj_cella

    data_lines_uj = ['\t'.join(cols) if cols is not None else '' for cols in rows]
    write_tsv_raw(path, comment_lines, header, data_lines_uj)

    print('%s: %d/%d csere alkalmazva' % (report_label, len(tervezett), len(replacements)))
    for _i, _mezo_idx, _uj, regi, uj, key_desc, mezo in tervezett:
        print('  %s [%s]: %r -> %r' % (key_desc, mezo, regi, uj))
    return True, tervezett


def main():
    ok1, _ = apply_replacements(
        os.path.join(ADAT, 'elofordulasok.tsv'), ('id', 'igehely'), W1, 'W1 (elofordulasok.tsv)')
    ok2, _ = apply_replacements(
        os.path.join(ADAT, 'motivumok.tsv'), ('id',), W2, 'W2 (motivumok.tsv)')
    ok3, _ = apply_replacements(
        os.path.join(ADAT, 'kapcsolatok.tsv'), ('id', 'forras_igehely', 'cel_igehely'), W3, 'W3 (kapcsolatok.tsv)')

    if not (ok1 and ok2 and ok3):
        print('\nMEGALLAS: legalabb egy blokk hibaval allt meg, semmi sem irodott felul azokban a blokkokban ahol hiba volt.')
        sys.exit(2)
    print('\nMind a harom blokk sikeresen alkalmazva.')


if __name__ == '__main__':
    main()
