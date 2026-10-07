"""BDB-szócikk gépi szeletelése apparátusokra (próba). Csak szerkezetet bont, értelmezés nincs:
címszó, alapjelentés, nyelvi háttér, alaktan, törzsek (igéknél), jelentésszerkezet (1, 2 … / a, b …),
igehely-hivatkozások száma, irodalmi és szövegkritikai jelek. A határok heurisztikusak."""
import re

TORZS = (r"Qal|Niph`al|Pi`el|Pu`al|Hiph`il|Hoph`al|Hithpa`el|Hithpe`el|Hithpo`el|Hithpalpel|"
         r"Pilpel|Polpal|Polel|Polal|Po`el|Po`al|Pil`el|Pul`al|Pual|Piel|Hiphil|Niphal|Hophal|Ishtaphel|Tiph`el|"
         r"Pe`al|Pa`el|Aph`el|Haph`el|Shaph`el|Ithpe`el|Ithpa`al|Ithpa`el|Ithpo`el|Hithpe`el|Hithpa`al|Pe`il|Ishtaph`al")
ARAMI_TORZS = re.compile(r"Pe`al|Pa`el|Aph`el|Haph`el|Shaph`el|Ithpe`el|Ithpa`al|Ithpa`el|Ithpo`el|Hithpe`el|Hithpa`al|Pe`il|Ishtaph`al")
TORZS_FEJ = re.compile(r'(?<![\w`])(' + TORZS + r')_(\d+)')
REF = re.compile(r'\d+:\d+')
NYELV = re.compile(r'(asszír|arab|arámi|szír|szíriai|föníciai|etióp|sabeus|ugariti|akkád|újhéber|nabateus|palmirai|'
                   r'Assyrian|Arabic|Aramaic|Syriac|Phoenician|Ethiopic|Sabean|Nabatean|Palmyrene|Biblical Hebrew|'
                   r'gyök|root)', re.I)
SIGLA = re.compile(r'\b[A-Z][A-Za-z]{0,12}\^[A-Za-z][\w.]*')
KRIT = re.compile(r'(ᵐ\s?\d+|ᵑ\s?\d+|\bKt\b|\bQr\b|\bVrss\b|\bTg\b|\bSyr\b|\bVulg?\b)')


def _zarojelek(s):
    """Felső szintű (…) és […] csoportok listája (beágyazás kezelve)."""
    ki, mely, kezd = [], 0, None
    for i, c in enumerate(s):
        if c in '([':
            if mely == 0:
                kezd = i
            mely += 1
        elif c in ')]' and mely:
            mely -= 1
            if mely == 0 and kezd is not None:
                ki.append((kezd, i + 1))
    return ki


def _szamozott(szoveg, minta_fn, elso):
    """Sorszámozott jelölők keresése szigorú sorrenddel (1, 2, 3 … vagy a, b, c …).
    Visszaad: [(jel, kezdo_index, tartalom_kezdete)]."""
    talalat, varas = [], elso
    for m in minta_fn().finditer(szoveg):
        csop = 1 if m.group(1) is not None else 2
        if m.group(csop) == varas:
            talalat.append((m.group(csop), m.start(csop), m.end()))
            varas = str(int(varas) + 1) if varas.isdigit() else chr(ord(varas) + 1)
    return talalat


def _szam_minta():
    # szám, előtte szóköz/kezdet/gondolatjel, utána szóköz és nem szám/hivatkozás
    # változatok: „— 1 …”, „1. …”, „1.a …” (a betű az alpont), és hivatkozás utáni „… 48:14 2 first”
    return re.compile(r'(?:(?<=—\s)|(?<=[.;:)]\s)|(?<=\d\s)|^)(\d{1,2})(?:\.(?=[a-l]\s)|\.?\s)(?=[^\d\s:,;.)(&])')


def _betu_minta():
    return re.compile(r'(?:(?<=\s)|^)([a-l])\.\s')


def _darabol(szoveg, jelolok):
    ki = []
    for i, (jel, k, t) in enumerate(jelolok):
        v = jelolok[i + 1][1] if i + 1 < len(jelolok) else len(szoveg)
        ki.append((jel, szoveg[t:v].strip(' ;,')))
    return ki


