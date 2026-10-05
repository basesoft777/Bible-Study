"""Olvasói pilot (prototípus, nem éles): az 1Móz 1:1–2:3 vers- és szó-lapjainak adata a repó tábláiból.

Csak olvas. Kimenet: olvaso_pilot.json a --kimenet könyvtárba (alapból a repón kívüli ideiglenes
könyvtárba, CLAUDE.md: a próbák kimenete nem kerül a repóba). Minden érték forrássorból jön;
a gépi feldolgozás (BDB-bontás, fő szó választása, görög szóalak párosítása) szabálya itt olvasható.
Futtatás: python eszkozok/olvaso_pilot/adat.py [--kimenet KÖNYVTÁR], utána epit.py."""
import argparse
import json
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bdb_szelet import szeletel  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/') + '/'
_ap = argparse.ArgumentParser(description='Olvasói pilot: adatkinyerés')
_ap.add_argument('--kimenet', default=os.path.join(tempfile.gettempdir(), 'olvaso_pilot'))
_args = _ap.parse_args()
os.makedirs(_args.kimenet, exist_ok=True)
KI = os.path.join(_args.kimenet, 'olvaso_pilot.json')
VERSEK = ['1Móz 1:%d' % v for v in range(1, 32)] + ['1Móz 2:%d' % v for v in range(1, 4)]
TS = '2026-10-05'


def sorok(ut, fejlec=True):
    with open(GY + ut, encoding='utf-8') as fh:
        elso = True
        for s in fh:
            s = s.rstrip('\r\n')
            if not s or s.startswith('#'):
                continue
            if fejlec and elso:
                elso = False
                continue
            yield s.split('\t')


def hnorm(s):
    s = s.strip().upper()
    m = re.match(r'^([HG])0*(\d+)([A-Z]?)$', s)
    if not m:
        return None
    return '%s%04d' % (m.group(1), int(m.group(2)))


# --- nyelvtani Strong-számok (nem kapnak szó-lapot)
nyelvtani = set()
for r in sorok('adat/grammatikai_strongok.tsv'):
    n = hnorm(r[0]) if r else None
    if n:
        nyelvtani.add(n)

# --- Károli-szöveg
karoli = {r[0]: r[1] for r in sorok('konkordancia/Karoli_1908.tsv') if len(r) > 1}

# --- TAHOT: versenkénti szavak és Strong-gyakoriság
tahot_vers = defaultdict(list)
tahot_db = Counter()
tahot_konyvek = defaultdict(set)
tahot_lemma = {}
for r in sorok('konkordancia/TAHOT_kivonat.tsv'):
    if len(r) < 7:
        continue
    n = hnorm(r[1])
    if r[0] in VERSEK:
        tahot_vers[r[0]].append({'strong': n or r[1], 'heber': r[2], 'atiras': r[3],
                                 'szoto': r[4], 'jelentes': r[5], 'tukor': r[6]})
    if n:
        tahot_db[n] += 1
        tahot_konyvek[n].add(r[0].split(' ')[0])
        tahot_lemma.setdefault(n, (r[4], r[3], r[5]))

# --- Strong-szótár (szótő, kiejtés, jelentés; görög lemmához is)
strong_szotar = {}
for r in sorok('konkordancia/Strong_szotar.tsv'):
    n = hnorm(r[0]) if r else None
    if n and len(r) >= 6:
        strong_szotar[n] = {'szoto': r[1], 'kiejtes': r[2], 'szofaj': r[3], 'jelentes': r[5]}

