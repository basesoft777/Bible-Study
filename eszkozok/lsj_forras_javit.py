"""F0.43: az LSJ forrás-javítása — `adat/lsj_forras_javitas.tsv` (SEMA 2.75).

A `konkordancia/LSJ_teljes.tsv` az Eliran Wong-modulból származik (`naplok/LSJ_PERSEUS_OSSZEVETES_2026-11-24.md`); sorai közül
942 nem LSJ-szöveg, hanem a modul készítőjének pótszövege (név-helyőrző, Strong-mondat; `naplok/LSJ_HIBAOSZTALYOK_2026-11-24.md`).
A nyers tábla érintetlen marad; a javítás sora a Strong-számhoz rendel egy döntést:

  `perseus_csere` — a Strong lemmájával azonos kulcsú Perseus-LSJ-szócikk szövege kerül a szócikk helyére;
  `nincs_szocikk` — a Perseus-LSJ-ben nincs önálló szócikk erre a lemmára: az `lsj` tábla sora üres szöveggel marad, az olvasó
                    ezt mondja ki, szöveget nem ad.

A `sqlite_epit.py` az `lsj` tábla építésekor alkalmazza (`alkalmaz`: a csere szövege a helyére kerül, a `nincs_szocikk` sor szövege üres); a sor `modul_hash` mezője az eredeti modul-szöveg
lenyomata: ha a nyers sor megváltozik, az építés megáll (a döntést újra kell vizsgálni).

Használat:
  python eszkozok/lsj_forras_javit.py --keszit <perseus_xml_mappa> [--ts 2026-11-24]   # a tábla (újra)írása
  python eszkozok/lsj_forras_javit.py --ellenoriz                                         # a tábla ellenőrzése a nyers táblával
"""
import argparse
import glob
import hashlib
import html
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join('adat', 'lsj_forras_javitas.tsv')
NYERS = os.path.join('konkordancia', 'LSJ_teljes.tsv')
TBESG = os.path.join('konkordancia', 'TBESG.txt')
OSZTALYOK = os.path.join('naplok', 'LSJ_HIBAOSZTALYOK_2026-11-24_strongok.tsv')
B_DONTESEK = os.path.join('naplok', 'LSJ_B_DONTESEK_2026-11-24.tsv')

PERSEUS_COMMIT = '1c34cdf756c63cf37db61bd366d733431dbd7aa0'
FEJLEC = ('strong', 'tipus', 'osztaly', 'modul_hash', 'perseus_kulcs', 'perseus_azonosito', 'modszer', 'szoveg', 'jelzes',
          'indoklas', 'proveniencia')
TIPUSOK = ('perseus_csere', 'perseus_szulo', 'nincs_szocikk')
MODSZEREK = ('gepi_lemma_egyezes', 'kezi_lemma_valtozat', 'gepi_nincs_lemma_egyezes', 'gepi_csonka_szocikk', 'kezi_kizaras',
             'dontes_pontos', 'dontes_szulo', 'dontes_nincs')

# A szülőszócikk olvasói jelzése (a szerkesztői döntés szövege, 2026-11-24): a kártya kimondja, hogy a szónak nincs önálló LSJ-szócikke.
JELZES = 'Az LSJ-ben önálló szócikke nincs; a(z) %s szócikke, amely ezt az alakot tárgyalja.'

# A pontos (ékezettel egyező) kulcs mellett a kézi átnézéssel elfogadott írásmód-változatok: a Strong lemmája és a Perseus-
# szócikk ugyanaz a szó (γινώσκω ~ γιγνώσκω, az attikai -ττ-/-σσ- stb.); az ékezet-érzéketlen egyezésű többi sort (név és
# főnév/melléknév-hasonmás: Τύρος / τυρός, ποτέ / πότε) a tábla nem cseréli: `nincs_szocikk`.
KEZI_ELFOGADOTT = {'G0314', 'G0581', 'G1097', 'G1230', 'G1231', 'G1920', 'G1921', 'G2607', 'G3854', 'G4266', 'G4267',
                   'G4836', 'G2909', 'G5101'}


