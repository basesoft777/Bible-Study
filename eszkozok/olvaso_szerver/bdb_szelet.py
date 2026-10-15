"""BDB-szócikk gépi szeletelése apparátusokra. Élesben a szerver mellett (DT-F99c (a), F99 M2); a pilot és az M0 mérőeszköz
az `eszkozok/olvaso_pilot/bdb_szelet.py` betöltőn át ugyanezt a modult használja. Csak szerkezetet bont, értelmezés nincs:
címszó, alapjelentés, nyelvi háttér, alaktan, törzsek (igéknél), jelentésszerkezet (1, 2 … / a, b …),
igehely-hivatkozások száma, irodalmi és szövegkritikai jelek. A határok heurisztikusak."""
import re

TORZS = (r"Qal|Niph`al|Pi`el|Pu`al|Hiph`il|Hoph`al|Hithpa`el|Hithpe`el|Hithpo`el|Hithpalpel|"
         r"Pilpel|Polpal|Polel|Polal|Po`el|Po`al|Pil`el|Pul`al|Pual|Piel|Hiphil|Niphal|Hophal|Ishtaphel|Tiph`el|"
         r"Pe`al|Pa`el|Aph`el|Haph`el|Shaph`el|Ithpe`el|Ithpa`al|Ithpa`el|Ithpo`el|Hithpe`el|Hithpa`al|Pe`il|Ishtaph`al")
ARAMI_TORZS = re.compile(r"Pe`al|Pa`el|Aph`el|Haph`el|Shaph`el|Ithpe`el|Ithpa`al|Ithpa`el|Ithpo`el|Hithpe`el|Hithpa`al|Pe`il|Ishtaph`al")
TORZS_FEJ = re.compile(r'(?<![\w`])(' + TORZS + r')(?:_(\d+)|(?=\s+(?:\([^)]{0,40}\)\s+)?(?:perfectum|imperfectum|participium|imperativus|infinitivus|'
                       r'Perfect|Imperfect|Participle|Imperative|Infinitive)))')
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


SZOFAJ_RE = re.compile(r"\b(?:verb|noun|adjective|adverb|preposition|conjunction|particle|pronoun|interjection|ige|főnév|melléknév|"
                       r"határozószó|elöljárószó|kötőszó|partikula|névmás|indulatszó|tulajdonnév)\b")


def _zarojelben(szoveg, max_hossz=400):
    """Logikai lista: a szöveg adott pozíciója felső szintű (…) vagy […] csoporton belül van-e. A csoport csak akkor számít, ha a záró
    zárójel `max_hossz` karakteren belül megvan (a csonka, lezáratlan zárójel nem némít el mindent utána)."""
    ki = [False] * (len(szoveg) + 1)
    i = 0
    n = len(szoveg)
    while i < n:
        if szoveg[i] in '([':
            mely, j = 0, i
            while j < n and j - i <= max_hossz:
                if szoveg[j] in '([':
                    mely += 1
                elif szoveg[j] in ')]':
                    mely -= 1
                    if mely == 0:
                        break
                j += 1
            if j < n and j - i <= max_hossz and mely == 0:
                for k in range(i, j + 1):
                    ki[k] = True
                i = j + 1
                continue
        i += 1
    return ki


def _szamozott(szoveg, minta_fn, elso, laza_fn=None, laza_elso=False):
    """Sorszámozott jelölők keresése szigorú sorrenddel (1, 2, 3 … vagy a, b, c …).
    Visszaad: [(jel, kezdo_index, tartalom_kezdete)]. A `laza_fn` (csak számokhoz) egy lazább mintát ad: ha a várt sorszám a szigorú
    mintával nem található a már megtalált jelölők után, de a laza minta (kisbetűs szó után, kisbetűs szó előtt álló szám) megtalálja,
    az számít jelölőnek (a magyar fordítás néha elhagyja a jelölő előtti írásjelet: „… a participiumot 2 ritkábban …”). Az első jelölőre
    (az „1”-re) a laza minta csak `laza_elso` esetén él (igetörzs szövege: „— megölni, halálra adni 1 abszolút használatban”)."""
    talalat, varas, poz = [], elso, 0
    bent = _zarojelben(szoveg)
    while True:
        van = None
        for fn in ((minta_fn, laza_fn) if (laza_fn and (talalat or laza_elso)) else (minta_fn,)):
            for m in fn().finditer(szoveg, poz):
                csop = 1 if m.group(1) is not None else 2
                if fn is laza_fn and not _laza_ok(szoveg, m.start(1)):
                    continue
                if m.group(csop) == varas and not bent[m.start(csop)]:
                    van = (m.group(csop), m.start(csop), m.end())
                    break
            if van:
                break
        if not van:
            return talalat
        talalat.append(van)
        poz = van[2]
        varas = str(int(varas) + 1) if varas.isdigit() else chr(ord(varas) + 1)


