"""Olvasói pilot: a pilot datasetjének felmérése (F60.5, v2).

Minden adatkészletre (konkordancia/*.tsv|txt, konkordancia/LXX_OS, adat/*.tsv, adat/karoli_strong, adat/kulso)
egy sor: használja-e a pilot (igen / most bővítve / nem), mi a kulcsa, a lefedettség a két szakaszon (db/összes, %),
a licenc (adat/licencek.tsv), a proveniencia-sor (scope=… | forras=… | ts=…), és ha nem használt, miért nem.
A végén összefoglaló: hány Strong-kulcsú szó-lapnak hány adatforrása van, mely lapokon vannak hiányok, mely
hiányok tölthetők ki meglévő adattal, melyek nem (és melyik feladat dolga).
A számokat méri (táblák olvasása + a szakasz-JSON), nem becsli. Csak olvas; a kimenet: naplok/OLVASOI_PILOT_adatfelmeres.md.
A TSV-t split('\\t')-bel olvassa (csv modul tilos).
Futtatás: python eszkozok/olvaso_pilot/felmeres.py [--szakasz "1Móz 1:1-2:3" --szakasz "Zsolt 22"] [--ki FÁJL] [--nincs-ujra]
(alapból az adat.py-t újrafuttatja a szakaszok alap-kimeneti könyvtárába, hogy a mérés a friss JSON-ból menjen)."""
import argparse
import datetime
import json
import os
import re
import statistics
import subprocess
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from szakasz import GY, alap_kimenet, szakasz_cim  # noqa: E402

ap = argparse.ArgumentParser(description='Olvasói pilot: adatfelmérés')
ap.add_argument('--szakasz', action='append', default=None)
ap.add_argument('--ki', default=GY + 'naplok/OLVASOI_PILOT_adatfelmeres.md')
ap.add_argument('--nincs-ujra', action='store_true', help='ne futtassa újra az adat.py-t (a meglévő JSON-t használja)')
args = ap.parse_args()
SZAKASZOK = args.szakasz or ['1Móz 1:1-2:3', 'Zsolt 22']
TS = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
KONYV_STEP = {'1Móz': 'Gen', 'Zsolt': 'Psa'}


# ------------------------------------------------------------------ olvasás
def sorok(rel, fejlec=True):
    with open(GY + rel, encoding='utf-8-sig') as fh:
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
    m = re.match(r'^([HG])0*(\d+)([A-Za-z]?)$', (s or '').strip())
    return '%s%04d' % (m.group(1).upper(), int(m.group(2))) if m else None


_C = {}


def strongs(rel, col=0, fejlec=True):
    k = ('S', rel, col)
    if k not in _C:
        _C[k] = {n for r in sorok(rel, fejlec) if len(r) > col for n in [hnorm(r[col])] if n}
    return _C[k]


def kulcsok(rel, col=0, fejlec=True):
    k = ('K', rel, col)
    if k not in _C:
        _C[k] = {r[col] for r in sorok(rel, fejlec) if len(r) > col}
    return _C[k]


def sorszam(rel, col, versek, fejlec=True):
    """Hány sor érinti a szakasz verseit (col: Károli-igehely)."""
    vs = set(versek)
    return sum(1 for r in sorok(rel, fejlec) if len(r) > col and r[col] in vs)


def tw_strongs():
    if ('tw',) not in _C:
        out = set()
        for r in sorok('konkordancia/tW_szocikkek.tsv'):
            if len(r) > 3:
                out.update(s for s in r[3].split('+') if s)
        _C[('tw',)] = out
    return _C[('tw',)]


def fr(db, ossz):
    return '%d/%d (%.1f%%)' % (db, ossz, 100.0 * db / ossz) if ossz else '%d/0' % db


# ------------------------------------------------------------------ szakasz-környezet
def betolt(szakasz):
    ki = alap_kimenet(szakasz)
    if not args.nincs_ujra:
        subprocess.run([sys.executable, os.path.join(D, 'adat.py'), '--szakasz', szakasz, '--kimenet', ki], check=True,
                       stdout=subprocess.DEVNULL)
    with open(os.path.join(ki, 'olvaso_pilot.json'), encoding='utf-8') as fh:
        d = json.load(fh)
    konyv = d['versek'][0]['igehely'].split(' ')[0]
    return {'szak': szakasz, 'cim': szakasz_cim(szakasz), 'd': d, 'heb': set(d['lapok']), 'gor': set(d['gor_lapok']),
            'versek': [v['igehely'] for v in d['versek']], 'konyv': konyv, 'step': KONYV_STEP.get(konyv, ''),
            'json_bajt': os.path.getsize(os.path.join(ki, 'olvaso_pilot.json')), 'ts_json': d['prov']['heber'].split('ts=')[-1]}


CTX = [betolt(s) for s in SZAKASZOK]


# ------------------------------------------------------------------ mérő-függvények (szakaszonként egy szöveg)
def H(rel, col=0, fejlec=True):
    return lambda c: 'H: ' + fr(len(c['heb'] & strongs(rel, col, fejlec)), len(c['heb']))


def G(rel, col=0, fejlec=True):
    return lambda c: 'G: ' + fr(len(c['gor'] & strongs(rel, col, fejlec)), len(c['gor']))


def HG(rel, hc=0, gc=0, fejlec=True):
    return lambda c: 'H: %s; G: %s' % (fr(len(c['heb'] & strongs(rel, hc, fejlec)), len(c['heb'])),
                                       fr(len(c['gor'] & strongs(rel, gc, fejlec)), len(c['gor'])))


def V(rel, col=0, fejlec=True):
    return lambda c: 'vers: ' + fr(len(set(c['versek']) & kulcsok(rel, col, fejlec)), len(c['versek']))


def SOR(rel, col, fejlec=True):
    return lambda c: '%d sor a szakasz verseire' % sorszam(rel, col, c['versek'], fejlec)


def JSV(fn, cimke='vers'):
    return lambda c: '%s: %s' % (cimke, fr(sum(1 for v in c['d']['versek'] if fn(v)), len(c['versek'])))


def NA(ok):
    return lambda c: 'n/a (%s)' % ok


def egy_konyv(konyv, fn):
    """A tábla csak a megadott könyvre vonatkozik; másik szakaszra n/a."""
    return lambda c: fn(c) if c['konyv'] == konyv else 'n/a (a tábla nem a szakasz könyvéről szól)'


def step_vers(rel, col=0, fejlec=True):
    """STEPBible-alakú kulcs (Gen.1.1), a Károli = KJV számozású szakaszra (Genezis)."""
    def f(c):
        if c['step'] != 'Gen':
            return 'n/a (a tábla nem a szakasz könyvéről szól)'
        kell = {'Gen.' + v.split(' ')[1].replace(':', '.') for v in c['versek']}
        return 'vers: ' + fr(len(kell & kulcsok(rel, col, fejlec)), len(kell))
    return f


def m_alias(c):
    return 'H: %d lap kapott aliast (a saját szócikk nélkül) / %d' % (sum(1 for l in c['d']['lapok'].values() if l.get('bdb_alias')), len(c['heb']))


def m_hu_bdb(c):
    return 'H: ' + fr(sum(1 for l in c['d']['lapok'].values() if l['bdb_hu']), len(c['heb'])) + '; G (Thayer/UBS_DNTG): ' + \
        fr(sum(1 for l in c['d']['gor_lapok'].values() if l['hu']), len(c['gor']))