def _jelentesek(regio):
    szamok = _szamozott(regio, _szam_minta, '1')
    if not szamok:
        al = _darabol(regio, _szamozott(regio, _betu_minta, 'a'))
        if al:
            elo = regio[:_szamozott(regio, _betu_minta, 'a')[0][1]].strip()
            return [{'jel': '', 'szoveg': elo, 'ref': len(REF.findall(elo)),
                     'al': [{'jel': j, 'szoveg': t, 'ref': len(REF.findall(t))} for j, t in al]}]
        return [{'jel': '', 'szoveg': regio.strip(), 'ref': len(REF.findall(regio)), 'al': []}]
    elotte = regio[:szamok[0][1]].strip(' —;')
    ki = []
    if elotte:
        ki.append({'jel': '', 'szoveg': elotte, 'ref': len(REF.findall(elotte)), 'al': []})
    for jel, t in _darabol(regio, szamok):
        betuk = _szamozott(t, _betu_minta, 'a')
        if betuk:
            sajat = t[:betuk[0][1]].strip()
            al = [{'jel': j, 'szoveg': s, 'ref': len(REF.findall(s))} for j, s in _darabol(t, betuk)]
        else:
            sajat, al = t, []
        ki.append({'jel': jel, 'szoveg': sajat, 'ref': len(REF.findall(sajat)) + sum(a['ref'] for a in al), 'al': al})
    return ki


def _egy(szoveg):
    if not szoveg:
        return None
    s = szoveg.replace('\n', ' ').strip()
    # „1.a beginning” → „1. a. beginning” (így a magyar „a” névelő nem téveszthető alpontnak)
    s = re.sub(r'(?<=[\s—])(\d{1,2})\.([a-l])\s', r'\1. \2. ', s)
    fej = {'strong': '', 'atiras': '', 'heber': '', 'ossz': ''}
    m = re.match(r"^(H\d+)\.\s+(\S+(?:\s')?)\s+(?:([IVX]+)\.\s+)?\[?([^\s\]_]+)\]?(?:_(\d+))?\s", s)
    if m:
        fej = {'strong': m.group(1), 'atiras': m.group(2), 'homonima': m.group(3) or '', 'heber': m.group(4), 'ossz': m.group(5) or ''}
        torzs = s[m.end():]
    else:
        torzs = s
    # a jelentésrégió kezdete: az első törzs-fejléc (igék), különben az első sorrendhelyes „1”
    tf = list(TORZS_FEJ.finditer(torzs))
    if not tf and re.search(r'\b(ige|verb)\b', torzs[:120]):
        # igék _N nélküli törzs-fejlécei: gondolatjel vagy mondatvég után álló törzsnév
        kezd = re.compile(r'(?:(?<=—\s)|(?<=\.\s))(' + TORZS + r')(?=[\s,.:])')
        jel, lat = [], set()
        for t in kezd.finditer(torzs):
            if t.group(1) not in lat:
                lat.add(t.group(1))
                jel.append(t)
        if len(jel) >= 1:
            tf = jel
    szamok = _szamozott(torzs, _szam_minta, '1')
    if tf:
        rk = tf[0].start()
    elif szamok:
        rk = szamok[0][1]
    else:
        rk = len(torzs)
    eleje, regio = torzs[:rk], torzs[rk:]
    # eleje: alapjelentés + nyelvi háttér + alaktan (gondolatjelek mentén)
    darabok = [d.strip(' —;') for d in re.split(r'\s—\s', eleje) if d.strip(' —;')]
    fo = darabok[0] if darabok else ''
    alaktan = ' — '.join(darabok[1:])
    nyelvi, alap, utolso = [], [], 0
    for a, b in _zarojelek(fo):
        csoport = fo[a:b]
        if NYELV.search(csoport) or SIGLA.search(csoport):
            nyelvi.append(csoport.strip('()[] '))
            alap.append(fo[utolso:a])
            utolso = b
    alap.append(fo[utolso:])
    alapjelentes = re.sub(r'\s{2,}', ' ', ''.join(alap)).strip(' :;,')
    # törzsek
    torzsek = []
    if tf:
        for i, t in enumerate(tf):
            v = tf[i + 1].start() - rk if i + 1 < len(tf) else len(regio)
            resz = regio[t.start() - rk + len(t.group(0)):v]
            db = t.group(2) if t.re.groups >= 2 else ''
            torzsek.append({'nev': t.group(1).replace('`', "'"), 'db': db, 'jelentesek': _jelentesek(resz)})
    else:
        torzsek.append({'nev': '', 'db': '', 'jelentesek': _jelentesek(regio)})
    return {
        'fej': fej,
        'alap': alapjelentes,
        'nyelvi': nyelvi,
        'alaktan': alaktan,
        'torzsek': torzsek,
        'irodalom': sorted(set(SIGLA.findall(s))),
        'krit': sorted(set(x.replace(' ', '') for x in KRIT.findall(s))),
        'ref_ossz': len(REF.findall(s)),
    }


