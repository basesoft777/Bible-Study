"""A szótári szerepmátrix 13. (Károli-megfelelők) és 14. (Rejtett / hamis párhuzam) szerepe — általános, motívumfüggetlen
építők (ISTENTISZT-001 arany lap, 2026-10-29; a szerepek leírása: `adat/szotar_szerepek.tsv`).

Bemenet: a motívum `elofordulasok.tsv`-sorai (dict-ek: `id`, `igehely`, `strong`, `karoli_szo`); a `konkordancia/Karoli_1908.tsv`
(versszöveg); a `TAHOT_kivonat.tsv` és a `TAGNT_kivonat.tsv` (versenkénti Strong-halmaz; az `Igehely` a Károli-vers, F85); az
`adat/szoto/karoli_szotari_alak.tsv` (szótári alak, DT130); az `adat/karoli_strong/parok_<könyv>.tsv` (Károli–Strong
párosítás, javaslat-állapotú modell-kimenet, SEMA 2.20); az `adat/grammatikai_strongok.tsv`; az `adat/jeloltek.tsv` (a meglévő
döntés kiírásához). Mind determinisztikus; a 14. csak megjelenít: jelölt csak a `jeloltek.tsv`-n át lesz (CLAUDE.md 2. szabály).

A szó a szótári alakja szerint számít (a mai helyesírású `szotari_alak_mai`, kisbetűvel): a *segítségűl* és a *segítségül*,
a *nevét* és a *nevedet* egy szó; a táblában nem álló alak önmaga.

- 13. **Károli-megfelelők:** a motívumsorok `karoli_szo`-jának szavai (névelő nélkül), szótári alakonként: a szóalakok, és
  hány igehelyen, melyiken. A „+SZPA” rész csak akkor áll (jelölt hiányként), ha az `adat/funkcio_kapcsolok.tsv`
  `SZPA_JOIN` kapcsolója `aktiv`; felfüggesztve a sor és a szerepcím „(+ SZPA)” része elmarad (ISTENTISZT-001 arany lap, 2026-10-29).
- 14. **Rejtett / hamis párhuzam** (a szerepmátrix szerint). A motívum *gerinc-kombinációi* a sorok `strong` mezőjének
  különböző értékei (pl. `H7121+H8034`, `G1941`). Legalább `KULCS_MIN_SOR` (3) soros kombinációnként a *kulcsszavak*: az e
  kombinációjú sorok `karoli_szo`-jának legalább felében álló szótári alakok, azok nélkül, amelyek a Károli–Strong
  párosításban a motívumverseken nem nyelvtani Strongra csak a kombinációtól idegenre párosulnak (pl. az *Úr* a H3068-ra:
  tárgy, nem a formula része; a nyelvtani pár — a *segítségül* a ב elöljáróra, H9003 — nem dönt). Egy szó a kulcsszóval
  egyezik, ha a szótári alakja azonos vele, vagy a szóalak (kisbetűvel) vagy a szótári alak vele kezdődik, és utána
  legfeljebb 3 betű áll — ez a szótárialak-tábla igealak-hiányait hidalja át (*hívni*, *hívám*, *hívák*, *híván*,
  *hívnám*). *Rejtett párhuzam* (ugyanaz a Strong, más magyar szó): motívumsor, amelynek `karoli_szo`-jából a saját
  kombinációjának valamely kulcsszava hiányzik. *Hamis párhuzam* (ugyanaz a magyar szó, a gerinc-kombináció nélkül): nem
  motívumsor Károli-vers, amelyben valamely kombináció minden kulcsszava áll, de egyik gerinc-kombináció sem teljes (a
  kombináció minden Strongja a versben); a versben álló gerinc-Strong (pl. a H7121 a H8034 nélkül) kiíródik. Ismert korlát:
  a 3 betűnél hosszabb toldalékú alak (*hívhatja*, Jób 27:10) nem egyezik a kulcsszóval.

TSV: split('\\t'), a '\\r' levágva; csv modul nélkül.
"""
import collections
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAROLI = os.path.join(GYOKER, 'konkordancia', 'Karoli_1908.tsv')
TAHOT = os.path.join(GYOKER, 'konkordancia', 'TAHOT_kivonat.tsv')
TAGNT = os.path.join(GYOKER, 'konkordancia', 'TAGNT_kivonat.tsv')
JELOLTEK = os.path.join(GYOKER, 'adat', 'jeloltek.tsv')
SZOTARI_ALAK = os.path.join(GYOKER, 'adat', 'szoto', 'karoli_szotari_alak.tsv')
PAROK = os.path.join(GYOKER, 'adat', 'karoli_strong')
GRAMMATIKAI = os.path.join(GYOKER, 'adat', 'grammatikai_strongok.tsv')
KAPCSOLOK = os.path.join(GYOKER, 'adat', 'funkcio_kapcsolok.tsv')