def m_bdb(c):
    return 'H: ' + fr(sum(1 for l in c['d']['lapok'].values() if l['bdb_hu'] or l['bdb_en']), len(c['heb']))


def m_ubs_dbh(c):
    szavak = [w for v in c['d']['versek'] for w in v['heber'] if not w['nyelvtani']]
    return 'H: %s; előfordulás: %s' % (fr(len(c['heb'] & strongs('konkordancia/UBS_DBH_referenciak.tsv', 1)), len(c['heb'])),
                                       fr(sum(1 for w in szavak if w['ubs']), len(szavak)))


def m_macula(c):
    szavak = [w for v in c['d']['versek'] for w in v['heber']]
    return 'szó: ' + fr(sum(1 for w in szavak if w.get('macula')), len(szavak))


def m_morf(c):
    mac = [w['macula'] for v in c['d']['versek'] for w in v['heber'] if w.get('macula') and w['macula'].get('morf')]
    return 'szó: ' + fr(sum(1 for m in mac if m.get('morf_hu')), len(mac))


def m_morf_nyelv(c):
    n = c['d']['stat']['morf_aramai_szo']
    return 'arámi szó: %d (a szakasz Macula-szavai közül; nincs arámi)' % n if not n else 'arámi szó: %d' % n


def m_tahot(c):
    return 'vers: ' + fr(len(set(c['versek']) & kulcsok('konkordancia/TAHOT_kivonat.tsv', 0)), len(c['versek']))


def m_tagnt(c):
    return 'G: ' + fr(len(c['gor'] & strongs('konkordancia/TAGNT_kivonat.tsv', 1)), len(c['gor']))


def m_usz(c):
    st = c['d']['stat']
    return 'ÚSZ-hely (a lapon listázott): ' + fr(st['usz_hely_ubs'], st['usz_hely'])


def m_tipnr(c):
    st = c['d']['stat']
    return 'vers: %s; sor illesztve: %s' % (fr(sum(1 for v in c['d']['versek'] if v['tipnr']), len(c['versek'])),
                                            fr(st['tipnr_illesztett'], st['tipnr_osszes']))


def m_adatreteg(kulcs):
    def f(c):
        db = sum(len(v[kulcs]) for v in c['d']['versek'])
        n = sum(1 for v in c['d']['versek'] if v[kulcs])
        return '%d sor, %d vers érintett / %d' % (db, n, len(c['versek']))
    return f


def m_lxx_par(c):
    st = c['d']['stat']
    return 'vers: %s; %d pár' % (fr(st['lxx_par_vers'], len(c['versek'])), st['lxx_par_sor'])


def m_tw(c):
    t = tw_strongs()
    return 'H: %s; G: %s' % (fr(len(c['heb'] & t), len(c['heb'])), fr(len(c['gor'] & t), len(c['gor'])))


def m_bsb(c):
    return 'vers: ' + fr(c['d']['stat']['bsb_vers'], len(c['versek']))


def m_kjv(c):
    return 'vers: ' + fr(c['d']['stat']['kjv_vers'], len(c['versek']))


def m_nave(c):
    return 'vers: ' + fr(c['d']['stat']['nave_vers'], len(c['versek']))


def m_lxx_os(c):
    return 'vers: ' + fr(sum(1 for v in c['d']['versek'] if v['lxx']), len(c['versek']))


def m_parok(c):
    n = sum(1 for v in c['d']['versek'] if any(w['strongok'] for w in v['hu_szavak']))
    return 'vers: %s; szó: %s' % (fr(n, len(c['versek'])), fr(sum(1 for v in c['d']['versek'] for w in v['hu_szavak'] if w['fo']),
                                                              sum(len(v['hu_szavak']) for v in c['d']['versek'])))


def m_tsk(c):
    return 'vers: ' + fr(sum(1 for v in c['d']['versek'] if v['tsk_db']), len(c['versek']))


def m_kh(c):
    return 'vers: ' + fr(sum(1 for v in c['d']['versek'] if v['karoli_kh']), len(c['versek']))


def m_tbesg(c):
    return 'G: ' + fr(sum(1 for l in c['d']['gor_lapok'].values() if l['tbesg']), len(c['gor']))


def m_tbesh(c):
    return 'H: ' + fr(sum(1 for l in c['d']['lapok'].values() if l.get('tbesh')), len(c['heb']))


def m_bridge(c):
    h = sum(1 for l in c['d']['lapok'].values() if l['lxx'])
    g = sum(1 for l in c['d']['gor_lapok'].values() if l['heber'])
    return 'H→G: %s; G→H: %s' % (fr(h, len(c['heb'])), fr(g, len(c['gor'])))


def m_versmegf(c):
    return 'vers: ' + fr(len(set(c['versek']) & kulcsok('konkordancia/Karoli_versmegfeleltetes.tsv', 0)), len(c['versek']))


def m_gramm(c):
    return 'a szakasz Strong-számai közül nyelvtani (szó-lap nélkül): %d' % len(c['d'].get('nyelvtani_strongok', []))


def m_kjv_oszlop(c):
    return 'KJV-szám egyezik a Károli-számmal: ' + fr(sum(1 for v in c['d']['versek'] if v['versszam']['kjv_kulcs'] == v['igehely'].split(' ')[1]), len(c['versek']))


# ------------------------------------------------------------------ licenc
LIC = {}
for r in sorok('adat/licencek.tsv'):
    if len(r) > 9:
        LIC[r[0]] = {'cimke': r[9], 'allapot': r[7], 'ker': r[4], 'sa': r[5]}


def lic(*kulcsok_):
    ki = []
    for k in kulcsok_:
        j = LIC.get(k)
        if not j:
            ki.append('%s: nincs sor a licencek.tsv-ben' % k)
            continue
        jel = []
        if j['allapot'] == 'tisztazatlan':
            jel.append('tisztázatlan')
        if j['ker'] != 'igen':
            jel.append({'nem': 'nem kereskedelmi', 'feltetelesen': 'kereskedelmi feltétellel', 'tisztazatlan': 'kereskedelmi: tisztázatlan'}.get(j['ker'], j['ker']))
        if j['sa'] == 'igen':
            jel.append('share-alike')
        ki.append('%s: %s%s' % (k, j['cimke'], ' [%s]' % ', '.join(jel) if jel else ''))
    return '; '.join(ki)


# ------------------------------------------------------------------ a sorok
IGEN, UJ, NEM = 'igen', 'most bővítve', 'nem'
SOROK = []


def R(nev, fajl, pilot, kulcs, lickulcs, mero, ok=''):
    SOROK.append({'nev': nev, 'fajl': fajl, 'pilot': pilot, 'kulcs': kulcs, 'lic': lic(*lickulcs) if lickulcs else 'nincs sor a licencek.tsv-ben (belső tábla)',
                  'mero': mero, 'ok': ok})