# Alakok személy-szám jelölése („1. egyes szám אֵהָ֑ב”, „3. nőnemű egyes szám …”, „2. hímnemű többes szám suffixummal …”): a szám PONTTAL áll,
# utána héber alak vagy alaktani szó (a táblán 1615 pontos és 5 pont nélküli előfordulás). A pont nélküli „3 többes szám מִשְׁכָּנוֺת, lakóhelyek”
# (H4908), valamint az „egyes számú főnévvel”, „többes számban”, „egyes szám: úr” jelentés-sorszám.
PERSON = (r'(?:(?:hímnemű|nőnemű|közös)\s+)?(?:egyes|többes)\s+szám\s+(?:suffixummal|consecutivummal|cohortativus|jussivus|'
          r'[֐-׿יִ-ﭏ])')


# Az angol alaklista személyszáma pont nélkül is áll („3 feminine singular כָּֽלְתָה 1Sam 20:7”, „1 singular suffix”; F99 M2, aranyminta
# 2.3/1): nem jelölő, ha utána suffix/consecutive, vagy héber alak és utána héber, zárójel, „+”, „;”, szám vagy igehely jön (a H4908
# „3 plural מִשְׁכָּנוֺת, dwellings” és a H0776 „5 plural אֲרָצוֺת is almost wholly late” valódi jelentés). A „2 2nd son” jelölő (H0029).
# A héber alak után vesszővel álló igehely is alaklista (H1157 „1 plural בַּעֲדֵנוּ, Amos 9:10”).
PERSON_EN = (r'(?:masculine\s+|feminine\s+|common\s+)?(?:singular|plural)\s+(?:suffix\b|consecutive\b|'
             r'[֐-׿׳][^\s,]*(?![^\s,])\s*(?=[֐-׿׳(+;]|\d|,?\s*[1-3]?[A-Z][a-z]{0,8}\.?\s+\d))')
# A magyar fordítás pont nélküli személyszáma (H1157 „1 többes szám בַּעֲדֵנוּ, Ámós 9:10”) ugyanezzel a feltétellel: a héber alakot
# héber, zárójel, „+”, „;”, szám vagy (vesszővel) igehely követi; a H4908 „3 többes szám מִשְׁכָּנוֺת, lakóhelyek” jelentés marad.
PERSON_HU_PONT_NELKUL = (r'(?:(?:hímnemű|nőnemű|közös)\s+)?(?:egyes|többes)\s+szám\s+[\u0590-\u05ff׳][^\s,]*(?![^\s,])\s*'
                         r'(?=[\u0590-\u05ff׳(+;]|\d|,?\s*[1-3]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,8}\.?\s+\d)')
# könyvnév része (F99 M2, aranyminta 2.3/2): „1 Kings 21”, „1 Samuel 14”, „2 Chron”
KONYV_SZAM = r'(?:Kings|Samuel|Chronicles|Chron|Sam|Kin|Ki|Chr|Kgs)\b'