def funkcio_kapcsolok(ut=None):
    """[sor] az `adat/funkcio_kapcsolok.tsv`-ből (SEMA 2.44; `id`: `*` vagy motívum-id); hiányzó fájl: üres."""
    ut = ut or KAPCSOLOK
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n') if x.strip() and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def kapcsolo_motivumok(kapcsolo, ut=None):
    """Azok a motívum-id-k, amelyeken a kapcsoló `aktiv` (a motívumonként jóváhagyott funkció)."""
    return frozenset(r['id'] for r in funkcio_kapcsolok(ut) if r['kapcsolo'] == kapcsolo and r['id'] != '*'
                     and r.get('allapot') == 'aktiv')


def szpa_aktiv():
    """A SzPA-join (konkordáns alternatíva) állapota: igaz, ha a kapcsoló `aktiv` (vagy nincs sora)."""
    r = next((x for x in funkcio_kapcsolok() if x['kapcsolo'] == 'SZPA_JOIN' and x['id'] == '*'), None)
    return r is None or r.get('allapot') == 'aktiv'


NEVELO = frozenset({'a', 'az'})
KULCS_ARANY = 0.5
KULCS_MIN_SOR = 3
ELOTAG_MARADEK = 3  # a mérés: 3-nál az ISTENTISZT-001 hamis párhuzama 17 (+ hívnám), 4-nél a KIRALY-001-é 19 → 61
RESZLET_HATAR = 10
SZO = re.compile(r'[^\W\d_]+', re.UNICODE)

_CACHE = {}