# Kézzel kizárt egyezések: a Perseus-szócikk lemmája ugyanaz, de más szó vagy más személy szócikke (a lemma-egyezés nem elég).
# G1488 εἶ (az εἰμί 2. személye) ~ az ε betű neve; G3385 μήτι (kérdő-szócska) ~ a μῆτις (ész) alakja; G5600 ὦ (az εἰμί
# kötőmódja) ~ a ὦ indulatszó; Δημήτριος, Διονύσιος, Διοτρεφής, Σίμων: az LSJ klasszikus melléknév vagy más személy.
# Kézzel kijelölt Perseus-szócikk: ugyanaz a szó más írásmóddal, más lemma-alakkal vagy elírt kulccsal áll a Perseus-forrásban
# (a független ellenőrzés, 2026-11-24): a Strong → a Perseus-kulcs (a homográfoknál a helyes számozott kulcs).
KEZI_KULCS = {'G0455': 'a)noi/gnumi', 'G1766': 'e)/natos', 'G4808': 'suke/a', 'G0573': 'a(plo/os', 'G1362': 'diplo/os',
              'G5493': 'xeima/rroos', 'G4483': 'e)rw=', 'G4326': 'prosde/w2', 'G1805': 'e)cagora/cw', 'G1842': 'e)coleqreu/w',
              'G2292': 'qarse/w', 'G4132': 'plh/mura', 'G4874': 'sunanamei/gnumi', 'G5379': 'filoniki/a',
              'G1495': 'ei)dwlolatri/a', 'G1744': 'e)ndu/w', 'G3338': 'metame/lomai', 'G3587': 'cure/w', 'G3830': 'pandokeu/s',
              'G4800': 'suzw='}

KEZI_KIZART = {'G1488': 'az εἶ (az εἰμί alakja) nem az ε betű neve', 'G3385': 'a μήτι (szócska) nem a μῆτις alakja',
               'G5600': 'a ὦ (az εἰμί alakja) nem a ὦ indulatszó',
               'G2748': 'helynév (Kidron): az LSJ-szócikk a κέδρος köznévről szól',
               'G1216': 'személynév: az LSJ-szócikk a melléknévről szól', 'G1354': 'személynév: az LSJ-szócikk a melléknévről szól',
               'G1361': 'személynév: az LSJ-szócikk a melléknévről szól', 'G4613': 'személynév: az LSJ-szócikk más Simonról szól'}
_NYELVJARAS = {'ion', 'lon', 'dor', 'att', 'ep', 'etc', 'aeol', 'boeot', 'delph', 'poet', 'lacon', 'cret', 'cypr', 'and', 'later',
               'also', 'late', 'or', 'v'}


def csonka(szoveg):
    """A Perseus-forrás csonka szócikke: a lemma után csak nyelvjárás-jelölés áll („καταπλέω, lon.”)."""
    maradek = re.sub(r'[Ͱ-Ͽἀ-῿̀-ͯ]+', ' ', szoveg)
    szavak = re.findall(r'[A-Za-z]+', maradek)
    return not szavak or all(w.lower() in _NYELVJARAS for w in szavak) and 'v.' not in maradek


def modul_hash(szoveg):
    """A nyers modul-szöveg lenyomata (a javítás-sor érvényességi őre)."""
    return hashlib.sha256(szoveg.strip().encode('utf-8')).hexdigest()[:16]


def strong_padded(s):
    return 'G%04d' % int(s[1:])


# --- a Perseus-oldal (TEI-XML, csak olvasás) ---------------------------------------------------------------------------
_BASE = {'a': 'α', 'b': 'β', 'g': 'γ', 'd': 'δ', 'e': 'ε', 'z': 'ζ', 'h': 'η', 'q': 'θ', 'i': 'ι', 'k': 'κ', 'l': 'λ',
         'm': 'μ', 'n': 'ν', 'c': 'ξ', 'o': 'ο', 'p': 'π', 'r': 'ρ', 's': 'σ', 't': 'τ', 'u': 'υ', 'f': 'φ', 'x': 'χ',
         'y': 'ψ', 'w': 'ω', 'v': 'ϝ'}
_DIA = {')': '̓', '(': '̔', '/': '́', '\\': '̀', '=': '͂', '|': 'ͅ', '+': '̈', '_': '̄', '^': '̆'}
_SORREND = {'+': 0, ')': 1, '(': 1, '/': 2, '\\': 2, '=': 2, '_': 3, '^': 3, '|': 4}


def _dj(dias):
    return ''.join(_DIA[d] for d in sorted(dias, key=lambda x: _SORREND.get(x, 9)))


_SZERK_ZAROJEL = re.compile(r'\(([A-Za-z])\)')


