"""Az 1/b. blokk („Kizárt és vizsgált helyek”) olvasói formája — általános, motívumfüggetlen (ISTENTISZT-001 arany lap,
2026-10-29).

Bemenet: a motívum elutasított / nyitva maradt `jeloltek.tsv`-sorai és az `adat/elutasitasi_okok.tsv` mintaszótára. Az adat
nem változik, csak a megjelenítés:
- **miért lett jelölt** — a `forras_kereses` mező szerkezetéből gépileg (`jeloles_oka`): TSK-ajánlás (melyik helyről, a
  szavazat vagy a találatszám, ha a mező hordozza), Károli-kereszthivatkozás, gépi keresés (Strong-keresés, szópár-keresés,
  motívumközi mérés), kutatói felvetés (a tematikus tanulmány, a kereszthivatkozás-napló, nevesített tanító, szótári
  felvetés);
- **döntés és indok** — a döntés, az elutasítás oka a mintaszótárból (`elutasitas_oka`), és az `indoklas` szövege
  változatlanul (a `|` utáni proveniencia-farok nélkül);
- „egyéb” kategória nincs (F123.EGYEB, a felhasználó, 2026-11-04: „ne legyen olyan indok, hogy egyéb”, „sehol”): a be nem
  sorolható jelölési forrás vagy elutasítási ok `BeNemSorolhato` kivételt dob, és a generálás megáll; a kapu az
  `ellenoriz.py` 28. szabálya (`hianyok`). A javítás a mintaszótárban (`adat/elutasitasi_okok.tsv`) vagy itt, a
  `jeloles_oka` szabályaiban történik, nem a lapon;
- a forrás nyers szövege és az indoklás proveniencia-farka lábjegyzetbe kerül.

TSV: split('\\t'), a '\\r' levágva; csv modul nélkül.
"""
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OKOK = os.path.join(GYOKER, 'adat', 'elutasitasi_okok.tsv')

CSOPORTOK = ('TSK-ajánlás', 'Károli-kereszthivatkozás', 'Gépi keresés', 'Kutatói felvetés')
# a teljesség-mérés hálói (`forras_kereses`-beli kulcs → olvasói név), a kiírás sorrendjében
TELJESSEG_HALOK = (('szópár-háló', 'szópár-háló'), ('Strong-háló', 'Strong-háló'), ('szótár (', 'szótári háló'),
                   ('Károli-szó', 'Károli-szó háló'), ('LXX-többlet', 'Septuaginta-többlet háló'),
                   ('Septuaginta-híd', 'Septuaginta-híd'))
HELY = re.compile(r'\b[1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,6} \d+:\d+(?:-\d+)?')
STRONG = re.compile(r'\b[HG]\d{4}\b')


class BeNemSorolhato(ValueError):
    """A jelölés forrása vagy az elutasítás oka nem sorolható be: a generálás megáll (F123.EGYEB)."""


