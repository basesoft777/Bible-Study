"""bdb_tagolas.py — a BDB-szócikk tagolása a szakasztáblából (`adat/bdb_szakaszok.tsv`, SEMA 2.30): egy szabály, egy hely.

A #185 óta a vers → jelentéspont döntés a javított szakasztáblából jön (DT726, SEMA 2.29). A tagolás megjelenítése ezért
ugyanebből a táblából épül (F182, 2. fázis, F33; N138):

- `szocikkek`: a Strong szócikkei a 2.30 sorrendjében, a szakaszok (kulcs: `(bdb_id, utvonal)`) szócikken belül
  útvonalanként összevonva — a lexikon-generátor 4.2-es kártyájának fája (`lexikon_general.bdb_gerinc_szocikkek`);
- `szakasz_szerint`: a sorok szakasz-címkéje (római szám, illetve a jelöletlen alcímszó `h:<váz>` címkéje) — ugyanaz a
  szabály, amellyel a 2.29 generátora (`olvaso_szerver/bdb_vers_jelentes.TablaPont`) a jelentéspont szakaszát adja;
- `ut3`: a 2.30 útvonala a 2.29 alakjában (a csomópont kulcsa);
- `szeletelo_alak`: ugyanez a fa az olvasó (`olvaso_szerver/blokkok.py`) megjelenítőjének alakjában (törzsek →
  jelentések → alpontok, további szakaszok), hogy az olvasó csomópontjai és a 2.29 útvonalai egy forrásból legyenek.

A szeletelő (`olvaso_szerver/bdb_szelet.py`) a tábla előállításában szerepel; a tagolás megjelenítésében nem. Az olvasó
a címszó fejének szövegét (alapjelentés, nyelvi háttér, alakok) a fej-szöveg elemzőjével bontja (`fej_elemzo` paraméter):
ez a fej szövegének elemzése, nem a tagolás.

A `szakasz_szerint` és az `ut3` szabálya a 2.29 generátoráé; a `bdb_vers_jelentes.py` itt nem változik, mert a fájl a
tábla kód-hash bemenete (`KOD_FAJLOK`). Az egyezést teszt őrzi (`eszkozok/teszt_bdb_tagolas.py`). Csak standard könyvtár.
"""
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HB_SZO = re.compile(r'[֐-׿יִ-ﭏ][֐-׿יִ-ﭏ־]*')
RESZ_SEP = '§'   # az olvasó szakasz-címkéjének elválasztója (`bdb_szelet.RESZ_SEP`)


def kons(x):
    """A héber szó mássalhangzó-váza (a prezentációs alakok kanonikus felbontása után); a `bdb_szelet._kons` szabálya."""
    return re.sub(r"[֑-ׇ]", "", unicodedata.normalize('NFD', x or ""))


def rendez(sorok):
    return sorted(sorok, key=lambda x: int(x['sorszam']))


def szakasz_szerint(sorok):
    """[(szakasz, rész)] soronként, a sorszám szerinti sorrendben (a `TablaPont` szabálya): a fő szócikk (alszócikk 0)
    szakasza a római szám; a jelöletlen alcímszó (`jelolo` = `alcimszo`) címkéje `h:<váz>`, héber címszó nélkül a fő
    szakaszé; az alszócikk sorai az alcímszó szakaszát viszik tovább."""
    ki, alcim, fo = [], '', ''
    for x in sorok:
        if x.get('alszocikk') == '0' and x.get('szakasz'):
            fo = x['szakasz']
        if x.get('jelolo') == 'alcimszo':
            m = re.match(r'\[?(' + HB_SZO.pattern + ')', x.get('szoveg') or '')
            alcim = 'h:' + kons(m.group(1)) if m else fo
        elif x.get('alszocikk') == '0':
            alcim = ''
        ki.append((x.get('szakasz') or alcim, x.get('resz') or ''))
    return ki