K = 'konkordancia/'
A = 'adat/'
# --- a pilot eddig is használta
R('Karoli_1908', K + 'Karoli_1908.tsv', IGEN, 'vers (szó: a szöveg tokenizálva)', ['Karoli_1908'], V(K + 'Karoli_1908.tsv'))
R('TAHOT_kivonat', K + 'TAHOT_kivonat.tsv', IGEN, 'vers, szó, Strong', ['TAHOT'], m_tahot, 'nem teljes (CLAUDE.md): a hiányzó fejezetek a két szakaszt nem érintik')
R('TAGNT_kivonat', K + 'TAGNT_kivonat.tsv', IGEN, 'Strong (görög), vers', ['TAGNT'], m_tagnt)
R('Macula_heber_Genezis / Macula_heber_Zsoltarok', K + 'Macula_heber_{Genezis,Zsoltarok}.tsv', IGEN, 'vers, szó (morfema), Strong', ['Macula_heber'], m_macula, 'a morfológiai kód magyar feloldása: most bővítve (morf_kulcs_heber)')
R('Macula_heber_* (a másik 37 könyv)', K + 'Macula_heber_*.tsv', NEM, 'vers, szó', ['Macula_heber'], NA('más könyvek'), 'a két szakasz könyvét (1Móz, Zsolt) a fenti sor már használja')
R('LXX_OS (genesis.tsv, psalms-lxx.tsv)', K + 'LXX_OS/{genesis,psalms-lxx}.tsv', IGEN, 'vers (Károli-kulcs), szó, Strong (görög)', ['LXX_OS'], m_lxx_os)
R('LXX_OS (a másik 58 könyvfájl)', K + 'LXX_OS/*.tsv', NEM, 'vers, szó', ['LXX_OS'], NA('más könyvek'), 'a két szakasz könyve nincs köztük')
R('LXX_OS/karoli_fejezet_dontes.tsv', K + 'LXX_OS/karoli_fejezet_dontes.tsv', NEM, 'fejezet (Károli-kulcs eltolás)', ['LXX_OS'],
  lambda c: '%d sor a szakasz fejezetére' % sum(1 for r in sorok(K + 'LXX_OS/karoli_fejezet_dontes.tsv') if r[0] == c['konyv'] and r[1] in {v.split(' ')[1].split(':')[0] for v in c['versek']}),
  'a Károli–LXX fejezet-eltolás (KK7) segédtábla; a pilot a LXX_OS kész Károli-kulcsát használja')
R('LXX_OS/karoli_vers_felulbiralas.tsv', K + 'LXX_OS/karoli_vers_felulbiralas.tsv', NEM, 'vers (Károli-kulcs felülbírálás)', ['LXX_OS'], SOR(K + 'LXX_OS/karoli_vers_felulbiralas.tsv', 3),
  'segédtábla (KK7.5) a Károli-kulcs felülbírálásához; a pilot a kész LXX_OS Károli-kulcsát használja')
R('TSK_kereszthivatkozasok', K + 'TSK_kereszthivatkozasok.tsv', IGEN, 'vers', ['TSK'], m_tsk)
R('Karoli_kereszthivatkozasok', K + 'Karoli_kereszthivatkozasok.tsv', IGEN, 'vers (STEP-alak, normalizálva)', ['Karoli_KH'], m_kh)
R('BDB_teljes_unabridged', K + 'BDB_teljes_unabridged.tsv', IGEN, 'Strong (héber)', ['BDB'], m_bdb, 'a lefedettség az alias-pótlással együtt (BDB_strong_alias, most bővítve)')
R('Strong_szotar', K + 'Strong_szotar.tsv', IGEN, 'Strong (héber, görög)', ['Strong_szotar'], HG(K + 'Strong_szotar.tsv', 0, 0))
R('TBESG', K + 'TBESG.txt', IGEN, 'Strong (görög)', ['TBESG'], m_tbesg)
R('Thayer_teljes', K + 'Thayer_teljes.tsv', IGEN, 'Strong (görög)', ['Thayer'], G(K + 'Thayer_teljes.tsv', 0))
R('UBS_DBH_referenciak + UBS_DBH_jelentesek', K + 'UBS_DBH_{referenciak,jelentesek}.tsv', IGEN, 'Strong + vers + szópozíció (előfordulás-jelentés)', ['UBS_DBH'], m_ubs_dbh)
R('Karoli_versmegfeleltetes', K + 'Karoli_versmegfeleltetes.tsv', IGEN, 'vers (Károli → KJV/MT)', ['Karoli_versmegfeleltetes'], m_versmegf,
  'Zsolt 22-re a KJV-oszlop hibás (lásd az összefoglalót); a pilot az LXX_OS KJV-oszlopával egészíti ki')
R('Konyv_normalizalo_tabla', K + 'Konyv_normalizalo_tabla.tsv', IGEN, 'könyvkód (STEP ↔ magyar)', ['Konyv_nevtablak'], NA('kulcs-konverzió, nem tartalmi adat'))
R('adat/karoli_strong/parok_*.tsv', A + 'karoli_strong/parok_{1Moz..Zsolt}.tsv', IGEN, 'vers + Károli-szó sorszám → Strong (modell-kimenet, #22)', ['projekt_adat'], m_parok)
R('adat/karoli_strong/szavak_*.tsv', A + 'karoli_strong/szavak_*.tsv', NEM, 'vers + oldal + szó sorszám', ['projekt_adat'], NA('a kötött párokat a parok_ tábla már tartalmazza'),
  'a szavak_ tábla a párosítatlan szavak állapotát is rögzíti (munkatábla); a pilot a párosítatlan Károli-szót a szövegből és a parok_ hiányából jelzi, további információt nem ad')
R('adat/forditasok.tsv', A + 'forditasok.tsv', IGEN, 'szótár + Strong + jelentés-szám (magyar fordítás, modell-kimenet)', ['projekt_adat'], m_hu_bdb)
R('adat/grammatikai_strongok.tsv', A + 'grammatikai_strongok.tsv', IGEN, 'Strong (nyelvtani elemek szűrése)', ['projekt_adat'], NA('szűrőlista: a nyelvtani Strong-számok nem kapnak szó-lapot'))
R('adat/kulso/lxx_bridge.tsv', A + 'kulso/lxx_bridge.tsv', IGEN, 'Strong (héber ↔ görög)', ['lxx_bridge'], m_bridge)
R('adat/licencek.tsv', A + 'licencek.tsv', IGEN, 'dataset (licenc-jelzés a „?” súgóban)', ['projekt_adat'], NA('minden blokk licenc-sora innen jön (a teszt ellenőrzi)'))