def beta_unicode(s):
    """Beta-kód → Unicode görög (a Perseus-kulcsok és a görög elemek). Az egy betűt záró zárójel (`kt(e)iron`, `ka\\(t) ta\\`) szerkesztői
    kiegészítés, nem lehelet: „(ε)” lesz (a független ellenőrzés, 2026-11-24: ᾤκτ̔ἐιρον helyett ᾤκτ(ε)ιρον)."""
    reszek = _SZERK_ZAROJEL.split(s)
    if len(reszek) > 1:
        return unicodedata.normalize('NFC', ''.join(
            _beta_alap(r) if j % 2 == 0 else '(' + _beta_alap(r) + ')' for j, r in enumerate(reszek)))
    return _beta_alap(s)


def _beta_alap(s):
    ki, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '*':
            i += 1
            dias = []
            while i < n and s[i] in _DIA:
                dias.append(s[i])
                i += 1
            if i < n and s[i].lower() in _BASE:
                betu = s[i].lower()
                i += 1
                while i < n and s[i] in _DIA:
                    dias.append(s[i])
                    i += 1
                ki.append(_BASE[betu].upper() + _dj(dias))
            else:
                ki.append('*' + ''.join(dias))
            continue
        kb = c.lower()
        if kb in _BASE and c.isalpha() and c.isascii():
            i += 1
            dias = []
            while i < n and s[i] in _DIA:
                dias.append(s[i])
                i += 1
            ch = _BASE[kb]
            if kb == 's':
                if i < n and s[i] in '123':
                    ch = {'1': 'σ', '2': 'ς', '3': 'ϲ'}[s[i]]
                    i += 1
                else:
                    kov = s[i] if i < n else ''
                    szoteszt = kov == '-' and i + 1 < n and s[i + 1].isalpha() and s[i + 1].isascii()   # morféma-határ: nem szóvég
                    if not (kov.isalpha() and kov.isascii()) and kov not in _DIA and not szoteszt:
                        ch = 'ς'
            if c.isupper():
                ch = ch.upper()
            ki.append(ch + _dj(dias))
        else:
            ki.append(c)
            i += 1
    return unicodedata.normalize('NFC', ''.join(ki))


_GOROG_EL = re.compile(r'<(\w+)\b[^>]*\blang="greek"[^>]*>(.*?)</\1>', re.S)
_TAG = re.compile(r'<[^>]+>')
_WS = re.compile(r'\s+')
_ENTRY = re.compile(r'<entryFree\b([^>]*)>(.*?)</entryFree>', re.S)
_ATTR = re.compile(r'(\w+)="([^"]*)"')


def szocikk_szoveg(nyers):
    """Egy `entryFree` jelölés nélküli szövege (a görög elemek Beta-kódból Unicode-ra)."""
    def g(m):
        t = html.unescape(_TAG.sub('', m.group(2)))
        t = html.unescape(t) if '&' in t else t          # a forrás kettős kódolású szerkesztői kiegészítése (&amp;lt;e&amp;gt;)
        # a szerkesztői ⟨ ⟩ jelölés nem tag: a beta-átírás és a tag-eltávolítás előtt védeni kell
        return ' ' + beta_unicode(t.replace('<', '⟨').replace('>', '⟩')) + ' '
    t = _TAG.sub(' ', _GOROG_EL.sub(g, nyers))
    t = html.unescape(t).replace('[schwa]', 'ə').replace('^_', '˘¯')      # a forrás hangjelölései: schwa; rövid-hosszú jel
    return _WS.sub(' ', unicodedata.normalize('NFC', t)).strip()


_KOZ_ELOTT = re.compile(r'\s+([,.;:!?)\]])')
_KOZ_UTAN = re.compile(r'([(\[])\s+')


def tisztit(szoveg):
    """A jelölés-eltávolítás szóközei az írásjelek körül (a szöveg többi része változatlan)."""
    return _KOZ_UTAN.sub(r'\1', _KOZ_ELOTT.sub(r'\1', szoveg))


