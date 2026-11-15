"""lapgen.bemenet.kartya — a 4.2 kártya szövegeinek feldolgozása (S3b): a szótári szöveg szegmentált idézetként.

A régi generátor a kártya szövegét (a szakasz magyar fordítását) szövegcserék láncán vitte át: kiemelés, forrásjavítás,
irányjel, rövidítés-feloldás, Károli-számozás, majd a kész lapon írásjel-takarítás, a BDB belső számlálóinak törlése,
kiejtés-pótlás és a digitalizálás jeleinek törlése. Itt ugyanezek a szabályok futnak, ugyanabban a sorrendben, de a
szöveg `Jelolt` (szegmentált idézet): a jelölés típusos darab, a forrásjavítás az idézet betűit cseréli, és egyik
művelet sem nyúlhat a jelölés vagy a keret belsejébe (kimondott hiba).

A bekezdés (`Bekezdes`) a régi generátor egy bekezdése: keret-darabok (a régi Markdown-keret belső alakja, a lapra nem
kerül, csak a minták látják) és `Jelolt` sorok. A minták a régi bekezdés teljes szövegén futnak, ezért a döntésük a régivel
azonos; a változtatás csak a `Jelolt` idézet-darabjait érheti.

A régi lánc olvasói átírásának tartalmi cseréi (zsargon, fájlnév, belső szavak) az idézeten nem futnak: idézetet nem
írunk át (DT-F212e); a két mintalapon nem fordulnak elő (a regresszió méri).
"""
import re
import unicodedata

import bdb_rovidites
import bdb_vj_szabaly

from lapgen.bemenet import szavak as szavak_be
from lapgen.bemenet.jelolt import Feloldas, FeloldasFajta, JelFajta, Jeloles, Jelolt, JeloltHiba

# --- hivatkozások a szövegben (a régi `hivatkozasok_a_szovegben`, a kiemelés mércéje) --------------------------------
_KONYV_RE = re.compile(r'((?:[1-3])?[A-ZÁÉÍÓÖŐÚÜŰ][A-Za-záéíóöőúüűÁÉÍÓÖŐÚÜŰ]*)\s+$')
_FV_RE = re.compile(r'(?<![\w:^])(\d+):(\d+)(?![\d])')
_FOLYT_RE = re.compile(r'(?:\s*[-–]\s*\d+(?![\d:]))?\s*,\s*(\d+)(?![\d:\w])(?!\s+[A-ZÁÉÍÓÖŐÚÜŰ])')


def hivatkozasok(szoveg):
    """[(kezdet, vég, könyv, fejezet, vers)]: a szöveg fejezet:vers hivatkozásai és vers-folytatásai; a könyv a közvetlenül
    előtte álló könyvnévből, ennek híján a legutóbbi kiírt könyvből (a szótár folytatásos írásmódja)."""
    out, aktualis = [], None
    for m in _FV_RE.finditer(szoveg):
        elotte = szoveg[max(0, m.start() - 12):m.start()]
        km = _KONYV_RE.search(elotte)
        kezdet = m.start()
        if km:
            aktualis = km.group(1)
            kezdet = m.start() - len(elotte) + km.start()
        out.append((kezdet, m.end(), aktualis, m.group(1), m.group(2)))
        q = m.end()
        while True:
            f = _FOLYT_RE.match(szoveg, q)
            if not f:
                break
            out.append((f.start(1), f.end(1), aktualis, m.group(1), f.group(1)))
            q = f.end()
    return out


# --- a Károli-számozás hivatkozásai (a régi `szotari_hivatkozasok`) -----------------------------------------------------
_HIV_TOK = re.compile(r'(?P<k>(?<![\w])(?:[1-5])?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,6})\s(?P<c>\d{1,3}):(?P<v>\d{1,3})(?![\d:])'
                      r'|(?<![\w:.])(?P<c2>\d{1,3}):(?P<v2>\d{1,3})(?![\d:])'
                      r'|(?<=, )(?P<v3>\d{1,3})(?![\d:])')