# --- Károli–Strong párok: a pilot versei és a teljes összesítés
parok_vers = defaultdict(list)
karoli_alak = defaultdict(Counter)
karoli_alak_magas = defaultdict(Counter)
karoli_konyv = defaultdict(set)
pkonyvek = []
for f in sorted(os.listdir(GY + 'adat/karoli_strong')):
    if not f.startswith('parok_'):
        continue
    pkonyvek.append(f[6:-4])
    for r in sorok('adat/karoli_strong/' + f):
        if len(r) < 7:
            continue
        n = hnorm(r[5])
        if r[0] in VERSEK:
            parok_vers[r[0]].append({'hu_sorszam': r[1], 'hu_szo': r[2], 'er_sorszam': r[3],
                                     'strong': n, 'bizonyossag': r[6]})
        if n and n not in nyelvtani:
            alak = re.sub(r'[^\wáéíóöőúüűÁÉÍÓÖŐÚÜŰ-]', '', r[2]).lower()
            if alak:
                karoli_alak[n][alak] += 1
                if r[6] == 'magas':
                    karoli_alak_magas[n][alak] += 1
                karoli_konyv[n].add(r[0].split(' ')[0])

# --- BDB: magyar fordítás és angol eredeti
bdb_hu = {}
for r in sorok('adat/forditasok.tsv'):
    if len(r) > 7 and r[0] == 'BDB' and r[6].strip():
        n = hnorm(r[1])
        if n:
            bdb_hu[n] = {'szoveg': r[6].replace('\\n', '\n'), 'allapot': r[7], 'modell': r[8], 'datum': r[9]}
bdb_en = {}
for r in sorok('konkordancia/BDB_teljes_unabridged.tsv'):
    n = hnorm(r[0]) if r else None
    if n and len(r) > 2:
        bdb_en[n] = r[2]

# --- LXX_OS a pilot verseire
lxx_vers = defaultdict(list)
for r in sorok('konkordancia/LXX_OS/genesis.tsv'):
    if len(r) > 10 and r[2] in VERSEK:
        g = ('G%04d' % int(r[9])) if r[9].isdigit() else ''
        lxx_vers[r[2]].append((int(r[4]) if r[4].isdigit() else 0,
                               {'szoalak': r[5], 'lemma': r[7], 'strong': g, 'morf': r[8]}))

# --- lxx_bridge
bridge = defaultdict(list)
for r in sorok('adat/kulso/lxx_bridge.tsv'):
    n = hnorm(r[0])
    if n and len(r) > 2:
        bridge[n].append((int(r[2]), hnorm(r[1])))

# --- kereszthivatkozások
tsk = defaultdict(list)
for r in sorok('konkordancia/TSK_kereszthivatkozasok.tsv'):
    if len(r) > 3 and r[0] in VERSEK:
        tsk[r[0]].append((int(r[3]) if r[3].lstrip('-').isdigit() else 0, r[2]))
kh = defaultdict(list)
for r in sorok('konkordancia/Karoli_kereszthivatkozasok.tsv'):
    m = re.match(r'^Gen\.(\d+)\.(\d+)$', r[0]) if r else None
    if m and len(r) > 2 and ('1Móz %s:%s' % (m.group(1), m.group(2))) in VERSEK:
        kh['1Móz %s:%s' % (m.group(1), m.group(2))].append(r[2])


FUNKCIO = ('elöljárószó', 'kötőszó', 'partikula', 'névmás', 'indulatszó')


def funkcioszo(strong):
    """Funkciószó-e a Strong-szótár szófaja szerint (elöljáró, kötőszó, partikula, névmás …)."""
    sz = strong_szotar.get(strong, {}).get('szofaj', '')
    return any(f in sz for f in FUNKCIO)


def tokenek(szoveg):
    return [t for t in szoveg.split(' ') if t]