def perseus_beolvas(mappa):
    """A Perseus-LSJ `main` szócikkei: [{'file', 'id', 'key', 'key_uni', 'text'}]."""
    ki = []
    for f in sorted(glob.glob(os.path.join(mappa, 'grc.lsj.perseus-eng*.xml')),
                    key=lambda x: int(re.search(r'eng(\d+)', x).group(1))):
        with open(f, encoding='utf-8') as fh:
            adat = fh.read()
        for m in _ENTRY.finditer(adat):
            at = dict(_ATTR.findall(m.group(1)))
            if at.get('type') != 'main':
                continue
            key = at.get('key', '')
            ki.append({'file': os.path.basename(f), 'id': at.get('id', ''), 'key': key,
                       'key_uni': beta_unicode(re.sub(r'\d+$', '', key)), 'text': tisztit(szocikk_szoveg(m.group(0)))})
    return ki


# --- a lemma-kulcsok ---------------------------------------------------------------------------------------------------
def kulcs_pontos(s):
    """Ékezetre és kis/nagybetűre egyező kulcs (a hosszúság- és rövidségjel, a szóvégi szigma, a homográf-szám nélkül)."""
    d = unicodedata.normalize('NFD', s.replace('ϲ', 'σ'))
    d = ''.join(c for c in d if c not in '̄̆')
    d = unicodedata.normalize('NFC', d)
    if d and d[0].lower() != d[0]:
        pre = 'N'
    else:
        pre = 'k'
    return pre + re.sub(r'[^\w]', '', d.lower().replace('ς', 'σ')).rstrip('0123456789')


def kulcs_laza(s):
    """Ékezet nélküli kulcs, az attikai/ión írásmód-változatokkal (γινώσκω ~ γιγνώσκω)."""
    d = unicodedata.normalize('NFD', s)
    d = ''.join(c for c in d if not unicodedata.combining(c)).lower().replace('ς', 'σ').replace('ϲ', 'σ')
    d = re.sub(r'[^\w]', '', d).rstrip('0123456789')
    return d.replace('ττ', 'σσ').replace('γιγν', 'γιν').replace('γιγ', 'γιν')


def tbesg_lemmak(tbesg_fajl):
    """{'G0002': 'Ἀαρών'}: az első TBESG-sor lemmája Strong-számonként."""
    ki = {}
    with open(tbesg_fajl, encoding='utf-8-sig') as fh:
        for sor in fh.read().split('\n'):
            p = sor.split('\t')
            if len(p) > 6 and re.match(r'^G\d{4}[a-zA-Z]?$', p[0]):
                ki.setdefault('G%04d' % int(p[0][1:5]), p[3].strip())
    return ki


def nyers_tabla(fajl=None):
    """{'G0002': teljes szócikk} a `LSJ_teljes.tsv`-ből."""
    ki = {}
    with open(fajl or os.path.join(ROOT, NYERS), encoding='utf-8') as fh:
        for sor in fh.read().split('\n')[1:]:
            p = sor.split('\t')
            if len(p) >= 3:
                ki[p[0]] = p[2]
    return ki


def osztalyok(fajl=None):
    """{'G0002': 'A1_nev_helyorzo'}: a mért pótszöveg-sorok (A-osztályok) a #864 Strong-szintű listájából."""
    ki = {}
    with open(fajl or os.path.join(ROOT, OSZTALYOK), encoding='utf-8') as fh:
        for sor in fh.read().split('\n'):
            p = sor.split('\t')
            if len(p) >= 2 and re.match(r'^G\d{4}$', p[0]) and p[1].startswith('A'):
                ki[p[0]] = p[1]
    return ki