def _sorok(ut):
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n')]
    s = [x for x in s if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def okok(motivum_id, ut=None):
    """[(lefordított minta, címke)] a mintaszótárból: a motívum saját sorai és a `*` sorok, `sorrend` szerint."""
    sorok = [r for r in _sorok(ut or OKOK) if r['id'] in ('*', motivum_id)]
    return [(re.compile(r['minta'], re.IGNORECASE), r['cimke']) for r in sorted(sorok, key=lambda r: int(r['sorrend']))]


OSSZESITO_TOLDALEK = re.compile(r'\s*\(összesítő sor\)\s*$')


def olvasoi_ok(cimke):
    """A címke olvasói alakja: a belső „(összesítő sor)” toldalék nélkül (F123.HAMART3, a felhasználó átnézése)."""
    return OSSZESITO_TOLDALEK.sub('', cimke or '')


def ok_megjegyzesek(motivum_id, ut=None):
    """{olvasói címke: megjegyzés} a mintaszótárból (a motívum saját sorai és a `*` sorok, `sorrend` szerint, az első
    nyer): az 1/b. döntési tábla „Mit jelent” oszlopa."""
    ki = {}
    for r in sorted((r for r in _sorok(ut or OKOK) if r['id'] in ('*', motivum_id)), key=lambda r: int(r['sorrend'])):
        ki.setdefault(olvasoi_ok(r['cimke']), (r.get('megjegyzes') or '').strip())
    return ki


def elutasitas_oka(indoklas, minta):
    for m, cimke in minta:
        if m.search(indoklas or ''):
            return cimke
    raise BeNemSorolhato('elutasítási ok: a mintaszótár (adat/elutasitasi_okok.tsv) nem sorolja be: %s'
                         % (indoklas or '—')[:120])


def nevelo(szo):
    """A határozott névelő a kiejtés szerint: „az” magánhangzó és az egy / öt (1, 5) előtt, különben „a”."""
    if not szo:
        return 'a'
    return 'az' if szo[0].lower() in 'aáeéiíoóöőuúüű15' else 'a'


def _ahol(hely, rag):
    return '%s %s %s' % (nevelo(hely), hely, rag)


def _tsk_reszlet(fo):
    p = re.search(r'\(([^)]*)\)', fo)
    if not p:
        return ''
    t = p.group(1).strip()
    v = re.fullmatch(r'Votes=(-?\d+)', t)
    if v:
        return ', %s szavazat' % v.group(1)
    v = re.fullmatch(r'(\d+) találat', t)
    if v:
        return ', a forráshelyen %s TSK-találat' % v.group(1)
    if re.fullmatch(r'[\d\s,\-–]+', t):
        return ', szavazat: %s' % t
    return ''


# F123.TUD1B: az összesítő (csoportos) jelöltsor versszámának egyetlen gépi forrása a `forras_kereses` „blokk-kizárás
# (…): N vers” / „blokk-sor (…): N vers” része; a próza (`indoklas`) szövegéből nem olvassuk ki. Kapu: `ellenoriz.py` 33.
CSOPORT_VERSSZAM = re.compile(r'blokk-(?:kizárás|sor)[^:|]*:\s*(\d+) vers')


def csoport_versszam(forras_kereses):
    """Az összesítő jelöltsor versszáma (int) a `forras_kereses` mezőből; None, ha a sor nem összesítő sor."""
    b = CSOPORT_VERSSZAM.search((forras_kereses or '').split(' | ')[0])
    return int(b.group(1)) if b else None


def osszesito_sor_e(r):
    """A jelöltsor összesítő (több verset fedő) sor-e: a forrás blokk-sort jelez, vagy az indoklás így kezdődik."""
    return ('blokk-' in (r.get('forras_kereses') or '')
            or (r.get('indoklas') or '').startswith('Összesítő sor'))


def versek(igehely):
    """Az igehely versei: a tartomány („Luk 9:55-56”) kibontva, különben maga a hely."""
    m = re.fullmatch(r'(.+ \d+):(\d+)[-–](\d+)', (igehely or '').strip())
    if m and int(m.group(2)) <= int(m.group(3)):
        return ['%s:%d' % (m.group(1), v) for v in range(int(m.group(2)), int(m.group(3)) + 1)]
    return [(igehely or '').strip()]


def versszam_hibak(sorok):
    """[(id, igehely, hiba)]: az összesítő sor, amelynek versszáma nem olvasható géppel, vagy eltér az indoklásban
    kimondott számtól (a próza itt csak az egyezés ellenőrzése, nem forrás)."""
    ki = []
    for r in sorok:
        if not osszesito_sor_e(r):
            continue
        n = csoport_versszam(r.get('forras_kereses'))
        if n is None:
            ki.append((r.get('id', ''), r.get('igehely', ''),
                       'a `forras_kereses` nem hordoz versszámot („blokk-kizárás (…): N vers”)'))
            continue
        p = re.match(r'Összesítő sor (\d+) versre', r.get('indoklas') or '')
        if p and int(p.group(1)) != n:
            ki.append((r.get('id', ''), r.get('igehely', ''),
                       'a versszám a forrásban %d, az indoklásban %s' % (n, p.group(1))))
    return ki


def vizsgalt_versek(sorok):
    """A vizsgált versek száma az 1/b. összesítőhöz: {'egyenkent', 'csoport_vers', 'csoport_sor', 'osszes',
    'elutasitva', 'nyitva'}. Az egyenként vizsgált versek különbözők (a tartomány kibontva, az ismétlődő vers egyszer;
    ha bármely sora nyitva, a vers nyitott); az összesítő sor a `csoport_versszam` szerinti verset fedi (a blokk versei
    a mérés szerint a jelöltsorok közt nem állnak)."""
    egyen = collections.OrderedDict()
    cs_vers = cs_sor = 0
    dontes_vers = collections.Counter()
    for r in sorok:
        n = csoport_versszam(r.get('forras_kereses'))
        if n is not None:
            cs_vers += n
            cs_sor += 1
            dontes_vers['nyitva' if r.get('dontes') == 'nyitva' else 'elutasítva'] += n
            continue
        for v in versek(r.get('igehely')):
            egyen.setdefault(v, set()).add(r.get('dontes'))
    for d in egyen.values():
        dontes_vers['nyitva' if 'nyitva' in d else 'elutasítva'] += 1
    return {'egyenkent': len(egyen), 'csoport_vers': cs_vers, 'csoport_sor': cs_sor, 'osszes': len(egyen) + cs_vers,
            'elutasitva': dontes_vers['elutasítva'], 'nyitva': dontes_vers['nyitva']}


def _teljesseg(fo):
    """A teljesség-mérés olvasói leírása: a háló(k) és a csoportos kizárás versszáma."""
    halo = [nev for kulcs, nev in TELJESSEG_HALOK if kulcs in fo]
    szoveg = 'gépi teljesség-mérés' + (' (%s)' % ', '.join(halo) if halo else '')
    n = csoport_versszam(fo)
    if n is not None:
        szoveg += '; csoportos kizárás: %d vers, az első itt' % n
    return szoveg


def jeloles_oka(forras_kereses):
    """(csoport, közérthető szöveg) a `forras_kereses` mezőből; a be nem sorolható `BeNemSorolhato`-t dob."""
    nyers = (forras_kereses or '').split(' | ')[0].strip()
    fo = re.split(r';\s*napló:', nyers)[0].strip()
    helyek = HELY.findall(fo)
    hely = helyek[0] if helyek else ''
    if fo.startswith('TSK/Károli-KH'):
        return CSOPORTOK[1], ('TSK- és Károli-kereszthivatkozás %s' % _ahol(hely, 'helyről') if hely
                              else 'TSK- és Károli-kereszthivatkozás')
    if fo.startswith('TSK'):
        if 'alacsony szavazat' in fo:
            return CSOPORTOK[0], 'TSK-ajánlás, alacsony szavazattal'
        cel = (' ' + _ahol(helyek[1], 'helyre')) if ('→' in fo or '↔' in fo) and len(helyek) > 1 else ''
        szoveg = 'TSK-ajánlás %s%s%s' % (_ahol(hely, 'helyről'), cel, _tsk_reszlet(fo)) if hely else 'TSK-ajánlás'
        if 'Károli-KH is' in fo:
            szoveg += ' (a Károli is ajánlja)'
        if re.match(r'scan', fo):
            szoveg += ' és gépi Strong-keresés'
        return CSOPORTOK[0], szoveg
    if fo.startswith('Károli-KH'):
        return CSOPORTOK[1], ('Károli-kereszthivatkozás %s' % _ahol(hely, 'helyről') if hely
                              else 'Károli-kereszthivatkozás')
    if re.match(r'scan', fo):
        st = STRONG.findall(fo)
        szoveg = 'gépi Strong-keresés: %s' % ', '.join(st) if st else 'gépi Strong-keresés'
        if 'TSK' in fo:
            szoveg += ', TSK-ajánlással'
        return CSOPORTOK[2], szoveg
    if fo.startswith('kollokacio'):
        return CSOPORTOK[2], 'gépi szópár-keresés: %s' % ' + '.join(STRONG.findall(fo))
    if fo.startswith('motívumközi'):
        return CSOPORTOK[2], 'motívumközi mérés (szomszédos vers egy másik motívumban)'
    if 'Seol-scan' in fo:
        return CSOPORTOK[2], 'gépi keresés a szó környezetében (Seol-ablak)'
    if 'visszakeresés' in fo:
        return CSOPORTOK[2], 'gépi visszakeresés a héber szövegben'
    if fo.startswith('tematikus:'):
        p = re.search(r'\(([^)]*)\)\s*$', fo)
        return CSOPORTOK[3], 'a tematikus tanulmány felvetése' + (' (%s)' % p.group(1) if p else '')
    if fo.startswith('napló:') or (not fo and 'napló:' in nyers):
        return CSOPORTOK[3], 'a kereszthivatkozás-napló kutatói minősítése'
    if fo.startswith('nevesített tanító'):
        t = re.match(r'nevesített tanító:\s*([^(;]+)', fo)
        return CSOPORTOK[3], 'nevesített tanító felvetése' + (': %s' % t.group(1).strip() if t else '')
    if fo.startswith('BDB'):
        return CSOPORTOK[3], 'szótári felvetés (BDB)'
    if fo.startswith('study') or fo.startswith('döntési fájl'):
        return CSOPORTOK[3], 'a tanulmány felvetése'
    if fo.startswith('négyforrásos audit'):   # F123.HAMART3 határkör: a régi tanulmány beépített helyei, most elutasítva
        return CSOPORTOK[3], 'a motívum korábbi tanulmányának négyforrásos ellenőrzése'
    if 'teljesség-mérés' in fo:
        return CSOPORTOK[2], _teljesseg(fo)
    if fo.startswith('pozíció-alapú frázis-keresés'):
        return CSOPORTOK[2], 'gépi frázis-keresés a szavak helyzete szerint, szótári, TSK- és Septuaginta-ellenőrzéssel'
    if fo.startswith('rokon '):
        par = [g.replace('|', '/') for g in re.findall(r'\(([^)]*)\)', fo)]
        return CSOPORTOK[2], 'gépi szópár-keresés: %s%s' % (' + '.join(par), ' (±1 vers)' if '±1' in fo else '')
    if fo.startswith('csalad '):
        return CSOPORTOK[2], 'gépi Strong-keresés a szócsaládban: %s' % ', '.join(STRONG.findall(fo))
    if fo.startswith('lanc'):
        return CSOPORTOK[2], 'gépi lánc-keresés: legalább két lánc-szó egy versben vagy a szomszédos versben'
    # általános szabály: a lekérdezés saját proveniencia-sora (nem `manual` scope) gépi keresést jelez
    if re.search(r'(?:^|\|)\s*scope=(?!manual\b)\S', forras_kereses or ''):
        return CSOPORTOK[2], 'gépi keresés'
    raise BeNemSorolhato('jelölési forrás: a `jeloles_oka` nem sorolja be: %s' % (forras_kereses or '—')[:120])


def _cella(s):
    return s.replace('|', '\\|').replace('\n', ' ')


# --- Az indoklás olvasói alakja (olvasói kapu, 2026-11-02) ---------------------------------------------------------
# Az `indoklas` adatmező a munkafolyamat naplója is: döntés-azonosítót, fájlnevet, munkaszereplőt, angol címkét hordoz.
# Az adat nem változik (DT28); a lapra az olvasói alak kerül, a nyers szöveg a lábjegyzetben marad.
BELSO_KIFEJEZES = [re.compile(x, re.I) for x in (
    r'\bF\d{1,3}(?:\.\d+)? szűrő\b', r'\b[A-D] osztály\b', r'\bK\d_\w+\b', r'\bkézi olvasás\b',
    r'\bretroaktív F\d+\.\d+ betöltés\b', r'\borkesztrátor(?:-chat)?\b')]
ANGOL_CSERE = [(re.compile(r'\bscanje\b'), 'keresése'), (re.compile(r'\bscan\b'), 'keresés'),
               (re.compile(r'\bstudy\b'), 'tanulmány'), (re.compile(r'\bgap\b'), 'hiány')]
AZON_ELEJEN = re.compile(r'^(?:(?:DT-?F?|N-?F?|F)\d+[a-z]?(?:\.\d+)?(?:\s+K\d(?:/K\d)?)?[\s:,;]*)+')
DONTES_MONDAT = re.compile(r'\s*Döntés:\s*(?:DT-?F?\d+[a-z]?)\s*(?:\([^()]*\))?\.?')


def _piszkos(t):
    """Belső jelölés, angol zsargon vagy egyenes idézőjel van benne (az olvasói kapu szabályai szerint)."""
    import olvasoi_kapu as K   # a kapu szabályai az egyetlen mérce: amit megfog, azt itt is kivesszük
    return (any(rx.search(t) for rx, _ in K.BELSO) or bool(K.ANGOL_SZO.search(K.kod_nelkul(t)))
            or '"' in K.kod_nelkul(t))


def _felso_zarojelek(t):
    """A legkülső zárójelcsoportok (kezdet, vég) helyei; a beágyazott zárójel a csoport része."""
    ki, mely, kezd = [], 0, 0
    for i, c in enumerate(t):
        if c == '(':
            if mely == 0:
                kezd = i
            mely += 1
        elif c == ')' and mely:
            mely -= 1
            if mely == 0:
                ki.append((kezd, i + 1))
    return ki


def olvasoi_indok(szoveg):
    """Az indoklás olvasói alakja, vagy None, ha tisztítás után sem olvasói szöveg. A belső jelölést hordozó zárójeles
    csoportot (pl. „(DT478, a felhasználó …)”), kód-jelölést és munkafolyamat-kifejezést elhagyja; az ok maga marad.
    Ha nincs benne belső jelölés, változatlanul adja vissza (az egyenes idézőjelet a lap utófeldolgozása javítja)."""
    t = szoveg or ''
    if not _piszkos(t.replace('"', '')):
        return t
    for rx in BELSO_KIFEJEZES:
        t = rx.sub('', t)
    elso = AZON_ELEJEN.match(t.strip())
    if elso:   # „DT478 (a felhasználó, …): ok” — az azonosítót követő minősítő zárójel is a naplóhoz tartozik
        t = t.strip()[elso.end():]
        if t.startswith('(') and _felso_zarojelek(t):
            t = t[_felso_zarojelek(t)[0][1]:]
    for a, b in reversed(_felso_zarojelek(t)):
        if _piszkos(t[a:b].replace('"', '')):
            t = t[:a] + t[b:]
    t = re.sub(r'`[^`]*`', lambda m: '' if _piszkos(m.group(0)) else m.group(0), t)
    t = DONTES_MONDAT.sub('', t)
    t = AZON_ELEJEN.sub('', t.strip())
    for rx, ki in ANGOL_CSERE:
        t = rx.sub(ki, t)
    t = re.sub(r'\s+([:,;.])', r'\1', t)
    t = re.sub(r'([,;:])\s*(?:[,;:]\s*)+', r'\1 ', t)
    t = re.sub(r'\s{2,}', ' ', t).strip(' ,;:')
    if len(re.findall(r'[^\W\d_]{3,}', t)) < 2 or _piszkos(t.replace('"', '')):
        return None
    return t


# A `dontes_ref` (SEMA 2.4) elemei ` · `-tal; a helyőrző alakú azonosító (pl. a számozás előtti N-F63a) az adatban a
# pontos nyom, a lapon viszont nem állhat (ellenoriz.py 21. szabály (i)), ezért a lábjegyzetből kimarad.
NYOM_SEP = ' · '
HELYORZO = re.compile(r'(?<![\w-])(?:DT|N|D)-F\d+[a-z]*\b')


def nyom_lapra(dontes_ref):
    """A `dontes_ref` lapra kerülő alakja: az elemek a helyőrző alakúak nélkül; üres, ha nem marad semmi."""
    elemek = [e.strip() for e in (dontes_ref or '').split(NYOM_SEP)]
    return NYOM_SEP.join(e for e in elemek if e and not HELYORZO.search(e))


# F123.TUD1B (3): az indoklás adatszövegében a latin betűs szó (kiejtés, átírás) utáni zárójeles Strong-szám („nem a
# JHVH (H3068) szó”) a lapon a #624 szerinti jelölt alakot kapja (DT-F181b): a szó a szónézet hivatkozása, a szám halvány
# felső index. Az `olvasoi_utofeldolg.strong_ki` ezt az alakot szándékosan érintetlenül hagyja (a próza „a kárá (H7121)”
# alakja adat); az 1/b. indoklásaiban viszont a szám a szó azonosítója, ezért itt jelöljük. Az adat nem változik.
# csak latin betűs szó: a héber/görög szó melletti számot az `olvasoi_utofeldolg.strong_ki` jelöli (a kiejtéssel együtt)
INDOK_STRONG = re.compile(r'(?<![\w\[\]/\-֑-ׇ])(?P<szo>[A-Za-zÀ-ɏ]+)(?P<jel>[*_]*) \(\s*(?P<strong>[HG]\d{4}[a-z]?)\s*\)')


def indok_strong(szoveg, cim=None):
    import olvasoi_utofeldolg as OU
    return INDOK_STRONG.sub(lambda m: '[%s](%s)%s%s' % (m.group('szo'), OU.SZONEZET % m.group('strong'),
                                                        m.group('jel'), OU.strong_jel(m.group('strong'), cim)),
                            szoveg)


def indok_cella(indoklas, ures='—'):
    """Az indoklás táblacellába szánt olvasói alakja: a nyers szöveg proveniencia-farka (` | scope=…`) változatlan;
    ha a főszöveg tisztítás után sem olvasói, a cella `ures` (a nyers szöveg az adattáblában van)."""
    fo, sep, farok = (indoklas or '').partition(' | ')
    olv = olvasoi_indok(fo)
    if olv is None:
        olv = ures
    return _cella(olv + sep + farok)


# F152 B.2: a blokkban ismétlődő proveniencia-sor a soron jellé rövidül, és a blokk alatt egyszer áll; a táblacellában
# a `|` escape-elve (`\|`) is. Alakja: `scope=… | forras=… | ts=…`, a lekérdezés további mezőivel a forras és a ts között
# (`strong=… | n=…`) és a ts után (`csatorna=…`), ahogy a `lekerdez.py` írja.
_SEP = r'\s\\?\|\s*'
PROV_HARMAS = re.compile(r'scope=[^|`\n]*?' + _SEP + r'forras=[^|`\n]*?(?:' + _SEP + r'(?!ts=)[a-z_]+=[^|`\n]*?)*'
                         + _SEP + r'ts=[0-9T:Z-]+(?:' + _SEP + r'csatorna=[a-z_]+)?')


def kozos_proveniencia(szovegek, elotag, kuszob=2):
    """(új szövegek, a blokk alá kerülő megjegyzés-sor vagy ''). Minden proveniencia-sor, amely a szövegek közül
    legalább `kuszob`-ban áll, gyakoriság szerint jelet kap: ‹`elotag`1›, ‹`elotag`2› … — az előtag blokkonként más
    (a lapon egy jel egy jelentés, és nem ütközik a szótárak saját jeleivel, pl. az Abbott-Smith †-ével); a szövegben a
    helyére a jel kerül, a megjegyzés-sor a jelet és a teljes proveniencia-sort egyszer hordozza. A proveniencia nem
    vész el, csak nem ismétlődik; az egyszer álló sor a helyén marad."""
    szaml = collections.Counter()
    for s in szovegek:
        for p in set(m.group(0).replace('\\|', '|') for m in PROV_HARMAS.finditer(s)):
            szaml[p] += 1
    kozos = [p for p, n in sorted(szaml.items(), key=lambda x: (-x[1], x[0])) if n >= kuszob]
    if not kozos:
        return list(szovegek), ''
    jel = {p: '‹%s%d›' % (elotag, i) for i, p in enumerate(kozos, 1)}

    def csere(m):
        p = m.group(0).replace('\\|', '|')
        return jel.get(p, m.group(0))
    uj = [PROV_HARMAS.sub(csere, s) for s in szovegek]
    if len(kozos) == 1 and szaml[kozos[0]] == len(szovegek):
        return uj, '*Minden sor forrásmegjelölése (%s): `%s`*' % (jel[kozos[0]], kozos[0])
    return uj, '*A közös forrásmegjelölések: %s*' % ' · '.join(
        '%s = `%s` (%d sor)' % (jel[p], p, szaml[p]) for p in kozos)


def _hely_reszek(hely):
    m = re.fullmatch(r'(.+) (\d+):(\d+)', hely)
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def osszevon(sorok_c):
    """F152 B.3: a csoport egymást követő sorai, ha egymást követő versek (ugyanaz a könyv és fejezet), és a „miért
    lett jelölt”, a döntés és az indok, valamint a lábjegyzet szövege azonos: egy sor, tartományként („1Móz
    25:21–26”). A lábjegyzet egyszer áll (azonos szövegű volt minden soron), az adat nem változik."""
    ki = []
    for t in sorok_c:
        if ki:
            elozo, utolso = ki[-1]
            a, b = _hely_reszek(utolso), _hely_reszek(t[0])
            if a and b and a[:2] == b[:2] and b[2] == a[2] + 1 and elozo[1:] == t[1:]:
                ki[-1] = (elozo, t[0])
                continue
        ki.append((t, t[0]))
    eredmeny = []
    for t, utolso in ki:
        if utolso != t[0]:
            t = ('%s–%d' % (t[0], _hely_reszek(utolso)[2]),) + tuple(t[1:])
        eredmeny.append(t)
    return eredmeny


def blokk_torzs(sorok, motivum_id, okok_ut=None, strong_cim=None):
    """(törzs-sorok listája, lábjegyzetek listája, összesítő dict) az 1/b. blokkhoz. `strong_cim`: a jelölt Strong-szám
    `title`-je (`lexikon_general.strong_cim`; alapból a szám)."""
    minta = okok(motivum_id, okok_ut)
    megj = ok_megjegyzesek(motivum_id, okok_ut)
    pelda = collections.OrderedDict()
    csop = collections.OrderedDict((c, []) for c in CSOPORTOK)
    ok_szaml, forras_szaml = collections.Counter(), collections.Counter()
    labj = []
    hiany = hianyok(sorok, motivum_id, minta)
    if hiany:
        raise BeNemSorolhato('%s: %d be nem sorolható sor az 1/b. blokkban — %s' % (
            motivum_id, len(hiany), '; '.join('%s (%s)' % x for x in hiany[:10])))
    for r in sorok:
        c, miert = jeloles_oka(r.get('forras_kereses'))
        # F123.TUD1B: a súly a sor verseinek száma (összesítő sor: a blokk, tartomány: a kibontott versek)
        suly = csoport_versszam(r.get('forras_kereses')) or len(versek(r.get('igehely')))
        forras_szaml[c] += suly
        ind = r.get('indoklas') or ''
        fo_ind, _sep, farok = ind.partition(' | ')
        if r.get('dontes') == 'nyitva':
            dontes = '**nyitott döntés**'
            ok_szaml['nyitott döntés'] += suly
        else:
            ok = olvasoi_ok(elutasitas_oka(fo_ind, minta))
            ok_szaml[ok] += suly
            if r['igehely'] not in pelda.setdefault(ok, []) and len(pelda[ok]) < 2:
                pelda[ok].append(r['igehely'])
            dontes = '**elutasítva** — %s' % ok
        olv = olvasoi_indok(fo_ind)
        lj = 'forrás: `%s`%s' % (r.get('forras_kereses') or '—', (' · ' + farok) if farok else '')
        if nyom_lapra(r.get('dontes_ref')):   # F123.INDOKLAS: a döntés gépi nyoma
            lj += ' · a döntés nyoma: `%s`' % nyom_lapra(r.get('dontes_ref'))
        if olv != fo_ind:
            lj += ' · indoklás (nyers): %s' % _cella(fo_ind)
        if olv is None:
            csop[c].append((r['igehely'], _cella(miert), dontes, lj))
        else:
            csop[c].append((r['igehely'], _cella(miert), '%s: %s' % (dontes, indok_strong(_cella(olv), strong_cim) or '—'), lj))
    ki = []
    for c, sorok_c in csop.items():
        if not sorok_c:
            continue
        sor_md = []
        for hely, miert, dont, lj in osszevon(sorok_c):
            labj.append(lj)
            sor_md.append('| %s | %s[^k%d] | %s |' % (hely, miert, len(labj), dont))
        # a darabszám a jelölteké, nem az összevont soroké; összesítő sornál a versszám is (F123.TUD1B)
        if forras_szaml[c] != len(sorok_c):
            ki.append('**%s** (%d sor, %d vers)' % (c, len(sorok_c), forras_szaml[c]))
        else:
            ki.append('**%s** (%d)' % (c, len(sorok_c)))
        ki.append('| Igehely | Miért lett jelölt | Döntés és indok |\n|---|---|---|\n' + '\n'.join(sor_md))
    ossz = {'ok': ok_szaml, 'forras': forras_szaml, 'pelda': pelda,
            'megj': {k: megj.get(k, '') for k in ok_szaml}}
    return ki, labj, ossz


def hianyok(sorok, motivum_id, minta=None):
    """[(igehely, mi nem sorolható be)] a motívum elutasított / nyitva maradt jelöltjei közül: a jelölés forrása
    (`jeloles_oka`) vagy az elutasítás oka (a mintaszótár). Üres lista: a blokk generálható. A generátor és az
    `ellenoriz.py` 28. szabálya ugyanezt a függvényt hívja."""
    minta = okok(motivum_id) if minta is None else minta
    ki = []
    for r in sorok:
        try:
            jeloles_oka(r.get('forras_kereses'))
        except BeNemSorolhato:
            ki.append((r.get('igehely', ''), 'jelölési forrás'))
        if r.get('dontes') == 'elutasítva':
            try:
                elutasitas_oka((r.get('indoklas') or '').partition(' | ')[0], minta)
            except BeNemSorolhato:
                ki.append((r.get('igehely', ''), 'elutasítási ok'))
    return ki


TABLA_OK_MAX = 10


def osszesito_sor(ossz):
    """Az összesítő bekezdés: az elutasítás okai (gyakoriság szerint, a nyitott a végén), a jelölés forrásai."""
    ok = ossz['ok']
    rend = sorted((k for k in ok if k != 'nyitott döntés'), key=lambda k: (-ok[k], k))
    # F123.HAMART3 (a felhasználó átnézése): okonként összevont döntési tábla, csökkenő versszám szerint; a tíz
    # legnagyobb ok a táblában, a többi alatta egy mondatban, versszámmal („egyéb” sor nincs)
    if rend:
        tabla = ['| Ok | Vers | Mit jelent | Példa |', '|---|---|---|---|']
        for k in rend[:TABLA_OK_MAX]:
            tabla.append('| %s | %d | %s | %s |' % (_cella(k), ok[k], _cella((ossz.get('megj') or {}).get(k) or '—'),
                                                  ', '.join((ossz.get('pelda') or {}).get(k) or []) or '—'))
        sor = ['**Az elutasítás okai:**\n\n' + '\n'.join(tabla)]
        if len(rend) > TABLA_OK_MAX:
            tobbi = rend[TABLA_OK_MAX:]
            sor.append('További %d ok, összesen %d vers: %s.' % (len(tobbi), sum(ok[k] for k in tobbi),
                                                                '; '.join('%s (%d)' % (k, ok[k]) for k in tobbi)))
    else:
        sor = ['**Az elutasítás okai:** —']
    if ok.get('nyitott döntés'):
        sor.append('**Nyitott döntés:** %d' % ok['nyitott döntés'])
    sor.append('**A jelölés forrása:** ' + ' · '.join('%s %d' % (c, ossz['forras'][c]) for c in CSOPORTOK
                                                     if ossz['forras'].get(c)))
    return '\n\n'.join(sor)