versek = []
szavak = set()
for v in VERSEK:
    hu = tokenek(karoli.get(v, ''))
    terkep = defaultdict(list)
    for p in parok_vers[v]:
        if p['hu_sorszam'].isdigit() and p['strong']:
            terkep[int(p['hu_sorszam'])].append({'strong': p['strong'], 'biz': p['bizonyossag']})
    hu_szavak = []
    for i, t in enumerate(hu, 1):
        kotes = terkep.get(i, [])
        # ha egy Károli-szó több héber szót ad vissza (pl. „világosságot” = בֵּין + אוֹר), a fő szó:
        # előbb a magas bizonyosságú, azon belül a tartalmas szófajú (nem elöljáró/kötőszó/partikula/névmás)
        fo = [k for k in kotes if k['strong'] not in nyelvtani]
        fo.sort(key=lambda k: (k['biz'] != 'magas', funkcioszo(k['strong'])))
        hu_szavak.append({'szo': t, 'strongok': [k['strong'] for k in kotes],
                          'fo': fo[0]['strong'] if fo else None,
                          'tobbi': [{'strong': k['strong'], 'biz': k['biz']} for k in fo[1:]],
                          'biz': fo[0]['biz'] if fo else (kotes[0]['biz'] if kotes else None)})
    for w in tahot_vers[v]:
        if w['strong'] and w['strong'] not in nyelvtani:
            szavak.add(w['strong'])
        w['nyelvtani'] = w['strong'] in nyelvtani
    versek.append({
        'igehely': v,
        'karoli': karoli.get(v, ''),
        'hu_szavak': hu_szavak,
        'heber': tahot_vers[v],
        'lxx': [x for _, x in sorted(lxx_vers[v], key=lambda t: t[0])],
        'tsk': [h for _, h in sorted(tsk[v], key=lambda t: -t[0])][:6],
        'tsk_db': len(tsk[v]),
        'karoli_kh': kh[v][:8],
    })

lapok = {}
for s in sorted(szavak):
    sz = strong_szotar.get(s, {})
    lem = tahot_lemma.get(s, ('', '', ''))
    hu = bdb_hu.get(s)
    en = bdb_en.get(s, '')
    lapok[s] = {
        'strong': s,
        'lemma': sz.get('szoto') or lem[0],
        'kiejtes': sz.get('kiejtes') or lem[1],
        'szofaj': sz.get('szofaj', ''),
        'rovid': sz.get('jelentes') or lem[2],
        'bdb_hu': hu['szoveg'] if hu else None,
        'bdb_hu_meta': ('%s, %s' % (hu['modell'], hu['datum'])) if hu else None,
        'bdb_en': en if not hu else None,
        'appar': szeletel(hu['szoveg'] if hu else en),
        'karoli': karoli_alak[s].most_common(8),
        'karoli_magas': sum(karoli_alak_magas[s].values()),
        'karoli_osszes': sum(karoli_alak[s].values()),
        'karoli_konyvek': sorted(karoli_konyv[s]),
        'elofordulas': tahot_db.get(s, 0),
        'konyvek_szama': len(tahot_konyvek.get(s, ())),
        'lxx': [{'strong': g, 'db': db, 'lemma': strong_szotar.get(g, {}).get('szoto', ''),
                 'jelentes': strong_szotar.get(g, {}).get('jelentes', '')}
                for db, g in sorted(bridge.get(s, []), reverse=True)[:3]],
    }

# ===================== 2. kör: Macula, UBS DBH, versszámozás, görög szó-lapok =====================
MORF_TORZS = {'q': 'Qal', 'N': "Nif'ál", 'p': "Pi'él", 'P': "Pu'al", 'h': "Hif'íl", 'H': "Hof'al",
              't': 'Hitpaél', 'o': 'Polel', 'O': 'Polal', 'r': 'Hitpolel', 'm': 'Poel', 'M': 'Poal',
              'k': 'Palel', 'K': 'Pulal', 'Q': 'Qal passzív', 'l': 'Pilpel', 'L': 'Polpal', 'f': 'Hitpalpel',
              'D': 'Nitpael', 'j': 'Pealal', 'i': 'Piel', 'u': 'Hotpaal', 'c': 'Tifil', 'v': 'Hishtafel', 'w': 'Nitpoel', 'y': 'Hishtafel'}