# --- a tábla elkészítése -----------------------------------------------------------------------------------------------
def keszit(perseus_mappa, ts, gyoker=ROOT):
    """A javítás-sorok az A-osztályú Strong-okra: a TBESG-lemma pontos egyezése a Perseus `main` szócikkeivel."""
    nyers = nyers_tabla(os.path.join(gyoker, NYERS))
    lemma = tbesg_lemmak(os.path.join(gyoker, TBESG))
    osz = osztalyok(os.path.join(gyoker, OSZTALYOK))
    perseus = perseus_beolvas(perseus_mappa)
    pontos, laza = {}, {}
    for e in perseus:
        pontos.setdefault(kulcs_pontos(e['key_uni']), []).append(e)
        laza.setdefault(kulcs_laza(e['key_uni']), []).append(e)
    per_kulcs = {}
    for e in perseus:
        per_kulcs.setdefault(e['key'], []).append(e)
    sorok = []
    for strong in sorted(osz):
        lem = lemma.get(strong, '')
        modszer, talalat = 'gepi_nincs_lemma_egyezes', []
        if strong in KEZI_KIZART:
            modszer = 'kezi_kizaras'
        elif strong in KEZI_KULCS:
            talalat = [x for k in KEZI_KULCS[strong].split(';') for x in per_kulcs.get(k, [])]
            if not talalat:
                raise JavitasHiba('%s: nincs Perseus-szócikk a(z) %s kulccsal' % (strong, KEZI_KULCS[strong]))
            modszer = 'kezi_lemma_valtozat'
        elif lem:
            talalat = pontos.get(kulcs_pontos(lem), [])
            if talalat:
                modszer = 'gepi_lemma_egyezes'
            elif strong in KEZI_ELFOGADOTT:
                talalat = laza.get(kulcs_laza(lem), [])
                modszer = 'kezi_lemma_valtozat' if talalat else 'gepi_nincs_lemma_egyezes'
        h = modul_hash(nyers[strong])
        if talalat and csonka(' '.join(e['text'] for e in talalat)):
            talalat, modszer = [], 'gepi_csonka_szocikk'
        if talalat:
            talalat = sorted(talalat, key=lambda e: (e['file'], e['id']))
            sz = ' '.join(e['text'] for e in talalat)
            sorok.append((strong, 'perseus_csere', osz[strong], h, ';'.join(e['key'] for e in talalat),
                          ';'.join(e['file'].replace('grc.lsj.perseus-', '').replace('.xml', '') + '#' + e['id']
                                   for e in talalat), modszer, sz, '',
                          'a TBESG-lemma (%s) azonos kulcsú Perseus-LSJ-szócikk; a modul-sor nem LSJ-szöveg (%s)'
                          % (lem, osz[strong]),
                          'scope=Strong→TBESG-lemma→Perseus-kulcs | forras=PerseusDL/lexica@%s %s | ts=%s'
                          % (PERSEUS_COMMIT, ' '.join(e['file'] + '#' + e['id'] for e in talalat), ts)))
        else:
            ok = {'kezi_kizaras': 'a Perseus-szócikk nem ennek a szónak a szócikke (%s)' % KEZI_KIZART.get(strong, ''),
                  'gepi_csonka_szocikk': 'a Perseus-forrás szócikke csonka (csak nyelvjárás-jelölés), tartalma nincs',
                  }.get(modszer, 'a TBESG-lemma kulcsával a Perseus-LSJ-ben nincs önálló szócikk')
            sorok.append((strong, 'nincs_szocikk', osz[strong], h, '', '', modszer, '', '',
                          '%s (TBESG-lemma: %s); a modul-sor nem LSJ-szöveg (%s)' % (ok, lem or 'nincs', osz[strong]),
                          'scope=Strong→TBESG-lemma × a Perseus-LSJ `main` szócikkeinek kulcsai | forras=PerseusDL/lexica@%s | ts=%s'
                          % (PERSEUS_COMMIT, ts)))
    sorok += b_sorok(perseus, nyers, lemma, ts, gyoker)
    return sorok


def b_dontesek(fajl=None):
    """{'G0089': {oszlop: érték}} a 2. hibaosztály döntés-tábláiból (`naplok/LSJ_B_DONTESEK_*.tsv`)."""
    ki, fej = {}, None
    with open(fajl or os.path.join(ROOT, B_DONTESEK), encoding='utf-8') as fh:
        for sor in fh.read().split('\n'):
            if not sor or sor.startswith('#'):
                continue
            p = sor.split('\t')
            if fej is None:
                fej = p
                continue
            r = dict(zip(fej, p))
            if r['dontes'] not in ('csere_pontos', 'csere_szulo', 'nincs_szocikk', 'megtartas') or r['strong'] in ki:
                raise JavitasHiba('a döntés-táblában ismeretlen döntés vagy kettős sor: %s' % r['strong'])
            ki[r['strong']] = r
    return ki


