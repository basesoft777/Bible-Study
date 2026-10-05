"""F58 M1: az OSHB héber morfológiai jelkulcs importja adat/morf_kulcs_heber.tsv-be.

Bemenet: adat/kulso/oshb_HebrewMorphologyCodes.html (openscriptures/morphhb
@3d15126fb1ef74867fc1434be1942e837932691f, parsing/HebrewMorphologyCodes.html,
CC BY 4.0). A kódok és a forrás megnevezései kizárólag ebből a fájlból jönnek.
A `jelentes_hu` a forrás megnevezésének fordítása az alábbi FORDITAS-szótárból
(a megnevezés szó szerinti fordítása, magyarázat nélkül); ismeretlen megnevezésnél
a szkript megáll (nincs csendes kitöltés).
Futtatás: python eszkozok/morf_kulcs_import.py
"""
import sys
import re
import html

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

FORRAS_FAJL = 'adat/kulso/oshb_HebrewMorphologyCodes.html'
KIMENET = 'adat/morf_kulcs_heber.tsv'
FORRAS = ('openscriptures/morphhb@3d15126fb1ef74867fc1434be1942e837932691f '
          'parsing/HebrewMorphologyCodes.html (CC BY 4.0)')
TS = '2026-10-05'

# szakasz-cím (a forrás h3-ja) -> (pozicio, nyelv); a szófaj-táblázat külön kezelt
SZAKASZ = {
    'Verb stems (Hebrew)': ('igetorzs', 'H'),
    'Verb stems (Aramaic)': ('igetorzs', 'A'),
    'Verb conjugation types': ('igetipus', '*'),
    'Adjective types': ('tipus_A', '*'),
    'Noun types': ('tipus_N', '*'),
    'Pronoun types': ('tipus_P', '*'),
    'Preposition types': ('tipus_R', '*'),
    'Suffix types': ('tipus_S', '*'),
    'Particle types': ('tipus_T', '*'),
    'Person': ('szemely', '*'),
    'Gender': ('nem', '*'),
    'Number': ('szam', '*'),
    'State': ('allapot', '*'),
    'Language': ('nyelv_jel', '*'),
}

FORDITAS = {
    # szófaj
    'adjective': 'melléknév', 'conjunction': 'kötőszó', 'adverb': 'határozószó', 'noun': 'főnév',
    'pronoun': 'névmás', 'preposition': 'elöljáró', 'suffix': 'toldalék', 'particle': 'partikula',
    'verb': 'ige',
    # igetörzsek, héber
    'qal': 'qal', 'niphal': 'nifal', 'piel': 'piel', 'pual': 'pual', 'hiphil': 'hifil',
    'hophal': 'hofal', 'hithpael': 'hitpael', 'polel': 'polel', 'polal': 'polal',
    'hithpolel': 'hitpolel', 'poel': 'poel', 'poal': 'poal', 'palel': 'palel', 'pulal': 'pulal',
    'qal passive': 'qal passzív', 'pilpel': 'pilpel', 'polpal': 'polpal',
    'hithpalpel': 'hitpalpel', 'nithpael': 'nitpael', 'pealal': 'pealal', 'pilel': 'pilel',
    'hothpaal': 'hotpaal', 'tiphil': 'tifil', 'hishtaphel': 'histafel', 'nithpalel': 'nitpalel',
    'nithpoel': 'nitpoel', 'hithpoel': 'hitpoel',
    # igetörzsek, arámi (a héberrel közös nevek fent)
    'peal': 'peal', 'peil': 'peil', 'hithpeel': 'hitpeel', 'pael': 'pael', 'ithpaal': 'itpaal',
    'hithpaal': 'hitpaal', 'aphel': 'afel', 'haphel': 'hafel', 'saphel': 'safel',
    'shaphel': 'shafel', 'ithpeel': 'itpeel', 'ishtaphel': 'istafel', 'hithaphel': 'hitafel',
    'ithpoel': 'itpoel', 'hephal': 'hefal', 'tiphel': 'tifel', 'palpel': 'palpel',
    'ithpalpel': 'itpalpel', 'ithpolel': 'itpolel', 'ittaphal': 'ittafal',
    # igetípusok
    'perfect (qatal)': 'perfectum (qatal)',
    'sequential perfect (weqatal)': 'szekvenciális perfectum (weqatal)',
    'imperfect (yiqtol)': 'imperfectum (yiqtol)',
    'sequential imperfect (wayyiqtol)': 'szekvenciális imperfectum (wayyiqtol)',
    'cohortative': 'kohortatívusz', 'jussive': 'jusszívusz', 'imperative': 'felszólító mód',
    'participle active': 'participium, cselekvő', 'participle passive': 'participium, szenvedő',
    'infinitive absolute': 'infinitivus absolutus', 'infinitive construct': 'infinitivus constructus',
    # melléknév-, főnév-, névmás-, prepozíció-, suffixum-, partikulatípusok
    'cardinal number': 'tőszámnév', 'gentilic': 'népnévi', 'ordinal number': 'sorszámnév',
    'common': 'köznév', 'proper name': 'tulajdonnév',
    'demonstrative': 'mutató', 'indefinite': 'határozatlan', 'interrogative': 'kérdő',
    'personal': 'személyes', 'relative': 'vonatkozó',
    'definite article': 'határozott névelő',
    'directional he': 'irányhatározói he', 'paragogic he': 'paragogikus he',
    'paragogic nun': 'paragogikus nun', 'pronominal': 'névmási',
    'affirmation': 'megerősítő', 'exhortation': 'buzdító', 'interjection': 'indulatszó',
    'negative': 'tagadó', 'direct object marker': 'tárgyjel',
    # személy, nem, szám, állapot, nyelv
    'first': 'első', 'second': 'második', 'third': 'harmadik',
    'both (noun)': 'mindkettő (főnév)', 'common (verb)': 'közös (ige)',
    'feminine': 'nőnem', 'masculine': 'hímnem',
    'dual': 'kettes szám', 'plural': 'többes szám', 'singular': 'egyes szám',
    'absolute': 'abszolút', 'construct': 'constructus', 'determined': 'határozott',
    'Hebrew': 'héber', 'Aramaic': 'arámi',
    # a szófaj-táblázat oszlopfejei
    'type': 'típus', 'stem': 'törzs', 'person': 'személy', 'gender': 'nem', 'number': 'szám',
    'state': 'állapot',
}