def _szam_minta():
    # szám, előtte szóköz/kezdet/gondolatjel, utána szóköz és nem szám/hivatkozás
    # változatok: „— 1 …”, „1. …”, „1.a …” (a betű az alpont), és hivatkozás utáni „… 48:14 2 first”
    # a „1. egyes szám”, „3. nőnemű”, „2. hímnemű többes szám” alak-személyek nem jelentés-sorszámok (H0157, H1869, H7121)
    return re.compile(r'(?:(?<=—\s)|(?<=[.;:)]\s)|(?<=\d\s)|^)(?!\d{1,2}\.\s+' + PERSON + r')(?!\d{1,2}\.?\s+' + PERSON_EN + r')(?!\d{1,2}\s+' + PERSON_HU_PONT_NELKUL + r')(?!\d\s+' + KONYV_SZAM + r')(\d{1,2})(?:\.(?=[a-l]\s)|\.?\s)(?=[^\d\s:,;.)(&]|\d{1,2}(?:st|nd|rd|th)\b)'
                      r'(?!\S*\^)')


def _laza_ok(szoveg, poz):
    """A laza jelölő előtti szó kisbetűs, csupa betű (nem „Qal 3”, „Ézs 2”, sigla vagy héber szó)."""
    m = re.search(r'(\S+)\s$', szoveg[max(0, poz - 40):poz])
    return bool(m) and m.group(1).isalpha() and m.group(1)[0].islower()


def _szam_laza():
    # laza sorszám-jelölő: kisbetűs magyar szó + szóköz + szám + szóköz + kisbetűs szó („… értelemben 3 présben tapos …”)
    return re.compile(r'(?<=[a-záéíóöőúüű]\s)(\d{1,2})\s(?=[a-záéíóöőúüű]{2})')


def _betu_minta():
    return re.compile(r'(?:(?<=\s)|^)([a-l])\.\s')


def _darabol(szoveg, jelolok):
    ki = []
    for i, (jel, k, t) in enumerate(jelolok):
        v = jelolok[i + 1][1] if i + 1 < len(jelolok) else len(szoveg)
        ki.append((jel, szoveg[t:v].strip(' ;,')))
    return ki


def _jelentesek(regio, laza_elso=False):
    """Jelentés-szerkezet egy törzs (vagy a teljes szócikk) szövegéből. Az „alakok; — 1 jelentés …” szerkezetben az alak-lista (benne a
    „1. egyes szám”, „3. nőnemű” személyszámokkal, amelyek nem jelölők) előtagként külön elem marad, a számozás az első valódi „1”-nél indul."""
    szamok = _szamozott(regio, _szam_minta, '1', _szam_laza, laza_elso)
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


_ROVIDITES_UTAN = re.compile(r'(?<![\wáéíóöőúüű])(?:olv|vö|l|stb|pl|ti|kb|ill|v)\.\s$')


def _rovidites_utan(szoveg, poz):
    """Igaz, ha a `poz` előtt rövidítés + pont áll („olv. Qal, vö. …”, „l. Niph`al”): a törzsnév ilyenkor hivatkozás, nem fejléc."""
    return bool(_ROVIDITES_UTAN.search(szoveg[max(0, poz - 8):poz]))