def szotari_hivatkozasok(szoveg):
    """[(match, könyv, fejezet, vers)] a könyv és a fejezet öröklésével („5Móz 29:11, 13; 30:1”)."""
    ki, konyv, fej, elozo_veg = [], None, None, -10
    for m in _HIV_TOK.finditer(szoveg):
        if m.group('k'):
            konyv, fej, vers = m.group('k'), m.group('c'), m.group('v')
        elif m.group('c2'):
            if konyv is None:
                elozo_veg = m.end()
                fej = m.group('c2')
                continue
            fej, vers = m.group('c2'), m.group('v2')
        else:
            if konyv is None or fej is None or m.start() - elozo_veg != 2:
                continue
            vers = m.group('v3')
        elozo_veg = m.end()
        ki.append((m, konyv, fej, vers))
    return ki


# --- a vázlatsor: az első tagmondat (a régi `_elso_tagmondat`) ------------------------------------------------------
CSONK_SZOKOZZEL, CSONK_TAPADT = ' …', '…'


def elso_tagmondat(szoveg, hatar=90, csonkit_jel=False):
    """(a szöveg első tagmondata a forrás részleteként, a csonkítás jele vagy None). A jel a generátoré (sablon)."""
    s = re.sub(r'^\s*(?:(?:\d+|[a-z]|T:\S+)\.?\s+){1,2}', '', szoveg or '').strip()
    csonk = None
    m = next((m for m in re.finditer(r'(?<!\d):|:(?!\d)|;', s)
              if s[:m.start()].count('(') <= s[:m.start()].count(')')), None)
    if m and m.start() <= hatar:
        folytatodik = bool(s[m.end():].strip(' .;:'))
        s = s[:m.start()]
        if csonkit_jel and folytatodik:
            s, csonk = s.rstrip(' ,;:'), CSONK_SZOKOZZEL
    elif len(s) > hatar:
        s = s[:hatar].rstrip()
        if s.count('(') > s.count(')'):
            s = s[:s.rfind('(')].rstrip(' ,;')
        csonk = CSONK_TAPADT
    while s.count('(') > s.count(')') and s.rfind('(') > 0:
        s, csonk = s[:s.rfind('(')].rstrip(' ,;'), CSONK_TAPADT
    s = s.lstrip() if csonk else s.strip()
    if not s:
        raise JeloltHiba('a vázlatsor üres maradna (a régi lap itt gondolatjelet írt): %r' % (szoveg or '')[:60])
    return s, csonk


# --- glosszák (a régi `alak_utani_glossza`, `gondolatjel_utani_glossza`, `fej_glossza`) ------------------------------
_ALAK_UTAN = re.compile(r'[֐-׿יִ-ﭏ][^\s]*\s*(?:\([^)]*\)\s*)?\u200e?\s*'
                        r'([a-záéíóöőúüű][a-záéíóöőúüű ,]*?)(?=\s*(?:[1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,6}\s+)?\d+:\d+'
                        r'|\s*[;(.:]|[\s,]*[֐-׿יִ-ﭏ]|$)')
_ALAKTANI_KEZDET = re.compile(r'(?i)(?:perfectum|imperfectum|participium|infinitivus|imperativus|status|suffixum|többes '
                              r'szám|egyes szám|hímnemű|nőnemű|jussivus|cohortativus)\b')


def alak_utani_glossza(szoveg):
    """Az alakjegyzékkel nyíló szakasz magyar meghatározása az alak után, vagy None."""
    for m in _ALAK_UTAN.finditer(szoveg or ''):
        g = m.group(1).strip(' ,')
        if len(g) >= 3 and not _ALAKTANI_KEZDET.match(g) and not re.fullmatch(r'(?:és|vagy|mind|stb)', g):
            return g
    return None


def gondolatjel_utani_glossza(hu):
    """A törzs-szakasz glosszája a gondolatjel után (a régi F182 A17 szabálya), vagy None."""
    def jo(g):
        return g and 3 <= len(g) <= 80 and not re.search(r'[֐-׿יִ-ﭏ\d]', g) and not _ALAKTANI_KEZDET.match(g)
    for m in re.finditer(r'\s—\s+([a-záéíóöőúüű][^;(.:]*?)\s*(?=[;(.:]|$)', hu or ''):
        if jo(m.group(1).strip(' ,')):
            return m.group(1).strip(' ,')
    m = re.search(r'^\S+:\s+([a-záéíóöőúüű][^;(.:]*?)(?=,\s*(?:perfectum|imperfectum|participium|infinitivus)|[;(.:]|$)',
                  hu or '')
    g = m.group(1).strip(' ,') if m else (alak_utani_glossza(hu) or '')
    return g if jo(g) else None