def ut3(ut):
    """A 2.30 útvonala a 2.29 alakjában: a nagybetűs csoport és a zárójeles szint nélkül, három szint, a hiányzó alpont
    nélkül („-/3”, „Qal/-”); `cim`/`fej` → `fej`."""
    if ut in ('cim', 'fej', ''):
        return 'fej'
    r = ut.split('/')
    r[0] = r[0].split('.')[0]
    r = r[:3]
    while len(r) < 3:
        r.append('-')
    if r[2] == '-':
        r = r[:2]
    return '/'.join(r)


def szocikkek(sorok, hu, jel_fn, javit=None):
    """A Strong BDB-szócikkei a 2.30 (a BDB) sorrendjében: ([{'bdb_id', 'fej', 'szakaszok'}], elnyelt).
    `sorok`: a Strong 2.30-sorai; `hu`: {sorszám: a 2.32 sora}; `jel_fn(utvonal)`: a szakasz jele; `javit(szöveg)`: a
    megjelenítés előtti szövegjavítás (None: változatlan).
    A szakasz (kulcs, jel, szöveg_hu, angol, kategória), a kulcs (bdb_id, utvonal): szócikken belül útvonalanként
    összevonva (a `jelolo_nelkul` sor szövege az előző szakaszé), `cim` nélkül; a `fej` külön. Különböző szócikkek
    azonos útvonalú szakaszai nem vonódnak össze (F123.BDBGER). `elnyelt`: {kulcs: kulcs} — a jelölő nélküli, magyar
    szöveg nélküli szakasz, amelynek szövege a 2.32 szerint az előző sorban, egy másik szócikk szakaszában áll."""
    javit = javit or (lambda t: t)
    sorrend, adatok, elnyelt = [], {}, {}
    utolso_hu = None
    for r in rendez(sorok):
        ut = r['utvonal']
        if ut == 'cim':
            continue
        k = (r.get('bdb_id', ''), ut)
        h = hu.get(r['sorszam']) or {}
        if k not in adatok:
            sorrend.append(k)
            adatok[k] = {'hu': [], 'en': [], 'kat': '', 'elnyelo': None, 'ures': True}
        e = adatok[k]
        if h.get('szoveg_hu'):
            e['hu'].append(h['szoveg_hu'])
            utolso_hu = k
        elif h.get('kategoria') == 'jelolo_nelkul' and utolso_hu and utolso_hu[0] != k[0] and e['elnyelo'] is None:
            e['elnyelo'] = utolso_hu
        if (r.get('szoveg') or '').strip():
            e['en'].append(('%s %s' % (r.get('jel') or '', r['szoveg'])).strip())
        if h.get('kategoria') in ('horgonnyal', 'elakad') or not e['kat']:
            e['kat'] = h.get('kategoria') or e['kat']
    ki = []
    for k in sorrend:
        e = adatok[k]
        szoveg_hu = ' '.join(e['hu']) if e['hu'] else None
        if e['kat'] == 'elakad':
            szoveg_hu = None
        if szoveg_hu is None and e['elnyelo'] and e['kat'] == 'jelolo_nelkul':
            elnyelt[k] = e['elnyelo']
        sz = (k, jel_fn(k[1]), javit(szoveg_hu), javit(' '.join(e['en'])), e['kat'])
        if not ki or ki[-1]['bdb_id'] != k[0]:
            ki.append({'bdb_id': k[0], 'fej': None, 'szakaszok': []})
        if k[1] == 'fej':
            ki[-1]['fej'] = sz
        else:
            ki[-1]['szakaszok'].append(sz)
    return ki, elnyelt


def _jel_le(szoveg, jel):
    """A csomópont szövegéről a saját jele (a 2.30 `jel` mezője, pl. „1”, „a.”, „Qal”) lekerül, ha azzal kezdődik."""
    s = (szoveg or '').strip()
    j = (jel or '').strip()
    if j and s.startswith(j):
        s = s[len(j):].lstrip(' .')
    return s