MORF_IDO = {'p': 'befejezett (qatal)', 'q': 'egymásutáni befejezett (weqatal)', 'i': 'befejezetlen (jiqtol)',
            'w': 'egymásutáni befejezetlen (wajjiqtol)', 'h': 'kohortatívusz', 'j': 'jusszívusz', 'v': 'felszólító',
            'r': 'cselekvő melléknévi igenév', 's': 'szenvedő melléknévi igenév', 'a': 'abszolút főnévi igenév',
            'c': 'szerkezeti főnévi igenév'}
SZEMELY = {'1': 'E/T 1.', '2': '2.', '3': '3.'}
NEM = {'m': 'hímnem', 'f': 'nőnem', 'c': 'közös nem', 'b': 'kétnemű'}
SZAM = {'s': 'egyes szám', 'p': 'többes szám', 'd': 'kettős szám'}
ALL = {'a': 'abszolút', 'c': 'szerkezeti (status constructus)', 'd': 'határozott'}
SZOFAJ = {'verb': 'ige', 'noun': 'főnév', 'adjective': 'melléknév', 'preposition': 'elöljáró', 'conjunction': 'kötőszó',
          'particle': 'partikula', 'pronoun': 'névmás', 'adverb': 'határozószó', 'suffix': 'rag', 'article': 'névelő'}


def csupasz(szo):
    """Görög szóalak ékezet és hehezet nélkül, kisbetűvel, végső szigma egységesítve (összevetéshez)."""
    import unicodedata
    t = unicodedata.normalize('NFD', szo or '')
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return t.lower().replace('ς', 'σ').strip('.,;·')


def tavolsag(a, b):
    """Levenshtein-távolság (rövid szavakra)."""
    if a == b:
        return 0
    elozo = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        akt = [i]
        for j, cb in enumerate(b, 1):
            akt.append(min(elozo[j] + 1, akt[j - 1] + 1, elozo[j - 1] + (ca != cb)))
        elozo = akt
    return elozo[-1]


def morf_hu(kod):
    """A Macula (OSHB-stílusú) morfológiai kód gépi magyar feloldása; ismeretlen jelnél a nyers kód marad."""
    if not kod:
        return ''
    if kod[0] == 'V' and len(kod) >= 3:
        r = [MORF_TORZS.get(kod[1], kod[1]), MORF_IDO.get(kod[2], kod[2])]
        rest = kod[3:]
        if rest[:1] in SZEMELY:
            r.append(SZEMELY[rest[0]] + ' személy'); rest = rest[1:]
        if rest[:1] in NEM:
            r.append(NEM[rest[0]]); rest = rest[1:]
        if rest[:1] in SZAM:
            r.append(SZAM[rest[0]]); rest = rest[1:]
        if rest[:1] in ALL:
            r.append(ALL[rest[0]])
        return ', '.join(r)
    if kod[0] in 'NA' and len(kod) >= 2:
        r = []
        rest = kod[2:]
        if kod[1] == 'p':
            r.append('tulajdonnév')
        elif kod[1] == 'g':
            r.append('népnév')
        if rest[:1] in NEM:
            r.append(NEM[rest[0]]); rest = rest[1:]
        if rest[:1] in SZAM:
            r.append(SZAM[rest[0]]); rest = rest[1:]
        if rest[:1] in ALL:
            r.append(ALL[rest[0]])
        return ', '.join(r)
    return ''


macula_vers = defaultdict(list)
for r in sorok('konkordancia/Macula_heber_Genezis.tsv'):
    if len(r) > 14 and r[2] in VERSEK:
        macula_vers[r[2]].append({'szo': r[5], 'lemma': r[6], 'strong': hnorm(r[7]) if r[7] else None,
                                  'morf': r[10], 'szofaj': r[11], 'gloss': r[12],
                                  'lxx': r[13], 'lxx_strong': hnorm(r[14]) if r[14] else None})