def alakkal_nyilik(szoveg):
    """Igaz, ha a szakasz (a szám-jelei után) nyelvtani alakkal nyílik (a régi `_ALAKTANI_KEZDET` próba)."""
    return bool(_ALAKTANI_KEZDET.match(re.sub(r'^\s*(?:\d+\.\s*)+', '', szoveg).strip(' —–-')))


# --- a bekezdés: keret és szegmentált sorok -----------------------------------------------------------------------
class Bekezdes:
    """A régi generátor egy bekezdése: keret-szövegek (str: a régi Markdown-keret belső alakja) és `Jelolt` sorok
    sorrendben. A minták a teljes szövegen futnak; a változás csak `Jelolt` idézet-darabot érhet."""

    def __init__(self, darabok):
        self.darabok = list(darabok)
        self.kesz = False

    def _t(self, d):
        if isinstance(d, Jelolt):
            return d.szoveg()
        if isinstance(d, Keret):
            return d.kesz if self.kesz else d.regi
        return d

    def szoveg(self):
        return ''.join(self._t(d) for d in self.darabok)

    def jeloltek(self):
        return [d for d in self.darabok if isinstance(d, Jelolt)]

    def _hol(self, poz, vege=False):
        """(a darab indexe, helyi pozíció). Határon a `Jelolt` darab az elsőbb (a keret nem változhat); `vege`:
        a tartomány vége (a határon az előző darabhoz tartozik)."""
        kezd = 0
        jelolt_hatar = None
        for i, d in enumerate(self.darabok):
            hossz = len(self._t(d))
            if kezd < poz < kezd + hossz:
                return i, poz - kezd
            if poz == kezd or poz == kezd + hossz:
                if isinstance(d, Jelolt):
                    if vege and poz == kezd + hossz:
                        return i, poz - kezd
                    if not vege and poz == kezd:
                        return i, 0
                    if jelolt_hatar is None:
                        jelolt_hatar = (i, poz - kezd)
            kezd += hossz
        if jelolt_hatar is not None:
            return jelolt_hatar
        raise JeloltHiba('a pozíció (%d) a keretbe esik' % poz)

    def _jelolt(self, kezd, veg):
        i, k = self._hol(kezd, vege=False)
        j, v = self._hol(veg, vege=True) if veg > kezd else (i, k)
        if i != j or not isinstance(self.darabok[i], Jelolt):
            raise JeloltHiba('a módosítás keretbe vagy sorhatáron át nyúlna: %r'
                             % self.szoveg()[max(0, kezd - 20):veg + 20])
        return self.darabok[i], k, v

    def beszur(self, poz, jeloles):
        d, k, _v = self._jelolt(poz, poz)
        d.beszur(k, jeloles)

    def javit(self, kezd, veg, uj):
        d, k, v = self._jelolt(kezd, veg)
        d.javit(k, v, uj)

    def cserel_jelolesre(self, kezd, veg, jeloles):
        d, k, v = self._jelolt(kezd, veg)
        d.cserel_jelolesre(k, v, jeloles)

    def burkol(self, kezd, veg, nyito, zaro):
        d, k, v = self._jelolt(kezd, veg)
        d.burkol(k, v, nyito, zaro)

    def torol_lrm_is(self, kezd, veg):
        d, k, v = self._jelolt(kezd, veg)
        d.torol_lrm_is(k, v)

    def futamonkent(self, f):
        """Forrásjavítás idézet-futamonként (a futam a jelölések közti idézet); a keret nem változhat."""
        for d in self.darabok:
            if isinstance(d, Jelolt):
                d.futamonkent(f)
            elif f(self._t(d)) != self._t(d):
                raise JeloltHiba('a forrásjavítás a keretet változtatná: %r' % self._t(d)[:60])

    def sub(self, rx, uj, vedett=None, soronkent=False):
        """A minta találatai (a `vedett` minta által védett részeken és — `soronkent` — sorhatáron át nem) az idézetben
        cserélődnek; a csere szövege a találatból (`m.expand`). Jobbról balra, egy menetben (mint a `re.sub`)."""
        szoveg = self.szoveg()
        reszek = _vedetlen_reszek(szoveg, vedett, soronkent)
        talalatok = []
        for kezd, veg in reszek:
            for m in rx.finditer(szoveg[kezd:veg]):
                talalatok.append((kezd + m.start(), kezd + m.end(), m.expand(uj) if isinstance(uj, str) else uj(m)))
        for kezd, veg, csere in sorted(talalatok, reverse=True):
            if szoveg[kezd:veg] != csere:
                self.javit(kezd, veg, csere)


