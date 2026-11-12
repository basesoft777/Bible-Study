"""bdb_szokartya.py — a BDB-szókártya megjelenítési szabályai (F213, FELADATOK #213): egy szabály, egy hely.

A szókártya a szó-lap BDB-blokkja (`blokkok._r_bdb_apparatus`); a szónézet és a későbbi motívumlap-nézet ugyanezt a komponenst
mutatja, csak az alapállapot más (a jóváhagyott mockup: a design-vászon „Szótári nézet” oldala, 2026-11-12). A tagolás a
szakasztáblából jön (`eszkozok/bdb_tagolas.py`, F182, F33): itt a tagolás nem változik, csak egy jelentés saját szövegének
olvasói bontása:

- `egysegek`: a jelentés magyar szövege használati sorokra (a felső szintű pontosvessző szerint); soronként szerkezet (a héber
  kifejezés), magyar magyarázat és a helyek szövegrésze. A szöveg nem változik: a sorok szövegrészei sorrendben a teljes
  szöveget adják, kivéve az apparátusba vitt zárójeleket (forrásjel, kérdőjeles vagy szerzői megjegyzés, hivatkozás nélkül);
  ha a bontás nem biztos, a sor a teljes szövegrész (`egesz`);
- a glossza a lexikonlap 4.2-es kártyájával közös szabályból jön (`eszkozok/szotari_glossza.olvasoi_glossza`), nem innen;
- `alap_nemi_tanu` és `csak_szofaj`: a fejléc alapjelentésének javítása (a „főnév hímnemű^2Móz 10:13 reggel” típus);
- `vers_kulcsok`: a motívum-előfordulás igehelye (tartomány is) Károli-versekre bontva.

Csak standard könyvtár; SQL és HTML nincs benne (a lekérdezés a `lekerdezesek.py`-ban, a HTML a `blokkok.py`-ban).
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HEB = r'֐-׿יִ-ﭏ'
HEB_FUTAM = re.compile(r"[׳״']?[%s][%s׳״'־\-]*(?:[\s,|‖=]+[׳״']?[%s][%s׳״'־\-]*)*" % (HEB, HEB, HEB, HEB))
BETU = re.compile(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2}')
# a helyek folytatása (új használati sor nélkül): ha a pontosvessző utáni rész előtagja csak ezek egyike
OSSZEFUZO = re.compile(r'^(?:vö\.(?:\s+még)?|l\.|továbbá|és|\+)?$')
LATHATO_HELY = 10     # ennyi hely látszik egy használati sorban; a többi a „még N hely” mögött (a vers és a motívum helye mindig)


def _parok(s):
    """A zárójelpárok ({nyitó: záró}); a pár nélküli zárójel nem számít (a forrásban gyakori, pl. H0127 3. „(vö. …,;”)."""
    verem, par = [], {}
    for i, c in enumerate(s):
        if c in '([':
            verem.append(i)
        elif c in ')]' and verem:
            par[verem.pop()] = i
    return par


def _felso_szint(s, jel):
    """A `jel` felső szintű (zárójelen kívüli) előfordulásainak helye."""
    par, ki, i = _parok(s), [], 0
    while i < len(s):
        if i in par:
            i = par[i] + 1
            continue
        if s[i] == jel:
            ki.append(i)
        i += 1
    return ki


def _darabol(s):
    h = _felso_szint(s, ';')
    ki, p = [], 0
    for i in h:
        ki.append(s[p:i])
        p = i + 1
    ki.append(s[p:])
    return ki


def apparatusba(s, ref_tokenek, apparatus_e, forrasjel_re):
    """(a szöveg az apparátusba vitt zárójelek nélkül, [forrásjel-csoport], [apparátus-zárójel]). Csak a felső szintű, hivatkozás
    nélküli zárójel megy át: a forrásjel-csoport („(mind J)”) és az, amelyre `apparatus_e` igaz (kérdőjel, szerzői jel)."""
    par = _parok(s)
    forras, app, ki, i = [], [], [], 0
    while i < len(s):
        if i in par and s[i] == '(':
            j = par[i]
            belso = s[i:j + 1]
            if not ref_tokenek(belso):
                if forrasjel_re.fullmatch(belso):
                    forras.append(belso)
                    i = j + 1
                    continue
                if apparatus_e(belso[1:-1]):
                    app.append(belso)
                    i = j + 1
                    continue
            ki.append(belso)
            i = j + 1
            continue
        ki.append(s[i])
        i += 1
    return re.sub(r'\s{2,}', ' ', ''.join(ki)), forras, app


def _szerkezet_e(s, f):
    """A héber futam önálló szerkezet-e: zárójelen kívül áll, és nem tapad hozzá magyar rag vagy szó (kötőjellel vagy közvetlenül)."""
    elotte = s[:f.start()]
    if elotte.count('(') + elotte.count('[') > elotte.count(')') + elotte.count(']'):
        return False
    if re.match(r'-?[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]', s[f.end():]) or f.group(0).endswith('-'):
        return False
    return not re.search(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]$', elotte)


def egysegek(s, ref_tokenek):
    """A jelentés saját szövegének használati sorai: [{'szerk', 'magy', 'hely', 'egesz'}]. `ref_tokenek(szöveg)` →
    [(kezdet, vég, kulcs)] (a `blokkok._ref_tokenek`). `hely`: a szövegrész az első hivatkozástól (a hivatkozások és a köztük álló
    szavak); `egesz`: a bontás nem biztos, a sor a teljes szövegrész (`magy`-ban)."""
    sorok = []
    for d in _darabol(s or ''):
        if not d.strip():
            continue
        refs = ref_tokenek(d)
        p = refs[0][0] if refs else len(d)
        elo, hely = d[:p], d[p:]
        csupasz = HEB_FUTAM.sub('', elo).strip(' ,.:;—-')
        if sorok and refs and not HEB_FUTAM.search(elo) and OSSZEFUZO.match(csupasz) and not sorok[-1]['egesz']:
            sorok[-1]['hely'] = (sorok[-1]['hely'].rstrip() + '; ' + d.strip()).strip()
            continue
        sor = {'szerk': '', 'magy': '', 'hely': hely.strip(), 'egesz': False}
        nyit, zar = d.count('(') + d.count('['), d.count(')') + d.count(']')
        if nyit != zar:
            sor.update(magy=d.strip(), hely='', egesz=True)
            sorok.append(sor)
            continue
        # a szerkezet csak a zárójelen kívüli, ragtalan héber kifejezés: a magyar mondatba ágyazott, ragos alak („szemben
        # לַיְלָה-val”) a magyarázat része marad, különben a rag leválik és a sor összekeveredik
        futamok = [f for f in HEB_FUTAM.finditer(elo) if _szerkezet_e(elo, f)]
        if futamok:
            f = futamok[0]
            sor['szerk'] = f.group(0).strip(' ,')
            sor['magy'] = (elo[:f.start()] + ' ' + elo[f.end():]).strip(' ,;:')
        else:
            sor['magy'] = elo.strip(' ,;:')
        sor['magy'] = re.sub(r'\s{2,}', ' ', sor['magy'])
        sorok.append(sor)
    return sorok


# „főnév hímnemű^2Móz 10:13 reggel”, „hímnemű főnév^1Móz 1:3 (nőnemű^Jób 36:32; Jer 13:16) fény”: a nem tanúja (^ + igehely, és a
# más nem zárójeles tanúi) nem a jelentés része
NEMI_TANU = re.compile(r'\^\s*\??\s*(?:\d?\s?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{0,6}\.?\s+)?\d+:\d+(?:\s*\((?:[^()]*\^[^()]*)\))?\s*')
SZOFAJ_SZAVAK = re.compile(r'hímnemű|nőnemű|közös|többes|egyes|számú|szám|főnév|ige|melléknév|tulajdonnév|határozószó|'
                           r'elöljárószó|kötőszó|névmás|[\[\]:,.\s?]')


def alap_nemi_tanu(alap):
    """A fej-szöveg a nem tanújának igehelye nélkül (a jelentés így nem esik a levágásba)."""
    return NEMI_TANU.sub(' ', alap or '').strip() if alap else alap


def csak_szofaj(t):
    """Igaz, ha a szöveg csak szófaji szavakból áll (pl. „hímnemű”): ilyen alapjelentés nem fogadható el. A rövid szó („kő”) jelentés."""
    return not BETU.search(SZOFAJ_SZAVAK.sub(' ', t or ''))


_IG = re.compile(r'^(.+?) (\d+):(\d+)(?:\s*[-–]\s*(\d+))?$')


def vers_kulcsok(igehely):
    """{Károli-vers}: „Sof 1:2-3” → {„Sof 1:2”, „Sof 1:3”}; egy vers változatlan; ismeretlen alakra üres."""
    m = _IG.match((igehely or '').strip())
    if not m:
        return set()
    k, f, v1 = m.group(1), int(m.group(2)), int(m.group(3))
    v2 = int(m.group(4)) if m.group(4) else v1
    return {'%s %d:%d' % (k, f, v) for v in range(v1, max(v1, v2) + 1)}