# --- most bővítve
R('SDBH_domenek', K + 'SDBH_domenek.tsv', UJ, 'Strong (héber)', ['SDBH'], H(K + 'SDBH_domenek.tsv', 0), 'szó-lap: szemantikai domén; üres eredmény nem negatív lelet (a szókincs ~90%-a)')
R('SDGNT_domenek', K + 'SDGNT_domenek.tsv', UJ, 'Strong (görög)', ['SDGNT'], G(K + 'SDGNT_domenek.tsv', 0))
R('SDBH_SDGNT_domenfa', K + 'SDBH_SDGNT_domenfa.tsv', UJ, 'domén-kód (szülő-szintek)', ['SDBH_SDGNT_segedtablak'], NA('a domén-kódok szülő-útját adja a domén-blokkban'))
R('SECE_H_teljes', K + 'SECE_H_teljes.tsv', UJ, 'Strong (héber)', ['SECE_H'], H(K + 'SECE_H_teljes.tsv', 0))
R('SECE_G_teljes', K + 'SECE_G_teljes.tsv', UJ, 'Strong (görög)', ['SECE_G'], G(K + 'SECE_G_teljes.tsv', 0))
R('OSHL_lexikalis_index', K + 'OSHL_lexikalis_index.tsv', UJ, 'Strong (héber) → TWOT, BDB-azonosító', ['OSHL'], H(K + 'OSHL_lexikalis_index.tsv', 0))
R('TBESH', K + 'TBESH.txt', UJ, 'Strong (héber, eStrong)', ['TBESH'], m_tbesh, 'licenc-aggály: a jelentés-lista Online Bible-eredetű (a fejléc szerint külön engedély kell)')
R('LSJ_teljes', K + 'LSJ_teljes.tsv', UJ, 'Strong (görög)', ['LSJ'], G(K + 'LSJ_teljes.tsv', 0))
R('MCGED_teljes', K + 'MCGED_teljes.tsv', UJ, 'Strong (görög)', ['MCGED'], G(K + 'MCGED_teljes.tsv', 0), 'licenc: nem kereskedelmi, kötelező forrásmegjelölés (a blokk mutatja)')
R('UBS_DNTG_jelentesek', K + 'UBS_DNTG_jelentesek.tsv', UJ, 'Strong (görög) → jelentések (angol)', ['UBS_DNTG'], G(K + 'UBS_DNTG_jelentesek.tsv', 0))
R('UBS_DNTG_referenciak', K + 'UBS_DNTG_referenciak.tsv', UJ, 'Strong + ÚSZ-igehely (az előfordulás jelentése)', ['UBS_DNTG'], m_usz)
R('tW_szocikkek', K + 'tW_szocikkek.tsv', UJ, 'Strong (a strong oszlop „+”-szal elválasztott lista)', ['tW_szocikkek'], m_tw, 'licenc: CC BY-SA, share-alike (a blokk jelzi)')
R('BSB_Strongs', K + 'BSB_Strongs.tsv', UJ, 'vers (STEP, MT-szám; „Számozás” oszlop) + szósorszám', ['BSB_Strongs'], m_bsb, 'Zsolt 22:1–2: nincs sor a táblában (nem pótolja a pilot)')
R('KJV_Strongs_teljes', K + 'KJV_Strongs_teljes.tsv', UJ, 'vers (STEP, KJV-szám) + szósorszám', ['KJV_Strongs_teljes'], m_kjv, 'licenc: a Strong-címkék tisztázatlanok; a vers-kulcs az LXX_OS KJV-oszlopából jön')
R('Nave_basokant', K + 'Nave_basokant.tsv', UJ, 'vers / tartomány / fejezet (KJV-számozás)', ['Nave_basokant'], m_nave, 'a tartomány bontása versekre: gépi feldolgozás')
R('TIPNR_kivonat', K + 'TIPNR_kivonat.tsv', UJ, 'vers (STEP) + Strong (név)', ['TIPNR'], m_tipnr, 'a számozást a vers Strong-számai igazolják (gépi illesztés)')
R('LXX_versszintu_parok', K + 'LXX_versszintu_parok.tsv', UJ, 'vers (Károli-kulcs) + héber Strong + görög Strong', ['LXX_versszintu_parok'], m_lxx_par, 'együttelőfordulás, NEM szóillesztés; licenc tisztázatlan')
R('LXX_tobblet_szakaszok', K + 'LXX_tobblet_szakaszok.tsv', UJ, 'vers (Károli-kulcs, próbált)', ['Versifikacios_tablak'], SOR(K + 'LXX_tobblet_szakaszok.tsv', 6), 'a két szakaszra nincs sor (üres eredmény, jelezve)')
R('Verzifikacios_elteres_tabla', K + 'Verzifikacios_elteres_tabla.tsv', UJ, 'vers (Károli-kulcs)', ['Versifikacios_tablak'], SOR(K + 'Verzifikacios_elteres_tabla.tsv', 2), 'a két szakaszra nincs sor (üres eredmény, jelezve)')
R('adat/morf_kulcs_heber.tsv', A + 'morf_kulcs_heber.tsv', UJ, 'morfológiai kód pozíciónként', ['morf_kulcs_heber'], m_morf, 'a nyers kód is látszik')
R('adat/morf_nyelv_aramai.tsv', A + 'morf_nyelv_aramai.tsv', UJ, 'xml_id (Macula) → nyelv (héber/arámi)', ['morf_nyelv_aramai'], m_morf_nyelv)
R('adat/kapcsolatok.tsv', A + 'kapcsolatok.tsv', UJ, 'forrás- vagy cél-igehely (tartomány)', ['projekt_adat'], m_adatreteg('kapcsolat'), 'nincs sor-szintű proveniencia-mező')
R('adat/elofordulasok.tsv', A + 'elofordulasok.tsv', UJ, 'igehely (tartomány)', ['projekt_adat'], m_adatreteg('motivum'), 'sor-szintű proveniencia-mezővel jelenik meg')
R('adat/motivumok.tsv', A + 'motivumok.tsv', UJ, 'motívum-ID (az elofordulasok/kapcsolatok címkéjéhez)', ['projekt_adat'], NA('csak a motívum-címke, az előfordulás-sorokhoz kapcsolva'))
R('adat/lxx_dontesek.tsv', A + 'lxx_dontesek.tsv', UJ, 'igehely (Károli)', ['projekt_adat'], m_adatreteg('lxx_dontes'), 'a két szakaszra nincs sor (üres eredmény, jelezve)')
R('adat/szotar_szerepek.tsv', A + 'szotar_szerepek.tsv', NEM, 'nyelv + sorrend (szótári szerepek)', None, NA('nem vers- vagy szó-kulcsú'),
  'a szerepmátrix a lexikonoldal rendereléséhez (RENDER) tartozik; a pilot a blokkokat adatforrásuk szerint nevezi, a felületi címke nem igényel adatot; a szerepek fele „nincs adatosítva”')
R('adat/terminologia.tsv', A + 'terminologia.tsv', NEM, 'angol kifejezés → magyar', None, NA('nem vers- vagy szó-kulcsú'),
  'a magyar BDB-fordítás rövidítés-feloldása (fordítási folyamat); a lapon nem jelenik meg adat-alapú felületi címkeként')

# --- a pilot nem használja
R('ASV_Strongs_{Genesis,Exodus,Proverbs}', K + 'ASV_Strongs_*.tsv', NEM, 'vers (STEP) + szósorszám', ['KJV_ASV_Strongs'], step_vers(K + 'ASV_Strongs_Genesis.tsv', 0),
  'az ASV nem használható (forráshibás, N29/D7); a BSB és a KJV teljes pótolja')
R('KJV_Strongs_{Genesis,Exodus,Proverbs}', K + 'KJV_Strongs_{Genesis,Exodus,Proverbs}.tsv', NEM, 'vers (STEP) + szósorszám', ['KJV_ASV_Strongs'], step_vers(K + 'KJV_Strongs_Genesis.tsv', 0),
  'a régi, három könyves KJV-fájl; a KJV_Strongs_teljes váltja (kivezetés: #48)')
R('Angol_konyvnev_STEPBible_tabla', K + 'Angol_konyvnev_STEPBible_tabla.tsv', NEM, 'könyvkód', ['Konyv_nevtablak'], NA('könyvnév-segédtábla'), 'a Konyv_normalizalo_tabla szolgálja a kulcs-konverziót')
R('BDB_aram_potlas', K + 'BDB_aram_potlas.tsv', NEM, 'Strong (arámi) → BDB-szócikk', ['BDB'], H(K + 'BDB_aram_potlas.tsv', 0), 'arámi szavak pótlása; a két szakaszon nincs arámi szó')
R('BDB_etimologia_kezi_hatarok', K + 'BDB_etimologia_kezi_hatarok.tsv', NEM, 'Strong → a nyelvi háttér határa', ['BDB'], H(K + 'BDB_etimologia_kezi_hatarok.tsv', 0),
  'a nyelvi háttér kézi határai a BDB-bontáshoz; a pilot a gépi szeletelést mutatja (jelezve), a kézi határokat nem veszi át (további bővítés)')