def _vedetlen_reszek(szoveg, vedett, soronkent):
    hatarok = []
    poz = 0
    if vedett is not None:
        for m in vedett.finditer(szoveg):
            hatarok.append((poz, m.start()))
            poz = m.end()
    hatarok.append((poz, len(szoveg)))
    if not soronkent:
        return hatarok
    ki = []
    for kezd, veg in hatarok:
        s = kezd
        for i in range(kezd, veg):
            if szoveg[i] == '\n':
                ki.append((s, i))
                s = i + 1
        ki.append((s, veg))
    return ki


# --- a jelölések belső (mintaillesztési) alakja: a régi lap jelölésével egyenértékű -----------------------------------
def mark_nyit(vers):
    return Jeloles(JelFajta.MARK_NYIT, vers, '<mark title="%s">' % vers.kod)


MARK_ZAR = Jeloles(JelFajta.MARK_ZAR, None, '</mark>')
ABBR_ZAR = Jeloles(JelFajta.ABBR_ZAR, None, '</abbr>')
LRM = Jeloles(JelFajta.LRM, None, bdb_rovidites.LRM)
NINCS_KAROLI_BELSO = ' *(a Károliban nincs ilyen vers: a szótár hivatkozása)*'
KAROLI_BELSO = ' (héber számozás: %s)'


def csonk(alak):
    return Jeloles(JelFajta.CSONK, alak == CSONK_TAPADT, alak)


def kiejtes_jel(kiejtes):
    return Jeloles(JelFajta.KIEJTES, kiejtes, ' (%s)' % kiejtes.ertek)


# --- a lánc lépései ---------------------------------------------------------------------------------------------
def kiemel(jelolt, celok, extra, igehely):
    """A célversek (`[(vers, azonosító)]`) előfordulásait kiemeli; a versenként k-adik előfordulás a k-adik azonosítóé;
    az `extra` versek (a motívum minden verse) minden előfordulása is kiemelt. A jelölés a mark-pár, a vers a cím
    adata (`igehely(vers)`). Visszaad: (kiemelt azonosítók, meg nem talált azonosítók)."""
    szoveg = jelolt.szoveg()
    poz = {}
    for kezd, veg, konyv, fej, v in hivatkozasok(szoveg):
        if konyv:
            poz.setdefault('%s %s:%s' % (konyv, fej, v), []).append((kezd, veg))
    csoport = {}
    for vers, azon in celok:
        csoport.setdefault(vers, []).append(azon)
    talalt, hianyzik, jelolok = [], [], {}
    for vers, azonok in csoport.items():
        helyek = poz.get(vers, [])
        for i, azon in enumerate(azonok):
            if i < len(helyek):
                jelolok.setdefault(helyek[i], vers)
                talalt.append(azon)
            else:
                hianyzik.append(azon)
    for vers in extra or ():
        for hely in poz.get(vers, []):
            jelolok.setdefault(hely, vers)
    for (kezd, veg), vers in sorted(jelolok.items(), reverse=True):
        jelolt.burkol(kezd, veg, mark_nyit(igehely(vers)), MARK_ZAR)
    return talalt, hianyzik