POS = r"(?:verb|noun|adjective|adverb|preposition|conjunction|particle|pronoun|interjection|ige|főnév|melléknév|határozószó|elöljárószó|kötőszó|partikula|névmás|indulatszó)"
CIM = re.compile(r"(?<=[\s.;—])((?:IV|VI|V|I{1,3}))\.\s+(?=\[?[\u0590-\u05ff]+\]?\s+" + POS + r"\b)")


def _kons(x):
    return re.sub(r"[\u0591-\u05c7]", "", x or "")


def szeletel(szoveg, lemma=""):
    """Egy BDB-sor szeletelése. Ha a sor több szócikket (homonimát) tartalmaz — zárójeles előszócikk, „I. / II. / IV. <héber szó> <szófaj>”
    címszavak, arámi (Pe`al) rész —, akkor szakaszokra bontja; a Strong-számhoz tartozó szakasz (a Strong-lemma mássalhangzó-vázával
    egyező első címszó) a fő elemzés, a többi a `szakaszok` listába kerül, szerepjelöléssel (elo / azonos_lemma / masik_lemma)."""
    if not szoveg:
        return None
    s = szoveg.replace("\n", " ").strip()
    mf = re.match(r"^(H\d+)\.\s+(\S+(?:\s')?)\s+", s)
    heads = [m for m in CIM.finditer(s) if mf and m.start() > mf.end()]
    if not heads:
        r = _egy(szoveg)
        r['elotag'] = ''
        r['szakaszok'] = []
        return r
    strong, atiras = mf.group(1), mf.group(2)
    hatarok = [0] + [m.start() for m in heads] + [len(s)]
    szakaszok = []
    for i in range(len(hatarok) - 1):
        resz = s[hatarok[i]:hatarok[i + 1]].strip()
        if i > 0:
            resz = "%s. %s %s" % (strong, atiras, resz)
        e = _egy(resz)
        if not e or not e['fej']['heber']:
            continue
        szakaszok.append({'jel': (heads[i - 1].group(1) if i > 0 else e['fej'].get('homonima', '')), 'szoveg': resz, 'e': e})
    if not szakaszok:
        r = _egy(szoveg)
        r['elotag'] = ''
        r['szakaszok'] = []
        return r
    if lemma:
        fo = next((k for k, x in enumerate(szakaszok) if _kons(x['e']['fej']['heber']) == _kons(lemma)), 0)
    else:
        fo = 0
    r = dict(szakaszok[fo]['e'])
    ki = []
    for k, x in enumerate(szakaszok):
        if k == fo:
            continue
        e = x['e']
        elo = k == 0 and not x['jel']
        stems = ' '.join(t['nev'] for t in e['torzsek'])
        ki.append({
            'jel': x['jel'], 'heber': e['fej']['heber'],
            'szerep': 'elo' if elo else ('azonos_lemma' if lemma and _kons(e['fej']['heber']) == _kons(lemma) else 'masik_lemma'),
            'nyelv': 'arámi' if ARAMI_TORZS.search(x['szoveg']) and not re.search(r'\bQal\b', x['szoveg']) else 'héber',
            'alap': e['alap'], 'nyelvi': e['nyelvi'], 'torzsek': e['torzsek'], 'ref': e['ref_ossz'],
            'zarojeles': bool(re.match(r"^H\d+\.\s+\S+(?:\s')?\s+(?:[IVX]+\.\s+)?\[", x['szoveg'])),
        })
    elotag = ''
    if szakaszok[0]['jel'] == '' and fo != 0:
        elotag = re.sub(r"^H\d+\.\s+\S+(?:\s')?\s+", '', szakaszok[0]['szoveg']).strip(' —;')
    r['elotag'] = elotag
    r['szakaszok'] = ki
    r['ref_ossz'] = szakaszok[fo]['e']['ref_ossz']
    return r


if __name__ == '__main__':
    import json
    import os
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    import tempfile
    d = json.load(open(os.path.join(tempfile.gettempdir(), 'olvaso_pilot', 'olvaso_pilot.json'), encoding='utf-8'))
    for k in sys.argv[1:]:
        l = d['lapok'][k]
        r = szeletel(l['bdb_hu'] or l['bdb_en'])
        print('=====', k, r['fej'], '| ref', r['ref_ossz'])
        print('ALAP:', r['alap'][:160])
        print('NYELVI:', [x[:80] for x in r['nyelvi']])
        print('ALAKTAN:', r['alaktan'][:120])
        for t in r['torzsek']:
            print(' TÖRZS', t['nev'], t['db'])
            for j in t['jelentesek']:
                print('   ', j['jel'], '|', j['szoveg'][:70], '| ref', j['ref'], '| al:', [a['jel'] for a in j['al']])
        print('IROD:', r['irodalom'][:8], 'KRIT:', r['krit'])