# UBS DBH: jelentés-besorolás előfordulásonként
ubs_ref = defaultdict(set)
for r in sorok('konkordancia/UBS_DBH_referenciak.tsv'):
    if len(r) > 2 and r[2] in VERSEK:
        n = hnorm(r[1])
        if n:
            ubs_ref[(r[2], n)].add(r[0])
ubs_jel = {}
for r in sorok('konkordancia/UBS_DBH_jelentesek.tsv'):
    if len(r) > 10:
        ubs_jel[r[4]] = {'domen': r[7], 'definicio': r[8], 'glosszak': r[10]}

# Versszámozás
versszam = {r[0]: {'kjv': r[1], 'mt': r[2], 'osztaly': r[3]} for r in sorok('konkordancia/Karoli_versmegfeleltetes.tsv')
            if r and r[0] in VERSEK}
lxx_igehely = {}
for r in sorok('konkordancia/LXX_OS/genesis.tsv'):
    if len(r) > 2 and r[2] in VERSEK:
        lxx_igehely.setdefault(r[2], r[0])

for v in versek:
    ig = v['igehely']
    mac = macula_vers[ig]
    th = v['heber']
    if len(mac) == len(th):
        for w, m in zip(th, mac):
            w['macula'] = m
    else:
        # eltérő szegmentálás: a tartalmas szót Strong-szám szerint, a H9xxx prefixumot a következő
        # Strong nélküli Macula-sorral párosítjuk, sorrendben
        mutato = defaultdict(int)
        hasznalt = set()
        for w in th:
            if w['strong'] and w['strong'].startswith('H9'):
                jel = [i for i, m in enumerate(mac) if m['strong'] is None and i not in hasznalt]
            else:
                jel = [i for i, m in enumerate(mac) if m['strong'] == w['strong'] and i not in hasznalt]
            w['macula'] = mac[jel[0]] if jel else None
            if jel:
                hasznalt.add(jel[0])
    # a görög szóalak az LXX_OS-ből (Rahlfs) jön; a Macula csak a héber–görög párosítást adja
    # (a Macula szóalakja helyenként hibás, pl. 1Móz 1:1 ἀρξῇ az ἀρχῇ helyett)
    # párosítás: azonos Strong-szám, és a szóalak ékezet nélkül azonos, vagy legfeljebb 1 betűben tér el
    lxx_szabad = [dict(x) for x in v['lxx']]
    for w in th:
        m = w.get('macula')
        if m and m.get('lxx_strong'):
            jelolt = [x for x in lxx_szabad if x['strong'] == m['lxx_strong'] and not x.get('_hasznalt')]
            mc = csupasz(m['lxx'])
            cel = next((x for x in jelolt if csupasz(x['szoalak']) == mc), None)
            if cel is None:
                cel = next((x for x in jelolt if tavolsag(csupasz(x['szoalak']), mc) <= 1), None)
            if cel:
                cel['_hasznalt'] = True
                m['lxx_macula'] = m['lxx']
                m['lxx'] = cel['szoalak']
                m['lxx_forras'] = 'LXX_OS'
            else:
                m['lxx_forras'] = 'Macula'
    for w in th:
        m = w.get('macula')
        if m:
            # a kód magyar feloldásához nincs jelkulcs a repóban (az ETCBC-modul NC-licencű, kizárt):
            # a Macula nyers kódja és szófaja áll, feloldás nélkül
            m['morf_hu'] = ''
            m['szofaj_hu'] = m['szofaj']
        lexidk = sorted(ubs_ref.get((ig, w['strong']), ()))
        w['ubs'] = [dict(ubs_jel[x], lexid=x) for x in lexidk if x in ubs_jel]
    vs = versszam.get(ig, {})
    v['versszam'] = {'karoli': ig, 'kjv': vs.get('kjv', ''), 'mt': vs.get('mt', '') or vs.get('kjv', ''),
                     'osztaly': vs.get('osztaly', ''), 'lxx': lxx_igehely.get(ig, '')}