def forrasjavitas(bek, strong, javitasok):
    """A forrás javításai (B17): a torz átírás, a Biblia által igazolt héber betűsorrend, a rafe-maqqéf és a betűjavítás.
    A magyar szövegben a javított átírás magyar alakja áll."""
    atiras, sorrend, betu = javitasok

    def f(t):
        t = bdb_rovidites.atiras_javit(t, strong, javitasok=atiras, magyar=True)
        t = bdb_rovidites.maqqef_javit(bdb_rovidites._sorrend_csere(t, strong, javitasok=sorrend))
        return bdb_rovidites.betu_javit(t, strong, javitasok=betu)
    bek.futamonkent(f)


_IZOLAL_RE = re.compile(r'(?<=[%s%s׳״])(?=(?:[\s,;:()\[\].*_=–—-]|<[^>]*>)*\d)'
                        % (bdb_rovidites.HEB_BETU, bdb_rovidites.HEB_JEL))


def izolal(bek):
    """Irányjel a héber futam után, ha utána (semleges jelek és jelölések után) szám áll."""
    for m in reversed(list(_IZOLAL_RE.finditer(bek.szoveg()))):
        bek.beszur(m.start(), LRM)


def rovidites(bek, cimszo_szoveg, kezdo):
    """Az egybetűs rövidítések („׳י” a forrás alakja, „י׳” a javított) a feloldással; a betű és a geres sorrendje a
    javított alak (forrásjavítás, DT-F131z)."""
    for m in reversed(list(bdb_rovidites._EGYUTT_RE.finditer(bek.szoveg()))):
        betu = m.group(1) or m.group(2)
        b = bdb_rovidites.alapbetu(betu)
        if b == 'י':
            fajta = FeloldasFajta.JAHVE_CIMSZO if kezdo == 'י' and cimszo_szoveg else FeloldasFajta.JAHVE
        elif b and b == kezdo and cimszo_szoveg:
            fajta = FeloldasFajta.CIMSZO
        else:
            fajta = FeloldasFajta.ALTALANOS
        belso = '<abbr title="%s">' % bdb_rovidites.feloldas(betu, cimszo_szoveg, kezdo)
        bek.javit(m.start(), m.end(), betu + '׳')
        bek.burkol(m.start(), m.start() + len(betu) + 1, Jeloles(JelFajta.ABBR_NYIT, Feloldas(fajta), belso), ABBR_ZAR)


def karoli_szamozas(bek, terkep, karoli, b, strong):
    """A hivatkozások Károli-számozással, az eredeti (héber) szám jelölésével; a Károliban nem létező versre mutató
    hivatkozás mellé a hiány jele. `terkep`: {(könyv, fejezet, vers) az MT szerint: (fejezet, vers) a Károliban};
    `karoli`: (versek, könyvek)."""
    versek, konyvek = karoli
    if not terkep and not versek:
        return
    muveletek = []
    for m, konyv, fej, vers in szotari_hivatkozasok(bek.szoveg()):
        cel = (terkep or {}).get((konyv, fej, vers))
        if not cel:
            if versek and konyv in konyvek and '%s %s:%s' % (konyv, fej, vers) not in versek:
                muveletek.append((m.end(), m.end(), None, None))
            continue
        eredeti = '%s:%s' % (fej, vers)
        if m.group('k'):
            uj = '%s %s:%s' % (konyv, cel[0], cel[1])
        elif m.group('c2') or cel[0] != fej:
            uj = '%s:%s' % cel
        else:
            uj = cel[1]
        muveletek.append((m.start(), m.end(), uj, eredeti))
    for kezd, veg, uj, eredeti in sorted(muveletek, key=lambda x: x[0], reverse=True):
        if uj is None:
            bek.beszur(kezd, Jeloles(JelFajta.NINCS_KAROLI, None, NINCS_KAROLI_BELSO))
        else:
            adat = (b.forrasszoveg('B19', 'karoli_alak', uj, strong), b.forrasszoveg('B18', 'szoveg_hu', eredeti, strong))
            bek.cserel_jelolesre(kezd, veg, Jeloles(JelFajta.KAROLI, adat, uj + KAROLI_BELSO % eredeti))


_BDB_AZON_RX = re.compile(r'(?<![\w.])BDB(\d+)\b(?:\s+szócikk)?')