def tisztit(s):
    s = re.sub(r'<sup>.*?</sup>', '', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s).replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', s).strip()


def hu(nev):
    if nev not in FORDITAS:
        sys.exit('HIÁNYZÓ FORDÍTÁS (nincs csendes kitöltés): ' + repr(nev))
    return FORDITAS[nev]


def main():
    t = open(FORRAS_FAJL, encoding='utf-8', newline='').read()
    sorok = []

    def sor(pozicio, nyelv, kod, forras_nev, hu_nev, hely):
        prov = f'scope={hely} | forras={FORRAS} | ts={TS}'
        sorok.append([pozicio, nyelv, kod, forras_nev, hu_nev, FORRAS, prov])

    # 1. szófaj-táblázat (az első <table> a "Part of Speech" h2 után) és szerkezete
    i = t.index('<h2>Part of Speech</h2>')
    tab = t[t.index('<table', i):t.index('</table>', i)]
    for tr in re.findall(r'<tr>(.*?)</tr>', tab, re.S):
        tds = re.findall(r'<td>(.*?)</td>', tr, re.S)
        kod, nev = tisztit(tds[0]), tisztit(tds[1])
        sor('szofaj', '*', kod, nev, hu(nev), 'Part of Speech táblázat')
        slotok = [tisztit(x) for x in tds[2:] if tisztit(x)]
        forras_szerk = ' > '.join(slotok) if slotok else '(nincs további pozíció)'
        hu_szerk = ' > '.join(hu(x) for x in slotok) if slotok else '(nincs további pozíció)'
        sor('szerkezet', '*', kod, forras_szerk, hu_szerk, 'Part of Speech táblázat, sor ' + kod)

    # 2. szakaszok
    for m in re.finditer(r'<h3[^>]*>(.*?)</h3>(.*?)</section>', t, re.S):
        cim = tisztit(m.group(1))
        if cim not in SZAKASZ:
            continue
        poz, nyelv = SZAKASZ[cim]
        for tr in re.findall(r'<tr>(.*?)</tr>', m.group(2), re.S):
            tds = re.findall(r'<td>(.*?)</td>', tr, re.S)
            if len(tds) < 2:
                continue
            kod, nev = tisztit(tds[0]), tisztit(tds[1])
            if not kod:
                continue
            sor(poz, nyelv, kod, nev, hu(nev), cim)

    # 3. a helykitöltő x (a forrás szó szerinti mondata)
    if "Use 'x' as a placeholder for unknown or unnecessary values" not in t:
        sys.exit('az x-helykitöltő mondata nem található')
    sor('helykitolto', '*', 'x', 'placeholder for unknown or unnecessary values',
        'ismeretlen vagy szükségtelen érték helykitöltője', 'Part of Speech jegyzet 5.')

    fejlec = ['pozicio', 'nyelv', 'kod', 'jelentes_forras', 'jelentes_hu', 'forras', 'proveniencia']
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/morf_kulcs_import.py — kézzel nem szerkesztendő.\n')
        f.write('# proveniencia: scope=adat/kulso/oshb_HebrewMorphologyCodes.html (teljes jelkulcs) | '
                f'forras={FORRAS} | licenc=CC BY 4.0; attribúció: "Original work of the Open Scriptures '
                'Hebrew Bible available at https://github.com/openscriptures/morphhb" | '
                f'ts={TS}\n')
        f.write('# nyelv: H = csak héber, A = csak arámi, * = mindkettő; a Macula-kód a nyelvet nem hordozza (adat/morf_nyelv_aramai.tsv)\n')
        f.write('\t'.join(fejlec) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    print(len(sorok), 'sor ->', KIMENET)


if __name__ == '__main__':
    main()
