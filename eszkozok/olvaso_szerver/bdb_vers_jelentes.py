"""bdb_vers_jelentes.py — F99 M2: a BDB igehely-hivatkozásai feloldva és jelentésponthoz kötve → adat/bdb_vers_jelentes.tsv.

Minden angol BDB-szócikk (konkordancia/BDB_teljes_unabridged.tsv) minden hivatkozására egy sor: a könyv feloldása (kiírt / örökölt /
vers-folytatás), az MT-vers, a Károli-vers (MT → Károli átkulcsolás), a jelentéspont (szakasz + törzs/jelentés/alpont, a szeletelő
csomópontjai szerint), okkóddal. A szabályok a DT-F99a döntése szerint (felhasználó, 2026-10-15):
  (1) a nem bibliai mű és a `^`-hoz tapadt kommentár-hely okkóddal kiszűrve (`szurt=1`, Károli-vers nélkül); a közeli sigla és a többértelmű
      könyvalak a táblában marad, `bizonytalan` jelöléssel (okkód); a nemi tanú („noun masculine^Gen 1:27”) bibliai hivatkozás;
  (2) MT → Károli: a Macula `karoli` oszlopa (konkordancia/Macula_heber_*.tsv), az F85-ben elvetett régiókban (naplok/F85_macula_elvetve.tsv)
      az azonos kulcs; a Károli-versmegfeleltetés MT-osztályú soraival ellenőrizve, ellentmondásnál `atkulcsolt_bizonytalan`;
  (3) a Károliban vagy az MT-ben nem létező vers a táblában marad, üres Károli-verssel és okkóddal, kitöltés nélkül;
  (4) egyfejezetes könyv fejezetszám nélkül („Obad 8”) az 1. fejezetre oldódik.

Használat (a repó gyökeréből):
  python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts 2026-10-15        # írja az adat/bdb_vers_jelentes.tsv-t
  python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts 2026-10-15 --ellenoriz   # újragenerál a memóriába, bájtra összeveti
  python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --minta 99                     # az M2 ⛔ vak munkalapja és kulcsa (naplok/)
  python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --minta 100                    # újramérés: naplok/BDB_SZELETELO_M2_minta_seed100_{vak,kulcs}.tsv
Azonos bemenettel és --ts-sel bájtra azonos. I/O: split('\\t') / '\\t'.join (csv modul nélkül).
"""
import argparse
import collections
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(D))
sys.path.insert(0, D)
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))

import bdb_szelet as B  # noqa: E402