def azonosito_kapu(bek):
    """A régi lap a szövegben álló BDB-azonosítót („BDB9520”) olvasható alakra írta; az idézetben ilyen nem állhat."""
    if any(_BDB_AZON_RX.search(j.idezet_szoveg()) for j in bek.jeloltek()):
        raise JeloltHiba('a szótári szövegben BDB-azonosító áll; az olvasható alak sablonmondatot kér')


# --- a kész lap lépései (a régi lánc 06., 07. és 12. lépése) ---------------------------------------------------------
_OLV_VEDETT = re.compile(r'<!--.*?-->|\]\([^)]*\)|<[^>]+>|\[\^[^\]]+\]')
_BACKTICK_RX = re.compile('`')      # a régi olvasói átírás a kódjelet törölte (a BDB-szöveg „Hiph`il” alakja)
_TAKARITAS = (
    (re.compile(r'\(\s*[;,·]?\s*\)'), ''),
    (re.compile(r'\(\s*[;,·]\s*'), '('),
    (re.compile(r'\s*[;,·]\s*\)'), ')'),
    (re.compile(r'(?:\s·){2,}\s'), ' · '),
    (re.compile(r';\s*;'), ';'),
    (re.compile(r',\s*,'), ','),
    (re.compile(r'(?<=\S)[ \t]{2,}'), ' '),
    (re.compile(r'(?<=\S)\s+([,.;:)])'), r'\1'),
)


def takaritas(bek):
    """A régi olvasói átírás írásjel-takarítása (üres zárójel, kettőzött elválasztó, szóköz az írásjel előtt), soronként,
    a jelölésen kívül: a forrás digitalizálásának nyoma, forrásjavításként."""
    bek.sub(_BACKTICK_RX, '', vedett=_OLV_VEDETT, soronkent=True)
    for _ in range(3):
        for rx, uj in _TAKARITAS:
            bek.sub(rx, uj, vedett=_OLV_VEDETT, soronkent=True)


FEJ_KERET = '**A szócikk feje (nyelvi háttér).** '
_FEJ_NYERS_RX = re.compile(r'(\*\*A szócikk feje \(nyelvi háttér\)\.\*\* )[HG]\d{1,4}[a-z]?\. [^֐-׿יִ-ﭏ\[\n]*?'
                           r'(?=(?:[IV]+\. )?\[?[֐-׿יִ-ﭏ])')
_SZAMLALO_RX = re.compile(r'(?:(?<=[֐-׿יִ-ﭏ\]‎])‎?|(?<=Qal)|(?<=[`\']al)|(?<=[`\']el)|(?<=[`\']il)|'
                          r'(?<=Hiphil)|(?<=Hophal)|(?<=Niphal))_\d+(?=[\s,;.)\]])')


def belso_jelek_torlese(bek):
    """A BDB-fej nyers előtagja („H7451. ra ' ”) és a címszó belső számlálója („רַע‎_226”) nélkül (a régi
    `kesz_lap_utana`): a digitalizálás nyoma, forrásjavításként. A számláló előtti irányjel is törlődik."""
    szoveg = bek.szoveg()
    for m in reversed(list(_FEJ_NYERS_RX.finditer(szoveg))):
        bek.javit(m.end(1), m.end(), '')
    for m in reversed(list(_SZAMLALO_RX.finditer(bek.szoveg()))):
        bek.torol_lrm_is(m.start(), m.end())


_OU_VEDETT = re.compile(r'<!--.*?-->|<sup class="strong"[^>]*>[^<]*</sup>|<[^>]+>|`[^`]*`|\]\([^)]*\)|https?://\S+|'
                        r'(?:\\?\|\s*)?scope=.*?ts=[\dT:Z.-]+')
_BDB_CSERE = (
    (re.compile('ֿ'), ''),
    (re.compile(r'(?<=[^\s,]),,'), ','),
    (re.compile(r' ?(?<!\[)\^ ?'), ' '),
)


def digitalizalas_jelei(bek):
    """A BDB-átalakítás maradék jelei (a régi `bdb_sor`): a rafe, a dupla vessző, a felső index jele."""
    for rx, uj in _BDB_CSERE:
        bek.sub(rx, uj, vedett=_OU_VEDETT, soronkent=True)