def _egy(szoveg):
    if not szoveg:
        return None
    s = szoveg.replace('\n', ' ').strip()
    # „1.a beginning” → „1. a. beginning” (így a magyar „a” névelő nem téveszthető alpontnak)
    s = re.sub(r'(?<=[\s—])(\d{1,2})\.([a-l])\s', r'\1. \2. ', s)
    fej = {'strong': '', 'atiras': '', 'heber': '', 'ossz': ''}
    HEB = "[\u0590-\u05ff\ufb1d-\ufb4f]"
    m2 = re.match(r"^(H\d+)\.\s+((?:(?!\[?" + HEB + r")[^\u0590-\u05ff\ufb1d-\ufb4f]){1,80}?)\s*(?:([IVX]+)\.\s+)?\[?(" + HEB + r"[^\s\]_,;:]*)\]?,?(?:_(\d+))?", s)
    m = re.match(r"^(H\d+)\.\s+(\S+(?:\s')?)\s+(?:([IVX]+)\.\s+)?\[?([^\s\]_]+)\]?(?:_(\d+))?\s", s)
    if m2:
        fej = {'strong': m2.group(1), 'atiras': m2.group(2).strip(), 'homonima': m2.group(3) or '', 'heber': m2.group(4), 'ossz': m2.group(5) or ''}
        torzs = s[m2.end():].lstrip(' ,;:')
    elif m:
        fej = {'strong': m.group(1), 'atiras': m.group(2), 'homonima': m.group(3) or '', 'heber': m.group(4), 'ossz': m.group(5) or ''}
        torzs = s[m.end():]
    else:
        torzs = s
    # a jelentésrégió kezdete: az első törzs-fejléc (igék), különben az első sorrendhelyes „1”
    # a „Név alakcsoport” fejléc (_N nélkül) csak gondolatjel, mondatvég, pontosvessző vagy zárójel-vég után törzs-fejléc; mondat közben
    # („l. fent Niph`al perfectum …”, „(vagy Qal imperfectum …)”) hivatkozás az alakra, nem új törzs
    # Főnév-szócikkben (nem ige) a „Név alakcsoport” sor az etimológiában álló hivatkozás (H4908: „… Pe`al imperfectum … lakik”), nem fejléc.
    ige = bool(re.search(r'\b(ige|verb)\b', torzs[:120]))
    tf = [t for t in TORZS_FEJ.finditer(torzs)
          if t.group(2) is not None
          or (ige and (t.start() == 0
                       or (torzs[max(0, t.start() - 2):t.start()] in ('— ', '. ', '; ', ') ') and not _rovidites_utan(torzs, t.start()))))]
    if ige:
        # igék _N nélküli törzs-fejlécei: gondolatjel vagy mondatvég után álló törzsnév. A már megtalált törzsek mellé csak az
        # még hiányzó nevű törzsek kerülnek (a „Name_N” és a „Name <alakcsoport>” fejlécek elsőbbséget élveznek).
        kezd = re.compile(r'(?:(?<=—\s)|(?<=\.\s))(' + TORZS + r')(?=[\s,.:])')
        van = {t.group(1) for t in tf}
        for t in kezd.finditer(torzs):
            if t.group(1) not in van and not _rovidites_utan(torzs, t.start()):
                van.add(t.group(1))
                tf.append(t)
        tf.sort(key=lambda t: t.start())
    szamok = _szamozott(torzs, _szam_minta, '1', _szam_laza)
    if tf:
        rk = tf[0].start()
    elif szamok:
        rk = szamok[0][1]
    else:
        rk = len(torzs)
    eleje, regio = torzs[:rk], torzs[rk:]
    # eleje: alapjelentés + nyelvi háttér + alaktan (gondolatjelek mentén)
    darabok = [d.strip(' —;,') for d in re.split(r'\s—\s', eleje) if d.strip(' —;,')]
    k = 0
    if len(darabok) > 1 and not SZOFAJ_RE.search(darabok[0]):
        k = next((i for i, d in enumerate(darabok) if i and SZOFAJ_RE.search(d[:50])), 0)
    fo = darabok[k] if darabok else ''
    alaktan = ' — '.join(darabok[:k] + darabok[k + 1:])
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
            torzsek.append({'nev': t.group(1).replace('`', "'"), 'db': db, 'jelentesek': _jelentesek(resz, True)})
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



# ---------- alapjelentés (a szó-lap fejlécéhez) ----------
HEB_BETU = re.compile(r"[֐-׿יִ-ﭏ]")
HEB_FUTAM = re.compile(r"[֐-׿יִ-ﭏ]+(?:,?_\d+)?")
GORBETU = re.compile(r"[Ͱ-Ͽ]")
SZOFAJ = ("főnév|ige|melléknév|tulajdonnév|határozószó|névmás|partikula|sorszámnév|elöljárószó|kötőszó|istennév|népnév")
CSAK_SZOFAJ = re.compile(r"hímnemű|nőnemű|közös|többes|egyes|számú|szám|főnév|ige|melléknév|tulajdonnév|határozószó|elöljárószó|kötőszó|névmás|[\[\]:,.\s]")
VEZETO = re.compile(r"^(?:és|vagy|csak|mindig|többes számban|egyes számban|többes szám|egyes szám|gyűjtőnév|hímnemű|nőnemű|közös nem)\s+", re.I)