def b_sorok(perseus, nyers, lemma, ts, gyoker=ROOT):
    """A 2. hibaosztály (téves Strong → szócikk kötés) sorai a szerkesztői döntés szerint: `csere_pontos` → `perseus_csere`;
    `csere_szulo` → `perseus_szulo` (a kártya kimondja, hogy a szónak nincs önálló szócikke); `nincs_szocikk`; a `megtartas`
    sor nem kerül a táblába (a modul-szöveg a megfelelő szócikk)."""
    per_kulcs = {}
    for e in perseus:
        per_kulcs.setdefault(e['key'], []).append(e)
        per_kulcs.setdefault(e['key'].rstrip('0123456789'), []).append(e)
    sorok = []
    for strong, r in sorted(b_dontesek(os.path.join(gyoker, B_DONTESEK)).items()):
        if r['dontes'] == 'megtartas':
            continue
        h = modul_hash(nyers[strong])
        lem = lemma.get(strong, '')
        if r['dontes'] == 'nincs_szocikk':
            sorok.append((strong, 'nincs_szocikk', r['osztaly'], h, '', '', 'dontes_nincs', '', '',
                          'szerkesztői döntés: %s' % r['bizonyitek'],
                          'scope=Strong→TBESG-lemma × a Perseus-LSJ main szócikkeinek kulcsai | forras=PerseusDL/lexica@%s; %s | ts=%s'
                          % (PERSEUS_COMMIT, r['dontes_ref'], ts)))
            continue
        talalat = []
        for k in r['perseus_kulcs'].split(';'):
            es = [e for e in per_kulcs.get(k, []) if e['key'] == k] or per_kulcs.get(k, [])
            if not es:
                raise JavitasHiba('%s: nincs Perseus-szócikk a(z) %s kulccsal' % (strong, k))
            talalat += es
        talalat = sorted({(e['file'], e['id']): e for e in talalat}.values(), key=lambda e: (e['file'], e['id']))
        sz = ' '.join(e['text'] for e in talalat)
        szulo = r['dontes'] == 'csere_szulo'
        sorok.append((strong, 'perseus_szulo' if szulo else 'perseus_csere', r['osztaly'], h,
                      ';'.join(e['key'] for e in talalat),
                      ';'.join(e['file'].replace('grc.lsj.perseus-', '').replace('.xml', '') + '#' + e['id'] for e in talalat),
                      'dontes_szulo' if szulo else 'dontes_pontos', sz,
                      JELZES % talalat[0]['key_uni'] if szulo else '',
                      'szerkesztői döntés: %s' % r['bizonyitek'],
                      'scope=Strong→Perseus-kulcs (%s) | forras=PerseusDL/lexica@%s %s; %s | ts=%s'
                      % (r['perseus_kulcs'], PERSEUS_COMMIT, ' '.join(e['file'] + '#' + e['id'] for e in talalat), r['dontes_ref'], ts)))
    return sorok


def kiir(sorok, ts, gyoker=ROOT):
    fej = ('# LSJ forrás-javítás (F0.43; séma: adat/SEMA.md 2.75): a `konkordancia/LSJ_teljes.tsv` pótszöveg-soraihoz döntés — '
           '`perseus_csere` (a Perseus-LSJ szócikke), `perseus_szulo` (a szülőszócikk, kimondott jelzéssel) vagy `nincs_szocikk`. Készítette: eszkozok/lsj_forras_javit.py --keszit (ts=%s); '
           'a Perseus-szöveg CC BY-SA 4.0 (Perseus Digital Library), módosítva: a TEI-jelölés eltávolítva, a Beta-kód Unicode-ra átírva, '
           'a szóközök az írásjelek körül rendezve, a szerkesztői ⟨ ⟩ jelölés megtartva; a homográf szócikkek szóközzel összefűzve.\n' % ts)
    with open(os.path.join(gyoker, TABLA), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej + '\t'.join(FEJLEC) + '\n')
        for s in sorok:
            assert not any(('\t' in x or '\n' in x) for x in s), s[0]
            f.write('\t'.join(s) + '\n')


# --- a tábla használata --------------------------------------------------------------------------------------------------
class JavitasHiba(Exception):
    pass