def nfc(s):
    return unicodedata.normalize('NFC', s)


# --- a keret két alakja ------------------------------------------------------------------------------------------
class Keret:
    """A régi bekezdés keret-szövege két alakban: a kártya építésekor (`regi`, a régi Markdown-jelöléssel) és a kész
    lapon (`kesz`, a régi olvasói átírás után). A minták a lánc lépésének megfelelő alakot látják."""
    __slots__ = ('regi', 'kesz')

    def __init__(self, regi, kesz=None):
        self.regi, self.kesz = regi, regi if kesz is None else kesz



# --- a kártya pontjai: melyik vers melyik szótári ponton áll (a régi `gerinc_blokk` első fele) ---------------------
class Pontok:
    """A szó motívumbeli verseinek pontjai a szótárban. A kulcsok szakaszkulcsok ((szócikk, útvonal)); a versek a
    Károli-kulcsok. `gyenge`: {(vers, kulcs): [a bizonytalanság kódjai]}; `celok`: {kulcs: [(a kiemelendő vers alakja,
    sorszám)]}; `fej_celok`: {szócikk: [...]}; `tartomanyban`: [(vers, [Tartomany])]."""

    def __init__(self):
        self.vers_pont, self.gyenge, self.eros = [], {}, set()
        self.celok, self.fej_celok, self.hordozo = {}, {}, set()
        self.nem_idezett, self.tartomanyban, self.pont_nelkul = [], [], []


def bizonytalan_kodok(r):
    """A példahely-sor bizonytalanságának kódjai (a régi `vj_bizonytalan` szabálya); üres: biztos sor."""
    kodok = [o for o in (r.get('okkod') or '').split(',') if o in bdb_vj_szabaly.BIZONYTALAN_OK]
    if r.get('vers_feloldas') in bdb_vj_szabaly.BIZONYTALAN_VERS:
        kodok.append(r['vers_feloldas'])
    if (r.get('bizonyossag') or '').startswith('ketes'):
        kodok.append(BIZONYTALAN_PONT)
    return kodok


BIZONYTALAN_PONT = 'ketes_pont'


def bdb_pontok(g, strong_kod, versek, kut_kulcsok, fa):
    """A BDB-kártya pontjai a versekre (a motívum versei a szó soraiból, a sorok rendjében) és a szerkesztői
    jelentésszámokra (`kut_kulcsok`). `fa`: a `kartya_fa` eredménye."""
    szocikkek, elnyelt = fa
    teljes_ut = {(k[0], utvonal_vag(k[1])): k for sz in szocikkek for k, _j, _h, _a, _f in sz['szakaszok']}
    p = Pontok()

    def pont(vers, k, r):
        p.vers_pont.append((vers, k))
        okok = bizonytalan_kodok(r)
        if okok:
            p.gyenge.setdefault((vers, k), set()).update(okok)
        else:
            p.eros.add((vers, k))

    def cel(hova, keres, azon, kulcs=None):
        if hova[1] == 'fej':
            p.fej_celok.setdefault(hova[0], []).append((keres, azon))
        else:
            p.celok.setdefault(hova, []).append((keres, azon))
            p.hordozo.add(hova)
        if kulcs is not None:
            p.hordozo.add(kulcs)

    for vers in dict.fromkeys(versek):
        sorok = g.vers_sorok(strong_kod, vers)
        if not sorok:
            tart = g.tartomanyban(strong_kod, vers)
            if tart:
                p.tartomanyban.append((vers, tart))
            else:
                p.nem_idezett.append(vers)
        for r in sorok:
            b_id, _ok = g.pelda_szocikk(strong_kod, r)
            if b_id is None:
                p.pont_nelkul.append(vers)
                continue
            if r['utvonal'] == 'fej':
                pont(vers, (b_id, 'fej'), r)
                cel(elnyelt.get((b_id, 'fej'), (b_id, 'fej')), vers, r['sorszam'])
                continue
            k = teljes_ut.get((b_id, utvonal_vag(r['utvonal'])))
            if k is None:
                if r['utvonal'] == 'tagolatlan':
                    pont(vers, (b_id, 'tagolatlan'), r)
                else:
                    p.pont_nelkul.append(vers)
                continue
            pont(vers, k, r)
            keres = vers
            if 'forras_javitas' in (r.get('okkod') or '').split(',') and re.fullmatch(r'\d+:\d+', r['nyers']):
                keres = '%s %s' % (vers.rsplit(' ', 1)[0], r['nyers'])
            cel(elnyelt.get(k, k), keres, r['sorszam'], k)
    for kk in kut_kulcsok:
        k = g.kutatoi_szakasz('BDB', strong_kod, kk)
        if k:
            p.hordozo.add(k)
    return p