R('BDB_strong_alias', K + 'BDB_strong_alias.tsv', UJ, 'Strong (másodlagos) → táblabeli Strong', ['projekt_adat'], m_alias, 'csak a saját szócikk nélküli Strong-számokra, jelzéssel (gépi alias)')
R('BDB_strong_alias_elvetett', K + 'BDB_strong_alias_elvetett.tsv', NEM, 'Strong (másodlagos)', ['projekt_adat'], H(K + 'BDB_strong_alias_elvetett.tsv', 0), 'elvetett alias-jelöltek (a #57 kimenete): éppen azért nem szabad megjeleníteni')
R('BDB_strong_potlas', K + 'BDB_strong_potlas.tsv', NEM, 'bdb_id → Strong', ['projekt_adat'], H(K + 'BDB_strong_potlas.tsv', 1), 'a hiányzó Strong-számok BDB-párosítása (#57); a megjelenítés a BDB-szócikk szövegét igényelné, az alias-sorok kivételével nincs egyértelmű pár')
R('OSHL_BDB_igehelyek', K + 'OSHL_BDB_igehelyek.tsv', NEM, 'Strong + BDB-azonosító + igehely (BDB-hivatkozás)', ['OSHL_BDB'], H(K + 'OSHL_BDB_igehelyek.tsv', 0),
  'a BDB-szócikkek igehely-hivatkozásai; a BDB hivatkozási számozása vegyes (javítótábla: #56), igazolt Károli-kulcs nincs: a vers-lapon félrevezető lenne')
R('Karoli_Strong_kivonat', K + 'Karoli_Strong_kivonat.tsv', NEM, 'vers (STEP) + Strong + Károli-szó', ['Karoli_Strong_kivonat'], step_vers(K + 'Karoli_Strong_kivonat.tsv', 0),
  'régi, 1Móz-ra szűkített kivonat (tisztázatlan licenc); az adat/karoli_strong/parok_ váltja')
R('Karoli_adatminosegi_anomaliak', K + 'Karoli_adatminosegi_anomaliak.tsv', NEM, 'Károli-igehely', None, SOR(K + 'Karoli_adatminosegi_anomaliak.tsv', 0), 'minőségi napló (a javított sorok); nem tartalmi adat')
R('Karoli_ures_helyorzo_sorok', K + 'Karoli_ures_helyorzo_sorok.tsv', NEM, 'Károli-igehely', None, SOR(K + 'Karoli_ures_helyorzo_sorok.tsv', 0), 'minőségi napló; nem tartalmi adat')
R('TAHOT_kivonat_nyitott_esetek', K + 'TAHOT_kivonat_nyitott_esetek.tsv', NEM, 'STEP-vers', None,
  lambda c: '%d sor a szakasz könyvére' % sum(1 for r in sorok(K + 'TAHOT_kivonat_nyitott_esetek.tsv') if r[0].startswith(c['step'] + '.')), 'minőségi napló (nyitott esetek); nem tartalmi adat')
R('UBS_DBH_anomaliak / UBS_DNTG_anomaliak / SDBH_SDGNT_anomaliak', K + 'UBS_*_anomaliak.tsv, SDBH_SDGNT_anomaliak.tsv', NEM, 'szócikk', ['UBS_DBH'], NA('minőségi napló'), 'import-anomáliák; nem tartalmi adat')
R('LXX_versificacios_terkep', K + 'LXX_versificacios_terkep.tsv', NEM, 'vers (Károli-igehely) → héber/latin/LXX-vers', ['Versifikacios_tablak'], V(K + 'LXX_versificacios_terkep.tsv', 0),
  'a „Károli-igehely” oszlop a Zsolt 22-re KJV-számozású (22:1 = „Psa.22:1-2”, EGYIK_SEM): a Károli (MT) számozásával ellentmond, ezért megjelenítése félrevezető lenne (lásd az összefoglalót)')
R('Nem_parszolhato_terkep_ertekek', K + 'Nem_parszolhato_terkep_ertekek.tsv', NEM, 'Károli-igehely', ['Versifikacios_tablak'], SOR(K + 'Nem_parszolhato_terkep_ertekek.tsv', 1), 'a verszámozási térkép nem értelmezhető értékei (segédtábla)')
R('Betu_utotag_kizarva', K + 'Betu_utotag_kizarva.tsv', NEM, 'Károli-igehely', ['Versifikacios_tablak'], SOR(K + 'Betu_utotag_kizarva.tsv', 1), 'betűutótagos LXX-hivatkozások kizárt sorai (segédtábla)')
R('Macula_gorog', K + 'Macula_gorog.tsv', NEM, 'vers (ÚSZ), szó, Strong', ['Macula_gorog'], NA('az ÚSZ-t fedi, a két szakasz ÓSZ'), 'a görög szó-lapok az LXX-szavakból és az ÚSZ-előfordulásokból (TAGNT) épülnek; az ÚSZ-szöveg külön pilot-szakasz tárgya lenne')
R('konkordancia/_nyers/*, lexikonok_nyers/*', K + '_nyers/*, lexikonok_nyers/*', NEM, 'nyers forrásfájlok', ['lexikonok_nyers'], NA('nyers forrás'), 'a feldolgozott táblákat használja a pilot; a nyers fájlok licence tisztázatlan')
R('konkordancia/Strongs bővítés', K + 'Strongs bővítés', NEM, '—', None, NA('jegyzetfájl, nem adat'), 'szabad szöveges ötletlista (nem adatkészlet)')
R('adat/jeloltek.tsv', A + 'jeloltek.tsv', NEM, 'motívum-ID + igehely (jelölt, döntéssel)', None, SOR(A + 'jeloltek.tsv', 1),
  'CLAUDE.md 2. szabály: keresési találatból nem lehet közvetlenül megjelenített adat; a jelölt döntés nélkül nem „adat”; a pilot csak az elofordulasok.tsv döntött sorait mutatja')
R('adat/kulcsszavak.tsv', A + 'kulcsszavak.tsv', NEM, 'tanulmány + igehely + Strong', None, SOR(A + 'kulcsszavak.tsv', 1), 'átmeneti tábla (tanulmány → adat átjáró); motívum-kontextus')
R('adat/lexikon_hivatkozasok.tsv', A + 'lexikon_hivatkozasok.tsv', NEM, 'Strong + szótár + jelentés-szám', None, H(A + 'lexikon_hivatkozasok.tsv', 0),
  'a BDB-szócikk jelentés-soraiként ugyanazt adja, mint a BDB_teljes_unabridged, amelyből a pilot saját bontást végez (nem duplikáljuk)')
