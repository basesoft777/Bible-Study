"""
zaro3_kiejtes_potlas.py — ISTENTISZT_V3_ZARO3.md X1-X2: a ZARO2 kimaradt
cseréi és a `kapcsolodas`-mezők kiejtése.

A ZARO2-es szkript hibája: ha egy (id[, igehely]) + mezo kulcshoz TÖBB
csere-sor is tartozott, mindegyiket az EREDETI (még cseretlen)
mezőtartalomból számolta, majd a legutolsó írta csak vissza -- a
korábbi cserék elvesztek. Ez a szkript minden kulcshoz tartozó cseréket
SORBAN, EGYMÁS UTÁN, a mező ténylegesen aktuális (már részben cserélt)
tartalmán alkalmazza; minden lépésnél megköveteli, hogy a "régi" a
JELENLEGI tartalomban pontosan egyszer forduljon elő, különben ⛔ (írás
nem történik semmelyik táblában).

A jelentés a VÉGSŐ, fájlba írt mezőtartalom alapján adja meg a "hány
csere hatott" számot (tartalmazza-e a mező az "új" szöveget), nem a
feldolgozott csere-sorok számából.

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
# X1 -- adat/motivumok.tsv (kulcs: id), a ZARO2-bol kimaradt 9 csere
# ---------------------------------------------------------------------------
X1 = [
    dict(id='ISTENTISZT-001', mezo='negativ_kriterium',
         regi='a קָרָא + בְּ (aktív', uj='a קָרָא (kárá) + בְּ (be) (aktív'),
    dict(id='TEREMT-001', mezo='negativ_kriterium',
         regi='a תְּהוֹם gyököt', uj='a תְּהוֹם (tehóm) gyököt'),
    dict(id='TEREMT-001', mezo='negativ_kriterium',
         regi='ἄβυσσος megfelelőjét)', uj='ἄβυσσος (abüsszosz) megfelelőjét)'),
    dict(id='ALVIL-001', mezo='negativ_kriterium',
         regi='a שְׁאוֹל gyököt', uj='a שְׁאוֹל (seól) gyököt'),
    dict(id='ALVIL-001', mezo='negativ_kriterium',
         regi='ᾍδης megfelelőjét) kell', uj='ᾍδης (hadész) megfelelőjét) kell'),
    dict(id='MENNY-001', mezo='negativ_kriterium',
         regi='a בְּנֵי (הָ)אֱלֹהִים szórendi', uj='a בְּנֵי (הָ)אֱלֹהִים (bené (há)elóhím) szórendi'),
    dict(id='MENNY-001', mezo='negativ_kriterium',
         regi='a נְפִלִים szót', uj='a נְפִלִים (nefilím) szót'),
    dict(id='HODIT-001', mezo='negativ_kriterium',
         regi='a רְפָאִים gyököt', uj='a רְפָאִים (refáím) gyököt'),
    dict(id='HODIT-001', mezo='negativ_kriterium',
         regi='זוּזִים, אֵימִים, זַמְזֻמִּים)', uj='זוּזִים – zúzím, אֵימִים – émím, זַמְזֻמִּים – zamzummím)'),
]

# ---------------------------------------------------------------------------
# X2 -- adat/elofordulasok.tsv (kulcs: id + igehely), kapcsolodas (49 csere)
# ---------------------------------------------------------------------------
X2 = [
    dict(id='KIRALY-001', igehely='2Móz 19:6', mezo='kapcsolodas',
         regi='. Ugyanaz a כֹּהֵן ', uj='. Ugyanaz a כֹּהֵן (kóhén) '),
    dict(id='TEREMT-001', igehely='Zsolt 33:7', mezo='kapcsolodas',
         regi=' fordítja a תְּהוֹם-', uj=' fordítja a תְּהוֹם (tehóm)-'),
    dict(id='TEREMT-001', igehely='Zsolt 107:26', mezo='kapcsolodas',
         regi=' fordítja a תְּהוֹם-', uj=' fordítja a תְּהוֹם (tehóm)-'),
    dict(id='TEREMT-001', igehely='Luk 8:31', mezo='kapcsolodas',
         regi='ἄβυσσος ', uj='ἄβυσσος (abüsszosz) '),
    dict(id='TEREMT-001', igehely='Róm 10:7', mezo='kapcsolodas',
         regi='ἄβυσσος ', uj='ἄβυσσος (abüsszosz) '),
    dict(id='TEREMT-001', igehely='Jel 9:1-2', mezo='kapcsolodas',
         regi='ἄβυσσος ', uj='ἄβυσσος (abüsszosz) '),
    dict(id='TEREMT-001', igehely='Jel 11:7', mezo='kapcsolodas',
         regi='ἄβυσσος ', uj='ἄβυσσος (abüsszosz) '),
    dict(id='TEREMT-001', igehely='Jel 17:8', mezo='kapcsolodas',
         regi='ἄβυσσος ', uj='ἄβυσσος (abüsszosz) '),
    dict(id='TEREMT-001', igehely='Jel 20:1-3', mezo='kapcsolodas',
         regi='ἄβυσσος ', uj='ἄβυσσος (abüsszosz) '),
    dict(id='ALVIL-001', igehely='Ézs 14:9', mezo='kapcsolodas',
         regi='asz, ahol a רְפָאִים ', uj='asz, ahol a רְפָאִים (refáím) '),
    dict(id='ALVIL-001', igehely='Luk 16:23', mezo='kapcsolodas',
         regi='ᾍδης ', uj='ᾍδης (hadész) '),
    dict(id='ALVIL-001', igehely='Jel 1:18', mezo='kapcsolodas',
         regi='ᾍδης ', uj='ᾍδης (hadész) '),
    dict(id='ALVIL-001', igehely='Jel 6:8', mezo='kapcsolodas',
         regi='ᾍδης ', uj='ᾍδης (hadész) '),
    dict(id='ALVIL-001', igehely='Jel 20:13-14', mezo='kapcsolodas',
         regi='ᾍδης ', uj='ᾍδης (hadész) '),
    dict(id='ALVIL-001', igehely='Luk 10:15', mezo='kapcsolodas',
         regi='ᾍδης ', uj='ᾍδης (hadész) '),
    dict(id='ALVIL-001', igehely='Mt 11:23', mezo='kapcsolodas',
         regi='ᾍδης ', uj='ᾍδης (hadész) '),
    dict(id='MENNY-001', igehely='1Móz 6:2', mezo='kapcsolodas',
         regi='בְּנֵי הָאֱלֹהִים ', uj='בְּנֵי הָאֱלֹהִים (bené háelóhím) '),
    dict(id='MENNY-001', igehely='1Móz 6:4', mezo='kapcsolodas',
         regi='születnek a גִּבֹּרִים,', uj='születnek a גִּבֹּרִים (gibbórím),'),
    dict(id='MENNY-001', igehely='1Móz 6:4', mezo='kapcsolodas',
         regi='נְפִלִים ', uj='נְפִלִים (nefilím) '),
    dict(id='MENNY-001', igehely='Jób 1:6', mezo='kapcsolodas',
         regi='בְּנֵי הָאֱלֹהִים ', uj='בְּנֵי הָאֱלֹהִים (bené háelóhím) '),
    dict(id='MENNY-001', igehely='Jób 38:7', mezo='kapcsolodas',
         regi='a בְּנֵי אֱלֹהִים ', uj='a בְּנֵי אֱלֹהִים (bené elóhím) '),
    dict(id='MENNY-001', igehely='4Móz 13:34', mezo='kapcsolodas',
         regi='elentésében נְפִלִים ', uj='elentésében נְפִלִים (nefilím) '),
    dict(id='HODIT-001', igehely='1Móz 14:5', mezo='kapcsolodas',
         regi='רְפָאִים, זוּזִים, אֵימִים ', uj='רְפָאִים, זוּזִים, אֵימִים (refáím, zúzím, émím) '),
    dict(id='HODIT-001', igehely='1Móz 15:20', mezo='kapcsolodas',
         regi='רְפָאִים ', uj='רְפָאִים (refáím) '),
    dict(id='HODIT-001', igehely='4Móz 13:34', mezo='kapcsolodas',
         regi='נְפִלִים ⇒ עֲנָקִים ', uj='נְפִלִים ⇒ עֲנָקִים (nefilím ⇒ anákím) '),
    dict(id='HODIT-001', igehely='5Móz 2:20', mezo='kapcsolodas',
         regi='זַמְזֻמִּים... רְפָאִים ', uj='זַמְזֻמִּים... רְפָאִים (zamzummím … refáím) '),
    dict(id='HODIT-001', igehely='5Móz 3:11', mezo='kapcsolodas',
         regi='עוֹג... מִיֶּתֶר הָרְפָאִים ', uj='עוֹג... מִיֶּתֶר הָרְפָאִים (óg … mijjeter hárefáím) '),
    dict(id='HODIT-001', igehely='Józs 12:4', mezo='kapcsolodas',
         regi='אֶרֶץ רְפָאִים ', uj='אֶרֶץ רְפָאִים (erec refáím) '),
    dict(id='HODIT-001', igehely='Jób 26:5', mezo='kapcsolodas',
         regi='רְפָאִים יְחוֹלָלוּ מִתַּחַת לַמָּיִם ', uj='רְפָאִים יְחוֹלָלוּ מִתַּחַת לַמָּיִם (refáím jehólálú mittahat lammájim) '),
    dict(id='HODIT-001', igehely='Zsolt 88:11', mezo='kapcsolodas',
         regi='הֲרְפָאִים יָקוּמוּ יוֹדוּךָ ', uj='הֲרְפָאִים יָקוּמוּ יוֹדוּךָ (harefáím jákúmú jódúkhá) '),
    dict(id='HODIT-001', igehely='Péld 2:18', mezo='kapcsolodas',
         regi='רְפָאִים ', uj='רְפָאִים (refáím) '),
    dict(id='HODIT-001', igehely='Ézs 14:9', mezo='kapcsolodas',
         regi='רְפָאִים... כָּל־עַתּוּדֵי אָרֶץ ', uj='רְפָאִים... כָּל־עַתּוּדֵי אָרֶץ (refáím … kol-attúdé árec) '),
    dict(id='HODIT-001', igehely='Ézs 26:14', mezo='kapcsolodas',
         regi='רְפָאִים ', uj='רְפָאִים (refáím) '),
    dict(id='HODIT-001', igehely='2Sám 5:18', mezo='kapcsolodas',
         regi='עֵמֶק רְפָאִים ', uj='עֵמֶק רְפָאִים (émek refáím) '),
    dict(id='HODIT-001', igehely='Ézs 17:5', mezo='kapcsolodas',
         regi='עֵמֶק רְפָאִים ', uj='עֵמֶק רְפָאִים (émek refáím) '),
    dict(id='HODIT-001', igehely='Józs 15:8', mezo='kapcsolodas',
         regi='עֵמֶק רְפָאִים ', uj='עֵמֶק רְפָאִים (émek refáím) '),
    dict(id='HODIT-001', igehely='Józs 18:16', mezo='kapcsolodas',
         regi='עֵמֶק רְפָאִים ', uj='עֵמֶק רְפָאִים (émek refáím) '),
    dict(id='HODIT-001', igehely='Józs 17:15', mezo='kapcsolodas',
         regi='אֶרֶץ הָרְפָאִים ', uj='אֶרֶץ הָרְפָאִים (erec hárefáím) '),
    dict(id='HAMART-001', igehely='1Móz 4:7', mezo='kapcsolodas',
         regi='חַטָּאת ', uj='חַטָּאת (hattát) '),
    dict(id='HAMART-001', igehely='1Móz 6:11', mezo='kapcsolodas',
         regi=', Nif\'ál) + וַתִּמָּלֵא הָאָרֶץ חָמָס ', uj=', Nif\'ál) + וַתִּמָּלֵא הָאָרֶץ חָמָס (vattimmálé háárec hámász) '),
    dict(id='HAMART-001', igehely='1Móz 8:21', mezo='kapcsolodas',
         regi='f lekallél) עוֹד אֶת־הָאֲדָמָה ', uj='f lekallél) עוֹד אֶת־הָאֲדָמָה (ód et-háadámá) '),
    dict(id='HAMART-001', igehely='Róm 8:20-22', mezo='kapcsolodas',
         regi='gyanabból a φθείρω-', uj='gyanabból a φθείρω (ftheiró)-'),
    dict(id='HAMART-001', igehely='Róm 8:20-22', mezo='kapcsolodas',
         regi='t áll, és a φθορά ', uj='t áll, és a φθορά (fthora) '),
    dict(id='HAMART-001', igehely='Gal 3:13', mezo='kapcsolodas',
         regi='ával, hanem ἐπικατάρατος-', uj='ával, hanem ἐπικατάρατος (epikataratosz)-'),
    dict(id='HAMART-001', igehely='Zsid 6:7-8', mezo='kapcsolodas',
         regi=':17-18-cal: γῆ + ἄκανθα + τρίβολος,', uj=':17-18-cal: γῆ + ἄκανθα + τρίβολος (gé + akantha + tribolosz),'),
    # A ZARO3.md 76. sora ('n (ἐφθάρη … ἡ γῆ)' -> '...ἡ γῆ (hé gé))') ütközött a
    # 79. sorral (ugyanazt a zárójelet célozza, eltérő eredménnyel) -- a
    # felhasználó döntése (chat, 2026.09.22): a 79. sor érvényes, ez a sor
    # (76.) kihagyva. Általános szabály innentől: azonos célú ütközésnél a
    # később álló sor nyer.
    dict(id='TEREMT-001', igehely='Jel 9:11', mezo='kapcsolodas',
         regi='ἄβυσσος, Ἀβαδδών/Ἀπολλύων', uj='ἄβυσσος (abüsszosz), Ἀβαδδών (Abaddón) / Ἀπολλύων (Apollüón)'),
    dict(id='HAMART-001', igehely='Zsid 6:7-8', mezo='kapcsolodas',
         regi='a κατάρα-szócsaláddal', uj='a κατάρα-szócsaláddal (katara)'),
    dict(id='HAMART-001', igehely='Jel 19:2', mezo='kapcsolodas',
         regi='(ἐφθάρη … ἡ γῆ)', uj='(ἐφθάρη … ἡ γῆ – eftharé … hé gé)'),
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


def apply_sequential(path, key_fields, replacements, report_label, stop_on_conflict=True):
    """stop_on_conflict=False: ha egy csere a JELENLEGI (mar reszben modositott)
    tartalomban nem illeszkedik pontosan egyszer, a szkript nem all meg -- a
    csere KIHAGYVA-kent naplozva folytatja (a felhasznalo altalanos szabalya,
    2026.09.22: azonos celu utkozesnel a kesobb allo sor nyer, a korabbit ne
    alkalmazd -- itt a masik iranyban: ha egy sor nem illeszkedik, kihagyando,
    nem allitando meg miatta a teljes tetel)."""
    comment_lines, header, data_lines = read_tsv_raw(path)
    idx = {name: i for i, name in enumerate(header)}

    rows = []
    for line in data_lines:
        rows.append(line.split('\t') if line else None)

    # key -> row index (must be unique)
    key_to_row = {}
    for i, cols in enumerate(rows):
        if cols is None:
            continue
        key = tuple(cols[idx[k]] for k in key_fields)
        key_to_row.setdefault(key, []).append(i)

    # current, evolving cell values: (row_index, mezo_idx) -> str
    current = {}
    hibak = []
    kihagyva = []
    terv = []  # (row_i, mezo_idx, regi, uj, key_desc)

    for spec in replacements:
        key = tuple(spec[k] for k in key_fields)
        key_desc = ' / '.join('%s=%s' % (k, spec[k]) for k in key_fields)
        talalt = key_to_row.get(key, [])
        if len(talalt) != 1:
            hibak.append('%s: %d sor illeszkedik a kulcsra (1 helyett)' % (key_desc, len(talalt)))
            continue
        row_i = talalt[0]
        mezo_idx = idx[spec['mezo']]
        cell_key = (row_i, mezo_idx)
        if cell_key not in current:
            current[cell_key] = rows[row_i][mezo_idx]

        cella = current[cell_key]
        n = cella.count(spec['regi'])
        if n != 1:
            uzenet = ("%s (%s): a régi minta a JELENLEGI tartalomban %d alkalommal fordul elő (1 helyett): %r"
                       % (key_desc, spec['mezo'], n, spec['regi']))
            if stop_on_conflict:
                hibak.append(uzenet)
            else:
                kihagyva.append(uzenet)
            continue

        uj_cella = cella.replace(spec['regi'], spec['uj'], 1)
        current[cell_key] = uj_cella
        terv.append((row_i, mezo_idx, spec['regi'], spec['uj'], key_desc, spec['mezo']))

    if hibak:
        print('%s: MEGALLAS -- %d hiba, iras nem tortent:' % (report_label, len(hibak)))
        for h in hibak:
            print('  - %s' % h)
        return False, []

    if kihagyva:
        print('%s: %d csere KIHAGYVA (utkozes a jelenlegi tartalommal, nem allitotta meg a tetelt):'
              % (report_label, len(kihagyva)))
        for k in kihagyva:
            print('  - %s' % k)

    for (row_i, mezo_idx), vegso_ertek in current.items():
        rows[row_i][mezo_idx] = vegso_ertek

    data_lines_uj = ['\t'.join(cols) if cols is not None else '' for cols in rows]
    write_tsv_raw(path, comment_lines, header, data_lines_uj)

    # vegso ellenorzes: a fajlbol UJRAOLVASVA, a vegso mezotartalom tartalmazza-e az "uj"-t
    _c2, _h2, data_lines2 = read_tsv_raw(path)
    rows2 = [line.split('\t') if line else None for line in data_lines2]

    talalt_n = 0
    for row_i, mezo_idx, regi, uj, key_desc, mezo in terv:
        vegso = rows2[row_i][mezo_idx]
        ok = uj in vegso
        talalt_n += 1 if ok else 0
        print('  %s [%s]: %r -> %r  [%s]' % (key_desc, mezo, regi, uj, 'OK' if ok else 'HIANYZIK A VEGSO TARTALOMBOL'))

    print('%s: %d/%d csere igazolva a vegso mezotartalomban' % (report_label, talalt_n, len(replacements)))
    return True, terv


def main():
    ok1, _ = apply_sequential(os.path.join(ADAT, 'motivumok.tsv'), ('id',), X1, 'X1 (motivumok.tsv)')
    ok2, _ = apply_sequential(os.path.join(ADAT, 'elofordulasok.tsv'), ('id', 'igehely'), X2,
                               'X2 (elofordulasok.tsv)', stop_on_conflict=False)

    if not (ok1 and ok2):
        print('\nMEGALLAS: legalabb egy blokk hibaval allt meg.')
        sys.exit(2)
    print('\nMind a ket blokk sikeresen alkalmazva.')


if __name__ == '__main__':
    main()