def szeletelo_alak(sorok, hu, nyelv, fej_elemzo, ref_szam):
    """A szakasztábla fája az olvasó megjelenítőjének alakjában (a `bdb_szelet.szeletel` kimenetének kulcsaival).
    `sorok`: a Strong 2.30-sorai; `hu`: {sorszám: a 2.32 sora}; `nyelv`: 'hu' vagy 'en' (a csomópont szövege: a magyar,
    ennek híján az angol; 'en' esetén az angol); `fej_elemzo(fej_szöveg)`: a fej elemzése (dict: fej, alap, nyelvi,
    alaktan, irodalom, krit); `ref_szam(szöveg)`: a szövegben álló igehely-hivatkozások száma.
    A csomópontok kulcsa — (szakasz-címke, `törzs/jel` vagy `törzs/jel/al`) — a 2.29 `szakasz`, `resz` és `utvonal`
    mezőjével azonos alakú (`ut3`). Az első szakasz a fő címszó; a többi a `szakaszok` listában (római szám:
    `azonos_lemma`, `h:` alcímszó: `masik_lemma`, rész: `tagolas`). None, ha nincs tagolható sor."""
    rend = [r for r in rendez(sorok) if r['utvonal'] != 'cim']
    if not rend:
        return None
    szak = dict(zip((r['sorszam'] for r in rendez(sorok)), szakasz_szerint(rendez(sorok))))
    szakaszok, aktualis = [], None
    for r in rend:
        cim = szak[r['sorszam']]
        if aktualis is None or aktualis['cim'] != cim or aktualis['bdb_id'] != r.get('bdb_id', ''):
            aktualis = {'cim': cim, 'bdb_id': r.get('bdb_id', ''), 'sorok': []}
            szakaszok.append(aktualis)
        aktualis['sorok'].append(r)

    def szoveg(r):
        h = hu.get(r['sorszam']) or {}
        if nyelv == 'hu' and h.get('szoveg_hu') and h.get('kategoria') != 'elakad':
            return _jel_le(h['szoveg_hu'], r.get('jel'))
        return (r.get('szoveg') or '').strip()

    def fa(sz):
        torzsek, fej_szoveg, fej_db = [], [], ''
        for r in sz['sorok']:
            u = ut3(r['utvonal'])
            t = szoveg(r)
            if u == 'fej':
                if t:
                    fej_szoveg.append(t)
                fej_db = fej_db or (r.get('gyakorisag') or '')
                continue
            reszek = u.split('/')
            tn = '' if reszek[0] == '-' else reszek[0]
            jel = '' if len(reszek) < 2 or reszek[1] == '-' else reszek[1]
            al = reszek[2] if len(reszek) > 2 else ''
            if not torzsek or torzsek[-1]['nev'] != tn:
                torzsek.append({'nev': tn, 'db': '', 'jelentesek': []})
            torzs = torzsek[-1]
            if not jel and not al and tn and not torzs['db']:
                torzs['db'] = r.get('gyakorisag') or ''
            js = torzs['jelentesek']
            if not js or js[-1]['jel'] != jel:
                js.append({'jel': jel, 'szoveg': '', 'ref': 0, 'al': []})
            j = js[-1]
            if al:
                if not j['al'] or j['al'][-1]['jel'] != al:
                    j['al'].append({'jel': al, 'szoveg': '', 'ref': 0})
                cel = j['al'][-1]
            else:
                cel = j
            cel['szoveg'] = ('%s %s' % (cel['szoveg'], t)).strip() if t else cel['szoveg']
        for torzs in torzsek:
            for j in torzs['jelentesek']:
                for a in j['al']:
                    a['ref'] = ref_szam(a['szoveg'])
                j['ref'] = ref_szam(j['szoveg']) + sum(a['ref'] for a in j['al'])
        if not torzsek:
            torzsek = [{'nev': '', 'db': '', 'jelentesek': []}]
        return torzsek, ' '.join(fej_szoveg), fej_db

    fo = szakaszok[0]
    torzsek, fej_szoveg, fej_db = fa(fo)
    e = fej_elemzo(fej_szoveg) or {}
    fej = dict(e.get('fej') or {})
    # a kijelzés (homonima-szám) a fej szövegéből; a csomópontok kulcsa a 2.29 címkéje (`cimke`)
    fej['cimke'] = fo['cim'][0] + (RESZ_SEP + fo['cim'][1] if fo['cim'][1] else '')
    fej.setdefault('homonima', '')
    if fej_db:
        fej['ossz'] = fej_db
    ki = {'fej': fej, 'alap': e.get('alap'), 'nyelvi': e.get('nyelvi') or [], 'alaktan': e.get('alaktan') or '',
          'torzsek': torzsek, 'irodalom': e.get('irodalom') or [], 'krit': e.get('krit') or [], 'elotag': '',
          'szakaszok': []}
    for sz in szakaszok[1:]:
        t, fsz, _db = fa(sz)
        ee = fej_elemzo(fsz) or {}
        s, resz = sz['cim']
        heber = ''
        m = HB_SZO.search(fsz)
        if m:
            heber = m.group(0)
        if resz:
            x = {'szerep': 'tagolas', 'gazda': s, 'jel': resz}
        elif s.startswith('h:'):
            # a címke a 2.29 alakja (`h:<váz>`): a megjelenítő ugyanezt képzi a `heber` mezőből (`_szakasz_cimke`)
            x = {'szerep': 'masik_lemma', 'jel': ''}
            if kons(heber) != s[2:]:
                heber = s[2:]
        else:
            x = {'szerep': 'azonos_lemma', 'jel': s}
        # a 2.29 címkéje: ha két szócikk ugyanazt kapja (H7451: BDB8032 és BDB8034 is ''), a csomópont-kulcs ütközik, és az
        # olvasó a sort „nem azonosítható”-ként mutatja, nem csatolja csendben a másik szócikk csomópontjához
        x['cimke'] = s + (RESZ_SEP + resz if resz else '')
        x.update({'heber': heber or (ee.get('fej') or {}).get('heber') or '', 'alap': ee.get('alap') or '',
                  'nyelvi': ee.get('nyelvi') or [], 'torzsek': t, 'nyelv': '', 'ref': ref_szam(fsz)})
        ki['szakaszok'].append(x)
    ki['ref_ossz'] = ref_szam(fej_szoveg) + sum(j['ref'] for tz in torzsek for j in tz['jelentesek']) + sum(
        x['ref'] for x in ki['szakaszok'])
    return ki