R('adat/auditok.tsv', A + 'auditok.tsv', NEM, 'motívum-ID + lépés', None, NA('lekérdezés-napló'), 'a motívumkutatás nyoma; nincs vers- vagy szó-kulcsa')
R('adat/res_forras.tsv', A + 'res_forras.tsv', NEM, 'motívum-ID + rés', None, NA('lexikonoldal-generálás'), 'a lexikonoldalak réseinek forrás-megfeleltetése; nem tartalmi adat')
R('adat/bdb_igehely_javitas.tsv', A + 'bdb_igehely_javitas.tsv', NEM, 'Strong + BDB-hivatkozás', None, H(A + 'bdb_igehely_javitas.tsv', 0), 'a BDB-hivatkozások fejezetszám-javítása (#56); a pilot nem használ BDB-igehely hivatkozást')
R('adat/datasetek.tsv', A + 'datasetek.tsv', NEM, 'study-típus + dataset', None, NA('policy-tábla'), 'kötelezőségi tábla a tanulmányokhoz, nem tartalmi adat')
R('adat/dontes_hatas.tsv', A + 'dontes_hatas.tsv', NEM, 'döntés + fájl', None, NA('döntés-nyilvántartás'), 'folyamat-tábla, nem tartalmi adat')
R('adat/kiejtes_{szabalyok,kivetelek,heber_jeloltszabalyok,heber_kivetelek}.tsv', A + 'kiejtes_*.tsv', NEM, 'átírási szabály / kivétel', None, NA('szabálytábla'),
  'a kiejtés (magyaros átírás) a szabályok futtatásával jönne létre, azaz új adat: a pilot nem állít elő új adatot; a jóváhagyott kivételek lexikonoldali megjelenítése a render dolga')
R('adat/SEMA.md, kulso/LICENC.md és társai', A + '{SEMA.md, kulso/*LICENC*, kulso/oshb_HebrewMorphologyCodes.html}', NEM, '—', None, NA('dokumentáció'), 'nem adatkészlet (a morf-jelkulcs HTML-je a morf_kulcs_heber.tsv forrása)')

# ------------------------------------------------------------------ a fájlok teljes listája (ellenőrzés: minden adatfájl szerepel-e)
KIHAGY = re.compile(r'(README|_README|\.md$|\.py$|LICENC|\.html$)', re.I)


def fajlok():
    ki = []
    for rel, ext in (('konkordancia', ('.tsv', '.txt')), ('adat', ('.tsv',))):
        for f in sorted(os.listdir(GY + rel)):
            if f.endswith(ext) or f == 'Strongs bővítés':
                ki.append('%s/%s' % (rel, f))
    for f in sorted(os.listdir(GY + 'konkordancia/LXX_OS')):
        if f.endswith('.tsv'):
            ki.append('konkordancia/LXX_OS/' + f)
    for f in sorted(os.listdir(GY + 'adat/karoli_strong')):
        ki.append('adat/karoli_strong/' + f)
    for f in sorted(os.listdir(GY + 'adat/kulso')):
        ki.append('adat/kulso/' + f)
    return ki


def lefedett(rel):
    """Szerepel-e a fájl valamelyik sor „fajl” mezőjében (a kapcsos zárójeles és csillagos mintákat is feloldva)."""
    nev = os.path.basename(rel)
    stem = re.sub(r'\.(tsv|txt)$', '', nev)
    for s in SOROK:
        f = s['fajl']
        if rel in f or nev in f or stem in f:
            return True
        for m in re.finditer(r'(\S*?)\{([^}]*)\}(\S*)', f):
            for alt in m.group(2).split(','):
                if (m.group(1) + alt.strip() + m.group(3)) == nev or (m.group(1) + alt.strip() + m.group(3)) in rel:
                    return True
        if '*' in f:
            mint = re.escape(f.split('/')[-1].split(',')[0].strip()).replace(r'\*', '.*')
            if re.fullmatch(mint, nev):
                return True
    return False


# ------------------------------------------------------------------ összefoglaló: szó-lapok forrásai
def forrasok_h(d, c):
    ubs_strongs = c['ubs_h']
    return {
        'Strong_szotar (szófaj, rövid jelentés)': lambda s, l: bool(l['szofaj'] or l['rovid']),
        'TAHOT-gyakoriság': lambda s, l: l['elofordulas'] > 0,
        'BDB (angol vagy magyar)': lambda s, l: bool(l['bdb_hu'] or l['bdb_en']),
        'BDB magyarul (modell-kimenet)': lambda s, l: bool(l['bdb_hu']),
        'Károli–Strong páros (modell-kimenet)': lambda s, l: l['karoli_osszes'] > 0,
        'lxx_bridge (görög megfelelő)': lambda s, l: bool(l['lxx']),
        'UBS_DBH előfordulás-jelentés': lambda s, l: s in ubs_strongs,
        'SDBH domén': lambda s, l: bool(l.get('domen')),
        'SECE_H': lambda s, l: bool(l.get('sece')),
        'OSHL (TWOT, BDB-azonosító)': lambda s, l: bool(l.get('oshl')),
        'TBESH': lambda s, l: bool(l.get('tbesh')),
        'tW (translationWords)': lambda s, l: bool(l.get('tw')),
    }


def forrasok_g():
    return {
        'Strong_szotar (szófaj, gloss)': lambda s, l: bool(l['szofaj'] or l['gloss']),
        'TBESG': lambda s, l: bool(l['tbesg']),
        'Thayer (angol)': lambda s, l: bool(l['thayer']),
        'magyar jelentés (Thayer/UBS_DNTG, modell-kimenet)': lambda s, l: bool(l['hu']),
        'TAGNT (ÚSZ-előfordulás)': lambda s, l: l['usz_db'] > 0,
        'lxx_bridge (héber háttér)': lambda s, l: bool(l['heber']),
        'SDGNT domén': lambda s, l: bool(l.get('domen')),
        'UBS_DNTG angol jelentések': lambda s, l: bool(l.get('ubs_en')),
        'LSJ': lambda s, l: bool(l.get('lsj')),
        'MCGED': lambda s, l: bool(l.get('mcged')),
        'SECE_G': lambda s, l: bool(l.get('sece')),
        'tW (translationWords)': lambda s, l: bool(l.get('tw')),
    }


for c in CTX:
    ubs = set()
    for v in c['d']['versek']:
        for w in v['heber']:
            if w['ubs']:
                ubs.add(w['strong'])
    c['ubs_h'] = ubs


def eloszlas(c, nyelv):
    d = c['d']
    lapok = d['lapok'] if nyelv == 'H' else d['gor_lapok']
    fn = forrasok_h(d, c) if nyelv == 'H' else forrasok_g()
    van = {s: [n for n, f in fn.items() if f(s, l)] for s, l in lapok.items()}
    hiany = {n: sorted(s for s, l in lapok.items() if not f(s, l)) for n, f in fn.items()}
    return van, hiany, list(fn)


def lista(xs, n=24):
    xs = list(xs)
    return ', '.join(xs[:n]) + (' … (+%d)' % (len(xs) - n) if len(xs) > n else '') if xs else '—'


TW_CIKK = sum(1 for _ in sorok(K + 'tW_szocikkek.tsv'))
TW_STRONG = len(tw_strongs())
BRIDGE_MIN = min(int(r[2]) for r in sorok(A + 'kulso/lxx_bridge.tsv') if len(r) > 2 and r[2].isdigit())