# Görög szó-lapok az LXX-szavakhoz
gor_szavak = set()
for v in versek:
    for x in v['lxx']:
        if x['strong'] and x['strong'] not in nyelvtani:
            gor_szavak.add(x['strong'])
    for w in v['heber']:
        m = w.get('macula')
        if m and m['lxx_strong'] and m['lxx_strong'] not in nyelvtani:
            gor_szavak.add(m['lxx_strong'])

tbesg = {}
for s in open(GY + 'konkordancia/TBESG.txt', encoding='utf-8'):
    r = s.rstrip('\r\n').split('\t')
    if len(r) > 7 and re.match(r'^G\d{4}$', r[0]) and r[0] in gor_szavak and r[0] not in tbesg:
        jel = re.sub(r'<ref=[^>]*>', '', r[7])
        jel = re.sub(r'<BR\s*/?>', '\n', jel)
        jel = re.sub(r'<[^>]+>', '', jel).replace('__', '').strip()
        tbesg[r[0]] = {'lemma': r[3], 'atiras': r[4], 'gloss': r[6], 'szoveg': jel}
thayer = {}
for r in sorok('konkordancia/Thayer_teljes.tsv'):
    n = hnorm(r[0]) if r else None
    if n in gor_szavak and len(r) > 2:
        thayer[n] = r[2]
gor_hu = defaultdict(list)
for r in sorok('adat/forditasok.tsv'):
    if len(r) > 7 and r[0] in ('Thayer', 'UBS_DNTG') and r[6].strip():
        n = hnorm(r[1])
        if n in gor_szavak:
            gor_hu[n].append({'szotar': r[0], 'szam': r[3], 'szoveg': r[6].replace('\\n', '\n')})
usz_db = Counter()
usz_versek = defaultdict(list)
for r in sorok('konkordancia/TAGNT_kivonat.tsv'):
    if len(r) > 1:
        n = hnorm(r[1])
        if n in gor_szavak:
            usz_db[n] += 1
            if r[0] not in usz_versek[n]:
                usz_versek[n].append(r[0])
vissza = defaultdict(list)
for h, lst in bridge.items():
    for db, g in lst:
        if g in gor_szavak:
            vissza[g].append((db, h))

gor_lapok = {}
for g in sorted(gor_szavak):
    tb = tbesg.get(g, {})
    sz = strong_szotar.get(g, {})
    hu = gor_hu.get(g, [])
    th = thayer.get(g, '')
    gor_lapok[g] = {
        'strong': g,
        'lemma': tb.get('lemma') or sz.get('szoto', ''),
        'atiras': tb.get('atiras') or sz.get('kiejtes', ''),
        'gloss': tb.get('gloss') or sz.get('jelentes', ''),
        'szofaj': sz.get('szofaj', ''),
        'hu': [x for x in hu][:6],
        'tbesg': (tb.get('szoveg', '')[:900] + ('…' if len(tb.get('szoveg', '')) > 900 else '')) if tb else '',
        'thayer': th[:700] + ('…' if len(th) > 700 else ''),
        'usz_db': usz_db.get(g, 0),
        'usz_versek': [{'ig': ig, 'karoli': karoli.get(ig, '')} for ig in usz_versek.get(g, [])[:5]],
        'usz_versek_db': len(usz_versek.get(g, [])),
        'heber': [{'strong': h, 'db': db, 'lemma': strong_szotar.get(h, {}).get('szoto', ''),
                   'jelentes': strong_szotar.get(h, {}).get('jelentes', ''), 'lap': h in lapok}
                  for db, h in sorted(vissza.get(g, []), reverse=True)[:5]],
    }