BDB_EN = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
STRONG_SZOTAR = os.path.join(REPO, 'konkordancia', 'Strong_szotar.tsv')
OSHL_INDEX = os.path.join(REPO, 'konkordancia', 'OSHL_lexikalis_index.tsv')
VERSMEGF = os.path.join(REPO, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')
KAROLI = os.path.join(REPO, 'konkordancia', 'Karoli_1908.tsv')
F85_ELVETVE = os.path.join(REPO, 'naplok', 'F85_macula_elvetve.tsv')
KI = os.path.join(REPO, 'adat', 'bdb_vers_jelentes.tsv')
TAHOT = os.path.join(REPO, 'konkordancia', 'TAHOT_kivonat.tsv')
F85_ESETLISTA = os.path.join(REPO, 'naplok', 'F85_esetlista.tsv')
# DT-F99h (b) (felhasználó, 2026-10-15): a Károli-kulcs javítása csak a rendszeres eltolású fejezetekben, fejezetszintű eltolás-táblával,
# amelynek forrása az F85 dokumentált javítása. Az F85 esetlistája (naplok/F85_esetlista.tsv) minden eltolt TAHOT-versnél megadja a vers
# WLC (MT) megfelelőjét és a Károli-versét: ez az MT → Károli megfeleltetés (`eltolas` és `osszevonas_2_1` sor, WLC-illeszkedés J ≥ 0,5,
# egyértelmű). A régi TAHOT-kulcs (F85_kulcsvaltas.tsv `regi_kulcs`) nem MT-szám (a Dán 4-ben és a Hós 2-ben el is tér tőle), ezért nem az
# a forrás. A TAHOT-számok csak megerősítenek (mérés: naplok/BDB_SZELETELO_M0.md 9.13). Soronkénti ±3 verses keresés nincs.
# Az Ézs 3: az F85 a Macula `karoli` oszlopát itt elvetette (naplok/F85_macula_elvetve.tsv, 26 vers), de MT → Károli megfeleltetést nem
# rögzített; a Károli-szöveg szerint a Károli Ézs 3:1 az MT Ézs 2:22 (a Károli Ézs 2-ben 21, az Ézs 3-ban 27 vers), így MT 2:22 → K 3:1,
# MT 3:n → K 3:(n+1). A TAHOT a sorok 190/211-ében megerősíti. DT-F99n (felhasználó, 2026-10-16): az Ézs 3 eltolásának forrása a
# Károli-szöveg (Karoli_1908.tsv) és a TAHOT, nem az F85 esetlista; a sorok saját `vers_feloldas` értéket kapnak: `atkulcsolt_karoli_szoveg`.
EZS3 = {'Ézs 2:22': 'Ézs 3:1'}
EZS3.update({'Ézs 3:%d' % v: 'Ézs 3:%d' % (v + 1) for v in range(1, 27)})

# DT-F99i: a `szakasz` a címszó homonima-száma (vagy h:<váz>), a `resz` a szócikk római számos fő tagolása (üres, ha nincs)
FEJ = ['strong', 'bdb_id', 'sorszam', 'poz', 'nyers', 'konyv_feloldas', 'mt_vers', 'karoli_vers', 'vers_feloldas', 'szakasz', 'resz',
       'utvonal', 'okkod', 'szurt', 'proveniencia']
SZURENDO = {'nem_bibliai'}
# DT-F99k (felhasználó, 2026-10-15): a sigla melletti (tapadt, közeli vagy listás) hivatkozás akkor szűrődik, ha a TAHOT szerint a vers
# NEM tartalmazza a szócikk Strong-számát; ha tartalmazza, bibliai hivatkozás marad, okkód `sigla_igazolt`. A TAHOT `Igehely` kulcsa a
# Károli-vers (F85.6); Károli-vers híján az azonos számú vers.
SIGLA_OK = {'sigla_tapadt', 'sigla_kozel', 'sigla_lista'}
# F99 M2 (felhasználó, 2026-10-15, seed-100 M006, M064, M079): a BDB forrásszövegének hibás igehelye. A tábla a forrás szövegét rögzíti
# (könyv, vers, jelentéspont változatlan), az okkód `forras_hiba`; nem szűrt. Kulcs: (Strong, poz); érték: a forrással igazolt ok (kézi,
# a felhasználó döntése; a vak ellenőr megjegyzése a TAHOT-tal egyezik).
FORRAS_HIBA = {
    ('H5591', 422): 'Joel 1:4, 12 — a סַעַר a Jón 1:4, 12-ben áll (könyvnév-hiba a forrásban)',
    ('H7913', 185): 'Psa 9:8 — a שְׁכֵחֵי אֱלֹהִים a Zsolt 9:18-ban áll (számhiba a forrásban)',
    ('H3051', 2292): 'Ezra 7:4, 6 — a יְהִיב Pe`il-alak a Dán 7:4, 6-ban áll (könyvnév-hiba a forrásban)',
    # seed-101 (felhasználó, 2026-10-15): M049, M121
    ('H1802', 512): 'Exod 2:6 — a דָּלָה a 2Móz 2:16, 19-ben áll (számhiba a forrásban; TAHOT)',
    ('H7804', 532): 'Dan 3:13 — a שֵׁיזִב suffixumos alakja a Dán 3:15-ben áll (számhiba a forrásban; TAHOT)',
}
# DT381 (a) (felhasználó, 2026-10-28): a `bdb_forras_javitas.tsv` (2.31) `hivatkozas_kezi` sorai a forrás létező, de hibás versét
# javítják: a Strong `elofordulas`-adik olyan hivatkozása, amelynek fejezet:verse a `forras_alak`, a `javitott_alak` versére oldódik
# (a `nyers` a forrás alakja marad), okkód `forras_javitas`. A FORRAS_HIBA (fent) a hibát csak rögzíti, ez javít.
JAVITAS = os.path.join(REPO, 'adat', 'bdb_forras_javitas.tsv')


def kezi_hivatkozas_javitasok():
    """{strong: [(forras_alak, elofordulas, javitott_alak)]} a 2.31 `hivatkozas_kezi` soraiból."""
    ki = collections.defaultdict(list)
    for d in tsv_sorok(JAVITAS):
        if d['hiba'] == 'hivatkozas_kezi':
            ki[d['strong']].append((d['forras_alak'], int(d['elofordulas']), d['javitott_alak']))
    return ki


def hivatkozas_javit(strong, hiv, javitasok):
    """A `hivatkozas_kezi` javítások alkalmazása a Strong hivatkozásaira; hiányzó illesztésnél megáll."""
    for forras_alak, k, javitott in javitasok:
        talalt = [i for i, h in enumerate(hiv) if h['konyv'] and '%d:%d' % (h['c'], h['v']) == forras_alak]
        if len(talalt) < k:
            raise SystemExit('HIBA: a 2.31 hivatkozas_kezi sora nem illeszthető: %s %s (%d. előfordulás)' % (strong, forras_alak, k))
        c, v = (int(x) for x in javitott.split(':'))
        hiv[talalt[k - 1]] = dict(hiv[talalt[k - 1]], c=c, v=v, forras_javitas=True)
    return hiv


def fajl_hash(ut):
    """A fájl tartalmának sha256-ja LF-re normalizált szövegből (ELLENOR_F99 3.: a repó core.autocrlf=true-val megy, a `*.py` munkafa-
    példánya platformonként CRLF vagy LF; a hash így checkouttól függetlenül azonos)."""
    with open(ut, 'rb') as f:
        adat = f.read()
    return hashlib.sha256(adat.replace(b'\r\n', b'\n')).hexdigest()[:12]


def fajlok_hash(utak):
    """Több fájl együttes hash-e (a fájlnevek sorrendjében, LF-re normalizálva)."""
    h = hashlib.sha256()
    for ut in sorted(utak):
        h.update(os.path.basename(ut).encode('utf-8') + b'\0' + fajl_hash(ut).encode('ascii') + b'\n')
    return h.hexdigest()[:12]


# ELLENOR_F99 4.: a kód-hash a tábla előállításában részt vevő minden kódot fed
KOD_FAJLOK = [os.path.join(D, 'bdb_szelet.py'), os.path.abspath(__file__), os.path.join(REPO, 'eszkozok', 'bdb_konyv_javit.py'),
              os.path.join(REPO, 'eszkozok', 'normalizal.py')]


def macula_fajlok():
    k = os.path.join(REPO, 'konkordancia')
    return [os.path.join(k, f) for f in sorted(os.listdir(k)) if f.startswith('Macula_heber_') and f.endswith('.tsv')]


def tsv_sorok(ut):
    fej, ki = None, []
    with open(ut, encoding='utf-8', newline='') as f:
        for sor in f:
            if sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            ki.append(dict(zip(fej, m)))
    return ki


def betolt():
    en = {d['Strong_padded']: d['Teljes_szocikk'] for d in tsv_sorok(BDB_EN)}
    lem = {}
    with open(STRONG_SZOTAR, encoding='utf-8', newline='') as f:
        for i, sor in enumerate(f):
            if i == 0 or sor.startswith('#'):
                continue
            m = sor.rstrip('\n').split('\t')
            if len(m) > 1:
                lem.setdefault(m[0], m[1])
    bdb_id = collections.defaultdict(list)
    for d in tsv_sorok(OSHL_INDEX):
        if d['strong'] != '—' and d['bdb_id'] != '—' and d['bdb_id'] not in bdb_id[d['strong']]:
            bdb_id[d['strong']].append(d['bdb_id'])
    vm_karoli, vm_mt = set(), {}
    for d in tsv_sorok(KAROLI):
        vm_karoli.add(d['Igehely'])
    for d in tsv_sorok(VERSMEGF):
        if d['igehely_mt']:
            k = d['igehely_karoli'].rsplit(' ', 1)[0]
            vm_mt['%s %s' % (k, d['igehely_mt'])] = d['igehely_karoli']
    elvetett = set()
    for d in tsv_sorok(F85_ELVETVE):
        elvetett.add((d['konyv'], int(d['fejezet'])))
    f85 = collections.defaultdict(set)
    for d in tsv_sorok(F85_ESETLISTA):
        m = re.search(r'WLC=(\S+ \d+:\d+) J=([\d.]+)', d.get('igazolas', ''))
        if m and d['tipus'] in ('eltolas', 'osszevonas_2_1') and float(m.group(2)) >= 0.5:
            f85[m.group(1)].add(d['karoli_vers'])
    f85 = {k: next(iter(v)) for k, v in f85.items() if len(v) == 1}
    tahot = collections.defaultdict(set)
    for d in tsv_sorok(TAHOT):
        m = re.match(r'^H0*(\d+)', d.get('Strong-szám', ''))
        if m:
            tahot[d['Igehely']].add(int(m.group(1)))
    return en, lem, bdb_id, vm_karoli, vm_mt, elvetett, tahot, f85


# A Károli-szöveg (Karoli_1908.tsv) és a versmegfeleltetés a Siralmakat „Sir”-nek írja, a könyvalak-tábla (LEK) „JSir”-nek: a Károli-vers
# a Karoli_1908 kulcsa (link a szerverre), az MT-vers a LEK alakja.
KAROLI_KONYV = {'JSir': 'Sir'}


def mt_karoli(K, versek, mt2k, vm_karoli, vm_mt, elvetett, konyv, c, v):
    """-> (mt_vers, karoli_vers, vers_feloldas, okkod_kieg)"""
    mt = '%s %d:%d' % (konyv, c, v)
    kk = KAROLI_KONYV.get(konyv, konyv)
    if v not in versek.get(konyv, {}).get(c, ()):
        return mt, '', 'nem_letezo_vers', 'nem_letezo_vers'
    if (konyv, c) in elvetett:
        kar = {(kk, c, v)}
        mod = 'azonos_f85'
    else:
        kar = set(mt2k.get((konyv, c, v), set()))
        mod = None
    if not kar:
        return mt, '', 'nincs_karoli', 'nincs_karoli'
    jel = sorted(kar, key=lambda x: (x[1], x[2]))
    karoli = '%s %d:%d' % jel[0]
    kieg = 'tobb_karoli_vers' if len(jel) > 1 else ''
    if mod is None:
        mod = 'azonos' if karoli == '%s %d:%d' % (kk, c, v) else 'atkulcsolt'
    mtk = '%s %d:%d' % (kk, c, v)
    if mtk in vm_mt and vm_mt[mtk] != karoli:
        mod = 'atkulcsolt_bizonytalan'
    if karoli not in vm_karoli:
        return mt, '', 'nincs_karoli', 'karoli_vers_nem_letezik'
    return mt, karoli, mod, kieg


def general(ts, strongok=None):
    """A tábla sorai (és a kód-hash); `strongok`: csak ezek a szócikkek (tesztekhez)."""
    K = B._konyvtabla()
    en, lem, bdb_id, vm_karoli, vm_mt, elvetett, tahot, f85 = betolt()
    versek, _, mt2k = K.macula_betolt()
    osz = set(K.OSZ)
    modhash = '+'.join(fajl_hash(u) for u in KOD_FAJLOK)
    javitasok = kezi_hivatkozas_javitasok()
    sorok = []
    for strong in sorted(strongok if strongok is not None else en):
        szoveg = en[strong]
        r = B.szeletel(szoveg, lem.get(strong, ''))
        savok = B.csomopont_savok(szoveg, r)
        # a szakaszok sávja: a csomópontokon kívüli hivatkozás a saját szakaszának „fej”-e, vagy „tagolatlan”, ha a szakaszban nincs
        # törzs, számozott jelentés vagy alpont (F99 M2 újramérés előtt: a szakasz a kulcs része)
        szsav = B.szakasz_savok(szoveg, r)
        # DT-F99g (felhasználó, 2026-10-15): a kód-hash csak a fájl fejlécében áll; a sor a forrásra és a generátorra hivatkozik
        prov = 'scope=%s | forras=bdb_vers_jelentes.py (fejléc) | ts=%s' % (strong, ts)
        for n, h in enumerate(hivatkozas_javit(strong, B.hivatkozasok(szoveg), javitasok.get(strong, [])), 1):
            cimke, ut = B.jelentespont(h['poz'], savok, szsav)
            szak, resz = B.szakasz_bont(cimke)
            if ut == '-/-':
                tag = next((t for a, b, c, t in szsav if a <= h['poz'] < b), True)
                ut = 'fej' if tag else 'tagolatlan'
            ok = h['okkod']
            mt = kar = ''
            vmod = ''
            kmod = h['konyv_mod']
            if (h['konyv'] and kmod in ('orokolt', 'folytatas') and h['konyv'] in osz and ok not in SZURENDO
                    and h['c'] not in versek.get(h['konyv'], {})):
                # F99 M2 (felhasználó, 2026-10-15, seed-100 M013 „Malachi 3:20 … 143:1”): nem létező fejezetre a könyv nem öröklődik;
                # a sor bizonytalan (`orokles_hibas`), könyv és vers nélkül
                h = dict(h, konyv=None)
                ok = 'orokles_hibas'
                kmod = 'feloldhatatlan'
            if (strong, h['poz']) in FORRAS_HIBA:
                ok = ok + ',forras_hiba' if ok else 'forras_hiba'
            if h.get('forras_javitas'):
                ok = ok + ',forras_javitas' if ok else 'forras_javitas'
            szurt = h['okkod'] in SZURENDO
            if h['konyv'] and not szurt:
                if h['konyv'] in osz:
                    mt, kar, vmod, kieg = mt_karoli(K, versek, mt2k, vm_karoli, vm_mt, elvetett, h['konyv'], h['c'], h['v'])
                    n_st = int(re.match(r'^H0*(\d+)', strong).group(1))
                    if mt in f85 or mt in EZS3:
                        # DT-F99h (b): az F85 eltolás-táblája (esetlista: WLC → Károli); DT-F99n: az Ézs 3 a Károli-szöveg és a TAHOT szerint
                        if mt in f85:
                            kar, vmod = f85[mt], 'atkulcsolt_f85'
                        else:
                            kar, vmod = EZS3[mt], 'atkulcsolt_karoli_szoveg'
                        kieg = ','.join(x for x in kieg.split(',') if x not in ('nincs_karoli', 'karoli_vers_nem_letezik', 'tobb_karoli_vers'))
                    elif 'nincs_karoli' in kieg.split(',') or 'karoli_vers_nem_letezik' in kieg.split(','):
                        # DT-F99h kiegészítés: az azonos számú Károli-vers, ha a TAHOT ott hordozza a szót
                        azon = '%s %d:%d' % (KAROLI_KONYV.get(h['konyv'], h['konyv']), h['c'], h['v'])
                        if azon in vm_karoli and n_st in tahot.get(azon, ()):
                            kar, vmod = azon, 'azonos_tahot'
                            kieg = ','.join(['karoli_tahot'] + [x for x in kieg.split(',') if x and x not in ('nincs_karoli', 'karoli_vers_nem_letezik')])
                    if kieg:
                        ok = ok + ',' + kieg if ok else kieg
                else:
                    mt, vmod = '%s %d:%d' % (h['konyv'], h['c'], h['v']), 'usz'
                    ok = ok + ',usz' if ok else 'usz'
            if h['okkod'] in SIGLA_OK and ok.split(',')[0] in SIGLA_OK:
                # DT-F99k: a TAHOT dönt (a Károli-versen, annak híján az azonos számú versen)
                kulcs = kar or ('%s %d:%d' % (KAROLI_KONYV.get(h['konyv'], h['konyv']), h['c'], h['v']) if h['konyv'] else '')
                n_st = int(re.match(r'^H0*(\d+)', strong).group(1))
                if kulcs and n_st in tahot.get(kulcs, ()):
                    ok = ','.join(['sigla_igazolt'] + ok.split(',')[1:])
                else:
                    szurt = True
                    mt = kar = vmod = ''
                    ok = h['okkod']
            sorok.append([strong, ','.join(bdb_id.get(strong, [])), str(n), str(h['poz']), h['nyers'], kmod, mt, kar, vmod,
                          szak, resz, ut, ok, '1' if szurt else '0', prov])
    return sorok, modhash


def kiir(sorok, modhash, ts):
    fej = ['# GENERÁLT: eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts %s — kézzel nem szerkesztendő (F99 M2; séma: adat/SEMA.md 2.29).' % ts,
           '# forras: konkordancia/BDB_teljes_unabridged.tsv@%s + Macula_heber_*.tsv (%d fájl)@%s (MT-versek, MT→Károli) + '
           'Karoli_versmegfeleltetes.tsv@%s + Karoli_1908.tsv@%s (Károli-versek; az Ézs 3 eltolásának forrása is, DT179) + naplok/F85_macula_elvetve.tsv@%s + naplok/F85_esetlista.tsv@%s '
           '(DT173) + OSHL_lexikalis_index.tsv@%s (bdb_id) + Strong_szotar.tsv@%s (lemma) + TAHOT_kivonat.tsv@%s (DT173, DT176; az Ézs 3 eltolásának megerősítése, DT179) + '
           'adat/bdb_forras_javitas.tsv@%s (a hivatkozas_kezi sorok, DT381 (a)); '
           'kód: bdb_szelet.py+bdb_vers_jelentes.py+bdb_konyv_javit.py+normalizal.py@%s (LF-re normalizált tartalom; DT172: a kód-hash csak itt áll, a sorok proveniencia-mezője erre a fejlécre hivatkozik); szabály: DT166, DT173, DT174, DT175, DT176, DT179'
           % (fajl_hash(BDB_EN), len(macula_fajlok()), fajlok_hash(macula_fajlok()), fajl_hash(VERSMEGF), fajl_hash(KAROLI), fajl_hash(F85_ELVETVE),
              fajl_hash(F85_ESETLISTA), fajl_hash(OSHL_INDEX), fajl_hash(STRONG_SZOTAR), fajl_hash(TAHOT), fajl_hash(JAVITAS), modhash),
           '\t'.join(FEJ)]
    for s in sorok:
        for x in s:
            if '\t' in x or '\n' in x:
                raise SystemExit('HIBA: tab vagy sortörés a mezőben: %r' % s)
    return '\n'.join(fej + ['\t'.join(s) for s in sorok]) + '\n'


def minta(seed, n, kieg, vak_ut, kulcs_ut):
    """Az M2 ⛔ minta-ellenőrzésének két fájlja (a felhasználó döntése, 2026-10-15; naplok/BDB_SZELETELO_M0.md 9.4):
    (a) VAK munkalap a független ellenőrnek: a hivatkozás azonosítója, a Strong, a nyers hivatkozás és a környezete a szócikk szövegéből,
        üres kitöltendő oszlopokkal — semmi a szeletelő feloldásából (könyv, vers, jelentéspont, szűrés, réteg);
    (b) KULCS: ugyanazok az azonosítók a szeletelő kimenetével és a réteggel (az ellenőrnek nem adjuk).
    A minta: `n` egyszerű véletlen sor a teljes táblából (random.Random(seed)), és rétegenként `kieg` sor a kiszűrt (szurt=1) és a bizonytalan
    (sigla_kozel, tobbertelmu) hivatkozásokból; a sorrend a seeddel megkeverve (a réteg a vak lapon nem látszik). Csak olvas."""
    import random
    fej, sorok = None, []
    with open(KI, encoding='utf-8', newline='') as f:
        for s in f:
            if s.startswith('#'):
                continue
            m = s.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            sorok.append(dict(zip(fej, m)))
    rnd = random.Random(seed)
    valasztott = [('veletlen', s) for s in rnd.sample(sorok, n)]
    marad = [s for s in sorok if not any(s is x for _, x in valasztott)]
    for nev, felt in (('szurt', lambda s: s['szurt'] == '1'),
                      ('bizonytalan', lambda s: any(o in s['okkod'].split(',') for o in ('sigla_kozel', 'tobbertelmu', 'orokles_hibas', 'sigla_igazolt')))):
        pool = [s for s in marad if felt(s)]  # noqa
        valasztott += [(nev, s) for s in rnd.sample(pool, min(kieg, len(pool)))]
    rnd.shuffle(valasztott)
    en = {d['Strong_padded']: d['Teljes_szocikk'] for d in tsv_sorok(BDB_EN)}
    vak = ['# M2 ⛔ VAK munkalap (F99): seed=%d; %d sor. Forrás: a BDB angol szócikke (konkordancia/BDB_teljes_unabridged.tsv, a Strong sora).' % (seed, len(valasztott)),
           '# Kitöltendő soronként, a szócikk TELJES szövegéből (a környezet csak tájékoztat; a könyv a szócikkben korábban állhat): '
           'konyv_mt = a hivatkozott hely könyve és MT fejezet:verse (pl. „1Móz 32:1”; egyfejezetes könyvnél 1. fejezet), ha bibliai hely; '
           'karoli_vers = a Károli-szám, ha eltér (különben „=”); jelentespont = a BDB tagolása szerinti hely (római szakasz, törzs, jelentés, alpont, '
           'pl. „II Qal/2/a”, „-/1/b”), vagy „fej” (címsor, nyelvi háttér, alaktan), vagy „tagolatlan” (a szócikknek nincs törzse, számozott jelentése, alpontja); '
           'szures = „bibliai” vagy „alhivatkozas: <ok>” (pl. kommentár-hely, nem bibliai mű) vagy „bizonytalan: <ok>”.',
           '# A RÓMAI SZAKASZ a jelentéspont része (a felhasználó döntése, 2026-10-15): (1) ha a forrás a címszó előtt római számot ír („H3499. yether '
           'I. יֶ֫תֶר noun …”, „II. [יָאַל] verb …”), azt a FŐ címszónál is írd („I fej”, „II Hiph`il”); (2) a szócikk római számos fő tagolását '
           '(„I. of man: 1 … II. of God: 1 …”, „I. preposition … II. conjunction …”) a KÜLÖN `resz` oszlopba írd (csak a római számot, pl. „II”), '
           'NEM a jelentéspontba (DT-F99i: két római szint, két mező; pl. „ad III. עַד … I. preposition … 3 …” → jelentespont „III -/3”, resz „I”); '
           'igénél a tagolás a törzsön belüli, a rákövetkező törzs (pl. Niph`al) már nem tartozik a tagoláshoz (resz üres); (3) római számot csak a forrásban kiírtat írj, következtetettet ne; (4) a '
           'jelöletlen második címszó (római szám nélkül) szakaszát római szám nélkül, a saját törzs/jelentés útvonalával írd. Az összevetés csak a „`” és az '
           '„\'” különbségét, és a „fej” = „tagolatlan” = „<törzs>” (= „<törzs>/-”) egyenértékűséget normálja; a zárójeles szint („(2)”, „(c)”) külön mutató.',
           '# A poz a hivatkozás kezdete a szöveg „lapított” alakjában (sortörés helyett szóköz; „1.a” → „1. a.”), csak a megtaláláshoz.',
           '\t'.join(['azon', 'strong', 'poz', 'nyers', 'kornyezet', 'konyv_mt', 'karoli_vers', 'jelentespont', 'resz', 'szures', 'megjegyzes'])]
    kulcs = ['# M2 ⛔ KULCS (F99): seed=%d; a szeletelő kimenete (adat/bdb_vers_jelentes.tsv) a vak munkalap azonosítóival. Az ellenőrnek NEM adandó.' % seed,
             '\t'.join(['azon', 'reteg', 'strong', 'sorszam', 'poz', 'nyers', 'konyv_feloldas', 'mt_vers', 'karoli_vers', 'vers_feloldas',
                        'szakasz', 'resz', 'utvonal', 'okkod', 'szurt'])]
    for k, (reteg, s) in enumerate(valasztott, 1):
        azon = 'M%03d' % k
        flat = B.lapit(en[s['strong']])
        p = int(s['poz'])
        hossz = len(s['nyers']) if flat[p:p + len(s['nyers'])] == s['nyers'] else len(s['nyers'].lstrip(', '))
        korny = flat[max(0, p - 100):p] + '⟦' + flat[p:p + hossz] + '⟧' + flat[p + hossz:p + hossz + 100]
        vak.append('\t'.join([azon, s['strong'], s['poz'], s['nyers'], korny.replace('\t', ' '), '', '', '', '', '', '']))
        kulcs.append('\t'.join([azon, reteg, s['strong'], s['sorszam'], s['poz'], s['nyers'], s['konyv_feloldas'], s['mt_vers'], s['karoli_vers'],
                                s['vers_feloldas'], s['szakasz'], s['resz'], s['utvonal'], s['okkod'], s['szurt']]))
    for ut, ki in ((vak_ut, vak), (kulcs_ut, kulcs)):
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(ki) + '\n')
    print('vak munkalap: %s; kulcs: %s (%d sor; réteg: %s)' % (vak_ut, kulcs_ut, len(valasztott),
                                                               dict(collections.Counter(r for r, _ in valasztott))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--minta', type=int, metavar='SEED', help='az M2 ⛔ vak munkalapja és kulcsa (nem írja a táblát)')
    ap.add_argument('--minta-n', type=int, default=200)
    ap.add_argument('--minta-kieg', type=int, default=25)
    # a 99-es seed a régi neveken; minden más seed saját fájlpárt kap (…_minta_seed<N>_vak.tsv / _kulcs.tsv), a korábbi minta nem íródik felül
    ap.add_argument('--minta-vak', default=None)
    ap.add_argument('--minta-kulcs', default=None)
    ap.add_argument('--ts', help='a proveniencia ts mezője (a futás napja); azonos ts-sel bájtra azonos a kimenet')
    ap.add_argument('--ellenoriz', action='store_true', help='nem ír: újragenerál és összeveti a meglévő táblával')
    a = ap.parse_args()
    if a.minta is not None:
        alap = 'BDB_SZELETELO_M2_minta' if a.minta == 99 else 'BDB_SZELETELO_M2_minta_seed%d' % a.minta
        minta(a.minta, a.minta_n, a.minta_kieg, a.minta_vak or os.path.join(REPO, 'naplok', alap + '_vak.tsv'),
              a.minta_kulcs or os.path.join(REPO, 'naplok', alap + '_kulcs.tsv'))
        return
    if not a.ts:
        ap.error('--ts kell')
    sorok, modhash = general(a.ts)
    szoveg = kiir(sorok, modhash, a.ts)
    if a.ellenoriz:
        regi = open(KI, encoding='utf-8', newline='').read() if os.path.exists(KI) else ''
        print('bájtra azonos' if regi == szoveg else 'ELTÉR')
        sys.exit(0 if regi == szoveg else 1)
    with open(KI, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    c = collections.Counter()
    i = {k: n for n, k in enumerate(FEJ)}
    for s in sorok:
        c['sor'] += 1
        c['szurt=' + s[i['szurt']]] += 1
        c['konyv:' + s[i['konyv_feloldas']]] += 1
        c['vers:' + (s[i['vers_feloldas']] or '—')] += 1
        c['karoli_vers_van' if s[i['karoli_vers']] else 'karoli_vers_nincs'] += 1
        c['jelentespont:' + (s[i['utvonal']] if s[i['utvonal']] in ('fej', 'tagolatlan') else 'csomopont')] += 1
        if s[i['resz']]:
            c['resz:van'] += 1
        for o in s[i['okkod']].split(','):
            if o:
                c['okkod:' + o] += 1
    for k in sorted(c):
        print('%s\t%d' % (k, c[k]))


if __name__ == '__main__':
    main()