# ------------------------------------------------------------------ a hiányok kitölthetősége és gazdája (a mérés után, kézzel megítélt, az indoklással)
KITOLT = {
    'BDB magyarul (modell-kimenet)': ('nem: új adat (nyelvi modell fordítása) kell', '#38 (BDB magyar fordítás, fut)'),
    'BDB (angol vagy magyar)': ('igen, meglévő táblából: BDB_strong_alias (a pilot most bővítve pótolja, jelezve)', '#57 (BDB Strong-pótlás, kész)'),
    'Károli–Strong páros (modell-kimenet)': ('nem: új adat (párosítás) kell; a nem párosított szó a Károli-szövegben nincs kötve', '#22 (Károli–Strong párosítás; a Zsoltárok csak egy modellel, „alacsony” bizonyosság)'),
    'lxx_bridge (görög megfelelő)': ('nem: a híd-tábla legkisebb darabszáma %d, vagyis a ritkább párt nem tartalmazza; a LXX_versszintu_parok csak együttelőfordulás (nem szóillesztés), tehát nem pótolja' % BRIDGE_MIN, 'nincs gazdája (adat-határ)'),
    'lxx_bridge (héber háttér)': ('nem: ugyanaz a határ', 'nincs gazdája (adat-határ)'),
    'UBS_DBH előfordulás-jelentés': ('nem: a DBH a szókincs kb. 90%-át fedi (üres eredmény nem negatív lelet)', 'nincs gazdája (a forrás határa)'),
    'SDBH domén': ('nem: ugyanaz a forrás-határ; az UBS_DBH-ban sincs (lásd az alábbi mérést)', 'nincs gazdája (a forrás határa)'),
    'SDGNT domén': ('nem: ugyanaz a forrás-határ', 'nincs gazdája (a forrás határa)'),
    'UBS_DNTG angol jelentések': ('nem: ugyanaz a forrás-határ', 'nincs gazdája (a forrás határa)'),
    'magyar jelentés (Thayer/UBS_DNTG, modell-kimenet)': ('nem: új adat (fordítás) kell', '#7 (Thayer magyar fordítás, halasztva), #28 (lexikon-szócikkek emelése)'),
    'TAGNT (ÚSZ-előfordulás)': ('nem hiány: a szó a TAGNT-kivonat szerint az ÚSZ-ben nem fordul elő', '—'),
    'SECE_H': ('nem: a tábla nem ad sort', 'nincs gazdája (a forrás határa)'),
    'SECE_G': ('nem: a tábla nem ad sort', 'nincs gazdája (a forrás határa)'),
    'OSHL (TWOT, BDB-azonosító)': ('nem: a tábla nem ad sort', 'nincs gazdája (a forrás határa)'),
    'TBESH': ('nem: a tábla nem ad sort', 'nincs gazdája (a forrás határa)'),
    'LSJ': ('nem: a tábla nem ad sort', 'nincs gazdája (a forrás határa)'),
    'MCGED': ('nem: a tábla nem ad sort', 'nincs gazdája (a forrás határa)'),
    'TBESG': ('nem: a tábla nem ad sort', 'nincs gazdája (a forrás határa)'),
    'Thayer (angol)': ('nem: a tábla nem ad sort', 'nincs gazdája (a forrás határa)'),
    'tW (translationWords)': ('nem: a tW %d szócikke összesen %d Strong-számot fed, a többihez nincs szócikk' % (TW_CIKK, TW_STRONG), 'nincs gazdája (a forrás határa)'),
    'Strong_szotar (szófaj, rövid jelentés)': ('—', '—'),
    'Strong_szotar (szófaj, gloss)': ('—', '—'),
    'TAHOT-gyakoriság': ('—', '—'),
}

# ------------------------------------------------------------------ a jelentés összeállítása
sor_ki = []
w = sor_ki.append
szcimek = [c['cim'] for c in CTX]
scope = ' + '.join(szcimek)
w('<!-- GENERÁLT: eszkozok/olvaso_pilot/felmeres.py — kézzel nem szerkesztendő. -->')
w('# Olvasói pilot — az adatkészletek felmérése (F60.5, v2)')
w('')
w('*Gép által generált (`eszkozok/olvaso_pilot/felmeres.py`), kézzel nem szerkesztendő. Mért adatállapot: a két szakasz pilot-JSON-ja (`ts`: %s); a táblák olvasásának ideje: %s. A számok a két szakaszra vonatkoznak: %s. A számokat a program méri (táblák és a szakasz-JSON olvasása), nem becsüli.*' %
  (', '.join('%s %s' % (c['cim'], c['ts_json']) for c in CTX), TS, scope))
w('')
w('**Olvasat.** *Pilot*: `igen` = a bővítés előtt is használta, `most bővítve` = a v2 (F60.5) óta használja, `nem` = nem használja (az ok az utolsó oszlopban). *Kulcs*: mi köti az adatot a laphoz (Strong = szó-lap, vers = vers-lap, szó = a vers szavai). *Lefedettség*: hány a szakasz szó-lapjai (H = héber, G = görög) / versei / szavai közül kap sort az adott táblából; „n/a” = a tábla nem erről a könyvről szól vagy nem kulcsolható. *Licenc*: `adat/licencek.tsv`, szögletes zárójelben a figyelmeztető jelzések (tisztázatlan, nem kereskedelmi, share-alike). *Proveniencia*: a mérés saját lekérdezés-sora.')
w('')

# --- 1. összkép
db = Counter(s['pilot'] for s in SOROK)
w('## 1. Összkép')
w('')
w('- A felmért sor: %d (egy sor = egy adatkészlet vagy egy összetartozó fájlcsoport). Pilot-használat: **%d igen**, **%d most bővítve**, **%d nem**.' % (len(SOROK), db[IGEN], db[UJ], db[NEM]))
fl = fajlok()
lef = [f for f in fl if lefedett(f)]
nincs = [f for f in fl if not lefedett(f)]
w('- Fájl-ellenőrzés: a `konkordancia/*.tsv|txt`, a `konkordancia/LXX_OS/*.tsv`, az `adat/*.tsv`, az `adat/karoli_strong/*` és az `adat/kulso/*` összesen %d fájl; ebből %d szerepel valamelyik sorban%s.' %
  (len(fl), len(lef), '; **nem szerepel: ' + ', '.join(nincs) + '**' if nincs else ' (mind)'))
for c in CTX:
    w('- %s: JSON %s bájt; %d vers, %d héber + %d görög szó-lap.' % (c['cim'], format(c['json_bajt'], ',').replace(',', ' '), len(c['versek']), len(c['heb']), len(c['gor'])))
w('')

# --- 2. táblázat
w('## 2. Adatkészletek sorról sorra')
w('')
fej = '| Adatkészlet | Fájl | Pilot | Kulcs | ' + ' | '.join('Lefedettség: ' + x for x in szcimek) + ' | Licenc | Proveniencia (a mérésé) | Megjegyzés, ok |'
w(fej)
w('|' + '---|' * (7 + len(CTX)))
for s in SOROK:
    mer = [s['mero'](c) for c in CTX]
    prov = '`scope=%s | forras=%s | ts=%s`' % (scope, s['fajl'].replace('|', '/'), TS)
    cella = lambda t: t.replace('|', '/')
    w('| %s | `%s` | %s | %s | %s | %s | %s | %s |' % (cella(s['nev']), s['fajl'], s['pilot'], s['kulcs'], ' | '.join(cella(m) for m in mer), cella(s['lic']), prov, cella(s['ok']) or '—'))
w('')

