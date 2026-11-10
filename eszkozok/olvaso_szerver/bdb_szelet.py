"""BDB-szócikk gépi szeletelése apparátusokra. Élesben a szerver mellett (DT-F99c (a), F99 M2); a pilot és az M0 mérőeszköz
az `eszkozok/olvaso_pilot/bdb_szelet.py` betöltőn át ugyanezt a modult használja. Csak szerkezetet bont, értelmezés nincs:
címszó, alapjelentés, nyelvi háttér, alaktan, törzsek (igéknél), jelentésszerkezet (1, 2 … / a, b …),
igehely-hivatkozások száma, irodalmi és szövegkritikai jelek. A határok heurisztikusak."""
import re
import unicodedata

TORZS = (r"Qal|Niph`al|Pi`el|Pu`al|Hiph`il|Hoph`al|Hithpa`el|Hithpe`el|Hithpo`el|Hithpalpel|"
         r"Pilpel|Polpal|Polel|Polal|Po`el|Po`al|Pil`el|Pul`al|Pual|Piel|Hiphil|Niphal|Hophal|Ishtaphel|Tiph`el|"
         r"Pe`al|Pa`el|Aph`el|Haph`el|Shaph`el|Ithpe`el|Ithpa`al|Ithpa`el|Ithpo`el|Hithpe`el|Hithpa`al|Pe`il|Ishtaph`al")