def _sorok(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [x.rstrip('\r') for x in f.read().split('\n')]
    sorok = [x for x in sorok if x and not x.startswith('#')]
    return sorok[0].split('\t'), [x.split('\t') for x in sorok[1:]]


def szotari_alakok():
    """{alak: szótári alak (mai helyesírás, kisbetű)} a `karoli_szotari_alak.tsv`-ből."""
    if 'lemma' not in _CACHE:
        fej, sorok = _sorok(SZOTARI_ALAK)
        a, sz, m = fej.index('alak'), fej.index('szotari_alak'), fej.index('szotari_alak_mai')
        _CACHE['lemma'] = {r[a]: (r[m] or r[sz] or r[a]).lower() for r in sorok if len(r) > m}
    return _CACHE['lemma']


def lemma(szo, tabla=None):
    tabla = szotari_alakok() if tabla is None else tabla
    return tabla.get(szo) or tabla.get(szo.lower()) or szo.lower()


def szavak(szoveg):
    """A szöveg szavai, ahogy állnak, sorrendben (a '...' és az írásjel kimarad)."""
    return SZO.findall(szoveg or '')


def egyezik(szo, kulcs, tabla=None):
    """A szó a kulcsszóval egyezik: azonos szótári alak, vagy a szóalak (kisbetű) / a szótári alak a kulcsszóval kezdődik,
    és utána legfeljebb `ELOTAG_MARADEK` betű áll (*hívni*, *hívám*, *híván*, *hívnám* → *hív*; a *rendeléseit* nem
    *rend*)."""
    l = lemma(szo, tabla)
    if l == kulcs:
        return True
    return any(x.startswith(kulcs) and len(x) - len(kulcs) <= ELOTAG_MARADEK for x in (l, szo.lower()))


def _komb(sor):
    return frozenset(x for x in sor.get('strong', '').split('+') if x)


def gerinc_kombinaciok(sorai):
    """A sorok `strong` mezőjének különböző kombinációi (frozenset), pl. {G1941}, {H7121, H8034}."""
    return sorted({_komb(s) for s in sorai if s.get('strong')}, key=lambda k: sorted(k))


def karoli_megfelelok(sorai, tabla=None):
    """[(szótári alak, [szóalak, …], [igehely, …])] — igehelyenként egyszer; rendezés: gyakoriság (csökkenő), majd alak.
    A ritkább szótári alak beolvad a gyakoribb, legalább 3 betűs alakba, ha minden szóalakja azzal `egyezik` (a
    szótárialak-tábla igealak-hiányai: *hívni*, *hívá*, *hí* → *hív*; *istent* → *isten*)."""
    hely, alak = collections.OrderedDict(), collections.defaultdict(list)
    for s in sorai:
        for w in szavak(s.get('karoli_szo')):
            l = lemma(w, tabla)
            if l in NEVELO:
                continue
            if w not in alak[l]:
                alak[l].append(w)
            if s['igehely'] not in hely.setdefault(l, []):
                hely[l].append(s['igehely'])
    rend = sorted(hely, key=lambda l: (-len(hely[l]), l))
    for i in range(len(rend) - 1, -1, -1):
        l = rend[i]
        cel = next((c for c in rend[:i] if len(c) >= 3 and c in hely and c != l
                    and all(egyezik(w, c, tabla) for w in alak[l])), None)
        if cel:
            alak[cel].extend(w for w in alak[l] if w not in alak[cel])
            hely[cel].extend(h for h in hely[l] if h not in hely[cel])
            del hely[l]
    return sorted(((l, alak[l], sorted(h, key=vers_kulcs)) for l, h in hely.items()), key=lambda x: (-len(x[2]), x[0]))


def grammatikai_strongok():
    if 'gram' not in _CACHE:
        fej, sorok = _sorok(GRAMMATIKAI)
        i = fej.index('strong')
        _CACHE['gram'] = frozenset(r[i] for r in sorok if r)
    return _CACHE['gram']


def nyelvtani(strong):
    return strong in grammatikai_strongok() or bool(re.fullmatch(r'H9\d{3}', strong))


def _fajlnev(konyv):
    return ''.join(c for c in unicodedata.normalize('NFD', konyv) if not unicodedata.combining(c))


def parok(igehelyek):
    """{igehely: [(hu_szo, strong), …]} a `karoli_strong/parok_<könyv>.tsv`-ből (csak a megadott versek; a hiányzó
    könyvfájl üres eredményt ad — a párosítás javaslat-állapotú, nem teljes)."""
    konyvek = collections.defaultdict(set)
    for h in igehelyek:
        konyvek[h.rsplit(' ', 1)[0]].add(h)
    ki = collections.defaultdict(list)
    for konyv, helyek in konyvek.items():
        ut = os.path.join(PAROK, 'parok_%s.tsv' % _fajlnev(konyv))
        if not os.path.exists(ut):
            continue
        kulcs = ('parok', ut)
        if kulcs not in _CACHE:
            fej, sorok = _sorok(ut)
            v, hu, st = fej.index('vers'), fej.index('hu_szo'), fej.index('strong')
            d = collections.defaultdict(list)
            for r in sorok:
                if len(r) > st:
                    d[r[v]].append((r[hu], r[st]))
            _CACHE[kulcs] = d
        for h in helyek:
            ki[h] = _CACHE[kulcs].get(h, [])
    return ki


def kulcsszavak(sorai, arany=KULCS_ARANY, tabla=None, parositas=None):
    """{gerinc-kombináció: [kulcsszó, …]} — l. a modul docstringjét."""
    parositas = parok([s['igehely'] for s in sorai]) if parositas is None else parositas
    ki = collections.OrderedDict()
    for k in gerinc_kombinaciok(sorai):
        csop = [s for s in sorai if _komb(s) == k and szavak(s.get('karoli_szo'))]
        if len(csop) < KULCS_MIN_SOR:
            continue
        jo = []
        for l, _a, h in karoli_megfelelok(csop, tabla):
            if len(h) < arany * len(csop):
                continue
            # a nem nyelvtani párok döntenek: ha van ilyen, és egyik sem a kombináció Strongja, a szó a formulán kívüli
            par_st = [st for hely in h for hu, st in parositas.get(hely, [])
                      if lemma(hu, tabla) == l and not nyelvtani(st)]
            if par_st and not any(st in k for st in par_st):
                continue
            jo.append(l)
        ki[k] = jo
    return ki


def strongjai(sorai, szo):
    """A motívumsorok gerinc-Strongjai, amelyekre a Károli–Strong párosításban a `szo` (szótári alak) párosul."""
    tabla = szotari_alakok()
    par = parok([s['igehely'] for s in sorai])
    return {st for s in sorai for hu, st in par.get(s['igehely'], []) if st in _komb(s) and egyezik(hu, szo, tabla)}


HELYETTESITO_TILTOTT = {'az', 'egy', 'és', 'is', 'nem', 'te', 'ti', 'ő', 'ők', 'én', 'mi'}


def helyettesitok(sorai, helyek, kizart, kombonkent=None, strongok=None):
    """[(szótári alak, [igehely, …])]: a megadott motívumhelyeken mivel fordít a Károli a motívum szava helyett — a
    Károli–Strong párosításban a hely saját gerinc-Strongjaira párosuló szavak, ennek híján a `karoli_szo` szavai; a
    `kizart` kulcsszavakkal és a hely saját kombinációjának kulcsszavaival (`kombonkent`: {kombináció: [kulcsszó]})
    egyező szavak nélkül. Gyakoriság szerint (a felhasználó, 2026-10-30: „irjuk le azt is károli
    a motivom kulcsszavai helyet jellemzően mit forditott”)."""
    helyek = set(helyek)
    tabla = szotari_alakok()
    par = parok(sorted(helyek))
    gyujt = collections.OrderedDict()
    for s in sorai:
        h = s['igehely']
        if h not in helyek:
            continue
        k = _komb(s)
        cel = strongok if strongok else k  # `strongok`: csak az ezekre párosuló szavak (pl. a leggyakoribb szó Strongjai)
        szok = [hu for hu, st in par.get(h, []) if st in cel] or szavak(s.get('karoli_szo'))
        for w in szok:
            if any(egyezik(w, kw, tabla) for kw in list(kizart) + list((kombonkent or {}).get(k, []))):
                continue
            l = lemma(w, tabla)
            if len(l) < 2 or l in HELYETTESITO_TILTOTT:
                continue
            if h not in gyujt.setdefault(l, []):
                gyujt[l].append(h)
    # a ragozott maradék a rövidebb, legalább 3 betűs alakba olvad (*seolban* → *seol*, *alvilágnál* → *alvilág*)
    for l in sorted(gyujt, key=len, reverse=True):
        alap = next((m for m in gyujt if m != l and len(m) >= 3 and l.startswith(m)), None)
        if alap:
            gyujt[alap] += [h for h in gyujt.pop(l) if h not in gyujt[alap]]
    return sorted(gyujt.items(), key=lambda x: (-len(x[1]), x[0]))


def vers_strongok():
    """{igehely: Strong-halmaz} a TAHOT és a TAGNT soraiból (a kulcs a Károli-vers)."""
    if 'strong' not in _CACHE:
        d = collections.defaultdict(set)
        for ut in (TAHOT, TAGNT):
            fej, sorok = _sorok(ut)
            i, j = fej.index('Igehely'), fej.index('Strong-szám')
            for r in sorok:
                if len(r) > j:
                    d[r[i]].add(r[j])
        _CACHE['strong'] = d
    return _CACHE['strong']


def karoli_versek():
    """[(igehely, szöveg)] a Károli-fájl sorrendjében."""
    if 'karoli' not in _CACHE:
        _fej, sorok = _sorok(KAROLI)
        _CACHE['karoli'] = [(r[0], r[1]) for r in sorok if len(r) > 1]
    return _CACHE['karoli']


def vers_kulcs(hely):
    """Kanonikus rendezési kulcs: a vers helye a Károli-fájlban (a tartomány az első versével: `1Móz 14:18-20` →
    `1Móz 14:18`); az ismeretlen hely a végére, betűrendben."""
    if 'sorrend' not in _CACHE:
        _CACHE['sorrend'] = {h: i for i, (h, _sz) in enumerate(karoli_versek())}
    elso = re.sub(r'^(.+ \d+:\d+)-\d+$', r'\1', hely)
    return (_CACHE['sorrend'].get(elso, len(_CACHE['sorrend'])), hely)


def jelolt_dontesek(motivum_id):
    """{igehely: döntés} a `jeloltek.tsv` motívumsoraiból (az utolsó sor a mérvadó)."""
    fej, sorok = _sorok(JELOLTEK)
    i, h, d = fej.index('id'), fej.index('igehely'), fej.index('dontes')
    return {r[h]: r[d] for r in sorok if len(r) > d and r[i] == motivum_id}


def _hianyzo(szoveg, kulcsok, tabla=None):
    sz = szavak(szoveg)
    return [k for k in kulcsok if not any(egyezik(w, k, tabla) for w in sz)]


def rejtett_parhuzamok(sorai, tabla=None, kulcs=None):
    """[(igehely, karoli_szo, strong, [hiányzó kulcsszó, …])]: motívumsor, amelynek `karoli_szo`-jából a saját
    kombinációjának valamely kulcsszava hiányzik."""
    kulcs = kulcsszavak(sorai, tabla=tabla) if kulcs is None else kulcs
    ki = []
    for s in sorai:
        v = kulcs.get(_komb(s))
        if not v or not s.get('karoli_szo'):
            continue
        hiany = _hianyzo(s['karoli_szo'], v, tabla)
        if hiany:
            ki.append((s['igehely'], s['karoli_szo'], s.get('strong', ''), hiany))
    return sorted(ki, key=lambda x: vers_kulcs(x[0]))


def hamis_parhuzamok(sorai, versek=None, strongok=None, tabla=None, kulcs=None):
    """[(igehely, szöveg, [a versben álló gerinc-Strong, …])]: nem motívumsor Károli-vers, amelyben valamely kombináció
    minden kulcsszava áll, de egyik gerinc-kombináció sem teljes (a kombináció egy része állhat benne, pl. a H7121 a H8034
    nélkül)."""
    kulcs = kulcsszavak(sorai, tabla=tabla) if kulcs is None else kulcs
    kulcs = collections.OrderedDict((k, v) for k, v in kulcs.items() if v)
    if not kulcs:
        return []
    versek = karoli_versek() if versek is None else versek
    strongok = vers_strongok() if strongok is None else strongok
    sajat = {s['igehely'] for s in sorai}
    gerinc = set().union(*kulcs)
    ki = []
    for hely, szoveg in versek:
        if hely in sajat:
            continue
        st = strongok.get(hely, set())
        if any(not _hianyzo(szoveg, v, tabla) for v in kulcs.values()) and not any(k <= st for k in kulcs):
            ki.append((hely, szoveg, sorted(gerinc & st)))
    return ki


def _prov(scope, forras, n, ts):
    return '*(proveniencia: scope=%s | forras=%s | n=%d | ts=%s)*' % (scope, forras, n, ts)


def blokk_13(sorai, ts):
    """A 13. szerep bekezdései (lista); üres, ha a motívumsoroknak nincs `karoli_szo`-ja."""
    mid = sorai[0]['id'] if sorai else ''
    tetel = karoli_megfelelok(sorai)
    if not tetel:
        return []
    out = ['*A motívum igehelyeinek Károli-szóalakjai (`adat/elofordulasok.tsv`, `karoli_szo`), szótári alakonként '
           '(`adat/szoto/karoli_szotari_alak.tsv`, mai helyesírás), névelő nélkül: a szóalakok, és hány igehelyen, melyiken.*']
    out.append('\n'.join('- **%s** (%d) — %s: %s' % (l, len(h), ', '.join(a), ', '.join(h)) for l, a, h in tetel))
    if szpa_aktiv():
        out.append('*+SZPA (konkordáns alternatíva): jelölt hiány — a hiány nincs kitöltve.*')
    out.append(_prov('adat/elofordulasok.tsv (id=%s, karoli_szo)' % mid,
                     'adat/elofordulasok.tsv+adat/szoto/karoli_szotari_alak.tsv (eszkozok/szerep_karoli.py)',
                     sum(1 for s in sorai if s.get('karoli_szo')), ts))
    return out


def blokk_14(sorai, ts):
    """A 14. szerep bekezdései (lista); üres, ha nincs kulcsszó (nincs `karoli_szo` vagy `strong`)."""
    mid = sorai[0]['id'] if sorai else ''
    kulcs = collections.OrderedDict((k, v) for k, v in kulcsszavak(sorai).items() if v)
    if not kulcs:
        return []
    dontes = jelolt_dontesek(mid)
    kulcs_sz = '; '.join('%s: %s' % ('+'.join(sorted(k)), ', '.join('„%s”' % w for w in v)) for k, v in kulcs.items())
    out = ['*Kulcsszavak gerinc-kombinációnként: %s — az e kombinációjú motívumsorok Károli-szóalakjainak legalább felében '
           'álló szótári alak, a Károli–Strong párosításban csak idegen Strongra párosuló szavak nélkül. Csak megjelenítés: '
           'jelölt ezekből csak az `adat/jeloltek.tsv`-n át lesz.*' % kulcs_sz]
    rejt = rejtett_parhuzamok(sorai, kulcs=kulcs)
    out.append('**Rejtett párhuzam** (ugyanaz a Strong, más magyar szó): a motívum igehelyei, ahol a Károli a saját '
               'gerinc-kombinációjának valamely kulcsszavát nem használja — %d hely.' % len(rejt))
    if rejt:
        out.append('\n'.join('- %s — „%s” (%s; hiányzik: %s)' % (h, k, s, ', '.join(hi)) for h, k, s, hi in rejt))
    hamis = hamis_parhuzamok(sorai, kulcs=kulcs)
    out.append('**Hamis párhuzam** (ugyanaz a magyar szó, a gerinc-kombináció nélkül): Károli-versek valamely kombináció '
               'minden kulcsszavával, amelyekben egyik gerinc-kombináció sem teljes — %d vers. A versben álló gerinc-Strong '
               '(a kombináció egy része) a vers után áll; a magyar kulcsszavak mindkét szövetségben ugyanazt a '
               'kifejezést keresik.' % len(hamis))
    if hamis:
        sorok = '\n'.join('- %s — %s · *gerinc a versben: %s*%s' % (
            h, sz, ', '.join(g) if g else 'nincs', ' · *jelölt: %s*' % dontes[h] if h in dontes else '')
            for h, sz, g in hamis)
        out.append('<details>\n<summary>A %d vers</summary>\n\n%s\n\n</details>' % (len(hamis), sorok)
                   if len(hamis) > RESZLET_HATAR else sorok)
    out.append(_prov('Károli teljes (%s)' % kulcs_sz,
                     'Karoli_1908.tsv+TAHOT_kivonat.tsv+TAGNT_kivonat.tsv+adat/elofordulasok.tsv+adat/szoto/'
                     'karoli_szotari_alak.tsv+adat/karoli_strong (eszkozok/szerep_karoli.py)', len(hamis) + len(rejt), ts))
    return out