def betolt(fajl=None):
    """{'G0002': {oszlop: érték}} a javítás-táblából; a séma hibája kivétel."""
    fajl = fajl or os.path.join(ROOT, TABLA)
    ki, fej = {}, None
    with open(fajl, encoding='utf-8') as fh:
        for sor in fh.read().split('\n'):
            if not sor or sor.startswith('#'):
                continue
            p = sor.split('\t')
            if fej is None:
                if tuple(p) != FEJLEC:
                    raise JavitasHiba('%s: váratlan fejléc: %s' % (fajl, p))
                fej = p
                continue
            if len(p) != len(FEJLEC):
                raise JavitasHiba('%s: %d oszlop a %d helyett: %s' % (fajl, len(p), len(FEJLEC), p[:1]))
            r = dict(zip(fej, p))
            if r['strong'] in ki:
                raise JavitasHiba('kétszer szerepel: %s' % r['strong'])
            if not re.match(r'^G\d{4}$', r['strong']):
                raise JavitasHiba('a Strong-szám nem G####: %s' % r['strong'])
            if r['tipus'] not in TIPUSOK or r['modszer'] not in MODSZEREK:
                raise JavitasHiba('ismeretlen típus vagy módszer: %s' % r['strong'])
            if (r['tipus'] != 'nincs_szocikk') != bool(r['szoveg']):
                raise JavitasHiba('a szöveg csak a perseus_* sorban áll: %s' % r['strong'])
            if (r['tipus'] == 'perseus_szulo') != bool(r['jelzes']):
                raise JavitasHiba('a jelzés kötelező és csak a perseus_szulo sorban áll: %s' % r['strong'])
            if r['tipus'] != 'nincs_szocikk' and not (r['perseus_kulcs'] and r['perseus_azonosito']):
                raise JavitasHiba('a perseus_* sorban kell a Perseus-kulcs és -azonosító: %s' % r['strong'])
            if not r['indoklas'] or not r['proveniencia'].startswith('scope=') or ' | forras=' not in r['proveniencia']:
                raise JavitasHiba('indoklás vagy proveniencia-sor hiányzik: %s' % r['strong'])
            ki[r['strong']] = r
    return ki


def alkalmaz(sorok, strong_idx, szoveg_idx, javitasok):
    """A nyers `lsj` sorok (lista-listák) javítása: a `perseus_csere` és a `perseus_szulo` (jelzéssel elöl) sor szövege cserélődik, a
    `nincs_szocikk` soré üres lesz (a sor marad).
    A `modul_hash` eltérése (a nyers sor megváltozott) kivétel. Visszaad: (új sorok, {tipus: darab})."""
    ki, db = [], {'perseus_csere': 0, 'perseus_szulo': 0, 'nincs_szocikk': 0}
    latott = set()
    for r in sorok:
        j = javitasok.get(r[strong_idx])
        if j is None:
            ki.append(r)
            continue
        if j['modul_hash'] != modul_hash(r[szoveg_idx]):
            raise JavitasHiba('%s: a nyers LSJ-sor megváltozott a javítás óta (modul_hash); a döntést újra kell vizsgálni'
                              % j['strong'])
        latott.add(r[strong_idx])
        db[j['tipus']] += 1
        r = list(r)
        r[szoveg_idx] = (j['jelzes'] + ' ' if j['jelzes'] else '') + j['szoveg']   # `nincs_szocikk`: üres szöveg, a sor marad
        ki.append(r)
    hiany = sorted(set(javitasok) - latott)
    if hiany:
        raise JavitasHiba('a javítás-tábla Strong-száma nincs a nyers LSJ-táblában: %s' % ', '.join(hiany[:5]))
    return ki, db


def ellenoriz(gyoker=ROOT):
    """A tábla és a nyers tábla összevetése; hibák listája (üres: rendben)."""
    hibak = []
    try:
        j = betolt(os.path.join(gyoker, TABLA))
    except JavitasHiba as e:
        return [str(e)]
    nyers = nyers_tabla(os.path.join(gyoker, NYERS))
    for s, r in j.items():
        if s not in nyers:
            hibak.append('%s: nincs a nyers táblában' % s)
        elif r['modul_hash'] != modul_hash(nyers[s]):
            hibak.append('%s: a modul-hash nem egyezik' % s)
        if r['tipus'] != 'nincs_szocikk' and ('This entry is a name' in r['szoveg'] or 'Defined by LSJ' in r['szoveg']):
            hibak.append('%s: a csere-szöveg pótszöveg' % s)
    return hibak


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--keszit', metavar='PERSEUS_MAPPA')
    ap.add_argument('--ellenoriz', action='store_true')
    ap.add_argument('--ts', default='2026-11-24')
    a = ap.parse_args(argv)
    if a.keszit:
        sorok = keszit(a.keszit, a.ts)
        kiir(sorok, a.ts)
        from collections import Counter
        print(Counter((s[1], s[6]) for s in sorok))
    if a.ellenoriz:
        h = ellenoriz()
        print('\n'.join(h) if h else 'rendben')
        return 1 if h else 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