# a forrás változatos törzsnév-írásai egy alakra (F99 M2: a vak minta-ellenőrzés a „Piel”-t és a „Pi`el”-t egynek veszi)
TORZS_KANON = {'Pual': "Pu'al", 'Piel': "Pi'el", 'Hiphil': "Hiph'il", 'Niphal': "Niph'al", 'Hophal': "Hoph'al", 'Ishtaphel': "Ishtaph'el"}
ARAMI_TORZS = re.compile(r"Pe`al|Pa`el|Aph`el|Haph`el|Shaph`el|Ithpe`el|Ithpa`al|Ithpa`el|Ithpo`el|Hithpe`el|Hithpa`al|Pe`il|Ishtaph`al")
# seed-100 (H7832): OCR-ban a törzsnév a „Perfect”-hez tapadhat („— QalPerfect3masculine singular”)
TORZS_FEJ = re.compile(r'(?<![\w`])(' + TORZS + r')(?:_(\d+)|(?=\s*(?:\([^)]{0,40}\)\s+)?(?:perfectum|imperfectum|participium|imperativus|infinitivus|'
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
                if fn is laza_fn and not _laza_ok(szoveg, m.start(1), bool(talalat)):
                    continue
                if m.group(csop) == varas and not bent[m.start(csop)]:
                    van = (m.group(csop), m.start(csop), m.end())
                    break
            if van:
                break
        if not van and talalat and varas.isdigit():
            van = _hezag(szoveg, poz, varas, minta_fn, bent)
        if not van and talalat and varas in OCR_BETU:
            # seed-100 (H2022): OCR-torzult alpont-jelölő a sorozat folytatásában — „l.” helyett „1”, „m.” helyett „masculine”
            # (ELLENOR_F99_minta E1: az OCR-torzult jelölő is jelölő)
            m = next((m for m in OCR_BETU[varas].finditer(szoveg, poz) if not bent[m.start(1)]), None)
            if m:
                van = (varas, m.start(1), m.end())
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
    # F123 (2026-10-29): a szögletes zárójellel záruló szakasz utáni szám is jelölő („… post-Biblical Judaism and NT.] 4 ׳שׁ
    # figurative …”, H7585); a teljes BDB-n 7 szócikk 184 sora kap helyes jelentéspontot (naplok/F123_bdb_szelet_meres.tsv)
    return re.compile(r'(?:(?<=—\s)|(?<=\s-\s)|(?<=;-\s)|(?<=[.;:)\]]\s)|(?<=\d\s)|^)(?!\d{1,2}\.\s+' + PERSON + r')(?!\d{1,2}\.?\s+' + PERSON_EN + r')(?!\d{1,2}\s+' + PERSON_HU_PONT_NELKUL + r')(?!\d\s+' + KONYV_SZAM + r')(\d{1,2})(?:\.(?=[a-l]\s)|\.?\s)(?![a-e][;,]\s)(?=[^\d\s:,;.)(&]|\d{1,2}(?:st|nd|rd|th)\b|[1-3][A-Z][a-z]+\.?\s+\d|\((?:c\.|kb\.|approximately|about)?\s*\d+\s*(?:t\.|times|-?szor|-?szer|-?ször)[);])'
                      r'(?!\S*\^)')


OCR_BETU = {'l': re.compile(r'(?<=[.;]\s)(1)\s(?=[a-z]{2})'), 'm': re.compile(r'(?<=[.;]\s)(masculine)\s(?=[a-z]{2})')}


def _laza_ok(szoveg, poz, folytatas=False):
    """A laza jelölő előtti szó kisbetűs, csupa betű (nem „Qal 3”, „Ézs 2”, sigla vagy héber szó). F99 M2: a sorozat folytatásában
    (2-től) héber szó is állhat előtte, ha utána kisbetűs szó jön („… see חתם 2 false prophets”, H5030)."""
    m = re.search(r'(\S+)\s$', szoveg[max(0, poz - 40):poz])
    if not m:
        return False
    w = m.group(1)
    if w.isalpha() and w[0].islower():
        return True
    return folytatas and bool(re.fullmatch(r'[\u0590-\u05ff]+', w)) and bool(re.match(r'\d{1,2}\.?\s[a-záéíóöőúüű]{2}', szoveg[poz:]))


def _hezag(szoveg, poz, varas, minta_fn, bent):
    """F99 M2 hézagpótlás: ha a várt n. jelölő sem szigorú, sem laza mintával nem található, de az n+1. szigorúan igen, akkor a kettő
    között az első kisbetűs szó után álló, szóval (bármilyen betűvel vagy héberrel) folytatódó n az n. jelölő („… compare ההוא ביום 7g
    below 4 Plural days of any one: a. …  5 Days: …”, H3117)."""
    kov = str(int(varas) + 1)
    q = next((m.start(1 if m.group(1) is not None else 2) for m in minta_fn().finditer(szoveg, poz)
              if (m.group(1) if m.group(1) is not None else m.group(2)) == kov and not bent[m.start(1 if m.group(1) is not None else 2)]), None)
    if q is None:
        return None
    # a személyszám és a könyvnév része itt sem jelölő („perfectum 3. hímnemű egyes szám suffixummal”, H4191)
    kizar = (r'(?!\d{1,2}\.\s+' + PERSON + r')(?!\d{1,2}\.?\s+' + PERSON_EN + r')(?!\d{1,2}\s+' + PERSON_HU_PONT_NELKUL + r')'
             r'(?!\d\s+' + KONYV_SZAM + r')(?!\d{1,2}\.?\s+(?:hímnemű|nőnemű|közös|egyes|többes|masculine|feminine|common|singular|plural)\b)')
    for m in re.finditer(r'(?<=[a-záéíóöőúüű]\s)' + kizar + r'(' + varas + r')\.?\s(?=[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű\u0590-\u05ff][^\s:]*\s)',
                         szoveg[:q]):
        if m.start(1) >= poz and not bent[m.start(1)] and _laza_ok(szoveg, m.start(1)):
            return (varas, m.start(1), m.end())
    return None


def _szam_laza():
    # laza sorszám-jelölő: kisbetűs szó + szóköz + szám (+ pont) + szóköz + kisbetűs szó, névelő vagy héber szó („… értelemben 3 présben
    # tapos …”; F99 M2: „… preposition below 4 יָד is used”, „feminine 1. a daughter”); a személyszám- és a könyvnév-kizárás itt is él
    # A héber szó előtti laza szám csak pont nélkül és nem „from/see” után jelölő („from 1. חוּל” homonima-utalás, H2490 II).
    return re.compile(r'(?<=[a-záéíóöőúüű\u0590-\u05ff]\s)(?<!from\s)(?<!see\s)(?<!lásd\s)(?!\d{1,2}\.\s+' + PERSON + r')(?!\d{1,2}\.?\s+' + PERSON_EN + r')(?!\d\s+' + KONYV_SZAM + r')'
                      r'(?!\d{1,2}\.?\s+(?:egyes|többes)\s+szám\s+(?:hímnem|nőnem|közös)\b)'
                      r'(\d{1,2})(?:\.?\s(?=[a-záéíóöőúüű]{2}|a\s[a-z]|\((?:c\.|kb\.|approximately|about)\s*\d+\s*(?:t\.|times|-?szor|-?szer|-?ször)[);])'
                      r'|\s(?=[\u0590-\u05ff]))')


def _betu_minta():
    # F99 M2: a forrásban tapadt alpont-jelölő („Est 3:10. c.as to hands”, H3027 1/c) is jelölő, ha mondatvég után áll („e.g.”, „i.e.” nem)
    return re.compile(r'(?:(?<=\s)|^)([a-l])\.\s|(?:(?<=[.;]\s))([a-l])\.(?![ge]\.)(?=[a-z]{2})')


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
    if not szamok and not laza_elso:
        laza = _szamozott(regio, _szam_minta, '1', _szam_laza, True)
        if len(laza) >= 2 and laza[0][1] < 3:
            szamok = laza
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


def _egy(szoveg, ige_e=None):
    """Egy szakasz elemzése. `ige_e`: kívülről megadott szófaj (a fő tagolás szakaszában nincs „verb”, de a törzsfejlécek igeként
    értendők — F99 M2, H2803 II: „… Niph`al Perfect …”); None: a szakasz saját szövegéből."""
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
    ige = bool(re.search(r'\b(ige|verb)\b', torzs[:120])) if ige_e is None else ige_e
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
    if not tf and not szamok:
        # F99 M2: a felső szint első jelölője laza helyzetben is állhat („— dream 1 ordinary dream”, „hence 1 end”, „feminine 1. a
        # daughter”); csak akkor fogadjuk el, ha a sor legalább a 2-ig folytatódik
        laza = _szamozott(torzs, _szam_minta, '1', _szam_laza, True)
        if len(laza) >= 2:
            szamok = laza
    if not tf and not szamok:
        # F99 M2: az „1” vessző vagy nagybetűs szó mellett áll („— nagy, 1 méretben …”, H1419; „— sea: especially 1 Mediterranean …”,
        # H3220); csak akkor jelölő, ha onnan legalább a 3-ig sorrendben folytatódik a számozás
        bent = _zarojelben(torzs)
        for m in re.finditer(r'(?<=\s)(?!1\s+' + KONYV_SZAM + r')1\.?\s(?=[^\d\s:,;.)(&])', torzs):
            if bent[m.start()]:
                continue
            uj = _szamozott(torzs[m.start():], _szam_minta, '1', _szam_laza)
            # seed-100 (H1138 „proper name, masculine 1. Levites, a. … 2 a chief”): a nemre utaló szó utáni pontos „1.” már a 2-vel is
            nemszo = re.search(r'(?:masculine|feminine|hímnemű|nőnemű)\s$', torzs[max(0, m.start() - 12):m.start()])
            if len(uj) >= 3 or (len(uj) >= 2 and nemszo and torzs[m.start() + 1] == '.'):
                szamok = [(j, k + m.start(), t + m.start()) for j, k, t in uj]
                break
    if not tf and len(szamok) >= 2 and len(torzs[szamok[0][2]:szamok[1][1]]) < 40:
        # F99 M2: a fejléc rövid, számozott glossza-felsorolása („1 devoted thing. 2 devotion, ban; — …”) nem a jelentés-szerkezet; ha a
        # 2. után gondolatjel áll, és onnan új, legalább 1–2-es számozás indul, az a valódi szerkezet (H2764)
        hatar = szamok[2][1] if len(szamok) > 2 else len(torzs)
        g = torzs.find('— ', szamok[1][1], hatar)
        uj = _szamozott(torzs[g:], _szam_minta, '1', _szam_laza) if g >= 0 else []
        if len(uj) >= 2:
            szamok = [(j, k + g, t + g) for j, k, t in uj]
        elif len(szamok) == 2:
            # seed-100 (H0389 „1 surely. 2 with a restrictive force …: a. … b. … Generally, only 1 asseverative … 2 restrictive: a.”): a
            # gondolatjel nélküli összefoglaló után 250 karakteren belül újrainduló (laza vagy szigorú) 1–2-es számozás a valódi szerkezet
            u = szamok[1][2]
            uj = _szamozott(torzs[u:], _szam_minta, '1', _szam_laza, True)
            if len(uj) >= 2 and uj[0][1] < 250:
                szamok = [(j, k + u, t + u) for j, k, t in uj]
    betu_rk = None
    if not tf and not szamok:
        # F99 M2: számozás nélküli, csak betűs alpontok a felső szinten („— wine: a. common drink … b. …”, „— a. of place … b. …”);
        # legalább a b-ig; a régió az alpontot megelőző utolsó gondolatjelnél kezdődik (ott a jelentés feje áll)
        betuk = _szamozott(torzs, _betu_minta, 'a')
        if len(betuk) >= 2:
            g = torzs.rfind('— ', 0, betuk[0][1])
            betu_rk = g + 2 if g >= 0 else betuk[0][1]
    # seed-100 (H6331 „[מָּרַר] verb Hiph`il break, frustrate …; — Perfect … — 1 break, violate … Hoph`al …”): a fejlécben megnevezett
    # egyetlen törzs („verb Hiph`il”, „verb only Hiph`il”) a később álló törzsfejléc előtti számozott jelentések törzse
    fej_torzs = None
    if ige and tf:
        mh = re.search(r'\b(?:verb|ige)\s+(?:only\s+|csak\s+)?(' + TORZS + r')\b', torzs[:150])
        if mh and mh.group(1) not in {t.group(1) for t in tf} and _szamozott(torzs[:tf[0].start()], _szam_minta, '1'):
            g = torzs.find('— ', mh.end(), tf[0].start())
            fej_torzs = (mh.group(1), g if g >= 0 else mh.end())
    if fej_torzs:
        rk = fej_torzs[1]
    elif tf:
        rk = tf[0].start()
    elif szamok:
        rk = szamok[0][1]
    elif betu_rk is not None:
        rk = betu_rk
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
    if fej_torzs:
        nev = fej_torzs[0].replace('`', "'")
        torzsek.append({'nev': TORZS_KANON.get(nev, nev), 'db': '', 'jelentesek': _jelentesek(regio[:tf[0].start() - rk], True)})
    if tf:
        for i, t in enumerate(tf):
            v = tf[i + 1].start() - rk if i + 1 < len(tf) else len(regio)
            resz = regio[t.start() - rk + len(t.group(0)):v]
            db = t.group(2) if t.re.groups >= 2 else ''
            nev = t.group(1).replace('`', "'")
            torzsek.append({'nev': TORZS_KANON.get(nev, nev), 'db': db, 'jelentesek': _jelentesek(resz, True)})
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
# F99 M2 (seed-100): a héber betűosztály a prezentációs alakokat (U+FB1D–FB4F, pl. „שׂ” FB2B, „שׁ” FB2A) is fedi (H7704, H4911), és a
# címszó két alakkal is állhat („II. בָּ֑ד בַּד, noun masculine”, H0905)
HB = "\u0590-\u05ff\ufb1d-\ufb4f"
CIM = re.compile(r"(?<=[\s.;—])((?:IV|VI|V|I{1,3}))\.\s+(?=\[?[" + HB + r"]+\]?(?:\s+\[?[" + HB + r"]+\]?){0,2}(?:_\d+)?,?(?:_\d+)?\s+"
                 r"(?:(?:and|és)\s+\(\s*[^()]{0,30}\)\s*\[?[" + HB + r"]+\]?,?\s+)?(?:(?:hímnemű|nőnemű|közös|denominativum)\s+)?"
                 r"(?:" + POS + r"\b|with prepositions|elöljárószókkal|proper name|tulajdonnév))")
# F99 M2: jelöletlen második címszó mondathatáron (római szám nélkül): „… Toy). רָעָה_310 noun feminine”, „… 34:10. עַוְלָה noun
# feminine^Job 11:14”, „… (Ew De Di). [שְׁפֵל] verb be low”, „… Qr. יַד noun feminine^Dan 5:5” (H7451, H5766, H8213, H3027)
# seed-100: két alak vesszővel („תּוֺלַ֫עַת תּוֺלֵעָה,_40 noun feminine”, H8438), tulajdonnév („בֻּנִּי proper name”, H1138), és a szófaj
# nélküli, gyakoriság-számmal jelölt alcímszó („מֵעִם_72 from with or beside”, H5973: a „_N” csak címszón áll)
JELOLETLEN = re.compile(r"(?<=[.;)]\s)(?<![\s(][a-l]\.\s)(?=\[?[" + HB + r"][" + HB + r"־]*\]?(?:\s+[" + HB + r"][" + HB + r"־]*){0,2}(?:,?_\d+)?\s+"
                        r"(?:noun\s+(?:masculine|feminine)|verb\b|adjective\b|proper name\b|(?:hímnemű|nőnemű)\s+főnév|ige\b|"
                        r"melléknév\b|tulajdonnév\b)"
                        r"|\[?[" + HB + r"][" + HB + r"־]*\]?_\d+\s+[a-záéíóöőúüű]{2,})")

# F99 M2: a szócikk római számos fő tagolása (nem homonima): „— inner part midst: I. seldom of things … II. elsewhere of men: 1 …” (H3820),
# „I. between men. 1 … II. between God and man. 1 … III. Phrases.” (H1285), „I. 1. a. Fall out … II. Come into being … III. Be” (H1961).
# A római szám után nem héber szó, hanem glossza vagy sorszám áll; csak az I.-gyel kezdődő, sorrendben folytatódó sorozat számít.
TAGOLAS = re.compile(r"(?:(?<=[.;:)]\s)|(?<=—\s))(I{1,3}|IV|V|VI)\.\s+(?=[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű(]|\d{1,2}\.?\s)(?!(?:q|v|e|i)\.)")
# A sorozat folytatása (II. …) írásjel nélkül is állhat, ha nagybetűs glossza követi: „… see a. (e) above II. Come into being” (H1961).
TAGOLAS_FOLYT = re.compile(r"(?<=\s)(II|III|IV|V|VI)\.\s+(?=[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű])")
ROMAI_SOR = ['I', 'II', 'III', 'IV', 'V', 'VI']
MAGANY_II = re.compile(r"(?<=\s)II\.\s+(?=as\s+(?:preposition|conjunction|adverb|substantive|noun|adjective)\b)")


def _tagolas(s, tilos):
    """A fő tagolás római fejei sorrendben [(poz, római)]; legalább I. és II.; a homonima-fejekkel (tilos) ütköző kimarad."""
    ki, var = [], 0
    jel = sorted({(m.start(), m.group(1)) for m in TAGOLAS.finditer(s)} | {(m.start(), m.group(1)) for m in TAGOLAS_FOLYT.finditer(s)})
    for poz, romai in jel:
        if any(abs(poz - t) <= 2 for t in tilos):
            continue
        if var < len(ROMAI_SOR) and romai == ROMAI_SOR[var]:
            ki.append((poz, romai))
            var += 1
    if len(ki) >= 2:
        return ki
    # F102 (d), seed-101 M130 (H8478 „— 1 as adverb accusative … Ezek 47:1b II. as preposition; … 2 … a. … Hab 3:16”): a magányos
    # „II.” (I. nélkül) akkor fő tagolás, ha szófaj-fej követi („as preposition”); az előtte álló rész római szám nélküli (a forrás nem
    # írja ki az „I.”-t). A teljes BDB-n csak a H8478-ban fordul elő (a többi I. nélküli „II.” arab igetörzs, l. naplo 5.)
    magany = [m.start() for m in MAGANY_II.finditer(s) if not any(abs(m.start() - t) <= 2 for t in tilos)]
    if not ki and len(magany) == 1 and not re.search(r'(?:^|[\s.;:)—])I\.\s', s):
        return [(magany[0], 'II')]
    return []


def _kons(x):
    # a héber prezentációs alakok (U+FB1D–FB4F) kanonikus felbontása után (seed-100: „שׂ” FB2B, H7704)
    return re.sub(r"[\u0591-\u05c7]", "", unicodedata.normalize('NFD', x or ""))


def szeletel(szoveg, lemma=""):
    """Egy BDB-sor szeletelése. Ha a sor több szócikket (homonimát) tartalmaz — zárójeles előszócikk, „I. / II. / IV. <héber szó> <szófaj>”
    címszavak, arámi (Pe`al) rész —, akkor szakaszokra bontja; a Strong-számhoz tartozó szakasz (a Strong-lemma mássalhangzó-vázával
    egyező első címszó) a fő elemzés, a többi a `szakaszok` listába kerül, szerepjelöléssel (elo / azonos_lemma / masik_lemma / tagolas).
    A `tagolas` szerepű szakasz nem homonima, hanem az előtte álló címszó római számos fő tagolása (F99 M2: H1961, H1285, H3820)."""
    if not szoveg:
        return None
    s = szoveg.replace("\n", " ").strip()
    # seed-100 (H9003 בְּ, H9005 לְ): a betű-szócikkek sora „H<szám>.” fej nélkül kezdődik („ב בּ ב,, Bêth, 2nd letter …”); a szakasz-
    # bontás egy belső fejjel fut, a pozíciók az eredeti szövegre visszaszámolva
    eltol = 0
    if not re.match(r"^H\d+\.\s", s):
        s = "H0000. - " + s
        eltol = len("H0000. - ")
    mf = re.match(r"^(H\d+)\.\s+(\S+(?:\s')?)\s+", s)
    romai = [(m.start(), m.group(1)) for m in CIM.finditer(s) if mf and m.start() > mf.end()]
    # a jelöletlen címszó-fej csak akkor, ha nem egy római fej címszava (a „II. חֲמוֺר noun” héber szava ne nyisson új szakaszt; a
    # „II. כֹּחַ and (Dan 11:6) כּוֺחַ noun” alakváltozata sem: mondathatár nélkül, 45 karakteren belül, H3581)
    def _romai_fej_resze(poz):
        return any(0 <= poz - r[0] <= 8 or (0 <= poz - r[0] <= 45 and '. ' not in s[r[0] + 3:poz]) for r in romai)
    heads = sorted(romai + [(m.start(), '') for m in JELOLETLEN.finditer(s)
                            if mf and m.start() > mf.end() + 20 and not _romai_fej_resze(m.start())
                            # a fejléc első mondatában álló alakváltozat („Anathoth עֲנָתוֺת and (1Kin 2:26) עֲנָתֹת proper name”) nem új címszó
                            and re.search(r'[.;]\s', s[mf.end():m.start()])])
    tagolas = _tagolas(s, [h[0] for h in heads]) if mf else []
    tag_poz = {p for p, _ in tagolas}
    heads = sorted(heads + tagolas)
    # F99 M2: igénél a fő tagolás (I., II. …) a Qal-on belüli tagolás; a rákövetkező törzsfejléc („Niph`al Perfect …”, H2803, H1961,
    # H2388) a tagolás végét jelenti, onnan a szöveg a címszó törzseinek folytatása (`folyt`), nem a tagolás része
    folyt_poz = set()
    for j, (p0, _) in enumerate(heads):
        if p0 not in tag_poz:
            continue
        veg0 = heads[j + 1][0] if j + 1 < len(heads) else len(s)
        t0 = next((t for t in TORZS_FEJ.finditer(s, p0 + 3, veg0)), None)
        if t0:
            folyt_poz.add(t0.start())
    heads = sorted(heads + [(p0, '') for p0 in folyt_poz])
    if not heads:
        r = _egy(szoveg)
        r['elotag'] = ''
        r['szakaszok'] = []
        return r
    strong, atiras = mf.group(1), mf.group(2)
    hatarok = [0] + [h[0] for h in heads] + [len(s)]
    szakaszok = []
    for i in range(len(hatarok) - 1):
        resz = s[hatarok[i]:hatarok[i + 1]].strip()
        tag = i > 0 and hatarok[i] in tag_poz
        folyt = i > 0 and hatarok[i] in folyt_poz
        ige_e = None
        if folyt:
            elozo_fo = next((x for x in reversed(szakaszok) if not x['tag'] and not x['folyt']), None)
            resz = "%s. %s %s %s" % (strong, atiras, elozo_fo['e']['fej']['heber'] if elozo_fo else '', resz)
            ige_e = True
        elif tag:
            # fő tagolás: a fejléc-elemzőnek a fő címszó héber alakja kell; a római szám marad a szakasz címkéje. Igénél a szakasz az
            # előző szakasz utolsó törzsében folytatódik (H1961: Qal … I. … II. …; H2803: Qal … I. of man … II. of God … Niph`al …): a
            # törzsnév a szakasz elejére kerül, így a későbbi törzsfejlécek (Niph`al …) is törzsként bomlanak
            elozo_fo = next((x for x in reversed(szakaszok) if not x['tag'] and not x['folyt']), None)
            ige_e = bool(elozo_fo and (any(t['nev'] for t in elozo_fo['e']['torzsek'])
                                       or re.search(r'\b(ige|verb)\b', elozo_fo['szoveg'][:200])))
            fo_heb = elozo_fo['e']['fej']['heber'] if elozo_fo else ''
            torzs_ny = re.sub(r"^(?:I{1,3}|IV|V|VI)\.\s+", "", resz)
            elozo_t = [t['nev'] for t in szakaszok[-1]['e']['torzsek'] if t['nev']] if szakaszok else []
            if ige_e and elozo_t and not re.match(TORZS, torzs_ny):
                torzs_ny = '. %s — %s' % (elozo_t[-1].replace("'", '`'), torzs_ny)
            resz = "%s. %s %s. %s %s" % (strong, atiras, heads[i - 1][1], fo_heb, torzs_ny)
        elif i > 0:
            resz = "%s. %s %s" % (strong, atiras, resz)
        e = _egy(resz, ige_e)
        if e and tag and szakaszok and e['torzsek'] and not e['torzsek'][0]['nev']:
            # a törzs nélküli tagolás-szakasz az előző szakasz utolsó törzsében folytatódik (H1961: Qal … I. … II. …)
            elozo = [t['nev'] for t in szakaszok[-1]['e']['torzsek'] if t['nev']]
            if elozo:
                e['torzsek'][0]['nev'] = elozo[-1]
        if not e or not e['fej']['heber']:
            continue
        if eltol:
            e['fej']['strong'] = ''
        szakaszok.append({'jel': (heads[i - 1][1] if i > 0 else e['fej'].get('homonima', '')), 'szoveg': resz, 'e': e,
                          'kezd': max(0, hatarok[i] - eltol), 'veg': hatarok[i + 1] - eltol, 'tag': tag, 'folyt': folyt})
    if not szakaszok:
        r = _egy(szoveg)
        r['elotag'] = ''
        r['szakaszok'] = []
        return r
    if lemma:
        egyezo = [k for k, x in enumerate(szakaszok)
                  if not x['tag'] and not x['folyt'] and _kons(x['e']['fej']['heber']) == _kons(lemma)]
        # több egyező címszó közül az első igehelyes (H9003: a betű leírása igehely nélküli, a „I. בְּ, preposition” a fő)
        fo = next((k for k in egyezo if szakaszok[k]['e']['ref_ossz'] > 0), egyezo[0] if egyezo else None)
        if fo is None:
            # F99 M2: a lemma egyik címszóval sem egyezik (H4325 מַיִם: „II. [מוֺ] = מַי víz. [מַי]_580 hímnemű főnév …”) — a fő elemzés az
            # első olyan (nem tagolás-) szakasz, amelyben van igehely: az igehely nélküli utaló csonk („= מַי víz.”) nem fő elemzés
            fo = next((k for k, x in enumerate(szakaszok) if not x['tag'] and not x['folyt'] and x['e']['ref_ossz'] > 0), 0)
    else:
        fo = 0
    # a törzs-folytatás (folyt) szakasz a gazdájához (az előtte álló utolsó címszó-szakaszhoz) tartozik: törzsei a gazda törzsei mögé
    gazda, utolso = {}, 0
    for k, x in enumerate(szakaszok):
        if x['folyt']:
            gazda.setdefault(utolso, []).append(x)
        elif not x['tag']:
            utolso = k
    r = dict(szakaszok[fo]['e'])
    r['torzsek'] = list(r['torzsek']) + [t for x in gazda.get(fo, []) for t in x['e']['torzsek']]
    r['folyt_savok'] = [(x['kezd'], x['veg']) for x in gazda.get(fo, [])]
    def cimke(k):
        # a szakasz címkéje a sávokban: a fő szakaszé a saját homonima-száma, a többié a római száma vagy h:<váz>
        if k == fo:
            return szakaszok[fo]['e']['fej'].get('homonima', '') or ''
        x = szakaszok[k]
        return x['jel'] or 'h:' + _kons(x['e']['fej']['heber'])
    gazda_tag, utolso_fo = {}, 0
    for k, x in enumerate(szakaszok):
        if x['tag']:
            gazda_tag[k] = cimke(utolso_fo)
        elif not x['folyt']:
            utolso_fo = k
    ki = []
    for k, x in enumerate(szakaszok):
        if k == fo or x['folyt']:
            continue
        e = x['e']
        elo = k == 0 and not x['jel']
        stems = ' '.join(t['nev'] for t in e['torzsek'])
        ki.append({
            'jel': x['jel'], 'heber': e['fej']['heber'],
            'szerep': 'elo' if elo else ('tagolas' if x['tag'] else
                                         ('azonos_lemma' if lemma and _kons(e['fej']['heber']) == _kons(lemma) else 'masik_lemma')),
            'nyelv': 'arámi' if ARAMI_TORZS.search(x['szoveg']) and not re.search(r'\bQal\b', x['szoveg']) else 'héber',
            'alap': e['alap'], 'nyelvi': e['nyelvi'], 'torzsek': list(e['torzsek']) + [t for y in gazda.get(k, []) for t in y['e']['torzsek']],
            'ref': e['ref_ossz'] + sum(y['e']['ref_ossz'] for y in gazda.get(k, [])),
            'folyt_savok': [(y['kezd'], y['veg']) for y in gazda.get(k, [])],
            'zarojeles': bool(re.match(r"^H\d+\.\s+\S+(?:\s')?\s+(?:[IVX]+\.\s+)?\[", x['szoveg'])),
            'kezd': x['kezd'], 'veg': x['veg'],
            # DT-F99i: a fő tagolás (tagolas) szakasza a gazda-címszó homonima-számát is hordozza
            'gazda': gazda_tag.get(k, ''),
        })
    elotag = ''
    if szakaszok[0]['jel'] == '' and fo != 0:
        elotag = re.sub(r"^H\d+\.\s+\S+(?:\s')?\s+", '', szakaszok[0]['szoveg']).strip(' —;')
    r['elotag'] = elotag
    r['szakaszok'] = ki
    r['ref_ossz'] = szakaszok[fo]['e']['ref_ossz'] + sum(y['e']['ref_ossz'] for y in gazda.get(fo, []))
    r['kezd'], r['veg'] = szakaszok[fo]['kezd'], szakaszok[fo]['veg']
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
# F99 M2 (a vak minta után, felhasználói döntés 2026-10-15): a közvetlenül a hivatkozás előtt álló `^`-os sigla-szó (szerző^mű, „Schr^COT
# Gen 2:8”, „Schr^COT on Neh 1:1”, „Schr^ib. 24:1”, „Fl^De Job 6:2”) a tapadt sigla szabályába tartozik: a hely a kommentár helye,
# nem a szó előfordulása. Csak nagybetűvel kezdődő szerző-sigla, írásjel (zárójel, vessző, pontosvessző) nélkül: a „(Kö^ii.l,74) Jer 6:13”,
# „(both R^D), Jer 6:24”, „(Ges^l.c.) Neh 8:10” lezárt megjegyzés után bibliai hely áll; a szövegtanú-sigla („ᵐ5^B Ezra 10:21”,
# „ᵑ7^J Gen 28:17”) a szó saját helyét is jelölheti, ezért marad `sigla_kozel` (bizonytalan). A szám a `^` után könyvrész („Isa^2
# Isa 24:16”, „Isa^3 50:9”: Deutero-/Trito-Ézsaiás), nem kommentár; az „R^D” forráskritikai jel (redaktor), utána bibliai hely áll
# („(compare R^D Josh 13:22)”, H1109). A két szóval távolabbi `^`-os szó továbbra is `sigla_kozel`.
_SIGLA_ELOTTE = re.compile(r'(?:^|\s)(?!R\^)[A-Z][A-Za-zäöü]*\^[^\s),;\]\d][^\s),;\]]*\s+(?:on\s+|in\s+)?$')
# F99 M2 (felhasználó, 2026-10-15, a seed-100 után, DT-F99j): a közeli sigla közül a megnevezett kommentár-siglák a szűrő listáján
# vannak (`sigla_lista`, kiszűrve): Schrader COT („Schr^COT”, „COT on Josh 17:11”), Driver („Dr on 2Sam 8:3”, „Dr^…”), a Mésa-felirat
# („MI^4”), Fleischer/Delitzsch („Fl^De”, „De^…”), Hupfeld („Hup^Now.”). A Targum (ᵑ7) és a LXX (ᵐ5) szövegtanú, nincs a listán
# (felhasználó, 2026-10-15). Minden sigla melletti hivatkozásról a generátorban a TAHOT dönt (DT-F99k: `sigla_igazolt` vagy szűrt).
# A többi `sigla_kozel` bibliai hivatkozásként a táblában marad, okkóddal.
_SIGLA_LISTA = re.compile(r'^(?:Schr\^\S+|COT\.?|Dr|Dr\^\S*|MI|MI\^\S*|Fl\^\S+|De\^\S*|Hup\^\S*)$')
_NEMI_TANU = re.compile(r'(?:masculine|feminine|plural|singular|hímnemű|nőnemű|főnév|_\d+)$')
_FOLYTATAS = re.compile(r'\s*,\s*(\d{1,3})(?:\s*-\s*\d{1,3})?(?=[\s,;.)\]]|$)(?!\s*:)')
# DT382 (A) (felhasználó, 2026-10-28): a kiírt vagy örökölt hivatkozás utáni verstartomány („1Kin 18:24-25, 26”): a tartomány
# átlépése után a vers-folytatás keresése ugyanúgy fut, mint tartomány nélkül; a tartományt nem bontja ki (a „-25” nem lesz sor)
_TARTOMANY = re.compile(r'\s*[-–]\s*(\d{1,3})(?![\d:])')
# F102 (b): az egyfejezetes könyvek (Károli-rövidítés); a könyv nélküli, nem 1. fejezetű hely nem ezeket örökli
EGYFEJEZETES_KONYV = frozenset({'Abd', 'Filem', '2Ján', '3Ján', 'Júd'})
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
    ki, utolso, kint, egyfej_elott, utolso_bibliai = [], None, None, None, None
    bent = _zarojelben(s)
    for p in sorted(kiirt):
        a, e, alak, c, v, nyers = kiirt[p]
        atugrott = False
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
            if konyv in EGYFEJEZETES_KONYV:
                # F102 (b): az egyfejezetes könyv előtti (nem egyfejezetes, bibliai) könyv megjegyezve
                if utolso is not None and utolso[0] and utolso[0] not in EGYFEJEZETES_KONYV:
                    egyfej_elott = utolso
            else:
                egyfej_elott = None
            utolso = (konyv, ok)
            if konyv:
                utolso_bibliai = konyv
            if not bent[a] or ok == '':
                # F99 M2: a zárójelen belüli nem bibliai/ismeretlen könyvjelölő („(… compare also Di 2:2)”, „(Ecclus … Ecclesiasticus
                # 50:12a)”) nem öröklődik a zárójelen kívülre: ott a zárójel előtti könyv folytatódik (H1714, H5409)
                kint = utolso
        elif not bent[a] and kint is not None and utolso != kint:
            (konyv, ok), mod = kint, 'orokolt'
            utolso = kint
        elif utolso is None:
            konyv, ok, mod = None, 'nincs_elozmeny', 'feloldhatatlan'
        else:
            (konyv, ok), mod = utolso, 'orokolt'
        if mod == 'orokolt' and konyv in EGYFEJEZETES_KONYV and c != 1 and egyfej_elott is not None:
            # F102 (b), seed-101 M092: „2Chr 17:2; compare 34:6; … Obadiah 19; hence … 31:1” — az egyfejezetes könyvnek nincs 31.
            # fejezete: a könyv nélküli hely a közbeékelt egyfejezetes könyv előtti könyvet folytatja (2Krón 31:1), okkóddal
            (konyv, ok), atugrott = egyfej_elott, True
        sajat = ok
        if ok == '':
            if a and s[a - 1] == '^':
                elotte = re.search(r'(\S*)\s*\^$', s[max(0, a - 30):a]).group(1)      # „masculine_79 ^Exod 4:8”: a szóköz is megengedett
                if not _NEMI_TANU.search(elotte):
                    sajat = 'sigla_tapadt'
            elif _SIGLA_ELOTTE.search(s[max(0, a - 40):a]):
                sajat = 'sigla_tapadt'
            elif _SIGLA_KOZEL.search(s[max(0, a - 40):a]):
                # a listás kommentár-sigla (sigla_lista) csak a hivatkozással egy tagmondatban számít: lezáró zárójel, pontosvessző,
                # kettőspont vagy gondolatjel után a hely NEM listás, hanem `sigla_kozel` marad („(MI^10) Jer 48:1”, „compare Dr^Amos 4:9:
                # Exod 10:13”, „Dr^Sm; … 1Sam 16:1”); hogy bibliai-e, azt a generátorban a TAHOT dönti el (DT-F99k: `sigla_igazolt` vagy
                # szűrt). (ELLENOR_F99 9.: a korábbi megjegyzés „a hely már bibliai” állítása téves volt; a szabály módosítása — a lezárt
                # megjegyzés utáni hely ne legyen sigla-sor — a javítási feladatban, pl. seed-101 M223.)
                ablak = re.split(r'[)\];:—]', s[max(0, a - 40):a])[-1]
                # a hivatkozás előtt visszafelé csak a héber idézett alak, az „on”/„in” és az „i.” állhat a sigla és a hely között
                # („ᵑ7^Jer כ ׳הֵי Gen 26:4”, „COT on Josh 17:11”); latin szó („compare”, „Glossary and”) vagy szám után a hely önálló
                szavak = [w.strip(',') for w in re.findall(r'[^\s;()]+', ablak)]
                while szavak and (re.fullmatch(r"[\u0590-\u05ff\ufb1d-\ufb4f׳־]+", szavak[-1]) or szavak[-1] in ('on', 'in', 'i.')):
                    szavak.pop()
                sajat = 'sigla_lista' if szavak and _SIGLA_LISTA.match(szavak[-1]) else 'sigla_kozel'
                # F102 (c), seed-101 M223 (ELLENOR_F99 9.): a lezárt zárójeles megjegyzésben álló sigla („Josh 23:7 (R^D), compare
                # Hosea 2:19”, „(Kö^ii.l,74) Jer 6:13”, „(MI^10) Jer 48:1”) után a hely nem sigla-sor: a sigla és a hely között záró
                # zárójel áll, a sigla tehát nem a helyre vonatkozik
                if sajat == 'sigla_kozel':
                    elozo = s[max(0, a - 40):a]
                    if re.search(r'[)\]]', elozo[elozo.rfind('^'):]):
                        sajat = ''
        if atugrott and sajat == '':
            sajat = 'orokles_egyfejezetes'
        hiv = {'poz': a, 'veg': e, 'nyers': nyers, 'konyv': konyv, 'c': c, 'v': v, 'konyv_mod': mod, 'okkod': sajat}
        if sajat == 'nem_bibliai' and mod == 'orokolt' and utolso_bibliai:
            # F102 (c), seed-101 (ELLENOR_F99 12.): a nem bibliai jelölőről öröklődő könyv („see 1Macc 2:42; 7:13; 2 Macc 14:6 …;
            # so perhaps 116:15; 149:1”, H2623) — a jelölő előtti utolsó bibliai könyv a jelölt; a generátor TAHOT-igazolással dönt
            hiv['alt_konyv'] = utolso_bibliai
        ki.append(hiv)
        t = _TARTOMANY.match(s, e)
        q = t.end() if t else e
        while True:
            f = _FOLYTATAS.match(s, q)
            # a tartomány utáni „, 1 Samuel 21:16” „1”-e a következő kiírt hivatkozás kezdete, nem vers-folytatás (DT382 (A)); F102 (g):
            # tartomány nélkül is („2Chr 10:19, 2 Chronicles 10…”, H1004: a „2” könyvnév, nem a 2Krón 10:2)
            if not f or f.start(1) in kiirt:
                break
            ki.append(dict({'poz': f.start(1), 'veg': f.end(), 'nyers': f.group(0).strip(), 'konyv': konyv, 'c': c, 'v': int(f.group(1)),
                            'konyv_mod': 'folytatas', 'okkod': sajat}, **({'alt_konyv': hiv['alt_konyv']} if 'alt_konyv' in hiv else {})))
            q = f.end()
    return ki


# DT-F99i (felhasználó, 2026-10-15): két római szint — a címszó homonima-száma és a szócikk fő tagolása (rész) külön mező. A sávok
# címkéjében a tagolás-szakasz „<homonima>§<rész>” (pl. „III§I”); a `szakasz_bont` választja szét.
RESZ_SEP = '§'


def szakasz_bont(cimke):
    """'III§I' -> ('III', 'I'); 'II' -> ('II', ''); '' -> ('', '')."""
    a, _, b = (cimke or '').partition(RESZ_SEP)
    return a, b


def _szakasz_cimke(x):
    if x.get('szerep') == 'tagolas':
        return '%s%s%s' % (x.get('gazda', ''), RESZ_SEP, x['jel'])
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
    # a fő szakasz a saját római számával (a homonima-sor I., II. … címszava), ha van; különben '' (F99 M2: a szakasz a kulcs része)
    torzsek(r['fej'].get('homonima', '') or '', r['torzsek'])
    for x in r.get('szakaszok', []):
        torzsek(_szakasz_cimke(x), x['torzsek'])
    return sorted(savok)


def szakasz_savok(szoveg, r):
    """A szakaszok (a fő és a többi) sávja a `lapit(szoveg)`-ben: [(kezdet, veg, címke, tagolt)]; `tagolt`: a szakaszban van törzs,
    számozott jelentés vagy alpont. Egyszakaszos szócikknél egy sáv az egész szövegre."""
    s0 = (szoveg or '').replace('\n', ' ').strip()

    def at(p):
        return len(lapit(s0[:p]))

    def tagolt(tl):
        return any(t['nev'] or any(j['jel'] or j['al'] for j in t['jelentesek']) for t in tl)
    if 'kezd' not in r:
        return [(0, len(lapit(szoveg)), r['fej'].get('homonima', '') or '', tagolt(r['torzsek']))]
    ki = [(at(r['kezd']), at(r['veg']), r['fej'].get('homonima', '') or '', tagolt(r['torzsek']))]
    ki += [(at(a), at(b), r['fej'].get('homonima', '') or '', tagolt(r['torzsek'])) for a, b in r.get('folyt_savok', [])]
    for x in r.get('szakaszok', []):
        if 'kezd' in x:
            ki.append((at(x['kezd']), at(x['veg']), _szakasz_cimke(x), tagolt(x['torzsek'])))
            ki += [(at(a), at(b), _szakasz_cimke(x), tagolt(x['torzsek'])) for a, b in x.get('folyt_savok', [])]
    return sorted(ki)


def jelentespont(poz, savok, szakaszok=None):
    """A `poz`-t tartalmazó legszűkebb sáv (szakasz, utvonal). A csomópontokon kívül a hivatkozást tartalmazó szakasz címkéjével:
    'tagolatlan', ha a szakaszban nincs törzs, számozott jelentés vagy alpont, különben 'fej' (címsor, nyelvi háttér, alaktan)."""
    jo = [x for x in savok if x[0] <= poz < x[1]]
    if jo:
        x = min(jo, key=lambda y: y[1] - y[0])
        return x[2], x[3]
    for a, b, cimke, tag in (szakaszok or []):
        if a <= poz < b:
            return cimke, ('fej' if tag else 'tagolatlan')
    return '', 'fej'


# ---------- használati csoportok (F103, FELADATOK #103; DT167) ----------
# A jelentésen (és alponton) belüli használati csoport a DT167 (1) (a) szerint (felhasználó, 2026-10-15): csak mondatkezdő (`;` `.` `:`
# `—` utáni), zárójelen kívüli bevezető a listáról — absolute, followed by, with + héber / accusative / suffix / infinitive, Inf. abs. as
# adverb (a „so” után is), in phrase(s), opposed to, especially (a „; &” után is, aranyminta B2) —, valamint a zárójeles harmadik szint
# `(1)`, `(a)` sorrendben, legalább a második tagig (az OCR-torzult `(I)`, `-2`, a görög `(β)` is jelölő, ELLENOR_F99_minta E1). A so /
# also / often nem nyit csoportot; a csomópont első szava a csomópont feje, nem csoport. A bontás kiegészítő: a `szeletel()` kimenetét
# nem változtatja, a `csoport_bont()` a csomópontokra `csop` listát tesz. Magyarul (DT167 (5) (a)) a bontás csak ott marad, ahol a
# magyar jelölők sorozata (szám és sorrend) az angoléval egyezik (`csoport_magyar`); a „with + héber” csoportnak nincs magyar bevezetője.
_CS_MONDAT = r'(?:(?<=[;.:]\s)|(?<=—\s))'
_CS_HEB = "֐-׿יִ-ﭏ"
_CS_KULCS = {'absolute': 'absolute', 'followed': 'followed by', 'with': 'with', 'figurative': 'figurative', 'infabs': 'Inf. abs. as adverb',
             'phrase': 'in phrase', 'opposed': 'opposed to', 'especially': 'especially'}
_CS_EN = re.compile(_CS_MONDAT + r'(?:'
                    r'(?P<absolute>absolute(?:ly)?\b)'
                    r'|(?P<followed>followed\s+by\b)'
                    r'|(?P<with>[Ww]ith\s+(?=[' + _CS_HEB + r']|(?:accusative|acc|suffix|infinitive|Infinitive|inf)\b))'
                    r'|(?P<figurative>figurative(?:ly)?\b)'
                    r'|(?P<infabs>(?:so\s+)?(?:Inf(?:initive)?\.?|infinitive)\s+abs(?:olute)?\.?\s+(?:as\s+)?adverb)'
                    r'|(?P<phrase>in\s+phrases?\b)'
                    r'|(?P<opposed>opposed\s+to\b)'
                    r'|(?P<especially>(?:&\s+)?especially\b))')
# a magyar fordítás bevezetői: a DT167 (2) kötelező alakja és a kész fordításban élő régi alak (a régi alak is jelölő, csere nincs:
# DT167 (5) (a)); a „követi” hátravetett („infinitivus követi”), mondatkezdő bevezetőként nem ismerhető fel
_CS_HU = re.compile(_CS_MONDAT + r'(?:'
                    r'(?P<absolute>abszolút\s+használatban)'
                    r'|(?P<followed>utána\b)'
                    r'|(?P<figurative>átvitt\s+értelemben|képletesen\b)'
                    r'|(?P<infabs>(?:így\s+)?(?:az\s+)?infinitivus\s+absolutus\s+határozó\w*)'
                    r'|(?P<phrase>kifejezés(?:ek)?ben\b)'
                    r'|(?P<opposed>ellentéte\b|ellentétben\b|szemben\b)'
                    r'|(?P<especially>(?:és\s+)?különösen\b))')
_CS_ZAROJELES = re.compile(r'(?:(?<=\s)|^)\((\d{1,2}|I|[a-h]|[α-θ])\)(?=\s|[' + _CS_HEB + r'])'
                           r'|(?:(?<=[\s;.:])|^)-(\d)(?=[^\d\s:,;.)\-])')
_GOROG = 'αβγδεζηθ'


def _cs_melyseg(t):
    """Igaz-hamis lista: a pozíció zárójelen belül áll-e — a szeletelő `_zarojelben` szabálya (a csoport csak 400 karakteren belüli
    lezárással számít: a lezáratlan OCR-zárójel — „עַליֿד(יׅ:”, H3027 5/h — nem némít el mindent utána)."""
    return _zarojelben(t)


# A zárójeles jelölő nem a prózai felsorolás tagja: ha az első 40 karakteren (a csomópont fején) túl áll, előtte nem prózai kötő- vagy
# viszonyszó van („developed … by (1) the prefixing … and (2) the addition …”, H0834 etimológiája); a hivatkozás-sor utáni „+ often (b)”
# (H6440 II 6/c) és a fejben álló jelölő („of divine love (a) to individual men”, H0157 5.) jelölő.
_CS_PROZA_ELOTTE = re.compile(r'(?<![A-Za-z])(and|or|by|of|to|the|in|with|from|that|as)\s$')


def _cs_zarojeles(t, mely):
    """A zárójeles harmadik szint jelölői sorrendben: [(kezdet, vég, jel)]. Sorozat 1-től (vagy a-tól), legalább a második tagig; a jel
    az aranyminta alakja: „(2)” (az OCR „-2” és „(I)” = „(1)” is), „(a)”, „(β)”."""
    sor, tipus, varas, ki = [], None, 1, []

    def lezar():
        if len(sor) >= 2:
            ki.extend(sor)

    for m in _CS_ZAROJELES.finditer(t):
        # a jelölő maga zárójel: a körülötte álló zárójelet az előtte álló pozíció mutatja
        if m.start() > 0 and mely[m.start() - 1]:
            continue
        if m.group(1) is not None and m.start() >= 40:
            if _CS_PROZA_ELOTTE.search(t[max(0, m.start() - 10):m.start()]):
                continue
        cimke = m.group(1) if m.group(1) is not None else m.group(2)
        if cimke == 'I' or cimke.isdigit():
            tp, idx, jel = 'szam', 1 if cimke == 'I' else int(cimke), '(%s)' % (1 if cimke == 'I' else int(cimke))
        elif m.group(2) is None:
            tp = 'betu'
            idx = (_GOROG.index(cimke) + 1) if cimke in _GOROG else ord(cimke) - ord('a') + 1
            jel = '(%s)' % cimke
        else:
            continue
        if m.group(2) is not None and tp != 'szam':
            continue
        if sor and tp == tipus and idx == varas:
            sor.append((m.start(), m.end(), jel))
            varas += 1
        elif idx == 1 and (not sor or tp != tipus):
            lezar()
            sor, tipus, varas = [(m.start(), m.end(), jel)], tp, 2
    lezar()
    return sorted(ki)


def _csoportok(t, nyelv='en'):
    """Egy csomópont saját szövegének használati csoportjai: [{'jel', 'kezd', 'szoveg'}] (a `kezd` a szövegen belüli eltolás)."""
    if not t:
        return []
    mely = _cs_melyseg(t)
    lex = [(m.start(), m.end(), _CS_KULCS[m.lastgroup]) for m in (_CS_HU if nyelv == 'hu' else _CS_EN).finditer(t)
           if not mely[m.start()]]
    zar = _cs_zarojeles(t, mely)
    kezdetek = []
    zar_kezd = {z[0]: z for z in zar}
    elnyelt = set()
    for a, b, kulcs in lex:
        # a bevezető közvetlenül a zárójeles jelölő előtt („especially (3) ביד נתן”, H3027 5/b): egy csoport, a zárójeles jelölővel
        z = next((z for z in zar if z[0] >= b and not t[b:z[0]].strip()), None)
        if z:
            elnyelt.add(z[0])
            kezdetek.append((a, z[2]))
        else:
            kezdetek.append((a, kulcs))
    kezdetek += [(z[0], z[2]) for z in zar if z[0] not in elnyelt]
    kezdetek = sorted(set(k for k in kezdetek if k[0] > 0))
    ki = []
    for i, (k, jel) in enumerate(kezdetek):
        v = kezdetek[i + 1][0] if i + 1 < len(kezdetek) else len(t)
        ki.append({'jel': jel, 'kezd': k, 'szoveg': t[k:v].strip(' ;,')})
    return ki


def csoport_bejar(r, fo_homonima=False):
    """A szeletelő csomópontjai (jelentés, alpont) a csoportbontáshoz: [(szakasz-címke, útvonal, csomópont-dict)]. A fő szakasz címkéje
    '' (az aranyminta alakja), `fo_homonima` esetén a saját homonima-száma (a 2.29 alakja, mint a `csomopont_savok`-ban)."""
    ki = []

    def torzsek(szak, tl):
        for t in tl:
            tn = t['nev'] or '-'
            for j in t['jelentesek']:
                jp = '%s/%s' % (tn, j['jel'] or '-')
                ki.append((szak, jp, j))
                for a in j['al']:
                    ki.append((szak, '%s/%s' % (jp, a['jel']), a))
    torzsek((r['fej'].get('homonima', '') or '') if fo_homonima else '', r['torzsek'])
    for x in r.get('szakaszok', []):
        torzsek(_szakasz_cimke(x), x['torzsek'])
    return ki


def csoport_bont(r, nyelv='en'):
    """A csomópontokra `csop` lista (helyben; vissza is adja). A törzs számozott jelentései előtti számozatlan elem (az alak-lista:
    „Perfect … Inf. abs. …”) nem kap csoportot: ott az „absolute” és az „Inf. abs.” alaktan, nem használat (DT167 (1) (a))."""
    if not r:
        return r

    def torzsek(tl):
        for t in tl:
            szamozott = any(j['jel'] for j in t['jelentesek'])
            for j in t['jelentesek']:
                j['csop'] = [] if (szamozott and not j['jel']) else _csoportok(j['szoveg'], nyelv)
                for a in j['al']:
                    a['csop'] = _csoportok(a['szoveg'], nyelv)
    torzsek(r['torzsek'])
    for x in r.get('szakaszok', []):
        torzsek(x['torzsek'])
    return r


def csoport_magyar(r_hu, r_en):
    """DT167 (5) (a): a magyar csomópont csoportjai csak ott maradnak, ahol a magyar jelölő-sorozat (szám és sorrend) azonos az angol
    szócikk ugyanazon csomópontjáéval (szakasz + útvonal); máshol a magyar csomópont bontás nélkül áll. Mindkét elemzésen előbb
    `csoport_bont` fut (magyarul `nyelv='hu'`)."""
    if not r_hu or not r_en:
        return r_hu

    def sorozatok(r):
        d = {}
        for szak, ut, n in csoport_bejar(r):
            d.setdefault((szak, ut), []).extend(c['jel'] for c in n.get('csop') or [])
        return d
    en, hu = sorozatok(r_en), sorozatok(r_hu)
    for szak, ut, n in csoport_bejar(r_hu):
        if hu.get((szak, ut)) != en.get((szak, ut)):
            n['csop'] = []
    return r_hu


def csoport_savok(szoveg, r):
    """A használati csoportok sávjai a `lapit(szoveg)`-ben, a `csomopont_savok` keresésével: [(kezdet, vég, szakasz, '<útvonal>/+<n>',
    'csoport', jel)]; a csomópontokon előbb `csoport_bont` fut. A sorszám a csomóponton belüli (1-től), mint az aranyminta `+n`-je; a
    szakasz-címke a `csomopont_savok`-é (a fő szakasz a saját homonima-számával)."""
    s = lapit(szoveg)
    savok = []
    sorszam = {}

    def keres(szak, ut, node, kurzor):
        t0 = node.get('szoveg') or ''
        t = t0.strip()
        if not t:
            return kurzor
        i = s.find(t, kurzor)
        if i < 0:
            i = s.find(t)
        if i < 0:
            return kurzor
        lead = len(t0) - len(t0.lstrip())
        cs = node.get('csop') or []
        for k, c in enumerate(cs):
            a = i + c['kezd'] - lead
            b = i + (cs[k + 1]['kezd'] - lead if k + 1 < len(cs) else len(t))
            n = sorszam[(szak, ut)] = sorszam.get((szak, ut), 0) + 1
            savok.append((a, b, szak, '%s/+%d' % (ut, n), 'csoport', c['jel']))
        return i + len(t)

    kurzor = {}
    for szak, ut, node in csoport_bejar(r, fo_homonima=True):
        kurzor[szak] = keres(szak, ut, node, kurzor.get(szak, 0))
    return sorted(savok)


# ---------------------------------------------------------------------------------------------------------------------
# A vers -> jelentés tábla (`adat/bdb_vers_jelentes.tsv`, SEMA 2.29) sorainak minősítése: EGY helyen, mert az olvasó-szerver
# BDB-blokkja (`blokkok.VersJelolo`) és a lexikon-generátor 4.2-es kártyája (`lexikon_general.bdb_olvasoi_reteg`) is ezt
# használja (DT-F104d; egy szabály, egy hely).
# ---------------------------------------------------------------------------------------------------------------------
def vj_feloldott(r):
    """A pontos hivatkozásszám alapja (#104 brief 2.: „a feloldott, szűrt hivatkozásoké”): nem szűrt, feloldott (maszoréta
    versszámmal bíró) bibliai hivatkozás. A Károli-vers nem feltétel."""
    return r.get('szurt') != '1' and bool(r.get('mt_vers'))


# a táblában maradó bizonytalan sorok okkódjai (SEMA 2.29 `okkod`: „bizonytalan, a táblában marad”), a kézzel azonosított hibás
# forrás-hely és a bizonytalan versszám-megfeleltetés: az ilyen hivatkozás pontja csak gyenge jelölést kap (DT178, DT-F104e)
BIZONYTALAN_OK = {'sigla_kozel': 'a hely mellett kommentár-jel áll', 'tobbertelmu': 'a könyvnév rövidítése többértelmű',
                  'ismeretlen_alak': 'a könyvnév alakja ismeretlen', 'nincs_elozmeny': 'a könyv nem állapítható meg',
                  'orokles_hibas': 'az örökölt könyvben nincs ilyen fejezet', 'forras_hiba': 'a BDB nyomtatott igehelye hibás'}
BIZONYTALAN_VERS = {'atkulcsolt_bizonytalan': 'a héber és a Károli-versszámozás megfeleltetése bizonytalan'}


def vj_bizonytalan(r):
    """A sor bizonytalanságának okai (olvasói szöveg); üres lista: biztos sor."""
    okok = [BIZONYTALAN_OK[o] for o in (r.get('okkod') or '').split(',') if o in BIZONYTALAN_OK]
    if r.get('vers_feloldas') in BIZONYTALAN_VERS:
        okok.append(BIZONYTALAN_VERS[r['vers_feloldas']])
    return okok


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