def szakasz_cimke(x):
    """Az olvasó szakasz-címkéje egy `szeletelo_alak` szakaszra: a 2.29 címkéje (`cimke`); ennek híján a
    `bdb_szelet._szakasz_cimke` szabálya."""
    if x.get('cimke') is not None:
        return x['cimke']
    if x.get('szerep') == 'tagolas':
        return '%s%s%s' % (x.get('gazda', ''), RESZ_SEP, x['jel'])
    if x['jel']:
        return x['jel']
    return 'h:' + kons(x['heber'])


def megjelenitett_pontok(alak, egyertelmu=True):
    """{(szakasz-címke, útvonal)}: a megjelenített fa csomópontjai a 2.29 kulcsának alakjában (az olvasó `VersJelolo`
    bejárásával azonosan). `egyertelmu`: csak az egyszer álló kulcs (a kétszer álló kulcsot az olvasó nem azonosítja: két
    szócikk ugyanazzal a 2.29-címkével; a kártya a hely szerint dönt, az olvasó nem: N-F182c)."""
    db = {}

    def bejar(cimke, tl):
        for t in tl:
            tn = t['nev'] or '-'
            for j in t['jelentesek']:
                jp = '%s/%s' % (tn, j['jel'] or '-')
                db[(cimke, jp)] = db.get((cimke, jp), 0) + 1
                for a in j['al']:
                    k = (cimke, '%s/%s' % (jp, a['jel']))
                    db[k] = db.get(k, 0) + 1
    bejar(alak['fej'].get('cimke', alak['fej'].get('homonima', '')) or '', alak['torzsek'])
    for x in alak.get('szakaszok') or []:
        bejar(szakasz_cimke(x), x['torzsek'])
    return {k for k, n in db.items() if n == 1 or not egyertelmu}


def vers_kulcs(r):
    """A 2.29 sorának csomópont-kulcsa: (szakasz-címke, útvonal)."""
    return (r.get('szakasz') or '') + (RESZ_SEP + r['resz'] if r.get('resz') else ''), r['utvonal']