def _tisztit_alap(alap):
    """A magyar BDB-sor elejéből (a szeletelő `alap` mezője: címszó-maradék, átírás, héber alakok, szófaj, jelentés) a magyar
    jelentés-rész: héber betűk, zárójeles részek, forrás-hivatkozások, szófaji szavak és átírás-maradékok nélkül. Üres, ha nem marad
    használható szöveg."""
    s = alap
    for _ in range(3):
        s = re.sub(r"\([^()]*\)", " ", s)
    s = re.sub(r"\^\S+(?:\s+\d+(?::\d+)?(?:-\d+)?)?", " ", s)
    s = HEB_FUTAM.sub(" ", s)
    s = re.sub(r"_\d+", " ", s)
    s = re.sub(r"\b[A-Z][a-z]?\^\S+|\bl\.\s+(?:lent|fent|ott)\b", " ", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    s = re.sub(r"([,;:])\s*(?=[,;:.])", "", s)
    kp = re.search(r"(?:%s)[^:;]{0,70}?:\s*" % SZOFAJ, s)
    if kp:
        t = s[kp.end():]
        # több egymás utáni „szófaj: ” előtag (pl. „melléknév: sorszámnév: második”) mind kiesik
        for _ in range(3):
            m2 = re.match(r"(?:%s)[^:;]{0,70}?:\s*" % SZOFAJ, t)
            if not m2:
                break
            t = t[m2.end():]
    else:
        poz = list(re.finditer(r"\b(?:%s)\b\s*" % SZOFAJ, s))
        t = s[poz[-1].end():] if poz else s
    t = t.lstrip(" ,:;.=")
    t = re.split(r";|\. |\[|\(", t)[0]
    tagok = []
    for x in re.split(r",\s*", t):
        y = x.strip()
        for _ in range(4):
            y = VEZETO.sub("", y)
        y = re.sub(r"\s+(?:mindig|csak)\b.*$", "", y, flags=re.I)
        y = re.sub(r"\s+(?:a|az|és|vagy|szóval)$", "", y, flags=re.I).strip()
        if (not y or len(y) > 40 or re.search(r"\d|:|suffix|status|stb|\bl\.", y, re.I) or GORBETU.search(y)
                or re.match(r"(?:fia|lánya|leánya|apja|atyja|neje)\b", y, re.I)):
            break
        tagok.append(y)
        if len(tagok) >= 3 or len(", ".join(tagok)) > 70:
            break
    ki = ", ".join(tagok)
    ki = re.sub(r"[\s,:;.]+$", "", ki)
    ki = re.sub(r"^[\s,:;.=]+", "", ki)
    ki = re.sub(r"(?:,\s*)?\b(?:és|vagy)$", "", ki).strip()
    if re.search(r"-(?:\s|,|$)", ki):
        return ""
    if (len(ki) < 2 or not re.search(r"[a-záéíóöőúüű]{2}", ki, re.I) or re.fullmatch(r"(?:participium|igenévi melléknév)", ki, re.I)
            or HEB_BETU.search(ki)):
        return ""
    return ki


def alap_jelentes(alap):
    """A szó-lap fejlécének alapjelentése a magyar BDB-sorból: {'szoveg', 'tisztitott'} vagy None (ekkor a Strong-szótár rövid jelentése áll).
    Egy rövid, tiszta első jelentés-sor változtatás nélkül marad („ige: felelni, válaszolni”); ha az héber betűt, hivatkozást vagy csak
    szófajt tartalmaz, vagy hosszú, a gépi tisztítás adja a magyar jelentés-részt."""
    if not alap:
        return None
    t = re.split(r";| — |\(", re.sub(r",_\d+", "", alap))[0].strip()
    tiszta = bool(t) and not HEB_BETU.search(t) and not re.search(r"\bl\.\s", t) and len(CSAK_SZOFAJ.sub("", t)) > 2
    if tiszta and len(t) <= 70 and "^" not in t:
        return {"szoveg": t, "tisztitott": False}
    c = _tisztit_alap(alap)
    return {"szoveg": c, "tisztitott": True} if c else None


# ---------- igehely-hivatkozások feloldása és jelentésponthoz kötése (F99 M2, DT-F99a) ----------
# A könyvalakok a BDB-forrás javításának eszközéből jönnek (eszkozok/bdb_konyv_javit.py: TOKEN, TAPADT_SZAM, CSUPASZ, LEK,
# LANCTORO, TOBBERTELMU; a normalizal.py APOKRIF_ALIAS-a), lustán betöltve: a szerver csak akkor húzza be, ha hivatkozást old fel.
_KONYV = None


def _konyvtabla():
    global _KONYV
    if _KONYV is None:
        import importlib
        import os
        import sys
        esz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if esz not in sys.path:
            sys.path.insert(0, esz)
        _KONYV = importlib.import_module('bdb_konyv_javit')
    return _KONYV


def lapit(szoveg):
    """A szócikk szövege abban az alakban, amelyen a szeletelő dolgozik (`_egy`): sortörés szóközre, „1.a” → „1. a.”. A hivatkozások
    `poz` mezője és a csomópont-sávok erre a szövegre vonatkoznak."""
    s = (szoveg or '').replace('\n', ' ').strip()
    return re.sub(r'(?<=[\s—])(\d{1,2})\.([a-l])\s', r'\1. \2. ', s)


# Irodalmi jel (sigla) a hivatkozás előtt (DT-F99a (1)): a hivatkozás közvetlenül a `^`-hoz tapad („De^Job 34:36”: kommentár-hely) —
# kiszűrve; `^`-os szó a megelőző két szóban — `bizonytalan`; a nemi tanú („noun masculine^Gen 1:27”: hol igazolt a nem) bibliai hivatkozás.
_SIGLA_KOZEL = re.compile(r'\S*\^\S*(?:\s+[^\s;()]+){0,2}\s*$')
_NEMI_TANU = re.compile(r'(?:masculine|feminine|plural|singular|hímnemű|nőnemű|főnév|_\d+)$')
_FOLYTATAS = re.compile(r'\s*,\s*(\d{1,3})(?:\s*-\s*\d{1,3})?(?=[\s,;.)\]]|$)(?!\s*:)')
# egyfejezetes könyv fejezetszám nélkül (DT-F99a (4)): „Obad 8”, „Obadiah 13” → 1. fejezet
_EGYFEJEZETES = re.compile(r'(?<![A-Za-z0-9])(Obad|Obadiah)\.?\s+(\d{1,2})(?![\d:])')


def hivatkozasok(szoveg):
    """Az igehely-hivatkozások sorrendben, a `lapit(szoveg)` pozícióival: dict(poz, veg, nyers, konyv (Károli-rövidítés vagy None),
    c, v, konyv_mod ('kiirt' | 'orokolt' | 'folytatas' | 'feloldhatatlan'), okkod).
    okkod: '' (bibliai, feloldott) | 'nem_bibliai' | 'sigla_tapadt' (mindkettő kiszűrendő, DT-F99a (1)) | 'sigla_kozel' | 'tobbertelmu' |
    'ismeretlen_alak' | 'nincs_elozmeny' (a bizonytalanok a táblában maradnak). A könyv a szócikk elejéig visszafelé öröklődik."""
    K = _konyvtabla()
    s = lapit(szoveg)
    tok = []
    for m in K.TOKEN.finditer(s):
        tok.append((m.start(), m.end(), m.group(1), int(m.group(2)), int(m.group(3)), m.group(0)))
    for m in K.TAPADT_SZAM.finditer(s):
        tok.append((m.start(), m.end(), m.group(1) + m.group(2), int(m.group(3)), int(m.group(4)), m.group(0)))
    for m in _EGYFEJEZETES.finditer(s):
        tok.append((m.start(), m.end(), 'Obad', 1, int(m.group(2)), m.group(0)))
    kiirt = {}
    for t in tok:
        kiirt.setdefault(t[0], t)
    lefedett = set()
    for t in kiirt.values():
        lefedett.update(range(t[0], t[1]))
    for m in K.CSUPASZ.finditer(s):
        if m.start() not in lefedett:
            kiirt.setdefault(m.start(), (m.start(), m.end(), None, int(m.group(1)), int(m.group(2)), m.group(0)))
    ki, utolso = [], None
    for p in sorted(kiirt):
        a, e, alak, c, v, nyers = kiirt[p]
        if alak is not None:
            n = alak.rstrip('.')
            if n in K.LEK:
                konyv, ok = K.LEK[n], ''
            elif n in K.LANCTORO or n in K.N.APOKRIF_ALIAS:
                konyv, ok = None, 'nem_bibliai'
            elif n in K.TOBBERTELMU:
                konyv, ok = None, 'tobbertelmu'
            else:
                konyv, ok = None, 'ismeretlen_alak'
            mod = 'kiirt'
            utolso = (konyv, ok)
        elif utolso is None:
            konyv, ok, mod = None, 'nincs_elozmeny', 'feloldhatatlan'
        else:
            (konyv, ok), mod = utolso, 'orokolt'
        sajat = ok
        if ok == '':
            if a and s[a - 1] == '^':
                elotte = re.search(r'(\S*)\s*\^$', s[max(0, a - 30):a]).group(1)      # „masculine_79 ^Exod 4:8”: a szóköz is megengedett
                if not _NEMI_TANU.search(elotte):
                    sajat = 'sigla_tapadt'
            elif _SIGLA_KOZEL.search(s[max(0, a - 40):a]):
                sajat = 'sigla_kozel'
        ki.append({'poz': a, 'veg': e, 'nyers': nyers, 'konyv': konyv, 'c': c, 'v': v, 'konyv_mod': mod, 'okkod': sajat})
        q = e
        while True:
            f = _FOLYTATAS.match(s, q)
            if not f:
                break
            ki.append({'poz': f.start(1), 'veg': f.end(), 'nyers': f.group(0).strip(), 'konyv': konyv, 'c': c, 'v': int(f.group(1)),
                       'konyv_mod': 'folytatas', 'okkod': sajat})
            q = f.end()
    return ki


def _szakasz_cimke(x):
    if x['jel']:
        return x['jel']
    return 'h:' + _kons(x['heber'])


def csomopont_savok(szoveg, r):
    """A szeletelő csomópontjainak sávjai a `lapit(szoveg)`-ben: [(kezdet, veg, szakasz, utvonal, szint)]. A szakasz '' (fő), római
    szám, vagy 'h:<mássalhangzó-váz>'; az útvonal `<törzs>/<jelentés>/<alpont>` (hiányzó szint: '-'), mint az aranymintában. A sáv a
    csomópont saját szövege (a jelentésé az alpontjai nélkül); a keresés szöveg-egyezéssel megy, a szakaszon belül sorrendben."""
    s = lapit(szoveg)
    savok = []

    def keres(szak, ut, szint, szov, kurzor):
        t = (szov or '').strip()
        if not t:
            return kurzor
        i = s.find(t, kurzor)
        if i < 0:
            i = s.find(t)
        if i < 0:
            return kurzor
        savok.append((i, i + len(t), szak, ut, szint))
        return i + len(t)

    def torzsek(szak, tl):
        kurzor = 0
        for t in tl:
            tn = t['nev'] or '-'
            for j in t['jelentesek']:
                jp = '%s/%s' % (tn, j['jel'] or '-')
                kurzor = keres(szak, jp, 'jelentes', j['szoveg'], kurzor)
                for a in j['al']:
                    kurzor = keres(szak, '%s/%s' % (jp, a['jel']), 'alpont', a['szoveg'], kurzor)
    torzsek('', r['torzsek'])
    for x in r.get('szakaszok', []):
        torzsek(_szakasz_cimke(x), x['torzsek'])
    return sorted(savok)


def jelentespont(poz, savok):
    """A `poz`-t tartalmazó legszűkebb sáv (szakasz, utvonal); a csomópontokon kívül (címsor, nyelvi háttér, alaktan) ('', 'fej')."""
    jo = [x for x in savok if x[0] <= poz < x[1]]
    if not jo:
        return '', 'fej'
    x = min(jo, key=lambda y: y[1] - y[0])
    return x[2], x[3]


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