# --- 3. szó-lapok forrásszáma
w('## 3. Hány adatforrása van a szó-lapoknak')
w('')
w('Forrás = a szó-lapon megjelenő, Strong-kulcsú tartalmi blokk (héber: 12, görög: 12 lehetséges). A „van” a mért tartalom: nem üres mező a szakasz-JSON-ban. A magyar BDB és a Károli–Strong párosítás modell-kimenet, a többi forrásadat.')
w('')
for nyelv, nev in (('H', 'héber'), ('G', 'görög')):
    w('### %s szó-lapok' % nev.capitalize())
    w('')
    ossz_kulon = {}
    for c in CTX:
        van, hiany, fnev = eloszlas(c, nyelv)
        ossz_kulon[c['cim']] = (van, hiany, fnev)
    hdr = '| Adatforrás-szám | ' + ' | '.join('%s (szó-lap)' % x for x in szcimek) + ' |'
    w(hdr)
    w('|' + '---|' * (1 + len(CTX)))
    max_k = len(ossz_kulon[szcimek[0]][2])
    eloszl = {cim: Counter(len(v) for v in van.values()) for cim, (van, _, _) in ossz_kulon.items()}
    for k in range(max_k, -1, -1):
        if any(eloszl[cim].get(k, 0) for cim in szcimek):
            w('| %d | ' % k + ' | '.join(fr(eloszl[cim].get(k, 0), len(ossz_kulon[cim][0])) for cim in szcimek) + ' |')
    w('')
    for cim in szcimek:
        van = ossz_kulon[cim][0]
        ks = [len(v) for v in van.values()]
        w('- %s: min %d, medián %s, max %d forrás / szó-lap (összesen %d lap).' % (cim, min(ks), statistics.median(ks), max(ks), len(ks)))
    w('')
    w('Forrásonként (lefedettség és a hiányzó lapok):')
    w('')
    w('| Adatforrás | ' + ' | '.join('Van: %s' % x for x in szcimek) + ' | Hiányzó lapok (' + ' / '.join(szcimek) + ') | Kitölthető meglévő adattal? | Melyik feladat dolga |')
    w('|' + '---|' * (4 + len(CTX)))
    for n in ossz_kulon[szcimek[0]][2]:
        van_s = []
        hi_s = []
        for cim in szcimek:
            van, hiany, _ = ossz_kulon[cim]
            ossz = len(van)
            van_s.append(fr(ossz - len(hiany[n]), ossz))
            hi_s.append(lista(hiany[n], 18))
        kit = KITOLT.get(n, ('—', '—'))
        w('| %s | %s | %s | %s | %s |' % (n, ' | '.join(van_s), ' / '.join(hi_s), kit[0], kit[1]))
    w('')

# --- 4. a kitölthetőség mérése
w('## 4. Mely hiányok tölthetők ki meglévő adattal?')
w('')
w('Mérés: a hiányzó lapokat a repó más tábláiban kerestük (nem a modell memóriájából).')
w('')
for c in CTX:
    d = c['d']
    alias = {s: l['bdb_alias'] for s, l in d['lapok'].items() if l.get('bdb_alias')}
    sdbh_hi = [s for s, l in d['lapok'].items() if not l.get('domen')]
    ubs_alt = strongs(K + 'UBS_DBH_jelentesek.tsv', 0) | strongs(K + 'UBS_DBH_referenciak.tsv', 1)
    sdgnt_hi = [s for s, l in d['gor_lapok'].items() if not l.get('domen')]
    dntg_alt = strongs(K + 'UBS_DNTG_jelentesek.tsv', 0) | strongs(K + 'UBS_DNTG_referenciak.tsv', 1)
    hu_hi = [s for s, l in d['lapok'].items() if not l['bdb_hu']]
    w('- **%s**' % c['cim'])
    w('  - BDB-szócikk: a saját szócikk nélküli Strong-számok alias-szal pótolva: %s (%s). Alias nélkül maradt (sem magyar, sem angol): %s.' %
      (len(alias), ', '.join('%s→%s (%s, %s)' % (s, a['tabla_strong'], a['bdb_id'], a['hasonlosag']) for s, a in sorted(alias.items())) or '—',
       lista([s for s, l in d['lapok'].items() if not l['bdb_hu'] and not l['bdb_en']])))
    w('  - Magyar BDB-szócikk hiányzik: %s lap; ezek közül angol szócikk van: %s (az angol szöveg a lapon megjelenik; a magyar új adat: #38).' %
      (len(hu_hi), len([s for s in hu_hi if d['lapok'][s]['bdb_en']])))
    w('  - SDBH-domén hiányzik %d lapról; ebből van más UBS_DBH-táblában (jelentések/referenciák): %d → **%s**.' % (len(sdbh_hi), len([s for s in sdbh_hi if s in ubs_alt]), 'kitölthető' if any(s in ubs_alt for s in sdbh_hi) else 'nem kitölthető (a másik tábla is üres)'))
    w('  - SDGNT-domén hiányzik %d görög lapról; ebből van az UBS_DNTG-táblákban: %d → **%s**.' % (len(sdgnt_hi), len([s for s in sdgnt_hi if s in dntg_alt]), 'kitölthető' if any(s in dntg_alt for s in sdgnt_hi) else 'nem kitölthető (a másik tábla is üres)'))
    st = d['stat']
    w('  - Versszintű hiány: BSB-sor hiányzik %d versről (%s); KJV-sor: %d versről; Nave: %d versről; LXX_OS-szó hiányzik: %s.' %
      (len(c['versek']) - st['bsb_vers'], lista([v['igehely'] for v in d['versek'] if not v['angol']['bsb']['szavak']]),
       len(c['versek']) - st['kjv_vers'], len(c['versek']) - st['nave_vers'], lista([v['igehely'] for v in d['versek'] if not v['lxx']])))
w('')

# --- 5. versszámozás
w('## 5. Versszámozás: az összefoglaló nyitott megállapítása')
w('')
for c in CTX:
    d = c['d']
    ell = [v['igehely'] for v in d['versek'] if v['versszam']['tabla_ellentmond']]
    w('- %s: a versmegfeleltető tábla KJV-oszlopa és a pilot KJV-kulcsa (az LXX_OS KJV-oszlopa, a KJV-szöveggel egyező) eltér %d versen%s.' %
      (c['cim'], len(ell), ': ' + lista(ell, 6) if ell else ''))
w('')
w('A Károli-szöveg a feliratos zsoltárokat az MT szerint számozza (a felirat a 22:1), a KJV a feliratot számozás nélkül hagyja (a „My God, my God” a KJV 22:1, a Károli 22:2). A `Karoli_versmegfeleltetes.tsv` és a `LXX_versificacios_terkep.tsv` a Zsolt 22-re Károli = KJV azonosságot ad; a `Nave_basokant.tsv` `karoli_allapot` oszlopa ezt örökli (a 22:1 hivatkozás „azonos”-nak jelölt). A pilot a KJV-kulcsot az LXX_OS KJV-oszlopából veszi (a hiányzó versre a fejezet eltolásával), és a vers-lapon jelzi az ellentmondást; a táblákat nem javítja. A feliratos zsoltárok többi része (kb. 60+ zsoltár) ugyanígy érintett lehet: **ez feladatot igényel (a jelentésben mint nyitott kérdés).**')
w('')
w('*Korlát:* a Nave `Ps 22:1` „AIJELETH SHAHAR — See TITLE” sora a KJV-felirat hivatkozása lehet (a Nave a feliratot nem számozza külön); a pilot KJV-számozás szerint a Károli 22:2-re teszi.')
w('')
open(args.ki, 'w', encoding='utf-8', newline='\n').write('\n'.join(sor_ki) + '\n')
print('kész:', args.ki, len(SOROK), 'sor; fájl-ellenőrzés: %d fájlból %d szerepel; nem szerepel: %s' % (len(fl), len(lef), nincs))