prov = {
    'macula': 'scope=1Móz 1:1–2:3 | forras=konkordancia/Macula_heber_Genezis.tsv (morf: gépi magyar feloldás; héber–görög párosítás) + LXX_OS/genesis.tsv (a görög szóalak) | ts=%s' % TS,
    'ubs': 'scope=1Móz 1:1–2:3 | forras=konkordancia/UBS_DBH_referenciak.tsv + UBS_DBH_jelentesek.tsv (CC BY-SA 4.0) | ts=%s' % TS,
    'versszam': 'scope=1Móz 1:1–2:3 | forras=konkordancia/Karoli_versmegfeleltetes.tsv + LXX_OS/genesis.tsv | ts=%s' % TS,
    'gor': 'scope=strong | forras=konkordancia/TBESG.txt + Thayer_teljes.tsv + adat/forditasok.tsv (Thayer, UBS_DNTG) | ts=%s' % TS,
    'usz': 'scope=NT | forras=konkordancia/TAGNT_kivonat.tsv + Karoli_1908.tsv | ts=%s' % TS,
    'vissza': 'scope=strong | forras=adat/kulso/lxx_bridge.tsv (görög → héber) | ts=%s' % TS,
    'karoli': 'scope=1Móz 1:1–2:3 | forras=konkordancia/Karoli_1908.tsv | ts=%s' % TS,
    'heber': 'scope=1Móz 1:1–2:3 | forras=konkordancia/TAHOT_kivonat.tsv | ts=%s' % TS,
    'parok': 'scope=1Móz 1:1–2:3 | forras=adat/karoli_strong/parok_1Moz.tsv | ts=%s' % TS,
    'lxx': 'scope=1Móz 1:1–2:3 | forras=konkordancia/LXX_OS/genesis.tsv | ts=%s' % TS,
    'tsk': 'scope=1Móz 1:1–2:3 | forras=konkordancia/TSK_kereszthivatkozasok.tsv | ts=%s' % TS,
    'kh': 'scope=1Móz 1:1–2:3 | forras=konkordancia/Karoli_kereszthivatkozasok.tsv | ts=%s' % TS,
    'bdb': 'scope=strong | forras=adat/forditasok.tsv (BDB) + konkordancia/BDB_teljes_unabridged.tsv | ts=%s' % TS,
    'karoli_alak': 'scope=strong | forras=adat/karoli_strong/parok_{%s}.tsv | ts=%s' % (','.join(pkonyvek), TS),
    'elofordulas': 'scope=OT | forras=konkordancia/TAHOT_kivonat.tsv (nem teljes) | ts=%s' % TS,
    'bridge': 'scope=strong | forras=adat/kulso/lxx_bridge.tsv | ts=%s' % TS,
}
with open(KI, 'w', encoding='utf-8') as fh:
    licenc = {}
    for r in sorok('adat/licencek.tsv'):
        if len(r) > 9:
            licenc[r[0]] = r[9]
    json.dump({'licenc': licenc, 'versek': versek, 'lapok': lapok, 'gor_lapok': gor_lapok, 'prov': prov, 'karoli_konyvek': pkonyvek,
               'bdb_kesz': len(bdb_hu)}, fh, ensure_ascii=False)
print('versek:', len(versek), '| szó-lapok:', len(lapok), '| ebből magyar BDB:',
      sum(1 for x in lapok.values() if x['bdb_hu']), '| Károli-könyvek:', pkonyvek)
for v in versek:
    print(v['igehely'], 'héber szó', len(v['heber']), 'LXX', len(v['lxx']), 'TSK', v['tsk_db'], 'KH', len(v['karoli_kh']),
          'kötött hu szó', sum(1 for h in v['hu_szavak'] if h['fo']))
print('görög szó-lap:', len(gor_lapok), '| magyar görög szócikk:', sum(1 for x in gor_lapok.values() if x['hu']))
for v in versek:
    print(v['igehely'], 'macula-kötés', sum(1 for w in v['heber'] if w.get('macula')), '/', len(v['heber']),
          '| UBS-jelentés', sum(1 for w in v['heber'] if w['ubs']), '| versszám', v['versszam'])
print('JSON bájt:', os.path.getsize(KI))