def utvonal_vag(utvonal):
    while utvonal.endswith('/-'):
        utvonal = utvonal[:-2]
    return utvonal


def hivatkozas_szam(g, strong_kod, fa):
    """A szakaszok hivatkozásszáma a feloldott példahely-sorokból (a régi `bdb_hivatkozas_szam`): {kulcs: szám}."""
    szocikkek, _elnyelt = fa
    teljes_ut = {(k[0], utvonal_vag(k[1])): k for sz in szocikkek for k, _j, _h, _a, _f in sz['szakaszok']}
    db = {}
    for r in g.feloldott_sorok(strong_kod):
        b_id, _ok = g.pelda_szocikk(strong_kod, r)
        if b_id is None:
            continue
        k = (b_id, 'fej') if r['utvonal'] == 'fej' else teljes_ut.get((b_id, utvonal_vag(r['utvonal'])))
        if k is not None:
            db[k] = db.get(k, 0) + 1
    return db


# --- kiejtés-pótlás a kész lapon (a régi lánc 10. lépése; a minta a kiejtés-szolgáltatásé, GK-13) ---------------
def latott_kulcsok(szoveg, latott):
    """A szöveg héber és görög szavainak kulcsai a látott szavak közé (a nyelvrész már kiírt, nem idézet sorai)."""
    szavak_be.latott_kulcsok(szoveg, latott)


def kiejtes_potlas(bek, kovetkezo, latott, kiejto):
    """Egy kész sor (`Bekezdes`, kész keret): a szakaszban először álló szó után a kiejtés, ha nincs mellette (a régi
    szabály). `kiejto(szó)`: Forrasszoveg vagy None. A beszúrás csak a szegmentált idézetbe kerülhet."""
    bek.kesz = True
    for hol, jav in reversed(szavak_be.potlas_helyek(bek.szoveg(), kovetkezo, latott, kiejto)):
        bek.beszur(hol, kiejtes_jel(jav))


def thayer_pontok(g, strong_kod, versek, kut_kulcsok, fa):
    """A Thayer-kártya pontjai (a régi `gerinc_blokk` Thayer-ága): a Thayer saját példahelyei; bizonytalan sor és
    verstartomány itt nincs, a szócikk egyetlen (azonosítója üres)."""
    szocikkek, _elnyelt = fa
    teljes_ut = {(k[0], utvonal_vag(k[1])): k for sz in szocikkek for k, _j, _h, _a, _f in sz['szakaszok']}
    p = Pontok()
    for vers in dict.fromkeys(versek):
        sorok = g.thayer_vers_sorok(strong_kod, vers)
        if not sorok:
            p.nem_idezett.append(vers)
        for r in sorok:
            if r['utvonal'] == 'fej':
                p.vers_pont.append((vers, ('', 'fej')))
                p.eros.add((vers, ('', 'fej')))
                p.fej_celok.setdefault('', []).append((vers, r['sorszam']))
                continue
            k = teljes_ut.get(('', utvonal_vag(r['utvonal'])))
            if k is None:
                if r['utvonal'] == 'tagolatlan':
                    p.vers_pont.append((vers, ('', 'tagolatlan')))
                    p.eros.add((vers, ('', 'tagolatlan')))
                else:
                    p.pont_nelkul.append(vers)
                continue
            p.vers_pont.append((vers, k))
            p.eros.add((vers, k))
            p.celok.setdefault(k, []).append((vers, r['sorszam']))
            p.hordozo.add(k)
    for kk in kut_kulcsok:
        k = g.kutatoi_szakasz('Thayer', strong_kod, kk)
        if k:
            p.hordozo.add(k)
    return p
